"""Driver series: availability lags, alignment, carry-forward, grades, provenance (E-2).

Purpose
-------
The driver half of unit `external-products` (W-5, W-8; R-57, R-57a, R-58, R-61, R-62,
R-63; SD-E-06, SD-E-07). Four series are governed here by contract -- Kp/ap3 and
Hp60/ap60 from GFZ, hourly Dst from Kyoto WDC, observed (not 1-AU-adjusted) F10.7 from
Canada's Solar Radio Monitoring Program -- and this module is DELIBERATELY OUTSIDE the
IRI/GIM import restriction: drivers ARE model inputs, subject to the availability lags
(R-56's constraint). Everything here is stdlib-only and value-parameterised: no
scientific constant lives in this file (TC-03e) -- the carry-forward bound, the window
length and the lags are frozen in `configs/` or in decision records and are passed in
by the caller, never chosen here.

What this module enforces, and with which exception:

* alignment of a PRESENT value onto the hourly grid -> `AlignmentError` (the existing
  shared-base class that owns this unit's two alignment conditions);
* the trailing mean's future-independence, missing-value carry-forward with the
  conservation invariant, time-indexed-only shape, single release grade, grade
  eligibility, provenance-field completeness/consistency, the GFZ near-real-time
  cross-assertion, and the SD-E-07 byte-identical-or-divergent re-run contract ->
  the `IntegrityError` BASE, because **`DriverError` is deliberately NOT declared**
  (Q1 = A, receipted 2026-09-05): its scope is contested upstream (carried Finding 9 --
  `domain-entities.md` section 9 specifies both readings at once), so raising the base
  with resource + expectation misclassifies nothing while the reconciliation is owed;
* the F10.7 daily-cadence composition stop -> `FeatureAvailabilityError` (R-57a,
  D-21/G-04: the composition is a Student freeze item and this module NEVER adopts a
  reading of it).

SD-E-07's re-run contract and the SD-E-03 producing-half provenance stamp live here
rather than in `iri.py`/`gim.py` because they are shared by all three product families
and this is the one `src/external` module every consumer may import -- placing a generic
integrity helper behind the two-path IRI/GIM allowlist would force the allowlist open
for a check that has nothing to do with IRI values.

Boundary split -- WHERE each refusal is invoked
-----------------------------------------------
A guard module alone fails open on a forgotten call, and inline copies drift
(`nfr-design:c58`; the R-105-vs-R-92 exception mismatch was that drift realised). Each
refusal below therefore has exactly ONE home and a NAMED call site, so nothing is
checked twice and nothing is checked nowhere.

**Driver-PRODUCING path** -- `scripts/04_build_external_products.py`, which constructs a
driver series from provider material. These guards are the producer's obligation and
have NO consumer-side equivalent:

* `assert_time_indexed_shape` -- refuse a row shape carrying a station/cell key AT
  CONSTRUCTION (TC-12, FR-P1-04-4). The consuming side cannot recover this: by the time
  a series reaches `build_features` it has already been flattened to `{epoch: value}`.
* `assert_grade_eligible` -- refuse a grade/use pair at the point of use (R-62
  restriction 3; D-11, D-13). NOTE: `src/evaluation/diagnostics.py` declares a DIFFERENT
  function of the same name for the reporting boundary; the two are not interchangeable
  and neither call site satisfies the other's rule.
* `assert_single_grade` -- see the D-10.1 split below.
* `refuse_divergent_rerun` -- SD-E-07's byte-identical-or-divergent re-run contract.
  `scripts/04_build_external_products.py`'s docstring describes an equivalent INLINE hash
  comparison; that script owns reconciling the two into one home, exactly as D-10.1 is
  reconciled below.

The driver-producing path does NOT EXIST YET. These calls are therefore a NAMED
OBLIGATION on the driver-producing Bolt, not dead code and not an optional extra: the
Bolt that writes `04_build_external_products.py`'s driver half wires each of them at the
construction site named above. Until it does, a driver series constructed outside this
project's code is unchecked on the producing limbs.

**Driver-CONSUMING path** -- `src/features/build.py::build_features` and
`src/features/transforms.py::carry_forward`, WIRED and live today:

* duplicate epoch -> `src/features/build.py::_hourly_series` raises `IntegrityError`
  naming the epoch. This is the ingest half of TC-12's one-value-per-epoch rule; it lives
  in the consumer because the consumer is what builds the `{epoch: value}` index.
* `assert_identical_across_cells` -> called by `build_features` per driver field AFTER
  the driver-to-station join, on the assembled rows (TC-12's joined-grid limb; R-63's
  negative control).
* `assert_carry_forward_conservation` -> called by `transforms.carry_forward` immediately
  after `apply_carry_forward`, on the series it is about to return (R-58 limb 3 -- the
  limb that carries the rule; it catches fills the AST token scan cannot reach).

**D-10.1's single-grade rule has TWO homes, and the split is declared here.** One binding
rule, two implementations, two exception classes -- so which one runs where is stated
rather than left to drift:

* PRODUCTION side (constructing a series from provider material): this module's
  `assert_single_grade`, raising `IntegrityError`. Mixed Kyoto Dst release grades FAIL AT
  CONSTRUCTION, never downstream. Part of the deferred driver-producing obligation above.
* CONSUMPTION side (reading supplied driver rows into the availability matrix):
  `src/features/availability.py::build_availability_matrix`'s inline grade check, raising
  `FeatureAvailabilityError`. That is the one that actually runs today, via
  `scripts/05_build_features_and_splits.py`.

The two are NOT redundant and must not be collapsed: the production check governs bytes
this project writes, the consumption check governs rows this project is handed. They
carry different exception classes on purpose -- an integrity failure in a product we
produced is not the same event as an availability-contract failure in a product we
consumed -- and a caller must not catch one expecting the other.

Inputs
------
Plain mappings and sequences supplied by `scripts/04_build_external_products.py` (the
orchestrator): per-epoch observation mappings, per-day daily medians, the parsed
`features` config mapping (read via `load_configs` upstream, never re-read here), and
manifest payload dictionaries. This module reads no file except in
`refuse_divergent_rerun`, which re-hashes one named product file.

Re-run behaviour
----------------
Every function is a pure check or a pure derivation over its arguments; nothing here
writes except `write_driver_manifest`, which routes every value through acquisition's
`guard_egress` and refuses inconsistent provenance before a byte is written. A re-run
over identical inputs produces identical outputs; a re-run over CHANGED external
product bytes is refused by `refuse_divergent_rerun`, which records BOTH identities and
BOTH hashes rather than overwriting (SD-E-07, adopting acquisition's SEC-A-02 contract
unchanged).
"""

from __future__ import annotations

import datetime as dt
import json
import math
from collections.abc import Callable, Collection, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.data.acquisition import guard_egress
from src.data.config import (
    TBD_SENTINEL,
    AlignmentError,
    FeatureAvailabilityError,
    IntegrityError,
)
from src.data.release import sha256_of_file

__all__ = [
    "DIAGNOSTIC_ONLY_SERIES",
    "DECLARED_STATUS_ONLY_SERIES",
    "DRIVER_PRODUCERS",
    "PROVENANCE_FIELDS",
    "GRADE_USES",
    "trailing_mean",
    "resolve_f107_at_origin",
    "F107Selection",
    "CARRY_FORWARD_COMPOSITION_CLOCK_HOURS",
    "SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG",
    "SELECTION_FIELDS",
    "select_lagged_series",
    "LAG_REFERENCE_INSTANT_INTERVAL_END",
    "assert_lagged_selection",
    "availability_rows_from_selection",
    "daily_medians_from_readings",
    "align_interval_series",
    "assert_alignment",
    "apply_carry_forward",
    "assert_carry_forward_conservation",
    "assert_time_indexed_shape",
    "assert_identical_across_cells",
    "assert_single_grade",
    "assert_grade_eligible",
    "assert_series_provenance",
    "assert_gfz_cross_products",
    "provenance_stamp",
    "write_driver_manifest",
    "refuse_divergent_rerun",
]

#: Dst is diagnostic/hindcast-only, never a confirmatory ML feature (TC-11; D-10.1's
#: series). A classification, not a scientific value: the rule is Vision's, frozen.
DIAGNOSTIC_ONLY_SERIES: frozenset[str] = frozenset({"dst"})

#: The producing-artifact identity of every driver-class TE 6.2 row (D-63, 2026-09-21;
#: closes the seven rows `configs/features.yaml: permitted_producers` deferred under D-35).
#: Each identity names the ONE provider product the governing decision already fixes for
#: that row -- a transcription of D-10.1 (providers), D-39 (Kp/ap: the archived settled
#: nowcast `Kp_now2022.wdc`, DOI 10.5880/Kp.0001), D-40 (Hp60/ap60: Hpo.0002 V2.0, the
#: contemporaneous product; V3.0 is a comparator only), D-21/D-22/D-23/D-25 (F10.7: the
#: NRCan observed flux, project-derived daily median) and D-10.1 (Dst: Kyoto WDC, one
#: release grade). The driver release that `05_build_features_and_splits.py` reads by
#: manifest MUST stamp `producing_artifact` with exactly these identities; `build_features`
#: refuses any other (row, producer) pair (SD-F-01). The config block transcribes this
#: constant and `tests/test_feature_availability.py` asserts the two cannot drift.
DRIVER_PRODUCERS: Mapping[str, str] = {
    "kp_safe": "gfz_kp_ap_nowcast_2022",
    "ap_safe": "gfz_kp_ap_nowcast_2022",
    "hp60_safe": "gfz_hp60ap60_v2_2022",
    "ap60_safe": "gfz_hp60ap60_v2_2022",
    "f107_safe": "nrcan_f107_observed_daily_median_2022",
    "f107_81_trailing": "nrcan_f107_observed_daily_median_2022",
    "dst": "kyoto_wdc_dst_2022",
}

#: Series whose reanalysed-value verifiability is DECLARED-STATUS ONLY (R-63's
#: Constraint): F10.7 (D-22: seven columns, no provenance column; D-21: publication
#: latency not derivable) and Dst (grade inferable from the filename alone; D-10.1's
#: 2022-grade item unchecked per D-11). Never reported as closed.
DECLARED_STATUS_ONLY_SERIES: frozenset[str] = frozenset({"f107", "dst"})

#: The four provenance fields every driver manifest records per series (R-63; the
#: reanalysed-value check's driver-product half).
PROVENANCE_FIELDS: tuple[str, ...] = (
    "release_status",
    "retrieval_date",
    "provider_product_identity",
    "sha256",
)

#: The uses GradeEligibility distinguishes (domain-entities section 3; D-11, D-13).
GRADE_USES: frozenset[str] = frozenset(
    {"fixture_characterisation", "modelling_input", "frozen_tolerance", "g05_regime_count"}
)

#: Release-grade tokens recognisable inside a provider product identity, used by the
#: declared-status consistency check (R-63 control 1: `final` against a
#: `dst_provisional_*` filename FAILS).
_GRADE_TOKENS: tuple[str, ...] = ("real-time", "realtime", "nrt", "provisional", "final")


# --- W-4 / R-57: the trailing mean, future-independent by construction -----------------


def trailing_mean(
    daily_values: Mapping[dt.date, float], *, end_day: dt.date, window_days: int
) -> float:
    """The mean of the `window_days` days ENDING AT `end_day` -- trailing, never centered.

    The window is [end_day - (window_days - 1), end_day] by construction, so no day
    after `end_day` can influence the result -- which is exactly the property R-57
    limb 2 tests: perturbing any day after the safe-lagged day leaves the mean
    unchanged, and a shifted input shifts the output with it. A centered mean uses
    future days and is a defect, not a fallback (project.md Forbidden). `window_days`
    is passed in by the caller from its frozen source (TE 6.2's `f107_81_trailing`
    row), never hardcoded here.

    Raises
    ------
    IntegrityError
        when any day of the window is missing from `daily_values`. TC-20: no value is
        imputed, substituted or reconstructed for the F10.7 outage window until the
        measured gap is recorded and governed -- how a window spanning a gap is treated
        is a governed decision, so this function stops and reports rather than choosing
        (TE 18.3). NaN values are gaps too (D-5: gaps are explicit NaN, never filled).
    """
    if window_days < 1:
        raise IntegrityError("trailing_mean", f"window_days must be >= 1, got {window_days!r}")
    days = [end_day - dt.timedelta(days=offset) for offset in range(window_days)]
    missing = sorted(day.isoformat() for day in days if day not in daily_values)
    nan_days = sorted(
        day.isoformat()
        for day in days
        if day in daily_values and math.isnan(float(daily_values[day]))
    )
    if missing or nan_days:
        raise IntegrityError(
            f"F10.7 trailing window ending {end_day.isoformat()}",
            f"window day(s) missing or NaN (missing: {missing or 'none'}; NaN: "
            f"{nan_days or 'none'}); TC-20 forbids imputing, substituting or "
            f"reconstructing a value for the F10.7 outage window until the measured "
            f"gap is recorded and governed -- stop and report, never fill",
        )
    return sum(float(daily_values[day]) for day in days) / window_days


# --- R-57a: the daily-cadence composition raise -----------------------------------------


#: The composition vocabulary the Student froze at G-04 (D-46, 2026-09-19, reading B):
#: the TE 6.2 "<= 3 h, then exclude" bound is applied in CLOCK HOURS from the expected
#: availability instant of the missing daily update. Any other value is refused.
CARRY_FORWARD_COMPOSITION_CLOCK_HOURS: str = "clock_hours"


@dataclass(frozen=True)
class F107Selection:
    """The F10.7 value resolved at one forecast origin, with its provenance kept apart:
    `source_day` (the UT day whose median is used, or None when excluded), `value`,
    `carried_forward` (True only for a MISSING-update carry, never for ordinary reuse of
    the designated previous-day value), `excluded` (the row's F10.7 limb is unavailable
    under the frozen composition), and `staleness_hours` measured from the expected
    availability instant of the designated value (0.0 for ordinary reuse)."""

    source_day: dt.date | None
    value: float | None
    carried_forward: bool
    excluded: bool
    staleness_hours: float


def resolve_f107_at_origin(
    daily_medians: Mapping[dt.date, float],
    *,
    origin: dt.datetime,
    availability_ts: Callable[[dt.date], dt.datetime],
    features: Mapping[str, Any],
) -> F107Selection:
    """The F10.7 previous-day observed value usable at `origin` (D-10.3, D-25) — the ONE
    owner of F10.7 selection at an origin — and, when the designated value is missing,
    the frozen missing-update composition (D-46, reading B).

    ORDINARY REUSE is not carry-forward: `median(D-1)` is the designated value for every
    origin on day *D* (available at `availability_ts(D-1)` = 00:00 UTC on *D* under
    D-25); using it at 00:00 … 23:00 of *D* is normal use of a daily value within its
    validity period, `carried_forward=False`, staleness 0.

    MISSING UPDATE (the designated `median(D-1)` is absent or not yet available at the
    origin): with `features["carry_forward_composition"] == "clock_hours"` (D-46) the
    last previously available median is carried forward while
    `origin - availability_ts(D-1) <= features["carry_forward_bound_hours"]` (the TE 6.2
    bound, read from configuration, never a literal here) — the boundary is INCLUSIVE,
    so with a 3-hour bound origins 00:00, 01:00, 02:00 and 03:00 of *D* keep the carried
    value and origins from 04:00 are EXCLUDED (`excluded=True`, `value=None`) until a
    valid update becomes available. The clock starts at the EXPECTED availability
    instant of the missing value, never at the carried value's own availability or
    observation instant. Where no median is available at all the row is excluded.

    Raises
    ------
    FeatureAvailabilityError
        while the composition field is absent or `TBD -- freeze gate` (the R-57a stop,
        naming the origin, the last available median's day and the staleness in BOTH
        units), or while `carry_forward_bound_hours` is absent/TBD under a frozen
        composition. TE 18.3: stop and report, never default.
    IntegrityError
        when the composition field carries any value other than `clock_hours` — this
        module applies the frozen vocabulary only, never an interpretation of its own.
    """
    previous_day = origin.date() - dt.timedelta(days=1)
    expected_instant = availability_ts(previous_day)
    if previous_day in daily_medians and expected_instant <= origin:
        value = float(daily_medians[previous_day])
        if not math.isnan(value):
            return F107Selection(previous_day, value, False, False, 0.0)

    available = sorted(
        day
        for day in daily_medians
        if availability_ts(day) <= origin and not math.isnan(float(daily_medians[day]))
    )
    last_available = available[-1] if available else None

    composition = features.get("carry_forward_composition")
    is_tbd = composition is None or (
        isinstance(composition, str) and composition.strip() == TBD_SENTINEL
    )
    if last_available is None:
        staleness_text = "no daily median is available at all at this origin"
    else:
        stale_hours = (origin - availability_ts(last_available)).total_seconds() / 3600.0
        stale_days = (origin.date() - last_available).days
        staleness_text = (
            f"last available median is for {last_available.isoformat()}; staleness "
            f"{stale_hours:.1f} clock hours since its availability timestamp and "
            f"{stale_days} whole daily step(s)"
        )
    if is_tbd:
        raise FeatureAvailabilityError(
            f"F10.7 at forecast origin {origin.isoformat()}",
            f"the previous-day median ({previous_day.isoformat()}) is not available at "
            f"this origin and configs/features.yaml's carry_forward_composition field "
            f"is TBD -- {staleness_text}. D-21 binds the composition of the <= 3 h "
            f"carry-forward bound on this DAILY series and the two readings differ by "
            f"20 of 24 scored rows per affected day; choosing one here would be an "
            f"agent filling a TE 18.2 item by convenience. The freeze is the "
            f"Student's, at G-04 (R-57a): stop and report, never default",
        )
    if composition != CARRY_FORWARD_COMPOSITION_CLOCK_HOURS:
        raise IntegrityError(
            "configs/features.yaml: carry_forward_composition",
            f"the field carries {composition!r}; the frozen vocabulary is "
            f"{CARRY_FORWARD_COMPOSITION_CLOCK_HOURS!r} (D-46, reading B) and this module "
            f"refuses to interpret any other composition -- {staleness_text}",
        )
    bound = features.get("carry_forward_bound_hours")
    if bound is None or (isinstance(bound, str) and bound.strip() == TBD_SENTINEL):
        raise FeatureAvailabilityError(
            "configs/features.yaml: carry_forward_bound_hours",
            "absent or TBD while carry_forward_composition is frozen; the <= 3 h bound is "
            "configuration (TC-09), never a literal here",
        )
    if isinstance(bound, bool) or not isinstance(bound, int | float) or bound < 0:
        raise IntegrityError(
            "configs/features.yaml: carry_forward_bound_hours",
            f"{bound!r} is not a non-negative number",
        )
    staleness = (origin - expected_instant).total_seconds() / 3600.0
    if last_available is not None and staleness <= float(bound):
        return F107Selection(
            last_available, float(daily_medians[last_available]), True, False, staleness
        )
    return F107Selection(None, None, False, True, staleness)


# --- W-5 / R-58: alignment of a PRESENT value onto the hourly grid ----------------------


def align_interval_series(
    observations: Sequence[Mapping[str, Any]],
) -> dict[dt.datetime, float]:
    """Map interval-valued observations onto whole hours WITHIN each observation's own
    interval (D-10.2): a Kp value repeats only inside its own defined 3-hour interval,
    a Dst value occupies only its own hourly averaging interval. Interval widths come
    from the observations themselves -- no lag or width constant lives here.

    Each observation carries `value`, `interval_start` and `interval_end`
    (datetime, end exclusive).

    Raises
    ------
    AlignmentError
        on overlapping intervals (one epoch would carry two values -- which one wins
        would be a silent choice), or an interval not aligned to whole hours.
    """
    aligned: dict[dt.datetime, float] = {}
    for record in observations:
        start = record["interval_start"]
        end = record["interval_end"]
        if start.minute or start.second or start.microsecond:
            raise AlignmentError(
                f"driver observation at {start.isoformat()}",
                "interval_start is not a whole hour; driver intervals align onto the "
                "hourly grid as their contract requires (D-10.2)",
            )
        epoch = start
        while epoch < end:
            if epoch in aligned:
                raise AlignmentError(
                    f"driver epoch {epoch.isoformat()}",
                    "two observations map onto one epoch (overlapping intervals); a "
                    "silent winner would shift a value outside its own interval "
                    "(D-10.2)",
                )
            aligned[epoch] = float(record["value"])
            epoch = epoch + dt.timedelta(hours=1)
    return aligned


def assert_alignment(
    series_id: str,
    aligned: Mapping[dt.datetime, float],
    observations: Sequence[Mapping[str, Any]],
) -> None:
    """R-58 limbs 1 and 2: every aligned value traces to an observation whose OWN
    interval contains that epoch and whose value it equals.

    Catches both named negative controls: a Kp value repeated OUTSIDE its 3-hour
    interval, and a Dst value shifted to a neighbouring hour ("not shifted to a
    neighbouring hour for convenience" -- D-10.2). Distinct from carry-forward
    (FR-P1-04-3), which governs a MISSING value; the two are tested separately so
    neither passes on the other's evidence.

    Raises
    ------
    AlignmentError
        naming the series and the first offending epoch.
    """
    for epoch in sorted(aligned):
        value = float(aligned[epoch])
        covered = any(
            record["interval_start"] <= epoch < record["interval_end"]
            and float(record["value"]) == value
            for record in observations
        )
        if not covered:
            raise AlignmentError(
                f"{series_id} at {epoch.isoformat()}",
                f"value {value!r} is present at an epoch outside the interval of any "
                f"observation carrying it; a present value maps onto the grid only "
                f"within its own defined interval and is never shifted to a "
                f"neighbouring hour for convenience (D-10.2, FR-P1-04-17)",
            )


# --- P-2 / D-44: the ONE lagged-selection owner for interval-valued indices ---------------

#: The selection rule identity a lagged `*_safe` series carries in its frame attributes
#: (`attrs["selection"]["rule"]`): at every epoch T the value of the LATEST source
#: interval whose completion instant (`interval_end`) plus the declared safe lag is at or
#: before T. D-43 fixes the reference instant (interval END, the completion instant —
#: D-10.3's "instant the value could first have been known"); D-44 fixes that this
#: function is the single place the lag is applied, once. `build_features` shifts nothing.
SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG: str = "latest_completed_interval_plus_lag"

#: The per-row fields a lagged selection carries BESIDE the hourly `interval_start_utc` /
#: `value` pair: the selected source interval (its own start AND end, preserved from the
#: provider record, never overwritten) and the assumed availability instant.
SELECTION_FIELDS: tuple[str, ...] = (
    "source_interval_start_utc",
    "source_interval_end_utc",
    "available_at_utc",
)


def _validated_intervals(observations: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Whole-hour, non-overlapping, end-after-start intervals sorted by end; values may be
    missing (None/NaN) — a missing observation keeps its interval identity."""
    norm: list[dict[str, Any]] = []
    for record in observations:
        start, end = record["interval_start"], record["interval_end"]
        if end <= start:
            raise AlignmentError(
                f"driver observation at {start.isoformat()}",
                "interval_end is not after interval_start",
            )
        for stamp in (start, end):
            if stamp.minute or stamp.second or stamp.microsecond:
                raise AlignmentError(
                    f"driver observation at {start.isoformat()}",
                    "interval boundaries are not whole hours (D-10.2)",
                )
        raw = record.get("value")
        value = None if raw is None or math.isnan(float(raw)) else float(raw)
        norm.append({"interval_start": start, "interval_end": end, "value": value})
    norm.sort(key=lambda r: r["interval_end"])
    for earlier, later in zip(norm, norm[1:], strict=False):
        if later["interval_start"] < earlier["interval_end"]:
            raise AlignmentError(
                f"driver observation at {later['interval_start'].isoformat()}",
                "overlaps the preceding interval; one epoch would carry two values (D-10.2)",
            )
    return norm


def select_lagged_series(
    observations: Sequence[Mapping[str, Any]],
    *,
    epochs: Sequence[dt.datetime],
    safe_lag_hours: float,
) -> list[dict[str, Any]]:
    """Build a `*_safe` hourly series from interval-valued observations: for each forecast
    origin `epoch`, the value of the LATEST observation whose `interval_end + safe_lag`
    is at or before the origin (D-43/D-44). The lag is applied HERE and nowhere else.

    Four things are kept distinct in every row: the source observation interval
    (`source_interval_start_utc`, `source_interval_end_utc` — the provider's own
    boundaries, unchanged), the assumed availability instant (`available_at_utc` =
    source end + lag; an assumption for retrospective evaluation, never a publication
    time), the forecast origin (`interval_start_utc`, the hourly epoch the row serves),
    and the selected value (`value`). A row whose selected interval carries a missing
    value keeps that interval's identity with `value` None — the ≤ 3 h carry-forward rule
    (R-57a) then applies downstream on the EPOCH axis; this function never reaches back
    to an older interval, which would be an unrecorded carry-forward. An origin before
    which no interval is eligible yields a row with `value` None and no source fields.

    Raises
    ------
    IntegrityError
        on a negative lag or a non-UTC-aware epoch.
    AlignmentError
        on overlapping or off-hour observation intervals.
    """
    if safe_lag_hours < 0:
        raise IntegrityError(
            "select_lagged_series", f"safe_lag_hours must be >= 0, got {safe_lag_hours!r}"
        )
    lag = dt.timedelta(hours=float(safe_lag_hours))
    intervals = _validated_intervals(observations)
    rows: list[dict[str, Any]] = []
    cursor = -1
    for epoch in sorted(epochs):
        if epoch.tzinfo is None:
            raise IntegrityError("select_lagged_series", f"epoch {epoch!r} is not timezone-aware")
        while cursor + 1 < len(intervals) and intervals[cursor + 1]["interval_end"] + lag <= epoch:
            cursor += 1
        if cursor < 0:
            rows.append(
                {
                    "interval_start_utc": epoch.isoformat(),
                    "value": None,
                    "source_interval_start_utc": None,
                    "source_interval_end_utc": None,
                    "available_at_utc": None,
                }
            )
            continue
        chosen = intervals[cursor]
        rows.append(
            {
                "interval_start_utc": epoch.isoformat(),
                "value": chosen["value"],
                "source_interval_start_utc": chosen["interval_start"].isoformat(),
                "source_interval_end_utc": chosen["interval_end"].isoformat(),
                "available_at_utc": (chosen["interval_end"] + lag).isoformat(),
            }
        )
    return rows


#: D-43's only implemented reference instant: this function ALWAYS measures a selected
#: interval's `available_at` from its END (`source_interval_end_utc` + lag). There is no
#: parameter that changes this -- it is the function's actual behaviour, not a choice.
LAG_REFERENCE_INSTANT_INTERVAL_END: str = "interval_end_utc"


def assert_lagged_selection(
    series_id: str,
    rows: Sequence[Mapping[str, Any]],
    observations: Sequence[Mapping[str, Any]],
    *,
    safe_lag_hours: float,
    expected_reference_instant: str | None = None,
) -> None:
    """The alignment contract for a LAGGED series (amends R-58 limbs 1–2 for `*_safe`
    series, D-44): every present value traces to an observation whose interval equals the
    row's recorded source interval and whose value it equals; `available_at_utc` equals
    that interval's end plus the declared lag and is at or before the origin (no double
    lag, no shortfall); and NO observation with a later end is also eligible at that
    origin (the latest eligible one was selected). A missing row is admissible only when
    no interval is eligible or the eligible one's value is missing.

    `expected_reference_instant`, when given (from the availability matrix row's
    `lag_reference_instant`, D-43), is a config-vs-implementation DRIFT GUARD: this
    function only ever implements `LAG_REFERENCE_INSTANT_INTERVAL_END` (interval END), so
    any other declared value cannot be honoured and is refused here rather than silently
    computed as if it had been — configuration cannot rewrite what the code actually does.

    Raises
    ------
    AlignmentError
        naming the series and the first offending origin, or (drift guard) naming a
        declared reference instant this function does not implement.
    """
    if expected_reference_instant is not None and (
        expected_reference_instant != LAG_REFERENCE_INSTANT_INTERVAL_END
    ):
        raise AlignmentError(
            f"driver series {series_id!r}",
            f"lag_reference_instant {expected_reference_instant!r} is declared, but this "
            f"selector only ever measures available_at from the interval END "
            f"({LAG_REFERENCE_INSTANT_INTERVAL_END!r}, D-43); configuration cannot silently "
            f"change what the producer code actually computes",
        )
    lag = dt.timedelta(hours=float(safe_lag_hours))
    intervals = _validated_intervals(observations)
    by_bounds = {(r["interval_start"], r["interval_end"]): r for r in intervals}
    for row in rows:
        origin = dt.datetime.fromisoformat(str(row["interval_start_utc"]))
        eligible = [r for r in intervals if r["interval_end"] + lag <= origin]
        latest = eligible[-1] if eligible else None
        raw = row.get("value")
        present = raw is not None and not (isinstance(raw, float) and math.isnan(raw))
        if not present:
            if latest is not None and latest["value"] is not None:
                raise AlignmentError(
                    f"{series_id} at {origin.isoformat()}",
                    f"value is missing while the interval ending {latest['interval_end'].isoformat()} "
                    f"is eligible with value {latest['value']!r}; a present source value is never dropped",
                )
            continue
        src = (
            dt.datetime.fromisoformat(str(row["source_interval_start_utc"])),
            dt.datetime.fromisoformat(str(row["source_interval_end_utc"])),
        )
        source = by_bounds.get(src)
        if source is None or source["value"] != float(raw):
            raise AlignmentError(
                f"{series_id} at {origin.isoformat()}",
                f"value {raw!r} does not trace to an observation on the recorded source interval "
                f"{src[0].isoformat()}..{src[1].isoformat()} (D-44: every selected value keeps its source identity)",
            )
        available_at = dt.datetime.fromisoformat(str(row["available_at_utc"]))
        if available_at != src[1] + lag:
            raise AlignmentError(
                f"{series_id} at {origin.isoformat()}",
                f"available_at {available_at.isoformat()} is not source end + {safe_lag_hours} h "
                f"({(src[1] + lag).isoformat()}); the lag is applied exactly once (D-44)",
            )
        if available_at > origin:
            raise AlignmentError(
                f"{series_id} at {origin.isoformat()}",
                f"selected interval becomes available at {available_at.isoformat()}, after the origin "
                f"(open or not-yet-available interval; D-10.3, D-43)",
            )
        if latest is None or latest["interval_end"] != src[1]:
            raise AlignmentError(
                f"{series_id} at {origin.isoformat()}",
                f"a later interval (ending {latest['interval_end'].isoformat() if latest else 'n/a'}) "
                f"is eligible at this origin; the LATEST eligible interval is selected (D-44)",
            )


def availability_rows_from_selection(
    rows: Sequence[Mapping[str, Any]], *, release_status: str
) -> list[dict[str, Any]]:
    """The availability-matrix rows (W-1; `build_availability_matrix`) for a lagged
    series, derived from the selection so the matrix measures the SAME instants the
    producer used: `forecast_origin` = the row's epoch, `observation_timestamp` = the
    selected source interval's END (D-43), `publication_timestamp` empty (no provider
    publication timestamp is held — the row's `publication_latency_statement` records the
    absence). Rows without a selected value carry no matrix row."""
    out: list[dict[str, Any]] = []
    for row in rows:
        if row.get("source_interval_end_utc") is None or row.get("value") is None:
            continue
        out.append(
            {
                "forecast_origin": dt.datetime.fromisoformat(str(row["interval_start_utc"])),
                "observation_timestamp": dt.datetime.fromisoformat(
                    str(row["source_interval_end_utc"])
                ),
                "publication_timestamp": None,
                "release_status": release_status,
            }
        )
    return out


# --- D-21 / D-22: the project-derived daily F10.7 value ------------------------------------


def daily_medians_from_readings(
    readings: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """The daily F10.7 value as the project derives it (D-21: the MEDIAN of the UT day's
    observed readings; D-22: readings sharing one UT timestamp are first averaged, the
    duplicate count logged and the day flagged; D-23: high-spread days — range > 20 % of
    the median — are flagged and RETAINED). Each reading carries `day` (date), `time`
    (str, the provider's UT stamp) and `value` (observed flux, sfu). Readings are never
    dropped, clipped or reconstructed; a day with no reading is simply absent.

    Returns `{"medians": {day: float}, "duplicate_days": {day: count}, "high_spread_days":
    {day: spread_pct}}`.
    """
    by_day: dict[dt.date, dict[str, list[float]]] = {}
    for record in readings:
        by_day.setdefault(record["day"], {}).setdefault(str(record["time"]), []).append(
            float(record["value"])
        )
    medians: dict[dt.date, float] = {}
    duplicate_days: dict[dt.date, int] = {}
    high_spread: dict[dt.date, float] = {}
    for day, slots in sorted(by_day.items()):
        values: list[float] = []
        for _stamp, readings_at in sorted(slots.items()):
            if len(readings_at) > 1:
                duplicate_days[day] = duplicate_days.get(day, 0) + len(readings_at) - 1
            values.append(sum(readings_at) / len(readings_at))
        values.sort()
        n = len(values)
        median = values[n // 2] if n % 2 else (values[n // 2 - 1] + values[n // 2]) / 2.0
        medians[day] = median
        if median > 0 and (max(values) - min(values)) / median > 0.20:
            high_spread[day] = 100.0 * (max(values) - min(values)) / median
    return {"medians": medians, "duplicate_days": duplicate_days, "high_spread_days": high_spread}


# --- R-57a / R-58 limb 3: carry-forward, and the conservation invariant ----------------


def apply_carry_forward(
    hourly: Mapping[dt.datetime, float | None],
    *,
    bound_h: int,
) -> dict[str, Any]:
    """Fill a MISSING epoch by carrying the last observed value forward at most
    `bound_h` hours; beyond the bound the row is EXCLUDED, never filled (FR-P1-04-3,
    TC-09 -- the register's named central leakage-prevention rule). The bound is read
    from `configs/features.yaml` by the caller and passed in; it is never hardcoded
    here (R-57a).

    A missing epoch is one whose value is None or NaN (D-5: gaps are explicit NaN at
    acquisition). Every carried-forward epoch is RECORDED -- the record is what
    distinguishes the sanctioned fill from a prohibited one, by construction (R-58
    limb 3's conservation invariant).

    Returns a mapping with `values` (kept epochs only), `carried_forward_epochs`
    (sorted, machine-readable) and `excluded_epochs` (sorted, machine-readable --
    a completeness fact, never console text only).
    """
    if bound_h < 0:
        raise IntegrityError("apply_carry_forward", f"bound_h must be >= 0, got {bound_h!r}")
    values: dict[dt.datetime, float] = {}
    carried: list[dt.datetime] = []
    excluded: list[dt.datetime] = []
    last_observed_at: dt.datetime | None = None
    last_observed: float | None = None
    for epoch in sorted(hourly):
        raw = hourly[epoch]
        present = raw is not None and not math.isnan(float(raw))
        if present:
            value = float(raw)  # type: ignore[arg-type]
            values[epoch] = value
            last_observed_at = epoch
            last_observed = value
            continue
        if (
            last_observed_at is not None
            and last_observed is not None
            and (epoch - last_observed_at) <= dt.timedelta(hours=bound_h)
        ):
            values[epoch] = last_observed
            carried.append(epoch)
        else:
            excluded.append(epoch)
    return {
        "values": values,
        "carried_forward_epochs": sorted(carried),
        "excluded_epochs": sorted(excluded),
    }


def assert_carry_forward_conservation(
    values: Mapping[dt.datetime, float],
    observations: Mapping[dt.datetime, float | None],
    carried_forward_epochs: Collection[dt.datetime],
) -> None:
    """R-58 limb 3's conservation invariant -- the limb that carries the rule.

    For every driver series, the count of epochs carrying a value that is NOT an
    observation at that epoch EQUALS the count of epochs recorded as carried-forward
    under R-57a. Any value present at an epoch with no observation and no recorded
    carry-forward FAILS. Stated as a law over the EMITTED series rather than over the
    source text, it catches any fill -- aliased, vectorised, dispatched or not yet
    invented -- that the AST token scan cannot reach.

    Raises
    ------
    IntegrityError
        naming each unrecorded filled epoch, or a recorded count that does not
        reconcile.
    """
    carried = set(carried_forward_epochs)
    unrecorded = sorted(
        epoch.isoformat()
        for epoch in values
        if epoch not in carried
        and (
            epoch not in observations
            or observations[epoch] is None
            or math.isnan(float(observations[epoch]))  # type: ignore[arg-type]
        )
    )
    if unrecorded:
        raise IntegrityError(
            "driver series conservation invariant",
            f"value(s) present at epoch(s) with no observation and no recorded "
            f"carry-forward: {unrecorded}; a filled epoch is permitted precisely "
            f"because it is recorded and prohibited precisely because it is not "
            f"(R-58 limb 3, TC-09)",
        )
    filled_count = sum(
        1
        for epoch in values
        if epoch not in observations
        or observations[epoch] is None
        or math.isnan(float(observations[epoch]))  # type: ignore[arg-type]
    )
    if filled_count != len(carried):
        raise IntegrityError(
            "driver series conservation invariant",
            f"carried_forward_epochs records {len(carried)} epoch(s) but the emitted "
            f"series carries {filled_count} non-observation value(s); the recorded "
            f"count is load-bearing, not decorative (domain-entities section 1)",
        )


# --- R-63: time-indexed only ------------------------------------------------------------

#: Keys that designate a cell or station in a row shape. A driver series carrying one
#: is a per-cell join shape and is refused (TC-12).
_CELL_KEYS: tuple[str, ...] = ("station", "station_id", "cell", "cell_id", "gdlat", "glon")


def assert_time_indexed_shape(rows: Sequence[Mapping[str, Any]]) -> None:
    """R-63: a driver series is time-indexed ONLY -- one value per epoch, identical
    across all three cells. A row shape carrying a station or cell key implies a
    per-cell measurement the dataset does not contain, and is refused at construction:
    a station performance difference must never be attributed to local forcing the
    dataset does not contain (TC-12, FR-P1-04-4).

    Raises
    ------
    IntegrityError
        naming the offending key. (Would-be `DriverError`; the base is raised while
        that declaration is contested -- see the module docstring.)
    """
    for index, row in enumerate(rows):
        offending = sorted(key for key in row if str(key).lower() in _CELL_KEYS)
        if offending:
            raise IntegrityError(
                f"driver series row {index}",
                f"row carries cell-designating key(s) {offending}; driver series are "
                f"time-indexed only -- one value per epoch, identical across all "
                f"three cells (TC-12, FR-P1-04-4) -- and a per-cell join shape is "
                f"refused at construction",
            )


def assert_identical_across_cells(
    joined_rows: Sequence[Mapping[str, Any]], *, epoch_key: str, value_key: str, cell_key: str
) -> None:
    """The joined-grid check: after a driver joins the cell grid, the value at one
    epoch is identical in every cell (R-63's negative control: a driver value that
    differs between cells at one epoch fails).

    Raises
    ------
    IntegrityError
        naming the first epoch whose values differ across cells.
    """
    by_epoch: dict[Any, dict[Any, float]] = {}
    for row in joined_rows:
        by_epoch.setdefault(row[epoch_key], {})[row[cell_key]] = float(row[value_key])
    for epoch in sorted(by_epoch, key=str):
        distinct = set(by_epoch[epoch].values())
        if len(distinct) > 1:
            raise IntegrityError(
                f"driver join at epoch {epoch}",
                f"values differ across cells ({by_epoch[epoch]}); one value per epoch, "
                f"identical across all three cells (TC-12) -- the join implies a "
                f"per-cell measurement the dataset does not contain",
            )


# --- R-62: grades and eligibility -------------------------------------------------------


def assert_single_grade(series_id: str, grades: Collection[str]) -> None:
    """R-62 restriction 2 / D-10.1: exactly one recorded release grade per series for
    calendar 2022 -- mixed grades FAIL AT CONSTRUCTION, never downstream.

    Raises
    ------
    IntegrityError
        naming the mixed grades. (Would-be `DriverError`; base raised -- module
        docstring.)
    """
    distinct = sorted({str(grade) for grade in grades})
    if len(distinct) != 1:
        raise IntegrityError(
            f"driver series {series_id}",
            f"release grades are mixed within one series: {distinct or ['<none>']}; "
            f"exactly ONE recorded grade per series for calendar 2022 (D-10.1; "
            f"project.md Forbidden: never mix Kyoto Dst release grades within one "
            f"series)",
        )


def assert_grade_eligible(series_id: str, grade: str, *, use: str) -> None:
    """R-62 restriction 3 / GradeEligibility: eligibility is a property of THE DATA,
    asserted at the point of use, so it survives a consumer nobody has written yet.

    Provisional grade: permitted for fixture characterisation ONLY (D-11); never a
    modelling input, never a frozen tolerance, never a G-05 regime count (D-13 --
    the December regime count comes from GFZ Kp/Hp60 at a recorded release grade).
    Dst is additionally diagnostic/hindcast-only whatever its grade (TC-11).

    Raises
    ------
    IntegrityError
        on an unknown use, a diagnostic-only series requested as a modelling input, or
        a provisional grade requested for any of the three barred uses.
    """
    if use not in GRADE_USES:
        raise IntegrityError(
            f"driver series {series_id}",
            f"unknown grade-eligibility use {use!r}; the distinguished uses are "
            f"{sorted(GRADE_USES)} (domain-entities section 3) -- an unlisted use is "
            f"refused rather than defaulted",
        )
    if series_id in DIAGNOSTIC_ONLY_SERIES and use == "modelling_input":
        raise IntegrityError(
            f"driver series {series_id}",
            "Dst is diagnostic/hindcast-only and never a confirmatory ML feature "
            "(TC-11); no grade makes it eligible as a modelling input",
        )
    if str(grade).lower() == "provisional" and use != "fixture_characterisation":
        detail = {
            "modelling_input": "a modelling input",
            "frozen_tolerance": "a frozen tolerance",
            "g05_regime_count": (
                "a G-05 regime count -- D-13 requires the December regime count to "
                "come from GFZ Kp/Hp60 at a recorded release grade"
            ),
        }[use]
        raise IntegrityError(
            f"driver series {series_id}",
            f"a provisional-graded series is ineligible as {detail}; provisional Dst "
            f"may characterise fixture selection only (D-11)",
        )


# --- R-63's Constraint: the reanalysed-value check's driver-product half ----------------


def assert_series_provenance(series_id: str, entry: Mapping[str, Any]) -> None:
    """The four provenance fields, their internal consistency, and the per-series
    verifiability record (R-63's Constraint; SD-E-06).

    Asserts: (1) all four of `release_status`, `retrieval_date`,
    `provider_product_identity` (FULL identity including any version suffix -- drift
    `g.002` vs `g.003` is already observed in this dataset) and `sha256` are present
    and non-empty; (2) the declared status is not contradicted by the recorded product
    identity (`final` against a `dst_provisional_*` filename FAILS -- the detectable
    form of the backfill rule); (3) a declared-status-only series (F10.7, Dst) carries
    a `provenance_verifiability` record with the documented absence and an explicit
    unverified-status statement -- inferring a grade from silence is not evidence; and
    (4) no declared-status-only series reports its verifiability as closed or
    verified -- the reanalysed-value check is BOUNDED, NOT CLOSED, for these series,
    and no artifact may report it as closed.

    Raises
    ------
    IntegrityError
        naming the series and the violated expectation. (Integrity tier: omission or
        inconsistency terminates; the verifiability record itself is the sanctioned
        completeness evidence.)
    """
    missing = sorted(
        field for field in PROVENANCE_FIELDS if not str(entry.get(field, "") or "").strip()
    )
    if missing:
        raise IntegrityError(
            f"driver manifest entry {series_id}",
            f"provenance field(s) {missing} absent or empty; every driver series "
            f"records all four of {list(PROVENANCE_FIELDS)} (R-63's Constraint -- the "
            f"reanalysed-value check's driver-product half), and an omitted field "
            f"terminates",
        )
    status = str(entry["release_status"]).lower()
    identity = str(entry["provider_product_identity"]).lower()
    identity_grades = {token for token in _GRADE_TOKENS if token in identity}
    status_grades = {token for token in _GRADE_TOKENS if token in status}
    if identity_grades and status_grades and not (identity_grades & status_grades):
        raise IntegrityError(
            f"driver manifest entry {series_id}",
            f"declared release_status {entry['release_status']!r} is inconsistent "
            f"with the recorded provider product identity "
            f"{entry['provider_product_identity']!r} (identity carries grade "
            f"token(s) {sorted(identity_grades)}); this is the detectable form of "
            f"the never-backfill rule (R-63 control 1) and it terminates",
        )
    if series_id in DECLARED_STATUS_ONLY_SERIES:
        verifiability = entry.get("provenance_verifiability")
        if not isinstance(verifiability, Mapping):
            raise IntegrityError(
                f"driver manifest entry {series_id}",
                "declared-status-only series carries no provenance_verifiability "
                "record; a status recorded for a file with no provenance column and "
                "no documented-absence/unverified-status statement is an integrity "
                "violation -- the absence must be STATED, never implied by silence "
                "(R-63's Constraint, D-25's shape, CR-2026-08-22-EV-12)",
            )
        for required in ("documented_absence", "unverified_status_statement"):
            if not str(verifiability.get(required, "") or "").strip():
                raise IntegrityError(
                    f"driver manifest entry {series_id}",
                    f"provenance_verifiability.{required} is absent or empty; the "
                    f"sanctioned evidence for a declared-status-only series is the "
                    f"declared status PLUS the documented absence PLUS an explicit "
                    f"unverified-status statement (R-63's Constraint)",
                )
        claim = json.dumps(dict(verifiability)).lower()
        if '"closed"' in claim or '"verified"' in claim or "status: closed" in claim:
            raise IntegrityError(
                f"driver manifest entry {series_id}",
                "provenance_verifiability reports the reanalysed-value check as "
                "closed or verified for a declared-status-only series; the check is "
                "BOUNDED, NOT CLOSED, for F10.7 and Dst, and no artifact may report "
                "it as closed (R-63's Constraint, carried to G-04)",
            )


def assert_gfz_cross_products(
    series_id: str,
    *,
    near_real_time: Mapping[Any, float],
    definitive: Mapping[Any, float],
    emitted: Mapping[Any, float],
) -> None:
    """The one substantive backfill detection this design can offer (R-63 control 5),
    specified NOW against the deferred GFZ retrieval: the near-real-time and
    definitive products are asserted against each other value by value, and an
    emitted value matching the DEFINITIVE product where the near-real-time product
    differs FAILS -- that is the actual backfill the rule exists to catch.

    Raises
    ------
    IntegrityError
        naming each epoch where the emitted value matches definitive against a
        differing near-real-time value.
    """
    offenders: list[str] = []
    for epoch in sorted(emitted, key=str):
        if epoch not in near_real_time or epoch not in definitive:
            continue
        nrt = float(near_real_time[epoch])
        deft = float(definitive[epoch])
        if nrt != deft and float(emitted[epoch]) == deft:
            offenders.append(str(epoch))
    if offenders:
        raise IntegrityError(
            f"driver series {series_id}",
            f"emitted value(s) at epoch(s) {offenders} match the DEFINITIVE product "
            f"where the near-real-time product differs; final archived values are not "
            f"equivalent to the contemporaneous operational values available at a "
            f"2022 forecast origin (project.md Forbidden: never backfill from future "
            f"final values; R-63 control 5)",
        )


# --- SD-E-03 producing half + SD-E-07: stamps and the re-run contract -------------------


def provenance_stamp(*, source: str, produced_by: str) -> dict[str, str]:
    """The provenance stamp every value written by `04_build_external_products.py`
    carries (SD-E-03's producing half, SEC-E-05).

    The stamp is EVIDENTIARY, never cryptographic: nothing validates its truthfulness,
    and no artifact may describe it as a signature. What the flipped default buys is
    that an omission becomes a commission -- a stripped stamp could be an accident of a
    copy step; a stamp asserting a false origin is a written, attributable claim
    (SD-E-03's disclosed framing, quoted at the stage gate as a recorded Minor).
    """
    return {
        "source": source,
        "produced_by": produced_by,
        "stamp_class": "evidentiary",
        "stamped_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }


def write_driver_manifest(
    path: Path,
    *,
    series_entries: Sequence[Mapping[str, Any]],
    missing_months: Sequence[str],
    produced_by: str,
) -> Path:
    """Write the driver manifest (domain-entities section 8): completeness recorded,
    integrity terminal.

    `missing_months` NAMES which months are missing -- a machine-readable completeness
    field, non-fatal, never console text only (a bare count is the "unattributed
    number" shape inventory-and-registry R-51 forbids in the G-P1A decision this
    feeds). Every series entry must pass `assert_series_provenance` and carry a
    `carried_forward_epochs` field (R-58 limb 3's manifest evidence -- a field survives
    the absence of a gate where a test result does not). Every value routes through
    acquisition's `guard_egress` (NFR-SEC-01) and carries a provenance stamp
    (SD-E-03's producing half).

    Raises
    ------
    IntegrityError
        on a provenance omission or inconsistency in any entry, or an entry with no
        `series_id` or no `carried_forward_epochs` field.
    CredentialEgressError
        when any value fails the redaction chokepoint.
    """
    stamped_entries: list[dict[str, Any]] = []
    for entry in series_entries:
        series_id = str(entry.get("series_id", "") or "")
        if not series_id:
            raise IntegrityError(
                str(path),
                "a driver manifest entry carries no series_id; an unattributable "
                "entry cannot be reconciled against anything (R-63)",
            )
        assert_series_provenance(series_id, entry)
        if "carried_forward_epochs" not in entry:
            raise IntegrityError(
                f"driver manifest entry {series_id}",
                "carried_forward_epochs is absent; the recorded count is the "
                "conservation invariant's manifest evidence and is load-bearing, "
                "not decorative (R-58 limb 3, Recommendation 38)",
            )
        stamped = dict(entry)
        stamped["provenance_stamp"] = provenance_stamp(
            source=str(entry["provider_product_identity"]), produced_by=produced_by
        )
        stamped_entries.append(stamped)

    payload: dict[str, Any] = {
        "artifact_class": "driver_manifest",
        "derived": True,
        "partial": bool(missing_months),
        "missing_months": sorted(str(month) for month in missing_months),
        "series": stamped_entries,
        "produced_by": produced_by,
        "provenance_stamp_note": (
            "stamps are evidentiary, not cryptographic (SD-E-03): nothing validates "
            "a stamp's truthfulness, and no reader may treat one as a signature"
        ),
    }
    guard_egress(payload, context=f"driver_manifest[{Path(path).name}]")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def refuse_divergent_rerun(
    product_path: Path,
    *,
    recorded_identity: str,
    recorded_sha256: str,
    current_identity: str,
) -> None:
    """SD-E-07: a revised external product is byte-identical, or explicitly divergent.

    A re-run recomputes the SHA-256 of every external product. On any difference it
    records BOTH product identities (each including the provider's version or issue
    designation, where one exists -- drift `g.002` vs `g.003` is already observed) and
    BOTH hashes, and REFUSES to overwrite. This is acquisition's SEC-A-02 contract
    adopted unchanged, so the two units that fetch external material do not diverge on
    the same question. A stopped run awaiting adjudication is the intended cost, and
    it will fire on legitimate provider re-issues.

    Raises
    ------
    IntegrityError
        on a hash difference, carrying both identities and both hashes -- the
        divergence record IS the message; nothing is overwritten.
    """
    actual = sha256_of_file(Path(product_path))
    if actual != recorded_sha256:
        raise IntegrityError(
            str(product_path),
            f"external product diverges from its recorded bytes and the overwrite is "
            f"REFUSED (SD-E-07, adopting SEC-A-02 unchanged): recorded identity "
            f"{recorded_identity!r} with sha256 {recorded_sha256}; current identity "
            f"{current_identity!r} with sha256 {actual}. A re-issued product day that "
            f"silently replaced the old one would change a published number with no "
            f"trace; record both and adjudicate, never overwrite",
        )
