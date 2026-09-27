"""Tests for `gim.py`'s provenance/validation extensions (IONEX header parse,
bundle hash+structural verification, overlap-audit computation), all exercised
through `scripts/04_build_external_products.py` in a subprocess, because that
script and `src/evaluation/` are the only allowlisted importers of
`src.external.gim` (TE 12; `tests/test_iri_denial.py`'s import-boundary scan
withdrew the previous `tests/*` grant, SD-E-01) -- a test importing `gim`
directly would itself be the violation these tests exist to avoid introducing.

Covers: hash-mismatch refusal, day/year mismatch refusal, grid-geometry
mismatch refusal, a passing bundle-verification round-trip, and the
overlap-audit's real presence/absence result on a small synthetic network
list (real ARUC/BSHM/NICO codes from `configs/data.yaml`, never invented).
"""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "04_build_external_products.py"


def _label_line(content: str, label: str) -> str:
    """One fixed-width IONEX header line: content left-justified to column 60,
    label starting at column 61 (0-indexed 60) -- the same convention
    `gim.py`'s `_ionex_label` reads."""
    return content.ljust(60) + label


def _minimal_ionex_header(*, day: int, year: int, lat1: float = 87.5) -> str:
    """A minimal-but-complete synthetic IONEX header: every field
    `parse_ionex_header` requires, values drawn from the real acquired
    `codg1000.22i.Z` file's own header (2026-09-26 acquisition) except where a
    test deliberately perturbs one field."""
    lines = [
        _label_line("     1.0            IONOSPHERE MAPS     GNSS", "IONEX VERSION / TYPE"),
        _label_line(
            f"CODE'S GLOBAL IONOSPHERE MAPS FOR DAY {day}, {year}", "COMMENT"
        ),
        _label_line("List of stations:", "COMMENT"),
        _label_line("aruc bshm nico", "COMMENT"),
        _label_line(f"  {year}     4    10     0     0     0", "EPOCH OF FIRST MAP"),
        _label_line(f"  {year}     4    11     0     0     0", "EPOCH OF LAST MAP"),
        _label_line("  3600", "INTERVAL"),
        _label_line("    25", "# OF MAPS IN FILE"),
        _label_line("   226", "# OF STATIONS"),
        _label_line(f"    {lat1} -87.5  -2.5", "LAT1 / LAT2 / DLAT"),
        _label_line("  -180.0 180.0   5.0", "LON1 / LON2 / DLON"),
        _label_line("    -1", "EXPONENT"),
        _label_line("", "END OF HEADER"),
    ]
    return "\n".join(lines) + "\n"


def _write_gz(path: Path, text: str) -> None:
    with gzip.open(path, "wb") as handle:
        handle.write(text.encode("ascii"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_script(args: list[str], workspace: Path) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env["TEC_WORKSPACE_ROOT"] = str(workspace)
    env.pop("TEC_PLATFORM", None)
    # R3 (GOV-2026-09-27-BT-02): CI markers now refuse; these subprocess tests
    # exercise marker-free default resolution deliberately.
    env.pop("GITHUB_ACTIONS", None)
    env.pop("CI", None)
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


def _mirror_declared_sources(workspace: Path) -> None:
    """Same purpose as `test_external_drivers.py`'s helper of the same name: make
    every `configs/data.yaml: declared_sources` path resolve inside the smoke
    workspace so the preflight's `assert_declared_sources_exist` step passes on
    the same bytes the real workspace has, rather than failing on an absent-
    source refusal unrelated to what this test file actually checks."""
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


@pytest.fixture()
def bundle_dir(tmp_path: Path) -> Path:
    """A tiny, valid, two-file synthetic bundle: day 100 and day 101, 2022,
    real filename patterns (long-form, matching the acquired bundle's late-
    2022 files), correct manifest."""
    d = tmp_path / "gim_bundle"
    d.mkdir()
    files = {
        "COD0OPSFIN_20221000000_01D_01H_GIM.INX.gz": _minimal_ionex_header(day=100, year=2022),
        "COD0OPSFIN_20221010000_01D_01H_GIM.INX.gz": _minimal_ionex_header(day=101, year=2022),
    }
    manifest: dict[str, str] = {}
    for name, text in files.items():
        path = d / name
        _write_gz(path, text)
        manifest[name] = _sha256(path)
    (d / "sha256_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return d


def test_verify_gim_bundle_passes_on_valid_bundle(tmp_path: Path, bundle_dir: Path) -> None:
    workspace = _workspace(tmp_path)
    result = _run_script(
        [
            "--verify-gim-bundle",
            str(bundle_dir),
            "--gim-bundle-out",
            "gim_bundle_report.json",
        ],
        workspace,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads((workspace / "gim_bundle_report.json").read_text(encoding="utf-8"))
    assert report["files_checked"] == 2


def test_verify_gim_bundle_refuses_on_hash_mismatch(tmp_path: Path, bundle_dir: Path) -> None:
    # Corrupt one file's bytes after the manifest was written.
    target = bundle_dir / "COD0OPSFIN_20221000000_01D_01H_GIM.INX.gz"
    target.write_bytes(target.read_bytes() + b"\x00")
    workspace = _workspace(tmp_path)
    result = _run_script(["--verify-gim-bundle", str(bundle_dir)], workspace)
    assert result.returncode != 0
    assert "hash mismatch" in result.stderr


def test_verify_gim_bundle_refuses_on_day_year_mismatch(tmp_path: Path) -> None:
    """A file whose own header claims a different day than its filename
    encodes -- a real failure mode if a provider serves a stale/wrong day."""
    d = tmp_path / "bad_bundle"
    d.mkdir()
    # Filename says day 100; header (deliberately) claims day 99.
    name = "COD0OPSFIN_20221000000_01D_01H_GIM.INX.gz"
    path = d / name
    _write_gz(path, _minimal_ionex_header(day=99, year=2022))
    (d / "sha256_manifest.json").write_text(
        json.dumps({name: _sha256(path)}), encoding="utf-8"
    )
    workspace = _workspace(tmp_path)
    result = _run_script(["--verify-gim-bundle", str(d)], workspace)
    assert result.returncode != 0
    assert "day/year mismatch" in result.stderr


def test_verify_gim_bundle_refuses_on_grid_mismatch(tmp_path: Path) -> None:
    """A differently-gridded product (e.g. a non-CODE IONEX file) must not be
    silently accepted as the expected 2.5x5 degree CODE final product."""
    d = tmp_path / "bad_grid_bundle"
    d.mkdir()
    name = "COD0OPSFIN_20221000000_01D_01H_GIM.INX.gz"
    path = d / name
    _write_gz(path, _minimal_ionex_header(day=100, year=2022, lat1=90.0))  # wrong grid
    (d / "sha256_manifest.json").write_text(
        json.dumps({name: _sha256(path)}), encoding="utf-8"
    )
    workspace = _workspace(tmp_path)
    result = _run_script(["--verify-gim-bundle", str(d)], workspace)
    assert result.returncode != 0
    assert "grid parameter" in result.stderr


def test_overlap_audit_flags_when_target_station_present(tmp_path: Path) -> None:
    """Real station codes (bshm, nico -- confirmed present in the acquired
    2022 CODE network; aruc confirmed absent, per the 2026-09-26 hand-back)
    drive a real True result, never a hardcoded one."""
    workspace = _workspace(tmp_path)
    network_file = tmp_path / "network.txt"
    network_file.write_text("bshm\nnico\nabpo\nalbh\n", encoding="utf-8")
    result = _run_script(
        [
            "--overlap-audit-network",
            str(network_file),
            "--overlap-audit-out",
            "overlap.json",
        ],
        workspace,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads((workspace / "overlap.json").read_text(encoding="utf-8"))
    assert report["gim_network_overlap_flag"] is True
    assert report["per_station"]["BSHM"]["present_in_network"] is True
    assert report["per_station"]["NICO"]["present_in_network"] is True
    assert report["per_station"]["ARUC"]["present_in_network"] is False


def test_overlap_audit_no_flag_when_no_target_station_present(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    network_file = tmp_path / "network.txt"
    network_file.write_text("abpo\nalbh\nalgo\n", encoding="utf-8")
    result = _run_script(
        [
            "--overlap-audit-network",
            str(network_file),
            "--overlap-audit-out",
            "overlap.json",
        ],
        workspace,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads((workspace / "overlap.json").read_text(encoding="utf-8"))
    assert report["gim_network_overlap_flag"] is False


def test_overlap_audit_result_shape_matches_generation_gate_contract(tmp_path: Path) -> None:
    """The dict this CLI writes must carry the two keys
    `evaluate_generation_gates`/`render_comparison_report` actually require
    (`gim_network_overlap_flag`, `recorded_at_utc`) so it is directly usable
    as a `--gate-state`/`--render-comparison` `overlap_audit` value."""
    workspace = _workspace(tmp_path)
    network_file = tmp_path / "network.txt"
    network_file.write_text("bshm\n", encoding="utf-8")
    result = _run_script(
        [
            "--overlap-audit-network",
            str(network_file),
            "--overlap-audit-out",
            "overlap.json",
        ],
        workspace,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads((workspace / "overlap.json").read_text(encoding="utf-8"))
    assert "gim_network_overlap_flag" in report
    assert "recorded_at_utc" in report
    # ISO-8601 with timezone -- the same shape evaluate_generation_gates parses.
    assert "+" in report["recorded_at_utc"] or report["recorded_at_utc"].endswith("Z")
