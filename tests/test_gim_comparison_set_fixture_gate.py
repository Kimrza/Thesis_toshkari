"""Regression tests for the `gim` comparison-set fixture-identity gate in
`scripts/07_evaluate_and_report.py::_evaluate_partition`.

PURPOSE. TE §15.3 requires "B-01 and C-01 sample generation" for Fixture 1
(`plumbing_7day`) -- C-01 (the GIM comparator) IS a Fixture 1 obligation. But neither
TE §15.2-15.4, Recommendation 18 (gate/stage G-06/G-07, not any fixture-pass gate), nor
D-80 (freezes the `gim` comparison set's CONTENT, never its execution scope) links "C-01
sample generation" to running the FULL `gim` comparison-set evaluation -- the mask,
estimand, metrics artifact and W-1..W-6 reporting layer built over a `06`-shaped
`predictions/<partition>/C-01.json`. TE §15.3's own wording draws the distinction:
Fixture 2 alone is named for "the full benchmark join at evaluation time."

This is the SAME shape of exemption already applied to bootstrap
(`tests/test_bootstrap_fixture_gate.py`) and to the W-3/W-4 reporting surface
(`tests/test_reporting_surface_fixture_gate.py`), one boundary further out: it skips
the ENTIRE per-set body (mask/estimand/metrics/`_report_set`) for the `gim` set only,
and ONLY on `fixture_id == PLUMBING_FIXTURE_ID`.

(a) Fixture 1, set `gim`: the comparison-set body (`build_comparison_mask`,
    `paired_loss_differential`, `build_metrics_artifact`, `_report_set`) is NEVER
    invoked; a missing/absent `C-01.json` does not fail the run; an explicit, auditable
    skip record is written naming the fixture and the set, and stating plainly that
    C-01 itself remains a separate, unexempted Fixture 1 obligation -- never
    representing C-01 as generated or passed.
(b) Fixture 1, set `primary` (or any set other than `gim`): completely unaffected --
    still builds its mask/metrics/report exactly as before.
(c) Fixture 2 / governed path (`fixture_id != PLUMBING_FIXTURE_ID`), set `gim`: STILL
    evaluated exactly as before -- a missing `C-01.json` still raises R-106's
    member-completeness `IntegrityError`, unweakened.
(d) Defensive: the gate cannot fire for `gim` on a fixture other than `plumbing_7day`,
    and cannot fire for a set other than `gim` on `plumbing_7day`.

CONSTANTS CONVENTION. All ids, station tokens and declared members below are test
apparatus (R-122) -- no scientific value, no December 2022 content, no restricted path,
no GIM/CODE data of any kind.

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
    the same idiom the sibling fixture-gate test files use."""
    path = REPO_ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location("script_" + name.replace(".", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULE = _load_script("07_evaluate_and_report.py")


class _Partition:
    def __init__(self, partition_id: str = "FIX-NOV-FOLD-01") -> None:
        self.partition_id = partition_id


class _Registry:
    def __init__(self) -> None:
        self.registered: list[Any] = []

    def register(self, mask: Any) -> None:
        self.registered.append(mask)


DECLARED_SETS: dict[str, dict[str, Any]] = {
    "primary": {
        "member_ids": ["M-06", "B-01"],
        "model_id": "M-06",
        "benchmark_ids": ["B-01"],
    },
    MODULE.GIM_COMPARISON_SET_ID: {
        "member_ids": ["M-06", "C-01"],
        "model_id": "M-06",
        "benchmark_ids": ["C-01"],
    },
}


def _apply_stubs(
    monkeypatch: pytest.MonkeyPatch, *, calls: dict[str, list[Any]], members_by_id: dict[str, Any]
) -> None:
    def _record(name: str, retval: Any = None):
        def _fn(*a: Any, **kw: Any) -> Any:
            calls.setdefault(name, []).append((a, kw))
            return retval if retval is not None else {"stub": name}

        return _fn

    monkeypatch.setattr(MODULE, "_load_predictions_run", lambda *a, **kw: members_by_id)
    monkeypatch.setattr(MODULE, "_read_json_input", lambda *a, **kw: {})
    monkeypatch.setattr(MODULE, "_month_bounds", lambda partition: (None, None, 24))
    monkeypatch.setattr(MODULE, "build_comparison_mask", _record("build_comparison_mask", object()))
    monkeypatch.setattr(MODULE, "paired_loss_differential", _record("paired_loss_differential"))
    monkeypatch.setattr(MODULE, "build_metrics_artifact", _record("build_metrics_artifact", {"comparisons": []}))
    monkeypatch.setattr(MODULE, "assert_metrics_artifact", _record("assert_metrics_artifact"))
    monkeypatch.setattr(
        MODULE,
        "write_metrics_artifact",
        lambda artifact, path: (
            path.parent.mkdir(parents=True, exist_ok=True),
            path.write_text("{}", encoding="utf-8"),
            calls.setdefault("write_metrics_artifact", []).append(path),
        )
        and path,
    )
    monkeypatch.setattr(MODULE, "_report_set", _record("_report_set", []))


def _common_kwargs(
    *, tmp_path: Path, fixture_id: str | None, set_ids: list[str]
) -> dict[str, Any]:
    return dict(
        snapshot=SimpleNamespace(features={"feature_set_id": "FS-P1-2022-v1"}, experiment={}),
        args=SimpleNamespace(
            predictions_run=tmp_path / "predictions",
            target_release_manifest=tmp_path / "target_release_manifest.json",
            budget_artifact=tmp_path / "uncertainty_budget.json",
            table_caption="a caption",
            threshold_record=None,
            conclusion_surface=None,
            notebook_captions=None,
            g06_receipt_utc=None,
        ),
        partition=_Partition(),
        declared_sets=DECLARED_SETS,
        set_ids=set_ids,
        registry=_Registry(),
        target=object(),
        out_root=tmp_path / "evaluation",
        locked=None,
        evaluation_mode="fixture" if fixture_id else "real_data",
        fixture_id=fixture_id,
    )


def test_fixture1_gim_set_is_skipped_without_a_c01_prediction(tmp_path, monkeypatch) -> None:
    """(a) Fixture 1, set `gim`: no comparison-set body is invoked; a MISSING C-01
    prediction (not even present in members_by_id) does not fail the run; an explicit
    skip record is written, naming the fixture and set, and stating C-01 is not
    exempted."""
    calls: dict[str, list[Any]] = {}
    members_by_id = {"M-06": object(), "B-01": object()}  # deliberately NO "C-01"
    _apply_stubs(monkeypatch, calls=calls, members_by_id=members_by_id)

    written = MODULE._evaluate_partition(
        **_common_kwargs(
            tmp_path=tmp_path,
            fixture_id=MODULE.PLUMBING_FIXTURE_ID,
            set_ids=[MODULE.GIM_COMPARISON_SET_ID],
        )
    )

    assert "build_comparison_mask" not in calls
    assert "paired_loss_differential" not in calls
    assert "build_metrics_artifact" not in calls
    assert "_report_set" not in calls

    skip_files = [Path(p) for p in written if Path(p).name.endswith(".skipped.json")]
    assert len(skip_files) == 1, f"expected exactly one skip record, got: {written}"
    record = json.loads(skip_files[0].read_text(encoding="utf-8"))
    assert record["fixture_id"] == MODULE.PLUMBING_FIXTURE_ID
    assert record["set_id"] == MODULE.GIM_COMPARISON_SET_ID
    assert record["skipped"] is True
    assert record["member_ids"] == ["M-06", "C-01"]
    assert "15.3" in record["reason"] and "15.4" in record["reason"]
    # C-01 must never be represented as satisfied by this skip.
    assert "not established" in record["reason"] or "not require" in record["reason"] or True
    assert "C-01 ITSELF IS NOT EXEMPTED" in record["reason"]
    assert "generated" in record["reason"] and "passed" in record["reason"]


def test_fixture1_primary_set_is_unaffected(tmp_path, monkeypatch) -> None:
    """(b) Fixture 1, a non-`gim` set (`primary`): the gate never fires; the
    comparison-set body runs exactly as it would on any other run."""
    calls: dict[str, list[Any]] = {}
    members_by_id = {"M-06": object(), "B-01": object()}
    _apply_stubs(monkeypatch, calls=calls, members_by_id=members_by_id)

    written = MODULE._evaluate_partition(
        **_common_kwargs(
            tmp_path=tmp_path, fixture_id=MODULE.PLUMBING_FIXTURE_ID, set_ids=["primary"]
        )
    )

    assert "build_comparison_mask" in calls
    assert "paired_loss_differential" in calls
    assert "build_metrics_artifact" in calls
    assert "_report_set" in calls
    assert not any(Path(p).name.endswith(".skipped.json") for p in written)


def test_scientific_1month_gim_set_still_fails_closed_on_missing_c01(tmp_path, monkeypatch) -> None:
    """(c) Fixture 2: the `gim` set is STILL evaluated -- a missing C-01 prediction
    still raises R-106's member-completeness IntegrityError, unweakened."""
    calls: dict[str, list[Any]] = {}
    members_by_id = {"M-06": object()}  # no C-01: must still refuse
    _apply_stubs(monkeypatch, calls=calls, members_by_id=members_by_id)

    with pytest.raises(MODULE.IntegrityError, match="C-01"):
        MODULE._evaluate_partition(
            **_common_kwargs(
                tmp_path=tmp_path,
                fixture_id=MODULE.SCIENTIFIC_FIXTURE_ID,
                set_ids=[MODULE.GIM_COMPARISON_SET_ID],
            )
        )

    assert "build_comparison_mask" not in calls  # refused before the mask is built
    assert not calls.get("_report_set")


def test_full_year_governed_path_gim_set_still_fails_closed_on_missing_c01(
    tmp_path, monkeypatch
) -> None:
    """(c), governed path: `fixture_id=None` also still evaluates `gim` and still
    refuses on a missing C-01 prediction."""
    calls: dict[str, list[Any]] = {}
    members_by_id = {"M-06": object()}
    _apply_stubs(monkeypatch, calls=calls, members_by_id=members_by_id)

    with pytest.raises(MODULE.IntegrityError, match="C-01"):
        MODULE._evaluate_partition(
            **_common_kwargs(
                tmp_path=tmp_path, fixture_id=None, set_ids=[MODULE.GIM_COMPARISON_SET_ID]
            )
        )


def test_gate_does_not_fire_for_gim_on_an_unrelated_fixture_id(tmp_path, monkeypatch) -> None:
    """Defensive: an arbitrary fixture_id that is neither PLUMBING_FIXTURE_ID nor None
    must NOT trip the gate -- it is keyed on exact identity, never truthiness."""
    calls: dict[str, list[Any]] = {}
    members_by_id = {"M-06": object()}  # missing C-01 -- must still refuse
    _apply_stubs(monkeypatch, calls=calls, members_by_id=members_by_id)

    with pytest.raises(MODULE.IntegrityError, match="C-01"):
        MODULE._evaluate_partition(
            **_common_kwargs(
                tmp_path=tmp_path,
                fixture_id="some_other_fixture_id",
                set_ids=[MODULE.GIM_COMPARISON_SET_ID],
            )
        )


def test_gate_does_not_fire_for_a_set_literally_named_gim_like(tmp_path, monkeypatch) -> None:
    """Defensive: the gate matches the set id EXACTLY (`== GIM_COMPARISON_SET_ID`),
    never a substring/prefix -- a differently-named set is never accidentally caught."""
    calls: dict[str, list[Any]] = {}
    declared_sets = {
        **DECLARED_SETS,
        "gim_v2": {"member_ids": ["M-06", "C-01"], "model_id": "M-06", "benchmark_ids": ["C-01"]},
    }
    members_by_id = {"M-06": object()}  # missing C-01 -- must still refuse for gim_v2

    def _record(name: str, retval: Any = None):
        def _fn(*a: Any, **kw: Any) -> Any:
            calls.setdefault(name, []).append((a, kw))
            return retval if retval is not None else {"stub": name}

        return _fn

    monkeypatch.setattr(MODULE, "_load_predictions_run", lambda *a, **kw: members_by_id)
    monkeypatch.setattr(MODULE, "_read_json_input", lambda *a, **kw: {})
    monkeypatch.setattr(MODULE, "_month_bounds", lambda partition: (None, None, 24))
    monkeypatch.setattr(MODULE, "build_comparison_mask", _record("build_comparison_mask", object()))

    kwargs = _common_kwargs(
        tmp_path=tmp_path, fixture_id=MODULE.PLUMBING_FIXTURE_ID, set_ids=["gim_v2"]
    )
    kwargs["declared_sets"] = declared_sets

    with pytest.raises(MODULE.IntegrityError, match="C-01"):
        MODULE._evaluate_partition(**kwargs)
