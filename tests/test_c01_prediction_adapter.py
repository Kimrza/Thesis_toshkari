"""C-01-to-`Prediction` bridge: `gim.predictions_from_comparator_rows`, and the `gim`
comparison set's per-station overlap-disclosure containment.

PURPOSE. The `gim` comparison set (D-80: `{M-06, C-01}`) needs a `06`-shaped C-01
prediction per fold partition, and none was ever produced: scientific_1month rehearsal 4
(2026-10-02) aborted in `07` with "prediction(s) missing for declared member(s)
['C-01']". `src.external.gim.predictions_from_comparator_rows` converts the verified
`gim_comparator.parquet` rows into the eight-field payload, partition-scoped exactly as
B-01's bridge (Option B, Student/Owner ruling 2026-09-26). The comparator is generated
per station against the D-73 audit with that station's own receiver-presence flag
(`gim.station_overlap_audit`), so `src.evaluation.metrics` checks containment per
station and states every station's flag in the disclosure.

IMPORT BOUNDARY (TE 12; TA-07). `src.external.gim` is importable only by
`scripts/04_build_external_products.py` and `src/evaluation/`; `tests/*` is not
allowlisted. As in `tests/test_b01_prediction_adapter.py`, every check that touches
`gim` runs inside a CHILD PROCESS, so this file's own AST carries no `gim` import.

INPUTS. Synthetic in-memory rows, a synthetic overlap audit shaped like
`evidence/r60_gim_gate_inputs/R60_overlap_audit_result_2026-09-26.json`, and directly
constructed `Partition`s. No config, no IONEX file, no network.

Re-run behaviour: pure; every run builds the same synthetic inputs.

Run: pytest tests/test_c01_prediction_adapter.py -rs
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

_PRELUDE = """
import datetime as dt
from src.data.config import ComparatorError, FairnessError
from src.data.splits import Partition, PartitionKind
from src.evaluation.guards import UNTRANSFORMED
from src.evaluation.masks import prediction_from_payload
from src.evaluation import metrics
from src.external.gim import (
    C01_MODEL_ID,
    _UNTRANSFORMED,
    overlap_audit_content_hash,
    predictions_from_comparator_rows,
    station_overlap_audit,
)

_UTC = dt.timezone.utc
STATIONS = ["ARUC", "BSHM", "NICO"]
STAMPS = {"phase_id": "P1A", "source_id": "gim_comparator_C-01_2022",
          "target_definition_id": "GRIDDed_VTEC_1H"}
AUDIT = {
    "audit_id": "gim-overlap-audit-test",
    "gim_network_overlap_flag": True,
    "recorded_at_utc": "2026-09-26T14:47:22+00:00",
    "per_station": {
        "ARUC": {"code": "aruc", "present_in_network": False},
        "BSHM": {"code": "bshm", "present_in_network": True},
        "NICO": {"code": "nico", "present_in_network": True},
    },
}

def _fold(partition_id, month, kind=PartitionKind.fold):
    return Partition(
        partition_id=partition_id,
        kind=kind,
        train_start=dt.date(2022, 1, 1),
        train_end=dt.date(2022, month, 1),
        validation_month=dt.date(2022, month, 1) if kind is not PartitionKind.refit else None,
        embargo_hours=24,
    )

def _row(station, when, value, audit=AUDIT):
    effective = station_overlap_audit(audit, station)
    return {
        "station": station,
        "target_epoch_utc": when.isoformat(),
        "value_tecu": value,
        "rule": "C",
        "gim_network_overlap_flag": effective["gim_network_overlap_flag"],
        "overlap_audit_id": effective["audit_id"],
        "overlap_audit_sha256": overlap_audit_content_hash(effective),
        "phase_id": "P1",
    }

def _rows(month=3, day=5):
    return [_row(s, dt.datetime(2022, month, day, h, tzinfo=_UTC), 10.0 + h)
            for s in STATIONS for h in range(3)]

def _refuses(fn, error, fragment):
    try:
        fn()
    except error as exc:
        assert fragment in str(exc), str(exc)
    else:
        raise AssertionError("expected a refusal")
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
        timeout=120,
        check=False,
    )


def _assert_ok(result: subprocess.CompletedProcess[str]) -> None:
    assert result.returncode == 0, f"child check failed\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"


def test_envelope_and_round_trip_through_prediction_from_payload() -> None:
    _assert_ok(
        _run(
            """
payloads = predictions_from_comparator_rows(_rows(), stamps=STAMPS, stations=STATIONS,
                                            partitions=[_fold("F1", 3)])
p = payloads["F1"]
assert p["model_id"] == C01_MODEL_ID == "C-01" and p["seed"] is None
assert p["transform_id"] == "untransformed" and p["confirmatory"] is False
assert (p["phase_id"], p["source_id"], p["target_definition_id"]) == (
    "P1A", "gim_comparator_C-01_2022", "GRIDDed_VTEC_1H")
assert len(p["rows"]) == 9 and set(p["rows"][0]) == {"station", "interval_start_utc", "y_hat"}
prov = p["c01_generation_provenance"]
assert prov["per_station"]["ARUC"]["gim_network_overlap_flag"] is False
assert prov["per_station"]["BSHM"]["gim_network_overlap_flag"] is True
loaded = prediction_from_payload(p, resource="test")
assert loaded.model_id == "C-01" and loaded.seed is None
assert loaded.frame.attrs["c01_generation_provenance"] == prov
"""
        )
    )


def test_untransformed_literal_matches_guards_reserved_token() -> None:
    _assert_ok(_run('assert _UNTRANSFORMED == UNTRANSFORMED == "untransformed"'))


def test_rows_are_scoped_to_each_partition_and_out_of_window_rows_are_counted() -> None:
    _assert_ok(
        _run(
            """
rows = _rows(month=3) + _rows(month=4) + _rows(month=2)
payloads = predictions_from_comparator_rows(rows, stamps=STAMPS, stations=STATIONS,
                                            partitions=[_fold("F1", 3), _fold("F2", 4)])
assert all(r["interval_start_utc"].startswith("2022-03") for r in payloads["F1"]["rows"])
assert all(r["interval_start_utc"].startswith("2022-04") for r in payloads["F2"]["rows"])
prov = payloads["F1"]["c01_generation_provenance"]
assert prov["unmatched_partition_row_count"] == 9 and prov["total_row_count"] == 27
"""
        )
    )


def test_refit_and_dec_partitions_are_refused() -> None:
    _assert_ok(
        _run(
            """
_refuses(lambda: predictions_from_comparator_rows(
    _rows(), stamps=STAMPS, stations=STATIONS,
    partitions=[_fold("REFIT", 11, PartitionKind.refit)]), ComparatorError, "not a fold")
_refuses(lambda: predictions_from_comparator_rows(
    _rows(), stamps=STAMPS, stations=STATIONS,
    partitions=[_fold("DEC", 12, PartitionKind.locked)]), ComparatorError, "not a fold")
"""
        )
    )


def test_integrity_refusals() -> None:
    _assert_ok(
        _run(
            """
f1 = [_fold("F1", 3)]
_refuses(lambda: predictions_from_comparator_rows(_rows(), stamps={**STAMPS, "source_id": ""},
         stations=STATIONS, partitions=f1), ComparatorError, "source_id")
_refuses(lambda: predictions_from_comparator_rows(_rows(), stamps=STAMPS,
         stations=["ARUC", "BSHM"], partitions=f1), ComparatorError, "station registry")
rows = _rows(); rows.append(dict(rows[0]))
_refuses(lambda: predictions_from_comparator_rows(rows, stamps=STAMPS, stations=STATIONS,
         partitions=f1), ComparatorError, "duplicate")
for bad in (float("nan"), True, None):
    rows = _rows(); rows[0] = {**rows[0], "value_tecu": bad}
    _refuses(lambda: predictions_from_comparator_rows(rows, stamps=STAMPS, stations=STATIONS,
             partitions=f1), ComparatorError, "finite number")
rows = _rows(); rows[0] = {**rows[0], "overlap_audit_sha256": ""}
_refuses(lambda: predictions_from_comparator_rows(rows, stamps=STAMPS, stations=STATIONS,
         partitions=f1), ComparatorError, "containment")
rows = _rows(); rows[1] = {**rows[1], "overlap_audit_sha256": "0" * 64}
_refuses(lambda: predictions_from_comparator_rows(rows, stamps=STAMPS, stations=STATIONS,
         partitions=f1), ComparatorError, "more than one overlap provenance")
rows = _rows(); rows[0] = {**rows[0], "target_epoch_utc": "2022-03-05T00:00:00"}
_refuses(lambda: predictions_from_comparator_rows(rows, stamps=STAMPS, stations=STATIONS,
         partitions=f1), ComparatorError, "timezone")
_refuses(lambda: predictions_from_comparator_rows(_rows(month=3), stamps=STAMPS,
         stations=STATIONS, partitions=[_fold("F2", 4)]), ComparatorError, "empty")
"""
        )
    )


def test_station_overlap_audit_uses_each_stations_own_presence() -> None:
    _assert_ok(
        _run(
            """
assert station_overlap_audit(AUDIT, "ARUC")["gim_network_overlap_flag"] is False
assert station_overlap_audit(AUDIT, "NICO")["gim_network_overlap_flag"] is True
assert station_overlap_audit(AUDIT, "ZZZZ") == AUDIT  # no per-station record: unchanged
assert AUDIT["gim_network_overlap_flag"] is True      # the input is never mutated
"""
        )
    )


def test_disclosure_checks_containment_per_station_and_states_every_flag() -> None:
    _assert_ok(
        _run(
            """
p = predictions_from_comparator_rows(_rows(), stamps=STAMPS, stations=STATIONS,
                                     partitions=[_fold("F1", 3)])["F1"]
block = metrics._gim_disclosure_block(
    overlap_audit=AUDIT, comparator_provenance=p["c01_generation_provenance"], set_id="gim")
assert block["gim_network_overlap_flag"] is True
assert block["per_station_gim_network_overlap_flag"] == {"ARUC": False, "BSHM": True, "NICO": True}
assert block["overlap_audit_id"] == "gim-overlap-audit-test" and block["overlap_audit_sha256"]
"""
        )
    )


def test_disclosure_refuses_a_comparator_generated_against_another_audit() -> None:
    """Negative control: an audit registered after generation (different content) cannot
    appear in the comparator's provenance, so the per-station containment check fails."""
    _assert_ok(
        _run(
            """
p = predictions_from_comparator_rows(_rows(), stamps=STAMPS, stations=STATIONS,
                                     partitions=[_fold("F1", 3)])["F1"]
later = {**AUDIT, "recorded_at_utc": "2026-10-01T00:00:00+00:00"}
_refuses(lambda: metrics._gim_disclosure_block(
    overlap_audit=later, comparator_provenance=p["c01_generation_provenance"], set_id="gim"),
    FairnessError, "does not match")
flipped = {**AUDIT, "per_station": {**AUDIT["per_station"],
           "ARUC": {"code": "aruc", "present_in_network": True}}}
_refuses(lambda: metrics._gim_disclosure_block(
    overlap_audit=flipped, comparator_provenance=p["c01_generation_provenance"], set_id="gim"),
    FairnessError, "ARUC")
_refuses(lambda: metrics._gim_disclosure_block(
    overlap_audit=None, comparator_provenance=p["c01_generation_provenance"], set_id="gim"),
    FairnessError, "no registered overlap-audit")
"""
        )
    )
