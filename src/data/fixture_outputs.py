"""TE §15.4 fixture-root outputs and stage measurement blocks for a walking-skeleton run.

Purpose
-------
TE §15.4 names the files a walking-skeleton run leaves at
`artifacts/walking_skeleton/<fixture_id>/` (nineteen for `plumbing_7day`, the uncertainty
budget being fixture-2 only), and `run_walking_skeleton.collect_required_outputs` requires
each one at exactly that relative path. The seven Phase 1 stage scripts already produce
the CONTENT of those files, but under their own per-fold / per-set names and folders. This
module is the one place that turns that already-produced content into the TE §15.4 names —
by byte copy, lossless format conversion or aggregation — so no stage script re-derives a
scientific value to satisfy a filename (CR-2026-09-29-Q31-CLOSURE).

It also writes the per-stage measurement blocks (`fixture_measurements.json`, board Rec 4)
that `collect_stage_measurements` folds into a measuring result, and exposes the numeric
fingerprint a measuring run records so a later run can measure cross-run variation
(`cross_run_variation`).

Nothing here computes a model, a metric, a statistic, a tolerance or an interval. Every
function reads an artifact a stage already wrote and writes a new file ONCE.

Inputs
------
Paths to artifacts the stages wrote this run (the released hourly target CSV, a feature
bundle, the B-01 benchmark rows, the fixture-scoped GIM comparator release, prediction
payloads, registered masks, metrics artifacts, per-pair bootstrap skip records) and the
fixture root they are exported under.

Re-run behaviour
----------------
Every writer is write-once (TE 13.3): an existing output refuses, naming the file, rather
than being overwritten. A second measuring run therefore starts from a fixture root whose
previous run's outputs have been moved aside; the `measuring_result_*.json` files the
orchestrator persists are left in place so the second run can compose ranges over both.
"""

from __future__ import annotations

import datetime as dt
import json
import math
import shutil
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any, Final

from src.data.config import IntegrityError
from src.data.fixture_manifest import MEASUREMENTS_NAME
from src.data.release import sha256_of_file

#: The subdirectory under the fixture root that holds the measurement blocks written by
#: stages which own no other output directory there (02, 04). `collect_stage_measurements`
#: rglobs the whole fixture root, so the location only has to be unique per stage.
STAGE_MEASUREMENTS_DIR: Final[str] = "stage_measurements"

#: The CR that authorises this module and the Fixture 1 status artifacts it writes.
CLOSURE_CHANGE_RECORD: Final[str] = "CR-2026-09-29-Q31-CLOSURE"


# =======================================================================================
# Write-once primitives
# =======================================================================================


def _refuse_existing(path: Path) -> None:
    if path.exists():
        raise IntegrityError(
            path,
            "already exists; a fixture output is written exactly once per run and never "
            "overwritten (TE 13.3). Move the previous measuring run's outputs aside before "
            "a new run, keeping its measuring_result_*.json in place",
        )


def write_json_once(path: Path, payload: Mapping[str, Any]) -> Path:
    """Write a deterministic JSON document once (sorted keys, trailing newline)."""
    path = Path(path)
    _refuse_existing(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
    return path


def copy_once(source: Path, destination: Path) -> Path:
    """Byte-for-byte copy, write-once; the copy's SHA-256 equals the source's."""
    source, destination = Path(source), Path(destination)
    if not source.is_file():
        raise IntegrityError(source, "no source artifact exists to export; nothing is invented")
    _refuse_existing(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    if sha256_of_file(destination) != sha256_of_file(source):
        raise IntegrityError(destination, "copy does not hash-equal its source")
    return destination


def _write_frame_once(frame: Any, destination: Path) -> Path:
    destination = Path(destination)
    _refuse_existing(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(destination, engine="pyarrow", index=False)
    return destination


def write_stage_measurements(
    fixture_root: Path, *, stage: str, measurements: Mapping[str, Mapping[str, Any]]
) -> Path:
    """One stage's measurement block, in the `{area: {key: {min, max, units}}}` shape that
    `collect_stage_measurements` requires (board Rec 4)."""
    for area, quantities in measurements.items():
        for key, value in quantities.items():
            if not isinstance(value, Mapping) or "min" not in value or "max" not in value:
                raise IntegrityError(
                    f"{stage}: {area}.{key}", "a measured quantity carries min and max"
                )
            for bound in ("min", "max"):
                number = value[bound]
                if isinstance(number, bool) or not isinstance(number, int | float):
                    raise IntegrityError(f"{stage}: {area}.{key}.{bound}", "must be a number")
                if math.isnan(float(number)):
                    raise IntegrityError(f"{stage}: {area}.{key}.{bound}", "is NaN")
    path = Path(fixture_root) / STAGE_MEASUREMENTS_DIR / stage / MEASUREMENTS_NAME
    return write_json_once(path, {"stage": stage, "measurements": measurements})


def _span(values: Iterable[float], units: str) -> dict[str, Any]:
    values = [float(v) for v in values]
    if not values:
        raise IntegrityError(f"measurement in {units}", "no value was observed to measure")
    return {"min": min(values), "max": max(values), "units": units}


def _seconds_past_hour(stamp: str) -> int:
    text = str(stamp).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    moment = dt.datetime.fromisoformat(text)
    return moment.minute * 60 + moment.second


# =======================================================================================
# 02: hourly_vtec.parquet and the target measurements
# =======================================================================================


def export_hourly_vtec(release_csv: Path, fixture_root: Path) -> Path:
    """`hourly_vtec.parquet`: the released hourly target CSV, losslessly re-encoded.

    Column order, row order and every value are preserved (a float parsed from its decimal
    repr round-trips exactly in float64); nothing is recomputed.
    """
    import pandas as pd  # deferred: only the export path needs it

    frame = pd.read_csv(release_csv)
    return _write_frame_once(frame, Path(fixture_root) / "hourly_vtec.parquet")


def target_measurements(release_csv: Path) -> dict[str, dict[str, Any]]:
    """Row count, target support, invalid hours and hourly-boundary offset of the released
    target (TE §15.2 areas 6, 7, 8), measured from the rows the run released."""
    import pandas as pd

    frame = pd.read_csv(release_csv)
    valid = frame["target_valid"].astype(str).str.lower() == "true"
    support = frame.loc[valid, "valid_observation_count"].tolist()
    return {
        "row_count_ranges": {"hourly_target": _span([len(frame)] * 2, "rows")},
        "support_missingness": {
            "target_support": _span(support, "samples per hourly bin"),
            "invalid_hour": _span([int((~valid).sum())] * 2, "hours"),
        },
        "timestamp_tolerances": {
            "hourly_boundary": _span(
                [_seconds_past_hour(s) for s in frame["interval_start_utc"]], "s"
            ),
        },
    }


# =======================================================================================
# 04: iri_benchmark.parquet, gim_comparator.parquet and their timestamp measurements
# =======================================================================================


def iri_rows_in_scope(
    rows_path: Path, *, station: str, start: dt.date, end: dt.date
) -> list[dict[str, Any]]:
    """The already-generated B-01 rows for one station and an inclusive date window,
    `status == "ok"` only, in time order. Nothing is regenerated."""
    selected: list[dict[str, Any]] = []
    with Path(rows_path).open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            day = dt.date.fromisoformat(str(row["target_time_utc"])[:10])
            if row.get("station_id") == station and start <= day <= end and row.get("status") == "ok":
                selected.append(row)
    if not selected:
        raise IntegrityError(
            rows_path,
            f"no status='ok' B-01 row for {station} in {start}..{end}; the benchmark table "
            f"is never emitted empty",
        )
    return sorted(selected, key=lambda r: str(r["target_time_utc"]))


def export_iri_benchmark(rows: Sequence[Mapping[str, Any]], fixture_root: Path) -> Path:
    import pandas as pd

    frame = pd.DataFrame([dict(r) for r in rows])
    return _write_frame_once(frame, Path(fixture_root) / "iri_benchmark.parquet")


def iri_measurements(rows: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        "timestamp_tolerances": {
            "iri": _span([_seconds_past_hour(r["target_time_utc"]) for r in rows], "s"),
        }
    }


def gim_measurements(gim_parquet: Path, *, map_interval_seconds: int) -> dict[str, dict[str, Any]]:
    """GIM timestamp tolerance: seconds between each target epoch and the nearest IONEX map
    epoch, read from the generated rows (`exact_epoch_match`, `f_t`)."""
    import pandas as pd

    frame = pd.read_parquet(gim_parquet)
    offsets: list[float] = []
    for exact, f_t in zip(frame["exact_epoch_match"], frame["f_t"], strict=True):
        if bool(exact):
            offsets.append(0.0)
        else:
            fraction = float(f_t)
            offsets.append(min(fraction, 1.0 - fraction) * map_interval_seconds)
    return {"timestamp_tolerances": {"gim": _span(offsets, "s")}}


# =======================================================================================
# 05: feature_table.parquet, split_manifest.json
# =======================================================================================


def export_feature_table(
    bundle_dir: Path,
    fixture_root: Path,
    *,
    denial_mechanism: str,
    columns_checked: Sequence[str],
) -> Path:
    """`feature_table.parquet`: the full-window untransformed feature bundle's matrix,
    byte-copied, with its IRI-denial evidence attached beside it (TE §15.4: "IRI-free;
    denial test evidence attached")."""
    bundle_dir = Path(bundle_dir)
    matrix, spec = bundle_dir / "matrix.parquet", bundle_dir / "spec.json"
    destination = copy_once(matrix, Path(fixture_root) / "feature_table.parquet")
    write_json_once(
        Path(fixture_root) / "feature_table.parquet.denial_evidence.json",
        {
            "artifact": "feature_table_denial_evidence",
            "source_bundle": bundle_dir.name,
            "source_matrix_sha256": sha256_of_file(matrix),
            "source_spec_sha256": sha256_of_file(spec),
            "denial_mechanism": denial_mechanism,
            "columns_checked": list(columns_checked),
            "result": "pass",
            "governing_rules": ["NFR-IRI-01", "Vision 7.1", "WS-10", "TE §15.4"],
            "change_record": CLOSURE_CHANGE_RECORD,
        },
    )
    return destination


def export_split_manifest(apparatus_manifest: Path, fixture_root: Path) -> Path:
    """`split_manifest.json`: the fixture's apparatus split manifest, byte-copied."""
    return copy_once(apparatus_manifest, Path(fixture_root) / "split_manifest.json")


# =======================================================================================
# 06: predictions.parquet, checkpoint_manifest.json
# =======================================================================================

_PREDICTION_IDENTITY: Final[tuple[str, ...]] = (
    "model_id",
    "seed",
    "partition_id",
    "transform_id",
    "phase_id",
    "source_id",
    "target_definition_id",
    "horizon_hours",
    "confirmatory",
)


def export_predictions(payload_paths: Sequence[Path], fixture_root: Path) -> Path:
    """`predictions.parquet`: every model prediction payload this run wrote, one row per
    prediction with its identity columns; values copied, never recomputed."""
    import pandas as pd

    records: list[dict[str, Any]] = []
    for path in sorted(Path(p) for p in payload_paths):
        payload = json.loads(path.read_text(encoding="utf-8"))
        identity = {key: payload.get(key) for key in _PREDICTION_IDENTITY}
        for row in payload.get("rows", ()):
            records.append(
                {
                    **identity,
                    "payload_file": path.name,
                    "station": row["station"],
                    "interval_start_utc": row["interval_start_utc"],
                    "y_hat": row["y_hat"],
                }
            )
    if not records:
        raise IntegrityError(fixture_root, "no prediction rows to export")
    frame = pd.DataFrame(records)
    frame["seed"] = frame["seed"].astype("Int64")
    frame = frame.sort_values(
        ["partition_id", "model_id", "payload_file", "station", "interval_start_utc"],
        kind="mergesort",
    ).reset_index(drop=True)
    return _write_frame_once(frame, Path(fixture_root) / "predictions.parquet")


def export_checkpoint_manifest(
    entries: Sequence[Mapping[str, Any]], fixture_root: Path, *, fixture_id: str
) -> Path:
    """`checkpoint_manifest.json`: the M-06 checkpoint facts the fit already computed.

    Fold-fit checkpoints are held in memory only (`06`'s `_InMemoryCheckpointBackend`; no
    approved on-disk format, TS-M-01), so NO checkpoint file hash is recorded and none is
    invented: each entry carries the checkpoint's in-run identity (`payload_ref`) and the
    save/restore facts instead.
    """
    ordered = sorted(
        (dict(e) for e in entries),
        key=lambda e: (str(e.get("partition_id")), str(e.get("model_id")), str(e.get("seed"))),
    )
    return write_json_once(
        Path(fixture_root) / "checkpoint_manifest.json",
        {
            "artifact": "checkpoint_manifest",
            "fixture_id": fixture_id,
            "persistence": (
                "in-memory only: fold-fit checkpoints have no approved on-disk format "
                "(TS-M-01 freezes the REFIT format only); no file hash exists and none is "
                "recorded"
            ),
            "entries": ordered,
            "change_record": CLOSURE_CHANGE_RECORD,
        },
    )


# =======================================================================================
# 07: mask_manifest.json, metrics.json, bootstrap_summary.json
# =======================================================================================

_MASK_MEMBERSHIP_KEYS: Final[tuple[str, ...]] = (
    "mask_id",
    "set_id",
    "partition_id",
    "member_ids",
    "member_transform_ids",
    "row_counts",
    "exclusion_counts",
    "scored_window_statement",
    "feature_set_id",
    "phase_id",
    "source_id",
    "target_definition_id",
)


def export_mask_manifest(
    mask_files: Sequence[Path],
    skipped_sets: Sequence[Mapping[str, Any]],
    fixture_root: Path,
    *,
    fixture_id: str,
) -> Path:
    """`mask_manifest.json`: partition membership of every registered comparison mask
    (the registration timestamp is left in the registry, not copied), and every comparison
    set the run skipped, recorded as skipped — never as an empty mask."""
    masks = []
    for path in sorted(Path(p) for p in mask_files):
        registration = json.loads(path.read_text(encoding="utf-8"))
        masks.append({key: registration.get(key) for key in _MASK_MEMBERSHIP_KEYS})
    if not masks:
        raise IntegrityError(fixture_root, "no registered comparison mask to list")
    return write_json_once(
        Path(fixture_root) / "mask_manifest.json",
        {
            "artifact": "mask_manifest",
            "fixture_id": fixture_id,
            "masks": masks,
            "skipped_comparison_sets": sorted(
                (dict(s) for s in skipped_sets),
                key=lambda s: (str(s.get("partition_id")), str(s.get("set_id"))),
            ),
        },
    )


def export_metrics(
    metrics_files: Sequence[Path],
    skipped_sets: Sequence[Mapping[str, Any]],
    fixture_root: Path,
    *,
    fixture_id: str,
) -> Path:
    """`metrics.json`: every metrics artifact the run emitted, verbatim, keyed by partition
    and comparison set, plus the sets deliberately not evaluated."""
    evaluated: dict[str, dict[str, Any]] = {}
    for path in sorted(Path(p) for p in metrics_files):
        artifact = json.loads(path.read_text(encoding="utf-8"))
        partition = str(artifact.get("comparisons", [{}])[0].get("partition_id") or path.parent.name)
        evaluated.setdefault(partition, {})[str(artifact["set_id"])] = artifact
    if not evaluated:
        raise IntegrityError(fixture_root, "no metrics artifact to aggregate")
    return write_json_once(
        Path(fixture_root) / "metrics.json",
        {
            "artifact": "metrics",
            "fixture_id": fixture_id,
            "evaluated": evaluated,
            "not_evaluated": sorted(
                (dict(s) for s in skipped_sets),
                key=lambda s: (str(s.get("partition_id")), str(s.get("set_id"))),
            ),
        },
    )


def export_bootstrap_not_executed(
    skipped_pairs: Sequence[Mapping[str, Any]], fixture_root: Path, *, fixture_id: str
) -> Path:
    """`bootstrap_summary.json` for a fixture on which TE §15.3 does not execute bootstrap:
    an explicit status record — no replicate count, interval, statistic or tolerance.

    Deterministic by construction (no timestamp, no run id, no path), so the same fixture
    run always writes the same bytes (its ledger class is `exact`, CR-2026-09-29-Q31-CLOSURE).
    """
    pairs = sorted(
        (
            {
                "partition_id": str(p["partition_id"]),
                "set_id": str(p["set_id"]),
                "model_id": str(p["model_id"]),
                "benchmark_id": str(p["benchmark_id"]),
            }
            for p in skipped_pairs
        ),
        key=lambda p: (p["partition_id"], p["set_id"], p["model_id"], p["benchmark_id"]),
    )
    if not pairs:
        raise IntegrityError(
            fixture_root,
            "no per-pair bootstrap skip record exists; a not-executed status is written only "
            "over the skips the run actually recorded",
        )
    return write_json_once(
        Path(fixture_root) / "bootstrap_summary.json",
        {
            "artifact": "bootstrap_summary",
            "fixture_id": fixture_id,
            "status": "not_executed",
            "reason": (
                "TE §15.3 names bootstrap for Fixture 2 only (scientific_1month: one "
                "execution at reduced replicate count for timing); Fixture 1 "
                "(plumbing_7day) is scoped to M-01..M-05, a minimal M-06 and B-01/C-01 "
                "sample generation, and fixture_manifest._validate_fixture_bootstrap "
                "refuses a bootstrap block on it. No replicate, interval, statistic or "
                "tolerance was computed, and none is recorded."
            ),
            "governing_references": [
                "TE §15.3",
                "TE §15.4",
                "src/data/fixture_manifest.py _validate_fixture_bootstrap",
                CLOSURE_CHANGE_RECORD,
            ],
            "skipped_pairs": pairs,
        },
    )


# =======================================================================================
# Cross-run variation (toleranced outputs; measured, never declared)
# =======================================================================================


def _numeric_leaves(node: Any, path: str, out: dict[str, float]) -> None:
    if isinstance(node, bool):
        return
    if isinstance(node, int | float):
        out[path] = float(node)
    elif isinstance(node, Mapping):
        for key in sorted(node):
            _numeric_leaves(node[key], f"{path}/{key}", out)
    elif isinstance(node, list | tuple):
        for index, child in enumerate(node):
            _numeric_leaves(child, f"{path}[{index}]", out)


def numeric_fingerprint(path: Path) -> dict[str, float]:
    """Every numeric value of a toleranced output, keyed by a stable locator, so two
    measuring runs can be compared element by element.

    `.parquet` (predictions): one entry per prediction row keyed by its identity;
    `.json` (metrics): one entry per numeric leaf keyed by its JSON path. NaN is kept as
    NaN and compared by position.
    """
    path = Path(path)
    values: dict[str, float] = {}
    if path.suffix == ".parquet":
        import pandas as pd

        frame = pd.read_parquet(path)
        for row in frame.itertuples(index=False):
            key = "|".join(
                str(getattr(row, c))
                for c in ("partition_id", "payload_file", "station", "interval_start_utc")
            )
            value = row.y_hat
            values[key] = float("nan") if value is None else float(value)
    elif path.suffix == ".json":
        _numeric_leaves(json.loads(path.read_text(encoding="utf-8")), "", values)
    else:
        raise IntegrityError(path, f"no numeric fingerprint reader for {path.suffix!r}")
    return values


def cross_run_variation(
    fingerprints: Mapping[str, Mapping[str, float]],
) -> dict[str, Any]:
    """Max absolute element-wise difference of one output across >= 2 measuring runs.

    Scope: the measured run-to-run variation of ONE environment's measuring runs, recorded
    on a Q-31 candidate manifest. It is **not** the D-83 item 11 cross-environment
    tolerance and never governs it: item 11 is computed only by
    `src.data.cross_environment_tolerance` (determinism per `environment_id` first, then a
    per-field floor; D-83 revision 8 section A8 items 9-11). `run_walking_skeleton.
    compose_tolerances` routes any multi-environment composition there.

    Refuses when fewer than two runs are supplied or when the runs do not carry the same
    element set (a tolerance measured over different elements measures nothing).
    """
    run_ids = sorted(fingerprints)
    if len(run_ids) < 2:
        raise IntegrityError(
            "cross-run variation",
            f"needs at least two measuring runs, got {run_ids}; a single run measures a "
            f"point, not a variation (board Rec 5)",
        )
    keys = set(fingerprints[run_ids[0]])
    for run_id in run_ids[1:]:
        if set(fingerprints[run_id]) != keys:
            raise IntegrityError(
                f"cross-run variation over {run_ids}",
                "the runs carry different element sets; they did not produce the same output",
            )
    worst = 0.0
    for key in keys:
        column = [fingerprints[r][key] for r in run_ids]
        nans = [math.isnan(v) for v in column]
        if any(nans):
            if not all(nans):
                raise IntegrityError(
                    f"cross-run variation at {key}", "NaN in some runs and a number in others"
                )
            continue
        worst = max(worst, max(column) - min(column))
    return {"value": worst, "elements_compared": len(keys), "measuring_run_ids": run_ids}


# --- the measuring run's RECORD of the non-measured TE 15.2 quantities -------------------
#
# CR-2026-09-29-Q31-CLOSURE. An identity declaration may carry only `identity`,
# `inputs.prepared_vtec` and the ledger template (`load_identity_declaration`); every other
# TE 15.2 input, processing, schema, unit and reference-check quantity is "the measuring
# run's record". `recorded_quantities` is that record. Each value is either (a) transcribed
# from a non-sentinel entry of the owner-authored skeleton manifest
# (`tests/fixtures/<id>/fixture_manifest.yaml`: the frozen contract citations and the
# Phase-2 not_applicable reasons), or (b) READ from an artifact this run produced or
# consumed (hashes, schemas, units, sample values). Nothing is computed beyond reading, and
# no value is chosen here.

_RECORDED_AREAS: Final[tuple[str, ...]] = (
    "inputs",
    "processing",
    "expected_schema",
    "units",
    "independent_reference_checks",
)
_TBD_PREFIX: Final[str] = "TBD"


def _is_sentinel(node: Any) -> bool:
    if isinstance(node, str):
        return node.strip().startswith(_TBD_PREFIX)
    if isinstance(node, Mapping):
        return any(_is_sentinel(v) for v in node.values())
    if isinstance(node, list | tuple):
        return any(_is_sentinel(v) for v in node)
    return False


def _parquet_schema(path: Path) -> dict[str, Any]:
    import pandas as pd

    frame = pd.read_parquet(path)
    return {
        "file": path.name,
        "sha256": sha256_of_file(path),
        "rows": int(len(frame)),
        "columns": {str(c): str(t) for c, t in frame.dtypes.items()},
    }


def _json_schema(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    keys = sorted(payload) if isinstance(payload, Mapping) else []
    return {"file": path.name, "sha256": sha256_of_file(path), "top_level_keys": keys}


def _release_manifest(root: Path, name: str) -> Mapping[str, Any]:
    path = Path(root) / "releases" / name / "release_manifest.json"
    if not path.is_file():
        raise IntegrityError(path, "the release this run consumed has no release manifest")
    return json.loads(path.read_text(encoding="utf-8"))


def config_id(hashes: Mapping[str, str]) -> str:
    """SHA-256 over the sorted `name=sha256` lines of the governed config hashes."""
    import hashlib

    text = "\n".join(f"{k}={v}" for k, v in sorted(hashes.items()))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def recorded_quantities(
    *,
    workspace: Path,
    fixture_root: Path,
    skeleton: Mapping[str, Any],
    ledger_template: Mapping[str, Mapping[str, Any]],
    driver_releases: Sequence[str],
    gim_release: str,
    target_release: str,
    site_log: Path,
    site_log_manifest: Path,
    b01_manifest: Path,
) -> dict[str, dict[str, Any]]:
    """The run's record of TE 15.2's non-measured quantities (see the block comment above).

    Raises
    ------
    IntegrityError
        a consumed artifact is missing; the site log's hash disagrees with its recorded
        manifest; a skeleton sentinel is left with no run-recorded replacement.
    """
    import pandas as pd
    import yaml

    workspace, root = Path(workspace).resolve(), Path(fixture_root)

    def rel(path: Path) -> str:
        return Path(path).resolve().relative_to(workspace).as_posix()

    out: dict[str, dict[str, Any]] = {}
    for area in _RECORDED_AREAS:
        block = skeleton.get(area)
        out[area] = {
            k: v
            for k, v in (block.items() if isinstance(block, Mapping) else ())
            if k != "prepared_vtec" and not _is_sentinel(v)
        }
    # The MEASURED areas carry their Phase-2-only quantities as the skeleton's recorded
    # `status: not_applicable` with its reason (Q3 = A); their measured quantities come
    # only from the measuring runs, never from here.
    for area, block in skeleton.items():
        if area in _RECORDED_AREAS or area in ("identity", "required_outputs"):
            continue
        if not isinstance(block, Mapping):
            continue
        for key, value in block.items():
            if isinstance(value, Mapping) and value.get("status") == "not_applicable":
                out.setdefault(area, {})[key] = dict(value)
    # Derived from the ledger template's own classes, never the skeleton's hand list (which
    # predates the bootstrap_summary amendment).
    exact = sorted(n for n, e in ledger_template.items() if e.get("comparison_class") == "exact")
    out.setdefault("numerical_variation", {})["exact_fields"] = {
        "value": exact,
        "source": "the comparison_ledger template's `exact` entries (D-74 and its "
        "CR-2026-09-29-Q31-CLOSURE amendment; TE 13.7)",
    }

    # inputs
    recorded_log = json.loads(Path(site_log_manifest).read_text(encoding="utf-8"))
    log_hash = sha256_of_file(site_log)
    if recorded_log.get(Path(site_log).name) != log_hash:
        raise IntegrityError(site_log, "site log hash disagrees with its recorded manifest")
    out["inputs"]["site_log"] = {
        "file": rel(site_log),
        "sha256": log_hash,
        "recorded_in": rel(site_log_manifest),
    }
    b01 = json.loads(Path(b01_manifest).read_text(encoding="utf-8"))
    out["inputs"]["iri"] = {
        "benchmark_id": "B-01",
        "artifact_hashes": dict(sorted(b01.items())),
        "recorded_in": rel(b01_manifest),
        "fixture_rows_file": "iri_benchmark.parquet",
        "fixture_rows_sha256": sha256_of_file(root / "iri_benchmark.parquet"),
    }
    gim = _release_manifest(root, gim_release)
    out["inputs"]["ionex"] = {
        "files": {f["filename"]: f["sha256"] for f in gim["source_files"]},
        "release": gim_release,
        "release_content_hash": gim.get("content_hash"),
    }
    out["inputs"]["space_weather"] = {
        name: {
            "content_hash": manifest.get("content_hash"),
            "release_status": manifest.get("release_status"),
            "output_files": manifest.get("output_files"),
        }
        for name in driver_releases
        for manifest in (_release_manifest(root, name),)
    }

    # processing
    snapshot = yaml.safe_load(
        (root / "processing_config_snapshot.yaml").read_text(encoding="utf-8")
    )
    hashes = dict(sorted(snapshot["config_hashes"].items()))
    out["processing"]["full_config_id"] = {
        "value": config_id(hashes),
        "config_hashes": hashes,
        "method": "sha256 over the sorted `name=sha256` lines of the four governed configs",
    }

    # expected_schema
    schema = out["expected_schema"]
    schema["hourly_target"] = {
        **dict(schema.get("hourly_target", {})),
        "produced": _parquet_schema(root / "hourly_vtec.parquet"),
    }
    schema["feature"] = _parquet_schema(root / "feature_table.parquet")
    schema["benchmark"] = _parquet_schema(root / "iri_benchmark.parquet")
    schema["comparator"] = _parquet_schema(root / "gim_comparator.parquet")
    schema["prediction"] = _parquet_schema(root / "predictions.parquet")
    schema["metric"] = _json_schema(root / "metrics.json")

    # units
    target_units = _release_manifest(root, target_release).get("units", {})
    count_dtype = schema["hourly_target"]["produced"]["columns"].get("valid_observation_count")
    out["units"]["seconds_counts"] = {
        "value": {
            "largest_internal_gap_s": target_units.get("largest_internal_gap_s"),
            "valid_observation_count": f"count ({count_dtype})",
        },
        "source": f"releases/{target_release}/release_manifest.json `units`; the count "
        f"column's dtype as produced in hourly_vtec.parquet",
    }
    out["units"]["external_index_units"] = {
        "value": {name: _release_manifest(root, name).get("units") for name in driver_releases},
        "source": "each consumed driver release's own `units`",
    }

    # independent_reference_checks
    iri = pd.read_parquet(root / "iri_benchmark.parquet")
    gim_frame = pd.read_parquet(root / "gim_comparator.parquet")
    iri_at = {
        pd.Timestamp(t): float(v)
        for t, v in zip(iri["target_time_utc"], iri["iri2016_t_plus_1_tecu"], strict=True)
    }
    stamps = gim_frame["target_epoch_utc"].map(pd.Timestamp)
    epochs = sorted(stamps)
    samples = []
    for epoch in (epochs[0], epochs[len(epochs) // 2], epochs[-1]):
        row = gim_frame[stamps == epoch].iloc[0]
        samples.append(
            {
                "epoch_utc": epoch.isoformat(),
                "station": str(row["station"]),
                "gim_value_tecu": float(row["value_tecu"]),
                "iri_value_tecu": iri_at.get(epoch),
            }
        )
    out["independent_reference_checks"]["sample_iri_gim_values"] = {
        "samples": samples,
        "units": "TECU",
        "note": "first, middle and last GIM epoch of the window with the IRI value at the "
        "same epoch, read from this run's iri_benchmark.parquet and gim_comparator.parquet "
        "(evaluation-time only, NFR-IRI-01)",
    }

    left = [f"{a}.{k}" for a, b in out.items() for k, v in b.items() if _is_sentinel(v)]
    if left:
        raise IntegrityError(root, f"recorded quantities still carry a sentinel: {left}")
    return out
