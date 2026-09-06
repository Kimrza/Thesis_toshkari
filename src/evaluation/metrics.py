"""C3/C5/C6 metrics: the ordered estimand, the DEC chokepoint composition, honesty by construction.

Purpose
-------
`evaluation-and-comparison` W-2 / W-5 / W-6, R-104/R-105/R-108/R-109/R-110/R-112:

* ``paired_loss_differential`` — the confirmatory estimand as ONE ordered executable
  pipeline (R-108; Vision §2.3; TE §1.3): guards FIRST (registered frozen mask for the
  members' declared set; stamps against the mask's recorded stamps; partition agreement;
  member-vs-mask alignment; target space; on `DEC`, the full `require_locked_receipt`
  composition), then (1) squared errors per (`station`, hour) on masked rows only,
  (2) per-station mean of paired differences **benchmark minus model**, (3) the unweighted
  mean of the per-station values (**equal-station** weighting, never pooled row-weighting).
* ``paired_difference_series`` / ``equal_station_mean`` — R-108's step 1 and steps 2–3 as
  named, importable pieces. Extracted 2026-09-06 per
  `governance/CHANGE_RECORD_2026-09-06_R119_bootstrap_confirmations.md` so
  `statistical-inference`'s `vector_block_bootstrap` resamples **the same code path** the
  estimand runs, rather than a second drift-prone copy (its R-114 one-copy rule; §14).
  Behaviour-preserving: same arithmetic, same iteration order, same raises;
  ``paired_loss_differential``'s signature and results are unchanged. This in-place edit
  to a READY-reviewed module is flagged for this unit's own record and re-check at its
  next touch, the same disposition as the Q2 = B `locked_test.py` edit.
* ``EstimandResult`` — the result carries its own interpretation: orientation
  ``benchmark_minus_model``, weighting ``equal_station``, the machine-readable
  sign-convention sentence, and the four mandated stamps (`phase_id`, `source_id`,
  `target_definition_id`, `partition_id`) COPIED from the registered mask at construction —
  a missing or mask-disagreeing stamp FAILS (control 30; Recommendation 35).
* ``build_metrics_artifact`` — W-6's three limbs as computable preconditions: the
  completeness refusal per declared set (any missing member's estimand refuses emission —
  control 24); ``beats_model`` per benchmark, derived from the estimand's sign and deciding
  nothing scientific (control 27); and the emitted disclosures — the TEC-06
  spatial-representativeness sentence on every serialized IRI/GIM comparison (control 25),
  the FAIL-CLOSED GIM overlap disclosure (no registered overlap-audit result →
  `FairnessError`, control 26; ordering by CONTAINMENT — the comparator records the audit
  result's ID and content hash found at generation, control 32), and the Phase-2
  not-independent-blind-test statement as an artifact field (VAL-05's mandated disclosure).

IRI/GIM boundary (R-112)
------------------------
`src/evaluation` is a permitted §12 importer of `src/external/iri.py`/`gim.py`; this module
imports `src/external/gim` at EVALUATION TIME ONLY — a deferred import inside the GIM
disclosure path, reached only after ``require_registered_mask`` has passed, so the join
lands on an already-registered frozen mask (NFR-IRI-01's join point; control 29). The
justification `logical-components.md` asks 3.5 to state: `gim.render_comparison_report` is
the disclosure chokepoint `external-products` R-60 owns, and rendering the GIM block through
it keeps ONE copy of that emission logic rather than a second drift-prone copy here. This
unit's own fail-closed refusal (`FairnessError`, SD-C-04) runs FIRST, so the refusal type at
this boundary is this unit's contract. `src/external/iri.py` is NOT imported: no path in
this module needs it (B-01 arrives as a generated, stamped prediction), and the allowlist is
permission, not obligation.

Inputs
------
Prediction-like objects (approved eight-field shape, structural), a `ComparisonMask` and
`MaskRegistry` (`src/evaluation/masks.py`), the declared sets from `ConfigSnapshot`, and —
on `DEC` only — the prediction file + hash receipt, the access record written by
`governance-guards`' `open_restricted`, and the frozen-bundle manifest. **No `src/features`
and no `src/models` import, direct or transitive** (D-27); `ABL-DIFF` refuses at
``guards.require_target_space``/``guards.resolve_inverse`` naming D-27, exactly as
`src/models/train.py` built it.

Re-run behaviour
----------------
Pure computation over supplied artifacts; nothing here writes the registry or the locked
test. ``write_metrics_artifact`` refuses to overwrite an existing artifact (NFR-AUD-01's
no-silent-replacement posture) and writes durably via `.tmp` → fsync → atomic rename.
Deterministic given identical inputs.

Governance
----------
No practical-relevance threshold is stated, introduced or reinterpreted anywhere in this
module (PC-09): this unit computes the estimand and emits fields; thresholds are not its to
state. Bootstrap intervals are `statistical-inference`'s (TS-C-02) and breakdown tables are
`regimes-diagnostics-reporting`'s — neither is computed here. FR-P1-05-7 stays `Pending`
(row approved under D-32, never run); FR-P1-05-17 stays `UNTESTED`; G-05/G-06 stay
`Blocked`; nothing here discharges an acceptance row.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.data.config import FairnessError, IntegrityError
from src.data.splits import LOCKED_ID
from src.evaluation.guards import (
    require_locked_receipt,
    require_mask_member_alignment,
    require_partition_agreement,
    require_registered_mask,
    require_stamps,
    require_target_space,
)
from src.evaluation.masks import ComparisonMask

__all__ = [
    "ORIENTATION",
    "WEIGHTING",
    "SIGN_CONVENTION_SENTENCE",
    "SPATIAL_REPRESENTATIVENESS_SENTENCE",
    "PHASE2_NOT_INDEPENDENT_STATEMENT",
    "EXTERNAL_COMPARATOR_IDS",
    "LockedContext",
    "EstimandResult",
    "paired_difference_series",
    "equal_station_mean",
    "paired_loss_differential",
    "build_metrics_artifact",
    "assert_metrics_artifact",
    "write_metrics_artifact",
]

#: Vision §2.3's binding convention — identity tokens carried machine-readably (R-108).
ORIENTATION: str = "benchmark_minus_model"
WEIGHTING: str = "equal_station"
SIGN_CONVENTION_SENTENCE: str = (
    "positive values favour the model: the differential is benchmark minus model"
)

#: TEC-06's mandated caveat, quoted from the governing documents (Vision §6.6; TE §5) —
#: wording fixed there, not invented here; emitted by the producing path on EVERY
#: serialized IRI/GIM comparison (R-110 limb 3; R-60's emit-from-the-path pattern).
#: `src/external/gim.py` carries its own fuller two-phase variant for the comparator's
#: report; this is the comparison-artifact sentence R-110 quotes.
SPATIAL_REPRESENTATIVENESS_SENTENCE: str = (
    "Phase 1 compares a grid cell against a station-coordinate evaluation, and part of any "
    "measured difference is a geometry and sampling artefact rather than skill"
)

#: VAL-05's mandated abstract-level disclosure (Vision §2.2, §7.0B; project.md Mandated),
#: carried as an artifact FIELD so the reporting unit asserts presence instead of prose.
PHASE2_NOT_INDEPENDENT_STATEMENT: str = (
    "Phase 2 is a fixed-protocol replication on a new target lineage, not a second "
    "statistically independent blind test, because it reuses the December timestamps after "
    "Phase 1 has already reported them"
)

#: The two externally generated comparison members (identities, not values): B-01 is the
#: IRI-generated benchmark, C-01 the CODE-final-GIM comparator. Every comparison row
#: naming one of them is an "IRI/GIM comparison" for R-110 limb 3's disclosures.
EXTERNAL_COMPARATOR_IDS: tuple[str, ...] = ("B-01", "C-01")
_GIM_COMPARATOR_ID: str = "C-01"


@dataclass(frozen=True)
class LockedContext:
    """Everything a `DEC` metric entry point must be handed to satisfy R-109's three limbs.

    Assembled by `scripts/07_evaluate_and_report.py` AFTER `materialise_locked_partition`'s
    G-05 signature guard and `open_restricted`'s log-then-read door — this unit constructs
    no path of its own into the restricted root (R-28). `access_record` is the record
    `open_restricted` wrote (carrying the SD-C-02 containment fields when a frozen-bundle
    manifest existed at access time); `month_start`/`month_end`/`embargo_hours` are the
    locked partition's own values, reaching here from configuration.
    """

    prediction_path: Path
    receipt_path: Path
    access_record: Any
    mask_bundle_manifest: Path | None
    month_start: dt.datetime
    month_end: dt.datetime
    embargo_hours: int


@dataclass(frozen=True)
class EstimandResult:
    """`domain-entities.md` § 4: the result carries its own interpretation.

    The four mandated stamps are copied from the registered mask at construction
    (Recommendation 35): a fold-validation differential and the G-06 locked-test
    differential are distinguishable on their own faces, and `target_definition_id` travels
    wherever a differential is reported (Vision §2.2/§6.6's no-target-equivalence rule).
    Construction VALIDATES: a missing stamp, a non-canonical orientation/weighting/sentence,
    or a per-station map inconsistent with the scalar fails (control 30's presence half;
    the mask-agreement half is enforced where the mask is in hand, in
    ``paired_loss_differential`` and ``assert_metrics_artifact``).
    """

    scalar: float
    per_station: Mapping[str, float]
    orientation: str
    weighting: str
    sign_convention_sentence: str
    mask_id: str
    set_id: str
    model_id: str
    benchmark_id: str
    phase_id: str
    source_id: str
    target_definition_id: str
    partition_id: str

    def __post_init__(self) -> None:
        if self.orientation != ORIENTATION:
            raise FairnessError(
                f"EstimandResult {self.model_id} vs {self.benchmark_id}",
                f"orientation {self.orientation!r} is not {ORIENTATION!r}; Vision §2.3's "
                f"convention is benchmark minus model, machine-readably (R-108)",
            )
        if self.weighting != WEIGHTING:
            raise FairnessError(
                f"EstimandResult {self.model_id} vs {self.benchmark_id}",
                f"weighting {self.weighting!r} is not {WEIGHTING!r}; equal-station "
                f"weighting is the estimand's fixed aggregation (R-108)",
            )
        if self.sign_convention_sentence != SIGN_CONVENTION_SENTENCE:
            raise FairnessError(
                f"EstimandResult {self.model_id} vs {self.benchmark_id}",
                "sign-convention sentence differs from Vision §2.3's binding wording; the "
                "convention travels as data, not as a remembered sentence (R-108)",
            )
        missing = [
            name
            for name in ("phase_id", "source_id", "target_definition_id", "partition_id")
            if not getattr(self, name)
        ]
        if missing:
            raise FairnessError(
                f"EstimandResult {self.model_id} vs {self.benchmark_id}",
                f"mandated stamp(s) {missing} absent; the comparison is one of the four "
                f"stamp targets (TE §13; project.md Mandated; control 30)",
            )
        if not self.per_station:
            raise FairnessError(
                f"EstimandResult {self.model_id} vs {self.benchmark_id}",
                "per_station components absent; the equal-station mean is over the "
                "per-station values and a result without them cannot evidence its own "
                "aggregation (R-108)",
            )


def _stamps_match_mask(result: EstimandResult, mask: Any) -> None:
    """Control (30)'s agreement half: the four copied stamps equal the registered mask's."""
    for name in ("phase_id", "source_id", "target_definition_id", "partition_id"):
        own = str(getattr(result, name))
        recorded = str(getattr(mask, name))
        if own != recorded:
            raise FairnessError(
                f"EstimandResult {result.model_id} vs {result.benchmark_id}",
                f"stamp {name} {own!r} differs from the registered mask's {recorded!r}; "
                f"the stamps are copied from the mask at construction and drift is a "
                f"failure, not a discrepancy (R-108, Recommendation 35)",
            )


def paired_difference_series(
    model_id: str, benchmark_id: str, mask: Any
) -> dict[str, list[tuple[str, float]]]:
    """R-108 step 1, ONE copy project-wide (this unit's R-108; the sibling's R-114).

    The per-(`station`, hour) paired squared-error difference series d_s(t) — **benchmark
    minus model** — computed on masked rows only, paired per station-hour on the
    (`station`, `interval_start_utc`) alignment key (R-92) BEFORE differencing. Returns,
    per station, the ordered list of (`interval_start_utc`, difference) in masked-row
    order. `statistical-inference`'s bootstrap resamples blocks of THIS series; no
    differencing arithmetic exists anywhere else (§14's one-copy rule).

    Raises
    ------
    FairnessError
        a masked row carrying no y_hat for either member — a mask-construction failure
        (R-108 step 1).
    """
    series: dict[str, list[tuple[str, float]]] = {}
    for row in mask.masked_rows:
        y_true = float(row["y_true"])
        y_hats = row["y_hats"]
        if model_id not in y_hats or benchmark_id not in y_hats:
            raise FairnessError(
                f"mask {mask.mask_id} row {row['station']}/{row['interval_start_utc']}",
                f"carries no y_hat for {model_id!r} or {benchmark_id!r}; the estimand is "
                f"computed on masked rows only, and a masked row missing a member is a "
                f"mask-construction failure (R-108 step 1)",
            )
        se_model = (y_true - float(y_hats[model_id])) ** 2
        se_benchmark = (y_true - float(y_hats[benchmark_id])) ** 2
        series.setdefault(str(row["station"]), []).append(
            (str(row["interval_start_utc"]), se_benchmark - se_model)
        )
    return series


def equal_station_mean(
    per_station_values: Mapping[str, Sequence[float]],
) -> tuple[float, dict[str, float]]:
    """R-108 steps 2–3, ONE copy project-wide: per-station mean, then the unweighted mean.

    Step 2: the per-station mean of the supplied paired differences (orientation is the
    series producer's — benchmark minus model). Step 3: the unweighted mean of the
    per-station values — **equal-station** weighting, never pooled row-weighting (the
    asymmetric-count fixture distinguishes the two by construction, control (16)).
    The bootstrap's replicate statistic reapplies exactly these two steps to drawn rows.

    Raises
    ------
    IntegrityError
        a station with zero values — the equal-station mean is undefined over an empty
        per-station series (the bootstrap raises its own `BootstrapError` for this
        condition BEFORE calling here, naming the station and window — R-116).
    """
    for station, values in per_station_values.items():
        if not values:
            raise IntegrityError(
                f"station {station}",
                "carries zero rows; the equal-station mean is undefined over an empty "
                "per-station series (R-108 steps 2-3)",
            )
    per_station = {
        station: sum(values) / len(values)
        for station, values in sorted(per_station_values.items())
    }
    scalar = sum(per_station.values()) / len(per_station)  # unweighted: equal station
    return scalar, per_station


def paired_loss_differential(
    model: Any,
    benchmark: Any,
    *,
    mask: ComparisonMask,
    declared_sets: Mapping[str, Mapping[str, Any]],
    registry: Any,
    locked: LockedContext | None = None,
) -> EstimandResult:
    """R-108 / W-2: the confirmatory estimand, guards first, then the ordered pipeline.

    Preconditions, in order (each a named guard — SD-C-01's per-entry invocation): the mask
    is a registered frozen mask for the members' declared comparison set (`FairnessError`
    otherwise — an unregistered or ad-hoc mask is an ERROR, not a wrong number; this is also
    R-112's join-point check for any externally generated member, control 29); both
    predictions pass the stamp check against the mask's recorded stamps (`LeakageError`),
    agree on `partition_id` (`PartitionError`), align with the mask's recorded partition
    (`FairnessError` — the sixth guard), and pass the target-space check
    (`InverseTransformError` — un-inverted `ABL-DIFF` refuses naming D-27); on `DEC`,
    R-109's full receipt/containment/window composition holds (`LockedTestError`;
    ``locked=None`` on a `DEC` mask refuses fail-closed).

    The pipeline (Q6 = D): squared errors per (`station`, hour) on masked rows only →
    per-station mean of paired differences, **benchmark minus model** → unweighted mean of
    the per-station values (equal-station; in production the three stations, asserted by
    the fixture — never pooled row-weighting, which control (16)'s asymmetric fixture
    distinguishes by construction).

    Returns an `EstimandResult` whose four stamps are copied from the registered mask.
    """
    members = (model, benchmark)
    require_registered_mask(
        mask, members=members, declared_sets=declared_sets, registry=registry
    )
    require_stamps(members, recorded_transform_ids=mask.member_transform_ids)
    require_partition_agreement(members)
    require_mask_member_alignment(mask, members)
    require_target_space(model)
    require_target_space(benchmark)
    if mask.partition_id == LOCKED_ID:
        if locked is None:
            raise IntegrityError(
                f"DEC estimand {getattr(model, 'model_id', '?')} vs "
                f"{getattr(benchmark, 'model_id', '?')}",
                "no LockedContext supplied for a DEC-partition mask; the locked path "
                "requires the hash receipt, the access record and the frozen-bundle "
                "manifest (R-109) and refuses fail-closed without them",
            )
        require_locked_receipt(
            mask=mask,
            prediction_path=locked.prediction_path,
            receipt_path=locked.receipt_path,
            access_record=locked.access_record,
            mask_bundle_manifest=locked.mask_bundle_manifest,
            month_start=locked.month_start,
            month_end=locked.month_end,
            embargo_hours=locked.embargo_hours,
        )

    model_id = str(getattr(model, "model_id"))
    benchmark_id = str(getattr(benchmark, "model_id"))
    series = paired_difference_series(model_id, benchmark_id, mask)  # step 1, one copy
    scalar, per_station = equal_station_mean(  # steps 2-3, one copy
        {station: [diff for _, diff in rows] for station, rows in series.items()}
    )

    result = EstimandResult(
        scalar=scalar,
        per_station=per_station,
        orientation=ORIENTATION,
        weighting=WEIGHTING,
        sign_convention_sentence=SIGN_CONVENTION_SENTENCE,
        mask_id=mask.mask_id,
        set_id=mask.set_id,
        model_id=model_id,
        benchmark_id=benchmark_id,
        phase_id=mask.phase_id,
        source_id=mask.source_id,
        target_definition_id=mask.target_definition_id,
        partition_id=mask.partition_id,
    )
    _stamps_match_mask(result, mask)
    return result


# =======================================================================================
# W-6: the MetricsArtifact — complete by construction, disclosing by construction
# =======================================================================================


def _audit_content_hash(overlap_audit: Mapping[str, Any]) -> str:
    canonical = json.dumps(dict(overlap_audit), sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _gim_disclosure_block(
    *,
    overlap_audit: Mapping[str, Any] | None,
    comparator_provenance: Mapping[str, Any] | None,
    set_id: str,
) -> dict[str, Any]:
    """SD-C-04's fail-closed, clock-free GIM overlap disclosure.

    Fail-closed (control 26): a GIM comparison with NO registered overlap-audit result
    refuses — the disclosure cannot be silently skipped, and its trigger is the COMPARISON
    EXISTING, not the audit having run (Recommendation 41; FR-P1-04-9's "overlap audit all
    exist" criterion). Ordering by CONTAINMENT (control 32): the comparator artifact records
    the audit result's ID and content hash found at its generation; a comparator without
    that containment evidence, or whose recorded hash does not match the registered audit,
    fails rather than being accepted retrospectively — the same idiom as SD-C-02, no clock
    compared. The rendered block itself comes from `src/external/gim.py`'s
    `render_comparison_report` — the R-60 disclosure chokepoint, imported HERE, at
    evaluation time only (R-112), so its emission logic has one copy project-wide.
    """
    if overlap_audit is None or "gim_network_overlap_flag" not in overlap_audit:
        raise FairnessError(
            f"GIM comparison in set {set_id}",
            "no registered overlap-audit result with its gim_network_overlap_flag value "
            "exists; emitting or reporting ANY GIM comparison without it FAILS — the "
            "trigger is the comparison's existence, disclosure is mandatory, and no "
            "independence claim precedes the audit (R-110 limb 3, re-keyed per "
            "Recommendation 41; TE §5.2; Vision §6.10)",
        )
    if comparator_provenance is None:
        raise FairnessError(
            f"GIM comparison in set {set_id}",
            "the C-01 comparator carries no generation provenance; ordering is proven by "
            "containment — the comparator records the audit result's ID and content hash "
            "found at generation — and a comparator without that evidence cannot prove the "
            "audit preceded it (SD-C-04; control 32)",
        )
    recorded_id = comparator_provenance.get("overlap_audit_id")
    recorded_hash = comparator_provenance.get("overlap_audit_sha256")
    if not recorded_id or not recorded_hash:
        raise FairnessError(
            f"GIM comparison in set {set_id}",
            "the C-01 comparator's provenance records no overlap_audit_id / "
            "overlap_audit_sha256; the audit's precedence over comparator generation is "
            "proven by containment, not clocks, and absent evidence fails rather than "
            "being accepted retrospectively (SD-C-04; control 32)",
        )
    actual_id = str(overlap_audit.get("audit_id", ""))
    actual_hash = _audit_content_hash(overlap_audit)
    if str(recorded_id) != actual_id or str(recorded_hash) != actual_hash:
        raise FairnessError(
            f"GIM comparison in set {set_id}",
            f"the comparator's recorded audit containment ({recorded_id!r}, "
            f"{str(recorded_hash)[:12]}…) does not match the registered overlap-audit "
            f"result ({actual_id!r}, {actual_hash[:12]}…); an audit registered AFTER "
            f"comparator generation cannot appear in the comparator's provenance, so a "
            f"mismatch fails (SD-C-04's containment ordering; control 32)",
        )
    # Evaluation-time-only import (R-112): reached only on the GIM path, after the
    # registered-mask precondition upstream; ONE copy of the rendering (R-60's chokepoint).
    from src.external import gim

    rendered = gim.render_comparison_report(
        comparison={"set_id": set_id, "comparator": _GIM_COMPARATOR_ID},
        overlap_audit=overlap_audit,
    )
    rendered["overlap_audit_id"] = actual_id
    rendered["overlap_audit_sha256"] = actual_hash
    return rendered


def build_metrics_artifact(
    *,
    set_id: str,
    declared_sets: Mapping[str, Mapping[str, Any]],
    mask: ComparisonMask,
    registry: Any,
    estimands: Sequence[EstimandResult],
    gim_overlap_audit: Mapping[str, Any] | None = None,
    gim_comparator_provenance: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """W-6: the results artifact `07` emits — refused unless complete and disclosing.

    Limb 1 — completeness per declared set (control 24): one estimand per declared
    (model, benchmark) pair over the set's ONE frozen mask; emission with any benchmark's
    estimand missing, or any estimand from another set/mask, is REFUSED upstream of any
    table. Limb 2 — `beats_model` per benchmark (control 27): under benchmark-minus-model
    orientation a NEGATIVE differential means the benchmark beat the model; the flag is
    derived from the sign and decides nothing scientific. Limb 3 — the disclosures
    (controls 25, 26, 32): the TEC-06 sentence on every IRI/GIM comparison row, the
    fail-closed GIM overlap disclosure, the Phase-2 statement as a field.

    Raises
    ------
    FairnessError
        incomplete emission; a foreign or unregistered mask; a GIM comparison without its
        registered audit result or containment evidence.
    """
    declared = declared_sets.get(set_id)
    if not isinstance(declared, Mapping):
        raise FairnessError(
            f"metrics artifact for set {set_id}",
            f"comparison set {set_id!r} is not declared in configs/experiment.yaml (R-106)",
        )
    require_registered_mask(mask, members=(), declared_sets=declared_sets, registry=registry)
    if str(mask.set_id) != str(set_id):
        raise FairnessError(
            f"metrics artifact for set {set_id}",
            f"mask {mask.mask_id} belongs to set {mask.set_id!r}; each set's artifact is "
            f"computed over that set's ONE frozen mask (R-110 limb 1)",
        )

    model_id = str(declared["model_id"])
    benchmark_ids = tuple(str(b) for b in declared["benchmark_ids"])
    by_benchmark: dict[str, EstimandResult] = {}
    for result in estimands:
        if result.set_id != set_id or result.mask_id != mask.mask_id:
            raise FairnessError(
                f"estimand {result.model_id} vs {result.benchmark_id}",
                f"belongs to set {result.set_id!r} / mask {result.mask_id!r}, not "
                f"{set_id!r} / {mask.mask_id!r}; estimands from another set or mask cannot "
                f"enter this artifact (R-110 limb 1)",
            )
        if result.model_id != model_id:
            raise FairnessError(
                f"estimand {result.model_id} vs {result.benchmark_id}",
                f"model {result.model_id!r} is not the declared model {model_id!r} "
                f"(R-106's declaration)",
            )
        _stamps_match_mask(result, mask)
        by_benchmark[result.benchmark_id] = result

    missing = [b for b in benchmark_ids if b not in by_benchmark]
    if missing:
        raise FairnessError(
            f"metrics artifact for set {set_id}",
            f"estimand(s) missing for declared benchmark(s) {missing}; the artifact is "
            f"refused rather than emitted incomplete — a table missing a member becomes "
            f"impossible UPSTREAM of the table (R-110 limb 1; W-6; control 24)",
        )

    comparisons: list[dict[str, Any]] = []
    for benchmark_id in benchmark_ids:
        result = by_benchmark[benchmark_id]
        row: dict[str, Any] = {
            "model_id": result.model_id,
            "benchmark_id": benchmark_id,
            "scalar": result.scalar,
            "per_station": dict(result.per_station),
            "orientation": result.orientation,
            "weighting": result.weighting,
            "sign_convention_sentence": result.sign_convention_sentence,
            # beats_model: benchmark minus model NEGATIVE ⇒ the benchmark's squared error
            # is smaller ⇒ the benchmark beat the model. Derived, never decided (R-110).
            "beats_model": result.scalar < 0.0,
            "mask_id": result.mask_id,
            "set_id": result.set_id,
            "phase_id": result.phase_id,
            "source_id": result.source_id,
            "target_definition_id": result.target_definition_id,
            "partition_id": result.partition_id,
        }
        if benchmark_id in EXTERNAL_COMPARATOR_IDS:
            row["spatial_representativeness_sentence"] = SPATIAL_REPRESENTATIVENESS_SENTENCE
        if benchmark_id == _GIM_COMPARATOR_ID:
            row["gim_overlap_disclosure"] = _gim_disclosure_block(
                overlap_audit=gim_overlap_audit,
                comparator_provenance=gim_comparator_provenance,
                set_id=set_id,
            )
        comparisons.append(row)

    return {
        "artifact_class": "metrics_artifact",
        "set_id": set_id,
        "model_id": model_id,
        "mask_id": mask.mask_id,
        # The five exposed reporting values, supplied for the reporting unit to PRINT and
        # never restate (R-107 limb 6).
        "feature_set_id": mask.feature_set_id,
        "row_counts": dict(mask.row_counts),
        "exclusion_counts": dict(mask.exclusion_counts),
        "scored_window_statement": mask.scored_window_statement,
        "comparisons": comparisons,
        "phase2_not_independent_statement": PHASE2_NOT_INDEPENDENT_STATEMENT,
        "emitted_at_utc": dt.datetime.now(dt.UTC).isoformat(),
    }


def assert_metrics_artifact(
    artifact: Mapping[str, Any], *, declared_sets: Mapping[str, Mapping[str, Any]]
) -> None:
    """The presence tests of R-110, runnable against a SERIALIZED artifact.

    Proves tampering or hand-assembly is caught: every declared benchmark present (24);
    every row carrying `beats_model` (27), the sign-convention sentence and the four stamps
    (30's presence half); the TEC-06 sentence on every IRI/GIM row (25); the GIM overlap
    disclosure with its flag value and containment fields on every C-01 row (26/32's
    presence half); the Phase-2 statement field.

    Raises
    ------
    FairnessError
        naming the first absent obligation.
    """
    set_id = str(artifact.get("set_id", ""))
    declared = declared_sets.get(set_id)
    if not isinstance(declared, Mapping):
        raise FairnessError(f"metrics artifact {set_id!r}", "names no declared set (R-106)")
    rows = {str(r.get("benchmark_id")): r for r in artifact.get("comparisons", ())}
    missing = [b for b in declared["benchmark_ids"] if str(b) not in rows]
    if missing:
        raise FairnessError(
            f"metrics artifact {set_id}",
            f"benchmark row(s) {missing} absent; completeness is per declared set (R-110)",
        )
    if artifact.get("phase2_not_independent_statement") != PHASE2_NOT_INDEPENDENT_STATEMENT:
        raise FairnessError(
            f"metrics artifact {set_id}",
            "the Phase-2 not-independent-blind-test statement is absent or altered; the "
            "disclosure is an artifact field, mandated verbatim (VAL-05; project.md)",
        )
    for key in ("mask_id", "feature_set_id", "row_counts", "exclusion_counts",
                "scored_window_statement"):
        if not artifact.get(key):
            raise FairnessError(
                f"metrics artifact {set_id}",
                f"reporting value {key!r} absent; the five exposed values travel on the "
                f"artifact (R-107 limb 6)",
            )
    for benchmark_id, row in rows.items():
        if "beats_model" not in row:
            raise FairnessError(
                f"metrics artifact {set_id} row {benchmark_id}",
                "carries no beats_model field; FR-P1-05-20's disclosure check downstream "
                "is a field comparison and the field must exist to compare (control 27)",
            )
        if row.get("sign_convention_sentence") != SIGN_CONVENTION_SENTENCE:
            raise FairnessError(
                f"metrics artifact {set_id} row {benchmark_id}",
                "sign-convention sentence absent or altered (R-108; FR-P1-05-7's "
                "every-table obligation, made checkable)",
            )
        for stamp in ("phase_id", "source_id", "target_definition_id", "partition_id"):
            if not row.get(stamp):
                raise FairnessError(
                    f"metrics artifact {set_id} row {benchmark_id}",
                    f"mandated stamp {stamp!r} absent (TE §13; control 30)",
                )
        if benchmark_id in EXTERNAL_COMPARATOR_IDS and (
            row.get("spatial_representativeness_sentence")
            != SPATIAL_REPRESENTATIVENESS_SENTENCE
        ):
            raise FairnessError(
                f"metrics artifact {set_id} row {benchmark_id}",
                "the TEC-06 spatial-representativeness sentence is absent or altered on an "
                "IRI/GIM comparison; the caveat travels with the comparison, emitted by "
                "the producing path (R-110 limb 3; control 25)",
            )
        if benchmark_id == _GIM_COMPARATOR_ID:
            block = row.get("gim_overlap_disclosure")
            if not isinstance(block, Mapping) or "gim_network_overlap_flag" not in block:
                raise FairnessError(
                    f"metrics artifact {set_id} row {benchmark_id}",
                    "GIM comparison without its overlap disclosure and flag value; "
                    "disclosure is mandatory and fail-closed (control 26)",
                )
            if not block.get("overlap_audit_id") or not block.get("overlap_audit_sha256"):
                raise FairnessError(
                    f"metrics artifact {set_id} row {benchmark_id}",
                    "GIM disclosure without the audit's ID/content-hash containment "
                    "evidence; ordering is proven by containment (control 32)",
                )


def write_metrics_artifact(artifact: Mapping[str, Any], path: Path) -> Path:
    """Durable, refuse-to-overwrite serialization of the metrics artifact.

    `.tmp` → flush+fsync → atomic rename, mirroring the project idiom; an existing artifact
    is never silently replaced (NFR-AUD-01) — a re-run writes under a new run directory.

    Raises
    ------
    FairnessError
        the target already exists.
    IntegrityError
        the durable write fails; nothing is recorded.
    """
    path = Path(path)
    if path.exists():
        raise FairnessError(
            path,
            "metrics artifact already exists; results are never silently overwritten "
            "(NFR-AUD-01) — a re-run emits under its own run directory",
        )
    payload = (json.dumps(dict(artifact), sort_keys=True, indent=2, default=str) + "\n").encode(
        "utf-8"
    )
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
        try:
            written = os.write(fd, payload)
            if written != len(payload):
                raise IntegrityError(tmp, f"wrote {written} of {len(payload)} bytes")
            os.fsync(fd)
        finally:
            os.close(fd)
        os.replace(tmp, path)
    except OSError as exc:
        raise IntegrityError(
            path, f"durable metrics-artifact write failed ({exc}); nothing is recorded"
        ) from exc
    return path
