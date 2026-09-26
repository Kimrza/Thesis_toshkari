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
* Per declared comparison set, the INFERENCE AND REPORTING layer then runs in the same
  `--set` loop (`_report_set`), wired 2026-09-20 under Recommendation 18: the vector
  time-block bootstrap per (model, benchmark) pair (`statistical-inference` W-1), the ONE
  primary results table, the breakdown family (member metrics, per-station, the D-17
  quality strata, the top-fraction sensitivity), the DEC regime breakdown on the locked
  partition, the practical-relevance record, and the claims-and-limitations checklist
  (`regimes-diagnostics-reporting` W-3...W-6). This is the path grant the boundary note
  already made (R-56): these two units own no stage script and run INSIDE this one. NO
  TENTH STAGE SCRIPT IS ADDED — TE 13.2 fixes the nine-script ordered sequence and
  amending it is a governing-document change.

  The gap this closed, recorded so the wiring is not mistaken for decoration: until
  2026-09-20 this script imported and called `build_comparison_mask`,
  `registry.register`, `paired_loss_differential` and `build_metrics_artifact` and
  nothing else. A grep across `scripts/` for `vector_block_bootstrap`,
  `build_primary_table`, `practical_relevance_statement`,
  `build_member_metrics_breakdown`, `top1pct_sensitivity_block`,
  `build_breakdown_artifact`, `build_claims_checklist` and `build_dec_regime_breakdown`
  returned ZERO call sites, and all ten `report_guards` rendering refusals had zero
  production callers. A clean run therefore produced a point estimate and no 95%
  interval, no bootstrap, no cross-station correlations, no 48-hour sensitivity, no
  primary results table, no December regime breakdown and no claims checklist — so
  PC-03/PC-04's requirement that the three difficulty controls appear in the SAME
  primary results table had no live enforcement path at all.

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

The reporting layer's inputs, each a governed upstream artifact read by path and NEVER
defaulted (Recommendation 18): `--target-release-manifest` (the stamped lineage the
metrics artifact's `units` is READ from — Recommendation 19), `--budget-artifact`,
`--table-caption` (supplied verbatim by the author; this script composes no governed
prose), `--conclusion-surface`, `--notebook-captions`, `--threshold-record` +
`--g06-receipt-utc` (optional; under D-34 no numeric threshold is approved and a run
without them RECORDS that state rather than skipping silently), and on `DEC`
`--audit-artifact`, `--kp-series`, `--kp-release-grade`, `--kp-source`. A run that cannot
report REFUSES naming the first absent input rather than emitting a point estimate with
no interval and calling that a result.

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
import csv
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
    TBD_SENTINEL,
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
    release_root_for,
)
from src.data.locked_test import AccessRecord, open_restricted  # noqa: E402
from src.data.release import verify_release  # noqa: E402
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
from src.evaluation.bootstrap import (  # noqa: E402
    read_bootstrap_declaration,
    vector_block_bootstrap,
    write_bootstrap_result,
)
from src.evaluation.diagnostics import (  # noqa: E402
    build_breakdown_artifact,
    build_claims_checklist,
    build_dec_regime_breakdown,
    build_member_metrics_breakdown,
    build_primary_table,
    build_quality_stratum,
    practical_relevance_statement,
    read_top1pct_declaration,
    top1pct_sensitivity_block,
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
from src.evaluation.regimes import read_regime_config  # noqa: E402
from src.evaluation.report_guards import ConclusionSurfaceRegistry  # noqa: E402

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
    # --- the inference and reporting layer, wired 2026-09-20 (Recommendation 18) --------
    "units",
    "comparisons",
    "artifact_id",
    "artifact_class",
    "kind",
    "rows",
    "members",
    "member_metrics",
    "caption",
    "budget_ref",
    "surviving_row_counts",
    "derived_percentage_rmse_reduction",
    "derived_percentage_rmse_reductions",
    "payload",
    "role_label",
    "aggregation",
    "breakdown_id",
    "completeness_shortfalls",
    "partial",
    "driver_identity_caveat",
    "stratum_field",
    "parent",
    "sensitivity",
    "rows_removed",
    "removed_fraction",
    "removed_keys",
    "removal_rule",
    "scope",
    "label",
    "ci_lower",
    "ci_upper",
    "ci_level",
    "interval_method",
    "block_hours",
    "block_scheme",
    "replicates",
    "point_estimate",
    "per_station_components",
    "seed",
    "seed_key",
    "generator_identity",
    "replicate_hash",
    "canonical_form",
    "stream_assignments",
    "replicate_vector",
    "widening_guard",
    "pairwise_correlations",
    "correlation_series",
    "n_blocks",
    "evaluation_mode",
    "registered_storm_event_count",
    "registered_audit_artifact_id",
    "comparison_storm_event_count",
    "descriptive_only",
    "events_wholly_outside_scored_set",
    "eligible_event_intervals",
    "practical_relevance",
    "first_conjunct",
    "second_conjunct",
    "enforcement",
    "enforcement_note",
    "inspected_registered_set",
    "conclusion_artifact_id",
    "claim_boundary",
    "nico_5min_bar",
    "residual",
    "post_access_report",
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
    # --- the inference and reporting layer's inputs (Recommendation 18, 2026-09-20) -----
    parser.add_argument(
        "--target-release-manifest",
        type=Path,
        default=None,
        help=(
            "the released Phase 1 target's release_manifest.json. Its TE §13.3 `units` "
            "field is the stamped lineage the metrics artifact's reporting unit is READ "
            "from (never hardcoded); its target_definition_id is checked against the "
            "registered mask's (Recommendation 19)"
        ),
    )
    parser.add_argument(
        "--budget-artifact",
        type=Path,
        default=None,
        help=(
            "the target uncertainty budget artifact placed adjacent to the primary result "
            "(FR-P1-05-10; TA-19), produced by target-standardization"
        ),
    )
    parser.add_argument(
        "--table-caption",
        type=str,
        default=None,
        help=(
            "the primary table's caption, supplied VERBATIM by the author. This script "
            "never composes it: FR-P1-05-19 requires the plasmaspheric-offset sentence in "
            "the caption and D-28's scored-set statement with it, and both are frozen "
            "wordings owned upstream — an orchestrator that wrote its own caption would "
            "be authoring governed prose (TE §7: scripts orchestrate)"
        ),
    )
    parser.add_argument(
        "--conclusion-surface",
        type=Path,
        default=None,
        help=(
            "the registered ConclusionSurfaceArtifact the claims checklist resolves its "
            "text rows against. ABSENT IS NOT SKIPPED: the checklist fails closed on None "
            "(R-126 control (36)), which is the designed behaviour, not an omission"
        ),
    )
    parser.add_argument(
        "--threshold-record",
        type=Path,
        default=None,
        help=(
            "the frozen practical-relevance threshold record (PC-09). Optional: under "
            "D-34 no numeric threshold is approved, so a run without it records that "
            "decided state machine-readably instead of producing a statement"
        ),
    )
    parser.add_argument(
        "--g06-receipt-utc",
        type=str,
        default=None,
        help="the G-06 receipt timestamp the threshold record must PRECEDE (PC-09)",
    )
    parser.add_argument(
        "--audit-artifact",
        type=Path,
        default=None,
        help=(
            "the REGISTERED pre-G-05 December coverage/regime audit (DEC only); its "
            "storm-event count is the DEC regime breakdown's sole governing input (R-124)"
        ),
    )
    parser.add_argument(
        "--kp-series",
        type=Path,
        default=None,
        help="the GFZ Kp series the DEC regime comparison count is derived from (DEC only)",
    )
    parser.add_argument(
        "--kp-release-grade",
        type=str,
        default=None,
        help="the Kp series' single recorded release grade (D-10.1; DEC only)",
    )
    parser.add_argument(
        "--kp-source",
        type=str,
        default=None,
        help="the Kp series' source, checked against the GFZ allowlist (D-13; DEC only)",
    )
    parser.add_argument(
        "--notebook-captions",
        type=Path,
        default=None,
        help=(
            "a JSON object of notebook_id -> caption for the checklist's FR-P1-03-4 row; "
            "absent leaves that row FAILED fail-closed, which is the designed behaviour"
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


#: The released target CSV's columns this loader reads — the SAME contract as
#: `06_train_and_predict.py`'s `_TARGET_COLUMNS` (three TARGET_* identities plus the three
#: NFR-TDEF-01 identity stamps). Two stage-local copies by the scripts' designed pattern;
#: consolidation into one `src/` home is flagged as owed in
#: `CR-2026-09-25-APPARATUS-HYPERPARAMETERS` §5 follow-ups.
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

    An upstream unit's artifact (`target-standardization`). A missing release refuses
    honestly (TE 13.3; TE 18.3) — exactly as `06` does; no loader is defaulted.
    `verify_release` re-derives the manifest's own claims before a single byte is
    trusted; only rows with `target_valid == "True"` are kept — a QC-invalid row is
    dropped, never imputed (D-5).

    Implemented 2026-09-26, mirroring `06`'s 2026-09-25 implementation verbatim (same
    stub, same reason, found by the first fixture run to reach stage 07 — see
    `CR-2026-09-25-APPARATUS-HYPERPARAMETERS`). Before this the function refused
    unconditionally even once the release existed on disk.
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
            "no released Phase 1 hourly target manifest; the truth an estimand scores "
            "against is read from a released target by manifest and hash, never from a "
            "bare path (TE 13.3)",
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
    # A plain record sequence, NOT a `src/features` frame: this script is boundaried to
    # `src/data` + `src/evaluation` (the import-boundary control in test_common_masks.py),
    # and `src/evaluation` consumes VALUES through its own `_rows_of` — which accepts a
    # record sequence by design (masks.py, D-27's transitive bar on `src/features`).
    return records


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
            retrieved_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
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


def _require_flag(value: Any, flag: str, what: str) -> Any:
    """A flag this code path needs — absent REFUSES, naming the flag (TE §18.3)."""
    if value in (None, ""):
        raise IntegrityError(
            flag,
            f"no {what} was named; this run reaches a path that requires it and refuses "
            f"rather than defaulting one (TE §18.3)",
        )
    return value


def _read_json_input(path: Path | None, *, flag: str, what: str) -> Mapping[str, Any]:
    """A governed upstream artifact read by path — absent or malformed REFUSES.

    Never defaulted, never substituted: TE §18.3's stop-and-report, the same posture
    `_load_target_by_manifest` takes for the released target.
    """
    if path is None:
        raise IntegrityError(
            flag,
            f"no {what} was named; the inference and reporting layer reads it from a "
            f"governed upstream artifact and refuses to invent one. A run that cannot "
            f"report refuses rather than emitting a point estimate with no interval, no "
            f"primary table and no claims checklist and calling that a result "
            f"(Recommendation 18; TE §18.3)",
        )
    resolved = Path(path)
    if not resolved.is_file():
        raise IntegrityError(resolved, f"no {what} exists at this path")
    try:
        payload = json.loads(resolved.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrityError(resolved, f"{what} is unreadable ({exc})") from exc
    if not isinstance(payload, Mapping):
        raise IntegrityError(resolved, f"{what} is not a JSON object")
    return payload


def _bootstrap_seed(snapshot: Any, *, seed_key: str) -> int:
    """The D-122 bootstrap seed, read from `seeds.yaml` by the DECLARED key (ADR-05).

    `seed_everything` never touches this seed, so it is read here at the call site, by
    the key the bootstrap declaration names — never a literal in source.
    """
    key = str(seed_key).split(".")[-1]
    value = snapshot.seeds.get(key)
    if value is None or (isinstance(value, str) and value.strip() == TBD_SENTINEL):
        raise IntegrityError(
            f"configs/seeds.yaml: {seed_key}",
            "absent or unresolved (TBD — freeze gate); the bootstrap seed is a frozen "
            "scientific value (D-122) read at the call site by ADR-05's carve-out and is "
            "never defaulted (TE §18.3)",
        )
    return int(value)


def _report_set(
    *,
    snapshot: Any,
    args: argparse.Namespace,
    partition: Partition,
    set_id: str,
    declared: Mapping[str, Any],
    declared_sets: Mapping[str, Mapping[str, Any]],
    mask: Any,
    registry: MaskRegistry,
    members_by_id: Mapping[str, Any],
    metrics_artifact: Mapping[str, Any],
    budget_artifact: Mapping[str, Any],
    report_dir: Path,
    month_start: dt.datetime,
    month_end: dt.datetime,
    embargo_hours: int,
    locked: LockedContext | None,
    evaluation_mode: str,
) -> list[str]:
    """The inference and reporting layer for ONE comparison set (Recommendation 18).

    Until 2026-09-20 this script computed the mask, the estimand and the metrics artifact
    and stopped. `grep` across `scripts/` for `vector_block_bootstrap`,
    `build_primary_table`, `practical_relevance_statement`,
    `build_member_metrics_breakdown`, `top1pct_sensitivity_block`,
    `build_breakdown_artifact`, `build_claims_checklist` and
    `build_dec_regime_breakdown` returned ZERO call sites, and all ten `report_guards`
    refusals had zero production callers — so a clean run produced a point estimate and
    no 95% interval, no bootstrap, no cross-station correlations, no 48-hour sensitivity,
    no primary results table, no December regime breakdown and no claims checklist, and
    PC-03/PC-04's requirement that the three difficulty controls appear in the SAME
    primary results table had no live enforcement path. This function is that path.

    NO TENTH STAGE SCRIPT: TE §13.2 fixes the nine-script ordered sequence, and amending
    it is a governing-document change. The boundary note's path grant (R-56) already
    places `statistical-inference` and `regimes-diagnostics-reporting` INSIDE this script.

    Every one of the ten SD-R-01 rendering refusals now lies on this path:
    ``require_complete_members``, ``require_units``, ``require_beats_model``,
    ``require_estimand_fields``, ``require_lineage_caveat``, ``require_derived_label``,
    ``require_provenance_block`` and ``require_registered_surface`` through
    ``build_primary_table``; ``require_driver_caveat`` through the per-station breakdown;
    ``require_d17_bound`` through ``build_quality_stratum``.
    """
    written: list[str] = []
    model_id = str(declared["model_id"])
    model = members_by_id[model_id]
    surfaces = ConclusionSurfaceRegistry(report_dir / "conclusion_surfaces")

    # --- W-1 (statistical-inference): the interval, per (model, benchmark) pair ---------
    declaration = read_bootstrap_declaration(snapshot.experiment)
    seed = _bootstrap_seed(snapshot, seed_key=str(declaration["seed_key"]))
    for benchmark_id in declared["benchmark_ids"]:
        result = vector_block_bootstrap(
            model,
            members_by_id[benchmark_id],
            mask=mask,
            block_hours=int(declaration["block_hours"]),
            replicates=int(declaration["replicates"]),
            seed=seed,
            declared_sets=declared_sets,
            registry=registry,
            experiment=snapshot.experiment,
            evaluation_mode=evaluation_mode,
            month_start=month_start,
            month_end=month_end,
            embargo_hours=embargo_hours,
            locked=locked,
        )
        written.append(
            str(
                write_bootstrap_result(
                    result, report_dir / f"bootstrap_{model_id}_vs_{benchmark_id}.json"
                )
            )
        )

    # --- W-3: the ONE primary results table (PC-03/PC-04's co-reporting, by construction)
    if not args.table_caption:
        raise IntegrityError(
            "--table-caption",
            "no caption was supplied; FR-P1-05-19 requires the plasmaspheric-offset "
            "sentence in the primary table's caption and D-28's scored-set statement "
            "with it, both frozen wordings owned upstream — this orchestrator supplies "
            "no caption of its own rather than authoring governed prose (TE §7)",
        )
    table = build_primary_table(
        metrics_artifact=metrics_artifact,
        mask=mask,
        budget_artifact=budget_artifact,
        declared_member_ids=declared["member_ids"],
        caption=str(args.table_caption),
        table_artifact_id=f"primary_table_{partition.partition_id}_{set_id}",
        registry=surfaces,
        emit_path=report_dir / f"primary_table_{set_id}.json",
    )
    written.append(str(report_dir / f"primary_table_{set_id}.json"))

    # --- W-5: the breakdown family -----------------------------------------------------
    breakdowns: list[Mapping[str, Any]] = []
    member_metrics_path = report_dir / f"breakdown_member_metrics_{set_id}.json"
    breakdowns.append(
        build_member_metrics_breakdown(
            metrics_artifact=metrics_artifact,
            mask=mask,
            breakdown_id=f"member_metrics_{set_id}",
            registry=surfaces,
            emit_path=member_metrics_path,
        )
    )
    written.append(str(member_metrics_path))

    # the per-station breakdown — the ONLY path that emits TC-12's standing caveat, so
    # `require_driver_caveat` reaches production here. Values are PRINTED from the
    # emitted artifact's own per-station components, never restated (R-107 limb 6).
    per_station_path = report_dir / f"breakdown_per_station_{set_id}.json"
    breakdowns.append(
        build_breakdown_artifact(
            breakdown_id=f"per_station_{set_id}",
            metrics_artifact=metrics_artifact,
            mask=mask,
            per_station=True,
            payload={
                "comparisons": [dict(row) for row in metrics_artifact.get("comparisons", ())]
            },
            registry=surfaces,
            emit_path=per_station_path,
        )
    )
    written.append(str(per_station_path))

    # the D-17 quality strata — `build_quality_stratum` is `require_d17_bound`'s only
    # caller, so the bound reaches production here. The masked rows carry the comparison
    # surface, not D-17's observation-quality columns, so each stratum is emitted EMPTY
    # with a machine-readable completeness shortfall rather than silently omitted (the
    # two-tier posture: a shortfall is recorded, never console text).
    regime_config = read_regime_config(snapshot.experiment)
    strata = []
    shortfalls: list[Mapping[str, Any]] = []
    for field_name in regime_config.quality_strata_fields:
        rows = [dict(row) for row in mask.masked_rows if field_name in row]
        strata.append(
            build_quality_stratum(
                stratum_field=field_name, config=regime_config, strata_rows=rows
            )
        )
        if not rows:
            shortfalls.append(
                {
                    "stratum_field": field_name,
                    "reason": (
                        "the registered comparison mask carries the comparison surface "
                        "(station, hour, y_true, y_hats) and not D-17's "
                        "observation-quality columns, so this stratum has no rows in a "
                        "07 run; the shortfall is recorded machine-readably and the "
                        "artifact is marked partial (R-127; the two-tier posture)"
                    ),
                }
            )
    strata_path = report_dir / f"breakdown_quality_strata_{set_id}.json"
    breakdowns.append(
        build_breakdown_artifact(
            breakdown_id=f"quality_strata_{set_id}",
            metrics_artifact=metrics_artifact,
            mask=mask,
            payload={"strata": strata},
            completeness_shortfalls=shortfalls,
            registry=surfaces,
            emit_path=strata_path,
        )
    )
    written.append(str(strata_path))

    # FR-P1-05-10's top-fraction sensitivity, COMPUTED per member (Recommendation 21) and
    # emitted as its own labelled breakdown — beside the parent figures, never merged.
    top1pct = read_top1pct_declaration(snapshot.experiment)
    sensitivity_path = report_dir / f"breakdown_top1pct_sensitivity_{set_id}.json"
    breakdowns.append(
        build_breakdown_artifact(
            breakdown_id=f"top1pct_sensitivity_{set_id}",
            metrics_artifact=metrics_artifact,
            mask=mask,
            payload={
                "blocks": [
                    top1pct_sensitivity_block(
                        mask=mask,
                        member_id=member_id,
                        removed_fraction=float(top1pct["removed_fraction"]),
                        scope=str(top1pct["scope"]),
                    )
                    for member_id in declared["member_ids"]
                ]
            },
            registry=surfaces,
            emit_path=sensitivity_path,
        )
    )
    written.append(str(sensitivity_path))

    # the DEC regime breakdown — post-receipt by construction (it consumes the emitted
    # metrics artifact, which cannot exist before R-109's verified hash receipt).
    if partition.partition_id == LOCKED_ID:
        dec_path = report_dir / f"breakdown_regime_split_dec_{set_id}.json"
        breakdowns.append(
            build_dec_regime_breakdown(
                metrics_artifact=metrics_artifact,
                mask=mask,
                kp=_read_target_artifact(
                    Path(
                        _require_flag(
                            args.kp_series, "--kp-series", "the DEC Kp series"
                        )
                    )
                ),
                audit=_read_json_input(
                    args.audit_artifact,
                    flag="--audit-artifact",
                    what="the REGISTERED pre-G-05 December coverage and regime audit",
                ),
                experiment=snapshot.experiment,
                release_grade=str(
                    _require_flag(
                        args.kp_release_grade,
                        "--kp-release-grade",
                        "the Kp series' recorded release grade",
                    )
                ),
                source=str(
                    _require_flag(args.kp_source, "--kp-source", "the Kp series' source")
                ),
                registry=surfaces,
                emit_path=dec_path,
            )
        )
        written.append(str(dec_path))

    # --- W-6: practical relevance ------------------------------------------------------
    relevance_path = report_dir / f"practical_relevance_{set_id}.json"
    if args.threshold_record is None:
        # D-34 (2026-09-10): the sentinel IS the decided state — no numeric threshold is
        # approved. The absence is RECORDED, machine-readably, so §5.3's conjuncts are
        # visibly not evaluated in this run rather than silently never running.
        relevance: dict[str, Any] = {
            "kind": "practical_relevance_not_produced",
            "reason": (
                "no --threshold-record was supplied. Under D-34 no numeric "
                "practical-relevance threshold is approved and practical relevance is "
                "reported DESCRIPTIVELY; Vision §5.3's two conjuncts are therefore NOT "
                "evaluated in this run. This is a recorded state, not a skipped check"
            ),
            "set_id": set_id,
            "partition_id": partition.partition_id,
        }
    else:
        threshold_record = _read_json_input(
            args.threshold_record,
            flag="--threshold-record",
            what="the frozen practical-relevance threshold record",
        )
        # WHICH benchmark the measured improvement is relative to is a scientific choice,
        # so it is READ from the frozen record and never picked here (a first-row default
        # would silently choose the reference §5.4's magnitude is compared against).
        reference_benchmark = threshold_record.get("reference_benchmark_id")
        if not reference_benchmark:
            raise IntegrityError(
                str(args.threshold_record),
                "the frozen threshold record names no reference_benchmark_id, so the "
                "measured improvement Vision §5.3's FIRST conjunct compares has no "
                "declared reference. Which benchmark the reduction is relative to is a "
                "scientific choice frozen in the record, never picked by this "
                "orchestrator (PC-09; TE §1.1 — no implementer fills such a value by "
                "convenience)",
            )
        measured = next(
            (
                row.get("derived_percentage_rmse_reduction")
                for row in table.get("rows", ())
                if str(row.get("benchmark_id")) == str(reference_benchmark)
            ),
            None,
        )
        relevance = dict(
            practical_relevance_statement(
                threshold_record=threshold_record,
                budget_artifact=budget_artifact,
                measured_improvement=measured,
                g06_receipt_utc=_require_flag(
                    args.g06_receipt_utc,
                    "--g06-receipt-utc",
                    "the G-06 receipt timestamp the threshold record must precede",
                ),
            )
        )
        relevance["reference_benchmark_id"] = str(reference_benchmark)
    relevance_path.parent.mkdir(parents=True, exist_ok=True)
    relevance_path.write_text(
        json.dumps(relevance, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8"
    )
    written.append(str(relevance_path))

    # --- W-4: the claims-and-limitations checklist -------------------------------------
    # `conclusion_surface=None` is NOT a skip: the checklist fails closed on it by design
    # (R-126 control (36)), which is why no pre-check guards this call.
    checklist_path = report_dir / f"claims_checklist_{set_id}.json"
    build_claims_checklist(
        registry=surfaces,
        conclusion_surface=(
            _read_json_input(
                args.conclusion_surface,
                flag="--conclusion-surface",
                what="the registered ConclusionSurfaceArtifact",
            )
            if args.conclusion_surface is not None
            else None
        ),
        table=table,
        breakdowns=breakdowns,
        notebook_captions=(
            dict(
                _read_json_input(
                    args.notebook_captions,
                    flag="--notebook-captions",
                    what="the notebook caption map",
                )
            )
            if args.notebook_captions is not None
            else None
        ),
        checklist_artifact_id=f"claims_checklist_{partition.partition_id}_{set_id}",
        emit_path=checklist_path,
    )
    written.append(str(checklist_path))
    return written


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
    evaluation_mode: str = "real_data",
) -> list[str]:
    """Masks, estimands, the metrics artifact AND the reporting layer for one partition.

    W-1, W-2, W-6 as before; since 2026-09-20 the `--set` loop also runs the inference
    and reporting layer per set through ``_report_set`` (Recommendation 18), so the
    bootstrap interval, the primary table, the breakdown family, the top-fraction
    sensitivity, the practical-relevance record and the claims checklist are produced by
    the same run that produces the point estimate.
    """
    members_by_id = _load_predictions_run(args.predictions_run, partition.partition_id)
    month_start, month_end, embargo_hours = _month_bounds(partition)
    feature_set_id = str(snapshot.features.get("feature_set_id", ""))
    target_release_manifest = _read_json_input(
        args.target_release_manifest,
        flag="--target-release-manifest",
        what="the released Phase 1 target's release manifest (the stamped units lineage)",
    )
    budget_artifact = _read_json_input(
        args.budget_artifact,
        flag="--budget-artifact",
        what="the target uncertainty budget artifact",
    )
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
            target_release_manifest=target_release_manifest,
        )
        assert_metrics_artifact(artifact, declared_sets=declared_sets)
        path = write_metrics_artifact(
            artifact, out_root / partition.partition_id / f"metrics_{set_id}.json"
        )
        written.append(str(path))
        written.extend(
            _report_set(
                snapshot=snapshot,
                args=args,
                partition=partition,
                set_id=set_id,
                declared=declared,
                declared_sets=declared_sets,
                mask=mask,
                registry=registry,
                members_by_id=members_by_id,
                metrics_artifact=artifact,
                budget_artifact=budget_artifact,
                report_dir=out_root / partition.partition_id / set_id,
                month_start=month_start,
                month_end=month_end,
                embargo_hours=embargo_hours,
                locked=locked,
                evaluation_mode=evaluation_mode,
            )
        )
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
    target = _load_target_by_manifest(snapshot, fixture_scope_id=entry.get("fixture_scope_id"))  # refuses honestly today
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
            # Rec 18: the reporting layer runs at fixture scale too, in `fixture` mode —
            # the mode the widening guard's failure semantics key on (R-120; Rec 23).
            evaluation_mode="fixture",
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

    target = _load_target_by_manifest(snapshot, fixture_scope_id=entry.get("fixture_scope_id"))  # refuses honestly today
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
        f"evaluation-and-comparison-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
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
