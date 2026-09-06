"""The §12-mandated station-registry test: every refusal in W-2…W-4, negative-controlled.

PURPOSE. `team.md` § Testing Posture makes a negative control mandatory for every hard
rule — a test that proves the violation is CAUGHT, not only that the happy path works.
This module carries: the Q2 = A runtime refusals (stations / cell rule / IGRF stay
`TBD — freeze gate` until the ONE pre-G-P1A freeze event); R-45's missing-field and
defaulted-IGRF raises (an ABSENT version fails, it never falls back); R-46's
presence-is-not-provenance raises and the per-consumer sufficiency mechanism; R-47's
named-source conflict equality including the three-source case an existence check would
pass AND the pinned coincidence residual; and R-48's migration diff (a transposed digit
fails).

FIXTURE DISCIPLINE. Every value below is SYNTHETIC (station ids `SYNA`/`SYNB`, made-up
coordinates): no real station coordinate, cell index or IGRF version appears here,
because those are §18.2 forbidden-choice values awaiting the freeze event (TE 18.2) and
no test may fill one. No fixture touches `evidence/` or December content.

RE-RUN BEHAVIOUR. Pure in-memory fixtures plus `tmp_path`; no network, no writes
outside `tmp_path`.

Run: pytest tests/test_station_registry.py -rs
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest
from src.data.config import TBD_SENTINEL, ConfigSnapshot, RegistryError
from src.data.registry import (
    CELL_RULE_ID,
    SECTION_6_2_FIELDS,
    ConflictResolution,
    Station,
    assert_migration_unchanged,
    assert_provenance_sufficient,
    assert_registry_resolved,
    assert_resolution,
    load_registry,
    migration_diff,
)

_YEAR_INTERVAL = [["2022-01-01", "2022-12-31", "SYN-EQUIP-1"]]


def _snapshot(tmp_path: Path, data: dict) -> ConfigSnapshot:
    return ConfigSnapshot(
        data=data,
        features={},
        experiment={},
        seeds={"development": 1},
        hashes={},
        snapshot_dir=tmp_path,
        resolved_roots={"workspace": tmp_path, "artifacts": tmp_path / "artifacts"},
        platform="local",
    )


def _station_entry(**overrides: object) -> dict:
    entry: dict = {
        "lat": 10.25,
        "lon": 20.75,
        "ellipsoidal_height_m": 100.0,
        "domes": "00000S000",
        "receiver_intervals": _YEAR_INTERVAL,
        "antenna_intervals": _YEAR_INTERVAL,
        "firmware_intervals": _YEAR_INTERVAL,
        "sampling_interval_s": 30,
        "observable_codes": ["C1C"],
        "hardware_changes_2022": [],
        "provenance": {name: "synthetic-fixture" for name in SECTION_6_2_FIELDS},
    }
    entry.update(overrides)
    return entry


def _frozen_data(tmp_path_unused: object = None, **station_overrides: object) -> dict:
    return {
        "stations": {"SYNA": _station_entry(**station_overrides)},
        "cell_rule": CELL_RULE_ID,
        "igrf_version": "SYN-PIN-1",
    }


def _station(**overrides: object) -> Station:
    values: dict = {
        "station_id": "SYNA",
        "lat": 10.25,
        "lon": 20.75,
        "ellipsoidal_height_m": 100.0,
        "domes": "00000S000",
        "receiver_intervals": ((dt.date(2022, 1, 1), dt.date(2022, 12, 31), "R"),),
        "antenna_intervals": ((dt.date(2022, 1, 1), dt.date(2022, 12, 31), "A"),),
        "firmware_intervals": ((dt.date(2022, 1, 1), dt.date(2022, 12, 31), "F"),),
        "sampling_interval_s": 30,
        "observable_codes": ("C1C",),
        "hardware_changes_2022": (),
        "igrf_version": "SYN-PIN-1",
        "cell": (10, 20),
        "provenance": {name: "synthetic-fixture" for name in SECTION_6_2_FIELDS},
    }
    values.update(overrides)
    return Station(**values)


# --- Q2 = A: the runtime refusals while the freeze-gate sentinels stand ------------------


def test_load_registry_refuses_while_stations_are_tbd(tmp_path: Path) -> None:
    snapshot = _snapshot(tmp_path, {"stations": TBD_SENTINEL, "cell_rule": TBD_SENTINEL})
    with pytest.raises(RegistryError) as excinfo:
        load_registry(snapshot)
    assert "TBD" in str(excinfo.value) and "freeze" in str(excinfo.value)


def test_load_registry_refuses_unresolved_cell_rule(tmp_path: Path) -> None:
    data = _frozen_data()
    data["cell_rule"] = TBD_SENTINEL
    with pytest.raises(RegistryError) as excinfo:
        load_registry(_snapshot(tmp_path, data))
    assert "cell_rule" in str(excinfo.value)


def test_load_registry_refuses_unknown_cell_rule_identifier(tmp_path: Path) -> None:
    data = _frozen_data()
    data["cell_rule"] = "some-other-rule"
    with pytest.raises(RegistryError):
        load_registry(_snapshot(tmp_path, data))


def test_absent_igrf_version_fails_and_never_falls_back(tmp_path: Path) -> None:
    """R-45: an ABSENT version fails exactly as a defaulted one — no fallback exists."""
    data = _frozen_data()
    del data["igrf_version"]
    with pytest.raises(RegistryError) as excinfo:
        load_registry(_snapshot(tmp_path, data))
    assert "igrf_version" in str(excinfo.value)
    assert "never falls back" in str(excinfo.value)


def test_tbd_igrf_version_refused(tmp_path: Path) -> None:
    data = _frozen_data()
    data["igrf_version"] = TBD_SENTINEL
    with pytest.raises(RegistryError):
        load_registry(_snapshot(tmp_path, data))


# --- The frozen-values path (synthetic transcription), D-1's rule shape ------------------


def test_load_registry_builds_from_a_complete_synthetic_transcription(tmp_path: Path) -> None:
    registry = load_registry(_snapshot(tmp_path, _frozen_data()))
    station = registry["SYNA"]
    assert station.cell == (10, 20)
    assert station.igrf_version == "SYN-PIN-1"
    assert station.provenance["lat"] == "synthetic-fixture"


def test_boundary_station_belongs_to_the_higher_indexed_cell(tmp_path: Path) -> None:
    """D-1: half-open [floor, floor+1) on both axes — a boundary station goes up."""
    data = _frozen_data(lat=11.0, lon=21.0)
    registry = load_registry(_snapshot(tmp_path, data))
    assert registry["SYNA"].cell == (11, 21)


def test_no_station_is_counted_twice_across_the_boundary(tmp_path: Path) -> None:
    data = _frozen_data()
    data["stations"]["SYNB"] = _station_entry(lat=10.999, lon=20.999)
    registry = load_registry(_snapshot(tmp_path, data))
    assert registry["SYNA"].cell == (10, 20)
    assert registry["SYNB"].cell == (10, 20)
    data["stations"]["SYNB"]["lat"] = 11.0
    registry = load_registry(_snapshot(tmp_path, data))
    assert registry["SYNB"].cell == (11, 20)


def test_transcribed_cell_disagreeing_with_the_rule_is_refused(tmp_path: Path) -> None:
    data = _frozen_data(cell=[11, 20])  # rule says (10, 20)
    with pytest.raises(RegistryError) as excinfo:
        load_registry(_snapshot(tmp_path, data))
    assert "disagrees" in str(excinfo.value)


def test_missing_6_2_field_is_refused_at_load(tmp_path: Path) -> None:
    data = _frozen_data(domes="")
    with pytest.raises(RegistryError) as excinfo:
        load_registry(_snapshot(tmp_path, data))
    assert "domes" in str(excinfo.value)


# --- R-45 / R-46: assert_registry_resolved -----------------------------------------------


def test_resolved_registry_passes() -> None:
    assert_registry_resolved({"SYNA": _station()})


def test_empty_registry_is_unresolved() -> None:
    with pytest.raises(RegistryError):
        assert_registry_resolved({})


def test_missing_6_2_field_raises() -> None:
    with pytest.raises(RegistryError) as excinfo:
        assert_registry_resolved({"SYNA": _station(observable_codes=())})
    assert "observable_codes" in str(excinfo.value)


def test_intervals_not_covering_2022_raise() -> None:
    short = ((dt.date(2022, 3, 1), dt.date(2022, 12, 31), "R"),)
    with pytest.raises(RegistryError) as excinfo:
        assert_registry_resolved({"SYNA": _station(receiver_intervals=short)})
    assert "cover" in str(excinfo.value)


def test_defaulted_igrf_version_raises() -> None:
    """R-45's negative control: a DEFAULT is refused exactly as an absence is."""
    with pytest.raises(RegistryError) as excinfo:
        assert_registry_resolved({"SYNA": _station(igrf_version="library default")})
    assert "DEFAULT" in str(excinfo.value)


def test_empty_igrf_version_raises() -> None:
    with pytest.raises(RegistryError):
        assert_registry_resolved({"SYNA": _station(igrf_version="")})


def test_omitted_provenance_raises() -> None:
    """R-46: presence is not provenance — omitting the provenance value entirely raises."""
    with pytest.raises(RegistryError) as excinfo:
        assert_registry_resolved({"SYNA": _station(provenance={})})
    assert "provenance" in str(excinfo.value)


def test_station_registry_raise_names_the_station_as_resource() -> None:
    """SD-I-03: the two registries sharing RegistryError are discriminated by resource."""
    with pytest.raises(RegistryError) as excinfo:
        assert_registry_resolved({"SYNA": _station(provenance={})})
    assert excinfo.value.resource == "SYNA"


def test_provenance_sufficiency_is_per_consumer() -> None:
    """R-46's chosen reading: a consumer requiring site-log provenance raises on a
    network-page value; a consumer that does not require it proceeds."""
    station = _station(
        provenance={
            **{name: "synthetic-fixture" for name in SECTION_6_2_FIELDS},
            "lat": "igs-network-page",
            "lon": "igs-network-page",
        }
    )
    registry = {"SYNA": station}
    with pytest.raises(RegistryError) as excinfo:
        assert_provenance_sufficient(registry, {"lat": "igs-site-log"})
    assert "site-log" in str(excinfo.value)
    assert_provenance_sufficient(registry, {})  # no requirement -> proceeds


# --- R-47: the conflict register's named-source equality ---------------------------------


def _resolution(**overrides: object) -> ConflictResolution:
    values: dict = {
        "station_id": "SYNA",
        "field": "lat",
        "source_values": {"source_a": 10.25, "source_b": 10.27},
        "named_source": "source_a",
        "resolved_value": 10.25,
        "rationale": "source_a is the synthetic higher-ranked source in this fixture",
    }
    values.update(overrides)
    return ConflictResolution(**values)


def test_legitimate_resolution_passes() -> None:
    assert_resolution(_resolution())


def test_two_source_average_is_rejected() -> None:
    with pytest.raises(RegistryError) as excinfo:
        assert_resolution(_resolution(resolved_value=10.26))  # (10.25 + 10.27) / 2
    assert "NAMES" in str(excinfo.value)


def test_three_source_average_equal_to_a_non_named_source_is_rejected() -> None:
    """The case an existence check would PASS: sources {0, 3, 6} average to the
    recorded 3, but the named source's value is 0 — the named-source equality rejects."""
    with pytest.raises(RegistryError):
        assert_resolution(
            _resolution(
                source_values={"source_a": 0.0, "source_b": 3.0, "source_c": 6.0},
                named_source="source_a",
                resolved_value=3.0,  # mean of {0, 3, 6}; equals source_b, not source_a
            )
        )


def test_coincidence_case_passes_and_is_pinned_as_the_stated_residual() -> None:
    """R-47's residual, PINNED rather than discovered: when the mean coincides with the
    NAMED source's own value, no check on the value can distinguish it from a
    legitimate resolution — the check passes, and this test asserts that it does."""
    assert_resolution(
        _resolution(
            source_values={"source_a": 0.0, "source_b": 3.0, "source_c": 6.0},
            named_source="source_b",
            resolved_value=3.0,  # the mean AND the named source's value, bit for bit
        )
    )


def test_value_matching_no_recorded_source_is_rejected() -> None:
    with pytest.raises(RegistryError):
        assert_resolution(_resolution(resolved_value=99.9))


def test_empty_rationale_is_rejected() -> None:
    with pytest.raises(RegistryError) as excinfo:
        assert_resolution(_resolution(rationale="   "))
    assert "rationale" in str(excinfo.value)


def test_naming_an_unrecorded_source_is_rejected() -> None:
    with pytest.raises(RegistryError):
        assert_resolution(_resolution(named_source="source_z"))


# --- R-48: the migration diff ------------------------------------------------------------


def test_unchanged_migration_passes_with_empty_diff() -> None:
    literal = {"SYNA": {"lat": 10.25, "lon": 20.75}}
    assert migration_diff(literal, {"SYNA": {"lat": 10.25, "lon": 20.75}}) == []
    assert_migration_unchanged(literal, {"SYNA": {"lat": 10.25, "lon": 20.75}})


def test_transposed_digit_fails_the_migration_diff() -> None:
    """R-48: the freeze prevents an intentional change; the diff catches the accidental
    transposed digit — the likelier failure in a hand migration."""
    literal = {"SYNA": {"lat": 10.25, "lon": 20.75}}
    with pytest.raises(RegistryError) as excinfo:
        assert_migration_unchanged(literal, {"SYNA": {"lat": 10.52, "lon": 20.75}})
    assert "10.52" in str(excinfo.value)


def test_dropped_station_fails_the_migration_diff() -> None:
    literal = {"SYNA": {"lat": 10.25}, "SYNB": {"lat": 11.25}}
    with pytest.raises(RegistryError):
        assert_migration_unchanged(literal, {"SYNA": {"lat": 10.25}})
