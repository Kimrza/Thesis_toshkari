"""DATA-07 re-acquisition of the Phase 1 prepared VTEC product, 2022-01-01 to 2022-11-30.

Purpose
-------
`team.md` § Walking Skeleton (DATA-07) and D-52: the eleven non-December months of the Phase 1
evidence are `derived_only`. No provider byte stream was kept, so their provenance is
unverifiable in principle, and FULL must not be relied on at a freeze gate until a
re-acquisition records the provider bytes. The Student authorized this re-acquisition on
2026-10-01, with the Madrigal identity supplied through environment variables.

The request reproduces the governed acquisition (D-3/D-144; `configs/data.yaml` `acquisition`:
instrument 8000, kindat 3500, parameters `ut1_unix, gdlat, glon, tec, dtec`). There is one
`isprint` extraction per daily experiment file, over the union bounding box of the three
frozen cells (the original notebook's request). Two things are added:
- each request carries a UT time filter bounding it to its own day, so no record dated
  2022-12-01 or later can arrive (BLK-07; D-15);
- the provider FILE requested for each day is exactly the one the original acquisition
  recorded (the `file` column of that month's `madrigal_coverage_raw_records.csv`), so the
  D-64 version mix declared in `configs/data.yaml` is reproduced, never re-chosen.

A day whose recorded file the provider no longer serves is surfaced, never substituted.

Each response is written as received, to `raw/<date>__<provider basename>.isprint.txt`. Each
record carries the full provider filename with its version suffix, the provider's
category and status for that file, the retrieval date, and the SHA-256 of the exact response
bytes (team.md DATA-07 obligation). Retrieval goes through
`src.data.acquisition.RetrievalClient`: bounded retry, completeness before hash, and divergence
recorded rather than overwritten (SEC-A-02).

Inputs
------
`--config configs/` (the acquisition identity, stations and cell rule) and the month evidence
under `evidence/audit_evidence_2022-MM/`. The Madrigal identity is read from
`MADRIGAL_USER_FULLNAME`, `MADRIGAL_USER_EMAIL` and `MADRIGAL_USER_AFFILIATION`. It is sent only
inside requests. It is never written, logged, hashed into a record, or echoed (NFR-SEC-01;
Known-defects row 13).

Re-run behaviour
----------------
Resumable. `day_records.jsonl` is append-only. A day whose last record is `complete` and whose
stored file still hashes to that record is skipped. `--plan` contacts no provider and prints
the per-day plan. `--days N` stops after N retrievals (a pilot). At the end,
`request_manifest.json` and `sha256_manifest.json` summarise every complete day, and they are
rewritten by every run that completes. Exit 0 means every planned day is complete. Exit 2
means some day is incomplete or was refused; that is recorded and non-fatal to the days
already done. Exit 1 is an integrity failure.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Final

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.data.acquisition import (  # noqa: E402
    AcquisitionError,
    RetrievalClient,
    TransportResult,
    guard_egress,
)
from src.data.config import IntegrityError  # noqa: E402

MADRIGAL_URL: Final[str] = "https://cedar.openmadrigal.org"
IDENTITY_VARIABLES: Final[tuple[str, str, str]] = (
    "MADRIGAL_USER_FULLNAME",
    "MADRIGAL_USER_EMAIL",
    "MADRIGAL_USER_AFFILIATION",
)
#: Measured on cedar.openmadrigal.org: one binned-TEC isprint costs about 160-180 s of
#: server-side extraction (the coverage notebook's cost model). An operational bound, not
#: a scientific value; the 60 s retrieval-policy default would never complete a call.
ISPRINT_READ_TIMEOUT_S: Final[float] = 900.0
LISTING_READ_TIMEOUT_S: Final[float] = 600.0
FIRST_DAY: Final[dt.date] = dt.date(2022, 1, 1)
LAST_DAY: Final[dt.date] = dt.date(2022, 11, 30)
OUT_DIR: Final[Path] = Path("evidence") / "madrigal_reacquisition_2022"
_ERROR_MARKERS: Final[tuple[str, ...]] = (
    "<html", "<!doctype", "traceback", "error occurred", "invalid", "exception",
)
_ROW: Final[re.Pattern[str]] = re.compile(r"^\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$")


def _identity() -> dict[str, str]:
    missing = [name for name in IDENTITY_VARIABLES if not os.environ.get(name, "").strip()]
    if missing:
        raise IntegrityError(
            "Madrigal identity",
            f"environment variable(s) {missing} are not set; CEDAR's rules of the road "
            f"require a real identity on every request, and it is supplied by the Student "
            f"through the environment only (never a file)",
        )
    return {
        "user_fullname": os.environ["MADRIGAL_USER_FULLNAME"].strip(),
        "user_email": os.environ["MADRIGAL_USER_EMAIL"].strip(),
        "user_affiliation": os.environ["MADRIGAL_USER_AFFILIATION"].strip(),
    }


def _acquisition_identity(config_dir: Path) -> dict[str, Any]:
    import yaml

    data = yaml.safe_load((config_dir / "data.yaml").read_text(encoding="utf-8"))
    acquisition = data["acquisition"]
    stations = data["stations"]
    cells = {
        name: (int(float(cfg["lat"]) // 1), int(float(cfg["lon"]) // 1))
        for name, cfg in stations.items()
    }
    return {
        "experiment": int(acquisition["experiment"]),
        "kindat": int(acquisition["kindat"]),
        "parameters": [str(p) for p in acquisition["parameters"]],
        "cells": cells,
    }


def recorded_files_by_day(evidence_root: Path) -> dict[str, dict[str, str]]:
    """The provider file each 2022-01-01..11-30 day was ORIGINALLY acquired from.

    Read from the `file` and `experiment_id` columns of every non-December month's raw
    records, keyed by the record's own `date` (never a folder name). A day carrying two
    different files is refused (D-64 measured none).
    """
    out: dict[str, dict[str, str]] = {}
    for month in range(1, 12):
        path = evidence_root / f"audit_evidence_2022-{month:02d}" / "madrigal_coverage_raw_records.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                day = dt.date.fromisoformat(row["date"])
                if not FIRST_DAY <= day <= LAST_DAY:
                    continue
                entry = {"file": row["file"], "experiment_id": row["experiment_id"]}
                prior = out.get(day.isoformat())
                if prior is not None and prior != entry:
                    raise IntegrityError(
                        path,
                        f"{day} carries two recorded provider files {prior} and {entry}; "
                        f"D-64 measured one file per day",
                    )
                out[day.isoformat()] = entry
    expected = (LAST_DAY - FIRST_DAY).days + 1
    if len(out) != expected:
        missing = [
            (FIRST_DAY + dt.timedelta(days=i)).isoformat()
            for i in range(expected)
            if (FIRST_DAY + dt.timedelta(days=i)).isoformat() not in out
        ]
        raise IntegrityError(
            evidence_root,
            f"{len(missing)} day(s) have no recorded provider file: {missing[:10]}; the "
            f"re-acquisition requests the recorded file, so such a day cannot be planned",
        )
    return out


def _session() -> Any:
    import requests

    session = requests.Session()
    session.headers["User-Agent"] = "TEC-thesis DATA-07 re-acquisition (requests)"
    return session


def _get(session: Any, service: str, params: Mapping[str, Any], *, timeout: float) -> Any:
    response = session.get(f"{MADRIGAL_URL}/{service}", params=dict(params), timeout=(30, timeout))
    if response.status_code != 200:
        raise OSError(f"{service} returned HTTP {response.status_code}")
    return response


def list_file_rows(session: Any, experiment_id: str) -> list[dict[str, str]]:
    """`getExperimentFilesService.py`: name, kindat, description, category, status, ..."""
    text = _get(
        session, "getExperimentFilesService.py", {"id": experiment_id},
        timeout=LISTING_READ_TIMEOUT_S,
    ).text
    rows = []
    for line in text.splitlines():
        parts = line.split(",")
        if len(parts) >= 5:
            rows.append(
                {
                    "name": parts[0],
                    "kindat": parts[1],
                    "kindat_description": parts[2],
                    "category": parts[3],
                    "status": parts[4],
                }
            )
    return rows


def isprint_parms(parameters: list[str]) -> str:
    """`isprintService.py` takes parameters space-separated; a comma-joined value reaches
    the server as one name and is refused ("OSError: Illegal parameter: ut1_unix,gdlat,...",
    measured 2026-10-02, which made every pilot day `incomplete`)."""
    return " ".join(parameters)


def isprint_filters(day: dt.date, bbox: Mapping[str, int]) -> str:
    stamp = day.strftime("%m/%d/%Y")
    return (
        f"date1={stamp} time1=00:00:00 date2={stamp} time2=23:59:59 "
        f"filter=gdlat,{bbox['lat_min']},{bbox['lat_max']} "
        f"filter=glon,{bbox['lon_min']},{bbox['lon_max']}"
    )


def check_isprint_body(data: bytes, day: dt.date) -> dict[str, Any]:
    """Completeness of one response: readable, five numeric columns, every row on `day`."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        return {"complete": False, "reason": f"not UTF-8 ({exc})"}
    head = text.lstrip()[:2000].lower()
    if not text.strip() or any(marker in head for marker in _ERROR_MARKERS):
        return {"complete": False, "reason": "empty body or a server error page"}
    rows = 0
    start = dt.datetime.combine(day, dt.time(0), dt.timezone.utc).timestamp()
    for line in text.splitlines():
        if not line.strip():
            continue
        match = _ROW.match(line)
        if not match:
            return {"complete": False, "reason": f"unparseable line {line[:60]!r}"}
        ut1 = float(match.group(1))
        if not start <= ut1 < start + 86400:
            return {"complete": False, "reason": f"record at ut1 {ut1} lies outside {day}"}
        rows += 1
    if rows == 0:
        return {"complete": False, "reason": "no record"}
    return {"complete": True, "rows": rows}


def make_transport(session: Any, identity: Mapping[str, str], parameters: list[str]) -> Any:
    def transport(spec: Mapping[str, Any], offset: int, timeout: float) -> TransportResult:
        del offset, timeout  # isprint is not resumable; its read bound is ISPRINT_READ_TIMEOUT_S
        params = {
            "file": spec["provider_path"],
            "parms": isprint_parms(parameters),
            "filters": spec["filters"],
            **identity,
        }
        data = _get(session, "isprintService.py", params, timeout=ISPRINT_READ_TIMEOUT_S).content
        check = check_isprint_body(data, dt.date.fromisoformat(spec["date"]))
        return TransportResult(
            data=data, complete=bool(check["complete"]), provider_filename=spec["provider_path"]
        )

    return transport


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _last_records(log: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    if log.is_file():
        for line in log.read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                out[str(record["date"])] = record
    return out


def _append(log: Path, record: Mapping[str, Any]) -> None:
    safe = guard_egress(dict(record), context=f"day_record[{record.get('date')}]")
    with log.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(safe, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def _manifests(out_dir: Path, ident: Mapping[str, Any], planned: list[str]) -> dict[str, Any]:
    records = _last_records(out_dir / "day_records.jsonl")
    complete = {d: r for d, r in records.items() if r.get("status") == "complete"}
    files = {
        f"raw/{r['logical_name']}": r["sha256"] for r in sorted(complete.values(), key=lambda r: r["date"])
    }
    manifest = {
        "kind": "madrigal_reacquisition_request_manifest",
        "provider": "CEDAR Madrigal (cedar.openmadrigal.org)",
        "citation": "D-6 (Madrigal / MIT Haystack citation and acknowledgement)",
        "experiment": ident["experiment"],
        "kindat": ident["kindat"],
        "parameters": ident["parameters"],
        "transport": "HTTP isprintService.py via requests (no madrigalWeb client)",
        "identity_handling": (
            "Madrigal user identity sent in requests only, from environment variables; never "
            "recorded (NFR-SEC-01; Known-defects row 13)"
        ),
        "window": [FIRST_DAY.isoformat(), LAST_DAY.isoformat()],
        "days_planned": len(planned),
        "days_complete": len(complete),
        "days_not_complete": sorted(set(planned) - set(complete)),
        "suffix_mismatches": sorted(d for d, r in complete.items() if r.get("suffix_mismatch")),
        "provenance_class": "full",
    }
    (out_dir / "request_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    files["day_records.jsonl"] = _sha256(out_dir / "day_records.jsonl")
    files["request_manifest.json"] = _sha256(out_dir / "request_manifest.json")
    (out_dir / "sha256_manifest.json").write_text(
        json.dumps(files, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def run(config_dir: Path, *, plan_only: bool, max_days: int | None) -> int:
    workspace = REPO_ROOT
    ident = _acquisition_identity(config_dir)
    recorded = recorded_files_by_day(workspace / "evidence")
    lats = [lat for lat, _ in ident["cells"].values()]
    lons = [lon for _, lon in ident["cells"].values()]
    bbox = {"lat_min": min(lats), "lat_max": max(lats) + 1, "lon_min": min(lons), "lon_max": max(lons) + 1}
    planned = sorted(recorded)
    out_dir = workspace / OUT_DIR
    raw_dir = out_dir / "raw"
    log = out_dir / "day_records.jsonl"
    if plan_only:
        suffixes: dict[str, int] = {}
        for entry in recorded.values():
            token = re.search(r"([a-z])\.(\d{3})\.hdf5$", entry["file"])
            key = f"{token.group(1)}.{token.group(2)}" if token else "unrecognised"
            suffixes[key] = suffixes.get(key, 0) + 1
        print(json.dumps({"days": len(planned), "bbox": bbox, "suffixes": suffixes,
                          "first": planned[0], "last": planned[-1]}, indent=2))
        return 0
    identity = _identity()
    session = _session()
    client = RetrievalClient(make_transport(session, identity, ident["parameters"]), min_interval_s=2.0)
    raw_dir.mkdir(parents=True, exist_ok=True)
    previous = _last_records(log)
    listings: dict[str, list[dict[str, str]]] = {}
    done = 0
    for day_text in planned:
        prior = previous.get(day_text)
        if prior and prior.get("status") == "complete":
            path = raw_dir / prior["logical_name"]
            if path.is_file() and _sha256(path) == prior["sha256"]:
                continue
        if max_days is not None and done >= max_days:
            break
        day = dt.date.fromisoformat(day_text)
        entry = recorded[day_text]
        provider_path = entry["file"]
        basename = Path(provider_path).name
        logical = f"{day_text}__{basename}.isprint.txt"
        record: dict[str, Any] = {
            "date": day_text,
            "experiment_id": entry["experiment_id"],
            "recorded_provider_filename": provider_path,
            "logical_name": logical,
            "request": {
                "service": "isprintService.py",
                "parms": isprint_parms(ident["parameters"]),
                "filters": isprint_filters(day, bbox),
            },
        }
        try:
            if entry["experiment_id"] not in listings:
                listings[entry["experiment_id"]] = list_file_rows(session, entry["experiment_id"])
            rows = [r for r in listings[entry["experiment_id"]] if r["kindat"] == str(ident["kindat"])]
            record["provider_listing_kindat"] = rows
            served = next((r for r in rows if r["name"] == provider_path), None)
            if served is None:
                record["status"] = "recorded_file_not_served"
                _append(log, record)
                print(f"{day_text}: recorded file {basename} is not served now", file=sys.stderr)
                done += 1
                continue
            record["provider_category"] = served["category"]
            record["provider_status"] = served["status"]
            result = client.retrieve(
                {
                    "provider": "CEDAR Madrigal",
                    "permanent_citation": f"{MADRIGAL_URL} instrument {ident['experiment']} kindat {ident['kindat']}",
                    "location_date": day_text,
                    "logical_name": logical,
                    "provider_path": provider_path,
                    "filters": record["request"]["filters"],
                    "date": day_text,
                },
                dest_dir=raw_dir,
                prior_record=(
                    {"provider_filename": prior.get("provider_filename"), "sha256": prior.get("sha256")}
                    if prior and prior.get("sha256") else {"provider_filename": provider_path}
                ),
            )
            record.update(result)
            if result.get("status") == "complete":
                check = check_isprint_body((raw_dir / logical).read_bytes(), day)
                record["rows"] = check.get("rows")
                record["bytes"] = (raw_dir / logical).stat().st_size
        except AcquisitionError as exc:
            record["status"] = "retry_exhausted"
            record["reason"] = str(exc)
        record["retrieved_at_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
        _append(log, record)
        print(f"{day_text}: {record.get('status')} rows={record.get('rows')}", flush=True)
        done += 1
    manifest = _manifests(out_dir, ident, planned)
    print(json.dumps({k: manifest[k] for k in ("days_planned", "days_complete")}))
    return 0 if manifest["days_complete"] == manifest["days_planned"] else 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--plan", action="store_true", help="print the plan; contact no provider")
    parser.add_argument("--days", type=int, default=None, help="stop after N retrievals (pilot)")
    args = parser.parse_args(argv)
    try:
        return run(args.config, plan_only=args.plan, max_days=args.days)
    except IntegrityError as exc:
        print(f"acquire_madrigal_reacquisition_2022: refused: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
