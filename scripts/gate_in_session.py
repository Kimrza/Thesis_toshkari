"""TC-03g gate wrapper: the critical set and both fixtures, INSIDE the Kaggle session.

Purpose
-------
The production caller `src/data/fixture_gate.py: emit_in_session_gate_result` never had
(`GOV-2026-09-20-CG-01` Recommendation 28: its only callers were test modules, so
`in_session_gate_result.json` was never produced and `require_in_session_gate` — the
refusal written to check it — had nothing to judge).

TC-03g (`constraint-register.md`, `binding: hard`; `project.md` § Mandated) requires the
critical test set and BOTH walking-skeleton fixtures to run **inside the Kaggle session**
before any governed run executed there, because a Kaggle session carries no git working
tree: a commit hook cannot fire there and a local suite run proves nothing about the
environment the governed run actually executes in (TE §9.1, §9.2; TA-03, TA-26).

This script is that one session's orchestrator. It:

1. loads the four governed configs and **REFUSES unless the resolved platform is
   `kaggle`** — early and by name, rather than after forty minutes of fixtures, since
   `require_in_session_gate` would refuse a `local` stamp anyway (control 30);
2. captures this session's TE §13.1 environment lock;
3. runs the **critical test set** as a subprocess with `--junitxml`, deselecting the three
   modules that read bytes under the December custody root — the same split criterion
   `.githooks/pre-commit` § 2 derives and states (Recommendation 30), because those belong
   to an occasion carrying an authorization to record (Vision §8.3), not to a gate run;
4. runs **both fixtures in order** through `scripts/run_walking_skeleton.py` — plumbing
   first, and the scientific fixture only if plumbing passed, because TE §9.2's ordering
   is a sequencing rule, not a preference;
5. emits the gate result through `emit_in_session_gate_result`, which writes
   `artifacts/walking_skeleton/in_session_gate_result.json` **write-once** and records its
   own append-only registry rows;
6. immediately passes the result back through `require_in_session_gate` against this
   session's own lock and the frozen manifests in force. That is a self-check, not a
   tautology: the three refusals are about the platform stamp, code-commit / config-hash
   agreement and frozen-manifest agreement, so a misconfigured session is caught here
   rather than by the next reader of the artifact.

What it never does
------------------
It computes no metric, reads no December byte, and judges no scientific result. A green
gate is a statement about the ENVIRONMENT, not about the science. It also does not emit
G-07's `environment_and_cpu_preflight_report`: that artifact is
`src/data/fixture_evidence.py: build_environment_and_cpu_preflight_report`'s, and it
already refuses when no gate result is supplied — this script produces the input that
refusal asks for.

Inputs
------
`--config configs/`; `--phase 1|2`; `--code-commit <sha>` (REQUIRED in a Kaggle session:
there is no git tree to read `HEAD` from); `--python` (the interpreter for the
subprocesses, default `sys.executable`); `--critical-tests` (repeatable, defaults to the
whole `tests/` tree minus the restricted readers); `--skip-fixtures` is deliberately NOT
offered — a gate that can be told to skip half of what it certifies is not a gate.

Re-run behaviour
----------------
The gate result is write-once (`emit_in_session_gate_result`), so a second run in the same
workspace refuses rather than overwriting; move or version the previous result to re-gate.
Every run appends `started` then `completed|aborted` registry rows for itself, and the
emitter appends its own child rows (NFR-AUD-01: a failed run stays visible with its
status and reason). Exit 0 only when the result was emitted AND accepted; 1 otherwise.
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import (  # noqa: E402
    IntegrityError,
    assert_lock_complete,
    capture_environment_lock,
    ensure_process_determinism,
    environment_lock_hash,
    load_configs,
    seed_everything,
)
from src.data.experiment_registry import append_registry_event  # noqa: E402
from src.data.fixture_gate import (  # noqa: E402
    KAGGLE,
    emit_in_session_gate_result,
    gate_result_path_for,
    require_in_session_gate,
)
from src.data.fixture_manifest import FIXTURE_IDS, manifest_path_for  # noqa: E402
from src.data.preflight_report import read_junit_module_outcomes  # noqa: E402

STAGE = "in-session-gate"
WRITER_ROLE = "gate_in_session"

#: Deselected from the critical set here for the reason `.githooks/pre-commit` § 2 states:
#: each READS BYTES from under the December custody root (D-15; the path literal lives in
#: `src/data/locked_test.py` alone, R-28's one door), and a December read
#: belongs to an occasion carrying an authorization to record, never to a gate run that
#: happens to sweep the tree. Kept as a named list so the deselection is visible in the
#: gate result rather than implied by an ignore flag.
RESTRICTED_READERS: tuple[str, ...] = (
    "tests/test_release_hashes.py",
    "tests/test_acquisition_window.py",
    "tests/test_phase_boundary.py",
)


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="gate_in_session.py", description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--phase", type=int, choices=(1, 2), default=1)
    parser.add_argument(
        "--code-commit",
        required=True,
        help="the commit the uploaded tree was taken from; a Kaggle session has no git tree",
    )
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument(
        "--critical-tests",
        action="append",
        default=None,
        help="test path(s) forming the critical set; default the tests/ tree minus the "
        "three restricted readers",
    )
    parser.add_argument("--junit-out", type=Path, default=None)
    return parser.parse_args(argv)


def critical_test_command(python: str, targets: list[str], junit: Path) -> list[str]:
    """The pytest invocation, with the restricted readers deselected BY NAME."""
    argv = [python, "-m", "pytest", "-q", *targets, "-p", "no:cacheprovider"]
    for module in RESTRICTED_READERS:
        argv.append(f"--ignore={module}")
    argv.append(f"--junitxml={junit}")
    return argv


def fixture_command(python: str, config_dir: Path, fixture_id: str, code_commit: str) -> list[str]:
    return [
        python,
        str(REPO_ROOT / "scripts" / "run_walking_skeleton.py"),
        "--config",
        str(config_dir),
        "--fixture",
        fixture_id,
        "--code-commit",
        code_commit,
    ]


def summarise_junit(junit: Path) -> dict[str, str]:
    """Per-module `passed` / `failed` from the junit an actual run wrote.

    Reuses `preflight_report.read_junit_module_outcomes` rather than parsing junit a second
    time: two parsers drift, and this project has already paid for one drifting copy
    (`nfr-design` c58). A module with zero executed cases never appears — the emitter
    refuses an empty result set, which is the right failure for a suite that did not run.
    """
    outcomes = read_junit_module_outcomes(junit)
    return {
        module: ("failed" if counts["failed"] or counts["errors"] else "passed")
        for module, counts in outcomes.items()
    }


def _registry_row(
    run_id: str, *, status: str, lock_hash: str, snapshot: Any, reason: str = ""
) -> dict[str, Any]:
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    row: dict[str, Any] = {
        "run_id": run_id,
        "started_at_utc": now,
        "completed_at_utc": now if status in ("completed", "aborted", "failed") else "",
        "status": status,
        "code_commit": "",
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
        "notes": "TC-03g in-session gate (TE 9.1/9.2); never a governed scientific run",
    }
    if reason:
        row["reason"] = reason
    return row


def main(argv: list[str] | None = None) -> int:
    ensure_process_determinism(sys.argv)
    args = _parse_args(argv)

    try:
        snapshot = load_configs(args.config, phase=args.phase)
    except IntegrityError as exc:
        print(f"gate_in_session: preflight refusal: {exc}", file=sys.stderr)
        return 1

    # Refuse a non-Kaggle platform BEFORE running anything. `require_in_session_gate`
    # refuses a `local` stamp at step 6 anyway (control 30); refusing here means an
    # operator learns it in a second rather than after both fixtures.
    if snapshot.platform != KAGGLE:
        print(
            f"gate_in_session: refusing: resolved platform is {snapshot.platform!r}, not "
            f"{KAGGLE!r}. TC-03g is about the environment a governed run actually executes "
            f"in; a result stamped anywhere else proves nothing about the Kaggle session and "
            f"is refused by require_in_session_gate (control 30). Set TEC_PLATFORM=kaggle in "
            f"the session, or do not claim the gate.",
            file=sys.stderr,
        )
        return 1

    workspace = Path(snapshot.resolved_roots["workspace"])
    artifacts = Path(snapshot.resolved_roots["artifacts"])
    registry_path = (
        Path(snapshot.resolved_roots.get("registry_root", artifacts / "registry"))
        / "experiment_registry.jsonl"
    )
    access_log = workspace / "evidence" / "merge_run_access_log.jsonl"

    determinism = seed_everything(snapshot, stage=STAGE)
    lock = capture_environment_lock(snapshot, determinism, code_commit=args.code_commit)
    assert_lock_complete(lock)
    lock_hash = environment_lock_hash(lock)
    run_id = f"in-session-gate-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    started_row = _registry_row(run_id, status="started", lock_hash=lock_hash, snapshot=snapshot)
    started_row["code_commit"] = lock.code_commit
    append_registry_event(
        registry_path,
        started_row,
        phase=args.phase,
        writer_role=WRITER_ROLE,
        access_log_path=access_log,
    )

    started_at = dt.datetime.now(dt.timezone.utc)
    junit = args.junit_out or (artifacts / "exec_evidence" / f"{run_id}" / "junit_in_session.xml")
    junit.parent.mkdir(parents=True, exist_ok=True)

    def _abort(reason: str) -> int:
        row = _registry_row(
            run_id, status="aborted", lock_hash=lock_hash, snapshot=snapshot, reason=reason
        )
        row["code_commit"] = lock.code_commit
        append_registry_event(
            registry_path,
            row,
            phase=args.phase,
            writer_role=WRITER_ROLE,
            access_log_path=access_log,
        )
        print(f"gate_in_session: aborted: {reason}", file=sys.stderr)
        return 1

    # --- 3. the critical set ------------------------------------------------------------
    targets = args.critical_tests or [str(REPO_ROOT / "tests")]
    tests = subprocess.run(  # noqa: S603 - fixed argv, no shell
        critical_test_command(args.python, targets, junit),
        cwd=str(workspace),
        capture_output=True,
        text=True,
        check=False,
    )
    print(tests.stdout[-4000:])
    if not junit.is_file():
        return _abort(
            f"the critical set wrote no junit at {junit}; a gate cannot record a per-test "
            f"result set that does not exist (exit {tests.returncode})"
        )
    critical_results = summarise_junit(junit)
    if tests.returncode != 0:
        failed = sorted(m for m, r in critical_results.items() if r == "failed")
        return _abort(
            f"the critical set failed inside the session (exit {tests.returncode}); failing "
            f"module(s): {failed or 'not attributable from the junit'}. TC-03g's whole point "
            f"is that this is discovered HERE, before a governed run"
        )

    # --- 4. both fixtures, in order ------------------------------------------------------
    fixture_results: dict[str, str] = {}
    for fixture_id in FIXTURE_IDS:
        completed = subprocess.run(  # noqa: S603 - fixed argv, no shell
            fixture_command(args.python, args.config, fixture_id, args.code_commit),
            cwd=str(workspace),
            capture_output=True,
            text=True,
            check=False,
        )
        print(completed.stdout[-2000:])
        fixture_results[fixture_id] = "passed" if completed.returncode == 0 else "failed"
        if completed.returncode != 0:
            return _abort(
                f"fixture {fixture_id} did not pass inside the session (exit "
                f"{completed.returncode}); TE 9.2 runs both fixtures before any full-year "
                f"job and the second only after the first passes. stderr tail: "
                f"{completed.stderr[-600:]!r}"
            )

    completed_at = dt.datetime.now(dt.timezone.utc)
    manifests = {fid: manifest_path_for(workspace, fid) for fid in FIXTURE_IDS}

    # --- 5 + 6. emit, then judge what was emitted ---------------------------------------
    try:
        result = emit_in_session_gate_result(
            snapshot=snapshot,
            lock=lock,
            manifests=manifests,
            critical_test_results=critical_results,
            fixture_results=fixture_results,
            started_at_utc=started_at.isoformat(),
            completed_at_utc=completed_at.isoformat(),
            registry_path=registry_path,
            access_log_path=access_log,
            result_path=gate_result_path_for(workspace),
            registry_row=_registry_row(
                run_id, status="completed", lock_hash=lock_hash, snapshot=snapshot
            ),
            run_id=run_id,
            phase=args.phase,
        )
        verdict = require_in_session_gate(result, lock=lock, manifests=manifests)
    except IntegrityError as exc:
        return _abort(f"gate result refused: {exc}")

    row = _registry_row(run_id, status="completed", lock_hash=lock_hash, snapshot=snapshot)
    row["code_commit"] = lock.code_commit
    row["artifact_manifest_path"] = str(gate_result_path_for(workspace))
    append_registry_event(
        registry_path,
        row,
        phase=args.phase,
        writer_role=WRITER_ROLE,
        access_log_path=access_log,
    )
    print(
        f"gate_in_session: accepted on {verdict['platform']}; "
        f"{len(critical_results)} critical module(s), fixtures {fixture_results}; "
        f"measured total {verdict['measured_total_runtime_seconds']} s -> "
        f"{gate_result_path_for(workspace)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
