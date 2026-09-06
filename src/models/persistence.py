"""M-01 persistence and M-02 24-hour seasonal persistence: the two unfitted difficulty controls.

Purpose
-------
`domain-entities.md` section 1 (W-2; R-98's companion controls; Vision 2.4's binding honesty
rule co-reports both in the primary results table, which `regimes-diagnostics-reporting`
owns). Neither family has fitted state and neither is seeded: `Prediction.seed is None` is
correct for both.

* **M-01 persistence**: the forecast for hour `t` at horizon `h` is the observed target at
  the forecast origin, `y(t - h)`.
* **M-02 24-hour seasonal persistence**: the forecast for hour `t` is the observed target one
  seasonal period earlier — the smallest multiple of a day that is at least the horizon, so
  the value is observable at the origin (`y(t - 24)` at `h = 1`).

Both read the RAW-TECU target series supplied by the caller (the D-17 target frame), not the
bundle's `vtec_lag_*` columns: those columns are standardised under the bundle's
`transform_id` for ridge/LSTM (TE 6.2) and no inverse exists (D-27), so a persistence forecast
read from them would be in standardised units. The bundle supplies WHICH rows are predicted
(its `(station, interval_start_utc)` index, its `partition_id` and `transform_id` stamps); the
series supplies the values.

Inputs
------
A consumable score-role `FeatureBundle`, the `Partition` being scored, the `ConfigSnapshot`
(for the horizon only), the D-17 target frame, and the horizon in hours. No hyperparameters:
a `params` argument is refused.

Re-run behaviour
----------------
Pure functions; deterministic; nothing persisted. A missing source value yields `y_hat = None`
and is COUNTED on the prediction frame's attrs (`missing_source_values`) — a completeness
shortfall recorded machine-readably, never console text (team.md two-tier posture).

Boundaries
----------
No scientific constant: the horizon and the seasonal period reach this module as parameters
or as a calendar fact (hours per day), flagged below for the reviewer. Never imports
`src.external.iri`, `src.external.gim`, `src.evaluation` or any NN stack.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Mapping
from typing import Any, Final

from src.data.config import IntegrityError
from src.data.splits import Partition
from src.features.build import FeatureBundle
from src.models.train import (
    ConfigSnapshot,
    Prediction,
    bundle_index,
    new_prediction,
    target_series,
)

__all__ = [
    "HOURS_PER_DAY",
    "seasonal_lag_hours",
    "persistence_rows",
    "fit_predict_rows",
]

#: Hours in a day — calendar arithmetic (the "24-hour" in M-02's family name, D-120), not a
#: TC-03e scientific constant; flagged for the reviewer exactly as `features-and-splits`
#: flagged its hours-per-day and degrees-per-hour facts.
HOURS_PER_DAY: Final[int] = 24


def seasonal_lag_hours(horizon_hours: int) -> int:
    """The smallest whole number of days, in hours, that is at least the horizon — so the
    seasonal value is observable at the forecast origin."""
    if isinstance(horizon_hours, bool) or not isinstance(horizon_hours, int) or horizon_hours <= 0:
        raise IntegrityError("horizon_hours", f"{horizon_hours!r} is not a positive integer")
    days = -(-horizon_hours // HOURS_PER_DAY)  # ceiling division
    return days * HOURS_PER_DAY


def persistence_rows(
    score_bundle: FeatureBundle,
    *,
    series: Mapping[tuple[str, dt.datetime], float],
    lag_hours: int,
) -> tuple[list[dict[str, Any]], int]:
    """`y_hat(t) = y(t - lag_hours)` for every row of the scored bundle; misses counted."""
    rows: list[dict[str, Any]] = []
    missing = 0
    offset = dt.timedelta(hours=lag_hours)
    for station, stamp in bundle_index(score_bundle):
        value = series.get((station, stamp - offset))
        if value is None:
            missing += 1
        rows.append({"station": station, "interval_start_utc": stamp, "y_hat": value})
    return rows, missing


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
) -> Prediction:
    """The family entry `train.fit_predict` dispatches to for M-01 and M-02."""
    if model_id not in ("M-01", "M-02"):
        raise IntegrityError(f"model_id {model_id!r}", "persistence.py serves M-01 and M-02 only")
    if params is not None:
        raise IntegrityError(
            f"fit_predict({model_id})",
            "persistence has no hyperparameters; a params argument here is a value chosen by "
            "convenience",
        )
    series = target_series(target)
    lag = horizon_hours if model_id == "M-01" else seasonal_lag_hours(horizon_hours)
    rows, missing = persistence_rows(score_bundle, series=series, lag_hours=lag)
    return new_prediction(
        model_id,
        seed=None,
        rows=rows,
        bundle=score_bundle,
        partition=partition,
        attrs={
            "role": score_bundle.spec.role,
            "horizon_hours": horizon_hours,
            "lag_hours": lag,
            "missing_source_values": missing,
        },
    )
