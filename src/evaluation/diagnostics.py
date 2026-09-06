"""R3/R4/R5 diagnostics: the primary table, the breakdown family, practical relevance,
the Dst/RF quarantine, the claims-and-limitations checklist, the notebook declaration
helper (R-125…R-128, R-130, R-131; W-3…W-6, W-8, W-9).

Purpose
-------
Everything between a computed number and a defensible statement, as producing paths:

* ``build_primary_table`` — W-3: the one primary-table artifact, built from the emitted
  metrics artifact (never assembled in a notebook, TE §14): refuses on a missing declared
  member; lands the three difficulty controls and the IRI comparison in the SAME artifact
  by construction; prints R-108's fields and the five provenance values from the producing
  objects, never restated; asserts TECU from units metadata (BLK-08 checked); prints
  `beats_model` per row (never judged); places the budget adjacent (TA-19); carries the
  §5.5 metric fields per member with the `derived: true` reduction (Rec 20).
* the breakdown family — W-5: stamped producing functions (TEC-05), the D-17 strata bound
  structural, headline/supplementary labels, the F1–F4 fold table, per-seed stability as
  separate fields, the top-1% sensitivity labelled never merged, machine-readable
  completeness shortfalls (two-tier posture), the inventory refusal, the standing TC-12
  driver-identity caveat emitted from the per-station producing path (Rec 17), and the
  DEC regime breakdown with the descriptive-only storm guard reading the REGISTERED
  pre-G-05 audit count, the audit-count consistency raise (control (31)) and the
  outside-scored-set exclusion (control (40)).
* ``practical_relevance_statement`` — W-6: the ONLY source of any practical-relevance
  statement; asserts the threshold timestamp precedes the G-06 receipt (PC-09), evaluates
  BOTH Vision §5.3 conjuncts (the measured improvement is a required input, control (35)),
  refuses non-TECU inputs, and emits the descriptive-only label where the reference is
  smaller than the budget. ``assert_post_access_labelled`` is FR-P1-05-14's reporting-side
  assertion (which surface WRITES the label stays routed to the gate).
* the diagnostics quarantine — W-8: Dst hindcast artifacts labelled diagnostic/
  hindcast-only with a single recorded release grade (mixed grade raises, D-10.1);
  provisional grade raises at any R-62-barred surface; the RF-importance figure renders
  only from `authoritative = false` metadata (R-100).
* ``build_claims_checklist`` — W-4: one row per prohibited class (cited from
  `requirements.md` § Out of scope C by reference, never duplicated) and per mandated
  disclosure, resolved against the REGISTERED `ConclusionSurfaceArtifact` and FAILING
  CLOSED when it is absent, unmanifested or unregistered (control (36)). The
  hand-authored-prose residual is STATED on the artifact, never claimed closed.
* ``declare_notebook_inputs`` / ``register_notebook_conclusion`` — W-9: the first-cell
  declaration helper (TA-16's machine-parsed header; REQ-ENG-12's Run-all stop semantics
  by construction) and the conclusion-cell registration.

Inputs
------
The emitted metrics artifact (`src/evaluation/metrics.build_metrics_artifact`'s shape),
the registered `ComparisonMask`, the registered pre-G-05 audit artifact
(`inventory-and-registry`'s read), the budget artifact (`target-standardization`'s), the
`regimes` block off `ConfigSnapshot.experiment`, and the `ConclusionSurfaceRegistry`.
Imports ONLY `src/data`, `src/evaluation` siblings and the standard library — no
`src/features`, `src/models`, `src/external`, directly or transitively (TE §12; D-27).

Re-run behaviour
----------------
Pure computation over supplied artifacts; emission goes through
`report_guards.emit_registered_artifact` (write-once atomic, registration enforced).
Deterministic given identical inputs. Every integrity refusal raises an `IntegrityError`
subclass naming the resource and the violated expectation; completeness shortfalls are
machine-readable fields on the artifact, never console text (the two-tier posture).

Governance
----------
No practical-relevance threshold is introduced, changed or reinterpreted here (PC-09;
§5.4's ten-percent figure is a reference magnitude read from the frozen record). No
scientific value is decided; December never informs selection through any path here
(ML-02). Planted-phrase detection catches the obvious wording, not a paraphrase — that
residue is recorded per row as `human_residue`, and the checklist never claims full
enforcement (SD-R-03).
"""

from __future__ import annotations

import datetime as dt
import json
import math
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from src.data.config import RegimeError
from src.data.splits import LOCKED_ID
from src.evaluation.metrics import (
    EXTERNAL_COMPARATOR_IDS,
    PHASE2_NOT_INDEPENDENT_STATEMENT,
    SPATIAL_REPRESENTATIVENESS_SENTENCE,
)
from src.evaluation.regimes import (
    RegimeConfig,
    activate_regime_config,
    assert_audit_count_consistency,
    assert_demotion_precedes_freeze,
    assert_events_eligible_for_threshold,
    count_storm_events,
    eligible_storm_events,
    read_audit_storm_count,
    read_december_day_range,
    read_regime_config,
)
from src.evaluation.report_guards import (
    DRIVER_IDENTITY_CAVEAT,
    ConclusionSurfaceRegistry,
    require_beats_model,
    require_complete_members,
    require_d17_bound,
    require_derived_label,
    require_driver_caveat,
    require_estimand_fields,
    require_lineage_caveat,
    require_provenance_block,
    require_registered_surface,
    require_units,
)

__all__ = [
    "FOLD_IDS",
    "SENSITIVITY_LABEL",
    "DIAGNOSTIC_LABEL",
    "NON_AUTHORITATIVE_LABEL",
    "R62_BARRED_SURFACES",
    "SUPPORTING_METRIC_FIELDS",
    "D8_CLAIM_BOUNDARY",
    "D7_NICO_5MIN_BAR",
    "CHECKLIST_RESIDUAL",
    "PROHIBITED_CLASS_ROWS",
    "compute_member_metrics",
    "derived_rmse_reduction",
    "build_primary_table",
    "build_breakdown_artifact",
    "assert_headline_role",
    "assert_fold_table",
    "assert_per_seed_stability",
    "assert_breakdown_stamps",
    "assert_breakdown_inventory",
    "build_quality_stratum",
    "top1pct_sensitivity_block",
    "build_dec_regime_breakdown",
    "assert_descriptive_only_label",
    "practical_relevance_statement",
    "assert_post_access_labelled",
    "build_dst_diagnostic",
    "assert_grade_eligible",
    "assert_no_diagnostic_field",
    "rf_importance_figure_source",
    "build_claims_checklist",
    "declare_notebook_inputs",
    "register_notebook_conclusion",
]

#: Vision §9.5's validation folds. Identity tokens.
FOLD_IDS: tuple[str, ...] = ("F1", "F2", "F3", "F4")

#: FR-P1-05-10's label — the top-1% sensitivity is labelled, never merged.
SENSITIVITY_LABEL: str = "sensitivity"

#: TC-11's lane label. Diagnostic artifacts live only under diagnostic paths.
DIAGNOSTIC_LABEL: str = "diagnostic/hindcast-only"

#: R-100's render label, printed from `authoritative = false` metadata.
NON_AUTHORITATIVE_LABEL: str = "non-authoritative"

#: The surfaces R-62 restriction 3 bars a provisional-grade series from (identity tokens).
R62_BARRED_SURFACES: tuple[str, ...] = (
    "modelling_input",
    "frozen_tolerance",
    "g05_regime_count",
)

#: Vision §5.5's six supporting metrics (the reported error surface; decides nothing).
SUPPORTING_METRIC_FIELDS: tuple[str, ...] = (
    "mae",
    "median_absolute_error",
    "mean_error_bias",
    "r_squared",
    "correlation",
    "pct90_95_absolute_error",
)

#: D-8's frozen claim boundary, quoted under its decision (a citation, not a choice).
D8_CLAIM_BOUNDARY: str = (
    "Hourly VTEC forecasting at ARUC 40/44, BSHM 32/35, NICO 35/33 cells, calendar year "
    "2022, tested on December 2022 only; no generalisation beyond these cells, this year, "
    "or this test month (D-8; TC-17)"
)

#: D-7's consequence, quoted under its decision.
D7_NICO_5MIN_BAR: str = (
    "Any scientific question requiring 5-minute resolution at NICO is out of reach on "
    "this dataset and must not be claimed (D-7)"
)

#: SD-R-03's stated residual — carried on every checklist artifact, never softened.
CHECKLIST_RESIDUAL: str = (
    "Hand-authored thesis prose written outside the pipeline never passes a producing "
    "path and cannot be forced to register; this checklist bounds what the pipeline "
    "produces, not what a human types elsewhere. Planted-phrase detection catches the "
    "obvious wording, not a paraphrase. The checklist is NARROWED, NOT CLOSED, and must "
    "never be described as fully enforced; the gate and the supervisor remain the check "
    "on unregistered prose."
)

#: The prohibited-class rows: the enumeration itself is maintained in `requirements.md`
#: § Out of scope C ONLY, cited by reference and never duplicated here; the named rows
#: below carry planted-phrase DETECTION tokens (identity tokens, with the paraphrase
#: residue recorded per row as human_residue).
PROHIBITED_CLASS_ROWS: tuple[Mapping[str, Any], ...] = (
    {
        "reference": "requirements.md § Out of scope C — D-8 claim boundary",
        "boundary_text": D8_CLAIM_BOUNDARY,
        "detection_phrases": ("generalises beyond", "generalizes beyond", "other years"),
    },
    {
        "reference": "requirements.md § Out of scope C — D-7 NICO 5-minute bar",
        "boundary_text": D7_NICO_5MIN_BAR,
        "detection_phrases": ("5-minute NICO", "five-minute NICO", "5-minute resolution at NICO"),
    },
    {
        "reference": "TC-12 interpretive half (project.md § Mandated, binding: hard)",
        "boundary_text": DRIVER_IDENTITY_CAVEAT,
        "detection_phrases": ("local forcing",),
    },
)

#: VAL-05's key fragment, detected inside the abstract-level interpretation (the full
#: statement is `metrics.PHASE2_NOT_INDEPENDENT_STATEMENT`).
_VAL05_FRAGMENT: str = "not a second statistically independent blind test"

#: FR-P1-05-19's detection token (the sentence's frozen wording lives upstream; detection
#: catches the obvious wording, human_residue recorded).
_PLASMASPHERIC_TOKEN: str = "plasmaspheric"


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


# =======================================================================================
# §5.5 metric surface (Rec 20) — the REPORTED error metrics; the estimand decides
# =======================================================================================


def _percentile(sorted_values: Sequence[float], pct: float) -> float:
    if not sorted_values:
        raise RegimeError("metric input", "percentile of an empty error series is undefined")
    rank = max(0, math.ceil(pct / 100.0 * len(sorted_values)) - 1)
    return sorted_values[rank]


def compute_member_metrics(mask: Any, member_id: str) -> dict[str, Any]:
    """RMSE and §5.5's six supporting metrics for one member over the masked rows only.

    The paired loss differential remains the confirmatory estimand (Vision §2.3) — these
    fields are the REPORTED error surface and decide nothing.

    Raises
    ------
    RegimeError
        a masked row without the member's y_hat (a mask-construction failure), or a
        degenerate series over which R² / correlation is undefined.
    """
    truths: list[float] = []
    preds: list[float] = []
    for row in mask.masked_rows:
        y_hats = row["y_hats"]
        if member_id not in y_hats:
            raise RegimeError(
                f"mask {mask.mask_id} row {row['station']}/{row['interval_start_utc']}",
                f"carries no y_hat for member {member_id!r}; metrics are computed on "
                f"masked rows only and a masked row missing a member is a mask-"
                f"construction failure (R-108 step 1's shape)",
            )
        truths.append(float(row["y_true"]))
        preds.append(float(y_hats[member_id]))
    n = len(truths)
    if n == 0:
        raise RegimeError(f"mask {mask.mask_id}", "no masked rows; metrics are undefined")
    errors = [p - t for p, t in zip(preds, truths, strict=True)]
    abs_errors = sorted(abs(e) for e in errors)
    rmse = math.sqrt(sum(e * e for e in errors) / n)
    mean_t = sum(truths) / n
    mean_p = sum(preds) / n
    ss_tot = sum((t - mean_t) ** 2 for t in truths)
    if ss_tot == 0.0:
        raise RegimeError(
            f"mask {mask.mask_id}",
            "target variance is zero over the masked rows; R² and correlation are "
            "undefined on a degenerate series and are never silently defaulted",
        )
    ss_res = sum(e * e for e in errors)
    cov = sum((t - mean_t) * (p - mean_p) for t, p in zip(truths, preds, strict=True))
    var_p = sum((p - mean_p) ** 2 for p in preds)
    correlation = 0.0 if var_p == 0.0 else cov / math.sqrt(ss_tot * var_p)
    return {
        "member_id": str(member_id),
        "rmse": rmse,
        "mae": sum(abs_errors) / n,
        "median_absolute_error": _percentile(abs_errors, 50.0),
        "mean_error_bias": sum(errors) / n,
        "r_squared": 1.0 - ss_res / ss_tot,
        "correlation": correlation,
        "pct90_95_absolute_error": {
            "p90": _percentile(abs_errors, 90.0),
            "p95": _percentile(abs_errors, 95.0),
        },
    }


def derived_rmse_reduction(model_rmse: float, reference_rmse: float) -> dict[str, Any]:
    """The §5.5 derived relative summary `1 - RMSE_model/RMSE_reference`, labelled.

    Raises
    ------
    RegimeError
        a zero reference RMSE (the ratio is undefined and never defaulted).
    """
    if reference_rmse == 0.0:
        raise RegimeError(
            "derived_percentage_rmse_reduction",
            "reference RMSE is zero; 1 - RMSE_model/RMSE_reference is undefined and is "
            "never silently defaulted",
        )
    return {
        "name": "derived_percentage_rmse_reduction",
        "value": 1.0 - model_rmse / reference_rmse,
        "definition": "1 - RMSE_model/RMSE_reference",
        "derived": True,  # Vision §9.5 required result 2: clearly labeled as derived
    }


# =======================================================================================
# W-3: the primary results table
# =======================================================================================


def _assert_budget(budget: Mapping[str, Any]) -> None:
    resource = f"budget artifact {budget.get('artifact_id', '<no id>')}"
    if not budget.get("phase1_contents"):
        raise RegimeError(
            resource,
            "Phase 1-applicable contents are absent or empty; FR-P1-05-10's budget "
            "adjacency asserts CONTENTS, not existence (TA-19)",
        )
    if not budget.get("asymmetry_statement"):
        raise RegimeError(resource, "the asymmetry statement is absent or empty (FR-P1-05-10)")
    phase2 = budget.get("phase2_quantities")
    if not isinstance(phase2, Mapping) or not phase2:
        raise RegimeError(
            resource,
            "the four Phase 2 quantities are absent; they are shown as RECORDED "
            "not-applicable, never omitted (requirements.md § Known defects row 11)",
        )
    wrong = [key for key, value in phase2.items() if value != "recorded not-applicable"]
    if wrong:
        raise RegimeError(
            resource,
            f"Phase 2 quantit(ies) {wrong} are not recorded not-applicable; a Phase 2 "
            f"value filled in Phase 1 is a phase-boundary defect (NFR-PHASE-01)",
        )


def build_primary_table(
    *,
    metrics_artifact: Mapping[str, Any],
    mask: Any,
    budget_artifact: Mapping[str, Any],
    declared_member_ids: Sequence[str],
    caption: str,
    table_artifact_id: str,
) -> dict[str, Any]:
    """W-3: the one primary-table artifact — refuses, co-reports, prints, checks units.

    The three difficulty controls and the IRI comparison are rows of THIS one artifact by
    construction (PC-03/PC-04: appendix relegation unrepresentable). Everything printed is
    a copy of a checked field on the producing objects; nothing is restated.

    Raises
    ------
    FairnessError
        a declared member's metric absent (the consumed R-110 limb 1 class).
    RegimeError
        units not TECU; a row without its estimand fields; a missing `beats_model`;
        provenance absent or the scored window disagreeing with the mask; an IRI/GIM row
        without its lineage caveat; a budget-contents defect.
    """
    surface = f"primary table {table_artifact_id}"
    rows = list(metrics_artifact.get("comparisons", ()))
    model_id = str(metrics_artifact.get("model_id", ""))
    present = [model_id] + [str(r.get("benchmark_id")) for r in rows]
    require_complete_members(
        present, declared_member_ids=declared_member_ids, surface=surface
    )
    require_units(metrics_artifact, surface=surface)
    require_beats_model(rows, surface=surface)

    table_rows: list[dict[str, Any]] = []
    member_metrics = {model_id: compute_member_metrics(mask, model_id)}
    for row in rows:
        require_estimand_fields(row, surface=surface)
        require_lineage_caveat(row, surface=surface, kind="row")
        benchmark_id = str(row["benchmark_id"])
        member_metrics[benchmark_id] = compute_member_metrics(mask, benchmark_id)
        reduction = derived_rmse_reduction(
            member_metrics[model_id]["rmse"], member_metrics[benchmark_id]["rmse"]
        )
        require_derived_label(reduction, surface=surface)
        out = dict(row)  # printed from the artifact, never restated
        out["derived_percentage_rmse_reduction"] = reduction
        table_rows.append(out)

    _assert_budget(budget_artifact)

    table: dict[str, Any] = {
        "artifact_id": str(table_artifact_id),
        "artifact_class": "primary_table",
        "kind": "primary_table",
        "set_id": metrics_artifact.get("set_id"),
        "model_id": model_id,
        "members": list(dict.fromkeys(present)),
        "rows": table_rows,
        "member_metrics": member_metrics,
        "units": metrics_artifact.get("units"),
        "caption": str(caption),
        "budget_ref": {
            "budget_artifact_id": budget_artifact.get("artifact_id"),
            "placement": "adjacent_to_primary_result",
            "asymmetry_statement": budget_artifact.get("asymmetry_statement"),
        },
        # the five provenance values, printed from the producing objects (Rec 16)
        "mask_id": metrics_artifact.get("mask_id"),
        "feature_set_id": metrics_artifact.get("feature_set_id"),
        "surviving_row_counts": dict(metrics_artifact.get("row_counts", {})),
        "exclusion_counts": dict(metrics_artifact.get("exclusion_counts", {})),
        "scored_window_statement": metrics_artifact.get("scored_window_statement"),
        # stamps copied from the registered mask (TEC-05)
        "phase_id": getattr(mask, "phase_id", None),
        "source_id": getattr(mask, "source_id", None),
        "target_definition_id": getattr(mask, "target_definition_id", None),
        "partition_id": getattr(mask, "partition_id", None),
        "phase2_not_independent_statement": metrics_artifact.get(
            "phase2_not_independent_statement"
        ),
    }
    require_provenance_block(table, mask=mask, surface=surface)
    if table["phase2_not_independent_statement"] != PHASE2_NOT_INDEPENDENT_STATEMENT:
        raise RegimeError(
            surface,
            "the Phase-2 not-independent-blind-test statement is absent or altered on the "
            "metrics artifact; the disclosure travels as a field (VAL-05)",
        )
    return table


# =======================================================================================
# W-5: the breakdown family
# =======================================================================================


def assert_breakdown_stamps(artifact: Mapping[str, Any]) -> None:
    """Control (17): an artifact missing any of the three stamps FAILS (TEC-05)."""
    missing = [
        stamp
        for stamp in ("phase_id", "source_id", "target_definition_id")
        if not artifact.get(stamp)
    ]
    if missing:
        raise RegimeError(
            f"breakdown {artifact.get('breakdown_id', '?')}",
            f"mandated stamp(s) {missing} absent (TEC-05; project.md Mandated)",
        )


def assert_headline_role(artifact: Mapping[str, Any]) -> None:
    """Control (14): a pooled row-weighted figure labelled headline FAILS — the
    equal-station macro-average is the headline value (FR-P1-05-16)."""
    role = artifact.get("role_label")
    if role not in ("headline", "supplementary"):
        raise RegimeError(
            f"breakdown {artifact.get('breakdown_id', '?')}",
            f"role_label {role!r} is not headline|supplementary; the label is carried on "
            f"the artifact (R-127)",
        )
    if role == "headline" and artifact.get("aggregation") != "equal_station_macro":
        raise RegimeError(
            f"breakdown {artifact.get('breakdown_id', '?')}",
            f"aggregation {artifact.get('aggregation')!r} labelled headline; the "
            f"equal-station macro-average is the headline and pooled row-weighted is "
            f"supplementary, always (R-127 control (14))",
        )


def assert_fold_table(fold_rows: Mapping[str, Any]) -> None:
    """Control (15): a fold table missing any of F1–F4 FAILS (Vision §9.5)."""
    missing = [fold for fold in FOLD_IDS if fold not in fold_rows]
    if missing:
        raise RegimeError(
            "validation-fold table",
            f"fold(s) {missing} absent; Vision §9.5 requires F1–F4, all four (R-127)",
        )


def assert_per_seed_stability(block: Mapping[str, Any]) -> None:
    """Control (16): per-seed stability reported as mean-only FAILS — the three per-seed
    values, the mean AND the spread are separate fields (TE §13.5)."""
    values = block.get("per_seed_values")
    missing = [key for key in ("per_seed_values", "mean", "spread") if key not in block]
    if missing or not isinstance(values, Sequence) or len(values) != 3:
        raise RegimeError(
            "per-seed stability block",
            f"requires the three per-seed values plus mean and spread as SEPARATE fields "
            f"(absent: {missing or 'per_seed_values must carry exactly three values'}); "
            f"mean-only reporting fails (TE §13.5; R-127 control (16))",
        )


def assert_breakdown_inventory(
    emitted_ids: Sequence[str], *, configured_list: Sequence[str]
) -> None:
    """Control (18): a declared breakdown missing from the inventory REFUSES the results
    artifact rather than shipping partial (R-110 limb 1's shape, one level down)."""
    missing = sorted(set(map(str, configured_list)) - set(map(str, emitted_ids)))
    if missing:
        raise RegimeError(
            "breakdown inventory",
            f"declared breakdown(s) {missing} missing from the emitted inventory "
            f"{sorted(map(str, emitted_ids))}; the results artifact is refused rather "
            f"than shipped partial (R-127 control (18))",
        )


def build_quality_stratum(
    *,
    stratum_field: str,
    config: RegimeConfig,
    strata_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """A quality stratum over D-17's measured-available fields ONLY — the enumerated set
    arrives from config, so a stratum on satellite count, elevation or zenith angle is
    unrepresentable (R-127; a bypass attempt is caught by the guard).

    Raises
    ------
    RegimeError
        `stratum_field` outside the configured enumeration.
    """
    require_d17_bound(
        stratum_field,
        configured_fields=config.quality_strata_fields,
        surface="quality stratum",
    )
    return {"stratum_field": str(stratum_field), "rows": list(strata_rows)}


def top1pct_sensitivity_block(
    parent_value: Mapping[str, Any], sensitivity_value: Mapping[str, Any]
) -> dict[str, Any]:
    """FR-P1-05-10: the top-1%-absolute-error-removed sensitivity, emitted BESIDE its
    parent figure, labelled `sensitivity`, never merged."""
    return {
        "parent": dict(parent_value),
        "sensitivity": {**dict(sensitivity_value), "label": SENSITIVITY_LABEL},
    }


def build_breakdown_artifact(
    *,
    breakdown_id: str,
    metrics_artifact: Mapping[str, Any],
    mask: Any,
    role_label: str = "supplementary",
    aggregation: str = "equal_station_macro",
    per_station: bool = False,
    payload: Mapping[str, Any] | None = None,
    completeness_shortfalls: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """The generic W-5 producing function: stamped, labelled, provenanced, caveated.

    Completeness shortfalls are machine-readable fields on the artifact — never console
    text — and mark the artifact partial (the two-tier posture). Per-station breakdowns
    carry the standing TC-12 driver-identity caveat from THIS producing path (Rec 17).

    Raises
    ------
    RegimeError
        via the stamp/role/provenance/caveat validators below.
    """
    surface = f"breakdown {breakdown_id}"
    artifact: dict[str, Any] = {
        "artifact_id": f"breakdown-{breakdown_id}",
        "artifact_class": "breakdown",
        "kind": "breakdown",
        "breakdown_id": str(breakdown_id),
        "role_label": role_label,
        "aggregation": aggregation,
        "per_station": bool(per_station),
        "payload": dict(payload or {}),
        "completeness_shortfalls": [dict(s) for s in completeness_shortfalls],
        "partial": bool(completeness_shortfalls),
        "phase_id": getattr(mask, "phase_id", None),
        "source_id": getattr(mask, "source_id", None),
        "target_definition_id": getattr(mask, "target_definition_id", None),
        "partition_id": getattr(mask, "partition_id", None),
        # the same five provenance values, carried on every breakdown (Rec 16)
        "mask_id": metrics_artifact.get("mask_id"),
        "feature_set_id": metrics_artifact.get("feature_set_id"),
        "surviving_row_counts": dict(metrics_artifact.get("row_counts", {})),
        "exclusion_counts": dict(metrics_artifact.get("exclusion_counts", {})),
        "scored_window_statement": metrics_artifact.get("scored_window_statement"),
    }
    if per_station:
        artifact["driver_identity_caveat"] = DRIVER_IDENTITY_CAVEAT
    assert_breakdown_stamps(artifact)
    assert_headline_role(artifact)
    require_provenance_block(artifact, mask=mask, surface=surface)
    if per_station:
        require_driver_caveat(artifact, surface=surface)
    return artifact


def build_dec_regime_breakdown(
    *,
    metrics_artifact: Mapping[str, Any],
    mask: Any,
    kp: Any,
    audit: Mapping[str, Any],
    experiment: Mapping[str, Any],
    release_grade: str,
    source: str,
    demotion_record: Mapping[str, Any] | None = None,
    g05_freeze_utc: Any | None = None,
) -> dict[str, Any]:
    """W-2's DEC regime breakdown: post-receipt by construction, guarded by the
    REGISTERED count, divergence-checked, outside-event-excluded.

    Post-receipt by construction: this function takes the emitted metrics artifact —
    which cannot exist before R-109's verified hash receipt — never raw predictions, so
    no pre-G-05 December performance channel opens here (ML-02).

    Raises
    ------
    RegimeError
        an unregistered audit or absent count; audit-vs-comparison divergence (control
        (31)); an unfrozen December day range (TE §18.3); a post-freeze demotion
        (control (6)); a wholly-outside event counted (control (40)); source/grade
        refusals at the one counting path.
    """
    partition = str(getattr(mask, "partition_id", ""))
    if partition != LOCKED_ID:
        raise RegimeError(
            f"DEC regime breakdown over mask {getattr(mask, 'mask_id', '?')}",
            f"mask partition is {partition!r}, not the locked partition {LOCKED_ID!r}; "
            f"the DEC regime breakdown is defined over the locked partition only (W-2)",
        )
    config = read_regime_config(experiment)
    registered_count, audit_id = read_audit_storm_count(audit)
    if demotion_record is not None:
        if g05_freeze_utc is None:
            raise RegimeError(
                f"H4/SRQ-5 demotion record {demotion_record.get('record_id', '<no id>')}",
                "a demotion record was supplied without the G-05 freeze timestamp; the "
                "ordering assertion cannot run unordered (FR-P1-05-18 clause 2)",
            )
        assert_demotion_precedes_freeze(demotion_record, g05_freeze_utc=g05_freeze_utc)
    scored_start, scored_end = read_december_day_range(config)
    activate_regime_config(experiment)
    _, events = count_storm_events(kp, release_grade=release_grade, source=source)
    eligible, outside = eligible_storm_events(
        events, scored_start=scored_start, scored_end=scored_end
    )
    assert_events_eligible_for_threshold(
        eligible, scored_start=scored_start, scored_end=scored_end
    )
    comparison_count = len(eligible)
    assert_audit_count_consistency(
        registered_count=registered_count,
        comparison_count=comparison_count,
        audit_artifact_id=audit_id,
        kp_resource=f"the DEC Kp series over {scored_start.isoformat()}..{scored_end.isoformat()}",
    )
    descriptive_only = registered_count < config.event_threshold
    payload: dict[str, Any] = {
        # the REGISTERED count is the guard's sole governing input; the comparison count
        # exists for divergence detection only and never substitutes (R-124).
        "registered_storm_event_count": registered_count,
        "registered_audit_artifact_id": audit_id,
        "comparison_storm_event_count": comparison_count,
        "descriptive_only": descriptive_only,
        "events_wholly_outside_scored_set": [list(event) for event in outside],
        "eligible_event_intervals": [list(event) for event in eligible],
    }
    return build_breakdown_artifact(
        breakdown_id="regime_split_dec",
        metrics_artifact=metrics_artifact,
        mask=mask,
        payload=payload,
    )


def assert_descriptive_only_label(breakdown: Mapping[str, Any], *, config: RegimeConfig) -> None:
    """Control (5): a December regime breakdown missing the descriptive-only label when
    the REGISTERED count is below the D-13 threshold FAILS. The converse must NOT fire: a
    registered count at the threshold or above renders confirmatory rows undemoted."""
    payload = breakdown.get("payload", {})
    registered = int(payload.get("registered_storm_event_count", -1))
    if registered < 0:
        raise RegimeError(
            f"breakdown {breakdown.get('breakdown_id', '?')}",
            "no registered_storm_event_count on the DEC regime payload; the guard reads "
            "the registered count, never recomputes it (R-124)",
        )
    if registered < config.event_threshold and payload.get("descriptive_only") is not True:
        raise RegimeError(
            f"breakdown {breakdown.get('breakdown_id', '?')}",
            f"registered count {registered} is below D-13's threshold "
            f"({config.event_threshold}) and the descriptive_only label is absent; "
            f"December regime results are descriptive-only unless the registered "
            f"pre-G-05 audit records the threshold (FR-P1-05-16; R-124 control (5))",
        )


# =======================================================================================
# W-6: practical relevance and post-access discipline
# =======================================================================================


def practical_relevance_statement(
    *,
    threshold_record: Mapping[str, Any],
    budget_artifact: Mapping[str, Any],
    measured_improvement: Mapping[str, Any] | None,
    g06_receipt_utc: Any,
) -> dict[str, Any]:
    """W-6: the ONLY producing path for any practical-relevance statement.

    Reads the frozen record and compares; invents no number and reinterprets none
    (PC-09). Evaluates BOTH Vision §5.3 conjuncts: the measured improvement against
    §5.4's named reference magnitude (reported as such — a reference magnitude, not a
    pass/fail rule), and the reference against the target uncertainty budget, emitting
    the descriptive-only label where the reference is smaller than the budget.

    Raises
    ------
    RegimeError
        a threshold timestamp that does not precede the G-06 receipt (control (19)); a
        non-TECU input (control (20)); a missing measured improvement leaving §5.3's
        first conjunct unevaluated (control (35)); a measured improvement without its
        `derived: true` label.
    """
    surface = "practical-relevance statement"
    recorded = threshold_record.get("recorded_at_utc")
    if not recorded:
        raise RegimeError(surface, "the threshold record carries no recorded_at_utc (PC-09)")
    recorded_at = _as_utc(recorded, resource="practical-relevance threshold record")
    receipt_at = _as_utc(g06_receipt_utc, resource="G-06 receipt timestamp")
    if not recorded_at < receipt_at:
        raise RegimeError(
            surface,
            f"threshold recorded at {recorded_at.isoformat()} does not precede the G-06 "
            f"receipt at {receipt_at.isoformat()}; no practical-relevance threshold is "
            f"introduced, changed or reinterpreted after the December locked test is "
            f"opened (PC-09; R-128 control (19))",
        )
    require_units(threshold_record, surface=f"{surface} (threshold record)")
    require_units(budget_artifact, surface=f"{surface} (budget artifact)")
    if measured_improvement is None:
        raise RegimeError(
            surface,
            "the measured improvement (the derived percentage RMSE reduction) is absent, "
            "leaving Vision §5.3's FIRST conjunct unevaluated; a practical-relevance "
            "statement without it refuses (Rec 20; R-128 control (35))",
        )
    require_derived_label(measured_improvement, surface=surface)
    reference = threshold_record.get("reference_magnitude")
    if not isinstance(reference, Mapping) or "value" not in reference:
        raise RegimeError(
            surface,
            "the frozen record carries no reference_magnitude value; §5.4's reference is "
            "read from the record, never invented here (PC-09)",
        )
    budget_value = budget_artifact.get("budget_value")
    if budget_value is None:
        raise RegimeError(
            surface, "the budget artifact carries no budget_value to compare against (§5.4)"
        )
    reference_value = float(reference["value"])
    statement: dict[str, Any] = {
        "kind": "practical_relevance_statement",
        "first_conjunct": {
            "measured_improvement": dict(measured_improvement),
            "reference_magnitude": dict(reference),
            "measured_reaches_reference": float(measured_improvement["value"])
            >= reference_value,
            "note": "a named reference magnitude, not a pass/fail rule (Vision §5.4)",
        },
        "second_conjunct": {
            "reference_value": reference_value,
            "budget_value": float(budget_value),
            "reference_smaller_than_budget": reference_value < float(budget_value),
        },
        "units": threshold_record.get("units"),
        "threshold_recorded_at_utc": recorded_at.isoformat(),
    }
    if reference_value < float(budget_value):
        statement["label"] = "descriptive-only"
    return statement


def assert_post_access_labelled(
    runs: Sequence[Mapping[str, Any]], *, access_events: Sequence[Mapping[str, Any]]
) -> None:
    """Control (21): a run reported after a recorded `locked_test_accessed = true` event
    without the exploratory label FAILS. Which surface WRITES the label is the registry
    writer's design, routed to the gate — this unit checks the surface it can see.

    Raises
    ------
    RegimeError
        a post-access run whose `label` is not "exploratory".
    """
    access_times = [
        _as_utc(event["retrieved_at_utc"], resource="access event")
        for event in access_events
        if event.get("locked_test_accessed") is True
    ]
    if not access_times:
        return
    first_access = min(access_times)
    for run in runs:
        run_at = _as_utc(run["timestamp_utc"], resource=f"run {run.get('run_id', '?')}")
        if run_at > first_access and run.get("label") != "exploratory":
            raise RegimeError(
                f"run {run.get('run_id', '?')}",
                f"registry timestamp {run_at.isoformat()} postdates the first recorded "
                f"locked_test_accessed event at {first_access.isoformat()} and the run "
                f"carries no exploratory label (Vision §8.3; FR-P1-05-14; R-128 control "
                f"(21))",
            )


# =======================================================================================
# W-8: the diagnostics quarantine
# =======================================================================================


def build_dst_diagnostic(
    series_rows: Sequence[Mapping[str, Any]], *, release_grades: Sequence[str]
) -> dict[str, Any]:
    """A Dst hindcast diagnostic artifact: single recorded grade, labelled, lane-bound.

    Raises
    ------
    RegimeError
        two release grades mixed in one series (D-10.1; control (25)), or no grade.
    """
    grades = sorted({str(g) for g in release_grades})
    if len(grades) != 1:
        raise RegimeError(
            "Dst diagnostic series",
            f"release grades {grades or '<none>'} — a series carries exactly ONE recorded "
            f"grade; mixing real-time, provisional and final within one series is barred "
            f"(D-10.1; R-130 control (25))",
        )
    return {
        "artifact_class": "dst_diagnostic",
        "kind": "dst_diagnostic",
        "diagnostic_label": DIAGNOSTIC_LABEL,
        "release_grade": grades[0],
        "rows": [dict(r) for r in series_rows],
    }


def assert_grade_eligible(release_grade: str, *, surface: str) -> None:
    """Control (28): a provisional-grade series reaching an R-62-barred surface RAISES at
    the point of use — eligibility is a property of the data, read from the grade field.

    Raises
    ------
    RegimeError
        provisional grade at a modelling input, a frozen tolerance, or a G-05 regime
        count.
    """
    if surface in R62_BARRED_SURFACES and str(release_grade).lower() == "provisional":
        raise RegimeError(
            f"Dst series (grade {release_grade!r}) at surface {surface!r}",
            "a provisional-grade series may characterise selection only and never becomes "
            "a modelling input, a frozen tolerance, or a G-05 regime count (R-62 "
            "restriction 3; D-11; R-130 control (28))",
        )


def assert_no_diagnostic_field(artifact: Mapping[str, Any]) -> None:
    """Control (26): a diagnostic-labelled field found in any feature-bearing or metrics
    artifact FAILS the quarantine presence test (TC-11).

    Raises
    ------
    RegimeError
        the diagnostic label found anywhere inside the artifact.
    """

    def _scan(node: Any, trail: str) -> None:
        if isinstance(node, Mapping):
            for key, value in node.items():
                _scan(value, f"{trail}.{key}")
        elif isinstance(node, list | tuple):
            for index, value in enumerate(node):
                _scan(value, f"{trail}[{index}]")
        elif node == DIAGNOSTIC_LABEL:
            raise RegimeError(
                f"artifact {artifact.get('artifact_id', artifact.get('set_id', '?'))}",
                f"diagnostic-labelled field at {trail}; Dst hindcast artifacts live only "
                f"under diagnostic paths — never in the metrics artifact, the primary "
                f"table, or any feature-bearing artifact (TC-11; R-130 control (26))",
            )

    _scan(artifact, "artifact")


def rf_importance_figure_source(artifact: Mapping[str, Any]) -> dict[str, Any]:
    """R-100/R-130: the RF-importance figure renders ONLY from the saved diagnostic
    artifact whose own metadata records `authoritative = false`; the render input carries
    the non-authoritative label printed from that metadata.

    Raises
    ------
    RegimeError
        metadata absent, or `authoritative` not exactly False (control (27)).
    """
    metadata = artifact.get("metadata")
    if not isinstance(metadata, Mapping) or metadata.get("authoritative") is not False:
        raise RegimeError(
            f"RF-importance artifact {artifact.get('artifact_id', '?')}",
            "metadata does not record authoritative = false; RF importance is a "
            "non-authoritative diagnostic, never a selection input, and the figure "
            "renders only from the labelled artifact (R-100; R-130 control (27))",
        )
    return {
        "source_artifact": dict(artifact),
        "caveat_labels": (NON_AUTHORITATIVE_LABEL,),
    }


# =======================================================================================
# W-4: the claims-and-limitations checklist
# =======================================================================================


def _artifact_text(artifact: Mapping[str, Any]) -> str:
    return json.dumps(dict(artifact), sort_keys=True, default=str)


def _conclusion_surfaces(
    registry: ConclusionSurfaceRegistry | None,
    conclusion_surface: Mapping[str, Any] | None,
) -> Mapping[str, str]:
    """Rec 21's fail-closed resolution of the checked text's declared subject."""
    resource = "ConclusionSurfaceArtifact"
    if conclusion_surface is None:
        raise RegimeError(
            resource,
            "absent; every text-surface row resolves against the registered, hash-listed "
            "conclusion surface and a checklist run without it FAILS CLOSED, never "
            "skipped (Rec 21; R-126 control (36)) — the rows it would have carried: "
            "beats_model conclusions, plasmaspheric, VAL-05, D-28 scored set, "
            "NFR-TDEF-01",
        )
    artifact_id = str(conclusion_surface.get("conclusion_artifact_id", ""))
    require_registered_surface(
        artifact_id or "<no id>", registry=registry, surface=resource
    )
    if not conclusion_surface.get("manifest_ref"):
        raise RegimeError(
            f"{resource} {artifact_id}",
            "manifest_ref is absent — the artifact is unmanifested; TE §15.4's closing "
            "rule hash-lists every output in artifact_manifest.json and an unmanifested "
            "surface fails closed (control (36))",
        )
    surfaces = conclusion_surface.get("surfaces")
    expected = ("abstract_level_interpretation", "conclusion", "limitations")
    if not isinstance(surfaces, Mapping) or sorted(surfaces) != sorted(expected):
        raise RegimeError(
            f"{resource} {artifact_id}",
            f"surfaces {sorted(surfaces) if isinstance(surfaces, Mapping) else '<none>'} "
            f"do not enumerate exactly {sorted(expected)} (domain-entities § 6)",
        )
    return {key: str(value) for key, value in surfaces.items()}


def build_claims_checklist(
    *,
    registry: ConclusionSurfaceRegistry | None,
    conclusion_surface: Mapping[str, Any] | None,
    table: Mapping[str, Any],
    breakdowns: Sequence[Mapping[str, Any]] = (),
    notebook_captions: Mapping[str, str] | None = None,
    gim_overlap_has_run: bool = False,
    post_access_report: Mapping[str, Any] | None = None,
    checklist_artifact_id: str = "claims_checklist",
) -> dict[str, Any]:
    """W-4: the machine-readable claims-and-limitations checklist artifact.

    One row per prohibited class (the enumeration maintained in `requirements.md`
    § Out of scope C only, cited by reference, never duplicated) and one row per mandated
    disclosure, each recording where the text was found — a registered artifact ID plus a
    surface plus a location — or FAILING. The residue (whether found text MEANS what the
    rule requires) stays human and is recorded per row. The checklist inspects EXACTLY
    the registered surface set, states the hand-authored-prose residual, and never claims
    full enforcement.

    Raises
    ------
    RegimeError
        an absent, unmanifested or unregistered conclusion surface (fail-closed,
        control (36)).
    """
    surfaces = _conclusion_surfaces(registry, conclusion_surface)
    conclusion_id = str(conclusion_surface.get("conclusion_artifact_id"))  # type: ignore
    registered_set = registry.ids() if registry is not None else ()

    reported: dict[str, Mapping[str, Any]] = {
        str(table.get("artifact_id", "primary_table")): table
    }
    for breakdown in breakdowns:
        reported[str(breakdown.get("artifact_id", breakdown.get("breakdown_id", "?")))] = (
            breakdown
        )

    rows: list[dict[str, Any]] = []

    # --- prohibited-class rows (planted-phrase detection; REQ-CLAIM-01) -----------------
    all_texts = {aid: _artifact_text(a).lower() for aid, a in reported.items()}
    all_texts[f"{conclusion_id}/surfaces"] = " ".join(surfaces.values()).lower()
    for spec in PROHIBITED_CLASS_ROWS:
        hits: list[str] = []
        for location, text in all_texts.items():
            for phrase in spec["detection_phrases"]:
                # a phrase asserted as the standing CAVEAT is not an assertion of the
                # prohibited claim: the caveat sentence itself is excluded from detection.
                if phrase.lower() in text.replace(DRIVER_IDENTITY_CAVEAT.lower(), ""):
                    hits.append(f"{location}: {phrase!r}")
        rows.append(
            {
                "row_kind": "prohibited_class",
                "reference": spec["reference"],
                "boundary_text": spec["boundary_text"],
                "required_location": "unasserted across every reported artifact",
                "found_at": hits,
                "status": "FAILED — prohibited phrase found" if hits else "unasserted",
                "human_residue": (
                    "detection catches the obvious wording, not a paraphrase; whether "
                    "any text asserts the prohibited class is a human check"
                ),
            }
        )

    # --- disclosure rows -----------------------------------------------------------------
    def _found(condition: bool, where: str) -> tuple[list[str], str]:
        return ([where] if condition else [], "found" if condition else "FAILED")

    # beats_model = true baselines: table AND abstract-level conclusion (FR-P1-05-20)
    winners = [
        str(row.get("benchmark_id"))
        for row in table.get("rows", table.get("comparisons", ()))
        if row.get("beats_model") is True
    ]
    conclusion_text = surfaces["conclusion"] + " " + surfaces["abstract_level_interpretation"]
    for winner in winners:
        found, status = _found(
            winner in conclusion_text,
            f"{conclusion_id}/abstract_level_interpretation+conclusion",
        )
        rows.append(
            {
                "row_kind": "disclosure",
                "reference": "FR-P1-05-20 (binding honesty rule; Vision §2.4)",
                "required_location": "primary table AND abstract-level conclusion",
                "subject": winner,
                "found_at": [f"{table.get('artifact_id')}/rows"] + found,
                "status": status,
                "human_residue": "whether the conclusion text discloses the result fairly",
            }
        )
    if not winners:
        rows.append(
            {
                "row_kind": "disclosure",
                "reference": "FR-P1-05-20 (binding honesty rule; Vision §2.4)",
                "required_location": "primary table AND abstract-level conclusion",
                "subject": "no beats_model = true baseline in this table",
                "found_at": [f"{table.get('artifact_id')}/rows"],
                "status": "found",
                "human_residue": "the flag comparison is a field check; fairness is human",
            }
        )

    # plasmaspheric sentence at its three points (FR-P1-05-19)
    caption = str(table.get("caption", ""))
    for location, text in (
        (f"{table.get('artifact_id')}/caption", caption),
        (
            f"{conclusion_id}/abstract_level_interpretation",
            surfaces["abstract_level_interpretation"],
        ),
        (f"{conclusion_id}/limitations", surfaces["limitations"]),
    ):
        found, status = _found(_PLASMASPHERIC_TOKEN in text.lower(), location)
        rows.append(
            {
                "row_kind": "disclosure",
                "reference": "FR-P1-05-19 (plasmaspheric-offset sentence)",
                "required_location": location,
                "found_at": found,
                "status": status,
                "human_residue": "token detection; whether the sentence means FR-P1-05-19's",
            }
        )

    # VAL-05 at the abstract-level interpretation (control (39))
    found, status = _found(
        _VAL05_FRAGMENT in surfaces["abstract_level_interpretation"].lower()
        or PHASE2_NOT_INDEPENDENT_STATEMENT.lower()
        in surfaces["abstract_level_interpretation"].lower(),
        f"{conclusion_id}/abstract_level_interpretation",
    )
    rows.append(
        {
            "row_kind": "disclosure",
            "reference": "VAL-05 (Phase 2 fixed-protocol replication, not independent)",
            "required_location": "abstract-level interpretation",
            "statement": PHASE2_NOT_INDEPENDENT_STATEMENT,
            "found_at": found,
            "status": status,
            "human_residue": "fragment detection; meaning stays a human check",
        }
    )

    # TEC-06 sentence on every serialized IRI/GIM comparison (presence asserted)
    for aid, artifact in reported.items():
        for row in artifact.get("rows", artifact.get("comparisons", ())):
            if str(row.get("benchmark_id", "")) in EXTERNAL_COMPARATOR_IDS:
                ok = (
                    row.get("spatial_representativeness_sentence")
                    == SPATIAL_REPRESENTATIVENESS_SENTENCE
                )
                found, status = _found(ok, f"{aid}/rows/{row.get('benchmark_id')}")
                rows.append(
                    {
                        "row_kind": "disclosure",
                        "reference": "TEC-06 (spatial representativeness; emitted upstream)",
                        "required_location": "every serialized IRI/GIM comparison artifact",
                        "found_at": found,
                        "status": status,
                        "human_residue": None,
                    }
                )

    # gim_network_overlap_flag wherever GIM is compared, once the audit has run
    if gim_overlap_has_run:
        for aid, artifact in reported.items():
            for row in artifact.get("rows", artifact.get("comparisons", ())):
                if str(row.get("benchmark_id", "")) == "C-01":
                    block = row.get("gim_overlap_disclosure")
                    ok = isinstance(block, Mapping) and "gim_network_overlap_flag" in block
                    found, status = _found(bool(ok), f"{aid}/rows/C-01/gim_overlap_disclosure")
                    rows.append(
                        {
                            "row_kind": "disclosure",
                            "reference": "TE §5.2 (gim_network_overlap_flag)",
                            "required_location": "wherever GIM is compared",
                            "found_at": found,
                            "status": status,
                            "human_residue": None,
                        }
                    )
    else:
        rows.append(
            {
                "row_kind": "disclosure",
                "reference": "TE §5.2 (gim_network_overlap_flag)",
                "required_location": "wherever GIM is compared",
                "found_at": [],
                "status": "conditional — the input-network overlap audit has not run",
                "human_residue": None,
            }
        )

    # driver-identity caveat on every per-station breakdown (emitted by W-5, asserted here)
    for aid, artifact in reported.items():
        if artifact.get("per_station"):
            ok = artifact.get("driver_identity_caveat") == DRIVER_IDENTITY_CAVEAT
            found, status = _found(bool(ok), f"{aid}/driver_identity_caveat")
            rows.append(
                {
                    "row_kind": "disclosure",
                    "reference": "TC-12 standing caveat (Rec 17; emitted by the producing path)",
                    "required_location": "every per-station breakdown artifact",
                    "found_at": found,
                    "status": status,
                    "human_residue": None,
                }
            )

    # the D-28 scored-set disclosure row (Rec 16) — one denominator, one place
    scored_statement = str(table.get("scored_window_statement", ""))
    for location, text in (
        (f"{table.get('artifact_id')}/caption", caption),
        (f"{conclusion_id}/limitations", surfaces["limitations"]),
    ):
        found, status = _found(bool(scored_statement) and scored_statement in text, location)
        rows.append(
            {
                "row_kind": "disclosure",
                "reference": "D-28 (2–31 December 2022, 30 days)",
                "statement": scored_statement,
                "required_location": location,
                "found_at": found,
                "status": status,
                "human_residue": None,
            }
        )

    # NFR-TDEF-01: the cross-phase target-lineage statement — presence asserted, NEVER
    # authored here (Rec 18 limb (3); distinct from TEC-06 and not discharged by it).
    for location, text in (
        (f"{table.get('artifact_id')}/target_lineage_statement",
         str(table.get("target_lineage_statement", ""))),
        (f"{conclusion_id}/limitations", surfaces["limitations"]),
    ):
        found, status = _found("lineage" in text.lower(), location)
        rows.append(
            {
                "row_kind": "disclosure",
                "reference": "NFR-TDEF-01 (cross-phase target lineage; emitted upstream by "
                "target-standardization — presence asserted, nothing authored here)",
                "required_location": "every reported artifact describing the Phase 1 target",
                "found_at": found,
                "status": status,
                "human_residue": "if the upstream path does not write the sentence, this "
                "row fails; this unit never writes a second version",
            }
        )

    # FR-P1-03-4: notebook figure captions describing the Phase 1 target
    if notebook_captions:
        for notebook_id, text in notebook_captions.items():
            rows.append(
                {
                    "row_kind": "disclosure",
                    "reference": "FR-P1-03-4 (notebook-caption review; "
                    "target-standardization R-69)",
                    "required_location": "every notebook figure caption describing the "
                    "Phase 1 target",
                    "found_at": [f"notebook {notebook_id}"],
                    "status": "reached — human review required",
                    "human_residue": "whether a caption MEANS what the rule requires is a "
                    "human check; this row makes the review reach a surface only",
                }
            )
    else:
        rows.append(
            {
                "row_kind": "disclosure",
                "reference": "FR-P1-03-4 (notebook-caption review; target-standardization R-69)",
                "required_location": "every notebook figure caption describing the Phase 1 target",
                "found_at": [],
                "status": "FAILED — no notebook caption surface supplied (fail-closed, "
                "never skipped)",
                "human_residue": "human check once a surface exists",
            }
        )

    checklist: dict[str, Any] = {
        "artifact_id": str(checklist_artifact_id),
        "artifact_class": "claims_checklist",
        "kind": "claims_checklist",
        "inspected_registered_set": list(registered_set),
        "conclusion_artifact_id": conclusion_id,
        "rows": rows,
        "claim_boundary": D8_CLAIM_BOUNDARY,
        "nico_5min_bar": D7_NICO_5MIN_BAR,
        "phase2_not_independent_statement": PHASE2_NOT_INDEPENDENT_STATEMENT,
        "scored_window_statement": scored_statement,
        "residual": CHECKLIST_RESIDUAL,
        "post_access_report": dict(post_access_report) if post_access_report else None,
        # stamps copied from the table artifact (TEC-05)
        "phase_id": table.get("phase_id"),
        "source_id": table.get("source_id"),
        "target_definition_id": table.get("target_definition_id"),
    }
    return checklist


# =======================================================================================
# W-9: the notebook declaration helper
# =======================================================================================


def declare_notebook_inputs(
    *,
    notebook_id: str,
    dataset_version: str,
    code_commit: str,
    config_ids: Mapping[str, str],
    artifact_ids: Sequence[str],
    workspace: Path | None = None,
    never_executed_note: str | None = None,
) -> dict[str, Any]:
    """W-9's first-cell helper: declare, verify, and STOP before any later cell runs.

    Emits the header-declaration block in a fixed machine-readable form (TA-16's evidence
    is a parse, not a screenshot) and verifies every declared artifact resolves under the
    workspace — REQ-ENG-12's "Run all" semantics by construction: the notebook either
    proceeds from declared inputs or stops with the stated message.

    Raises
    ------
    RegimeError
        any declared field empty, or any declared artifact missing (naming every missing
        one, so a human fixes them in one pass).
    """
    resource = f"notebook {notebook_id} declaration"
    empty = [
        name
        for name, value in (
            ("dataset_version", dataset_version),
            ("code_commit", code_commit),
        )
        if not str(value).strip()
    ]
    if empty or not config_ids:
        raise RegimeError(
            resource,
            f"declared field(s) {empty or ['config_ids']} empty; the declaration names "
            f"the expected dataset version, code commit, configuration IDs and artifact "
            f"IDs before any later cell runs (REQ-ENG-12; TE §14)",
        )
    root = Path(workspace) if workspace is not None else Path.cwd()
    missing = [str(a) for a in artifact_ids if not (root / str(a)).exists()]
    if missing:
        raise RegimeError(
            resource,
            f"declared input artifact(s) {missing} are missing under {root}; STOPPING "
            f"before any later cell runs — 'Run all' never proceeds on partial state, "
            f"and on Kaggle a network-dependent input additionally requires Settings > "
            f"Internet: On (REQ-ENG-12's stated stop message)",
        )
    header = {
        "header_declaration": {
            "notebook_id": str(notebook_id),
            "dataset_version": str(dataset_version),
            "code_commit": str(code_commit),
            "config_ids": dict(config_ids),
            "artifact_ids": [str(a) for a in artifact_ids],
            "declared_at_utc": dt.datetime.now(dt.UTC).isoformat(),
            "never_executed_note": never_executed_note,
        }
    }
    print(json.dumps(header, sort_keys=True))  # TA-16: machine-parsed fixed form
    return header


def register_notebook_conclusion(
    registry_root: Path,
    *,
    notebook_id: str,
    conclusion_text: str,
    phase_id: str,
    source_id: str,
    target_definition_id: str,
) -> Path:
    """Register a notebook's conclusion cell as a ConclusionSurfaceArtifact surface
    (Q1 = A: notebook conclusion cells are registered surfaces, inspected by the
    checklist like any other location; the registration is metadata on the emitted
    artifact, not logic in the notebook)."""
    registry = ConclusionSurfaceRegistry(Path(registry_root))
    return registry.register(
        {
            "artifact_id": f"notebook-conclusion-{notebook_id}",
            "kind": "notebook_conclusion_cell",
            "phase_id": phase_id,
            "source_id": source_id,
            "target_definition_id": target_definition_id,
            "conclusion_text": str(conclusion_text),
        }
    )
