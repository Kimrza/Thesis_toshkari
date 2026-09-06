"""The TE 10.1 reuse register: registered before use, all fifteen fields, or refused.

Purpose
-------
TA-28's evidence module (R-29, R-30, SD-G-06). Proves the register's two-sided
enforcement: a provenance-marked adapter module with no complete register row is
refused (use before registration), a row missing any of the fifteen 10.1 fields is
refused at construction and at load, the register is append-safe, and the
reimplementation-as-default posture is pinned in the implementation's own docstring.
Nothing here discharges TA-28 or gate G-P2 — this is mechanism, run as smoke evidence
only until the governed environment exists.

Inputs
------
`tmp_path` for every register and fixture module; the repository's own `src/` and
`scripts/` trees, read only for the real-tree completeness assertion. No third-party
source is copied anywhere in this suite.

Re-run behaviour
----------------
Deterministic and self-contained; every register lives under `tmp_path` and the real
tree is never written to.

Governance
----------
* TE 10.1; NFR-LIC-01; gate G-P2 (unaffected by G-09's signature).
* `project.md` § Forbidden: reimplementation with a citation is the standing default
  while the AGPLv3 distribution question is open.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, replace
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import src.data.reuse_registry as reuse_registry_module  # noqa: E402
from src.data.config import IntegrityError  # noqa: E402
from src.data.reuse_registry import (  # noqa: E402
    PROVENANCE_MARKER,
    REUSE_REGISTER_FIELDS,
    ReuseError,
    ReuseRecord,
    assert_reuse_registered_before_use,
    find_marked_modules,
    load_register,
    register_reuse,
)


def _complete_record(reuse_id: str = "RU-001") -> ReuseRecord:
    return ReuseRecord(
        reuse_id=reuse_id,
        repository_url="https://example.org/upstream/repo",
        commit_or_tag="a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
        upstream_reference="upstream/module.py::the_function (lines 10-42)",
        retrieval_date="2026-09-05",
        licence_spdx_id="MIT",
        copied_or_adapted="adapted",
        destination_file="src/example/adapter.py",
        scientific_purpose="synthetic fixture for the register mechanism test",
        modifications="renamed symbols; removed I/O; typed signatures",
        tests="tests/test_reuse_registry.py",
        original_citation="Author et al. (2020), Journal, doi:10.0000/example",
        notice_location="NOTICE.md",
        reviewer="Kimia Rezaei",
        approval_date="2026-09-05",
    )


def _marked_module(directory: Path, reuse_id: str) -> Path:
    module = directory / "adapter.py"
    module.write_text(
        f'"""Synthetic adapter fixture."""\n# {PROVENANCE_MARKER} {reuse_id}\n',
        encoding="utf-8",
    )
    return module


# --- the fifteen-field row is enforced at construction and at load ----------------------


def test_the_field_set_is_exactly_the_fifteen_of_te_10_1() -> None:
    assert len(REUSE_REGISTER_FIELDS) == 15
    assert len(set(REUSE_REGISTER_FIELDS)) == 15


@pytest.mark.parametrize("field_name", REUSE_REGISTER_FIELDS)
def test_a_row_blank_on_any_field_is_refused(field_name: str) -> None:
    """Negative control: each of the fifteen fields, blanked, is refused."""
    with pytest.raises(ReuseError) as excinfo:
        replace(_complete_record(), **{field_name: "  "})
    assert field_name in str(excinfo.value)


def test_copied_or_adapted_is_a_closed_vocabulary() -> None:
    with pytest.raises(ReuseError):
        replace(_complete_record(), copied_or_adapted="borrowed")


def test_a_short_row_written_by_hand_is_refused_at_load(tmp_path: Path) -> None:
    """A row that bypassed `ReuseRecord` and lacks a field still cannot pass."""
    register = tmp_path / "reuse_register.jsonl"
    row = asdict(_complete_record())
    del row["licence_spdx_id"]
    register.write_text(json.dumps(row) + "\n", encoding="utf-8")
    with pytest.raises(ReuseError) as excinfo:
        load_register(register)
    assert "licence_spdx_id" in str(excinfo.value)


def test_an_unparseable_register_line_is_a_failure(tmp_path: Path) -> None:
    register = tmp_path / "reuse_register.jsonl"
    register.write_text("{not json\n", encoding="utf-8")
    with pytest.raises(ReuseError):
        load_register(register)


# --- registered-before-use ---------------------------------------------------------------


def test_a_marked_module_with_no_register_row_is_use_before_registration(
    tmp_path: Path,
) -> None:
    """The central negative control: the adapter exists, its registration does not."""
    _marked_module(tmp_path, "RU-unregistered")
    register = tmp_path / "reuse_register.jsonl"
    with pytest.raises(ReuseError) as excinfo:
        assert_reuse_registered_before_use([tmp_path], register)
    message = str(excinfo.value)
    assert "RU-unregistered" in message
    assert "BEFORE" in message


def test_a_registered_marked_module_passes_and_the_population_is_returned(
    tmp_path: Path,
) -> None:
    module = _marked_module(tmp_path, "RU-001")
    register = tmp_path / "reuse_register.jsonl"
    register_reuse(register, _complete_record("RU-001"))
    verified = assert_reuse_registered_before_use([tmp_path], register)
    assert verified == {module.as_posix(): "RU-001"}


def test_the_marker_scan_finds_marked_and_ignores_unmarked(tmp_path: Path) -> None:
    _marked_module(tmp_path, "RU-002")
    unmarked = tmp_path / "original_work.py"
    unmarked.write_text('"""Original work, no reuse."""\n', encoding="utf-8")
    marked = find_marked_modules([tmp_path])
    assert list(marked.values()) == ["RU-002"]


def test_the_real_tree_carries_no_unregistered_reuse() -> None:
    """The completeness assertion over the actual `src/` and `scripts/` trees.

    Population recorded explicitly: TODAY the marked-module set is expected empty —
    no reuse has been approved and reimplementation is the standing default — and the
    assertion derives that emptiness from a real scan rather than assuming it. The
    moment an adapter carrying the provenance marker lands without a complete register
    row, this test fails (never a silent vacuous pass).
    """
    register = REPO_ROOT / "evidence" / "reuse_register.jsonl"
    verified = assert_reuse_registered_before_use(
        [REPO_ROOT / "src", REPO_ROOT / "scripts"], register
    )
    # The derived population, stated so a reader of the test output sees it changed.
    assert verified == {}, (
        f"provenance-marked modules now exist ({sorted(verified)}); each must carry a "
        f"complete fifteen-field register row, and this assertion message is the "
        f"explicit record that the population is no longer empty"
    )


# --- append safety -----------------------------------------------------------------------


def test_registering_appends_and_never_rewrites(tmp_path: Path) -> None:
    register = tmp_path / "reuse_register.jsonl"
    register_reuse(register, _complete_record("RU-001"))
    first_bytes = register.read_bytes()
    register_reuse(register, _complete_record("RU-002"))
    after = register.read_bytes()
    assert after.startswith(first_bytes), (
        "the second registration rewrote the first row; the register is append-safe "
        "(NFR-AUD-01 posture) and prior rows are never rewritten or reordered"
    )
    assert len(load_register(register)) == 2


def test_a_duplicated_reuse_id_is_refused_at_load(tmp_path: Path) -> None:
    register = tmp_path / "reuse_register.jsonl"
    register_reuse(register, _complete_record("RU-001"))
    register_reuse(register, _complete_record("RU-001"))
    with pytest.raises(ReuseError):
        load_register(register)


# --- posture and hierarchy ---------------------------------------------------------------


def test_reimplementation_default_and_agplv3_dependency_are_stated_in_the_docstring() -> None:
    """The posture lives where the code lives, not only in a design document."""
    doc = reuse_registry_module.__doc__ or ""
    assert "Reimplementation is the standing default" in doc
    assert "AGPLv3" in doc
    assert "does not resolve" in doc


def test_reuse_error_derives_from_integrity_error() -> None:
    """R-01: every project-defined exception derives from the one base, so the stage
    entry contract's `except IntegrityError` catches it and writes the aborted row."""
    assert issubclass(ReuseError, IntegrityError)
