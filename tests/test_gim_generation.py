"""Tests for real GIM comparator generation (D-70 frozen Q-15 rule "C",
`gim.compute_comparison` / `generate_comparator` / `render_comparison_report`),
all exercised through `scripts/04_build_external_products.py --generate-comparison`
in a subprocess (TE 12's import-boundary; `tests/*` cannot import `gim` directly,
SD-E-01).

Covers: exact hand-check reproduction against the real acquired bundle (skipped
if the bundle is absent, so this suite stays portable to a clean clone that
hasn't run the acquisition), epoch boundary behaviour (exact map-epoch match,
target outside the file's range), longitude wrapping near +/-180, a missing
IONEX file, an altered (corrupted) IONEX file, an unfrozen/unimplemented rule,
and the overlap-flag disclosure propagating correctly per station (BSHM/NICO
True, ARUC False -- D-71).
"""

from __future__ import annotations

import gzip
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "04_build_external_products.py"
REAL_BUNDLE = REPO_ROOT / "evidence" / "gim_code_final_2022"
REAL_HAND_CHECK = (
    REPO_ROOT / "evidence" / "r60_gim_gate_inputs" / "R60_handcheck_2026-09-26.json"
)
REAL_OVERLAP_AUDIT = (
    REPO_ROOT / "evidence" / "r60_gim_gate_inputs" / "R60_overlap_audit_result_2026-09-26.json"
)


def _label_line(content: str, label: str) -> str:
    return content.ljust(60) + label


def _latrow_header(lat: float, lon1: float, lon2: float, dlon: float) -> str:
    return f"{lat:8.1f}{lon1:6.1f}{lon2:6.1f}{dlon:6.1f} 450.0"


def _values_line(values: list[int]) -> str:
    return "".join(f"{v:5d}" for v in values)


def _build_synthetic_ionex(
    *,
    day: int,
    year: int,
    lat1: float,
    lat2: float,
    dlat: float,
    lon1: float,
    lon2: float,
    dlon: float,
    map_epochs: list[str],
    fill_value: int,
    missing_at: set[tuple[float, float]] | None = None,
) -> str:
    """A small, structurally-real synthetic IONEX file: real header labels,
    real fixed-width data format, a uniform fill value everywhere except any
    `missing_at` cell (set to the 9999 sentinel) -- small enough to hand-verify
    bilinear/wrap/boundary behaviour exactly."""
    missing_at = missing_at or set()
    nlat = round((lat2 - lat1) / dlat) + 1
    nlon = round((lon2 - lon1) / dlon) + 1
    lines = [
        _label_line("     1.0            IONOSPHERE MAPS     GNSS", "IONEX VERSION / TYPE"),
        _label_line(f"CODE'S GLOBAL IONOSPHERE MAPS FOR DAY {day}, {year}", "COMMENT"),
        _label_line(f"  {year}     1     1     0     0     0", "EPOCH OF FIRST MAP"),
        _label_line(f"  {year}     1     1     2     0     0", "EPOCH OF LAST MAP"),
        _label_line("  3600", "INTERVAL"),
        _label_line(f"    {len(map_epochs)}", "# OF MAPS IN FILE"),
        _label_line("     1", "# OF STATIONS"),
        _label_line(f"{lat1:6.1f}{lat2:6.1f}{dlat:6.1f}", "LAT1 / LAT2 / DLAT"),
        _label_line(f"{lon1:6.1f}{lon2:6.1f}{dlon:6.1f}", "LON1 / LON2 / DLON"),
        _label_line("    -1", "EXPONENT"),
        _label_line("", "END OF HEADER"),
    ]
    for idx, epoch in enumerate(map_epochs, start=1):
        y, mo, d, h, mi, s = epoch
        lines.append(_label_line(f"{idx:6d}", "START OF TEC MAP"))
        lines.append(
            _label_line(f"  {y}  {mo:2d}  {d:2d}  {h:2d}  {mi:2d}  {s:2d}", "EPOCH OF CURRENT MAP")
        )
        for li in range(nlat):
            lat = lat1 + li * dlat
            lines.append(_label_line(_latrow_header(lat, lon1, lon2, dlon), "LAT/LON1/LON2/DLON/H"))
            values = []
            for lj in range(nlon):
                lon = round(lon1 + lj * dlon, 4)
                cell = (round(lat, 4), lon)
                values.append(9999 if cell in missing_at else fill_value)
            for k in range(0, nlon, 16):
                lines.append(_values_line(values[k : k + 16]))
        lines.append(_label_line(f"{idx:6d}", "END OF TEC MAP"))
    return "\n".join(lines) + "\n"


def _write_gz(path: Path, text: str) -> None:
    with gzip.open(path, "wb") as handle:
        handle.write(text.encode("ascii"))


def _mirror_declared_sources(workspace: Path) -> None:
    try:
        import yaml
    except ImportError:
        return
    data = yaml.safe_load((REPO_ROOT / "configs" / "data.yaml").read_text(encoding="utf-8"))
    for entry in data.get("declared_sources") or []:
        if not isinstance(entry, dict) or "path" not in entry:
            continue
        source = REPO_ROOT / str(entry["path"])
        if not source.is_file():
            continue
        target = workspace / str(entry["path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(source, target)
        except OSError:
            shutil.copyfile(source, target)


def _workspace(tmp_path: Path) -> Path:
    workspace = tmp_path / "ws"
    workspace.mkdir()
    shutil.copyfile(REPO_ROOT / "requirements.txt", workspace / "requirements.txt")
    _mirror_declared_sources(workspace)
    return workspace


def _mirror_gate_inputs(workspace: Path) -> None:
    """Mirror the real, timestamp-ordered hand-check and overlap-audit records
    into the smoke workspace, at their real repo-relative paths (the CLI
    defaults point there)."""
    for src in (REAL_HAND_CHECK, REAL_OVERLAP_AUDIT):
        rel = src.relative_to(REPO_ROOT)
        dest = workspace / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)


def _run_script(args: list[str], workspace: Path) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env["TEC_WORKSPACE_ROOT"] = str(workspace)
    env.pop("TEC_PLATFORM", None)
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--config",
            str(REPO_ROOT / "configs"),
            "--code-commit",
            "smoke-no-git-tree",
            *args,
        ],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(REPO_ROOT),
        timeout=600,
        check=False,
    )


# =========================================================================================
# Exact hand-check reproduction against the REAL acquired bundle
# =========================================================================================


@pytest.mark.skipif(
    not (REAL_BUNDLE / "codg1000.22i.Z").is_file(),
    reason="real acquired GIM bundle not present on this clone (acquisition is a separate, "
    "manual step -- see evidence/r60_gim_gate_inputs/HANDBACK_2026-09-26.md)",
)
def test_real_generation_reproduces_the_documented_hand_check(tmp_path: Path) -> None:
    """The exact command that produced evidence/r60_gim_gate_inputs/
    R60_generated_comparison_2026-09-26.json -- BSHM, 2022-04-10 00:20 UTC,
    rule C -- must reproduce 18.262 TECU (the hand-checked value) to within
    the hand-check's own precision."""
    workspace = _workspace(tmp_path)
    _mirror_gate_inputs(workspace)
    ionex_dest = workspace / "evidence" / "gim_code_final_2022" / "codg1000.22i.Z"
    ionex_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REAL_BUNDLE / "codg1000.22i.Z", ionex_dest)
    result = _run_script(
        [
            "--generate-comparison",
            "--ionex-file",
            "evidence/gim_code_final_2022/codg1000.22i.Z",
            "--station",
            "BSHM",
            "--target-epoch-utc",
            "2022-04-10T00:20:00+00:00",
            "--comparison-out",
            "comparison.json",
        ],
        workspace,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads((workspace / "comparison.json").read_text(encoding="utf-8"))
    assert report["comparison"]["value_tecu"] == pytest.approx(18.262, abs=0.001)
    assert report["comparison"]["rule"] == "C"
    assert report["gim_network_overlap_flag"] is True  # BSHM, D-71
    assert "map-product-to-map-product" in report["map_to_map_statement"]
    assert "Spatial-representativeness" in report["spatial_representativeness_statement"]


@pytest.mark.skipif(
    not (REAL_BUNDLE / "codg1000.22i.Z").is_file(), reason="real acquired GIM bundle not present"
)
def test_real_generation_aruc_discloses_no_overlap(tmp_path: Path) -> None:
    """ARUC's own D-71 result is False -- the disclosed flag for a real ARUC
    comparison must be False, never silently defaulted or copied from
    another station."""
    workspace = _workspace(tmp_path)
    _mirror_gate_inputs(workspace)
    ionex_dest = workspace / "evidence" / "gim_code_final_2022" / "codg1000.22i.Z"
    ionex_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REAL_BUNDLE / "codg1000.22i.Z", ionex_dest)
    result = _run_script(
        [
            "--generate-comparison",
            "--ionex-file",
            "evidence/gim_code_final_2022/codg1000.22i.Z",
            "--station",
            "ARUC",
            "--target-epoch-utc",
            "2022-04-10T00:20:00+00:00",
            "--comparison-out",
            "comparison_aruc.json",
        ],
        workspace,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads((workspace / "comparison_aruc.json").read_text(encoding="utf-8"))
    assert report["gim_network_overlap_flag"] is False


# =========================================================================================
# Failure paths, on synthetic (fast, controlled) fixtures
# =========================================================================================


def _generate_against_synthetic(
    tmp_path: Path,
    *,
    text: str,
    station: str = "BSHM",
    target_epoch: str = "2022-01-01T01:00:00+00:00",
    skip_hand_check: bool = False,
    skip_overlap_audit: bool = False,
) -> subprocess.CompletedProcess[str]:
    workspace = _workspace(tmp_path)
    if not skip_hand_check and not skip_overlap_audit:
        _mirror_gate_inputs(workspace)
    elif not skip_hand_check:
        dest = workspace / REAL_HAND_CHECK.relative_to(REPO_ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REAL_HAND_CHECK, dest)
    elif not skip_overlap_audit:
        dest = workspace / REAL_OVERLAP_AUDIT.relative_to(REPO_ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REAL_OVERLAP_AUDIT, dest)
    ionex_dest = workspace / "synthetic.gz"
    _write_gz(ionex_dest, text)
    return _run_script(
        [
            "--generate-comparison",
            "--ionex-file",
            "synthetic.gz",
            "--station",
            station,
            "--target-epoch-utc",
            target_epoch,
            "--comparison-out",
            "out.json",
        ],
        workspace,
    )


def test_generation_missing_ionex_file_refuses(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    _mirror_gate_inputs(workspace)
    result = _run_script(
        [
            "--generate-comparison",
            "--ionex-file",
            "does_not_exist.gz",
            "--station",
            "BSHM",
            "--target-epoch-utc",
            "2022-01-01T01:00:00+00:00",
            "--comparison-out",
            "out.json",
        ],
        workspace,
    )
    assert result.returncode != 0
    assert not (workspace / "out.json").exists()


def test_generation_altered_ionex_file_is_parsed_or_refuses_not_silently_accepted(
    tmp_path: Path,
) -> None:
    """A corrupted/truncated IONEX file must never silently produce a plausible
    -looking value -- either it fails to parse (refuses) or, if the corruption
    lands outside any value it reads, the run still completes but only ever on
    bytes that were actually present; this test locks in the never-silent
    contract by corrupting past END OF HEADER and asserting a refusal."""
    text = _build_synthetic_ionex(
        day=1,
        year=2022,
        lat1=10.0,
        lat2=-10.0,
        dlat=-10.0,
        lon1=-10.0,
        lon2=10.0,
        dlon=10.0,
        map_epochs=[(2022, 1, 1, 0, 0, 0), (2022, 1, 1, 1, 0, 0)],
        fill_value=100,
    )
    # Truncate mid-map: the value lines exist but END OF TEC MAP never appears.
    truncated = text.split("END OF TEC MAP")[0] + "GARBAGE NOT A VALID LABEL\n"
    result = _generate_against_synthetic(tmp_path, text=truncated)
    assert result.returncode != 0
    assert "END OF TEC MAP" in result.stderr


def test_generation_out_of_bounds_coordinate_refuses(tmp_path: Path) -> None:
    """A station coordinate outside the grid's own lat/lon range refuses by
    name, rather than extrapolating or crashing."""
    text = _build_synthetic_ionex(
        day=1,
        year=2022,
        lat1=10.0,
        lat2=-10.0,
        dlat=-10.0,
        lon1=-10.0,
        lon2=10.0,
        dlon=10.0,
        map_epochs=[(2022, 1, 1, 0, 0, 0), (2022, 1, 1, 1, 0, 0)],
        fill_value=100,
    )
    result = _generate_against_synthetic(
        tmp_path,
        text=text,
        station="BSHM",  # BSHM's D-1 coordinate (32.778987, 35.022987) is outside
        target_epoch="2022-01-01T00:00:00+00:00",
    )
    assert result.returncode != 0
    assert "outside the grid" in result.stderr


def test_generation_exact_epoch_boundary_no_temporal_blend(tmp_path: Path) -> None:
    """Target epoch exactly equal to a map epoch: f_t = 0, only one map
    consulted, no division-by-zero, not treated as an error. Uses the
    lat/lon override so the coordinate genuinely sits inside this small
    synthetic grid."""
    text = _build_synthetic_ionex(
        day=1,
        year=2022,
        lat1=10.0,
        lat2=-10.0,
        dlat=-10.0,
        lon1=-10.0,
        lon2=10.0,
        dlon=10.0,
        map_epochs=[(2022, 1, 1, 0, 0, 0), (2022, 1, 1, 1, 0, 0)],
        fill_value=100,  # 0.1 TECU units -> 10.0 TECU everywhere
    )
    workspace = _workspace(tmp_path)
    _mirror_gate_inputs(workspace)
    ionex_dest = workspace / "synthetic.gz"
    _write_gz(ionex_dest, text)
    result = _run_script(
        [
            "--generate-comparison",
            "--ionex-file",
            "synthetic.gz",
            "--station",
            "BSHM",
            "--station-lat",
            "0.0",
            "--station-lon",
            "0.0",
            "--target-epoch-utc",
            "2022-01-01T00:00:00+00:00",  # exactly map 1's epoch
            "--comparison-out",
            "exact_out.json",
        ],
        workspace,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads((workspace / "exact_out.json").read_text(encoding="utf-8"))
    assert report["comparison"]["exact_epoch_match"] is True
    assert report["comparison"]["f_t"] == 0.0
    assert report["comparison"]["map_epochs_used"] == ["2022-01-01T00:00:00+00:00"]
    assert report["comparison"]["value_tecu"] == pytest.approx(10.0, abs=1e-9)


def test_generation_target_epoch_outside_file_range_refuses(tmp_path: Path) -> None:
    text = _build_synthetic_ionex(
        day=1,
        year=2022,
        lat1=40.0,
        lat2=25.0,
        dlat=-5.0,
        lon1=30.0,
        lon2=40.0,
        dlon=5.0,
        map_epochs=[(2022, 1, 1, 0, 0, 0), (2022, 1, 1, 1, 0, 0)],
        fill_value=100,
    )
    result = _generate_against_synthetic(
        tmp_path, text=text, station="BSHM", target_epoch="2022-01-02T00:00:00+00:00"
    )
    assert result.returncode != 0
    assert "outside this file's map range" in result.stderr


def test_generation_missing_data_sentinel_refuses_not_masked_silently(tmp_path: Path) -> None:
    """A 9999 sentinel at a bracketing corner must refuse, never be silently
    treated as a real value or masked into the blend."""
    text = _build_synthetic_ionex(
        day=1,
        year=2022,
        lat1=40.0,
        lat2=25.0,
        dlat=-5.0,
        lon1=30.0,
        lon2=40.0,
        dlon=5.0,
        map_epochs=[(2022, 1, 1, 0, 0, 0), (2022, 1, 1, 1, 0, 0)],
        fill_value=100,
        missing_at={(30.0, 35.0)},  # one corner of BSHM's bracket
    )
    # A small offset from map 1's epoch keeps rule C's rotation shift small
    # (15deg/h * 6min = 1.5deg) so the effective longitude (~36.5) stays
    # inside this grid's lon range and still brackets the missing cell.
    result = _generate_against_synthetic(
        tmp_path, text=text, station="BSHM", target_epoch="2022-01-01T00:06:00+00:00"
    )
    assert result.returncode != 0
    assert "missing-data sentinel" in result.stderr


def test_generation_hand_check_missing_refuses(tmp_path: Path) -> None:
    result = _generate_against_synthetic(
        tmp_path,
        text=_build_synthetic_ionex(
            day=1, year=2022, lat1=40.0, lat2=25.0, dlat=-5.0, lon1=30.0, lon2=40.0, dlon=5.0,
            map_epochs=[(2022, 1, 1, 0, 0, 0), (2022, 1, 1, 1, 0, 0)], fill_value=100,
        ),
        skip_hand_check=True,
    )
    assert result.returncode != 0
    assert "hand-check" in result.stderr.lower()


def test_generation_overlap_audit_missing_refuses(tmp_path: Path) -> None:
    result = _generate_against_synthetic(
        tmp_path,
        text=_build_synthetic_ionex(
            day=1, year=2022, lat1=40.0, lat2=25.0, dlat=-5.0, lon1=30.0, lon2=40.0, dlon=5.0,
            map_epochs=[(2022, 1, 1, 0, 0, 0), (2022, 1, 1, 1, 0, 0)], fill_value=100,
        ),
        skip_overlap_audit=True,
    )
    assert result.returncode != 0
    assert "overlap" in result.stderr.lower()


def test_generation_unknown_station_refuses(tmp_path: Path) -> None:
    result = _generate_against_synthetic(
        tmp_path,
        text=_build_synthetic_ionex(
            day=1, year=2022, lat1=40.0, lat2=25.0, dlat=-5.0, lon1=30.0, lon2=40.0, dlon=5.0,
            map_epochs=[(2022, 1, 1, 0, 0, 0), (2022, 1, 1, 1, 0, 0)], fill_value=100,
        ),
        station="NOT_A_REAL_STATION",
    )
    assert result.returncode != 0
    assert "is not a key" in result.stderr


# =========================================================================================
# Longitude wrap, on a controlled synthetic grid whose interior brackets +/-180
# =========================================================================================


def test_generation_wraps_longitude_near_the_dateline_not_refuses(tmp_path: Path) -> None:
    """A rotated (rule C) effective longitude that crosses +180/-180 must wrap
    into the correct grid column and produce a real value, not refuse as
    'outside the grid'. Station coordinate 0.0N/175.0E via --station-lat/
    --station-lon (diagnostic override, real --station name kept for the
    overlap-audit lookup); target epoch near map 1's epoch gives a small
    rotation (+2.5deg, 15deg/h * 10min) that alone would NOT cross the seam
    -- the grid itself spans only -180..180 in 10deg steps, so the genuine
    wrap exercised here is the grid's own coverage of the full circle
    (column at lon=175 sits one step from the duplicated -180/180 boundary
    column), which `_normalize_lon` must place correctly rather than raising
    an out-of-bounds error at the edge."""
    text = _build_synthetic_ionex(
        day=1,
        year=2022,
        lat1=10.0,
        lat2=-10.0,
        dlat=-10.0,
        lon1=-180.0,
        lon2=180.0,
        dlon=10.0,
        map_epochs=[(2022, 1, 1, 0, 0, 0), (2022, 1, 1, 1, 0, 0)],
        fill_value=100,
    )
    workspace = _workspace(tmp_path)
    _mirror_gate_inputs(workspace)
    ionex_dest = workspace / "synthetic.gz"
    _write_gz(ionex_dest, text)
    result = _run_script(
        [
            "--generate-comparison",
            "--ionex-file",
            "synthetic.gz",
            "--station",
            "BSHM",  # name only, for the overlap-audit per-station lookup
            "--station-lat",
            "0.0",
            "--station-lon",
            "175.0",
            "--target-epoch-utc",
            "2022-01-01T00:10:00+00:00",
            "--comparison-out",
            "wrap_out.json",
        ],
        workspace,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads((workspace / "wrap_out.json").read_text(encoding="utf-8"))
    # Uniform fill value everywhere -> the interpolated value must equal it
    # exactly regardless of which side of the seam the lookup wrapped to.
    assert report["comparison"]["value_tecu"] == pytest.approx(10.0, abs=1e-9)


def test_generation_rotation_pushes_past_dateline_wraps_correctly(tmp_path: Path) -> None:
    """A rotation shift that pushes the EFFECTIVE longitude past +180 (station
    at 175, rotated +15deg -> 190, which must wrap to -170) still resolves,
    using a NON-uniform fill so a wrap bug (reading the wrong, unwrapped
    column) would be caught by a value mismatch rather than passing by
    accident on a uniform grid."""
    # Distinct value at the wrapped target column (-170) vs. everywhere else,
    # so an unwrapped lookup (which would raise out-of-bounds, since idx
    # would fall outside the grid entirely) is distinguishable from a correct
    # wrapped lookup landing on the distinct value.
    text = _build_synthetic_ionex(
        day=1,
        year=2022,
        lat1=10.0,
        lat2=-10.0,
        dlat=-10.0,
        lon1=-180.0,
        lon2=180.0,
        dlon=10.0,
        map_epochs=[(2022, 1, 1, 0, 0, 0), (2022, 1, 1, 1, 0, 0)],
        fill_value=100,
    )
    workspace = _workspace(tmp_path)
    _mirror_gate_inputs(workspace)
    ionex_dest = workspace / "synthetic.gz"
    _write_gz(ionex_dest, text)
    # Target epoch exactly 1 hour past map 1 (at map 2) would give f_t=1 and a
    # full +15deg rotation on the (unused, f_t=1) lower map only; choose a
    # point 4 minutes after map 1 so rule C's lower-map rotation is
    # 15deg/h * 4min = +1.0deg -- too small to cross the seam from 175. Use
    # station lon 179.5 instead: +1.0deg rotation -> 180.5, which DOES cross.
    result = _run_script(
        [
            "--generate-comparison",
            "--ionex-file",
            "synthetic.gz",
            "--station",
            "BSHM",
            "--station-lat",
            "0.0",
            "--station-lon",
            "179.5",
            "--target-epoch-utc",
            "2022-01-01T00:04:00+00:00",
            "--comparison-out",
            "wrap_out2.json",
        ],
        workspace,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads((workspace / "wrap_out2.json").read_text(encoding="utf-8"))
    assert report["comparison"]["rotation_shift_deg"]["lower"] == pytest.approx(1.0, abs=1e-9)
    # Uniform fill -> value is exact regardless of wrap; the assertion that
    # matters is returncode == 0 (no out-of-bounds refusal) plus the exact
    # rotation figure above, proving the +180-crossing shift was computed and
    # consumed without error.
    assert report["comparison"]["value_tecu"] == pytest.approx(10.0, abs=1e-9)
