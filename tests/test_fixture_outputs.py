"""Regression tests for `src/data/fixture_outputs.py` (TE §15.4 fixture-root outputs), the
data-drawing figure renderer in `src/evaluation/plots.py`, and the cross-run measurement
plumbing added to `src/data/fixture_manifest.py` (CR-2026-09-29-Q31-CLOSURE).

Every writer exports content a stage already produced — byte copy, lossless re-encoding or
aggregation — and is write-once. Status artifacts record non-execution without inventing a
statistic. Tolerances are measured across recorded runs, never declared, and the
UNCHANGED ledger validator still refuses a non-positive tolerance (negative control).

CONSTANTS CONVENTION. Synthetic apparatus only (R-122): no scientific value, no December
2022 content, no restricted path. RE-RUN BEHAVIOUR. Pure: every tree lives under tmp_path.
"""

from __future__ import annotations

import datetime as dt
import json
import math
from pathlib import Path

import pytest
from src.data.config import IntegrityError, RegimeError
from src.data.fixture_outputs import (
    STAGE_MEASUREMENTS_DIR,
    copy_once,
    cross_run_variation,
    export_bootstrap_not_executed,
    export_checkpoint_manifest,
    export_feature_table,
    export_hourly_vtec,
    export_iri_benchmark,
    export_mask_manifest,
    export_metrics,
    export_predictions,
    gim_measurements,
    iri_measurements,
    iri_rows_in_scope,
    numeric_fingerprint,
    target_measurements,
    write_stage_measurements,
)

pd = pytest.importorskip("pandas")
pytest.importorskip("pyarrow")

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _target_csv(tmp_path: Path) -> Path:
    path = tmp_path / "hourly_target_phase1.csv"
    path.write_text(
        "interval_start_utc,station_id,vtec_tecu,valid_observation_count,"
        "within_hour_spread_tecu,provider_dtec_summary,target_valid\n"
        "2022-11-01T00:00:00Z,BSHM,7.03719,12,0.5,1.1,True\n"
        "2022-11-01T01:00:00Z,BSHM,6.468905,9,0.25,0.9,True\n"
        "2022-11-01T02:00:00Z,BSHM,,0,,,False\n",
        encoding="utf-8",
    )
    return path


# --- 02: hourly_vtec.parquet and target measurements ---------------------------------


def test_hourly_vtec_is_a_lossless_reencoding_of_the_released_csv(tmp_path: Path) -> None:
    csv = _target_csv(tmp_path)
    out = export_hourly_vtec(csv, tmp_path / "root")
    assert out.name == "hourly_vtec.parquet"
    exported, source = pd.read_parquet(out), pd.read_csv(csv)
    assert list(exported.columns) == list(source.columns)
    pd.testing.assert_frame_equal(exported, source)
    assert exported["vtec_tecu"].iloc[1] == 6.468905  # float repr round-trips exactly


def test_hourly_vtec_is_write_once(tmp_path: Path) -> None:
    csv = _target_csv(tmp_path)
    export_hourly_vtec(csv, tmp_path / "root")
    with pytest.raises(IntegrityError, match="written exactly once"):
        export_hourly_vtec(csv, tmp_path / "root")


def test_target_measurements_are_read_from_the_released_rows(tmp_path: Path) -> None:
    m = target_measurements(_target_csv(tmp_path))
    assert m["row_count_ranges"]["hourly_target"] == {"min": 3.0, "max": 3.0, "units": "rows"}
    assert m["support_missingness"]["target_support"]["min"] == 9.0
    assert m["support_missingness"]["target_support"]["max"] == 12.0
    assert m["support_missingness"]["invalid_hour"]["max"] == 1.0
    assert m["timestamp_tolerances"]["hourly_boundary"] == {"min": 0.0, "max": 0.0, "units": "s"}


# --- stage measurement blocks --------------------------------------------------------


def test_stage_measurements_land_where_the_collector_looks(tmp_path: Path) -> None:
    from src.data.fixture_manifest import collect_stage_measurements

    write_stage_measurements(
        tmp_path, stage="02_x", measurements={"row_count_ranges": {"hourly_target": {"min": 1, "max": 2, "units": "rows"}}}
    )
    assert (tmp_path / STAGE_MEASUREMENTS_DIR / "02_x" / "fixture_measurements.json").is_file()
    merged = collect_stage_measurements(tmp_path)
    assert merged["row_count_ranges"]["hourly_target"]["max"] == 2.0


@pytest.mark.parametrize(
    "value",
    [{"max": 1, "units": "rows"}, {"min": "1", "max": 2}, {"min": float("nan"), "max": 1}, {"min": True, "max": 1}],
)
def test_stage_measurements_refuse_a_value_that_is_not_a_measured_range(tmp_path: Path, value) -> None:
    with pytest.raises(IntegrityError):
        write_stage_measurements(tmp_path, stage="s", measurements={"a": {"q": value}})


# --- 04: iri_benchmark.parquet, IRI/GIM timestamp measurements -----------------------


def _b01_rows(tmp_path: Path) -> Path:
    path = tmp_path / "rows.jsonl"
    rows = [
        {"station_id": "BSHM", "target_time_utc": "2022-11-01T12:00:00+00:00", "status": "ok", "iri2016_t_plus_1_tecu": 38.18},
        {"station_id": "BSHM", "target_time_utc": "2022-11-01T11:00:00+00:00", "status": "ok", "iri2016_t_plus_1_tecu": 37.0},
        {"station_id": "BSHM", "target_time_utc": "2022-11-09T00:00:00+00:00", "status": "ok", "iri2016_t_plus_1_tecu": 1.0},
        {"station_id": "ARUC", "target_time_utc": "2022-11-01T12:00:00+00:00", "status": "ok", "iri2016_t_plus_1_tecu": 2.0},
        {"station_id": "BSHM", "target_time_utc": "2022-11-02T00:00:00+00:00", "status": "error", "iri2016_t_plus_1_tecu": None},
    ]
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return path


def test_iri_rows_are_filtered_to_station_window_and_ok_status(tmp_path: Path) -> None:
    rows = iri_rows_in_scope(
        _b01_rows(tmp_path), station="BSHM", start=dt.date(2022, 11, 1), end=dt.date(2022, 11, 7)
    )
    assert [r["target_time_utc"][11:13] for r in rows] == ["11", "12"]  # time-ordered
    out = export_iri_benchmark(rows, tmp_path / "root")
    assert pd.read_parquet(out)["iri2016_t_plus_1_tecu"].tolist() == [37.0, 38.18]
    assert iri_measurements(rows)["timestamp_tolerances"]["iri"]["max"] == 0.0


def test_iri_rows_refuse_an_empty_scope_rather_than_emit_an_empty_table(tmp_path: Path) -> None:
    with pytest.raises(IntegrityError, match="never emitted empty"):
        iri_rows_in_scope(
            _b01_rows(tmp_path), station="NICO", start=dt.date(2022, 11, 1), end=dt.date(2022, 11, 7)
        )


def test_gim_timestamp_offsets_are_read_from_the_generated_rows(tmp_path: Path) -> None:
    path = tmp_path / "gim.parquet"
    pd.DataFrame({"exact_epoch_match": [True, False], "f_t": [0.0, 0.25]}).to_parquet(path)
    measured = gim_measurements(path, map_interval_seconds=3600)["timestamp_tolerances"]["gim"]
    assert measured == {"min": 0.0, "max": 900.0, "units": "s"}


# --- 05: feature_table.parquet --------------------------------------------------------


def test_feature_table_is_a_byte_copy_with_denial_evidence(tmp_path: Path) -> None:
    from src.data.release import sha256_of_file

    bundle = tmp_path / "FIX-REFIT__train__untransformed"
    bundle.mkdir()
    pd.DataFrame({"interval_start_utc": ["2022-11-01T00:00:00+00:00"], "vtec_lag_1h": [1.5]}).to_parquet(
        bundle / "matrix.parquet"
    )
    (bundle / "spec.json").write_text("{}", encoding="utf-8")
    out = export_feature_table(bundle, tmp_path / "root", denial_mechanism="m", columns_checked=["vtec_lag_1h"])
    assert sha256_of_file(out) == sha256_of_file(bundle / "matrix.parquet")
    evidence = json.loads((tmp_path / "root" / "feature_table.parquet.denial_evidence.json").read_text(encoding="utf-8"))
    assert evidence["result"] == "pass" and evidence["columns_checked"] == ["vtec_lag_1h"]


def test_copy_once_refuses_a_missing_source_and_an_existing_destination(tmp_path: Path) -> None:
    with pytest.raises(IntegrityError, match="nothing is invented"):
        copy_once(tmp_path / "absent", tmp_path / "out")
    (tmp_path / "src").write_text("x")
    (tmp_path / "out").write_text("y")
    with pytest.raises(IntegrityError, match="written exactly once"):
        copy_once(tmp_path / "src", tmp_path / "out")


# --- 06: predictions.parquet, checkpoint_manifest.json -------------------------------


def _payload(path: Path, model_id: str, seed, values) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "model_id": model_id, "seed": seed, "partition_id": "FIX-F1", "transform_id": "T",
                "phase_id": "P1A", "source_id": "S", "target_definition_id": "D",
                "horizon_hours": 1, "confirmatory": seed is None and model_id == "M-06",
                "rows": [
                    {"station": "BSHM", "interval_start_utc": f"2022-11-04T0{i}:00:00+00:00", "y_hat": v}
                    for i, v in enumerate(values)
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def test_predictions_are_aggregated_verbatim_with_identity(tmp_path: Path) -> None:
    a = _payload(tmp_path / "p" / "M-06_seed7.json", "M-06", 7, [1.25, 2.5])
    b = _payload(tmp_path / "p" / "M-01.json", "M-01", None, [None, 3.0])
    frame = pd.read_parquet(export_predictions([a, b], tmp_path / "root"))
    assert len(frame) == 4
    assert {"model_id", "seed", "partition_id", "station", "interval_start_utc", "y_hat"} <= set(frame.columns)
    m06 = frame[frame["model_id"] == "M-06"]["y_hat"].tolist()
    assert m06 == [1.25, 2.5] and frame[frame["model_id"] == "M-06"]["seed"].tolist() == [7, 7]
    assert frame[frame["model_id"] == "M-01"]["seed"].isna().all()


def test_checkpoint_manifest_records_facts_and_no_invented_file_hash(tmp_path: Path) -> None:
    entries = [
        {"partition_id": "FIX-F2", "model_id": "M-06", "seed": 7, "restored_epoch": 3, "checkpoint_payload_ref": "epoch-3-2"},
        {"partition_id": "FIX-F1", "model_id": "M-06", "seed": 7, "restored_epoch": 2, "checkpoint_payload_ref": "epoch-2-1"},
    ]
    doc = json.loads(export_checkpoint_manifest(entries, tmp_path, fixture_id="plumbing_7day").read_text(encoding="utf-8"))
    assert [e["partition_id"] for e in doc["entries"]] == ["FIX-F1", "FIX-F2"]
    assert "in-memory only" in doc["persistence"]
    text = json.dumps(doc)
    assert "sha256" not in text  # no checkpoint file exists, so no file hash is recorded


# --- 07: mask_manifest.json, metrics.json, bootstrap_summary.json --------------------


def test_mask_manifest_keeps_membership_drops_timestamps_and_records_skips(tmp_path: Path) -> None:
    mask = tmp_path / "mask_primary.json"
    mask.write_text(json.dumps({"mask_id": "m1", "set_id": "primary", "partition_id": "F1",
                                "member_ids": ["M-06", "B-01"], "registered_at_utc": "2026-09-29T00:00:00Z"}))
    doc = json.loads(export_mask_manifest(
        [mask], [{"partition_id": "F1", "set_id": "gim", "status": "skipped"}], tmp_path / "r", fixture_id="plumbing_7day"
    ).read_text(encoding="utf-8"))
    assert doc["masks"][0]["mask_id"] == "m1" and "registered_at_utc" not in doc["masks"][0]
    assert doc["skipped_comparison_sets"] == [{"partition_id": "F1", "set_id": "gim", "status": "skipped"}]


def test_metrics_carry_evaluated_and_not_evaluated_sets(tmp_path: Path) -> None:
    metrics = tmp_path / "F1" / "metrics_primary.json"
    metrics.parent.mkdir()
    metrics.write_text(json.dumps({"set_id": "primary", "comparisons": [{"partition_id": "F1", "scalar": -1.5}]}))
    doc = json.loads(export_metrics([metrics], [{"partition_id": "F1", "set_id": "gim"}], tmp_path / "r", fixture_id="x").read_text(encoding="utf-8"))
    assert doc["evaluated"]["F1"]["primary"]["comparisons"][0]["scalar"] == -1.5
    assert doc["not_evaluated"] == [{"partition_id": "F1", "set_id": "gim"}]


def test_bootstrap_summary_records_non_execution_deterministically(tmp_path: Path) -> None:
    pairs = [
        {"partition_id": "F2", "set_id": "primary", "model_id": "M-06", "benchmark_id": "B-01"},
        {"partition_id": "F1", "set_id": "primary", "model_id": "M-06", "benchmark_id": "M-01"},
    ]
    first = export_bootstrap_not_executed(pairs, tmp_path / "a", fixture_id="plumbing_7day")
    second = export_bootstrap_not_executed(list(reversed(pairs)), tmp_path / "b", fixture_id="plumbing_7day")
    assert first.read_bytes() == second.read_bytes()  # exact class: same run => same bytes
    doc = json.loads(first.read_text(encoding="utf-8"))
    assert doc["status"] == "not_executed" and "TE §15.3" in doc["reason"]
    forbidden = {"replicates", "ci_lower", "ci_upper", "interval", "point_estimate", "fp_tolerance", "statistic"}
    assert not forbidden & set(doc)
    assert [p["partition_id"] for p in doc["skipped_pairs"]] == ["F1", "F2"]


def test_bootstrap_summary_refuses_without_recorded_skips(tmp_path: Path) -> None:
    with pytest.raises(IntegrityError, match="skip record"):
        export_bootstrap_not_executed([], tmp_path, fixture_id="plumbing_7day")


# --- cross-run variation: measured, never declared -----------------------------------


def test_cross_run_variation_measures_the_largest_elementwise_difference() -> None:
    measured = cross_run_variation({"r1": {"a": 1.0, "b": math.nan}, "r2": {"a": 1.5, "b": math.nan}})
    assert measured == {"value": 0.5, "elements_compared": 2, "measuring_run_ids": ["r1", "r2"]}


def test_cross_run_variation_of_identical_runs_is_zero() -> None:
    assert cross_run_variation({"r1": {"a": 2.0}, "r2": {"a": 2.0}})["value"] == 0.0


@pytest.mark.parametrize(
    "fingerprints",
    [{"r1": {"a": 1.0}}, {"r1": {"a": 1.0}, "r2": {"b": 1.0}}, {"r1": {"a": math.nan}, "r2": {"a": 1.0}}],
)
def test_cross_run_variation_refuses_what_is_not_a_measurement(fingerprints) -> None:
    with pytest.raises(IntegrityError):
        cross_run_variation(fingerprints)


def test_numeric_fingerprint_reads_predictions_and_metrics(tmp_path: Path) -> None:
    preds = export_predictions([_payload(tmp_path / "p" / "M-01.json", "M-01", None, [1.0, None])], tmp_path / "r")
    fp = numeric_fingerprint(preds)
    assert len(fp) == 2 and sorted(v for v in fp.values() if not math.isnan(v)) == [1.0]
    metrics = tmp_path / "m.json"
    metrics.write_text(json.dumps({"x": {"scalar": -2.0, "beats_model": True, "label": "s"}}))
    assert numeric_fingerprint(metrics) == {"/x/scalar": -2.0}


def test_measuring_result_keeps_fingerprints_and_composer_stamps_only_toleranced(tmp_path: Path) -> None:
    from src.data.fixture_manifest import (
        compose_candidate_manifest,
        load_measuring_results,
        write_measuring_result,
    )

    write_measuring_result(tmp_path, run_id="r1", measurements={}, fingerprints={"predictions.parquet": {"k": 1.0}})
    assert load_measuring_results(tmp_path)[0]["fingerprints"] == {"predictions.parquet": {"k": 1.0}}
    ledger = {
        "predictions.parquet": {"comparison_class": "toleranced", "units": "TECU", "producing_path": {"script": "s"}},
        "split_manifest.json": {"comparison_class": "exact", "exact_kind": "partition_membership", "units": "n/a", "producing_path": {"script": "s"}},
    }
    measured = {"value": 0.25, "elements_compared": 3, "measuring_run_ids": ["r1", "r2"]}
    data = compose_candidate_manifest(
        {"identity": {}}, fixture_id="plumbing_7day", measurements={}, measuring_run_id="r1+r2",
        outputs=list(ledger), comparison_ledger=ledger, artifact_manifest_ref="x",
        tolerances={"predictions.parquet": measured, "split_manifest.json": measured},
    )
    out = data["required_outputs"]["comparison_ledger"]
    assert out["predictions.parquet"]["fp_tolerance"] == {
        "value": 0.25, "units": "TECU", "measuring_run_id": "r1+r2", "measured_over_runs": 2,
        "elements_compared": 3, "method": "max |element-wise difference| across the recorded measuring runs",
    }
    assert "fp_tolerance" not in out["split_manifest.json"]  # exact entries never get one
    assert "fp_tolerance" not in ledger["predictions.parquet"]  # the template is not mutated


def _toleranced(value: float, runs: int | None = 2) -> dict:
    tolerance = {"value": value, "units": "TECU", "measuring_run_id": "r1+r2"}
    if runs is not None:
        tolerance["measured_over_runs"] = runs
    return {
        "comparison_class": "toleranced", "units": "TECU",
        "producing_path": {"script": "s", "inverse_route": "identity (D-27: primary target untransformed)"},
        "fp_tolerance": tolerance,
    }


@pytest.mark.parametrize("value", [0.0, 0.25])
def test_candidate_admits_a_measured_zero_or_positive_tolerance_over_two_runs(value: float) -> None:
    from src.data.fixture_manifest import _validate_ledger_entry

    _validate_ledger_entry("ledger[p]", _toleranced(value), status="candidate")


@pytest.mark.parametrize(
    ("value", "runs", "match"),
    [(-0.1, 2, "negative"), (float("nan"), 2, "not a number"), (0.0, 1, "measured_over_runs"),
     (0.0, None, "measured_over_runs")],
)
def test_candidate_refuses_negative_nan_or_single_run_tolerance(value, runs, match) -> None:
    from src.data.fixture_manifest import _validate_ledger_entry

    with pytest.raises(IntegrityError, match=match):
        _validate_ledger_entry("ledger[p]", _toleranced(value, runs), status="candidate")


def test_frozen_still_refuses_a_zero_tolerance_and_admits_a_positive_one() -> None:
    """NEGATIVE CONTROL: the frozen rule (and the default, for any caller that passes no
    status) keeps value > 0 — the acceptance tolerance is the Q-31 freeze act (TE 18.2)."""
    from src.data.fixture_manifest import _validate_ledger_entry

    for kwargs in ({"status": "frozen"}, {}):
        with pytest.raises(IntegrityError, match="not a positive number"):
            _validate_ledger_entry("ledger[p]", _toleranced(0.0), **kwargs)
    _validate_ledger_entry("ledger[p]", _toleranced(0.25), status="frozen")


# --- plots: real data, never a placeholder -------------------------------------------


def test_series_figure_draws_real_points_into_a_png(tmp_path: Path) -> None:
    pytest.importorskip("matplotlib")
    from src.evaluation.plots import render_series_figure

    out = tmp_path / "residuals.png"
    drawn = render_series_figure(
        plot_id="residuals", title="t", units_label="TECU", caveat_labels=["smoke only"],
        series=[{"label": "M-06", "x": ["a", "b", "c"], "y": [0.5, None, -0.25]}], out_path=out,
    )
    assert drawn == 2  # None skipped, never filled
    assert out.read_bytes()[:8] == PNG_MAGIC and out.stat().st_size > 1000


@pytest.mark.parametrize(
    "series",
    [[], [{"label": "x", "x": [], "y": []}], [{"label": "x", "x": ["a"], "y": [math.nan]}], [{"label": "x", "x": ["a"], "y": []}]],
)
def test_series_figure_refuses_an_empty_placeholder(tmp_path: Path, series) -> None:
    from src.evaluation.plots import render_series_figure

    with pytest.raises(RegimeError):
        render_series_figure(
            plot_id="p", title="t", units_label="u", caveat_labels=[], series=series, out_path=tmp_path / "p.png"
        )
    assert not (tmp_path / "p.png").exists()


# --- the plumbing ledger template and the bootstrap_summary amendment ----------------


_DECLARATION = Path(__file__).parent / "fixtures" / "plumbing_7day" / "identity_declaration.yaml"


def _declared_ledger() -> dict:
    from src.data.fixture_manifest import load_identity_declaration

    return dict(load_identity_declaration(_DECLARATION).data["required_outputs"]["comparison_ledger"])


def test_the_declared_ledger_classifies_all_nineteen_outputs_and_each_entry_validates() -> None:
    from src.data.fixture_manifest import (
        PLUMBING_FIXTURE_ID,
        _validate_ledger_entry,
        output_matches,
        required_outputs_for,
    )

    ledger = _declared_ledger()
    required = required_outputs_for(PLUMBING_FIXTURE_ID)
    assert sorted(ledger) == sorted(required) and len(ledger) == 19
    for name, entry in ledger.items():
        assert any(output_matches(name, r) for r in required)
        assert "fp_tolerance" not in entry  # tolerances are measured, never declared
        # D-74 amendment 2: an exact output's toleranced FIELDS are declared, never their
        # tolerance; the template validates as the candidate it is before any measurement.
        assert "fp_tolerance" not in (entry.get("field_exceptions") or {})
        if entry["comparison_class"] != "toleranced":
            _validate_ledger_entry(f"ledger[{name}]", entry, status="candidate")


def test_fixture1_bootstrap_summary_is_an_exact_schema_status_artifact() -> None:
    """D-74 amendment (CR-2026-09-29-Q31-CLOSURE): on Fixture 1 the file is a
    `not_executed` status record (TE 15.3), classed exact/schema, carrying no tolerance."""
    from src.data.fixture_manifest import _validate_ledger_entry

    entry = _declared_ledger()["bootstrap_summary.json"]
    assert entry["comparison_class"] == "exact" and entry["exact_kind"] == "schema"
    _validate_ledger_entry("ledger[bootstrap_summary.json]", entry)
    with pytest.raises(IntegrityError, match="no fp_tolerance"):
        _validate_ledger_entry(
            "ledger[bootstrap_summary.json]",
            {**entry, "fp_tolerance": {"value": 0.1, "units": entry["units"], "measuring_run_id": "r"}},
        )


def test_only_predictions_and_metrics_remain_toleranced_with_an_inverse_route() -> None:
    ledger = _declared_ledger()
    toleranced = sorted(n for n, e in ledger.items() if e["comparison_class"] == "toleranced")
    assert toleranced == ["metrics.json", "predictions.parquet"]
    for name in toleranced:
        assert ledger[name]["producing_path"]["inverse_route"].startswith("identity")


def test_a_toleranced_entry_without_a_measured_tolerance_is_still_refused() -> None:
    """A genuinely toleranced output still needs its measured fp_tolerance."""
    from src.data.fixture_manifest import _validate_ledger_entry

    with pytest.raises(IntegrityError, match="fp_tolerance"):
        _validate_ledger_entry("ledger[predictions.parquet]", _declared_ledger()["predictions.parquet"])


def test_fixture2_bootstrap_block_is_still_refused_on_the_plumbing_declaration(tmp_path: Path) -> None:
    """Fixture 2's bootstrap governance is untouched: a fixture_bootstrap block remains
    fixture-2 only and is refused on plumbing_7day."""
    from src.data.fixture_manifest import load_identity_declaration

    data = json.loads(_DECLARATION.read_text(encoding="utf-8"))
    data["fixture_bootstrap"] = {"block_length_hours": 24}
    path = tmp_path / "identity_declaration.yaml"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(IntegrityError, match="fixture_bootstrap|bootstrap"):
        load_identity_declaration(path)


# --- the measuring run's record of the non-measured quantities -----------------------


def test_sentinel_detection_and_config_id_are_deterministic() -> None:
    from src.data.fixture_outputs import _is_sentinel, config_id

    assert _is_sentinel({"value": "TBD — freeze gate"})
    assert _is_sentinel([{"a": "TBD — freeze gate"}])
    assert not _is_sentinel({"value": "TECU", "source": "glossary"})
    hashes = {"seeds.yaml": "b" * 64, "data.yaml": "a" * 64}
    assert config_id(hashes) == config_id(dict(reversed(list(hashes.items()))))
    assert config_id(hashes) != config_id({**hashes, "data.yaml": "c" * 64})


def test_the_composer_carries_the_record_but_never_overrides_a_declared_value() -> None:
    from src.data.fixture_manifest import compose_candidate_manifest

    data = compose_candidate_manifest(
        {"identity": {}, "inputs": {"prepared_vtec": {"x": 1}}},
        fixture_id="plumbing_7day",
        measurements={},
        measuring_run_id="r1+r2",
        outputs=[],
        comparison_ledger={},
        artifact_manifest_ref="ref",
        recorded={"inputs": {"prepared_vtec": {"x": 2}, "site_log": {"sha256": "a" * 64}}},
    )
    assert data["inputs"]["prepared_vtec"] == {"x": 1}
    assert data["inputs"]["site_log"] == {"sha256": "a" * 64}


def test_stage_measurements_ignore_archived_previous_runs(tmp_path: Path) -> None:
    """2026-10-01 defect: an archived earlier run's block was folded into the current run's
    envelope, widening it with values this run never measured."""
    from src.data.fixture_manifest import collect_stage_measurements

    write_stage_measurements(
        tmp_path, stage="02_x", measurements={"row_count_ranges": {"hourly_target": {"min": 1, "max": 2, "units": "rows"}}}
    )
    old = tmp_path / f"{STAGE_MEASUREMENTS_DIR}.archived-run0" / "02_x"
    old.mkdir(parents=True)
    (old / "fixture_measurements.json").write_text(json.dumps(
        {"stage": "02_x", "measurements": {"row_count_ranges": {"hourly_target": {"min": 1, "max": 99, "units": "rows"}}}}
    ), encoding="utf-8")
    nested = tmp_path / "archived_releases" / "x" / STAGE_MEASUREMENTS_DIR / "02_x"
    nested.mkdir(parents=True)
    (nested / "fixture_measurements.json").write_text("not json", encoding="utf-8")
    merged = collect_stage_measurements(tmp_path)
    assert merged["row_count_ranges"]["hourly_target"]["max"] == 2.0


def _bootstrap_record(tmp_path: Path, name: str, pid: str, value: float) -> Path:
    record = {
        "artifact_class": "bootstrap_result", "partition_id": pid, "set_id": "primary",
        "model_id": "M-06", "benchmark_id": "B-01", "point_estimate": value,
        "ci_lower": value - 1.0, "ci_upper": value + 1.0, "ci_level": 0.95,
        "replicates": 1000, "block_hours": 24,
        "per_station_components": {"ARUC": value, "BSHM": value, "NICO": value},
        "pairwise_correlations": {"ARUC|BSHM": 0.5}, "replicate_hash": "h", "seed_key": "k",
    }
    path = tmp_path / name
    path.write_text(json.dumps(record), encoding="utf-8")
    return path


def test_bootstrap_executed_summary_aggregates_pairs_and_is_deterministic(tmp_path: Path) -> None:
    from src.data.fixture_outputs import export_bootstrap_executed, numeric_fingerprint

    a = _bootstrap_record(tmp_path, "b1.json", "FIX-MAR-FOLD-01", 2.0)
    b = _bootstrap_record(tmp_path, "b2.json", "FIX-MAR-FOLD-02", 3.0)
    out1 = tmp_path / "r1"
    out2 = tmp_path / "r2"
    out1.mkdir()
    out2.mkdir()
    p1 = export_bootstrap_executed([a, b], out1, fixture_id="scientific_1month")
    p2 = export_bootstrap_executed([b, a], out2, fixture_id="scientific_1month")
    assert p1.read_bytes() == p2.read_bytes()
    fp = numeric_fingerprint(p1)
    assert fp["/pairs/FIX-MAR-FOLD-01/primary/M-06/B-01/point_estimate"] == 2.0
    assert all(not k.startswith("/units") for k in fp)


def test_bootstrap_executed_summary_refuses_empty_and_duplicates(tmp_path: Path) -> None:
    from src.data.fixture_outputs import export_bootstrap_executed

    with pytest.raises(IntegrityError, match="never ran"):
        export_bootstrap_executed([], tmp_path, fixture_id="scientific_1month")
    a = _bootstrap_record(tmp_path, "b1.json", "F", 2.0)
    a2 = _bootstrap_record(tmp_path, "b2.json", "F", 2.0)
    with pytest.raises(IntegrityError, match="second bootstrap result"):
        export_bootstrap_executed([a, a2], tmp_path, fixture_id="scientific_1month")


def test_fixture_bootstrap_replicates_read_from_real_scopes() -> None:
    """Regression (2026-10-01, P-5): 07 called the `fixture_bootstrap` PROPERTY as a method
    and both fixture runs aborted in 07. Read through the real loader for both fixtures."""
    import importlib.util

    from src.data.fixture_manifest import load_fixture_scope

    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("s07_fb", root / "scripts" / "07_evaluate_and_report.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sci = load_fixture_scope(root / "tests" / "fixtures" / "scientific_1month" / "identity_declaration.yaml")
    plu = load_fixture_scope(root / "tests" / "fixtures" / "plumbing_7day" / "identity_declaration.yaml")
    assert mod._fixture_bootstrap_replicates(sci) == 1000
    assert mod._fixture_bootstrap_replicates(plu) is None
