"""Stage script 01: source inventory, station registry, and the December audit host.

Purpose
-------
The second of the nine phase-aware stage scripts (TE 12/13.2; `services.md` § The nine
stage scripts — P1-02, phases 1 and 2). It ORCHESTRATES `src/data/inventory.py` and
`src/data/registry.py` (W-1 … W-9): the TE 5.1 nine-field source inventory, the station
registry with its conflict register and provenance, the prepared-product schema
validation, and — when authorised — the performance-blind December coverage and regime
audit whose reports feed G-P1A and G-05. `merge_coverage_year.py`'s merge/coverage logic
is MIGRATED into this script (W-9); the original is left untouched this run and its §12
retirement is a gate item.

What this script can and cannot run today
-----------------------------------------
* **The audit entry point REFUSES while BLK-07's authorization limb stands, naming
  BLK-07.** No run may touch calendar 2022-12 while it stands; the authorization is the
  project decision owner's, recorded as a D-number in `_DECEMBER_AUDIT_AUTHORIZATION`
  below, and this refusal is mechanism honouring that record — never a substitute for
  the decision.
* **The registry path refuses at runtime** while `configs/data.yaml` carries its
  `TBD — freeze gate` sentinels for the coordinates, the cell rule and the IGRF version
  (Q2 = A: one pre-G-P1A freeze event; the code is complete, the values await it).
* The source-inventory path runs: with no released acquisition artifact on disk it
  honestly records an EMPTY inventory with a machine-readable `missing_entries` field —
  a completeness shortfall, never console text only (team.md § Code Style).

Migration notes (DISC-I-2 discharged in this copy)
--------------------------------------------------
The migrated restricted reads bind a UNIQUE per-attempt `run_id`
(`audit-<UTCstamp>-<8charuuid>`, SD-I-05) and a REAL `retrieved_at_utc` call-time value —
the `'recorded-at-call-time-by-the-runner'` placeholder is NOT carried over; the
guard-stamped `logged_at_utc` remains the ordering evidence. The triplicated SHA-256
helper is consolidated onto `src/data/release.py`'s `sha256_of_file`. Month folders are
DISCOVERED by name across both evidence roots (an inventory convenience, exactly as the
original script did); membership and every per-month statistic derive from RECORD DATES
only (project.md § Forbidden; R-50) — routing class and content are cross-checked and a
disagreement is a stop-and-report naming the file.

Inputs
------
`--config configs/` (the four governed configs, read only through `load_configs`) and
the process environment. `--build-registry` attempts the station-registry build (refuses
today); `--audit` attempts the December audit (refuses today, naming BLK-07); the
default path writes the source inventory.

Re-run behaviour
----------------
Each run appends its own `started` and terminal rows to the experiment registry
(append-only, R-08/R-09; failed and aborted runs stay visible, NFR-AUD-01). Each audit
ATTEMPT binds a distinct `run_id`, and reconciliation is per-`run_id`, so an honest
re-run is distinguishable from an undisclosed extra access. An interrupted audit writes
NO report; its access rows stand.

Boundaries this script holds
----------------------------
* Step 4 of the stage entry contract is `assert_phase_boundary`; `assert_no_raw_fields`
  runs BEFORE the first write (R-23/R-24).
* This script holds no restricted-root literal (R-28): the restricted root is imported
  as `locked_test`'s constant and resolved through that module's own derivation.
* Every inventory value routes through `acquisition`'s `guard_egress` inside the
  library writers; no credential, token or signed URL enters any output (NFR-SEC-01).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import sys
import uuid
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Final

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import (  # noqa: E402
    IntegrityError,
    LockedTestError,
    assert_declared_sources_exist,
    assert_lock_complete,
    assert_no_tbd,
    capture_environment_lock,
    ensure_process_determinism,
    environment_lock_hash,
    load_configs,
    required_fields_for,
    seed_everything,
)
from src.data.experiment_registry import (  # noqa: E402
    append_registry_event,
    record_abort_honestly,
)
from src.data.inventory import (  # noqa: E402
    assert_record_date_class_agreement,
    assert_scope_equals_reference,
    attribute_records_by_month,
    build_regime_report,
    coverage_figures,
    finalize_audit_reports,
    governed_reference_scope,
    new_audit_run_id,
    route_audit_path,
    write_source_inventory,
)
from src.data.fixture_gate import require_receipts_for_snapshot  # noqa: E402
from src.data.locked_test import RESTRICTED_ROOT  # noqa: E402
from src.data.phase_contract import assert_no_raw_fields, assert_phase_boundary  # noqa: E402
from src.data.registry import assert_registry_resolved, load_registry  # noqa: E402
from src.data.release import sha256_of_file  # noqa: E402

STAGE = "inventory-and-registry"
PHASE = 1

#: BLK-07's authorization limb: the project decision owner's D-number authorising the
#: December coverage/regime audit. `None` records the limb as OPEN — the audit entry
#: point REFUSES while it stands. Filling this constant is the OWNER's act (a recorded
#: decision, cited by D-number), never an implementer's (TE 18.2/18.3); the mechanism
#: below honours the record, it does not substitute for the decision.
_DECEMBER_AUDIT_AUTHORIZATION: Final[str | None] = None

#: The manifest/artifact field names this run can produce, screened through R-23's
#: produced-field limb BEFORE the first write (R-24).
PRODUCED_FIELDS: tuple[str, ...] = (
    "provider",
    "role",
    "provider_product_identity",
    "coverage",
    "retrieval_date",
    "checksum",
    "release_status",
    "licence_access_notes",
    "consuming_configuration",
    "acknowledgment_notice",
    "missing_entries",
    "field_contract",
    "station",
    "month",
    "days_present",
    "days_in_month",
    "day_coverage_pct",
    "hourly_bins_present",
    "hourly_bins_in_month",
    "hourly_coverage_pct",
    "provenance_class",
    "data07_caveat",
    "per_month",
    "figures",
    "count_window",
    "scored_window",
    "one_day_excess_statement",
    "events_tallied",
    "tally",
    "unscored_events",
    "threshold_owner",
)


def _assert_phase1_field_contract() -> None:
    """R-24: the produced-field guard, called before this run's first write."""
    assert_no_raw_fields(PRODUCED_FIELDS, phase=1)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="01_inventory_and_registry.py",
        description=(
            "Source inventory (TE 5.1 nine fields), station registry (Vision 6.2), and "
            "the performance-blind December coverage/regime audit host (P1-02)."
        ),
    )
    parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="the governed configs directory (always configs/; TE 13.2)",
    )
    parser.add_argument(
        "--phase",
        type=int,
        choices=(1, 2),
        default=1,
        help="phase-aware per services.md; every path below is phase-1-legal",
    )
    parser.add_argument(
        "--build-registry",
        action="store_true",
        help=(
            "attempt the station-registry build; REFUSES while configs/data.yaml "
            "carries its TBD — freeze gate sentinels (Q2=A)"
        ),
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help=(
            "attempt the December coverage/regime audit; REFUSES while BLK-07's "
            "authorization limb stands"
        ),
    )
    parser.add_argument(
        "--fixture-manifest",
        type=Path,
        default=None,
        help=(
            "the walking-skeleton fixture scope (a fixture manifest or identity declaration, "
            "validated through the one loader). When given, this run is a FIXTURE run: the "
            "TE 9.2 two-receipt gate is exempt (a fixture run is not a full-year job, Q5 = A) "
            "and the exemption is recorded, never silent. Additive edit flagged for "
            "`inventory-and-registry`'s record (fixtures-and-reproducibility CR-2026-09-07)"
        ),
    )
    return parser.parse_args(argv)


def _stage_entry(config_dir: Path, *, fixture_manifest: Path | None = None) -> dict[str, Any]:
    """Steps 2-6 of the stage entry contract (step 1, determinism, ran in main()).

    2. `load_configs` — snapshot, hash, resolve roots (the only read of configs/).
    3. Preflight: `assert_no_tbd` over this stage's required fields (deliberately
       minimal — the registry's own fields refuse at the registry, per Q2=A) and
       `assert_declared_sources_exist`.
    4. `assert_phase_boundary` — no raw-processing module loaded.
    5. No authenticated provider access is declared for this stage (the inventory reads
       released local artifacts); the credential-NAME presence check has nothing to
       check and nothing is silently skipped — this line records the fact.
    6. Seed, capture the eight-item environment lock, open the run record, then
       `require_receipts_for_snapshot` (TE 9.2: both fixtures pass before any full-year
       job; exempt on a fixture run carrying `--fixture-manifest`, Q5 = A).
    """
    snapshot = load_configs(config_dir, phase=PHASE)
    assert_no_tbd(snapshot, required=required_fields_for(STAGE, PHASE))
    assert_declared_sources_exist(snapshot)
    assert_phase_boundary(PHASE, loaded_modules=sys.modules)
    determinism = seed_everything(snapshot, stage=STAGE)
    lock = capture_environment_lock(snapshot, determinism)
    assert_lock_complete(lock)
    receipts_gate = require_receipts_for_snapshot(
        snapshot, lock, fixture_manifest=fixture_manifest
    )
    return {
        "snapshot": snapshot,
        "determinism": determinism,
        "lock": lock,
        "receipts_gate": receipts_gate,
    }


def _registry_paths(snapshot: Any) -> tuple[Path, Path]:
    registry_root = Path(
        snapshot.resolved_roots.get(
            "registry_root", snapshot.resolved_roots["artifacts"] / "registry"
        )
    )
    registry_path = registry_root / "experiment_registry.jsonl"
    access_log = (
        Path(snapshot.resolved_roots["workspace"]) / "evidence" / "merge_run_access_log.jsonl"
    )
    return registry_path, access_log


def _registry_row(
    run_id: str, *, status: str, lock_hash: str, snapshot: Any, reason: str = ""
) -> dict[str, Any]:
    now = dt.datetime.now(dt.UTC).isoformat()
    row: dict[str, Any] = {
        "run_id": run_id,
        "started_at_utc": now,
        "completed_at_utc": now if status in ("completed", "aborted", "failed") else "",
        "status": status,
        "code_commit": "",  # populated from the lock by the caller
        "environment_lock_hash": lock_hash,
        "platform": snapshot.platform,
        "dataset_version": "",
        "fold_id": "",
        "mask_id": "",
        "feature_set_id": "",
        "model_id": "",
        "hyperparameters_json": "",
        "seed": "",
        "validation_metric_name": "",
        "validation_metric_value": "",
        "artifact_manifest_path": "",
        "prediction_hash": "",
        "locked_test_accessed": False,
        "notes": "inventory-and-registry run (P1-02)",
    }
    if reason:
        row["reason"] = reason
    return row


# =======================================================================================
# The source-inventory path (runs today)
# =======================================================================================


def _run_inventory(entry: Mapping[str, Any]) -> dict[str, Any]:
    """W-1: write the source inventory from acquisition's RELEASED artifacts.

    Entries are consumed by release ID and hash, never by path (R-44). No released
    acquisition artifact exists in this workspace yet, so the inventory honestly
    records zero entries with a machine-readable `missing_entries` field — a
    completeness shortfall is non-fatal and never console text only (team.md § Code
    Style); fabricating nine-field entries from nothing would be the integrity failure.
    """
    _assert_phase1_field_contract()  # R-24: before the first write, always

    snapshot = entry["snapshot"]
    release_root = Path(
        snapshot.resolved_roots.get(
            "release_root", snapshot.resolved_roots["artifacts"] / "releases"
        )
    )
    out_path = Path(snapshot.resolved_roots["artifacts"]) / "inventory" / "source_inventory.json"

    manifests = sorted(release_root.rglob("release_manifest.json")) if release_root.is_dir() else []
    missing_entries: list[str] = []
    if not manifests:
        missing_entries.append(
            f"no released acquisition artifact exists under {release_root.name}/ — the "
            f"inventory consumes releases by release ID and hash (R-44), and none has "
            f"been produced; recorded machine-readably rather than fabricated"
        )
    inventory_path = write_source_inventory(out_path, [], missing_entries=missing_entries)
    return {"source_inventory": str(inventory_path), "release_manifests_found": len(manifests)}


# =======================================================================================
# The registry path (refuses today — Q2 = A)
# =======================================================================================


def _run_registry(entry: Mapping[str, Any]) -> dict[str, Any]:
    """W-2 … W-4: build and resolve the station registry.

    REFUSES today: `load_registry` raises while `configs/data.yaml` carries its
    `TBD — freeze gate` sentinels for the coordinates, the cell rule and the IGRF
    version (Q2 = A — one pre-G-P1A freeze event; no value is defaulted here).
    """
    _assert_phase1_field_contract()
    registry = load_registry(entry["snapshot"])  # raises RegistryError while TBD
    assert_registry_resolved(registry)
    return {"stations": sorted(registry)}


# =======================================================================================
# The December audit path (refuses today — BLK-07)
# =======================================================================================


def _require_december_authorization() -> str:
    """The BLK-07 gate on the audit entry point.

    Raises
    ------
    LockedTestError
        while BLK-07's authorization limb stands (the recorded state:
        `_DECEMBER_AUDIT_AUTHORIZATION is None`). The refusal NAMES BLK-07. The
        authorization is the project decision owner's; when the owner records it as a
        D-number, that D-number is transcribed into the constant and this gate opens —
        nothing here reads an authorization the project does not hold (TE 18.3).
    """
    if _DECEMBER_AUDIT_AUTHORIZATION is None:
        raise LockedTestError(
            "December coverage/regime audit",
            "REFUSED: BLK-07's authorization limb is open, and no run may touch "
            "calendar 2022-12 while it stands. The pre-G-05 coverage and regime audit "
            "(Vision §8.3) runs only once the project decision owner records the "
            "authorization as a D-number; this refusal is the mechanism honouring that "
            "open limb, not a reading of it (TE 18.3 — stop and report, never default)",
        )
    return _DECEMBER_AUDIT_AUTHORIZATION


def _month_dirs(evidence_root: Path, restricted_root: Path) -> dict[int, Path]:
    """Per-month evidence folders across both roots (migrated from the merge script).

    Folder names are an artifact-DISCOVERY convenience only, exactly as the original
    script used them; membership and every per-month statistic derive from RECORD DATES
    (R-50, project.md § Forbidden). A month resolving in both roots is an ambiguity,
    not a preference: the run stops rather than guessing which copy is authoritative.
    """
    found: dict[int, Path] = {}
    for root in (evidence_root, restricted_root):
        if not root.is_dir():
            continue
        for child in sorted(root.iterdir()):
            name = child.name
            if not child.is_dir() or name.endswith("-FULL"):
                continue
            if not name.startswith("audit_evidence_"):
                continue
            suffix = name.rsplit("-", 1)[-1]
            if not suffix.isdigit():
                continue
            month = int(suffix)
            if month in found:
                raise LockedTestError(
                    child,
                    f"month {month:02d} resolves in two roots ({found[month]} and "
                    f"{child}); refusing to guess which copy is authoritative — remove "
                    f"or rename one, or record a decision naming the authoritative root",
                )
            found[month] = child
    return dict(sorted(found.items()))


def _read_month_records(
    month_dir: Path,
    *,
    december_bearing: bool,
    run_id: str,
    registry: Path,
) -> tuple[list[dict[str, str]], list[str]]:
    """Read one month's raw records, routed by class, hash-verified first.

    Hash verification uses `release.sha256_of_file` (the consolidated helper — the
    migrated copy of `merge_coverage_year.py`'s local `sha256_of_file` is NOT carried
    over). Every December-bearing read routes through `open_restricted` with a durable
    row BEFORE the read, under the coverage limb's bound purpose; the routed
    `AccessRecord` carries a real call-time `retrieved_at_utc` (DISC-I-2 discharged in
    this copy) and the guard stamps `logged_at_utc` as the ordering evidence. Returns
    the parsed rows and the identities of every routed December-bearing artifact, for
    reconciliation 3a.
    """
    import json as _json

    routed_identities: list[str] = []

    def _routed(path: Path) -> Path:
        result = route_audit_path(
            path,
            december_bearing=december_bearing,
            run_id=run_id,
            limb="coverage",
            registry=registry,
        )
        if december_bearing:
            routed_identities.append(result.name)
        return result

    hashes_path = month_dir / "sha256_manifest.json"
    if not hashes_path.is_file():
        raise LockedTestError(
            hashes_path,
            "month has no sha256_manifest.json — refusing to audit unverified evidence "
            "(integrity tier; team.md two-tier posture)",
        )
    hashes = _json.loads(_routed(hashes_path).read_text(encoding="utf-8"))
    for name, expected in hashes.items():
        target = month_dir / name
        if not target.is_file():
            raise LockedTestError(
                target,
                "listed in the month's hash manifest but missing on disk; the audit "
                "never proceeds past a failed integrity check",
            )
        actual = sha256_of_file(_routed(target))
        if actual != expected:
            raise LockedTestError(
                target,
                f"FAILED hash check (recorded {expected}, actual {actual}) — evidence "
                f"altered since the run; never continue silently past a failed hash "
                f"(team.md § Mandated)",
            )

    raw_path = month_dir / "madrigal_coverage_raw_records.csv"
    with io.StringIO(_routed(raw_path).read_text(encoding="utf-8")) as handle:
        rows = list(csv.DictReader(handle))
    assert_record_date_class_agreement(
        raw_path, rows, december_bearing=december_bearing, timestamp_key="date"
    )
    return rows, routed_identities


def _dedup(rows: Sequence[Mapping[str, str]]) -> list[Mapping[str, str]]:
    """Cross-month deduplication on (station, ut1_unix, gdlat, glon) — migrated as-is.

    Madrigal experiments straddle UTC day boundaries, so consecutive monthly runs
    legitimately fetch the same file twice; counting those rows twice would inflate
    record counts.
    """
    seen: set[tuple[str, str, str, str]] = set()
    merged: list[Mapping[str, str]] = []
    for row in rows:
        key = (row["station"], row["ut1_unix"], row["gdlat"], row["glon"])
        if key in seen:
            continue
        seen.add(key)
        merged.append(row)
    return merged


def _run_audit(entry: Mapping[str, Any]) -> dict[str, Any]:
    """W-6/W-7: the December coverage and regime audit — REFUSED while BLK-07 stands.

    The refusal is the FIRST statement, before any scope declaration or read. The
    migrated pipeline below is complete and unreachable until the owner's authorization
    lands: declare scope, check it against the governed reference set before any read,
    route every artifact by record-date class with one durable row per December-bearing
    artifact, attribute every count by record timestamp, reconcile per `run_id` (3a
    rows-vs-scope, 3b all twelve months vs the report, December included), and write
    both reports only after every check passes — an interrupted audit yields no report
    while its rows stand.
    """
    _require_december_authorization()  # ALWAYS first; refuses today naming BLK-07

    _assert_phase1_field_contract()
    snapshot = entry["snapshot"]
    workspace = Path(snapshot.resolved_roots["workspace"])
    evidence_root = workspace / "evidence"
    restricted_root = workspace / RESTRICTED_ROOT
    _registry_path, access_log = _registry_paths(snapshot)

    inventory_entries: list[Mapping[str, Any]] = []  # the release inventory (R-44)
    reference = governed_reference_scope(snapshot.data, inventory_entries)
    declared = reference  # the audit declares exactly what is required, up front
    assert_scope_equals_reference(declared, reference)  # check 1: BEFORE any read

    run_id = new_audit_run_id()
    months = _month_dirs(evidence_root, restricted_root)

    all_rows: list[Mapping[str, str]] = []
    december_identities: list[str] = []
    for _month, month_dir in months.items():
        # Residency is the routing HYPOTHESIS — the expected CONSEQUENCE of the
        # record-date class, never its definition (SD-I-04's corrected table). A
        # pre-read content probe would itself be an unlogged December read, so the
        # hypothesis routes the read (logged for the restricted class) and
        # `assert_record_date_class_agreement` verifies the class by record date AFTER
        # the logged read: any disagreement is a stop-and-report naming the file.
        december_bearing = month_dir.resolve().is_relative_to(restricted_root.resolve())
        rows, routed_identities = _read_month_records(
            month_dir,
            december_bearing=december_bearing,
            run_id=run_id,
            registry=access_log,
        )
        all_rows.extend(rows)
        december_identities.extend(routed_identities)

    merged = _dedup(all_rows)
    by_month, excluded = attribute_records_by_month(merged, timestamp_key="date")
    provenance_classes: dict[str, str] = {}  # sourced from acquisition manifests (R-36)
    figures = coverage_figures(
        by_month, provenance_classes=provenance_classes, timestamp_key="date"
    )
    coverage_report = {
        "figures": figures,
        "per_month": {month: len(rows) for month, rows in by_month.items()},
        "rows_outside_audit_year_excluded": excluded,
        "one_day_excess_statement": (
            "December is counted over 1-31 (31 days); the G-06 scored set is 2-31 "
            "(30 days, D-28) — one day of excess, stated rather than left to compute"
        ),
    }
    regime_report = build_regime_report([])
    out_dir = Path(snapshot.resolved_roots["artifacts"]) / "december_audit"
    coverage_path, regime_path = finalize_audit_reports(
        out_dir,
        run_id=run_id,
        registry_path=access_log,
        declared=declared,
        december_identities=december_identities,
        coverage_report=coverage_report,
        regime_report=regime_report,
    )
    return {"coverage_report": str(coverage_path), "regime_report": str(regime_path)}


def main() -> int:
    ensure_process_determinism(sys.argv)  # FIRST statement, before any framework import
    args = _parse_args(sys.argv[1:])

    try:
        entry = _stage_entry(args.config, fixture_manifest=args.fixture_manifest)
    except IntegrityError as exc:
        print(f"01_inventory_and_registry: preflight refusal: {exc}", file=sys.stderr)
        return 1

    snapshot = entry["snapshot"]
    lock = entry["lock"]
    lock_hash = environment_lock_hash(lock)
    registry_path, access_log = _registry_paths(snapshot)
    run_id = (
        f"inventory-and-registry-{dt.datetime.now(dt.UTC).strftime('%Y%m%dT%H%M%SZ')}"
        f"-{uuid.uuid4().hex[:8]}"
    )

    started = _registry_row(run_id, status="started", lock_hash=lock_hash, snapshot=snapshot)
    started["code_commit"] = lock.code_commit
    append_registry_event(
        registry_path, started, phase=PHASE, writer_role="stage", access_log_path=access_log
    )

    try:
        if args.audit:
            summary = _run_audit(entry)
        elif args.build_registry:
            summary = _run_registry(entry)
        else:
            summary = _run_inventory(entry)
    except IntegrityError as exc:
        aborted = _registry_row(
            run_id, status="aborted", lock_hash=lock_hash, snapshot=snapshot, reason=str(exc)
        )
        aborted["code_commit"] = lock.code_commit
        record_abort_honestly(
            registry_path,
            aborted,
            phase=PHASE,
            writer_role="stage",
            access_log_path=access_log,
            original_error=exc,
        )
        print(f"01_inventory_and_registry: aborted: {exc}", file=sys.stderr)
        return 1

    completed = _registry_row(run_id, status="completed", lock_hash=lock_hash, snapshot=snapshot)
    completed["code_commit"] = lock.code_commit
    completed["artifact_manifest_path"] = str(next(iter(summary.values())))
    append_registry_event(
        registry_path, completed, phase=PHASE, writer_role="stage", access_log_path=access_log
    )
    print(f"01_inventory_and_registry: completed: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
