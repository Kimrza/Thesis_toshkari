"""FR-P1-04-2 / WS-11 / TA-08: the availability matrix's THREE limbs, each negative-controlled,
plus the closed-dictionary, producer, support-field and window guards of `build_features`.

PURPOSE. Every predictor is lagged to its actual availability (Kp/ap3 >= 3 h, Hp60/ap60
>= 1 h, F10.7 previous-day with a TRAILING 81-day mean) -- and those VALUES live in
`configs/features.yaml`, so this module supplies them as SYNTHETIC fixture parameters and
proves the mechanism, never the values. The three limbs (R-75, W-1a):

1. `actual_lag >= safe_lag` -- a value published after the origin FAILS;
2. trailing, never centered -- a centered window definition FAILS;
3. the ANCHOR, asserted and recomputed -- a trailing mean whose window ends at day t passes
   limbs 1 and 2 while including same-day F10.7 and FAILS here; a correct anchor whose
   values came from another window FAILS on the recomputation.

Plus: the backfill refusal (a `final` grade where `provisional` was required), the
documented-absence limb, Dst diagnostic-only, the SSN grep-class assertion over `src/`,
the R-76a alignment raise through `build_features`, the closed dictionary (`iri_*`, raw
longitude, removed row, outside row), the fail-closed permitted-producer refusal naming
WHICH rows lack entries (SD-F-01), the R-78 support-field assertions, the grid-free window,
and one full `build_features` happy path over synthetic records (stdlib representations when
pandas/numpy are absent; the governed types when present).

INPUTS. Synthetic in-memory records and configs. No December 2022 content, no restricted
root, no real config value. RE-RUN: pure functions.

WHAT NO TEST HERE DISCHARGES. WS-10, WS-11, WS-13, TA-07, TA-08, TA-33, TA-34, TA-35 and
TA-36 stay `Pending`; FR-P1-04-10 has no row. Smoke evidence only on this interpreter.

Run: pytest tests/test_feature_availability.py -rs
"""

from __future__ import annotations

import datetime as dt
import re
import sys
import tokenize
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "tests") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "tests"))

from test_split_embargo import (  # noqa: E402
    SYNTH_WINDOW_HOURS,
    SYNTH_YEAR,
    synthetic_partitions,
    synthetic_snapshot,
)

from src.data.config import (  # noqa: E402
    TBD_SENTINEL,
    AlignmentError,
    FeatureAvailabilityError,
    IntegrityError,
    LeakageError,
    PreflightError,
    RegistryError,
)
from src.data.splits import RecordFrame, partition_by_id, training_range  # noqa: E402
from src.features.availability import (  # noqa: E402
    AvailabilityRow,
    assert_anchor_recomputed,
    assert_dst_diagnostic_only,
    assert_lags_safe,
    assert_release_status_not_backfilled,
    assert_trailing_not_centered,
    build_availability_matrix,
    read_availability_lags,
)
from src.features import build  # noqa: E402
from src.features.build import (  # noqa: E402
    SECTION_6_2_ROWS,
    FrameSpec,
    build_features,
    load_feature_dictionary,
    load_permitted_producers,
)
from src.features.transforms import fit_transforms  # noqa: E402
from src.features.windows import (  # noqa: E402
    assert_window_length_grid_free,
    assert_window_parity,
    build_comparison_mask,
    build_windows,
    read_window_length,
)

UTC = dt.UTC
PARTITIONS = synthetic_partitions()

#: Synthetic lag VALUES -- fixture parameters, not the frozen ones (which are configuration).
KP_SAFE_LAG_H = 3
F107_SAFE_LAG_H = 24
F107_WINDOW_DAYS = 5
F107_TOLERANCE = 1e-9


def _ts(month: int, day: int, hour: int = 0) -> dt.datetime:
    return dt.datetime(SYNTH_YEAR, month, day, hour, tzinfo=UTC)


def _lags(**overrides: Any) -> dict[str, Any]:
    block: dict[str, Any] = {
        "kp_safe": {
            "safe_lag_hours": KP_SAFE_LAG_H,
            "release_status_required": "provisional",
        },
        "f107_81_trailing": {
            "safe_lag_hours": F107_SAFE_LAG_H,
            "release_status_required": "observed",
            "window": {
                "kind": "trailing",
                "days": F107_WINDOW_DAYS,
                "source": "f107_daily",
                "recomputation_tolerance": F107_TOLERANCE,
            },
            "publication_latency_statement": (
                "fluxtable.txt carries no publication timestamp; the conservative D+1 00:00 UTC "
                "availability convention is recorded and the publication latency is unverified"
            ),
        },
    }
    for key, value in overrides.items():
        block[key] = value
    return block


def _daily() -> list[dict[str, Any]]:
    """Ten days of synthetic daily medians, day n -> value 100 + n."""
    return [
        {"day": dt.date(SYNTH_YEAR, 2, 1) + dt.timedelta(days=n), "value": 100.0 + n}
        for n in range(10)
    ]


def _trailing_mean(end: dt.date) -> float:
    values = {row["day"]: row["value"] for row in _daily()}
    days = [end - dt.timedelta(days=k) for k in range(F107_WINDOW_DAYS)]
    return sum(values[d] for d in days) / F107_WINDOW_DAYS


def _kp_rows(lag_h: float = 3.0, grade: str = "provisional", *, publish_after: bool = False):
    rows = []
    for hour in range(3):
        origin = _ts(2, 9, 12 + hour)
        observed = origin - dt.timedelta(hours=lag_h)
        if publish_after:
            published = origin + dt.timedelta(hours=1)
        else:
            published = observed + dt.timedelta(minutes=30)
        rows.append(
            {
                "forecast_origin": origin,
                "observation_timestamp": observed,
                "publication_timestamp": published,
                "release_status": grade,
            }
        )
    return rows


def _f107_rows(anchor_offset_days: int = 1, mean_shift: float = 0.0):
    rows = []
    for hour in (6, 12):
        origin = _ts(2, 9, hour)
        anchor = origin.date() - dt.timedelta(days=anchor_offset_days)
        rows.append(
            {
                "forecast_origin": origin,
                "observation_timestamp": dt.datetime.combine(anchor, dt.time(0), tzinfo=UTC),
                "publication_timestamp": None,
                "release_status": "observed",
                "anchor_day": anchor,
                "mean_value": _trailing_mean(anchor) + mean_shift,
            }
        )
    return rows


def _drivers(**overrides: Any) -> dict[str, Any]:
    drivers: dict[str, Any] = {
        "kp_safe": _kp_rows(),
        "f107_81_trailing": _f107_rows(),
        "f107_daily": _daily(),
    }
    drivers.update(overrides)
    return drivers


# --- the config block --------------------------------------------------------------------


def test_lags_block_tbd_refuses_naming_d_10_3() -> None:
    with pytest.raises(FeatureAvailabilityError) as excinfo:
        read_availability_lags(synthetic_snapshot(features={"availability_lags": TBD_SENTINEL}))
    assert "D-10.3" in str(excinfo.value)


def test_window_fields_tbd_refuse() -> None:
    lags = _lags()
    lags["f107_81_trailing"]["window"]["recomputation_tolerance"] = TBD_SENTINEL
    with pytest.raises(FeatureAvailabilityError) as excinfo:
        read_availability_lags(synthetic_snapshot(features={"availability_lags": lags}))
    assert "recomputation_tolerance" in str(excinfo.value)


# --- the matrix and limb 1 -------------------------------------------------------------


def test_matrix_records_six_fields_plus_anchor_and_latency_statement() -> None:
    snapshot = synthetic_snapshot(features={"availability_lags": _lags()})
    matrix = build_availability_matrix(snapshot, drivers=_drivers())
    by_feature = {row.feature: row for row in matrix}
    kp = by_feature["kp_safe"]
    assert kp.safe_lag_hours == KP_SAFE_LAG_H
    assert abs(kp.actual_lag_hours - 2.5) < 1e-9
    assert kp.release_status == "provisional" and kp.publication_timestamp
    f107 = by_feature["f107_81_trailing"]
    assert f107.publication_timestamp == "" and f107.latency_statement
    assert f107.anchor_policy and "recomputed" in f107.anchor_policy
    assert isinstance(kp, AvailabilityRow)


def test_limb_1_publication_after_the_origin_fails_the_lag_assertion() -> None:
    snapshot = synthetic_snapshot(features={"availability_lags": _lags()})
    matrix = build_availability_matrix(
        snapshot, drivers=_drivers(kp_safe=_kp_rows(publish_after=True))
    )
    with pytest.raises(LeakageError) as excinfo:
        assert_lags_safe(matrix)
    assert "actual lag" in str(excinfo.value) and "kp_safe" in str(excinfo.value)


def test_limb_1_actual_lag_below_safe_lag_fails() -> None:
    snapshot = synthetic_snapshot(features={"availability_lags": _lags()})
    matrix = build_availability_matrix(snapshot, drivers=_drivers(kp_safe=_kp_rows(lag_h=1.0)))
    with pytest.raises(LeakageError):
        assert_lags_safe(matrix)


def test_limb_1_passes_when_every_lag_clears_and_records_status() -> None:
    snapshot = synthetic_snapshot(features={"availability_lags": _lags()})
    matrix = build_availability_matrix(snapshot, drivers=_drivers(kp_safe=_kp_rows(lag_h=3.5)))
    assert_lags_safe(
        matrix,
        required_release_status={"kp_safe": "provisional", "f107_81_trailing": "observed"},
    )


def test_backfilled_final_grade_fails_where_provisional_was_required() -> None:
    snapshot = synthetic_snapshot(features={"availability_lags": _lags()})
    matrix = build_availability_matrix(
        snapshot, drivers=_drivers(kp_safe=_kp_rows(lag_h=3.5, grade="final"))
    )
    with pytest.raises(LeakageError) as excinfo:
        assert_lags_safe(matrix, required_release_status={"kp_safe": "provisional"})
    assert "backfill" in str(excinfo.value).lower() or "reanalysed" in str(excinfo.value)
    with pytest.raises(LeakageError):
        assert_release_status_not_backfilled("kp_safe", "final", required="provisional")


def test_mixed_grades_within_one_series_are_refused() -> None:
    rows = _kp_rows(lag_h=3.5)
    rows[1]["release_status"] = "final"
    snapshot = synthetic_snapshot(features={"availability_lags": _lags()})
    with pytest.raises(FeatureAvailabilityError) as excinfo:
        build_availability_matrix(snapshot, drivers=_drivers(kp_safe=rows))
    assert "distinct release grades" in str(excinfo.value)


def test_missing_publication_without_a_statement_is_refused() -> None:
    lags = _lags()
    del lags["f107_81_trailing"]["publication_latency_statement"]
    snapshot = synthetic_snapshot(features={"availability_lags": lags})
    with pytest.raises(FeatureAvailabilityError) as excinfo:
        build_availability_matrix(snapshot, drivers=_drivers())
    assert "publication_latency_statement" in str(excinfo.value)


def test_a_feature_without_driver_rows_is_refused_not_assumed() -> None:
    snapshot = synthetic_snapshot(features={"availability_lags": _lags()})
    drivers = _drivers()
    del drivers["kp_safe"]
    with pytest.raises(FeatureAvailabilityError):
        build_availability_matrix(snapshot, drivers=drivers)


def test_empty_matrix_is_not_an_assertion() -> None:
    with pytest.raises(LeakageError):
        assert_lags_safe(())


# --- limb 2: trailing, never centered ------------------------------------------------------


def test_limb_2_centered_window_fails() -> None:
    with pytest.raises(LeakageError) as excinfo:
        assert_trailing_not_centered("f107_81_trailing", {"kind": "centered", "days": 81})
    assert "centered" in str(excinfo.value)
    lags = _lags()
    lags["f107_81_trailing"]["window"]["kind"] = "centered"
    snapshot = synthetic_snapshot(features={"availability_lags": lags})
    with pytest.raises(LeakageError):
        build_availability_matrix(snapshot, drivers=_drivers())


# --- limb 3: the anchor, asserted AND recomputed -------------------------------------------


def test_limb_3_anchor_at_the_origin_day_fails_where_limbs_1_and_2_pass() -> None:
    """FR-P1-04-2's named hole: a TRAILING window ending at day t includes same-day F10.7."""
    rows = _f107_rows(anchor_offset_days=0)
    # limb 2 passes (kind is trailing); limb 1 would pass on lag alone:
    assert_trailing_not_centered("f107_81_trailing", _lags()["f107_81_trailing"]["window"])
    with pytest.raises(LeakageError) as excinfo:
        assert_anchor_recomputed(
            "f107_81_trailing",
            rows,
            daily_values={r["day"]: r["value"] for r in _daily()},
            safe_lag_hours=F107_SAFE_LAG_H,
            window_days=F107_WINDOW_DAYS,
            tolerance=F107_TOLERANCE,
        )
    assert "safe-lagged day" in str(excinfo.value)


def test_limb_3_correct_anchor_wrong_values_fails_on_the_recomputation() -> None:
    """A recorded-but-wrong anchor: the end date is right, the values came from elsewhere."""
    rows = _f107_rows(mean_shift=0.5)
    with pytest.raises(LeakageError) as excinfo:
        assert_anchor_recomputed(
            "f107_81_trailing",
            rows,
            daily_values={r["day"]: r["value"] for r in _daily()},
            safe_lag_hours=F107_SAFE_LAG_H,
            window_days=F107_WINDOW_DAYS,
            tolerance=F107_TOLERANCE,
        )
    assert "recomputed" in str(excinfo.value)


def test_limb_3_passes_on_the_correct_anchor_and_values() -> None:
    assert_anchor_recomputed(
        "f107_81_trailing",
        _f107_rows(),
        daily_values={r["day"]: r["value"] for r in _daily()},
        safe_lag_hours=F107_SAFE_LAG_H,
        window_days=F107_WINDOW_DAYS,
        tolerance=F107_TOLERANCE,
    )


def test_limb_3_missing_window_day_stops_rather_than_fills() -> None:
    """TC-20 through `trailing_mean`: a gap in the window is a stop, never a fill."""
    daily = {r["day"]: r["value"] for r in _daily()}
    del daily[dt.date(SYNTH_YEAR, 2, 6)]
    with pytest.raises(IntegrityError):
        assert_anchor_recomputed(
            "f107_81_trailing",
            _f107_rows(),
            daily_values=daily,
            safe_lag_hours=F107_SAFE_LAG_H,
            window_days=F107_WINDOW_DAYS,
            tolerance=F107_TOLERANCE,
        )


def test_limb_3_unrecorded_anchor_fails() -> None:
    rows = _f107_rows()
    for row in rows:
        row["anchor_day"] = None
    with pytest.raises(LeakageError) as excinfo:
        assert_anchor_recomputed(
            "f107_81_trailing",
            rows,
            daily_values={r["day"]: r["value"] for r in _daily()},
            safe_lag_hours=F107_SAFE_LAG_H,
            window_days=F107_WINDOW_DAYS,
            tolerance=F107_TOLERANCE,
        )
    assert "unrecorded anchor" in str(excinfo.value)


def test_trailing_row_without_anchor_record_fails_lags_safe() -> None:
    row = AvailabilityRow(
        feature="f107_81_trailing",
        observation_timestamp="x",
        publication_timestamp="",
        release_status="observed",
        safe_lag_hours=24.0,
        actual_lag_hours=30.0,
        anchor_policy=None,
        latency_statement="documented absence",
    )
    with pytest.raises(LeakageError) as excinfo:
        assert_lags_safe((row,))
    assert "third limb" in str(excinfo.value)


# --- Dst diagnostic-only; SSN absent (grep-class) ----------------------------------------


def test_dst_declared_as_a_model_input_fails() -> None:
    with pytest.raises(LeakageError):
        assert_dst_diagnostic_only({"dst_index": "driver"})
    assert_dst_diagnostic_only({"dst_index": "diagnostic", "kp_safe": "driver"}) is None


def test_ssn_is_absent_from_src_identifiers_and_the_dictionary_rows() -> None:
    """TA-08's grep-class limb: no identifier or string field name under src/ names SSN, and
    the closed row table carries no ssn row (it is REMOVED, and declaring it raises)."""
    needle = "ssn"
    hits: list[str] = []
    for module in sorted((REPO_ROOT / "src").rglob("*.py")):
        with tokenize.open(module) as handle:
            for token in tokenize.generate_tokens(handle.readline):
                if token.type == tokenize.NAME and needle in token.string.lower().split("_"):
                    hits.append(f"{module.relative_to(REPO_ROOT).as_posix()}:{token.start[0]}")
    assert hits == [], f"SSN identifiers found under src/: {hits}"
    assert needle not in SECTION_6_2_ROWS
    snapshot = synthetic_snapshot(
        features={
            "feature_dictionary": {
                "ssn_daily": {"dictionary_row": "ssn", "normalization": "none"},
            }
        }
    )
    with pytest.raises(LeakageError) as excinfo:
        load_feature_dictionary(snapshot)
    assert "REMOVED" in str(excinfo.value)


# --- the closed dictionary (R-76; TA-33's subject) --------------------------------------


def _dictionary(**extra: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "vtec_lag_1h": {
            "dictionary_row": "vtec_lag",
            "lag_hours": 1,
            "source_column": "vtec_tecu",
            "normalization": "train_only_standardize",
        },
        "vtec_lag_3h": {
            "dictionary_row": "vtec_lag",
            "lag_hours": 3,
            "source_column": "vtec_tecu",
            "normalization": "train_only_standardize",
        },
        "vtec_seq_24": {
            "dictionary_row": "vtec_seq_24",
            "sequence_steps": SYNTH_WINDOW_HOURS,
            "source_column": "vtec_tecu",
            "normalization": "train_only_standardize",
        },
        "utc_hour_sin": {"dictionary_row": "utc_hour_sin", "normalization": "none"},
        "utc_hour_cos": {"dictionary_row": "utc_hour_cos", "normalization": "none"},
        "kp_safe": {
            "dictionary_row": "kp_safe",
            "source_series": "kp",
            "normalization": "none",
        },
    }
    base.update(extra)
    return base


def _producers() -> dict[str, list[str]]:
    return {
        "vtec_lag": ["phase1_hourly_target"],
        "vtec_seq_24": ["phase1_hourly_target"],
        "utc_hour_sin": ["record_timestamp"],
        "utc_hour_cos": ["record_timestamp"],
        "kp_safe": ["gfz_kp_provisional"],
    }


def test_dictionary_tbd_is_a_preflight_stop() -> None:
    with pytest.raises(PreflightError):
        load_feature_dictionary(synthetic_snapshot(features={"feature_dictionary": TBD_SENTINEL}))


def test_field_outside_the_dictionary_raises() -> None:
    snapshot = synthetic_snapshot(
        features={
            "feature_dictionary": _dictionary(
                cloud_cover={"dictionary_row": "cloud", "normalization": "none"}
            )
        }
    )
    with pytest.raises(LeakageError) as excinfo:
        load_feature_dictionary(snapshot)
    assert "outside the TE 6.2 dictionary" in str(excinfo.value)


def test_iri_field_injected_into_the_dictionary_raises() -> None:
    """WS-10's data-flow limb: the denial mechanism rejects a deliberately injected iri_*."""
    snapshot = synthetic_snapshot(
        features={
            "feature_dictionary": _dictionary(
                iri_vtec={
                    "dictionary_row": "kp_safe",
                    "source_series": "iri",
                    "normalization": "none",
                }
            )
        }
    )
    with pytest.raises(LeakageError) as excinfo:
        load_feature_dictionary(snapshot)
    assert "NFR-IRI-01" in str(excinfo.value)


def test_raw_longitude_column_raises() -> None:
    for name in ("station_lon", "glon", "longitude"):
        snapshot = synthetic_snapshot(
            features={
                "feature_dictionary": _dictionary(
                    **{name: {"dictionary_row": "station_lat", "normalization": "none"}}
                )
            }
        )
        with pytest.raises(LeakageError) as excinfo:
            load_feature_dictionary(snapshot)
        assert "lst_sin and lst_cos" in str(excinfo.value)


def test_lag_name_must_match_its_declared_lag() -> None:
    bad = _dictionary()
    bad["vtec_lag_3h"]["lag_hours"] = 2
    with pytest.raises(LeakageError):
        load_feature_dictionary(synthetic_snapshot(features={"feature_dictionary": bad}))


def test_normalization_must_be_declared() -> None:
    bad = _dictionary()
    del bad["kp_safe"]["normalization"]
    with pytest.raises(LeakageError):
        load_feature_dictionary(synthetic_snapshot(features={"feature_dictionary": bad}))


# --- the permitted-producer list (SD-F-01): fail closed, naming the rows ------------------


def test_permitted_producers_tbd_names_every_row_lacking_an_entry() -> None:
    snapshot = synthetic_snapshot(features={"permitted_producers": TBD_SENTINEL})
    with pytest.raises(LeakageError) as excinfo:
        load_permitted_producers(snapshot, dictionary_rows=["vtec_lag", "kp_safe"])
    message = str(excinfo.value)
    assert "kp_safe" in message and "vtec_lag" in message
    assert "No feature matrix is produced" in message


def test_permitted_producers_incomplete_names_only_the_missing_rows() -> None:
    snapshot = synthetic_snapshot(features={"permitted_producers": {"vtec_lag": ["target"]}})
    with pytest.raises(LeakageError) as excinfo:
        load_permitted_producers(snapshot, dictionary_rows=["vtec_lag", "kp_safe", "doy_sin"])
    message = str(excinfo.value)
    assert "['doy_sin', 'kp_safe']" in message and "'vtec_lag'" not in message.split("row(s)")[1]


#: The eleven dictionary rows whose PRODUCING ARTIFACT the implemented contract itself
#: fixes, and the producer each takes — transcribed by the owner's ruling of 2026-09-10
#: (D-35, adopted 2026-09-10). Enumerated here literally, never imported from the
#: config it checks (that would be circular).
_CONTRACT_FIXED_PRODUCERS: dict[str, str] = {
    "vtec_lag": "phase1_hourly_target",
    "vtec_seq_24": "phase1_hourly_target",
    "target_support": "phase1_hourly_target",
    "utc_hour_sin": "record_timestamp",
    "utc_hour_cos": "record_timestamp",
    "doy_sin": "record_timestamp",
    "doy_cos": "record_timestamp",
    "lst_sin": "station_registry",
    "lst_cos": "station_registry",
    "station_onehot": "station_registry",
    "station_lat": "station_registry",
}
#: The seven driver-class rows deliberately left unassigned until the driver release
#: exists (D-35 limb 3): NOT rejected on policy grounds, and still fail-closed.
_DEFERRED_DRIVER_ROWS: tuple[str, ...] = (
    "kp_safe",
    "ap_safe",
    "hp60_safe",
    "ap60_safe",
    "f107_safe",
    "f107_81_trailing",
    "dst",
)


def test_permitted_producers_real_features_yaml_carries_exactly_the_contract_fixed_rows() -> (
    None
):
    """Owner ruling 2026-09-10, adopted as D-35: the repository's own block now carries the
    eleven contract-fixed rows with their contract-fixed producers, and NOTHING else.

    Asserted by set-difference in both directions, so an added row (a producer assigned
    without a decision) and a dropped row both fail. The producer strings are compared to
    the code constants they transcribe, so config and code cannot drift apart.
    """
    pytest.importorskip("yaml")
    producers = load_permitted_producers(REPO_ROOT / "configs")
    missing = sorted(set(_CONTRACT_FIXED_PRODUCERS) - set(producers))
    extra = sorted(set(producers) - set(_CONTRACT_FIXED_PRODUCERS))
    assert missing == [] and extra == [], f"missing {missing}, extra {extra}"
    for row, expected in _CONTRACT_FIXED_PRODUCERS.items():
        assert tuple(producers[row]) == (expected,), row
    # the transcription agrees with the code constants it came from
    assert build.STATION_REGISTRY_PRODUCER == "station_registry"
    assert build.TIMESTAMP_PRODUCER == "record_timestamp"


def test_permitted_producers_still_fails_closed_on_every_deferred_driver_row() -> None:
    """The seven driver rows are UNASSIGNED, not admitted: any run requesting one refuses
    naming exactly the missing rows, and no feature matrix is produced (SD-F-01)."""
    pytest.importorskip("yaml")
    for row in _DEFERRED_DRIVER_ROWS:
        with pytest.raises(LeakageError) as excinfo:
            load_permitted_producers(REPO_ROOT / "configs", dictionary_rows=["vtec_lag", row])
        message = str(excinfo.value)
        assert row in message and "no feature matrix is produced" in message.lower()


def test_permitted_producers_admit_no_removed_or_iri_or_longitude_row() -> None:
    """The leakage-safe policy's absolute exclusions cannot enter THROUGH the block: a
    REMOVED row (`ssn`), an `iri_*` row and a raw-longitude row are all outside the TE 6.2
    dictionary, so the loader refuses them by name rather than admitting a producer."""
    for forbidden in ("ssn", "iri_vtec", "glon", "longitude"):
        snapshot = synthetic_snapshot(
            features={"permitted_producers": {forbidden: ["some_artifact"]}}
        )
        with pytest.raises(LeakageError):
            load_permitted_producers(snapshot)
    assert "ssn" in build.REMOVED_ROWS
    assert not set(_CONTRACT_FIXED_PRODUCERS) & set(build.REMOVED_ROWS)


def test_permitted_producers_row_outside_dictionary_refused() -> None:
    snapshot = synthetic_snapshot(features={"permitted_producers": {"cloud": ["x"]}})
    with pytest.raises(LeakageError):
        load_permitted_producers(snapshot)


def test_build_features_refuses_at_the_producer_list_before_producing_anything() -> None:
    snapshot = synthetic_snapshot(
        features={"feature_dictionary": _dictionary(), "permitted_producers": TBD_SENTINEL}
    )
    start, end = training_range(partition_by_id(PARTITIONS, "F1"))
    with pytest.raises(LeakageError) as excinfo:
        build_features(
            [],
            drivers={},
            registry={},
            matrix=(),
            spec=FrameSpec("F1", "train", start, end),
            partitions=PARTITIONS,
            snapshot=snapshot,
        )
    assert "permitted_producers" in str(excinfo.value)


# --- R-78: support fields, four rules, separate failures -----------------------------------


def _support(**fields: Any) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "dictionary_row": "target_support",
        "source_column": "valid_observation_count",
        "normalization": "none",
        "lag_hours": 1,
    }
    entry.update(fields)
    return entry


def _features_with_support(support_entry: dict[str, Any], *, freeze: Any = None) -> dict[str, Any]:
    features: dict[str, Any] = {
        "feature_dictionary": _dictionary(support_count=support_entry),
        "permitted_producers": {**_producers(), "target_support": ["phase1_hourly_target"]},
        "carry_forward_bound_hours": 3,
    }
    if freeze is not None:
        features["feature_set_freeze_utc"] = freeze
    return features


def _happy_inputs(snapshot):
    """Synthetic target + driver inputs for F1's training range over one station."""
    f1 = partition_by_id(PARTITIONS, "F1")
    start, end = training_range(f1)
    hours = int((end - start).total_seconds() // 3600)
    target = RecordFrame(
        {
            "interval_start_utc": (start + dt.timedelta(hours=h)).isoformat(),
            "station_id": "S1",
            "vtec_tecu": 10.0 + (h % 17) * 0.5,
            "valid_observation_count": 5 + (h % 3),
            "phase_id": "phase1",
            "source_id": "synthetic",
            "target_definition_id": "synthetic-gridded",
        }
        for h in range(hours)
    )
    target.attrs["producing_artifact"] = "phase1_hourly_target"
    kp = RecordFrame(
        {"interval_start_utc": (start + dt.timedelta(hours=h)).isoformat(), "value": float(h % 9)}
        for h in range(hours)
    )
    kp.attrs["producing_artifact"] = "gfz_kp_provisional"
    matrix = (
        AvailabilityRow(
            feature="kp_safe",
            observation_timestamp="x",
            publication_timestamp="y",
            release_status="provisional",
            safe_lag_hours=3.0,
            actual_lag_hours=3.5,
        ),
    )
    return target, {"kp": kp}, matrix, FrameSpec("F1", "train", start, end)


def _run_build(features: dict[str, Any], **kwargs: Any):
    snapshot = synthetic_snapshot(features=features)
    target, drivers, matrix, spec = _happy_inputs(snapshot)
    return build_features(
        target,
        drivers=drivers,
        registry={},
        matrix=matrix,
        spec=kwargs.pop("spec", spec),
        partitions=PARTITIONS,
        snapshot=snapshot,
        parity_tolerance=kwargs.pop("parity_tolerance", 0.0),
        **kwargs,
    )


def test_support_field_without_approval_is_not_in_the_feature_set_at_all() -> None:
    bundle = _run_build(_features_with_support(_support()))
    assert "support_count" not in bundle.provenance


def test_target_hour_quality_field_is_permanently_forbidden_even_when_approved() -> None:
    entry = _support(
        support_kind="target_hour_quality",
        approval={"approval_id": "G-04-001", "recorded_utc": "2001-01-01T00:00:00Z"},
    )
    with pytest.raises(LeakageError) as excinfo:
        _run_build(_features_with_support(entry, freeze="2001-02-01T00:00:00Z"))
    assert "permanently forbidden" in str(excinfo.value)


def test_approval_recorded_after_the_freeze_fails_on_ordering() -> None:
    entry = _support(approval={"approval_id": "G-04-001", "recorded_utc": "2001-03-01T00:00:00Z"})
    with pytest.raises(LeakageError) as excinfo:
        _run_build(_features_with_support(entry, freeze="2001-02-01T00:00:00Z"))
    assert "PRECEDE" in str(excinfo.value)


def test_approval_without_id_or_timestamp_fails_separately() -> None:
    with pytest.raises(LeakageError) as excinfo:
        _run_build(
            _features_with_support(
                _support(approval={"recorded_utc": "2001-01-01T00:00:00Z"}),
                freeze="2001-02-01T00:00:00Z",
            )
        )
    assert "approval_id" in str(excinfo.value)
    with pytest.raises(LeakageError) as excinfo2:
        _run_build(
            _features_with_support(
                _support(approval={"approval_id": "G-04-001"}), freeze="2001-02-01T00:00:00Z"
            )
        )
    assert "recorded_utc" in str(excinfo2.value)


def test_support_read_at_hour_t_fails() -> None:
    entry = _support(
        lag_hours=0,
        approval={"approval_id": "G-04-001", "recorded_utc": "2001-01-01T00:00:00Z"},
    )
    with pytest.raises(LeakageError) as excinfo:
        _run_build(_features_with_support(entry, freeze="2001-02-01T00:00:00Z"))
    assert "hours <= t" in str(excinfo.value)


def test_approved_lagged_support_field_enters_with_its_provenance() -> None:
    entry = _support(approval={"approval_id": "G-04-001", "recorded_utc": "2001-01-01T00:00:00Z"})
    bundle = _run_build(_features_with_support(entry, freeze="2001-02-01T00:00:00Z"))
    assert bundle.provenance["support_count"]["dictionary_row"] == "target_support"


# --- the window: frozen, grid-free, one definition, parity --------------------------------


def test_window_length_tbd_or_disagreeing_with_the_dictionary_fails() -> None:
    with pytest.raises(LeakageError):
        read_window_length(
            synthetic_snapshot(experiment={"window_length_hours": TBD_SENTINEL}),
            sequence_steps=SYNTH_WINDOW_HOURS,
        )
    with pytest.raises(LeakageError) as excinfo:
        read_window_length(synthetic_snapshot(), sequence_steps=SYNTH_WINDOW_HOURS + 1)
    assert "disagrees" in str(excinfo.value)


def test_window_length_placed_in_a_grid_fails() -> None:
    grids = {"M-06": {"units": [16, 32], "window_length_hours": [24, 48]}}
    with pytest.raises(LeakageError) as excinfo:
        assert_window_length_grid_free({"grids": grids})
    assert "grid" in str(excinfo.value)
    with pytest.raises(LeakageError):
        read_window_length(
            synthetic_snapshot(experiment={"grids": grids}), sequence_steps=SYNTH_WINDOW_HOURS
        )
    assert_window_length_grid_free({"grids": {"M-04": {"alpha": [0.1, 1.0]}}}) is None


def test_one_definition_emits_both_representations_and_counts_exclusions() -> None:
    start = _ts(3, 1)
    records = [
        {
            "interval_start_utc": (start + dt.timedelta(hours=h)).isoformat(),
            "station_id": "S1",
            "v": float(h),
        }
        for h in range(30)
        if h != 20  # one missing epoch -> incomplete windows for rows 21..(20+W)
    ]
    result = build_windows(
        records,
        window_hours=4,
        sequence_fields={"v_seq": "v"},
        lag_fields={"v_lag_2h": ("v", 2)},
        scored_start=start,
        scored_end=start + dt.timedelta(hours=30),
    )
    assert result.excluded_before_scored_start == 4  # rows 0..3 reach before the start
    assert result.excluded_incomplete_windows == 4  # rows 21..24 need epoch 20
    row = result.records[0]  # epoch 4: window is epochs 0..3
    assert row["v_seq_t-1"] == 3.0 and row["v_seq_t-4"] == 0.0 and row["v_lag_2h"] == 2.0
    assert_window_parity(
        result.records,
        result.tensor,
        sequence_columns=result.sequence_columns,
        tensor_features=result.tensor_features,
        tolerance=0.0,
    )


def test_lag_beyond_the_window_cannot_come_from_one_definition() -> None:
    with pytest.raises(LeakageError):
        build_windows(
            [],
            window_hours=4,
            sequence_fields={"v_seq": "v"},
            lag_fields={"v_lag_5h": ("v", 5)},
            scored_start=_ts(3, 1),
            scored_end=_ts(3, 2),
        )


def test_parity_value_limb_stops_naming_the_te_15_2_field_when_tolerance_is_unset() -> None:
    records = [{"v_seq_t-1": 1.0, "v_seq_t-2": 0.0}]
    tensor = [[[0.0], [1.0]]]
    with pytest.raises(IntegrityError) as excinfo:
        assert_window_parity(
            records,
            tensor,
            sequence_columns={"v_seq": ("v_seq_t-2", "v_seq_t-1")},
            tensor_features=("v_seq",),
            tolerance=None,
        )
    assert "permitted_floating_point_tolerances" in str(excinfo.value)


def test_parity_shape_then_value_failures_are_distinguished() -> None:
    records = [{"v_seq_t-1": 1.0, "v_seq_t-2": 0.0}]
    with pytest.raises(LeakageError) as shape:
        assert_window_parity(
            records,
            [[[0.0], [1.0]], [[0.0], [1.0]]],
            sequence_columns={"v_seq": ("v_seq_t-2", "v_seq_t-1")},
            tensor_features=("v_seq",),
            tolerance=0.0,
        )
    assert "shape" in str(shape.value)
    with pytest.raises(LeakageError) as value:
        assert_window_parity(
            records,
            [[[0.0], [5.0]]],
            sequence_columns={"v_seq": ("v_seq_t-2", "v_seq_t-1")},
            tensor_features=("v_seq",),
            tolerance=0.0,
        )
    assert "value" in str(value.value)


# --- build_features end to end over synthetic records --------------------------------------


def _base_features() -> dict[str, Any]:
    return {
        "feature_dictionary": _dictionary(),
        "permitted_producers": _producers(),
        "carry_forward_bound_hours": 3,
    }


def test_build_features_happy_path_stamps_provenance_equal_to_columns() -> None:
    bundle = _run_build(_base_features())
    from src.features._frames import columns_of

    keys = ("interval_start_utc", "station_id")
    feature_columns = [c for c in columns_of(bundle.matrix) if c not in keys]
    assert set(feature_columns) == set(bundle.provenance)
    assert bundle.transform_id is None
    assert bundle.identity == {
        "phase_id": "phase1",
        "source_id": "synthetic",
        "target_definition_id": "synthetic-gridded",
    }
    assert bundle.excluded_counts["excluded_before_scored_start"] == SYNTH_WINDOW_HOURS
    assert bundle.provenance["kp_safe"] == {
        "dictionary_row": "kp_safe",
        "dictionary_field": "kp_safe",
        "producing_artifact": "gfz_kp_provisional",
    }
    assert len(bundle.sequence_columns["vtec_seq_24"]) == SYNTH_WINDOW_HOURS


def test_three_call_sequence_fits_then_transforms_both_representations() -> None:
    features = _base_features()
    raw = _run_build(features)
    f1 = partition_by_id(PARTITIONS, "F1")
    transform = fit_transforms(raw, partition=f1)
    train = _run_build(features, transform=transform)
    assert train.transform_id == "T-F1"
    from src.features._frames import column_values, tensor_as_nested

    values = column_values(train.matrix, "vtec_lag_1h")
    assert abs(sum(values) / len(values)) < 1e-9  # standardised on its own training range
    nested = tensor_as_nested(train.tensor)
    idx = train.sequence_columns["vtec_seq_24"].index("vtec_seq_24_t-1")
    assert abs(nested[0][idx][0] - column_values(train.matrix, "vtec_seq_24_t-1")[0]) < 1e-9


def test_unpermitted_producer_for_a_row_is_refused() -> None:
    features = _base_features()
    features["permitted_producers"]["kp_safe"] = ["some_other_artifact"]
    with pytest.raises(LeakageError) as excinfo:
        _run_build(features)
    assert "not a permitted producer" in str(excinfo.value)


def test_absent_provenance_on_an_input_fails() -> None:
    snapshot = synthetic_snapshot(features=_base_features())
    target, drivers, matrix, spec = _happy_inputs(snapshot)
    drivers["kp"].attrs.pop("producing_artifact")
    with pytest.raises(LeakageError) as excinfo:
        build_features(
            target,
            drivers=drivers,
            registry={},
            matrix=matrix,
            spec=spec,
            partitions=PARTITIONS,
            snapshot=snapshot,
            parity_tolerance=0.0,
        )
    assert "ABSENT provenance FAILS" in str(excinfo.value)


def test_driver_without_an_availability_row_is_refused() -> None:
    snapshot = synthetic_snapshot(features=_base_features())
    target, drivers, _, spec = _happy_inputs(snapshot)
    with pytest.raises(LeakageError) as excinfo:
        build_features(
            target,
            drivers=drivers,
            registry={},
            matrix=(),
            spec=spec,
            partitions=PARTITIONS,
            snapshot=snapshot,
            parity_tolerance=0.0,
        )
    assert "availability-matrix row" in str(excinfo.value)


def test_driver_repeated_outside_its_interval_raises_alignment_error() -> None:
    """R-76a's enforcement raise through build_features (TA-36's subject)."""
    snapshot = synthetic_snapshot(features=_base_features())
    target, drivers, matrix, spec = _happy_inputs(snapshot)
    start = spec.scored_start
    drivers["kp"].attrs["observations"] = [
        {"value": 0.0, "interval_start": start, "interval_end": start + dt.timedelta(hours=3)},
    ]
    with pytest.raises(AlignmentError):
        build_features(
            target,
            drivers=drivers,
            registry={},
            matrix=matrix,
            spec=spec,
            partitions=PARTITIONS,
            snapshot=snapshot,
            parity_tolerance=0.0,
        )


def test_station_fields_are_blocked_by_an_unresolved_registry() -> None:
    features = _base_features()
    features["feature_dictionary"]["station_lat"] = {
        "dictionary_row": "station_lat",
        "normalization": "none",
    }
    features["permitted_producers"]["station_lat"] = ["station_registry"]
    with pytest.raises(RegistryError):
        _run_build(features)


def test_carry_forward_bound_tbd_refuses() -> None:
    features = _base_features()
    features["carry_forward_bound_hours"] = TBD_SENTINEL
    with pytest.raises(LeakageError) as excinfo:
        _run_build(features)
    assert "carry_forward_bound_hours" in str(excinfo.value)


def test_score_spec_exceeding_the_validation_month_raises() -> None:
    f1 = partition_by_id(PARTITIONS, "F1")
    spec = FrameSpec("F1", "score", _ts(4, 1), _ts(5, 2))
    with pytest.raises(LeakageError):
        _run_build(_base_features(), spec=spec)
    assert f1.validation_month == dt.date(SYNTH_YEAR, 4, 1)


def test_comparison_mask_is_the_intersection_with_three_stamps() -> None:
    identity = {"phase_id": "p", "source_id": "s", "target_definition_id": "t"}
    rows_a = [("S1", _ts(4, 2, h)) for h in range(5)]
    rows_b = [("S1", _ts(4, 2, h)) for h in range(2, 7)]
    mask = build_comparison_mask(
        {"M-01": rows_a, "M-06": rows_b}, comparison_set_id="cs1", identity=identity
    )
    assert mask.kept_count == 3 and mask.members == ("M-01", "M-06")
    from src.data.config import FairnessError

    with pytest.raises(FairnessError):
        build_comparison_mask({"M-01": rows_a}, comparison_set_id="cs1", identity=identity)
    with pytest.raises(FairnessError):
        build_comparison_mask(
            {"M-01": rows_a, "M-06": rows_b}, comparison_set_id="cs1", identity={"phase_id": "p"}
        )


def test_no_iri_or_gim_import_under_src_features() -> None:
    """The module-graph limb is external-products' scan; this is the local restatement."""
    pattern = re.compile(
        r"^\s*(?:from src\.external\.(?:iri|gim)\b|import src\.external\.(?:iri|gim)\b"
        r"|from src\.external import [^\n]*\b(?:iri|gim)\b)",
        re.MULTILINE,
    )
    for module in sorted((REPO_ROOT / "src" / "features").rglob("*.py")):
        assert not pattern.search(module.read_text(encoding="utf-8")), module
