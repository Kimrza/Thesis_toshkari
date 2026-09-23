"""Stage script 02: standardize the Phase 1 hourly target under D-17 — or REFUSE.

Purpose
-------
The third of the nine phase-aware stage scripts (TE 12/13.2; P1-03, Phase 1). It
ORCHESTRATES `src/data/prepared.py`: exactly the closed four-transformation set
(documented QC; UTC normalization; D-1's half-open floor cell selection; D-16's median
hourly aggregation), D-17's sixteen-field row contract with the lineage-caveat column,
the three definition IDs on every artifact, D-19's support thresholds read from config
with their January-November basis, the cell-and-month coverage report, the data-quality
block and the Phase 1 uncertainty budget.

What this script can and cannot run today
-----------------------------------------
**The target-producing path REFUSES while `configs/data.yaml`'s `qc_operations` is
`TBD — freeze gate` or absent (Q2 = A).** The refusal fires BEFORE any output write, the
raise names the field and the expectation that the list be frozen under a D-number —
never mere non-emptiness — and the run's `aborted` registry row is honest. **No
standardized target artifact is produced by any path while that stands.** The refusal is
the deliverable; production waits on a supervisor freeze. The D-17 schema contract, the
caveat column, and their fixture tests are properties of the writer and run regardless
(`tests/test_prepared_target_schema.py`).

The `02` ordinal
----------------
`scripts/02_build_vtec_target.py` (Phase 2) shares this ordinal in TE 12's tree — a
RECORDED defect, not a resolved one. The ordinal denotes the pipeline position and
`--phase` selects exactly one script, so a clean run contains one `02` per phase; the
one-`02`-per-run assertion is `fixtures-and-reproducibility`'s to author in
`tests/test_clean_run.py` against `foundation`'s run-manifest record (an owed
dependency). NO `02a`/`02b` convention is invented (R-73). This script is Phase 1 only:
`--phase` accepts exactly 1, and step 4 of the entry contract
(`assert_phase_boundary`) is never skipped.

Inputs
------
`--config configs/` (the four governed configs, read only through `load_configs`).
Provider input is consumed from RELEASED acquisition artifacts under the release root,
by release manifest and hash — never by bare path (R-44): each candidate release is
verified via `release.verify_release`, and each consumed file's bytes are re-hashed
against the manifest's recorded digest before a row is read.

Re-run behaviour
----------------
Each run appends its own `started` and terminal rows to the experiment registry
(append-only, NFR-AUD-01; failed and aborted runs stay visible with status and reason).
Re-running while the QC list is unfrozen produces another honest `aborted` row, never a
target. No value is interpolated, smoothed or filled; provider values are preserved.

Boundaries this script holds
----------------------------
* `ensure_process_determinism` is the FIRST statement of `main()`; step 4 of the stage
  entry contract is `assert_phase_boundary`; `assert_no_raw_fields` runs BEFORE the
  first write (R-23/R-24).
* No restricted-root literal appears here and no path into the December evidence root is
  constructed (R-28; SD-05).
* Every written payload routes through `acquisition.guard_egress` inside the library
  writers; no credential, token or signed URL enters any output (NFR-SEC-01).
* No scientific value is decided here: D-16, D-17, D-19 and D-1 are applied from config
  and decision records; `qc_operations` and the diff tolerance stay unset by this unit.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import uuid
from collections.abc import Mapping
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.acquisition import assert_records_within_window  # noqa: E402
from src.data.config import (  # noqa: E402
    IntegrityError,
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
from src.data.fixture_manifest import load_fixture_scope  # noqa: E402
from src.data.phase_contract import assert_no_raw_fields, assert_phase_boundary  # noqa: E402
from src.data.prepared import (  # noqa: E402
    LINEAGE_CAVEAT_FIELD,
    assert_qc_operations_frozen,
    load_released_provider_rows,
    standardize_hourly_target,
    write_json_artifact,
    write_target_rows_csv,
)
from src.data.release import (  # noqa: E402
    MANIFEST_NAME,
    ReleaseError,
    content_hash_of,
    sha256_of_file,
    verify_release,
    write_release,
)

STAGE = "target-standardization"
PHASE = 1

#: The field names this run can produce, screened through R-23's produced-field limb
#: BEFORE the first write (R-24). D-17's sixteen fields, the lineage-caveat column, and
#: the coverage/quality/budget artifact keys. No excluded-class token appears here.
PRODUCED_FIELDS: tuple[str, ...] = (
    "interval_start_utc",
    "station_id",
    "cell_gdlat",
    "cell_glon",
    "cell_lat_bounds",
    "cell_lon_bounds",
    "vtec_tecu",
    "valid_observation_count",
    "within_hour_spread_tecu",
    "largest_internal_gap_s",
    "provider_dtec_summary",
    "aggregation_config_id",
    "target_valid",
    "phase_id",
    "source_id",
    "target_definition_id",
    LINEAGE_CAVEAT_FIELD,
    "target_label",
    "artifact_class",
    "station",
    "month",
    "rows",
    "valid_rows",
    "invalid_rows",
    "invalid_reasons",
    "keys",
    "keying_note",
    "per_cell_month",
    "documentation",
    "negative_vtec",
    "missingness_and_support",
    "uncertainty_budget",
    "processor_qc_flags",
    "unexplained_discrepancies",
    "applicable",
    "asymmetry_statement",
    "not_applicable",
    "bounds_statement",
    "completeness",
    # TE 13.3 release-manifest field names, produced by the target release this stage now
    # publishes (see _publish_target_release). Declared to R-23's produced-field guard for
    # the same reason stage 00 declares its own: the guard screens the names this run can
    # write, and a field written but undeclared is the hole it exists to close.
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
    "created_at_utc",
    "provider",
    "citation",
    "location_date",
    "filename",
    "retrieval_date",
    "sha256",
    "reason",
    "count",
    "provider_experiment_kindat",
    "parameters",
    "station_coordinate_to_cell_rule",
    "selected_cell_bounds",
    "hourly_aggregation",
    "by_station",
    "by_month",
    "by_split",
    "by_qc_stage",
)

#: The ONE directory 05, 06 and 07 read the released Phase 1 hourly target from. Each
#: resolves `release_root / TARGET_RELEASE_DIR / release_manifest.json` literally, so the
#: name is the contract between this stage and all three consumers, not a preference.
TARGET_RELEASE_DIR: str = "phase1_hourly_target"

#: Recorded where a fold, mask or feature-set id does not exist yet. Stage 02 precedes all
#: three (splits are 05's, masks are the comparison's, the feature set is the dictionary's),
#: and TE 13.3 requires all fourteen fields non-empty. Deliberately unusable as a real
#: identifier, exactly as stage 00's own placeholder is, so it can never be mistaken for one.
_STAGE02_ID_PLACEHOLDER: str = "NOT_YET_ASSIGNED_stage_02_precedes_splits_masks_features"

#: Stage 02's own change record.
_TARGET_RELEASE_CHANGE_RECORD: str = "CR-2026-09-23-TARGET-RELEASE-OPTION-A"


def _assert_phase1_field_contract() -> None:
    """R-24: the produced-field guard, called before this run's first write."""
    assert_no_raw_fields(PRODUCED_FIELDS, phase=PHASE)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="02_standardize_prepared_target.py",
        description=(
            "Standardize the Phase 1 hourly target under D-17's sixteen-field "
            "contract (P1-03). REFUSES while configs/data.yaml qc_operations is "
            "TBD — freeze gate (Q2 = A): no standardized target is produced."
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
        help=(
            "Phase 1 only: the Phase 2 target build is scripts/02_build_vtec_target.py, "
            "selected by --phase 2 there; one 02 per run, no 02a/02b (R-73)"
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
            "`target-standardization`'s record (fixtures-and-reproducibility CR-2026-09-07)"
        ),
    )
    return parser.parse_args(argv)


def _declared_data_window(snapshot: Any) -> tuple[dt.date, dt.date]:
    """Board Rec 2 (ML-01): the config-declared data window, read from
    `configs/data.yaml`'s acquisition block (c59 — this script's own input declaration,
    since the standardizer consumes `acquisition`'s retrieved prepared product).

    NOT the fixture path (CR-2026-09-13-000102-FIXTURE-WINDOW, owner-ruled Option B, the
    Stage-04 precedent): on a fixture run the declared window IS the fixture scope's
    cited window — D-11's and D-14's windows are disjoint, so no single static config
    pair could serve both fixtures — and this function is never consulted there; the
    standardized rows are asserted inside the scope's window before any write. This
    config declaration remains for the future real re-acquisition window (DATA-07);
    while `window_start/window_end` stay untranscribed it REFUSES naming them
    (TE 18.3: stop and report, never default).

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
            "undeclared or unresolved; a fixture standardization run declares the data "
            "window it consumes (acquisition's declared window), and the TE 9.2 exemption "
            "is BOUND to the fixture scope's cited window rather than granted on a "
            "validating flag alone (board Rec 2 / ML-01; TE 18.3: stop and report)",
        ) from exc


def _stage_entry(
    config_dir: Path, *, fixture_manifest: Path | None = None, code_commit: str | None = None
) -> dict[str, Any]:
    """Steps 2-6 of the stage entry contract (step 1, determinism, ran in main()).

    2. `load_configs` — snapshot, hash, resolve roots (the only read of configs/).
    3. Preflight: `assert_no_tbd` over this stage's required fields (deliberately
       minimal — `qc_operations`' enforcement point is the target-producing run, per
       Q2 = A) and `assert_declared_sources_exist`.
    4. `assert_phase_boundary` — no raw-processing module loaded (never skipped).
    5. No authenticated provider access is declared for this stage (input is released
       local artifacts); the credential-NAME presence check has nothing to check and
       nothing is silently skipped — this line records the fact.
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
    if fixture_manifest is not None:
        # Option B (CR-2026-09-13-000102-FIXTURE-WINDOW, Stage-04 precedent): the fixture
        # scope's cited window is BOTH the declaration and the row bound the target-
        # producing run enforces before any write; the config pair
        # `acquisition.window_start/window_end` is deliberately not consulted here.
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
            "scripts/02_standardize_prepared_target.py: declared data window "
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
        "notes": "target-standardization run (P1-03)",
    }
    if reason:
        row["reason"] = reason
    return row


# =======================================================================================
# The target release (D-61's option A, applied at the 02 -> 05/06/07 boundary)
# =======================================================================================
#
# WHY IT LIVES HERE. D-61 (2026-09-21) closed the identical defect one boundary upstream:
# `write_release` was complete and tested with no production caller, so stage 02 refused
# for want of a released provider input. Stage 00 now publishes what it acquired. The same
# shape reappeared at THIS boundary the moment the ladder advanced: `05`, `06` and `07`
# each resolve `release_root/phase1_hourly_target/release_manifest.json` literally and
# refuse when it is absent, and nothing published it. The owner ruled option A again on
# 2026-09-23 -- the stage publishes the release the downstream stages consume.
#
# NOTHING IS FABRICATED. `source_files` is built from the CONSUMED release manifests, whose
# bytes `load_released_provider_rows` has already verified through `verify_release`;
# `processing` carries the consumed release's own seven Phase 1 keys with the aggregation
# statistic this run actually applied; `row_counts` and `exclusions_qc_summary` are this
# run's measured outcome. `dataset_version` is absent by construction -- `write_release`
# derives it from the release's own content hash (D-29) and refuses a caller-supplied one.
#
# RE-RUNS AND R-13. The consumers fix the directory name, so a re-run cannot simply write a
# new version beside the old one. R-13 refuses to overwrite a release, and this function
# never asks it to: when a release already exists there, the would-be manifest's
# `content_hash` is computed and compared against the published one. Identical content
# republishes NOTHING and reports that (the content hash excludes `created_at_utc`, so an
# identical run is identical by construction). DIFFERENT content REFUSES, naming both
# hashes -- a changed target under an unchanged citation is exactly what TE 13.3's
# "stored under a NEW version rather than overwritten" forbids, and choosing that new
# version is an owner act, not this script's.


def _consumed_release_manifests(release_root: Path) -> list[tuple[Path, dict[str, Any]]]:
    """Every verified release under the root, as (manifest path, manifest) pairs.

    The same enumeration `load_released_provider_rows` performs, re-run here so the release
    this stage publishes can name its inputs. `verify_release` is re-applied rather than
    assumed: the rows were verified when they were read, and the manifest is being cited
    now, so it is checked now.
    """
    out: list[tuple[Path, dict[str, Any]]] = []
    manifests = sorted(release_root.rglob(MANIFEST_NAME)) if release_root.is_dir() else []
    for manifest_path in manifests:
        if manifest_path.parent.name == TARGET_RELEASE_DIR:
            continue  # this stage's own output is never its own input
        problems = verify_release(manifest_path)
        if problems:
            raise IntegrityError(
                manifest_path,
                "a consumed release does not verify, so it cannot be cited as a source of "
                f"the target release: {'; '.join(problems)}",
            )
        out.append((manifest_path, json.loads(manifest_path.read_text(encoding="utf-8"))))
    return out


def _target_release_manifest(
    *,
    snapshot: Any,
    result: Any,
    consumed: list[tuple[Path, dict[str, Any]]],
    output_files: Mapping[str, str],
    fixture_scope_id: str | None,
) -> dict[str, Any]:
    """The thirteen caller-supplied TE 13.3 fields for the Phase 1 hourly target release."""
    if not consumed:
        raise IntegrityError(
            "target release",
            "no consumed release to cite as a source; the target release names the provider "
            "release it was standardized from, never an empty source set (TE 13.3, R-44)",
        )

    source_files: list[dict[str, Any]] = []
    for manifest_path, manifest in consumed:
        version = str(manifest.get("dataset_version", ""))
        content = str(manifest.get("content_hash", ""))
        created = str(manifest.get("created_at_utc", ""))
        for name, digest in sorted(dict(manifest.get("output_files") or {}).items()):
            source_files.append(
                {
                    # The immediate provider of these bytes is the project's own stage-00
                    # release; the ORIGINAL provider travels in that release's own
                    # source_files and is not re-asserted here as if re-retrieved.
                    "provider": "project release (stage 00 acquisition)",
                    "citation": (
                        f"consumed release dataset_version {version}, content_hash {content}"
                    ),
                    "location_date": f"{manifest_path.parent.name} (created {created})",
                    "filename": str(name),
                    "retrieval_date": created,
                    "sha256": str(digest),
                }
            )

    # `processing`: the consumed release's own seven Phase 1 keys, with the identity
    # re-resolved from config (never carried) and the aggregation statistic recorded as the
    # one this run APPLIED -- stage 00 records it as a destination, stage 02 performs it.
    identity = result.identity
    first = dict(consumed[0][1].get("processing") or {})
    processing = {
        "phase_id": identity["phase_id"],
        "target_definition_id": identity["target_definition_id"],
        "provider_experiment_kindat": first.get("provider_experiment_kindat", ""),
        "parameters": list(first.get("parameters") or []),
        "station_coordinate_to_cell_rule": first.get("station_coordinate_to_cell_rule", ""),
        "selected_cell_bounds": dict(first.get("selected_cell_bounds") or {}),
        "hourly_aggregation": first.get("hourly_aggregation", ""),
    }

    rows = list(result.rows)
    by_station: dict[str, int] = {}
    by_month: dict[str, int] = {}
    valid = 0
    for row in rows:
        station = str(row["station_id"])
        by_station[station] = by_station.get(station, 0) + 1
        month = str(row["interval_start_utc"])[:7]
        by_month[month] = by_month.get(month, 0) + 1
        if row.get("target_valid"):
            valid += 1

    # `exclusions_qc_summary`: the MEASURED documented-QC outcome, one entry per reason
    # class, derived from the coverage report's own `invalid_reasons` rather than restated.
    # A row invalidated for two reasons counts under each: the field reports why rows were
    # excluded, not a partition of them.
    # `result.coverage_report` is the RAW report; `payload` is the wrapper
    # `write_json_artifact` adds on the way to disk. Read the raw shape and fall back to the
    # wrapped one, because reading only the wrapper silently yielded zero reasons beside a
    # `by_qc_stage` count of ten invalid rows -- a contradiction inside one manifest, found
    # by running the stage rather than by reading it.
    reasons: dict[str, int] = {}
    report = dict(result.coverage_report)
    entries_by_row = dict(report.get("invalid_reasons") or {}) or dict(
        dict(report.get("payload") or {}).get("invalid_reasons") or {}
    )
    for entries in entries_by_row.values():
        for entry in entries:
            # Group by the RULE violated, not by the measured value. The raw reason reads
            # "largest_internal_gap_s 2400.0 above D-19 maximum 1800.0"; keying on the whole
            # string produced one "class" per distinct float (seven entries for ten rows,
            # four of them singletons), which is a listing rather than a summary. The field
            # and the bound are the class; the value is the instance.
            text = str(entry).strip()
            field = text.split(" ", 1)[0]
            for keyword in (" above ", " below "):
                if keyword in text:
                    reasons_key = f"{field}{keyword}{text.split(keyword, 1)[1]}"
                    break
            else:
                reasons_key = text
            reasons[reasons_key] = reasons.get(reasons_key, 0) + 1
    exclusions = [{"reason": reason, "count": count} for reason, count in sorted(reasons.items())]
    if not exclusions:
        exclusions = [
            {
                "reason": (
                    "no row was invalidated by documented QC in this run (D-53's five "
                    "operations applied; a measured absence, not an unfilled field)"
                ),
                "count": 0,
            }
        ]

    return {
        "source_manifest_id": ";".join(
            sorted(str(m.get("dataset_version", "")) for _p, m in consumed)
        ),
        "source_files": source_files,
        "processing": processing,
        "schema_version": str(snapshot.data.get("schema_version", "")),
        "units": {
            "vtec_tecu": "TECU",
            "within_hour_spread_tecu": "TECU",
            "largest_internal_gap_s": "s",
        },
        "row_counts": {
            "by_station": by_station,
            "by_month": by_month,
            # Stage 02 precedes splitting; the axis carries the stage's position explicitly
            # rather than being omitted, so a reader meets a fact rather than a gap.
            "by_split": {"unsplit_stage_02": len(rows)},
            "by_qc_stage": {
                "post_documented_qc_valid": valid,
                "post_documented_qc_invalid": len(rows) - valid,
            },
        },
        "exclusions_qc_summary": exclusions,
        "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "fold_ids": [_STAGE02_ID_PLACEHOLDER],
        "mask_ids": [_STAGE02_ID_PLACEHOLDER],
        "feature_set_ids": [_STAGE02_ID_PLACEHOLDER],
        "output_files": dict(output_files),
        "change_record_id": _TARGET_RELEASE_CHANGE_RECORD,
        # TC-03f, stamped ON the release. A fixture run publishes the fixture's window
        # under the citation 05/06/07 resolve by a FIXED name, so the directory cannot
        # carry the distinction and the manifest must (see
        # CR-2026-09-23-DRIVER-RELEASE-OPTION-A for the open naming question).
        "evidence_class": "fixture_plumbing" if fixture_scope_id else "governed_run",
        "fixture_scope_id": fixture_scope_id or "",
    }


def _publish_target_release(
    *,
    snapshot: Any,
    result: Any,
    out_dir: Path,
    target_path: Path,
    fixture_scope_id: str | None,
) -> dict[str, Any]:
    """Publish the standardized target as the release 05/06/07 read by manifest and hash."""
    release_root = Path(
        snapshot.resolved_roots.get(
            "release_root", snapshot.resolved_roots["artifacts"] / "releases"
        )
    )
    directory = release_root / TARGET_RELEASE_DIR
    manifest_path = directory / MANIFEST_NAME
    consumed = _consumed_release_manifests(release_root)

    directory.mkdir(parents=True, exist_ok=True)
    released_rows = write_target_rows_csv(directory / target_path.name, result.rows)
    output_files = {released_rows.name: sha256_of_file(released_rows)}
    manifest = _target_release_manifest(
        snapshot=snapshot,
        result=result,
        consumed=consumed,
        output_files=output_files,
        fixture_scope_id=fixture_scope_id,
    )

    if manifest_path.is_file():
        published = json.loads(manifest_path.read_text(encoding="utf-8"))
        would_be = content_hash_of(manifest)
        existing = str(published.get("content_hash", ""))
        if would_be == existing:
            return {
                "release_dir": str(directory),
                "dataset_version": str(published.get("dataset_version", "")),
                "rows_released": len(result.rows),
                "republished": False,
                "note": (
                    "a release with identical content is already published here; R-13 "
                    "refuses an overwrite and none was attempted (the content hash excludes "
                    "created_at_utc, so an identical run is identical by construction)"
                ),
            }
        raise IntegrityError(
            manifest_path,
            f"a DIFFERENT Phase 1 hourly target is already published under this citation "
            f"(published content_hash {existing}, this run's {would_be}). TE 13.3 requires a "
            f"new version rather than an overwrite, and the consumers read this directory by "
            f"name, so choosing how to version it is an owner act -- refusing rather than "
            f"republishing over a citation other artifacts may already cite (R-13)",
        )

    try:
        written = write_release(directory, manifest, release_root=release_root)
    except ReleaseError as exc:
        raise IntegrityError(directory, f"the target release was refused: {exc}") from exc
    return {
        "release_dir": str(directory),
        "dataset_version": written["dataset_version"],
        "rows_released": len(result.rows),
        "republished": True,
    }


def _run_standardize(entry: Mapping[str, Any]) -> dict[str, Any]:
    """W-1: the target-producing run — REFUSED while the QC list is unfrozen (Q2 = A).

    The refusal is the FIRST statement after the produced-field guard, BEFORE input is
    even located, so no output write can precede it and the `aborted` registry row is
    honest. The pipeline below it is complete and unreachable until the supervisor
    freeze lands: consume released provider input by hash, apply exactly the four
    documented transformations, and write the target rows, coverage report,
    data-quality block and uncertainty budget — each artifact stamped with the three
    IDs, the label and the lineage caveat.
    """
    _assert_phase1_field_contract()  # R-24: before the first write, always

    snapshot = entry["snapshot"]
    # Q2 = A: refuse to RUN while qc_operations is TBD — before any output write.
    assert_qc_operations_frozen(snapshot.data)

    release_root = Path(
        snapshot.resolved_roots.get(
            "release_root", snapshot.resolved_roots["artifacts"] / "releases"
        )
    )
    provider_rows = load_released_provider_rows(release_root)
    result = standardize_hourly_target(
        provider_rows,
        data_config=snapshot.data,
        aggregation_config_id=snapshot.hashes["data.yaml"][:12],
    )

    # Option B reads-narrowing (CR-2026-09-13-000102-FIXTURE-WINDOW): on a fixture run
    # every standardized row must lie inside the scope's cited window, asserted BEFORE
    # any write so the aborted registry row stays honest. Released input files are
    # hash-verified wholesale (R-44's carrier, the fluxtable nuance of the Stage-04
    # precedent); the row bound is where an out-of-window input REFUSES — provider rows
    # carry unix-second stamps, so the bound is asserted on the standardized rows'
    # ISO `interval_start_utc` through R-31's ONE date reader, never a second parser.
    audit_window = entry.get("audit_window")
    if audit_window is not None:
        assert_records_within_window(
            result.rows,
            start=audit_window[0],
            end=audit_window[1],
            timestamp_key="interval_start_utc",
        )

    out_dir = Path(snapshot.resolved_roots["artifacts"]) / "prepared_target"
    target_path = write_target_rows_csv(out_dir / "hourly_target_phase1.csv", result.rows)
    coverage_path = write_json_artifact(
        out_dir / "coverage_report.json",
        result.coverage_report,
        identity=result.identity,
        artifact_class="coverage_report",
    )
    quality_path = write_json_artifact(
        out_dir / "data_quality_block.json",
        result.data_quality,
        identity=result.identity,
        artifact_class="data_quality_block",
    )
    budget_path = write_json_artifact(
        out_dir / "uncertainty_budget.json",
        result.uncertainty_budget,
        identity=result.identity,
        artifact_class="uncertainty_budget",
    )
    release = _publish_target_release(
        snapshot=snapshot,
        result=result,
        out_dir=out_dir,
        target_path=target_path,
        fixture_scope_id=entry.get("fixture_scope_id"),
    )
    return {
        "target": str(target_path),
        "coverage_report": str(coverage_path),
        "data_quality_block": str(quality_path),
        "uncertainty_budget": str(budget_path),
        "rows": len(result.rows),
        "release": release,
    }


def main() -> int:
    ensure_process_determinism(sys.argv)  # FIRST statement, before any framework import
    args = _parse_args(sys.argv[1:])

    try:
        entry = _stage_entry(
            args.config, fixture_manifest=args.fixture_manifest, code_commit=args.code_commit
        )
    except IntegrityError as exc:
        print(f"02_standardize_prepared_target: preflight refusal: {exc}", file=sys.stderr)
        return 1

    snapshot = entry["snapshot"]
    lock = entry["lock"]
    lock_hash = environment_lock_hash(lock)
    registry_path, access_log = _registry_paths(snapshot)
    run_id = (
        f"target-standardization-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
        f"-{uuid.uuid4().hex[:8]}"
    )

    started = _registry_row(run_id, status="started", lock_hash=lock_hash, snapshot=snapshot)
    started["code_commit"] = lock.code_commit
    append_registry_event(
        registry_path, started, phase=PHASE, writer_role="stage", access_log_path=access_log
    )

    try:
        summary = _run_standardize(entry)
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
        print(f"02_standardize_prepared_target: aborted: {exc}", file=sys.stderr)
        return 1

    completed = _registry_row(run_id, status="completed", lock_hash=lock_hash, snapshot=snapshot)
    completed["code_commit"] = lock.code_commit
    completed["artifact_manifest_path"] = summary["target"]
    append_registry_event(
        registry_path, completed, phase=PHASE, writer_role="stage", access_log_path=access_log
    )
    print(f"02_standardize_prepared_target: completed: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
