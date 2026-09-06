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
fits are unrun (scikit-learn not installable here) and M-06's Keras path is unexecutable
until the pin is frozen. Smoke evidence only on the interpreter used here.

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
    GRID_TRACKS,
    LSTM_FIXED_SETTING_KEYS,
    MODEL_IDS,
    CandidateScore,
    Prediction,
    PredictionHashReceipt,
    TuningRecord,
    assert_ablation_runnable,
    assert_grid_content,
    assert_grid_unchanged,
    assert_in_grid,
    assert_locked_exit_allowed,
    assert_no_promotion,
    assert_refit_unchanged,
    assert_stamp_match,
    criterion_hash,
    eligible_feature_columns,
    enumerate_grid,
    expected_transform_id,
    fit_predict,
    grid_hash,
    mean_per_fold_skill,
    pinned_requirement,
    read_ablations,
    read_horizons,
    read_lstm_fixed_settings,
    record_tuning,
    resolve_horizon,
    select_configuration,
    three_seed_mean,
    write_prediction_hash_receipt,
)

UTC = dt.UTC
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
        "models": {"lstm_fixed_settings": SYNTH_SETTINGS},
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
    assert records_of(prediction.frame)[0]["y_hat"] is None
    with pytest.raises(IntegrityError):
        fit_predict(
            "M-01", bundle=score, partition=_p("F1"), snapshot=SNAPSHOT, target=target,
            params={"alpha": 1},
        )


def test_climatology_is_fitted_on_the_training_range_and_predicts_station_month_hour() -> None:
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
    # the validation month (April) has no (station, month=4, hour) key in a Jan-only fit:
    assert attrs["missing_climatology_keys"] == 3 * len(STATIONS)


def test_climatology_fitted_across_the_whole_year_fails_the_r98_control() -> None:
    """The exact case FR-P1-05-21 names: rows beyond the training range reach the fit."""
    start, _ = training_range(_p("F1"))
    beyond = _bundle(_train_spec("F1"), transform_id="T-F1", start=start, hours=24 * 120)
    series = {}
    with pytest.raises(LeakageError) as excinfo:
        climatology.fit_climatology(beyond, partition=_p("F1"), series=series)
    assert "outside partition F1's training range" in str(excinfo.value)


def test_climatology_refuses_a_score_role_bundle_and_a_tampered_fit_record() -> None:
    score = _bundle(_score_spec("F1"), transform_id="T-F1")
    with pytest.raises(LeakageError):
        climatology.fit_climatology(score, partition=_p("F1"), series={})
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
    with pytest.raises(IntegrityError):
        read_horizons(snapshot)  # TE 2.1's horizons are NOT transcribed by this pass


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
            "selection": {"simplicity_tolerance_fraction": 0.05, "declared_baseline": "M-01"},
        }
    )
    assert select_configuration([simple, complex_], snapshot=snapshot, fold_ids=folds) is simple
    far = CandidateScore({"alpha": 0.1}, {f: 0.5 for f in folds}, complexity=3.0)
    assert select_configuration([simple, complex_, far], snapshot=snapshot, fold_ids=folds) is far
    assert_refit_unchanged({"alpha": 2.0}, {"alpha": 2.0})
    with pytest.raises(IntegrityError):
        assert_refit_unchanged({"alpha": 2.0}, {"alpha": 0.5})


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
# 11. M-06: the pin guard refuses while the pin is TBD; settings from config (FU-1 = C)
# =======================================================================================


def test_the_pin_guard_refuses_against_the_real_requirements_and_a_commented_pin(
    tmp_path: Path,
) -> None:
    with pytest.raises(IntegrityError) as excinfo:
        lstm.require_frozen_pin()  # the real requirements.txt: comment-only TBD entry
    assert "TS-M-01" in str(excinfo.value) and "TBD" in str(excinfo.value)
    commented = tmp_path / "requirements.txt"
    commented.write_text("# tensorflow==2.21.0 (candidate, not frozen)\nnumpy==1.26.4\n")
    with pytest.raises(IntegrityError):
        lstm.require_frozen_pin(commented)
    frozen = tmp_path / "frozen.txt"
    frozen.write_text("numpy==1.26.4\ntensorflow==0.0.0\n")
    assert lstm.require_frozen_pin(frozen) == "tensorflow==0.0.0"
    assert "tensorflow" not in sys.modules


class _NullBackend:
    def save(self, *, epoch: int, weights: Any) -> str:
        return f"null://{epoch}"

    def load(self, payload_ref: str) -> Any:
        return None


def test_m06_fit_refuses_at_the_guard_before_any_tensorflow_import() -> None:
    train = _bundle(_train_spec("F1"), transform_id="T-F1", hours=4)
    score = _bundle(_score_spec("F1"), transform_id="T-F1", hours=2)
    params = lstm.enumerate_lstm_grid(SNAPSHOT)[0]
    seed = sorted(EXPECTED)[0]
    with pytest.raises(SeedError):
        fit_predict(
            "M-06", bundle=train, partition=_p("F1"), snapshot=SNAPSHOT,
            target=_target(_ts(1, 1), _ts(5, 1)), score_bundle=score, params=params,
        )
    with pytest.raises(IntegrityError) as excinfo:
        lstm.fit_predict_rows(
            "M-06", bundle=train, score_bundle=score, partition=_p("F1"), snapshot=SNAPSHOT,
            target=_target(_ts(1, 1), _ts(5, 1)), seed=seed, params=params,
            horizon_hours=SYNTH_HORIZON, backend=_NullBackend(),
        )
    assert "TS-M-01" in str(excinfo.value)
    assert "tensorflow" not in sys.modules
    with pytest.raises(IntegrityError):
        lstm.determinism_check(seed=seed)
    with pytest.raises(IntegrityError):
        lstm.build_keras_model(params, n_features=1, window_steps=3, settings=SYNTH_SETTINGS)


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
            "models": {"lstm_fixed_settings": SYNTH_SETTINGS},
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
