"""D-74 amendment 3 (2026-10-01, Student ruling): parquet exactness by value; 2 ULP across envs.

Purpose
-------
A (c) `g07-clean-run` comparison of `plumbing_7day` met (a)'s reference value for value
everywhere except three cyclical-encoding columns of `feature_table.parquet`, which differed
by exactly 1 ULP (glibc against the Windows runtime's `sin`/`cos`). Two other tables were
value-identical but not byte-identical. These are the negative controls for the amendment:
- parquet tables are compared by value;
- a float64 column must be bit-identical within one environment;
- across environments, a column may differ by at most 2 ULP, and only on a
  `deterministic_cpu_transformation` output;
- schema, row count, NaN positions and non-float columns stay exact everywhere.

Inputs: the synthetic manifest apparatus of `tests/test_clean_run.py`. Re-run behaviour:
pure, `tmp_path` only.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from src.data.config import IntegrityError
from src.data.fixture_manifest import (
    CROSS_ENVIRONMENT_MAX_ULP,
    compare_required_outputs,
    load_fixture_manifest,
)
from src.data.release import sha256_of_file

from test_clean_run import (
    FROZEN,
    MANIFEST_NAME,
    PLUMBING_FIXTURE_ID,
    SIBLING_HASH_NAME,
    build_manifest_mapping,
)

A_ENV, C_ENV = "tec-thesis-311", "g07-clean-run"
TABLE = "feature_table.parquet"


def _table(sin_values, *, station=("BSHM", "BSHM", "BSHM")) -> pa.Table:
    return pa.table(
        {
            "station": list(station),
            "utc_hour_sin": pa.array(sin_values, type=pa.float64()),
            "lag_1": pa.array([1.5, float("nan"), 2.5], type=pa.float64()),
        }
    )


BASE = [0.25881904510252074, 0.5, 0.7071067811865476]


def _frozen(tmp_path: Path, *, kind: str = "deterministic_cpu_transformation"):
    root = tmp_path / "reference"
    root.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=FROZEN)
    pq.write_table(_table(BASE), root / TABLE)
    listing = json.loads((root / "artifact_manifest.json").read_text(encoding="utf-8"))
    listing["outputs"][TABLE] = sha256_of_file(root / TABLE)
    (root / "artifact_manifest.json").write_text(json.dumps(listing, sort_keys=True), encoding="utf-8")
    data["required_outputs"]["comparison_ledger"][TABLE]["exact_kind"] = kind
    data["required_outputs"]["reference_environment_id"] = A_ENV
    path = root / MANIFEST_NAME
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    (root / SIBLING_HASH_NAME).write_text(sha256_of_file(path) + "\n", encoding="utf-8")
    return load_fixture_manifest(path, parsed=data)


def _produce(manifest, tmp_path: Path, table: pa.Table, **write_kwargs) -> Path:
    produced = tmp_path / "produced"
    for name in manifest.outputs:
        target = produced / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((manifest.artifact_manifest_path.parent / name).read_bytes())
    pq.write_table(table, produced / TABLE, **write_kwargs)
    return produced


def _shift(values, ulp):
    return [float(np.nextafter(v, np.inf)) if ulp == 1 else float(v + ulp * np.spacing(v)) for v in values]


def test_value_equal_tables_with_different_bytes_match(tmp_path):
    manifest = _frozen(tmp_path)
    produced = _produce(manifest, tmp_path, _table(BASE), compression="gzip")
    assert sha256_of_file(produced / TABLE) != sha256_of_file(manifest.artifact_manifest_path.parent / TABLE)
    report = compare_required_outputs(manifest, produced, environment_id=A_ENV)
    assert report["outputs"][TABLE]["values_equal"] is True


def test_one_ulp_refused_within_one_environment(tmp_path):
    manifest = _frozen(tmp_path)
    produced = _produce(manifest, tmp_path, _table(_shift(BASE, 1)), compression="gzip")
    with pytest.raises(IntegrityError, match="1 ULP"):
        compare_required_outputs(manifest, produced, environment_id=A_ENV)


def test_one_ulp_admitted_across_environments(tmp_path):
    manifest = _frozen(tmp_path)
    produced = _produce(manifest, tmp_path, _table(_shift(BASE, 1)))
    report = compare_required_outputs(manifest, produced, environment_id=C_ENV)
    assert report["outputs"][TABLE]["ulp_by_column"] == {"utc_hour_sin": 1}
    assert report["outputs"][TABLE]["ulp_allowance"] == CROSS_ENVIRONMENT_MAX_ULP == 2


def test_three_ulp_refused_across_environments(tmp_path):
    manifest = _frozen(tmp_path)
    produced = _produce(manifest, tmp_path, _table(_shift(BASE, 3)))
    with pytest.raises(IntegrityError, match="3 ULP"):
        compare_required_outputs(manifest, produced, environment_id=C_ENV)


def test_allowance_only_for_deterministic_transformations(tmp_path):
    manifest = _frozen(tmp_path, kind="id")
    produced = _produce(manifest, tmp_path, _table(_shift(BASE, 1)))
    with pytest.raises(IntegrityError, match="1 ULP"):
        compare_required_outputs(manifest, produced, environment_id=C_ENV)


def test_non_float_column_and_nan_positions_stay_exact(tmp_path):
    manifest = _frozen(tmp_path)
    produced = _produce(manifest, tmp_path, _table(BASE, station=("BSHM", "BSHM", "NICO")))
    with pytest.raises(IntegrityError, match="column station"):
        compare_required_outputs(manifest, produced, environment_id=C_ENV)
    moved_nan = _table(BASE).set_column(2, "lag_1", pa.array([float("nan"), 1.5, 2.5]))
    produced = _produce(manifest, tmp_path / "x", moved_nan)
    with pytest.raises(IntegrityError, match="NaN positions"):
        compare_required_outputs(manifest, produced, environment_id=C_ENV)


def test_schema_and_unreadable_tables_refused(tmp_path):
    manifest = _frozen(tmp_path)
    renamed = _table(BASE).rename_columns(["station", "utc_hour_cos", "lag_1"])
    produced = _produce(manifest, tmp_path, renamed)
    with pytest.raises(IntegrityError, match="schema differs"):
        compare_required_outputs(manifest, produced, environment_id=C_ENV)
    (produced / TABLE).write_bytes(b"not a parquet file")
    with pytest.raises(IntegrityError, match="cannot be read as parquet"):
        compare_required_outputs(manifest, produced, environment_id=C_ENV)
