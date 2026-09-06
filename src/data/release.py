"""Immutable dataset releases: the TE 13.3 manifest, D-29's version encoding, R-13's refusal.

Purpose
-------
Write a dataset release whose manifest carries every field TE 13.3 requires, whose
`dataset_version` is derived and verified rather than allocated, and which **refuses** to
overwrite an existing release.

Inputs
------
* `directory` -- where the release is written. Must not already contain a release (R-13).
* `manifest` -- a mapping supplying the THIRTEEN caller-supplied 13.3 fields. Supplying
  `dataset_version` is refused (W-7 step 1, resolved 2026-08-25): the label is a function
  of a `content_hash` that does not exist until the manifest is canonicalized, so a
  caller-supplied value could only duplicate the derivation or disagree with it.
* `release_root` -- the SINGLE authoritative release root (SD-04, Q2=A owner decision at
  a TE 18.3 stop-and-report point). D-29's verify-on-write check enumerates each release
  directory under it. A root that CANNOT BE REACHED refuses the write -- an unreachable
  population is never treated as an empty one, because an empty population makes every
  hash unique and converts the guard into a rubber stamp exactly when it is most needed.
* `existing_releases` -- additional explicit release directories for the same check
  (kept for callers that assemble the population themselves, e.g. tests). Reading either
  surface is **not** a ledger: nothing is allocated and no index is stored.

Re-run behaviour
----------------
**Idempotent in the label, refusing in the act.** The same content always yields the same
`dataset_version` (a pure function of `content_hash`). Writing the same release twice into
the same directory **raises** rather than succeeding quietly -- that is R-13, and it is
what makes a release immutable in practice rather than in intent.

Governance
----------
* **TE 13.3** -- the fourteen manifest fields, enumerated in `REQUIRED_MANIFEST_FIELDS`
  and derived from the table rather than carried from prose.
* **D-29** (2026-08-28) -- `dataset_version` is the first **12 hex** of the release's
  `content_hash`, with a recorded collision bound and a **verify-on-write** check that the
  prefix is unused. The bound is recorded so it can be checked, not relied on; the check
  is what establishes never-reuse.
* **R-11** -- release identity is the `content_hash`. `dataset_version` is a citation
  device; after D-29 it is a citation device with idempotence **and verified injectivity
  within the release population**.
* **R-13** -- `write_release` rejects a directory already containing a release.
* Created under **D-31** (2026-08-28), which signed G-09.

Limitation
----------
The collision bound below is arithmetic, not measurement: no release exists yet, so the
population is projected rather than observed. If it ever approaches those figures, the
prefix length is the parameter to revisit, and revisiting it is a fresh D-number rather
than an implementation choice (TE 18.2).
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any, Final

from src.data.config import ReleaseError

__all__ = [
    "REQUIRED_MANIFEST_FIELDS",
    "INCLUDED_CONTENT_FIELDS",
    "EXCLUDED_CONTENT_FIELDS",
    "DATASET_VERSION_HEX_LENGTH",
    "MANIFEST_NAME",
    "sha256_of_file",
    "canonical_content_json",
    "content_hash_of",
    "dataset_version_for",
    "collision_probability",
    "write_release",
    "verify_release",
]

#: TE 13.3's manifest fields, transcribed from the table -- ten rows, **fourteen** field
#: names (three rows name two fields each). This tuple is the enumeration; any count is
#: derived from it with `len()` rather than written as a numeral in prose.
REQUIRED_MANIFEST_FIELDS: Final[tuple[str, ...]] = (
    "dataset_version",
    "created_at_utc",
    "source_manifest_id",
    "source_files",
    "processing",
    "schema_version",
    "units",
    "row_counts",
    "exclusions_qc_summary",
    "fold_ids",
    "mask_ids",
    "feature_set_ids",
    "output_files",
    "change_record_id",
)

#: D-29: 12 hexadecimal characters = 48 bits.
DATASET_VERSION_HEX_LENGTH: Final[int] = 12

MANIFEST_NAME: Final[str] = "release_manifest.json"

#: R-11's canonical representation (decided 2026-08-25; array clause F-1): the TWELVE of
#: the thirteen caller-supplied 13.3 fields that enter the authoritative identity.
INCLUDED_CONTENT_FIELDS: Final[tuple[str, ...]] = (
    "source_manifest_id",
    "source_files",
    "processing",
    "schema_version",
    "units",
    "row_counts",
    "exclusions_qc_summary",
    "fold_ids",
    "mask_ids",
    "feature_set_ids",
    "output_files",
    "change_record_id",
)

#: Excluded -- exactly the three categories Q6's answer named, bound to fields (R-11):
#: the label (derived FROM the hash, so including it would be circular), the volatile
#: metadata (identical content re-released later MUST reproduce the same identity), and
#: the self-referential hash field.
EXCLUDED_CONTENT_FIELDS: Final[tuple[str, ...]] = (
    "dataset_version",
    "created_at_utc",
    "content_hash",
)


def sha256_of_file(path: Path) -> str:
    """SHA-256 of a file's bytes, streamed so a large artifact does not load into memory."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical(value: Any, trail: str) -> Any:
    """Normalise a value for RFC 8785-profile serialization; refuse what it cannot carry.

    Floats are refused rather than approximated: no identity-bearing 13.3 field is
    float-valued (row counts are integers), and a float that serialises differently
    across platforms would silently break the two-platform byte-identity WS-20/TA-17
    requires of the authoritative identity.
    """
    if isinstance(value, bool) or value is None or isinstance(value, int | str):
        return value
    if isinstance(value, float):
        raise ReleaseError(
            trail,
            "float values are refused in the canonical content representation (R-11): "
            "platform-dependent float serialization would break the byte-identical "
            "two-platform requirement",
        )
    if isinstance(value, Mapping):
        return {str(k): _canonical(v, f"{trail}.{k}") for k, v in sorted(value.items())}
    if isinstance(value, list | tuple):
        return [_canonical(v, f"{trail}[{i}]") for i, v in enumerate(value)]
    raise ReleaseError(
        trail,
        f"value of type {type(value).__name__} has no canonical JSON form (R-11)",
    )


def canonical_content_json(manifest: Mapping[str, Any]) -> bytes:
    """R-11's canonical representation: the twelve included fields, canonical JSON.

    UTF-8, lexicographically sorted keys at every level, no insignificant whitespace
    (RFC 8785 profile). Before serialization, every ARRAY-VALUED included field is
    sorted lexicographically by the serialization of its elements (F-1, 2026-08-25:
    JCS canonicalizes object keys and numbers but does NOT reorder arrays, and a
    directory listing on Kaggle versus local would otherwise yield two canonical
    documents for byte-identical content). The excluded fields -- `dataset_version`,
    `created_at_utc`, `content_hash` -- never enter.

    Raises `ReleaseError` naming any included field that is absent.
    """
    missing = [f for f in INCLUDED_CONTENT_FIELDS if f not in manifest]
    if missing:
        raise ReleaseError(
            "manifest",
            "canonical content representation requires every included TE 13.3 field; "
            "absent: " + ", ".join(missing),
        )
    payload: dict[str, Any] = {}
    for field in INCLUDED_CONTENT_FIELDS:
        value = _canonical(manifest[field], field)
        if isinstance(value, list):
            value = sorted(
                value,
                key=lambda item: json.dumps(
                    item, sort_keys=True, separators=(",", ":"), ensure_ascii=False
                ),
            )
        payload[field] = value
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def content_hash_of(manifest: Mapping[str, Any]) -> str:
    """Release identity (R-11): SHA-256 over the canonical content representation.

    A pure function of the twelve included caller-supplied fields, so identical content
    yields an identical identity regardless of insertion order, platform, or the time
    of release -- the idempotence D-29 rests on. (Before 2026-09-05 this hashed only
    `output_files`; R-11's decided canonical representation covers all twelve included
    fields, so two releases with identical bytes but different processing provenance no
    longer share an identity.)
    """
    return hashlib.sha256(canonical_content_json(manifest)).hexdigest()


def dataset_version_for(content_hash: str) -> str:
    """D-29's encoding: the first 12 hex characters of `content_hash`."""
    if len(content_hash) != 64 or any(c not in "0123456789abcdef" for c in content_hash):
        raise ReleaseError(
            "content_hash",
            f"expected 64 lowercase hex characters, got {content_hash!r}",
        )
    return content_hash[:DATASET_VERSION_HEX_LENGTH]


def collision_probability(n_releases: int) -> float:
    """D-29's recorded collision bound: approximately n^2 / 2^49 at 48 bits.

    Recorded so it can be **checked**, not relied on. Never-reuse is established by the
    verify-on-write check in `write_release`, not by this number being small.
    """
    if n_releases < 0:
        raise ValueError("n_releases must be non-negative")
    return (n_releases**2) / float(2**49)


def _existing_prefixes(existing_releases: Iterable[Path]) -> dict[str, str]:
    """Map `dataset_version -> content_hash` over the existing release population.

    This read-back is D-29's verify-on-write input. It allocates nothing and stores no
    index, which is why it is not the release ledger the owner declined.
    """
    prefixes: dict[str, str] = {}
    for directory in existing_releases:
        manifest_path = Path(directory) / MANIFEST_NAME
        if not manifest_path.is_file():
            continue
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ReleaseError(
                manifest_path,
                f"existing release manifest could not be read for the D-29 "
                f"prefix-uniqueness check ({exc}); the check cannot be skipped, because "
                f"skipping it is exactly the silent acceptance D-29 forbids",
            ) from exc
        version = data.get("dataset_version")
        content = data.get("content_hash")
        if isinstance(version, str) and isinstance(content, str):
            prefixes[version] = content
    return prefixes


def _enumerate_release_root(release_root: Path) -> list[Path]:
    """SD-04: enumerate the single authoritative release root, or REFUSE.

    An unreachable root is never treated as an empty population -- an empty population
    makes every hash unique, which turns D-29's guard into a rubber stamp at exactly the
    moment it is most needed (Q2=A, the owner decision at the TE 18.3 stop-and-report
    point).
    """
    root = Path(release_root)
    if not root.is_dir():
        raise ReleaseError(
            root,
            "the single authoritative release root is unreachable; write_release "
            "REFUSES rather than treating an unreachable population as empty (SD-04): "
            "an empty population makes every hash unique and converts D-29's "
            "verify-on-write guard into a rubber stamp",
        )
    try:
        return sorted(child for child in root.iterdir() if child.is_dir())
    except OSError as exc:
        raise ReleaseError(
            root,
            f"the single authoritative release root could not be enumerated ({exc}); "
            f"write_release refuses rather than proceeding on a partial population "
            f"(SD-04)",
        ) from exc


def write_release(
    directory: Path,
    manifest: Mapping[str, Any],
    *,
    release_root: Path | None = None,
    existing_releases: Iterable[Path] = (),
) -> dict[str, Any]:
    """Write an immutable release, or raise.

    Order of checks is deliberate: R-13's refusal fires **before** anything is computed or
    written, so a rejected write leaves the target directory exactly as it was.

    `release_root` is the single authoritative release root D-29's verify-on-write check
    enumerates (SD-04; resolved from `configs/data.yaml` `roots.release_root` against the
    platform workspace root). Governed callers MUST pass it; it is optional only so a
    caller may assemble the population explicitly via `existing_releases` (tests). When
    passed and unreachable, the write REFUSES -- never an empty-population pass.

    Raises
    ------
    ReleaseError
        * the directory already contains a release (**R-13**);
        * the caller supplied `dataset_version` (**W-7 step 1**: the label is derived,
          never chosen -- a supplied value could only duplicate the derivation or
          disagree with it);
        * a TE 13.3 field is missing or empty;
        * `output_files` is empty, or an entry's recorded hash does not match the file;
        * the release root is unreachable (**SD-04**);
        * the 12-hex prefix already names a **different** `content_hash` (**D-29**).
    """
    target = Path(directory)
    manifest_path = target / MANIFEST_NAME

    # --- R-13: refuse before doing anything else --------------------------------------
    if manifest_path.exists():
        raise ReleaseError(
            manifest_path,
            "a release already exists in this directory; TE 13.3 requires the final "
            "dataset to be write-protected or stored under a NEW version rather than "
            "overwritten, so this write is refused and the existing bytes are untouched",
        )

    # --- W-7 step 1: the caller supplies thirteen fields and never the label -----------
    if "dataset_version" in manifest:
        raise ReleaseError(
            target,
            "dataset_version was supplied by the caller; write_release DERIVES it from "
            "the release's own content_hash (W-7, D-29) and a caller-supplied value "
            "could only duplicate the derivation or disagree with it -- it is not the "
            "caller's to choose",
        )

    payload: dict[str, Any] = dict(manifest)

    # --- output_files must exist and verify -------------------------------------------
    output_files = payload.get("output_files")
    if not isinstance(output_files, Mapping) or not output_files:
        raise ReleaseError(
            target,
            "output_files is missing or empty; TE 13.3 requires a relative artifact path "
            "and SHA-256 for every release file, and a release with no files has no "
            "identity to hash",
        )
    for rel_path, recorded in sorted(output_files.items()):
        artifact = target / rel_path
        if not artifact.is_file():
            raise ReleaseError(
                artifact,
                "declared in output_files but absent from the release directory",
            )
        actual = sha256_of_file(artifact)
        if actual != recorded:
            raise ReleaseError(
                artifact,
                f"recorded SHA-256 {recorded} does not match the file as written ({actual})",
            )

    # --- identity and D-29's derived label --------------------------------------------
    content_hash = content_hash_of(payload)
    derived_version = dataset_version_for(content_hash)
    payload["content_hash"] = content_hash
    payload["dataset_version"] = derived_version

    # --- D-29 verify-on-write: the prefix must not already name different content -----
    population: list[Path] = list(existing_releases)
    if release_root is not None:
        population.extend(_enumerate_release_root(release_root))
    for known_version, known_hash in _existing_prefixes(population).items():
        if known_version == derived_version and known_hash != content_hash:
            raise ReleaseError(
                target,
                f"dataset_version {derived_version!r} already names a different release "
                f"(content_hash {known_hash}); D-29's verify-on-write check refuses rather "
                f"than reusing a citation label, which is what 'never reused' requires",
            )

    # --- every TE 13.3 field present and non-empty -------------------------------------
    missing = [f for f in REQUIRED_MANIFEST_FIELDS if payload.get(f) in (None, "", [], {})]
    if missing:
        raise ReleaseError(
            target,
            f"TE 13.3 manifest fields missing or empty: {', '.join(missing)} "
            f"({len(missing)} of {len(REQUIRED_MANIFEST_FIELDS)})",
        )

    target.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return payload


def verify_release(manifest_path: Path) -> list[str]:
    """Report problems with a written release. Returns an empty list when it verifies.

    Reports rather than raises, matching the approved `Sequence[str]` contract. D-29 closed
    the read-back hole on the **write** path, so this function is a reporting aid and not
    the mechanism never-reuse depends on -- stated here so a reader does not mistake a
    clean report for the guarantee.
    """
    path = Path(manifest_path)
    problems: list[str] = []
    if not path.is_file():
        return [f"{path}: no release manifest"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: manifest unreadable ({exc})"]

    for field in REQUIRED_MANIFEST_FIELDS:
        if data.get(field) in (None, "", [], {}):
            problems.append(f"{path}: TE 13.3 field {field!r} missing or empty")

    output_files = data.get("output_files")
    if isinstance(output_files, Mapping):
        for rel_path, recorded in sorted(output_files.items()):
            artifact = path.parent / rel_path
            if not artifact.is_file():
                problems.append(f"{artifact}: declared in output_files but absent")
            elif sha256_of_file(artifact) != recorded:
                problems.append(f"{artifact}: bytes do not match the recorded SHA-256")
        try:
            expected = content_hash_of(data)
        except ReleaseError as exc:
            problems.append(f"{path}: canonical content representation failed ({exc})")
        else:
            if data.get("content_hash") != expected:
                problems.append(
                    f"{path}: content_hash does not match the canonical content "
                    f"representation (R-11) — a label/hash mismatch is an integrity "
                    f"violation, not a discrepancy to reconcile"
                )
            if data.get("dataset_version") != expected[:DATASET_VERSION_HEX_LENGTH]:
                problems.append(
                    f"{path}: dataset_version is not the first {DATASET_VERSION_HEX_LENGTH} "
                    f"hex of content_hash (D-29)"
                )
    return problems
