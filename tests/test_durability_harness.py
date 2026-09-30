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


def test_partial_acknowledged_receipt_fails_and_partial_unacknowledged_passes(tmp_path) -> None:
    h = _harness()
    body = json.dumps({"receipt": 1}) + "\n"
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    (tmp_path / "receipt_000001.json").write_bytes(body.encode("utf-8"))
    (tmp_path / "receipt_000002.json").write_text('{"rec', encoding="utf-8")
    assert h.verify("receipt", tmp_path, [(1, digest)])["pass"]
    assert not h.verify("receipt", tmp_path, [(1, digest), (2, "x")])["pass"]


@pytest.mark.parametrize("write_type", ["access", "registry", "receipt"])
def test_one_real_kill_trial_per_write_type(tmp_path, write_type) -> None:
    h = _harness()
    result = h.kill_trial(write_type, tmp_path / write_type, random.Random(1))
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
