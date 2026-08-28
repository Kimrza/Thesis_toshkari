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
    MANIFEST_NAME,
    REQUIRED_MANIFEST_FIELDS,
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
    """A complete, valid TE 13.3 manifest with one output file already on disk."""
    digest = _write_artifact(directory, "prepared.csv", body)
    return {
        "created_at_utc": "2026-08-28T00:00:00Z",
        "source_manifest_id": "src-manifest-0001",
        "source_files": [
            {
                "provider": "Madrigal / OpenMadrigal",
                "citation": "experiments4/2022/gps",
                "filename": "gps220301g.003.hdf5",
                "retrieved_at_utc": "2026-08-12T00:00:00Z",
                "sha256": "0" * 64,
            }
        ],
        "processing": {
            "phase_id": "P1",
            "target_definition_id": "P1-GRID-MEDIAN",
            "cell_rule": "floor(lat), floor(lon), half-open",
            "hourly_aggregation": "median",
        },
        "schema_version": "1.0.0",
        "units": {"vtec": "TECU"},
        "row_counts": {"ARUC": 8760, "BSHM": 8760, "NICO": 8760},
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
    """Negative control: the label is derived, never chosen."""
    manifest = _manifest_for(tmp_path)
    manifest["dataset_version"] = "deadbeefcafe"
    with pytest.raises(ReleaseError) as excinfo:
        write_release(tmp_path, manifest)
    assert "not the first" in str(excinfo.value)


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
    derived = dataset_version_for(content_hash_of(manifest["output_files"]))

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
    content = content_hash_of(manifest["output_files"])

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
