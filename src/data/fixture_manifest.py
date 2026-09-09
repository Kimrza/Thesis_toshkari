"""F1 + F2 (read side): the ONE fixture-manifest schema, the ONE validating loader, the ledger.

Purpose
-------
`fixtures-and-reproducibility` W-1, W-2, W-3 limb 1, W-5 limb 1 (R-133, R-134, R-135, R-137,
R-139's declaration side). This module is the single read path for
`tests/fixtures/<fixture_id>/fixture_manifest.yaml` (TE 15.2): `load_fixture_manifest(path)`
validates on read and REFUSES, naming the file and the violated expectation (R-01's
constructor contract; the two-tier posture), a manifest that

* lacks any of the TWELVE TE 15.2 content areas, required BY NAME (Identity, Inputs,
  Processing, Expected schema, Units, Row-count ranges, Support/missingness, Timestamp
  tolerances, Independent reference checks, Required outputs, Runtime, Numerical variation) —
  asserted per area, so the block set stays correct whichever numeral a register carries
  (the "thirteen" in `requirements.md` REQ-ENG-4 is a reported correction, not applied);
* records `status: not_applicable` on a Phase-1-applicable quantity, or omits the `reason` on a
  Phase-2-only one (Q3 = A, the FR-P1-03-5 precedent — the quantity table below derives the
  Phase-2-only set from TE 15.2's wording against TE 7.0's Phase 1 hard prohibition);
* carries a MEASURED field without its `measuring_run_id` (R-134: an invented value has
  nowhere to hide), or cites no D-number for its identity (identity by citation, never
  re-derived — the agreement of the cited values with `evidence/DECISIONS.md` is F7's check in
  `src/data/fixture_evidence.py`, not this loader's, so this module parses no prose);
* is `frozen` without a sibling `fixture_manifest.sha256` equal to the file's own SHA-256, or
  is a `candidate` carrying one (SD-X-01 step 1 — the mechanical half of the freeze record);
* names a TE 15.4 required output without a comparison-ledger entry, or a ledger entry without
  a class, units, or (when `toleranced`) a tolerance with provenance (R-139), or a `toleranced`
  TECU entry whose producing path declares no `inverse_route` (BLK-08 down-arrow made a checked
  refusal: R-139 control 25);
* declares an apparatus partition under one of the six frozen ids (R-137 control 15), or a
  `scientific_1month` `fixture_bootstrap` block that is absent or whose `scored_range` is not
  evenly divisible by a declared block length (R-133 control 37);
* whose TE 15.4 `artifact_manifest.json` is absent, incomplete, or disagrees with a file on
  disk (R-133 control 2).

The comparison ledger is consumed here too: `compare_required_outputs` compares a produced
output tree against the frozen expectations — `exact` classes by equality of `sha256`, never
tolerance, and NEVER updating an expectation (TE 13.7; NFR-REP-01; the D-18 traversal-order
lesson); `toleranced` classes within the manifest's own tolerance with units declared. No
tolerance, class or expectation is accepted from a caller.

Inputs
------
The manifest path (YAML, parsed with `pyyaml` imported lazily — absent, the loader refuses BY
NAME, the pattern siblings use for matplotlib and scikit-learn); the sibling `.sha256` when
frozen; the TE 15.4 hash listing the manifest references; `src/data/release.sha256_of_file`
(the single hashing home — nothing here re-implements a digest); `src/data/splits.PARTITION_IDS`
(the six frozen ids, read never restated). A `ConfigSnapshot` for `read_embargo_hours` only.

`parsed=` is a DOCUMENTED test-apparatus injection point: it feeds an already-parsed mapping
so the identical validation runs where pyyaml is uninstallable (this clone). Production callers
never pass it; the ONLY production read path is `load_fixture_manifest(path)`.

Re-run behaviour
----------------
Pure reads. Loading never writes. `write_candidate_manifest` writes exactly once and refuses an
existing file (a superseded manifest is preserved, never overwritten — foundation R-13's
posture applied to test apparatus); it writes `status: candidate` ONLY — nothing here writes
`frozen`, which is the owner's act under Q-31. `compare_required_outputs` reads both trees and
mutates neither.

What this pass cannot make run (TE 18.3, stated once per affected module)
--------------------------------------------------------------------------
No `fixture_manifest.yaml` exists in either fixture tree and none may be authored by hand
(BLK-02); `configs/experiment.yaml` `embargo_hours` is `TBD — freeze gate`, so
`build_apparatus_partitions` refuses today naming that field; this clone has no pyyaml, so the
production read path refuses by name and the tests exercise the loader through `parsed=`.

Limit, stated in the body (SD-X-01; TS-X-01; qualified per board Rec 10 / DR-03)
--------------------------------------------------------------------------------
The chokepoint is a convention plus a scan, not an enforcement: a direct `yaml.safe_load` of a
manifest bypasses every check here. The only-copy control (R-133 control 4,
`tests/test_clean_run.py`) is an AST scan that fails the suite on `yaml.*load` calls under
`src/`, `scripts/` or `tests/` outside this module **whose argument subtree textually
references `fixture_manifest`** — an intermediate-variable parse (`text = path.read_text();
yaml.safe_load(text)`) is outside its reach and remains a convention backed by review. The
scan narrows the author-convenience case and closes nothing that goes around the repository.

Enumerations carried (frozen upstream; identities, never values)
----------------------------------------------------------------
The twelve TE 15.2 area names and their quantities; TE 15.4's hash-listable outputs (22 tree
lines minus the `plots/` directory line and `artifact_manifest.json` itself = 20, of which
`target_uncertainty_budget.json` is fixture-2-only, so 19 for `plumbing_7day`); TE 13.7's five
exact classes; the two comparison classes; the two manifest states; the two fixture ids. NO
date, station, month, count, tolerance or runtime literal appears in this module.
"""

from __future__ import annotations

import fnmatch
import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Final

from src.data.config import TBD_SENTINEL, ConfigSnapshot, IntegrityError
from src.data.release import sha256_of_file
from src.data.splits import PARTITION_IDS, Partition, PartitionKind

__all__ = [
    "FIXTURE_IDS",
    "PLUMBING_FIXTURE_ID",
    "SCIENTIFIC_FIXTURE_ID",
    "MANIFEST_NAME",
    "SIBLING_HASH_NAME",
    "ARTIFACT_MANIFEST_NAME",
    "WALKING_SKELETON_ROOT",
    "FIXTURES_ROOT",
    "MANIFEST_STATUSES",
    "CANDIDATE",
    "FROZEN",
    "NOT_APPLICABLE",
    "Quantity",
    "CONTENT_AREAS",
    "AREA_KEYS",
    "PHASE2_ONLY_QUANTITIES",
    "REQUIRED_OUTPUTS",
    "SCIENTIFIC_ONLY_OUTPUTS",
    "COMPARISON_CLASSES",
    "EXACT_KINDS",
    "TECU",
    "FixtureManifest",
    "IdentityDeclaration",
    "DECLARATION_KIND",
    "load_fixture_manifest",
    "load_identity_declaration",
    "load_fixture_scope",
    "validate_manifest_mapping",
    "window_days",
    "required_outputs_for",
    "output_matches",
    "read_embargo_hours",
    "build_apparatus_partitions",
    "compare_required_outputs",
    "assert_run_level_ranges",
    "MEASUREMENTS_NAME",
    "MEASURING_RESULT_PREFIX",
    "collect_stage_measurements",
    "write_measuring_result",
    "load_measuring_results",
    "compose_measurement_ranges",
    "compose_candidate_manifest",
    "write_candidate_manifest",
    "manifest_path_for",
    "fixture_root_for",
]

# --- identities and enumerations (TE 15.1, 15.2, 15.4, 13.7) ------------------------------

PLUMBING_FIXTURE_ID: Final[str] = "plumbing_7day"
SCIENTIFIC_FIXTURE_ID: Final[str] = "scientific_1month"
#: TE 15.1's two fixture date windows, by id (TE 12: `tests/fixtures/<fixture_id>/`).
FIXTURE_IDS: Final[tuple[str, ...]] = (PLUMBING_FIXTURE_ID, SCIENTIFIC_FIXTURE_ID)

MANIFEST_NAME: Final[str] = "fixture_manifest.yaml"
#: SD-X-01 step 1: the mechanical half of the freeze record, written ONLY by the owner's act.
SIBLING_HASH_NAME: Final[str] = "fixture_manifest.sha256"
#: TE 15.4: "Every output is hash-listed in `artifact_manifest.json`."
ARTIFACT_MANIFEST_NAME: Final[str] = "artifact_manifest.json"
#: TE 15.4's tree root, relative to the workspace: `artifacts/walking_skeleton/<fixture_id>/`.
WALKING_SKELETON_ROOT: Final[str] = "artifacts/walking_skeleton"
#: TE 12's fixture-tree root, relative to the workspace.
FIXTURES_ROOT: Final[str] = "tests/fixtures"

CANDIDATE: Final[str] = "candidate"
FROZEN: Final[str] = "frozen"
#: R-134's two states; the Q-31 human act sits between them and nothing here performs it.
MANIFEST_STATUSES: Final[tuple[str, ...]] = (CANDIDATE, FROZEN)
#: Q3 = A: the recorded status of a Phase-2-only quantity on a Phase 1 manifest.
NOT_APPLICABLE: Final[str] = "not_applicable"


@dataclass(frozen=True)
class Quantity:
    """One TE 15.2 quantity inside a content area.

    `phase2_only`: may be recorded `status: not_applicable` with a reason on a Phase 1 manifest
    (Q3 = A) — derived from TE 15.2's row wording against TE 7.0's Phase 1 hard prohibition.
    `measured`: every value under it carries `measuring_run_id` (R-134; TE 15.1 "measured from
    the fixtures and frozen; they are not invented here"). `scientific_only`: required on
    `scientific_1month` and refused absent there; optional on `plumbing_7day`.
    """

    key: str
    phase2_only: bool = False
    measured: bool = False
    scientific_only: bool = False


def _q(key: str, **flags: bool) -> Quantity:
    return Quantity(key, **flags)


#: The twelve TE 15.2 content areas BY NAME — (yaml key, TE 15.2 area name, quantities), in
#: the table's order. Naming rather than counting is deliberate (R-133 obligation 1).
CONTENT_AREAS: Final[tuple[tuple[str, str, tuple[Quantity, ...]], ...]] = (
    (
        "identity",
        "Identity",
        (
            _q("fixture_id"),
            _q("stations"),
            _q("utc_dates"),
            _q("selection_rule"),
            _q("creator"),
            _q("approval_status"),
        ),
    ),
    (
        "inputs",
        "Inputs",
        (
            _q("rinex_crx", phase2_only=True),
            _q("site_log"),
            _q("dcb", phase2_only=True),
            _q("iri"),
            _q("ionex"),
            _q("space_weather"),
            # The Phase 1 counterpart of the RINEX/CRX row: TE 15.1, "The Phase 1 fixture
            # reads prepared provider VTEC only" — the month's declared derived artifacts.
            _q("prepared_vtec"),
        ),
    ),
    (
        "processing",
        "Processing",
        (
            _q("gnss_tec_version", phase2_only=True),
            _q("calibration_layer_commit", phase2_only=True),
            _q("full_config_id"),
        ),
    ),
    (
        "expected_schema",
        "Expected schema",
        (
            _q("raw", phase2_only=True),
            _q("intermediate", phase2_only=True),
            _q("hourly_target"),
            _q("feature"),
            _q("benchmark"),
            _q("comparator"),
            _q("prediction"),
            _q("metric"),
            _q("registry"),
        ),
    ),
    (
        "units",
        "Units",
        (
            _q("utc_convention"),
            _q("coordinates"),
            _q("tecu"),
            _q("seconds_counts"),
            _q("external_index_units"),
        ),
    ),
    (
        "row_count_ranges",
        "Row-count ranges",
        (
            _q("parsing", phase2_only=True),
            _q("valid_observation", phase2_only=True),
            _q("hourly_target", measured=True),
            _q("feature_window", measured=True),
            _q("split", measured=True),
        ),
    ),
    (
        "support_missingness",
        "Support/missingness",
        (
            _q("target_support", measured=True),
            _q("invalid_hour", measured=True),
            _q("external_feature", measured=True),
            _q("comparator", measured=True),
        ),
    ),
    (
        "timestamp_tolerances",
        "Timestamp tolerances",
        (
            _q("parser", phase2_only=True),
            _q("hourly_boundary", measured=True),
            _q("iri", measured=True),
            _q("gim", measured=True),
            _q("feature_alignment", measured=True),
        ),
    ),
    (
        "independent_reference_checks",
        "Independent reference checks",
        (
            _q("stec_vtec_intermediates", phase2_only=True),
            _q("hand_worked_dcb_pass", phase2_only=True),
            _q("sample_iri_gim_values"),
        ),
    ),
    (
        "required_outputs",
        "Required outputs",
        (
            _q("artifact_manifest_ref"),
            _q("outputs"),
            _q("comparison_ledger"),
        ),
    ),
    (
        "runtime",
        "Runtime",
        (
            _q("cpu_total", measured=True),
            _q("storage_total", measured=True),
            # statistical-inference R-120 clause 4: the widening guard's measured doubled CPU
            # cost lands here on the scientific fixture (a named cross-unit slot).
            _q("widening_guard_cpu", measured=True, scientific_only=True),
        ),
    ),
    (
        "numerical_variation",
        "Numerical variation",
        (
            _q("exact_fields"),
            _q("floating_point_tolerances", measured=True),
            # statistical-inference R-121: the planted-correlation recovery tolerance lives
            # in the fixture manifest, never in the rule (a named cross-unit slot).
            _q("planted_correlation_recovery_tolerance", measured=True, scientific_only=True),
        ),
    ),
)

AREA_KEYS: Final[tuple[str, ...]] = tuple(key for key, _name, _qs in CONTENT_AREAS)

#: Derived from the table above, never carried: every (area, quantity) that may be recorded
#: `not_applicable` on a Phase 1 manifest.
PHASE2_ONLY_QUANTITIES: Final[tuple[tuple[str, str], ...]] = tuple(
    (area, quantity.key)
    for area, _name, quantities in CONTENT_AREAS
    for quantity in quantities
    if quantity.phase2_only
)

#: TE 15.4's hash-listable required outputs, in tree order. `.*` entries keep TE 15.4's
#: extension wildcard; the manifest names the concrete file and `output_matches` binds them.
REQUIRED_OUTPUTS: Final[tuple[str, ...]] = (
    "input_manifest.yaml",
    "processing_config_snapshot.yaml",
    "hourly_vtec.parquet",
    "feature_table.parquet",
    "iri_benchmark.parquet",
    "gim_comparator.parquet",
    "split_manifest.json",
    "mask_manifest.json",
    "predictions.parquet",
    "metrics.json",
    "bootstrap_summary.json",
    "checkpoint_manifest.json",
    "registry_entry.json",
    "target_uncertainty_budget.json",
    "plots/target_support.*",
    "plots/predictions.*",
    "plots/residuals.*",
    "plots/quality_diagnostics.*",
    "test_report.*",
    "clean_run_log.*",
)
#: TE 15.4: "target_uncertainty_budget.json  # fixture 2 only".
SCIENTIFIC_ONLY_OUTPUTS: Final[tuple[str, ...]] = ("target_uncertainty_budget.json",)

#: R-139's two comparison classes.
COMPARISON_CLASSES: Final[tuple[str, ...]] = ("exact", "toleranced")
#: TE 13.7's five exact-equality classes, by name.
EXACT_KINDS: Final[tuple[str, ...]] = (
    "hash",
    "schema",
    "partition_membership",
    "id",
    "deterministic_cpu_transformation",
)
#: The unit whose tolerance is unfreezable without an inverse route (BLK-08; R-103; R-139).
TECU: Final[str] = "TECU"

_SHA256_RE: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")
_DECISION_RE: Final[re.Pattern[str]] = re.compile(r"^D-\d+[a-z]?$")
_VALUE_KEYS: Final[frozenset[str]] = frozenset(
    {"min", "max", "value", "tolerance", "expected", "seconds", "bytes", "hours", "range"}
)
_STAMP_KEYS: Final[tuple[str, ...]] = ("phase_id", "source_id", "target_definition_id")


# --- the validated shape -----------------------------------------------------------------


@dataclass(frozen=True)
class FixtureManifest:
    """domain-entities § 1: the two-state contract, validated on read.

    `sha256` is the manifest FILE's digest (what a receipt binds to and what the sibling
    `.sha256` must equal when frozen). `data` is the parsed mapping; the properties below are
    typed views, never a second copy of the content.
    """

    path: Path
    fixture_id: str
    status: str
    sha256: str
    data: Mapping[str, Any]
    artifact_manifest_path: Path
    reference_files_present: tuple[str, ...]

    @property
    def is_frozen(self) -> bool:
        return self.status == FROZEN

    @property
    def identity(self) -> Mapping[str, Any]:
        return self.data["identity"]

    @property
    def window(self) -> tuple[date, date]:
        citation = self.identity["window_citation"]
        return _as_date(citation["start_utc"], resource="window_citation.start_utc"), _as_date(
            citation["end_utc"], resource="window_citation.end_utc"
        )

    @property
    def outputs(self) -> tuple[str, ...]:
        return tuple(str(o) for o in self.data["required_outputs"]["outputs"])

    @property
    def comparison_ledger(self) -> Mapping[str, Mapping[str, Any]]:
        return self.data["required_outputs"]["comparison_ledger"]

    @property
    def apparatus_partitions(self) -> Mapping[str, Mapping[str, Any]]:
        block = self.data.get("apparatus_partitions")
        return block if isinstance(block, Mapping) else {}

    @property
    def fixture_bootstrap(self) -> Mapping[str, Any] | None:
        block = self.data.get("fixture_bootstrap")
        return block if isinstance(block, Mapping) else None

    def expected_hashes(self) -> Mapping[str, str]:
        """The frozen expectation for `exact` classes: the TE 15.4 hash listing."""
        listing = json.loads(self.artifact_manifest_path.read_text(encoding="utf-8"))
        return {str(k): str(v) for k, v in listing["outputs"].items()}


# --- small helpers ------------------------------------------------------------------------


def _refuse(resource: object, expectation: str) -> IntegrityError:
    return IntegrityError(resource, expectation)


def _is_tbd(value: object) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == TBD_SENTINEL)


def _as_date(value: object, *, resource: str) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value.strip()[:10])
        except ValueError as exc:
            raise _refuse(resource, f"{value!r} is not an ISO calendar date") from exc
    raise _refuse(resource, f"{value!r} is not a calendar date")


def _nonempty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _parse_yaml_text(path: Path, text: str) -> Mapping[str, Any]:
    """Strict YAML load through pyyaml, imported lazily; absent -> refuse BY NAME (TS-X-01)."""
    try:
        import yaml
    except ImportError as exc:
        raise _refuse(
            path,
            f"pyyaml is required to read a fixture manifest and is not importable ({exc}); "
            f"the production read path stays on pyyaml (TS-X-01) and refuses by name rather "
            f"than falling back to a second parser",
        ) from exc
    try:
        loaded = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise _refuse(path, f"fixture manifest is unparseable YAML: {exc}") from exc
    if not isinstance(loaded, Mapping):
        raise _refuse(path, "fixture manifest must be a mapping at the top level")
    return loaded


def manifest_path_for(workspace: Path, fixture_id: str) -> Path:
    """`<workspace>/tests/fixtures/<fixture_id>/fixture_manifest.yaml` (TE 12; R-122)."""
    _require_fixture_id(fixture_id, resource="fixture_id")
    return Path(workspace) / FIXTURES_ROOT / fixture_id / MANIFEST_NAME


def fixture_root_for(workspace: Path, fixture_id: str) -> Path:
    """`<workspace>/artifacts/walking_skeleton/<fixture_id>/` (TE 15.4)."""
    _require_fixture_id(fixture_id, resource="fixture_id")
    return Path(workspace) / WALKING_SKELETON_ROOT / fixture_id


def _require_fixture_id(fixture_id: object, *, resource: str) -> str:
    if fixture_id not in FIXTURE_IDS:
        raise _refuse(
            resource,
            f"fixture_id {fixture_id!r} is not one of TE 15.1's two fixtures {list(FIXTURE_IDS)}",
        )
    return str(fixture_id)


def required_outputs_for(fixture_id: str) -> tuple[str, ...]:
    """TE 15.4's enumeration for a fixture: 20 for `scientific_1month`, 19 for `plumbing_7day`."""
    _require_fixture_id(fixture_id, resource="fixture_id")
    if fixture_id == SCIENTIFIC_FIXTURE_ID:
        return REQUIRED_OUTPUTS
    return tuple(o for o in REQUIRED_OUTPUTS if o not in SCIENTIFIC_ONLY_OUTPUTS)


def output_matches(output: str, required: str) -> bool:
    """Bind a concrete manifest output to a TE 15.4 entry (`plots/residuals.*` matches
    `plots/residuals.png`); exact names match exactly. Paths are compared with `/`."""
    normalised = output.replace("\\", "/")
    if required.endswith(".*"):
        return fnmatch.fnmatchcase(normalised, required) and normalised.count("/") == required.count(
            "/"
        )
    return normalised == required


# --- validation: the twelve areas ---------------------------------------------------------


def _validate_quantity(
    manifest_path: Path, area: str, quantity: Quantity, value: object, *, fixture_id: str
) -> None:
    resource = f"{manifest_path}: {area}.{quantity.key}"
    if quantity.scientific_only and fixture_id != SCIENTIFIC_FIXTURE_ID and value is None:
        return  # optional on plumbing_7day
    if value is None:
        raise _refuse(
            resource,
            f"TE 15.2 area {area!r} lacks its quantity {quantity.key!r}; every quantity is "
            f"present — a Phase-2-only one as `status: not_applicable` with its reason, never "
            f"absent and never emitted empty (Q3 = A; R-133 obligation 2)",
        )
    if isinstance(value, Mapping) and value.get("status") == NOT_APPLICABLE:
        if not quantity.phase2_only:
            raise _refuse(
                resource,
                f"recorded {NOT_APPLICABLE!r} on a Phase-1-applicable quantity; only the "
                f"Phase-2-only quantities TE 7.0 bars Phase 1 from producing may be "
                f"not_applicable {sorted(k for a, k in PHASE2_ONLY_QUANTITIES if a == area)} "
                f"(Q3 = A)",
            )
        if not _nonempty_str(value.get("reason")):
            raise _refuse(
                resource,
                f"{NOT_APPLICABLE!r} requires a non-empty reason (the FR-P1-03-5 precedent: "
                f"recorded not-applicable rather than emitted empty)",
            )
        return
    if quantity.measured:
        _validate_measured(resource, value)


def _validate_measured(resource: str, value: object) -> None:
    """R-134 control 8: a measured field without `measuring_run_id` is unrepresentable."""
    if not isinstance(value, Mapping):
        raise _refuse(
            resource,
            f"a measured quantity is a mapping carrying its measuring_run_id, got "
            f"{type(value).__name__}",
        )
    if "measuring_run_id" in value:
        if not _nonempty_str(value["measuring_run_id"]):
            raise _refuse(resource, "measuring_run_id is empty; provenance is required (R-134)")
        return
    children = [v for k, v in value.items() if k not in ("units", "note", "scope")]
    if not children or not all(isinstance(child, Mapping) for child in children):
        raise _refuse(
            resource,
            "measured field carries no measuring_run_id; every row-count range, support and "
            "missingness limit, timestamp tolerance, runtime range and floating-point "
            "tolerance is MEASURED from a fixture run and carries that run's registry id — "
            "a field without one is unrepresentable (TE 15.1; R-134 control 8)",
        )
    for key, child in value.items():
        if key in ("units", "note", "scope"):
            continue
        if not _nonempty_str(child.get("measuring_run_id")):
            raise _refuse(
                f"{resource}.{key}",
                "measured field carries no measuring_run_id (TE 15.1; R-134 control 8)",
            )


def _validate_identity(manifest_path: Path, fixture_id: str, data: Mapping[str, Any]) -> None:
    identity = data["identity"]
    res = f"{manifest_path}: identity"
    if identity.get("fixture_id") != fixture_id:
        raise _refuse(
            f"{res}.fixture_id",
            f"{identity.get('fixture_id')!r} disagrees with the manifest's fixture_id "
            f"{fixture_id!r}",
        )
    citation = identity.get("window_citation")
    if not isinstance(citation, Mapping) or not _DECISION_RE.match(
        str(citation.get("decision", ""))
    ):
        raise _refuse(
            f"{res}.window_citation",
            "the window is CITED from its D-number (D-11 for plumbing_7day, D-14 for "
            "scientific_1month), never re-derived; `decision`, `start_utc`, `end_utc` are "
            "required (R-134; R-135)",
        )
    start = _as_date(citation.get("start_utc"), resource=f"{res}.window_citation.start_utc")
    end = _as_date(citation.get("end_utc"), resource=f"{res}.window_citation.end_utc")
    if start > end:
        raise _refuse(f"{res}.window_citation", f"start_utc {start} is after end_utc {end}")
    stations = identity.get("stations")
    if not isinstance(stations, Sequence) or isinstance(stations, str) or not stations:
        raise _refuse(f"{res}.stations", "a non-empty station list is required (TE 15.2)")
    station_citation = identity.get("station_citation")
    if fixture_id == PLUMBING_FIXTURE_ID:
        if len(stations) != 1:
            raise _refuse(
                f"{res}.stations",
                f"plumbing_7day executes on ONE station (TE 15.1; TC-03f), got {len(stations)}",
            )
        if not isinstance(station_citation, Mapping) or not _DECISION_RE.match(
            str(station_citation.get("decision", ""))
        ):
            raise _refuse(
                f"{res}.station_citation",
                "plumbing_7day cites its station from its D-number (D-20), never re-derived; "
                "`decision`, `station_id`, `cell` are required (R-135 limb 1)",
            )
        if str(station_citation.get("station_id")) != str(stations[0]):
            raise _refuse(
                f"{res}.station_citation.station_id",
                f"{station_citation.get('station_id')!r} disagrees with stations {list(stations)}",
            )
        if not _nonempty_str(station_citation.get("cell")):
            raise _refuse(f"{res}.station_citation.cell", "the cited cell is required")
        shortfall = identity.get("aruc_shortfall_status")
        if not isinstance(shortfall, Mapping) or shortfall.get("status") != "dormant":
            raise _refuse(
                f"{res}.aruc_shortfall_status",
                "ARUC's one-bin shortfall is recorded `dormant` — the register's word, never "
                "`discharged` — with its reactivation condition (D-11; D-20; BLK-02)",
            )
        if not _nonempty_str(shortfall.get("reactivation_condition")):
            raise _refuse(
                f"{res}.aruc_shortfall_status.reactivation_condition",
                "the reactivation condition travels with the dormancy so it cannot be misread "
                "as closure",
            )
    elif station_citation is not None:
        raise _refuse(
            f"{res}.station_citation",
            "station_citation (D-20) belongs to plumbing_7day only; scientific_1month runs all "
            "cited stations (D-14)",
        )
    limitations = identity.get("limitations")
    if not isinstance(limitations, Mapping):
        raise _refuse(f"{res}.limitations", "the verbatim limitations block is required")
    if limitations.get("december_representativeness") != "not_representative":
        raise _refuse(
            f"{res}.limitations.december_representativeness",
            "must be the literal `not_representative` — the operative clause of D-11's / "
            "D-14's mandatory limitation as machine-readable freight (R-135 limb 4)",
        )
    clauses = limitations.get("clauses")
    if (
        not isinstance(clauses, Sequence)
        or isinstance(clauses, str)
        or len(clauses) < 2
        or not all(_nonempty_str(c) for c in clauses)
    ):
        raise _refuse(
            f"{res}.limitations.clauses",
            "the limitation is carried VERBATIM as at least two non-empty clauses (D-11's "
            "not-representative-of-December limitation and its provisional-Dst restriction; "
            "D-14's clauses (i) and (ii)); agreement with the cited record is F7's check",
        )
    if not _nonempty_str(identity.get("data07_caveat")):
        raise _refuse(
            f"{res}.data07_caveat",
            "the DATA-07 provenance caveat is a machine-readable manifest field propagated onto "
            "every artifact carrying the fixture's coverage figures (team.md; R-135 limb 3)",
        )
    eligibility = identity.get("eligibility_evidence")
    if not isinstance(eligibility, Mapping) or not _DECISION_RE.match(
        str(eligibility.get("decision", ""))
    ):
        raise _refuse(
            f"{res}.eligibility_evidence",
            "the eligibility-evidence block (cited D-number, source) is distinct from the "
            "expected-assertion blocks and is required (R-134 obligation 4)",
        )
    for key in _STAMP_KEYS:
        if not _nonempty_str(identity.get(key)):
            raise _refuse(
                f"{res}.{key}",
                "the three TEC-05 stamps (phase_id, source_id, target_definition_id) are "
                "required identity fields (project.md Mandated)",
            )
    if data.get("status") == FROZEN:
        freeze = identity.get("freeze_citation")
        if not isinstance(freeze, Mapping) or not _DECISION_RE.match(str(freeze.get("decision", ""))):
            raise _refuse(
                f"{res}.freeze_citation",
                "a frozen manifest cites the D-number of its freeze act (SD-X-01 step 2); the "
                "agreement of that record's hash with the sibling file is F7's check",
            )


def _validate_required_outputs(
    manifest_path: Path, fixture_id: str, data: Mapping[str, Any]
) -> None:
    block = data["required_outputs"]
    res = f"{manifest_path}: required_outputs"
    outputs = block.get("outputs")
    if not isinstance(outputs, Sequence) or isinstance(outputs, str):
        raise _refuse(f"{res}.outputs", "a list of the TE 15.4 required outputs is required")
    listed = [str(o) for o in outputs]
    required = required_outputs_for(fixture_id)
    unmatched_required = [r for r in required if not any(output_matches(o, r) for o in listed)]
    unmatched_outputs = [o for o in listed if not any(output_matches(o, r) for r in required)]
    if unmatched_required or unmatched_outputs:
        raise _refuse(
            f"{res}.outputs",
            f"the Required-outputs block is asserted COMPLETE against TE 15.4's enumeration "
            f"({len(required)} hash-listable outputs for {fixture_id}); missing "
            f"{unmatched_required}, unexpected {unmatched_outputs} (R-133 obligation 3; the "
            f"R-129 inventory-completeness pattern)",
        )
    if len(set(listed)) != len(listed):
        raise _refuse(f"{res}.outputs", "duplicate output entries")
    if fixture_id != SCIENTIFIC_FIXTURE_ID:
        stray = [o for o in listed if any(output_matches(o, s) for s in SCIENTIFIC_ONLY_OUTPUTS)]
        if stray:
            raise _refuse(f"{res}.outputs", f"{stray} is fixture-2-only (TE 15.4)")
    ledger = block.get("comparison_ledger")
    if not isinstance(ledger, Mapping):
        raise _refuse(f"{res}.comparison_ledger", "one ledger entry per required output (R-139)")
    for output in listed:
        entry = ledger.get(output)
        if not isinstance(entry, Mapping):
            raise _refuse(
                f"{res}.comparison_ledger[{output}]",
                "required output has no comparison-ledger entry; every output declares its "
                "class at freeze time, never in a test body (R-133 control 3; R-139)",
            )
        _validate_ledger_entry(f"{res}.comparison_ledger[{output}]", entry)
    extra = sorted(set(ledger) - set(listed))
    if extra:
        raise _refuse(f"{res}.comparison_ledger", f"ledger entries for undeclared outputs {extra}")
    if not _nonempty_str(block.get("artifact_manifest_ref")):
        raise _refuse(
            f"{res}.artifact_manifest_ref",
            "the TE 15.4 hash listing is cross-referenced by path (R-133 obligation 3)",
        )


def _validate_ledger_entry(resource: str, entry: Mapping[str, Any]) -> None:
    klass = entry.get("comparison_class")
    if klass not in COMPARISON_CLASSES:
        raise _refuse(
            resource,
            f"comparison_class {klass!r} is not one of {list(COMPARISON_CLASSES)} (R-139)",
        )
    if not _nonempty_str(entry.get("units")):
        raise _refuse(resource, "units are declared on every ledger entry (R-139; entity 2)")
    producing = entry.get("producing_path")
    if not isinstance(producing, Mapping) or not _nonempty_str(producing.get("script")):
        raise _refuse(
            resource,
            "producing_path.script is required: the ledger records which path produced the "
            "output so the inverse-route obligation can be checked (R-139 control 25)",
        )
    if klass == "exact":
        if entry.get("exact_kind") not in EXACT_KINDS:
            raise _refuse(
                resource,
                f"an exact entry names one of TE 13.7's five classes {list(EXACT_KINDS)}",
            )
        if "fp_tolerance" in entry:
            raise _refuse(
                resource,
                "an exact entry carries no fp_tolerance: exact classes compare by EQUALITY, "
                "not tolerance (TE 13.7; NFR-REP-01)",
            )
        return
    tolerance = entry.get("fp_tolerance")
    if not isinstance(tolerance, Mapping):
        raise _refuse(
            resource,
            "a toleranced entry carries fp_tolerance {value, units, measuring_run_id} — the "
            "tolerance lives in the manifest and nowhere else (R-139 control 22)",
        )
    value = tolerance.get("value")
    if isinstance(value, bool) or not isinstance(value, int | float) or value <= 0:
        raise _refuse(f"{resource}.fp_tolerance.value", f"{value!r} is not a positive number")
    if not _nonempty_str(tolerance.get("units")):
        raise _refuse(f"{resource}.fp_tolerance.units", "the tolerance's units are declared")
    if not _nonempty_str(tolerance.get("measuring_run_id")):
        raise _refuse(
            f"{resource}.fp_tolerance.measuring_run_id",
            "tolerance provenance (the measuring run's registry id) is required (R-134)",
        )
    if str(tolerance.get("units")) != str(entry.get("units")):
        raise _refuse(
            f"{resource}.fp_tolerance.units",
            f"{tolerance.get('units')!r} disagrees with the entry's units {entry.get('units')!r}",
        )
    if str(entry.get("units")).upper() == TECU and not _nonempty_str(
        producing.get("inverse_route")
    ):
        raise _refuse(
            resource,
            "a toleranced entry declaring TECU units for an output whose producing path "
            "declares no inverse_route is NOT freezable: a TECU-stated tolerance cannot be "
            "checked against output no design path returns to TECU until evaluation-and-"
            "comparison's R-103 joint contract is adopted by both halves (BLK-08 down-arrow, "
            "checked not inherited; R-139 control 25)",
        )


def _validate_apparatus_partitions(
    manifest_path: Path, fixture_id: str, data: Mapping[str, Any]
) -> None:
    block = data.get("apparatus_partitions")
    res = f"{manifest_path}: apparatus_partitions"
    if block is None:
        if fixture_id == SCIENTIFIC_FIXTURE_ID:
            raise _refuse(
                res,
                "scientific_1month declares its apparatus partition set (ids outside the six "
                "frozen ids) so stages 05-07 can run at fixture scale (R-137; Q4 = A)",
            )
        return
    if not isinstance(block, Mapping) or not block:
        raise _refuse(res, "a non-empty mapping partition_id -> declaration is required")
    start, end = _window_of(data, manifest_path)
    refits = 0
    for pid, entry in block.items():
        pres = f"{res}.{pid}"
        if str(pid) in PARTITION_IDS:
            raise _refuse(
                pres,
                f"{pid!r} is one of the six frozen partition ids {list(PARTITION_IDS)}; "
                f"apparatus ids are quarantined from the frozen id space both ways (R-137 "
                f"control 15; no seventh enumerated exception is minted)",
            )
        if not isinstance(entry, Mapping):
            raise _refuse(pres, "declaration must be a mapping")
        try:
            kind = PartitionKind(str(entry.get("kind")))
        except ValueError as exc:
            raise _refuse(pres, f"kind {entry.get('kind')!r} is not fold | refit") from exc
        if kind is PartitionKind.locked:
            raise _refuse(
                pres,
                "an apparatus partition is never `locked`; the locked month is access-gated "
                "and December-free fixtures construct no December read (R-137; R-82)",
            )
        t_start = _as_date(entry.get("train_start"), resource=f"{pres}.train_start")
        t_end = _as_date(entry.get("train_end"), resource=f"{pres}.train_end")
        if not (start <= t_start <= t_end <= end):
            raise _refuse(
                pres,
                f"training range {t_start}..{t_end} is not inside the cited fixture window "
                f"{start}..{end}",
            )
        raw_month = entry.get("validation_month")
        if kind is PartitionKind.refit:
            refits += 1
            if raw_month is not None:
                raise _refuse(f"{pres}.validation_month", "a refit is scored nowhere; null")
        else:
            month = _as_date(raw_month, resource=f"{pres}.validation_month")
            if not (t_end < month <= end):
                raise _refuse(
                    f"{pres}.validation_month",
                    f"{month} must follow train_end {t_end} and lie inside the window",
                )
    if refits > 1:
        raise _refuse(res, "at most one apparatus refit")


def _window_of(data: Mapping[str, Any], manifest_path: Path) -> tuple[date, date]:
    citation = data["identity"]["window_citation"]
    return (
        _as_date(citation["start_utc"], resource=f"{manifest_path}: window_citation.start_utc"),
        _as_date(citation["end_utc"], resource=f"{manifest_path}: window_citation.end_utc"),
    )


def _validate_fixture_bootstrap(
    manifest_path: Path, fixture_id: str, data: Mapping[str, Any]
) -> None:
    block = data.get("fixture_bootstrap")
    res = f"{manifest_path}: fixture_bootstrap"
    if fixture_id != SCIENTIFIC_FIXTURE_ID:
        if block is not None:
            raise _refuse(res, "the reduced-replicate fixture bootstrap is fixture-2-only (TE 15.3)")
        return
    if not isinstance(block, Mapping):
        raise _refuse(
            res,
            "TE 15.3 requires one bootstrap execution at reduced replicate count for timing on "
            "fixture 2; declare replicates, scored_range and block_counts as apparatus "
            "constants (R-133 limb 5; control 37; Q6 = A (iii))",
        )
    for key in ("replicates", "scored_range", "block_counts"):
        if key not in block:
            raise _refuse(f"{res}.{key}", "required fixture_bootstrap field absent (control 37)")
    replicates = block["replicates"]
    if isinstance(replicates, bool) or not isinstance(replicates, int) or replicates <= 0:
        raise _refuse(f"{res}.replicates", f"{replicates!r} is not a positive integer")
    scored = block["scored_range"]
    hours = scored.get("hours") if isinstance(scored, Mapping) else scored
    if isinstance(hours, bool) or not isinstance(hours, int) or hours <= 0:
        raise _refuse(f"{res}.scored_range", "scored_range.hours must be a positive integer")
    counts = block["block_counts"]
    if not isinstance(counts, Mapping) or not counts:
        raise _refuse(f"{res}.block_counts", "block_counts maps block length (h) -> whole blocks")
    for raw_length, count in counts.items():
        try:
            length = int(str(raw_length).rstrip("h"))
        except ValueError as exc:
            raise _refuse(f"{res}.block_counts[{raw_length}]", "block length not an int") from exc
        if length <= 0:
            raise _refuse(f"{res}.block_counts[{raw_length}]", "block length must be positive")
        if hours % length != 0:
            raise _refuse(
                f"{res}.block_counts[{raw_length}]",
                f"scored_range {hours} h is not evenly divisible by the {length} h block "
                f"length; statistical-inference R-115 limb 1 raises on an indivisible range, "
                f"so it is evaluated at freeze rather than discovered inside the run "
                f"(control 37)",
            )
        if count != hours // length:
            raise _refuse(
                f"{res}.block_counts[{raw_length}]",
                f"declared {count!r} blocks, but {hours} h / {length} h = {hours // length}",
            )


def _validate_status_and_sibling(
    manifest_path: Path, data: Mapping[str, Any], *, file_sha256: str | None
) -> None:
    status = data.get("status")
    if status not in MANIFEST_STATUSES:
        raise _refuse(
            f"{manifest_path}: status",
            f"{status!r} is not one of {list(MANIFEST_STATUSES)} (R-134's two states)",
        )
    if file_sha256 is None:
        return
    sibling = manifest_path.with_name(SIBLING_HASH_NAME)
    if status == FROZEN:
        if not sibling.is_file():
            raise _refuse(
                sibling,
                "a frozen manifest requires its sibling fixture_manifest.sha256, written only by "
                "the owner's freeze act (SD-X-01 step 1; Q1 = C at nfr-design)",
            )
        recorded = sibling.read_text(encoding="utf-8").strip().split()[0].lower()
        if recorded != file_sha256:
            raise _refuse(
                manifest_path,
                f"frozen manifest's SHA-256 {file_sha256} disagrees with the sibling record "
                f"{recorded}; a post-freeze edit without a new freeze act fails and the "
                f"expectation is never updated (R-134 control 6; SD-X-01)",
            )
    elif sibling.exists():
        raise _refuse(
            sibling,
            "a candidate manifest carries no sibling hash; only frozen manifests do "
            "(SD-X-01's negative control)",
        )


def _validate_hash_listing(
    manifest_path: Path, fixture_id: str, data: Mapping[str, Any]
) -> tuple[Path, tuple[str, ...]]:
    """R-133 obligation 3 / control 2: the TE 15.4 listing exists, is complete, agrees with disk."""
    ref = str(data["required_outputs"]["artifact_manifest_ref"])
    listing_path = (manifest_path.parent / ref).resolve()
    if not listing_path.is_file():
        raise _refuse(
            listing_path,
            "the TE 15.4 artifact_manifest.json the manifest cross-references is absent; every "
            "output is hash-listed there and the loader asserts the listing (R-133 control 2)",
        )
    try:
        listing = json.loads(listing_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise _refuse(listing_path, f"hash listing is unreadable ({exc})") from exc
    outputs = listing.get("outputs") if isinstance(listing, Mapping) else None
    if not isinstance(outputs, Mapping):
        raise _refuse(listing_path, "hash listing carries no `outputs` mapping name -> sha256")
    if listing.get("fixture_id") != fixture_id:
        raise _refuse(
            listing_path,
            f"hash listing names fixture {listing.get('fixture_id')!r}, not {fixture_id!r}",
        )
    ledger = data["required_outputs"]["comparison_ledger"]
    present: list[str] = []
    for output in data["required_outputs"]["outputs"]:
        name = str(output)
        digest = outputs.get(name)
        if not isinstance(digest, str) or not _SHA256_RE.match(digest):
            raise _refuse(
                listing_path,
                f"required output {name!r} is not hash-listed with a SHA-256 (TE 15.4: every "
                f"output is hash-listed; R-133 control 2)",
            )
        reference = listing_path.parent / name
        if reference.is_file():
            actual = sha256_of_file(reference)
            if actual != digest:
                raise _refuse(
                    reference,
                    f"hash listing records {digest} but the file on disk hashes to {actual}; "
                    f"the listing disagrees with disk (R-133 control 2)",
                )
            present.append(name)
        elif ledger[name].get("comparison_class") == "toleranced":
            raise _refuse(
                reference,
                "the reference artifact of a toleranced output must be present beside the hash "
                "listing: its VALUES are the expectation a clean run compares within tolerance "
                "(R-139)",
            )
    return listing_path, tuple(present)


def validate_manifest_mapping(
    data: Mapping[str, Any], *, manifest_path: Path, file_sha256: str | None
) -> tuple[str, str, Path, tuple[str, ...]]:
    """Every check of the one schema, in one place. Returns (fixture_id, status, listing, present).

    `file_sha256` is None only when validating a mapping that has not been written yet (the
    candidate writer); the sibling-hash rules then do not apply.
    """
    if not isinstance(data, Mapping):
        raise _refuse(manifest_path, "fixture manifest must be a mapping")
    fixture_id = _require_fixture_id(data.get("fixture_id"), resource=f"{manifest_path}: fixture_id")
    _validate_status_and_sibling(manifest_path, data, file_sha256=file_sha256)
    for area_key, area_name, quantities in CONTENT_AREAS:
        block = data.get(area_key)
        if not isinstance(block, Mapping):
            raise _refuse(
                f"{manifest_path}: {area_key}",
                f"TE 15.2 content area {area_name!r} is absent; all twelve areas are required "
                f"BY NAME (R-133 obligation 1, control 1)",
            )
        for quantity in quantities:
            _validate_quantity(
                manifest_path, area_key, quantity, block.get(quantity.key), fixture_id=fixture_id
            )
    _validate_identity(manifest_path, fixture_id, data)
    _validate_required_outputs(manifest_path, fixture_id, data)
    _validate_apparatus_partitions(manifest_path, fixture_id, data)
    _validate_fixture_bootstrap(manifest_path, fixture_id, data)
    listing_path, present = _validate_hash_listing(manifest_path, fixture_id, data)
    return fixture_id, str(data["status"]), listing_path, present


def load_fixture_manifest(path: Path, *, parsed: Mapping[str, Any] | None = None) -> FixtureManifest:
    """THE read path (R-133): read, parse, validate, hash-check; refuse on any violation.

    Raises
    ------
    IntegrityError
        naming the file and the violated expectation, for every refusal in the module
        docstring. A missing manifest names its path — the state this pass leaves both
        fixture trees in (BLK-02).
    """
    manifest_path = Path(path)
    if not manifest_path.is_file():
        raise _refuse(
            manifest_path,
            "no fixture manifest exists at this path; the manifest is emitted as `candidate` by "
            "a measuring run and frozen by the owner's Q-31 act — it is never authored by hand "
            "and never invented (TE 15.1; BLK-02)",
        )
    file_sha256 = sha256_of_file(manifest_path)
    data = parsed if parsed is not None else _parse_yaml_text(
        manifest_path, manifest_path.read_text(encoding="utf-8")
    )
    fixture_id, status, listing_path, present = validate_manifest_mapping(
        data, manifest_path=manifest_path, file_sha256=file_sha256
    )
    return FixtureManifest(
        path=manifest_path,
        fixture_id=fixture_id,
        status=status,
        sha256=file_sha256,
        data=data,
        artifact_manifest_path=listing_path,
        reference_files_present=present,
    )


# --- W-5 / R-137: apparatus partitions -------------------------------------------------------


def read_embargo_hours(snapshot: ConfigSnapshot) -> int:
    """`configs/experiment.yaml` `embargo_hours`, or refuse naming the field (TC-03e; TE 18.3).

    The apparatus `Partition` carries an embargo like every partition; its VALUE enters from
    configuration at its freeze and never from source — `TBD — freeze gate` today.
    """
    value = snapshot.experiment.get("embargo_hours")
    if _is_tbd(value):
        raise _refuse(
            "configs/experiment.yaml: embargo_hours",
            "absent or unresolved (TBD — freeze gate); an apparatus partition carries the "
            "configured embargo, never a source literal — stop and report (TE 18.3)",
        )
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise _refuse("configs/experiment.yaml: embargo_hours", f"{value!r} is not a positive int")
    return value


def build_apparatus_partitions(
    manifest: FixtureManifest, *, embargo_hours: int
) -> tuple[Partition, ...]:
    """The manifest's declared apparatus partitions as `Partition` objects (R-137; Q4 = A).

    Ids outside the six frozen ids by validation; a frozen id here is unreachable because the
    loader already refused it (control 15), and is refused again so a caller constructing a
    manifest mapping by hand meets the same wall.
    """
    block = manifest.apparatus_partitions
    if not block:
        raise _refuse(
            manifest.path,
            "no apparatus partition declaration; stages 05-07 run a fixture at fixture scale "
            "over the manifest's declared apparatus partitions, never over a frozen id (R-137)",
        )
    out: list[Partition] = []
    for pid, entry in block.items():
        if str(pid) in PARTITION_IDS:
            raise _refuse(
                f"{manifest.path}: apparatus_partitions.{pid}",
                f"{pid!r} is a frozen partition id; a fixture artifact never carries one "
                f"(R-137 control 15)",
            )
        kind = PartitionKind(str(entry["kind"]))
        month = entry.get("validation_month")
        out.append(
            Partition(
                partition_id=str(pid),
                kind=kind,
                train_start=_as_date(entry["train_start"], resource=f"{pid}.train_start"),
                train_end=_as_date(entry["train_end"], resource=f"{pid}.train_end"),
                validation_month=(
                    None if month is None else _as_date(month, resource=f"{pid}.validation_month")
                ),
                embargo_hours=embargo_hours,
            )
        )
    return tuple(out)


# --- W-6 / R-139: the comparison ledger applied -------------------------------------------


def _numeric_leaf_compare(expected: Any, actual: Any, *, tolerance: float, trail: str) -> None:
    if isinstance(expected, Mapping) and isinstance(actual, Mapping):
        if set(expected) != set(actual):
            raise _refuse(trail, f"key sets differ: {sorted(expected)} vs {sorted(actual)}")
        for key in expected:
            _numeric_leaf_compare(expected[key], actual[key], tolerance=tolerance, trail=f"{trail}.{key}")
        return
    if isinstance(expected, list | tuple) and isinstance(actual, list | tuple):
        if len(expected) != len(actual):
            raise _refuse(trail, f"lengths differ: {len(expected)} vs {len(actual)}")
        for index, (e, a) in enumerate(zip(expected, actual, strict=True)):
            _numeric_leaf_compare(e, a, tolerance=tolerance, trail=f"{trail}[{index}]")
        return
    if (
        isinstance(expected, int | float)
        and isinstance(actual, int | float)
        and not isinstance(expected, bool)
        and not isinstance(actual, bool)
    ):
        if abs(float(expected) - float(actual)) > tolerance:
            raise _refuse(
                trail,
                f"value {actual!r} differs from the frozen expectation {expected!r} by more than "
                f"the manifest's declared tolerance {tolerance!r}; a clean run FAILS when a value "
                f"exceeds its declared tolerance and never updates the expected value (TE 13.7)",
            )
        return
    if expected != actual:
        raise _refuse(trail, f"non-numeric leaf {actual!r} differs from expectation {expected!r}")


def _read_values(path: Path) -> Any:
    if path.suffix.lower() in (".json", ".jsonl"):
        text = path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".jsonl":
            return [json.loads(line) for line in text.splitlines() if line.strip()]
        return json.loads(text)
    raise _refuse(
        path,
        f"no value reader for {path.suffix!r} in this pass: a toleranced comparison of a "
        f"{path.suffix} artifact needs pandas/pyarrow, which are not importable here; the "
        f"comparison stops rather than approximating (TS-X-02; TE 18.3)",
    )


def compare_required_outputs(manifest: FixtureManifest, produced_root: Path) -> dict[str, Any]:
    """R-139: compare a produced output tree against the frozen expectations; NEVER update them.

    `exact` -> `sha256_of_file(produced) == listing[output]`; `toleranced` -> every numeric leaf
    within `fp_tolerance.value` of the reference artifact's value, units agreeing. Returns the
    matched-artifact report (WS-20 / TA-17's evidence shape). Raises on the FIRST mismatch,
    naming the file and the violated expectation; the manifest and its listing are pure inputs
    here and are not written (control 23 asserts their bytes are unchanged after a raise).
    """
    if not manifest.is_frozen:
        raise _refuse(
            manifest.path,
            "a comparison is made against a FROZEN expectation only; a candidate manifest "
            "cannot produce WS-20/TA-17 evidence (R-134 control 5)",
        )
    expected = manifest.expected_hashes()
    ledger = manifest.comparison_ledger
    root = Path(produced_root)
    results: dict[str, Any] = {}
    for output in manifest.outputs:
        entry = ledger[output]
        produced = root / output
        if not produced.is_file():
            raise _refuse(produced, "required output absent from the produced tree (TE 15.4)")
        actual = sha256_of_file(produced)
        if entry["comparison_class"] == "exact":
            if actual != expected[output]:
                raise _refuse(
                    produced,
                    f"exact-class ({entry['exact_kind']}) mismatch: produced SHA-256 {actual} != "
                    f"frozen expectation {expected[output]}; exact classes compare for equality, "
                    f"not tolerance, and the expectation is never updated (TE 13.7; NFR-REP-01; "
                    f"R-139 control 21/23)",
                )
            results[output] = {"comparison_class": "exact", "sha256": actual, "matched": True}
            continue
        reference = manifest.artifact_manifest_path.parent / output
        tolerance = float(entry["fp_tolerance"]["value"])
        _numeric_leaf_compare(
            _read_values(reference), _read_values(produced), tolerance=tolerance, trail=str(produced)
        )
        results[output] = {
            "comparison_class": "toleranced",
            "units": entry["units"],
            "fp_tolerance": tolerance,
            "sha256": actual,
            "matched": True,
        }
    return {
        "artifact_class": "matched_artifact_report",
        "fixture_id": manifest.fixture_id,
        "frozen_manifest_hash": manifest.sha256,
        "outputs": results,
    }


def _range_of(block: Mapping[str, Any], key: str, *, resource: str) -> tuple[float, float]:
    entry = block.get(key)
    if not isinstance(entry, Mapping):
        raise _refuse(f"{resource}.{key}", "measured range absent")
    try:
        return float(entry["min"]), float(entry["max"])
    except (KeyError, TypeError, ValueError) as exc:
        raise _refuse(f"{resource}.{key}", "measured range needs numeric min and max") from exc


def assert_run_level_ranges(
    manifest: FixtureManifest, *, runtime_seconds: float, storage_bytes: int
) -> dict[str, Any]:
    """R-139 control 24: runtime and storage inside the manifest's MEASURED ranges (TA-17)."""
    runtime = manifest.data["runtime"]
    resource = f"{manifest.path}: runtime"
    lo, hi = _range_of(runtime, "cpu_total", resource=resource)
    if not (lo <= runtime_seconds <= hi):
        raise _refuse(
            f"{resource}.cpu_total",
            f"measured runtime {runtime_seconds} s is outside the frozen range [{lo}, {hi}] s "
            f"(TA-17's declared runtime tolerance; R-139 control 24)",
        )
    slo, shi = _range_of(runtime, "storage_total", resource=resource)
    if not (slo <= storage_bytes <= shi):
        raise _refuse(
            f"{resource}.storage_total",
            f"measured storage {storage_bytes} bytes is outside the frozen range [{slo}, {shi}] "
            f"(TA-17's declared storage tolerance; R-139 control 24)",
        )
    return {"runtime_seconds": runtime_seconds, "storage_bytes": storage_bytes, "within": True}


# --- board Recs 4-5 (owner-authorised, CR §11.5): stage measurements and multi-run ranges --

#: The machine-readable measurement block each stage fixture path emits under its own
#: output root (board Rec 4 / ML-03): {"stage": ..., "measurements": {area: {key:
#: {"min": n, "max": n, "units": u}}}} — VALUES measured by the run, never invented.
MEASUREMENTS_NAME: Final[str] = "fixture_measurements.json"
#: One per measuring run under the fixture root (board Rec 5 / ML-04): the raw measurement
#: set a later --emit-candidate composes min/max ranges over.
MEASURING_RESULT_PREFIX: Final[str] = "measuring_result_"
#: The two run-level quantities whose composed range may never be zero-width (Rec 5): a
#: single measuring run cannot freeze a RANGE (TE 15.1 measures ranges, not points).
_RANGE_REQUIRED: Final[tuple[tuple[str, str], ...]] = (
    ("runtime", "cpu_total"),
    ("runtime", "storage_total"),
)


def collect_stage_measurements(fixture_root: Path) -> dict[str, dict[str, dict[str, Any]]]:
    """Fold every stage-emitted `fixture_measurements.json` under the fixture root into one
    {area: {key: {"min", "max", "units", "sources"}}} envelope (board Rec 4).

    Raises
    ------
    IntegrityError
        an unreadable block; a block without the `measurements` mapping; two stages
        declaring the same quantity with disagreeing units.
    """
    merged: dict[str, dict[str, dict[str, Any]]] = {}
    for path in sorted(Path(fixture_root).rglob(MEASUREMENTS_NAME)):
        try:
            block = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise _refuse(path, f"stage measurement block unreadable ({exc})") from exc
        stage = str(block.get("stage", path.parent.name))
        measurements = block.get("measurements")
        if not isinstance(measurements, Mapping):
            raise _refuse(path, "a stage measurement block carries a `measurements` mapping")
        for area, quantities in measurements.items():
            if not isinstance(quantities, Mapping):
                raise _refuse(f"{path}: {area}", "area must map quantity -> measured values")
            for key, value in quantities.items():
                if not isinstance(value, Mapping) or "min" not in value or "max" not in value:
                    raise _refuse(
                        f"{path}: {area}.{key}", "a measured quantity carries min and max"
                    )
                slot = merged.setdefault(str(area), {}).setdefault(str(key), {})
                low, high = float(value["min"]), float(value["max"])
                units = str(value.get("units", ""))
                if slot:
                    if str(slot.get("units", "")) != units:
                        raise _refuse(
                            f"{path}: {area}.{key}",
                            f"units {units!r} disagree with an earlier block's "
                            f"{slot.get('units')!r}; one quantity has one unit",
                        )
                    slot["min"] = min(float(slot["min"]), low)
                    slot["max"] = max(float(slot["max"]), high)
                    slot["sources"] = sorted({*slot["sources"], stage})
                else:
                    slot.update({"min": low, "max": high, "units": units, "sources": [stage]})
    return merged


def write_measuring_result(
    fixture_root: Path, *, run_id: str, measurements: Mapping[str, Mapping[str, Any]]
) -> Path:
    """Persist ONE measuring run's raw measurement set (write-once; board Rec 5)."""
    if not _nonempty_str(run_id):
        raise _refuse("measuring_run_id", "a measuring result carries its run's registry id")
    target = Path(fixture_root) / f"{MEASURING_RESULT_PREFIX}{run_id}.json"
    if target.exists():
        raise _refuse(target, "a measuring result is written once per run id (NFR-AUD-01)")
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "kind": "measuring_result",
        "measuring_run_id": run_id,
        "measurements": {a: dict(q) for a, q in measurements.items()},
    }
    target.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8"
    )
    return target


def load_measuring_results(source: Path) -> list[dict[str, Any]]:
    """Persisted measuring results from a fixture root (every `measuring_result_*.json`,
    sorted by file name) or from ONE result file — the Rec 5 `--measuring-runs`
    aggregation input from another environment's fixture root."""
    source = Path(source)
    if source.is_file():
        paths = [source]
    elif source.is_dir():
        paths = sorted(source.glob(f"{MEASURING_RESULT_PREFIX}*.json"))
    else:
        raise _refuse(source, "no measuring result file or fixture root exists at this path")
    results: list[dict[str, Any]] = []
    for path in paths:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise _refuse(path, f"measuring result unreadable ({exc})") from exc
        if not isinstance(payload, Mapping) or payload.get("kind") != "measuring_result":
            raise _refuse(path, "payload does not carry `kind: measuring_result`")
        results.append(dict(payload))
    return results


def compose_measurement_ranges(
    results: Sequence[Mapping[str, Any]],
) -> dict[str, dict[str, dict[str, Any]]]:
    """Board Rec 5 (ML-04): compose min/max over N measuring runs, each run id stamped.

    Every composed field carries `measuring_run_ids` (the per-run provenance, one entry per
    contributing run). A ZERO-WIDTH runtime/storage range refuses: TE 15.1 freezes measured
    RANGES, and a single run (or N identical runs) measures a point, not a range — run the
    fixture again rather than inventing a width.

    Raises
    ------
    IntegrityError
        no results; a result without its run id; disagreeing units for one quantity; a
        zero-width `runtime.cpu_total` or `runtime.storage_total` range.
    """
    if not results:
        raise _refuse(
            "measuring results",
            "no measuring result exists; a candidate's measured ranges compose over at "
            "least one recorded measuring run (TE 15.1; board Rec 5)",
        )
    composed: dict[str, dict[str, dict[str, Any]]] = {}
    for result in results:
        run_id = str(result.get("measuring_run_id", ""))
        if not run_id.strip():
            raise _refuse("measuring result", "carries no measuring_run_id (R-134)")
        measurements = result.get("measurements")
        if not isinstance(measurements, Mapping):
            raise _refuse(f"measuring result {run_id}", "carries no `measurements` mapping")
        for area, quantities in measurements.items():
            for key, value in quantities.items():
                if not isinstance(value, Mapping) or "min" not in value or "max" not in value:
                    raise _refuse(
                        f"measuring result {run_id}: {area}.{key}",
                        "a measured quantity carries min and max",
                    )
                slot = composed.setdefault(str(area), {}).setdefault(str(key), {})
                low, high = float(value["min"]), float(value["max"])
                units = str(value.get("units", ""))
                if slot:
                    if str(slot.get("units", "")) != units:
                        raise _refuse(
                            f"measuring result {run_id}: {area}.{key}",
                            f"units {units!r} disagree with {slot.get('units')!r}",
                        )
                    slot["min"] = min(float(slot["min"]), low)
                    slot["max"] = max(float(slot["max"]), high)
                    slot["measuring_run_ids"] = [*slot["measuring_run_ids"], run_id]
                else:
                    slot.update(
                        {"min": low, "max": high, "units": units, "measuring_run_ids": [run_id]}
                    )
    for area, key in _RANGE_REQUIRED:
        slot = composed.get(area, {}).get(key)
        if slot is None:
            raise _refuse(
                f"measuring results: {area}.{key}",
                "the run-level quantity was never measured; a candidate cannot compose "
                "without it (TE 15.2 Runtime block)",
            )
        if float(slot["min"]) == float(slot["max"]):
            raise _refuse(
                f"measuring results: {area}.{key}",
                f"zero-width range [{slot['min']}, {slot['max']}] over run(s) "
                f"{slot['measuring_run_ids']}; TE 15.1 freezes measured RANGES and a range "
                f"needs at least two measuring runs with distinct measurements — run the "
                f"fixture again rather than inventing a width (board Rec 5 / ML-04)",
            )
    return composed


# --- W-2 / R-134: the candidate writer ----------------------------------------------------


def compose_candidate_manifest(
    identity_declaration: Mapping[str, Any],
    *,
    fixture_id: str,
    measurements: Mapping[str, Mapping[str, Any]],
    measuring_run_id: str,
    outputs: Sequence[str],
    comparison_ledger: Mapping[str, Mapping[str, Any]],
    artifact_manifest_ref: str,
) -> dict[str, Any]:
    """Assemble a `status: candidate` mapping from the owner's identity declaration and a
    measuring run's measurements — every measured field stamped with `measuring_run_id`.

    Nothing is invented: the identity block (citations, limitations, stamps) is the owner's
    declaration; `measurements` is what THIS run measured. The result is validated by the
    same schema before it is returned, so an incomplete run cannot compose a candidate.
    """
    _require_fixture_id(fixture_id, resource="fixture_id")
    if not _nonempty_str(measuring_run_id):
        raise _refuse("measuring_run_id", "a candidate carries its measuring run's registry id")
    data: dict[str, Any] = {"fixture_id": fixture_id, "status": CANDIDATE}
    for area_key, _name, _quantities in CONTENT_AREAS:
        declared = identity_declaration.get(area_key, {})
        measured = measurements.get(area_key, {})
        block: dict[str, Any] = dict(declared) if isinstance(declared, Mapping) else {}
        for key, value in measured.items():
            block[key] = _stamp_measured(value, measuring_run_id)
        data[area_key] = block
    for extra in ("apparatus_partitions", "fixture_bootstrap"):
        if extra in identity_declaration:
            data[extra] = identity_declaration[extra]
    data["required_outputs"] = {
        **data.get("required_outputs", {}),
        "artifact_manifest_ref": artifact_manifest_ref,
        "outputs": list(outputs),
        "comparison_ledger": {k: dict(v) for k, v in comparison_ledger.items()},
    }
    return data


def _stamp_measured(value: Any, measuring_run_id: str) -> Any:
    if isinstance(value, Mapping):
        if any(k in _VALUE_KEYS for k in value):
            return {**value, "measuring_run_id": measuring_run_id}
        return {k: _stamp_measured(v, measuring_run_id) for k, v in value.items()}
    return value


def write_candidate_manifest(path: Path, data: Mapping[str, Any]) -> Path:
    """Write a `candidate` manifest ONCE (never `frozen`; never over an existing file).

    Serialised in YAML's JSON subset with sorted keys — a deterministic write order (TS-X-02)
    that pyyaml parses and that needs no serializer beyond stdlib. Validated by the schema
    before a byte is written; the hash-listing check runs against the listing the run wrote.
    """
    target = Path(path)
    if data.get("status") != CANDIDATE:
        raise _refuse(
            target,
            f"a measuring run writes status {CANDIDATE!r} only; {data.get('status')!r} is the "
            f"owner's Q-31 act and nothing here performs it (R-134 obligation 2)",
        )
    if target.exists():
        raise _refuse(
            target,
            "a manifest already exists at this path; a superseded manifest is preserved, never "
            "overwritten — re-measurement goes through a new candidate and a new freeze act "
            "(R-134 obligation 3; foundation R-13's posture)",
        )
    validate_manifest_mapping(data, manifest_path=target, file_sha256=None)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
    return target


def window_days(manifest: FixtureManifest | IdentityDeclaration) -> tuple[date, ...]:
    """Every calendar day of the cited window, inclusive (a derived enumeration, not a value)."""
    start, end = manifest.window
    return tuple(start + timedelta(days=offset) for offset in range((end - start).days + 1))


# --- the owner's identity declaration: the fixture scope BEFORE a candidate exists ----------

#: The `kind` literal that distinguishes an identity declaration from a manifest.
DECLARATION_KIND: Final[str] = "identity_declaration"


@dataclass(frozen=True)
class IdentityDeclaration:
    """The owner's citation-only declaration of a fixture's identity — NOT a manifest.

    The first measuring run has no manifest to read (a candidate is what it emits), yet it must
    know which window, station and apparatus partitions it runs over and must carry the Q5
    exemption into the seven stage scripts. That knowledge is the owner's transcription of the
    frozen D-numbers — identity by citation — plus the apparatus constants (R-122): partition
    ids and ranges, the reduced-replicate bootstrap declaration. It states NO measured value and
    NO expectation; it can never be compared against, never produce evidence, never be frozen.
    `status` is the fixed literal `"declaration"`; `is_frozen` is always False.
    """

    path: Path
    fixture_id: str
    sha256: str
    data: Mapping[str, Any]

    status: str = "declaration"
    is_frozen: bool = False

    @property
    def identity(self) -> Mapping[str, Any]:
        return self.data["identity"]

    @property
    def window(self) -> tuple[date, date]:
        citation = self.identity["window_citation"]
        return _as_date(citation["start_utc"], resource="window_citation.start_utc"), _as_date(
            citation["end_utc"], resource="window_citation.end_utc"
        )

    @property
    def apparatus_partitions(self) -> Mapping[str, Mapping[str, Any]]:
        block = self.data.get("apparatus_partitions")
        return block if isinstance(block, Mapping) else {}

    @property
    def fixture_bootstrap(self) -> Mapping[str, Any] | None:
        block = self.data.get("fixture_bootstrap")
        return block if isinstance(block, Mapping) else None


#: A declaration may carry `identity`, the Phase 1 input it reads (`inputs.prepared_vtec`,
#: whose hashes are the month's RECORDED eligibility evidence, cited from its
#: `sha256_manifest.json`) and the owner's per-output classification template
#: (`required_outputs.comparison_ledger` without tolerance VALUES); every other TE 15.2 area
#: is a measurement or an expectation and belongs to a manifest emitted by a measuring run.
_DECLARATION_FORBIDDEN_AREAS: Final[tuple[str, ...]] = tuple(
    key for key in AREA_KEYS if key not in ("identity", "inputs", "required_outputs")
)
_DECLARATION_INPUT_KEYS: Final[tuple[str, ...]] = ("prepared_vtec",)


def load_identity_declaration(
    path: Path, *, parsed: Mapping[str, Any] | None = None
) -> IdentityDeclaration:
    """Read and validate an identity declaration (`kind: identity_declaration`).

    Validated with the SAME identity, apparatus-partition and fixture-bootstrap rules as a
    manifest; refuses any of the eleven non-identity TE 15.2 areas (a declaration states no
    measurement, no schema and no expectation), a `status` field (it has none — the two
    statuses belong to manifests), and a `kind` other than the literal.
    """
    declaration_path = Path(path)
    if not declaration_path.is_file():
        raise _refuse(
            declaration_path,
            "no identity declaration exists at this path; the owner transcribes the fixture's "
            "cited identity (D-11/D-20 or D-14) and apparatus constants here before the first "
            "measuring run — nothing here invents it",
        )
    file_sha256 = sha256_of_file(declaration_path)
    data = parsed if parsed is not None else _parse_yaml_text(
        declaration_path, declaration_path.read_text(encoding="utf-8")
    )
    if not isinstance(data, Mapping) or data.get("kind") != DECLARATION_KIND:
        raise _refuse(
            declaration_path,
            f"an identity declaration carries `kind: {DECLARATION_KIND}`; this file does not",
        )
    if "status" in data:
        raise _refuse(
            declaration_path,
            "a declaration has no status; candidate/frozen are manifest states (R-134)",
        )
    forbidden = [key for key in _DECLARATION_FORBIDDEN_AREAS if key in data]
    if forbidden:
        raise _refuse(
            declaration_path,
            f"a declaration states no measurement, schema or expectation; TE 15.2 areas "
            f"{forbidden} belong to a manifest emitted by a measuring run",
        )
    fixture_id = _require_fixture_id(data.get("fixture_id"), resource=f"{declaration_path}: fixture_id")
    if not isinstance(data.get("identity"), Mapping):
        raise _refuse(declaration_path, "the identity block is required")
    inputs = data.get("inputs")
    if inputs is not None:
        stray = [] if not isinstance(inputs, Mapping) else sorted(set(inputs) - set(_DECLARATION_INPUT_KEYS))
        if not isinstance(inputs, Mapping) or stray:
            raise _refuse(
                f"{declaration_path}: inputs",
                f"a declaration's inputs block carries only {list(_DECLARATION_INPUT_KEYS)} "
                f"(the Phase 1 product the run reads, hashes cited from the month's "
                f"sha256_manifest.json); other input quantities are the measuring run's record",
            )
    template = data.get("required_outputs")
    if template is not None:
        ledger = template.get("comparison_ledger") if isinstance(template, Mapping) else None
        if not isinstance(template, Mapping) or set(template) != {"comparison_ledger"}:
            raise _refuse(
                f"{declaration_path}: required_outputs",
                "a declaration carries only the comparison_ledger template (class, units, "
                "exact_kind, producing_path per output); outputs and the hash listing are the "
                "measuring run's",
            )
        if not isinstance(ledger, Mapping):
            raise _refuse(f"{declaration_path}: required_outputs.comparison_ledger", "mapping")
        for output, entry in ledger.items():
            if not isinstance(entry, Mapping) or "fp_tolerance" in entry:
                raise _refuse(
                    f"{declaration_path}: required_outputs.comparison_ledger[{output}]",
                    "a template entry classifies (class, units, exact_kind, producing_path) and "
                    "carries no fp_tolerance VALUE — tolerances are measured, never declared "
                    "(TE 15.1; R-134)",
                )
    for quantity in CONTENT_AREAS[0][2]:
        _validate_quantity(
            declaration_path, "identity", quantity, data["identity"].get(quantity.key),
            fixture_id=fixture_id,
        )
    _validate_identity(declaration_path, fixture_id, data)
    _validate_apparatus_partitions(declaration_path, fixture_id, data)
    _validate_fixture_bootstrap(declaration_path, fixture_id, data)
    return IdentityDeclaration(
        path=declaration_path, fixture_id=fixture_id, sha256=file_sha256, data=data
    )


def load_fixture_scope(
    path: Path, *, parsed: Mapping[str, Any] | None = None
) -> FixtureManifest | IdentityDeclaration:
    """Read whatever the `--fixture-manifest` option names: a manifest, or a declaration.

    One parse, then dispatch on `kind`: `identity_declaration` -> `load_identity_declaration`;
    anything else -> `load_fixture_manifest`. Both paths validate fully; both refuse a missing
    file naming its path. This is the function every stage script's Q5 exemption calls, so
    the exemption is never satisfied by an arbitrary path.
    """
    scope_path = Path(path)
    if not scope_path.is_file():
        raise _refuse(
            scope_path,
            "no fixture manifest or identity declaration exists at this path; a fixture run "
            "carries a validated scope, never a bare flag (Q5 = A's exemption is not a bypass)",
        )
    data = parsed if parsed is not None else _parse_yaml_text(
        scope_path, scope_path.read_text(encoding="utf-8")
    )
    if isinstance(data, Mapping) and data.get("kind") == DECLARATION_KIND:
        return load_identity_declaration(scope_path, parsed=data)
    return load_fixture_manifest(scope_path, parsed=data)
