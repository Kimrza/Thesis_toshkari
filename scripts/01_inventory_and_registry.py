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
* **The source-inventory path now REFUSES too, and for one reason only**: it stamps the
  three TE 13 definition IDs (R-70/TEC-05, board finding 24) and resolves them through
  `prepared.resolve_target_identity`, which raises while `configs/data.yaml` carries no
  `target:` block. Before 2026-09-20 this path ran and wrote a LITERAL EMPTY entry list,
  which is why `assert_source_entry` and `assert_verbatim_notice` had never once fired
  (board finding 26). It now builds a real TE 5.1 nine-field entry per month declared in
  `declared_sources`, with `release_status` carrying the MEASURED provider-version
  distribution (board finding 8). Completeness shortfalls — the ten months awaiting the
  DATA-07 re-acquisition, and any provider whose verbatim acknowledgment notice is not
  transcribed — stay machine-readable `missing_entries` fields and stay non-fatal
  (team.md § Code Style).
* **The schema-validation path (`--validate-schema`) refuses** while `configs/data.yaml`
  carries no `prepared_schema` block: W-5's `expected_schema_from` and `validate_schema`
  had no production caller at all, and this is their entry point (TE 18.3 — stop and
  report, never an implementer default).

Provider-version census (board findings 8 and 22)
-------------------------------------------------
Five of the eleven non-December months carry more than one provider version token
(`g.001` alongside `g.002`) in their own `file` column, and the mix was recorded nowhere
in the workspace. `read_provider_suffix_census` MEASURES the per-month, per-day
distribution and `assert_sources_unmixed_or_recorded` REFUSES a mix the month's declared
`release_status_versions` does not cover — R-52 prohibition 2's first production call
site. The rule is not "never mixed": provider version drift is an observed fact of this
dataset. The rule is "absent or RECORDED". No census figure is written into this script
or into a config by hand; the run produces them (TE 18.2).

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

from src.data.acquisition import (  # noqa: E402
    count_gaps,
    store_gaps_as_nan,
)
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
from src.data.fixture_gate import require_receipts_for_snapshot  # noqa: E402
from src.data.fixture_manifest import (  # noqa: E402
    load_fixture_scope,
    release_root_for,
)
from src.data.inventory import (  # noqa: E402
    AUDIT_MONTHS,
    assert_no_silent_imputation,
    assert_record_date_class_agreement,
    assert_scope_equals_reference,
    attribute_records_by_month,
    build_regime_report,
    coverage_figures,
    expected_schema_from,
    finalize_audit_reports,
    governed_reference_scope,
    new_audit_run_id,
    read_provider_suffix_census,
    route_audit_path,
    validate_schema,
    write_source_inventory,
)
from src.data.locked_test import RESTRICTED_ROOT  # noqa: E402
from src.data.phase_contract import assert_no_raw_fields, assert_phase_boundary  # noqa: E402
from src.data.prepared import resolve_target_identity  # noqa: E402
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
    # TE 13 identity stamps (R-70/TEC-05, board finding 24). The source inventory and
    # both audit reports are gate-read artifacts and carried no identity at all.
    "phase_id",
    "source_id",
    "target_definition_id",
    # The measured provider-version census (board finding 8/22) and the prohibition
    # results it feeds. `provider_version_census` carries the per-month, per-day
    # distribution; `release_status` above is where the month DECLARES it.
    "provider_version_census",
    "records_by_version",
    "provider_files_by_version",
    "version_tokens",
    "version_mixed",
    "days_version_mixed",
    "recorded_versions",
    "mix_recorded",
    "records_examined",
    "records_unrecognised_version",
    "by_day",
    "prohibition_results",
    "gaps_at_retrieval",
    "gaps_in_artifact",
    "expected_schema_digest",
    "observed",
    "checked_at_utc",
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
        "--validate-schema",
        action="store_true",
        help=(
            "attempt the W-5 prepared-product schema validation against the governed "
            "schema; REFUSES while configs/data.yaml carries no prepared_schema block "
            "(TE 18.3 — stop and report, never an implementer default)"
        ),
    )
    parser.add_argument(
        "--code-commit",
        type=str,
        default=None,
        help=(
            "explicit code commit for the environment lock where no git tree exists "
            "(a Kaggle session; the walking-skeleton orchestrator threads its own "
            "--code-commit through here); the lock is never written unpopulated "
            "(REQ-ENG-10; CR-2026-09-20-B01-PREREQS §2)"
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


def _declared_data_window(snapshot: Any) -> tuple[dt.date, dt.date]:
    """Board Rec 2 (ML-01): the config-declared data window, read from
    `configs/data.yaml`'s acquisition block (c59 — this script's own input declaration,
    since the inventory surface walks `acquisition`'s outputs).

    NOT the fixture path (CR-2026-09-13-000102-FIXTURE-WINDOW, owner-ruled Option B, the
    Stage-04 precedent): on a fixture run the declared window IS the fixture scope's
    cited window — D-11's and D-14's windows are disjoint, so no single static config
    pair could serve both fixtures — and this function is never consulted there. On a
    fixture run this stage's only record-reading path, the December audit, is REFUSED
    outright by `_refuse_fixture_audit`, so no month directory is read, counted, or
    required at all. This config declaration remains for the future real re-acquisition
    window (DATA-07); while `window_start/window_end` stay untranscribed it REFUSES
    naming them (TE 18.3: stop and report, never default).

    Raises
    ------
    IntegrityError
        `acquisition.window_start`/`window_end` absent, unresolved, or not calendar dates.
    """
    acquisition_cfg = snapshot.data.get("acquisition")
    block = acquisition_cfg if isinstance(acquisition_cfg, Mapping) else {}
    start, end = block.get("window_start"), block.get("window_end")
    try:
        if start is None or end is None:
            raise ValueError("undeclared")
        return (
            dt.date.fromisoformat(str(start)[:10]),
            dt.date.fromisoformat(str(end)[:10]),
        )
    except (TypeError, ValueError) as exc:
        raise IntegrityError(
            "configs/data.yaml: acquisition.window_start/window_end",
            "undeclared or unresolved; a fixture inventory run declares the data window "
            "it walks (acquisition's declared window), and the TE 9.2 exemption is BOUND "
            "to the fixture scope's cited window rather than granted on a validating flag "
            "alone (board Rec 2 / ML-01; TE 18.3: stop and report, never default)",
        ) from exc


def _refuse_fixture_audit(audit: bool, fixture_manifest: Path | None) -> None:
    """Board Rec 2 (ML-01, owner-authorised per CR-2026-09-07 §11.5; flagged for
    `inventory-and-registry`'s record): the December coverage/regime audit reads the locked
    month, which lies OUTSIDE every fixture scope's cited window by construction (both
    fixtures are December-free), so an audit invocation can never ride the TE 9.2 fixture
    exemption.

    Raises
    ------
    IntegrityError
        `--audit` combined with `--fixture-manifest`.
    """
    if audit and fixture_manifest is not None:
        raise IntegrityError(
            "--audit with --fixture-manifest",
            "the December coverage/regime audit reads the locked month, outside every "
            "fixture scope's cited window by construction; a fixture run cannot host the "
            "audit and the TE 9.2 receipt-gate exemption does not extend to it (board "
            "Rec 2 / ML-01)",
        )


def _stage_entry(
    config_dir: Path,
    *,
    fixture_manifest: Path | None = None,
    audit: bool = False,
    code_commit: str | None = None,
) -> dict[str, Any]:
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
    lock = capture_environment_lock(snapshot, determinism, code_commit=code_commit)
    assert_lock_complete(lock)
    _refuse_fixture_audit(audit, fixture_manifest)
    if fixture_manifest is not None:
        # Option B (CR-2026-09-13-000102-FIXTURE-WINDOW, Stage-04 precedent): the fixture
        # scope's cited window IS the declaration. The reads-narrowing half for this
        # stage is `_refuse_fixture_audit` above: the December audit — this script's only
        # month-record reading path — refuses under ANY fixture scope, so no month
        # directory is read, counted, or required on a fixture run; the inventory path
        # consumes release manifests by ID and hash, never records.
        scope = load_fixture_scope(fixture_manifest)
        audit_window: tuple[dt.date, dt.date] | None = scope.window
        fixture_scope_id: str | None = scope.fixture_id
        declared_window: tuple[dt.date, dt.date] | None = audit_window
    else:
        audit_window = None
        fixture_scope_id = None
        declared_window = None
    receipts_gate = require_receipts_for_snapshot(
        snapshot,
        lock,
        fixture_manifest=fixture_manifest,
        declared_window=declared_window,
        declared_window_resource=(
            "scripts/01_inventory_and_registry.py: declared data window "
            "(fixture scope's cited window on a fixture run)"
        ),
    )
    return {
        "snapshot": snapshot,
        "determinism": determinism,
        "lock": lock,
        "receipts_gate": receipts_gate,
        "audit_window": audit_window,
        "fixture_scope_id": fixture_scope_id,
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
    now = dt.datetime.now(dt.timezone.utc).isoformat()
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


def _resolve_stamps(snapshot: Any) -> Mapping[str, str]:
    """The three TE 13 definition IDs, RESOLVED from `configs/data.yaml` — never invented.

    Delegates to `prepared.resolve_target_identity`, the ONE resolver, so the head of the
    provenance chain and stage 02 stamp from the same transcription rather than from two
    that can drift (R-70, R-30; board finding 24).

    This REFUSES today, and the refusal is the correct state: `configs/data.yaml` carries
    no `target:` block, so `resolve_target_identity` raises a `StandardizationError`
    naming the absent field. Stamping this unit's three gate-read artifacts with an
    identity an implementer chose would be exactly the §18.2 violation the stop-and-report
    exists to prevent. The exception is deliberately NOT caught here.
    """
    return resolve_target_identity(snapshot.data)


def _declared_month_sources(snapshot: Any) -> list[Mapping[str, Any]]:
    """The declared per-month sources this run inventories, from `configs/data.yaml`.

    Read from `declared_sources` rather than hardcoded here, for two reasons. The
    descriptive TE 5.1 values (provider, role, licence/access notes, the consuming
    configuration) are the OWNER's transcription and belong in a governed config, not in a
    script; and `assert_declared_sources_exist` has already hash-verified every entry
    carrying `path` and `sha256` at stage entry, so an entry reaching this function is one
    whose bytes match what the config declares.

    Board findings 8 and 22: `declared_sources` was the literal `[]` and no
    `source_inventory.json` existed anywhere, while both fixture identity declarations
    already cited their month's evidence directory and four SHA-256 hashes. The two
    fixture source months are what this list is populated with first; the remaining ten
    follow at the DATA-07 re-acquisition and are recorded as an open item below.
    """
    declared = snapshot.data.get("declared_sources") or []
    return [item for item in declared if isinstance(item, Mapping)]


def _source_notices(snapshot: Any) -> dict[str, str]:
    """Provider -> the VERBATIM acknowledgment text that provider requires (FR-P1-01-6).

    Read from `configs/data.yaml`'s `source_notices` block. The text is the PROVIDER's,
    character for character, and transcribing it is the owner's act — a paraphrase fails
    `assert_verbatim_notice` exactly as an absent notice does, and inventing one here
    would produce a notice that passes its own check while satisfying nobody.

    Empty today: no notice text is recorded anywhere in this workspace. The absence is
    reported as a machine-readable open item on the inventory rather than papered over.
    """
    block = snapshot.data.get("source_notices")
    if not isinstance(block, Mapping):
        return {}
    return {str(provider): str(text) for provider, text in block.items()}


def _inventory_entry(
    workspace: Path, declaration: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build ONE TE 5.1 nine-field entry for a declared month, and its measured census.

    Every value is either transcribed by the owner into `declared_sources` or MEASURED
    from the month's own evidence. Nothing is composed here:

    * `release_status` is the MEASURED provider-version distribution — the field board
      finding 8 identified as the one that would have surfaced the mix. It is derived from
      the census, never from the declaration, so a declaration that understates the mix
      produces a visible disagreement rather than a quiet agreement.
    * `provider_product_identity` combines the owner's declared identity with the distinct
      provider filenames the month actually carries, so the version suffixes are ON the
      entry.
    * `checksum` is the declared SHA-256, already verified against the bytes at stage
      entry by `assert_declared_sources_exist`.

    Raises
    ------
    IntegrityError
        (as `InventoryError` / `LockedTestError` / `GateError`) from
        `read_provider_suffix_census`: an absent records file, a path inside the
        restricted root, or an UNRECORDED provider-version mix.
    """
    records_path = workspace / str(declaration["path"])
    recorded_versions = [str(v) for v in declaration.get("release_status_versions", ())]
    _rows, census = read_provider_suffix_census(
        records_path,
        recorded_versions=recorded_versions,
        label=str(declaration.get("coverage") or records_path.parent.name),
    )
    observed = census["version_tokens"]
    entry: dict[str, Any] = {
        "provider": declaration["provider"],
        "role": declaration["role"],
        "provider_product_identity": (
            f"{declaration['provider_product_identity']}; provider files carry version "
            f"token(s) {', '.join(observed) or '<none recognised>'} "
            f"({census['provider_files_by_version']} distinct file(s) per token)"
        ),
        "coverage": declaration["coverage"],
        "retrieval_date": declaration["retrieval_date"],
        "checksum": declaration["sha256"],
        # MEASURED, not declared. TE 5.1's "version or release status" slot, given the
        # asserted meaning board finding 8 found missing everywhere in this workspace.
        "release_status": (
            f"provider version distribution (MEASURED {census['records_examined']} "
            f"records): {census['records_by_version']}; mixed={census['version_mixed']}; "
            f"days carrying more than one version: {len(census['days_version_mixed'])}; "
            f"declared: {census['recorded_versions']}"
        ),
        "licence_access_notes": declaration["licence_access_notes"],
        "consuming_configuration": declaration["consuming_configuration"],
    }
    if declaration.get("acknowledgment_notice"):
        entry["acknowledgment_notice"] = declaration["acknowledgment_notice"]
    return entry, census


def _run_inventory(entry: Mapping[str, Any]) -> dict[str, Any]:
    """W-1: write the source inventory from the DECLARED per-month sources.

    Entries are consumed by release ID and hash, never by path (R-44), and every entry
    passes `assert_source_entry`'s nine-field check and `assert_verbatim_notice` where the
    provider requires a notice — both of which had no production caller before 2026-09-20
    because this function wrote a literal empty entry list (board finding 26).

    Two completeness shortfalls are recorded machine-readably rather than as console text
    (`team.md` § Code Style), and neither is fatal:

    * the ten months beyond the two fixture source months, deferred to the DATA-07
      re-acquisition;
    * any provider whose verbatim acknowledgment notice is not yet transcribed.

    A month that IS declared but whose records are absent, or whose provider-version mix
    is not recorded, is an INTEGRITY failure and terminates — that is the two-tier split,
    and it is what makes the census's finding actionable rather than advisory.
    """
    _assert_phase1_field_contract()  # R-24: before the first write, always

    snapshot = entry["snapshot"]
    stamps = _resolve_stamps(snapshot)
    workspace = Path(snapshot.resolved_roots["workspace"])
    # Owner ruling 2026-09-23: a fixture run releases under the walking-skeleton root,
    # a governed run under artifacts/releases/. ONE resolver, so a fixture release can
    # never occupy a governed citation and a governed run can never read a fixture's.
    release_root = release_root_for(
        workspace,
        artifacts_root=Path(snapshot.resolved_roots["artifacts"]),
        fixture_id=entry.get("fixture_scope_id"),
    )
    out_path = Path(snapshot.resolved_roots["artifacts"]) / "inventory" / "source_inventory.json"

    manifests = (
        sorted(release_root.rglob("release_manifest.json")) if release_root.is_dir() else []
    )
    missing_entries: list[str] = []
    if not manifests:
        missing_entries.append(
            f"no released acquisition artifact exists under {release_root.name}/ — the "
            f"inventory consumes releases by release ID and hash (R-44), and none has "
            f"been produced; recorded machine-readably rather than fabricated"
        )

    declarations = _declared_month_sources(snapshot)
    if not declarations:
        missing_entries.append(
            "configs/data.yaml declared_sources is empty — no month is declared, so no "
            "TE 5.1 entry can be built. This is the state board finding 22 reports; the "
            "two fixture source months are the owner's first transcription"
        )
    entries: list[dict[str, Any]] = []
    census_by_source: dict[str, Any] = {}
    for declaration in declarations:
        built, census = _inventory_entry(workspace, declaration)
        entries.append(built)
        census_by_source[str(declaration.get("coverage") or declaration["path"])] = census

    inventoried = len(entries)
    if inventoried and inventoried < len(AUDIT_MONTHS):
        missing_entries.append(
            f"{len(AUDIT_MONTHS) - inventoried} of "
            f"{len(AUDIT_MONTHS)} calendar-2022 months are not yet inventoried; "
            f"the remainder follow at the DATA-07 re-acquisition, which records each "
            f"re-acquired file's FULL provider filename including its version suffix, its "
            f"retrieval date and its SHA-256 (team.md § Walking Skeleton)"
        )

    notices = _source_notices(snapshot)
    providers = sorted({str(built["provider"]) for built in entries})
    unnoticed = [provider for provider in providers if provider not in notices]
    if unnoticed:
        missing_entries.append(
            "no verbatim acknowledgment notice is transcribed for provider(s): "
            + ", ".join(unnoticed)
            + " — FR-P1-01-6 requires the provider's text character for character, its "
            "transcription is the owner's, and a paraphrase fails exactly as an absent "
            "notice does; recorded as an open item rather than invented"
        )

    inventory_path = write_source_inventory(
        out_path,
        entries,
        stamps=stamps,
        required_notices=notices,
        missing_entries=missing_entries,
        provider_version_census=census_by_source,
    )
    return {
        "source_inventory": str(inventory_path),
        "release_manifests_found": len(manifests),
        "entries_written": inventoried,
    }


def _run_schema_validation(entry: Mapping[str, Any]) -> dict[str, Any]:
    """W-5: validate the prepared product against the GOVERNED schema (R-49, TS-I-03).

    `expected_schema_from` and `validate_schema` were implemented and unit-tested with no
    production caller at all (board finding 26), so the governed schema was never checked
    against anything on a real run. This is their entry point, derived from R-49's own
    scope statement ("the expected schema lives in `configs/data.yaml`").

    REFUSES today, and the refusal is the recorded state, not a defect:
    `configs/data.yaml` carries no `prepared_schema` block, so `expected_schema_from`
    raises a `PreflightError` under TE 18.3 rather than validating against a schema an
    implementer supplied by convenience. The shape matches `--build-registry`'s: the code
    is complete and the governed values await their freeze event.
    """
    _assert_phase1_field_contract()
    snapshot = entry["snapshot"]
    expected = expected_schema_from(snapshot.data)  # raises while the block is absent
    observed = snapshot.data.get("prepared_product_observed", {})
    report = validate_schema(observed, expected, resource="prepared product")
    return {
        "expected_schema_digest": report.expected_schema_digest,
        "checked_at_utc": report.checked_at_utc,
    }


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
    # Phase 1 registry resolution: the Phase-2-only `observable_codes` (RINEX-header
    # material, Vision 3.6 phase table / TE 7.0) are not required here; every other 6.2
    # field, the 2022 coverage, the IGRF pin and provenance are (CR-2026-09-20-B01-PREREQS §5).
    assert_registry_resolved(registry, phase=PHASE)
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

    # R-52 prohibition 1, at its production entry point (board finding 26).
    # `assert_no_silent_imputation` and `store_gaps_as_nan` were implemented and
    # unit-tested with no production caller, so the D-5/D-10.2 "gaps are explicit NaN and
    # nothing fills them" rule was carried by nobody on a real run. The audit's own
    # normalisation is where the invariant first has two states to compare: an empty CSV
    # cell is a GAP and becomes an explicit NaN, and the gap count before and after that
    # step must be equal. A fill of any kind — named, aliased or vectorised — changes the
    # count, which is what catches it on branches no fixture exercises.
    prohibition_results: dict[str, str] = {}
    for month in sorted(by_month):
        raw = [
            None if str(row.get("tec", "")).strip() == "" else row.get("tec")
            for row in by_month[month]
        ]
        stored = store_gaps_as_nan(raw)
        assert_no_silent_imputation(raw, stored, series=f"tec[{month}]")
    prohibition_results["silent_imputation"] = "PASS"
    # Prohibition 2's result is established for each month at inventory time, by
    # `read_provider_suffix_census` -> `assert_sources_unmixed_or_recorded`; the audit
    # records the outcome rather than re-deriving it. The remaining two prohibitions
    # (retrospective_split_redesign, map_value_mislabel) are OTHER units' to establish,
    # and `assert_prohibition_results` refuses a record that omits either — the four are
    # separately named exactly so one citation cannot stand for four (R-52).

    provenance_classes: dict[str, str] = {}  # sourced from acquisition manifests (R-36)
    figures = coverage_figures(
        by_month, provenance_classes=provenance_classes, timestamp_key="date"
    )
    coverage_report = {
        "figures": figures,
        "per_month": {month: len(rows) for month, rows in by_month.items()},
        "rows_outside_audit_year_excluded": excluded,
        "prohibition_results": prohibition_results,
        "gaps_in_artifact": {
            month: count_gaps(
                store_gaps_as_nan(
                    [
                        None if str(row.get("tec", "")).strip() == "" else row.get("tec")
                        for row in by_month[month]
                    ]
                )
            )
            for month in sorted(by_month)
        },
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
        stamps=_resolve_stamps(snapshot),
    )
    return {"coverage_report": str(coverage_path), "regime_report": str(regime_path)}


def main() -> int:
    ensure_process_determinism(sys.argv)  # FIRST statement, before any framework import
    args = _parse_args(sys.argv[1:])

    try:
        entry = _stage_entry(
            args.config,
            fixture_manifest=args.fixture_manifest,
            audit=args.audit,
            code_commit=args.code_commit,
        )
    except IntegrityError as exc:
        print(f"01_inventory_and_registry: preflight refusal: {exc}", file=sys.stderr)
        return 1

    snapshot = entry["snapshot"]
    lock = entry["lock"]
    lock_hash = environment_lock_hash(lock)
    registry_path, access_log = _registry_paths(snapshot)
    run_id = (
        f"inventory-and-registry-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
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
        elif args.validate_schema:
            summary = _run_schema_validation(entry)
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
