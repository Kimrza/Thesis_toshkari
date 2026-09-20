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

**Availability RULES (D-25; `CR-2026-09-16-D25-AVAILABILITY-RULE`).** A calendar-day rule
cannot be stated as a scalar `safe_lag_hours`: D-25 makes `median(D-1)` available at
`00:00 UTC on D`, so its lag depends on the origin's hour within the day. A feature may
therefore declare `availability_rule` — one of the CLOSED set `AVAILABILITY_RULE_KINDS` —
INSTEAD of `safe_lag_hours` (never both). A rule in `AVAILABILITY_RULES_WITH_WINDOW` may
also carry the trailing window (A2, `CR-2026-09-19-GATE-PREP-2`): the window's end day is
then DERIVED from the rule for each origin, never from a scalar. The rule instant is
combined with the observation/publication instant by `max`, so it sets a floor on
availability, never a ceiling: it can only shorten a measured lag, which is the
conservative direction, and a later publication timestamp still governs.

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
from src.external.spaceweather import (
    DIAGNOSTIC_ONLY_SERIES,
    SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG,
    trailing_mean,
)
from src.features._frames import ensure_records, records_of

__all__ = [
    "AvailabilityRow",
    "WINDOW_KIND_TRAILING",
    "AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC",
    "AVAILABILITY_RULE_KINDS",
    "AVAILABILITY_RULE_SCOPE",
    "AVAILABILITY_RULES_WITH_WINDOW",
    "LAG_REFERENCE_INSTANT_INTERVAL_END",
    "LAG_REFERENCE_INSTANT_KINDS",
    "SELECTION_RULE_KINDS",
    "read_availability_lags",
    "build_availability_matrix",
    "assert_lags_safe",
    "assert_trailing_not_centered",
    "assert_anchor_recomputed",
    "recomputation_tolerance_bound",
    "assert_recomputation_domain",
    "latest_eligible_window_end",
    "assert_dst_diagnostic_only",
    "assert_release_status_not_backfilled",
]

#: The only permitted window kind for a rolling driver mean (TE 6.2 `f107_81_trailing`).
WINDOW_KIND_TRAILING: Final[str] = "trailing"

#: D-25 as an executable identity: the daily median observed on UT day D-1 becomes
#: available at 00:00 UTC on day D (`availability_ts(median(D-1)) = 00:00 UTC on D`).
AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC: Final[str] = "previous_day_median_midnight_utc"

#: D-43's closed set for the safe-lag reference instant of an interval-valued (scalar-lag,
#: i.e. GFZ-style) row: the instant a safe lag is measured FROM is the observation
#: interval's END (completion) -- never its start. One value today; declaring anything
#: else is refused, never silently honoured (D-43 fixes this uniformly for every scalar-lag
#: row; a rule-governed row such as F10.7 has no interval to reference and must not carry
#: this field at all -- D-25's rule already fixes ITS own reference instant).
LAG_REFERENCE_INSTANT_INTERVAL_END: Final[str] = "interval_end_utc"
LAG_REFERENCE_INSTANT_KINDS: Final[frozenset[str]] = frozenset(
    {LAG_REFERENCE_INSTANT_INTERVAL_END}
)

#: D-44's closed set for the lagged-selection mechanism a scalar-lag row declares.
#: Mirrors `spaceweather.SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG` -- imported, never
#: retyped, so the reader's closed set and the producer's actual selection rule cannot
#: silently drift apart.
SELECTION_RULE_KINDS: Final[frozenset[str]] = frozenset({SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG})

#: The CLOSED set of recognised availability-rule kinds. An `availability_rule` outside
#: this set is refused at config read; nothing here infers a rule from a name.
AVAILABILITY_RULE_KINDS: Final[frozenset[str]] = frozenset(
    {AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC}
)

#: Which §6.2 rows each rule may govern. D-25 supplements D-21 and names the F10.7 daily
#: median only, so its rule is confined to the two F10.7 rows; the GFZ rows keep scalar
#: safe lags (D-10.3). A rule declared on any other feature is refused at config read
#: (A2, `CR-2026-09-19-A2-RULE-WINDOW`).
AVAILABILITY_RULE_SCOPE: Final[Mapping[str, frozenset[str]]] = {
    AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC: frozenset(
        {"f107_safe", "f107_81_trailing"}
    ),
}

#: Rules that may COMPOSE with a trailing window (A2). Under D-25 the window's end day is
#: derived from the rule — the latest observation day whose constituent availability
#: instant is at or before the forecast origin — so the anchor limb needs no scalar.
AVAILABILITY_RULES_WITH_WINDOW: Final[frozenset[str]] = frozenset(
    {AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC}
)

_UTC: Final = dt.timezone.utc


@dataclass(frozen=True)
class AvailabilityRow:
    """The approved six fields, plus three ADDITIVE recorded fields.

    `anchor_policy` records, for a trailing-mean feature, the rule its anchor was checked
    against (the safe-lagged day) — the matrix is per FEATURE while anchors are per ORIGIN,
    so the per-origin anchors are checked in `assert_anchor_recomputed` and the row records
    that the check ran. `latency_statement` carries the documented absence of a publication
    timestamp with the unverified-latency statement TE 7.0A stage 4 requires; it is required
    whenever `publication_timestamp` is empty. `availability_rule` records the recognised
    calendar-day rule (D-25) a feature declares INSTEAD of a scalar lag; `safe_lag_hours` is
    `None` exactly when such a rule is recorded, and never otherwise.
    """

    feature: str
    observation_timestamp: str
    publication_timestamp: str
    release_status: str
    safe_lag_hours: float | None
    actual_lag_hours: float
    anchor_policy: str | None = None
    latency_statement: str | None = None
    availability_rule: str | None = None
    lag_reference_instant: str | None = None
    selection_rule: str | None = None


# --- config ------------------------------------------------------------------------------


def _is_tbd(value: object) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == TBD_SENTINEL)


def read_availability_lags(snapshot: ConfigSnapshot) -> Mapping[str, Mapping[str, Any]]:
    """`features.availability_lags`: per feature EITHER `safe_lag_hours` OR a recognised
    `availability_rule` (D-25), plus `release_status_required`, optional `window` (`kind`,
    `days`, `source`, `recomputation_tolerance`; with a scalar lag, or with a rule in
    `AVAILABILITY_RULES_WITH_WINDOW` — A2) and optional `publication_latency_statement`.

    Raises
    ------
    FeatureAvailabilityError
        when the block is absent, `TBD — freeze gate`, not a mapping or empty; when a
        feature declares neither a valid scalar `safe_lag_hours` nor a recognised
        `availability_rule` (D-10.3's values are configuration frozen under their D-number,
        never a literal); when `availability_rule` is outside `AVAILABILITY_RULE_KINDS`;
        or when a rule-bearing feature also declares `safe_lag_hours`, or a `window`
        under a rule outside `AVAILABILITY_RULES_WITH_WINDOW`.
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
        rule = entry.get("availability_rule")
        window = entry.get("window")
        if "availability_rule" in entry:
            # D-25 route: a recognised rule identity REPLACES the scalar lag. The set is
            # closed, the scalar must be absent (not merely None), the rule is confined to
            # the rows its decision names, and a trailing window may ride on the rule ONLY
            # when the rule can derive the window's end day (A2: the D-25 rule can).
            if _is_tbd(rule):
                raise FeatureAvailabilityError(
                    f"{resource}.availability_rule",
                    "absent or unresolved (TBD — freeze gate); a rule identity is frozen "
                    "configuration under its D-number (D-25), never inferred here",
                )
            if not isinstance(rule, str) or rule not in AVAILABILITY_RULE_KINDS:
                raise FeatureAvailabilityError(
                    f"{resource}.availability_rule",
                    f"{rule!r} is not a recognised availability rule "
                    f"({sorted(AVAILABILITY_RULE_KINDS)}); the set is closed and an unknown "
                    f"kind is refused, never defaulted",
                )
            if "safe_lag_hours" in entry:
                raise FeatureAvailabilityError(
                    f"{resource}.safe_lag_hours",
                    f"declared alongside availability_rule {rule!r}; a feature carries a "
                    f"scalar lag OR a calendar-day rule, never both — a scalar cannot state "
                    f"the rule and two statements of one availability would disagree",
                )
            if str(feature) not in AVAILABILITY_RULE_SCOPE.get(rule, frozenset()):
                raise FeatureAvailabilityError(
                    f"{resource}.availability_rule",
                    f"{rule!r} governs only {sorted(AVAILABILITY_RULE_SCOPE.get(rule, ()))} "
                    f"(D-25 supplements D-21 and names the F10.7 daily median only); the GFZ "
                    f"rows keep scalar safe lags (D-10.3) and a calendar-day rule is never "
                    f"extended to them by configuration",
                )
            if window is not None and rule not in AVAILABILITY_RULES_WITH_WINDOW:
                raise FeatureAvailabilityError(
                    f"{resource}.window",
                    f"declared alongside availability_rule {rule!r}, which cannot derive a "
                    f"window end day; only {sorted(AVAILABILITY_RULES_WITH_WINDOW)} compose "
                    f"with a trailing window (A2)",
                )
            if window is not None:
                _validate_window_fields(resource, window)
            for forbidden_key in ("lag_reference_instant", "selection_rule"):
                if forbidden_key in entry:
                    raise FeatureAvailabilityError(
                        f"{resource}.{forbidden_key}",
                        f"declared alongside availability_rule {rule!r}; {forbidden_key} "
                        f"states the reference instant / selection mechanism for an "
                        f"INTERVAL-VALUED scalar-lag row (D-43/D-44) and has no meaning on "
                        f"a calendar-day rule row, whose own reference instant is fixed by "
                        f"the rule itself (D-25)",
                    )
            out[str(feature)] = entry
            continue
        if _is_tbd(lag):
            raise FeatureAvailabilityError(
                f"{resource}.safe_lag_hours",
                "absent or unresolved (TBD — freeze gate), and no availability_rule is "
                "declared; every feature carries a valid scalar safe lag OR a recognised "
                "rule, never neither",
            )
        if isinstance(lag, bool) or not isinstance(lag, int | float) or lag < 0:
            raise FeatureAvailabilityError(
                f"{resource}.safe_lag_hours", f"{lag!r} is not a non-negative number of hours"
            )
        # D-43/D-44: every scalar-lag (interval-valued, GFZ-style) row states BOTH the
        # reference instant its lag is measured from and the selection mechanism that
        # applies it -- required, not optional, and drawn from the same closed sets the
        # actual producer/consumer code implements (imported, never retyped).
        reference_instant = entry.get("lag_reference_instant")
        if _is_tbd(reference_instant):
            raise FeatureAvailabilityError(
                f"{resource}.lag_reference_instant",
                "absent or unresolved (TBD — freeze gate); D-43 fixes the safe lag's "
                "reference instant as the observation interval's END for every scalar-lag "
                "row, never a literal chosen here",
            )
        if reference_instant not in LAG_REFERENCE_INSTANT_KINDS:
            raise FeatureAvailabilityError(
                f"{resource}.lag_reference_instant",
                f"{reference_instant!r} is not a recognised reference instant "
                f"({sorted(LAG_REFERENCE_INSTANT_KINDS)}); the set is closed and an "
                f"unrecognised value is refused, never defaulted or silently honoured",
            )
        selection_rule = entry.get("selection_rule")
        if _is_tbd(selection_rule):
            raise FeatureAvailabilityError(
                f"{resource}.selection_rule",
                "absent or unresolved (TBD — freeze gate); D-44 fixes the ONE lagged-"
                "selection mechanism for every scalar-lag row, never a literal chosen here",
            )
        if selection_rule not in SELECTION_RULE_KINDS:
            raise FeatureAvailabilityError(
                f"{resource}.selection_rule",
                f"{selection_rule!r} is not a recognised selection rule "
                f"({sorted(SELECTION_RULE_KINDS)}); the set is closed and an unrecognised "
                f"value is refused, never defaulted or silently honoured",
            )
        if window is not None:
            _validate_window_fields(resource, window)
        out[str(feature)] = entry
    return out


def _validate_window_fields(resource: str, window: object) -> None:
    """The five frozen window fields must be present and resolved (scalar or rule row)."""
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
    # D-47: the recomputation certificate applies ONLY inside a stated numerical domain
    # (an applicability condition, never a physical maximum) -- required alongside the
    # tolerance it bounds, never left as an unchecked pass-through field.
    bound = window.get("recomputation_input_bound_sfu")
    if _is_tbd(bound):
        raise FeatureAvailabilityError(
            f"{resource}.window.recomputation_input_bound_sfu",
            "absent or unresolved (TBD — freeze gate); D-47's tolerance is certified only "
            "inside a stated |value| domain, frozen alongside the tolerance itself, never "
            "invented at read time",
        )
    if isinstance(bound, bool) or not isinstance(bound, int | float) or bound <= 0:
        raise FeatureAvailabilityError(
            f"{resource}.window.recomputation_input_bound_sfu",
            f"{bound!r} is not a positive number",
        )


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


def _rule_available_at(rule: str, observed: dt.datetime, *, resource: str) -> dt.datetime:
    """The instant a value observed at `observed` becomes available under `rule`.

    `previous_day_median_midnight_utc` (D-25): midnight UTC of the observation's UT day
    plus one day — `availability_ts(median(D)) = 00:00 UTC on D+1`, equivalently
    `availability_ts(median(D-1)) = 00:00 UTC on D`. A function of the observation DAY
    only, so every origin within one day sees the same instant.
    """
    if rule == AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC:
        next_day = observed.astimezone(_UTC).date() + dt.timedelta(days=1)
        return dt.datetime.combine(next_day, dt.time(0), tzinfo=_UTC)
    raise FeatureAvailabilityError(
        resource,
        f"availability rule {rule!r} is not recognised ({sorted(AVAILABILITY_RULE_KINDS)})",
    )


def _constituent_available_at(
    rule: str, observation_day: dt.date, *, resource: str
) -> dt.datetime:
    """The constituent availability time of the daily value observed on `observation_day`
    under `rule` — for D-25, 00:00 UTC of the following day. Distinct from the
    observation day itself, from the window end day, and from the forecast origin."""
    day_start = dt.datetime.combine(observation_day, dt.time(0), tzinfo=_UTC)
    return _rule_available_at(rule, day_start, resource=resource)


def latest_eligible_window_end(rule: str, origin: dt.datetime, *, resource: str) -> dt.date:
    """The latest observation day whose constituent is available at or before `origin`
    under `rule` — the only admissible trailing-window end day for that origin (A2).
    Derived, never conventional: walk back from the origin's own UT day until the
    constituent availability time is at or before the origin (at most two steps)."""
    candidate = origin.astimezone(_UTC).date()
    for _ in range(3):
        if _constituent_available_at(rule, candidate, resource=resource) <= origin:
            return candidate
        candidate -= dt.timedelta(days=1)
    raise FeatureAvailabilityError(
        resource, f"no observation day is available at origin {origin.isoformat()} under {rule!r}"
    )


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
    because the per-origin anchors live in these rows. A rule-bearing feature (D-25) has
    its availability instant raised to `max(observation/publication instant, rule
    instant)` — the rule is a floor, never a ceiling — and an origin BEFORE that instant
    (same-day or future-day anchoring) is refused here rather than recorded.

    Raises
    ------
    FeatureAvailabilityError
        a feature with no driver rows; a missing column; a publication timestamp absent
        with no documented-absence statement; mixed release grades within one series.
    LeakageError
        a centered window (limb 2); an anchor/recomputation failure (limb 3); a
        rule-bearing row whose origin precedes its rule availability instant.
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
        rule: str | None = entry.get("availability_rule")
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
            if rule is not None:
                # D-25: the rule can only make availability LATER, never earlier — a later
                # publication timestamp still governs through the max.
                rule_at = _rule_available_at(rule, observed, resource=resource)
                available_at = max(available_at, rule_at)
            lag = _hours(origin - available_at)
            if rule is not None and lag < 0:
                raise LeakageError(
                    resource,
                    f"forecast origin {origin.isoformat()} precedes the availability instant "
                    f"{available_at.isoformat()} under rule {rule!r} (observation day "
                    f"{observed.date().isoformat()}); a same-day or future-day anchor is "
                    f"forecast leakage by construction (D-25; FR-P1-04-2)",
                )
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
                safe_lag_hours=None if rule is not None else float(entry["safe_lag_hours"]),
                window_days=int(window["days"]),
                tolerance=float(window["recomputation_tolerance"]),
                availability_rule=rule,
                # D-47's applicability-domain check is wired into the REAL matrix build here
                # -- not merely available for a caller to remember to pass (the gap this
                # limb closes: the reader carried `recomputation_input_bound_sfu` through
                # unenforced until this call actually reads it).
                input_bound=float(window["recomputation_input_bound_sfu"]),
            )
            anchor_policy = (
                f"window ends at the latest observation day available under rule {rule!r}; "
                f"every constituent's availability verified; mean recomputed from anchor"
                if rule is not None
                else "window ends at the safe-lagged day; mean recomputed from anchor"
            )
        assert best_lag is not None
        rows.append(
            AvailabilityRow(
                feature=feature,
                observation_timestamp=best_obs,
                publication_timestamp=best_pub,
                release_status=next(iter(grades)),
                safe_lag_hours=None if rule is not None else float(entry["safe_lag_hours"]),
                actual_lag_hours=best_lag,
                anchor_policy=anchor_policy,
                latency_statement=latency_statement,
                availability_rule=rule,
                # D-43/D-44: recorded on the row so a downstream consumer (build_features)
                # can cross-check a driver's ACTUAL selection against what config declared,
                # rather than only against a hardcoded module constant.
                lag_reference_instant=None
                if rule is not None
                else entry.get("lag_reference_instant"),
                selection_rule=None if rule is not None else entry.get("selection_rule"),
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
        when any scalar-lag row has `actual_lag_hours < safe_lag_hours`; when a rule row
        carries an unrecognised rule or a negative measured lag; when a row carries
        neither a scalar lag nor a rule; when a row's
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
        if row.availability_rule is not None:
            if (
                row.availability_rule not in AVAILABILITY_RULE_KINDS
                or row.safe_lag_hours is not None
            ):
                raise LeakageError(
                    f"availability matrix: {row.feature}",
                    f"availability_rule {row.availability_rule!r} with safe_lag_hours "
                    f"{row.safe_lag_hours!r}; a row carries a recognised rule with no scalar "
                    f"lag, or a scalar lag with no rule, never another shape (D-25)",
                )
            if row.actual_lag_hours < 0:
                raise LeakageError(
                    f"availability matrix: {row.feature}",
                    f"actual lag {row.actual_lag_hours:.3f} h is negative under rule "
                    f"{row.availability_rule!r}; the origin precedes the rule's availability "
                    f"instant (D-25; FR-P1-04-2, NFR-LEAK-01)",
                )
            continue
        if row.safe_lag_hours is None:
            raise LeakageError(
                f"availability matrix: {row.feature}",
                "carries neither a scalar safe lag nor an availability rule; an unstated "
                "availability is not an availability (D-10.3; D-25)",
            )
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


def recomputation_tolerance_bound(*, window_days: int, input_bound: float) -> float:
    """The a-priori float64 bound on |recorded − recomputed| for a `window_days`-term mean
    of constituents with |value| ≤ `input_bound` (D-47): (N + 1) · ε · B with ε = 2⁻⁵²
    (machine epsilon, twice the unit round-off u), covering one rounding per parsed
    constituent, N − 1 sequential additions and one division — a rigorous bound with a
    factor ≈ 2 of margin over the first-order (N + 1)·u·B. Numerical agreement only:
    it says nothing about sensor accuracy. `input_bound` is an APPLICABILITY CONDITION
    of the certificate, never a physical maximum."""
    if window_days < 1 or input_bound <= 0:
        raise IntegrityError(
            "recomputation_tolerance_bound",
            f"window_days={window_days!r}, input_bound={input_bound!r}",
        )
    return (window_days + 1) * 2.0**-52 * float(input_bound)


def assert_recomputation_domain(
    daily_values: Mapping[dt.date, float], *, input_bound: float, feature: str
) -> None:
    """D-47's applicability check: every constituent the recomputation may read lies
    within the certified numerical domain |value| ≤ `input_bound`. A value outside it is
    NOT clipped, deleted or declared invalid — the numerical certificate simply does not
    cover it, so the certification FAILS clearly and a justified wider bound (its own
    decision) or a more accurate implementation is required; the tolerance is never
    raised silently."""
    outside = sorted(
        (day.isoformat(), float(value))
        for day, value in daily_values.items()
        if not math.isnan(float(value)) and abs(float(value)) > float(input_bound)
    )
    if outside:
        raise IntegrityError(
            f"availability_lags.{feature}.window.recomputation_input_bound",
            f"numerical certification FAILS: {len(outside)} constituent(s) exceed the certified "
            f"input domain |value| <= {input_bound!r} (first: {outside[0]}); the value is kept "
            f"unchanged — a justified bound under its own decision or a more accurate "
            f"implementation is required, never a silently raised tolerance (D-47)",
        )


def assert_anchor_recomputed(
    feature: str,
    rows: Sequence[Mapping[str, Any]],
    *,
    daily_values: Mapping[dt.date, float],
    safe_lag_hours: float | None,
    window_days: int,
    tolerance: float,
    availability_rule: str | None = None,
    input_bound: float | None = None,
) -> None:
    """Limb 3: for every origin, the recorded anchor IS the admissible window end day, and
    the mean recomputed from that anchor over `daily_values` agrees within `tolerance`.

    Two ways to fix the admissible end day, exactly one of which applies per feature:

    * scalar lag — the safe-lagged day `(origin − safe_lag_hours).date()` (unchanged);
    * availability rule (A2; D-25) — `latest_eligible_window_end`: the latest observation
      day whose CONSTITUENT AVAILABILITY TIME (00:00 UTC of the following day under D-25)
      is at or before the FORECAST ORIGIN. Every window day's constituent availability is
      then verified individually, so no constituent that is not yet available can enter.
      The daily source rows carry `day` and `value` only (no publication timestamp), so a
      later publication can only reach this limb through the trailing row's own
      `publication_timestamp`, which limb 1 honours via `max` (build_availability_matrix).

    Raises
    ------
    LeakageError
        a row without `anchor_day`/`mean_value`; an anchor that is not the admissible end
        day (an anchor AT the origin day passes limbs 1 and 2 while including same-day
        F10.7 — FR-P1-04-2's named hole; a stale earlier anchor is likewise refused); a
        constituent whose availability time is after the origin; or a recorded mean that
        differs from the recomputation (a recorded-but-wrong anchor whose values came from
        another window).
    IntegrityError
        propagated from `trailing_mean` when a window day is missing (TC-20: never fill);
        or when neither/both of `safe_lag_hours` and `availability_rule` are given.
    """
    if (safe_lag_hours is None) == (availability_rule is None):
        raise IntegrityError(
            f"availability_lags.{feature}",
            "the anchor limb takes exactly one of safe_lag_hours or availability_rule",
        )
    if availability_rule is not None and availability_rule not in AVAILABILITY_RULES_WITH_WINDOW:
        raise IntegrityError(
            f"availability_lags.{feature}.availability_rule",
            f"{availability_rule!r} cannot derive a window end day",
        )
    if tolerance < 0:
        raise IntegrityError(
            f"availability_lags.{feature}.window.recomputation_tolerance",
            f"{tolerance!r} is negative",
        )
    if input_bound is not None:
        # D-47: the certificate applies only inside its stated input domain.
        assert_recomputation_domain(daily_values, input_bound=input_bound, feature=feature)
    for index, record in enumerate(rows):
        resource = f"{feature} row {index}"
        if _is_missing(record.get("anchor_day")) or _is_missing(record.get("mean_value")):
            raise LeakageError(
                resource,
                "trailing-mean row carries no `anchor_day` or `mean_value`; the anchor is a "
                "recorded field, and the third limb cannot run over an unrecorded anchor",
            )
        origin = _as_utc(record["forecast_origin"], resource=f"{resource}.forecast_origin")
        if availability_rule is not None:
            expected_anchor = latest_eligible_window_end(
                availability_rule, origin, resource=resource
            )
            basis = f"the latest observation day available under {availability_rule!r}"
        else:
            assert safe_lag_hours is not None  # noqa: S101 — exclusivity checked above
            expected_anchor = (origin - dt.timedelta(hours=safe_lag_hours)).date()
            basis = "the safe-lagged day"
        recorded_anchor = _as_date(record["anchor_day"], resource=f"{resource}.anchor_day")
        if recorded_anchor != expected_anchor:
            raise LeakageError(
                resource,
                f"trailing window ends at {recorded_anchor.isoformat()} but {basis} for "
                f"origin {origin.isoformat()} is {expected_anchor.isoformat()}; a trailing "
                f"mean ending at day t passes the not-centered check and the lag assertion "
                f"while including same-day F10.7, and a stale end day silently drops the "
                f"latest available constituent (FR-P1-04-2, third limb)",
            )
        if availability_rule is not None:
            # Defence in depth, redundant under the supported contract and KEPT deliberately
            # (A2 mutant disposition, `CR-2026-09-19-SCI-REVIEW`): the daily source rows
            # carry `day` and `value` only — no per-day publication timestamp exists — and
            # every recognised rule is monotone in the observation day (pinned by
            # `test_d25_constituent_availability_is_monotone_so_the_anchor_bounds_the_window`),
            # so once `recorded_anchor == expected_anchor` no earlier window day can become
            # available after the origin. The loop would only bite for a future rule kind
            # that is not monotone; removing it would silently rely on that property.
            for offset in range(window_days):
                day = recorded_anchor - dt.timedelta(days=offset)
                available_at = _constituent_available_at(availability_rule, day, resource=resource)
                if available_at > origin:
                    raise LeakageError(
                        resource,
                        f"window constituent observed on {day.isoformat()} becomes available "
                        f"at {available_at.isoformat()}, after the forecast origin "
                        f"{origin.isoformat()} (D-25; FR-P1-04-2)",
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
