"""R-139 regression: a comparison run compares against a reference it cannot overwrite.

Purpose
-------
Found 2026-10-01 before the D-85 post-freeze verification run. The candidate's
`artifact_manifest_ref` pointed at the live `artifacts/walking_skeleton/<fixture>/` listing,
and the comparison run rewrites that listing and its outputs before comparing, so every
output was compared against itself and the comparison could not fail. Separately, every
`exact` output was compared by whole-file SHA-256 although `schema` files (run log,
registry row, test report) carry their run id and durations by design, so a comparison
against a genuinely frozen reference could never pass. These tests are the negative
controls for both repairs, plus the reference snapshot the candidate now cites.

Inputs: the synthetic manifest apparatus of `tests/test_clean_run.py`. Re-run behaviour:
pure, `tmp_path` only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from src.data.config import IntegrityError
from src.data.fixture_manifest import (
    FixtureManifest,
    compare_required_outputs,
    load_fixture_manifest,
    snapshot_reference_outputs,
)
from src.data.release import sha256_of_file

from test_clean_run import (
    FROZEN,
    MANIFEST_NAME,
    PLUMBING_FIXTURE_ID,
    SIBLING_HASH_NAME,
    build_manifest_mapping,
    write_and_load,
)


def _copy_tree(manifest: FixtureManifest, produced: Path) -> None:
    for name in manifest.outputs:
        target = produced / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((manifest.artifact_manifest_path.parent / name).read_bytes())


def _frozen_with_documents(
    tmp_path: Path, documents: dict[str, tuple[str, Any]]
) -> FixtureManifest:
    root = tmp_path / "reference"
    root.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=FROZEN)
    listing = json.loads((root / "artifact_manifest.json").read_text(encoding="utf-8"))
    for name, (kind, document) in documents.items():
        (root / name).write_text(json.dumps(document, indent=2), encoding="utf-8")
        listing["outputs"][name] = sha256_of_file(root / name)
        data["required_outputs"]["comparison_ledger"][name]["exact_kind"] = kind
    (root / "artifact_manifest.json").write_text(
        json.dumps(listing, indent=2, sort_keys=True), encoding="utf-8"
    )
    manifest_path = root / MANIFEST_NAME
    manifest_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    (root / SIBLING_HASH_NAME).write_text(sha256_of_file(manifest_path) + "\n", encoding="utf-8")
    return load_fixture_manifest(manifest_path, parsed=data)


RUN_LOG = {
    "kind": "clean_run_log",
    "run_id": "walking-skeleton-plumbing_7day-A",
    "freeze_record_agreement": None,
    "commands": [["python", "a.py"], ["python", "b.py", "--phase", "1"]],
    "input_verification": {"files": {"records.csv": "a" * 64}},
}
CONFIG_SNAPSHOT = {
    "kind": "processing_config_snapshot",
    "config_hashes": {"data.yaml": "b" * 64, "seeds.yaml": "c" * 64},
    "snapshot_dir": "artifacts/registry/snapshots/run-A",
}


def test_reference_inside_the_produced_tree_is_refused(tmp_path):
    """The defect's negative control: comparing a tree against the listing it contains."""
    manifest = write_and_load(tmp_path, PLUMBING_FIXTURE_ID, status=FROZEN)
    with pytest.raises(IntegrityError, match="inside the produced tree"):
        compare_required_outputs(manifest, manifest.artifact_manifest_path.parent)
    with pytest.raises(IntegrityError, match="inside the produced tree"):
        compare_required_outputs(manifest, manifest.artifact_manifest_path.parent.parent)


def test_reference_changed_after_load_is_refused(tmp_path):
    manifest = write_and_load(tmp_path, PLUMBING_FIXTURE_ID, status=FROZEN)
    produced = tmp_path / "produced"
    _copy_tree(manifest, produced)
    target = manifest.artifact_manifest_path.parent / "split_manifest.json"
    target.write_text("rewritten after load", encoding="utf-8")
    with pytest.raises(IntegrityError, match="changed or vanished"):
        compare_required_outputs(manifest, produced)


def test_schema_kind_passes_on_run_specific_values_and_nullable_fields(tmp_path):
    manifest = _frozen_with_documents(tmp_path, {"clean_run_log.json": ("schema", RUN_LOG)})
    produced = tmp_path / "produced"
    _copy_tree(manifest, produced)
    other_run = json.loads(json.dumps(RUN_LOG))
    other_run["run_id"] = "walking-skeleton-plumbing_7day-B"
    other_run["freeze_record_agreement"] = {"agrees": True, "sha256": "d" * 64}
    (produced / "clean_run_log.json").write_text(json.dumps(other_run), encoding="utf-8")
    report = compare_required_outputs(manifest, produced)
    entry = report["outputs"]["clean_run_log.json"]
    assert entry["byte_equal"] is False and entry["schema_equal"] is True


@pytest.mark.parametrize(
    "mutate, match",
    [
        (lambda d: d.pop("input_verification"), "absent from the produced file"),
        (lambda d: d.__setitem__("extra", 1), "not in the frozen schema"),
        (lambda d: d.__setitem__("run_id", 7), "type number"),
        (lambda d: d.__setitem__("commands", [{"argv": "x"}]), "element"),
    ],
)
def test_schema_kind_refuses_a_structural_change(tmp_path, mutate, match):
    manifest = _frozen_with_documents(tmp_path, {"clean_run_log.json": ("schema", RUN_LOG)})
    produced = tmp_path / "produced"
    _copy_tree(manifest, produced)
    changed = json.loads(json.dumps(RUN_LOG))
    mutate(changed)
    (produced / "clean_run_log.json").write_text(json.dumps(changed), encoding="utf-8")
    with pytest.raises(IntegrityError, match=match):
        compare_required_outputs(manifest, produced)


def test_hash_kind_compares_every_recorded_sha256(tmp_path):
    manifest = _frozen_with_documents(
        tmp_path, {"processing_config_snapshot.yaml": ("hash", CONFIG_SNAPSHOT)}
    )
    produced = tmp_path / "produced"
    _copy_tree(manifest, produced)
    moved = dict(CONFIG_SNAPSHOT, snapshot_dir="artifacts/registry/snapshots/run-B")
    (produced / "processing_config_snapshot.yaml").write_text(json.dumps(moved), encoding="utf-8")
    report = compare_required_outputs(manifest, produced)
    assert report["outputs"]["processing_config_snapshot.yaml"]["sha256_leaves_equal"] == 2
    drifted = json.loads(json.dumps(moved))
    drifted["config_hashes"]["data.yaml"] = "e" * 64
    (produced / "processing_config_snapshot.yaml").write_text(json.dumps(drifted), encoding="utf-8")
    with pytest.raises(IntegrityError, match="recorded SHA-256"):
        compare_required_outputs(manifest, produced)


def test_byte_exact_kinds_stay_byte_exact(tmp_path):
    """`partition_membership` is never loosened to a schema comparison."""
    membership = {"partitions": {"F1": ["2022-11-01T00:00Z"]}}
    manifest = _frozen_with_documents(
        tmp_path, {"split_manifest.json": ("partition_membership", membership)}
    )
    produced = tmp_path / "produced"
    _copy_tree(manifest, produced)
    (produced / "split_manifest.json").write_text(
        json.dumps({"partitions": {"F1": ["2022-11-02T00:00Z"]}}), encoding="utf-8"
    )
    with pytest.raises(IntegrityError, match="partition_membership"):
        compare_required_outputs(manifest, produced)


def test_unreadable_semantic_pair_fails(tmp_path):
    manifest = _frozen_with_documents(tmp_path, {"clean_run_log.json": ("schema", RUN_LOG)})
    produced = tmp_path / "produced"
    _copy_tree(manifest, produced)
    (produced / "clean_run_log.json").write_text("{not json", encoding="utf-8")
    with pytest.raises(IntegrityError, match="cannot be read"):
        compare_required_outputs(manifest, produced)


def test_snapshot_copies_listing_and_compared_outputs_once(tmp_path):
    source = tmp_path / "run_root"
    source.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, source, status=FROZEN)
    ledger = data["required_outputs"]["comparison_ledger"]
    outputs = data["required_outputs"]["outputs"]
    plot = next(o for o in outputs if o.startswith("plots/"))
    ledger[plot] = {"comparison_class": "recorded_presence", "image_format": "png"}
    manifest_dir = tmp_path / "tests" / "fixtures" / PLUMBING_FIXTURE_ID
    destination = manifest_dir / "reference_run-A"
    ref = snapshot_reference_outputs(source, outputs, ledger, destination, manifest_dir=manifest_dir)
    assert ref == "reference_run-A/artifact_manifest.json"
    assert "\\" not in ref
    assert (destination / "artifact_manifest.json").read_bytes() == (
        source / "artifact_manifest.json"
    ).read_bytes()
    assert not (destination / plot).exists()
    for name in outputs:
        if name != plot:
            assert sha256_of_file(destination / name) == sha256_of_file(source / name)
    with pytest.raises(IntegrityError, match="written once"):
        snapshot_reference_outputs(source, outputs, ledger, destination, manifest_dir=manifest_dir)


def test_snapshot_refuses_and_leaves_nothing_when_an_output_is_missing(tmp_path):
    source = tmp_path / "run_root"
    source.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, source, status=FROZEN)
    outputs = data["required_outputs"]["outputs"]
    (source / "metrics.json").unlink()
    destination = tmp_path / "reference_run-A"
    with pytest.raises(IntegrityError, match="absent"):
        snapshot_reference_outputs(
            source, outputs, data["required_outputs"]["comparison_ledger"], destination,
            manifest_dir=tmp_path,
        )
    assert not destination.exists()


STAMP = {
    "evidence_class": "smoke_only",
    "fixture_id": PLUMBING_FIXTURE_ID,
    "frozen_manifest_hash": None,
    "phase_id": "P1A",
}


def _stamped(document: dict[str, Any], frozen_hash: str | None) -> dict[str, Any]:
    return {**document, "fixture_stamp": {**STAMP, "frozen_manifest_hash": frozen_hash}}


def test_stamp_set_aside_and_bound_to_the_frozen_manifest(tmp_path):
    """A measuring-run reference stamps null; a comparison run stamps the frozen hash."""
    membership = {"partitions": {"F1": ["2022-11-01T00:00Z"]}}
    manifest = _frozen_with_documents(
        tmp_path,
        {"split_manifest.json": ("partition_membership", _stamped(membership, None))},
    )
    produced = tmp_path / "produced"
    _copy_tree(manifest, produced)
    (produced / "split_manifest.json").write_text(
        json.dumps(_stamped(membership, manifest.sha256)), encoding="utf-8"
    )
    report = compare_required_outputs(manifest, produced)
    entry = report["outputs"]["split_manifest.json"]
    assert entry["stamp_bound_to_frozen_manifest"] is True and entry["values_equal"] is True


@pytest.mark.parametrize(
    "produced_doc, match",
    [
        (lambda h: _stamped({"partitions": {"F1": ["2022-11-01T00:00Z"]}}, "f" * 64), "not the frozen manifest"),
        (lambda h: {**_stamped({"partitions": {"F1": ["2022-11-01T00:00Z"]}}, h), "fixture_stamp": {**STAMP, "frozen_manifest_hash": h, "evidence_class": "scientific_fixture"}}, "evidence_class"),
        (lambda h: {"partitions": {"F1": ["2022-11-01T00:00Z"]}}, "one side only"),
        (lambda h: _stamped({"partitions": {"F1": ["2022-11-01T01:00Z"]}}, h), "content differs"),
    ],
)
def test_stamp_and_content_negative_controls(tmp_path, produced_doc, match):
    membership = {"partitions": {"F1": ["2022-11-01T00:00Z"]}}
    manifest = _frozen_with_documents(
        tmp_path,
        {"split_manifest.json": ("partition_membership", _stamped(membership, None))},
    )
    produced = tmp_path / "produced"
    _copy_tree(manifest, produced)
    (produced / "split_manifest.json").write_text(
        json.dumps(produced_doc(manifest.sha256)), encoding="utf-8"
    )
    with pytest.raises(IntegrityError, match=match):
        compare_required_outputs(manifest, produced)


def test_byte_exact_kind_float_must_match_bit_for_bit(tmp_path):
    checkpoint = {"entries": [{"epoch": 3, "restored_validation_rmse": 16.593359789183356}]}
    manifest = _frozen_with_documents(tmp_path, {"checkpoint_manifest.json": ("id", checkpoint)})
    produced = tmp_path / "produced"
    _copy_tree(manifest, produced)
    drifted = {"entries": [{"epoch": 3, "restored_validation_rmse": 16.59335993287129}]}
    (produced / "checkpoint_manifest.json").write_text(json.dumps(drifted), encoding="utf-8")
    with pytest.raises(IntegrityError, match="restored_validation_rmse"):
        compare_required_outputs(manifest, produced)
