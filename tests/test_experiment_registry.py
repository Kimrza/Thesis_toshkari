"""C-2 Registry writer tests: TA-10/TA-21 subjects (NFR-AUD-01, FR-P1-05-13).

Purpose
-------
Negative controls and happy paths for `src/data/experiment_registry.py`, per the
code-generation plan step 6 and rules R-07, R-08, R-09, R-10, R-18, R-19, R-20:
unknown status refused; write-time twenty-column schema violations refused (one absent
column at a time, so the assertion cannot pass on a subset); no code path can locate or
rewrite a prior row; orphans detected in BOTH directions and reported, back-fill
impossible (the reconciliation never writes); the durability stamp present on an
uncharacterised platform; failed/aborted runs remaining visible with status and reason;
the torn-write three-case distinction; the `exploratory` derivation with its G-06
carve-out; the forbidden `prediction_hash` writers; and R-10's report-honestly-even-
when-reporting-fails behaviour.

Inputs
------
`tmp_path` and `capsys` only. Every registry and access log is synthesised in tmp
space; the real `evidence/` tree is never read or written, and no restricted-root path
is constructed.

Re-run behaviour
----------------
Deterministic and self-contained; no network, no clock dependence beyond fixed ISO
timestamps embedded in the fixtures.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import src.data.experiment_registry as registry_module  # noqa: E402
from src.data.config import RegistryError  # noqa: E402
from src.data.experiment_registry import (  # noqa: E402
    EXTENSION_FIELDS,
    REGISTRY_COLUMNS,
    STATUSES,
    append_registry_event,
    check_registry_integrity,
    derive_csv,
    reconcile_access_records,
    record_abort_honestly,
)


def _row(**overrides) -> dict:
    """A complete, valid twenty-column row (Phase 1, no December access)."""
    base = {
        "run_id": "run-0001",
        "started_at_utc": "2026-09-05T10:00:00Z",
        "completed_at_utc": "",
        "status": "started",
        "code_commit": "a" * 40,
        "environment_lock_hash": "b" * 64,
        "platform": "local",
        "dataset_version": "",
        "fold_id": "",
        "mask_id": "",
        "feature_set_id": "",
        "model_id": "",
        "hyperparameters_json": "",
        "seed": 42,
        "validation_metric_name": "",
        "validation_metric_value": "",
        "artifact_manifest_path": "",
        "prediction_hash": "",
        "locked_test_accessed": False,
        "notes": "",
    }
    base.update(overrides)
    return base


def _access(run_id: str, ts: str, purpose: str = "coverage_audit") -> dict:
    return {
        "run_id": run_id,
        "retrieved_at_utc": ts,
        "logged_at_utc": ts,
        "scope": "synthetic",
        "purpose": purpose,
        "performance_inspected": False,
        "locked_test_accessed": True,
        "authorization": "synthetic test fixture",
    }


@pytest.fixture()
def paths(tmp_path):
    return tmp_path / "experiment_registry.jsonl", tmp_path / "access_log.jsonl"


def _append(registry, access, **kw) -> dict:
    defaults = dict(phase=1, writer_role="stage", access_log_path=access)
    defaults.update(kw)
    return append_registry_event(registry, _row(**kw.pop("row", {})), **defaults)


# --- R-07: the closed status vocabulary --------------------------------------------------


def test_unknown_status_is_refused(paths) -> None:
    registry, access = paths
    with pytest.raises(RegistryError) as excinfo:
        append_registry_event(
            registry,
            _row(status="running"),
            phase=1,
            writer_role="stage",
            access_log_path=access,
        )
    assert "unknown status" in str(excinfo.value)
    assert not registry.exists(), "a refused write must leave nothing behind"


def test_aborted_with_empty_reason_is_refused(paths) -> None:
    registry, access = paths
    with pytest.raises(RegistryError) as excinfo:
        append_registry_event(
            registry,
            _row(status="aborted", reason="  "),
            phase=1,
            writer_role="stage",
            access_log_path=access,
        )
    assert "reason" in str(excinfo.value)


def test_the_vocabulary_is_exactly_four(paths) -> None:
    assert STATUSES == {"started", "completed", "aborted", "failed"}


# --- R-18: the write-time twenty-column schema assertion ---------------------------------


@pytest.mark.parametrize("column", REGISTRY_COLUMNS)
def test_each_missing_column_is_refused_and_named(paths, column) -> None:
    """One absent column at a time — the assertion cannot pass by checking a subset."""
    registry, access = paths
    row = _row()
    del row[column]
    if column == "status":
        # Without a status the vocabulary check fires first; both are refusals.
        with pytest.raises(RegistryError):
            append_registry_event(
                registry, row, phase=1, writer_role="stage", access_log_path=access
            )
        return
    with pytest.raises(RegistryError) as excinfo:
        append_registry_event(
            registry, row, phase=1, writer_role="stage", access_log_path=access
        )
    assert column in str(excinfo.value), f"the absent column {column!r} must be NAMED"


@pytest.mark.parametrize("column", ["code_commit", "environment_lock_hash"])
def test_unpopulated_required_column_is_refused(paths, column) -> None:
    """FR-P1-05-13's second criterion: population, not mere presence."""
    registry, access = paths
    with pytest.raises(RegistryError) as excinfo:
        append_registry_event(
            registry,
            _row(**{column: "   "}),
            phase=1,
            writer_role="stage",
            access_log_path=access,
        )
    assert column in str(excinfo.value)


def test_prediction_hash_from_a_metric_computing_process_is_refused(paths) -> None:
    """R-18 limb 2: 07/bootstrap may not write the receipt they later consume."""
    registry, access = paths
    for role in ("evaluate", "bootstrap"):
        with pytest.raises(RegistryError) as excinfo:
            append_registry_event(
                registry,
                _row(prediction_hash="c" * 64),
                phase=1,
                writer_role=role,
                access_log_path=access,
            )
        assert "prediction_hash" in str(excinfo.value)
    # The training process (06) MAY write it.
    written = append_registry_event(
        registry,
        _row(prediction_hash="c" * 64),
        phase=1,
        writer_role="train",
        access_log_path=access,
    )
    assert written["prediction_hash"] == "c" * 64


def test_prior_period_exposure_true_on_a_phase1_row_is_refused(paths) -> None:
    """R-18: Phase 1 IS the first December exposure; `true` belongs to Phase 2."""
    registry, access = paths
    with pytest.raises(RegistryError) as excinfo:
        append_registry_event(
            registry,
            _row(prior_period_exposure=True),
            phase=1,
            writer_role="stage",
            access_log_path=access,
        )
    assert "prior_period_exposure" in str(excinfo.value)


# --- R-20: exploratory is derived, never caller-passed -----------------------------------


def test_caller_passed_exploratory_is_rejected(paths) -> None:
    registry, access = paths
    with pytest.raises(RegistryError) as excinfo:
        append_registry_event(
            registry,
            _row(exploratory=False),
            phase=1,
            writer_role="stage",
            access_log_path=access,
        )
    assert "exploratory" in str(excinfo.value)


def test_run_postdating_first_restricted_access_is_exploratory_on_the_row(paths) -> None:
    registry, access = paths
    access.write_text(
        json.dumps(_access("audit-run", "2026-09-01T00:00:00Z")) + "\n", encoding="utf-8"
    )
    written = append_registry_event(
        registry,
        _row(started_at_utc="2026-09-05T10:00:00Z"),
        phase=1,
        writer_role="stage",
        access_log_path=access,
    )
    assert written["exploratory"] is True
    on_disk = json.loads(registry.read_text(encoding="utf-8").splitlines()[0])
    assert on_disk["exploratory"] is True, "the label lands ON THE ROW, not in a report"


def test_run_predating_first_restricted_access_is_not_exploratory(paths) -> None:
    registry, access = paths
    access.write_text(
        json.dumps(_access("audit-run", "2026-09-08T00:00:00Z")) + "\n", encoding="utf-8"
    )
    written = append_registry_event(
        registry,
        _row(started_at_utc="2026-09-05T10:00:00Z"),
        phase=1,
        writer_role="stage",
        access_log_path=access,
    )
    assert written["exploratory"] is False


def test_g06_carveout_requires_the_runs_own_locked_evaluation_record(paths) -> None:
    """R-20's own control: the carve-out is keyed to purpose=locked_evaluation on the
    run's OWN AccessRecord and recorded on the row; a run without one is labelled true."""
    registry, access = paths
    access.write_text(
        json.dumps(_access("audit-run", "2026-09-01T00:00:00Z")) + "\n"
        + json.dumps(_access("g06-run", "2026-09-02T00:00:00Z", "locked_evaluation")) + "\n",
        encoding="utf-8",
    )
    # The G-06 confirmatory run: postdates the earliest access, carve-out applies.
    g06 = append_registry_event(
        registry,
        _row(run_id="g06-run", started_at_utc="2026-09-05T10:00:00Z",
             locked_test_accessed=True),
        phase=1,
        writer_role="stage",
        access_log_path=access,
    )
    assert g06["exploratory"] is False
    assert "carve-out" in g06["exploratory_carveout"]

    # A run CLAIMING the carve-out without its own locked_evaluation record: refused
    # (i.e. labelled true, carve-out not granted).
    pretender = append_registry_event(
        registry,
        _row(run_id="pretender-run", started_at_utc="2026-09-06T10:00:00Z"),
        phase=1,
        writer_role="stage",
        access_log_path=access,
    )
    assert pretender["exploratory"] is True
    assert pretender["exploratory_carveout"] == ""


# --- R-08 / R-09: append-only, no rewrite, visibility ------------------------------------


def test_the_module_exposes_no_rewrite_or_delete_path(paths) -> None:
    """R-09 negative control: an in-place status mutation is impossible through the API.
    The public surface is append + pure reads; nothing locates a prior row to change."""
    public = [name for name in registry_module.__all__]
    mutators = [n for n in public if any(v in n.lower() for v in ("update", "delete", "rewrite", "amend", "set_"))]
    assert mutators == [], f"the registry API must expose no rewrite path, found {mutators}"


def test_aborted_run_stays_visible_after_a_later_successful_run(paths) -> None:
    """NFR-AUD-01: the aborted row survives a subsequent successful run of the stage."""
    registry, access = paths
    append_registry_event(
        registry, _row(run_id="run-a"), phase=1, writer_role="stage", access_log_path=access
    )
    append_registry_event(
        registry,
        _row(run_id="run-a", status="aborted", reason="preflight raised: planted TBD"),
        phase=1,
        writer_role="stage",
        access_log_path=access,
    )
    append_registry_event(
        registry, _row(run_id="run-b"), phase=1, writer_role="stage", access_log_path=access
    )
    append_registry_event(
        registry,
        _row(run_id="run-b", status="completed", completed_at_utc="2026-09-05T11:00:00Z"),
        phase=1,
        writer_role="stage",
        access_log_path=access,
    )
    lines = [json.loads(ln) for ln in registry.read_text(encoding="utf-8").splitlines()]
    aborted = [ln for ln in lines if ln["status"] == "aborted"]
    assert len(aborted) == 1
    assert aborted[0]["run_id"] == "run-a"
    assert aborted[0]["reason"] == "preflight raised: planted TBD"


def test_every_row_carries_the_durability_stamp_on_an_uncharacterised_platform(
    paths,
) -> None:
    """SD-03 (Q3=B): the stamp is present; no platform has measured evidence yet."""
    registry, access = paths
    written = _append_simple(registry, access)
    assert "unverified on this platform" in written["durability"]
    on_disk = json.loads(registry.read_text(encoding="utf-8").splitlines()[0])
    assert "unverified on this platform" in on_disk["durability"]


def _append_simple(registry, access):
    return append_registry_event(
        registry, _row(), phase=1, writer_role="stage", access_log_path=access
    )


def test_field_order_puts_run_id_first(paths) -> None:
    """R-08: run_id is column 1 so a torn record's owner is recoverable from a prefix."""
    registry, access = paths
    _append_simple(registry, access)
    line = registry.read_text(encoding="utf-8").splitlines()[0]
    assert line.startswith('{"run_id"')
    parsed = json.loads(line)
    assert list(parsed) == [*REGISTRY_COLUMNS, *EXTENSION_FIELDS]


# --- the registry-integrity test: transition graph + torn writes -------------------------


def test_integrity_passes_on_a_legal_log(paths) -> None:
    registry, access = paths
    _append_simple(registry, access)
    append_registry_event(
        registry,
        _row(status="completed", completed_at_utc="2026-09-05T11:00:00Z"),
        phase=1,
        writer_role="stage",
        access_log_path=access,
    )
    report = check_registry_integrity(registry)
    assert report.violations == [] and report.rows == 2 and report.torn_final_run_id is None


@pytest.mark.parametrize(
    "events,expected",
    [
        ([("r", "started"), ("r", "started")], "duplicate started"),
        ([("r", "started"), ("r", "completed"), ("r", "failed")], "repeated terminal"),
        ([("r", "completed")], "no started row"),
        ([("r", "started"), ("r", "sideways")], "unknown status"),
    ],
)
def test_each_illegal_sequence_fails_the_integrity_test(paths, events, expected) -> None:
    """R-08 negative control: synthesise each rejected sequence; each must fail."""
    registry, _ = paths
    with registry.open("w", encoding="utf-8") as handle:
        for run_id, status in events:
            row = _row(run_id=run_id, status=status)
            if status in ("aborted", "failed"):
                row["reason"] = "synthetic"
            handle.write(json.dumps(row) + "\n")
    report = check_registry_integrity(registry)
    assert report.violations, f"sequence {events} must be rejected"
    assert any(expected in v for v in report.violations)


def test_torn_final_record_is_reported_with_its_run_id_not_rejected(paths) -> None:
    """R-08 torn-write case 1: a truncated FINAL record is a torn write; the run stays
    visible and the report names it."""
    registry, access = paths
    _append_simple(registry, access)
    full_line = json.dumps(_row(run_id="dying-run", status="aborted", reason="killed"))
    with registry.open("a", encoding="utf-8") as handle:
        handle.write(full_line[: len(full_line) // 2])  # truncated, no newline
    report = check_registry_integrity(registry)
    assert report.torn_final_run_id == "dying-run"
    assert report.torn_final_reported and "torn final record" in report.torn_final_reported
    assert not any("dying-run" in v for v in report.violations), (
        "a torn final record is reported, never rejected"
    )


def test_same_malformed_bytes_as_an_interior_line_are_rejected(paths) -> None:
    """R-08 torn-write case 2: interior malformation is corruption, rejected."""
    registry, access = paths
    torn_bytes = json.dumps(_row(run_id="dying-run"))[:40]
    with registry.open("w", encoding="utf-8") as handle:
        handle.write(torn_bytes + "\n")  # newline-terminated AND unparseable: interior
        handle.write(json.dumps(_row()) + "\n")
    report = check_registry_integrity(registry)
    assert any("malformed" in v for v in report.violations)


def test_a_row_reported_written_is_on_disk(paths) -> None:
    """R-08 torn-write case 3's invariant: after append returns, the record IS on disk —
    never a row reported written that is not (R-10 at the durability layer)."""
    registry, access = paths
    written = _append_simple(registry, access)
    on_disk = json.loads(registry.read_text(encoding="utf-8").splitlines()[-1])
    assert on_disk == written


# --- R-10: report honestly even when reporting fails -------------------------------------


def test_abort_record_success_path(paths) -> None:
    registry, access = paths
    ok = record_abort_honestly(
        registry,
        _row(status="aborted", reason="preflight raised"),
        phase=1,
        writer_role="stage",
        access_log_path=access,
        original_error=RuntimeError("original failure"),
    )
    assert ok is True
    assert json.loads(registry.read_text(encoding="utf-8"))["status"] == "aborted"


def test_when_the_registry_write_itself_fails_both_failures_reach_stderr(
    paths, capsys, tmp_path
) -> None:
    """R-10 negative control: unwritable registry path; both failures reported; no
    success claimed; the original exception preserved for the caller to re-raise."""
    _, access = paths
    unwritable = tmp_path / "not-a-dir-but-a-file"
    unwritable.write_text("occupied", encoding="utf-8")
    original = RuntimeError("preflight raised: the ORIGINAL failure")
    ok = record_abort_honestly(
        unwritable / "experiment_registry.jsonl",  # parent is a file: mkdir will fail
        _row(status="aborted", reason="preflight raised"),
        phase=1,
        writer_role="stage",
        access_log_path=access,
        original_error=original,
    )
    assert ok is False, "no claim that an aborted record was written"
    err = capsys.readouterr().err
    assert "ORIGINAL FAILURE" in err and "the ORIGINAL failure" in err
    assert "REGISTRY WRITE FAILURE" in err


# --- R-19: the reconciliation, orphans both ways, back-fill impossible -------------------


def test_unregistered_restricted_access_is_an_integrity_violation(paths) -> None:
    registry, access = paths
    _append_simple(registry, access)
    access.write_text(
        json.dumps(_access("ghost-run", "2026-09-01T00:00:00Z")) + "\n", encoding="utf-8"
    )
    with pytest.raises(RegistryError) as excinfo:
        reconcile_access_records(registry, access)
    assert "ghost-run" in str(excinfo.value)


def test_flag_without_logged_access_is_an_integrity_violation(paths) -> None:
    registry, access = paths
    append_registry_event(
        registry,
        _row(run_id="claimer", locked_test_accessed=True),
        phase=1,
        writer_role="stage",
        access_log_path=access,
    )
    with pytest.raises(RegistryError) as excinfo:
        reconcile_access_records(registry, access)
    assert "claimer" in str(excinfo.value)


def test_known_pre_guard_orphans_are_reported_with_reason_and_never_cleared(paths) -> None:
    """R-19's third control: the known orphans stay visible; nothing back-fills them.
    The five pre-guard rows and Rec-31's unresolved access are exactly this class."""
    registry, access = paths
    _append_simple(registry, access)
    access.write_text(
        json.dumps(_access("pre-guard-3", "2026-08-01T00:00:00Z")) + "\n", encoding="utf-8"
    )
    registry_bytes = registry.read_bytes()
    access_bytes = access.read_bytes()

    known = {"pre-guard-3": "retrospective pre-guard access (experiment_registry.md row 3)"}
    report = reconcile_access_records(registry, access, known_orphans=known)
    assert report.expected_orphans == known  # reported WITH the reason, not suppressed

    # Back-fill impossible: the reconciliation wrote nothing to either artifact.
    assert registry.read_bytes() == registry_bytes
    assert access.read_bytes() == access_bytes

    # And a future clean run cannot be achieved by hiding them: run again, same report.
    assert reconcile_access_records(registry, access, known_orphans=known).expected_orphans == known


# --- the derived CSV ---------------------------------------------------------------------


def test_derived_csv_is_hashed_and_marked_derived(paths, tmp_path) -> None:
    registry, access = paths
    _append_simple(registry, access)
    csv_path = tmp_path / "experiment_registry.csv"
    manifest = derive_csv(registry, csv_path)
    assert manifest["derived"] is True
    assert manifest["row_count"] == 1
    assert manifest["csv_sha256"] and manifest["source_sha256"]
    assert manifest["was_stale"] is False

    # Regenerating over a now-stale CSV records the shortfall machine-readably.
    _append_simple(registry, access)
    manifest2 = derive_csv(registry, csv_path)
    assert manifest2["was_stale"] is True  # the non-fatal tier: a field, never a raise
    sidecar = json.loads(
        (tmp_path / "experiment_registry.csv.manifest.json").read_text(encoding="utf-8")
    )
    assert sidecar["derived"] is True and sidecar["row_count"] == 2
