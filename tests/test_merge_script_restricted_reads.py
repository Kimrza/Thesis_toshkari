"""`scripts/merge_coverage_year.py` routes its restricted reads through the chokepoint.

Purpose
-------
The `GOV-2026-08-28-FD-01` board named three `tests/` modules as restricted-root holders.
A full-repository sweep on 2026-08-28 found a **fourth file that is not a test at all**:
`scripts/merge_coverage_year.py`, a production script that holds the restricted-root
literal, writes the merged year there, and read **six** restricted content sites with no
`AccessRecord`. R-28's exemption is a `tests/` exemption and never covered it.

This module is that fix's test. It exercises the script's `guarded()` helper directly
rather than running the merge, because running the merge would re-derive a governed
artifact (D-18) and this test must not do that.

Inputs
------
`tmp_path`, plus the script imported as a module. `main()` is never called.

Re-run behaviour
----------------
Deterministic. Writes only under `tmp_path`. The real merge access log is never touched.

Governance
----------
* `governance-guards` R-25, R-28 (as narrowed 2026-08-28 to exact list membership).
* FR-P1-02-3, `VAL-2` -- log-then-read ordering.
* **D-18** -- the year re-merge, which is why this script's restricted access is
  legitimate and enumerated rather than removed.
* Written under **D-31**, which signed G-09.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import LockedTestError  # noqa: E402

SCRIPT = REPO_ROOT / "scripts" / "merge_coverage_year.py"


def _load_script():
    spec = importlib.util.spec_from_file_location("merge_coverage_year", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # main() is guarded by __name__ == "__main__"
    return module


def test_script_imports_without_running_the_merge() -> None:
    """Importing must not re-derive a governed artifact."""
    module = _load_script()
    assert hasattr(module, "guarded")
    assert hasattr(module, "main")


def test_restricted_root_is_inside_the_searched_roots() -> None:
    """The script genuinely reaches the locked month -- so it is a real reader.

    If it did not, the honest fix would be to drop it from the exemption rather than to
    route it. This pins that the exemption is earned.
    """
    module = _load_script()
    roots = [str(r) for r in module.EVIDENCE_ROOTS]
    assert any("locked_test_restricted" in r for r in roots)


def test_guarded_routes_a_restricted_path_and_writes_a_row(tmp_path: Path) -> None:
    module = _load_script()
    restricted = Path(module.RESTRICTED_DIR)
    if not restricted.is_dir():
        pytest.skip("restricted root absent")
    target = next((p for p in sorted(restricted.rglob("*")) if p.is_file()), None)
    if target is None:
        pytest.skip("no restricted artifact present")

    module.ACCESS_LOG = str(tmp_path / "merge_access.jsonl")
    returned = module.guarded(str(target))

    log = Path(module.ACCESS_LOG)
    assert log.is_file(), "the routed read wrote no access row"
    row = json.loads(log.read_text(encoding="utf-8").splitlines()[-1])
    assert row["run_id"] == "merge_coverage_year"
    assert row["locked_test_accessed"] is True
    assert row["performance_inspected"] is False
    assert row["purpose"] == "coverage_audit"
    assert dt.datetime.fromisoformat(row["logged_at_utc"]).tzinfo is not None
    assert Path(returned) == target.resolve()


def test_guarded_passes_an_ordinary_path_through_unlogged(tmp_path: Path) -> None:
    """Ordinary reads must NOT be routed: `open_restricted` refuses them by contract, and
    logging them would make the access log unable to distinguish restricted from ordinary."""
    module = _load_script()
    module.ACCESS_LOG = str(tmp_path / "merge_access.jsonl")
    ordinary = tmp_path / "plain.csv"
    ordinary.write_text("a,b\n1,2\n", encoding="utf-8")

    returned = module.guarded(str(ordinary))
    assert Path(returned) == ordinary
    assert not Path(module.ACCESS_LOG).exists()


def test_guarded_aborts_when_the_access_log_cannot_be_written(tmp_path: Path) -> None:
    """A failed log write aborts the read rather than proceeding unlogged."""
    module = _load_script()
    restricted = Path(module.RESTRICTED_DIR)
    if not restricted.is_dir():
        pytest.skip("restricted root absent")
    target = next((p for p in sorted(restricted.rglob("*")) if p.is_file()), None)
    if target is None:
        pytest.skip("no restricted artifact present")

    blocker = tmp_path / "blocker"
    blocker.write_text("file, not a directory", encoding="utf-8")
    module.ACCESS_LOG = str(blocker / "nested" / "merge_access.jsonl")

    with pytest.raises(LockedTestError):
        module.guarded(str(target))


def test_every_restricted_read_site_is_routed() -> None:
    """All six sites the sweep found call `guarded(...)`, and none reads directly.

    Asserted against the source text: a regression that reintroduces a bare
    `open(hashes_path)` would restore the unlogged read this fix removed, and no runtime
    assertion would catch it because the merge is not executed by the suite.
    """
    source = SCRIPT.read_text(encoding="utf-8")
    routed = source.count("guarded(")
    # 6 call sites + the def + the docstring reference in the chokepoint comment block.
    assert routed >= 7, f"expected the six routed read sites plus the definition, found {routed}"

    for bare in (
        "with open(hashes_path) as fh:",
        "with open(raw_path, newline='') as fh:",
        "if sha256_of_file(target) != expected:",
    ):
        assert bare not in source, (
            f"unrouted restricted read reintroduced: {bare!r}"
        )
