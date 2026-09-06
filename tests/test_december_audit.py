"""The December audit engine's negative controls: scope, routing, reconciliation, gate.

PURPOSE. Every refusal of `src/data/inventory.py` (W-1, W-5…W-8; R-44, R-49…R-53;
SD-I-04/05/08) is negative-controlled: the nine-field inventory failure naming entry AND
field; the verbatim-notice defect; the short scope refused BEFORE any read; the ordinary
path never logged; the class/residency disagreement stop-and-report naming the file; the
`locked_evaluation` refusal and the limb/purpose pairing; the interrupted audit leaving
NO report while rows stand; the per-`run_id` reconciliation with December included in
limb 3b; the caveat-less `derived_only` figure; the unattributed threshold figure; the
four separately named prohibition results; and the schema mismatches, each failing
separately.

FIXTURE DISCIPLINE (team.md § Walking Skeleton; the approved plan's hard constraint).
NO test or fixture touches the live restricted evidence root or December content: every
tree is synthetic under `tmp_path`, reached through the SUPPORTED SEAMS only —
`locked_test._repo_root` (the guard's own documented test seam) and the audit engine's
synthetic-locked-month parameters. December is what the controls MODEL; synthetic months
are what they EXECUTE. This file holds no restricted-root literal: the boundary path is
built from `locked_test.RESTRICTED_ROOT`, the imported constant.

RE-RUN BEHAVIOUR. Pure `tmp_path` fixtures; no network; no write outside `tmp_path`.

Run: pytest tests/test_december_audit.py -rs
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import pytest
from src.data import locked_test
from src.data.acquisition import CredentialEgressError
from src.data.config import (
    TBD_SENTINEL,
    AuditScopeError,
    InventoryError,
    LockedTestError,
    PreflightError,
    SchemaError,
)
from src.data.inventory import (
    AUDIT_MONTHS,
    DATA07_CAVEAT,
    DeclaredAuditScope,
    GateError,
    assert_figures_caveated,
    assert_gp1a_record,
    assert_no_silent_imputation,
    assert_performance_blind,
    assert_prohibition_results,
    assert_record_date_class_agreement,
    assert_regime_report_states_range,
    assert_scope_equals_reference,
    assert_source_entry,
    assert_unmixed_sources,
    assert_verbatim_notice,
    attribute_records_by_month,
    audit_access_record,
    build_gp1a_record,
    build_regime_report,
    coverage_figures,
    data07_caveat_for,
    expected_schema_from,
    finalize_audit_reports,
    governed_reference_scope,
    gp1a_thresholds_from,
    new_audit_run_id,
    reconcile_audit,
    route_audit_path,
    schema_digest,
    validate_schema,
    write_source_inventory,
)

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The synthetic locked month every December-modeling control executes against.
SYNTHETIC_LOCKED = (2021, 6)


def _entry(**overrides: object) -> dict:
    entry: dict = {
        "provider": "synthetic-provider",
        "role": "prepared-product",
        "provider_product_identity": "syn_product_v1.txt",
        "coverage": "synthetic-window",
        "retrieval_date": "2026-09-05",
        "checksum": "0" * 64,
        "release_status": "final",
        "licence_access_notes": "open licence; retrieval via public interface",
        "consuming_configuration": "data.yaml",
    }
    entry.update(overrides)
    return entry


def _scope(**overrides: object) -> DeclaredAuditScope:
    values: dict = {
        "months": AUDIT_MONTHS,
        "december_days": (1, 31),
        "cells": {"SYNA": (10, 20)},
        "artifact_classes": ("prepared-product",),
    }
    values.update(overrides)
    return DeclaredAuditScope(**values)


@pytest.fixture()
def synthetic_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Repoint the boundary derivation at a synthetic root — the guard's own seam."""
    monkeypatch.setattr(locked_test, "_repo_root", lambda: tmp_path)
    (tmp_path / locked_test.RESTRICTED_ROOT).mkdir(parents=True)
    return tmp_path


# --- W-1 / R-44: the source inventory ------------------------------------------------


def test_nine_field_entry_passes() -> None:
    assert_source_entry(_entry())


def test_missing_field_failure_names_entry_and_field() -> None:
    with pytest.raises(InventoryError) as excinfo:
        assert_source_entry(_entry(coverage=""))
    message = str(excinfo.value)
    assert "syn_product_v1.txt" in message and "coverage" in message


def test_fewer_than_nine_fields_fails_naming_every_missing_field() -> None:
    entry = _entry()
    del entry["role"], entry["release_status"]
    with pytest.raises(InventoryError) as excinfo:
        assert_source_entry(entry)
    assert "role" in str(excinfo.value) and "release_status" in str(excinfo.value)


def test_release_hash_mismatch_fails(tmp_path: Path) -> None:
    artifact = tmp_path / "syn_product_v1.txt"
    artifact.write_text("synthetic bytes", encoding="utf-8")
    from src.data.inventory import assert_entry_matches_release

    with pytest.raises(InventoryError) as excinfo:
        assert_entry_matches_release(_entry(), artifact)  # checksum "000…" cannot match
    assert "hash" in str(excinfo.value).lower()


def test_verbatim_notice_absent_fails() -> None:
    with pytest.raises(InventoryError) as excinfo:
        assert_verbatim_notice(_entry(), "The required verbatim text.")
    assert "verbatim" in str(excinfo.value)


def test_paraphrased_notice_fails_and_verbatim_passes() -> None:
    required = "Data were provided by the Synthetic Data Centre."
    with pytest.raises(InventoryError):
        assert_verbatim_notice(
            _entry(acknowledgment_notice="Data came from the Synthetic Data Centre."),
            required,
        )
    assert_verbatim_notice(_entry(acknowledgment_notice=required), required)


def test_write_source_inventory_enforces_notices_and_writes(tmp_path: Path) -> None:
    required = {"synthetic-provider": "The required verbatim text."}
    with pytest.raises(InventoryError):
        write_source_inventory(tmp_path / "inv.json", [_entry()], required_notices=required)
    path = write_source_inventory(
        tmp_path / "inv.json",
        [_entry(acknowledgment_notice="The required verbatim text.")],
        required_notices=required,
        missing_entries=["synthetic shortfall, recorded machine-readably"],
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["missing_entries"] == ["synthetic shortfall, recorded machine-readably"]


def test_inventory_refuses_credential_shaped_values(tmp_path: Path) -> None:
    """SD-I-06: the access-notes field is a secret-egress surface; the chokepoint fires."""
    entry = _entry(licence_access_notes="Bearer abcdefghijklmnop0123456789ABCDEFGH")
    with pytest.raises(CredentialEgressError):
        write_source_inventory(tmp_path / "inv.json", [entry])


# --- W-5 / R-49: schema validation ----------------------------------------------------


_EXPECTED_SCHEMA = {
    "parameters": {
        "tec": {"unit": "TECU", "fill_value": "nan"},
        "dtec": {"unit": "TECU", "fill_value": "nan"},
    },
    "cadence_seconds": 3600,
    "duplicate_policy": "none",
}


def _observed(**overrides: object) -> dict:
    observed: dict = {
        "parameters": {
            "tec": {"unit": "TECU", "fill_value": "nan"},
            "dtec": {"unit": "TECU", "fill_value": "nan"},
        },
        "timestamps": ["2021-06-01T00:00:00+00:00", "2021-06-01T01:00:00+00:00"],
    }
    observed.update(overrides)
    return observed


def test_matching_schema_yields_self_contained_report() -> None:
    report = validate_schema(_observed(), _EXPECTED_SCHEMA)
    assert report.expected_schema_digest == schema_digest(_EXPECTED_SCHEMA)
    assert report.observed["parameters"]["tec"]["unit"] == "TECU"


def test_renamed_parameter_fails() -> None:
    observed = _observed()
    observed["parameters"] = {"tec_renamed": {"unit": "TECU", "fill_value": "nan"}}
    with pytest.raises(SchemaError):
        validate_schema(observed, _EXPECTED_SCHEMA)


def test_changed_unit_fails() -> None:
    observed = _observed()
    observed["parameters"]["tec"] = {"unit": "el/m^2", "fill_value": "nan"}
    with pytest.raises(SchemaError) as excinfo:
        validate_schema(observed, _EXPECTED_SCHEMA)
    assert "unit" in str(excinfo.value)


def test_altered_fill_value_fails() -> None:
    observed = _observed()
    observed["parameters"]["tec"] = {"unit": "TECU", "fill_value": -999}
    with pytest.raises(SchemaError) as excinfo:
        validate_schema(observed, _EXPECTED_SCHEMA)
    assert "fill value" in str(excinfo.value)


def test_broken_utc_cadence_fails() -> None:
    observed = _observed(
        timestamps=["2021-06-01T00:00:00+00:00", "2021-06-01T00:47:00+00:00"]
    )
    with pytest.raises(SchemaError) as excinfo:
        validate_schema(observed, _EXPECTED_SCHEMA)
    assert "cadence" in str(excinfo.value)


def test_non_utc_timestamp_fails() -> None:
    observed = _observed(timestamps=["2021-06-01T00:00:00+02:00"])
    with pytest.raises(SchemaError):
        validate_schema(observed, _EXPECTED_SCHEMA)


def test_duplicate_timestamp_fails() -> None:
    observed = _observed(
        timestamps=["2021-06-01T00:00:00+00:00", "2021-06-01T00:00:00+00:00"]
    )
    with pytest.raises(SchemaError) as excinfo:
        validate_schema(observed, _EXPECTED_SCHEMA)
    assert "duplicate" in str(excinfo.value)


def test_modified_expected_schema_changes_the_digest() -> None:
    modified = json.loads(json.dumps(_EXPECTED_SCHEMA))
    modified["cadence_seconds"] = 7200
    assert schema_digest(modified) != schema_digest(_EXPECTED_SCHEMA)


def test_absent_prepared_schema_is_a_stop_and_report() -> None:
    with pytest.raises(PreflightError):
        expected_schema_from({})
    with pytest.raises(PreflightError):
        expected_schema_from({"prepared_schema": TBD_SENTINEL})


# --- R-50 check 1: the declared scope, refused BEFORE any read -------------------------


def test_eleven_month_declaration_fails_before_any_read() -> None:
    reference = _scope()
    declared = _scope(months=AUDIT_MONTHS[:-1])
    with pytest.raises(AuditScopeError) as excinfo:
        assert_scope_equals_reference(declared, reference)
    assert excinfo.value.resource == "declared audit scope"  # never a file path


def test_short_december_day_range_fails() -> None:
    with pytest.raises(AuditScopeError) as excinfo:
        assert_scope_equals_reference(_scope(december_days=(1, 30)), _scope())
    assert "31" in str(excinfo.value)


def test_omitted_cell_fails() -> None:
    with pytest.raises(AuditScopeError):
        assert_scope_equals_reference(_scope(cells={}), _scope())


def test_omitted_artifact_class_fails() -> None:
    with pytest.raises(AuditScopeError):
        assert_scope_equals_reference(_scope(artifact_classes=()), _scope())


def test_reference_scope_refuses_while_stations_are_tbd() -> None:
    with pytest.raises(PreflightError) as excinfo:
        governed_reference_scope({"stations": TBD_SENTINEL}, [_entry()])
    assert "TBD" in str(excinfo.value)


def test_reference_scope_derives_classes_from_the_inventory() -> None:
    data = {"stations": {"SYNA": {"cell": [10, 20]}}}
    reference = governed_reference_scope(data, [_entry()])
    assert reference.artifact_classes == ("prepared-product",)
    assert reference.december_days == (1, 31)
    assert len(reference.months) == 12


# --- R-50 check 2 / SD-I-04: routing, purposes, class agreement ------------------------


def test_audit_run_id_format_is_unique_per_attempt() -> None:
    first, second = new_audit_run_id(), new_audit_run_id()
    pattern = r"^audit-\d{8}T\d{6}Z-[0-9a-f]{8}$"
    assert re.match(pattern, first) and re.match(pattern, second)
    assert first != second


def test_locked_evaluation_purpose_is_refused() -> None:
    with pytest.raises(LockedTestError) as excinfo:
        audit_access_record("audit-x", limb="coverage", purpose="locked_evaluation")
    assert "G-06" in str(excinfo.value)


def test_limb_and_purpose_are_paired_not_interchangeable() -> None:
    with pytest.raises(LockedTestError):
        audit_access_record("audit-x", limb="regime", purpose="coverage_audit")
    with pytest.raises(LockedTestError):
        audit_access_record("audit-x", limb="coverage", purpose="regime_audit")


def test_each_limb_binds_its_literal() -> None:
    coverage = audit_access_record("audit-x", limb="coverage", artifact_identity="a")
    regime = audit_access_record("audit-x", limb="regime", artifact_identity="a")
    assert coverage.purpose == "coverage_audit"
    assert regime.purpose == "regime_audit"
    assert coverage.performance_inspected is False and regime.performance_inspected is False
    assert coverage.locked_test_accessed is True


def test_ordinary_path_is_read_directly_and_never_logged(synthetic_root: Path) -> None:
    ordinary = synthetic_root / "ordinary_artifact.json"
    ordinary.write_text("{}", encoding="utf-8")
    registry = synthetic_root / "access_log.jsonl"
    routed = route_audit_path(
        ordinary, december_bearing=False, run_id="audit-x", limb="coverage", registry=registry
    )
    assert routed.read_text(encoding="utf-8") == "{}"
    assert not registry.exists(), "an ordinary read must produce NO access row"


def test_restricted_class_read_is_logged_before_and_placeholder_is_gone(
    synthetic_root: Path,
) -> None:
    """DISC-I-2 discharged: a real call-time retrieved_at_utc, a guard-stamped
    logged_at_utc, one durable row per artifact BEFORE the read."""
    restricted_dir = synthetic_root / locked_test.RESTRICTED_ROOT
    artifact = restricted_dir / "synthetic_restricted.json"
    artifact.write_text("{}", encoding="utf-8")
    registry = synthetic_root / "access_log.jsonl"
    run_id = new_audit_run_id()
    routed = route_audit_path(
        artifact, december_bearing=True, run_id=run_id, limb="coverage", registry=registry
    )
    rows = [json.loads(line) for line in registry.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    row = rows[0]
    assert row["run_id"] == run_id
    assert row["purpose"] == "coverage_audit"
    assert row["performance_inspected"] is False
    assert row["retrieved_at_utc"] != "recorded-at-call-time-by-the-runner"
    assert row["retrieved_at_utc"].startswith("202")
    assert "logged_at_utc" in row
    assert routed.read_text(encoding="utf-8") == "{}"


def test_december_bearing_class_outside_root_is_a_stop_and_report(
    synthetic_root: Path,
) -> None:
    stray = synthetic_root / "stray_artifact.csv"
    stray.write_text("station,timestamp\n", encoding="utf-8")
    with pytest.raises(LockedTestError) as excinfo:
        route_audit_path(
            stray,
            december_bearing=True,
            run_id="audit-x",
            limb="coverage",
            registry=synthetic_root / "access_log.jsonl",
        )
    assert "stray_artifact.csv" in str(excinfo.value)  # names the file
    assert "OUTSIDE" in str(excinfo.value)


def test_ordinary_class_inside_root_is_a_stop_and_report(synthetic_root: Path) -> None:
    inside = synthetic_root / locked_test.RESTRICTED_ROOT / "misfiled_ordinary.csv"
    inside.write_text("station,timestamp\n", encoding="utf-8")
    with pytest.raises(LockedTestError) as excinfo:
        route_audit_path(
            inside,
            december_bearing=False,
            run_id="audit-x",
            limb="coverage",
            registry=synthetic_root / "access_log.jsonl",
        )
    assert "misfiled_ordinary.csv" in str(excinfo.value)


def test_ordinary_read_carrying_a_locked_month_record_stops_and_reports(
    tmp_path: Path,
) -> None:
    """The realized TEC-09 shape, executed on a SYNTHETIC locked month: a record whose
    observation date falls in the locked month, read through an ordinary route, is a
    stop-and-report naming the file — the month directory's name plays no role."""
    artifact = tmp_path / "synthetic_month_2021-05" / "records.csv"
    artifact.parent.mkdir(parents=True)
    artifact.write_text("synthetic", encoding="utf-8")
    records = [
        {"station": "SYNA", "timestamp": "2021-05-30T23:00:00+00:00"},
        {"station": "SYNA", "timestamp": "2021-06-02T01:00:00+00:00"},  # locked month
    ]
    with pytest.raises(LockedTestError) as excinfo:
        assert_record_date_class_agreement(
            artifact, records, december_bearing=False, locked=SYNTHETIC_LOCKED
        )
    assert "records.csv" in str(excinfo.value)


def test_restricted_routed_artifact_with_no_locked_record_also_disagrees(
    tmp_path: Path,
) -> None:
    artifact = tmp_path / "records.csv"
    records = [{"station": "SYNA", "timestamp": "2021-05-30T23:00:00+00:00"}]
    with pytest.raises(LockedTestError):
        assert_record_date_class_agreement(
            artifact, records, december_bearing=True, locked=SYNTHETIC_LOCKED
        )


# --- membership by record timestamps, never names --------------------------------------


def test_month_attribution_follows_the_timestamp_not_the_directory() -> None:
    """R-50's negative control: a record whose timestamp falls in month M+1, filed under
    month M's directory, is attributed to M+1 and M's count does not move."""
    records = [
        {"station": "SYNA", "timestamp": "2022-05-31T23:00:00+00:00"},
        {"station": "SYNA", "timestamp": "2022-06-01T00:00:00+00:00"},  # misfiled in May
    ]
    by_month, excluded = attribute_records_by_month(records)
    assert excluded == 0
    assert len(by_month["2022-05"]) == 1
    assert len(by_month["2022-06"]) == 1


def test_out_of_year_records_are_excluded_from_every_per_month_statistic() -> None:
    records = [
        {"station": "SYNA", "timestamp": "2022-05-01T00:00:00+00:00"},
        {"station": "SYNA", "timestamp": "2023-05-01T00:00:00+00:00"},
    ]
    by_month, excluded = attribute_records_by_month(records)
    assert excluded == 1
    assert sorted(by_month) == ["2022-05"]


def test_unparseable_record_timestamp_fails_closed() -> None:
    with pytest.raises(InventoryError):
        attribute_records_by_month([{"station": "SYNA", "timestamp": "not-a-date"}])


# --- the data07 caveat -----------------------------------------------------------------


def test_absent_provenance_class_is_a_stop_and_report_never_an_uncaveated_figure() -> None:
    with pytest.raises(PreflightError) as excinfo:
        data07_caveat_for("2022-05", None)
    assert "18.3" in str(excinfo.value)


def test_unknown_provenance_class_is_refused() -> None:
    with pytest.raises(PreflightError):
        data07_caveat_for("2022-05", "mystery")


def test_caveat_populated_for_derived_only_and_absent_for_full() -> None:
    assert data07_caveat_for("2022-05", "derived_only") == DATA07_CAVEAT
    assert data07_caveat_for("2022-05", "full") is None


def test_coverage_figures_carry_the_caveat_for_derived_only_months() -> None:
    records = [{"station": "SYNA", "timestamp": "2022-05-01T00:00:00+00:00"}]
    by_month, _ = attribute_records_by_month(records)
    figures = coverage_figures(by_month, provenance_classes={"2022-05": "derived_only"})
    assert figures[0]["data07_caveat"] == DATA07_CAVEAT
    assert_figures_caveated(figures)


def test_caveatless_derived_only_figure_fails() -> None:
    figure = {"station": "SYNA", "month": "2022-05", "provenance_class": "derived_only"}
    with pytest.raises(GateError) as excinfo:
        assert_figures_caveated([figure])
    assert "data07_caveat" in str(excinfo.value)


# --- performance blindness --------------------------------------------------------------


def test_performance_figure_in_a_report_fails() -> None:
    with pytest.raises(GateError) as excinfo:
        assert_performance_blind({"per_month": {}, "rmse": 0.5}, resource="coverage report")
    assert "rmse" in str(excinfo.value)


def test_clean_report_is_performance_blind() -> None:
    assert_performance_blind({"per_month": {"2022-05": 1}}, resource="coverage report")


# --- R-50 check 3 / SD-I-05: per-run_id reconciliation, December included in 3b ---------


def _write_rows(registry: Path, rows: list[dict]) -> None:
    with registry.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def test_reconciliation_3a_is_per_run_id(tmp_path: Path) -> None:
    registry = tmp_path / "access_log.jsonl"
    _write_rows(
        registry,
        [
            {"run_id": "audit-A", "scope": "artifact-1"},
            {"run_id": "audit-A", "scope": "artifact-2"},
            {"run_id": "audit-B", "scope": "stale-row-from-an-interrupted-attempt"},
        ],
    )
    per_month = {month: 1 for month in AUDIT_MONTHS}
    # Attempt A reconciles against ITS OWN rows; attempt B's standing row is ignored.
    reconcile_audit(
        "audit-A",
        registry_path=registry,
        declared=_scope(),
        december_identities=["artifact-1", "artifact-2"],
        per_month_output=per_month,
    )


def test_reconciliation_3a_mismatch_fails(tmp_path: Path) -> None:
    registry = tmp_path / "access_log.jsonl"
    _write_rows(registry, [{"run_id": "audit-A", "scope": "artifact-1"}])
    per_month = {month: 1 for month in AUDIT_MONTHS}
    with pytest.raises(AuditScopeError) as excinfo:
        reconcile_audit(
            "audit-A",
            registry_path=registry,
            declared=_scope(),
            december_identities=["artifact-1", "artifact-2"],
            per_month_output=per_month,
        )
    assert "artifact-2" in str(excinfo.value)


def test_reconciliation_3b_covers_all_twelve_months_december_included(
    tmp_path: Path,
) -> None:
    """The 2026-09-02 correction's control: a report whose December count was dropped
    fails 3b even when every access row reconciles."""
    registry = tmp_path / "access_log.jsonl"
    _write_rows(registry, [{"run_id": "audit-A", "scope": "artifact-1"}])
    eleven = {month: 1 for month in AUDIT_MONTHS[:-1]}  # December's count dropped
    with pytest.raises(AuditScopeError) as excinfo:
        reconcile_audit(
            "audit-A",
            registry_path=registry,
            declared=_scope(),
            december_identities=["artifact-1"],
            per_month_output=eleven,
        )
    assert AUDIT_MONTHS[-1] in str(excinfo.value)


# --- the regime report and the one-day excess -------------------------------------------


def test_event_wholly_outside_the_scored_set_is_reported_separately_not_tallied() -> None:
    events = [
        {  # wholly before the synthetic scored set opens on day 2
            "event_id": "SYN-EV-1",
            "pre_window_start_utc": "2021-05-31T12:00:00+00:00",
            "end_utc": "2021-06-01T18:00:00+00:00",
            "start_utc": "2021-06-01T06:00:00+00:00",
        },
        {  # reaches into the scored set
            "event_id": "SYN-EV-2",
            "pre_window_start_utc": "2021-06-04T00:00:00+00:00",
            "end_utc": "2021-06-05T12:00:00+00:00",
            "start_utc": "2021-06-04T12:00:00+00:00",
        },
    ]
    report = build_regime_report(events, audit_year=2021, locked_month=6)
    assert report["tally"] == 1
    assert [event["event_id"] for event in report["unscored_events"]] == ["SYN-EV-1"]
    assert_regime_report_states_range(report)


def test_regime_report_without_its_day_range_fails() -> None:
    report = build_regime_report([], audit_year=2021, locked_month=6)
    del report["count_window"]
    with pytest.raises(GateError):
        assert_regime_report_states_range(report)


# --- all-or-nothing evidence -------------------------------------------------------------


def test_interrupted_audit_leaves_no_report_while_rows_stand(tmp_path: Path) -> None:
    registry = tmp_path / "access_log.jsonl"
    _write_rows(registry, [{"run_id": "audit-A", "scope": "artifact-1"}])
    out_dir = tmp_path / "reports"
    coverage_report = {"figures": [], "per_month": {m: 1 for m in AUDIT_MONTHS[:-1]}}
    regime = build_regime_report([], audit_year=2021, locked_month=6)
    with pytest.raises(AuditScopeError):
        finalize_audit_reports(
            out_dir,
            run_id="audit-A",
            registry_path=registry,
            declared=_scope(),
            december_identities=["artifact-1"],
            coverage_report=coverage_report,
            regime_report=regime,
        )
    assert not out_dir.exists() or not list(out_dir.iterdir()), "NO report on failure"
    assert registry.read_text(encoding="utf-8").strip(), "the rows stand (NFR-AUD-01)"


def test_consistent_audit_writes_both_reports(tmp_path: Path) -> None:
    registry = tmp_path / "access_log.jsonl"
    _write_rows(registry, [{"run_id": "audit-A", "scope": "artifact-1"}])
    out_dir = tmp_path / "reports"
    coverage_report = {"figures": [], "per_month": {m: 1 for m in AUDIT_MONTHS}}
    regime = build_regime_report([], audit_year=2021, locked_month=6)
    coverage_path, regime_path = finalize_audit_reports(
        out_dir,
        run_id="audit-A",
        registry_path=registry,
        declared=_scope(),
        december_identities=["artifact-1"],
        coverage_report=coverage_report,
        regime_report=regime,
    )
    assert coverage_path.is_file() and regime_path.is_file()


# --- R-51 / R-52: the G-P1A record and the four prohibitions -----------------------------


_THRESHOLDS = {
    "hourly_coverage_min_pct": 90,
    "day_coverage_min_pct": 95,
    "december_days_required": 31,
}

_ALL_PASS = {name: "PASS" for name in (
    "silent_imputation",
    "source_mixing",
    "retrospective_split_redesign",
    "map_value_mislabel",
)}


def _figure(**overrides: object) -> dict:
    figure: dict = {
        "station": "SYNA",
        "month": "2022-05",
        "days_present": 31,
        "days_in_month": 31,
        "day_coverage_pct": 100.0,
        "hourly_bins_present": 744,
        "hourly_bins_in_month": 744,
        "hourly_coverage_pct": 100.0,
        "provenance_class": "derived_only",
        "data07_caveat": DATA07_CAVEAT,
    }
    figure.update(overrides)
    return figure


def test_gp1a_thresholds_are_read_from_config_never_inlined() -> None:
    with pytest.raises(PreflightError):
        gp1a_thresholds_from({})
    with pytest.raises(PreflightError):
        gp1a_thresholds_from({"gp1a": TBD_SENTINEL})
    with pytest.raises(PreflightError):
        gp1a_thresholds_from({"gp1a": {"hourly_coverage_min_pct": 90}})
    block = gp1a_thresholds_from({"gp1a": dict(_THRESHOLDS)})
    assert block["december_days_required"] == 31


def test_passing_day_rule_but_failing_hourly_gate_fails_the_verdict() -> None:
    """R-51: neither threshold substitutes for the other."""
    record = build_gp1a_record(
        [_figure(hourly_coverage_pct=89.9)],
        thresholds=_THRESHOLDS,
        prohibition_results=_ALL_PASS,
    )
    assert record["station_months"][0]["verdict"] == "FAIL"


def test_both_thresholds_passing_yields_pass_with_attribution() -> None:
    record = build_gp1a_record(
        [_figure()], thresholds=_THRESHOLDS, prohibition_results=_ALL_PASS
    )
    entry = record["station_months"][0]
    assert entry["verdict"] == "PASS"
    assert entry["hourly_judged_against"] == "D-12"
    assert entry["day_judged_against"] == "D-2"
    assert_gp1a_record(record)


def test_verdict_with_no_measured_figure_fails() -> None:
    record = build_gp1a_record(
        [_figure()], thresholds=_THRESHOLDS, prohibition_results=_ALL_PASS
    )
    record["station_months"][0]["hourly_coverage_pct"] = None
    with pytest.raises(GateError) as excinfo:
        assert_gp1a_record(record)
    assert "measured figure" in str(excinfo.value)


def test_figure_without_d_number_attribution_fails() -> None:
    record = build_gp1a_record(
        [_figure()], thresholds=_THRESHOLDS, prohibition_results=_ALL_PASS
    )
    record["station_months"][0]["hourly_judged_against"] = ""
    with pytest.raises(GateError) as excinfo:
        assert_gp1a_record(record)
    assert "unattributed" in str(excinfo.value)


def test_record_omitting_d2_disclosure_fails() -> None:
    record = build_gp1a_record(
        [_figure()], thresholds=_THRESHOLDS, prohibition_results=_ALL_PASS
    )
    record["d2_disclosure"] = ""
    with pytest.raises(GateError) as excinfo:
        assert_gp1a_record(record)
    assert "disclosure" in str(excinfo.value)


def test_derived_only_record_entry_without_caveat_fails() -> None:
    record = build_gp1a_record(
        [_figure()], thresholds=_THRESHOLDS, prohibition_results=_ALL_PASS
    )
    del record["station_months"][0]["data07_caveat"]
    with pytest.raises(GateError):
        assert_gp1a_record(record)


def test_removing_any_one_of_the_four_prohibition_results_fails_the_gate() -> None:
    for name in _ALL_PASS:
        partial = {key: value for key, value in _ALL_PASS.items() if key != name}
        with pytest.raises(GateError) as excinfo:
            assert_prohibition_results(partial)
        assert name in str(excinfo.value)


def test_a_non_passing_prohibition_result_fails_by_name() -> None:
    results = dict(_ALL_PASS)
    results["source_mixing"] = "FAIL"
    with pytest.raises(GateError) as excinfo:
        assert_prohibition_results(results)
    assert "source_mixing" in str(excinfo.value)


def test_injected_imputed_value_fails() -> None:
    """R-52 prohibition 1 (this unit's): an imputed value must fail."""
    with pytest.raises(GateError) as excinfo:
        assert_no_silent_imputation([1.0, None, 3.0], [1.0, 2.0, 3.0], series="syn-series")
    assert "imputation" in str(excinfo.value)
    assert_no_silent_imputation([1.0, None, 3.0], [1.0, float("nan"), 3.0], series="s")


def test_injected_mixed_source_artifact_fails() -> None:
    """R-52 prohibition 2 (this unit's): a mixed-source artifact must fail."""
    rows = [{"source_id": "syn-a"}, {"source_id": "syn-b"}]
    with pytest.raises(GateError) as excinfo:
        assert_unmixed_sources(rows, artifact="syn-artifact")
    assert "syn-a" in str(excinfo.value) and "syn-b" in str(excinfo.value)
    assert_unmixed_sources([{"source_id": "syn-a"}], artifact="syn-artifact")
    with pytest.raises(GateError):
        assert_unmixed_sources([{"other": 1}], artifact="syn-artifact")


# --- the stage script's BLK-07 refusal ----------------------------------------------------


def _load_stage_script():
    path = REPO_ROOT / "scripts" / "01_inventory_and_registry.py"
    spec = importlib.util.spec_from_file_location("stage01_inventory_and_registry", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_audit_entry_point_refuses_naming_blk07() -> None:
    """The approved plan's hard constraint: the December audit is NOT executed; the
    script's audit entry point refuses while BLK-07's authorization limb stands."""
    stage01 = _load_stage_script()
    assert stage01._DECEMBER_AUDIT_AUTHORIZATION is None
    with pytest.raises(LockedTestError) as excinfo:
        stage01._require_december_authorization()
    message = str(excinfo.value)
    assert "BLK-07" in message
    assert "2022-12" in message
