"""C-1 Resolve: configs, platform, credentials, seeding, the environment lock — and the exception base.

Purpose
-------
Two responsibilities live in this module.

**First: C-1 Resolve** (`logical-components.md`). The only module that reads
`configs/` (R-15). It loads, snapshots and hashes the four governed configs
(W-2), runs the TE 18.3 preflight assertions (W-3: `assert_no_tbd`,
`assert_declared_sources_exist`), resolves the platform and its roots without
ever touching a credential value (W-8, R-14, SD-02), applies determinism before
any graph construction (W-4, R-05, R-06) and captures the eight-item per-run
environment lock (W-5, REQ-ENG-10, TE 13.1). A bad or incomplete resolve fails
the run loudly and locally; no persisted state is altered.

**Second: the exception hierarchy.**
`foundation` R-01 fixes one rule: **every project-defined exception derives from
`IntegrityError`**, whose base lives here in `src/data/config.py`. R-01 deliberately
stopped asserting a *count* after its enumeration went stale twice; the named classes
below are a **named subset**, not a completeness claim, and any future integrity-related
exception derives from the same base whether or not it is listed here.

Inputs
------
`configs/data.yaml`, `configs/features.yaml`, `configs/experiment.yaml`,
`configs/seeds.yaml` (via `load_configs` only); the process environment (via
`resolve_platform_roots` and `ensure_process_determinism`); `requirements.txt`
and `git HEAD` (via `capture_environment_lock`). This module imports nothing
from the project and is importable from every package, which is why it is the
exception declaration site: `component-dependency.md` marks
`src/features` -> `src/models` and `src/data` -> `src/models` both as absent, so an
exception declared under `src/models/` could not be raised by `src/data/splits.py` or by
anything under `src/features/`. **No framework and no third-party package is
imported at module scope** (R-05: `ensure_process_determinism` must run before
any framework import, and this module is imported before it runs; the
prohibition is transitive). `yaml`, `numpy` and `tensorflow` are imported
inside the functions that need them.

Re-run behaviour
----------------
Importing this module has no side effects and is idempotent. `load_configs`
writes one verbatim snapshot per call under the platform's snapshot root and
never mutates `configs/`; re-running produces a new snapshot directory and
identical hashes for identical files. `ensure_process_determinism` re-execs the
interpreter at most once per process (recorded in
`DeterminismRecord.reexec_performed`, never mistaken for a double run). The
preflight assertions and the credential presence check are pure reads. No
function here reads, returns, logs, serializes, interpolates or persists a
credential VALUE (R-14; SD-02) and no code path constructs a path into the
restricted December evidence root (R-15; SD-05: only `src/data/locked_test.py`,
owned by `governance-guards`, may reach it — this module does not even name it).

Governance
----------
* `foundation` R-01 -- the hierarchy and the `src/data/config.py` base.
* `PartitionError` was promoted into R-01's enumeration as its fifteenth entry under
  `GOV-2026-08-28-FD-01` Recommendation 8, and its **declaration site was ruled to be this
  module** by the project decision owner on 2026-08-28, amending the wording of that
  ruling. `models-and-baselines` remains the exception's semantic owner (R-92's
  `PartitionError` / `LeakageError` discriminating rule is unchanged); it is no longer its
  declaration site.
* `InverseTransformError` rides R-01's "any future integrity-related exception" clause and
  is **not** a sixteenth enumerated entry -- `foundation` R-01's dated box records the
  three reasons, the first being that the two units raising it agree on its condition and
  meaning, so nothing needs reconciling.
* `ImportBoundaryError`, `FeatureAvailabilityError`, `BenchmarkError` and
  `ComparatorError` (unit `external-products`, Q1 = A receipted 2026-09-05, extending the
  nfr-design Q2 = A ruling) likewise ride the any-future clause: each is raised by one
  unit with one meaning, so nothing needs reconciling, and none is an enumeration entry.
  Declared here because the whole point of the TE 12 import allowlist is that
  `src/features` and `src/models` CANNOT import `src/external` -- a package forbidden
  from importing a leaf module must still be able to catch what it raises.
* `StandardizationError` (unit `target-standardization`, code-generation Q1 = A receipted
  at the 3.5 plan gate, resolving DISC-T-1) rides the any-future clause identically:
  raised by one unit with one meaning, so nothing needs reconciling, and it is not an
  enumeration entry. Declared here because R-01 makes this module the declaration site,
  and DISC-T-1's set-difference against this file's `__all__` was exactly
  `{StandardizationError}` (`PhaseBoundaryError` was already present).
* **`DriverError` is deliberately NOT declared.** Its scope is contested upstream:
  `external-products`' `business-logic-model.md` carried Finding 9 (Major), recording
  that `domain-entities.md` section 9's `DriverError` cell was annotated without being
  changed, so the artifact specifies both readings at once -- `DriverError` both is and
  is not the exception for the two alignment conditions that `AlignmentError` in fact
  owns. Placing an exception whose raise-conditions are self-contradictory would fix the
  wrong thing; the declaration waits on the domain-entities reconciliation. Until then,
  conditions that would have raised `DriverError` (mixed release grades, grade
  ineligibility, driver hash mismatch) raise the `IntegrityError` base directly, naming
  resource and expectation, so nothing is silently misclassified.
* Constructor contract (R-01): every raise names the file or resource **and** the violated
  expectation. `IntegrityError` enforces the shape rather than trusting each call site.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform as _platform
import random
import shutil
import subprocess
import sys
import uuid
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from dataclasses import fields as _dataclass_fields
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Final

__all__ = [
    # C-1 Resolve
    "TBD_SENTINEL",
    "GOVERNED_CONFIG_FILES",
    "REEXEC_SENTINEL_ENV",
    "ConfigSnapshot",
    "DeterminismRecord",
    "RunRecord",
    "REQUIRED_FIELDS_MAP",
    "CREDENTIAL_NAME_MAP",
    "load_configs",
    "assert_no_tbd",
    "assert_declared_sources_exist",
    "assert_config_hashes_match",
    "resolve_platform_roots",
    "required_fields_for",
    "credential_names_for",
    "assert_credential_names_present",
    "seed_everything",
    "ensure_process_determinism",
    "reexec_performed",
    "capture_environment_lock",
    "environment_lock_hash",
    "assert_lock_complete",
    # exception hierarchy (R-01)
    "IntegrityError",
    "ConfigError",
    "PreflightError",
    "PlatformError",
    "DeterminismError",
    "ReleaseError",
    "RegistryError",
    "PhaseBoundaryError",
    "LockedTestError",
    "LeakageError",
    "AlignmentError",
    "SeedError",
    "FairnessError",
    "BootstrapError",
    "RegimeError",
    "PartitionError",
    "InverseTransformError",
    "InventoryError",
    "SchemaError",
    "AuditScopeError",
    "ImportBoundaryError",
    "FeatureAvailabilityError",
    "BenchmarkError",
    "ComparatorError",
    "StandardizationError",
]


class IntegrityError(Exception):
    """Base for every project-defined integrity violation.

    R-01's constructor contract: a raise names the **resource** and the **violated
    expectation**. Both are required, because `team.md` fixes the two-tier error posture --
    an integrity violation terminates the run with a message naming the file and the
    expectation, while a completeness shortfall is recorded as a machine-readable field
    instead. A message that names neither cannot be acted on by the person reading the
    traceback.
    """

    def __init__(self, resource: object, expectation: str) -> None:
        resource_text = str(resource)
        if not resource_text:
            raise ValueError(
                "IntegrityError requires a non-empty resource: R-01's constructor "
                "contract is that every raise names the file or resource it concerns"
            )
        if not expectation:
            raise ValueError(
                "IntegrityError requires a non-empty expectation: R-01's constructor "
                "contract is that every raise names the violated expectation"
            )
        self.resource = resource_text
        self.expectation = expectation
        super().__init__(f"{resource_text}: {expectation}")


# --- foundation's own six -------------------------------------------------------------

class ConfigError(IntegrityError):
    """A governed config file is missing, malformed, or carries an unresolved `TBD`."""


class PreflightError(IntegrityError):
    """A TE 18.3 preflight precondition is unmet."""


class PlatformError(IntegrityError):
    """Execution is attempted on a platform TC-03c does not authorise."""


class DeterminismError(IntegrityError):
    """A run that must be reproducible is not."""


class ReleaseError(IntegrityError):
    """A dataset release violates its 13.3 contract.

    Raised by `write_release` for a missing 13.3 field, a `dataset_version` that is not
    the first 12 hex of its own `content_hash`, a 12-hex prefix already naming a
    *different* `content_hash` (D-29's verify-on-write check), and by R-13's refusal to
    write into a directory that already contains a release.
    """


class RegistryError(IntegrityError):
    """A registry invariant is violated — and TWO registries share this class (SD-I-03).

    **Experiment registry** (`foundation`, TE 13.4, R-08/R-18): a registry write would be
    lost, silently overwritten, or reordered.

    **Station registry** (`inventory-and-registry`, `src/data/registry.py`, W-2/R-45..R-48):
    a Vision 6.2 field is missing; `igrf_version` is a default rather than a pin; a field's
    provenance is absent or insufficient for the requesting consumer; a resolved conflict
    value does not equal the single value of the source it NAMES, or carries an empty
    rationale; a migration changed a frozen value.

    The two are discriminated by `resource`, not by type: every station-registry raise
    names its registry artifact or `station_id` as the resource, while experiment-registry
    raises name the registry file. A caller that must tell them apart reads `.resource`.
    Type-level separation (`StationRegistryError`) remains available only as a change
    record against the approved `functional-design` contract and is deliberately NOT
    taken here (Q3 = A).
    """


# --- raised by other units, declared here so every package can import them -------------

class PhaseBoundaryError(IntegrityError):
    """Phase 1 code reached a raw-processing module or field (NFR-PHASE-01)."""


class LockedTestError(IntegrityError):
    """A restricted-root read was attempted outside the `open_restricted` chokepoint.

    Also raised when the access-log write fails: a failed log write **aborts the read**
    rather than proceeding unlogged (`component-methods.md`, `open_restricted`).
    """


class LeakageError(IntegrityError):
    """Information from outside a partition's training range reached a fitted object."""


class AlignmentError(IntegrityError):
    """A driver series did not align onto the hourly grid as its contract requires."""


class SeedError(IntegrityError):
    """A seed was defaulted, inlined, or chosen on validation."""


class FairnessError(IntegrityError):
    """A comparison used a pairwise or model-specific mask (NFR-FAIR-01, TC-16)."""


class BootstrapError(IntegrityError):
    """The vector time-block bootstrap was constructed contrary to TE 13.6."""


class RegimeError(IntegrityError):
    """A regime classification or count violated its configured contract."""


class PartitionError(IntegrityError):
    """A frame reached a scoring path for a partition it does not belong to.

    R-92's discriminating rule, unchanged: a `partition_id` disagreement or a training
    partition reaching a score path raises **`PartitionError`**; a `transform_id`
    disagreement or a `None` transform raises **`LeakageError`**. The first is a
    declared-identity disagreement; the second implies information flow.
    """


# --- riding R-01's any-future clause ---------------------------------------------------

class InverseTransformError(IntegrityError):
    """An inverse transform was not applied before a metric was computed.

    Not an enumerated entry of R-01: it rides the "any future integrity-related exception"
    clause. `evaluation-and-comparison` and `statistical-inference` both raise it for the
    same condition with the same meaning, so there is no cross-unit disagreement to
    reconcile -- which is the discriminator that promoted `PartitionError` and does not
    apply here. Per D-27 the **primary** path needs no inverse transform (its target stays
    raw TECU); this exception guards `ABL-DIFF`, the sole configuration that transforms the
    target.
    """


class InventoryError(IntegrityError):
    """A source-inventory invariant is violated (`inventory-and-registry` W-1, R-44).

    Raised when a source entry carries fewer than TE 5.1's nine fields (the failure names
    the entry AND the missing field, not the file alone); when a released artifact's bytes
    do not match its release hash; or when a notice-requiring provider's verbatim
    acknowledgment text is absent or paraphrased (FR-P1-01-6). Rides R-01's "any future
    integrity-related exception" clause — raised by one unit, nothing to reconcile, so it
    is deliberately NOT an enumeration entry (Q1 = A, 2026-09-05; the `SchemaError`
    extension of that ruling receipted the same day).
    """


class SchemaError(IntegrityError):
    """The prepared product does not match its governed expected schema (W-5, R-49).

    Raised when a parameter name, unit, fill value, UTC cadence or duplicate policy does
    not match the `PreparedSchema` block in `configs/data.yaml` — each mismatch class is a
    separate raise, never one aggregate. Declared here identically to `InventoryError`
    and `AuditScopeError` per the receipted Q1 = A ruling (2026-09-05), riding R-01's
    any-future clause: one raising unit, nothing to reconcile, not an enumeration entry.
    """


class AuditScopeError(IntegrityError):
    """The December audit's declared scope fails a scope check (W-6, R-50, SD-I-04).

    Raised BEFORE any read when the declared scope does not equal the governed reference
    set (twelve 2022 months, December at day granularity 1-31, all three cells, the named
    artifact classes), and at reconciliation when the access rows written (3a, per
    `run_id`) or the report's per-month output (3b, all twelve months, December included)
    do not reconcile against the declaration. **The `resource` is the declared scope,
    never a file path** — a check-1 raise happens before any artifact is opened, and
    naming a file would imply a read that did not occur. Rides R-01's any-future clause
    (Q1 = A, 2026-09-05); not an enumeration entry.
    """


class ImportBoundaryError(IntegrityError):
    """A module outside the TE 12 allowlist can reach `iri` or `gim` (unit external-products).

    The allowlist, at module-path granularity: `scripts/04_build_external_products.py`
    and modules under `src/evaluation/` -- exactly two paths (TE 12; TA-07; R-56). An
    import from `src/data`, `src/features`, `src/models`, `src/gnss`, a training script,
    a test or a notebook violates it identically.

    Constructor contract, extended per SD-E-02: the `resource` is the offending module
    path, and the `expectation` names the full reachability CHAIN -- every hop, not just
    the endpoint -- because a transitive violation whose message names only `gim` tells
    an implementer nothing about which hop to cut. Rides R-01's any-future clause
    (Q1 = A, 2026-09-05); not an enumeration entry.
    """


class FeatureAvailabilityError(IntegrityError):
    """Driver-availability resolution had to stop rather than choose a default (R-57a).

    Raised when the next daily F10.7 median is not available at a forecast origin while
    `configs/features.yaml`'s `carry_forward_composition` field is `TBD` or absent. The
    raise names the origin timestamp, the last available median's day, and the elapsed
    staleness in BOTH units (clock hours and whole daily steps), then stops -- it never
    silently carries forward and never silently excludes (TE 18.3: "must stop and report
    rather than choose a default"; D-21/G-04). Also raised on a violation of the
    composition once the Student's G-04 freeze fills the field. Rides R-01's any-future
    clause (nfr-design Q2 = A; Q1 = A, 2026-09-05); not an enumeration entry.
    """


class BenchmarkError(IntegrityError):
    """The IRI benchmark gate refused (R-59, FR-P1-04-15; unit external-products).

    Raised when generation is attempted without a passing pre-declared validation
    report; when the report is missing any of its seven content areas; when the
    tolerance's recorded timestamp does not precede the comparison; or when the
    benchmark's own drivers are absent from the frozen availability matrix. A
    validation failure BLOCKS generation rather than warning, and the implementation
    is never silently switched on failure (R-59). Rides R-01's any-future clause
    (Q1 = A, 2026-09-05); not an enumeration entry.
    """


class ComparatorError(IntegrityError):
    """The GIM comparator gate refused (R-60, FR-P1-04-18, FR-P1-04-9).

    Raised when generation is attempted while the Q-15 interpolation rule is UNSET (a
    TE 18.2 Student-owned forbidden choice); when the interpolation hand-check's
    timestamp does not precede generation (EV-11 -- a retrospective hand-check is not
    accepted); when the overlap audit's recorded timestamp does not precede generation;
    or when a GIM comparison artifact exists with no registered overlap-audit result and
    flag value (the disclosure trigger is the COMPARISON'S EXISTENCE, Vision 6.10).
    Rides R-01's any-future clause (Q1 = A, 2026-09-05); not an enumeration entry.
    """


class StandardizationError(IntegrityError):
    """A target-standardization invariant is violated (unit `target-standardization`).

    Raised when a fifth transformation appears beyond the closed four-member set
    (documented QC, UTC normalization, D-1's half-open floor cell selection, D-16's
    median hourly aggregation — R-64); when the aggregation statistic resolves to a
    default rather than to D-16, or is configured without its D-16 citation (R-65);
    when `configs/data.yaml`'s `qc_operations` list is absent or `TBD — freeze gate`
    at a target-producing run (Q2 = A: the run REFUSES and no standardized target is
    produced — the raise names the field and the expectation that the list be frozen
    under a D-number, never mere non-emptiness, because a list filled by convenience
    satisfies "non-empty" and is exactly what TE 18.2 forbids); on a D-17 contract
    defect (config drift from D-17's sixteen fields, a row defect, a substituted
    excluded set — the two layers fail with messages saying which broke); on an
    unexplained negative VTEC; on an uncertainty-budget defect; and on a prohibited
    "receiver-specific station-observed" labelling of the gridded product.

    Rides R-01's any-future clause (code-generation Q1 = A, resolving DISC-T-1):
    raised by one unit with one meaning, so nothing needs reconciling, and it is NOT
    an enumeration entry. `domain-entities.md` § 9's `TargetQualityError` and
    `BudgetError` names are deliberately NOT declared — the receipted ruling covered
    exactly `{StandardizationError}`, and applying it to names the owner was not
    shown would be the widening this project has already had to correct; their
    conditions raise this class, naming resource and expectation.
    """


# =======================================================================================
# C-1 Resolve
# =======================================================================================

#: The literal sentinel every unfrozen governed scientific field carries. NEVER filled
#: by an implementer or agent by convenience (Vision 1.2; TE 1.1; project.md Forbidden).
TBD_SENTINEL: Final[str] = "TBD — freeze gate"

#: Exactly four governed config files (TE 12; TC-03e). No fifth is ever introduced.
GOVERNED_CONFIG_FILES: Final[tuple[str, ...]] = (
    "data.yaml",
    "features.yaml",
    "experiment.yaml",
    "seeds.yaml",
)

#: The re-exec sentinel environment variable (R-05). An implementation identifier, not a
#: scientific constant or governed config field: set by the parent immediately before
#: `os.execv`, read ONCE by the child in `ensure_process_determinism` and immediately
#: removed, so a subprocess of a re-exec'd script never inherits it.
REEXEC_SENTINEL_ENV: Final[str] = "TEC_FOUNDATION_REEXEC"

#: The PYTHONHASHSEED value the re-exec establishes (WS-17 precondition; engineering
#: constant, not scientific).
_PYTHONHASHSEED_VALUE: Final[str] = "0"

#: Module-level state carrying the re-exec bit from the pop (W-1 step 1) to the
#: `DeterminismRecord` (W-4 step 4). Intra-module by design — see R-05.
_REEXEC_PERFORMED: bool = False

#: Platforms whose write-durability semantics have MEASURED evidence. Empty until W-6
#: step 8's measurement obligation (Bolt 1's in-Kaggle work) is discharged; extending
#: this set requires that measured evidence, never an assumption (SD-03, Q3=B).
CHARACTERISED_DURABILITY_PLATFORMS: Final[frozenset[str]] = frozenset()

#: Environment markers of the platform Google Colab, which is explicitly REMOVED as a
#: governed platform (TE 9.1; Vision 8.3; TC-03c). Their presence is a PlatformError.
_COLAB_MARKERS: Final[tuple[str, ...]] = ("COLAB_RELEASE_TAG", "COLAB_GPU", "COLAB_JUPYTER_IP")

#: Kaggle detection markers. Only NAMES are consulted; no value is read beyond the
#: platform label check — never a credential (R-14).
_KAGGLE_MARKERS: Final[tuple[str, ...]] = ("KAGGLE_KERNEL_RUN_TYPE", "KAGGLE_URL_BASE")


@dataclass(frozen=True)
class ConfigSnapshot:
    """The approved stage-2.6 contract, unchanged (component-methods.md; domain-entities 1).

    Created once per run by `load_configs`, frozen, passed by value. A run that needs
    different configuration is a different run. No machine path enters the four configs
    (R-16); machine paths live only in `resolved_roots`.
    """

    data: Mapping[str, object]
    features: Mapping[str, object]
    experiment: Mapping[str, object]
    seeds: Mapping[str, object]
    hashes: Mapping[str, str]
    snapshot_dir: Path
    resolved_roots: Mapping[str, Path]
    platform: str


@dataclass(frozen=True)
class DeterminismRecord:
    """The approved nine-field contract (component-methods.md; Amendment B, 2026-08-24).

    Produced by `seed_everything` after `ensure_process_determinism` and before any graph
    construction. An empty `nondeterministic_ops` is NEVER proof of determinism (R-06):
    `probe_scope` records what was examined and `measurement_status` distinguishes
    `complete` from `partial` and `not-yet-measured`. Does NOT carry the bootstrap seed —
    that carve-out is `src/evaluation/bootstrap.py` by ADR-05.
    """

    seeds_applied: Mapping[str, int]
    pythonhashseed: str
    reexec_performed: bool
    framework_versions: Mapping[str, str]
    tf_op_determinism: bool
    nondeterministic_ops: Sequence[str]
    probe_scope: Sequence[str]
    measurement_status: str  # "complete" | "partial" | "not-yet-measured"
    declared_vs_observed_mismatches: Sequence[str]


@dataclass(frozen=True)
class RunRecord:
    """The eight-field per-run environment lock (REQ-ENG-10; TE 13.1; domain-entities 5).

    Eight fields over TE 13.1's seven bullets — bullet 1 names two separately capturable
    artifacts (the pinned `requirements.txt` hash and a per-run `pip freeze`). Opened at
    W-1 step 6, before any domain work, so an aborted run is already visible. Every field
    is populated, not "unavailable": `assert_lock_complete` fails the run rather than
    letting it complete silently.
    """

    requirements_hash: str
    pip_freeze: str
    runtime_versions: Mapping[str, str]
    code_commit: str
    config_hashes: Mapping[str, str]
    input_versions: Sequence[str]
    platform: str
    nondeterministic_ops: Sequence[str]


#: `RequiredFieldsMap` (FU-1 = C; domain-entities 2): `(stage_slug, phase)` -> field
#: paths (dotted, first segment naming the config) that must be present and non-TBD for
#: that stage-phase pair. A declarative structure, NOT a governed config file — it names
#: field identities, never values, so it carries no scientific constant. Completeness is
#: asserted by test (R-03), not trusted. Entries are added as their owning stages land;
#: the phase is in the KEY because a Phase-2 field is legitimately TBD during Phase 1
#: (TE 7.0) and a stage-only key would force listing either the union or the
#: intersection, both wrong.
REQUIRED_FIELDS_MAP: Final[Mapping[tuple[str, int], tuple[str, ...]]] = {
    # Foundation's own preflight: the frozen D-122 seed values must be resolved for any
    # run that seeds (every run).
    ("foundation", 1): (
        "seeds.development",
        "seeds.final",
        "seeds.bootstrap",
    ),
    # Acquisition's preflight (unit `acquisition`, stage 3.5): the D-144-frozen
    # Madrigal experiment/kindat/parameter identity set that R-30 requires
    # `00_acquire_prepared_vtec.py` to RESOLVE FROM configs/data.yaml, never choose
    # — plus the development seed its seeding step applies. Field IDENTITIES only,
    # never values (the map's own rule). Two of D-144's four attached freezes remain
    # open and the transcription into data.yaml is its owner's: until it lands, this
    # entry makes the script REFUSE at the TE 18.3 preflight, naming the absent
    # fields, rather than letting an implementer default them (TE 18.2/18.3).
    ("acquisition", 1): (
        "data.acquisition.experiment",
        "data.acquisition.kindat",
        "data.acquisition.parameters",
        "seeds.development",
    ),
    # inventory-and-registry's preflight (stage 3.5): deliberately MINIMAL. The
    # registry's own fields (data.stations, data.cell_rule, the IGRF pin) are NOT
    # listed here, because Q2 = A (receipted 2026-09-05) fixes their enforcement
    # point: data.yaml keeps its `TBD — freeze gate` sentinels until the ONE
    # pre-G-P1A freeze event, and `src/data/registry.py` REFUSES at runtime until
    # then — a blanket preflight entry would bar the script's permitted
    # non-registry, non-December paths, which the approved plan requires to run.
    ("inventory-and-registry", 1): ("seeds.development",),
    # external-products' preflight (stage 3.5): deliberately MINIMAL, the same shape as
    # inventory-and-registry's Q2 = A entry. `features.carry_forward_composition` is NOT
    # listed here BY DESIGN: its enforcement point is driver-availability resolution,
    # which raises FeatureAvailabilityError while the field is TBD (R-57a, D-21/G-04) --
    # a blanket preflight entry would bar the script's permitted driver-audit path and
    # its refusal-attempt paths, which the approved plan requires to run (the refusals
    # ARE the deliverable). The IRI/GIM gates refuse at their own entry points (R-59,
    # R-60), never through this map.
    ("external-products", 1): ("seeds.development",),
    # target-standardization's preflight (stage 3.5): deliberately MINIMAL, the same
    # shape as inventory-and-registry's and external-products' entries, and required
    # because `required_fields_for` refuses an absent entry outright — the stage script
    # cannot run any path, including its own mandated refusal path, without one.
    # `data.qc_operations` is NOT listed here BY DESIGN (Q2 = A): its enforcement point
    # is the target-producing run, which raises StandardizationError naming the field
    # and the frozen-under-a-D-number expectation while the list is TBD or absent. A
    # blanket preflight entry would bar the script's permitted non-target paths and the
    # refusal-attempt path itself, and the refusal IS the deliverable. Field IDENTITIES
    # only, never values (the map's own rule).
    ("target-standardization", 1): ("seeds.development",),
    # features-and-splits' preflight (stage 3.5): deliberately MINIMAL, the same shape as
    # the three entries above. `data.partitions`, `experiment.embargo_hours`,
    # `experiment.window_length_hours`, `features.feature_dictionary`,
    # `features.availability_lags` and `features.permitted_producers` are NOT listed here
    # BY DESIGN: each is enforced at its own entry point (`build_partitions` raises
    # PartitionError; `read_window_length` / `build_features` raise LeakageError;
    # `load_feature_dictionary` raises PreflightError; `read_availability_lags` raises
    # FeatureAvailabilityError; `load_permitted_producers` raises LeakageError naming which
    # rows lack entries) — the refusals ARE this unit's deliverable while the values stay
    # unfrozen (SD-F-01, Q1 = A), and a blanket preflight entry would bar the script's
    # honest `aborted` registry row, which the approved plan requires. Field IDENTITIES
    # only, never values (the map's own rule).
    ("features-and-splits", 1): ("seeds.development",),
}

#: `CredentialNameMap` (FU-3 = A, Q8 = D; domain-entities 3): `(stage_slug, provider)`
#: (optionally `(stage, provider, phase)`) -> environment-variable NAMES — never values.
#: `foundation` declares and hosts this map and never consumes a credential value; only
#: stages that actually require authenticated provider access apply the presence check
#: (SD-02). Empty until `acquisition` names its providers: a shape without contents,
#: exactly as `logical-components.md` records.
CREDENTIAL_NAME_MAP: Final[Mapping[tuple[str, ...], tuple[str, ...]]] = {}


# --- W-2: load, snapshot, hash, resolve -------------------------------------------------


def _parse_yaml(path: Path) -> Mapping[str, Any]:
    """Strict YAML load with duplicate-key rejection (W-2 step 2).

    A duplicate key silently dropping a governed value is an integrity failure, not a
    parse convenience. `yaml` is imported here, not at module scope (R-05 transitive
    module-scope import prohibition).
    """
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - environment defect, not logic
        raise ConfigError(path, f"pyyaml is required to parse governed configs ({exc})") from exc

    class _StrictLoader(yaml.SafeLoader):
        pass

    def _no_duplicates(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise ConfigError(
                    path,
                    f"duplicate key {key!r} at line {key_node.start_mark.line + 1}; a "
                    f"duplicate key silently dropping a governed value is an integrity "
                    f"failure",
                )
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    _StrictLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_duplicates
    )

    if not path.is_file():
        raise ConfigError(path, "governed config file is missing (TE 12 mandates all four)")
    try:
        # _StrictLoader derives SafeLoader; only duplicate-key rejection is added.
        loaded = yaml.load(  # noqa: S506
            path.read_text(encoding="utf-8"), Loader=_StrictLoader  # noqa: S506
        )
    except ConfigError:
        raise
    except yaml.YAMLError as exc:
        raise ConfigError(path, f"governed config is unparseable: {exc}") from exc
    if loaded is None:
        loaded = {}
    if not isinstance(loaded, dict):
        raise ConfigError(path, "governed config must be a mapping at the top level")
    return loaded


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_snapshot(config_dir: Path, snapshot_dir: Path) -> None:
    """Verbatim copies of the four files (W-2 step 3).

    Verbatim because the snapshot is the evidence of what the run actually read; a
    re-serialised copy proves the parser's behaviour, not the file's content.
    """
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    for name in GOVERNED_CONFIG_FILES:
        shutil.copyfile(config_dir / name, snapshot_dir / name)


def resolve_platform_roots(env: Mapping[str, str]) -> tuple[str, Mapping[str, Path]]:
    """W-8: identify the platform as exactly `kaggle` or `local`, resolve roots.

    Returns the label and roots. No credential value is read, returned, logged,
    serialized, interpolated or persisted — here or in any foundation-layer diagnostic
    (R-14, SD-02). Only environment NAMES listed in this module's constants are
    consulted, none of them secret-bearing.

    Raises
    ------
    PlatformError
        when the platform is not exactly one of the two TC-03c authorises. A Colab
        marker is an explicit refusal, not an unknown: Colab was removed as a governed
        platform (TE 9.1, Vision 8.3).
    """
    explicit = env.get("TEC_PLATFORM")
    if explicit is not None:
        if explicit not in ("kaggle", "local"):
            raise PlatformError(
                "TEC_PLATFORM",
                f"platform {explicit!r} is not one of the exactly two authorised "
                f"platforms 'kaggle' | 'local' (TC-03c); no third platform exists",
            )
        label = explicit
    elif any(marker in env for marker in _KAGGLE_MARKERS):
        label = "kaggle"
    elif any(marker in env for marker in _COLAB_MARKERS):
        raise PlatformError(
            "platform",
            "a Google Colab environment marker is present; Colab is explicitly removed "
            "as a governed platform (TE 9.1; Vision 8.3; TC-03c)",
        )
    else:
        label = "local"

    if label == "kaggle":
        workspace = Path("/kaggle/working")
    else:
        override = env.get("TEC_WORKSPACE_ROOT")
        workspace = Path(override) if override else Path.cwd()

    roots: dict[str, Path] = {
        "workspace": workspace,
        "artifacts": workspace / "artifacts",
    }
    return label, roots


def load_configs(config_dir: Path, *, phase: int) -> ConfigSnapshot:
    """W-2: read, snapshot, hash and resolve — the only read of `configs/` (R-15).

    Raises
    ------
    ConfigError
        a file missing or unparseable; `phase` not in {1, 2}; a config-declared root
        that is an absolute path (R-16: no machine path enters a governed config).
    PlatformError
        the platform is not exactly one of the two authorised.
    """
    if phase not in (1, 2):
        raise ConfigError(config_dir, f"phase must be 1 or 2, got {phase!r}")

    config_dir = Path(config_dir)
    parsed: dict[str, Mapping[str, Any]] = {}
    for name in GOVERNED_CONFIG_FILES:
        parsed[name.removesuffix(".yaml")] = _parse_yaml(config_dir / name)

    label, roots = resolve_platform_roots(os.environ)
    resolved_roots = dict(roots)

    declared_roots = parsed["data"].get("roots", {})
    if isinstance(declared_roots, Mapping):
        for key, value in declared_roots.items():
            rel = Path(str(value))
            if rel.is_absolute():
                raise ConfigError(
                    config_dir / "data.yaml",
                    f"roots.{key} is an absolute path ({value!r}); no machine path may "
                    f"enter a governed config (R-16, ADR-07)",
                )
            resolved_roots[str(key)] = resolved_roots["workspace"] / rel

    snapshot_base = resolved_roots.get(
        "snapshot_root", resolved_roots["artifacts"] / "run_snapshots"
    )
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    snapshot_dir = Path(snapshot_base) / f"{stamp}-{uuid.uuid4().hex[:8]}"
    _write_snapshot(config_dir, snapshot_dir)

    hashes = {
        name: _sha256_bytes((config_dir / name).read_bytes()) for name in GOVERNED_CONFIG_FILES
    }

    return ConfigSnapshot(
        data=parsed["data"],
        features=parsed["features"],
        experiment=parsed["experiment"],
        seeds=parsed["seeds"],
        hashes=hashes,
        snapshot_dir=snapshot_dir,
        resolved_roots=resolved_roots,
        platform=label,
    )


def assert_config_hashes_match(snapshot: ConfigSnapshot) -> None:
    """Re-hash the snapshot copies against the recorded hashes.

    A governed-config hash mismatch is an integrity violation and terminates, naming the
    file and the violated expectation — never a warning (two-tier posture; team.md).
    """
    for name in GOVERNED_CONFIG_FILES:
        copy = snapshot.snapshot_dir / name
        if not copy.is_file():
            raise ConfigError(copy, "snapshot copy of a governed config is missing")
        actual = _sha256_bytes(copy.read_bytes())
        recorded = snapshot.hashes.get(name, "")
        if actual != recorded:
            raise ConfigError(
                copy,
                f"snapshot copy no longer matches the recorded governed hash "
                f"(recorded {recorded}, actual {actual}); a mutated snapshot cannot "
                f"evidence what the run read",
            )


# --- W-3: the TE 18.3 preflight ---------------------------------------------------------


def _lookup_path(parsed: Mapping[str, Mapping[str, Any]], dotted: str) -> tuple[bool, Any]:
    """Resolve a dotted field path whose first segment names the config file."""
    parts = dotted.split(".")
    node: Any = parsed.get(parts[0], _MISSING)
    for part in parts[1:]:
        if not isinstance(node, Mapping) or part not in node:
            return False, None
        node = node[part]
    if node is _MISSING:
        return False, None
    return True, node


_MISSING: Final[object] = object()


def _configs_of(snapshot: ConfigSnapshot) -> Mapping[str, Mapping[str, Any]]:
    return {
        "data": snapshot.data,
        "features": snapshot.features,
        "experiment": snapshot.experiment,
        "seeds": snapshot.seeds,
    }


def required_fields_for(stage: str, phase: int) -> tuple[str, ...]:
    """The `(stage, phase)` entry of `REQUIRED_FIELDS_MAP` (R-03).

    Raises
    ------
    ConfigError
        when no entry exists — an absent entry is a preflight gap surfaced loudly, never
        an implicit empty requirement set.
    """
    try:
        return REQUIRED_FIELDS_MAP[(stage, phase)]
    except KeyError:
        raise ConfigError(
            "REQUIRED_FIELDS_MAP",
            f"no required-fields entry for stage {stage!r} phase {phase}; the map is a "
            f"list and the completeness test is what makes it a rule (R-03) — add the "
            f"entry, never default to an empty set",
        ) from None


def assert_no_tbd(snapshot: ConfigSnapshot, *, required: Sequence[str]) -> None:
    """W-3 steps 1-4: the TE 18.3 zero-`TBD` precondition (R-02).

    Two rejections, both fatal: a required field ABSENT from the configuration, and a
    required field carrying the literal `TBD — freeze gate` sentinel. All offenders are
    collected and raised ONCE, so a human fixes every field in one pass rather than one
    run at a time.

    Raises
    ------
    PreflightError
        naming every offending field.
    """
    parsed = _configs_of(snapshot)
    offenders: list[str] = []
    for dotted in required:
        present, value = _lookup_path(parsed, dotted)
        if not present:
            offenders.append(f"{dotted} (absent)")
        elif isinstance(value, str) and value.strip() == TBD_SENTINEL:
            offenders.append(f"{dotted} (unresolved: {TBD_SENTINEL!r})")
    if offenders:
        raise PreflightError(
            "configs/",
            "TE 18.3 requires zero unresolved required fields; offending: "
            + "; ".join(offenders),
        )


def assert_declared_sources_exist(snapshot: ConfigSnapshot) -> None:
    """W-3 step 5, the 18.3 clause restored by DATA-13: every declared source resolves.

    A declared source is any mapping inside the four parsed configs carrying both a
    `path` and a `sha256`. `path` is resolved against the workspace root. A declared
    hash that does not resolve is a failure, never a warning.

    Raises
    ------
    PreflightError
        naming each unresolved declaration.
    """
    workspace = snapshot.resolved_roots["workspace"]
    problems: list[str] = []

    def _walk(node: Any, trail: str) -> None:
        if isinstance(node, Mapping):
            if "path" in node and "sha256" in node:
                declared_path = workspace / str(node["path"])
                if not declared_path.is_file():
                    problems.append(f"{trail}: declared source {node['path']!r} is absent")
                else:
                    actual = _sha256_bytes(declared_path.read_bytes())
                    if actual != str(node["sha256"]):
                        problems.append(
                            f"{trail}: declared sha256 {node['sha256']} does not resolve "
                            f"(actual {actual})"
                        )
            for key, value in node.items():
                _walk(value, f"{trail}.{key}")
        elif isinstance(node, list | tuple):
            for index, value in enumerate(node):
                _walk(value, f"{trail}[{index}]")

    for name, config in _configs_of(snapshot).items():
        _walk(config, name)

    if problems:
        raise PreflightError(
            "configs/",
            "every declared source and hash must resolve (TE 18.3, DATA-13); "
            + "; ".join(problems),
        )


# --- W-8 companion: the credential-name presence check (R-14) ---------------------------


def credential_names_for(stage: str, provider: str, phase: int | None = None) -> tuple[str, ...]:
    """The declared credential NAMES for a stage/provider pair — never values (R-14).

    Returns an empty tuple when nothing is declared: the presence check applies only to
    stages that actually require authenticated provider access (SD-02), so an absent
    entry means no credential precondition, not an error.
    """
    if phase is not None:
        found = CREDENTIAL_NAME_MAP.get((stage, provider, str(phase)))
        if found is not None:
            return found
    return CREDENTIAL_NAME_MAP.get((stage, provider), ())


def assert_credential_names_present(names: Sequence[str], env: Mapping[str, str]) -> None:
    """Fail early, naming every missing credential NAME (W-8; R-14; SD-02).

    Checks membership only: no value is read, returned or logged. Presence does NOT
    prove a value is non-empty, valid or authorized — the provider client validates the
    value without exposing it. A presence check mistaken for a validity check reports a
    readiness that does not exist.

    Raises
    ------
    PreflightError
        naming each missing environment-variable name.
    """
    missing = [name for name in names if name not in env]
    if missing:
        raise PreflightError(
            "environment",
            "required credential environment-variable name(s) missing: "
            + ", ".join(sorted(missing))
            + " — supply via the platform secret store or environment configuration "
            "excluded from version control (TE 10; NFR-SEC-01)",
        )


# --- W-4 / R-05: process determinism and seeding -----------------------------------------


def ensure_process_determinism(argv: Sequence[str]) -> None:
    """FU-1 = D: establish `PYTHONHASHSEED` before any framework import (R-05).

    The FIRST statement of every stage script's `main()`. When `PYTHONHASHSEED` is
    unset, sets it to "0", sets the re-exec sentinel, and re-execs the current
    interpreter with the same argv, so the guarantee holds for a directly invoked
    script. When already set, reads the sentinel ONCE, records it in module-level state
    (read later by `seed_everything` into `DeterminismRecord.reexec_performed`) and
    REMOVES it from the environment immediately — without the pop, a subprocess of a
    re-exec'd script would inherit the sentinel and record `True` for a process that
    never re-exec'd (R-05: the pop is load-bearing, not hygiene).

    Returns `None` by approved contract; nothing crosses the `exec` boundary in a
    return value. On Windows, `os.execv` spawns a replacement process and the parent
    exits — callers observe one logical run either way, and the re-exec is recorded so
    it is never mistaken for a double run.
    """
    global _REEXEC_PERFORMED
    if os.environ.get("PYTHONHASHSEED"):
        _REEXEC_PERFORMED = os.environ.pop(REEXEC_SENTINEL_ENV, None) is not None
        return
    os.environ["PYTHONHASHSEED"] = _PYTHONHASHSEED_VALUE
    os.environ[REEXEC_SENTINEL_ENV] = "1"
    # The R-05 re-exec IS the mechanism; sys.executable, no shell.
    os.execv(sys.executable, [sys.executable, *argv])  # noqa: S606


def reexec_performed() -> bool:
    """The module-level re-exec bit (R-05): set at the sentinel pop, read at W-4 step 4."""
    return _REEXEC_PERFORMED


def seed_everything(snapshot: ConfigSnapshot, *, stage: str) -> DeterminismRecord:
    """W-4: apply `seeds.yaml`, enable op determinism BEFORE any graph construction.

    Applies the frozen development seed (D-122, via `configs/seeds.yaml` — never inlined
    here, TC-03e) to `random`, NumPy and TensorFlow where each is importable, and
    enables TensorFlow op determinism. TensorFlow is imported INSIDE this function,
    never at module scope (R-05); with its pin excluded from requirements (Q3=A,
    `TBD — freeze gate`), an absent TensorFlow is recorded honestly in the probe scope
    and measurement status rather than treated as determinism.

    Does NOT touch the bootstrap seed — that carve-out is `src/evaluation/bootstrap.py`
    by ADR-05, a design decision rather than an oversight.

    Raises
    ------
    DeterminismError
        when TensorFlow has already been initialised — observed as `"tensorflow" in
        sys.modules`, evaluated BEFORE this function's own deferred import (R-05).
        Enabling op determinism afterwards is not equivalent.
    SeedError
        when `seeds.development` is missing, unresolved, or not an integer — a defaulted
        or inlined seed is exactly what SeedError names.
    """
    tf_preloaded = "tensorflow" in sys.modules
    if tf_preloaded:
        raise DeterminismError(
            "tensorflow",
            f"already initialised before seed_everything(stage={stage!r}); TensorFlow op "
            f"determinism must be enabled before any graph construction (R-05), so the "
            f"stage entry contract orders seed_everything before any framework import",
        )

    dev_seed = snapshot.seeds.get("development", _MISSING)
    if dev_seed is _MISSING or (isinstance(dev_seed, str) and dev_seed.strip() == TBD_SENTINEL):
        raise SeedError(
            "configs/seeds.yaml",
            "seeds.development is missing or unresolved; seeds are fixed in seeds.yaml "
            "(NFR-DET-01, D-122) and are never defaulted by an implementer",
        )
    if not isinstance(dev_seed, int) or isinstance(dev_seed, bool):
        raise SeedError(
            "configs/seeds.yaml",
            f"seeds.development must be an integer, got {dev_seed!r}",
        )

    seeds_applied: dict[str, int] = {}
    probe_scope: list[str] = []
    framework_versions: dict[str, str] = {
        "python": _platform.python_version(),
    }

    random.seed(dev_seed)
    seeds_applied["python"] = dev_seed
    probe_scope.append("python.random")

    try:
        import numpy
    except ImportError:
        framework_versions["numpy"] = "absent"
    else:
        numpy.random.seed(dev_seed)
        seeds_applied["numpy"] = dev_seed
        probe_scope.append("numpy.random")
        framework_versions["numpy"] = str(numpy.__version__)

    tf_op_determinism = False
    try:
        import tensorflow  # deferred import; module-scope import is prohibited (R-05)
    except ImportError:
        framework_versions["tensorflow"] = "absent (pin is TBD — freeze gate; Q3=A)"
    else:
        tensorflow.random.set_seed(dev_seed)
        seeds_applied["tensorflow"] = dev_seed
        tensorflow.config.experimental.enable_op_determinism()
        tf_op_determinism = True
        probe_scope.append("tensorflow.op_determinism")
        framework_versions["tensorflow"] = str(tensorflow.__version__)

    # --- the probe (Q3 = C): observed set, cross-checked against the declared set ------
    # At seed time no domain operation has executed, so the observed set is empty and the
    # status says so: an empty list is NEVER presented as proof of determinism (R-06).
    observed: list[str] = []
    declared_node = snapshot.seeds.get("determinism", {})
    declared: Sequence[str] = ()
    if isinstance(declared_node, Mapping):
        raw = declared_node.get("expected_nondeterministic_ops", ())
        if isinstance(raw, list | tuple):
            declared = [str(op) for op in raw]
    mismatches = [f"declared-not-observed: {op}" for op in declared if op not in observed]
    mismatches += [f"observed-not-declared: {op}" for op in observed if op not in declared]

    measurement_status = "not-yet-measured" if tf_op_determinism else "partial"

    return DeterminismRecord(
        seeds_applied=seeds_applied,
        pythonhashseed=os.environ.get("PYTHONHASHSEED", "unset"),
        reexec_performed=_REEXEC_PERFORMED,
        framework_versions=framework_versions,
        tf_op_determinism=tf_op_determinism,
        nondeterministic_ops=observed,
        probe_scope=probe_scope,
        measurement_status=measurement_status,
        declared_vs_observed_mismatches=mismatches,
    )


# --- W-5: the eight-item environment lock (REQ-ENG-10, TE 13.1) --------------------------


def _git_head(workspace: Path) -> str:
    try:
        # Fixed argv, no shell; git is resolved from PATH by design (local platform).
        result = subprocess.run(  # noqa: S603, S607
            ["git", "rev-parse", "HEAD"],  # noqa: S603, S607
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise IntegrityError(
            workspace,
            f"code_commit could not be captured from git HEAD ({exc}); a Kaggle session "
            f"carries no git working tree, so pass code_commit explicitly there — the "
            f"lock is never written with the field unpopulated (REQ-ENG-10)",
        ) from exc
    return result.stdout.strip()


def _pip_freeze() -> str:
    try:
        # Fixed argv, sys.executable, no shell (TE 13.1 per-run pip freeze).
        result = subprocess.run(  # noqa: S603
            [sys.executable, "-m", "pip", "freeze"],  # noqa: S603
            capture_output=True,
            text=True,
            timeout=300,
            check=True,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise IntegrityError(
            "pip freeze",
            f"the per-run pip freeze could not be captured ({exc}); TE 13.1 bullet 1 "
            f"names it as one of the two environment-pin artifacts and it is never "
            f"recorded as 'unavailable'",
        ) from exc
    return result.stdout


def capture_environment_lock(
    snapshot: ConfigSnapshot,
    determinism: DeterminismRecord,
    *,
    input_versions: Sequence[str] = (),
    requirements_path: Path | None = None,
    code_commit: str | None = None,
) -> RunRecord:
    """W-5: capture the eight-item per-run environment lock (REQ-ENG-10; TE 13.1).

    Every field populated, not "unavailable" — a capture that cannot complete raises
    rather than completing silently, because the thirteen pre-git runs are recorded as
    violating exactly this and the lock "was not captured at the time and cannot be
    reconstructed". `input_versions` lists the release manifests consumed; empty is a
    fact for a run that consumes none (Bolt 1), not a gap.

    Raises
    ------
    IntegrityError
        naming the file or capture that failed: a missing `requirements.txt`, a failed
        `pip freeze`, or an uncapturable `code_commit` (pass it explicitly on Kaggle).
    """
    workspace = Path(snapshot.resolved_roots["workspace"])
    req_path = Path(requirements_path) if requirements_path else workspace / "requirements.txt"
    if not req_path.is_file():
        raise IntegrityError(
            req_path,
            "the pinned requirements.txt is required for the environment lock's "
            "requirements hash (TE 13.1 bullet 1; TC-06 places the pin before any "
            "acquisition work)",
        )

    runtime_versions: dict[str, str] = {
        "python": _platform.python_version(),
        "os": _platform.platform(),
        "cpu": _platform.machine() or "unknown-cpu",
    }
    runtime_versions.update(
        {k: v for k, v in determinism.framework_versions.items() if k != "python"}
    )

    return RunRecord(
        requirements_hash=_sha256_bytes(req_path.read_bytes()),
        pip_freeze=_pip_freeze(),
        runtime_versions=runtime_versions,
        code_commit=code_commit if code_commit is not None else _git_head(workspace),
        config_hashes=dict(snapshot.hashes),
        input_versions=list(input_versions),
        platform=snapshot.platform,
        nondeterministic_ops=list(determinism.nondeterministic_ops),
    )


def environment_lock_hash(record: RunRecord) -> str:
    """The hash a registry row's `environment_lock_hash` column points at (R-18 col 6).

    SHA-256 over the canonical JSON of the eight fields, sorted keys, no insignificant
    whitespace — deterministic across platforms so the same environment yields the same
    hash.
    """
    payload = {
        "requirements_hash": record.requirements_hash,
        "pip_freeze": record.pip_freeze,
        "runtime_versions": dict(sorted(record.runtime_versions.items())),
        "code_commit": record.code_commit,
        "config_hashes": dict(sorted(record.config_hashes.items())),
        "input_versions": list(record.input_versions),
        "platform": record.platform,
        "nondeterministic_ops": list(record.nondeterministic_ops),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return _sha256_bytes(canonical.encode("utf-8"))


def assert_lock_complete(record: RunRecord) -> None:
    """REQ-ENG-10's criterion: all eight fields populated, or fail — never silence.

    Scalar and mapping fields must be non-empty. The two sequence fields
    (`input_versions`, `nondeterministic_ops`) may legitimately be empty — an empty
    list is a recorded fact, not an unpopulated field — which is why they are exempt
    from the emptiness check while remaining required attributes.

    Raises
    ------
    IntegrityError
        naming every unpopulated field.
    """
    empty_ok = {"input_versions", "nondeterministic_ops"}
    missing: list[str] = []
    for field in _dataclass_fields(record):
        value = getattr(record, field.name)
        if field.name in empty_ok:
            continue
        if value is None or (isinstance(value, str | Mapping) and not value):
            missing.append(field.name)
    if missing:
        raise IntegrityError(
            "environment lock",
            "REQ-ENG-10 requires all eight fields populated, not 'unavailable'; "
            "unpopulated: " + ", ".join(missing),
        )
