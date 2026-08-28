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

ACCESS_LOG = EVIDENCE_DIR / "test_run_access_log.jsonl"


def _test_access_record() -> AccessRecord:
    """The access row this module writes before any restricted read.

    `purpose` is `coverage_audit`: integrity verification is custody assessment, not
    analysis, which is the performance-blind class Vision 8.3 permits before G-05. No
    December target value, coverage figure or performance quantity is read, parsed,
    counted or computed by this module.
    """
    return AccessRecord(
        run_id="test_release_hashes",
        retrieved_at_utc="recorded-at-call-time-by-the-runner",
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
    """SHA-256 of a file, streamed so a 45 MB year artifact does not enter memory whole."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
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
