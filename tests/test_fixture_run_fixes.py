"""Two real bugs found by executing `run_walking_skeleton.py --emit-candidate`
against `plumbing_7day` for the first time in this state, 2026-09-26:

1. `src.data.prepared.load_released_provider_rows` only excluded its own
   output directory (`TARGET_RELEASE_DIR`) from the provider-input scan, not
   the four driver-release directories that share the same release root
   (D-61 option A) -- so once stage 04 had published driver releases, stage
   02 tried to read `hp60_ap60_1h.csv` as five-column provider VTEC and
   refused on the column mismatch. Correct refusal, wrong input offered.
2. `scripts/02_standardize_prepared_target.py` wrote the target CSV straight
   to its published path BEFORE checking whether a different release was
   already there under that citation -- so a refused write still silently
   overwrote a committed artifact on disk. Fixed with a write-to-temp,
   check, then place pattern; the published path is now provably untouched
   on a genuine version conflict.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT)) if str(REPO_ROOT) not in sys.path else None

from src.data.prepared import _non_provider_release_dirs, load_released_provider_rows  # noqa: E402


def test_non_provider_release_dirs_includes_all_four_driver_producers() -> None:
    """The exclusion set must name every D-63 driver identity, not just the
    stage's own output dir -- the exact gap that let a driver CSV reach the
    provider-column check."""
    from src.external.spaceweather import DRIVER_PRODUCERS

    excluded = _non_provider_release_dirs()
    assert "phase1_hourly_target" in excluded
    for driver_dir in DRIVER_PRODUCERS.values():
        assert driver_dir in excluded, f"{driver_dir} must be excluded from provider-row scanning"


def test_load_released_provider_rows_glob_never_yields_a_driver_directory(
    tmp_path: Path,
) -> None:
    """Direct proof against the real scan logic: seed a release root with only
    a driver-shaped release manifest (no provider release at all) and confirm
    the driver's manifest path is filtered out of the candidate list before
    any TE 13.3 verification runs -- so it can never reach the column check
    that used to fire on it. (A full valid-manifest provider release is
    exercised end-to-end by the real `--emit-candidate` run against the
    actual acquired bundle, not rebuilt by hand here.)"""
    release_root = tmp_path / "releases"
    driver_dir = release_root / "gfz_hp60ap60_v2_2022"
    driver_dir.mkdir(parents=True)
    (driver_dir / "release_manifest.json").write_text("{}", encoding="utf-8")

    with pytest.raises(Exception) as exc_info:
        load_released_provider_rows(release_root)
    # Must refuse with "no released provider input exists" (the driver
    # manifest was correctly excluded, leaving zero candidates) -- NOT with a
    # TE 13.3 verification failure against the driver manifest, which would
    # mean the exclusion did not fire.
    assert "no released provider input exists" in str(exc_info.value)


REPO_ROOT_STR = str(REPO_ROOT)
SCRIPT02 = REPO_ROOT / "scripts" / "02_standardize_prepared_target.py"


def test_write_order_never_touches_published_path_on_version_conflict() -> None:
    """Static proof, not just behavioural: the target CSV is written to a
    temp path and only `.replace()`d into the published path AFTER the
    manifest-hash decision, in `02_standardize_prepared_target.py`'s own
    source -- so a version-conflict refusal provably cannot have touched the
    published file. (An end-to-end reproduction needs a full stage-00/01
    pipeline run, which is exercised manually via
    `run_walking_skeleton.py --emit-candidate`, not as a fast unit test.)
    """
    source = SCRIPT02.read_text(encoding="utf-8")
    write_temp_idx = source.index("write_target_rows_csv(target_temp_path")
    version_conflict_idx = source.index("DIFFERENT Phase 1 hourly target is already published")
    replace_idx = source.index("target_temp_path.replace(target_final_path)")
    # The temp write and the conflict check both precede the ONLY place the
    # published path is ever written to (the rename/replace call).
    assert write_temp_idx < replace_idx
    assert version_conflict_idx < replace_idx
    # And the published final path is never opened for writing anywhere else
    # in this function -- `write_target_rows_csv` is called exactly once,
    # against the temp path, not the final path.
    assert source.count("write_target_rows_csv(target_temp_path") == 1
    assert "write_target_rows_csv(target_final_path" not in source
    assert "write_target_rows_csv(directory / target_path.name" not in source


def _write_valid_provider_release(directory: Path, *, row_marker: str) -> str:
    """A fully TE 13.3-valid, write_release-compatible release manifest (all
    fourteen required fields, correct content_hash/dataset_version
    derivation). `row_marker` varies the CSV content (and therefore the
    derived dataset_version) between calls; two calls with the SAME marker
    produce the SAME dataset_version, exactly like two identical stage-00
    re-runs. Returns the derived dataset_version."""
    from src.data.release import content_hash_of, dataset_version_for
    import hashlib

    directory.mkdir(parents=True, exist_ok=True)
    csv_body = f"station,ut1_unix,gdlat,glon,tec,dtec\nBSHM,1667260800,32,35,{row_marker},0.5\n"
    csv_path = directory / "rows.csv"
    csv_path.write_text(csv_body, encoding="utf-8")
    digest = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    payload = {
        "created_at_utc": "2026-09-26T00:00:00+00:00",
        "source_manifest_id": "test:source",
        "source_files": [
            {
                "provider": "test",
                "citation": "test",
                "location_date": "test",
                "filename": "rows.csv",
                "retrieval_date": "2026-09-26",
                "sha256": digest,
            }
        ],
        "processing": {
            "phase_id": "P1A",
            "target_definition_id": "test",
            "provider_experiment_kindat": "test",
            "parameters": ["tec"],
            "station_coordinate_to_cell_rule": "test",
            "selected_cell_bounds": {"test": "test"},
            "hourly_aggregation": "test",
        },
        "schema_version": "1",
        "units": {"tec": "TECU"},
        "row_counts": {
            "by_station": {"BSHM": 1},
            "by_month": {"2022-11": 1},
            "by_split": {"unsplit": 1},
            "by_qc_stage": {"raw": 1},
        },
        "exclusions_qc_summary": [{"reason": "test", "count": 0}],
        "fold_ids": ["NOT_YET_ASSIGNED"],
        "mask_ids": ["NOT_YET_ASSIGNED"],
        "feature_set_ids": ["NOT_YET_ASSIGNED"],
        "output_files": {"rows.csv": digest},
        "change_record_id": "test",
    }
    content_hash = content_hash_of(payload)
    dataset_version = dataset_version_for(content_hash)
    manifest = {**payload, "content_hash": content_hash, "dataset_version": dataset_version}
    (directory / "release_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return dataset_version


def test_load_released_provider_rows_dedupes_identical_dataset_version_duplicates(
    tmp_path: Path,
) -> None:
    """Real bug found 2026-09-26: repeated stage-00 runs create a new timestamped
    release directory per run even for byte-identical content; without dedup, N
    identical-content releases made every row get counted N times. Three release
    directories with IDENTICAL content (and therefore identical derived
    dataset_version, exactly like three re-runs of the same acquisition) must
    collapse to one."""
    release_root = tmp_path / "releases"
    versions = {
        _write_valid_provider_release(release_root / name, row_marker="7.0")
        for name in ("run_a", "run_b", "run_c")
    }
    assert len(versions) == 1, "test setup: all three must derive the same dataset_version"

    rows = load_released_provider_rows(release_root)
    assert len(rows) == 1, "three identical-content releases must collapse to one row set"


def test_load_released_provider_rows_refuses_genuinely_different_dataset_versions(
    tmp_path: Path,
) -> None:
    """Two releases with DIFFERENT content (and therefore different derived
    dataset_version) is real ambiguity -- must refuse by name, never guess or
    sum rows from two different releases."""
    release_root = tmp_path / "releases"
    v1 = _write_valid_provider_release(release_root / "run_a", row_marker="7.0")
    v2 = _write_valid_provider_release(release_root / "run_b", row_marker="9.0")
    assert v1 != v2, "test setup: different content must derive different dataset_version"

    with pytest.raises(Exception) as exc_info:
        load_released_provider_rows(release_root)
    assert "DIFFERENT dataset_version" in str(exc_info.value)


def test_load_released_provider_rows_skips_archived_release_dirs(tmp_path: Path) -> None:
    """A second real gap found alongside the first: an already-committed
    `<name>.archived-<commit>` directory (pre-dating this session,
    `phase1_hourly_target.archived-e535521/`) carries TARGET-shaped columns
    and must never be offered to the provider-column check either."""
    from src.data.prepared import _is_archived_release_dirname

    assert _is_archived_release_dirname("phase1_hourly_target.archived-e535521")
    assert not _is_archived_release_dirname("gfz_hp60ap60_v2_2022")
    assert not _is_archived_release_dirname("phase1_hourly_target")

    release_root = tmp_path / "releases"
    archived_dir = release_root / "phase1_hourly_target.archived-e535521"
    archived_dir.mkdir(parents=True)
    (archived_dir / "release_manifest.json").write_text("{}", encoding="utf-8")

    with pytest.raises(Exception) as exc_info:
        load_released_provider_rows(release_root)
    assert "no released provider input exists" in str(exc_info.value)


def test_gim_comparator_release_is_excluded_and_matches_stage_04_name(tmp_path: Path) -> None:
    """Third gap, found 2026-10-01 re-measuring plumbing_7day (D-83 item 12): stage 04
    publishes the CODE GIM comparator release into the shared root, and a live provider
    release beside it refused on two dataset_versions. The comparator must be excluded,
    and the excluded name must equal the name stage 04 actually writes."""
    import re

    from src.data.prepared import GIM_COMPARATOR_RELEASE_DIR

    stage04 = (REPO_ROOT / "scripts" / "04_build_external_products.py").read_text(
        encoding="utf-8"
    )
    produced = re.search(r'_GIM_COMPARATOR_ARTIFACT: Final\[str\] = "([^"]+)"', stage04)
    assert produced is not None
    assert produced.group(1) == GIM_COMPARATOR_RELEASE_DIR
    assert GIM_COMPARATOR_RELEASE_DIR in _non_provider_release_dirs()

    release_root = tmp_path / "releases"
    version = _write_valid_provider_release(release_root / "run_a", row_marker="7.0")
    other = _write_valid_provider_release(
        release_root / GIM_COMPARATOR_RELEASE_DIR, row_marker="9.0"
    )
    assert version != other, "test setup: the comparator must carry a different version"
    rows = load_released_provider_rows(release_root)
    assert len(rows) == 1, "only the provider release may be read"


def test_unknown_non_provider_release_still_refuses_as_ambiguous(tmp_path: Path) -> None:
    """Negative control: the exclusion is by exact name only. A differently-named second
    release with another dataset_version is still genuine ambiguity and refuses."""
    release_root = tmp_path / "releases"
    _write_valid_provider_release(release_root / "run_a", row_marker="7.0")
    _write_valid_provider_release(release_root / "gim_comparator_other", row_marker="9.0")
    with pytest.raises(Exception) as exc_info:
        load_released_provider_rows(release_root)
    assert "DIFFERENT dataset_version" in str(exc_info.value)


def _stage02():
    import importlib.util

    spec = importlib.util.spec_from_file_location("stage02_under_test", SCRIPT02)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_PROVIDER_PROCESSING = {"parameters": ["ut1_unix", "gdlat", "glon", "tec", "dtec"],
                        "hourly_aggregation": "median"}
_DRIVER_PROCESSING = {"parameters": ["ap60", "hp60"],
                      "hourly_aggregation": "none: values are released at the provider's own cadence"}


def test_target_processing_is_the_providers_even_when_a_driver_sorts_first() -> None:
    """2026-10-01 defect: `consumed[0]` was a driver release (sorts before
    `plumbing_7day_*`), so the VTEC target carried the driver's processing block."""
    mod = _stage02()
    consumed = [
        (Path("releases/gfz_hp60ap60_v2_2022/release_manifest.json"),
         {"output_files": {"hp60_ap60_1h.csv": "x"}, "processing": _DRIVER_PROCESSING}),
        (Path("releases/plumbing_7day_20261001T000000Z/release_manifest.json"),
         {"output_files": {"prepared_vtec_records.csv": "y"}, "processing": _PROVIDER_PROCESSING}),
    ]
    assert mod._provider_processing(consumed) == _PROVIDER_PROCESSING


def test_target_processing_refuses_without_a_provider_release() -> None:
    mod = _stage02()
    consumed = [(Path("releases/gfz/release_manifest.json"),
                 {"output_files": {"hp60_ap60_1h.csv": "x"}, "processing": _DRIVER_PROCESSING})]
    with pytest.raises(Exception, match="PROVIDER release"):
        mod._provider_processing(consumed)


def test_target_processing_refuses_disagreeing_provider_releases() -> None:
    mod = _stage02()
    other = {**_PROVIDER_PROCESSING, "hourly_aggregation": "mean"}
    consumed = [
        (Path("a/release_manifest.json"),
         {"output_files": {"prepared_vtec_records.csv": "y"}, "processing": _PROVIDER_PROCESSING}),
        (Path("b/release_manifest.json"),
         {"output_files": {"prepared_vtec_records.csv": "z"}, "processing": other}),
    ]
    with pytest.raises(Exception, match="disagree"):
        mod._provider_processing(consumed)
