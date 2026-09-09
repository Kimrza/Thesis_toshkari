"""Stage script 07: evaluate and report -- masks, estimands, the metrics artifact, one door to DEC.

Purpose
-------
The eighth of the nine phase-aware stage scripts (TE 12/13.2; `services.md`: reads
predictions carrying `partition_id`/`transform_id`, the benchmark and the mask; writes
metrics). It ORCHESTRATES `src/evaluation` (W-1, W-2, W-5, W-6, W-7; R-103 ... R-112) --
every governed check lives in `src/evaluation/{guards,masks,metrics}.py`, none inline here
(section 7: scripts are orchestrators precisely so governed checks do not live in them):

* Per declared comparison set (`experiment.comparison_sets`, confirmed Q1 = A under
  `governance/CHANGE_RECORD_2026-09-06_R106_comparison_sets.md`): read the members'
  predictions BY MANIFEST from a `06` predictions run, build the ONE comparison-wide
  intersection mask (stamps first, membership exact, matched windows), register it once,
  compute `paired_loss_differential` per (model, benchmark) pair, and emit the
  `MetricsArtifact` -- refused unless complete and disclosing (R-110).
* Bootstrap intervals and breakdown tables are NOT computed here: they are
  `statistical-inference`'s and `regimes-diagnostics-reporting`'s, running inside this
  script later per the boundary note (the path grant, R-56; no unit-level narrowing).

What this script can and cannot run today
-----------------------------------------
* **It REFUSES, honestly, before any mask is built**: no `06` predictions run exists (no
  feature bundle has ever been produced, so `06` refuses upstream), and the released
  Phase 1 target manifest does not exist -- the run writes an `aborted` registry row naming
  the first absent input (R-01/R-10; NFR-AUD-01).
* **`DEC` is UNREACHABLE.** The locked path is implemented in full but enters ONLY through
  `materialise_locked_partition(snapshot, g05_signature=...)` -- which refuses without a
  verifying G-05 signature (R-82) -- and `governance-guards`' `open_restricted` with purpose
  `"locked_evaluation"` and the G-05 signature reference in `AccessRecord.authorization`
  (R-109 limb 2; R-25 log-then-read; R-28's one door). `--partition DEC` additionally
  requires `--g05-signature`, `--locked-input`, `--locked-authorization` and
  `--mask-bundle-manifest`. G-05 is `Blocked`, so no December content is readable by any
  path this script can reach today; this script never names the restricted root.
* Every `DEC` metric additionally refuses at `require_locked_receipt` without a verifying
  prediction-hash receipt, the SD-C-02 containment fields on the access record, and the
  D-28 scored window (redundancy at the locked boundary is by design -- the one event that
  can never be re-run).

Inputs
------
`--config configs/`; `--phase 1|2`; `--predictions-run` (a `06` output directory, read by
manifest); `--partition` (repeatable; default the four folds plus REFIT-scored sets found;
`DEC` only with the four locked-path arguments); `--set` (repeatable; default every declared
comparison set); `--evaluation-out` (default `artifacts/evaluation`); `--code-commit`.

Re-run behaviour
----------------
Each run appends its own `started` and terminal registry rows (append-only, R-08/R-09;
aborted runs stay visible, NFR-AUD-01). Mask registration is once-only per set and the
frozen-bundle manifest is write-once (Q4 = A); metrics artifacts are never overwritten --
each run emits under its own run directory. On `DEC`, the access sets
`locked_test_accessed = true` through the `AccessRecord` this script supplies to the one
door; this unit constructs no path of its own into the restricted root.

Boundaries this script holds
----------------------------
* Step 1 of the entry contract is `ensure_process_determinism`; `assert_phase_boundary` is
  step 4; `assert_no_raw_fields` runs BEFORE the first write (R-23/R-24).
* Imports NOTHING under `src/features`, `src/models`, `src/gnss` or `src/external` --
  predictions arrive as serialized artifacts; IRI/GIM reach `src/evaluation/metrics.py`
  at evaluation time only (R-112; TE 12; TA-07).
* No scientific constant: memberships, windows, embargo and seeds are configuration; no
  practical-relevance threshold is stated anywhere (PC-09).
"""

from __future__ import annotations

import argparse
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
    fixture_root_for,
    load_fixture_scope,
    read_embargo_hours,
)
from src.data.locked_test import AccessRecord, open_restricted  # noqa: E402
from src.data.phase_contract import assert_no_raw_fields, assert_phase_boundary  # noqa: E402
from src.data.splits import (  # noqa: E402
    LOCKED_ID,
    PARTITION_IDS,
    Partition,
    RecordFrame,
    build_partitions,
    materialise_locked_partition,
    partition_by_id,
    validation_month_range,
)
from src.evaluation.masks import (  # noqa: E402
    MaskRegistry,
    build_comparison_mask,
    prediction_from_payload,
    read_comparison_sets,
)
from src.evaluation.metrics import (  # noqa: E402
    LockedContext,
    assert_metrics_artifact,
    build_metrics_artifact,
    paired_loss_differential,
    write_metrics_artifact,
)

STAGE = "evaluation-and-comparison"
PHASE_DEFAULT = 1
WRITER_ROLE = "evaluate"  # R-18: never `train`, never `bootstrap`

#: The artifact field names this run can produce, screened through R-23's produced-field
#: limb BEFORE the first write (R-24).
PRODUCED_FIELDS: tuple[str, ...] = (
    "set_id",
    "mask_id",
    "feature_set_id",
    "member_ids",
    "member_transform_ids",
    "partition_id",
    "phase_id",
    "source_id",
    "target_definition_id",
    "row_counts",
    "exclusion_counts",
    "scored_window_statement",
    "window_length_hours",
    "lag_set",
    "registered_at_utc",
    "scalar",
    "per_station",
    "orientation",
    "weighting",
    "sign_convention_sentence",
    "model_id",
    "benchmark_id",
    "beats_model",
    "spatial_representativeness_sentence",
    "gim_overlap_disclosure",
    "phase2_not_independent_statement",
    "emitted_at_utc",
    "mask_ids",
    "entries",
    "frozen_at_utc",
)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="07_evaluate_and_report.py",
        description=(
            "Evaluate and compare (P1-04/P1-05): one comparison-wide mask per declared set, "
            "the paired-loss-differential estimand, the complete disclosing metrics "
            "artifact. REFUSES today before any mask (no 06 predictions run exists); DEC "
            "runs only through the G-05 signature guard and open_restricted."
        ),
    )
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--phase", type=int, choices=(1, 2), default=PHASE_DEFAULT)
    parser.add_argument(
        "--predictions-run",
        type=Path,
        default=None,
        help="a 06 predictions run directory, read by manifest (required for any scoring)",
    )
    parser.add_argument(
        "--partition",
        action="append",
        choices=PARTITION_IDS,
        default=None,
        help=(
            "partition(s) to evaluate (repeatable). DEC is NOT in any default and runs only "
            "through the locked path (G-05 signature; R-82)"
        ),
    )
    parser.add_argument(
        "--set",
        dest="sets",
        action="append",
        default=None,
        help="declared comparison set(s) to evaluate (default: every declared set)",
    )
    parser.add_argument("--evaluation-out", type=Path, default=Path("artifacts/evaluation"))
    parser.add_argument("--code-commit", type=str, default=None)
    parser.add_argument("--g05-signature", type=str, default=None)
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
        "--mask-bundle-manifest",
        type=Path,
        default=None,
        help=(
            "the write-once frozen-bundle manifest; open_restricted populates the SD-C-02 "
            "containment fields from it, and require_locked_receipt re-verifies it"
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
            "R-137), the metrics artifacts receive sibling fixture stamps, no locked path "
            "exists, and the TE 9.2 two-receipt gate is exempt (Q4/Q5 = A). Additive edit "
            "flagged for `evaluation-and-comparison`'s record (fixtures-and-reproducibility "
            "CR-2026-09-07)"
        ),
    )
    args = parser.parse_args(argv)
    if args.fixture_manifest is not None and args.partition:
        parser.error(
            "--fixture-manifest runs the manifest's declared apparatus partitions; a frozen "
            "--partition id alongside it is a contradiction (R-137's two-way quarantine)"
        )
    wanted = tuple(args.partition) if args.partition else ()
    if LOCKED_ID in wanted and not (
        args.g05_signature
        and args.locked_input
        and args.locked_authorization
        and args.mask_bundle_manifest
    ):
        parser.error(
            "--partition DEC requires --g05-signature, --locked-input, "
            "--locked-authorization and --mask-bundle-manifest; the locked path enters only "
            "through the G-05 guard and the one door"
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
        "prediction_hash": "",
        "locked_test_accessed": False,
        "notes": "evaluation-and-comparison run (P1-04/P1-05); DEC only through the G-05 "
        "signature guard and open_restricted",
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

    An upstream unit's artifact (`target-standardization`). A missing release refuses
    honestly (TE 13.3; TE 18.3) — exactly as `06` does; no loader is defaulted.
    """
    release_root = Path(snapshot.resolved_roots.get("release_root", ""))
    manifest = release_root / "phase1_hourly_target" / "release_manifest.json"
    if not manifest.is_file():
        raise IntegrityError(
            manifest,
            "no released Phase 1 hourly target manifest; the truth an estimand scores "
            "against is read from a released target by manifest and hash, never from a "
            "bare path (TE 13.3)",
        )
    raise IntegrityError(
        manifest,
        "reading the released target into a frame is reached only after the upstream "
        "freezes land; none has today, so this path stops here rather than defaulting a "
        "loader (TE 18.3)",
    )


def _load_predictions_run(run_dir: Path | None, partition_id: str) -> dict[str, Any]:
    """`06`'s serialized predictions for one partition, read by their payload contract.

    Returns a mapping model_id -> prediction-like object. The confirmatory M-06 payload
    (`M-06_confirmatory.json`, the three-seed mean with `seed = None`) stands as M-06's
    comparison entry — never a single-seed run (BLK-03 consumption contract point 1).
    """
    if run_dir is None:
        raise IntegrityError(
            "--predictions-run",
            "no 06 predictions run was named; predictions are read by manifest from a 06 "
            "output directory, and none exists today (06 refuses upstream of any fit)",
        )
    partition_dir = Path(run_dir) / partition_id
    if not partition_dir.is_dir():
        raise IntegrityError(
            partition_dir,
            f"no predictions directory for partition {partition_id!r}; 07 scores only what "
            f"06 wrote and refuses to invent an input (TE 18.3)",
        )
    members: dict[str, Any] = {}
    for path in sorted(partition_dir.glob("*.json")):
        if path.name.endswith(".receipt.json"):
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        prediction = prediction_from_payload(payload, resource=str(path))
        if prediction.model_id == "M-06" and path.stem != "M-06_confirmatory":
            continue  # per-seed M-06 runs: the confirmatory mean is the comparison entry
        members[prediction.model_id] = prediction
    return members


# =======================================================================================
# The locked path (W-5): reachable ONLY through the G-05 signature guard and the one door
# =======================================================================================


def _read_target_artifact(path: Path) -> Any:
    """Read a target artifact (`.jsonl` or `.json`) that `open_restricted` ALREADY logged."""
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        rows = [
            json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line
        ]
    elif suffix == ".json":
        rows = json.loads(path.read_text(encoding="utf-8"))
    else:
        raise IntegrityError(path, f"unsupported target artifact suffix {suffix!r}")
    return RecordFrame(rows)


def _locked_loader(args: argparse.Namespace, *, run_id: str, access_log: Path):
    """The one-door loader: log-then-read with purpose `locked_evaluation` (R-109 limb 2).

    The AccessRecord carries the G-05 signature reference in `authorization`; the SD-C-02
    containment fields are populated by `open_restricted` from the write-once frozen-bundle
    manifest found at access time (Q2 = B), and re-verified at every DEC metric by
    `require_locked_receipt`. The record it wrote is exposed on the returned closure for
    the metric path to consume.
    """
    state: dict[str, Any] = {}

    def loader(locked: Partition) -> Any:
        record = AccessRecord(
            run_id=run_id,
            retrieved_at_utc=dt.datetime.now(dt.UTC).isoformat(),
            scope=(
                f"{locked.partition_id} {locked.validation_month.isoformat()} locked "
                f"evaluation"
            ),
            purpose="locked_evaluation",
            performance_inspected=False,
            locked_test_accessed=True,
            authorization=str(args.locked_authorization),
        )
        opened = open_restricted(
            Path(args.locked_input),
            record=record,
            registry=access_log,
            mask_bundle_manifest=args.mask_bundle_manifest,
        )
        state["record"] = record
        return _read_target_artifact(Path(opened))

    loader.state = state  # type: ignore[attr-defined]
    return loader


# =======================================================================================
# The run
# =======================================================================================


def _month_bounds(partition: Partition) -> tuple[dt.datetime, dt.datetime, int]:
    start, end = validation_month_range(partition)
    return start, end, int(partition.embargo_hours)


def _evaluate_partition(
    *,
    snapshot: Any,
    args: argparse.Namespace,
    partition: Partition,
    declared_sets: Mapping[str, Mapping[str, Any]],
    set_ids: Sequence[str],
    registry: MaskRegistry,
    target: Any,
    out_root: Path,
    locked: LockedContext | None,
) -> list[str]:
    """Masks, estimands and the metrics artifact for one partition (W-1, W-2, W-6)."""
    members_by_id = _load_predictions_run(args.predictions_run, partition.partition_id)
    month_start, month_end, embargo_hours = _month_bounds(partition)
    feature_set_id = str(snapshot.features.get("feature_set_id", ""))
    written: list[str] = []
    for set_id in set_ids:
        declared = declared_sets[set_id]
        missing = [m for m in declared["member_ids"] if m not in members_by_id]
        if missing:
            raise IntegrityError(
                f"comparison set {set_id} on partition {partition.partition_id}",
                f"prediction(s) missing for declared member(s) {missing}; the mask is "
                f"built over the declared set exactly, never over whatever arrived "
                f"(R-106)",
            )
        members = [members_by_id[m] for m in declared["member_ids"]]
        mask = build_comparison_mask(
            members,
            set_id=set_id,
            declared_sets=declared_sets,
            target=target,
            feature_set_id=feature_set_id,
            month_start=month_start,
            month_end=month_end,
            embargo_hours=embargo_hours,
        )
        registry.register(mask)  # once-only; a second registration raises (R-107)
        model = members_by_id[declared["model_id"]]
        estimands = [
            paired_loss_differential(
                model,
                members_by_id[benchmark_id],
                mask=mask,
                declared_sets=declared_sets,
                registry=registry,
                locked=locked,
            )
            for benchmark_id in declared["benchmark_ids"]
        ]
        artifact = build_metrics_artifact(
            set_id=set_id,
            declared_sets=declared_sets,
            mask=mask,
            registry=registry,
            estimands=estimands,
        )
        assert_metrics_artifact(artifact, declared_sets=declared_sets)
        path = write_metrics_artifact(
            artifact, out_root / partition.partition_id / f"metrics_{set_id}.json"
        )
        written.append(str(path))
    return written


def _run_fixture_scale(
    entry: Mapping[str, Any], args: argparse.Namespace, *, run_id: str
) -> dict[str, Any]:
    """Q4 = A (fixtures-and-reproducibility R-137): the fixture-scale path, additive only.

    The SAME per-partition mask/estimand/artifact sequence as the full-year path, but over
    the APPARATUS partitions the fixture scope declares (never a frozen id — the loader
    refuses one, control 15), with a sibling fixture stamp written beside every metrics
    artifact (`<artifact>.fixture_stamp.json`, carrying `evidence_class`, `data07_caveat`,
    `december_representativeness` and `apparatus_partition_id`). NO locked path exists
    here: an apparatus partition is never `locked` (R-137; R-82), so no G-05 argument, no
    `open_restricted`, no `LockedContext` is reachable. The governed reads are unchanged
    (declared comparison sets, the released target by manifest), so today this path
    refuses exactly where the full-year path does (TE 18.3, stop and report).

    Board Rec 3 (ML-02, owner-authorised per CR-2026-09-07 §11.5; flagged for
    `evaluation-and-comparison`'s record): the fixture path's mask registry is ROOTED
    UNDER THE FIXTURE TREE — `artifacts/walking_skeleton/<fixture_id>/mask_registry/
    <apparatus_partition_id>/` — never under the confirmatory registry root, so an
    apparatus registration can never occupy a confirmatory set_id slot or enter the G-05
    frozen bundle, and a two-fold apparatus declaration never self-collides (one registry
    dir per apparatus partition). The fixture stamp is written INSIDE each per-partition
    registry dir (`fixture_stamp.json`, beside its registration entries). Board Rec 4
    (ML-03): a machine-readable measurement block (`fixture_measurements.json`,
    per-station surviving mask rows where measurable) is emitted under the evaluation
    output root for the orchestrator to fold into candidate measurements.
    """
    assert_no_raw_fields(PRODUCED_FIELDS, phase=args.phase)
    snapshot = entry["snapshot"]
    workspace = Path(snapshot.resolved_roots["workspace"])
    scope = load_fixture_scope(Path(args.fixture_manifest))

    declared_sets = read_comparison_sets(snapshot)  # refuses while undeclared (R-106)
    set_ids = tuple(args.sets) if args.sets else tuple(declared_sets)
    for set_id in set_ids:
        if set_id not in declared_sets:
            raise IntegrityError(
                f"--set {set_id}",
                f"is not a declared comparison set {sorted(declared_sets)}; membership is "
                f"configuration (R-106)",
            )
    target = _load_target_by_manifest(snapshot)  # refuses honestly today
    out_root = workspace / args.evaluation_out / run_id
    fixture_root = fixture_root_for(workspace, scope.fixture_id)
    partitions = build_apparatus_partitions(scope, embargo_hours=read_embargo_hours(snapshot))

    written: list[str] = []
    surviving_counts: list[int] = []
    for partition in partitions:
        if partition.validation_month is None:
            continue  # an apparatus refit is scored nowhere, like the frozen one
        stamp = stamp_for_manifest(scope, apparatus_partition_id=partition.partition_id)
        # Rec 3: one registry dir per apparatus partition, under the fixture tree.
        registry = MaskRegistry(fixture_root / "mask_registry" / partition.partition_id)
        artifacts = _evaluate_partition(
            snapshot=snapshot,
            args=args,
            partition=partition,
            declared_sets=declared_sets,
            set_ids=set_ids,
            registry=registry,
            target=target,
            out_root=out_root,
            locked=None,  # no locked path at fixture scale, structurally
        )
        write_sibling_stamp(registry.registry_dir, stamp)  # the stamp beside the entries
        for artifact in artifacts:
            write_sibling_stamp(Path(artifact), stamp)
            try:
                payload = json.loads(Path(artifact).read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            row_counts = payload.get("row_counts")
            if isinstance(row_counts, Mapping):
                surviving_counts.extend(int(v) for v in row_counts.values())
        written.extend(artifacts)
    if surviving_counts:  # Rec 4: measurable here — per-station surviving mask rows
        measurements_path = out_root / MEASUREMENTS_NAME
        measurements_path.parent.mkdir(parents=True, exist_ok=True)
        measurements_path.write_text(
            json.dumps(
                {
                    "stage": "07_evaluate_and_report",
                    "measurements": {
                        "support_missingness": {
                            "comparator": {
                                "min": min(surviving_counts),
                                "max": max(surviving_counts),
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
    return {"sets": list(set_ids), "artifacts_written": written}


def _run(entry: Mapping[str, Any], args: argparse.Namespace, *, run_id: str) -> dict[str, Any]:
    if args.fixture_manifest is not None:
        return _run_fixture_scale(entry, args, run_id=run_id)  # Q4 = A: the ONE fixture entry
    assert_no_raw_fields(PRODUCED_FIELDS, phase=args.phase)  # R-24: before the first write
    snapshot = entry["snapshot"]
    workspace = Path(snapshot.resolved_roots["workspace"])
    _, access_log = _registry_paths(snapshot)

    declared_sets = read_comparison_sets(snapshot)  # refuses while undeclared (R-106)
    set_ids = tuple(args.sets) if args.sets else tuple(declared_sets)
    for set_id in set_ids:
        if set_id not in declared_sets:
            raise IntegrityError(
                f"--set {set_id}",
                f"is not a declared comparison set {sorted(declared_sets)}; membership is "
                f"configuration (R-106)",
            )
    if not args.partitions:
        raise IntegrityError(
            "--partition",
            "no partition named; 07 evaluates the partition(s) whose 06 predictions exist "
            "and never guesses (DEC is never a default)",
        )

    target = _load_target_by_manifest(snapshot)  # refuses honestly today
    out_root = workspace / args.evaluation_out / run_id
    registry = MaskRegistry(workspace / args.evaluation_out / "mask_registry")
    partitions = build_partitions(snapshot)

    written: list[str] = []
    for pid in args.partitions:
        partition = partition_by_id(partitions, pid)
        locked: LockedContext | None = None
        if pid == LOCKED_ID:
            # The ONE door, twice guarded: the G-05 signature (R-82) then open_restricted
            # (R-25/R-28). Unreachable today: G-05 is Blocked and no signature verifies.
            loader = _locked_loader(args, run_id=run_id, access_log=access_log)
            materialise_locked_partition(
                snapshot,
                g05_signature=args.g05_signature,
                loader=loader,
                partitions=partitions,
            )
            month_start, month_end, embargo_hours = _month_bounds(partition)
            prediction_path = Path(args.predictions_run) / pid / "M-06_confirmatory.json"
            locked = LockedContext(
                prediction_path=prediction_path,
                receipt_path=prediction_path.with_name("M-06_confirmatory.receipt.json"),
                access_record=loader.state.get("record"),  # type: ignore[attr-defined]
                mask_bundle_manifest=args.mask_bundle_manifest,
                month_start=month_start,
                month_end=month_end,
                embargo_hours=embargo_hours,
            )
        written.extend(
            _evaluate_partition(
                snapshot=snapshot,
                args=args,
                partition=partition,
                declared_sets=declared_sets,
                set_ids=set_ids,
                registry=registry,
                target=target,
                out_root=out_root,
                locked=locked,
            )
        )
    return {"sets": list(set_ids), "artifacts_written": written}


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
        print(f"07_evaluate_and_report: preflight refusal: {exc}", file=sys.stderr)
        return 1

    snapshot = entry["snapshot"]
    lock = entry["lock"]
    lock_hash = environment_lock_hash(lock)
    registry_path, access_log = _registry_paths(snapshot)
    run_id = (
        f"evaluation-and-comparison-{dt.datetime.now(dt.UTC).strftime('%Y%m%dT%H%M%SZ')}"
        f"-{uuid.uuid4().hex[:8]}"
    )

    locked_run = bool(args.partitions and LOCKED_ID in args.partitions)
    started = _registry_row(
        run_id, status="started", lock_hash=lock_hash, snapshot=snapshot,
        code_commit=lock.code_commit, locked_test_accessed=False,
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
        print(f"07_evaluate_and_report: aborted: {exc}", file=sys.stderr)
        return 1

    completed = _registry_row(
        run_id, status="completed", lock_hash=lock_hash, snapshot=snapshot,
        code_commit=lock.code_commit, locked_test_accessed=locked_run,
    )
    append_registry_event(
        registry_path, completed, phase=args.phase, writer_role=WRITER_ROLE,
        access_log_path=access_log,
    )
    print(f"07_evaluate_and_report: completed: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
