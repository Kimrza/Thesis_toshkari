"""WS-14 / TA-12 / TA-26: the six-family ladder, its closed set, and every hard rule's control.

PURPOSE. `models-and-baselines` R-90 ... R-102a, each with the negative control that proves
the violation is CAUGHT (team.md § Testing Posture). Over SYNTHETIC frames, partitions,
seeds, grids and settings: no D-122 seed, no D-121 grid value and no Vision 8.6 setting value
appears as a literal here — the real values live only in `configs/*.yaml`, and the one test
that reads them (`test_real_experiment_yaml_transcription_is_internally_consistent`) re-reads
the counts and compares them with the enumerated product rather than asserting a number.

What is covered: the closed model set (M-07 refuses; the two removed architectures, a second
deep-learning stack, and the forbidden import edges are absent by AST scan); M-01/M-02/M-03
happy paths and M-03's training-only control; M-04/M-05 refusal by NAME without scikit-learn
and grid-content controls; R-90's four stamp-match controls with control 3 by enumeration
over the six partition ids and the must-not-fire control; `three_seed_mean`'s four limbs;
tuning's December, criterion-hash and attestation refusals; the five-entry ablation registry
with `ABL-HIST48` and `ABL-DIFF` refusals; the config-only horizon (R-99) with a static scan;
the RF importance marker (R-100); the M-06 pin guard (FU-1 = C); and `06`'s receipt controls
driven through the script's own functions on a synthetic NON-DEC fixture, with the DEC guard
asserted to refuse.

INPUTS. In-memory synthetic bundles and targets over the synthetic partition year authored by
`test_split_embargo.py`. No December 2022 content, no restricted-root path, no real
signature, no model trained.

WHAT NO TEST HERE DISCHARGES. WS-14, WS-15, TA-12, TA-13, TA-26 stay `Pending`; M-04/M-05
fits are unrun (scikit-learn not installable here) and no M-06 Keras fit has ever run. The
TensorFlow pin is FROZEN (`requirements.txt` `tensorflow==2.21.0`, D-36) and
`require_frozen_pin` PASSES against the governed file: what blocks an M-06 fit is the
unverified ENVIRONMENT — no install or import has ever been exercised — not the guard. The
guard's refusal is still proved, on synthetic requirements files that carry no pin. Smoke
evidence only on the interpreter used here.

Run: pytest tests/test_models_smoke.py -rs
"""

from __future__ import annotations

import ast
import dataclasses
import datetime as dt
import hashlib
import importlib.util
import itertools
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "tests") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "tests"))
from _fresh_process import in_fresh_process  # noqa: E402
if str(REPO_ROOT / "tests") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "tests"))

from test_split_embargo import (  # noqa: E402
    SYNTH_YEAR,
    synthetic_partitions,
    synthetic_snapshot,
)

from src.data.config import (  # noqa: E402
    TBD_SENTINEL,
    AlignmentError,
    IntegrityError,
    InverseTransformError,
    LeakageError,
    LockedTestError,
    PartitionError,
    PhaseBoundaryError,
    SeedError,
)
from src.data.experiment_registry import REGISTRY_COLUMNS  # noqa: E402
from src.data.splits import (  # noqa: E402
    LOCKED_ID,
    PARTITION_IDS,
    REFIT_ID,
    RecordFrame,
    materialise_locked_partition,
    partition_by_id,
    training_range,
    validation_month_range,
)
from src.features._frames import frame_attrs, records_of  # noqa: E402
from src.features.build import FeatureBundle, FrameSpec  # noqa: E402
from src.features.transforms import transform_id_for  # noqa: E402
from src.models import climatology, lstm, persistence, random_forest, ridge  # noqa: E402
from src.models.train import (  # noqa: E402
    ABLATION_IDS,
    FITTED_MODEL_IDS,
    FOLD_PARTITION_IDS,
    GRID_TRACKS,
    LSTM_FIXED_SETTING_KEYS,
    MODEL_IDS,
    REFIT_EPOCH_RULE_ID,
    CandidateScore,
    FittedModelRecord,
    JsonStateBackend,
    Prediction,
    PredictionHashReceipt,
    TuningRecord,
    assert_ablation_runnable,
    assert_fitted_payload_unchanged,
    assert_grid_content,
    assert_grid_unchanged,
    assert_in_grid,
    assert_locked_exit_allowed,
    assert_no_promotion,
    assert_not_locked_fit,
    assert_refit_unchanged,
    assert_stamp_match,
    assert_validation_bundle,
    criterion_hash,
    eligible_feature_columns,
    enumerate_grid,
    expected_transform_id,
    fit_and_persist,
    fit_predict,
    grid_hash,
    load_fitted_model,
    mean_per_fold_skill,
    pinned_requirement,
    predict_from_fitted,
    read_ablations,
    read_horizons,
    read_lstm_fixed_settings,
    read_refit_epochs,
    record_tuning,
    resolve_horizon,
    select_configuration,
    three_seed_mean,
    write_prediction_hash_receipt,
)

UTC = dt.timezone.utc
PARTITIONS = synthetic_partitions()
MODELS_DIR = REPO_ROOT / "src" / "models"
SCRIPT_PATH = REPO_ROOT / "scripts" / "06_train_and_predict.py"

# --- the synthetic contract fixture (values are FIXTURE values, never the frozen ones) -----

SYNTH_HORIZON = 2  # a horizon at which lag-1 inputs are unobservable — exercises R-99's rule
SYNTH_SEEDS = {"development": 5, "final": [11, 22, 33]}
SYNTH_GRIDS: dict[str, Any] = {
    "ridge": {"model_id": "M-04", "axes": {"alpha": [0.5, 2.0]}, "combinations": 2},
    "random_forest": {
        "model_id": "M-05",
        "axes": {"n_estimators": [3, 5], "max_depth": [2, None], "min_samples_leaf": [1]},
        "fixed": {"max_features": "sqrt"},
        "combinations": 4,
    },
    "lstm": {
        "model_id": "M-06",
        "axes": {"layers": [1], "units": [4], "learning_rate": [0.5], "batch_size": [2]},
        "combinations": 1,
    },
}
SYNTH_SETTINGS: dict[str, Any] = {
    "dropout": 0.35,
    "optimizer": "Adam",
    "loss": "MSE",
    "max_epochs": 6,
    "early_stopping_patience": 2,
    "early_stopping_monitor": "validation_rmse",
    "min_improvement_tecu": 0.05,
    "checkpoint_policy": "best_checkpoint",
}
#: M-03's key definition and the refit's epoch rule as CONFIG — fixture values, never the
#: governed ones (the real `models.refit.epochs` is `TBD — freeze gate` until the folds run).
SYNTH_CLIMATOLOGY: dict[str, Any] = {
    "key": ["station", "hour"],
    "fitted_on": "training_partition_only",
}
SYNTH_REFIT: dict[str, Any] = {"rule": REFIT_EPOCH_RULE_ID, "epochs": 4}
SYNTH_MODELS: dict[str, Any] = {
    "lstm_fixed_settings": SYNTH_SETTINGS,
    "climatology": SYNTH_CLIMATOLOGY,
    "refit": SYNTH_REFIT,
}


def _ablation_entries(**overrides: dict[str, Any]) -> dict[str, dict[str, Any]]:
    base = {
        "ABL-NODOY": {"phase1_reachable": True},
        "ABL-DIFF": {"phase1_reachable": True, "inverse_before_metric": True},
        "ABL-NOSW": {"phase1_reachable": True},
        "ABL-HIST48": {"phase1_reachable": True, "after_primary_freeze_only": True},
        "ABL-ZENITH": {"phase1_reachable": False, "phase_deferral": "Phase 2"},
    }
    for entry in base.values():
        entry.setdefault("run_id", TBD_SENTINEL)
        entry.setdefault("registered_at", TBD_SENTINEL)
    for key, patch in overrides.items():
        base[key].update(patch)
    return base


def _snapshot(**experiment: Any):
    exp: dict[str, Any] = {
        "horizons": [SYNTH_HORIZON],
        "grids": SYNTH_GRIDS,
        "models": dict(SYNTH_MODELS),
        "ablations": {"entries": _ablation_entries()},
    }
    exp.update(experiment)
    snapshot = synthetic_snapshot(experiment=exp)
    return dataclasses.replace(snapshot, seeds=dict(SYNTH_SEEDS))


SNAPSHOT = _snapshot()


def _p(pid: str):
    return partition_by_id(PARTITIONS, pid)


def _ts(month: int, day: int, hour: int = 0) -> dt.datetime:
    return dt.datetime(SYNTH_YEAR, month, day, hour, tzinfo=UTC)


def _train_spec(pid: str) -> FrameSpec:
    start, end = training_range(_p(pid))
    return FrameSpec(pid, "train", start, end)


def _score_spec(pid: str) -> FrameSpec:
    start, end = validation_month_range(_p(pid))
    return FrameSpec(pid, "score", start, end)


STATIONS = ("S1", "S2")
FEATURES = ("vtec_lag_1h", "vtec_lag_2h", "f107_safe", "seq_t-1", "seq_t-3")
PROVENANCE = {
    "vtec_lag_1h": {"dictionary_row": "vtec_lag", "dictionary_field": "vtec_lag_1h"},
    "vtec_lag_2h": {"dictionary_row": "vtec_lag", "dictionary_field": "vtec_lag_2h"},
    "f107_safe": {"dictionary_row": "f107_safe", "dictionary_field": "f107_safe"},
    "seq_t-1": {"dictionary_row": "vtec_seq_24", "dictionary_field": "seq"},
    "seq_t-3": {"dictionary_row": "vtec_seq_24", "dictionary_field": "seq"},
}
IDENTITY = {"phase_id": "p", "source_id": "s", "target_definition_id": "t"}


def _value(station: str, stamp: dt.datetime) -> float:
    """A deterministic synthetic target: station offset + hour-of-day shape + day drift."""
    base = 10.0 if station == "S1" else 20.0
    return base + stamp.hour * 0.5 + stamp.timetuple().tm_yday * 0.01


def _target(start: dt.datetime, end: dt.datetime, *, stations=STATIONS, gaps=()) -> RecordFrame:
    rows = []
    stamp = start
    while stamp < end:
        for station in stations:
            value = None if (station, stamp) in gaps else _value(station, stamp)
            rows.append(
                {
                    "interval_start_utc": stamp.isoformat(),
                    "station_id": station,
                    "vtec_tecu": value,
                }
            )
        stamp += dt.timedelta(hours=1)
    return RecordFrame(rows)


def _bundle(
    spec: FrameSpec,
    *,
    transform_id: str | None,
    start: dt.datetime | None = None,
    hours: int = 6,
    stations=STATIONS,
    identity: Mapping[str, str] | None = None,
) -> FeatureBundle:
    """A hand-built bundle: rows at hourly stamps from `start`, feature columns from the
    target (so a fit has signal), the identity stamps a consumer reads from spec.json."""
    begin = start if start is not None else spec.scored_start
    records = []
    nested = []
    for h in range(hours):
        stamp = begin + dt.timedelta(hours=h)
        for station in stations:
            y1 = _value(station, stamp - dt.timedelta(hours=1))
            y2 = _value(station, stamp - dt.timedelta(hours=2))
            records.append(
                {
                    "interval_start_utc": stamp.isoformat(),
                    "station_id": station,
                    "vtec_lag_1h": y1,
                    "vtec_lag_2h": y2,
                    "f107_safe": 100.0,
                    "seq_t-1": y1,
                    "seq_t-3": _value(station, stamp - dt.timedelta(hours=3)),
                }
            )
            nested.append([[_value(station, stamp - dt.timedelta(hours=k))] for k in (3, 2, 1)])
    frame = RecordFrame(records)
    frame.attrs.update({"partition_id": spec.partition_id, "role": spec.role})
    return FeatureBundle(
        matrix=frame,
        tensor=nested,
        spec=spec,
        transform_id=transform_id,
        provenance={k: dict(v) for k, v in PROVENANCE.items()},
        identity=dict(identity or IDENTITY),
        standardized_columns=("vtec_lag_1h", "vtec_lag_2h"),
        sequence_columns={"seq": ("seq_t-3", "seq_t-2", "seq_t-1")},
        tensor_features=("seq",),
    )


def _prediction(
    *,
    seed: int | None = 11,
    model_id: str = "M-06",
    partition_id: str = "F1",
    transform_id: str | None = "T-F1",
    rows: list[dict[str, Any]] | None = None,
    role: str = "score",
    identity: Mapping[str, str] | None = None,
) -> Prediction:
    base_rows = rows or [
        {"station": "S1", "interval_start_utc": _ts(4, 1, 0).isoformat(), "y_hat": 1.0},
        {"station": "S1", "interval_start_utc": _ts(4, 1, 1).isoformat(), "y_hat": 2.0},
        {"station": "S2", "interval_start_utc": _ts(4, 1, 0).isoformat(), "y_hat": 3.0},
    ]
    frame = RecordFrame(base_rows)
    frame.attrs.update({"role": role})
    ident = dict(identity or IDENTITY)
    return Prediction(
        model_id=model_id,
        seed=seed,
        frame=frame,
        target_definition_id=ident["target_definition_id"],
        phase_id=ident["phase_id"],
        source_id=ident["source_id"],
        partition_id=partition_id,
        transform_id=transform_id,  # type: ignore[arg-type]
    )


def _three(seeds: list[int], **kwargs: Any) -> list[Prediction]:
    return [_prediction(seed=s, **kwargs) for s in seeds]


def _load_script():
    spec = importlib.util.spec_from_file_location("script06", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _ast_of(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


# =======================================================================================
# 1. The closed model set, and the absences that are evidence (R-102; TA-12)
# =======================================================================================


def test_the_model_set_is_exactly_the_six_families_and_a_seventh_refuses() -> None:
    assert MODEL_IDS == ("M-01", "M-02", "M-03", "M-04", "M-05", "M-06")
    bundle = _bundle(_train_spec("F1"), transform_id="T-F1")
    with pytest.raises(IntegrityError) as excinfo:
        fit_predict("M-07", bundle=bundle, partition=_p("F1"), snapshot=SNAPSHOT, target=[])
    assert "closed model set" in str(excinfo.value)


def test_the_two_removed_architectures_and_a_second_dl_stack_are_absent_from_src_models() -> None:
    """TA-12's grep evidence, mechanised: no module named for the removed architectures, no
    identifier or import naming them, no PyTorch import — over every file under src/models."""
    removed_tokens = {"gru", "residual"}
    forbidden_imports = {"torch"}
    files = sorted(MODELS_DIR.glob("*.py"))
    assert len(files) == 8, [f.name for f in files]  # __init__ + the seven owned modules
    for path in files:
        assert not any(tok in path.stem.lower() for tok in removed_tokens), path
        tree = _ast_of(path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[0] not in forbidden_imports, (path, alias.name)
            elif isinstance(node, ast.ImportFrom):
                assert (node.module or "").split(".")[0] not in forbidden_imports, path
            elif isinstance(node, ast.Name):
                assert node.id.lower() not in removed_tokens, (path, node.id)
            elif isinstance(node, ast.Attribute):
                assert node.attr.lower() not in removed_tokens, (path, node.attr)
        text = path.read_text(encoding="utf-8").lower()
        assert "torch" not in text, f"{path}: the grep evidence must be token-clean"


def test_src_models_never_imports_iri_gim_or_evaluation_and_frameworks_only_lazily() -> None:
    """R-102's import boundary (TE 12; TA-07) and FU-1 = C / Q3 = A: `tensorflow` and
    `sklearn` appear only INSIDE function bodies, never at module scope."""
    forbidden = ("src.external.iri", "src.external.gim", "src.evaluation")
    for path in sorted(MODELS_DIR.glob("*.py")):
        tree = _ast_of(path)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom | ast.Import):
                names = (
                    [node.module or ""]
                    if isinstance(node, ast.ImportFrom)
                    else [a.name for a in node.names]
                )
                for name in names:
                    assert not any(name.startswith(f) for f in forbidden), (path, name)
        for node in tree.body:  # module scope only
            if isinstance(node, ast.Import | ast.ImportFrom):
                names = (
                    [node.module or ""]
                    if isinstance(node, ast.ImportFrom)
                    else [a.name for a in node.names]
                )
                for name in names:
                    assert name.split(".")[0] not in ("tensorflow", "sklearn"), (path, name)


@in_fresh_process
def test_importing_src_models_loads_neither_tensorflow_nor_sklearn() -> None:
    assert "tensorflow" not in sys.modules
    assert "sklearn" not in sys.modules


def test_prediction_carries_exactly_the_eight_approved_fields() -> None:
    names = [f.name for f in dataclasses.fields(Prediction)]
    assert names == [
        "model_id",
        "seed",
        "frame",
        "target_definition_id",
        "phase_id",
        "source_id",
        "partition_id",
        "transform_id",
    ]


# =======================================================================================
# 2. M-01, M-02, M-03 over synthetic frames; M-03's training-only control (R-98)
# =======================================================================================


def test_persistence_reads_the_raw_target_at_the_forecast_origin() -> None:
    score = _bundle(_score_spec("F1"), transform_id="T-F1")
    target = _target(_ts(1, 1), _ts(5, 1))
    prediction = fit_predict(
        "M-01", bundle=score, partition=_p("F1"), snapshot=SNAPSHOT, target=target
    )
    assert prediction.model_id == "M-01" and prediction.seed is None
    assert (prediction.partition_id, prediction.transform_id) == ("F1", "T-F1")
    rows = records_of(prediction.frame)
    assert len(rows) == 6 * len(STATIONS)
    first = rows[0]
    stamp = dt.datetime.fromisoformat(first["interval_start_utc"])
    assert first["y_hat"] == _value("S1", stamp - dt.timedelta(hours=SYNTH_HORIZON))
    assert frame_attrs(prediction.frame)["missing_source_values"] == 0


def test_seasonal_persistence_uses_the_smallest_whole_day_at_least_the_horizon() -> None:
    lag = persistence.seasonal_lag_hours(SYNTH_HORIZON)
    assert lag % persistence.HOURS_PER_DAY == 0 and lag >= SYNTH_HORIZON
    assert persistence.seasonal_lag_hours(persistence.HOURS_PER_DAY) == persistence.HOURS_PER_DAY
    assert persistence.seasonal_lag_hours(persistence.HOURS_PER_DAY + 1) == (
        2 * persistence.HOURS_PER_DAY
    )
    score = _bundle(_score_spec("F1"), transform_id="T-F1")
    target = _target(_ts(1, 1), _ts(5, 1))
    prediction = fit_predict(
        "M-02", bundle=score, partition=_p("F1"), snapshot=SNAPSHOT, target=target
    )
    row = records_of(prediction.frame)[0]
    stamp = dt.datetime.fromisoformat(row["interval_start_utc"])
    assert row["y_hat"] == _value("S1", stamp - dt.timedelta(hours=lag))


def test_persistence_counts_a_missing_source_value_and_refuses_hyperparameters() -> None:
    score = _bundle(_score_spec("F1"), transform_id="T-F1", hours=2)
    origin = score.spec.scored_start - dt.timedelta(hours=SYNTH_HORIZON)
    target = _target(_ts(1, 1), _ts(5, 1), gaps={("S1", origin)})
    prediction = fit_predict(
        "M-01", bundle=score, partition=_p("F1"), snapshot=SNAPSHOT, target=target
    )
    assert frame_attrs(prediction.frame)["missing_source_values"] == 1
    y_hat = records_of(prediction.frame)[0]["y_hat"]
    # MISSING in either representation: None (record sequence) or NaN (DataFrame — pandas
    # coerces None to NaN in a float column). Asserting `is None` alone was a
    # representation assumption that only held while pandas was absent (G-10).
    assert y_hat is None or (isinstance(y_hat, float) and y_hat != y_hat), y_hat
    with pytest.raises(IntegrityError):
        fit_predict(
            "M-01", bundle=score, partition=_p("F1"), snapshot=SNAPSHOT, target=target,
            params={"alpha": 1},
        )


def test_climatology_is_keyed_by_station_and_hour_and_covers_every_scored_row() -> None:
    """Recommendation 2 (owner ruling, 2026-09-20): the key is `(station, hour)`, fitted on
    the training range alone, and EVERY scored row is producible from it.

    The superseded `(station, month, hour)` key could not produce a single scored key on any
    of the five scored partitions — the split calendar is strictly expanding, so the scored
    month is always after the training range — and answered `y_hat = None` for every row
    while reporting the hole only as a count. `missing_climatology_keys` is now a MEASURED
    zero: the coverage guard makes it so, and the assertion below would have read
    `3 * len(STATIONS)` under the old key.
    """
    train = _bundle(_train_spec("F1"), transform_id="T-F1", hours=48)
    score = _bundle(_score_spec("F1"), transform_id="T-F1", hours=3)
    target = _target(_ts(1, 1), _ts(5, 1))
    prediction = fit_predict(
        "M-03", bundle=train, partition=_p("F1"), snapshot=SNAPSHOT, target=target,
        score_bundle=score,
    )
    assert climatology.climatology_fit_partition(prediction) == ("F1",)
    climatology.assert_fitted_on_training_partitions(prediction)
    attrs = frame_attrs(prediction.frame)
    assert attrs["fitted_role"] == "train" and attrs["fitted_rows"] == 48 * len(STATIONS)
    assert attrs["missing_climatology_keys"] == 0
    assert attrs["climatology_key"] == list(climatology.CLIMATOLOGY_KEY_FIELDS) == [
        "station", "hour",
    ]
    assert "no seasonal term" in attrs["climatology_limitation"]
    rows = records_of(prediction.frame)
    assert len(rows) == 3 * len(STATIONS)
    assert all(r["y_hat"] is not None for r in rows), "every scored row is answered"
    # the value is the training-range mean over that (station, hour), computed here from the
    # fixture generator rather than carried: two January days at hour 0 for S1
    first = rows[0]
    stamp = dt.datetime.fromisoformat(first["interval_start_utc"])
    train_start, _ = training_range(_p("F1"))
    same_hour = [
        _value("S1", train_start + dt.timedelta(hours=h))
        for h in range(48)
        if (train_start + dt.timedelta(hours=h)).hour == stamp.hour
    ]
    assert first["y_hat"] == pytest.approx(sum(same_hour) / len(same_hour))


def test_a_fit_that_cannot_produce_a_scored_key_fails_early_naming_the_key() -> None:
    """Negative control (a): the coverage guard fires AT FIT TIME, not at prediction time.

    A two-hour training range cannot answer an hour-2 scored row. Under the superseded
    behaviour this produced `y_hat = None` and a count; it now refuses, naming the missing
    `(station, hour)` keys, the fitting range and the config field that defines the key.
    """
    train = _bundle(_train_spec("F1"), transform_id="T-F1", hours=2)
    score = _bundle(_score_spec("F1"), transform_id="T-F1", hours=3)
    target = _target(_ts(1, 1), _ts(5, 1))
    with pytest.raises(IntegrityError) as excinfo:
        fit_predict(
            "M-03", bundle=train, partition=_p("F1"), snapshot=SNAPSHOT, target=target,
            score_bundle=score,
        )
    message = str(excinfo.value)
    assert "('S1', 2)" in message and "('S2', 2)" in message
    assert "models.climatology.key" in message
    assert "src/models/climatology.py" in message


def test_climatology_fitted_across_the_whole_year_fails_the_r98_control() -> None:
    """Negative control (b): the train-only rule is NOT weakened by the key change.

    Rows beyond the training range reach the fit — the exact case FR-P1-05-21 names — and
    the refusal is the same `LeakageError` it always was, raised before any coverage check.
    """
    start, _ = training_range(_p("F1"))
    beyond = _bundle(_train_spec("F1"), transform_id="T-F1", start=start, hours=24 * 120)
    score = _bundle(_score_spec("F1"), transform_id="T-F1", hours=3)
    with pytest.raises(LeakageError) as excinfo:
        climatology.fit_climatology(
            beyond, partition=_p("F1"), series={}, snapshot=SNAPSHOT, score_bundle=score
        )
    assert "outside partition F1's training range" in str(excinfo.value)


def test_climatology_refuses_a_score_role_bundle_and_a_tampered_fit_record() -> None:
    score = _bundle(_score_spec("F1"), transform_id="T-F1")
    with pytest.raises(LeakageError):
        climatology.fit_climatology(
            score, partition=_p("F1"), series={}, snapshot=SNAPSHOT, score_bundle=None
        )
    with pytest.raises(LeakageError):
        fit_predict(
            "M-03", bundle=score, partition=_p("F1"), snapshot=SNAPSHOT,
            target=_target(_ts(1, 1), _ts(5, 1)),
        )
    tampered = _prediction(model_id="M-03", seed=None)
    tampered.frame.attrs.update({"fitted_partitions": ["F1"], "fitted_role": "score"})
    with pytest.raises(LeakageError):
        climatology.assert_fitted_on_training_partitions(tampered)
    with pytest.raises(IntegrityError):
        climatology.climatology_fit_partition(_prediction(model_id="M-03", seed=None))


def test_the_climatology_key_is_configuration_and_an_unimplemented_field_refuses() -> None:
    """TC-03e: the key definition lives in `configs/experiment.yaml`, not in source.

    A month-bearing key — the superseded definition — is refused BY NAME rather than
    silently grouped, so re-adopting it needs an implementation and the ordering argument
    re-examined, never a config edit alone. `fitted_on` is likewise not widenable.
    """
    assert climatology.read_climatology_key(SNAPSHOT) == ("station", "hour")
    with pytest.raises(IntegrityError) as excinfo:
        climatology.read_climatology_key(
            _snapshot(models=dict(SYNTH_MODELS, climatology={
                "key": ["station", "month", "hour"], "fitted_on": "training_partition_only",
            }))
        )
    assert "'month'" in str(excinfo.value)
    with pytest.raises(IntegrityError):  # a known field in the wrong order is still refused
        climatology.read_climatology_key(
            _snapshot(models=dict(SYNTH_MODELS, climatology={
                "key": ["hour", "station"], "fitted_on": "training_partition_only",
            }))
        )
    with pytest.raises(LeakageError) as excinfo:
        climatology.read_climatology_key(
            _snapshot(models=dict(SYNTH_MODELS, climatology={
                "key": ["station", "hour"], "fitted_on": "all_partitions",
            }))
        )
    assert "training_partition_only" in str(excinfo.value)
    with pytest.raises(IntegrityError):  # the block itself unresolved
        climatology.read_climatology_key(
            _snapshot(models=dict(SYNTH_MODELS, climatology=TBD_SENTINEL))
        )
    with pytest.raises(IntegrityError):  # and absent entirely
        climatology.read_climatology_key(
            _snapshot(models={"lstm_fixed_settings": SYNTH_SETTINGS})
        )


def test_fit_predict_refuses_an_untransformed_bundle_a_seed_on_an_unseeded_family_and_no_target(
) -> None:
    raw = _bundle(_train_spec("F1"), transform_id=None)
    with pytest.raises(LeakageError):
        fit_predict("M-01", bundle=raw, partition=_p("F1"), snapshot=SNAPSHOT, target=[])
    good = _bundle(_score_spec("F1"), transform_id="T-F1")
    with pytest.raises(SeedError):
        fit_predict("M-01", bundle=good, partition=_p("F1"), snapshot=SNAPSHOT, target=[], seed=3)
    with pytest.raises(IntegrityError) as excinfo:
        fit_predict("M-01", bundle=good, partition=_p("F1"), snapshot=SNAPSHOT)
    assert "D-27" in str(excinfo.value)
    with pytest.raises(PartitionError):
        fit_predict("M-01", bundle=good, partition=_p("F2"), snapshot=SNAPSHOT, target=[])


# =======================================================================================
# 3. M-04 / M-05: refusal by name without scikit-learn; grid content against config (R-96)
# =======================================================================================


def _sklearn_absent() -> bool:
    return importlib.util.find_spec("sklearn") is None


def test_ridge_and_forest_refuse_by_name_when_sklearn_is_absent() -> None:
    if not _sklearn_absent():
        pytest.skip("scikit-learn is installed here; the refusal path is not reachable")
    pin = pinned_requirement("scikit-learn")
    assert pin is not None and pin.startswith("scikit-learn=="), "Q3 = A's pin must exist"
    train = _bundle(_train_spec("F1"), transform_id="T-F1", hours=4)
    score = _bundle(_score_spec("F1"), transform_id="T-F1", hours=2)
    target = _target(_ts(1, 1), _ts(5, 1))
    for model_id, params in (
        ("M-04", {"alpha": 0.5}),
        (
            "M-05",
            {"n_estimators": 3, "max_depth": 2, "min_samples_leaf": 1, "max_features": "sqrt"},
        ),
    ):
        with pytest.raises(IntegrityError) as excinfo:
            fit_predict(
                model_id, bundle=train, partition=_p("F1"), snapshot=SNAPSHOT, target=target,
                score_bundle=score, params=params,
            )
        assert pin in str(excinfo.value), "the refusal names the governed pin"
        assert "TS-M-03" in str(excinfo.value)
    assert "sklearn" not in sys.modules


def test_a_grid_point_outside_the_config_grid_refuses_before_any_import() -> None:
    train = _bundle(_train_spec("F1"), transform_id="T-F1", hours=4)
    with pytest.raises(IntegrityError) as excinfo:
        fit_predict(
            "M-04", bundle=train, partition=_p("F1"), snapshot=SNAPSHOT,
            target=_target(_ts(1, 1), _ts(5, 1)), params={"alpha": 7.5},
        )
    assert "not a member" in str(excinfo.value)
    with pytest.raises(IntegrityError):
        fit_predict(
            "M-04", bundle=train, partition=_p("F1"), snapshot=SNAPSHOT,
            target=_target(_ts(1, 1), _ts(5, 1)),
        )  # no grid point at all: a default alpha would be a value chosen by convenience


def test_grid_content_is_the_enumerated_product_and_a_declared_count_mismatch_fails() -> None:
    counts = assert_grid_content(SNAPSHOT)
    for track, spec in SYNTH_GRIDS.items():
        product = 1
        for axis in spec["axes"].values():
            product *= len(axis)
        assert counts[track] == product == spec["combinations"]
        assert len(enumerate_grid(SNAPSHOT, track)) == product
    wrong = json.loads(json.dumps(SYNTH_GRIDS))
    wrong["ridge"]["combinations"] += 1  # a grid that is immutable but wrong is immutably wrong
    with pytest.raises(IntegrityError) as excinfo:
        assert_grid_content(_snapshot(grids=wrong))
    assert "content is asserted" in str(excinfo.value)
    assert_in_grid(SNAPSHOT, "random_forest", enumerate_grid(SNAPSHOT, "random_forest")[0])
    with pytest.raises(IntegrityError):
        assert_in_grid(SNAPSHOT, "random_forest", {"n_estimators": 3})  # a partial point


def test_the_grid_hash_is_the_frozen_object_and_a_changed_range_fails_the_diff() -> None:
    frozen = grid_hash(SNAPSHOT)
    assert_grid_unchanged(SNAPSHOT, frozen)
    changed = json.loads(json.dumps(SYNTH_GRIDS))
    changed["lstm"]["axes"]["units"] = [4, 8]
    changed["lstm"]["combinations"] = 2
    with pytest.raises(IntegrityError):
        assert_grid_unchanged(_snapshot(grids=changed), frozen)
    with pytest.raises(IntegrityError):
        assert_grid_content(_snapshot(grids=TBD_SENTINEL))


def test_real_experiment_yaml_transcription_is_internally_consistent() -> None:
    """Re-reads the REAL configs/experiment.yaml (Q5 = A) and checks D-121's declared counts
    against the enumerated product of the transcribed axes, the seven settings, and the five
    ablations — asserting no number from this file."""
    yaml = pytest.importorskip("yaml")
    parsed = yaml.safe_load((REPO_ROOT / "configs" / "experiment.yaml").read_text("utf-8"))
    snapshot = dataclasses.replace(SNAPSHOT, experiment=parsed)
    counts = assert_grid_content(snapshot)
    for track in GRID_TRACKS:
        assert counts[track] == parsed["grids"][track]["combinations"]
    settings = read_lstm_fixed_settings(snapshot)
    assert tuple(settings) == LSTM_FIXED_SETTING_KEYS
    assert tuple(e.ablation_id for e in read_ablations(snapshot)) == ABLATION_IDS
    assert parsed["grids"]["decision"] == "D-121"
    # D-51 (2026-09-20): TE 2.1's `horizons: [1]` is transcribed; the +24 h horizon stays
    # outside the default run list (a config change, never a code change).
    assert read_horizons(snapshot) == (1,)


# =======================================================================================
# 4. R-90: the stamp match before every scoring path — four controls + must-not-fire
# =======================================================================================


def test_control_1_a_train_frame_reaching_its_own_score_path_is_a_partition_error() -> None:
    bundle = _bundle(_train_spec("F4"), transform_id="T-F4")
    with pytest.raises(PartitionError) as excinfo:
        assert_stamp_match(bundle, _p("F4"))
    assert "role" in str(excinfo.value)


def test_control_2_an_untransformed_frame_reaching_any_score_path_is_a_leakage_error() -> None:
    for pid in PARTITION_IDS:
        if _p(pid).validation_month is None:
            continue
        bundle = _bundle(_score_spec(pid), transform_id=None)
        with pytest.raises(LeakageError):
            assert_stamp_match(bundle, _p(pid))


def test_control_3_by_enumeration_over_ordered_pairs_of_the_six_ids() -> None:
    """Every mismatched ordered pair (j, k) with a score-role frame for j reaching k's path
    raises PartitionError — 30 pairs, derived not carried; the 6 identities are the
    must-not-fire cases checked separately."""
    scorable = [pid for pid in PARTITION_IDS if _p(pid).validation_month is not None]
    raised = 0
    for frame_pid, scored_pid in itertools.product(scorable, PARTITION_IDS):
        if frame_pid == scored_pid:
            continue
        bundle = _bundle(_score_spec(frame_pid), transform_id=expected_transform_id(_p(frame_pid)))
        with pytest.raises(PartitionError):
            assert_stamp_match(bundle, _p(scored_pid))
        raised += 1
    assert raised == len(scorable) * (len(PARTITION_IDS) - 1) == 25


def test_control_4_a_correctly_stamped_frame_carrying_another_transform_is_a_leakage_error(
) -> None:
    bundle = _bundle(_score_spec("F3"), transform_id="T-F1")
    with pytest.raises(LeakageError) as excinfo:
        assert_stamp_match(bundle, _p("F3"))
    assert "wrongly applied" in str(excinfo.value)


def test_the_ordinary_path_must_not_fire() -> None:
    for pid in PARTITION_IDS:
        partition = _p(pid)
        if partition.validation_month is None:
            continue
        own = expected_transform_id(partition)
        assert_stamp_match(_bundle(_score_spec(pid), transform_id=own), partition)
    assert expected_transform_id(_p(LOCKED_ID)) == transform_id_for(REFIT_ID)
    with pytest.raises(LeakageError):  # DEC carrying its own name rather than the refit's fit
        assert_stamp_match(
            _bundle(_score_spec(LOCKED_ID), transform_id=transform_id_for(LOCKED_ID)),
            _p(LOCKED_ID),
        )


# =======================================================================================
# 5. three_seed_mean: all four limbs (R-91, R-92, R-93; BLK-03 approved 2026-09-06)
# =======================================================================================

EXPECTED = frozenset(SYNTH_SEEDS["final"])


def test_the_pass_case_averages_element_wise_and_copies_provenance_with_seed_none() -> None:
    inputs = _three(sorted(EXPECTED))
    for offset, prediction in enumerate(inputs):
        for row in prediction.frame:
            row["y_hat"] = row["y_hat"] + offset  # 1,2,3 / 2,3,4 / 3,4,5 -> means 2,3,4
    mean = three_seed_mean(inputs, expected_seeds=EXPECTED)
    assert mean.model_id == "M-06" and mean.seed is None
    assert [r["y_hat"] for r in records_of(mean.frame)] == [2.0, 3.0, 4.0]
    assert (mean.partition_id, mean.transform_id) == ("F1", "T-F1")
    assert (mean.phase_id, mean.source_id, mean.target_definition_id) == ("p", "s", "t")
    assert frame_attrs(mean.frame)["confirmatory"] is True
    assert all(p.seed is not None for p in inputs), "the three inputs are preserved, untouched"


def test_single_seed_and_best_of_three_substitutes_are_seed_errors() -> None:
    with pytest.raises(SeedError):
        three_seed_mean(_three([sorted(EXPECTED)[0]]), expected_seeds=EXPECTED)
    with pytest.raises(SeedError):
        three_seed_mean(_three(sorted(EXPECTED)[:2]), expected_seeds=EXPECTED)
    with pytest.raises(SeedError):
        three_seed_mean(_three(sorted(EXPECTED) + [sorted(EXPECTED)[0]]), expected_seeds=EXPECTED)


def test_a_wrong_but_distinct_triple_is_a_seed_error_not_a_pass() -> None:
    """Constructed from the fixture set at test time: one seed off by one, the others kept."""
    ordered = sorted(EXPECTED)
    wrong = [ordered[0] + 1, *ordered[1:]]
    assert len(set(wrong)) == 3, "pairwise distinct — exactly what a distinctness check passes"
    with pytest.raises(SeedError) as excinfo:
        three_seed_mean(_three(wrong), expected_seeds=EXPECTED)
    assert "not exactly the configured set" in str(excinfo.value)


def test_seed_none_input_non_m06_input_and_a_bad_expected_set_are_seed_errors() -> None:
    inputs = _three(sorted(EXPECTED))
    inputs[1] = _prediction(seed=None)
    with pytest.raises(SeedError):
        three_seed_mean(inputs, expected_seeds=EXPECTED)
    inputs = _three(sorted(EXPECTED))
    inputs[2] = _prediction(seed=sorted(EXPECTED)[2], model_id="M-04")
    with pytest.raises(SeedError):
        three_seed_mean(inputs, expected_seeds=EXPECTED)
    with pytest.raises(SeedError):
        three_seed_mean(_three(sorted(EXPECTED)), expected_seeds=frozenset(sorted(EXPECTED)[:2]))


def test_one_row_misalignment_and_same_rows_in_a_different_order_are_alignment_errors() -> None:
    inputs = _three(sorted(EXPECTED))
    inputs[2].frame.append(
        {"station": "S2", "interval_start_utc": _ts(4, 1, 1).isoformat(), "y_hat": 9.0}
    )
    with pytest.raises(AlignmentError):
        three_seed_mean(inputs, expected_seeds=EXPECTED)
    inputs = _three(sorted(EXPECTED))
    inputs[1].frame.reverse()  # identical row SET, different order
    with pytest.raises(AlignmentError) as excinfo:
        three_seed_mean(inputs, expected_seeds=EXPECTED)
    assert "ORDER" in str(excinfo.value)


def test_cross_partition_and_training_partition_inputs_are_partition_errors() -> None:
    inputs = _three(sorted(EXPECTED))
    inputs[0] = _prediction(seed=sorted(EXPECTED)[0], partition_id="F2", transform_id="T-F1")
    with pytest.raises(PartitionError):
        three_seed_mean(inputs, expected_seeds=EXPECTED)
    with pytest.raises(PartitionError):
        three_seed_mean(_three(sorted(EXPECTED), role="train"), expected_seeds=EXPECTED)
    inputs = _three(sorted(EXPECTED))
    inputs[0] = _prediction(
        seed=sorted(EXPECTED)[0], identity=dict(IDENTITY, source_id="other")
    )
    with pytest.raises(PartitionError):
        three_seed_mean(inputs, expected_seeds=EXPECTED)


def test_transform_disagreement_or_none_is_a_leakage_error() -> None:
    inputs = _three(sorted(EXPECTED))
    inputs[1] = _prediction(seed=sorted(EXPECTED)[1], transform_id="T-F2")
    with pytest.raises(LeakageError):
        three_seed_mean(inputs, expected_seeds=EXPECTED)
    inputs = _three(sorted(EXPECTED))
    inputs[2] = _prediction(seed=sorted(EXPECTED)[2], transform_id=None)
    with pytest.raises(LeakageError):
        three_seed_mean(inputs, expected_seeds=EXPECTED)


def test_the_frozen_seed_set_never_appears_in_src_models() -> None:
    """R-91: the set reaches `three_seed_mean` as a parameter. Mechanised as: no set or list
    literal of three integers anywhere under src/models."""
    for path in sorted(MODELS_DIR.glob("*.py")):
        for node in ast.walk(_ast_of(path)):
            if isinstance(node, ast.Set | ast.List | ast.Tuple) and len(node.elts) == 3:
                assert not all(
                    isinstance(e, ast.Constant) and isinstance(e.value, int) for e in node.elts
                ), (path, node.lineno)


# =======================================================================================
# 6. Tuning: December excluded, criterion hash pair, unconditional attestation (R-95; SD-M-01)
# =======================================================================================

CRITERION = {"criterion": "mean_per_fold_skill", "declared_baseline": "M-01", "folds": "F1-F4"}
DECLARED_AT = "2026-09-01T00:00:00+00:00"
RUN_AT = "2026-09-02T00:00:00+00:00"


def _tune(**overrides: Any) -> TuningRecord:
    kwargs: dict[str, Any] = {
        "run_id": "tune-1",
        "partitions_read": ("F1", "F2", "F3", "F4"),
        "criterion_declared": CRITERION,
        "criterion_declared_at": DECLARED_AT,
        "criterion_used": CRITERION,
        "run_at": RUN_AT,
        "attested_by": "student",
        "attested_at_utc": RUN_AT,
        "attests_criterion_hash": criterion_hash(CRITERION),
    }
    kwargs.update(overrides)
    return record_tuning(**kwargs)


def test_a_tuning_record_carries_the_seven_approved_fields_plus_three_attestation_fields(
) -> None:
    record = _tune()
    names = [f.name for f in dataclasses.fields(TuningRecord)]
    assert len(names) == 10
    assert names[-3:] == ["attested_by", "attested_at_utc", "attests_criterion_hash"]
    assert record.criterion_hash == record.criterion_used_hash == criterion_hash(CRITERION)


def test_a_december_partition_in_partitions_read_fails() -> None:
    with pytest.raises(LeakageError) as excinfo:
        _tune(partitions_read=("F1", LOCKED_ID))
    assert "January" in str(excinfo.value)
    with pytest.raises(PartitionError):
        _tune(partitions_read=("F9",))


def test_a_criterion_changed_after_declaration_fails() -> None:
    with pytest.raises(LeakageError) as excinfo:
        _tune(criterion_used=dict(CRITERION, declared_baseline="M-02"))
    assert "criterion_used_hash" in str(excinfo.value)


def test_a_missing_or_unbound_attestation_fails_unconditionally() -> None:
    with pytest.raises(LeakageError) as excinfo:
        _tune(attested_by="")
    assert "attestation" in str(excinfo.value)
    with pytest.raises(LeakageError):
        _tune(attests_criterion_hash=criterion_hash(dict(CRITERION, declared_baseline="M-02")))
    with pytest.raises(LeakageError):
        _tune(run_at=DECLARED_AT)  # the criterion must be declared BEFORE the run


# =======================================================================================
# 7. Selection (R-101) and the refit
# =======================================================================================


def test_selection_refuses_raw_rmse_row_weighting_and_an_unresolved_selection_block() -> None:
    folds = ("F1", "F2", "F3", "F4")
    skill = CandidateScore({"alpha": 0.5}, {f: 0.2 for f in folds}, complexity=1.0)
    rmse = CandidateScore({"alpha": 2.0}, {f: 3.0 for f in folds}, complexity=2.0, metric="rmse")
    assert mean_per_fold_skill(skill, fold_ids=folds) == 0.2
    with pytest.raises(IntegrityError):
        mean_per_fold_skill(rmse, fold_ids=folds)
    with pytest.raises(PartitionError):
        mean_per_fold_skill(skill, fold_ids=folds[:3])
    with pytest.raises(IntegrityError):
        select_configuration([skill], snapshot=SNAPSHOT, fold_ids=folds, weights={"F1": 2.0})
    with pytest.raises(IntegrityError) as excinfo:
        select_configuration([skill], snapshot=SNAPSHOT, fold_ids=folds)
    assert "models.selection" in str(excinfo.value)  # D-124's values are NOT transcribed here


def test_selection_prefers_the_simpler_configuration_within_the_configured_tolerance() -> None:
    folds = ("F1", "F2", "F3", "F4")
    simple = CandidateScore({"alpha": 2.0}, {f: 0.20 for f in folds}, complexity=1.0)
    complex_ = CandidateScore({"alpha": 0.5}, {f: 0.201 for f in folds}, complexity=2.0)
    snapshot = _snapshot(
        models={
            "lstm_fixed_settings": SYNTH_SETTINGS,
            "selection": {"simplicity_margin": 0.05},
            "declared_baseline_per_track": {"all_tracks": "persistence"},
        }
    )
    assert select_configuration([simple, complex_], snapshot=snapshot, fold_ids=folds) is simple
    far = CandidateScore({"alpha": 0.1}, {f: 0.5 for f in folds}, complexity=3.0)
    assert select_configuration([simple, complex_, far], snapshot=snapshot, fold_ids=folds) is far
    assert_refit_unchanged({"alpha": 2.0}, {"alpha": 2.0})
    with pytest.raises(IntegrityError):
        assert_refit_unchanged({"alpha": 2.0}, {"alpha": 0.5})


def test_selection_reads_the_real_transcribed_config_keys() -> None:
    """Regression control (2026-09-25, build-and-test item 3). The reader once expected
    `selection.simplicity_tolerance_fraction` and `selection.declared_baseline`, names no
    governed record gave; the owner's transcription (CR-2026-09-21-RECONCILIATION §2, D-124;
    D-58) wrote `selection.simplicity_margin` and the sibling `declared_baseline_per_track`.
    Every selection test used a synthetic snapshot, so the real file was never read here.
    This test reads it, and pins that the retired names are refused, not silently accepted."""
    yaml = pytest.importorskip("yaml")
    parsed = yaml.safe_load((REPO_ROOT / "configs" / "experiment.yaml").read_text("utf-8"))
    snapshot = dataclasses.replace(SNAPSHOT, experiment=parsed)
    folds = tuple(parsed["models"]["selection"]["folds"])
    assert folds == ("F1", "F2", "F3", "F4")
    only = CandidateScore({"alpha": 1.0}, {f: 0.1 for f in folds}, complexity=1.0)
    assert select_configuration([only], snapshot=snapshot, fold_ids=folds) is only

    retired = _snapshot(
        models={
            "lstm_fixed_settings": SYNTH_SETTINGS,
            "selection": {"simplicity_tolerance_fraction": 0.05, "declared_baseline": "M-01"},
        }
    )
    with pytest.raises(IntegrityError) as excinfo:
        select_configuration([only], snapshot=retired, fold_ids=folds)
    assert "simplicity_margin" in str(excinfo.value)

    no_baseline = _snapshot(
        models={"lstm_fixed_settings": SYNTH_SETTINGS, "selection": {"simplicity_margin": 0.01}}
    )
    with pytest.raises(IntegrityError) as excinfo:
        select_configuration([only], snapshot=no_baseline, fold_ids=folds)
    assert "declared_baseline_per_track" in str(excinfo.value)


# =======================================================================================
# 8. Ablations: five named, four reachable; ABL-HIST48 and ABL-DIFF refusals (R-97)
# =======================================================================================


def test_five_ablations_are_read_from_config_and_a_missing_one_fails() -> None:
    entries = read_ablations(SNAPSHOT)
    assert tuple(e.ablation_id for e in entries) == ABLATION_IDS
    assert sum(e.phase1_reachable for e in entries) == 4
    incomplete = {k: v for k, v in _ablation_entries().items() if k != "ABL-NOSW"}
    with pytest.raises(IntegrityError) as excinfo:
        read_ablations(_snapshot(ablations={"entries": incomplete}))
    assert "ABL-NOSW" in str(excinfo.value)
    with pytest.raises(IntegrityError):
        read_ablations(_snapshot(ablations=TBD_SENTINEL))


def _entry(ablation_id: str, **patch: Any):
    entries = _ablation_entries(**{ablation_id: patch}) if patch else _ablation_entries()
    return next(
        e for e in read_ablations(_snapshot(ablations={"entries": entries}))
        if e.ablation_id == ablation_id
    )


FREEZE_AT = "2026-10-01T00:00:00+00:00"
REGISTERED = {"run_id": "abl-run", "registered_at": "2026-09-20T00:00:00+00:00"}


def test_an_unregistered_ablation_and_one_registered_after_the_freeze_fail() -> None:
    with pytest.raises(IntegrityError) as excinfo:
        assert_ablation_runnable(
            _entry("ABL-NODOY"), phase=1, primary_frozen_hash="h", freeze_at=FREEZE_AT
        )
    assert "TBD" in str(excinfo.value)
    late = _entry("ABL-NODOY", run_id="abl-run", registered_at="2026-10-02T00:00:00+00:00")
    with pytest.raises(IntegrityError) as excinfo:
        assert_ablation_runnable(late, phase=1, primary_frozen_hash="h", freeze_at=FREEZE_AT)
    assert "after results are seen" in str(excinfo.value)
    assert_ablation_runnable(
        _entry("ABL-NODOY", **REGISTERED), phase=1, primary_frozen_hash=None, freeze_at=FREEZE_AT
    )


def test_abl_hist48_refuses_before_the_primary_configuration_is_frozen() -> None:
    entry = _entry("ABL-HIST48", **REGISTERED)
    with pytest.raises(IntegrityError) as excinfo:
        assert_ablation_runnable(entry, phase=1, primary_frozen_hash=None, freeze_at=FREEZE_AT)
    assert "after the primary configuration is frozen" in str(excinfo.value)
    assert_ablation_runnable(entry, phase=1, primary_frozen_hash="h", freeze_at=FREEZE_AT)


def test_abl_diff_refuses_while_no_inverse_exists_naming_d27() -> None:
    entry = _entry("ABL-DIFF", **REGISTERED)
    with pytest.raises(InverseTransformError) as excinfo:
        assert_ablation_runnable(entry, phase=1, primary_frozen_hash="h", freeze_at=FREEZE_AT)
    assert "D-27" in str(excinfo.value)
    assert_ablation_runnable(
        entry, phase=1, primary_frozen_hash="h", freeze_at=FREEZE_AT, inverse_available=True
    )


def test_abl_zenith_is_a_phase_deferral_and_no_promotion_is_checked_by_hash() -> None:
    with pytest.raises(PhaseBoundaryError):
        assert_ablation_runnable(
            _entry("ABL-ZENITH", **REGISTERED), phase=1, primary_frozen_hash="h",
            freeze_at=FREEZE_AT,
        )
    assert_no_promotion("abc", "abc")
    with pytest.raises(IntegrityError):
        assert_no_promotion("abc", "abd")


# =======================================================================================
# 9. The horizon is config-only (R-99)
# =======================================================================================


def test_horizons_are_read_from_config_and_refuse_while_unresolved() -> None:
    assert read_horizons(SNAPSHOT) == (SYNTH_HORIZON,)
    assert resolve_horizon(SNAPSHOT, None) == SYNTH_HORIZON
    with pytest.raises(IntegrityError):
        read_horizons(_snapshot(horizons=TBD_SENTINEL))
    two = _snapshot(horizons=[SYNTH_HORIZON, SYNTH_HORIZON + 3])
    with pytest.raises(IntegrityError):
        resolve_horizon(two, None)  # two entries and no choice: never pick one by convenience
    assert resolve_horizon(two, SYNTH_HORIZON + 3) == SYNTH_HORIZON + 3


def test_input_eligibility_is_arithmetic_on_the_column_step_and_needs_no_code_change() -> None:
    bundle = _bundle(_train_spec("F1"), transform_id="T-F1")
    at_two = eligible_feature_columns(bundle, horizon_hours=SYNTH_HORIZON)
    assert "vtec_lag_1h" not in at_two and "seq_t-1" not in at_two
    assert {"vtec_lag_2h", "f107_safe", "seq_t-3"} <= set(at_two)
    at_one = eligible_feature_columns(bundle, horizon_hours=1)
    assert set(at_one) == set(FEATURES)
    far = eligible_feature_columns(bundle, horizon_hours=SYNTH_HORIZON + 3)
    assert set(far) == {"f107_safe"}
    assert lstm.observable_steps(3, horizon_hours=1) == (0, 3)
    assert lstm.observable_steps(3, horizon_hours=SYNTH_HORIZON) == (0, 2)


def test_no_code_path_in_src_models_branches_on_a_literal_horizon() -> None:
    """R-99's static check: no comparison of a horizon-named value against a constant."""
    for path in sorted(MODELS_DIR.glob("*.py")):
        for node in ast.walk(_ast_of(path)):
            if not isinstance(node, ast.Compare):
                continue
            names = [
                n.id.lower() if isinstance(n, ast.Name) else getattr(n, "attr", "").lower()
                for n in [node.left, *node.comparators]
                if isinstance(n, ast.Name | ast.Attribute)
            ]
            constants = [c for c in [node.left, *node.comparators] if isinstance(c, ast.Constant)]
            if any("horizon" in n for n in names) and any(
                isinstance(c.value, int) and not isinstance(c.value, bool) and c.value > 0
                for c in constants
            ):
                raise AssertionError(f"{path}:{node.lineno} branches on a literal horizon")


# =======================================================================================
# 10. RF importance is diagnostic only (R-100)
# =======================================================================================


def test_the_importance_marker_is_recorded_and_true_is_unrepresentable() -> None:
    figure = random_forest.ImportanceFigure("M-05", False, "fig.png", {"a": 0.5})
    assert figure.authoritative is False
    with pytest.raises(IntegrityError):
        random_forest.ImportanceFigure("M-05", True, "fig.png", {"a": 0.5})


def test_no_importance_score_reaches_the_fit_or_selection_path() -> None:
    """Checked on this unit's own module graph: `feature_importances_` and
    `diagnostic_importance` are referenced only inside `diagnostic_importance` itself."""
    tree = _ast_of(MODELS_DIR / "random_forest.py")
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name != "diagnostic_importance":
            for inner in ast.walk(node):
                if isinstance(inner, ast.Attribute):
                    assert inner.attr != "feature_importances_", node.name
                if isinstance(inner, ast.Name):
                    assert inner.id != "diagnostic_importance", node.name
    for path in (MODELS_DIR / "train.py", REPO_ROOT / "scripts" / "06_train_and_predict.py"):
        assert "importance" not in path.read_text(encoding="utf-8").lower(), path


# =======================================================================================
# 11. M-06: the pin guard PASSES on the frozen pin (D-36) and refuses an absent or
#     commented one; settings from config (FU-1 = C)
# =======================================================================================


@in_fresh_process
def test_the_pin_guard_refuses_an_absent_or_commented_pin_and_reads_the_frozen_one(
    tmp_path: Path,
) -> None:
    """The pin-guard negative controls, re-pointed 2026-09-10 after the owner froze the
    pin at `tensorflow==2.21.0` (D-36, adopted 2026-09-10).

    The refusal is still PROVED, on synthetic requirements files: an absent pin and a
    commented-out pin both raise naming TS-M-01. What changed is the real
    `requirements.txt`, which now carries the frozen pin — asserted here so the guard's
    positive branch is covered against the governed file, not only a synthetic one. No
    `tensorflow` import happens in any branch.
    """
    absent = tmp_path / "absent.txt"
    absent.write_text("numpy==1.26.4\n")
    with pytest.raises(IntegrityError) as excinfo:
        lstm.require_frozen_pin(absent)
    assert "TS-M-01" in str(excinfo.value) and "TBD" in str(excinfo.value)
    commented = tmp_path / "requirements.txt"
    commented.write_text("# tensorflow==2.21.0 (candidate, not frozen)\nnumpy==1.26.4\n")
    with pytest.raises(IntegrityError):
        lstm.require_frozen_pin(commented)
    frozen = tmp_path / "frozen.txt"
    frozen.write_text("numpy==1.26.4\ntensorflow==0.0.0\n")
    assert lstm.require_frozen_pin(frozen) == "tensorflow==0.0.0"
    # the governed file: the owner's frozen pin, read through the same guard
    assert lstm.require_frozen_pin() == "tensorflow==2.21.0"
    assert "tensorflow" not in sys.modules


class _NullBackend:
    def save(self, *, epoch: int, weights: Any) -> str:
        return f"null://{epoch}"

    def load(self, payload_ref: str) -> Any:
        return None


@in_fresh_process
def test_m06_fit_refuses_at_the_guard_before_any_tensorflow_import(tmp_path: Path) -> None:
    """The guard fires BEFORE any TensorFlow import — proved against a synthetic
    requirements file carrying no pin (re-pointed 2026-09-10: the real file now carries
    the owner's frozen `tensorflow==2.21.0`, so the unfrozen state must be injected to
    stay testable). The seed refusal ahead of it is unchanged."""
    unpinned = tmp_path / "requirements.txt"
    unpinned.write_text("numpy==1.26.4\n")
    train = _bundle(_train_spec("F1"), transform_id="T-F1", hours=4)
    score = _bundle(_score_spec("F1"), transform_id="T-F1", hours=2)
    params = lstm.enumerate_lstm_grid(SNAPSHOT)[0]
    seed = sorted(EXPECTED)[0]
    with pytest.raises(SeedError):
        fit_predict(
            "M-06", bundle=train, partition=_p("F1"), snapshot=SNAPSHOT,
            target=_target(_ts(1, 1), _ts(5, 1)), score_bundle=score,
            validation_bundle=score, params=params,
        )
    with pytest.raises(IntegrityError) as excinfo:
        lstm.fit_predict_rows(
            "M-06", bundle=train, score_bundle=score, partition=_p("F1"), snapshot=SNAPSHOT,
            target=_target(_ts(1, 1), _ts(5, 1)), seed=seed, params=params,
            horizon_hours=SYNTH_HORIZON, backend=_NullBackend(),
            validation_bundle=score, requirements_path=unpinned,
        )
    assert "TS-M-01" in str(excinfo.value)
    assert "tensorflow" not in sys.modules
    with pytest.raises(IntegrityError):
        lstm.determinism_check(seed=seed, requirements_path=unpinned)
    with pytest.raises(IntegrityError):
        lstm.build_keras_model(
            params,
            n_features=1,
            window_steps=3,
            settings=SYNTH_SETTINGS,
            requirements_path=unpinned,
        )
    # With the owner's frozen pin the guard PASSES; what happens next is an environment
    # fact, asserted in BOTH supported states so the "no import before the guard" property
    # stays proved either way (G-11, `CR-2026-09-19-GATE-PREP-2`): with the pinned
    # TensorFlow installed (the governed environment) the model builds and the import is
    # observed to have happened ONLY after the guard; without it, the next obstacle is the
    # absent module itself, not a guard failure.
    import importlib.util

    if importlib.util.find_spec("tensorflow") is None:
        with pytest.raises(ModuleNotFoundError):
            lstm.build_keras_model(params, n_features=1, window_steps=3, settings=SYNTH_SETTINGS)
        assert "tensorflow" not in sys.modules
    else:
        model = lstm.build_keras_model(params, n_features=1, window_steps=3, settings=SYNTH_SETTINGS)
        assert model is not None and "tensorflow" in sys.modules
        assert model.name == "m06_compact_direct_lstm"


def test_the_seven_fixed_settings_are_asserted_from_config() -> None:
    settings = read_lstm_fixed_settings(SNAPSHOT)
    assert tuple(settings) == LSTM_FIXED_SETTING_KEYS and len(LSTM_FIXED_SETTING_KEYS) == 8
    assert lstm.fixed_settings(SNAPSHOT) == settings
    for key in LSTM_FIXED_SETTING_KEYS:
        broken = {k: v for k, v in SYNTH_SETTINGS.items() if k != key}
        with pytest.raises(IntegrityError):
            read_lstm_fixed_settings(_snapshot(models={"lstm_fixed_settings": broken}))
    with pytest.raises(IntegrityError):
        read_lstm_fixed_settings(_snapshot(models=TBD_SENTINEL))
    with pytest.raises(IntegrityError):
        lstm.fixed_settings(
            _snapshot(models={"lstm_fixed_settings": dict(SYNTH_SETTINGS, optimizer="SGD")})
        )


# =======================================================================================
# 12. `06`: the receipt controls on a synthetic NON-DEC fixture; the DEC guard refuses
# =======================================================================================


def _payload(partition_id: str = "F1") -> dict[str, Any]:
    return {"model_id": "M-06", "seed": None, "partition_id": partition_id, "rows": [{"y_hat": 1}]}


def test_receipt_is_written_durably_and_matches_the_file_as_written(tmp_path: Path) -> None:
    prediction = tmp_path / "pred.json"
    prediction.write_text(json.dumps(_payload()))
    receipt_path = tmp_path / "pred.receipt.json"
    receipt = write_prediction_hash_receipt(
        prediction, run_id="r", partition_id="F1", receipt_path=receipt_path
    )
    assert receipt_path.is_file() and not receipt_path.with_suffix(".json.tmp").exists()
    assert [f.name for f in dataclasses.fields(PredictionHashReceipt)] == [
        "prediction_path", "sha256", "recorded_at_utc", "run_id", "partition_id",
    ]
    assert_locked_exit_allowed(prediction, receipt_path=receipt_path, registry_appended=True)
    with pytest.raises(LockedTestError):  # write-once: a second receipt is refused
        write_prediction_hash_receipt(
            prediction, run_id="r", partition_id="F1", receipt_path=receipt_path
        )


def test_no_receipt_hash_mismatch_and_failed_append_each_raise_in_06(tmp_path: Path) -> None:
    prediction = tmp_path / "pred.json"
    prediction.write_text(json.dumps(_payload()))
    receipt_path = tmp_path / "pred.receipt.json"
    with pytest.raises(LockedTestError) as excinfo:  # no receipt
        assert_locked_exit_allowed(prediction, receipt_path=receipt_path, registry_appended=True)
    assert "no prediction-hash receipt" in str(excinfo.value)
    write_prediction_hash_receipt(
        prediction, run_id="r", partition_id="F1", receipt_path=receipt_path
    )
    with pytest.raises(LockedTestError) as excinfo:  # append did not succeed
        assert_locked_exit_allowed(prediction, receipt_path=receipt_path, registry_appended=False)
    assert "column 18" in str(excinfo.value)
    prediction.write_text(json.dumps(_payload()) + " ")  # the file is no longer what was hashed
    with pytest.raises(LockedTestError) as excinfo:
        assert_locked_exit_allowed(prediction, receipt_path=receipt_path, registry_appended=True)
    assert "does not match the receipt" in str(excinfo.value)
    assert_locked_exit_allowed(
        tmp_path / "absent.json", receipt_path=receipt_path, registry_appended=False
    )  # nothing on disk -> nothing to refuse


def test_06s_locked_write_sequence_refuses_to_exit_when_the_append_fails(tmp_path: Path) -> None:
    script = _load_script()
    prediction = tmp_path / "F1" / "M-06_confirmatory.json"
    receipt = tmp_path / "F1" / "M-06_confirmatory.receipt.json"
    seen: list[str] = []

    def ok(sha256: str) -> bool:
        seen.append(sha256)
        return True

    script._finish_locked_write(
        prediction_path=prediction, payload=_payload(), run_id="r", receipt_path=receipt,
        append_row=ok,
    )
    assert len(seen) == 1 and receipt.is_file()
    with pytest.raises(LockedTestError):  # write-once: the same path is never rewritten
        script._write_prediction_once(prediction, _payload())
    prediction2 = tmp_path / "F2" / "M-06_confirmatory.json"
    receipt2 = tmp_path / "F2" / "M-06_confirmatory.receipt.json"
    with pytest.raises(LockedTestError) as excinfo:
        script._finish_locked_write(
            prediction_path=prediction2, payload=_payload("F2"), run_id="r",
            receipt_path=receipt2, append_row=lambda sha: False,
        )
    assert "refuses to exit" in str(excinfo.value)
    prediction3 = tmp_path / "F3" / "M-06_confirmatory.json"
    receipt3 = tmp_path / "F3" / "M-06_confirmatory.receipt.json"

    def failing(sha256: str) -> bool:
        raise IntegrityError("registry", "append failed")

    with pytest.raises(LockedTestError):
        script._finish_locked_write(
            prediction_path=prediction3, payload=_payload("F3"), run_id="r",
            receipt_path=receipt3, append_row=failing,
        )
    assert receipt3.is_file(), "the receipt landed; the append did not — 06 aborted, not 07"


def test_prediction_hash_is_the_eighteenth_registry_column_and_06_asserts_it() -> None:
    assert REGISTRY_COLUMNS.index("prediction_hash") + 1 == 18
    script = _load_script()
    script._assert_registry_column_18()
    assert script.WRITER_ROLE == "train"


def test_the_dec_path_is_unreachable_without_the_g05_guard_and_the_three_arguments() -> None:
    script = _load_script()
    with pytest.raises(SystemExit):
        script._parse_args(["--config", "configs", "--partition", LOCKED_ID])
    args = script._parse_args(["--config", "configs"])
    assert LOCKED_ID not in args.partitions and set(args.partitions) == set(PARTITION_IDS) - {
        LOCKED_ID
    }
    with pytest.raises(LockedTestError):  # the one door refuses before any read
        materialise_locked_partition(
            synthetic_snapshot(), g05_signature=None, loader=lambda p: RecordFrame([]),
            partitions=PARTITIONS,
        )
    with pytest.raises(IntegrityError) as excinfo:  # the selected grid point is not defaulted
        script._selected_params(_snapshot(models={"lstm_fixed_settings": SYNTH_SETTINGS}), "M-04")
    assert "models.selected" in str(excinfo.value)
    assert script._selected_params(SNAPSHOT, "M-01") is None
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    # compared against the guard's own constant, never spelled here (R-28's one-door scan)
    from src.data.locked_test import RESTRICTED_ROOT

    assert RESTRICTED_ROOT not in text, "06 never names the restricted root"
    for path in sorted(MODELS_DIR.glob("*.py")):
        assert RESTRICTED_ROOT not in path.read_text(encoding="utf-8"), path
    assert "prior_period_exposure" not in text.replace(
        "`prior_period_exposure` is NOT written here", ""
    ), "06 writes no prior_period_exposure value (R-102a deviation box)"


def test_fixture_scale_params_come_from_the_scope_never_models_selected() -> None:
    """CR-2026-09-25: the fixture-scale grid point is the scope's apparatus constant.

    Four limbs: M-01..M-03 stay `None`; a declared track resolves EVEN THOUGH this
    snapshot carries no `models.selected` at all (independence from the governed field is
    the point — the circular refusal is broken); an undeclared track REFUSES naming the
    field, never defaulting (TE 18.3); an off-grid point refuses at `assert_in_grid`
    (the apparatus picks among D-121's members, never invents one)."""
    from types import SimpleNamespace

    script = _load_script()
    scope = SimpleNamespace(
        path=Path("identity_declaration.yaml"),
        apparatus_hyperparameters={
            "ridge": {
                "params": {"alpha": 0.5},
                "reason": "fixture-scale plumbing point (test apparatus)",
                "citation": "D-905",
            }
        },
    )
    assert script._apparatus_params(scope, SNAPSHOT, "M-01") is None
    assert script._apparatus_params(scope, SNAPSHOT, "M-04") == {"alpha": 0.5}
    # D-121 `fixed` entries complete the point from the ONE grid in config — the scope
    # declares axes only, and the completed point must be a full grid member.
    rf_scope = SimpleNamespace(
        path=Path("identity_declaration.yaml"),
        apparatus_hyperparameters={
            "random_forest": {
                "params": {"n_estimators": 3, "max_depth": 2, "min_samples_leaf": 1},
                "reason": "axes-only point (test apparatus)",
                "citation": "D-905",
            }
        },
    )
    resolved = script._apparatus_params(rf_scope, SNAPSHOT, "M-05")
    assert resolved == {
        "n_estimators": 3, "max_depth": 2, "min_samples_leaf": 1, "max_features": "sqrt",
    }
    contradicting = SimpleNamespace(
        path=Path("identity_declaration.yaml"),
        apparatus_hyperparameters={
            "random_forest": {
                "params": {
                    "n_estimators": 3, "max_depth": 2, "min_samples_leaf": 1,
                    "max_features": "log2",  # contradicts D-121's fixed value
                },
                "reason": "r",
                "citation": "D-905",
            }
        },
    )
    with pytest.raises(IntegrityError, match="not a member"):
        script._apparatus_params(contradicting, SNAPSHOT, "M-05")
    with pytest.raises(IntegrityError) as excinfo:
        script._apparatus_params(scope, SNAPSHOT, "M-05")
    assert "apparatus_hyperparameters.random_forest" in str(excinfo.value)
    assert "models.selected" in str(excinfo.value), "the refusal teaches the boundary"
    off_grid = SimpleNamespace(
        path=Path("identity_declaration.yaml"),
        apparatus_hyperparameters={
            "ridge": {"params": {"alpha": 7.5}, "reason": "r", "citation": "D-905"}
        },
    )
    with pytest.raises(IntegrityError, match="not a member"):
        script._apparatus_params(off_grid, SNAPSHOT, "M-04")


# =======================================================================================
# 13. The DEC iteration scores the frame the one door RETURNED (R-102a; SD-M-04; W-12)
# =======================================================================================

SYNTH_SIGNATURE = "synthetic-g05-signature-for-the-fixture-year"
SYNTH_LOCKED_OFFSET = 1000.0  # marks values that exist ONLY in the loader's frame


def _signed_snapshot():
    """A synthetic `gates.G-05` record that a SYNTHETIC signature verifies against — over the
    fixture year only; the real `configs/data.yaml` carries no G-05 record."""
    digest = hashlib.sha256(SYNTH_SIGNATURE.encode("utf-8")).hexdigest()
    gates = {"G-05": {"status": "signed", "signature_sha256": digest, "decision": "D-synthetic"}}
    snapshot = synthetic_snapshot(
        data={"gates": gates},
        experiment={
            "horizons": [SYNTH_HORIZON],
            "grids": SYNTH_GRIDS,
            "models": dict(SYNTH_MODELS),
            "ablations": {"entries": _ablation_entries()},
        },
    )
    return dataclasses.replace(snapshot, seeds=dict(SYNTH_SEEDS))


def _locked_month_frame() -> RecordFrame:
    """What the fake one-door loader returns: two days of the fixture year's locked month with
    values offset so they cannot be mistaken for the released January–November target's."""
    locked = _p(LOCKED_ID)
    start, _ = validation_month_range(locked)
    rows = []
    stamp = start
    while stamp < start + dt.timedelta(hours=48):
        for station in STATIONS:
            rows.append(
                {
                    "interval_start_utc": stamp.isoformat(),
                    "station_id": station,
                    "vtec_tecu": _value(station, stamp) + SYNTH_LOCKED_OFFSET,
                }
            )
        stamp += dt.timedelta(hours=1)
    return RecordFrame(rows)


def test_the_dec_iteration_scores_the_frame_the_one_door_returned_not_the_released_target(
) -> None:
    """The frame `materialise_locked_partition` returns (loader output, embargo excluded and
    counted) is what reaches `fit_predict` on the DEC branch; the pre-loop released target —
    January–November, no locked-month rows — is not consulted."""
    script = _load_script()
    snapshot = _signed_snapshot()
    locked = _p(LOCKED_ID)
    released_target = _target(_ts(1, 1), _ts(12, 1))  # January–November only, as 06 loads it
    loader_calls: list[str] = []

    def fake_loader(partition) -> RecordFrame:
        loader_calls.append(partition.partition_id)
        return _locked_month_frame()

    loaded = script._locked_target(
        snapshot,
        g05_signature=SYNTH_SIGNATURE,
        loader=fake_loader,
        partitions=PARTITIONS,
        released_target=released_target,
    )
    assert loader_calls == [LOCKED_ID], "the loader is called once, for the locked partition"
    assert loaded is not released_target
    assert loaded.attrs["partition_id"] == LOCKED_ID
    assert loaded.attrs["excluded_embargo_rows"] == locked.embargo_hours * len(STATIONS)
    from src.models.train import target_series

    series = target_series(loaded)
    assert series and all(v > SYNTH_LOCKED_OFFSET for v in series.values())
    assert not any(key in target_series(released_target) for key in series), (
        "the released target carries no locked-month row; the loaded frame is a different frame"
    )
    # Score the DEC bundle with the LOADED frame: persistence reads the loader's offset values.
    start, _ = validation_month_range(locked)
    dec_score = _bundle(
        _score_spec(LOCKED_ID),
        transform_id=expected_transform_id(locked),
        start=start + dt.timedelta(hours=locked.embargo_hours + 12),
        hours=2,
    )
    assert_stamp_match(dec_score, locked)
    prediction = fit_predict(
        "M-01", bundle=dec_score, partition=locked, snapshot=snapshot, target=loaded
    )
    row = records_of(prediction.frame)[0]
    origin = dt.datetime.fromisoformat(row["interval_start_utc"]) - dt.timedelta(
        hours=SYNTH_HORIZON
    )
    assert row["y_hat"] == _value("S1", origin) + SYNTH_LOCKED_OFFSET
    assert frame_attrs(prediction.frame)["missing_source_values"] == 0
    # The same scoring with the pre-loop target would have had NOTHING to read for the month.
    with_released = fit_predict(
        "M-01", bundle=dec_score, partition=locked, snapshot=snapshot, target=released_target
    )
    assert all(r["y_hat"] is None for r in records_of(with_released.frame))


def test_a_dec_iteration_handed_the_pre_loop_target_is_refused() -> None:
    """The negative control: a loader that hands back the released target object itself is
    refused by identity, as is a loader returning nothing and an unverified signature."""
    script = _load_script()
    snapshot = _signed_snapshot()
    released_target = _target(_ts(1, 1), _ts(12, 1))
    with pytest.raises(LockedTestError) as excinfo:
        script._locked_target(
            snapshot,
            g05_signature=SYNTH_SIGNATURE,
            loader=lambda partition: released_target,
            partitions=PARTITIONS,
            released_target=released_target,
        )
    assert "pre-loop released target" in str(excinfo.value)
    with pytest.raises(LockedTestError):  # the guard refuses BEFORE the loader runs
        script._locked_target(
            snapshot,
            g05_signature="not-the-signature",
            loader=lambda partition: _locked_month_frame(),
            partitions=PARTITIONS,
            released_target=released_target,
        )
    with pytest.raises(LockedTestError):
        script._locked_target(
            snapshot,
            g05_signature=None,
            loader=lambda partition: _locked_month_frame(),
            partitions=PARTITIONS,
            released_target=released_target,
        )
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "target=partition_target" in text and "target=target" not in text, (
        "no scoring call in 06 consumes the pre-loop object directly"
    )


# =======================================================================================
# 14. December is INFERENCE-ONLY: the fit/predict split and the validation bundle
#     (Recommendation 5, owner ruling 2026-09-20)
# =======================================================================================


def _refit_train_bundle() -> FeatureBundle:
    """REFIT's train bundle — January-November, carrying REFIT's own transform."""
    return _bundle(_train_spec(REFIT_ID), transform_id=transform_id_for(REFIT_ID), hours=48)


def _dec_score_bundle(hours: int = 2) -> FeatureBundle:
    """The December score bundle: DEC's rows under REFIT's transform (R-74's one apply)."""
    locked = _p(LOCKED_ID)
    start, _ = validation_month_range(locked)
    return _bundle(
        _score_spec(LOCKED_ID),
        transform_id=expected_transform_id(locked),
        start=start + dt.timedelta(hours=locked.embargo_hours),
        hours=hours,
    )


@pytest.mark.parametrize("model_id", list(FITTED_MODEL_IDS))
def test_no_fitted_family_may_be_fitted_on_the_locked_partition(model_id: str) -> None:
    """Negative control (a): a `(REFIT train, DEC score)` pair pushed through the FIT
    surface raises, for every fitted family.

    Before the ruling, `06`'s locked branch called `fit_predict` with exactly this pair, so
    December supplied the labels that drove M-06's per-epoch validation RMSE, its
    `should_stop` decision and its restored checkpoint. The guard makes the violation
    impossible rather than merely absent.
    """
    snapshot = _signed_snapshot()
    params = _grid_point_for(model_id)
    seed = sorted(EXPECTED)[0] if model_id in ("M-06",) else None
    with pytest.raises(LeakageError) as excinfo:
        fit_predict(
            model_id,
            bundle=_refit_train_bundle(),
            partition=_p(LOCKED_ID),
            snapshot=snapshot,
            target=_target(_ts(12, 2), _ts(12, 3)),
            score_bundle=_dec_score_bundle(),
            seed=seed,
            params=params,
        )
    message = str(excinfo.value)
    assert "INFERENCE-ONLY" in message and LOCKED_ID in message
    assert "Vision 8.3" in message and REFIT_ID in message


def _grid_point_for(model_id: str) -> dict[str, Any] | None:
    track = next((t for t, mid in GRID_TRACKS.items() if mid == model_id), None)
    return None if track is None else dict(enumerate_grid(SNAPSHOT, track)[0])


def test_the_two_unfitted_families_are_still_reachable_on_the_locked_partition() -> None:
    """The must-not-fire case: M-01 and M-02 carry no fitted state, so the inference-only
    rule has nothing to refuse — they are recomputed from the locked target series."""
    for model_id in ("M-01", "M-02"):
        assert model_id not in FITTED_MODEL_IDS
        assert_not_locked_fit(model_id, _p(LOCKED_ID))  # must not raise
    for model_id in FITTED_MODEL_IDS:
        for pid in FOLD_PARTITION_IDS + (REFIT_ID,):
            assert_not_locked_fit(model_id, _p(pid))  # must not raise off the locked month


def test_a_december_bundle_offered_as_the_validation_set_is_refused() -> None:
    """Negative control (b): the validation bundle is named, constrained and never inferred.

    A `DEC` bundle, a `REFIT` bundle, a train-role frame and an unnamed set for M-06 on a
    fold are each refused — the four ways the scored frame could have become the validation
    frame again.
    """
    train = _bundle(_train_spec("F1"), transform_id="T-F1", hours=4)
    score = _bundle(_score_spec("F1"), transform_id="T-F1", hours=2)
    params = _grid_point_for("M-06")
    seed = sorted(EXPECTED)[0]
    with pytest.raises(LeakageError) as excinfo:
        fit_predict(
            "M-06", bundle=train, partition=_p("F1"), snapshot=SNAPSHOT,
            target=_target(_ts(1, 1), _ts(5, 1)), score_bundle=score,
            validation_bundle=_dec_score_bundle(), seed=seed, params=params,
        )
    assert LOCKED_ID in str(excinfo.value) and "Vision 8.3" in str(excinfo.value)
    # a non-fold frozen partition
    with pytest.raises(LeakageError):
        assert_validation_bundle(
            _bundle(_train_spec(REFIT_ID), transform_id=transform_id_for(REFIT_ID)),
            model_id="M-06", partition=_p("F1"),
        )
    # a train-role frame: in-sample error cannot stop an epoch loop honestly
    with pytest.raises(LeakageError) as excinfo:
        assert_validation_bundle(train, model_id="M-06", partition=_p("F1"))
    assert "score-role" in str(excinfo.value)
    # the refit selects nothing, so a validation bundle there is refused
    with pytest.raises(LeakageError) as excinfo:
        assert_validation_bundle(score, model_id="M-06", partition=_p(REFIT_ID))
    assert REFIT_EPOCH_RULE_ID in str(excinfo.value)
    # M-06 on a fold with no validation bundle named at all
    with pytest.raises(IntegrityError) as excinfo:
        assert_validation_bundle(None, model_id="M-06", partition=_p("F1"))
    assert "no validation_bundle was named" in str(excinfo.value)
    # the must-not-fire cases: the fold's own score bundle, and the refit with none
    assert_validation_bundle(score, model_id="M-06", partition=_p("F1"))
    assert_validation_bundle(None, model_id="M-06", partition=_p(REFIT_ID))
    assert_validation_bundle(None, model_id="M-01", partition=_p("F1"))


def test_the_refit_epoch_count_is_a_frozen_rule_read_from_config() -> None:
    """The VALUE cannot exist until the folds have run, so the pipeline refuses rather than
    defaulting one; the RULE identifier is asserted, not assumed."""
    assert read_refit_epochs(SNAPSHOT) == SYNTH_REFIT["epochs"]
    with pytest.raises(IntegrityError) as excinfo:
        read_refit_epochs(
            _snapshot(models=dict(SYNTH_MODELS, refit={
                "rule": REFIT_EPOCH_RULE_ID, "epochs": TBD_SENTINEL,
            }))
        )
    assert "TBD" in str(excinfo.value) and REFIT_EPOCH_RULE_ID in str(excinfo.value)
    with pytest.raises(IntegrityError) as excinfo:  # a different rule is not implemented here
        read_refit_epochs(
            _snapshot(models=dict(SYNTH_MODELS, refit={"rule": "last_epoch", "epochs": 3}))
        )
    assert REFIT_EPOCH_RULE_ID in str(excinfo.value)
    with pytest.raises(IntegrityError):  # the block absent entirely
        read_refit_epochs(_snapshot(models={"lstm_fixed_settings": SYNTH_SETTINGS}))


def test_persistence_history_augments_only_m01_m02_and_only_with_all_three_inputs(
    monkeypatch,
) -> None:
    """D-28 option (b) / D-68 wiring (2026-09-24): `_persistence_history_augmented_target`
    is the thin orchestration layer between script 06 and
    `src.data.locked_test.read_persistence_history_lookup` (already fully tested in
    isolation, `tests/test_locked_test_guard.py`). This test proves the WIRING, not the
    mechanism's own 5 conditions again: (a) a non-M-01/M-02 model_id is untouched and the
    lookup is never called; (b) M-01/M-02 WITH all three inputs get an augmented frame
    carrying the extra rows; (c) M-01/M-02 with any input missing raises rather than
    silently returning the unaugmented frame."""
    from src.data.locked_test import RESTRICTED_ROOT

    restricted_path = Path(RESTRICTED_ROOT)  # never a literal (R-28: one door)
    script = _load_script()
    base_target = RecordFrame(
        [{"interval_start_utc": "2022-12-02T00:00:00Z", "station_id": "BSHM", "vtec_tecu": 1.0}]
    )
    calls: list[str] = []
    seen_run_ids: list[str] = []

    def fake_lookup(
        snapshot, *, model_id, run_id, g05_signature, path, loader, registry, now=None
    ):
        calls.append(model_id)
        seen_run_ids.append(run_id)
        return {
            (
                "BSHM",
                dt.datetime(2022, 12, 1, 5, tzinfo=dt.timezone.utc),
            ): 9.5
        }

    monkeypatch.setattr(script, "read_persistence_history_lookup", fake_lookup)

    # (a) must-not-fire: a non-caller model_id is untouched, lookup never invoked.
    untouched = script._persistence_history_augmented_target(
        locked_target=base_target,
        model_id="M-03",
        snapshot=_signed_snapshot(),
        run_id="wiring-test-run",
        g05_signature="sig",
        locked_input=restricted_path,
        access_log=Path("registry.jsonl"),
    )
    assert untouched is base_target
    assert calls == [], "the lookup must never be invoked for a non-M-01/M-02 model_id"

    # (b) positive: M-01 with all three inputs gets the augmented frame.
    augmented = script._persistence_history_augmented_target(
        locked_target=base_target,
        model_id="M-01",
        snapshot=_signed_snapshot(),
        run_id="wiring-test-run",
        g05_signature="sig",
        locked_input=restricted_path,
        access_log=Path("registry.jsonl"),
    )
    assert calls == ["M-01"]
    # Rec 10 (GOV-2026-09-24-BT-01): the wiring threads the governed run's own id through.
    assert seen_run_ids == ["wiring-test-run"]
    rows = records_of(augmented)
    assert len(rows) == 2, "expected the original row plus the one 1-Dec lookup row"
    extra = [r for r in rows if r["interval_start_utc"].startswith("2022-12-01")]
    assert len(extra) == 1 and extra[0]["vtec_tecu"] == 9.5
    original = [r for r in rows if r["interval_start_utc"].startswith("2022-12-02")]
    assert len(original) == 1 and original[0]["vtec_tecu"] == 1.0

    # (c) negative: M-02 with any of the three missing raises, never silently unaugmented.
    for missing_kwargs in (
        {"g05_signature": None},
        {"locked_input": None},
        {"access_log": None},
    ):
        kwargs = {
            "run_id": "wiring-test-run",
            "g05_signature": "sig",
            "locked_input": restricted_path,
            "access_log": Path("registry.jsonl"),
        }
        kwargs.update(missing_kwargs)
        with pytest.raises(LockedTestError) as excinfo:
            script._persistence_history_augmented_target(
                locked_target=base_target,
                model_id="M-02",
                snapshot=_signed_snapshot(),
                **kwargs,
            )
        assert "incomplete" in str(excinfo.value)

    # Rec 10 second limb: an absent run_id refuses for M-01/M-02 (attribution by key,
    # never by timestamp correlation), while a non-caller family is still untouched.
    with pytest.raises(LockedTestError) as excinfo:
        script._persistence_history_augmented_target(
            locked_target=base_target,
            model_id="M-02",
            snapshot=_signed_snapshot(),
            run_id=None,
            g05_signature="sig",
            locked_input=restricted_path,
            access_log=Path("registry.jsonl"),
        )
    assert "run_id" in str(excinfo.value)


def test_the_dec_iteration_with_no_persisted_refit_model_raises_rather_than_fitting(
    tmp_path: Path,
) -> None:
    """Negative control (c): an absent persisted model is a refusal, never a silent refit.

    `06`'s locked branch loads the REFIT model for every fitted family. With none on disk it
    raises `LockedTestError` naming the fallback it will not take — a fit reached from the
    locked branch is December in the training loop.
    """
    with pytest.raises(LockedTestError) as excinfo:
        load_fitted_model(tmp_path / "absent.fitted_record.json")
    assert "never falls back to fitting" in str(excinfo.value)
    script = _load_script()
    snapshot = _signed_snapshot()
    with pytest.raises(LockedTestError):
        script._locked_predictions(
            snapshot=snapshot,
            partition=_p(LOCKED_ID),
            train_bundle=_refit_train_bundle(),
            score_bundle=_dec_score_bundle(),
            locked_target=_locked_month_frame(),
            horizon=SYNTH_HORIZON,
            expected_seeds=EXPECTED,
            models_root=tmp_path / "empty",
        )


def test_a_tampered_persisted_model_fails_the_hash_check(tmp_path: Path) -> None:
    """The persisted model is hashed as written and re-verified before it predicts: the
    weights December is scored with are the weights January-November produced."""
    record = FittedModelRecord(
        model_id="M-03", seed=None, fitted_partition_id=REFIT_ID, transform_id="T-REFIT",
        payload_ref=str(tmp_path / "M-03.fitted.json"), payload_sha256="0" * 64,
        fitted_at_utc="2026-09-20T00:00:00+00:00", hyperparameters={}, attrs={},
    )
    with pytest.raises(IntegrityError) as excinfo:  # absent payload
        assert_fitted_payload_unchanged(record)
    assert "is absent" in str(excinfo.value)
    Path(record.payload_ref).write_text("{}", encoding="utf-8")
    with pytest.raises(IntegrityError) as excinfo:
        assert_fitted_payload_unchanged(record)
    assert "does not match the fitted-model record" in str(excinfo.value)


def test_a_state_no_governed_format_can_persist_refuses_instead_of_pickling(
    tmp_path: Path,
) -> None:
    """`JsonStateBackend` serves the families whose fitted state is JSON-serialisable and
    refuses the rest BY NAME: choosing a binary format for a fitted estimator or for Keras
    weights is a governed decision (TS-M-01), not an implementer's."""
    backend = JsonStateBackend(tmp_path)
    with pytest.raises(IntegrityError) as excinfo:
        backend.save_state(model_id="M-04", seed=None, state={"estimator": object()})
    assert "governed choice" in str(excinfo.value) and "TS-M-01" in str(excinfo.value)
    ref, digest = backend.save_state(model_id="M-03", seed=None, state={"entries": []})
    assert Path(ref).is_file() and len(digest) == 64
    assert backend.load_state(ref) == {"entries": []}
    with pytest.raises(IntegrityError):  # write-once
        backend.save_state(model_id="M-03", seed=None, state={"entries": []})


# =======================================================================================
# 15. The G-06 path EXECUTES: refit -> persist -> locked load -> predict -> receipt
#     (Recommendation 6, option 2) — synthetic signature, synthetic December fixture
# =======================================================================================


def test_the_locked_path_runs_end_to_end_on_synthetic_december_and_leaves_a_receipt(
    tmp_path: Path,
) -> None:
    """The success control the locked path never had.

    Every earlier `DEC` test asserted only that the path was UNREACHABLE or that it refused
    a substituted target. Both limbs of Recommendation 6's defect are exercised here:

    * the December score bundle now HAS a producer (`05 --partition DEC`, behind the same
      G-05 signature guard) — here it is synthesised directly, standing in for that output;
    * the locked iteration never looks up a training label against a December frame, because
      it LOADS the model fitted on `REFIT` and only predicts.

    No real December data, no real signature: the G-05 record is synthetic and verifies a
    synthetic signature over the fixture year, and the December frame is generated by
    `_locked_month_frame` with an offset that marks it as the loader's.
    """
    script = _load_script()
    snapshot = _signed_snapshot()
    locked = _p(LOCKED_ID)
    models_root = tmp_path / "models"
    backend = JsonStateBackend(models_root)
    released_target = _target(_ts(1, 1), _ts(12, 1))  # January–November, as 06 loads it

    # 1. REFIT: fit on January-November and PERSIST, hashed. Nothing is scored here.
    refit_train = _refit_train_bundle()
    record_path = script._fitted_record_path(models_root, "M-03", None)
    record = fit_and_persist(
        "M-03",
        bundle=refit_train,
        partition=_p(REFIT_ID),
        snapshot=snapshot,
        target=released_target,
        backend=backend,
        record_path=record_path,
        validation_bundle=None,  # the refit selects nothing
        horizon_hours=SYNTH_HORIZON,
    )
    assert record.fitted_partition_id == REFIT_ID
    assert Path(record.payload_ref).is_file() and len(record.payload_sha256) == 64
    assert record_path.is_file(), "the fitted-model record lands beside the payload"
    with pytest.raises(IntegrityError):  # write-once: a refit is never silently redone
        fit_and_persist(
            "M-03", bundle=refit_train, partition=_p(REFIT_ID), snapshot=snapshot,
            target=released_target, backend=JsonStateBackend(models_root),
            record_path=record_path, horizon_hours=SYNTH_HORIZON,
        )

    # 2. The one door: the December target is the frame `open_restricted` returned.
    loaded = script._locked_target(
        snapshot,
        g05_signature=SYNTH_SIGNATURE,
        loader=lambda partition: _locked_month_frame(),
        partitions=PARTITIONS,
        released_target=released_target,
    )
    assert loaded is not released_target

    # 3. DEC: LOAD the persisted model and PREDICT. No fit happens on this path.
    dec_score = _dec_score_bundle(hours=2)
    assert_stamp_match(dec_score, locked)  # R-90, before every scoring path
    reloaded = load_fitted_model(record_path)
    prediction = predict_from_fitted(
        reloaded,
        score_bundle=dec_score,
        partition=locked,
        snapshot=snapshot,
        backend=JsonStateBackend(models_root),
        target=loaded,
        horizon_hours=SYNTH_HORIZON,
    )
    assert prediction.partition_id == LOCKED_ID
    rows = records_of(prediction.frame)
    assert len(rows) == 2 * len(STATIONS)
    assert all(row["y_hat"] is not None for row in rows), "every locked row is answered"
    attrs = frame_attrs(prediction.frame)
    assert attrs["inference_only"] is True
    assert attrs["fitted_model_partition_id"] == REFIT_ID
    assert attrs["fitted_model_sha256"] == record.payload_sha256
    assert attrs["missing_climatology_keys"] == 0

    # 4. The one-shot write: prediction file, hash-as-written, durable receipt, exit check.
    prediction_path = tmp_path / LOCKED_ID / "M-03_locked.json"
    receipt_path = tmp_path / LOCKED_ID / "M-03_locked.receipt.json"
    hashes: list[str] = []
    script._finish_locked_write(
        prediction_path=prediction_path,
        payload=script._prediction_payload(prediction, horizon_hours=SYNTH_HORIZON),
        run_id="synthetic-locked-run",
        receipt_path=receipt_path,
        append_row=lambda sha256: bool(hashes.append(sha256)) or True,
    )
    assert prediction_path.is_file(), "the locked prediction file is produced"
    assert receipt_path.is_file(), "and its receipt lands durably"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["partition_id"] == LOCKED_ID and receipt["sha256"] == hashes[0]
    assert_locked_exit_allowed(
        prediction_path, receipt_path=receipt_path, registry_appended=True
    )  # the receipt VERIFIES against the file as written


def test_script_05_has_a_guarded_dec_branch_that_refuses_without_the_signature() -> None:
    """Recommendation 6 limb (a): `05 --partition DEC` now exists and is guarded.

    The December score bundle `06` demands had NO producer — `05` refused `DEC` by argparse,
    so `load_bundle` could only ever raise "bundle is missing". The branch is now present and
    enters through the same `materialise_locked_partition` guard, and BOTH refusal controls
    are kept: `05` refuses without a verifying signature, and `06`'s locked path still
    refuses a substituted target.
    """
    source = (REPO_ROOT / "scripts" / "05_build_features_and_splits.py").read_text("utf-8")
    assert "materialise_locked_partition(" in source
    assert "open_restricted(" in source
    assert 'purpose="locked_evaluation"' in source
    assert "--partition DEC requires --g05-signature" in source
    from src.data.locked_test import RESTRICTED_ROOT

    assert RESTRICTED_ROOT not in source, "05 never names the restricted root"

    spec = importlib.util.spec_from_file_location(
        "script05", REPO_ROOT / "scripts" / "05_build_features_and_splits.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    with pytest.raises(SystemExit):  # DEC without the three locked-path arguments
        module._parse_args(["--config", "configs", "--partition", LOCKED_ID])
    with pytest.raises(SystemExit):  # DEC without REFIT in the same run: no transform to apply
        module._parse_args(
            [
                "--config", "configs", "--partition", LOCKED_ID,
                "--g05-signature", "sig", "--locked-input", "x.jsonl",
                "--locked-authorization", "auth",
            ]
        )
    args = module._parse_args(["--config", "configs"])
    assert LOCKED_ID not in args.partitions
    ok = module._parse_args(
        [
            "--config", "configs", "--partition", REFIT_ID, "--partition", LOCKED_ID,
            "--g05-signature", "sig", "--locked-input", "x.jsonl",
            "--locked-authorization", "auth",
        ]
    )
    assert set(ok.partitions) == {REFIT_ID, LOCKED_ID}
    # and the branch itself refuses when the signature does not verify — before any read
    with pytest.raises(LockedTestError):
        module._build_locked_score_bundle(
            args=ok,
            snapshot=_signed_snapshot(),
            partitions=PARTITIONS,
            refit_transform=object(),
            common={},
            out_root=REPO_ROOT / "artifacts" / "unused",
            run_id="r",
            access_log=REPO_ROOT / "artifacts" / "unused" / "access.jsonl",
        )
