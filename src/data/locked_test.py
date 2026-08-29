"""The restricted-root path guard: one chokepoint for every read under the locked month.

Purpose
-------
D-15 made `evidence/locked_test_restricted/` a governance boundary that holds **only while
exactly one code path reaches it**. `governance-guards` R-28 states the consequence in its
own words: the boundary "does not weaken slightly; it ends" if a second path exists. This
module is that one path.

Inputs
------
* `path` -- the artifact to read, which must lie under `RESTRICTED_ROOT`.
* `record` -- a fully populated `AccessRecord` describing the read *before* it happens.
* `registry` -- the access log the record is appended to (normally
  `evidence/experiment_registry.md`, or a JSONL sidecar in tests and fixtures).

Re-run behaviour
----------------
**Not idempotent by design.** Every call appends one row. `component-methods.md` fixes
"one row per artifact opened", and `inventory-and-registry` gives the reason: one row per
*run* would make the log say less than what happened, and a reviewer could not tell which
reads occurred. Re-running a read legitimately produces a second row.

Ordering contract, which is the whole point
-------------------------------------------
The record is written **and flushed to disk** before the path is returned for reading.
FR-P1-02-3 and `VAL-2` require log-then-read: an access recorded after the fact *fails*
the ordering check rather than satisfying it. Rows 5, 8, 9 and 10 of the project's own
access log are retrospective and say so; rows 6, 7, 11 and 12 set the standard this module
enforces mechanically.

Governance
----------
* `component-methods.md` -- the approved `AccessRecord` shape and `open_restricted`
  signature, reproduced here without widening.
* `governance-guards` R-25 (durable before the read), R-26, R-27, R-28.
* Created under **D-31** (2026-08-28), which signed G-09 and thereby authorised writing
  this module. D-31 records that G-09's own TE 18.3 preconditions were **unmet** when
  signed; nothing in this module claims otherwise.
* This module is the **only** one permitted to contain the restricted-root literal outside
  R-28's enumerated `tests/` exemption.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Final, Sequence

from src.data.config import LockedTestError

__all__ = [
    "RESTRICTED_ROOT",
    "AccessRecord",
    "PURPOSES",
    "open_restricted",
    "assert_no_december_outside_restricted",
]

RESTRICTED_ROOT: Final[str] = "evidence/locked_test_restricted"

#: The three purposes Vision 8.3 distinguishes. `coverage_audit` and `regime_audit` are
#: performance-blind and permitted before G-05; `locked_evaluation` is the one-shot,
#: hash-before-metrics event G-06 gates.
PURPOSES: Final[frozenset[str]] = frozenset(
    {"coverage_audit", "regime_audit", "locked_evaluation"}
)


@dataclass(frozen=True)
class AccessRecord:
    """One row of the locked-month access log, describing a read before it happens."""

    run_id: str
    retrieved_at_utc: str
    scope: str
    purpose: str
    performance_inspected: bool
    locked_test_accessed: bool
    authorization: str

    def __post_init__(self) -> None:
        for field_name in (
            "run_id",
            "retrieved_at_utc",
            "scope",
            "purpose",
            "authorization",
        ):
            if not getattr(self, field_name):
                raise LockedTestError(
                    "AccessRecord",
                    f"field {field_name!r} is empty; an access row that does not say who "
                    f"read what, when, why and under whose authority is not a record",
                )
        if self.purpose not in PURPOSES:
            raise LockedTestError(
                "AccessRecord",
                f"purpose {self.purpose!r} is not one of {sorted(PURPOSES)}",
            )
        if not self.locked_test_accessed:
            raise LockedTestError(
                "AccessRecord",
                "locked_test_accessed must be True for any read under RESTRICTED_ROOT; "
                "TE 13.4 makes the flag the fact a G-06 reviewer establishes",
            )


def _restricted_root(repo_root: Path) -> Path:
    return (repo_root / RESTRICTED_ROOT).resolve()


def _append_and_flush(registry: Path, record: AccessRecord) -> str:
    """Append one row, stamp it with the guard's OWN write time, force it to disk.

    `os.fsync` is what makes "durable before the read" true rather than merely intended
    (R-25). A row sitting in the OS page cache when the process dies is a read that
    happened with no record of it -- exactly the failure the ordering rule exists to
    prevent.

    **`logged_at_utc` is stamped here, by the guard, never by the caller.**
    `retrieved_at_utc` is caller-supplied and descriptive; a field the caller controls
    cannot evidence that the log preceded the read. `logged_at_utc` is written
    immediately before the fsync, and therefore before `open_restricted` returns the path
    the caller then reads -- so comparing it against any later artifact or run timestamp
    is a real ordering check rather than a restatement of the caller's intent.

    Found by execution, 2026-08-28: the first run of the routed suites produced 37 rows
    whose `retrieved_at_utc` was all the same caller-supplied placeholder string, leaving
    FR-P1-02-3's ordering requirement unverifiable from the log it is recorded in. This
    field is that defect's fix.
    """
    registry.parent.mkdir(parents=True, exist_ok=True)
    row = asdict(record)
    row["logged_at_utc"] = _dt.datetime.now(_dt.timezone.utc).isoformat()
    line = json.dumps(row, sort_keys=True, ensure_ascii=False)
    with registry.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return row["logged_at_utc"]


def open_restricted(path: Path, *, record: AccessRecord, registry: Path) -> Path:
    """Record the access, flush it, then return `path` for reading.

    Raises
    ------
    LockedTestError
        * when `path` is not under `RESTRICTED_ROOT` -- callers must not route ordinary
          reads through the guard, because a guard that accepts anything stops being
          evidence that restricted reads went through it;
        * when the registry write fails -- **a failed log write aborts the read rather
          than proceeding unlogged.** This is the branch that makes the ordering rule
          enforceable instead of advisory.

    Returns
    -------
    Path
        The same path, resolved. The caller reads it *after* this function returns, which
        is what makes the log-then-read ordering hold by construction.
    """
    resolved = Path(path).resolve()

    # Derive the repository root from this module's own location rather than from the
    # caller, so a caller cannot relocate the boundary by passing a different root.
    repo_root = Path(__file__).resolve().parent.parent.parent
    root = _restricted_root(repo_root)

    if not resolved.is_relative_to(root):
        raise LockedTestError(
            resolved,
            f"path is not under {RESTRICTED_ROOT}; open_restricted is the chokepoint for "
            f"restricted reads only, and routing an ordinary read through it would make "
            f"the access log unable to distinguish the two",
        )

    try:
        _append_and_flush(Path(registry), record)
    except OSError as exc:
        raise LockedTestError(
            registry,
            f"access-log write failed ({exc}); the read is aborted rather than performed "
            f"unlogged -- FR-P1-02-3 requires the record to be durable BEFORE the read",
        ) from exc

    return resolved


def assert_no_december_outside_restricted(evidence_root: Path) -> Sequence[Path]:
    """FR-P1-02-6's regression guard: December-bearing artifacts outside the restricted root.

    Walks `evidence/` **recursively** and returns every December-bearing artifact found
    outside the restricted root. An empty sequence is the pass condition.

    Recursive by construction: `DATA-01` showed a non-recursive glob silently stopped
    checking the artifacts that matter most, and D-15 relocated 21 files, so a guard that
    only looks one level down would report clean while missing the relocation entirely.

    Membership is decided by **record date**, never by directory name -- `project.md`
    forbids deriving partition membership from a path, after a year-blind acquisition
    predicate filed locked-month records into `audit_evidence_2022-01/`.
    """
    root = Path(evidence_root).resolve()
    if not root.is_dir():
        return []
    restricted = (root / "locked_test_restricted").resolve()

    offenders: list[Path] = []
    for candidate in sorted(root.rglob("*.json")):
        if candidate.is_relative_to(restricted):
            continue
        try:
            text = candidate.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if '"2022-12' in text or "'2022-12" in text:
            offenders.append(candidate)
    return offenders
