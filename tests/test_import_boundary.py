"""SEC-I-01 limb 2 / SD-I-01: the December audit's import boundary, two limbs.

PURPOSE. The audit code path imports no module under `src/models/` or `src/evaluation/`,
directly or transitively. Two limbs, neither a superset of the other:

* **Limb A — a package-wide forbidden edge.** Every file in `src/data/*` plus
  `scripts/01_inventory_and_registry.py` is checked DIRECTLY (reusing
  `test_phase_boundary._imported_modules`): if each member of the set is checked, a
  chain that stays inside the set is caught at its first hop. Limb A checks every
  member regardless of reachability.
* **Limb B — an entry-point reachability closure.** The module graph over `src/` and
  `scripts/` is closed transitively from the audit entry point
  (`scripts/01_inventory_and_registry.py`); the closure must contain no models or
  evaluation module. This is the limb that catches a chain LEAVING the constrained set
  (audit -> src/external -> src/evaluation), which Limb A structurally cannot see.

IMPLEMENTATION CONSTRAINTS (SD-I-01, fixed at design so 3.5 does not re-decide them):
an unparseable file FAILS (preserved from `_imported_modules`'s `pytest.fail`, never a
skip reintroduced by the graph walk); a CYCLE terminates the walk and is not itself a
violation; a dynamic or computed import the walker cannot resolve is REPORTED as a
failure, never assumed clean. `test_phase_boundary.py`'s `PHASE1_PERMITTED_PACKAGES`
behaviour is untouched — the two boundaries answer different questions over the same
primitive, and NFR-PHASE-01 remains `governance-guards`' with no coverage claimed here.

NEGATIVE CONTROLS (team.md § Testing Posture — every hard rule gets a test that proves
the violation is CAUGHT): one injected direct import for Limb A, one injected two-hop
chain through an unconstrained package for Limb B — two separately named results.

NOTE. `component-dependency.md` is NOT edited by this unit: the three matrix edits this
boundary owes ride `governance/CHANGE_RECORD_2026-09-05_import_boundary_matrix.md`,
applied only on owner approval at the gate.

RE-RUN BEHAVIOUR. Pure function of the tree; no network, no writes, no fixtures beyond
`tmp_path` synthetics.

Run: pytest tests/test_import_boundary.py -rs
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from test_phase_boundary import _imported_modules

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
SCRIPTS_DIR = REPO_ROOT / "scripts"
AUDIT_ENTRY_POINT = SCRIPTS_DIR / "01_inventory_and_registry.py"

#: The forbidden target packages (SEC-I-01 limb 2). Names as project code imports them.
FORBIDDEN_PACKAGES = ("src.models", "src.evaluation")

#: Limb A's constrained set: every file under src/data/ plus the audit's stage script.
def _limb_a_files() -> list[Path]:
    files = sorted((SRC_DIR / "data").glob("*.py")) if (SRC_DIR / "data").is_dir() else []
    if AUDIT_ENTRY_POINT.is_file():
        files.append(AUDIT_ENTRY_POINT)
    return files


def _is_forbidden(module_name: str) -> bool:
    return any(
        module_name == package or module_name.startswith(package + ".")
        for package in FORBIDDEN_PACKAGES
    )


def _limb_a_offenders(files: list[Path]) -> dict[str, list[str]]:
    """Direct-import check over every member of the constrained set (Limb A)."""
    offenders: dict[str, list[str]] = {}
    for path in files:
        hits = sorted(name for name in _imported_modules(path) if _is_forbidden(name))
        if hits:
            offenders[path.name] = hits
    return offenders


def _dynamic_import_sites(path: Path) -> list[str]:
    """Dynamic/computed imports the static walker cannot resolve — REPORTED, never
    assumed clean (SD-I-01's third constraint)."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:  # preservation, not repair: an unparseable file fails
        pytest.fail(f"{path} does not parse, so its imports cannot be checked: {exc}")
    sites: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        is_dunder = isinstance(node.func, ast.Name) and node.func.id == "__import__"
        is_importlib = (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "import_module"
        )
        if not (is_dunder or is_importlib):
            continue
        if not node.args or not isinstance(node.args[0], ast.Constant):
            sites.append(f"{path.name}:{node.lineno} (computed import target)")
    return sites


def _module_index(roots: list[Path], *, repo_root: Path) -> dict[str, Path]:
    """Project module name -> file, for closure resolution."""
    index: dict[str, Path] = {}
    for root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.py")):
            relative = path.relative_to(repo_root)
            parts = list(relative.with_suffix("").parts)
            if parts[-1] == "__init__":
                parts = parts[:-1]
            index[".".join(parts)] = path
    return index


def _resolve_to_file(module_name: str, index: dict[str, Path]) -> Path | None:
    """Longest-prefix resolution: `src.data.config.IntegrityError` -> src/data/config.py."""
    parts = module_name.split(".")
    for cut in range(len(parts), 0, -1):
        candidate = ".".join(parts[:cut])
        if candidate in index:
            return index[candidate]
    return None


def _closure_from(
    entry: Path, index: dict[str, Path]
) -> tuple[set[str], list[str]]:
    """Transitive closure of project-module names reachable from `entry` (Limb B).

    Cycles terminate the walk (a revisited file is skipped); they never fail it.
    Returns (module names in the closure, unresolved dynamic-import sites).
    """
    visited_files: set[Path] = set()
    closure: set[str] = set()
    unresolved: list[str] = []
    frontier: list[Path] = [entry]
    while frontier:
        current = frontier.pop()
        if current in visited_files:  # cycle or diamond: terminate, never fail
            continue
        visited_files.add(current)
        unresolved.extend(_dynamic_import_sites(current))
        for name in _imported_modules(current):
            target = _resolve_to_file(name, index)
            if target is None:
                continue  # stdlib / third-party: outside the project graph
            closure.add(name)
            frontier.append(target)
    return closure, unresolved


# --- Limb A -----------------------------------------------------------------------------


def test_limb_a_src_data_and_audit_script_import_no_models_or_evaluation() -> None:
    """Limb A over the real tree: no direct forbidden edge from the constrained set."""
    files = _limb_a_files()
    assert files, "constrained set is empty; src/data and the audit script must exist"
    offenders = _limb_a_offenders(files)
    assert not offenders, (
        f"forbidden direct import(s) from the December-audit constrained set: "
        f"{offenders}. src/data/* and scripts/01_inventory_and_registry.py may not "
        f"import src/models/* or src/evaluation/* (SEC-I-01 limb 2; SD-I-01 Limb A). "
        f"The matrix edits this rule owes ride the 2026-09-05 change record and are "
        f"applied only on owner approval."
    )


def test_limb_a_catches_injected_direct_import(tmp_path: Path) -> None:
    """Negative control (separately named result 1): an injected DIRECT import fails."""
    injected = tmp_path / "injected_direct.py"
    injected.write_text(
        "import src.models.lstm  # deliberate violation for the negative control\n",
        encoding="utf-8",
    )
    offenders = _limb_a_offenders([injected])
    assert offenders == {"injected_direct.py": ["src.models.lstm"]}, (
        "Limb A failed to catch a deliberately injected direct import; the boundary "
        "check is not demonstrating anything (WS-10's injection pattern)"
    )


# --- Limb B -----------------------------------------------------------------------------


def test_limb_b_audit_entry_point_closure_excludes_models_and_evaluation() -> None:
    """Limb B over the real tree: the audit entry point's transitive closure is clean,
    and every dynamic import in it is resolvable (reported, never assumed clean)."""
    assert AUDIT_ENTRY_POINT.is_file(), "the audit entry point must exist"
    index = _module_index([SRC_DIR], repo_root=REPO_ROOT)
    closure, unresolved = _closure_from(AUDIT_ENTRY_POINT, index)
    assert not unresolved, (
        f"dynamic/computed import(s) the walker cannot resolve: {unresolved}; an "
        f"unresolved edge is the one case a static walker can be silently wrong about, "
        f"and it is reported rather than assumed clean (SD-I-01)"
    )
    forbidden = sorted(name for name in closure if _is_forbidden(name))
    assert not forbidden, (
        f"the audit entry point transitively reaches forbidden module(s): {forbidden} "
        f"(SEC-I-01 limb 2; SD-I-01 Limb B)"
    )


def test_limb_b_catches_injected_two_hop_chain(tmp_path: Path) -> None:
    """Negative control (separately named result 2): a two-hop chain through an
    UNCONSTRAINED package is caught by the closure — the case Limb A cannot see."""
    entry = tmp_path / "entry.py"
    hop = tmp_path / "external_helper.py"
    entry.write_text("import external_helper\n", encoding="utf-8")
    hop.write_text(
        "import src.evaluation.metrics  # second hop, through an unconstrained module\n",
        encoding="utf-8",
    )
    fake_eval = tmp_path / "fake_evaluation_metrics.py"
    fake_eval.write_text("", encoding="utf-8")
    index = {
        "external_helper": hop,
        "src.evaluation.metrics": fake_eval,
    }
    closure, unresolved = _closure_from(entry, index)
    assert not unresolved
    forbidden = sorted(name for name in closure if _is_forbidden(name))
    assert forbidden == ["src.evaluation.metrics"], (
        "Limb B failed to catch a deliberately injected two-hop chain through an "
        "unconstrained package; the closure is the limb that must see it (SD-I-01)"
    )


def test_limb_b_cycle_terminates_and_does_not_fail(tmp_path: Path) -> None:
    """A cycle terminates the walk; it is not itself a violation (SD-I-01)."""
    first = tmp_path / "cycle_a.py"
    second = tmp_path / "cycle_b.py"
    first.write_text("import cycle_b\n", encoding="utf-8")
    second.write_text("import cycle_a\n", encoding="utf-8")
    index = {"cycle_a": first, "cycle_b": second}
    closure, unresolved = _closure_from(first, index)
    assert not unresolved
    assert closure == {"cycle_a", "cycle_b"}


def test_dynamic_computed_import_is_reported_never_assumed_clean(tmp_path: Path) -> None:
    """An import target the walker cannot resolve is a reported failure, not a pass."""
    dynamic = tmp_path / "dynamic_importer.py"
    dynamic.write_text(
        "import importlib\n"
        "def load(name):\n"
        "    return importlib.import_module(name)  # computed target\n",
        encoding="utf-8",
    )
    sites = _dynamic_import_sites(dynamic)
    assert sites and "dynamic_importer.py" in sites[0], (
        "a computed import target must be reported, never assumed clean (SD-I-01)"
    )
