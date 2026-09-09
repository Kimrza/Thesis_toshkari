"""Stage script 05: features and splits -- partitions, the permitted-producer refusal, bundles.

Purpose
-------
The sixth of the nine phase-aware stage scripts (TE 12/13.2; `services.md` section The nine
stage scripts -- P1-04's feature/split half). It ORCHESTRATES `src/data/splits.py` and
`src/features/{availability,build,transforms,windows}.py` (W-1 ... W-6, W-8, W-9):
the six partitions and the five-row split manifest, the availability matrix and its three
limbs, the three-call `raw` -> `fit_transforms` -> `train`/`score` sequence per
fitting-capable partition, and the persisted `FeatureBundle`s.

What this script can and cannot run today
-----------------------------------------
* **It REFUSES, honestly, at the permitted-producer list** (SD-F-01, Q1 = A; Q3 = A's
  separate loader): `configs/features.yaml`'s `permitted_producers` is `TBD -- freeze gate`
  and assigned to nobody, so `load_permitted_producers` raises `LeakageError` naming the
  rows lacking entries, the run writes an `aborted` registry row carrying that reason, and
  NO feature matrix is produced. The refusal is checked GENUINELY FIRST -- before the
  feature dictionary is read and before partitions -- against the closed TE 6.2 row
  identities (`SECTION_6_2_ROWS`), because it is this unit's deliverable and the reason a
  reviewer must see on the aborted row even while `features.feature_dictionary` is itself
  `TBD -- freeze gate`. Once the dictionary loads, producers are re-checked against the
  dictionary-derived rows so a dictionary/row disagreement still surfaces.
* Behind it, `build_partitions` REFUSES while `data.partitions` / `experiment.embargo_hours`
  are unfrozen (`PartitionError`), and `read_availability_lags` while
  `features.availability_lags` is (`FeatureAvailabilityError`). Every refusal is an
  `IntegrityError`, so the same honest `aborted` row covers each.
* **No December path exists.** The fitting-capable set is `F1`..`F4`, `REFIT`;
  `--partition DEC` is refused by `argparse` and no call here materialises the locked
  partition (that is `materialise_locked_partition`'s, behind a verifying G-05 signature,
  and it is not invoked by this script).
* When every value is frozen, `--partition <id>` (default: all five) runs the three-call
  sequence with the target and driver inputs supplied through the release root; those
  loaders are `target-standardization`'s and `external-products`' artifacts and are read
  by manifest -- a missing release refuses.

Inputs
------
`--config configs/` (the four governed configs, read only through `load_configs`);
`--phase 1|2` (every path below is phase-1-legal); `--partition` (repeatable, from
`F1`..`F4`,`REFIT`); `--bundles-out` (workspace-relative bundle root, default
`artifacts/features`); `--parity-tolerance` (the fixture manifest's declared value, TE 15.2;
absent -> the value-level parity limb STOPS naming the field); `--code-commit`.

Re-run behaviour
----------------
Each run appends its own `started` and terminal rows to the experiment registry
(append-only, R-08/R-09; aborted runs stay visible, NFR-AUD-01). Bundles are never
overwritten (`write_bundle` refuses an existing directory). A re-run under the same frozen
configs reproduces the same bundles.

Boundaries this script holds
----------------------------
* Step 1 of the entry contract is `ensure_process_determinism`; `assert_phase_boundary` is
  step 4; `assert_no_raw_fields` runs BEFORE the first write (R-23/R-24).
* Imports nothing under `src/external/iri.py`, `src/external/gim.py`, `src/gnss/`,
  `src/models/` or `src/evaluation/`.
* No scientific constant: every lag, bound, window, boundary and the producer list are
  configuration; nothing here defaults one.
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
from src.data.fixture_evidence import stamp_for_manifest, write_sibling_stamp  # noqa: E402
from src.data.fixture_gate import require_receipts_for_snapshot  # noqa: E402
from src.data.fixture_manifest import (  # noqa: E402
    MEASUREMENTS_NAME,
    build_apparatus_partitions,
    load_fixture_scope,
    read_embargo_hours,
)
from src.data.phase_contract import assert_no_raw_fields, assert_phase_boundary  # noqa: E402
from src.data.registry import load_registry  # noqa: E402
from src.data.splits import (  # noqa: E402
    FITTING_PARTITION_IDS,
    apply_embargo,
    build_partitions,
    build_split_manifest,
    locked_partition_record,
    partition_by_id,
    training_range,
    validation_month_range,
)
from src.features._frames import records_of  # noqa: E402
from src.features.availability import assert_lags_safe, build_availability_matrix  # noqa: E402
from src.features.build import (  # noqa: E402
    SECTION_6_2_ROWS,
    FrameSpec,
    build_features,
    load_feature_dictionary,
    load_permitted_producers,
    write_bundle,
)
from src.features.transforms import fit_transforms  # noqa: E402

STAGE = "features-and-splits"
PHASE_DEFAULT = 1

#: The manifest/artifact field names this run can produce, screened through R-23's
#: produced-field limb BEFORE the first write (R-24).
PRODUCED_FIELDS: tuple[str, ...] = (
    "artifact_class",
    "partition_count",
    "partitions",
    "partition_id",
    "kind",
    "train_start",
    "train_end",
    "validation_month",
    "embargo_hours",
    "excluded_embargo_rows",
    "locked_partition_recorded_separately",
    "cross_validation",
    "evaluated_month",
    "access_gate_state",
    "recorded_separately_from_split_manifest",
    "role",
    "scored_start",
    "scored_end",
    "transform_id",
    "phase_id",
    "source_id",
    "target_definition_id",
    "columns",
    "provenance",
    "dictionary_row",
    "dictionary_field",
    "producing_artifact",
    "excluded_counts",
    "standardized_columns",
    "sequence_columns",
    "tensor_features",
    "feature",
    "observation_timestamp",
    "publication_timestamp",
    "release_status",
    "safe_lag_hours",
    "actual_lag_hours",
    "anchor_policy",
    "latency_statement",
)


def _assert_phase1_field_contract(phase: int) -> None:
    """R-24: the produced-field guard, called before this run's first write."""
    assert_no_raw_fields(PRODUCED_FIELDS, phase=phase)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="05_build_features_and_splits.py",
        description=(
            "Features and splits (P1-04): six partitions, five-row split manifest, the "
            "availability matrix, per-partition train-only transforms and feature bundles. "
            "REFUSES today at the unset permitted-producer list (SD-F-01)."
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
        default=PHASE_DEFAULT,
        help="phase-aware per services.md; every path below is phase-1-legal",
    )
    parser.add_argument(
        "--partition",
        action="append",
        choices=FITTING_PARTITION_IDS,
        default=None,
        help=(
            "fitting-capable partition(s) to build (repeatable; default all five). DEC is "
            "not a choice: no December path exists in this script"
        ),
    )
    parser.add_argument(
        "--bundles-out",
        type=Path,
        default=Path("artifacts/features"),
        help="workspace-relative bundle root (one directory per bundle, M9)",
    )
    parser.add_argument(
        "--parity-tolerance",
        type=float,
        default=None,
        help=(
            "the fixture manifest's declared floating-point tolerance for WS-13's value-level "
            "parity limb (TE 15.2); absent, that limb stops naming the field"
        ),
    )
    parser.add_argument(
        "--code-commit",
        type=str,
        default=None,
        help=(
            "explicit code commit for the environment lock where no git tree exists "
            "(a Kaggle session, or a temporary smoke workspace); the lock is never "
            "written unpopulated (REQ-ENG-10)"
        ),
    )
    parser.add_argument(
        "--fixture-manifest",
        type=Path,
        default=None,
        help=(
            "the walking-skeleton fixture scope (a fixture manifest or identity declaration, "
            "validated through the one loader). When given, this run is a FIXTURE run: the "
            "apparatus partitions are built from the scope's declaration (never a frozen id, "
            "R-137), every output is stamped, the run is fixture-scale, and the TE 9.2 "
            "two-receipt gate is exempt (Q4/Q5 = A). Additive edit flagged for "
            "`features-and-splits`' record (fixtures-and-reproducibility CR-2026-09-07)"
        ),
    )
    args = parser.parse_args(argv)
    if args.fixture_manifest is not None and args.partition:
        parser.error(
            "--fixture-manifest runs the manifest's declared apparatus partitions; a frozen "
            "--partition id alongside it is a contradiction (R-137's two-way quarantine)"
        )
    return args


def _stage_entry(
    config_dir: Path,
    *,
    phase: int,
    code_commit: str | None,
    fixture_manifest: Path | None = None,
) -> dict[str, Any]:
    """Steps 2-6 of the stage entry contract (step 1, determinism, ran in main());
    then `require_receipts_for_snapshot` (TE 9.2; exempt on a fixture run, Q5 = A)."""
    snapshot = load_configs(config_dir, phase=phase)
    assert_no_tbd(snapshot, required=required_fields_for(STAGE, PHASE_DEFAULT))
    assert_declared_sources_exist(snapshot)
    assert_phase_boundary(phase, loaded_modules=sys.modules)
    determinism = seed_everything(snapshot, stage=STAGE)
    lock = capture_environment_lock(snapshot, determinism, code_commit=code_commit)
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
        "feature_set_id": str(snapshot.features.get("feature_set_id", "")),
        "model_id": "",
        "hyperparameters_json": "",
        "seed": "",
        "validation_metric_name": "",
        "validation_metric_value": "",
        "artifact_manifest_path": "",
        "prediction_hash": "",
        "locked_test_accessed": False,
        "notes": "features-and-splits run (P1-04); no December path exists in this script",
    }
    if reason:
        row["reason"] = reason
    return row


# =======================================================================================
# The run: refusals first, then the three-call sequence per fitting-capable partition
# =======================================================================================


def _load_release_inputs(snapshot: Any) -> tuple[Any, Mapping[str, Any]]:
    """The target frame and the driver series, read BY MANIFEST from the release root.

    Both are upstream units' artifacts (`target-standardization`, `external-products`).
    A missing release refuses: this script never constructs a target or a driver itself.
    """
    release_root = Path(snapshot.resolved_roots.get("release_root", ""))
    target_manifest = release_root / "phase1_hourly_target" / "release_manifest.json"
    if not target_manifest.is_file():
        raise IntegrityError(
            target_manifest,
            "no released Phase 1 hourly target manifest; features are built from a released "
            "target read by manifest and hash, never from a bare path (TE 13.3)",
        )
    raise IntegrityError(
        target_manifest,
        "reading the released target and driver products into frames is reached only after "
        "the permitted-producer list, the partitions and the availability lags are frozen; "
        "none is today, so this path is unreachable and stops here rather than defaulting a "
        "loader (TE 18.3)",
    )


def _run_fixture_scale(entry: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    """Q4 = A (fixtures-and-reproducibility R-137): the fixture-scale path, additive only.

    Runs the SAME three-call sequence as the full-year path, but over the APPARATUS
    partitions the fixture scope declares (ids quarantined from the six frozen ids — the
    loader refuses a frozen id, control 15), with `apparatus_partition_id` and the fixture
    stamp on every output and an apparatus split manifest instead of the five-row one. The
    scientific values are unchanged: the permitted-producer refusal, the dictionary, the
    availability lags and the release-root inputs are the same governed reads, so today
    this path refuses exactly where the full-year path does (first at the unset
    permitted-producer list; behind it `read_embargo_hours` refuses at
    `configs/experiment.yaml: embargo_hours` `TBD — freeze gate`). No locked record is
    written: no fixture partition is ever `locked` (R-137; R-82).

    Board Rec 4 (ML-03, owner-authorised per CR-2026-09-07 §11.5; flagged for
    `features-and-splits`' record): a machine-readable measurement block
    (`fixture_measurements.json`, scored feature-window rows where measurable) is emitted
    under the bundle root for the orchestrator to fold into candidate measurements.
    """
    _assert_phase1_field_contract(args.phase)  # R-24: before the first write, always
    snapshot = entry["snapshot"]
    workspace = Path(snapshot.resolved_roots["workspace"])
    scope = load_fixture_scope(Path(args.fixture_manifest))

    # The same fail-closed science refusals as the full-year path (fixture scale changes
    # the partitions and the data scope, never a governed value — TC-03e; R-122).
    load_permitted_producers(args.config, dictionary_rows=sorted(SECTION_6_2_ROWS))
    dictionary = load_feature_dictionary(snapshot)
    rows = sorted({str(e["dictionary_row"]) for e in dictionary.values()})
    load_permitted_producers(args.config, dictionary_rows=rows)

    # Apparatus partitions from the scope's declaration; embargo from configuration.
    partitions = build_apparatus_partitions(scope, embargo_hours=read_embargo_hours(snapshot))
    stamp_base = stamp_for_manifest(scope)

    target, drivers = _load_release_inputs(snapshot)  # refuses honestly today (TE 18.3)
    matrix = build_availability_matrix(snapshot, drivers=drivers)
    assert_lags_safe(matrix)
    registry = load_registry(snapshot)

    out_root = workspace / args.bundles_out
    written: list[str] = []
    excluded_embargo: dict[str, int] = {}
    scored_rows: list[int] = []
    for partition in partitions:
        pid = partition.partition_id
        train_start, train_end = training_range(partition)
        train_spec = FrameSpec(pid, "train", train_start, train_end)
        common = {
            "drivers": drivers,
            "registry": registry,
            "matrix": matrix,
            "partitions": partitions,
            "snapshot": snapshot,
            "parity_tolerance": args.parity_tolerance,
        }
        stamp = stamp_for_manifest(scope, apparatus_partition_id=pid)
        raw = build_features(target, spec=train_spec, **common)
        transform = fit_transforms(raw, partition=partition)
        train = build_features(target, spec=train_spec, transform=transform, **common)
        for bundle in (raw, train):
            bundle_dir = write_bundle(bundle, out_root)
            write_sibling_stamp(Path(bundle_dir), stamp)
            written.append(str(bundle_dir))
        if partition.validation_month is not None:
            score_start, score_end = validation_month_range(partition)
            scored_target, excluded = apply_embargo(target, partition)
            excluded_embargo[pid] = excluded
            score_spec = FrameSpec(pid, "score", score_start, score_end)
            score = build_features(scored_target, spec=score_spec, transform=transform, **common)
            bundle_dir = write_bundle(score, out_root)
            write_sibling_stamp(Path(bundle_dir), stamp)
            written.append(str(bundle_dir))
            scored_rows.append(len(records_of(score.matrix)))

    if scored_rows:  # Rec 4: measurable here — scored feature-window rows per partition
        measurements_path = out_root / MEASUREMENTS_NAME
        measurements_path.parent.mkdir(parents=True, exist_ok=True)
        measurements_path.write_text(
            json.dumps(
                {
                    "stage": "05_build_features_and_splits",
                    "measurements": {
                        "row_count_ranges": {
                            "feature_window": {
                                "min": min(scored_rows),
                                "max": max(scored_rows),
                                "units": "rows",
                            }
                        }
                    },
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        written.append(str(measurements_path))

    manifest = {
        "artifact_class": "apparatus_split_manifest",
        "fixture_id": scope.fixture_id,
        "partitions": sorted(p.partition_id for p in partitions),
        "excluded_embargo_rows": excluded_embargo,
        "fixture_stamp": stamp_base.as_mapping(),
        "note": (
            "apparatus partitions (R-122 test-apparatus constants; R-137's two-way "
            "quarantine from the six frozen ids); never the five-row confirmatory manifest"
        ),
    }
    manifest_path = out_root / "apparatus_split_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return {"split_manifest": str(manifest_path), "bundles_written": written}


def _run(entry: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.fixture_manifest is not None:
        return _run_fixture_scale(entry, args)  # Q4 = A: the ONE fixture-scale entry
    _assert_phase1_field_contract(args.phase)  # R-24: before the first write, always
    snapshot = entry["snapshot"]
    workspace = Path(snapshot.resolved_roots["workspace"])

    # 1. The fail-closed refusal GENUINELY FIRST (SD-F-01): the permitted-producer list is
    #    checked against the closed TE 6.2 ROW IDENTITIES (`SECTION_6_2_ROWS`, identities not
    #    values) BEFORE the dictionary is read, so the aborted row names the producer list even
    #    while `features.feature_dictionary` is itself `TBD -- freeze gate`. Then the dictionary
    #    loads and producers are RE-CHECKED against the dictionary-derived rows, so a
    #    dictionary/row disagreement still surfaces.
    load_permitted_producers(args.config, dictionary_rows=sorted(SECTION_6_2_ROWS))
    dictionary = load_feature_dictionary(snapshot)
    rows = sorted({str(e["dictionary_row"]) for e in dictionary.values()})
    load_permitted_producers(args.config, dictionary_rows=rows)

    # 2. Partitions (values from configs/data.yaml), the five-row manifest, the locked record.
    partitions = build_partitions(snapshot)
    locked_record = locked_partition_record(
        partitions, access_gate_state="G-05 Blocked; no execution path in this script"
    )

    # 3. Inputs by manifest, the availability matrix and its three limbs.
    target, drivers = _load_release_inputs(snapshot)
    matrix = build_availability_matrix(snapshot, drivers=drivers)
    assert_lags_safe(matrix)
    registry = load_registry(snapshot)

    # 4. The three-call sequence per fitting-capable partition (R-81, FU-6 = A).
    wanted = tuple(args.partition) if args.partition else FITTING_PARTITION_IDS
    out_root = workspace / args.bundles_out
    written: list[str] = []
    excluded_embargo: dict[str, int] = {}
    for pid in wanted:
        partition = partition_by_id(partitions, pid)
        train_start, train_end = training_range(partition)
        train_spec = FrameSpec(pid, "train", train_start, train_end)
        common = {
            "drivers": drivers,
            "registry": registry,
            "matrix": matrix,
            "partitions": partitions,
            "snapshot": snapshot,
            "parity_tolerance": args.parity_tolerance,
        }
        raw = build_features(target, spec=train_spec, **common)
        transform = fit_transforms(raw, partition=partition)
        written.append(str(write_bundle(raw, out_root)))
        train = build_features(target, spec=train_spec, transform=transform, **common)
        written.append(str(write_bundle(train, out_root)))
        if partition.validation_month is not None:
            score_start, score_end = validation_month_range(partition)
            scored_target, excluded = apply_embargo(target, partition)
            excluded_embargo[pid] = excluded
            score_spec = FrameSpec(pid, "score", score_start, score_end)
            score = build_features(scored_target, spec=score_spec, transform=transform, **common)
            written.append(str(write_bundle(score, out_root)))

    manifest = build_split_manifest(partitions, excluded_embargo_rows=excluded_embargo)
    manifest_path = out_root / "split_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    (out_root / "locked_partition_record.json").write_text(
        json.dumps(locked_record, indent=2, sort_keys=True), encoding="utf-8"
    )
    return {"split_manifest": str(manifest_path), "bundles_written": written}


def main() -> int:
    ensure_process_determinism(sys.argv)  # FIRST statement, before any framework import
    args = _parse_args(sys.argv[1:])

    try:
        entry = _stage_entry(
            args.config,
            phase=args.phase,
            code_commit=args.code_commit,
            fixture_manifest=args.fixture_manifest,
        )
    except IntegrityError as exc:
        print(f"05_build_features_and_splits: preflight refusal: {exc}", file=sys.stderr)
        return 1

    snapshot = entry["snapshot"]
    lock = entry["lock"]
    lock_hash = environment_lock_hash(lock)
    registry_path, access_log = _registry_paths(snapshot)
    run_id = (
        f"features-and-splits-{dt.datetime.now(dt.UTC).strftime('%Y%m%dT%H%M%SZ')}"
        f"-{uuid.uuid4().hex[:8]}"
    )

    started = _registry_row(run_id, status="started", lock_hash=lock_hash, snapshot=snapshot)
    started["code_commit"] = lock.code_commit
    append_registry_event(
        registry_path,
        started,
        phase=args.phase,
        writer_role="stage",
        access_log_path=access_log,
    )

    try:
        summary = _run(entry, args)
    except IntegrityError as exc:
        aborted = _registry_row(
            run_id, status="aborted", lock_hash=lock_hash, snapshot=snapshot, reason=str(exc)
        )
        aborted["code_commit"] = lock.code_commit
        record_abort_honestly(
            registry_path,
            aborted,
            phase=args.phase,
            writer_role="stage",
            access_log_path=access_log,
            original_error=exc,
        )
        print(f"05_build_features_and_splits: aborted: {exc}", file=sys.stderr)
        return 1

    completed = _registry_row(run_id, status="completed", lock_hash=lock_hash, snapshot=snapshot)
    completed["code_commit"] = lock.code_commit
    completed["artifact_manifest_path"] = summary["split_manifest"]
    append_registry_event(
        registry_path,
        completed,
        phase=args.phase,
        writer_role="stage",
        access_log_path=access_log,
    )
    print(f"05_build_features_and_splits: completed: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
