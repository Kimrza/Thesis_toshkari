"""Stage script 03: verify Phase 1 target processing — value-level, tolerance declared.

Purpose
-------
The fourth of the nine phase-aware stage scripts (TE 12/13.2; P1-03's verification half,
Phase 1 scope). It ORCHESTRATES `src/data/prepared.py`'s `verify_value_level`: a
VALUE-LEVEL closed-set diff of the standardized target against the released provider
bytes, showing only the four documented transformations (documented QC, UTC
normalization, D-1 cell selection, D-16 median aggregation) — a fifth transformation is
a FAILURE, not something a reviewer must notice. Schema-level comparison (column names
and dtypes) is explicitly insufficient (FR-P1-03-1; SD-T-03; W-2).

Phase 1 scope, thinner than TE 12's prose implies
-------------------------------------------------
Per `functional-design`'s settlement (W-4, § Known defects row 11), the four Phase 2
uncertainty contents of Vision 6.9 — per-satellite, per-IPP, and geometry quantities —
are BARRED from this Phase 1 verification: the evidence records them not-applicable with
their reason, never emitted empty. Vision 6.9 states its list without a phase qualifier;
the qualifier runs through Vision 15.2.

The tolerance is a declared value, and it is NOT set here
---------------------------------------------------------
The float diff tolerance is read from the fixture manifest's permitted floating-point
tolerances (TE 15.2), supplied via `--fixture-manifest`. Unset — flag omitted, file
absent, or field missing — the run STOPS naming that field: a tolerance taken from a
library default such as `numpy.isclose`'s is a scientific value filled by convenience.

What this script can and cannot run today
-----------------------------------------
Under Q2 = A no standardized target artifact exists (script 02 refuses while
`configs/data.yaml`'s `qc_operations` is `TBD — freeze gate`), so this run REFUSES at
the missing-artifact check and its `aborted` registry row is honest. The recomputation
inside `verify_value_level` re-runs the same Q2 = A gate: a verification of a target
that must not exist refuses identically.

Inputs
------
`--config configs/` (the four governed configs, read only through `load_configs`);
`--phase 1` (Phase 1 only); `--fixture-manifest <path>` (the fixture manifest carrying
the declared tolerance, TE 15.2). Provider input is consumed from RELEASED artifacts by
manifest and hash (R-44); the target artifact is script 02's output.

Re-run behaviour
----------------
Each run appends its own `started` and terminal rows to the experiment registry
(append-only, NFR-AUD-01; failed and aborted runs stay visible with status and reason).
The verification is a pure function of its inputs; the evidence artifact is rewritten
identically for identical inputs. Nothing here mutates the target, the releases, or any
config.

Boundaries this script holds
----------------------------
* `ensure_process_determinism` is the FIRST statement of `main()`; step 4 of the stage
  entry contract is `assert_phase_boundary`; `assert_no_raw_fields` runs BEFORE the
  first write (R-23/R-24).
* No restricted-root literal appears here and no path into the December evidence root is
  constructed (R-28; SD-05).
* The verification evidence is written through `prepared.write_json_artifact`, so it
  carries the three definition IDs, the `location-sampled gridded VTEC` label and the
  lineage caveat (R-69, R-70), and routes through `guard_egress` (NFR-SEC-01).
* No scientific value is decided here: the tolerance is the fixture manifest's; the QC
  list stays unset by this unit.
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
from src.data.phase_contract import assert_no_raw_fields, assert_phase_boundary  # noqa: E402
from src.data.prepared import (  # noqa: E402
    LINEAGE_CAVEAT_FIELD,
    TOLERANCE_MANIFEST_KEY,
    TOLERANCE_MANIFEST_SUBKEY,
    StandardizationError,
    load_released_provider_rows,
    read_target_rows_csv,
    resolve_float_tolerance,
    resolve_target_identity,
    verify_value_level,
    write_json_artifact,
)

STAGE = "target-standardization"
PHASE = 1

#: The field names this run can produce, screened through R-23's produced-field limb
#: BEFORE the first write (R-24). Verification-evidence keys only; no excluded-class
#: token appears in any field name.
PRODUCED_FIELDS: tuple[str, ...] = (
    "artifact_class",
    "phase_id",
    "source_id",
    "target_definition_id",
    "target_label",
    LINEAGE_CAVEAT_FIELD,
    "transformations_enumerated",
    "comparison_level",
    "tolerance_tecu",
    "tolerance_source",
    "rows_compared",
    "differences",
    "uncertainty_contents_not_applicable",
    "content",
    "reason",
)


def _assert_phase1_field_contract() -> None:
    """R-24: the produced-field guard, called before this run's first write."""
    assert_no_raw_fields(PRODUCED_FIELDS, phase=PHASE)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="03_verify_processing.py",
        description=(
            "Value-level closed-set verification of the Phase 1 standardized target "
            "against the released provider bytes (P1-03; FR-P1-03-1). The float "
            "tolerance is the fixture manifest's declared value (TE 15.2), never a "
            "library default."
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
        help="Phase 1 only: the Phase 2 verification chain is a Phase 2 stage's",
    )
    parser.add_argument(
        "--fixture-manifest",
        type=Path,
        default=None,
        help=(
            "path to the fixture manifest carrying permitted_floating_point_tolerances "
            "(TE 15.2); omitted or unset, the run STOPS rather than choosing a default"
        ),
    )
    return parser.parse_args(argv)


def _stage_entry(config_dir: Path) -> dict[str, Any]:
    """Steps 2-6 of the stage entry contract (step 1, determinism, ran in main()).

    2. `load_configs` — snapshot, hash, resolve roots (the only read of configs/).
    3. Preflight: `assert_no_tbd` over this stage's required fields and
       `assert_declared_sources_exist`.
    4. `assert_phase_boundary` — no raw-processing module loaded (never skipped).
    5. No authenticated provider access is declared for this stage; the
       credential-NAME presence check has nothing to check and nothing is silently
       skipped — this line records the fact.
    6. Seed, capture the eight-item environment lock, and open the run record.
    """
    snapshot = load_configs(config_dir, phase=PHASE)
    assert_no_tbd(snapshot, required=required_fields_for(STAGE, PHASE))
    assert_declared_sources_exist(snapshot)
    assert_phase_boundary(PHASE, loaded_modules=sys.modules)
    determinism = seed_everything(snapshot, stage=STAGE)
    lock = capture_environment_lock(snapshot, determinism)
    assert_lock_complete(lock)
    return {"snapshot": snapshot, "determinism": determinism, "lock": lock}


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
        "notes": "target verification run (P1-03, Phase 1 scope)",
    }
    if reason:
        row["reason"] = reason
    return row


def _load_tolerance(fixture_manifest_path: Path | None) -> float:
    """The declared tolerance from the fixture manifest — or STOP naming TE 15.2's field.

    The manifest is read ONLY through the one validating loader
    (`src.data.fixture_manifest.load_fixture_scope`, R-133): a second `yaml.safe_load`
    of a fixture manifest here would be a second parser of one contract and fails
    `tests/test_clean_run.py`'s only-copy scan (R-133 control 4). Rerouted 2026-09-09 by
    `fixtures-and-reproducibility` code-generation (CR-2026-09-07); flagged for
    `target-standardization`'s record — behaviour is strictly narrower: a file that is
    not a valid fixture manifest or identity declaration now refuses at the loader
    naming the violated expectation, instead of being parsed loosely for one field.

    Raises
    ------
    StandardizationError
        when the flag is omitted or the file is absent (the tolerance is then unset in
        every sense), and through `resolve_float_tolerance` when the manifest exists
        but the permitted-floating-point-tolerances field does not resolve.
    IntegrityError
        from the loader, when the named file is not a valid fixture manifest or
        identity declaration (R-133).
    """
    field = f"{TOLERANCE_MANIFEST_KEY}.{TOLERANCE_MANIFEST_SUBKEY}"
    if fixture_manifest_path is None or not Path(fixture_manifest_path).is_file():
        raise StandardizationError(
            f"fixture_manifest.yaml {field}",
            "the permitted floating-point tolerance (TE 15.2) is unset — no fixture "
            "manifest was supplied or the named file does not exist; the tolerance "
            "is a DECLARED value belonging with the fixture manifest, never a "
            "library default such as numpy.isclose's, and the run stops rather than "
            "choosing one (SD-T-03)",
        )
    from src.data.fixture_manifest import load_fixture_scope  # deferred (R-05, transitive)

    scope = load_fixture_scope(Path(fixture_manifest_path))
    return resolve_float_tolerance(scope.data)


def _run_verification(entry: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    """W-2: the value-level verification — refuses honestly while no target exists.

    Order: produced-field guard; the target artifact must exist (under Q2 = A it does
    not, and the refusal names that); the tolerance must be declared (TE 15.2);
    provider input is consumed by manifest and hash; the value-level diff recomputes
    the target through the same closed four-transformation engine (re-running the
    Q2 = A gate) and fails on any change the four documented transformations do not
    explain; the evidence is written with the three IDs, the label and the caveat.
    """
    _assert_phase1_field_contract()  # R-24: before the first write, always

    snapshot = entry["snapshot"]
    target_path = (
        Path(snapshot.resolved_roots["artifacts"]) / "prepared_target" / "hourly_target_phase1.csv"
    )
    if not target_path.is_file():
        raise IntegrityError(
            target_path,
            "no standardized target artifact exists to verify; under Q2 = A script 02 "
            "refuses while configs/data.yaml qc_operations is TBD — freeze gate, and "
            "no standardized target is produced by any path — this verification "
            "refuses honestly rather than passing vacuously",
        )

    tolerance = _load_tolerance(args.fixture_manifest)

    release_root = Path(
        snapshot.resolved_roots.get(
            "release_root", snapshot.resolved_roots["artifacts"] / "releases"
        )
    )
    provider_rows = load_released_provider_rows(release_root)
    target_rows = read_target_rows_csv(target_path)

    evidence = verify_value_level(
        provider_rows,
        target_rows,
        data_config=snapshot.data,
        aggregation_config_id=snapshot.hashes["data.yaml"][:12],
        tolerance=tolerance,
    )
    identity = resolve_target_identity(snapshot.data)
    out_path = write_json_artifact(
        Path(snapshot.resolved_roots["artifacts"])
        / "prepared_target"
        / "verification_evidence.json",
        evidence,
        identity=identity,
        artifact_class="verification_evidence",
    )
    return {"verification_evidence": str(out_path), "rows_compared": evidence["rows_compared"]}


def main() -> int:
    ensure_process_determinism(sys.argv)  # FIRST statement, before any framework import
    args = _parse_args(sys.argv[1:])

    try:
        entry = _stage_entry(args.config)
    except IntegrityError as exc:
        print(f"03_verify_processing: preflight refusal: {exc}", file=sys.stderr)
        return 1

    snapshot = entry["snapshot"]
    lock = entry["lock"]
    lock_hash = environment_lock_hash(lock)
    registry_path, access_log = _registry_paths(snapshot)
    run_id = (
        f"target-verification-{dt.datetime.now(dt.UTC).strftime('%Y%m%dT%H%M%SZ')}"
        f"-{uuid.uuid4().hex[:8]}"
    )

    started = _registry_row(run_id, status="started", lock_hash=lock_hash, snapshot=snapshot)
    started["code_commit"] = lock.code_commit
    append_registry_event(
        registry_path, started, phase=PHASE, writer_role="stage", access_log_path=access_log
    )

    try:
        summary = _run_verification(entry, args)
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
        print(f"03_verify_processing: aborted: {exc}", file=sys.stderr)
        return 1

    completed = _registry_row(run_id, status="completed", lock_hash=lock_hash, snapshot=snapshot)
    completed["code_commit"] = lock.code_commit
    completed["artifact_manifest_path"] = summary["verification_evidence"]
    append_registry_event(
        registry_path, completed, phase=PHASE, writer_role="stage", access_log_path=access_log
    )
    print(f"03_verify_processing: completed: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
