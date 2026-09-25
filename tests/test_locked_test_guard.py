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

Extended at stage 3.5 (2026-09-05), four additions:

5. The one-door literal scan is now **AST-based with constant folding**. Scope stated
   exactly: **DISC-2's named evasion (Q2 = B, ``+``-concatenation of literals --
   ``EVIDENCE_DIR / ("locked_test" + "_restricted")``) is closed; the folder is
   extended to constant-only call forms** (``os.path.join``/``joinpath``,
   ``%``-format, ``str.format``, ``str.join`` over constant elements, pathlib ``/``
   over constants); **runtime assembly remains statically unclosable and is
   disclosed** as this scan's named residual rather than implied closed -- the
   run-time chokepoint is the layer that holds regardless of how a path string was
   assembled. The plain-text substring catch is RETAINED as a superset (a literal in
   a comment still names the boundary), notebook code cells are scanned, and an
   unparseable file is a **failure** via the one shared R-27 helper both custody
   scans call (`src.data.locked_test.fail_unparseable`).
6. The exempt set is re-derived **exactly** against the seven on-disk members, closing
   the nfr-design review Minor that spot-checked rather than re-derived it (DISC-1: the
   code asserts the true seven; the six-in-prose discrepancy stays a gate item).
7. **Q1 = A**: `open_restricted` refuses, fail-closed, on a platform whose write
   durability is uncharacterised -- no read, no access row consumed.
8. The **SD-G-02 join** is wired: `AccessRecord` reconciles against foundation's
   registry (`reconcile_access_records`, a pure read), orphans both ways, known
   pre-guard orphans reported and never back-filled, both logs byte-identical after.

Two units in one module (features-and-splits nfr-design Q3 = C, 2026-09-04)
---------------------------------------------------------------------------
ADR-03 splits the locked-test guard into two limbs held by two units, and this one
TE 12-mandated module carries both. The ownership is stated here so a later reader does
not attribute either limb to the other unit:

* **Limb 2 -- the READ chokepoint -- `governance-guards`.** Sections 1-8 above AND
  section 10 below: `src/data/locked_test.py`'s `open_restricted` / `write_restricted`,
  R-25 (durable before the read), R-27 (unparseable is a failure), R-28 (one door, the
  exempt list), SD-G-01..SD-G-04. Cases unchanged by the 2026-09-06 extension.
* **Limb 1 -- the EXECUTION block -- `features-and-splits`.** Section 9 below:
  `src/data/splits.py`'s `materialise_locked_partition(snapshot, *, g05_signature)`
  refuses with `LockedTestError` when the signature is `None` (the pre-G-05 execution
  block WS-18 evidences) and when it fails verification against `configs/data.yaml`
  `gates.G-05`; it owns no read path (a loader routed through `open_restricted` must be
  supplied, and none is today); and a verifying signature over a SYNTHETIC calendar
  materialises with the first embargo hours EXCLUDED AND COUNTED (R-82, SD-F-05,
  D-28's 30-day shape). The read for the required pre-G-05 coverage audit never comes
  through limb 1 -- that is limb 2's door.

Section 10 -- the SD-C-02 containment fields (added 2026-09-11, governance-guards)
----------------------------------------------------------------------------------
`src/data/locked_test.py` is this unit's module, and commit `8a6cb61` (2026-09-07)
added an owner-ruled, additive edit to it from `evaluation-and-comparison`'s stage 3.5
(Q2 = B, SD-C-02; `governance/CHANGE_RECORD_2026-09-06_R106_comparison_sets.md:82-85`,
which records the review as "owed to `governance-guards`' next touch"). Until now the
only coverage of that edit lived in a sibling's `tests/test_common_masks.py`, and it
covered the CONSUMER (`require_locked_receipt`'s refusal), never the PRODUCER. Section
10 is this unit's own coverage of the producer: every violating input is driven through
the real `open_restricted` entry point (the c58/c59 shape -- prove invocation per entry
point, never correctness of a bare helper once), including the new failure mode a
present-but-unparseable manifest introduces, which ABORTS the read rather than logging
`None`.

**No December 2022 content is read, parsed, counted or computed anywhere in this
module** -- limb 1's cases run over the synthetic partition fixture
`test_split_embargo.py` authors (a synthetic calendar year), and the repository's
`configs/data.yaml` carries no `gates.G-05` record, so no real signature can verify.
Section 10 likewise runs entirely against a synthetic `tmp_path` boundary installed
through the module's supported `_repo_root` seam: no real restricted artifact is opened
and no manifest fixture carries a December timestamp.
Both limbs support WS-18 and TA-18; neither discharges them.
"""

from __future__ import annotations

import ast
import datetime as dt
import json
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data import locked_test  # noqa: E402
from src.data.config import LockedTestError, RegistryError  # noqa: E402
from src.data.experiment_registry import (  # noqa: E402
    REGISTRY_COLUMNS,
    append_registry_event,
    reconcile_access_records,
)
from src.data.locked_test import (  # noqa: E402
    DECEMBER_DRIVER_EXCLUSION_CLASSES,
    PURPOSES,
    RESTRICTED_LITERAL_EXEMPT_MODULES,
    RESTRICTED_ROOT,
    AccessRecord,
    EvidenceScanError,
    assert_no_december_outside_restricted,
    december_custody_inventory,
    december_driver_exclusion_class,
    fail_unparseable,
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


def test_log_timestamp_is_guard_stamped_and_precedes_the_read(tmp_path: Path) -> None:
    """Ordering must be VERIFIABLE from the log, not merely intended by the caller.

    Regression test for a defect found by execution on 2026-08-28: the first routed run
    wrote 37 rows whose `retrieved_at_utc` was all the same caller-supplied placeholder
    string. Every row was present, every read was logged -- and the log still could not
    evidence that logging preceded reading, because the only timestamp in it came from
    the caller.

    `logged_at_utc` is stamped by the guard immediately before the fsync. This test pins
    that it exists, that it parses as a real UTC instant, and that it lands before the
    artifact is read -- proved by reading the file only afterwards and comparing.
    """
    target = _any_restricted_file()
    if target is None:
        pytest.skip("no restricted artifact present to guard")
    registry = tmp_path / "access.jsonl"

    returned = open_restricted(target, record=_record(), registry=registry)
    row = json.loads(registry.read_text(encoding="utf-8").splitlines()[-1])

    assert "logged_at_utc" in row, (
        "the guard wrote no timestamp of its own; ordering would rest entirely on a "
        "caller-supplied field, which is the defect this test exists for"
    )
    logged = dt.datetime.fromisoformat(row["logged_at_utc"])
    assert logged.tzinfo is not None, "logged_at_utc must be timezone-aware UTC"

    # The read happens only now -- after the row was flushed.
    returned.read_bytes()
    assert logged <= dt.datetime.now(dt.timezone.utc)


def test_caller_supplied_timestamp_is_not_trusted_for_ordering(tmp_path: Path) -> None:
    """A caller may still write a well-formed LIE; the guard's own stamp is what holds.

    Amended 2026-09-20 (Recommendation 1). It previously used the literal
    `"not-a-timestamp-at-all"`, which `AccessRecord` now refuses outright -- see
    `test_record_rejects_an_unparseable_retrieved_at_utc` below for that limb. The point
    this test was written to make is untouched and is now made with a value the tightened
    constructor accepts: a wildly FUTURE-dated timestamp. The narrowing is deliberate and
    stated so it is not over-read -- parseability is not truthfulness, and
    `retrieved_at_utc` is still a descriptive caller field that ordering must not rest on.
    """
    target = _any_restricted_file()
    if target is None:
        pytest.skip("no restricted artifact present to guard")
    registry = tmp_path / "access.jsonl"

    future = "2999-01-01T00:00:00+00:00"
    bogus = AccessRecord(
        run_id="r",
        retrieved_at_utc=future,
        scope="s",
        purpose="coverage_audit",
        performance_inspected=False,
        locked_test_accessed=True,
        authorization="a",
    )
    open_restricted(target, record=bogus, registry=registry)
    row = json.loads(registry.read_text(encoding="utf-8").splitlines()[-1])

    assert row["retrieved_at_utc"] == future
    # The guard's own stamp is still a real instant, independent of the caller's field --
    # and it is in the PAST relative to the caller's claim, which is the whole point.
    logged = dt.datetime.fromisoformat(row["logged_at_utc"])
    assert logged.tzinfo is not None
    assert logged < dt.datetime.fromisoformat(future), (
        "the guard's stamp tracked the caller's claim; ordering evidence would then be "
        "caller-controlled, which is the defect this test exists for"
    )


def test_record_rejects_an_unparseable_retrieved_at_utc() -> None:
    """NEGATIVE CONTROL for Recommendation 1's durable closure.

    Four mutants, each pushed through the real public entry point -- the `AccessRecord`
    constructor -- and each required to raise: the exact historical placeholder that all
    5,964 rows of `evidence/test_run_access_log.jsonl` carried, plus three other
    non-parsing shapes. Without this, the check could be deleted and nothing would notice.
    """
    for bad in (
        "recorded-at-call-time-by-the-runner",  # the literal 5,964 rows actually carried
        "not-a-timestamp-at-all",
        "t",
        "2026-13-45T99:99:99Z",  # well-shaped but not a real instant
    ):
        with pytest.raises(LockedTestError) as excinfo:
            AccessRecord(
                run_id="r",
                retrieved_at_utc=bad,
                scope="s",
                purpose="coverage_audit",
                performance_inspected=False,
                locked_test_accessed=True,
                authorization="a",
            )
        assert "retrieved_at_utc" in str(excinfo.value), (
            f"{bad!r} was refused for some other reason; the refusal must name the field"
        )


def test_record_accepts_the_shapes_a_real_producer_writes() -> None:
    """MUST-NOT-FIRE limb. The check must not refuse a legitimate timestamp.

    Three shapes: what `datetime.now(timezone.utc).isoformat()` produces (the form
    `scripts/06`, `scripts/07`, `src/data/inventory.py` and both repaired test producers
    write), the `Z`-suffixed form already on disk in existing fixtures, and a
    second-resolution offset form.
    """
    for good in (
        dt.datetime.now(dt.timezone.utc).isoformat(),
        "2026-08-28T00:00:00Z",
        "2026-09-20T15:16:20+00:00",
    ):
        record = AccessRecord(
            run_id="r",
            retrieved_at_utc=good,
            scope="s",
            purpose="coverage_audit",
            performance_inspected=False,
            locked_test_accessed=True,
            authorization="a",
        )
        assert record.retrieved_at_utc == good


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
    assert (
        not registry.exists()
    ), "a refused read wrote an access row for a read that never happened"


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
            retrieved_at_utc="2026-08-28T00:00:00Z",
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
            retrieved_at_utc="2026-08-28T00:00:00Z",
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
#
# DISC-2's named evasion (Q2 = B, TS-G-02: a path assembled from joined literals via
# `+`-concatenation) is CLOSED: the scan is AST-based with constant folding, and the
# plain substring catch is retained as a superset (a literal held only in a comment
# still names the boundary). The folder is further extended to constant-only CALL
# forms: `os.path.join`/`joinpath` over constant args, `%`-formatting and
# `str.format` with constant operands, `str.join` over a constant-element list or
# tuple, and pathlib-style `/` over constants. DISCLOSED RESIDUAL, named rather than
# implied closed: arbitrary runtime assembly (a variable-fed format, a computed
# component, any value that is not a constant expression) REMAINS STATICALLY
# UNCLOSABLE and is not caught by this scan -- a static check can fold constants, not
# execute programs. That residual is bounded by review plus the run-time chokepoint
# (`open_restricted` refuses any path outside the root regardless of how its string
# was assembled), exactly the layering R-28 records when it leaves the
# run-time-path-assembly gap open deliberately. Notebook code cells are scanned per
# the declared width. An unparseable file is a FAILURE via the shared R-27 helper
# (`fail_unparseable`), the one home both custody scans call.

_LITERAL = "locked_test_restricted"

#: Lines dropped from notebook cell sources before AST parsing: IPython magics and
#: shell escapes are not Python and would otherwise make every magic-bearing cell an
#: R-27 failure. This is a DECLARED transformation, not silence -- a cell that still
#: fails to parse after it is a failure.
_NOTEBOOK_NON_PYTHON_PREFIXES = ("%", "!")


#: Cartesian-product cap for join-like folds, so a pathological constant expression
#: cannot make the scan combinatorial. Real code holds one or two candidates per node.
_FOLD_CANDIDATE_CAP = 64


def _fold_candidates(node: ast.AST) -> set[str]:
    """Every string this CONSTANT-ONLY expression can be statically folded to.

    Folded forms: string literals; ``+`` concatenation (DISC-2's named evasion);
    f-strings (constant parts joined -- a partial fold, conservative in the catching
    direction); ``%``-formatting and ``str.format`` with constant operands;
    ``str.join`` over a constant-element list/tuple; ``os.path.join``-shaped calls
    (any ``.join(...)`` whose receiver is not itself a constant string) and
    ``.joinpath(...)``, over constant args; and pathlib-style ``/`` over constants.
    Join-like forms yield BOTH the separator-joined and the separator-less
    concatenation, conservative in the catching direction: a needle split across path
    components is an assembly attempt, and a false positive is bounded by the exempt
    list while a false negative is a hole in the boundary.

    NOT folded, by the nature of a static check: anything with a non-constant part --
    a variable, an attribute read, a computed component, a runtime format value.
    Runtime assembly is statically unclosable; the disclosure lives in this section's
    header and the module docstring, and the run-time chokepoint is the layer that
    holds regardless of how a path string was assembled.
    """
    out: set[str] = set()
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        out.add(node.value)
    elif isinstance(node, ast.BinOp):
        lefts = _fold_candidates(node.left)
        rights = _fold_candidates(node.right)
        if isinstance(node.op, ast.Add):
            out |= {left + right for left in lefts for right in rights}
        elif isinstance(node.op, ast.Div):
            # pathlib-style joining over constants: both the "/"-joined path form and
            # the separator-less concatenation are candidates.
            for left in lefts:
                for right in rights:
                    out.add(f"{left}/{right}")
                    out.add(left + right)
        elif isinstance(node.op, ast.Mod):
            operand_tuples: list[tuple[str, ...]] = []
            if isinstance(node.right, ast.Tuple):
                element_sets = [_fold_candidates(element) for element in node.right.elts]
                if all(element_sets):
                    operand_tuples = [tuple(chosen) for chosen in _bounded_product(element_sets)]
            else:
                operand_tuples = [(value,) for value in _fold_candidates(node.right)]
            for template in lefts:
                for values in operand_tuples:
                    try:
                        out.add(template % (values if len(values) != 1 else values[0]))
                    except (TypeError, ValueError, KeyError):
                        continue
    elif isinstance(node, ast.JoinedStr):
        out.add(
            "".join(
                value.value
                for value in node.values
                if isinstance(value, ast.Constant) and isinstance(value.value, str)
            )
        )
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and not node.keywords:
        receiver_strings = _fold_candidates(node.func.value)
        arg_sets = [_fold_candidates(arg) for arg in node.args]
        if (
            node.func.attr == "join"
            and receiver_strings
            and len(node.args) == 1
            and isinstance(node.args[0], ast.List | ast.Tuple)
        ):
            element_sets = [_fold_candidates(element) for element in node.args[0].elts]
            if all(element_sets):
                for separator in receiver_strings:
                    for chosen in _bounded_product(element_sets):
                        out.add(separator.join(chosen))
        elif node.func.attr in ("join", "joinpath") and node.args and all(arg_sets):
            # os.path.join / posixpath.join / PurePath.joinpath shape: the receiver is
            # a module or path object (not a constant string); fold the args.
            for chosen in _bounded_product(arg_sets):
                out.add("/".join(chosen))
                out.add("".join(chosen))
        elif node.func.attr == "format" and receiver_strings and all(arg_sets):
            for template in receiver_strings:
                for chosen in _bounded_product(arg_sets):
                    try:
                        out.add(template.format(*chosen))
                    except (IndexError, KeyError, ValueError):
                        continue
    return out


def _bounded_product(element_sets: list[set[str]]) -> list[tuple[str, ...]]:
    """Cartesian product of candidate sets, capped at `_FOLD_CANDIDATE_CAP` combos."""
    combos: list[tuple[str, ...]] = [()]
    for candidates in element_sets:
        combos = [(*combo, candidate) for combo in combos for candidate in sorted(candidates)][
            :_FOLD_CANDIDATE_CAP
        ]
        if not combos:
            return []
    return combos


def _source_holds_literal(source: str, origin: object) -> bool:
    """True when `source` names the restricted root, textually or by constant folding.

    Calls the shared R-27 helper on a source that will not parse: an unparseable file
    is a failure, never a pass. Catches the textual literal, DISC-2's
    ``+``-concatenation, and the constant-only call forms `_fold_candidates`
    enumerates; does NOT catch runtime assembly, which is statically unclosable and
    disclosed as this scan's named residual.
    """
    if _LITERAL in source:
        return True
    try:
        tree = ast.parse(source, filename=str(origin))
    except (SyntaxError, ValueError) as exc:
        fail_unparseable(origin, f"not parseable as Python: {exc}")
        raise AssertionError("unreachable: fail_unparseable always raises") from exc
    for node in ast.walk(tree):
        for folded in _fold_candidates(node):
            if _LITERAL in folded:
                return True
    return False


def _notebook_cell_sources(path: Path) -> Iterator[tuple[str, str]]:
    """Yield (origin, python_source) per code cell, magics/shell lines dropped."""
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
        cells = loaded["cells"]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        fail_unparseable(path, f"not parseable as a notebook: {exc}")
        raise AssertionError("unreachable: fail_unparseable always raises") from exc
    for index, cell in enumerate(cells):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        kept = [
            line
            for line in source.splitlines()
            if not line.lstrip().startswith(_NOTEBOOK_NON_PYTHON_PREFIXES)
        ]
        identity = (
            path.relative_to(REPO_ROOT).as_posix()
            if path.is_relative_to(REPO_ROOT)
            else path.as_posix()
        )
        yield f"{identity}::cell[{index}]", "\n".join(kept)


def _literal_holders() -> set[str]:
    """Every module (and notebook) under the scan width that names the restricted root."""
    holders: set[str] = set()
    for tree_name in ("src", "tests", "scripts"):
        base = REPO_ROOT / tree_name
        if not base.is_dir():
            continue
        for module in sorted(base.rglob("*.py")):
            try:
                text = module.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                fail_unparseable(module, str(exc))
                raise AssertionError("unreachable: fail_unparseable always raises") from exc
            if _source_holds_literal(text, module):
                holders.add(module.relative_to(REPO_ROOT).as_posix())
    notebooks = REPO_ROOT / "notebooks"
    if notebooks.is_dir():
        for notebook in sorted(notebooks.rglob("*.ipynb")):
            for origin, source in _notebook_cell_sources(notebook):
                if _source_holds_literal(source, origin):
                    holders.add(notebook.relative_to(REPO_ROOT).as_posix())
    return holders


def test_restricted_literal_holders_are_exactly_the_enumerated_exemption() -> None:
    """R-28 as ruled 2026-08-28: exact list membership, never a substring exemption.

    The exemption exists because test modules must be able to assert *where the boundary
    is*. It covers holding the **literal**; it never covers obtaining the **content**.
    Asserted in BOTH directions: an unlisted holder fails (the one-door property does
    not weaken slightly; it ends), and a listed module that no longer holds the literal
    fails until the list is edited under review, so the list cannot rot in either
    direction.
    """
    holders = _literal_holders()
    exempt = set(RESTRICTED_LITERAL_EXEMPT_MODULES)

    unexpected = holders - exempt
    assert not unexpected, (
        f"modules outside R-28's enumerated exemption contain the restricted-root "
        f"literal: {sorted(unexpected)}. The one-door property does not weaken slightly; "
        f"it ends."
    )
    stale = exempt - holders
    assert not stale, (
        f"exempt modules no longer hold the restricted-root literal: {sorted(stale)}. "
        f"A listed module that stops needing the literal fails the membership check "
        f"until the list is edited -- the exemption cannot be narrowed into falsehood "
        f"silently (R-28)."
    )


def test_exempt_list_membership_is_rederived_exactly() -> None:
    """DISC-1 / review-Minor closure: the seven on-disk members, re-derived line by line.

    The nfr-design READY pass recorded that the seven-member claim was spot-checked
    rather than re-derived under its tool budget. This test IS that re-derivation, and
    it fails on any addition OR removal: the expected set is enumerated here literally,
    never imported from the constant it checks (that would be circular). The prose
    count of six (five members plus the chokepoint) stays a gate item for the
    documents; the code asserts the true seven.
    """
    expected = {
        # the chokepoint itself
        "src/data/locked_test.py",
        # the one production script legitimately merging the locked month (D-18)
        "scripts/merge_coverage_year.py",
        # the four tests/ modules the 2026-08-28 rulings enumerated
        "tests/test_acquisition_window.py",
        "tests/test_phase_boundary.py",
        "tests/test_release_hashes.py",
        "tests/test_locked_test_guard.py",
        # the seventh holder, caught by this file's membership assertion on first run
        # (the behaviour R-28 specifies: a new holder fails, never silently admitted)
        "tests/test_merge_script_restricted_reads.py",
    }
    assert len(expected) == 7
    assert set(RESTRICTED_LITERAL_EXEMPT_MODULES) == expected, (
        f"RESTRICTED_LITERAL_EXEMPT_MODULES drifted from the seven ruled members: "
        f"added {sorted(set(RESTRICTED_LITERAL_EXEMPT_MODULES) - expected)}, "
        f"removed {sorted(expected - set(RESTRICTED_LITERAL_EXEMPT_MODULES))}. "
        f"Every membership change is a reviewed edit (SD-G-03)."
    )


def test_concatenated_literal_is_caught_by_constant_folding(tmp_path: Path) -> None:
    """DISC-2's negative control: the exact evasion Q2 = B was chosen to close.

    ``EVIDENCE_DIR / ("locked_test" + "_restricted")`` never contains the joined
    string in its source text, so the superseded substring scan could not see it.
    The folded AST scan must.
    """
    snippet = tmp_path / "evader.py"
    snippet.write_text(
        "from pathlib import Path\n"
        'EVIDENCE_DIR = Path("evidence")\n'
        'SNEAKY = EVIDENCE_DIR / ("locked_test" + "_restricted")\n',
        encoding="utf-8",
    )
    source = snippet.read_text(encoding="utf-8")
    assert _LITERAL not in source, "control is invalid: the joined literal appears verbatim"
    assert _source_holds_literal(source, snippet), (
        "the constant-folding scan missed a concatenated restricted-root literal -- "
        "DISC-2's evasion is open again"
    )


@pytest.mark.parametrize(
    ("form", "snippet"),
    [
        (
            "os.path.join over constant args",
            'import os\nSNEAKY = os.path.join("locked_test", "_restricted")\n',
        ),
        (
            "%-format with constant operands",
            'SNEAKY = "%s_restricted" % "locked_test"\n',
        ),
        (
            "%-format with a constant tuple",
            'SNEAKY = "%s_%s" % ("locked_test", "restricted")\n',
        ),
        (
            "str.join over a constant-element list",
            'SNEAKY = "".join(["locked_test", "_restricted"])\n',
        ),
        (
            "str.format with constant args",
            'SNEAKY = "{}_restricted".format("locked_test")\n',
        ),
        (
            "pathlib-style / over constants",
            'SNEAKY = "evidence/locked_test" / "_restricted"\n',
        ),
        (
            "joinpath over constant args",
            "from pathlib import Path\n"
            'SNEAKY = Path("evidence").joinpath("locked_test", "_restricted")\n',
        ),
    ],
)
def test_constant_only_call_assembly_is_caught(form: str, snippet: str) -> None:
    """The reviewer-proved call-form evasions (iteration-1 Major 1), each now caught.

    Every snippet assembles the restricted-root literal from constants without the
    joined text ever appearing contiguously in source. Each is a negative control for
    one folded form; the joined-form candidates include the separator-less
    concatenation deliberately (a needle split across path components is an assembly
    attempt).
    """
    assert _LITERAL not in snippet, f"control invalid for {form}: literal appears verbatim"
    assert _source_holds_literal(
        snippet, f"<{form}>"
    ), f"constant-only call assembly escaped the folding scan: {form}"


def test_runtime_assembly_residual_is_disclosed_where_the_scan_lives() -> None:
    """The residual is NAMED, not implied closed (iteration-1 Major 1, part b).

    Runtime assembly -- any non-constant component -- is statically unclosable, and
    the module must say so where the scan lives. This test fails the day the
    disclosure is removed, exactly like the subordinate-status documentation test.
    """
    docstring = ast.get_docstring(ast.parse(Path(__file__).read_text(encoding="utf-8"))) or ""
    assert (
        "statically unclosable" in docstring
    ), "the runtime-assembly residual disclosure left the module docstring"
    # And the residual really is a residual: a runtime-fed assembly is NOT caught.
    runtime_snippet = 'import sys\nSNEAKY = "locked_" + sys.argv[1] + "_restricted"\n'
    assert not _source_holds_literal(runtime_snippet, "<runtime assembly>"), (
        "a runtime-fed assembly was reported caught; if the scan has genuinely widened, "
        "update the disclosure rather than deleting this control"
    )


def test_unparseable_python_is_a_failure_not_a_pass(tmp_path: Path) -> None:
    """R-27 via the shared helper: a file the scan cannot parse is a failure."""
    snippet = tmp_path / "broken.py"
    snippet.write_text("def broken(:\n    pass\n", encoding="utf-8")
    with pytest.raises(EvidenceScanError) as excinfo:
        _source_holds_literal(snippet.read_text(encoding="utf-8"), snippet)
    assert "failure" in str(excinfo.value)


def test_notebook_code_cells_are_scanned(tmp_path: Path) -> None:
    """The scan's declared width includes notebook code cells (magics dropped)."""
    notebook = tmp_path / "notebooks" / "evader.ipynb"
    notebook.parent.mkdir()
    notebook.write_text(
        json.dumps(
            {
                "cells": [
                    {"cell_type": "markdown", "source": ["# prose only\n"]},
                    {
                        "cell_type": "code",
                        "source": [
                            "%matplotlib inline\n",
                            "from pathlib import Path\n",
                            'ROOT = Path("evidence") / ("locked_test" + "_restricted")\n',
                        ],
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    hits = [
        origin
        for origin, source in _notebook_cell_sources(notebook)
        if _source_holds_literal(source, origin)
    ]
    assert hits, "a concatenated restricted-root literal in a notebook code cell was missed"


def test_unparseable_notebook_is_a_failure(tmp_path: Path) -> None:
    """R-27 reaches the notebook limb of the scan too."""
    notebook = tmp_path / "broken.ipynb"
    notebook.write_text("{not json", encoding="utf-8")
    with pytest.raises(EvidenceScanError):
        list(_notebook_cell_sources(notebook))


# --- 6. the residency scan shares the same fail-closed rule -----------------------------


def test_december_bearing_json_outside_the_restricted_root_is_found(tmp_path: Path) -> None:
    """The residency scan's positive control, against a synthetic evidence root."""
    evidence = tmp_path / "evidence"
    (evidence / "locked_test_restricted").mkdir(parents=True)
    inside = evidence / "locked_test_restricted" / "december.json"
    inside.write_text('{"interval_start_utc": "2022-12-01T00:00:00Z"}', encoding="utf-8")
    escaped = evidence / "summary" / "escaped.json"
    escaped.parent.mkdir()
    escaped.write_text('{"interval_start_utc": "2022-12-05T10:00:00Z"}', encoding="utf-8")
    clean = evidence / "summary" / "clean.json"
    clean.write_text('{"interval_start_utc": "2022-11-05T10:00:00Z"}', encoding="utf-8")

    offenders = assert_no_december_outside_restricted(evidence)
    assert [p.name for p in offenders] == ["escaped.json"], (
        "the residency scan must flag exactly the December-bearing artifact outside "
        "the restricted root -- not the one inside it, not the clean one"
    )


def test_r26_driver_exclusions_are_exactly_five_and_content_gated(tmp_path: Path) -> None:
    """G-4 (2026-09-19) + D-48: R-26's four enumerated driver exclusions plus the class 5
    the project decision owner adopted for the GFZ captures. (i) the enumeration is
    pinned at EXACTLY five classes with exact path patterns; (ii) eligibility needs BOTH
    the class path AND content that validates as that class's driver-only schema: a
    target-bearing or mixed JSON at an excluded path is still flagged, as is any
    December-bearing JSON outside the classes; (iii) the real evidence tree scans clean
    with every excluded file INVENTORIED with its reason (exposure, never a licence)."""
    assert [c[0] for c in DECEMBER_DRIVER_EXCLUSION_CLASSES] == [1, 2, 3, 4, 5]
    assert [c[2] for c in DECEMBER_DRIVER_EXCLUSION_CLASSES] == [
        ("audit_ec1_2026-08-15/kyoto_dst/dst_provisional_*.html",),
        ("audit_ec1_2026-08-15/nrcan_f107/fluxtable.txt",),
        ("audit_ec1_2026-08-15/ec1-audit-report.json",),
        ("audit_ec1_2026-08-15/kyoto_dst/.dst_summary.json",),
        (
            "audit_gfz_*/Kp_*.wdc",
            "audit_gfz_*/hp60ap60doi_*.txt",
            "audit_gfz_*/gfz-comparison-report.json",
        ),
    ]
    evidence = tmp_path / "evidence"
    (evidence / "locked_test_restricted").mkdir(parents=True)
    ec1 = evidence / "audit_ec1_2026-08-15"
    (ec1 / "kyoto_dst").mkdir(parents=True)
    # driver-only content at the class-3 path: excluded
    (ec1 / "ec1-audit-report.json").write_text(
        '{"obligation_2_canadian_f107": {"last_2022_date": "2022-12-31", "days_present_2022": 365}}',
        encoding="utf-8",
    )
    # driver-only content at the class-4 path: excluded
    (ec1 / "kyoto_dst" / ".dst_summary.json").write_text(
        '{"12": {"days_parsed": 31, "daily_min": {"2022-12-01": -30}}}', encoding="utf-8"
    )
    assert assert_no_december_outside_restricted(evidence) == []
    # MIXED content at the class-3 path (a target aggregate rides along): flagged
    (ec1 / "ec1-audit-report.json").write_text(
        '{"obligation_2_canadian_f107": {"last_2022_date": "2022-12-31"},'
        ' "december_coverage_pct": 96.4}',
        encoding="utf-8",
    )
    assert [p.name for p in assert_no_december_outside_restricted(evidence)] == [
        "ec1-audit-report.json"
    ]
    (ec1 / "ec1-audit-report.json").write_text(
        '{"obligation_2_canadian_f107": {"last_2022_date": "2022-12-31"}, "vtec_tecu": [1.0]}',
        encoding="utf-8",
    )
    assert [p.name for p in assert_no_december_outside_restricted(evidence)] == [
        "ec1-audit-report.json"
    ]
    # a December-bearing JSON anywhere OUTSIDE the four classes: flagged, driver or not
    (ec1 / "kyoto_dst" / "dst_extract.json").write_text('{"hour": "2022-12-05T10:00:00Z"}')
    gfz = evidence / "audit_gfz_2026-09-18"
    gfz.mkdir()
    (gfz / "driver_epochs.json").write_text('{"epoch": "2022-12-05T03:00:00Z", "kp": 2.0}')
    (ec1 / "ec1-audit-report.json").write_text(
        '{"obligation_2_canadian_f107": {"last_2022_date": "2022-12-31"}}', encoding="utf-8"
    )
    flagged = sorted(p.name for p in assert_no_december_outside_restricted(evidence))
    assert flagged == ["driver_epochs.json", "dst_extract.json"]
    # the REAL evidence tree: clean, and every December-bearing file is inventoried
    assert assert_no_december_outside_restricted(REPO_ROOT / "evidence") == []
    assert december_driver_exclusion_class(
        REPO_ROOT / "evidence" / "audit_ec1_2026-08-15" / "ec1-audit-report.json",
        REPO_ROOT / "evidence",
    ) == (3, "Derived driver audit report")
    inventory = december_custody_inventory(REPO_ROOT / "evidence")
    excluded = {e.path: e.exclusion_class for e in inventory if e.disposition == "excluded"}
    assert excluded == {
        "audit_ec1_2026-08-15/ec1-audit-report.json": 3,
        "audit_ec1_2026-08-15/kyoto_dst/.dst_summary.json": 4,
        "audit_ec1_2026-08-15/kyoto_dst/dst_provisional_202211.html": 1,
        "audit_ec1_2026-08-15/nrcan_f107/fluxtable.txt": 2,
        "audit_gfz_2026-09-18/Kp_def2022.wdc": 5,
        "audit_gfz_2026-09-18/Kp_now2022.wdc": 5,
        "audit_gfz_2026-09-18/gfz-comparison-report.json": 5,
        "audit_gfz_2026-09-18/hp60ap60doi_2022_v2.txt": 5,
        "audit_gfz_2026-09-18/hp60ap60doi_2022_v3.txt": 5,
    }
    assert all(e.reason for e in inventory if e.disposition == "excluded")
    outside = {e.path for e in inventory if e.disposition == "outside_automated_inspection"}
    assert outside == {
        "CORRECTION_2026-08-16_acquisition_window.md",
        "DECISIONS.md",
        "experiment_registry.md",
        "audit_ec1_2026-08-15/EC1-AUDIT.md",
        "audit_gfz_2026-09-18/GFZ-AUDIT.md",
        # 2026-09-19: the returned IRI-2016 Kaggle verification bundle's return record and
        # its validation README (prose; no December target content -- the JSON/py files
        # beside them are inside automated inspection and pass it).
        "iri2016_kaggle_verification_2026-09-19/RETURN_RECORD.md",
        "iri2016_kaggle_verification_2026-09-19/validation/README.md",
        # 2026-09-20, first execution of this suite under the governed 3.11 pin: the
        # Recommendation 1 remediation added the supersession notice beside the closed
        # access log. It lands here because it is a Markdown record, which is the
        # disposition every `.md` above carries -- not because of its content: derived
        # 2026-09-20 and printed before assertion, it matches `vtec|tecu` 0 times and
        # carries no `2022-12-DD` date at all. The closed log it describes is itself
        # unmodified (5,964 rows, sha256 985f0671..., verified before and after this run).
        "test_run_access_log.SUPERSEDED_2026-09-20.md",
    }
    assert not [e for e in inventory if e.disposition == "flagged"]


def test_december_detection_is_structural_not_lexical(tmp_path: Path) -> None:
    """P-4a (D-48): December is detected by STRUCTURE — integer `{y, m}` records at any
    depth, month-number keys, compact `202212` literals, WDC and Hpo line layouts, isprint
    endpoint epochs and Madrigal `ut1_unix` epochs — so an encoding chosen to dodge a
    quoted-literal scan no longer passes. Each shape is flagged when no class covers it."""
    evidence = tmp_path / "evidence"
    (evidence / "locked_test_restricted").mkdir(parents=True)
    other = evidence / "other"
    other.mkdir()
    (other / "int_keys.json").write_text(
        '{"epochs": [{"y": 2022, "m": 11, "d": 30, "h": 23}, {"y": 2022, "m": 12, "d": 1, "h": 0}]}'
    )
    (other / "month_keys.json").write_text('{"1": {"n": 31}, "12": {"n": 31}}')
    (other / "compact.json").write_text('{"stamp": "20221201"}')
    (other / "nested_year_month.json").write_text(
        '{"a": {"b": [{"year": "2022", "month": "12", "v": 1.0}]}}'
    )
    (other / "records.wdc").write_text("# header\n2212 1" + "0" * 60 + "\n")
    (other / "hp60ap60doi_x.txt").write_text(
        "# h\n2022 12 01 00.0 00.50 33207.00000 33207.02083  1.667    6 0\n"
    )
    cache = other / "raw_isprint_cache"
    cache.mkdir()
    (cache / "day.txt").write_text(
        "1669852800.000  32.0 33.0 1.0 0.1\n1669939200.000  32.0 33.0 1.0 0.1\n"
    )
    (other / "records.csv").write_text("ut1_unix,tec\n1669856400.0,5.0\n")
    (other / "november.csv").write_text("ut1_unix,tec\n1667260800.0,5.0\n")
    (other / "notes.md").write_text("December 2022 is the locked month.\n")
    flagged = sorted(p.name for p in assert_no_december_outside_restricted(evidence))
    assert flagged == [
        "compact.json",
        "day.txt",
        "hp60ap60doi_x.txt",
        "int_keys.json",
        "month_keys.json",
        "nested_year_month.json",
        "records.csv",
        "records.wdc",
    ]
    rows = {e.path: e for e in december_custody_inventory(evidence)}
    assert rows["other/notes.md"].disposition == "outside_automated_inspection"
    assert rows["other/november.csv"].disposition == "no_december_content"
    assert rows["other/raw_isprint_cache/day.txt"].detection == "isprint-endpoint"


def _gfz_fixture(evidence: Path) -> Path:
    """A synthetic `audit_gfz_*` directory whose files satisfy class 5's content AND
    provenance conditions (sha256 recorded in a sibling retrieval record)."""
    import hashlib as _hashlib
    import json as _json

    gfz = evidence / "audit_gfz_2030-01-01"
    gfz.mkdir(parents=True)
    wdc = gfz / "Kp_now2022.wdc"
    wdc.write_text("# DOI\n2212 1" + "0" * 60 + "\n", encoding="utf-8")
    hpo = gfz / "hp60ap60doi_2022_v2.txt"
    hpo.write_text(
        "# h\n2022 12 01 00.0 00.50 33207.00000 33207.02083  1.667    6 0\n", encoding="utf-8"
    )
    report = gfz / "gfz-comparison-report.json"
    report.write_text(
        _json.dumps(
            {
                "run_id": "r1",
                "december_custody": "driver records only",
                "provider_limitations": {"kp_ap3": "settled nowcast"},
                "validation": {"Kp_now2022.wdc": {"coverage": "2920 epochs"}},
                "comparisons": {
                    "kp_ap3": {"differing_epochs": [{"y": 2022, "m": 12, "d": 1, "h": 0}]}
                },
            }
        ),
        encoding="utf-8",
    )
    (gfz / "retrieval_record.json").write_text(
        _json.dumps(
            {
                "run_id": "r1",
                "provider_files": [
                    {"logical_name": p.name, "sha256": _hashlib.sha256(p.read_bytes()).hexdigest()}
                    for p in (wdc, hpo)
                ],
            }
        ),
        encoding="utf-8",
    )
    return gfz


def test_class_5_excludes_only_validated_driver_captures_with_provenance(tmp_path: Path) -> None:
    """D-48's conditions as negative controls: (a) the validated fixture is excluded and
    inventoried; (b) a target key inside the report → flagged; (c) a `y` outside an epoch
    key or a `coverage` outside `validation` → flagged; (d) an extra column in a raw
    line → flagged; (e) a raw file whose sha256 is not in the retrieval record, or no
    retrieval record at all → flagged; (f) a prediction file placed in the directory →
    flagged. The directory name alone never qualifies."""
    import json as _json

    evidence = tmp_path / "evidence"
    (evidence / "locked_test_restricted").mkdir(parents=True)
    gfz = _gfz_fixture(evidence)
    assert assert_no_december_outside_restricted(evidence) == []
    inv = {e.path: e for e in december_custody_inventory(evidence)}
    assert inv["audit_gfz_2030-01-01/Kp_now2022.wdc"].exclusion_class == 5
    assert "exposure recorded" in inv["audit_gfz_2030-01-01/gfz-comparison-report.json"].reason
    # (b) target key in the report
    report = gfz / "gfz-comparison-report.json"
    good = _json.loads(report.read_text(encoding="utf-8"))
    bad = dict(good)
    bad["comparisons"] = {
        "kp_ap3": {"vtec_tecu": [1.0], "differing_epochs": [{"y": 2022, "m": 12, "d": 1, "h": 0}]}
    }
    report.write_text(_json.dumps(bad), encoding="utf-8")
    assert [p.name for p in assert_no_december_outside_restricted(evidence)] == [
        "gfz-comparison-report.json"
    ]
    # (c) y outside an epoch key; coverage outside validation
    bad = dict(good)
    bad["comparisons"] = {
        "kp_ap3": {"y": [1.0, 2.0], "epoch": {"y": 2022, "m": 12, "d": 1, "h": 0}}
    }
    report.write_text(_json.dumps(bad), encoding="utf-8")
    assert [p.name for p in assert_no_december_outside_restricted(evidence)] == [
        "gfz-comparison-report.json"
    ]
    bad = dict(good)
    bad["comparisons"] = {
        "kp_ap3": {"coverage": 0.96, "epoch": {"y": 2022, "m": 12, "d": 1, "h": 0}}
    }
    report.write_text(_json.dumps(bad), encoding="utf-8")
    assert [p.name for p in assert_no_december_outside_restricted(evidence)] == [
        "gfz-comparison-report.json"
    ]
    report.write_text(_json.dumps(good), encoding="utf-8")
    assert assert_no_december_outside_restricted(evidence) == []
    # (d) an extra column in a raw Hpo line
    hpo = gfz / "hp60ap60doi_2022_v2.txt"
    original = hpo.read_bytes()
    hpo.write_text(
        "# h\n2022 12 01 00.0 00.50 33207.00000 33207.02083  1.667    6 0 7.5\n", encoding="utf-8"
    )
    assert [p.name for p in assert_no_december_outside_restricted(evidence)] == [
        "hp60ap60doi_2022_v2.txt"
    ]
    hpo.write_bytes(original)
    assert assert_no_december_outside_restricted(evidence) == []
    # (e) bytes not matching the recorded sha256; then no retrieval record at all
    wdc = gfz / "Kp_now2022.wdc"
    original = wdc.read_bytes()
    wdc.write_text("# DOI\n2212 2" + "0" * 60 + "\n", encoding="utf-8")
    assert [p.name for p in assert_no_december_outside_restricted(evidence)] == ["Kp_now2022.wdc"]
    wdc.write_bytes(original)
    record = gfz / "retrieval_record.json"
    saved = record.read_bytes()
    record.unlink()
    assert sorted(p.name for p in assert_no_december_outside_restricted(evidence)) == [
        "Kp_now2022.wdc",
        "gfz-comparison-report.json",
        "hp60ap60doi_2022_v2.txt",
    ]
    record.write_bytes(saved)
    # (f) a prediction file dropped into the directory: the name never qualifies it
    (gfz / "predictions_december.json").write_text(
        '{"y_hat": [1.0], "epoch": {"y": 2022, "m": 12, "d": 1, "h": 0}}'
    )
    assert [p.name for p in assert_no_december_outside_restricted(evidence)] == [
        "predictions_december.json"
    ]


def test_unreadable_evidence_file_fails_the_residency_scan(tmp_path: Path) -> None:
    """R-27's negative control on the residency scan: unreadable bytes are a failure."""
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    hostile = evidence / "hostile.json"
    hostile.write_bytes(b"\xff\xfe\x00\x00 not utf-8 \x9c")
    with pytest.raises(EvidenceScanError) as excinfo:
        assert_no_december_outside_restricted(evidence)
    assert "hostile.json" in str(excinfo.value)


# --- 7. Q1 = A: fail closed where the platform's durability is uncharacterised ----------


def test_uncharacterised_platform_is_refused_before_any_row(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """SD-G-01's design decision: refuse, no read, no access row consumed.

    Kaggle's fsync semantics are characterised nowhere in this project, and
    `CHARACTERISED_DURABILITY_PLATFORMS` is empty until W-6 step 8's measurement, so
    a kaggle-labelled process is refused fail-closed. The stated, accepted cost is
    blocking the pre-G-05 December coverage audit on Kaggle until the measurement.
    """
    monkeypatch.setenv("TEC_PLATFORM", "kaggle")
    registry = tmp_path / "access.jsonl"
    with pytest.raises(LockedTestError) as excinfo:
        open_restricted(RESTRICTED_DIR / "anything.json", record=_record(), registry=registry)
    assert "uncharacterised" in str(excinfo.value)
    assert (
        not registry.exists()
    ), "a refused platform consumed an access row; the refusal must precede the append"


def test_local_platform_keeps_its_designed_behaviour(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The refusal targets the governed audit host, not local development.

    Per the design's scheduling note, `local` keeps its behaviour: foundation SD-03's
    unverified-durability stamp already disqualifies local rows as freeze-gate
    evidence, so refusing here would buy nothing and would break fixture runs and
    review, which TC-03c assigns to local.
    """
    monkeypatch.setenv("TEC_PLATFORM", "local")
    target = _any_restricted_file()
    if target is None:
        pytest.skip("no restricted artifact present to guard")
    registry = tmp_path / "access.jsonl"
    returned = open_restricted(target, record=_record(), registry=registry)
    assert returned == target.resolve()
    assert registry.is_file(), "the local read must still be logged before it happens"


# --- 8. SD-G-02: the AccessRecord <-> RegistryEvent join, wired against foundation ------
#
# Foundation's `reconcile_access_records` owns the both-way reconciliation as a PURE
# READ with a `known_orphans` parameter; these tests wire this unit's AccessRecord
# against it and do not redesign it. The six known pre-guard orphans of the real log
# (the five retrospective December accesses, rows 3, 4, 5, 8 and 9 of
# `evidence/experiment_registry.md`, plus GOV-2026-08-28-FD-01 Recommendation 31's
# expressly unresolved access) are represented here by synthetic run_ids of the same
# SHAPE: these tests exercise the mechanism against synthetic logs only and read no
# December content.

_KNOWN_PRE_GUARD_ORPHANS = {
    "retro-row-3": "retrospective pre-guard access (experiment_registry.md row 3)",
    "retro-row-4": "retrospective pre-guard access (experiment_registry.md row 4)",
    "retro-row-5": "retrospective pre-guard access (experiment_registry.md row 5)",
    "retro-row-8": "retrospective pre-guard access (experiment_registry.md row 8)",
    "retro-row-9": "retrospective pre-guard access (experiment_registry.md row 9)",
    "rec-31-unresolved": (
        "possible unauthorized access GOV-2026-08-28-FD-01 Recommendation 31 records "
        "as expressly unresolved"
    ),
}


def _access_row(run_id: str) -> str:
    return json.dumps(
        {
            "run_id": run_id,
            "retrieved_at_utc": "2026-08-01T00:00:00+00:00",
            "scope": "December 2022, ARUC/BSHM/NICO cells",
            "purpose": "coverage_audit",
            "performance_inspected": False,
            "locked_test_accessed": True,
            "authorization": "Vision 8.3 performance-blind coverage audit",
            "logged_at_utc": "2026-08-01T00:00:00+00:00",
        },
        sort_keys=True,
    )


def _registry_row(run_id: str, *, locked_test_accessed: bool) -> dict[str, object]:
    row: dict[str, object] = {column: "" for column in REGISTRY_COLUMNS}
    row.update(
        run_id=run_id,
        started_at_utc="2026-09-05T00:00:00+00:00",
        status="started",
        code_commit="deadbeef",
        environment_lock_hash="cafef00d",
        platform="local",
        locked_test_accessed=locked_test_accessed,
    )
    return row


def test_reconciliation_reports_known_orphans_and_mutates_neither_log(
    tmp_path: Path,
) -> None:
    """Both-way orphan detection runs; known pre-guard orphans are reported, never
    back-filled; both logs are byte-identical after the reconciliation (pure read)."""
    access_log = tmp_path / "access.jsonl"
    registry = tmp_path / "registry.jsonl"

    lines = [_access_row(run_id) for run_id in sorted(_KNOWN_PRE_GUARD_ORPHANS)]
    lines.append(_access_row("run-joined"))
    access_log.write_text("\n".join(lines) + "\n", encoding="utf-8")

    append_registry_event(
        registry,
        _registry_row("run-joined", locked_test_accessed=True),
        phase=1,
        writer_role="stage",
        access_log_path=access_log,
    )

    access_before = access_log.read_bytes()
    registry_before = registry.read_bytes()

    report = reconcile_access_records(registry, access_log, known_orphans=_KNOWN_PRE_GUARD_ORPHANS)

    assert set(report.expected_orphans) == set(
        _KNOWN_PRE_GUARD_ORPHANS
    ), "every known pre-guard orphan must be REPORTED with its reason, not cleared"
    assert report.access_rows == 7
    assert (
        access_log.read_bytes() == access_before
    ), "the reconciliation wrote to the access log; it is specified as a pure read"
    assert registry.read_bytes() == registry_before, (
        "the reconciliation back-filled the registry; a back-filled row to clear an "
        "orphan is the reconstruction failure repeated deliberately (R-19, NFR-AUD-01)"
    )


def test_unknown_access_orphan_is_an_integrity_failure(tmp_path: Path) -> None:
    """An access row no registry run and no known-orphan entry explains must raise."""
    access_log = tmp_path / "access.jsonl"
    registry = tmp_path / "registry.jsonl"
    access_log.write_text(_access_row("ghost-run") + "\n", encoding="utf-8")
    with pytest.raises(RegistryError) as excinfo:
        reconcile_access_records(registry, access_log, known_orphans=_KNOWN_PRE_GUARD_ORPHANS)
    assert "ghost-run" in str(excinfo.value)


def test_registry_claim_without_access_row_is_an_integrity_failure(tmp_path: Path) -> None:
    """The other direction: `locked_test_accessed = true` with no logged access."""
    access_log = tmp_path / "access.jsonl"
    registry = tmp_path / "registry.jsonl"
    append_registry_event(
        registry,
        _registry_row("phantom-run", locked_test_accessed=True),
        phase=1,
        writer_role="stage",
        access_log_path=access_log,
    )
    with pytest.raises(RegistryError) as excinfo:
        reconcile_access_records(registry, access_log, known_orphans=_KNOWN_PRE_GUARD_ORPHANS)
    assert "phantom-run" in str(excinfo.value)


# --- 9. LIMB 1 (features-and-splits): the EXECUTION block on the locked partition -------
#
# ADR-03's other limb, owned by `features-and-splits` (nfr-design Q3 = C placed its cases
# here rather than in a new module, keeping TE 12's mandated tree unchanged). Every case
# runs over `test_split_embargo.py`'s SYNTHETIC partition fixture (a synthetic calendar
# year): no December 2022 content, no restricted-root path, no real signature. The
# repository's `configs/data.yaml` carries no `gates.G-05` record, so no real signature can
# verify today, and none is supplied anywhere in this module.

_TESTS_DIR = Path(__file__).resolve().parent
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

import hashlib  # noqa: E402

from src.data.config import PartitionError  # noqa: E402
from src.data.splits import (  # noqa: E402
    LOCKED_ID,
    materialise_locked_partition,
    partition_by_id,
    verify_g05_signature,
)

from test_split_embargo import (  # noqa: E402
    SYNTH_EMBARGO_HOURS,
    SYNTH_YEAR,
    synthetic_partitions,
    synthetic_snapshot,
)

_SYNTH_SIGNATURE = "synthetic G-05 signature artifact -- never a real one"


def _signed_snapshot():
    """A synthetic snapshot whose gates.G-05 record verifies `_SYNTH_SIGNATURE`."""
    return synthetic_snapshot(
        data={
            "gates": {
                "G-05": {
                    "status": "signed",
                    "decision": "D-synthetic",
                    "signature_sha256": hashlib.sha256(
                        _SYNTH_SIGNATURE.encode("utf-8")
                    ).hexdigest(),
                }
            }
        }
    )


def _synthetic_locked_loader(partition):
    """Rows over the SYNTHETIC locked month (synthetic year); stands in for a loader that,
    in production, would route through `open_restricted` (limb 2's door)."""
    assert partition.partition_id == LOCKED_ID and partition.validation_month is not None
    first = dt.datetime(
        partition.validation_month.year, partition.validation_month.month, 1, tzinfo=dt.timezone.utc
    )
    return [
        {"interval_start_utc": (first + dt.timedelta(hours=h)).isoformat(), "vtec_tecu": 1.0}
        for h in range(3 * SYNTH_EMBARGO_HOURS)
    ]


def test_limb1_signature_absent_refuses_before_any_read(monkeypatch) -> None:
    """R-82 / WS-18: `g05_signature=None` raises; the loader is never called."""
    called: list[str] = []

    def loader(partition):
        called.append(partition.partition_id)
        return []

    with pytest.raises(LockedTestError) as excinfo:
        materialise_locked_partition(synthetic_snapshot(), g05_signature=None, loader=loader)
    assert "g05_signature is None" in str(excinfo.value)
    assert "open_restricted" in str(excinfo.value)
    assert called == [], "the read limb was reached without a signature"


def test_limb1_signature_that_fails_verification_refuses() -> None:
    """A signature string with no matching signed G-05 record is no signature."""
    with pytest.raises(LockedTestError) as excinfo:
        materialise_locked_partition(
            synthetic_snapshot(), g05_signature="anything", loader=lambda p: []
        )
    assert "fails verification" in str(excinfo.value)
    with pytest.raises(LockedTestError):
        materialise_locked_partition(
            _signed_snapshot(), g05_signature="the wrong artifact", loader=lambda p: []
        )
    assert verify_g05_signature(synthetic_snapshot(), "anything") is False
    assert verify_g05_signature(_signed_snapshot(), _SYNTH_SIGNATURE) is True


def test_limb1_unsigned_or_tbd_gate_record_never_verifies() -> None:
    for status in ("pending", "Blocked", "TBD — freeze gate", ""):
        snapshot = synthetic_snapshot(
            data={
                "gates": {
                    "G-05": {
                        "status": status,
                        "decision": "D-synthetic",
                        "signature_sha256": hashlib.sha256(
                            _SYNTH_SIGNATURE.encode("utf-8")
                        ).hexdigest(),
                    }
                }
            }
        )
        assert verify_g05_signature(snapshot, _SYNTH_SIGNATURE) is False


def test_limb1_owns_no_read_path() -> None:
    """A verifying signature with NO loader still refuses: the read is limb 2's door."""
    with pytest.raises(LockedTestError) as excinfo:
        materialise_locked_partition(_signed_snapshot(), g05_signature=_SYNTH_SIGNATURE)
    assert "no loader supplied" in str(excinfo.value)


def test_limb1_verifying_signature_materialises_with_the_embargo_excluded_and_counted() -> None:
    """The positive control R-82 requires -- on synthetic dates only. The first embargo
    hours of the locked month are excluded AND counted (D-28's 30-day shape on a synthetic
    calendar)."""
    kept = materialise_locked_partition(
        _signed_snapshot(), g05_signature=_SYNTH_SIGNATURE, loader=_synthetic_locked_loader
    )
    assert len(kept) == 2 * SYNTH_EMBARGO_HOURS
    assert kept.attrs["excluded_embargo_rows"] == SYNTH_EMBARGO_HOURS
    assert kept.attrs["partition_id"] == LOCKED_ID
    dec = partition_by_id(synthetic_partitions(), LOCKED_ID)
    assert dec.validation_month is not None and dec.validation_month.year == SYNTH_YEAR


def test_limb1_rows_outside_the_locked_month_are_refused_by_timestamp() -> None:
    """Membership from record timestamps: a row from another month in the loaded frame fails
    even though the loader filed it under DEC."""

    def loader(partition):
        rows = _synthetic_locked_loader(partition)
        rows.append({"interval_start_utc": f"{SYNTH_YEAR}-11-05T00:00:00+00:00", "vtec_tecu": 1.0})
        return rows

    with pytest.raises(PartitionError):
        materialise_locked_partition(
            _signed_snapshot(), g05_signature=_SYNTH_SIGNATURE, loader=loader
        )


def test_limb1_real_configs_carry_no_g05_record() -> None:
    """The repository's own data.yaml has no gates.G-05 record: nothing verifies today, so the
    execution limb cannot open the locked partition on this checkout."""
    text = (REPO_ROOT / "configs" / "data.yaml").read_text(encoding="utf-8")
    assert "G-05" not in text or "signature_sha256" not in text


def test_limb1_splits_module_never_names_the_restricted_root() -> None:
    """R-28's one-door property survives the new module: `src/data/splits.py` is NOT an
    exempt literal holder and holds no restricted-root literal."""
    source = (REPO_ROOT / "src" / "data" / "splits.py").read_text(encoding="utf-8")
    assert "src/data/splits.py" not in RESTRICTED_LITERAL_EXEMPT_MODULES
    assert not _source_holds_literal(source, REPO_ROOT / "src" / "data" / "splits.py")


# --- 10. SD-C-02 containment fields: governance-guards' own coverage of the Q2 = B edit --
#
# OWNERSHIP. `src/data/locked_test.py` belongs to `governance-guards`. Commit `8a6cb61`
# (2026-09-07) edited it in place from `evaluation-and-comparison`'s stage 3.5 on the
# owner's explicit Q2 = B instruction, and the change record
# (`governance/CHANGE_RECORD_2026-09-06_R106_comparison_sets.md:82-85`) states verbatim
# that "`governance-guards` owes its own review of the two fields at its next touch".
# This section is that touch. It was written 2026-09-11 after two consecutive review
# passes found the edit tested only by a sibling (`tests/test_common_masks.py`), which
# exercises the CONSUMER refusal (`require_locked_receipt` on `None`) and never the
# PRODUCER that populates -- or refuses to populate -- the fields.
#
# WHAT IS NEW, AND WHY IT NEEDS A NEGATIVE CONTROL HERE. The edit adds a failure mode
# the chokepoint did not previously have: a supplied frozen-bundle manifest that EXISTS
# but cannot be read or parsed ABORTS the read, rather than recording `None` and
# proceeding. That distinction is the whole of SD-C-02's evidentiary value -- `None` is
# a legitimate, fail-closed state downstream, so silently writing `None` over a broken
# manifest would launder a defect into an ordinary refusal and destroy the signal. Every
# case below drives the violating input through `open_restricted` ITSELF, never through
# `_containment_fields` directly (project.md `nfr-design:c58`/`c59`: prove invocation per
# public entry point, because a helper proved correct once still fails open on a call
# site that forgets it).
#
# NO DECEMBER CONTENT. The boundary is a synthetic `tmp_path` tree installed through the
# module's own documented test seam (`locked_test._repo_root`); the guarded artifact and
# every manifest fixture are synthetic and carry no 2022-12 timestamp.


@pytest.fixture
def containment_boundary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """The module's SUPPORTED TEST SEAM: `_repo_root` -> `tmp_path`.

    The boundary is composed from the imported `RESTRICTED_ROOT` constant rather than
    spelled out again, and holds one synthetic artifact with no December content.
    `TEC_PLATFORM` is pinned to `local` so the Q1 = A durability refusal (section 7)
    does not pre-empt the containment path under test.
    """
    monkeypatch.setattr(locked_test, "_repo_root", lambda: tmp_path)
    monkeypatch.setenv("TEC_PLATFORM", "local")
    root = tmp_path / RESTRICTED_ROOT
    root.mkdir(parents=True, exist_ok=True)
    target = root / "synthetic_guarded_artifact.json"
    target.write_text('{"synthetic": true, "december_content": false}', encoding="utf-8")
    return target


def _manifest(path: Path, mask_ids: list[str]) -> bytes:
    """Write a frozen-bundle manifest in the producer's shape and return its exact bytes.

    The shape mirrors `src/evaluation/masks.py`'s `freeze_bundle` (sibling-owned). Only
    the `mask_ids` key is the CONSUMER contract `_containment_fields` actually reads;
    `test_containment_manifest_key_matches_the_producer` pins that key against the real
    producer statically, so this fixture cannot drift away from it unnoticed.
    """
    raw = (
        json.dumps(
            {"artifact_class": "frozen_mask_bundle_manifest", "mask_ids": mask_ids},
            sort_keys=True,
            indent=2,
        )
        + "\n"
    ).encode("utf-8")
    path.write_bytes(raw)
    return raw


#: Every way a PRESENT manifest can be unusable, one row per exception class
#: `_containment_fields` declares it catches. Each must abort, none may log `None`.
_BROKEN_MANIFESTS: list[tuple[str, bytes]] = [
    ("not JSON at all", b"{not json at all"),
    ("valid JSON, no mask_ids key", b'{"artifact_class": "frozen_mask_bundle_manifest"}'),
    ("mask_ids is not iterable", b'{"mask_ids": 5}'),
    ("top-level JSON is a list, not an object", b"[1, 2]"),
    ("bytes are not UTF-8", b"\xff\xfe\x00\x00 not utf-8 \x9c"),
    ("empty file", b""),
]


@pytest.mark.parametrize(("label", "payload"), _BROKEN_MANIFESTS)
def test_containment_present_but_unparseable_manifest_aborts_the_read(
    containment_boundary: Path, tmp_path: Path, label: str, payload: bytes
) -> None:
    """THE new failure mode, driven through the real entry point: abort, never log `None`.

    A present-but-broken manifest is exactly the case where recording `None` would be
    indistinguishable from the legitimate no-manifest state that `require_locked_receipt`
    refuses on -- the defect would arrive downstream wearing the costume of an ordinary
    fail-closed refusal. Asserted in three parts, because any one alone is passable by a
    weaker implementation: the call RAISES, no access row is consumed, and the message
    names the offending manifest rather than failing anonymously.
    """
    manifest = tmp_path / "broken_manifest.json"
    manifest.write_bytes(payload)
    registry = tmp_path / "access.jsonl"

    with pytest.raises(LockedTestError) as excinfo:
        open_restricted(
            containment_boundary,
            record=_record(),
            registry=registry,
            mask_bundle_manifest=manifest,
        )

    message = str(excinfo.value)
    assert "cannot be read or parsed" in message, (
        f"the abort for {label!r} did not say the manifest was unreadable; a guard that "
        f"refuses anonymously cannot be acted on by the reviewer who reads the failure"
    )
    assert manifest.name in message, f"the refusal for {label!r} does not name the manifest"
    assert not registry.exists(), (
        f"a broken manifest ({label}) consumed an access row; the containment read must "
        f"abort BEFORE the append, or a refused read leaves a phantom row behind"
    )


def test_containment_abort_leaves_an_existing_access_log_byte_identical(
    containment_boundary: Path, tmp_path: Path
) -> None:
    """The stronger form of the ordering claim: not merely 'no file', but 'no append'.

    `test_containment_present_but_unparseable_manifest_aborts_the_read` asserts the
    registry does not exist, which a pre-existing log would satisfy vacuously. Here the
    log already holds one good row; the aborted call must leave it byte-identical.
    """
    registry = tmp_path / "access.jsonl"
    good = tmp_path / "good_manifest.json"
    _manifest(good, ["mask-alpha"])
    open_restricted(
        containment_boundary, record=_record(), registry=registry, mask_bundle_manifest=good
    )
    before = registry.read_bytes()

    broken = tmp_path / "broken_manifest.json"
    broken.write_bytes(b"{not json at all")
    with pytest.raises(LockedTestError):
        open_restricted(
            containment_boundary,
            record=_record(),
            registry=registry,
            mask_bundle_manifest=broken,
        )

    assert registry.read_bytes() == before, (
        "the aborted containment read appended to the access log anyway; the abort must "
        "precede `_append_and_flush`, not follow it"
    )


def test_containment_valid_manifest_populates_the_record_and_the_read_proceeds(
    containment_boundary: Path, tmp_path: Path
) -> None:
    """The MUST-NOT-FIRE half: a usable manifest is evidence, not an obstacle.

    A refusal-only test would pass against a guard that refused everything, which would
    block the pre-G-05 coverage audit outright. This pins that a valid manifest yields a
    populated row -- the `mask_id`s AS FOUND (order preserved, not normalised, because
    the record is evidence of the bytes read) and the manifest's byte-level SHA-256 --
    and that the read still returns the resolved path.
    """
    import hashlib

    manifest = tmp_path / "frozen_bundle_manifest.json"
    raw = _manifest(manifest, ["mask-beta", "mask-alpha"])
    registry = tmp_path / "access.jsonl"

    returned = open_restricted(
        containment_boundary,
        record=_record(),
        registry=registry,
        mask_bundle_manifest=manifest,
    )

    assert returned == containment_boundary.resolve(), "the read did not proceed"
    row = json.loads(registry.read_text(encoding="utf-8").splitlines()[-1])
    assert row["mask_bundle_ids"] == ["mask-beta", "mask-alpha"], (
        "the containment field was normalised or reordered; the record must contain the "
        "ids as the manifest held them at access time"
    )
    assert row["mask_registry_hash"] == hashlib.sha256(raw).hexdigest(), (
        "the recorded hash is not the SHA-256 of the manifest's own bytes, so it cannot "
        "be re-verified against the artifact after the fact"
    )


def test_containment_record_cannot_contain_a_mask_registered_after_the_access(
    containment_boundary: Path, tmp_path: Path
) -> None:
    """SD-C-02's actual property, stated as a test: containment, not clock comparison.

    The access row evidences registration-before-access because it CONTAINS the bundle
    as of the read. A mask that lands in the manifest afterwards therefore cannot appear
    in a row already written -- which is what makes the ordering provable on any clocks
    and across any hosts, with no timestamp comparison anywhere.
    """
    manifest = tmp_path / "frozen_bundle_manifest.json"
    _manifest(manifest, ["mask-registered-before"])
    registry = tmp_path / "access.jsonl"

    open_restricted(
        containment_boundary,
        record=_record(),
        registry=registry,
        mask_bundle_manifest=manifest,
    )
    # A later registration rewrites the manifest. (The real producer's manifest is
    # write-once per freeze, `src/evaluation/masks.py` Q4 = A; this fixture simulates the
    # next freeze's bundle to prove the ALREADY-WRITTEN row cannot absorb it.)
    _manifest(manifest, ["mask-registered-before", "mask-registered-after"])

    row = json.loads(registry.read_text(encoding="utf-8").splitlines()[-1])
    assert row["mask_bundle_ids"] == ["mask-registered-before"], (
        "a mask registered after the access appeared in the access record; containment "
        "is the ordering proof and a mutable row would destroy it"
    )


def test_containment_absent_manifest_leaves_the_fields_none_and_the_read_proceeds(
    containment_boundary: Path, tmp_path: Path
) -> None:
    """ABSENT is not BROKEN: the two must stay distinguishable.

    A manifest path that does not exist records `None` and proceeds (the downstream
    `require_locked_receipt` refusal is the fail-closed half). Widening the abort to
    cover this case would break the acquisition and coverage-audit read paths, which
    supply no bundle; narrowing the abort to cover neither would hide broken evidence.
    This test is the boundary between the two, and it fails if either drifts.
    """
    registry = tmp_path / "access.jsonl"
    returned = open_restricted(
        containment_boundary,
        record=_record(),
        registry=registry,
        mask_bundle_manifest=tmp_path / "no_such_manifest.json",
    )
    row = json.loads(registry.read_text(encoding="utf-8").splitlines()[-1])
    assert returned == containment_boundary.resolve()
    assert row["mask_bundle_ids"] is None and row["mask_registry_hash"] is None


def test_containment_default_keyword_is_backward_compatible(
    containment_boundary: Path, tmp_path: Path
) -> None:
    """The edit was ruled ADDITIVE; this is the test that holds it to that.

    A caller that predates the 2026-09-06 edit passes no `mask_bundle_manifest` at all.
    It must still log and read exactly as before, with the two new fields present and
    `None` rather than absent -- a row missing the keys would break the consuming
    refusal's own `None` check as surely as a wrong value would.
    """
    registry = tmp_path / "access.jsonl"
    returned = open_restricted(containment_boundary, record=_record(), registry=registry)

    assert returned == containment_boundary.resolve()
    row = json.loads(registry.read_text(encoding="utf-8").splitlines()[-1])
    assert row["mask_bundle_ids"] is None
    assert row["mask_registry_hash"] is None
    # The pre-edit contract is untouched: same required fields, same guard-stamped
    # ordering evidence, same one-row-per-open behaviour.
    assert row["locked_test_accessed"] is True
    assert row["purpose"] in PURPOSES
    assert dt.datetime.fromisoformat(row["logged_at_utc"]).tzinfo is not None


def test_containment_fields_are_optional_on_the_record_itself() -> None:
    """`AccessRecord`'s required-field check must be untouched by the additive edit.

    Constructed three ways: without the fields (the pre-edit call shape), with them, and
    with a required field blanked while the new fields are supplied -- the last proving
    the new optional fields cannot be mistaken for the required set.
    """
    without = _record()
    assert without.mask_bundle_ids is None and without.mask_registry_hash is None

    with_fields = AccessRecord(
        run_id="r",
        retrieved_at_utc="2026-08-28T00:00:00Z",
        scope="s",
        purpose="locked_evaluation",
        performance_inspected=False,
        locked_test_accessed=True,
        authorization="a",
        mask_bundle_ids=("mask-alpha",),
        mask_registry_hash="0" * 64,
    )
    assert with_fields.mask_bundle_ids == ("mask-alpha",)

    with pytest.raises(LockedTestError):
        AccessRecord(
            run_id="",
            retrieved_at_utc="2026-08-28T00:00:00Z",
            scope="s",
            purpose="locked_evaluation",
            performance_inspected=False,
            locked_test_accessed=True,
            authorization="a",
            mask_bundle_ids=("mask-alpha",),
            mask_registry_hash="0" * 64,
        )


def test_containment_manifest_key_matches_the_producer() -> None:
    """Static cross-check: the key this unit's guard reads is the key the producer writes.

    `_containment_fields` reads `payload["mask_ids"]`, and the fixtures above synthesise
    manifests in that shape. A synthetic fixture agreeing with a synthetic expectation
    proves nothing about the real producer, so this test parses the sibling's
    `src/evaluation/masks.py` and confirms `freeze_bundle` really does build a mapping
    with a literal `mask_ids` key. Parsed, never imported and never executed: the
    producer is `evaluation-and-comparison`'s module, and this unit checks the contract
    between them without taking a runtime dependency on it.
    """
    producer = REPO_ROOT / "src" / "evaluation" / "masks.py"
    if not producer.is_file():
        pytest.skip(
            "src/evaluation/masks.py (the frozen-bundle manifest's producer, owned by "
            "evaluation-and-comparison) is not on disk; the consumer contract "
            "`payload['mask_ids']` in `_containment_fields` cannot be cross-checked "
            "against it, and is left asserted only by this section's fixtures"
        )
    tree = ast.parse(producer.read_text(encoding="utf-8"), filename=str(producer))
    freeze = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "freeze_bundle"
    ]
    assert freeze, "src/evaluation/masks.py no longer defines freeze_bundle"
    keys = {
        key.value
        for node in ast.walk(freeze[0])
        if isinstance(node, ast.Dict)
        for key in node.keys
        if isinstance(key, ast.Constant) and isinstance(key.value, str)
    }
    assert "mask_ids" in keys, (
        f"`freeze_bundle` no longer writes a 'mask_ids' key (found {sorted(keys)}), but "
        f"`_containment_fields` still reads `payload['mask_ids']` -- the producer and "
        f"the guard have drifted, and every read supplying a manifest would now abort"
    )


# --- R-19 reconciliation against the REAL pair (Recommendation 1, 2026-09-20) ----------
#
# `reconcile_access_records` has existed since `src/data/experiment_registry.py` was written
# and had never been run against the real pair of artifacts on disk. That is the gap this
# section closes: every assertion below reads the actual
# `artifacts/registry/experiment_registry.jsonl` and the actual access logs, never a fixture.
#
# NOT EXECUTED BY THE AUTHOR. No Python interpreter resolves on the clone where this was
# written (`python`/`python3` are Microsoft Store App Execution Alias stubs) and PyPI is
# unreachable, so these tests have never run. They are the STANDING check, written so the
# first interpreter that exists runs them. Nothing here claims a result.

REAL_REGISTRY = REPO_ROOT / "artifacts" / "registry" / "experiment_registry.jsonl"
#: The governed access log, CLOSED to further appends 2026-09-20 and preserved unedited.
GOVERNED_ACCESS_LOG = REPO_ROOT / "evidence" / "test_run_access_log.jsonl"
#: Where suite rows go from 2026-09-20 (gitignored; may legitimately be absent).
TEST_MODE_ACCESS_LOG = REPO_ROOT / "artifacts" / "exec_evidence" / "test_access_log.jsonl"

#: The two `run_id`s in the closed governed log, with the reason they are orphans. Both are
#: pytest modules, which open no registry run, so no `RegistryEvent` exists or should.
#: `reconcile_access_records` REPORTS them and never suppresses them, and it never writes --
#: back-filling a registry row to clear an orphan is the reconstruction failure this project
#: has already refused once.
HISTORICAL_TEST_ORPHANS = {
    "test_release_hashes": (
        "5,640 pre-2026-09-20 suite rows in the now-closed governed access log; a pytest "
        "module opens no registry run. See "
        "evidence/test_run_access_log.SUPERSEDED_2026-09-20.md"
    ),
    "test_acquisition_window": (
        "324 pre-2026-09-20 suite rows in the now-closed governed access log; a pytest "
        "module opens no registry run. See "
        "evidence/test_run_access_log.SUPERSEDED_2026-09-20.md"
    ),
    "test_phase_boundary": (
        "tests/test_phase_boundary.py:117 writes run_id=\"test_phase_boundary\" into the "
        "shared test-mode access log on every run; a pytest module opens no registry run. "
        "See governance/RULING_REQUEST_2026-09-23_CONSTRUCTION_STOPS.md"
    ),
}


def test_r19_reconciliation_runs_clean_against_the_real_registry_and_governed_log() -> None:
    """R-19 on the REAL pair: no UNEXPECTED orphan in either direction.

    "Clean" is stated precisely rather than loosely. It does NOT mean zero orphans: the
    closed governed log holds 5,964 suite rows under two `run_id`s the experiment registry
    has never known and should never know. It means (a) `reconcile_access_records` does not
    RAISE, which it does on any orphan outside `known_orphans`, and (b) the only orphans it
    reports are the two historical test `run_id`s named above. A THIRD `run_id` in that log
    -- a real December access with no registry row -- fails here, which is the case R-19
    exists to find.

    The owner's ruling on whether these two are permanently registered as known orphans, or
    whether the closed log leaves reconciliation scope entirely, is OWED and is recorded in
    the superseded-log notice. This test encodes the first reading; it does not decide it.
    """
    if not REAL_REGISTRY.is_file():
        pytest.skip(f"{REAL_REGISTRY.relative_to(REPO_ROOT)} does not exist yet")
    if not GOVERNED_ACCESS_LOG.is_file():
        pytest.skip(f"{GOVERNED_ACCESS_LOG.relative_to(REPO_ROOT)} does not exist")

    report = reconcile_access_records(
        REAL_REGISTRY, GOVERNED_ACCESS_LOG, known_orphans=HISTORICAL_TEST_ORPHANS
    )
    unexpected = sorted(set(report.expected_orphans) - set(HISTORICAL_TEST_ORPHANS))
    assert not unexpected, (
        f"reconciliation reported an orphan outside the enumerated historical set: "
        f"{unexpected}"
    )
    assert report.access_rows > 0 and report.registry_rows > 0, (
        "reconciliation read zero rows from one side; a join over an empty set proves "
        "nothing and must not be mistaken for a clean result"
    )


def test_r19_reconciliation_would_raise_on_an_unregistered_access(tmp_path: Path) -> None:
    """NEGATIVE CONTROL. A reconciliation that never raises is not a check.

    The real governed log is copied to `tmp_path` byte-for-byte -- the on-disk artifact is
    append-only and is NEVER written to by a test -- and one synthetic access row for an
    unknown `run_id` is appended to the COPY. Reconciliation must raise, naming that
    `run_id`. The must-not-fire limb runs first: the same copy WITHOUT the planted row,
    with the historical orphans declared, must not raise.
    """
    if not REAL_REGISTRY.is_file() or not GOVERNED_ACCESS_LOG.is_file():
        pytest.skip("the real registry/access-log pair is not both present")

    copy = tmp_path / "access_copy.jsonl"
    copy.write_bytes(GOVERNED_ACCESS_LOG.read_bytes())

    reconcile_access_records(
        REAL_REGISTRY, copy, known_orphans=HISTORICAL_TEST_ORPHANS
    )  # must-not-fire on the unplanted copy

    planted = {
        "run_id": "unregistered-december-access",
        "retrieved_at_utc": "2026-09-20T00:00:00+00:00",
        "scope": "synthetic control row, tmp copy only",
        "purpose": "locked_evaluation",
        "performance_inspected": True,
        "locked_test_accessed": True,
        "authorization": "none -- this is the violation being detected",
    }
    with copy.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(planted, sort_keys=True) + "\n")

    with pytest.raises(RegistryError) as excinfo:
        reconcile_access_records(REAL_REGISTRY, copy, known_orphans=HISTORICAL_TEST_ORPHANS)
    assert "unregistered-december-access" in str(excinfo.value)

    assert GOVERNED_ACCESS_LOG.is_file(), "the real access log must survive this test"


def test_the_test_mode_access_log_also_reconciles_when_it_exists() -> None:
    """The separated suite log is held to the same rule once it has rows.

    It is gitignored and legitimately absent on a fresh clone, so absence SKIPS with a
    named reason rather than passing vacuously. Its rows carry the same two test `run_id`s.
    """
    if not TEST_MODE_ACCESS_LOG.is_file():
        pytest.skip(
            f"{TEST_MODE_ACCESS_LOG.relative_to(REPO_ROOT)} has no rows yet; it is written "
            f"by tests/test_release_hashes.py and tests/test_acquisition_window.py on a run "
            f"where restricted artifacts are present, and it is gitignored"
        )
    if not REAL_REGISTRY.is_file():
        pytest.skip(f"{REAL_REGISTRY.relative_to(REPO_ROOT)} does not exist yet")
    report = reconcile_access_records(
        REAL_REGISTRY, TEST_MODE_ACCESS_LOG, known_orphans=HISTORICAL_TEST_ORPHANS
    )
    assert not (set(report.expected_orphans) - set(HISTORICAL_TEST_ORPHANS))


def test_every_row_of_the_closed_governed_log_is_performance_blind() -> None:
    """The closed log's own content claim, DERIVED here rather than carried.

    `evidence/test_run_access_log.SUPERSEDED_2026-09-20.md` states that all 5,964 rows
    record `performance_inspected: false` and that none is the G-06 one-shot evaluation.
    A notice asserting its own contents is worth nothing unless something checks it. Only
    the JSON envelope fields are read; no December content is opened by this test.
    """
    if not GOVERNED_ACCESS_LOG.is_file():
        pytest.skip(f"{GOVERNED_ACCESS_LOG.relative_to(REPO_ROOT)} does not exist")
    inspected: list[str] = []
    evaluations: list[str] = []
    rows = 0
    with GOVERNED_ACCESS_LOG.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rows += 1
            row = json.loads(line)
            if row.get("performance_inspected"):
                inspected.append(str(row.get("run_id")))
            if row.get("purpose") == "locked_evaluation":
                evaluations.append(str(row.get("run_id")))
    print(f"closed governed access log: rows derived {rows}")
    assert not inspected, (
        f"rows claiming performance_inspected in the closed log: {sorted(set(inspected))}. "
        f"The superseded-log notice asserts none exists, and a G-05 reviewer reads that "
        f"notice"
    )
    assert not evaluations, (
        f"rows claiming purpose=locked_evaluation in the closed log: "
        f"{sorted(set(evaluations))}. The G-06 one-shot event has not occurred and no row "
        f"may be read as evidence that it did"
    )


# --- D-28 option (b): `read_persistence_history_lookup` (2026-09-24, post-receipt ---------
# --- amendment, governance-guards unit). 5 tests, one per enforced condition. -------------
# Section 10's SD-C-02 precedent is the model: a new, additive capability disclosed and
# tested in this same module, the READY receipt left standing as history.

from src.data.locked_test import (  # noqa: E402
    PERSISTENCE_HISTORY_CALLERS,
    PERSISTENCE_HISTORY_DAY,
    read_persistence_history_lookup,
)

_PH_SIGNATURE = "synthetic D-28-option-b G-05 signature -- never a real one"


def _ph_signed_snapshot(*, authorized: bool = True, decision: str = "D-synthetic-ph"):
    """A synthetic snapshot whose gates.G-05 verifies AND whose
    persistence_history_lookup block is authorized -- both conditions (iv) and (v)
    satisfied by default, so each test below can flip exactly the one condition it tests."""
    return synthetic_snapshot(
        data={
            "gates": {
                "G-05": {
                    "status": "signed",
                    "decision": "D-synthetic-ph",
                    "signature_sha256": hashlib.sha256(_PH_SIGNATURE.encode("utf-8")).hexdigest(),
                }
            }
        },
        experiment={
            "persistence_history_lookup": {"authorized": authorized, "decision": decision}
        },
    )


def _ph_loader():
    """Synthetic UNEMBARGOED December rows: 2 Dec (would be scored) and 1 Dec (history-only).
    Real column names (interval_start_utc/station_id/vtec_tecu), synthetic values."""
    rows = []
    for day, hour_count in (("2022-12-01", 24), ("2022-12-02", 3)):
        for h in range(hour_count):
            rows.append(
                {
                    "interval_start_utc": f"{day}T{h:02d}:00:00Z",
                    "station_id": "BSHM",
                    "vtec_tecu": 5.0 + h,
                }
            )
    return rows


def _ph_tmp_registry() -> Path:
    import tempfile

    return Path(tempfile.mkdtemp()) / "persistence_history_access_log.jsonl"


def test_ph_condition_i_never_returns_a_row_outside_1_december() -> None:
    """(i) no 1-Dec row is ever SCORED -- this function's own second check: it silently
    drops every row outside PERSISTENCE_HISTORY_DAY rather than returning it, so even a
    loader that hands back the whole month cannot leak a 2-Dec (scorable) value out."""
    lookup = read_persistence_history_lookup(
        _ph_signed_snapshot(),
        model_id="M-01",
        run_id="test-ph-run",
        g05_signature=_PH_SIGNATURE,
        path=RESTRICTED_DIR,
        loader=_ph_loader,
        registry=_ph_tmp_registry(),
    )
    assert lookup, "expected at least the 24 synthetic 1-Dec rows"
    for _station, stamp in lookup:
        assert stamp.date().isoformat() == PERSISTENCE_HISTORY_DAY, (
            f"a 2-Dec (or other) row reached the caller: {stamp}"
        )
    assert len(lookup) == 24, "expected exactly the 24 synthetic 1-Dec hours, no more"


def test_ph_condition_ii_only_m01_m02_may_call_it() -> None:
    """(ii) any model_id outside {M-01, M-02} is refused before any read is attempted."""
    for bad_id in ("M-03", "M-06", "", "m-01", "M-01 "):
        with pytest.raises(LockedTestError) as excinfo:
            read_persistence_history_lookup(
                _ph_signed_snapshot(),
                model_id=bad_id,
                run_id="test-ph-run",
                g05_signature=_PH_SIGNATURE,
                path=RESTRICTED_DIR,
                loader=_ph_loader,
                registry=_ph_tmp_registry(),
            )
        assert "not one of" in str(excinfo.value)
    assert PERSISTENCE_HISTORY_CALLERS == frozenset({"M-01", "M-02"})
    for good_id in sorted(PERSISTENCE_HISTORY_CALLERS):
        lookup = read_persistence_history_lookup(
            _ph_signed_snapshot(),
            model_id=good_id,
            run_id="test-ph-run",
            g05_signature=_PH_SIGNATURE,
            path=RESTRICTED_DIR,
            loader=_ph_loader,
            registry=_ph_tmp_registry(),
        )
        assert lookup


def test_ph_condition_iii_logs_a_complete_access_record() -> None:
    """(iii) routed through open_restricted; the registry receives one complete,
    correctly-tagged row per call, with purpose="persistence_history"."""
    registry = _ph_tmp_registry()
    read_persistence_history_lookup(
        _ph_signed_snapshot(),
        model_id="M-02",
        run_id="test-ph-run",
        g05_signature=_PH_SIGNATURE,
        path=RESTRICTED_DIR,
        loader=_ph_loader,
        registry=registry,
    )
    rows = [json.loads(line) for line in registry.read_text(encoding="utf-8").splitlines() if line]
    assert len(rows) == 1, f"expected exactly one logged access row, got {len(rows)}"
    row = rows[0]
    assert row["purpose"] == "persistence_history"
    assert row["locked_test_accessed"] is True
    assert row["performance_inspected"] is False
    # Rec 10 (GOV-2026-09-24-BT-01): the row carries the CALLER-supplied run_id, so a
    # G-06 reviewer attributes the read by key — a constant on every row evidences nothing.
    assert row["run_id"] == "test-ph-run"
    assert "M-02" in row["authorization"]
    assert row["scope"]
    assert row["retrieved_at_utc"]


def test_ph_run_id_is_caller_supplied_and_empty_refuses() -> None:
    """Rec 10 (GOV-2026-09-24-BT-01): attribution by key. Two limbs: (a) a distinct
    caller-supplied run_id lands verbatim on the appended access row; (b) an empty
    run_id refuses via AccessRecord's own emptiness check, with no row appended."""
    registry = _ph_tmp_registry()
    read_persistence_history_lookup(
        _ph_signed_snapshot(),
        model_id="M-01",
        run_id="governed-run-2026-09-24T21Z",
        g05_signature=_PH_SIGNATURE,
        path=RESTRICTED_DIR,
        loader=_ph_loader,
        registry=registry,
    )
    rows = [json.loads(line) for line in registry.read_text(encoding="utf-8").splitlines() if line]
    assert [r["run_id"] for r in rows] == ["governed-run-2026-09-24T21Z"]
    empty_registry = _ph_tmp_registry()
    with pytest.raises(LockedTestError) as excinfo:
        read_persistence_history_lookup(
            _ph_signed_snapshot(),
            model_id="M-01",
            run_id="",
            g05_signature=_PH_SIGNATURE,
            path=RESTRICTED_DIR,
            loader=_ph_loader,
            registry=empty_registry,
        )
    assert "run_id" in str(excinfo.value)
    assert not empty_registry.exists() or not empty_registry.read_text(encoding="utf-8").strip()


def test_ph_condition_iv_blocked_pre_g05_succeeds_post_g05() -> None:
    """(iv) pre-G-05: g05_signature=None refuses, and a non-verifying signature refuses,
    with NO row appended to the registry either time. Post-G-05 (a verifying signature):
    succeeds."""
    registry = _ph_tmp_registry()
    with pytest.raises(LockedTestError) as excinfo:
        read_persistence_history_lookup(
            _ph_signed_snapshot(),
            model_id="M-01",
            run_id="test-ph-run",
            g05_signature=None,
            path=RESTRICTED_DIR,
            loader=_ph_loader,
            registry=registry,
        )
    assert "g05_signature" in str(excinfo.value) or "verification" in str(excinfo.value)
    with pytest.raises(LockedTestError):
        read_persistence_history_lookup(
            _ph_signed_snapshot(),
            model_id="M-01",
            run_id="test-ph-run",
            g05_signature="the wrong artifact",
            path=RESTRICTED_DIR,
            loader=_ph_loader,
            registry=registry,
        )
    assert not registry.exists() or registry.read_text(encoding="utf-8").strip() == "", (
        "a pre-G-05 or non-verifying attempt must not append any access row"
    )
    lookup = read_persistence_history_lookup(
        _ph_signed_snapshot(),
        model_id="M-01",
        run_id="test-ph-run",
        g05_signature=_PH_SIGNATURE,
        path=RESTRICTED_DIR,
        loader=_ph_loader,
        registry=registry,
    )
    assert lookup, "a verifying post-G-05 signature must succeed"


def test_ph_condition_v_inert_until_its_own_d_number_is_authorized() -> None:
    """(v) frozen under its own D-number before use -- the mechanism's kill switch.
    authorized=False, a TBD decision, and a non-D-number decision string each refuse,
    independent of conditions (i)-(iv) all being otherwise satisfied. This is the SAME
    check configs/experiment.yaml ships today (authorized: false,
    decision: "TBD - freeze gate") -- the mechanism is inert on the real config until
    the owner rules and flips both fields."""
    unauthorized = _ph_signed_snapshot(authorized=False)
    with pytest.raises(LockedTestError) as excinfo:
        read_persistence_history_lookup(
            unauthorized,
            model_id="M-01",
            run_id="test-ph-run",
            g05_signature=_PH_SIGNATURE,
            path=RESTRICTED_DIR,
            loader=_ph_loader,
            registry=_ph_tmp_registry(),
        )
    assert "authorized" in str(excinfo.value)

    tbd_decision = _ph_signed_snapshot(decision="TBD — freeze gate")
    with pytest.raises(LockedTestError):
        read_persistence_history_lookup(
            tbd_decision,
            model_id="M-01",
            run_id="test-ph-run",
            g05_signature=_PH_SIGNATURE,
            path=RESTRICTED_DIR,
            loader=_ph_loader,
            registry=_ph_tmp_registry(),
        )

    not_a_d_number = _ph_signed_snapshot(decision="approved, verbally")
    with pytest.raises(LockedTestError) as excinfo:
        read_persistence_history_lookup(
            not_a_d_number,
            model_id="M-01",
            run_id="test-ph-run",
            g05_signature=_PH_SIGNATURE,
            path=RESTRICTED_DIR,
            loader=_ph_loader,
            registry=_ph_tmp_registry(),
        )
    assert "D-number" in str(excinfo.value)

    # positive control: both fields correct together succeed (already exercised by the
    # other four tests above; restated here so this test alone proves the switch, not
    # only its refusals).
    lookup = read_persistence_history_lookup(
        _ph_signed_snapshot(),
        model_id="M-01",
        run_id="test-ph-run",
        g05_signature=_PH_SIGNATURE,
        path=RESTRICTED_DIR,
        loader=_ph_loader,
        registry=_ph_tmp_registry(),
    )
    assert lookup


def test_ph_the_real_config_reflects_its_actual_authorization_state() -> None:
    """The mechanism's OWN config, as shipped, is checked against whatever it actually
    says today -- not against a fixed assumption. D-68 (2026-09-24) authorized it: the
    real config now carries `authorized: true` and cites the real D-number, and this
    test asserts exactly that (not "unauthorized", which was the pre-D-68 state)."""
    import yaml

    real = yaml.safe_load(
        (Path(__file__).resolve().parent.parent / "configs" / "experiment.yaml").read_text(
            encoding="utf-8"
        )
    )
    block = real["persistence_history_lookup"]
    assert block["authorized"] is True
    assert str(block["decision"]).strip() == "D-68"
    # positive control: the real config, read through the real function, actually works.
    lookup = read_persistence_history_lookup(
        synthetic_snapshot(
            data={
                "gates": {
                    "G-05": {
                        "status": "signed",
                        "decision": "D-synthetic-real-config-check",
                        "signature_sha256": hashlib.sha256(_PH_SIGNATURE.encode("utf-8")).hexdigest(),
                    }
                }
            },
            experiment={"persistence_history_lookup": block},
        ),
        model_id="M-01",
        run_id="test-ph-run",
        g05_signature=_PH_SIGNATURE,
        path=RESTRICTED_DIR,
        loader=_ph_loader,
        registry=_ph_tmp_registry(),
    )
    assert lookup, "the real, committed config should permit a real call to succeed"
