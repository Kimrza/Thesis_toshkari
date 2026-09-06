"""M-05 direct Random Forest over D-121's grid of eighteen; importance is diagnostic only.

Purpose
-------
`domain-entities.md` sections 1 and 10 (W-2; R-96; R-100; TS-M-03). The forest is fitted per
fold on the train-role bundle's eligible columns at the run's horizon and predicts on the
score-role bundle — DIRECT only (D-120; TE 8.2: the removed architectures are absent by
design). `scikit-learn` is imported lazily and refuses by name when absent (shared with
`ridge.py`); its CV splitters are never used.

**R-100 — importance never reaches selection.** The fit path returns a `Prediction` and
NOTHING else. `ImportanceFigure` is produced only by `diagnostic_importance`, a separate
function no selection path calls, and it carries `authoritative = False` as a RECORDED
marker: constructing one with `authoritative=True` refuses. No importance score adds,
removes or ranks a feature into the production feature set (Vision 6.4; TE 6.4).
FR-P1-05-3's stated evidence — the feature manifest's provenance — belongs to
`features-and-splits` and is claimed by nobody here (W-10).

The forest's `random_state` is the development seed from `configs/seeds.yaml`
(NFR-DET-01) read through the snapshot — a determinism setting, not a confirmatory seed:
M-05 is unseeded in the D-122 sense and `Prediction.seed is None`.

Inputs
------
Train and score `FeatureBundle`s, the `Partition`, the `ConfigSnapshot` (grids, horizons,
`seeds.development`), the D-17 target frame, and `params` naming a grid member (R-96).

Re-run behaviour
----------------
Deterministic under the fixed development seed and `n_jobs=1`. Rows whose label is a gap are
excluded and COUNTED.

Boundaries
----------
Never imports `src.external.iri`, `src.external.gim`, `src.evaluation` or any NN stack. No
scientific constant in source.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from src.data.config import TBD_SENTINEL, IntegrityError, SeedError
from src.data.splits import Partition
from src.features.build import FeatureBundle
from src.models.ridge import require_sklearn
from src.models.train import (
    ConfigSnapshot,
    Prediction,
    assert_in_grid,
    bundle_index,
    eligible_feature_columns,
    feature_rows,
    labels_for,
    new_prediction,
    target_series,
)

__all__ = ["ImportanceFigure", "diagnostic_importance", "development_seed", "fit_predict_rows"]

GRID_TRACK: Final[str] = "random_forest"


@dataclass(frozen=True)
class ImportanceFigure:
    """`domain-entities.md` section 10: `authoritative` is ALWAYS False — a recorded marker."""

    model_id: str
    authoritative: bool
    payload_ref: str
    importances: Mapping[str, float]

    def __post_init__(self) -> None:
        if self.authoritative is not False:
            raise IntegrityError(
                "ImportanceFigure",
                "authoritative must be False: RF importance is a non-authoritative diagnostic "
                "figure and never a selection input (R-100; Vision 6.4; TE 6.4)",
            )
        if self.model_id != "M-05":
            raise IntegrityError("ImportanceFigure", "the importance figure is M-05's")


def development_seed(snapshot: ConfigSnapshot) -> int:
    """`seeds.development` (D-122) — the forest's `random_state`; never defaulted here."""
    value = snapshot.seeds.get("development")
    if value is None or (isinstance(value, str) and value.strip() == TBD_SENTINEL):
        raise SeedError(
            "configs/seeds.yaml: seeds.development",
            "missing or unresolved; the forest's random_state is the development seed from "
            "configuration, never a literal (NFR-DET-01; TC-03e)",
        )
    if isinstance(value, bool) or not isinstance(value, int):
        raise SeedError("configs/seeds.yaml: seeds.development", f"{value!r} is not an integer")
    return value


def diagnostic_importance(
    fitted_model: Any, columns: list[str], *, payload_ref: str
) -> ImportanceFigure:
    """The ONLY producer of an importance figure; called by no selection or fit path."""
    scores = getattr(fitted_model, "feature_importances_", None)
    if scores is None:
        raise IntegrityError("fitted forest", "exposes no importances to save as a diagnostic")
    return ImportanceFigure(
        model_id="M-05",
        authoritative=False,
        payload_ref=payload_ref,
        importances={c: float(s) for c, s in zip(columns, list(scores), strict=True)},
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
    requirements_path: Path | None = None,
) -> Prediction:
    """The family entry `train.fit_predict` dispatches to for M-05. Returns a `Prediction`
    ONLY — no importance score travels on any fit or selection path (R-100)."""
    if model_id != "M-05":
        raise IntegrityError(f"model_id {model_id!r}", "random_forest.py serves M-05 only")
    if params is None:
        raise IntegrityError(
            "fit_predict(M-05)",
            "a grid point {n_estimators, max_depth, min_samples_leaf, max_features} is required; "
            "a default would be a value chosen by convenience (R-96; TE 18.2)",
        )
    assert_in_grid(snapshot, GRID_TRACK, params)
    columns = list(eligible_feature_columns(bundle, horizon_hours=horizon_hours))
    missing_columns = [c for c in columns if c not in score_bundle.provenance]
    if missing_columns:
        raise IntegrityError(
            f"score bundle {score_bundle.spec.partition_id}/{score_bundle.spec.role}",
            f"lacks fitted feature column(s) {missing_columns}",
        )
    x_train = feature_rows(bundle, columns)
    x_score = feature_rows(score_bundle, columns)
    _, labels, missing_labels = labels_for(bundle, target_series(target))
    kept = [(x, y) for x, y in zip(x_train, labels, strict=True) if y is not None]
    if not kept:
        raise IntegrityError(
            f"bundle {bundle.spec.partition_id}/{bundle.spec.role}",
            "no training row carries a label; a fit over zero rows is not a fit",
        )
    random_state = development_seed(snapshot)
    require_sklearn(requirements_path)
    from sklearn.ensemble import RandomForestRegressor  # lazy: inside the fit path only

    model = RandomForestRegressor(
        n_estimators=params["n_estimators"],
        max_depth=params["max_depth"],
        min_samples_leaf=params["min_samples_leaf"],
        max_features=params["max_features"],
        random_state=random_state,
        n_jobs=1,
    )
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
            "random_state_source": "configs/seeds.yaml: seeds.development",
            "training_rows_excluded_missing_label": missing_labels,
        },
    )
