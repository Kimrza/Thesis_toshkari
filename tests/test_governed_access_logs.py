"""D-83 revision 7 §W7 W-9 (governed-log enumeration and the closed-log guard) and the
W-1 once-per-phase locked-evaluation refusal.

Purpose: prove the closed log refuses appends, holds harness rows only, and is out of the
governed scan set; that every enumerated writer targets the governed log; and that the 06
one-shot refusal matches exactly what D-83 says. Inputs: the real closed log (read-only,
no December content: it holds access RECORDS, not data) and synthetic logs in `tmp_path`.
Re-run behaviour: pure; the real closed log is never written.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.data.locked_test import (
    CLOSED_ACCESS_LOG,
    GOVERNED_ACCESS_LOG,
    AccessRecord,
    LockedTestError,
    _append_and_flush,
    assert_closed_log_harness_only,
    assert_first_locked_evaluation,
    is_closed_access_log,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

#: The enumerated governed-log writers (D-83 revision 7 A7 item 18): file -> literal.
WRITERS = {
    "scripts/gate_in_session.py": "merge_run_access_log.jsonl",
    "scripts/run_walking_skeleton.py": "merge_run_access_log.jsonl",
    "scripts/merge_coverage_year.py": "merge_run_access_log.jsonl",
    "scripts/00_acquire_prepared_vtec.py": "merge_run_access_log.jsonl",
    "scripts/audit_gfz_drivers.py": "merge_run_access_log.jsonl",
}


def _record(run_id: str, purpose: str = "coverage_audit", **kw) -> AccessRecord:
    return AccessRecord(
        run_id=run_id,
        retrieved_at_utc="2026-09-30T00:00:00+00:00",
        scope="synthetic",
        purpose=purpose,
        performance_inspected=False,
        locked_test_accessed=True,
        authorization="synthetic",
        **kw,
    )


def test_the_closed_log_refuses_an_append(tmp_path) -> None:
    closed = tmp_path / "evidence" / "test_run_access_log.jsonl"
    closed.parent.mkdir()
    closed.write_text("", encoding="utf-8")
    with pytest.raises(LockedTestError) as exc:
        _append_and_flush(closed, _record("r1"))
    assert "CLOSED" in str(exc.value)
    assert closed.read_text(encoding="utf-8") == ""


def test_the_governed_log_accepts_an_append(tmp_path) -> None:
    governed = tmp_path / "evidence" / "merge_run_access_log.jsonl"
    _append_and_flush(governed, _record("r1"))
    assert json.loads(governed.read_text(encoding="utf-8"))["run_id"] == "r1"


def test_the_real_closed_log_holds_harness_rows_only() -> None:
    path = REPO_ROOT / CLOSED_ACCESS_LOG
    assert is_closed_access_log(path)
    assert assert_closed_log_harness_only(path) == 5964


def test_a_non_harness_row_in_the_closed_log_is_refused(tmp_path) -> None:
    path = tmp_path / "evidence" / "test_run_access_log.jsonl"
    path.parent.mkdir()
    path.write_text(json.dumps({"run_id": "walking-skeleton-x"}) + "\n", encoding="utf-8")
    with pytest.raises(LockedTestError):
        assert_closed_log_harness_only(path)


@pytest.mark.parametrize("script,literal", sorted(WRITERS.items()))
def test_every_enumerated_writer_targets_the_governed_log(script, literal) -> None:
    source = (REPO_ROOT / script).read_text(encoding="utf-8")
    assert literal in source
    assert GOVERNED_ACCESS_LOG.endswith(literal)


def test_no_script_reads_or_writes_the_closed_log_as_its_access_log() -> None:
    for path in (REPO_ROOT / "scripts").glob("*.py"):
        for line in path.read_text(encoding="utf-8").splitlines():
            code = line.split("#", 1)[0]
            assert '"test_run_access_log.jsonl"' not in code, f"{path.name}: {line.strip()}"


# --- W-1: once per phase_id for the 06 locked evaluation ----------------------------


def _log(tmp_path: Path, *rows: dict) -> Path:
    path = tmp_path / "merge_run_access_log.jsonl"
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return path


def _row(run_id, script_id="06_train_and_predict", phase_id="P1A", logged="2026-10-01T00:00:00+00:00", purpose="locked_evaluation"):
    row = {"run_id": run_id, "purpose": purpose, "logged_at_utc": logged}
    if script_id is not None:
        row["script_id"] = script_id
    if phase_id is not None:
        row["phase_id"] = phase_id
    return row


def _check(path, run_id="new", **kw):
    assert_first_locked_evaluation(path, run_id=run_id, script_id="06_train_and_predict", phase_id="P1A", **kw)


def test_first_06_run_passes_on_an_empty_or_absent_log(tmp_path) -> None:
    _check(tmp_path / "absent.jsonl")
    _check(_log(tmp_path))


def test_a_05_row_does_not_block_the_first_06_run(tmp_path) -> None:
    _check(_log(tmp_path, _row("r05", script_id="05_build_features_and_splits"), _row("r07", script_id="07_evaluate_and_report")))


def test_a_repeated_06_run_is_refused(tmp_path) -> None:
    with pytest.raises(LockedTestError):
        _check(_log(tmp_path, _row("r06")))


@pytest.mark.parametrize("missing", ["script_id", "phase_id"])
def test_a_record_missing_a_field_counts_as_a_match(tmp_path, missing) -> None:
    with pytest.raises(LockedTestError):
        _check(_log(tmp_path, _row("old", **{missing: None})))


def test_another_phase_does_not_block(tmp_path) -> None:
    _check(_log(tmp_path, _row("r06", phase_id="P2A")))


def test_rows_before_the_cutoff_do_not_match_and_own_rows_are_ignored(tmp_path) -> None:
    path = _log(tmp_path, _row("old", logged="2026-01-01T00:00:00+00:00"), _row("new"))
    _check(path, cutoff_utc="2026-06-01T00:00:00+00:00")
    with pytest.raises(LockedTestError):
        _check(path, run_id="other", cutoff_utc="2026-06-01T00:00:00+00:00")


def test_audit_purposes_never_match(tmp_path) -> None:
    _check(_log(tmp_path, _row("a", purpose="coverage_audit", script_id=None, phase_id=None)))


def test_an_unreadable_line_refuses(tmp_path) -> None:
    path = tmp_path / "log.jsonl"
    path.write_text("{not json\n", encoding="utf-8")
    with pytest.raises(LockedTestError):
        _check(path)


@pytest.mark.parametrize("missing", ["script_id", "phase_id"])
def test_locked_evaluation_record_requires_script_and_phase(missing) -> None:
    fields = {"script_id": "06_train_and_predict", "phase_id": "P1A"}
    fields.pop(missing)
    with pytest.raises(LockedTestError):
        _record("r", purpose="locked_evaluation", **fields)
    _record("r", purpose="coverage_audit")  # other purposes are unaffected


def test_builders_05_06_07_stamp_script_and_phase() -> None:
    for script in (
        "05_build_features_and_splits",
        "06_train_and_predict",
        "07_evaluate_and_report",
    ):
        source = (REPO_ROOT / "scripts" / f"{script}.py").read_text(encoding="utf-8")
        assert f'script_id="{script}"' in source
        assert "phase_id=phase_id" in source
    assert "assert_first_locked_evaluation(" in (
        REPO_ROOT / "scripts" / "06_train_and_predict.py"
    ).read_text(encoding="utf-8")


# --- GOV-2026-09-30-PV-09 remediation negative controls --------------------------------


@pytest.mark.parametrize("line", ["{garbage", "[1, 2]"])
def test_pv09_impl09_closed_log_malformed_row_is_refused_by_name(tmp_path, line) -> None:
    from src.data.locked_test import LockedTestError, assert_closed_log_harness_only

    path = tmp_path / "closed.jsonl"
    path.write_text(line + "\n", encoding="utf-8")
    with pytest.raises(LockedTestError) as exc:
        assert_closed_log_harness_only(path)
    assert "line 1" in str(exc.value)


def test_pv09_val04_z_cutoff_and_fractional_offset_row_order_correctly() -> None:
    from src.data.locked_test import _logged_before

    # lexically ".5+00:00" < "Z" would call this row pre-cutoff; parsed, it is after
    assert not _logged_before("2026-10-01T00:00:00.5+00:00", "2026-10-01T00:00:00Z")
    assert _logged_before("2026-09-30T23:00:00+00:00", "2026-10-01T00:00:00Z")
    assert _logged_before("2026-10-01T03:00:00+03:30", "2026-10-01T00:00:00Z")
    assert not _logged_before("not-a-time", "2026-10-01T00:00:00Z")


def test_pv09_val04_exploratory_derivation_uses_parsed_times() -> None:
    from src.data.experiment_registry import _derive_exploratory

    access = [{"run_id": "a", "logged_at_utc": "2026-10-01T00:00:00.5+00:00", "purpose": "coverage_audit"}]
    # started a quarter-second after the access, written with Z: postdates (exploratory)
    flag, _ = _derive_exploratory({"run_id": "r", "started_at_utc": "2026-10-01T00:00:00.75Z"}, access)
    assert flag is True
    # started in +03:30 before the access instant: does not postdate
    flag, _ = _derive_exploratory({"run_id": "r", "started_at_utc": "2026-10-01T03:29:00+03:30"}, access)
    assert flag is False


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("2026-10-01T00:00:00.5+00:00", "2026-10-01T00:00:00.500000+00:00"),
        ("2026-10-01T00:00:00.75Z", "2026-10-01T00:00:00.750000+00:00"),
        ("2026-10-01T00:00:00.1234567+03:30", "2026-10-01T00:00:00.123456+03:30"),
        ("2026-10-01T00:00:00Z", "2026-10-01T00:00:00+00:00"),
    ],
)
def test_parse_iso8601_utc_is_interpreter_independent(text: str, expected: str) -> None:
    """2026-10-01: Python 3.10 (environment (b)) rejected `.5` and `Z`, so custody ordering
    fell back to string comparison there. The helper must parse these on 3.10 and 3.11."""
    from src.data.config import parse_iso8601_utc

    parsed = parse_iso8601_utc(text)
    assert parsed is not None and parsed.isoformat() == expected


@pytest.mark.parametrize("text", ["2026-10-01T00:00:00", "not-a-time", "", "2026-13-01T00:00:00Z"])
def test_parse_iso8601_utc_refuses_naive_and_malformed(text: str) -> None:
    from src.data.config import parse_iso8601_utc

    assert parse_iso8601_utc(text) is None
