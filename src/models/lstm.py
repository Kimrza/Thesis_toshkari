"""M-06 compact direct LSTM (tf.keras): every TensorFlow import lives behind the pin guard.

Purpose
-------
`domain-entities.md` sections 1, 4, 7 (W-2, W-4, W-6; R-94, R-96; TS-M-01, TS-M-02, TS-M-04).
The one NN stack is TensorFlow/Keras (TE 8.3 prohibits a second deep-learning stack). This
module is written against the tf.keras API of **2.21.0**, which the project decision owner
selected as the frozen pin on **2026-09-10**, adopted as **D-36** (prepared at
`governance/CHANGE_RECORD_2026-09-10_owner_rulings_implementation.md`, recorded in
`evidence/DECISIONS.md`) — so `requirements.txt` carries `tensorflow==2.21.0` and the implemented
API and the pinned version agree by construction. **No `tensorflow` import exists at module
scope or outside a path that first calls `require_frozen_pin()`**: that guard reads
`requirements.txt` and refuses — naming TS-M-01 and the pin — unless a non-comment
`tensorflow==<version>` line exists, and it keeps refusing an absent or commented-out pin.
Nothing here fills the pin. **The pin is frozen; the ENVIRONMENT is not verified**:
installation, import, API-compatibility and TE 8.1's both-platform (Kaggle and local) check
have never executed here (PyPI unreachable), so no M-06 fit has ever run and TA-26 stays
`Pending`.

What is real and testable without the pin: grid enumeration from `configs/experiment.yaml`
(sixteen combinations, D-121), the seven fixed Vision 8.6 settings asserted from config,
horizon-parameterised window slicing (R-99), and lowest-validation-RMSE checkpoint selection
and restore through `checkpoint.py`'s backend-neutral interface.

Determinism (TS-M-02; SD-M-05): `determinism_check` sets the seed with
`tf.keras.utils.set_random_seed`, enables `tf.config.experimental.enable_op_determinism()`
("where supported"), and runs a POSITIVE PROBE — a caller-supplied operation expected to be
refused under op determinism. `nondeterministic_ops` is a MEASURED output: an empty list is
never proof of determinism. The probe's subject operation is owed at pin-freeze; when none is
supplied the check degrades to a recorded boolean and the degradation is recorded, not hidden.

Inputs
------
Train and score `FeatureBundle`s (the rank-3 `tensor` is the LSTM input), the `Partition`,
the `ConfigSnapshot`, the D-17 target frame, the seed (required — each seed is its own
registry run, TE 13.5), `params` naming a grid member, the horizon, a `CheckpointBackend`.

Re-run behaviour
----------------
Deterministic where the frozen environment supports it; the run records what it cannot
guarantee. Nothing is persisted by this module except through the backend.

Boundaries
----------
Never imports `src.external.iri`, `src.external.gim`, `src.evaluation` or a second
deep-learning stack. No grid
value or setting is held in source. Never names the restricted December root.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from src.data.config import IntegrityError, SeedError
from src.data.splits import Partition
from src.features._frames import tensor_as_nested, tensor_shape
from src.features.build import FeatureBundle
from src.models.checkpoint import (
    CheckpointBackend,
    EpochRecord,
    restore,
    should_stop,
)
from src.models.train import (
    ConfigSnapshot,
    Prediction,
    assert_in_grid,
    enumerate_grid,
    labels_for,
    new_prediction,
    pinned_requirement,
    read_lstm_fixed_settings,
    target_series,
)

__all__ = [
    "GRID_TRACK",
    "DeterminismProbeResult",
    "require_frozen_pin",
    "enumerate_lstm_grid",
    "fixed_settings",
    "observable_steps",
    "build_keras_model",
    "determinism_check",
    "fit_predict_rows",
]

GRID_TRACK: Final[str] = "lstm"
#: Config identity -> Keras optimizer/loss identifiers. Identity mappings, not values.
_OPTIMIZERS: Final[Mapping[str, str]] = {"Adam": "Adam"}
_LOSSES: Final[Mapping[str, str]] = {"MSE": "mse"}


@dataclass(frozen=True)
class DeterminismProbeResult:
    """SD-M-05's positive-probe record: what was set, what the probe did, what was measured."""

    seed: int
    op_determinism_enabled: bool
    probe_ran: bool
    probe_detected: bool
    nondeterministic_ops: tuple[str, ...]
    degradation: str


def require_frozen_pin(requirements_path: Path | None = None) -> str:
    """The guard every TensorFlow import sits behind (TS-M-01; FU-1 = C).

    Raises
    ------
    IntegrityError
        no non-comment `tensorflow==<version>` line in `requirements.txt` — the pin is
        `TBD — freeze gate`, is frozen only after the fixture runs (TE 8.1) and is never
        filled by an implementer (Vision 1.2; TE 1.1). Returns the pin line when frozen.
    """
    pin = pinned_requirement("tensorflow", requirements_path)
    if pin is None:
        raise IntegrityError(
            "requirements.txt: tensorflow",
            "the TensorFlow pin is TBD — freeze gate (TS-M-01): M-06's serialization contract, "
            "checkpoint format and determinism settings are version-dependent, TE 8.1 freezes "
            "the pin only after the Kaggle and local fixture runs, and no implementer fills it by "
            "convenience — every tensorflow import is refused until a frozen `tensorflow==` "
            "line exists (code-generation FU-1 = C)",
        )
    return pin


def enumerate_lstm_grid(snapshot: ConfigSnapshot) -> tuple[dict[str, Any], ...]:
    """D-121's sixteen combinations, enumerated from config (the count is asserted by R-96)."""
    return enumerate_grid(snapshot, GRID_TRACK)


def fixed_settings(snapshot: ConfigSnapshot) -> Mapping[str, Any]:
    """Vision 8.6's seven fixed settings, from config; identities mapped to Keras names."""
    settings = read_lstm_fixed_settings(snapshot)
    if str(settings["optimizer"]) not in _OPTIMIZERS:
        raise IntegrityError(
            "configs/experiment.yaml: models.lstm_fixed_settings.optimizer",
            f"{settings['optimizer']!r} has no Keras mapping in this module ({list(_OPTIMIZERS)})",
        )
    if str(settings["loss"]) not in _LOSSES:
        raise IntegrityError(
            "configs/experiment.yaml: models.lstm_fixed_settings.loss",
            f"{settings['loss']!r} has no Keras mapping in this module ({list(_LOSSES)})",
        )
    return settings


def observable_steps(window_steps: int, *, horizon_hours: int) -> tuple[int, int]:
    """The slice `[start, stop)` of a window's steps observable at the forecast origin.

    Steps are ordered oldest first (`windows.py`: step index i is k = window - i hours before
    t); a step with k < horizon is not yet observed. Arithmetic on the horizon — no literal.
    """
    if window_steps <= 0:
        raise IntegrityError("window_steps", "must be positive")
    stop = window_steps - (horizon_hours - 1)
    if stop <= 0:
        raise IntegrityError(
            "window",
            f"no step of a {window_steps}-step window is observable at horizon {horizon_hours} h",
        )
    return 0, stop


def build_keras_model(
    params: Mapping[str, Any],
    *,
    n_features: int,
    window_steps: int,
    settings: Mapping[str, Any],
    requirements_path: Path | None = None,
) -> Any:
    """The compact direct LSTM (tf.keras 2.21.0 candidate API). GUARDED: the import happens
    only after `require_frozen_pin` passes."""
    require_frozen_pin(requirements_path)
    import tensorflow as tf  # guarded import (FU-1 = C)

    layers = int(params["layers"])
    units = int(params["units"])
    model = tf.keras.Sequential(name="m06_compact_direct_lstm")
    model.add(tf.keras.Input(shape=(window_steps, n_features)))
    for index in range(layers):
        model.add(tf.keras.layers.LSTM(units, return_sequences=index < layers - 1))
        model.add(tf.keras.layers.Dropout(float(settings["dropout"])))
    model.add(tf.keras.layers.Dense(1))
    optimizer_name = _OPTIMIZERS[str(settings["optimizer"])]
    optimizer = getattr(tf.keras.optimizers, optimizer_name)(
        learning_rate=float(params["learning_rate"])
    )
    model.compile(optimizer=optimizer, loss=_LOSSES[str(settings["loss"])])
    return model


def determinism_check(
    *,
    seed: int,
    probe: Callable[[Any], Any] | None = None,
    requirements_path: Path | None = None,
) -> DeterminismProbeResult:
    """SD-M-05's positive probe. GUARDED. `probe(tf)` runs a known-nondeterministic operation;
    under op determinism TensorFlow refuses it, and that refusal is what is recorded. With no
    probe supplied the check DEGRADES to a recorded boolean and says so."""
    require_frozen_pin(requirements_path)
    import tensorflow as tf  # guarded import (FU-1 = C)

    tf.keras.utils.set_random_seed(int(seed))
    tf.config.experimental.enable_op_determinism()
    if probe is None:
        return DeterminismProbeResult(
            seed=int(seed),
            op_determinism_enabled=True,
            probe_ran=False,
            probe_detected=False,
            nondeterministic_ops=(),
            degradation=(
                "no probe operation supplied: the probe's subject is owed at pin-freeze "
                "(SD-M-05); this result is a recorded boolean, not evidence of determinism"
            ),
        )
    detected: list[str] = []
    try:
        probe(tf)
    except tf.errors.UnimplementedError as exc:  # the refusal IS the detection
        detected.append(f"probe refused under op determinism: {exc}")
    if not detected:
        raise IntegrityError(
            "determinism probe",
            "the known-nondeterministic probe operation ran WITHOUT being refused; either op "
            "determinism is not effective on this pin or the probe subject is wrong — an empty "
            "nondeterministic_ops from a probe that detected nothing is never accepted (SD-M-05)",
        )
    return DeterminismProbeResult(
        seed=int(seed),
        op_determinism_enabled=True,
        probe_ran=True,
        probe_detected=True,
        nondeterministic_ops=tuple(detected),
        degradation="",
    )


def _rmse(pairs: list[tuple[float, float]]) -> float:
    if not pairs:
        raise IntegrityError(
            "validation set", "is empty; a validation RMSE over zero rows is not one"
        )
    return (sum((a - b) ** 2 for a, b in pairs) / len(pairs)) ** 0.5


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
    backend: CheckpointBackend | None = None,
    requirements_path: Path | None = None,
) -> Prediction:
    """The family entry `train.fit_predict` dispatches to for M-06.

    Order of refusals: grid membership (R-96) and the seven settings from config; the seed;
    then `require_frozen_pin` — BEFORE any TensorFlow import. Today the pin guard refuses,
    so every M-06 fit stops here with a message naming TS-M-01; nothing below it has executed
    anywhere (FU-1 = C's honest limit; TA-26 `Pending`).
    """
    if model_id != "M-06":
        raise IntegrityError(f"model_id {model_id!r}", "lstm.py serves M-06 only")
    if params is None:
        raise IntegrityError(
            "fit_predict(M-06)",
            "a grid point {layers, units, learning_rate, batch_size} is required; a default would "
            "be a value chosen by convenience (R-96; TE 18.2)",
        )
    assert_in_grid(snapshot, GRID_TRACK, params)
    settings = fixed_settings(snapshot)
    if seed is None or isinstance(seed, bool) or not isinstance(seed, int):
        raise SeedError(
            "fit_predict(M-06)", "M-06 requires the run's seed from configs/seeds.yaml"
        )
    if backend is None:
        raise IntegrityError(
            "fit_predict(M-06)",
            "a CheckpointBackend is required: best-checkpoint restoration is a fixed setting "
            "(R-94) and needs somewhere to keep the per-epoch weights",
        )
    require_frozen_pin(requirements_path)  # refuses today; nothing below has ever run
    import tensorflow as tf  # guarded import (FU-1 = C)

    rows_n, window_steps, n_features = tensor_shape(bundle.tensor)
    start, stop = observable_steps(window_steps, horizon_hours=horizon_hours)
    series = target_series(target)
    _, labels, missing_labels = labels_for(bundle, series)
    nested = tensor_as_nested(bundle.tensor)
    x_train = [steps[start:stop] for steps, y in zip(nested, labels, strict=True) if y is not None]
    y_train = [y for y in labels if y is not None]
    if not x_train:
        raise IntegrityError(
            f"bundle {bundle.spec.partition_id}/{bundle.spec.role}", "no training row has a label"
        )
    score_keys, score_labels, _ = labels_for(score_bundle, series)
    x_score = [steps[start:stop] for steps in tensor_as_nested(score_bundle.tensor)]
    validation = [
        (x, y) for x, y in zip(x_score, score_labels, strict=True) if y is not None
    ]
    determinism = determinism_check(seed=seed, requirements_path=requirements_path)
    model = build_keras_model(
        params,
        n_features=n_features,
        window_steps=stop - start,
        settings=settings,
        requirements_path=requirements_path,
    )
    history: list[EpochRecord] = []
    max_epochs = int(settings["max_epochs"])
    patience = int(settings["early_stopping_patience"])
    min_improvement = float(settings["min_improvement_tecu"])
    x_arr = tf.constant(x_train, dtype=tf.float32)
    y_arr = tf.constant(y_train, dtype=tf.float32)
    x_val = tf.constant([x for x, _ in validation], dtype=tf.float32)
    y_val = [y for _, y in validation]
    for epoch in range(1, max_epochs + 1):
        model.fit(x_arr, y_arr, batch_size=int(params["batch_size"]), epochs=1, verbose=0,
                  shuffle=True)
        predicted = [float(v[0]) for v in model.predict(x_val, verbose=0)]
        rmse = _rmse(list(zip(predicted, y_val, strict=True)))
        payload_ref = backend.save(epoch=epoch, weights=model.get_weights())
        history.append(EpochRecord(epoch=epoch, validation_rmse=rmse, payload_ref=payload_ref))
        if should_stop(history, patience=patience, min_improvement=min_improvement):
            break
    checkpoint, weights = restore(
        history,
        backend=backend,
        model_id=model_id,
        seed=seed,
        fold_id=partition.partition_id,
    )
    model.set_weights(weights)  # best-checkpoint restoration, never the last epoch (R-94)
    y_hat = [float(v[0]) for v in model.predict(tf.constant(x_score, dtype=tf.float32), verbose=0)]
    rows = [
        {"station": station, "interval_start_utc": stamp, "y_hat": value}
        for (station, stamp), value in zip(score_keys, y_hat, strict=True)
    ]
    return new_prediction(
        model_id,
        seed=seed,
        rows=rows,
        bundle=score_bundle,
        partition=partition,
        attrs={
            "role": score_bundle.spec.role,
            "horizon_hours": horizon_hours,
            "hyperparameters": dict(params),
            "fixed_settings": dict(settings),
            "restored_epoch": checkpoint.epoch,
            "restored_validation_rmse": checkpoint.validation_rmse,
            "epochs_run": len(history),
            "training_rows_excluded_missing_label": missing_labels,
            "tensorflow_pin": require_frozen_pin(requirements_path),
            "nondeterministic_ops": list(determinism.nondeterministic_ops),
            "determinism_degradation": determinism.degradation,
            "training_rows": rows_n,
        },
    )
