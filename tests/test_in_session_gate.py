"""`scripts/gate_in_session.py` — TC-03g's production caller, and the four refusals.

`GOV-2026-09-20-CG-01` Recommendation 28: `emit_in_session_gate_result` had callers only in
test modules, so `in_session_gate_result.json` was never produced and
`require_in_session_gate` — the refusal written to check it — had nothing to judge. The
wrapper is that caller. These controls prove the guard bites at each of its three named
boundaries (R-141 controls 30, 31, 32) plus the absence case, and that the wrapper refuses a
non-Kaggle platform before running anything.

Synthetic throughout: no fixture runs, no December byte, no real Kaggle session.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import IntegrityError, RunRecord  # noqa: E402
from src.data.fixture_gate import (  # noqa: E402
    GATE_RESULT_KIND,
    KAGGLE,
    require_in_session_gate,
)
from src.data.fixture_manifest import FIXTURE_IDS  # noqa: E402


def _load_wrapper() -> Any:
    spec = importlib.util.spec_from_file_location(
        "gate_in_session", REPO_ROOT / "scripts" / "gate_in_session.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


GATE = _load_wrapper()


def _Lock(code_commit: str = "c" * 40, config_hashes: Any = None) -> RunRecord:
    """A synthetic TE 13.1 lock; only `code_commit` and `config_hashes` matter to the guard."""
    return RunRecord(
        requirements_hash="a" * 64,
        pip_freeze="synthetic==0.0",
        runtime_versions={"python": "3.11.16"},
        code_commit=code_commit,
        config_hashes=config_hashes or {"data.yaml": "d" * 64},
        input_versions=[],
        platform=KAGGLE,
        nondeterministic_ops=[],
    )


def _manifest_pair(tmp_path: Path) -> dict[str, Path]:
    """A FROZEN synthetic manifest per fixture, built through `test_clean_run`'s own writer
    so this module never grows a second manifest builder to drift from that one."""
    from test_clean_run import FROZEN, write_and_load

    return {fid: write_and_load(tmp_path, fid, status=FROZEN).path for fid in FIXTURE_IDS}


def _result(lock: _Lock, manifests: dict[str, Path], **overrides: Any) -> dict[str, Any]:
    from src.data.fixture_gate import _frozen_hashes, lock_items

    now = dt.datetime.now(dt.timezone.utc)
    payload: dict[str, Any] = {
        "kind": GATE_RESULT_KIND,
        "platform": KAGGLE,
        "environment_lock": lock_items(lock),
        "frozen_manifest_hashes": _frozen_hashes(manifests),
        "started_at_utc": now.isoformat(),
        "completed_at_utc": now.isoformat(),
        "critical_test_results": {"tests/test_iri_denial.py": "passed"},
        "fixture_results": dict.fromkeys(FIXTURE_IDS, "passed"),
        "measured_total_runtime_seconds": 12.5,
    }
    payload.update(overrides)
    return payload


# --- the must-not-fire limb: a well-formed result is ACCEPTED ---------------------------


def test_a_well_formed_kaggle_result_is_accepted(tmp_path: Path) -> None:
    lock, manifests = _Lock(), _manifest_pair(tmp_path)
    verdict = require_in_session_gate(_result(lock, manifests), lock=lock, manifests=manifests)
    assert verdict["accepted"] is True
    assert verdict["platform"] == KAGGLE
    assert verdict["measured_total_runtime_seconds"] == 12.5


# --- R-141 control 30: the platform stamp ------------------------------------------------


def test_a_local_stamped_result_is_refused(tmp_path: Path) -> None:
    lock, manifests = _Lock(), _manifest_pair(tmp_path)
    with pytest.raises(IntegrityError) as excinfo:
        require_in_session_gate(
            _result(lock, manifests, platform="local"), lock=lock, manifests=manifests
        )
    message = str(excinfo.value)
    assert "local" in message and "TC-03g" in message


# --- R-141 control 31: the code commit / config hashes -----------------------------------


def test_a_result_from_another_sessions_code_is_refused(tmp_path: Path) -> None:
    """The defect this catches is subtle and is exactly BENCH-01's: a gate result that is
    perfectly valid — for a DIFFERENT session's code."""
    manifests = _manifest_pair(tmp_path)
    earlier, current = _Lock(code_commit="0" * 40), _Lock(code_commit="c" * 40)
    with pytest.raises(IntegrityError) as excinfo:
        require_in_session_gate(_result(earlier, manifests), lock=current, manifests=manifests)
    assert "code_commit" in str(excinfo.value)


def test_a_result_with_other_config_hashes_is_refused(tmp_path: Path) -> None:
    manifests = _manifest_pair(tmp_path)
    earlier = _Lock(config_hashes={"data.yaml": "e" * 64})
    with pytest.raises(IntegrityError) as excinfo:
        require_in_session_gate(_result(earlier, manifests), lock=_Lock(), manifests=manifests)
    assert "config_hashes" in str(excinfo.value)


# --- R-141 control 32: the frozen manifests in force -------------------------------------


def test_a_result_predating_a_manifest_refreeze_is_refused(tmp_path: Path) -> None:
    lock = _Lock()
    manifests = _manifest_pair(tmp_path)
    stale = _result(lock, manifests)
    # The manifests are RE-FROZEN after the gate ran: the mapping is rewritten with a
    # different selection rule and its sibling hash recomputed, so the hashes the result
    # recorded no longer name the manifests in force. Mutating the file WITHOUT refreshing
    # the sibling would exercise the tamper check instead, which is a different guard.
    import json

    from src.data.release import sha256_of_file

    from test_clean_run import SIBLING_HASH_NAME, build_manifest_mapping

    for fid in FIXTURE_IDS:
        root = manifests[fid].parent
        data = build_manifest_mapping(fid, root, status="frozen")
        data["identity"]["selection_rule"] = "synthetic apparatus, re-frozen 2026-09-22"
        manifests[fid].write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
        (root / SIBLING_HASH_NAME).write_text(
            sha256_of_file(manifests[fid]) + "\n", encoding="utf-8"
        )
    with pytest.raises(IntegrityError) as excinfo:
        require_in_session_gate(stale, lock=lock, manifests=manifests)
    assert "frozen-manifest hashes" in str(excinfo.value)


def test_a_payload_that_is_not_a_gate_result_is_refused(tmp_path: Path) -> None:
    lock, manifests = _Lock(), _manifest_pair(tmp_path)
    with pytest.raises(IntegrityError):
        require_in_session_gate(
            _result(lock, manifests, kind="fixture_pass_receipt"), lock=lock, manifests=manifests
        )


# --- the wrapper's own contract ----------------------------------------------------------


def test_the_wrapper_deselects_exactly_the_three_restricted_readers() -> None:
    """The split criterion is `.githooks/pre-commit` § 2's, applied by name rather than by a
    pattern that could quietly widen or narrow."""
    assert set(GATE.RESTRICTED_READERS) == {
        "tests/test_release_hashes.py",
        "tests/test_acquisition_window.py",
        "tests/test_phase_boundary.py",
    }
    argv = GATE.critical_test_command("py", ["tests"], Path("j.xml"))
    for module in GATE.RESTRICTED_READERS:
        assert f"--ignore={module}" in argv
    assert "--junitxml=j.xml" in argv


def test_the_wrapper_offers_no_way_to_skip_a_fixture() -> None:
    """A gate that can be told to skip half of what it certifies is not a gate: the parser
    must expose no skip/only flag for the fixtures, and both ids must be run."""
    source = (REPO_ROOT / "scripts" / "gate_in_session.py").read_text(encoding="utf-8")
    for forbidden in ("--skip-fixtures", "--only-fixture", "--no-fixtures"):
        assert f'"{forbidden}"' not in source
    assert "for fixture_id in FIXTURE_IDS:" in source


def test_the_wrapper_refuses_a_non_kaggle_platform_before_running_anything(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Control 30 would refuse a `local` result at the end anyway; refusing at the START is
    what stops an operator spending both fixtures to learn it. Proven by asserting that no
    subprocess is launched."""
    launched: list[Any] = []
    monkeypatch.setattr(GATE.subprocess, "run", lambda *a, **k: launched.append(a))
    monkeypatch.setattr(GATE, "ensure_process_determinism", lambda *a, **k: None)

    class _Snapshot:
        platform = "local"
        features: dict[str, Any] = {}
        resolved_roots = {"workspace": tmp_path, "artifacts": tmp_path / "artifacts"}
        hashes: dict[str, str] = {}

    monkeypatch.setattr(GATE, "load_configs", lambda *a, **k: _Snapshot())
    code = GATE.main(["--config", str(tmp_path), "--code-commit", "c0ffee"])
    assert code == 1
    assert launched == [], "no subprocess may run once the platform check has refused"


def test_the_junit_summary_reuses_the_one_parser(tmp_path: Path) -> None:
    """One junit parser project-wide (`nfr-design` c58: a second, drifting copy is the
    failure mode). A failing case must render `failed`, a passing one `passed`."""
    junit = tmp_path / "j.xml"
    junit.write_text(
        "<testsuites><testsuite name='pytest'>"
        "<testcase classname='tests.test_a' name='t1' file='tests/test_a.py'/>"
        "<testcase classname='tests.test_b' name='t2' file='tests/test_b.py'>"
        "<failure message='boom'/></testcase>"
        "</testsuite></testsuites>",
        encoding="utf-8",
    )
    assert GATE.summarise_junit(junit) == {
        "tests/test_a.py": "passed",
        "tests/test_b.py": "failed",
    }
