"""D-83 revision 7 §W7 W-7 (peak RSS, CPU model, TC-03 limits) and W-8 (storage excludes
archived copies).

Purpose: show the capture measures a real child's memory, the TC-03 limbs refuse a breach
and an unmeasured value, and `storage_total` ignores archived copies. Inputs: a short-lived
child interpreter and a synthetic fixture root in `tmp_path`. Re-run behaviour: pure.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

from src.data.config import IntegrityError
from src.data.resources import (
    TC03_RUNTIME_LIMIT_SECONDS,
    assert_tc03_limits,
    cpu_model,
    meminfo_total_bytes,
    peak_rss_of_popen,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _skeleton():
    spec = importlib.util.spec_from_file_location(
        "rws_under_test", REPO_ROOT / "scripts" / "run_walking_skeleton.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_peak_rss_of_a_child_reflects_its_allocation() -> None:
    proc = subprocess.Popen(  # noqa: S603 - fixed argv
        [sys.executable, "-c", "b = bytearray(80 * 1024 * 1024); b[::4096] = b'x' * len(b[::4096])"],
    )
    proc.wait(timeout=120)
    measured = peak_rss_of_popen(proc)
    assert measured["bytes"] is not None and measured["bytes"] >= 70 * 1024 * 1024
    assert measured["method"]


def test_cpu_model_is_a_model_string() -> None:
    assert cpu_model() and cpu_model() != "unknown-cpu"


def test_meminfo_total_parses_and_absent_is_none(tmp_path) -> None:
    path = tmp_path / "meminfo"
    path.write_text("MemTotal:        8123456 kB\nMemFree: 1 kB\n", encoding="utf-8")
    assert meminfo_total_bytes(path) == 8123456 * 1024
    assert meminfo_total_bytes(tmp_path / "absent") is None


def test_tc03_runtime_limb_refuses_over_12_hours() -> None:
    with pytest.raises(IntegrityError):
        assert_tc03_limits(
            runtime_seconds=TC03_RUNTIME_LIMIT_SECONDS + 1, peak_rss_bytes=1, g07_memtotal_bytes=2
        )


def test_tc03_ram_limb_refuses_over_memtotal_and_unmeasured() -> None:
    with pytest.raises(IntegrityError):
        assert_tc03_limits(runtime_seconds=1, peak_rss_bytes=3, g07_memtotal_bytes=2)
    with pytest.raises(IntegrityError):
        assert_tc03_limits(runtime_seconds=1, peak_rss_bytes=None, g07_memtotal_bytes=2)


def test_tc03_ram_limb_is_pending_not_passed_before_g07() -> None:
    result = assert_tc03_limits(runtime_seconds=1, peak_rss_bytes=1, g07_memtotal_bytes=None)
    assert result["ram"].startswith("pending")
    assert assert_tc03_limits(runtime_seconds=1, peak_rss_bytes=1, g07_memtotal_bytes=2) == {
        "runtime": "pass",
        "ram": "pass",
    }


def test_run_command_records_peak_rss() -> None:
    mod = _skeleton()
    result = mod.run_command(
        [sys.executable, "-c", "print('ok')"], env=dict(__import__("os").environ), cwd=REPO_ROOT
    )
    assert result["returncode"] == 0 and result["peak_rss_bytes"] and result["peak_rss_method"]


def test_storage_total_excludes_archived_copies(tmp_path) -> None:
    mod = _skeleton()
    root = tmp_path / "fixture"
    (root / "features" / "F1").mkdir(parents=True)
    (root / "features" / "F1.archived-run2").mkdir(parents=True)
    (root / "archived_releases" / "x").mkdir(parents=True)
    (root / "metrics.json").write_bytes(b"a" * 10)
    (root / "metrics.json.archived-pv-2026-09-29").write_bytes(b"b" * 1000)
    (root / "features" / "F1" / "t.parquet").write_bytes(b"c" * 20)
    (root / "features" / "F1.archived-run2" / "t.parquet").write_bytes(b"d" * 1000)
    (root / "archived_releases" / "x" / "r.json").write_bytes(b"e" * 1000)
    assert mod._storage_bytes(root) == 30


def test_storage_is_unchanged_by_adding_an_archive(tmp_path) -> None:
    """The property W-8 exists for: a re-run that archives the prior outputs does not grow
    this run's measured storage."""
    mod = _skeleton()
    root = tmp_path / "fixture"
    root.mkdir()
    (root / "predictions.parquet").write_bytes(b"p" * 100)
    before = mod._storage_bytes(root)
    (root / "predictions.parquet.archived-run9").write_bytes(b"p" * 100)
    assert mod._storage_bytes(root) == before


def test_live_files_never_descends_into_archived_directories(tmp_path, monkeypatch) -> None:
    """2026-10-01: a nested archive past MAX_PATH aborted a measuring run from inside
    `rglob`. The live walk must prune archived directories without visiting them."""
    import os

    mod = _skeleton()
    (tmp_path / "metrics.json").write_text("{}", encoding="utf-8")
    deep = tmp_path / "archived_releases" / "evaluation.archived-x" / "a"
    deep.mkdir(parents=True)
    (deep / "metrics.json").write_text("{}", encoding="utf-8")
    (tmp_path / "plots.archived-y").mkdir()
    (tmp_path / "metrics.json.archived-z").write_text("{}", encoding="utf-8")

    visited: list[str] = []
    real_walk = os.walk

    def spy(top, *a, **k):
        for dirpath, dirnames, filenames in real_walk(top, *a, **k):
            visited.append(dirpath)
            yield dirpath, dirnames, filenames

    monkeypatch.setattr(mod.os, "walk", spy)
    files = mod.live_files(tmp_path)
    assert [p.name for p in files] == ["metrics.json"]
    assert not any(".archived-" in v or "archived_releases" in v for v in visited)


def test_live_files_still_finds_nested_live_outputs(tmp_path) -> None:
    """Negative control: pruning is by archive marker only; a live nested output is kept."""
    mod = _skeleton()
    nested = tmp_path / "plots"
    nested.mkdir()
    (nested / "residuals.png").write_bytes(b"x")
    assert [p.relative_to(tmp_path).as_posix() for p in mod.live_files(tmp_path)] == [
        "plots/residuals.png"
    ]

def test_storage_counts_only_what_this_run_wrote(tmp_path) -> None:
    """D-85 V-2 (2026-10-01): files left live by earlier runs are not this run's storage."""
    import os

    mod = _skeleton()
    root = tmp_path / "fixture"
    (root / "releases" / "plumbing_7day_20261001T120000Z").mkdir(parents=True)
    (root / "releases" / "plumbing_7day_20261001T120000Z" / "f.parquet").write_bytes(b"o" * 500)
    (root / "measuring_result_old.json").write_bytes(b"m" * 300)
    (root / "metrics.json").write_bytes(b"x" * 40)
    before = mod.live_file_states(root)
    (root / "releases" / "plumbing_7day_20261001T130000Z").mkdir(parents=True)
    (root / "releases" / "plumbing_7day_20261001T130000Z" / "f.parquet").write_bytes(b"n" * 70)
    (root / "metrics.json").write_bytes(b"y" * 45)
    stat = (root / "metrics.json").stat()
    os.utime(root / "metrics.json", ns=(stat.st_atime_ns, stat.st_mtime_ns + 10_000_000))
    (root / "metrics.json.archived-run1").write_bytes(b"a" * 900)
    assert mod._storage_bytes(root, before) == 70 + 45
    assert mod._storage_bytes(root) == 500 + 300 + 70 + 45


def test_storage_counts_a_rewrite_with_unchanged_size(tmp_path) -> None:
    import os

    mod = _skeleton()
    root = tmp_path / "fixture"
    root.mkdir()
    (root / "registry_entry.json").write_bytes(b"r" * 64)
    before = mod.live_file_states(root)
    stat = (root / "registry_entry.json").stat()
    os.utime(root / "registry_entry.json", ns=(stat.st_atime_ns, stat.st_mtime_ns + 10_000_000))
    assert mod._storage_bytes(root, before) == 64
    assert mod.live_file_states(tmp_path / "absent") == {}
