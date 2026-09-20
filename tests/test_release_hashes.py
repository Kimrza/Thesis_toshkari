"""Release-hash and byte-integrity verification for the governed evidence base.

PURPOSE. `Technical_Environment_and_Research_Implementation` §13.3 requires every
dataset release to record immutable SHA-256 hashes and to be write-protected or
stored under a new version rather than overwritten, gated by a mutation-protection
test (§19 TA-15). §13.7 requires exact equality for hashes, schemas, partition
membership, IDs and deterministic CPU transformations. This module is the executable
form of both: it recomputes every hash the evidence base declares and fails on any
divergence.

INPUTS. Read-only, from the repository working tree:
  * `evidence/audit_evidence_2022-*/sha256_manifest.json` -- one mapping of
    filename -> sha256 per acquisition month, plus the merged year artifact;
  * `evidence/audit_ec1_2026-08-15/ec1-audit-report.json` -- the EC-1 driver-audit
    recorded hashes (twelve Kyoto Dst pages plus the Canadian F10.7 flux table);
  * `.gitattributes` -- the normalization policy those hashes depend on.

RE-RUN / REPRODUCIBILITY BEHAVIOUR. Pure function of the working tree: no network,
no writes, no fixtures, no ordering dependence. It must pass in a FRESH CLONE on
both governed platforms (local and Kaggle, TE §9.1). That last property is the one
this module exists to protect, and the reason it also asserts the normalization
policy rather than only the hashes -- see below.

WHY THE .gitattributes ASSERTION IS PART OF AN INTEGRITY TEST. Recorded hashes are
computed over exact provider- or script-produced bytes. With `core.autocrlf=true`
and no attributes, Git checked every governed artifact out CRLF-converted on
Windows: all thirteen manifests and the EC-1 hashes mismatched the working tree
while matching the index, `scripts/merge_coverage_year.py` exited at its
verification line on every month, and a real tampering event was indistinguishable
from a checkout artifact. Hashes alone cannot detect the cause, so the policy that
prevents it is asserted directly.

Origin: GOV-2026-08-20-RA-01 finding DATA-01, confirmed 2026-08-21; remediation
approved the same day (Rec 17, option A).

Run: pytest tests/test_release_hashes.py
"""

from __future__ import annotations

import ast
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.locked_test import AccessRecord, open_restricted  # noqa: E402

EVIDENCE_DIR = REPO_ROOT / "evidence"
RESTRICTED_DIR = EVIDENCE_DIR / "locked_test_restricted"
GITATTRIBUTES = REPO_ROOT / ".gitattributes"
EC1_REPORT = EVIDENCE_DIR / "audit_ec1_2026-08-15" / "ec1-audit-report.json"
KYOTO_DIR = EVIDENCE_DIR / "audit_ec1_2026-08-15" / "kyoto_dst"
F107_FILE = EVIDENCE_DIR / "audit_ec1_2026-08-15" / "nrcan_f107" / "fluxtable.txt"

# --- the restricted-root chokepoint (R-28, ruled 2026-08-28) --------------------------
#
# This module is one of R-28s enumerated `tests/` exemption modules: it may HOLD the
# restricted-root literal, because asserting where the boundary is requires naming it.
# The exemption never covers obtaining the CONTENT. Every read below that touches a file
# under the restricted root goes through `open_restricted`, which writes a durable
# `AccessRecord` BEFORE returning the path (FR-P1-02-3, VAL-2, governance-guards R-25).
#
# Before 2026-08-28 this module read restricted content directly and wrote no access row
# at all -- the RES-04 hazard `evidence/experiment_registry.md:79-83` recorded as
# "occurring in fact rather than in principle" (GOV-2026-08-28-FD-01 Rec 2, VAL-02,
# Validation Auditor veto). Corrected under D-31, which signed G-09 and thereby authorised
# editing this file.

# TEST-MODE ACCESS LOG, separated 2026-09-20 (Recommendation 1, owner ruling = option 2).
#
# Until this remediation, every access row this module wrote landed in
# `evidence/test_run_access_log.jsonl`, the SAME file a real governed December access would
# use. 5,640 of that file's 5,964 rows came from this module alone, so the artifact a G-06
# reviewer must read to find a genuine access was 100% suite noise. The custody rule is
# unchanged -- a restricted read still writes a durable `AccessRecord` BEFORE the read -- but
# the destination is now a test-mode sidecar under `artifacts/exec_evidence/`, which is
# gitignored. `evidence/test_run_access_log.jsonl` is reserved for real, governed accesses
# and is closed to further appends; the historical rows are preserved unedited and described
# in `evidence/test_run_access_log.SUPERSEDED_2026-09-20.md`. Nothing is deleted.
ACCESS_LOG = REPO_ROOT / "artifacts" / "exec_evidence" / "test_access_log.jsonl"


def _test_access_record() -> AccessRecord:
    """The access row this module writes before any restricted read.

    `purpose` is `coverage_audit`: integrity verification is custody assessment, not
    analysis, which is the performance-blind class Vision 8.3 permits before G-05. No
    December target value, coverage figure or performance quantity is read, parsed,
    counted or computed by this module.

    `retrieved_at_utc` is a REAL timestamp, taken at call time. It carried the placeholder
    string `"recorded-at-call-time-by-the-runner"` on all 5,964 historical rows, which left
    FR-P1-02-3's ordering requirement unverifiable from the very log that records it
    (Recommendation 1). `AccessRecord.__post_init__` now refuses any value that does not
    parse as ISO-8601, so the placeholder cannot come back. This matches what
    `scripts/06_train_and_predict.py` and `scripts/07_evaluate_and_report.py` already do.
    """
    return AccessRecord(
        run_id="test_release_hashes",
        retrieved_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        scope="restricted-root manifests and declared artifacts, bytes and hashes only",
        purpose="coverage_audit",
        performance_inspected=False,
        locked_test_accessed=True,
        authorization="TA-15 integrity verification; Vision 8.3 performance-blind class",
    )


def _read_guarded(path: Path) -> Path:
    """Return `path` for reading, routing it through the chokepoint when restricted.

    A path outside the restricted root is returned unchanged: `open_restricted` REFUSES
    ordinary paths by contract, so routing everything through it would raise rather than
    protect.
    """
    if path.is_relative_to(RESTRICTED_DIR):
        return open_restricted(path, record=_test_access_record(), registry=ACCESS_LOG)
    return path

# Paths whose bytes are governed and must never be line-ending normalized.
PROTECTED_PATH_GLOBS = ("evidence/**", "artifacts/**", "tests/fixtures/**")

CHUNK = 1 << 20


def _sha256(path: Path) -> str:
    """SHA-256 of a file, streamed so a 45 MB year artifact does not enter memory whole.

    ROUTED THROUGH THE CHOKEPOINT since 2026-09-20 (Recommendation 32). This function was
    the module's real restricted-byte reader and it opened `path` directly: the manifest
    read at `_declared_artifacts` was guarded, but `_sha256(artifact)` -- called on the
    December artifacts those manifests declare -- was not, so the bytes that matter most
    were obtained with NO `AccessRecord`. R-28's `RESTRICTED_LITERAL_EXEMPT_MODULES`
    exemption covers HOLDING the restricted-root literal and has never covered obtaining
    the CONTENT; its own comment says so. Guarding here rather than at each call site is
    deliberate: `_sha256` is the single place the bytes are actually opened, so one guard
    home covers every present and future caller (`nfr-design` c58).

    An ordinary path passes through unchanged -- `_read_guarded` returns it as-is, because
    `open_restricted` REFUSES a non-restricted path by contract.
    """
    digest = hashlib.sha256()
    with _read_guarded(path).open("rb") as handle:
        while chunk := handle.read(CHUNK):
            digest.update(chunk)
    return digest.hexdigest()


def _manifests() -> list[Path]:
    """Every declared hash manifest anywhere under evidence/, sorted for stable ids.

    Searched RECURSIVELY and therefore across both evidence roots. A non-recursive glob
    over the ordinary root alone found 11 of 15 after decision D-15 relocated the December
    and merged-year artifacts under `evidence/locked_test_restricted/` -- so it stopped
    verifying exactly the artifacts whose integrity matters most. Custody relocation must
    never remove an artifact from hash verification.
    """
    if not EVIDENCE_DIR.is_dir():
        return []
    return sorted(EVIDENCE_DIR.rglob("sha256_manifest.json"))


def _declared_artifacts() -> list[tuple[Path, str, str]]:
    """Flatten every manifest into (manifest_path, declared_filename, recorded_sha256)."""
    rows: list[tuple[Path, str, str]] = []
    for manifest in _manifests():
        entries = json.loads(_read_guarded(manifest).read_text(encoding="utf-8"))
        for name, recorded in sorted(entries.items()):
            rows.append((manifest, name, recorded))
    return rows


def _ec1_recorded() -> list[tuple[str, Path, str]]:
    """EC-1 recorded hashes as (label, path, recorded_sha256)."""
    if not EC1_REPORT.is_file():
        return []
    report = json.loads(EC1_REPORT.read_text(encoding="utf-8"))
    rows: list[tuple[str, Path, str]] = []

    kyoto = report.get("obligation_1_kyoto_dst", {})
    for month, record in sorted(kyoto.items(), key=lambda kv: int(kv[0])):
        recorded = record.get("sha256")
        if not recorded:
            continue
        declared = record.get("file") or record.get("path") or record.get("filename")
        name = Path(str(declared).replace("\\", "/")).name if declared else (
            f"dst_provisional_2022{int(month):02d}.html"
        )
        rows.append((f"kyoto_dst_2022-{int(month):02d}", KYOTO_DIR / name, recorded))

    f107 = report.get("obligation_2_canadian_f107", {})
    if f107.get("sha256"):
        rows.append(("canadian_f107_fluxtable", F107_FILE, f107["sha256"]))
    return rows


# --- the evidence base actually verifies ---------------------------------------------


def test_manifests_are_present() -> None:
    """Thirteen manifests are expected: twelve acquisition months plus the merged year.

    Asserted as a floor rather than an equality so that adding a month's evidence does
    not fail the suite, while a manifest silently disappearing does.
    """
    manifests = _manifests()
    assert manifests, f"no sha256_manifest.json found under {EVIDENCE_DIR}"
    # 15 as at 2026-08-21: twelve acquisition months, the merged year, and the two
    # superseded_2026-08-16 snapshots. Asserted as a floor so adding evidence does not
    # fail the suite, while a manifest silently disappearing does.
    assert len(manifests) >= 15, (
        f"expected at least 15 hash manifests (twelve months, the merged year, and two "
        f"superseded snapshots), found {len(manifests)}: "
        f"{[str(m.parent.relative_to(EVIDENCE_DIR)) for m in manifests]}"
    )
    restricted = [m for m in manifests if m.is_relative_to(RESTRICTED_DIR)]
    assert restricted, (
        "no manifest was found under the restricted custody root; after D-15 the December "
        "and merged-year manifests live there, and a collector that misses them silently "
        "stops verifying the locked month"
    )


@pytest.mark.parametrize(
    "manifest,name,recorded",
    _declared_artifacts(),
    ids=lambda v: v.parent.name if isinstance(v, Path) else str(v),
)
def test_declared_artifact_matches_its_recorded_hash(
    manifest: Path, name: str, recorded: str
) -> None:
    """Every artifact a manifest declares exists and hashes to the recorded value."""
    artifact = manifest.parent / name
    assert artifact.is_file(), (
        f"{manifest.parent.name}/{name} is declared in {manifest.name} but is absent "
        f"from the tree. A manifest that names a missing file cannot verify anything."
    )
    actual = _sha256(artifact)
    assert actual == recorded, (
        f"{manifest.parent.name}/{name} does not match its recorded hash.\n"
        f"  recorded: {recorded}\n"
        f"  actual:   {actual}\n"
        f"If this fails in a fresh clone, check `git check-attr -a {artifact.relative_to(REPO_ROOT)}` "
        f"reports `text: unset`; line-ending normalization is the known cause "
        f"(GOV-2026-08-20-RA-01 DATA-01)."
    )


@pytest.mark.parametrize("label,path,recorded", _ec1_recorded(), ids=lambda v: str(v))
def test_ec1_recorded_hash_matches(label: str, path: Path, recorded: str) -> None:
    """The EC-1 driver audit's recorded hashes reproduce: twelve Kyoto pages plus F10.7."""
    assert path.is_file(), f"{label}: recorded in the EC-1 report but absent at {path}"
    actual = _sha256(path)
    assert actual == recorded, (
        f"{label} ({path.name}) does not match its EC-1 recorded hash.\n"
        f"  recorded: {recorded}\n  actual:   {actual}"
    )


# --- the policy the hashes depend on -------------------------------------------------


def test_gitattributes_disables_normalization_for_governed_paths() -> None:
    """Governed byte paths are marked `-text`, and no later rule re-enables it.

    In .gitattributes the LAST matching pattern wins, so an ordering mistake -- a
    generic `*.json text eol=lf` placed after `evidence/** -text` -- silently restores
    the exact failure this guards against. The line index of each rule is therefore
    checked, not just its presence.
    """
    assert GITATTRIBUTES.is_file(), (
        ".gitattributes is absent. Without it, core.autocrlf converts governed "
        "artifacts on checkout and every recorded hash above fails on Windows."
    )
    lines = [ln.split("#", 1)[0].strip() for ln in GITATTRIBUTES.read_text(encoding="utf-8").splitlines()]
    rules = [(i, ln.split()) for i, ln in enumerate(lines) if ln]

    for glob in PROTECTED_PATH_GLOBS:
        protecting = [i for i, parts in rules if parts and parts[0] == glob and "-text" in parts[1:]]
        assert protecting, f"{glob} is not marked `-text` in .gitattributes"
        last_protection = max(protecting)
        # Any later rule whose pattern could also match inside these paths must not set text.
        for i, parts in rules:
            if i <= last_protection or not parts:
                continue
            pattern, attrs = parts[0], parts[1:]
            if pattern.startswith("*.") and any(a == "text" or a.startswith("eol=") for a in attrs):
                pytest.fail(
                    f"line {i + 1}: `{' '.join(parts)}` comes after `{glob} -text` and "
                    f"re-enables normalization for matching files, because the last "
                    f"matching pattern wins. Move generic type rules above the "
                    f"governed-path overrides."
                )


@pytest.mark.parametrize(
    "manifest,name,recorded",
    _declared_artifacts(),
    ids=lambda v: v.parent.name if isinstance(v, Path) else str(v),
)
def test_declared_artifact_has_no_crlf_seam(manifest: Path, name: str, recorded: str) -> None:
    """No governed artifact carries CRLF unless its recorded hash says it should.

    A hash comparison already catches a converted file, but only after the fact and
    only with an opaque message. This states the cause directly: every declared
    artifact whose recorded hash matches an LF form must contain no CRLF pair.
    """
    artifact = manifest.parent / name
    if not artifact.is_file():
        pytest.skip("absence is asserted by test_declared_artifact_matches_its_recorded_hash")
    data = _read_guarded(artifact).read_bytes()
    if b"\r\n" not in data:
        return
    stripped = data.replace(b"\r\n", b"\n")
    assert hashlib.sha256(stripped).hexdigest() != recorded, (
        f"{manifest.parent.name}/{name} is CRLF in the working tree but its recorded "
        f"hash is over the LF form -- line-ending normalization has been re-enabled "
        f"for this path (GOV-2026-08-20-RA-01 DATA-01)."
    )


# --- mutation protection (TA-15) -----------------------------------------------------


def test_mutation_is_detected(tmp_path: Path) -> None:
    """A one-byte change to a declared artifact is caught. Negative control for TA-15.

    Runs against a copy in `tmp_path`; the evidence base is never written to. Without
    this, every assertion above could pass on a verifier that always returns True.
    """
    declared = _declared_artifacts()
    assert declared, "no declared artifacts to test mutation detection against"
    manifest, name, recorded = declared[0]
    source = manifest.parent / name
    if not source.is_file():
        pytest.skip(f"{name} absent; covered by the presence assertion")

    copy = tmp_path / name
    guarded_source = _read_guarded(source)
    copy.write_bytes(guarded_source.read_bytes())
    assert _sha256(copy) == recorded, "copy of an unmutated artifact must still verify"

    copy.write_bytes(guarded_source.read_bytes() + b"#")
    assert _sha256(copy) != recorded, (
        "a mutated artifact hashed to its recorded value -- the verification path is "
        "not actually comparing content"
    )


# --- TA-15: the release contract over the SINGLE authoritative release root (SD-04) ----
#
# Extended 2026-09-05 per the code-generation plan step 8. The full 13.3 field matrix
# and the R-13/D-29 controls live in tests/test_release_contract.py (created under
# D-31); this section adds the SD-04 enumeration-surface controls (Q2=A, the owner
# decision at the TE 18.3 stop-and-report point) plus the field-presence and mutation
# belts the plan names for THIS module, so TA-15's named module exercises the contract
# directly.

from src.data.config import ReleaseError  # noqa: E402
from src.data.release import (  # noqa: E402
    MANIFEST_NAME,
    REQUIRED_MANIFEST_FIELDS,
    content_hash_of,
    dataset_version_for,
    verify_release,
    write_release,
)


def _release_manifest(directory: Path, body: bytes = b"row,value\n1,2\n") -> dict:
    """A complete, valid TE 13.3 manifest with its one output file on disk.

    ⚠ SYNTHETIC throughout, matching `tests/test_release_contract.py::_manifest_for`.
    `processing.station_coordinate_to_cell_rule` and `selected_cell_bounds` are §18.2
    forbidden-choice items awaiting their freeze; a fixture carrying the governed values
    would be a second transcription competing with `configs/data.yaml` (project.md
    § Forbidden). The previous fixture's `cell_rule: "floor(lat), floor(lon), half-open"`
    read like the real rule and is deliberately NOT carried forward.

    Rewritten 2026-09-20 against board **Recommendation 25**'s sub-schema guards
    (`src/data/release.py`: `assert_manifest_content_contract`, wired into
    `write_release`). The previous fixture predated them and would now be refused at three
    fields: a `source_files` entry with no `location_date` and a `retrieved_at_utc` key
    TE §13.3 does not name (the table's item is `retrieval_date`); a FOUR-key
    `processing` block missing the provider kindat, the parameters, the cell rule and the
    selected cell bounds; and a station-keyed `row_counts` satisfying one axis of four.
    `filename` keeps a full provider filename INCLUDING its version suffix — the field
    Recommendation 8's version mixing is recordable in — but with a synthetic stem.
    """
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "prepared.csv").write_bytes(body)
    return {
        "created_at_utc": "2026-09-05T00:00:00Z",
        "source_manifest_id": "src-manifest-0001",
        # Six items per file (SOURCE_FILE_FIELDS): provider, citation, location_date,
        # filename, retrieval_date, sha256.
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
        # All seven Phase 1 keys (PROCESSING_PHASE1_FIELDS). The Phase 2 limb is
        # deliberately absent (TE §7.0, NFR-PHASE-01).
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
        # All four mandated axes (ROW_COUNT_AXES), each a non-empty mapping of label to
        # INTEGER count. Labels are synthetic, not the three governed stations.
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
        "output_files": {"prepared.csv": _sha256(directory / "prepared.csv")},
        "change_record_id": "CR-2026-09-05-CODEGEN",
    }


def test_written_release_carries_every_te_13_3_field(tmp_path: Path) -> None:
    """Plan step 8: all 13.3 manifest fields present -- asserted over the enumeration."""
    root = tmp_path / "releases"
    root.mkdir()
    target = root / "rel-a"
    payload = write_release(target, _release_manifest(target), release_root=root)
    on_disk = json.loads((target / MANIFEST_NAME).read_text(encoding="utf-8"))
    for field in REQUIRED_MANIFEST_FIELDS:
        assert field in on_disk and on_disk[field] not in (None, "", [], {}), (
            f"TE 13.3 field {field!r} missing or empty in the written release"
        )
    assert payload["dataset_version"] == payload["content_hash"][:12]


def test_overwrite_of_an_existing_release_is_refused_bytes_unchanged(tmp_path: Path) -> None:
    """R-13 negative control (plan step 8): refused, and the original bytes untouched."""
    root = tmp_path / "releases"
    root.mkdir()
    target = root / "rel-a"
    write_release(target, _release_manifest(target), release_root=root)
    original = (target / MANIFEST_NAME).read_bytes()
    with pytest.raises(ReleaseError) as excinfo:
        write_release(
            target, _release_manifest(target, body=b"row,value\n9,9\n"), release_root=root
        )
    assert "already exists" in str(excinfo.value)
    assert (target / MANIFEST_NAME).read_bytes() == original


def test_unreachable_release_root_refuses_never_an_empty_population_pass(
    tmp_path: Path,
) -> None:
    """SD-04 negative control: an unreachable root REFUSES -- an empty population makes
    every hash unique and would turn D-29's guard into a rubber stamp."""
    target = tmp_path / "rel-a"
    manifest = _release_manifest(target)
    with pytest.raises(ReleaseError) as excinfo:
        write_release(target, manifest, release_root=tmp_path / "no-such-root")
    assert "unreachable" in str(excinfo.value)
    assert not (target / MANIFEST_NAME).exists(), "a refused write leaves no manifest"

    # A root that exists but is a FILE is equally unreachable as a population.
    not_a_dir = tmp_path / "root-file"
    not_a_dir.write_text("occupied", encoding="utf-8")
    with pytest.raises(ReleaseError):
        write_release(target, manifest, release_root=not_a_dir)


def test_prefix_collision_within_the_release_root_is_refused(tmp_path: Path) -> None:
    """D-29 verify-on-write over the SD-04 enumeration surface: a planted release under
    the root whose label equals the new derivation with a DIFFERENT content_hash."""
    root = tmp_path / "releases"
    root.mkdir()
    target = root / "rel-new"
    manifest = _release_manifest(target)
    derived = dataset_version_for(content_hash_of(manifest))

    planted = root / "rel-planted"
    planted.mkdir()
    (planted / MANIFEST_NAME).write_text(
        json.dumps({"dataset_version": derived, "content_hash": "f" * 64}),
        encoding="utf-8",
    )
    with pytest.raises(ReleaseError) as excinfo:
        write_release(target, manifest, release_root=root)
    assert "already names a different release" in str(excinfo.value)


def test_mutation_of_a_written_release_is_detected(tmp_path: Path) -> None:
    """Plan step 8: post-write mutation of a release artifact is reported."""
    root = tmp_path / "releases"
    root.mkdir()
    target = root / "rel-a"
    write_release(target, _release_manifest(target), release_root=root)
    (target / "prepared.csv").write_bytes(b"row,value\n1,2\n#tampered")
    problems = verify_release(target / MANIFEST_NAME)
    assert any("do not match" in p for p in problems)


# --- the chokepoint drift control (Recommendation 32, 2026-09-20) ---------------------
#
# R-28's boundary "does not weaken slightly; it ends" if a second path to restricted
# content exists. `_sha256` WAS that second path from 2026-08-28 until 2026-09-20: it
# opened December bytes directly while the manifest read beside it was guarded. Nothing
# detected it, because nothing checked. This section is that check.
#
# The control is structural, not textual: it walks this module's OWN AST for every read
# call and refuses any whose receiver is not recognisably safe. A future edit that adds an
# unguarded read must add itself to one of the enumerated lists below, under review --
# which is the only outcome that keeps the boundary from ending quietly again.

#: Read methods that obtain file CONTENT. `write_bytes` / `write_text` are deliberately
#: absent: this module never writes under the restricted root, and `write_restricted` is
#: the guard for anything that would.
READ_METHODS = frozenset({"open", "read_bytes", "read_text"})

#: Module-level constants provably OUTSIDE `evidence/locked_test_restricted/`. Asserted
#: below rather than trusted.
UNRESTRICTED_READ_RECEIVERS = frozenset({"EC1_REPORT", "GITATTRIBUTES"})

#: Local names bound from `_read_guarded(...)` earlier in their own function. Enumerated
#: explicitly rather than inferred, so a rename cannot silently widen the exemption.
GUARDED_LOCALS = frozenset({"guarded_source"})

#: Leftmost names of `tmp_path`-rooted path expressions (`target / MANIFEST_NAME`). Every
#: one is a pytest `tmp_path` descendant and cannot resolve under the real evidence tree.
TMP_PATH_ROOTS = frozenset(
    {"tmp_path", "target", "copy", "root", "planted", "directory", "not_a_dir"}
)


def _receiver_root(node: ast.AST) -> str | None:
    """The leftmost `Name` of a path expression, or None when there is not one."""
    while isinstance(node, ast.BinOp):
        node = node.left
    if isinstance(node, ast.Name):
        return node.id
    return None


def scan_unguarded_reads(source: str, *, filename: str = "<scanned>") -> list[str]:
    """Every content read whose receiver is not recognisably guarded or unrestricted.

    Returned as `"line N: .method() on <receiver>"` strings, so a failure names the site.
    Callable with an arbitrary source string, which is what makes the negative control
    below a real one: it pushes a violating module through THIS function rather than
    asserting that the real module happens to be clean (`nfr-design` c58).
    """
    tree = ast.parse(source, filename=filename)
    offenders: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Attribute) or func.attr not in READ_METHODS:
            continue
        receiver = func.value
        if (
            isinstance(receiver, ast.Call)
            and isinstance(receiver.func, ast.Name)
            and receiver.func.id == "_read_guarded"
        ):
            continue
        root = _receiver_root(receiver)
        if root in UNRESTRICTED_READ_RECEIVERS or root in GUARDED_LOCALS:
            continue
        if root in TMP_PATH_ROOTS:
            continue
        offenders.append(f"line {func.lineno}: .{func.attr}() on {root or type(receiver).__name__}")
    return offenders


def test_no_restricted_read_in_this_module_bypasses_the_chokepoint() -> None:
    """Every content read here is guarded, or its receiver is enumerated as unrestricted.

    The positive limb. Recommendation 32's defect -- `_sha256` opening December bytes with
    no `AccessRecord` -- fails this test at the line that does it.
    """
    offenders = scan_unguarded_reads(
        Path(__file__).read_text(encoding="utf-8"), filename=__file__
    )
    assert not offenders, (
        "unguarded content reads in tests/test_release_hashes.py: "
        + "; ".join(offenders)
        + ". Route the read through `_read_guarded`, or -- only if the path provably "
        "cannot lie under evidence/locked_test_restricted/ -- add its receiver to "
        "UNRESTRICTED_READ_RECEIVERS / GUARDED_LOCALS / TMP_PATH_ROOTS with a stated "
        "reason. R-28: the boundary does not weaken slightly; it ends."
    )


def test_enumerated_unrestricted_receivers_really_are_outside_the_restricted_root() -> None:
    """The allowlist is asserted, not trusted.

    A constant relocated under the restricted root would otherwise keep its exemption
    silently -- which is how D-15's relocation defeated the previous collector (VAL-3).
    """
    for name in sorted(UNRESTRICTED_READ_RECEIVERS):
        value = globals()[name]
        assert isinstance(value, Path), f"{name} is not a Path"
        assert not value.is_relative_to(RESTRICTED_DIR), (
            f"{name} resolves under {RESTRICTED_DIR}; an allowlisted receiver that moved "
            f"into the restricted root is exactly the drift this list must not absorb"
        )


def test_the_drift_scanner_catches_an_injected_unguarded_restricted_read() -> None:
    """NEGATIVE CONTROL. A scanner that never fires proves nothing.

    Three mutants, each pushed through the real public entry point `scan_unguarded_reads`:
    a direct `.open(...)`, a `.read_bytes()`, and a `.read_text(...)` on a receiver in none
    of the three enumerated lists. Each must be reported. The fourth case is the
    must-not-fire limb: the same read routed through `_read_guarded` must NOT be reported.
    """
    mutant_calls = (
        'artifact.open("rb")',
        "artifact.read_bytes()",
        'artifact.read_text(encoding="utf-8")',
    )
    for call in mutant_calls:
        mutant = (
            "from pathlib import Path\n"
            "def offending():\n"
            "    artifact = Path('e/locked_test_restricted/x/records.csv')\n"
            f"    return {call}\n"
        )
        offenders = scan_unguarded_reads(mutant, filename="<mutant>")
        assert offenders, f"the scanner did not catch `{call}` -- it bites nothing"
        assert "artifact" in offenders[0]

    clean = (
        "from pathlib import Path\n"
        "def compliant():\n"
        "    artifact = Path('e/locked_test_restricted/x/records.csv')\n"
        '    return _read_guarded(artifact).open("rb")\n'
    )
    assert not scan_unguarded_reads(clean, filename="<clean>"), (
        "must-not-fire: a read routed through the chokepoint was reported as a bypass"
    )


# --- the separated test-mode access log (Recommendation 1, 2026-09-20) ----------------


def test_the_test_mode_access_log_is_not_the_governed_evidence_log() -> None:
    """Suite rows never again land in the governed access log.

    `evidence/test_run_access_log.jsonl` is reserved for real, governed accesses and is
    closed to further appends; its 5,964 historical rows are preserved unedited and
    described in `evidence/test_run_access_log.SUPERSEDED_2026-09-20.md`.
    """
    assert ACCESS_LOG == REPO_ROOT / "artifacts" / "exec_evidence" / "test_access_log.jsonl"
    assert not ACCESS_LOG.is_relative_to(EVIDENCE_DIR), (
        "the test-mode access log resolves inside evidence/; suite noise would again be "
        "indistinguishable from a governed December access (Recommendation 1)"
    )
    notice = EVIDENCE_DIR / "test_run_access_log.SUPERSEDED_2026-09-20.md"
    assert notice.is_file(), (
        f"{notice.name} is absent; the superseded log must carry its notice, because a "
        f"closed log with no explanation reads as an abandoned one -- records are "
        f"superseded, never deleted"
    )


def test_the_access_record_this_module_writes_carries_a_real_timestamp() -> None:
    """Recommendation 1, limb 3: the placeholder cannot come back.

    All 5,964 historical rows carried `retrieved_at_utc =
    "recorded-at-call-time-by-the-runner"`, which left FR-P1-02-3's ordering requirement
    unverifiable from the log that records it. `AccessRecord.__post_init__` now refuses a
    non-ISO-8601 value; this asserts THIS module's producer satisfies it.
    """
    record = _test_access_record()
    parsed = dt.datetime.fromisoformat(record.retrieved_at_utc)
    assert parsed.tzinfo is not None, "retrieved_at_utc must be timezone-aware UTC"
    assert record.retrieved_at_utc != "recorded-at-call-time-by-the-runner"
