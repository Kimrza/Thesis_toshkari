"""scripts/04 resolve_b01_receipt (closure 2026-10-01; D-83 A8 item 12).

The superseded legacy November receipt is never consumed by default; the W-2 receipt whose
months cover the fixture is. Inputs: empty files under tmp_path. Re-run: pure.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def _mod():
    spec = importlib.util.spec_from_file_location(
        "s04_resolver", REPO_ROOT / "scripts" / "04_build_external_products.py"
    )
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _touch(d: Path, *names: str) -> None:
    for n in names:
        (d / n).write_text("", encoding="utf-8")


def test_legacy_receipt_alone_is_refused_not_consumed(tmp_path: Path) -> None:
    m = _mod()
    _touch(tmp_path, "b01_iri2016_rows_partial.jsonl", "b01_provenance.json")
    with pytest.raises(m.IntegrityError, match="superseded"):
        m.resolve_b01_receipt(tmp_path, rows=None, provenance=None, months=[11])


def test_covering_w2_receipt_is_selected_with_its_own_provenance(tmp_path: Path) -> None:
    m = _mod()
    _touch(tmp_path, "b01_iri2016_rows_partial.jsonl", "b01_iri2016_rows_P1A_m03_11.jsonl")
    rows, prov = m.resolve_b01_receipt(tmp_path, rows=None, provenance=None, months=[3])
    assert rows.name == "b01_iri2016_rows_P1A_m03_11.jsonl"
    assert prov.name == "b01_provenance_P1A_m03_11.json"


def test_receipt_not_covering_the_months_is_refused(tmp_path: Path) -> None:
    m = _mod()
    _touch(tmp_path, "b01_iri2016_rows_P1A_m03_11.jsonl")
    with pytest.raises(m.IntegrityError, match="covers months"):
        m.resolve_b01_receipt(tmp_path, rows=None, provenance=None, months=[7])


def test_two_covering_receipts_are_ambiguous(tmp_path: Path) -> None:
    m = _mod()
    _touch(tmp_path, "b01_iri2016_rows_P1A_m11.jsonl", "b01_iri2016_rows_P1A_m03_11.jsonl")
    with pytest.raises(m.IntegrityError, match="more than one"):
        m.resolve_b01_receipt(tmp_path, rows=None, provenance=None, months=[11])


def test_explicit_rows_win(tmp_path: Path) -> None:
    m = _mod()
    rows, prov = m.resolve_b01_receipt(
        tmp_path, rows=tmp_path / "b01_iri2016_rows_partial.jsonl", provenance=None, months=[11]
    )
    assert rows.name == "b01_iri2016_rows_partial.jsonl" and prov.name == "b01_provenance.json"


def test_month_range_tag_covers_inner_months(tmp_path: Path) -> None:
    m = _mod()
    _touch(tmp_path, "b01_iri2016_rows_P1A_m01-11.jsonl")
    rows, _ = m.resolve_b01_receipt(tmp_path, rows=None, provenance=None, months=[3, 11])
    assert rows.name == "b01_iri2016_rows_P1A_m01-11.jsonl"


def _write(p: Path, text: str) -> str:
    import hashlib

    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_validation_report_recorded_path_is_used_when_its_hash_matches(tmp_path: Path) -> None:
    m = _mod()
    sha = _write(tmp_path / "iri_implementation_validation_report.json", "legacy")
    assert m.locate_validation_report(
        tmp_path, tmp_path / "iri_implementation_validation_report.json", sha
    ).name == "iri_implementation_validation_report.json"


def test_validation_report_is_found_by_hash_in_the_transfer_record(tmp_path: Path) -> None:
    m = _mod()
    _write(tmp_path / "iri_implementation_validation_report.json", "legacy")
    sha = _write(tmp_path / "transfer_20261001" / "iri_implementation_validation_report.json", "new")
    found = m.locate_validation_report(
        tmp_path, tmp_path / "iri_implementation_validation_report.json", sha
    )
    assert found.parent.name == "transfer_20261001"


def test_validation_report_with_no_matching_hash_refuses(tmp_path: Path) -> None:
    m = _mod()
    _write(tmp_path / "iri_implementation_validation_report.json", "legacy")
    with pytest.raises(m.IntegrityError, match="not found"):
        m.locate_validation_report(
            tmp_path, tmp_path / "iri_implementation_validation_report.json", "0" * 64
        )
