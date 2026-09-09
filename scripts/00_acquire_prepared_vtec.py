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
import datetime as dt
import os
import sys
import uuid
from collections.abc import Mapping
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.acquisition import (  # noqa: E402
    AcquisitionError,
    RetrievalClient,
    assert_no_locked_month_records,
    retrieval_policy,
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
from src.data.phase_contract import assert_no_raw_fields, assert_phase_boundary  # noqa: E402

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


def _stage_entry(config_dir: Path, *, fixture_manifest: Path | None = None) -> dict[str, Any]:
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
    # Read-only input to the writer's R-20 exploratory derivation: this run performs
    # no restricted access, and a missing log means none has occurred.
    access_log = (
        Path(snapshot.resolved_roots["workspace"]) / "evidence" / ("test_run_access_log.jsonl")
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


def _run(entry: Mapping[str, Any]) -> dict[str, Any]:
    """The acquisition work: guard, resolve, retrieve, screen, account, write.

    Returns the summary the completed registry row's notes cite. Every output value
    passes the W-9 redaction chokepoint inside the manifest writers; December is
    excluded by RECORD-DATE predicate before anything is written (R-31, BLK-07).
    """
    _assert_phase1_field_contract()  # R-24: before the first write, always

    snapshot = entry["snapshot"]
    acquisition_cfg = snapshot.data["acquisition"]  # present: preflight asserted it

    workspace = Path(snapshot.resolved_roots["workspace"])
    out_dir = Path(snapshot.resolved_roots["artifacts"]) / "acquisition"

    client = RetrievalClient(_build_transport())  # raises: no live transport here
    retrieved_records: list[Mapping[str, Any]] = []

    # Membership from record timestamps, never from a name (R-31); no acquisition
    # run may touch calendar 2022-12 while BLK-07 stands.
    assert_no_locked_month_records(retrieved_records, timestamp_key="timestamp")

    request_manifest = write_request_manifest(
        out_dir / "request_manifest.json",
        identity={
            "experiment": acquisition_cfg["experiment"],
            "kindat": acquisition_cfg["kindat"],
            "parameters": acquisition_cfg["parameters"],
            "madrigalWeb_version": str(acquisition_cfg.get("madrigalWeb_version", "")),
        },
        provider_files=retrieved_records,
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
        entry = _stage_entry(args.config, fixture_manifest=args.fixture_manifest)
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
        f"acquisition-{dt.datetime.now(dt.UTC).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
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
    completed["artifact_manifest_path"] = summary["request_manifest"]
    append_registry_event(
        registry_path, completed, phase=PHASE, writer_role="stage", access_log_path=access_log
    )
    print(f"00_acquire_prepared_vtec: completed: {summary['request_manifest']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
