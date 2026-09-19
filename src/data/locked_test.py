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
import fnmatch
import hashlib
import json
import os
import re
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
    "DECEMBER_DRIVER_EXCLUSION_CLASSES",
    "TARGET_INDICATOR_KEYS",
    "december_driver_exclusion_class",
    "DecemberCustodyEntry",
    "december_custody_inventory",
]

RESTRICTED_ROOT: Final[str] = "evidence/locked_test_restricted"

#: R-26's ENUMERATED driver-exclusion classes (governance-guards business-rules R-26,
#: "the four excluded driver classes, enumerated exhaustively", 2026-08-28; class 4
#: unconditional since D-30), implemented 2026-09-19 (G-4, `CR-2026-09-19-GATE-PREP-2`),
#: PLUS class 5 adopted by the project decision owner as **D-48** (2026-09-19,
#: `CR-2026-09-19-SCI-DECISIONS`): raw external-driver captures and their source-version
#: audit summary under `evidence/audit_gfz_*/`, with documented provenance. Membership is an
#: exact (class, label, evidence-relative path patterns) list, never a directory
#: predicate, and the path match is only HALF of eligibility: the file's CONTENT must
#: validate as that class's driver-only schema (`_class_content_ok`), and class 5 must
#: also carry a provenance record. Mixed or unclassifiable content fails closed. A
#: custody exclusion is never a licence to use; excluded files stay inventoried with
#: their reason (`december_custody_inventory`).
DECEMBER_DRIVER_EXCLUSION_CLASSES: Final[tuple[tuple[int, str, tuple[str, ...]], ...]] = (
    (
        1,
        "Raw provisional-Dst monthly capture",
        ("audit_ec1_2026-08-15/kyoto_dst/dst_provisional_*.html",),
    ),
    (2, "Raw F10.7 flux table", ("audit_ec1_2026-08-15/nrcan_f107/fluxtable.txt",)),
    (3, "Derived driver audit report", ("audit_ec1_2026-08-15/ec1-audit-report.json",)),
    (4, "Derived driver summary", ("audit_ec1_2026-08-15/kyoto_dst/.dst_summary.json",)),
    (
        5,
        "Raw GFZ geomagnetic-index capture or source-version audit summary (D-48)",
        (
            "audit_gfz_*/Kp_*.wdc",
            "audit_gfz_*/hp60ap60doi_*.txt",
            "audit_gfz_*/gfz-comparison-report.json",
        ),
    ),
)

#: Key tokens whose presence anywhere in a JSON artifact marks TARGET, PREDICTION,
#: EVALUATION or mixed content — such a file is NEVER excluded, whatever its path. Token
#: match is on the lower-cased key split at `_`/`-`, so `december_days_present`,
#: `vtec_tecu`, `y_hat`, `paired_error` all hit. Widening this set is a reviewed edit.
TARGET_INDICATOR_KEYS: Final[frozenset[str]] = frozenset(
    {
        "vtec",
        "tec",
        "tecu",
        "target",
        "y",
        "yhat",
        "prediction",
        "predictions",
        "forecast",
        "metric",
        "metrics",
        "rmse",
        "mae",
        "mse",
        "loss",
        "paired",
        "estimand",
        "residual",
        "residuals",
        "coverage",
        "madrigal",
        "station",
        "stations",
        "cell",
        "cells",
        "aruc",
        "bshm",
        "nico",
        "mask",
        "fold",
        "model",
    }
)

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
        record = replace(record, mask_bundle_ids=bundle_ids, mask_registry_hash=registry_hash)

    try:
        _append_and_flush(Path(registry), record)
    except OSError as exc:
        raise LockedTestError(
            registry,
            f"access-log write failed ({exc}); the read is aborted rather than performed "
            f"unlogged -- FR-P1-02-3 requires the record to be durable BEFORE the read",
        ) from exc

    return resolved


def write_restricted(path: Path, payload: bytes, *, record: AccessRecord, registry: Path) -> Path:
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


def _key_tokens(obj: object, acc: set[str]) -> set[str]:
    if isinstance(obj, dict):
        for key, value in obj.items():
            for token in str(key).lower().replace("-", "_").split("_"):
                if token:
                    acc.add(token)
            _key_tokens(value, acc)
    elif isinstance(obj, list):
        for value in obj:
            _key_tokens(value, acc)
    return acc


# --- December detection: STRUCTURAL, per format (D-48; P-4a) ------------------------------

#: December 2022 as a unix-epoch range [start, end) — isprint extractions and the Madrigal
#: record CSVs carry `ut1_unix`, not a calendar string.
_DECEMBER_2022_UNIX: Final[tuple[int, int]] = (1669852800, 1672531200)
_DEC_TEXT = re.compile(r"2022-12|202212")
_DEC_WDC_LINE = re.compile(r"^2212[ \d]\d", re.M)
_DEC_HPO_LINE = re.compile(r"^2022 12 \d\d", re.M)
_MONTH_KEYS: Final[frozenset[str]] = frozenset(str(m) for m in range(1, 13))
_DETECT_STRING_FIELDS: Final[frozenset[str]] = frozenset({"y", "year", "m", "month"})


def _json_december(obj: object) -> str | None:
    """Why a parsed JSON payload is December-bearing, or None. Structural: (a) any string
    (key or value) carrying `2022-12` / `202212`; (b) any record with year 2022 and month
    12 under `y`/`year` and `m`/`month` (integer or string), at any depth; (c) a mapping
    keyed by month numbers that carries `"12"` (a per-month summary)."""
    if isinstance(obj, dict):
        keys = {str(k) for k in obj}
        if "12" in keys and len(keys) >= 2 and keys <= _MONTH_KEYS:
            return "month-number key '12' in a per-month mapping"
        year = None
        month = None
        for key, value in obj.items():
            skey = str(key).lower()
            if _DEC_TEXT.search(str(key)):
                return f"key {key!r} carries a December-2022 literal"
            if skey in ("y", "year"):
                year = value
            elif skey in ("m", "month"):
                month = value
        if str(year) == "2022" and str(month) == "12":
            return "record with year 2022 and month 12"
        for value in obj.values():
            found = _json_december(value)
            if found:
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = _json_december(value)
            if found:
                return found
    elif isinstance(obj, str) and _DEC_TEXT.search(obj):
        return "string value carries a December-2022 literal"
    return None


def _endpoint_epochs(candidate: Path) -> tuple[float, float] | None:
    """First and last leading numeric field of a large whitespace table (isprint output),
    read from the file's two ends only — an O(1) endpoint inspection, disclosed as such."""
    size = candidate.stat().st_size
    if size == 0:
        return None
    with candidate.open("rb") as handle:
        head = handle.read(min(size, 4096)).decode("utf-8", errors="replace")
        handle.seek(max(0, size - 4096))
        tail = handle.read().decode("utf-8", errors="replace")
    first = next((ln for ln in head.splitlines() if ln.strip()), "")
    last = next((ln for ln in reversed(tail.splitlines()) if ln.strip()), "")
    try:
        return float(first.split()[0]), float(last.split()[0])
    except (ValueError, IndexError):
        return None


def _detect_december(candidate: Path, text: str | None) -> tuple[str, str | None]:
    """(detection method, reason-or-None) for one file, by format."""
    suffix = candidate.suffix.lower()
    name = candidate.name
    if suffix == ".json":
        payload = json.loads(text if text is not None else candidate.read_text(encoding="utf-8"))
        return "json-structural", _json_december(payload)
    if suffix == ".wdc":
        body = text if text is not None else candidate.read_text(encoding="utf-8")
        hits = _DEC_WDC_LINE.findall(body)
        return "wdc-line", (f"{len(hits)} December-2022 day line(s)" if hits else None)
    if name.startswith("hp60ap60doi") or name.startswith("Hp60ap60doi"):
        body = text if text is not None else candidate.read_text(encoding="utf-8")
        hits = _DEC_HPO_LINE.findall(body)
        return "hpo-line", (f"{len(hits)} December-2022 hourly line(s)" if hits else None)
    if candidate.parent.name == "raw_isprint_cache":
        ends = _endpoint_epochs(candidate)
        if ends is None:
            fail_unparseable(candidate, "no leading numeric field at either end")
        lo, hi = _DECEMBER_2022_UNIX
        first, last = ends  # type: ignore[misc]
        spans = first < hi and last >= lo
        return "isprint-endpoint", (
            f"record epochs {first:.0f}..{last:.0f} overlap December 2022" if spans else None
        )
    if suffix == ".md":
        return "outside-automated-inspection", None
    body = text if text is not None else candidate.read_text(encoding="utf-8")
    hits = _DEC_TEXT.findall(body)
    if not hits and suffix == ".csv" and "ut1_unix" in body[:400]:
        lo, hi = _DECEMBER_2022_UNIX
        for line in body.splitlines()[1:]:
            field = line.split(",", 1)[0]
            try:
                epoch = float(field)
            except ValueError:
                continue
            if lo <= epoch < hi:
                return "csv-epoch", f"ut1_unix {epoch:.0f} in December 2022"
    return "text-literal", (f"{len(hits)} December-2022 literal(s)" if hits else None)


# --- exclusion classes: content validators ------------------------------------------------

_FLUX_LINE = re.compile(r"^\d{8}\s+\d{6}\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s*$")
_WDC_LINE = re.compile(r"^[0-9 .+\-]{62,}$")
_TARGET_WORDS = re.compile(r"\b(vtec|tecu|madrigal|aruc|bshm|nico|prediction|rmse)\b", re.I)


def _lines(text: str, *, comment: str = "#") -> list[str]:
    return [ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith(comment)]


def _driver_only_json(text: str) -> bool:
    return not (_key_tokens(json.loads(text), set()) & TARGET_INDICATOR_KEYS)


def _gfz_provenance(candidate: Path, text: str) -> bool:
    """D-48's provenance condition: a sibling `retrieval_record.json` documents the file —
    for a raw capture, a `provider_files` entry with this on-disk name and a sha256 equal
    to the file's bytes; for the comparison report, the same `run_id`."""
    record_path = candidate.with_name("retrieval_record.json")
    if not record_path.is_file():
        return False
    record = json.loads(record_path.read_text(encoding="utf-8"))
    if candidate.name == "gfz-comparison-report.json":
        return bool(record.get("run_id")) and json.loads(text).get("run_id") == record.get(
            "run_id"
        )
    for entry in record.get("provider_files", []):
        if entry.get("logical_name") == candidate.name:
            digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
            return entry.get("sha256") == digest
    return False


_GFZ_REPORT_KEYS: Final[frozenset[str]] = frozenset(
    {"comparisons", "december_custody", "provider_limitations", "run_id", "validation"}
)
_EPOCH_KEYS: Final[frozenset[str]] = frozenset({"y", "m", "d", "h"})


def _gfz_report_ok(payload: object) -> bool:
    """Schema-validated driver-only content for the GFZ source-version audit summary
    (D-48). Two `TARGET_INDICATOR_KEYS` tokens occur in this report with a non-target
    meaning and are admitted ONLY in their validated structural position: `y` as the
    year of an epoch key `{y, m, d, h}` (integer values, no other sibling), and
    `coverage` as the epoch-count statement under `validation.<file>`. Any other target
    token anywhere, any other top-level key, or either token elsewhere fails closed."""
    if not isinstance(payload, dict) or not set(payload) <= _GFZ_REPORT_KEYS:
        return False

    def walk(obj: object, path: tuple[str, ...]) -> bool:
        if isinstance(obj, dict):
            keys = {str(k) for k in obj}
            if "y" in keys:
                if not keys <= _EPOCH_KEYS or not all(
                    isinstance(v, int) and not isinstance(v, bool) for v in obj.values()
                ):
                    return False
                return True
            for key, value in obj.items():
                tokens = {tok for tok in str(key).lower().replace("-", "_").split("_") if tok}
                if "coverage" in tokens:
                    if not (len(path) == 2 and path[0] == "validation"):
                        return False
                    tokens.discard("coverage")
                if tokens & TARGET_INDICATOR_KEYS:
                    return False
                if not walk(value, (*path, str(key))):
                    return False
            return True
        if isinstance(obj, list):
            return all(walk(v, path) for v in obj)
        return True

    return walk(payload, ())


def _class_content_ok(number: int, candidate: Path, text: str) -> bool:
    """The CONTENT half of eligibility per class — validated schema, never a path alone.
    Anything unexpected returns False (fail closed for review)."""
    if number == 1:
        return "dst" in text.lower() and not _TARGET_WORDS.search(text)
    if number == 2:
        body = [ln for ln in text.splitlines() if ln.strip()]
        data = [ln for ln in body if not ln.lstrip().startswith(("fluxdate", "---"))]
        return bool(data) and all(_FLUX_LINE.match(ln) for ln in data)
    if number in (3, 4):
        return _driver_only_json(text)
    if number == 5:
        if candidate.suffix.lower() == ".wdc":
            data = _lines(text)
            ok = bool(data) and all(_WDC_LINE.match(ln) for ln in data)
        elif candidate.suffix.lower() == ".txt":
            data = _lines(text)
            ok = bool(data) and all(
                len(ln.split()) == 10 and all(_numeric(tok) for tok in ln.split()) for ln in data
            )
        elif candidate.name == "gfz-comparison-report.json":
            ok = _gfz_report_ok(json.loads(text))
        else:
            return False
        return ok and _gfz_provenance(candidate, text)
    return False


def _numeric(token: str) -> bool:
    try:
        float(token)
    except ValueError:
        return False
    return True


def december_driver_exclusion_class(
    candidate: Path, evidence_root: Path, *, text: str | None = None
) -> tuple[int, str] | None:
    """The R-26/D-48 driver-exclusion class `candidate` belongs to, or None when it is
    subject to the December custody scan.

    Eligibility is TWO conditions, both required: (a) the evidence-relative path matches
    one of the enumerated class patterns exactly (`fnmatch`, no directory predicate); and
    (b) the file's CONTENT validates as that class's driver-only schema
    (`_class_content_ok`) — for JSON, no key token in `TARGET_INDICATOR_KEYS` at any
    depth; for raw captures, every data line parses as the provider's format; for class 5
    additionally a documented provenance record (D-48). Mixed, unknown or unclassifiable
    content returns None — flagged for review, never excluded. An unparseable JSON is not
    "excluded": the caller's unparseable-file failure stands.
    """
    try:
        rel = candidate.resolve().relative_to(Path(evidence_root).resolve()).as_posix()
    except ValueError:
        return None
    for number, label, patterns in DECEMBER_DRIVER_EXCLUSION_CLASSES:
        if not any(fnmatch.fnmatch(rel, pattern) for pattern in patterns):
            continue
        body = text if text is not None else candidate.read_text(encoding="utf-8")
        if _class_content_ok(number, candidate, body):
            return number, label
        return None  # path matched, content did not: fail closed
    return None


@dataclass(frozen=True)
class DecemberCustodyEntry:
    """One inventory row of the custody scan: WHAT was inspected, HOW, and its disposition.
    `disposition` is one of `flagged` (December-bearing, no exclusion applies — an
    offender), `excluded` (December-bearing, class content validated — inventoried with
    its reason; exposure, never a licence to use), `no_december_content`, or
    `outside_automated_inspection` (governance prose; handled by review, never labelled
    clean)."""

    path: str
    detection: str
    disposition: str
    exclusion_class: int | None
    reason: str


def _read_text(candidate: Path) -> str:
    """UTF-8, else — for NON-JSON text formats only — Latin-1, which decodes every byte
    and leaves the ASCII date patterns intact (a provider HTML page in a legacy encoding
    is readable for detection, not "unreadable"). JSON must be UTF-8 (R-27: failure)."""
    raw = candidate.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        if candidate.suffix.lower() == ".json":
            raise
        return raw.decode("latin-1")


def december_custody_inventory(evidence_root: Path) -> list[DecemberCustodyEntry]:
    """FR-P1-02-6 / R-27: walk `evidence/` recursively and inventory EVERY file outside the
    restricted root with its December detection method and disposition. Scanner
    COVERAGE (which formats are inspected how) is reported by `detection`, separately
    from policy COMPLIANCE (`disposition`): an inspection method that reads only a file's
    endpoints says so, and a format no method reads is `outside_automated_inspection`.

    Detection is structural per format (D-48, P-4a): JSON by parsed structure (string
    literals, `{y: 2022, m: 12}` records at any depth, month-number keys), WDC and Hpo
    lines by their own date layout, isprint tables by endpoint epochs, Madrigal CSVs by
    `ut1_unix` epochs or literals, other text by literal. Membership is decided by record
    content, never by directory name (`project.md` § Forbidden).

    Raises
    ------
    EvidenceScanError
        when a candidate cannot be read or decoded (R-27: unreadable is a failure).
    """
    root = Path(evidence_root).resolve()
    if not root.is_dir():
        return []
    restricted = (root / "locked_test_restricted").resolve()
    rows: list[DecemberCustodyEntry] = []
    for candidate in sorted(p for p in root.rglob("*") if p.is_file()):
        if candidate.is_relative_to(restricted):
            continue
        rel = candidate.relative_to(root).as_posix()
        text: str | None = None
        try:
            if candidate.parent.name != "raw_isprint_cache":
                text = _read_text(candidate)
            detection, reason = _detect_december(candidate, text)
        except EvidenceScanError:
            raise
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            fail_unparseable(candidate, str(exc))
            raise AssertionError("unreachable: fail_unparseable always raises") from exc
        if detection == "outside-automated-inspection":
            rows.append(
                DecemberCustodyEntry(
                    rel,
                    detection,
                    "outside_automated_inspection",
                    None,
                    "governance prose; reviewed by a person, never labelled clean",
                )
            )
            continue
        if reason is None:
            rows.append(DecemberCustodyEntry(rel, detection, "no_december_content", None, ""))
            continue
        try:
            excluded = december_driver_exclusion_class(candidate, root, text=text)
        except ValueError as exc:
            fail_unparseable(candidate, str(exc))
            raise AssertionError("unreachable: fail_unparseable always raises") from exc
        if excluded is None:
            rows.append(DecemberCustodyEntry(rel, detection, "flagged", None, reason))
        else:
            rows.append(
                DecemberCustodyEntry(
                    rel,
                    detection,
                    "excluded",
                    excluded[0],
                    f"{reason}; class {excluded[0]} ({excluded[1]}) — content validated; exposure recorded",
                )
            )
    return rows


def assert_no_december_outside_restricted(evidence_root: Path) -> Sequence[Path]:
    """FR-P1-02-6's regression guard: December-bearing artifacts outside the restricted root.

    Returns every `flagged` entry of `december_custody_inventory` as a path; an empty
    sequence is the pass condition. Recursive by construction (`DATA-01`); membership by
    record content, never by directory name; unreadable is a failure (R-27). The
    inventory itself — including the `excluded` files with their reasons and the formats
    outside automated inspection — is the coverage record a reviewer reads beside the
    pass/fail result.

    Raises
    ------
    EvidenceScanError
        when a candidate file cannot be read or decoded.
    """
    root = Path(evidence_root).resolve()
    return [
        root / entry.path
        for entry in december_custody_inventory(root)
        if entry.disposition == "flagged"
    ]
