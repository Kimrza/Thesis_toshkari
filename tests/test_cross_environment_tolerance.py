"""D-83 revision 8 §A8 items 9-12: determinism precondition, per-field floor, `environment_id`
keying, pre-W-4 non-comparability.

Purpose: negative controls proving each Student ruling of 2026-10-01 (ML-01, ML-05, DATA-09,
DATA-12) is enforced, plus the happy path. Inputs: synthetic fingerprints only; no fixture
data, no December content. Re-run behaviour: pure; nothing persists.
"""

from __future__ import annotations

import dataclasses
import json
import math
import sys
from pathlib import Path

import pytest
from src.data import cross_environment_tolerance as tol
from src.data.config import ENVIRONMENT_IDS, IntegrityError, RunRecord

A, C = tol.A_ENVIRONMENT, tol.C_ENVIRONMENT
UNITS = {"vtec": "TECU", "mse": "TECU^2"}


def field_of(key: str) -> str:
    return key.split("/")[0]


def _fp(vtec: float, mse: float) -> dict[str, float]:
    return {"vtec/0": vtec, "vtec/1": 10.0, "mse/0": mse}


def _runs(a=None, c=None):
    a = a or (_fp(20.0, 4.0), _fp(20.0, 4.0))
    c = c or (_fp(20.001, 4.0), _fp(20.001, 4.0))
    return {
        A: {f"a{i}": dict(x) for i, x in enumerate(a)},
        C: {f"c{i}": dict(x) for i, x in enumerate(c)},
    }


def test_canonical_literals_are_the_established_environment_ids() -> None:
    assert {A, C} <= ENVIRONMENT_IDS
    assert ENVIRONMENT_IDS == {"tec-thesis-311", "b01_iri", "g07-clean-run"}


def test_deterministic_runs_freeze_a_per_field_tolerance() -> None:
    frozen = tol.freeze_tolerance(_runs(), field_of=field_of, field_units=UNITS)
    assert frozen["vtec"]["unit"] == "TECU"
    assert frozen["vtec"]["statistic"] == pytest.approx(0.001)
    assert frozen["mse"]["statistic"] == 0.0
    assert frozen["mse"]["tolerance"] == frozen["mse"]["floor"] == tol.FLOOR_FACTOR * 4.0


# --- ML-01: determinism first ------------------------------------------------------------


def test_nondeterministic_a_runs_fail_the_precondition_not_the_tolerance() -> None:
    runs = _runs(a=(_fp(20.0, 4.0), _fp(20.0000001, 4.0)))
    with pytest.raises(tol.DeterminismFailure):
        tol.freeze_tolerance(runs, field_of=field_of, field_units=UNITS)


def test_nondeterministic_c_runs_fail_the_precondition() -> None:
    runs = _runs(c=(_fp(20.001, 4.0), _fp(20.002, 4.0)))
    with pytest.raises(tol.DeterminismFailure):
        tol.freeze_tolerance(runs, field_of=field_of, field_units=UNITS)


def test_single_run_cannot_show_determinism() -> None:
    with pytest.raises(tol.DeterminismFailure):
        tol.assert_deterministic(A, {"a0": _fp(1.0, 1.0)})


def test_nondeterministic_candidate_within_tolerance_is_not_rescued() -> None:
    frozen = tol.freeze_tolerance(_runs(), field_of=field_of, field_units=UNITS)
    # Both candidate values lie inside the frozen vtec tolerance, but they disagree.
    candidate = {"r0": _fp(20.0, 4.0), "r1": _fp(20.0005, 4.0)}
    with pytest.raises(tol.DeterminismFailure) as exc:
        tol.check_candidate(frozen, _fp(20.0, 4.0), C, candidate, field_of=field_of)
    assert not isinstance(exc.value, tol.ToleranceFailure)


def test_deterministic_candidate_beyond_tolerance_is_a_tolerance_failure() -> None:
    frozen = tol.freeze_tolerance(_runs(), field_of=field_of, field_units=UNITS)
    candidate = {"r0": _fp(20.5, 4.0), "r1": _fp(20.5, 4.0)}
    with pytest.raises(tol.ToleranceFailure) as exc:
        tol.check_candidate(frozen, _fp(20.0, 4.0), C, candidate, field_of=field_of)
    assert not isinstance(exc.value, tol.DeterminismFailure)


def test_deterministic_candidate_within_tolerance_passes() -> None:
    frozen = tol.freeze_tolerance(_runs(), field_of=field_of, field_units=UNITS)
    candidate = {"r0": _fp(20.0005, 4.0), "r1": _fp(20.0005, 4.0)}
    tol.check_candidate(frozen, _fp(20.0, 4.0), C, candidate, field_of=field_of)


# --- ML-05: one floor per field ------------------------------------------------------------


def test_floors_are_separate_per_field_not_shared_across_units() -> None:
    runs = _runs(a=(_fp(20.0, 400.0), _fp(20.0, 400.0)), c=(_fp(20.0, 400.0), _fp(20.0, 400.0)))
    frozen = tol.freeze_tolerance(runs, field_of=field_of, field_units=UNITS)
    assert frozen["vtec"]["floor"] == tol.FLOOR_FACTOR * 20.0
    assert frozen["mse"]["floor"] == tol.FLOOR_FACTOR * 400.0


def test_undeclared_field_cannot_inherit_a_floor() -> None:
    runs = _runs()
    for env in runs.values():
        for fp in env.values():
            fp["newfield/0"] = 1.0
    with pytest.raises(IntegrityError) as exc:
        tol.freeze_tolerance(runs, field_of=field_of, field_units=UNITS)
    assert "newfield" in str(exc.value)


def test_field_with_blank_unit_is_refused() -> None:
    with pytest.raises(IntegrityError):
        tol.freeze_tolerance(_runs(), field_of=field_of, field_units={"vtec": "TECU", "mse": " "})


def test_candidate_element_of_unfrozen_field_is_refused() -> None:
    frozen = tol.freeze_tolerance(_runs(), field_of=field_of, field_units=UNITS)
    frozen.pop("mse")
    candidate = {"r0": _fp(20.0, 4.0), "r1": _fp(20.0, 4.0)}
    with pytest.raises(IntegrityError):
        tol.check_candidate(frozen, _fp(20.0, 4.0), C, candidate, field_of=field_of)


# --- DATA-09: keyed to environment_id ------------------------------------------------------


@pytest.mark.parametrize("label", ["G-07 clean-run", "(c)", "native-Windows", "undeclared"])
def test_runs_keyed_by_a_human_readable_name_are_refused(label) -> None:
    runs = _runs()
    runs[label] = runs.pop(C)
    with pytest.raises(IntegrityError):
        tol.freeze_tolerance(runs, field_of=field_of, field_units=UNITS)


def test_b01_iri_is_not_a_tolerance_leg() -> None:
    runs = _runs()
    runs["b01_iri"] = runs.pop(C)
    with pytest.raises(IntegrityError):
        tol.freeze_tolerance(runs, field_of=field_of, field_units=UNITS)


# --- DATA-12: pre-W-4 records are not comparable -------------------------------------------


def test_pre_w4_lock_with_identical_pins_is_still_non_comparable() -> None:
    from src.data.fixture_gate import lock_items

    post = RunRecord(
        requirements_hash="r",
        pip_freeze="numpy==2.1.3\n",
        runtime_versions={"python": "3.11.9"},
        code_commit="aaaa",
        config_hashes={"data.yaml": "d"},
        input_versions=[],
        platform="local",
        nondeterministic_ops=[],
        environment_id=A,
    )
    lock_items(post)  # the post-W-4 lock is accepted
    legacy = {f.name: getattr(post, f.name) for f in dataclasses.fields(RunRecord)}
    legacy.pop("environment_id")  # every package/version value identical
    with pytest.raises(IntegrityError) as exc:
        lock_items(legacy)
    assert "non-comparable" in str(exc.value)


# --- PV-10 Rec 6 (ML-08): a non-finite value never yields an infinite floor ------------------


@pytest.mark.parametrize("bad", [float("inf"), float("-inf")])
def test_infinite_a_value_is_invalid_input_not_an_infinite_floor(bad) -> None:
    runs = _runs(a=(_fp(bad, 4.0), _fp(bad, 4.0)), c=(_fp(bad, 4.0), _fp(bad, 4.0)))
    with pytest.raises(IntegrityError) as exc:
        tol.freeze_tolerance(runs, field_of=field_of, field_units=UNITS)
    assert not isinstance(exc.value, tol.DeterminismFailure | tol.ToleranceFailure)
    assert "non-finite" in str(exc.value)


@pytest.mark.parametrize("bad", [float("inf"), float("-inf")])
def test_infinite_candidate_value_is_refused_not_passed(bad) -> None:
    frozen = tol.freeze_tolerance(_runs(), field_of=field_of, field_units=UNITS)
    candidate = {"r0": _fp(bad, 4.0), "r1": _fp(bad, 4.0)}
    with pytest.raises(IntegrityError, match="non-finite"):
        tol.check_candidate(frozen, _fp(20.0, 4.0), C, candidate, field_of=field_of)


def test_finite_candidate_against_non_finite_reference_is_refused() -> None:
    frozen = tol.freeze_tolerance(_runs(), field_of=field_of, field_units=UNITS)
    candidate = {"r0": _fp(20.0, 4.0), "r1": _fp(20.0, 4.0)}
    with pytest.raises(IntegrityError, match="non-finite"):
        tol.check_candidate(frozen, _fp(float("inf"), 4.0), C, candidate, field_of=field_of)


def test_finite_values_still_use_the_per_field_floor() -> None:
    runs = _runs(a=(_fp(20.0, 4.0), _fp(20.0, 4.0)), c=(_fp(20.0, 4.0), _fp(20.0, 4.0)))
    frozen = tol.freeze_tolerance(runs, field_of=field_of, field_units=UNITS)
    assert frozen["vtec"]["tolerance"] == tol.FLOOR_FACTOR * 20.0
    assert math.isfinite(frozen["vtec"]["tolerance"])
    over = {"r0": _fp(20.0 + 1e-3, 4.0), "r1": _fp(20.0 + 1e-3, 4.0)}
    with pytest.raises(tol.ToleranceFailure):
        tol.check_candidate(frozen, _fp(20.0, 4.0), C, over, field_of=field_of)


# --- PV-10 Rec 5: the governed field table ---------------------------------------------------

DECLARATION = Path(__file__).parent / "fixtures" / "plumbing_7day" / "identity_declaration.yaml"


def _ledger() -> dict:
    return json.loads(DECLARATION.read_text(encoding="utf-8"))["required_outputs"][
        "comparison_ledger"
    ]


def test_every_toleranced_plumbing_output_declares_a_field_table() -> None:
    ledger = _ledger()
    toleranced = [k for k, v in ledger.items() if v.get("comparison_class") == "toleranced"]
    assert sorted(toleranced) == ["metrics.json", "predictions.parquet"]
    for name in toleranced:
        table = tol.validate_field_table(name, ledger[name]["fields"])
        assert all(e["unit"].strip() for e in table)


@pytest.mark.parametrize(
    ("locator", "field", "unit"),
    [
        (
            "/evaluated/FIX-NOV-FOLD-01/primary/comparisons[0]/scalar",
            "paired_loss_differential",
            "TECU^2",
        ),
        (
            "/evaluated/FIX-NOV-FOLD-02/tier3/comparisons[1]/per_station/BSHM",
            "paired_loss_differential",
            "TECU^2",
        ),
        ("/evaluated/FIX-NOV-FOLD-01/primary/row_counts/BSHM", "row_count", "count"),
        ("/evaluated/FIX-NOV-FOLD-01/tier3/exclusion_counts/BSHM", "exclusion_count", "count"),
    ],
)
def test_metrics_locators_resolve_to_their_own_field_and_unit(locator, field, unit) -> None:
    field_of, units = tol.field_resolver("metrics.json", _ledger()["metrics.json"]["fields"])
    assert field_of(locator) == field
    assert units[field] == unit


@pytest.mark.parametrize(
    "locator",
    ["/evaluated/F/primary/new_metric", "/evaluated/F/primary/comparisons[0]/rmse"],
)
def test_a_new_metrics_leaf_inherits_no_field(locator) -> None:
    field_of, _ = tol.field_resolver("metrics.json", _ledger()["metrics.json"]["fields"])
    with pytest.raises(IntegrityError, match="matches no declared field"):
        field_of(locator)


def test_prediction_rows_resolve_to_y_hat_in_tecu() -> None:
    field_of, units = tol.field_resolver(
        "predictions.parquet", _ledger()["predictions.parquet"]["fields"]
    )
    assert field_of("FIX-NOV-FOLD-01|payload.parquet|BSHM|2022-11-03 05:00:00+00:00") == "y_hat"
    assert units["y_hat"] == "TECU"


@pytest.mark.parametrize(
    ("table", "match"),
    [
        ([], "non-empty"),
        ([{"field": "x", "locator": "a", "unit": "", "meaning": "m", "citation": "c"}], "lacks"),
        (
            [{"field": "x", "locator": "(", "unit": "u", "meaning": "m", "citation": "c"}],
            "does not compile",
        ),
        (
            [
                {"field": "x", "locator": "a", "unit": "u", "meaning": "m", "citation": "c"},
                {"field": "x", "locator": "b", "unit": "u", "meaning": "m", "citation": "c"},
            ],
            "declared twice",
        ),
    ],
)
def test_field_table_validation_refusals(table, match) -> None:
    with pytest.raises(IntegrityError, match=match):
        tol.validate_field_table("metrics.json", table)


def test_overlapping_locators_are_refused_as_ambiguous() -> None:
    table = [
        {"field": "x", "locator": "/a.*", "unit": "u", "meaning": "m", "citation": "c"},
        {"field": "y", "locator": "/ab", "unit": "v", "meaning": "m", "citation": "c"},
    ]
    field_of, _ = tol.field_resolver("o", table)
    with pytest.raises(IntegrityError, match="more than one"):
        field_of("/ab")


# --- PV-10 Recs 3-4: the runtime path routes item 11 to this module only ----------------------

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_walking_skeleton as skeleton  # noqa: E402

LEDGER = {
    "m.json": {
        "comparison_class": "toleranced",
        "fields": [
            {
                "field": "vtec",
                "locator": "vtec/.*",
                "unit": "TECU",
                "meaning": "m",
                "citation": "c",
            },
            {
                "field": "mse",
                "locator": "mse/.*",
                "unit": "TECU^2",
                "meaning": "m",
                "citation": "c",
            },
        ],
    }
}


def _result(run_id: str, env: str | None, vtec: float = 20.0) -> dict:
    out = {"measuring_run_id": run_id, "fingerprints": {"m.json": _fp(vtec, 4.0)}}
    if env is not None:
        out["environment_id"] = env
    return out


def test_runtime_routes_a_cross_environment_composition_to_item11(monkeypatch) -> None:
    calls = []
    real = skeleton.compose_item11_tolerances
    monkeypatch.setattr(
        skeleton, "compose_item11_tolerances", lambda *a, **k: calls.append(a) or real(*a, **k)
    )
    monkeypatch.setattr(
        skeleton,
        "cross_run_variation",
        lambda *_a, **_k: pytest.fail("cross_run_variation must never govern item 11"),
    )
    results = [
        _result("a0", A),
        _result("a1", A),
        _result("c0", C, 20.001),
        _result("c1", C, 20.001),
    ]
    out = skeleton.compose_tolerances(results, LEDGER, ["m.json"])
    assert calls, "the runtime path did not invoke cross_environment_tolerance"
    assert set(out["m.json"]["fields"]) == {"vtec", "mse"}
    assert out["m.json"]["environment_ids"] == sorted([A, C])


def test_runtime_refuses_a_nondeterministic_leg() -> None:
    results = [_result("a0", A), _result("a1", A, 20.5), _result("c0", C), _result("c1", C)]
    with pytest.raises(tol.DeterminismFailure):
        skeleton.compose_tolerances(results, LEDGER, ["m.json"])


def test_runtime_refuses_a_pre_w4_result_without_environment_id() -> None:
    results = [_result("a0", A), _result("legacy", None)]
    with pytest.raises(IntegrityError, match="W-4"):
        skeleton.compose_tolerances(results, LEDGER, ["m.json"])


def test_runtime_refuses_a_cross_environment_mix_other_than_a_and_c() -> None:
    results = [
        _result("a0", A),
        _result("a1", A),
        _result("b0", "b01_iri"),
        _result("b1", "b01_iri"),
    ]
    with pytest.raises(IntegrityError, match="item 11"):
        skeleton.compose_tolerances(results, LEDGER, ["m.json"])


def test_single_environment_measurement_is_not_an_item11_tolerance() -> None:
    results = [_result("a0", A), _result("a1", A)]
    out = skeleton.compose_tolerances(results, LEDGER, ["m.json"])
    assert "fields" not in out["m.json"]
    assert out["m.json"]["value"] == 0.0
