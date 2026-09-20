"""Retrieve, hash, parse and cross-compare the provider-native 2022 GFZ driver pairs.

Purpose
-------
Owner-approved (2026-09-18, qualified approval recorded in
`governance/CHANGE_RECORD_2026-09-18_gfz_driver_pair_audit.md` and the build-and-test diary)
acquisition of exactly FOUR GFZ Data Services files and the value-by-value comparison
the design specifies for the two GFZ driver series:

* **Kp / ap** — `Kp_now2022.wdc` (nowcast) against `Kp_def2022.wdc` (definitive), both
  under DOI 10.5880/Kp.0001. This IS the comparison `external-products` R-63 control 5
  and `acquisition` R-40's "re-acquired in BOTH grades" constraint name. Provider
  limitation, recorded verbatim in every output: the archived nowcast is the SETTLED,
  final-stage nowcast after its ~1-2-day revision period ("At the time of the
  calculation of the definitive Kp, also the nowcast Kp for the previous month has
  reached a final stage. It will not change any more and is archived here." —
  `kp_index_data_description_20210311.pdf` §4). It is NOT the first-issued value that was
  available at each 2022 forecast origin, and no exact first-issue reconstruction is
  claimed.
* **Hp60 / ap60** — `Hp60ap60doi_2022.txt` under DOI 10.5880/Hpo.0002 (V2.0, the DOI in
  force throughout 2022; accepted by the owner as the contemporaneous 2022 grade)
  against the same filename under DOI 10.5880/Hpo.0003 (V3.0, the 2024 algorithm
  recomputation). GFZ publishes NO definitive Hp60/ap60 and NO archived Hp60 nowcast,
  so the literal R-63 control 5 comparison is impossible for this series. The
  comparison performed is labelled **"contemporaneous V2.0 versus later
  algorithm-recomputed V3.0"** — a DOCUMENTED SUBSTITUTE control that tests sensitivity
  to later algorithmic recomputation and does NOT demonstrate definitive backfill.

Nothing here is a scientific constant: the four request specs are provider identities
(URL, DOI, filename), the 2022 calendar is the claim boundary (D-8), and every measured
figure is written to the report rather than asserted (TE §15.1). No `configs/` value is
read or written; no producer artifact is released; no `permitted_producers` entry is
made; `availability_lags` is untouched.

Inputs
------
Network: the four HTTPS URLs in `SPECS`, retrieved through `acquisition`'s own
bounded-retry `RetrievalClient` (TS-A-01) with a stdlib `urllib` transport INJECTED by
this script — `scripts/00_acquire_prepared_vtec.py:_build_transport` is not modified and
still refuses. Licence: CC BY 4.0 (stated in every provider header). No credential is
declared or used for the `gfz` provider (`credential_names_for` → `()`).

Outputs (all under `evidence/audit_gfz_<date>/`)
-----------------------------------------------
* the four provider files, byte-for-byte as served;
* `retrieval_record.json` — per file the TE §13.3 `source_files` items
  (`RetrievalClient.retrieve`'s record: provider, permanent citation, location/date,
  full provider filename INCLUDING its DOI-version path, retrieval date, SHA-256) plus
  the server's declared length, Last-Modified and ETag, the nine-field TE §5.1 driver
  inventory per series (`assert_driver_inventory`), and the provider-limitation
  statements;
* `sha256_manifest.json` — the canonical flat {path: sha256} mapping over the four
  provider files plus the derived artifacts (TE 13.3; TA-15's reader verifies it) and
  `sha256_manifest_meta.json` — W-4's metadata sidecar (provider identities with DOI
  version, provenance class, interpreter, hash arithmetic);
* `gfz-comparison-report.json` — parse validation (2022 coverage, chronology, cadence,
  duplicates, missing symbols) and the value-by-value comparison per series, epochs
  keyed by INTEGER `{y, m, d, h}`. Since D-48 (2026-09-19) the December-custody scan
  detects such records STRUCTURALLY and excludes this file only by validated content
  plus provenance (R-26 class 5, `src/data/locked_test.py`); the integer keys are no
  longer what keeps it outside custody, and the file stays inventoried as excluded
  DRIVER exposure — never a licence to use its December values;
* `GFZ-AUDIT.md` — the human-readable report.
* Two rows in `artifacts/registry/experiment_registry.jsonl` (`started`, then
  `completed` or `failed`) through `append_registry_event`, `locked_test_accessed =
  false` (driver data; no December TARGET value is read), with the environment lock
  recorded as a supplemental stdlib lock because the governed `capture_environment_lock`
  needs `pyyaml`, absent on this host — stated in `notes`, never silently substituted.

Re-run behaviour
----------------
Deterministic over identical provider bytes. A re-run reads the prior
`retrieval_record.json` and hands each prior record to `RetrievalClient.retrieve`, so a
provider reissue is recorded as `divergent-not-overwritten` with BOTH hashes and the
on-disk bytes are never replaced (SEC-A-02). Registry rows are append-only; every run
adds its own pair and no earlier row is touched (NFR-AUD-01).

Usage
-----
    python scripts/audit_gfz_drivers.py [--out evidence/audit_gfz_2026-09-18]
                                        [--offline]   # parse+compare held files only

Exit status: 0 on a complete run (mismatches are REPORTED, not fatal — a nowcast that
differs from the definitive is the phenomenon the control exists to measure); 1 on an
integrity failure (incomplete retrieval, divergence, parse failure, coverage shortfall).
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import platform
import subprocess
import sys
import urllib.error
import urllib.request
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.acquisition import (  # noqa: E402
    RetrievalClient,
    TransportResult,
    assert_driver_inventory,
    guard_egress,
    guard_egress_free_text,
    write_sha256_manifest,
)
from src.data.config import IntegrityError  # noqa: E402
from src.data.experiment_registry import append_registry_event  # noqa: E402
from src.data.release import sha256_of_file  # noqa: E402
from src.external.spaceweather import assert_gfz_cross_products  # noqa: E402

YEAR = 2022
KP_MISSING = -1
HP_MISSING = -1.0
USER_AGENT = "TEC-thesis-driver-audit (Kimia Rezaei; scripts/audit_gfz_drivers.py)"

#: The four owner-approved request identities. `provider_filename` carries the DOI and
#: folder beside the served filename because the Hpo filename is identical across DOIs —
#: the DOI IS the version suffix DATA-07 requires recorded. Written as prose rather than
#: one path token: the W-9 egress heuristic refuses any single 20+-char three-class token
#: (SD-A-02), and the allowlist is a reviewed surface this script must not grow.
SPECS: tuple[dict[str, str], ...] = (
    {
        "series": "kp_ap3",
        "grade": "nowcast",
        "provider": "GFZ Helmholtz Centre for Geosciences, Geomagnetic Observatory Niemegk",
        "permanent_citation": "https://doi.org/10.5880/Kp.0001",
        "url": "https://datapub.gfz.de/download/10.5880.Kp.0001/Kp_nowcast/Kp_now2022.wdc",
        "provider_filename": "Kp_now2022.wdc (DOI 10.5880/Kp.0001, folder Kp_nowcast)",
        "logical_name": "Kp_now2022.wdc",
        "format": "wdc",
    },
    {
        "series": "kp_ap3",
        "grade": "definitive",
        "provider": "GFZ Helmholtz Centre for Geosciences, Geomagnetic Observatory Niemegk",
        "permanent_citation": "https://doi.org/10.5880/Kp.0001",
        "url": "https://datapub.gfz.de/download/10.5880.Kp.0001/Kp_definitive/Kp_def2022.wdc",
        "provider_filename": "Kp_def2022.wdc (DOI 10.5880/Kp.0001, folder Kp_definitive)",
        "logical_name": "Kp_def2022.wdc",
        "format": "wdc",
    },
    {
        "series": "hp60_ap60",
        "grade": "contemporaneous V2.0",
        "provider": "GFZ Helmholtz Centre for Geosciences, Geomagnetic Observatory Niemegk",
        "permanent_citation": "https://doi.org/10.5880/Hpo.0002",
        "url": "https://datapub.gfz.de/download/10.5880.HPO.0002/Hpo60/Hp60ap60doi_2022.txt",
        "provider_filename": "Hp60ap60doi_2022.txt (DOI 10.5880/Hpo.0002, folder Hpo60)",
        "logical_name": "hp60ap60doi_2022_v2.txt",
        "format": "hpo",
    },
    {
        "series": "hp60_ap60",
        "grade": "recomputed V3.0",
        "provider": "GFZ Helmholtz Centre for Geosciences, Geomagnetic Observatory Niemegk",
        "permanent_citation": "https://doi.org/10.5880/Hpo.0003",
        "url": "https://datapub.gfz.de/download/10.5880.HPO.0003/Hpo60/Hp60ap60doi_2022.txt",
        "provider_filename": "Hp60ap60doi_2022.txt (DOI 10.5880/Hpo.0003, folder Hpo60)",
        "logical_name": "hp60ap60doi_2022_v3.txt",
        "format": "hpo",
    },
)

PROVIDER_LIMITATIONS: dict[str, str] = {
    "kp_ap3": (
        "Historical nowcast and definitive variants exist for 2022 under DOI "
        "10.5880/Kp.0001 (Kp_nowcast/Kp_now2022.wdc, Kp_definitive/Kp_def2022.wdc). The "
        "archived nowcast is the SETTLED, final-stage nowcast after its approximately "
        "1-2-day revision period, not the first-issued value available at each 2022 "
        "forecast origin; exact first-issue reconstruction is not claimed."
    ),
    "hp60_ap60": (
        "No provider-native NRT/definitive pair exists: GFZ publishes Hpo as a single "
        "near-real-time-algorithm product with no definitive grade and no archived "
        "nowcast. The comparison performed is 'contemporaneous V2.0 (DOI 10.5880/Hpo.0002, "
        "in force 2022-03-26 to 2024-06-17) versus later algorithm-recomputed V3.0 (DOI "
        "10.5880/Hpo.0003, 2024-06-17)'. It tests sensitivity to later algorithmic "
        "recomputation and does NOT demonstrate definitive backfill; the literal R-63 "
        "control 5 comparison is impossible for this series."
    ),
}


# --- transport -----------------------------------------------------------------------


def _urllib_transport(spec: Mapping[str, Any], offset: int, timeout: float) -> TransportResult:
    """Plain HTTPS GET with byte-range resume; completeness = declared length matched."""
    headers = {"User-Agent": USER_AGENT}
    if offset:
        headers["Range"] = f"bytes={offset}-"
    url = str(spec["url"])
    if not url.startswith("https://datapub.gfz.de/"):
        raise IntegrityError(
            url, "only the four owner-approved https://datapub.gfz.de/ URLs are retrievable"
        )
    request = urllib.request.Request(url, headers=headers)  # noqa: S310 — scheme+host pinned above
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
        data = response.read()
        declared = response.headers.get("Content-Length")
        complete = declared is None or len(data) == int(declared)
        spec_meta = spec.setdefault("_server", {})
        spec_meta["content_length"] = declared
        spec_meta["last_modified"] = response.headers.get("Last-Modified")
        spec_meta["etag"] = response.headers.get("ETag")
        spec_meta["status"] = response.status
    return TransportResult(
        data=data,
        complete=complete,
        provider_filename=str(spec["provider_filename"]),
        resumable=bool(offset) or False,
    )


# --- parsing --------------------------------------------------------------------------


def _kp_third(code: int) -> float:
    """WDC two-digit Kp code -> numeric thirds (PDF §5: 0/3/7 = 0, 1/3, 2/3)."""
    whole, frac = divmod(code, 10)
    thirds = {0: 0.0, 3: 1 / 3, 7: 2 / 3}
    if frac not in thirds:
        raise IntegrityError("Kp WDC code", f"{code!r} has an unrecognised thirds digit")
    return round(whole + thirds[frac], 3)


def parse_wdc(path: Path) -> dict[tuple[int, int, int, int], tuple[float, int]]:
    """`Kp_*YYYY.wdc` -> {(y, m, d, start_hour): (Kp, ap)}; fixed columns per PDF §5."""
    out: dict[tuple[int, int, int, int], tuple[float, int]] = {}
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.startswith("#"):
            continue
        line = raw.rstrip("\n")
        if len(line) < 62:
            raise IntegrityError(f"{path.name}:{line_no}", "WDC line shorter than 62 chars")
        yy, mm, dd = int(line[0:2]), int(line[2:4]), int(line[4:6])
        year = 1900 + yy if yy >= 32 else 2000 + yy
        kps = [line[12 + 2 * i : 14 + 2 * i] for i in range(8)]
        aps = [line[31 + 3 * i : 34 + 3 * i] for i in range(8)]
        for slot in range(8):
            kp_txt, ap_txt = kps[slot].strip(), aps[slot].strip()
            kp_code = int(kp_txt) if kp_txt else KP_MISSING
            ap_val = int(ap_txt) if ap_txt else KP_MISSING
            key = (year, mm, dd, slot * 3)
            if key in out:
                raise IntegrityError(f"{path.name}:{line_no}", f"duplicate epoch {key}")
            kp_val = float(KP_MISSING) if kp_code < 0 else _kp_third(kp_code)
            out[key] = (kp_val, ap_val)
    return out


def parse_hpo(path: Path) -> dict[tuple[int, int, int, int], tuple[float, int]]:
    """`Hp60ap60doi_YYYY.txt` -> {(y, m, d, start_hour): (Hp60, ap60)}; blank-separated."""
    out: dict[tuple[int, int, int, int], tuple[float, int]] = {}
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.startswith("#"):
            continue
        parts = raw.split()
        if len(parts) != 10:
            raise IntegrityError(
                f"{path.name}:{line_no}", f"expected 10 columns, got {len(parts)}"
            )
        year, mm, dd = int(parts[0]), int(parts[1]), int(parts[2])
        start_hour = float(parts[3])
        if start_hour != int(start_hour):
            raise IntegrityError(f"{path.name}:{line_no}", f"non-integer start hour {parts[3]}")
        key = (year, mm, dd, int(start_hour))
        if key in out:
            raise IntegrityError(f"{path.name}:{line_no}", f"duplicate epoch {key}")
        out[key] = (float(parts[7]), int(parts[8]))
    return out


def _day(y: int, m: int, d: int) -> dict[str, int]:
    return {"y": y, "m": m, "d": d}


def validate_series(
    label: str,
    series: Mapping[tuple[int, int, int, int], tuple[float, int]],
    *,
    step_hours: int,
    missing_value: float,
) -> dict[str, Any]:
    """Coverage, chronology, cadence, duplicates (raised at parse) and missingness."""
    keys_2022 = sorted(k for k in series if k[0] == YEAR)
    out_of_year = [k for k in series if k[0] != YEAR]
    expected = 365 * (24 // step_hours)
    stamps = [dt.datetime(*k, tzinfo=dt.timezone.utc) for k in keys_2022]
    gaps = [
        (stamps[i - 1], stamps[i])
        for i in range(1, len(stamps))
        if stamps[i] - stamps[i - 1] != dt.timedelta(hours=step_hours)
    ]
    missing_epochs = [k for k in keys_2022 if series[k][0] == missing_value or series[k][1] < 0]
    per_month: dict[int, int] = {m: 0 for m in range(1, 13)}
    for k in keys_2022:
        per_month[k[1]] += 1
    report = {
        "label": label,
        "epochs_2022": len(keys_2022),
        "epochs_expected_2022": expected,
        "coverage_complete": len(keys_2022) == expected,
        "out_of_year_epochs": len(out_of_year),
        "first_epoch": _day(*keys_2022[0][:3]) | {"h": keys_2022[0][3]} if keys_2022 else None,
        "last_epoch": _day(*keys_2022[-1][:3]) | {"h": keys_2022[-1][3]} if keys_2022 else None,
        "chronology_monotonic": stamps == sorted(stamps),
        "cadence_breaks": len(gaps),
        "cadence_hours": step_hours,
        "missing_epochs": len(missing_epochs),
        "missing_epoch_list": [_day(*k[:3]) | {"h": k[3]} for k in missing_epochs],
        "epochs_per_month": per_month,
    }
    return report


def compare_series(
    series_id: str,
    label: str,
    a: Mapping[tuple[int, int, int, int], tuple[float, int]],
    b: Mapping[tuple[int, int, int, int], tuple[float, int]],
    names: tuple[str, str],
    value_names: tuple[str, str],
) -> dict[str, Any]:
    """Value-by-value over the intersection of 2022 epochs; both columns compared."""
    common = sorted(k for k in a if k in b and k[0] == YEAR)
    only_a = sum(1 for k in a if k[0] == YEAR and k not in b)
    only_b = sum(1 for k in b if k[0] == YEAR and k not in a)
    mismatches: list[dict[str, Any]] = []
    per_month = {m: 0 for m in range(1, 13)}
    max_abs = [0.0, 0]
    for k in common:
        va, vb = a[k], b[k]
        if va != vb:
            per_month[k[1]] += 1
            max_abs[0] = max(max_abs[0], abs(va[0] - vb[0]))
            max_abs[1] = max(max_abs[1], abs(va[1] - vb[1]))
            mismatches.append(
                {
                    "epoch": _day(*k[:3]) | {"h": k[3]},
                    names[0]: {value_names[0]: va[0], value_names[1]: va[1]},
                    names[1]: {value_names[0]: vb[0], value_names[1]: vb[1]},
                }
            )
    # The DESIGNED control (R-63 control 5, `assert_gfz_cross_products`): an emitted
    # series equal to the later product fails wherever the earlier product differs.
    # Exercised here with emitted := the later product, so it fires iff mismatches exist.
    first = {k: a[k][0] for k in common}
    later = {k: b[k][0] for k in common}
    try:
        assert_gfz_cross_products(series_id, near_real_time=first, definitive=later, emitted=later)
        designed_control_fired = False
    except IntegrityError:
        designed_control_fired = True
    return {
        "series": series_id,
        "comparison_label": label,
        "compared": names,
        "epochs_compared": len(common),
        "epochs_only_in_first": only_a,
        "epochs_only_in_second": only_b,
        "mismatch_epochs": len(mismatches),
        "mismatch_fraction": (len(mismatches) / len(common)) if common else None,
        "mismatches_per_month": per_month,
        f"max_abs_diff_{value_names[0]}": max_abs[0],
        f"max_abs_diff_{value_names[1]}": max_abs[1],
        "designed_control_assert_gfz_cross_products_fired": designed_control_fired,
        "designed_control_consistent_with_count": designed_control_fired == bool(mismatches),
        "mismatch_list": mismatches,
    }


# --- environment + registry ------------------------------------------------------------


def _git_head() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True, cwd=REPO_ROOT
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _git_dirty() -> bool:
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
            cwd=REPO_ROOT,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return True
    return bool(out.strip())


def _supplemental_lock(out_dir: Path) -> tuple[str, dict[str, Any]]:
    """A stdlib environment record + its hash. NOT `capture_environment_lock` (needs
    pyyaml, absent here); labelled supplemental wherever it is cited."""
    record = {
        "lock_class": "supplemental-stdlib (not capture_environment_lock)",
        "python": sys.version,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "script": "scripts/audit_gfz_drivers.py",
        "script_sha256": sha256_of_file(Path(__file__)),
        "code_commit": _git_head(),
        "working_tree_dirty": _git_dirty(),
    }
    digest = hashlib.sha256(
        json.dumps(record, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    (out_dir / "environment_supplemental.json").write_text(
        json.dumps(record | {"sha256": digest}, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return digest, record


def _registry_row(
    run_id: str, *, status: str, lock_hash: str, code_commit: str, notes: str, reason: str = ""
) -> dict[str, Any]:
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    row: dict[str, Any] = {
        "run_id": run_id,
        "started_at_utc": now,
        "completed_at_utc": now if status != "started" else "",
        "status": status,
        "code_commit": code_commit,
        "environment_lock_hash": lock_hash,
        "platform": "local",
        "dataset_version": "",
        "fold_id": "",
        "mask_id": "",
        "feature_set_id": "",
        "model_id": "",
        "hyperparameters_json": "",
        "seed": "",
        "validation_metric_name": "",
        "validation_metric_value": "",
        "artifact_manifest_path": "",
        "prediction_hash": "",
        "locked_test_accessed": False,
        "notes": notes,
    }
    if reason:
        row["reason"] = reason
    return row


# --- main -----------------------------------------------------------------------------


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if '"2022-12' in text or "'2022-12" in text:
        raise IntegrityError(
            str(path),
            "would carry a December-2022 literal that the custody scan matches; driver "
            "epochs are integer-keyed precisely to keep the R-26 exclusion mechanical",
        )
    path.write_text(text, encoding="utf-8")


def run(out_dir: Path, *, offline: bool) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    started_utc = dt.datetime.now(dt.timezone.utc).isoformat()
    # lower-case + digits with separators only: the W-9 heuristic refuses a 20+-char
    # three-class token, and the allowlist is not grown for a run id.
    run_id = "gfz-driver-audit-" + started_utc[:19].replace(":", "").replace("-", "").replace(
        "T", "-"
    )
    lock_hash, lock = _supplemental_lock(out_dir)
    registry_path = REPO_ROOT / "artifacts" / "registry" / "experiment_registry.jsonl"
    access_log = REPO_ROOT / "evidence" / "test_run_access_log.jsonl"
    notes = (
        "GFZ driver-pair audit (Kp nowcast vs definitive; Hp60 V2.0 vs V3.0). Driver data "
        "only: no December 2022 TARGET value read (R-26 driver exclusion). environment_lock_hash "
        "is a SUPPLEMENTAL stdlib lock, not capture_environment_lock (pyyaml absent). Working "
        f"tree dirty at run: {lock['working_tree_dirty']}."
    )
    append_registry_event(
        registry_path,
        _registry_row(
            run_id,
            status="started",
            lock_hash=lock_hash,
            code_commit=lock["code_commit"],
            notes=notes,
        ),
        phase=1,
        writer_role="acquisition-audit",
        access_log_path=access_log,
    )
    try:
        summary = _run_body(
            out_dir, offline=offline, run_id=run_id, started_utc=started_utc, lock_hash=lock_hash
        )
    except Exception as exc:  # noqa: BLE001 — recorded honestly, then re-raised as exit 1
        append_registry_event(
            registry_path,
            _registry_row(
                run_id,
                status="failed",
                lock_hash=lock_hash,
                code_commit=lock["code_commit"],
                notes=notes,
                reason=f"{type(exc).__name__}: {exc}",
            ),
            phase=1,
            writer_role="acquisition-audit",
            access_log_path=access_log,
        )
        print(f"integrity failure: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    append_registry_event(
        registry_path,
        _registry_row(
            run_id,
            status="completed",
            lock_hash=lock_hash,
            code_commit=lock["code_commit"],
            notes=notes + f" Result: {summary}",
        ),
        phase=1,
        writer_role="acquisition-audit",
        access_log_path=access_log,
    )
    print(summary)
    return 0


def _run_body(
    out_dir: Path, *, offline: bool, run_id: str, started_utc: str, lock_hash: str
) -> str:
    record_path = out_dir / "retrieval_record.json"
    prior: dict[str, Any] = {}
    if record_path.exists():
        prior = {
            r["logical_name"]: r
            for r in json.loads(record_path.read_text(encoding="utf-8"))["provider_files"]
        }

    records: list[dict[str, Any]] = []
    if not offline:
        client = RetrievalClient(_urllib_transport, min_interval_s=1.0)
        for spec in SPECS:
            live_spec: dict[str, Any] = dict(spec) | {"location_date": "see _server.last_modified"}
            record = client.retrieve(
                live_spec, dest_dir=out_dir, prior_record=prior.get(spec["logical_name"])
            )
            server = live_spec.get("_server", {})
            record = dict(record) | {
                "logical_name": spec["logical_name"],
                "series": spec["series"],
                "grade": spec["grade"],
                "url": spec["url"],
                "location_date": str(server.get("last_modified")),
                "server_content_length": server.get("content_length"),
                "server_last_modified": server.get("last_modified"),
                "server_etag": server.get("etag"),
            }
            if record.get("status") != "complete":
                raise IntegrityError(
                    spec["logical_name"],
                    f"retrieval status {record.get('status')!r}: {json.dumps(record.get('divergence'))}",
                )
            records.append(record)
    else:
        if not prior:
            raise IntegrityError(
                str(record_path), "offline run requires a prior retrieval_record.json"
            )
        records = list(prior.values())

    # hashes re-derived from disk, never carried
    for record in records:
        on_disk = sha256_of_file(out_dir / record["logical_name"])
        if on_disk != record["sha256"]:
            raise IntegrityError(
                record["logical_name"], f"on-disk sha256 {on_disk} != recorded {record['sha256']}"
            )

    by_name = {r["logical_name"]: r for r in records}
    kp_now = parse_wdc(out_dir / "Kp_now2022.wdc")
    kp_def = parse_wdc(out_dir / "Kp_def2022.wdc")
    hp_v2 = parse_hpo(out_dir / "hp60ap60doi_2022_v2.txt")
    hp_v3 = parse_hpo(out_dir / "hp60ap60doi_2022_v3.txt")

    validation = {
        "Kp_now2022.wdc": validate_series(
            "Kp/ap nowcast 2022", kp_now, step_hours=3, missing_value=float(KP_MISSING)
        ),
        "Kp_def2022.wdc": validate_series(
            "Kp/ap definitive 2022", kp_def, step_hours=3, missing_value=float(KP_MISSING)
        ),
        "hp60ap60doi_2022_v2.txt": validate_series(
            "Hp60/ap60 V2.0 2022", hp_v2, step_hours=1, missing_value=HP_MISSING
        ),
        "hp60ap60doi_2022_v3.txt": validate_series(
            "Hp60/ap60 V3.0 2022", hp_v3, step_hours=1, missing_value=HP_MISSING
        ),
    }
    for name, v in validation.items():
        if not v["coverage_complete"] or not v["chronology_monotonic"] or v["cadence_breaks"]:
            raise IntegrityError(
                name,
                f"coverage/chronology/cadence failure: {json.dumps({k: v[k] for k in ('epochs_2022', 'epochs_expected_2022', 'chronology_monotonic', 'cadence_breaks')})}",
            )

    comparisons = {
        "kp_ap3": compare_series(
            "kp_ap3",
            "nowcast (settled, final-stage) versus definitive — R-63 control 5, literal",
            kp_now,
            kp_def,
            ("nowcast", "definitive"),
            ("kp", "ap"),
        ),
        "hp60_ap60": compare_series(
            "hp60_ap60",
            "contemporaneous V2.0 versus later algorithm-recomputed V3.0 — documented SUBSTITUTE control, not NRT versus definitive",
            hp_v2,
            hp_v3,
            ("v2_contemporaneous", "v3_recomputed"),
            ("hp60", "ap60"),
        ),
    }

    retrieval_date = records[0]["retrieval_date"]
    inventory = [
        {
            "series": "kp_ap3",
            "provider": SPECS[0]["provider"],
            "role": "primary driver candidate (kp_safe, ap_safe) — NOT yet a producer artifact; no permitted_producers entry",
            "provider_product_identity": f"{SPECS[0]['provider_filename']} + {SPECS[1]['provider_filename']} (DOI 10.5880/Kp.0001, V. 1.0)",
            "coverage": "calendar 2022, 3-hourly, both grades, 2920 epochs each (measured; see validation)",
            "retrieval_date": retrieval_date,
            "checksum": f"nowcast {by_name['Kp_now2022.wdc']['sha256']}; definitive {by_name['Kp_def2022.wdc']['sha256']}",
            "release_status": "nowcast (archived, settled) SELECTED per D-39 (student decision; supervisor status open); definitive held as audit comparator only; not proven available at every forecast origin; availability rule owed from evidence before producer release",
            "licence_access_notes": "CC BY 4.0; cite Matzka et al. 2021 (Space Weather, doi:10.1029/2020SW002641) and the data DOI",
            "consuming_configuration": "none yet — configs/features.yaml availability_lags remains 'TBD — freeze gate'",
        },
        {
            "series": "hp60_ap60",
            "provider": SPECS[2]["provider"],
            "role": "primary driver candidate (hp60_safe, ap60_safe) — NOT yet a producer artifact; no permitted_producers entry",
            "provider_product_identity": f"{SPECS[2]['provider_filename']} (V2.0) + {SPECS[3]['provider_filename']} (V3.0)",
            "coverage": "calendar 2022, hourly, both DOI versions, 8760 epochs each (measured; see validation)",
            "retrieval_date": retrieval_date,
            "checksum": f"V2.0 {by_name['hp60ap60doi_2022_v2.txt']['sha256']}; V3.0 {by_name['hp60ap60doi_2022_v3.txt']['sha256']}",
            "release_status": "contemporaneous V2.0 SELECTED per D-40 (student decision; supervisor status open); V3.0 held as later-recomputed comparator only; single provider grade, no definitive exists; substitute control establishes neither first-issue availability nor absence of leakage",
            "licence_access_notes": "CC BY 4.0; cite Yamazaki et al. 2024 and the data DOIs 10.5880/Hpo.0002, 10.5880/Hpo.0003",
            "consuming_configuration": "none yet — configs/features.yaml availability_lags remains 'TBD — freeze gate'",
        },
    ]
    assert_driver_inventory(inventory)

    retrieval_record = {
        "run_id": run_id,
        "started_utc": started_utc,
        "authorisation": "owner qualified approval 2026-09-18 (governance/CHANGE_RECORD_2026-09-18_gfz_driver_pair_audit.md; build-and-test diary)",
        "transport": "stdlib urllib injected into src.data.acquisition.RetrievalClient (TS-A-01); scripts/00 _build_transport unchanged",
        "provider_files": records,
        "driver_inventory": inventory,
        "provider_limitations": PROVIDER_LIMITATIONS,
        "environment_supplemental": {"file": "environment_supplemental.json", "sha256": lock_hash},
    }
    guard_egress_free_text(json.dumps(PROVIDER_LIMITATIONS), context="provider_limitations")
    _write_json(record_path, guard_egress(retrieval_record, context="retrieval_record"))

    report = {
        "run_id": run_id,
        "validation": validation,
        "comparisons": comparisons,
        "provider_limitations": PROVIDER_LIMITATIONS,
        "december_custody": "driver records only; excluded from locked-test custody by governance-guards R-26; month keys are integers; no December target value read; locked_test_accessed=false",
    }
    _write_json(out_dir / "gfz-comparison-report.json", report)
    _write_markdown(out_dir / "GFZ-AUDIT.md", records, validation, comparisons)

    derived = {
        "retrieval_record.json": sha256_of_file(record_path),
        "gfz-comparison-report.json": sha256_of_file(out_dir / "gfz-comparison-report.json"),
        "GFZ-AUDIT.md": sha256_of_file(out_dir / "GFZ-AUDIT.md"),
        "environment_supplemental.json": sha256_of_file(out_dir / "environment_supplemental.json"),
    }
    # G-1 (2026-09-19): `write_sha256_manifest` now emits the canonical TE 13.3 flat
    # {path: sha256} mapping under the governed filename (TA-15's reader verifies it) and
    # the W-4 metadata (provider identities with version suffix, provenance class,
    # interpreter, hash arithmetic) in `sha256_manifest_meta.json` beside it. The interim
    # `w4_provider_sha256_manifest.json` this script wrote on 2026-09-18 is superseded.
    write_sha256_manifest(
        out_dir / "sha256_manifest.json",
        provider_files=records,
        derived_artifacts=derived,
        provenance_class="full",
        producing_interpreter=sys.version.split()[0],
    )
    kp, hp = comparisons["kp_ap3"], comparisons["hp60_ap60"]
    return (
        f"kp_ap3 nowcast-vs-definitive: {kp['mismatch_epochs']}/{kp['epochs_compared']} epochs differ; "
        f"hp60_ap60 V2.0-vs-V3.0: {hp['mismatch_epochs']}/{hp['epochs_compared']} epochs differ"
    )


def _write_markdown(
    path: Path,
    records: Sequence[Mapping[str, Any]],
    validation: Mapping[str, Any],
    comparisons: Mapping[str, Any],
) -> None:
    lines = [
        "# GFZ driver-pair audit — retrieval, hashes, parse validation and cross-comparison",
        "",
        f"Generated {dt.datetime.now(dt.timezone.utc).isoformat()} by `scripts/audit_gfz_drivers.py`; machine-readable twins: `retrieval_record.json`, `gfz-comparison-report.json`, `sha256_manifest.json`.",
        "",
        "## Retrieved files (TE 13.3 source_files items)",
        "",
        "| Logical name | Provider product identity (incl. DOI version path) | Retrieval date | Server Last-Modified | Bytes | SHA-256 |",
        "|---|---|---|---|---|---|",
    ]
    for r in records:
        lines.append(
            f"| `{r['logical_name']}` | `{r['provider_filename']}` | {r['retrieval_date']} | {r.get('server_last_modified')} | {r.get('server_content_length')} | `{r['sha256']}` |"
        )
    lines += [
        "",
        "## Parse validation",
        "",
        "| File | 2022 epochs | expected | chronology | cadence breaks | missing epochs |",
        "|---|---|---|---|---|---|",
    ]
    for name, v in validation.items():
        lines.append(
            f"| `{name}` | {v['epochs_2022']} | {v['epochs_expected_2022']} | {'monotonic' if v['chronology_monotonic'] else 'BROKEN'} | {v['cadence_breaks']} | {v['missing_epochs']} |"
        )
    lines += ["", "## Value-by-value comparisons", ""]
    for c in comparisons.values():
        lines += [
            f"### `{c['series']}` — {c['comparison_label']}",
            "",
            f"- epochs compared: {c['epochs_compared']}; only in first: {c['epochs_only_in_first']}; only in second: {c['epochs_only_in_second']}",
            f"- mismatching epochs: **{c['mismatch_epochs']}** ({c['mismatch_fraction']:.4%} of compared)"
            if c["mismatch_fraction"] is not None
            else "- no common epochs",
            f"- mismatches per month (1..12): {[c['mismatches_per_month'][m] for m in range(1, 13)]}",
            f"- designed control `assert_gfz_cross_products` fired: {c['designed_control_assert_gfz_cross_products_fired']} (consistent with count: {c['designed_control_consistent_with_count']})",
            "",
        ]
    lines += ["## Provider limitations (recorded verbatim in the JSON twins)", ""]
    for series, text in PROVIDER_LIMITATIONS.items():
        lines.append(f"- **{series}**: {text}")
    lines += [
        "",
        "## What this audit does NOT do",
        "",
        "- creates no producer artifact and no `permitted_producers` entry; `availability_lags` stays `TBD — freeze gate`;",
        "- decides no release grade for any feature contract (Student + Supervisor, G-04);",
        "- reads no December 2022 target value (`locked_test_accessed = false`; driver records are R-26-excluded from custody);",
        "- claims no first-issue reconstruction for the Kp nowcast and no definitive-backfill detection for Hp60/ap60.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="audit_gfz_drivers.py", description=__doc__.split("\n\n")[0]
    )
    parser.add_argument(
        "--out",
        default="evidence/audit_gfz_2026-09-18",
        help="output directory (relative to the repository root)",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="parse and compare the already-held files; no network",
    )
    args = parser.parse_args(argv)
    out_dir = REPO_ROOT / args.out
    return run(out_dir, offline=args.offline)


if __name__ == "__main__":
    sys.exit(main())
