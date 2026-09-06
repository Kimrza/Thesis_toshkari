"""Stage script 06: train and predict -- six families, three seeds, the stamp match, the receipt.

Purpose
-------
The seventh of the nine phase-aware stage scripts (TE 12/13.2; `services.md`: reads
`FeatureBundle`s and partitions, writes per-seed predictions, the three-seed mean and
checkpoints). It ORCHESTRATES `src/models` (W-1, W-2, W-3, W-6, W-7, W-12; R-90 ... R-102a):

* `assert_stamp_match` runs BEFORE EVERY scoring path (R-90): a frame whose spec is not
  `(partition k, role "score")`, or whose transform is not k's own, never reaches k's scoring.
* Per fitting-capable partition, M-01 ... M-05 once and M-06 once per configured final seed;
  the three M-06 predictions are averaged by `three_seed_mean` with `expected_seeds` read from
  `ConfigSnapshot.seeds` HERE, at the call site (R-91, R-93) -- never inlined.
* The grid content is asserted against config before any fit (R-96), and every grid point a
  family is given is a member of that grid.
* The ONE-SHOT `DEC` write (W-12; R-102a; SD-M-04): write the prediction file once; hash it
  as written; durably flush the `PredictionHashReceipt` (`.tmp` -> fsync -> atomic rename);
  append the registry row carrying `prediction_hash` at TE 13.4's column 18; and REFUSE TO
  EXIT (`LockedTestError`) unless both the rename and the append succeeded.

What this script can and cannot run today
-----------------------------------------
* **It REFUSES, honestly, before any model is fitted**: the released Phase 1 target manifest
  and the bundle root's `split_manifest.json` do not exist (no feature bundle has ever been
  produced -- `05` refuses at the unset permitted-producer list), so the run writes an
  `aborted` registry row naming the first absent input. Behind that, `experiment.horizons` is
  not transcribed yet and `read_horizons` refuses naming it (TE 2.1; R-99).
* **`DEC` is UNREACHABLE.** The locked path is implemented in full but enters ONLY through
  `materialise_locked_partition(snapshot, g05_signature=...)`, which refuses without a
  verifying G-05 signature (R-82, ADR-03); `--partition DEC` is not in the default list and
  additionally requires `--g05-signature`, `--locked-input` and `--locked-authorization`. No
  December content is read by any path this script can reach today, and this script never
  names the restricted root -- the loader routes the human-supplied path through
  `governance-guards`' `open_restricted`, the one door.
* M-06's Keras path refuses at the TensorFlow pin guard (FU-1 = C); M-04/M-05 refuse by name
  without `scikit-learn` installed.

Inputs
------
`--config configs/`; `--phase 1|2`; `--partition` (repeatable; default F1..F4, REFIT; `DEC`
permitted only with the three locked-path arguments); `--horizon` (default: the single
default-list entry of `experiment.horizons`); `--bundles-root` (default `artifacts/features`);
`--predictions-out` (default `artifacts/predictions`); `--code-commit`.

Re-run behaviour
----------------
Each run appends its own `started` and terminal rows (append-only, R-08/R-09; aborted runs
stay visible, NFR-AUD-01), plus one `started`/`completed` pair per (partition, model, seed)
child run -- each seed is its own registry run (TE 13.5; D-122). Prediction files are never
overwritten; the `DEC` file and its receipt are written exactly once.

Boundaries this script holds
----------------------------
* Step 1 of the entry contract is `ensure_process_determinism`; `assert_phase_boundary` is
  step 4; `assert_no_raw_fields` runs BEFORE the first write (R-23/R-24).
* Imports nothing under `src/external/iri.py`, `src/external/gim.py`, `src/gnss/` or
  `src/evaluation/`; `tensorflow` only through `src/models/lstm.py`'s guard.
* No scientific constant: seeds, grids, settings, horizons and ablations are configuration.
* `prior_period_exposure` is NOT written here (R-102a's deviation box; `foundation` R-18).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
import uuid
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import (  # noqa: E402
    IntegrityError,
    LockedTestError,
    SeedError,
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
    REGISTRY_COLUMNS,
    append_registry_event,
    record_abort_honestly,
)
from src.data.locked_test import AccessRecord, open_restricted  # noqa: E402
from src.data.phase_contract import assert_no_raw_fields, assert_phase_boundary  # noqa: E402
from src.data.splits import (  # noqa: E402
    FITTING_PARTITION_IDS,
    LOCKED_ID,
    PARTITION_IDS,
    REFIT_ID,
    Partition,
    RecordFrame,
    build_partitions,
    materialise_locked_partition,
    partition_by_id,
    training_range,
    validation_month_range,
)
from src.features._frames import frame_attrs, records_of  # noqa: E402
from src.features.build import FrameSpec, bundle_directory_name, load_bundle  # noqa: E402
from src.features.transforms import transform_id_for  # noqa: E402
from src.models.train import (  # noqa: E402
    GRID_TRACKS,
    MODEL_IDS,
    TBD_SENTINEL,
    Prediction,
    assert_grid_content,
    assert_in_grid,
    assert_locked_exit_allowed,
    assert_stamp_match,
    expected_transform_id,
    fit_predict,
    resolve_horizon,
    three_seed_mean,
    write_prediction_hash_receipt,
)

STAGE = "models-and-baselines"
PHASE_DEFAULT = 1
WRITER_ROLE = "train"  # R-18: the receipt's writer; `evaluate` and `bootstrap` may not be
PREDICTION_HASH_COLUMN = "prediction_hash"
PREDICTION_HASH_COLUMN_ORDINAL = 18  # TE 13.4's eighteenth column of twenty (R-102a)

#: The artifact field names this run can produce, screened through R-23's produced-field limb
#: BEFORE the first write (R-24).
PRODUCED_FIELDS: tuple[str, ...] = (
    "station",
    "interval_start_utc",
    "y_hat",
    "model_id",
    "seed",
    "partition_id",
    "transform_id",
    "phase_id",
    "source_id",
    "target_definition_id",
    "horizon_hours",
    "hyperparameters",
    "confirmatory",
    "seeds_averaged",
    "rows",
    "prediction_path",
    "sha256",
    "recorded_at_utc",
    "run_id",
    "fitted_partitions",
    "fitted_role",
    "missing_source_values",
    "missing_climatology_keys",
    "training_rows_excluded_missing_label",
)


def _assert_phase1_field_contract(phase: int) -> None:
    """R-24: the produced-field guard, called before this run's first write."""
    assert_no_raw_fields(PRODUCED_FIELDS, phase=phase)


def _assert_registry_column_18() -> None:
    """R-102a: `prediction_hash` is TE 13.4's eighteenth column; asserted, not assumed."""
    ordinal = REGISTRY_COLUMNS.index(PREDICTION_HASH_COLUMN) + 1
    if ordinal != PREDICTION_HASH_COLUMN_ORDINAL:
        raise IntegrityError(
            "src/data/experiment_registry.py: REGISTRY_COLUMNS",
            f"{PREDICTION_HASH_COLUMN!r} is column {ordinal}, not "
            f"{PREDICTION_HASH_COLUMN_ORDINAL} (TE 13.4; R-102a); the receipt's sha256 must "
            f"land on the eighteenth column",
        )


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="06_train_and_predict.py",
        description=(
            "Train and predict (P1-05): six families over the fitting-capable partitions, the "
            "three-seed confirmatory mean, and the one-shot DEC write behind the G-05 signature "
            "guard. REFUSES today before any fit (no released target, no bundles, horizons "
            "untranscribed)."
        ),
    )
    parser.add_argument(
        "--config", required=True, type=Path, help="the governed configs directory"
    )
    parser.add_argument("--phase", type=int, choices=(1, 2), default=PHASE_DEFAULT)
    parser.add_argument(
        "--partition",
        action="append",
        choices=PARTITION_IDS,
        default=None,
        help=(
            "partition(s) to run (repeatable; default the five fitting-capable ones). DEC is "
            "NOT in the default list and runs only through the locked path (G-05 signature)"
        ),
    )
    parser.add_argument("--horizon", type=int, default=None, help="forecast horizon in hours")
    parser.add_argument("--bundles-root", type=Path, default=Path("artifacts/features"))
    parser.add_argument("--predictions-out", type=Path, default=Path("artifacts/predictions"))
    parser.add_argument("--code-commit", type=str, default=None)
    parser.add_argument(
        "--g05-signature",
        type=str,
        default=None,
        help="the G-05 signature artifact; DEC materialises only when it verifies (R-82)",
    )
    parser.add_argument(
        "--locked-input",
        type=Path,
        default=None,
        help="the December target artifact, opened ONLY through locked_test.open_restricted",
    )
    parser.add_argument(
        "--locked-authorization",
        type=str,
        default=None,
        help="the authorization the AccessRecord carries (the G-05 decision record)",
    )
    args = parser.parse_args(argv)
    wanted = tuple(args.partition) if args.partition else FITTING_PARTITION_IDS
    if LOCKED_ID in wanted and not (
        args.g05_signature and args.locked_input and args.locked_authorization
    ):
        parser.error(
            "--partition DEC requires --g05-signature, --locked-input and "
            "--locked-authorization; the locked path enters only through the G-05 guard"
        )
    args.partitions = wanted
    return args


def _stage_entry(config_dir: Path, *, phase: int, code_commit: str | None) -> dict[str, Any]:
    """Steps 2-6 of the stage entry contract (step 1, determinism, ran in main())."""
    snapshot = load_configs(config_dir, phase=phase)
    assert_no_tbd(snapshot, required=required_fields_for(STAGE, PHASE_DEFAULT))
    assert_declared_sources_exist(snapshot)
    assert_phase_boundary(phase, loaded_modules=sys.modules)
    determinism = seed_everything(snapshot, stage=STAGE)
    lock = capture_environment_lock(snapshot, determinism, code_commit=code_commit)
    assert_lock_complete(lock)
    return {"snapshot": snapshot, "determinism": determinism, "lock": lock}


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
    run_id: str,
    *,
    status: str,
    lock_hash: str,
    snapshot: Any,
    code_commit: str,
    reason: str = "",
    **columns: Any,
) -> dict[str, Any]:
    now = dt.datetime.now(dt.UTC).isoformat()
    row: dict[str, Any] = {
        "run_id": run_id,
        "started_at_utc": now,
        "completed_at_utc": now if status in ("completed", "aborted", "failed") else "",
        "status": status,
        "code_commit": code_commit,
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
        PREDICTION_HASH_COLUMN: "",
        "locked_test_accessed": False,
        "notes": "models-and-baselines run (P1-05); DEC only through the G-05 signature guard",
    }
    row.update(columns)
    if reason:
        row["reason"] = reason
    return row


# =======================================================================================
# Inputs by manifest
# =======================================================================================


def _load_target_by_manifest(snapshot: Any) -> Any:
    """The released Phase 1 hourly target, read BY MANIFEST from the release root.

    An upstream unit's artifact (`target-standardization`). A missing release refuses; and the
    loader itself is reached only after every governed value upstream is frozen -- none is
    today -- so this stops here rather than defaulting a reader (TE 18.3), exactly as `05` does.
    """
    release_root = Path(snapshot.resolved_roots.get("release_root", ""))
    manifest = release_root / "phase1_hourly_target" / "release_manifest.json"
    if not manifest.is_file():
        raise IntegrityError(
            manifest,
            "no released Phase 1 hourly target manifest; labels are read from a released target "
            "by manifest and hash, never from a bare path (TE 13.3)",
        )
    raise IntegrityError(
        manifest,
        "reading the released target into a frame is reached only after the permitted-producer "
        "list, the partitions, the availability lags and the horizons are frozen; none is "
        "today, so this path stops here rather than defaulting a loader (TE 18.3)",
    )


def _bundle_root(snapshot: Any, args: argparse.Namespace) -> Path:
    root = Path(snapshot.resolved_roots["workspace"]) / args.bundles_root
    manifest = root / "split_manifest.json"
    if not manifest.is_file():
        raise IntegrityError(
            manifest,
            "no split manifest under the bundle root; bundles are read by manifest (FR-P1-04-5), "
            "and none has been produced (05 refuses at the unset permitted-producer list)",
        )
    return root


def _bundle_pair(
    root: Path, partition: Partition, partitions: Sequence[Partition]
) -> tuple[Any, Any]:
    """The train bundle a family is fitted on and the score bundle it predicts on.

    For `DEC` the fit bundle is `REFIT`'s train bundle and the score bundle carries `REFIT`'s
    transform -- the one enumerated G-06 apply (R-74).
    """
    fit_partition = partition
    if partition.partition_id == LOCKED_ID:
        fit_partition = partition_by_id(partitions, REFIT_ID)
    tid = expected_transform_id(partition)
    if transform_id_for(fit_partition.partition_id) != tid:
        raise IntegrityError(
            f"partition {partition.partition_id}",
            f"its own transform {tid!r} is not the fit partition's {fit_partition.partition_id!r}",
        )
    start, end = training_range(fit_partition)
    train_dir = root / bundle_directory_name(
        FrameSpec(fit_partition.partition_id, "train", start, end), tid
    )
    if partition.validation_month is None:
        return load_bundle(train_dir), None
    s_start, s_end = validation_month_range(partition)
    score_dir = root / bundle_directory_name(
        FrameSpec(partition.partition_id, "score", s_start, s_end), tid
    )
    return load_bundle(train_dir), load_bundle(score_dir)


# =======================================================================================
# Writes
# =======================================================================================


def _selected_params(snapshot: Any, model_id: str) -> Mapping[str, Any] | None:
    """The SELECTED grid point for a fitted family, from `experiment.models.selected.<track>`.

    R-101: selection is on mean per-fold skill over F1–F4 and the refit changes no
    hyperparameter; the selected configuration is frozen before G-05 (TE 7.0B). While the
    block is `TBD — freeze gate` this REFUSES naming the field — a grid point picked here
    would be a selection with no record. M-01..M-03 have no hyperparameters (`None`).
    """
    track = next((t for t, mid in GRID_TRACKS.items() if mid == model_id), None)
    if track is None:
        return None
    models = snapshot.experiment.get("models")
    selected = models.get("selected") if isinstance(models, Mapping) else None
    if selected is None or (isinstance(selected, str) and selected.strip() == TBD_SENTINEL):
        raise IntegrityError(
            "configs/experiment.yaml: models.selected",
            f"absent or unresolved (TBD — freeze gate); {model_id}'s grid point is the tuning "
            f"run's SELECTED configuration (R-101, mean per-fold skill over F1–F4, refit "
            f"unchanged), frozen before G-05 — never picked here by convenience (TE 18.3)",
        )
    if not isinstance(selected, Mapping) or track not in selected:
        raise IntegrityError(
            f"configs/experiment.yaml: models.selected.{track}", "no selected grid point recorded"
        )
    params = selected[track]
    if not isinstance(params, Mapping):
        raise IntegrityError(
            f"configs/experiment.yaml: models.selected.{track}", "must be a mapping of the axes"
        )
    assert_in_grid(snapshot, track, params)  # R-96: the selection is a member of the grid
    return dict(params)


def _prediction_payload(prediction: Prediction, *, horizon_hours: int) -> dict[str, Any]:
    attrs = frame_attrs(prediction.frame)
    return {
        "model_id": prediction.model_id,
        "seed": prediction.seed,
        "partition_id": prediction.partition_id,
        "transform_id": prediction.transform_id,
        "phase_id": prediction.phase_id,
        "source_id": prediction.source_id,
        "target_definition_id": prediction.target_definition_id,
        "horizon_hours": horizon_hours,
        "hyperparameters": attrs.get("hyperparameters"),
        "confirmatory": bool(attrs.get("confirmatory", False)),
        "seeds_averaged": attrs.get("seeds_averaged"),
        "rows": records_of(prediction.frame),
    }


def _write_prediction_once(path: Path, payload: Mapping[str, Any]) -> Path:
    """Write-once: an existing prediction file is never overwritten (TE 13.3; R-102a step 1)."""
    path = Path(path)
    if path.exists():
        raise LockedTestError(
            path,
            "prediction file already exists; predictions are generated and written exactly once "
            "and never regenerated after a score is seen (FR-P1-05-12; R-102a)",
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str), encoding="utf-8")
    return path


def _child_rows(
    run_id: str,
    *,
    lock_hash: str,
    snapshot: Any,
    code_commit: str,
    registry_path: Path,
    access_log: Path,
    phase: int,
    prediction: Prediction,
    manifest_path: Path,
    prediction_hash: str = "",
    locked: bool = False,
) -> bool:
    """One `started` + `completed` pair per (partition, model, seed): each seed is its own
    registry run (TE 13.5). Returns True only when BOTH appends returned."""
    child_id = f"{run_id}/{prediction.partition_id}/{prediction.model_id}" + (
        f"/seed{prediction.seed}" if prediction.seed is not None else ""
    )
    common = {
        "fold_id": prediction.partition_id,
        "model_id": prediction.model_id,
        "seed": "" if prediction.seed is None else prediction.seed,
        "hyperparameters_json": json.dumps(
            frame_attrs(prediction.frame).get("hyperparameters") or {}, sort_keys=True, default=str
        ),
        "locked_test_accessed": locked,
    }
    started = _registry_row(
        child_id, status="started", lock_hash=lock_hash, snapshot=snapshot,
        code_commit=code_commit, **common,
    )
    append_registry_event(
        registry_path, started, phase=phase, writer_role=WRITER_ROLE, access_log_path=access_log
    )
    completed = _registry_row(
        child_id, status="completed", lock_hash=lock_hash, snapshot=snapshot,
        code_commit=code_commit, artifact_manifest_path=str(manifest_path),
        **{PREDICTION_HASH_COLUMN: prediction_hash}, **common,
    )
    append_registry_event(
        registry_path, completed, phase=phase, writer_role=WRITER_ROLE, access_log_path=access_log
    )
    return True


def _final_seeds(snapshot: Any) -> frozenset[int]:
    """`seeds.final` read from `ConfigSnapshot.seeds` at the CALL SITE (R-91; BLK-03)."""
    raw = snapshot.seeds.get("final")
    if not isinstance(raw, list | tuple) or not raw:
        raise SeedError(
            "configs/seeds.yaml: seeds.final",
            "missing or empty; the confirmatory seeds are D-122's and reach three_seed_mean as a "
            "parameter from configuration, never inlined (TC-03e)",
        )
    seeds = frozenset(int(s) for s in raw if not isinstance(s, bool))
    if len(seeds) != len(raw):
        raise SeedError("configs/seeds.yaml: seeds.final", "carries a duplicate or non-integer")
    return seeds


# =======================================================================================
# The locked path (W-12): reachable ONLY through the G-05 signature guard
# =======================================================================================


def _read_target_artifact(path: Path) -> Any:
    """Read a target artifact (`.jsonl` or `.csv`) that `open_restricted` has ALREADY logged.

    This is the only reader the locked loader uses; it is reached only with a path that the
    chokepoint returned, so this script never constructs a restricted path itself.
    """
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    elif suffix == ".csv":
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
    else:
        raise IntegrityError(path, f"unsupported target artifact suffix {suffix!r}")
    return RecordFrame(rows)


def _locked_loader(args: argparse.Namespace, *, run_id: str, access_log: Path):
    def loader(locked: Partition) -> Any:
        record = AccessRecord(
            run_id=run_id,
            retrieved_at_utc=dt.datetime.now(dt.UTC).isoformat(),
            scope=f"{locked.partition_id} {locked.validation_month.isoformat()} locked evaluation",
            purpose="locked_evaluation",
            performance_inspected=False,
            locked_test_accessed=True,
            authorization=str(args.locked_authorization),
        )
        opened = open_restricted(Path(args.locked_input), record=record, registry=access_log)
        return _read_target_artifact(Path(opened))

    return loader


def _finish_locked_write(
    *,
    prediction_path: Path,
    payload: Mapping[str, Any],
    run_id: str,
    receipt_path: Path,
    append_row,
) -> None:
    """W-12 steps 1-4 in order: write once; hash as written + receipt (`.tmp` -> fsync ->
    rename); registry append carrying `prediction_hash` at column 18; then REFUSE TO EXIT
    unless rename AND append both succeeded (`LockedTestError`).

    `append_row(sha256) -> bool` is the registry append, injected so the exit refusal can be
    exercised on a synthetic fixture without a registry.
    """
    _write_prediction_once(prediction_path, payload)
    receipt = write_prediction_hash_receipt(
        prediction_path, run_id=run_id, partition_id=str(payload["partition_id"]),
        receipt_path=receipt_path,
    )
    appended = False
    try:
        appended = bool(append_row(receipt.sha256))
    except IntegrityError as exc:
        print(f"06_train_and_predict: registry append failed: {exc}", file=sys.stderr)
        appended = False
    assert_locked_exit_allowed(
        prediction_path, receipt_path=receipt_path, registry_appended=appended
    )


# =======================================================================================
# The run
# =======================================================================================


def _run(entry: Mapping[str, Any], args: argparse.Namespace, *, run_id: str) -> dict[str, Any]:
    _assert_phase1_field_contract(args.phase)  # R-24: before the first write, always
    _assert_registry_column_18()
    snapshot = entry["snapshot"]
    lock = entry["lock"]
    lock_hash = environment_lock_hash(lock)
    registry_path, access_log = _registry_paths(snapshot)
    workspace = Path(snapshot.resolved_roots["workspace"])

    # 1. Config-only preconditions: the horizon (R-99) and the grid content (R-96).
    horizon = resolve_horizon(snapshot, args.horizon)
    grid_counts = assert_grid_content(snapshot)
    expected_seeds = _final_seeds(snapshot)  # the call site reads ConfigSnapshot.seeds (R-91)

    # 2. Inputs by manifest -- refuse honestly while none exists.
    partitions = build_partitions(snapshot)
    bundle_root = _bundle_root(snapshot, args)
    target = _load_target_by_manifest(snapshot)
    out_root = workspace / args.predictions_out / run_id

    written: list[str] = []
    for pid in args.partitions:
        partition = partition_by_id(partitions, pid)
        if pid == LOCKED_ID:
            # The ONE door: refuses without a verifying G-05 signature (R-82) before any read.
            materialise_locked_partition(
                snapshot,
                g05_signature=args.g05_signature,
                loader=_locked_loader(args, run_id=run_id, access_log=access_log),
                partitions=partitions,
            )
        train_bundle, score_bundle = _bundle_pair(bundle_root, partition, partitions)
        if score_bundle is None:
            continue  # the final refit is scored nowhere (FR-P1-04-14)
        assert_stamp_match(score_bundle, partition)  # R-90: before EVERY scoring path
        seeded: list[Prediction] = []
        for model_id in MODEL_IDS:
            seeds: tuple[int | None, ...] = (
                tuple(sorted(expected_seeds)) if model_id == "M-06" else (None,)
            )
            params = _selected_params(snapshot, model_id)  # refuses while models.selected is TBD
            for seed in seeds:
                assert_stamp_match(score_bundle, partition)
                prediction = fit_predict(
                    model_id,
                    bundle=train_bundle,
                    partition=partition,
                    snapshot=snapshot,
                    target=target,
                    score_bundle=score_bundle,
                    seed=seed,
                    params=params,
                    horizon_hours=horizon,
                )
                if model_id == "M-06":
                    seeded.append(prediction)
                if pid != LOCKED_ID:
                    name = f"{model_id}" + (f"_seed{seed}" if seed is not None else "") + ".json"
                    path = _write_prediction_once(
                        out_root / pid / name,
                        _prediction_payload(prediction, horizon_hours=horizon),
                    )
                    _child_rows(
                        run_id, lock_hash=lock_hash, snapshot=snapshot,
                        code_commit=lock.code_commit, registry_path=registry_path,
                        access_log=access_log, phase=args.phase, prediction=prediction,
                        manifest_path=path,
                    )
                    written.append(str(path))
        confirmatory = three_seed_mean(seeded, expected_seeds=expected_seeds)
        if pid == LOCKED_ID:
            prediction_path = out_root / pid / "M-06_confirmatory.json"
            receipt_path = out_root / pid / "M-06_confirmatory.receipt.json"

            def _append(sha256: str, _p: Prediction = confirmatory, _path: Path = prediction_path):
                return _child_rows(
                    run_id, lock_hash=lock_hash, snapshot=snapshot, code_commit=lock.code_commit,
                    registry_path=registry_path, access_log=access_log, phase=args.phase,
                    prediction=_p, manifest_path=_path, prediction_hash=sha256, locked=True,
                )

            _finish_locked_write(
                prediction_path=prediction_path,
                payload=_prediction_payload(confirmatory, horizon_hours=horizon),
                run_id=run_id,
                receipt_path=receipt_path,
                append_row=_append,
            )
            written.append(str(prediction_path))
        else:
            path = _write_prediction_once(
                out_root / pid / "M-06_confirmatory.json",
                _prediction_payload(confirmatory, horizon_hours=horizon),
            )
            _child_rows(
                run_id, lock_hash=lock_hash, snapshot=snapshot, code_commit=lock.code_commit,
                registry_path=registry_path, access_log=access_log, phase=args.phase,
                prediction=confirmatory, manifest_path=path,
            )
            written.append(str(path))
    return {"horizon_hours": horizon, "grid_counts": grid_counts, "predictions_written": written}


def main() -> int:
    ensure_process_determinism(sys.argv)  # FIRST statement, before any framework import
    args = _parse_args(sys.argv[1:])

    try:
        entry = _stage_entry(args.config, phase=args.phase, code_commit=args.code_commit)
    except IntegrityError as exc:
        print(f"06_train_and_predict: preflight refusal: {exc}", file=sys.stderr)
        return 1

    snapshot = entry["snapshot"]
    lock = entry["lock"]
    lock_hash = environment_lock_hash(lock)
    registry_path, access_log = _registry_paths(snapshot)
    run_id = (
        f"models-and-baselines-{dt.datetime.now(dt.UTC).strftime('%Y%m%dT%H%M%SZ')}"
        f"-{uuid.uuid4().hex[:8]}"
    )

    started = _registry_row(
        run_id, status="started", lock_hash=lock_hash, snapshot=snapshot,
        code_commit=lock.code_commit,
    )
    append_registry_event(
        registry_path, started, phase=args.phase, writer_role=WRITER_ROLE,
        access_log_path=access_log,
    )

    try:
        summary = _run(entry, args, run_id=run_id)
    except IntegrityError as exc:
        aborted = _registry_row(
            run_id, status="aborted", lock_hash=lock_hash, snapshot=snapshot,
            code_commit=lock.code_commit, reason=str(exc),
        )
        record_abort_honestly(
            registry_path, aborted, phase=args.phase, writer_role=WRITER_ROLE,
            access_log_path=access_log, original_error=exc,
        )
        print(f"06_train_and_predict: aborted: {exc}", file=sys.stderr)
        return 1

    completed = _registry_row(
        run_id, status="completed", lock_hash=lock_hash, snapshot=snapshot,
        code_commit=lock.code_commit,
    )
    append_registry_event(
        registry_path, completed, phase=args.phase, writer_role=WRITER_ROLE,
        access_log_path=access_log,
    )
    print(f"06_train_and_predict: completed: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
