"""Stage script 02: standardize the Phase 1 hourly target under D-17 — or REFUSE.

Purpose
-------
The third of the nine phase-aware stage scripts (TE 12/13.2; P1-03, Phase 1). It
ORCHESTRATES `src/data/prepared.py`: exactly the closed four-transformation set
(documented QC; UTC normalization; D-1's half-open floor cell selection; D-16's median
hourly aggregation), D-17's sixteen-field row contract with the lineage-caveat column,
the three definition IDs on every artifact, D-19's support thresholds read from config
with their January-November basis, the cell-and-month coverage report, the data-quality
block and the Phase 1 uncertainty budget.

What this script can and cannot run today
-----------------------------------------
**The target-producing path REFUSES while `configs/data.yaml`'s `qc_operations` is
`TBD — freeze gate` or absent (Q2 = A).** The refusal fires BEFORE any output write, the
raise names the field and the expectation that the list be frozen under a D-number —
never mere non-emptiness — and the run's `aborted` registry row is honest. **No
standardized target artifact is produced by any path while that stands.** The refusal is
the deliverable; production waits on a supervisor freeze. The D-17 schema contract, the
caveat column, and their fixture tests are properties of the writer and run regardless
(`tests/test_prepared_target_schema.py`).

The `02` ordinal
----------------
`scripts/02_build_vtec_target.py` (Phase 2) shares this ordinal in TE 12's tree — a
RECORDED defect, not a resolved one. The ordinal denotes the pipeline position and
`--phase` selects exactly one script, so a clean run contains one `02` per phase; the
one-`02`-per-run assertion is `fixtures-and-reproducibility`'s to author in
`tests/test_clean_run.py` against `foundation`'s run-manifest record (an owed
dependency). NO `02a`/`02b` convention is invented (R-73). This script is Phase 1 only:
`--phase` accepts exactly 1, and step 4 of the entry contract
(`assert_phase_boundary`) is never skipped.

Inputs
------
`--config configs/` (the four governed configs, read only through `load_configs`).
Provider input is consumed from RELEASED acquisition artifacts under the release root,
by release manifest and hash — never by bare path (R-44): each candidate release is
verified via `release.verify_release`, and each consumed file's bytes are re-hashed
against the manifest's recorded digest before a row is read.

Re-run behaviour
----------------
Each run appends its own `started` and terminal rows to the experiment registry
(append-only, NFR-AUD-01; failed and aborted runs stay visible with status and reason).
Re-running while the QC list is unfrozen produces another honest `aborted` row, never a
target. No value is interpolated, smoothed or filled; provider values are preserved.

Boundaries this script holds
----------------------------
* `ensure_process_determinism` is the FIRST statement of `main()`; step 4 of the stage
  entry contract is `assert_phase_boundary`; `assert_no_raw_fields` runs BEFORE the
  first write (R-23/R-24).
* No restricted-root literal appears here and no path into the December evidence root is
  constructed (R-28; SD-05).
* Every written payload routes through `acquisition.guard_egress` inside the library
  writers; no credential, token or signed URL enters any output (NFR-SEC-01).
* No scientific value is decided here: D-16, D-17, D-19 and D-1 are applied from config
  and decision records; `qc_operations` and the diff tolerance stay unset by this unit.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
import uuid
from collections.abc import Mapping
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import (  # noqa: E402
    IntegrityError,
    assert_declared_sources_exist,
    assert_lock_complete,
    assert_no_tbd,
    capture_environment_lock,
    ensure_process_determinism,
    environment_lock_hash,
    load_configs,
    required_fields_for,
    seed_everything,
)
from src.data.experiment_registry import (  # noqa: E402
    append_registry_event,
    record_abort_honestly,
)
from src.data.fixture_gate import require_receipts_for_snapshot  # noqa: E402
from src.data.phase_contract import assert_no_raw_fields, assert_phase_boundary  # noqa: E402
from src.data.prepared import (  # noqa: E402
    LINEAGE_CAVEAT_FIELD,
    assert_qc_operations_frozen,
    load_released_provider_rows,
    standardize_hourly_target,
    write_json_artifact,
    write_target_rows_csv,
)

STAGE = "target-standardization"
PHASE = 1

#: The field names this run can produce, screened through R-23's produced-field limb
#: BEFORE the first write (R-24). D-17's sixteen fields, the lineage-caveat column, and
#: the coverage/quality/budget artifact keys. No excluded-class token appears here.
PRODUCED_FIELDS: tuple[str, ...] = (
    "interval_start_utc",
    "station_id",
    "cell_gdlat",
    "cell_glon",
    "cell_lat_bounds",
    "cell_lon_bounds",
    "vtec_tecu",
    "valid_observation_count",
    "within_hour_spread_tecu",
    "largest_internal_gap_s",
    "provider_dtec_summary",
    "aggregation_config_id",
    "target_valid",
    "phase_id",
    "source_id",
    "target_definition_id",
    LINEAGE_CAVEAT_FIELD,
    "target_label",
    "artifact_class",
    "station",
    "month",
    "rows",
    "valid_rows",
    "invalid_rows",
    "invalid_reasons",
    "keys",
    "keying_note",
    "per_cell_month",
    "documentation",
    "negative_vtec",
    "missingness_and_support",
    "uncertainty_budget",
    "processor_qc_flags",
    "unexplained_discrepancies",
    "applicable",
    "asymmetry_statement",
    "not_applicable",
    "bounds_statement",
    "completeness",
)


def _assert_phase1_field_contract() -> None:
    """R-24: the produced-field guard, called before this run's first write."""
    assert_no_raw_fields(PRODUCED_FIELDS, phase=PHASE)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="02_standardize_prepared_target.py",
        description=(
            "Standardize the Phase 1 hourly target under D-17's sixteen-field "
            "contract (P1-03). REFUSES while configs/data.yaml qc_operations is "
            "TBD — freeze gate (Q2 = A): no standardized target is produced."
        ),
    )
    parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="the governed configs directory (always configs/; TE 13.2)",
    )
    parser.add_argument(
        "--phase",
        type=int,
        choices=(1,),
        default=1,
        help=(
            "Phase 1 only: the Phase 2 target build is scripts/02_build_vtec_target.py, "
            "selected by --phase 2 there; one 02 per run, no 02a/02b (R-73)"
        ),
    )
    parser.add_argument(
        "--fixture-manifest",
        type=Path,
        default=None,
        help=(
            "the walking-skeleton fixture scope (a fixture manifest or identity declaration, "
            "validated through the one loader). When given, this run is a FIXTURE run: the "
            "TE 9.2 two-receipt gate is exempt (a fixture run is not a full-year job, Q5 = A) "
            "and the exemption is recorded, never silent. Additive edit flagged for "
            "`target-standardization`'s record (fixtures-and-reproducibility CR-2026-09-07)"
        ),
    )
    return parser.parse_args(argv)


def _stage_entry(config_dir: Path, *, fixture_manifest: Path | None = None) -> dict[str, Any]:
    """Steps 2-6 of the stage entry contract (step 1, determinism, ran in main()).

    2. `load_configs` — snapshot, hash, resolve roots (the only read of configs/).
    3. Preflight: `assert_no_tbd` over this stage's required fields (deliberately
       minimal — `qc_operations`' enforcement point is the target-producing run, per
       Q2 = A) and `assert_declared_sources_exist`.
    4. `assert_phase_boundary` — no raw-processing module loaded (never skipped).
    5. No authenticated provider access is declared for this stage (input is released
       local artifacts); the credential-NAME presence check has nothing to check and
       nothing is silently skipped — this line records the fact.
    6. Seed, capture the eight-item environment lock, open the run record, then
       `require_receipts_for_snapshot` (TE 9.2: both fixtures pass before any full-year
       job; exempt on a fixture run carrying `--fixture-manifest`, Q5 = A).
    """
    snapshot = load_configs(config_dir, phase=PHASE)
    assert_no_tbd(snapshot, required=required_fields_for(STAGE, PHASE))
    assert_declared_sources_exist(snapshot)
    assert_phase_boundary(PHASE, loaded_modules=sys.modules)
    determinism = seed_everything(snapshot, stage=STAGE)
    lock = capture_environment_lock(snapshot, determinism)
    assert_lock_complete(lock)
    receipts_gate = require_receipts_for_snapshot(
        snapshot, lock, fixture_manifest=fixture_manifest
    )
    return {
        "snapshot": snapshot,
        "determinism": determinism,
        "lock": lock,
        "receipts_gate": receipts_gate,
    }


def _registry_paths(snapshot: Any) -> tuple[Path, Path]:
    registry_root = Path(
        snapshot.resolved_roots.get(
            "registry_root", snapshot.resolved_roots["artifacts"] / "registry"
        )
    )
    registry_path = registry_root / "experiment_registry.jsonl"
    access_log = (
        Path(snapshot.resolved_roots["workspace"]) / "evidence" / "merge_run_access_log.jsonl"
    )
    return registry_path, access_log


def _registry_row(
    run_id: str, *, status: str, lock_hash: str, snapshot: Any, reason: str = ""
) -> dict[str, Any]:
    now = dt.datetime.now(dt.UTC).isoformat()
    row: dict[str, Any] = {
        "run_id": run_id,
        "started_at_utc": now,
        "completed_at_utc": now if status in ("completed", "aborted", "failed") else "",
        "status": status,
        "code_commit": "",  # populated from the lock by the caller
        "environment_lock_hash": lock_hash,
        "platform": snapshot.platform,
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
        "notes": "target-standardization run (P1-03)",
    }
    if reason:
        row["reason"] = reason
    return row


def _run_standardize(entry: Mapping[str, Any]) -> dict[str, Any]:
    """W-1: the target-producing run — REFUSED while the QC list is unfrozen (Q2 = A).

    The refusal is the FIRST statement after the produced-field guard, BEFORE input is
    even located, so no output write can precede it and the `aborted` registry row is
    honest. The pipeline below it is complete and unreachable until the supervisor
    freeze lands: consume released provider input by hash, apply exactly the four
    documented transformations, and write the target rows, coverage report,
    data-quality block and uncertainty budget — each artifact stamped with the three
    IDs, the label and the lineage caveat.
    """
    _assert_phase1_field_contract()  # R-24: before the first write, always

    snapshot = entry["snapshot"]
    # Q2 = A: refuse to RUN while qc_operations is TBD — before any output write.
    assert_qc_operations_frozen(snapshot.data)

    release_root = Path(
        snapshot.resolved_roots.get(
            "release_root", snapshot.resolved_roots["artifacts"] / "releases"
        )
    )
    provider_rows = load_released_provider_rows(release_root)
    result = standardize_hourly_target(
        provider_rows,
        data_config=snapshot.data,
        aggregation_config_id=snapshot.hashes["data.yaml"][:12],
    )

    out_dir = Path(snapshot.resolved_roots["artifacts"]) / "prepared_target"
    target_path = write_target_rows_csv(out_dir / "hourly_target_phase1.csv", result.rows)
    coverage_path = write_json_artifact(
        out_dir / "coverage_report.json",
        result.coverage_report,
        identity=result.identity,
        artifact_class="coverage_report",
    )
    quality_path = write_json_artifact(
        out_dir / "data_quality_block.json",
        result.data_quality,
        identity=result.identity,
        artifact_class="data_quality_block",
    )
    budget_path = write_json_artifact(
        out_dir / "uncertainty_budget.json",
        result.uncertainty_budget,
        identity=result.identity,
        artifact_class="uncertainty_budget",
    )
    return {
        "target": str(target_path),
        "coverage_report": str(coverage_path),
        "data_quality_block": str(quality_path),
        "uncertainty_budget": str(budget_path),
        "rows": len(result.rows),
    }


def main() -> int:
    ensure_process_determinism(sys.argv)  # FIRST statement, before any framework import
    args = _parse_args(sys.argv[1:])

    try:
        entry = _stage_entry(args.config, fixture_manifest=args.fixture_manifest)
    except IntegrityError as exc:
        print(f"02_standardize_prepared_target: preflight refusal: {exc}", file=sys.stderr)
        return 1

    snapshot = entry["snapshot"]
    lock = entry["lock"]
    lock_hash = environment_lock_hash(lock)
    registry_path, access_log = _registry_paths(snapshot)
    run_id = (
        f"target-standardization-{dt.datetime.now(dt.UTC).strftime('%Y%m%dT%H%M%SZ')}"
        f"-{uuid.uuid4().hex[:8]}"
    )

    started = _registry_row(run_id, status="started", lock_hash=lock_hash, snapshot=snapshot)
    started["code_commit"] = lock.code_commit
    append_registry_event(
        registry_path, started, phase=PHASE, writer_role="stage", access_log_path=access_log
    )

    try:
        summary = _run_standardize(entry)
    except IntegrityError as exc:
        aborted = _registry_row(
            run_id, status="aborted", lock_hash=lock_hash, snapshot=snapshot, reason=str(exc)
        )
        aborted["code_commit"] = lock.code_commit
        record_abort_honestly(
            registry_path,
            aborted,
            phase=PHASE,
            writer_role="stage",
            access_log_path=access_log,
            original_error=exc,
        )
        print(f"02_standardize_prepared_target: aborted: {exc}", file=sys.stderr)
        return 1

    completed = _registry_row(run_id, status="completed", lock_hash=lock_hash, snapshot=snapshot)
    completed["code_commit"] = lock.code_commit
    completed["artifact_manifest_path"] = summary["target"]
    append_registry_event(
        registry_path, completed, phase=PHASE, writer_role="stage", access_log_path=access_log
    )
    print(f"02_standardize_prepared_target: completed: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
