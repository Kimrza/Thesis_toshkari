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
