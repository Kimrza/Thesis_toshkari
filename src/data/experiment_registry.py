"""C-2 Registry writer: TE 13.4's twenty-column append-only experiment registry.

Purpose
-------
The permanent record (`logical-components.md` C-2). One JSONL line per run event in
`experiment_registry.jsonl`, which is authoritative; the CSV is derived, hashed and
marked derived. Implements W-6's eight steps and rules R-07 (closed status vocabulary),
R-08 (writes never read the run history; single append-mode write plus durability
confirmation; torn-write distinction), R-09 (failed/aborted runs stay visible), R-10
(report honestly even when reporting fails), R-18 (write-time twenty-column schema
assertion; `prediction_hash` writer refusal; Phase 1 `prior_period_exposure` refusal),
R-19 (`AccessRecord`/`RegistryEvent` join on `run_id`, orphan detection both ways,
known pre-guard orphans reported and never back-filled) and R-20 (`exploratory` DERIVED
in the writer, never caller-passed, with the G-06 carve-out keyed to
`purpose = locked_evaluation` on the run's own `AccessRecord`).

This module was created as a NEW file under the TE 12 naming amendment reported at the
code-generation governance stop (Q1=A, receipted): TE 12's tree does not enumerate it,
and `src/data/registry.py` is NOT this module — that path belongs to
`inventory-and-registry` and holds station metadata.

Inputs
------
* `registry_path` — the JSONL registry file (created on first append).
* `access_log_path` — the restricted-access log `governance-guards`' chokepoint writes
  (`AccessRecord` JSONL). Read at write time ONLY for the `exploratory` derivation
  (R-20); the reconciliation of R-19 runs with the integrity test, never on the write
  path. This module never constructs a path into the restricted December evidence
  root (R-15) — it reads the access log, not the restricted root, and does not even
  name that root's path.
* the row payload — TE 13.4's twenty columns plus the named extension fields.

Re-run behaviour
----------------
Append-only and idempotence-free BY DESIGN: every call appends exactly one new
newline-terminated record under append mode and never reads, rewrites, deletes or
reorders prior rows (R-08). Re-running a stage appends new rows; the earlier rows —
including failed and aborted ones — stay visible with status and reason (R-09,
NFR-AUD-01). No entry is ever deleted, overwritten or silently re-run. The integrity
check and the reconciliation are pure reads.

Durability
----------
Every append is followed by flush + fsync before the writer returns; a durability
failure raises `RegistryError` naming the file and the violated expectation — never a
warning beside a write reported as successful (W-6 step 8; `governance-guards` R-25's
accepted pattern). Platform durability semantics are characterised NOWHERE yet, so
every row carries a durability stamp reading unverified-on-this-platform (SD-03,
Q3=B); the freeze gate refuses a so-stamped row as evidence, and the measurement is
owed on Bolt 1's in-Kaggle work.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final

from src.data.config import (
    CHARACTERISED_DURABILITY_PLATFORMS,
    RegistryError,
)

__all__ = [
    "REGISTRY_COLUMNS",
    "EXTENSION_FIELDS",
    "STATUSES",
    "TERMINAL_STATUSES",
    "FORBIDDEN_PREDICTION_HASH_WRITERS",
    "append_registry_event",
    "record_abort_honestly",
    "check_registry_integrity",
    "reconcile_access_records",
    "derive_csv",
    "IntegrityReport",
    "ReconciliationReport",
]

#: TE 13.4's twenty columns, in order, `run_id` FIRST — deliberately, so a torn final
#: record's owning run is recoverable from the legible prefix (R-08).
REGISTRY_COLUMNS: Final[tuple[str, ...]] = (
    "run_id",
    "started_at_utc",
    "completed_at_utc",
    "status",
    "code_commit",
    "environment_lock_hash",
    "platform",
    "dataset_version",
    "fold_id",
    "mask_id",
    "feature_set_id",
    "model_id",
    "hyperparameters_json",
    "seed",
    "validation_metric_name",
    "validation_metric_value",
    "artifact_manifest_path",
    "prediction_hash",
    "locked_test_accessed",
    "notes",
)

#: The named extension fields (R-18: TE 13.4 reads "including:", so the twenty are a
#: floor and these are named as extensions rather than smuggled into the twenty).
#: `durability` carries SD-03's stamp (Q3=B) and `exploratory_carveout` records R-20's
#: G-06 carve-out ON THE ROW, as the rule requires — `notes` is free text and must not
#: be repurposed to carry a structured fact.
EXTENSION_FIELDS: Final[tuple[str, ...]] = (
    "reason",
    "prior_period_exposure",
    "exploratory",
    "exploratory_carveout",
    "durability",
)

#: R-07: the closed status vocabulary. `aborted` is an intentional or
#: preflight-triggered stop; `failed` is an execution failure. Not interchangeable.
STATUSES: Final[frozenset[str]] = frozenset({"started", "completed", "aborted", "failed"})
TERMINAL_STATUSES: Final[frozenset[str]] = frozenset({"completed", "aborted", "failed"})

#: R-18 limb 2: the registry writer REFUSES a `prediction_hash` presented by the
#: process that computes a metric over that prediction. `06_train_and_predict` writes
#: the receipt; `07_evaluate_and_report` and the bootstrap may not. Writer and reader
#: stay in different processes — the only thing that makes "the receipt precedes the
#: metric" mean anything.
FORBIDDEN_PREDICTION_HASH_WRITERS: Final[frozenset[str]] = frozenset({"evaluate", "bootstrap"})

_MAX_TIMESTAMP: Final[str] = "~"  # sorts after every ISO-8601 timestamp


def _validate_row(
    registry_path: Path,
    row: Mapping[str, Any],
    *,
    phase: int,
    writer_role: str,
) -> None:
    """W-6 steps 1-5: every write-time check that needs NO read of prior rows (R-08)."""
    status = row.get("status")
    if status not in STATUSES:
        raise RegistryError(
            registry_path,
            f"unknown status {status!r}; the vocabulary is closed and validated at "
            f"write time (R-07): started | completed | aborted | failed — an unknown "
            f"status is a failure, not a new category",
        )

    if status in ("aborted", "failed"):
        reason = row.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            raise RegistryError(
                registry_path,
                f"status {status!r} requires a non-empty reason (R-07; NFR-AUD-01: "
                f"failed and aborted runs remain visible with status AND reason)",
            )

    missing = [column for column in REGISTRY_COLUMNS if column not in row]
    if missing:
        raise RegistryError(
            registry_path,
            "TE 13.4 twenty-column schema violated at write time (R-18); absent "
            "column(s): " + ", ".join(missing),
        )

    for populated in ("code_commit", "environment_lock_hash"):
        value = row.get(populated)
        if not isinstance(value, str) or not value.strip():
            raise RegistryError(
                registry_path,
                f"column {populated!r} must be POPULATED on every row, not merely "
                f"present (R-18; FR-P1-05-13's second criterion)",
            )

    if row.get("prediction_hash") and writer_role in FORBIDDEN_PREDICTION_HASH_WRITERS:
        raise RegistryError(
            registry_path,
            f"a prediction_hash may not be written by writer_role {writer_role!r} "
            f"(R-18 limb 2): the process that computes a metric over a prediction may "
            f"not write its receipt — that repair would make 'the receipt precedes the "
            f"metric' self-certifying",
        )

    if phase == 1 and bool(row.get("prior_period_exposure")):
        raise RegistryError(
            registry_path,
            "prior_period_exposure = true is rejected on a Phase 1 row (R-18): Phase 1 "
            "IS the first December exposure; true belongs to the Phase 2 replication "
            "(TE 7.0B)",
        )

    if "exploratory" in row or "exploratory_carveout" in row or "durability" in row:
        raise RegistryError(
            registry_path,
            "exploratory (and its carve-out and the durability stamp) is DERIVED in "
            "the registry writer and never passed by a caller (R-20): a caller that "
            "could set it could suppress it, which is the act the flag exists to "
            "prevent",
        )


def _read_access_records(access_log_path: Path) -> list[Mapping[str, Any]]:
    """Parse the restricted-access log. A missing log means no access has occurred."""
    path = Path(access_log_path)
    if not path.is_file():
        return []
    records: list[Mapping[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            # The access log is governance-guards' artifact; an unparseable line there
            # is ITS integrity problem, surfaced by its own tests. For the derivation we
            # are conservative and skip nothing silently: an unreadable record cannot
            # prove the access happened later, so it is treated as earliest-possible.
            records.append({"_unparseable": line})
            continue
        if isinstance(parsed, dict):
            records.append(parsed)
    return records


def _access_timestamp(record: Mapping[str, Any]) -> str:
    """The record's best timestamp, conservatively early when unparseable.

    `retrieved_at_utc` is preferred; the observed log carries a placeholder string
    there, in which case `logged_at_utc` is used. A record with neither, or with a
    non-ISO value in both, sorts as EARLIEST (empty string) — the conservative
    direction: it can only make later runs exploratory, never hide an exposure.
    """
    for key in ("retrieved_at_utc", "logged_at_utc"):
        value = record.get(key)
        if isinstance(value, str) and len(value) >= 10 and value[:4].isdigit():
            return value
    return ""


def _derive_exploratory(
    row: Mapping[str, Any], access_records: Sequence[Mapping[str, Any]]
) -> tuple[bool, str]:
    """R-20: derive `exploratory` from `started_at_utc` against the access log.

    `true` when the run's `started_at_utc` postdates the earliest `AccessRecord` under
    the restricted root; `false` otherwise. The G-06 carve-out applies IFF the run's
    OWN `AccessRecord` carries `purpose = locked_evaluation` — a field the guard sets
    structurally, not by caller choice — and is recorded on the row, never left unset.
    The pre-G-05 coverage audit legitimately starts the clock (`purpose =
    coverage_audit` records are counted): the trigger is December being SEEN, not the
    locked test being opened (project.md Forbidden).
    """
    if not access_records:
        return False, ""

    earliest = min(_access_timestamp(record) for record in access_records)
    started = str(row.get("started_at_utc", ""))
    postdates = started > earliest

    if not postdates:
        return False, ""

    run_id = row.get("run_id")
    own_locked_evaluation = any(
        record.get("run_id") == run_id and record.get("purpose") == "locked_evaluation"
        for record in access_records
    )
    if own_locked_evaluation:
        return False, (
            "G-06 carve-out (R-20): this run's own AccessRecord carries "
            "purpose = locked_evaluation; the locked evaluation is not exploratory"
        )
    return True, ""


def append_registry_event(
    registry_path: Path,
    row: Mapping[str, Any],
    *,
    phase: int,
    writer_role: str,
    access_log_path: Path,
) -> dict[str, Any]:
    """W-6: validate, derive, append ONE newline-terminated record, confirm durability.

    Never reads the run history (R-08): every validation above is write-time-only, the
    `exploratory` derivation reads the ACCESS LOG (a different artifact), and the
    append is a single `os.write` under `O_APPEND`. The status transition graph is
    enforced by `check_registry_integrity`, never here — a log whose write path depends
    on reading is no longer a pure append.

    Parameters
    ----------
    writer_role
        The calling process's declared role (e.g. ``"stage"``, ``"train"``,
        ``"evaluate"``, ``"bootstrap"``). Rows carrying a `prediction_hash` are REFUSED
        for the metric-computing roles (R-18 limb 2).

    Returns the record as written (twenty columns plus extensions).

    Raises
    ------
    RegistryError
        unknown status; empty reason on aborted|failed; a missing or unpopulated 13.4
        column; a forbidden `prediction_hash` writer; `prior_period_exposure = true` on
        a Phase 1 row; caller-passed `exploratory`; or a durability failure on the
        append — named with the file and the violated expectation, never a warning
        beside a write reported as successful (R-10 reaching the durability layer).
    """
    registry_path = Path(registry_path)
    _validate_row(registry_path, row, phase=phase, writer_role=writer_role)

    access_records = _read_access_records(Path(access_log_path))
    exploratory, carveout = _derive_exploratory(row, access_records)

    platform = str(row.get("platform", ""))
    if platform in CHARACTERISED_DURABILITY_PLATFORMS:  # pragma: no cover - set is empty
        durability = f"measured on platform {platform!r}"
    else:
        durability = (
            f"unverified on this platform ({platform or 'unknown'}); fsync was "
            f"confirmed but the platform's durability semantics are uncharacterised "
            f"(SD-03, Q3=B) — a freeze gate refuses a so-stamped row as evidence"
        )

    record: dict[str, Any] = {column: row[column] for column in REGISTRY_COLUMNS}
    record["reason"] = row.get("reason", "")
    record["prior_period_exposure"] = bool(row.get("prior_period_exposure", False))
    record["exploratory"] = exploratory
    record["exploratory_carveout"] = carveout
    record["durability"] = durability

    # run_id first (R-08: recoverable from a torn prefix), then the remaining columns in
    # schema order, then the extensions — a stable, documented field order.
    ordered = {key: record[key] for key in (*REGISTRY_COLUMNS, *EXTENSION_FIELDS)}
    encoded = (json.dumps(ordered, ensure_ascii=False, separators=(", ", ": ")) + "\n").encode(
        "utf-8"
    )

    registry_path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(registry_path, os.O_APPEND | os.O_CREAT | os.O_WRONLY)
    try:
        written = os.write(fd, encoded)  # ONE single write of ONE record (R-08)
        if written != len(encoded):
            raise RegistryError(
                registry_path,
                f"append wrote {written} of {len(encoded)} bytes; the row is not "
                f"durably recorded and this is reported as the failure it is",
            )
        try:
            os.fsync(fd)  # durability confirmation BEFORE returning (W-6 step 8)
        except OSError as exc:
            raise RegistryError(
                registry_path,
                f"durability confirmation (fsync) failed ({exc}); the append is not "
                f"confirmed durable and is never reported as successful (R-10)",
            ) from exc
    finally:
        os.close(fd)

    return ordered


def record_abort_honestly(
    registry_path: Path,
    row: Mapping[str, Any],
    *,
    phase: int,
    writer_role: str,
    access_log_path: Path,
    original_error: BaseException,
) -> bool:
    """R-10: attempt the `aborted` row; if THAT fails, report both and claim nothing.

    Returns ``True`` when the aborted record was durably appended, ``False`` when the
    registry write itself failed — in which case the ORIGINAL exception is preserved
    (re-raise it at the call site), BOTH failures are reported to stderr, and no claim
    is made that an aborted record was written. A handler that swallows its own write
    failure produces a run that failed, was not recorded, and reported that it had been
    recorded — the worst possible artifact.
    """
    try:
        append_registry_event(
            registry_path,
            row,
            phase=phase,
            writer_role=writer_role,
            access_log_path=access_log_path,
        )
        return True
    except Exception as registry_error:  # noqa: BLE001 - R-10 requires reporting, not masking
        print(f"ORIGINAL FAILURE (preserved): {original_error}", file=sys.stderr)
        print(
            f"REGISTRY WRITE FAILURE (the aborted record was NOT written): "
            f"{registry_error}",
            file=sys.stderr,
        )
        return False


# --- the registry-integrity test (R-08, R-09): a pure read, never on the write path ----


@dataclass(frozen=True)
class IntegrityReport:
    """What `check_registry_integrity` found. Violations empty means the log is legal."""

    rows: int
    violations: Sequence[str]
    torn_final_run_id: str | None = None
    torn_final_reported: str | None = None


def check_registry_integrity(registry_path: Path) -> IntegrityReport:
    """Enforce the status transition graph and the torn-write distinction (R-08).

    Legal transitions per `run_id`: started -> completed | aborted | failed. Rejected:
    duplicate `started`, repeated terminals, transitions out of a terminal, unknown or
    malformed rows. Position decides a malformed row's meaning: an unterminated or
    truncated FINAL line is a torn write — REPORTED with the `run_id` recovered from
    its legible prefix, the run staying visible (NFR-AUD-01) — while any INTERIOR
    malformed line, or a newline-terminated trailing line that is still unparseable, is
    a violation. Runs when the reconciliation runs: before TA-10 / G-09 acceptance and
    before registry contents are relied on as audit evidence.
    """
    path = Path(registry_path)
    violations: list[str] = []
    torn_run_id: str | None = None
    torn_reported: str | None = None

    if not path.is_file():
        return IntegrityReport(rows=0, violations=[f"{path}: registry file is absent"])

    raw = path.read_bytes()
    if not raw:
        return IntegrityReport(rows=0, violations=[])

    body, sep, tail = raw.rpartition(b"\n")
    complete_lines = [ln for ln in body.split(b"\n") if ln.strip()] if sep else []
    if not sep:
        # No newline anywhere: the whole file is one torn (or first, interrupted) write.
        tail_bytes = raw
    else:
        tail_bytes = tail

    if tail_bytes.strip():
        # An unterminated FINAL line: a torn write, not corruption (R-08).
        text = tail_bytes.decode("utf-8", errors="replace")
        run_id = None
        marker = '"run_id": "'
        alt_marker = '"run_id":"'
        for m in (marker, alt_marker):
            start = text.find(m)
            if start != -1:
                rest = text[start + len(m):]
                run_id = rest.split('"', 1)[0] if '"' in rest else rest
                break
        torn_run_id = run_id
        torn_reported = (
            f"{path}: torn final record (unterminated append) belonging to run "
            f"{run_id!r}; the run STAYS VISIBLE and the record is reported, not "
            f"rejected — an aborted row is written while the process is dying, which "
            f"is exactly when a non-atomic append tears"
        )

    parsed_rows: list[Mapping[str, Any]] = []
    for index, line in enumerate(complete_lines):
        try:
            parsed = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            violations.append(
                f"{path}: line {index + 1} is malformed and newline-terminated — "
                f"corruption or an illegal row, rejected (R-08)"
            )
            continue
        if not isinstance(parsed, dict):
            violations.append(f"{path}: line {index + 1} is not a JSON object; rejected")
            continue
        parsed_rows.append(parsed)

    by_run: dict[str, list[Mapping[str, Any]]] = {}
    for parsed in parsed_rows:
        by_run.setdefault(str(parsed.get("run_id")), []).append(parsed)

    for run_id, events in by_run.items():
        started = [e for e in events if e.get("status") == "started"]
        terminals = [e for e in events if e.get("status") in TERMINAL_STATUSES]
        unknown = [e for e in events if e.get("status") not in STATUSES]
        for event in unknown:
            violations.append(
                f"{path}: run {run_id!r} carries unknown status "
                f"{event.get('status')!r} (R-07)"
            )
        if len(started) > 1:
            violations.append(f"{path}: run {run_id!r} has duplicate started rows")
        if len(terminals) > 1:
            violations.append(
                f"{path}: run {run_id!r} has repeated terminal statuses "
                f"({[e.get('status') for e in terminals]})"
            )
        # A transition OUT of a terminal: any event ordered after a terminal event.
        saw_terminal = False
        for event in events:  # file order is event order within one log
            if saw_terminal:
                violations.append(
                    f"{path}: run {run_id!r} has an event after a terminal status — "
                    f"transitions out of a terminal are rejected"
                )
                break
            if event.get("status") in TERMINAL_STATUSES:
                saw_terminal = True
        if not started and terminals:
            violations.append(
                f"{path}: run {run_id!r} has a terminal row with no started row"
            )

    return IntegrityReport(
        rows=len(parsed_rows),
        violations=violations,
        torn_final_run_id=torn_run_id,
        torn_final_reported=torn_reported,
    )


# --- R-19: the AccessRecord/RegistryEvent reconciliation --------------------------------


@dataclass(frozen=True)
class ReconciliationReport:
    """R-19's output. Expected orphans are REPORTED with their reason, never cleared."""

    registry_rows: int
    access_rows: int
    expected_orphans: Mapping[str, str] = field(default_factory=dict)


def reconcile_access_records(
    registry_path: Path,
    access_log_path: Path,
    *,
    known_orphans: Mapping[str, str] | None = None,
) -> ReconciliationReport:
    """R-19: join `AccessRecord` and `RegistryEvent` on `run_id`, orphans both ways.

    A restricted access with no registry row, and a registry row claiming
    `locked_test_accessed = true` with no logged access, are each an integrity
    violation. `known_orphans` maps `run_id` -> reason for the KNOWN pre-guard rows
    (the five retrospective accesses `evidence/experiment_registry.md` rows 3, 4, 5, 8
    and 9 record, plus Recommendation 31's expressly unresolved access — the caller
    supplies the run_ids from that evidence record); they are REPORTED in the returned
    report and never suppressed, and this function NEVER writes: back-filling a
    registry row to clear an orphan would be the reconstruction failure repeated
    deliberately. Runs with the integrity test, never on the write path (Q4=D).

    Raises
    ------
    RegistryError
        naming the `run_id` of any orphan not in `known_orphans`, in either direction.
    """
    known = dict(known_orphans or {})
    registry_report = check_registry_integrity(registry_path)
    registry_rows: list[Mapping[str, Any]] = []
    path = Path(registry_path)
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError:
                continue  # already reported by check_registry_integrity
            if isinstance(parsed, dict):
                registry_rows.append(parsed)

    access_records = _read_access_records(Path(access_log_path))
    registry_run_ids = {str(r.get("run_id")) for r in registry_rows}
    access_run_ids = {str(a.get("run_id")) for a in access_records if "run_id" in a}

    reported: dict[str, str] = {}

    for access_run in sorted(access_run_ids):
        if access_run not in registry_run_ids:
            if access_run in known:
                reported[access_run] = known[access_run]
            else:
                raise RegistryError(
                    access_log_path,
                    f"AccessRecord run_id {access_run!r} matches no RegistryEvent: a "
                    f"December access by a run the experiment registry does not know "
                    f"about (R-19) — the unregistered-access case the audit exists to "
                    f"find; it is never cleared by back-filling a row",
                )

    for row in registry_rows:
        if bool(row.get("locked_test_accessed")) and str(row.get("run_id")) not in access_run_ids:
            run_id = str(row.get("run_id"))
            if run_id in known:
                reported[run_id] = known[run_id]
            else:
                raise RegistryError(
                    registry_path,
                    f"RegistryEvent run_id {run_id!r} claims locked_test_accessed = "
                    f"true with no logged AccessRecord (R-19): either the flag is "
                    f"wrong or the log-then-read ordering was bypassed",
                )

    return ReconciliationReport(
        registry_rows=registry_report.rows,
        access_rows=len(access_records),
        expected_orphans=reported,
    )


# --- the derived CSV (W-6: "the CSV is derived, hashed, and marked derived") ------------


def derive_csv(registry_path: Path, csv_path: Path) -> dict[str, Any]:
    """Regenerate `experiment_registry.csv` by folding the JSONL; hash it; mark derived.

    A stale CSV is a COMPLETENESS SHORTFALL recorded machine-readably in the returned
    manifest (`was_stale`), never a fatal error and never console text only — the
    non-fatal tier of the two-tier posture. The manifest is also written beside the CSV
    as `<name>.manifest.json` with `derived: true`.
    """
    registry_path = Path(registry_path)
    csv_path = Path(csv_path)

    rows: list[Mapping[str, Any]] = []
    if registry_path.is_file():
        for line in registry_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError:
                continue  # integrity problems are check_registry_integrity's report
            if isinstance(parsed, dict):
                rows.append(parsed)

    was_stale = csv_path.exists()
    fieldnames = [*REGISTRY_COLUMNS, *EXTENSION_FIELDS]
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})

    manifest = {
        "derived": True,
        "authoritative_source": registry_path.name,
        "source_sha256": (
            hashlib.sha256(registry_path.read_bytes()).hexdigest()
            if registry_path.is_file()
            else ""
        ),
        "csv_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        "row_count": len(rows),
        "was_stale": was_stale,
    }
    manifest_path = csv_path.with_suffix(csv_path.suffix + ".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest
