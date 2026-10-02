"""B-01 cross-environment handoff (src/data/b01_handoff.py): every refusal has a negative control.

PURPOSE. The (b) `b01_iri` -> (a) `tec-thesis-311` handoff of the January-November IRI-2016
benchmark. Two halves:

* `require_cross_environment_receipts`, which is GATED on a D-number. It refuses with no
  authorizing decision, from a caller outside (b), for a receipt written outside (a), and when
  the code commit, config hashes or platform differ. It passes only when all of those hold.
* `admit_jan_nov_receipt`, which is ungated and additive. It refuses a missing or corrupt
  artifact, the wrong generating or admitting environment, a wrong commit or config, an edited
  lock, incomplete coverage, a duplicate timestamp, an invalid value, the wrong months or
  phase, a mismatched error count, and a second admission. It records error rows as
  completeness, and identical rows yield identical hashes.

Synthetic trees only (tmp_path); nothing reads the real workspace.

INPUTS. `tests/test_clean_run.py`'s synthetic manifest, lock and registry builders.

RE-RUN. Pure: every test builds its own tmp tree.
"""

from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
for p in (REPO_ROOT, REPO_ROOT / "tests"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from src.data import b01_handoff as h  # noqa: E402
from src.data.config import IntegrityError, environment_lock_hash  # noqa: E402
from src.data.fixture_gate import (  # noqa: E402
    fixture_input_version_tag,
    lock_items,
    receipt_path_for,
    write_fixture_pass_receipt,
)
from src.data.fixture_manifest import PLUMBING_FIXTURE_ID, SCIENTIFIC_FIXTURE_ID  # noqa: E402
from src.data.release import sha256_of_file  # noqa: E402

from test_clean_run import FROZEN, RUN_ID, _lock, _registry_template, write_and_load  # noqa: E402

pytest.importorskip("yaml")

A, B = h.ADMITTING_ENVIRONMENT_ID, h.GENERATING_ENVIRONMENT_ID
PHASE = "P1A"
FIELD = "vtec_tecu"


def _snapshot(ws: Path) -> SimpleNamespace:
    return SimpleNamespace(
        platform="local",
        resolved_roots={"workspace": ws, "artifacts": ws / "artifacts"},
    )


def _decisions(ws: Path, *, marker: bool) -> Path:
    path = ws / "evidence" / "DECISIONS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    body = f"\n{h.CROSS_ENVIRONMENT_RECEIPT_MARKER}\n" if marker else "\nunrelated\n"
    path.write_text(f"## D-1 — earlier\n\ntext\n\n## D-91 — handoff\n{body}", encoding="utf-8")
    return path


def _receipts(ws: Path, *, receipt_env: str = A, **lock_overrides: Any) -> None:
    """Both fixture receipts written in `receipt_env`, at the canonical workspace paths."""
    snap = _snapshot(ws)
    registry = ws / "artifacts" / "registry" / "experiment_registry.jsonl"
    access = ws / "artifacts" / "registry" / "access_log.jsonl"
    plumbing_payload = None
    for fid in (PLUMBING_FIXTURE_ID, SCIENTIFIC_FIXTURE_ID):
        manifest = write_and_load(ws / "tests" / "fixtures", fid, status=FROZEN)
        lock = _lock(
            input_versions=[fixture_input_version_tag(fid, manifest.sha256)],
            environment_id=receipt_env,
            **lock_overrides,
        )
        target = receipt_path_for(ws, fid)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = write_fixture_pass_receipt(
            manifest=manifest,
            result="PASS",
            run_id=RUN_ID,
            lock=lock,
            snapshot=snap,
            registry_path=registry,
            access_log_path=access,
            receipt_path=target,
            registry_row=_registry_template(),
            phase=1,
            plumbing_receipt=plumbing_payload,
        )
        plumbing_payload = payload


def _b_lock(**overrides: Any):
    fields = dict(environment_id=B, pip_freeze="iricore==1.8.0", requirements_hash="b" * 64)
    fields.update(overrides)
    return _lock(**fields)


# --- half 1: cross-environment receipts (gated) --------------------------------------------


def test_cross_binding_refuses_without_an_authorizing_decision(tmp_path):
    _receipts(tmp_path)
    with pytest.raises(IntegrityError, match="governed act"):
        h.require_cross_environment_receipts(
            _snapshot(tmp_path), _b_lock(), decisions_path=_decisions(tmp_path, marker=False)
        )


def test_cross_binding_refuses_a_missing_register(tmp_path):
    with pytest.raises(IntegrityError, match="decision register"):
        h.find_authorizing_decision(tmp_path / "nope.md")


def test_cross_binding_passes_under_decision_with_equal_code_configs_platform(tmp_path):
    _receipts(tmp_path)
    out = h.require_cross_environment_receipts(
        _snapshot(tmp_path), _b_lock(), decisions_path=_decisions(tmp_path, marker=True)
    )
    assert out["decision"] == "D-91" and out["cross_environment"] is True
    assert out["caller_environment_id"] == B and out["receipt_environment_id"] == A
    assert set(out["receipts"]) == {PLUMBING_FIXTURE_ID, SCIENTIFIC_FIXTURE_ID}


def test_cross_binding_refuses_a_caller_outside_b(tmp_path):
    _receipts(tmp_path)
    with pytest.raises(IntegrityError, match="only for a B-01 generation"):
        h.require_cross_environment_receipts(
            _snapshot(tmp_path),
            _b_lock(environment_id="g07-clean-run"),
            decisions_path=_decisions(tmp_path, marker=True),
        )


def test_cross_binding_refuses_a_receipt_written_outside_a(tmp_path):
    _receipts(tmp_path, receipt_env="g07-clean-run")
    with pytest.raises(IntegrityError, match="was written in"):
        h.require_cross_environment_receipts(
            _snapshot(tmp_path), _b_lock(), decisions_path=_decisions(tmp_path, marker=True)
        )


@pytest.mark.parametrize(
    "override",
    [
        {"code_commit": "e" * 40},
        {"config_hashes": {"data.yaml": "f" * 64}},
        {"platform": "kaggle"},
    ],
)
def test_cross_binding_refuses_wrong_commit_config_or_platform(tmp_path, override):
    _receipts(tmp_path)
    with pytest.raises(IntegrityError, match="differs between"):
        h.require_cross_environment_receipts(
            _snapshot(tmp_path),
            _b_lock(**override),
            decisions_path=_decisions(tmp_path, marker=True),
        )


def test_cross_binding_refuses_missing_receipts(tmp_path):
    with pytest.raises(IntegrityError, match="receipt"):
        h.require_cross_environment_receipts(
            _snapshot(tmp_path), _b_lock(), decisions_path=_decisions(tmp_path, marker=True)
        )


def test_cross_binding_refuses_an_edited_receipt(tmp_path):
    _receipts(tmp_path)
    path = receipt_path_for(tmp_path, PLUMBING_FIXTURE_ID)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["environment_lock"]["pip_freeze"] = "tampered==1"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(IntegrityError, match="edited|hash"):
        h.require_cross_environment_receipts(
            _snapshot(tmp_path), _b_lock(), decisions_path=_decisions(tmp_path, marker=True)
        )


# --- half 2: admission in (a) ---------------------------------------------------------------


def _grid(n_hours: int = 6) -> list[tuple[str, str]]:
    return [
        (st, f"2022-01-01T{hour:02d}:00:00+00:00")
        for st in ("ARUC", "BSHM")
        for hour in range(n_hours)
    ]


def _rows(keys, *, value: float = 12.5) -> list[dict[str, Any]]:
    return [
        {"phase_id": PHASE, "station_id": st, "target_time_utc": t, FIELD: value, "status": "ok"}
        for st, t in keys
    ]


def _write_half(out: Path, rows, *, gen_lock=None, **prov_overrides: Any) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    gen_lock = gen_lock or _b_lock()
    rows_path = out / f"b01_iri2016_rows_{PHASE}_m01-11.jsonl"
    rows_path.write_text(
        "".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8", newline="\n"
    )
    prov = {
        "rows_file": rows_path.name,
        "rows_sha256": sha256_of_file(rows_path),
        "months": h.JAN_NOV,
        "phase_id": PHASE,
        "error_rows": sum(1 for r in rows if r["status"] == "error"),
        "environment_lock": lock_items(gen_lock),
        "environment_lock_hash": environment_lock_hash(gen_lock),
        "data_yaml_sans_gates_sha256": "s" * 64,
    }
    prov.update(prov_overrides)
    prov_path = out / f"b01_provenance_{PHASE}_m01-11.json"
    prov_path.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    (out / f"b01_sha256_manifest_{PHASE}_m01-11.json").write_text(
        json.dumps(
            {rows_path.name: sha256_of_file(rows_path), prov_path.name: sha256_of_file(prov_path)}
        ),
        encoding="utf-8",
    )
    return prov_path


def _admit(ws: Path, prov: Path, *, lock=None, keys=None, sans: str = "s" * 64):
    return h.admit_jan_nov_receipt(
        prov,
        snapshot=_snapshot(ws),
        lock=lock or _lock(environment_id=A),
        phase_id=PHASE,
        expected_keys=keys if keys is not None else _grid(),
        output_field=FIELD,
        data_yaml_sans_gates_sha256=sans,
    )


def test_admission_passes_and_records_both_environments(tmp_path):
    prov = _write_half(tmp_path / "b01", _rows(_grid()))
    out = _admit(tmp_path, prov)
    marker = json.loads(out["jan_nov_marker"].read_text(encoding="utf-8"))
    assert marker["generating_environment_id"] == B and marker["admitting_environment_id"] == A
    assert out["rows"] == 12 and out["error_rows"] == 0
    assert (
        h.require_jan_nov_admission(tmp_path, PHASE, prov_path=prov)["rows_sha256"]
        == marker["rows_sha256"]
    )


def test_admission_is_once_only(tmp_path):
    prov = _write_half(tmp_path / "b01", _rows(_grid()))
    _admit(tmp_path, prov)
    with pytest.raises(IntegrityError, match="already admitted"):
        _admit(tmp_path, prov)


def test_admission_refuses_missing_provenance(tmp_path):
    with pytest.raises(IntegrityError, match="missing"):
        _admit(tmp_path, tmp_path / "b01" / "absent.json")


@pytest.mark.parametrize("victim", ["rows", "manifest"])
def test_admission_refuses_missing_rows_or_manifest(tmp_path, victim):
    prov = _write_half(tmp_path / "b01", _rows(_grid()))
    name = "b01_iri2016_rows_" if victim == "rows" else "b01_sha256_manifest_"
    next(p for p in prov.parent.iterdir() if p.name.startswith(name)).unlink()
    with pytest.raises(IntegrityError, match="missing"):
        _admit(tmp_path, prov)


def test_admission_refuses_corrupt_rows(tmp_path):
    prov = _write_half(tmp_path / "b01", _rows(_grid()))
    rows = next(prov.parent.glob("b01_iri2016_rows_*"))
    rows.write_text(rows.read_text(encoding="utf-8").replace("12.5", "99.5", 1), encoding="utf-8")
    with pytest.raises(IntegrityError, match="corrupt"):
        _admit(tmp_path, prov)


def test_admission_refuses_corrupt_provenance_against_manifest(tmp_path):
    prov = _write_half(tmp_path / "b01", _rows(_grid()))
    payload = json.loads(prov.read_text(encoding="utf-8"))
    payload["note"] = "edited after transfer"
    prov.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(IntegrityError, match="manifest disagrees"):
        _admit(tmp_path, prov)


def test_admission_refuses_wrong_generating_environment(tmp_path):
    prov = _write_half(tmp_path / "b01", _rows(_grid()), gen_lock=_b_lock(environment_id=A))
    with pytest.raises(IntegrityError, match="generated in"):
        _admit(tmp_path, prov)


def test_admission_refuses_wrong_admitting_environment(tmp_path):
    prov = _write_half(tmp_path / "b01", _rows(_grid()))
    with pytest.raises(IntegrityError, match="admission runs in"):
        _admit(tmp_path, prov, lock=_lock(environment_id=B))


def test_admission_refuses_an_edited_generating_lock(tmp_path):
    lock = _b_lock()
    items = lock_items(lock)
    items["pip_freeze"] = "forged==1"
    prov = _write_half(tmp_path / "b01", _rows(_grid()), environment_lock=items)
    with pytest.raises(IntegrityError, match="edited"):
        _admit(tmp_path, prov)


def test_admission_refuses_wrong_commit(tmp_path):
    prov = _write_half(tmp_path / "b01", _rows(_grid()), gen_lock=_b_lock(code_commit="e" * 40))
    with pytest.raises(IntegrityError, match="generated at code"):
        _admit(tmp_path, prov)


def test_admission_refuses_a_non_data_config_difference(tmp_path):
    gen = _b_lock(config_hashes={"data.yaml": "d" * 64, "features.yaml": "1" * 64})
    prov = _write_half(tmp_path / "b01", _rows(_grid()), gen_lock=gen)
    admit = _lock(
        environment_id=A, config_hashes={"data.yaml": "d" * 64, "features.yaml": "2" * 64}
    )
    with pytest.raises(IntegrityError, match="other than data.yaml"):
        _admit(tmp_path, prov, lock=admit)


def test_admission_allows_only_a_gates_difference_in_data_yaml(tmp_path):
    prov = _write_half(tmp_path / "b01", _rows(_grid()))
    signed = _lock(environment_id=A, config_hashes={"data.yaml": "9" * 64})
    with pytest.raises(IntegrityError, match="outside the `gates` node"):
        _admit(tmp_path, prov, lock=signed, sans="x" * 64)
    assert _admit(tmp_path, prov, lock=signed)["rows"] == 12  # same sans-gates digest


def test_admission_refuses_incomplete_coverage(tmp_path):
    keys = _grid()
    prov = _write_half(tmp_path / "b01", _rows(keys[:-1]))
    with pytest.raises(IntegrityError, match="1 missing"):
        _admit(tmp_path, prov, keys=keys)


def test_admission_refuses_unexpected_rows(tmp_path):
    keys = _grid()
    prov = _write_half(tmp_path / "b01", _rows(keys + [("NICO", "2022-01-01T00:00:00+00:00")]))
    with pytest.raises(IntegrityError, match="1 unexpected"):
        _admit(tmp_path, prov, keys=keys)


def test_admission_refuses_duplicate_timestamps(tmp_path):
    keys = _grid()
    prov = _write_half(tmp_path / "b01", _rows(keys + [keys[0]]))
    with pytest.raises(IntegrityError, match="duplicate"):
        _admit(tmp_path, prov, keys=keys)


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -0.1, "12.5", None, True])
def test_admission_refuses_invalid_values(tmp_path, bad):
    rows = _rows(_grid())
    rows[3][FIELD] = bad
    prov = _write_half(tmp_path / "b01", rows)
    with pytest.raises(IntegrityError, match="not a"):
        _admit(tmp_path, prov)


def test_admission_refuses_unknown_status_and_valued_error_row(tmp_path):
    rows = _rows(_grid())
    rows[0]["status"] = "maybe"
    with pytest.raises(IntegrityError, match="neither"):
        _admit(tmp_path, _write_half(tmp_path / "b1", rows))
    rows = _rows(_grid())
    rows[0]["status"] = "error"
    with pytest.raises(IntegrityError, match="error row carrying a value"):
        _admit(tmp_path, _write_half(tmp_path / "b2", rows, error_rows=1))


def test_admission_records_error_rows_as_completeness_not_failure(tmp_path):
    rows = _rows(_grid())
    rows[0].update({"status": "error", FIELD: None, "error": "RuntimeError: x"})
    out = _admit(tmp_path, _write_half(tmp_path / "b01", rows))
    assert out["error_rows"] == 1 and out["ok_rows"] == 11


def test_admission_refuses_an_error_count_disagreeing_with_provenance(tmp_path):
    rows = _rows(_grid())
    rows[0].update({"status": "error", FIELD: None})
    with pytest.raises(IntegrityError, match="error rows"):
        _admit(tmp_path, _write_half(tmp_path / "b01", rows, error_rows=0))


@pytest.mark.parametrize("override", [{"months": [12]}, {"months": [1, 2]}, {"phase_id": "P2A"}])
def test_admission_refuses_wrong_months_or_phase(tmp_path, override):
    with pytest.raises(IntegrityError):
        _admit(tmp_path, _write_half(tmp_path / "b01", _rows(_grid()), **override))


def test_admission_refuses_a_row_from_another_phase(tmp_path):
    rows = _rows(_grid())
    rows[5]["phase_id"] = "P2A"
    with pytest.raises(IntegrityError, match="phase_id"):
        _admit(tmp_path, _write_half(tmp_path / "b01", rows))


def test_assembly_binding_refuses_a_substituted_half(tmp_path):
    prov = _write_half(tmp_path / "b01", _rows(_grid()))
    _admit(tmp_path, prov)
    other = _write_half(tmp_path / "b02", _rows(_grid(), value=13.0))
    with pytest.raises(IntegrityError, match="not the receipt"):
        h.require_jan_nov_admission(tmp_path, PHASE, prov_path=other)
    with pytest.raises(IntegrityError, match="admit it in"):
        h.require_jan_nov_admission(tmp_path / "elsewhere", PHASE, prov_path=prov)


def test_identical_rows_hash_identically(tmp_path):
    """Determinism of the artifact identity: same rows, same bytes, same SHA-256."""
    a = _write_half(tmp_path / "a", _rows(_grid()))
    b = _write_half(tmp_path / "b", _rows(_grid()))
    ra, rb = (next(p.parent.glob("b01_iri2016_rows_*")) for p in (a, b))
    assert sha256_of_file(ra) == sha256_of_file(rb)
    assert json.loads(a.read_text())["rows_sha256"] == json.loads(b.read_text())["rows_sha256"]


def test_lock_relabel_helper_is_a_dataclass_replace():
    lock = _lock(environment_id=A)
    assert dataclasses.replace(lock, environment_id=B).environment_id == B
