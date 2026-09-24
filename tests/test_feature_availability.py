"""FR-P1-04-2 / WS-11 / TA-08: the availability matrix's THREE limbs, each negative-controlled,
plus the closed-dictionary, producer, support-field and window guards of `build_features`.

PURPOSE. Every predictor is lagged to its actual availability (Kp/ap3 >= 3 h, Hp60/ap60
>= 1 h, F10.7 previous-day with a TRAILING 81-day mean) -- and those VALUES live in
`configs/features.yaml`, so this module supplies them as SYNTHETIC fixture parameters and
proves the mechanism, never the values. The three limbs (R-75, W-1a):

1. `actual_lag >= safe_lag` -- a value published after the origin FAILS;
2. trailing, never centered -- a centered window definition FAILS;
3. the ANCHOR, asserted and recomputed -- a trailing mean whose window ends at day t passes
   limbs 1 and 2 while including same-day F10.7 and FAILS here; a correct anchor whose
   values came from another window FAILS on the recomputation.

Plus: the backfill refusal (a `final` grade where `provisional` was required), the
documented-absence limb, Dst diagnostic-only, the SSN grep-class assertion over `src/`,
the D-25 availability RULE (a calendar-day rule declared instead of a scalar lag: next-day
midnight availability, origin-hour independence, same-day/future anchoring refused, closed
rule set, rule-vs-scalar and rule-vs-window exclusion, later publication still governs),
the R-76a alignment raise through `build_features`, the closed dictionary (`iri_*`, raw
longitude, removed row, outside row), the fail-closed permitted-producer refusal naming
WHICH rows lack entries (SD-F-01), the R-78 support-field assertions, the grid-free window,
and one full `build_features` happy path over synthetic records (stdlib representations when
pandas/numpy are absent; the governed types when present).

INPUTS. Synthetic in-memory records and configs. No December 2022 content, no restricted
root, no real config value. RE-RUN: pure functions.

WHAT NO TEST HERE DISCHARGES. WS-10, WS-11, WS-13, TA-07, TA-08, TA-33, TA-34, TA-35 and
TA-36 stay `Pending`; FR-P1-04-10 has no row. Smoke evidence only on this interpreter.

Run: pytest tests/test_feature_availability.py -rs
"""

from __future__ import annotations

import datetime as dt
import re
import sys
import tokenize
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "tests") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "tests"))

from src.data.config import (  # noqa: E402
    TBD_SENTINEL,
    AlignmentError,
    FeatureAvailabilityError,
    IntegrityError,
    LeakageError,
    PreflightError,
    RegistryError,
)
from src.data.splits import RecordFrame, partition_by_id, training_range  # noqa: E402
from src.external import spaceweather  # noqa: E402
from src.features import build  # noqa: E402
from src.features.availability import (  # noqa: E402
    AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC,
    AvailabilityRow,
    assert_anchor_recomputed,
    assert_dst_diagnostic_only,
    assert_lags_safe,
    assert_release_status_not_backfilled,
    assert_trailing_not_centered,
    build_availability_matrix,
    latest_eligible_window_end,
    read_availability_lags,
)
from src.features.build import (  # noqa: E402
    SECTION_6_2_ROWS,
    FrameSpec,
    build_features,
    load_feature_dictionary,
    load_permitted_producers,
)
from src.features.transforms import fit_transforms  # noqa: E402
from src.features.windows import (  # noqa: E402
    assert_window_length_grid_free,
    assert_window_parity,
    build_comparison_mask,
    build_windows,
    read_window_length,
)

from test_split_embargo import (  # noqa: E402
    SYNTH_WINDOW_HOURS,
    SYNTH_YEAR,
    synthetic_partitions,
    synthetic_snapshot,
)

UTC = dt.timezone.utc
PARTITIONS = synthetic_partitions()

#: Synthetic lag VALUES -- fixture parameters, not the frozen ones (which are configuration).
KP_SAFE_LAG_H = 3
F107_SAFE_LAG_H = 24
F107_WINDOW_DAYS = 5
F107_TOLERANCE = 1e-9


def _ts(month: int, day: int, hour: int = 0) -> dt.datetime:
    return dt.datetime(SYNTH_YEAR, month, day, hour, tzinfo=UTC)


def _lags(**overrides: Any) -> dict[str, Any]:
    block: dict[str, Any] = {
        "kp_safe": {
            "safe_lag_hours": KP_SAFE_LAG_H,
            "lag_reference_instant": "interval_end_utc",
            "selection_rule": "latest_completed_interval_plus_lag",
            "release_status_required": "provisional",
        },
        "f107_81_trailing": {
            "safe_lag_hours": F107_SAFE_LAG_H,
            "lag_reference_instant": "interval_end_utc",
            "selection_rule": "latest_completed_interval_plus_lag",
            "release_status_required": "observed",
            "window": {
                "kind": "trailing",
                "days": F107_WINDOW_DAYS,
                "source": "f107_daily",
                "recomputation_tolerance": F107_TOLERANCE,
                "recomputation_input_bound_sfu": 400,
            },
            "publication_latency_statement": (
                "fluxtable.txt carries no publication timestamp; the conservative D+1 00:00 UTC "
                "availability convention is recorded and the publication latency is unverified"
            ),
        },
    }
    for key, value in overrides.items():
        block[key] = value
    return block


def _daily() -> list[dict[str, Any]]:
    """Ten days of synthetic daily medians, day n -> value 100 + n."""
    return [
        {"day": dt.date(SYNTH_YEAR, 2, 1) + dt.timedelta(days=n), "value": 100.0 + n}
        for n in range(10)
    ]


def _trailing_mean(end: dt.date) -> float:
    values = {row["day"]: row["value"] for row in _daily()}
    days = [end - dt.timedelta(days=k) for k in range(F107_WINDOW_DAYS)]
    return sum(values[d] for d in days) / F107_WINDOW_DAYS


def _kp_rows(lag_h: float = 3.0, grade: str = "provisional", *, publish_after: bool = False):
    rows = []
    for hour in range(3):
        origin = _ts(2, 9, 12 + hour)
        observed = origin - dt.timedelta(hours=lag_h)
        if publish_after:
            published = origin + dt.timedelta(hours=1)
        else:
            published = observed + dt.timedelta(minutes=30)
        rows.append(
            {
                "forecast_origin": origin,
                "observation_timestamp": observed,
                "publication_timestamp": published,
                "release_status": grade,
            }
        )
    return rows


def _f107_rows(anchor_offset_days: int = 1, mean_shift: float = 0.0):
    rows = []
    for hour in (6, 12):
        origin = _ts(2, 9, hour)
        anchor = origin.date() - dt.timedelta(days=anchor_offset_days)
        rows.append(
            {
                "forecast_origin": origin,
                "observation_timestamp": dt.datetime.combine(anchor, dt.time(0), tzinfo=UTC),
                "publication_timestamp": None,
                "release_status": "observed",
                "anchor_day": anchor,
                "mean_value": _trailing_mean(anchor) + mean_shift,
            }
        )
    return rows


def _drivers(**overrides: Any) -> dict[str, Any]:
    drivers: dict[str, Any] = {
        "kp_safe": _kp_rows(),
        "f107_81_trailing": _f107_rows(),
        "f107_daily": _daily(),
    }
    drivers.update(overrides)
    return drivers


# --- the config block --------------------------------------------------------------------


def test_lags_block_tbd_refuses_naming_d_10_3() -> None:
    with pytest.raises(FeatureAvailabilityError) as excinfo:
        read_availability_lags(synthetic_snapshot(features={"availability_lags": TBD_SENTINEL}))
    assert "D-10.3" in str(excinfo.value)


def test_window_fields_tbd_refuse() -> None:
    lags = _lags()
    lags["f107_81_trailing"]["window"]["recomputation_tolerance"] = TBD_SENTINEL
    with pytest.raises(FeatureAvailabilityError) as excinfo:
        read_availability_lags(synthetic_snapshot(features={"availability_lags": lags}))
    assert "recomputation_tolerance" in str(excinfo.value)


# --- the matrix and limb 1 -------------------------------------------------------------


def test_matrix_records_six_fields_plus_anchor_and_latency_statement() -> None:
    snapshot = synthetic_snapshot(features={"availability_lags": _lags()})
    matrix = build_availability_matrix(snapshot, drivers=_drivers())
    by_feature = {row.feature: row for row in matrix}
    kp = by_feature["kp_safe"]
    assert kp.safe_lag_hours == KP_SAFE_LAG_H
    assert abs(kp.actual_lag_hours - 2.5) < 1e-9
    assert kp.release_status == "provisional" and kp.publication_timestamp
    f107 = by_feature["f107_81_trailing"]
    assert f107.publication_timestamp == "" and f107.latency_statement
    assert f107.anchor_policy and "recomputed" in f107.anchor_policy
    assert isinstance(kp, AvailabilityRow)


def test_limb_1_publication_after_the_origin_fails_the_lag_assertion() -> None:
    snapshot = synthetic_snapshot(features={"availability_lags": _lags()})
    matrix = build_availability_matrix(
        snapshot, drivers=_drivers(kp_safe=_kp_rows(publish_after=True))
    )
    with pytest.raises(LeakageError) as excinfo:
        assert_lags_safe(matrix)
    assert "actual lag" in str(excinfo.value) and "kp_safe" in str(excinfo.value)


def test_limb_1_actual_lag_below_safe_lag_fails() -> None:
    snapshot = synthetic_snapshot(features={"availability_lags": _lags()})
    matrix = build_availability_matrix(snapshot, drivers=_drivers(kp_safe=_kp_rows(lag_h=1.0)))
    with pytest.raises(LeakageError):
        assert_lags_safe(matrix)


def test_limb_1_passes_when_every_lag_clears_and_records_status() -> None:
    snapshot = synthetic_snapshot(features={"availability_lags": _lags()})
    matrix = build_availability_matrix(snapshot, drivers=_drivers(kp_safe=_kp_rows(lag_h=3.5)))
    assert_lags_safe(
        matrix,
        required_release_status={"kp_safe": "provisional", "f107_81_trailing": "observed"},
    )


def test_backfilled_final_grade_fails_where_provisional_was_required() -> None:
    snapshot = synthetic_snapshot(features={"availability_lags": _lags()})
    matrix = build_availability_matrix(
        snapshot, drivers=_drivers(kp_safe=_kp_rows(lag_h=3.5, grade="final"))
    )
    with pytest.raises(LeakageError) as excinfo:
        assert_lags_safe(matrix, required_release_status={"kp_safe": "provisional"})
    assert "backfill" in str(excinfo.value).lower() or "reanalysed" in str(excinfo.value)
    with pytest.raises(LeakageError):
        assert_release_status_not_backfilled("kp_safe", "final", required="provisional")


def test_mixed_grades_within_one_series_are_refused() -> None:
    rows = _kp_rows(lag_h=3.5)
    rows[1]["release_status"] = "final"
    snapshot = synthetic_snapshot(features={"availability_lags": _lags()})
    with pytest.raises(FeatureAvailabilityError) as excinfo:
        build_availability_matrix(snapshot, drivers=_drivers(kp_safe=rows))
    assert "distinct release grades" in str(excinfo.value)


def test_missing_publication_without_a_statement_is_refused() -> None:
    lags = _lags()
    del lags["f107_81_trailing"]["publication_latency_statement"]
    snapshot = synthetic_snapshot(features={"availability_lags": lags})
    with pytest.raises(FeatureAvailabilityError) as excinfo:
        build_availability_matrix(snapshot, drivers=_drivers())
    assert "publication_latency_statement" in str(excinfo.value)


def test_a_feature_without_driver_rows_is_refused_not_assumed() -> None:
    snapshot = synthetic_snapshot(features={"availability_lags": _lags()})
    drivers = _drivers()
    del drivers["kp_safe"]
    with pytest.raises(FeatureAvailabilityError):
        build_availability_matrix(snapshot, drivers=drivers)


def test_empty_matrix_is_not_an_assertion() -> None:
    with pytest.raises(LeakageError):
        assert_lags_safe(())


# --- limb 2: trailing, never centered ------------------------------------------------------


def test_limb_2_centered_window_fails() -> None:
    with pytest.raises(LeakageError) as excinfo:
        assert_trailing_not_centered("f107_81_trailing", {"kind": "centered", "days": 81})
    assert "centered" in str(excinfo.value)
    lags = _lags()
    lags["f107_81_trailing"]["window"]["kind"] = "centered"
    snapshot = synthetic_snapshot(features={"availability_lags": lags})
    with pytest.raises(LeakageError):
        build_availability_matrix(snapshot, drivers=_drivers())


# --- limb 3: the anchor, asserted AND recomputed -------------------------------------------


def test_limb_3_anchor_at_the_origin_day_fails_where_limbs_1_and_2_pass() -> None:
    """FR-P1-04-2's named hole: a TRAILING window ending at day t includes same-day F10.7."""
    rows = _f107_rows(anchor_offset_days=0)
    # limb 2 passes (kind is trailing); limb 1 would pass on lag alone:
    assert_trailing_not_centered("f107_81_trailing", _lags()["f107_81_trailing"]["window"])
    with pytest.raises(LeakageError) as excinfo:
        assert_anchor_recomputed(
            "f107_81_trailing",
            rows,
            daily_values={r["day"]: r["value"] for r in _daily()},
            safe_lag_hours=F107_SAFE_LAG_H,
            window_days=F107_WINDOW_DAYS,
            tolerance=F107_TOLERANCE,
        )
    assert "safe-lagged day" in str(excinfo.value)


def test_limb_3_correct_anchor_wrong_values_fails_on_the_recomputation() -> None:
    """A recorded-but-wrong anchor: the end date is right, the values came from elsewhere."""
    rows = _f107_rows(mean_shift=0.5)
    with pytest.raises(LeakageError) as excinfo:
        assert_anchor_recomputed(
            "f107_81_trailing",
            rows,
            daily_values={r["day"]: r["value"] for r in _daily()},
            safe_lag_hours=F107_SAFE_LAG_H,
            window_days=F107_WINDOW_DAYS,
            tolerance=F107_TOLERANCE,
        )
    assert "recomputed" in str(excinfo.value)


def test_limb_3_passes_on_the_correct_anchor_and_values() -> None:
    assert_anchor_recomputed(
        "f107_81_trailing",
        _f107_rows(),
        daily_values={r["day"]: r["value"] for r in _daily()},
        safe_lag_hours=F107_SAFE_LAG_H,
        window_days=F107_WINDOW_DAYS,
        tolerance=F107_TOLERANCE,
    )


def test_limb_3_missing_window_day_stops_rather_than_fills() -> None:
    """TC-20 through `trailing_mean`: a gap in the window is a stop, never a fill."""
    daily = {r["day"]: r["value"] for r in _daily()}
    del daily[dt.date(SYNTH_YEAR, 2, 6)]
    with pytest.raises(IntegrityError):
        assert_anchor_recomputed(
            "f107_81_trailing",
            _f107_rows(),
            daily_values=daily,
            safe_lag_hours=F107_SAFE_LAG_H,
            window_days=F107_WINDOW_DAYS,
            tolerance=F107_TOLERANCE,
        )


def test_limb_3_unrecorded_anchor_fails() -> None:
    rows = _f107_rows()
    for row in rows:
        row["anchor_day"] = None
    with pytest.raises(LeakageError) as excinfo:
        assert_anchor_recomputed(
            "f107_81_trailing",
            rows,
            daily_values={r["day"]: r["value"] for r in _daily()},
            safe_lag_hours=F107_SAFE_LAG_H,
            window_days=F107_WINDOW_DAYS,
            tolerance=F107_TOLERANCE,
        )
    assert "unrecorded anchor" in str(excinfo.value)


def test_trailing_row_without_anchor_record_fails_lags_safe() -> None:
    row = AvailabilityRow(
        feature="f107_81_trailing",
        observation_timestamp="x",
        publication_timestamp="",
        release_status="observed",
        safe_lag_hours=24.0,
        actual_lag_hours=30.0,
        anchor_policy=None,
        latency_statement="documented absence",
    )
    with pytest.raises(LeakageError) as excinfo:
        assert_lags_safe((row,))
    assert "third limb" in str(excinfo.value)


# --- D-25 availability rule (Route 1): a calendar-day rule, not a scalar ------------------
# `availability_ts(median(D-1)) = 00:00 UTC on D` (D-25). A scalar `safe_lag_hours` cannot
# state it, so a feature declares `availability_rule` INSTEAD. The rule identity below is
# the module's own closed-set token, not a frozen VALUE; every timestamp is synthetic.

RULE_FEATURE = "f107_safe"


def _rule_lags(**entry_overrides: Any) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "availability_rule": AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC,
        "release_status_required": "observed",
        "publication_latency_statement": (
            "fluxtable.txt carries no publication timestamp; the conservative D+1 00:00 UTC "
            "availability convention is recorded and the publication latency is unverified"
        ),
    }
    entry.update(entry_overrides)
    return _lags(**{RULE_FEATURE: entry})


def _rule_rows(
    origin_hours: tuple[int, ...] = (6, 12),
    *,
    observation_day_offset: int = -1,
    observation_hour: int = 22,
    publish_at: dt.datetime | None = None,
) -> list[dict[str, Any]]:
    """Origins on 9 Feb; the observation on day 9 Feb + `observation_day_offset`."""
    rows = []
    for hour in origin_hours:
        origin = _ts(2, 9, hour)
        observed = dt.datetime.combine(
            origin.date() + dt.timedelta(days=observation_day_offset),
            dt.time(observation_hour),
            tzinfo=UTC,
        )
        rows.append(
            {
                "forecast_origin": origin,
                "observation_timestamp": observed,
                "publication_timestamp": publish_at,
                "release_status": "observed",
            }
        )
    return rows


def _rule_matrix(rows: list[dict[str, Any]], **entry_overrides: Any) -> AvailabilityRow:
    snapshot = synthetic_snapshot(features={"availability_lags": _rule_lags(**entry_overrides)})
    matrix = build_availability_matrix(snapshot, drivers=_drivers(**{RULE_FEATURE: rows}))
    return {row.feature: row for row in matrix}[RULE_FEATURE]


def test_d25_rule_computes_next_day_midnight_availability() -> None:
    # observed 22:00 on 8 Feb -> available 00:00 UTC 9 Feb; tightest origin 06:00 -> 6 h.
    row = _rule_matrix(_rule_rows((6, 12)))
    assert row.availability_rule == AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC
    assert row.safe_lag_hours is None
    assert abs(row.actual_lag_hours - 6.0) < 1e-9
    assert row.observation_timestamp == _ts(2, 8, 22).isoformat()
    assert_lags_safe((row,), required_release_status={RULE_FEATURE: "observed"})


def test_d25_availability_instant_is_independent_of_the_origin_hour() -> None:
    instants = set()
    for hour in (1, 6, 12, 23):
        row = _rule_matrix(_rule_rows((hour,)))
        instants.add(_ts(2, 9, hour) - dt.timedelta(hours=row.actual_lag_hours))
    assert instants == {_ts(2, 9, 0)}


def test_d25_same_day_anchoring_is_refused() -> None:
    # the observation day IS the origin day: availability is 00:00 of the NEXT day.
    with pytest.raises(LeakageError) as excinfo:
        _rule_matrix(_rule_rows((12,), observation_day_offset=0, observation_hour=3))
    assert "precedes the availability instant" in str(excinfo.value)
    assert RULE_FEATURE in str(excinfo.value)


def test_d25_future_looking_anchoring_is_refused() -> None:
    # a centered / forward window would observe AFTER the origin day.
    with pytest.raises(LeakageError):
        _rule_matrix(_rule_rows((12,), observation_day_offset=1, observation_hour=0))


def test_d25_unknown_rule_kind_is_refused_at_config_read() -> None:
    for bad in ("same_day_midnight_utc", "", 3, None, TBD_SENTINEL):
        lags = _rule_lags(availability_rule=bad)
        with pytest.raises(FeatureAvailabilityError) as excinfo:
            read_availability_lags(synthetic_snapshot(features={"availability_lags": lags}))
        assert f"{RULE_FEATURE}.availability_rule" in str(excinfo.value)


def test_d25_rule_beside_a_scalar_lag_is_refused() -> None:
    for scalar in (24, 0, None):
        lags = _rule_lags(safe_lag_hours=scalar)
        with pytest.raises(FeatureAvailabilityError) as excinfo:
            read_availability_lags(synthetic_snapshot(features={"availability_lags": lags}))
        assert "never both" in str(excinfo.value)


def test_d25_rule_composes_with_a_trailing_window_only_for_that_rule() -> None:
    """A2 (`CR-2026-09-19-A2-RULE-WINDOW`): the D-25 rule may ride on the trailing row
    because it derives the window end day; a centered window, a scalar beside the rule,
    and a rule on a GFZ row are all still refused at config read."""
    window = dict(_lags()["f107_81_trailing"]["window"])
    accepted = _lags(f107_81_trailing=_rule_entry(window=window))
    lags = read_availability_lags(synthetic_snapshot(features={"availability_lags": accepted}))
    assert lags["f107_81_trailing"]["availability_rule"] == (
        AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC
    )
    centered = _lags(f107_81_trailing=_rule_entry(window={**window, "kind": "centered"}))
    with pytest.raises(LeakageError):
        build_availability_matrix(
            synthetic_snapshot(features={"availability_lags": centered}),
            drivers=_drivers(f107_81_trailing=_rule_trailing_rows()),
        )
    with_scalar = _lags(
        f107_81_trailing=_rule_entry(window=window, safe_lag_hours=F107_SAFE_LAG_H)
    )
    with pytest.raises(FeatureAvailabilityError, match="never both"):
        read_availability_lags(synthetic_snapshot(features={"availability_lags": with_scalar}))
    on_gfz = _lags(kp_safe=_rule_entry())
    with pytest.raises(FeatureAvailabilityError, match="governs only"):
        read_availability_lags(synthetic_snapshot(features={"availability_lags": on_gfz}))


def _rule_entry(**overrides: Any) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "availability_rule": AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC,
        "release_status_required": "observed",
        "publication_latency_statement": (
            "synthetic: no publication timestamp; D+1 00:00 UTC convention recorded; "
            "publication latency unverified"
        ),
    }
    entry.update(overrides)
    return entry


def _rule_trailing_rows(
    day: dt.date = dt.date(SYNTH_YEAR, 2, 9),
    hours: tuple[int, ...] = (6, 12),
    *,
    anchor_offset_days: int = 1,
    observation_hour: int = 23,
    publish_at: dt.datetime | None = None,
    mean_shift: float = 0.0,
) -> list[dict[str, Any]]:
    """Trailing rows with the HONEST constituent instant: the last daily median (day
    `anchor`) completes at `observation_hour` UT on that day — no anchor-day-midnight
    convention (A2)."""
    rows = []
    for hour in hours:
        origin = dt.datetime.combine(day, dt.time(hour), tzinfo=UTC)
        anchor = day - dt.timedelta(days=anchor_offset_days)
        rows.append(
            {
                "forecast_origin": origin,
                "observation_timestamp": dt.datetime.combine(
                    anchor, dt.time(observation_hour), tzinfo=UTC
                ),
                "publication_timestamp": publish_at,
                "release_status": "observed",
                "anchor_day": anchor,
                "mean_value": _trailing_mean(anchor) + mean_shift,
            }
        )
    return rows


def _rule_window_matrix(rows: list[dict[str, Any]], daily: list[dict[str, Any]] | None = None):
    window = dict(_lags()["f107_81_trailing"]["window"])
    lags = _lags(f107_81_trailing=_rule_entry(window=window))
    drivers = _drivers(f107_81_trailing=rows)
    if daily is not None:
        drivers["f107_daily"] = daily
    matrix = build_availability_matrix(
        synthetic_snapshot(features={"availability_lags": lags}), drivers=drivers
    )
    return {row.feature: row for row in matrix}["f107_81_trailing"]


def test_d25_window_anchors_at_the_latest_available_day_for_every_origin_hour() -> None:
    """All 24 origin hours on a mid-month day: anchor D−1 accepted with the honest
    observation instant (D−1 23:00); measured lag is the hour past 00:00 D; limb 1 passes
    under rule semantics; the recorded anchor policy names the rule."""
    for hour in range(24):
        row = _rule_window_matrix(_rule_trailing_rows(hours=(hour,)))
        assert row.availability_rule == AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC
        assert row.safe_lag_hours is None
        assert abs(row.actual_lag_hours - hour) < 1e-9
        assert row.anchor_policy and "latest observation day" in row.anchor_policy
        assert_lags_safe((row,))


def test_d25_window_end_day_across_month_and_year_boundaries() -> None:
    """The latest eligible end day is derived, not conventional: 1 Feb → 31 Jan and the
    synthetic-year 1 Jan → 31 Dec of the prior year, at 00:00 and 23:00."""
    daily = [
        {"day": dt.date(SYNTH_YEAR - 1, 12, 1) + dt.timedelta(days=n), "value": 50.0 + n}
        for n in range(80)
    ]
    values = {r["day"]: r["value"] for r in daily}

    def mean_to(end: dt.date) -> float:
        return sum(values[end - dt.timedelta(days=k)] for k in range(F107_WINDOW_DAYS)) / (
            F107_WINDOW_DAYS
        )

    for day, expected_anchor in (
        (dt.date(SYNTH_YEAR, 2, 1), dt.date(SYNTH_YEAR, 1, 31)),
        (dt.date(SYNTH_YEAR, 1, 1), dt.date(SYNTH_YEAR - 1, 12, 31)),
    ):
        for hour in (0, 23):
            origin = dt.datetime.combine(day, dt.time(hour), tzinfo=UTC)
            assert (
                latest_eligible_window_end(
                    AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC, origin, resource="t"
                )
                == expected_anchor
            )
            rows = [
                {
                    "forecast_origin": origin,
                    "observation_timestamp": dt.datetime.combine(
                        expected_anchor, dt.time(23), tzinfo=UTC
                    ),
                    "publication_timestamp": None,
                    "release_status": "observed",
                    "anchor_day": expected_anchor,
                    "mean_value": mean_to(expected_anchor),
                }
            ]
            row = _rule_window_matrix(rows, daily=daily)
            assert abs(row.actual_lag_hours - hour) < 1e-9


def test_d25_window_refuses_same_day_stale_and_unavailable_constituents() -> None:
    """Anchor AT the origin day (a constituent not yet available) → refused; anchor at
    D−2 (stale end day) → refused; a missing constituent inside the window → the
    approved missing-day behaviour (IntegrityError, never filled)."""
    # a same-day constituent is caught first by limb 1's build-time refusal (its
    # availability instant is after the origin); the anchor limb would refuse it too.
    with pytest.raises(LeakageError, match="precedes the availability instant"):
        _rule_window_matrix(_rule_trailing_rows(anchor_offset_days=0, observation_hour=3))
    rows = _rule_trailing_rows(anchor_offset_days=0, observation_hour=3)
    with pytest.raises(LeakageError, match="third limb"):
        assert_anchor_recomputed(
            "f107_81_trailing",
            rows,
            daily_values={r["day"]: r["value"] for r in _daily()},
            safe_lag_hours=None,
            window_days=F107_WINDOW_DAYS,
            tolerance=F107_TOLERANCE,
            availability_rule=AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC,
        )
    with pytest.raises(LeakageError, match="third limb"):
        _rule_window_matrix(_rule_trailing_rows(anchor_offset_days=2))
    holed = [r for r in _daily() if r["day"] != dt.date(SYNTH_YEAR, 2, 6)]
    with pytest.raises(IntegrityError):
        _rule_window_matrix(_rule_trailing_rows(), daily=holed)
    with pytest.raises(LeakageError, match="recomputed"):
        _rule_window_matrix(_rule_trailing_rows(mean_shift=1.0))


def test_d25_window_row_honours_a_later_publication_timestamp() -> None:
    """A publication timestamp after the rule instant still governs limb 1 (max)."""
    row = _rule_window_matrix(_rule_trailing_rows(hours=(6,), publish_at=_ts(2, 9, 3)))
    assert abs(row.actual_lag_hours - 3.0) < 1e-9
    early = _rule_window_matrix(_rule_trailing_rows(hours=(6,), publish_at=_ts(2, 8, 23)))
    assert abs(early.actual_lag_hours - 6.0) < 1e-9


def test_d25_constituent_availability_is_monotone_so_the_anchor_bounds_the_window() -> None:
    """The invariant behind the anchor limb's per-constituent loop (A2 mutant disposition):
    under D-25 the constituent availability instant is strictly increasing in the
    observation day, so with the anchor fixed at the latest eligible day every earlier
    window day is available strictly before it — an interior day can never become
    available after the origin under the supported contract (daily rows carry `day` and
    `value` only; no per-day publication timestamp exists to move one). Checked across a
    year of consecutive days including the month and year boundaries."""
    from src.features.availability import _constituent_available_at

    rule = AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC
    days = [dt.date(SYNTH_YEAR - 1, 12, 1) + dt.timedelta(days=n) for n in range(400)]
    instants = [_constituent_available_at(rule, day, resource="t") for day in days]
    assert all(later > earlier for earlier, later in zip(instants, instants[1:], strict=False))
    assert all(
        instant == dt.datetime.combine(day + dt.timedelta(days=1), dt.time(0), tzinfo=UTC)
        for day, instant in zip(days, instants, strict=True)
    )
    for hour in (0, 11, 23):
        origin = _ts(2, 9, hour)
        anchor = latest_eligible_window_end(rule, origin, resource="t")
        assert _constituent_available_at(rule, anchor, resource="t") <= origin
        assert all(
            _constituent_available_at(rule, anchor - dt.timedelta(days=k), resource="t") < origin
            for k in range(1, F107_WINDOW_DAYS)
        )


def test_trailing_window_membership_is_exactly_the_declared_days_ending_at_the_anchor() -> None:
    """Exact membership: the window ending at the anchor is [anchor − (N−1), anchor]. The
    recorded mean survives a perturbation of day anchor − N (outside) and fails on a
    perturbation of day anchor − (N−1) (the oldest member) and of the anchor itself; a
    missing member stops rather than shifting to an older window (TC-20)."""
    rule = AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC
    origin = _ts(2, 9, 6)
    anchor = latest_eligible_window_end(rule, origin, resource="t")
    assert anchor == dt.date(SYNTH_YEAR, 2, 8)
    values = {r["day"]: r["value"] for r in _daily()}
    rows = _rule_trailing_rows(hours=(6,))
    kwargs: dict[str, Any] = dict(
        safe_lag_hours=None,
        window_days=F107_WINDOW_DAYS,
        tolerance=F107_TOLERANCE,
        availability_rule=rule,
    )
    assert_anchor_recomputed("f107_81_trailing", rows, daily_values=values, **kwargs)
    outside = dict(values)
    outside[anchor - dt.timedelta(days=F107_WINDOW_DAYS)] += 50.0
    assert_anchor_recomputed("f107_81_trailing", rows, daily_values=outside, **kwargs)
    for member in (anchor - dt.timedelta(days=F107_WINDOW_DAYS - 1), anchor):
        perturbed = dict(values)
        perturbed[member] += 50.0
        with pytest.raises(LeakageError, match="recomputed"):
            assert_anchor_recomputed("f107_81_trailing", rows, daily_values=perturbed, **kwargs)
    holed = {d: v for d, v in values.items() if d != anchor - dt.timedelta(days=2)}
    with pytest.raises(IntegrityError):
        assert_anchor_recomputed("f107_81_trailing", rows, daily_values=holed, **kwargs)


def test_real_fluxtable_carries_every_day_of_the_window_ending_before_2022() -> None:
    """Pre-2022 coverage of the held provider file (a driver-only R-26 class-2 file; no
    December-2022 line is inspected — only dates before 2022 are read): the 81 UT days
    ending 2021-12-31, which the first 2022 origin's window needs, are all present with at
    least one observed reading each. A coverage fact, not a value; nothing is filled."""
    flux = REPO_ROOT / "evidence" / "audit_ec1_2026-08-15" / "nrcan_f107" / "fluxtable.txt"
    if not flux.is_file():
        pytest.skip("provider file not held in this clone")
    needed = {dt.date(2021, 12, 31) - dt.timedelta(days=k) for k in range(81)}
    seen: set[dt.date] = set()
    with flux.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            stamp = line[:8]
            if stamp.isdigit() and stamp < "20220101":
                seen.add(dt.datetime.strptime(stamp, "%Y%m%d").date())
    assert needed <= seen
    assert min(needed) == dt.date(2021, 10, 12)


def test_interval_end_observation_timestamps_make_the_lag_a_post_completion_margin() -> None:
    """Synthetic boundary cases for the interval-valued indices (Kp/ap 3 h, Hp60/ap60 1 h),
    with `observation_timestamp` = the interval END (its completion instant — D-10.3: the
    instant the value could first have been known). The declared lag is then a margin
    AFTER completion: the value of [03,06) UT is refused at origins 06:00, 07:00 and 08:00
    and admitted from 09:00; the value of [04,05) UT is refused at 05:00 and admitted at
    06:00. The last case shows the trap the convention exists to close: the SAME [03,06)
    value labelled by its interval START (03:00, the provider file's own label) clears a
    3-hour lag at 06:00 — the moment the interval completes, with no publication margin
    at all — and the matrix cannot tell the two labellings apart. The interval-end
    convention is therefore a producer-contract obligation (proposal P-1,
    `CR-2026-09-19-SCI-REVIEW`), pinned here only in its arithmetic."""

    def row(origin_hour: int, observed_hour: int) -> dict[str, Any]:
        return {
            "forecast_origin": _ts(2, 9, origin_hour),
            "observation_timestamp": _ts(2, 9, observed_hour),
            "publication_timestamp": None,
            "release_status": "provisional",
        }

    def lag_of(feature: str, rows: list[dict[str, Any]]) -> tuple[float, AvailabilityRow]:
        statement = "synthetic: no publication timestamp held; latency unverified"
        lags = _lags(
            kp_safe={
                "safe_lag_hours": 3,
                "lag_reference_instant": "interval_end_utc",
                "selection_rule": "latest_completed_interval_plus_lag",
                "release_status_required": "provisional",
                "publication_latency_statement": statement,
            },
            hp60_safe={
                "safe_lag_hours": 1,
                "lag_reference_instant": "interval_end_utc",
                "selection_rule": "latest_completed_interval_plus_lag",
                "release_status_required": "provisional",
                "publication_latency_statement": statement,
            },
        )
        snapshot = synthetic_snapshot(features={"availability_lags": lags})
        drivers = _drivers(
            kp_safe=rows if feature == "kp_safe" else [row(12, 9)],
            hp60_safe=rows if feature == "hp60_safe" else [row(12, 11)],
        )
        by = {r.feature: r for r in build_availability_matrix(snapshot, drivers=drivers)}
        return by[feature].actual_lag_hours, by[feature]

    # Kp/ap: interval [03,06) completes at 06:00; observation_timestamp = 06:00
    for origin_hour, expected in ((6, 0.0), (7, 1.0), (8, 2.0)):
        lag, matrix_row = lag_of("kp_safe", [row(origin_hour, 6)])
        assert lag == expected
        with pytest.raises(LeakageError):
            assert_lags_safe((matrix_row,))
    lag, matrix_row = lag_of("kp_safe", [row(9, 6)])
    assert lag == 3.0
    assert_lags_safe((matrix_row,))
    # Hp60/ap60: interval [04,05) completes at 05:00
    lag, matrix_row = lag_of("hp60_safe", [row(5, 5)])
    assert lag == 0.0
    with pytest.raises(LeakageError):
        assert_lags_safe((matrix_row,))
    lag, matrix_row = lag_of("hp60_safe", [row(6, 5)])
    assert lag == 1.0
    assert_lags_safe((matrix_row,))
    # the trap: the same [03,06) value labelled by its START clears 3 h at completion
    lag, matrix_row = lag_of("kp_safe", [row(6, 3)])
    assert lag == 3.0
    assert_lags_safe((matrix_row,))  # passes — exactly why P-1 must pin interval END


def test_d47_tolerance_derivation_against_an_exact_reference_and_the_certified_domain() -> None:
    """D-47's certificate, checked rather than asserted: (i) the a-priori bound
    (N+1)·2⁻⁵²·B for N = 81, B = 400 is 7.28e-12 < the frozen 8.0e-12; (ii) on constituents
    from the project's own grid (D-21 medians of 0.1-sfu readings, D-22 half-grid means →
    multiples of 0.05 sfu) inside the domain, |float mean − exact rational mean| stays
    below the bound over every window (independent `Fraction` reference, no floating
    point); (iii) `json` round-trips the float exactly while a 6-decimal writer would not;
    (iv) must-fail perturbations — an 80-day window and a one-day-shifted anchor — exceed
    the tolerance by ten orders; (v) a constituent outside the certified domain fails the
    certification clearly and is left unchanged, never clipped."""
    import json
    import random
    from fractions import Fraction

    from src.external.spaceweather import trailing_mean
    from src.features.availability import (
        assert_recomputation_domain,
        recomputation_tolerance_bound,
    )

    n, bound, tolerance = 81, 400.0, 8.0e-12
    apriori = recomputation_tolerance_bound(window_days=n, input_bound=bound)
    assert 7.2e-12 < apriori < 7.3e-12 and apriori < tolerance < 1e-11
    rng = random.Random(20221201)
    days = [dt.date(SYNTH_YEAR - 1, 1, 1) + dt.timedelta(days=i) for i in range(400)]
    exact = {d: Fraction(rng.randint(60 * 20, int(bound) * 20), 20) for d in days}
    values = {d: float(v) for d, v in exact.items()}
    worst = 0.0
    six_decimal_violations = 0
    for end in days[n - 1 :]:
        mean = trailing_mean(values, end_day=end, window_days=n)
        reference = sum(exact[end - dt.timedelta(days=k)] for k in range(n)) / n
        worst = max(worst, abs(float(Fraction(mean) - reference)))
        assert json.loads(json.dumps(mean)) == mean  # repr round trip is exact
        if abs(float(f"{mean:.6f}") - mean) > tolerance:
            six_decimal_violations += 1
    assert worst < apriori < tolerance
    assert six_decimal_violations > 300  # a fixed-precision writer breaks the certificate
    end = days[200]
    mean = trailing_mean(values, end_day=end, window_days=n)
    assert abs(trailing_mean(values, end_day=end, window_days=n - 1) - mean) > 1e-3
    assert (
        abs(trailing_mean(values, end_day=end - dt.timedelta(days=1), window_days=n) - mean) > 1e-3
    )
    assert_recomputation_domain(values, input_bound=bound, feature="f107_81_trailing")
    outside = dict(values)
    outside[days[10]] = 400.05
    with pytest.raises(IntegrityError, match="numerical certification FAILS"):
        assert_recomputation_domain(outside, input_bound=bound, feature="f107_81_trailing")
    assert outside[days[10]] == 400.05  # kept unchanged: never clipped or deleted
    rows = _rule_trailing_rows(hours=(6,))
    daily = {r["day"]: r["value"] for r in _daily()}
    assert_anchor_recomputed(
        "f107_81_trailing",
        rows,
        daily_values=daily,
        safe_lag_hours=None,
        window_days=F107_WINDOW_DAYS,
        tolerance=F107_TOLERANCE,
        availability_rule=AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC,
        input_bound=bound,
    )
    with pytest.raises(IntegrityError, match="certified input domain"):
        assert_anchor_recomputed(
            "f107_81_trailing",
            rows,
            daily_values=daily,
            safe_lag_hours=None,
            window_days=F107_WINDOW_DAYS,
            tolerance=F107_TOLERANCE,
            availability_rule=AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC,
            input_bound=50.0,
        )


def test_a_rule_without_window_support_cannot_compose_with_a_window(monkeypatch) -> None:
    """Only rules in AVAILABILITY_RULES_WITH_WINDOW may carry a window. Exercised with a
    synthetic second rule kind admitted to the closed set and scope but not to the
    window-capable set — the branch is unreachable with today's single rule otherwise."""
    from src.features import availability as mod

    fake = "synthetic_rule_without_window_support"
    monkeypatch.setattr(mod, "AVAILABILITY_RULE_KINDS", frozenset({fake}))
    monkeypatch.setattr(mod, "AVAILABILITY_RULE_SCOPE", {fake: frozenset({"f107_81_trailing"})})
    window = dict(_lags()["f107_81_trailing"]["window"])
    lags = _lags(f107_81_trailing=_rule_entry(availability_rule=fake, window=window))
    with pytest.raises(FeatureAvailabilityError, match="cannot derive a window end day"):
        read_availability_lags(synthetic_snapshot(features={"availability_lags": lags}))


def test_d25_scalar_path_of_the_anchor_limb_is_unchanged() -> None:
    """The scalar-lag trailing feature (fixture convention) behaves exactly as before, and
    the anchor limb refuses neither-or-both of scalar and rule."""
    snapshot = synthetic_snapshot(features={"availability_lags": _lags()})
    matrix = build_availability_matrix(snapshot, drivers=_drivers())
    f107 = {row.feature: row for row in matrix}["f107_81_trailing"]
    assert f107.safe_lag_hours == F107_SAFE_LAG_H and f107.availability_rule is None
    assert f107.anchor_policy == "window ends at the safe-lagged day; mean recomputed from anchor"
    for kwargs in (
        {"safe_lag_hours": None, "availability_rule": None},
        {
            "safe_lag_hours": 24.0,
            "availability_rule": AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC,
        },
    ):
        with pytest.raises(IntegrityError, match="exactly one"):
            assert_anchor_recomputed(
                "f107_81_trailing",
                _f107_rows(),
                daily_values={},
                window_days=F107_WINDOW_DAYS,
                tolerance=F107_TOLERANCE,
                **kwargs,
            )


def test_neither_scalar_nor_rule_is_refused_naming_both() -> None:
    lags = _lags(**{RULE_FEATURE: {"release_status_required": "observed"}})
    with pytest.raises(FeatureAvailabilityError) as excinfo:
        read_availability_lags(synthetic_snapshot(features={"availability_lags": lags}))
    text = str(excinfo.value)
    assert "safe_lag_hours" in text and "availability_rule" in text and "never neither" in text


def test_d25_later_publication_timestamp_still_governs() -> None:
    # rule instant 00:00 9 Feb; published 03:00 9 Feb; origin 06:00 -> lag 3 h, not 6 h.
    row = _rule_matrix(_rule_rows((6,), publish_at=_ts(2, 9, 3)))
    assert abs(row.actual_lag_hours - 3.0) < 1e-9
    assert row.publication_timestamp == _ts(2, 9, 3).isoformat()
    # and an earlier publication never pulls availability BEFORE the rule instant.
    early = _rule_matrix(_rule_rows((6,), publish_at=_ts(2, 8, 23)))
    assert abs(early.actual_lag_hours - 6.0) < 1e-9


def test_scalar_features_keep_their_previous_rows_beside_a_rule_feature() -> None:
    snapshot = synthetic_snapshot(features={"availability_lags": _rule_lags()})
    by_feature = {
        row.feature: row
        for row in build_availability_matrix(
            snapshot, drivers=_drivers(**{RULE_FEATURE: _rule_rows()})
        )
    }
    kp = by_feature["kp_safe"]
    assert kp.safe_lag_hours == KP_SAFE_LAG_H and kp.availability_rule is None
    assert abs(kp.actual_lag_hours - 2.5) < 1e-9
    f107 = by_feature["f107_81_trailing"]
    assert f107.safe_lag_hours == F107_SAFE_LAG_H and f107.availability_rule is None
    assert f107.anchor_policy and "recomputed" in f107.anchor_policy
    # limb 1 still bites on the scalar row exactly as before
    with pytest.raises(LeakageError) as excinfo:
        assert_lags_safe(
            tuple(
                build_availability_matrix(
                    snapshot,
                    drivers=_drivers(**{RULE_FEATURE: _rule_rows(), "kp_safe": _kp_rows(1.0)}),
                )
            )
        )
    assert "kp_safe" in str(excinfo.value)


def test_availability_lags_stays_fail_closed_with_a_rule_present() -> None:
    # a rule entry never unlocks a partial block: the block itself, a TBD scalar sibling and
    # an empty block all still refuse.
    for block in (TBD_SENTINEL, None, {}, "not a mapping"):
        with pytest.raises(FeatureAvailabilityError):
            read_availability_lags(synthetic_snapshot(features={"availability_lags": block}))
    lags = _rule_lags()
    lags["kp_safe"]["safe_lag_hours"] = TBD_SENTINEL
    with pytest.raises(FeatureAvailabilityError) as excinfo:
        read_availability_lags(synthetic_snapshot(features={"availability_lags": lags}))
    assert "kp_safe.safe_lag_hours" in str(excinfo.value)


def test_lags_safe_refuses_a_negative_rule_lag_and_a_row_with_neither() -> None:
    base = dict(
        feature=RULE_FEATURE,
        observation_timestamp=_ts(2, 8, 22).isoformat(),
        publication_timestamp="",
        release_status="observed",
        actual_lag_hours=-1.0,
        latency_statement="documented absence",
    )
    negative = AvailabilityRow(
        safe_lag_hours=None,
        availability_rule=AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC,
        **base,
    )
    with pytest.raises(LeakageError) as excinfo:
        assert_lags_safe((negative,))
    assert "negative" in str(excinfo.value)
    neither = AvailabilityRow(safe_lag_hours=None, availability_rule=None, **base)
    with pytest.raises(LeakageError) as excinfo:
        assert_lags_safe((neither,))
    assert "neither" in str(excinfo.value)
    both = AvailabilityRow(
        safe_lag_hours=3.0,
        availability_rule=AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC,
        **{**base, "actual_lag_hours": 6.0},
    )
    with pytest.raises(LeakageError):
        assert_lags_safe((both,))


def test_prepared_six_entry_availability_lags_load_without_error() -> None:
    """D-42/D-43/D-46/D-47's six-entry transcription (2026-09-19,
    `CR-2026-09-19-SCI-DECISIONS` item 6), on the real `configs/features.yaml`: exactly
    the six §6.2 driver rows, the two GFZ rows carrying scalar `safe_lag_hours` (3, 1),
    the two F10.7 rows carrying `availability_rule` (D-25) with the trailing window on
    `f107_81_trailing` only, `carry_forward_bound_hours`/`carry_forward_composition`
    frozen (D-46), and the window's tolerance/domain at D-47's values. The reader
    (`read_availability_lags`) accepts the file unmodified and carries the ADDITIVE
    fields (`lag_reference_instant`, `selection_rule`,
    `window.recomputation_input_bound_sfu`) through without asserting them — a reviewed
    reader change is owed before they are enforced, not before they are recorded (this
    test is that verification, not that enforcement). Reads the real file through a bare
    YAML parse, no snapshot directory written: a test of the transcription, not a
    governed run."""
    yaml = pytest.importorskip("yaml")
    features = yaml.safe_load(
        (REPO_ROOT / "configs" / "features.yaml").read_text(encoding="utf-8")
    )

    assert features["carry_forward_bound_hours"] == 3
    assert features["carry_forward_composition"] == "clock_hours"

    lags = read_availability_lags(synthetic_snapshot(features=features))
    assert sorted(lags) == [
        "ap60_safe",
        "ap_safe",
        "f107_81_trailing",
        "f107_safe",
        "hp60_safe",
        "kp_safe",
    ]
    for name, expected_lag in (("kp_safe", 3), ("ap_safe", 3), ("hp60_safe", 1), ("ap60_safe", 1)):
        entry = lags[name]
        assert entry["safe_lag_hours"] == expected_lag
        assert "availability_rule" not in entry
        assert entry["lag_reference_instant"] == "interval_end_utc"
        assert entry["selection_rule"] == "latest_completed_interval_plus_lag"
        assert entry["publication_latency_statement"].strip()
    for name in ("f107_safe", "f107_81_trailing"):
        entry = lags[name]
        assert entry["availability_rule"] == AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC
        assert "safe_lag_hours" not in entry
    window = lags["f107_81_trailing"]["window"]
    assert window["kind"] == "trailing" and window["days"] == 81
    assert window["recomputation_tolerance"] == pytest.approx(8.0e-12)
    assert window["recomputation_input_bound_sfu"] == 400
    assert "window" not in lags["f107_safe"]

    # the D-47 tolerance actually loaded is the certified bound this pass derived and
    # verified (test_d47_tolerance_derivation_...): not re-derived here, only carried.
    from src.features.availability import recomputation_tolerance_bound

    apriori = recomputation_tolerance_bound(window_days=81, input_bound=400.0)
    assert apriori < window["recomputation_tolerance"] < 1e-11

    from src.features.build import _is_tbd, _read_carry_forward_bound

    assert not _is_tbd(features["carry_forward_bound_hours"])
    assert (
        _read_carry_forward_bound(synthetic_snapshot(features=features))
        == features["carry_forward_bound_hours"]
    )


def test_f107_source_series_keys_never_collide_on_the_real_config() -> None:
    """D-60/D-66 (2026-09-23): `f107_safe`, `f107_81_trailing` and the trailing window's
    `window.source` were once all keyed by the single literal `f107_daily_median`, so one
    mapping key returned one frame to fields/consumers needing incompatible row shapes
    (`build_features` needs an hourly value per epoch for `f107_safe`;
    `build_availability_matrix`'s trailing limb needs one value per day for the 81-day
    window). Fixed by giving `f107_safe` its own `source_series`
    (`f107_safe_at_origin`) and `f107_81_trailing` its own (`f107_81_trailing_mean`),
    leaving `f107_daily_median` as the plain daily series D-21 defines and the one the
    trailing window's `window.source` still names. This is a NEGATIVE CONTROL against the
    collision recurring under a third field: the three keys the two F10.7 consumers read
    must always be pairwise distinct, on the real, committed `configs/features.yaml` —
    not a synthetic fixture, since the whole point is that this file cannot regress."""
    yaml = pytest.importorskip("yaml")
    features = yaml.safe_load(
        (REPO_ROOT / "configs" / "features.yaml").read_text(encoding="utf-8")
    )

    dictionary = features["feature_dictionary"]
    f107_safe_series = dictionary["f107_safe"]["source_series"]
    f107_trailing_series = dictionary["f107_81_trailing"]["source_series"]
    window_source = features["availability_lags"]["f107_81_trailing"]["window"]["source"]

    keys = {f107_safe_series, f107_trailing_series, window_source}
    assert len(keys) == 3, (
        f"expected f107_safe.source_series, f107_81_trailing.source_series and "
        f"f107_81_trailing.window.source to be three DISTINCT keys, got {keys!r} — a "
        f"collision here silently gives f107_safe and/or f107_81_trailing the wrong "
        f"values (D-66)"
    )
    assert f107_safe_series == "f107_safe_at_origin"
    assert f107_trailing_series == "f107_81_trailing_mean"
    assert window_source == "f107_daily_median"

    # `load_feature_dictionary` still accepts the file, and D-60's frozen field count
    # (21 fields) is unchanged by the rename. (The distinct `dictionary_row` count is
    # NOT re-asserted here as "13": measured directly on this file it is 16, not 13 --
    # D-60's own "13 dictionary rows" phrase evidently counts something other than
    # `len(set(dictionary_row for field in fields))`, e.g. rows shared with support/other
    # fields outside `feature_dictionary`, and re-deriving that distinction is outside
    # this negative control's purpose. Carrying the un-rederived "13" here would repeat
    # exactly the mistake `project.md` warns against -- a count taken from prose rather
    # than derived and printed.)
    snapshot = synthetic_snapshot(features=features)
    loaded = load_feature_dictionary(snapshot)
    assert len(loaded) == 21


def test_reader_enforces_d43_d44_reference_instant_and_selection_rule() -> None:
    """D-43/D-44 at the reader boundary: a scalar-lag (GFZ-style) row REQUIRES
    `lag_reference_instant` and `selection_rule`, each drawn from a CLOSED set; a
    rule-governed row (F10.7) FORBIDS both, since D-25's rule already fixes its own
    reference instant and has no interval to select from. Positive and negative controls
    for every combination — required-absent, unrecognised value, and forbidden-present."""
    good = _lags()
    read_availability_lags(synthetic_snapshot(features={"availability_lags": good}))  # passes

    for missing_field in ("lag_reference_instant", "selection_rule"):
        broken = _lags()
        del broken["kp_safe"][missing_field]
        with pytest.raises(FeatureAvailabilityError, match=missing_field):
            read_availability_lags(synthetic_snapshot(features={"availability_lags": broken}))

    for field, junk in (
        ("lag_reference_instant", "interval_start_utc"),
        ("selection_rule", "earliest_completed_interval_plus_lag"),
    ):
        broken = _lags()
        broken["kp_safe"][field] = junk
        with pytest.raises(FeatureAvailabilityError, match="not a recognised"):
            read_availability_lags(synthetic_snapshot(features={"availability_lags": broken}))

    for field in ("lag_reference_instant", "selection_rule"):
        broken = _rule_lags(**{field: "interval_end_utc"})
        with pytest.raises(FeatureAvailabilityError, match=field):
            read_availability_lags(synthetic_snapshot(features={"availability_lags": broken}))


def test_reader_enforces_d47_recomputation_input_bound() -> None:
    """D-47's applicability-domain field is REQUIRED alongside the tolerance it bounds
    (never an unchecked pass-through), on both the scalar-lag-plus-window shape and the
    rule-plus-window shape (A2), and must be a positive number."""
    good = _lags()
    read_availability_lags(synthetic_snapshot(features={"availability_lags": good}))

    missing = _lags()
    del missing["f107_81_trailing"]["window"]["recomputation_input_bound_sfu"]
    with pytest.raises(FeatureAvailabilityError, match="recomputation_input_bound_sfu"):
        read_availability_lags(synthetic_snapshot(features={"availability_lags": missing}))

    for junk in (-1, 0, "400", True):
        bad = _lags()
        bad["f107_81_trailing"]["window"]["recomputation_input_bound_sfu"] = junk
        with pytest.raises(FeatureAvailabilityError, match="recomputation_input_bound_sfu"):
            read_availability_lags(synthetic_snapshot(features={"availability_lags": bad}))

    # the rule-plus-window shape (A2) needs it too — same field, same requirement
    window = dict(_lags()["f107_81_trailing"]["window"])
    rule_missing = dict(window)
    del rule_missing["recomputation_input_bound_sfu"]
    rule_lags = _rule_lags(window=rule_missing)
    with pytest.raises(FeatureAvailabilityError, match="recomputation_input_bound_sfu"):
        read_availability_lags(synthetic_snapshot(features={"availability_lags": rule_lags}))


def test_build_availability_matrix_actually_applies_the_configured_input_bound() -> None:
    """The integration gap this pass closes: `recomputation_input_bound_sfu` reaching
    `assert_anchor_recomputed`'s `input_bound` is NOT exercised merely by a caller who
    remembers to pass it directly — it must be applied by the REAL matrix-build path,
    `build_availability_matrix`, from the config it was handed. A daily constituent
    exceeding the configured bound fails the certification through THAT path, and
    lowering the configured bound (never touching the constituents) is what flips the
    same window from passing to failing — proving the value in `configs/features.yaml`
    is what governs, not a hardcoded default."""
    window = dict(_lags()["f107_81_trailing"]["window"])
    lags = _lags(f107_81_trailing=_rule_entry(window=window))
    snapshot = synthetic_snapshot(features={"availability_lags": lags})
    rows = _rule_trailing_rows(hours=(6,))  # values are 100.0 .. 109.0 (well inside 400 sfu)
    drivers = _drivers(f107_81_trailing=rows, f107_daily=_daily())
    build_availability_matrix(snapshot, drivers=drivers)  # passes: 400 sfu bound, values ~100-109

    tight = _lags(
        f107_81_trailing=_rule_entry(window={**window, "recomputation_input_bound_sfu": 5})
    )
    tight_snapshot = synthetic_snapshot(features={"availability_lags": tight})
    with pytest.raises(IntegrityError, match="numerical certification FAILS"):
        build_availability_matrix(tight_snapshot, drivers=drivers)


def test_config_declared_selection_mechanics_are_cross_checked_against_the_driver() -> None:
    """D-43/D-44 end to end, closing the remaining integration gap: the availability
    matrix's `selection_rule` and `lag_reference_instant` (populated from
    `configs/features.yaml` by `build_availability_matrix`) are cross-checked by
    `build_features` against the driver's ACTUAL `attrs["selection"]` — a config that
    declares one selection mechanism while the producer implements another is refused,
    and a `lag_reference_instant` this project's code cannot honour is refused as a
    drift guard, never silently accepted."""
    from src.external.spaceweather import (
        SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG,
        select_lagged_series,
    )
    from src.features._frames import records_of

    snapshot = synthetic_snapshot(features=_base_features())
    target, drivers, _old_matrix, spec = _happy_inputs(snapshot)
    matrix = (
        AvailabilityRow(
            feature="kp_safe",
            observation_timestamp="x",
            publication_timestamp="y",
            release_status="provisional",
            safe_lag_hours=3.0,
            actual_lag_hours=3.5,
            selection_rule=SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG,
            lag_reference_instant="interval_end_utc",
        ),
    )
    start = spec.scored_start
    hours = len(list(records_of(drivers["kp"])))
    observations = [
        {
            "value": float(100 + k),
            "interval_start": start + dt.timedelta(hours=3 * k),
            "interval_end": start + dt.timedelta(hours=3 * k + 3),
        }
        for k in range(hours // 3 + 1)
    ]
    epochs = [start + dt.timedelta(hours=h) for h in range(hours)]
    lagged = RecordFrame(select_lagged_series(observations, epochs=epochs, safe_lag_hours=3))
    lagged.attrs["producing_artifact"] = "gfz_kp_provisional"
    lagged.attrs["observations"] = observations
    lagged.attrs["selection"] = {
        "rule": SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG,
        "safe_lag_hours": 3,
    }

    def build(frame, mat):
        return build_features(
            target,
            drivers={"kp": frame},
            registry={},
            matrix=mat,
            spec=spec,
            partitions=PARTITIONS,
            snapshot=snapshot,
            parity_tolerance=0.0,
        )

    build(lagged, matrix)  # config and driver agree: passes

    mismatched_rule = (
        AvailabilityRow(
            feature="kp_safe",
            observation_timestamp="x",
            publication_timestamp="y",
            release_status="provisional",
            safe_lag_hours=3.0,
            actual_lag_hours=3.5,
            selection_rule="a_different_mechanism_entirely",
            lag_reference_instant="interval_end_utc",
        ),
    )
    with pytest.raises(AlignmentError, match="differs from configs/features.yaml"):
        build(lagged, mismatched_rule)

    mismatched_instant = (
        AvailabilityRow(
            feature="kp_safe",
            observation_timestamp="x",
            publication_timestamp="y",
            release_status="provisional",
            safe_lag_hours=3.0,
            actual_lag_hours=3.5,
            selection_rule=SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG,
            lag_reference_instant="interval_start_utc",  # not implemented by the selector
        ),
    )
    with pytest.raises(AlignmentError, match="lag_reference_instant"):
        build(lagged, mismatched_instant)


# --- Dst diagnostic-only; SSN absent (grep-class) ----------------------------------------


def test_dst_declared_as_a_model_input_fails() -> None:
    with pytest.raises(LeakageError):
        assert_dst_diagnostic_only({"dst_index": "driver"})
    assert assert_dst_diagnostic_only({"dst_index": "diagnostic", "kp_safe": "driver"}) is None


def test_ssn_is_absent_from_src_identifiers_and_the_dictionary_rows() -> None:
    """TA-08's grep-class limb: no identifier or string field name under src/ names SSN, and
    the closed row table carries no ssn row (it is REMOVED, and declaring it raises)."""
    needle = "ssn"
    hits: list[str] = []
    for module in sorted((REPO_ROOT / "src").rglob("*.py")):
        with tokenize.open(module) as handle:
            for token in tokenize.generate_tokens(handle.readline):
                if token.type == tokenize.NAME and needle in token.string.lower().split("_"):
                    hits.append(f"{module.relative_to(REPO_ROOT).as_posix()}:{token.start[0]}")
    assert hits == [], f"SSN identifiers found under src/: {hits}"
    assert needle not in SECTION_6_2_ROWS
    snapshot = synthetic_snapshot(
        features={
            "feature_dictionary": {
                "ssn_daily": {"dictionary_row": "ssn", "normalization": "none"},
            }
        }
    )
    with pytest.raises(LeakageError) as excinfo:
        load_feature_dictionary(snapshot)
    assert "REMOVED" in str(excinfo.value)


# --- the closed dictionary (R-76; TA-33's subject) --------------------------------------


def _dictionary(**extra: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "vtec_lag_1h": {
            "dictionary_row": "vtec_lag",
            "lag_hours": 1,
            "source_column": "vtec_tecu",
            "normalization": "train_only_standardize",
        },
        "vtec_lag_3h": {
            "dictionary_row": "vtec_lag",
            "lag_hours": 3,
            "source_column": "vtec_tecu",
            "normalization": "train_only_standardize",
        },
        "vtec_seq_24": {
            "dictionary_row": "vtec_seq_24",
            "sequence_steps": SYNTH_WINDOW_HOURS,
            "source_column": "vtec_tecu",
            "normalization": "train_only_standardize",
        },
        "utc_hour_sin": {"dictionary_row": "utc_hour_sin", "normalization": "none"},
        "utc_hour_cos": {"dictionary_row": "utc_hour_cos", "normalization": "none"},
        "kp_safe": {
            "dictionary_row": "kp_safe",
            "source_series": "kp",
            "normalization": "none",
        },
    }
    base.update(extra)
    return base


def _producers() -> dict[str, list[str]]:
    return {
        "vtec_lag": ["phase1_hourly_target"],
        "vtec_seq_24": ["phase1_hourly_target"],
        "utc_hour_sin": ["record_timestamp"],
        "utc_hour_cos": ["record_timestamp"],
        "kp_safe": ["gfz_kp_provisional"],
    }


def test_dictionary_tbd_is_a_preflight_stop() -> None:
    with pytest.raises(PreflightError):
        load_feature_dictionary(synthetic_snapshot(features={"feature_dictionary": TBD_SENTINEL}))


def test_field_outside_the_dictionary_raises() -> None:
    snapshot = synthetic_snapshot(
        features={
            "feature_dictionary": _dictionary(
                cloud_cover={"dictionary_row": "cloud", "normalization": "none"}
            )
        }
    )
    with pytest.raises(LeakageError) as excinfo:
        load_feature_dictionary(snapshot)
    assert "outside the TE 6.2 dictionary" in str(excinfo.value)


def test_iri_field_injected_into_the_dictionary_raises() -> None:
    """WS-10's data-flow limb: the denial mechanism rejects a deliberately injected iri_*."""
    snapshot = synthetic_snapshot(
        features={
            "feature_dictionary": _dictionary(
                iri_vtec={
                    "dictionary_row": "kp_safe",
                    "source_series": "iri",
                    "normalization": "none",
                }
            )
        }
    )
    with pytest.raises(LeakageError) as excinfo:
        load_feature_dictionary(snapshot)
    assert "NFR-IRI-01" in str(excinfo.value)


def test_raw_longitude_column_raises() -> None:
    for name in ("station_lon", "glon", "longitude"):
        snapshot = synthetic_snapshot(
            features={
                "feature_dictionary": _dictionary(
                    **{name: {"dictionary_row": "station_lat", "normalization": "none"}}
                )
            }
        )
        with pytest.raises(LeakageError) as excinfo:
            load_feature_dictionary(snapshot)
        assert "lst_sin and lst_cos" in str(excinfo.value)


def test_lag_name_must_match_its_declared_lag() -> None:
    bad = _dictionary()
    bad["vtec_lag_3h"]["lag_hours"] = 2
    with pytest.raises(LeakageError):
        load_feature_dictionary(synthetic_snapshot(features={"feature_dictionary": bad}))


def test_normalization_must_be_declared() -> None:
    bad = _dictionary()
    del bad["kp_safe"]["normalization"]
    with pytest.raises(LeakageError):
        load_feature_dictionary(synthetic_snapshot(features={"feature_dictionary": bad}))


# --- the permitted-producer list (SD-F-01): fail closed, naming the rows ------------------


def test_permitted_producers_tbd_names_every_row_lacking_an_entry() -> None:
    snapshot = synthetic_snapshot(features={"permitted_producers": TBD_SENTINEL})
    with pytest.raises(LeakageError) as excinfo:
        load_permitted_producers(snapshot, dictionary_rows=["vtec_lag", "kp_safe"])
    message = str(excinfo.value)
    assert "kp_safe" in message and "vtec_lag" in message
    assert "No feature matrix is produced" in message


def test_permitted_producers_incomplete_names_only_the_missing_rows() -> None:
    snapshot = synthetic_snapshot(features={"permitted_producers": {"vtec_lag": ["target"]}})
    with pytest.raises(LeakageError) as excinfo:
        load_permitted_producers(snapshot, dictionary_rows=["vtec_lag", "kp_safe", "doy_sin"])
    message = str(excinfo.value)
    assert "['doy_sin', 'kp_safe']" in message and "'vtec_lag'" not in message.split("row(s)")[1]


#: The eleven dictionary rows whose PRODUCING ARTIFACT the implemented contract itself
#: fixes, and the producer each takes — transcribed by the owner's ruling of 2026-09-10
#: (D-35, adopted 2026-09-10). Enumerated here literally, never imported from the
#: config it checks (that would be circular).
_CONTRACT_FIXED_PRODUCERS: dict[str, str] = {
    "vtec_lag": "phase1_hourly_target",
    "vtec_seq_24": "phase1_hourly_target",
    "target_support": "phase1_hourly_target",
    "utc_hour_sin": "record_timestamp",
    "utc_hour_cos": "record_timestamp",
    "doy_sin": "record_timestamp",
    "doy_cos": "record_timestamp",
    "lst_sin": "station_registry",
    "lst_cos": "station_registry",
    "station_onehot": "station_registry",
    "station_lat": "station_registry",
}
#: The seven driver-class rows D-35 limb 3 left unassigned until the driver release
#: existed, CLOSED 2026-09-21 under D-63 with the producer each takes — enumerated here
#: literally (never imported from the config it checks) so that config, the code
#: constant `spaceweather.DRIVER_PRODUCERS` and this transcription are three independent
#: statements that must agree.
_DRIVER_PRODUCERS: dict[str, str] = {
    "kp_safe": "gfz_kp_ap_nowcast_2022",
    "ap_safe": "gfz_kp_ap_nowcast_2022",
    "hp60_safe": "gfz_hp60ap60_v2_2022",
    "ap60_safe": "gfz_hp60ap60_v2_2022",
    "f107_safe": "nrcan_f107_observed_daily_median_2022",
    "f107_81_trailing": "nrcan_f107_observed_daily_median_2022",
    "dst": "kyoto_wdc_dst_2022",
}
_DRIVER_ROWS: tuple[str, ...] = tuple(_DRIVER_PRODUCERS)


def test_permitted_producers_real_features_yaml_carries_exactly_the_contract_fixed_rows() -> None:
    """D-35 (2026-09-10) fixed eleven rows; D-63 (2026-09-21) closed the seven driver rows.
    The repository's own block now carries exactly those eighteen rows with their
    decision-fixed producers, and NOTHING else.

    Asserted by set-difference in both directions, so an added row (a producer assigned
    without a decision) and a dropped row both fail. The producer strings are compared to
    the code constants they transcribe, so config and code cannot drift apart.
    """
    pytest.importorskip("yaml")
    producers = load_permitted_producers(REPO_ROOT / "configs")
    expected_all = {**_CONTRACT_FIXED_PRODUCERS, **_DRIVER_PRODUCERS}
    missing = sorted(set(expected_all) - set(producers))
    extra = sorted(set(producers) - set(expected_all))
    assert missing == [] and extra == [], f"missing {missing}, extra {extra}"
    for row, expected in expected_all.items():
        assert tuple(producers[row]) == (expected,), row
    # the transcription agrees with the code constants it came from
    assert build.STATION_REGISTRY_PRODUCER == "station_registry"
    assert build.TIMESTAMP_PRODUCER == "record_timestamp"
    assert dict(spaceweather.DRIVER_PRODUCERS) == _DRIVER_PRODUCERS


def test_permitted_producers_driver_rows_admit_only_their_decision_fixed_producer() -> None:
    """D-63 admits PROVENANCE, never a role: each driver row resolves to exactly one
    producer, a frame stamped with any other producing_artifact is refused by
    `build_features`' (row, producer) check, and `dst` stays diagnostic-only (TC-11)."""
    pytest.importorskip("yaml")
    producers = load_permitted_producers(REPO_ROOT / "configs", dictionary_rows=list(_DRIVER_ROWS))
    for row in _DRIVER_ROWS:
        assert producers[row] == (_DRIVER_PRODUCERS[row],), row
        assert "gfz_kp_ap_definitive_2022" not in producers[row]  # D-39: nowcast, not definitive
        assert "gfz_hp60ap60_v3_2022" not in producers[row]  # D-40: V3.0 is a comparator only
    assert "dst" in spaceweather.DIAGNOSTIC_ONLY_SERIES
    # the two F10.7 rows and the two Kp/ap rows share one released product each
    assert producers["f107_safe"] == producers["f107_81_trailing"]
    assert producers["kp_safe"] == producers["ap_safe"]
    assert producers["hp60_safe"] == producers["ap60_safe"]


def test_permitted_producers_admit_no_removed_or_iri_or_longitude_row() -> None:
    """The leakage-safe policy's absolute exclusions cannot enter THROUGH the block: a
    REMOVED row (`ssn`), an `iri_*` row and a raw-longitude row are all outside the TE 6.2
    dictionary, so the loader refuses them by name rather than admitting a producer."""
    for forbidden in ("ssn", "iri_vtec", "glon", "longitude"):
        snapshot = synthetic_snapshot(
            features={"permitted_producers": {forbidden: ["some_artifact"]}}
        )
        with pytest.raises(LeakageError):
            load_permitted_producers(snapshot)
    assert "ssn" in build.REMOVED_ROWS
    assert not set(_CONTRACT_FIXED_PRODUCERS) & set(build.REMOVED_ROWS)


def test_permitted_producers_row_outside_dictionary_refused() -> None:
    snapshot = synthetic_snapshot(features={"permitted_producers": {"cloud": ["x"]}})
    with pytest.raises(LeakageError):
        load_permitted_producers(snapshot)


def test_build_features_refuses_at_the_producer_list_before_producing_anything() -> None:
    snapshot = synthetic_snapshot(
        features={"feature_dictionary": _dictionary(), "permitted_producers": TBD_SENTINEL}
    )
    start, end = training_range(partition_by_id(PARTITIONS, "F1"))
    with pytest.raises(LeakageError) as excinfo:
        build_features(
            [],
            drivers={},
            registry={},
            matrix=(),
            spec=FrameSpec("F1", "train", start, end),
            partitions=PARTITIONS,
            snapshot=snapshot,
        )
    assert "permitted_producers" in str(excinfo.value)


# --- R-78: support fields, four rules, separate failures -----------------------------------


def _support(**fields: Any) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "dictionary_row": "target_support",
        "source_column": "valid_observation_count",
        "normalization": "none",
        "lag_hours": 1,
    }
    entry.update(fields)
    return entry


def _features_with_support(support_entry: dict[str, Any], *, freeze: Any = None) -> dict[str, Any]:
    features: dict[str, Any] = {
        "feature_dictionary": _dictionary(support_count=support_entry),
        "permitted_producers": {**_producers(), "target_support": ["phase1_hourly_target"]},
        "carry_forward_bound_hours": 3,
    }
    if freeze is not None:
        features["feature_set_freeze_utc"] = freeze
    return features


def _happy_inputs(snapshot):
    """Synthetic target + driver inputs for F1's training range over one station."""
    f1 = partition_by_id(PARTITIONS, "F1")
    start, end = training_range(f1)
    hours = int((end - start).total_seconds() // 3600)
    target = RecordFrame(
        {
            "interval_start_utc": (start + dt.timedelta(hours=h)).isoformat(),
            "station_id": "S1",
            "vtec_tecu": 10.0 + (h % 17) * 0.5,
            "valid_observation_count": 5 + (h % 3),
            "phase_id": "phase1",
            "source_id": "synthetic",
            "target_definition_id": "synthetic-gridded",
        }
        for h in range(hours)
    )
    target.attrs["producing_artifact"] = "phase1_hourly_target"
    kp = RecordFrame(
        {"interval_start_utc": (start + dt.timedelta(hours=h)).isoformat(), "value": float(h % 9)}
        for h in range(hours)
    )
    kp.attrs["producing_artifact"] = "gfz_kp_provisional"
    matrix = (
        AvailabilityRow(
            feature="kp_safe",
            observation_timestamp="x",
            publication_timestamp="y",
            release_status="provisional",
            safe_lag_hours=3.0,
            actual_lag_hours=3.5,
        ),
    )
    return target, {"kp": kp}, matrix, FrameSpec("F1", "train", start, end)


def _run_build(features: dict[str, Any], **kwargs: Any):
    snapshot = synthetic_snapshot(features=features)
    target, drivers, matrix, spec = _happy_inputs(snapshot)
    return build_features(
        target,
        drivers=drivers,
        registry={},
        matrix=matrix,
        spec=kwargs.pop("spec", spec),
        partitions=PARTITIONS,
        snapshot=snapshot,
        parity_tolerance=kwargs.pop("parity_tolerance", 0.0),
        **kwargs,
    )


def test_support_field_without_approval_is_not_in_the_feature_set_at_all() -> None:
    bundle = _run_build(_features_with_support(_support()))
    assert "support_count" not in bundle.provenance


def test_target_hour_quality_field_is_permanently_forbidden_even_when_approved() -> None:
    entry = _support(
        support_kind="target_hour_quality",
        approval={"approval_id": "G-04-001", "recorded_utc": "2001-01-01T00:00:00Z"},
    )
    with pytest.raises(LeakageError) as excinfo:
        _run_build(_features_with_support(entry, freeze="2001-02-01T00:00:00Z"))
    assert "permanently forbidden" in str(excinfo.value)


def test_approval_recorded_after_the_freeze_fails_on_ordering() -> None:
    entry = _support(approval={"approval_id": "G-04-001", "recorded_utc": "2001-03-01T00:00:00Z"})
    with pytest.raises(LeakageError) as excinfo:
        _run_build(_features_with_support(entry, freeze="2001-02-01T00:00:00Z"))
    assert "PRECEDE" in str(excinfo.value)


def test_approval_without_id_or_timestamp_fails_separately() -> None:
    with pytest.raises(LeakageError) as excinfo:
        _run_build(
            _features_with_support(
                _support(approval={"recorded_utc": "2001-01-01T00:00:00Z"}),
                freeze="2001-02-01T00:00:00Z",
            )
        )
    assert "approval_id" in str(excinfo.value)
    with pytest.raises(LeakageError) as excinfo2:
        _run_build(
            _features_with_support(
                _support(approval={"approval_id": "G-04-001"}), freeze="2001-02-01T00:00:00Z"
            )
        )
    assert "recorded_utc" in str(excinfo2.value)


def test_support_read_at_hour_t_fails() -> None:
    entry = _support(
        lag_hours=0,
        approval={"approval_id": "G-04-001", "recorded_utc": "2001-01-01T00:00:00Z"},
    )
    with pytest.raises(LeakageError) as excinfo:
        _run_build(_features_with_support(entry, freeze="2001-02-01T00:00:00Z"))
    assert "hours <= t" in str(excinfo.value)


def test_approved_lagged_support_field_enters_with_its_provenance() -> None:
    entry = _support(approval={"approval_id": "G-04-001", "recorded_utc": "2001-01-01T00:00:00Z"})
    bundle = _run_build(_features_with_support(entry, freeze="2001-02-01T00:00:00Z"))
    assert bundle.provenance["support_count"]["dictionary_row"] == "target_support"


# --- the window: frozen, grid-free, one definition, parity --------------------------------


def test_window_length_tbd_or_disagreeing_with_the_dictionary_fails() -> None:
    with pytest.raises(LeakageError):
        read_window_length(
            synthetic_snapshot(experiment={"window_length_hours": TBD_SENTINEL}),
            sequence_steps=SYNTH_WINDOW_HOURS,
        )
    with pytest.raises(LeakageError) as excinfo:
        read_window_length(synthetic_snapshot(), sequence_steps=SYNTH_WINDOW_HOURS + 1)
    assert "disagrees" in str(excinfo.value)


def test_window_length_placed_in_a_grid_fails() -> None:
    grids = {"M-06": {"units": [16, 32], "window_length_hours": [24, 48]}}
    with pytest.raises(LeakageError) as excinfo:
        assert_window_length_grid_free({"grids": grids})
    assert "grid" in str(excinfo.value)
    with pytest.raises(LeakageError):
        read_window_length(
            synthetic_snapshot(experiment={"grids": grids}), sequence_steps=SYNTH_WINDOW_HOURS
        )
    assert assert_window_length_grid_free({"grids": {"M-04": {"alpha": [0.1, 1.0]}}}) is None


def test_one_definition_emits_both_representations_and_counts_exclusions() -> None:
    start = _ts(3, 1)
    records = [
        {
            "interval_start_utc": (start + dt.timedelta(hours=h)).isoformat(),
            "station_id": "S1",
            "v": float(h),
        }
        for h in range(30)
        if h != 20  # one missing epoch -> incomplete windows for rows 21..(20+W)
    ]
    result = build_windows(
        records,
        window_hours=4,
        sequence_fields={"v_seq": "v"},
        lag_fields={"v_lag_2h": ("v", 2)},
        scored_start=start,
        scored_end=start + dt.timedelta(hours=30),
    )
    assert result.excluded_before_scored_start == 4  # rows 0..3 reach before the start
    assert result.excluded_incomplete_windows == 4  # rows 21..24 need epoch 20
    row = result.records[0]  # epoch 4: window is epochs 0..3
    assert row["v_seq_t-1"] == 3.0 and row["v_seq_t-4"] == 0.0 and row["v_lag_2h"] == 2.0
    assert_window_parity(
        result.records,
        result.tensor,
        sequence_columns=result.sequence_columns,
        tensor_features=result.tensor_features,
        tolerance=0.0,
    )


def test_lag_beyond_the_window_cannot_come_from_one_definition() -> None:
    with pytest.raises(LeakageError):
        build_windows(
            [],
            window_hours=4,
            sequence_fields={"v_seq": "v"},
            lag_fields={"v_lag_5h": ("v", 5)},
            scored_start=_ts(3, 1),
            scored_end=_ts(3, 2),
        )


def test_parity_value_limb_stops_naming_the_te_15_2_field_when_tolerance_is_unset() -> None:
    records = [{"v_seq_t-1": 1.0, "v_seq_t-2": 0.0}]
    tensor = [[[0.0], [1.0]]]
    with pytest.raises(IntegrityError) as excinfo:
        assert_window_parity(
            records,
            tensor,
            sequence_columns={"v_seq": ("v_seq_t-2", "v_seq_t-1")},
            tensor_features=("v_seq",),
            tolerance=None,
        )
    assert "permitted_floating_point_tolerances" in str(excinfo.value)


def test_parity_shape_then_value_failures_are_distinguished() -> None:
    records = [{"v_seq_t-1": 1.0, "v_seq_t-2": 0.0}]
    with pytest.raises(LeakageError) as shape:
        assert_window_parity(
            records,
            [[[0.0], [1.0]], [[0.0], [1.0]]],
            sequence_columns={"v_seq": ("v_seq_t-2", "v_seq_t-1")},
            tensor_features=("v_seq",),
            tolerance=0.0,
        )
    assert "shape" in str(shape.value)
    with pytest.raises(LeakageError) as value:
        assert_window_parity(
            records,
            [[[0.0], [5.0]]],
            sequence_columns={"v_seq": ("v_seq_t-2", "v_seq_t-1")},
            tensor_features=("v_seq",),
            tolerance=0.0,
        )
    assert "value" in str(value.value)


# --- build_features end to end over synthetic records --------------------------------------


def _base_features() -> dict[str, Any]:
    return {
        "feature_dictionary": _dictionary(),
        "permitted_producers": _producers(),
        "carry_forward_bound_hours": 3,
    }


def test_build_features_happy_path_stamps_provenance_equal_to_columns() -> None:
    bundle = _run_build(_base_features())
    from src.features._frames import columns_of

    keys = ("interval_start_utc", "station_id")
    feature_columns = [c for c in columns_of(bundle.matrix) if c not in keys]
    assert set(feature_columns) == set(bundle.provenance)
    assert bundle.transform_id is None
    assert bundle.identity == {
        "phase_id": "phase1",
        "source_id": "synthetic",
        "target_definition_id": "synthetic-gridded",
    }
    assert bundle.excluded_counts["excluded_before_scored_start"] == SYNTH_WINDOW_HOURS
    assert bundle.provenance["kp_safe"] == {
        "dictionary_row": "kp_safe",
        "dictionary_field": "kp_safe",
        "producing_artifact": "gfz_kp_provisional",
    }
    assert len(bundle.sequence_columns["vtec_seq_24"]) == SYNTH_WINDOW_HOURS


def test_three_call_sequence_fits_then_transforms_both_representations() -> None:
    features = _base_features()
    raw = _run_build(features)
    f1 = partition_by_id(PARTITIONS, "F1")
    transform = fit_transforms(raw, partition=f1)
    train = _run_build(features, transform=transform)
    assert train.transform_id == "T-F1"
    from src.features._frames import column_values, tensor_as_nested

    values = column_values(train.matrix, "vtec_lag_1h")
    assert abs(sum(values) / len(values)) < 1e-9  # standardised on its own training range
    nested = tensor_as_nested(train.tensor)
    idx = train.sequence_columns["vtec_seq_24"].index("vtec_seq_24_t-1")
    assert abs(nested[0][idx][0] - column_values(train.matrix, "vtec_seq_24_t-1")[0]) < 1e-9


def test_unpermitted_producer_for_a_row_is_refused() -> None:
    features = _base_features()
    features["permitted_producers"]["kp_safe"] = ["some_other_artifact"]
    with pytest.raises(LeakageError) as excinfo:
        _run_build(features)
    assert "not a permitted producer" in str(excinfo.value)


def test_absent_provenance_on_an_input_fails() -> None:
    snapshot = synthetic_snapshot(features=_base_features())
    target, drivers, matrix, spec = _happy_inputs(snapshot)
    drivers["kp"].attrs.pop("producing_artifact")
    with pytest.raises(LeakageError) as excinfo:
        build_features(
            target,
            drivers=drivers,
            registry={},
            matrix=matrix,
            spec=spec,
            partitions=PARTITIONS,
            snapshot=snapshot,
            parity_tolerance=0.0,
        )
    assert "ABSENT provenance FAILS" in str(excinfo.value)


def test_driver_without_an_availability_row_is_refused() -> None:
    snapshot = synthetic_snapshot(features=_base_features())
    target, drivers, _, spec = _happy_inputs(snapshot)
    with pytest.raises(LeakageError) as excinfo:
        build_features(
            target,
            drivers=drivers,
            registry={},
            matrix=(),
            spec=spec,
            partitions=PARTITIONS,
            snapshot=snapshot,
            parity_tolerance=0.0,
        )
    assert "availability-matrix row" in str(excinfo.value)


def test_lagged_safe_series_passes_through_build_features_with_no_second_lag() -> None:
    """D-44 end to end: a `kp` series produced by `select_lagged_series` (lag applied ONCE,
    3 h after each interval's completion) with its provider observations attached is
    accepted by `build_features`; the matrix row's `kp_safe` at origin T is the value of
    the interval that completed at T − 3 h (no second shift), traceable to the source
    interval; the same rows with a `selection` lag that disagrees with the availability
    matrix are refused; a lagged series WITHOUT the `selection` attribute is refused by
    the raw own-interval check (never silently relabelled); a raw own-interval series is
    still accepted on the raw path."""
    from src.external.spaceweather import (
        SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG,
        select_lagged_series,
    )
    from src.features._frames import records_of

    snapshot = synthetic_snapshot(features=_base_features())
    target, drivers, matrix, spec = _happy_inputs(snapshot)
    start = spec.scored_start
    hours = len(list(records_of(drivers["kp"])))
    observations = [
        {
            "value": float(100 + k),
            "interval_start": start + dt.timedelta(hours=3 * k),
            "interval_end": start + dt.timedelta(hours=3 * k + 3),
        }
        for k in range(hours // 3 + 1)
    ]
    epochs = [start + dt.timedelta(hours=h) for h in range(hours)]
    lagged_rows = select_lagged_series(observations, epochs=epochs, safe_lag_hours=3)
    lagged = RecordFrame(lagged_rows)
    lagged.attrs["producing_artifact"] = "gfz_kp_provisional"
    lagged.attrs["observations"] = observations
    lagged.attrs["selection"] = {
        "rule": SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG,
        "safe_lag_hours": 3,
    }

    def build(frame):
        return build_features(
            target,
            drivers={"kp": frame},
            registry={},
            matrix=matrix,
            spec=spec,
            partitions=PARTITIONS,
            snapshot=snapshot,
            parity_tolerance=0.0,
        )

    bundle = build(lagged)
    rows = {r["interval_start_utc"]: r for r in records_of(bundle.matrix)}
    origin = start + dt.timedelta(hours=33)  # day 2, 09:00
    assert rows[origin.isoformat()]["kp_safe"] == 100 + 9  # interval [03,06) of day 2, ended 06:00
    origin = start + dt.timedelta(hours=32)  # day 2, 08:00 — [03,06) not yet 3 h old
    assert rows[origin.isoformat()]["kp_safe"] == 100 + 8
    # selection lag disagreeing with the matrix's declared safe lag: refused (no double lag)
    lagged.attrs["selection"] = {
        "rule": SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG,
        "safe_lag_hours": 6,
    }
    with pytest.raises(AlignmentError, match="applied once"):
        build(lagged)
    lagged.attrs["selection"] = {"rule": "some_other_rule", "safe_lag_hours": 3}
    with pytest.raises(AlignmentError, match="not recognised"):
        build(lagged)
    # lagged rows presented as a RAW series: the own-interval check refuses them
    del lagged.attrs["selection"]
    with pytest.raises(AlignmentError):
        build(lagged)
    # a raw own-interval series still passes the raw path
    raw = RecordFrame(
        {
            "interval_start_utc": (start + dt.timedelta(hours=h)).isoformat(),
            "value": float(100 + h // 3),
        }
        for h in range(hours)
    )
    raw.attrs["producing_artifact"] = "gfz_kp_provisional"
    raw.attrs["observations"] = observations
    build(raw)


def test_driver_repeated_outside_its_interval_raises_alignment_error() -> None:
    """R-76a's enforcement raise through build_features (TA-36's subject)."""
    snapshot = synthetic_snapshot(features=_base_features())
    target, drivers, matrix, spec = _happy_inputs(snapshot)
    start = spec.scored_start
    drivers["kp"].attrs["observations"] = [
        {"value": 0.0, "interval_start": start, "interval_end": start + dt.timedelta(hours=3)},
    ]
    with pytest.raises(AlignmentError):
        build_features(
            target,
            drivers=drivers,
            registry={},
            matrix=matrix,
            spec=spec,
            partitions=PARTITIONS,
            snapshot=snapshot,
            parity_tolerance=0.0,
        )


def test_station_fields_are_blocked_by_an_unresolved_registry() -> None:
    features = _base_features()
    features["feature_dictionary"]["station_lat"] = {
        "dictionary_row": "station_lat",
        "normalization": "none",
    }
    features["permitted_producers"]["station_lat"] = ["station_registry"]
    with pytest.raises(RegistryError):
        _run_build(features)


def test_carry_forward_bound_tbd_refuses() -> None:
    features = _base_features()
    features["carry_forward_bound_hours"] = TBD_SENTINEL
    with pytest.raises(LeakageError) as excinfo:
        _run_build(features)
    assert "carry_forward_bound_hours" in str(excinfo.value)


def test_score_spec_exceeding_the_validation_month_raises() -> None:
    f1 = partition_by_id(PARTITIONS, "F1")
    spec = FrameSpec("F1", "score", _ts(4, 1), _ts(5, 2))
    with pytest.raises(LeakageError):
        _run_build(_base_features(), spec=spec)
    assert f1.validation_month == dt.date(SYNTH_YEAR, 4, 1)


def test_comparison_mask_is_the_intersection_with_three_stamps() -> None:
    identity = {"phase_id": "p", "source_id": "s", "target_definition_id": "t"}
    rows_a = [("S1", _ts(4, 2, h)) for h in range(5)]
    rows_b = [("S1", _ts(4, 2, h)) for h in range(2, 7)]
    mask = build_comparison_mask(
        {"M-01": rows_a, "M-06": rows_b}, comparison_set_id="cs1", identity=identity
    )
    assert mask.kept_count == 3 and mask.members == ("M-01", "M-06")
    from src.data.config import FairnessError

    with pytest.raises(FairnessError):
        build_comparison_mask({"M-01": rows_a}, comparison_set_id="cs1", identity=identity)
    with pytest.raises(FairnessError):
        build_comparison_mask(
            {"M-01": rows_a, "M-06": rows_b}, comparison_set_id="cs1", identity={"phase_id": "p"}
        )


def test_no_iri_or_gim_import_under_src_features() -> None:
    """The module-graph limb is external-products' scan; this is the local restatement."""
    pattern = re.compile(
        r"^\s*(?:from src\.external\.(?:iri|gim)\b|import src\.external\.(?:iri|gim)\b"
        r"|from src\.external import [^\n]*\b(?:iri|gim)\b)",
        re.MULTILINE,
    )
    for module in sorted((REPO_ROOT / "src" / "features").rglob("*.py")):
        assert not pattern.search(module.read_text(encoding="utf-8")), module
