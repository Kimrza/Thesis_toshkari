"""Intra-package frame helpers: one record/column vocabulary over DataFrames and records.

Purpose
-------
`src/features` produces a `pandas.DataFrame` matrix and a `numpy` tensor (ADR-11's
`FeatureBundle`; TS-F-03). Every guard in this package, however, is a rule over VALUES and
TIMESTAMPS, not over a library type — and the governed environment pins `pandas`/`numpy` while
a review or fixture machine may lack them. These helpers let each guard read a frame as
records and write one back, choosing the governed types when the libraries are importable
and a plain-record fallback (`src.data.splits.RecordFrame`, nested lists) otherwise. In the
governed environment the fallback is never taken; it exists so the leakage checks are
testable on a stdlib-only interpreter, which is smoke evidence only, never governed evidence.

Inputs
------
In-memory frames only. No file is read, no third-party package is imported at module scope
(the `pandas`/`numpy` imports are deferred to the functions that need them).

Re-run behaviour
----------------
Pure functions; deterministic; nothing persisted.
"""

from __future__ import annotations

import importlib.util
from collections.abc import Mapping, Sequence
from typing import Any

from src.data.config import IntegrityError
from src.data.splits import RecordFrame

__all__ = [
    "pandas_available",
    "numpy_available",
    "records_of",
    "columns_of",
    "column_values",
    "frame_from_records",
    "tensor_from_nested",
    "tensor_as_nested",
    "tensor_shape",
    "frame_attrs",
    "ensure_records",
]


def pandas_available() -> bool:
    return importlib.util.find_spec("pandas") is not None


def numpy_available() -> bool:
    return importlib.util.find_spec("numpy") is not None


def _is_dataframe(frame: Any) -> bool:
    return hasattr(frame, "columns") and hasattr(frame, "iloc")


def records_of(frame: Any) -> list[dict[str, Any]]:
    """A frame as a list of plain record dicts (DataFrame rows or record mappings)."""
    if _is_dataframe(frame):
        return [dict(row) for row in frame.to_dict(orient="records")]
    out: list[dict[str, Any]] = []
    for index, row in enumerate(frame):
        if not isinstance(row, Mapping):
            raise IntegrityError(f"row {index}", "is not a record mapping")
        out.append(dict(row))
    return out


def columns_of(frame: Any) -> tuple[str, ...]:
    """Column names, in order (union over records for the record form)."""
    if _is_dataframe(frame):
        return tuple(str(c) for c in frame.columns)
    seen: dict[str, None] = {}
    for row in frame:
        for key in row:
            seen.setdefault(str(key), None)
    return tuple(seen)


def column_values(frame: Any, column: str) -> list[Any]:
    if _is_dataframe(frame):
        if column not in list(frame.columns):
            raise IntegrityError(f"frame column {column!r}", "absent from the frame")
        return list(frame[column])
    values: list[Any] = []
    for index, row in enumerate(frame):
        if column not in row:
            raise IntegrityError(f"row {index}", f"carries no column {column!r}")
        values.append(row[column])
    return values


def frame_from_records(
    records: Sequence[Mapping[str, Any]], *, columns: Sequence[str], attrs: Mapping | None = None
) -> Any:
    """A DataFrame when pandas is importable, else a `RecordFrame`; column order fixed."""
    ordered = [{name: row.get(name) for name in columns} for row in records]
    if pandas_available():
        import pandas as pd

        frame = pd.DataFrame(ordered, columns=list(columns))
        if attrs:
            frame.attrs.update(dict(attrs))
        return frame
    fallback = RecordFrame(ordered)
    if attrs:
        fallback.attrs.update(dict(attrs))
    return fallback


def tensor_from_nested(
    nested: Sequence[Sequence[Sequence[float]]], *, shape: tuple[int, int, int]
) -> Any:
    """An `NDArray` when numpy is importable, else the nested lists (shape checked)."""
    if len(nested) != shape[0] or any(
        len(steps) != shape[1] or any(len(step) != shape[2] for step in steps) for steps in nested
    ):
        raise IntegrityError(
            "tensor", f"nested window values do not have the declared shape {shape}"
        )
    if numpy_available():
        import numpy as np

        if shape[0] == 0:
            return np.zeros(shape, dtype=float)
        return np.asarray(nested, dtype=float)
    return [[list(step) for step in steps] for steps in nested]


def tensor_as_nested(tensor: Any) -> list[list[list[float]]]:
    to_list = getattr(tensor, "tolist", None)
    if callable(to_list):
        return to_list()
    return [[list(step) for step in steps] for steps in tensor]


def tensor_shape(tensor: Any) -> tuple[int, int, int]:
    shape = getattr(tensor, "shape", None)
    if shape is not None:
        dims = tuple(int(d) for d in shape)
        if len(dims) != 3:
            raise IntegrityError("tensor", f"expected a rank-3 tensor, got shape {dims}")
        return dims  # type: ignore[return-value]
    rows = len(tensor)
    steps = len(tensor[0]) if rows else 0
    width = len(tensor[0][0]) if rows and steps else 0
    return rows, steps, width


def frame_attrs(frame: Any) -> dict[str, Any]:
    attrs = getattr(frame, "attrs", None)
    return dict(attrs) if isinstance(attrs, dict) else {}


def ensure_records(frame: Any, *, resource: str) -> list[dict[str, Any]]:
    """`records_of` with an empty-frame refusal (a check that never ran must not pass)."""
    records = records_of(frame)
    if not records:
        raise IntegrityError(resource, "is empty; a check over zero rows is not a check")
    return records

