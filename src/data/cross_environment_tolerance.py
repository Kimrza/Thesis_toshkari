"""The (a)/(c) cross-environment tolerance of D-83 item 11, with the determinism precondition
and the per-field floor (D-83 revision 8 §A8 items 9 and 10; GOV-2026-09-30-PV-09 ML-01, ML-05).

Purpose
-------
D-83 item 11 freezes, per toleranced output, tolerance = max(statistic, floor). Revision 8
adds two rules the Student ruled on 2026-10-01:

* **Determinism first (ML-01).** The tolerance is computed, and a candidate is checked against
  it, only after every environment's measuring runs have satisfied the determinism
  precondition: within one `environment_id`, the runs agree element for element exactly (NaN
  at the same positions). A run set that fails raises `DeterminismFailure`; the tolerance is
  never widened to absorb ordinary nondeterministic variation, and a determinism failure is
  never reported as a tolerance failure. A candidate that exceeds the frozen tolerance raises
  `ToleranceFailure`, a separate type.
* **One floor per field (ML-05).** Every element belongs to exactly one declared field, and
  every field carries its own declared unit. The floor is 2⁻²³ × max|x| over THAT field's (a)
  elements. An element whose field is undeclared, or a field without a unit, is refused, so
  a future field cannot inherit another field's floor.

Comparisons are keyed to `environment_id` (DATA-09): the measuring runs are grouped by their
recorded `environment_id`, and (a) and (c) are the canonical literals `tec-thesis-311` and
`g07-clean-run`, never a human-readable environment name.

Inputs
------
Numeric fingerprints (`src.data.fixture_outputs.numeric_fingerprint`) grouped as
``{environment_id: {run_id: {locator: value}}}``, a `field_of(locator)` mapping, and the
declared ``{field: unit}`` table.

Re-run behaviour
----------------
Pure and deterministic; nothing is read or written. The same inputs give the same tolerance
or the same refusal.
"""

from __future__ import annotations

import math
import re
from collections.abc import Callable, Mapping, Sequence
from typing import Any, Final

from src.data.config import ENVIRONMENT_IDS, IntegrityError

__all__ = [
    "C_ENVIRONMENT",
    "A_ENVIRONMENT",
    "FLOOR_FACTOR",
    "DeterminismFailure",
    "ToleranceFailure",
    "assert_deterministic",
    "check_candidate",
    "check_produced_output",
    "compose_item11_tolerances",
    "field_resolver",
    "freeze_tolerance",
    "validate_field_table",
]

#: D-83 item 1: (a) native-Windows and (c) WSL2 G-07 clean-run, as `environment_id` literals.
A_ENVIRONMENT: Final[str] = "tec-thesis-311"
C_ENVIRONMENT: Final[str] = "g07-clean-run"

#: float32 machine epsilon, the coarsest compute precision in the pipeline (§A8 item 7).
FLOOR_FACTOR: Final[float] = 2.0**-23


class DeterminismFailure(IntegrityError):
    """Runs within one `environment_id` disagree: a reproducibility failure, not a metric one."""


class ToleranceFailure(IntegrityError):
    """A deterministic candidate exceeds a field's frozen tolerance: a genuine metric failure."""


def _same(x: float, y: float) -> bool:
    """Exact equality with NaN matching NaN by position.

    Disclosed (GOV-2026-10-01-PV-10 Rec 25, ML-11): IEEE-754 equality treats `-0.0` and
    `0.0` as EQUAL, and so does this check. A run producing `-0.0` where another produced
    `0.0` therefore satisfies the determinism precondition. The two are the same real
    number and no output field in the governed table assigns meaning to the sign of zero.
    The minimum of two runs per environment matches the precommitted K = 2.
    """
    return (math.isnan(x) and math.isnan(y)) or x == y


def _require_finite_or_nan(resource: str, value: float) -> None:
    """`±inf` is invalid input, never a value a tolerance is computed from or compared with.

    An infinite element would make a field's floor infinite and pass every difference
    (GOV-2026-10-01-PV-10 Rec 6, ML-08). It is refused as an integrity violation, distinct
    from both a determinism failure and a tolerance failure. NaN keeps its existing meaning
    (a recorded gap, matched by position).
    """
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise IntegrityError(resource, f"{value!r} is not a number")
    if math.isinf(value):
        raise IntegrityError(
            resource,
            f"non-finite value {value!r}: an infinite element is invalid input and is never "
            "toleranced (D-83 revision 8 section A8 item 10; PV-10 Rec 6)",
        )


def assert_deterministic(
    environment_id: str, runs: Mapping[str, Mapping[str, float]]
) -> dict[str, float]:
    """The determinism precondition for one environment; returns its single agreed fingerprint.

    Needs at least two runs (one run cannot show determinism) carrying the same element set
    and exactly equal values, NaN matching NaN by position.
    """
    if environment_id not in ENVIRONMENT_IDS:
        raise IntegrityError(
            "environment_id", f"{environment_id!r} is not a named environment (D-83 item 1)"
        )
    run_ids = sorted(runs)
    if len(run_ids) < 2:
        raise DeterminismFailure(
            f"environment {environment_id}",
            f"needs at least two measuring runs to show determinism, got {run_ids}",
        )
    for run_id in run_ids:
        for key, value in runs[run_id].items():
            _require_finite_or_nan(f"environment {environment_id} run {run_id} at {key}", value)
    first = runs[run_ids[0]]
    for run_id in run_ids[1:]:
        other = runs[run_id]
        if set(other) != set(first):
            raise DeterminismFailure(
                f"environment {environment_id}",
                f"runs {run_ids[0]} and {run_id} carry different element sets",
            )
        for key, value in first.items():
            if not _same(value, other[key]):
                raise DeterminismFailure(
                    f"environment {environment_id} at {key}",
                    f"runs {run_ids[0]} and {run_id} differ ({value!r} vs {other[key]!r}); the "
                    "determinism precondition fails and no tolerance is computed "
                    "(D-83 revision 8 section A8 item 9)",
                )
    return dict(first)


def _fields(
    keys: set[str], field_of: Callable[[str], str], field_units: Mapping[str, str]
) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for key in sorted(keys):
        field = field_of(key)
        unit = field_units.get(field)
        if not isinstance(unit, str) or not unit.strip():
            raise IntegrityError(
                f"element {key}",
                f"field {field!r} has no declared unit; every field carries its own unit and "
                "floor, and none inherits another's (D-83 revision 8 section A8 item 10)",
            )
        grouped.setdefault(field, []).append(key)
    return grouped


def freeze_tolerance(
    runs_by_environment: Mapping[str, Mapping[str, Mapping[str, float]]],
    *,
    field_of: Callable[[str], str],
    field_units: Mapping[str, str],
) -> dict[str, dict[str, Any]]:
    """Per-field tolerance = max(statistic, floor) over the (a) and (c) measuring runs.

    Determinism is asserted for (a) and (c) before anything is computed. The statistic is the
    maximum |(c) − (a)| over the field's elements; the floor is `FLOOR_FACTOR` × max|x| over
    the field's (a) elements.
    """
    if set(runs_by_environment) != {A_ENVIRONMENT, C_ENVIRONMENT}:
        raise IntegrityError(
            "measuring runs",
            f"keyed by environment_id {sorted(runs_by_environment)}; exactly "
            f"{[A_ENVIRONMENT, C_ENVIRONMENT]} are required (D-83 item 11)",
        )
    a = assert_deterministic(A_ENVIRONMENT, runs_by_environment[A_ENVIRONMENT])
    c = assert_deterministic(C_ENVIRONMENT, runs_by_environment[C_ENVIRONMENT])
    if set(a) != set(c):
        raise IntegrityError("measuring runs", "(a) and (c) carry different element sets")
    out: dict[str, dict[str, Any]] = {}
    for field, keys in _fields(set(a), field_of, field_units).items():
        statistic = 0.0
        scale = 0.0
        for key in keys:
            if math.isnan(a[key]) or math.isnan(c[key]):
                if not (math.isnan(a[key]) and math.isnan(c[key])):
                    raise IntegrityError(f"element {key}", "NaN in one environment only")
                continue
            statistic = max(statistic, abs(c[key] - a[key]))
            scale = max(scale, abs(a[key]))
        floor = FLOOR_FACTOR * scale
        out[field] = {
            "unit": field_units[field],
            "statistic": statistic,
            "floor": floor,
            "tolerance": max(statistic, floor),
            "elements": len(keys),
        }
    return out


def check_candidate(
    frozen: Mapping[str, Mapping[str, Any]],
    reference: Mapping[str, float],
    candidate_environment_id: str,
    candidate_runs: Mapping[str, Mapping[str, float]],
    *,
    field_of: Callable[[str], str],
) -> None:
    """Check a candidate environment's runs against the frozen per-field tolerance.

    The determinism precondition is asserted first; only a deterministic candidate reaches
    the tolerance comparison. An element whose field has no frozen tolerance is refused.
    """
    candidate = assert_deterministic(candidate_environment_id, candidate_runs)
    for key, value in reference.items():
        _require_finite_or_nan(f"reference at {key}", value)
    if set(candidate) != set(reference):
        raise IntegrityError(
            f"environment {candidate_environment_id}", "element set differs from the reference"
        )
    for key, ref in reference.items():
        field = field_of(key)
        if field not in frozen:
            raise IntegrityError(
                f"element {key}",
                f"field {field!r} has no frozen tolerance; it does not inherit one",
            )
        value = candidate[key]
        if math.isnan(ref) or math.isnan(value):
            if not (math.isnan(ref) and math.isnan(value)):
                raise ToleranceFailure(f"element {key}", "NaN in one of reference and candidate")
            continue
        limit = frozen[field]["tolerance"]
        if abs(value - ref) > limit:
            raise ToleranceFailure(
                f"element {key} ({frozen[field]['unit']})",
                f"|difference| {abs(value - ref)!r} exceeds field {field!r} tolerance {limit!r}",
            )


# =======================================================================================
# The governed field table (D-83 revision 8 section A8 item 10; PV-10 Rec 5)
# =======================================================================================
#
# A toleranced output's ledger entry in the fixture's identity declaration carries
# `fields`: a list of {field, locator, unit, meaning, citation}. `locator` is a regular
# expression matched in full against each element locator `numeric_fingerprint` produces.
# Every element must match exactly one declared field; an element matching none is
# refused (no field inherits another's floor), and one matching two is refused (the
# partition is ambiguous).

FIELD_KEYS: Final[tuple[str, ...]] = ("field", "locator", "unit", "meaning", "citation")


#: PV-10 Rec 12 (TEC-02): units and field-name tokens that mark a timestamp or an index.
#: Such a field is offset-dominated, so 2^-23 x max|x| would grant a large silent tolerance.
EXACT_ONLY_UNITS: Final[frozenset[str]] = frozenset(
    {"s_since_epoch", "unix_s", "epoch_s", "epoch", "timestamp", "utc", "index", "id"}
)
_EXACT_ONLY_NAME = re.compile(r"(^|_)(time|timestamp|epoch|utc|index|idx|id)(_|$)", re.I)


def _is_exact_only(name: str, unit: str) -> bool:
    return unit.strip().lower() in EXACT_ONLY_UNITS or bool(_EXACT_ONLY_NAME.search(name))


def validate_field_table(output: str, fields: Any) -> tuple[dict[str, Any], ...]:
    """Validate one output's declared field table; returns it as a tuple of entries."""
    resource = f"field table of {output}"
    if not isinstance(fields, Sequence) or isinstance(fields, str) or not fields:
        raise IntegrityError(
            resource,
            "a toleranced output declares a non-empty `fields` list; without it no element "
            "has a unit and no tolerance can be computed (D-83 revision 8 section A8 item 10)",
        )
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for index, entry in enumerate(fields):
        where = f"{resource}[{index}]"
        if not isinstance(entry, Mapping):
            raise IntegrityError(where, "a field entry is a mapping")
        missing = [k for k in FIELD_KEYS if not str(entry.get(k) or "").strip()]
        if missing:
            raise IntegrityError(where, f"field entry lacks {missing}; all of {FIELD_KEYS}")
        name = str(entry["field"])
        if name in seen:
            raise IntegrityError(where, f"field {name!r} is declared twice")
        seen.add(name)
        try:
            re.compile(str(entry["locator"]))
        except re.error as exc:
            raise IntegrityError(where, f"locator does not compile ({exc})") from exc
        if _is_exact_only(name, str(entry["unit"])):
            raise IntegrityError(
                where,
                f"field {name!r} (unit {entry['unit']!r}) is a timestamp or index field: such "
                "fields are exact-only and never floor-toleranced, because the floor scales "
                "with magnitude (epoch seconds near 1.67e9 would be granted about 199 s); "
                "compare them under D-74 exact_fields instead (GOV-2026-10-01-PV-10 Rec 12)",
            )
        out.append(dict(entry))
    return tuple(out)


def field_resolver(output: str, fields: Any) -> tuple[Callable[[str], str], dict[str, str]]:
    """`(field_of, field_units)` for one output's declared table."""
    table = validate_field_table(output, fields)
    compiled = [(str(e["field"]), re.compile(str(e["locator"]))) for e in table]
    units = {str(e["field"]): str(e["unit"]) for e in table}

    def field_of(locator: str) -> str:
        hits = [name for name, pattern in compiled if pattern.fullmatch(locator)]
        if not hits:
            raise IntegrityError(
                f"{output} element {locator}",
                "matches no declared field; a new field has no unit, floor or tolerance until "
                "it is declared in the governed field table (D-83 revision 8 section A8 "
                "item 10)",
            )
        if len(hits) > 1:
            raise IntegrityError(
                f"{output} element {locator}", f"matches more than one declared field {hits}"
            )
        return hits[0]

    return field_of, units


def compose_item11_tolerances(
    results: Sequence[Mapping[str, Any]],
    ledger: Mapping[str, Mapping[str, Any]],
    outputs: Sequence[str],
) -> dict[str, dict[str, Any]]:
    """The D-83 item 11 composition over recorded measuring results (the governed path).

    Groups the results by their recorded `environment_id`, requires exactly the (a) and (c)
    legs, asserts determinism per leg, and freezes a per-field tolerance for every
    toleranced output from that output's governed field table. A result without an
    `environment_id` (a pre-W-4 record) is refused by name (section A8 item 12).
    """
    grouped: dict[str, dict[str, Mapping[str, Any]]] = {}
    for result in results:
        run_id = str(result.get("measuring_run_id"))
        env = result.get("environment_id")
        if not isinstance(env, str) or not env.strip():
            raise IntegrityError(
                f"measuring result {run_id}",
                "carries no environment_id: a record made before W-4 is not comparable "
                "governed evidence, however similar its values (D-83 revision 8 section A8 "
                "item 12)",
            )
        grouped.setdefault(env, {})[run_id] = result
    if set(grouped) != {A_ENVIRONMENT, C_ENVIRONMENT}:
        raise IntegrityError(
            "item 11 composition",
            f"measuring results span environment_id {sorted(grouped)}; the item 11 tolerance "
            f"is composed over exactly {[A_ENVIRONMENT, C_ENVIRONMENT]}",
        )
    composed: dict[str, dict[str, Any]] = {}
    for output in outputs:
        entry = ledger.get(output) or {}
        field_of, field_units = field_resolver(output, entry.get("fields"))
        runs_by_env = {
            env: {rid: dict(r.get("fingerprints", {}).get(output, {})) for rid, r in runs.items()}
            for env, runs in grouped.items()
        }
        fields = freeze_tolerance(runs_by_env, field_of=field_of, field_units=field_units)
        composed[output] = {
            "fields": fields,
            "environment_ids": sorted(grouped),
            "measuring_run_ids": sorted(rid for runs in grouped.values() for rid in runs),
            "elements_compared": sum(f["elements"] for f in fields.values()),
        }
    return composed


def check_produced_output(
    output: str,
    reference: Mapping[str, float],
    produced: Mapping[str, float],
    *,
    produced_environment_id: str,
    fp_tolerance: Mapping[str, Any],
    fields: Any,
) -> dict[str, Any]:
    """Compare one produced output against its frozen reference under item 11.

    The producing environment must be one whose measuring runs satisfied the determinism
    precondition when the tolerance was frozen (`fp_tolerance.environment_ids`); otherwise
    the comparison is refused as a determinism failure, never rescued by the tolerance.
    """
    shown = fp_tolerance.get("environment_ids") or []
    if produced_environment_id not in shown:
        raise DeterminismFailure(
            f"{output} produced in {produced_environment_id!r}",
            f"the frozen tolerance was composed over {shown}; this environment has not shown "
            "determinism, so no tolerance applies to it (D-83 revision 8 section A8 item 9)",
        )
    frozen = fp_tolerance.get("fields")
    if not isinstance(frozen, Mapping) or not frozen:
        raise IntegrityError(f"{output}.fp_tolerance", "carries no per-field tolerances")
    field_of, _units = field_resolver(output, fields)
    for key, value in produced.items():
        _require_finite_or_nan(f"{output} produced at {key}", value)
    for key, value in reference.items():
        _require_finite_or_nan(f"{output} reference at {key}", value)
    if set(produced) != set(reference):
        raise IntegrityError(output, "produced element set differs from the frozen reference")
    worst: dict[str, float] = {}
    for key, ref in reference.items():
        field = field_of(key)
        if field not in frozen:
            raise IntegrityError(
                f"{output} element {key}", f"field {field!r} has no frozen tolerance"
            )
        value = produced[key]
        if math.isnan(ref) or math.isnan(value):
            if not (math.isnan(ref) and math.isnan(value)):
                raise ToleranceFailure(f"{output} element {key}", "NaN in only one of the two")
            continue
        limit = float(frozen[field]["tolerance"])
        diff = abs(value - ref)
        if diff > limit:
            raise ToleranceFailure(
                f"{output} element {key} ({frozen[field]['unit']})",
                f"|difference| {diff!r} exceeds field {field!r} tolerance {limit!r}",
            )
        worst[field] = max(worst.get(field, 0.0), diff)
    return {"fields_checked": sorted(worst), "max_difference_by_field": worst}
