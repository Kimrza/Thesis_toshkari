"""Regression tests for the fixture-identity reporting-surface gate in
`scripts/07_evaluate_and_report.py::_report_set`.

PURPOSE. TE §15.3 ("Minimal model execution") exhaustively names Fixture 1's
(`plumbing_7day`) required execution: M-01, M-02, M-03, M-04, M-05, and a minimal M-06
checkpoint save/restore, plus B-01 and C-01 sample generation. TE §15.4 ("Required
outputs") exhaustively names its required outputs -- nineteen files, with
`target_uncertainty_budget.json` explicitly marked `# fixture 2 only` -- and lists NO
`claims_checklist` or `ConclusionSurfaceArtifact` entry for EITHER fixture. Neither
requires the primary table's budget adjacency (W-3) or the claims-and-limitations
checklist (W-4; R-126 control (36)) from Fixture 1.

This mirrors the already-established bootstrap exemption in `_run_bootstrap_step`
(`tests/test_bootstrap_fixture_gate.py`) at the next boundary down in the same
function, `_report_set`:

(a) Fixture 1 (`plumbing_7day`): `build_primary_table` and `build_claims_checklist`
    are NEVER called; no `ConclusionSurfaceArtifact` is required; an explicit,
    auditable skip record is written naming TE §15.3/§15.4. The mask/comparison/metric
    work upstream of this boundary (already exercised by `_run_bootstrap_step`, W-5's
    breakdowns, and W-6's practical-relevance record) is untouched.
(b) Fixture 2 (`scientific_1month`) and the governed/full-year path (`fixture_id=None`):
    `build_primary_table` and `build_claims_checklist` are STILL called, with the same
    arguments as before this change (budget_artifact, table, breakdowns,
    conclusion_surface resolved from `--conclusion-surface` exactly as before) --
    R-126 control (36) stays fail-closed, unweakened, for these runs.

CONSTANTS CONVENTION. All ids, station tokens and declared members below are test
apparatus (R-122) -- no scientific value, no December 2022 content, no restricted path.

RE-RUN BEHAVIOUR. Pure: every tree is built fresh under tmp_path; nothing under the
repository is written; repeated runs are equivalent.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_script(name: str):
    """Import a digit-prefixed stage script as a module (its `main()` never runs) --
    the same idiom `tests/test_bootstrap_fixture_gate.py` uses."""
    path = REPO_ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location("script_" + name.replace(".", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULE = _load_script("07_evaluate_and_report.py")


class _Snapshot:
    """Duck-typed stand-in: `.experiment` (read_regime_config / read_top1pct_declaration,
    both stubbed below) and `.seeds` (the Fixture-2/governed bootstrap path's seed
    lookup, real code -- `_run_bootstrap_step` is exercised for real on those paths)."""

    def __init__(self) -> None:
        self.experiment: dict[str, Any] = {}
        self.seeds: dict[str, Any] = {"replicate_seed": 20221201}


class _Partition:
    """Duck-typed stand-in: `.partition_id` only, never `LOCKED_ID` (keeps the DEC
    regime-breakdown branch, which needs `--kp-series` etc., un-reached)."""

    def __init__(self, partition_id: str = "FIX-NOV-FOLD-01") -> None:
        self.partition_id = partition_id


def _stub_regime_config(*_a: Any, **_kw: Any) -> SimpleNamespace:
    return SimpleNamespace(quality_strata_fields=[])


def _stub_top1pct_declaration(*_a: Any, **_kw: Any) -> dict[str, Any]:
    return {"removed_fraction": 0.01, "scope": "comparison_wide"}


def _apply_common_stubs(monkeypatch: pytest.MonkeyPatch, *, calls: dict[str, list[Any]]) -> None:
    """Stub every W-1/W-5/W-6 producing call `_report_set` makes so the function runs
    to completion without touching real masks, registries or governed content -- the
    same style `test_bootstrap_fixture_gate.py` uses for the bootstrap sub-step, applied
    to the rest of `_report_set`."""

    def _record(name: str):
        def _fn(*a: Any, **kw: Any) -> dict[str, Any]:
            calls.setdefault(name, []).append((a, kw))
            return {"stub": name}

        return _fn

    monkeypatch.setattr(MODULE, "read_bootstrap_declaration", lambda *a, **kw: pytest.fail(
        "bootstrap declaration must not be read on a Fixture 1 report_set run"
    ) if calls.get("_fixture_id") == [MODULE.PLUMBING_FIXTURE_ID] else {
        "block_hours": 24,
        "replicates": 10000,
        "confidence_level": 0.95,
        "sensitivity_block_hours": 48,
        "seed_key": "bootstrap.replicate_seed",
        "interval_method": "percentile",
        "block_scheme": "fixed_nonoverlapping",
        "correlation_series": "paired_error_pearson_all_pairs",
    })
    monkeypatch.setattr(MODULE, "vector_block_bootstrap", _record("vector_block_bootstrap"))
    monkeypatch.setattr(
        MODULE,
        "write_bootstrap_result",
        lambda result, path: (
            path.parent.mkdir(parents=True, exist_ok=True),
            path.write_text("{}", encoding="utf-8"),
            calls.setdefault("write_bootstrap_result", []).append(path),
        )
        and path,
    )
    monkeypatch.setattr(MODULE, "build_member_metrics_breakdown", _record("build_member_metrics_breakdown"))
    monkeypatch.setattr(MODULE, "build_breakdown_artifact", _record("build_breakdown_artifact"))
    monkeypatch.setattr(MODULE, "read_regime_config", _stub_regime_config)
    monkeypatch.setattr(MODULE, "read_top1pct_declaration", _stub_top1pct_declaration)
    monkeypatch.setattr(
        MODULE,
        "top1pct_sensitivity_block",
        lambda **kw: calls.setdefault("top1pct_sensitivity_block", []).append(kw) or {"stub": True},
    )
    monkeypatch.setattr(MODULE, "build_primary_table", _record("build_primary_table"))
    monkeypatch.setattr(MODULE, "build_claims_checklist", _record("build_claims_checklist"))


def _common_kwargs(*, tmp_path: Path, fixture_id: str | None) -> dict[str, Any]:
    report_dir = tmp_path / "report"
    return dict(
        snapshot=_Snapshot(),
        args=SimpleNamespace(
            table_caption="a caption",
            threshold_record=None,
            conclusion_surface=None,
            notebook_captions=None,
            g06_receipt_utc=None,
        ),
        partition=_Partition(),
        set_id="primary",
        declared={
            "model_id": "lstm_primary",
            "member_ids": ["lstm_primary", "iri_benchmark"],
            "benchmark_ids": ["iri_benchmark"],
        },
        declared_sets={},
        mask=object(),
        registry=object(),
        members_by_id={"lstm_primary": object(), "iri_benchmark": object()},
        metrics_artifact={"comparisons": []},
        budget_artifact={"artifact_id": "uncertainty_budget"},
        report_dir=report_dir,
        month_start=None,
        month_end=None,
        embargo_hours=24,
        locked=None,
        evaluation_mode="fixture" if fixture_id else "real_data",
        fixture_id=fixture_id,
    )


def test_plumbing_7day_skips_primary_table_and_claims_checklist(tmp_path, monkeypatch) -> None:
    """(a) Fixture 1: build_primary_table and build_claims_checklist are never called;
    no ConclusionSurfaceArtifact is required (args.conclusion_surface stays None and is
    never read); an explicit skip record is written and returned in `written`."""
    calls: dict[str, list[Any]] = {"_fixture_id": [MODULE.PLUMBING_FIXTURE_ID]}
    _apply_common_stubs(monkeypatch, calls=calls)

    written = MODULE._report_set(
        **_common_kwargs(tmp_path=tmp_path, fixture_id=MODULE.PLUMBING_FIXTURE_ID)
    )

    assert "build_primary_table" not in calls, "the primary table must not be built for Fixture 1"
    assert "build_claims_checklist" not in calls, "the claims checklist must not run for Fixture 1"

    # the bootstrap gate (tested separately in test_bootstrap_fixture_gate.py) also
    # writes its own skip record on this same Fixture 1 run -- filter to this boundary's.
    skip_files = [
        Path(p)
        for p in written
        if Path(p).name == "primary_table_and_claims_checklist_primary.skipped.json"
    ]
    assert len(skip_files) == 1, f"expected exactly one reporting-surface skip record, got: {written}"
    record = json.loads(skip_files[0].read_text(encoding="utf-8"))
    assert record["fixture_id"] == MODULE.PLUMBING_FIXTURE_ID
    assert "primary_table_budget_adjacency" in record["skipped"]
    assert "claims_checklist" in record["skipped"]
    assert "ConclusionSurfaceArtifact_requirement" in record["skipped"]
    assert "15.3" in record["reason"] and "15.4" in record["reason"]

    # the mask/comparison-adjacent W-5 breakdown work upstream of the exempted boundary
    # is untouched: the member-metrics and per-station/quality-strata/top1pct
    # breakdowns still ran.
    assert "build_member_metrics_breakdown" in calls
    assert "build_breakdown_artifact" in calls
    assert "top1pct_sensitivity_block" in calls

    # practical relevance (W-6) still ran, taking the D-34 "not produced" path (no
    # --threshold-record supplied), which needs no primary table.
    relevance_files = [Path(p) for p in written if "practical_relevance" in Path(p).name]
    assert len(relevance_files) == 1
    relevance = json.loads(relevance_files[0].read_text(encoding="utf-8"))
    assert relevance["kind"] == "practical_relevance_not_produced"


def test_scientific_1month_still_builds_table_and_checklist_unchanged(tmp_path, monkeypatch) -> None:
    """(b) Fixture 2: build_primary_table and build_claims_checklist ARE still called,
    with the real budget_artifact / table / breakdowns forwarded exactly as before --
    R-126 control (36) is not weakened for this run."""
    calls: dict[str, list[Any]] = {"_fixture_id": [MODULE.SCIENTIFIC_FIXTURE_ID]}
    _apply_common_stubs(monkeypatch, calls=calls)

    written = MODULE._report_set(
        **_common_kwargs(tmp_path=tmp_path, fixture_id=MODULE.SCIENTIFIC_FIXTURE_ID)
    )

    assert "build_primary_table" in calls, "the primary table must still be built for Fixture 2"
    table_args, table_kwargs = calls["build_primary_table"][0]
    assert table_kwargs["budget_artifact"] == {"artifact_id": "uncertainty_budget"}

    assert "build_claims_checklist" in calls, "the claims checklist must still run for Fixture 2"
    checklist_args, checklist_kwargs = calls["build_claims_checklist"][0]
    # conclusion_surface=None is NOT a skip -- it is forwarded through exactly as
    # before, and the real `build_claims_checklist` fails closed on it (R-126 control
    # (36)); this stub only proves the CALL still happens, not the fail-closed body
    # (covered by `test_conclusion_surface_none_still_fails_closed_for_governed_runs`).
    assert checklist_kwargs["conclusion_surface"] is None

    assert not any(Path(p).name.endswith(".skipped.json") for p in written), (
        "no reporting-surface skip record for a Fixture 2 run"
    )


def test_full_year_governed_path_fixture_id_none_still_builds_table_and_checklist(
    tmp_path, monkeypatch
) -> None:
    """(b), governed path: `fixture_id=None` (the full-year call site) also still
    builds the primary table and runs the claims checklist, unchanged."""
    calls: dict[str, list[Any]] = {"_fixture_id": [None]}
    _apply_common_stubs(monkeypatch, calls=calls)

    written = MODULE._report_set(**_common_kwargs(tmp_path=tmp_path, fixture_id=None))

    assert "build_primary_table" in calls
    assert "build_claims_checklist" in calls
    assert not any(Path(p).name.endswith(".skipped.json") for p in written)


def test_conclusion_surface_none_still_fails_closed_for_governed_runs() -> None:
    """R-126 control (36), unmodified: `build_claims_checklist` itself (not the
    orchestrator wiring) still raises when `conclusion_surface` is absent -- proving the
    guard's substance, not just its call site, is untouched by this change."""
    from src.evaluation.diagnostics import build_claims_checklist
    from src.evaluation.report_guards import ConclusionSurfaceRegistry
    from src.data.config import RegimeError

    registry = ConclusionSurfaceRegistry(Path("does-not-matter"))
    with pytest.raises(RegimeError):
        build_claims_checklist(
            registry=registry,
            conclusion_surface=None,
            table={"rows": []},
            breakdowns=[],
            notebook_captions=None,
            checklist_artifact_id="claims_checklist_test",
            emit_path=None,
        )


def test_threshold_record_on_a_fixture1_run_refuses_instead_of_crashing(tmp_path, monkeypatch) -> None:
    """Defensive control: if a caller ever supplies --threshold-record on a Fixture 1
    run (the orchestrator never does), practical relevance refuses by name rather than
    raising an unbound-`table` NameError -- the exemption fails safely, not silently."""
    calls: dict[str, list[Any]] = {"_fixture_id": [MODULE.PLUMBING_FIXTURE_ID]}
    _apply_common_stubs(monkeypatch, calls=calls)

    kwargs = _common_kwargs(tmp_path=tmp_path, fixture_id=MODULE.PLUMBING_FIXTURE_ID)
    threshold_path = tmp_path / "threshold_record.json"
    threshold_path.write_text(
        json.dumps({"reference_benchmark_id": "iri_benchmark"}), encoding="utf-8"
    )
    kwargs["args"].threshold_record = threshold_path

    with pytest.raises(MODULE.IntegrityError, match="no primary table was built"):
        MODULE._report_set(**kwargs)
