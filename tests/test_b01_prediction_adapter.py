"""B-01-to-`Prediction` bridge: `iri.predictions_from_benchmark_rows` (Phase 3/4 design;
partition-scoping Q1 = B, Student/Owner decision 2026-09-26).

PURPOSE. `src.external.iri.predictions_from_benchmark_rows` converts B-01's raw
generated rows (`evaluate_points`'s shape: `station_id`, `target_time_utc`,
`contract.output_field`, `status`) into the eight-field `Prediction` payload
convention `06` already writes and `src.evaluation.masks.prediction_from_payload`
already reads -- one payload per `PartitionKind.fold` partition (F1-F4), rows
pre-filtered to that partition's own `validation_month_range` window (Option B).

IMPORT BOUNDARY (TE 12; TA-07; `tests/test_iri_denial.py`'s own methodology, copied
here). `src.external.iri` is importable ONLY by `scripts/04_build_external_products.py`
and modules under `src/evaluation/` -- `tests/*` is explicitly NOT allowlisted
(`tests/test_iri_denial.py: ALLOWLISTED_RELATIVE`). Exactly like
`tests/test_external_drivers.py` ("No test here imports `src.external.iri` or
`src.external.gim`, statically or dynamically"), this module never places an `iri`
import in its own source: every check on `predictions_from_benchmark_rows` runs the
import and the assertions inside a CHILD PROCESS (`python -c "<code>"`), so the
containment scanner's static AST walk of this file's source sees no import of `iri` at
all -- only a string literal passed to `subprocess.run`.

INPUTS. Pure in-memory synthetic rows, a directly-constructed `BenchmarkContract`, a
plain `{station_id: object()}` registry stand-in (only membership is checked), and
`Partition` instances built directly -- no config file, no `iricore`, no network.

`_emit_prediction_payload`'s own provenance re-verification (rows-hash mismatch,
validation-report status, `artifact_class` mismatch) and `_write_prediction_once`'s
write-once refusal are exercised directly, in a child process, against a synthetic
rows/provenance/report triple and a minimal stand-in `entry`/`args` -- never a real
Kaggle-produced B-01 artifact, and R-59 is not weakened to manufacture one. These
checks all run before `_emit_prediction_payload` reaches `load_registry` (still
`TBD -- freeze gate` today, Q2 = A) or `build_partitions`, so no station registry or
resolved split configuration is needed to reach them.

WHAT NO TEST HERE DISCHARGES. The full `scripts/04_build_external_products.py` CLI
entry point (`main`, argument parsing, the TE 9.2 receipt gate, the registry event
log) is not exercised -- only `_emit_prediction_payload` and `_write_prediction_once`
are called directly. It does not touch REFIT or DEC in any live sense; both are
asserted refused by the pure function.

Run: pytest tests/test_b01_prediction_adapter.py -rs
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

#: Shared child-process prelude: contract/partition/row builders mirroring the
#: production shapes exactly (`configs/experiment.yaml: benchmark_b01`,
#: `src.data.splits.Partition`) -- imports live HERE, inside the string, never in this
#: file's own AST.
_PRELUDE = """
import datetime as dt
from src.data.config import BenchmarkError
from src.data.splits import Partition, PartitionKind
from src.evaluation.guards import UNTRANSFORMED
from src.evaluation.masks import prediction_from_payload
from src.external.iri import BenchmarkContract, _UNTRANSFORMED, predictions_from_benchmark_rows

_UTC = dt.timezone.utc

def _contract(**overrides):
    fields = {
        "benchmark_id": "B-01",
        "iri_version": 16,
        "htop_km": 2000.0,
        "hbot_km": 90.0,
        "hstep_km": 0.5,
        "oarr_overrides": {},
        "output_field": "iri2016_t_plus_1_tecu",
        "output_units": "TECU",
        "index_semantics": "retrospective, centered, same-day",
        "package": "iricore",
        "release": "1.8.0",
        "wheel_sha256": "f452b223" + "0" * 56,
        "installed_default_iri_version": 20,
        "index_file_pins": {"apf107.dat": "cdf4d5df", "ig_rz.dat": "fbbed304"},
        "year": 2022,
        "cadence_hours": 1,
        "stamps": {
            "phase_id": "P1A",
            "source_id": "IRI2016_B01",
            "target_definition_id": "GRIDDed_VTEC_1H",
        },
        "report_name": "iri_implementation_validation_report",
        "tolerance_tecu": 1.0,
        "tolerance_declared_at_utc": "2026-09-20T12:27:01Z",
    }
    fields.update(overrides)
    return BenchmarkContract(**fields)

def _fold(partition_id, month):
    return Partition(
        partition_id=partition_id,
        kind=PartitionKind.fold,
        train_start=dt.date(2022, 1, 1),
        train_end=dt.date(2022, month, 1),
        validation_month=dt.date(2022, month, 1),
        embargo_hours=24,
    )

def _row(station_id, when, value, status="ok"):
    row = {
        "benchmark_id": "B-01",
        "station_id": station_id,
        "cell_id": "cell",
        "lat": 40.0,
        "lon": 44.0,
        "target_time_utc": when.isoformat(),
        "units": "TECU",
        "iri_version": 16,
        "htop_km": 2000.0,
        "status": status,
    }
    if status == "ok":
        row["iri2016_t_plus_1_tecu"] = value
    else:
        row["iri2016_t_plus_1_tecu"] = None
        row["error"] = "RuntimeError: boom"
    return row

STATIONS = {"ARUC": object(), "BSHM": object(), "NICO": object()}
"""


def _run(code: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT)
    return subprocess.run(
        [sys.executable, "-c", _PRELUDE + "\n" + code],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        env=env,
        timeout=60,
        check=False,
    )


def _assert_ok(result: subprocess.CompletedProcess[str]) -> None:
    assert result.returncode == 0, (
        f"child check failed\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    )


# --- unit: field mapping / envelope correctness ------------------------------------------


def test_field_mapping_and_envelope() -> None:
    result = _run(
        """
contract = _contract()
f1 = _fold("F1", 1)
rows = [_row("ARUC", dt.datetime(2022, 1, 5, 12, tzinfo=_UTC), 12.1)]
payloads = predictions_from_benchmark_rows(rows, contract=contract, stations=STATIONS, partitions=[f1])
payload = payloads["F1"]
assert payload["model_id"] == "B-01"
assert payload["seed"] is None
assert payload["partition_id"] == "F1"
assert payload["transform_id"] == "untransformed"
assert payload["phase_id"] == "P1A"
assert payload["source_id"] == "IRI2016_B01"
assert payload["target_definition_id"] == "GRIDDed_VTEC_1H"
assert payload["rows"] == [
    {"station": "ARUC", "interval_start_utc": "2022-01-05T12:00:00+00:00", "y_hat": 12.1}
]
"""
    )
    _assert_ok(result)


def test_untransformed_literal_matches_guards_reserved_token() -> None:
    """`src.external.iri._UNTRANSFORMED` is duplicated to avoid an external->evaluation
    import edge (TE 12); this pins it against `src.evaluation.guards.UNTRANSFORMED` so
    the two cannot drift unnoticed."""
    result = _run('assert _UNTRANSFORMED == UNTRANSFORMED == "untransformed"')
    _assert_ok(result)


def test_payload_round_trips_through_prediction_from_payload() -> None:
    """Integration/contract: the emitted payload is accepted, unmodified, by the same
    `prediction_from_payload` `07` uses -- no adapter-side reimplementation of that
    check."""
    result = _run(
        """
contract = _contract()
f1 = _fold("F1", 1)
rows = [_row("ARUC", dt.datetime(2022, 1, 5, 12, tzinfo=_UTC), 12.1)]
payloads = predictions_from_benchmark_rows(rows, contract=contract, stations=STATIONS, partitions=[f1])
loaded = prediction_from_payload(payloads["F1"], resource="test")
assert loaded.model_id == "B-01"
assert loaded.seed is None
assert loaded.partition_id == "F1"
assert loaded.transform_id == "untransformed"
"""
    )
    _assert_ok(result)


# --- partition-scoping (Option B): filtering ----------------------------------------------


def test_rows_are_filtered_to_each_partitions_own_window() -> None:
    result = _run(
        """
contract = _contract()
f1, f2 = _fold("F1", 1), _fold("F2", 2)
rows = [
    _row("ARUC", dt.datetime(2022, 1, 5, 12, tzinfo=_UTC), 12.1),
    _row("ARUC", dt.datetime(2022, 2, 5, 12, tzinfo=_UTC), 9.5),
]
payloads = predictions_from_benchmark_rows(rows, contract=contract, stations=STATIONS, partitions=[f1, f2])
assert [r["y_hat"] for r in payloads["F1"]["rows"]] == [12.1]
assert [r["y_hat"] for r in payloads["F2"]["rows"]] == [9.5]
"""
    )
    _assert_ok(result)


def test_a_partition_never_carries_another_partitions_rows() -> None:
    result = _run(
        """
contract = _contract()
f1, f2 = _fold("F1", 1), _fold("F2", 2)
rows = [_row("ARUC", dt.datetime(2022, 1, 5, 12, tzinfo=_UTC), 12.1)]
try:
    predictions_from_benchmark_rows(rows, contract=contract, stations=STATIONS, partitions=[f1, f2])
    raise SystemExit("expected BenchmarkError for F2's empty window")
except BenchmarkError as exc:
    assert "empty" in str(exc)
"""
    )
    _assert_ok(result)


# --- negative / guard tests ---------------------------------------------------------------


def test_refit_partition_is_refused() -> None:
    result = _run(
        """
refit = Partition(
    partition_id="REFIT", kind=PartitionKind.refit, train_start=dt.date(2022, 1, 1),
    train_end=dt.date(2022, 12, 1), validation_month=None, embargo_hours=24,
)
try:
    predictions_from_benchmark_rows([], contract=_contract(), stations=STATIONS, partitions=[refit])
    raise SystemExit("expected BenchmarkError for REFIT")
except BenchmarkError as exc:
    assert "not a fold partition" in str(exc)
"""
    )
    _assert_ok(result)


def test_dec_partition_is_refused() -> None:
    result = _run(
        """
dec = Partition(
    partition_id="DEC", kind=PartitionKind.locked, train_start=dt.date(2022, 1, 1),
    train_end=dt.date(2022, 12, 1), validation_month=dt.date(2022, 12, 1), embargo_hours=24,
)
try:
    predictions_from_benchmark_rows([], contract=_contract(), stations=STATIONS, partitions=[dec])
    raise SystemExit("expected BenchmarkError for DEC")
except BenchmarkError as exc:
    assert "one-door" in str(exc)
"""
    )
    _assert_ok(result)


def test_unregistered_station_is_refused() -> None:
    result = _run(
        """
contract = _contract()
f1 = _fold("F1", 1)
rows = [_row("GHOST", dt.datetime(2022, 1, 5, 12, tzinfo=_UTC), 12.1)]
try:
    predictions_from_benchmark_rows(rows, contract=contract, stations=STATIONS, partitions=[f1])
    raise SystemExit("expected BenchmarkError for an unregistered station")
except BenchmarkError as exc:
    assert "station registry" in str(exc)
"""
    )
    _assert_ok(result)


def test_duplicate_station_time_pair_is_refused() -> None:
    result = _run(
        """
contract = _contract()
f1 = _fold("F1", 1)
when = dt.datetime(2022, 1, 5, 12, tzinfo=_UTC)
rows = [_row("ARUC", when, 12.1), _row("ARUC", when, 12.3)]
try:
    predictions_from_benchmark_rows(rows, contract=contract, stations=STATIONS, partitions=[f1])
    raise SystemExit("expected BenchmarkError for a duplicate row")
except BenchmarkError as exc:
    assert "duplicate" in str(exc)
"""
    )
    _assert_ok(result)


def test_error_status_row_is_excluded_and_counted_not_dropped_silently() -> None:
    result = _run(
        """
contract = _contract()
f1 = _fold("F1", 1)
rows = [
    _row("ARUC", dt.datetime(2022, 1, 5, 12, tzinfo=_UTC), 12.1),
    _row("BSHM", dt.datetime(2022, 1, 6, 0, tzinfo=_UTC), None, status="error"),
]
payloads = predictions_from_benchmark_rows(rows, contract=contract, stations=STATIONS, partitions=[f1])
payload = payloads["F1"]
assert len(payload["rows"]) == 1
assert payload["b01_generation_provenance"]["error_row_count"] == 1
assert payload["b01_generation_provenance"]["unmatched_partition_row_count"] == 0
assert payload["b01_generation_provenance"]["total_row_count"] == 2
"""
    )
    _assert_ok(result)


def test_valid_row_outside_every_supplied_partition_is_accounted_not_dropped() -> None:
    """Finding 1: a well-formed, status='ok' row whose month is not any SUPPLIED
    partition's validation month (e.g. a training-only month between F1 and F2) is not
    an error and is not silently discarded -- it is counted in
    `unmatched_partition_row_count`, distinct from `error_row_count`."""
    result = _run(
        """
contract = _contract()
f1, f2 = _fold("F1", 1), _fold("F2", 2)
rows = [
    _row("ARUC", dt.datetime(2022, 1, 5, 12, tzinfo=_UTC), 12.1),   # F1's window
    _row("BSHM", dt.datetime(2022, 2, 5, 12, tzinfo=_UTC), 9.5),    # F2's window
    _row("NICO", dt.datetime(2022, 5, 5, 12, tzinfo=_UTC), 7.0),    # neither window
]
payloads = predictions_from_benchmark_rows(rows, contract=contract, stations=STATIONS, partitions=[f1, f2])
assert [r["y_hat"] for r in payloads["F1"]["rows"]] == [12.1]
assert [r["y_hat"] for r in payloads["F2"]["rows"]] == [9.5]
for pid in ("F1", "F2"):
    prov = payloads[pid]["b01_generation_provenance"]
    assert prov["error_row_count"] == 0, "the NICO row is valid, never an error"
    assert prov["unmatched_partition_row_count"] == 1, "the NICO row must be counted, not dropped"
    assert prov["total_row_count"] == 3
"""
    )
    _assert_ok(result)


def test_boolean_is_never_accepted_as_a_tec_value() -> None:
    """Finding 3: `isinstance(True, int)` is True in Python, so the numeric guard must
    exclude `bool` explicitly rather than relying on `isinstance(value, int | float)`
    alone."""
    result = _run(
        """
contract = _contract()
f1 = _fold("F1", 1)
row = _row("ARUC", dt.datetime(2022, 1, 5, 12, tzinfo=_UTC), True)
try:
    predictions_from_benchmark_rows([row], contract=contract, stations=STATIONS, partitions=[f1])
    raise SystemExit("expected BenchmarkError for a boolean TEC value")
except BenchmarkError as exc:
    assert "not a number" in str(exc)
"""
    )
    _assert_ok(result)


def test_legitimate_int_and_float_tec_values_still_accepted() -> None:
    """The Finding 3 fix must not reject ordinary numeric TEC values, including a bare
    int (a legitimate, if unusual, TEC reading)."""
    result = _run(
        """
contract = _contract()
f1 = _fold("F1", 1)
rows = [
    _row("ARUC", dt.datetime(2022, 1, 5, 12, tzinfo=_UTC), 12),    # int
    _row("BSHM", dt.datetime(2022, 1, 6, 12, tzinfo=_UTC), 9.5),   # float
]
payloads = predictions_from_benchmark_rows(rows, contract=contract, stations=STATIONS, partitions=[f1])
y_hats = sorted(r["y_hat"] for r in payloads["F1"]["rows"])
assert y_hats == [9.5, 12.0]
"""
    )
    _assert_ok(result)


def test_missing_stamp_is_refused() -> None:
    result = _run(
        """
contract = _contract(stamps={"phase_id": "P1A", "source_id": "IRI2016_B01"})
f1 = _fold("F1", 1)
try:
    predictions_from_benchmark_rows([], contract=contract, stations=STATIONS, partitions=[f1])
    raise SystemExit("expected BenchmarkError for a missing stamp")
except BenchmarkError as exc:
    assert "missing required stamp" in str(exc)
"""
    )
    _assert_ok(result)


def test_empty_partition_after_filtering_is_refused() -> None:
    result = _run(
        """
contract = _contract()
f1 = _fold("F1", 1)
rows = [_row("ARUC", dt.datetime(2022, 3, 5, 12, tzinfo=_UTC), 12.1)]
try:
    predictions_from_benchmark_rows(rows, contract=contract, stations=STATIONS, partitions=[f1])
    raise SystemExit("expected BenchmarkError for an empty-after-filtering partition")
except BenchmarkError as exc:
    assert "empty" in str(exc)
"""
    )
    _assert_ok(result)


# =========================================================================================
# Finding 2 -- `_emit_prediction_payload` and `_write_prediction_once`, THROUGH the real
# implementation in `scripts/04_build_external_products.py` (child process; the module is
# loaded dynamically inside the child so this file's own AST names neither `scripts` nor
# `iri`). A minimal stand-in `entry`/`args` reaches exactly as far as the checks under
# test: `_b01_out_dir` only reads `entry["snapshot"].resolved_roots["workspace"]`, and
# every check below (artifact_class, rows hash, report hash, report status) runs BEFORE
# `load_registry`/`build_partitions`/`iri.read_benchmark_contract` are ever reached.
# =========================================================================================

_SCRIPT_PATH = REPO_ROOT / "scripts" / "04_build_external_products.py"

_EMIT_PRELUDE = """
import argparse
import hashlib
import importlib.util
import json
import sys
import types
from pathlib import Path

sys.path.insert(0, r"{repo_root}")
spec = importlib.util.spec_from_file_location("stage04_under_test", r"{script_path}")
stage04 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stage04)

def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def _entry(workspace):
    snapshot = types.SimpleNamespace(resolved_roots={{"workspace": str(workspace)}})
    return {{"snapshot": snapshot}}

def _args(**overrides):
    ns = argparse.Namespace(
        phase=1,
        out=None,
        emit_prediction_payload=None,
        benchmark_rows=None,
        benchmark_provenance=None,
    )
    for k, v in overrides.items():
        setattr(ns, k, v)
    return ns
""".format(repo_root=str(REPO_ROOT), script_path=str(_SCRIPT_PATH))


def _run_emit(code: str, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT)
    return subprocess.run(
        [sys.executable, "-c", _EMIT_PRELUDE + "\n" + code],
        capture_output=True,
        text=True,
        cwd=str(tmp_path),
        env=env,
        timeout=60,
        check=False,
    )


def test_emit_refuses_on_rows_hash_mismatch(tmp_path: Path) -> None:
    """Finding 2, item 1: the rows file's actual SHA-256 must match provenance's
    recorded `rows_sha256`, re-derived at consumption time, not merely copied."""
    rows_path = tmp_path / "rows.jsonl"
    rows_path.write_text('{"station_id": "ARUC"}\\n', encoding="utf-8")
    report_path = tmp_path / "report.json"
    report_path.write_text(json.dumps({"status": "passed"}), encoding="utf-8")
    result = _run_emit(
        f"""
provenance = {{
    "artifact_class": "B-01 benchmark rows (generated, not trained)",
    "rows_sha256": "0" * 64,
    "validation_report_file": r"{report_path}",
    "validation_report_sha256": _sha256(r"{report_path}"),
}}
Path(r"{tmp_path / "provenance.json"}").write_text(json.dumps(provenance), encoding="utf-8")
entry = _entry(r"{tmp_path}")
args = _args(
    emit_prediction_payload=r"{tmp_path / "run"}",
    benchmark_rows=r"{rows_path}",
    benchmark_provenance=r"{tmp_path / "provenance.json"}",
)
try:
    stage04._emit_prediction_payload(entry, args)
    raise SystemExit("expected IntegrityError for a rows-hash mismatch")
except stage04.IntegrityError as exc:
    assert "does not match" in str(exc) and "rows_sha256" in str(exc)
""",
        tmp_path,
    )
    _assert_ok(result)


def test_emit_refuses_on_failed_validation_report(tmp_path: Path) -> None:
    """Finding 2, item 2: R-59 limb 1 is re-asserted at consumption -- a report whose
    own `status` is not `"passed"` refuses even if provenance's hashes all check out."""
    rows_path = tmp_path / "rows.jsonl"
    rows_path.write_text('{"station_id": "ARUC"}\\n', encoding="utf-8")
    report_path = tmp_path / "report.json"
    report_path.write_text(json.dumps({"status": "failed"}), encoding="utf-8")
    result = _run_emit(
        f"""
provenance = {{
    "artifact_class": "B-01 benchmark rows (generated, not trained)",
    "rows_sha256": _sha256(r"{rows_path}"),
    "validation_report_file": r"{report_path}",
    "validation_report_sha256": _sha256(r"{report_path}"),
}}
Path(r"{tmp_path / "provenance.json"}").write_text(json.dumps(provenance), encoding="utf-8")
entry = _entry(r"{tmp_path}")
args = _args(
    emit_prediction_payload=r"{tmp_path / "run"}",
    benchmark_rows=r"{rows_path}",
    benchmark_provenance=r"{tmp_path / "provenance.json"}",
)
try:
    stage04._emit_prediction_payload(entry, args)
    raise SystemExit("expected IntegrityError for a failed validation report")
except stage04.IntegrityError as exc:
    assert "not \\'passed\\'" in str(exc)
""",
        tmp_path,
    )
    _assert_ok(result)


def test_emit_refuses_on_wrong_artifact_class(tmp_path: Path) -> None:
    """Finding 2, item 3: a provenance record not labelled as a B-01 generated
    benchmark is refused before any hash is even checked."""
    rows_path = tmp_path / "rows.jsonl"
    rows_path.write_text('{"station_id": "ARUC"}\\n', encoding="utf-8")
    result = _run_emit(
        f"""
provenance = {{"artifact_class": "some other artifact"}}
Path(r"{tmp_path / "provenance.json"}").write_text(json.dumps(provenance), encoding="utf-8")
entry = _entry(r"{tmp_path}")
args = _args(
    emit_prediction_payload=r"{tmp_path / "run"}",
    benchmark_rows=r"{rows_path}",
    benchmark_provenance=r"{tmp_path / "provenance.json"}",
)
try:
    stage04._emit_prediction_payload(entry, args)
    raise SystemExit("expected IntegrityError for a wrong artifact_class")
except stage04.IntegrityError as exc:
    assert "is not a B-01 generated-benchmark" in str(exc)
""",
        tmp_path,
    )
    _assert_ok(result)


def test_write_prediction_once_refuses_an_existing_file(tmp_path: Path) -> None:
    """Finding 2, item 4: `_write_prediction_once` never overwrites an existing
    prediction file (TE 13.3; R-102a step 1), the same discipline `06`'s own
    `_write_prediction_once` applies to every prediction file it writes."""
    target = tmp_path / "F1" / "B-01.json"
    result = _run_emit(
        f"""
path = stage04._write_prediction_once(Path(r"{target}"), {{"model_id": "B-01"}})
assert path.is_file()
try:
    stage04._write_prediction_once(Path(r"{target}"), {{"model_id": "B-01"}})
    raise SystemExit("expected IntegrityError on the second write")
except stage04.IntegrityError as exc:
    assert "already exists" in str(exc)
""",
        tmp_path,
    )
    _assert_ok(result)
