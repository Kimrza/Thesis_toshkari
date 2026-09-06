"""Source inventory, prepared-schema validation, and the December audit engine.

Purpose
-------
The `inventory-and-registry` unit's library surface for W-1, W-5, W-6, W-7 and W-8
(`functional-design/business-logic-model.md`), designed MINIMALLY per Q1 = D: only what
`write_release`'s stated dependency and TE 5.1's nine fields require, plus the audit
mechanism R-50/SD-I-04 fix. Four responsibilities:

1. **The source inventory (W-1, R-44, SD-I-06).** TE 5.1's nine fields per entry — an
   entry carrying fewer than nine FAILS, and the failure names the entry AND the missing
   field, never the file alone. Entries are consumed by release ID and hash, never by
   path. FR-P1-01-6's verbatim Kyoto/CEDAR acknowledgment notice is a DISTINCT field from
   the operational access notes, so a redaction rule cannot mangle text that must not
   change. Every written value routes through `acquisition`'s `guard_egress` redaction
   chokepoint (hard dependency, SD-I-06). FR-P1-01-2's `suffix_mismatch` surfacing is
   ⚠ PROPOSED, not settled (`acquisition` R-34 holds the release-manifest carriage Open
   for stage 3.2) — it is recorded here and deliberately NOT implemented.
2. **Schema validation (W-5, R-49, TS-I-03).** The expected schema lives in
   `configs/data.yaml`; the report records BOTH the expected schema's digest and the
   observed values, so it is self-contained evidence. Stdlib only — if a package ever
   proves necessary, STOP and report to stage 3.2 (do not add a dependency).
3. **The December coverage and regime audit engine (W-6, R-50..R-53, SD-I-04/05/08).**
   Importable mechanism ONLY: scope declaration checked against a governed reference set
   BEFORE any read; two-class routing decided by RECORD DATE (never path or filename),
   with restricted-root residency the expected CONSEQUENCE of the class and any
   disagreement a stop-and-report naming the file; one durable access row per
   December-bearing artifact BEFORE the read, `purpose` bound per limb
   (`coverage_audit` | `regime_audit`, `locked_evaluation` refused); per-`run_id`
   reconciliation 3a (rows vs declared scope) and 3b (all twelve declared months vs the
   report's per-month output, December included); every coverage figure carrying
   `data07_caveat` sourced from its month's `provenance_class`, with an absent source
   field a TE 18.3 stop-and-report, never an uncaveated figure. An interrupted audit
   yields NO report; its rows stand (NFR-AUD-01).
4. **The G-P1A record and the four prohibitions (W-7, W-8, R-51, R-52, SD-I-08).**
   Verdicts against BOTH D-12 and D-2, every measured figure attributed to the D-number
   it is judged against, D-2's post-hoc disclosure travelling on the record, no soft
   margin band; four separately named prohibition results asserted present (this unit
   owns two: silent imputation, source mixing).

Inputs
------
`acquisition`'s released artifacts (by release ID and hash), the `ConfigSnapshot`
mappings (`configs/data.yaml`'s `prepared_schema`, `stations` and `gp1a` blocks — read
via `foundation`'s `load_configs`, never directly), and per-month `provenance_class`
values from `acquisition`'s manifests. Threshold values (D-12's hourly minimum, D-2's
day minimum) are READ from configuration and never inlined here (TC-03e); an absent
block is a TE 18.3 stop-and-report, never a default.

Re-run behaviour
----------------
Pure functions and validators; the only writers are `write_source_inventory` and
`finalize_audit_reports`, both of which regenerate their target files per run and write
NOTHING when any validation fails (all-or-nothing evidence, SEC-I-03). Restricted reads
are not idempotent by design: each routes through `open_restricted`, which appends one
durable access row per artifact per attempt, and rows from an interrupted attempt stand
permanently (NFR-AUD-01) — per-`run_id` reconciliation is what keeps an honest re-run
distinguishable from an undisclosed extra access.

Governance
----------
* `InventoryError`, `SchemaError`, `AuditScopeError` are declared in
  `src/data/config.py` per the receipted Q1 = A ruling (2026-09-05), riding foundation
  R-01's "any future integrity-related exception" clause. `GateError` is declared HERE,
  its sole raising module, on the `component-methods.md` assumption that exceptions are
  "declared where raised until 3.1 places them" — Q1 = A's receipted scope named three
  names for `config.py`, and applying an owner's answer to a fourth item the owner was
  not shown is the widening this project has already had to correct once.
* **BLK-07's authorization limb is open. No run may touch calendar 2022-12 while it
  stands.** This module is mechanism only; the refusal keyed to BLK-07 lives at the
  stage script's audit entry point (`scripts/01_inventory_and_registry.py`), per the
  approved code-generation plan.
* **This module constructs no path into the restricted root and never holds its
  literal** (R-28): residency is computed against `locked_test`'s own derivation
  (`_repo_root`/`_restricted_root`), the module's supported test seam, so tests exercise
  the boundary against `tmp_path` roots only.
* The locked month (December 2022) is a governance boundary identity fixed by D-8/D-15,
  imported from `acquisition` (`LOCKED_YEAR`/`LOCKED_MONTH`) — never a scientific
  constant, and never derived from a directory or file name (project.md § Forbidden;
  ML-07/TEC-09). Synthetic-month parameters exist so negative controls model December
  without touching December content (`team.md` § Walking Skeleton fixture rule).
"""

from __future__ import annotations

import calendar
import datetime as _dt
import hashlib
import json
import uuid
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from src.data import locked_test
from src.data.acquisition import (
    LOCKED_MONTH,
    LOCKED_YEAR,
    PROVENANCE_CLASSES,
    guard_egress,
)
from src.data.config import (
    TBD_SENTINEL,
    AuditScopeError,
    IntegrityError,
    InventoryError,
    LockedTestError,
    PreflightError,
    SchemaError,
)
from src.data.locked_test import AccessRecord, open_restricted
from src.data.release import sha256_of_file

__all__ = [
    "GateError",
    "SOURCE_INVENTORY_FIELDS",
    "ACKNOWLEDGMENT_FIELD",
    "assert_source_entry",
    "assert_entry_matches_release",
    "assert_verbatim_notice",
    "write_source_inventory",
    "expected_schema_from",
    "schema_digest",
    "SchemaReport",
    "validate_schema",
    "AUDIT_MONTHS",
    "DECEMBER_DAY_RANGE",
    "SCORED_DAY_RANGE",
    "ONE_DAY_EXCESS_STATEMENT",
    "DATA07_CAVEAT",
    "D2_DISCLOSURE",
    "DeclaredAuditScope",
    "governed_reference_scope",
    "assert_scope_equals_reference",
    "new_audit_run_id",
    "AUDIT_LIMB_PURPOSES",
    "audit_access_record",
    "is_december_bearing",
    "route_audit_path",
    "read_audit_artifact",
    "assert_record_date_class_agreement",
    "attribute_records_by_month",
    "coverage_figures",
    "data07_caveat_for",
    "assert_figures_caveated",
    "assert_performance_blind",
    "reconcile_audit",
    "build_regime_report",
    "assert_regime_report_states_range",
    "finalize_audit_reports",
    "gp1a_thresholds_from",
    "build_gp1a_record",
    "assert_gp1a_record",
    "PROHIBITION_RESULT_NAMES",
    "assert_prohibition_results",
    "assert_no_silent_imputation",
    "assert_unmixed_sources",
]


class GateError(IntegrityError):
    """A G-P1A gate invariant is violated (W-7, W-8, R-51, R-52; SD-I-08).

    Raised when: a G-P1A record carries an unattributed number, a verdict with no
    measured figure, or omits D-2's post-hoc disclosure; a `derived_only` coverage
    figure reaches a report or the record with no `data07_caveat` field (R-50/R-51);
    a performance figure appears in a performance-blind report (FR-P1-02-3's checkable
    criterion); a prohibition result is absent from the four individually named ones,
    or an injection this unit owns (silent imputation, source mixing) is detected.

    Declared here, its sole raising module, riding foundation R-01's "any future
    integrity-related exception" clause. The receipted Q1 = A ruling (2026-09-05) named
    `InventoryError`, `AuditScopeError` and `SchemaError` for `src/data/config.py` and
    was not shown this name, so it is NOT folded into that ruling; the declaration-site
    question stays the standing OPEN item (`component-methods.md`: "declared where
    raised until 3.1 places them").
    """


# =======================================================================================
# W-1 / R-44 / SD-I-06: the source inventory
# =======================================================================================

#: TE 5.1's nine fields per source entry — the same nine names `acquisition`'s
#: driver-inventory check uses, so `write_release`'s `source_files` validation reads one
#: vocabulary across the package. Fewer than nine FAILS (R-44).
SOURCE_INVENTORY_FIELDS: Final[tuple[str, ...]] = (
    "provider",
    "role",
    "provider_product_identity",
    "coverage",
    "retrieval_date",
    "checksum",
    "release_status",
    "licence_access_notes",
    "consuming_configuration",
)

#: FR-P1-01-6's verbatim acknowledgment notice — a DISTINCT field from
#: `licence_access_notes` (SD-I-06 point 3), so a redaction rule cannot mangle text that
#: must not change and a notice field never becomes a place operational detail is parked.
ACKNOWLEDGMENT_FIELD: Final[str] = "acknowledgment_notice"


def _entry_id(entry: Mapping[str, object]) -> str:
    return str(
        entry.get("provider_product_identity", "") or entry.get("provider", "") or "<unnamed entry>"
    )


def assert_source_entry(entry: Mapping[str, object]) -> None:
    """R-44: all nine TE 5.1 fields present and non-empty, or the entry FAILS.

    Raises
    ------
    InventoryError
        naming the ENTRY and every missing field — an entry-level raise is what makes a
        partial inventory actionable; a file-level one is not (SD-I-07).
    """
    missing = [
        field
        for field in SOURCE_INVENTORY_FIELDS
        if not str(entry.get(field, "") or "").strip()
    ]
    if missing:
        raise InventoryError(
            _entry_id(entry),
            "source inventory entry is missing TE 5.1 field(s): "
            + ", ".join(missing)
            + " — nine fields per entry, not three, including the configuration that "
            "consumes the source (R-44); fewer than nine fails",
        )


def assert_entry_matches_release(entry: Mapping[str, object], artifact_path: Path) -> None:
    """R-44's boundary: consumed by release ID and hash, never by path.

    Raises
    ------
    InventoryError
        when the artifact's bytes do not hash to the entry's recorded `checksum` — an
        upstream change surfaces as a hash mismatch rather than as silently different
        content (`unit-of-work.md` § 4).
    """
    artifact_path = Path(artifact_path)
    if not artifact_path.is_file():
        raise InventoryError(
            artifact_path,
            f"released artifact for entry {_entry_id(entry)!r} is absent; the inventory "
            f"consumes released artifacts by release ID and hash, and an absent artifact "
            f"cannot be verified (R-44)",
        )
    actual = sha256_of_file(artifact_path)
    expected = str(entry.get("checksum", "") or "")
    if actual != expected:
        raise InventoryError(
            artifact_path,
            f"artifact bytes do not match the release hash recorded for entry "
            f"{_entry_id(entry)!r} (recorded {expected}, actual {actual}); an upstream "
            f"change must surface as a hash mismatch, never as silently different "
            f"content (R-44)",
        )


def assert_verbatim_notice(entry: Mapping[str, object], required_text: str) -> None:
    """FR-P1-01-6: the provider's acknowledgment notice, VERBATIM, as a distinct field.

    Raises
    ------
    InventoryError
        when the notice is absent, or present but not character-for-character identical
        to the provider's required text — "a notice recorded by reference rather than
        verbatim, fails", and a paraphrase is the same defect (R-44's box).
    """
    recorded = entry.get(ACKNOWLEDGMENT_FIELD)
    if recorded is None or not str(recorded).strip():
        raise InventoryError(
            _entry_id(entry),
            f"provider requires a verbatim acknowledgment notice and the entry carries "
            f"none in its {ACKNOWLEDGMENT_FIELD!r} field (FR-P1-01-6; due before the "
            f"G-P1A gate this unit hosts)",
        )
    if str(recorded) != required_text:
        raise InventoryError(
            _entry_id(entry),
            "acknowledgment notice is not verbatim: the recorded text differs from the "
            "provider's required text (FR-P1-01-6) — a notice recorded by reference or "
            "paraphrase fails, and the field is kept distinct from access notes exactly "
            "so nothing rewrites it (SD-I-06)",
        )


def write_source_inventory(
    path: Path,
    entries: Sequence[Mapping[str, object]],
    *,
    required_notices: Mapping[str, str] | None = None,
    missing_entries: Sequence[str] = (),
) -> Path:
    """Validate and write the source inventory. Every value routes through `guard_egress`.

    `required_notices` maps a provider name to its required verbatim acknowledgment text;
    every entry for such a provider must carry it character for character (FR-P1-01-6).
    `missing_entries` is the machine-readable completeness-shortfall field (`team.md`
    § Code Style): a source that could not be inventoried is recorded here, never
    console text only, and is non-fatal.

    FR-P1-01-2's `suffix_mismatch` surfacing to `write_release` is ⚠ PROPOSED and NOT
    implemented here: `acquisition` R-34 holds the release-manifest carriage of that
    field Open for stage 3.2, and this module defers to that resolution rather than
    silently answering it (R-44's box, terminal finding N3).

    Raises
    ------
    InventoryError
        per entry, naming the entry and the missing field(s) or the notice defect.
    CredentialEgressError
        when any value is credential-shaped — no credential, token or signed URL enters
        any field of a committed artifact (SD-I-06, NFR-SEC-01).
    """
    notices = dict(required_notices or {})
    for entry in entries:
        assert_source_entry(entry)
        provider = str(entry.get("provider", ""))
        if provider in notices:
            assert_verbatim_notice(entry, notices[provider])
    payload: dict[str, Any] = {
        "entries": [dict(entry) for entry in entries],
        "missing_entries": list(missing_entries),
        "field_contract": list(SOURCE_INVENTORY_FIELDS),
    }
    guard_egress(payload, context=f"source_inventory[{Path(path).name}]")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


# =======================================================================================
# W-5 / R-49 / TS-I-03: schema validation against a governed schema
# =======================================================================================


def expected_schema_from(data_config: Mapping[str, object]) -> Mapping[str, Any]:
    """The `prepared_schema` block of `configs/data.yaml` (Q7 = D: governed, reviewable).

    Raises
    ------
    PreflightError
        when the block is absent or unresolved — the expected schema is a governed value
        (TE 12; TC-03e) and an absent one is a TE 18.3 stop-and-report, never a schema
        an implementer supplies by convenience.
    """
    block = data_config.get("prepared_schema")
    if block is None or (isinstance(block, str) and block.strip() == TBD_SENTINEL):
        raise PreflightError(
            "configs/data.yaml",
            "prepared_schema is absent or unresolved; the expected schema for the "
            "D-144-approved prepared product is a governed value and its transcription "
            "is stop-and-report under TE 18.3, never an implementer default (R-49)",
        )
    if not isinstance(block, Mapping):
        raise PreflightError(
            "configs/data.yaml",
            "prepared_schema must be a mapping (parameters with units and fill values, "
            "cadence_seconds, duplicate_policy) — R-49, Q7=D",
        )
    return block


def schema_digest(expected: Mapping[str, Any]) -> str:
    """SHA-256 of the canonical JSON of the expected schema (stdlib only, TS-I-03).

    Recorded IN the report so the report is self-contained evidence: a changed expected
    schema produces a visibly different digest (R-49).
    """
    canonical = json.dumps(expected, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class SchemaReport:
    """Self-contained schema-validation evidence (W-5): digest + observed values."""

    expected_schema_digest: str
    observed: Mapping[str, Any]
    checked_at_utc: str


def _parse_utc(stamp: str, *, resource: str) -> _dt.datetime:
    try:
        parsed = _dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        raise SchemaError(
            resource,
            f"timestamp {stamp!r} is not parseable ISO-8601; the UTC cadence check "
            f"cannot clear a timestamp it cannot read (R-49) — fail closed",
        ) from None
    if parsed.tzinfo is None or parsed.utcoffset() != _dt.timedelta(0):
        raise SchemaError(
            resource,
            f"timestamp {stamp!r} is not explicit UTC; the prepared product's cadence "
            f"is UTC by contract (FR-P1-02-2)",
        )
    return parsed


def validate_schema(
    observed: Mapping[str, Any],
    expected: Mapping[str, Any],
    *,
    resource: str = "prepared product",
) -> SchemaReport:
    """R-49: parameter names, units, fill values, UTC cadence and duplicates — each
    failing SEPARATELY, against the governed expected schema.

    `expected` (from `configs/data.yaml`): `parameters` (name -> {unit, fill_value}),
    `cadence_seconds`, `duplicate_policy`. `observed` mirrors `parameters` from the
    product and carries `timestamps` (per-station sequences or one flat sequence).

    Raises
    ------
    SchemaError
        naming the resource and the exact mismatch class: a renamed parameter, a changed
        unit, an altered fill value, a broken UTC cadence, or a duplicate timestamp.
    """
    expected_params = expected.get("parameters")
    if not isinstance(expected_params, Mapping):
        raise PreflightError(
            "configs/data.yaml",
            "prepared_schema.parameters is absent or not a mapping (R-49)",
        )
    observed_params = observed.get("parameters")
    if not isinstance(observed_params, Mapping):
        raise SchemaError(resource, "observed product carries no parameters mapping (R-49)")

    missing = sorted(set(expected_params) - set(observed_params))
    extra = sorted(set(observed_params) - set(expected_params))
    if missing or extra:
        raise SchemaError(
            resource,
            f"parameter names do not match the governed schema (missing: {missing}; "
            f"unexpected: {extra}) — FR-P1-02-2",
        )
    for name, spec in expected_params.items():
        obs = observed_params[name]
        if str(obs.get("unit")) != str(spec.get("unit")):
            raise SchemaError(
                resource,
                f"parameter {name!r} unit {obs.get('unit')!r} does not match the "
                f"governed unit {spec.get('unit')!r} (FR-P1-02-2)",
            )
        if obs.get("fill_value") != spec.get("fill_value"):
            raise SchemaError(
                resource,
                f"parameter {name!r} fill value {obs.get('fill_value')!r} does not match "
                f"the governed fill value {spec.get('fill_value')!r} (FR-P1-02-2)",
            )

    cadence_s = expected.get("cadence_seconds")
    timestamps = observed.get("timestamps", ())
    series_map: Mapping[str, Sequence[str]]
    if isinstance(timestamps, Mapping):
        series_map = timestamps
    else:
        series_map = {"<product>": list(timestamps)}
    for series, stamps in series_map.items():
        parsed = [_parse_utc(str(stamp), resource=f"{resource}[{series}]") for stamp in stamps]
        seen: set[_dt.datetime] = set()
        for value in parsed:
            if value in seen:
                raise SchemaError(
                    f"{resource}[{series}]",
                    f"duplicate timestamp {value.isoformat()}; the governed duplicate "
                    f"policy admits none (FR-P1-02-2)",
                )
            seen.add(value)
        if cadence_s is not None and len(parsed) >= 2:
            ordered = sorted(parsed)
            for earlier, later in zip(ordered, ordered[1:], strict=False):
                delta = (later - earlier).total_seconds()
                if delta % float(cadence_s) != 0.0:
                    raise SchemaError(
                        f"{resource}[{series}]",
                        f"UTC cadence broken: consecutive timestamps "
                        f"{earlier.isoformat()} -> {later.isoformat()} are {delta} s "
                        f"apart, not a multiple of the governed cadence {cadence_s} s "
                        f"(FR-P1-02-2)",
                    )

    return SchemaReport(
        expected_schema_digest=schema_digest(expected),
        observed=dict(observed),
        checked_at_utc=_dt.datetime.now(_dt.UTC).isoformat(),
    )


# =======================================================================================
# W-6 / R-50 / SD-I-04 / SD-I-05: the December audit engine (mechanism only)
# =======================================================================================

#: The twelve audit-year months, derived from the D-8/D-15 boundary identity — never a
#: new literal, never a directory name.
AUDIT_MONTHS: Final[tuple[str, ...]] = tuple(
    f"{LOCKED_YEAR}-{month:02d}" for month in range(1, 13)
)

#: R-50 (Recommendation 15): the audit's December day range is FULL CALENDAR DECEMBER,
#: for both limbs. A December cell declared at fewer than 31 days fails check 1.
DECEMBER_DAY_RANGE: Final[tuple[int, int]] = (1, 31)

#: D-28's G-06 scored set: 2-31 December, 30 days (first 24 h excluded and counted).
#: A frozen decision identity cited for the mandatory one-day-excess disclosure — this
#: module measures over 1-31 and DISCLOSES the excess; it never judges D-13's threshold.
SCORED_DAY_RANGE: Final[tuple[int, int]] = (2, 31)

#: The disclosure both reports must state in terms, not leave the reader to compute.
ONE_DAY_EXCESS_STATEMENT: Final[str] = (
    "This report's count window is full calendar December (1-31 December 2022, 31 days). "
    "The G-06 scored set is 2-31 December 2022 (30 days) under D-28, so the count window "
    "exceeds the scored window by exactly one day. Which day range governs D-13's >=3 "
    "independent-storm-event threshold is Student + Supervisor's to decide; this unit "
    "measures, it does not demote."
)

#: The DATA-07 provenance caveat, machine-readable, sourced per month from
#: `provenance_class` (R-50, Recommendation 29). The three facts a supervisor accepting
#: G-P1A must be able to read off the report, plus team.md's reliance limit.
DATA07_CAVEAT: Final[str] = (
    "DATA-07: this month's provenance is unverifiable in principle, not merely "
    "unverified — no provider byte stream exists anywhere in the workspace, and the "
    "provider-side term of the hash arithmetic is zero. Three of the twelve months "
    "(2022-04, 2022-07 and 2022-12, the locked month) hold no raw_isprint_cache/ at "
    "all. The 2026-08-16 corrected extracts were produced under Python 3.14, outside "
    "the governed 3.11 pin. FULL must not be relied on at a freeze gate while its "
    "provenance chain points at superseded per-month hashes (team.md § Walking "
    "Skeleton)."
)

#: D-2's own post-hoc disclosure, carried INTO the G-P1A record (R-51): a record that
#: omits it presents a partly post-hoc threshold as blind.
D2_DISCLOSURE: Final[str] = (
    "D-2 discloses that five of twelve months had already been audited at 100% day "
    "coverage when the >=95%-of-calendar-days threshold was chosen — it was not set "
    "blind, and is stated here so a reviewer can discount it accordingly."
)

#: The two audit limbs and the `AccessRecord.purpose` literal each BINDS (R-50,
#: Recommendation 11). `locked_evaluation` is G-06's literal and is refused.
AUDIT_LIMB_PURPOSES: Final[Mapping[str, str]] = {
    "coverage": "coverage_audit",
    "regime": "regime_audit",
}

#: The authorization reference both audit rows carry.
_AUDIT_AUTHORIZATION: Final[str] = "Vision §8.3 performance-blind pre-G-05 audit"

#: Key fragments that mark a performance figure. FR-P1-02-3's criterion — no performance
#: figure in the coverage report or its execution log — made checkable.
_PERFORMANCE_KEY_FRAGMENTS: Final[tuple[str, ...]] = (
    "rmse",
    "mae",
    "mse",
    "loss",
    "skill",
    "accuracy",
    "r2",
    "residual",
    "prediction",
    "validation_metric",
    "performance_metric",
)


@dataclass(frozen=True)
class DeclaredAuditScope:
    """What the audit declares it will read, stated BEFORE it reads anything (§ 5)."""

    months: tuple[str, ...]
    december_days: tuple[int, int]
    cells: Mapping[str, tuple[int, int]]
    artifact_classes: tuple[str, ...]


def governed_reference_scope(
    data_config: Mapping[str, object],
    inventory_entries: Sequence[Mapping[str, object]],
) -> DeclaredAuditScope:
    """The governed reference set check 1 compares the declaration against (R-50).

    Months and the December day range are fixed by the D-8 boundary identity; the three
    cells come from `configs/data.yaml`'s `stations` block (D-1's frozen values, once
    transcribed at the single pre-G-P1A freeze event — Q2 = A); the artifact classes are
    derived from the release inventory (R-44), NEVER from the audit's own declaration.

    Raises
    ------
    PreflightError
        while `stations` carries the `TBD — freeze gate` sentinel or lacks cells — a
        TE 18.3 stop-and-report, never a cell set invented here (§18.2).
    """
    stations = data_config.get("stations")
    if stations is None or (isinstance(stations, str) and stations.strip() == TBD_SENTINEL):
        raise PreflightError(
            "configs/data.yaml",
            "stations is unresolved (TBD — freeze gate): the coordinates, the cell rule "
            "and the IGRF version defer to ONE pre-G-P1A freeze event (Q2=A), and the "
            "audit's governed reference cells cannot be invented here (TE 18.2/18.3)",
        )
    if not isinstance(stations, Mapping) or not stations:
        raise PreflightError(
            "configs/data.yaml",
            "stations must be a non-empty mapping of station_id to its frozen entry "
            "(lat, lon, cell) once the freeze event lands",
        )
    cells: dict[str, tuple[int, int]] = {}
    for station_id, entry in stations.items():
        if not isinstance(entry, Mapping) or "cell" not in entry:
            raise PreflightError(
                "configs/data.yaml",
                f"stations.{station_id} carries no frozen cell; the reference set "
                f"cannot be derived from an incomplete transcription (TE 18.3)",
            )
        lat_idx, lon_idx = entry["cell"]
        cells[str(station_id)] = (int(lat_idx), int(lon_idx))

    classes = sorted({str(entry.get("role", "") or "") for entry in inventory_entries} - {""})
    if not classes:
        raise PreflightError(
            "source inventory",
            "no artifact classes derivable from the release inventory; the reference "
            "set is derived from the inventory (R-44), never from the declaration",
        )
    return DeclaredAuditScope(
        months=AUDIT_MONTHS,
        december_days=DECEMBER_DAY_RANGE,
        cells=cells,
        artifact_classes=tuple(classes),
    )


def assert_scope_equals_reference(
    declared: DeclaredAuditScope, reference: DeclaredAuditScope
) -> None:
    """Check 1 — declared versus REQUIRED, BEFORE any read (R-50, Q4 = C).

    Raises
    ------
    AuditScopeError
        whose resource is the DECLARED SCOPE, never a file path: the raise happens
        before any artifact is opened, and naming a file would imply a read that did
        not occur (SD-I-02). An audit that declares eleven months and would execute
        exactly eleven fails HERE — the case checks 2 and 3 structurally cannot see.
    """
    problems: list[str] = []
    if tuple(declared.months) != tuple(reference.months):
        missing = sorted(set(reference.months) - set(declared.months))
        extra = sorted(set(declared.months) - set(reference.months))
        problems.append(f"months (missing: {missing}; extra: {extra})")
    if tuple(declared.december_days) != tuple(reference.december_days):
        problems.append(
            f"December day range {declared.december_days} != required "
            f"{reference.december_days} (1-31 December, 31 days; Recommendation 15)"
        )
    if dict(declared.cells) != dict(reference.cells):
        problems.append(
            f"cells {sorted(declared.cells)} != required {sorted(reference.cells)}"
        )
    if set(declared.artifact_classes) != set(reference.artifact_classes):
        problems.append(
            f"artifact classes {sorted(declared.artifact_classes)} != required "
            f"{sorted(reference.artifact_classes)}"
        )
    if problems:
        raise AuditScopeError(
            "declared audit scope",
            "declared scope does not equal the governed reference set — a short "
            "declaration fails BEFORE anything is read, because a silently skipped "
            "month produces a wrong figure that looks right (R-50 check 1): "
            + "; ".join(problems),
        )


def new_audit_run_id(now: _dt.datetime | None = None) -> str:
    """A distinct `run_id` per audit attempt: `audit-<UTCstamp>-<8charuuid>` (SD-I-05).

    Per-`run_id` reconciliation is what keeps an honest re-run distinguishable from an
    undisclosed extra access — an interrupted audit's rows stand permanently, so the
    log will legitimately show December opened more times than the audit ran.
    """
    stamp = (now or _dt.datetime.now(_dt.UTC)).strftime("%Y%m%dT%H%M%SZ")
    return f"audit-{stamp}-{uuid.uuid4().hex[:8]}"


def audit_access_record(
    run_id: str, *, limb: str, artifact_identity: str = "", purpose: str | None = None
) -> AccessRecord:
    """One typed access row per December-bearing artifact per limb (R-50, Rec. 11).

    The limb BINDS the purpose literal: `coverage` -> `"coverage_audit"`, `regime` ->
    `"regime_audit"`. An explicit `purpose` is accepted only when it equals the limb's
    bound literal — the limb and its literal are paired, not interchangeable.

    Raises
    ------
    LockedTestError
        for `purpose="locked_evaluation"` (that literal is G-06's, and an audit
        carrying it would block the read Vision §8.3 REQUIRES), for any other
        limb/purpose mismatch, and for an unknown limb.
    """
    if limb not in AUDIT_LIMB_PURPOSES:
        raise LockedTestError(
            "audit access record",
            f"unknown audit limb {limb!r}; the two limbs are "
            f"{sorted(AUDIT_LIMB_PURPOSES)} (R-50)",
        )
    bound = AUDIT_LIMB_PURPOSES[limb]
    if purpose is not None and purpose != bound:
        if purpose == "locked_evaluation":
            raise LockedTestError(
                "audit access record",
                "purpose 'locked_evaluation' is refused for an audit read: that literal "
                "is G-06's one-shot hash-before-metrics event, and an audit carrying it "
                "would trip the sibling must-not-fire control and block the read Vision "
                "§8.3 requires (R-50, Recommendation 11)",
            )
        raise LockedTestError(
            "audit access record",
            f"purpose {purpose!r} does not match the {limb!r} limb's bound literal "
            f"{bound!r}; the limb and its literal are paired, not interchangeable "
            f"(R-50, Recommendation 11)",
        )
    return AccessRecord(
        run_id=run_id,
        retrieved_at_utc=_dt.datetime.now(_dt.UTC).isoformat(),
        scope=artifact_identity,
        purpose=bound,
        performance_inspected=False,
        locked_test_accessed=True,
        authorization=_AUDIT_AUTHORIZATION,
    )


def _record_date(record: Mapping[str, object], timestamp_key: str) -> _dt.date:
    raw = str(record.get(timestamp_key, "") or "")
    try:
        return _dt.date.fromisoformat(raw[:10])
    except ValueError:
        raise InventoryError(
            raw or f"<record with no {timestamp_key}>",
            f"record timestamp {timestamp_key!r} is missing or unparseable; membership "
            f"derives from RECORD TIMESTAMPS, never from a directory or file name "
            f"(R-50, project.md § Forbidden), and a record whose date cannot be "
            f"established cannot be cleared — fail closed, never guess",
        ) from None


def is_december_bearing(
    records: Iterable[Mapping[str, object]],
    *,
    timestamp_key: str = "timestamp",
    locked: tuple[int, int] = (LOCKED_YEAR, LOCKED_MONTH),
) -> bool:
    """The two-class test, decided by RECORD DATE — never path, directory or filename.

    `locked` defaults to the D-8/D-15 boundary identity (December 2022). Negative
    controls pass a synthetic locked month over a synthetic tree, so December is what
    the control MODELS and synthetic months are what it EXECUTES (R-50's fixture rule;
    `team.md` § Walking Skeleton).
    """
    for record in records:
        stamp = _record_date(record, timestamp_key)
        if (stamp.year, stamp.month) == locked:
            return True
    return False


def _current_restricted_root() -> Path:
    """The restricted root, derived by `locked_test`'s OWN derivation.

    This module never holds the restricted-root literal and never constructs a path
    into the root of its own (R-28): it asks the one module that owns the boundary.
    `locked_test._repo_root` is that module's supported test seam, so monkeypatching it
    moves this check and `open_restricted` together — the two can never disagree about
    where the boundary is.
    """
    return locked_test._restricted_root(locked_test._repo_root())


def route_audit_path(
    path: Path,
    *,
    december_bearing: bool,
    run_id: str,
    limb: str,
    registry: Path,
) -> Path:
    """Check 2 — route one artifact by its class; residency must AGREE with the class.

    December-bearing (by record-date class): residency under the restricted root is the
    expected CONSEQUENCE of the class, never its definition (SD-I-04's corrected table).
    The path routes through `open_restricted`, which writes one durable access row
    BEFORE the caller reads it. Ordinary: returned directly, NO access row —
    FR-P1-02-3's obligation is scoped to any operation that reads a December 2022
    record. Returns the resolved path the caller then reads.

    Raises
    ------
    LockedTestError
        stop-and-report NAMING THE FILE on either disagreement: a December-bearing
        artifact residing outside the restricted root (D-15's relocation is incomplete
        or the standing guard missed it — both findings a human must see), or an
        ordinary-classed artifact residing inside it (reading it directly would be a
        second path into the root, which R-28 forbids). Also raised by the chokepoint
        itself when the access-log write fails: the read is aborted, never unlogged.
    """
    resolved = Path(path).resolve()
    resident = resolved.is_relative_to(_current_restricted_root())
    if december_bearing and not resident:
        raise LockedTestError(
            resolved,
            "record-date class is December-bearing but the artifact resides OUTSIDE the "
            "restricted root — stop-and-report: either D-15's relocation is incomplete "
            "or the standing guard missed it, and both are findings a human must see "
            "(SD-I-04); the read does not proceed",
        )
    if not december_bearing and resident:
        raise LockedTestError(
            resolved,
            "artifact is classed ordinary by record date but resides INSIDE the "
            "restricted root — stop-and-report: reading it directly would be a second "
            "path into the root (R-28), and a class/residency disagreement is never "
            "silently preferred one way (SD-I-04)",
        )
    if december_bearing:
        record = audit_access_record(run_id, limb=limb, artifact_identity=str(resolved.name))
        return open_restricted(resolved, record=record, registry=Path(registry))
    return resolved


def read_audit_artifact(
    path: Path,
    *,
    december_bearing: bool,
    run_id: str,
    limb: str,
    registry: Path,
) -> str:
    """Route one artifact per `route_audit_path`, then read its text."""
    routed = route_audit_path(
        path,
        december_bearing=december_bearing,
        run_id=run_id,
        limb=limb,
        registry=registry,
    )
    return routed.read_text(encoding="utf-8")


def assert_record_date_class_agreement(
    path: Path,
    records: Sequence[Mapping[str, object]],
    *,
    december_bearing: bool,
    timestamp_key: str = "timestamp",
    locked: tuple[int, int] = (LOCKED_YEAR, LOCKED_MONTH),
) -> None:
    """The post-read half of the class test: the CONTENT must agree with the class.

    This is what catches the realized TEC-09 failure — a December-bearing record filed
    under an ordinary month's directory and read unlogged. The class was declared before
    the read (routing); the record dates verify it after.

    Raises
    ------
    LockedTestError
        stop-and-report naming the file, on either direction of disagreement.
    """
    derived = is_december_bearing(records, timestamp_key=timestamp_key, locked=locked)
    if derived and not december_bearing:
        raise LockedTestError(
            Path(path),
            f"artifact was read as ordinary but its records include a "
            f"{locked[0]}-{locked[1]:02d} observation — the record-date class "
            f"disagrees with the routing class: stop-and-report naming the file "
            f"(SD-I-04; the realized TEC-09 defect is exactly this shape)",
        )
    if not derived and december_bearing:
        raise LockedTestError(
            Path(path),
            f"artifact was routed as December-bearing but no record's observation date "
            f"falls in {locked[0]}-{locked[1]:02d} — the record-date class disagrees "
            f"with the routing class: stop-and-report naming the file (SD-I-04)",
        )


def attribute_records_by_month(
    records: Iterable[Mapping[str, object]],
    *,
    timestamp_key: str = "timestamp",
    audit_year: int = LOCKED_YEAR,
) -> tuple[dict[str, list[Mapping[str, object]]], int]:
    """Membership from record timestamps, never a name; out-of-year records EXCLUDED.

    Returns (records by "YYYY-MM", excluded out-of-year count). Every per-month
    statistic excludes out-of-month and out-of-year records (project.md § Forbidden) —
    a record is attributed to the month its OBSERVATION timestamp falls in, regardless
    of the directory its file sat in.
    """
    by_month: dict[str, list[Mapping[str, object]]] = {}
    excluded = 0
    for record in records:
        stamp = _record_date(record, timestamp_key)
        if stamp.year != audit_year:
            excluded += 1
            continue
        by_month.setdefault(f"{stamp.year}-{stamp.month:02d}", []).append(record)
    return by_month, excluded


def data07_caveat_for(month: str, provenance_class: str | None) -> str | None:
    """The machine-readable DATA-07 caveat, sourced from the month's `provenance_class`.

    `derived_only` -> the caveat, populated. `full` -> None (the month does not carry
    the defect, so no caveat field is emitted).

    Raises
    ------
    PreflightError
        when the source field is absent or unrecognised — the TE 18.3 stop-and-report
        R-50 requires, NEVER an uncaveated figure: `provenance_class` is `acquisition`'s
        field and its arrival at this unit's boundary is stage 3.2's open seam.
    """
    if provenance_class is None or not str(provenance_class).strip():
        raise PreflightError(
            f"provenance_class[{month}]",
            "the month's provenance_class is absent; the data07_caveat is SOURCED from "
            "that field (acquisition R-36) and an absent source field is a TE 18.3 "
            "stop-and-report, never an uncaveated coverage figure (R-50, Rec. 29)",
        )
    if provenance_class not in PROVENANCE_CLASSES:
        raise PreflightError(
            f"provenance_class[{month}]",
            f"unrecognised provenance_class {provenance_class!r}; the closed set is "
            f"{sorted(PROVENANCE_CLASSES)} (acquisition R-36)",
        )
    return DATA07_CAVEAT if provenance_class == "derived_only" else None


def coverage_figures(
    by_month: Mapping[str, Sequence[Mapping[str, object]]],
    *,
    provenance_classes: Mapping[str, str],
    station_key: str = "station",
    timestamp_key: str = "timestamp",
) -> list[dict[str, Any]]:
    """Per-station-month measured coverage figures, each carrying its DATA-07 caveat.

    Figures are MEASURED, never judged here: day presence and hourly-bin presence per
    station per month, with `days_in_month` from the calendar. Judgment against D-12
    and D-2 is `build_gp1a_record`'s, against thresholds read from configuration.
    """
    figures: list[dict[str, Any]] = []
    for month in sorted(by_month):
        year_n, month_n = (int(part) for part in month.split("-"))
        days_in_month = calendar.monthrange(year_n, month_n)[1]
        stations: dict[str, tuple[set[_dt.date], set[str]]] = {}
        for record in by_month[month]:
            station = str(record.get(station_key, "") or "<unnamed station>")
            date = _record_date(record, timestamp_key)
            hour_slot = str(record.get(timestamp_key, ""))[:13]
            days, hours = stations.setdefault(station, (set(), set()))
            days.add(date)
            hours.add(hour_slot)
        for station in sorted(stations):
            days, hours = stations[station]
            figure: dict[str, Any] = {
                "station": station,
                "month": month,
                "days_present": len(days),
                "days_in_month": days_in_month,
                "day_coverage_pct": round(100.0 * len(days) / days_in_month, 3),
                "hourly_bins_present": len(hours),
                "hourly_bins_in_month": 24 * days_in_month,
                "hourly_coverage_pct": round(100.0 * len(hours) / (24 * days_in_month), 3),
                "provenance_class": provenance_classes.get(month),
            }
            caveat = data07_caveat_for(month, provenance_classes.get(month))
            if caveat is not None:
                figure["data07_caveat"] = caveat
            figures.append(figure)
    return figures


def assert_figures_caveated(figures: Sequence[Mapping[str, object]]) -> None:
    """R-50's negative-control target: a `derived_only` figure with no caveat FAILS.

    Raises
    ------
    GateError
        naming the station-month whose `derived_only` figure carries no
        `data07_caveat` field — team.md's caveat is unconditional wherever FULL's
        coverage figures are relied on, and this is the producing surface.
    """
    for figure in figures:
        if figure.get("provenance_class") == "derived_only" and not str(
            figure.get("data07_caveat", "") or ""
        ):
            raise GateError(
                f"{figure.get('station', '?')}/{figure.get('month', '?')}",
                "a derived_only coverage figure carries no data07_caveat field; the "
                "caveat is machine-readable and sourced from provenance_class, and an "
                "uncaveated figure never leaves this unit (R-50/R-51, Rec. 29)",
            )


def assert_performance_blind(payload: Mapping[str, object], *, resource: str) -> None:
    """FR-P1-02-3's checkable criterion: NO performance figure in report or log.

    Scans mapping keys recursively for performance-figure fragments.

    Raises
    ------
    GateError
        naming the offending key.
    """

    def _walk(node: object, trail: str) -> None:
        if isinstance(node, Mapping):
            for key, value in node.items():
                key_text = str(key).lower()
                for fragment in _PERFORMANCE_KEY_FRAGMENTS:
                    if fragment in key_text:
                        raise GateError(
                            resource,
                            f"performance-shaped field {trail}.{key} in a "
                            f"performance-blind artifact; the pre-G-05 audit inspects "
                            f"no model performance (Vision §8.3, FR-P1-02-3)",
                        )
                _walk(value, f"{trail}.{key}")
        elif isinstance(node, list | tuple):
            for index, item in enumerate(node):
                _walk(item, f"{trail}[{index}]")

    _walk(payload, resource)


def reconcile_audit(
    run_id: str,
    *,
    registry_path: Path,
    declared: DeclaredAuditScope,
    december_identities: Sequence[str],
    per_month_output: Mapping[str, object],
) -> None:
    """Check 3 — TWO reconciliations over DIFFERENT questions (SD-I-04, corrected).

    3a — access rows against the declared scope, PER `run_id`, over the December-bearing
    class (the only class with access rows): did this attempt read exactly the
    restricted artifacts it declared? 3b — declared months against the report's
    per-month output, over ALL TWELVE months, DECEMBER INCLUDED: did every declared
    month actually produce a count? December is covered twice over, by different
    evidence — its reads by 3a, its count by 3b.

    Raises
    ------
    AuditScopeError
        on a mismatch in either limb, naming the missing/extra identities or months.
    """
    registry_path = Path(registry_path)
    rows: list[Mapping[str, Any]] = []
    if registry_path.is_file():
        for line in registry_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("run_id") == run_id:
                rows.append(row)
    written = {str(row.get("scope", "")) for row in rows}
    expected = set(december_identities)
    if written != expected:
        raise AuditScopeError(
            "declared audit scope",
            f"reconciliation 3a failed for run_id {run_id!r}: access rows written do "
            f"not match the declared December-bearing artifacts (missing rows for: "
            f"{sorted(expected - written)}; unexpected rows for: "
            f"{sorted(written - expected)}) — the audit must read exactly what it "
            f"declared, per attempt (R-50 check 3; SD-I-05)",
        )
    missing_months = [month for month in declared.months if month not in per_month_output]
    if missing_months:
        raise AuditScopeError(
            "declared audit scope",
            f"reconciliation 3b failed: declared month(s) {missing_months} are absent "
            f"from the report's per-month output — every declared month must produce a "
            f"count, DECEMBER INCLUDED; a December read that logged correctly but "
            f"whose count was dropped is exactly this check's case (SD-I-04, corrected "
            f"2026-09-02)",
        )


def build_regime_report(
    events: Sequence[Mapping[str, object]],
    *,
    audit_year: int = LOCKED_YEAR,
    locked_month: int = LOCKED_MONTH,
) -> dict[str, Any]:
    """The regime-count report: 31-day window, scored/unscored attribution, no demotion.

    Each event carries `event_id`, `start_utc`, `end_utc` (the `Kp>=5` interval) and
    `pre_window_start_utc` (its -12 h pre-event window). An event whose ENTIRE extent
    (interval AND pre-window) falls outside the D-28 scored set (2-31 December) is
    reported as a separately labelled observation and EXCLUDED from the >=3 tally — an
    interval confined to 1 December must not promote H4/SRQ-5 while contributing zero
    scored rows (R-50). The report states its day range in terms; which range governs
    D-13's threshold is Student + Supervisor's — this unit measures, it does not demote.
    """
    # The month's last calendar day: 31 for December (DECEMBER_DAY_RANGE), derived from
    # the calendar for the synthetic locked months negative controls execute against.
    last_day = calendar.monthrange(audit_year, locked_month)[1]
    scored_start = _dt.date(audit_year, locked_month, SCORED_DAY_RANGE[0])
    scored_end = _dt.date(audit_year, locked_month, last_day)
    tallied: list[Mapping[str, object]] = []
    unscored: list[Mapping[str, object]] = []
    for event in events:
        pre_start = _dt.date.fromisoformat(str(event["pre_window_start_utc"])[:10])
        end = _dt.date.fromisoformat(str(event["end_utc"])[:10])
        wholly_outside = end < scored_start or pre_start > scored_end
        (unscored if wholly_outside else tallied).append(event)
    return {
        "count_window": (
            f"{audit_year}-{locked_month:02d}-{DECEMBER_DAY_RANGE[0]:02d}"
            f"..{audit_year}-{locked_month:02d}-{last_day:02d}"
        ),
        "scored_window": (
            f"{audit_year}-{locked_month:02d}-{SCORED_DAY_RANGE[0]:02d}"
            f"..{audit_year}-{locked_month:02d}-{last_day:02d} (D-28)"
        ),
        "one_day_excess_statement": ONE_DAY_EXCESS_STATEMENT,
        "events_tallied": [dict(event) for event in tallied],
        "tally": len(tallied),
        "unscored_events": [dict(event) for event in unscored],
        "threshold_owner": (
            "D-13 (Student + Supervisor); this unit measures, it does not demote"
        ),
    }


def assert_regime_report_states_range(report: Mapping[str, object]) -> None:
    """R-50's control: a regime-count report that does not state its day range FAILS.

    Raises
    ------
    GateError
        when `count_window` or the one-day-excess statement is absent — the window
        mismatch is RECORDED, not left to be discovered.
    """
    if not str(report.get("count_window", "") or "") or not str(
        report.get("one_day_excess_statement", "") or ""
    ):
        raise GateError(
            "regime-count report",
            "the report does not state the day range its count was taken over (and its "
            "one-day excess over D-28's scored set); both reports state the mismatch in "
            "terms rather than leaving the reader to compute it (R-50, Rec. 15)",
        )


def finalize_audit_reports(
    out_dir: Path,
    *,
    run_id: str,
    registry_path: Path,
    declared: DeclaredAuditScope,
    december_identities: Sequence[str],
    coverage_report: Mapping[str, Any],
    regime_report: Mapping[str, Any],
) -> tuple[Path, Path]:
    """All-or-nothing evidence (SEC-I-03): validate, reconcile, THEN write both reports.

    Every check runs before the first byte is written, so an interrupted or failed
    audit yields NO report while its access rows stand (NFR-AUD-01). Both payloads
    route through the redaction chokepoint before writing.

    Raises
    ------
    AuditScopeError, GateError, PreflightError
        from the checks below — in every case, nothing is written.
    """
    assert_performance_blind(coverage_report, resource="coverage report")
    assert_performance_blind(regime_report, resource="regime-count report")
    figures = coverage_report.get("figures", ())
    if isinstance(figures, Sequence):
        assert_figures_caveated([f for f in figures if isinstance(f, Mapping)])
    assert_regime_report_states_range(regime_report)
    per_month = coverage_report.get("per_month")
    if not isinstance(per_month, Mapping):
        raise AuditScopeError(
            "declared audit scope",
            "coverage report carries no per_month output; reconciliation 3b has "
            "nothing to check against (R-50 check 3)",
        )
    reconcile_audit(
        run_id,
        registry_path=registry_path,
        declared=declared,
        december_identities=december_identities,
        per_month_output=per_month,
    )
    guard_egress(dict(coverage_report), context="coverage_report")
    guard_egress(dict(regime_report), context="regime_report")

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    coverage_path = out_dir / "coverage_report.json"
    regime_path = out_dir / "regime_count_report.json"
    coverage_path.write_text(
        json.dumps(dict(coverage_report), indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    regime_path.write_text(
        json.dumps(dict(regime_report), indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return coverage_path, regime_path


# =======================================================================================
# W-7 / W-8 / R-51 / R-52 / SD-I-08: the G-P1A record and the four prohibitions
# =======================================================================================

#: The four G-P1A prohibitions, each a separately NAMED result — one citation standing
#: for four obligations is how FR-P1-02-8 went untested through four boards (R-52).
PROHIBITION_RESULT_NAMES: Final[tuple[str, ...]] = (
    "silent_imputation",
    "source_mixing",
    "retrospective_split_redesign",
    "map_value_mislabel",
)


def gp1a_thresholds_from(data_config: Mapping[str, object]) -> Mapping[str, Any]:
    """D-12's and D-2's threshold values, read from `configs/data.yaml` — never inlined.

    Expected block: `gp1a` with `hourly_coverage_min_pct` (D-12), `day_coverage_min_pct`
    and `december_days_required` (D-2). These are supervisor-frozen decision values;
    their transcription into the governed config is the owner's, cited by D-number.

    Raises
    ------
    PreflightError
        when the block or any field is absent or unresolved — a TE 18.3 stop-and-report,
        never a threshold an implementer inlines (TC-03e; TE 18.2).
    """
    block = data_config.get("gp1a")
    if block is None or (isinstance(block, str) and block.strip() == TBD_SENTINEL):
        raise PreflightError(
            "configs/data.yaml",
            "gp1a threshold block is absent or unresolved; D-12's hourly minimum and "
            "D-2's day minima are frozen decision values whose config transcription is "
            "the owner's — stop and report under TE 18.3, never inline a threshold "
            "(R-51, TC-03e)",
        )
    if not isinstance(block, Mapping):
        raise PreflightError("configs/data.yaml", "gp1a must be a mapping (R-51)")
    missing = [
        name
        for name in ("hourly_coverage_min_pct", "day_coverage_min_pct", "december_days_required")
        if name not in block
        or (isinstance(block[name], str) and str(block[name]).strip() == TBD_SENTINEL)
    ]
    if missing:
        raise PreflightError(
            "configs/data.yaml",
            "gp1a threshold field(s) absent or unresolved: "
            + ", ".join(missing)
            + " — stop and report under TE 18.3 (R-51)",
        )
    return block


def build_gp1a_record(
    figures: Sequence[Mapping[str, Any]],
    *,
    thresholds: Mapping[str, Any],
    prohibition_results: Mapping[str, str],
    audit_year: int = LOCKED_YEAR,
    locked_month: int = LOCKED_MONTH,
) -> dict[str, Any]:
    """R-51: a verdict per station-month against BOTH D-12 and D-2, every figure
    attributed to the D-number it is judged against, no soft margin.

    A station-month passing the day rule and failing the hourly gate FAILS — neither
    threshold substitutes for the other, and §6.12's exception path does not apply at
    G-P1A. December additionally requires 31/31 days present (D-2). D-2's post-hoc
    disclosure and the DATA-07 provenance statement travel ON the record.
    """
    hourly_min = float(thresholds["hourly_coverage_min_pct"])
    day_min = float(thresholds["day_coverage_min_pct"])
    december_days = int(thresholds["december_days_required"])
    december_key = f"{audit_year}-{locked_month:02d}"

    station_months: list[dict[str, Any]] = []
    for figure in figures:
        month = str(figure.get("month", ""))
        hourly_pct = figure.get("hourly_coverage_pct")
        day_pct = figure.get("day_coverage_pct")
        hourly_pass = hourly_pct is not None and float(hourly_pct) >= hourly_min
        day_pass = day_pct is not None and float(day_pct) >= day_min
        if month == december_key:
            day_pass = day_pass and int(figure.get("days_present", 0)) >= december_days
        entry: dict[str, Any] = {
            "station": figure.get("station"),
            "month": month,
            "hourly_coverage_pct": hourly_pct,
            "hourly_judged_against": "D-12",
            "day_coverage_pct": day_pct,
            "days_present": figure.get("days_present"),
            "day_judged_against": "D-2",
            "provenance_class": figure.get("provenance_class"),
            "verdict": "PASS" if (hourly_pass and day_pass) else "FAIL",
        }
        if "data07_caveat" in figure:
            entry["data07_caveat"] = figure["data07_caveat"]
        station_months.append(entry)

    return {
        "station_months": station_months,
        "d2_disclosure": D2_DISCLOSURE,
        "provenance_statement": DATA07_CAVEAT,
        "prohibition_results": dict(prohibition_results),
        "thresholds": {
            "hourly_coverage_min_pct": hourly_min,
            "hourly_decision": "D-12",
            "day_coverage_min_pct": day_min,
            "december_days_required": december_days,
            "day_decision": "D-2",
        },
    }


def assert_gp1a_record(record: Mapping[str, Any]) -> None:
    """R-51/R-52's record-surface checks: no unattributed number, no bare verdict, the
    D-2 disclosure present, every `derived_only` figure caveated, four named results.

    Raises
    ------
    GateError
        naming the first defect found: a verdict with no measured figure, a figure with
        no D-number attribution, an omitted D-2 disclosure, a caveat-less
        `derived_only` figure, or a missing/failing prohibition result.
    """
    station_months = record.get("station_months")
    if not isinstance(station_months, Sequence) or not station_months:
        raise GateError(
            "G-P1A record", "record carries no station-month entries (R-51)"
        )
    for entry in station_months:
        label = f"{entry.get('station', '?')}/{entry.get('month', '?')}"
        if entry.get("hourly_coverage_pct") is None or entry.get("day_coverage_pct") is None:
            raise GateError(
                label,
                "verdict carries no measured figure; the record requires the measured "
                "hourly and day figure for every station-month — a bare PASS makes "
                "100.0% and 93.2% look identical (R-51)",
            )
        if entry.get("hourly_judged_against") != "D-12" or entry.get("day_judged_against") != "D-2":
            raise GateError(
                label,
                "measured figure is not attributed to the D-number it is judged "
                "against; the criterion forbids an unattributed number (R-51)",
            )
        if entry.get("provenance_class") == "derived_only" and not str(
            entry.get("data07_caveat", "") or ""
        ):
            raise GateError(
                label,
                "a derived_only station-month figure reached the G-P1A record with no "
                "data07_caveat field (R-51, Rec. 29)",
            )
    if not str(record.get("d2_disclosure", "") or ""):
        raise GateError(
            "G-P1A record",
            "D-2's post-hoc disclosure is absent; a record that omits it presents a "
            "partly post-hoc threshold as blind (R-51)",
        )
    assert_prohibition_results(record.get("prohibition_results", {}))


def assert_prohibition_results(results: Mapping[str, object]) -> None:
    """R-52: four separately named results, all present and passing, before G-P1A.

    Raises
    ------
    GateError
        naming each absent or non-passing result individually — a missing one is
        structural, not something a fifth reviewer has to notice.
    """
    if not isinstance(results, Mapping):
        raise GateError("G-P1A evidence set", "prohibition results are not a mapping (R-52)")
    problems: list[str] = []
    for name in PROHIBITION_RESULT_NAMES:
        status = str(results.get(name, "") or "")
        if not status:
            problems.append(f"{name} (absent)")
        elif status != "PASS":
            problems.append(f"{name} ({status})")
    if problems:
        raise GateError(
            "G-P1A evidence set",
            "prohibition result(s) absent or not passing: "
            + "; ".join(problems)
            + " — four separately named results, and the gate asserts all four before "
            "G-P1A accepts (R-52, FR-P1-02-8)",
        )


def _is_gap(value: object) -> bool:
    if value is None:
        return True
    return isinstance(value, float) and value != value  # NaN


def assert_no_silent_imputation(
    before_values: Sequence[object], after_values: Sequence[object], *, series: str
) -> None:
    """Prohibition 1 (this unit's): an imputed value must FAIL.

    A fill of any kind — named, aliased or vectorised — reduces the gap count between
    input and output, so the count equality catches it on branches no fixture exercises
    (the same conservation invariant D-5/D-10.2 fix at acquisition).

    Raises
    ------
    GateError
        naming the series and both counts.
    """
    before = sum(1 for value in before_values if _is_gap(value))
    after = sum(1 for value in after_values if _is_gap(value))
    if before != after:
        raise GateError(
            series,
            f"silent imputation detected: {before} gap(s) at input but {after} in the "
            f"output; gaps are explicit NaN and nothing fills them (D-5, D-10.2, R-52 "
            f"prohibition 1)",
        )


def assert_unmixed_sources(
    rows: Sequence[Mapping[str, object]], *, source_key: str = "source_id", artifact: str
) -> None:
    """Prohibition 2 (this unit's): a mixed-source artifact must FAIL.

    Raises
    ------
    GateError
        naming the artifact and every distinct source found, when more than one source
        identity appears within one artifact — or when a row carries none, because a
        row whose source cannot be established cannot be cleared.
    """
    sources: set[str] = set()
    for index, row in enumerate(rows):
        source = str(row.get(source_key, "") or "")
        if not source:
            raise GateError(
                artifact,
                f"row {index} carries no {source_key!r}; a row whose source cannot be "
                f"established cannot be cleared for the single-source check (R-52 "
                f"prohibition 2) — fail closed",
            )
        sources.add(source)
    if len(sources) > 1:
        raise GateError(
            artifact,
            f"mixed sources within one artifact: {sorted(sources)}; source mixing is a "
            f"named G-P1A prohibition (R-52 prohibition 2, FR-P1-02-8)",
        )
