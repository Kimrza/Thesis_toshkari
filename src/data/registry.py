"""The station registry: Vision 6.2 in full, provenance-aware, conflict-honest.

Purpose
-------
The `inventory-and-registry` unit's W-2/W-2a/W-3/W-4 surface: the approved `Station`
contract (`component-methods.md`, `src/data/registry.py` block) plus the ONE amendment
this unit owes — a per-field `provenance` value (R-46, stated as an amendment against the
approved dataclass and applied here at 3.5 under the approved plan). `load_registry`
builds the registry from `configs/data.yaml`; `assert_registry_resolved` raises
`RegistryError` when any Vision 6.2 field is missing, when `igrf_version` is a default
rather than a pin, when a field's provenance is absent, or when a conflict was resolved
by averaging (through the conflict register's named-source equality).

**The registry cannot be built today, by design (Q2 = A, receipted 2026-09-05).** The
station coordinates, the coordinate-to-cell rule and the IGRF version defer to ONE
pre-G-P1A freeze event; `configs/data.yaml` keeps its `TBD — freeze gate` sentinels and
`load_registry` REFUSES at runtime until the owner's transcription lands, citing its
D-numbers. No coordinate, cell index or IGRF version appears in this module (TC-03e;
TE 18.2 — no implementer fills a freeze-gate value by convenience). The code is complete;
the values await the freeze.

Inputs
------
A `ConfigSnapshot` from `foundation`'s `load_configs` (the only read of `configs/`); the
frozen notebook literal, supplied by the caller at migration time for R-48's diff. An
unresolved registry BLOCKS `station_lat` and EXCLUDES `lst_sin`/`lst_cos`:
`features.build` calls `assert_registry_resolved` before constructing either.

Re-run behaviour
----------------
Pure functions of the snapshot; nothing is written, no network, no restricted path. A
re-run against an unchanged config yields an identical registry. This module holds no
restricted-root literal and constructs no path into the restricted root (R-28).

Governance
----------
* `component-methods.md` — the approved `Station`, `load_registry`,
  `assert_registry_resolved` signatures, reproduced without widening; the `provenance`
  field is the unit's one stated amendment (R-46).
* D-1 froze the cell rule — `cell = (floor(lat), floor(lon))`, half-open
  `[floor, floor+1)` on both axes, a station exactly on a boundary belonging to the
  higher-indexed cell. The rule's IDENTIFIER is validated here; its numeric consequences
  enter only through the config transcription the freeze event owns.
* R-47 — a resolved value equals the single value of its NAMED source and carries a
  non-empty rationale; the coincidence residual (a mean equal to the named source's own
  value) is UNDETECTABLE by any value check and is pinned by test, not claimed caught.
* R-48 — the migration emits a diff against the notebook literal and asserts no value
  changed; the freeze prevents an intentional change, the diff catches the accidental
  transposed digit.
* What provenance is SUFFICIENT is not decided here: coordinates are a §18.2 Student
  forbidden choice, the cell rule Student + Supervisor. `assert_provenance_sufficient`
  is the per-consumer mechanism; it ships with no default requirement.
"""

from __future__ import annotations

import datetime as _dt
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Final

from src.data.config import TBD_SENTINEL, ConfigSnapshot, RegistryError

__all__ = [
    "SECTION_6_2_FIELDS",
    "CELL_RULE_ID",
    "Station",
    "ConflictResolution",
    "assert_resolution",
    "load_registry",
    "assert_registry_resolved",
    "assert_provenance_sufficient",
    "migration_diff",
    "assert_migration_unchanged",
]

#: Vision 6.2's content fields, per station — the seven items beyond coordinates plus
#: the coordinates themselves. Every one carries a provenance value (R-46).
SECTION_6_2_FIELDS: Final[tuple[str, ...]] = (
    "lat",
    "lon",
    "ellipsoidal_height_m",
    "domes",
    "receiver_intervals",
    "antenna_intervals",
    "firmware_intervals",
    "sampling_interval_s",
    "observable_codes",
    "hardware_changes_2022",
    "igrf_version",
)

#: The identifier of D-1's frozen coordinate-to-cell rule. The config's `cell_rule`
#: value must equal this identifier once the freeze event transcribes it; any other
#: value (including the TBD sentinel) is refused. The identifier names the frozen rule
#: — it does not choose one (D-1 is the freeze; TE 18.2 stands).
CELL_RULE_ID: Final[str] = "floor-half-open-d1"

#: Values that mark an igrf_version as DEFAULTED rather than pinned. A default and an
#: absence are refused identically (R-45; the R-35 "unknown" precedent).
_DEFAULT_MARKERS: Final[tuple[str, ...]] = ("default", "unknown")

#: The calendar year every hardware interval set must cover (D-8's frozen study year —
#: a claim-boundary identity, not a chosen value).
_STUDY_YEAR: Final[int] = 2022


@dataclass(frozen=True)
class Station:
    """The approved stage-2.6 contract, plus the ONE amendment: per-field provenance.

    `provenance` maps each Vision 6.2 field name to the source the value was taken from
    (e.g. an IGS site log versus an IGS network page). Presence is not provenance
    (R-46): D-1's site-log validation limitation is still open, and the mechanism keeps
    what is *not yet established* about a value attached to the value.
    """

    station_id: str
    lat: float
    lon: float
    ellipsoidal_height_m: float
    domes: str
    receiver_intervals: Sequence[tuple[_dt.date, _dt.date, str]]
    antenna_intervals: Sequence[tuple[_dt.date, _dt.date, str]]
    firmware_intervals: Sequence[tuple[_dt.date, _dt.date, str]]
    sampling_interval_s: int
    observable_codes: Sequence[str]
    hardware_changes_2022: Sequence[tuple[_dt.date, str]]
    igrf_version: str  # pinned, never defaulted
    cell: tuple[int, int]  # (floor(lat), floor(lon)), half-open, D-1
    provenance: Mapping[str, str] = field(default_factory=dict)  # R-46 amendment


@dataclass(frozen=True)
class ConflictResolution:
    """One resolved field of the conflict register (W-3, R-47).

    `source_values` records EVERY source value (limb 1); `named_source` is the source
    the resolution NAMES (limb 3); `resolved_value` must be identical to that named
    source's value (limb 2); `rationale` must be non-empty (limb 3). Limb 4 — the
    injection negative control, including the coincidence case — lives in the tests.
    """

    station_id: str
    field: str
    source_values: Mapping[str, object]
    named_source: str
    resolved_value: object
    rationale: str


def assert_resolution(resolution: ConflictResolution) -> None:
    """R-47 limbs 2 and 3: named-source equality plus a non-empty rationale.

    The equality binds the value to the source it NAMES — not merely to *some* recorded
    source value, because with three or more sources an existence check passes an
    average ({0, 3, 6} averages to the recorded 3). The stated residual stands: a mean
    that coincides bit-for-bit with the named source's own value is indistinguishable
    from a legitimate resolution by any value check; the rationale, read by a human at
    G-P1A, is what reaches that case.

    Raises
    ------
    RegistryError
        naming the station and field, when the named source is not in the register,
        when the resolved value does not equal the named source's value, or when the
        rationale is empty.
    """
    resource = f"{resolution.station_id}.{resolution.field}"
    if resolution.named_source not in resolution.source_values:
        raise RegistryError(
            resource,
            f"resolution names source {resolution.named_source!r}, which is not in the "
            f"conflict register; every source value is recorded and the named source "
            f"must be one of them (R-47 limbs 1 and 3)",
        )
    named_value = resolution.source_values[resolution.named_source]
    if resolution.resolved_value != named_value:
        raise RegistryError(
            resource,
            f"resolved value {resolution.resolved_value!r} is not identical to the "
            f"value of the source it NAMES ({resolution.named_source!r} = "
            f"{named_value!r}); a conflict is resolved and recorded, never averaged or "
            f"ignored, and matching merely some recorded value is insufficient (R-47 "
            f"limb 2)",
        )
    if not resolution.rationale.strip():
        raise RegistryError(
            resource,
            "resolution carries an empty rationale; §6.2 states two obligations — "
            "resolved AND recorded — and the rationale is what a G-P1A reviewer judges "
            "(R-47 limb 3)",
        )


def _cell_for(lat: float, lon: float) -> tuple[int, int]:
    """D-1's frozen rule: `(floor(lat), floor(lon))`, half-open on both axes.

    `floor` is half-open by construction — a station exactly on a boundary belongs to
    the higher-indexed cell, and no station is counted twice. Reached only AFTER
    `load_registry` has verified the config names D-1's rule identifier; this function
    applies a frozen rule, it does not choose one.
    """
    return (math.floor(lat), math.floor(lon))


def _parse_intervals(
    raw: object, *, resource: str, kind: str
) -> tuple[tuple[_dt.date, _dt.date, str], ...]:
    if not isinstance(raw, Sequence) or isinstance(raw, str | bytes):
        raise RegistryError(resource, f"{kind} must be a sequence of [start, end, label] entries")
    parsed: list[tuple[_dt.date, _dt.date, str]] = []
    for entry in raw:
        try:
            start_raw, end_raw, label = entry  # type: ignore[misc]
            start = _dt.date.fromisoformat(str(start_raw))
            end = _dt.date.fromisoformat(str(end_raw))
        except (TypeError, ValueError) as exc:
            raise RegistryError(
                resource,
                f"{kind} entry {entry!r} is not a parseable [start, end, label] triple "
                f"({exc}); an interval the check cannot read cannot be cleared",
            ) from None
        parsed.append((start, end, str(label)))
    return tuple(parsed)


def _intervals_cover_year(
    intervals: Sequence[tuple[_dt.date, _dt.date, str]], year: int
) -> bool:
    """Whether the union of intervals covers [Jan 1, Dec 31] of `year`."""
    needed = _dt.date(year, 1, 1)
    year_end = _dt.date(year, 12, 31)
    for start, end, _label in sorted(intervals):
        if start > needed:
            return False
        if end >= needed:
            needed = end + _dt.timedelta(days=1)
        if needed > year_end:
            return True
    return needed > year_end


def _is_defaulted(igrf_version: str) -> bool:
    lowered = igrf_version.strip().lower()
    return any(marker in lowered for marker in _DEFAULT_MARKERS)


def load_registry(snapshot: ConfigSnapshot) -> Mapping[str, Station]:
    """W-2: build the station registry from `configs/data.yaml` — or REFUSE.

    Refusal is the designed state today (Q2 = A): `stations`, `cell_rule` and
    `igrf_version` stay `TBD — freeze gate` until the ONE pre-G-P1A freeze event, and
    this function raises rather than defaulting any of them. When the transcription
    lands, each station entry supplies the Vision 6.2 fields plus a per-field
    `provenance` mapping; the cell is computed by D-1's rule and cross-checked against
    any transcribed cell.

    Raises
    ------
    RegistryError
        naming the registry artifact (`configs/data.yaml:stations`) or the
        `station_id`: an unresolved sentinel, an unknown cell-rule identifier, a
        missing 6.2 field, an absent-or-defaulted `igrf_version` (an absent version
        FAILS — it never falls back to a library default, R-45), or a transcribed cell
        disagreeing with the D-1 rule.
    """
    data = snapshot.data
    stations_block = data.get("stations")
    if stations_block is None or (
        isinstance(stations_block, str) and stations_block.strip() == TBD_SENTINEL
    ):
        raise RegistryError(
            "configs/data.yaml:stations",
            "station coordinates are unresolved (TBD — freeze gate); coordinates, the "
            "cell rule and the IGRF version defer to ONE pre-G-P1A freeze event "
            "(Q2=A), the values are the Student's §18.2 forbidden choice, and this "
            "code refuses rather than defaulting them (TE 18.2/18.3; D-1's site-log "
            "limitation is still open)",
        )
    if not isinstance(stations_block, Mapping) or not stations_block:
        raise RegistryError(
            "configs/data.yaml:stations",
            "stations must be a non-empty mapping of station_id to its transcribed "
            "6.2 entry",
        )

    cell_rule = data.get("cell_rule")
    if cell_rule is None or (isinstance(cell_rule, str) and cell_rule.strip() == TBD_SENTINEL):
        raise RegistryError(
            "configs/data.yaml:cell_rule",
            "the coordinate-to-cell rule is unresolved (TBD — freeze gate); D-1 is the "
            "freeze and the migration transcribes its identifier at the single freeze "
            "event (Q2=A) — refused, never defaulted",
        )
    if str(cell_rule) != CELL_RULE_ID:
        raise RegistryError(
            "configs/data.yaml:cell_rule",
            f"cell_rule {cell_rule!r} is not the frozen D-1 identifier "
            f"{CELL_RULE_ID!r}; an unrecognised rule is refused, never guessed",
        )

    igrf_version = data.get("igrf_version")
    if igrf_version is None or (
        isinstance(igrf_version, str)
        and (not igrf_version.strip() or igrf_version.strip() == TBD_SENTINEL)
    ):
        raise RegistryError(
            "configs/data.yaml:igrf_version",
            "igrf_version is absent or unresolved; an ABSENT version FAILS exactly as a "
            "defaulted one fails — it never falls back to a library default (R-45, "
            "TS-I-01), and the pin stays TBD — freeze gate until frozen under a "
            "D-number",
        )
    igrf_text = str(igrf_version).strip()

    registry: dict[str, Station] = {}
    for station_id, raw in stations_block.items():
        sid = str(station_id)
        if not isinstance(raw, Mapping):
            raise RegistryError(sid, "station entry must be a mapping of 6.2 fields")
        missing = [
            name
            for name in ("lat", "lon", "ellipsoidal_height_m", "domes", "sampling_interval_s")
            if raw.get(name) is None or str(raw.get(name)).strip() == ""
        ]
        if missing:
            raise RegistryError(
                sid,
                "station entry is missing 6.2 field(s): " + ", ".join(missing) + " (R-45)",
            )
        lat = float(raw["lat"])  # type: ignore[arg-type]
        lon = float(raw["lon"])  # type: ignore[arg-type]
        computed_cell = _cell_for(lat, lon)
        if "cell" in raw:
            declared_cell = (int(raw["cell"][0]), int(raw["cell"][1]))  # type: ignore[index]
            if declared_cell != computed_cell:
                raise RegistryError(
                    sid,
                    f"transcribed cell {declared_cell} disagrees with D-1's rule "
                    f"applied to the transcribed coordinates ({computed_cell}); a "
                    f"disagreement is surfaced, never silently preferred one way",
                )
        provenance_raw = raw.get("provenance")
        provenance: dict[str, str] = (
            {str(k): str(v) for k, v in provenance_raw.items()}
            if isinstance(provenance_raw, Mapping)
            else {}
        )
        hardware_raw = raw.get("hardware_changes_2022", ())
        hardware: list[tuple[_dt.date, str]] = []
        if isinstance(hardware_raw, Sequence) and not isinstance(hardware_raw, str | bytes):
            for entry in hardware_raw:
                stamp, note = entry  # type: ignore[misc]
                hardware.append((_dt.date.fromisoformat(str(stamp)), str(note)))
        registry[sid] = Station(
            station_id=sid,
            lat=lat,
            lon=lon,
            ellipsoidal_height_m=float(raw["ellipsoidal_height_m"]),  # type: ignore[arg-type]
            domes=str(raw["domes"]),
            receiver_intervals=_parse_intervals(
                raw.get("receiver_intervals", ()), resource=sid, kind="receiver_intervals"
            ),
            antenna_intervals=_parse_intervals(
                raw.get("antenna_intervals", ()), resource=sid, kind="antenna_intervals"
            ),
            firmware_intervals=_parse_intervals(
                raw.get("firmware_intervals", ()), resource=sid, kind="firmware_intervals"
            ),
            sampling_interval_s=int(raw["sampling_interval_s"]),  # type: ignore[arg-type]
            observable_codes=tuple(str(code) for code in raw.get("observable_codes", ())),
            hardware_changes_2022=tuple(hardware),
            igrf_version=igrf_text,
            cell=computed_cell,
            provenance=provenance,
        )
    return registry


def assert_registry_resolved(registry: Mapping[str, Station]) -> None:
    """The approved gate: raises `RegistryError` on any unresolved station (R-45/R-46).

    Checks, per station: every 6.2 field present and non-empty; receiver, antenna and
    firmware intervals COVERING ALL OF 2022; a pinned (never defaulted) `igrf_version`
    — an absent version was already refused at load, and a default marker is refused
    here; and a provenance value for EVERY 6.2 field (presence is not provenance —
    omitting the provenance value entirely raises; what provenance is SUFFICIENT is the
    owner's question, mechanised by `assert_provenance_sufficient`).

    An unresolved registry BLOCKS `station_lat` and EXCLUDES `lst_sin`/`lst_cos`:
    `features.build` calls this before constructing either.

    Raises
    ------
    RegistryError
        naming the `station_id` (the station-registry resource, SD-I-03) and the
        violated expectation.
    """
    if not registry:
        raise RegistryError(
            "station registry",
            "registry is empty; an empty registry cannot authorise station_lat or "
            "lst_sin/lst_cos construction (R-45)",
        )
    for sid, station in registry.items():
        if not station.domes.strip():
            raise RegistryError(sid, "domes / full identifier is missing (6.2; R-45)")
        for kind, intervals in (
            ("receiver_intervals", station.receiver_intervals),
            ("antenna_intervals", station.antenna_intervals),
            ("firmware_intervals", station.firmware_intervals),
        ):
            if not intervals:
                raise RegistryError(sid, f"{kind} is empty (6.2 requires intervals; R-45)")
            if not _intervals_cover_year(intervals, _STUDY_YEAR):
                raise RegistryError(
                    sid,
                    f"{kind} does not cover all of {_STUDY_YEAR}; 6.2 requires "
                    f"intervals covering the whole study year (R-45)",
                )
        if station.sampling_interval_s <= 0:
            raise RegistryError(sid, "sampling_interval_s must be a positive integer (R-45)")
        if not station.observable_codes:
            raise RegistryError(sid, "observable_codes is empty (6.2; R-45)")
        if not station.igrf_version.strip():
            raise RegistryError(
                sid,
                "igrf_version is empty; an absent version FAILS, it never falls back "
                "(R-45)",
            )
        if station.igrf_version.strip() == TBD_SENTINEL:
            raise RegistryError(
                sid,
                "igrf_version is unresolved (TBD — freeze gate); the pin is frozen at "
                "the single pre-G-P1A freeze event (Q2=A), never defaulted (R-45)",
            )
        if _is_defaulted(station.igrf_version):
            raise RegistryError(
                sid,
                f"igrf_version {station.igrf_version!r} is a DEFAULT rather than a pin; "
                f"the distinction that matters is between no value and a value chosen "
                f"for you, and both are refused (R-45, TS-I-01)",
            )
        missing_provenance = [
            name for name in SECTION_6_2_FIELDS if not station.provenance.get(name, "").strip()
        ]
        if missing_provenance:
            raise RegistryError(
                sid,
                "provenance value(s) missing for 6.2 field(s): "
                + ", ".join(missing_provenance)
                + " — presence is not provenance, and a field with no recorded source "
                "cannot be resolved (R-46, W-2a)",
            )


def assert_provenance_sufficient(
    registry: Mapping[str, Station], required: Mapping[str, str]
) -> None:
    """The per-consumer sufficiency check (R-46's chosen reading).

    `required` maps a 6.2 field name to the provenance a CONSUMER requires (for
    example, a gate demanding site-log provenance for coordinates where a fixture run
    does not). An empty mapping proceeds: this module ships NO default requirement,
    because what provenance is sufficient is a §18.2 owner question, and a written
    default is how a deferral stops being one.

    Raises
    ------
    RegistryError
        naming the station and field whose recorded provenance does not satisfy the
        consumer's requirement.
    """
    for sid, station in registry.items():
        for field_name, needed in required.items():
            recorded = station.provenance.get(field_name, "")
            if recorded != needed:
                raise RegistryError(
                    sid,
                    f"provenance for {field_name!r} is {recorded!r}, but the requesting "
                    f"consumer requires {needed!r}; the value is not treated as final "
                    f"for this consumer (FR-P1-02-1; D-1's site-log limitation is "
                    f"still open)",
                )


def migration_diff(
    notebook_literal: Mapping[str, Mapping[str, object]],
    migrated: Mapping[str, Mapping[str, object]],
) -> list[str]:
    """R-48: the migration's diff against the frozen notebook literal.

    Compares every station and every field present in the notebook literal against the
    migrated values, plus stations present on one side only. Returns a list of
    human-readable differences — empty means no value changed in the move.
    """
    differences: list[str] = []
    for sid in sorted(set(notebook_literal) | set(migrated)):
        if sid not in migrated:
            differences.append(f"{sid}: present in the notebook literal, absent after migration")
            continue
        if sid not in notebook_literal:
            differences.append(f"{sid}: absent from the notebook literal, added by migration")
            continue
        source = notebook_literal[sid]
        target = migrated[sid]
        for field_name in sorted(source):
            if field_name not in target:
                differences.append(f"{sid}.{field_name}: dropped by migration")
            elif target[field_name] != source[field_name]:
                differences.append(
                    f"{sid}.{field_name}: {source[field_name]!r} -> {target[field_name]!r}"
                )
    return differences


def assert_migration_unchanged(
    notebook_literal: Mapping[str, Mapping[str, object]],
    migrated: Mapping[str, Mapping[str, object]],
) -> None:
    """R-48's assertion: the migration moved values WITHOUT changing them.

    The freeze (D-1) prevents an intentional change; this diff catches the accidental
    one — a transposed digit in a hand migration of three coordinate pairs is the
    likelier failure, and only a comparison catches it.

    Raises
    ------
    RegistryError
        listing every difference, when any value changed in the move.
    """
    differences = migration_diff(notebook_literal, migrated)
    if differences:
        raise RegistryError(
            "station-coordinate migration",
            "the migration changed value(s) against the frozen notebook literal: "
            + "; ".join(differences)
            + " — the diff enforces the freeze-first rule's stated purpose (R-48, Q9=D)",
        )
