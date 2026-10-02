"""The DATA-07 re-acquisition, read back: verify, parse, select, compare (stage 00 full year).

Purpose
-------
`scripts/acquire_madrigal_reacquisition_2022.py` stores one Madrigal `isprint` response per day
of 2022-01-01..11-30 as received, with its full provider filename (version suffix included),
its retrieval date and the SHA-256 of the exact bytes. This module is the governed pipeline's
read path over that evidence, used by stage 00's full-year run:

1. `verify_reacquisition` re-hashes every stored response and the day log against the
   evidence's `sha256_manifest.json`. A disagreement fails, naming the file.
2. `parse_isprint` reads the five provider columns from a response, verbatim.
3. `select_cell_records` keeps the rows of the three frozen cells (D-1 / D-33 floor rule,
   `src.data.prepared.cell_of`) and stamps each with its station and record date.
4. `compare_with_prior_records` is the DATA-07 check the re-acquisition exists for. It compares
   the re-acquired rows, per station, timestamp and value, against the derived evidence the
   pipeline relied on until now (`evidence/audit_evidence_2022-MM/madrigal_coverage_raw_records.csv`).
   The result is machine-readable counts: equal, different, only in the re-acquisition, only in
   the prior evidence. A difference is recorded, never hidden and never fatal. The
   re-acquisition cannot prove the original bytes, and a disagreement is the finding.

Inputs: the evidence directory and the config-resolved station cells. Re-run behaviour: pure
functions; nothing is written here.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Final

from src.data.config import IntegrityError
from src.data.prepared import cell_of

PROVIDER_FIELDS: Final[tuple[str, ...]] = ("ut1_unix", "gdlat", "glon", "tec", "dtec")
#: The prior evidence's floats were re-serialised by pandas from the same provider text; equal
#: values agree to well inside this relative bound, and anything wider is a real difference.
PRIOR_VALUE_RTOL: Final[float] = 1e-9


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_reacquisition(evidence_dir: Path) -> dict[str, Any]:
    """Re-hash the evidence against its manifest; return the complete day records by date."""
    evidence_dir = Path(evidence_dir)
    manifest_path = evidence_dir / "sha256_manifest.json"
    if not manifest_path.is_file():
        raise IntegrityError(manifest_path, "the re-acquisition has no sha256_manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for rel, digest in sorted(manifest.items()):
        path = evidence_dir / rel
        if not path.is_file():
            raise IntegrityError(path, "listed in the re-acquisition manifest but absent")
        actual = _sha256(path)
        if actual != digest:
            raise IntegrityError(
                path, f"hashes to {actual}, the re-acquisition manifest records {digest}"
            )
    records: dict[str, dict[str, Any]] = {}
    for line in (evidence_dir / "day_records.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            records[str(record["date"])] = record
    complete = {d: r for d, r in records.items() if r.get("status") == "complete"}
    for day, record in complete.items():
        rel = f"raw/{record['logical_name']}"
        if manifest.get(rel) != record.get("sha256"):
            raise IntegrityError(
                evidence_dir / rel,
                f"day {day}'s record hash {record.get('sha256')} is not the manifest's "
                f"{manifest.get(rel)}",
            )
    request = json.loads((evidence_dir / "request_manifest.json").read_text(encoding="utf-8"))
    return {
        "evidence_dir": evidence_dir,
        "manifest": manifest,
        "request": request,
        "complete": complete,
        "not_complete": sorted(set(records) - set(complete)),
    }


def parse_isprint(text: str) -> list[dict[str, str]]:
    """The five provider columns of one response, as the provider wrote them."""
    rows = []
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) != len(PROVIDER_FIELDS):
            raise IntegrityError(f"isprint line {number}", f"expected 5 columns, got {parts!r}")
        for token in parts:
            float(token)  # every token is numeric, or the response is refused
        rows.append(dict(zip(PROVIDER_FIELDS, parts, strict=True)))
    return rows


def select_cell_records(
    rows: Sequence[Mapping[str, str]], cells: Mapping[str, tuple[int, int]]
) -> tuple[list[dict[str, str]], int]:
    """Rows inside one of the frozen cells, stamped with station and record date."""
    by_cell = {cell: station for station, cell in cells.items()}
    kept: list[dict[str, str]] = []
    outside = 0
    for row in rows:
        station = by_cell.get(cell_of(float(row["gdlat"]), float(row["glon"])))
        if station is None:
            outside += 1
            continue
        moment = dt.datetime.fromtimestamp(float(row["ut1_unix"]), dt.timezone.utc)
        kept.append(
            {
                **row,
                "station": station,
                "date": moment.date().isoformat(),
                "timestamp": moment.isoformat(),
            }
        )
    return kept, outside


def _prior_index(evidence_root: Path, months: Sequence[int]) -> dict[tuple[str, float], tuple[float, float]]:
    index: dict[tuple[str, float], tuple[float, float]] = {}
    for month in months:
        path = evidence_root / f"audit_evidence_2022-{month:02d}" / "madrigal_coverage_raw_records.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                index[(row["station"], float(row["ut1_unix"]))] = (float(row["tec"]), float(row["dtec"]))
    return index


def _close(a: float, b: float) -> bool:
    return abs(a - b) <= PRIOR_VALUE_RTOL * max(abs(a), abs(b), 1e-300)


def compare_with_prior_records(
    records: Sequence[Mapping[str, str]],
    evidence_root: Path,
    *,
    window: tuple[dt.date, dt.date],
) -> dict[str, Any]:
    """DATA-07: re-acquired rows against the derived evidence relied on until now, by key."""
    start, end = window
    lo = dt.datetime.combine(start, dt.time(0), dt.timezone.utc).timestamp()
    hi = dt.datetime.combine(end + dt.timedelta(days=1), dt.time(0), dt.timezone.utc).timestamp()
    prior = {
        k: v
        for k, v in _prior_index(Path(evidence_root), range(start.month, end.month + 1)).items()
        if lo <= k[1] < hi
    }
    fresh = {(str(r["station"]), float(r["ut1_unix"])): (float(r["tec"]), float(r["dtec"])) for r in records}
    shared = sorted(set(prior) & set(fresh))
    different = [k for k in shared if not (_close(prior[k][0], fresh[k][0]) and _close(prior[k][1], fresh[k][1]))]
    by_station: dict[str, dict[str, int]] = {}
    for station in sorted({k[0] for k in set(prior) | set(fresh)}):
        by_station[station] = {
            "prior": sum(1 for k in prior if k[0] == station),
            "reacquired": sum(1 for k in fresh if k[0] == station),
            "equal": sum(1 for k in shared if k[0] == station and k not in different),
            "different": sum(1 for k in different if k[0] == station),
        }
    return {
        "kind": "data07_reacquisition_comparison",
        "window": [start.isoformat(), end.isoformat()],
        "relative_tolerance_for_equal": PRIOR_VALUE_RTOL,
        "prior_records": len(prior),
        "reacquired_records": len(fresh),
        "equal": len(shared) - len(different),
        "different": len(different),
        "only_reacquired": len(set(fresh) - set(prior)),
        "only_prior": len(set(prior) - set(fresh)),
        "by_station": by_station,
        "first_differences": [
            {"station": k[0], "ut1_unix": k[1], "prior": prior[k], "reacquired": fresh[k]}
            for k in different[:20]
        ],
    }
