"""D-88 rulings (2026-10-02): runtime ranges per environment; storage stays pooled.

Purpose
-------
D-87's runtime range was pooled over (a) `tec-thesis-311` and (c) `g07-clean-run`. Windows and
Linux differ by about 2x, and the range was measured under one power profile. The D-87
verifications matched every output and still failed TA-17 in both directions: (a) at
635-663 s under a capped profile, and (c) at 173 s under the Performance profile. These tests
cover the remedy: composition keeps a range per `environment_id`, and a run is checked
against its own environment's runtime range. Storage stays pooled (second ruling): within one
environment two runs differ by a few bytes, while sessions drift by hundreds to thousands, so a
per-environment storage range would fail on byte noise. Inputs: synthetic measuring results.
Re-run behaviour: pure.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from src.data.config import IntegrityError
from src.data.fixture_manifest import assert_run_level_ranges, compose_measurement_ranges

from test_clean_run import MANIFEST_NAME, PLUMBING_FIXTURE_ID, write_and_load

A, C = "tec-thesis-311", "g07-clean-run"


def _result(run_id: str, env: str | None, seconds: float, storage: int) -> dict:
    out = {
        "measuring_run_id": run_id,
        "measurements": {
            "runtime": {
                "cpu_total": {"min": seconds, "max": seconds, "units": "s"},
                "storage_total": {"min": storage, "max": storage, "units": "bytes"},
            }
        },
    }
    if env is not None:
        out["environment_id"] = env
    return out


RESULTS = [
    _result("a1", A, 390.0, 2_311_000),
    _result("a2", A, 420.0, 2_312_000),
    _result("c1", C, 170.0, 2_345_000),
    _result("c2", C, 180.0, 2_346_000),
]


def test_ranges_are_composed_per_environment():
    composed = compose_measurement_ranges(RESULTS)
    cpu = composed["runtime"]["cpu_total"]
    assert (cpu["min"], cpu["max"]) == (170.0, 420.0)
    assert cpu["by_environment"][A]["min"] == 390.0 and cpu["by_environment"][A]["max"] == 420.0
    assert cpu["by_environment"][C]["measuring_run_ids"] == ["c1", "c2"]
    storage = composed["runtime"]["storage_total"]
    assert "by_environment" not in storage
    assert (storage["min"], storage["max"]) == (2_311_000, 2_346_000)


def test_zero_width_range_in_one_environment_refuses():
    flat = [*RESULTS[:2], _result("c1", C, 170.0, 2_345_000), _result("c2", C, 170.0, 2_345_500)]
    same_storage = [*RESULTS[:2], _result("c1", C, 170.0, 2_345_000), _result("c2", C, 180.0, 2_345_000)]
    compose_measurement_ranges(same_storage)  # a flat per-environment STORAGE range is fine
    with pytest.raises(IntegrityError, match="in g07-clean-run"):
        compose_measurement_ranges(flat)


def test_results_without_environment_keep_the_pooled_range():
    pooled = compose_measurement_ranges([_result("r1", None, 10.0, 5), _result("r2", None, 12.0, 6)])
    assert "by_environment" not in pooled["runtime"]["cpu_total"]


def _manifest_with_ranges(tmp_path: Path):
    manifest = write_and_load(tmp_path, PLUMBING_FIXTURE_ID, status="candidate")
    composed = compose_measurement_ranges(RESULTS)
    data = json.loads(json.dumps(manifest.data))
    for key in ("cpu_total", "storage_total"):
        data["runtime"][key] = {**composed["runtime"][key], "measuring_run_id": "a1+a2+c1+c2"}
    return type(manifest)(**{**manifest.__dict__, "data": data})


def test_a_run_is_checked_against_its_own_environment(tmp_path):
    manifest = _manifest_with_ranges(tmp_path)
    assert assert_run_level_ranges(
        manifest, runtime_seconds=175.0, storage_bytes=2_345_500, environment_id=C
    )["range_scope"] == C
    with pytest.raises(IntegrityError, match="outside the frozen range"):
        assert_run_level_ranges(manifest, runtime_seconds=175.0, storage_bytes=2_311_500, environment_id=A)
    assert assert_run_level_ranges(  # storage is pooled: an (a)-sized figure is fine in (c)
        manifest, runtime_seconds=175.0, storage_bytes=2_311_500, environment_id=C
    )["within"]
    with pytest.raises(IntegrityError, match="storage"):
        assert_run_level_ranges(manifest, runtime_seconds=175.0, storage_bytes=2_400_000, environment_id=C)
    with pytest.raises(IntegrityError, match="outside the frozen range"):
        assert_run_level_ranges(manifest, runtime_seconds=400.0, storage_bytes=2_345_500, environment_id=C)


def test_unknown_or_missing_environment_refuses(tmp_path):
    manifest = _manifest_with_ranges(tmp_path)
    with pytest.raises(IntegrityError, match="no range was measured"):
        assert_run_level_ranges(manifest, runtime_seconds=400.0, storage_bytes=2_311_500, environment_id="b01_iri")
    with pytest.raises(IntegrityError, match="naming no environment"):
        assert_run_level_ranges(manifest, runtime_seconds=400.0, storage_bytes=2_311_500)


def test_pooled_manifest_still_checks_the_pooled_range(tmp_path):
    manifest = write_and_load(tmp_path, PLUMBING_FIXTURE_ID, status="candidate")
    assert assert_run_level_ranges(
        manifest, runtime_seconds=10.0, storage_bytes=10, environment_id=A
    )["range_scope"] == "pooled"
    assert (tmp_path / PLUMBING_FIXTURE_ID / MANIFEST_NAME).is_file()
