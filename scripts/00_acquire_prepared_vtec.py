"""Stage script 00: acquire the D-144-approved prepared VTEC product and driver series.

Purpose
-------
The first of the nine phase-aware stage scripts (TE 12/13.2; `services.md` § The nine
stage scripts — phase 1 only). It ORCHESTRATES `src/data/acquisition.py` (W-1): resolve
the frozen Madrigal experiment/kindat/parameter identity from `configs/data.yaml`
(D-144 fixes it; this script never chooses it — R-30), retrieve via the bounded-retry
client, record provenance per file (W-3), hash per file (W-4), account for gaps as
explicit NaN (W-7), and write `request_manifest.json` + `sha256_manifest.json`. It
applies NO scientific transformation at retrieval: it fetches, records, hashes and
refuses (FR-P1-01-1).

Inputs
------
`--config configs/` (the four governed configs, read only through `load_configs`) and
the process environment. Credentials, where a provider requires any, reach the client
via `foundation`'s credential-NAME resolution only (R-14, SD-02) — no credential value
is read, logged or persisted here, and none is declared today: `credential_names_for`
returns an empty tuple for every acquisition provider, which is the recorded state
(the Madrigal identity-field question is the supervisor's, NFR-SEC-01 / Known defects
row 13 — this script does not adopt a reading on it).

Re-run behaviour
----------------
Each run appends its own `started` and terminal rows to the experiment registry
(append-only, R-08/R-09; failed and aborted runs stay visible). A re-run against an
unchanged provider is byte-identical; against a reissued provider file it records the
divergence machine-readably and refuses to overwrite (SEC-A-02). Missing months are
machine-readable manifest fields, never console text only, and are NON-FATAL — the
`audit_ec1_drivers.py:184` gap (exit 0 with no recorded shortfall) is not reproduced:
completeness shortfalls land in the manifest, and a non-zero exit means an integrity
violation (two-tier posture, `team.md` § Code Style).

Boundaries this script holds
----------------------------
* **No December content, path or fixture is touched while BLK-07 stands.** Retrieved
  records are screened by RECORD TIMESTAMP (`assert_no_locked_month_records`, R-31)
  — never by directory or file name — and no restricted path is constructed here;
  this script does not even import the restricted-root guard module (R-28, R-32).
* Step 4 of the stage entry contract is `assert_phase_boundary` — phase 1 only, no
  raw-processing module loaded; `assert_no_raw_fields` runs BEFORE the first write
  (R-23/R-24, checked by `tests/test_phase_contract.py`'s completeness test).
* The TE 18.3 preflight REFUSES while the D-144 acquisition identity is not yet
  transcribed into `configs/data.yaml` (two of D-144's four attached freezes remain
  open): stop and report, never default (TE 18.2/18.3).
* No live provider call is made in this environment: the transport is injected, and
  `_build_transport` refuses with a recorded reason (TE 8.1 permits `requests` only
  where provider terms permit; the retrieval client's rate bound is that permission's
  mechanical form).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
import uuid
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Final

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.acquisition import (  # noqa: E402
    AcquisitionError,
    RetrievalClient,
    assert_no_locked_month_records,
    assert_records_within_window,
    cited_stations,
    count_gaps,
    gap_accounting_entry,
    read_records_csv,
    retrieval_policy,
    select_records_within_window,
    select_station_records,
    store_gaps_as_nan,
    verify_declared_inputs,
    write_fixture_read_manifest,
    write_request_manifest,
    write_sha256_manifest,
)
from src.data.config import (  # noqa: E402
    IntegrityError,
    assert_credential_names_present,
    assert_declared_sources_exist,
    assert_lock_complete,
    assert_no_tbd,
    capture_environment_lock,
    credential_names_for,
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
from src.data.fixture_manifest import load_fixture_scope  # noqa: E402
from src.data.phase_contract import assert_no_raw_fields, assert_phase_boundary  # noqa: E402
from src.data.prepared import (  # noqa: E402
    D16_STATISTIC,
    PROVIDER_COLUMNS,
    cell_bounds,
    cell_of,
    resolve_target_identity,
)
from src.data.release import sha256_of_file, write_release  # noqa: E402

#: The manifest/artifact field names this run produces. Screened through R-23's
#: produced-field limb BEFORE the first write (R-24): a Phase 1 artifact may carry no
#: D-17-excluded field, and the completeness test in tests/test_phase_contract.py
#: asserts this script makes the call.
PRODUCED_FIELDS: tuple[str, ...] = (
    "provider",
    "permanent_citation",
    "location_date",
    "provider_filename",
    "retrieval_date",
    "sha256",
    "suffix_mismatch",
    "divergence",
    "status",
    "attempts",
    "release_status",
    "provider_product_identity",
    "coverage",
    "checksum",
    "licence_access_notes",
    "consuming_configuration",
    "gaps_at_retrieval",
    "gaps_in_artifact",
    "series",
    "provenance_class",
    "producing_interpreter",
    "missing_months",
    # TE 13 identity stamps (R-70/TEC-05, board finding 24): every manifest this stage
    # writes now carries all three, so they are declared to R-23's produced-field guard.
    "phase_id",
    "source_id",
    "target_definition_id",
    # W-7 gap accounting, now actually emitted (board finding 26): the conservation loop
    # in `write_request_manifest` iterated zero entries on every run because this script
    # never passed any.
    "gap_accounting",
)


def _assert_phase1_field_contract() -> None:
    """R-24: the produced-field guard, called before this run's first write."""
    assert_no_raw_fields(PRODUCED_FIELDS, phase=1)


#: The acquisition providers (W-1, W-6). Credential NAMES are resolved per provider
#: through foundation's CredentialNameMap; an empty tuple means no authenticated
#: access is declared for that provider (SD-02) — the recorded state today.
PROVIDERS: tuple[str, ...] = ("madrigal", "gfz", "kyoto_wdc", "nrcan_srmp")

STAGE = "acquisition"
PHASE = 1


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="00_acquire_prepared_vtec.py",
        description=(
            "Acquire the D-144-approved Madrigal MAPGPS gps binned-VTEC product and "
            "the driver series, with full provenance (phase 1 only)."
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
        choices=(1,),
        default=1,
        help="this stage is phase 1 only (TE 7.0A P1-00); 2 is refused by choices",
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
            "`acquisition`'s record (fixtures-and-reproducibility CR-2026-09-07)"
        ),
    )
    return parser.parse_args(argv)


def _declared_data_window(snapshot: Any) -> tuple[dt.date, dt.date]:
    """Board Rec 2 (ML-01): the config-declared retrieval window, read from
    `configs/data.yaml`'s acquisition block (c59 — this script's own input declaration).

    NOT the fixture path (CR-2026-09-13-000102-FIXTURE-WINDOW, owner-ruled Option B, the
    Stage-04 precedent): on a fixture run the declared window IS the fixture scope's
    cited window and the retrieval reads are bounded to it, so this function is never
    consulted there — D-11's and D-14's windows are disjoint, and no single static config
    pair could serve both fixtures. This config declaration remains for the future real
    re-acquisition window (DATA-07 work); `window_start/window_end` stay deliberately
    untranscribed until that work lands, and while undeclared this function REFUSES
    naming them (TE 18.3: stop and report, never default).

    Raises
    ------
    IntegrityError
        `acquisition.window_start`/`window_end` absent, unresolved (`TBD — freeze gate`),
        or not calendar dates.
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
            "undeclared or unresolved; a fixture acquisition run declares the retrieval "
            "window it touches, and the TE 9.2 exemption is BOUND to the fixture scope's "
            "cited window rather than granted on a validating flag alone (board Rec 2 / "
            "ML-01; TE 18.3: stop and report, never default)",
        ) from exc


def _stage_entry(
    config_dir: Path, *, fixture_manifest: Path | None = None, code_commit: str | None = None
) -> dict[str, Any]:
    """Steps 2-6 of the stage entry contract (step 1, determinism, ran in main()).

    2. `load_configs` — snapshot, hash, resolve roots (the only read of configs/).
    3. Preflight: `assert_no_tbd` over this stage's required fields (the D-144
       acquisition identity — REFUSES until its owner transcribes the frozen values)
       and `assert_declared_sources_exist`.
    4. `assert_phase_boundary` — no raw-processing module loaded under phase 1.
    5. Credential-NAME presence per provider (names only, never values).
    6. Seed, capture the eight-item environment lock, open the run record, then
       `require_receipts_for_snapshot` (TE 9.2: both fixtures pass before any full-year
       job; exempt on a fixture run carrying `--fixture-manifest`, Q5 = A).
    """
    snapshot = load_configs(config_dir, phase=PHASE)
    assert_no_tbd(snapshot, required=required_fields_for(STAGE, PHASE))
    assert_declared_sources_exist(snapshot)
    assert_phase_boundary(PHASE, loaded_modules=sys.modules)
    for provider in PROVIDERS:
        assert_credential_names_present(credential_names_for(STAGE, provider, PHASE), os.environ)
    determinism = seed_everything(snapshot, stage=STAGE)
    lock = capture_environment_lock(snapshot, determinism, code_commit=code_commit)
    assert_lock_complete(lock)
    if fixture_manifest is not None:
        # Option B (CR-2026-09-13-000102-FIXTURE-WINDOW, Stage-04 precedent): the fixture
        # scope's cited window is BOTH the declaration and the retrieval read bound; the
        # config pair `acquisition.window_start/window_end` is deliberately not consulted
        # on this path (it stays reserved for the real re-acquisition window, DATA-07).
        scope = load_fixture_scope(fixture_manifest)
        fixture_scope: Any = scope
        audit_window: tuple[dt.date, dt.date] | None = scope.window
        fixture_scope_id: str | None = scope.fixture_id
        declared_window: tuple[dt.date, dt.date] | None = audit_window
    else:
        audit_window = None
        fixture_scope_id = None
        fixture_scope = None
        declared_window = None
    receipts_gate = require_receipts_for_snapshot(
        snapshot,
        lock,
        fixture_manifest=fixture_manifest,
        declared_window=declared_window,
        declared_window_resource=(
            "scripts/00_acquire_prepared_vtec.py: declared retrieval window "
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
        "fixture_scope": fixture_scope,
    }


def _registry_paths(snapshot: Any) -> tuple[Path, Path]:
    registry_root = Path(
        snapshot.resolved_roots.get(
            "registry_root", snapshot.resolved_roots["artifacts"] / "registry"
        )
    )
    registry_path = registry_root / "experiment_registry.jsonl"
    # Read-only input to the writer's R-20 exploratory derivation: this run performs
    # no restricted access, and a missing log means none has occurred.
    access_log = (
        Path(snapshot.resolved_roots["workspace"]) / "evidence" / ("test_run_access_log.jsonl")
    )
    return registry_path, access_log


def _registry_row(
    run_id: str, *, status: str, lock_hash: str, snapshot: Any, reason: str = ""
) -> dict[str, Any]:
    """Compose one TE 13.4 registry row for this run (started | aborted | completed).

    The two free-text columns this function fills — `notes`, and `reason` on the aborted
    branch, where `reason` is `str(exc)` and would carry a live transport's error text —
    are routed through the W-9 redaction chokepoint by the registry writer itself
    (`experiment_registry.REDACTED_FREE_TEXT_FIELDS`, applied in `append_registry_event`
    before any byte is written). This script deliberately keeps NO inline copy of that
    guard: one boundary, one guard home, and the refusal is proved per entry point rather
    than per composer (nfr-design c58).
    """
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    row: dict[str, Any] = {
        "run_id": run_id,
        "started_at_utc": now,
        "completed_at_utc": now if status in ("completed", "aborted", "failed") else "",
        "status": status,
        "code_commit": "",  # populated below from the lock
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
        "notes": f"acquisition run; retrieval policy: {retrieval_policy()}",
    }
    if reason:
        row["reason"] = reason
    return row


def _resolve_stamps(entry: Mapping[str, Any]) -> Mapping[str, str]:
    """The three TE 13 definition IDs for this run, RESOLVED — never invented (R-70, R-30).

    Two sources, in order, and neither is a default:

    1. On a FIXTURE run, the scope's own `identity` block. A fixture scope is required to
       carry all three stamps (`fixture_manifest` validates them as required identity
       fields), and they are the identity of the thing being read, so a fixture manifest
       and the manifests a fixture run writes cannot disagree about it.
    2. Otherwise `configs/data.yaml`'s `target.identity`, through
       `prepared.resolve_target_identity` — the ONE resolver, shared with stage 02, so the
       head and the middle of the chain stamp from the same place rather than from two
       transcriptions that can drift.

    Neither source resolving is a TE 18.3 stop-and-report: `resolve_target_identity`
    raises while `target.identity` is absent or `TBD — freeze gate`, and this function does
    not catch it. That refusal is the correct state today — `configs/data.yaml` carries no
    `target:` block, so a non-fixture run of this stage refuses here and says why, rather
    than writing three artifacts with an identity an implementer chose (TE 18.2).
    """
    scope = entry.get("fixture_scope")
    if scope is not None:
        return dict(scope.identity)
    return resolve_target_identity(entry["snapshot"].data)


def _gap_accounting_for(series: str, raw_values: Sequence[Any]) -> dict[str, Any]:
    """One W-7 `GapAccounting` entry for a series this run read or retrieved.

    Board finding 26: `store_gaps_as_nan` and `gap_accounting_entry` were implemented and
    unit-tested with ZERO production callers, and `write_request_manifest`'s
    `gap_accounting` defaulted empty — so the NaN-count conservation loop iterated nothing
    on every run and the D-5/D-10.2 invariant was carried by nobody. This is their
    production call site, derived from `gap_accounting_entry`'s own scope statement ("the
    entry is a manifest field because FR-P1-01-9 has no acceptance row").

    An empty CSV cell is a GAP, not the string `""`: it is normalised to `None` before
    `store_gaps_as_nan` turns it into an explicit NaN, so a blank the provider left blank
    is counted as missing rather than silently surviving as a present value. The count is
    taken BEFORE and AFTER that normalisation and `gap_accounting_entry` asserts the two
    are equal — the invariant catches a fill on branches no fixture exercises (R-37).
    """
    before = [None if str(value).strip() == "" else value for value in raw_values]
    after = store_gaps_as_nan(before)
    return gap_accounting_entry(
        series,
        gaps_at_retrieval=count_gaps(before),
        gaps_in_artifact=count_gaps(after),
    )


def _build_transport() -> Any:
    """The live provider transport — deliberately NOT constructed in this environment.

    Raises
    ------
    AcquisitionError
        always, with the recorded reason: no live provider call is made while the
        network is unavailable and BLK-07 stands; retrieval runs against injected
        recorded-response transports only (TS-A-01), and TE 8.1 permits `requests`
        only where provider terms permit — wiring a real transport is the deferred
        re-acquisition work, with DATA-07's suffix-recording obligations attached.
    """
    raise AcquisitionError(
        "provider transport",
        "no live provider transport is configured in this environment: retrieval is "
        "exercised against injected recorded-response transports only (TS-A-01), no "
        "network call is authorised here, and the re-acquisition is deferred work "
        "(DATA-07) — supply a transport via RetrievalClient when that work is "
        "authorised; this refusal is recorded rather than defaulted (TE 18.3)",
    )


# =======================================================================================
# The release step (D-61, option A; CR-2026-09-21-RELEASE-OPTION-A)
#
# WHY IT LIVES HERE. `src/data/release.py: write_release` was a complete, tested, TE 13.3
# conformant writer with NO production caller anywhere -- verified 2026-09-21 by grep over
# `scripts/`, `src/`, `notebooks/` and `kaggle/`: only two test modules called it. Meanwhile
# `01_inventory_and_registry.py` reported `release_manifests_found: 0` and
# `02_standardize_prepared_target.py` REFUSED ("no released provider input exists under the
# release root ... refusing rather than fabricating input"), so the Phase 1 sequence could
# not advance past stage 01. Both refusals were correct; the producer was simply never wired.
#
# The owner chose option A on 2026-09-21 -- stage 00 releases what it acquired -- and ruled
# that D-52's "no transport" prohibits transport of PROVIDER BYTES, not writes as such. A
# fixture run still contacts no provider and still reads only the scope's verified derived
# artifacts; what it now also does is publish those verified rows as an immutable release so
# the stages downstream have the input their contract requires.
#
# NOTHING IS FABRICATED. Every manifest field is populated from this run's own facts or from
# a governed config field. `dataset_version` is deliberately absent -- `write_release`
# DERIVES it from the release's own content hash (D-29) and refuses a caller-supplied value.
# =======================================================================================



#: Recorded in a stage-00 release where a fold, mask or feature-set id does not exist yet.
#: Deliberately unusable as a real identifier, so it can never be mistaken for one.
_STAGE00_ID_PLACEHOLDER: Final[str] = "NOT_YET_ASSIGNED_stage_00_precedes_splits_masks_features"


def _cell_descriptor(station_cfg: Mapping[str, Any]) -> dict[str, Any]:
    """The station's selected cell as integers and bound strings — never raw floats (R-11)."""
    lat, lon = station_cfg.get("lat"), station_cfg.get("lon")
    if lat is None or lon is None:
        return {"resolved": False, "reason": "station coordinates unresolved in configs/data.yaml"}
    cell_lat, cell_lon = cell_of(float(lat), float(lon))
    return {
        "resolved": True,
        "cell_gdlat": cell_lat,
        "cell_glon": cell_lon,
        "cell_lat_bounds": cell_bounds(cell_lat),
        "cell_lon_bounds": cell_bounds(cell_lon),
        "rule": "floor-half-open-d1",
    }


def _release_manifest(
    *,
    snapshot: Any,
    verification: Mapping[str, Any],
    evidence_dir: Path,
    records: Sequence[Mapping[str, Any]],
    stations: Sequence[str],
    audit_window: tuple[Any, Any],
    output_files: Mapping[str, str],
) -> dict[str, Any]:
    """The twelve caller-supplied TE 13.3 fields for a fixture run's release."""
    identity = resolve_target_identity(snapshot.data)
    data_cfg = snapshot.data
    acquisition_cfg = data_cfg["acquisition"]

    retrieval_date = "not recorded in the month's request manifest"
    month_request = evidence_dir / "request_manifest.json"
    if month_request.is_file():
        try:
            loaded = json.loads(month_request.read_text(encoding="utf-8"))
            retrieval_date = str(loaded.get("retrieved_at_utc") or retrieval_date)
        except (OSError, ValueError):
            pass

    # source_files: the DERIVED artifacts this run verified and read. A fixture run reads no
    # provider bytes (D-52), so `provider` says so rather than claiming a transfer that did
    # not happen.
    source_files = [
        {
            "provider": "madrigal_derived_artifact",
            "citation": "D-6 (Madrigal / MIT Haystack citation and acknowledgement)",
            "location_date": (
                f"{evidence_dir.name} "
                f"{audit_window[0].isoformat()}..{audit_window[1].isoformat()}"
            ),
            "filename": str(name),
            "retrieval_date": retrieval_date,
            "sha256": str(digest),
        }
        for name, digest in sorted(dict(verification["verified"]).items())
    ]

    stations_cfg = data_cfg.get("stations") or {}
    processing = {
        "phase_id": identity["phase_id"],
        "target_definition_id": identity["target_definition_id"],
        "provider_experiment_kindat": (
            f"{acquisition_cfg['experiment']}/{acquisition_cfg['kindat']}"
        ),
        "parameters": list(acquisition_cfg["parameters"]),
        "station_coordinate_to_cell_rule": str(data_cfg["cell_rule"]),
        # The CELL each station's coordinate selects under D-1's floor rule, with the
        # cell's own bounds as strings. Deliberately NOT the raw lat/lon floats: R-11
        # refuses floats in the canonical content representation, because
        # platform-dependent float serialization would break the byte-identical
        # two-platform requirement — and the cell, not the coordinate, is what the Phase 1
        # target is actually sampled on (D-1; D-17).
        "selected_cell_bounds": {
            station: _cell_descriptor(stations_cfg.get(station) or {})
            for station in stations
        },
        # D-16's frozen statistic, as an IDENTITY. Stage 00 aggregates nothing; the key
        # records which aggregation the released rows are destined for, which is what lets a
        # downstream consumer refuse a mismatch instead of discovering one.
        "hourly_aggregation": D16_STATISTIC,
    }

    by_station: dict[str, int] = {}
    for record in records:
        key = str(record.get("station") or record.get("station_id") or "unattributed")
        by_station[key] = by_station.get(key, 0) + 1

    return {
        "source_manifest_id": (
            f"{evidence_dir.name}:{Path(verification['sha256_manifest']).name}"
        ),
        "source_files": source_files,
        "processing": processing,
        "schema_version": str(data_cfg.get("schema_version", "")),
        "units": {"tec": "TECU", "dtec": "TECU", "ut1_unix": "s"},
        "row_counts": {
            "by_station": by_station,
            "by_month": {evidence_dir.name.replace("audit_evidence_", ""): len(records)},
            # Stage 00 precedes splitting and QC. These axes carry the stage's own position
            # explicitly rather than being omitted, so a reader meets a fact, not a gap.
            "by_split": {"unsplit_stage_00": len(records)},
            "by_qc_stage": {"pre_documented_qc": len(records)},
        },
        "exclusions_qc_summary": [
            {
                "reason": (
                    "records outside the fixture's cited window, excluded on RECORD DATES "
                    "(Option B; never on the folder a record was filed under)"
                ),
                "count": int(verification.get("records_excluded_out_of_window", 0)),
            }
        ],
        "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        # Stage 00 precedes folds, masks and features, so no such id EXISTS yet. TE 13.3
        # requires all fourteen fields non-empty, and `write_release` refuses an empty list,
        # so the stage's position is stated as an explicit token rather than either
        # fabricating an id or leaving the field empty. It is a POSITION, not a scientific
        # value: `NOT_YET_ASSIGNED` is unusable as a fold, mask or feature-set identifier,
        # and every consuming stage asserts a real id at its own boundary.
        "fold_ids": [_STAGE00_ID_PLACEHOLDER],
        "mask_ids": [_STAGE00_ID_PLACEHOLDER],
        "feature_set_ids": [_STAGE00_ID_PLACEHOLDER],
        "output_files": dict(output_files),
        "change_record_id": "CR-2026-09-21-RELEASE-OPTION-A",
    }


def _write_fixture_release(
    *,
    snapshot: Any,
    scope: Any,
    verification: Mapping[str, Any],
    evidence_dir: Path,
    workspace: Path,
    records: Sequence[Mapping[str, Any]],
    stations: Sequence[str],
    audit_window: tuple[Any, Any],
) -> dict[str, Any]:
    """Publish this run's verified rows as an immutable release under the release root.

    The release directory is named for the fixture and this run, so a re-run never collides
    with an earlier release: R-13 refuses a directory that already holds one, and TE 13.3
    requires a NEW version rather than an overwrite.
    """
    release_root = Path(snapshot.resolved_roots["artifacts"]) / "releases"
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    directory = release_root / f"{scope.fixture_id}_{stamp}"
    directory.mkdir(parents=True, exist_ok=False)

    # The released file is a CSV carrying EXACTLY the five provider columns plus the station
    # key, because that is what the consumer requires: `load_released_provider_rows` reads
    # only `.csv` output files and refuses any whose header is not exactly
    # `PROVIDER_COLUMNS` (R-44; D-17). Found by execution — the first version of this step
    # released the rows as JSON, which the consumer SKIPS rather than refuses, so stage 02
    # ran to "completed" with `rows: 0`: a vacuous success. Columns are written in sorted
    # order so the bytes are deterministic across platforms.
    rows_path = directory / "prepared_vtec_records.csv"
    columns = sorted(PROVIDER_COLUMNS)
    with rows_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            missing = [column for column in columns if record.get(column) in (None, "")]
            if missing:
                raise IntegrityError(
                    rows_path,
                    f"a verified record is missing provider column(s) {missing}; the "
                    f"release carries exactly the five provider columns plus the station "
                    f"key and no value is substituted for an absent one (D-17, R-44)",
                )
            writer.writerow({column: record[column] for column in columns})
    output_files = {rows_path.name: sha256_of_file(rows_path)}

    manifest = _release_manifest(
        snapshot=snapshot,
        verification=verification,
        evidence_dir=evidence_dir,
        records=records,
        stations=stations,
        audit_window=audit_window,
        output_files=output_files,
    )
    written = write_release(directory, manifest, release_root=release_root)
    return {
        "release_dir": str(directory.relative_to(workspace)),
        "dataset_version": written["dataset_version"],
        "rows_released": len(records),
    }


def _run_fixture_scoped(
    entry: Mapping[str, Any], *, workspace: Path, out_dir: Path
) -> dict[str, Any]:
    """A fixture run's stage 00: READ the scope's declared derived artifacts, never retrieve.

    Freeze-package item 1, option (a) (CR-2026-09-20-B01-PREREQS 2.5; owner ruling
    2026-09-20). TE 15.1: a walking-skeleton fixture "reads prepared provider VTEC only";
    the input of a fixture run is the month's already-acquired derived artifacts, cited in
    the scope's `inputs.prepared_vtec` and hash-verified by the orchestrator before the
    stage sequence starts. This path re-executes that verification (one guard home:
    `verify_declared_inputs`), reads the cited records file, SELECTS the cited station(s)' in-window
    records on record dates (Option B) and ASSERTS the assembled set (no locked-month record; every
    record inside the cited window), then writes this run's `fixture_read_manifest.json`
    (what was read -- not a request manifest: nothing was requested, so R-35's retrieval
    check is neither applied nor imitated) and `sha256_manifest.json` with
    `provenance_class = "derived_only"` (R-36: the pre-TC-06 months are derived-only and
    say so) and zero provider files. No live transport is
    constructed, no provider is contacted, and DATA-07's re-acquisition obligations are
    untouched -- a fixture run proves plumbing over verified evidence, not retrieval.
    """
    scope = entry["fixture_scope"]
    snapshot = entry["snapshot"]
    acquisition_cfg = snapshot.data["acquisition"]
    verification = verify_declared_inputs(scope, workspace=workspace)
    evidence_dir = Path(verification["evidence_dir"])
    rows = read_records_csv(evidence_dir / verification["records_file"])
    audit_window = entry.get("audit_window")
    if audit_window is None:
        raise IntegrityError(
            scope.path, "a fixture run declares the window it reads (Option B); none resolved"
        )
    stations = cited_stations(scope)
    records = select_records_within_window(
        select_station_records(rows, stations),
        start=audit_window[0],
        end=audit_window[1],
        timestamp_key="date",
    )
    assert_no_locked_month_records(records, timestamp_key="date")
    assert_records_within_window(
        records, start=audit_window[0], end=audit_window[1], timestamp_key="date"
    )
    stamps = _resolve_stamps(entry)
    # W-7 gap accounting over the columns this fixture run actually READ (board finding
    # 26). A fixture run is the one path in this stage that reads real records today, so
    # it is where the conservation invariant first has something to conserve.
    gap_accounting = [
        _gap_accounting_for(f"{scope.fixture_id}:{column}", [r.get(column) for r in records])
        for column in ("tec", "dtec")
    ]
    fixture_inputs = {
        "fixture_id": str(scope.fixture_id),
        "evidence_dir": str(evidence_dir.relative_to(workspace)),
        "sha256_manifest": Path(verification["sha256_manifest"]).name,
        "records_file": verification["records_file"],
        "verified_artifacts": dict(verification["verified"]),
        "stations": stations,
        "records_read_from_month_file": len(rows),
        "records_in_window": len(records),
        "window": [audit_window[0].isoformat(), audit_window[1].isoformat()],
        "gap_accounting": gap_accounting,
    }
    read_manifest = write_fixture_read_manifest(
        out_dir / "fixture_read_manifest.json",
        identity={
            "experiment": acquisition_cfg["experiment"],
            "kindat": acquisition_cfg["kindat"],
            "parameters": acquisition_cfg["parameters"],
        },
        stamps=stamps,
        fixture_inputs=fixture_inputs,
        month_request_manifest=evidence_dir / "request_manifest.json",
        producing_interpreter=sys.version,
    )
    sha256_manifest = write_sha256_manifest(
        out_dir / "sha256_manifest.json",
        provider_files=[],
        derived_artifacts=dict(verification["verified"]),
        provenance_class="derived_only",
        producing_interpreter=sys.version,
        stamps=stamps,
    )
    # D-61 option A: publish the verified rows as an immutable release, so stages 01 and 02
    # have the input their contract requires (R-44: releases by manifest and hash, never
    # bare paths). Runs AFTER every assertion above, so nothing is released that was not
    # first verified, window-checked and proven free of locked-month records.
    release = _write_fixture_release(
        snapshot=snapshot,
        scope=scope,
        verification=verification,
        evidence_dir=evidence_dir,
        workspace=workspace,
        records=records,
        stations=stations,
        audit_window=audit_window,
    )
    return {
        "workspace": str(workspace),
        "fixture_read_manifest": str(read_manifest),
        "sha256_manifest": str(sha256_manifest),
        "client": "none (fixture-scoped read of verified derived artifacts)",
        "fixture_inputs": fixture_inputs,
        "release": release,
    }


def _run(entry: Mapping[str, Any]) -> dict[str, Any]:
    """The acquisition work: guard, resolve, retrieve, screen, account, write.

    Returns the summary the completed registry row's notes cite. Every output value
    passes the W-9 redaction chokepoint: manifest payloads inside the manifest writers,
    and this run's registry free-text columns inside `append_registry_event` (see
    `_registry_row`). December is excluded by RECORD-DATE predicate before anything is
    written (R-31, BLK-07).
    """
    _assert_phase1_field_contract()  # R-24: before the first write, always

    snapshot = entry["snapshot"]
    acquisition_cfg = snapshot.data["acquisition"]  # present: preflight asserted it

    workspace = Path(snapshot.resolved_roots["workspace"])
    out_dir = Path(snapshot.resolved_roots["artifacts"]) / "acquisition"

    if entry.get("fixture_scope") is not None:
        return _run_fixture_scoped(entry, workspace=workspace, out_dir=out_dir)

    client = RetrievalClient(_build_transport())  # raises: no live transport here
    retrieved_records: list[Mapping[str, Any]] = []

    # Membership from record timestamps, never from a name (R-31); no acquisition
    # run may touch calendar 2022-12 while BLK-07 stands.
    assert_no_locked_month_records(retrieved_records, timestamp_key="timestamp")

    # Option B reads-narrowing (CR-2026-09-13-000102-FIXTURE-WINDOW): on a fixture run
    # every retrieved/read record must lie inside the scope's cited window — an
    # out-of-window record REFUSES (R-31's record-date assertion consumed, never
    # copied). Non-fixture runs are unchanged: no window bound beyond R-31.
    audit_window = entry.get("audit_window")
    if audit_window is not None:
        assert_records_within_window(
            retrieved_records,
            start=audit_window[0],
            end=audit_window[1],
            timestamp_key="timestamp",
        )

    stamps = _resolve_stamps(entry)
    # W-7 gap accounting, one entry per retrieved series (board finding 26). Composed from
    # what was retrieved, so a run that retrieved nothing emits nothing and a run that
    # retrieved a series cannot leave the conservation invariant unenforced by omission.
    gap_accounting = [
        _gap_accounting_for(
            str(record.get("logical_name") or record.get("provider_filename") or "<series>"),
            list(record.get("values", ())),
        )
        for record in retrieved_records
        if "values" in record
    ]

    request_manifest = write_request_manifest(
        out_dir / "request_manifest.json",
        identity={
            "experiment": acquisition_cfg["experiment"],
            "kindat": acquisition_cfg["kindat"],
            "parameters": acquisition_cfg["parameters"],
            "madrigalWeb_version": str(acquisition_cfg.get("madrigalWeb_version", "")),
        },
        stamps=stamps,
        provider_files=retrieved_records,
        gap_accounting=gap_accounting,
        provenance_class="full",
        producing_interpreter=sys.version,
        missing_months=[],
    )
    sha256_manifest = write_sha256_manifest(
        out_dir / "sha256_manifest.json",
        provider_files=retrieved_records,
        derived_artifacts={},
        provenance_class="full",
        producing_interpreter=sys.version,
        stamps=stamps,
    )
    return {
        "workspace": str(workspace),
        "request_manifest": str(request_manifest),
        "sha256_manifest": str(sha256_manifest),
        "client": type(client).__name__,
    }


def main() -> int:
    ensure_process_determinism(sys.argv)  # FIRST statement, before any framework import
    args = _parse_args(sys.argv[1:])

    try:
        entry = _stage_entry(
            args.config, fixture_manifest=args.fixture_manifest, code_commit=args.code_commit
        )
    except IntegrityError as exc:
        # Integrity tier, before the run record exists: terminate non-zero naming the
        # resource and the violated expectation. No registry row is fabricated for a
        # run that never entered (a terminal row with no started row is itself an
        # integrity violation, R-08).
        print(f"00_acquire_prepared_vtec: preflight refusal: {exc}", file=sys.stderr)
        return 1

    snapshot = entry["snapshot"]
    lock = entry["lock"]
    lock_hash = environment_lock_hash(lock)
    registry_path, access_log = _registry_paths(snapshot)
    run_id = (
        f"acquisition-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    )

    started = _registry_row(run_id, status="started", lock_hash=lock_hash, snapshot=snapshot)
    started["code_commit"] = lock.code_commit
    append_registry_event(
        registry_path, started, phase=PHASE, writer_role="stage", access_log_path=access_log
    )

    try:
        summary = _run(entry)
    except IntegrityError as exc:
        aborted = _registry_row(
            run_id,
            status="aborted",
            lock_hash=lock_hash,
            snapshot=snapshot,
            reason=str(exc),
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
        print(f"00_acquire_prepared_vtec: aborted: {exc}", file=sys.stderr)
        return 1

    completed = _registry_row(run_id, status="completed", lock_hash=lock_hash, snapshot=snapshot)
    completed["code_commit"] = lock.code_commit
    # a retrieval run's artifact is its request manifest; a fixture-scoped run's is the
    # read manifest (item 1, option (a)) -- whichever the run produced, never both
    artifact = summary.get("request_manifest") or summary["fixture_read_manifest"]
    completed["artifact_manifest_path"] = artifact
    append_registry_event(
        registry_path, completed, phase=PHASE, writer_role="stage", access_log_path=access_log
    )
    print(f"00_acquire_prepared_vtec: completed: {artifact}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
