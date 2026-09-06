"""C1 guards: the six refusals of SD-C-01 — one failure domain for every metric boundary.

Purpose
-------
`evaluation-and-comparison` SD-C-01 (Q3 = A) fixes ONE guard module owning every refusal
check, so drift between two copies of one rule — the R-105-vs-R-92 defect class the
2026-08-28 governance board caught — has no second copy to drift. The six guards:

* ``require_stamps`` — `LeakageError` on a `None` `partition_id`/`transform_id` stamp, and on
  a `transform_id` outside the mask's recorded member set (the information-flow limbs;
  R-105 limb 1, W-1 step 1, matching `models-and-baselines` R-92).
* ``require_partition_agreement`` — `PartitionError` when members of one comparison disagree
  on `partition_id` (a declared-identity disagreement; R-105 limb 2, W-4, R-92-matched).
* ``require_registered_mask`` — `FairnessError` unless the mask is registered, frozen, and
  the passed members match the declared `experiment.yaml` set EXACTLY: missing, extra,
  duplicate, any two sets merged, and every pairwise/ad-hoc subset all refuse
  (R-106, R-107, W-1; NFR-FAIR-01).
* ``require_target_space`` — `InverseTransformError` on transformed-space input at any metric
  entry point; the reserved literal ``untransformed`` (B-01/C-01) reads native; `ABL-DIFF`
  refuses naming D-27 while no inverse exists (R-103/R-104, W-3).
* ``require_locked_receipt`` — `LockedTestError` on `DEC` only, three ordered limbs:
  (1) the prediction-hash receipt verifies (write-once detection, FR-P1-05-12);
  (2) SD-C-02 containment — the access record carries `mask_bundle_ids` and
  `mask_registry_hash`, the frozen bundle's manifest re-hashes to the recorded hash, and the
  scored mask's `mask_id` is in `mask_bundle_ids`;
  (3) the D-28 scored window — "2–31 December 2022, 30 days, first 24 h excluded and
  counted": a row inside the excluded first 24 h raises (R-109, W-5).
* ``require_mask_member_alignment`` — `FairnessError` when the mask's RECORDED `partition_id`
  disagrees with any member's: a self-consistent member set scored against a mask built for a
  different partition refuses (W-4's third failure, W-2 step 1; the sixth guard added at the
  2026-09-05 gate on governance Recommendation 1).

The discriminating rule, ONE copy, project-wide (GOV-2026-08-28-FD-01 Recommendation 8):
**`PartitionError`** for a declared-identity disagreement (a `partition_id` mismatch between
members); **`LeakageError`** where the disagreement implies information flow (`transform_id`
disagreement, or a `None` stamp); **`FairnessError`** for a member-versus-MASK partition
disagreement, membership violations, and once-only violations — scoring against the wrong
exam rather than a provenance disagreement among members.

Exception declaration note (deviation from `domain-entities.md` § 8, recorded not hidden):
that table places `FairnessError`'s and `InverseTransformError`'s declaration "here
(`src/evaluation`)". It was written before `foundation`'s R-01 amendment ruled
`src/data/config.py` the ONE declaration site (see that module's docstring: `PartitionError`'s
site "was ruled to be this module by the project decision owner on 2026-08-28";
`StandardizationError`, `InventoryError` and four `external-products` exceptions followed the
same receipted pattern). Both classes ALREADY EXIST there; a second class object with the
same name would break catchability — a caller catching one would not catch the other, the
exact cross-unit-drift failure R-01 exists to prevent. This module therefore IMPORTS and
RE-EXPORTS them from the R-01 declaration site rather than redeclaring them; this unit
remains their raise site. `PartitionError`/`LeakageError`/`LockedTestError` are imported
exactly as the design states.

Inputs
------
In-memory prediction-like objects (structurally typed on the approved eight `Prediction`
fields: `model_id`, `seed`, `frame`, `target_definition_id`, `phase_id`, `source_id`,
`partition_id`, `transform_id`), mask objects (`src/evaluation/masks.py`), the declared
comparison sets read from `configs/experiment.yaml` through `ConfigSnapshot` (by the caller),
receipt/manifest files on disk, and `governance-guards`' `AccessRecord`. This module imports
ONLY `src/data` and the standard library: **no `src/features`, no `src/models`, no
`src/external` — directly or transitively** (D-27: the R-103 edge is unauthorised; TE §12).

Re-run behaviour
----------------
Pure checks; nothing is persisted; every failure is an `IntegrityError` subclass naming the
file or resource and the violated expectation (R-01's constructor contract). Deterministic
given the same inputs and on-disk artifacts.

Governance
----------
R-103…R-112; SD-C-01…SD-C-03; D-27 (inverse withheld — `resolve_inverse` refuses);
D-28 (the scored window); Q2 = B (`AccessRecord` containment fields, populated by
`open_restricted`, refused on `None` here — the fail-closed half); Q4 = A (write-once
manifest; a mid-registration read sees only complete manifests).
"""

from __future__ import annotations

import datetime as dt
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from src.data.config import (
    FairnessError,
    IntegrityError,
    InverseTransformError,
    LeakageError,
    LockedTestError,
    PartitionError,
)
from src.data.release import sha256_of_file

__all__ = [
    "UNTRANSFORMED",
    "STAMP_FIELDS",
    "FairnessError",
    "InverseTransformError",
    "LeakageError",
    "LockedTestError",
    "PartitionError",
    "require_stamps",
    "require_partition_agreement",
    "require_declared_membership",
    "require_registered_mask",
    "require_target_space",
    "require_locked_receipt",
    "require_mask_member_alignment",
    "resolve_inverse",
    "scored_window_statement",
]

#: The reserved transform literal for generated (never trained) products — B-01 and C-01
#: are stamped with it at generation and read machine-readably as native target-space
#: (R-104, R-105). An identity token, not a scientific constant.
UNTRANSFORMED: str = "untransformed"

#: The four mandated identity stamps plus the two provenance stamps every prediction-like
#: object carries (approved eight-field `Prediction`, `component-methods.md`; TE §13).
STAMP_FIELDS: tuple[str, ...] = ("partition_id", "transform_id")


def _label(prediction: Any) -> str:
    model = getattr(prediction, "model_id", "<no model_id>")
    seed = getattr(prediction, "seed", None)
    return f"prediction {model}" + (f"/seed{seed}" if seed is not None else "")


def _frame_attrs(prediction: Any) -> Mapping[str, Any]:
    attrs = getattr(getattr(prediction, "frame", None), "attrs", None)
    return attrs if isinstance(attrs, Mapping) else {}


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
            raise IntegrityError(resource, f"timestamp {value!r} is not ISO-8601") from exc
    if stamp.tzinfo is None:
        return stamp.replace(tzinfo=dt.UTC)
    return stamp.astimezone(dt.UTC)


# --- guard 1: require_stamps (LeakageError — the information-flow limbs) -------------------


def require_stamps(
    predictions: Sequence[Any], *, recorded_transform_ids: Sequence[str] | None = None
) -> None:
    """R-105 limb 1 / W-1 step 1: non-`None` stamps, before any row is touched.

    Runs BEFORE ``require_partition_agreement`` (limb order is load-bearing: a `None`
    `partition_id` is caught here and never reaches the mismatch test). When
    ``recorded_transform_ids`` — the mask's recorded member-`transform_id` set — is given
    (W-2 step 1: "against the mask's recorded stamps"), a member whose `transform_id` is not
    in the recorded set raises: a fit from one partition reaching another partition's rows is
    the leak itself. Members of one comparison legitimately DIFFER on `transform_id`
    (B-01/C-01 carry ``untransformed``); the mask records the SET.

    Raises
    ------
    LeakageError
        an absent (`None`) `partition_id` or `transform_id` — the hand-assembled prediction,
        the exact residual R-74 names; or a `transform_id` outside the mask's recorded set.
    """
    for prediction in predictions:
        for field in STAMP_FIELDS:
            if getattr(prediction, field, None) is None:
                raise LeakageError(
                    _label(prediction),
                    f"{field} is None; an absent stamp is the information-flow case — a "
                    f"hand-assembled prediction entering a comparison (R-105 limb 1, "
                    f"matching R-92's None limb)",
                )
        if recorded_transform_ids is not None:
            tid = getattr(prediction, "transform_id")
            if tid not in tuple(recorded_transform_ids):
                raise LeakageError(
                    _label(prediction),
                    f"transform_id {tid!r} is not in the mask's recorded member set "
                    f"{sorted(map(str, recorded_transform_ids))}; a transform_id "
                    f"disagreement implies information flow (R-105 limb 1; W-2 step 1)",
                )


# --- guard 2: require_partition_agreement (PartitionError — declared identity) -------------


def require_partition_agreement(predictions: Sequence[Any]) -> None:
    """R-105 limb 2 / W-4: all members of one comparison agree on `partition_id`.

    Raises
    ------
    PartitionError
        a `partition_id` mismatch between members — a declared-identity disagreement;
        nothing has yet flowed. The SAME exception R-92 raises for the same condition
        (GOV-2026-08-28-FD-01 Recommendation 8), so a test asserting
        ``pytest.raises(PartitionError)`` passes at `06` and at `07` alike.
    """
    seen = {str(getattr(p, "partition_id")) for p in predictions}
    if len(seen) > 1:
        raise PartitionError(
            "comparison members",
            f"disagree on partition_id {sorted(seen)}; a declared-identity disagreement "
            f"raises PartitionError (R-105 limb 2, matching R-92) — members of one "
            f"comparison must all declare the same partition",
        )


# --- guard 3: require_registered_mask (FairnessError — membership + registration) ----------


def _declared_membership(
    declared_sets: Mapping[str, Mapping[str, Any]], set_id: str, resource: str
) -> tuple[str, ...]:
    node = declared_sets.get(set_id)
    if not isinstance(node, Mapping) or not node.get("member_ids"):
        raise FairnessError(
            resource,
            f"comparison set {set_id!r} is not declared in configs/experiment.yaml "
            f"comparison_sets; membership is a frozen scientific choice living in "
            f"configuration (R-106, TC-03e) and an undeclared set can never build a mask",
        )
    return tuple(str(m) for m in node["member_ids"])


def require_declared_membership(
    member_ids: Sequence[str],
    *,
    set_id: str,
    declared_sets: Mapping[str, Mapping[str, Any]],
) -> tuple[str, ...]:
    """R-106: the passed member IDs match the declared `experiment.yaml` set EXACTLY.

    One copy of the membership-exact check (SD-C-01's one-failure-domain rule), invoked at
    mask construction (W-1 step 2), inside ``require_registered_mask``, and at the
    metrics-artifact completeness refusal (W-6 limb 1). Returns the declared membership.

    Raises
    ------
    FairnessError
        missing member, extra member, duplicate member, or any two declared sets merged into
        one call (the merge is named when the extras overlap another declared set); an
        undeclared `set_id`; every pairwise/ad-hoc subset refuses the same way
        (FR-P1-04-7's own criterion; NFR-FAIR-01).
    """
    declared = _declared_membership(declared_sets, set_id, f"comparison set {set_id}")
    passed = [str(m) for m in member_ids]

    duplicates = sorted({m for m in passed if passed.count(m) > 1})
    if duplicates:
        raise FairnessError(
            f"comparison set {set_id}",
            f"duplicate member(s) {duplicates} passed; the declared set enumerates each "
            f"member once (R-106)",
        )
    missing = sorted(set(declared) - set(passed))
    extra = sorted(set(passed) - set(declared))
    if missing or extra:
        merged_hint = ""
        if extra:
            for other_id, node in declared_sets.items():
                if other_id == set_id or not isinstance(node, Mapping):
                    continue
                others = {str(m) for m in node.get("member_ids", ())}
                if set(extra) & others:
                    merged_hint = (
                        f"; the extra members overlap declared set {other_id!r} — two "
                        f"declared sets merged into one call match NO declared set and a "
                        f"silent merge would shrink the primary scored set (R-106)"
                    )
                    break
        raise FairnessError(
            f"comparison set {set_id}",
            f"passed members {sorted(passed)} do not match the declared set "
            f"{sorted(declared)} exactly (missing {missing or 'none'}, extra "
            f"{extra or 'none'}); a pairwise or model-specific mask is never permitted "
            f"(FR-P1-04-7; NFR-FAIR-01){merged_hint}",
        )
    return declared


def require_registered_mask(
    mask: Any,
    *,
    members: Sequence[Any],
    declared_sets: Mapping[str, Mapping[str, Any]],
    registry: Any,
) -> None:
    """R-106/R-107/R-108: the mask is registered, frozen, and IS the declared set's.

    ``registry`` is duck-typed (``lookup(set_id) -> Mapping | None``) so the read path stays
    in `masks.py` while the refusal logic has one home here (SD-C-01). ``members`` are the
    predictions entering THIS metric call — a (model, benchmark) pair at the estimand, the
    full set at emission — each of which must be a declared member; the membership-EXACT
    check (R-106) is ``require_declared_membership``'s, fired where the full set is passed.

    Raises
    ------
    FairnessError
        the mask's `set_id` is not a declared set; a passed member is not in the declared
        membership; the mask's own recorded membership differs from the declaration; the
        mask is not registered for its set; or the registered entry's `mask_id` differs from
        the mask's — a metric computed off-mask or on an ad-hoc mask is an error, not a
        wrong number (R-108).
    """
    set_id = str(getattr(mask, "set_id", ""))
    declared = _declared_membership(declared_sets, set_id, f"mask {getattr(mask, 'mask_id', '?')}")

    for member in members:
        model_id = str(getattr(member, "model_id"))
        if model_id not in declared:
            raise FairnessError(
                _label(member),
                f"is not a member of declared comparison set {set_id!r} "
                f"({sorted(declared)}); a prediction outside the declared set cannot be "
                f"scored on its mask (R-106, R-108)",
            )

    mask_members = tuple(str(m) for m in getattr(mask, "member_ids", ()))
    if sorted(mask_members) != sorted(declared):
        raise FairnessError(
            f"mask {getattr(mask, 'mask_id', '?')}",
            f"records members {sorted(mask_members)}, not the declared set "
            f"{sorted(declared)}; a mask built off-declaration cannot produce a number "
            f"(R-106, R-108)",
        )

    entry = registry.lookup(set_id) if registry is not None else None
    if not isinstance(entry, Mapping):
        raise FairnessError(
            f"mask {getattr(mask, 'mask_id', '?')}",
            f"is not registered for comparison set {set_id!r}; a metric computed off-mask "
            f"or on an ad-hoc mask is an error, not a wrong number (R-108; R-107's registry "
            f"supplies the check)",
        )
    if str(entry.get("mask_id")) != str(getattr(mask, "mask_id", "")):
        raise FairnessError(
            f"mask {getattr(mask, 'mask_id', '?')}",
            f"differs from the registered mask {entry.get('mask_id')!r} for set {set_id!r}; "
            f"the registered frozen mask is the precondition of every metric (R-107, R-108)",
        )


# --- guard 4: require_target_space (InverseTransformError — R-104's boundary) --------------


def resolve_inverse(transform_id: str) -> Any:
    """R-103's `ABL-DIFF`-only resolver slot — REFUSES today, always, naming D-27.

    D-27 withheld the inverse mechanism (*"no import-boundary change is authorised by this
    decision"*), `evidence/DECISIONS.md` ends at D-32 with D-27 unreopened (verified
    2026-09-06), and the `src/evaluation` → `src/features` edge is unauthorised — so there is
    NO registry to search and no persisted inverse to resolve. This function exists so the
    refusal has one home and control (1) has a named surface; it never returns.

    Raises
    ------
    InverseTransformError
        always, naming the identifier and the (absent) registry searched.
    """
    raise InverseTransformError(
        f"transform {transform_id!r}",
        "resolves to no persisted inverse: no inverse registry exists in src/evaluation and "
        "the src/evaluation -> src/features edge is unauthorised (D-27: 'no import-boundary "
        "change is authorised by this decision'; R-103) — ABL-DIFF has no executable inverse "
        "path and refuses rather than defaulting (TE 18.3)",
    )


def require_target_space(prediction: Any) -> None:
    """R-104: every metric entry point refuses transformed-space input.

    The decision ladder, in order:

    1. `transform_id == "untransformed"` — B-01/C-01 and any generated product — passes
       natively (machine-readably target-space).
    2. A transform lineage recording an applied inversion (frame attrs
       ``inverse_applied == True`` naming this `transform_id`) passes — the inversion is a
       stamp on the artifact, not a remembered call (ADR-11's stamp-not-memory principle).
    3. A prediction DECLARED target-touching — frame attrs ``touches_target`` truthy, or
       ``ablation_id == "ABL-DIFF"`` (TE §7.2's sole target-transforming configuration,
       frozen by D-27) — refuses: no inverse exists while D-27 stands.
    4. Anything else passes as non-target-touching: D-27 froze that the primary
       configuration's train-only transform acts on target-derived INPUT features and the
       target stays raw TECU. The machine-readable ``touches_target`` declaration is half B's
       (`features-and-splits` R-84, pending adoption); when it travels on a prediction it is
       checked here, not trusted — a primary transform declaring itself target-touching is
       refused, which is what makes a D-27 contradiction catchable (R-103's limitation,
       carried not softened).

    Raises
    ------
    InverseTransformError
        a target-touching prediction whose lineage records no inversion — the un-inverted
        `ABL-DIFF` case, controls (3) and (4).
    """
    tid = getattr(prediction, "transform_id", None)
    if tid == UNTRANSFORMED:
        return
    attrs = _frame_attrs(prediction)
    if attrs.get("inverse_applied") is True:
        return
    touches = bool(attrs.get("touches_target")) or attrs.get("ablation_id") == "ABL-DIFF"
    if touches:
        raise InverseTransformError(
            _label(prediction),
            f"is target-touching (transform {tid!r}) and its lineage records no applied "
            f"inverse; ABL-DIFF inverse-transforms to absolute TECU before ANY metric "
            f"(project.md Mandated; TE 7.2; R-104) — and no inverse exists while D-27 "
            f"stands unreopened, so this refuses rather than defaulting",
        )


# --- guard 5: require_locked_receipt (LockedTestError — DEC only, three ordered limbs) -----


def scored_window_statement(
    month_start: dt.datetime, month_end: dt.datetime, *, embargo_hours: int
) -> str:
    """The mask's scored-window statement, DERIVED from the partition, never invented.

    Pure string arithmetic over the locked month's bounds and its embargo: for the real
    locked partition (December 2022, 24 h embargo) this yields EXACTLY D-28's mandated
    disclosure — ``"2–31 December 2022, 30 days, first 24 h excluded and counted"`` — with
    no December read and no scientific constant in source: the month and embargo reach this
    function from configuration through the partition machinery (R-107 limb 6; D-28's own
    consequence that the scored set "must be disclosed as 30 days").
    """
    scored_start = month_start + dt.timedelta(hours=embargo_hours)
    last_day = (month_end - dt.timedelta(hours=1)).day
    days = (month_end - scored_start) // dt.timedelta(days=1)
    return (
        f"{scored_start.day}–{last_day} {month_start.strftime('%B %Y')}, {days} days, "
        f"first {embargo_hours} h excluded and counted"
    )


def _load_receipt(receipt_path: Path) -> Mapping[str, Any]:
    """`06`'s five-field prediction-hash receipt, consumed as a FILE contract.

    The receipt is produced by `models-and-baselines`' `write_prediction_hash_receipt`
    (`domain-entities.md` § 5: `prediction_path`, `sha256`, `recorded_at_utc`, `run_id`,
    `partition_id`). It is read here from its serialized form rather than by importing
    `src/models/train.py`, because that module imports `src/features` at module scope and
    this package may not reach `src/features` even transitively while D-27 stands.
    """
    path = Path(receipt_path)
    if not path.is_file():
        raise LockedTestError(
            path,
            "no prediction-hash receipt exists; every metric entry point on DEC requires the "
            "recorded receipt BEFORE computing (R-109 limb 1; FR-P1-05-12; hash-before-"
            "metrics, project.md Mandated) — recording it is 06's act, refusing without it "
            "is this unit's (TA-18's supporting-role split)",
        )
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        for field in ("prediction_path", "sha256", "recorded_at_utc", "run_id", "partition_id"):
            if not payload.get(field):
                raise KeyError(field)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise LockedTestError(path, f"receipt is malformed ({exc})") from exc
    return payload


def require_locked_receipt(
    *,
    mask: Any,
    prediction_path: Path,
    receipt_path: Path,
    access_record: Any,
    mask_bundle_manifest: Path | None,
    month_start: dt.datetime,
    month_end: dt.datetime,
    embargo_hours: int,
    now: dt.datetime | None = None,
) -> None:
    """R-109 / SD-C-03: the three ordered limbs guarding every `DEC` metric entry point.

    Limb 1 — the prediction-hash receipt is re-verified: present, the prediction file
    re-hashes to it (write-once DETECTION — a second write of the file is caught here, never
    assumed absent), and its timestamp precedes the metric call.

    Limb 2 — SD-C-02 containment, not clocks: the access record (written by
    `governance-guards`' `open_restricted`, log-then-read) carries `mask_bundle_ids` and
    `mask_registry_hash`; the frozen bundle's write-once manifest re-hashes to the recorded
    hash; and the scored mask's `mask_id` is contained in `mask_bundle_ids`. A record
    without the two fields refuses — the fail-closed half of the Q2 = B half-contract. An
    absent access record refuses too: a December read not routed through `open_restricted`
    never produces one (control 23; R-28's one door).

    Limb 3 — the D-28 window: the mask's scored-window statement equals the one DERIVED from
    the locked partition's month and embargo, and no masked row lies inside the excluded
    first `embargo_hours` — a 1 December row raises, so the 30-day ruling cannot be silently
    widened back to 31 at implementation.

    Raises
    ------
    LockedTestError
        on any limb, naming the limb, the file or resource, and the violated expectation.
    """
    # --- limb 1: hash receipt ---------------------------------------------------------
    receipt = _load_receipt(Path(receipt_path))
    actual = sha256_of_file(Path(prediction_path))
    if actual != str(receipt["sha256"]):
        raise LockedTestError(
            prediction_path,
            f"limb 1: sha256 {actual[:12]}… does not match the receipt's "
            f"{str(receipt['sha256'])[:12]}…; the prediction file is not the one hashed as "
            f"written — a detected second write (FR-P1-05-12's write-once criterion; a "
            f"Validation-Auditor veto condition)",
        )
    call_time = now if now is not None else dt.datetime.now(dt.UTC)
    recorded_at = _as_utc(receipt["recorded_at_utc"], resource=str(receipt_path))
    if not recorded_at < call_time:
        raise LockedTestError(
            receipt_path,
            f"limb 1: receipt timestamp {recorded_at.isoformat()} does not precede the "
            f"metric call at {call_time.isoformat()}; hash-before-metrics is an ordering, "
            f"not a co-occurrence (R-109 limb 1)",
        )

    # --- limb 2: SD-C-02 containment ---------------------------------------------------
    if access_record is None:
        raise LockedTestError(
            f"DEC metric for mask {getattr(mask, 'mask_id', '?')}",
            "limb 2: no access record — a December target read arrives ONLY through "
            "open_restricted with purpose 'locked_evaluation' (R-109 limb 2; R-25 "
            "log-then-read; R-28's one door), and a read that produced no record did not go "
            "through it",
        )
    bundle_ids = getattr(access_record, "mask_bundle_ids", None)
    registry_hash = getattr(access_record, "mask_registry_hash", None)
    if bundle_ids is None or registry_hash is None:
        raise LockedTestError(
            f"access record {getattr(access_record, 'run_id', '?')}",
            "limb 2: mask_bundle_ids/mask_registry_hash absent from the access record; "
            "SD-C-02 proves mask-freeze-before-access by CONTAINMENT and a record without "
            "the two fields refuses fail-closed (the populating half is governance-guards' "
            "open_restricted, per the Q2=B owner instruction; refusing on None is this "
            "unit's half)",
        )
    if mask_bundle_manifest is None or not Path(mask_bundle_manifest).is_file():
        raise LockedTestError(
            f"frozen-bundle manifest {mask_bundle_manifest}",
            "limb 2: the write-once frozen-bundle manifest is absent, so the recorded "
            "mask_registry_hash cannot be re-verified (SD-C-02: verification is possible "
            "post hoc from the two artifacts alone)",
        )
    manifest_hash = sha256_of_file(Path(mask_bundle_manifest))
    if manifest_hash != str(registry_hash):
        raise LockedTestError(
            Path(mask_bundle_manifest),
            f"limb 2: manifest re-hashes to {manifest_hash[:12]}…, not the access record's "
            f"{str(registry_hash)[:12]}…; the containment evidence does not verify, so "
            f"registration-before-access is not proven (SD-C-02)",
        )
    mask_id = str(getattr(mask, "mask_id", ""))
    if mask_id not in tuple(str(b) for b in bundle_ids):
        raise LockedTestError(
            f"mask {mask_id}",
            f"limb 2: not in the access record's mask_bundle_ids "
            f"{sorted(map(str, bundle_ids))}; a mask registered AFTER the access cannot "
            f"appear in a record written from an earlier registry read — containment is the "
            f"ordering proof, on any clocks (SD-C-02)",
        )

    # --- limb 3: the D-28 scored window -------------------------------------------------
    expected = scored_window_statement(month_start, month_end, embargo_hours=embargo_hours)
    stated = str(getattr(mask, "scored_window_statement", ""))
    if stated != expected:
        raise LockedTestError(
            f"mask {mask_id}",
            f"limb 3: scored-window statement {stated!r} is not the D-28-derived "
            f"{expected!r}; the scored set is disclosed as the month less its first "
            f"{embargo_hours} h, exactly (D-28; R-107 limb 6; R-109 limb 3)",
        )
    scored_start = month_start + dt.timedelta(hours=embargo_hours)
    for row in getattr(mask, "masked_rows", ()):
        stamp = _as_utc(
            row.get("interval_start_utc"), resource=f"mask {mask_id} row"
        )
        if not (scored_start <= stamp < month_end):
            raise LockedTestError(
                f"mask {mask_id} row {stamp.isoformat()}",
                f"limb 3: lies outside the D-28 scored window "
                f"[{scored_start.isoformat()}, {month_end.isoformat()}); a day-1 row in the "
                f"locked month's excluded first {embargo_hours} h raises — the 30-day "
                f"ruling cannot be silently widened back (D-28; R-109 limb 3)",
            )


# --- guard 6: require_mask_member_alignment (FairnessError — the wrong exam) ---------------


def require_mask_member_alignment(mask: Any, members: Sequence[Any]) -> None:
    """W-4's third failure / W-2 step 1: the mask's RECORDED `partition_id` matches every
    member's.

    A self-consistent member set sharing one (wrong) `partition_id` that disagrees with the
    mask's recorded `partition_id` passes ``require_partition_agreement`` (members agree with
    each other) and ``require_registered_mask`` (set membership exact) — this guard is what
    stops it reaching the metric (the sixth guard, added at the 2026-09-05 gate on
    governance Recommendation 1: the exact "compute the wrong comparison instead of
    nothing" failure this unit's design exists to close).

    Raises
    ------
    FairnessError
        a member whose `partition_id` differs from the mask's recorded one — scoring against
        the wrong exam, not a provenance disagreement among members (the discriminating
        rule's third row).
    """
    recorded = str(getattr(mask, "partition_id", ""))
    for member in members:
        own = str(getattr(member, "partition_id", ""))
        if own != recorded:
            raise FairnessError(
                _label(member),
                f"carries partition_id {own!r} but the mask "
                f"{getattr(mask, 'mask_id', '?')!r} records {recorded!r}; scoring against a "
                f"mask built for a different partition is the member-versus-mask "
                f"disagreement (W-4's third failure; R-105 limb 3; W-2 step 1)",
            )
