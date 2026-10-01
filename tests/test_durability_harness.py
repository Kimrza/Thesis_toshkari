"""D-83 revision 7 §W7 W-6: the durability harness's verifier is not vacuous.

Purpose: a harness that passes every trial proves nothing unless its verifier fails a
damaged file. Each test hands `verify` a deliberately damaged scratch directory and asserts
the trial FAILS; the undamaged cases assert it passes. Inputs: synthetic files in
`tmp_path`. Re-run behaviour: pure. One end-to-end kill trial per write type runs the real
child process.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def _harness():
    spec = importlib.util.spec_from_file_location(
        "durability_harness_under_test", REPO_ROOT / "scripts" / "durability_harness.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _access_rows(path: Path, ids, tail: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(json.dumps({"run_id": f"durability-{i:06d}"}) + "\n" for i in ids)
    path.write_text(body + tail, encoding="utf-8")


def test_intact_log_with_unacknowledged_extra_row_passes(tmp_path) -> None:
    h = _harness()
    _access_rows(tmp_path / "merge_run_access_log.jsonl", [1, 2, 3])
    assert h.verify("access", tmp_path, [(1, None), (2, None)])["pass"]


def test_torn_unacknowledged_tail_is_reported_not_failed(tmp_path) -> None:
    h = _harness()
    _access_rows(tmp_path / "merge_run_access_log.jsonl", [1, 2], tail='{"run_id": "durab')
    result = h.verify("access", tmp_path, [(1, None), (2, None)])
    assert result["pass"] and result["torn_tail"]


def test_lost_acknowledged_row_fails(tmp_path) -> None:
    h = _harness()
    _access_rows(tmp_path / "merge_run_access_log.jsonl", [1])
    result = h.verify("access", tmp_path, [(1, None), (2, None)])
    assert not result["pass"] and "lost" in result["problems"][0]


def test_corrupt_complete_line_fails(tmp_path) -> None:
    h = _harness()
    path = tmp_path / "merge_run_access_log.jsonl"
    _access_rows(path, [1])
    with path.open("a", encoding="utf-8") as handle:
        handle.write("{garbage\n")
    assert not h.verify("access", tmp_path, [(1, None)])["pass"]


def test_altered_acknowledged_receipt_fails(tmp_path) -> None:
    h = _harness()
    body = json.dumps({"receipt": 1}) + "\n"
    (tmp_path / "receipt_000001.json").write_text(json.dumps({"receipt": 2}) + "\n", encoding="utf-8")
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    assert not h.verify("receipt", tmp_path, [(1, digest)])["pass"]


def test_any_partial_receipt_at_a_final_name_fails(tmp_path) -> None:
    """Complete-or-absent (D-83 revision 8 section A8 item 6): a partial file at a FINAL
    name fails whether or not it was acknowledged. Before revision 8 an unacknowledged
    partial receipt was tolerated; the hard-link writer makes that state a defect."""
    h = _harness()
    body = json.dumps({"receipt": 1}) + "\n"
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    (tmp_path / "receipt_000001.json").write_bytes(body.encode("utf-8"))
    assert h.verify("receipt", tmp_path, [(1, digest)])["pass"]
    (tmp_path / "receipt_000002.json").write_text('{"rec', encoding="utf-8")
    result = h.verify("receipt", tmp_path, [(1, digest)])
    assert not result["pass"]
    assert result["outcome"] == "partial_final"
    assert not h.verify("receipt", tmp_path, [(1, digest), (2, "x")])["pass"]


# --- D-83 revision 8 section A8 item 14: deterministic in-write interruption -----------------


@pytest.mark.parametrize(
    ("write_type", "n", "point", "outcome"),
    [
        ("access", 1, "mid-record", "torn_detected"),
        ("registry", 1, "mid-record", "torn_detected"),
        ("receipt", 1, "mid-temp-write", "intact_old"),
        ("receipt", 2, "before-link", "intact_old"),
        ("receipt", 3, "after-link", "intact_new"),
    ],
)
def test_one_real_torn_trial_per_injection_point(tmp_path, write_type, n, point, outcome) -> None:
    h = _harness()
    result = h.torn_trial(write_type, tmp_path / write_type, random.Random(1), n)  # noqa: S311 - trial selection, not cryptography
    assert result["pass"], result["problems"]
    assert result["injection_point"] == point
    assert result["outcome"] == outcome == result["expected_outcome"]


def test_undetected_torn_registry_record_fails(tmp_path, monkeypatch) -> None:
    """Negative control: a torn tail the reader does not report is a failure."""
    import src.data.experiment_registry as reg

    h = _harness()
    good = json.dumps({"run_id": "durability-000001", "status": "started"}) + "\n"
    (tmp_path / "experiment_registry.jsonl").write_text(good + '{"run_id": "durab', encoding="utf-8")
    real = reg.check_registry_integrity

    def blind(path):
        import dataclasses

        return dataclasses.replace(real(path), torn_final_run_id=None, torn_final_reported=None)

    monkeypatch.setattr(reg, "check_registry_integrity", blind)
    result = h.verify("registry", tmp_path, [(1, None)])
    assert not result["pass"]
    assert result["outcome"] == "torn_undetected"


def test_unreached_injection_point_fails_the_trial(tmp_path, monkeypatch) -> None:
    """A trial whose child never reports INJECTED is never a pass (no silent fallback)."""
    h = _harness()
    monkeypatch.setattr(h, "_INJECTED_MARKER", "NEVER-PRINTED")
    monkeypatch.setattr(h, "TORN_TRIAL_TIMEOUT_S", 5)
    result = h.torn_trial("registry", tmp_path / "r", random.Random(1), 1)  # noqa: S311 - trial selection, not cryptography
    assert not result["pass"]
    assert any("never reached" in p for p in result["problems"])


def test_dirty_tree_is_refused_without_allow_dirty(tmp_path, monkeypatch) -> None:
    h = _harness()
    monkeypatch.setattr(
        h,
        "working_tree_state",
        lambda: {"dirty": True, "governed_changes": [" M src/x.py"], "other_tracked_changes": []},
    )
    with pytest.raises(SystemExit, match="dirty"):
        h.main(["--fault", "kill-torn", "--out", str(tmp_path), "--scratch", str(tmp_path / "s")])


def test_untracked_governed_file_makes_the_tree_dirty(monkeypatch) -> None:
    h = _harness()

    class _Done:
        def __init__(self, out):
            self.stdout = out

    def run(argv, **_k):
        if "--" in argv:  # the governed-path query
            return _Done("?? src/data/new_module.py\n")
        return _Done(" M aidlc/audit.md\n")

    monkeypatch.setattr(h.subprocess, "run", run)
    state = h.working_tree_state()
    assert state["dirty"]
    assert state["governed_changes"] == ["?? src/data/new_module.py"]
    assert state["other_tracked_changes"] == [" M aidlc/audit.md"]


def test_non_code_tracked_change_is_recorded_not_dirty(monkeypatch) -> None:
    h = _harness()

    class _Done:
        def __init__(self, out):
            self.stdout = out

    monkeypatch.setattr(
        h.subprocess,
        "run",
        lambda argv, **_k: _Done("" if "--" in argv else " M governance/x.md\n"),
    )
    state = h.working_tree_state()
    assert not state["dirty"]
    assert state["other_tracked_changes"] == [" M governance/x.md"]


def test_b01_iri_label_requires_its_pinned_interpreter(monkeypatch) -> None:
    h = _harness()
    monkeypatch.setenv("TEC_ENVIRONMENT_ID", "b01_iri")
    monkeypatch.setattr(h.sys, "version_info", (3, 11, 0))
    assert h._campaign_environment_id() == "undeclared"
    monkeypatch.setattr(h.sys, "version_info", (3, 10, 12))
    assert h._campaign_environment_id() == "b01_iri"


@pytest.mark.parametrize("write_type", ["access", "registry", "receipt"])
def test_one_real_kill_trial_per_write_type(tmp_path, write_type) -> None:
    h = _harness()
    result = h.kill_trial(write_type, tmp_path / write_type, random.Random(1))  # noqa: S311 - trial selection, not cryptography
    assert result["pass"], result["problems"]
    assert result["acknowledged"] >= 1


def test_power_loss_is_refused_by_the_harness(tmp_path) -> None:
    h = _harness()
    with pytest.raises(SystemExit) as exc:
        h.main(["--fault", "power-loss", "--out", str(tmp_path), "--scratch", str(tmp_path / "s")])
    assert "power-loss trials are not run" in str(exc.value)


def test_non_governed_interpreter_is_not_labelled_governed(monkeypatch) -> None:
    """GOV-2026-09-30-PV-09 ML-03 / DATA-05: a 3.14 run is `undeclared`, not tec-thesis-311."""
    h = _harness()
    monkeypatch.setenv("TEC_ENVIRONMENT_ID", "tec-thesis-311")
    monkeypatch.setattr(h.sys, "version_info", (3, 14, 0))
    assert h._campaign_environment_id() == "undeclared"
    monkeypatch.setattr(h.sys, "version_info", (3, 11, 16))
    assert h._campaign_environment_id() == "tec-thesis-311"
