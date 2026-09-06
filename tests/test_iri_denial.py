"""NFR-IRI-01 / FR-P1-04-1: the IRI/GIM containment check, ordered and never vacuous.

PURPOSE. TE 12's import-boundary rule, WS-10 and TA-07's subject: nothing outside
`scripts/04_build_external_products.py` and `src/evaluation/` may reach
`src.external.iri` or `src.external.gim`, DIRECTLY OR TRANSITIVELY, and no `iri_*`
value, IRI-derived residual or IRI-computed value may reach a training or inference
surface. This module asserts the boundary WITHOUT importing the guarded modules -- the
whole check is an `ast` walk, the technique `tests/test_phase_boundary.py` established
(SD-E-01: "no test needs the grant, and the grant is withdrawn"). `tests/*` is NOT
allowlisted; the blanket `component-dependency.md`:34 row is routed to the gate as a
discrepancy, not followed.

THE ORDERED SWITCH (SD-E-01 -- a check that cannot fail is not a control). The outcome
is decided in this order, and a detected violation outranks everything:

1. the scan found a reachability path -> `failed`, regardless of either limb and
   regardless of any unresolved edge elsewhere in the graph (a found path is a fact;
   an absence of information never outranks a fact);
2. no path, but the walk hit an unresolved FIRST-PARTY edge -> `skipped`, edge
   recorded (a partly-built tree is full of unresolvable intermediates; treating them
   as clean would restore the vacuous pass by a third route);
3. no path, no unresolved edge, BOTH limbs populated -> `passed`;
4. either limb empty -> `skipped`, naming which limb (machine-readable, JSON -- the
   foundation preflight reads the structured reason rather than counting non-failures;
   that dependency is FR-WS-7's, routed to the gate, not assumed).

THE CANDIDATE-IMPORTER SET is defined ONCE, BY COMPLEMENT, never by directory list
(SD-E-01: three prior enumerations each failed by omitting one more directory): the
domain is everything in the repository that can execute Python -- `.py` files AND the
code cells of `.ipynb` notebooks, ast-parsed -- and the candidate set is the domain
minus TE 12's two allowlisted paths. The AI-DLC workflow shell (`.claude/`, `aidlc/`)
is outside the domain: team.md records it as workflow infrastructure, never a project
deliverable, and SD-E-00's own printed 18-file derivation of this set contained no
file from either tree. `__init__.py` files are WALKED (a package `__init__` can carry
an import like any other module) and SUBTRACTED from the risk-surface CARDINALITY only
(an otherwise-empty package is not a populated risk surface): the walk is a strict
superset of the count.

Clause 1 is decided by NAME-MATCHING, not file resolution, so a violation is
detectable with no target file present (a partly-built tree can still NAME
`src.external.gim` in an import). A third-party or stdlib import is NOT an edge and
NOT an unresolved edge -- the graph is first-party only (all six-plus tests import
pytest; scoring that as unresolved would land every run on clause 2). A grep-class
visibility check records every `importlib`/`__import__` call site outside the
allowlist in the payload as REVIEW ITEMS -- visible, never silently clean, and never an
automatic pass or fail (R-56's partial control; the run-time-computed dynamic import
remains the named, accepted residual).

THE CONTENT LIMB (SD-E-03, WS-10): a column reaching a training/inference surface is
admitted only when its provenance is PRESENT AND NOT IRI. An absent provenance FAILS
-- the flipped default: a laundered value must forge a stamp, not merely delete one.
The barrier is EVIDENTIARY, not cryptographic, and NFR-IRI-01 is not described as
fully enforced: a value renamed, recomputed from scratch and carrying a fabricated
provenance survives (the named residual). The feature-matrix half of this contract is
`features-and-splits`'; the predicate here is this unit's statement of it.

EVERY OUTCOME CARRIES ONE PAYLOAD SCHEMA: the candidate set actually walked (count and
module paths), any unresolved edges, the dynamic-import review items, and -- on a skip
-- the identifier of the empty limb.

RE-RUN BEHAVIOUR. Pure function of the tree; no imports of guarded modules, no writes,
no network. Negative controls run over `tmp_path` synthetic trees.

Run: pytest tests/test_iri_denial.py -rs
"""

from __future__ import annotations

import ast
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The containment targets, as module paths (TE 12; project.md Forbidden).
TARGET_MODULES: tuple[str, ...] = ("src.external.iri", "src.external.gim")

#: TE 12's two allowlisted importer paths -- exactly two, as the requirement states
#: them. `tests/*` is NOT here (SD-E-01: the previous grant is withdrawn).
ALLOWLISTED_RELATIVE: tuple[str, ...] = (
    "scripts/04_build_external_products.py",
    "src/evaluation/",
)

#: Outside the Python-executing domain: VCS internals, bytecode, virtualenvs, and the
#: AI-DLC workflow shell (team.md: workflow infrastructure, never a project
#: deliverable; SD-E-00's printed derivation of the candidate set contained no file
#: from either tree).
_EXCLUDED_DIR_NAMES: frozenset[str] = frozenset(
    {".git", "__pycache__", ".venv", "node_modules", ".claude", "aidlc"}
)

#: First-party top-level segments: an import whose top segment is one of these, and
#: which resolves to no repository file, is an UNRESOLVED EDGE (clause 2). Anything
#: else unresolvable is third-party/stdlib and is not an edge at all.
_FIRST_PARTY_TOPS: frozenset[str] = frozenset({"src", "scripts", "tests", "notebooks"})


# --- domain, parsing, and the import graph ----------------------------------------------


def _in_domain(path: Path) -> bool:
    return not any(part in _EXCLUDED_DIR_NAMES for part in path.parts)


def _python_domain(root: Path) -> list[Path]:
    """Every file under `root` that can execute Python: `.py` AND `.ipynb`."""
    files = [p for p in root.rglob("*.py") if _in_domain(p.relative_to(root))]
    files += [p for p in root.rglob("*.ipynb") if _in_domain(p.relative_to(root))]
    return sorted(files)


def _is_allowlisted(path: Path, root: Path) -> bool:
    relative = path.relative_to(root).as_posix()
    for allowed in ALLOWLISTED_RELATIVE:
        if allowed.endswith("/"):
            if relative.startswith(allowed):
                return True
        elif relative == allowed:
            return True
    return False


def _parse_units(path: Path) -> list[tuple[str, ast.Module]]:
    """The ast module(s) of a file: one for a `.py`, one per code cell for `.ipynb`.

    An unparseable file or cell raises SyntaxError to the caller, which records it as
    a FAILURE: a file that will not parse cannot be cleared (R-27's rule, preserved
    from `test_phase_boundary._imported_modules`).
    """
    if path.suffix == ".ipynb":
        notebook = json.loads(path.read_text(encoding="utf-8"))
        units: list[tuple[str, ast.Module]] = []
        for index, cell in enumerate(notebook.get("cells", [])):
            if cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", []))
            units.append((f"{path.name}[cell {index}]", ast.parse(source)))
        return units
    return [(path.name, ast.parse(path.read_text(encoding="utf-8"), filename=str(path)))]


def _imports_of(tree: ast.Module, *, package_parts: tuple[str, ...]) -> tuple[set[str], set[str]]:
    """The absolute import names of one ast unit, relative imports resolved.

    Returns (module_names, member_names). A MODULE name (`import x.y`; the module part
    of `from x.y import z`) must resolve EXACTLY: `import src.data.missing` is an
    unresolved edge even though `src.data` exists, because the leaf is what the
    statement demands. A MEMBER name (`x.y.z` from `from x.y import z`) may be a
    module OR an attribute: it participates in target NAME-MATCHING (so
    `from src.external import gim` is caught) and, where it resolves to a file, in the
    walk -- but an unresolvable member is not an unresolved edge, because `z` may
    legitimately be a function.
    """
    modules: set[str] = set()
    members: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = package_parts[: len(package_parts) - (node.level - 1)]
                module = ".".join((*base, node.module)) if node.module else ".".join(base)
            else:
                module = node.module or ""
            if module:
                modules.add(module)
                members.update(f"{module}.{alias.name}" for alias in node.names)
    return modules, members


def _dynamic_import_sites(units: Sequence[tuple[str, ast.Module]]) -> list[str]:
    """Every `importlib.import_module` / `__import__` call site -- REVIEW ITEMS.

    Recorded in the payload so a dynamic-import site is visible rather than silent
    (R-56's grep-class partial control); never an automatic pass or fail. The
    run-time-computed target remains the accepted, named residual.
    """
    sites: list[str] = []
    for unit_name, tree in units:
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            is_dunder = isinstance(node.func, ast.Name) and node.func.id == "__import__"
            is_importlib = (
                isinstance(node.func, ast.Attribute) and node.func.attr == "import_module"
            )
            if is_dunder or is_importlib:
                sites.append(f"{unit_name}:{node.lineno}")
    return sites


def _module_index(files: Sequence[Path], *, root: Path) -> dict[str, Path]:
    """Module name -> file, dotted-from-root plus bare stem for same-dir imports."""
    index: dict[str, Path] = {}
    for path in files:
        if path.suffix != ".py":
            continue
        parts = list(path.relative_to(root).with_suffix("").parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
        if parts:
            index[".".join(parts)] = path
            index.setdefault(parts[-1], path)
    return index


def _resolve(name: str, index: Mapping[str, Path]) -> Path | None:
    parts = name.split(".")
    for cut in range(len(parts), 0, -1):
        candidate = ".".join(parts[:cut])
        if candidate in index:
            return index[candidate]
    return None


def _matches_target(name: str, targets: Sequence[str]) -> bool:
    return any(name == target or name.startswith(target + ".") for target in targets)


def _package_parts(path: Path, root: Path) -> tuple[str, ...]:
    parts = list(path.relative_to(root).with_suffix("").parts)
    return tuple(parts[:-1])


def run_containment_scan(
    root: Path,
    *,
    targets: Sequence[str] = TARGET_MODULES,
) -> dict[str, Any]:
    """The ordered-switch transitive containment scan. Returns the ONE payload schema
    every outcome carries (SD-E-01): outcome, walked candidate set (count and module
    paths), risk-surface count, unresolved edges, violations (full reachability
    CHAINS, not endpoints), dynamic-import review items, target presence, and -- on a
    skip -- the empty limb's identifier.
    """
    domain = _python_domain(root)
    target_files = {root / Path(target.replace(".", "/") + ".py") for target in targets}
    # The target files are the OBJECTS of containment, not candidate importers: the
    # risk surface is what could import them, so they are subtracted alongside the
    # allowlist (they are still name-matchable targets at every hop of the walk).
    candidates = [
        path for path in domain if not _is_allowlisted(path, root) and path not in target_files
    ]
    index = _module_index(domain, root=root)
    target_limb_populated = any(path.is_file() for path in target_files)
    counted = [
        path for path in candidates if not (path.suffix == ".py" and path.name == "__init__.py")
    ]

    violations: list[dict[str, Any]] = []
    unresolved_edges: list[str] = []
    unparseable: list[str] = []
    dynamic_sites: list[str] = []

    for start in candidates:
        # BFS from this candidate; the chain names every hop (SD-E-02: a transitive
        # violation whose message names only `gim` says nothing about which hop to cut).
        frontier: list[tuple[Path, list[str]]] = [(start, [start.relative_to(root).as_posix()])]
        visited: set[Path] = set()
        while frontier:
            current, chain = frontier.pop()
            if current in visited:
                continue  # cycle or diamond: terminate, never fail
            visited.add(current)
            try:
                units = _parse_units(current)
            except SyntaxError as exc:
                unparseable.append(f"{current.relative_to(root).as_posix()}: {exc}")
                continue
            if current == start:
                dynamic_sites.extend(_dynamic_import_sites(units))
            package = _package_parts(current, root)
            for unit_name, tree in units:
                modules, members = _imports_of(tree, package_parts=package)
                for name in sorted(modules | members):
                    if _matches_target(name, targets):
                        violations.append(
                            {"module": chain[0], "chain": [*chain, name], "via": unit_name}
                        )
                for name in sorted(modules):
                    if _matches_target(name, targets):
                        continue  # already recorded above
                    if name in index:
                        resolved = index[name]
                        if resolved not in visited:
                            frontier.append(
                                (resolved, [*chain, resolved.relative_to(root).as_posix()])
                            )
                    elif name.split(".")[0] in _FIRST_PARTY_TOPS:
                        # A module name that resolves to NO file is an unresolved
                        # first-party edge (clause 2) -- resolving to a parent package
                        # is not resolution: the leaf is what the statement demands.
                        unresolved_edges.append(f"{chain[-1]} -> {name}")
                    # else: third-party/stdlib -- not an edge, not unresolved.
                for name in sorted(members):
                    if _matches_target(name, targets):
                        continue
                    resolved = _resolve(name, index)
                    if resolved is not None and resolved not in visited:
                        frontier.append(
                            (resolved, [*chain, resolved.relative_to(root).as_posix()])
                        )

    payload: dict[str, Any] = {
        "check": "iri_gim_containment",
        "targets": list(targets),
        "target_limb_populated": target_limb_populated,
        "walked_count": len(candidates),
        "walked_modules": [path.relative_to(root).as_posix() for path in candidates],
        "risk_surface_count": len(counted),
        "unresolved_edges": sorted(set(unresolved_edges)),
        "unparseable": unparseable,
        "violations": violations,
        "dynamic_import_review_items": sorted(set(dynamic_sites)),
        "empty_limb": None,
    }

    # The ordered switch (SD-E-01). An unparseable file is a failure (R-27's rule),
    # reported alongside clause 1: a file that will not parse cannot be cleared.
    if violations or unparseable:
        payload["outcome"] = "failed"
    elif payload["unresolved_edges"]:
        payload["outcome"] = "skipped"
        payload["skip_reason"] = "unresolved first-party edge(s) recorded"
    elif target_limb_populated and payload["risk_surface_count"] > 0:
        payload["outcome"] = "passed"
    else:
        payload["outcome"] = "skipped"
        payload["empty_limb"] = "target" if not target_limb_populated else "risk_surface"
        payload["skip_reason"] = (
            "no containment target exists"
            if not target_limb_populated
            else "the candidate-importer set is empty"
        )
    return payload


# --- the content limb (SD-E-03; WS-10) ---------------------------------------------------


def iri_column_violations(columns: Sequence[Mapping[str, Any]]) -> list[str]:
    """The content-assertion predicate: a column is admitted only when its provenance
    is PRESENT AND DOES NOT SAY IRI. An `iri_*` NAME fails outright (WS-10's injected
    field); an ABSENT provenance fails (the flipped default -- SD-E-03: admitting a
    column because its provenance is silent is inferring a grade from silence); a
    provenance that says IRI fails. Present-and-not-IRI is admitted.

    The barrier is evidentiary, not cryptographic; the renamed-and-recomputed value
    with a fabricated provenance is the named residual no artifact may describe as
    closed. The feature-matrix half of this contract is `features-and-splits`'.
    """
    problems: list[str] = []
    for column in columns:
        name = str(column.get("name", ""))
        provenance = column.get("provenance")
        if name.lower().startswith("iri_"):
            problems.append(f"{name}: iri_* field on a training/inference surface (WS-10)")
            continue
        if provenance is None or not str(provenance).strip():
            problems.append(
                f"{name}: ABSENT provenance fails (SD-E-03 flipped default; a stripped "
                f"stamp is caught, not admitted)"
            )
            continue
        if "iri" in str(provenance).lower():
            problems.append(f"{name}: provenance says IRI ({provenance!r})")
    return problems


# --- the real tree -----------------------------------------------------------------------


def test_containment_scan_over_real_tree_is_never_vacuous() -> None:
    """The ordered switch over the real repository, asserted end to end.

    With this unit landed, `iri.py` and `gim.py` exist and the candidate set is
    populated, so a clean tree yields a REAL `passed` -- reached over named modules,
    with the payload proving what was walked (the symmetry mitigation: a reader of a
    `passed` can see it was earned over N modules, without the check judging which
    modules are 'real'). A violation fails with its full chain; a skip carries its
    machine-readable reason.
    """
    payload = run_containment_scan(REPO_ROOT)
    # One payload schema on every outcome.
    for field in (
        "outcome",
        "walked_count",
        "walked_modules",
        "risk_surface_count",
        "unresolved_edges",
        "violations",
        "dynamic_import_review_items",
        "empty_limb",
    ):
        assert field in payload, f"payload field {field} missing; the schema is unified"
    assert payload["walked_count"] == len(payload["walked_modules"])
    assert (
        payload["risk_surface_count"] <= payload["walked_count"]
    ), "the walk is a strict superset of the count; only the count subtracts __init__.py"
    if payload["outcome"] == "failed":
        pytest.fail(
            "IRI/GIM containment violated (TE 12; NFR-IRI-01; project.md Forbidden): "
            + json.dumps(payload["violations"] + payload["unparseable"], indent=2)
        )
    if payload["outcome"] == "skipped":
        # Machine-readable structured reason: the WHOLE payload, as JSON (the
        # foundation FR-WS-7 preflight reads this rather than parsing English; a
        # skipped critical check is UNMET there by definition).
        pytest.skip(json.dumps(payload))
    assert payload["outcome"] == "passed"
    assert payload["target_limb_populated"], "passed requires the target limb populated"
    assert payload["risk_surface_count"] > 0, "passed requires a populated risk surface"


def test_allowlist_is_exactly_te12s_two_paths() -> None:
    """`tests/*` is NOT allowlisted; the blanket component-dependency row is routed to
    the gate as a discrepancy, not followed here (SD-E-01)."""
    assert ALLOWLISTED_RELATIVE == (
        "scripts/04_build_external_products.py",
        "src/evaluation/",
    )
    assert not _is_allowlisted(REPO_ROOT / "tests" / "test_iri_denial.py", REPO_ROOT)
    assert _is_allowlisted(REPO_ROOT / "scripts" / "04_build_external_products.py", REPO_ROOT)
    assert _is_allowlisted(REPO_ROOT / "src" / "evaluation" / "__init__.py", REPO_ROOT)


def test_clause4_target_limb_pinned_over_the_real_candidate_set() -> None:
    """The plan's pinned state, expressed with the target limb forced empty OVER THE
    REAL CANDIDATE SET: when neither target exists, the scan reports `skipped` NAMING
    the target limb -- never `passed` -- while still walking the real candidates.

    (The plan pinned 'today's clause-4 state'; Steps 3-4 of the same plan created the
    real targets, so the pin is expressed by scanning for target names that do not
    exist. The walked set is the real one, which is what the pin protects.)
    """
    payload = run_containment_scan(
        REPO_ROOT, targets=("src.external.iri_absent", "src.external.gim_absent")
    )
    assert payload["outcome"] == "skipped"
    assert payload["empty_limb"] == "target"
    assert payload["walked_count"] > 0, "the skip is reported OVER a real walked set"
    assert not payload["target_limb_populated"]
    # The structured reason round-trips as machine-readable JSON.
    assert json.loads(json.dumps(payload))["empty_limb"] == "target"


# --- negative controls: the module-graph limb (tmp trees) --------------------------------


def _write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _tree_with_targets(root: Path) -> None:
    _write(root, "src/__init__.py", "")
    _write(root, "src/external/__init__.py", "")
    _write(root, "src/external/iri.py", "")
    _write(root, "src/external/gim.py", "")


def test_injected_direct_import_fails(tmp_path: Path) -> None:
    """Negative control: a direct `iri` import from src/features -> `failed`."""
    _tree_with_targets(tmp_path)
    _write(tmp_path, "src/features/__init__.py", "")
    _write(tmp_path, "src/features/build.py", "import src.external.iri\n")
    payload = run_containment_scan(tmp_path)
    assert payload["outcome"] == "failed"
    chains = [violation["chain"] for violation in payload["violations"]]
    assert any("src/features/build.py" in chain[0] for chain in chains), chains


def test_injected_transitive_import_fails_with_full_chain(tmp_path: Path) -> None:
    """Negative control: models -> shim (src/data) -> gim is caught ON TRANSITIVITY,
    and the violation names the CHAIN, not just the endpoint (SD-E-02)."""
    _tree_with_targets(tmp_path)
    _write(tmp_path, "src/data/__init__.py", "")
    _write(tmp_path, "src/data/shim.py", "from src.external import gim\n")
    _write(tmp_path, "src/models/__init__.py", "")
    _write(tmp_path, "src/models/lstm.py", "import src.data.shim\n")
    payload = run_containment_scan(tmp_path)
    assert payload["outcome"] == "failed"
    matching = [
        violation
        for violation in payload["violations"]
        if violation["module"] == "src/models/lstm.py"
    ]
    assert matching, payload["violations"]
    chain = matching[0]["chain"]
    assert chain[0] == "src/models/lstm.py"
    assert "src/data/shim.py" in chain, "the chain names the intermediate hop"
    assert chain[-1].startswith("src.external.gim"), "the chain ends at the target name"


def test_injected_notebook_import_fails(tmp_path: Path) -> None:
    """Negative control (R-56: 'Import iri from a notebook -> fails'): a `.ipynb` code
    cell is ast-parsed and its import is caught -- the domain spans notebooks."""
    _tree_with_targets(tmp_path)
    notebook = {
        "cells": [
            {"cell_type": "markdown", "source": ["# analysis\n"]},
            {"cell_type": "code", "source": ["import src.external.iri\n"]},
        ],
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    _write(tmp_path, "notebooks/probe.ipynb", json.dumps(notebook))
    payload = run_containment_scan(tmp_path)
    assert payload["outcome"] == "failed"
    assert any("probe.ipynb" in violation["via"] for violation in payload["violations"])


def test_name_match_fires_with_target_absent(tmp_path: Path) -> None:
    """Clause 1 is decided by NAME-MATCHING: a file that does not exist can still be
    NAMED in an import, so a violation is detectable with no target file present, and
    clause 1 fires AHEAD of the clause-4 skip."""
    _write(tmp_path, "src/__init__.py", "")
    _write(tmp_path, "src/features/__init__.py", "")
    _write(tmp_path, "src/features/early.py", "import src.external.gim\n")
    payload = run_containment_scan(tmp_path)
    assert payload["outcome"] == "failed", (
        "a named target must fail even while the target limb is empty; skipping here "
        "is the vacuous pass returning by another route"
    )


def test_found_path_outranks_unresolved_edge(tmp_path: Path) -> None:
    """Clause 1 outranks clause 2: a found path fails even when an unresolved edge
    exists elsewhere in the graph -- an absence of information never outranks a fact."""
    _tree_with_targets(tmp_path)
    _write(tmp_path, "src/features/__init__.py", "")
    _write(tmp_path, "src/features/bad.py", "import src.external.iri\n")
    _write(tmp_path, "src/data/__init__.py", "")
    _write(tmp_path, "src/data/broken.py", "import src.data.missing_module\n")
    payload = run_containment_scan(tmp_path)
    assert payload["outcome"] == "failed"
    assert payload["unresolved_edges"], "the unresolved edge is still recorded"


def test_unresolved_intermediate_skips_and_records_the_edge(tmp_path: Path) -> None:
    """Clause 2: an unresolvable FIRST-PARTY intermediate breaks the chain and the
    outcome is `skipped` with the edge recorded -- never `passed` (the transitive-walk
    counterpart of R-27's unparseable-file rule)."""
    _tree_with_targets(tmp_path)
    _write(tmp_path, "src/data/__init__.py", "")
    _write(tmp_path, "src/data/loader.py", "import src.data.not_written_yet\n")
    payload = run_containment_scan(tmp_path)
    assert payload["outcome"] == "skipped"
    assert any("not_written_yet" in edge for edge in payload["unresolved_edges"])


def test_third_party_imports_are_not_edges(tmp_path: Path) -> None:
    """A third-party or stdlib import is NOT an edge and NOT an unresolved edge: a
    tree whose candidates import only pytest/json reaches clause 3, not clause 2."""
    _tree_with_targets(tmp_path)
    _write(tmp_path, "tests_dir/probe.py", "import pytest\nimport json\n")
    payload = run_containment_scan(tmp_path)
    assert payload["outcome"] == "passed"
    assert payload["unresolved_edges"] == []


def test_empty_risk_surface_skips_naming_the_limb(tmp_path: Path) -> None:
    """Clause 4, risk-surface side: targets exist but every candidate is an
    `__init__.py` -- walked, yet subtracted from the cardinality -- so the scan skips
    NAMING the risk-surface limb rather than passing over nothing."""
    _tree_with_targets(tmp_path)  # candidates: src/__init__.py, src/external/__init__.py
    payload = run_containment_scan(tmp_path)
    assert payload["outcome"] == "skipped"
    assert payload["empty_limb"] == "risk_surface"
    assert payload["walked_count"] > 0, "__init__.py files are WALKED"
    assert payload["risk_surface_count"] == 0, "and subtracted from the COUNT"


def test_init_py_is_walked_even_though_uncounted(tmp_path: Path) -> None:
    """The walk is a strict superset of the count: a violating import written in the
    ONE file the count subtracts (`__init__.py`) still fails -- on today's tree shape,
    that file is the only place an src/features -> iri import could be written."""
    _tree_with_targets(tmp_path)
    _write(tmp_path, "src/features/__init__.py", "import src.external.iri\n")
    payload = run_containment_scan(tmp_path)
    assert payload["outcome"] == "failed"


def test_spaceweather_import_from_features_passes(tmp_path: Path) -> None:
    """R-56's stated-permitted control: `spaceweather` is deliberately OUTSIDE the
    restriction (drivers ARE model inputs), and a test asserts the scan admits it."""
    _tree_with_targets(tmp_path)
    _write(tmp_path, "src/external/spaceweather.py", "")
    _write(tmp_path, "src/features/__init__.py", "")
    _write(tmp_path, "src/features/build.py", "import src.external.spaceweather\n")
    payload = run_containment_scan(tmp_path)
    assert payload["outcome"] == "passed", payload


def test_dynamic_import_sites_are_review_items_not_outcomes(tmp_path: Path) -> None:
    """The grep-class visibility check: an `importlib`/`__import__` call site outside
    the allowlist is SURFACED in the payload for review -- and it alone changes no
    outcome (a review item, not an automatic pass or fail; R-56)."""
    _tree_with_targets(tmp_path)
    _write(
        tmp_path,
        "src/data/dyn.py",
        "import importlib\n\ndef load(name):\n    return importlib.import_module(name)\n",
    )
    payload = run_containment_scan(tmp_path)
    assert payload["dynamic_import_review_items"], "the site must be visible"
    assert payload["outcome"] == "passed", (
        "a dynamic-import site alone is a review item; the run-time-computed target "
        "is the accepted, NAMED residual (R-56), not a failure the scan can prove"
    )


def test_unparseable_candidate_is_a_failure_not_a_skip(tmp_path: Path) -> None:
    """R-27's rule carried into the walk: a file that will not parse cannot be
    cleared, and it FAILS the check rather than importing nothing."""
    _tree_with_targets(tmp_path)
    _write(tmp_path, "src/data/__init__.py", "")
    _write(tmp_path, "src/data/broken.py", "def broken(:\n")
    payload = run_containment_scan(tmp_path)
    assert payload["outcome"] == "failed"
    assert payload["unparseable"], payload


# --- negative controls: the content limb (SD-E-03; WS-10) --------------------------------


def test_injected_iri_field_is_caught() -> None:
    """WS-10: a deliberately injected `iri_*` field on a training/inference surface is
    caught by the content assertion -- the denial test passes by proving the denial."""
    columns = [
        {"name": "vtec_lag1", "provenance": "madrigal gridded VTEC (D-9 input)"},
        {"name": "iri_vtec_estimate", "provenance": "IRI-2016 run B-01"},
    ]
    problems = iri_column_violations(columns)
    assert any("iri_vtec_estimate" in problem for problem in problems), problems


def test_stripped_provenance_stamp_is_caught() -> None:
    """SD-E-03's flipped default: an ABSENT provenance FAILS -- a laundered value must
    forge a stamp rather than merely delete one (evidentiary, not cryptographic)."""
    columns = [{"name": "smoothed_column", "provenance": ""}]
    problems = iri_column_violations(columns)
    assert problems and "ABSENT provenance" in problems[0], problems


def test_present_non_iri_provenance_is_admitted() -> None:
    """The admitting half, asserted so the flip is a default change and not a blanket
    refusal: provenance PRESENT AND NOT IRI admits the column."""
    columns = [
        {"name": "kp_lag3h", "provenance": "GFZ Kp index, availability-lagged (D-10.3)"},
        {"name": "f107_prev_day", "provenance": "NRCan observed F10.7 (D-21/D-22/D-23)"},
    ]
    assert iri_column_violations(columns) == []


def test_iri_named_column_fails_even_with_innocent_provenance() -> None:
    """The name limb and the provenance limb are independent: an `iri_*` NAME fails
    whatever its stamp says (NFR-IRI-01's own spelling of the rule)."""
    columns = [{"name": "iri_residual", "provenance": "definitely not what it says"}]
    problems = iri_column_violations(columns)
    assert problems and "iri_residual" in problems[0]
