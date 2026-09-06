"""F-2 (window half): ONE window definition, two representations, and the comparison mask.

Purpose
-------
`features-and-splits` W-4 / R-81 / SD-F-06 and the NFR-FAIR-01 mask (SD-F-04):

* `build_windows` is the single window definition. For every (station, epoch t) inside the
  scored range it takes the `window_hours` hourly epochs strictly BEFORE t of each sequence
  source, and emits from that one window BOTH representations: the flattened matrix columns
  (`<field>_t-<k>` for k = 1..W, plus the exact-lag fields `vtec_lag_<k>h` that are the same
  window's step k) and the sequence tensor (rows x W x sequence_features, oldest step first).
  A transformed matrix beside an untransformed tensor is not constructible because nothing
  else produces either.
* Exclusions are COUNTED, never silent (FR-P1-04-5, FR-P1-04-13): a window that would reach
  before `scored_start` (`excluded_before_scored_start`), and an incomplete window — a missing
  epoch or NaN inside it (`excluded_incomplete_windows`). No target-derived value is carried
  forward: the window is excluded instead.
* `assert_window_parity` is WS-13's check as Q4 = A designed it: TWO ORDERED assertions.
  Shape and ordering first (no tolerance needed, makes a value failure interpretable), then
  value-level reconstruction of the flattened columns from the tensor's slices within the
  fixture manifest's declared floating-point tolerance. With `tolerance=None` the value limb
  STOPS naming the TE 15.2 field — the tolerance is measured and frozen, never invented — so
  the check exists and is unrunnable until that value is frozen.
* `read_window_length` reads the window from `configs/experiment.yaml` (`window_length_hours`),
  requires it equal to the dictionary's `vtec_seq_*` step count (two frozen config values
  agreeing; no `24` lives here), and refuses when the field is placed in any grid (Vision 8.1:
  history length is not a tuned hyperparameter; TS-F-03).
* `ComparisonMask`: ONE comparison-wide intersection mask per comparison set, stored, with a
  content-derived `mask_id`, member row counts, and the three identity stamps required on every
  mask (NFR-TDEF-01). A mask that is not comparison-wide raises `FairnessError` (TC-16).

Inputs
------
Target records (station, hourly `interval_start_utc`, a source column), the frozen window
length from the snapshot, member row sets for a mask. No file is read except by
`load_mask`; no third-party package is imported at module scope (TS-F-03: no windowing
package is added).

Re-run behaviour
----------------
Pure functions; deterministic; the mask writer refuses to overwrite an existing mask
(a recomputed mask is a mask that can differ).
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Final

from src.data.config import (
    TBD_SENTINEL,
    ConfigSnapshot,
    FairnessError,
    IntegrityError,
    LeakageError,
)
from src.features._frames import tensor_as_nested, tensor_from_nested, tensor_shape

__all__ = [
    "HOURLY_STEP",
    "WINDOW_LENGTH_FIELD",
    "TOLERANCE_MANIFEST_FIELD",
    "WindowResult",
    "read_window_length",
    "assert_window_length_grid_free",
    "flattened_column_name",
    "build_windows",
    "assert_window_parity",
    "ComparisonMask",
    "build_comparison_mask",
    "assert_mask_is_comparison_wide",
    "write_mask",
    "load_mask",
]

#: D-17's hourly grid: `interval_start_utc` is an hour start, so consecutive epochs are one
#: hour apart. A property of the frozen target contract, not a tunable value.
HOURLY_STEP: Final[dt.timedelta] = dt.timedelta(hours=1)

#: Where the frozen window length lives (`configs/experiment.yaml`), and the TE 15.2 field the
#: value-level parity limb names when its tolerance is unset.
WINDOW_LENGTH_FIELD: Final[str] = "window_length_hours"
TOLERANCE_MANIFEST_FIELD: Final[str] = (
    "tests/fixtures/<fixture_id>/fixture_manifest.yaml: permitted_floating_point_tolerances"
)

_UTC: Final = dt.UTC
_GRID_TOKENS: Final[frozenset[str]] = frozenset({"window", "history", "seq", "sequence"})


def _is_tbd(value: object) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == TBD_SENTINEL)


# --- the frozen window length ------------------------------------------------------------


def assert_window_length_grid_free(experiment: Mapping[str, Any]) -> None:
    """The window length appears in NO grid: placing it in one fails (R-76; Vision 8.1)."""
    grids = experiment.get("grids")
    if _is_tbd(grids) or not isinstance(grids, Mapping):
        return

    def _walk(node: Any, trail: str) -> None:
        if isinstance(node, Mapping):
            for key, value in node.items():
                key_text = str(key)
                tokens = {t for t in key_text.lower().replace("-", "_").split("_") if t}
                if key_text == WINDOW_LENGTH_FIELD or tokens & _GRID_TOKENS:
                    raise LeakageError(
                        f"configs/experiment.yaml: grids{trail}.{key_text}",
                        "places the history window length inside a grid; the window is one "
                        "frozen value per feature-set ID shared across all model families "
                        "and appears in no grid (Vision 8.1 'History length is not a tuned "
                        "hyperparameter'; R-76; TS-F-03)",
                    )
                _walk(value, f"{trail}.{key_text}")
        elif isinstance(node, list | tuple):
            for index, value in enumerate(node):
                _walk(value, f"{trail}[{index}]")

    _walk(grids, "")


def read_window_length(snapshot: ConfigSnapshot, *, sequence_steps: int) -> int:
    """`experiment.window_length_hours`, frozen, grid-free, equal to the dictionary's steps.

    Raises
    ------
    LeakageError
        absent or `TBD — freeze gate`; not a positive integer; disagreeing with the
        dictionary's `vtec_seq_*` `sequence_steps` (two frozen config values must agree —
        that agreement is how "equals 24" is asserted without a 24 in source); or present in
        any grid.
    """
    value = snapshot.experiment.get(WINDOW_LENGTH_FIELD)
    if _is_tbd(value):
        raise LeakageError(
            f"configs/experiment.yaml: {WINDOW_LENGTH_FIELD}",
            "absent or unresolved (TBD — freeze gate); the primary history window is a "
            "frozen constant per feature-set ID (Vision 8.1; TE 6.4), transcribed under its "
            "D-number, never a literal in source (TC-03e)",
        )
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise LeakageError(
            f"configs/experiment.yaml: {WINDOW_LENGTH_FIELD}",
            f"{value!r} is not a positive integer number of hours",
        )
    if value != sequence_steps:
        raise LeakageError(
            f"configs/experiment.yaml: {WINDOW_LENGTH_FIELD}",
            f"{value} disagrees with the feature dictionary's sequence step count "
            f"{sequence_steps}; the flattened matrix and the sequence tensor must encode the "
            f"identical causal window (TE 6.4 matched-representation rule)",
        )
    assert_window_length_grid_free(snapshot.experiment)
    return value


# --- the one window definition -----------------------------------------------------------


def flattened_column_name(sequence_field: str, k: int) -> str:
    """The flattened matrix column for step k (k hours before t) of a sequence field."""
    return f"{sequence_field}_t-{k}"


@dataclass(frozen=True)
class WindowResult:
    """Both representations from one definition, with every exclusion counted."""

    records: tuple[dict[str, Any], ...]
    tensor: Any
    sequence_columns: Mapping[str, tuple[str, ...]]
    tensor_features: tuple[str, ...]
    excluded_before_scored_start: int
    excluded_incomplete_windows: int


def _as_utc(value: object, *, resource: str) -> dt.datetime:
    if isinstance(value, dt.datetime):
        stamp = value
    elif isinstance(value, str):
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            stamp = dt.datetime.fromisoformat(text)
        except ValueError as exc:
            raise IntegrityError(resource, f"timestamp {value!r} is not ISO-8601") from exc
    else:
        to_py = getattr(value, "to_pydatetime", None)
        if not callable(to_py):
            raise IntegrityError(resource, f"timestamp {value!r} is unrecognised")
        stamp = to_py()
    if stamp.tzinfo is None:
        return stamp.replace(tzinfo=_UTC)
    return stamp.astimezone(_UTC)


def _is_missing(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    try:
        return math.isnan(float(value))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return False


def build_windows(
    records: Sequence[Mapping[str, Any]],
    *,
    window_hours: int,
    sequence_fields: Mapping[str, str],
    lag_fields: Mapping[str, tuple[str, int]],
    scored_start: dt.datetime,
    scored_end: dt.datetime,
    timestamp_column: str = "interval_start_utc",
    station_column: str = "station_id",
) -> WindowResult:
    """The single window definition emitting both representations.

    `sequence_fields` maps a dictionary sequence field (e.g. `vtec_seq_24`) to its source
    column; `lag_fields` maps an exact-lag field (e.g. `vtec_lag_3h`) to `(source, k)`. A
    lag beyond the window is refused: it could not come from this definition.

    Returns matrix records (each carrying the row's station and timestamp plus the flattened
    columns and the lag fields), the tensor (rows x W x len(sequence_fields), oldest step
    first) and the two exclusion counts. Rows whose window is incomplete or would reach
    before `scored_start` are EXCLUDED AND COUNTED — never filled (FR-P1-04-13).
    """
    if window_hours <= 0:
        raise LeakageError(
            "window definition", f"window_hours must be positive, got {window_hours!r}"
        )
    for lag_field, (source, k) in lag_fields.items():
        if k <= 0 or k > window_hours:
            raise LeakageError(
                f"lag field {lag_field!r}",
                f"lag {k} h lies outside the {window_hours} h window; an exact lag is the "
                f"same window's step k and cannot exceed it (one definition, two "
                f"representations — R-81)",
            )
        if source not in sequence_fields.values():
            raise LeakageError(
                f"lag field {lag_field!r}",
                f"source {source!r} is not a windowed sequence source "
                f"{sorted(set(sequence_fields.values()))}; lags are read from the window, "
                f"never constructed separately",
            )
    seq_names = tuple(sequence_fields)
    sources = tuple(sequence_fields[name] for name in seq_names)

    # Index every (station, epoch) once; a duplicate epoch is an integrity failure.
    by_station: dict[str, dict[dt.datetime, Mapping[str, Any]]] = {}
    for index, record in enumerate(records):
        if station_column not in record or timestamp_column not in record:
            raise IntegrityError(
                f"target row {index}",
                f"lacks {station_column!r} or {timestamp_column!r}; windows are indexed by "
                f"station and record timestamp",
            )
        station = str(record[station_column])
        epoch = _as_utc(record[timestamp_column], resource=f"target row {index}")
        per_station = by_station.setdefault(station, {})
        if epoch in per_station:
            raise IntegrityError(
                f"target row {index}",
                f"duplicate epoch {epoch.isoformat()} for station {station}; one row per "
                f"station-hour (D-17)",
            )
        per_station[epoch] = record

    out_records: list[dict[str, Any]] = []
    nested: list[list[list[float]]] = []
    excluded_before = 0
    excluded_incomplete = 0
    for station in sorted(by_station):
        per_station = by_station[station]
        for epoch in sorted(per_station):
            if not (scored_start <= epoch < scored_end):
                continue
            if epoch - window_hours * HOURLY_STEP < scored_start:
                excluded_before += 1
                continue
            steps: list[list[float]] = []
            complete = True
            for k in range(window_hours, 0, -1):  # oldest first
                past = per_station.get(epoch - k * HOURLY_STEP)
                if past is None:
                    complete = False
                    break
                values: list[float] = []
                for source in sources:
                    raw = past.get(source)
                    if _is_missing(raw):
                        complete = False
                        break
                    values.append(float(raw))
                if not complete:
                    break
                steps.append(values)
            if not complete:
                excluded_incomplete += 1
                continue
            row: dict[str, Any] = dict(per_station[epoch])
            for name_index, name in enumerate(seq_names):
                for k in range(1, window_hours + 1):
                    # steps[0] is k = window_hours (oldest); steps[-1] is k = 1.
                    row[flattened_column_name(name, k)] = steps[window_hours - k][name_index]
            for lag_field, (source, k) in lag_fields.items():
                source_index = sources.index(source)
                row[lag_field] = steps[window_hours - k][source_index]
            out_records.append(row)
            nested.append(steps)
    sequence_columns = {
        name: tuple(flattened_column_name(name, k) for k in range(window_hours, 0, -1))
        for name in seq_names
    }
    tensor = tensor_from_nested(nested, shape=(len(nested), window_hours, len(seq_names)))
    return WindowResult(
        records=tuple(out_records),
        tensor=tensor,
        sequence_columns=sequence_columns,
        tensor_features=seq_names,
        excluded_before_scored_start=excluded_before,
        excluded_incomplete_windows=excluded_incomplete,
    )


# --- WS-13: two ordered assertions ------------------------------------------------------


def assert_window_parity(
    matrix_records: Sequence[Mapping[str, Any]],
    tensor: Any,
    *,
    sequence_columns: Mapping[str, Sequence[str]],
    tensor_features: Sequence[str],
    tolerance: float | None,
) -> None:
    """WS-13 parity, in Q4 = A's two ordered assertions.

    1. Shape and ordering: the tensor is rank 3 with `len(matrix_records)` rows,
       `len(columns)` steps and `len(tensor_features)` features, and every sequence field
       has the same step count, in the same order.
    2. Value level: each flattened matrix column is reconstructed from the tensor's slice
       and compared element-wise within `tolerance`.

    Raises
    ------
    LeakageError
        on either assertion failing.
    IntegrityError
        when `tolerance is None`: the value-level limb STOPS naming the TE 15.2 field. The
        tolerance is measured from the fixtures and frozen, never invented (TE 15.1), so
        the check is designed and unrunnable until that value exists.
    """
    rows, steps, width = tensor_shape(tensor)
    if rows != len(matrix_records):
        raise LeakageError(
            "window parity (shape)",
            f"tensor carries {rows} rows but the matrix carries {len(matrix_records)}; the two "
            f"representations were not built from one window definition (WS-13, FR-P1-04-8)",
        )
    if tuple(tensor_features) != tuple(sequence_columns):
        raise LeakageError(
            "window parity (ordering)",
            f"tensor feature order {list(tensor_features)} differs from the matrix's sequence "
            f"fields {list(sequence_columns)} (WS-13 ordering precondition)",
        )
    if width != len(tensor_features):
        raise LeakageError(
            "window parity (shape)",
            f"tensor width {width} differs from {len(tensor_features)} sequence features",
        )
    step_counts = {name: len(cols) for name, cols in sequence_columns.items()}
    distinct = set(step_counts.values())
    if len(distinct) > 1 or (distinct and steps != next(iter(distinct))):
        raise LeakageError(
            "window parity (shape)",
            f"tensor step count {steps} disagrees with the matrix's flattened column counts "
            f"{step_counts}; one window length per feature-set ID (TE 6.4)",
        )
    if tolerance is None:
        raise IntegrityError(
            TOLERANCE_MANIFEST_FIELD,
            "the value-level parity limb needs the fixture manifest's declared floating-point "
            "tolerance and it is unset; TE 15.1 fixes that tolerances are measured from the "
            "fixtures and frozen, never invented, so this check stops here rather than "
            "choosing one (SD-F-06, Q4 = A; WS-13 stays Pending)",
        )
    if tolerance < 0:
        raise IntegrityError(TOLERANCE_MANIFEST_FIELD, f"tolerance {tolerance!r} is negative")
    nested = tensor_as_nested(tensor)
    for row_index, record in enumerate(matrix_records):
        for feature_index, name in enumerate(tensor_features):
            for step_index, column in enumerate(sequence_columns[name]):
                expected = float(nested[row_index][step_index][feature_index])
                actual = float(record[column])
                if abs(expected - actual) > tolerance:
                    raise LeakageError(
                        f"window parity (value) row {row_index} column {column!r}",
                        f"matrix value {actual!r} differs from the tensor slice {expected!r} "
                        f"by more than the declared tolerance {tolerance!r}; the flattened "
                        f"matrix and the sequence tensor must contain the same underlying "
                        f"window values (FR-P1-04-8, WS-13)",
                    )


# --- NFR-FAIR-01: one comparison-wide mask -----------------------------------------------

_IDENTITY_KEYS: Final[tuple[str, ...]] = ("phase_id", "source_id", "target_definition_id")


@dataclass(frozen=True)
class ComparisonMask:
    """One stored intersection mask per comparison set, stamped with the three identity IDs."""

    mask_id: str
    comparison_set_id: str
    members: tuple[str, ...]
    rows: tuple[tuple[str, str], ...]
    member_row_counts: Mapping[str, int]
    kept_count: int
    phase_id: str
    source_id: str
    target_definition_id: str


def _mask_id(
    comparison_set_id: str, members: Sequence[str], rows: Sequence[tuple[str, str]]
) -> str:
    payload = json.dumps(
        {"comparison_set_id": comparison_set_id, "members": list(members), "rows": list(rows)},
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def build_comparison_mask(
    member_rows: Mapping[str, Iterable[tuple[str, object]]],
    *,
    comparison_set_id: str,
    identity: Mapping[str, str],
) -> ComparisonMask:
    """The intersection over EVERY member of the comparison set, computed once.

    Raises
    ------
    FairnessError
        fewer than two members (a comparison set is a set of models compared together, and
        a one-member mask is a model-specific mask), or a missing identity stamp.
    """
    members = tuple(sorted(member_rows))
    if len(members) < 2:
        raise FairnessError(
            f"comparison set {comparison_set_id!r}",
            f"has {len(members)} member(s); a comparison-wide mask is the intersection over "
            f"every model in the comparison, never a model-specific or pairwise mask "
            f"(NFR-FAIR-01, TC-16)",
        )
    for key in _IDENTITY_KEYS:
        if not str(identity.get(key, "") or "").strip():
            raise FairnessError(
                f"comparison set {comparison_set_id!r}",
                f"identity stamp {key!r} is missing; every mask carries phase_id, source_id "
                f"and target_definition_id (NFR-TDEF-01)",
            )
    sets: dict[str, set[tuple[str, str]]] = {}
    for member in members:
        normalised: set[tuple[str, str]] = set()
        for station, stamp in member_rows[member]:
            normalised.add((str(station), _as_utc(stamp, resource=f"{member} row").isoformat()))
        sets[member] = normalised
    kept = set.intersection(*sets.values()) if sets else set()
    rows = tuple(sorted(kept))
    return ComparisonMask(
        mask_id=_mask_id(comparison_set_id, members, rows),
        comparison_set_id=comparison_set_id,
        members=members,
        rows=rows,
        member_row_counts={member: len(sets[member]) for member in members},
        kept_count=len(rows),
        phase_id=str(identity["phase_id"]),
        source_id=str(identity["source_id"]),
        target_definition_id=str(identity["target_definition_id"]),
    )


def assert_mask_is_comparison_wide(mask: ComparisonMask, *, members: Iterable[str]) -> None:
    """The mask used for a comparison must be the one computed over EXACTLY its members."""
    expected = tuple(sorted(members))
    if mask.members != expected:
        raise FairnessError(
            f"mask {mask.mask_id}",
            f"was computed over {list(mask.members)} but the comparison has members "
            f"{list(expected)}; a pairwise or model-specific mask is refused (NFR-FAIR-01)",
        )


def write_mask(mask: ComparisonMask, path: Path) -> Path:
    """Store the mask ONCE; an existing file is never overwritten (a recomputed mask differs)."""
    path = Path(path)
    if path.exists():
        raise FairnessError(
            path,
            "a mask already exists at this path; the comparison-wide mask is computed once per "
            "comparison set and stored, never recomputed or overwritten (TS-F-04)",
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = asdict(mask)
    payload["rows"] = [list(row) for row in mask.rows]
    payload["members"] = list(mask.members)
    payload["member_row_counts"] = dict(mask.member_row_counts)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def load_mask(path: Path) -> ComparisonMask:
    """Load a stored mask and REFUSE one whose content no longer matches its `mask_id`."""
    path = Path(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FairnessError(
            path, f"mask is unreadable ({exc}); an unreadable mask is refused"
        ) from exc
    try:
        rows = tuple((str(s), str(t)) for s, t in payload["rows"])
        mask = ComparisonMask(
            mask_id=str(payload["mask_id"]),
            comparison_set_id=str(payload["comparison_set_id"]),
            members=tuple(str(m) for m in payload["members"]),
            rows=rows,
            member_row_counts={str(k): int(v) for k, v in payload["member_row_counts"].items()},
            kept_count=int(payload["kept_count"]),
            phase_id=str(payload["phase_id"]),
            source_id=str(payload["source_id"]),
            target_definition_id=str(payload["target_definition_id"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise FairnessError(path, f"mask payload is malformed ({exc})") from exc
    recomputed = _mask_id(mask.comparison_set_id, mask.members, mask.rows)
    if recomputed != mask.mask_id or mask.kept_count != len(mask.rows):
        raise FairnessError(
            path,
            f"stored mask_id {mask.mask_id} does not match its content ({recomputed}); a mask "
            f"whose rows changed after it was stored is not the mask that was frozen",
        )
    return mask
