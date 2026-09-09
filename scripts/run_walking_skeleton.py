"""F3: the walking-skeleton orchestrator — plumbing then scientific, the receipts, the run log.

Purpose
-------
`fixtures-and-reproducibility` W-3, W-4, W-5, W-7 (R-135, R-136, R-137, R-140), the script
`services.md` names as the orchestrator that ENFORCES the ordering contract rather than
documenting it. `python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day`
(then `--fixture scientific_1month`) is the first pair of commands in TE 13.2's amended
clean-run fence. It implements NO domain logic: it reads the fixture's manifest through the one
loader, verifies the fixture's lineage, assembles the fixture's input on record dates, invokes
the SEVEN Phase 1 stage scripts as subprocesses in TE 13.2's order, runs the M10 contract
fixture as its own named step after the plumbing fixture, hash-lists the TE 15.4 required
outputs, compares them against the frozen expectations, and writes the fixture-pass receipt.

The six-step stage entry (services.md), exactly as the seven stage scripts do it:
1. `ensure_process_determinism` FIRST in `main()`; 2. `load_configs`; 3. `assert_no_tbd` over
this stage's `REQUIRED_FIELDS_MAP` entry (deliberately minimal, as every sibling's) and
`assert_declared_sources_exist`; 4. `assert_phase_boundary`; 5. `seed_everything`; 6. the
eight-item lock (`input_versions` carrying `fixture_manifest:<fixture_id>:<sha256>` so the
receipt's row-hashed lock binds the manifest — SD-X-02 Rec 7) and `assert_lock_complete`,
then `require_receipts_for_snapshot` — EXEMPT here by construction (a fixture run is not a
full-year job; Q5 = A), the exemption recorded in the run log.

What the fixture run does, in order (W-3/W-4/W-5/W-7):
* reads the manifest ONLY through `load_fixture_scope` — a missing manifest refuses naming the
  path (the state this pass leaves both fixture trees in, BLK-02);
* asserts the cited identity agrees with `evidence/DECISIONS.md` (R-134 control 7; R-135
  control 10) and, when frozen, that the sibling hash agrees with the freeze D-number
  (SD-X-01 step 3);
* `scientific_1month` REQUIRES a verified plumbing receipt first (R-140 control 26);
* verifies the month's four declared derived artifacts against its `sha256_manifest.json`
  BEFORE anything runs (R-135 control 12; team.md's derived-artifact eligibility criterion,
  re-verified at use);
* selects the cited station's records and asserts the assembled input: a foreign-station
  record raises (control 9), every record's OBSERVATION DATE lies in the cited window
  (`acquisition.assert_records_within_window`) and none falls in the locked month
  (`acquisition.assert_no_locked_month_records`) — R-31 consumed, never copied; the folder a
  record came from plays no role (control 14; TEC-09);
* invokes TE 13.2's seven Phase 1 invocations as subprocesses, each with `--config` and the
  fixture scope (`--fixture-manifest <path>`, Q4/Q5), with `PYTHONHASHSEED` already set (the
  parent's step 1) and `CUDA_VISIBLE_DEVICES=""` so no GPU is visible (TC-01; R-138 control
  19); a Phase-2-only script (`02_build_vtec_target.py`, `03_verify_processing.py`) raises
  `PhaseBoundaryError` before any subprocess (control 39);
* after the plumbing fixture, runs the M10 contract fixture
  (`python -m pytest tests/test_train_only_transforms.py tests/test_split_embargo.py`) as a
  named step whose result is clean-run evidence in the run log — NEVER a third receipt
  (Q12 = C; TC-03f);
* hash-lists the TE 15.4 required outputs into `artifact_manifest.json` via
  `release.sha256_of_file`, records missing outputs as a machine-readable completeness field,
  writes `clean_run_log.json` and `test_report.json`, and stamps every artifact it owns
  (`evidence_class: smoke_only` on plumbing; `data07_caveat`; `december_representativeness`);
* against a FROZEN manifest: compares every required output through the manifest's ledger
  (`exact` by equality, never updating the expectation; `toleranced` within the declared
  tolerance), asserts runtime and storage inside the MEASURED ranges, and writes the
  fixture-pass receipt as append-safe registry rows;
* with `--emit-candidate --identity <declaration>`: composes a `status: candidate` manifest
  from the owner's identity declaration and THIS run's measurements, every measured field
  carrying this run's registry id, and refuses an incomplete candidate rather than inventing
  a value. Nothing here writes `frozen`.

Inputs
------
`--config configs/` (the only read of `configs/` is `load_configs`); `--fixture`;
`--emit-candidate` with `--identity <path>`; `--code-commit` where no git tree exists (Kaggle);
`--python` (the interpreter for the subprocesses, default `sys.executable`). The month evidence
under `evidence/audit_evidence_<YYYY>-<MM>/` as the declaration/manifest cites it;
`evidence/DECISIONS.md` for the citation checks.

Re-run behaviour
----------------
Every run appends `started` then `completed|aborted` registry rows (NFR-AUD-01); artifacts are
written under `artifacts/walking_skeleton/<fixture_id>/` and the receipt payload is
write-once. A re-run against a frozen manifest compares and never updates; a candidate is
never written over an existing manifest.

What this pass cannot make run (TE 18.3)
-----------------------------------------
No manifest or declaration exists, so today `_run` refuses at the missing scope naming its
path and writes an honest `aborted` row; with a declaration, `05`'s apparatus partitions refuse
at `configs/experiment.yaml: embargo_hours` (`TBD — freeze gate`); the plumbing fixture's
minimal M-06 refuses on the unfrozen TensorFlow pin; on this clone `load_configs` refuses first
(pyyaml absent). Every refusal is a stop-and-report, never a default.

Boundaries
----------
No import of `src/external/iri.py` or `src/external/gim.py`; no hashing re-implemented; no
scientific constant in source (the TE 13.2 script enumeration, TE 15.4 output names and the
two Phase-2-only script names are identities frozen upstream and carried as such).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import subprocess
import sys
import time
import uuid
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Final

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.acquisition import (  # noqa: E402
    assert_no_locked_month_records,
    assert_records_within_window,
)
from src.data.config import (  # noqa: E402
    IntegrityError,
    PhaseBoundaryError,
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
from src.data.fixture_evidence import (  # noqa: E402
    DECISIONS_PATH,
    FREEZE_RECORD_SIDECAR_DIR,
    assert_freeze_record_agrees,
    assert_identity_agrees_with_decisions,
    stamp_fixture_artifact,
    stamp_for_manifest,
)
from src.data.fixture_gate import (  # noqa: E402
    RESULT_PASS,
    fixture_input_version_tag,
    receipt_path_for,
    require_plumbing_receipt,
    require_receipts_for_snapshot,
    write_fixture_pass_receipt,
)
from src.data.fixture_manifest import (  # noqa: E402
    ARTIFACT_MANIFEST_NAME,
    FIXTURE_IDS,
    PLUMBING_FIXTURE_ID,
    SCIENTIFIC_FIXTURE_ID,
    WALKING_SKELETON_ROOT,
    FixtureManifest,
    IdentityDeclaration,
    assert_run_level_ranges,
    collect_stage_measurements,
    compare_required_outputs,
    compose_candidate_manifest,
    compose_measurement_ranges,
    fixture_root_for,
    load_fixture_scope,
    load_measuring_results,
    manifest_path_for,
    output_matches,
    required_outputs_for,
    window_days,
    write_candidate_manifest,
    write_measuring_result,
)
from src.data.phase_contract import assert_no_raw_fields, assert_phase_boundary  # noqa: E402
from src.data.release import sha256_of_file  # noqa: E402

STAGE = "fixtures-and-reproducibility"
PHASE = 1

#: TE 13.2's Phase 1 stage-script invocations, in its order, exactly as the fence writes them:
#: (script, `--phase` value or None). Derived from the fence and compared to it by
#: `tests/test_clean_run.py` (R-138 controls 18 and 39) — an identity enumeration, not a copy
#: that may drift unchecked.
PHASE1_SEQUENCE: Final[tuple[tuple[str, int | None], ...]] = (
    ("00_acquire_prepared_vtec.py", None),
    ("01_inventory_and_registry.py", 1),
    ("02_standardize_prepared_target.py", None),
    ("04_build_external_products.py", 1),
    ("05_build_features_and_splits.py", 1),
    ("06_train_and_predict.py", 1),
    ("07_evaluate_and_report.py", 1),
)
#: The two TE 13.2 scripts that appear ONLY below `# Phase 2, only after G-P2` (TE:795).
PHASE2_ONLY_SCRIPTS: Final[tuple[str, ...]] = (
    "02_build_vtec_target.py",
    "03_verify_processing.py",
)
#: Q4 = A / Q5 = A: the one option that carries the fixture scope into every stage script.
FIXTURE_SCOPE_OPTION: Final[str] = "--fixture-manifest"
#: The M10 contract fixture's two modules (authored by features-and-splits; run here, Q12 = C).
M10_MODULES: Final[tuple[str, ...]] = (
    "tests/test_train_only_transforms.py",
    "tests/test_split_embargo.py",
)
RUN_LOG_NAME: Final[str] = "clean_run_log.json"
TEST_REPORT_NAME: Final[str] = "test_report.json"
INPUT_MANIFEST_NAME: Final[str] = "input_manifest.yaml"
CONFIG_SNAPSHOT_NAME: Final[str] = "processing_config_snapshot.yaml"
REGISTRY_ENTRY_NAME: Final[str] = "registry_entry.json"
#: The default subprocess timeout (seconds) — operational, not scientific.
SUBPROCESS_TIMEOUT_S: Final[int] = 3600
_TAIL_CHARS: Final[int] = 4000

#: The field names this script writes, screened by R-23's produced-field limb before the first
#: write (R-24). Identities, never values.
PRODUCED_FIELDS: tuple[str, ...] = (
    "kind",
    "fixture_id",
    "status",
    "run_id",
    "platform",
    "outputs",
    "missing_required_outputs",
    "commands",
    "argv",
    "returncode",
    "stdout_tail",
    "stderr_tail",
    "started_at_utc",
    "ended_at_utc",
    "duration_seconds",
    "pythonhashseed",
    "cuda_visible_devices",
    "records",
    "days_present",
    "stations",
    "window_start",
    "window_end",
    "fixture_stamp",
    "evidence_class",
    "data07_caveat",
    "december_representativeness",
    "apparatus_partition_id",
    "phase_id",
    "source_id",
    "target_definition_id",
    "m10_contract_fixture",
    "sequence",
    "assembly_assertion",
    "input_verification",
    "config_hashes",
    "snapshot_dir",
    "receipt",
    "matched_artifact_report",
    "runtime_seconds",
    "storage_bytes",
    "exemption",
    "identity_agreement",
    "freeze_record_agreement",
    "declared_inputs",
    "note",
    "measurements",
    "measuring_run_id",
    "measuring_run_ids",
    "min",
    "max",
    "units",
    "sources",
)


def _assert_phase1_field_contract() -> None:
    """R-24: the produced-field guard, called before this run's first write."""
    assert_no_raw_fields(PRODUCED_FIELDS, phase=PHASE)


# =======================================================================================
# Arguments and the stage entry
# =======================================================================================


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="run_walking_skeleton.py",
        description=(
            "Run one walking-skeleton fixture (TE 15): plumbing_7day, then scientific_1month, "
            "in order, before any full-year job (TE 9.2). Invokes TE 13.2's seven Phase 1 stage "
            "scripts at fixture scale, runs the M10 contract fixture after the plumbing fixture, "
            "compares against the FROZEN manifest and writes the fixture-pass receipt. REFUSES "
            "today: no manifest exists (BLK-02)."
        ),
    )
    parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="the governed configs directory (always configs/; TE 13.2)",
    )
    parser.add_argument(
        "--fixture",
        required=True,
        choices=FIXTURE_IDS,
        help="which of TE 15.1's two fixtures to run; scientific_1month requires the plumbing receipt",
    )
    parser.add_argument(
        "--emit-candidate",
        action="store_true",
        help=(
            "a MEASURING run: compose a `status: candidate` manifest from --identity plus this "
            "run's measurements (every measured field carries this run's registry id); never "
            "writes `frozen` (the owner's Q-31 act)"
        ),
    )
    parser.add_argument(
        "--identity",
        type=Path,
        default=None,
        help=(
            "the owner's identity declaration (kind: identity_declaration) a measuring run reads "
            "before any candidate exists; required with --emit-candidate"
        ),
    )
    parser.add_argument(
        "--measuring-runs",
        action="append",
        type=Path,
        default=None,
        help=(
            "additional measuring-result inputs for --emit-candidate (board Rec 5): a "
            "measuring_result_<run_id>.json file or a fixture root holding them, from "
            "another environment's run; repeatable. Ranges compose min/max over ALL runs, "
            "each run id stamped; a zero-width runtime/storage range refuses"
        ),
    )
    parser.add_argument(
        "--code-commit",
        type=str,
        default=None,
        help="explicit code commit for the lock where no git tree exists (Kaggle); never unpopulated",
    )
    parser.add_argument(
        "--python",
        type=str,
        default=sys.executable,
        help="the interpreter that runs the seven stage scripts and the M10 step (default: this one)",
    )
    args = parser.parse_args(argv)
    if args.emit_candidate and args.identity is None:
        parser.error("--emit-candidate requires --identity <declaration>: a measuring run reads "
                     "the owner's cited identity; nothing here invents it")
    if not args.emit_candidate and args.identity is not None:
        parser.error("--identity is read only by a measuring run (--emit-candidate); a comparison "
                     "run reads the manifest at its fixed path")
    if args.measuring_runs and not args.emit_candidate:
        parser.error("--measuring-runs aggregates measuring results for --emit-candidate only "
                     "(board Rec 5); a comparison run composes nothing")
    return args


def _scope_path(workspace: Path, args: argparse.Namespace) -> Path:
    if args.emit_candidate:
        identity = Path(args.identity)
        return identity if identity.is_absolute() else workspace / identity
    return manifest_path_for(workspace, args.fixture)


def _stage_entry(
    config_dir: Path, *, fixture_id: str, scope_path: Path | None, code_commit: str | None
) -> dict[str, Any]:
    """Steps 2-6 of the stage entry contract (step 1, determinism, ran in main()).

    2. `load_configs` — snapshot, hash, resolve roots (the only read of configs/).
    3. Preflight: `assert_no_tbd` over this stage's required fields (deliberately minimal, as
       every sibling's — the fixture's own refusals land in `_run` with an honest aborted
       row) and `assert_declared_sources_exist`.
    4. `assert_phase_boundary` — no raw-processing module loaded under phase 1.
    5. Seed.
    6. Capture the eight-item lock — `input_versions` binds the fixture scope's SHA-256 when
       the scope file exists (the receipt's row-hashed binding, SD-X-02 Rec 7) — assert it
       complete, and record the Q5 exemption (`require_receipts_for_snapshot` with the scope:
       a fixture run is not a full-year job). When no scope file exists yet the lock carries
       no input version (an empty list is a fact) and `_run` refuses at the load, naming it.
    """
    snapshot = load_configs(config_dir, phase=PHASE)
    assert_no_tbd(snapshot, required=required_fields_for(STAGE, PHASE))
    assert_declared_sources_exist(snapshot)
    assert_phase_boundary(PHASE, loaded_modules=sys.modules)
    determinism = seed_everything(snapshot, stage=STAGE)
    workspace = Path(snapshot.resolved_roots["workspace"])
    resolved_scope = scope_path if scope_path is not None else manifest_path_for(workspace, fixture_id)
    input_versions = (
        [fixture_input_version_tag(fixture_id, sha256_of_file(resolved_scope))]
        if resolved_scope.is_file()
        else []
    )
    lock = capture_environment_lock(
        snapshot, determinism, input_versions=input_versions, code_commit=code_commit
    )
    assert_lock_complete(lock)
    exemption = (
        require_receipts_for_snapshot(snapshot, lock, fixture_manifest=resolved_scope)
        if resolved_scope.is_file()
        else {"exempt": True, "reason": "fixture run; scope file absent, refused in _run"}
    )
    return {
        "snapshot": snapshot,
        "determinism": determinism,
        "lock": lock,
        "scope_path": resolved_scope,
        "exemption": exemption,
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
        "feature_set_id": str(snapshot.features.get("feature_set_id", "")),
        "model_id": "",
        "hyperparameters_json": "",
        "seed": "",
        "validation_metric_name": "",
        "validation_metric_value": "",
        "artifact_manifest_path": "",
        "prediction_hash": "",
        "locked_test_accessed": False,
        "notes": "walking-skeleton fixture run (TE 15; TE 9.2); never a full-year job",
    }
    if reason:
        row["reason"] = reason
    return row


# =======================================================================================
# The TE 13.2 sequence: commands, environment, execution (W-6 as consumed by the fixture run)
# =======================================================================================


def assert_phase1_invocation(script_name: str) -> None:
    """R-138 control 39: a Phase-2-only script in a Phase 1 clean run raises PhaseBoundaryError."""
    if script_name in PHASE2_ONLY_SCRIPTS:
        raise PhaseBoundaryError(
            f"scripts/{script_name}",
            "appears in TE 13.2 only below `# Phase 2, only after G-P2`; executing it inside "
            "the Phase 1 clean run would run raw processing TE 7.0's Phase 1 hard prohibition "
            "bars (NFR-PHASE-01; R-138 control 39; governance-guards R-23/R-24)",
        )
    if script_name not in {name for name, _phase in PHASE1_SEQUENCE}:
        raise IntegrityError(
            f"scripts/{script_name}",
            f"is not one of TE 13.2's seven Phase 1 stage-script invocations "
            f"{[n for n, _p in PHASE1_SEQUENCE]}; the clean run executes the fence verbatim",
        )


def lifecycle_arguments(script: str, fixture_id: str) -> list[str]:
    """Board Rec 4 (ML-03, owner-authorised per CR §11.5): the explicit output roots the
    orchestrator threads through 05/06/07 — all under the fixture root, so 05's bundles
    feed 06, 06's predictions feed 07, and the TE 15.4 outputs land where
    `collect_required_outputs` scans. Workspace-relative; POSIX-form for a platform-stable
    argv."""
    base = Path(WALKING_SKELETON_ROOT) / fixture_id
    if script.startswith("05_"):
        return ["--bundles-out", (base / "features").as_posix()]
    if script.startswith("06_"):
        return [
            "--bundles-root",
            (base / "features").as_posix(),
            "--predictions-out",
            (base / "predictions").as_posix(),
        ]
    if script.startswith("07_"):
        return [
            "--predictions-run",
            (base / "predictions").as_posix(),
            "--evaluation-out",
            (base / "evaluation").as_posix(),
        ]
    return []


def build_phase1_commands(
    *,
    python: str,
    scripts_dir: Path,
    config_dir: Path,
    scope_path: Path,
    fixture_id: str | None = None,
) -> list[list[str]]:
    """TE 13.2's seven Phase 1 invocations, in order, plus the ruled scope argument (Q4/Q5)
    and — when `fixture_id` is given — the Rec 4 lifecycle roots under the fixture root."""
    commands: list[list[str]] = []
    for script, phase in PHASE1_SEQUENCE:
        assert_phase1_invocation(script)
        argv = [python, str(Path(scripts_dir) / script), "--config", str(config_dir)]
        if phase is not None:
            argv += ["--phase", str(phase)]
        argv += [FIXTURE_SCOPE_OPTION, str(scope_path)]
        if fixture_id is not None:
            argv += lifecycle_arguments(script, fixture_id)
        commands.append(argv)
    return commands


def m10_command(python: str) -> list[str]:
    """The M10 contract-fixture step (Q12 = C): pytest over the two features-and-splits modules."""
    return [python, "-m", "pytest", *M10_MODULES]


def child_environment(base_env: Mapping[str, str], *, workspace: Path) -> dict[str, str]:
    """The subprocess environment: PYTHONHASHSEED already set (TE 13.2's first line, R-138
    control 20), NO GPU visible (`CUDA_VISIBLE_DEVICES=""`, TC-01, control 19)."""
    if not base_env.get("PYTHONHASHSEED"):
        raise IntegrityError(
            "PYTHONHASHSEED",
            "must be set before the first command of the clean run (TE 13.2, amended under "
            "CR-2026-08-22-TE-AMEND, ADR-10); the orchestrator's own step 1 sets it and a "
            "child never runs without it (R-138 control 20)",
        )
    env = dict(base_env)
    env["CUDA_VISIBLE_DEVICES"] = ""
    env.setdefault("TEC_WORKSPACE_ROOT", str(workspace))
    return env


def run_command(
    argv: Sequence[str], *, env: Mapping[str, str], cwd: Path, timeout: int = SUBPROCESS_TIMEOUT_S
) -> dict[str, Any]:
    """Run ONE command, recording its argv, exit code, timing and output tails."""
    started = dt.datetime.now(dt.UTC)
    clock = time.monotonic()
    try:
        completed = subprocess.run(  # noqa: S603 - fixed argv, no shell; the interpreter is ours
            list(argv), capture_output=True, text=True, env=dict(env), cwd=str(cwd), timeout=timeout,
            check=False,
        )
        returncode = completed.returncode
        stdout, stderr = completed.stdout, completed.stderr
    except subprocess.TimeoutExpired as exc:
        returncode = -1
        stdout = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        stderr = f"timeout after {timeout} s"
    except OSError as exc:
        returncode = -2
        stdout, stderr = "", f"could not start: {exc}"
    return {
        "argv": list(argv),
        "returncode": returncode,
        "started_at_utc": started.isoformat(),
        "ended_at_utc": dt.datetime.now(dt.UTC).isoformat(),
        "duration_seconds": time.monotonic() - clock,
        "stdout_tail": stdout[-_TAIL_CHARS:],
        "stderr_tail": stderr[-_TAIL_CHARS:],
    }


def run_sequence(
    commands: Sequence[Sequence[str]], *, env: Mapping[str, str], cwd: Path
) -> list[dict[str, Any]]:
    """Execute the commands in order; a non-zero exit stops the run, naming the script."""
    results: list[dict[str, Any]] = []
    for argv in commands:
        result = run_command(argv, env=env, cwd=cwd)
        results.append(result)
        if result["returncode"] != 0:
            raise IntegrityError(
                str(argv[1]) if len(argv) > 1 else " ".join(argv),
                f"exited {result['returncode']} inside the fixture run; the sequence stops at "
                f"the first refusal and reports it (stderr tail: {result['stderr_tail'][-600:]!r})",
            )
    return results


# =======================================================================================
# W-3 / W-4: lineage — verify the declared inputs, assemble on record dates
# =======================================================================================


def _month_manifest_entries(payload: Mapping[str, Any]) -> Mapping[str, str]:
    """Accept the flat `{name: sha256}` shape the existing evidence carries, or acquisition's
    `{"derived_artifacts": {...}}` shape."""
    if isinstance(payload.get("derived_artifacts"), Mapping):
        return {str(k): str(v) for k, v in payload["derived_artifacts"].items()}
    return {str(k): str(v) for k, v in payload.items() if isinstance(v, str)}


def verify_declared_inputs(
    scope: FixtureManifest | IdentityDeclaration, *, workspace: Path
) -> dict[str, Any]:
    """R-135 control 12 / limb 2: every declared derived artifact verifies against the month's
    `sha256_manifest.json` AND against its bytes on disk, BEFORE the fixture runs."""
    inputs = scope.data.get("inputs")
    declared = inputs.get("prepared_vtec") if isinstance(inputs, Mapping) else None
    if not isinstance(declared, Mapping):
        raise IntegrityError(
            scope.path,
            "inputs.prepared_vtec is required: the month's declared derived artifacts with their "
            "SHA-256 are the eligibility evidence re-verified at use (team.md; R-135 limb 2)",
        )
    evidence_dir = Path(workspace) / str(declared.get("evidence_dir", ""))
    month_manifest = evidence_dir / str(declared.get("sha256_manifest", "sha256_manifest.json"))
    if not month_manifest.is_file():
        raise IntegrityError(
            month_manifest,
            "the month's sha256_manifest.json is absent; eligibility is judged on derived-"
            "artifact verification and cannot be assumed from the selection record",
        )
    try:
        entries = _month_manifest_entries(json.loads(month_manifest.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrityError(month_manifest, f"unreadable ({exc})") from exc
    files = declared.get("files")
    if not isinstance(files, Mapping) or not files:
        raise IntegrityError(scope.path, "inputs.prepared_vtec.files must map artifact -> sha256")
    verified: dict[str, str] = {}
    for name, declared_hash in files.items():
        recorded = entries.get(str(name))
        if recorded is None:
            raise IntegrityError(
                month_manifest, f"declared artifact {name!r} is not hash-listed by the month"
            )
        if str(declared_hash).lower() != recorded.lower():
            raise IntegrityError(
                evidence_dir / str(name),
                f"declared SHA-256 {declared_hash} disagrees with the month's recorded {recorded} "
                f"(R-135 control 12)",
            )
        artifact = evidence_dir / str(name)
        if not artifact.is_file():
            raise IntegrityError(artifact, "declared derived artifact is absent from the evidence")
        actual = sha256_of_file(artifact)
        if actual != recorded.lower():
            raise IntegrityError(
                artifact,
                f"bytes hash to {actual} but the month's sha256_manifest.json records {recorded}; "
                f"the eligibility check re-executed at use FAILS before the fixture runs "
                f"(R-135 control 12; team.md, CHAIR-02)",
            )
        verified[str(name)] = actual
    records_file = str(declared.get("records_file", ""))
    if records_file not in verified:
        raise IntegrityError(
            scope.path,
            f"inputs.prepared_vtec.records_file {records_file!r} is not one of the verified "
            f"declared artifacts {sorted(verified)}",
        )
    return {
        "evidence_dir": str(evidence_dir),
        "sha256_manifest": str(month_manifest),
        "verified": verified,
        "records_file": records_file,
    }


def read_records_csv(path: Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def select_station_records(
    rows: Sequence[Mapping[str, Any]], stations: Sequence[str], *, station_key: str = "station"
) -> list[Mapping[str, Any]]:
    """Select the cited stations' records — SELECTION, before the assembled input is asserted."""
    wanted = {str(s) for s in stations}
    return [row for row in rows if str(row.get(station_key, "")) in wanted]


def assert_assembled_records(
    records: Sequence[Mapping[str, Any]],
    *,
    scope: FixtureManifest | IdentityDeclaration,
    station_key: str = "station",
    timestamp_key: str = "date",
) -> dict[str, Any]:
    """W-3 limb 2 + W-4 (FR-WS-3): the assembled input, asserted — not read.

    A record from a station other than the cited one(s) RAISES (R-135 control 9); every
    record's observation date lies inside the cited window and none in the locked month, on
    RECORD dates through `acquisition`'s predicates (R-136 control 14 — the folder a record
    came from is never consulted). Completeness figures are MEASURED and returned, never tested
    against a threshold (team.md § Walking Skeleton).
    """
    identity = scope.identity
    citation = identity.get("station_citation")
    stations = (
        [str(citation["station_id"])]
        if isinstance(citation, Mapping)
        else [str(s) for s in identity["stations"]]
    )
    for index, record in enumerate(records):
        station = str(record.get(station_key, ""))
        if station not in stations:
            raise IntegrityError(
                f"record {index} (station {station!r})",
                f"is not from the cited station(s) {stations}; one-station scope is a raise, not "
                f"a reading — assembly fails on a foreign-station record (TE 15.1 'One station'; "
                f"D-20; R-135 control 9)",
            )
    start, end = scope.window
    checked = assert_records_within_window(records, start=start, end=end, timestamp_key=timestamp_key)
    assert_no_locked_month_records(records, timestamp_key=timestamp_key)
    days = {str(record.get(timestamp_key, ""))[:10] for record in records}
    return {
        "records": checked,
        "stations": stations,
        "window_start": start.isoformat(),
        "window_end": end.isoformat(),
        "days_present": len(days & {d.isoformat() for d in window_days(scope)}),
        "window_days": len(window_days(scope)),
        "december_excluded_on": "record dates (acquisition.assert_no_locked_month_records)",
        "folder_name_consulted": False,
    }


# =======================================================================================
# TE 15.4: the required outputs, the hash listing, the run's own artifacts
# =======================================================================================


def collect_required_outputs(
    fixture_root: Path, scope: FixtureManifest | IdentityDeclaration
) -> tuple[dict[str, str], list[str]]:
    """Hash-list every TE 15.4 required output present under the fixture root; name the absent."""
    root = Path(fixture_root)
    listing: dict[str, str] = {}
    missing: list[str] = []
    for required in required_outputs_for(scope.fixture_id):
        matches = sorted(
            p for p in root.rglob("*")
            if p.is_file() and output_matches(str(p.relative_to(root)).replace("\\", "/"), required)
        )
        if not matches:
            missing.append(required)
            continue
        if len(matches) > 1:
            raise IntegrityError(
                root / required,
                f"{len(matches)} files match one TE 15.4 output; the listing is one hash per "
                f"output and cannot choose ({[str(m.relative_to(root)) for m in matches]})",
            )
        rel = str(matches[0].relative_to(root)).replace("\\", "/")
        listing[rel] = sha256_of_file(matches[0])
    return listing, missing


def _write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    return path


def _storage_bytes(root: Path) -> int:
    return sum(p.stat().st_size for p in Path(root).rglob("*") if p.is_file())


# =======================================================================================
# The run
# =======================================================================================


def _run(entry: Mapping[str, Any], args: argparse.Namespace, *, run_id: str) -> dict[str, Any]:
    _assert_phase1_field_contract()  # R-24: before the first write, always
    snapshot = entry["snapshot"]
    lock = entry["lock"]
    workspace = Path(snapshot.resolved_roots["workspace"])
    registry_path, access_log = _registry_paths(snapshot)
    scope_path: Path = entry["scope_path"]
    clock = time.monotonic()

    # 1. The manifest, ONLY through the loader (a missing one refuses naming the path).
    scope = load_fixture_scope(scope_path)
    if scope.fixture_id != args.fixture:
        raise IntegrityError(scope_path, f"names fixture {scope.fixture_id!r}, not {args.fixture!r}")
    if args.emit_candidate and not isinstance(scope, IdentityDeclaration):
        raise IntegrityError(
            scope_path,
            "--emit-candidate reads an identity declaration; a manifest is measured against, "
            "never re-measured over (R-134: re-measurement is a new candidate, a new freeze act)",
        )
    if not args.emit_candidate and not isinstance(scope, FixtureManifest):
        raise IntegrityError(
            scope_path,
            "a comparison run reads a fixture manifest; a declaration states no expectation — "
            "run with --emit-candidate to measure",
        )
    if args.emit_candidate and manifest_path_for(workspace, args.fixture).exists():
        raise IntegrityError(
            manifest_path_for(workspace, args.fixture),
            "a manifest already exists; it is preserved, never overwritten (R-134 obligation 3)",
        )

    # 2. Identity by citation, checked against the register; the freeze record when frozen.
    decisions = workspace / DECISIONS_PATH
    identity_agreement = assert_identity_agrees_with_decisions(scope, decisions_path=decisions)
    freeze_agreement: dict[str, Any] | None = None
    if isinstance(scope, FixtureManifest) and scope.is_frozen:
        freeze_agreement = assert_freeze_record_agrees(
            scope.path,
            decisions_path=decisions,
            freeze_decision=str(scope.identity["freeze_citation"]["decision"]),
            sidecar_dir=workspace / FREEZE_RECORD_SIDECAR_DIR,
        )

    # 3. Ordering: the scientific fixture requires a verified plumbing receipt (control 26).
    plumbing_receipt: Mapping[str, Any] | None = None
    if args.fixture == SCIENTIFIC_FIXTURE_ID:
        found = require_plumbing_receipt(
            registry_path=registry_path,
            plumbing_manifest_path=manifest_path_for(workspace, PLUMBING_FIXTURE_ID),
            receipt_path=receipt_path_for(workspace, PLUMBING_FIXTURE_ID),
            lock=lock,
        )
        plumbing_receipt = found["payload"]

    # 4. Lineage: verify the declared inputs BEFORE anything runs; assemble on record dates.
    verification = verify_declared_inputs(scope, workspace=workspace)
    rows = read_records_csv(Path(verification["evidence_dir"]) / verification["records_file"])
    citation = scope.identity.get("station_citation")
    stations = (
        [str(citation["station_id"])] if isinstance(citation, Mapping) else list(scope.identity["stations"])
    )
    assembled = select_station_records(rows, stations)
    assembly = assert_assembled_records(assembled, scope=scope)

    # 5. The fixture's own TE 15.4 artifacts, stamped by the producing path.
    stamp = stamp_for_manifest(scope)
    fixture_root = fixture_root_for(workspace, args.fixture)
    fixture_root.mkdir(parents=True, exist_ok=True)
    _write_json(
        fixture_root / INPUT_MANIFEST_NAME,
        stamp_fixture_artifact(
            {"kind": "input_manifest", "declared_inputs": verification, "assembly_assertion": assembly},
            stamp,
        ),
    )
    _write_json(
        fixture_root / CONFIG_SNAPSHOT_NAME,
        stamp_fixture_artifact(
            {
                "kind": "processing_config_snapshot",
                "config_hashes": dict(snapshot.hashes),
                "snapshot_dir": str(snapshot.snapshot_dir),
            },
            stamp,
        ),
    )
    _write_json(
        fixture_root / REGISTRY_ENTRY_NAME,
        stamp_fixture_artifact({"kind": "registry_entry", "run_id": run_id, "platform": snapshot.platform}, stamp),
    )

    # 6. TE 13.2's seven Phase 1 invocations, in order, no GPU visible; then the M10 step.
    env = child_environment(os.environ, workspace=workspace)
    commands = build_phase1_commands(
        python=args.python, scripts_dir=REPO_ROOT / "scripts", config_dir=Path(args.config),
        scope_path=scope_path, fixture_id=args.fixture,
    )
    sequence = run_sequence(commands, env=env, cwd=workspace)
    m10: dict[str, Any] | None = None
    if args.fixture == PLUMBING_FIXTURE_ID:
        m10 = run_command(m10_command(args.python), env=env, cwd=REPO_ROOT)
        m10["note"] = (
            "M10 contract fixture (features-and-splits authored; run here, Q12 = C): clean-run "
            "evidence, NOT a third receipt; gates no full-year job (TC-03f)"
        )
        if m10["returncode"] != 0:
            raise IntegrityError(
                "M10 contract fixture",
                f"exited {m10['returncode']}; the negative control on the ADR-11 mechanism failed "
                f"(stderr tail: {m10['stderr_tail'][-600:]!r})",
            )

    # 7. The run log and the test report (both TE 15.4 outputs), then the hash listing.
    _write_json(
        fixture_root / TEST_REPORT_NAME,
        stamp_fixture_artifact({"kind": "test_report", "sequence": sequence, "m10_contract_fixture": m10}, stamp),
    )
    listing, missing = collect_required_outputs(fixture_root, scope)
    run_log = stamp_fixture_artifact(
        {
            "kind": "clean_run_log",
            "fixture_id": args.fixture,
            "run_id": run_id,
            "platform": snapshot.platform,
            "pythonhashseed": env.get("PYTHONHASHSEED"),
            "cuda_visible_devices": env.get("CUDA_VISIBLE_DEVICES"),
            "exemption": entry["exemption"],
            "identity_agreement": identity_agreement,
            "freeze_record_agreement": freeze_agreement,
            "input_verification": verification,
            "assembly_assertion": assembly,
            "commands": [c["argv"] for c in sequence],
            "m10_contract_fixture": m10,
            "missing_required_outputs": [m for m in missing if m not in (RUN_LOG_NAME.replace(".json", ".*"), ARTIFACT_MANIFEST_NAME)],
        },
        stamp,
    )
    _write_json(fixture_root / RUN_LOG_NAME, run_log)
    listing, missing = collect_required_outputs(fixture_root, scope)
    _write_json(
        fixture_root / ARTIFACT_MANIFEST_NAME,
        stamp_fixture_artifact(
            {"kind": "artifact_manifest", "fixture_id": args.fixture, "outputs": listing,
             "missing_required_outputs": missing},
            stamp,
        ),
    )
    runtime_seconds = time.monotonic() - clock
    storage_bytes = _storage_bytes(fixture_root)
    if missing:
        raise IntegrityError(
            fixture_root / ARTIFACT_MANIFEST_NAME,
            f"fixture run incomplete: TE 15.4 required output(s) absent {missing}; recorded as "
            f"a machine-readable field on the listing, and no pass is claimed",
        )

    # 8. Against a FROZEN manifest: compare, assert ranges, write the receipt.
    summary: dict[str, Any] = {
        "fixture_root": str(fixture_root),
        "runtime_seconds": runtime_seconds,
        "storage_bytes": storage_bytes,
    }
    if isinstance(scope, FixtureManifest):
        matched = compare_required_outputs(scope, fixture_root)
        assert_run_level_ranges(scope, runtime_seconds=runtime_seconds, storage_bytes=storage_bytes)
        receipt = write_fixture_pass_receipt(
            manifest=scope,
            result=RESULT_PASS,
            run_id=run_id,
            lock=lock,
            snapshot=snapshot,
            registry_path=registry_path,
            access_log_path=access_log,
            receipt_path=receipt_path_for(workspace, args.fixture),
            registry_row=_registry_row(run_id, status="completed", lock_hash=environment_lock_hash(lock), snapshot=snapshot),
            phase=PHASE,
            plumbing_receipt=plumbing_receipt,
        )
        summary.update({"matched_artifact_report": matched, "receipt": receipt["receipt_run_id"]})
        return summary

    # 9. A measuring run (board Recs 4-5, owner-authorised per CR §11.5): fold the stage-
    #    emitted measurement blocks into THIS run's measuring result, persist it, then
    #    compose min/max RANGES over every measuring result available — this run's, prior
    #    runs' under the fixture root, and any --measuring-runs aggregation inputs from
    #    other environments' fixture roots. Composition refuses a zero-width runtime or
    #    storage range (a single run measures a point, not a range), and the schema refuses
    #    an incomplete candidate rather than inventing one.
    run_measurements: dict[str, dict[str, Any]] = {
        "runtime": {
            "cpu_total": {"min": runtime_seconds, "max": runtime_seconds, "units": "s"},
            "storage_total": {"min": storage_bytes, "max": storage_bytes, "units": "bytes"},
        },
    }
    for area, quantities in collect_stage_measurements(fixture_root).items():
        block = run_measurements.setdefault(area, {})
        for key, value in quantities.items():
            block[key] = {"min": value["min"], "max": value["max"], "units": value["units"]}
    write_measuring_result(fixture_root, run_id=run_id, measurements=run_measurements)
    results = load_measuring_results(fixture_root)
    for extra in args.measuring_runs or []:
        extra_path = Path(extra) if Path(extra).is_absolute() else workspace / extra
        results.extend(load_measuring_results(extra_path))
    seen_run_ids: set[str] = set()
    for result in results:
        rid = str(result.get("measuring_run_id"))
        if rid in seen_run_ids:
            raise IntegrityError(
                f"measuring result {rid}",
                "duplicate measuring_run_id across the aggregated results; every measuring "
                "run is one recorded execution (NFR-AUD-01; board Rec 5)",
            )
        seen_run_ids.add(rid)
    composed = compose_measurement_ranges(results)  # refuses a zero-width range (Rec 5)
    template = scope.data.get("required_outputs", {}).get("comparison_ledger", {})
    candidate = compose_candidate_manifest(
        scope.data,
        fixture_id=args.fixture,
        measurements=composed,
        measuring_run_id="+".join(sorted(seen_run_ids)),
        outputs=sorted(listing),
        comparison_ledger=template,
        artifact_manifest_ref=os.path.relpath(fixture_root / ARTIFACT_MANIFEST_NAME, manifest_path_for(workspace, args.fixture).parent),
    )
    written = write_candidate_manifest(manifest_path_for(workspace, args.fixture), candidate)
    summary["candidate_manifest"] = str(written)
    summary["measuring_run_ids"] = sorted(seen_run_ids)
    return summary


def main() -> int:
    ensure_process_determinism(sys.argv)  # FIRST statement, before any framework import
    args = _parse_args(sys.argv[1:])

    try:
        probe_workspace = Path(os.environ.get("TEC_WORKSPACE_ROOT") or Path.cwd())
        scope_path = _scope_path(probe_workspace, args) if args.emit_candidate else None
        entry = _stage_entry(
            args.config, fixture_id=args.fixture, scope_path=scope_path, code_commit=args.code_commit
        )
    except IntegrityError as exc:
        # Integrity tier before the run record exists: terminate non-zero naming the resource
        # and the violated expectation; no terminal row is fabricated for a run that never
        # opened a started row (R-08) — exactly as the seven siblings do.
        print(f"run_walking_skeleton: preflight refusal: {exc}", file=sys.stderr)
        return 1

    snapshot = entry["snapshot"]
    lock = entry["lock"]
    lock_hash = environment_lock_hash(lock)
    registry_path, access_log = _registry_paths(snapshot)
    run_id = (
        f"walking-skeleton-{args.fixture}-{dt.datetime.now(dt.UTC).strftime('%Y%m%dT%H%M%SZ')}"
        f"-{uuid.uuid4().hex[:8]}"
    )

    started = _registry_row(run_id, status="started", lock_hash=lock_hash, snapshot=snapshot)
    started["code_commit"] = lock.code_commit
    append_registry_event(
        registry_path, started, phase=PHASE, writer_role="stage", access_log_path=access_log
    )

    try:
        summary = _run(entry, args, run_id=run_id)
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
        print(f"run_walking_skeleton: aborted: {exc}", file=sys.stderr)
        return 1

    completed = _registry_row(run_id, status="completed", lock_hash=lock_hash, snapshot=snapshot)
    completed["code_commit"] = lock.code_commit
    completed["artifact_manifest_path"] = str(Path(summary["fixture_root"]) / ARTIFACT_MANIFEST_NAME)
    append_registry_event(
        registry_path, completed, phase=PHASE, writer_role="stage", access_log_path=access_log
    )
    print(f"run_walking_skeleton: completed: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
