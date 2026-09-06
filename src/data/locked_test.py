"""The restricted-root path guard: one chokepoint for every read under the locked month.

Purpose
-------
D-15 made `evidence/locked_test_restricted/` a governance boundary that holds **only while
exactly one code path reaches it**. `governance-guards` R-28 states the consequence in its
own words: the boundary "does not weaken slightly; it ends" if a second path exists. This
module is that one path.

Inputs
------
* `path` -- the artifact to read, which must lie under `RESTRICTED_ROOT`.
* `record` -- a fully populated `AccessRecord` describing the read *before* it happens.
* `registry` -- the access log the record is appended to (normally
  `evidence/experiment_registry.md`, or a JSONL sidecar in tests and fixtures).

Re-run behaviour
----------------
**Not idempotent by design.** Every call appends one row. `component-methods.md` fixes
"one row per artifact opened", and `inventory-and-registry` gives the reason: one row per
*run* would make the log say less than what happened, and a reviewer could not tell which
reads occurred. Re-running a read legitimately produces a second row.

Ordering contract, which is the whole point
-------------------------------------------
The record is written **and flushed to disk** before the path is returned for reading.
FR-P1-02-3 and `VAL-2` require log-then-read: an access recorded after the fact *fails*
the ordering check rather than satisfying it. Rows 5, 8, 9 and 10 of the project's own
access log are retrospective and say so; rows 6, 7, 11 and 12 set the standard this module
enforces mechanically.

Governance
----------
* `component-methods.md` -- the approved `AccessRecord` shape and `open_restricted`
  signature, reproduced here without widening.
* `governance-guards` R-25 (durable before the read), R-26, R-27, R-28.
* Created under **D-31** (2026-08-28), which signed G-09 and thereby authorised writing
  this module. D-31 records that G-09's own TE 18.3 preconditions were **unmet** when
  signed; nothing in this module claims otherwise.
* This module is the **only** one permitted to contain the restricted-root literal outside
  R-28's enumerated exemption, whose membership is the `RESTRICTED_LITERAL_EXEMPT_MODULES`
  constant below (SD-G-03: a source constant in the guard, never a config — TC-03e governs
  scientific constants, and a security allowlist is not one).
* **Q1 = A (SD-G-01), added at stage 3.5:** `open_restricted` fails CLOSED on a platform
  whose write-durability semantics are uncharacterised. `fsync`'s guarantee is a property
  of the filesystem beneath it, and Kaggle's is characterised nowhere in this project, so
  with `CHARACTERISED_DURABILITY_PLATFORMS` empty the guard refuses on Kaggle — no read,
  no access row consumed — until W-6 step 8's durability measurement is done. The stated
  cost is blocking the pre-G-05 December coverage audit on Kaggle; `local` keeps its
  existing behaviour per the design's scheduling note (the refusal targets the governed
  audit host, and foundation SD-03's unverified-durability stamp already qualifies local
  rows at every freeze gate).
* **Q2 = B (SD-C-02 containment), edited in place 2026-09-06 at `evaluation-and-comparison`
  stage 3.5 on the owner's explicit instruction** (`governance/
  CHANGE_RECORD_2026-09-06_R106_comparison_sets.md`; **flagged for `governance-guards`'
  record and re-check** — this is a sibling unit's module and the edit is additive):
  `AccessRecord` gains two OPTIONAL containment fields, `mask_bundle_ids` and
  `mask_registry_hash`, and `open_restricted` populates them when a frozen-bundle manifest
  is supplied and exists at access time (reads the manifest, hashes its bytes, lists its
  `mask_id`s). The access record thereby CONTAINS evidence derived from the completed mask
  registration, so registration-before-access is proven on any clocks, across any hosts —
  no timestamp comparison (SD-C-02, Q1 = A there). With no manifest the fields stay `None`,
  existing rows and callers are unbroken, and `evaluation-and-comparison`'s
  `require_locked_receipt` REFUSES a `DEC` metric on `None` — the fail-closed half of the
  half-contract. The manifest is write-once per freeze (`src/evaluation/masks.py`, Q4 = A),
  so a mid-registration read sees either the old complete manifest or the new complete one,
  never a partial file.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
from collections.abc import Sequence
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Final

from src.data.config import (
    CHARACTERISED_DURABILITY_PLATFORMS,
    IntegrityError,
    LockedTestError,
    resolve_platform_roots,
)

__all__ = [
    "RESTRICTED_ROOT",
    "RESTRICTED_LITERAL_EXEMPT_MODULES",
    "AccessRecord",
    "PURPOSES",
    "EvidenceScanError",
    "fail_unparseable",
    "open_restricted",
    "write_restricted",
    "assert_no_december_outside_restricted",
]

RESTRICTED_ROOT: Final[str] = "evidence/locked_test_restricted"

#: R-28's enumerated exemption: the ONLY modules permitted to hold the restricted-root
#: literal, INCLUDING the chokepoint itself (the design's prose counts "five members in
#: addition to the chokepoint", i.e. six; the seventh on-disk member,
#: `tests/test_merge_script_restricted_reads.py`, was caught by the membership assertion
#: on first run — DISC-1 records the mechanism working and the prose count lagging).
#: Membership is an EXACT enumerated list, never a directory or substring predicate; the
#: exemption covers holding the LITERAL, never obtaining the CONTENT — any content read
#: beneath the root still goes through `open_restricted` or a synthetic fixture root.
#: `tests/test_locked_test_guard.py` re-derives this set exactly, so an addition or a
#: removal fails there until the list is edited under review (SD-G-03, board BLOCKER
#: VAL-02 closure control).
RESTRICTED_LITERAL_EXEMPT_MODULES: Final[frozenset[str]] = frozenset(
    {
        "src/data/locked_test.py",
        "scripts/merge_coverage_year.py",
        "tests/test_acquisition_window.py",
        "tests/test_phase_boundary.py",
        "tests/test_release_hashes.py",
        "tests/test_locked_test_guard.py",
        "tests/test_merge_script_restricted_reads.py",
    }
)


class EvidenceScanError(IntegrityError):
    """R-27's fail-closed scan limb: a file a custody scan cannot read or parse.

    Rides foundation R-01's "any future integrity-related exception" clause: declared
    here because the residency scan below and the literal scan in
    `tests/test_locked_test_guard.py` are the only raisers, and both call the ONE
    shared helper `fail_unparseable` so the two scans cannot drift apart on the rule
    (SD-G-04).
    """


def fail_unparseable(artifact: object, reason: str) -> None:
    """R-27's shared rule, one home: an unparseable artifact is a FAILURE, never a pass.

    A file the guard cannot read is exactly where a December record would hide, so
    treating it as clean is the one answer that cannot be defended. Getting past a
    genuinely irrelevant unparseable file requires an explicit recorded exclusion,
    never silence. Both custody scans — the residency scan in this module and the
    literal scan in `tests/test_locked_test_guard.py` — call this helper (SD-G-04:
    the one place the rule lives, without coupling the scans themselves).
    """
    raise EvidenceScanError(
        artifact,
        f"cannot be read or parsed ({reason}); an unparseable artifact is a failure, "
        f"not a pass (R-27) — a file the guard cannot read is exactly where a December "
        f"record would hide, and passing it requires an explicit recorded exclusion, "
        f"never silence",
    )

#: The three purposes Vision 8.3 distinguishes — `coverage_audit` and `regime_audit`
#: are performance-blind and permitted before G-05; `locked_evaluation` is the
#: one-shot, hash-before-metrics event G-06 gates — PLUS the two Q2 = C acquisition
#: purposes the R-33 interface amendment adds (`acquisition` unit, accepted by owner
#: ruling 2026-09-05, Q1 = A; change record
#: `governance/CHANGE_RECORD_2026-09-05_R33_write_restricted.md`): `acquisition_read`
#: for a named-accessor read of a restricted input, `acquisition_write` for
#: `write_restricted`. Reusing a knowingly wrong value (`coverage_audit` for an
#: acquisition write) was REJECTED because the access log's whole value is that a
#: G-05 reviewer can read its rows as meaning what they say. `authorization` widens
#: accordingly: for the acquisition purposes it names a D-number.
PURPOSES: Final[frozenset[str]] = frozenset(
    {
        "coverage_audit",
        "regime_audit",
        "locked_evaluation",
        "acquisition_read",
        "acquisition_write",
    }
)


@dataclass(frozen=True)
class AccessRecord:
    """One row of the locked-month access log, describing a read before it happens.

    The two OPTIONAL containment fields (`mask_bundle_ids`, `mask_registry_hash`) are
    SD-C-02's ordering evidence, added additively 2026-09-06 under the Q2 = B owner
    instruction (`governance/CHANGE_RECORD_2026-09-06_R106_comparison_sets.md`; flagged for
    `governance-guards`' re-check): the record CONTAINS the frozen mask bundle's `mask_id`s
    and its write-once manifest's SHA-256 as found at access time, so a mask registered
    AFTER the access cannot appear in the record — registration-before-access is proven by
    containment, on any clocks. `None` means no manifest was supplied or none existed;
    `evaluation-and-comparison`'s `require_locked_receipt` refuses a `DEC` metric on `None`
    (the fail-closed half). Existing rows and callers are unbroken: both fields default and
    the required-field check below is untouched.
    """

    run_id: str
    retrieved_at_utc: str
    scope: str
    purpose: str
    performance_inspected: bool
    locked_test_accessed: bool
    authorization: str
    mask_bundle_ids: tuple[str, ...] | None = None
    mask_registry_hash: str | None = None

    def __post_init__(self) -> None:
        for field_name in (
            "run_id",
            "retrieved_at_utc",
            "scope",
            "purpose",
            "authorization",
        ):
            if not getattr(self, field_name):
                raise LockedTestError(
                    "AccessRecord",
                    f"field {field_name!r} is empty; an access row that does not say who "
                    f"read what, when, why and under whose authority is not a record",
                )
        if self.purpose not in PURPOSES:
            raise LockedTestError(
                "AccessRecord",
                f"purpose {self.purpose!r} is not one of {sorted(PURPOSES)}",
            )
        if not self.locked_test_accessed:
            raise LockedTestError(
                "AccessRecord",
                "locked_test_accessed must be True for any read under RESTRICTED_ROOT; "
                "TE 13.4 makes the flag the fact a G-06 reviewer establishes",
            )


def _repo_root() -> Path:
    """The repository root, derived from this module's OWN location.

    One home for the boundary derivation both directions share (read and write), so
    a caller cannot relocate the boundary by passing a different root. This function
    is also the module's SUPPORTED TEST SEAM: tests that must exercise the guard
    against a synthetic root monkeypatch THIS function (never the boundary constant,
    and never a real December artifact) — the R-33 negative controls run against
    `tmp_path` roots exactly this way.
    """
    return Path(__file__).resolve().parent.parent.parent


def _restricted_root(repo_root: Path) -> Path:
    return (repo_root / RESTRICTED_ROOT).resolve()


def _append_and_flush(registry: Path, record: AccessRecord) -> str:
    """Append one row, stamp it with the guard's OWN write time, force it to disk.

    `os.fsync` is what makes "durable before the read" true rather than merely intended
    (R-25). A row sitting in the OS page cache when the process dies is a read that
    happened with no record of it -- exactly the failure the ordering rule exists to
    prevent.

    **`logged_at_utc` is stamped here, by the guard, never by the caller.**
    `retrieved_at_utc` is caller-supplied and descriptive; a field the caller controls
    cannot evidence that the log preceded the read. `logged_at_utc` is written
    immediately before the fsync, and therefore before `open_restricted` returns the path
    the caller then reads -- so comparing it against any later artifact or run timestamp
    is a real ordering check rather than a restatement of the caller's intent.

    Found by execution, 2026-08-28: the first run of the routed suites produced 37 rows
    whose `retrieved_at_utc` was all the same caller-supplied placeholder string, leaving
    FR-P1-02-3's ordering requirement unverifiable from the log it is recorded in. This
    field is that defect's fix.
    """
    registry.parent.mkdir(parents=True, exist_ok=True)
    row = asdict(record)
    row["logged_at_utc"] = _dt.datetime.now(_dt.UTC).isoformat()
    line = json.dumps(row, sort_keys=True, ensure_ascii=False)
    with registry.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return row["logged_at_utc"]


def _containment_fields(
    mask_bundle_manifest: Path | None,
) -> tuple[tuple[str, ...] | None, str | None]:
    """SD-C-02's containment evidence, read at access time (Q2 = B, 2026-09-06).

    When a frozen-bundle manifest is supplied and exists, returns its enumerated
    `mask_id`s and its byte-level SHA-256; otherwise `(None, None)` — the fields stay
    unpopulated and the consuming refusal (`require_locked_receipt`) fails closed. A
    manifest that exists but cannot be read or parsed is a FAILURE, not a pass (the same
    R-27 posture as the custody scans): the containment evidence is what a G-06 reviewer
    verifies, and silently recording `None` over a present-but-broken manifest would hide
    exactly the defect the field exists to surface.
    """
    if mask_bundle_manifest is None:
        return None, None
    manifest_path = Path(mask_bundle_manifest)
    if not manifest_path.is_file():
        return None, None
    try:
        raw = manifest_path.read_bytes()
        payload = json.loads(raw.decode("utf-8"))
        mask_ids = tuple(str(m) for m in payload["mask_ids"])
    except (OSError, UnicodeDecodeError, ValueError, KeyError, TypeError) as exc:
        raise LockedTestError(
            manifest_path,
            f"frozen-bundle manifest exists but cannot be read or parsed ({exc}); the "
            f"containment fields are ordering EVIDENCE (SD-C-02) and recording None over a "
            f"present-but-broken manifest would hide the defect rather than surface it",
        ) from exc
    return mask_ids, hashlib.sha256(raw).hexdigest()


def open_restricted(
    path: Path,
    *,
    record: AccessRecord,
    registry: Path,
    mask_bundle_manifest: Path | None = None,
) -> Path:
    """Record the access, flush it, then return `path` for reading.

    When `mask_bundle_manifest` names an existing frozen-bundle manifest
    (`src/evaluation/masks.py`'s write-once artifact), the appended record is populated
    with `mask_bundle_ids` and `mask_registry_hash` read from it AT ACCESS TIME — SD-C-02's
    containment proof that mask registration preceded this access, on any clocks (Q2 = B,
    2026-09-06; additive keyword, existing callers unbroken). With no manifest the two
    fields stay `None` and the DEC metric path refuses downstream (fail-closed).

    Raises
    ------
    LockedTestError
        * when `path` is not under `RESTRICTED_ROOT` -- callers must not route ordinary
          reads through the guard, because a guard that accepts anything stops being
          evidence that restricted reads went through it;
        * when the registry write fails -- **a failed log write aborts the read rather
          than proceeding unlogged.** This is the branch that makes the ordering rule
          enforceable instead of advisory;
        * when a supplied frozen-bundle manifest exists but cannot be read or parsed --
          broken containment evidence aborts the read rather than logging `None`.

    Returns
    -------
    Path
        The same path, resolved. The caller reads it *after* this function returns, which
        is what makes the log-then-read ordering hold by construction.
    """
    # Q1 = A (SD-G-01): refuse FIRST, before any row is appended and before the path is
    # resolved for reading, on a platform whose write-durability semantics are
    # uncharacterised. An AccessRecord is the only evidence the locked test was opened
    # at all; on a platform where fsync's guarantee is unmeasured, a "durable" row is a
    # row that might not exist — the failure this guard exists to prevent. `local` is
    # exempt per the design's scheduling note: the refusal targets the governed audit
    # host (Kaggle today), whose measurement W-6 step 8 owes, and foundation SD-03's
    # unverified-durability stamp already disqualifies local rows as gate evidence.
    # The characterised set is imported from `src/data/config.py` so the two sibling
    # postures (foundation's stamp, this refusal) can never disagree about which
    # platforms are measured.
    platform_label, _ = resolve_platform_roots(os.environ)
    if platform_label != "local" and platform_label not in CHARACTERISED_DURABILITY_PLATFORMS:
        raise LockedTestError(
            path,
            f"restricted read refused on platform {platform_label!r}: its write-"
            f"durability semantics are uncharacterised, so a pre-read access row "
            f"cannot be known durable (Q1=A, SD-G-01; fail-closed) — no read occurs "
            f"and no access row is consumed until W-6 step 8's durability measurement "
            f"characterises the platform",
        )

    resolved = Path(path).resolve()

    # Derive the repository root from this module's own location rather than from the
    # caller, so a caller cannot relocate the boundary by passing a different root.
    root = _restricted_root(_repo_root())

    if not resolved.is_relative_to(root):
        raise LockedTestError(
            resolved,
            f"path is not under {RESTRICTED_ROOT}; open_restricted is the chokepoint for "
            f"restricted reads only, and routing an ordinary read through it would make "
            f"the access log unable to distinguish the two",
        )

    # Q2 = B: populate the SD-C-02 containment fields from the frozen-bundle manifest as
    # found at THIS moment, before the row is appended — the record then contains evidence
    # derived from the completed registration, which is the ordering proof.
    bundle_ids, registry_hash = _containment_fields(mask_bundle_manifest)
    if bundle_ids is not None:
        record = replace(
            record, mask_bundle_ids=bundle_ids, mask_registry_hash=registry_hash
        )

    try:
        _append_and_flush(Path(registry), record)
    except OSError as exc:
        raise LockedTestError(
            registry,
            f"access-log write failed ({exc}); the read is aborted rather than performed "
            f"unlogged -- FR-P1-02-3 requires the record to be durable BEFORE the read",
        ) from exc

    return resolved


def write_restricted(
    path: Path, payload: bytes, *, record: AccessRecord, registry: Path
) -> Path:
    """Log durably FIRST, then write `payload` under the restricted root (R-33, Q2 = C).

    The write-side sibling of `open_restricted`, added under the R-33/BLK-07 interface
    amendment accepted by owner ruling 2026-09-05 (Q1 = A;
    `governance/CHANGE_RECORD_2026-09-05_R33_write_restricted.md`). It lives HERE,
    in `governance-guards`' module, because a separate write path in `acquisition`
    would make a second module name the restricted-root literal, taking R-28's exempt
    list from seven to eight — one module, one door, one durability implementation
    for both directions (SD-A-03). `acquisition` is this function's CALLER, not the
    boundary's co-owner.

    Ordering: **log-before-WRITE.** A write that logged afterwards would leave a
    mutation with no record if it failed between the two operations; a partially
    written December artifact with no access row creates December bytes nobody
    recorded creating, which is worse than a blocked read (W-2a). The shared
    `_append_and_flush` owns the append, the guard-stamped `logged_at_utc` and the
    fsync — one log-then-proceed code path, not two behaviourally identical ones.

    Raises
    ------
    LockedTestError
        * on a platform whose write-durability semantics are uncharacterised — the
          same Q1 = A fail-closed refusal as the read side, before any row is
          appended and before any byte is written (a durability-unknown WRITE is
          strictly worse than a durability-unknown read);
        * when `record.purpose` is not `acquisition_write` — a write recorded under
          a read purpose describes an event that did not happen, and the access
          log's value is that a G-05 reviewer reads its rows as meaning what they say;
        * when `path` is not under `RESTRICTED_ROOT` — ordinary writes must not
          route through the guard (the boundary is derived from `_repo_root()`,
          this module's own location, never from the caller);
        * when the target already exists — a restricted artifact is never
          overwritten; re-acquired bytes go under a new name or behind a recorded
          decision (SEC-A-02's refuse-to-overwrite posture, applied at the boundary);
        * when the access-log append or its durability confirmation fails — **no
          byte is written**: a failed log aborts the write BEFORE any mutation.

    NOTHING here grants December access: BLK-07's authorization limb — which units
    may reach the locked month, and when — is the project decision owner's, and this
    function is mechanism only. No acquisition run may touch calendar 2022-12 while
    BLK-07 stands.
    """
    platform_label, _ = resolve_platform_roots(os.environ)
    if platform_label != "local" and platform_label not in CHARACTERISED_DURABILITY_PLATFORMS:
        raise LockedTestError(
            path,
            f"restricted write refused on platform {platform_label!r}: its write-"
            f"durability semantics are uncharacterised, so neither the pre-write "
            f"access row nor the written bytes can be known durable (Q1=A, SD-G-01 "
            f"applied to the write side; fail-closed) — no row is appended and no "
            f"byte is written",
        )

    if record.purpose != "acquisition_write":
        raise LockedTestError(
            path,
            f"restricted write refused: purpose {record.purpose!r} is not "
            f"'acquisition_write' (R-33, Q2=C); a write recorded under a read purpose "
            f"describes an event that did not happen, and a G-05 reviewer must be able "
            f"to read the access log's rows as meaning what they say",
        )

    resolved = Path(path).resolve()
    root = _restricted_root(_repo_root())
    if not resolved.is_relative_to(root):
        raise LockedTestError(
            resolved,
            f"path is not under {RESTRICTED_ROOT}; write_restricted is the chokepoint "
            f"for restricted writes only, and routing an ordinary write through it "
            f"would make the access log unable to distinguish the two",
        )

    if resolved.exists():
        raise LockedTestError(
            resolved,
            "restricted target already exists; a restricted artifact is never "
            "overwritten -- write under a new name or record the superseding decision "
            "first (SEC-A-02's refuse-to-overwrite posture; NFR-AUD-01's no-silent-"
            "replacement rule applied at the boundary)",
        )

    try:
        _append_and_flush(Path(registry), record)
    except OSError as exc:
        raise LockedTestError(
            registry,
            f"access-log write failed ({exc}); the WRITE is aborted BEFORE any byte "
            f"is written -- R-33's ordering exists so a change cannot happen "
            f"unrecorded, and a mutation with no record is the failure this guard "
            f"prevents",
        ) from exc

    resolved.parent.mkdir(parents=True, exist_ok=True)
    with resolved.open("wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    return resolved


def assert_no_december_outside_restricted(evidence_root: Path) -> Sequence[Path]:
    """FR-P1-02-6's regression guard: December-bearing artifacts outside the restricted root.

    Walks `evidence/` **recursively** and returns every December-bearing artifact found
    outside the restricted root. An empty sequence is the pass condition.

    Recursive by construction: `DATA-01` showed a non-recursive glob silently stopped
    checking the artifacts that matter most, and D-15 relocated 21 files, so a guard that
    only looks one level down would report clean while missing the relocation entirely.

    Membership is decided by **record date**, never by directory name -- `project.md`
    forbids deriving partition membership from a path, after a year-blind acquisition
    predicate filed locked-month records into `audit_evidence_2022-01/`.

    An unreadable file is a **failure**, not a pass (R-27, via the shared
    `fail_unparseable` helper): a file this scan cannot read is exactly where a
    December record would hide. Known narrowing, disclosed not closed: the scan reads
    `*.json` only, while R-27 specifies a per-class walk of every file -- widening it
    is this unit's change to make and is not made at this step (recorded by
    `inventory-and-registry` and in `nfr-design/security-design.md`'s banner).

    Raises
    ------
    EvidenceScanError
        when a candidate file cannot be read or decoded.
    """
    root = Path(evidence_root).resolve()
    if not root.is_dir():
        return []
    restricted = (root / "locked_test_restricted").resolve()

    offenders: list[Path] = []
    for candidate in sorted(root.rglob("*.json")):
        if candidate.is_relative_to(restricted):
            continue
        try:
            text = candidate.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            fail_unparseable(candidate, str(exc))
            raise AssertionError("unreachable: fail_unparseable always raises") from exc
        if '"2022-12' in text or "'2022-12" in text:
            offenders.append(candidate)
    return offenders
