"""M-03 station x hour climatology, fitted on TRAINING partitions only (W-9; R-98).

Purpose
-------
The third difficulty control (Vision 2.4; FR-P1-05-21). The climatology is the mean target
value per KEY over the rows of a TRAIN-role bundle whose timestamps all lie inside the
fitting partition's training range. A climatology fitted across all of the study year --
validation months or the locked month included -- "stops functioning as a difficulty control
while passing every other stated check" (R-98), so the fit REFUSES (`LeakageError`) rather
than passing a module inventory.

The key is read from `configs/experiment.yaml` `models.climatology.key` and is
`(station, hour of day)`. No key definition is spelled as a scientific constant in source
(TC-03e): this module holds the field IDENTITIES it knows how to compute and refuses a
configured key it cannot produce, exactly as `checkpoint.py` refuses a checkpoint policy it
does not implement.

Why the key carries no month
----------------------------
The split calendar is a strictly expanding window: every partition's scored month lies
AFTER its training range (F1 trains on January-March and is scored on April; F2 on
January-June scored on July; F3 on January-September scored on October; F4 on
January-October scored on November; DEC on January-November scored on December). A
`(station, calendar month, hour)` key fitted on the training range therefore cannot produce
a single key that the scored month demands -- five of five scored partitions -- and the
earlier form of this module answered `y_hat = None` for EVERY scored row while reporting
the shortfall only as a count. The difficulty control produced nothing at all. Dropping
month from the key makes every scored row producible from the training range, which is the
property the fit-time coverage guard below now asserts rather than assumes.

Seasonal limitation -- state this wherever M-03's performance is reported
------------------------------------------------------------------------
A station-by-hour climatology carries NO seasonal term. It is the mean diurnal shape of the
whole training range, not of the scored month, so it does not adjust for season, and it is a
weaker difficulty control than a station-by-month-by-hour climatology would be. Every
interpretation of M-03's performance -- the primary results table, any regime breakdown, and
the abstract-level conclusion -- must say so: where a model beats M-03, part of the margin
may be seasonal adjustment that M-03 structurally cannot make, and where M-03 is competitive
the comparison is against a control that never adjusted for the scored month's season. The
sentence travels with the fitted object (`Climatology.limitation`) and onto every prediction
frame (`climatology_limitation`) so a reader of the artifact cannot miss it.

Vision 2.4 names the third difficulty control as a fitted station x month x hour
climatology. This key does NOT satisfy that wording. The substitution is the project
decision owner's ruling, recorded under its own D-number before G-05 and verified without
touching the locked test; it is not a choice this module makes, and the config block is the
one place the choice is written down.

`climatology_fit_partition(prediction)` -- the approved signature (`component-methods.md`) --
returns the partition identifiers M-03 was ACTUALLY fitted on, read from the prediction
frame's attrs, so the negative case fails a test. The approved `Prediction` shape is not
amended for this (the ninth-amendment option `domain-entities.md` section 6 declined).

Inputs
------
A consumable train-role `FeatureBundle` (the fit), the score-role bundle whose keys the fit
must cover (`None` only on the REFIT persist path, where no scored bundle exists yet and the
SAME guard runs when the persisted state is loaded), the `Partition`, the `ConfigSnapshot`
(the key definition), the D-17 target frame (the values), the horizon (recorded, not used: a
climatology is a function of the key alone).

Re-run behaviour
----------------
Pure functions; deterministic. A key the fit cannot produce is an INTEGRITY FAILURE, not a
missing value: the fit-time guard raises naming the missing keys, the fitting range and the
config field, and `predict_rows` raises rather than emitting `y_hat = None`. Nothing is
interpolated or filled. `missing_climatology_keys` stays on the prediction frame as a
measured zero, so the artifact records that coverage was checked rather than assumed.

Boundaries
----------
No scientific constant. No inverse: the climatology is computed in raw TECU from the target
series, never from standardised bundle columns (D-27). Never imports `src.external.iri`,
`src.external.gim`, `src.evaluation` or any NN stack.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final

from src.data.config import TBD_SENTINEL, IntegrityError, LeakageError
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
    "CLIMATOLOGY_KEY_FIELDS",
    "FITTED_ON_TOKEN",
    "SEASONAL_LIMITATION",
    "Climatology",
    "FittedPartitionRecord",
    "read_climatology_key",
    "fit_climatology",
    "assert_keys_cover_scored_rows",
    "predict_rows",
    "climatology_fit_partition",
    "assert_fitted_on_training_partitions",
    "fit_state",
    "climatology_from_state",
    "predict_rows_from_state",
    "fit_predict_rows",
]

#: The key-field IDENTITIES this module can compute -- never a key definition, which lives in
#: `configs/experiment.yaml` `models.climatology.key` (TC-03e). A configured field outside
#: this table refuses by name, so a month-bearing key cannot be adopted by editing config
#: alone: it would need an implementation here and the ordering argument in the docstring
#: above re-examined.
_KEY_FIELD_VALUES: Final[Mapping[str, Callable[[str, dt.datetime], Any]]] = {
    "station": lambda station, stamp: station,
    "hour": lambda station, stamp: stamp.hour,
}
#: The ordered key this module implements -- an identity tuple, asserted against config.
CLIMATOLOGY_KEY_FIELDS: Final[tuple[str, ...]] = ("station", "hour")
#: The one `fitted_on` token this module implements (R-98's train-only rule, as config states
#: it). Any other value refuses: the fit is not widened by a configuration edit.
FITTED_ON_TOKEN: Final[str] = "training_partition_only"

#: The prose a supervisor reads. Travels on the fitted object and on every prediction frame.
SEASONAL_LIMITATION: Final[str] = (
    "M-03 is a station-by-hour climatology and carries no seasonal term: it is the mean "
    "diurnal shape of the whole training range, not of the scored month. It does not adjust "
    "for season and is therefore a weaker difficulty control than a station-by-month-by-hour "
    "climatology would be. Any interpretation of M-03's performance must state this — where "
    "a model beats M-03, part of the margin may be seasonal adjustment M-03 structurally "
    "cannot make, and where M-03 is competitive the comparison is against a control that "
    "never adjusted for the scored month's season."
)

#: How many missing keys the coverage refusal prints before it summarises the rest.
_MISSING_KEYS_SHOWN: Final[int] = 12


def _is_tbd(value: object) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == TBD_SENTINEL)


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
    """The fitted table, the key it is grouped by, and the limitation that travels with it."""

    means: Mapping[tuple[Any, ...], float]
    counts: Mapping[tuple[Any, ...], int]
    record: FittedPartitionRecord
    key_fields: tuple[str, ...]
    limitation: str = SEASONAL_LIMITATION


def read_climatology_key(snapshot: ConfigSnapshot) -> tuple[str, ...]:
    """`models.climatology`: the ONE copy of M-03's key definition (TC-03e).

    Raises
    ------
    IntegrityError
        the block or `key` absent or `TBD — freeze gate`; a key field this module cannot
        compute; a key that is not the one this module implements. The definition is the
        owner's, recorded under its own D-number before G-05 — never defaulted here
        (TE 18.3).
    LeakageError
        `fitted_on` is not `training_partition_only`; the fit is not widened by a config edit.
    """
    models = snapshot.experiment.get("models")
    block = models.get("climatology") if isinstance(models, Mapping) else None
    if _is_tbd(block) or not isinstance(block, Mapping):
        raise IntegrityError(
            "configs/experiment.yaml: models.climatology",
            "absent or unresolved (TBD — freeze gate); M-03's key definition is a governed "
            "scientific choice recorded under its own D-number before G-05 and reaches the "
            "code only from configuration (TC-03e) — stop and report, never default (TE 18.3)",
        )
    key = block.get("key")
    if _is_tbd(key) or not isinstance(key, list | tuple) or not key:
        raise IntegrityError(
            "configs/experiment.yaml: models.climatology.key",
            "absent, unresolved or empty; the key is the ordered list of field identities the "
            "mean is grouped by",
        )
    fields = tuple(str(f) for f in key)
    unknown = [f for f in fields if f not in _KEY_FIELD_VALUES]
    if unknown:
        raise IntegrityError(
            "configs/experiment.yaml: models.climatology.key",
            f"names key field(s) {unknown} that src/models/climatology.py cannot compute; the "
            f"implemented fields are {list(_KEY_FIELD_VALUES)}. A month-bearing key in "
            f"particular cannot be produced from a strictly expanding training window — every "
            f"scored month lies after its own training range — so adopting one needs an "
            f"implementation here and a re-examination of that ordering, not a config edit",
        )
    if fields != CLIMATOLOGY_KEY_FIELDS:
        raise IntegrityError(
            "configs/experiment.yaml: models.climatology.key",
            f"is {list(fields)}; src/models/climatology.py implements "
            f"{list(CLIMATOLOGY_KEY_FIELDS)} exactly, in that order, and refuses a key it does "
            f"not implement rather than silently grouping by something else",
        )
    fitted_on = block.get("fitted_on")
    if _is_tbd(fitted_on) or str(fitted_on) != FITTED_ON_TOKEN:
        raise LeakageError(
            "configs/experiment.yaml: models.climatology.fitted_on",
            f"is {fitted_on!r}, not {FITTED_ON_TOKEN!r}; M-03 is fitted exclusively on each "
            f"partition's own training data and no configuration value widens that (R-98; "
            f"NFR-LEAK-01)",
        )
    return fields


def _key(key_fields: Sequence[str], station: str, stamp: dt.datetime) -> tuple[Any, ...]:
    """The grouping key for one row, built in the CONFIGURED field order."""
    return tuple(_KEY_FIELD_VALUES[field](station, stamp) for field in key_fields)


def fit_climatology(
    bundle: FeatureBundle,
    *,
    partition: Partition,
    series: Mapping[tuple[str, dt.datetime], float],
    snapshot: ConfigSnapshot,
    score_bundle: FeatureBundle | None,
) -> Climatology:
    """Fit on the TRAIN-role bundle's rows, all inside the partition's training range.

    `score_bundle` is the bundle this fit will be asked to predict on. It is a REQUIRED
    keyword with no default so no caller can skip the coverage guard by omission. Pass `None`
    ONLY on the REFIT persist path, where the scored bundle does not exist yet; the same
    guard (`assert_keys_cover_scored_rows`) then runs when the persisted state is loaded, so
    the boundary keeps exactly one guard home.

    Raises
    ------
    LeakageError
        `bundle.spec.role != "train"`; any row whose timestamp lies outside
        `[train_start, train_end + 1 day)` — the "fitted across all of 2022" case FR-P1-05-21
        names; the bundle's `partition_id` disagreeing with the fitting partition; a
        `fitted_on` in config that is not `training_partition_only`.
    IntegrityError
        the key definition absent or unimplementable; no row carries a target value (a fit
        over zero rows is not a fit); a key the scored bundle demands that this fit cannot
        produce (the fail-early coverage guard).
    """
    key_fields = read_climatology_key(snapshot)
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
    sums: dict[tuple[Any, ...], float] = {}
    counts: dict[tuple[Any, ...], int] = {}
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
        key = _key(key_fields, station, stamp)
        sums[key] = sums.get(key, 0.0) + value
        counts[key] = counts.get(key, 0) + 1
        rows += 1
    if rows == 0:
        raise IntegrityError(
            f"bundle {spec.partition_id}/{spec.role}",
            "no row carries a target value; a climatology fitted over zero rows is not a fit",
        )
    climatology = Climatology(
        means={key: sums[key] / counts[key] for key in sums},
        counts=counts,
        key_fields=key_fields,
        limitation=SEASONAL_LIMITATION,
        record=FittedPartitionRecord(
            partition_ids=(partition.partition_id,),
            role="train",
            fitted_start=start.isoformat(),
            fitted_end=end.isoformat(),
            fitted_rows=rows,
        ),
    )
    if score_bundle is not None:
        assert_keys_cover_scored_rows(climatology, score_bundle)
    return climatology


def assert_keys_cover_scored_rows(
    climatology: Climatology, score_bundle: FeatureBundle
) -> None:
    """Fail EARLY: every key the scored bundle demands must be producible from the fit.

    The single guard home for M-03's coverage boundary. Called from `fit_climatology` when
    the scored bundle is known at fit time (the fold path) and from `predict_rows_from_state`
    when it is not (the REFIT persist path), so every public entry point is guarded and the
    failure never waits for prediction.

    Raises
    ------
    IntegrityError
        naming the missing `(station, hour)` keys, the fitting range they could not be
        produced from, and the config field that defines the key.
    """
    missing: list[tuple[Any, ...]] = []
    seen: set[tuple[Any, ...]] = set()
    for station, stamp in bundle_index(score_bundle):
        key = _key(climatology.key_fields, station, stamp)
        if key not in climatology.means and key not in seen:
            seen.add(key)
            missing.append(key)
    if not missing:
        return
    ordered = sorted(missing, key=lambda k: tuple(str(part) for part in k))
    shown = ordered[:_MISSING_KEYS_SHOWN]
    tail = "" if len(ordered) <= _MISSING_KEYS_SHOWN else f" (+{len(ordered) - len(shown)} more)"
    raise IntegrityError(
        f"src/models/climatology.py: M-03 fitted for partition "
        f"{climatology.record.partition_ids[0]} over "
        f"[{climatology.record.fitted_start}, {climatology.record.fitted_end})",
        f"cannot produce {len(ordered)} key(s) {shown}{tail} keyed by "
        f"{list(climatology.key_fields)} (configs/experiment.yaml: models.climatology.key) "
        f"that the scored bundle {score_bundle.spec.partition_id}/{score_bundle.spec.role} "
        f"demands. Every scored row must be producible from the training range; a key that is "
        f"not is a silent hole in the difficulty control rather than a missing value, so the "
        f"fit fails here and never at prediction time (R-98; FR-P1-05-21)",
    )


def predict_rows(
    climatology: Climatology, score_bundle: FeatureBundle
) -> tuple[list[dict[str, Any]], int]:
    """`y_hat` per scored row. A key the fit cannot produce RAISES — never `y_hat = None`.

    The returned count is the measured number of missing keys, which the coverage guard
    makes zero by construction; it stays on the prediction frame so the artifact records
    that coverage was checked rather than assumed.
    """
    rows: list[dict[str, Any]] = []
    missing = 0
    for station, stamp in bundle_index(score_bundle):
        key = _key(climatology.key_fields, station, stamp)
        if key not in climatology.means:
            raise IntegrityError(
                f"src/models/climatology.py: M-03 prediction for "
                f"{score_bundle.spec.partition_id}/{score_bundle.spec.role} row {station} "
                f"{stamp.isoformat()}",
                f"demands key {key!r}, which the fit over "
                f"[{climatology.record.fitted_start}, {climatology.record.fitted_end}) cannot "
                f"produce. Reaching here means the fit was never put through "
                f"assert_keys_cover_scored_rows for this bundle; a climatology that answers "
                f"nothing is not a difficulty control (R-98)",
            )
        rows.append(
            {"station": station, "interval_start_utc": stamp, "y_hat": climatology.means[key]}
        )
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


def _prediction_attrs(
    climatology: Climatology, *, score_bundle: FeatureBundle, horizon_hours: int, missing: int
) -> dict[str, Any]:
    record = climatology.record
    return {
        "role": score_bundle.spec.role,
        "horizon_hours": horizon_hours,
        "fitted_partitions": list(record.partition_ids),
        "fitted_role": record.role,
        "fitted_start": record.fitted_start,
        "fitted_end": record.fitted_end,
        "fitted_rows": record.fitted_rows,
        "missing_climatology_keys": missing,
        "climatology_key": list(climatology.key_fields),
        "climatology_limitation": climatology.limitation,
    }


# --- the persist / load-and-predict surface (the REFIT -> DEC path) -----------------------


def fit_state(
    model_id: str,
    *,
    bundle: FeatureBundle,
    partition: Partition,
    snapshot: ConfigSnapshot,
    target: Any,
    seed: int | None = None,
    params: Mapping[str, Any] | None = None,
    horizon_hours: int,
    validation_bundle: FeatureBundle | None = None,
    backend: Any | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Fit WITHOUT predicting and return the JSON-serialisable state plus its fit attrs.

    The REFIT half of the locked path: the model is fitted on January-November and persisted;
    the scored bundle does not exist yet, so the coverage guard runs in
    `predict_rows_from_state` instead — the same function, the same boundary.
    """
    if model_id != "M-03":
        raise IntegrityError(f"model_id {model_id!r}", "climatology.py serves M-03 only")
    if params is not None:
        raise IntegrityError(
            "fit_state(M-03)", "the climatology has no hyperparameters; params is refused"
        )
    climatology = fit_climatology(
        bundle,
        partition=partition,
        series=target_series(target),
        snapshot=snapshot,
        score_bundle=None,
    )
    record = climatology.record
    state = {
        "model_id": "M-03",
        "key_fields": list(climatology.key_fields),
        "limitation": climatology.limitation,
        "entries": [
            {"key": list(key), "mean": float(mean), "count": int(climatology.counts[key])}
            for key, mean in sorted(
                climatology.means.items(), key=lambda kv: tuple(str(p) for p in kv[0])
            )
        ],
        "fitted_partitions": list(record.partition_ids),
        "fitted_role": record.role,
        "fitted_start": record.fitted_start,
        "fitted_end": record.fitted_end,
        "fitted_rows": record.fitted_rows,
        "horizon_hours": horizon_hours,
    }
    attrs = {
        "fitted_partitions": list(record.partition_ids),
        "fitted_role": record.role,
        "fitted_start": record.fitted_start,
        "fitted_end": record.fitted_end,
        "fitted_rows": record.fitted_rows,
        "climatology_key": list(climatology.key_fields),
        "climatology_limitation": climatology.limitation,
    }
    return state, attrs


def climatology_from_state(state: Mapping[str, Any]) -> Climatology:
    """Rebuild the fitted table from a persisted state; a malformed state RAISES."""
    try:
        key_fields = tuple(str(f) for f in state["key_fields"])
        entries = list(state["entries"])
        means = {tuple(entry["key"]): float(entry["mean"]) for entry in entries}
        counts = {tuple(entry["key"]): int(entry["count"]) for entry in entries}
        record = FittedPartitionRecord(
            partition_ids=tuple(str(p) for p in state["fitted_partitions"]),
            role=str(state["fitted_role"]),
            fitted_start=str(state["fitted_start"]),
            fitted_end=str(state["fitted_end"]),
            fitted_rows=int(state["fitted_rows"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise IntegrityError(
            "persisted M-03 state", f"is malformed ({exc}); a fitted climatology is not guessed"
        ) from exc
    if key_fields != CLIMATOLOGY_KEY_FIELDS:
        raise IntegrityError(
            "persisted M-03 state",
            f"was fitted on key {list(key_fields)}; this module implements "
            f"{list(CLIMATOLOGY_KEY_FIELDS)} and never reinterprets a persisted key",
        )
    if record.role != "train":
        raise LeakageError(
            "persisted M-03 state", f"records fitted_role {record.role!r}, not 'train' (R-98)"
        )
    return Climatology(
        means=means,
        counts=counts,
        record=record,
        key_fields=key_fields,
        limitation=str(state.get("limitation") or SEASONAL_LIMITATION),
    )


def predict_rows_from_state(
    state: Mapping[str, Any],
    model_id: str,
    *,
    score_bundle: FeatureBundle,
    partition: Partition,
    snapshot: ConfigSnapshot,
    target: Any = None,
    horizon_hours: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Predict from a PERSISTED fit — no fitting happens here (the locked path's half)."""
    if model_id != "M-03":
        raise IntegrityError(f"model_id {model_id!r}", "climatology.py serves M-03 only")
    read_climatology_key(snapshot)  # the configured key must still be the one that was fitted
    climatology = climatology_from_state(state)
    assert_keys_cover_scored_rows(climatology, score_bundle)  # the same guard, this entry point
    rows, missing = predict_rows(climatology, score_bundle)
    return rows, _prediction_attrs(
        climatology, score_bundle=score_bundle, horizon_hours=horizon_hours, missing=missing
    )


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
    validation_bundle: FeatureBundle | None = None,
) -> Prediction:
    """The family entry `train.fit_predict` dispatches to for M-03.

    `validation_bundle` is accepted for a uniform family signature and is unused: M-03 has no
    early stopping and no epoch count to select.
    """
    if model_id != "M-03":
        raise IntegrityError(f"model_id {model_id!r}", "climatology.py serves M-03 only")
    if params is not None:
        raise IntegrityError(
            "fit_predict(M-03)", "the climatology has no hyperparameters; params is refused"
        )
    series = target_series(target)
    climatology = fit_climatology(
        bundle,
        partition=partition,
        series=series,
        snapshot=snapshot,
        score_bundle=score_bundle,
    )
    rows, missing = predict_rows(climatology, score_bundle)
    return new_prediction(
        model_id,
        seed=None,
        rows=rows,
        bundle=score_bundle,
        partition=partition,
        attrs=_prediction_attrs(
            climatology,
            score_bundle=score_bundle,
            horizon_hours=horizon_hours,
            missing=missing,
        ),
    )
