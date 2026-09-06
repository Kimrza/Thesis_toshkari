"""C-1/C-3 training orchestration: the boundary shapes, the stamp match, the three-seed
mean, tuning, the grid freeze, selection, the ablation registry, the horizon, the receipt.

Purpose
-------
The `src/models` hub (`unit-of-work.md` section 8; W-1, W-2, W-3, W-5, W-6, W-7, W-8, W-12;
R-90 ... R-102a). It owns:

* `Prediction` -- the approved eight-field boundary shape (`component-methods.md`), carrying
  `partition_id` and `transform_id` so the provenance `FeatureBundle` established survives
  `06` -> `07` (ADR-11).
* `assert_stamp_match(bundle, partition_being_scored)` -- R-90's named function, called by
  `06` before EVERY scoring path: `spec.partition_id` equals the scored partition
  (`PartitionError`), `spec.role == "score"` (`PartitionError`), `transform_id` present and
  equal to that partition's own transform (`LeakageError`). The split follows R-92's
  discriminating rule: declared-identity disagreements versus information flow.
* `fit_predict(model_id, *, bundle, partition, snapshot)` -- the approved training call over
  the closed six-family set; `LeakageError` when `bundle.transform_id is None`; the horizon
  travels from `snapshot` as a parameter (R-99) and no code path branches on a literal one.
* `three_seed_mean(predictions, *, expected_seeds)` -- BLK-03's contract, approved 2026-09-06
  (`governance/CHANGE_RECORD_2026-09-06_BLK03_confirmatory_contract.md`): all four limbs.
  `expected_seeds` is read from `ConfigSnapshot.seeds` AT THE CALL SITE and never inlined here.
* `TuningRecord` / `record_tuning` -- R-95's two runnable mechanisms plus SD-M-01's
  unconditional attestation (seven approved fields + three attestation fields).
* the grid freeze (R-96): the grid lives once in `configs/experiment.yaml`; content is
  asserted against config (cardinality = enumerated product, seven settings present) and the
  frozen object is its hash. NO grid value, seed or setting is held in this module.
* selection (R-101): mean per-fold skill; raw RMSE and row-count weighting refused; the
  refit changes no hyperparameter. The 1% tolerance and the declared baseline are
  configuration (Vision 8.7 / D-124) and REFUSE while `TBD -- freeze gate`.
* the ablation registry (R-97): five named entries read from `experiment.yaml`; a missing one
  fails; `ABL-HIST48` refuses before the primary freeze; `ABL-DIFF` refuses while no inverse
  exists, naming D-27.
* `PredictionHashReceipt` (R-102a; SD-M-04): `.tmp` -> fsync -> atomic rename; the receipt file
  is authoritative for the hash, the registry row for the run's existence, and `06` refuses to
  exit unless both landed.

Inputs
------
`FeatureBundle`s and `Partition`s produced by `features-and-splits`; a `ConfigSnapshot`
(`experiment.grids`, `experiment.models`, `experiment.ablations`, `experiment.horizons`,
`seeds.final`); the D-17 target frame for labels and the raw-TECU series the two persistence
families read. Nothing is read from `configs/` here (foundation R-15) and no third-party
package is imported at module scope.

Re-run behaviour
----------------
Pure functions of their inputs; deterministic; the receipt writer is the one persisting
function and it never overwrites an existing receipt.

Boundaries
----------
Never imports `src.external.iri`, `src.external.gim`, `src.evaluation`, or a second
deep-learning stack (R-102; TE 12; TE 8.3). Family modules are imported lazily inside
`fit_predict` so this module can be the shared `Prediction` home without a cycle. Never names
the restricted December root.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import itertools
import json
import math
import os
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from src.data.config import (
    TBD_SENTINEL,
    AlignmentError,
    ConfigSnapshot,
    IntegrityError,
    InverseTransformError,
    LeakageError,
    LockedTestError,
    PartitionError,
    PhaseBoundaryError,
    SeedError,
)
from src.data.release import sha256_of_file
from src.data.splits import LOCKED_ID, PARTITION_IDS, REFIT_ID, Partition
from src.features._frames import frame_attrs, frame_from_records, records_of
from src.features.build import FeatureBundle
from src.features.transforms import assert_consumable, transform_id_for

__all__ = [
    "MODEL_IDS",
    "SEEDED_MODEL_IDS",
    "PREDICTION_COLUMNS",
    "TARGET_TIMESTAMP_COLUMN",
    "TARGET_STATION_COLUMN",
    "TARGET_VALUE_COLUMN",
    "GRID_TRACKS",
    "LSTM_FIXED_SETTING_KEYS",
    "ABLATION_IDS",
    "Prediction",
    "TuningRecord",
    "CandidateScore",
    "AblationEntry",
    "PredictionHashReceipt",
    "pinned_requirement",
    "read_horizons",
    "resolve_horizon",
    "eligible_feature_columns",
    "feature_rows",
    "target_series",
    "bundle_index",
    "labels_for",
    "new_prediction",
    "prediction_index",
    "expected_transform_id",
    "assert_stamp_match",
    "fit_predict",
    "three_seed_mean",
    "criterion_hash",
    "record_tuning",
    "read_grids",
    "enumerate_grid",
    "assert_grid_content",
    "assert_in_grid",
    "grid_hash",
    "assert_grid_unchanged",
    "read_lstm_fixed_settings",
    "mean_per_fold_skill",
    "select_configuration",
    "assert_refit_unchanged",
    "read_ablations",
    "assert_ablation_runnable",
    "assert_no_promotion",
    "write_prediction_hash_receipt",
    "load_prediction_hash_receipt",
    "assert_receipt_matches",
    "assert_locked_exit_allowed",
]

#: FR-P1-05-1's closed model set -- identities, never values (R-102).
MODEL_IDS: Final[tuple[str, ...]] = ("M-01", "M-02", "M-03", "M-04", "M-05", "M-06")
#: Only M-06 is seeded; `Prediction.seed is None` is CORRECT for the other five
#: (`domain-entities.md` section 1).
SEEDED_MODEL_IDS: Final[tuple[str, ...]] = ("M-06",)
#: The family module each id dispatches to (lazy import inside `fit_predict`).
_FAMILY_MODULE: Final[Mapping[str, str]] = {
    "M-01": "persistence",
    "M-02": "persistence",
    "M-03": "climatology",
    "M-04": "ridge",
    "M-05": "random_forest",
    "M-06": "lstm",
}
#: The prediction frame's columns (`component-methods.md`: station, interval_start_utc, y_hat).
PREDICTION_COLUMNS: Final[tuple[str, ...]] = ("station", "interval_start_utc", "y_hat")
#: D-17's target-row column identities (`src/data/prepared.py`), read here, never redefined.
TARGET_TIMESTAMP_COLUMN: Final[str] = "interval_start_utc"
TARGET_STATION_COLUMN: Final[str] = "station_id"
TARGET_VALUE_COLUMN: Final[str] = "vtec_tecu"
#: The three identity stamps every prediction carries (NFR-TDEF-01).
_IDENTITY_KEYS: Final[tuple[str, ...]] = ("phase_id", "source_id", "target_definition_id")
#: The three D-121 grid tracks, as `configs/experiment.yaml` keys them (identities).
GRID_TRACKS: Final[Mapping[str, str]] = {"ridge": "M-04", "random_forest": "M-05", "lstm": "M-06"}
#: The keys the seven Vision 8.6 fixed LSTM settings occupy in config (setting 5 -- patience
#: monitored on validation RMSE -- occupies two keys). Key IDENTITIES only; the values live
#: in `configs/experiment.yaml` and are never compared against a literal here.
LSTM_FIXED_SETTING_KEYS: Final[tuple[str, ...]] = (
    "dropout",
    "optimizer",
    "loss",
    "max_epochs",
    "early_stopping_patience",
    "early_stopping_monitor",
    "min_improvement_tecu",
    "checkpoint_policy",
)
#: The one checkpoint policy this unit implements (R-94): an identity token, not a value.
BEST_CHECKPOINT_POLICY: Final[str] = "best_checkpoint"
#: TE 7.2's five named ablations -- identities (R-97: five named, four reachable in Phase 1).
ABLATION_IDS: Final[tuple[str, ...]] = (
    "ABL-NODOY",
    "ABL-DIFF",
    "ABL-NOSW",
    "ABL-HIST48",
    "ABL-ZENITH",
)
_REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[2]
_SEQUENCE_STEP_SUFFIX: Final[re.Pattern[str]] = re.compile(r"_t-(\d+)$")
_LAG_FIELD: Final[re.Pattern[str]] = re.compile(r"^vtec_lag_(\d+)h$")
_UTC: Final = dt.UTC


# --- the boundary shape -------------------------------------------------------------------


@dataclass(frozen=True)
class Prediction:
    """The approved eight-field shape (`component-methods.md`; `domain-entities.md` section 2).

    `frame` carries `station`, `interval_start_utc`, `y_hat`. `partition_id` and
    `transform_id` were added under ADR-11 so `07`, which receives predictions rather than
    bundles, can tell which partition's transform produced the numbers it scores. Quoted, not
    amended: this unit owes 0 amendments to the boundary contract.
    """

    model_id: str
    seed: int | None
    frame: Any
    target_definition_id: str
    phase_id: str
    source_id: str
    partition_id: str
    transform_id: str


def _is_tbd(value: object) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == TBD_SENTINEL)


def _as_utc(value: object, *, resource: str) -> dt.datetime:
    if isinstance(value, dt.datetime):
        stamp = value
    elif isinstance(value, str):
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            stamp = dt.datetime.fromisoformat(text)
        except ValueError as exc:
            raise IntegrityError(resource, f"timestamp {value!r} is not ISO-8601") from exc
    else:
        to_py = getattr(value, "to_pydatetime", None)
        if not callable(to_py):
            raise IntegrityError(resource, f"timestamp {value!r} is unrecognised")
        stamp = to_py()
    if stamp.tzinfo is None:
        return stamp.replace(tzinfo=_UTC)
    return stamp.astimezone(_UTC)


def pinned_requirement(package: str, requirements_path: Path | None = None) -> str | None:
    """The non-comment `<package>==<version>` line of `requirements.txt`, or `None`.

    The single governed pin surface (TE 13.1). A pin that exists only inside a comment --
    the TensorFlow `TBD -- freeze gate` entry -- is NOT a pin, so comments are skipped.
    """
    path = Path(requirements_path) if requirements_path else _REPO_ROOT / "requirements.txt"
    if not path.is_file():
        raise IntegrityError(path, "requirements.txt is required to resolve a governed pin")
    pattern = re.compile(rf"^{re.escape(package)}==\S+$", re.IGNORECASE)
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if pattern.match(line):
            return line
    return None


# --- R-99: the horizon is a parameter ---------------------------------------------------


def read_horizons(snapshot: ConfigSnapshot) -> tuple[int, ...]:
    """`experiment.horizons` -- the default run list (TE 2.1: `[1]`, with 24 implemented).

    Raises
    ------
    IntegrityError
        absent, `TBD -- freeze gate`, empty, or carrying a non-positive-integer entry. The
        list's VALUE is TE 2.1's frozen text and its config transcription is its owner's; this
        module never defaults it (TE 18.3).
    """
    value = snapshot.experiment.get("horizons")
    if _is_tbd(value):
        raise IntegrityError(
            "configs/experiment.yaml: horizons",
            "absent or unresolved (TBD — freeze gate); TE 2.1 fixes `horizons: [1]` with 24 "
            "implemented and testable but outside the default run list, and the horizon reaches "
            "every model as a parameter from this field (R-99) — never a literal in source",
        )
    if not isinstance(value, list | tuple) or not value:
        raise IntegrityError(
            "configs/experiment.yaml: horizons", "must be a non-empty list of positive integers"
        )
    out: list[int] = []
    for item in value:
        if isinstance(item, bool) or not isinstance(item, int) or item <= 0:
            raise IntegrityError(
                "configs/experiment.yaml: horizons", f"entry {item!r} is not a positive integer"
            )
        out.append(item)
    return tuple(out)


def resolve_horizon(snapshot: ConfigSnapshot, horizon_hours: int | None) -> int:
    """The horizon a run trains for: the caller's, or the single default-list entry.

    A default run list carrying more than one horizon with no explicit choice is refused --
    picking the first would be a default made by convenience.
    """
    horizons = read_horizons(snapshot)
    if horizon_hours is None:
        if len(horizons) != 1:
            raise IntegrityError(
                "configs/experiment.yaml: horizons",
                f"carries {len(horizons)} entries {list(horizons)} and no horizon was named; "
                f"the run must name which one it trains for",
            )
        return horizons[0]
    if isinstance(horizon_hours, bool) or not isinstance(horizon_hours, int) or horizon_hours <= 0:
        raise IntegrityError("horizon_hours", f"{horizon_hours!r} is not a positive integer")
    return horizon_hours


def eligible_feature_columns(bundle: FeatureBundle, *, horizon_hours: int) -> tuple[str, ...]:
    """The bundle columns a model may read at the given horizon.

    A lagged target column `vtec_lag_<k>h` or a flattened sequence step `<field>_t-<k>` with
    `k < horizon_hours` is not yet observed at the forecast origin and is excluded. The rule
    is arithmetic over the column's own declared step -- no literal horizon appears (R-99).
    """
    out: list[str] = []
    for column, stamp in bundle.provenance.items():
        step: int | None = None
        field = str(stamp.get("dictionary_field", column))
        lag_match = _LAG_FIELD.match(field)
        seq_match = _SEQUENCE_STEP_SUFFIX.search(column)
        if lag_match:
            step = int(lag_match.group(1))
        elif seq_match:
            step = int(seq_match.group(1))
        if step is not None and step < horizon_hours:
            continue
        out.append(column)
    if not out:
        raise IntegrityError(
            f"bundle {bundle.spec.partition_id}/{bundle.spec.role}",
            f"no feature column is observable at horizon {horizon_hours} h",
        )
    return tuple(out)


# --- the target series and labels ----------------------------------------------------------


def target_series(target: Any) -> dict[tuple[str, dt.datetime], float]:
    """`(station, interval_start_utc) -> vtec_tecu` from the D-17 target frame.

    Gaps stored as NaN/None (D-5) are kept OUT of the mapping so a lookup miss is the
    honest answer. Raises when a row lacks the three D-17 columns.
    """
    out: dict[tuple[str, dt.datetime], float] = {}
    for index, row in enumerate(records_of(target)):
        for column in (TARGET_TIMESTAMP_COLUMN, TARGET_STATION_COLUMN, TARGET_VALUE_COLUMN):
            if column not in row:
                raise IntegrityError(
                    f"target row {index}",
                    f"carries no {column!r}; the D-17 target frame is the label source",
                )
        raw = row[TARGET_VALUE_COLUMN]
        if raw is None or (isinstance(raw, str) and not raw.strip()):
            continue
        value = float(raw)
        if math.isnan(value):
            continue
        key = (
            str(row[TARGET_STATION_COLUMN]),
            _as_utc(row[TARGET_TIMESTAMP_COLUMN], resource=f"target row {index}"),
        )
        out[key] = value
    return out


def feature_rows(bundle: FeatureBundle, columns: Sequence[str]) -> list[list[float]]:
    """The bundle's rows restricted to `columns`, as floats; a NaN or missing value raises
    (gaps are excluded and counted upstream, never fed to a fit)."""
    out: list[list[float]] = []
    for index, row in enumerate(records_of(bundle.matrix)):
        values: list[float] = []
        for column in columns:
            if column not in row or row[column] is None:
                raise IntegrityError(
                    f"bundle {bundle.spec.partition_id}/{bundle.spec.role} row {index}",
                    f"lacks feature column {column!r}",
                )
            value = float(row[column])
            if math.isnan(value):
                raise IntegrityError(
                    f"bundle {bundle.spec.partition_id}/{bundle.spec.role} row {index}",
                    f"carries NaN in {column!r}; gaps are excluded upstream, never modelled over",
                )
            values.append(value)
        out.append(values)
    return out


def bundle_index(bundle: FeatureBundle) -> list[tuple[str, dt.datetime]]:
    """The ORDERED (`station`, `interval_start_utc`) keys of a bundle's rows."""
    keys: list[tuple[str, dt.datetime]] = []
    for index, row in enumerate(records_of(bundle.matrix)):
        if TARGET_TIMESTAMP_COLUMN not in row or TARGET_STATION_COLUMN not in row:
            raise IntegrityError(
                f"bundle row {index}",
                f"carries no {TARGET_TIMESTAMP_COLUMN!r}/{TARGET_STATION_COLUMN!r}",
            )
        keys.append(
            (
                str(row[TARGET_STATION_COLUMN]),
                _as_utc(row[TARGET_TIMESTAMP_COLUMN], resource=f"bundle row {index}"),
            )
        )
    return keys


def labels_for(
    bundle: FeatureBundle, series: Mapping[tuple[str, dt.datetime], float]
) -> tuple[list[tuple[str, dt.datetime]], list[float | None], int]:
    """The label `y(t)` for every bundle row, looked up on `(station, t)`.

    The horizon governs which INPUT columns are observable (`eligible_feature_columns`); the
    label is the target value at the row's own hour. Returns the keys, the labels (`None`
    where the target has a gap) and the count of gaps -- a completeness shortfall recorded
    as a number, never console text (team.md two-tier posture).
    """
    keys = bundle_index(bundle)
    labels: list[float | None] = []
    missing = 0
    for key in keys:
        value = series.get(key)
        if value is None:
            missing += 1
        labels.append(value)
    return keys, labels, missing


def new_prediction(
    model_id: str,
    *,
    seed: int | None,
    rows: Sequence[Mapping[str, Any]],
    bundle: FeatureBundle,
    partition: Partition,
    attrs: Mapping[str, Any] | None = None,
) -> Prediction:
    """Assemble a `Prediction` whose stamps are COPIED from the bundle it was scored on."""
    for key in _IDENTITY_KEYS:
        if not str(bundle.identity.get(key, "") or "").strip():
            raise IntegrityError(
                f"bundle {bundle.spec.partition_id}/{bundle.spec.role}",
                f"identity stamp {key!r} is missing; every prediction carries phase_id, "
                f"source_id and target_definition_id (NFR-TDEF-01)",
            )
    if bundle.transform_id is None:
        raise LeakageError(
            f"bundle {bundle.spec.partition_id}/{bundle.spec.role}/untransformed",
            "a prediction cannot be stamped with transform_id None (ADR-11)",
        )
    ordered = [
        {
            "station": str(row["station"]),
            "interval_start_utc": _as_utc(row["interval_start_utc"], resource="prediction row")
            .isoformat(),
            "y_hat": row["y_hat"],
        }
        for row in rows
    ]
    frame = frame_from_records(
        ordered,
        columns=PREDICTION_COLUMNS,
        attrs={
            **dict(attrs or {}),
            "model_id": model_id,
            "partition_id": partition.partition_id,
            "transform_id": bundle.transform_id,
        },
    )
    return Prediction(
        model_id=model_id,
        seed=seed,
        frame=frame,
        target_definition_id=str(bundle.identity["target_definition_id"]),
        phase_id=str(bundle.identity["phase_id"]),
        source_id=str(bundle.identity["source_id"]),
        partition_id=partition.partition_id,
        transform_id=bundle.transform_id,
    )


def prediction_index(prediction: Prediction) -> list[tuple[str, str]]:
    """The ORDERED (`station`, `interval_start_utc`) index of a prediction frame (R-92)."""
    out: list[tuple[str, str]] = []
    for index, row in enumerate(records_of(prediction.frame)):
        for column in ("station", "interval_start_utc"):
            if column not in row:
                raise AlignmentError(
                    f"prediction {prediction.model_id} row {index}",
                    f"carries no {column!r}; the alignment key is (station, interval_start_utc)",
                )
        out.append(
            (
                str(row["station"]),
                _as_utc(row["interval_start_utc"], resource="prediction row").isoformat(),
            )
        )
    return out


# --- W-1 / R-90: the stamp match before every scoring path ---------------------------------


def expected_transform_id(partition: Partition) -> str:
    """The transform that is `partition`'s OWN: `T-<id>`, and for the locked month the
    refit's (`REFIT` -> `DEC` under role "score" is the one enumerated apply, R-74)."""
    if partition.partition_id == LOCKED_ID:
        return transform_id_for(REFIT_ID)
    return transform_id_for(partition.partition_id)


def assert_stamp_match(
    bundle: FeatureBundle,
    partition_being_scored: Partition,
    *,
    own_transform_id: str | None = None,
) -> None:
    """R-90: a frame whose spec is not `(partition k, role "score")` never reaches partition
    k's scoring, and the transform must be k's own.

    Raises
    ------
    PartitionError
        `bundle.spec.partition_id != partition_being_scored.partition_id`; or
        `bundle.spec.role != "score"` -- declared-identity / declared-role disagreements.
    LeakageError
        `bundle.transform_id is None`, or not equal to the scored partition's own transform
        -- a disagreement that implies information flow (R-92's discriminating rule).
    """
    spec = bundle.spec
    scored = partition_being_scored.partition_id
    if spec.partition_id != scored:
        raise PartitionError(
            f"bundle {spec.partition_id}/{spec.role} reaching {scored}'s score path",
            f"spec.partition_id {spec.partition_id!r} is not the partition being scored "
            f"{scored!r}; a declared-identity disagreement (R-90 check 1; R-92)",
        )
    if spec.role != "score":
        raise PartitionError(
            f"bundle {spec.partition_id}/{spec.role} reaching {scored}'s score path",
            f"spec.role {spec.role!r} is not 'score'; a training frame is not a scored frame "
            f"(R-90 check 2; R-92) — in-sample numbers, not a result",
        )
    if bundle.transform_id is None:
        raise LeakageError(
            f"bundle {spec.partition_id}/{spec.role}/untransformed reaching {scored}'s score path",
            "transform_id is None; the untransformed fitting bundle is live in the process and "
            "consuming it for scoring is the leak R-74 element 4 closes (R-90 check 3)",
        )
    own = own_transform_id or expected_transform_id(partition_being_scored)
    if bundle.transform_id != own:
        raise LeakageError(
            f"bundle {spec.partition_id}/{spec.role}/{bundle.transform_id} reaching {scored}'s "
            f"score path",
            f"transform_id {bundle.transform_id!r} is not {scored}'s own {own!r}; a transform "
            f"fitted elsewhere has touched these rows — correctly fitted, wrongly applied "
            f"(R-90 check 3; R-74 element 4)",
        )


# --- W-2: fit and predict over six families -------------------------------------------------


def _assert_fit_bundle_for_partition(bundle: FeatureBundle, partition: Partition) -> None:
    """The bundle a model is fitted on belongs to `partition`: same id, or the refit's
    train bundle under the locked partition (the G-06 apply, mirroring R-74's exception)."""
    spec = bundle.spec
    if spec.partition_id == partition.partition_id:
        return
    if spec.partition_id == REFIT_ID and partition.partition_id == LOCKED_ID:
        return
    raise PartitionError(
        f"bundle {spec.partition_id}/{spec.role} fitted for partition {partition.partition_id}",
        f"spec.partition_id {spec.partition_id!r} disagrees with the partition "
        f"{partition.partition_id!r}; a declared-identity disagreement (R-92) — the one "
        f"permitted pair is REFIT's train bundle under DEC",
    )


def fit_predict(
    model_id: str,
    *,
    bundle: FeatureBundle,
    partition: Partition,
    snapshot: ConfigSnapshot,
    target: Any = None,
    score_bundle: FeatureBundle | None = None,
    seed: int | None = None,
    params: Mapping[str, Any] | None = None,
    horizon_hours: int | None = None,
) -> Prediction:
    """The approved boundary call (`component-methods.md`), with ADDITIVE keyword-only inputs.

    `bundle` is the bundle the family is fitted on (role `train` for M-03..M-06);
    `score_bundle` is the bundle predicted on (default: `bundle` itself, an in-sample
    prediction); `target` is the D-17 target frame supplying labels and the raw-TECU series
    the two persistence families read (the bundle's lag columns are standardised under
    `transform_id` and no inverse exists, D-27); `seed` is required for M-06 and refused for
    every other family; `params` names the grid point for M-04..M-06 and is asserted to lie
    in the config grid (R-96); `horizon_hours` defaults to the single default-list entry.

    Raises
    ------
    IntegrityError
        a `model_id` outside the closed set M-01..M-06 (FR-P1-05-1, R-102); a missing target.
    LeakageError
        `bundle.transform_id is None` (the approved raise); a fitted family offered a
        score-role bundle to fit on; `score_bundle.transform_id != bundle.transform_id`.
    PartitionError
        the fit bundle does not belong to `partition`; the score bundle names another.
    SeedError
        a seed on an unseeded family, or no seed on M-06.
    """
    if model_id not in MODEL_IDS:
        raise IntegrityError(
            f"model_id {model_id!r}",
            f"is outside the closed model set {list(MODEL_IDS)} (FR-P1-05-1; R-102); the two "
            f"removed architectures of D-120 are absent by design",
        )
    assert_consumable(bundle)  # LeakageError: transform_id is None
    _assert_fit_bundle_for_partition(bundle, partition)
    scored = score_bundle if score_bundle is not None else bundle
    if scored is not bundle:
        assert_consumable(scored)
        if scored.spec.partition_id != partition.partition_id:
            raise PartitionError(
                f"score bundle {scored.spec.partition_id}/{scored.spec.role}",
                f"names partition {scored.spec.partition_id!r}, not {partition.partition_id!r}",
            )
        if scored.transform_id != bundle.transform_id:
            raise LeakageError(
                f"score bundle {scored.spec.partition_id}/{scored.spec.role}/"
                f"{scored.transform_id}",
                f"transform_id disagrees with the fit bundle's {bundle.transform_id!r}; the rows "
                f"scored must have been transformed by the same fitted state (R-74 element 4)",
            )
    if model_id in SEEDED_MODEL_IDS:
        if seed is None or isinstance(seed, bool) or not isinstance(seed, int):
            raise SeedError(
                f"fit_predict({model_id})",
                "M-06 is seeded and each seed is its own registry run (TE 13.5); the seed comes "
                "from configs/seeds.yaml through the caller, never defaulted here",
            )
    elif seed is not None:
        raise SeedError(
            f"fit_predict({model_id})",
            f"{model_id} is an unseeded family; Prediction.seed is None for M-01..M-05 and a "
            f"seed here would misrepresent the run (domain-entities section 1)",
        )
    if target is None:
        raise IntegrityError(
            f"fit_predict({model_id})",
            "the D-17 target frame is required: labels are looked up on (station, t), and "
            "M-01/M-02 read the raw-TECU series because the bundle's lag columns are standardised "
            "under transform_id and no inverse exists (D-27)",
        )
    horizon = resolve_horizon(snapshot, horizon_hours)
    if model_id in ("M-03", "M-04", "M-05", "M-06") and bundle.spec.role != "train":
        raise LeakageError(
            f"bundle {bundle.spec.partition_id}/{bundle.spec.role}",
            f"{model_id} is fitted on a train-role bundle only; fitting on a score-role bundle "
            f"is fitting on the validation month (NFR-LEAK-01)",
        )
    module_name = _FAMILY_MODULE[model_id]
    family = __import__(f"src.models.{module_name}", fromlist=["fit_predict_rows"])
    return family.fit_predict_rows(
        model_id,
        bundle=bundle,
        score_bundle=scored,
        partition=partition,
        snapshot=snapshot,
        target=target,
        seed=seed,
        params=params,
        horizon_hours=horizon,
    )


# --- W-3 / R-91, R-92, R-93: the confirmatory prediction ---------------------------------------


def three_seed_mean(
    predictions: Sequence[Prediction],
    *,
    expected_seeds: frozenset[int],
) -> Prediction:
    """BLK-03's contract, all four limbs (`domain-entities.md` section 3; approved 2026-09-06).

    `expected_seeds` is read from `ConfigSnapshot.seeds` at the call site. The frozen set
    is NEVER inlined here, and the check is never weakened to pairwise distinctness.

    Raises
    ------
    SeedError
        fewer or more than three; the seed set not EXACTLY `expected_seeds`; any input with
        `seed is None`; any input whose `model_id` is not "M-06"; an `expected_seeds` that is
        not a set of exactly three integers.
    AlignmentError
        the frames do not share an identical (`station`, `interval_start_utc`) index, as a
        set AND in order.
    PartitionError
        `partition_id` differs across the inputs, or names a training partition.
    LeakageError
        `transform_id` differs across the inputs, or is `None` on any of them.
    """
    if (
        not isinstance(expected_seeds, frozenset | set)
        or len(expected_seeds) != 3
        or any(isinstance(s, bool) or not isinstance(s, int) for s in expected_seeds)
    ):
        raise SeedError(
            "expected_seeds",
            f"must be the configured set of exactly three integer seeds (D-122, "
            f"configs/seeds.yaml `final`), got {expected_seeds!r}",
        )
    inputs = list(predictions)
    if len(inputs) != 3:
        raise SeedError(
            "three_seed_mean",
            f"received {len(inputs)} prediction(s); the confirmatory prediction is the "
            f"element-wise mean of EXACTLY three seeds — a single-seed or best-of-three "
            f"substitute is refused (R-91; NFR-DET-01)",
        )
    for prediction in inputs:
        if prediction.model_id != "M-06":
            raise SeedError(
                f"prediction {prediction.model_id}",
                "only M-06 is seeded; the three-seed mean applies to M-06 alone and an unseeded "
                "family here is a SeedError, not a no-op (domain-entities section 1)",
            )
        if prediction.seed is None or isinstance(prediction.seed, bool):
            raise SeedError(
                "prediction M-06",
                "an input with seed None is not a single-seed run and cannot enter the mean",
            )
    seeds = {p.seed for p in inputs}
    if seeds != set(expected_seeds):
        raise SeedError(
            "three_seed_mean",
            f"seed set {sorted(seeds)} is not exactly the configured set "
            f"{sorted(expected_seeds)}; the values are asserted, not merely counted or checked "
            f"for distinctness (R-91, R-93)",
        )
    partition_ids = {p.partition_id for p in inputs}
    if len(partition_ids) != 1:
        raise PartitionError(
            "three_seed_mean",
            f"inputs disagree on partition_id {sorted(partition_ids)}; a declared-identity "
            f"disagreement (R-92)",
        )
    partition_id = partition_ids.pop()
    transform_ids = {p.transform_id for p in inputs}
    if None in transform_ids or len(transform_ids) != 1:
        raise LeakageError(
            "three_seed_mean",
            f"inputs disagree on transform_id or carry None ({sorted(map(str, transform_ids))}); "
            f"a disagreement that implies information flow (R-92)",
        )
    for key in _IDENTITY_KEYS:
        values = {getattr(p, key) for p in inputs}
        if len(values) != 1:
            raise PartitionError(
                "three_seed_mean", f"inputs disagree on {key} {sorted(values)} (R-92)"
            )
    roles = {str(frame_attrs(p.frame).get("role", "")) for p in inputs}
    if "train" in roles:
        raise PartitionError(
            "three_seed_mean",
            "a confirmatory prediction over training rows is not a result (limb 3): the input "
            "frames were scored on a train-role bundle",
        )
    indices = [prediction_index(p) for p in inputs]
    first = indices[0]
    for prediction, index in zip(inputs, indices, strict=True):
        if set(index) != set(first):
            raise AlignmentError(
                f"prediction M-06 seed {prediction.seed}",
                "row set differs from the other inputs on (station, interval_start_utc); "
                "averaging misaligned predictions silently is the failure this check exists for",
            )
        if index != first:
            raise AlignmentError(
                f"prediction M-06 seed {prediction.seed}",
                "identical row set in a different ORDER; element-wise averaging would pair the "
                "wrong rows (R-92: compared as a set AND in order)",
            )
    if len(set(first)) != len(first):
        raise AlignmentError("three_seed_mean", "duplicate (station, interval_start_utc) rows")
    y_hats = [[row["y_hat"] for row in records_of(p.frame)] for p in inputs]
    rows: list[dict[str, Any]] = []
    for position, (station, stamp) in enumerate(first):
        values = [column[position] for column in y_hats]
        if any(v is None for v in values):
            mean: float | None = None
        else:
            floats = [float(v) for v in values]
            mean = None if any(math.isnan(f) for f in floats) else sum(floats) / len(floats)
        rows.append({"station": station, "interval_start_utc": stamp, "y_hat": mean})
    template = inputs[0]
    frame = frame_from_records(
        rows,
        columns=PREDICTION_COLUMNS,
        attrs={
            **{k: v for k, v in frame_attrs(template.frame).items() if k != "seed"},
            "model_id": "M-06",
            "confirmatory": True,
            "seeds_averaged": sorted(seeds),
        },
    )
    return Prediction(
        model_id="M-06",
        seed=None,
        frame=frame,
        target_definition_id=template.target_definition_id,
        phase_id=template.phase_id,
        source_id=template.source_id,
        partition_id=partition_id,
        transform_id=template.transform_id,
    )


# --- W-5 / R-95 / SD-M-01: tuning ---------------------------------------------------------


@dataclass(frozen=True)
class TuningRecord:
    """The seven approved fields (`domain-entities.md` section 5) PLUS the three attestation
    fields SD-M-01 adds (Q1 = C at nfr-design; the field group is the owed entity amendment,
    carried here as this pass's implementation of that design)."""

    run_id: str
    partitions_read: tuple[str, ...]
    criterion_declared_at: str
    criterion_hash: str
    criterion_used_hash: str
    run_at: str
    audit_access_since_declaration: bool
    attested_by: str
    attested_at_utc: str
    attests_criterion_hash: str


def criterion_hash(criterion: Mapping[str, Any]) -> str:
    """SHA-256 over the canonical JSON of a selection criterion (sorted keys, no whitespace)."""
    canonical = json.dumps(dict(criterion), sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def record_tuning(
    *,
    run_id: str,
    partitions_read: Sequence[str],
    criterion_declared: Mapping[str, Any],
    criterion_declared_at: str,
    criterion_used: Mapping[str, Any],
    run_at: str,
    attested_by: str,
    attested_at_utc: str,
    attests_criterion_hash: str,
    audit_access_since_declaration: bool = False,
) -> TuningRecord:
    """R-95's two runnable mechanisms and SD-M-01's UNCONDITIONAL attestation.

    Raises
    ------
    LeakageError
        a December partition in `partitions_read` (December must not inform selection;
        Vision 8.3); `criterion_hash != criterion_used_hash` (a criterion changed after
        December was seen); `run_at` not after `criterion_declared_at`; a missing attestation;
        an attestation not bound to THIS run's criterion hash.
    PartitionError
        a `partitions_read` entry outside the closed six-value space.
    """
    read = tuple(str(p) for p in partitions_read)
    if not read:
        raise LeakageError(f"tuning run {run_id}", "partitions_read is empty; a tuning run reads")
    for pid in read:
        if pid not in PARTITION_IDS:
            raise PartitionError(
                f"tuning run {run_id}",
                f"partitions_read names {pid!r}, outside {list(PARTITION_IDS)}",
            )
        if pid == LOCKED_ID:
            raise LeakageError(
                f"tuning run {run_id}",
                f"partitions_read includes the locked partition {LOCKED_ID!r}; model selection, "
                f"feature selection, thresholds and hyperparameters use January–November only "
                f"(R-95 mechanism 1; Vision 8.3; project.md Forbidden)",
            )
    declared_hash = criterion_hash(criterion_declared)
    used_hash = criterion_hash(criterion_used)
    if declared_hash != used_hash:
        raise LeakageError(
            f"tuning run {run_id}",
            f"criterion_used_hash {used_hash[:12]}… differs from criterion_hash "
            f"{declared_hash[:12]}…; the criterion declared before tuning must equal the one "
            f"used (R-95 mechanism 2; R-101)",
        )
    declared_at = _as_utc(criterion_declared_at, resource=f"tuning run {run_id} declared_at")
    ran_at = _as_utc(run_at, resource=f"tuning run {run_id} run_at")
    if not declared_at < ran_at:
        raise LeakageError(
            f"tuning run {run_id}",
            f"criterion_declared_at {declared_at.isoformat()} does not PRECEDE run_at "
            f"{ran_at.isoformat()}; the criterion is declared before tuning begins",
        )
    if not str(attested_by).strip() or not str(attested_at_utc).strip():
        raise LeakageError(
            f"tuning run {run_id}",
            "no attestation: every tuning run carries a dated, named attestation that no "
            "December figure informed the criterion (SD-M-01, unconditional, Q1 = C)",
        )
    _as_utc(attested_at_utc, resource=f"tuning run {run_id} attested_at_utc")
    if attests_criterion_hash != declared_hash:
        raise LeakageError(
            f"tuning run {run_id}",
            f"attests_criterion_hash {str(attests_criterion_hash)[:12]}… is not this run's "
            f"criterion_hash {declared_hash[:12]}…; a re-declared criterion invalidates the "
            f"attestation and a fresh one is required (SD-M-01)",
        )
    return TuningRecord(
        run_id=run_id,
        partitions_read=read,
        criterion_declared_at=declared_at.isoformat(),
        criterion_hash=declared_hash,
        criterion_used_hash=used_hash,
        run_at=ran_at.isoformat(),
        audit_access_since_declaration=bool(audit_access_since_declaration),
        attested_by=str(attested_by),
        attested_at_utc=_as_utc(attested_at_utc, resource="attested_at_utc").isoformat(),
        attests_criterion_hash=attests_criterion_hash,
    )


# --- W-6 / R-96: the grid freeze ----------------------------------------------------------


def read_grids(snapshot: ConfigSnapshot) -> Mapping[str, Mapping[str, Any]]:
    """`experiment.grids`: the ONE copy of D-121's grids. Refuses absent/TBD naming the field."""
    block = snapshot.experiment.get("grids")
    if _is_tbd(block):
        raise IntegrityError(
            "configs/experiment.yaml: grids",
            "absent or unresolved (TBD — freeze gate); the grids are D-121's and reach the code "
            "only from configuration (R-96; TC-03e) — never defaulted (TE 18.3)",
        )
    if not isinstance(block, Mapping):
        raise IntegrityError("configs/experiment.yaml: grids", "must be a mapping of tracks")
    for track in GRID_TRACKS:
        if track not in block or not isinstance(block[track], Mapping):
            raise IntegrityError(
                f"configs/experiment.yaml: grids.{track}", "track is absent or not a mapping"
            )
    return {track: block[track] for track in GRID_TRACKS}


def enumerate_grid(snapshot: ConfigSnapshot, track: str) -> tuple[dict[str, Any], ...]:
    """Every grid point of a track: the Cartesian product of `axes`, merged with `fixed`."""
    if track not in GRID_TRACKS:
        raise IntegrityError(f"grid track {track!r}", f"is not one of {list(GRID_TRACKS)}")
    spec = read_grids(snapshot)[track]
    axes = spec.get("axes")
    if not isinstance(axes, Mapping) or not axes:
        raise IntegrityError(f"configs/experiment.yaml: grids.{track}.axes", "must be a mapping")
    names = list(axes)
    values: list[list[Any]] = []
    for name in names:
        axis = axes[name]
        if _is_tbd(axis):
            raise IntegrityError(
                f"configs/experiment.yaml: grids.{track}.axes.{name}",
                "unresolved (TBD — freeze gate); every grid axis is D-121's transcription",
            )
        if not isinstance(axis, list | tuple) or not axis:
            raise IntegrityError(
                f"configs/experiment.yaml: grids.{track}.axes.{name}", "must be a non-empty list"
            )
        values.append(list(axis))
    fixed = spec.get("fixed", {}) or {}
    if not isinstance(fixed, Mapping):
        raise IntegrityError(f"configs/experiment.yaml: grids.{track}.fixed", "must be a mapping")
    points: list[dict[str, Any]] = []
    for combo in itertools.product(*values):
        point = dict(zip(names, combo, strict=True))
        point.update(dict(fixed))
        points.append(point)
    return tuple(points)


def assert_grid_content(snapshot: ConfigSnapshot) -> dict[str, int]:
    """R-96's content check: for every track the enumerated product equals D-121's declared
    `combinations`, and the seven LSTM settings are present. Returns the counts, derived."""
    counts: dict[str, int] = {}
    grids = read_grids(snapshot)
    for track, model_id in GRID_TRACKS.items():
        declared = grids[track].get("combinations")
        if _is_tbd(declared) or isinstance(declared, bool) or not isinstance(declared, int):
            raise IntegrityError(
                f"configs/experiment.yaml: grids.{track}.combinations",
                "D-121's combination count is absent or not an integer",
            )
        if str(grids[track].get("model_id", "")) != model_id:
            raise IntegrityError(
                f"configs/experiment.yaml: grids.{track}.model_id",
                f"must be {model_id!r} (the track's family identity)",
            )
        enumerated = len(enumerate_grid(snapshot, track))
        if enumerated != declared:
            raise IntegrityError(
                f"configs/experiment.yaml: grids.{track}",
                f"enumerates {enumerated} combinations but declares {declared} (D-121); a grid "
                f"that is immutable but wrong is immutably wrong — content is asserted, not "
                f"only immutability (R-96)",
            )
        counts[track] = enumerated
    read_lstm_fixed_settings(snapshot)
    return counts


def assert_in_grid(snapshot: ConfigSnapshot, track: str, params: Mapping[str, Any]) -> None:
    """A grid point must be a member of the config grid: a value outside it refuses (R-96)."""
    points = enumerate_grid(snapshot, track)
    candidate = dict(params)
    for point in points:
        if all(point.get(k) == v for k, v in candidate.items()) and set(candidate) == set(point):
            return
    raise IntegrityError(
        f"grid point {candidate!r} for track {track}",
        f"is not a member of configs/experiment.yaml grids.{track} ({len(points)} points); "
        f"grids are exact and no range changes after December is seen (R-96; Vision 8.6)",
    )


def grid_hash(snapshot: ConfigSnapshot) -> str:
    """The frozen object: SHA-256 over the canonical JSON of `experiment.grids` (R-96)."""
    block = read_grids(snapshot)
    canonical = json.dumps(
        {t: dict(block[t]) for t in GRID_TRACKS},
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def assert_grid_unchanged(snapshot: ConfigSnapshot, frozen_hash: str) -> None:
    """The post-G-05 diff-empty check is the SAME mechanism: current hash == frozen hash."""
    current = grid_hash(snapshot)
    if current != frozen_hash:
        raise IntegrityError(
            "configs/experiment.yaml: grids",
            f"hash {current[:12]}… differs from the hash frozen before G-05 "
            f"{frozen_hash[:12]}…; no grid range changes after December is seen (R-96; "
            f"project.md Forbidden)",
        )


def read_lstm_fixed_settings(snapshot: ConfigSnapshot) -> Mapping[str, Any]:
    """Vision 8.6's seven fixed LSTM settings, asserted PRESENT and well-typed from config.

    The values are never compared against a literal here: the config is the one copy. The
    checkpoint policy is asserted to be the one identity this unit implements (R-94).
    """
    models = snapshot.experiment.get("models")
    if _is_tbd(models) or not isinstance(models, Mapping):
        raise IntegrityError(
            "configs/experiment.yaml: models",
            "absent or unresolved (TBD — freeze gate); Vision 8.6's seven fixed LSTM settings "
            "reach the code only from configuration (R-96)",
        )
    block = models.get("lstm_fixed_settings")
    if _is_tbd(block) or not isinstance(block, Mapping):
        raise IntegrityError(
            "configs/experiment.yaml: models.lstm_fixed_settings",
            "absent or unresolved; the seven settings are D-121's 'fixed training settings'",
        )
    missing = [key for key in LSTM_FIXED_SETTING_KEYS if _is_tbd(block.get(key))]
    if missing:
        raise IntegrityError(
            "configs/experiment.yaml: models.lstm_fixed_settings",
            f"setting key(s) absent or TBD: {missing}; all seven settings are asserted "
            f"individually",
        )
    numeric = ("dropout", "max_epochs", "early_stopping_patience", "min_improvement_tecu")
    for key in numeric:
        value = block[key]
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise IntegrityError(
                f"configs/experiment.yaml: models.lstm_fixed_settings.{key}",
                f"{value!r} is not numeric",
            )
    for key in ("optimizer", "loss", "early_stopping_monitor", "checkpoint_policy"):
        if not isinstance(block[key], str) or not block[key].strip():
            raise IntegrityError(
                f"configs/experiment.yaml: models.lstm_fixed_settings.{key}", "must be a string"
            )
    if block["checkpoint_policy"] != BEST_CHECKPOINT_POLICY:
        raise IntegrityError(
            "configs/experiment.yaml: models.lstm_fixed_settings.checkpoint_policy",
            f"{block['checkpoint_policy']!r} is not {BEST_CHECKPOINT_POLICY!r}; M-06 restores "
            f"its lowest-validation-RMSE checkpoint, never the last epoch (R-94; WS-15; TA-13)",
        )
    return {key: block[key] for key in LSTM_FIXED_SETTING_KEYS}


# --- R-101: selection on mean per-fold skill ----------------------------------------------


@dataclass(frozen=True)
class CandidateScore:
    """One grid point's per-fold SKILL scores (Vision 8.7: `1 - RMSE_model / RMSE_baseline`).

    `metric` names what the values are; anything but skill is refused at selection.
    `complexity` orders candidates for the simpler-within-tolerance rule (lower = simpler).
    """

    params: Mapping[str, Any]
    fold_skill: Mapping[str, float]
    complexity: float
    metric: str = "skill"


def mean_per_fold_skill(candidate: CandidateScore, *, fold_ids: Sequence[str]) -> float:
    """The unweighted mean over EXACTLY the fold ids (F1–F4); a missing fold refuses."""
    if candidate.metric != "skill":
        raise IntegrityError(
            f"candidate {dict(candidate.params)!r}",
            f"scores are {candidate.metric!r}, not skill; raw mean RMSE is not used — it lets "
            f"one fold dominate (R-101; Vision 8.7)",
        )
    wanted = list(fold_ids)
    missing = [f for f in wanted if f not in candidate.fold_skill]
    extra = [f for f in candidate.fold_skill if f not in wanted]
    if missing or extra:
        raise PartitionError(
            f"candidate {dict(candidate.params)!r}",
            f"fold_skill must cover exactly {wanted}; missing {missing}, unexpected {extra}",
        )
    values = [float(candidate.fold_skill[f]) for f in wanted]
    if any(math.isnan(v) for v in values):
        raise IntegrityError(f"candidate {dict(candidate.params)!r}", "a fold skill is NaN")
    return sum(values) / len(values)


def _read_selection_block(snapshot: ConfigSnapshot) -> Mapping[str, Any]:
    models = snapshot.experiment.get("models")
    block = models.get("selection") if isinstance(models, Mapping) else None
    if _is_tbd(block) or not isinstance(block, Mapping):
        raise IntegrityError(
            "configs/experiment.yaml: models.selection",
            "absent or unresolved (TBD — freeze gate); Vision 8.7 / D-124's simplicity "
            "tolerance and declared baseline are configuration named BEFORE tuning begins, "
            "transcribed by their owner — stop and report, never default (TE 18.3; R-101)",
        )
    for key in ("simplicity_tolerance_fraction", "declared_baseline"):
        if _is_tbd(block.get(key)):
            raise IntegrityError(
                f"configs/experiment.yaml: models.selection.{key}", "absent or TBD — freeze gate"
            )
    tolerance = block["simplicity_tolerance_fraction"]
    if isinstance(tolerance, bool) or not isinstance(tolerance, int | float) or tolerance < 0:
        raise IntegrityError(
            "configs/experiment.yaml: models.selection.simplicity_tolerance_fraction",
            f"{tolerance!r} is not a non-negative number",
        )
    return block


def select_configuration(
    candidates: Sequence[CandidateScore],
    *,
    snapshot: ConfigSnapshot,
    fold_ids: Sequence[str],
    weights: Mapping[str, float] | None = None,
) -> CandidateScore:
    """R-101 / Vision 8.7: highest mean per-fold skill; within the configured tolerance the
    simpler configuration wins; row-count weighting is refused outright.

    Raises
    ------
    IntegrityError
        `weights` supplied (row-count weighting rewards easier data availability); a
        non-skill metric; no candidates; the selection block unresolved in config.
    """
    if weights is not None:
        raise IntegrityError(
            "select_configuration",
            "row-count weighting is not used (R-101; Vision 8.7); the mean is unweighted",
        )
    if not candidates:
        raise IntegrityError("select_configuration", "no candidates")
    block = _read_selection_block(snapshot)
    tolerance = float(block["simplicity_tolerance_fraction"])
    scored = [(mean_per_fold_skill(c, fold_ids=fold_ids), c) for c in candidates]
    best_skill = max(s for s, _ in scored)
    within = [c for s, c in scored if best_skill - s <= tolerance * abs(best_skill)]

    def _order(candidate: CandidateScore) -> tuple[float, str]:
        ordered = json.dumps(dict(candidate.params), sort_keys=True, default=str)
        return candidate.complexity, ordered

    return min(within, key=_order)


def assert_refit_unchanged(
    selected: Mapping[str, Any], refit: Mapping[str, Any]
) -> None:
    """R-101: the refit on January–November changes NO hyperparameter."""
    if dict(selected) != dict(refit):
        changed = sorted(
            k for k in set(selected) | set(refit) if selected.get(k) != refit.get(k)
        )
        raise IntegrityError(
            "refit hyperparameters",
            f"differ from the selected configuration on {changed}; a refit that re-tunes is a "
            f"second selection with no record (R-101; FR-P1-04-14)",
        )


# --- W-7 / R-97: the ablation registry ----------------------------------------------------


@dataclass(frozen=True)
class AblationEntry:
    """`domain-entities.md` section 8's entry, read from `experiment.yaml`."""

    ablation_id: str
    run_id: str | None
    registered_at: str | None
    phase1_reachable: bool
    phase_deferral: str | None
    inverse_before_metric: bool
    after_primary_freeze_only: bool
    configuration_change: str


def read_ablations(snapshot: ConfigSnapshot) -> tuple[AblationEntry, ...]:
    """Exactly the five TE 7.2 entries; a missing one FAILS rather than passing unnoticed."""
    block = snapshot.experiment.get("ablations")
    if _is_tbd(block) or not isinstance(block, Mapping):
        raise IntegrityError(
            "configs/experiment.yaml: ablations",
            "absent or unresolved (TBD — freeze gate); ablations are predeclared named runs "
            "registered in experiment.yaml (TE 7.2; R-97)",
        )
    entries = block.get("entries")
    if not isinstance(entries, Mapping):
        raise IntegrityError("configs/experiment.yaml: ablations.entries", "must be a mapping")
    declared = {str(k) for k in entries}
    expected = set(ABLATION_IDS)
    if declared != expected:
        raise IntegrityError(
            "configs/experiment.yaml: ablations.entries",
            f"must name exactly TE 7.2's five ablations {list(ABLATION_IDS)}; missing "
            f"{sorted(expected - declared)}, unexpected {sorted(declared - expected)} — a "
            f"missing required ablation fails the check rather than passing unnoticed (R-97)",
        )
    out: list[AblationEntry] = []
    for ablation_id in ABLATION_IDS:
        entry = entries[ablation_id]
        if not isinstance(entry, Mapping):
            raise IntegrityError(f"ablations.entries.{ablation_id}", "must be a mapping")
        reachable = entry.get("phase1_reachable")
        if not isinstance(reachable, bool):
            raise IntegrityError(
                f"ablations.entries.{ablation_id}.phase1_reachable", "must be true or false"
            )
        run_id = entry.get("run_id")
        registered_at = entry.get("registered_at")
        out.append(
            AblationEntry(
                ablation_id=ablation_id,
                run_id=None if _is_tbd(run_id) else str(run_id),
                registered_at=None if _is_tbd(registered_at) else str(registered_at),
                phase1_reachable=reachable,
                phase_deferral=(
                    None if _is_tbd(entry.get("phase_deferral")) else str(entry["phase_deferral"])
                ),
                inverse_before_metric=bool(entry.get("inverse_before_metric", False)),
                after_primary_freeze_only=bool(entry.get("after_primary_freeze_only", False)),
                configuration_change=str(entry.get("configuration_change", "")),
            )
        )
    return tuple(out)


def assert_ablation_runnable(
    entry: AblationEntry,
    *,
    phase: int,
    primary_frozen_hash: str | None,
    freeze_at: str | None,
    inverse_available: bool = False,
) -> None:
    """R-97's runnability checks for ONE registered ablation.

    Raises
    ------
    PhaseBoundaryError
        a Phase-2-deferred ablation (`ABL-ZENITH`) under Phase 1.
    IntegrityError
        no `run_id` / `registered_at` (not registered); registered at or after the freeze (an
        ablation registered after results are seen); `ABL-HIST48` before the primary freeze.
    InverseTransformError
        `ABL-DIFF` while no inverse exists — naming D-27.
    """
    if phase == 1 and not entry.phase1_reachable:
        raise PhaseBoundaryError(
            f"ablation {entry.ablation_id}",
            f"is deferred to Phase 2 ({entry.phase_deferral or 'phase deferral recorded'}); it "
            f"varies a target-aggregation choice that does not exist on the Phase 1 target",
        )
    if entry.run_id is None or entry.registered_at is None:
        raise IntegrityError(
            f"ablation {entry.ablation_id}",
            "carries no run_id / registered_at (TBD — freeze gate): every ablation is a named "
            "run registered in experiment.yaml with a run ID BEFORE the freeze (TE 7.2; R-97) — "
            "the registration is the owner's act, never defaulted",
        )
    if freeze_at is None:
        raise IntegrityError(
            f"ablation {entry.ablation_id}",
            "no freeze timestamp is recorded, so 'registered before the freeze' cannot be "
            "asserted",
        )
    registered = _as_utc(entry.registered_at, resource=f"ablation {entry.ablation_id}")
    frozen = _as_utc(freeze_at, resource="primary freeze")
    if not registered < frozen:
        raise IntegrityError(
            f"ablation {entry.ablation_id}",
            f"registered at {registered.isoformat()}, not before the freeze at "
            f"{frozen.isoformat()}; an ablation registered after results are seen fails (R-97)",
        )
    if entry.after_primary_freeze_only and not primary_frozen_hash:
        raise IntegrityError(
            f"ablation {entry.ablation_id}",
            "runs only after the primary configuration is frozen (TE 7.2), and no frozen "
            "primary grid hash exists yet (R-96's G-05 hash)",
        )
    if entry.inverse_before_metric and not inverse_available:
        raise InverseTransformError(
            f"ablation {entry.ablation_id}",
            "inverse-transforms to absolute TECU before any metric (TE 7.2), and no "
            "Transform.inverse exists: D-27 withheld the inverse mechanism and reopening it is "
            "the owner's act by a new D-number (code-generation FU-2 = B) — refused, not "
            "defaulted",
        )


def assert_no_promotion(reported_primary_hash: str, frozen_hash: str) -> None:
    """TE 7.2: no ablation configuration is promoted to primary once the locked test is
    opened — checked as reported-primary-hash == G-05-frozen-hash (R-97)."""
    if reported_primary_hash != frozen_hash:
        raise IntegrityError(
            "reported primary configuration",
            f"hash {reported_primary_hash[:12]}… differs from the G-05-frozen primary "
            f"{frozen_hash[:12]}…; no ablation configuration may be promoted to primary "
            f"(TE 7.2)",
        )


# --- W-12 / R-102a / SD-M-04: the prediction-hash receipt ---------------------------------


@dataclass(frozen=True)
class PredictionHashReceipt:
    """`domain-entities.md` section 13's five fields, matching the consuming units' shape."""

    prediction_path: str
    sha256: str
    recorded_at_utc: str
    run_id: str
    partition_id: str


def write_prediction_hash_receipt(
    prediction_path: Path, *, run_id: str, partition_id: str, receipt_path: Path
) -> PredictionHashReceipt:
    """Hash the prediction file AS WRITTEN and durably flush the receipt:
    `.tmp` -> fsync -> atomic rename (SD-M-04 steps 1–3). Never overwrites a receipt.

    Raises
    ------
    LockedTestError
        the prediction file is absent; a receipt already exists (write-once); the durable
        write fails at any step.
    """
    prediction_path = Path(prediction_path)
    receipt_path = Path(receipt_path)
    if not prediction_path.is_file():
        raise LockedTestError(
            prediction_path, "prediction file is absent; a receipt hashes a file as written"
        )
    if receipt_path.exists():
        raise LockedTestError(
            receipt_path,
            "a receipt already exists; the locked prediction is written and hashed exactly once "
            "(R-102a; FR-P1-05-12)",
        )
    receipt = PredictionHashReceipt(
        prediction_path=str(prediction_path),
        sha256=sha256_of_file(prediction_path),
        recorded_at_utc=dt.datetime.now(_UTC).isoformat(),
        run_id=run_id,
        partition_id=partition_id,
    )
    tmp = receipt_path.with_suffix(receipt_path.suffix + ".tmp")
    payload = (json.dumps(receipt.__dict__, sort_keys=True, indent=2) + "\n").encode("utf-8")
    try:
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
        try:
            written = os.write(fd, payload)
            if written != len(payload):
                raise LockedTestError(tmp, f"wrote {written} of {len(payload)} receipt bytes")
            os.fsync(fd)
        finally:
            os.close(fd)
        os.replace(tmp, receipt_path)  # atomic rename: a reader never sees a partial receipt
    except OSError as exc:
        raise LockedTestError(
            receipt_path, f"durable receipt write failed ({exc}); the receipt is not recorded"
        ) from exc
    return receipt


def load_prediction_hash_receipt(receipt_path: Path) -> PredictionHashReceipt:
    path = Path(receipt_path)
    if not path.is_file():
        raise LockedTestError(path, "no prediction-hash receipt exists (R-102a)")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return PredictionHashReceipt(
            prediction_path=str(payload["prediction_path"]),
            sha256=str(payload["sha256"]),
            recorded_at_utc=str(payload["recorded_at_utc"]),
            run_id=str(payload["run_id"]),
            partition_id=str(payload["partition_id"]),
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise LockedTestError(path, f"receipt is malformed ({exc})") from exc


def assert_receipt_matches(receipt: PredictionHashReceipt, prediction_path: Path) -> None:
    """The receipt file is authoritative for the hash; a mismatch against the file RAISES."""
    actual = sha256_of_file(Path(prediction_path))
    if actual != receipt.sha256:
        raise LockedTestError(
            prediction_path,
            f"sha256 {actual[:12]}… does not match the receipt's {receipt.sha256[:12]}…; the "
            f"prediction file is not the one that was hashed as written (R-102a)",
        )


def assert_locked_exit_allowed(
    prediction_path: Path, *, receipt_path: Path, registry_appended: bool
) -> None:
    """SD-M-04 step 5: `06` exits ONLY IF the receipt landed (rename) AND the registry row
    appended; a `DEC` prediction on disk with either missing raises `LockedTestError` on
    `06`'s own exit path — the failure reads `06` aborted, not `07` blocked."""
    prediction_path = Path(prediction_path)
    if not prediction_path.exists():
        return
    receipt = load_prediction_hash_receipt(receipt_path)  # raises: no receipt
    assert_receipt_matches(receipt, prediction_path)  # raises: hash mismatch
    if receipt.prediction_path != str(prediction_path):
        raise LockedTestError(
            receipt_path,
            f"receipt names {receipt.prediction_path!r}, not {str(prediction_path)!r}",
        )
    if not registry_appended:
        raise LockedTestError(
            prediction_path,
            "the registry append carrying prediction_hash (TE 13.4 column 18) did not succeed; "
            "the receipt file is authoritative for the hash and the registry row for the run's "
            "existence, and 06 refuses to exit with one and not the other (SD-M-04)",
        )
    if receipt.partition_id not in PARTITION_IDS:
        raise LockedTestError(receipt_path, f"partition_id {receipt.partition_id!r} is unknown")
