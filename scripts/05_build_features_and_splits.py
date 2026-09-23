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
* **The December path is GUARDED, not absent.** `--partition DEC` is off the default list and
  runs only behind the same guard `06` uses: `materialise_locked_partition`, which refuses
  (`LockedTestError`) without a G-05 signature that verifies against `configs/data.yaml`
  `gates.G-05` (R-82, ADR-03). Naming `DEC` additionally requires `--g05-signature`,
  `--locked-input` and `--locked-authorization`, and requires `REFIT` in the same run,
  because the December score bundle carries REFIT's transform -- the one enumerated G-06
  apply (R-74). The December bundle is written ONCE, under the signature; `write_bundle`
  refuses an existing directory. This script never names the restricted root: the
  human-supplied path is routed through `governance-guards`' `open_restricted`, the one door,
  which writes the `AccessRecord`. The split manifest stays five rows and never enumerates
  `DEC` (FR-P1-04-5, ADR-11 M5) -- the locked partition keeps its separate record, whose
  `access_gate_state` now reports whether the signature verified.

  Before 2026-09-20 there was no producer for the `DEC` score bundle at all, so `06`'s locked
  branch could only ever fail at `load_bundle` with "bundle is missing": the G-06 path was
  unexecutable end to end. This branch is what makes it executable, and it stays refused
  until G-05 is signed.
* When every value is frozen, `--partition <id>` (default: the five fitting-capable ones)
  runs the three-call sequence with the target and driver inputs supplied through the release
  root; those loaders are `target-standardization`'s and `external-products`' artifacts and
  are read by manifest -- a missing release refuses.

Inputs
------
`--config configs/` (the four governed configs, read only through `load_configs`);
`--phase 1|2` (every path below is phase-1-legal); `--partition` (repeatable, from
`F1`..`F4`,`REFIT`,`DEC`; default the five fitting-capable ones); `--bundles-out`
(workspace-relative bundle root, default `artifacts/features`); `--parity-tolerance` (the
fixture manifest's declared value, TE 15.2; absent -> the value-level parity limb STOPS
naming the field); `--g05-signature`, `--locked-input`, `--locked-authorization` (required
together with `--partition DEC`); `--code-commit`.

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
import csv
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
    release_root_for,
)
from src.data.locked_test import AccessRecord, open_restricted  # noqa: E402
from src.data.phase_contract import assert_no_raw_fields, assert_phase_boundary  # noqa: E402
from src.data.registry import load_registry  # noqa: E402
from src.data.release import verify_release  # noqa: E402
from src.data.splits import (  # noqa: E402
    FITTING_PARTITION_IDS,
    LOCKED_ID,
    PARTITION_IDS,
    REFIT_ID,
    Partition,
    RecordFrame,
    apply_embargo,
    build_partitions,
    build_split_manifest,
    locked_partition_record,
    materialise_locked_partition,
    partition_by_id,
    training_range,
    validation_month_range,
)
from src.external.spaceweather import (  # noqa: E402
    SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG,
    availability_rows_from_selection,
    select_lagged_series,
    trailing_mean,
)
from src.features._frames import records_of  # noqa: E402
from src.features.availability import (  # noqa: E402
    assert_lags_safe,
    build_availability_matrix,
    latest_eligible_window_end,
    read_availability_lags,
)
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
    "availability_rule",
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
        choices=PARTITION_IDS,
        default=None,
        help=(
            "partition(s) to build (repeatable; default the five fitting-capable ones). DEC "
            "is NOT in the default list: it requires --g05-signature, --locked-input, "
            "--locked-authorization and REFIT in the same run"
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
    if args.fixture_manifest is not None and args.partition:
        parser.error(
            "--fixture-manifest runs the manifest's declared apparatus partitions; a frozen "
            "--partition id alongside it is a contradiction (R-137's two-way quarantine)"
        )
    wanted = tuple(args.partition) if args.partition else FITTING_PARTITION_IDS
    if LOCKED_ID in wanted:
        if not (args.g05_signature and args.locked_input and args.locked_authorization):
            parser.error(
                "--partition DEC requires --g05-signature, --locked-input and "
                "--locked-authorization; the December bundle is written only behind the G-05 "
                "guard"
            )
        if REFIT_ID not in wanted:
            parser.error(
                "--partition DEC requires --partition REFIT in the same run: the December "
                "score bundle carries REFIT's transform, the one enumerated G-06 apply "
                "(R-74), and that transform is fitted on REFIT's training rows here"
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
        "feature_set_id": str(snapshot.features.get("feature_set_id", "")),
        "model_id": "",
        "hyperparameters_json": "",
        "seed": "",
        "validation_metric_name": "",
        "validation_metric_value": "",
        "artifact_manifest_path": "",
        "prediction_hash": "",
        "locked_test_accessed": False,
        "notes": ("features-and-splits run (P1-04); DEC only through the G-05 signature guard"),
    }
    if reason:
        row["reason"] = reason
    return row


#: The released target's producing artifact, as `configs/features.yaml`'s permitted-producer
#: list names it for every target-derived row (D-35).
TARGET_PRODUCER: str = "phase1_hourly_target"

#: Each driver FEATURE's `source_series`, read from the frozen dictionary rather than
#: restated, so this loader cannot drift from the contract `build_features` resolves.
#: (Both F10.7 fields were corrected on 2026-09-23 to name their own series: see
#: `configs/features.yaml` and RULING_REQUEST_2026-09-23_CONSTRUCTION_STOPS §1 and §3.)
_SERIES_OF_FEATURE: dict[str, str] = {
    "kp_safe": "kp",
    "ap_safe": "ap",
    "hp60_safe": "hp60",
    "ap60_safe": "ap60",
    "f107_safe": "f107_safe_at_origin",
    "f107_81_trailing": "f107_81_trailing_mean",
}

#: Which D-63 release each provider series is parsed from.
_ARTIFACT_OF_SERIES: dict[str, str] = {
    "kp": "gfz_kp_ap_nowcast_2022",
    "ap": "gfz_kp_ap_nowcast_2022",
    "hp60": "gfz_hp60ap60_v2_2022",
    "ap60": "gfz_hp60ap60_v2_2022",
}


# =======================================================================================
# The run: refusals first, then the three-call sequence per fitting-capable partition
# =======================================================================================


def _load_release_inputs(
    snapshot: Any, *, fixture_scope_id: str | None
) -> tuple[Any, Mapping[str, Any]]:
    """The target frame and the driver series, read BY MANIFEST from the release root.

    Both are upstream units' artifacts (`target-standardization`, `external-products`).
    A missing release refuses: this script never constructs a target or a driver itself.
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
    target_manifest = release_root / "phase1_hourly_target" / "release_manifest.json"
    if not target_manifest.is_file():
        raise IntegrityError(
            target_manifest,
            "no released Phase 1 hourly target manifest; features are built from a released "
            "target read by manifest and hash, never from a bare path (TE 13.3)",
        )
    target = _released_frame(target_manifest, producing_artifact=TARGET_PRODUCER)
    epochs = _target_epochs(target)
    drivers = _load_driver_frames(snapshot, release_root=release_root, epochs=epochs)
    return target, drivers


# =======================================================================================
# The release loader (owner rulings of 2026-09-23; D-61's option A at 02->05 and 04->05)
# =======================================================================================
#
# WHAT THIS READS AND WHY IT IS SHAPED THIS WAY. Two consumers key `drivers` DIFFERENTLY,
# and both keyings are supplied:
#
#   * `build_availability_matrix` keys by FEATURE (`kp_safe` ... `f107_81_trailing`) and
#     reads availability rows -- `forecast_origin`, `observation_timestamp`,
#     `publication_timestamp`, `release_status` -- plus `anchor_day` and `mean_value` for
#     the trailing feature, which its third limb recomputes against (D-47);
#   * `build_features` keys by `source_series` (`kp`, `ap`, `hp60`, `ap60`,
#     `f107_safe_at_origin`, `f107_81_trailing_mean`) and reads `interval_start_utc` and
#     `value` per row.
#
# `f107_daily_median` is supplied as the PLAIN DAILY SERIES (one row per covered day,
# carrying `day` and `value`): it is the window source the trailing limb recomputes from,
# and after the 2026-09-23 rulings no dictionary field names it, so nothing asks it to be
# hourly as well.
#
# NO GOVERNED RULE IS RE-IMPLEMENTED HERE. The safe lag is applied ONCE, by
# `spaceweather.select_lagged_series` (D-43/D-44); the eligible observation day under D-25
# comes from `availability.latest_eligible_window_end`, the same function the anchor limb
# checks against; the 81-day mean comes from `spaceweather.trailing_mean`, which is
# trailing by construction. A second implementation of any of them would be the drift this
# project has already paid for once (`nfr-design` c58).


def _released_frame(manifest_path: Path, *, producing_artifact: str) -> Any:
    """Read ONE released CSV into a `RecordFrame`, by manifest and hash, never by path.

    `verify_release` re-checks the manifest contract and every recorded output hash before
    a byte is parsed (R-44), so a release whose bytes changed under it refuses here rather
    than flowing into a feature matrix. `producing_artifact` travels in the frame's attrs
    because it is the producer half of the (row, producer) pair `build_features` resolves
    against the permitted-producer list (SD-F-01; D-63 names the identities).
    """
    problems = verify_release(manifest_path)
    if problems:
        raise IntegrityError(
            manifest_path,
            "the release does not verify, so nothing is read from it: " + "; ".join(problems),
        )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    outputs = sorted(
        name for name in dict(manifest.get("output_files") or {}) if name.endswith(".csv")
    )
    if len(outputs) != 1:
        raise IntegrityError(
            manifest_path,
            f"expected exactly one released CSV to read, found {outputs}; a reader that "
            f"picked one of several would be choosing its data by convention",
        )
    with (manifest_path.parent / outputs[0]).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    frame = RecordFrame(rows)
    frame.attrs["producing_artifact"] = producing_artifact
    frame.attrs["dataset_version"] = str(manifest.get("dataset_version", ""))
    frame.attrs["release_manifest"] = str(manifest_path)
    return frame


def _as_utc_stamp(value: Any, *, resource: str) -> dt.datetime:
    stamp = dt.datetime.fromisoformat(str(value))
    if stamp.tzinfo is None:
        raise IntegrityError(resource, f"{value!r} is not timezone-aware; driver epochs are UTC")
    return stamp.astimezone(dt.timezone.utc)


def _target_epochs(target: Any) -> tuple[dt.datetime, ...]:
    """The forecast origins the drivers must answer at: the released target's own epochs.

    Taken from the target rather than generated from the window, so a driver series is
    built for exactly the instants the features are built at -- a generated range would
    silently answer at epochs the target does not carry.
    """
    seen: dict[dt.datetime, None] = {}
    for index, record in enumerate(target):
        seen.setdefault(
            _as_utc_stamp(record["interval_start_utc"], resource=f"target row {index}"), None
        )
    return tuple(sorted(seen))


def _interval_observations(frame: Any, *, value_column: str) -> list[dict[str, Any]]:
    """Provider observations as `select_lagged_series` takes them: both boundaries and the
    value, an absent value kept as `None` so the interval keeps its identity (D-5)."""
    out: list[dict[str, Any]] = []
    for index, record in enumerate(frame):
        raw = record.get(value_column)
        out.append(
            {
                "interval_start": _as_utc_stamp(
                    record["interval_start_utc"], resource=f"{value_column} row {index}"
                ),
                "interval_end": _as_utc_stamp(
                    record["interval_end_utc"], resource=f"{value_column} row {index}"
                ),
                "value": None if raw in (None, "") else float(raw),
            }
        )
    return out


def _daily_frame(frame: Any, *, producing_artifact: str) -> Any:
    """The released F10.7 product as the plain daily series: `day` and `value` per row."""
    rows = [
        {
            "day": record["day_utc"],
            "value": (
                None
                if record["f107_daily_median"] in (None, "")
                else float(record["f107_daily_median"])
            ),
        }
        for record in frame
    ]
    daily = RecordFrame(rows)
    daily.attrs["producing_artifact"] = producing_artifact
    return daily


def _daily_map(daily: Any) -> dict[dt.date, float]:
    out: dict[dt.date, float] = {}
    for record in daily:
        if record["value"] is None:
            continue
        out[dt.date.fromisoformat(str(record["day"]))] = float(record["value"])
    return out


def _load_driver_frames(
    snapshot: Any, *, release_root: Path, epochs: tuple[dt.datetime, ...]
) -> dict[str, Any]:
    """Every driver frame the two consumers need, from the four D-63 releases."""
    lags = read_availability_lags(snapshot)
    sources = {
        "gfz_kp_ap_nowcast_2022": ("kp", "ap"),
        "gfz_hp60ap60_v2_2022": ("hp60", "ap60"),
        "nrcan_f107_observed_daily_median_2022": ("f107_daily_median",),
    }
    released: dict[str, Any] = {}
    for artifact in sources:
        manifest_path = release_root / artifact / "release_manifest.json"
        if not manifest_path.is_file():
            raise IntegrityError(
                manifest_path,
                f"no released driver product for {artifact!r}; features are built from "
                f"released driver products read by manifest and hash (R-44), and D-63 names "
                f"this producing artifact",
            )
        released[artifact] = _released_frame(manifest_path, producing_artifact=artifact)

    f107_artifact = "nrcan_f107_observed_daily_median_2022"
    daily = _daily_frame(released[f107_artifact], producing_artifact=f107_artifact)
    daily_values = _daily_map(daily)
    frames: dict[str, Any] = {"f107_daily_median": daily}

    for feature, entry in lags.items():
        status = str(entry["release_status_required"])
        rule = entry.get("availability_rule")
        window = entry.get("window")

        if rule is None:
            # --- interval-valued *_safe series (Kp/ap, Hp60/ap60) -----------------------
            series = _SERIES_OF_FEATURE[feature]
            artifact = _ARTIFACT_OF_SERIES[series]
            observations = _interval_observations(released[artifact], value_column=series)
            lag_hours = float(entry["safe_lag_hours"])
            selection = select_lagged_series(observations, epochs=epochs, safe_lag_hours=lag_hours)
            selected = RecordFrame(selection)
            selected.attrs["producing_artifact"] = artifact
            selected.attrs["observations"] = observations
            selected.attrs["selection"] = {
                "rule": SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG,
                "safe_lag_hours": lag_hours,
                "lag_reference_instant": str(entry["lag_reference_instant"]),
            }
            frames[series] = selected
            frames[feature] = RecordFrame(
                availability_rows_from_selection(selection, release_status=status)
            )
            continue

        # --- the two rule-bearing F10.7 features ---------------------------------------
        # D-25's eligible observation day per origin, from THE function the anchor limb
        # checks against — never a second derivation of the same rule.
        anchors = {
            epoch: latest_eligible_window_end(str(rule), epoch, resource=f"{feature} origin")
            for epoch in epochs
        }
        value_rows: list[dict[str, Any]] = []
        matrix_rows: list[dict[str, Any]] = []
        for epoch in epochs:
            anchor = anchors[epoch]
            if window is None:
                value = daily_values.get(anchor)
            else:
                value = trailing_mean(
                    daily_values, end_day=anchor, window_days=int(window["days"])
                )
            value_rows.append({"interval_start_utc": epoch.isoformat(), "value": value})
            if value is None:
                continue
            row: dict[str, Any] = {
                "forecast_origin": epoch,
                # The observation instant is the eligible DAY itself; the rule then places
                # its availability at 00:00 of the following day, which
                # `build_availability_matrix` applies (a rule is a floor, never a ceiling).
                "observation_timestamp": dt.datetime(
                    anchor.year, anchor.month, anchor.day, tzinfo=dt.timezone.utc
                ),
                "publication_timestamp": None,
                "release_status": status,
            }
            if window is not None:
                row["anchor_day"] = anchor.isoformat()
                row["mean_value"] = value
            matrix_rows.append(row)
        series = _SERIES_OF_FEATURE[feature]
        values = RecordFrame(value_rows)
        values.attrs["producing_artifact"] = f107_artifact
        frames[series] = values
        frames[feature] = RecordFrame(matrix_rows)
    return frames


def _read_target_artifact(path: Path) -> Any:
    """Read a target artifact (`.jsonl` or `.csv`) that `open_restricted` has ALREADY logged.

    The only reader the locked loader uses. It is reached only with a path the chokepoint
    returned, so this script never constructs a restricted path itself (R-28, one door).
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
    """The one door: every byte of December this script reads comes through here, logged."""

    def loader(locked: Partition) -> Any:
        record = AccessRecord(
            run_id=run_id,
            retrieved_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
            scope=f"{locked.partition_id} {locked.validation_month.isoformat()} feature build",
            purpose="locked_evaluation",
            performance_inspected=False,
            locked_test_accessed=True,
            authorization=str(args.locked_authorization),
        )
        opened = open_restricted(Path(args.locked_input), record=record, registry=access_log)
        return _read_target_artifact(Path(opened))

    return loader


def _build_locked_score_bundle(
    *,
    args: argparse.Namespace,
    snapshot: Any,
    partitions: tuple[Partition, ...],
    refit_transform: Any,
    common: Mapping[str, Any],
    out_root: Path,
    run_id: str,
    access_log: Path,
) -> tuple[str, int]:
    """The guarded December branch: materialise `DEC` behind G-05 and write its score bundle.

    `materialise_locked_partition` refuses (`LockedTestError`) unless `--g05-signature`
    verifies against `configs/data.yaml` `gates.G-05`, and it refuses BEFORE the loader runs,
    so an unsigned invocation reads no December byte at all. What it returns is the December
    frame with its first `embargo_hours` excluded and counted (D-28) — and that returned frame
    is the only thing the feature build consumes.

    The bundle carries REFIT's transform, fitted on REFIT's training rows in this same run:
    `DEC` fits no transform of its own (R-74 element 4's one enumerated apply). Returns the
    bundle directory and the embargo-excluded row count.
    """
    if refit_transform is None:
        raise IntegrityError(
            f"partition {LOCKED_ID}",
            f"no {REFIT_ID} transform was fitted in this run; the December score bundle is "
            f"the one enumerated apply of {REFIT_ID}'s fitted transform (R-74) and is never "
            f"built against a transform fitted elsewhere",
        )
    locked = partition_by_id(partitions, LOCKED_ID)
    scored_target = materialise_locked_partition(
        snapshot,
        g05_signature=args.g05_signature,
        loader=_locked_loader(args, run_id=run_id, access_log=access_log),
        partitions=partitions,
    )
    if scored_target is None:
        raise IntegrityError(
            f"partition {LOCKED_ID}",
            "the locked loader returned no frame; the December bundle is built from the frame "
            "the one door returned, never from an absent or substituted target",
        )
    excluded = int(getattr(scored_target, "attrs", {}).get("excluded_embargo_rows", 0))
    score_start, score_end = validation_month_range(locked)
    score_spec = FrameSpec(LOCKED_ID, "score", score_start, score_end)
    score = build_features(
        scored_target, spec=score_spec, transform=refit_transform, **dict(common)
    )
    return str(write_bundle(score, out_root)), excluded


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

    target, drivers = _load_release_inputs(
        snapshot, fixture_scope_id=entry.get("fixture_scope_id")
    )  # refuses honestly today (TE 18.3)
    matrix = build_availability_matrix(snapshot, drivers=drivers)
    assert_lags_safe(matrix)
    registry = load_registry(snapshot)

    out_root = workspace / args.bundles_out
    written: list[str] = []
    excluded_embargo: dict[str, int] = {}
    scored_rows: list[int] = []
    parity_diffs: list[float] = []
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
            # TE 15.1: the fixture's floating-point tolerance is MEASURED from the fixture
            # and frozen, never invented, so a run with no frozen tolerance measures the
            # parity difference instead of asserting against a number that does not exist.
            # WS-13 stays Pending either way — a measurement is not a passed check.
            "measure_parity": args.parity_tolerance is None,
            # The fixture's own apparatus normalization overrides (R-122), read from the
            # scope this run is bound to. A governed run reaches `build_features` by a path
            # that carries no fixture scope, so it can never pick one up: the deviation is
            # confined to the apparatus that needs it and `configs/features.yaml` stays
            # frozen exactly as D-60 left it (owner ruling 2026-09-23, §5 option 1).
            "apparatus_unstandardized": {
                str(column): str(entry["reason"])
                for column, entry in scope.apparatus_normalization.items()
            },
            # registry gate scoped to this run's phase (Phase 1 does not require the
            # Phase-2-only observable_codes; CR-2026-09-20-B01-PREREQS §5)
            "phase": args.phase,
        }
        stamp = stamp_for_manifest(scope, apparatus_partition_id=pid)
        raw = build_features(target, spec=train_spec, **common)
        transform = fit_transforms(raw, partition=partition)
        train = build_features(target, spec=train_spec, transform=transform, **common)
        parity_diffs.extend(
            bundle.measured_parity_diff
            for bundle in (raw, train)
            if bundle.measured_parity_diff is not None
        )
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
            if score.measured_parity_diff is not None:
                parity_diffs.append(score.measured_parity_diff)

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
                        },
                        # TE 15.2 area: the fixture-derived floating-point tolerance for
                        # WS-13's value-level limb. Reported as the LARGEST difference this
                        # run observed between the flattened matrix and the sequence tensor;
                        # freezing a tolerance from it is the owner's act, and until one is
                        # frozen the limb is measured rather than asserted and WS-13 stays
                        # Pending (TE 15.1: measured from the fixtures, never invented).
                        **(
                            {
                                "permitted_floating_point_tolerances": {
                                    "value_level_diff_tecu": {
                                        "observed_max": max(parity_diffs),
                                        "units": "TECU",
                                        "measured_over_bundles": len(parity_diffs),
                                        "status": "measured, not frozen; WS-13 Pending",
                                    }
                                }
                            }
                            if parity_diffs
                            else {}
                        ),
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


def _run(entry: Mapping[str, Any], args: argparse.Namespace, *, run_id: str) -> dict[str, Any]:
    if args.fixture_manifest is not None:
        return _run_fixture_scale(entry, args)  # Q4 = A: the ONE fixture-scale entry
    _assert_phase1_field_contract(args.phase)  # R-24: before the first write, always
    snapshot = entry["snapshot"]
    workspace = Path(snapshot.resolved_roots["workspace"])
    _, access_log = _registry_paths(snapshot)
    wanted = tuple(getattr(args, "partitions", None) or FITTING_PARTITION_IDS)

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

    # 2. Partitions (values from configs/data.yaml) and the five-row manifest. The locked
    #    record's gate state is written at the end, once the branch's outcome is known.
    partitions = build_partitions(snapshot)

    # 3. Inputs by manifest, the availability matrix and its three limbs.
    target, drivers = _load_release_inputs(
        snapshot, fixture_scope_id=entry.get("fixture_scope_id")
    )
    matrix = build_availability_matrix(snapshot, drivers=drivers)
    assert_lags_safe(matrix)
    registry = load_registry(snapshot)

    # 4. The three-call sequence per fitting-capable partition (R-81, FU-6 = A).
    out_root = workspace / args.bundles_out
    written: list[str] = []
    excluded_embargo: dict[str, int] = {}
    common = {
        "drivers": drivers,
        "registry": registry,
        "matrix": matrix,
        "partitions": partitions,
        "snapshot": snapshot,
        "parity_tolerance": args.parity_tolerance,
        # registry gate scoped to this run's phase (Phase 1 does not require the
        # Phase-2-only observable_codes; CR-2026-09-20-B01-PREREQS §5)
        "phase": args.phase,
    }
    refit_transform: Any = None
    for pid in wanted:
        if pid == LOCKED_ID:
            continue  # built after the loop: it applies REFIT's transform, fitted below
        partition = partition_by_id(partitions, pid)
        train_start, train_end = training_range(partition)
        train_spec = FrameSpec(pid, "train", train_start, train_end)
        raw = build_features(target, spec=train_spec, **common)
        transform = fit_transforms(raw, partition=partition)
        if pid == REFIT_ID:
            refit_transform = transform
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

    # 5. The GUARDED December branch. Refuses before any December byte is read unless the
    #    G-05 signature verifies (R-82, ADR-03); the released January–November target loaded
    #    above is never the source here — the one door's returned frame is.
    if LOCKED_ID in wanted:
        bundle_dir, excluded = _build_locked_score_bundle(
            args=args,
            snapshot=snapshot,
            partitions=partitions,
            refit_transform=refit_transform,
            common=common,
            out_root=out_root,
            run_id=run_id,
            access_log=access_log,
        )
        written.append(bundle_dir)
        excluded_embargo[LOCKED_ID] = excluded
        gate_state = (
            f"G-05 signature verified; DEC score bundle written once under it "
            f"({excluded} embargo rows excluded, D-28)"
        )
    else:
        gate_state = "G-05 gated; no December bundle requested in this run"
    locked_record = locked_partition_record(partitions, access_gate_state=gate_state)

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
        f"features-and-splits-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
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
        summary = _run(entry, args, run_id=run_id)
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
