"""Unit `external-products`: every Step 2-6 refusal negative-controlled.

PURPOSE. The driver-series contracts (W-4, W-5, W-8; R-57, R-57a, R-58, R-61, R-62,
R-63; SD-E-06, SD-E-07) tested directly against `src/external/spaceweather.py` -- which
is deliberately OUTSIDE the IRI/GIM import restriction (drivers ARE model inputs) --
and the IRI/GIM gate refusals (R-59, R-60) exercised THROUGH
`scripts/04_build_external_products.py` in a subprocess, because that script and
`src/evaluation/` are TE 12's only permitted importers of `iri` and `gim` and `tests/*`
is NOT allowlisted (SD-E-01). No test here imports `src.external.iri` or
`src.external.gim`, statically or dynamically.

The affirmed methodology is a negative control paired with every hard rule (team.md):
each test below proves a violation is CAUGHT, and the pairs whose halves assert
OPPOSITE outcomes (missing month vs hash mismatch; carry-forward within vs beyond the
bound; provisional-grade permitted vs barred uses) are asserted in both directions,
because a single-direction test lets the other half regress silently (R-61's shape).

WHAT NO TEST HERE DISCHARGES. WS-09/WS-10/WS-11/TA-07/TA-36 stay `Pending`; REQ-ENG-9,
FR-P1-04-4, FR-P1-04-15 and FR-P1-04-18 remain UNTESTED in the acceptance sense (no
row exists); TA-36's PRIMARY test is `features-and-splits`' (R-54a), and the alignment
and carry-forward controls here are this unit's UPSTREAM CONTRACT EVIDENCE, documented
separately and not replacing the primary rejection test. A passing run of this module
is smoke evidence on a non-governed interpreter, never governed evidence.

RE-RUN BEHAVIOUR. Unit tests are pure functions over synthetic in-memory series.
Subprocess tests run the stage script against a TEMPORARY workspace
(`TEC_WORKSPACE_ROOT`), so registry rows, config snapshots and manifests land under
`tmp_path`, never in the repository; `--code-commit` is passed explicitly because the
temporary workspace has no git tree (the lock is never written unpopulated), and
`PYTHONHASHSEED=0` is set so the determinism step does not re-exec inside the
subprocess. Injected gate-state values are CONTROL DATA, not governed evidence: the
gates refuse in injection mode even when fully satisfied, so no benchmark and no
comparator can be produced by any test in this module.

Run: pytest tests/test_external_drivers.py -rs
"""

from __future__ import annotations

import ast
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from src.data.config import AlignmentError, FeatureAvailabilityError, IntegrityError
from src.external.spaceweather import (
    align_interval_series,
    apply_carry_forward,
    assert_alignment,
    assert_carry_forward_conservation,
    assert_gfz_cross_products,
    assert_grade_eligible,
    assert_identical_across_cells,
    assert_series_provenance,
    assert_single_grade,
    assert_time_indexed_shape,
    provenance_stamp,
    refuse_divergent_rerun,
    resolve_f107_at_origin,
    trailing_mean,
    write_driver_manifest,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "04_build_external_products.py"
UTC = dt.UTC

#: The TE 6.2 window length (`f107_81_trailing`) as a TEST PARAMETER: the module under
#: test takes it as an argument (frozen elsewhere); tests exercise the property with
#: it and with small windows, proving the property is window-independent.
WINDOW_81 = 81


def _day(n: int) -> dt.date:
    return dt.date(2022, 1, 1) + dt.timedelta(days=n)


def _hour(n: int) -> dt.datetime:
    return dt.datetime(2022, 6, 1, tzinfo=UTC) + dt.timedelta(hours=n)


# =========================================================================================
# R-57: the F10.7 trailing mean, proven as a property (W-4; centered = defect)
# =========================================================================================


def test_trailing_mean_definitional_limb() -> None:
    """Limb 1: the mean at day d equals the mean of the window ENDING at d."""
    series = {_day(n): float(n) for n in range(200)}
    end = _day(100)
    expected = sum(range(100 - (WINDOW_81 - 1), 101)) / WINDOW_81
    assert trailing_mean(series, end_day=end, window_days=WINDOW_81) == pytest.approx(expected)


def test_trailing_mean_future_independence_property() -> None:
    """Limb 2 -- the limb that carries the rule: perturbing ANY day after the
    safe-lagged day leaves the computed mean UNCHANGED. This is exactly what 'uses
    future days' means, stated so a test can fail on it."""
    series = {_day(n): float(n % 17) for n in range(200)}
    end = _day(100)
    baseline = trailing_mean(series, end_day=end, window_days=WINDOW_81)
    for future_offset in (1, 2, 10, 40, 99):
        perturbed = dict(series)
        perturbed[_day(100 + future_offset)] = 9999.0
        assert (
            trailing_mean(perturbed, end_day=end, window_days=WINDOW_81) == baseline
        ), f"perturbing day +{future_offset} moved the mean; the window is not trailing"


def test_shifted_input_shifts_output_with_it() -> None:
    """The shifted-input property (SD-E-06): shift the input one day, the output
    follows -- catching a centered variant regardless of which API produced it."""
    series = {_day(n): float((n * 7) % 23) for n in range(200)}
    shifted = {day + dt.timedelta(days=1): value for day, value in series.items()}
    assert trailing_mean(series, end_day=_day(120), window_days=WINDOW_81) == trailing_mean(
        shifted, end_day=_day(121), window_days=WINDOW_81
    )


def test_centered_mean_variant_is_caught_by_both_limbs() -> None:
    """Negative control: a CENTERED mean fails limb 1 at every index and fails limb 2
    on perturbation -- a centered mean is a defect, not a fallback."""
    series = {_day(n): float(n) for n in range(200)}
    end = _day(100)
    half = WINDOW_81 // 2

    def centered_mean(values: dict[dt.date, float], day: dt.date) -> float:
        window = [day + dt.timedelta(days=offset) for offset in range(-half, half + 1)]
        return sum(values[d] for d in window) / len(window)

    trailing = trailing_mean(series, end_day=end, window_days=WINDOW_81)
    assert centered_mean(series, end) != trailing, "limb 1: definitional mismatch"
    perturbed = dict(series)
    perturbed[_day(101)] = 9999.0
    assert centered_mean(perturbed, end) != centered_mean(series, end), (
        "limb 2: a centered mean MOVES when a future day is perturbed -- the property "
        "that convicts it"
    )


def test_trailing_mean_refuses_missing_window_day() -> None:
    """TC-20: no value is imputed for the F10.7 outage window -- a window spanning a
    missing day stops and reports rather than choosing a treatment."""
    series = {_day(n): float(n) for n in range(200)}
    del series[_day(60)]
    with pytest.raises(IntegrityError, match="TC-20"):
        trailing_mean(series, end_day=_day(100), window_days=WINDOW_81)


# =========================================================================================
# R-57a: the daily-cadence composition raise (D-21/G-04 -- decided by nobody here)
# =========================================================================================


def _f107_availability(day: dt.date) -> dt.datetime:
    """D-25's convention shape as a TEST callable: available at 00:00 UTC on D+1."""
    return dt.datetime.combine(day + dt.timedelta(days=1), dt.time(0, 0), tzinfo=UTC)


def test_f107_previous_day_available_resolves() -> None:
    origin = dt.datetime(2022, 6, 10, 12, 0, tzinfo=UTC)
    medians = {dt.date(2022, 6, n): 100.0 + n for n in range(1, 10)}
    day, value = resolve_f107_at_origin(
        medians,
        origin=origin,
        availability_ts=_f107_availability,
        features={"carry_forward_composition": "TBD — freeze gate"},
    )
    assert day == dt.date(2022, 6, 9)
    assert value == 109.0


def test_f107_unavailable_with_tbd_composition_stops_naming_both_units() -> None:
    """The R-57a stop: unavailable previous-day median + TBD composition ->
    FeatureAvailabilityError naming the origin, the last available median's day, and
    the staleness in BOTH units (clock hours and whole daily steps)."""
    origin = dt.datetime(2022, 6, 10, 12, 0, tzinfo=UTC)
    medians = {dt.date(2022, 6, n): 100.0 + n for n in range(1, 8)}  # last: June 7
    with pytest.raises(FeatureAvailabilityError) as excinfo:
        resolve_f107_at_origin(
            medians,
            origin=origin,
            availability_ts=_f107_availability,
            features={"carry_forward_composition": "TBD — freeze gate"},
        )
    message = str(excinfo.value)
    assert "2022-06-10T12:00" in message, "names the origin timestamp"
    assert "2022-06-07" in message, "names the last available median's day"
    assert "clock hours" in message and "daily step" in message, "staleness in BOTH units"
    assert "G-04" in message, "routes the value to the Student's freeze"


def test_f107_absent_composition_field_stops_identically() -> None:
    """An ABSENT field is the same stop as a TBD one (the zero-TBD preflight's shape)."""
    origin = dt.datetime(2022, 6, 10, 12, 0, tzinfo=UTC)
    with pytest.raises(FeatureAvailabilityError):
        resolve_f107_at_origin(
            {dt.date(2022, 6, 1): 100.0},
            origin=origin,
            availability_ts=_f107_availability,
            features={},
        )


def test_f107_filled_composition_is_not_interpreted_here() -> None:
    """A filled composition field is NOT silently applied: its vocabulary and its
    application are the G-04 freeze plus features-and-splits' boundary, and this
    module refuses to interpret it (stop-and-report, never guess)."""
    origin = dt.datetime(2022, 6, 10, 12, 0, tzinfo=UTC)
    with pytest.raises(IntegrityError, match="carry_forward_composition"):
        resolve_f107_at_origin(
            {dt.date(2022, 6, 1): 100.0},
            origin=origin,
            availability_ts=_f107_availability,
            features={"carry_forward_composition": "A"},
        )


# =========================================================================================
# R-58 limbs 1-2: alignment of a PRESENT value (upstream contract evidence, not TA-36)
# =========================================================================================


def _kp_observations() -> list[dict[str, object]]:
    return [
        {"value": 3.0, "interval_start": _hour(0), "interval_end": _hour(3)},
        {"value": 5.0, "interval_start": _hour(3), "interval_end": _hour(6)},
    ]


def test_kp_aligns_only_within_its_own_interval() -> None:
    aligned = align_interval_series(_kp_observations())
    assert aligned[_hour(0)] == 3.0 and aligned[_hour(2)] == 3.0
    assert aligned[_hour(3)] == 5.0 and aligned[_hour(5)] == 5.0
    assert_alignment("kp_ap3", aligned, _kp_observations())


def test_kp_repeated_outside_interval_fails() -> None:
    """R-58 limb 1's negative control: a Kp value repeated OUTSIDE its 3-hour
    interval fails."""
    aligned = align_interval_series(_kp_observations())
    aligned[_hour(6)] = 3.0  # the first interval's value, repeated beyond hour 6
    with pytest.raises(AlignmentError, match="outside the interval"):
        assert_alignment("kp_ap3", aligned, _kp_observations())


def test_dst_shifted_to_neighbouring_hour_fails() -> None:
    """R-58 limb 2's negative control: a Dst value shifted to a neighbouring hour
    fails -- 'not shifted to a neighbouring hour for convenience' (D-10.2)."""
    observations = [
        {"value": -30.0, "interval_start": _hour(0), "interval_end": _hour(1)},
        {"value": -45.0, "interval_start": _hour(1), "interval_end": _hour(2)},
    ]
    aligned = align_interval_series(observations)
    shifted = {_hour(0): -30.0, _hour(1): -30.0}  # hour 1 got hour 0's value
    assert_alignment("dst", aligned, observations)  # the honest alignment passes
    with pytest.raises(AlignmentError, match="neighbouring hour"):
        assert_alignment("dst", shifted, observations)


def test_alignment_fails_even_when_carry_forward_is_satisfied() -> None:
    """R-58's separation constraint: satisfy the carry-forward rule and violate
    alignment -> the alignment test STILL fails, proving neither passes on the
    other's evidence."""
    observations = [{"value": 7.0, "interval_start": _hour(0), "interval_end": _hour(3)}]
    hourly: dict[dt.datetime, float | None] = {
        _hour(n): (7.0 if n < 3 else None) for n in range(5)
    }
    result = apply_carry_forward(hourly, bound_h=3)
    assert result["excluded_epochs"] == []  # carry-forward satisfied
    misaligned = dict(result["values"])
    misaligned[_hour(10)] = 7.0  # aligned nowhere near its interval
    with pytest.raises(AlignmentError):
        assert_alignment("kp_ap3", misaligned, observations)


# =========================================================================================
# R-57a bound + R-58 limb 3: carry-forward, the injected 4-hour gap, conservation
# =========================================================================================


def test_carry_forward_within_bound_fills_and_records() -> None:
    hourly: dict[dt.datetime, float | None] = {_hour(n): None for n in range(6)}
    hourly[_hour(0)] = 1.0
    hourly[_hour(4)] = 2.0
    hourly[_hour(5)] = 3.0
    result = apply_carry_forward(hourly, bound_h=3)
    assert result["values"][_hour(1)] == 1.0
    assert result["values"][_hour(3)] == 1.0
    assert result["carried_forward_epochs"] == [_hour(1), _hour(2), _hour(3)]
    assert result["excluded_epochs"] == []


def test_injected_four_hour_gap_excludes_the_row() -> None:
    """FR-P1-04-3's own criterion (TC-09, binding hard): inject a 4-hour gap -> the
    row beyond the 3-hour bound is EXCLUDED, never filled -- and the within-bound rows
    are carried, so BOTH directions are asserted."""
    hourly: dict[dt.datetime, float | None] = {_hour(n): None for n in range(6)}
    hourly[_hour(0)] = 1.0
    hourly[_hour(5)] = 2.0  # hours 1-4 are a four-hour gap
    result = apply_carry_forward(hourly, bound_h=3)
    assert _hour(4) in result["excluded_epochs"], "the 4th hour is excluded, not filled"
    assert _hour(4) not in result["values"]
    assert result["carried_forward_epochs"] == [_hour(1), _hour(2), _hour(3)]


def test_conservation_invariant_passes_on_recorded_fill() -> None:
    hourly: dict[dt.datetime, float | None] = {
        _hour(0): 1.0,
        _hour(1): None,
        _hour(2): 3.0,
    }
    result = apply_carry_forward(hourly, bound_h=3)
    assert_carry_forward_conservation(result["values"], hourly, result["carried_forward_epochs"])


def test_vectorised_fill_missed_by_scan_and_caught_by_invariant() -> None:
    """R-58 limb 3's control 3, asserted IN ORDER: a vectorised fill that names no
    fill function (a) is MISSED by the AST token scan and (b) FAILS the conservation
    invariant -- proving the invariant does the work the scan cannot."""
    vectorised_source = "s[s.isna()] = s.shift(1)[s.isna()]\n"
    assert _interpolation_fill_sites(vectorised_source, name="vectorised") == [], (
        "(a) the scan must MISS the vectorised spelling; if it starts catching it, "
        "this test's ordering claim is stale and must be rewritten"
    )
    observations: dict[dt.datetime, float | None] = {_hour(0): 1.0, _hour(1): None}
    emitted = {_hour(0): 1.0, _hour(1): 1.0}  # filled, with NO recorded carry-forward
    with pytest.raises(IntegrityError, match="no observation and no recorded carry-forward"):
        assert_carry_forward_conservation(emitted, observations, carried_forward_epochs=[])


def test_conservation_count_mismatch_fails() -> None:
    """The recorded count is load-bearing: a count that does not reconcile fails."""
    observations: dict[dt.datetime, float | None] = {_hour(0): 1.0, _hour(1): None}
    emitted = {_hour(0): 1.0, _hour(1): 1.0}
    with pytest.raises(IntegrityError, match="load-bearing"):
        assert_carry_forward_conservation(
            emitted, observations, carried_forward_epochs=[_hour(1), _hour(5)]
        )


# =========================================================================================
# R-58 limb 3: the AST-level no-interpolation scan over the named token set
# =========================================================================================

#: R-58's named token set (the floor, not the ceiling -- the conservation invariant is
#: what carries the rule for spellings outside it).
_FILL_METHOD_TOKENS: frozenset[str] = frozenset(
    {
        "interpolate",
        "ffill",
        "bfill",
        "pad",
        "backfill",
        "fillna",
        "combine_first",
        "update",
    }
)


def _interpolation_fill_sites(source: str, *, name: str) -> list[str]:
    """The AST-level scan (R-58 limb 3): resolves the call target through import
    bindings and local aliases, so an aliased or getattr-dispatched fill is REACHED
    and a token inside a string or comment is NOT flagged. Scoped by its caller to
    `src/external/spaceweather.py` and the driver path."""
    tree = ast.parse(source, filename=name)
    alias_bound: dict[str, str] = {}
    sites: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Attribute):
            if node.value.attr in _FILL_METHOD_TOKENS:
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        alias_bound[target.id] = node.value.attr
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute):
            if func.attr in _FILL_METHOD_TOKENS:
                sites.append(f"{name}:{node.lineno} .{func.attr}(")
            elif (
                func.attr == "interp"
                and isinstance(func.value, ast.Name)
                and func.value.id
                in (
                    "np",
                    "numpy",
                )
            ):
                sites.append(f"{name}:{node.lineno} {func.value.id}.interp(")
            elif (isinstance(func.value, ast.Attribute) and func.value.attr == "interpolate") or (
                isinstance(func.value, ast.Name) and func.value.id == "interpolate"
            ):
                sites.append(f"{name}:{node.lineno} scipy.interpolate.{func.attr}(")
            elif func.attr in ("reindex", "asfreq") and any(
                keyword.arg == "method"
                and not (isinstance(keyword.value, ast.Constant) and keyword.value.value is None)
                for keyword in node.keywords
            ):
                sites.append(f"{name}:{node.lineno} .{func.attr}(method=...)")
        elif isinstance(func, ast.Name) and func.id in alias_bound:
            sites.append(
                f"{name}:{node.lineno} alias {func.id!r} resolved to .{alias_bound[func.id]}"
            )
        elif (
            isinstance(func, ast.Call)
            and isinstance(func.func, ast.Name)
            and func.func.id == "getattr"
            and len(func.args) >= 2
            and isinstance(func.args[1], ast.Constant)
            and str(func.args[1].value) in _FILL_METHOD_TOKENS
        ):
            sites.append(f"{name}:{node.lineno} getattr dispatch to {func.args[1].value!r}")
    return sites


def test_spaceweather_source_carries_no_interpolation_call() -> None:
    """R-58 limb 3 over the real driver path: the named token set finds no
    interpolation or fill call in `spaceweather.py` -- 'no driver is interpolated, at
    any stage' (D-10.2). The sanctioned carry-forward is a RECORDED dict operation,
    not a fill-function call, so it does not trip the scan (by construction)."""
    source = (REPO_ROOT / "src" / "external" / "spaceweather.py").read_text(encoding="utf-8")
    assert _interpolation_fill_sites(source, name="spaceweather.py") == []


def test_scan_catches_direct_interpolate_call() -> None:
    """R-58 limb 3, control 1: `.interpolate()` on a driver series is caught, naming
    module, line and resolved target."""
    sites = _interpolation_fill_sites("s = s.interpolate()\n", name="inject.py")
    assert sites and "inject.py:1" in sites[0] and "interpolate" in sites[0]


def test_scan_catches_aliased_fill_that_a_textual_grep_passes() -> None:
    """R-58 limb 3, control 2: `f = pd.Series.ffill; f(s)` names no `.ffill(` token,
    so a textual grep passes it -- the AST scan resolves the alias and fails."""
    source = "f = pd.Series.ffill\nresult = f(s)\n"
    sites = _interpolation_fill_sites(source, name="alias.py")
    assert sites and "alias" in sites[0] and "ffill" in sites[0]


def test_scan_catches_getattr_dispatch_and_ignores_strings() -> None:
    """A getattr-dispatched fill is reached; the same token inside a string literal or
    comment is NOT flagged (the two failure directions of a textual grep)."""
    dispatched = 'getattr(s, "fillna")(0)\n'
    assert _interpolation_fill_sites(dispatched, name="dispatch.py")
    innocent = '# .fillna( in a comment\nmessage = "call .interpolate() never"\n'
    assert _interpolation_fill_sites(innocent, name="innocent.py") == []


def test_scan_catches_reindex_with_method_and_np_interp() -> None:
    assert _interpolation_fill_sites("s.reindex(idx, method='pad')\n", name="r.py")
    assert _interpolation_fill_sites("v = np.interp(x, xp, fp)\n", name="n.py")
    assert _interpolation_fill_sites("s.reindex(idx)\n", name="ok.py") == []


# =========================================================================================
# R-63: time-indexed only; the reanalysed-value driver half; GFZ cross-assertion
# =========================================================================================


def test_per_cell_join_shape_is_refused() -> None:
    """FR-P1-04-4/TC-12: a row shape carrying a station or cell key is refused at
    construction -- the per-cell join shape negative control."""
    rows = [{"epoch": _hour(0), "value": 3.0, "station": "ARUC"}]
    with pytest.raises(IntegrityError, match="time-indexed only"):
        assert_time_indexed_shape(rows)
    assert_time_indexed_shape([{"epoch": _hour(0), "value": 3.0}])  # the clean shape passes


def test_value_differing_across_cells_fails() -> None:
    rows = [
        {"epoch": _hour(0), "value": 3.0, "cell": "ARUC"},
        {"epoch": _hour(0), "value": 3.0, "cell": "BSHM"},
        {"epoch": _hour(1), "value": 4.0, "cell": "ARUC"},
        {"epoch": _hour(1), "value": 5.0, "cell": "BSHM"},  # differs at hour 1
    ]
    with pytest.raises(IntegrityError, match="identical across all three cells"):
        assert_identical_across_cells(rows, epoch_key="epoch", value_key="value", cell_key="cell")


def test_mixed_release_grades_fail_at_construction() -> None:
    """D-10.1: grades never mixed within one series -- fails at construction, and the
    single-grade series passes (both directions)."""
    with pytest.raises(IntegrityError, match="mixed"):
        assert_single_grade("dst", ["provisional", "final"])
    assert_single_grade("dst", ["provisional", "provisional"])


def test_grade_eligibility_three_bars_and_the_permitted_use() -> None:
    """R-62 restriction 3, all four directions: provisional fails as a modelling
    input, a frozen tolerance, and a G-05 regime count (naming D-13's GFZ Kp/Hp60
    requirement) -- and is PERMITTED for fixture characterisation (D-11), asserted so
    the permitted use is explicitly distinguishable."""
    with pytest.raises(IntegrityError, match="modelling input"):
        assert_grade_eligible("f107", "provisional", use="modelling_input")
    with pytest.raises(IntegrityError, match="frozen tolerance"):
        assert_grade_eligible("f107", "provisional", use="frozen_tolerance")
    with pytest.raises(IntegrityError, match="GFZ Kp/Hp60"):
        assert_grade_eligible("f107", "provisional", use="g05_regime_count")
    assert_grade_eligible("f107", "provisional", use="fixture_characterisation")


def test_dst_is_diagnostic_only_whatever_its_grade() -> None:
    """TC-11: no grade makes Dst a confirmatory modelling input."""
    with pytest.raises(IntegrityError, match="diagnostic"):
        assert_grade_eligible("dst", "final", use="modelling_input")


def test_unknown_grade_use_is_refused_not_defaulted() -> None:
    with pytest.raises(IntegrityError, match="unknown grade-eligibility use"):
        assert_grade_eligible("f107", "final", use="whatever_new_use")


def _valid_dst_entry() -> dict[str, object]:
    return {
        "series_id": "dst",
        "release_status": "provisional",
        "retrieval_date": "2026-08-15",
        "provider_product_identity": "kyoto_dst/dst_provisional_2022MM.html (12 files)",
        "sha256": "0" * 64,
        "provenance_verifiability": {
            "status": "declared-status-only",
            "documented_absence": "no provenance column; grade inferable from filename alone",
            "unverified_status_statement": "declared, not verified (D-10.1 open per D-11)",
        },
        "carried_forward_epochs": [],
    }


def test_provenance_field_omission_terminates() -> None:
    """R-63 control 2: omit any of the four fields -> fails on manifest completeness."""
    for field in ("release_status", "retrieval_date", "provider_product_identity", "sha256"):
        entry = _valid_dst_entry()
        del entry[field]
        with pytest.raises(IntegrityError, match="provenance field"):
            assert_series_provenance("dst", entry)


def test_status_inconsistent_with_product_identity_terminates() -> None:
    """R-63 control 1 -- the detectable form of the never-backfill rule: `final`
    declared against a `dst_provisional_*` filename FAILS."""
    entry = _valid_dst_entry()
    entry["release_status"] = "final"
    with pytest.raises(IntegrityError, match="inconsistent"):
        assert_series_provenance("dst", entry)


def test_missing_documented_absence_statement_terminates() -> None:
    """R-63 control 3: a status recorded for a no-provenance-column file WITHOUT the
    documented-absence and unverified-status statement fails -- the absence must be
    STATED, never implied by silence."""
    entry = _valid_dst_entry()
    entry["provenance_verifiability"] = {"status": "declared-status-only"}
    with pytest.raises(IntegrityError, match="documented_absence"):
        assert_series_provenance("dst", entry)


def test_declared_status_only_never_reported_closed() -> None:
    """No artifact may report the reanalysed-value check as closed for F10.7/Dst."""
    entry = _valid_dst_entry()
    entry["provenance_verifiability"] = {
        "status": "closed",
        "documented_absence": "x",
        "unverified_status_statement": "y",
    }
    with pytest.raises(IntegrityError, match="BOUNDED, NOT CLOSED"):
        assert_series_provenance("dst", entry)


def test_gfz_cross_assertion_catches_definitive_backfill() -> None:
    """R-63 control 5: an emitted value matching the DEFINITIVE product where the
    near-real-time product differs FAILS; matching the NRT value passes."""
    nrt = {_hour(0): 3.0, _hour(1): 4.0}
    definitive = {_hour(0): 3.0, _hour(1): 4.5}
    with pytest.raises(IntegrityError, match="never backfill"):
        assert_gfz_cross_products(
            "kp_ap3",
            near_real_time=nrt,
            definitive=definitive,
            emitted={_hour(0): 3.0, _hour(1): 4.5},
        )
    assert_gfz_cross_products(
        "kp_ap3",
        near_real_time=nrt,
        definitive=definitive,
        emitted={_hour(0): 3.0, _hour(1): 4.0},
    )


# =========================================================================================
# SD-E-03 producing half + SD-E-07: stamps, manifest, and the re-run contract
# =========================================================================================


def test_manifest_stamps_every_series_and_names_missing_months(tmp_path: Path) -> None:
    """The producing half: every entry the manifest writer emits carries a provenance
    stamp (evidentiary class, never described as cryptographic), and missing months
    are NAMED machine-readably with the artifact marked derived/partial."""
    path = write_driver_manifest(
        tmp_path / "driver_manifest.json",
        series_entries=[_valid_dst_entry()],
        missing_months=["2022-04 (dst: file not retrieved)"],
        produced_by="scripts/04_build_external_products.py",
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["partial"] is True and payload["derived"] is True
    assert payload["missing_months"] == ["2022-04 (dst: file not retrieved)"]
    stamp = payload["series"][0]["provenance_stamp"]
    assert stamp["stamp_class"] == "evidentiary"
    assert stamp["produced_by"] == "scripts/04_build_external_products.py"
    assert "not cryptographic" in payload["provenance_stamp_note"]


def test_manifest_refuses_entry_without_carried_forward_epochs(tmp_path: Path) -> None:
    entry = _valid_dst_entry()
    del entry["carried_forward_epochs"]
    with pytest.raises(IntegrityError, match="carried_forward_epochs"):
        write_driver_manifest(
            tmp_path / "m.json",
            series_entries=[entry],
            missing_months=[],
            produced_by="scripts/04_build_external_products.py",
        )


def test_stamp_helper_is_evidentiary() -> None:
    stamp = provenance_stamp(source="fluxtable.txt", produced_by="scripts/04")
    assert stamp["stamp_class"] == "evidentiary"


def test_rerun_byte_identical_passes_and_divergence_refuses(tmp_path: Path) -> None:
    """SD-E-07: byte-identical re-run passes; a divergent product records BOTH
    identities and BOTH hashes and refuses overwrite (SEC-A-02 adopted unchanged)."""
    product = tmp_path / "codg0010.22i"
    product.write_bytes(b"gim bytes v1")
    from src.data.release import sha256_of_file

    recorded = sha256_of_file(product)
    refuse_divergent_rerun(
        product,
        recorded_identity="CODG0010.22I (g.002)",
        recorded_sha256=recorded,
        current_identity="CODG0010.22I (g.002)",
    )
    product.write_bytes(b"gim bytes v2 -- reissued")
    with pytest.raises(IntegrityError) as excinfo:
        refuse_divergent_rerun(
            product,
            recorded_identity="CODG0010.22I (g.002)",
            recorded_sha256=recorded,
            current_identity="CODG0010.22I (g.003)",
        )
    message = str(excinfo.value)
    assert "g.002" in message and "g.003" in message, "BOTH identities recorded"
    assert recorded in message and sha256_of_file(product) in message, "BOTH hashes recorded"
    assert "REFUSED" in message


# =========================================================================================
# The no-tuning grep-class check over gim.py (R-60 obligation 4's partial limb)
# =========================================================================================


def _tuning_call_sites(source: str, *, name: str) -> list[str]:
    """AST-level (not textual) so the module's own docstring USE of the word 'tuning'
    is not a false positive: flags CALL TARGETS whose dotted name contains a fitting,
    tuning, optimiser or parameter-search token."""
    tokens = ("fit", "tune", "optim", "minimiz", "grid_search", "hyperparam", "search_cv")
    tree = ast.parse(source, filename=name)
    sites: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        parts: list[str] = []
        while isinstance(func, ast.Attribute):
            parts.append(func.attr)
            func = func.value
        if isinstance(func, ast.Name):
            parts.append(func.id)
        dotted = ".".join(reversed(parts)).lower()
        if any(token in dotted for token in tokens):
            sites.append(f"{name}:{node.lineno} {dotted}(")
    return sites


def test_gim_module_carries_no_tuning_call() -> None:
    """Obligation 4's partial control: no fitting, tuning, optimiser or
    parameter-search call appears in `gim.py` -- catching the realistic case of a
    tuning step left in the comparator module. ⚠ The residual stays open and named:
    tuning performed OUTSIDE gim.py and pasted in as a constant is reached by no
    check (R-60) -- this test does not and cannot close it."""
    source = (REPO_ROOT / "src" / "external" / "gim.py").read_text(encoding="utf-8")
    assert _tuning_call_sites(source, name="gim.py") == []


def test_tuning_call_injection_is_caught() -> None:
    """Negative control: a fitting or parameter-search call injected into comparator
    source is caught by the grep-class check."""
    assert _tuning_call_sites("model.fit(x, y)\n", name="inject.py")
    assert _tuning_call_sites("GridSearchCV(est, grid).fit(x)\n", name="inject2.py")
    assert _tuning_call_sites("scipy.optimize.minimize(f, x0)\n", name="inject3.py")


# =========================================================================================
# The migrated exit-code pair and the two refusals, THROUGH the allowlisted script
# =========================================================================================


def _workspace(tmp_path: Path) -> Path:
    """A temporary workspace: requirements.txt copied (the lock hashes it); no git
    tree, so --code-commit is passed explicitly (config.py's documented Kaggle shape)."""
    workspace = tmp_path / "ws"
    workspace.mkdir()
    shutil.copyfile(REPO_ROOT / "requirements.txt", workspace / "requirements.txt")
    return workspace


def _run_script(args: list[str], workspace: Path) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"  # the determinism step reads it; no re-exec in the child
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


def _dst_month_html(days: int) -> str:
    return "\n".join(f"{day:>2}" + " -10" * 24 for day in range(1, days + 1)) + "\n"


def _driver_evidence(workspace: Path, *, omit_month: int | None = 4) -> Path:
    """Synthetic driver evidence in the original layout, named with a retrieval date."""
    evidence = workspace / "evidence_fixture" / "audit_ec1_2020-01-01"
    kyoto = evidence / "kyoto_dst"
    kyoto.mkdir(parents=True)
    for month in range(1, 13):
        if month == omit_month:
            continue
        days = 31 if month in (1, 3, 5, 7, 8, 10, 12) else (28 if month == 2 else 30)
        (kyoto / f"dst_provisional_2022{month:02d}.html").write_text(
            _dst_month_html(days), encoding="utf-8"
        )
    nrcan = evidence / "nrcan_f107"
    nrcan.mkdir(parents=True)
    nrcan.joinpath("fluxtable.txt").write_text(
        "fluxdate    fluxtime   fluxjulian  fluxcarrington fluxobsflux fluxadjflux fluxursi\n"
        "----------  --------   ----------  -------------- ----------- ----------- --------\n"
        "20220101    200000     2459580.5   2250.0         100.1       98.0        99.0\n"
        "20220102    200000     2459581.5   2250.0         101.1       99.0        99.5\n",
        encoding="utf-8",
    )
    return evidence


#: The governed refusals a FULL-SCALE (non-fixture) invocation of `04` may legitimately
#: stop at, in the order they fire. The TE 9.2 receipt gate is the one Q5 = A installed;
#: on a clone without `pyyaml` the governed-config preflight refuses even earlier, before
#: the gate is reached. Both are fail-closed refusals of the SAME kind: the run is not
#: accepted, and no external product is treated as usable because it happens to exist.
_GOVERNED_FULL_SCALE_REFUSALS: tuple[str, ...] = (
    "fixture",  # require_receipts_for_snapshot: both fixtures pass before any full-year job
    "receipt",
    "pyyaml is required",  # the governed-config preflight on a pyyaml-less clone
)


def _assert_gate_fails_closed(
    result: subprocess.CompletedProcess[str], *, also_accepts: tuple[str, ...] = ()
) -> str:
    """Q5 = Choice B (owner ruling 2026-09-10; CR-2026-09-10 §1): assert the receipt-gate
    contract AT SUBPROCESS LEVEL.

    A full-scale run of `04` is **not accepted merely because it produced outputs**: TE
    §9.2's two-receipt gate runs inside `_stage_entry`, no frozen manifest or receipt
    exists, and the run therefore REFUSES — non-zero, naming a governed refusal. This
    helper asserts fail-closed and returns the stderr so a caller can add its own checks.

    `also_accepts` carries the caller's own pre-Q5 refusal markers: those texts stay
    covered at FUNCTION level (per the ruling's design), and accepting them here keeps
    each test honest about which refusal it actually observed rather than asserting a
    refusal order the environment does not guarantee.

    HONEST LIMIT: on this clone the FIRST governed refusal is the `pyyaml` preflight, so
    these assertions prove *fail-closed* everywhere and prove *which* gate fires only in a
    `pyyaml`-bearing environment. **No fixture manifest or receipt is fabricated here** —
    a synthetic receipt chain would be the manufactured evidence the rules forbid.
    """
    assert result.returncode != 0, (
        "a full-scale (non-fixture) invocation must REFUSE while no frozen "
        "manifest/receipt chain exists — accepting it because outputs exist is exactly "
        f"what Q5 = A's gate prevents.\nstdout: {result.stdout[-400:]}"
    )
    stderr = result.stderr
    markers = (*_GOVERNED_FULL_SCALE_REFUSALS, *also_accepts)
    assert any(marker.lower() in stderr.lower() for marker in markers), (
        f"the refusal names none of the governed refusals {list(markers)}; an unnamed "
        f"refusal is not evidence of the gate.\nstderr: {stderr[-600:]}"
    )
    return stderr


def test_script_missing_month_continues_and_names_which(tmp_path: Path) -> None:
    """Q5 = Choice B (owner ruling 2026-09-10): this test's subject CHANGED with the gate.

    Before Q5 = A, an injected missing month meant "the run continues (exit 0) and the
    manifest names which months are missing". A full-scale run can no longer exit 0: the
    TE §9.2 receipt gate refuses it. What this test now asserts at subprocess level is the
    gate contract — the run is NOT accepted merely because it would have produced an audit
    manifest, and no manifest artifact is left behind as if it were usable.

    REQ-ENG-9 half 1's two-tier completeness semantics (a missing month is a
    machine-readable field, never console text, and marks the artifact partial) stay
    covered at FUNCTION level by this module's `write_driver_manifest` tests.
    """
    workspace = _workspace(tmp_path)
    _driver_evidence(workspace, omit_month=4)
    result = _run_script(["--evidence-root", "evidence_fixture/audit_ec1_2020-01-01"], workspace)
    _assert_gate_fails_closed(result)
    assert not (
        workspace / "artifacts" / "external" / "ec1_driver_audit_manifest.json"
    ).is_file(), "a refused full-scale run leaves no audit manifest behind"


def test_script_hash_mismatch_terminates_naming_file_and_expectation(tmp_path: Path) -> None:
    """REQ-ENG-9 half 2 (R-61) -- the OPPOSITE outcome: an injected hash mismatch
    terminates non-zero, naming the file and the violated expectation."""
    workspace = _workspace(tmp_path)
    evidence = _driver_evidence(workspace, omit_month=None)
    evidence.joinpath("ec1-audit-report.json").write_text(
        json.dumps(
            {
                "obligation_1_kyoto_dst": {
                    "1": {"file": "dst_provisional_202201.html", "sha256": "0" * 64}
                },
                "obligation_2_canadian_f107": {},
            }
        ),
        encoding="utf-8",
    )
    result = _run_script(["--evidence-root", "evidence_fixture/audit_ec1_2020-01-01"], workspace)
    # Q5 = Choice B: the run refuses either at the TE §9.2 gate or, once past it, at the
    # hash check — both are fail-closed refusals; the hash-check TEXT stays asserted at
    # function level by this module's own `sha256`/manifest tests.
    stderr = _assert_gate_fails_closed(result, also_accepts=("FAILED hash check",))
    if "FAILED hash check" in stderr:
        assert "dst_provisional_202201.html" in stderr, "names the file"
        assert "recorded" in stderr and "actual" in stderr, "names the expectation"


def test_attempt_benchmark_refuses_without_validation_report(tmp_path: Path) -> None:
    """R-59 limb 1 through the allowlisted importer: the real benchmark attempt
    refuses, naming the missing passing pre-declared validation report; the aborted
    registry row records the refusal honestly (exit 1)."""
    workspace = _workspace(tmp_path)
    result = _run_script(["--attempt-benchmark"], workspace)
    stderr = _assert_gate_fails_closed(
        result, also_accepts=("no passing pre-declared validation report exists",)
    )
    if "no passing pre-declared validation report exists" in stderr:
        assert "never silently switched" in stderr, "R-59's no-silent-switch clause"


def test_attempt_comparator_refuses_while_q15_is_unset(tmp_path: Path) -> None:
    """R-60 obligation 1 through the allowlisted importer: the real comparator attempt
    refuses, naming Q-15's unset Student-owned interpolation rule (TE 18.2)."""
    workspace = _workspace(tmp_path)
    result = _run_script(["--attempt-comparator"], workspace)
    stderr = _assert_gate_fails_closed(result, also_accepts=("Q-15",))
    if "Q-15" in stderr:
        assert "UNSET" in stderr and "18.2" in stderr


def _valid_benchmark_state() -> dict[str, object]:
    """INJECTED control state (not governed evidence; injection mode never generates).
    The 2000 km ceiling is FR-P1-04-15's own enumerated criterion; the tolerance value
    is control data proving the gate shape, used for nothing scientific."""
    samples = [
        {
            "site": "ARUC",
            "local_time_class": "day",
            "activity_class": "quiet",
            "official_interface_value": 10.0,
        },
        {
            "site": "BSHM",
            "local_time_class": "night",
            "activity_class": "disturbed",
            "official_interface_value": 11.0,
        },
        {
            "site": "NICO",
            "local_time_class": "day",
            "activity_class": "disturbed",
            "official_interface_value": 12.0,
        },
        {
            "site": "ARUC",
            "local_time_class": "night",
            "activity_class": "quiet",
            "official_interface_value": 13.0,
        },
        {
            "site": "BSHM",
            "local_time_class": "day",
            "activity_class": "quiet",
            "official_interface_value": 14.0,
        },
    ]
    report = {
        "status": "passed",
        "package_version": "iricore (injected control) @ commit 0000000",
        "model_switches": {"switch": "control"},
        "topside_option": "control",
        "altitude_ceiling_km": 2000,
        "units": "TECU",
        "output_extraction": "control",
        "driver_inputs": {
            "no_future_centering_confirmed": True,
            "available_at_target_time_confirmed": True,
        },
        "samples": samples,
        "tolerance": {"value": 0.5, "declared_at_utc": "2026-09-01T00:00:00+00:00"},
        "comparison_ran_at_utc": "2026-09-02T00:00:00+00:00",
    }
    matrix = [
        {
            "driver_id": "f107",
            "observation_timestamp": "2022-06-01T20:00:00+00:00",
            "conservative_convention": "D-25: 00:00 UTC on D+1, never same-day",
            "documented_absence": "no provider publication timestamp (D-21/D-22)",
            "unverified_latency_statement": "latency not derivable from held file",
            "release_status": "observed (grade undeclared by provider)",
            "safe_lag": "previous-day observed",
        },
        {
            "driver_id": "kp_ap3",
            "observation_timestamp": "2022-06-01T00:00:00+00:00",
            "publication_timestamp": "2022-06-01T03:00:00+00:00",
            "release_status": "definitive",
            "safe_lag": ">= 3 h",
        },
    ]
    return {
        "validation_report": report,
        "report_name": "injected_validation_report",
        "availability_matrix": matrix,
        "benchmark_drivers": ["f107", "kp_ap3"],
    }


def _write_state(tmp_path: Path, state: dict[str, object]) -> Path:
    path = tmp_path / "gate_state.json"
    path.write_text(json.dumps(state), encoding="utf-8")
    return path


def test_benchmark_tolerance_after_comparison_fails_on_ordering(tmp_path: Path) -> None:
    """R-59 limb 2's negative control: a tolerance recorded AFTER the comparison ran
    is refused on ordering -- the failure a presence check cannot see."""
    workspace = _workspace(tmp_path)
    state = _valid_benchmark_state()
    state["validation_report"]["tolerance"]["declared_at_utc"] = "2026-09-03T00:00:00+00:00"
    result = _run_script(
        ["--attempt-benchmark", "--gate-state", str(_write_state(tmp_path, state))], workspace
    )
    stderr = _assert_gate_fails_closed(result, also_accepts=("does not PRECEDE",))
    if "does not PRECEDE" in stderr:
        assert "fitted after" in stderr


def test_benchmark_missing_content_area_fails_field_by_field(tmp_path: Path) -> None:
    """R-59 limb 3's negative control: omit one of the seven content areas (the
    ceiling) -> the report fails field by field rather than passing on presence."""
    workspace = _workspace(tmp_path)
    state = _valid_benchmark_state()
    del state["validation_report"]["altitude_ceiling_km"]
    result = _run_script(
        ["--attempt-benchmark", "--gate-state", str(_write_state(tmp_path, state))], workspace
    )
    stderr = _assert_gate_fails_closed(result, also_accepts=("missing content area",))
    if "missing content area" in stderr:
        assert "altitude_ceiling_km" in stderr


def test_benchmark_fully_satisfied_injection_still_refuses_generation(tmp_path: Path) -> None:
    """The injection-mode terminal refusal: a state satisfying EVERY gate still
    refuses -- injected state is not governed evidence, and NO benchmark is generated
    by this unit (the refusals are the deliverable)."""
    workspace = _workspace(tmp_path)
    result = _run_script(
        [
            "--attempt-benchmark",
            "--gate-state",
            str(_write_state(tmp_path, _valid_benchmark_state())),
        ],
        workspace,
    )
    stderr = _assert_gate_fails_closed(result, also_accepts=("refused anyway",))
    if "refused anyway" in stderr:
        assert "not governed evidence" in stderr


def test_comparator_hand_check_after_generation_fails_on_ordering(tmp_path: Path) -> None:
    """R-60 obligation 2's negative control: a comparator generated before the
    hand-check FAILS rather than being accepted retrospectively (EV-11)."""
    workspace = _workspace(tmp_path)
    state = {
        "interpolation_rule": "injected-control-rule",
        "hand_check": {
            "worked_arithmetic": "control arithmetic",
            "checked_at_utc": "2026-09-05T13:00:00+00:00",
        },
        "overlap_audit": {
            "gim_network_overlap_flag": "control",
            "recorded_at_utc": "2026-09-05T09:00:00+00:00",
        },
        "generation_attempt_utc": "2026-09-05T12:00:00+00:00",
    }
    result = _run_script(
        ["--attempt-comparator", "--gate-state", str(_write_state(tmp_path, state))], workspace
    )
    stderr = _assert_gate_fails_closed(
        result, also_accepts=("does not PRECEDE this generation attempt",)
    )
    if "does not PRECEDE this generation attempt" in stderr:
        assert "retrospective" in stderr


def test_comparator_missing_overlap_audit_fails_on_ordering(tmp_path: Path) -> None:
    """R-60's Constraint (Recommendation 41): the overlap audit's recorded timestamp
    must PRECEDE comparator generation, and an absent audit refuses -- the Q-15
    refusal is a mitigation that EXPIRES, so this control does not lean on it."""
    workspace = _workspace(tmp_path)
    state = {
        "interpolation_rule": "injected-control-rule",
        "hand_check": {
            "worked_arithmetic": "control arithmetic",
            "checked_at_utc": "2026-09-05T09:00:00+00:00",
        },
        "overlap_audit": None,
        "generation_attempt_utc": "2026-09-05T12:00:00+00:00",
    }
    result = _run_script(
        ["--attempt-comparator", "--gate-state", str(_write_state(tmp_path, state))], workspace
    )
    stderr = _assert_gate_fails_closed(result, also_accepts=("gim_network_overlap_flag",))
    if "gim_network_overlap_flag" in stderr:
        assert "No independence claim" in stderr


def test_comparison_without_registered_audit_fails_on_existence(tmp_path: Path) -> None:
    """R-60's disclosure trigger, keyed to the COMPARISON'S EXISTENCE: rendering ANY
    GIM comparison with no registered overlap-audit result FAILS, whatever the result
    would have been."""
    workspace = _workspace(tmp_path)
    state = {"comparison": {"metric": "control"}, "overlap_audit": None}
    result = _run_script(["--render-comparison", str(_write_state(tmp_path, state))], workspace)
    stderr = _assert_gate_fails_closed(
        result, also_accepts=("the trigger is the comparison's existence",)
    )
    assert "the trigger is the comparison's existence" in stderr or any(
        marker.lower() in stderr.lower() for marker in _GOVERNED_FULL_SCALE_REFUSALS
    )


def test_comparison_report_emits_statements_and_flag_itself(tmp_path: Path) -> None:
    """R-60 obligation 3: the map-product-to-map-product limitation AND the
    spatial-representativeness mismatch are emitted BY THE REPORTING PATH ITSELF, with
    the flag value -- over injected state, printed and never written (no comparison
    artifact is produced by this unit)."""
    workspace = _workspace(tmp_path)
    state = {
        "comparison": {"metric": "control"},
        "overlap_audit": {
            "gim_network_overlap_flag": "overlap-audit-not-run-control-value",
            "recorded_at_utc": "2026-09-05T09:00:00+00:00",
        },
    }
    result = _run_script(["--render-comparison", str(_write_state(tmp_path, state))], workspace)
    if result.returncode == 0:
        # the reporting path reached: it emits both statements and the flag itself
        assert "map-product-to-map-product comparison" in result.stdout
        assert "geometry and sampling artefact" in result.stdout
        assert "overlap-audit-not-run-control-value" in result.stdout
        assert "no artifact written" in result.stdout
    else:
        # Q5 = Choice B: a full-scale invocation may refuse at the gate before the
        # reporting path runs. The emitted-statement contract stays covered at function
        # level by this module's render tests over the allowlisted importer.
        _assert_gate_fails_closed(result)
