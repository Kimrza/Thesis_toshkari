"""F-1 Availability record: no predictor precedes its own availability (W-1, W-1a; R-75).

Purpose
-------
The availability matrix — one `AvailabilityRow` per feature — and the THREE limbs that make
FR-P1-04-2 executable rather than declared:

1. **Lag assertion**: `actual_lag_hours >= safe_lag_hours` for every feature, where the
   actual lag is measured from the forecast origin back to the instant the value became
   available (the later of its observation and, where known, its publication timestamp). A
   value published after the origin has a negative lag and fails here.
2. **Trailing, never centered**: the `f107_81_trailing` window definition read from
   `configs/features.yaml` must be `trailing`; a centered window is a defect, not a fallback
   (`project.md` Forbidden).
3. **The anchor, asserted AND recomputed** (Q4 = D): a trailing mean's recorded end day
   must equal the safe-lagged day for its origin, and the mean is RECOMPUTED from that anchor
   over the daily values (through `external-products`' `trailing_mean`, the one home of the
   trailing-window arithmetic) and compared within the configured tolerance. A recorded end
   date is a claim; the recomputation is the check — it catches a recorded-but-wrong anchor
   whose values were never computed from it, which limbs 1 and 2 both pass.

Plus: the release-status record and the backfill refusal (a `final` archived grade where the
contemporaneous grade was required — never backfill from future final values), Dst as
diagnostic/hindcast-only, and the documented-absence limb for a series whose archive carries
no publication timestamp (recorded WITH an unverified-latency statement, never as a blank).

Every lag VALUE (3 h, 1 h, previous-day, 81 days) is `configs/features.yaml` content
(`availability_lags`), never a literal here (TC-03e; D-10.3). While the block is absent or
`TBD — freeze gate` this module REFUSES, naming the field (TE 18.3).

Inputs
------
`snapshot.features["availability_lags"]`; caller-supplied driver frames (DataFrames or record
sequences) carrying `forecast_origin`, `observation_timestamp`, `publication_timestamp`
(nullable), `release_status`, and — for a trailing-mean feature — `anchor_day` and
`mean_value`, with the daily source series supplied under the window's declared `source`.

Re-run behaviour
----------------
Pure functions of their inputs; deterministic; nothing persisted.

Boundary
--------
Imports `src.external.spaceweather` only (the driver product's own arithmetic); never
`src.external.iri` or `src.external.gim` (TE 12 import-boundary rule; R-56).
"""

from __future__ import annotations

import datetime as dt
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final

from src.data.config import (
    TBD_SENTINEL,
    ConfigSnapshot,
    FeatureAvailabilityError,
    IntegrityError,
    LeakageError,
)
from src.external.spaceweather import DIAGNOSTIC_ONLY_SERIES, trailing_mean
from src.features._frames import ensure_records, records_of

__all__ = [
    "AvailabilityRow",
    "WINDOW_KIND_TRAILING",
    "read_availability_lags",
    "build_availability_matrix",
    "assert_lags_safe",
    "assert_trailing_not_centered",
    "assert_anchor_recomputed",
    "assert_dst_diagnostic_only",
    "assert_release_status_not_backfilled",
]

#: The only permitted window kind for a rolling driver mean (TE 6.2 `f107_81_trailing`).
WINDOW_KIND_TRAILING: Final[str] = "trailing"

_UTC: Final = dt.UTC


@dataclass(frozen=True)
class AvailabilityRow:
    """The approved six fields, plus two ADDITIVE recorded fields.

    `anchor_policy` records, for a trailing-mean feature, the rule its anchor was checked
    against (the safe-lagged day) — the matrix is per FEATURE while anchors are per ORIGIN,
    so the per-origin anchors are checked in `assert_anchor_recomputed` and the row records
    that the check ran. `latency_statement` carries the documented absence of a publication
    timestamp with the unverified-latency statement TE 7.0A stage 4 requires; it is required
    whenever `publication_timestamp` is empty.
    """

    feature: str
    observation_timestamp: str
    publication_timestamp: str
    release_status: str
    safe_lag_hours: float
    actual_lag_hours: float
    anchor_policy: str | None = None
    latency_statement: str | None = None


# --- config ------------------------------------------------------------------------------


def _is_tbd(value: object) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == TBD_SENTINEL)


def read_availability_lags(snapshot: ConfigSnapshot) -> Mapping[str, Mapping[str, Any]]:
    """`features.availability_lags`: per feature `safe_lag_hours`, `release_status_required`,
    optional `window` (`kind`, `days`, `source`, `recomputation_tolerance`) and optional
    `publication_latency_statement`.

    Raises
    ------
    FeatureAvailabilityError
        when the block or any feature's `safe_lag_hours` is absent or `TBD — freeze gate`
        (D-10.3's values are configuration frozen under their D-number, never a literal).
    """
    block = snapshot.features.get("availability_lags")
    if _is_tbd(block):
        raise FeatureAvailabilityError(
            "configs/features.yaml: availability_lags",
            "absent or unresolved (TBD — freeze gate); every safe lag (Kp/ap3, Hp60/ap60, "
            "F10.7 previous-day, the 81-day trailing window) is configuration frozen under "
            "D-10.3, never a literal in src/features — stop and report (TE 18.3)",
        )
    if not isinstance(block, Mapping) or not block:
        raise FeatureAvailabilityError(
            "configs/features.yaml: availability_lags",
            "must be a non-empty mapping of feature -> lag record",
        )
    out: dict[str, Mapping[str, Any]] = {}
    for feature, entry in block.items():
        resource = f"configs/features.yaml: availability_lags.{feature}"
        if not isinstance(entry, Mapping):
            raise FeatureAvailabilityError(resource, "entry must be a mapping")
        lag = entry.get("safe_lag_hours")
        if _is_tbd(lag):
            raise FeatureAvailabilityError(
                f"{resource}.safe_lag_hours", "absent or unresolved (TBD — freeze gate)"
            )
        if isinstance(lag, bool) or not isinstance(lag, int | float) or lag < 0:
            raise FeatureAvailabilityError(
                f"{resource}.safe_lag_hours", f"{lag!r} is not a non-negative number of hours"
            )
        window = entry.get("window")
        if window is not None:
            if not isinstance(window, Mapping):
                raise FeatureAvailabilityError(f"{resource}.window", "must be a mapping")
            for key in ("kind", "days", "source", "recomputation_tolerance"):
                if _is_tbd(window.get(key)):
                    raise FeatureAvailabilityError(
                        f"{resource}.window.{key}",
                        "absent or unresolved (TBD — freeze gate); the window's kind, "
                        "length, daily source and recomputation tolerance are all frozen "
                        "configuration (TE 6.2 f107_81_trailing; TE 15.1 tolerances are "
                        "measured and frozen, never invented)",
                    )
        out[str(feature)] = entry
    return out


# --- timestamps --------------------------------------------------------------------------


def _as_utc(value: object, *, resource: str) -> dt.datetime:
    if isinstance(value, dt.datetime):
        stamp = value
    elif isinstance(value, dt.date):
        stamp = dt.datetime(value.year, value.month, value.day)
    elif isinstance(value, str):
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            stamp = dt.datetime.fromisoformat(text)
        except ValueError as exc:
            raise FeatureAvailabilityError(
                resource, f"timestamp {value!r} is not ISO-8601"
            ) from exc
    else:
        to_py = getattr(value, "to_pydatetime", None)
        if callable(to_py):
            stamp = to_py()
        else:
            raise FeatureAvailabilityError(resource, f"timestamp {value!r} is unrecognised")
    if stamp.tzinfo is None:
        return stamp.replace(tzinfo=_UTC)
    return stamp.astimezone(_UTC)


def _as_date(value: object, *, resource: str) -> dt.date:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value.strip())
        except ValueError as exc:
            raise FeatureAvailabilityError(resource, f"{value!r} is not an ISO date") from exc
    raise FeatureAvailabilityError(resource, f"{value!r} is not a calendar date")


def _is_missing(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, float) and math.isnan(value):
        return True
    return False


def _hours(delta: dt.timedelta) -> float:
    return delta.total_seconds() / 3600.0


# --- W-1: the matrix ---------------------------------------------------------------------


def build_availability_matrix(
    snapshot: ConfigSnapshot, *, drivers: Mapping[str, Any]
) -> tuple[AvailabilityRow, ...]:
    """One `AvailabilityRow` per configured feature, measured from the supplied driver rows.

    For each feature in `availability_lags`, `drivers[feature]` must supply rows carrying
    `forecast_origin`, `observation_timestamp`, `publication_timestamp` (may be empty when
    the archive carries none — then the configured `publication_latency_statement` is
    REQUIRED and recorded), and `release_status`. The recorded `actual_lag_hours` is the
    MINIMUM over rows of origin minus availability instant — the tightest lag, which is the
    one the assertion must clear. Trailing-mean features run limbs 2 and 3 here as well,
    because the per-origin anchors live in these rows.

    Raises
    ------
    FeatureAvailabilityError
        a feature with no driver rows; a missing column; a publication timestamp absent
        with no documented-absence statement; mixed release grades within one series.
    LeakageError
        a centered window (limb 2) or an anchor/recomputation failure (limb 3).
    """
    lags = read_availability_lags(snapshot)
    rows: list[AvailabilityRow] = []
    for feature, entry in lags.items():
        if feature not in drivers:
            raise FeatureAvailabilityError(
                f"availability matrix: {feature}",
                f"no driver rows supplied; every configured feature is measured, none is "
                f"assumed available (drivers supplied: {sorted(drivers)})",
            )
        records = ensure_records(drivers[feature], resource=f"driver rows for {feature}")
        grades: set[str] = set()
        best_lag: float | None = None
        best_obs = ""
        best_pub = ""
        publication_absent = False
        for index, record in enumerate(records):
            resource = f"{feature} row {index}"
            for key in ("forecast_origin", "observation_timestamp", "release_status"):
                if key not in record or _is_missing(record[key]):
                    raise FeatureAvailabilityError(
                        resource, f"column {key!r} absent or empty; the matrix records it"
                    )
            origin = _as_utc(record["forecast_origin"], resource=f"{resource}.forecast_origin")
            observed = _as_utc(
                record["observation_timestamp"], resource=f"{resource}.observation_timestamp"
            )
            available_at = observed
            publication_text = ""
            pub_raw = record.get("publication_timestamp")
            if _is_missing(pub_raw):
                publication_absent = True
            else:
                published = _as_utc(pub_raw, resource=f"{resource}.publication_timestamp")
                available_at = max(observed, published)
                publication_text = published.isoformat()
            lag = _hours(origin - available_at)
            grades.add(str(record["release_status"]).strip())
            if best_lag is None or lag < best_lag:
                best_lag = lag
                best_obs = observed.isoformat()
                best_pub = publication_text
        if len(grades) != 1:
            raise FeatureAvailabilityError(
                f"availability matrix: {feature}",
                f"driver rows carry {len(grades)} distinct release grades {sorted(grades)}; "
                f"grades are never mixed within one series (D-10.1), and the matrix records "
                f"exactly one",
            )
        latency_statement: str | None = None
        if publication_absent:
            statement = entry.get("publication_latency_statement")
            if _is_tbd(statement) or not str(statement).strip():
                raise FeatureAvailabilityError(
                    f"configs/features.yaml: availability_lags.{feature}."
                    f"publication_latency_statement",
                    "the archive carries no publication timestamp for this series, so the "
                    "approved conservative availability convention AND the documented "
                    "absence must be recorded in its place, with the publication latency "
                    "marked unverified (TE 7.0A stage 4) — a blank is not a record",
                )
            latency_statement = str(statement)
        anchor_policy: str | None = None
        window = entry.get("window")
        if window is not None:
            assert_trailing_not_centered(feature, window)
            source = str(window["source"])
            if source not in drivers:
                raise FeatureAvailabilityError(
                    f"availability matrix: {feature}",
                    f"the trailing window's daily source {source!r} was not supplied; the "
                    f"anchor limb recomputes the mean and cannot run without it",
                )
            assert_anchor_recomputed(
                feature,
                records,
                daily_values=_daily_values(drivers[source], resource=source),
                safe_lag_hours=float(entry["safe_lag_hours"]),
                window_days=int(window["days"]),
                tolerance=float(window["recomputation_tolerance"]),
            )
            anchor_policy = "window ends at the safe-lagged day; mean recomputed from anchor"
        assert best_lag is not None
        rows.append(
            AvailabilityRow(
                feature=feature,
                observation_timestamp=best_obs,
                publication_timestamp=best_pub,
                release_status=next(iter(grades)),
                safe_lag_hours=float(entry["safe_lag_hours"]),
                actual_lag_hours=best_lag,
                anchor_policy=anchor_policy,
                latency_statement=latency_statement,
            )
        )
    return tuple(rows)


def _daily_values(frame: Any, *, resource: str) -> dict[dt.date, float]:
    out: dict[dt.date, float] = {}
    for index, record in enumerate(records_of(frame)):
        if "day" not in record or "value" not in record:
            raise FeatureAvailabilityError(
                f"{resource} row {index}", "daily source rows carry `day` and `value`"
            )
        day = _as_date(record["day"], resource=f"{resource} row {index}.day")
        value = record["value"]
        out[day] = float("nan") if _is_missing(value) else float(value)
    return out


# --- the three limbs, each its own function ----------------------------------------------


def assert_lags_safe(
    matrix: Sequence[AvailabilityRow],
    *,
    required_release_status: Mapping[str, str] | None = None,
) -> None:
    """Limb 1 (plus the backfill refusal and the anchor-record presence check).

    Raises
    ------
    LeakageError
        when any row has `actual_lag_hours < safe_lag_hours`; when a row's
        `release_status` is a grade other than the one `required_release_status` names for
        it (a backfilled `final` where the contemporaneous grade was required); when a
        trailing-mean row carries no `anchor_policy` (the third limb never ran); or when a
        row records neither a publication timestamp nor a documented-absence statement.
    """
    if not matrix:
        raise LeakageError(
            "availability matrix", "is empty; an assertion over zero rows is not an assertion"
        )
    for row in matrix:
        if row.actual_lag_hours < row.safe_lag_hours:
            raise LeakageError(
                f"availability matrix: {row.feature}",
                f"actual lag {row.actual_lag_hours:.3f} h < safe lag {row.safe_lag_hours:.3f} h; "
                f"a predictor used before its availability instant is forecast leakage "
                f"(FR-P1-04-2, NFR-LEAK-01, D-10.3)",
            )
        if not row.publication_timestamp and not (row.latency_statement or "").strip():
            raise LeakageError(
                f"availability matrix: {row.feature}",
                "no publication timestamp and no documented-absence statement; the "
                "publication latency must be recorded as unverified, never left blank",
            )
        if required_release_status is not None and row.feature in required_release_status:
            assert_release_status_not_backfilled(
                row.feature, row.release_status, required=required_release_status[row.feature]
            )
    for row in matrix:
        if row.feature.endswith("_trailing") and not row.anchor_policy:
            raise LeakageError(
                f"availability matrix: {row.feature}",
                "trailing-mean feature carries no anchor record; the third limb (anchor "
                "asserted and mean recomputed) did not run, and a check that never ran must "
                "not pass for one that did",
            )


def assert_release_status_not_backfilled(
    feature: str, release_status: str, *, required: str
) -> None:
    """Never backfill a driver from future final values: the grade must be the required one."""
    if release_status.strip().lower() != required.strip().lower():
        raise LeakageError(
            f"availability matrix: {feature}",
            f"release_status {release_status!r} where {required!r} was required; a final "
            f"archived value is not the contemporaneous operational value available at a "
            f"2022 forecast origin, and a series can satisfy its lag while built from "
            f"reanalysed indices (project.md Forbidden; TE 10 driver table; R-09)",
        )


def assert_trailing_not_centered(feature: str, window: Mapping[str, Any]) -> None:
    """Limb 2: the window kind must be `trailing`; a centered mean uses future days."""
    kind = str(window.get("kind", "")).strip().lower()
    if kind != WINDOW_KIND_TRAILING:
        raise LeakageError(
            f"configs/features.yaml: availability_lags.{feature}.window.kind",
            f"{kind!r} is not {WINDOW_KIND_TRAILING!r}; a centered rolling mean uses future "
            f"days and is a defect, not a fallback (TE 6.2 f107_81_trailing; TE 10; "
            f"project.md Forbidden)",
        )


def assert_anchor_recomputed(
    feature: str,
    rows: Sequence[Mapping[str, Any]],
    *,
    daily_values: Mapping[dt.date, float],
    safe_lag_hours: float,
    window_days: int,
    tolerance: float,
) -> None:
    """Limb 3: for every origin, the recorded anchor IS the safe-lagged day, and the mean
    recomputed from that anchor over `daily_values` agrees within `tolerance`.

    Raises
    ------
    LeakageError
        a row without `anchor_day`/`mean_value`; an anchor that is not the safe-lagged day
        (an anchor AT the origin day passes limbs 1 and 2 while including same-day F10.7 —
        FR-P1-04-2's named hole); or a recorded mean that differs from the recomputation
        (a recorded-but-wrong anchor whose values came from another window).
    IntegrityError
        propagated from `trailing_mean` when a window day is missing (TC-20: never fill).
    """
    if tolerance < 0:
        raise IntegrityError(
            f"availability_lags.{feature}.window.recomputation_tolerance",
            f"{tolerance!r} is negative",
        )
    for index, record in enumerate(rows):
        resource = f"{feature} row {index}"
        if _is_missing(record.get("anchor_day")) or _is_missing(record.get("mean_value")):
            raise LeakageError(
                resource,
                "trailing-mean row carries no `anchor_day` or `mean_value`; the anchor is a "
                "recorded field, and the third limb cannot run over an unrecorded anchor",
            )
        origin = _as_utc(record["forecast_origin"], resource=f"{resource}.forecast_origin")
        expected_anchor = (origin - dt.timedelta(hours=safe_lag_hours)).date()
        recorded_anchor = _as_date(record["anchor_day"], resource=f"{resource}.anchor_day")
        if recorded_anchor != expected_anchor:
            raise LeakageError(
                resource,
                f"trailing window ends at {recorded_anchor.isoformat()} but the safe-lagged "
                f"day for origin {origin.isoformat()} is {expected_anchor.isoformat()}; a "
                f"trailing mean ending at day t passes the not-centered check and the lag "
                f"assertion while including same-day F10.7 (FR-P1-04-2, third limb)",
            )
        recomputed = trailing_mean(daily_values, end_day=recorded_anchor, window_days=window_days)
        recorded = float(record["mean_value"])
        if math.isnan(recorded) or abs(recomputed - recorded) > tolerance:
            raise LeakageError(
                resource,
                f"recorded mean {recorded!r} differs from the mean recomputed from anchor "
                f"{recorded_anchor.isoformat()} over {window_days} days ({recomputed!r}) by "
                f"more than the frozen tolerance {tolerance!r}; a recorded end date is a "
                f"claim and the recomputation is the check (Q4 = D)",
            )


def assert_dst_diagnostic_only(field_classes: Mapping[str, str]) -> None:
    """Dst is diagnostic/hindcast-only (TC-11): a Dst-named field with any other class fails."""
    for name, field_class in field_classes.items():
        tokens = {token for token in name.lower().replace("-", "_").split("_") if token}
        if tokens & DIAGNOSTIC_ONLY_SERIES and field_class != "diagnostic":
            raise LeakageError(
                f"feature dictionary field {name!r}",
                f"is a Dst-derived field declared {field_class!r}; Dst is diagnostic/"
                f"hindcast-only and never a confirmatory ML feature (Vision glossary; "
                f"TE 6.2; TC-11)",
            )
