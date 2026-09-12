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
    PURPOSES,
    RESTRICTED_LITERAL_EXEMPT_MODULES,
    RESTRICTED_ROOT,
    AccessRecord,
    EvidenceScanError,
    assert_no_december_outside_restricted,
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
    assert logged <= dt.datetime.now(dt.UTC)


def test_caller_supplied_timestamp_is_not_trusted_for_ordering(tmp_path: Path) -> None:
    """A caller may write anything in `retrieved_at_utc`; the guard's stamp still holds.

    Negative control for the same defect: a caller that supplies a meaningless or even a
    future-dated `retrieved_at_utc` must not be able to corrupt the ordering evidence.
    """
    target = _any_restricted_file()
    if target is None:
        pytest.skip("no restricted artifact present to guard")
    registry = tmp_path / "access.jsonl"

    bogus = AccessRecord(
        run_id="r",
        retrieved_at_utc="not-a-timestamp-at-all",
        scope="s",
        purpose="coverage_audit",
        performance_inspected=False,
        locked_test_accessed=True,
        authorization="a",
    )
    open_restricted(target, record=bogus, registry=registry)
    row = json.loads(registry.read_text(encoding="utf-8").splitlines()[-1])

    assert row["retrieved_at_utc"] == "not-a-timestamp-at-all"
    # The guard's own stamp is still a real instant, independent of the caller's field.
    assert dt.datetime.fromisoformat(row["logged_at_utc"]).tzinfo is not None


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

from test_split_embargo import (  # noqa: E402
    SYNTH_EMBARGO_HOURS,
    SYNTH_YEAR,
    synthetic_partitions,
    synthetic_snapshot,
)

from src.data.config import PartitionError  # noqa: E402
from src.data.splits import (  # noqa: E402
    LOCKED_ID,
    materialise_locked_partition,
    partition_by_id,
    verify_g05_signature,
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
        partition.validation_month.year, partition.validation_month.month, 1, tzinfo=dt.UTC
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
        rows.append(
            {"interval_start_utc": f"{SYNTH_YEAR}-11-05T00:00:00+00:00", "vtec_tecu": 1.0}
        )
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
        retrieved_at_utc="t",
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
            retrieved_at_utc="t",
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
