"""Stage 5 (2026-10-02): the selection rule as ruled, the refit persistence format, and the
governed tuning helpers.

Purpose
-------
The Student ruled on 2026-10-02 that:

- D-124's "within 1%" is an ABSOLUTE margin in skill units, strictly less than the margin;
- "simpler" is the complexity proxy (ridge 1/alpha, random forest n_estimators x depth with
  None counted as 32, LSTM layers x units), with equal complexity going to the higher
  mean skill;
- the refit is persisted as `.keras` (M-06) and joblib (M-04/M-05), hashed at write and
  re-hashed before every load.

These tests pin each rule, prove the persistence round trip and its tamper refusal, and
cover the governed tune's mask RMSE, its December-access scan, and the refit-epoch
re-derivation guard that runs before REFIT.

Inputs: synthetic snapshots, a tiny scikit-learn Ridge, a tiny Keras model. Re-run
behaviour: pure; files go to pytest's tmp_path.
"""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
for entry in (REPO_ROOT, REPO_ROOT / "tests"):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from src.data.config import IntegrityError  # noqa: E402
from src.data.splits import PartitionKind  # noqa: E402
from src.models.train import (  # noqa: E402
    CandidateScore,
    FittedModelRecord,
    ModelFileStateBackend,
    assert_fitted_payload_unchanged,
    complexity_proxy,
    select_configuration,
)

from _fresh_process import in_fresh_process  # noqa: E402
from test_models_smoke import SYNTH_SETTINGS, _load_script, _snapshot  # noqa: E402

FOLDS = ("F1", "F2", "F3", "F4")
UTC = dt.timezone.utc


def _margin_snapshot(margin: float):
    return _snapshot(
        models={
            "lstm_fixed_settings": SYNTH_SETTINGS,
            "selection": {"simplicity_margin": margin},
            "declared_baseline_per_track": {"all_tracks": "persistence"},
        }
    )


def _candidate(params: dict, skill: float, complexity: float) -> CandidateScore:
    return CandidateScore(params, {f: skill for f in FOLDS}, complexity=complexity)


# --- the selection rule ---------------------------------------------------------------------


def test_margin_is_absolute_in_skill_units():
    """0.300 vs 0.295 differs by 0.005: inside an absolute 0.01, outside the old relative
    reading (0.01 x 0.300 = 0.003). The simpler candidate must win."""
    complex_ = _candidate({"units": 64}, 0.300, complexity=128.0)
    simple = _candidate({"units": 32}, 0.295, complexity=32.0)
    chosen = select_configuration([complex_, simple], snapshot=_margin_snapshot(0.01), fold_ids=FOLDS)
    assert chosen is simple


def test_margin_is_strict():
    """A difference exactly equal to the margin is not 'less than' it (Vision 8.7)."""
    best = _candidate({"units": 64}, 0.5, complexity=128.0)
    edge = _candidate({"units": 32}, 0.25, complexity=32.0)
    chosen = select_configuration([best, edge], snapshot=_margin_snapshot(0.25), fold_ids=FOLDS)
    assert chosen is best


def test_equal_complexity_goes_to_the_higher_mean_skill():
    lower = _candidate({"batch_size": 64, "units": 32}, 0.296, complexity=32.0)
    higher = _candidate({"batch_size": 256, "units": 32}, 0.299, complexity=32.0)
    far_more_complex = _candidate({"units": 64}, 0.300, complexity=128.0)
    chosen = select_configuration(
        [lower, higher, far_more_complex], snapshot=_margin_snapshot(0.01), fold_ids=FOLDS
    )
    assert chosen is higher


def test_zero_margin_selects_the_best():
    best = _candidate({"units": 64}, 0.31, complexity=128.0)
    simple = _candidate({"units": 32}, 0.30, complexity=32.0)
    assert select_configuration([best, simple], snapshot=_margin_snapshot(0.0), fold_ids=FOLDS) is best


def test_complexity_proxy_values():
    assert complexity_proxy("ridge", {"alpha": 10}) == pytest.approx(0.1)
    assert complexity_proxy("random_forest", {"n_estimators": 300, "max_depth": None}) == 300 * 32
    assert complexity_proxy("random_forest", {"n_estimators": 600, "max_depth": 8}) == 4800
    assert complexity_proxy("lstm", {"layers": 2, "units": 64}) == 128
    with pytest.raises(IntegrityError):
        complexity_proxy("gru", {})


# --- the refit persistence format -----------------------------------------------------------


def _record(model_id: str, ref: str, sha: str, seed=None) -> FittedModelRecord:
    return FittedModelRecord(
        model_id=model_id, seed=seed, fitted_partition_id="REFIT", transform_id="t",
        payload_ref=ref, payload_sha256=sha, fitted_at_utc="2026-10-02T00:00:00+00:00",
        hyperparameters={}, attrs={},
    )


def test_joblib_round_trip_hash_and_write_once(tmp_path):
    from sklearn.linear_model import Ridge

    model = Ridge(alpha=1.0).fit([[0.0, 1.0], [1.0, 0.0], [1.0, 1.0]], [1.0, 2.0, 3.0])
    backend = ModelFileStateBackend(tmp_path)
    state = {"estimator": model, "columns": ["a", "b"], "hyperparameters": {"alpha": 1.0}}
    ref, sha = backend.save_state(model_id="M-04", seed=None, state=state)
    assert ref.endswith("M-04.joblib")
    record = _record("M-04", ref, sha)
    assert_fitted_payload_unchanged(record)  # the hash the record holds is the file's
    loaded = backend.load_state(ref)
    assert loaded["columns"] == ["a", "b"]
    assert loaded["estimator"].predict([[0.5, 0.5]])[0] == model.predict([[0.5, 0.5]])[0]
    with pytest.raises(IntegrityError, match="written once"):
        backend.save_state(model_id="M-04", seed=None, state=state)
    Path(ref).write_bytes(Path(ref).read_bytes() + b"tamper")
    with pytest.raises(IntegrityError, match="does not match"):
        assert_fitted_payload_unchanged(record)  # refused BEFORE any load


@in_fresh_process  # TensorFlow is imported first in its own interpreter (R-05)
def test_keras_round_trip_and_tamper_refusal(tmp_path):
    from src.models import lstm

    params = {"layers": 1, "units": 4, "learning_rate": 1e-3, "batch_size": 64}
    model = lstm.build_keras_model(params, n_features=3, window_steps=5, settings=SYNTH_SETTINGS)
    weights = model.get_weights()

    class _Memory:
        def save(self, *, epoch, weights):  # pragma: no cover - not reached
            raise AssertionError

        def load(self, ref):
            assert ref == "epoch-7"
            return weights

    state = {
        "model_id": "M-06", "seed": 11, "payload_ref": "epoch-7", "n_features": 3,
        "window_steps": 5, "hyperparameters": params, "fixed_settings": dict(SYNTH_SETTINGS),
        "observable_slice": [0, 5], "restored_epoch": 7,
    }
    backend = ModelFileStateBackend(tmp_path, checkpoint_backend=_Memory())
    ref, sha = backend.save_state(model_id="M-06", seed=11, state=state)
    assert ref.endswith("M-06_seed11.state.json")
    assert (tmp_path / "M-06_seed11.keras").is_file()
    assert_fitted_payload_unchanged(_record("M-06", ref, sha, seed=11))
    loaded = ModelFileStateBackend(tmp_path).load_state(ref)
    assert loaded["payload_ref"] == str(tmp_path / "M-06_seed11.keras")
    restored = lstm.KerasFileCheckpointBackend().load(loaded["payload_ref"])
    assert all((a == b).all() for a, b in zip(restored, weights, strict=True))
    keras_file = tmp_path / "M-06_seed11.keras"
    keras_file.write_bytes(keras_file.read_bytes() + b"x")
    with pytest.raises(IntegrityError, match="does not match"):
        ModelFileStateBackend(tmp_path).load_state(ref)
    with pytest.raises(IntegrityError, match="inference-only"):
        lstm.KerasFileCheckpointBackend().save(epoch=1, weights=weights)


def test_m06_persistence_needs_the_checkpoint_backend(tmp_path):
    with pytest.raises(IntegrityError, match="checkpoint backend"):
        ModelFileStateBackend(tmp_path).save_state(
            model_id="M-06", seed=11, state={"payload_ref": "x"}
        )


# --- the governed tune's helpers ------------------------------------------------------------


@pytest.fixture(scope="module")
def six():
    return _load_script()


def test_mask_rmse_scores_exactly_the_mask(six):
    t0 = dt.datetime(2022, 4, 2, tzinfo=UTC)
    t1 = t0 + dt.timedelta(hours=1)
    values = {("ARUC", t0): 3.0, ("ARUC", t1): 100.0}
    series = {("ARUC", t0): 1.0, ("ARUC", t1): 1.0}
    assert six._mask_rmse(values, series, [("ARUC", t0)]) == pytest.approx(2.0)
    with pytest.raises(IntegrityError, match="empty"):
        six._mask_rmse(values, series, [])


def test_december_access_scan(six, tmp_path):
    log = tmp_path / "evidence" / "merge_run_access_log.jsonl"  # GOVERNED_ACCESS_LOG
    log.parent.mkdir()
    rows = [
        {"locked_test_accessed": True, "logged_at_utc": "2026-10-01T00:00:00+00:00", "run_id": "old"},
        {"locked_test_accessed": True, "logged_at_utc": "2026-10-03T00:00:00+00:00",
         "run_id": "new", "purpose": "coverage_audit", "performance_inspected": False},
        {"locked_test_accessed": False, "logged_at_utc": "2026-10-04T00:00:00+00:00"},
    ]
    log.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    hits = six._december_accesses_since(tmp_path, dt.datetime(2026, 10, 2, tzinfo=UTC))
    assert [h["run_id"] for h in hits] == ["new"] and hits[0]["performance_inspected"] is False
    log.write_text(log.read_text(encoding="utf-8") + "{not json\n", encoding="utf-8")
    with pytest.raises(IntegrityError, match="not valid JSON"):
        six._december_accesses_since(tmp_path, dt.datetime(2026, 10, 2, tzinfo=UTC))


def test_refit_epochs_are_rederived_from_this_invocations_folds(six):
    snapshot = _snapshot()  # SYNTH_REFIT: epochs 4
    partitions = [p for p in six.build_partitions(snapshot)]
    folds = [p for p in partitions if p.kind == PartitionKind.fold]
    seeds = frozenset({11, 22, 33})
    n = len(folds) * len(seeds)
    six._assert_refit_epochs_from_folds(snapshot, [4] * n, partitions=partitions, expected_seeds=seeds)
    with pytest.raises(IntegrityError, match="not 4|produces"):
        six._assert_refit_epochs_from_folds(
            snapshot, [9] * n, partitions=partitions, expected_seeds=seeds
        )
    with pytest.raises(IntegrityError, match="restored M-06 fold epochs"):
        six._assert_refit_epochs_from_folds(
            snapshot, [4] * (n - 1), partitions=partitions, expected_seeds=seeds
        )


def test_criterion_used_carries_the_rulings(six):
    snapshot = _margin_snapshot(0.01)
    criterion = six._criterion_used(snapshot)
    assert criterion["selection_margin_rule"] == "absolute_skill_units_strictly_less_than_margin"
    assert criterion["complexity_proxy_rule"].startswith("ridge:1/alpha")
    assert criterion["baseline_model_id"] == "M-01"
    assert six._criterion_used(snapshot) == criterion  # deterministic, hashable content
