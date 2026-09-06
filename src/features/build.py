"""F-2 Feature bundle: nothing enters the ML input space by name alone (W-2; R-74, R-76,
R-76a, R-77, R-78, R-79 data-flow limb; SD-F-01, SD-F-02).

Purpose
-------
`build_features` is the ONLY producer of either representation and the ONLY place a fitted
transform is applied. It refuses, in this order, before it assembles anything:

1. **Spec validation against the partition list** (ADR-11): `spec.partition_id` must name a
   partition (`PartitionError` otherwise); the scored range must be CONTAINED in the training
   range for `role="train"` and in the `validation_month` for `role="score"` (`LeakageError`).
2. **The identity check** (R-74 element 4): `transform.partition_id == spec.partition_id`, with
   exactly ONE enumerated exception — `REFIT` -> `DEC` under `role="score"`, the G-06 apply;
   the same pair under `role="train"` raises; every other mismatched ordered pair raises
   (30 raising conditions, enumerated by the tests).
3. **The closed dictionary** (R-76, FR-P1-04-12): every dictionary field maps to a TE 6.2 row
   from a closed list of row identities; `iri_*` raises; the removed `ssn` row raises; a raw
   longitude column raises (longitude enters only through `lst_sin`/`lst_cos`, FR-P1-04-10);
   Dst is diagnostic-only; every field is exactly one `FieldClass` (R-77); support fields are
   EXCLUDED unless an approval ID with a timestamp PRECEDING the feature-set freeze is
   recorded, a read at hour t fails, and a target-hour quality field fails permanently (R-78,
   three separate assertions plus the permanent one).
4. **The permitted-producer list** (SD-F-01, Q1 = A, Q3 = A): `load_permitted_producers`
   reads `configs/features.yaml`'s `permitted_producers` block through a SEPARATE loader (the
   frozen `ConfigSnapshot` is untouched). While it is unset or incomplete, `LeakageError`
   names WHICH rows lack an entry and NO FEATURE MATRIX IS PRODUCED — the fail-closed
   refusal is this unit's deliverable today. Each input's `producing_artifact` must be
   permitted for the (row, producer) pair it supplies.
5. **The station registry** gates `station_lat`, `station_onehot_*` and `lst_*`
   (`assert_registry_resolved`; an unresolved registry blocks them).

Then it assembles the frame (target-derived window through the ONE definition in
`windows.py`; driver series through the R-77 field-class carry-forward boundary and, where
observations are supplied, R-76a's alignment raise; time and station fields from the record
timestamp and the verified registry), refuses an empty frame, applies the transform, builds
both representations, asserts WS-13 parity (shape first, value within the declared tolerance
or stop), and stamps per-column provenance into the bundle so the key set EQUALS the column
set — a stamp cannot go missing without the bundle failing to load (SD-F-02).

Inputs
------
The D-17 target frame (`interval_start_utc`, `station_id`, `vtec_tecu`, the three identity
stamps, plus support columns), driver series keyed by `source_series` (hourly
`interval_start_utc`/`value` rows; optional `observations` in attrs for the alignment check),
the station registry, the availability matrix, a `FrameSpec`, the partition list, the
`ConfigSnapshot` (`features.feature_dictionary`, `features.permitted_producers`,
`features.carry_forward_bound_hours`, `features.feature_set_freeze_utc`,
`experiment.window_length_hours`), and an optional `Transform`.

Re-run behaviour
----------------
Pure function of its inputs; deterministic. `write_bundle` refuses to overwrite an existing
bundle directory; `load_bundle` reads all three files or raises.

Boundaries
----------
Never imports `src.external.iri` / `src.external.gim` (TE 12) nor anything under `src/models`
or `src/evaluation`. No scientific constant in source: lags, steps, bounds, freeze
timestamps and the producer list are all configuration. No inverse path (Q4 = A, D-27).
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final, Literal

from src.data.config import (
    TBD_SENTINEL,
    ConfigSnapshot,
    IntegrityError,
    LeakageError,
    PartitionError,
    PreflightError,
)
from src.data.registry import Station, assert_registry_resolved
from src.data.splits import (
    LOCKED_ID,
    REFIT_ID,
    Partition,
    assert_membership_from_timestamps,
    partition_by_id,
    training_range,
    validation_month_range,
)
from src.external.spaceweather import align_interval_series, assert_alignment
from src.features._frames import (
    columns_of,
    frame_attrs,
    frame_from_records,
    pandas_available,
    records_of,
    tensor_as_nested,
    tensor_from_nested,
)
from src.features.availability import AvailabilityRow, assert_dst_diagnostic_only
from src.features.transforms import (
    FieldClass,
    Transform,
    apply_fitted_transform,
    assert_field_classes_partition,
    carry_forward,
)
from src.features.windows import (
    assert_window_parity,
    build_windows,
    read_window_length,
)

__all__ = [
    "SECTION_6_2_ROWS",
    "REMOVED_ROWS",
    "IDENTITY_KEYS",
    "UNTRANSFORMED_SEGMENT",
    "FrameSpec",
    "FeatureBundle",
    "load_feature_dictionary",
    "load_permitted_producers",
    "assert_producers_cover",
    "validate_spec",
    "assert_transform_identity",
    "build_features",
    "bundle_directory_name",
    "write_bundle",
    "load_bundle",
]

#: TE 6.2's dictionary ROW identities and the class each row belongs to. Identities of frozen
#: text, never values (the REQUIRED_FIELDS_MAP precedent): the table is closed, and a field
#: whose declared row is not here is outside the ML input space (FR-P1-04-12).
SECTION_6_2_ROWS: Final[Mapping[str, FieldClass]] = {
    "vtec_lag": FieldClass.target,
    "vtec_seq_24": FieldClass.target,
    "utc_hour_sin": FieldClass.time,
    "utc_hour_cos": FieldClass.time,
    "doy_sin": FieldClass.time,
    "doy_cos": FieldClass.time,
    "lst_sin": FieldClass.station,
    "lst_cos": FieldClass.station,
    "station_onehot": FieldClass.station,
    "station_lat": FieldClass.station,
    "kp_safe": FieldClass.driver,
    "ap_safe": FieldClass.driver,
    "hp60_safe": FieldClass.driver,
    "ap60_safe": FieldClass.driver,
    "f107_safe": FieldClass.driver,
    "f107_81_trailing": FieldClass.driver,
    "dst": FieldClass.diagnostic,
    "target_support": FieldClass.support,
}
#: Rows TE 6.2 lists as REMOVED — declaring a field on one is a raise, not an omission.
REMOVED_ROWS: Final[frozenset[str]] = frozenset({"ssn"})
#: The three project-wide identity stamps required on every dataset and mask (NFR-TDEF-01).
IDENTITY_KEYS: Final[tuple[str, ...]] = ("phase_id", "source_id", "target_definition_id")
#: M9's literal directory segment for `transform_id is None`.
UNTRANSFORMED_SEGMENT: Final[str] = "untransformed"
#: Producer identity of every station-derived column (the verified registry).
STATION_REGISTRY_PRODUCER: Final[str] = "station_registry"
#: Producer identity of time-derived columns (a pure function of the record timestamp).
TIMESTAMP_PRODUCER: Final[str] = "record_timestamp"
#: Field-name tokens that would carry RAW longitude into the input space (FR-P1-04-10).
_RAW_LONGITUDE_TOKENS: Final[frozenset[str]] = frozenset({"lon", "longitude", "glon", "lng"})
_TARGET_HOUR_QUALITY: Final[str] = "target_hour_quality"
_STANDARDIZE: Final[str] = "train_only_standardize"
_NO_NORMALIZATION: Final[str] = "none"
_UTC: Final = dt.UTC
_MODEL_INPUT_CLASSES: Final[frozenset[FieldClass]] = frozenset(
    {FieldClass.driver, FieldClass.target, FieldClass.station, FieldClass.time}
)


# --- the boundary shapes (ADR-11) --------------------------------------------------------


@dataclass(frozen=True)
class FrameSpec:
    """ADR-11's `FrameSpec`. `scored_end` is EXCLUSIVE: the scored range is
    `[scored_start, scored_end)`, so range equality against a partition's training range
    is `scored_start == train_start 00:00` and `scored_end == (train_end + 1 day) 00:00`
    with no cadence constant involved."""

    partition_id: str
    role: Literal["train", "score"]
    scored_start: dt.datetime
    scored_end: dt.datetime

    def __post_init__(self) -> None:
        if self.role not in ("train", "score"):
            raise PartitionError(
                f"FrameSpec {self.partition_id}", f"role {self.role!r} is not 'train' | 'score'"
            )
        for name in ("scored_start", "scored_end"):
            value = getattr(self, name)
            if not isinstance(value, dt.datetime) or value.tzinfo is None:
                raise PartitionError(
                    f"FrameSpec {self.partition_id}",
                    f"{name} must be a timezone-aware datetime; a naive scored bound cannot be "
                    f"compared against the partition's UTC range",
                )
        if self.scored_start >= self.scored_end:
            raise PartitionError(
                f"FrameSpec {self.partition_id}",
                f"scored_start {self.scored_start.isoformat()} is not before scored_end "
                f"{self.scored_end.isoformat()} (end exclusive)",
            )


@dataclass(frozen=True)
class FeatureBundle:
    """ADR-11's `FeatureBundle` (matrix, tensor, spec, transform_id) plus ADDITIVE recorded
    fields, all defaulted so the approved four-field construction still holds:
    `provenance` (SD-F-02: column -> {dictionary_row, dictionary_field, producing_artifact};
    key set EQUALS the matrix column set), `identity` (the three stamps), `excluded_counts`
    (every exclusion counted), `standardized_columns` (what `fit_transforms` standardises)
    and the window's `sequence_columns`/`tensor_features` (what parity is asserted over)."""

    matrix: Any
    tensor: Any
    spec: FrameSpec
    transform_id: str | None
    provenance: Mapping[str, Mapping[str, str]] = field(default_factory=dict)
    identity: Mapping[str, str] = field(default_factory=dict)
    excluded_counts: Mapping[str, int] = field(default_factory=dict)
    standardized_columns: tuple[str, ...] = ()
    sequence_columns: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    tensor_features: tuple[str, ...] = ()


# --- config reads ------------------------------------------------------------------------


def _is_tbd(value: object) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == TBD_SENTINEL)


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


def load_feature_dictionary(snapshot: ConfigSnapshot) -> Mapping[str, Mapping[str, Any]]:
    """`features.feature_dictionary`: field -> {dictionary_row, normalization, ...}.

    Raises
    ------
    PreflightError
        absent or `TBD — freeze gate` (TE 18.3: the dictionary's transcription is its
        owner's freeze; nothing is built over an unresolved one).
    LeakageError
        malformed entries; a declared row outside `SECTION_6_2_ROWS`; a REMOVED row; an
        `iri_*` field; a missing or unknown `normalization`.
    """
    block = snapshot.features.get("feature_dictionary")
    if _is_tbd(block):
        raise PreflightError(
            "configs/features.yaml: feature_dictionary",
            "absent or unresolved (TBD — freeze gate); the closed TE 6.2 dictionary is "
            "transcribed under its D-number by its owner, and no feature is constructed over "
            "an unresolved dictionary (TE 18.3; FR-P1-04-12)",
        )
    if not isinstance(block, Mapping) or not block:
        raise LeakageError(
            "configs/features.yaml: feature_dictionary", "must be a non-empty mapping of fields"
        )
    out: dict[str, Mapping[str, Any]] = {}
    for raw_name, entry in block.items():
        name = str(raw_name)
        resource = f"feature dictionary field {name!r}"
        if not isinstance(entry, Mapping):
            raise LeakageError(resource, "entry must be a mapping")
        row = entry.get("dictionary_row")
        if _is_tbd(row):
            raise LeakageError(
                resource, "declares no dictionary_row; the input space is closed by row"
            )
        row_text = str(row)
        if row_text in REMOVED_ROWS:
            raise LeakageError(
                resource,
                f"declares the REMOVED row {row_text!r} (TE 6.2: 'Removed. Not used anywhere.'); "
                f"SSN never enters the feature path",
            )
        if row_text not in SECTION_6_2_ROWS:
            raise LeakageError(
                resource,
                f"declares row {row_text!r}, which is outside the TE 6.2 dictionary "
                f"{sorted(SECTION_6_2_ROWS)}; no field outside that table enters training or "
                f"inference (FR-P1-04-12, R-76)",
            )
        _assert_field_name_clean(name)
        _assert_name_matches_row(name, row_text, entry)
        normalization = entry.get("normalization")
        if _is_tbd(normalization) or str(normalization) not in (_STANDARDIZE, _NO_NORMALIZATION):
            raise LeakageError(
                resource,
                f"normalization {normalization!r} is not one of "
                f"{[_STANDARDIZE, _NO_NORMALIZATION]}; whether a field is standardised is a "
                f"dictionary declaration (TE 6.2 'Normalization' column), never a default",
            )
        out[name] = entry
    return out


def _tokens(name: str) -> set[str]:
    return {t for t in name.lower().replace("-", "_").split("_") if t}


def _assert_field_name_clean(name: str) -> None:
    lowered = name.lower()
    if lowered.startswith("iri_") or "iri" in _tokens(name):
        raise LeakageError(
            f"feature dictionary field {name!r}",
            "is an iri_* / IRI-derived field; no IRI value, residual or IRI-computed field "
            "reaches ML training or inference (NFR-IRI-01; Vision 7.1; WS-10)",
        )
    if _tokens(name) & _RAW_LONGITUDE_TOKENS:
        raise LeakageError(
            f"feature dictionary field {name!r}",
            "carries raw longitude; longitude enters only through lst_sin and lst_cos "
            "(FR-P1-04-10; TE 7.2; project.md Forbidden)",
        )
    if "ssn" in _tokens(name):
        raise LeakageError(
            f"feature dictionary field {name!r}",
            "is an SSN field; sunspot number is removed and used nowhere (TE 6.2)",
        )


def _assert_name_matches_row(name: str, row: str, entry: Mapping[str, Any]) -> None:
    resource = f"feature dictionary field {name!r}"
    if row == "vtec_lag":
        lag = entry.get("lag_hours")
        if _is_tbd(lag) or isinstance(lag, bool) or not isinstance(lag, int) or lag <= 0:
            raise LeakageError(resource, "vtec_lag row needs a positive integer lag_hours")
        if name != f"vtec_lag_{lag}h":
            raise LeakageError(
                resource,
                f"name disagrees with its declared lag {lag} h (expected 'vtec_lag_{lag}h'); "
                f"exact lags are strictly causal at the named hour (FR-P1-04-13)",
            )
    elif row == "vtec_seq_24":
        steps = entry.get("sequence_steps")
        if _is_tbd(steps) or isinstance(steps, bool) or not isinstance(steps, int) or steps <= 0:
            raise LeakageError(resource, "vtec_seq row needs a positive integer sequence_steps")
        if name != row:
            raise LeakageError(resource, f"the sequence field is named {row!r}, not {name!r}")
    elif row == "station_onehot":
        if not name.startswith("station_onehot_") or _is_tbd(entry.get("station_id")):
            raise LeakageError(
                resource, "station_onehot fields are 'station_onehot_<ID>' with a station_id"
            )
    elif row == "dst":
        if not name.startswith("dst"):
            raise LeakageError(resource, "a dst row field is named 'dst' or 'dst_*'")
    elif row == "target_support":
        if _is_tbd(entry.get("source_column")):
            raise LeakageError(resource, "a support field names its source_column")
    elif name != row:
        raise LeakageError(
            resource,
            f"name {name!r} disagrees with its declared row {row!r}; single-field rows are "
            f"named exactly as TE 6.2 names them",
        )
    if SECTION_6_2_ROWS[row] is FieldClass.driver and _is_tbd(entry.get("source_series")):
        raise LeakageError(resource, "a driver field names its source_series")


def load_permitted_producers(
    source: Path | ConfigSnapshot, *, dictionary_rows: Sequence[str] | None = None
) -> Mapping[str, tuple[str, ...]]:
    """The SEPARATE permitted-producer loader (Q3 = A): `configs/features.yaml`'s
    `permitted_producers` block, keyed per dictionary row -> permitted producing artifacts.

    `source` is the configs directory (the ruled signature) or an already-loaded
    `ConfigSnapshot` (the same file, already parsed and hashed by `load_configs`). Nothing is
    added to the frozen `ConfigSnapshot` shape.

    Raises
    ------
    LeakageError
        when the block is absent, `TBD — freeze gate`, malformed, or lacks an entry for any
        row in `dictionary_rows` — naming WHICH rows lack an entry. While it raises, no
        feature matrix is produced (SD-F-01, Q1 = A): a matrix with one unverifiable column
        produces a metric that looks exactly like a measurement.
    """
    if isinstance(source, ConfigSnapshot):
        block = source.features.get("permitted_producers")
        resource = "configs/features.yaml: permitted_producers"
    else:
        path = Path(source) / "features.yaml"
        resource = f"{path}: permitted_producers"
        if not path.is_file():
            raise LeakageError(resource, "configs/features.yaml is missing")
        try:
            import yaml
        except ImportError as exc:  # pragma: no cover - environment defect
            raise LeakageError(resource, f"pyyaml is required to read the block ({exc})") from exc
        try:
            loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            raise LeakageError(resource, f"features.yaml is unparseable ({exc})") from exc
        block = loaded.get("permitted_producers") if isinstance(loaded, Mapping) else None
    rows_wanted = list(dictionary_rows) if dictionary_rows is not None else []
    if _is_tbd(block):
        raise LeakageError(
            resource,
            "unset (absent or TBD — freeze gate): a permitted-producer entry for every TE 6.2 "
            "dictionary row in the requested feature set is required before ANY feature "
            "matrix is produced, and none exists for any row"
            + (f" (rows lacking entries: {sorted(set(rows_wanted))})" if rows_wanted else "")
            + ". The list is assigned to nobody and is not this unit's to author "
            "(SD-F-01, Q1 = A; TS-F-01: whether it is governed config is a TC-03e question). "
            "No feature matrix is produced.",
        )
    if not isinstance(block, Mapping):
        raise LeakageError(resource, "must be a mapping of dictionary_row -> [producers]")
    producers: dict[str, tuple[str, ...]] = {}
    for row, entry in block.items():
        row_text = str(row)
        if row_text not in SECTION_6_2_ROWS:
            raise LeakageError(
                f"{resource}.{row_text}",
                f"names a row outside the TE 6.2 dictionary {sorted(SECTION_6_2_ROWS)}",
            )
        if isinstance(entry, str):
            values: list[str] = [entry]
        elif isinstance(entry, list | tuple):
            values = [str(v) for v in entry]
        else:
            raise LeakageError(f"{resource}.{row_text}", "entry must be a producer id or a list")
        cleaned = tuple(v.strip() for v in values if str(v).strip() and not _is_tbd(v))
        if not cleaned:
            raise LeakageError(f"{resource}.{row_text}", "entry is empty or TBD")
        producers[row_text] = cleaned
    if rows_wanted:
        assert_producers_cover(producers, rows_wanted, resource=resource)
    return producers


def assert_producers_cover(
    producers: Mapping[str, Sequence[str]],
    rows: Sequence[str],
    *,
    resource: str = "configs/features.yaml: permitted_producers",
) -> None:
    missing = sorted({row for row in rows if row not in producers})
    if missing:
        raise LeakageError(
            resource,
            f"incomplete: no permitted-producer entry for dictionary row(s) {missing}; a "
            f"permitted-producer entry for every TE 6.2 row in the requested feature set is "
            f"required, and no feature matrix is produced while any is missing (SD-F-01)",
        )


# --- spec validation and the identity check ---------------------------------------------


def validate_spec(spec: FrameSpec, partitions: Sequence[Partition]) -> Partition:
    """ADR-11: the spec names a partition and its scored range is contained in what its role
    permits — the training range for `train`, the validation month for `score`.

    Raises
    ------
    PartitionError
        `spec.partition_id` names no partition (R-92's shape), or a `score` spec for the
        final refit, which has no validation month.
    LeakageError
        the scored range is not contained in the role's permitted range — including the
        Critical-1 case `FrameSpec("F1", "train", Jan 1, Dec 1)`.
    """
    partition = partition_by_id(partitions, spec.partition_id)
    if spec.role == "train":
        start, end = training_range(partition)
        permitted = "training range"
    else:
        if partition.validation_month is None:
            raise PartitionError(
                f"FrameSpec {spec.partition_id}/score",
                "the final refit has no validation month and is scored nowhere "
                "(FR-P1-04-14); no score-role spec exists for it",
            )
        start, end = validation_month_range(partition)
        permitted = "validation month"
    if not (start <= spec.scored_start and spec.scored_end <= end):
        raise LeakageError(
            f"FrameSpec {spec.partition_id}/{spec.role}",
            f"scored range [{spec.scored_start.isoformat()}, {spec.scored_end.isoformat()}) "
            f"is not contained in partition {partition.partition_id}'s {permitted} "
            f"[{start.isoformat()}, {end.isoformat()}); a spec's fields are caller assertions "
            f"until validated against the partition list (ADR-11)",
        )
    return partition


def assert_transform_identity(transform: Transform | None, spec: FrameSpec) -> None:
    """R-74 element 4: identity, not containment, with exactly one enumerated exception.

    Raises
    ------
    LeakageError
        `transform.partition_id != spec.partition_id` for every ordered pair except
        (`REFIT`, `DEC`) under `role == "score"`; that pair under `role == "train"` raises,
        because training on the locked month is the locked-test violation itself.
    """
    if transform is None:
        return
    if transform.partition_id == spec.partition_id:
        return
    if (
        transform.partition_id == REFIT_ID
        and spec.partition_id == LOCKED_ID
        and spec.role == "score"
    ):
        return  # the G-06 apply: fitted Jan–Nov, December never fitted on
    raise LeakageError(
        f"transform {transform.transform_id} on spec {spec.partition_id}/{spec.role}",
        f"transform.partition_id {transform.partition_id!r} != spec.partition_id "
        f"{spec.partition_id!r}; partition j's fitted state applied to partition k's frame "
        f"moves j's training statistics onto k's rows regardless of which months overlap. "
        f"The one enumerated exception is REFIT -> DEC under role='score' (the G-06 apply); "
        f"this pair/role is not it (R-74 element 4; ADR-11)",
    )


# --- support fields (R-78): four rules, four failures -----------------------------------


def _support_admitted(name: str, entry: Mapping[str, Any], snapshot: ConfigSnapshot) -> bool:
    """Whether a support field enters the MODEL input set. Default: NO.

    Rule 4 (permanent): a target-hour quality field is refused whether or not approved.
    Rule 2: a read at hour t (lag 0) fails; support fields are readable over hours <= t only
    — so `lag_hours >= 1` is required for admission.
    Rule 1/3: excluded unless `approval.approval_id` is present AND `approval.recorded_utc`
    PRECEDES `features.feature_set_freeze_utc` (three separate assertions).
    """
    resource = f"support field {name!r}"
    if str(entry.get("support_kind", "")).strip() == _TARGET_HOUR_QUALITY:
        raise LeakageError(
            resource,
            "is a target-hour quality field; target-hour quality fields are future "
            "information and permanently forbidden as features, approval or not "
            "(TE 6.2; NFR-LEAK-01; R-78 rule 4)",
        )
    approval = entry.get("approval")
    if approval is None:
        return False  # rule 1: diagnostic by default — the default IS the mechanism
    if not isinstance(approval, Mapping):
        raise LeakageError(resource, "approval must be a mapping {approval_id, recorded_utc}")
    approval_id = approval.get("approval_id")
    if _is_tbd(approval_id) or not str(approval_id).strip():
        raise LeakageError(
            resource,
            "declares an approval with no approval_id; model use of a support field requires "
            "explicit G-04 approval and the ID is the record (R-78 rule 3, first assertion)",
        )
    recorded = approval.get("recorded_utc")
    if _is_tbd(recorded):
        raise LeakageError(
            resource,
            "approval carries no recorded_utc; 'recorded before the feature-set freeze' "
            "cannot be asserted without a timestamp (R-78 rule 3, second assertion)",
        )
    freeze = snapshot.features.get("feature_set_freeze_utc")
    if _is_tbd(freeze):
        raise LeakageError(
            "configs/features.yaml: feature_set_freeze_utc",
            "absent or TBD; an approved support field's approval must be ordered against the "
            "feature-set freeze, and the freeze timestamp is unrecorded (R-78 rule 3)",
        )
    recorded_at = _as_utc(recorded, resource=f"{resource} approval.recorded_utc")
    frozen_at = _as_utc(freeze, resource="features.feature_set_freeze_utc")
    if not recorded_at < frozen_at:
        raise LeakageError(
            resource,
            f"approval recorded at {recorded_at.isoformat()} does not PRECEDE the feature-set "
            f"freeze at {frozen_at.isoformat()}; a presence check would pass an approval "
            f"recorded afterwards, which is what 'recorded before' exists to prevent "
            f"(R-78 rule 3, third assertion)",
        )
    lag = entry.get("lag_hours")
    if _is_tbd(lag) or isinstance(lag, bool) or not isinstance(lag, int) or lag < 1:
        raise LeakageError(
            resource,
            f"lag_hours {lag!r}: a support field is readable over hours <= t only, so a read "
            f"at or beyond the target hour (lag 0) fails (R-78 rule 2)",
        )
    return True


# --- assembly helpers ---------------------------------------------------------------------


def _identity_from_target(records: Sequence[Mapping[str, Any]]) -> dict[str, str]:
    identity: dict[str, str] = {}
    for key in IDENTITY_KEYS:
        values = {str(r.get(key, "") or "").strip() for r in records}
        values.discard("")
        if len(values) != 1:
            raise IntegrityError(
                f"target frame stamp {key!r}",
                f"must carry exactly one non-empty value across every row, found "
                f"{sorted(values)}; every dataset, prediction, mask and comparison carries "
                f"phase_id, source_id and target_definition_id (NFR-TDEF-01; TE 13)",
            )
        identity[key] = values.pop()
    return identity


def _producer_of(frame: Any, *, resource: str) -> str:
    producer = str(frame_attrs(frame).get("producing_artifact", "") or "").strip()
    if not producer:
        raise LeakageError(
            resource,
            "carries no `producing_artifact` provenance; ABSENT provenance FAILS (SD-E-03's "
            "flipped default: a laundered value must forge a stamp, not merely delete one)",
        )
    return producer


def _hourly_series(frame: Any, *, series: str) -> dict[dt.datetime, float | None]:
    out: dict[dt.datetime, float | None] = {}
    for index, record in enumerate(records_of(frame)):
        if "interval_start_utc" not in record or "value" not in record:
            raise IntegrityError(
                f"driver {series} row {index}", "driver rows carry interval_start_utc and value"
            )
        epoch = _as_utc(record["interval_start_utc"], resource=f"driver {series} row {index}")
        raw = record["value"]
        if raw is None or (isinstance(raw, str) and not raw.strip()):
            out[epoch] = None
        else:
            value = float(raw)
            out[epoch] = None if math.isnan(value) else value
    return out


def _assert_driver_alignment(
    frame: Any, *, series: str, hourly: Mapping[dt.datetime, float | None]
) -> None:
    """R-76a's enforcement raise: a driver value repeated outside its interval or shifted to a
    neighbouring hour raises `AlignmentError`, through `external-products`' own assertion."""
    observations = frame_attrs(frame).get("observations")
    if not observations:
        return
    normalised = [
        {
            "value": float(o["value"]),
            "interval_start": _as_utc(o["interval_start"], resource=f"{series} observation"),
            "interval_end": _as_utc(o["interval_end"], resource=f"{series} observation"),
        }
        for o in observations
    ]
    align_interval_series(normalised)  # overlapping or off-hour intervals raise here
    present = {epoch: value for epoch, value in hourly.items() if value is not None}
    assert_alignment(series, present, normalised)


def _read_carry_forward_bound(snapshot: ConfigSnapshot) -> int:
    value = snapshot.features.get("carry_forward_bound_hours")
    if _is_tbd(value):
        raise LeakageError(
            "configs/features.yaml: carry_forward_bound_hours",
            "absent or TBD; the <= 3 h driver carry-forward bound is configuration (TC-09; "
            "FR-P1-04-3), never a literal in source",
        )
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise LeakageError(
            "configs/features.yaml: carry_forward_bound_hours",
            f"{value!r} is not a non-negative int",
        )
    return value


def _time_features(epoch: dt.datetime, wanted: Mapping[str, str]) -> dict[str, float]:
    """utc_hour_* and doy_* from the record timestamp (calendar encodings, not constants)."""
    out: dict[str, float] = {}
    hours_per_day = 24
    hour_angle = 2.0 * math.pi * (epoch.hour + epoch.minute / 60.0) / hours_per_day
    year_days = 366 if _is_leap(epoch.year) else 365
    doy_angle = 2.0 * math.pi * (epoch.timetuple().tm_yday - 1) / year_days
    for name, row in wanted.items():
        if row == "utc_hour_sin":
            out[name] = math.sin(hour_angle)
        elif row == "utc_hour_cos":
            out[name] = math.cos(hour_angle)
        elif row == "doy_sin":
            out[name] = math.sin(doy_angle)
        elif row == "doy_cos":
            out[name] = math.cos(doy_angle)
    return out


def _is_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _station_features(
    epoch: dt.datetime, station: Station, wanted: Mapping[str, Mapping[str, Any]]
) -> dict[str, float]:
    """station_lat, station_onehot_<ID>, lst_sin/lst_cos — longitude enters ONLY through the
    local-solar-time angle `(UTC + lon/15) mod 24` (TE 6.2), never as a column."""
    out: dict[str, float] = {}
    degrees_per_hour = 360.0 / 24.0
    for name, entry in wanted.items():
        row = str(entry["dictionary_row"])
        if row == "station_lat":
            out[name] = float(station.lat)
        elif row == "station_onehot":
            out[name] = 1.0 if str(entry["station_id"]) == station.station_id else 0.0
        elif row in ("lst_sin", "lst_cos"):
            utc_hours = epoch.hour + epoch.minute / 60.0
            lst = (utc_hours + float(station.lon) / degrees_per_hour) % 24.0
            angle = 2.0 * math.pi * lst / 24.0
            out[name] = math.sin(angle) if row == "lst_sin" else math.cos(angle)
    return out


# --- W-2: build_features ------------------------------------------------------------------


def build_features(
    target: Any,
    *,
    drivers: Mapping[str, Any],
    registry: Mapping[str, Station],
    matrix: Sequence[AvailabilityRow],
    spec: FrameSpec,
    partitions: Sequence[Partition],
    snapshot: ConfigSnapshot,
    transform: Transform | None = None,
    parity_tolerance: float | None = None,
    timestamp_column: str = "interval_start_utc",
    station_column: str = "station_id",
) -> FeatureBundle:
    """ADR-11's `build_features`, refusing in the order the module docstring states.

    `parity_tolerance` is the fixture manifest's declared floating-point tolerance for
    WS-13's value-level limb (TE 15.2); `None` makes that limb STOP naming the field (the
    shape/ordering limb runs regardless). Everything else is the approved signature.
    """
    # 1. the spec against the partition list
    partition = validate_spec(spec, partitions)
    # 2. the identity check
    assert_transform_identity(transform, spec)
    # 3. the closed dictionary, its classes, Dst, support policy
    dictionary = load_feature_dictionary(snapshot)
    declared_classes = {
        name: SECTION_6_2_ROWS[str(entry["dictionary_row"])].value
        for name, entry in dictionary.items()
    }
    classes = assert_field_classes_partition(declared_classes)
    assert_dst_diagnostic_only(declared_classes)
    feature_set: dict[str, Mapping[str, Any]] = {}
    for name, entry in dictionary.items():
        field_class = classes[name]
        if field_class in _MODEL_INPUT_CLASSES:
            feature_set[name] = entry
        elif field_class is FieldClass.support and _support_admitted(name, entry, snapshot):
            feature_set[name] = entry
        # diagnostic and unapproved support: excluded — the default is the mechanism
    if not feature_set:
        raise LeakageError(
            "feature dictionary", "admits no model-input field; nothing to construct"
        )
    # 4. the permitted-producer list — the fail-closed refusal (SD-F-01)
    rows_in_set = sorted({str(entry["dictionary_row"]) for entry in feature_set.values()})
    producers = load_permitted_producers(snapshot, dictionary_rows=rows_in_set)
    # the availability matrix must cover every driver field the set requests
    matrix_features = {row.feature for row in matrix}
    for name, entry in feature_set.items():
        if classes[name] is FieldClass.driver and name not in matrix_features:
            raise LeakageError(
                f"feature {name!r}",
                f"has no availability-matrix row; every predictor is lagged to its actual "
                f"availability and asserted before it enters (FR-P1-04-2; rows present: "
                f"{sorted(matrix_features)})",
            )
    # 5. the registry gates station-derived fields
    station_fields = {n: e for n, e in feature_set.items() if classes[n] is FieldClass.station}
    if station_fields:
        assert_registry_resolved(registry)
    # the frozen window
    sequence_fields = {
        n: e for n, e in feature_set.items() if str(e["dictionary_row"]) == "vtec_seq_24"
    }
    lag_fields = {
        n: e for n, e in feature_set.items() if str(e["dictionary_row"]) == "vtec_lag"
    }
    step_counts = {int(e["sequence_steps"]) for e in sequence_fields.values()}
    if len(step_counts) != 1:
        raise LeakageError(
            "feature dictionary",
            f"sequence fields declare {len(step_counts)} distinct step counts "
            f"{sorted(step_counts)}; one window length per feature-set ID (TE 6.4; "
            f"FR-P1-04-12)",
        )
    window_hours = read_window_length(snapshot, sequence_steps=step_counts.pop())

    # --- the target frame: provenance, identity, rows in the scored range -------------------
    target_producer = _producer_of(target, resource="target frame")
    target_records = records_of(target)
    if not target_records:
        raise LeakageError("target frame", "is empty; nothing to construct and no check to run")
    identity = _identity_from_target(target_records)
    in_range = [
        r
        for r in target_records
        if spec.scored_start
        <= _as_utc(r[timestamp_column], resource="target row")
        < spec.scored_end
    ]
    if not in_range:
        raise LeakageError(
            f"target frame for {spec.partition_id}/{spec.role}",
            "carries no row inside the scored range; an empty assembled frame is a check that "
            "never ran (R-74's empty-frame control)",
        )
    assert_membership_from_timestamps(
        in_range, partition=partition, role=spec.role, timestamp_column=timestamp_column
    )
    windowed = build_windows(
        in_range,
        window_hours=window_hours,
        sequence_fields={n: str(e["source_column"]) for n, e in sequence_fields.items()},
        lag_fields={
            n: (str(e["source_column"]), int(e["lag_hours"])) for n, e in lag_fields.items()
        },
        scored_start=spec.scored_start,
        scored_end=spec.scored_end,
        timestamp_column=timestamp_column,
        station_column=station_column,
    )
    excluded: dict[str, int] = {
        "excluded_before_scored_start": windowed.excluded_before_scored_start,
        "excluded_incomplete_windows": windowed.excluded_incomplete_windows,
    }

    # --- drivers through the field-class boundary and the alignment raise ---------------
    driver_fields = {n: e for n, e in feature_set.items() if classes[n] is FieldClass.driver}
    driver_values: dict[str, Mapping[dt.datetime, float]] = {}
    driver_producers: dict[str, str] = {}
    if driver_fields:
        bound = _read_carry_forward_bound(snapshot)
        for name, entry in driver_fields.items():
            series = str(entry["source_series"])
            if series not in drivers:
                raise LeakageError(
                    f"driver field {name!r}", f"source_series {series!r} not supplied"
                )
            frame = drivers[series]
            driver_producers[name] = _producer_of(frame, resource=f"driver series {series!r}")
            hourly = _hourly_series(frame, series=series)
            _assert_driver_alignment(frame, series=series, hourly=hourly)
            carried = carry_forward(
                hourly, field_class=FieldClass.driver, bound_h=bound, feature=name
            )
            driver_values[name] = carried["values"]
            excluded[f"carry_forward_excluded_{name}"] = carried["excluded_count"]
            excluded[f"carry_forward_carried_{name}"] = len(carried["carried_forward_epochs"])

    # --- assemble ---------------------------------------------------------------------------
    time_fields = {
        n: str(e["dictionary_row"])
        for n, e in feature_set.items()
        if classes[n] is FieldClass.time
    }
    support_fields = {n: e for n, e in feature_set.items() if classes[n] is FieldClass.support}
    by_station_hour: dict[tuple[str, dt.datetime], Mapping[str, Any]] = {
        (str(r[station_column]), _as_utc(r[timestamp_column], resource="target row")): r
        for r in in_range
    }
    columns: list[str] = []
    for name in feature_set:
        if name in sequence_fields:
            columns.extend(windowed.sequence_columns[name])
        else:
            columns.append(name)
    assembled: list[dict[str, Any]] = []
    nested_kept: list[int] = []
    driver_rows_excluded = 0
    for index, record in enumerate(windowed.records):
        epoch = _as_utc(record[timestamp_column], resource="window row")
        station_id = str(record[station_column])
        row: dict[str, Any] = {timestamp_column: epoch.isoformat(), station_column: station_id}
        for name in lag_fields:
            row[name] = record[name]
        for name in sequence_fields:
            for column in windowed.sequence_columns[name]:
                row[column] = record[column]
        row.update(_time_features(epoch, time_fields))
        if station_fields:
            row.update(_station_features(epoch, registry[station_id], station_fields))
        drop = False
        for name in driver_fields:
            value = driver_values[name].get(epoch)
            if value is None:
                drop = True
                break
            row[name] = value
        if drop:
            driver_rows_excluded += 1
            continue
        for name, entry in support_fields.items():
            read_at = epoch - dt.timedelta(hours=int(entry["lag_hours"]))
            source_row = by_station_hour.get((station_id, read_at))
            if source_row is None or source_row.get(str(entry["source_column"])) is None:
                drop = True
                break
            row[name] = source_row[str(entry["source_column"])]
        if drop:
            excluded["support_rows_excluded"] = excluded.get("support_rows_excluded", 0) + 1
            continue
        assembled.append(row)
        nested_kept.append(index)
    excluded["driver_rows_excluded"] = driver_rows_excluded
    if not assembled:
        raise LeakageError(
            f"assembled frame for {spec.partition_id}/{spec.role}",
            "is empty after windowing and exclusions; an empty assembled frame is a check that "
            "never ran, and must not pass for one that did (R-74)",
        )
    # every assembled column is a dictionary field or a flattened step of one
    admitted = set(columns) | {timestamp_column, station_column}
    for row in assembled:
        outside = sorted(set(row) - admitted)
        if outside:
            raise LeakageError(
                f"assembled frame for {spec.partition_id}/{spec.role}",
                f"carries column(s) {outside} outside the closed TE 6.2 dictionary (FR-P1-04-12)",
            )

    # --- transform (inside build_features, before both representations) -----------------
    standardized = tuple(
        n
        for n, e in feature_set.items()
        if str(e["normalization"]) == _STANDARDIZE and n not in sequence_fields
    ) + tuple(
        c
        for n in sequence_fields
        if str(feature_set[n]["normalization"]) == _STANDARDIZE
        for c in windowed.sequence_columns[n]
    )
    transform_id: str | None = None
    if transform is not None:
        assembled = apply_fitted_transform(assembled, transform)
        transform_id = transform.transform_id

    # --- both representations from the one window, then parity --------------------------
    nested_all = tensor_as_nested(windowed.tensor)
    nested = [nested_all[i] for i in nested_kept]
    if transform is not None:
        # the tensor inherits the same standardisation as its flattened columns (one definition)
        for row_index, steps in enumerate(nested):
            for step_index, step in enumerate(steps):
                for feature_index, name in enumerate(windowed.tensor_features):
                    column = windowed.sequence_columns[name][step_index]
                    if column in transform.columns:
                        step[feature_index] = (
                            float(step[feature_index]) - transform.means[column]
                        ) / transform.scales[column]
    tensor = tensor_from_nested(
        nested, shape=(len(nested), window_hours, len(windowed.tensor_features))
    )
    assert_window_parity(
        assembled,
        tensor,
        sequence_columns=windowed.sequence_columns,
        tensor_features=windowed.tensor_features,
        tolerance=parity_tolerance,
    )

    # --- provenance: (row, producer) resolved per column, key set == column set --------
    provenance: dict[str, dict[str, str]] = {}
    for name, entry in feature_set.items():
        row_id = str(entry["dictionary_row"])
        field_class = classes[name]
        if field_class is FieldClass.driver:
            producer = driver_producers[name]
        elif field_class is FieldClass.station:
            producer = STATION_REGISTRY_PRODUCER
        elif field_class is FieldClass.time:
            producer = TIMESTAMP_PRODUCER
        else:
            producer = target_producer
        if producer not in producers[row_id]:
            raise LeakageError(
                f"feature {name!r}",
                f"produced by {producer!r}, which is not a permitted producer for dictionary "
                f"row {row_id!r} ({list(producers[row_id])}); provenance is resolved per "
                f"(row, producer) pair, so a value with a legitimate name and an illegitimate "
                f"history — or a column mislabelled to the wrong row — is refused (SD-F-01)",
            )
        stamp = {
            "dictionary_row": row_id,
            "dictionary_field": name,
            "producing_artifact": producer,
        }
        if name in sequence_fields:
            for column in windowed.sequence_columns[name]:
                provenance[column] = dict(stamp)
        else:
            provenance[name] = stamp
    _assert_provenance_matches_columns(provenance, columns)

    frame_columns = [timestamp_column, station_column, *columns]
    matrix_frame = frame_from_records(
        assembled,
        columns=frame_columns,
        attrs={**identity, "partition_id": spec.partition_id, "role": spec.role},
    )
    return FeatureBundle(
        matrix=matrix_frame,
        tensor=tensor,
        spec=spec,
        transform_id=transform_id,
        provenance=provenance,
        identity=identity,
        excluded_counts=excluded,
        standardized_columns=standardized,
        sequence_columns=dict(windowed.sequence_columns),
        tensor_features=tuple(windowed.tensor_features),
    )


def _assert_provenance_matches_columns(
    provenance: Mapping[str, Mapping[str, str]], columns: Sequence[str]
) -> None:
    keys = set(provenance)
    cols = set(columns)
    if keys != cols:
        raise LeakageError(
            "bundle provenance",
            f"key set differs from the matrix column set: columns without an entry "
            f"{sorted(cols - keys)}, entries without a column {sorted(keys - cols)}; the two "
            f"sets are asserted EQUAL, never provenance-as-subset (SD-F-02)",
        )


# --- M9: the bundle on disk ---------------------------------------------------------------


def bundle_directory_name(spec: FrameSpec, transform_id: str | None) -> str:
    """`<partition_id>__<role>__<transform_id>/`, literal `untransformed` for `None`."""
    return f"{spec.partition_id}__{spec.role}__{transform_id or UNTRANSFORMED_SEGMENT}"


def _feature_columns(bundle: FeatureBundle) -> list[str]:
    return [c for c in columns_of(bundle.matrix) if c in bundle.provenance]


def _spec_payload(bundle: FeatureBundle) -> dict[str, Any]:
    return {
        "partition_id": bundle.spec.partition_id,
        "role": bundle.spec.role,
        "scored_start": bundle.spec.scored_start.isoformat(),
        "scored_end": bundle.spec.scored_end.isoformat(),
        "transform_id": bundle.transform_id,
        **{key: bundle.identity.get(key, "") for key in IDENTITY_KEYS},
        "columns": _feature_columns(bundle),
        "provenance": {k: dict(v) for k, v in bundle.provenance.items()},
        "excluded_counts": dict(bundle.excluded_counts),
        "standardized_columns": list(bundle.standardized_columns),
        "sequence_columns": {k: list(v) for k, v in bundle.sequence_columns.items()},
        "tensor_features": list(bundle.tensor_features),
    }


def write_bundle(bundle: FeatureBundle, out_root: Path) -> Path:
    """Persist ONE directory per bundle: `matrix.parquet`, `tensor.npy`, `spec.json`.

    Raises
    ------
    IntegrityError
        an existing bundle directory (never overwritten); a missing identity stamp; `pyarrow`
        not importable — TE 8.1's required Parquet engine is NOT pinned in
        `requirements.txt` today, and adding an unpinned dependency is a reviewed pin
        change, not an implementer default, so the writer refuses with that message.
    """
    for key in IDENTITY_KEYS:
        if not str(bundle.identity.get(key, "") or "").strip():
            raise IntegrityError(
                f"bundle {bundle_directory_name(bundle.spec, bundle.transform_id)}",
                f"identity stamp {key!r} is missing; every dataset carries all three "
                f"(NFR-TDEF-01)",
            )
    _assert_provenance_matches_columns(bundle.provenance, _feature_columns(bundle))
    if not pandas_available() or importlib.util.find_spec("pyarrow") is None:
        raise IntegrityError(
            "matrix.parquet",
            "writing the matrix needs pandas with the pyarrow engine (TE 8.1's required "
            "artifact format), and pyarrow is not pinned in requirements.txt; the pin is a "
            "reviewed change (team.md Way of Working), never an implementer's default, so no "
            "bundle is written",
        )
    import numpy as np

    directory = Path(out_root) / bundle_directory_name(bundle.spec, bundle.transform_id)
    if directory.exists():
        raise IntegrityError(
            directory, "bundle directory already exists; a bundle is never overwritten (TE 13.3)"
        )
    directory.mkdir(parents=True)
    bundle.matrix.to_parquet(directory / "matrix.parquet", engine="pyarrow", index=False)
    np.save(directory / "tensor.npy", np.asarray(bundle.tensor, dtype=float))
    (directory / "spec.json").write_text(
        json.dumps(_spec_payload(bundle), indent=2, sort_keys=True), encoding="utf-8"
    )
    return directory


def load_bundle(directory: Path) -> FeatureBundle:
    """Read all three files or raise; a directory name disagreeing with its `spec.json`
    raises; a provenance key set differing from the matrix columns raises (a dropped stamp is
    a load failure, SD-F-02)."""
    directory = Path(directory)
    missing = [
        n for n in ("matrix.parquet", "tensor.npy", "spec.json") if not (directory / n).is_file()
    ]
    if missing:
        raise IntegrityError(
            directory, f"bundle is missing {missing}; the three files are one artifact (M9)"
        )
    try:
        payload = json.loads((directory / "spec.json").read_text(encoding="utf-8"))
        spec = FrameSpec(
            partition_id=str(payload["partition_id"]),
            role=payload["role"],
            scored_start=_as_utc(payload["scored_start"], resource="spec.json scored_start"),
            scored_end=_as_utc(payload["scored_end"], resource="spec.json scored_end"),
        )
        transform_id = payload.get("transform_id")
        provenance = {str(k): dict(v) for k, v in payload["provenance"].items()}
        identity = {key: str(payload.get(key, "")) for key in IDENTITY_KEYS}
        columns = [str(c) for c in payload["columns"]]
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise IntegrityError(directory / "spec.json", f"spec is malformed ({exc})") from exc
    expected_name = bundle_directory_name(spec, transform_id)
    if directory.name != expected_name:
        raise IntegrityError(
            directory,
            f"directory name disagrees with its spec.json (expected {expected_name!r}); the "
            f"name is a second copy of the stamp and a disagreement is detectable (M9)",
        )
    _assert_provenance_matches_columns(provenance, columns)
    for key in IDENTITY_KEYS:
        if not identity[key].strip():
            raise IntegrityError(directory / "spec.json", f"identity stamp {key!r} is missing")
    if not pandas_available():
        raise IntegrityError(directory / "matrix.parquet", "pandas is required to read the matrix")
    import numpy as np
    import pandas as pd

    matrix = pd.read_parquet(directory / "matrix.parquet")
    tensor = np.load(directory / "tensor.npy")
    matrix_columns = [c for c in matrix.columns if c in provenance]
    if set(matrix_columns) != set(columns):
        raise IntegrityError(
            directory / "matrix.parquet",
            f"matrix columns {sorted(matrix_columns)} differ from spec.json's {sorted(columns)}",
        )
    return FeatureBundle(
        matrix=matrix,
        tensor=tensor,
        spec=spec,
        transform_id=transform_id,
        provenance=provenance,
        identity=identity,
        excluded_counts={str(k): int(v) for k, v in payload.get("excluded_counts", {}).items()},
        standardized_columns=tuple(payload.get("standardized_columns", [])),
        sequence_columns={
            str(k): tuple(v) for k, v in payload.get("sequence_columns", {}).items()
        },
        tensor_features=tuple(payload.get("tensor_features", [])),
    )
