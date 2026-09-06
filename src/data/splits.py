"""F-3 Partition set: the six partitions, the five-row split manifest, the embargo, the lock.

Purpose
-------
`features-and-splits` W-5 / W-6 (R-80, R-82, R-83; SD-F-04, SD-F-05). This module owns the
`Partition` shape and everything that makes a fold boundary the frozen calendar boundary and
nothing else:

* `Partition` carries **both** bounds of its training range (`train_start` and `train_end`,
  R-83 / BLK-09, approved 2026-09-05 under
  `governance/CHANGE_RECORD_2026-09-05_R74_R83_leakage_contracts.md`) plus `validation_month`
  and `embargo_hours`. Every calendar VALUE is read from `configs/data.yaml` (the six
  partitions) and `configs/experiment.yaml` (`embargo_hours`) by `build_partitions`; none is
  written here (TC-03e). While those fields are absent or carry `TBD — freeze gate`,
  `build_partitions` REFUSES, naming the field — the values enter only at their freeze.
* `build_partitions` returns exactly **6** (`F1`…`F4`, `REFIT`, `DEC`); the split manifest
  FR-P1-04-5 gates on enumerates exactly **5** (`F1`…`F4`, `REFIT`); the locked partition's
  record is kept SEPARATE because it is access-gated and the manifest is not. A manifest of
  six rows fails, and so does one of four.
* Structural checks that need no calendar constant: the six ids are a closed set; `None`
  `validation_month` means `REFIT` alone; each month of the study year has exactly one
  evaluation ROLE (the reading of Vision 8.1 adopted so the check can run — carried to the
  gate, not settled here); `DEC.train_end == REFIT.train_end`, so a December fit is
  unrepresentable by the field itself (R-80's Recommendation-25 bar).
* The 24-hour embargo (value from config) is EXCLUDED AND COUNTED, never silently dropped.
* `assert_membership_from_timestamps` VALIDATES rows against the partition and role they are
  filed under, from record timestamps only — never a directory or file name — and DERIVES
  nothing: the training ranges nest, so no per-row partition label exists.
* `materialise_locked_partition` is ADR-03's EXECUTION limb: `LockedTestError` when
  `g05_signature` is `None` or fails verification. The READ limb is `governance-guards`'
  `locked_test.open_restricted`; this module never names the restricted root.

Inputs
------
A `ConfigSnapshot` (`configs/data.yaml` `partitions` and `gates.G-05`;
`configs/experiment.yaml` `embargo_hours`), frames or timestamp sequences supplied by the
caller. No file is read here; no third-party package is imported at module scope.

Re-run behaviour
----------------
Pure functions of their inputs; deterministic; nothing persisted. `materialise_locked_partition`
never reads December itself — it takes a caller-supplied loader that must route through
`open_restricted`, and refuses before calling it unless the G-05 signature verifies.

Boundaries this module holds
----------------------------
No scientific constant in source: no calendar year, no embargo length, no month number.
The one literal allowed is the closed six-value id space (identities, not values).
`scikit-learn`'s splitters are not used (TS-F-04). No December content is read or constructed
in this module or its tests.
"""

from __future__ import annotations

import datetime as dt
import hashlib
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Final

from src.data.config import (
    TBD_SENTINEL,
    ConfigSnapshot,
    LockedTestError,
    PartitionError,
)

__all__ = [
    "PARTITION_IDS",
    "FITTING_PARTITION_IDS",
    "REFIT_ID",
    "LOCKED_ID",
    "PartitionKind",
    "Partition",
    "build_partitions",
    "partition_by_id",
    "training_range",
    "validation_month_range",
    "embargo_window",
    "embargo_exclusions",
    "apply_embargo",
    "RecordFrame",
    "build_split_manifest",
    "assert_split_manifest",
    "locked_partition_record",
    "assert_membership_from_timestamps",
    "verify_g05_signature",
    "materialise_locked_partition",
]

#: R-80's closed six-value id space — identities, never values (`models-and-baselines`
#: relies on `partition_id` taking no seventh value without this table changing first).
PARTITION_IDS: Final[tuple[str, ...]] = ("F1", "F2", "F3", "F4", "REFIT", "DEC")
REFIT_ID: Final[str] = "REFIT"
LOCKED_ID: Final[str] = "DEC"
#: The fitting-capable set: every partition a transform may be fitted for, and exactly
#: the rows the split manifest enumerates (derived, not asserted: PARTITION_IDS minus DEC).
FITTING_PARTITION_IDS: Final[tuple[str, ...]] = tuple(
    pid for pid in PARTITION_IDS if pid != LOCKED_ID
)

_UTC: Final = dt.UTC


class PartitionKind(StrEnum):
    """`fold` (F1…F4), `refit` (REFIT), `locked` (DEC) — ADR-11's closed kind space."""

    fold = "fold"
    refit = "refit"
    locked = "locked"


@dataclass(frozen=True)
class Partition:
    """ADR-11's `Partition`, extended by R-83's `train_start` (approved 2026-09-05).

    `validation_month` is the first day of the evaluated month; `None` means the final refit
    ALONE (FR-P1-04-14: scored nowhere). `DEC` carries its locked month. `embargo_hours` has
    NO default here: the approved contract wrote `= 24`, but `project.md` forbids a scientific
    constant in source, so the value reaches this field from `configs/experiment.yaml` via
    `build_partitions` and nowhere else — a narrowing of the approved shape, recorded in the
    code-generation summary.
    """

    partition_id: str
    kind: PartitionKind
    train_start: dt.date
    train_end: dt.date
    validation_month: dt.date | None
    embargo_hours: int


# --- config reading helpers -------------------------------------------------------------


def _is_tbd(value: object) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == TBD_SENTINEL)


def _as_date(value: object, *, resource: str) -> dt.date:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value.strip())
        except ValueError as exc:
            raise PartitionError(
                resource, f"value {value!r} is not an ISO calendar date (YYYY-MM-DD)"
            ) from exc
    raise PartitionError(resource, f"value {value!r} is not a calendar date")


def _month_start(day: dt.date) -> dt.date:
    return day.replace(day=1)


def _next_month(day: dt.date) -> dt.date:
    first = _month_start(day)
    if first.month == 12:
        return first.replace(year=first.year + 1, month=1)
    return first.replace(month=first.month + 1)


def _months_between(start: dt.date, end_inclusive: dt.date) -> list[dt.date]:
    months: list[dt.date] = []
    cursor = _month_start(start)
    last = _month_start(end_inclusive)
    while cursor <= last:
        months.append(cursor)
        cursor = _next_month(cursor)
    return months


def _midnight(day: dt.date) -> dt.datetime:
    return dt.datetime(day.year, day.month, day.day, tzinfo=_UTC)


def _as_utc(value: object, *, resource: str) -> dt.datetime:
    """Normalise a record timestamp to an aware UTC datetime (naive values are UTC)."""
    if isinstance(value, dt.datetime):
        stamp = value
    elif isinstance(value, dt.date):
        stamp = _midnight(value)
    elif isinstance(value, str):
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            stamp = dt.datetime.fromisoformat(text)
        except ValueError as exc:
            raise PartitionError(resource, f"timestamp {value!r} is not ISO-8601") from exc
    else:
        # pandas.Timestamp and numpy datetime64 expose to_pydatetime / isoformat.
        to_py = getattr(value, "to_pydatetime", None)
        if callable(to_py):
            stamp = to_py()
        else:
            raise PartitionError(resource, f"timestamp {value!r} has an unrecognised type")
    if stamp.tzinfo is None:
        return stamp.replace(tzinfo=_UTC)
    return stamp.astimezone(_UTC)


# --- W-5: build_partitions --------------------------------------------------------------


def _read_embargo_hours(snapshot: ConfigSnapshot) -> int:
    value = snapshot.experiment.get("embargo_hours")
    if _is_tbd(value):
        raise PartitionError(
            "configs/experiment.yaml: embargo_hours",
            "absent or unresolved (TBD — freeze gate); the 24-hour embargo's VALUE enters "
            "from configuration at its freeze, never from source (TC-03e; TE 7.1; "
            "FR-P1-04-5) — stop and report, never default (TE 18.3)",
        )
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise PartitionError(
            "configs/experiment.yaml: embargo_hours",
            f"value {value!r} is not a positive integer number of hours",
        )
    return value


def _read_partition_block(snapshot: ConfigSnapshot) -> Mapping[str, Mapping[str, Any]]:
    block = snapshot.data.get("partitions")
    if _is_tbd(block):
        raise PartitionError(
            "configs/data.yaml: partitions",
            "absent or unresolved (TBD — freeze gate); every partition's train_start, "
            "train_end and validation_month are configuration frozen under a D-number "
            "(R-83, BLK-09; R-80's table; D-8; D-28), never a hard-coded calendar in "
            "src/data/splits.py and never derived from the data's earliest row — "
            "stop and report, never default (TE 18.3)",
        )
    if not isinstance(block, Mapping):
        raise PartitionError(
            "configs/data.yaml: partitions",
            f"must be a mapping of partition_id -> fields, got {type(block).__name__}",
        )
    declared = {str(key) for key in block}
    expected = set(PARTITION_IDS)
    if declared != expected:
        raise PartitionError(
            "configs/data.yaml: partitions",
            f"must declare exactly the six partition ids {list(PARTITION_IDS)}; missing "
            f"{sorted(expected - declared)}, unexpected {sorted(declared - expected)} "
            f"(R-80's closed six-value space)",
        )
    for pid, entry in block.items():
        if not isinstance(entry, Mapping):
            raise PartitionError(
                f"configs/data.yaml: partitions.{pid}", "entry must be a mapping of fields"
            )
    return {str(k): v for k, v in block.items()}


def _expected_kind(pid: str) -> PartitionKind:
    if pid == REFIT_ID:
        return PartitionKind.refit
    if pid == LOCKED_ID:
        return PartitionKind.locked
    return PartitionKind.fold


def _partition_from_entry(pid: str, entry: Mapping[str, Any], embargo_hours: int) -> Partition:
    resource = f"configs/data.yaml: partitions.{pid}"
    for field_name in ("kind", "train_start", "train_end"):
        if _is_tbd(entry.get(field_name)):
            raise PartitionError(
                f"{resource}.{field_name}",
                "absent or unresolved (TBD — freeze gate); enters at the split-boundary "
                "freeze under its D-number (R-83), never by an implementer's convenience",
            )
    try:
        kind = PartitionKind(str(entry["kind"]))
    except ValueError as exc:
        raise PartitionError(
            f"{resource}.kind",
            f"{entry['kind']!r} is not one of {[k.value for k in PartitionKind]}",
        ) from exc
    if kind is not _expected_kind(pid):
        raise PartitionError(
            f"{resource}.kind",
            f"{kind.value!r} disagrees with the id: {pid!r} must be "
            f"{_expected_kind(pid).value!r} (ADR-11's closed kind space)",
        )
    train_start = _as_date(entry["train_start"], resource=f"{resource}.train_start")
    train_end = _as_date(entry["train_end"], resource=f"{resource}.train_end")
    if train_start > train_end:
        raise PartitionError(
            resource, f"train_start {train_start} is after train_end {train_end}"
        )
    raw_month = entry.get("validation_month")
    if pid == REFIT_ID:
        if raw_month is not None:
            raise PartitionError(
                f"{resource}.validation_month",
                "the final refit is scored nowhere (FR-P1-04-14); its validation_month "
                "must be null — None means REFIT alone (ADR-11 M5)",
            )
        validation_month: dt.date | None = None
    else:
        if _is_tbd(raw_month):
            raise PartitionError(
                f"{resource}.validation_month",
                "absent or unresolved; every fold and the locked partition names the month "
                "it evaluates (ADR-11 M5: only REFIT carries None)",
            )
        validation_month = _as_date(raw_month, resource=f"{resource}.validation_month")
        if validation_month != _month_start(validation_month):
            raise PartitionError(
                f"{resource}.validation_month",
                f"{validation_month} is not the first day of a month",
            )
        if validation_month <= train_end:
            raise PartitionError(
                resource,
                f"validation_month {validation_month} does not follow train_end "
                f"{train_end}; a validation month inside the training range is leakage by "
                f"construction",
            )
        if kind is PartitionKind.fold and validation_month != train_end + dt.timedelta(days=1):
            raise PartitionError(
                resource,
                f"fold validation_month {validation_month} is not the day after train_end "
                f"{train_end}; TE 7.1's folds are contiguous calendar blocks (no window "
                f"crosses a boundary, and no month is left between them)",
            )
    return Partition(
        partition_id=pid,
        kind=kind,
        train_start=train_start,
        train_end=train_end,
        validation_month=validation_month,
        embargo_hours=embargo_hours,
    )


def _assert_structural_rules(partitions: Sequence[Partition]) -> None:
    """The checks that need no calendar value: the December-fit bar and exactly-one role."""
    by_id = {p.partition_id: p for p in partitions}
    refit = by_id[REFIT_ID]
    locked = by_id[LOCKED_ID]

    # R-80 (Recommendation 25): DEC.train_end == REFIT.train_end — the locked partition never
    # fits beyond the refit's range, so a fit that includes the locked month is
    # unrepresentable by the field itself.
    if locked.train_end != refit.train_end:
        raise PartitionError(
            "configs/data.yaml: partitions.DEC.train_end",
            f"{locked.train_end} differs from REFIT.train_end {refit.train_end}; R-80 fixes "
            f"DEC.train_end to the refit's boundary so that a locked-month fit is "
            f"unrepresentable by the field (Recommendation 25, board option 1)",
        )
    assert locked.validation_month is not None  # enforced per-entry above
    if locked.validation_month <= locked.train_end:
        raise PartitionError(
            "configs/data.yaml: partitions.DEC",
            "the locked month lies inside DEC's training range",
        )

    # Exactly one evaluation ROLE per month (Vision 8.1, read over roles because the training
    # ranges nest — a reading carried to the gate). Overlap and gap both fail.
    roles: dict[dt.date, str] = {}
    for partition in partitions:
        if partition.validation_month is None:
            continue
        month = partition.validation_month
        if month in roles:
            raise PartitionError(
                "configs/data.yaml: partitions",
                f"month {month.isoformat()} carries two evaluation roles "
                f"({roles[month]} and {partition.partition_id}); each month has exactly one "
                f"(Vision 8.1, evaluation-role reading)",
            )
        roles[month] = partition.partition_id
    study_start = min(p.train_start for p in partitions)
    training_only_months = set(_months_between(refit.train_start, refit.train_end))
    for month in _months_between(study_start, locked.validation_month):
        if month not in roles and month not in training_only_months:
            raise PartitionError(
                "configs/data.yaml: partitions",
                f"month {month.isoformat()} has NO role: it is neither any partition's "
                f"validation month, nor the locked month, nor inside the final refit's "
                f"training range (Vision 8.1: a gap fails exactly as an overlap does)",
            )
    for partition in partitions:
        if partition.train_start != study_start:
            raise PartitionError(
                f"configs/data.yaml: partitions.{partition.partition_id}.train_start",
                f"{partition.train_start} differs from the study start {study_start}; "
                f"TE 7.1's folds are an expanding window from one origin (D-8's calendar "
                f"boundary), and a differing lower bound is where an embargo silently moves",
            )


def build_partitions(snapshot: ConfigSnapshot) -> tuple[Partition, ...]:
    """ADR-11's `build_partitions`: exactly six partitions, every value from configuration.

    Raises
    ------
    PartitionError
        when `data.partitions` or `experiment.embargo_hours` is absent or `TBD — freeze
        gate` (the refusal, not a default); when the block does not declare exactly the six
        ids; when an entry's kind, dates or validation month are malformed or disagree with
        the id; when `DEC.train_end != REFIT.train_end`; or when a month has two evaluation
        roles or none.
    """
    embargo_hours = _read_embargo_hours(snapshot)
    block = _read_partition_block(snapshot)
    partitions = tuple(
        _partition_from_entry(pid, block[pid], embargo_hours) for pid in PARTITION_IDS
    )
    _assert_structural_rules(partitions)
    return partitions


def partition_by_id(partitions: Sequence[Partition], partition_id: str) -> Partition:
    """The named partition, or `PartitionError` when the id names none (R-92's shape)."""
    for partition in partitions:
        if partition.partition_id == partition_id:
            return partition
    raise PartitionError(
        f"partition_id {partition_id!r}",
        f"names no partition in the list {[p.partition_id for p in partitions]}; the "
        f"six-value space is closed (R-80)",
    )


# --- ranges, embargo --------------------------------------------------------------------


def training_range(partition: Partition) -> tuple[dt.datetime, dt.datetime]:
    """`[train_start 00:00, train_end + 1 day 00:00)` as aware UTC datetimes (end exclusive)."""
    return _midnight(partition.train_start), _midnight(partition.train_end + dt.timedelta(days=1))


def validation_month_range(partition: Partition) -> tuple[dt.datetime, dt.datetime]:
    """`[validation_month 00:00, next month 00:00)`; `PartitionError` for REFIT."""
    if partition.validation_month is None:
        raise PartitionError(
            f"partition {partition.partition_id}",
            "has no validation month (the final refit is scored nowhere, FR-P1-04-14); a "
            "score-role range cannot be derived for it",
        )
    start = _midnight(partition.validation_month)
    return start, _midnight(_next_month(partition.validation_month))


def embargo_window(partition: Partition) -> tuple[dt.datetime, dt.datetime]:
    """The first `embargo_hours` of the validation month: `[start, start + embargo)`."""
    start, _ = validation_month_range(partition)
    return start, start + dt.timedelta(hours=partition.embargo_hours)


def embargo_exclusions(
    timestamps: Iterable[object], partition: Partition
) -> tuple[tuple[int, ...], int]:
    """Indices of rows OUTSIDE the embargo window, and the count of rows excluded by it.

    The count is the load-bearing output (FR-P1-04-5 "excluded and counted"): a silent
    exclusion and a counted one are indistinguishable at the artifact.
    """
    start, end = embargo_window(partition)
    kept: list[int] = []
    excluded = 0
    for index, raw in enumerate(timestamps):
        stamp = _as_utc(raw, resource=f"row {index}")
        if start <= stamp < end:
            excluded += 1
        else:
            kept.append(index)
    return tuple(kept), excluded


def _timestamps_of(frame: Any, column: str) -> list[object]:
    """Record timestamps of a DataFrame column or of a sequence of record mappings."""
    if hasattr(frame, "columns") and hasattr(frame, "__getitem__"):
        if column not in list(frame.columns):
            raise PartitionError(
                f"frame column {column!r}",
                f"absent; membership derives from record timestamps and needs the "
                f"timestamp column (columns present: {list(frame.columns)})",
            )
        return list(frame[column])
    rows = list(frame)
    out: list[object] = []
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping) or column not in row:
            raise PartitionError(
                f"row {index}", f"carries no {column!r} timestamp; membership derives from it"
            )
        out.append(row[column])
    return out


class RecordFrame(list):
    """A sequence of record mappings carrying an `attrs` dict, mirroring `DataFrame.attrs`.

    Used where a caller supplies plain records instead of a `pandas.DataFrame` (tests and
    fixtures); production frames are DataFrames. Exists so the counted exclusion is never
    lost on the non-DataFrame path.
    """

    def __init__(self, rows: Iterable[Mapping[str, Any]] = ()) -> None:
        super().__init__(rows)
        self.attrs: dict[str, Any] = {}


def _take_rows(frame: Any, indices: Sequence[int]) -> Any:
    if hasattr(frame, "iloc"):
        return frame.iloc[list(indices)].reset_index(drop=True)
    rows = list(frame)
    return RecordFrame(rows[i] for i in indices)


def apply_embargo(
    frame: Any, partition: Partition, *, timestamp_column: str = "interval_start_utc"
) -> tuple[Any, int]:
    """Drop the embargo rows from a score-role frame and RETURN THE COUNT alongside.

    `frame` is a `pandas.DataFrame` (or, in tests, a sequence of record mappings). The
    returned pair is `(kept_frame, excluded_count)`; the caller records the count in the
    split manifest or the bundle — never console text only (team.md two-tier posture).
    """
    kept, excluded = embargo_exclusions(_timestamps_of(frame, timestamp_column), partition)
    return _take_rows(frame, kept), excluded


# --- the split manifest (5 rows) and the locked record (separate) ------------------------


def build_split_manifest(
    partitions: Sequence[Partition], *, excluded_embargo_rows: Mapping[str, int]
) -> dict[str, Any]:
    """FR-P1-04-5's split manifest: exactly the five fitting-capable partitions.

    `excluded_embargo_rows` maps each FOLD id to the number of rows its embargo excluded
    (counted by `apply_embargo`). A fold without a count is refused: an omitted count is
    the negative control R-80 names.
    """
    rows: list[dict[str, Any]] = []
    for pid in FITTING_PARTITION_IDS:
        partition = partition_by_id(partitions, pid)
        row: dict[str, Any] = {
            "partition_id": pid,
            "kind": partition.kind.value,
            "train_start": partition.train_start.isoformat(),
            "train_end": partition.train_end.isoformat(),
            "validation_month": (
                partition.validation_month.isoformat() if partition.validation_month else None
            ),
            "embargo_hours": partition.embargo_hours,
        }
        if partition.kind is PartitionKind.fold:
            if pid not in excluded_embargo_rows:
                raise PartitionError(
                    f"split manifest row {pid}",
                    "excluded-row count omitted; FR-P1-04-5 requires the embargo's first "
                    "24 h excluded AND counted — a manifest without the count fails",
                )
            row["excluded_embargo_rows"] = int(excluded_embargo_rows[pid])
        else:
            row["excluded_embargo_rows"] = None
        rows.append(row)
    manifest = {
        "artifact_class": "split_manifest",
        "partition_count": len(rows),
        "partitions": rows,
        "locked_partition_recorded_separately": True,
        "cross_validation": "exact fixed calendar boundaries; no random or shuffled CV",
    }
    assert_split_manifest(manifest)
    return manifest


def assert_split_manifest(manifest: Mapping[str, Any]) -> None:
    """A manifest carrying six rows fails FR-P1-04-5, and so does one carrying four."""
    rows = manifest.get("partitions")
    if not isinstance(rows, Sequence) or isinstance(rows, str):
        raise PartitionError("split manifest", "carries no `partitions` row list")
    ids = [str(row.get("partition_id")) for row in rows]
    if LOCKED_ID in ids:
        raise PartitionError(
            "split manifest",
            f"enumerates {LOCKED_ID}; the locked partition is access-gated and is recorded "
            f"separately, never as a manifest row (ADR-11 M5)",
        )
    if ids != list(FITTING_PARTITION_IDS):
        raise PartitionError(
            "split manifest",
            f"enumerates {ids} ({len(ids)} rows); FR-P1-04-5 requires exactly the "
            f"{len(FITTING_PARTITION_IDS)} partitions {list(FITTING_PARTITION_IDS)} in order",
        )
    if manifest.get("partition_count") != len(FITTING_PARTITION_IDS):
        raise PartitionError(
            "split manifest",
            f"partition_count {manifest.get('partition_count')!r} disagrees with the "
            f"{len(FITTING_PARTITION_IDS)} rows",
        )
    for row in rows:
        if row.get("kind") == PartitionKind.fold.value and not isinstance(
            row.get("excluded_embargo_rows"), int
        ):
            raise PartitionError(
                f"split manifest row {row.get('partition_id')}",
                "fold row carries no integer excluded_embargo_rows count (FR-P1-04-5)",
            )


def locked_partition_record(
    partitions: Sequence[Partition], *, access_gate_state: str
) -> dict[str, Any]:
    """The locked partition's SEPARATE record: its evaluated month and access-gate state."""
    locked = partition_by_id(partitions, LOCKED_ID)
    assert locked.validation_month is not None
    if not access_gate_state.strip():
        raise PartitionError("locked partition record", "access_gate_state is empty")
    return {
        "artifact_class": "locked_partition_record",
        "partition_id": LOCKED_ID,
        "kind": locked.kind.value,
        "evaluated_month": locked.validation_month.isoformat(),
        "train_end": locked.train_end.isoformat(),
        "embargo_hours": locked.embargo_hours,
        "access_gate_state": access_gate_state,
        "recorded_separately_from_split_manifest": True,
    }


# --- membership from record timestamps ---------------------------------------------------


def assert_membership_from_timestamps(
    frame: Any,
    *,
    partition: Partition,
    role: str,
    timestamp_column: str = "interval_start_utc",
) -> None:
    """Validate every row's record timestamp against the partition and role it is filed under.

    Derives NOTHING (the training ranges nest, so no per-row partition label exists; any
    leakage check that needs "which partition" compares declared identities). Raises
    `PartitionError` on the first row whose timestamp lies outside the declared range —
    the defect that filed locked-month records into a January evidence directory by
    directory name. The approved `(frame) -> None` signature is extended with keyword-only
    `partition` and `role`, because a frame carries no declaration of what it is filed
    under and the check is meaningless without one.
    """
    if role == "train":
        start, end = training_range(partition)
    elif role == "score":
        start, end = validation_month_range(partition)
    else:
        raise PartitionError(f"role {role!r}", "is not one of 'train' | 'score'")
    for index, raw in enumerate(_timestamps_of(frame, timestamp_column)):
        stamp = _as_utc(raw, resource=f"row {index}")
        if not (start <= stamp < end):
            raise PartitionError(
                f"row {index} ({stamp.isoformat()})",
                f"lies outside the {role} range {start.isoformat()}..{end.isoformat()} of "
                f"partition {partition.partition_id}; membership is derived from record "
                f"timestamps, never from the directory or file a row was filed under",
            )


# --- W-6 / R-82: the execution limb of the locked-test guard ----------------------------


def verify_g05_signature(snapshot: ConfigSnapshot, g05_signature: str | None) -> bool:
    """True only when `data.gates.G-05` is a signed record whose hash matches the signature.

    The signature artifact is a caller-supplied string; it verifies when
    `sha256(signature) == gates.G-05.signature_sha256` AND `gates.G-05.status == "signed"`
    AND a `decision` (D-number) is recorded. Any absent or `TBD` field is `False` — the
    gate is `Blocked` today and nothing here can open it.
    """
    if not g05_signature:
        return False
    gates = snapshot.data.get("gates")
    if not isinstance(gates, Mapping):
        return False
    node = gates.get("G-05")
    if not isinstance(node, Mapping):
        return False
    status = node.get("status")
    recorded = node.get("signature_sha256")
    decision = node.get("decision")
    if _is_tbd(status) or _is_tbd(recorded) or _is_tbd(decision):
        return False
    if str(status).strip().lower() != "signed":
        return False
    digest = hashlib.sha256(str(g05_signature).encode("utf-8")).hexdigest()
    return digest == str(recorded).strip().lower()


def materialise_locked_partition(
    snapshot: ConfigSnapshot,
    *,
    g05_signature: str | None,
    loader: Callable[[Partition], Any] | None = None,
    partitions: Sequence[Partition] | None = None,
    timestamp_column: str = "interval_start_utc",
) -> Any:
    """ADR-03's EXECUTION limb: materialise `DEC` only against a verifying G-05 signature.

    Raises
    ------
    LockedTestError
        when `g05_signature` is `None`; when it fails verification against
        `configs/data.yaml` `gates.G-05`; or when no `loader` is supplied (this function
        owns no read path — reads under the restricted root go through
        `governance-guards`' `open_restricted`, which the loader must call).
    PartitionError
        when the loaded rows are not the locked month's (membership from timestamps).

    Returns the loaded frame with the first `embargo_hours` EXCLUDED AND COUNTED (D-28: the
    scored set is the month less its first 24 h; the count is recorded on the frame as
    `attrs["excluded_embargo_rows"]` where the frame supports `attrs`, and returned
    through `apply_embargo` otherwise).
    """
    if g05_signature is None:
        raise LockedTestError(
            f"partition {LOCKED_ID}",
            "g05_signature is None; the December partition materialises only after G-05 is "
            "signed and the signature verifies — the pre-G-05 EXECUTION block WS-18 "
            "evidences (R-82, ADR-03). The required pre-G-05 coverage audit is a READ and "
            "belongs to open_restricted, not to this function",
        )
    if not verify_g05_signature(snapshot, g05_signature):
        raise LockedTestError(
            f"partition {LOCKED_ID}",
            "g05_signature fails verification against configs/data.yaml gates.G-05 (absent, "
            "TBD, not 'signed', or its sha256 does not match); a signature that does not "
            "verify is no signature (R-82)",
        )
    resolved = tuple(partitions) if partitions is not None else build_partitions(snapshot)
    locked = partition_by_id(resolved, LOCKED_ID)
    if loader is None:
        raise LockedTestError(
            f"partition {LOCKED_ID}",
            "no loader supplied; this function owns the execution limb only and never reads "
            "the restricted root itself — supply a loader that routes through "
            "locked_test.open_restricted (ADR-03, R-28 one door)",
        )
    frame = loader(locked)
    assert_membership_from_timestamps(
        frame, partition=locked, role="score", timestamp_column=timestamp_column
    )
    kept, excluded = apply_embargo(frame, locked, timestamp_column=timestamp_column)
    attrs = getattr(kept, "attrs", None)
    if isinstance(attrs, dict):
        attrs["excluded_embargo_rows"] = excluded
        attrs["partition_id"] = LOCKED_ID
    return kept
