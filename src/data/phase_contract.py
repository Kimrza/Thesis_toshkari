"""Run-time phase boundary: NFR-PHASE-01's authoritative limb, and the G-P3C hash diff.

Purpose
-------
Three guards live here, all owned by `governance-guards` (R-23, R-24, SD-G-05):

1. **Import limb** — `assert_phase_boundary(phase, loaded_modules=...)`: under Phase 1,
   none of the four raw-processing adapters (`RAW_MODULES`) may be loaded. Called at
   step 4 of every stage script's entry contract, INSIDE the session, because a Kaggle
   session carries no git working tree and a local suite run proves nothing about the
   environment a governed run executes in (ADR-02).
2. **Produced-field limb** — `assert_no_raw_fields(...)`: a Phase 1 artifact may carry
   no field in D-17's excluded set (8 exclusions, wider than TE 7.0's five classes —
   the authority is `evidence/DECISIONS.md` D-17 together with TE 7.0, per R-23's
   2026-08-28 amendment). Called by each of the eight Phase 1 producing scripts before
   its first write; a completeness test in `tests/test_phase_contract.py` asserts that.
   **Neither limb substitutes for the other** (R-23), and the static AST scan in
   `tests/test_phase_boundary.py` is the SUBORDINATE early-warning limb (R-24): this
   module is the authoritative one.
3. **Transition hash diff** — `diff_protected_hashes` / `assert_protected_hashes_unchanged`:
   TE 7.0B and gate G-P3C's refusal semantics as a pure function. Phase 2 refuses to
   train if any protected hash differs. No manifest format is invented here: the
   functions take `name -> digest` mappings plus the authoritative protected-entry
   list, which R-19 places in `configs/experiment.yaml` (this module never hardcodes
   the governed 17-item enumeration — TC-03e and R-19 bar a literal copy in source,
   and R-20 records that where a TEST gets D-24's list from is OPEN).

Inputs
------
* `loaded_modules` — normally `sys.modules`; the boundary itself (`RAW_MODULES`) is
  derived from this module's own constants, never from caller input.
* artifact field names — an iterable of column names, or any object exposing
  `.columns` (the approved `component-methods.md` signature names a DataFrame; this
  module duck-types it so the guard carries no pandas dependency).
* two `protected_hashes` mappings plus the caller-supplied protected-entry list.

Re-run behaviour
----------------
Pure functions of their arguments: no file is read or written, no state is kept, and
re-running with the same inputs raises or passes identically. Importing this module
has no side effects.

Governance
----------
* `PhaseBoundaryError` is raised by both boundary limbs and is declared in
  `src/data/config.py` (foundation R-01's declaration site); `ManifestError` is
  declared HERE, riding R-01's "any future integrity-related exception" clause — it is
  raised only through this module, so no cross-package declaration is needed.
* R-22, binding: an EMPTY diff is the G-P3C pass condition but **must not be read as
  proof that no protected item changed** while BLK-06's per-item binding is pending.
  Nothing in this module states or implies otherwise.
* TA-27 stays `Pending`: this module supplies mechanism, never acceptance evidence.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Final

from src.data.config import IntegrityError, PhaseBoundaryError

__all__ = [
    "RAW_MODULES",
    "RAW_FIELD_TOKENS",
    "RAW_FIELD_COMPOUNDS",
    "PHASE1_PRODUCING_SCRIPTS",
    "ManifestError",
    "assert_phase_boundary",
    "assert_no_raw_fields",
    "diff_protected_hashes",
    "assert_protected_hashes_unchanged",
]


class ManifestError(IntegrityError):
    """A transition-manifest comparison is malformed or a protected hash differs.

    Rides foundation R-01's "any future integrity-related exception" clause: declared
    here rather than in `src/data/config.py` because only this module raises it, and
    every raise names the resource and the violated expectation (R-01's constructor
    contract, enforced by the base).
    """


#: TE 7.0's raw-processing adapters — all FOUR `src/gnss/` modules, not the two
#: FR-P1-03-2's earlier wording listed; `target` and `verification` were added per
#: finding IMPL-2 because 7.0 says "every raw-processing adapter". Module identities,
#: not scientific constants (TC-03e does not reach a module-name boundary).
RAW_MODULES: Final[frozenset[str]] = frozenset(
    {
        "src.gnss.rinex",
        "src.gnss.calibration",
        "src.gnss.target",
        "src.gnss.verification",
    }
)

#: The eight Phase 1 producing scripts (R-24), each of which must call
#: `assert_no_raw_fields` before its first write. The completeness test in
#: `tests/test_phase_contract.py` ranges over this tuple; a new producing script that
#: forgets the call fails there rather than being silently unchecked (DP-DATA-01).
PHASE1_PRODUCING_SCRIPTS: Final[tuple[str, ...]] = (
    "00_acquire_prepared_vtec",
    "01_inventory_and_registry",
    "02_standardize_prepared_target",
    "03_verify_processing",
    "04_build_external_products",
    "05_build_features_and_splits",
    "06_train_and_predict",
    "07_evaluate_and_report",
)

#: D-17's excluded set, matched as underscore-delimited TOKENS of a field name.
#: Token matching carries the static limb's "fragments, not exact names" discipline
#: (a column called `n_sat_valid` or `sat_count` must trip this as surely as
#: `valid_satellite_count`) while keeping the short forms `zen`, `elev`, `sat`, `arc`
#: and `ipp` from false-positive matching INSIDE innocent words (`frozen`, `skipped`),
#: which a raw substring check cannot avoid. Coverage of D-17's 8 exclusions:
#: 1 `valid_satellite_count` -> satellite | sat; 2 per-satellite / per-IPP -> sat, ipp;
#: 3 zenith angle or weight -> zenith, zen; 4 elevation -> elevation, elev;
#: 5 DCB -> dcb; 6 STEC -> stec; 7 mapping function output -> mapping;
#: 8 arc or cycle-slip statistics -> arc, plus the `cycle_slip` compound below.
#: Field-name identities, never scientific values (the REQUIRED_FIELDS_MAP precedent).
RAW_FIELD_TOKENS: Final[frozenset[str]] = frozenset(
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

#: Multi-token compounds matched as substrings of the lowered field name, because
#: their single tokens (`cycle`, `slip`, `function`, `count`, `n`) are innocent alone.
RAW_FIELD_COMPOUNDS: Final[tuple[str, ...]] = (
    "cycle_slip",
    "n_sat",
    "sat_count",
    "mapping_function",
)

#: Loaded-module name suffixes derived from RAW_MODULES (`gnss.rinex`, ...), so an
#: import that reaches an adapter under a different top-level package name still trips.
_RAW_MODULE_SUFFIXES: Final[tuple[str, ...]] = tuple(
    sorted(name.removeprefix("src.") for name in RAW_MODULES)
)


def _require_known_phase(phase: int) -> None:
    if phase not in (1, 2):
        raise PhaseBoundaryError(
            "phase",
            f"phase must be 1 or 2, got {phase!r}; an unknown phase cannot be cleared "
            f"against the Phase 1 hard prohibition (TE 7.0, NFR-PHASE-01)",
        )


def assert_phase_boundary(phase: int, *, loaded_modules: Mapping[str, object]) -> None:
    """R-23's import limb: under Phase 1, no raw-processing adapter may be loaded.

    The boundary is derived from `RAW_MODULES` — this module's own constant — never
    from caller input, so a caller cannot relocate it. `loaded_modules` is normally
    `sys.modules`. Called at step 4 of every stage script's entry contract so the
    prohibition holds inside the Kaggle session (ADR-02).

    Raises
    ------
    PhaseBoundaryError
        naming every offending loaded module, when `phase == 1` and any name in
        `RAW_MODULES` (or a dotted suffix of one, e.g. `gnss.rinex`) is present.
        Also raised for a phase outside {1, 2}.
    """
    _require_known_phase(phase)
    if phase != 1:
        return
    offenders = sorted(
        name
        for name in loaded_modules
        if name in RAW_MODULES
        or any(name == suffix or name.endswith("." + suffix) for suffix in _RAW_MODULE_SUFFIXES)
    )
    if offenders:
        raise PhaseBoundaryError(
            ", ".join(offenders),
            "raw-processing module(s) loaded under Phase 1; TE 7.0 makes "
            "src/gnss/rinex.py, calibration.py, target.py and verification.py "
            "inaccessible from the Phase 1 target-build command (NFR-PHASE-01, R-23 "
            "import limb) — neither this limb nor the produced-field limb substitutes "
            "for the other",
        )


def _field_names(artifact_fields: object) -> list[str]:
    """Accept an iterable of names or any object exposing `.columns` (DataFrame)."""
    columns = getattr(artifact_fields, "columns", artifact_fields)
    if isinstance(columns, str) or not isinstance(columns, Iterable):
        raise PhaseBoundaryError(
            "artifact_fields",
            f"expected an iterable of field names or an object with .columns, got "
            f"{type(artifact_fields).__name__}; the produced-field limb cannot clear "
            f"an artifact whose fields it cannot enumerate",
        )
    return [str(name) for name in columns]


def _tokens(field_name: str) -> frozenset[str]:
    return frozenset(token for token in re.split(r"[^a-z0-9]+", field_name.lower()) if token)


def assert_no_raw_fields(artifact_fields: object, *, phase: int) -> None:
    """R-23's produced-field limb: a Phase 1 artifact carries no D-17-excluded field.

    Enforces D-17's 8 enumerated exclusions (`evidence/DECISIONS.md` D-17, "Explicitly
    NOT in the Phase 1 row, and not substituted"), which is WIDER than TE 7.0's five
    classes — the widening is R-23's 2026-08-28 amendment (board Recommendation 37)
    and costs nothing scientifically because D-17 is frozen. Matching is by token and
    compound, never exact name, so a renamed column (`n_sat_valid`, `zen_wt`,
    `elev_deg`) cannot walk past an exact-name list.

    Called by each of the eight Phase 1 producing scripts BEFORE its first write
    (R-24); the completeness test asserts every one of them does.

    Raises
    ------
    PhaseBoundaryError
        naming every offending field, when `phase == 1` and any field matches.
        Also raised for a phase outside {1, 2} or a non-enumerable input.
    """
    names = _field_names(artifact_fields)
    _require_known_phase(phase)
    if phase != 1:
        return
    offenders = sorted(
        name
        for name in names
        if _tokens(name) & RAW_FIELD_TOKENS
        or any(compound in name.lower() for compound in RAW_FIELD_COMPOUNDS)
    )
    if offenders:
        raise PhaseBoundaryError(
            ", ".join(offenders),
            "Phase 1 artifact carries raw-processing field(s) from D-17's excluded set "
            "(valid_satellite_count, per-satellite or per-IPP quantities, zenith angle "
            "or weight, elevation, DCB, STEC, mapping function output, arc or "
            "cycle-slip statistics); a Phase 1 frame carrying such a field cannot have "
            "been measured — it can only have been invented, imported from Phase 2, or "
            "mislabelled (D-16, D-17, NFR-PHASE-01, R-23 produced-field limb)",
        )


def _validate_manifest_keys(
    label: str,
    manifest: Mapping[str, str],
    protected: frozenset[str],
) -> None:
    missing = sorted(protected - set(manifest))
    if missing:
        raise ManifestError(
            label,
            f"protected entr{'ies' if len(missing) != 1 else 'y'} missing from the "
            f"manifest: {', '.join(missing)}; the membership assertion fails BEFORE "
            f"any diff is computed, so a short set can never produce a reassuring "
            f"empty diff (R-21, R-22)",
        )
    unknown = sorted(set(manifest) - protected)
    if unknown:
        raise ManifestError(
            label,
            f"unknown entr{'ies' if len(unknown) != 1 else 'y'} not in the protected "
            f"set: {', '.join(unknown)}; an unlisted key is an integrity failure, "
            f"never silently ignored (R-20: addition fails the membership assertion)",
        )


def _validated_protected_entries(protected_entries: Iterable[str]) -> frozenset[str]:
    listed = [str(entry) for entry in protected_entries]
    if not listed:
        raise ManifestError(
            "protected_entries",
            "the protected-entry list is empty; a diff over zero entries would pass "
            "every comparison, so an empty list is refused (R-22: a hollow list "
            "cannot pass silently)",
        )
    if len(set(listed)) != len(listed):
        duplicates = sorted({entry for entry in listed if listed.count(entry) > 1})
        raise ManifestError(
            "protected_entries",
            f"duplicate protected entr{'ies' if len(duplicates) != 1 else 'y'}: "
            f"{', '.join(duplicates)}; D-24's cardinality is calculated from its "
            f"enumeration, so a duplicate is a malformed set, not a longer one (R-20)",
        )
    return frozenset(listed)


def diff_protected_hashes(
    frozen: Mapping[str, str],
    current: Mapping[str, str],
    *,
    protected_entries: Iterable[str],
) -> dict[str, tuple[str, str]]:
    """TA-27's hash-diff half: the named set of protected entries whose hashes differ.

    Pure function over two `name -> digest` mappings. `protected_entries` is the
    authoritative protected-entry list, supplied by the CALLER because R-19 places it
    in `configs/experiment.yaml`'s protected-set section and R-20 records as OPEN
    where a test may obtain D-24's list — this module hardcodes no governed
    enumeration (TC-03e) and invents no manifest format.

    Both manifests' key sets must equal the protected set exactly: a missing entry or
    an unknown entry is an integrity failure naming the manifest and the expectation,
    raised BEFORE any diff (R-21's freeze-mode membership assertion; R-22's negative
    control).

    Returns the differing entries mapped to `(frozen_digest, current_digest)`. An
    empty mapping is the G-P3C pass condition — and per R-22, while BLK-06's per-item
    binding is pending, an empty diff must NOT be read as proof that no protected
    item changed.
    """
    protected = _validated_protected_entries(protected_entries)
    _validate_manifest_keys("frozen manifest", frozen, protected)
    _validate_manifest_keys("current manifest", current, protected)
    return {
        name: (frozen[name], current[name])
        for name in sorted(protected)
        if frozen[name] != current[name]
    }


def assert_protected_hashes_unchanged(
    frozen: Mapping[str, str],
    current: Mapping[str, str],
    *,
    protected_entries: Iterable[str],
) -> None:
    """TE 7.0B / G-P3C refusal semantics: Phase 2 refuses to train on ANY diff.

    Raises
    ------
    ManifestError
        naming every protected entry whose hash differs, or any membership defect
        `diff_protected_hashes` refuses. Catching this and training anyway is the
        act the phase-transition freeze exists to prevent.
    """
    differing = diff_protected_hashes(frozen, current, protected_entries=protected_entries)
    if differing:
        raise ManifestError(
            ", ".join(sorted(differing)),
            "protected hash(es) differ between the frozen transition manifest and the "
            "current state; Phase 2 refuses to train if any protected hash differs "
            "(TE 7.0B, gate G-P3C, NFR-PHASE-01) — a signed, hashed freeze is this "
            "project's rollback-safety mechanism",
        )
