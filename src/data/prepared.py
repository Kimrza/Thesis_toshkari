"""Target standardization: D-17's sixteen-field Phase 1 hourly target, and its guards.

Purpose
-------
The standardization engine for unit `target-standardization` (W-1 ... W-7; R-64 ... R-72).
It turns validated provider rows (the five-column gridded product: `ut1_unix`, `gdlat`,
`glon`, `tec`, `dtec`, plus the station key) into Phase 1 hourly target rows under D-17's
sixteen-field contract, applying EXACTLY the closed four-transformation set (R-64):

1. documented QC        -- the `configs/data.yaml` `qc_operations` list, a
                           `TBD — freeze gate` value TODAY (see the Q2 = A gate below);
2. UTC normalization    -- `interval_start_utc` derived from `ut1_unix`, hour start;
3. cell selection       -- D-1's floor rule, half-open `[floor, floor+1)` on both axes;
4. hourly aggregation   -- D-16's MEDIAN of the valid provider VTEC samples inside the
                           UTC hour for the station's frozen cell.

A fifth transformation FAILS. An aggregation statistic that does not resolve to D-16
FAILS. The excluded set is asserted, never substituted (R-67). Every row carries the
three definition IDs (R-70) and the lineage-caveat COLUMN (SD-T-02, Q1 = A), and every
artifact the write paths here produce carries the `location-sampled gridded VTEC` label
and the caveat beside it (R-69 limbs 2-3).

THE Q2 = A GATE (SD-T-01). While `configs/data.yaml`'s `qc_operations` is absent or
carries the literal `TBD — freeze gate`, `standardize_hourly_target` RAISES AND STOPS
before any output exists: no standardized target artifact is EVER produced by any path.
The raise names the field and the expectation that the list be FROZEN UNDER A D-NUMBER —
never mere non-emptiness, because a list filled by convenience satisfies "non-empty" and
is exactly what TE 18.2 forbids. The gate's scope is bound: it binds the run that
produces a standardized target, NOT the D-17 schema contract, the caveat column, or any
fixture exercise of either (those are properties of the writer, testable with no QC list
at all).

Inputs
------
Parsed provider rows and the PARSED `data.yaml` mapping (a `ConfigSnapshot.data` — this
module never reads `configs/` itself; `src/data/config.py` is the only module that does,
R-15). Threshold VALUES are read from config with their January–November basis carried
and are never inlined here (D-19; TC-03e); the CONTRACT SHAPES — the sixteen field
names, the four transformation identities, the four threshold statistic identities, the
excluded-set enumeration — are module constants citing their D-numbers, field and
statistic IDENTITIES rather than scientific values (the `REQUIRED_FIELDS_MAP`
precedent).

Re-run behaviour
----------------
Pure functions of their arguments plus explicit write paths. Importing this module has
no side effects. `standardize_hourly_target` is deterministic for identical inputs
(sorted grouping, `statistics.median`); the write paths overwrite their own outputs
byte-for-byte for identical inputs and never touch the experiment registry (the stage
script owns registry rows). No code path here constructs a path into the restricted
December evidence root, and no credential value is read or written; every written
payload routes through `acquisition.guard_egress` (NFR-SEC-01).

Governance
----------
* D-1 (cell rule), D-16 (median), D-17 (sixteen fields), D-19 (support thresholds) are
  APPLIED, never decided or reinterpreted here. Q2 = A and Q1 = A are the receipted
  code-generation answers.
* `StandardizationError` (declared in `src/data/config.py`, Q1 = A) is the failure class
  for every integrity condition of this unit; the two-tier posture holds — coverage
  shortfalls are recorded machine-readably, never fatal (R-71 content 3).
* The lineage-caveat column buys DETECTABILITY, not survival (SD-T-02, corrected): a
  consumer that subsets columns loses it, and only that consumer's own check can catch
  it. This module preserves the column through its OWN write paths (the round-trip test
  asserts that) and claims nothing beyond them.
* The float diff tolerance is a declared value read from the fixture manifest (TE 15.2)
  and is NEVER a library default; unset, `resolve_float_tolerance` stops naming the
  field.
* No numerical equivalence is claimed between the Phase 1 and Phase 2 targets anywhere
  in this module's outputs; the caveat states the fixed-protocol-replication bound.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import math
import statistics
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from src.data.acquisition import guard_egress
from src.data.config import TBD_SENTINEL, IntegrityError, StandardizationError
from src.data.release import MANIFEST_NAME, sha256_of_file, verify_release

__all__ = [
    "PROVIDER_COLUMNS",
    "load_released_provider_rows",
    "TARGET_LABEL",
    "LINEAGE_CAVEAT_FIELD",
    "LINEAGE_CAVEAT_TEXT",
    "ASYMMETRY_STATEMENT",
    "PERMITTED_TRANSFORMATIONS",
    "D16_STATISTIC",
    "D17_FIELDS",
    "DECLARED_EXCLUDED_SET",
    "D19_STATISTIC_CONTRACT",
    "D19_BASIS_WINDOW",
    "PHASE1_APPLICABLE_UNCERTAINTY_CONTENTS",
    "PHASE2_ONLY_UNCERTAINTY_CONTENTS",
    "TOLERANCE_MANIFEST_KEY",
    "TOLERANCE_MANIFEST_SUBKEY",
    "StandardizationResult",
    "assert_qc_operations_frozen",
    "assert_qc_operation_permitted",
    "assert_closed_transformation_set",
    "resolve_aggregation_statistic",
    "resolve_support_thresholds",
    "resolve_target_identity",
    "assert_d17_config_matches",
    "assert_row_conforms",
    "assert_excluded_absent",
    "assert_label_permitted",
    "assert_no_prohibited_phrasing",
    "cell_of",
    "cell_bounds",
    "hour_start_utc",
    "standardize_hourly_target",
    "build_coverage_report",
    "build_data_quality_block",
    "build_uncertainty_budget",
    "assert_budget_complete",
    "write_target_rows_csv",
    "read_target_rows_csv",
    "write_json_artifact",
    "resolve_float_tolerance",
    "verify_value_level",
]

# --- labelling and the lineage caveat (FR-P1-03-4, NFR-TDEF-01; R-69; SD-T-02) ----------

#: The ONLY permitted label for the Phase 1 target (FR-P1-03-4): never
#: "receiver-specific station-observed VTEC", everywhere it is described.
TARGET_LABEL: Final[str] = "location-sampled gridded VTEC"

#: Fragments whose presence in a label or output value is the prohibited phrasing.
#: Matched against machine-readable outputs by the grep-class check (R-69 limb 5).
_PROHIBITED_FRAGMENTS: Final[tuple[str, ...]] = ("station-observed", "receiver-specific")

#: The caveat travels as a COLUMN on every row, beside `target_definition_id` (Q1 = A).
LINEAGE_CAVEAT_FIELD: Final[str] = "lineage_caveat"

#: The two disclosures the column carries (SD-T-02), plus the cross-phase lineage bound
#: (R-69 limb 3): one fixed string so its loss or alteration is visible to a schema
#: check. It QUOTES the prohibited phrasing in negation, which is why the grep-class
#: check skips strings exactly equal to this constant.
LINEAGE_CAVEAT_TEXT: Final[str] = (
    "The Phase 1 target is location-sampled gridded VTEC (Madrigal cell), never "
    "receiver-specific station-observed VTEC, and it carries its own distinct "
    "target_definition_id. The Phase 1 grid-cell target population is not the Phase 2 "
    "IPP target population: no numerical equivalence between the Phase 1 and Phase 2 "
    "targets is claimed, and Phase 2 is a fixed-protocol replication on a new target "
    "lineage, not a second statistically independent blind test (Vision 2.2, 6.6). "
    "Part of any measured IRI or GIM difference is a geometry and sampling artefact "
    "rather than skill: Phase 1 compares a grid cell against a station-coordinate "
    "evaluation, Phase 2 an IPP cloud against a zenith estimate (Vision 6.6)."
)

#: FR-P1-05-10's asymmetry statement, quoted from the requirement.
ASYMMETRY_STATEMENT: Final[str] = (
    "A slowly varying per-station-day bias partially cancels in the paired difference "
    "but does not cancel in the derived percentage summary, because it inflates the "
    "reference denominator."
)

# --- the closed transformation set (FR-P1-03-1; R-64; D-1, D-16) ------------------------

#: Exactly four permitted transformations — identities, not scientific values. A fifth
#: entry in any declared ledger FAILS (R-64); an operation outside the frozen QC list
#: fails like a fifth transformation.
PERMITTED_TRANSFORMATIONS: Final[tuple[str, ...]] = (
    "documented_qc",
    "utc_normalization",
    "cell_selection",
    "hourly_aggregation",
)

#: D-16's frozen aggregation statistic identity and its decision citation. The VALUE the
#: run uses is resolved from config and must equal this identity citing this decision
#: (R-65); a run cannot proceed on a default.
D16_STATISTIC: Final[str] = "median"
_D16_DECISION: Final[str] = "D-16"

# --- D-17's sixteen-field row contract (FR-P1-03-5; R-66; W-3) --------------------------

#: The sixteen fields, in D-17's enumeration order. Field IDENTITIES, never values.
#: Where the conformance check reads the frozen set FROM is the open authority question
#: (`governance-guards` R-20's shape), carried to the gate: this constant is the in-code
#: representation of D-17's enumeration, and `assert_d17_config_matches` asserts the
#: CONFIG set equals it before any row is compared, so a config drift and a row defect
#: fail differently and say which layer broke.
D17_FIELDS: Final[tuple[str, ...]] = (
    "interval_start_utc",
    "station_id",
    "cell_gdlat",
    "cell_glon",
    "cell_lat_bounds",
    "cell_lon_bounds",
    "vtec_tecu",
    "valid_observation_count",
    "within_hour_spread_tecu",
    "largest_internal_gap_s",
    "provider_dtec_summary",
    "aggregation_config_id",
    "target_valid",
    "phase_id",
    "source_id",
    "target_definition_id",
)
_D17_DECISION: Final[str] = "D-17"

#: D-17's excluded set: eight classes, NEVER present and NEVER substituted (R-67).
#: "None is derivable from a five-column gridded product" — audited 2026-08-21 across
#: all twelve request manifests. A run that finds a different declared set FAILS; it
#: does not adopt the set it found.
DECLARED_EXCLUDED_SET: Final[tuple[str, ...]] = (
    "valid_satellite_count",
    "per-satellite or per-IPP quantities",
    "zenith angle or weight",
    "elevation",
    "DCB",
    "STEC",
    "mapping function output",
    "arc or cycle-slip statistics",
)

#: Field-name tokens and compounds that mark an excluded-class field on a row. This is
#: this unit's own D-17-shaped check (R-67); `governance-guards` R-23's produced-field
#: limb guards the same boundary INDEPENDENTLY and neither substitutes for the other —
#: two checks on that boundary is the design's intent, not duplication.
_EXCLUDED_TOKENS: Final[frozenset[str]] = frozenset(
    {
        "satellite",
        "sat",
        "prn",
        "dcb",
        "stec",
        "slant",
        "mapping",
        "arc",
        "elevation",
        "elev",
        "zenith",
        "zen",
        "ipp",
    }
)
_EXCLUDED_COMPOUNDS: Final[tuple[str, ...]] = (
    "cycle_slip",
    "n_sat",
    "sat_count",
    "mapping_function",
)

# --- D-19's support thresholds: statistic identities and the basis rule (R-68) ----------

#: The four D-19 threshold rows: statistic identity and role. VALUES are never inlined —
#: they are read from config carrying their measured basis (a threshold without its
#: basis is indistinguishable from a chosen one, and FAILS). `provider_dtec_summary`'s
#: threshold is a FLAG, not a validity bound (D-19).
D19_STATISTIC_CONTRACT: Final[Mapping[str, Mapping[str, str]]] = {
    "valid_observation_count": {"statistic": "minimum", "role": "validity"},
    "within_hour_spread_tecu": {"statistic": "range", "role": "validity"},
    "largest_internal_gap_s": {"statistic": "maximum", "role": "validity"},
    "provider_dtec_summary": {"statistic": "median", "role": "flag"},
}
_D19_DECISION: Final[str] = "D-19"

#: D-19's stated measurement window — a provenance label, not a scientific value.
#: December is excluded BY CONSTRUCTION: a basis that references December is refused,
#: because December must never inform a threshold (the trigger is December being SEEN,
#: not the lock being opened).
D19_BASIS_WINDOW: Final[str] = "January-November 2022"
_DECEMBER_MARKERS: Final[tuple[str, ...]] = ("december", "2022-12")

# --- the uncertainty budget's content sets (FR-P1-05-10; R-72; W-4/W-7) -----------------

#: The two Vision 6.9 contents the five-column product can yield, named from D-17's own
#: uncertainty-bearing fields (provider `dtec`; within-hour aggregation spread).
PHASE1_APPLICABLE_UNCERTAINTY_CONTENTS: Final[tuple[str, ...]] = (
    "provider_reported_uncertainty",
    "within_hour_aggregation_spread",
)

#: The four Vision 6.9 contents that are Phase 2 quantities (per satellite, per IPP, or
#: geometry): recorded not-applicable WITH their reason, never emitted empty. Content
#: DESCRIPTIONS (values), never field names, so no excluded token enters a field name.
PHASE2_ONLY_UNCERTAINTY_CONTENTS: Final[tuple[str, ...]] = (
    "per-satellite residual spread",
    "per-IPP sampling dispersion",
    "zenith and elevation geometry uncertainty",
    "mapping-function contribution",
)

_PHASE2_CONTENT_REASON: Final[str] = (
    "a Phase 2 quantity: not derivable from the five-column gridded product "
    "(ut1_unix, gdlat, glon, tec, dtec; D-17 audit 2026-08-21) — recorded "
    "not-applicable rather than emitted empty (R-72)"
)

# --- the fixture-manifest tolerance (TE 15.2; SD-T-03) ----------------------------------

#: Where the value-level diff tolerance lives: the fixture manifest's permitted
#: floating-point tolerances (TE 15.2). It is a DECLARED value; unset, the diff STOPS
#: naming this field — never a `numpy.isclose` default.
TOLERANCE_MANIFEST_KEY: Final[str] = "permitted_floating_point_tolerances"
TOLERANCE_MANIFEST_SUBKEY: Final[str] = "value_level_diff_tecu"


#: The five provider columns plus the station key — the entire input surface (D-17).
PROVIDER_COLUMNS: Final[tuple[str, ...]] = (
    "station",
    "ut1_unix",
    "gdlat",
    "glon",
    "tec",
    "dtec",
)


def load_released_provider_rows(release_root: Path) -> list[dict[str, str]]:
    """Consume released provider input by release manifest and hash — never bare path.

    Every candidate release under the release root is verified through
    `release.verify_release`; each consumed CSV's bytes are re-hashed against the
    manifest's recorded digest before a row is read; every consumed file must carry
    exactly the five provider columns plus the station key (R-44; D-17). No released
    provider input existing is an integrity refusal, never a fabricated empty input.

    Raises
    ------
    IntegrityError
        naming the release root when no released provider input exists, or the file
        and violated expectation on any verification failure.
    """
    release_root = Path(release_root)
    manifests = sorted(release_root.rglob(MANIFEST_NAME)) if release_root.is_dir() else []
    if not manifests:
        raise IntegrityError(
            release_root,
            "no released provider input exists under the release root; the "
            "standardization consumes releases by manifest and hash (R-44), never "
            "bare paths, and none has been produced — refusing rather than "
            "fabricating input",
        )
    rows: list[dict[str, str]] = []
    for manifest_path in manifests:
        problems = verify_release(manifest_path)
        if problems:
            raise IntegrityError(
                manifest_path,
                "release failed verification before consumption: " + "; ".join(problems),
            )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        output_files = manifest.get("output_files")
        if not isinstance(output_files, Mapping):
            raise IntegrityError(
                manifest_path,
                "release manifest carries no output_files mapping; input is consumed "
                "by recorded digest and there is nothing recorded to consume",
            )
        for rel_path, recorded_digest in sorted(output_files.items()):
            if not str(rel_path).lower().endswith(".csv"):
                continue
            artifact = manifest_path.parent / str(rel_path)
            actual = sha256_of_file(artifact)
            if actual != str(recorded_digest):
                raise IntegrityError(
                    artifact,
                    f"FAILED hash check before consumption (recorded "
                    f"{recorded_digest}, actual {actual}); never continue silently "
                    f"past a failed hash",
                )
            with artifact.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                header = tuple(reader.fieldnames or ())
                if sorted(header) != sorted(PROVIDER_COLUMNS):
                    raise IntegrityError(
                        artifact,
                        f"released input carries columns {sorted(header)}, expected "
                        f"exactly the five provider columns plus the station key "
                        f"{sorted(PROVIDER_COLUMNS)} (D-17)",
                    )
                rows.extend(dict(row) for row in reader)
    return rows


# =======================================================================================
# Config-facing resolvers and refusals
# =======================================================================================


def assert_qc_operations_frozen(data_config: Mapping[str, Any]) -> Mapping[str, Any]:
    """The Q2 = A refuse-to-RUN gate (SD-T-01): frozen under a D-number, or STOP.

    Refuses while `qc_operations` is absent, carries the literal `TBD — freeze gate`,
    or is present without a D-number citation and a non-empty operations list. The
    expectation named is FROZEN UNDER A D-NUMBER — never mere non-emptiness, because a
    list filled by convenience satisfies "non-empty" and is exactly what TE 18.2
    forbids. While this raises, no standardized target artifact is produced by any
    path.

    Raises
    ------
    StandardizationError
        naming `configs/data.yaml`'s `qc_operations` field and the frozen-under-a-
        D-number expectation.
    """

    def _refuse(state: str) -> StandardizationError:
        return StandardizationError(
            "configs/data.yaml qc_operations",
            f"the documented-QC operation list is {state}; the closed four-"
            f"transformation set (FR-P1-03-1) cannot be closed until the list is "
            f"FROZEN UNDER A D-NUMBER by the supervisor freeze — never mere "
            f"non-emptiness, since a list filled by convenience satisfies "
            f"'non-empty' and is exactly what TE 18.2 forbids. Under Q2 = A this "
            f"run REFUSES and no standardized target artifact is produced",
        )

    node = data_config.get("qc_operations")
    if node is None:
        raise _refuse("absent")
    if isinstance(node, str):
        if node.strip() == TBD_SENTINEL:
            raise _refuse(f"the literal {TBD_SENTINEL!r}")
        raise _refuse(f"a bare string ({node!r}) rather than a frozen, cited list")
    if not isinstance(node, Mapping):
        raise _refuse(f"of type {type(node).__name__}, not a mapping")
    operations = node.get("operations")
    decision = str(node.get("decision", "") or "")
    if not isinstance(operations, list | tuple) or not operations:
        raise _refuse("present without a non-empty enumerated operations list")
    if not _is_d_number(decision):
        raise _refuse("present without a D-number citation recording its freeze")
    return node


def _is_d_number(text: str) -> bool:
    """True for a `D-<digits>` citation (optionally dotted, e.g. `D-10.2`)."""
    if not text.startswith("D-"):
        return False
    body = text[2:]
    return (
        bool(body)
        and all(part.isdigit() for part in body.split(".") if part != "")
        and (body.replace(".", "").isdigit())
    )


def assert_qc_operation_permitted(operation: str, frozen_qc: Mapping[str, Any]) -> None:
    """An operation outside the frozen QC list fails LIKE A FIFTH TRANSFORMATION (R-64).

    Raises
    ------
    StandardizationError
        naming the operation and the frozen list it is absent from.
    """
    operations = [str(op) for op in frozen_qc.get("operations", ())]
    if operation not in operations:
        raise StandardizationError(
            f"qc operation {operation!r}",
            f"absent from the frozen qc_operations list {operations!r} "
            f"({frozen_qc.get('decision', 'no decision cited')}); an operation outside "
            f"the enumerated list fails like a fifth transformation would (R-64)",
        )


def assert_closed_transformation_set(applied: Iterable[str]) -> None:
    """R-64: the applied set is EXACTLY the four permitted transformations, no fifth.

    Raises
    ------
    StandardizationError
        naming every unenumerated transformation, or any permitted one that is
        missing — "only the documented transformations" is a closed-set claim, and an
        open-ended diff cannot express it.
    """
    applied_list = [str(item) for item in applied]
    extra = sorted(set(applied_list) - set(PERMITTED_TRANSFORMATIONS))
    missing = sorted(set(PERMITTED_TRANSFORMATIONS) - set(applied_list))
    if extra:
        raise StandardizationError(
            ", ".join(extra),
            "a fifth transformation beyond the closed four-member set (documented QC, "
            "UTC normalization, D-1 cell selection, D-16 hourly aggregation); "
            "FR-P1-03-1 permits exactly four and a fifth is a FAILURE, not something "
            "a reviewer must notice (R-64)",
        )
    if missing:
        raise StandardizationError(
            ", ".join(missing),
            "the declared transformation ledger omits (a) permitted transformation(s); "
            "the closed set has exactly four members and the ledger must enumerate "
            "all of them for the value-level diff to attribute every change (R-64)",
        )


def resolve_aggregation_statistic(data_config: Mapping[str, Any]) -> str:
    """R-65: the statistic resolves from config CITING D-16; a run never runs a default.

    Raises
    ------
    StandardizationError
        when `target.aggregation` is absent (a recorded default would satisfy the
        words and not the purpose); when the citation is not D-16; or when the
        configured statistic is not D-16's median (e.g. a mean, or a zenith-weighted
        statistic — deferred as not computable, with nothing substituted).
    """
    target_node = data_config.get("target")
    node = target_node.get("aggregation") if isinstance(target_node, Mapping) else None
    if not isinstance(node, Mapping):
        raise StandardizationError(
            "configs/data.yaml target.aggregation",
            "absent or not a mapping; the aggregation statistic must RESOLVE from "
            "config citing D-16 and a run cannot proceed on a default (R-65, "
            "FR-P1-03-1 second limb)",
        )
    statistic = str(node.get("statistic", "") or "")
    decision = str(node.get("decision", "") or "")
    if decision != _D16_DECISION:
        raise StandardizationError(
            "configs/data.yaml target.aggregation.decision",
            f"the configured statistic cites {decision!r}, not {_D16_DECISION}; a "
            f"statistic without its D-16 citation is a recorded default and the run "
            f"refuses rather than proceeding on it (R-65)",
        )
    if statistic != D16_STATISTIC:
        raise StandardizationError(
            "configs/data.yaml target.aggregation.statistic",
            f"configured statistic {statistic!r} does not resolve to D-16's "
            f"{D16_STATISTIC!r}; zenith-weighted aggregation is deferred as not "
            f"computable and nothing is substituted (R-65) — a non-D-16 statistic "
            f"FAILS",
        )
    return statistic


def resolve_support_thresholds(
    data_config: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    """R-68: D-19's four thresholds, read from config WITH their measured basis carried.

    Each entry must carry its statistic identity (matching D-19's enumeration), its
    value, a non-empty measured basis, the January–November basis window, and the D-19
    citation. A threshold without its basis is indistinguishable from a chosen one and
    FAILS; a December-informed basis FAILS (December must never inform a threshold —
    the trigger is December being SEEN).

    Raises
    ------
    StandardizationError
        naming the offending field and the violated expectation.
    """
    target_node = data_config.get("target")
    node = target_node.get("support_thresholds") if isinstance(target_node, Mapping) else None
    if not isinstance(node, Mapping):
        raise StandardizationError(
            "configs/data.yaml target.support_thresholds",
            "absent or not a mapping; D-19's four support thresholds are read from "
            "config with their January-November basis carried, never inlined in "
            "source (R-68, TC-03e)",
        )
    resolved: dict[str, dict[str, Any]] = {}
    for field, contract in D19_STATISTIC_CONTRACT.items():
        entry = node.get(field)
        if not isinstance(entry, Mapping):
            raise StandardizationError(
                f"configs/data.yaml target.support_thresholds.{field}",
                "absent; every one of D-19's four threshold rows must be present "
                "with statistic, value, basis, basis_window and decision (R-68)",
            )
        statistic = str(entry.get("statistic", "") or "")
        if statistic != contract["statistic"]:
            raise StandardizationError(
                f"configs/data.yaml target.support_thresholds.{field}.statistic",
                f"configured statistic {statistic!r} does not match D-19's "
                f"{contract['statistic']!r} for this field; the config drifted from "
                f"the decision that froze it",
            )
        value = entry.get("value")
        if isinstance(value, str) and value.strip() == TBD_SENTINEL:
            raise StandardizationError(
                f"configs/data.yaml target.support_thresholds.{field}.value",
                f"carries the literal {TBD_SENTINEL!r}; the value is D-19's to "
                f"transcribe and no implementer fills it by convenience",
            )
        if not isinstance(value, int | float) or isinstance(value, bool):
            raise StandardizationError(
                f"configs/data.yaml target.support_thresholds.{field}.value",
                f"expected a number, got {value!r}",
            )
        basis = str(entry.get("basis", "") or "")
        if not basis:
            raise StandardizationError(
                f"configs/data.yaml target.support_thresholds.{field}.basis",
                "empty; a threshold without its measured basis is indistinguishable "
                "from a chosen one and FAILS (R-68)",
            )
        basis_window = str(entry.get("basis_window", "") or "")
        if basis_window != D19_BASIS_WINDOW:
            raise StandardizationError(
                f"configs/data.yaml target.support_thresholds.{field}.basis_window",
                f"expected D-19's stated window {D19_BASIS_WINDOW!r}, got "
                f"{basis_window!r}; December is excluded by construction",
            )
        joined = f"{basis} {basis_window}".lower()
        if any(marker in joined for marker in _DECEMBER_MARKERS):
            raise StandardizationError(
                f"configs/data.yaml target.support_thresholds.{field}.basis",
                "references December; December must never inform a threshold — the "
                "trigger is December being SEEN, not the lock being opened",
            )
        decision = str(entry.get("decision", "") or "")
        if decision != _D19_DECISION:
            raise StandardizationError(
                f"configs/data.yaml target.support_thresholds.{field}.decision",
                f"cites {decision!r}, not {_D19_DECISION}; the threshold's freeze "
                f"citation must travel with its value",
            )
        resolved[field] = {
            "statistic": statistic,
            "role": contract["role"],
            "value": float(value),
            "basis": basis,
            "basis_window": basis_window,
        }
    return resolved


def resolve_target_identity(data_config: Mapping[str, Any]) -> dict[str, str]:
    """The three definition IDs, resolved from config — never invented here (R-70).

    Raises
    ------
    StandardizationError
        when any of `phase_id`, `source_id`, `target_definition_id` is absent, empty
        or `TBD — freeze gate` under `target.identity`.
    """
    target_node = data_config.get("target")
    node = target_node.get("identity") if isinstance(target_node, Mapping) else None
    if not isinstance(node, Mapping):
        raise StandardizationError(
            "configs/data.yaml target.identity",
            "absent; phase_id, source_id and target_definition_id are stamped on "
            "every artifact (R-70, TE 13) and their values are resolved from config, "
            "never invented by an implementer",
        )
    identity: dict[str, str] = {}
    for key in ("phase_id", "source_id", "target_definition_id"):
        value = str(node.get(key, "") or "")
        if not value or value.strip() == TBD_SENTINEL:
            raise StandardizationError(
                f"configs/data.yaml target.identity.{key}",
                "absent, empty or unresolved; every dataset, prediction, mask and "
                "comparison carries all three definition IDs (R-70)",
            )
        identity[key] = value
    return identity


def assert_d17_config_matches(data_config: Mapping[str, Any]) -> tuple[str, ...]:
    """W-3 steps 1-2: the CONFIG field set equals D-17 — before any row is compared.

    A config-sourced field list can drift from the decision that froze it, and then
    every row passes against the wrong contract. This assertion makes a config drift
    and a row defect FAIL DIFFERENTLY: this raise says the CONFIG drifted;
    `assert_row_conforms` says the ROW is wrong. Where the check reads D-17 FROM is
    the open authority question (`governance-guards` R-20's shape), carried to the
    gate; no third option is invented here.

    Raises
    ------
    StandardizationError
        when `target.contract` is absent, its field set is not exactly D-17's
        sixteen, its excluded set differs from D-17's declared eight classes (never
        adopted — R-67), or its citation is not D-17.
    """
    target_node = data_config.get("target")
    node = target_node.get("contract") if isinstance(target_node, Mapping) else None
    if not isinstance(node, Mapping):
        raise StandardizationError(
            "configs/data.yaml target.contract",
            "absent; the D-17 field contract is read from config and asserted equal "
            "to D-17's enumeration before any row is compared (R-66)",
        )
    fields = [str(f) for f in node.get("fields", ()) or ()]
    if sorted(fields) != sorted(D17_FIELDS) or len(fields) != len(D17_FIELDS):
        raise StandardizationError(
            "configs/data.yaml target.contract.fields",
            f"the CONFIG drifted from D-17: expected exactly the {len(D17_FIELDS)} "
            f"frozen fields, got {len(fields)} "
            f"(missing: {sorted(set(D17_FIELDS) - set(fields))}, "
            f"extra: {sorted(set(fields) - set(D17_FIELDS))}); every row would pass "
            f"against the wrong contract, so this fails BEFORE any row is read (R-66)",
        )
    excluded = [str(f) for f in node.get("excluded", ()) or ()]
    if sorted(excluded) != sorted(DECLARED_EXCLUDED_SET):
        raise StandardizationError(
            "configs/data.yaml target.contract.excluded",
            f"the declared excluded set differs from D-17's eight classes "
            f"(missing: {sorted(set(DECLARED_EXCLUDED_SET) - set(excluded))}, "
            f"extra: {sorted(set(excluded) - set(DECLARED_EXCLUDED_SET))}); the "
            f"excluded set is ASSERTED, never substituted — a run that finds a "
            f"different set FAILS and does not adopt it (R-67)",
        )
    decision = str(node.get("decision", "") or "")
    if decision != _D17_DECISION:
        raise StandardizationError(
            "configs/data.yaml target.contract.decision",
            f"cites {decision!r}, not {_D17_DECISION}; the contract's freeze citation "
            f"must travel with the field set",
        )
    return tuple(fields)


# =======================================================================================
# Row-level checks
# =======================================================================================


def _field_tokens(field_name: str) -> frozenset[str]:
    out: set[str] = set()
    token = []
    for char in field_name.lower():
        if char.isalnum():
            token.append(char)
        elif token:
            out.add("".join(token))
            token = []
    if token:
        out.add("".join(token))
    return frozenset(out)


def assert_excluded_absent(field_names: Iterable[str]) -> None:
    """R-67: no field of D-17's excluded classes is present, under any spelling.

    Token and compound matching, so a renamed column (`n_sat_valid`, `zen_wt`) cannot
    walk past an exact-name list. `governance-guards` R-23's produced-field limb
    guards the same boundary independently; neither substitutes for the other.

    Raises
    ------
    StandardizationError
        naming every offending field.
    """
    offenders = sorted(
        name
        for name in (str(n) for n in field_names)
        if _field_tokens(name) & _EXCLUDED_TOKENS
        or any(compound in name.lower() for compound in _EXCLUDED_COMPOUNDS)
    )
    if offenders:
        raise StandardizationError(
            ", ".join(offenders),
            "field(s) of D-17's excluded set (valid_satellite_count, per-satellite or "
            "per-IPP quantities, zenith angle or weight, elevation, DCB, STEC, "
            "mapping function output, arc or cycle-slip statistics) are present on a "
            "Phase 1 target row; none is derivable from the five-column gridded "
            "product and nothing is substituted (R-67, D-17)",
        )


def assert_row_conforms(row: Mapping[str, Any]) -> None:
    """W-3 step 3: the ROW check — sixteen fields, the caveat column, the three IDs.

    The row carries exactly D-17's sixteen fields PLUS the lineage-caveat column
    (Q1 = A: the caveat is a declared companion carrier required by NFR-TDEF-01, not
    an "additional field" in R-66's sense — the D-17 count stays sixteen). Any other
    extra field fails; any excluded-class field fails; an empty definition-ID stamp
    fails; an absent or altered caveat fails, because the writing path emits it and a
    target artifact must not exist without it (R-69).

    Raises
    ------
    StandardizationError
        saying the ROW is wrong and naming the defect.
    """
    names = {str(name) for name in row}
    missing = sorted(set(D17_FIELDS) - names)
    if missing:
        raise StandardizationError(
            f"target row missing {', '.join(missing)}",
            f"the ROW is wrong: D-17's contract is exactly {len(D17_FIELDS)} fields — "
            f"not fifteen, not seventeen — and every one must be present (R-66)",
        )
    extra = sorted(names - set(D17_FIELDS) - {LINEAGE_CAVEAT_FIELD})
    if extra:
        raise StandardizationError(
            f"target row carries {', '.join(extra)}",
            "the ROW is wrong: a field beyond D-17's sixteen (plus the declared "
            "lineage-caveat column) fails; an additional field is where a Phase 2 "
            "quantity would appear (R-66, R-67)",
        )
    assert_excluded_absent(names)
    for key in ("phase_id", "source_id", "target_definition_id"):
        if not str(row.get(key, "") or ""):
            raise StandardizationError(
                f"target row field {key}",
                "empty; every dataset, prediction, mask and comparison carries "
                "phase_id, source_id and target_definition_id (R-70, TE 13)",
            )
    caveat = str(row.get(LINEAGE_CAVEAT_FIELD, "") or "")
    if caveat != LINEAGE_CAVEAT_TEXT:
        raise StandardizationError(
            f"target row field {LINEAGE_CAVEAT_FIELD}",
            "absent or altered; the grid-cell-versus-IPP lineage caveat travels as a "
            "column on every row beside target_definition_id, emitted by the "
            "target-writing path, and a target artifact written without it FAILS "
            "(R-69 limb 3, NFR-TDEF-01, Q1 = A)",
        )


def assert_label_permitted(label: str) -> None:
    """FR-P1-03-4: the product is labelled location-sampled gridded VTEC, and only that.

    Raises
    ------
    StandardizationError
        when the label is not exactly `TARGET_LABEL`, or carries the prohibited
        receiver-specific / station-observed phrasing.
    """
    lowered = label.lower()
    if any(fragment in lowered for fragment in _PROHIBITED_FRAGMENTS):
        raise StandardizationError(
            f"target label {label!r}",
            f"carries prohibited phrasing; the Phase 1 gridded product is NEVER "
            f"labelled receiver-specific station-observed VTEC — it is "
            f"{TARGET_LABEL!r}, everywhere it is described (FR-P1-03-4)",
        )
    if label != TARGET_LABEL:
        raise StandardizationError(
            f"target label {label!r}",
            f"is not the frozen label {TARGET_LABEL!r}; the label is emitted by the "
            f"writing path so an artifact cannot be described without it (R-69)",
        )


def assert_no_prohibited_phrasing(obj: object, *, context: str = "output") -> None:
    """R-69 limb 5: the grep-class check over machine-readable output VALUES.

    Skips strings exactly equal to `LINEAGE_CAVEAT_TEXT`, which quotes the prohibited
    phrasing in negation — the caveat is the disclosure, not a mislabelling.

    Raises
    ------
    StandardizationError
        naming the context in which prohibited phrasing appears.
    """
    if isinstance(obj, str):
        if obj == LINEAGE_CAVEAT_TEXT:
            return
        lowered = obj.lower()
        if any(fragment in lowered for fragment in _PROHIBITED_FRAGMENTS):
            raise StandardizationError(
                context,
                f"machine-readable output contains prohibited phrasing "
                f"({'/'.join(_PROHIBITED_FRAGMENTS)}); the Phase 1 target is "
                f"{TARGET_LABEL!r} and is never described as receiver-specific "
                f"station-observed VTEC (FR-P1-03-4, R-69 grep-class check)",
            )
        return
    if isinstance(obj, Mapping):
        for key, value in obj.items():
            key_context = f"{context}.{key}" if isinstance(key, str) else context
            assert_no_prohibited_phrasing(key, context=key_context)
            assert_no_prohibited_phrasing(value, context=key_context)
        return
    if isinstance(obj, list | tuple | set | frozenset):
        for index, value in enumerate(obj):
            assert_no_prohibited_phrasing(value, context=f"{context}[{index}]")


# =======================================================================================
# The four transformations
# =======================================================================================


def cell_of(gdlat: float, glon: float) -> tuple[int, int]:
    """D-1's cell selection: `cell = (floor(lat), floor(lon))`, half-open on both axes."""
    return (math.floor(gdlat), math.floor(glon))


def cell_bounds(index: int) -> str:
    """D-1's half-open bounds string for one axis: `[floor, floor+1)`."""
    return f"[{index}, {index + 1})"


def hour_start_utc(ut1_unix: float) -> str:
    """UTC normalization: the ISO hour start `[h, h+1)` containing `ut1_unix`."""
    hour = int(ut1_unix // 3600) * 3600
    stamp = dt.datetime.fromtimestamp(hour, dt.UTC)
    return stamp.strftime("%Y-%m-%dT%H:00:00Z")


def _parse_float(record: Mapping[str, Any], key: str) -> float:
    raw = record.get(key)
    if raw is None or (isinstance(raw, str) and not raw.strip()):
        raise StandardizationError(
            f"provider record field {key}",
            "missing or empty; the five-column product carries ut1_unix, gdlat, "
            "glon, tec and dtec on every record, and a record whose value cannot be "
            "established cannot be standardized — fail closed, never guess",
        )
    try:
        return float(raw)
    except (TypeError, ValueError) as exc:
        raise StandardizationError(
            f"provider record field {key}",
            f"unparseable value {raw!r}; provider values are preserved, never "
            f"repaired ({exc})",
        ) from exc


# =======================================================================================
# The standardization engine
# =======================================================================================


@dataclass(frozen=True)
class StandardizationResult:
    """What one standardization run establishes: rows, coverage, quality, budget."""

    rows: Sequence[Mapping[str, Any]]
    coverage_report: Mapping[str, Any]
    data_quality: Mapping[str, Any]
    uncertainty_budget: Mapping[str, Any]
    identity: Mapping[str, str]
    statistic: str
    thresholds: Mapping[str, Mapping[str, Any]]


def standardize_hourly_target(
    provider_rows: Sequence[Mapping[str, Any]],
    *,
    data_config: Mapping[str, Any],
    aggregation_config_id: str,
    negative_vtec_explanations: Mapping[str, str] | None = None,
    applied_transformations: Iterable[str] = PERMITTED_TRANSFORMATIONS,
) -> StandardizationResult:
    """W-1: the target-producing run. REFUSES FIRST while the QC list is unfrozen.

    Order is the rule: the Q2 = A gate fires before anything else — before input
    validation, before any aggregation, before any output could exist — so no
    standardized target artifact is ever produced while `qc_operations` is
    `TBD — freeze gate` or absent. Then the closed transformation set, the D-16
    statistic, the D-19 thresholds, the D-17 contract and the three IDs are resolved
    from config (never defaulted), and exactly the four permitted transformations are
    applied.

    `negative_vtec_explanations` maps `"<station>:<ut1_unix>"` to a recorded
    explanation: an EXPLAINED negative VTEC is accepted with its explanation recorded
    in the data-quality block; an UNEXPLAINED one is rejected — a negative VTEC is not
    a small value but an impossible one (R-71 content 2).

    Raises
    ------
    StandardizationError
        the Q2 = A refusal; a fifth transformation; a non-D-16 statistic; a config or
        row contract defect; an unexplained negative VTEC; an empty
        `aggregation_config_id`.
    """
    assert_qc_operations_frozen(data_config)  # Q2 = A: ALWAYS first
    # The validated list closes the ledger's "documented_qc" member: an operation
    # outside it fails like a fifth transformation via assert_qc_operation_permitted.
    assert_closed_transformation_set(applied_transformations)
    statistic = resolve_aggregation_statistic(data_config)
    thresholds = resolve_support_thresholds(data_config)
    identity = resolve_target_identity(data_config)
    assert_d17_config_matches(data_config)
    if not aggregation_config_id:
        raise StandardizationError(
            "aggregation_config_id",
            "empty; every row records which frozen configuration produced its "
            "aggregation (D-17 field 12)",
        )

    explanations = dict(negative_vtec_explanations or {})
    explained_negatives: list[dict[str, str]] = []

    groups: dict[tuple[str, int, int, int], list[dict[str, float]]] = {}
    for record in provider_rows:
        station = str(record.get("station", "") or "")
        if not station:
            raise StandardizationError(
                "provider record field station",
                "missing; the station key is assigned by D-1's cell rule upstream "
                "and every record must carry it",
            )
        ut1 = _parse_float(record, "ut1_unix")
        gdlat = _parse_float(record, "gdlat")
        glon = _parse_float(record, "glon")
        tec = _parse_float(record, "tec")
        dtec = _parse_float(record, "dtec")
        if tec < 0:
            key = f"{station}:{record.get('ut1_unix')}"
            explanation = explanations.get(key, "")
            if not explanation:
                raise StandardizationError(
                    f"provider record {key}",
                    f"carries a negative VTEC ({tec}) with no recorded explanation; "
                    f"a negative VTEC is not a small value but an impossible one — "
                    f"an unexplained negative is REJECTED, never accepted quietly "
                    f"(R-71 content 2, NFR-DQ-01)",
                )
            explained_negatives.append({"record": key, "explanation": explanation})
        cell = cell_of(gdlat, glon)  # transformation 3: cell selection (D-1)
        hour = int(ut1 // 3600)  # transformation 2: UTC normalization
        groups.setdefault((station, cell[0], cell[1], hour), []).append(
            {"ut1_unix": ut1, "tec": tec, "dtec": dtec}
        )

    rows: list[dict[str, Any]] = []
    invalid_reasons: dict[str, list[str]] = {}
    dtec_flags: list[str] = []
    for (station, cell_lat, cell_lon, hour), samples in sorted(groups.items()):
        samples.sort(key=lambda s: s["ut1_unix"])
        tec_values = [s["tec"] for s in samples]
        dtec_values = [s["dtec"] for s in samples]
        stamps = [s["ut1_unix"] for s in samples]
        # transformation 4: D-16's median hourly aggregation
        vtec = statistics.median(tec_values)
        spread = max(tec_values) - min(tec_values)
        gaps = [b - a for a, b in zip(stamps, stamps[1:], strict=False)]
        largest_gap = max(gaps) if gaps else 0.0
        dtec_summary = statistics.median(dtec_values)
        count = len(samples)

        row_key = f"{station}:{cell_lat}:{cell_lon}:{hour_start_utc(hour * 3600)}"
        reasons: list[str] = []
        if count < thresholds["valid_observation_count"]["value"]:
            reasons.append(
                f"valid_observation_count {count} below D-19 minimum "
                f"{thresholds['valid_observation_count']['value']}"
            )
        if spread > thresholds["within_hour_spread_tecu"]["value"]:
            reasons.append(
                f"within_hour_spread_tecu {spread} above D-19 range bound "
                f"{thresholds['within_hour_spread_tecu']['value']}"
            )
        if largest_gap > thresholds["largest_internal_gap_s"]["value"]:
            reasons.append(
                f"largest_internal_gap_s {largest_gap} above D-19 maximum "
                f"{thresholds['largest_internal_gap_s']['value']}"
            )
        if reasons:
            invalid_reasons[row_key] = reasons
        if dtec_summary > thresholds["provider_dtec_summary"]["value"]:
            dtec_flags.append(
                f"{row_key}: provider_dtec_summary {dtec_summary} above the D-19 "
                f"{thresholds['provider_dtec_summary']['value']} TECU flag level"
            )

        row: dict[str, Any] = {
            "interval_start_utc": hour_start_utc(hour * 3600),
            "station_id": station,
            "cell_gdlat": cell_lat,
            "cell_glon": cell_lon,
            "cell_lat_bounds": cell_bounds(cell_lat),
            "cell_lon_bounds": cell_bounds(cell_lon),
            "vtec_tecu": vtec,
            "valid_observation_count": count,
            "within_hour_spread_tecu": spread,
            "largest_internal_gap_s": largest_gap,
            "provider_dtec_summary": dtec_summary,
            "aggregation_config_id": aggregation_config_id,
            "target_valid": not reasons,
            "phase_id": identity["phase_id"],
            "source_id": identity["source_id"],
            "target_definition_id": identity["target_definition_id"],
            LINEAGE_CAVEAT_FIELD: LINEAGE_CAVEAT_TEXT,
        }
        assert_row_conforms(row)
        rows.append(row)

    coverage = build_coverage_report(rows, invalid_reasons=invalid_reasons)
    budget = build_uncertainty_budget(rows)
    assert_budget_complete(budget)
    quality = build_data_quality_block(
        coverage_report=coverage,
        uncertainty_budget=budget,
        explained_negatives=explained_negatives,
        aggregation_flags=dtec_flags,
        unexplained_discrepancies=(),
    )
    return StandardizationResult(
        rows=rows,
        coverage_report=coverage,
        data_quality=quality,
        uncertainty_budget=budget,
        identity=identity,
        statistic=statistic,
        thresholds=thresholds,
    )


# =======================================================================================
# Coverage, data quality, uncertainty budget
# =======================================================================================


def build_coverage_report(
    rows: Sequence[Mapping[str, Any]],
    *,
    invalid_reasons: Mapping[str, Sequence[str]] | None = None,
) -> dict[str, Any]:
    """R-71 content 3: missingness and support BY CELL AND MONTH — completeness tier.

    Keyed to the same cell and month identifiers `inventory-and-registry`'s G-P1A
    record uses (station, cell_gdlat, cell_glon, month), so a G-P1A reviewer reading
    both can line them up. A coverage shortfall is recorded machine-readably here and
    is never fatal (the two-tier posture's second tier).
    """
    per: dict[tuple[str, int, int, str], dict[str, Any]] = {}
    for row in rows:
        month = str(row["interval_start_utc"])[:7]
        key = (str(row["station_id"]), int(row["cell_gdlat"]), int(row["cell_glon"]), month)
        bucket = per.setdefault(
            key,
            {
                "station": key[0],
                "cell_gdlat": key[1],
                "cell_glon": key[2],
                "month": key[3],
                "rows": 0,
                "valid_rows": 0,
                "invalid_rows": 0,
            },
        )
        bucket["rows"] += 1
        if row["target_valid"]:
            bucket["valid_rows"] += 1
        else:
            bucket["invalid_rows"] += 1
    return {
        "keys": ["station", "cell_gdlat", "cell_glon", "month"],
        "keying_note": (
            "keyed to the same cell and month identifiers the G-P1A record uses "
            "(R-71); different keying is how two reports about one dataset become "
            "impossible to reconcile"
        ),
        "per_cell_month": [per[key] for key in sorted(per)],
        "invalid_reasons": {k: list(v) for k, v in sorted((invalid_reasons or {}).items())},
    }


def build_uncertainty_budget(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """W-7 / R-72: two applicable contents, the asymmetry statement, four not-applicable.

    The budget STATES ITS BOUNDS rather than truncating: the observed ranges of the two
    applicable quantities are reported as computed — a budget that silently clips
    under-reports. The four Phase 2 contents are recorded not-applicable WITH their
    reason, never emitted empty.
    """
    dtec_values = [float(row["provider_dtec_summary"]) for row in rows]
    spread_values = [float(row["within_hour_spread_tecu"]) for row in rows]

    def _bounds(values: Sequence[float]) -> str:
        if not values:
            return "no rows produced; bounds are stated as empty rather than invented"
        return (
            f"observed over {len(values)} row(s): min {min(values)}, max {max(values)} "
            f"— reported as computed, never truncated or clipped to a bound (R-72)"
        )

    return {
        "applicable": {
            "provider_reported_uncertainty": (
                "provider-reported dtec, summarised per hour as provider_dtec_summary "
                "(D-19 statistic: median); " + _bounds(dtec_values)
            ),
            "within_hour_aggregation_spread": (
                "within-hour spread of contributing samples, within_hour_spread_tecu "
                "(D-19 statistic: range, max minus min); " + _bounds(spread_values)
            ),
        },
        "asymmetry_statement": ASYMMETRY_STATEMENT,
        "not_applicable": [
            {"content": content, "reason": _PHASE2_CONTENT_REASON}
            for content in PHASE2_ONLY_UNCERTAINTY_CONTENTS
        ],
        "bounds_statement": (
            "This budget covers the Phase 1-applicable set only (two of Vision 6.9's "
            "six contents plus the asymmetry statement); Vision 6.9 states its list "
            "without a phase qualifier, and the phase qualifier runs through Vision "
            "15.2 — recorded so the gap reads as governed rather than as "
            "non-compliance. Values are stated as computed; nothing is truncated."
        ),
        "completeness": {
            "phase1_applicable": list(PHASE1_APPLICABLE_UNCERTAINTY_CONTENTS),
            "asserted": True,
        },
    }


def assert_budget_complete(budget: Mapping[str, Any]) -> None:
    """R-72: the budget asserts its own completeness against the Phase 1-applicable set.

    FR-P1-05-10's failure condition is "a budget file that exists and states nothing";
    this assertion is what turns that from a reading into a check.

    Raises
    ------
    StandardizationError
        when an applicable content is missing or empty; when the asymmetry statement
        is absent; when a Phase 2 quantity is emitted empty rather than recorded
        not-applicable with its reason; or when the budget states nothing.
    """
    applicable = budget.get("applicable")
    if not isinstance(applicable, Mapping):
        raise StandardizationError(
            "uncertainty budget",
            "carries no applicable-contents mapping; a budget that exists and states "
            "nothing fails the completeness assertion (FR-P1-05-10, R-72)",
        )
    for content in PHASE1_APPLICABLE_UNCERTAINTY_CONTENTS:
        if not str(applicable.get(content, "") or ""):
            raise StandardizationError(
                f"uncertainty budget content {content}",
                "an applicable content is missing or empty; the budget asserts its "
                "own completeness against the Phase 1-applicable set (R-72)",
            )
    if str(budget.get("asymmetry_statement", "") or "") != ASYMMETRY_STATEMENT:
        raise StandardizationError(
            "uncertainty budget asymmetry_statement",
            "absent or altered; FR-P1-05-10's asymmetry statement is a produced "
            "content, quoted from the requirement",
        )
    not_applicable = budget.get("not_applicable")
    if not isinstance(not_applicable, list):
        raise StandardizationError(
            "uncertainty budget not_applicable",
            "absent; the four Phase 2 contents are recorded not-applicable with "
            "their reason, never omitted silently (R-72)",
        )
    recorded = {
        str(entry.get("content", "")): str(entry.get("reason", "") or "")
        for entry in not_applicable
        if isinstance(entry, Mapping)
    }
    for content in PHASE2_ONLY_UNCERTAINTY_CONTENTS:
        if content not in recorded:
            raise StandardizationError(
                f"uncertainty budget not_applicable entry {content!r}",
                "missing; each of the four Phase 2 contents is recorded "
                "not-applicable with its reason (R-72)",
            )
        if not recorded[content]:
            raise StandardizationError(
                f"uncertainty budget not_applicable entry {content!r}",
                "emitted EMPTY rather than recorded not-applicable with its reason; "
                "an empty emission is exactly what R-72 forbids",
            )


def build_data_quality_block(
    *,
    coverage_report: Mapping[str, Any],
    uncertainty_budget: Mapping[str, Any],
    explained_negatives: Sequence[Mapping[str, str]] = (),
    aggregation_flags: Sequence[str] = (),
    unexplained_discrepancies: Sequence[str] = (),
) -> dict[str, Any]:
    """R-71 / NFR-DQ-01: the four contents, with "unexplained" recorded AS unexplained.

    Content 1 documents units, times, signs and fill values; content 2 records the
    negative-VTEC policy and every EXPLAINED negative (unexplained ones were rejected
    before this block could be built); content 3 is the cell-and-month coverage
    report; content 4 is the uncertainty budget. An unexplained discrepancy is
    recorded as unexplained, never attributed to the nearest plausible cause
    (SD-T-04). `processor_qc_flags` carries AGGREGATION flags only; the package, DCB,
    arc, elevation, slip and mapping classes are Phase 2 and recorded not-applicable
    rather than emitted empty (W-3).
    """
    return {
        "documentation": {
            "units": "vtec_tecu, within_hour_spread_tecu, provider_dtec_summary in TECU",
            "times": (
                "UTC throughout; interval_start_utc is the hour start of the "
                "half-open interval [h, h+1)"
            ),
            "signs": (
                "VTEC is non-negative; a negative value is impossible, not small — "
                "an unexplained negative is rejected (R-71 content 2)"
            ),
            "fill_values": (
                "gaps are explicit NaN at acquisition (D-5); standardization "
                "interpolates, smooths and fills NOTHING"
            ),
        },
        "negative_vtec": {
            "policy": (
                "unexplained rejected with an explicit raise naming the record; "
                "explained accepted with the explanation recorded here"
            ),
            "explained": [dict(entry) for entry in explained_negatives],
        },
        "missingness_and_support": dict(coverage_report),
        "uncertainty_budget": dict(uncertainty_budget),
        "processor_qc_flags": {
            "aggregation_flags": list(aggregation_flags),
            "not_applicable_classes": [
                "package-level QC (Phase 2 — recorded not-applicable, never emitted empty)",
                "DCB QC (Phase 2)",
                "arc and cycle-slip QC (Phase 2)",
                "elevation QC (Phase 2)",
                "mapping-function QC (Phase 2)",
            ],
        },
        "unexplained_discrepancies": [
            {"discrepancy": item, "status": "unexplained"} for item in unexplained_discrepancies
        ],
    }


# =======================================================================================
# Write paths — the label and the caveat travel with the product (R-69)
# =======================================================================================

_TARGET_CSV_HEADER: Final[tuple[str, ...]] = (*D17_FIELDS, LINEAGE_CAVEAT_FIELD)


def write_target_rows_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> Path:
    """The target-writing path: every row conforms, every write carries the caveat.

    Every artifact this unit writes carries the caveat column — not the first write
    only, every write (SD-T-02 preservation obligation 1). Beyond this unit's write
    path, survival is neither guaranteed nor claimed: the column buys detectability,
    not survival.

    Raises
    ------
    StandardizationError
        via `assert_row_conforms` for any nonconforming row, before any byte is
        written.
    """
    for row in rows:
        assert_row_conforms(row)
    payload = [{name: row[name] for name in _TARGET_CSV_HEADER} for row in rows]
    guard_egress(payload, context="target rows")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(_TARGET_CSV_HEADER))
        writer.writeheader()
        for row in payload:
            writer.writerow(row)
    return path


def read_target_rows_csv(path: Path) -> list[dict[str, str]]:
    """Read back rows written by `write_target_rows_csv` (the round-trip's read half)."""
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json_artifact(
    path: Path,
    payload: Mapping[str, Any],
    *,
    identity: Mapping[str, str],
    artifact_class: str,
) -> Path:
    """Write a JSON artifact stamped with the three IDs, the label and the caveat.

    Every artifact that describes or carries the Phase 1 target — a coverage report,
    a data-quality block, an uncertainty budget, verification evidence — carries
    `phase_id`, `source_id`, `target_definition_id` (R-70), the
    `location-sampled gridded VTEC` label and the lineage caveat beside it (R-69
    limbs 2-3): a comparison is not the caveat's trigger. The grep-class check runs
    over the whole envelope before the write.

    Raises
    ------
    StandardizationError
        when any identity stamp is empty, or prohibited phrasing appears in the
        payload.
    """
    for key in ("phase_id", "source_id", "target_definition_id"):
        if not str(identity.get(key, "") or ""):
            raise StandardizationError(
                f"artifact identity field {key}",
                "empty; every artifact carries all three definition IDs (R-70)",
            )
    envelope: dict[str, Any] = {
        "artifact_class": artifact_class,
        "phase_id": identity["phase_id"],
        "source_id": identity["source_id"],
        "target_definition_id": identity["target_definition_id"],
        "target_label": TARGET_LABEL,
        LINEAGE_CAVEAT_FIELD: LINEAGE_CAVEAT_TEXT,
        "payload": payload,
    }
    assert_label_permitted(envelope["target_label"])
    assert_no_prohibited_phrasing(envelope, context=artifact_class)
    guard_egress(envelope, context=artifact_class)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(envelope, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


# =======================================================================================
# Verification (W-2; SD-T-03): the value-level closed-set diff
# =======================================================================================


def resolve_float_tolerance(fixture_manifest: Mapping[str, Any]) -> float:
    """The declared float tolerance from the fixture manifest — or STOP (TE 15.2).

    Raises
    ------
    StandardizationError
        naming the fixture manifest's permitted floating-point tolerances field when
        it is unset: a tolerance taken from a library default (e.g. `numpy.isclose`)
        is a scientific value filled by convenience, and the run stops instead.
    """
    node = fixture_manifest.get(TOLERANCE_MANIFEST_KEY)
    value = node.get(TOLERANCE_MANIFEST_SUBKEY) if isinstance(node, Mapping) else None
    if isinstance(value, str) and value.strip() == TBD_SENTINEL:
        value = None
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise StandardizationError(
            f"fixture_manifest.yaml {TOLERANCE_MANIFEST_KEY}.{TOLERANCE_MANIFEST_SUBKEY}",
            "the permitted floating-point tolerance (TE 15.2) is unset; the "
            "value-level diff tolerance is a DECLARED value belonging with the "
            "fixture manifest, never a library default such as numpy.isclose's — "
            "the verification stops rather than choosing one (SD-T-03)",
        )
    return float(value)


_COMPARED_FLOAT_FIELDS: Final[tuple[str, ...]] = (
    "vtec_tecu",
    "within_hour_spread_tecu",
    "largest_internal_gap_s",
    "provider_dtec_summary",
)
_COMPARED_EXACT_FIELDS: Final[tuple[str, ...]] = (
    "station_id",
    "cell_gdlat",
    "cell_glon",
    "cell_lat_bounds",
    "cell_lon_bounds",
    "valid_observation_count",
    "phase_id",
    "source_id",
    "target_definition_id",
    LINEAGE_CAVEAT_FIELD,
)


def verify_value_level(
    provider_rows: Sequence[Mapping[str, Any]],
    target_rows: Sequence[Mapping[str, Any]],
    *,
    data_config: Mapping[str, Any],
    aggregation_config_id: str,
    tolerance: float,
    negative_vtec_explanations: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """FR-P1-03-1's proof: a VALUE-LEVEL diff showing only the documented transformations.

    Value-level, not schema-level — a check comparing column names and dtypes does not
    meet the criterion, and it is the cheaper check, so it looks like progress
    (SD-T-03). The expected target is recomputed from the provider rows through the
    same closed four-transformation engine, and every value is compared: a difference
    beyond the declared tolerance is a change NOT attributable to any of the four
    documented transformations — a fifth transformation, and a FAILURE rather than
    something a reviewer must notice (limb 1, Q7 = D). The recomputation itself
    re-resolves the statistic from config citing D-16 (limb 2).

    Raises
    ------
    StandardizationError
        on a missing or extra target row; on any value difference beyond `tolerance`;
        or through the recomputation's own gates (including the Q2 = A refusal while
        the QC list is unfrozen — a verification of a target that must not exist
        refuses identically).
    """
    expected = standardize_hourly_target(
        provider_rows,
        data_config=data_config,
        aggregation_config_id=aggregation_config_id,
        negative_vtec_explanations=negative_vtec_explanations,
    )

    def _key(row: Mapping[str, Any]) -> tuple[str, str]:
        return (str(row["station_id"]), str(row["interval_start_utc"]))

    expected_by_key = {_key(row): row for row in expected.rows}
    actual_by_key = {_key(row): row for row in target_rows}
    missing = sorted(set(expected_by_key) - set(actual_by_key))
    extra = sorted(set(actual_by_key) - set(expected_by_key))
    if missing or extra:
        raise StandardizationError(
            "target artifact rows",
            f"the value-level diff found rows the documented transformations do not "
            f"explain (missing from artifact: {missing}; not derivable from the "
            f"provider bytes: {extra}); only the four documented transformations are "
            f"permitted (R-64)",
        )

    differences: list[str] = []
    for key in sorted(expected_by_key):
        expected_row = expected_by_key[key]
        actual_row = actual_by_key[key]
        for field in _COMPARED_FLOAT_FIELDS:
            expected_value = float(expected_row[field])
            actual_value = float(actual_row[field])
            if abs(expected_value - actual_value) > tolerance:
                differences.append(
                    f"{key} {field}: artifact {actual_value} vs recomputed "
                    f"{expected_value} (tolerance {tolerance})"
                )
        for field in _COMPARED_EXACT_FIELDS:
            if str(actual_row.get(field)) != str(expected_row[field]):
                differences.append(
                    f"{key} {field}: artifact {actual_row.get(field)!r} vs "
                    f"recomputed {expected_row[field]!r}"
                )
    if differences:
        raise StandardizationError(
            "; ".join(differences),
            "value(s) differ from what the provider bytes plus the four documented "
            "transformations produce — a change not attributable to documented QC, "
            "UTC normalization, D-1 cell selection or D-16 aggregation is a FIFTH "
            "transformation and fails (FR-P1-03-1, R-64, SD-T-03)",
        )

    return {
        "transformations_enumerated": list(PERMITTED_TRANSFORMATIONS),
        "comparison_level": (
            "value-level against the provider bytes; schema-level comparison is "
            "explicitly insufficient (SD-T-03)"
        ),
        "tolerance_tecu": tolerance,
        "tolerance_source": (
            f"fixture manifest {TOLERANCE_MANIFEST_KEY}.{TOLERANCE_MANIFEST_SUBKEY} "
            f"(TE 15.2); never a library default"
        ),
        "rows_compared": len(expected_by_key),
        "differences": [],
        "uncertainty_contents_not_applicable": [
            {"content": content, "reason": _PHASE2_CONTENT_REASON}
            for content in PHASE2_ONLY_UNCERTAINTY_CONTENTS
        ],
    }
