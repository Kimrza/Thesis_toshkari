"""Phase 1 / Phase 2 boundary enforcement.

PURPOSE. `Technical_Environment_and_Research_Implementation` §7.0 states the Phase 1 hard
prohibition in two limbs, and requires this module to fail on either:

    "`src/gnss/rinex.py`, `src/gnss/calibration.py`, and every raw-processing adapter are
     inaccessible from the Phase 1 target-build command. `test_phase_boundary.py` shall
     fail if the Phase 1 dependency graph imports them OR if Phase 1 produces DCB, STEC,
     mapping, satellite, or arc fields."

NFR-PHASE-01 makes the same rule binding, and requirement FR-P1-03-2 decomposes both
limbs. §2.2 and §7.0B add the protected-hash limb enforced by the transition-manifest
hash-diff test, which is a separate module.

INPUTS. Read-only:
  * `src/` -- the Phase 1 module graph, when it exists;
  * `scripts/` -- the phase-aware stage scripts, when they exist;
  * `evidence/` and `evidence/locked_test_restricted/` -- produced Phase 1 artifacts,
    checked for forbidden field names against the D-17 target-row contract.

RE-RUN BEHAVIOUR. Pure function of the tree; no network, no writes, no fixtures. Tests
whose subject does not exist yet SKIP with an explicit reason rather than passing vacuously
-- a vacuous pass on a boundary test is what NFR-PHASE-01 cannot afford. Every skip names
the artifact whose absence caused it, so `pytest -rs` lists exactly what is not yet
enforceable.

WHAT IS ENFORCEABLE TODAY. The produced-field limb: the acquired Phase 1 evidence carries
five provider columns (`ut1_unix`, `gdlat`, `glon`, `tec`, `dtec`) and no satellite, DCB,
STEC, mapping or arc quantity, and D-17 freezes that contract. The import limb activates
when `src/` is built (REQ-ENG-1).

Origin: GOV-2026-08-20-RA-01 finding IMPL-2 (both limbs narrowed); decisions D-16, D-17.

Run: pytest tests/test_phase_boundary.py -rs
"""

from __future__ import annotations

import ast
import csv
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
SCRIPTS_DIR = REPO_ROOT / "scripts"
EVIDENCE_DIR = REPO_ROOT / "evidence"
RESTRICTED_DIR = EVIDENCE_DIR / "locked_test_restricted"

# Raw-processing adapters. The first two are named in §7.0; the remaining two are the other
# `src/gnss/` modules in the §12 tree, assigned to Phase 2 stages 2 and 3, and are included
# because §7.0 says "every raw-processing adapter" rather than only the two it names.
RAW_PROCESSING_MODULES = (
    "src/gnss/rinex.py",
    "src/gnss/calibration.py",
    "src/gnss/target.py",
    "src/gnss/verification.py",
)
RAW_MODULE_NAMES = tuple(m[len("src/"): -len(".py")].replace("/", ".") for m in RAW_PROCESSING_MODULES)

# Packages a Phase 1 code path may reach. `src/gnss/` is absent by design.
PHASE1_PERMITTED_PACKAGES = ("data", "external", "features", "models", "evaluation")

# Field-name fragments that mark a Phase 2 quantity. Matched case-insensitively against
# artifact column names. Deliberately fragments, not exact names: a column called
# `n_sat_valid` or `sat_count` must trip this as surely as `valid_satellite_count`.
FORBIDDEN_FIELD_FRAGMENTS = (
    "satellite",
    "n_sat",
    "sat_count",
    "prn",
    "dcb",
    "stec",
    "slant",
    "mapping_function",
    "arc_",
    "cycle_slip",
    "elevation",
    "zenith",
    "ipp",
)

# The D-17 Phase 1 target-row contract. Column names a Phase 1 target artifact may carry.
D17_TARGET_FIELDS = frozenset({
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
    "processor_qc_flags",
    "aggregation_config_id",
    "target_valid",
    "phase_id",
    "source_id",
    "target_definition_id",
})


def _python_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.py")) if root.is_dir() else []


def _imported_modules(path: Path) -> set[str]:
    """Every module name imported by a file, from its AST rather than by text match."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:  # a file that will not parse cannot be cleared
        pytest.fail(f"{path} does not parse, so its imports cannot be checked: {exc}")
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
            names.update(f"{node.module}.{alias.name}" for alias in node.names)
    return names


def _csv_header(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.reader(handle):
            return [c.strip() for c in row]
    return []


def _phase1_artifacts() -> list[Path]:
    """Produced Phase 1 coverage/target artifacts, both evidence roots, any depth."""
    if not EVIDENCE_DIR.is_dir():
        return []
    return sorted(EVIDENCE_DIR.rglob("madrigal_coverage_*.csv"))


# --- limb 1: the import boundary ------------------------------------------------------


def test_raw_processing_modules_are_absent_or_unreferenced_from_phase1_code() -> None:
    """No Phase 1 module or stage script imports a raw-processing adapter.

    Covers all four `src/gnss/` modules, not only the two §7.0 names, because the clause
    says "every raw-processing adapter". A violation via `target.py` or `verification.py`
    was previously outside every stated prohibition (finding IMPL-2).
    """
    candidates = [p for p in _python_files(SRC_DIR) if "gnss" not in p.parts]
    candidates += _python_files(SCRIPTS_DIR)
    if not candidates:
        pytest.skip(
            "no Phase 1 source or stage scripts exist yet (src/ and the nine phase-aware "
            "scripts are REQ-ENG-1); the import limb activates when they are built"
        )
    offenders: dict[str, list[str]] = {}
    for path in candidates:
        hits = sorted(
            name
            for name in _imported_modules(path)
            for raw in RAW_MODULE_NAMES
            if name == raw or name.endswith(raw) or raw.endswith(name)
        )
        if hits:
            offenders[str(path.relative_to(REPO_ROOT))] = hits
    assert not offenders, (
        f"Phase 1 code imports raw-processing adapters: {offenders}. TE §7.0 makes "
        f"{', '.join(RAW_PROCESSING_MODULES)} inaccessible from the Phase 1 target-build "
        f"command."
    )


def test_gnss_package_is_not_imported_by_phase1_packages() -> None:
    """`src/gnss/` is unreachable from the Phase 1 packages, transitively or directly."""
    if not SRC_DIR.is_dir():
        pytest.skip("src/ does not exist yet (REQ-ENG-1)")
    offenders: dict[str, list[str]] = {}
    for package in PHASE1_PERMITTED_PACKAGES:
        for path in _python_files(SRC_DIR / package):
            hits = sorted(n for n in _imported_modules(path) if "gnss" in n.split("."))
            if hits:
                offenders[str(path.relative_to(REPO_ROOT))] = hits
    assert not offenders, f"Phase 1 packages reach src/gnss/: {offenders}"


# --- limb 2: the produced-field prohibition -------------------------------------------


@pytest.mark.parametrize("artifact", _phase1_artifacts(), ids=lambda p: str(p.name))
def test_phase1_artifact_carries_no_phase2_field(artifact: Path) -> None:
    """No produced Phase 1 artifact carries a DCB, STEC, mapping, satellite or arc field.

    This is the limb §7.0 requires and that FR-P1-03-2 previously left without any
    criterion. It is enforceable today against the acquired evidence.
    """
    header = _csv_header(artifact)
    if not header:
        pytest.skip(f"{artifact.name} has no header row")
    offenders = sorted(
        col for col in header
        for frag in FORBIDDEN_FIELD_FRAGMENTS
        if frag in col.lower()
    )
    assert not offenders, (
        f"{artifact.relative_to(REPO_ROOT)} carries Phase 2 field(s) {offenders}. "
        f"TE §7.0 requires this test to fail if Phase 1 produces DCB, STEC, mapping, "
        f"satellite or arc fields. Phase 1 holds five provider columns and cannot "
        f"legitimately derive any of these (decision D-17)."
    )


def test_d17_contract_excludes_every_phase2_quantity() -> None:
    """The frozen D-17 field set contains no Phase 2 quantity.

    Guards the contract itself, not only the artifacts: if a future edit adds a satellite
    or zenith field to D17_TARGET_FIELDS, the boundary is breached in the specification
    before any data is produced.
    """
    offenders = sorted(
        field for field in D17_TARGET_FIELDS
        for frag in FORBIDDEN_FIELD_FRAGMENTS
        if frag in field.lower()
    )
    assert not offenders, (
        f"the D-17 Phase 1 target contract names Phase 2 quantities {offenders}; "
        f"D-17 excludes valid_satellite_count, per-IPP quantities, zenith weights, "
        f"elevation, DCB, STEC, mapping output and arc statistics, with nothing substituted"
    )


def test_target_artifact_conforms_to_d17_when_it_exists() -> None:
    """A produced hourly target conforms to D-17 exactly: no extra field, none missing."""
    candidates = sorted(EVIDENCE_DIR.rglob("hourly_target*.csv")) if EVIDENCE_DIR.is_dir() else []
    candidates += sorted((REPO_ROOT / "artifacts").rglob("hourly_target*.csv")) if (REPO_ROOT / "artifacts").is_dir() else []
    if not candidates:
        pytest.skip(
            "no hourly target artifact exists yet; produced by "
            "scripts/02_standardize_prepared_target.py against the D-17 contract"
        )
    for artifact in candidates:
        header = set(_csv_header(artifact))
        extra = sorted(header - D17_TARGET_FIELDS)
        missing = sorted(D17_TARGET_FIELDS - header)
        assert not extra, f"{artifact.name} carries fields outside the D-17 contract: {extra}"
        assert not missing, f"{artifact.name} is missing D-17 contract fields: {missing}"


# --- the restricted root is in scope, not an exemption --------------------------------


def test_restricted_root_artifacts_are_checked_too() -> None:
    """The produced-field checks reach inside the restricted custody root.

    Relocating December under `evidence/locked_test_restricted/` (D-15) must not remove it
    from boundary checking. A custody boundary is not a checking exemption, and this
    asserts the collector still sees it.
    """
    if not RESTRICTED_DIR.is_dir():
        pytest.skip("restricted root does not exist")
    seen = [p for p in _phase1_artifacts() if RESTRICTED_DIR in p.parents or p.is_relative_to(RESTRICTED_DIR)]
    assert seen, (
        "no artifact inside the restricted root was collected for boundary checking; "
        "the collector must reach relocated December evidence (D-15), because custody "
        "containment and phase-boundary checking are separate obligations"
    )
