"""Stage script 06: train and predict -- six families, three seeds, the stamp match, the receipt.

Purpose
-------
The seventh of the nine phase-aware stage scripts (TE 12/13.2; `services.md`: reads
`FeatureBundle`s and partitions, writes per-seed predictions, the three-seed mean and
checkpoints). It ORCHESTRATES `src/models` (W-1, W-2, W-3, W-6, W-7, W-12; R-90 ... R-102a):

* `assert_stamp_match` runs BEFORE EVERY scoring path (R-90): a frame whose spec is not
  `(partition k, role "score")`, or whose transform is not k's own, never reaches k's scoring.
* Per FOLD partition, M-01 ... M-05 once and M-06 once per configured final seed; the three
  M-06 predictions are averaged by `three_seed_mean` with `expected_seeds` read from
  `ConfigSnapshot.seeds` HERE, at the call site (R-91, R-93) -- never inlined. A fold fit
  names its own score bundle as the explicit `validation_bundle`: on a fold the two
  legitimately coincide, and naming it is what keeps them from coinciding on `DEC`.
* The grid content is asserted against config before any fit (R-96), and every grid point a
  family is given is a member of that grid.
* The ONE-SHOT `DEC` write (W-12; R-102a; SD-M-04): write the prediction file once; hash it
  as written; durably flush the `PredictionHashReceipt` (`.tmp` -> fsync -> atomic rename);
  append the registry row carrying `prediction_hash` at TE 13.4's column 18; and REFUSE TO
  EXIT (`LockedTestError`) unless both the rename and the append succeeded.

REFIT fits and persists; DEC loads and predicts (owner ruling, 2026-09-20)
--------------------------------------------------------------------------
The refit is no longer skipped and December no longer fits anything:

* **`REFIT`** is a FIT-AND-PERSIST iteration. It is scored nowhere (FR-P1-04-14), so it has
  no score bundle and produces no prediction; what it produces is a persisted, SHA-256-hashed
  fitted model per fitted family (and per final seed for M-06) plus a `FittedModelRecord`
  naming the payload and its hash. The M-06 refit trains for the frozen epoch count that
  `models.refit.epochs` carries -- the value `train.REFIT_EPOCH_RULE_ID` produced from the
  pre-December folds -- with no validation set and no early stopping, so nothing is selected
  at refit time. Before this change the loop `continue`d here and the Jan-Nov refit was never
  fitted standalone at all.
* **`DEC`** is a LOAD-AND-PREDICT iteration. The fitted families reach it only through
  `train.predict_from_fitted`, which re-verifies the persisted payload's hash and calls the
  family's `predict_rows_from_state`; `model.fit` does not appear anywhere on that path, and
  `train.assert_not_locked_fit` raises `LeakageError` if any future caller reaches for a fit
  there. M-01 and M-02 carry no fitted state and are recomputed from the locked target
  series as before. December therefore never influences training, early stopping, checkpoint
  selection or model selection (Vision 8.3).

What this script can and cannot run today
-----------------------------------------
* **It REFUSES, honestly, before any model is fitted**: the released Phase 1 target manifest
  and the bundle root's `split_manifest.json` do not exist (no feature bundle has ever been
  produced -- `05` refuses at the unset permitted-producer list), so the run writes an
  `aborted` registry row naming the first absent input.
* **`DEC` requires the G-05 signature.** The locked path is implemented in full but enters
  ONLY through `materialise_locked_partition(snapshot, g05_signature=...)`, which refuses
  without a verifying G-05 signature (R-82, ADR-03); `--partition DEC` is not in the default
  list and additionally requires `--g05-signature`, `--locked-input` and
  `--locked-authorization`. This script never names the restricted root -- the loader routes
  the human-supplied path through `governance-guards`' `open_restricted`, the one door. The
  frame the door RETURNS is the `DEC` iteration's target (`_locked_target`); the released
  January-November target loaded before the partition loop is refused on that branch by
  identity, so the access-logged read is the data the receipt's prediction was computed from
  (R-102a; SD-M-04; W-12).
* **The TensorFlow pin is FROZEN at `tensorflow==2.21.0` (D-36) and `require_frozen_pin`
  PASSES.** What stops an M-06 run here is the ENVIRONMENT, not the guard: TensorFlow has
  never been installed or imported on this clone (PyPI unreachable), TE 8.1's both-platform
  check has not run, and TA-26 stays `Pending`. Separately, this script supplies no
  `CheckpointBackend`, so M-06 refuses for that reason too. M-04/M-05 refuse by name without
  `scikit-learn` installed.
* **Persisting M-04, M-05 and M-06 refuses by design.** `train.JsonStateBackend` serves any
  family whose fitted state is JSON-serialisable (M-03's mean table is). A fitted
  scikit-learn estimator and a set of Keras weights are not, and choosing a binary
  serialization format for them is a governed decision that does not exist yet (TS-M-01
  freezes the Keras checkpoint format at pin-freeze). The refusal names that, rather than
  reaching for pickle.

Inputs
------
`--config configs/`; `--phase 1|2`; `--partition` (repeatable; default F1..F4, REFIT; `DEC`
permitted only with the three locked-path arguments); `--horizon` (default: the single
default-list entry of `experiment.horizons`); `--bundles-root` (default `artifacts/features`);
`--predictions-out` (default `artifacts/predictions`); `--fitted-models-root` (default
`artifacts/models`, where the REFIT persist writes and the DEC load reads); `--code-commit`.

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
from typing import Any, Final

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
from src.data.fixture_evidence import stamp_fixture_artifact, stamp_for_manifest  # noqa: E402
from src.data.fixture_gate import require_receipts_for_snapshot  # noqa: E402
from src.data.fixture_manifest import (  # noqa: E402
    MEASUREMENTS_NAME,
    build_apparatus_partitions,
    load_fixture_scope,
    read_embargo_hours,
    release_root_for,
)
from src.data.locked_test import (  # noqa: E402
    PERSISTENCE_HISTORY_CALLERS,
    AccessRecord,
    open_restricted,
    read_persistence_history_lookup,
)
from src.data.phase_contract import assert_no_raw_fields, assert_phase_boundary  # noqa: E402
from src.data.release import verify_release  # noqa: E402
from src.data.splits import (  # noqa: E402
    FITTING_PARTITION_IDS,
    LOCKED_ID,
    PARTITION_IDS,
    REFIT_ID,
    Partition,
    PartitionKind,
    RecordFrame,
    build_partitions,
    materialise_locked_partition,
    partition_by_id,
    training_range,
    validation_month_range,
)
from src.features._frames import frame_attrs, frame_from_records, records_of  # noqa: E402
from src.features.build import FrameSpec, bundle_directory_name, load_bundle  # noqa: E402
from src.features.transforms import transform_id_for  # noqa: E402
from src.models.train import (  # noqa: E402
    FITTED_MODEL_IDS,
    GRID_TRACKS,
    MODEL_IDS,
    TBD_SENTINEL,
    CandidateScore,
    JsonStateBackend,
    Prediction,
    assert_grid_content,
    assert_in_grid,
    assert_locked_exit_allowed,
    assert_stamp_match,
    enumerate_grid,
    expected_transform_id,
    fit_and_persist,
    fit_predict,
    load_fitted_model,
    mean_per_fold_skill,
    predict_from_fitted,
    resolve_horizon,
    select_configuration,
    target_series,
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
    "climatology_key",
    "climatology_limitation",
    "training_rows_excluded_missing_label",
    "fitted_partition_id",
    "fitted_model_partition_id",
    "fitted_model_sha256",
    "payload_ref",
    "payload_sha256",
    "fitted_at_utc",
    "inference_only",
    "checkpoint_selected",
    "epoch_source",
    "restored_epoch",
    "epochs_run",
    "validation_partition_id",
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
    parser.add_argument(
        "--fitted-models-root",
        type=Path,
        default=Path("artifacts/models"),
        help=(
            "workspace-relative root where the REFIT fit persists its hashed models and "
            "fitted-model records, and where the DEC iteration loads them from"
        ),
    )
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
    parser.add_argument(
        "--fixture-manifest",
        type=Path,
        default=None,
        help=(
            "the walking-skeleton fixture scope (a fixture manifest or identity declaration, "
            "validated through the one loader). When given, this run is a FIXTURE run: the "
            "apparatus partitions are built from the scope's declaration (never a frozen id, "
            "R-137), every prediction payload is stamped, no locked path exists, and the "
            "TE 9.2 two-receipt gate is exempt (Q4/Q5 = A). Additive edit flagged for "
            "`models-and-baselines`' record (fixtures-and-reproducibility CR-2026-09-07)"
        ),
    )
    parser.add_argument(
        "--tune",
        action="store_true",
        help=(
            "run D-124's selection (mean per-fold skill vs the declared baseline, per grid "
            "track) over the fixture's own apparatus folds instead of a governed fit/predict "
            "run. FIXTURE-SCALE ONLY (requires --fixture-manifest): proves the selection "
            "mechanism on real fixture data without writing the governed models.selected "
            "field, which only a full-year F1-F4 run may freeze (build-and-test item 3)"
        ),
    )
    parser.add_argument(
        "--probe",
        action="store_true",
        help=(
            "with --tune: run exactly one LSTM candidate on exactly one apparatus fold, for "
            "timing before committing to the full grid sweep"
        ),
    )
    parser.add_argument(
        "--tune-out",
        type=Path,
        default=None,
        help="where --tune writes its result JSON (default: under --predictions-out)",
    )
    args = parser.parse_args(argv)
    if args.fixture_manifest is not None and args.partition:
        parser.error(
            "--fixture-manifest runs the manifest's declared apparatus partitions; a frozen "
            "--partition id alongside it is a contradiction (R-137's two-way quarantine)"
        )
    if args.tune and args.fixture_manifest is None:
        parser.error(
            "--tune runs at fixture scale only, per the owner's resolution of the fixture / "
            "models.selected deadlock (build-and-test item 3): it needs --fixture-manifest"
        )
    if args.probe and not args.tune:
        parser.error("--probe only means something with --tune")
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
        # The fixture scope this run is bound to, or None for a governed run. Carried on
        # the entry because it selects the RELEASE ROOT this stage reads from (owner ruling
        # 2026-09-23): a fixture run reads the fixture's own releases, a governed run reads
        # the governed ones, and neither can reach the other's.
        "fixture_scope_id": (
            load_fixture_scope(fixture_manifest).fixture_id
            if fixture_manifest is not None
            else None
        ),
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
    run_id: str,
    *,
    status: str,
    lock_hash: str,
    snapshot: Any,
    code_commit: str,
    reason: str = "",
    **columns: Any,
) -> dict[str, Any]:
    now = dt.datetime.now(dt.timezone.utc).isoformat()
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


#: The released target CSV's columns this loader reads. Superset of `train.py`'s three
#: TARGET_* identities (`interval_start_utc`, `station_id`, `vtec_tecu`) plus the three
#: NFR-TDEF-01 identity stamps every downstream frame is asserted to carry.
_TARGET_COLUMNS: Final[tuple[str, ...]] = (
    "interval_start_utc",
    "station_id",
    "vtec_tecu",
    "target_valid",
    "phase_id",
    "source_id",
    "target_definition_id",
)


def _load_target_by_manifest(snapshot: Any, *, fixture_scope_id: str | None) -> Any:
    """The released Phase 1 hourly target, read BY MANIFEST from the release root.

    An upstream unit's artifact (`target-standardization`). A missing release refuses.
    `verify_release` re-derives the manifest's own claims (required §13.3 fields, every
    declared output file's SHA-256, and R-11's content-hash/dataset_version correspondence)
    before a single byte is trusted (TE §13.3) -- the same check `test_release_hashes.py`
    runs, called here rather than duplicated. Only rows with `target_valid == "True"` are
    kept; a QC-invalid row is dropped, never imputed (D-5).

    Implemented 2026-09-25 (build-and-test item 3, Student's explicit instruction). Before
    this the function refused unconditionally, even once the release existed on disk --
    the reason no prediction has ever been written for `plumbing_7day`, fixture or
    governed. See `governance/CHANGE_RECORD_2026-09-25_target_loader_implementation.md`.
    """
    # Owner ruling 2026-09-23: ONE resolver for the release root. On a fixture run the
    # releases live under the walking-skeleton root, so this stage reads the fixture's
    # own releases and never a governed citation (and vice versa). The directory name
    # below is unchanged: it is the contract three stages resolve literally.
    release_root = release_root_for(
        Path(snapshot.resolved_roots["workspace"]),
        artifacts_root=Path(snapshot.resolved_roots["artifacts"]),
        fixture_id=fixture_scope_id,
    )
    release_dir = release_root / "phase1_hourly_target"
    manifest = release_dir / "release_manifest.json"
    if not manifest.is_file():
        raise IntegrityError(
            manifest,
            "no released Phase 1 hourly target manifest; labels are read from a released target "
            "by manifest and hash, never from a bare path (TE 13.3)",
        )
    problems = verify_release(manifest)
    if problems:
        raise IntegrityError(
            manifest,
            "the released target manifest does not verify (TE 13.3; R-11): " + "; ".join(problems),
        )
    parsed = json.loads(manifest.read_text(encoding="utf-8"))
    output_files = parsed.get("output_files")
    if not isinstance(output_files, Mapping) or not output_files:
        raise IntegrityError(manifest, "output_files is absent or empty after verification")
    records: list[dict[str, Any]] = []
    for rel_path in sorted(output_files):
        csv_path = release_dir / rel_path
        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if str(row.get("target_valid", "")).strip() != "True":
                    continue  # D-5: a QC-invalid row is dropped, never imputed
                records.append({name: row.get(name) for name in _TARGET_COLUMNS})
    if not records:
        raise IntegrityError(
            manifest, "the released target carries zero rows with target_valid == 'True'"
        )
    return frame_from_records(records, columns=_TARGET_COLUMNS)


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


def _fixture_bundle_root(snapshot: Any, args: argparse.Namespace) -> Path:
    """The fixture-scale bundle root, validated against 05's ACTUAL fixture output by name
    (`apparatus_split_manifest.json` — board Rec 4 / ML-03, owner-authorised per
    CR-2026-09-07 §11.5; never the five-row confirmatory `split_manifest.json`, whose ids
    are quarantined from every fixture artifact, R-137)."""
    root = Path(snapshot.resolved_roots["workspace"]) / args.bundles_root
    manifest = root / "apparatus_split_manifest.json"
    if not manifest.is_file():
        raise IntegrityError(
            manifest,
            "no apparatus split manifest under the fixture bundle root; the fixture path "
            "reads what 05's fixture path actually wrote (apparatus_split_manifest.json), "
            "by name, never the confirmatory split manifest (board Rec 4 / ML-03; R-137's "
            "two-way quarantine)",
        )
    return root


def _bundle_pair(
    root: Path, partition: Partition, partitions: Sequence[Partition]
) -> tuple[Any, Any]:
    """The train bundle a family is fitted on and the score bundle it predicts on.

    For `DEC` the fit bundle is `REFIT`'s train bundle and the score bundle carries `REFIT`'s
    transform -- the one enumerated G-06 apply (R-74). The `DEC` score bundle is produced by
    `05 --partition DEC`, behind the same G-05 signature guard.

    The score slot is `None` for `REFIT` alone, and that is the truthful answer: the final
    refit is scored nowhere (FR-P1-04-14), so there is no score-role bundle to load and
    fabricating one would contradict the split manifest. What changed on 2026-09-20 is the
    CALLER: `_run` no longer treats a `None` score slot as "skip this partition". It routes
    `REFIT` to the fit-and-persist branch, which is the only producer of the model the `DEC`
    iteration loads.
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


def _model_registry_rows(
    run_id: str,
    *,
    lock_hash: str,
    snapshot: Any,
    code_commit: str,
    registry_path: Path,
    access_log: Path,
    phase: int,
    model_id: str,
    seed: int | None,
    fold_id: str,
    hyperparameters: Mapping[str, Any] | None,
    manifest_path: Path,
) -> None:
    """One `started` + `completed` pair for an artifact that is not a prediction — the
    REFIT's persisted fitted model. Each seed is its own registry run (TE 13.5)."""
    child_id = f"{run_id}/{fold_id}/{model_id}" + (f"/seed{seed}" if seed is not None else "")
    common = {
        "fold_id": fold_id,
        "model_id": model_id,
        "seed": "" if seed is None else seed,
        "hyperparameters_json": json.dumps(
            dict(hyperparameters or {}), sort_keys=True, default=str
        ),
        "locked_test_accessed": False,
    }
    for status, manifest in (("started", None), ("completed", manifest_path)):
        row = _registry_row(
            child_id, status=status, lock_hash=lock_hash, snapshot=snapshot,
            code_commit=code_commit,
            artifact_manifest_path="" if manifest is None else str(manifest),
            **common,
        )
        append_registry_event(
            registry_path, row, phase=phase, writer_role=WRITER_ROLE, access_log_path=access_log
        )


def _fitted_record_path(models_root: Path, model_id: str, seed: int | None) -> Path:
    """Where the REFIT persist writes a family's fitted-model record and the DEC load finds
    it. One file per (model, seed): each seed is its own run (TE 13.5)."""
    suffix = "" if seed is None else f"_seed{seed}"
    return Path(models_root) / f"{model_id}{suffix}.fitted_record.json"


def _refit_and_persist(
    *,
    snapshot: Any,
    partition: Partition,
    train_bundle: Any,
    refit_target: Any,
    horizon: int,
    expected_seeds: frozenset[int],
    models_root: Path,
) -> list[tuple[str, int | None, Any, Path]]:
    """The REFIT iteration: FIT on January-November and PERSIST, hashed. Nothing is scored.

    Every fitted family is refitted from scratch on the refit partition's training range and
    written through `JsonStateBackend`, which hashes the payload as written. M-06 is refitted
    once per configured final seed, each seed its own persisted model and its own registry
    run (TE 13.5), for exactly the frozen `models.refit.epochs` count with no validation set
    — so no epoch, checkpoint or hyperparameter is selected here and December cannot reach
    one. `validation_bundle=None` is the refit contract, asserted by
    `train.assert_validation_bundle`.

    M-01 and M-02 are skipped: they carry no fitted state and are recomputed from the target
    series wherever they are scored.
    """
    backend = JsonStateBackend(models_root)
    persisted: list[tuple[str, int | None, Any, Path]] = []
    for model_id in MODEL_IDS:
        if model_id not in FITTED_MODEL_IDS:
            continue
        params = _selected_params(snapshot, model_id)
        seeds: tuple[int | None, ...] = (
            tuple(sorted(expected_seeds)) if model_id == "M-06" else (None,)
        )
        for seed in seeds:
            record_path = _fitted_record_path(models_root, model_id, seed)
            record = fit_and_persist(
                model_id,
                bundle=train_bundle,
                partition=partition,
                snapshot=snapshot,
                target=refit_target,
                backend=backend,
                record_path=record_path,
                validation_bundle=None,  # the refit selects nothing (frozen epoch count)
                seed=seed,
                params=params,
                horizon_hours=horizon,
            )
            persisted.append((model_id, seed, record, record_path))
    return persisted


def _persistence_history_augmented_target(
    *,
    locked_target: Any,
    model_id: str,
    snapshot: Any,
    run_id: str | None,
    g05_signature: str | None,
    locked_input: Path | None,
    access_log: Path | None,
) -> Any:
    """D-28 option (b) / D-68 (2026-09-24): for M-01/M-02 ONLY, append 2022-12-01 lookup
    history to the December target rows `fit_predict` reads -- never rows inside the scored
    window, never for any other model.

    `locked_target` itself (the embargo-trimmed frame `materialise_locked_partition`
    returned) is NEVER mutated or re-scored from; this builds a SEPARATE, augmented copy
    handed only to `fit_predict`'s `target=` for this one call, exactly as
    `src.data.locked_test.read_persistence_history_lookup`'s own docstring specifies. If any
    of `g05_signature` / `locked_input` / `access_log` is absent (mirrors the same
    all-or-nothing precondition `materialise_locked_partition` itself already enforces via
    `args.g05_signature and args.locked_input and args.locked_authorization` at this script's
    own argument-parsing stage), or if D-68's own kill switch in `configs/experiment.yaml`
    is not authorized, this raises rather than silently falling back to the unaugmented
    frame -- an unauthorized-but-silent skip would misreport why the scored set came up
    short, which is exactly what D-28's Recommendation 15 disclosure guard exists to catch.
    """
    if model_id not in PERSISTENCE_HISTORY_CALLERS:
        return locked_target
    if g05_signature is None or locked_input is None or access_log is None:
        raise LockedTestError(
            f"_persistence_history_augmented_target({model_id})",
            "g05_signature / locked_input / access_log incomplete; the December iteration "
            "for M-01/M-02 requires all three to attempt the D-68 lookup, mirroring the "
            "same all-or-nothing precondition this script already enforces for the DEC "
            "partition itself",
        )
    if run_id is None or not str(run_id).strip():
        raise LockedTestError(
            f"_persistence_history_augmented_target({model_id})",
            "run_id absent; every persistence_history access row must be attributable to "
            "the governed run that made it by key, never by timestamp correlation "
            "(NFR-AUD-01; Rec 10 of GOV-2026-09-24-BT-01)",
        )

    def _raw_december_loader() -> Any:
        return _read_target_artifact(Path(locked_input))

    lookup = read_persistence_history_lookup(
        snapshot,
        model_id=model_id,
        run_id=run_id,
        g05_signature=g05_signature,
        path=Path(locked_input),
        loader=_raw_december_loader,
        registry=access_log,
    )
    extra_rows = [
        {
            "interval_start_utc": stamp.isoformat(),
            "station_id": station,
            "vtec_tecu": value,
        }
        for (station, stamp), value in lookup.items()
    ]
    return RecordFrame([*records_of(locked_target), *extra_rows])


def _locked_predictions(
    *,
    snapshot: Any,
    partition: Partition,
    train_bundle: Any,
    score_bundle: Any,
    locked_target: Any,
    horizon: int,
    expected_seeds: frozenset[int],
    models_root: Path,
    run_id: str | None = None,
    g05_signature: str | None = None,
    locked_input: Path | None = None,
    access_log: Path | None = None,
) -> tuple[list[Prediction], list[Prediction]]:
    """The DEC iteration: LOAD the persisted REFIT models and PREDICT. Nothing fits here.

    A fitted family reaches December ONLY through `predict_from_fitted`, which re-verifies
    the persisted payload against the hash recorded when it was written and dispatches to the
    family's `predict_rows_from_state`. An absent record RAISES rather than falling back to a
    fit: a fit reached from this branch is December in the training loop (Vision 8.3).
    M-01 and M-02 carry no fitted state and are recomputed from the locked target series.

    `g05_signature`/`locked_input`/`access_log` (added 2026-09-24, D-28 option (b) / D-68):
    when all three are supplied, M-01/M-02 additionally receive the D-68-authorized
    2022-12-01 lookup history via `_persistence_history_augmented_target`, recovering the
    full D-28/D-59 30-day scored set. Every other family, and M-01/M-02 when any of the
    three is omitted, is unaffected -- `locked_target` itself passes through unchanged.
    """
    backend = JsonStateBackend(models_root)
    produced: list[Prediction] = []
    seeded: list[Prediction] = []
    for model_id in MODEL_IDS:
        seeds: tuple[int | None, ...] = (
            tuple(sorted(expected_seeds)) if model_id == "M-06" else (None,)
        )
        model_target = (
            _persistence_history_augmented_target(
                locked_target=locked_target,
                model_id=model_id,
                snapshot=snapshot,
                run_id=run_id,
                g05_signature=g05_signature,
                locked_input=locked_input,
                access_log=access_log,
            )
            if model_id in PERSISTENCE_HISTORY_CALLERS
            else locked_target
        )
        for seed in seeds:
            assert_stamp_match(score_bundle, partition)  # R-90: before EVERY scoring path
            if model_id in FITTED_MODEL_IDS:
                record_path = _fitted_record_path(models_root, model_id, seed)
                record = load_fitted_model(record_path)  # raises: no persisted refit model
                if record.model_id != model_id or record.fitted_partition_id != REFIT_ID:
                    raise LockedTestError(
                        record_path,
                        f"records model {record.model_id!r} fitted on "
                        f"{record.fitted_partition_id!r}; the locked iteration predicts with "
                        f"the {model_id} model fitted on {REFIT_ID} and nothing else "
                        f"(Vision 8.3; TE 7.0B)",
                    )
                prediction = predict_from_fitted(
                    record,
                    score_bundle=score_bundle,
                    partition=partition,
                    snapshot=snapshot,
                    backend=backend,
                    target=locked_target,
                    horizon_hours=horizon,
                )
            else:
                prediction = fit_predict(
                    model_id,
                    bundle=train_bundle,
                    partition=partition,
                    snapshot=snapshot,
                    target=model_target,
                    score_bundle=score_bundle,
                    seed=seed,
                    params=None,
                    horizon_hours=horizon,
                )
            if model_id == "M-06":
                seeded.append(prediction)
            produced.append(prediction)
    return produced, seeded


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
            retrieved_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
            scope=f"{locked.partition_id} {locked.validation_month.isoformat()} locked evaluation",
            purpose="locked_evaluation",
            performance_inspected=False,
            locked_test_accessed=True,
            authorization=str(args.locked_authorization),
        )
        opened = open_restricted(Path(args.locked_input), record=record, registry=access_log)
        return _read_target_artifact(Path(opened))

    return loader


def _locked_target(
    snapshot: Any,
    *,
    g05_signature: str | None,
    loader,
    partitions: Sequence[Partition],
    released_target: Any,
) -> Any:
    """The `DEC` iteration's target: the frame the one door RETURNS, and nothing else.

    `materialise_locked_partition` refuses without a verifying G-05 signature (R-82), then
    calls `loader` (which routes through `open_restricted`, writing the `AccessRecord`) and
    returns the locked month with its embargo excluded and counted. That returned frame is
    the ONLY target the locked scoring may consume: the `AccessRecord` asserts a
    `locked_evaluation` read, so the prediction the receipt hashes must be computed from
    exactly what that read produced (R-102a; SD-M-04; W-12). The released January–November
    target loaded before the partition loop is refused here by IDENTITY, so nothing from it
    can reach `DEC` scoring.

    Raises
    ------
    LockedTestError
        the guard's own refusals; a loader returning nothing; a loader returning the
        pre-loop released target object.
    """
    def _guarded_loader(partition: Partition) -> Any:
        frame = loader(partition)
        if frame is released_target:
            raise LockedTestError(
                f"partition {LOCKED_ID}",
                "the locked loader handed back the pre-loop released target object; the DEC "
                "iteration scores ONLY the frame the one door returns, and the access-logged "
                "read must be the data the receipt's prediction was computed from "
                "(R-102a; SD-M-04; W-12)",
            )
        return frame

    loaded = materialise_locked_partition(
        snapshot, g05_signature=g05_signature, loader=_guarded_loader, partitions=partitions
    )
    if loaded is None:
        raise LockedTestError(
            f"partition {LOCKED_ID}",
            "the locked loader returned no frame; the DEC prediction is computed from the frame "
            "the one door returned, never from an absent or substituted target (W-12)",
        )
    if loaded is released_target:
        raise LockedTestError(
            f"partition {LOCKED_ID}",
            "the DEC target IS the pre-loop released target object; the locked iteration scores "
            "the frame open_restricted returned through materialise_locked_partition, and the "
            "access-logged read must be the data the receipt's prediction was computed from "
            "(R-102a; SD-M-04)",
        )
    return loaded


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


def _run_fixture_scale(
    entry: Mapping[str, Any], args: argparse.Namespace, *, run_id: str
) -> dict[str, Any]:
    """Q4 = A (fixtures-and-reproducibility R-137): the fixture-scale path, additive only.

    The SAME per-partition fit/predict sequence as the full-year path, but over the
    APPARATUS partitions the fixture scope declares (never a frozen id — the loader refuses
    one, control 15), with the fixture stamp embedded in every prediction payload and
    `apparatus_partition_id` carried on each. NO locked path exists here: an apparatus
    partition is never `locked` (R-137; R-82), so no G-05 argument, no `open_restricted`,
    no receipt writer is reachable. The governed reads are unchanged (horizon, grids,
    seeds, the released target by manifest), so today this path refuses exactly where the
    full-year path does (TE 18.3, stop and report).

    Board Rec 4 (ML-03, owner-authorised per CR-2026-09-07 §11.5; flagged for
    `models-and-baselines`' record): the fixture bundle root is validated against 05's
    ACTUAL fixture output (`apparatus_split_manifest.json`, by name — never the five-row
    confirmatory `split_manifest.json`); predictions land DIRECTLY under
    `--predictions-out` (no per-run segment), so the orchestrator's `--predictions-run`
    hand-off to 07 is deterministic and a re-run refuses at the write-once prediction
    rather than forking a second tree; and a machine-readable measurement block
    (`fixture_measurements.json`, scored prediction rows) is emitted under the predictions
    root for the orchestrator to fold into candidate measurements.
    """
    _assert_phase1_field_contract(args.phase)
    _assert_registry_column_18()
    snapshot = entry["snapshot"]
    lock = entry["lock"]
    lock_hash = environment_lock_hash(lock)
    registry_path, access_log = _registry_paths(snapshot)
    workspace = Path(snapshot.resolved_roots["workspace"])
    scope = load_fixture_scope(Path(args.fixture_manifest))

    horizon = resolve_horizon(snapshot, args.horizon)
    grid_counts = assert_grid_content(snapshot)
    expected_seeds = _final_seeds(snapshot)

    partitions = build_apparatus_partitions(scope, embargo_hours=read_embargo_hours(snapshot))
    bundle_root = _fixture_bundle_root(snapshot, args)  # 05's apparatus manifest, by name
    fixture_target = _load_target_by_manifest(snapshot, fixture_scope_id=entry.get("fixture_scope_id"))  # the fixture-scale released target
    out_root = workspace / args.predictions_out  # deterministic: no per-run segment (Rec 4)

    written: list[str] = []
    scored_rows: list[int] = []
    for partition in partitions:
        pid = partition.partition_id
        stamp = stamp_for_manifest(scope, apparatus_partition_id=pid)
        train_bundle, score_bundle = _bundle_pair(bundle_root, partition, partitions)
        if score_bundle is None:
            continue  # an apparatus refit is scored nowhere, like the frozen one
        assert_stamp_match(score_bundle, partition)  # R-90: before EVERY scoring path
        seeded: list[Prediction] = []
        for model_id in MODEL_IDS:
            seeds: tuple[int | None, ...] = (
                tuple(sorted(expected_seeds)) if model_id == "M-06" else (None,)
            )
            params = _selected_params(snapshot, model_id)
            for seed in seeds:
                assert_stamp_match(score_bundle, partition)
                prediction = fit_predict(
                    model_id,
                    bundle=train_bundle,
                    partition=partition,
                    snapshot=snapshot,
                    target=fixture_target,  # the fixture-scale target; no locked path exists
                    score_bundle=score_bundle,
                    # apparatus folds mirror the frozen folds: the scored bundle IS the
                    # validation bundle here, named rather than implied
                    validation_bundle=score_bundle,
                    seed=seed,
                    params=params,
                    horizon_hours=horizon,
                )
                if model_id == "M-06":
                    seeded.append(prediction)
                name = f"{model_id}" + (f"_seed{seed}" if seed is not None else "") + ".json"
                path = _write_prediction_once(
                    out_root / pid / name,
                    stamp_fixture_artifact(
                        _prediction_payload(prediction, horizon_hours=horizon), stamp
                    ),
                )
                _child_rows(
                    run_id, lock_hash=lock_hash, snapshot=snapshot,
                    code_commit=lock.code_commit, registry_path=registry_path,
                    access_log=access_log, phase=args.phase, prediction=prediction,
                    manifest_path=path,
                )
                written.append(str(path))
        confirmatory = three_seed_mean(seeded, expected_seeds=expected_seeds)
        path = _write_prediction_once(
            out_root / pid / "M-06_confirmatory.json",
            stamp_fixture_artifact(
                _prediction_payload(confirmatory, horizon_hours=horizon), stamp
            ),
        )
        _child_rows(
            run_id, lock_hash=lock_hash, snapshot=snapshot, code_commit=lock.code_commit,
            registry_path=registry_path, access_log=access_log, phase=args.phase,
            prediction=confirmatory, manifest_path=path,
        )
        written.append(str(path))
        scored_rows.append(len(records_of(confirmatory.frame)))
    if scored_rows:  # Rec 4: measurable here — scored prediction rows per partition
        measurements_path = out_root / MEASUREMENTS_NAME
        measurements_path.parent.mkdir(parents=True, exist_ok=True)
        measurements_path.write_text(
            json.dumps(
                {
                    "stage": "06_train_and_predict",
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
    return {"horizon_hours": horizon, "grid_counts": grid_counts, "predictions_written": written}


# =======================================================================================
# --tune: D-124's selection at fixture scale (build-and-test item 3)
# =======================================================================================


class _InMemoryCheckpointBackend:
    """A `CheckpointBackend` (`src/models/checkpoint.py`) that holds per-epoch weights in a
    dict for the lifetime of one fold fit, never on disk. Fold-fit checkpointing has no
    approved persistence format (`TS-M-01` freezes the REFIT format only, and this is never
    a refit) -- this is scratch state for `checkpoint.restore` to pick from, discarded when
    the candidate's fold fit returns."""

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}
        self._next = 0

    def save(self, *, epoch: int, weights: Any) -> str:
        ref = f"epoch-{epoch}-{self._next}"
        self._next += 1
        self._store[ref] = weights
        return ref

    def load(self, payload_ref: str) -> Any:
        return self._store[payload_ref]


#: PROPOSED complexity ordering for R-101's "prefer the simpler configuration within the
#: margin" rule -- no governed record (functional design, business rules, or a change
#: record) states a formula. Lower is simpler. Flagged as proposed, not committed; the
#: owner may replace it without touching the selection mechanism itself.
def _proposed_complexity(track: str, params: Mapping[str, Any]) -> float:
    if track == "ridge":
        return 1.0 / float(params["alpha"])  # smaller alpha = less regularised = more complex
    if track == "random_forest":
        depth = params["max_depth"]
        depth_factor = 32.0 if depth is None else float(depth)
        return float(params["n_estimators"]) * depth_factor
    if track == "lstm":
        return float(params["layers"]) * float(params["units"])
    raise IntegrityError(f"grid track {track!r}", "no complexity proxy defined")


def _rmse(
    prediction: Prediction, series: Mapping[tuple[str, dt.datetime], float]
) -> tuple[float, dict[str, int]]:
    """RMSE of one prediction against the D-17 target series, matched on
    `(station, interval_start_utc)`. Two classes of row are dropped, never imputed (D-5),
    both non-fatal completeness shortfalls rather than errors: a row the target series has
    no value for, and a row whose own `y_hat` is a legitimate MISSING marker -- `None` or
    `NaN` -- which M-01/M-02 emit by design when a fold's short training window carries no
    history at the required lag (`src/models/persistence.py`). A silently-NaN RMSE (found
    on this script's first real run, plumbing_7day, FIX-NOV-FOLD-01) is exactly the
    unflagged-shortfall failure mode `team.md`'s two-tier posture forbids."""
    squared_errors: list[float] = []
    dropped_missing_prediction = 0
    dropped_missing_target = 0
    for row in records_of(prediction.frame):
        y_hat = row["y_hat"]
        if y_hat is None or (isinstance(y_hat, float) and y_hat != y_hat):  # None or NaN
            dropped_missing_prediction += 1
            continue
        station = str(row["station"])
        ts = dt.datetime.fromisoformat(str(row["interval_start_utc"]).replace("Z", "+00:00"))
        target_value = series.get((station, ts))
        if target_value is None:
            dropped_missing_target += 1
            continue
        squared_errors.append((float(y_hat) - target_value) ** 2)
    if not squared_errors:
        raise IntegrityError(
            f"prediction {prediction.model_id}/{prediction.partition_id}",
            f"no row matched the target series (dropped {dropped_missing_prediction} missing "
            f"y_hat, {dropped_missing_target} missing target); RMSE over zero rows is not a "
            f"measurement",
        )
    rmse = (sum(squared_errors) / len(squared_errors)) ** 0.5
    dropped = {
        "missing_prediction": dropped_missing_prediction,
        "missing_target": dropped_missing_target,
        "scored_rows": len(squared_errors),
    }
    return rmse, dropped


def _fit_candidate(
    *,
    track: str,
    model_id: str,
    params: Mapping[str, Any],
    train_bundle: Any,
    score_bundle: Any,
    partition: Partition,
    snapshot: Any,
    target: Any,
    horizon: int,
    seed: int,
) -> Prediction:
    """Fit-then-predict one grid point on one apparatus fold.

    Ridge and Random Forest go through the approved generic `fit_predict` (`train.py`).
    LSTM does NOT: `fit_predict`'s approved signature carries no `CheckpointBackend`
    parameter, so it can never reach a fold's best-checkpoint restoration (R-94) -- a real,
    separate gap in the generic dispatcher, disclosed here rather than routed around
    silently (see `governance/CHANGE_RECORD_2026-09-25_target_loader_implementation.md`
    § "A second gap found, not fixed"). LSTM is fit by calling its family module directly,
    exactly as `fit_predict` would if it forwarded a backend.
    """
    if track != "lstm":
        return fit_predict(
            model_id,
            bundle=train_bundle,
            partition=partition,
            snapshot=snapshot,
            target=target,
            score_bundle=score_bundle,
            validation_bundle=score_bundle,
            seed=None,
            params=params,
            horizon_hours=horizon,
        )
    from src.models import lstm as _lstm  # lazy import (R-05); TF loads only when reached

    return _lstm.fit_predict_rows(
        model_id,
        bundle=train_bundle,
        score_bundle=score_bundle,
        partition=partition,
        snapshot=snapshot,
        target=target,
        seed=seed,
        params=params,
        horizon_hours=horizon,
        validation_bundle=score_bundle,
        backend=_InMemoryCheckpointBackend(),
    )


def _run_tune(entry: Mapping[str, Any], args: argparse.Namespace, *, run_id: str) -> dict[str, Any]:
    """D-124's selection rule (R-101), over the fixture's own apparatus folds.

    FIXTURE SCALE ONLY. Writes nothing to `configs/experiment.yaml`: this session's job is
    to prove the selection mechanism runs against real (if fixture-scale) data, never to
    freeze a governed value, which only the Student may do, from a full January-November
    F1-F4 run (`project.md` § Forbidden). The result file is advisory and clearly labelled;
    nothing here is copied into `models.selected` or `models.refit.epochs` by this script.
    """
    _assert_phase1_field_contract(args.phase)
    snapshot = entry["snapshot"]
    scope = load_fixture_scope(Path(args.fixture_manifest))
    embargo_hours = read_embargo_hours(snapshot)
    partitions = build_apparatus_partitions(scope, embargo_hours=embargo_hours)
    fold_partitions = [p for p in partitions if p.kind == PartitionKind.fold]
    if not fold_partitions:
        raise IntegrityError(
            args.fixture_manifest, "the fixture declares no apparatus fold partitions to tune on"
        )

    horizon = resolve_horizon(snapshot, args.horizon)
    grid_counts = assert_grid_content(snapshot)  # R-96: config grid content before any fit
    bundle_root = _fixture_bundle_root(snapshot, args)
    target = _load_target_by_manifest(snapshot, fixture_scope_id=entry.get("fixture_scope_id"))
    series = target_series(target)
    final_seeds = sorted(_final_seeds(snapshot))

    baseline_block = snapshot.experiment.get("models", {}).get("declared_baseline_per_track")
    baseline = baseline_block.get("all_tracks") if isinstance(baseline_block, Mapping) else None
    if baseline != "persistence":
        raise IntegrityError(
            "configs/experiment.yaml: models.declared_baseline_per_track.all_tracks",
            f"is {baseline!r}, not 'persistence' -- D-58 names the only baseline this script "
            f"knows how to score against (TE line 456: M-01 is Persistence)",
        )
    baseline_model_id = "M-01"

    if args.probe:
        tracks = ("lstm",)
        fold_partitions = fold_partitions[:1]
    else:
        tracks = tuple(GRID_TRACKS)

    print(
        f"06_train_and_predict --tune: {len(tracks)} track(s), "
        f"{len(fold_partitions)} apparatus fold(s), probe={args.probe}"
    )

    per_track_results: dict[str, Any] = {}
    all_candidate_audit: list[dict[str, Any]] = []
    for track in tracks:
        model_id = GRID_TRACKS[track]
        candidates = list(enumerate_grid(snapshot, track))
        if args.probe:
            candidates = candidates[:1]
        print(f"  track={track} model_id={model_id} candidates={len(candidates)}")

        scored: list[CandidateScore] = []
        for params in candidates:
            fold_skill: dict[str, float] = {}
            for fold in fold_partitions:
                assert_in_grid(snapshot, track, params)
                train_bundle, score_bundle = _bundle_pair(bundle_root, fold, partitions)
                if score_bundle is None:
                    continue
                assert_stamp_match(score_bundle, fold)
                seed = final_seeds[0] if model_id == "M-06" else None
                t0 = dt.datetime.now(dt.timezone.utc)
                prediction = _fit_candidate(
                    track=track, model_id=model_id, params=params,
                    train_bundle=train_bundle, score_bundle=score_bundle, partition=fold,
                    snapshot=snapshot, target=target, horizon=horizon, seed=seed or 0,
                )
                baseline_prediction = fit_predict(
                    baseline_model_id, bundle=train_bundle, partition=fold, snapshot=snapshot,
                    target=target, score_bundle=score_bundle, validation_bundle=score_bundle,
                    seed=None, params=None, horizon_hours=horizon,
                )
                elapsed = (dt.datetime.now(dt.timezone.utc) - t0).total_seconds()
                rmse_model, dropped_model = _rmse(prediction, series)
                rmse_baseline, dropped_baseline = _rmse(baseline_prediction, series)
                skill = 1.0 - (rmse_model / rmse_baseline)
                fold_skill[fold.partition_id] = skill
                print(
                    f"    {track} {params} fold={fold.partition_id} "
                    f"rmse={rmse_model:.4f} skill={skill:.4f} ({elapsed:.1f}s) "
                    f"dropped_model={dropped_model} dropped_baseline={dropped_baseline}"
                )
                all_candidate_audit.append(
                    {
                        "track": track, "params": dict(params), "fold_id": fold.partition_id,
                        "rmse": rmse_model, "baseline_rmse": rmse_baseline, "skill": skill,
                        "seconds": elapsed, "dropped_rows_model": dropped_model,
                        "dropped_rows_baseline": dropped_baseline,
                    }
                )
            if fold_skill:
                scored.append(
                    CandidateScore(
                        params=params, fold_skill=fold_skill,
                        complexity=_proposed_complexity(track, params),
                    )
                )
        if args.probe:
            per_track_results[track] = {"probe_only": True, "candidates_run": len(scored)}
            continue
        winner = select_configuration(
            scored, snapshot=snapshot,
            fold_ids=[f.partition_id for f in fold_partitions],
        )
        per_track_results[track] = {
            "params": dict(winner.params),
            "mean_skill": mean_per_fold_skill(
                winner, fold_ids=[f.partition_id for f in fold_partitions]
            ),
            "fold_skill": dict(winner.fold_skill),
            "candidates_evaluated": len(scored),
        }

    result = {
        "advisory": True,
        "governed": False,
        "note": (
            "FIXTURE-SCALE selection, not a governed F1-F4 run. Never copy directly into "
            "configs/experiment.yaml: models.selected without a real full-year tuning pass "
            "(project.md § Forbidden; build-and-test item 3)."
        ),
        "fixture_id": scope.fixture_id if hasattr(scope, "fixture_id") else None,
        "run_id": run_id,
        "probe": args.probe,
        "apparatus_fold_ids": [f.partition_id for f in fold_partitions],
        "horizon_hours": horizon,
        "grid_counts": grid_counts,
        "declared_baseline": baseline,
        "per_track": per_track_results,
        "candidate_audit": all_candidate_audit,
    }

    out_path = args.tune_out
    if out_path is None:
        workspace = Path(snapshot.resolved_roots["workspace"])
        out_path = workspace / args.predictions_out / "tuning" / "tuning_result.json"
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True, default=str), encoding="utf-8")
    print(f"06_train_and_predict --tune: wrote {out_path}")

    return {"tune_result_path": str(out_path), "tracks_run": list(tracks), "probe": args.probe}


def _run(entry: Mapping[str, Any], args: argparse.Namespace, *, run_id: str) -> dict[str, Any]:
    if args.tune:
        return _run_tune(entry, args, run_id=run_id)  # fixture-scale D-124 selection only
    if args.fixture_manifest is not None:
        return _run_fixture_scale(entry, args, run_id=run_id)  # Q4 = A: the ONE fixture entry
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
    released_target = _load_target_by_manifest(snapshot, fixture_scope_id=entry.get("fixture_scope_id"))  # January–November; never DEC's
    out_root = workspace / args.predictions_out / run_id
    models_root = workspace / args.fitted_models_root

    written: list[str] = []
    locked_models_predicted = 0
    for pid in args.partitions:
        partition = partition_by_id(partitions, pid)
        # The bundles load FIRST, so a missing DEC bundle refuses before any locked read is
        # made: an access-logged open of the restricted root is a custody event and is not
        # spent discovering that `05 --partition DEC` never ran.
        train_bundle, score_bundle = _bundle_pair(bundle_root, partition, partitions)
        if pid == LOCKED_ID:
            # The ONE door: refuses without a verifying G-05 signature (R-82) before any read,
            # and the frame it RETURNS is the DEC iteration's target -- the pre-loop released
            # target is refused by identity (R-102a; SD-M-04; W-12).
            partition_target = _locked_target(
                snapshot,
                g05_signature=args.g05_signature,
                loader=_locked_loader(args, run_id=run_id, access_log=access_log),
                partitions=partitions,
                released_target=released_target,
            )
        else:
            partition_target = released_target

        if pid == REFIT_ID:
            # FIT AND PERSIST. The refit is scored nowhere (FR-P1-04-14) so it writes no
            # prediction -- but it is NOT skipped: the hashed model it persists here is the
            # ONLY model the DEC iteration is allowed to predict with (Vision 8.3).
            for model_id, seed, record, record_path in _refit_and_persist(
                snapshot=snapshot,
                partition=partition,
                train_bundle=train_bundle,
                refit_target=partition_target,
                horizon=horizon,
                expected_seeds=expected_seeds,
                models_root=models_root,
            ):
                _model_registry_rows(
                    run_id, lock_hash=lock_hash, snapshot=snapshot,
                    code_commit=lock.code_commit, registry_path=registry_path,
                    access_log=access_log, phase=args.phase, model_id=model_id, seed=seed,
                    fold_id=pid, hyperparameters=record.hyperparameters,
                    manifest_path=record_path,
                )
                written.append(str(record_path))
            continue

        if score_bundle is None:
            raise IntegrityError(
                f"partition {pid}",
                "carries no score-role bundle; only the final refit is scored nowhere "
                "(FR-P1-04-14) and it is handled on its own branch — a silently skipped "
                "partition is how the refit went unfitted",
            )
        assert_stamp_match(score_bundle, partition)  # R-90: before EVERY scoring path
        seeded: list[Prediction] = []
        if pid == LOCKED_ID:
            # LOAD AND PREDICT. No fitted family is fitted here; `assert_not_locked_fit`
            # makes that a LeakageError rather than a convention.
            produced, seeded = _locked_predictions(
                snapshot=snapshot,
                partition=partition,
                train_bundle=train_bundle,
                score_bundle=score_bundle,
                locked_target=partition_target,
                horizon=horizon,
                expected_seeds=expected_seeds,
                models_root=models_root,
                run_id=run_id,
                g05_signature=args.g05_signature,
                locked_input=Path(args.locked_input) if args.locked_input else None,
                access_log=access_log,
            )
            locked_models_predicted = len(produced)
        else:
            for model_id in MODEL_IDS:
                seeds: tuple[int | None, ...] = (
                    tuple(sorted(expected_seeds)) if model_id == "M-06" else (None,)
                )
                params = _selected_params(snapshot, model_id)  # refuses while selected is TBD
                for seed in seeds:
                    assert_stamp_match(score_bundle, partition)
                    prediction = fit_predict(
                        model_id,
                        bundle=train_bundle,
                        partition=partition,
                        snapshot=snapshot,
                        target=partition_target,
                        score_bundle=score_bundle,
                        # on a FOLD the validation bundle and the scored bundle legitimately
                        # coincide; naming it is what stops them coinciding on DEC
                        validation_bundle=score_bundle,
                        seed=seed,
                        params=params,
                        horizon_hours=horizon,
                    )
                    if model_id == "M-06":
                        seeded.append(prediction)
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
    return {
        "horizon_hours": horizon,
        "grid_counts": grid_counts,
        "predictions_written": written,
        "locked_models_predicted": locked_models_predicted,
    }


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
        print(f"06_train_and_predict: preflight refusal: {exc}", file=sys.stderr)
        return 1

    snapshot = entry["snapshot"]
    lock = entry["lock"]
    lock_hash = environment_lock_hash(lock)
    registry_path, access_log = _registry_paths(snapshot)
    run_id = (
        f"models-and-baselines-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
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
