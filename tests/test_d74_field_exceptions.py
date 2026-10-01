"""D-74 amendment 2 (2026-10-01, Student ruling): TE 13.7 applied field by field.

Purpose
-------
Two `exact` outputs embed model-output floats. `mask_manifest.json`'s `mask_id` hashes the
masked rows including the predictions (R-107 limb 1), and `checkpoint_manifest.json` records
`restored_validation_rmse`. Both differed between (a) `tec-thesis-311` and (c) `g07-clean-run`
by about 1e-6 to 1e-8, within the frozen prediction tolerance. So no (c) run could pass a
fixture comparison, and R-140 refused every (c) `scientific_1month` run. These tests are the
negative controls for the amendment: a float-free `membership_id` compared exactly everywhere,
`mask_id` exact within the reference's own environment only, and `restored_validation_rmse`
under its item 11 tolerance. Everything else stays exact.

Inputs: the synthetic manifest apparatus of `tests/test_clean_run.py`. Re-run behaviour:
pure, `tmp_path` only.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

import pytest
from src.data.config import IntegrityError
from src.data.cross_environment_tolerance import (
    A_ENVIRONMENT,
    C_ENVIRONMENT,
    DeterminismFailure,
    ToleranceFailure,
)
from src.data.fixture_manifest import (
    CANDIDATE,
    compare_required_outputs,
    load_fixture_manifest,
    validate_manifest_mapping,
)
from src.data.release import sha256_of_file
from src.evaluation.masks import compute_mask_id, compute_membership_id

from test_clean_run import (
    FROZEN,
    MANIFEST_NAME,
    PLUMBING_FIXTURE_ID,
    SIBLING_HASH_NAME,
    build_manifest_mapping,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

MASK_EXC = {
    "citation": "D-74 amendment 2",
    "environment_bound": [{"locator": r"/masks\[\d+\]/mask_id", "reason": "R-107 limb 1"}],
}
CKPT_FIELDS = [
    {
        "field": "restored_validation_rmse",
        "locator": r"/entries\[\d+\]/restored_validation_rmse",
        "unit": "TECU",
        "meaning": "validation RMSE of the restored checkpoint",
        "citation": "TE 13.7; D-74 amendment 2",
    }
]
CKPT_TOL = {
    "fields": {
        "restored_validation_rmse": {
            "unit": "TECU",
            "tolerance": 1e-6,
            "statistic": 3e-7,
            "floor": 2e-6,
            "elements": 2,
        }
    },
    "environment_ids": [A_ENVIRONMENT, C_ENVIRONMENT],
    "measuring_run_id": "run-a1+run-c1",
}
MASKS = {
    "masks": [
        {"set_id": "primary", "mask_id": "a" * 64, "membership_id": "b" * 64, "row_counts": {"S": 3}}
    ]
}
CHECKPOINTS = {
    "entries": [
        {"model_id": "M-06", "restored_epoch": 12, "restored_validation_rmse": 16.593359789183356},
        {"model_id": "M-06", "restored_epoch": 9, "restored_validation_rmse": 14.954789964643071},
    ]
}


def _frozen(tmp_path: Path, *, with_tolerance: bool = True, reference_env: str | None = A_ENVIRONMENT):
    root = tmp_path / "reference"
    root.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=FROZEN)
    listing = json.loads((root / "artifact_manifest.json").read_text(encoding="utf-8"))
    ledger = data["required_outputs"]["comparison_ledger"]
    for name, kind, doc, exc in (
        ("mask_manifest.json", "partition_membership", MASKS, MASK_EXC),
        ("checkpoint_manifest.json", "id", CHECKPOINTS, {"citation": "D-74 amendment 2", "toleranced_fields": CKPT_FIELDS}),
    ):
        (root / name).write_text(json.dumps(doc, indent=2), encoding="utf-8")
        listing["outputs"][name] = sha256_of_file(root / name)
        ledger[name]["exact_kind"] = kind
        ledger[name]["field_exceptions"] = json.loads(json.dumps(exc))
    if with_tolerance:
        ledger["checkpoint_manifest.json"]["field_exceptions"]["fp_tolerance"] = json.loads(
            json.dumps(CKPT_TOL)
        )
    if reference_env is not None:
        data["required_outputs"]["reference_environment_id"] = reference_env
    (root / "artifact_manifest.json").write_text(
        json.dumps(listing, indent=2, sort_keys=True), encoding="utf-8"
    )
    path = root / MANIFEST_NAME
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    (root / SIBLING_HASH_NAME).write_text(sha256_of_file(path) + "\n", encoding="utf-8")
    return load_fixture_manifest(path, parsed=data), data


def _produce(manifest, tmp_path: Path, *, masks=None, checkpoints=None) -> Path:
    produced = tmp_path / "produced"
    for name in manifest.outputs:
        target = produced / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((manifest.artifact_manifest_path.parent / name).read_bytes())
    if masks is not None:
        (produced / "mask_manifest.json").write_text(json.dumps(masks), encoding="utf-8")
    if checkpoints is not None:
        (produced / "checkpoint_manifest.json").write_text(json.dumps(checkpoints), encoding="utf-8")
    return produced


def _with(doc: dict[str, Any], path: tuple, value: Any) -> dict[str, Any]:
    out = json.loads(json.dumps(doc))
    node = out
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = value
    return out


def test_mask_id_is_environment_bound_and_membership_id_is_not(tmp_path):
    manifest, _ = _frozen(tmp_path)
    other_mask_id = _with(MASKS, ("masks", 0, "mask_id"), "c" * 64)
    produced = _produce(manifest, tmp_path, masks=other_mask_id)
    report = compare_required_outputs(manifest, produced, environment_id=C_ENVIRONMENT)
    assert report["outputs"]["mask_manifest.json"]["environment_bound_skipped"] == 1
    with pytest.raises(IntegrityError, match="environment-bound field /masks\\[0\\]/mask_id"):
        compare_required_outputs(manifest, produced, environment_id=A_ENVIRONMENT)
    moved = _with(other_mask_id, ("masks", 0, "membership_id"), "d" * 64)
    (produced / "mask_manifest.json").write_text(json.dumps(moved), encoding="utf-8")
    with pytest.raises(IntegrityError, match="membership_id"):
        compare_required_outputs(manifest, produced, environment_id=C_ENVIRONMENT)


def test_environment_bound_comparison_needs_an_environment(tmp_path):
    manifest, _ = _frozen(tmp_path)
    produced = _produce(manifest, tmp_path, masks=_with(MASKS, ("masks", 0, "mask_id"), "c" * 64))
    with pytest.raises(IntegrityError, match="keyed to no environment"):
        compare_required_outputs(manifest, produced)


def test_checkpoint_rmse_under_its_item11_tolerance(tmp_path):
    manifest, _ = _frozen(tmp_path)
    near = _with(CHECKPOINTS, ("entries", 0, "restored_validation_rmse"), 16.59335993287129)
    produced = _produce(manifest, tmp_path, checkpoints=near)
    report = compare_required_outputs(manifest, produced, environment_id=C_ENVIRONMENT)
    assert report["outputs"]["checkpoint_manifest.json"]["toleranced_checked"] == 2
    far = _with(CHECKPOINTS, ("entries", 0, "restored_validation_rmse"), 16.6)
    (produced / "checkpoint_manifest.json").write_text(json.dumps(far), encoding="utf-8")
    with pytest.raises(ToleranceFailure):
        compare_required_outputs(manifest, produced, environment_id=C_ENVIRONMENT)


def test_checkpoint_identity_fields_stay_exact(tmp_path):
    manifest, _ = _frozen(tmp_path)
    produced = _produce(
        manifest, tmp_path, checkpoints=_with(CHECKPOINTS, ("entries", 0, "restored_epoch"), 13)
    )
    with pytest.raises(IntegrityError, match="restored_epoch"):
        compare_required_outputs(manifest, produced, environment_id=C_ENVIRONMENT)


def test_toleranced_field_refused_in_an_environment_that_showed_no_determinism(tmp_path):
    manifest, _ = _frozen(tmp_path)
    near = _with(CHECKPOINTS, ("entries", 0, "restored_validation_rmse"), 16.59335993287129)
    produced = _produce(manifest, tmp_path, checkpoints=near)
    with pytest.raises(DeterminismFailure):
        compare_required_outputs(manifest, produced, environment_id="b01_iri")


def test_frozen_manifest_requires_the_composed_tolerance(tmp_path):
    with pytest.raises(IntegrityError, match="item 11 per-field tolerance"):
        _frozen(tmp_path, with_tolerance=False)


def test_environment_bound_requires_reference_environment(tmp_path):
    with pytest.raises(IntegrityError, match="reference_environment_id"):
        _frozen(tmp_path, reference_env=None)


@pytest.mark.parametrize(
    "mutate, match",
    [
        (lambda e: e.pop("citation"), "cited"),
        (lambda e: e.__setitem__("environment_bound", [{"locator": "(", "reason": "x"}]), "compile"),
        (lambda e: e.__setitem__("environment_bound", []), "neither"),
    ],
)
def test_field_exception_shape_refusals(tmp_path, mutate, match):
    root = tmp_path / "r"
    root.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=CANDIDATE)
    entry = data["required_outputs"]["comparison_ledger"]["mask_manifest.json"]
    entry["exact_kind"] = "partition_membership"
    entry["field_exceptions"] = json.loads(json.dumps(MASK_EXC))
    data["required_outputs"]["reference_environment_id"] = A_ENVIRONMENT
    mutate(entry["field_exceptions"])
    with pytest.raises(IntegrityError, match=match):
        validate_manifest_mapping(data, manifest_path=root / MANIFEST_NAME, file_sha256=None)


def test_field_exceptions_refused_on_structure_kinds(tmp_path):
    root = tmp_path / "r"
    root.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=CANDIDATE)
    entry = data["required_outputs"]["comparison_ledger"]["registry_entry.json"]
    entry["exact_kind"] = "schema"
    entry["field_exceptions"] = json.loads(json.dumps(MASK_EXC))
    data["required_outputs"]["reference_environment_id"] = A_ENVIRONMENT
    with pytest.raises(IntegrityError, match="value-exact kinds only"):
        validate_manifest_mapping(data, manifest_path=root / MANIFEST_NAME, file_sha256=None)


def test_membership_id_ignores_values_but_not_keys():
    rows = [
        {"station": "S1", "interval_start_utc": "2022-03-15T00:00:00+00:00", "y_true": 10.0, "y_hats": {"M-06": 11.0}},
        {"station": "S2", "interval_start_utc": "2022-03-15T00:00:00+00:00", "y_true": 12.0, "y_hats": {"M-06": 12.5}},
    ]
    drifted = [dict(r, y_hats={"M-06": r["y_hats"]["M-06"] + 1e-7}) for r in rows]
    assert compute_membership_id("primary", ["M-06", "B-01"], rows) == compute_membership_id(
        "primary", ["B-01", "M-06"], list(reversed(drifted))
    )
    assert compute_mask_id("primary", ["M-06"], rows) != compute_mask_id("primary", ["M-06"], drifted)
    assert compute_membership_id("primary", ["M-06"], rows) != compute_membership_id(
        "primary", ["M-06"], rows[:1]
    )


def _runner():
    spec = importlib.util.spec_from_file_location(
        "run_walking_skeleton", REPO_ROOT / "scripts" / "run_walking_skeleton.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_runner_composes_the_in_exact_toleranced_field():
    rws = _runner()
    template = {
        "checkpoint_manifest.json": {
            "comparison_class": "exact",
            "exact_kind": "id",
            "field_exceptions": {"citation": "D-74 amendment 2", "toleranced_fields": CKPT_FIELDS},
        }
    }
    assert set(rws.exact_toleranced_fields(template)) == {"checkpoint_manifest.json"}
    full = {"/entries[0]/restored_epoch": 12.0, "/entries[0]/restored_validation_rmse": 16.5}
    assert rws.restrict_fingerprint(full, CKPT_FIELDS) == {"/entries[0]/restored_validation_rmse": 16.5}
    results = []
    for env, runs in ((A_ENVIRONMENT, ("a1", "a2")), (C_ENVIRONMENT, ("c1", "c2"))):
        for rid in runs:
            value = 16.5 if env == A_ENVIRONMENT else 16.5000001
            results.append(
                {
                    "measuring_run_id": rid,
                    "environment_id": env,
                    "fingerprints": {
                        "checkpoint_manifest.json": {"/entries[0]/restored_validation_rmse": value}
                    },
                }
            )
    composed = rws.compose_tolerances(results, template, [])
    field = composed["checkpoint_manifest.json"]["fields"]["restored_validation_rmse"]
    assert field["unit"] == "TECU" and field["tolerance"] > 0
