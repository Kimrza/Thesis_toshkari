"""D-17 target-row schema contract, and every hard rule's negative control (P1-03).

PURPOSE. The tree-named schema test (`CR-2026-08-22-TARGET-SCHEMA-TEST`; BLK-05's
implementation limb) for unit `target-standardization`. BLK-05's approved acceptance
behaviour, fixed by the owner "so implementation cannot narrow it": a valid row
containing exactly D-17's 16 fields PASSES; a row containing an excluded or additional
field FAILS; a row missing any required field FAILS. This module also carries the
negative control paired with every hard rule of the unit (team.md's affirmed
methodology — a test that proves the violation is CAUGHT, not only that the happy path
works):

* the Q2 = A refuse-to-RUN gate while `qc_operations` is `TBD — freeze gate` or absent,
  naming the field and the frozen-under-a-D-number expectation (never non-emptiness);
* a fifth transformation FAILS; an aggregation statistic that does not resolve to D-16
  FAILS; a QC operation outside the frozen list fails like a fifth transformation;
* a missing D-17 field fails (16 exactly — not 15, not 17); a missing ID stamp fails;
  the caveat column absent fails; the round-trip preserves the column through this
  unit's own write path; a substituted excluded set fails and is never adopted;
* a D-19 threshold without its measured basis is refused; a December-informed basis is
  refused; the receiver-specific label is refused; the fixture-manifest tolerance
  unset STOPS naming the TE 15.2 field (never a numpy.isclose default).

INPUTS. None outside this repository: synthetic provider rows and synthetic config
mappings built in-test. The config doubles carry MECHANISM-EXERCISING synthetic values
(threshold value 2, window bound 5.0, fake decision numbers), never D-19's frozen
values — those live in the governed config transcription owned elsewhere, and no
scientific constant is inlined here (TC-03e). Station names are synthetic (STA1/STA2).
Writes go to pytest `tmp_path` only: NO standardized target artifact is produced —
`configs/data.yaml`'s `qc_operations` remains `TBD — freeze gate` and the governed
refusal is itself under test. Anything run here is smoke evidence only, never governed
evidence (the governed pin is Python 3.11 exactly).

RE-RUN BEHAVIOUR. Pure functions of the synthetic inputs plus tmp_path writes; no
network, no registry rows, no fixture directories touched. Deterministic.

Run: pytest tests/test_prepared_target_schema.py -rs
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import src.data.config as config_module  # noqa: E402
from src.data.config import TBD_SENTINEL, IntegrityError, StandardizationError  # noqa: E402
from src.data.prepared import (  # noqa: E402
    D17_FIELDS,
    DECLARED_EXCLUDED_SET,
    LINEAGE_CAVEAT_FIELD,
    LINEAGE_CAVEAT_TEXT,
    PERMITTED_TRANSFORMATIONS,
    TARGET_LABEL,
    TOLERANCE_MANIFEST_KEY,
    TOLERANCE_MANIFEST_SUBKEY,
    assert_budget_complete,
    assert_closed_transformation_set,
    assert_d17_config_matches,
    assert_label_permitted,
    assert_no_prohibited_phrasing,
    assert_qc_operation_permitted,
    assert_qc_operations_frozen,
    assert_row_conforms,
    build_uncertainty_budget,
    read_target_rows_csv,
    resolve_aggregation_statistic,
    resolve_float_tolerance,
    resolve_support_thresholds,
    standardize_hourly_target,
    verify_value_level,
    write_json_artifact,
    write_target_rows_csv,
)

SCRIPTS_DIR = REPO_ROOT / "scripts"


# --------------------------------------------------------------------------------------
# Synthetic doubles. Mechanism-exercising values ONLY — never D-19's frozen values.
# --------------------------------------------------------------------------------------


def _threshold_entry(statistic: str, value: float) -> dict[str, object]:
    return {
        "statistic": statistic,
        "value": value,
        "basis": "synthetic mechanism-exercising basis (test double)",
        "basis_window": "January-November 2022",
        "decision": "D-19",
    }


def _frozen_config() -> dict[str, object]:
    """A config double with every gate satisfied — the mechanism's happy path."""
    return {
        "qc_operations": {
            "operations": ["provider_validity_screen"],
            "decision": "D-90",  # synthetic decision number: a test double, not a freeze
        },
        "target": {
            "aggregation": {"statistic": "median", "decision": "D-16"},
            "identity": {
                "phase_id": "phase-1",
                "source_id": "test-source",
                "target_definition_id": "test-tdef-p1-gridded",
            },
            "contract": {
                "fields": list(D17_FIELDS),
                "excluded": list(DECLARED_EXCLUDED_SET),
                "decision": "D-17",
            },
            "support_thresholds": {
                "valid_observation_count": _threshold_entry("minimum", 2),
                "within_hour_spread_tecu": _threshold_entry("range", 5.0),
                "largest_internal_gap_s": _threshold_entry("maximum", 900),
                "provider_dtec_summary": _threshold_entry("median", 0.5),
            },
        },
    }


def _provider_rows() -> list[dict[str, object]]:
    """Two stations, one UTC hour each, integer bin labels — the five-column shape."""
    base = 1667260800  # 2022-11-01T00:00:00Z, inside the November fixture window
    return [
        {
            "station": "STA1",
            "ut1_unix": base + 0,
            "gdlat": 40.0,
            "glon": 44.0,
            "tec": 10.0,
            "dtec": 0.2,
        },
        {
            "station": "STA1",
            "ut1_unix": base + 300,
            "gdlat": 40.0,
            "glon": 44.0,
            "tec": 12.0,
            "dtec": 0.3,
        },
        {
            "station": "STA1",
            "ut1_unix": base + 600,
            "gdlat": 40.0,
            "glon": 44.0,
            "tec": 11.0,
            "dtec": 0.1,
        },
        {
            "station": "STA2",
            "ut1_unix": base + 0,
            "gdlat": 32.0,
            "glon": 35.0,
            "tec": 8.0,
            "dtec": 0.2,
        },
        {
            "station": "STA2",
            "ut1_unix": base + 300,
            "gdlat": 32.0,
            "glon": 35.0,
            "tec": 9.0,
            "dtec": 0.2,
        },
        {
            "station": "STA2",
            "ut1_unix": base + 600,
            "gdlat": 32.0,
            "glon": 35.0,
            "tec": 7.0,
            "dtec": 0.2,
        },
    ]


def _standardize(config: dict[str, object] | None = None, **kwargs: object):
    return standardize_hourly_target(
        _provider_rows(),
        data_config=config if config is not None else _frozen_config(),
        aggregation_config_id="testcfg000001",
        **kwargs,  # type: ignore[arg-type]
    )


# --------------------------------------------------------------------------------------
# Contract shapes: 16 exactly — not 15, not 17
# --------------------------------------------------------------------------------------


def test_d17_field_set_is_exactly_sixteen() -> None:
    """D-17's count is 16, counted from the enumeration; no duplicate; no QC-flag field."""
    assert len(D17_FIELDS) == 16
    assert len(set(D17_FIELDS)) == 16
    # processor_qc_flags is NOT a D-17 row field: aggregation flags live in the
    # data-quality block (W-3), and D-17's enumeration carries sixteen fields exactly.
    assert "processor_qc_flags" not in D17_FIELDS


def test_permitted_transformations_are_exactly_four() -> None:
    assert len(PERMITTED_TRANSFORMATIONS) == 4
    assert len(set(PERMITTED_TRANSFORMATIONS)) == 4


def test_declared_excluded_set_is_d17s_eight_classes() -> None:
    assert len(DECLARED_EXCLUDED_SET) == 8
    assert "valid_satellite_count" in DECLARED_EXCLUDED_SET


def test_standardization_error_is_declared_in_config_module() -> None:
    """Q1 = A: declared in src/data/config.py, an IntegrityError subclass, in __all__."""
    assert issubclass(StandardizationError, IntegrityError)
    assert "StandardizationError" in config_module.__all__
    with pytest.raises(StandardizationError) as excinfo:
        raise StandardizationError("resource", "expectation")
    assert "resource" in str(excinfo.value)


# --------------------------------------------------------------------------------------
# The Q2 = A refuse-to-RUN gate
# --------------------------------------------------------------------------------------


def test_qc_tbd_refusal_names_field_and_frozen_under_d_number_expectation() -> None:
    """The raise names configs/data.yaml qc_operations and the D-number expectation."""
    with pytest.raises(StandardizationError) as excinfo:
        assert_qc_operations_frozen({"qc_operations": TBD_SENTINEL})
    message = str(excinfo.value)
    assert "qc_operations" in message
    assert "D-NUMBER" in message.upper()
    assert "non-empt" in message.lower()  # never mere non-emptiness


def test_qc_absent_refuses_identically() -> None:
    with pytest.raises(StandardizationError) as excinfo:
        assert_qc_operations_frozen({})
    assert "qc_operations" in str(excinfo.value)


def test_qc_non_empty_list_without_d_number_still_refuses() -> None:
    """A list filled by convenience satisfies 'non-empty' and is what TE 18.2 forbids."""
    with pytest.raises(StandardizationError):
        assert_qc_operations_frozen(
            {"qc_operations": {"operations": ["anything"], "decision": ""}}
        )


def test_standardize_refuses_to_run_while_qc_is_tbd_and_produces_nothing() -> None:
    """Q2 = A: the target-producing run refuses FIRST; no rows exist afterwards."""
    config = _frozen_config()
    config["qc_operations"] = TBD_SENTINEL
    with pytest.raises(StandardizationError) as excinfo:
        _standardize(config)
    assert "qc_operations" in str(excinfo.value)


# --------------------------------------------------------------------------------------
# The closed four-transformation set (R-64) and the D-16 statistic (R-65)
# --------------------------------------------------------------------------------------


def test_fifth_transformation_fails() -> None:
    with pytest.raises(StandardizationError) as excinfo:
        assert_closed_transformation_set([*PERMITTED_TRANSFORMATIONS, "rescale"])
    assert "fifth transformation" in str(excinfo.value)


def test_missing_permitted_transformation_fails() -> None:
    with pytest.raises(StandardizationError):
        assert_closed_transformation_set(PERMITTED_TRANSFORMATIONS[:3])


def test_fifth_transformation_fails_through_the_engine_too() -> None:
    with pytest.raises(StandardizationError):
        _standardize(applied_transformations=[*PERMITTED_TRANSFORMATIONS, "unit_conversion"])


def test_qc_operation_outside_frozen_list_fails_like_a_fifth_transformation() -> None:
    frozen = {"operations": ["provider_validity_screen"], "decision": "D-90"}
    with pytest.raises(StandardizationError) as excinfo:
        assert_qc_operation_permitted("despike", frozen)
    assert "fifth transformation" in str(excinfo.value)


def test_statistic_absent_is_refused_never_defaulted() -> None:
    config = _frozen_config()
    del config["target"]["aggregation"]  # type: ignore[union-attr]
    with pytest.raises(StandardizationError) as excinfo:
        resolve_aggregation_statistic(config)
    assert "default" in str(excinfo.value)


def test_statistic_without_d16_citation_is_refused() -> None:
    config = _frozen_config()
    config["target"]["aggregation"] = {"statistic": "median", "decision": ""}  # type: ignore[index]
    with pytest.raises(StandardizationError):
        resolve_aggregation_statistic(config)


@pytest.mark.parametrize("statistic", ["mean", "zenith_weighted_mean"])
def test_non_d16_statistic_fails(statistic: str) -> None:
    config = _frozen_config()
    config["target"]["aggregation"] = {"statistic": statistic, "decision": "D-16"}  # type: ignore[index]
    with pytest.raises(StandardizationError) as excinfo:
        resolve_aggregation_statistic(config)
    assert "D-16" in str(excinfo.value)


# --------------------------------------------------------------------------------------
# D-19 thresholds: basis carried, December never informing (R-68)
# --------------------------------------------------------------------------------------


def test_threshold_without_basis_is_refused() -> None:
    config = _frozen_config()
    entry = config["target"]["support_thresholds"]["valid_observation_count"]  # type: ignore[index]
    entry["basis"] = ""
    with pytest.raises(StandardizationError) as excinfo:
        resolve_support_thresholds(config)
    assert "basis" in str(excinfo.value)


def test_december_informed_basis_is_refused() -> None:
    config = _frozen_config()
    entry = config["target"]["support_thresholds"]["within_hour_spread_tecu"]  # type: ignore[index]
    entry["basis"] = "measured including December 2022 tails"
    with pytest.raises(StandardizationError) as excinfo:
        resolve_support_thresholds(config)
    assert "December" in str(excinfo.value)


def test_threshold_statistic_drift_from_d19_is_refused() -> None:
    config = _frozen_config()
    entry = config["target"]["support_thresholds"]["within_hour_spread_tecu"]  # type: ignore[index]
    entry["statistic"] = "stddev"
    with pytest.raises(StandardizationError):
        resolve_support_thresholds(config)


def test_missing_threshold_row_is_refused() -> None:
    config = _frozen_config()
    del config["target"]["support_thresholds"]["largest_internal_gap_s"]  # type: ignore[union-attr]
    with pytest.raises(StandardizationError):
        resolve_support_thresholds(config)


# --------------------------------------------------------------------------------------
# The D-17 contract: config drift vs row defect fail differently (R-66, R-67)
# --------------------------------------------------------------------------------------


def test_config_field_set_of_fifteen_fails_before_any_row() -> None:
    config = _frozen_config()
    config["target"]["contract"]["fields"] = list(D17_FIELDS[:-1])  # type: ignore[index]
    with pytest.raises(StandardizationError) as excinfo:
        assert_d17_config_matches(config)
    assert "CONFIG drifted" in str(excinfo.value)


def test_config_field_set_of_seventeen_fails() -> None:
    config = _frozen_config()
    config["target"]["contract"]["fields"] = [*D17_FIELDS, "extra_field"]  # type: ignore[index]
    with pytest.raises(StandardizationError):
        assert_d17_config_matches(config)


def test_substituted_excluded_set_fails_and_is_never_adopted() -> None:
    """A run that finds a different excluded set FAILS; it does not adopt it (R-67)."""
    config = _frozen_config()
    substituted = list(DECLARED_EXCLUDED_SET[:-1]) + ["a different class"]
    config["target"]["contract"]["excluded"] = substituted  # type: ignore[index]
    with pytest.raises(StandardizationError) as excinfo:
        assert_d17_config_matches(config)
    assert "never substituted" in str(excinfo.value)


def _valid_row() -> dict[str, object]:
    result = _standardize()
    return dict(result.rows[0])


def test_valid_sixteen_field_row_passes() -> None:
    """BLK-05's approved acceptance behaviour, limb 1: a valid row PASSES."""
    assert_row_conforms(_valid_row())


def test_row_missing_a_required_field_fails() -> None:
    row = _valid_row()
    del row["vtec_tecu"]
    with pytest.raises(StandardizationError) as excinfo:
        assert_row_conforms(row)
    assert "ROW is wrong" in str(excinfo.value)


def test_row_with_an_additional_field_fails() -> None:
    row = _valid_row()
    row["surprise_field"] = 1
    with pytest.raises(StandardizationError):
        assert_row_conforms(row)


@pytest.mark.parametrize("field", ["n_sat_valid", "zen_wt", "elev_deg", "dcb_bias"])
def test_row_with_an_excluded_class_field_fails(field: str) -> None:
    """Token matching: a renamed excluded-class column cannot walk past the check."""
    row = _valid_row()
    row[field] = 1
    with pytest.raises(StandardizationError):
        assert_row_conforms(row)


@pytest.mark.parametrize("field", ["phase_id", "source_id", "target_definition_id"])
def test_row_with_a_missing_id_stamp_fails(field: str) -> None:
    row = _valid_row()
    row[field] = ""
    with pytest.raises(StandardizationError) as excinfo:
        assert_row_conforms(row)
    assert field in str(excinfo.value)


def test_row_without_the_caveat_column_fails() -> None:
    """R-69: a target artifact written without the lineage statement FAILS."""
    row = _valid_row()
    del row[LINEAGE_CAVEAT_FIELD]
    with pytest.raises(StandardizationError) as excinfo:
        assert_row_conforms(row)
    assert "lineage" in str(excinfo.value).lower()


def test_row_with_an_altered_caveat_fails() -> None:
    row = _valid_row()
    row[LINEAGE_CAVEAT_FIELD] = "a truncated caveat"
    with pytest.raises(StandardizationError):
        assert_row_conforms(row)


# --------------------------------------------------------------------------------------
# Labelling (FR-P1-03-4): the prohibited phrasing is refused
# --------------------------------------------------------------------------------------


def test_receiver_specific_label_is_refused() -> None:
    with pytest.raises(StandardizationError):
        assert_label_permitted("receiver-specific station-observed VTEC")


def test_only_the_frozen_label_passes() -> None:
    assert_label_permitted(TARGET_LABEL)
    with pytest.raises(StandardizationError):
        assert_label_permitted("gridded VTEC")


def test_grep_class_check_catches_prohibited_phrasing_but_passes_the_caveat() -> None:
    """The caveat quotes the prohibition in negation and must not trip the check."""
    assert_no_prohibited_phrasing({"caveat": LINEAGE_CAVEAT_TEXT, "note": "clean"})
    with pytest.raises(StandardizationError):
        assert_no_prohibited_phrasing({"note": "this is station-observed VTEC"})


# --------------------------------------------------------------------------------------
# The engine's happy path, negative VTEC, coverage keying, budget
# --------------------------------------------------------------------------------------


def test_standardize_happy_path_produces_conforming_median_rows() -> None:
    result = _standardize()
    assert len(result.rows) == 2  # one row per station-hour
    by_station = {row["station_id"]: row for row in result.rows}
    sta1 = by_station["STA1"]
    assert sta1["vtec_tecu"] == 11.0  # median of 10, 12, 11 (D-16)
    assert sta1["valid_observation_count"] == 3
    assert sta1["within_hour_spread_tecu"] == 2.0  # range: max - min
    assert sta1["largest_internal_gap_s"] == 300.0
    assert sta1["cell_gdlat"] == 40
    assert sta1["cell_lat_bounds"] == "[40, 41)"
    assert sta1["interval_start_utc"] == "2022-11-01T00:00:00Z"
    assert sta1["target_valid"] is True
    for row in result.rows:
        assert row[LINEAGE_CAVEAT_FIELD] == LINEAGE_CAVEAT_TEXT
        assert_row_conforms(row)


def test_below_threshold_row_is_invalid_with_reason_recorded_not_fatal() -> None:
    """R-68: a cell-hour below a threshold sets target_valid false; the reason is kept."""
    config = _frozen_config()
    config["target"]["support_thresholds"]["valid_observation_count"] = (  # type: ignore[index]
        _threshold_entry("minimum", 5)
    )
    result = _standardize(config)
    assert all(row["target_valid"] is False for row in result.rows)
    assert result.coverage_report["invalid_reasons"]  # machine-readable, never console-only


def test_unexplained_negative_vtec_is_rejected() -> None:
    rows = _provider_rows()
    rows[0]["tec"] = -3.0
    with pytest.raises(StandardizationError) as excinfo:
        standardize_hourly_target(
            rows, data_config=_frozen_config(), aggregation_config_id="testcfg000001"
        )
    assert "negative" in str(excinfo.value).lower()


def test_explained_negative_vtec_is_accepted_and_the_explanation_recorded() -> None:
    rows = _provider_rows()
    rows[0]["tec"] = -3.0
    key = f"STA1:{rows[0]['ut1_unix']}"
    result = standardize_hourly_target(
        rows,
        data_config=_frozen_config(),
        aggregation_config_id="testcfg000001",
        negative_vtec_explanations={key: "synthetic recorded explanation (test double)"},
    )
    explained = result.data_quality["negative_vtec"]["explained"]
    assert explained and explained[0]["record"] == key


def test_coverage_report_is_keyed_by_cell_and_month() -> None:
    """R-71 content 3: the same cell and month identifiers the G-P1A record uses."""
    result = _standardize()
    report = result.coverage_report
    assert report["keys"] == ["station", "cell_gdlat", "cell_glon", "month"]
    months = {entry["month"] for entry in report["per_cell_month"]}
    assert months == {"2022-11"}


def test_budget_is_complete_and_phase2_contents_carry_reasons() -> None:
    result = _standardize()
    budget = result.uncertainty_budget
    assert_budget_complete(budget)  # the budget asserts its own completeness (R-72)
    assert budget["asymmetry_statement"]
    assert len(budget["not_applicable"]) == 4
    assert all(entry["reason"] for entry in budget["not_applicable"])


def test_budget_that_states_nothing_fails() -> None:
    """FR-P1-05-10's failure condition: a budget file that exists and states nothing."""
    with pytest.raises(StandardizationError):
        assert_budget_complete({})


def test_budget_with_an_empty_phase2_emission_fails() -> None:
    """A Phase 2 quantity emitted empty rather than recorded not-applicable fails."""
    budget = dict(build_uncertainty_budget(_standardize().rows))
    hollow = [dict(entry) for entry in budget["not_applicable"]]
    hollow[0]["reason"] = ""
    budget["not_applicable"] = hollow
    with pytest.raises(StandardizationError):
        assert_budget_complete(budget)


def test_budget_missing_an_applicable_content_fails() -> None:
    budget = dict(build_uncertainty_budget(_standardize().rows))
    applicable = dict(budget["applicable"])
    applicable["provider_reported_uncertainty"] = ""
    budget["applicable"] = applicable
    with pytest.raises(StandardizationError):
        assert_budget_complete(budget)


# --------------------------------------------------------------------------------------
# The write paths: round-trip preservation, ID stamps, label and caveat on artifacts
# --------------------------------------------------------------------------------------


def test_round_trip_preserves_the_caveat_column(tmp_path: Path) -> None:
    """SD-T-02 obligation 2: the column survives the operations THIS unit performs."""
    result = _standardize()
    path = write_target_rows_csv(tmp_path / "rows.csv", result.rows)
    back = read_target_rows_csv(path)
    assert len(back) == len(result.rows)
    for row in back:
        assert row[LINEAGE_CAVEAT_FIELD] == LINEAGE_CAVEAT_TEXT
    # header carries D-17's sixteen plus the caveat column, nothing else
    assert len(back[0]) == 17


def test_write_path_refuses_a_row_without_the_caveat(tmp_path: Path) -> None:
    result = _standardize()
    rows = [dict(result.rows[0])]
    del rows[0][LINEAGE_CAVEAT_FIELD]
    with pytest.raises(StandardizationError):
        write_target_rows_csv(tmp_path / "rows.csv", rows)
    assert not (tmp_path / "rows.csv").exists()  # refused BEFORE any byte was written


def test_json_artifact_carries_ids_label_and_caveat(tmp_path: Path) -> None:
    import json

    identity = {
        "phase_id": "phase-1",
        "source_id": "test-source",
        "target_definition_id": "test-tdef-p1-gridded",
    }
    path = write_json_artifact(
        tmp_path / "artifact.json",
        {"note": "clean"},
        identity=identity,
        artifact_class="coverage_report",
    )
    envelope = json.loads(path.read_text(encoding="utf-8"))
    assert envelope["target_label"] == TARGET_LABEL
    assert envelope[LINEAGE_CAVEAT_FIELD] == LINEAGE_CAVEAT_TEXT
    for key, value in identity.items():
        assert envelope[key] == value


def test_json_artifact_refuses_an_empty_id_stamp(tmp_path: Path) -> None:
    with pytest.raises(StandardizationError):
        write_json_artifact(
            tmp_path / "artifact.json",
            {"note": "clean"},
            identity={"phase_id": "phase-1", "source_id": "", "target_definition_id": "x"},
            artifact_class="coverage_report",
        )


def test_json_artifact_refuses_prohibited_phrasing_in_payload(tmp_path: Path) -> None:
    identity = {
        "phase_id": "phase-1",
        "source_id": "test-source",
        "target_definition_id": "test-tdef-p1-gridded",
    }
    with pytest.raises(StandardizationError):
        write_json_artifact(
            tmp_path / "artifact.json",
            {"caption": "receiver-specific station-observed VTEC at STA1"},
            identity=identity,
            artifact_class="coverage_report",
        )


# --------------------------------------------------------------------------------------
# Verification: the declared tolerance, and the value-level closed-set diff
# --------------------------------------------------------------------------------------


def test_tolerance_unset_stops_naming_the_te152_field() -> None:
    """Never a numpy.isclose default: unset -> stop, naming the fixture-manifest field."""
    with pytest.raises(StandardizationError) as excinfo:
        resolve_float_tolerance({})
    message = str(excinfo.value)
    assert TOLERANCE_MANIFEST_KEY in message
    assert "15.2" in message


def test_tolerance_tbd_sentinel_also_stops() -> None:
    manifest = {TOLERANCE_MANIFEST_KEY: {TOLERANCE_MANIFEST_SUBKEY: TBD_SENTINEL}}
    with pytest.raises(StandardizationError):
        resolve_float_tolerance(manifest)


def test_declared_tolerance_resolves() -> None:
    manifest = {TOLERANCE_MANIFEST_KEY: {TOLERANCE_MANIFEST_SUBKEY: 0.001}}
    assert resolve_float_tolerance(manifest) == 0.001


def test_value_level_verification_passes_on_a_faithful_artifact() -> None:
    result = _standardize()
    evidence = verify_value_level(
        _provider_rows(),
        result.rows,
        data_config=_frozen_config(),
        aggregation_config_id="testcfg000001",
        tolerance=0.001,
    )
    assert evidence["rows_compared"] == 2
    assert evidence["transformations_enumerated"] == list(PERMITTED_TRANSFORMATIONS)
    assert len(evidence["uncertainty_contents_not_applicable"]) == 4


def test_value_level_diff_fails_on_an_altered_value_as_a_fifth_transformation() -> None:
    """An unattributable value change is a FIFTH transformation, not a reviewer's job."""
    result = _standardize()
    altered = [dict(row) for row in result.rows]
    altered[0]["vtec_tecu"] = float(altered[0]["vtec_tecu"]) * 1.05  # a rescale
    with pytest.raises(StandardizationError) as excinfo:
        verify_value_level(
            _provider_rows(),
            altered,
            data_config=_frozen_config(),
            aggregation_config_id="testcfg000001",
            tolerance=0.001,
        )
    assert "FIFTH" in str(excinfo.value).upper()


def test_value_level_diff_fails_on_a_missing_or_extra_row() -> None:
    result = _standardize()
    with pytest.raises(StandardizationError):
        verify_value_level(
            _provider_rows(),
            result.rows[:1],
            data_config=_frozen_config(),
            aggregation_config_id="testcfg000001",
            tolerance=0.001,
        )


def test_verification_refuses_while_qc_is_tbd_like_the_producer() -> None:
    """A verification of a target that must not exist refuses identically (Q2 = A)."""
    config = _frozen_config()
    config["qc_operations"] = TBD_SENTINEL
    with pytest.raises(StandardizationError):
        verify_value_level(
            _provider_rows(),
            [],
            data_config=config,
            aggregation_config_id="testcfg000001",
            tolerance=0.001,
        )


# --------------------------------------------------------------------------------------
# Script identity: position 02/03, --phase (1,), and NO 02a/02b convention (R-73)
# --------------------------------------------------------------------------------------


def test_stage_scripts_exist_under_their_tree_names_with_no_02a_02b() -> None:
    assert (SCRIPTS_DIR / "02_standardize_prepared_target.py").is_file()
    assert (SCRIPTS_DIR / "03_verify_processing.py").is_file()
    offenders = [p.name for p in SCRIPTS_DIR.glob("02[a-z]_*.py")]
    assert not offenders, (
        f"an 02a/02b convention was invented: {offenders}; the ordinal denotes the "
        f"pipeline position and --phase selects exactly one script per run (R-73)"
    )


@pytest.mark.parametrize(
    "script", ["02_standardize_prepared_target.py", "03_verify_processing.py"]
)
def test_scripts_are_phase1_only_and_never_skip_the_boundary(script: str) -> None:
    text = (SCRIPTS_DIR / script).read_text(encoding="utf-8")
    assert "choices=(1,)" in text  # Phase 1 only; the Phase 2 `02` is a different script
    assert "assert_phase_boundary" in text  # entry-contract step 4, never skipped
    assert "assert_no_raw_fields" in text  # R-24: before the first write
    assert "ensure_process_determinism(sys.argv)" in text  # entry-contract step 1
