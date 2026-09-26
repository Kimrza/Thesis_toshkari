"""D-75 (evidence/DECISIONS.md): the `recorded_presence` comparison class for
rendered plot outputs -- existence + readable-as-declared-format + recorded
SHA-256, never a pixel/hash comparison against a prior rendering. Direct unit
tests against `FixtureManifest`/`compare_required_outputs`/
`_validate_ledger_entry`, constructed by hand (not through the full candidate/
freeze machinery `test_clean_run.py` owns) to keep this test bounded to the
one new class."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT)) if str(REPO_ROOT) not in sys.path else None

from src.data.config import IntegrityError  # noqa: E402
from src.data.fixture_manifest import (  # noqa: E402
    RECORDED_PRESENCE_FORMATS,
    FixtureManifest,
    _validate_ledger_entry,
    compare_required_outputs,
)


def test_recorded_presence_is_a_valid_comparison_class() -> None:
    """A well-formed recorded_presence ledger entry passes validation."""
    entry = {
        "comparison_class": "recorded_presence",
        "units": "n/a (image)",
        "image_format": "png",
        "producing_path": {"script": "scripts/07_evaluate_and_report.py"},
    }
    _validate_ledger_entry("test", entry)  # must not raise


def test_recorded_presence_rejects_unknown_image_format() -> None:
    entry = {
        "comparison_class": "recorded_presence",
        "units": "n/a",
        "image_format": "bmp",  # not in RECORDED_PRESENCE_FORMATS
        "producing_path": {"script": "x"},
    }
    with pytest.raises(IntegrityError):
        _validate_ledger_entry("test", entry)


def test_recorded_presence_rejects_fp_tolerance_or_exact_kind() -> None:
    entry = {
        "comparison_class": "recorded_presence",
        "units": "n/a",
        "image_format": "png",
        "producing_path": {"script": "x"},
        "fp_tolerance": {"value": 1.0, "units": "x", "measuring_run_id": "x"},
    }
    with pytest.raises(IntegrityError):
        _validate_ledger_entry("test", entry)


def _build_manifest(tmp_path: Path, *, ledger_entry: dict) -> FixtureManifest:
    fixture_root = tmp_path / "fixture_root"
    fixture_root.mkdir()
    (fixture_root / "artifact_manifest.json").write_text(
        json.dumps({"fixture_id": "x", "outputs": {}}), encoding="utf-8"
    )
    return FixtureManifest(
        path=tmp_path / "fixture_manifest.yaml",
        fixture_id="x",
        status="frozen",
        sha256="0" * 64,
        data={
            "identity": {},
            "required_outputs": {
                "outputs": ["plots/target_support.png"],
                "comparison_ledger": {"plots/target_support.png": ledger_entry},
            },
        },
        artifact_manifest_path=fixture_root / "artifact_manifest.json",
        reference_files_present=(),
    )


def test_compare_required_outputs_accepts_a_real_png_regardless_of_prior_hash(
    tmp_path: Path,
) -> None:
    """The core D-75 behaviour: two DIFFERENT PNG byte sequences (simulating two
    different renderings across library versions) both pass -- because the
    class never compares against a prior hash, only existence + format."""
    ledger_entry = {
        "comparison_class": "recorded_presence",
        "units": "n/a",
        "image_format": "png",
        "producing_path": {"script": "x"},
    }
    manifest = _build_manifest(tmp_path, ledger_entry=ledger_entry)
    produced_root = tmp_path / "produced"
    (produced_root / "plots").mkdir(parents=True)

    png_magic = RECORDED_PRESENCE_FORMATS["png"]
    (produced_root / "plots" / "target_support.png").write_bytes(png_magic + b"AAAA rendering 1")
    result1 = compare_required_outputs(manifest, produced_root)
    hash1 = result1["outputs"]["plots/target_support.png"]["sha256"]

    (produced_root / "plots" / "target_support.png").write_bytes(png_magic + b"BBBB rendering 2 different bytes")
    result2 = compare_required_outputs(manifest, produced_root)
    hash2 = result2["outputs"]["plots/target_support.png"]["sha256"]

    assert hash1 != hash2  # genuinely different renderings
    assert result1["outputs"]["plots/target_support.png"]["matched"] is True
    assert result2["outputs"]["plots/target_support.png"]["matched"] is True


def test_compare_required_outputs_refuses_missing_plot(tmp_path: Path) -> None:
    ledger_entry = {
        "comparison_class": "recorded_presence",
        "units": "n/a",
        "image_format": "png",
        "producing_path": {"script": "x"},
    }
    manifest = _build_manifest(tmp_path, ledger_entry=ledger_entry)
    produced_root = tmp_path / "produced"
    produced_root.mkdir()
    with pytest.raises(IntegrityError, match="absent"):
        compare_required_outputs(manifest, produced_root)


def test_compare_required_outputs_refuses_corrupt_plot(tmp_path: Path) -> None:
    """A file present but not actually a PNG (wrong magic bytes) still fails --
    'recorded_presence' is not 'unconditionally present'."""
    ledger_entry = {
        "comparison_class": "recorded_presence",
        "units": "n/a",
        "image_format": "png",
        "producing_path": {"script": "x"},
    }
    manifest = _build_manifest(tmp_path, ledger_entry=ledger_entry)
    produced_root = tmp_path / "produced"
    (produced_root / "plots").mkdir(parents=True)
    (produced_root / "plots" / "target_support.png").write_bytes(b"not a png at all")
    with pytest.raises(IntegrityError, match="signature"):
        compare_required_outputs(manifest, produced_root)


def test_compare_required_outputs_refuses_empty_plot(tmp_path: Path) -> None:
    ledger_entry = {
        "comparison_class": "recorded_presence",
        "units": "n/a",
        "image_format": "png",
        "producing_path": {"script": "x"},
    }
    manifest = _build_manifest(tmp_path, ledger_entry=ledger_entry)
    produced_root = tmp_path / "produced"
    (produced_root / "plots").mkdir(parents=True)
    (produced_root / "plots" / "target_support.png").write_bytes(b"")
    with pytest.raises(IntegrityError):
        compare_required_outputs(manifest, produced_root)
