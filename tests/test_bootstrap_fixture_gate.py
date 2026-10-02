"""Regression tests for the fixture-identity bootstrap gate in
`scripts/07_evaluate_and_report.py`.

PURPOSE. TE §15.3 ("Minimal model execution") names the vector time-block bootstrap
ONLY for Fixture 2 (`scientific_1month`, "one bootstrap execution at reduced replicate
count for timing"). Fixture 1 (`plumbing_7day`) is scoped to M-01..M-05 plus a minimal
M-06 checkpoint save/restore and B-01/C-01 sample generation -- bootstrap is not named
for it, and D-20's single-station (BSHM) freeze is structurally mismatched with the
bootstrap's three-station, equal-station-weighted mechanism. This is a student-owned
Q-31 execution-scoping decision, not a change to any scientific value.

These tests exercise `_run_bootstrap_step`, the function `_report_set` delegates the
W-1 bootstrap sub-step to, in isolation:

(a) Fixture 1 (`plumbing_7day`) must NOT invoke `vector_block_bootstrap` at all, and
    must instead write an auditable skip record naming the reason.
(b) Fixture 2 (`scientific_1month`) and the governed/full-year path (`fixture_id=None`)
    must invoke `vector_block_bootstrap` exactly as before, with unchanged parameters
    (block_hours, replicates, seed) read from the bootstrap declaration.
(c) The gate is keyed on fixture IDENTITY, never on a caught R-116 (zero-masked-rows)
    failure -- R-116 itself is untouched by this change and still raises when bootstrap
    IS invoked and support is genuinely zero.

CONSTANTS CONVENTION. All ids, station tokens, seeds and replicate counts below are
declared constants OF THE TEST APPARATUS (R-122) -- no scientific value, no December
2022 content, no restricted path.

RE-RUN BEHAVIOUR. Pure: every tree is built fresh under tmp_path; nothing under the
repository is written; repeated runs are equivalent.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

import pytest
from src.data.config import IntegrityError  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_script(name: str):
    """Import a digit-prefixed stage script as a module (its `main()` never runs)."""
    path = REPO_ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location("script_" + name.replace(".", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULE = _load_script("07_evaluate_and_report.py")


class _Snapshot:
    """Duck-typed stand-in for the config snapshot: only `.experiment` and `.seeds` are
    consumed on the non-gated (bootstrap IS invoked) path."""

    def __init__(self, *, experiment: dict[str, Any], seeds: dict[str, Any]) -> None:
        self.experiment = experiment
        self.seeds = seeds


def _declaration_payload() -> dict[str, Any]:
    return {
        "block_hours": 24,
        "replicates": 10000,
        "confidence_level": 0.95,
        "sensitivity_block_hours": 48,
        "seed_key": "bootstrap.replicate_seed",
        "interval_method": "percentile",
        "block_scheme": "fixed_nonoverlapping",
        "correlation_series": "paired_error_pearson_all_pairs",
    }


def _common_kwargs(*, tmp_path: Path, fixture_id: str | None) -> dict[str, Any]:
    return dict(
        snapshot=_Snapshot(
            experiment={"bootstrap": _declaration_payload()},
            seeds={"replicate_seed": 20221201},
        ),
        model_id="lstm_primary",
        model=object(),
        members_by_id={"lstm_primary": object(), "iri_benchmark": object()},
        declared={"model_id": "lstm_primary", "benchmark_ids": ["iri_benchmark"]},
        declared_sets={},
        mask=object(),
        registry=object(),
        report_dir=tmp_path / "report",
        month_start=None,
        month_end=None,
        embargo_hours=24,
        locked=None,
        evaluation_mode="fixture" if fixture_id else "real_data",
        fixture_id=fixture_id,
        # TE 15.3 / R-122 (closure 2026-10-01): Fixture 2's reduced replicate count comes from
        # its identity declaration's fixture_bootstrap block (1000), never the governed 10,000.
        fixture_bootstrap_replicates=(
            1000 if fixture_id == MODULE.SCIENTIFIC_FIXTURE_ID else None
        ),
    )


def test_plumbing_7day_never_invokes_bootstrap_and_writes_audit_note(tmp_path, monkeypatch):
    """(a) Fixture 1 (plumbing_7day): vector_block_bootstrap is never called; an
    auditable skip record is written and named in `written`."""
    calls: list[Any] = []
    monkeypatch.setattr(
        MODULE, "vector_block_bootstrap", lambda *a, **kw: calls.append((a, kw))
    )
    monkeypatch.setattr(
        MODULE,
        "read_bootstrap_declaration",
        lambda *a, **kw: pytest.fail("read_bootstrap_declaration must not be called"),
    )

    written = MODULE._run_bootstrap_step(
        **_common_kwargs(tmp_path=tmp_path, fixture_id=MODULE.PLUMBING_FIXTURE_ID)
    )

    assert calls == [], "vector_block_bootstrap must never be invoked for plumbing_7day"
    assert len(written) == 1
    skip_path = Path(written[0])
    assert skip_path.name == "bootstrap_lstm_primary_vs_iri_benchmark.skipped.json"
    assert skip_path.is_file()
    record = json.loads(skip_path.read_text(encoding="utf-8"))
    assert record["skipped"] is True
    assert record["fixture_id"] == MODULE.PLUMBING_FIXTURE_ID
    assert record["model_id"] == "lstm_primary"
    assert record["benchmark_id"] == "iri_benchmark"
    assert "TE" in record["reason"] and "15.3" in record["reason"]
    assert "does not require Fixture 1" in record["reason"]


def test_scientific_1month_still_invokes_bootstrap_unchanged(tmp_path, monkeypatch):
    """(b) Fixture 2 (scientific_1month): vector_block_bootstrap IS invoked, with the
    declared block_hours/replicates/seed unchanged."""
    calls: list[dict[str, Any]] = []

    def _spy(model, benchmark, **kwargs):
        calls.append(kwargs)
        return {"ok": True}

    written_paths: list[Path] = []

    def _write_stub(result, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result), encoding="utf-8")
        written_paths.append(path)
        return path

    monkeypatch.setattr(MODULE, "vector_block_bootstrap", _spy)
    monkeypatch.setattr(MODULE, "write_bootstrap_result", _write_stub)
    # The duck-typed mask carries no rows; the planted-correlation control (R-121 control
    # (23)) is fed an apparatus series instead and asserted recorded below.
    stamps = ["2001-03-02T00:00:00Z", "2001-03-03T00:00:00Z", "2001-03-04T00:00:00Z"]
    monkeypatch.setattr(
        MODULE,
        "paired_difference_series",
        lambda *a: {s: list(zip(stamps, [1.0, 4.0, 2.0], strict=True)) for s in ("A", "B", "C")},
    )
    MODULE._SCIENTIFIC_INSTRUMENTS["planted_deviations"] = []

    written = MODULE._run_bootstrap_step(
        **_common_kwargs(tmp_path=tmp_path, fixture_id=MODULE.SCIENTIFIC_FIXTURE_ID)
    )

    assert len(calls) == 1
    kwargs = calls[0]
    assert kwargs["block_hours"] == 24
    # Fixture 2 runs TE 15.3's REDUCED replicate count (fixture_bootstrap.replicates), not
    # the governed 10,000 that this assertion carried before 2026-10-01.
    assert kwargs["replicates"] == 1000
    assert kwargs["seed"] == 20221201
    assert kwargs["evaluation_mode"] == "fixture"
    assert kwargs["timings"] is MODULE._SCIENTIFIC_INSTRUMENTS["timings"]  # R-120 limb 4
    assert MODULE._SCIENTIFIC_INSTRUMENTS["planted_deviations"] == [pytest.approx(0.0)]
    assert len(written) == 1
    assert Path(written[0]).name == "bootstrap_lstm_primary_vs_iri_benchmark.json"


def test_full_year_path_fixture_id_none_still_invokes_bootstrap(tmp_path, monkeypatch):
    """(b), governed path: `fixture_id=None` (the full-year call site never passes
    `fixture_id`) still invokes bootstrap exactly as before."""
    calls: list[dict[str, Any]] = []

    def _spy(model, benchmark, **kwargs):
        calls.append(kwargs)
        return {"ok": True}

    monkeypatch.setattr(MODULE, "vector_block_bootstrap", _spy)
    monkeypatch.setattr(
        MODULE,
        "write_bootstrap_result",
        lambda result, path: (path.parent.mkdir(parents=True, exist_ok=True), path.write_text("{}"), path)[-1],
    )

    written = MODULE._run_bootstrap_step(**_common_kwargs(tmp_path=tmp_path, fixture_id=None))

    assert len(calls) == 1
    assert calls[0]["block_hours"] == 24
    assert calls[0]["replicates"] == 10000
    assert calls[0]["timings"] is None  # the fixture-only measurement never runs governed
    assert len(written) == 1


def test_r116_untouched_zero_support_still_raises_when_bootstrap_is_invoked(tmp_path, monkeypatch):
    """(c) R-116 is untouched: when bootstrap IS invoked (fixture_id != plumbing_7day)
    and support is genuinely zero, the underlying error still propagates -- it is never
    caught or swallowed by the gate."""

    class _ZeroSupportError(RuntimeError):
        pass

    def _raises(*a, **kw):
        raise _ZeroSupportError(
            "station BSHM: has zero masked rows across a replicate's drawn blocks"
        )

    monkeypatch.setattr(MODULE, "vector_block_bootstrap", _raises)

    with pytest.raises(_ZeroSupportError, match="zero masked rows"):
        MODULE._run_bootstrap_step(
            **_common_kwargs(tmp_path=tmp_path, fixture_id=MODULE.SCIENTIFIC_FIXTURE_ID)
        )


def test_scientific_1month_without_fixture_bootstrap_refuses(tmp_path):
    """Negative control (closure 2026-10-01): Fixture 2 never falls back to the governed
    replicate count; an absent fixture_bootstrap block refuses by name."""
    kwargs = _common_kwargs(tmp_path=tmp_path, fixture_id=MODULE.SCIENTIFIC_FIXTURE_ID)
    kwargs["fixture_bootstrap_replicates"] = None
    with pytest.raises(IntegrityError, match="fixture_bootstrap.replicates"):
        MODULE._run_bootstrap_step(**kwargs)


def test_governed_path_keeps_the_declared_replicates(tmp_path, monkeypatch):
    """The governed/full-year path (fixture_id None) still uses experiment.bootstrap.replicates."""
    calls = []
    monkeypatch.setattr(MODULE, "vector_block_bootstrap", lambda *a, **k: calls.append(k) or (_ for _ in ()).throw(RuntimeError("stop")))
    with pytest.raises(RuntimeError, match="stop"):
        MODULE._run_bootstrap_step(**_common_kwargs(tmp_path=tmp_path, fixture_id=None))
    assert calls and calls[0]["replicates"] == 10000


def test_scientific_measurements_refuse_when_unmeasured_and_emit_when_measured():
    """P-S3 SC2's refusal cause: both scientific-only quantities are MEASURED by stage 07
    or the stage refuses; nothing is invented."""
    MODULE._SCIENTIFIC_INSTRUMENTS["timings"] = {}
    MODULE._SCIENTIFIC_INSTRUMENTS["planted_deviations"] = []
    with pytest.raises(IntegrityError, match="never invented"):
        MODULE._scientific_measurements()
    MODULE._SCIENTIFIC_INSTRUMENTS["timings"] = {MODULE.WIDENING_COMPARATOR_CPU_KEY: 2.5}
    MODULE._SCIENTIFIC_INSTRUMENTS["planted_deviations"] = [1e-16, 0.0]
    out = MODULE._scientific_measurements()
    assert out["runtime"]["widening_guard_cpu"] == {"min": 2.5, "max": 2.5, "units": "s"}
    planted = out["numerical_variation"]["planted_correlation_recovery_tolerance"]
    assert (planted["min"], planted["max"], planted["units"]) == (0.0, 1e-16, "dimensionless")
