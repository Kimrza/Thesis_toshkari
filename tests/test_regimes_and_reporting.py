"""R-132's one home: every named regimes/diagnostics/plots/checklist control (1)-(40)'s
render-side set, each proving the violation is CAUGHT (team.md § Testing Posture), plus
the must-NOT-fire controls.

PURPOSE. `regimes-diagnostics-reporting` R-123 ... R-131: classifier boundary controls,
the one-counting-path refusals (non-GFZ source, absent grade, provisional-Dst input
naming `.dst_summary.json` — the fixture NAMES the path, nothing reads that file), the
audit-count consistency raise (31), December-blind-by-signature evidence, the TEN render
guards per entry point (W-3 table, W-5 breakdowns, W-7 plots manifest, W-4 checklist),
the diagnostics quarantine, the claims checklist over the registered conclusion-surface
set, and static scans of the four governed notebook skeletons.

INPUTS. Synthetic fixtures only, mirroring `tests/test_common_masks.py`'s stdlib stand-in
approach: `src.data.splits.RecordFrame` record sequences, a SYNTHETIC year (2001 — never
2022, so no test can brush the locked month), and in-memory artifact mappings. Scientific
values (thresholds, window, D-13 count) arrive FROM configs/experiment.yaml even under
test (TC-03e): the regimes block is re-read from the real file at test time — via pyyaml
when importable, else a minimal stdlib fallback parser for exactly that block (test
apparatus; pyyaml is absent on the scratchpad smoke interpreter). Fixture Kp values are
DERIVED from the config-read thresholds, never literal. The one transcription-exactness
test asserts the Q1 = A copy against the change record's citation table — the copy's
exactness being the only new claim that transcription makes.

WHAT NO TEST HERE DISCHARGES. WS-19, TA-16, TA-20 stay `Pending`; the five D-32 rows stay
approved-never-run (NOT evidence); FR-P1-05-14/-15 stay rowless; BLK-03/04/08/09 stay
open; G-05/G-06 stay `Blocked`; the December day range stays a Student + Supervisor gate
item (its refusal is itself tested); control (29)'s EXECUTED per-notebook stop assertion
stays owed to an environment with a Jupyter kernel — the helper's stop is tested here,
the notebooks are statically scanned only.

Run: pytest tests/test_regimes_and_reporting.py -rs
"""

from __future__ import annotations

import ast
import datetime as dt
import inspect
import json
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import FairnessError, RegimeError, TBD_SENTINEL  # noqa: E402
from src.data.splits import RecordFrame  # noqa: E402
from src.evaluation import diagnostics, plots, regimes, report_guards  # noqa: E402
from src.evaluation.diagnostics import (  # noqa: E402
    D8_CLAIM_BOUNDARY,
    assert_breakdown_inventory,
    assert_breakdown_stamps,
    assert_descriptive_only_label,
    assert_fold_table,
    assert_grade_eligible,
    assert_headline_role,
    assert_no_diagnostic_field,
    assert_per_seed_stability,
    assert_post_access_labelled,
    build_breakdown_artifact,
    build_claims_checklist,
    build_dec_regime_breakdown,
    build_dst_diagnostic,
    build_primary_table,
    build_quality_stratum,
    compute_member_metrics,
    declare_notebook_inputs,
    derived_rmse_reduction,
    practical_relevance_statement,
    register_notebook_conclusion,
    rf_importance_figure_source,
    top1pct_sensitivity_block,
)
from src.evaluation.metrics import (  # noqa: E402
    PHASE2_NOT_INDEPENDENT_STATEMENT,
    SIGN_CONVENTION_SENTENCE,
    SPATIAL_REPRESENTATIVENESS_SENTENCE,
)
from src.evaluation.plots import (  # noqa: E402
    REQUIRED_PLOT_KINDS,
    assert_manifest_complete,
    assert_manifest_entry,
    build_plot_manifest_entry,
)
from src.evaluation.regimes import (  # noqa: E402
    assert_audit_count_consistency,
    assert_demotion_precedes_freeze,
    assert_event_window,
    assert_events_eligible_for_threshold,
    classify_hours,
    count_storm_events,
    eligible_storm_events,
    read_audit_storm_count,
    read_december_day_range,
    read_regime_config,
)
from src.evaluation.report_guards import (  # noqa: E402
    DRIVER_IDENTITY_CAVEAT,
    ConclusionSurfaceRegistry,
    emit_registered_artifact,
    require_beats_model,
    require_derived_label,
    require_driver_caveat,
    require_lineage_caveat,
    require_provenance_block,
    require_registered_surface,
)

UTC = dt.UTC
SYNTH_YEAR = 2001  # fixture year; never 2022, so no test can brush the locked month


# --- the regimes block, re-read from the REAL config at test time (TC-03e) ---------------


def _parse_regimes_fallback(text: str) -> dict[str, Any]:
    """Minimal stdlib parser for exactly the `regimes:` block (test apparatus: pyyaml is
    absent on the scratchpad smoke interpreter; when yaml imports, it is used instead)."""

    def _value(raw: str) -> Any:
        raw = raw.strip()
        if raw.startswith("["):
            inner = raw.strip("[]")
            return [part.strip().strip("\"'") for part in inner.split(",") if part.strip()]
        raw = raw.strip("\"'")
        try:
            return int(raw)
        except ValueError:
            return raw

    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("regimes:"))
    block: dict[str, Any] = {}
    current: dict[str, Any] = block
    for line in lines[start + 1 :]:
        if line.strip().startswith("#"):
            continue
        if line and not line.startswith(" "):
            break  # next top-level key
        content = line.split(" #", 1)[0].rstrip()
        if not content.strip():
            continue
        indent = len(content) - len(content.lstrip())
        key, _, rest = content.strip().partition(":")
        if indent == 2:
            if rest.strip():
                block[key] = _value(rest)
                current = block
            else:
                block[key] = {}
                current = block[key]
        elif indent >= 4:
            current[key] = _value(rest)
    return {"regimes": block}


def _load_experiment() -> dict[str, Any]:
    text = (REPO_ROOT / "configs" / "experiment.yaml").read_text(encoding="utf-8")
    try:
        import yaml

        return dict(yaml.safe_load(text))
    except ImportError:
        return _parse_regimes_fallback(text)


EXPERIMENT = _load_experiment()
CONFIG = read_regime_config(EXPERIMENT)

#: A synthetic experiment carrying a FROZEN day range (test APPARATUS over the synthetic
#: year — the real field is `TBD — freeze gate`, a Student + Supervisor gate item, and its
#: refusal is itself tested below; this stand-in exercises the mechanism only).
SYNTH_EXPERIMENT: dict[str, Any] = {
    "regimes": {
        **{k: v for k, v in EXPERIMENT["regimes"].items()},
        "december_day_range": {
            "start": f"{SYNTH_YEAR}-12-02",
            "end": f"{SYNTH_YEAR}-12-31",
        },
    }
}

STORM_KP = float(CONFIG.storm_kp_min)  # derived from config, never literal
DISTURBED_KP = float(CONFIG.disturbed_kp_min)
QUIET_KP = float(CONFIG.quiet_kp_below) - 1.0


def _kp_frame(rows: list[tuple[dt.datetime, float]], **attrs: Any) -> RecordFrame:
    frame = RecordFrame(
        {"interval_start_utc": stamp.isoformat(), "kp": value} for stamp, value in rows
    )
    frame.attrs.update(attrs)
    return frame


def _hourly(start: dt.datetime, values: list[float]) -> list[tuple[dt.datetime, float]]:
    return [(start + dt.timedelta(hours=i), v) for i, v in enumerate(values)]


def _event_series(
    *, events: int, storm_hours: int = 3, quiet_gap_hours: int | None = None
) -> RecordFrame:
    """Contiguous storm runs separated by RECORDED quiet gaps, values from config."""
    gap = (
        quiet_gap_hours
        if quiet_gap_hours is not None
        else CONFIG.independence_min_quiet_hours
    )
    rows: list[tuple[dt.datetime, float]] = []
    cursor = dt.datetime(SYNTH_YEAR, 12, 10, 0, tzinfo=UTC)
    for index in range(events):
        rows += _hourly(cursor, [STORM_KP] * storm_hours)
        cursor += dt.timedelta(hours=storm_hours)
        if index < events - 1:
            rows += _hourly(cursor, [QUIET_KP] * gap)
            cursor += dt.timedelta(hours=gap)
    return _kp_frame(rows)


def _activated() -> None:
    regimes.activate_regime_config(EXPERIMENT)


# --- reporting fixtures (synthetic apparatus) ---------------------------------------------

STATIONS = ("S1", "S2", "S3")
IDENTITY = {"phase_id": "p", "source_id": "s", "target_definition_id": "t"}
SCORED_STATEMENT = f"2–31 December {SYNTH_YEAR}, 30 days, first 24 h excluded and counted"
DECLARED_MEMBERS = ("M-A", "M-B", "M-C", "B-01")  # M-C the model; B-01 the IRI benchmark


class _Mask:
    """Registered-mask stand-in carrying exactly the surfaces diagnostics reads."""

    def __init__(self, *, partition_id: str = "F1") -> None:
        self.mask_id = "mask-synth-1"
        self.set_id = "setX"
        self.feature_set_id = "FS-synth"
        self.partition_id = partition_id
        self.phase_id = IDENTITY["phase_id"]
        self.source_id = IDENTITY["source_id"]
        self.target_definition_id = IDENTITY["target_definition_id"]
        self.row_counts = {s: 6 for s in STATIONS}
        self.exclusion_counts = {s: 0 for s in STATIONS}
        self.scored_window_statement = SCORED_STATEMENT
        self.masked_rows = tuple(
            {
                "station": station,
                "interval_start_utc": dt.datetime(
                    SYNTH_YEAR, 4, day, hour, tzinfo=UTC
                ).isoformat(),
                "y_true": 10.0 + day + 0.5 * hour + {"S1": 0, "S2": 5, "S3": 9}[station],
                "y_hats": {},
            }
            for station in STATIONS
            for day in (2, 3)
            for hour in (0, 1, 2)
        )
        for row in self.masked_rows:
            truth = row["y_true"]
            row["y_hats"] = {
                "M-C": truth,  # the model, perfect
                "M-A": truth + 1.0,
                "M-B": truth + 2.0,
                "B-01": truth + 1.5,
            }


def _row(benchmark_id: str, *, beats: bool = False) -> dict[str, Any]:
    row = {
        "model_id": "M-C",
        "benchmark_id": benchmark_id,
        "scalar": -1.0 if beats else 1.0,
        "per_station": {s: 1.0 for s in STATIONS},
        "orientation": "benchmark_minus_model",
        "weighting": "equal_station",
        "sign_convention_sentence": SIGN_CONVENTION_SENTENCE,
        "beats_model": beats,
        "mask_id": "mask-synth-1",
        "set_id": "setX",
        **IDENTITY,
        "partition_id": "F1",
    }
    if benchmark_id in ("B-01", "C-01"):
        row["spatial_representativeness_sentence"] = SPATIAL_REPRESENTATIVENESS_SENTENCE
    return row


def _metrics_artifact(mask: _Mask, *, benchmarks: tuple[str, ...] = ("M-A", "M-B", "B-01")):
    # `units` is FIXTURE apparatus: the real emitted metrics artifact carries NO units
    # metadata today, and the refusal that fires on it is itself tested below (BLK-08).
    return {
        "artifact_class": "metrics_artifact",
        "set_id": "setX",
        "model_id": "M-C",
        "mask_id": mask.mask_id,
        "feature_set_id": mask.feature_set_id,
        "row_counts": dict(mask.row_counts),
        "exclusion_counts": dict(mask.exclusion_counts),
        "scored_window_statement": mask.scored_window_statement,
        "units": "TECU",
        "comparisons": [_row(b) for b in benchmarks],
        "phase2_not_independent_statement": PHASE2_NOT_INDEPENDENT_STATEMENT,
    }


def _budget() -> dict[str, Any]:
    return {
        "artifact_id": "budget-synth-1",
        "units": "TECU",
        "phase1_contents": {"provider_dtec_summary": "present", "aggregation_spread": "present"},
        "asymmetry_statement": "the budget is asymmetric about zero on this product",
        "phase2_quantities": {
            "dcb_uncertainty": "recorded not-applicable",
            "mapping_function_error": "recorded not-applicable",
            "stec_noise": "recorded not-applicable",
            "arc_alignment_error": "recorded not-applicable",
        },
        "budget_value": 0.8,
    }


def _table(mask: _Mask, artifact: dict[str, Any] | None = None, **kwargs: Any):
    caption = kwargs.pop(
        "caption",
        f"Primary results ({SCORED_STATEMENT}); plasmaspheric contribution caveat applies.",
    )
    table = build_primary_table(
        metrics_artifact=artifact if artifact is not None else _metrics_artifact(mask),
        mask=mask,
        budget_artifact=kwargs.pop("budget", _budget()),
        declared_member_ids=kwargs.pop("declared", DECLARED_MEMBERS),
        caption=caption,
        table_artifact_id="primary-table-synth-1",
    )
    table["target_lineage_statement"] = (
        "Phase 1 target lineage: location-sampled gridded VTEC (grid-cell population)"
    )
    return table


def _registry(tmp_path: Path) -> ConclusionSurfaceRegistry:
    return ConclusionSurfaceRegistry(tmp_path / "conclusion_surfaces")


def _conclusion(registry: ConclusionSurfaceRegistry) -> dict[str, Any]:
    surface_text = {
        "abstract_level_interpretation": (
            "Interpretation bounded to the frozen scope; plasmaspheric caveat applies. "
            + PHASE2_NOT_INDEPENDENT_STATEMENT
        ),
        "conclusion": "Conclusion bounded to the frozen scope.",
        "limitations": (
            f"Limitations: plasmaspheric contribution; target lineage mismatch "
            f"(grid-cell vs IPP population); scored set {SCORED_STATEMENT}."
        ),
    }
    artifact = {
        "conclusion_artifact_id": "conclusion-surface-1",
        "manifest_ref": "artifact_manifest.json#conclusion-surface-1",
        "surfaces": surface_text,
        **IDENTITY,
    }
    registry.register(
        {"artifact_id": "conclusion-surface-1", "kind": "conclusion_surface", **IDENTITY}
    )
    return artifact


_DEFAULT = object()


def _checklist(tmp_path: Path, **overrides: Any) -> dict[str, Any]:
    registry = overrides.pop("registry", None) or _registry(tmp_path)
    conclusion = overrides.pop("conclusion", _DEFAULT)
    if conclusion is _DEFAULT:
        conclusion = _conclusion(registry)
    mask = overrides.pop("mask", None) or _Mask()
    table = overrides.pop("table", None)
    if table is None:
        table = _table(mask)
    return build_claims_checklist(
        registry=registry,
        conclusion_surface=conclusion,
        table=table,
        breakdowns=overrides.pop("breakdowns", ()),
        notebook_captions=overrides.pop(
            "notebook_captions", {"04_results_and_claims_review": "Phase 1 target figure"}
        ),
        gim_overlap_has_run=overrides.pop("gim_overlap_has_run", False),
        **overrides,
    )


def _rows_by_ref(checklist: dict[str, Any], fragment: str) -> list[dict[str, Any]]:
    return [r for r in checklist["rows"] if fragment in str(r.get("reference", ""))]


# =======================================================================================
# 1. The transcription and the classifier (R-123; controls (1), (2))
# =======================================================================================


def test_regimes_transcription_matches_frozen_values() -> None:
    """Q1 = A's only new claim: the config block is an EXACT copy of Vision §9.3 / D-13
    (the change record's citation table). The expected values here are the frozen
    decisions' own, asserted against the transcription — never read INTO source code."""
    block = EXPERIMENT["regimes"]
    assert block["thresholds"]["quiet_kp_below"] == 4  # Vision §9.3: quiet Kp < 4
    assert block["thresholds"]["disturbed_kp_min"] == 4  # Vision §9.3: disturbed Kp >= 4
    assert block["thresholds"]["storm_kp_min"] == 5  # Vision §9.3: storm Kp >= 5
    assert block["event_window"]["pre_hours"] == 12  # −12 h
    assert block["event_window"]["post_hours"] == 24  # +24 h
    assert block["independence_min_quiet_hours"] == 24  # >=24 h of Kp<4 (D-13)
    assert block["independent_storm_event_threshold"] == 3  # D-13
    assert "GFZ" in str(block["count_source"]) and "D-11" in str(block["count_source"])
    assert str(block["december_day_range"]).strip() == TBD_SENTINEL  # routed, not decided
    assert list(block["d17_quality_strata"]["fields"]) == [
        "valid_observation_count",
        "within_hour_spread_tecu",
        "provider_dtec_summary",
    ]  # D-17, referenced by its decision


def test_regime_config_absent_block_refuses_naming_it() -> None:
    with pytest.raises(RegimeError) as excinfo:
        read_regime_config({})
    assert "regimes" in str(excinfo.value)


def test_control_1_boundary_hours_classified_from_config_values() -> None:
    """A Kp>=disturbed hour labelled quiet, or a Kp>=storm hour not labelled storm, FAILS
    these assertions — fixture Kp values are DERIVED from the config-read thresholds."""
    start = dt.datetime(SYNTH_YEAR, 6, 1, 0, tzinfo=UTC)
    frame = _kp_frame(_hourly(start, [QUIET_KP, DISTURBED_KP, STORM_KP]))
    labels = [row["regime"] for row in classify_hours(frame, config=CONFIG)]
    assert labels == ["quiet", "disturbed", "storm"]  # boundary-exact (>= boundaries)


def test_control_2_wrong_event_window_fails() -> None:
    assert_event_window(CONFIG.window_pre_hours, CONFIG.window_post_hours, config=CONFIG)
    with pytest.raises(RegimeError):
        assert_event_window(CONFIG.window_pre_hours + 1, CONFIG.window_post_hours, config=CONFIG)


def test_december_blind_by_signature() -> None:
    """No date/partition/December parameter exists on the classifier or the counting
    path, and no date filtering hides inside the classifier (W-2 point 1)."""
    classify_params = set(inspect.signature(classify_hours).parameters)
    count_params = set(inspect.signature(count_storm_events).parameters)
    assert classify_params == {"kp", "config"}
    assert count_params == {"kp", "release_grade", "source"}
    # scan the classifier's CODE (docstring excluded — it legitimately names the rule)
    tree = ast.parse(inspect.getsource(classify_hours))
    function = tree.body[0]
    code_dump = ast.dump(ast.Module(body=function.body[1:], type_ignores=[])).lower()
    for token in ("december", "partition", "month", "2022"):
        assert token not in code_dump


def test_no_threshold_literal_in_regimes_source() -> None:
    """FR-P1-05-18 clause 3 by construction: no integer threshold/window/count literal
    (4, 5, 12, 24, 3) exists as a code constant anywhere in regimes.py."""
    tree = ast.parse((REPO_ROOT / "src" / "evaluation" / "regimes.py").read_text("utf-8"))
    offenders = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, int)
        and not isinstance(node.value, bool)
        and node.value in (3, 4, 5, 12, 24)
    ]
    assert offenders == []


# =======================================================================================
# 2. The one counting path (controls (3), (4); must-not-fire)
# =======================================================================================


def test_control_3_non_gfz_source_and_absent_grade_raise() -> None:
    _activated()
    frame = _event_series(events=1)
    with pytest.raises(RegimeError):
        count_storm_events(frame, release_grade="definitive", source="NOAA Kp")
    with pytest.raises(RegimeError):
        count_storm_events(frame, release_grade="", source="GFZ Kp")
    with pytest.raises(RegimeError):
        count_storm_events(frame, release_grade=TBD_SENTINEL, source="GFZ Kp")


def test_control_4_provisional_dst_input_raises_naming_dst_summary() -> None:
    """The fixture NAMES `.dst_summary.json` (the VAL-11 custody item) as the input's
    derivation; nothing here reads that file."""
    _activated()
    frame = _event_series(events=1)
    with pytest.raises(RegimeError) as excinfo:
        count_storm_events(
            frame, release_grade="provisional", source="provisional Dst (.dst_summary.json)"
        )
    assert ".dst_summary.json" in str(excinfo.value)
    derived = _kp_frame(
        _hourly(dt.datetime(SYNTH_YEAR, 12, 10, tzinfo=UTC), [STORM_KP] * 3),
        derived_from=".dst_summary.json (provisional Dst)",
    )
    with pytest.raises(RegimeError) as excinfo2:
        count_storm_events(derived, release_grade="definitive", source="GFZ Kp")
    assert "D-11" in str(excinfo2.value)


def test_must_not_fire_gfz_graded_count_returns_with_intervals() -> None:
    """The pass path: a GFZ Kp series with a recorded grade returns the count and its
    event intervals (D-13's definitions from config)."""
    _activated()
    two = _event_series(events=2)  # separated by exactly the configured independence span
    count, intervals = count_storm_events(two, release_grade="definitive", source="GFZ Kp")
    assert count == 2 and len(intervals) == 2
    assert all(start < end for start, end in intervals)


def test_dependence_merges_events_below_configured_quiet_span() -> None:
    _activated()
    merged = _event_series(
        events=2, quiet_gap_hours=CONFIG.independence_min_quiet_hours - 1
    )
    count, intervals = count_storm_events(merged, release_grade="definitive", source="GFZ Kp")
    assert count == 1 and len(intervals) == 1


def test_unactivated_count_refuses_naming_the_block() -> None:
    regimes.reset_regime_config()
    try:
        with pytest.raises(RegimeError) as excinfo:
            count_storm_events(
                _event_series(events=1), release_grade="definitive", source="GFZ Kp"
            )
        assert "regimes" in str(excinfo.value)
    finally:
        _activated()


# =======================================================================================
# 3. The December guards (controls (5), (6), (31), (40); the routed day range)
# =======================================================================================


def test_december_day_range_tbd_refuses_stop_and_report() -> None:
    """The REAL config's day range is the `TBD — freeze gate` sentinel: the mechanism is
    built, the value is routed (Rec 15; TE §18.3) — the refusal names the field."""
    with pytest.raises(RegimeError) as excinfo:
        read_december_day_range(CONFIG)
    assert "december_day_range" in str(excinfo.value)


def test_audit_read_requires_registration_and_bars_dst_source() -> None:
    with pytest.raises(RegimeError):
        read_audit_storm_count({"artifact_id": "audit-1", "storm_event_count": 3})
    with pytest.raises(RegimeError):
        read_audit_storm_count({"artifact_id": "audit-1", "registered": True})
    with pytest.raises(RegimeError):
        read_audit_storm_count(
            {
                "artifact_id": "audit-1",
                "registered": True,
                "storm_event_count": 3,
                "count_source": "provisional Dst (.dst_summary.json)",
            }
        )
    count, artifact_id = read_audit_storm_count(
        {
            "artifact_id": "audit-1",
            "registered": True,
            "storm_event_count": 3,
            "count_source": "GFZ Kp",
        }
    )
    assert (count, artifact_id) == (3, "audit-1")


def test_control_31_audit_count_divergence_raises_naming_both() -> None:
    with pytest.raises(RegimeError) as excinfo:
        assert_audit_count_consistency(
            registered_count=3,
            comparison_count=2,
            audit_artifact_id="audit-1",
            kp_resource="the synthetic DEC Kp series",
        )
    message = str(excinfo.value)
    assert "3" in message and "2" in message and "audit-1" in message
    assert_audit_count_consistency(
        registered_count=2, comparison_count=2, audit_artifact_id="audit-1", kp_resource="kp"
    )


def test_control_6_post_freeze_demotion_fails() -> None:
    freeze = dt.datetime(SYNTH_YEAR, 12, 1, tzinfo=UTC).isoformat()
    early = {"record_id": "DEM-1", "recorded_at_utc": f"{SYNTH_YEAR}-11-30T00:00:00+00:00"}
    late = {"record_id": "DEM-2", "recorded_at_utc": f"{SYNTH_YEAR}-12-02T00:00:00+00:00"}
    assert_demotion_precedes_freeze(early, g05_freeze_utc=freeze)
    with pytest.raises(RegimeError):
        assert_demotion_precedes_freeze(late, g05_freeze_utc=freeze)


def test_control_40_wholly_outside_event_counted_fails() -> None:
    scored_start = dt.date(SYNTH_YEAR, 12, 2)
    scored_end = dt.date(SYNTH_YEAR, 12, 31)
    outside_event = (
        f"{SYNTH_YEAR}-11-20T00:00:00+00:00",
        f"{SYNTH_YEAR}-11-20T06:00:00+00:00",
    )
    inside_event = (
        f"{SYNTH_YEAR}-12-10T00:00:00+00:00",
        f"{SYNTH_YEAR}-12-10T06:00:00+00:00",
    )
    eligible, outside = eligible_storm_events(
        [outside_event, inside_event], scored_start=scored_start, scored_end=scored_end
    )
    assert eligible == (inside_event,) and outside == (outside_event,)
    with pytest.raises(RegimeError) as excinfo:
        assert_events_eligible_for_threshold(
            [outside_event], scored_start=scored_start, scored_end=scored_end
        )
    assert "D-13" in str(excinfo.value)


def _dec_fixture(*, registered: int, events: int):
    mask = _Mask(partition_id="DEC")
    artifact = _metrics_artifact(mask)
    audit = {
        "artifact_id": "audit-dec-1",
        "registered": True,
        "storm_event_count": registered,
        "count_source": "GFZ Kp",
    }
    kp = _event_series(events=events)
    return mask, artifact, audit, kp


def test_dec_breakdown_descriptive_only_below_threshold() -> None:
    """Registered count below D-13's threshold → the descriptive-only label rides the
    payload; the wholly-outside report field exists; the audit count governs."""
    mask, artifact, audit, kp = _dec_fixture(registered=2, events=2)
    breakdown = build_dec_regime_breakdown(
        metrics_artifact=artifact,
        mask=mask,
        kp=kp,
        audit=audit,
        experiment=SYNTH_EXPERIMENT,
        release_grade="definitive",
        source="GFZ Kp",
    )
    payload = breakdown["payload"]
    assert payload["descriptive_only"] is True
    assert payload["registered_storm_event_count"] == 2
    assert payload["events_wholly_outside_scored_set"] == []
    assert_descriptive_only_label(breakdown, config=CONFIG)


def test_must_not_fire_dec_breakdown_confirmatory_at_threshold() -> None:
    """The guard must NOT demote what D-13's threshold admits: registered count at the
    threshold renders confirmatory regime rows without the label."""
    mask, artifact, audit, kp = _dec_fixture(
        registered=CONFIG.event_threshold, events=CONFIG.event_threshold
    )
    breakdown = build_dec_regime_breakdown(
        metrics_artifact=artifact,
        mask=mask,
        kp=kp,
        audit=audit,
        experiment=SYNTH_EXPERIMENT,
        release_grade="definitive",
        source="GFZ Kp",
    )
    assert breakdown["payload"]["descriptive_only"] is False
    assert_descriptive_only_label(breakdown, config=CONFIG)  # nothing fires


def test_dec_breakdown_divergence_raises_at_the_path() -> None:
    mask, artifact, audit, kp = _dec_fixture(registered=3, events=2)
    with pytest.raises(RegimeError) as excinfo:
        build_dec_regime_breakdown(
            metrics_artifact=artifact,
            mask=mask,
            kp=kp,
            audit=audit,
            experiment=SYNTH_EXPERIMENT,
            release_grade="definitive",
            source="GFZ Kp",
        )
    assert "audit-dec-1" in str(excinfo.value)


def test_control_5_missing_descriptive_label_fails() -> None:
    mask, artifact, audit, kp = _dec_fixture(registered=1, events=1)
    breakdown = build_dec_regime_breakdown(
        metrics_artifact=artifact,
        mask=mask,
        kp=kp,
        audit=audit,
        experiment=SYNTH_EXPERIMENT,
        release_grade="definitive",
        source="GFZ Kp",
    )
    breakdown["payload"]["descriptive_only"] = False  # tamper: the label suppressed
    with pytest.raises(RegimeError):
        assert_descriptive_only_label(breakdown, config=CONFIG)


# =======================================================================================
# 4. W-3: the primary table (controls (7), (8), (9), (32), (33), (34); per-entry)
# =======================================================================================


def test_must_not_fire_complete_provenanced_caveated_table_renders() -> None:
    mask = _Mask()
    table = _table(mask)
    assert {r["benchmark_id"] for r in table["rows"]} == {"M-A", "M-B", "B-01"}
    assert table["scored_window_statement"] == SCORED_STATEMENT
    assert table["surviving_row_counts"] == mask.row_counts
    for row in table["rows"]:
        assert row["derived_percentage_rmse_reduction"]["derived"] is True
    metrics = table["member_metrics"]
    assert set(metrics) == {"M-C", "M-A", "M-B", "B-01"}
    for block in metrics.values():
        for field in ("rmse", *diagnostics.SUPPORTING_METRIC_FIELDS):
            assert field in block  # RMSE + the six supporting metrics, per member
    assert table["budget_ref"]["placement"] == "adjacent_to_primary_result"
    assert table["phase2_not_independent_statement"] == PHASE2_NOT_INDEPENDENT_STATEMENT


def test_control_7_missing_declared_member_refuses() -> None:
    mask = _Mask()
    artifact = _metrics_artifact(mask, benchmarks=("M-A", "B-01"))  # M-B's metric absent
    with pytest.raises(FairnessError):
        _table(mask, artifact)


def test_per_entry_fieldless_estimand_into_w3_raises() -> None:
    mask = _Mask()
    artifact = _metrics_artifact(mask)
    del artifact["comparisons"][0]["orientation"]
    with pytest.raises(RegimeError):
        _table(mask, artifact)


def test_control_9_missing_beats_model_fails() -> None:
    mask = _Mask()
    artifact = _metrics_artifact(mask)
    del artifact["comparisons"][1]["beats_model"]
    with pytest.raises(RegimeError):
        _table(mask, artifact)


def test_units_absent_refuses_blk08_checked() -> None:
    """The REAL metrics artifact carries no units metadata today (BLK-08's bound): the
    units refusal is what fires instead of a wrong number shipping."""
    mask = _Mask()
    artifact = _metrics_artifact(mask)
    del artifact["units"]
    with pytest.raises(RegimeError):
        _table(mask, artifact)
    artifact2 = _metrics_artifact(mask)
    artifact2["units"] = "meters"
    with pytest.raises(RegimeError):
        _table(mask, artifact2)


def test_caveatless_iri_row_into_w3_raises() -> None:
    mask = _Mask()
    artifact = _metrics_artifact(mask)
    for row in artifact["comparisons"]:
        if row["benchmark_id"] == "B-01":
            del row["spatial_representativeness_sentence"]
    with pytest.raises(RegimeError):
        _table(mask, artifact)


def test_control_32_provenance_field_missing_fails_on_table_and_breakdown() -> None:
    mask = _Mask()
    artifact = _metrics_artifact(mask)
    artifact["feature_set_id"] = ""  # the field Rec 16 names as not yet supplied upstream
    with pytest.raises(RegimeError) as excinfo:
        _table(mask, artifact)
    assert "feature_set_id" in str(excinfo.value)
    artifact_b = _metrics_artifact(mask)
    artifact_b["exclusion_counts"] = {}
    with pytest.raises(RegimeError):
        build_breakdown_artifact(
            breakdown_id="per_cell", metrics_artifact=artifact_b, mask=mask
        )


def test_control_33_scored_window_disagreement_raises_naming_both() -> None:
    mask = _Mask()
    artifact = _metrics_artifact(mask)
    artifact["scored_window_statement"] = "1–31 December, 31 days"  # a second denominator
    with pytest.raises(RegimeError) as excinfo:
        _table(mask, artifact)
    message = str(excinfo.value)
    assert "1–31 December, 31 days" in message and SCORED_STATEMENT in message


def test_control_34_unlabelled_derived_field_fails() -> None:
    with pytest.raises(RegimeError):
        require_derived_label({"value": 0.1, "derived": False}, surface="test")
    labelled = derived_rmse_reduction(1.0, 2.0)
    require_derived_label(labelled, surface="test")
    assert labelled["value"] == pytest.approx(0.5)
    with pytest.raises(RegimeError):
        derived_rmse_reduction(1.0, 0.0)  # undefined ratio never defaulted


def test_budget_contents_asserted_not_existence() -> None:
    mask = _Mask()
    broken = _budget()
    broken["asymmetry_statement"] = ""
    with pytest.raises(RegimeError):
        _table(mask, budget=broken)
    broken2 = _budget()
    broken2["phase2_quantities"]["dcb_uncertainty"] = 0.3  # a Phase 2 value filled
    with pytest.raises(RegimeError):
        _table(mask, budget=broken2)


def test_member_metrics_computed_not_restated() -> None:
    mask = _Mask()
    block = compute_member_metrics(mask, "M-A")  # constant +1 error
    assert block["rmse"] == pytest.approx(1.0)
    assert block["mae"] == pytest.approx(1.0)
    assert block["mean_error_bias"] == pytest.approx(1.0)
    assert block["pct90_95_absolute_error"]["p95"] == pytest.approx(1.0)


# =======================================================================================
# 5. W-5: the breakdown family (controls (13)-(18), (38))
# =======================================================================================


def test_control_13_non_d17_stratum_unrepresentable() -> None:
    with pytest.raises(RegimeError):
        build_quality_stratum(stratum_field="valid_satellite_count", config=CONFIG, strata_rows=[])
    for field in CONFIG.quality_strata_fields:
        build_quality_stratum(stratum_field=field, config=CONFIG, strata_rows=[])


def test_control_14_pooled_row_weighted_headline_fails() -> None:
    mask = _Mask()
    breakdown = build_breakdown_artifact(
        breakdown_id="pooled",
        metrics_artifact=_metrics_artifact(mask),
        mask=mask,
        role_label="supplementary",
        aggregation="pooled_row_weighted",
    )
    breakdown["role_label"] = "headline"  # tamper: pooled promoted to headline
    with pytest.raises(RegimeError):
        assert_headline_role(breakdown)


def test_control_15_fold_table_missing_fold_fails() -> None:
    complete = {fold: {"rmse": 1.0} for fold in diagnostics.FOLD_IDS}
    assert_fold_table(complete)
    incomplete = dict(complete)
    del incomplete["F4"]
    with pytest.raises(RegimeError):
        assert_fold_table(incomplete)


def test_control_16_mean_only_per_seed_fails() -> None:
    full = {"per_seed_values": [1.0, 1.1, 0.9], "mean": 1.0, "spread": 0.2}
    assert_per_seed_stability(full)
    with pytest.raises(RegimeError):
        assert_per_seed_stability({"mean": 1.0})
    with pytest.raises(RegimeError):
        assert_per_seed_stability({"per_seed_values": [1.0, 1.1], "mean": 1.0, "spread": 0.1})


def test_control_17_missing_stamp_fails() -> None:
    mask = _Mask()
    breakdown = build_breakdown_artifact(
        breakdown_id="per_cell", metrics_artifact=_metrics_artifact(mask), mask=mask
    )
    assert_breakdown_stamps(breakdown)
    breakdown["source_id"] = None  # tamper
    with pytest.raises(RegimeError):
        assert_breakdown_stamps(breakdown)


def test_control_18_missing_declared_breakdown_refuses() -> None:
    configured = ("per_cell", "regime_split", "fold_table", "tier3")
    assert_breakdown_inventory(configured, configured_list=configured)
    with pytest.raises(RegimeError) as excinfo:
        assert_breakdown_inventory(("per_cell", "fold_table"), configured_list=configured)
    assert "tier3" in str(excinfo.value)


def test_control_38_missing_driver_caveat_fails() -> None:
    mask = _Mask()
    per_station = build_breakdown_artifact(
        breakdown_id="per_station",
        metrics_artifact=_metrics_artifact(mask),
        mask=mask,
        per_station=True,
    )
    assert per_station["driver_identity_caveat"] == DRIVER_IDENTITY_CAVEAT  # emitted
    del per_station["driver_identity_caveat"]  # tamper
    with pytest.raises(RegimeError):
        require_driver_caveat(per_station, surface="test")


def test_per_entry_caveatless_gim_into_w5_raises() -> None:
    """Per-entry control (SD-R-01 § negative controls: "a caveat-less GIM comparison into
    W-5"): the violating row is pushed THROUGH `build_breakdown_artifact` — the W-5
    producing path — and the raise is asserted from that entry point. Iteration-2 repair
    of the 2026-09-06 Critical: the earlier form called the bare guard directly, so the
    suite was green while the call site had no coverage (`nfr-design:c58`)."""
    mask = _Mask()

    def _breakdown(payload: dict[str, Any]) -> dict[str, Any]:
        return build_breakdown_artifact(
            breakdown_id="tier3",
            metrics_artifact=_metrics_artifact(mask),
            mask=mask,
            payload=payload,
        )

    # must NOT fire: the same payload WITH the caveat renders, the row printed unchanged
    rendered = _breakdown({"rows": [_row("M-A"), _row("C-01")]})
    assert (
        rendered["payload"]["rows"][1]["spatial_representativeness_sentence"]
        == SPATIAL_REPRESENTATIVENESS_SENTENCE
    )
    # the control: a caveat-less GIM row in the payload refuses at the producing path
    caveatless = _row("C-01")
    del caveatless["spatial_representativeness_sentence"]
    with pytest.raises(RegimeError) as excinfo:
        _breakdown({"rows": [_row("M-A"), caveatless]})
    assert "C-01" in str(excinfo.value) and "lineage caveat" in str(excinfo.value)
    # the walker, not a top-level key, is the mechanism: a nested per-station placement
    # and an IRI row under `comparisons` are caught the same way
    iri_caveatless = _row("B-01")
    del iri_caveatless["spatial_representativeness_sentence"]
    with pytest.raises(RegimeError):
        _breakdown({"per_station": {"S1": {"comparisons": [iri_caveatless]}}})
    # a non-IRI/GIM row without the sentence is NOT an IRI/GIM comparison: no refusal
    plain = _row("M-B")
    assert "spatial_representativeness_sentence" not in plain
    _breakdown({"rows": [plain]})


def test_per_entry_unitless_metrics_artifact_into_w5_raises() -> None:
    """Per-entry control for `require_units` at W-5 (security-design.md Called-by "W-3,
    W-5, W-6"; iteration-2 suggestion 1): a metrics artifact with no TECU units metadata
    pushed THROUGH `build_breakdown_artifact` refuses, and the must-NOT-fire half: with
    TECU metadata the breakdown renders carrying `units` printed from that metadata."""
    mask = _Mask()
    unitless = _metrics_artifact(mask)
    del unitless["units"]
    with pytest.raises(RegimeError) as excinfo:
        build_breakdown_artifact(breakdown_id="per_cell", metrics_artifact=unitless, mask=mask)
    assert "TECU" in str(excinfo.value)
    wrong = _metrics_artifact(mask)
    wrong["units"] = "TECU/10"  # a non-TECU assertion is refused, not rescaled
    with pytest.raises(RegimeError):
        build_breakdown_artifact(breakdown_id="per_cell", metrics_artifact=wrong, mask=mask)
    rendered = build_breakdown_artifact(
        breakdown_id="per_cell", metrics_artifact=_metrics_artifact(mask), mask=mask
    )
    assert rendered["units"] == "TECU"


def test_top1pct_sensitivity_labelled_never_merged() -> None:
    block = top1pct_sensitivity_block({"rmse": 1.0}, {"rmse": 0.9})
    assert block["sensitivity"]["label"] == diagnostics.SENSITIVITY_LABEL
    assert block["parent"] == {"rmse": 1.0}  # separate, never merged


def test_completeness_shortfalls_machine_readable_two_tier() -> None:
    mask = _Mask()
    breakdown = build_breakdown_artifact(
        breakdown_id="daily_error",
        metrics_artifact=_metrics_artifact(mask),
        mask=mask,
        completeness_shortfalls=[{"month": f"{SYNTH_YEAR}-07", "reason": "partial retrieval"}],
    )
    assert breakdown["partial"] is True
    assert breakdown["completeness_shortfalls"][0]["month"] == f"{SYNTH_YEAR}-07"


# =======================================================================================
# 6. W-6: practical relevance and post-access (controls (19), (20), (21), (35))
# =======================================================================================


def _threshold_record(*, recorded_at: str | None = None) -> dict[str, Any]:
    return {
        "recorded_at_utc": recorded_at or f"{SYNTH_YEAR}-11-01T00:00:00+00:00",
        "units": "TECU",
        "reference_magnitude": {"value": 0.25, "description": "synthetic fixture reference"},
    }


_G06_RECEIPT = f"{SYNTH_YEAR}-12-05T00:00:00+00:00"


def test_control_19_threshold_after_g06_fails() -> None:
    late = _threshold_record(recorded_at=f"{SYNTH_YEAR}-12-06T00:00:00+00:00")
    with pytest.raises(RegimeError):
        practical_relevance_statement(
            threshold_record=late,
            budget_artifact=_budget(),
            measured_improvement=derived_rmse_reduction(1.0, 2.0),
            g06_receipt_utc=_G06_RECEIPT,
        )


def test_control_20_non_tecu_input_refused() -> None:
    record = _threshold_record()
    record["units"] = "meters"
    with pytest.raises(RegimeError):
        practical_relevance_statement(
            threshold_record=record,
            budget_artifact=_budget(),
            measured_improvement=derived_rmse_reduction(1.0, 2.0),
            g06_receipt_utc=_G06_RECEIPT,
        )


def test_control_35_missing_measured_improvement_refused() -> None:
    with pytest.raises(RegimeError) as excinfo:
        practical_relevance_statement(
            threshold_record=_threshold_record(),
            budget_artifact=_budget(),
            measured_improvement=None,
            g06_receipt_utc=_G06_RECEIPT,
        )
    assert "conjunct" in str(excinfo.value).lower()


def test_both_conjuncts_reported_and_demotion_label_emitted() -> None:
    statement = practical_relevance_statement(
        threshold_record=_threshold_record(),
        budget_artifact=_budget(),  # budget 0.8 > reference 0.25 → descriptive-only
        measured_improvement=derived_rmse_reduction(1.0, 2.0),
        g06_receipt_utc=_G06_RECEIPT,
    )
    assert statement["label"] == "descriptive-only"  # Vision §5.4's first constraint
    assert statement["first_conjunct"]["measured_reaches_reference"] is True
    assert statement["second_conjunct"]["reference_smaller_than_budget"] is True
    big_budget = _budget()
    big_budget["budget_value"] = 0.1  # reference 0.25 >= budget → no demotion label
    undemoted = practical_relevance_statement(
        threshold_record=_threshold_record(),
        budget_artifact=big_budget,
        measured_improvement=derived_rmse_reduction(1.9, 2.0),
        g06_receipt_utc=_G06_RECEIPT,
    )
    assert "label" not in undemoted
    assert undemoted["first_conjunct"]["measured_reaches_reference"] is False


def test_control_21_post_access_run_without_exploratory_label_fails() -> None:
    access = [
        {
            "retrieved_at_utc": f"{SYNTH_YEAR}-12-05T00:00:00+00:00",
            "locked_test_accessed": True,
        }
    ]
    before = {"run_id": "r1", "timestamp_utc": f"{SYNTH_YEAR}-12-04T00:00:00+00:00"}
    after_ok = {
        "run_id": "r2",
        "timestamp_utc": f"{SYNTH_YEAR}-12-06T00:00:00+00:00",
        "label": "exploratory",
    }
    after_bad = {"run_id": "r3", "timestamp_utc": f"{SYNTH_YEAR}-12-07T00:00:00+00:00"}
    assert_post_access_labelled([before, after_ok], access_events=access)
    with pytest.raises(RegimeError):
        assert_post_access_labelled([after_bad], access_events=access)
    assert_post_access_labelled([after_bad], access_events=[])  # no access → nothing fires


# =======================================================================================
# 7. W-8: the diagnostics quarantine (controls (25)-(28))
# =======================================================================================


def test_control_25_mixed_grade_raises_single_grade_builds() -> None:
    with pytest.raises(RegimeError):
        build_dst_diagnostic([], release_grades=["provisional", "final"])
    artifact = build_dst_diagnostic(
        [{"interval_start_utc": f"{SYNTH_YEAR}-06-01T00:00:00+00:00", "dst": -30.0}],
        release_grades=["final"],
    )
    assert artifact["diagnostic_label"] == diagnostics.DIAGNOSTIC_LABEL
    assert artifact["release_grade"] == "final"


def test_control_26_diagnostic_field_in_metrics_artifact_fails() -> None:
    clean = _metrics_artifact(_Mask())
    assert_no_diagnostic_field(clean)
    poisoned = _metrics_artifact(_Mask())
    poisoned["comparisons"][0]["note"] = diagnostics.DIAGNOSTIC_LABEL
    with pytest.raises(RegimeError):
        assert_no_diagnostic_field(poisoned)


def test_control_27_rf_figure_without_authoritative_false_refuses() -> None:
    with pytest.raises(RegimeError):
        rf_importance_figure_source({"artifact_id": "rf-1", "metadata": {}})
    with pytest.raises(RegimeError):
        rf_importance_figure_source({"artifact_id": "rf-1", "metadata": {"authoritative": True}})
    source = rf_importance_figure_source(
        {"artifact_id": "rf-1", "metadata": {"authoritative": False}}
    )
    assert diagnostics.NON_AUTHORITATIVE_LABEL in source["caveat_labels"]


def test_control_28_provisional_grade_at_barred_surface_raises() -> None:
    for surface in diagnostics.R62_BARRED_SURFACES:
        with pytest.raises(RegimeError):
            assert_grade_eligible("provisional", surface=surface)
    assert_grade_eligible("provisional", surface="diagnostic")  # its permitted lane
    assert_grade_eligible("final", surface="g05_regime_count")


# =======================================================================================
# 8. W-7: the plots manifest (controls (22)-(24); per-entry; the quarantine)
# =======================================================================================


def _registered_source(tmp_path: Path, **extra: Any):
    registry = _registry(tmp_path)
    artifact = {
        "artifact_id": "breakdown-per_cell",
        "kind": "breakdown",
        "units": "TECU",
        **IDENTITY,
        **extra,
    }
    registry.register(
        {"artifact_id": artifact["artifact_id"], "kind": "breakdown", **IDENTITY}
    )
    return registry, artifact


def test_manifest_entry_carries_ids_stamps_and_units_from_metadata(tmp_path: Path) -> None:
    registry, artifact = _registered_source(tmp_path)
    entry = build_plot_manifest_entry(
        plot_id="plot-1",
        plot_kind="prediction",
        source_artifacts=[artifact],
        registry=registry,
    )
    assert entry["source_artifact_ids"] == ["breakdown-per_cell"]
    assert entry["units_label"] == "TECU"  # taken from metadata, never hardcoded
    assert entry["source_stamps"][0]["phase_id"] == IDENTITY["phase_id"]
    assert_manifest_entry(entry, source_artifacts=[artifact])


def test_per_entry_unregistered_artifact_through_w7_refuses(tmp_path: Path) -> None:
    """The R-120 widening comparator has no registered surface — an unregistered
    comparator-shaped artifact refuses at the manifest entry point."""
    registry = _registry(tmp_path)
    registry.register({"artifact_id": "anchor", "kind": "breakdown", **IDENTITY})
    comparator = {
        "artifact_id": "widening-guard-comparator",
        "kind": "quarantined_comparator",
        "units": "TECU",
        **IDENTITY,
    }
    with pytest.raises(RegimeError):
        build_plot_manifest_entry(
            plot_id="plot-x",
            plot_kind="quality",
            source_artifacts=[comparator],
            registry=registry,
        )


def test_control_22_missing_source_ids_fails() -> None:
    with pytest.raises(RegimeError):
        assert_manifest_entry(
            {"plot_id": "p", "units_label": "TECU", "source_artifact_ids": []},
            source_artifacts=[],
        )


def test_control_23_units_label_disagreement_fails(tmp_path: Path) -> None:
    registry, artifact = _registered_source(tmp_path)
    entry = build_plot_manifest_entry(
        plot_id="plot-1",
        plot_kind="residual",
        source_artifacts=[artifact],
        registry=registry,
    )
    entry["units_label"] = "meters"  # tamper: label no longer from metadata
    with pytest.raises(RegimeError):
        assert_manifest_entry(entry, source_artifacts=[artifact])


def test_control_24_missing_required_plot_refuses(tmp_path: Path) -> None:
    registry, artifact = _registered_source(tmp_path)
    entries = [
        build_plot_manifest_entry(
            plot_id=f"plot-{kind}",
            plot_kind=kind,
            source_artifacts=[artifact],
            registry=registry,
        )
        for kind in REQUIRED_PLOT_KINDS
    ]
    assert_manifest_complete(entries, required_plots=REQUIRED_PLOT_KINDS)
    with pytest.raises(RegimeError):
        assert_manifest_complete(entries[:-1], required_plots=REQUIRED_PLOT_KINDS)


def test_per_entry_caveatless_figure_through_w7_raises(tmp_path: Path) -> None:
    """Rec 9's widening: an IRI/GIM-bearing figure whose caption AND metadata carry no
    lineage caveat refuses; 'present' = caption or figure metadata."""
    registry, artifact = _registered_source(
        tmp_path, is_irigim_comparison=True
    )
    entry = build_plot_manifest_entry(
        plot_id="plot-gim",
        plot_kind="prediction",
        source_artifacts=[artifact],
        registry=registry,
    )
    assert entry["is_irigim_comparison"] is True  # built entry carries the caveat metadata
    entry["metadata"] = {}
    entry["caption"] = "a caption without the caveat"
    entry["caveat_labels"] = ()
    with pytest.raises(RegimeError):
        assert_manifest_entry(entry, source_artifacts=[artifact])


def test_units_metadata_absent_on_every_source_refuses(tmp_path: Path) -> None:
    registry = _registry(tmp_path)
    registry.register({"artifact_id": "no-units", "kind": "breakdown", **IDENTITY})
    with pytest.raises(RegimeError):
        build_plot_manifest_entry(
            plot_id="plot-2",
            plot_kind="quality",
            source_artifacts=[{"artifact_id": "no-units", **IDENTITY}],
            registry=registry,
        )


def test_render_figure_refuses_naming_pin_surface_when_matplotlib_absent() -> None:
    try:
        import matplotlib  # noqa: F401

        pytest.skip("matplotlib installed; the absence refusal cannot be exercised here")
    except ImportError:
        pass
    with pytest.raises(RegimeError) as excinfo:
        plots.render_figure({"plot_id": "p", "units_label": "TECU"}, "out.png")
    assert "requirements.txt" in str(excinfo.value)


# =======================================================================================
# 9. W-4: the claims checklist (controls (10), (11), (12), (36), (37), (39))
# =======================================================================================


def test_control_36_absent_or_unregistered_conclusion_surface_fails_closed(
    tmp_path: Path,
) -> None:
    registry = _registry(tmp_path)
    with pytest.raises(RegimeError):
        _checklist(tmp_path, registry=registry, conclusion=None)  # absent → fail closed
    unregistered = {
        "conclusion_artifact_id": "never-registered",
        "manifest_ref": "artifact_manifest.json#x",
        "surfaces": {
            "abstract_level_interpretation": "a",
            "conclusion": "b",
            "limitations": "c",
        },
        **IDENTITY,
    }
    registry.register({"artifact_id": "anchor", "kind": "conclusion_surface", **IDENTITY})
    with pytest.raises(RegimeError):
        _checklist(tmp_path, registry=registry, conclusion=unregistered)
    registry2 = _registry(tmp_path / "second")
    conclusion = _conclusion(registry2)
    conclusion.pop("manifest_ref")  # unmanifested → fail closed
    with pytest.raises(RegimeError):
        _checklist(tmp_path, registry=registry2, conclusion=conclusion)


def test_checklist_inspects_exactly_the_registered_set(tmp_path: Path) -> None:
    registry = _registry(tmp_path)
    conclusion = _conclusion(registry)
    mask = _Mask()
    table = _table(mask)
    registry.register({"artifact_id": table["artifact_id"], "kind": "primary_table", **IDENTITY})
    checklist = _checklist(
        tmp_path, registry=registry, conclusion=conclusion, mask=mask, table=table
    )
    assert tuple(checklist["inspected_registered_set"]) == registry.ids()


def test_happy_checklist_no_failed_rows_and_residual_stated(tmp_path: Path) -> None:
    checklist = _checklist(tmp_path)
    failed = [r for r in checklist["rows"] if str(r["status"]).startswith("FAILED")]
    assert failed == []
    assert "NARROWED, NOT CLOSED" in checklist["residual"]
    assert "fully enforced" in checklist["residual"]  # stated, never claimed closed
    assert checklist["claim_boundary"] == D8_CLAIM_BOUNDARY
    assert "D-7" in checklist["nico_5min_bar"]
    assert checklist["phase2_not_independent_statement"] == PHASE2_NOT_INDEPENDENT_STATEMENT
    references = " ".join(str(r["reference"]) for r in checklist["rows"])
    for token in ("D-28", "TC-12", "NFR-TDEF-01", "FR-P1-03-4", "VAL-05", "FR-P1-05-19"):
        assert token in references


def test_control_10_beats_true_baseline_absent_from_conclusion_fails(tmp_path: Path) -> None:
    registry = _registry(tmp_path)
    conclusion = _conclusion(registry)  # conclusion text never names M-A
    mask = _Mask()
    artifact = _metrics_artifact(mask)
    artifact["comparisons"][0] = _row("M-A", beats=True)  # a planted winning baseline
    table = _table(mask, artifact)
    checklist = build_claims_checklist(
        registry=registry,
        conclusion_surface=conclusion,
        table=table,
        notebook_captions={"04": "Phase 1 target figure"},
    )
    rows = [r for r in _rows_by_ref(checklist, "FR-P1-05-20") if r.get("subject") == "M-A"]
    assert rows and rows[0]["status"] == "FAILED"


def test_control_11_caption_missing_plasmaspheric_fails_row(tmp_path: Path) -> None:
    registry = _registry(tmp_path)
    conclusion = _conclusion(registry)
    mask = _Mask()
    table = _table(mask, caption=f"Primary results ({SCORED_STATEMENT})")  # no sentence
    checklist = build_claims_checklist(
        registry=registry,
        conclusion_surface=conclusion,
        table=table,
        notebook_captions={"04": "caption"},
    )
    caption_rows = [
        r for r in _rows_by_ref(checklist, "FR-P1-05-19") if "caption" in r["required_location"]
    ]
    assert caption_rows and caption_rows[0]["status"] == "FAILED"


def test_control_12_planted_prohibited_phrase_caught(tmp_path: Path) -> None:
    mask = _Mask()
    poisoned = build_breakdown_artifact(
        breakdown_id="per_cell",
        metrics_artifact=_metrics_artifact(mask),
        mask=mask,
        payload={"claim": "this generalises beyond the frozen cells to other years"},
    )
    checklist = _checklist(tmp_path, mask=mask, breakdowns=[poisoned])
    d8_rows = _rows_by_ref(checklist, "D-8 claim boundary")
    assert d8_rows and d8_rows[0]["status"].startswith("FAILED")
    assert d8_rows[0]["found_at"]


def test_control_37_planted_local_forcing_attribution_caught(tmp_path: Path) -> None:
    mask = _Mask()
    poisoned = build_breakdown_artifact(
        breakdown_id="per_station",
        metrics_artifact=_metrics_artifact(mask),
        mask=mask,
        per_station=True,
        payload={"note": "NICO underperforms due to local forcing at the site"},
    )
    checklist = _checklist(tmp_path, mask=mask, breakdowns=[poisoned])
    tc12_rows = _rows_by_ref(checklist, "TC-12 interpretive half")
    assert tc12_rows and tc12_rows[0]["status"].startswith("FAILED")


def test_must_not_fire_caveat_itself_is_not_a_planted_phrase(tmp_path: Path) -> None:
    """The standing TC-12 caveat CONTAINS the words 'local forcing'; the caveat sentence
    is excluded from detection so emitting the mandated caveat never trips its own row."""
    mask = _Mask()
    clean = build_breakdown_artifact(
        breakdown_id="per_station",
        metrics_artifact=_metrics_artifact(mask),
        mask=mask,
        per_station=True,
    )
    checklist = _checklist(tmp_path, mask=mask, breakdowns=[clean])
    tc12_rows = _rows_by_ref(checklist, "TC-12 interpretive half")
    assert tc12_rows and tc12_rows[0]["status"] == "unasserted"


def test_control_39_missing_val05_sentence_fails(tmp_path: Path) -> None:
    registry = _registry(tmp_path)
    conclusion = _conclusion(registry)
    conclusion["surfaces"]["abstract_level_interpretation"] = "plasmaspheric note only"
    checklist = build_claims_checklist(
        registry=registry,
        conclusion_surface=conclusion,
        table=_table(_Mask()),
        notebook_captions={"04": "caption"},
    )
    val_rows = _rows_by_ref(checklist, "VAL-05")
    assert val_rows and val_rows[0]["status"] == "FAILED"


def test_d28_row_one_denominator_and_fails_when_absent(tmp_path: Path) -> None:
    registry = _registry(tmp_path)
    conclusion = _conclusion(registry)
    conclusion["surfaces"]["limitations"] = "limitations without the scored window"
    checklist = build_claims_checklist(
        registry=registry,
        conclusion_surface=conclusion,
        table=_table(_Mask()),
        notebook_captions={"04": "caption"},
    )
    d28_rows = _rows_by_ref(checklist, "D-28")
    limitation_rows = [r for r in d28_rows if "limitations" in str(r["required_location"])]
    assert limitation_rows and limitation_rows[0]["status"] == "FAILED"
    assert all(r["statement"] == SCORED_STATEMENT for r in d28_rows)  # printed, not authored


def test_fr_p1_03_4_row_fails_closed_without_a_caption_surface(tmp_path: Path) -> None:
    checklist = _checklist(tmp_path, notebook_captions=None)
    rows = _rows_by_ref(checklist, "FR-P1-03-4")
    assert rows and rows[0]["status"].startswith("FAILED")
    assert rows[0]["human_residue"]


def test_checklist_emitted_as_registered_surface_write_once(tmp_path: Path) -> None:
    registry = _registry(tmp_path)
    conclusion = _conclusion(registry)
    checklist = _checklist(tmp_path, registry=registry, conclusion=conclusion)
    out = tmp_path / "claims_checklist.json"
    emit_registered_artifact(checklist, out, registry=registry)
    assert registry.lookup("claims_checklist") is not None
    assert json.loads(out.read_text("utf-8"))["artifact_class"] == "claims_checklist"
    with pytest.raises(RegimeError):
        emit_registered_artifact(checklist, tmp_path / "again.json", registry=registry)


def test_registry_write_once_and_stamp_requirements(tmp_path: Path) -> None:
    registry = _registry(tmp_path)
    registry.register({"artifact_id": "a-1", "kind": "breakdown", **IDENTITY})
    with pytest.raises(RegimeError):
        registry.register({"artifact_id": "a-1", "kind": "breakdown", **IDENTITY})
    with pytest.raises(RegimeError):
        registry.register({"artifact_id": "a-2", "kind": "breakdown"})  # stamps absent
    with pytest.raises(RegimeError):
        require_registered_surface("a-9", registry=registry, surface="test")
    require_registered_surface("a-1", registry=registry, surface="test")
    with pytest.raises(RegimeError):
        require_registered_surface("x", registry=None, surface="test")  # fail closed


def test_provenance_guard_direct_negative(tmp_path: Path) -> None:
    mask = _Mask()
    artifact = {
        "mask_id": mask.mask_id,
        "feature_set_id": mask.feature_set_id,
        "surviving_row_counts": dict(mask.row_counts),
        "exclusion_counts": {"S1": 0},
        "scored_window_statement": SCORED_STATEMENT,
    }
    require_provenance_block(artifact, mask=mask, surface="test")
    del artifact["surviving_row_counts"]
    with pytest.raises(RegimeError):
        require_provenance_block(artifact, mask=mask, surface="test")


def test_beats_model_guard_direct() -> None:
    require_beats_model([_row("M-A")], surface="test")
    with pytest.raises(RegimeError):
        require_beats_model([{"benchmark_id": "M-A"}], surface="test")


# =======================================================================================
# 10. W-9: the notebooks — static scans and the helper's stop semantics
# =======================================================================================

NOTEBOOKS = (
    "01_data_and_target_audit",
    "02_processing_and_features_review",
    "03_model_training_review",
    "04_results_and_claims_review",
)


def _cells(name: str) -> list[dict[str, Any]]:
    payload = json.loads((REPO_ROOT / "notebooks" / f"{name}.ipynb").read_text("utf-8"))
    assert payload["metadata"]["kernelspec"]["name"] == "python3"
    return payload["cells"]


def test_notebooks_declaration_cell_first_with_never_executed_limit() -> None:
    for name in NOTEBOOKS:
        cells = _cells(name)
        first = cells[0]
        source = "".join(first["source"])
        assert first["cell_type"] == "code", name
        assert "declare_notebook_inputs" in source, name
        assert "NEVER EXECUTED" in source, name  # the honest limit, stated in cell 1
        assert f'notebook_id="{name}"' in source, name


def test_notebooks_no_only_copy_and_src_imports_only() -> None:
    """Control (30)'s grep evidence: no function/class definition (no logic class has its
    only copy in a notebook) and every import is stdlib-or-src."""
    allowed_stdlib = {"sys", "json", "pathlib"}
    for name in NOTEBOOKS:
        for cell in _cells(name):
            if cell["cell_type"] != "code":
                continue
            tree = ast.parse("".join(cell["source"]))
            for node in ast.walk(tree):
                assert not isinstance(
                    node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef
                ), (name, "a notebook may hold no only-copy of logic (TE §14, §7)")
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".")[0]
                        assert root in allowed_stdlib or root == "src", (name, alias.name)
                if isinstance(node, ast.ImportFrom):
                    root = (node.module or "").split(".")[0]
                    assert root in allowed_stdlib or root == "src", (name, node.module)


def test_notebooks_conclusion_cells_register_as_surfaces() -> None:
    for name in NOTEBOOKS:
        last = _cells(name)[-1]
        assert "register_notebook_conclusion" in "".join(last["source"]), name


def test_declaration_helper_stops_on_missing_input(tmp_path: Path) -> None:
    """Control (29)'s mechanism (the executed per-notebook stop stays owed to a kernel):
    a deliberately missing declared input stops with the stated message."""
    with pytest.raises(RegimeError) as excinfo:
        declare_notebook_inputs(
            notebook_id="fixture",
            dataset_version="v1",
            code_commit="abc123",
            config_ids={"experiment.yaml": "deadbeef"},
            artifact_ids=["artifacts/absent.json"],
            workspace=tmp_path,
        )
    assert "absent.json" in str(excinfo.value)
    present = tmp_path / "artifacts"
    present.mkdir()
    (present / "there.json").write_text("{}", encoding="utf-8")
    header = declare_notebook_inputs(
        notebook_id="fixture",
        dataset_version="v1",
        code_commit="abc123",
        config_ids={"experiment.yaml": "deadbeef"},
        artifact_ids=["artifacts/there.json"],
        workspace=tmp_path,
    )
    block = header["header_declaration"]  # TA-16: a parse, not a screenshot
    assert block["notebook_id"] == "fixture" and block["code_commit"] == "abc123"
    with pytest.raises(RegimeError):
        declare_notebook_inputs(
            notebook_id="fixture",
            dataset_version="  ",
            code_commit="abc123",
            config_ids={"experiment.yaml": "deadbeef"},
            artifact_ids=[],
            workspace=tmp_path,
        )


def test_register_notebook_conclusion_registers(tmp_path: Path) -> None:
    path = register_notebook_conclusion(
        tmp_path / "conclusion_surfaces",
        notebook_id="04_results_and_claims_review",
        conclusion_text="bounded conclusion",
        **IDENTITY,
    )
    entry = json.loads(Path(path).read_text("utf-8"))
    assert entry["kind"] == "notebook_conclusion_cell"


# =======================================================================================
# 11. Import boundary and module hygiene
# =======================================================================================

NEW_MODULES = ("regimes.py", "report_guards.py", "diagnostics.py", "plots.py")


def test_new_modules_import_no_features_models_external() -> None:
    """TE §12 / D-27: no `src.features`, `src.models` or `src.external` import anywhere
    in this unit's four modules (module scope OR function bodies); matplotlib appears at
    function scope only (lazy, R-05)."""
    forbidden = ("src.features", "src.models", "src.external")
    for name in NEW_MODULES:
        path = REPO_ROOT / "src" / "evaluation" / name
        tree = ast.parse(path.read_text("utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import | ast.ImportFrom):
                names = (
                    [node.module or ""]
                    if isinstance(node, ast.ImportFrom)
                    else [a.name for a in node.names]
                )
                for imported in names:
                    assert not any(
                        imported == f or imported.startswith(f + ".") for f in forbidden
                    ), (name, imported)
        for node in tree.body:  # module scope: matplotlib must not appear
            if isinstance(node, ast.Import | ast.ImportFrom):
                names = (
                    [node.module or ""]
                    if isinstance(node, ast.ImportFrom)
                    else [a.name for a in node.names]
                )
                for imported in names:
                    assert not imported.startswith("matplotlib"), (name, imported)


def test_plots_module_computes_no_reported_quantity() -> None:
    """Presentation-only by signature: no arithmetic aggregation call and no arithmetic
    operator exists in plots.py — every value and label is a copy of an input field."""
    tree = ast.parse((REPO_ROOT / "src" / "evaluation" / "plots.py").read_text("utf-8"))
    banned_calls = {"sum", "mean", "median", "sqrt", "average", "std"}
    offenders = [
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in banned_calls
    ]
    assert offenders == []
    banned_ops = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div | ast.Mult | ast.Sub)
    ]
    assert banned_ops == []


def test_regime_error_declared_once_at_the_r01_site() -> None:
    """The recorded deviation: RegimeError's class object lives in src/data/config.py
    (the R-01 declaration site) and regimes.py re-exports the SAME object — catchability
    preserved, no second class minted."""
    from src.data.config import RegimeError as base_regime_error

    assert regimes.RegimeError is base_regime_error
    assert report_guards.RegimeError is base_regime_error
