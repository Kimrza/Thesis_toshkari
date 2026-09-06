"""Checkpoint selection and restore: lowest validation RMSE, never the last epoch (W-4; R-94).

Purpose
-------
`domain-entities.md` section 4. Best-checkpoint restoration is one of Vision 8.6's seven
fixed LSTM settings (`configs/experiment.yaml` `models.lstm_fixed_settings.checkpoint_policy`),
not a choice made here. This module is BACKEND-NEUTRAL: it selects over a recorded epoch
history and restores through a `CheckpointBackend` the caller supplies (the Keras backend in
`lstm.py`, a fake in `tests/test_checkpoint_restore.py`), so the selection and restore logic —
the part WS-15 / TA-13 test — is real and testable while the TensorFlow pin is
`TBD — freeze gate` (code-generation FU-1 = C).

Semantics stated so an implementer needs no second lookup:

* selection is on the LOWEST `validation_rmse` in the history;
* a tie is broken toward the EARLIEST epoch (the first time the best value was reached);
* a NaN or negative `validation_rmse` REFUSES — it cannot be compared and is never skipped;
* an empty history refuses;
* `assert_restored_is_best` is the negative control: a checkpoint whose epoch is not the
  selected one (for instance the LAST epoch) fails.

Early stopping is the same history read forward: `should_stop` is true once the best value
has not improved by at least `min_improvement` for `patience` consecutive epochs — both
values from configuration, never literals here.

Inputs
------
`EpochRecord`s appended by the training loop; a `CheckpointBackend` with `save`/`load`.

Re-run behaviour
----------------
Pure functions of the history; the backend owns persistence.

Boundaries
----------
Imports no ML framework. No scientific constant.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Protocol

from src.data.config import IntegrityError
from src.models.train import BEST_CHECKPOINT_POLICY, ConfigSnapshot, read_lstm_fixed_settings

__all__ = [
    "EpochRecord",
    "Checkpoint",
    "CheckpointBackend",
    "select_best",
    "restore",
    "assert_restored_is_best",
    "should_stop",
    "read_checkpoint_policy",
]


@dataclass(frozen=True)
class EpochRecord:
    """One epoch of a run: the metric it was checkpointed on and where its weights went."""

    epoch: int
    validation_rmse: float
    payload_ref: str


@dataclass(frozen=True)
class Checkpoint:
    """`domain-entities.md` section 4's six attributes."""

    model_id: str
    seed: int
    fold_id: str
    epoch: int
    validation_rmse: float
    payload_ref: str


class CheckpointBackend(Protocol):
    def save(self, *, epoch: int, weights: Any) -> str: ...

    def load(self, payload_ref: str) -> Any: ...


def _validate(history: Sequence[EpochRecord]) -> list[EpochRecord]:
    records = list(history)
    if not records:
        raise IntegrityError("epoch history", "is empty; nothing to select a checkpoint from")
    seen: set[int] = set()
    for record in records:
        if record.epoch in seen:
            raise IntegrityError("epoch history", f"epoch {record.epoch} is recorded twice")
        seen.add(record.epoch)
        rmse = record.validation_rmse
        if not isinstance(rmse, int | float) or isinstance(rmse, bool) or math.isnan(rmse):
            raise IntegrityError(
                f"epoch {record.epoch}",
                f"validation_rmse {rmse!r} is not a comparable number; a NaN metric is refused, "
                f"never skipped (R-94)",
            )
        if rmse < 0:
            raise IntegrityError(f"epoch {record.epoch}", "validation_rmse is negative")
        if not str(record.payload_ref).strip():
            raise IntegrityError(f"epoch {record.epoch}", "carries no payload_ref")
    return records


def select_best(history: Sequence[EpochRecord]) -> EpochRecord:
    """The record with the LOWEST validation RMSE; ties -> the earliest epoch (R-94)."""
    records = _validate(history)
    return min(records, key=lambda r: (r.validation_rmse, r.epoch))


def restore(
    history: Sequence[EpochRecord],
    *,
    backend: CheckpointBackend,
    model_id: str,
    seed: int,
    fold_id: str,
) -> tuple[Checkpoint, Any]:
    """Restore the lowest-validation-RMSE checkpoint through the backend; returns it with the
    loaded weights. Never the last epoch (R-94; WS-15; TA-13)."""
    best = select_best(history)
    weights = backend.load(best.payload_ref)
    checkpoint = Checkpoint(
        model_id=model_id,
        seed=seed,
        fold_id=fold_id,
        epoch=best.epoch,
        validation_rmse=float(best.validation_rmse),
        payload_ref=best.payload_ref,
    )
    return checkpoint, weights


def assert_restored_is_best(checkpoint: Checkpoint, history: Sequence[EpochRecord]) -> None:
    """R-94's negative control: a restore returning any epoch but the selected one FAILS."""
    best = select_best(history)
    if checkpoint.epoch != best.epoch or checkpoint.payload_ref != best.payload_ref:
        raise IntegrityError(
            f"checkpoint epoch {checkpoint.epoch}",
            f"is not the lowest-validation-RMSE epoch {best.epoch} (rmse {best.validation_rmse}); "
            f"a last-epoch restore is the library default shape and is exactly what R-94 refuses",
        )


def should_stop(
    history: Sequence[EpochRecord], *, patience: int, min_improvement: float
) -> bool:
    """Early stopping on validation RMSE: true once `patience` consecutive epochs have not
    improved the best value by at least `min_improvement` (both from configuration)."""
    if isinstance(patience, bool) or not isinstance(patience, int) or patience <= 0:
        raise IntegrityError("early_stopping_patience", f"{patience!r} is not a positive integer")
    if not isinstance(min_improvement, int | float) or min_improvement < 0:
        raise IntegrityError(
            "min_improvement", f"{min_improvement!r} is not a non-negative number"
        )
    records = _validate(history) if history else []
    best: float | None = None
    stale = 0
    for record in sorted(records, key=lambda r: r.epoch):
        if best is None or best - record.validation_rmse >= min_improvement:
            best = record.validation_rmse
            stale = 0
        else:
            stale += 1
    return stale >= patience


def read_checkpoint_policy(snapshot: ConfigSnapshot) -> str:
    """The configured policy — asserted to be the one this module implements (R-94)."""
    policy = str(read_lstm_fixed_settings(snapshot)["checkpoint_policy"])
    if policy != BEST_CHECKPOINT_POLICY:
        raise IntegrityError(
            "configs/experiment.yaml: models.lstm_fixed_settings.checkpoint_policy",
            f"{policy!r} is not {BEST_CHECKPOINT_POLICY!r}",
        )
    return policy
