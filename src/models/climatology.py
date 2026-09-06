"""M-03 station x month x hour climatology, fitted on TRAINING partitions only (W-9; R-98).

Purpose
-------
The third difficulty control (Vision 2.4; FR-P1-05-21). The climatology is the mean target
value per `(station, calendar month, hour of day)` over the rows of a TRAIN-role bundle whose
timestamps all lie inside the fitting partition's training range. A climatology fitted across
all of the study year — validation months or the locked month included — "stops functioning
as a difficulty control while passing every other stated check" (R-98), so the fit REFUSES
(`LeakageError`) rather than passing a module inventory.

`climatology_fit_partition(prediction)` — the approved signature (`component-methods.md`) —
returns the partition identifiers M-03 was ACTUALLY fitted on, read from the prediction
frame's attrs, so the negative case fails a test. The approved `Prediction` shape is not
amended for this (the ninth-amendment option `domain-entities.md` section 6 declined).

Inputs
------
A consumable train-role `FeatureBundle` (the fit) and score-role bundle (the prediction), the
`Partition`, the D-17 target frame (the values), the horizon (recorded, not used: a
climatology is a function of the target hour alone).

Re-run behaviour
----------------
Pure functions; deterministic. A `(station, month, hour)` key absent from the fitted table
yields `y_hat = None`, COUNTED on the frame's attrs (`missing_climatology_keys`) — the
downstream comparison-wide mask excludes it; nothing is interpolated or filled.

Boundaries
----------
No scientific constant. No inverse: the climatology is computed in raw TECU from the target
series, never from standardised bundle columns (D-27). Never imports `src.external.iri`,
`src.external.gim`, `src.evaluation` or any NN stack.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from src.data.config import IntegrityError, LeakageError
from src.data.splits import PARTITION_IDS, Partition, training_range
from src.features._frames import frame_attrs
from src.features.build import FeatureBundle
from src.models.train import (
    ConfigSnapshot,
    Prediction,
    bundle_index,
    new_prediction,
    target_series,
)

__all__ = [
    "Climatology",
    "FittedPartitionRecord",
    "fit_climatology",
    "predict_rows",
    "climatology_fit_partition",
    "assert_fitted_on_training_partitions",
    "fit_predict_rows",
]


@dataclass(frozen=True)
class FittedPartitionRecord:
    """`domain-entities.md` section 6: the partitions M-03 was actually fitted on."""

    partition_ids: tuple[str, ...]
    role: str
    fitted_start: str
    fitted_end: str
    fitted_rows: int


@dataclass(frozen=True)
class Climatology:
    means: Mapping[tuple[str, int, int], float]
    counts: Mapping[tuple[str, int, int], int]
    record: FittedPartitionRecord


def fit_climatology(
    bundle: FeatureBundle,
    *,
    partition: Partition,
    series: Mapping[tuple[str, dt.datetime], float],
) -> Climatology:
    """Fit on the TRAIN-role bundle's rows, all inside the partition's training range.

    Raises
    ------
    LeakageError
        `bundle.spec.role != "train"`; any row whose timestamp lies outside
        `[train_start, train_end + 1 day)` — the "fitted across all of 2022" case FR-P1-05-21
        names; the bundle's `partition_id` disagreeing with the fitting partition.
    IntegrityError
        no row carries a target value (a fit over zero rows is not a fit).
    """
    spec = bundle.spec
    if spec.role != "train":
        raise LeakageError(
            f"bundle {spec.partition_id}/{spec.role}",
            "M-03 is fitted on a train-role bundle only; a score-role bundle is the validation "
            "month (R-98; NFR-LEAK-01)",
        )
    if spec.partition_id != partition.partition_id:
        raise LeakageError(
            f"bundle {spec.partition_id}/{spec.role}",
            f"fitted for partition {partition.partition_id!r}; the training rows must be that "
            f"partition's own (R-98)",
        )
    start, end = training_range(partition)
    sums: dict[tuple[str, int, int], float] = {}
    counts: dict[tuple[str, int, int], int] = {}
    rows = 0
    for station, stamp in bundle_index(bundle):
        if not (start <= stamp < end):
            raise LeakageError(
                f"bundle {spec.partition_id}/{spec.role} row {station} {stamp.isoformat()}",
                f"lies outside partition {partition.partition_id}'s training range "
                f"[{start.isoformat()}, {end.isoformat()}); a climatology fitted on validation or "
                f"locked-month rows stops being a difficulty control (R-98; FR-P1-05-21)",
            )
        value = series.get((station, stamp))
        if value is None:
            continue
        key = (station, stamp.month, stamp.hour)
        sums[key] = sums.get(key, 0.0) + value
        counts[key] = counts.get(key, 0) + 1
        rows += 1
    if rows == 0:
        raise IntegrityError(
            f"bundle {spec.partition_id}/{spec.role}",
            "no row carries a target value; a climatology fitted over zero rows is not a fit",
        )
    means = {key: sums[key] / counts[key] for key in sums}
    return Climatology(
        means=means,
        counts=counts,
        record=FittedPartitionRecord(
            partition_ids=(partition.partition_id,),
            role="train",
            fitted_start=start.isoformat(),
            fitted_end=end.isoformat(),
            fitted_rows=rows,
        ),
    )


def predict_rows(
    climatology: Climatology, score_bundle: FeatureBundle
) -> tuple[list[dict[str, Any]], int]:
    rows: list[dict[str, Any]] = []
    missing = 0
    for station, stamp in bundle_index(score_bundle):
        value = climatology.means.get((station, stamp.month, stamp.hour))
        if value is None:
            missing += 1
        rows.append({"station": station, "interval_start_utc": stamp, "y_hat": value})
    return rows, missing


def climatology_fit_partition(prediction: Prediction) -> Sequence[str]:
    """The approved signature: the partition identifiers M-03 was ACTUALLY fitted on."""
    if prediction.model_id != "M-03":
        raise IntegrityError(
            f"prediction {prediction.model_id}", "climatology_fit_partition applies to M-03 only"
        )
    attrs = frame_attrs(prediction.frame)
    fitted = attrs.get("fitted_partitions")
    if not isinstance(fitted, list | tuple) or not fitted:
        raise IntegrityError(
            "prediction M-03",
            "carries no fitted_partitions record; the fitting partitions travel with the "
            "prediction so the negative case fails a test rather than a module inventory (R-98)",
        )
    return tuple(str(p) for p in fitted)


def assert_fitted_on_training_partitions(prediction: Prediction) -> None:
    """Every returned identifier is a training partition, fitted under role `train`."""
    fitted = climatology_fit_partition(prediction)
    attrs = frame_attrs(prediction.frame)
    if attrs.get("fitted_role") != "train":
        raise LeakageError(
            "prediction M-03",
            f"fitted under role {attrs.get('fitted_role')!r}, not 'train' (R-98)",
        )
    for pid in fitted:
        if pid not in PARTITION_IDS:
            raise LeakageError("prediction M-03", f"fitted on unknown partition {pid!r}")


def fit_predict_rows(
    model_id: str,
    *,
    bundle: FeatureBundle,
    score_bundle: FeatureBundle,
    partition: Partition,
    snapshot: ConfigSnapshot,
    target: Any,
    seed: int | None,
    params: Mapping[str, Any] | None,
    horizon_hours: int,
) -> Prediction:
    """The family entry `train.fit_predict` dispatches to for M-03."""
    if model_id != "M-03":
        raise IntegrityError(f"model_id {model_id!r}", "climatology.py serves M-03 only")
    if params is not None:
        raise IntegrityError(
            "fit_predict(M-03)", "the climatology has no hyperparameters; params is refused"
        )
    series = target_series(target)
    climatology = fit_climatology(bundle, partition=partition, series=series)
    rows, missing = predict_rows(climatology, score_bundle)
    record = climatology.record
    return new_prediction(
        model_id,
        seed=None,
        rows=rows,
        bundle=score_bundle,
        partition=partition,
        attrs={
            "role": score_bundle.spec.role,
            "horizon_hours": horizon_hours,
            "fitted_partitions": list(record.partition_ids),
            "fitted_role": record.role,
            "fitted_start": record.fitted_start,
            "fitted_end": record.fitted_end,
            "fitted_rows": record.fitted_rows,
            "missing_climatology_keys": missing,
        },
    )
