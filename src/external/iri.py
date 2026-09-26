"""IRI-2016 benchmark gate: validated before generation, blocked on failure (W-6, R-59).

Purpose
-------
The benchmark half of unit `external-products` (SD-E-04; FR-P1-04-15). `generate_benchmark`
is the attempt/refusal contract: it refuses at limb 1 on every invocation without a
passing pre-declared validation report and never generates in injection mode. Since
2026-09-19 (owner's final-preparation instruction; D-45 as annotated) the module also
carries the GATED production path -- `read_benchmark_contract`, `verify_runtime`,
`build_validation_report`, `run_gated_generation` -- reached only from the stage
script's `--generate-benchmark` with governed inputs, after the full index-file pins
are verified and all four limbs pass. B-01 is labelled GENERATED, NOT TRAINED in the
model/config inventory -- never fitted.

Import boundary: this module is importable ONLY by
`scripts/04_build_external_products.py` and modules under `src/evaluation/` (TE 12;
TA-07; project.md Forbidden). Nothing it produces may reach training or inference; IRI
joins only at evaluation time onto the frozen comparison-wide mask (NFR-IRI-01).
`tests/test_iri_denial.py` asserts the boundary with an `ast` scan and never imports
this module; behaviour is exercised through the allowlisted stage script.

The four limbs (R-59), three of them ordering or content checks rather than presence
checks:

1. generation refuses without a PASSING report (`BenchmarkError` naming the report and
   the missing pass);
2. the tolerance's recorded timestamp PRECEDES the comparison -- the only evidence
   class separating *declared before* from *fitted after*;
3. the report's seven content areas are asserted FIELD BY FIELD, never by presence of
   a report;
4. the benchmark's own drivers appear as rows in the same frozen availability matrix
   used for ML features (the matrix is `features-and-splits`' artifact; this module
   states the obligation and does not own the row). Where a provider supplies no
   publication timestamp, the row admits the approved conservative convention plus the
   documented absence and an unverified-latency statement -- for F10.7 that convention
   is **D-25**, whose authorising TE 15.2 amendment was **GRANTED AND APPLIED
   2026-08-22** (`CR-2026-08-22-EV-12`: TE EV-12 row and section 7.0A stage 4). The
   earlier wording here ("requests, but does not take ... UNMET at G-04") described the
   pre-grant state and was corrected 2026-09-19 (P-5, `CR-2026-09-19-SCI-DECISIONS`);
   the grant's scope is exactly the EV-12 row shape and no wider -- it does not certify
   any lag, producer or G-04 outcome.

On validation failure the implementation is NEVER silently switched (R-59): a switch
made because the first implementation failed validation is a scientific change wearing
an operational disguise (TE 18.2).

The `iricore` import lives INSIDE the gated generation path only: the package is TE 8.1
required but is not installed in this environment, the network is blocked, and
generation is blocked regardless -- so the import is unreachable until the gates pass on
governed evidence.

Inputs
------
A validation-report mapping, an availability-matrix row sequence, and the benchmark's
declared driver ids -- all supplied by the orchestrating stage script. This module reads
no file and no config directly.

Re-run behaviour
----------------
Pure checks over arguments; no writes, no network, no state. Re-running a refusal
reproduces the same refusal. The 26,000-call workload timing obligation (TC-04) is
recorded in the gated path and cannot execute until generation is authorised by a
passing governed validation.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from src.data.config import BenchmarkError
from src.data.splits import Partition, PartitionKind, validation_month_range

__all__ = [
    "REPORT_CONTENT_AREAS",
    "assert_validation_report",
    "assert_benchmark_drivers_in_matrix",
    "evaluate_generation_gates",
    "generate_benchmark",
    "BENCHMARK_DRIVER_IDS",
    "BenchmarkContract",
    "read_benchmark_contract",
    "verify_runtime",
    "assert_index_unchanged",
    "build_target_grid",
    "evaluate_points",
    "benchmark_driver_rows",
    "build_validation_report",
    "run_gated_generation",
    "predictions_from_benchmark_rows",
]

#: FR-P1-04-15's seven content areas, asserted field by field (R-59 limb 3). The keys
#: are this unit's report schema; the VALUES asserted against them (the 2000 km
#: ceiling, the 5-10 sample range) are the requirement's own enumerated criteria,
#: quoted -- not values chosen here.
REPORT_CONTENT_AREAS: tuple[str, ...] = (
    "package_version",  # 1: the pinned package/build with exact version or commit
    "model_switches",  # 2: all model switches and the topside option
    "topside_option",
    "altitude_ceiling_km",  # 3: stated explicitly as 2000 km
    "units",  # 4: units and output extraction
    "output_extraction",
    "driver_inputs",  # 5: coordinate/time/solar/geomagnetic inputs + confirmations
    "samples",  # 6: 5-10 samples against the official IRI interface
    "tolerance",  # 7: predeclared, with its timestamp
)

#: The altitude ceiling FR-P1-04-15 requires the report to state explicitly, quoted
#: from the requirement's criterion (a validation expectation, not a chosen value).
_REQUIRED_CEILING_KM = 2000

#: The sample-count range FR-P1-04-15 fixes ("five to ten samples").
_SAMPLE_RANGE = (5, 10)


def _parse_utc(value: Any, *, resource: str, field: str) -> dt.datetime:
    text = str(value)
    if text.endswith("Z"):  # the `Z` suffix parses only from Python 3.11; 3.10 needs +00:00
        text = text[:-1] + "+00:00"
    try:
        parsed = dt.datetime.fromisoformat(text)
    except (TypeError, ValueError) as exc:
        raise BenchmarkError(
            resource,
            f"{field} is not an ISO-8601 timestamp ({value!r}); an ordering check "
            f"over an unparseable timestamp proves nothing (R-59 limb 2)",
        ) from exc
    if parsed.tzinfo is None:
        raise BenchmarkError(
            resource,
            f"{field} carries no timezone ({value!r}); a naive timestamp cannot "
            f"evidence ordering across sessions",
        )
    return parsed


def assert_validation_report(report: Mapping[str, Any], *, report_name: str) -> None:
    """R-59 limbs 1-3: passing status, seven content areas field by field, and the
    predeclared-tolerance ordering.

    Raises
    ------
    BenchmarkError
        naming the report and the first violated expectation: a non-`passed` status; a
        missing content area; a ceiling not stated as 2000 km; driver inputs that omit
        the D-45 retrospective-centered-index disclosure, still claim
        `no_future_centering_confirmed`, or omit the pinned index/version/override
        fields; a sample
        set outside 5-10 or not spanning sites, day and night, quiet and disturbed, or
        not validated against the official IRI interface; a tolerance without a frozen
        value; or a tolerance timestamp that does not PRECEDE the comparison.
    """
    missing = sorted(area for area in REPORT_CONTENT_AREAS if area not in report)
    if missing:
        raise BenchmarkError(
            report_name,
            f"validation report is missing content area(s) {missing}; FR-P1-04-15 "
            f"enumerates seven areas and each is asserted field by field -- a report "
            f"missing the ceiling or the driver-availability confirmation must not "
            f"pass on presence (R-59 limb 3)",
        )
    if str(report.get("status", "")).lower() != "passed":
        raise BenchmarkError(
            report_name,
            f"validation report status is {report.get('status')!r}, not 'passed'; a "
            f"validation failure BLOCKS benchmark generation rather than warning "
            f"(FR-P1-04-15), and the implementation is never silently switched on "
            f"failure (R-59)",
        )
    ceiling = report["altitude_ceiling_km"]
    if not isinstance(ceiling, int | float) or float(ceiling) != float(_REQUIRED_CEILING_KM):
        raise BenchmarkError(
            report_name,
            f"altitude_ceiling_km is {ceiling!r}; FR-P1-04-15 requires the ceiling "
            f"stated explicitly as {_REQUIRED_CEILING_KM} km (R-59 limb 3)",
        )
    drivers = report["driver_inputs"]
    if not isinstance(drivers, Mapping):
        raise BenchmarkError(
            report_name,
            f"driver_inputs is {type(drivers).__name__}, not a mapping of the "
            f"coordinate, time, solar and geomagnetic inputs",
        )
    # D-45 (student selection recorded 2026-09-19; supervisor approval REPORTED by the
    # student 2026-09-19, countersignature artifact PENDING --
    # governance/COUNTERSIGNATURE_REQUEST_2026-09-19.md -- applied here on the recorded
    # decision owner's explicit authorisation to apply this patch; it does not itself
    # pass G-04 or certify the IRI role closed). IRI-2016 is run with its standard
    # index files, whose inputs are retrospective and centered by construction. The
    # report therefore RECORDS and DISCLOSES that fact instead of confirming its
    # absence; a report that still claims "not future-centered" for a standard-index
    # run is refused as a false confirmation.
    if drivers.get("index_inputs_retrospective_centered") is not True:
        raise BenchmarkError(
            report_name,
            "driver_inputs.index_inputs_retrospective_centered is not True; under D-45 the "
            "benchmark is a retrospective climatological reference whose index inputs "
            "(adjusted target-day F10.7, centered 81-/365-day means, centered IG12/Rz12, "
            "target-day ap) are recorded and disclosed, never confirmed absent "
            "(Vision 6.11 as amended; FR-P1-04-15 area 5)",
        )
    if drivers.get("no_future_centering_confirmed") is True:
        raise BenchmarkError(
            report_name,
            "driver_inputs.no_future_centering_confirmed is True for a standard-index IRI "
            "run; that confirmation is false by construction (D-45)",
        )
    for field in ("index_files_sha256", "iri_version", "oarr_overrides"):
        if field not in drivers:
            raise BenchmarkError(
                report_name,
                f"driver_inputs.{field} is absent; D-45 pins the shipped index files by hash, "
                f"requires version=16 and records that no oarr override is used",
            )
    if drivers.get("iri_version") != 16 or drivers.get("oarr_overrides") not in ({}, [], None):
        raise BenchmarkError(
            report_name, "D-45 requires IRI-2016 (version=16) and no oarr overrides"
        )
    samples = report["samples"]
    if not isinstance(samples, Sequence) or isinstance(samples, str):
        raise BenchmarkError(report_name, "samples is not a sequence of sample records")
    low, high = _SAMPLE_RANGE
    if not (low <= len(samples) <= high):
        raise BenchmarkError(
            report_name,
            f"report carries {len(samples)} sample(s); FR-P1-04-15 requires five to "
            f"ten, spanning sites, day and night, quiet and disturbed",
        )
    sites = {str(sample.get("site", "")) for sample in samples}
    day_night = {str(sample.get("local_time_class", "")).lower() for sample in samples}
    activity = {str(sample.get("activity_class", "")).lower() for sample in samples}
    if len(sites - {""}) < 2:
        raise BenchmarkError(
            report_name, "samples do not span at least two sites (FR-P1-04-15 area 6)"
        )
    if not {"day", "night"} <= day_night:
        raise BenchmarkError(
            report_name, "samples do not span both day and night (FR-P1-04-15 area 6)"
        )
    if not {"quiet", "disturbed"} <= activity:
        raise BenchmarkError(
            report_name, "samples do not span both quiet and disturbed (FR-P1-04-15 area 6)"
        )
    unvalidated = [
        index for index, sample in enumerate(samples) if "official_interface_value" not in sample
    ]
    if unvalidated:
        raise BenchmarkError(
            report_name,
            f"sample(s) {unvalidated} carry no official_interface_value; every sample "
            f"is validated against the OFFICIAL IRI interface (FR-P1-04-15 area 6)",
        )
    tolerance = report["tolerance"]
    if not isinstance(tolerance, Mapping) or "value" not in tolerance:
        raise BenchmarkError(
            report_name,
            "tolerance carries no frozen value; a tolerance without a value cannot "
            "have been predeclared (FR-P1-04-15 area 7)",
        )
    declared_at = _parse_utc(
        tolerance.get("declared_at_utc"), resource=report_name, field="tolerance.declared_at_utc"
    )
    comparison_at = _parse_utc(
        report.get("comparison_ran_at_utc"),
        resource=report_name,
        field="comparison_ran_at_utc",
    )
    if declared_at >= comparison_at:
        raise BenchmarkError(
            report_name,
            f"tolerance declared_at_utc ({declared_at.isoformat()}) does not PRECEDE "
            f"the comparison ({comparison_at.isoformat()}); 'a passing report exists' "
            f"is satisfiable by a tolerance chosen AFTER the comparison ran, which is "
            f"the failure the predeclared clause exists to prevent (R-59 limb 2) -- a "
            f"frozen value plus an ordering is the only evidence class separating "
            f"'declared before' from 'fitted after'",
        )


def assert_benchmark_drivers_in_matrix(
    availability_matrix: Sequence[Mapping[str, Any]],
    *,
    benchmark_drivers: Sequence[str],
    report_name: str,
) -> None:
    """R-59 limb 4: the benchmark's own drivers appear as rows in the SAME frozen
    availability matrix used for ML features -- each carrying an observation timestamp,
    a publication timestamp OR (where the provider supplies none) the approved
    conservative convention plus the documented absence and an unverified-latency
    statement, a release status and a safe lag.

    *A benchmark fed better-timed drivers than the model gets is not a benchmark* --
    this is the one limb whose violation would FLATTER the model rather than break the
    run. The matrix is `features-and-splits`' artifact: this function states the
    obligation against rows it is handed; it does not own or build the row.

    D-25 standing (SD-E-04): the F10.7 convention this limb admits rests on the TE 15.2
    amendment granted and applied 2026-08-22 (`CR-2026-08-22-EV-12`); the pre-grant
    wording was corrected 2026-09-19 (P-5). The row shape is the whole of the grant.

    Raises
    ------
    BenchmarkError
        naming each benchmark driver with no matrix row, and each row missing its
        required evidence fields.
    """
    rows_by_driver = {str(row.get("driver_id", "")): row for row in availability_matrix}
    absent = sorted(set(benchmark_drivers) - set(rows_by_driver))
    if absent:
        raise BenchmarkError(
            report_name,
            f"benchmark driver(s) {absent} have no row in the frozen availability "
            f"matrix used for ML features; a benchmark fed better-timed drivers than "
            f"the model gets is not a benchmark (R-59 limb 4, FR-P1-04-15)",
        )
    for driver_id in benchmark_drivers:
        row = rows_by_driver[str(driver_id)]
        problems: list[str] = []
        if not str(row.get("observation_timestamp", "") or ""):
            problems.append("observation_timestamp")
        has_publication = bool(str(row.get("publication_timestamp", "") or ""))
        has_convention = (
            bool(str(row.get("conservative_convention", "") or ""))
            and bool(str(row.get("documented_absence", "") or ""))
            and bool(str(row.get("unverified_latency_statement", "") or ""))
        )
        if not (has_publication or has_convention):
            problems.append(
                "publication_timestamp OR (conservative_convention + "
                "documented_absence + unverified_latency_statement)"
            )
        if not str(row.get("release_status", "") or ""):
            problems.append("release_status")
        if not str(row.get("safe_lag", "") or ""):
            problems.append("safe_lag")
        if problems:
            raise BenchmarkError(
                report_name,
                f"availability-matrix row for benchmark driver {driver_id!r} is "
                f"missing {problems}; the CR-2026-08-22-EV-12 row shape admits a "
                f"documented absence only WITH the convention and the "
                f"unverified-latency statement (R-59 limb 4; for F10.7 the convention "
                f"is D-25, whose authorising TE 15.2 amendment was granted and applied "
                f"2026-08-22 under CR-2026-08-22-EV-12 -- the row shape is the whole "
                f"of that grant)",
            )


def evaluate_generation_gates(
    *,
    validation_report: Mapping[str, Any] | None,
    report_name: str,
    availability_matrix: Sequence[Mapping[str, Any]] | None,
    benchmark_drivers: Sequence[str],
) -> None:
    """All four R-59 limbs, in order; the first violated limb raises.

    Raises
    ------
    BenchmarkError
        limb 1 when no report exists; limbs 2-3 via `assert_validation_report`;
        limb 4 via `assert_benchmark_drivers_in_matrix`.
    """
    if validation_report is None:
        raise BenchmarkError(
            report_name,
            "no passing pre-declared validation report exists: the R-59 validation "
            "has not been run, so IRI benchmark generation is REFUSED -- a validation "
            "failure (or absence) blocks generation rather than warning "
            "(FR-P1-04-15), and the implementation is never silently switched "
            "(R-59). This refusal is the deliverable while the gate is unattempted",
        )
    assert_validation_report(validation_report, report_name=report_name)
    if availability_matrix is None:
        raise BenchmarkError(
            report_name,
            "no frozen availability matrix was supplied; the benchmark's own drivers "
            "must appear as rows in the same matrix used for ML features (R-59 "
            "limb 4) -- the matrix is features-and-splits' artifact, and its absence "
            "refuses generation rather than being waived",
        )
    assert_benchmark_drivers_in_matrix(
        availability_matrix, benchmark_drivers=benchmark_drivers, report_name=report_name
    )


def generate_benchmark(
    *,
    validation_report: Mapping[str, Any] | None,
    report_name: str,
    availability_matrix: Sequence[Mapping[str, Any]] | None,
    benchmark_drivers: Sequence[str],
    injection_mode: bool = False,
) -> None:
    """Attempt IRI benchmark generation. TODAY THIS ALWAYS REFUSES.

    Every real invocation refuses at limb 1 (no governed validation report exists).
    `injection_mode=True` marks a negative-control attempt driven by injected state:
    the gates are evaluated exactly as for a real attempt, and if the injected state
    satisfies them the attempt STILL refuses -- injected state is not governed
    evidence, and proving the gates reject violations must never itself generate a
    benchmark (WS-10's injection pattern: the test passes by proving the denial
    fires).

    Raises
    ------
    BenchmarkError
        always, today: either from the violated gate (naming it), or -- when injected
        state satisfies every gate -- from the injection-mode terminal refusal.
    """
    evaluate_generation_gates(
        validation_report=validation_report,
        report_name=report_name,
        availability_matrix=availability_matrix,
        benchmark_drivers=benchmark_drivers,
    )
    if injection_mode:
        raise BenchmarkError(
            report_name,
            "injection-mode gate evaluation complete: every gate passed on the "
            "INJECTED state, and generation is refused anyway -- injected state is "
            "not governed evidence, and no benchmark is generated by this unit "
            "(the refusals are the deliverable)",
        )
    # The gated generation path. Unreachable today: limb 1 refuses on every real
    # invocation because the R-59 validation has not run. The `iricore` import lives
    # HERE, inside the gated path, by design (TE 8.1 requires the package; it is not
    # installed in this environment and the network is blocked, so the import must
    # never execute outside a governed, gate-passing run). The 26,000-call workload is
    # timed and its measured runtime recorded, and the iri2016 Fortran build
    # re-establishes from pins on a cold session (TC-04) -- obligations recorded here,
    # dischargeable only inside that governed run.
    import iricore  # noqa: F401  -- deferred inside the gated path (R-59; TE 8.1)

    raise BenchmarkError(
        report_name,
        "gated generation path reached with governed evidence; generation itself is "
        "performed by `run_gated_generation` from the stage script's --generate-benchmark "
        "path (pins verified before and after the session), never by this attempt "
        "contract -- reaching this line indicates the attempt path was used for production",
    )


# =====================================================================================
# Execution contract, runtime pin protection, target grid, validation-report builder and
# the gated workload (added 2026-09-19 under the owner's "final preparation" instruction;
# D-45 as annotated 2026-09-19). Everything below reads its scientific values from
# `configs/experiment.yaml: benchmark_b01` through the one config loader -- nothing is
# hidden in source (TC-03e). The `iricore` import still lives only inside the paths a
# passing gate (or an explicit runtime verification) reaches.
# =====================================================================================

#: Driver ids of the benchmark's OWN inputs -- the IRI index rows, recorded in the
#: availability matrix as hindcast-only grade rows (D-45 item 4; R-59 limb 4).
BENCHMARK_DRIVER_IDS: tuple[str, ...] = (
    "iri_apf107_f107_adjusted",
    "iri_apf107_ap_3h",
    "iri_ig_rz_ig12_rz12",
)


@dataclass(frozen=True)
class BenchmarkContract:
    """`benchmark_b01`, read once per run. Field names mirror the config block."""

    benchmark_id: str
    iri_version: int
    htop_km: float
    hbot_km: float
    hstep_km: float
    oarr_overrides: Mapping[str, Any]
    output_field: str
    output_units: str
    index_semantics: str
    package: str
    release: str
    wheel_sha256: str
    installed_default_iri_version: int
    index_file_pins: Mapping[str, str]
    year: int
    cadence_hours: int
    stamps: Mapping[str, str]
    report_name: str
    tolerance_tecu: object
    tolerance_declared_at_utc: object


def _is_tbd(value: object) -> bool:
    return isinstance(value, str) and value.strip().upper().startswith("TBD")


def read_benchmark_contract(snapshot: Any) -> BenchmarkContract:
    """Read `experiment.benchmark_b01`; refuse a block that is absent, malformed, or whose
    ceiling is not the required 2000 km. The tolerance may be TBD here (it is checked
    where it is used: the report builder), so the driver-audit path is never blocked by
    an unrelated freeze."""
    block = snapshot.experiment.get("benchmark_b01")
    resource = "experiment.benchmark_b01"
    if not isinstance(block, Mapping):
        raise BenchmarkError(
            resource,
            "block is absent; the B-01 execution contract (D-45) is read from configuration, never assumed",
        )
    try:
        integ = block["integration"]
        rt = block["runtime"]
        vr = block["validation_report"]
        contract = BenchmarkContract(
            benchmark_id=str(block["benchmark_id"]),
            iri_version=int(block["iri_version"]),
            htop_km=float(integ["htop_km"]),
            hbot_km=float(integ["hbot_km"]),
            hstep_km=float(integ["hstep_km"]),
            oarr_overrides=dict(block.get("oarr_overrides") or {}),
            output_field=str(block["output_field"]),
            output_units=str(block["output_units"]),
            index_semantics=str(block["index_semantics"]),
            package=str(rt["package"]),
            release=str(rt["release"]),
            wheel_sha256=str(rt["wheel_sha256"]),
            installed_default_iri_version=int(rt["installed_default_iri_version"]),
            index_file_pins={str(k): str(v) for k, v in dict(block["index_file_pins"]).items()},
            year=int(block["target_grid"]["year"]),
            cadence_hours=int(block["target_grid"]["cadence_hours"]),
            stamps={str(k): str(v) for k, v in dict(block["stamps"]).items()},
            report_name=str(vr["name"]),
            tolerance_tecu=vr.get("tolerance_tecu"),
            tolerance_declared_at_utc=vr.get("tolerance_declared_at_utc"),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise BenchmarkError(resource, f"malformed block: {exc!r}") from exc
    if contract.iri_version != 16:
        raise BenchmarkError(
            resource,
            f"iri_version is {contract.iri_version}; D-45 requires IRI-2016 (16), passed explicitly",
        )
    if contract.htop_km != float(_REQUIRED_CEILING_KM):
        raise BenchmarkError(
            resource,
            f"integration.htop_km is {contract.htop_km}; Vision 6.11 freezes the ceiling at {_REQUIRED_CEILING_KM} km",
        )
    if contract.oarr_overrides:
        raise BenchmarkError(
            resource, f"oarr_overrides is {contract.oarr_overrides!r}; D-45 item 1 admits none"
        )
    if set(contract.index_file_pins) != {"apf107.dat", "ig_rz.dat"}:
        raise BenchmarkError(
            resource,
            f"index_file_pins must pin exactly apf107.dat and ig_rz.dat, got {sorted(contract.index_file_pins)}",
        )
    for name, digest in contract.index_file_pins.items():
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise BenchmarkError(
                resource,
                f"index_file_pins[{name!r}] is not a full lowercase SHA-256 ({digest!r}); an abbreviated pin is not a pin",
            )
    return contract


def _sha256_path(path: Any) -> str:
    import hashlib

    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_runtime(contract: BenchmarkContract) -> dict[str, Any]:
    """Runtime pin protection, run BEFORE an execution session (D-45 item 1; annotation
    item 2): the installed package is the pinned release, its default IRI version is the
    recorded one (so the explicit `version=16` is guarding what it claims to), and the
    two index files ACTUALLY on the import path hash exactly to the full pins.

    Returns the runtime identity to be recorded with every output. Raises
    `BenchmarkError` naming the file and the expected/actual digest on any mismatch --
    the run never continues past a failed pin.
    """
    import importlib.metadata
    import platform as _plat
    import sys as _sys
    from pathlib import Path as _Path

    import iricore  # noqa: F401  -- reachable only through verification or a passing gate
    from iricore.config import DEFAULT_IRI_VERSION

    resource = f"{contract.package} runtime"
    try:
        installed = importlib.metadata.version(contract.package)
    except importlib.metadata.PackageNotFoundError as exc:
        raise BenchmarkError(
            resource, "package metadata not found; the pinned wheel is not what is installed"
        ) from exc
    if installed != contract.release:
        raise BenchmarkError(
            resource,
            f"installed release {installed!r} != pinned {contract.release!r}; the pin is on this exact wheel",
        )
    if int(DEFAULT_IRI_VERSION) != contract.installed_default_iri_version:
        raise BenchmarkError(
            resource,
            f"installed DEFAULT_IRI_VERSION is {DEFAULT_IRI_VERSION}, recorded {contract.installed_default_iri_version}; "
            f"a changed default changes what the explicit version=16 is guarding against",
        )
    index_dir = _Path(iricore.__file__).resolve().parent / "data" / "index"
    measured: dict[str, str] = {}
    for name, expected in contract.index_file_pins.items():
        path = index_dir / name
        if not path.is_file():
            raise BenchmarkError(
                str(path), "pinned index file is absent from the installed package"
            )
        actual = _sha256_path(path)
        measured[name] = actual
        if actual != expected:
            raise BenchmarkError(
                str(path),
                f"SHA-256 {actual} != D-45 pin {expected}; the file IRI would consume is not the frozen one "
                f"(iricore.update() run, or a different wheel) -- generation refused",
            )
    return {
        "package": contract.package,
        "release": installed,
        "installed_default_iri_version": int(DEFAULT_IRI_VERSION),
        "iri_version_requested": contract.iri_version,
        "index_dir": str(index_dir),
        "index_files_sha256": measured,
        "python": _sys.version.split()[0],
        "executable": _sys.executable,
        "platform": _plat.platform(),
    }


def assert_index_unchanged(
    identity: Mapping[str, Any], contract: BenchmarkContract
) -> dict[str, str]:
    """Re-hash the same two files AFTER a session's calls: an in-session replacement or
    update is refused, never silently carried into the outputs. One check per session,
    not per point (TC-04-scale workloads are not slowed by per-hour hashing)."""
    from pathlib import Path as _Path

    index_dir = _Path(str(identity["index_dir"]))
    after: dict[str, str] = {}
    for name, expected in contract.index_file_pins.items():
        after[name] = _sha256_path(index_dir / name)
        if after[name] != expected:
            raise BenchmarkError(
                str(index_dir / name),
                f"index file changed during the session: {expected} before, {after[name]} after; "
                f"outputs of this session are not attributable to the pinned inputs and are refused",
            )
    return after


def build_target_grid(
    stations: Mapping[str, Any],
    *,
    year: int,
    cadence_hours: int,
    months: Sequence[int] | None = None,
) -> list[dict[str, Any]]:
    """Every (station, hourly UTC target time) of `year`, optionally restricted to
    `months` (a restricted grid is a PARTIAL product and is labelled so by the caller).
    Coordinates come from the resolved station registry (data.yaml: stations, D-1);
    the cell is D-1's frozen floor rule. Timestamps are timezone-aware UTC."""
    import math as _math

    wanted = set(range(1, 13)) if months is None else {int(m) for m in months}
    bad = sorted(m for m in wanted if not 1 <= m <= 12)
    if bad:
        raise BenchmarkError("months", f"invalid month(s) {bad}")
    points: list[dict[str, Any]] = []
    for station_id in sorted(stations):
        st = stations[station_id]
        lat, lon = float(st.lat), float(st.lon)
        cell = (_math.floor(lat), _math.floor(lon))
        t = dt.datetime(year, 1, 1, tzinfo=dt.timezone.utc)
        end = dt.datetime(year + 1, 1, 1, tzinfo=dt.timezone.utc)
        step = dt.timedelta(hours=cadence_hours)
        while t < end:
            if t.month in wanted:
                points.append(
                    {
                        "station_id": station_id,
                        "lat": lat,
                        "lon": lon,
                        "cell_id": f"{cell[0]}/{cell[1]}",
                        "target_time_utc": t,
                    }
                )
            t += step
    return points


def _hmf2_at(contract: BenchmarkContract, when: dt.datetime, lat: float, lon: float) -> float:
    """The D-50 hmF2 DIAGNOSTIC: IRI-2016's F2-peak height (oarr[1], km) from one
    `iricore.iri` call under the same version, index files and default switches as
    `_vtec_at`. No threshold is attached to it and it never enters the tolerance test; it
    is recorded beside the official interface's own hmF2 so a wrong hmF2-model option on the
    official form (an effect of <= 0.45 TECU, below any per-case tolerance) is visible by
    inspection instead of absorbed (governance/proposed/B01_TOLERANCE_PROPOSAL_2026-09-19.md 3)."""
    import math as _math

    import iricore
    import numpy as _np

    if when.tzinfo is None or when.utcoffset() != dt.timedelta(0):
        raise BenchmarkError("target_time_utc", f"{when!r} is not a UTC-aware timestamp")
    naive = when.replace(tzinfo=None)
    out = iricore.iri(naive, [300.0, 300.0, 10.0], lat, lon, version=contract.iri_version)
    oarr = _np.asarray(out.oarr, dtype=float).reshape(-1)
    scalar = float(oarr[1])
    if not _math.isfinite(scalar) or scalar <= 0.0:
        raise BenchmarkError(
            "iricore.iri", f"hmF2 diagnostic {scalar!r} at {when.isoformat()} ({lat}, {lon})"
        )
    return scalar


def _vtec_at(contract: BenchmarkContract, when: dt.datetime, lat: float, lon: float) -> float:
    """One IRI-2016 call exactly as D-45 states it. `when` must be UTC-aware; iricore takes
    a naive datetime it treats as UT, so the tz is stripped only after the check."""
    import math as _math

    import iricore

    if when.tzinfo is None or when.utcoffset() != dt.timedelta(0):
        raise BenchmarkError("target_time_utc", f"{when!r} is not a UTC-aware timestamp")
    naive = when.replace(tzinfo=None)
    value = iricore.vtec(
        naive,
        lat,
        lon,
        hbot=contract.hbot_km,
        htop=contract.htop_km,
        hstep=contract.hstep_km,
        version=contract.iri_version,
    )
    scalar = float(value[0] if hasattr(value, "__len__") else value)
    if not _math.isfinite(scalar):
        raise BenchmarkError(
            "iricore.vtec", f"non-finite output {scalar!r} at {when.isoformat()} ({lat}, {lon})"
        )
    return scalar


def evaluate_points(
    points: Sequence[Mapping[str, Any]],
    contract: BenchmarkContract,
    *,
    progress: Any = None,
    progress_every: int = 500,
) -> list[dict[str, Any]]:
    """The workload: one row per point, stamped (TEC-05), value in TECU under
    `contract.output_field`. A per-point failure is a COMPLETENESS shortfall recorded on
    the row (`status: "error"`, value null, the exception text) -- never a silent skip and
    never an abort of the whole session (team.md two-tier posture); an integrity failure
    (a pin mismatch) is raised before this function is reached."""
    rows: list[dict[str, Any]] = []
    stamps = dict(contract.stamps)
    total = len(points)
    for i, p in enumerate(points, 1):
        row: dict[str, Any] = {
            **stamps,
            "benchmark_id": contract.benchmark_id,
            "station_id": p["station_id"],
            "cell_id": p["cell_id"],
            "lat": p["lat"],
            "lon": p["lon"],
            "target_time_utc": p["target_time_utc"].isoformat(),
            "units": contract.output_units,
            "iri_version": contract.iri_version,
            "htop_km": contract.htop_km,
        }
        try:
            row[contract.output_field] = _vtec_at(
                contract, p["target_time_utc"], p["lat"], p["lon"]
            )
            row["status"] = "ok"
        except Exception as exc:  # noqa: BLE001 -- recorded per row, by design
            row[contract.output_field] = None
            row["status"] = "error"
            row["error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
        if progress is not None and (i % progress_every == 0 or i == total):
            progress(i, total)
    return rows


def benchmark_driver_rows(
    identity: Mapping[str, Any], contract: BenchmarkContract
) -> list[dict[str, Any]]:
    """R-59 limb 4 rows for the benchmark's OWN drivers -- the pinned index files -- in
    the EV-12 row shape, graded hindcast-only (D-45 item 4). The index files carry no
    publication timestamp per value; the documented absence and the unverified-latency
    statement are recorded WITH the conservative convention (the file's own update date
    is the earliest instant at which every value in it can have existed)."""
    pins = dict(identity["index_files_sha256"])
    common = {
        "release_status": "hindcast-only (retrospective, centered, same-day index inputs; D-45 item 2)",
        "safe_lag": "not applicable: hindcast-only grade, never a forecast-safe row (D-45 item 4)",
        "publication_timestamp": "",
        "conservative_convention": "the shipped file's own update date bounds availability of every value it carries (apf107.dat last row 2024-03-06; ig_rz.dat header 2024-03-07); no per-value publication instant exists",
        "documented_absence": "the IRI index files record no per-value publication timestamp; none is claimed",
        "unverified_latency_statement": "the provider-side latency of each index value is unverified; the rows are hindcast-only and are never compared against the model's forecast-safe rows as if equivalent",
        "index_files_sha256": pins,
    }
    return [
        {
            "driver_id": "iri_apf107_f107_adjusted",
            "observation_timestamp": "target day, 20 UT adjusted reading; 81-/365-day means centered on the target day",
            **common,
        },
        {
            "driver_id": "iri_apf107_ap_3h",
            "observation_timestamp": "target day 3-hourly ap up to the target UT hour (and back to UT-39 h)",
            **common,
        },
        {
            "driver_id": "iri_ig_rz_ig12_rz12",
            "observation_timestamp": "12-month running means centered on the target month; interpolated to the day",
            **common,
        },
    ]


def build_validation_report(
    contract: BenchmarkContract,
    identity: Mapping[str, Any],
    samples: Sequence[Mapping[str, Any]],
    *,
    now: dt.datetime | None = None,
) -> dict[str, Any]:
    """R-59's seven-area report, in this unit's schema, from 5-10 student-supplied samples
    each carrying `site`, `lat`, `lon`, `target_time_utc`, `local_time_class`,
    `activity_class` and the `official_interface_value` read from the official IRI-2016
    interface. The adapter's own value is computed here for each sample; the report
    passes only if every |adapter - official| <= the PREDECLARED tolerance, whose value
    and declaration timestamp come from configuration and must precede this comparison.
    A report that fails is returned with status "failed" -- it is written, never hidden."""
    resource = contract.report_name
    if _is_tbd(contract.tolerance_tecu) or _is_tbd(contract.tolerance_declared_at_utc):
        raise BenchmarkError(
            "experiment.benchmark_b01.validation_report",
            "tolerance_tecu / tolerance_declared_at_utc are TBD; the tolerance is predeclared by the "
            "student BEFORE the comparison (R-59 limb 2, area 7) and no implementer may fill it (TE 1.1)",
        )
    tolerance = float(contract.tolerance_tecu)  # type: ignore[arg-type]
    declared_at = _parse_utc(
        contract.tolerance_declared_at_utc, resource=resource, field="tolerance.declared_at_utc"
    )
    comparison_at = now or dt.datetime.now(dt.timezone.utc)
    if declared_at >= comparison_at:
        raise BenchmarkError(
            resource,
            f"tolerance declared_at_utc {declared_at.isoformat()} does not precede this comparison {comparison_at.isoformat()} (R-59 limb 2)",
        )
    low, high = _SAMPLE_RANGE
    if not (low <= len(samples) <= high):
        raise BenchmarkError(
            resource, f"{len(samples)} sample(s) supplied; FR-P1-04-15 requires five to ten"
        )
    out_samples: list[dict[str, Any]] = []
    all_within = True
    for s in samples:
        for key in (
            "site",
            "lat",
            "lon",
            "target_time_utc",
            "local_time_class",
            "activity_class",
            "official_interface_value",
        ):
            if key not in s:
                raise BenchmarkError(resource, f"sample {s.get('site')!r} lacks {key!r}")
        when = _parse_utc(s["target_time_utc"], resource=resource, field="sample.target_time_utc")
        if when.month == 12 and when.year == contract.year:
            raise BenchmarkError(
                resource,
                f"sample at {when.isoformat()} falls in the locked month; validation samples never touch December {contract.year}",
            )
        adapter_value = _vtec_at(contract, when, float(s["lat"]), float(s["lon"]))
        official = float(s["official_interface_value"])
        diff = abs(adapter_value - official)
        within = diff <= tolerance
        all_within = all_within and within
        # D-50 hmF2 diagnostic: recorded when the sample carries the official interface's
        # hmF2; no threshold, never part of `within_tolerance`.
        official_hmf2 = s.get("official_interface_hmf2_km")
        adapter_hmf2: float | None = None
        hmf2_diff: float | None = None
        if official_hmf2 is not None:
            official_hmf2 = float(official_hmf2)
            adapter_hmf2 = _hmf2_at(contract, when, float(s["lat"]), float(s["lon"]))
            hmf2_diff = adapter_hmf2 - official_hmf2
        out_samples.append(
            {
                "site": str(s["site"]),
                "lat": float(s["lat"]),
                "lon": float(s["lon"]),
                "target_time_utc": when.isoformat(),
                "local_time_class": str(s["local_time_class"]),
                "activity_class": str(s["activity_class"]),
                "official_interface_value": official,
                "official_interface_source": str(s.get("official_interface_source", "")),
                "official_interface_top": s.get("official_interface_top"),
                "official_interface_header": str(s.get("official_interface_header", "")),
                "adapter_value": adapter_value,
                "abs_diff": diff,
                "within_tolerance": within,
                "official_interface_hmf2_km": official_hmf2,
                "adapter_hmf2_km": adapter_hmf2,
                "hmf2_diff_km_diagnostic_no_threshold": hmf2_diff,
            }
        )
    return {
        "report_name": resource,
        "status": "passed" if all_within else "failed",
        "comparison_ran_at_utc": comparison_at.isoformat(),
        "package_version": {
            "package": contract.package,
            "release": identity["release"],
            "wheel_sha256": contract.wheel_sha256,
            "python": identity["python"],
            "platform": identity["platform"],
        },
        "model_switches": {
            "jf": "iricore default jf array (IRI-2016 defaults; foF2 storm model jf(26) on, foE storm jf(35) off)",
            "iri_version": contract.iri_version,
        },
        "topside_option": "IRI-2016 default topside (NeQuick, jf default)",
        "altitude_ceiling_km": contract.htop_km,
        "units": contract.output_units,
        "output_extraction": f"iricore.vtec: electron density integrated {contract.hbot_km}-{contract.htop_km} km, step {contract.hstep_km} km, sum(Ne*step_km)*1e3*1e-16 -> TECU",
        "driver_inputs": {
            "coordinate": "station geodetic lat/lon (data.yaml: stations, D-1)",
            "time": "UTC target time, hourly",
            "index_inputs_retrospective_centered": True,
            "index_semantics": contract.index_semantics,
            "index_files_sha256": dict(identity["index_files_sha256"]),
            "iri_version": contract.iri_version,
            "oarr_overrides": dict(contract.oarr_overrides),
        },
        "samples": out_samples,
        "tolerance": {
            "value": tolerance,
            "units": contract.output_units,
            "declared_at_utc": declared_at.isoformat(),
        },
    }


def run_gated_generation(
    *,
    contract: BenchmarkContract,
    validation_report: Mapping[str, Any],
    stations: Mapping[str, Any],
    months: Sequence[int] | None = None,
    progress: Any = None,
) -> dict[str, Any]:
    """The production path: pins verified -> all four R-59 limbs -> target grid ->
    workload -> pins re-verified -> stamped rows + provenance. Never called by
    `generate_benchmark`'s injection mode. Returns a mapping with `rows`,
    `provenance` and `partial` (True when `months` restricts the grid)."""
    import time as _time

    identity = verify_runtime(contract)
    driver_rows = benchmark_driver_rows(identity, contract)
    evaluate_generation_gates(
        validation_report=validation_report,
        report_name=contract.report_name,
        availability_matrix=driver_rows,
        benchmark_drivers=BENCHMARK_DRIVER_IDS,
    )
    reported = dict(validation_report.get("driver_inputs", {})).get("index_files_sha256")
    if reported != identity["index_files_sha256"]:
        raise BenchmarkError(
            contract.report_name,
            f"validation report's index_files_sha256 {reported!r} differ from the files installed now {identity['index_files_sha256']!r}; the report validated a different runtime",
        )
    points = build_target_grid(
        stations, year=contract.year, cadence_hours=contract.cadence_hours, months=months
    )
    started = _time.perf_counter()
    rows = evaluate_points(points, contract, progress=progress)
    elapsed = _time.perf_counter() - started
    after = assert_index_unchanged(identity, contract)
    n_err = sum(1 for r in rows if r["status"] != "ok")
    provenance = {
        "benchmark_id": contract.benchmark_id,
        "label": "generated, not trained",
        "runtime_identity": identity,
        "index_files_sha256_after_session": after,
        "validation_report_name": contract.report_name,
        "validation_report_status": validation_report.get("status"),
        "benchmark_driver_rows": driver_rows,
        "stamps": dict(contract.stamps),
        "call_count": len(rows),
        "error_rows": n_err,
        "partial": months is not None,
        "months": sorted(set(int(m) for m in months))
        if months is not None
        else list(range(1, 13)),
        "workload_seconds": round(elapsed, 3),
        "calls_per_second": round(len(rows) / elapsed, 2) if elapsed > 0 else None,
        "integration": {
            "hbot_km": contract.hbot_km,
            "htop_km": contract.htop_km,
            "hstep_km": contract.hstep_km,
            "iri_version": contract.iri_version,
            "oarr_overrides": dict(contract.oarr_overrides),
        },
        "index_semantics": contract.index_semantics,
        "spatial_representativeness_statement": "Phase 1 compares a gridded-cell target against IRI evaluated at the station coordinate; part of any measured difference is geometry and sampling, not skill (Vision 6.6)",
    }
    return {"rows": rows, "provenance": provenance, "partial": months is not None}


#: The reserved transform-identity literal `06` stamps on every generated (never
#: fitted) comparison member -- B-01 and C-01 (`evaluation-and-comparison`
#: business-rules.md: "B-01 and C-01 ... stamped with ... the reserved literal
#: `untransformed`"). Duplicated here, rather than imported from
#: `src.evaluation.guards.UNTRANSFORMED`, to avoid a `src/external` -> `src/evaluation`
#: import edge this unit's boundary note does not grant (TE 12; TA-07); a dedicated
#: equality test (`tests/test_b01_prediction_adapter.py`) asserts the two literals
#: agree so they cannot drift unnoticed.
_UNTRANSFORMED: str = "untransformed"


def predictions_from_benchmark_rows(
    rows: Sequence[Mapping[str, Any]],
    *,
    contract: BenchmarkContract,
    stations: Mapping[str, Any],
    partitions: Sequence[Partition],
) -> dict[str, dict[str, Any]]:
    """Bridge B-01's raw generated rows (`evaluate_points`'s shape) into the eight-field
    `Prediction` payload convention `06` already writes and `07` already reads
    (`src.evaluation.masks.prediction_from_payload`) -- one payload per fold partition.

    Partition-scoping decision (Student/Owner, 2026-09-26): **Option B** -- rows are
    filtered to each partition's own `[validation_month, next_month)` window
    (`src.data.splits.validation_month_range`) before being written into that
    partition's payload; a partition's payload never carries another partition's rows.

    Only `PartitionKind.fold` partitions (F1-F4) are accepted -- `REFIT` has no
    `validation_month` (scored nowhere, FR-P1-04-14) and `DEC` is refused outright: the
    locked partition is reachable only through `governance-guards`' one-door
    `open_restricted` (R-109), which this pure function does not implement and must not
    be assumed by writing into a `DEC` directory ahead of that gate.

    Every envelope field below traces to an already-frozen source -- none is invented
    here (TE 18.2):

    * `model_id` = `contract.benchmark_id` (`configs/experiment.yaml:
      benchmark_b01.benchmark_id`, `"B-01"`);
    * `seed` = `None` (`evaluation-and-comparison/domain-entities.md`: "B-01 and C-01
      are producible as `Prediction`s with `seed = None`");
    * `phase_id`, `source_id`, `target_definition_id` = `contract.stamps` (`configs/
      experiment.yaml: benchmark_b01.stamps`);
    * `transform_id` = the reserved literal `"untransformed"` (same source, "the
      reserved literal `untransformed`");
    * `partition_id` = the fold partition's own `partition_id`.

    Row rename only (`station_id` -> `station`, `target_time_utc` ->
    `interval_start_utc`, `contract.output_field` value -> `y_hat`) -- no new schema.

    Accounting (never a silent drop). Every payload's `b01_generation_provenance`
    carries `total_row_count` (all raw rows supplied), `error_row_count` (rows whose own
    `status != "ok"`), and `unmatched_partition_row_count` (rows that ARE valid B-01
    points but fall in none of the SUPPLIED `partitions`' windows -- e.g. a training-only
    month between F1-F4, per `configs/data.yaml`'s real fold months). The three counts
    are disjoint and sum to `total_row_count`. An unmatched row is NOT an error: it is a
    legitimate completeness fact about the partition set the caller supplied, exactly
    the two-tier posture (integrity violation vs. non-fatal completeness shortfall)
    `evaluate_points`' own `status` field already applies to its rows.

    Raises
    ------
    BenchmarkError
        a `partitions` entry that is not `PartitionKind.fold` (REFIT/DEC refused
        outright); `contract.stamps` missing `phase_id`/`source_id`/
        `target_definition_id`; a row with an unparseable/naive `target_time_utc`; a
        row whose `station_id` is not in `stations` (the registry, D-1); a duplicate
        `(station_id, target_time_utc)` pair across the raw rows; or a fold partition
        whose filtered row set is empty (an empty comparison member masks nothing --
        the same posture `build_comparison_mask` takes on an empty intersection).
    """
    for partition in partitions:
        if partition.kind is not PartitionKind.fold:
            raise BenchmarkError(
                f"partition {partition.partition_id}",
                "is not a fold partition (F1-F4); REFIT has no validation_month (scored "
                "nowhere, FR-P1-04-14) and DEC is reachable only through "
                "governance-guards' one-door open_restricted (R-109) -- this function "
                "accepts fold partitions only",
            )
    required_stamps = ("phase_id", "source_id", "target_definition_id")
    missing_stamps = [k for k in required_stamps if not contract.stamps.get(k)]
    if missing_stamps:
        raise BenchmarkError(
            "experiment.benchmark_b01.stamps",
            f"missing required stamp(s) {missing_stamps}; phase_id/source_id/"
            f"target_definition_id are the comparison's identity stamps and are never "
            f"defaulted (R-105/TE 13)",
        )

    windows: dict[str, tuple[dt.datetime, dt.datetime]] = {
        p.partition_id: validation_month_range(p) for p in partitions
    }
    buckets: dict[str, list[dict[str, Any]]] = {p.partition_id: [] for p in partitions}
    seen_keys: set[tuple[str, str]] = set()
    error_row_count = 0
    unmatched_partition_row_count = 0

    for row in rows:
        status = row.get("status")
        if status != "ok":
            error_row_count += 1
            continue
        station_id = row.get("station_id")
        if station_id not in stations:
            raise BenchmarkError(
                "b01 rows",
                f"row station_id {station_id!r} is not in the station registry "
                f"(configs/data.yaml: stations, D-1); a benchmark row for an "
                f"unregistered station cannot be scored",
            )
        target_time = _parse_utc(row.get("target_time_utc"), resource="b01 rows", field="target_time_utc")
        key = (str(station_id), target_time.isoformat())
        if key in seen_keys:
            raise BenchmarkError(
                "b01 rows",
                f"duplicate row for (station_id, target_time_utc) = {key}; the raw "
                f"benchmark output must not carry the same point twice",
            )
        seen_keys.add(key)
        value = row.get(contract.output_field)
        if not isinstance(value, int | float) or isinstance(value, bool):
            raise BenchmarkError(
                "b01 rows",
                f"row for {key} has status 'ok' but {contract.output_field!r} is "
                f"{value!r}, not a number (a bool is never accepted as a TEC value, "
                f"even though `isinstance(True, int)` is True in Python)",
            )
        for partition_id, (start, end) in windows.items():
            if start <= target_time < end:
                buckets[partition_id].append(
                    {
                        "station": str(station_id),
                        "interval_start_utc": target_time.isoformat(),
                        "y_hat": float(value),
                    }
                )
                break  # windows are disjoint by construction (splits.py); one match only
        else:
            # No supported partition's window claimed this row. This is NOT an error
            # (team.md's two-tier posture): a valid, well-formed B-01 row for a month no
            # declared partition scores (e.g. a training-only month between F1-F4) is a
            # legitimate, non-fatal completeness fact about the SUPPLIED partition set,
            # never an integrity violation. It must still be counted, never silently
            # dropped -- the same posture `evaluate_points`' own error-row accounting
            # already takes for its own rows.
            unmatched_partition_row_count += 1

    payloads: dict[str, dict[str, Any]] = {}
    for partition in partitions:
        member_rows = buckets[partition.partition_id]
        if not member_rows:
            raise BenchmarkError(
                f"partition {partition.partition_id}",
                "the B-01 rows filtered to this partition's validation-month window are "
                "empty; an empty comparison member masks nothing and is refused rather "
                "than written (matches build_comparison_mask's empty-intersection "
                "refusal)",
            )
        payloads[partition.partition_id] = {
            "model_id": contract.benchmark_id,
            "seed": None,
            "partition_id": partition.partition_id,
            "transform_id": _UNTRANSFORMED,
            "phase_id": str(contract.stamps["phase_id"]),
            "source_id": str(contract.stamps["source_id"]),
            "target_definition_id": str(contract.stamps["target_definition_id"]),
            "confirmatory": False,
            "rows": member_rows,
            "b01_generation_provenance": {
                "label": "generated, not trained",
                "error_row_count": error_row_count,
                "unmatched_partition_row_count": unmatched_partition_row_count,
                "total_row_count": len(rows),
            },
        }
    return payloads
