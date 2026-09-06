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
    "PROVENANCE_FIELDS",
    "GRADE_USES",
    "trailing_mean",
    "resolve_f107_at_origin",
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


def resolve_f107_at_origin(
    daily_medians: Mapping[dt.date, float],
    *,
    origin: dt.datetime,
    availability_ts: Callable[[dt.date], dt.datetime],
    features: Mapping[str, Any],
) -> tuple[dt.date, float]:
    """The F10.7 previous-day observed value usable at `origin`, or the R-57a stop.

    The value usable at a forecast origin is the PREVIOUS DAY's observed median
    (D-10.3), available only once `availability_ts(day)` has passed (for F10.7 that
    convention is D-25's 00:00 UTC on day D+1 -- supplied by the CALLER as a callable,
    because the convention is a decision record's, not this module's). When the
    previous-day median is available, it is returned with no carry-forward.

    When it is NOT available, what a "<= 3 h" carry-forward bound means on a series
    whose native step is 24 h is the G-04 freeze item D-21 governs, and this function
    NEVER adopts a reading:

    Raises
    ------
    FeatureAvailabilityError
        while `features["carry_forward_composition"]` is absent or carries the literal
        `TBD -- freeze gate` sentinel -- naming the origin timestamp, the last available
        median's day, and the elapsed staleness in BOTH units (clock hours and whole
        daily steps). TE 18.3: stop and report, never default.
    IntegrityError
        when the field carries any other value: the adopted reading's vocabulary and
        its application are the Student's G-04 freeze plus `features-and-splits`'
        enforcement boundary (R-57a's negative controls are specified for
        `test_feature_availability.py`, sited there). Applying an unrecognised
        composition value here would be this module choosing the semantics of a frozen
        field it does not own -- refused, naming the field.
    """
    previous_day = origin.date() - dt.timedelta(days=1)
    if previous_day in daily_medians and availability_ts(previous_day) <= origin:
        return previous_day, float(daily_medians[previous_day])

    available = sorted(day for day in daily_medians if availability_ts(day) <= origin)
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
    raise IntegrityError(
        "configs/features.yaml: carry_forward_composition",
        f"the field carries {composition!r}; the adopted reading's application is the "
        f"Student's G-04 freeze plus features-and-splits' enforcement boundary "
        f"(R-57a), and this module refuses to interpret a composition vocabulary it "
        f"does not own -- {staleness_text}",
    )


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
        "stamped_at_utc": dt.datetime.now(dt.UTC).isoformat(),
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
