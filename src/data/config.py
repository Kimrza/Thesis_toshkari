"""Project exception hierarchy and the base every integrity violation derives from.

Purpose
-------
`foundation` R-01 fixes one rule: **every project-defined exception derives from
`IntegrityError`**, whose base lives here in `src/data/config.py`. R-01 deliberately
stopped asserting a *count* after its enumeration went stale twice; the named classes
below are a **named subset**, not a completeness claim, and any future integrity-related
exception derives from the same base whether or not it is listed here.

Inputs
------
None. This module imports nothing from the project and is importable from every package,
which is why it is the declaration site: `component-dependency.md` marks
`src/features` -> `src/models` and `src/data` -> `src/models` both as absent, so an
exception declared under `src/models/` could not be raised by `src/data/splits.py` or by
anything under `src/features/`.

Re-run behaviour
----------------
Pure declarations. Importing this module has no side effects and is idempotent.

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
* Constructor contract (R-01): every raise names the file or resource **and** the violated
  expectation. `IntegrityError` enforces the shape rather than trusting each call site.
"""

from __future__ import annotations

__all__ = [
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
    """An experiment-registry write would be lost, silently overwritten, or reordered."""


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
