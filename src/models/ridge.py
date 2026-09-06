"""M-04 Ridge over D-121's grid of six alphas, direct, on the standardised matrix.

Purpose
-------
`domain-entities.md` section 1 (W-2; R-96; TS-M-03). Ridge is fitted per fold on the
train-role bundle's ELIGIBLE columns at the run's horizon (`train.eligible_feature_columns`:
a lagged column not yet observed at the forecast origin is excluded by arithmetic on its own
declared step — no literal horizon, R-99) and predicts on the score-role bundle.

`scikit-learn` is imported LAZILY, inside the fit path (`require_sklearn`), and its absence
refuses by NAME — the pin `requirements.txt` carries (`scikit-learn==1.4.2`, code-generation
Q3 = A) is read from that file, never restated here. Its CV splitters are never used: fold
construction is `features-and-splits`' (`Partition`), and this module consumes partitions.

The grid point is a caller argument asserted to be a MEMBER of `configs/experiment.yaml`'s
`grids.ridge` (R-96: a value outside the grid refuses); no alpha lives in source.

Inputs
------
Train and score `FeatureBundle`s, the `Partition`, the `ConfigSnapshot` (grids, horizons),
the D-17 target frame (labels), `params = {"alpha": ...}`.

Re-run behaviour
----------------
Deterministic for a given input (Ridge has no random state). Rows whose label is a target gap
are excluded from the fit and COUNTED on the prediction frame's attrs.

Boundaries
----------
Never imports `src.external.iri`, `src.external.gim`, `src.evaluation` or any NN stack. No
scientific constant.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from src.data.config import IntegrityError
from src.data.splits import Partition
from src.features.build import FeatureBundle
from src.models.train import (
    ConfigSnapshot,
    Prediction,
    assert_in_grid,
    bundle_index,
    eligible_feature_columns,
    feature_rows,
    labels_for,
    new_prediction,
    pinned_requirement,
    target_series,
)

__all__ = ["require_sklearn", "fit_predict_rows"]

GRID_TRACK = "ridge"


def require_sklearn(requirements_path: Path | None = None) -> Any:
    """Import `sklearn` lazily; refuse BY NAME when it is absent (TS-M-03; Q3 = A)."""
    try:
        import sklearn  # noqa: F401 - lazy import is the point
    except ImportError as exc:
        pin = pinned_requirement("scikit-learn", requirements_path) or "scikit-learn (UNPINNED)"
        raise IntegrityError(
            "scikit-learn",
            f"is not importable ({exc}); M-04 Ridge and M-05 Random Forest need the governed pin "
            f"{pin!r} from requirements.txt installed on the Python 3.11 pin (TS-M-03; TE 13.1) — "
            f"refused, never substituted",
        ) from exc
    return sklearn


def _scored_features(
    bundle: FeatureBundle, score_bundle: FeatureBundle, *, horizon_hours: int
) -> tuple[list[str], list[list[float]], list[list[float]]]:
    columns = list(eligible_feature_columns(bundle, horizon_hours=horizon_hours))
    missing = [c for c in columns if c not in score_bundle.provenance]
    if missing:
        raise IntegrityError(
            f"score bundle {score_bundle.spec.partition_id}/{score_bundle.spec.role}",
            f"lacks fitted feature column(s) {missing}; the score frame is not the one the "
            f"model was fitted for",
        )
    return columns, feature_rows(bundle, columns), feature_rows(score_bundle, columns)


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
    requirements_path: Path | None = None,
) -> Prediction:
    """The family entry `train.fit_predict` dispatches to for M-04."""
    if model_id != "M-04":
        raise IntegrityError(f"model_id {model_id!r}", "ridge.py serves M-04 only")
    if params is None:
        raise IntegrityError(
            "fit_predict(M-04)",
            "a grid point {alpha} is required; a default alpha would be a value chosen by "
            "convenience (R-96; TE 18.2)",
        )
    assert_in_grid(snapshot, GRID_TRACK, params)  # a value outside the config grid refuses
    columns, x_train, x_score = _scored_features(bundle, score_bundle, horizon_hours=horizon_hours)
    series = target_series(target)
    _, labels, missing_labels = labels_for(bundle, series)
    kept = [(x, y) for x, y in zip(x_train, labels, strict=True) if y is not None]
    if not kept:
        raise IntegrityError(
            f"bundle {bundle.spec.partition_id}/{bundle.spec.role}",
            "no training row carries a label; a fit over zero rows is not a fit",
        )
    require_sklearn(requirements_path)
    from sklearn.linear_model import Ridge  # lazy: inside the fit path only

    model = Ridge(alpha=params["alpha"])
    model.fit([x for x, _ in kept], [y for _, y in kept])
    y_hat = [float(v) for v in model.predict(x_score)]
    rows = [
        {"station": station, "interval_start_utc": stamp, "y_hat": value}
        for (station, stamp), value in zip(bundle_index(score_bundle), y_hat, strict=True)
    ]
    return new_prediction(
        model_id,
        seed=None,
        rows=rows,
        bundle=score_bundle,
        partition=partition,
        attrs={
            "role": score_bundle.spec.role,
            "horizon_hours": horizon_hours,
            "hyperparameters": dict(params),
            "feature_columns": columns,
            "training_rows_excluded_missing_label": missing_labels,
        },
    )
