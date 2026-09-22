"""The run-time phase boundary: NFR-PHASE-01's authoritative limb, proven by refusal.

Purpose
-------
Negative controls for `src/data/phase_contract.py` (R-23, R-24, SD-G-05): one import
control per RAW module, one produced-field control per D-17 exclusion (eight, not
TE 7.0's five), renamed-column controls proving fragment/token matching, the
independence assertion (neither limb substitutes for the other), the
producing-script completeness test (gated on script existence, never a silent
vacuous pass), the G-P3C hash-diff controls, and the documentation test pinning the
static scan's subordinate status. Nothing here discharges TA-27 — mechanism only,
smoke evidence until the governed environment exists.

**THIS MODULE IS THE HASH-DIFF LIMB'S HOME** (cross-reference added 2026-09-20,
Recommendation 58). `team.md` § Deployment names `tests/test_phase_boundary.py` as that
home. It is not: `diff_protected_hashes` and `assert_protected_hashes_unchanged` are
exercised here, over a synthetic protected-entry list, by
`test_identical_manifests_diff_empty_and_training_is_permitted`,
`test_a_differing_hash_is_named_and_training_is_refused`,
`test_a_missing_protected_entry_fails_before_any_diff`,
`test_an_unknown_entry_is_an_integrity_failure` and
`test_an_empty_or_duplicated_protected_entry_list_is_refused`. Both required tests exist;
only the LOCATION differs from the affirmed practice's wording, and
`tests/test_phase_boundary.py`'s own docstring now points here so a G-P3C reviewer
arriving from either side finds the limb rather than recording a false gap.

Inputs
------
`tmp_path` and the repository's own `scripts/` tree (read-only, for the completeness
population) and `tests/test_phase_boundary.py` (read-only, for the documentation
test). No December content, no restricted path, no scientific value.

Re-run behaviour
----------------
Deterministic and self-contained; pure functions under test, no writes outside
`tmp_path`.

Governance
----------
* TE 7.0 / 7.0B; D-16, D-17; NFR-PHASE-01; gate G-P3C; R-22 ("an empty diff is not
  yet proof" while BLK-06's per-item binding is pending — asserted nowhere here as
  proof of anything).
* The authoritative protected-entry list lives in `configs/experiment.yaml` per R-19,
  and where a test obtains D-24's list is OPEN per R-20: the hash-diff tests below use
  SYNTHETIC entry lists, exercising the mechanism and hardcoding no governed
  enumeration.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import IntegrityError, PhaseBoundaryError  # noqa: E402
from src.data.phase_contract import (  # noqa: E402
    PHASE1_PRODUCING_SCRIPTS,
    RAW_MODULES,
    ManifestError,
    assert_no_raw_fields,
    assert_phase_boundary,
    assert_protected_hashes_unchanged,
    diff_protected_hashes,
)

SCRIPTS_DIR = REPO_ROOT / "scripts"

#: D-17's sixteen Phase 1 target-row fields, used here ONLY as the happy-path control for
#: `assert_no_raw_fields`: the field guard must clear the frozen legitimate schema without a
#: false positive. It is a sample of legitimate column names, not a contract this module
#: enforces -- the guard under test never checks membership, completeness or arity, and this
#: constant reaches nothing but the two `assert_no_raw_fields` calls below. The exact
#: sixteen-field contract is owned by `src/data/prepared.py`'s `D17_FIELDS` and pinned by
#: `tests/test_phase_boundary.py`'s drift guard; the copy here is kept equal to it so a
#: reader does not meet two different sixteens.
#:
#: `processor_qc_flags` is absent on purpose: it is a key inside the data-quality block
#: (R-71 / NFR-DQ-01, W-3), never a row column. It was listed here in error from commit
#: `b844a4d` (2026-08-21), with the count misdescribed as seventeen; removed 2026-09-13.
D17_ALLOWED_FIELDS = (
    "interval_start_utc",
    "station_id",
    "cell_gdlat",
    "cell_glon",
    "cell_lat_bounds",
    "cell_lon_bounds",
    "vtec_tecu",
    "valid_observation_count",
    "within_hour_spread_tecu",
    "largest_internal_gap_s",
    "provider_dtec_summary",
    "aggregation_config_id",
    "target_valid",
    "phase_id",
    "source_id",
    "target_definition_id",
)


# --- limb 1: the import boundary ---------------------------------------------------------


@pytest.mark.parametrize("raw_module", sorted(RAW_MODULES))
def test_each_raw_module_is_refused_under_phase_1(raw_module: str) -> None:
    """One negative control per RAW module — all four, not the two 7.0 names."""
    with pytest.raises(PhaseBoundaryError) as excinfo:
        assert_phase_boundary(1, loaded_modules={raw_module: object()})
    assert raw_module in str(excinfo.value)


def test_a_raw_module_loaded_under_a_bare_dotted_name_is_still_refused() -> None:
    """The boundary is derived from module names, so a `gnss.rinex` import (no `src.`
    prefix, as under a different sys.path root) does not walk past it."""
    with pytest.raises(PhaseBoundaryError):
        assert_phase_boundary(1, loaded_modules={"gnss.rinex": object()})


def test_clean_modules_pass_under_phase_1_and_raw_modules_pass_under_phase_2() -> None:
    assert_phase_boundary(1, loaded_modules={"json": object(), "src.data.config": object()})
    # Phase 2 legitimately runs raw processing (TE 7.0 restricts Phase 1 only).
    assert_phase_boundary(2, loaded_modules={"src.gnss.rinex": object()})


def test_an_unknown_phase_is_refused() -> None:
    with pytest.raises(PhaseBoundaryError):
        assert_phase_boundary(3, loaded_modules={})


# --- limb 2: the produced-field prohibition, one control per D-17 exclusion --------------


@pytest.mark.parametrize(
    ("field_name", "d17_exclusion"),
    [
        ("valid_satellite_count", "1: valid_satellite_count"),
        ("ipp_lat", "2: any per-satellite or per-IPP quantity"),
        ("zenith_angle", "3: zenith angle or zenith weight"),
        ("elevation", "4: elevation"),
        ("dcb_bias_ns", "5: DCB"),
        ("stec_tecu", "6: STEC"),
        ("mapping_function_output", "7: mapping function output"),
        ("arc_count", "8: arc or cycle-slip statistics"),
    ],
)
def test_each_d17_exclusion_is_refused(field_name: str, d17_exclusion: str) -> None:
    """Eight produced-field controls, not five: the enumeration is D-17's, not 7.0's."""
    with pytest.raises(PhaseBoundaryError) as excinfo:
        assert_no_raw_fields(["interval_start_utc", field_name], phase=1)
    assert field_name in str(excinfo.value), f"exclusion {d17_exclusion} not caught"


@pytest.mark.parametrize("renamed", ["n_sat_valid", "zen_wt", "elev_deg", "cycle_slip_count"])
def test_a_renamed_exclusion_is_still_refused(renamed: str) -> None:
    """Fragment/token matching, not exact names: a renamed column cannot walk past."""
    with pytest.raises(PhaseBoundaryError):
        assert_no_raw_fields([renamed], phase=1)


def test_the_frozen_d17_contract_passes_and_innocent_lookalikes_pass() -> None:
    """Happy path plus the false-positive bound the token discipline exists for:
    `frozen_flag` contains the substring `zen` and `skipped_rows` contains `ipp`,
    and neither is a raw-processing quantity."""
    assert_no_raw_fields(D17_ALLOWED_FIELDS, phase=1)
    assert_no_raw_fields(["frozen_flag", "skipped_rows"], phase=1)


def test_phase_2_artifacts_are_not_restricted_by_this_limb() -> None:
    assert_no_raw_fields(["stec_tecu", "dcb_bias_ns"], phase=2)


def test_an_object_exposing_columns_is_accepted() -> None:
    """The approved signature names a DataFrame; the guard duck-types `.columns`."""

    class _FrameLike:
        columns = ("interval_start_utc", "stec_tecu")

    with pytest.raises(PhaseBoundaryError):
        assert_no_raw_fields(_FrameLike(), phase=1)


def test_a_non_enumerable_input_is_refused() -> None:
    with pytest.raises(PhaseBoundaryError):
        assert_no_raw_fields(42, phase=1)


def test_neither_limb_substitutes_for_the_other() -> None:
    """R-23's independence assertion, both directions."""
    # Import limb clean while the field limb refuses:
    assert_phase_boundary(1, loaded_modules={})
    with pytest.raises(PhaseBoundaryError):
        assert_no_raw_fields(["dcb_bias_ns"], phase=1)
    # Field limb clean while the import limb refuses:
    assert_no_raw_fields(D17_ALLOWED_FIELDS, phase=1)
    with pytest.raises(PhaseBoundaryError):
        assert_phase_boundary(1, loaded_modules={"src.gnss.rinex": object()})


# --- R-24: the producing-script completeness test ----------------------------------------

#: Call names that count as a write for the ordering assertion. A heuristic by
#: necessity (static analysis cannot see run time), documented so a reviewer can
#: judge its width; the authoritative ordering guarantee remains the run-time call
#: itself at each script's entry.
_WRITE_MARKERS = frozenset(
    {
        "write_text",
        "write_bytes",
        "to_csv",
        "to_parquet",
        "writerow",
        "writerows",
        "dump",
        "write",
        "savefig",
        "save",
    }
)


def _call_name(node: ast.Call) -> str:
    func = node.func
    return func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")


def _is_write_call(node: ast.Call) -> bool:
    name = _call_name(node)
    if name == "open" and len(node.args) >= 2:
        mode = node.args[1]
        if isinstance(mode, ast.Constant) and isinstance(mode.value, str):
            return any(ch in mode.value for ch in "wax+")
    return name in _WRITE_MARKERS


def _first_write_lineno(tree: ast.AST) -> int | None:
    first: int | None = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _is_write_call(node):
            if first is None or node.lineno < first:
                first = node.lineno
    return first


def _first_unguarded_write_lineno(tree: ast.Module) -> int | None:
    """The first write reached in EXECUTION order without a guard call before it.

    WHY THIS EXISTS, and why `_first_write_lineno` alone is the wrong test (derived
    2026-09-20 from the first execution of this suite under the governed Python 3.11
    pin; the suite had never been run when the check was written).

    R-24's obligation is that `assert_no_raw_fields` RUNS before the first write runs.
    Comparing the smallest write line number against the smallest guard line number is
    a proxy for that, and it is wrong in BOTH directions:

      * False positive, observed: `scripts/07_evaluate_and_report.py` was reported as
        "first write (line 1040) precedes the first assert_no_raw_fields call (line
        1213)". Line 1040 is inside `_report_set` (744-1077), which is *defined* above
        but *called* below the guard: `_run` (1292) guards at :1295 and only then
        reaches `_report_set` through `_evaluate_partition`; the fixture entry point
        `_run_fixture_scale` (1186) guards at :1213 before the same descent. Both
        execution paths satisfy R-24. The script was never in violation.
      * False negative, unobserved and the more dangerous half: a writer helper defined
        BELOW the guard line but called BEFORE the guard would have a larger line
        number and clear the line-order check while writing unguarded at run time.

    So this walks the call graph from the module body in statement order, carrying a
    `guarded` flag: a call to `assert_no_raw_fields` sets it for everything that follows
    on that path, a call to a module-local function descends with the current flag, and
    a write reached while the flag is false is the violation. Recursion is cut by a
    visiting set. Calls the checker cannot resolve to a module-local function are
    stepped over, which keeps the check conservative in the same direction the original
    was: it can only clear a script whose resolvable paths guard first.
    """
    functions: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
    }

    def walk_body(
        body: list[ast.stmt], guarded: bool, visiting: frozenset[str]
    ) -> tuple[int | None, bool]:
        """Return (first unguarded write line on this path, guarded state on exit)."""
        for stmt in body:
            if isinstance(stmt, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
                continue  # a definition executes nothing; its body is walked when called
            for node in ast.walk(stmt):
                if not isinstance(node, ast.Call):
                    continue
                name = _call_name(node)
                if name == "assert_no_raw_fields":
                    guarded = True
                    continue
                if _is_write_call(node) and not guarded:
                    return node.lineno, guarded
                target = functions.get(name)
                if target is not None and name not in visiting:
                    found, guarded = walk_body(
                        target.body, guarded, visiting | {name}
                    )
                    if found is not None:
                        return found, guarded
        return None, guarded

    found, _ = walk_body(tree.body, False, frozenset())
    return found


def _first_guard_call_lineno(tree: ast.AST) -> int | None:
    first: int | None = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
            if name == "assert_no_raw_fields" and (first is None or node.lineno < first):
                first = node.lineno
    return first


def _producing_script_violations(scripts_dir: Path) -> tuple[list[str], dict[str, str]]:
    """R-24's completeness check, factored so it runs against ANY supplied directory.

    Returns `(checked_script_names, offenders)`, where an offender maps script name to
    the violated expectation: no `assert_no_raw_fields` call at all, a first write
    preceding the first guard call, or an unparseable script (fail-closed: a script
    the checker cannot parse cannot be cleared, the R-27 posture). Factored out of the
    real test (iteration-1 Major 2) so synthetic fixture scripts can prove the
    detection fires BEFORE the real population arrives.
    """
    checked: list[str] = []
    offenders: dict[str, str] = {}
    for name in PHASE1_PRODUCING_SCRIPTS:
        script = scripts_dir / f"{name}.py"
        if not script.is_file():
            continue
        checked.append(script.name)
        try:
            tree = ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
        except SyntaxError as exc:
            offenders[script.name] = f"does not parse, so its guard call cannot be checked: {exc}"
            continue
        guard_line = _first_guard_call_lineno(tree)
        if guard_line is None:
            # Unchanged from the original check, deliberately: a producing script that
            # never calls the guard is an offender whether or not a write was detected.
            # Narrowing this to write-bearing scripts would let a producing script whose
            # write shape the marker set does not recognise clear the check silently.
            offenders[script.name] = "never calls assert_no_raw_fields"
            continue
        unguarded_line = _first_unguarded_write_lineno(tree)
        if unguarded_line is not None:
            offenders[script.name] = (
                f"first write (line {unguarded_line}) precedes the first "
                f"assert_no_raw_fields call (line {guard_line}) on the execution path "
                f"that reaches it"
            )
    return checked, offenders


def test_every_phase1_producing_script_calls_the_field_guard_before_its_first_write() -> None:
    """R-24's completeness test, gated on script existence.

    The population is the eight named producing scripts. With ZERO of them on disk the
    test SKIPS with the population recorded explicitly in the reason — the project's
    established shape for a subject that does not exist yet (`test_phase_boundary.py`'s
    own convention), never a silent vacuous pass. The moment the first producing
    script appears without the `assert_no_raw_fields` call, this test FAILS — and the
    detection that promise rests on is itself proven by the synthetic-fixture controls
    below, not assumed.
    """
    assert (
        len(PHASE1_PRODUCING_SCRIPTS) == 8
    ), "the producing-script enumeration drifted from R-24's eight"
    checked, offenders = _producing_script_violations(SCRIPTS_DIR)
    if not checked:
        pytest.skip(
            "population EMPTY, recorded explicitly: zero of the eight Phase 1 "
            "producing scripts (00_acquire_prepared_vtec ... 07_evaluate_and_report) "
            "exist yet; this completeness test binds the moment the first one appears "
            "and fails if it omits the assert_no_raw_fields call (R-24, DP-DATA-01)"
        )
    assert not offenders, (
        f"Phase 1 producing script(s) violate R-24's before-first-write obligation: "
        f"{offenders}"
    )


# Synthetic-fixture controls (iteration-1 Major 2): the detection logic is proven to
# FIRE before the real population exists. Fixture scripts live under tmp_path and
# reuse a real producing-script name so `_producing_script_violations` collects them;
# nothing is added to the real scripts/ tree.

_SYNTHETIC_SCRIPT_NAME = f"{PHASE1_PRODUCING_SCRIPTS[0]}.py"


def test_a_producing_script_with_no_guard_call_is_detected(tmp_path: Path) -> None:
    """Negative control 1: the write exists, the guard call does not."""
    (tmp_path / _SYNTHETIC_SCRIPT_NAME).write_text(
        '"""Synthetic violating producing script."""\n'
        "from pathlib import Path\n\n"
        'Path("out.csv").write_text("vtec_tecu\\n", encoding="utf-8")\n',
        encoding="utf-8",
    )
    checked, offenders = _producing_script_violations(tmp_path)
    assert checked == [_SYNTHETIC_SCRIPT_NAME]
    assert offenders == {_SYNTHETIC_SCRIPT_NAME: "never calls assert_no_raw_fields"}


def test_a_guard_call_after_the_first_write_is_detected(tmp_path: Path) -> None:
    """Negative control 2: the call is present but the write already happened."""
    (tmp_path / _SYNTHETIC_SCRIPT_NAME).write_text(
        '"""Synthetic ordering-violating producing script."""\n'
        "from pathlib import Path\n\n"
        "from src.data.phase_contract import assert_no_raw_fields\n\n"
        'Path("out.csv").write_text("vtec_tecu\\n", encoding="utf-8")\n'
        'assert_no_raw_fields(["vtec_tecu"], phase=1)\n',
        encoding="utf-8",
    )
    checked, offenders = _producing_script_violations(tmp_path)
    assert checked == [_SYNTHETIC_SCRIPT_NAME]
    assert _SYNTHETIC_SCRIPT_NAME in offenders
    assert "precedes" in offenders[_SYNTHETIC_SCRIPT_NAME]


def test_a_compliant_producing_script_passes(tmp_path: Path) -> None:
    """Positive control: guard call before the first write clears the checker."""
    (tmp_path / _SYNTHETIC_SCRIPT_NAME).write_text(
        '"""Synthetic compliant producing script."""\n'
        "from pathlib import Path\n\n"
        "from src.data.phase_contract import assert_no_raw_fields\n\n"
        'assert_no_raw_fields(["vtec_tecu"], phase=1)\n'
        'Path("out.csv").write_text("vtec_tecu\\n", encoding="utf-8")\n',
        encoding="utf-8",
    )
    checked, offenders = _producing_script_violations(tmp_path)
    assert checked == [_SYNTHETIC_SCRIPT_NAME]
    assert offenders == {}


def test_a_write_in_a_helper_called_before_the_guard_is_detected(tmp_path: Path) -> None:
    """Negative control 4: the write is in a helper DEFINED BELOW the guard line.

    This is the shape the superseded line-order check could not see. `_emit` writes at a
    LARGER line number than the `assert_no_raw_fields` call, so `min(write) < min(guard)`
    is false and the old check cleared the script -- while at run time `main` calls
    `_emit` first and writes unguarded. Added 2026-09-20 with the execution-order walk.
    """
    (tmp_path / _SYNTHETIC_SCRIPT_NAME).write_text(
        '"""Synthetic script whose unguarded write hides in a later-defined helper."""\n'
        "from pathlib import Path\n\n"
        "from src.data.phase_contract import assert_no_raw_fields\n\n"
        "def main():\n"
        "    _emit()\n"
        '    assert_no_raw_fields(["vtec_tecu"], phase=1)\n\n'
        "def _emit():\n"
        '    Path("out.csv").write_text("vtec_tecu\\n", encoding="utf-8")\n\n'
        "main()\n",
        encoding="utf-8",
    )
    checked, offenders = _producing_script_violations(tmp_path)
    assert checked == [_SYNTHETIC_SCRIPT_NAME]
    assert "precedes" in offenders[_SYNTHETIC_SCRIPT_NAME]


def test_a_write_in_a_helper_called_after_the_guard_passes(tmp_path: Path) -> None:
    """Positive control for the same walk: helper DEFINED ABOVE, CALLED AFTER the guard.

    `scripts/07_evaluate_and_report.py`'s real shape, reduced. The superseded check
    reported this as a violation; it is not one, and the walk must clear it without
    clearing the control above.
    """
    (tmp_path / _SYNTHETIC_SCRIPT_NAME).write_text(
        '"""Synthetic compliant script whose writer is defined above its entry point."""\n'
        "from pathlib import Path\n\n"
        "from src.data.phase_contract import assert_no_raw_fields\n\n"
        "def _emit():\n"
        '    Path("out.csv").write_text("vtec_tecu\\n", encoding="utf-8")\n\n'
        "def main():\n"
        '    assert_no_raw_fields(["vtec_tecu"], phase=1)\n'
        "    _emit()\n\n"
        "main()\n",
        encoding="utf-8",
    )
    checked, offenders = _producing_script_violations(tmp_path)
    assert checked == [_SYNTHETIC_SCRIPT_NAME]
    assert offenders == {}


def test_an_unparseable_producing_script_is_detected(tmp_path: Path) -> None:
    """Negative control 3: a script the checker cannot parse cannot be cleared."""
    (tmp_path / _SYNTHETIC_SCRIPT_NAME).write_text("def broken(:\n", encoding="utf-8")
    checked, offenders = _producing_script_violations(tmp_path)
    assert checked == [_SYNTHETIC_SCRIPT_NAME]
    assert "does not parse" in offenders[_SYNTHETIC_SCRIPT_NAME]


# --- the G-P3C hash diff ------------------------------------------------------------------

_SYNTHETIC_ENTRIES = ("alpha", "beta", "gamma")


def _manifest(**overrides: str) -> dict[str, str]:
    base = {"alpha": "hash-a", "beta": "hash-b", "gamma": "hash-c"}
    base.update(overrides)
    return base


def test_identical_manifests_diff_empty_and_training_is_permitted() -> None:
    assert (
        diff_protected_hashes(_manifest(), _manifest(), protected_entries=_SYNTHETIC_ENTRIES) == {}
    )
    assert_protected_hashes_unchanged(
        _manifest(), _manifest(), protected_entries=_SYNTHETIC_ENTRIES
    )


def test_a_differing_hash_is_named_and_training_is_refused() -> None:
    """G-P3C's refusal semantics: any diff -> refuse to train (TE 7.0B)."""
    current = _manifest(beta="hash-b-CHANGED")
    diff = diff_protected_hashes(_manifest(), current, protected_entries=_SYNTHETIC_ENTRIES)
    assert diff == {"beta": ("hash-b", "hash-b-CHANGED")}
    with pytest.raises(ManifestError) as excinfo:
        assert_protected_hashes_unchanged(
            _manifest(), current, protected_entries=_SYNTHETIC_ENTRIES
        )
    assert "beta" in str(excinfo.value)
    assert "refuses to train" in str(excinfo.value)


def test_a_missing_protected_entry_fails_before_any_diff() -> None:
    """R-21/R-22: a short set can never produce a reassuring empty diff."""
    short = {"alpha": "hash-a", "beta": "hash-b"}
    with pytest.raises(ManifestError) as excinfo:
        diff_protected_hashes(short, _manifest(), protected_entries=_SYNTHETIC_ENTRIES)
    assert "gamma" in str(excinfo.value)


def test_an_unknown_entry_is_an_integrity_failure() -> None:
    widened = _manifest(delta="hash-d")
    with pytest.raises(ManifestError) as excinfo:
        diff_protected_hashes(_manifest(), widened, protected_entries=_SYNTHETIC_ENTRIES)
    assert "delta" in str(excinfo.value)


def test_an_empty_or_duplicated_protected_entry_list_is_refused() -> None:
    with pytest.raises(ManifestError):
        diff_protected_hashes(_manifest(), _manifest(), protected_entries=())
    with pytest.raises(ManifestError):
        diff_protected_hashes(
            _manifest(), _manifest(), protected_entries=("alpha", "alpha", "beta", "gamma")
        )


# --- documentation tests (the Q7 rider) ---------------------------------------------------


def test_the_static_scan_declares_its_subordinate_status_in_its_own_docstring() -> None:
    """R-24's rider: the subordinate status is recorded WHERE THE CODE LIVES.

    `tests/test_phase_boundary.py` must state in its module docstring that it is the
    early-warning limb and does not discharge FR-P1-03-2's run-time requirement, so a
    future maintainer cannot read its presence as sufficient. Stating it only in a
    design document is exactly where it would be missed — this test fails the day the
    sentence is removed.
    """
    module_path = REPO_ROOT / "tests" / "test_phase_boundary.py"
    tree = ast.parse(module_path.read_text(encoding="utf-8"), filename=str(module_path))
    docstring = ast.get_docstring(tree) or ""
    assert (
        "early-warning limb" in docstring
    ), "test_phase_boundary.py no longer declares itself the early-warning limb"
    assert "does not discharge FR-P1-03-2" in docstring, (
        "test_phase_boundary.py no longer states that it does not discharge "
        "FR-P1-03-2's run-time requirement (R-24's Q7 rider)"
    )


def test_this_units_exceptions_derive_from_the_one_base() -> None:
    """R-23's base-class box: every exception this unit raises derives from
    `IntegrityError`, so the stage entry contract's `except IntegrityError` catches
    each and writes the aborted registry row."""
    assert issubclass(PhaseBoundaryError, IntegrityError)
    assert issubclass(ManifestError, IntegrityError)
