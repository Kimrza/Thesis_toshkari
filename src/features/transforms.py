"""F-4 Fitting identity: train-only transforms enforced by check, not by shape (W-3; R-74).

Purpose
-------
The BLK-04 cross-unit contract, approved 2026-09-05 (Q1 = A,
`governance/CHANGE_RECORD_2026-09-05_R74_R83_leakage_contracts.md`), in its ADR-11 form:

* `Transform` carries `transform_id` and `partition_id` — the identity every consumer
  compares — plus its fitted state (intra-package: the standardised columns, their means and
  scales, and the exact range fitted). It exposes NO apply surface: a function that applies a
  fitted transform to an arbitrary frame IS the hole ADR-11 removed, so application happens
  only inside `build_features`, through this module's `apply_fitted_transform`, which
  `build_features` alone calls.
* `fit_transforms(bundle, *, partition)` raises `PartitionError` on a declared-identity
  disagreement (`bundle.spec.partition_id != partition.partition_id`) and `LeakageError`
  when the role is not `train`, when the bundle is already transformed, or when the scored
  range is not EXACTLY `[partition.train_start, partition.train_end]` — both bounds read from
  the `Partition` (R-83), over-wide OR strict subset. The most natural `scikit-learn` idiom
  (fit once, transform everything) is the leak; nothing in a library's API distinguishes the
  fold-correct fit from the full-dataset one, so the control is a check that fails (TS-F-02).
* `assert_consumable(bundle)`: a bundle whose `transform_id is None` is the fitting input
  and is never consumable — `fit_predict`, `06` and `07` call this and raise.
* The R-77 carry-forward boundary: `carry_forward(series, *, field_class, bound_h)` REQUIRES
  the field class; only `FieldClass.driver` reaches `external-products`' bounded carry-
  forward, and `vtec_lag_*`/target-derived, station, time, support and diagnostic fields are
  refused at that boundary. `assert_field_classes_partition` proves every dictionary field
  belongs to exactly one class.

Nothing here decides a scientific value: which columns are standardised comes from the
dictionary's `normalization` declarations in `configs/features.yaml`; the carry-forward bound
comes from `configs/features.yaml` too. No inverse path is built (Q4 = A; D-27: `ABL-DIFF`'s
obligation stays open, narrowed, and no `src/evaluation` -> `src/features` edge exists).

Inputs
------
A `FeatureBundle` and its `Partition`; hourly driver series for the carry-forward boundary.
No file is read; no third-party package is imported at module scope.

Re-run behaviour
----------------
Pure functions; deterministic; nothing persisted. `fit_transforms` on the same bundle yields
the same `Transform`.
"""

from __future__ import annotations

import datetime as dt
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING, Any, Final

from src.data.config import IntegrityError, LeakageError, PartitionError
from src.data.splits import Partition, training_range
from src.external.spaceweather import apply_carry_forward
from src.features._frames import column_values

if TYPE_CHECKING:  # pragma: no cover - typing only; build.py imports this module at runtime
    from src.features.build import FeatureBundle

__all__ = [
    "Transform",
    "FieldClass",
    "TRANSFORM_ID_PREFIX",
    "transform_id_for",
    "fit_transforms",
    "apply_fitted_transform",
    "assert_consumable",
    "carry_forward",
    "assert_field_classes_partition",
]

#: M9's transform-id form (`T-F1`, `T-REFIT`): an addressing identity, not a value.
TRANSFORM_ID_PREFIX: Final[str] = "T-"


class FieldClass(StrEnum):
    """Every dictionary field is exactly one of these (R-77 part 2's partition).

    `driver` and `target` are the two classes R-77 keeps apart at the carry-forward
    boundary; `station`, `time`, `support` and `diagnostic` are the remaining TE 6.2 rows,
    none of which carries forward at all. The partition is over the whole enum because a
    field belonging to no class — or to two — escapes both carry-forward rules.
    """

    driver = "driver"
    target = "target"
    station = "station"
    time = "time"
    support = "support"
    diagnostic = "diagnostic"


@dataclass(frozen=True)
class Transform:
    """ADR-11's `Transform` (`transform_id`, `partition_id`) plus intra-package fitted state.

    `touches_target` is R-84's machine-readable declaration; the primary configuration's
    transform acts on target-DERIVED inputs and never the target (D-27), so it is `False`
    for every transform this module fits. No `inverse` and no `apply` method exist here
    (Q4 = A).
    """

    transform_id: str
    partition_id: str
    columns: tuple[str, ...]
    means: Mapping[str, float]
    scales: Mapping[str, float]
    fitted_start: dt.datetime
    fitted_end: dt.datetime
    touches_target: bool = False
    fitted_on_rows: int = field(default=0)


def transform_id_for(partition_id: str) -> str:
    return f"{TRANSFORM_ID_PREFIX}{partition_id}"


# --- R-74 element 2: the fitting checks ---------------------------------------------------


def fit_transforms(bundle: FeatureBundle, *, partition: Partition) -> Transform:
    """Fit the train-only standardisation on a `train`-role, untransformed bundle whose scored
    range is EXACTLY the partition's training range.

    Raises
    ------
    PartitionError
        `bundle.spec.partition_id != partition.partition_id` — two declared ids disagree
        before anything is fitted (Recommendation 8's discriminating rule; the same
        condition `models-and-baselines` R-92 raises `PartitionError` on).
    LeakageError
        `bundle.spec.role != "train"`; `bundle.transform_id is not None`; or the scored range
        `[scored_start, scored_end)` is not exactly `[train_start, train_end + 1 day)` — in
        either direction. Over-wide is information flow outright; a strict subset is a fit
        that silently departs from the declared fold protocol (R-83's negative control).
    IntegrityError
        an empty matrix (a fit over zero rows is not a fit), or a declared standardised
        column with zero variance (a scale cannot be chosen for it by convenience).
    """
    spec = bundle.spec
    if spec.partition_id != partition.partition_id:
        raise PartitionError(
            f"bundle {spec.partition_id}/{spec.role}",
            f"spec.partition_id {spec.partition_id!r} disagrees with the fitting partition "
            f"{partition.partition_id!r}; a declared-identity disagreement (R-74 element 2, "
            f"Recommendation 8)",
        )
    if spec.role != "train":
        raise LeakageError(
            f"bundle {spec.partition_id}/{spec.role}",
            "a transform is fitted on a train-role bundle only; fitting on a score-role "
            "bundle is fitting on the validation month (R-74 element 2; NFR-LEAK-01)",
        )
    if bundle.transform_id is not None:
        raise LeakageError(
            f"bundle {spec.partition_id}/{spec.role}/{bundle.transform_id}",
            "bundle is already transformed; a transform is fitted on the untransformed "
            "fitting bundle, never re-fitted on transformed values (R-74 element 2)",
        )
    train_start, train_end = training_range(partition)
    if (spec.scored_start, spec.scored_end) != (train_start, train_end):
        direction = "over-wide" if (
            spec.scored_start < train_start or spec.scored_end > train_end
        ) else "a strict subset of"
        raise LeakageError(
            f"bundle {spec.partition_id}/{spec.role}",
            f"scored range [{spec.scored_start.isoformat()}, {spec.scored_end.isoformat()}) "
            f"is {direction} partition {partition.partition_id}'s training range "
            f"[{train_start.isoformat()}, {train_end.isoformat()}); a transform is fitted on "
            f"the training range EXACTLY — range equality, both bounds from the Partition "
            f"(R-74 element 1; R-83, BLK-09)",
        )
    columns = tuple(bundle.standardized_columns)
    n_rows = _row_count(bundle.matrix)
    if n_rows == 0:
        raise IntegrityError(
            f"bundle {spec.partition_id}/{spec.role}",
            "matrix is empty; a transform fitted over zero rows is a check that never ran",
        )
    means: dict[str, float] = {}
    scales: dict[str, float] = {}
    for column in columns:
        values = [float(v) for v in column_values(bundle.matrix, column)]
        if any(math.isnan(v) for v in values):
            raise IntegrityError(
                f"bundle {spec.partition_id}/{spec.role} column {column!r}",
                "carries NaN inside the fitting bundle; gaps are excluded and counted "
                "upstream, never standardised over",
            )
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        if variance <= 0.0:
            raise IntegrityError(
                f"bundle {spec.partition_id}/{spec.role} column {column!r}",
                "has zero variance over the training range; a scale for a constant column "
                "cannot be chosen by convenience — declare it `normalization: none` in the "
                "dictionary or fix the input (TE 18.2)",
            )
        means[column] = mean
        scales[column] = math.sqrt(variance)
    return Transform(
        transform_id=transform_id_for(partition.partition_id),
        partition_id=partition.partition_id,
        columns=columns,
        means=means,
        scales=scales,
        fitted_start=train_start,
        fitted_end=train_end,
        touches_target=False,
        fitted_on_rows=n_rows,
    )


def _row_count(matrix: Any) -> int:
    if hasattr(matrix, "shape"):
        return int(matrix.shape[0])
    return len(matrix)


def apply_fitted_transform(
    records: Sequence[Mapping[str, Any]], transform: Transform
) -> list[dict[str, Any]]:
    """Standardise `transform.columns` in place on plain records — INTRA-PACKAGE.

    Called ONLY by `build_features`, after the identity check has passed. This is not an
    apply surface for callers outside `src/features`: it takes records, not a bundle, and
    the leakage decision (which transform may touch which spec) is made before it runs.
    """
    out: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        row = dict(record)
        for column in transform.columns:
            if column not in row:
                raise LeakageError(
                    f"row {index}",
                    f"lacks standardised column {column!r}; the transform's columns and the "
                    f"frame's disagree, which means the frame is not the one the transform "
                    f"was fitted for",
                )
            row[column] = (float(row[column]) - transform.means[column]) / transform.scales[column]
        out.append(row)
    return out


def assert_consumable(bundle: FeatureBundle) -> None:
    """Every consumer (`fit_predict`, `06`, `07`) raises on an untransformed bundle."""
    if bundle.transform_id is None:
        raise LeakageError(
            f"bundle {bundle.spec.partition_id}/{bundle.spec.role}/untransformed",
            "transform_id is None: this is the fitting input, addressable and visible but "
            "never consumable — consuming it for training or scoring is the leak R-74 "
            "element 4 closes (W-4; FU-6 = A's surviving limb)",
        )


# --- R-77: the carry-forward boundary ----------------------------------------------------


def carry_forward(
    hourly: Mapping[dt.datetime, float | None],
    *,
    field_class: FieldClass,
    bound_h: int,
    feature: str,
) -> dict[str, Any]:
    """The bounded carry-forward, reachable by DRIVER-class fields only (R-77 part 1).

    Raises
    ------
    LeakageError
        for every class other than `driver`. `vtec_lag_*` (target-derived) is refused
        here: FR-P1-04-3's <= 3 h allowance is scoped to external drivers and "must never be
        read as reaching `vtec_lag_*`" — the target-derived window is EXCLUDED instead
        (FR-P1-04-13).
    """
    if not isinstance(field_class, FieldClass):
        raise LeakageError(
            f"carry-forward of {feature!r}",
            f"field_class {field_class!r} is not a FieldClass; the class is a REQUIRED "
            f"argument of the carry-forward path (R-77 part 1)",
        )
    if field_class is not FieldClass.driver:
        raise LeakageError(
            f"carry-forward of {feature!r}",
            f"field class {field_class.value!r} never carries forward; the <= bound_h "
            f"allowance is scoped to external drivers only (FR-P1-04-3), a target-derived "
            f"lag's window is excluded and counted instead (FR-P1-04-13), and no other "
            f"class has a value to carry",
        )
    result = apply_carry_forward(hourly, bound_h=bound_h)
    result["feature"] = feature
    result["excluded_count"] = len(result["excluded_epochs"])
    return result


def assert_field_classes_partition(
    dictionary_classes: Mapping[str, Any],
) -> dict[str, FieldClass]:
    """Every dictionary field maps to exactly one `FieldClass` (R-77 part 2).

    Raises
    ------
    LeakageError
        a field with no class, an unknown class, or a class list (two classes); a
        `vtec_lag_*` / `vtec_seq_*` field declared anything but `target` (which would let it
        into the driver carry-forward path).
    """
    out: dict[str, FieldClass] = {}
    for name, declared in dictionary_classes.items():
        if isinstance(declared, list | tuple | set | frozenset):
            raise LeakageError(
                f"feature dictionary field {name!r}",
                f"declares {len(declared)} classes {sorted(map(str, declared))}; the classes "
                f"PARTITION the dictionary — exactly one per field (R-77 part 2)",
            )
        if declared is None or not str(declared).strip():
            raise LeakageError(
                f"feature dictionary field {name!r}",
                "declares no field class; a field in no class escapes both carry-forward "
                "rules (R-77 part 2)",
            )
        try:
            field_class = FieldClass(str(declared))
        except ValueError as exc:
            raise LeakageError(
                f"feature dictionary field {name!r}",
                f"class {declared!r} is not one of {[c.value for c in FieldClass]}",
            ) from exc
        lowered = name.lower()
        if (lowered.startswith("vtec_lag_") or lowered.startswith("vtec_seq_")) and (
            field_class is not FieldClass.target
        ):
            raise LeakageError(
                f"feature dictionary field {name!r}",
                f"target-derived lag declared {field_class.value!r}; vtec_lag_* and "
                f"vtec_seq_* are target-derived and carry-forward is prohibited for them "
                f"(FR-P1-04-13)",
            )
        out[name] = field_class
    return out
