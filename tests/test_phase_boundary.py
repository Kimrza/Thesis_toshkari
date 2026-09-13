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

SUBORDINATE STATUS (R-24, the Q7 rider — recorded where the code lives, on purpose).
This static AST scan is the early-warning limb ONLY. It fires before anything executes,
which is earlier than run time and worth keeping — and it does not discharge FR-P1-03-2's
run-time requirement. The AUTHORITATIVE limb is `src/data/phase_contract.py`
(`assert_phase_boundary`, `assert_no_raw_fields`), called at step 4 of every stage
script's entry contract inside the session, because a static scan of a local checkout
constrains nothing about a Kaggle session. A future maintainer must not read this
module's presence as sufficient; `tests/test_phase_contract.py` carries a documentation
test that fails the day this paragraph is removed.

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

# The D-17 Phase 1 target-row contract: EXACTLY these sixteen row fields -- not fifteen,
# not seventeen. This is an exact contract, not a permission list: a conforming row carries
# all sixteen and nothing else (beyond DECLARED_CAVEAT_FIELD below). The producer states the
# same bound at `src/data/prepared.py:788`, and D-17's frozen table in `evidence/DECISIONS.md`
# enumerates these sixteen and no more.
#
# `processor_qc_flags` is NOT a row field and is deliberately absent. It is a key inside the
# data-quality block (R-71 / NFR-DQ-01, W-3), built as a nested mapping of `aggregation_flags`
# and `not_applicable_classes` -- D-17 discusses it in its own paragraph, outside the row
# table, for exactly that reason. It was carried here in error from commit `b844a4d`
# (2026-08-21) and removed 2026-09-13; `test_d17_target_fields_match_the_producer_contract`
# below now makes that divergence un-repeatable.
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
    "aggregation_config_id",
    "target_valid",
    "phase_id",
    "source_id",
    "target_definition_id",
})

# The ONE column a written target artifact may carry beyond D-17's sixteen: the lineage
# caveat the producer attaches to every write (SD-T-02). Mirrors `LINEAGE_CAVEAT_FIELD` in
# `src/data/prepared.py`, whose row guard at `:791` subtracts exactly this one name before
# computing `extra`. Pinned against the producer's literal by the drift guard below, so the
# two spellings cannot part company.
DECLARED_CAVEAT_FIELD = "lineage_caveat"

# The producer-side home of the contract this module's copy must equal. Read STATICALLY
# (see `_module_level_literal`), never imported -- see the drift guard's docstring.
PREPARED_MODULE = SRC_DIR / "data" / "prepared.py"


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


def _module_level_literal(path: Path, name: str) -> object:
    """Read a module-level constant's literal value from a file's AST, without importing it.

    This module reaches source by PARSING it (`_imported_modules` above), never by importing
    it: it carries no `sys.path` insert and no `from src...` import, there is no `conftest.py`
    to supply one, and its contract is to stay collectible and to SKIP with a named reason
    when `src/` is absent. A module-level import of the producer would turn that explicit
    skip into a collection error and would drag in `src.data.acquisition`, `src.data.config`
    and `src.data.release` transitively. So the drift guard uses the mechanism already here.

    Fail-closed, matching `_imported_modules`: a file that will not parse, or a constant that
    is missing or is not a literal, cannot be cleared.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        pytest.fail(f"{path} does not parse, so its {name} cannot be read: {exc}")
    for node in tree.body:
        targets = (
            [node.target] if isinstance(node, ast.AnnAssign) else getattr(node, "targets", [])
        )
        if not any(isinstance(t, ast.Name) and t.id == name for t in targets):
            continue
        if node.value is None:
            pytest.fail(f"{path} declares {name} without a value")
        try:
            return ast.literal_eval(node.value)
        except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError) as exc:
            pytest.fail(f"{path}'s {name} is not a literal, so it cannot be compared: {exc}")
    pytest.fail(
        f"{path} no longer defines a module-level {name}; the D-17 contract's producer-side "
        f"home moved or was renamed, and this test cannot confirm the two copies agree"
    )


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


def test_d17_target_fields_match_the_producer_contract() -> None:
    """This module's D-17 copy equals the producer's, field for field.

    The drift guard. `D17_TARGET_FIELDS` here and `D17_FIELDS` in `src/data/prepared.py` are
    two copies of one frozen contract, and they DID silently diverge: this copy carried a
    seventeenth name, `processor_qc_flags`, from commit `b844a4d` (2026-08-21) until
    2026-09-13 -- a transcription slip against a data-quality-block key, invisible because
    nothing compared the two. Divergence is now a failure rather than a discovery made on the
    first real artifact.

    The producer is read statically, not imported (`_module_level_literal`). The caveat
    literal is pinned in the same test because it is the same failure mode: a second copied
    spelling, whose drift would silently widen or narrow the `extra` computation below.
    """
    if not PREPARED_MODULE.is_file():
        pytest.skip(
            f"{PREPARED_MODULE.relative_to(REPO_ROOT)} does not exist, so there is no "
            f"producer-side D17_FIELDS to compare against (REQ-ENG-1)"
        )
    producer_fields = _module_level_literal(PREPARED_MODULE, "D17_FIELDS")
    assert isinstance(producer_fields, (tuple, list, frozenset, set)), (
        f"{PREPARED_MODULE.name}'s D17_FIELDS is a {type(producer_fields).__name__}, not an "
        f"enumeration of field names"
    )
    producer_set = set(producer_fields)
    assert len(producer_set) == len(tuple(producer_fields)), (
        f"{PREPARED_MODULE.name}'s D17_FIELDS repeats a field name: "
        f"{sorted(producer_fields)}"
    )
    assert set(D17_TARGET_FIELDS) == producer_set, (
        f"the D-17 contract has drifted between its two copies. Only here: "
        f"{sorted(set(D17_TARGET_FIELDS) - producer_set)}; only in "
        f"{PREPARED_MODULE.name}: {sorted(producer_set - set(D17_TARGET_FIELDS))}. D-17 "
        f"freezes exactly sixteen row fields and neither copy may be edited alone."
    )
    assert len(D17_TARGET_FIELDS) == 16, (
        f"D17_TARGET_FIELDS holds {len(D17_TARGET_FIELDS)} fields; D-17's frozen table "
        f"enumerates exactly sixteen -- not fifteen, not seventeen"
    )

    producer_caveat = _module_level_literal(PREPARED_MODULE, "LINEAGE_CAVEAT_FIELD")
    assert DECLARED_CAVEAT_FIELD == producer_caveat, (
        f"the declared lineage-caveat column name has drifted: {DECLARED_CAVEAT_FIELD!r} "
        f"here against {producer_caveat!r} in {PREPARED_MODULE.name}"
    )
    assert DECLARED_CAVEAT_FIELD not in D17_TARGET_FIELDS, (
        "the lineage-caveat column is the one field permitted BEYOND D-17's sixteen, so it "
        "must not also be counted as one of them"
    )


def test_target_artifact_conforms_to_d17_when_it_exists() -> None:
    """A produced hourly target carries D-17's sixteen fields, plus only the caveat column.

    Exact in both directions. `missing` is the full sixteen: every one must be present, and
    that limb is not relaxed. `extra` permits exactly one name beyond them --
    `DECLARED_CAVEAT_FIELD` -- mirroring the producer's own row guard at
    `src/data/prepared.py:791`, which subtracts `{LINEAGE_CAVEAT_FIELD}` before computing its
    own `extra`. The producer's write path is `(*D17_FIELDS, LINEAGE_CAVEAT_FIELD)`
    (`prepared.py:1324`), so without that allowance this test would reject every artifact the
    pipeline legitimately writes. Any OTHER additional field still fails: an extra column is
    where a Phase 2 quantity would appear (R-66, R-67).
    """
    candidates = sorted(EVIDENCE_DIR.rglob("hourly_target*.csv")) if EVIDENCE_DIR.is_dir() else []
    candidates += sorted((REPO_ROOT / "artifacts").rglob("hourly_target*.csv")) if (REPO_ROOT / "artifacts").is_dir() else []
    if not candidates:
        pytest.skip(
            "no hourly target artifact exists yet; produced by "
            "scripts/02_standardize_prepared_target.py against the D-17 contract"
        )
    for artifact in candidates:
        header = set(_csv_header(artifact))
        extra = sorted(header - D17_TARGET_FIELDS - {DECLARED_CAVEAT_FIELD})
        missing = sorted(D17_TARGET_FIELDS - header)
        assert not extra, (
            f"{artifact.name} carries fields beyond D-17's sixteen and the declared "
            f"lineage-caveat column: {extra}"
        )
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
