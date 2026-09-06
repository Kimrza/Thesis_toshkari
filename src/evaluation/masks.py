"""C2 masks: one comparison-wide intersection mask per declared set, registered once, frozen.

Purpose
-------
`evaluation-and-comparison` W-1 / R-106 / R-107 / FR-P1-04-7 / NFR-FAIR-01, made executable:

* ``read_comparison_sets`` — the three declared sets (primary 5, gim 2, tier3 3 members) read
  from `configs/experiment.yaml` through `ConfigSnapshot`; membership is a frozen scientific
  choice living in configuration (TC-03e; confirmed Q1 = A,
  `governance/CHANGE_RECORD_2026-09-06_R106_comparison_sets.md`), NEVER in source.
* ``build_comparison_mask`` — stamps checked FIRST (W-1 step 1), membership checked exactly
  (W-1 step 2, one copy in `guards.require_declared_membership`), matched windows asserted
  across members (NFR-FAIR-01's matched-windows limb, control 28), ONE intersection over the
  members' and the target's availability (W-1 step 3, exclusions counted per station), then
  identity and the reporting surface (W-1 step 4): a deterministic ``mask_id`` over the
  declared set and the masked row content, per-station surviving AND exclusion counts, the
  full stamp set, and the scored-window statement derived from the partition's month and
  embargo (D-28's disclosure, `guards.scored_window_statement`).
* ``MaskRegistry`` — once-only registration per comparison set ("computed once" as a CHECK,
  R-107 limb 4), the registry read path the SD-C-02 containment check consumes, and the
  WRITE-ONCE frozen-bundle manifest (Q4 = A).
* The five exposed reporting values (R-107 limb 6, Recommendation 16): ``mask_id``,
  ``feature_set_id``, per-station surviving row counts, per-station exclusion counts, and the
  scored-window statement — for `regimes-diagnostics-reporting` to print and never restate;
  ``assert_reporting_surface`` is control (31)'s presence test.

The Q4 = A race analysis (SD-C-02's read-then-write Minor, resolved here)
-------------------------------------------------------------------------
The frozen bundle's manifest is written ONCE per freeze via ``.tmp`` → flush+fsync →
``os.replace`` (the same idiom as `models-and-baselines`' prediction-hash receipt,
SD-M-04), and any second write REFUSES. Because `os.replace` is atomic on one filesystem, a
reader — in particular `governance-guards`' `open_restricted`, populating the access
record's `mask_bundle_ids`/`mask_registry_hash` at locked-test access time — sees either the
old complete manifest or the new complete manifest, never a partial one. The residual
interleaving (a registration landing between the access path's manifest read and its record
write) is benign BY CONTAINMENT: the record then evidences the earlier freeze, and post-hoc
verification (re-hash the manifest, compare with the recorded hash, check the scored
``mask_id`` ∈ ``mask_bundle_ids``) still decides ordering on any clocks, across any hosts.
No lock machinery is added (option B rejected: a second mutual-exclusion mechanism with no
shared semantics across the two authorised platforms).

Inputs
------
Prediction-like objects (the approved eight-field `Prediction` shape, structurally typed —
also constructible from `06`'s serialized payloads via ``prediction_from_payload``), the
target frame (rows carrying `station_id`, `interval_start_utc`, `vtec_tecu`), the declared
sets from `ConfigSnapshot.experiment`, and a registry directory. This module imports ONLY
`src/data`, `src/evaluation/guards` and the standard library — **no `src/features`, no
`src/models`, no `src/external`, directly or transitively** (D-27; TE §12).

Re-run behaviour
----------------
``build_comparison_mask`` is pure and deterministic: the same declared set over the same
rows reproduces the same ``mask_id`` (recomputation that does not is a FAILURE — R-107
limb 1, ``assert_mask_id_reproduces``). Registration is once-only per set and the frozen
bundle manifest is write-once: re-running a registration or a freeze REFUSES rather than
silently replacing (NFR-AUD-01's no-silent-replacement posture applied to the mask
registry, which sits inside the G-05 frozen bundle — FR-P1-05-17).

Governance
----------
R-106 (membership declared configuration, checked exactly); R-107 (identity, once-only,
freeze, reporting surface); D-28 (the scored-window disclosure); Q1 = A / Q4 = A
(`CR-2026-09-06-R106-COMPARISON-SETS`); FR-P1-04-7; NFR-FAIR-01/TC-16; WS-16/TA-11 stay
`Pending` — nothing here discharges an acceptance row.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.data.config import FairnessError, IntegrityError, TBD_SENTINEL
from src.data.splits import RecordFrame
from src.evaluation.guards import (
    require_declared_membership,
    require_partition_agreement,
    require_stamps,
    scored_window_statement,
)

__all__ = [
    "FROZEN_BUNDLE_MANIFEST_NAME",
    "LoadedPrediction",
    "ComparisonMask",
    "MaskRegistry",
    "read_comparison_sets",
    "prediction_from_payload",
    "build_comparison_mask",
    "compute_mask_id",
    "assert_mask_id_reproduces",
    "assert_reporting_surface",
]

#: The write-once frozen-bundle manifest's file name inside a registry directory. An
#: implementation identifier, not a scientific constant.
FROZEN_BUNDLE_MANIFEST_NAME: str = "frozen_bundle_manifest.json"

#: Target-frame column identities (D-17's, read as `src/models/train.py` reads them).
_TARGET_STATION = "station_id"
_TARGET_TIMESTAMP = "interval_start_utc"
_TARGET_VALUE = "vtec_tecu"

#: The three identity stamps every prediction carries (NFR-TDEF-01; TE §13).
_IDENTITY_KEYS = ("phase_id", "source_id", "target_definition_id")


@dataclass(frozen=True)
class LoadedPrediction:
    """The approved eight-field `Prediction` shape, reconstructed from `06`'s payload.

    Mirrors `src/models/train.py`'s `Prediction` field-for-field. It exists because this
    package consumes predictions AS SERIALIZED ARTIFACTS (read by manifest, W-7) and may not
    import `src/models/train.py`, which imports `src/features` at module scope — an edge
    D-27 leaves unauthorised for this package even transitively. Guards are structurally
    typed, so a real `Prediction` and a `LoadedPrediction` pass identically.
    """

    model_id: str
    seed: int | None
    frame: Any
    target_definition_id: str
    phase_id: str
    source_id: str
    partition_id: str
    transform_id: str


def prediction_from_payload(payload: Mapping[str, Any], *, resource: str) -> LoadedPrediction:
    """`06`'s serialized prediction payload → a `LoadedPrediction` (file contract, W-7).

    Raises
    ------
    IntegrityError
        a payload missing `rows` or any of the eight approved fields' keys — a prediction
        that does not say what it is cannot enter a comparison.
    """
    rows = payload.get("rows")
    if not isinstance(rows, Sequence) or isinstance(rows, str):
        raise IntegrityError(resource, "prediction payload carries no `rows` list")
    frame = RecordFrame(dict(r) for r in rows)
    for key in ("horizon_hours", "hyperparameters", "confirmatory", "seeds_averaged"):
        if key in payload:
            frame.attrs[key] = payload[key]
    missing = [
        k
        for k in (
            "model_id",
            "partition_id",
            "transform_id",
            "phase_id",
            "source_id",
            "target_definition_id",
        )
        if payload.get(k) in (None, "")
    ]
    if missing:
        raise IntegrityError(
            resource,
            f"prediction payload is missing {missing}; the eight-field shape travels whole "
            f"(ADR-11: the stamp has to travel the whole way)",
        )
    seed = payload.get("seed")
    return LoadedPrediction(
        model_id=str(payload["model_id"]),
        seed=int(seed) if isinstance(seed, int) and not isinstance(seed, bool) else None,
        frame=frame,
        target_definition_id=str(payload["target_definition_id"]),
        phase_id=str(payload["phase_id"]),
        source_id=str(payload["source_id"]),
        partition_id=str(payload["partition_id"]),
        transform_id=str(payload["transform_id"]),
    )


def read_comparison_sets(snapshot: Any) -> dict[str, dict[str, Any]]:
    """The declared comparison sets from `experiment.comparison_sets` (R-106).

    Raises
    ------
    IntegrityError
        the block is absent or `TBD — freeze gate` (membership is a frozen scientific
        choice; without a declaration nothing can ever build a mask, and this refusal names
        the field rather than defaulting it — TE §18.3); a set entry without a non-empty
        `member_ids` list, `model_id`, or `benchmark_ids`; a benchmark or model outside the
        set's own membership.
    """
    node = snapshot.experiment.get("comparison_sets")
    if node is None or (isinstance(node, str) and node.strip() == TBD_SENTINEL):
        raise IntegrityError(
            "configs/experiment.yaml: comparison_sets",
            "absent or unresolved (TBD — freeze gate); comparison-set membership is a "
            "frozen scientific choice living in configuration (R-106, TC-03e) and is never "
            "filled by an implementer by convenience (TE 18.3) — without the declaration no "
            "mask can ever be built, which is the fail-closed posture",
        )
    if not isinstance(node, Mapping):
        raise IntegrityError(
            "configs/experiment.yaml: comparison_sets", "must be a mapping of named sets"
        )
    declared: dict[str, dict[str, Any]] = {}
    for set_id, entry in node.items():
        if str(set_id) in ("decision", "source"):
            continue  # provenance keys of the transcription, not sets
        if not isinstance(entry, Mapping):
            raise IntegrityError(
                f"configs/experiment.yaml: comparison_sets.{set_id}", "must be a mapping"
            )
        members = entry.get("member_ids")
        model_id = entry.get("model_id")
        benchmarks = entry.get("benchmark_ids")
        if not isinstance(members, Sequence) or isinstance(members, str) or not members:
            raise IntegrityError(
                f"configs/experiment.yaml: comparison_sets.{set_id}.member_ids",
                "must be a non-empty enumerated list (R-106)",
            )
        if not model_id or not isinstance(benchmarks, Sequence) or not benchmarks:
            raise IntegrityError(
                f"configs/experiment.yaml: comparison_sets.{set_id}",
                "must name model_id and a non-empty benchmark_ids list",
            )
        member_ids = tuple(str(m) for m in members)
        if str(model_id) not in member_ids:
            raise IntegrityError(
                f"configs/experiment.yaml: comparison_sets.{set_id}.model_id",
                f"{model_id!r} is not among the set's own member_ids {list(member_ids)}",
            )
        for bench in benchmarks:
            if str(bench) not in member_ids:
                raise IntegrityError(
                    f"configs/experiment.yaml: comparison_sets.{set_id}.benchmark_ids",
                    f"{bench!r} is not among the set's own member_ids {list(member_ids)}",
                )
        declared[str(set_id)] = {
            "member_ids": member_ids,
            "model_id": str(model_id),
            "benchmark_ids": tuple(str(b) for b in benchmarks),
        }
    if not declared:
        raise IntegrityError(
            "configs/experiment.yaml: comparison_sets", "declares no comparison set"
        )
    return declared


@dataclass(frozen=True)
class ComparisonMask:
    """`domain-entities.md` § 2: one intersection, a stable identity, the stamps that travel.

    The five REPORTING values `regimes-diagnostics-reporting` prints and never restates
    (R-107 limb 6): `mask_id`, `feature_set_id`, `row_counts` (surviving, per station),
    `exclusion_counts` (dropped by the intersection, per station), and
    `scored_window_statement`.
    """

    mask_id: str
    set_id: str
    feature_set_id: str
    partition_id: str
    member_ids: tuple[str, ...]
    member_transform_ids: tuple[str, ...]
    phase_id: str
    source_id: str
    target_definition_id: str
    row_counts: Mapping[str, int]
    exclusion_counts: Mapping[str, int]
    masked_rows: tuple[Mapping[str, Any], ...]
    scored_window_statement: str
    window_length_hours: int | None = None
    lag_set: tuple[str, ...] = field(default_factory=tuple)


def _canonical_rows(masked_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for row in masked_rows:
        item = {
            "station": str(row["station"]),
            "interval_start_utc": str(row["interval_start_utc"]),
            "y_true": row["y_true"],
            "y_hats": {str(k): v for k, v in dict(row["y_hats"]).items()},
        }
        out.append(item)
    return sorted(out, key=lambda r: (r["station"], r["interval_start_utc"]))


def compute_mask_id(set_id: str, member_ids: Sequence[str], masked_rows: Sequence[Mapping]) -> str:
    """R-107 limb 1: `mask_id` derives deterministically from the declared set and the
    masked row content — canonical JSON, sorted keys, no insignificant whitespace."""
    payload = {
        "set_id": str(set_id),
        "member_ids": sorted(str(m) for m in member_ids),
        "rows": _canonical_rows(masked_rows),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def assert_mask_id_reproduces(mask: ComparisonMask) -> None:
    """R-107 limb 1's executable half: recomputation reproduces the ID or RAISES.

    Raises
    ------
    FairnessError
        the recomputed `mask_id` differs from the recorded one — the mask's content and its
        identity have diverged, and a number computed over it would cite a mask that no
        longer exists (control 12).
    """
    recomputed = compute_mask_id(mask.set_id, mask.member_ids, mask.masked_rows)
    if recomputed != mask.mask_id:
        raise FairnessError(
            f"mask {mask.mask_id}",
            f"recomputation yields {recomputed}; a mask whose identity does not reproduce "
            f"from its declared set and row content is a failure, not a version (R-107 "
            f"limb 1; TS-C-03)",
        )


def assert_reporting_surface(mask: ComparisonMask) -> None:
    """Control (31): a registered mask missing any of the five reporting values FAILS.

    Raises
    ------
    FairnessError
        `mask_id`, `feature_set_id`, per-station surviving row counts, per-station exclusion
        counts, or the scored-window statement absent/empty — the reporting surface cannot
        be silently unsupplied (R-107 limb 6, Recommendation 16; Vision §8.9's "exclusions
        and row counts are reported" clause; D-28's 30-day disclosure).
    """
    missing = []
    if not mask.mask_id:
        missing.append("mask_id")
    if not mask.feature_set_id:
        missing.append("feature_set_id")
    if not isinstance(mask.row_counts, Mapping) or not mask.row_counts:
        missing.append("row_counts")
    if not isinstance(mask.exclusion_counts, Mapping) or not mask.exclusion_counts:
        missing.append("exclusion_counts")
    if not mask.scored_window_statement:
        missing.append("scored_window_statement")
    if missing:
        raise FairnessError(
            f"mask {mask.mask_id or '<no id>'}",
            f"reporting surface incomplete: {missing} absent; the five exposed values are "
            f"what regimes-diagnostics-reporting prints and never restates (R-107 limb 6)",
        )


def _rows_of(frame: Any) -> list[Mapping[str, Any]]:
    """Frame rows as record mappings — DataFrame (`to_dict`) or record-sequence form.

    The same stdlib-first stance as `src/features/_frames.py` (not imported: D-27 bars this
    package from `src/features` even transitively): production frames are DataFrames, tests
    and fixture machines may lack pandas, and every rule here is over VALUES, not a library
    type.
    """
    to_records = getattr(frame, "to_dict", None)
    if callable(to_records) and hasattr(frame, "columns"):
        return [dict(row) for row in frame.to_dict(orient="records")]
    out: list[Mapping[str, Any]] = []
    for index, row in enumerate(frame):
        if not isinstance(row, Mapping):
            raise IntegrityError(f"frame row {index}", "is not a record mapping")
        out.append(dict(row))
    return out


def _prediction_keys(prediction: Any) -> dict[tuple[str, str], Any]:
    keyed: dict[tuple[str, str], Any] = {}
    for row in _rows_of(prediction.frame):
        station = row.get("station")
        stamp = row.get("interval_start_utc")
        if station is None or stamp is None:
            raise IntegrityError(
                f"prediction {getattr(prediction, 'model_id', '?')} row",
                "carries no (station, interval_start_utc) key; the alignment key is the "
                "ordered pair R-92 fixed",
            )
        if row.get("y_hat") is not None:
            keyed[(str(station), str(stamp))] = row["y_hat"]
    return keyed


def _window_attrs(prediction: Any) -> tuple[Any, Any]:
    attrs = getattr(getattr(prediction, "frame", None), "attrs", None)
    if not isinstance(attrs, Mapping):
        return None, None
    lag = attrs.get("lag_set")
    return attrs.get("window_length_hours"), tuple(lag) if lag is not None else None


def build_comparison_mask(
    predictions: Sequence[Any],
    *,
    set_id: str,
    declared_sets: Mapping[str, Mapping[str, Any]],
    target: Any,
    feature_set_id: str,
    month_start: dt.datetime,
    month_end: dt.datetime,
    embargo_hours: int,
) -> ComparisonMask:
    """W-1: the one comparison-wide intersection mask, computed once per declared set.

    Ordered exactly as W-1 fixes it: (1) stamps first — `LeakageError` on a `None` stamp,
    `PartitionError` on a member `partition_id` mismatch; (2) membership exact against the
    declared set — `FairnessError` on missing/extra/duplicate/merged (and thereby on every
    pairwise attempt); matched windows asserted across members (control 28) —
    `FairnessError` on a window-length or lag-set mismatch; (3) intersection over the
    members' and the target's availability, exclusions COUNTED per station; (4) identity,
    stamps and the reporting surface.

    The scored-window statement is DERIVED from `month_start`/`month_end`/`embargo_hours`
    (the partition's own values, reaching this function from configuration): for the real
    locked partition it reads exactly D-28's "2–31 December 2022, 30 days, first 24 h
    excluded and counted".

    Raises
    ------
    LeakageError, PartitionError, FairnessError
        per the guard order above.
    IntegrityError
        identity-stamp disagreement between members (`phase_id`/`source_id`/
        `target_definition_id` — a comparison across target lineages, Vision §2.2/§6.6), a
        rowless intersection, or malformed rows.
    """
    members = list(predictions)
    require_stamps(members)  # W-1 step 1 first limb: None stamps (LeakageError)
    require_partition_agreement(members)  # second limb: PartitionError on mismatch
    member_ids = [str(getattr(p, "model_id")) for p in members]
    declared = require_declared_membership(
        member_ids, set_id=set_id, declared_sets=declared_sets
    )  # W-1 step 2 (FairnessError: missing/extra/duplicate/merged/pairwise)

    for key in _IDENTITY_KEYS:
        values = {str(getattr(p, key)) for p in members}
        if len(values) > 1:
            raise FairnessError(
                f"comparison set {set_id}",
                f"members disagree on {key} {sorted(values)}; a comparison across target "
                f"lineages is not a comparison (Vision §2.2/§6.6 stamp rule; TE §13)",
            )

    # Matched windows at the comparison boundary (R-111's limb; NFR-FAIR-01; control 28,
    # instantiated on the tier-3 set too — Vision §8.9's M-04/M-05 clause).
    windows = {m: _window_attrs(p) for m, p in zip(member_ids, members, strict=True)}
    stated = {(w, l) for (w, l) in windows.values() if w is not None or l is not None}
    if len(stated) > 1:
        raise FairnessError(
            f"comparison set {set_id}",
            f"members were scored over mismatched window lengths / lag sets "
            f"{ {m: v for m, v in windows.items()} }; every member of a comparison set is "
            f"scored over the same window length and lag set (NFR-FAIR-01; TA-11; Vision "
            f"§8.9's matched-window clause)",
        )
    window_length, lag_set = (next(iter(stated)) if stated else (None, None))

    # W-1 step 3: the intersection, with exclusions counted per station. The universe is
    # the target's observed rows (a row with no observed VTEC is scorable by no member).
    target_rows = _rows_of(target)
    universe: dict[tuple[str, str], Any] = {}
    for row in target_rows:
        station = row.get(_TARGET_STATION)
        stamp = row.get(_TARGET_TIMESTAMP)
        value = row.get(_TARGET_VALUE)
        if station is None or stamp is None:
            raise IntegrityError(
                "target frame row", "carries no (station_id, interval_start_utc) key"
            )
        if value is not None:
            universe[(str(station), str(stamp))] = value
    member_keys = {m: _prediction_keys(p) for m, p in zip(member_ids, members, strict=True)}
    surviving = [
        key for key in sorted(universe) if all(key in keys for keys in member_keys.values())
    ]
    if not surviving:
        raise IntegrityError(
            f"comparison set {set_id}",
            "the intersection over the members' and the target's availability is empty; a "
            "mask over zero rows masks nothing and a check over zero rows is not a check",
        )
    row_counts: dict[str, int] = {}
    exclusion_counts: dict[str, int] = {}
    surviving_set = set(surviving)
    for station, _ in universe:
        row_counts.setdefault(station, 0)
        exclusion_counts.setdefault(station, 0)
    for key in universe:
        if key in surviving_set:
            row_counts[key[0]] += 1
        else:
            exclusion_counts[key[0]] += 1

    masked_rows = tuple(
        {
            "station": station,
            "interval_start_utc": stamp,
            "y_true": universe[(station, stamp)],
            "y_hats": {m: member_keys[m][(station, stamp)] for m in member_ids},
        }
        for station, stamp in surviving
    )

    # W-1 step 4: identity, stamps, the reporting surface.
    statement = scored_window_statement(month_start, month_end, embargo_hours=embargo_hours)
    template = members[0]
    mask = ComparisonMask(
        mask_id=compute_mask_id(set_id, declared, masked_rows),
        set_id=str(set_id),
        feature_set_id=str(feature_set_id),
        partition_id=str(getattr(template, "partition_id")),
        member_ids=tuple(declared),
        member_transform_ids=tuple(
            sorted({str(getattr(p, "transform_id")) for p in members})
        ),
        phase_id=str(getattr(template, "phase_id")),
        source_id=str(getattr(template, "source_id")),
        target_definition_id=str(getattr(template, "target_definition_id")),
        row_counts=dict(sorted(row_counts.items())),
        exclusion_counts=dict(sorted(exclusion_counts.items())),
        masked_rows=masked_rows,
        scored_window_statement=statement,
        window_length_hours=window_length,
        lag_set=tuple(lag_set or ()),
    )
    assert_reporting_surface(mask)
    return mask


def _write_once_atomic(path: Path, payload: bytes, *, what: str) -> None:
    """The project's durable write-once idiom: `.tmp` → flush+fsync → `os.replace`.

    A second write of a write-once artifact REFUSES (Q4 = A); a reader never sees a partial
    file (the rename is atomic on one filesystem).

    Raises
    ------
    FairnessError
        the target already exists — write-once is a check, not a description.
    IntegrityError
        the durable write fails at any step; the artifact is then not recorded.
    """
    path = Path(path)
    if path.exists():
        raise FairnessError(
            path,
            f"{what} already exists; it is written exactly once per freeze and never "
            f"overwritten (Q4 = A; R-107 limb 4's once-only posture; NFR-AUD-01's "
            f"no-silent-replacement rule)",
        )
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
        try:
            written = os.write(fd, payload)
            if written != len(payload):
                raise IntegrityError(tmp, f"wrote {written} of {len(payload)} bytes")
            os.fsync(fd)
        finally:
            os.close(fd)
        os.replace(tmp, path)  # atomic: a reader sees the old or the new file, never partial
    except OSError as exc:
        raise IntegrityError(
            path, f"durable write of {what} failed ({exc}); nothing is recorded"
        ) from exc


class MaskRegistry:
    """R-107's registry: once-only registration, the read path, the write-once freeze.

    One directory, one JSON entry per comparison set (``mask_<set_id>.json``), plus the
    write-once ``frozen_bundle_manifest.json`` enumerating the bundle's ``mask_id``s and
    content hashes — the artifact SD-C-02's containment check hashes into the access record,
    and part of the G-05 frozen bundle (FR-P1-05-17: required here, produced by the G-05
    record).
    """

    def __init__(self, registry_dir: Path) -> None:
        self.registry_dir = Path(registry_dir)

    # --- read path (consumed by guards.require_registered_mask and SD-C-02) -----------

    def _entry_path(self, set_id: str) -> Path:
        return self.registry_dir / f"mask_{set_id}.json"

    @property
    def manifest_path(self) -> Path:
        return self.registry_dir / FROZEN_BUNDLE_MANIFEST_NAME

    def lookup(self, set_id: str) -> Mapping[str, Any] | None:
        path = self._entry_path(str(set_id))
        if not path.is_file():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            raise IntegrityError(path, f"registry entry is unreadable ({exc})") from exc

    def frozen(self) -> bool:
        return self.manifest_path.is_file()

    # --- write path --------------------------------------------------------------------

    def register(self, mask: ComparisonMask) -> Mapping[str, Any]:
        """Register a mask ONCE for its comparison set (R-107 limb 4).

        Raises
        ------
        FairnessError
            a second registration for the same set — "computed once per comparison set" is
            a check, not a description (control 13); or a registration after the bundle is
            frozen — the freeze is the G-05 boundary and a post-freeze mask cannot join it.
        """
        assert_mask_id_reproduces(mask)
        assert_reporting_surface(mask)
        if self.frozen():
            raise FairnessError(
                self.manifest_path,
                f"the frozen-bundle manifest already exists; mask {mask.mask_id} cannot "
                f"register after the freeze (R-107 limb 5: the registered set sits inside "
                f"the G-05 frozen bundle)",
            )
        existing = self.lookup(mask.set_id)
        if existing is not None:
            raise FairnessError(
                self._entry_path(mask.set_id),
                f"comparison set {mask.set_id!r} already holds registered mask "
                f"{existing.get('mask_id')!r}; the mask is computed ONCE per comparison "
                f"set and a second registration raises (R-107 limb 4; FR-P1-04-7)",
            )
        entry = {
            "artifact_class": "comparison_mask_registration",
            "set_id": mask.set_id,
            "mask_id": mask.mask_id,
            "feature_set_id": mask.feature_set_id,
            "partition_id": mask.partition_id,
            "member_ids": list(mask.member_ids),
            "member_transform_ids": list(mask.member_transform_ids),
            "phase_id": mask.phase_id,
            "source_id": mask.source_id,
            "target_definition_id": mask.target_definition_id,
            "row_counts": dict(mask.row_counts),
            "exclusion_counts": dict(mask.exclusion_counts),
            "scored_window_statement": mask.scored_window_statement,
            "window_length_hours": mask.window_length_hours,
            "lag_set": list(mask.lag_set),
            "registered_at_utc": dt.datetime.now(dt.UTC).isoformat(),
        }
        payload = (json.dumps(entry, sort_keys=True, indent=2) + "\n").encode("utf-8")
        _write_once_atomic(self._entry_path(mask.set_id), payload, what="mask registration")
        return entry

    def freeze_bundle(self) -> Mapping[str, Any]:
        """Write the frozen-bundle manifest ONCE (Q4 = A; SD-C-02's hash target).

        Enumerates every registered mask's `set_id`, `mask_id` and registration-entry
        content hash. The manifest is the append-immune artifact whose SHA-256
        `open_restricted` records as `mask_registry_hash` — write-once per freeze, so a
        correct access record can never fail post-hoc re-verification after an append
        (the Recommendation-8 narrowing at nfr-design).

        Raises
        ------
        FairnessError
            a second freeze — the manifest is write-once (see the module docstring's race
            analysis); or a freeze over an empty registry (a bundle of nothing freezes
            nothing).
        """
        entries: dict[str, Mapping[str, Any]] = {}
        for path in sorted(self.registry_dir.glob("mask_*.json")):
            entry = json.loads(path.read_text(encoding="utf-8"))
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            entries[str(entry["set_id"])] = {
                "mask_id": str(entry["mask_id"]),
                "entry_sha256": digest,
            }
        if not entries:
            raise FairnessError(
                self.registry_dir,
                "no registered mask exists; a frozen bundle over an empty registry would "
                "evidence a freeze that froze nothing",
            )
        manifest = {
            "artifact_class": "frozen_mask_bundle_manifest",
            "mask_ids": sorted(e["mask_id"] for e in entries.values()),
            "entries": entries,
            "frozen_at_utc": dt.datetime.now(dt.UTC).isoformat(),
        }
        payload = (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode("utf-8")
        _write_once_atomic(self.manifest_path, payload, what="frozen-bundle manifest")
        return manifest
