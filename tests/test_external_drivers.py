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
from typing import Any

import pytest
from src.data.config import AlignmentError, FeatureAvailabilityError, IntegrityError
from src.external.spaceweather import (
    F107Selection,
    align_interval_series,
    apply_carry_forward,
    assert_alignment,
    assert_carry_forward_conservation,
    assert_gfz_cross_products,
    assert_grade_eligible,
    assert_identical_across_cells,
    assert_lagged_selection,
    assert_series_provenance,
    assert_single_grade,
    assert_time_indexed_shape,
    availability_rows_from_selection,
    daily_medians_from_readings,
    provenance_stamp,
    refuse_divergent_rerun,
    resolve_f107_at_origin,
    select_lagged_series,
    trailing_mean,
    write_driver_manifest,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "04_build_external_products.py"
UTC = dt.timezone.utc

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
    sel = resolve_f107_at_origin(
        medians,
        origin=origin,
        availability_ts=_f107_availability,
        features={"carry_forward_composition": "TBD — freeze gate"},
    )
    assert sel.source_day == dt.date(2022, 6, 9)
    assert sel.value == 109.0
    assert not sel.carried_forward and not sel.excluded and sel.staleness_hours == 0.0


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
    """A composition value outside the frozen vocabulary (`clock_hours`, D-46) is NOT
    interpreted: this module applies the Student's freeze only, never a reading of its
    own (stop-and-report, never guess)."""
    origin = dt.datetime(2022, 6, 10, 12, 0, tzinfo=UTC)
    with pytest.raises(IntegrityError, match="carry_forward_composition"):
        resolve_f107_at_origin(
            {dt.date(2022, 6, 1): 100.0},
            origin=origin,
            availability_ts=_f107_availability,
            features={"carry_forward_composition": "A"},
        )


# =========================================================================================
# D-46 (A3 = reading B): the missing-update composition in CLOCK HOURS, inclusive boundary
# =========================================================================================

_B = {"carry_forward_composition": "clock_hours", "carry_forward_bound_hours": 3}


def test_f107_ordinary_reuse_of_the_designated_value_is_not_carry_forward() -> None:
    """median(D-1) at every origin hour of D: source_day D-1, not carried, staleness 0."""
    medians = {dt.date(2022, 3, 13): 110.0, dt.date(2022, 3, 14): 120.0}
    for hour in range(24):
        sel = resolve_f107_at_origin(
            medians,
            origin=dt.datetime(2022, 3, 15, hour, tzinfo=UTC),
            availability_ts=_f107_availability,
            features=_B,
        )
        assert sel == F107Selection(dt.date(2022, 3, 14), 120.0, False, False, 0.0)


def test_f107_missing_update_allows_three_clock_hours_inclusive_then_excludes() -> None:
    """The designated median(03-15) is absent at 00:00 03-16: median(03-14) is carried
    at 00:00, 01:00, 02:00 and 03:00 (INCLUSIVE boundary, clock from the EXPECTED
    availability instant 00:00 03-16), origins 04:00 … 23:00 are excluded — 20 of 24
    rows; a valid update (median(03-16)) restores ordinary reuse on 03-17."""
    medians = {dt.date(2022, 3, 14): 120.0, dt.date(2022, 3, 16): 130.0}
    kept, excluded = [], []
    for hour in range(24):
        sel = resolve_f107_at_origin(
            medians,
            origin=dt.datetime(2022, 3, 16, hour, tzinfo=UTC),
            availability_ts=_f107_availability,
            features=_B,
        )
        if sel.excluded:
            excluded.append(hour)
            assert sel.value is None and sel.source_day is None and not sel.carried_forward
        else:
            kept.append(hour)
            assert sel == F107Selection(dt.date(2022, 3, 14), 120.0, True, False, float(hour))
    assert kept == [0, 1, 2, 3] and excluded == list(range(4, 24))
    restored = resolve_f107_at_origin(
        medians,
        origin=dt.datetime(2022, 3, 17, 5, tzinfo=UTC),
        availability_ts=_f107_availability,
        features=_B,
    )
    assert restored == F107Selection(dt.date(2022, 3, 16), 130.0, False, False, 0.0)


def test_f107_clock_starts_at_the_expected_instant_not_the_carried_value() -> None:
    """Two consecutive missing days: on 03-17 the clock restarts at 00:00 03-17 for the
    missing median(03-16), so median(03-14) is carried again at 00:00-03:00 of 03-17
    (staleness measured from 00:00 03-17), then excluded — the bound is on the
    missing-update clock, not on the carried value's age. A NaN median counts as
    missing (D-5); no median at all → excluded."""
    medians = {dt.date(2022, 3, 14): 120.0, dt.date(2022, 3, 16): float("nan")}
    sel = resolve_f107_at_origin(
        medians,
        origin=dt.datetime(2022, 3, 17, 3, tzinfo=UTC),
        availability_ts=_f107_availability,
        features=_B,
    )
    assert sel == F107Selection(dt.date(2022, 3, 14), 120.0, True, False, 3.0)
    assert resolve_f107_at_origin(
        medians,
        origin=dt.datetime(2022, 3, 17, 4, tzinfo=UTC),
        availability_ts=_f107_availability,
        features=_B,
    ).excluded
    assert resolve_f107_at_origin(
        {},
        origin=dt.datetime(2022, 3, 17, 1, tzinfo=UTC),
        availability_ts=_f107_availability,
        features=_B,
    ).excluded


def test_f107_frozen_composition_needs_the_configured_bound_and_refuses_other_vocab() -> None:
    medians = {dt.date(2022, 3, 14): 120.0}
    origin = dt.datetime(2022, 3, 16, 1, tzinfo=UTC)
    with pytest.raises(FeatureAvailabilityError, match="carry_forward_bound_hours"):
        resolve_f107_at_origin(
            medians,
            origin=origin,
            availability_ts=_f107_availability,
            features={"carry_forward_composition": "clock_hours"},
        )
    with pytest.raises(IntegrityError, match="clock_hours"):
        resolve_f107_at_origin(
            medians,
            origin=origin,
            availability_ts=_f107_availability,
            features={"carry_forward_composition": "daily_step", "carry_forward_bound_hours": 3},
        )


# =========================================================================================
# D-21 / D-22: the project-derived daily median
# =========================================================================================


def test_daily_median_is_the_median_of_slot_values_after_duplicate_averaging() -> None:
    """Three slots → the middle value; a duplicated slot is averaged first (D-22) and
    counted; a high-spread day is flagged and RETAINED (D-23); no reading is dropped."""
    readings = [
        {"day": dt.date(2022, 3, 26), "time": "170000", "value": 100.0},
        {"day": dt.date(2022, 3, 26), "time": "200000", "value": 102.0},
        {"day": dt.date(2022, 3, 26), "time": "230000", "value": 104.0},
        {"day": dt.date(2022, 3, 26), "time": "230000", "value": 106.0},  # duplicate slot
        {"day": dt.date(2022, 3, 31), "time": "170000", "value": 148.7},
        {"day": dt.date(2022, 3, 31), "time": "200000", "value": 239.5},
        {"day": dt.date(2022, 3, 31), "time": "230000", "value": 149.8},
    ]
    out = daily_medians_from_readings(readings)
    assert out["medians"][dt.date(2022, 3, 26)] == 102.0
    assert out["duplicate_days"] == {dt.date(2022, 3, 26): 1}
    assert out["medians"][dt.date(2022, 3, 31)] == 149.8
    assert set(out["high_spread_days"]) == {dt.date(2022, 3, 31)}


# =========================================================================================
# D-43 / D-44: lagged selection for interval-valued indices — the ONE owner of the lag
# =========================================================================================


def _kp_obs(day: dt.date, *, missing_slot: int | None = None) -> list[dict[str, Any]]:
    """Eight 3-hour Kp intervals of `day`, value = 10 + slot; provider boundaries kept."""
    base = dt.datetime.combine(day, dt.time(0), tzinfo=UTC)
    return [
        {
            "value": (None if k == missing_slot else 10.0 + k),
            "interval_start": base + dt.timedelta(hours=3 * k),
            "interval_end": base + dt.timedelta(hours=3 * k + 3),
        }
        for k in range(8)
    ]


def _hp_obs(day: dt.date) -> list[dict[str, Any]]:
    base = dt.datetime.combine(day, dt.time(0), tzinfo=UTC)
    return [
        {
            "value": 1.0 + h / 10.0,
            "interval_start": base + dt.timedelta(hours=h),
            "interval_end": base + dt.timedelta(hours=h + 1),
        }
        for h in range(24)
    ]


def _epochs(day: dt.date) -> list[dt.datetime]:
    base = dt.datetime.combine(day, dt.time(0), tzinfo=UTC)
    return [base + dt.timedelta(hours=h) for h in range(24)]


def test_kp_selection_at_and_before_the_availability_boundary() -> None:
    """Kp [00,03) completes at 03:00; with the 3 h margin it is eligible at 06:00 and not
    at 05:00; [03,06) is eligible from 09:00. Each selected value keeps its provider
    interval boundaries and its available_at = end + 3 h; the value is unchanged."""
    day = dt.date(2022, 6, 10)
    rows = {
        r["interval_start_utc"]: r
        for r in select_lagged_series(_kp_obs(day), epochs=_epochs(day), safe_lag_hours=3)
    }
    at = lambda h: rows[dt.datetime.combine(day, dt.time(h), tzinfo=UTC).isoformat()]  # noqa: E731
    assert at(5)["value"] is None and at(5)["source_interval_end_utc"] is None
    assert at(6)["value"] == 10.0
    assert at(6)["source_interval_start_utc"] == f"{day}T00:00:00+00:00"
    assert at(6)["source_interval_end_utc"] == f"{day}T03:00:00+00:00"
    assert at(6)["available_at_utc"] == f"{day}T06:00:00+00:00"
    assert at(8)["value"] == 10.0  # [03,06) ended 06:00: not yet 3 h old
    assert at(9)["value"] == 11.0 and at(9)["source_interval_end_utc"] == f"{day}T06:00:00+00:00"
    assert at(23)["value"] == 15.0  # [15,18) ends 18:00, +3 h = 21:00 ≤ 23:00; [18,21) not yet
    assert_lagged_selection("kp", list(rows.values()), _kp_obs(day), safe_lag_hours=3)


def test_hp60_selection_at_and_before_the_availability_boundary() -> None:
    day = dt.date(2022, 6, 10)
    rows = select_lagged_series(_hp_obs(day), epochs=_epochs(day), safe_lag_hours=1)
    by = {r["interval_start_utc"]: r for r in rows}
    five = by[f"{day}T05:00:00+00:00"]
    six = by[f"{day}T06:00:00+00:00"]
    assert five["source_interval_end_utc"] == f"{day}T04:00:00+00:00"  # [03,04) at 05:00
    assert six["source_interval_end_utc"] == f"{day}T05:00:00+00:00"  # [04,05) at 06:00
    assert six["value"] == 1.4 and six["available_at_utc"] == f"{day}T06:00:00+00:00"
    assert_lagged_selection("hp60", rows, _hp_obs(day), safe_lag_hours=1)


def test_lagged_selection_rejects_open_later_double_lag_and_wrong_source() -> None:
    """Negative controls on the alignment contract: an OPEN or not-yet-available interval
    at the origin; a stale selection when a later interval is eligible; a double-applied
    lag (available_at = end + 6 h) or a shortfall (end + 0 h); a value that does not trace
    to its recorded source interval; a dropped present value."""
    day = dt.date(2022, 6, 10)
    obs = _kp_obs(day)
    rows = select_lagged_series(obs, epochs=_epochs(day), safe_lag_hours=3)
    by = {r["interval_start_utc"]: r for r in rows}

    def variant(hour: int, **changes: Any) -> list[dict[str, Any]]:
        key = dt.datetime.combine(day, dt.time(hour), tzinfo=UTC).isoformat()
        return [{**r, **changes} if r["interval_start_utc"] == key else r for r in rows]

    # open interval [03,06) presented at 04:00
    with pytest.raises(AlignmentError, match="after the origin"):
        assert_lagged_selection(
            "kp",
            variant(
                4,
                value=11.0,
                source_interval_start_utc=f"{day}T03:00:00+00:00",
                source_interval_end_utc=f"{day}T06:00:00+00:00",
                available_at_utc=f"{day}T09:00:00+00:00",
            ),
            obs,
            safe_lag_hours=3,
        )
    # stale: [00,03) presented at 09:00 while [03,06) is eligible
    with pytest.raises(AlignmentError, match="LATEST eligible"):
        assert_lagged_selection(
            "kp",
            variant(
                9,
                **{
                    k: by[f"{day}T06:00:00+00:00"][k]
                    for k in (
                        "value",
                        "source_interval_start_utc",
                        "source_interval_end_utc",
                        "available_at_utc",
                    )
                },
            ),
            obs,
            safe_lag_hours=3,
        )
    # double lag / shortfall
    with pytest.raises(AlignmentError, match="applied exactly once"):
        assert_lagged_selection(
            "kp", variant(9, available_at_utc=f"{day}T12:00:00+00:00"), obs, safe_lag_hours=3
        )
    with pytest.raises(AlignmentError, match="applied exactly once"):
        assert_lagged_selection(
            "kp", variant(9, available_at_utc=f"{day}T06:00:00+00:00"), obs, safe_lag_hours=3
        )
    # value not traceable to the recorded source interval
    with pytest.raises(AlignmentError, match="does not trace"):
        assert_lagged_selection("kp", variant(9, value=99.0), obs, safe_lag_hours=3)
    # a present source value dropped
    with pytest.raises(AlignmentError, match="never dropped"):
        assert_lagged_selection("kp", variant(9, value=None), obs, safe_lag_hours=3)
    # the same rows re-checked under a different lag fail (no silent re-lagging)
    with pytest.raises(AlignmentError):
        assert_lagged_selection("kp", rows, obs, safe_lag_hours=6)


def test_lagged_selection_composes_with_missing_data_and_carry_forward() -> None:
    """A missing source interval keeps its identity: at origins 09:00-11:00 the eligible
    [03,06) value is missing, so the rows are missing (never the older [00,03) value —
    that would be an unrecorded carry-forward); the epoch-axis carry-forward then fills at
    most bound_h hours and excludes beyond (R-57a), with the fill RECORDED."""
    day = dt.date(2022, 6, 10)
    obs = _kp_obs(day, missing_slot=1)
    rows = select_lagged_series(obs, epochs=_epochs(day), safe_lag_hours=3)
    by = {r["interval_start_utc"]: r for r in rows}
    for hour in (9, 10, 11):
        row = by[f"{day}T{hour:02d}:00:00+00:00"]
        assert row["value"] is None
        assert row["source_interval_end_utc"] == f"{day}T06:00:00+00:00"
    assert_lagged_selection("kp", rows, obs, safe_lag_hours=3)
    hourly = {dt.datetime.fromisoformat(r["interval_start_utc"]): r["value"] for r in rows}
    carried = apply_carry_forward(hourly, bound_h=3)
    base = dt.datetime.combine(day, dt.time(0), tzinfo=UTC)
    assert carried["carried_forward_epochs"] == [base + dt.timedelta(hours=h) for h in (9, 10, 11)]
    assert carried["values"][base + dt.timedelta(hours=11)] == 10.0
    assert carried["values"][base + dt.timedelta(hours=12)] == 12.0  # [06,09) eligible at 12:00
    tight = apply_carry_forward(hourly, bound_h=1)
    assert tight["excluded_epochs"] == [
        base + dt.timedelta(hours=h) for h in (0, 1, 2, 3, 4, 5, 10, 11)
    ]
    matrix_rows = availability_rows_from_selection(rows, release_status="nowcast")
    assert all(
        r["observation_timestamp"] + dt.timedelta(hours=3) <= r["forecast_origin"]
        for r in matrix_rows
    )
    assert len(matrix_rows) == 24 - 6 - 3  # 00-05 no eligible interval; 09-11 missing value


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


def _mirror_declared_sources(workspace: Path) -> None:
    """Make every `configs/data.yaml: declared_sources` path resolve inside the smoke
    workspace, so `assert_declared_sources_exist` (TE 18.3, step 5) sees the SAME bytes the
    real workspace declares and the test observes the refusal it is written for, not an
    absent-source refusal. Hard-linked where the filesystem allows (no bytes duplicated),
    copied otherwise; nothing is fabricated — a path the real workspace lacks stays absent
    here too, and the preflight then names it exactly as it would in production."""
    try:
        import yaml
    except ImportError:  # the pyyaml refusal is itself one of the governed refusals
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
    """A temporary workspace: requirements.txt copied (the lock hashes it) and the
    declared sources mirrored (the preflight hashes them); no git tree, so --code-commit
    is passed explicitly (config.py's documented Kaggle shape)."""
    workspace = tmp_path / "ws"
    workspace.mkdir()
    shutil.copyfile(REPO_ROOT / "requirements.txt", workspace / "requirements.txt")
    _mirror_declared_sources(workspace)
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


# ------------------------------------------------------------------------------------------
# CR-2026-09-13-04-FIXTURE-WINDOW (owner-ruled Option a): scope-derived windowing of the
# driver audit on fixture runs. The invariant under test: on a fixture run the declared
# window IS the scope's cited window and every audit read, count, and requirement is
# bounded to it — the declaration is made true by narrowing the READS, never the report.
# On a non-fixture run behaviour is unchanged (full calendar year, non-exempt gate).
# These controls import the stage script by path (module-level code is import-only; main()
# is __main__-guarded) and exercise the audit tiers in-process — no configs, no yaml.
# ------------------------------------------------------------------------------------------


def _load_stage_04():
    """Load scripts/04_build_external_products.py as a module, by path (digit-prefixed
    stage-script names are not importable; the script's module level only imports)."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("stage_04_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules["stage_04_under_test"] = module
    spec.loader.exec_module(module)
    return module


_NOVEMBER_WEEK = (dt.date(2022, 11, 1), dt.date(2022, 11, 7))  # D-11's frozen shape
_FULL_YEAR = (dt.date(2022, 1, 1), dt.date(2022, 12, 31))


def _dst_html(days: range) -> str:
    """Minimal Kyoto-shaped monthly table: one parseable row per day (24 hourly ints)."""
    return "\n".join(f" {day} " + " ".join(["-12"] * 24) for day in days) + "\n"


def test_fixture_scoped_dst_audit_reads_only_in_window_evidence(tmp_path) -> None:
    """LOAD-BEARING negative control: under a fixture window, an out-of-window monthly
    file is neither opened, hashed, counted, nor required. The out-of-window artifact is
    a POISON — a directory named like the January file, so any open/hash attempt raises
    (a stronger proof than mere absence from the result). Pre-repair `_audit_dst` walks
    all twelve months and both trips the poison and counts ten absent months missing —
    this control fails on that code (verified against HEAD in the CR's results)."""
    mod = _load_stage_04()
    kyoto = tmp_path / "kyoto_dst"
    kyoto.mkdir()
    (kyoto / "dst_provisional_202211.html").write_text(_dst_html(range(1, 8)), encoding="utf-8")
    (kyoto / "dst_provisional_202201.html").mkdir()  # poison: reading/hashing raises
    coverage, missing = mod._audit_dst(kyoto, window=_NOVEMBER_WEEK)
    assert [record["month"] for record in coverage] == ["2022-11"]
    assert (
        missing == []
    ), f"a fixture-scoped audit must not count out-of-window months missing: {missing}"
    november = coverage[0]
    assert november["expected_days"] == 7  # the in-window slice, not the 30-day month
    assert november["day_rows_parsed"] == 7
    assert november["missing_days"] == []


def test_fixture_scoped_f107_accounting_is_window_bounded(tmp_path) -> None:
    """The carrier file is read, but counting/missing accounting covers only the window."""
    mod = _load_stage_04()
    flux = tmp_path / "fluxtable.txt"
    rows = []
    for day in (1, 2, 3):  # in-window observations
        rows.append(f"202211{day:02d} 170000 2459000.000 2290.000 100.0 101.0 99.0")
    rows.append("20220615 170000 2459000.000 2290.000 100.0 101.0 99.0")  # out-of-window
    flux.write_text("\n".join(rows) + "\n", encoding="utf-8")
    result = mod._audit_f107(flux, window=_NOVEMBER_WEEK)
    assert result["present"] is True
    assert result["days_present_2022"] == 3  # the June row is not counted
    assert result["records_2022"] == 3
    assert len(result["days_missing_2022"]) == 4  # 7-day window minus 3 observed
    assert all(day.startswith("2022-11") for day in result["days_missing_2022"])


def test_fixture_scoped_integrity_tier_neither_reads_nor_requires_out_of_window(
    tmp_path,
) -> None:
    """Narrowest integration control on the two-tier ordering: a recorded out-of-window
    dst entry that is MISSING on disk does not refuse under the fixture scope, while the
    identical recording refuses on the non-fixture path — both directions asserted. An
    unattributable recorded name refuses fail-closed under the scope."""
    mod = _load_stage_04()
    root = tmp_path / "audit_ec1_2026-01-01"
    (root / "kyoto_dst").mkdir(parents=True)
    november = root / "kyoto_dst" / "dst_provisional_202211.html"
    november.write_text(_dst_html(range(1, 8)), encoding="utf-8")
    from src.data.release import sha256_of_file

    report = {
        "obligation_1_kyoto_dst": {
            "2022-11": {"file": november.name, "sha256": sha256_of_file(november)},
            "2022-01": {"file": "dst_provisional_202201.html", "sha256": "0" * 64},
        }
    }
    (root / "ec1-audit-report.json").write_text(json.dumps(report), encoding="utf-8")
    # Fixture-scoped: the recorded January entry (missing on disk) is out-of-window —
    # neither read nor required.
    mod._verify_recorded_hashes(root, window=_NOVEMBER_WEEK, fixture_scoped=True)
    # Non-fixture: the identical recording refuses on the missing January file.
    with pytest.raises(IntegrityError, match="missing on disk"):
        mod._verify_recorded_hashes(root, window=_FULL_YEAR, fixture_scoped=False)
    # Fail-closed: a recorded name whose month cannot be parsed refuses under the scope.
    report["obligation_1_kyoto_dst"]["weird"] = {
        "file": "dst_weird.html",
        "sha256": "0" * 64,
    }
    (root / "ec1-audit-report.json").write_text(json.dumps(report), encoding="utf-8")
    with pytest.raises(IntegrityError, match="cannot be parsed"):
        mod._verify_recorded_hashes(root, window=_NOVEMBER_WEEK, fixture_scoped=True)


def test_full_year_audit_behaviour_is_unchanged_without_a_fixture_scope(tmp_path) -> None:
    """Full-year invariance: the non-fixture window still iterates exactly the twelve
    2022 months with full-month day expectations, names absent months exactly as before,
    and the year filter is extensionally the pre-repair `date.year == 2022` filter."""
    mod = _load_stage_04()
    kyoto = tmp_path / "kyoto_dst"
    kyoto.mkdir()
    (kyoto / "dst_provisional_202203.html").write_text(_dst_html(range(1, 32)), encoding="utf-8")
    coverage, missing = mod._audit_dst(kyoto, window=_FULL_YEAR)
    assert [record["month"] for record in coverage] == ["2022-03"]
    assert coverage[0]["expected_days"] == 31 and coverage[0]["missing_days"] == []
    assert len(missing) == 11  # the other eleven months, named individually
    assert missing[0] == "2022-01 (dst: file not retrieved)"  # pre-repair label, exact
    assert all("(dst: file not retrieved)" in entry for entry in missing)
    # The default full-year window constant is unchanged.
    assert mod._declared_data_window() == _FULL_YEAR
    # And the months helper yields exactly the pre-repair twelve for the full year.
    assert mod._months_in_window(_FULL_YEAR) == [(2022, month) for month in range(1, 13)]


def test_fixture_declaration_derives_from_the_scope_never_the_full_year() -> None:
    """Declaration-truth control (AST, repo style): on `_stage_entry`'s fixture branch
    the declared window comes from `load_fixture_scope(...).window`, and
    `_declared_data_window()` — the full-year constant — is NOT consulted on that
    branch. Pins the repaired shape so the unconditional-refusal deadlock cannot be
    silently reintroduced."""
    source = SCRIPT.read_text(encoding="utf-8")
    tree = ast.parse(source)
    stage_entry = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "_stage_entry"
    )
    branches = [node for node in ast.walk(stage_entry) if isinstance(node, ast.If)]
    fixture_branch = None
    for node in branches:
        test_src = ast.get_source_segment(source, node.test) or ""
        if "fixture_manifest" in test_src:
            fixture_branch = node
            break
    assert fixture_branch is not None, "_stage_entry lost its fixture branch"
    body_src = "\n".join(
        ast.get_source_segment(source, stmt) or "" for stmt in fixture_branch.body
    )
    assert (
        "load_fixture_scope" in body_src and "scope.window" in body_src
    ), "the fixture branch must derive the declared window from the scope's cited window"
    assert "_declared_data_window" not in body_src, (
        "the fixture branch must never consult the full-year declaration — that is the "
        "unconditional-refusal deadlock CR-2026-09-13-04-FIXTURE-WINDOW repairs"
    )
    else_src = "\n".join(
        ast.get_source_segment(source, stmt) or "" for stmt in fixture_branch.orelse
    )
    assert (
        "_declared_data_window" in else_src
    ), "the non-fixture branch must keep the full-year window (D-8's claim boundary)"


# =====================================================================================
# B-01 production path (2026-09-19): runtime pin protection, validation-report builder,
# gated generation -- exercised at FUNCTION level through the allowlisted stage script
# (`_load_stage_04`), never by importing `src.external.iri` here (TE 12; TA-07).
# `iricore` is a STUB on sys.path carrying the REAL pinned index bytes from
# evidence/iri2016_kaggle_verification_2026-09-19/ (hash-equal to the D-45 pins), so the
# pin checks run against the genuine files while `vtec` returns a deterministic value.
# Station coordinates are D-1's (evidence/DECISIONS.md D-1) in a TEMPORARY config copy,
# because configs/data.yaml:stations is still `TBD -- freeze gate` (the student's freeze).
# =====================================================================================

_EVIDENCE_INDEX = (
    REPO_ROOT
    / "evidence"
    / "iri2016_kaggle_verification_2026-09-19"
    / "index_files"
    / "installed_iricore-1.8.0_wheel"
)
_D1_STATIONS = {  # D-1 coordinates; other 6.2 fields synthetic, provenance labelled so
    "ARUC": (40.286, 44.086),
    "BSHM": (32.778987, 35.022987),
    "NICO": (35.140989, 33.396450),
}


def _stub_iricore(
    tmp_path: Path,
    *,
    version: str = "1.8.0",
    default_iri: int = 20,
    corrupt: str | None = None,
    fail_at: str | None = None,
) -> Path:
    """A stub `iricore` distribution: config.DEFAULT_IRI_VERSION, data/index/* (real
    pinned bytes unless `corrupt` names a file to alter), and a `vtec` that records its
    arguments and returns a deterministic TECU value (or raises for `fail_at`)."""
    site = tmp_path / "stub_site"
    pkg = site / "iricore"
    (pkg / "data" / "index").mkdir(parents=True, exist_ok=True)
    for name in ("apf107.dat", "ig_rz.dat"):
        data = (_EVIDENCE_INDEX / name).read_bytes()
        if corrupt == name:
            data = data + b" \n"
        (pkg / "data" / "index" / name).write_bytes(data)
    (pkg / "config.py").write_text(
        f"IRI_VERSIONS = [16, 20]\nDEFAULT_IRI_VERSION = {default_iri}\n", encoding="utf-8"
    )
    fail_clause = (
        f"    if dt.isoformat().startswith({fail_at!r}):\n        raise RuntimeError('stub failure')\n"
        if fail_at
        else ""
    )
    (pkg / "__init__.py").write_text(
        "CALLS = []\n"
        "IRI_CALLS = []\n"
        "def vtec(dt, lat, lon, hbot=90.0, htop=2000.0, hstep=0.5, version=20, **kw):\n"
        "    CALLS.append((dt, lat, lon, hbot, htop, hstep, version))\n"
        + fail_clause
        + "    return [10.0 + dt.hour * 0.5 + (lat - 30.0)]\n"
        "class _Out:\n"
        "    def __init__(self, oarr):\n"
        "        self.oarr = oarr\n"
        "def iri(dt, altrange, lat, lon, version=20, **kw):\n"
        "    # oarr[1] is hmF2/km (the D-50 diagnostic); deterministic from the hour\n"
        "    IRI_CALLS.append((dt, tuple(altrange), lat, lon, version))\n"
        "    oarr = [0.0] * 100\n"
        "    oarr[1] = 250.0 + dt.hour\n"
        "    return _Out(oarr)\n",
        encoding="utf-8",
    )
    dist = site / f"iricore-{version}.dist-info"
    dist.mkdir(exist_ok=True)
    (dist / "METADATA").write_text(
        f"Metadata-Version: 2.1\nName: iricore\nVersion: {version}\n", encoding="utf-8"
    )
    return site


def _b01_configs(
    tmp_path: Path,
    *,
    tolerance: object = 1.0,
    declared_at: object = "2026-09-19T00:00:00+00:00",
    stations: bool = True,
) -> Path:
    """A temporary copy of configs/ with D-1 stations transcribed (synthetic 6.2 fields),
    igrf_version set, and the predeclared tolerance filled -- the freezes the real
    config still carries as TBD, supplied here as test data only."""
    import yaml

    cfg = tmp_path / "configs"
    shutil.copytree(REPO_ROOT / "configs", cfg)
    data = yaml.safe_load((cfg / "data.yaml").read_text(encoding="utf-8"))
    if stations:
        data["stations"] = {
            sid: {
                "lat": lat,
                "lon": lon,
                "ellipsoidal_height_m": 0.0,
                "domes": "00000M000",
                "sampling_interval_s": 30,
                "provenance": {
                    k: "test-fixture (D-1 coordinates; other fields synthetic)"
                    for k in ("lat", "lon", "ellipsoidal_height_m", "domes", "sampling_interval_s")
                },
            }
            for sid, (lat, lon) in _D1_STATIONS.items()
        }
        data["igrf_version"] = "test-fixture"
    else:
        # the real data.yaml carries the transcription since 2026-09-19; this branch
        # re-creates the pre-transcription refusal state deliberately
        data["stations"] = "TBD — freeze gate"
    (cfg / "data.yaml").write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    exp = yaml.safe_load((cfg / "experiment.yaml").read_text(encoding="utf-8"))
    exp["benchmark_b01"]["validation_report"]["tolerance_tecu"] = tolerance
    exp["benchmark_b01"]["validation_report"]["tolerance_declared_at_utc"] = declared_at
    (cfg / "experiment.yaml").write_text(
        yaml.safe_dump(exp, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    return cfg


_B01_DETERMINISM: list[Any] = []  # seed_everything runs once per process (R-05: TensorFlow init)


def _b01_entry(mod, cfg: Path, workspace: Path):
    from src.data.config import capture_environment_lock, load_configs, seed_everything

    os.environ["TEC_WORKSPACE_ROOT"] = str(workspace)
    snapshot = load_configs(cfg, phase=1)
    if not _B01_DETERMINISM:
        _B01_DETERMINISM.append(seed_everything(snapshot, stage="external-products"))
    lock = capture_environment_lock(snapshot, _B01_DETERMINISM[0], code_commit="test-no-git-tree")
    return {"snapshot": snapshot, "lock": lock}


def _samples(n: int = 6) -> list[dict[str, object]]:
    specs = [
        ("ARUC", 40.286, 44.086, "2022-06-15T12:00:00+00:00", "day", "quiet"),
        ("ARUC", 40.286, 44.086, "2022-06-15T00:00:00+00:00", "night", "quiet"),
        ("BSHM", 32.778987, 35.022987, "2022-03-31T12:00:00+00:00", "day", "disturbed"),
        ("BSHM", 32.778987, 35.022987, "2022-03-31T01:00:00+00:00", "night", "disturbed"),
        ("NICO", 35.140989, 33.396450, "2022-08-28T13:00:00+00:00", "day", "disturbed"),
        ("NICO", 35.140989, 33.396450, "2022-01-06T02:00:00+00:00", "night", "quiet"),
        ("ARUC", 40.286, 44.086, "2022-09-01T11:00:00+00:00", "day", "quiet"),
    ]
    out = []
    for site, lat, lon, t, ltc, act in specs[:n]:
        hour = int(t[11:13])
        out.append(
            {
                "site": site,
                "lat": lat,
                "lon": lon,
                "target_time_utc": t,
                "local_time_class": ltc,
                "activity_class": act,
                "official_interface_value": 10.0 + hour * 0.5 + (lat - 30.0),
                "official_interface_source": "test-fixture",
            }
        )
    return out


@pytest.fixture
def b01(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    pytest.importorskip("yaml")
    site = _stub_iricore(tmp_path)
    monkeypatch.syspath_prepend(str(site))
    for name in [m for m in sys.modules if m == "iricore" or m.startswith("iricore.")]:
        del sys.modules[name]
    workspace = _workspace(tmp_path)
    mod = _load_stage_04()
    yield mod, tmp_path, workspace, site
    for name in [m for m in sys.modules if m == "iricore" or m.startswith("iricore.")]:
        del sys.modules[name]


def _ns(**kw):
    import argparse

    base = dict(
        phase=1, out=None, months=None, validation_report=None, build_validation_report=None
    )
    base.update(kw)
    return argparse.Namespace(**base)


def test_b01_verify_runtime_writes_identity_with_full_pins(b01) -> None:
    mod, tmp_path, workspace, _ = b01
    entry = _b01_entry(mod, _b01_configs(tmp_path), workspace)
    summary = mod._verify_runtime(entry, _ns())
    identity = json.loads(summary["runtime_identity"].read_text(encoding="utf-8"))
    assert identity["release"] == "1.8.0" and identity["installed_default_iri_version"] == 20
    assert identity["index_files_sha256"] == {
        "apf107.dat": "cdf4d5dffe6d05eaae9ed90532cddea4c3cf2fdad255d837e660018cae60e674",
        "ig_rz.dat": "fbbed3049483ac445070cc63841b7d14aa2929894eb725bdf946889840a41486",
    }
    assert (summary["runtime_identity"].parent / "sha256_manifest.json").is_file()


@pytest.mark.parametrize("corrupt", ["apf107.dat", "ig_rz.dat"])
def test_b01_verify_runtime_refuses_altered_index_file(
    tmp_path: Path, monkeypatch, corrupt: str
) -> None:
    pytest.importorskip("yaml")
    from src.data.config import BenchmarkError

    site = _stub_iricore(tmp_path, corrupt=corrupt)
    monkeypatch.syspath_prepend(str(site))
    for name in [m for m in sys.modules if m.startswith("iricore")]:
        del sys.modules[name]
    mod = _load_stage_04()
    entry = _b01_entry(mod, _b01_configs(tmp_path), _workspace(tmp_path))
    with pytest.raises(BenchmarkError) as exc:
        mod._verify_runtime(entry, _ns())
    assert (
        corrupt in str(exc.value) and "D-45 pin" in str(exc.value) and "refused" in str(exc.value)
    )
    for name in [m for m in sys.modules if m.startswith("iricore")]:
        del sys.modules[name]


def test_b01_verify_runtime_refuses_wrong_release_or_default(tmp_path: Path, monkeypatch) -> None:
    pytest.importorskip("yaml")
    from src.data.config import BenchmarkError

    for kw, marker in (
        (dict(version="1.9.0"), "pinned '1.8.0'"),
        (dict(default_iri=16), "DEFAULT_IRI_VERSION is 16"),
    ):
        site = _stub_iricore(tmp_path / marker.replace(" ", "_").replace("'", ""), **kw)
        monkeypatch.syspath_prepend(str(site))
        for name in [m for m in sys.modules if m.startswith("iricore")]:
            del sys.modules[name]
        mod = _load_stage_04()
        entry = _b01_entry(
            mod,
            _b01_configs(tmp_path / marker.replace(" ", "_").replace("'", "")),
            _workspace(tmp_path / marker.replace(" ", "_").replace("'", "")),
        )
        with pytest.raises(BenchmarkError) as exc:
            mod._verify_runtime(entry, _ns())
        assert marker in str(exc.value)
        sys.path.remove(str(site))
        for name in [m for m in sys.modules if m.startswith("iricore")]:
            del sys.modules[name]


def test_b01_validation_report_records_the_hmf2_diagnostic_without_a_threshold(b01) -> None:
    """D-50's hmF2 diagnostic column: when a sample carries the official interface's
    hmF2, the report records it beside the adapter's own hmF2 (one `iricore.iri` call at
    version 16) and their difference, and that difference never changes the tolerance
    verdict; a sample without it records nulls and makes no `iri` call."""
    import iricore

    mod, tmp_path, workspace, _ = b01
    entry = _b01_entry(mod, _b01_configs(tmp_path), workspace)
    samples = _samples()
    samples[0]["official_interface_hmf2_km"] = 200.0  # far from the stub's 262 -> still passes
    samples[1]["official_interface_hmf2_km"] = 250.0  # exactly the stub's value at 00 UT
    samples_path = tmp_path / "samples_hmf2.json"
    samples_path.write_text(json.dumps(samples), encoding="utf-8")
    del iricore.IRI_CALLS[:]
    summary = mod._build_validation_report(entry, _ns(build_validation_report=samples_path))
    report = json.loads(summary["validation_report"].read_text(encoding="utf-8"))
    assert report["status"] == "passed"
    rows = report["samples"]
    assert rows[0]["official_interface_hmf2_km"] == 200.0
    assert rows[0]["adapter_hmf2_km"] == 262.0
    assert rows[0]["hmf2_diff_km_diagnostic_no_threshold"] == pytest.approx(62.0)
    assert rows[0]["within_tolerance"] is True  # a 62 km hmF2 gap is diagnostic, not a failure
    assert rows[1]["hmf2_diff_km_diagnostic_no_threshold"] == pytest.approx(0.0)
    for row in rows[2:]:
        assert row["official_interface_hmf2_km"] is None
        assert row["adapter_hmf2_km"] is None
        assert row["hmf2_diff_km_diagnostic_no_threshold"] is None
    assert len(iricore.IRI_CALLS) == 2 and all(c[4] == 16 for c in iricore.IRI_CALLS)


def test_b01_validation_report_passes_and_carries_seven_areas(b01) -> None:
    mod, tmp_path, workspace, _ = b01
    entry = _b01_entry(mod, _b01_configs(tmp_path), workspace)
    samples_path = tmp_path / "samples.json"
    samples_path.write_text(json.dumps(_samples()), encoding="utf-8")
    summary = mod._build_validation_report(entry, _ns(build_validation_report=samples_path))
    report = json.loads(summary["validation_report"].read_text(encoding="utf-8"))
    assert report["status"] == "passed" and report["altitude_ceiling_km"] == 2000.0
    for area in (
        "package_version",
        "model_switches",
        "topside_option",
        "altitude_ceiling_km",
        "units",
        "output_extraction",
        "driver_inputs",
        "samples",
        "tolerance",
    ):
        assert area in report
    d = report["driver_inputs"]
    assert (
        d["index_inputs_retrospective_centered"] is True
        and d["iri_version"] == 16
        and d["oarr_overrides"] == {}
    )
    assert d["index_files_sha256"]["apf107.dat"].startswith("cdf4d5df")
    assert len(report["samples"]) == 6 and all(s["within_tolerance"] for s in report["samples"])
    assert report["tolerance"]["declared_at_utc"] < report["comparison_ran_at_utc"]
    # the adapter's call is the D-45 call: explicit version 16, ceiling 2000, wrapper hbot/hstep
    import iricore

    assert iricore.CALLS and all(c[3:] == (90.0, 2000.0, 0.5, 16) for c in iricore.CALLS)
    assert all(c[0].tzinfo is None for c in iricore.CALLS)  # naive UT handed to iricore


def test_b01_validation_report_failed_is_written_and_blocks(b01) -> None:
    from src.data.config import IntegrityError

    mod, tmp_path, workspace, _ = b01
    entry = _b01_entry(mod, _b01_configs(tmp_path, tolerance=0.001), workspace)
    samples = _samples()
    samples[2]["official_interface_value"] += 5.0  # one sample outside tolerance
    samples_path = tmp_path / "samples.json"
    samples_path.write_text(json.dumps(samples), encoding="utf-8")
    with pytest.raises(IntegrityError) as exc:
        mod._build_validation_report(entry, _ns(build_validation_report=samples_path))
    assert "status is 'failed'" in str(exc.value) and "never silently switched" in str(exc.value)
    written = json.loads(
        (
            workspace
            / "artifacts"
            / "external"
            / "b01"
            / "iri_implementation_validation_report.json"
        ).read_text(encoding="utf-8")
    )
    assert (
        written["status"] == "failed"
        and sum(not s["within_tolerance"] for s in written["samples"]) == 1
    )


def test_b01_validation_report_refuses_tbd_tolerance_and_late_declaration(b01) -> None:
    from src.data.config import BenchmarkError

    mod, tmp_path, workspace, _ = b01
    samples_path = tmp_path / "samples.json"
    samples_path.write_text(json.dumps(_samples()), encoding="utf-8")
    entry = _b01_entry(
        mod, _b01_configs(tmp_path / "tbd", tolerance="TBD — freeze gate"), workspace
    )
    with pytest.raises(BenchmarkError) as exc:
        mod._build_validation_report(entry, _ns(build_validation_report=samples_path))
    assert "predeclared" in str(exc.value) and "TE 1.1" in str(exc.value)
    entry = _b01_entry(
        mod, _b01_configs(tmp_path / "late", declared_at="2099-01-01T00:00:00+00:00"), workspace
    )
    with pytest.raises(BenchmarkError) as exc:
        mod._build_validation_report(entry, _ns(build_validation_report=samples_path))
    assert "does not precede" in str(exc.value)


def test_b01_validation_report_refuses_december_sample(b01) -> None:
    from src.data.config import BenchmarkError

    mod, tmp_path, workspace, _ = b01
    entry = _b01_entry(mod, _b01_configs(tmp_path), workspace)
    samples = _samples()
    samples[0]["target_time_utc"] = "2022-12-05T12:00:00+00:00"
    samples_path = tmp_path / "samples.json"
    samples_path.write_text(json.dumps(samples), encoding="utf-8")
    with pytest.raises(BenchmarkError) as exc:
        mod._build_validation_report(entry, _ns(build_validation_report=samples_path))
    assert "locked month" in str(exc.value)


def test_b01_generate_partial_month_end_to_end(b01) -> None:
    mod, tmp_path, workspace, _ = b01
    cfg = _b01_configs(tmp_path)
    entry = _b01_entry(mod, cfg, workspace)
    samples_path = tmp_path / "samples.json"
    samples_path.write_text(json.dumps(_samples()), encoding="utf-8")
    report_path = mod._build_validation_report(entry, _ns(build_validation_report=samples_path))[
        "validation_report"
    ]
    summary = mod._generate_benchmark(
        entry, _ns(generate_benchmark=True, validation_report=report_path, months="2")
    )
    rows = [
        json.loads(line)
        for line in summary["benchmark_rows"].read_text(encoding="utf-8").splitlines()
    ]
    assert len(rows) == 3 * 28 * 24 and summary["benchmark_rows"].name.endswith("_partial.jsonl")
    first = rows[0]
    assert (
        first["phase_id"] == "P1A"
        and first["source_id"] == "IRI2016_B01"
        and first["target_definition_id"] == "GRIDDed_VTEC_1H"
    )
    assert (
        first["benchmark_id"] == "B-01"
        and first["units"] == "TECU"
        and first["iri_version"] == 16
        and first["htop_km"] == 2000.0
    )
    assert (
        first["station_id"] == "ARUC"
        and first["cell_id"] == "40/44"
        and first["target_time_utc"] == "2022-02-01T00:00:00+00:00"
    )
    assert {r["cell_id"] for r in rows} == {"40/44", "32/35", "35/33"}
    assert all(r["status"] == "ok" and isinstance(r["iri2016_t_plus_1_tecu"], float) for r in rows)
    times = [r["target_time_utc"] for r in rows if r["station_id"] == "NICO"]
    assert times == sorted(times) and len(set(times)) == 28 * 24
    prov = json.loads(summary["provenance"].read_text(encoding="utf-8"))
    assert (
        prov["partial"] is True
        and prov["months"] == [2]
        and prov["call_count"] == len(rows)
        and prov["error_rows"] == 0
    )
    assert (
        prov["index_files_sha256_after_session"] == prov["runtime_identity"]["index_files_sha256"]
    )
    assert (
        prov["validation_report_status"] == "passed" and prov["label"] == "generated, not trained"
    )
    assert {r["driver_id"] for r in prov["benchmark_driver_rows"]} == {
        "iri_apf107_f107_adjusted",
        "iri_apf107_ap_3h",
        "iri_ig_rz_ig12_rz12",
    }
    assert all(
        r["release_status"].startswith("hindcast-only") for r in prov["benchmark_driver_rows"]
    )
    manifest = json.loads(
        (summary["benchmark_rows"].parent / "sha256_manifest.json").read_text(encoding="utf-8")
    )
    assert set(manifest) == {"b01_iri2016_rows_partial.jsonl", "b01_provenance.json"}


def test_b01_generate_refuses_failed_report_and_mismatched_pins(b01) -> None:
    from src.data.config import BenchmarkError

    mod, tmp_path, workspace, _ = b01
    entry = _b01_entry(mod, _b01_configs(tmp_path), workspace)
    samples_path = tmp_path / "samples.json"
    samples_path.write_text(json.dumps(_samples()), encoding="utf-8")
    report_path = mod._build_validation_report(entry, _ns(build_validation_report=samples_path))[
        "validation_report"
    ]
    report = json.loads(report_path.read_text(encoding="utf-8"))
    failed = dict(report, status="failed")
    failed_path = tmp_path / "failed.json"
    failed_path.write_text(json.dumps(failed), encoding="utf-8")
    with pytest.raises(BenchmarkError) as exc:
        mod._generate_benchmark(
            entry, _ns(generate_benchmark=True, validation_report=failed_path, months="2")
        )
    assert "not 'passed'" in str(exc.value)
    other = json.loads(json.dumps(report))
    other["driver_inputs"]["index_files_sha256"]["apf107.dat"] = "0" * 64
    other_path = tmp_path / "other.json"
    other_path.write_text(json.dumps(other), encoding="utf-8")
    with pytest.raises(BenchmarkError) as exc:
        mod._generate_benchmark(
            entry, _ns(generate_benchmark=True, validation_report=other_path, months="2")
        )
    assert "validated a different runtime" in str(exc.value)


def test_b01_generate_refuses_unresolved_stations(b01) -> None:
    from src.data.config import RegistryError

    mod, tmp_path, workspace, _ = b01
    entry = _b01_entry(mod, _b01_configs(tmp_path, stations=False), workspace)
    report_path = tmp_path / "r.json"
    report_path.write_text("{}", encoding="utf-8")
    with pytest.raises(RegistryError) as exc:
        mod._generate_benchmark(
            entry, _ns(generate_benchmark=True, validation_report=report_path, months="2")
        )
    assert "TBD" in str(exc.value)


def test_b01_per_point_failure_is_recorded_not_fatal(tmp_path: Path, monkeypatch) -> None:
    pytest.importorskip("yaml")
    site = _stub_iricore(tmp_path, fail_at="2022-02-03T05")
    monkeypatch.syspath_prepend(str(site))
    for name in [m for m in sys.modules if m.startswith("iricore")]:
        del sys.modules[name]
    mod = _load_stage_04()
    workspace = _workspace(tmp_path)
    entry = _b01_entry(mod, _b01_configs(tmp_path), workspace)
    samples_path = tmp_path / "samples.json"
    samples_path.write_text(json.dumps(_samples()), encoding="utf-8")
    report_path = mod._build_validation_report(entry, _ns(build_validation_report=samples_path))[
        "validation_report"
    ]
    summary = mod._generate_benchmark(
        entry, _ns(generate_benchmark=True, validation_report=report_path, months="2")
    )
    rows = [
        json.loads(line)
        for line in summary["benchmark_rows"].read_text(encoding="utf-8").splitlines()
    ]
    bad = [r for r in rows if r["status"] == "error"]
    assert len(bad) == 3 and all(
        r["iri2016_t_plus_1_tecu"] is None and "stub failure" in r["error"] for r in bad
    )
    prov = json.loads(summary["provenance"].read_text(encoding="utf-8"))
    assert prov["error_rows"] == 3
    for name in [m for m in sys.modules if m.startswith("iricore")]:
        del sys.modules[name]


def test_b01_config_block_is_the_annotated_d45_contract() -> None:
    """The one authoritative pin record: experiment.benchmark_b01 carries the full hashes
    D-45's annotation recorded, version 16, the 2000 km ceiling and no overrides."""
    pytest.importorskip("yaml")
    import yaml

    block = yaml.safe_load(
        (REPO_ROOT / "configs" / "experiment.yaml").read_text(encoding="utf-8")
    )["benchmark_b01"]
    assert (
        block["iri_version"] == 16
        and block["integration"]["htop_km"] == 2000.0
        and block["oarr_overrides"] == {}
    )
    assert block["index_file_pins"] == {
        "apf107.dat": "cdf4d5dffe6d05eaae9ed90532cddea4c3cf2fdad255d837e660018cae60e674",
        "ig_rz.dat": "fbbed3049483ac445070cc63841b7d14aa2929894eb725bdf946889840a41486",
    }
    assert (
        block["runtime"]["wheel_sha256"]
        == "f452b22316891d87ee766dba266de6a07e4e6008ab515ffed902ea8b5446a874"
    )
    # D-50 (2026-09-20): the student's predeclaration is frozen — 1.0 TECU absolute per
    # case, declared with a timestamp that precedes any comparison (R-59 limb 2).
    assert block["validation_report"]["tolerance_tecu"] == 1.0
    import datetime as _dt

    declared_text = str(block["validation_report"]["tolerance_declared_at_utc"])
    if declared_text.endswith("Z"):  # Python 3.10 cannot parse the `Z` suffix
        declared_text = declared_text[:-1] + "+00:00"
    declared = _dt.datetime.fromisoformat(declared_text)
    assert declared.tzinfo is not None


def test_b01_verify_runtime_completes_at_subprocess_level(tmp_path: Path) -> None:
    """`--verify-runtime` is a bounded check, not a full-year job: the TE 9.2 receipt gate
    is recorded as not required, the run completes (exit 0) on the real configs (stations
    may stay TBD -- no coordinate is needed to hash two files), and the identity carries
    the full D-45 pins. The stub iricore carries the real pinned bytes."""
    pytest.importorskip("yaml")
    site = _stub_iricore(tmp_path)
    workspace = _workspace(tmp_path)
    env = dict(
        os.environ, PYTHONHASHSEED="0", TEC_WORKSPACE_ROOT=str(workspace), PYTHONPATH=str(site)
    )
    env.pop("TEC_PLATFORM", None)
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--config",
            str(REPO_ROOT / "configs"),
            "--code-commit",
            "smoke-no-git-tree",
            "--verify-runtime",
        ],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(REPO_ROOT),
        timeout=600,
        check=False,
    )
    assert result.returncode == 0, result.stderr[-2000:]
    identity = json.loads(
        (workspace / "artifacts" / "external" / "b01" / "b01_runtime_identity.json").read_text(
            encoding="utf-8"
        )
    )
    assert (
        identity["index_files_sha256"]["ig_rz.dat"]
        == "fbbed3049483ac445070cc63841b7d14aa2929894eb725bdf946889840a41486"
    )
    assert "runtime verified" in result.stdout
    # a full-year driver-audit invocation on the same workspace still fails closed (gate kept)
    audit = _run_script([], workspace)
    _assert_gate_fails_closed(audit)


# =======================================================================================
# Board Recommendation 51 — the legacy EC-1 audit marks its own artifact PARTIAL
# =======================================================================================
#
# `scripts/audit_ec1_drivers.py` is pre-TC-06 tooling pending a retirement ruling (the
# board's preferred option 2, an owner act). The board added one obligation that stands
# either way: "Add the `partial` field regardless." This is that field's control.
#
# Read the board's own qualification precisely, because it bounds what is tested here.
# The machine-readable limb was ALREADY satisfied — `audit_dst` writes `missing_days` and
# `expected_days` per month into the report, so a shortfall was never console-text-only —
# and a completeness shortfall is legitimately NON-FATAL, so `main`'s unconditional
# `return 0` is correct and is NOT the defect. What was unmet is the remaining clause of
# `team.md` § Code Style: "the artifact explicitly marked derived and/or partial". A
# reader had the per-month detail and no way to see at a glance whether the report AS A
# WHOLE is complete.
#
# `_partial_reasons` is exercised directly rather than through `main`: it is pure, while
# `main` writes into the real `evidence/` tree, which no test here may do.


def _load_ec1_audit_module() -> Any:
    """Import the legacy script by path. Its module scope is pure path construction."""
    import importlib.util

    script = REPO_ROOT / "scripts" / "audit_ec1_drivers.py"
    spec = importlib.util.spec_from_file_location("audit_ec1_drivers_under_test", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_ec1_audit_marks_a_complete_report_clean_and_an_incomplete_one_partial() -> None:
    """Both directions. A flag that is always set, or never set, records nothing.

    SYNTHETIC inputs throughout: these are the report's own SHAPES, never the measured
    2022 figures, which the run owns and no test may transcribe (TE §15.1, §18.2).
    """
    module = _load_ec1_audit_module()

    complete_dst = {1: {"missing_days": [], "expected_days": 31}}
    complete_f107 = {"days_missing_2022": [], "days_expected_2022": 365, "unparsed_lines": 0}
    assert module._partial_reasons(complete_dst, complete_f107) == [], (
        "a complete audit must NOT be marked partial; a flag that is always set carries "
        "no information and teaches its reader to ignore it"
    )

    # Each of the four shortfall classes sets the flag AND names itself.
    shortfalls = {
        "missing day rows": (
            {1: {"missing_days": ["2022-01-05"], "expected_days": 31}},
            complete_f107,
            "kyoto_dst",
        ),
        "a month that errored": (
            {2: {"error": "synthetic retrieval failure"}},
            complete_f107,
            "synthetic retrieval failure",
        ),
        "absent F10.7 calendar days": (
            complete_dst,
            {"days_missing_2022": ["2022-03-18"], "days_expected_2022": 365},
            "nrcan_f107",
        ),
        "unparsed F10.7 lines": (
            complete_dst,
            {"days_missing_2022": [], "unparsed_lines": 4},
            "unparsed",
        ),
    }
    for label, (dst, f107, owed) in shortfalls.items():
        reasons = module._partial_reasons(dst, f107)
        assert reasons, f"{label} did not set the partial flag"
        assert any(owed in reason for reason in reasons), (
            f"{label} set the flag without naming itself ({owed!r} absent from "
            f"{reasons!r}); `partial: true` with no reason is a shortfall a reader "
            f"cannot act on"
        )


def test_ec1_audit_marks_itself_derived_and_keeps_completeness_off_the_exit_code() -> None:
    """The two-tier split, asserted over `main`'s SOURCE rather than by running it.

    `main` writes into the real `evidence/` tree, so it is read, not executed. Two facts
    are pinned: the artifact declares its own kind and partial state, and the exit code
    still reports INTEGRITY only — a completeness shortfall must not become a non-zero
    exit, or the two tiers collapse into one (`team.md` § Code Style).
    """
    import inspect

    module = _load_ec1_audit_module()
    source = inspect.getsource(module.main)
    for owed in ('"artifact_kind"', '"partial"', '"partial_reasons"'):
        assert owed in source, (
            f"the EC-1 report no longer carries {owed}; the artifact must mark itself "
            f"derived and/or partial (board Recommendation 51)"
        )
    assert "_partial_reasons(" in source, "the flag must be DERIVED from the measurements"
    assert source.rstrip().endswith("return 0"), (
        "main must still return 0 on a completeness shortfall: shortfalls are non-fatal "
        "by contract and are recorded as report fields, never signalled by exit status"
    )
