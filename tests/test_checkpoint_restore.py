"""WS-15 / TA-13: M-06 restores its lowest-validation-RMSE checkpoint, never the last epoch.

PURPOSE. R-94's control (`domain-entities.md` section 4; W-4): checkpoint SELECTION is on the
lowest validation RMSE over a recorded epoch history, RESTORE returns that checkpoint through
a backend-neutral interface, and a restore that returns the LAST epoch FAILS. Tie and NaN
handling are stated and tested; a fake backend proves the save/load round trip without any ML
framework — the TensorFlow pin is `TBD — freeze gate` (code-generation FU-1 = C) and this
module exercises exactly the version-agnostic part.

INPUTS. Synthetic epoch histories and a synthetic `ConfigSnapshot`; no config value of the
real repository is read or asserted as a literal (the fixed-setting VALUES live only in
`configs/experiment.yaml`). No December content, no restricted path, no real signature.

WHAT NO TEST HERE DISCHARGES. WS-15 and TA-13 stay `Pending`: the real Keras checkpoint bytes
wait for the pin. Smoke evidence only on the interpreter used here.

Run: pytest tests/test_checkpoint_restore.py -rs
"""

from __future__ import annotations

import dataclasses
import math
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "tests") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "tests"))

from test_split_embargo import synthetic_snapshot  # noqa: E402

from src.data.config import IntegrityError  # noqa: E402
from src.models.checkpoint import (  # noqa: E402
    Checkpoint,
    EpochRecord,
    assert_restored_is_best,
    read_checkpoint_policy,
    restore,
    select_best,
    should_stop,
)
from src.models.train import BEST_CHECKPOINT_POLICY, LSTM_FIXED_SETTING_KEYS  # noqa: E402

# Synthetic fixed-settings block: the KEY identities are the module's; the numeric values are
# fixture values, not Vision 8.6's (which live only in configs/experiment.yaml).
SYNTH_SETTINGS: dict[str, Any] = {
    "dropout": 0.35,
    "optimizer": "Adam",
    "loss": "MSE",
    "max_epochs": 6,
    "early_stopping_patience": 2,
    "early_stopping_monitor": "validation_rmse",
    "min_improvement_tecu": 0.05,
    "checkpoint_policy": BEST_CHECKPOINT_POLICY,
}


class FakeBackend:
    """An in-memory `CheckpointBackend`: proves the round trip without a framework."""

    def __init__(self) -> None:
        self.store: dict[str, Any] = {}
        self.loads: list[str] = []

    def save(self, *, epoch: int, weights: Any) -> str:
        ref = f"fake://epoch/{epoch}"
        self.store[ref] = weights
        return ref

    def load(self, payload_ref: str) -> Any:
        self.loads.append(payload_ref)
        return self.store[payload_ref]


def _history(rmses: list[float], backend: FakeBackend | None = None) -> list[EpochRecord]:
    out: list[EpochRecord] = []
    for epoch, rmse in enumerate(rmses, start=1):
        ref = backend.save(epoch=epoch, weights={"w": epoch}) if backend else f"ref-{epoch}"
        out.append(EpochRecord(epoch=epoch, validation_rmse=rmse, payload_ref=ref))
    return out


# --- selection ---------------------------------------------------------------------------


def test_selection_is_on_the_lowest_validation_rmse_not_the_last_epoch() -> None:
    history = _history([5.0, 3.0, 2.5, 4.0, 4.5])
    best = select_best(history)
    assert best.epoch == 3
    assert best.validation_rmse == 2.5
    assert best.epoch != history[-1].epoch, "the last epoch is not the best here"


def test_tie_breaks_toward_the_earliest_epoch() -> None:
    history = _history([4.0, 2.0, 3.0, 2.0])
    assert select_best(history).epoch == 2


def test_nan_validation_rmse_is_refused_never_skipped() -> None:
    history = _history([4.0, math.nan, 1.0])
    with pytest.raises(IntegrityError) as excinfo:
        select_best(history)
    assert "NaN" in str(excinfo.value)


def test_negative_rmse_duplicate_epoch_and_empty_history_are_refused() -> None:
    with pytest.raises(IntegrityError):
        select_best(_history([1.0, -0.5]))
    with pytest.raises(IntegrityError):
        select_best(
            [EpochRecord(1, 1.0, "a"), EpochRecord(1, 0.5, "b")]
        )
    with pytest.raises(IntegrityError):
        select_best([])
    with pytest.raises(IntegrityError):
        select_best([EpochRecord(1, 1.0, "")])


# --- restore ----------------------------------------------------------------------------


def test_restore_returns_the_best_checkpoint_and_its_weights_through_the_backend() -> None:
    backend = FakeBackend()
    history = _history([3.0, 1.5, 2.0, 2.5], backend)
    checkpoint, weights = restore(
        history, backend=backend, model_id="M-06", seed=11, fold_id="F2"
    )
    assert checkpoint.epoch == 2
    assert checkpoint.validation_rmse == 1.5
    assert weights == {"w": 2}, "the round trip must return the SELECTED epoch's weights"
    assert backend.loads == ["fake://epoch/2"], "exactly one load, of the best payload"
    assert (checkpoint.model_id, checkpoint.seed, checkpoint.fold_id) == ("M-06", 11, "F2")
    assert_restored_is_best(checkpoint, history)


def test_a_last_epoch_restore_fails_the_negative_control() -> None:
    backend = FakeBackend()
    history = _history([3.0, 1.5, 2.0, 2.5], backend)
    last = history[-1]
    last_epoch_restore = Checkpoint(
        model_id="M-06",
        seed=11,
        fold_id="F2",
        epoch=last.epoch,
        validation_rmse=last.validation_rmse,
        payload_ref=last.payload_ref,
    )
    with pytest.raises(IntegrityError) as excinfo:
        assert_restored_is_best(last_epoch_restore, history)
    assert "last-epoch" in str(excinfo.value)


def test_a_restore_with_the_right_epoch_but_a_foreign_payload_fails() -> None:
    history = _history([3.0, 1.5, 2.0])
    forged = Checkpoint("M-06", 11, "F1", epoch=2, validation_rmse=1.5, payload_ref="elsewhere")
    with pytest.raises(IntegrityError):
        assert_restored_is_best(forged, history)


def test_checkpoint_carries_exactly_the_six_approved_attributes() -> None:
    names = [f.name for f in dataclasses.fields(Checkpoint)]
    assert names == ["model_id", "seed", "fold_id", "epoch", "validation_rmse", "payload_ref"]


# --- early stopping on validation RMSE --------------------------------------------------


def test_should_stop_after_patience_epochs_without_a_minimum_improvement() -> None:
    patience = SYNTH_SETTINGS["early_stopping_patience"]
    min_improvement = SYNTH_SETTINGS["min_improvement_tecu"]
    improving = _history([3.0, 2.0, 1.0])
    assert not should_stop(improving, patience=patience, min_improvement=min_improvement)
    stale = _history([3.0, 2.0, 1.99, 1.98])  # improvements below the minimum do not reset
    assert should_stop(stale, patience=patience, min_improvement=min_improvement)
    assert not should_stop([], patience=patience, min_improvement=min_improvement)


def test_should_stop_refuses_a_non_positive_patience() -> None:
    with pytest.raises(IntegrityError):
        should_stop(_history([1.0]), patience=0, min_improvement=0.1)


# --- the policy comes from config and is the one this module implements ------------------


def test_the_configured_policy_is_best_checkpoint_and_last_epoch_is_refused() -> None:
    good = synthetic_snapshot(experiment={"models": {"lstm_fixed_settings": SYNTH_SETTINGS}})
    assert read_checkpoint_policy(good) == BEST_CHECKPOINT_POLICY
    bad_settings = dict(SYNTH_SETTINGS, checkpoint_policy="last_epoch")
    bad = synthetic_snapshot(experiment={"models": {"lstm_fixed_settings": bad_settings}})
    with pytest.raises(IntegrityError) as excinfo:
        read_checkpoint_policy(bad)
    assert "last epoch" in str(excinfo.value)


def test_every_one_of_the_seven_setting_keys_is_required(
) -> None:
    for key in LSTM_FIXED_SETTING_KEYS:
        settings = {k: v for k, v in SYNTH_SETTINGS.items() if k != key}
        snapshot = synthetic_snapshot(experiment={"models": {"lstm_fixed_settings": settings}})
        with pytest.raises(IntegrityError) as excinfo:
            read_checkpoint_policy(snapshot)
        assert key in str(excinfo.value)
