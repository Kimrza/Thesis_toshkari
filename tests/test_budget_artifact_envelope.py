"""Regression: `07_evaluate_and_report.py`'s `--budget-artifact` read site must unwrap
`write_json_artifact`'s (R-70/R-69) identity envelope before handing the budget on to
code written against `build_uncertainty_budget`'s flat, authoritative shape.

Root cause (traced, not guessed): `02_standardize_prepared_target.py` writes
`uncertainty_budget.json` through the SAME generic `write_json_artifact` envelope used
for `coverage_report.json` and `data_quality_block.json` -- domain payload nested under
`"payload"`, identity/caveat fields beside it. Every other on-disk reader of that
envelope unwraps it (`02_standardize_prepared_target.py:564` does `report.get('payload')`
for the coverage report); `07_evaluate_and_report.py`'s budget-artifact read site was the
one that did not, so it handed the raw envelope straight to `_assert_budget`
(`src/evaluation/diagnostics.py`), which checks for `artifact_id`/`phase1_contents`/
`asymmetry_statement`/`phase2_quantities` at the TOP level -- exactly where
`build_uncertainty_budget` puts them, and exactly where `tests/test_regimes_and_reporting
.py::_budget()` already puts them in its (flat, unenveloped) authoritative test fixture.

This is a wiring gap at the read site, not a producer defect and not a change to the
flat-shape contract: the fix (`_unwrap_budget_artifact` in
`scripts/07_evaluate_and_report.py`) touches only that one read site.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_script(name: str):
    """Import a digit-prefixed stage script as a module (its `main()` never runs) --
    the same idiom `tests/test_clean_run.py::_load_script` uses."""
    path = REPO_ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location("script_" + name.replace(".", "_"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


_SEVEN = _load_script("07_evaluate_and_report.py")


#: `build_uncertainty_budget`'s own flat return shape (mirrors
#: `tests/test_regimes_and_reporting.py::_budget()`, the authoritative fixture that
#: `build_primary_table` is already tested against).
_FLAT_BUDGET: dict[str, Any] = {
    "artifact_id": "uncertainty_budget",
    "units": "TECU",
    "phase1_contents": {
        "provider_reported_uncertainty": {"statement": "...", "measured_tecu": {"rows": 168}},
    },
    "phase2_quantities": {"dcb_uncertainty": "recorded not-applicable"},
    "asymmetry_statement": "a slowly varying per-station-day bias ...",
    "budget_value": 9.54,
}

#: The on-disk shape `write_json_artifact` actually produces (R-70/R-69 identity
#: envelope wrapping the same flat payload under `"payload"`), reproducing exactly the
#: nesting `02_standardize_prepared_target.py` writes for `uncertainty_budget.json`.
_ENVELOPED_BUDGET: dict[str, Any] = {
    "artifact_class": "uncertainty_budget",
    "phase_id": "P1A",
    "source_id": "GNSS_VTEC",
    "target_definition_id": "GRIDDed_VTEC_1H",
    "target_label": "location-sampled gridded VTEC",
    "lineage_caveat": "...",
    "payload": _FLAT_BUDGET,
}


def test_flat_budget_passes_through_unchanged() -> None:
    """POSITIVE CONTROL. A budget already in the producer's flat shape (no envelope) is
    returned as-is -- the unwrap is a no-op when there is nothing to unwrap, so a future
    producer that stops enveloping this artifact is never broken by this fix."""
    result = _SEVEN._unwrap_budget_artifact(_FLAT_BUDGET)
    assert result is _FLAT_BUDGET
    assert result["artifact_id"] == "uncertainty_budget"
    assert "phase1_contents" in result
    assert "asymmetry_statement" in result
    assert "phase2_quantities" in result


def test_enveloped_budget_is_unwrapped_to_the_flat_authoritative_shape() -> None:
    """The actual on-disk shape (write_json_artifact's envelope): before the fix, handing
    this straight to `_assert_budget` raised naming all four required fields missing
    (they are one level too deep, under `payload`). After the fix, unwrapping recovers
    exactly the flat shape the producer emitted and the consumer's contract requires."""
    result = _SEVEN._unwrap_budget_artifact(_ENVELOPED_BUDGET)
    assert result == _FLAT_BUDGET
    assert result["artifact_id"] == "uncertainty_budget"
    assert result["phase1_contents"] == _FLAT_BUDGET["phase1_contents"]
    assert result["asymmetry_statement"] == _FLAT_BUDGET["asymmetry_statement"]
    assert result["phase2_quantities"] == _FLAT_BUDGET["phase2_quantities"]


def test_enveloped_budget_would_fail_required_field_check_without_the_unwrap() -> None:
    """NEGATIVE CONTROL, proving the OLD (pre-fix) behaviour actually broke: passing the
    still-enveloped artifact straight into the consumer's required-field check (bypassing
    `_unwrap_budget_artifact` entirely, exactly as the read site did before this fix)
    must still be missing every field but reproduces this bug, not paper over it."""
    from src.evaluation.diagnostics import RegimeError, _assert_budget

    try:
        _assert_budget(_ENVELOPED_BUDGET)
    except RegimeError as exc:
        message = str(exc)
        assert "artifact_id" in message
        assert "phase1_contents" in message
        assert "phase2_quantities" in message
    else:
        raise AssertionError(
            "the still-enveloped budget must fail _assert_budget's required-field check "
            "(reproducing the original bug) when the unwrap step is bypassed"
        )


def test_unwrapped_budget_satisfies_the_consumer_required_field_check() -> None:
    """The fixed path end-to-end: unwrap, then the consumer's own required-field check
    (the authoritative contract, unchanged) accepts it."""
    from src.evaluation.diagnostics import _assert_budget

    unwrapped = _SEVEN._unwrap_budget_artifact(_ENVELOPED_BUDGET)
    _assert_budget(unwrapped)  # must not raise


def test_unwrap_never_misreads_a_flat_budget_that_happens_to_carry_a_payload_field() -> None:
    """A flat budget is distinguished from an enveloped one by the presence of its own
    `artifact_id` at the top level (exactly what `build_uncertainty_budget` always emits
    and `write_json_artifact`'s envelope never does) -- never by the mere presence of a
    `payload` key, so a flat shape is never accidentally unwrapped a second time."""
    flat_with_stray_payload_key = {**_FLAT_BUDGET, "payload": "not an envelope"}
    result = _SEVEN._unwrap_budget_artifact(flat_with_stray_payload_key)
    assert result is flat_with_stray_payload_key
    assert result["artifact_id"] == "uncertainty_budget"
