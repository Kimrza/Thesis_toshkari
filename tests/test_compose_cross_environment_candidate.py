"""Refusals of scripts/compose_cross_environment_candidate.py (closure 2026-10-01).

The script composes a candidate from recorded measuring results only; these negative
controls prove it refuses a composition that would not be the precommitted run set.
Re-run: pure, writes only under tmp_path.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def _mod():
    spec = importlib.util.spec_from_file_location(
        "compose_xenv", REPO_ROOT / "scripts" / "compose_cross_environment_candidate.py"
    )
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _result(tmp_path: Path, run_id: str) -> Path:
    p = tmp_path / f"measuring_result_{run_id}.json"
    p.write_text(json.dumps({"measuring_run_id": run_id, "environment_id": "tec-thesis-311"}),
                 encoding="utf-8")
    return p


IDENTITY = REPO_ROOT / "tests" / "fixtures" / "plumbing_7day" / "identity_declaration.yaml"


def test_refuses_duplicate_run_ids(tmp_path: Path) -> None:
    m = _mod()
    a = _result(tmp_path, "r1")
    with pytest.raises(m.IntegrityError, match="duplicate"):
        m.compose(fixture="plumbing_7day", identity=IDENTITY, results=[a, a], outputs_run="r1")


def test_refuses_a_single_run(tmp_path: Path) -> None:
    m = _mod()
    with pytest.raises(m.IntegrityError, match="at least two"):
        m.compose(fixture="plumbing_7day", identity=IDENTITY,
                  results=[_result(tmp_path, "r1")], outputs_run="r1")


def test_refuses_outputs_run_outside_the_composed_set(tmp_path: Path) -> None:
    m = _mod()
    with pytest.raises(m.IntegrityError, match="not one of the composed"):
        m.compose(fixture="plumbing_7day", identity=IDENTITY,
                  results=[_result(tmp_path, "r1"), _result(tmp_path, "r2")],
                  outputs_run="r3")
