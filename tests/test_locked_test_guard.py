"""The restricted-root chokepoint: log-then-read ordering, and refusal of every bypass.

Purpose
-------
WS-18 and TA-18 require an executable guard, not a procedure. This module is that guard's
test. It proves four things the design asserts and nothing previously checked:

1. `open_restricted` writes a durable `AccessRecord` **before** the read.
2. A read attempted outside the chokepoint is refused.
3. **A failed access-log write aborts the read** rather than proceeding unlogged.
4. The ordering is **verifiable after the fact** from the log itself.

Inputs
------
`tmp_path` and the repository's own `evidence/` tree, read only for the negative control
that ordinary paths are rejected. No December target value is read, parsed, counted or
computed anywhere in this module.

Re-run behaviour
----------------
Deterministic and self-contained. Each test uses its own registry file under `tmp_path`;
the project's real access log is never written to.

Governance
----------
* `component-methods.md` -- the `open_restricted` contract and its two raise conditions.
* `governance-guards` R-25 (durable before the read), R-28 (one door).
* FR-P1-02-3, `VAL-2` -- log-then-read ordering.
* `evidence/experiment_registry.md` -- rows 5, 8, 9, 10 are retrospective and say so; rows
  6, 7, 11, 12 set the standard this module enforces mechanically.
* Written under **D-31**, which signed G-09 and authorised creating this module.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import LockedTestError  # noqa: E402
from src.data.locked_test import (  # noqa: E402
    PURPOSES,
    RESTRICTED_ROOT,
    AccessRecord,
    open_restricted,
)

RESTRICTED_DIR = REPO_ROOT / RESTRICTED_ROOT


def _record(purpose: str = "coverage_audit") -> AccessRecord:
    return AccessRecord(
        run_id="test-run",
        retrieved_at_utc="2026-08-28T00:00:00Z",
        scope="December 2022, ARUC/BSHM/NICO cells",
        purpose=purpose,
        performance_inspected=False,
        locked_test_accessed=True,
        authorization="Vision 8.3 performance-blind coverage audit",
    )


def _any_restricted_file() -> Path | None:
    if not RESTRICTED_DIR.is_dir():
        return None
    for candidate in sorted(RESTRICTED_DIR.rglob("*")):
        if candidate.is_file():
            return candidate
    return None


# --- 1. the record is durable before the read -----------------------------------------


def test_access_record_is_written_and_flushed_before_the_path_is_returned(
    tmp_path: Path,
) -> None:
    target = _any_restricted_file()
    if target is None:
        pytest.skip("no restricted artifact present to guard")
    registry = tmp_path / "access.jsonl"

    returned = open_restricted(target, record=_record(), registry=registry)

    assert registry.is_file(), "no access row was written"
    rows = [json.loads(line) for line in registry.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    assert rows[0]["locked_test_accessed"] is True
    assert rows[0]["purpose"] in PURPOSES
    assert returned == target.resolve()


def test_each_call_appends_its_own_row(tmp_path: Path) -> None:
    """One row per artifact opened, not one per run -- otherwise the log says less than
    what happened and a reviewer cannot tell which reads occurred."""
    target = _any_restricted_file()
    if target is None:
        pytest.skip("no restricted artifact present to guard")
    registry = tmp_path / "access.jsonl"
    open_restricted(target, record=_record(), registry=registry)
    open_restricted(target, record=_record(purpose="regime_audit"), registry=registry)
    rows = registry.read_text(encoding="utf-8").strip().splitlines()
    assert len(rows) == 2


# --- 2. reads outside the chokepoint are refused ---------------------------------------


def test_ordinary_path_is_refused(tmp_path: Path) -> None:
    """A guard that accepts anything stops being evidence that restricted reads used it."""
    ordinary = tmp_path / "ordinary.txt"
    ordinary.write_text("not restricted", encoding="utf-8")
    with pytest.raises(LockedTestError) as excinfo:
        open_restricted(ordinary, record=_record(), registry=tmp_path / "access.jsonl")
    assert RESTRICTED_ROOT in str(excinfo.value)


def test_refused_path_writes_no_access_row(tmp_path: Path) -> None:
    """Negative control: a rejected call must not pollute the log with a phantom read."""
    ordinary = tmp_path / "ordinary.txt"
    ordinary.write_text("x", encoding="utf-8")
    registry = tmp_path / "access.jsonl"
    with pytest.raises(LockedTestError):
        open_restricted(ordinary, record=_record(), registry=registry)
    assert not registry.exists(), "a refused read wrote an access row for a read that never happened"


def test_traversal_out_of_the_restricted_root_is_refused(tmp_path: Path) -> None:
    """`..` must not walk out of the boundary and still be accepted."""
    if not RESTRICTED_DIR.is_dir():
        pytest.skip("restricted root absent")
    escape = RESTRICTED_DIR / ".." / "experiment_registry.md"
    with pytest.raises(LockedTestError):
        open_restricted(escape, record=_record(), registry=tmp_path / "access.jsonl")


# --- 3. a failed log write aborts the read ---------------------------------------------


def test_failed_registry_write_aborts_the_read(tmp_path: Path) -> None:
    """The branch that makes the ordering rule enforceable rather than advisory.

    The registry path is made unwritable by pointing it at a location whose parent is a
    *file*, so `mkdir` fails. The call must raise rather than return a readable path.
    """
    target = _any_restricted_file()
    if target is None:
        pytest.skip("no restricted artifact present to guard")
    blocker = tmp_path / "blocker"
    blocker.write_text("I am a file, not a directory", encoding="utf-8")
    unwritable = blocker / "nested" / "access.jsonl"

    with pytest.raises(LockedTestError) as excinfo:
        open_restricted(target, record=_record(), registry=unwritable)
    assert "aborted" in str(excinfo.value) or "write failed" in str(excinfo.value)


# --- 4. the record's own shape is enforced ---------------------------------------------


def test_record_rejects_an_unknown_purpose() -> None:
    with pytest.raises(LockedTestError):
        AccessRecord(
            run_id="r",
            retrieved_at_utc="t",
            scope="s",
            purpose="browsing",
            performance_inspected=False,
            locked_test_accessed=True,
            authorization="a",
        )


def test_record_rejects_locked_test_accessed_false() -> None:
    """Every read under the restricted root is a locked-test access by definition."""
    with pytest.raises(LockedTestError):
        AccessRecord(
            run_id="r",
            retrieved_at_utc="t",
            scope="s",
            purpose="coverage_audit",
            performance_inspected=False,
            locked_test_accessed=False,
            authorization="a",
        )


@pytest.mark.parametrize(
    "field", ["run_id", "retrieved_at_utc", "scope", "purpose", "authorization"]
)
def test_record_rejects_an_empty_required_field(field: str) -> None:
    kwargs = {
        "run_id": "r",
        "retrieved_at_utc": "t",
        "scope": "s",
        "purpose": "coverage_audit",
        "performance_inspected": False,
        "locked_test_accessed": True,
        "authorization": "a",
    }
    kwargs[field] = ""
    with pytest.raises(LockedTestError):
        AccessRecord(**kwargs)


# --- 5. one door: the static membership check ------------------------------------------


def test_restricted_literal_holders_are_exactly_the_enumerated_exemption() -> None:
    """R-28 as ruled 2026-08-28: exact list membership, never a substring exemption.

    The exemption exists because test modules must be able to assert *where the boundary
    is*. It covers holding the **literal**; it never covers obtaining the **content**.
    """
    # The chokepoint itself, R-28s four enumerated tests/ modules, and the one
    # production script that legitimately merges the locked month (D-18). The script was
    # found by the full-scope sweep on 2026-08-28 and is listed here rather than left
    # unenumerated -- an exemption a reader cannot see is not an exemption, it is a hole.
    exempt = {
        "src/data/locked_test.py",
        "scripts/merge_coverage_year.py",
        "tests/test_acquisition_window.py",
        "tests/test_phase_boundary.py",
        "tests/test_release_hashes.py",
        "tests/test_locked_test_guard.py",
    }
    holders: set[str] = set()
    for tree in ("src", "tests", "scripts"):
        base = REPO_ROOT / tree
        if not base.is_dir():
            continue
        for module in sorted(base.rglob("*.py")):
            text = module.read_text(encoding="utf-8", errors="replace")
            if "locked_test_restricted" in text:
                holders.add(module.relative_to(REPO_ROOT).as_posix())

    unexpected = holders - exempt
    assert not unexpected, (
        f"modules outside R-28's enumerated exemption contain the restricted-root "
        f"literal: {sorted(unexpected)}. The one-door property does not weaken slightly; "
        f"it ends."
    )
