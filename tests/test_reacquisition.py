"""DATA-07 re-acquisition read path and downloader helpers (no network).

Purpose: negative controls for `src/data/reacquisition.py` (verify, parse, cell selection,
DATA-07 comparison) and the pure helpers of `scripts/acquire_madrigal_reacquisition_2022.py`
(filters, body completeness, recorded-file plan). Inputs: synthetic files under `tmp_path`.
Re-run behaviour: pure.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest
from src.data.config import IntegrityError
from src.data.reacquisition import (
    compare_with_prior_records,
    parse_isprint,
    select_cell_records,
    verify_reacquisition,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DAY = dt.date(2022, 3, 1)
T0 = int(dt.datetime(2022, 3, 1, tzinfo=dt.timezone.utc).timestamp())
CELLS = {"ARUC": (40, 44), "BSHM": (32, 35), "NICO": (35, 33)}
BODY = (
    f"{T0}.000       32.00      35.00   5.19080e+00   1.31143e+00\n"
    f"{T0}.000       40.00      44.00   6.00000e+00   5.00000e-01\n"
    f"{T0}.000       33.00      35.00   7.00000e+00   5.00000e-01\n"
)


def _script():
    spec = importlib.util.spec_from_file_location(
        "acq", REPO_ROOT / "scripts" / "acquire_madrigal_reacquisition_2022.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _evidence(tmp_path: Path, body: str = BODY) -> Path:
    root = tmp_path / "madrigal_reacquisition_2022"
    (root / "raw").mkdir(parents=True)
    logical = "2022-03-01__gps220301g.002.hdf5.isprint.txt"
    (root / "raw" / logical).write_bytes(body.encode("utf-8"))
    digest = hashlib.sha256(body.encode()).hexdigest()
    (root / "day_records.jsonl").write_text(
        json.dumps({"date": "2022-03-01", "status": "complete", "logical_name": logical,
                    "sha256": digest, "provider_filename": "/x/gps220301g.002.hdf5",
                    "retrieval_date": "2026-10-02"}) + "\n",
        encoding="utf-8",
    )
    (root / "request_manifest.json").write_text(json.dumps({"window": ["2022-03-01", "2022-03-01"]}), encoding="utf-8")
    manifest = {f"raw/{logical}": digest}
    for name in ("day_records.jsonl", "request_manifest.json"):
        manifest[name] = hashlib.sha256((root / name).read_bytes()).hexdigest()
    (root / "sha256_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return root


def test_verify_parse_and_select(tmp_path):
    root = _evidence(tmp_path)
    evidence = verify_reacquisition(root)
    assert set(evidence["complete"]) == {"2022-03-01"} and evidence["not_complete"] == []
    rows = parse_isprint((root / "raw" / evidence["complete"]["2022-03-01"]["logical_name"]).read_text())
    kept, outside = select_cell_records(rows, CELLS)
    assert [r["station"] for r in kept] == ["BSHM", "ARUC"] and outside == 1
    assert kept[0]["tec"] == "5.19080e+00" and kept[0]["date"] == "2022-03-01"


def test_verify_refuses_a_tampered_response(tmp_path):
    root = _evidence(tmp_path)
    raw = next((root / "raw").iterdir())
    raw.write_bytes(BODY.replace("5.19080e+00", "5.19081e+00").encode("utf-8"))
    with pytest.raises(IntegrityError, match="hashes to"):
        verify_reacquisition(root)


def test_parse_refuses_a_malformed_line():
    with pytest.raises(IntegrityError, match="5 columns"):
        parse_isprint(f"{T0}.000 32.00 35.00 5.0\n")
    with pytest.raises(ValueError):
        parse_isprint(f"{T0}.000 32.00 35.00 5.0 nan-ish\n")


def test_comparison_counts_equal_different_and_unmatched(tmp_path):
    month = tmp_path / "audit_evidence_2022-03"
    month.mkdir()
    (month / "madrigal_coverage_raw_records.csv").write_text(
        "ut1_unix,gdlat,glon,tec,dtec,station,experiment_id,file,timestamp_utc,year,date,month,hour\n"
        f"{T0}.0,32.0,35.0,5.1908,1.31143,BSHM,1,f,x,2022,2022-03-01,3,x\n"
        f"{T0}.0,40.0,44.0,6.5,0.5,ARUC,1,f,x,2022,2022-03-01,3,x\n"
        f"{T0 + 300}.0,35.0,33.0,4.0,0.5,NICO,1,f,x,2022,2022-03-01,3,x\n",
        encoding="utf-8",
    )
    kept, _ = select_cell_records(parse_isprint(BODY), CELLS)
    report = compare_with_prior_records(kept, tmp_path, window=(DAY, DAY))
    assert (report["equal"], report["different"], report["only_prior"], report["only_reacquired"]) == (1, 1, 1, 0)


def test_downloader_filters_and_body_completeness():
    acq = _script()
    filters = acq.isprint_filters(DAY, {"lat_min": 32, "lat_max": 41, "lon_min": 33, "lon_max": 45})
    assert filters.startswith("date1=03/01/2022 time1=00:00:00 date2=03/01/2022 time2=23:59:59")
    assert acq.check_isprint_body(BODY.encode(), DAY) == {"complete": True, "rows": 3}
    late = f"{T0 + 86400}.000 32.00 35.00 5.0 1.0\n".encode()
    assert acq.check_isprint_body(late, DAY)["complete"] is False
    assert acq.check_isprint_body(b"<html>error</html>", DAY)["complete"] is False


def test_downloader_plans_exactly_the_recorded_files():
    acq = _script()
    plan = acq.recorded_files_by_day(REPO_ROOT / "evidence")
    assert len(plan) == 334 and min(plan) == "2022-01-01" and max(plan) == "2022-11-30"
    assert sum(1 for e in plan.values() if e["file"].endswith("g.001.hdf5")) == 9


def test_downloader_refuses_without_identity(monkeypatch):
    acq = _script()
    for name in acq.IDENTITY_VARIABLES:
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(IntegrityError, match="not set"):
        acq._identity()
