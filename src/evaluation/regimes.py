"""R1 regimes: ONE hour-classifier, ONE counting path, the December guards (R-123, R-124).

Purpose
-------
`regimes-diagnostics-reporting` W-1/W-2: exactly one hour-classification function labels
hours quiet/disturbed/storm from the configured Vision §9.3 thresholds, and
``count_storm_events`` is the ONLY counting path, implementing D-13's event definition (a
contiguous Kp>=5 interval) and independence rule (>=24 h of Kp<4). Every consumer in this
unit calls these and never reclassifies. No threshold, window, independence or count
literal exists in this module (TC-03e; FR-P1-05-18 clause 3 by construction): the values
arrive from `configs/experiment.yaml`'s `regimes` block through `ConfigSnapshot`.

December discipline (W-2; ML-02): the classifier consumes ONLY the Kp driver series and
configured thresholds — December-blind by signature, no date filtering hidden inside. The
storm count reaching any report is READ from the registered pre-G-05 audit artifact
(``read_audit_storm_count``), never recomputed as the guard's input; the post-receipt
comparison count exists for divergence detection only (control (31),
``assert_audit_count_consistency`` raises rather than adjudicating). A storm event wholly
outside the D-28 scored set is reported separately and never counts toward D-13's >=3
threshold (control (40), ``assert_events_eligible_for_threshold``). The H4/SRQ-5 demotion
record's timestamp must precede the G-05 freeze (control (6),
``assert_demotion_precedes_freeze``).

Exception declaration note (recorded, not hidden — the guards.py precedent):
`domain-entities.md` § 5 places `RegimeError`'s declaration "here
(`src/evaluation/regimes.py`)". It was written before `foundation`'s R-01 amendment ruled
`src/data/config.py` the ONE declaration site, and `RegimeError` ALREADY EXISTS there. A
second class object with the same name would break catchability, so this module IMPORTS
and RE-EXPORTS it from the R-01 declaration site rather than redeclaring it; this unit
remains its raise site (CHANGE_RECORD_2026-09-06_R123_regimes_and_reporting.md § 4).

Configured-values delivery (recorded design choice): `count_storm_events`'s signature is
the approved cross-package boundary call, consumed exactly with NO signature amendment —
it carries no config parameter. R-15 bars this unit from reading `configs/` itself, so the
resolved `regimes` block is activated once per run by the producing path via
``activate_regime_config(snapshot.experiment)`` (module-level state, the
`_REEXEC_PERFORMED` precedent in `src/data/config.py`); an unactivated call REFUSES
fail-closed naming the block. Intra-package callables take the config explicitly.

Inputs
------
Hourly Kp records: a sequence of mappings (or `src.data.splits.RecordFrame`) each carrying
`interval_start_utc` (ISO-8601, UTC) and `kp` (float), optionally with frame `attrs`
carrying provenance (`derived_from`); the parsed `experiment` mapping off `ConfigSnapshot`;
the registered pre-G-05 audit artifact mapping (`inventory-and-registry`'s read). No
`src/features`, `src/models` or `src/external` import, direct or transitive (TE §12; D-27).

Re-run behaviour
----------------
Pure computation; nothing is persisted; deterministic given identical inputs. Every
refusal raises an `IntegrityError` subclass naming the resource and the violated
expectation (R-01's constructor contract).

Governance
----------
Vision §9.3; D-13; D-11 (provisional Dst barred from any G-05 regime count — the
`.dst_summary.json` material must not supply the figure); D-28 (the 30-day scored set);
`GOV-2026-08-28-FD-01` Rec 15 (asserted day range; value routed to the gate, Student +
Supervisor). No scientific value is decided here; the `december_day_range` field refuses
while its `TBD — freeze gate` sentinel stands (TE §18.3, stop-and-report).
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from src.data.config import TBD_SENTINEL, RegimeError

__all__ = [
    "GFZ_SOURCES",
    "REGIME_LABELS",
    "RegimeError",
    "RegimeConfig",
    "read_regime_config",
    "activate_regime_config",
    "active_regime_config",
    "reset_regime_config",
    "classify_hours",
    "count_storm_events",
    "assert_event_window",
    "read_december_day_range",
    "read_audit_storm_count",
    "assert_audit_count_consistency",
    "assert_demotion_precedes_freeze",
    "eligible_storm_events",
    "assert_events_eligible_for_threshold",
]

#: The two accepted count sources (D-13 "Source of the count": GFZ Kp/ap3 and Hp60/ap60 at
#: a single recorded release grade). Identity tokens, not scientific constants.
GFZ_SOURCES: tuple[str, ...] = ("GFZ Kp", "GFZ Hp60", "GFZ Kp/Hp60")

#: The three regime labels (Vision §9.3). Identity tokens.
REGIME_LABELS: tuple[str, ...] = ("quiet", "disturbed", "storm")

#: The workspace custody item D-11/D-13 name as exactly the path of least resistance the
#: provisional-Dst control closes. An identity token naming a file, not a data source.
_DST_SUMMARY_PATH: str = ".dst_summary.json"


@dataclass(frozen=True)
class RegimeConfig:
    """The resolved `regimes` block — frozen values encoded upstream, decided nowhere here."""

    quiet_kp_below: float
    disturbed_kp_min: float
    storm_kp_min: float
    window_pre_hours: int
    window_post_hours: int
    independence_min_quiet_hours: int
    event_threshold: int
    december_day_range: object
    quality_strata_fields: tuple[str, ...]


_ACTIVE_CONFIG: RegimeConfig | None = None


def _require(block: Mapping[str, Any], key: str, resource: str) -> Any:
    if not isinstance(block, Mapping) or key not in block:
        raise RegimeError(
            resource,
            f"required field {key!r} is absent; the regime configuration encodes frozen "
            f"values and decides nothing (R-123; Vision §9.3; D-13) — an absent field "
            f"refuses rather than defaulting (TE §18.3)",
        )
    return block[key]


def read_regime_config(experiment: Mapping[str, Any]) -> RegimeConfig:
    """Resolve the `regimes` block off `ConfigSnapshot.experiment` (R-123; TC-03e).

    Validates internal coherence only — the disturbed floor equals the quiet ceiling
    (Vision §9.3's complementary boundary) and the storm floor is not below the disturbed
    floor — and NEVER compares against a literal threshold: the copy's exactness is
    asserted by test against the change record's citation table, not re-encoded here.

    Raises
    ------
    RegimeError
        the block or any required field absent; an incoherent boundary; a non-positive
        window, independence span or event threshold.
    """
    resource = "configs/experiment.yaml regimes"
    block = experiment.get("regimes")
    if not isinstance(block, Mapping):
        raise RegimeError(
            resource,
            "the regimes block is absent; R-123's classifier reads its thresholds and "
            "window from configuration only, so no classification or count can run "
            "without it (TC-03e; Q1 = A transcription)",
        )
    thresholds = _require(block, "thresholds", resource)
    window = _require(block, "event_window", resource)
    quiet = float(_require(thresholds, "quiet_kp_below", resource))
    disturbed = float(_require(thresholds, "disturbed_kp_min", resource))
    storm = float(_require(thresholds, "storm_kp_min", resource))
    if disturbed != quiet:
        raise RegimeError(
            resource,
            f"disturbed_kp_min ({disturbed}) does not equal quiet_kp_below ({quiet}); "
            f"Vision §9.3's quiet/disturbed boundary is complementary (Kp<x quiet, Kp>=x "
            f"disturbed) and a gap or overlap would leave hours unlabelled or double-"
            f"labelled",
        )
    if storm < disturbed:
        raise RegimeError(
            resource,
            f"storm_kp_min ({storm}) is below disturbed_kp_min ({disturbed}); a storm "
            f"hour is a disturbed hour by Vision §9.3's ordering",
        )
    pre = int(_require(window, "pre_hours", resource))
    post = int(_require(window, "post_hours", resource))
    independence = int(_require(block, "independence_min_quiet_hours", resource))
    threshold = int(_require(block, "independent_storm_event_threshold", resource))
    if pre <= 0 or post <= 0 or independence <= 0 or threshold <= 0:
        raise RegimeError(
            resource,
            f"event_window ({pre}/{post}), independence_min_quiet_hours ({independence}) "
            f"and independent_storm_event_threshold ({threshold}) must all be positive; "
            f"a non-positive frozen value is a transcription defect, not a choice",
        )
    strata = _require(block, "d17_quality_strata", resource)
    fields = tuple(str(f) for f in _require(strata, "fields", resource))
    if not fields:
        raise RegimeError(
            resource,
            "d17_quality_strata.fields is empty; the strata surface is an enumerated set "
            "from config (D-17; R-127) and an empty enumeration bars every stratum",
        )
    return RegimeConfig(
        quiet_kp_below=quiet,
        disturbed_kp_min=disturbed,
        storm_kp_min=storm,
        window_pre_hours=pre,
        window_post_hours=post,
        independence_min_quiet_hours=independence,
        event_threshold=threshold,
        december_day_range=block.get("december_day_range"),
        quality_strata_fields=fields,
    )


def activate_regime_config(experiment: Mapping[str, Any]) -> RegimeConfig:
    """Resolve and activate the module-level config `count_storm_events` reads.

    The approved boundary signature carries no config parameter and is consumed with no
    amendment, so the producing path activates the resolved block once per run (see the
    module docstring's recorded design choice). Re-activation with identical content is
    idempotent; different content replaces it (a run that needs different configuration
    is a different run — `ConfigSnapshot`'s own rule).
    """
    global _ACTIVE_CONFIG
    _ACTIVE_CONFIG = read_regime_config(experiment)
    return _ACTIVE_CONFIG


def active_regime_config() -> RegimeConfig:
    """The activated config, or a fail-closed refusal naming the block (TE §18.3)."""
    if _ACTIVE_CONFIG is None:
        raise RegimeError(
            "configs/experiment.yaml regimes",
            "no regime configuration is activated; call activate_regime_config("
            "snapshot.experiment) on the producing path before count_storm_events — the "
            "thresholds arrive from configuration only, never from a default (R-123)",
        )
    return _ACTIVE_CONFIG


def reset_regime_config() -> None:
    """Clear the activation (test apparatus; a fresh run activates its own snapshot)."""
    global _ACTIVE_CONFIG
    _ACTIVE_CONFIG = None


# --- the one classifier (W-1; December-blind by signature) -------------------------------


def _as_utc(value: Any, *, resource: str) -> dt.datetime:
    if isinstance(value, dt.datetime):
        stamp = value
    else:
        text = str(value).strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            stamp = dt.datetime.fromisoformat(text)
        except ValueError as exc:
            raise RegimeError(resource, f"timestamp {value!r} is not ISO-8601") from exc
    if stamp.tzinfo is None:
        return stamp.replace(tzinfo=dt.UTC)
    return stamp.astimezone(dt.UTC)


def _kp_rows(kp: Any) -> list[tuple[dt.datetime, float]]:
    rows: list[tuple[dt.datetime, float]] = []
    for row in kp:
        stamp = _as_utc(row["interval_start_utc"], resource="kp series row")
        rows.append((stamp, float(row["kp"])))
    rows.sort(key=lambda item: item[0])
    return rows


def classify_hours(
    kp: Sequence[Mapping[str, Any]], *, config: RegimeConfig
) -> list[dict[str, Any]]:
    """W-1's one hour-classification function: quiet | disturbed | storm, from config only.

    December-blind BY SIGNATURE: the inputs are the Kp driver series and the configured
    thresholds — never a target, a prediction, a partition or a date filter. Labels are
    boundary-exact: an hour at exactly the disturbed floor is disturbed, at exactly the
    storm floor is storm (Vision §9.3's >= boundaries).

    Raises
    ------
    RegimeError
        a row without a parseable timestamp or Kp value.
    """
    labelled: list[dict[str, Any]] = []
    for stamp, value in _kp_rows(kp):
        if value >= config.storm_kp_min:
            label = "storm"
        elif value >= config.disturbed_kp_min:
            label = "disturbed"
        else:
            label = "quiet"
        labelled.append(
            {"interval_start_utc": stamp.isoformat(), "kp": value, "regime": label}
        )
    return labelled


# --- the one counting path (W-1; the approved boundary contract) -------------------------


def _refuse_dst_derived(kp: Any, *, context: str) -> None:
    attrs = getattr(kp, "attrs", None)
    derived = str(attrs.get("derived_from", "")) if isinstance(attrs, Mapping) else ""
    if "dst" in derived.lower():
        raise RegimeError(
            context,
            f"the input series is derived from Dst material ({derived!r}); D-11 bars any "
            f"provisional-Dst-derived figure from a G-05 regime count, and "
            f"{_DST_SUMMARY_PATH!r} is exactly the path of least resistance this control "
            f"closes — the count comes from GFZ Kp/Hp60 at a recorded release grade or it "
            f"does not exist (D-13; R-62 restriction 3)",
        )


def count_storm_events(
    kp: Any,
    *,
    release_grade: str,
    source: str,
) -> tuple[int, tuple[tuple[str, str], ...]]:
    """The ONLY counting path (R-123), the approved boundary call consumed exactly.

    D-13's definitions, from the activated configuration: a storm event is a contiguous
    interval of hours at or above the storm floor; two events are independent if separated
    by at least the configured span of hours below the quiet ceiling (Kp<4). Only RECORDED
    hours count toward independence — a gap in the series is never assumed quiet. Returns
    the independent-event count and, per independent event, its (start, end-exclusive)
    ISO-8601 interval spanning any merged non-independent runs.

    Raises
    ------
    RegimeError
        `source` not GFZ Kp/Hp60; `release_grade` absent, empty or unresolved; a
        provisional-Dst-derived input (naming `.dst_summary.json`); no activated regime
        configuration.
    """
    context = f"count_storm_events(source={source!r})"
    if source not in GFZ_SOURCES:
        hint = (
            f"; a Dst-derived series ({_DST_SUMMARY_PATH!r} included) may never supply a "
            f"G-05 regime count (D-11)"
            if "dst" in str(source).lower()
            else ""
        )
        raise RegimeError(
            context,
            f"source {source!r} is not GFZ Kp/Hp60 ({sorted(GFZ_SOURCES)}); the §9.3 "
            f"count cannot be computed from an unrecorded or provisional-Dst-derived "
            f"series without that appearing at the call site (D-13; approved contract)"
            + hint,
        )
    if not release_grade or str(release_grade).strip() in ("", TBD_SENTINEL):
        raise RegimeError(
            context,
            "release_grade is absent or unresolved; the count comes from GFZ Kp/Hp60 at a "
            "RECORDED release grade (D-13 'Source of the count'; approved contract)",
        )
    _refuse_dst_derived(kp, context=context)
    config = active_regime_config()

    rows = _kp_rows(kp)
    hour = dt.timedelta(hours=1)

    # Contiguous Kp>=storm runs (contiguity = adjacent hourly timestamps).
    runs: list[tuple[dt.datetime, dt.datetime]] = []
    run_start: dt.datetime | None = None
    prev_stamp: dt.datetime | None = None
    for stamp, value in rows:
        is_storm = value >= config.storm_kp_min
        contiguous = prev_stamp is not None and stamp - prev_stamp == hour
        if is_storm:
            if run_start is None or not contiguous:
                if run_start is not None:
                    runs.append((run_start, prev_stamp + hour))  # type: ignore[operator]
                run_start = stamp
        elif run_start is not None:
            runs.append((run_start, prev_stamp + hour))  # type: ignore[operator]
            run_start = None
        prev_stamp = stamp
    if run_start is not None and prev_stamp is not None:
        runs.append((run_start, prev_stamp + hour))

    # Independence: >= configured hours of RECORDED Kp<quiet-ceiling between runs.
    events: list[tuple[dt.datetime, dt.datetime]] = []
    for run in runs:
        if not events:
            events.append(run)
            continue
        prev_start, prev_end = events[-1]
        quiet_hours = sum(
            1
            for stamp, value in rows
            if prev_end <= stamp < run[0] and value < config.quiet_kp_below
        )
        if quiet_hours >= config.independence_min_quiet_hours:
            events.append(run)
        else:
            events[-1] = (prev_start, run[1])
    intervals = tuple((start.isoformat(), end.isoformat()) for start, end in events)
    return len(intervals), intervals


def assert_event_window(pre_hours: int, post_hours: int, *, config: RegimeConfig) -> None:
    """Control (2): an event window of any span other than the configured one FAILS.

    Raises
    ------
    RegimeError
        the offered (pre, post) span differs from the configured −pre/+post window.
    """
    if (pre_hours, post_hours) != (config.window_pre_hours, config.window_post_hours):
        raise RegimeError(
            "regime event window",
            f"offered window (−{pre_hours} h/+{post_hours} h) differs from the configured "
            f"(−{config.window_pre_hours} h/+{config.window_post_hours} h); the reporting "
            f"window is Vision §9.3's frozen value, read from configuration only "
            f"(FR-P1-05-18 clause 4)",
        )


# --- the December guards (W-2) -----------------------------------------------------------


def read_december_day_range(config: RegimeConfig) -> tuple[dt.date, dt.date]:
    """The EXPLICITLY CONFIGURED December day range, asserted at the call site (Rec 15).

    The value is a Student + Supervisor gate item; while `december_day_range` carries the
    `TBD — freeze gate` sentinel (or is absent) this function REFUSES naming the field —
    the mechanism is built, the value is routed (TE §18.3; W-2 point 5).

    Accepted frozen forms: a mapping with `start`/`end` ISO dates, or a string
    `"YYYY-MM-DD..YYYY-MM-DD"` (end inclusive).

    Raises
    ------
    RegimeError
        sentinel, absent, or unparseable.
    """
    resource = "configs/experiment.yaml regimes.december_day_range"
    raw = config.december_day_range
    if raw is None or (isinstance(raw, str) and raw.strip() == TBD_SENTINEL):
        raise RegimeError(
            resource,
            "the December day range governing D-13's comparison count is not frozen; it "
            "is a Student + Supervisor gate item (GOV-2026-08-28-FD-01 Rec 15) and this "
            "stage may not fill it by convenience (TE §18.3) — the audit-count "
            "consistency check refuses until the freeze lands",
        )
    if isinstance(raw, Mapping):
        start_text, end_text = str(raw.get("start", "")), str(raw.get("end", ""))
    else:
        text = str(raw)
        if ".." not in text:
            raise RegimeError(resource, f"unparseable day range {raw!r}")
        start_text, end_text = (part.strip() for part in text.split("..", 1))
    try:
        start, end = dt.date.fromisoformat(start_text), dt.date.fromisoformat(end_text)
    except ValueError as exc:
        raise RegimeError(resource, f"unparseable day range {raw!r} ({exc})") from exc
    if end < start:
        raise RegimeError(resource, f"day range end {end} precedes start {start}")
    return start, end


def read_audit_storm_count(audit: Mapping[str, Any]) -> tuple[int, str]:
    """R-124: the storm count reaching any report is READ from the REGISTERED pre-G-05
    audit artifact — `inventory-and-registry`'s performance-blind read — never recomputed
    here as the guard's input. Returns (count, artifact_id).

    Raises
    ------
    RegimeError
        an unregistered artifact, an absent count, or a count whose recorded source is
        Dst-derived (D-11).
    """
    artifact_id = str(audit.get("artifact_id", "")) if isinstance(audit, Mapping) else ""
    resource = f"registered pre-G-05 audit artifact {artifact_id or '<no id>'}"
    if not isinstance(audit, Mapping) or not artifact_id or not audit.get("registered"):
        raise RegimeError(
            resource,
            "the pre-G-05 December regime-count audit artifact is absent, carries no "
            "artifact_id, or is not marked registered; the registered count is the storm "
            "guard's SOLE governing input (D-13's one measured quantity; Vision §8.3; "
            "R-124) and an unregistered count is no count",
        )
    if "storm_event_count" not in audit:
        raise RegimeError(
            resource,
            "storm_event_count is absent from the registered audit artifact; the "
            "descriptive-only guard reads the recorded count, never recomputes it (R-124)",
        )
    recorded_source = str(audit.get("count_source", ""))
    if "dst" in recorded_source.lower():
        raise RegimeError(
            resource,
            f"the registered count records a Dst-derived source ({recorded_source!r}); "
            f"D-11 bars any provisional-Dst figure from a G-05 regime count",
        )
    return int(audit["storm_event_count"]), artifact_id


def assert_audit_count_consistency(
    *,
    registered_count: int,
    comparison_count: int,
    audit_artifact_id: str,
    kp_resource: str,
) -> None:
    """Control (31): a registered audit count and this unit's post-receipt comparison
    count over the same Kp series and asserted day range that disagree RAISE — naming both
    counts and the artifact — rather than silently preferring either. This unit does not
    adjudicate; the disagreement surfaces at the gate.

    Raises
    ------
    RegimeError
        on divergence.
    """
    if registered_count != comparison_count:
        raise RegimeError(
            f"registered pre-G-05 audit artifact {audit_artifact_id}",
            f"records {registered_count} independent storm event(s) while this unit's "
            f"comparison count over {kp_resource} is {comparison_count}; D-13 collapsed "
            f"H4's fate and the storm-claim guard onto ONE measured quantity, and a "
            f"divergence is adjudicated at the gate, never resolved here (R-124 control "
            f"(31))",
        )


def assert_demotion_precedes_freeze(
    demotion_record: Mapping[str, Any], *, g05_freeze_utc: Any
) -> None:
    """Control (6): the H4/SRQ-5 demotion record's timestamp precedes the G-05 freeze; a
    post-freeze demotion FAILS rather than being corrected (FR-P1-05-18 clause 2).

    Raises
    ------
    RegimeError
        an absent timestamp, or one that does not precede the freeze.
    """
    record_id = str(demotion_record.get("record_id", "<no id>"))
    resource = f"H4/SRQ-5 demotion record {record_id}"
    recorded = demotion_record.get("recorded_at_utc")
    if not recorded:
        raise RegimeError(resource, "recorded_at_utc is absent; an undated demotion is unordered")
    recorded_at = _as_utc(recorded, resource=resource)
    freeze_at = _as_utc(g05_freeze_utc, resource="G-05 freeze timestamp")
    if not recorded_at < freeze_at:
        raise RegimeError(
            resource,
            f"demotion recorded at {recorded_at.isoformat()} does not precede the G-05 "
            f"freeze at {freeze_at.isoformat()}; the demotion is recorded BEFORE the "
            f"freeze or it fails (D-13; FR-P1-05-18 clause 2)",
        )


def eligible_storm_events(
    events: Sequence[tuple[str, str]], *, scored_start: dt.date, scored_end: dt.date
) -> tuple[tuple[tuple[str, str], ...], tuple[tuple[str, str], ...]]:
    """Rec 15's exclusion split: (eligible, wholly-outside) against the scored day range.

    An event is wholly outside when its entire interval falls outside
    [scored_start, scored_end] (end-inclusive days). Wholly-outside events are REPORTED
    SEPARATELY on the DEC regime rows and never count toward D-13's threshold.
    """
    window_start = dt.datetime.combine(scored_start, dt.time(0), tzinfo=dt.UTC)
    window_end = dt.datetime.combine(
        scored_end + dt.timedelta(days=1), dt.time(0), tzinfo=dt.UTC
    )
    eligible: list[tuple[str, str]] = []
    outside: list[tuple[str, str]] = []
    for start_text, end_text in events:
        start = _as_utc(start_text, resource="storm event interval")
        end = _as_utc(end_text, resource="storm event interval")
        if end <= window_start or start >= window_end:
            outside.append((start_text, end_text))
        else:
            eligible.append((start_text, end_text))
    return tuple(eligible), tuple(outside)


def assert_events_eligible_for_threshold(
    counted_events: Sequence[tuple[str, str]],
    *,
    scored_start: dt.date,
    scored_end: dt.date,
) -> None:
    """Control (40): a storm event wholly outside the scored set counted toward D-13's
    >=3 threshold FAILS, naming the event interval, the scored range and the violated
    threshold. Executable whichever day range is frozen — it tests the exclusion rule,
    not the range value.

    Raises
    ------
    RegimeError
        any counted event wholly outside the scored range.
    """
    _, outside = eligible_storm_events(
        counted_events, scored_start=scored_start, scored_end=scored_end
    )
    if outside:
        raise RegimeError(
            f"storm event {outside[0][0]}..{outside[0][1]}",
            f"falls wholly outside the scored set {scored_start.isoformat()}.."
            f"{scored_end.isoformat()} and was counted toward D-13's >=3 independent-"
            f"storm-event threshold; a wholly-outside event is reported separately and "
            f"never counts (GOV-2026-08-28-FD-01 Rec 15; R-124 control (40))",
        )

