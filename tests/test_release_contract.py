"""TA-15: the TE 13.3 release contract, D-29's version encoding, R-13's overwrite refusal.

Purpose
-------
`tests/test_release_hashes.py` verifies that *recorded evidence hashes still match their
files*. That is real coverage of mutation **detection**, and it is not TA-15. TA-15 is the
release **contract**: every TE 13.3 manifest field present, `dataset_version` derived and
verified under D-29, and `write_release` refusing to overwrite an existing release (R-13).
Derived 2026-08-28 before this module was written: `test_release_hashes.py` matched none of
`dataset_version`, `mask_id`, `feature_set_id`, `row_count` or `exclusion`, and exercised no
overwrite refusal. This module is the missing half.

Inputs
------
`tmp_path` only. Every test builds its own release in a temporary directory; the `evidence/`
tree is never written to, and no test here reads anything under the restricted root.

Re-run behaviour
----------------
Fully deterministic and self-contained. No network, no clock dependence, no shared state
between tests. Re-running yields identical results.

Governance
----------
* **TE 13.3** -- the fourteen manifest fields. Enumerated once in
  `src/data/release.REQUIRED_MANIFEST_FIELDS`; this module asserts against that tuple and
  derives its count with `len()` rather than hardcoding a numeral, so the enumeration and
  the count cannot drift apart.
* **D-29** -- 12-hex `dataset_version`, verify-on-write prefix uniqueness.
* **R-13** -- refusal to write into a directory that already holds a release.
* **R-11** -- identity is the `content_hash`.
* Written under **D-31**, which signed G-09 and authorised creating this module.
* `team.md`: every hard rule gets a test proving the violation is **caught**, not only a
  test that the happy path works. Every rule below carries its negative control.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import ReleaseError  # noqa: E402
from src.data.release import (  # noqa: E402
    DATASET_VERSION_HEX_LENGTH,
    EXCLUSION_ENTRY_FIELDS,
    MANIFEST_NAME,
    PROCESSING_PHASE1_FIELDS,
    REQUIRED_MANIFEST_FIELDS,
    ROW_COUNT_AXES,
    SOURCE_FILE_FIELDS,
    collision_probability,
    content_hash_of,
    dataset_version_for,
    sha256_of_file,
    verify_release,
    write_release,
)

# --- helpers --------------------------------------------------------------------------


def _write_artifact(directory: Path, name: str, body: bytes) -> str:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / name).write_bytes(body)
    return hashlib.sha256(body).hexdigest()


def _manifest_for(directory: Path, body: bytes = b"row,value\n1,2\n") -> dict:
    """A complete, valid TE 13.3 manifest with one output file already on disk.

    ⚠ SYNTHETIC throughout. Every value is fixture data for the CONTRACT, never a
    transcription of a governed one: `processing.selected_cell_bounds` and
    `station_coordinate_to_cell_rule` are §18.2 forbidden-choice items awaiting their
    freeze, and a fixture carrying the real values would become a second transcription
    competing with `configs/data.yaml` (project.md § Forbidden — no scientific constant
    lives in source or a test).

    Rewritten 2026-09-20 for board **Recommendation 25**. Until then this fixture
    satisfied the contract as it was then enforced — one top-level non-empty test per
    field — while omitting most of TE 13.3's "Required content" column, which was the
    finding itself: a `source_files` entry with no `location_date` and a
    `retrieved_at_utc` key the table does not name; a FOUR-key `processing` block missing
    the provider kindat, the parameters, the cell rule and the selected cell bounds; and
    a station-keyed `row_counts` satisfying one of four mandated axes while reading as a
    satisfied field. That the old fixture cannot pass the new contract is the cheapest
    available proof that the contract now bites.
    """
    digest = _write_artifact(directory, "prepared.csv", body)
    return {
        "created_at_utc": "2026-08-28T00:00:00Z",
        "source_manifest_id": "src-manifest-0001",
        # Six items per file. `filename` carries the FULL provider filename INCLUDING its
        # version suffix: provider version drift is an observed fact of this dataset, and
        # a suffix-less filename makes a mix unrecordable (board Recommendation 8).
        "source_files": [
            {
                "provider": "synthetic-provider",
                "citation": "syn/experiments/0000 (synthetic permanent citation)",
                "location_date": "synthetic-site / 2022-03-01",
                "filename": "syn220301g.003.hdf5",
                "retrieval_date": "2026-08-12",
                "sha256": "0" * 64,
            }
        ],
        # All seven Phase 1 keys. The Phase 2 limb is deliberately absent: Phase 1 code
        # must not produce or require a raw-processing field (TE §7.0, NFR-PHASE-01).
        "processing": {
            "phase_id": "SYN-PHASE",
            "target_definition_id": "SYN-TARGET-DEF",
            "provider_experiment_kindat": "SYNTHETIC instrument/kindat",
            "parameters": "SYNTHETIC parameter list",
            "station_coordinate_to_cell_rule": "SYNTHETIC rule, not the governed one",
            "selected_cell_bounds": "SYNTHETIC bounds, not the governed ones",
            "hourly_aggregation": "SYNTHETIC aggregation",
        },
        "schema_version": "1.0.0",
        "units": {"vtec": "TECU"},
        # All four mandated axes, each a non-empty mapping of label to INTEGER count.
        "row_counts": {
            "by_station": {"SYNA": 8760, "SYNB": 8760, "SYNC": 8760},
            "by_month": {"2022-01": 2232, "2022-02": 2016},
            "by_split": {"F1-train": 2000, "F1-validation": 500},
            "by_qc_stage": {"raw": 26280, "post_support_filter": 26268},
        },
        "exclusions_qc_summary": {"below_support_threshold": 12},
        "fold_ids": ["F1", "F2", "F3", "F4"],
        "mask_ids": ["DEC-COMPARISON-WIDE"],
        "feature_set_ids": ["FS-24H"],
        "output_files": {"prepared.csv": digest},
        "change_record_id": "CR-2026-08-28-DST-RELOC",
    }


# --- the fourteen TE 13.3 fields ------------------------------------------------------


def test_required_field_enumeration_matches_te_13_3() -> None:
    """The enumeration is the contract; its length is derived, never asserted as prose."""
    assert len(REQUIRED_MANIFEST_FIELDS) == len(set(REQUIRED_MANIFEST_FIELDS)), (
        "REQUIRED_MANIFEST_FIELDS contains a duplicate, so its length overstates coverage"
    )
    # The four fields the governance board found untested by name are present.
    for named in ("dataset_version", "mask_ids", "feature_set_ids", "row_counts"):
        assert named in REQUIRED_MANIFEST_FIELDS


def test_written_manifest_carries_every_required_field(tmp_path: Path) -> None:
    """Happy path: a complete manifest is written and every 13.3 field survives to disk."""
    payload = write_release(tmp_path, _manifest_for(tmp_path))
    on_disk = json.loads((tmp_path / MANIFEST_NAME).read_text(encoding="utf-8"))
    for field in REQUIRED_MANIFEST_FIELDS:
        assert field in on_disk, f"TE 13.3 field {field!r} absent from the written manifest"
        assert on_disk[field] not in (None, "", [], {}), f"{field!r} written empty"
    assert payload["content_hash"] == on_disk["content_hash"]


@pytest.mark.parametrize("field", REQUIRED_MANIFEST_FIELDS)
def test_missing_required_field_is_refused(tmp_path: Path, field: str) -> None:
    """Negative control, one per field: dropping any 13.3 field refuses the write.

    Parametrised over the enumeration rather than a hand-picked subset, so a field added
    to TE 13.3 gains its control automatically instead of silently going untested.
    """
    manifest = _manifest_for(tmp_path)
    if field == "dataset_version":
        # dataset_version is derived, so its absence is legal; supplying a WRONG one is
        # the violation, and it has its own test below.
        pytest.skip("dataset_version is derived by write_release; see the D-29 tests")
    manifest.pop(field, None)
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    assert field in str(excinfo.value)
    assert not (tmp_path / MANIFEST_NAME).exists(), (
        "a refused write must leave no manifest behind"
    )


# =======================================================================================
# Board Recommendation 25 — TE 13.3's SECOND column: required CONTENT, not only presence
# =======================================================================================
#
# The board's derivation: TE 13.3 has ten rows naming fourteen field NAMES, and
# `REQUIRED_MANIFEST_FIELDS` matched them exactly — set difference empty both ways, order
# identical. Enforcement was one top-level non-empty check, so a manifest could satisfy
# every enforced check while carrying `source_files: ["x"]`, a four-key `processing`
# block and a station-keyed `row_counts` — precisely the content the table exists to
# require. These controls are the missing half, parametrised over the sub-schema tuples
# so a sub-field added to a tuple gains its control automatically rather than silently
# going untested, exactly as `test_missing_required_field_is_refused` does for the names.


def test_sub_schema_enumerations_have_no_duplicates_and_their_sizes_are_derived() -> None:
    """Sizes are DERIVED with `len()` and printed by the assertion, never asserted as prose.

    Four tuples, four counts, each read off TE 13.3's own row rather than from adjacent
    text (project.md § Way of Working — derive a count programmatically and print it
    before asserting it).
    """
    for name, tuple_ in (
        ("SOURCE_FILE_FIELDS", SOURCE_FILE_FIELDS),
        ("PROCESSING_PHASE1_FIELDS", PROCESSING_PHASE1_FIELDS),
        ("ROW_COUNT_AXES", ROW_COUNT_AXES),
        ("EXCLUSION_ENTRY_FIELDS", EXCLUSION_ENTRY_FIELDS),
    ):
        assert len(tuple_) == len(set(tuple_)), (
            f"{name} contains a duplicate, so its length overstates its coverage and "
            f"every parametrised control below inherits the overstatement"
        )
        assert tuple_, f"{name} is empty; an empty sub-schema enforces nothing"


@pytest.mark.parametrize("field", SOURCE_FILE_FIELDS)
def test_source_file_entry_missing_one_te_item_is_refused(tmp_path: Path, field: str) -> None:
    """One control per TE 13.3 `source_files` item: six per file, not one.

    The board's own example of what passed before: the literal `["x"]`. This drops ONE
    item at a time, which is the harder case — a manifest that looks populated.
    """
    manifest = _manifest_for(tmp_path)
    manifest["source_files"][0].pop(field)
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    assert field in str(excinfo.value)
    assert not (tmp_path / MANIFEST_NAME).exists(), "a refused write leaves no manifest"


def test_a_bare_scalar_source_file_list_is_refused(tmp_path: Path) -> None:
    """The board's literal example: `source_files = ["x"]` passed every enforced check."""
    manifest = _manifest_for(tmp_path)
    manifest["source_files"] = ["x"]
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    assert "not a mapping" in str(excinfo.value)
    assert not (tmp_path / MANIFEST_NAME).exists()


@pytest.mark.parametrize("field", PROCESSING_PHASE1_FIELDS)
def test_processing_block_missing_one_phase1_key_is_refused(tmp_path: Path, field: str) -> None:
    """One control per TE 13.3 Phase 1 `processing` key — all seven, or refuse.

    The kindat, the parameters, the cell rule and the SELECTED CELL BOUNDS were the four
    the board found omitted by the then-current fixture; parametrising over the tuple
    covers those four and the three that happened to be present, without privileging the
    ones a review looked at (project.md — derive the sites, do not carry them from a
    finding's enumeration).
    """
    manifest = _manifest_for(tmp_path)
    manifest["processing"].pop(field)
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    assert field in str(excinfo.value)
    assert not (tmp_path / MANIFEST_NAME).exists()


@pytest.mark.parametrize("axis", ROW_COUNT_AXES)
def test_row_counts_missing_one_axis_is_refused(tmp_path: Path, axis: str) -> None:
    """One control per TE 13.3 row-count axis: station, month, split AND QC stage."""
    manifest = _manifest_for(tmp_path)
    manifest["row_counts"].pop(axis)
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    assert axis in str(excinfo.value)
    assert not (tmp_path / MANIFEST_NAME).exists()


def test_the_station_only_row_counts_shape_the_board_found_is_refused(tmp_path: Path) -> None:
    """The exact pre-repair shape: one axis of four, reading as a satisfied field."""
    manifest = _manifest_for(tmp_path)
    manifest["row_counts"] = {"SYNA": 8760, "SYNB": 8760, "SYNC": 8760}
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    message = str(excinfo.value)
    for axis in ROW_COUNT_AXES:
        assert axis in message, (
            f"the refusal must name every absent axis including {axis!r}; naming one at a "
            f"time turns a four-axis shortfall into four separate runs"
        )


@pytest.mark.parametrize("axis", ROW_COUNT_AXES)
def test_an_empty_row_count_axis_is_refused(tmp_path: Path, axis: str) -> None:
    """Present-but-empty is the shape a presence check cannot distinguish from populated."""
    manifest = _manifest_for(tmp_path)
    manifest["row_counts"][axis] = {}
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    assert axis in str(excinfo.value)


def test_a_non_integer_row_count_is_refused(tmp_path: Path) -> None:
    """Counts are integers; a float would otherwise fail later at `_canonical` (R-11)."""
    manifest = _manifest_for(tmp_path)
    manifest["row_counts"]["by_station"]["SYNA"] = 8760.0
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    assert "not an integer" in str(excinfo.value)


@pytest.mark.parametrize("field", EXCLUSION_ENTRY_FIELDS)
def test_an_exclusion_entry_missing_reason_or_count_is_refused(
    tmp_path: Path, field: str
) -> None:
    """TE 13.3 requires REASONS and COUNTS; a bare total is a count with no reason."""
    manifest = _manifest_for(tmp_path)
    entry = {"reason": "below_support_threshold", "count": 12}
    entry.pop(field)
    manifest["exclusions_qc_summary"] = [entry]
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    assert field in str(excinfo.value)


def test_an_exclusion_summary_that_is_a_bare_total_is_refused(tmp_path: Path) -> None:
    manifest = _manifest_for(tmp_path)
    manifest["exclusions_qc_summary"] = 12
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    assert "exclusions_qc_summary" in str(excinfo.value)


def test_both_accepted_exclusion_shapes_pass(tmp_path: Path) -> None:
    """MUST-NOT-FIRE half. A guard that refused every shape would pass every control above.

    Both shapes carry a reason and a count, which is all TE 13.3 asks; refusing one of
    them would be house style enforced as contract.
    """
    as_mapping = tmp_path / "mapping"
    write_release(as_mapping, _manifest_for(as_mapping))
    assert (as_mapping / MANIFEST_NAME).is_file()

    as_sequence = tmp_path / "sequence"
    manifest = _manifest_for(as_sequence)
    manifest["exclusions_qc_summary"] = [
        {"reason": "below_support_threshold", "count": 12},
        {"reason": "carry_forward_exceeded", "count": 3},
    ]
    write_release(as_sequence, manifest)
    assert (as_sequence / MANIFEST_NAME).is_file()


@pytest.mark.parametrize(
    "escaping_key",
    [
        "/etc/passwd",
        "../outside.csv",
        "nested/../../outside.csv",
        "C:\\Windows\\system32\\drivers\\etc\\hosts",
        "\\\\server\\share\\outside.csv",
    ],
)
def test_an_output_files_key_that_escapes_the_release_is_refused(
    tmp_path: Path, escaping_key: str
) -> None:
    """`target / key` DISCARDS `target` when `key` is absolute — silently, in both worlds.

    The release would then verify against bytes it does not contain: the hash check at
    `write_release` would read a file outside the release directory and pass. `..`
    escapes upward by a different route with the same consequence. Both POSIX and Windows
    absolute forms are covered, because the check must not depend on which OS the release
    was written from.
    """
    manifest = _manifest_for(tmp_path)
    manifest["output_files"] = {escaping_key: "0" * 64}
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    message = str(excinfo.value)
    assert "absolute" in message or ".." in message
    assert not (tmp_path / MANIFEST_NAME).exists()


def test_verify_release_reports_a_content_short_manifest_rather_than_raising(
    tmp_path: Path,
) -> None:
    """`verify_release` REPORTS; `write_release` RAISES. Both run the same sub-contracts.

    A manifest written before Recommendation 25's sub-schemas existed cannot be caught by
    `write_release` — it is already on disk. It is planted here directly, because that is
    exactly the state `verify_release` exists to describe and the only way to reach the
    reporting branch now that the writing branch refuses.
    """
    write_release(tmp_path, _manifest_for(tmp_path))
    on_disk = json.loads((tmp_path / MANIFEST_NAME).read_text(encoding="utf-8"))
    on_disk["row_counts"] = {"SYNA": 8760}  # the pre-Rec-25 station-only shape
    (tmp_path / MANIFEST_NAME).write_text(json.dumps(on_disk), encoding="utf-8")

    problems = verify_release(tmp_path / MANIFEST_NAME)
    assert any("required content not satisfied" in p for p in problems), (
        "verify_release must REPORT a content-short manifest; raising would break its "
        "Sequence[str] contract and skip every later problem in the same file"
    )


# --- R-13: overwrite refusal ----------------------------------------------------------


def test_second_write_to_an_occupied_directory_is_refused(tmp_path: Path) -> None:
    """R-13's overwrite refusal, and that the original bytes are left untouched."""
    write_release(tmp_path, _manifest_for(tmp_path))
    original = (tmp_path / MANIFEST_NAME).read_bytes()

    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, _manifest_for(tmp_path, body=b"row,value\n9,9\n"))
    assert "already exists" in str(excinfo.value)

    assert (tmp_path / MANIFEST_NAME).read_bytes() == original, (
        "the refused second write modified the existing manifest -- R-13's refusal must "
        "leave the original release byte-identical, or immutability is intent not fact"
    )


def test_refusal_fires_before_any_content_is_examined(tmp_path: Path) -> None:
    """R-13 refuses on occupancy alone, so a rejected write cannot partially apply."""
    write_release(tmp_path, _manifest_for(tmp_path))
    broken = {"output_files": {}}  # would fail several later checks
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, broken)
    assert "already exists" in str(excinfo.value), (
        "occupancy must be checked first; otherwise the error a caller sees depends on "
        "which other field happened to be wrong"
    )


# --- D-29: encoding, derivation, verify-on-write --------------------------------------


def test_dataset_version_is_the_first_twelve_hex_of_content_hash(tmp_path: Path) -> None:
    payload = write_release(tmp_path, _manifest_for(tmp_path))
    assert len(payload["dataset_version"]) == DATASET_VERSION_HEX_LENGTH == 12
    assert payload["dataset_version"] == payload["content_hash"][:12]


def test_a_supplied_wrong_dataset_version_is_refused(tmp_path: Path) -> None:
    """Negative control: the label is derived, never chosen (W-7 step 1)."""
    manifest = _manifest_for(tmp_path)
    manifest["dataset_version"] = "deadbeefcafe"
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    assert "supplied by the caller" in str(excinfo.value)


def test_a_supplied_correct_dataset_version_is_also_refused(tmp_path: Path) -> None:
    """W-7 step 1 rejects a call that SUPPLIES dataset_version even when correct:
    a caller-supplied value could only duplicate the derivation or disagree with it."""
    manifest = _manifest_for(tmp_path)
    manifest["dataset_version"] = dataset_version_for(content_hash_of(manifest))
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    assert "supplied by the caller" in str(excinfo.value)


def test_identical_content_yields_an_identical_label(tmp_path: Path) -> None:
    """Idempotence -- the property D-29 says was already PROVIDED."""
    a, b = tmp_path / "a", tmp_path / "b"
    first = write_release(a, _manifest_for(a))
    second = write_release(b, _manifest_for(b))
    assert first["content_hash"] == second["content_hash"]
    assert first["dataset_version"] == second["dataset_version"]


def test_different_content_yields_a_different_label(tmp_path: Path) -> None:
    """Injectivity in the ordinary case, which the prefix check then guarantees."""
    a, b = tmp_path / "a", tmp_path / "b"
    first = write_release(a, _manifest_for(a, body=b"row,value\n1,2\n"))
    second = write_release(b, _manifest_for(b, body=b"row,value\n3,4\n"))
    assert first["content_hash"] != second["content_hash"]
    assert first["dataset_version"] != second["dataset_version"]


def test_prefix_collision_on_different_content_is_refused(tmp_path: Path) -> None:
    """D-29's verify-on-write check -- the mechanism that ESTABLISHES never-reuse.

    A real 48-bit collision is not findable in a test, so the population is forged: an
    existing release is planted whose `dataset_version` equals the new release's derived
    label while its `content_hash` differs. That is exactly the state the check exists to
    refuse, and constructing it directly is the only way to prove the branch runs.
    """
    new_dir = tmp_path / "new"
    manifest = _manifest_for(new_dir)
    derived = dataset_version_for(content_hash_of(manifest))

    planted = tmp_path / "planted"
    planted.mkdir()
    (planted / MANIFEST_NAME).write_text(
        json.dumps({"dataset_version": derived, "content_hash": "f" * 64}),
        encoding="utf-8",
    )

    with pytest.raises(ReleaseError) as excinfo:
        write_release(new_dir, manifest, existing_releases=[planted])
    assert "already names a different release" in str(excinfo.value)


def test_same_prefix_with_same_content_is_not_a_collision(tmp_path: Path) -> None:
    """Must-not-fire: idempotence is not a collision, and R-13 is what guards re-writes."""
    new_dir = tmp_path / "new"
    manifest = _manifest_for(new_dir)
    content = content_hash_of(manifest)

    planted = tmp_path / "planted"
    planted.mkdir()
    (planted / MANIFEST_NAME).write_text(
        json.dumps({"dataset_version": dataset_version_for(content), "content_hash": content}),
        encoding="utf-8",
    )
    payload = write_release(new_dir, manifest, existing_releases=[planted])
    assert payload["dataset_version"] == dataset_version_for(content)


def test_collision_bound_is_recorded_and_matches_d29(tmp_path: Path) -> None:
    """D-29 records ~1.8e-9 at n=1,000 and ~1.8e-7 at n=10,000. Check the figures."""
    assert collision_probability(1_000) == pytest.approx(1.78e-9, rel=0.05)
    assert collision_probability(10_000) == pytest.approx(1.78e-7, rel=0.05)


# --- output_files integrity -----------------------------------------------------------


def test_declared_output_file_absent_is_refused(tmp_path: Path) -> None:
    manifest = _manifest_for(tmp_path)
    manifest["output_files"]["ghost.csv"] = "0" * 64
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    assert "absent" in str(excinfo.value)


def test_output_file_hash_mismatch_is_refused(tmp_path: Path) -> None:
    manifest = _manifest_for(tmp_path)
    manifest["output_files"]["prepared.csv"] = "1" * 64
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    assert "does not match" in str(excinfo.value)


def test_empty_output_files_is_refused(tmp_path: Path) -> None:
    manifest = _manifest_for(tmp_path)
    manifest["output_files"] = {}
    with pytest.raises(ReleaseError):
        write_release(tmp_path, manifest)


# --- verify_release reports rather than raises ----------------------------------------


def test_verify_release_is_clean_for_a_good_release(tmp_path: Path) -> None:
    write_release(tmp_path, _manifest_for(tmp_path))
    assert verify_release(tmp_path / MANIFEST_NAME) == []


def test_verify_release_reports_a_mutated_artifact(tmp_path: Path) -> None:
    """Negative control: mutation after the write is reported, not silently tolerated."""
    write_release(tmp_path, _manifest_for(tmp_path))
    (tmp_path / "prepared.csv").write_bytes(b"row,value\n1,2\n#")
    problems = verify_release(tmp_path / MANIFEST_NAME)
    assert any("do not match" in p for p in problems)


def test_sha256_helper_agrees_with_hashlib(tmp_path: Path) -> None:
    body = b"some bytes"
    (tmp_path / "f.bin").write_bytes(body)
    assert sha256_of_file(tmp_path / "f.bin") == hashlib.sha256(body).hexdigest()
