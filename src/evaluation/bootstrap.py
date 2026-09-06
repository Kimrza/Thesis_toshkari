"""B1–B6 bootstrap: the vector time-block bootstrap — TE §13.6 made executable, refusals first.

Purpose
-------
`statistical-inference` R-113…R-121, W-1…W-7 (`vector_block_bootstrap`, the one public
boundary; runs inside `scripts/07_evaluate_and_report.py` and owns no stage script):

* **A metric entry point in full** (R-113): the six SD-C-01 guards are re-asserted here by
  calling `src/evaluation/guards.py` — one copy each, nothing duplicated — before any draw:
  registered mask, stamps against the mask's recorded set, partition agreement,
  mask-vs-member alignment, target space (both members), and on `DEC` the full
  `require_locked_receipt` composition (fail-closed on a missing `LockedContext`, exactly
  as `paired_loss_differential` refuses).
* **One copy of the estimand** (R-114): the per-(station, hour) paired squared-error
  difference series is computed ONCE through `metrics.paired_difference_series` (R-108's
  step-1 path) and replicates reapply ONLY steps 2–3 through `metrics.equal_station_mean`.
  Nothing here re-implements differencing or weighting; the full-data point estimate must
  equal `paired_loss_differential`'s scalar EXACTLY (§13.7) or `BootstrapError` is raised.
* **The confirmed fixed non-overlapping block grid** (R-115; Q2 = A,
  `CR-2026-09-06-R119-BOOTSTRAP-CONFIRMATIONS`): contiguous `block_hours`-hour blocks
  aligned to the scored range's start, derived from the mask's partition window — no
  calendar constant in source. An indivisible range REFUSES rather than truncating or
  padding; a masked row outside the scored range REFUSES (the 1-December redundancy at the
  locked boundary). Scheme and realised block count are recorded on `BootstrapResult`.
* **The vector property and the declared missing-pair rule** (R-116): ONE block-index
  sequence per replicate applied to all stations simultaneously (`VectorBlockDraw` cannot
  represent per-station indices); a block carries, per station, exactly the masked rows in
  its window; a replicate leaving any station with zero rows raises naming the station.
* **Seed and stream discipline** (R-117; D-122; ADR-05 carve-out): `seed` is a REQUIRED
  keyword read from `ConfigSnapshot.seeds` at the call site — a call without it is a
  `TypeError` by signature, never a default. The generator is
  `numpy.random.Generator(PCG64(SeedSequence(seed)))`; block-index draws are the ONLY
  consumer of the primary stream; the 48-hour sensitivity draws from spawn child 0 and the
  widening comparator from spawn child 1, assignments recorded on the result.
* **Method-parametric interval** (R-119; Q1 = A): the interval method is read from
  `configs/experiment.yaml` (`bootstrap.interval_method`); the confirmed `percentile`
  method (2.5th/97.5th, linear interpolation — exactly re-derivable from the replicate
  set) is implemented; any unrecognised, absent or `TBD` value refuses naming the field.
* **The widening guard** (R-120, as amended per GOV-2026-08-28-FD-01 Rec 23/24): the
  rejected Q-27 within-station method runs as the QUARANTINED comparator on child stream 1
  with the SAME masked data, block length and replicate count as its primary call — width
  only, never serialized as a reported interval. At fixture time a narrower vector
  interval RAISES; on real data the failure emits the MANDATORY machine-readable
  disclosure carrying both widths, the comparator parameters, block length and realised
  block count, and the measured cross-station correlations.
* **The correlation emission** (R-121; Q3 = A): pairwise Pearson correlation of the
  per-station paired-difference series over common masked timestamps of each pair, all
  pairs, carried machine-readably on `BootstrapResult`.
* **Byte-pinned determinism evidence** (SD-S-01, Q1 = A): the replicate hash is SHA-256
  over the replicate vector's raw IEEE-754 bytes, canonical form pinned by four recorded
  facts (float64, little-endian, C-order, replicate order = draw order — never sorted
  before hashing); the vector is materialised in full (10,000 × 8 bytes = 80,000 bytes).
* **Append-safe emission** (NFR-AUD-01): `write_bootstrap_result` refuses to overwrite —
  a rerun writes a NEW result via the `.tmp` → fsync → `os.replace` idiom.

Exception declaration note (R-01): `BootstrapError` is one of `foundation` R-01's
enumerated project exceptions and ALREADY EXISTS at the single declaration site,
`src/data/config.py` (verified 2026-09-06). This module IMPORTS and RE-EXPORTS it rather
than redeclaring — a second class object with the same name would break catchability —
and remains its raise site, exactly the pattern `guards.py` records for
`FairnessError`/`InverseTransformError`.

Inputs
------
Prediction-like objects (the approved eight-field `Prediction` shape, structurally typed),
a registered `ComparisonMask` and its registry, the declared comparison sets and the
`experiment.yaml` `bootstrap` declaration read through `ConfigSnapshot` (by the caller,
script 07), the partition window (`month_start`/`month_end`/`embargo_hours` — the
partition's own configured values), the D-122 seed from `ConfigSnapshot.seeds`, and on
`DEC` a `metrics.LockedContext`. **`numpy` is imported LAZILY inside the draw path**: its
absence refuses naming the pinned `numpy==1.26.4` (`requirements.txt`) rather than
substituting a stdlib RNG (the sklearn/FU-1 precedent). Everything numpy-independent —
grid construction, config reads, refusals, correlations, hashing, evidence shapes — is
stdlib-real. This module imports ONLY `src/data`, `src/evaluation` and the standard
library: **no `src/features`, no `src/models`, no `src/external`, directly or
transitively** (D-27; TE §12).

Re-run behaviour
----------------
Pure computation over supplied artifacts plus the append-safe writer. The same seed
reproduces the identical replicate vector and hash EXACTLY (WS-17; §13.7 equality, not
tolerance); a rerun never overwrites a prior serialized `BootstrapResult`. Every refusal
is an `IntegrityError` subclass naming the file or resource and the violated expectation
(R-01's constructor contract), so `foundation` R-10's stage-entry catch writes the
`aborted` registry row for each.

Governance
----------
Q1–Q4 = A (`CR-2026-09-06-R119-BOOTSTRAP-CONFIRMATIONS`); TE §13.6/TC-19 (`binding:
hard`); D-122 (seed 20221201); D-28 (the 720-h DEC scored set: 30 blocks at 24 h, 15 at
48 h); D-27 unreopened (`ABL-DIFF` refuses at the target-space guard). WS-17, TA-13,
TA-14, TA-26 stay `Pending` — nothing here discharges an acceptance row; no bootstrap has
ever executed on real data; G-05/G-06 stay `Blocked`; the G-06 abort policy for a failed
widening comparison is the Supervisor's at G-05 (Rec 23), decided nowhere here. The
approved `component-methods.md` signature is implemented as quoted — `block_hours=24` /
`replicates=10_000` defaults present but NEVER exercised (R-118: both are passed
explicitly from config at every call; on a confirmatory run a mismatch against the
declared config values refuses — control (17)); their removal stays a proposed amendment.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import os
import struct
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.data.config import BootstrapError, IntegrityError, TBD_SENTINEL
from src.data.splits import LOCKED_ID
from src.evaluation.guards import (
    require_mask_member_alignment,
    require_partition_agreement,
    require_registered_mask,
    require_stamps,
    require_target_space,
)
from src.evaluation.metrics import (
    LockedContext,
    equal_station_mean,
    paired_difference_series,
    paired_loss_differential,
)

__all__ = [
    "BootstrapError",
    "GENERATOR_IDENTITY",
    "CANONICAL_FORM_FACTS",
    "STREAM_ASSIGNMENTS",
    "BLOCK_SCHEME_FIXED_NONOVERLAPPING",
    "INTERVAL_METHOD_PERCENTILE",
    "CORRELATION_SERIES_ID",
    "EVALUATION_MODES",
    "NUMPY_PIN",
    "BlockGrid",
    "VectorBlockDraw",
    "WideningGuardEvidence",
    "SensitivityResult",
    "BootstrapResult",
    "read_bootstrap_declaration",
    "build_block_grid",
    "percentile_interval",
    "replicate_hash",
    "pairwise_pearson",
    "vector_block_bootstrap",
    "serialize_bootstrap_result",
    "write_bootstrap_result",
]

#: Engineering contracts, not scientific constants (R-117: "no more a scientific constant
#: than the language pin"). The scientific values — 24, 10000, 0.95, 48, 20221201, the
#: method/scheme/series — live in configs/ and reach this module only as arguments.
GENERATOR_IDENTITY: str = "numpy.random.Generator(PCG64)"

#: SD-S-01's four canonical-form facts, recorded beside the hash so a future dtype or
#: layout drift is detectable rather than silent (Q1 = A).
CANONICAL_FORM_FACTS: Mapping[str, str] = {
    "dtype": "float64",
    "byte_order": "little-endian",
    "layout": "C-order",
    "replicate_order": "draw_order",
}

#: The fixed spawn-tree assignment (R-117 point 2): block-index draws are the ONLY
#: consumer of the primary stream; children are deterministically derived, so no consumer
#: can perturb another's draws.
STREAM_ASSIGNMENTS: Mapping[str, str] = {
    "primary": "block-index draws (root SeedSequence)",
    "child_0": "48-hour sensitivity",
    "child_1": "widening comparator",
}

#: Identity tokens for the config-declared values (the values themselves live in
#: configs/experiment.yaml under the Q1/Q2/Q3 confirmations — never here).
BLOCK_SCHEME_FIXED_NONOVERLAPPING: str = "fixed_nonoverlapping"
INTERVAL_METHOD_PERCENTILE: str = "percentile"
CORRELATION_SERIES_ID: str = "paired_error_pearson_all_pairs"
EVALUATION_MODES: tuple[str, ...] = ("fixture", "real_data")

#: The pinned numpy requirement named by the lazy-import refusal (requirements.txt).
NUMPY_PIN: str = "numpy==1.26.4"

_DECLARATION_FIELD: str = "configs/experiment.yaml: bootstrap"


def _require_numpy() -> Any:
    """Lazy numpy import (the sklearn/FU-1 refusal precedent).

    Raises
    ------
    BootstrapError
        numpy is not importable — the draws refuse naming the pin rather than
        substituting a stdlib RNG, whose different bit stream would silently break
        WS-17's exact reproduction from seed 20221201.
    """
    try:
        import numpy
    except ImportError as exc:
        raise BootstrapError(
            "numpy",
            f"is not importable; the bootstrap's replicate draws require the pinned "
            f"{NUMPY_PIN} (requirements.txt) and refuse rather than substituting a "
            f"different RNG — a different bit stream silently breaks WS-17's exact "
            f"reproduction (R-117; the sklearn/FU-1 refusal precedent)",
        ) from exc
    return numpy


def _as_utc(value: Any, *, resource: str) -> dt.datetime:
    """ISO-8601 → aware UTC datetime; naive values are read as UTC."""
    if isinstance(value, dt.datetime):
        stamp = value
    else:
        text = str(value).strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            stamp = dt.datetime.fromisoformat(text)
        except ValueError as exc:
            raise IntegrityError(resource, f"timestamp {value!r} is not ISO-8601") from exc
    if stamp.tzinfo is None:
        return stamp.replace(tzinfo=dt.UTC)
    return stamp.astimezone(dt.UTC)


# =======================================================================================
# The declaration: every scientific value arrives from configs/experiment.yaml (R-118)
# =======================================================================================


def read_bootstrap_declaration(experiment: Mapping[str, Any]) -> dict[str, Any]:
    """`BootstrapDeclaration` (domain-entities § 1): the frozen numbers live in config.

    Reads `experiment.bootstrap` (the block transcribed under
    `CR-2026-09-06-R119-BOOTSTRAP-CONFIRMATIONS`). The three gate-confirmed identity
    values are validated against the implemented components — an unconfirmed or
    unrecognised value is TE §18.3's stop-and-report made executable (control (18)).

    Raises
    ------
    BootstrapError
        the block is absent or `TBD — freeze gate`; a required field is absent or `TBD`;
        `interval_method`, `block_scheme` or `correlation_series` carries a value no
        implemented component recognises — each refusal names the config field.
    """
    node = experiment.get("bootstrap")
    if node is None or (isinstance(node, str) and node.strip() == TBD_SENTINEL):
        raise BootstrapError(
            _DECLARATION_FIELD,
            "absent or unresolved (TBD — freeze gate); the bootstrap parameters are "
            "frozen scientific protocol values living in configuration (TE 13.6; TC-19; "
            "TC-03e) and are never filled by an implementer by convenience (TE 18.3)",
        )
    if not isinstance(node, Mapping):
        raise BootstrapError(_DECLARATION_FIELD, "must be a mapping of declared fields")

    declared: dict[str, Any] = {}
    for name in (
        "block_hours",
        "replicates",
        "confidence_level",
        "sensitivity_block_hours",
        "seed_key",
        "interval_method",
        "block_scheme",
        "correlation_series",
    ):
        value = node.get(name)
        if value is None or (isinstance(value, str) and value.strip() == TBD_SENTINEL):
            raise BootstrapError(
                f"{_DECLARATION_FIELD}.{name}",
                "absent or unresolved (TBD — freeze gate); the field is part of the "
                "frozen bootstrap declaration and the run refuses rather than defaulting "
                "it (TE 18.2/18.3; R-118, R-119)",
            )
        declared[name] = value

    if declared["interval_method"] != INTERVAL_METHOD_PERCENTILE:
        raise BootstrapError(
            f"{_DECLARATION_FIELD}.interval_method",
            f"value {declared['interval_method']!r} is not a confirmed, implemented "
            f"interval-construction method (the confirmed method is "
            f"{INTERVAL_METHOD_PERCENTILE!r}, Q1 = A); interval construction is "
            f"method-parametric and refuses an unrecognised value rather than choosing "
            f"a default (R-119 control (18); TE 18.3)",
        )
    if declared["block_scheme"] != BLOCK_SCHEME_FIXED_NONOVERLAPPING:
        raise BootstrapError(
            f"{_DECLARATION_FIELD}.block_scheme",
            f"value {declared['block_scheme']!r} is not the confirmed, implemented "
            f"block-resampling scheme ({BLOCK_SCHEME_FIXED_NONOVERLAPPING!r}, Q2 = A); "
            f"the grid builder refuses an unrecognised scheme rather than improvising "
            f"one (R-115; Rec 26)",
        )
    if declared["correlation_series"] != CORRELATION_SERIES_ID:
        raise BootstrapError(
            f"{_DECLARATION_FIELD}.correlation_series",
            f"value {declared['correlation_series']!r} is not the confirmed correlation "
            f"series ({CORRELATION_SERIES_ID!r}, Q3 = A); the emission refuses an "
            f"unrecognised series rather than substituting one (R-121)",
        )
    return declared


# =======================================================================================
# The block grid (R-115): fixed non-overlapping partition, derived from the mask's window
# =======================================================================================


@dataclass(frozen=True)
class BlockGrid:
    """domain-entities § 2: the partition as an assertable fact, scheme recorded."""

    scored_range_start_utc: str
    scored_range_end_utc: str
    block_hours: int
    block_scheme: str
    n_blocks: int
    block_boundaries_utc: tuple[str, ...]


def build_block_grid(
    *,
    month_start: dt.datetime,
    month_end: dt.datetime,
    embargo_hours: int,
    block_hours: int,
    block_scheme: str,
) -> BlockGrid:
    """The confirmed fixed non-overlapping partition of the scored range (R-115; Q2 = A).

    The scored range is the partition's own window less its embargo — the same derivation
    `guards.scored_window_statement` prints — so no calendar constant appears in source:
    for DEC (D-28) this yields exactly 30 blocks at 24 h and 15 at 48 h.

    Raises
    ------
    BootstrapError
        an unrecognised scheme (naming the config field); a scored range that is not a
        whole number of hours; a scored range not evenly divisible by `block_hours` —
        R-115 limb 1: a changed range surfaces as an error, never a quiet truncation,
        padding or reweighting.
    """
    if block_scheme != BLOCK_SCHEME_FIXED_NONOVERLAPPING:
        raise BootstrapError(
            f"{_DECLARATION_FIELD}.block_scheme",
            f"value {block_scheme!r} is not the confirmed, implemented scheme "
            f"({BLOCK_SCHEME_FIXED_NONOVERLAPPING!r}, Q2 = A); the grid builder refuses "
            f"rather than improvising a scheme (R-115; Rec 26)",
        )
    scored_start = month_start + dt.timedelta(hours=int(embargo_hours))
    span = month_end - scored_start
    one_hour = dt.timedelta(hours=1)
    total_hours, remainder = divmod(span, one_hour)
    if remainder or total_hours <= 0:
        raise BootstrapError(
            f"scored range [{scored_start.isoformat()}, {month_end.isoformat()})",
            f"is not a positive whole number of hours ({span}); the hourly grid is the "
            f"partition's own contract and a fractional range cannot be blocked (R-115)",
        )
    if int(block_hours) <= 0 or total_hours % int(block_hours) != 0:
        raise BootstrapError(
            f"scored range [{scored_start.isoformat()}, {month_end.isoformat()})",
            f"is {total_hours} h, not evenly divisible by the {block_hours}-hour block "
            f"length; a partial block is unrepresentable — the range refuses rather than "
            f"silently truncating, padding or reweighting (R-115 limb 1)",
        )
    n_blocks = total_hours // int(block_hours)
    boundaries = tuple(
        (scored_start + dt.timedelta(hours=i * int(block_hours))).isoformat()
        for i in range(n_blocks)
    )
    return BlockGrid(
        scored_range_start_utc=scored_start.isoformat(),
        scored_range_end_utc=month_end.isoformat(),
        block_hours=int(block_hours),
        block_scheme=block_scheme,
        n_blocks=int(n_blocks),
        block_boundaries_utc=boundaries,
    )


def _block_values(
    series: Mapping[str, Sequence[tuple[str, float]]], grid: BlockGrid
) -> dict[str, list[list[float]]]:
    """Per station, the masked-row differences of each block window (R-116's declared rule).

    A block carries, per station, exactly the masked rows falling inside its window —
    arithmetic on what the frozen mask already says, never a new exclusion policy and
    never a narrowing of the scored population. Blocks are generally RAGGED across
    stations (the mask is an intersection per (station, hour)).

    Raises
    ------
    BootstrapError
        a masked row outside the grid's scored range — R-115 limb 2's boundary raise:
        a 1-December row in a DEC grid is refused here in addition to the mask's own
        upstream assertion (redundancy at the locked boundary is by design).
    """
    scored_start = _as_utc(grid.scored_range_start_utc, resource="block grid")
    scored_end = _as_utc(grid.scored_range_end_utc, resource="block grid")
    block_span = dt.timedelta(hours=grid.block_hours)
    out: dict[str, list[list[float]]] = {
        station: [[] for _ in range(grid.n_blocks)] for station in series
    }
    for station, rows in series.items():
        for stamp_text, diff in rows:
            stamp = _as_utc(stamp_text, resource=f"station {station} masked row")
            if not (scored_start <= stamp < scored_end):
                raise BootstrapError(
                    f"station {station} masked row {stamp.isoformat()}",
                    f"lies outside the grid's scored range "
                    f"[{grid.scored_range_start_utc}, {grid.scored_range_end_utc}); a "
                    f"block extending outside the mask's scored range is refused — the "
                    f"locked-boundary redundancy (R-115 limb 2; R-109 limb 3 upstream)",
                )
            index = (stamp - scored_start) // block_span
            out[station][int(index)].append(float(diff))
    return out


# =======================================================================================
# The draw shape (R-116): one index sequence per replicate, applied to ALL stations
# =======================================================================================


@dataclass(frozen=True)
class VectorBlockDraw:
    """domain-entities § 3: the vector property is UNREPRESENTABLE to violate.

    One `block_indices` sequence per replicate, applied to all stations simultaneously —
    the shape carries no per-station index field, so the Q-27 anti-pattern (independent
    per-station resampling) cannot be expressed through it (TC-19, caught structurally).
    """

    block_indices: tuple[int, ...]


def _replicate_statistic(
    draw: VectorBlockDraw,
    block_values: Mapping[str, Sequence[Sequence[float]]],
    *,
    window: str,
) -> float:
    """Steps 2–3 of R-108 reapplied to the drawn rows (R-114; via `equal_station_mean`).

    Raises
    ------
    BootstrapError
        a station whose drawn blocks contain zero masked rows — the equal-station mean is
        undefined; the raise names the station and window (R-116 point 3; R-01's
        constructor contract).
    """
    per_station: dict[str, list[float]] = {}
    for station, blocks in block_values.items():
        drawn: list[float] = []
        for index in draw.block_indices:
            drawn.extend(blocks[index])
        if not drawn:
            raise BootstrapError(
                f"station {station}",
                f"has zero masked rows across a replicate's drawn blocks over {window}; "
                f"the equal-station mean is undefined for a zero-support station — a "
                f"structural guard December's measured coverage makes practically "
                f"unreachable (R-116)",
            )
        per_station[station] = drawn
    scalar, _ = equal_station_mean(per_station)
    return scalar


# =======================================================================================
# Interval construction (R-119, method-parametric) and the byte-pinned hash (SD-S-01)
# =======================================================================================


def percentile_interval(values: Sequence[float], *, ci_level: float) -> tuple[float, float]:
    """The confirmed percentile interval (Q1 = A): quantiles of the ordered replicate set.

    Linear interpolation over the order statistics (position (n-1)·p), which is exactly
    re-derivable from the hashed replicate vector alone — WS-17's evidence stays
    sufficient. The input sequence is NOT mutated and NOT the hash input (the hash is
    taken over draw order before any sorting).

    Raises
    ------
    BootstrapError
        an empty replicate set or a `ci_level` outside (0, 1).
    """
    if not values:
        raise BootstrapError(
            "replicate set", "is empty; an interval over zero replicates is not an interval"
        )
    if not (0.0 < float(ci_level) < 1.0):
        raise BootstrapError(
            f"{_DECLARATION_FIELD}.confidence_level",
            f"value {ci_level!r} is not a probability strictly between 0 and 1",
        )
    ordered = sorted(float(v) for v in values)

    def quantile(p: float) -> float:
        position = (len(ordered) - 1) * p
        low = math.floor(position)
        high = math.ceil(position)
        if low == high:
            return ordered[low]
        return ordered[low] + (ordered[high] - ordered[low]) * (position - low)

    alpha = (1.0 - float(ci_level)) / 2.0
    return quantile(alpha), quantile(1.0 - alpha)


def replicate_hash(values: Sequence[float]) -> str:
    """SD-S-01 (Q1 = A): SHA-256 over the replicate vector's raw IEEE-754 bytes.

    Canonical form is the four recorded facts (`CANONICAL_FORM_FACTS`): float64 values,
    little-endian byte order, contiguous C-order layout, replicate order = draw order —
    the vector is hashed exactly as drawn, NEVER sorted first. `struct.pack('<d')`
    produces the identical bytes `numpy.float64.tobytes()` would on the same values, so
    the hash is platform-independent on both governed platforms.
    """
    return hashlib.sha256(struct.pack(f"<{len(values)}d", *values)).hexdigest()


def pairwise_pearson(
    series: Mapping[str, Sequence[tuple[str, float]]],
) -> dict[str, float]:
    """R-121 (Q3 = A): Pearson correlation of d_s(t) per station pair, all pairs.

    Computed over the COMMON masked timestamps of each pair — the estimand's own series,
    whose cross-station correlation is precisely the quantity that justifies the vector
    construction. Keys are ``"<A>-<B>"`` over sorted station names, so the three real
    stations report as ARUC-BSHM, ARUC-NICO, BSHM-NICO.

    Raises
    ------
    BootstrapError
        a pair with fewer than two common masked timestamps, or a degenerate
        (zero-variance) series on either side — an undefined correlation is surfaced,
        never silently skipped (the unit's refuse-loudly posture).
    """
    stations = sorted(series)
    out: dict[str, float] = {}
    for i, first in enumerate(stations):
        for second in stations[i + 1 :]:
            a = {stamp: diff for stamp, diff in series[first]}
            b = {stamp: diff for stamp, diff in series[second]}
            common = sorted(set(a) & set(b))
            if len(common) < 2:
                raise BootstrapError(
                    f"station pair {first}-{second}",
                    f"has {len(common)} common masked timestamp(s); the pairwise "
                    f"paired-error Pearson correlation needs at least two (R-121)",
                )
            xs = [a[stamp] for stamp in common]
            ys = [b[stamp] for stamp in common]
            mean_x = sum(xs) / len(xs)
            mean_y = sum(ys) / len(ys)
            sxx = sum((x - mean_x) ** 2 for x in xs)
            syy = sum((y - mean_y) ** 2 for y in ys)
            if sxx == 0.0 or syy == 0.0:
                raise BootstrapError(
                    f"station pair {first}-{second}",
                    "has a zero-variance paired-difference series on the common "
                    "timestamps; the Pearson correlation is undefined and is surfaced "
                    "rather than defaulted (R-121)",
                )
            sxy = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys, strict=True))
            out[f"{first}-{second}"] = sxy / math.sqrt(sxx * syy)
    return out


# =======================================================================================
# Guard evidence, sensitivity, and the result (domain-entities §§ 5-7)
# =======================================================================================


@dataclass(frozen=True)
class WideningGuardEvidence:
    """domain-entities § 6: evidence of the check, quarantined from reporting (R-120).

    Width only — the shape carries NO comparator interval bounds and NO comparator CI
    level, so the Q-27 variant is unserialisable as a reported interval (control (20)).
    Construction ENFORCES the amended failure semantics: a fixture-mode failure raises
    (the TA-14 assertion TE §13.6 specifies), and a real-data failure is representable
    only WITH its mandatory disclosure carrying the measured correlations (control (22)).
    """

    vector_width: float
    comparator_width: float
    comparator_replicates: int
    comparator_derived_seed: str
    passed: bool
    evaluation_mode: str
    disclosure: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.evaluation_mode not in EVALUATION_MODES:
            raise BootstrapError(
                "widening guard evidence",
                f"evaluation_mode {self.evaluation_mode!r} is not one of "
                f"{list(EVALUATION_MODES)}; the failure semantics differ by mode "
                f"(Rec 23) and an unlabelled mode cannot pick one",
            )
        if self.evaluation_mode == "fixture" and not self.passed:
            raise BootstrapError(
                "widening guard (fixture)",
                f"the vector interval (width {self.vector_width}) is NARROWER than the "
                f"naive within-station comparator's (width {self.comparator_width}, "
                f"{self.comparator_replicates} replicates, "
                f"{self.comparator_derived_seed}) on the synthetic fixture, where the "
                f"planted correlation makes widening hold by construction — the Q-27 "
                f"substitution signal TE 13.6's final sentence exists to catch (R-120; "
                f"TC-19). A serialized fixture-mode result therefore always implies "
                f"passed",
            )
        if self.evaluation_mode == "real_data" and not self.passed:
            required = (
                "vector_width",
                "comparator_width",
                "comparator_replicates",
                "comparator_derived_seed",
                "block_hours",
                "block_scheme",
                "n_blocks",
                "pairwise_correlations",
            )
            missing = [
                name
                for name in required
                if not isinstance(self.disclosure, Mapping) or name not in self.disclosure
            ]
            if missing:
                raise BootstrapError(
                    "widening guard (real data)",
                    f"the comparison failed and the MANDATORY machine-readable "
                    f"disclosure is absent or incomplete (missing {missing}); the "
                    f"disclosure — both widths, the comparator parameters, block length "
                    f"and realised block count, and the measured cross-station "
                    f"correlations — is not optional, not a log line, and not "
                    f"suppressible (R-120 as amended per Rec 23; control (22))",
                )
        if self.passed and self.disclosure is not None:
            raise BootstrapError(
                "widening guard evidence",
                "carries a failure disclosure on a PASSED comparison; the disclosure "
                "exists only where the comparison failed on real data (R-120)",
            )


@dataclass(frozen=True)
class SensitivityResult:
    """domain-entities § 7: the 48-hour sensitivity — labelled, separate, never merged.

    A predeclared named run (TE §7.2's registration discipline); `run_id` is the owner's
    registration act and is carried as `None` until the owner registers it — never filled
    by convenience. Same seed on its OWN derived child stream (child 0), so the
    sensitivity can never perturb the confirmatory draws.
    """

    label: str
    block_hours: int
    n_blocks: int
    ci_lower: float
    ci_upper: float
    ci_level: float
    derived_seed: str
    run_id: str | None = None

    def __post_init__(self) -> None:
        if self.label != "sensitivity":
            raise BootstrapError(
                "sensitivity result",
                f"label {self.label!r} is not 'sensitivity'; the 48-hour result is a "
                f"distinct labelled field, never merged into or substituted for the "
                f"confirmatory interval (R-118 control (16))",
            )


@dataclass(frozen=True)
class BootstrapResult:
    """domain-entities § 5: the result carries its own evidence (R-110's pattern).

    Construction VALIDATES the evidence surface: the four canonical-form facts, the
    generator identity, the seed key, the stream assignments, the fully materialised
    replicate vector, the correlations, the guard evidence and the labelled sensitivity
    must all be present — an evidence-incomplete result is unconstructible, not merely
    discouraged (SD-S-01's presence controls; controls (21) and (24)).
    """

    # interval
    ci_lower: float
    ci_upper: float
    ci_level: float
    interval_method: str
    block_hours: int
    block_scheme: str
    replicates: int
    # point estimate (equality-checked against EstimandResult.scalar, R-114)
    point_estimate: float
    per_station_components: Mapping[str, float]
    # determinism evidence (WS-17; R-117; SD-S-01)
    seed: int
    seed_key: str
    generator_identity: str
    replicate_hash: str
    canonical_form: Mapping[str, str]
    stream_assignments: Mapping[str, str]
    replicate_vector: tuple[float, ...]
    # guard evidence (R-120) and the mandated correlations (R-121)
    widening_guard: WideningGuardEvidence
    pairwise_correlations: Mapping[str, float]
    correlation_series: str
    # the labelled sensitivity (R-118)
    sensitivity: SensitivityResult
    # provenance (the mask/stamp identifiers the interval was computed over)
    mask_id: str
    set_id: str
    partition_id: str
    model_id: str
    benchmark_id: str
    n_blocks: int
    evaluation_mode: str = field(default="real_data")

    def __post_init__(self) -> None:
        def _fail(name: str, expectation: str) -> None:
            raise BootstrapError(
                f"BootstrapResult {self.model_id} vs {self.benchmark_id}", f"{name}: {expectation}"
            )

        for fact, expected in CANONICAL_FORM_FACTS.items():
            if self.canonical_form.get(fact) != expected:
                _fail(
                    "canonical_form",
                    f"fact {fact!r} absent or not {expected!r}; the hash's canonical "
                    f"form is recorded beside it so drift is detectable (SD-S-01)",
                )
        if not self.generator_identity:
            _fail("generator_identity", "absent; WS-17's evidence names its generator (R-117)")
        if not self.seed_key:
            _fail("seed_key", "absent; the consumed seeds.yaml key is recorded (R-117)")
        for child in ("child_0", "child_1"):
            if child not in self.stream_assignments:
                _fail(
                    "stream_assignments",
                    f"{child} unassigned; the spawn tree is recorded so the evidence "
                    f"names its streams (R-117; SD-S-03)",
                )
        if len(self.replicate_hash) != 64:
            _fail("replicate_hash", "is not a SHA-256 hex digest (SD-S-01)")
        if len(self.replicate_vector) != self.replicates:
            _fail(
                "replicate_vector",
                f"carries {len(self.replicate_vector)} of {self.replicates} replicate "
                f"statistics; the vector is materialised IN FULL (SD-S-04: the "
                f"percentile interval re-derives from it and the hash is over its bytes)",
            )
        if not self.per_station_components:
            _fail("per_station_components", "absent; the equal-station mean must evidence itself")
        if not self.pairwise_correlations:
            _fail(
                "pairwise_correlations",
                "absent; TE 13.6's mandated cross-station paired-error correlation is a "
                "produced field, all pairs (R-121 control (24))",
            )
        if self.correlation_series != CORRELATION_SERIES_ID:
            _fail(
                "correlation_series",
                f"is {self.correlation_series!r}, not the confirmed "
                f"{CORRELATION_SERIES_ID!r} (Q3 = A)",
            )
        if not isinstance(self.widening_guard, WideningGuardEvidence):
            _fail("widening_guard", "absent; the guard evidence travels on the result (R-120)")
        if not isinstance(self.sensitivity, SensitivityResult):
            _fail("sensitivity", "absent; the labelled 48-hour result travels on the result")
        if self.sensitivity.block_hours == self.block_hours:
            _fail(
                "sensitivity",
                f"block_hours {self.sensitivity.block_hours} equals the confirmatory "
                f"{self.block_hours}; the sensitivity is a DISTINCT labelled field, "
                f"never merged (R-118 control (16))",
            )
        if self.ci_lower > self.ci_upper:
            _fail("interval", f"ci_lower {self.ci_lower} exceeds ci_upper {self.ci_upper}")
        if self.evaluation_mode not in EVALUATION_MODES:
            _fail("evaluation_mode", f"{self.evaluation_mode!r} not in {list(EVALUATION_MODES)}")


# =======================================================================================
# W-1: the boundary
# =======================================================================================


def vector_block_bootstrap(
    model: Any,
    benchmark: Any,
    *,
    mask: Any,
    block_hours: int = 24,
    replicates: int = 10_000,
    seed: int,
    declared_sets: Mapping[str, Mapping[str, Any]],
    registry: Any,
    experiment: Mapping[str, Any],
    evaluation_mode: str,
    month_start: dt.datetime,
    month_end: dt.datetime,
    embargo_hours: int,
    locked: LockedContext | None = None,
) -> BootstrapResult:
    """W-1: the vector time-block bootstrap, a metric entry point in full (TE §13.6).

    The approved `component-methods.md` parameters (`model`, `benchmark`, `mask`,
    `block_hours=24`, `replicates=10_000`, `seed`) are implemented exactly as quoted —
    the two defaults are NEVER exercised (every call passes both explicitly from
    `ConfigSnapshot`; on a confirmatory run a mismatch against the config-declared values
    refuses, control (17)); their removal is the R-118 amendment, proposed at the gate,
    not applied. The additional keyword-only parameters are the guard inputs and
    config-declared values the design fixes (SD-S-02: preconditions via the shared guard
    module; R-118: values passed explicitly from config; Rec 23: the evaluation mode that
    selects the widening guard's failure semantics) — intra-package surface, `seed` still
    required by signature (a call without it is a `TypeError`, R-117 control (15)).

    Ordered exactly as W-1 fixes it: preconditions (the sibling's six guards, one copy
    each) → precompute the paired-difference series ONCE (W-2, via
    `metrics.paired_difference_series`) → the exact-equality control against
    `paired_loss_differential`'s scalar → the confirmed fixed non-overlapping block grid
    (W-3) → 10,000 vector draws on the primary PCG64 stream (W-4) → the config-declared
    percentile interval (W-5) → the 48-hour sensitivity on child stream 0 (W-5) → the
    quarantined within-station widening comparator on child stream 1 (W-6) → assembly
    (W-7). `numpy` is required only at the draw step and its absence refuses naming the
    `numpy==1.26.4` pin.

    Raises
    ------
    FairnessError, PartitionError, LeakageError, LockedTestError, InverseTransformError
        the re-asserted metric-entry preconditions (R-113, one copy each via
        `src/evaluation/guards.py`; `IntegrityError` fail-closed on a `DEC` mask with no
        `LockedContext`, mirroring `paired_loss_differential`).
    BootstrapError
        every bootstrap-specific refusal: unconfirmed/unrecognised declaration values;
        confirmatory echo drift (control (17)); point-estimate inequality (R-114);
        indivisible range or boundary-crossing row (R-115); zero-support replicate
        (R-116); numpy absent (naming the pin); fixture-time widening failure (R-120);
        evidence-incomplete result shapes.
    TypeError
        a call without `seed` — by signature, unrepresentable rather than checked.
    """
    if evaluation_mode not in EVALUATION_MODES:
        raise BootstrapError(
            "vector_block_bootstrap call",
            f"evaluation_mode {evaluation_mode!r} is not one of {list(EVALUATION_MODES)}; "
            f"the widening guard's failure semantics differ by mode (Rec 23) and an "
            f"unlabelled call cannot pick one",
        )

    # --- W-1 preconditions: the sibling's guards, one copy each (R-113; SD-S-02) --------
    members = (model, benchmark)
    require_registered_mask(mask, members=members, declared_sets=declared_sets, registry=registry)
    require_stamps(members, recorded_transform_ids=mask.member_transform_ids)
    require_partition_agreement(members)
    require_mask_member_alignment(mask, members)
    require_target_space(model)
    require_target_space(benchmark)
    if str(getattr(mask, "partition_id", "")) == LOCKED_ID and locked is None:
        raise IntegrityError(
            f"DEC bootstrap {getattr(model, 'model_id', '?')} vs "
            f"{getattr(benchmark, 'model_id', '?')}",
            "no LockedContext supplied for a DEC-partition mask; the locked path requires "
            "the hash receipt, the access record and the frozen-bundle manifest (R-109; "
            "R-113 precondition 3) and refuses fail-closed without them",
        )

    # --- the declaration: every scientific value from config (R-118, R-119) -------------
    declaration = read_bootstrap_declaration(experiment)
    if evaluation_mode == "real_data" and (
        int(block_hours) != int(declaration["block_hours"])
        or int(replicates) != int(declaration["replicates"])
    ):
        raise BootstrapError(
            "confirmatory bootstrap call",
            f"was passed block_hours={block_hours} / replicates={replicates} but "
            f"configs/experiment.yaml declares "
            f"{declaration['block_hours']} / {declaration['replicates']}; on a "
            f"confirmatory run the recorded values must equal the config-declared ones — "
            f"the dead-default drift channel made visible (R-118 control (17); the "
            f"declared reduced-replicate fixture execution runs in 'fixture' mode against "
            f"the fixture manifest instead, TE 15.3)",
        )
    ci_level = float(declaration["confidence_level"])
    interval_method = str(declaration["interval_method"])
    block_scheme = str(declaration["block_scheme"])
    sensitivity_hours = int(declaration["sensitivity_block_hours"])
    seed_key = str(declaration["seed_key"])

    # --- W-2: precompute ONCE through the estimand's own step-1 path (R-114) ------------
    estimand = paired_loss_differential(
        model,
        benchmark,
        mask=mask,
        declared_sets=declared_sets,
        registry=registry,
        locked=locked,
    )
    model_id = str(getattr(model, "model_id"))
    benchmark_id = str(getattr(benchmark, "model_id"))
    series = paired_difference_series(model_id, benchmark_id, mask)
    point_estimate, per_station_components = equal_station_mean(
        {station: [diff for _, diff in rows] for station, rows in series.items()}
    )
    if point_estimate != estimand.scalar or per_station_components != dict(estimand.per_station):
        raise BootstrapError(
            f"bootstrap point estimate {model_id} vs {benchmark_id}",
            f"full-data point estimate {point_estimate!r} does not equal "
            f"paired_loss_differential's scalar {estimand.scalar!r} EXACTLY on the same "
            f"mask; a deterministic CPU transformation admits no tolerance (13.7) and "
            f"the one-copy claim is a checked invariant, not a diagram (R-114 control (5))",
        )

    # --- W-3: the confirmed grid and the per-block masked rows (R-115, R-116) -----------
    grid = build_block_grid(
        month_start=month_start,
        month_end=month_end,
        embargo_hours=embargo_hours,
        block_hours=int(block_hours),
        block_scheme=block_scheme,
    )
    block_values = _block_values(series, grid)
    window = f"[{grid.scored_range_start_utc}, {grid.scored_range_end_utc})"

    # --- R-121: the mandated correlations (stdlib; also the disclosure's content) --------
    correlations = pairwise_pearson(series)

    # --- W-4: seed and stream discipline; draws need numpy, lazily (R-117) --------------
    np = _require_numpy()
    root = np.random.SeedSequence(int(seed))
    child_sensitivity, child_comparator = root.spawn(2)
    sensitivity_seed_id = f"SeedSequence({int(seed)}, spawn_key=(0,))"
    comparator_seed_id = f"SeedSequence({int(seed)}, spawn_key=(1,))"

    primary_rng = np.random.Generator(np.random.PCG64(root))
    primary_indices = primary_rng.integers(0, grid.n_blocks, size=(int(replicates), grid.n_blocks))
    replicate_stats = [
        _replicate_statistic(
            VectorBlockDraw(block_indices=tuple(int(i) for i in row)),
            block_values,
            window=window,
        )
        for row in primary_indices
    ]
    vector_hash = replicate_hash(replicate_stats)
    ci_lower, ci_upper = percentile_interval(replicate_stats, ci_level=ci_level)
    vector_width = ci_upper - ci_lower

    # --- W-5: the 48-hour sensitivity on child stream 0 (R-118) -------------------------
    sensitivity_grid = build_block_grid(
        month_start=month_start,
        month_end=month_end,
        embargo_hours=embargo_hours,
        block_hours=sensitivity_hours,
        block_scheme=block_scheme,
    )
    sensitivity_values = _block_values(series, sensitivity_grid)
    sensitivity_rng = np.random.Generator(np.random.PCG64(child_sensitivity))
    sensitivity_indices = sensitivity_rng.integers(
        0, sensitivity_grid.n_blocks, size=(int(replicates), sensitivity_grid.n_blocks)
    )
    sensitivity_stats = [
        _replicate_statistic(
            VectorBlockDraw(block_indices=tuple(int(i) for i in row)),
            sensitivity_values,
            window=window,
        )
        for row in sensitivity_indices
    ]
    sensitivity_lower, sensitivity_upper = percentile_interval(
        sensitivity_stats, ci_level=ci_level
    )
    declared_run_id = experiment.get("bootstrap", {}).get("sensitivity_run_id")
    if isinstance(declared_run_id, str) and declared_run_id.strip() == TBD_SENTINEL:
        declared_run_id = None  # the owner's TE 7.2 registration act, never defaulted
    sensitivity = SensitivityResult(
        label="sensitivity",
        block_hours=sensitivity_hours,
        n_blocks=sensitivity_grid.n_blocks,
        ci_lower=sensitivity_lower,
        ci_upper=sensitivity_upper,
        ci_level=ci_level,
        derived_seed=sensitivity_seed_id,
        run_id=declared_run_id if isinstance(declared_run_id, str) else None,
    )

    # --- W-6: the quarantined within-station comparator on child stream 1 (R-120) -------
    # The rejected Q-27 method, present solely to be beaten: SAME masked data, SAME block
    # length, SAME replicate count as this primary call — independent per-station index
    # sequences are exactly the property the vector draw forbids.
    comparator_rng = np.random.Generator(np.random.PCG64(child_comparator))
    stations = sorted(block_values)
    comparator_indices = comparator_rng.integers(
        0, grid.n_blocks, size=(int(replicates), len(stations), grid.n_blocks)
    )
    comparator_stats: list[float] = []
    for row in comparator_indices:
        per_station: dict[str, list[float]] = {}
        for station, station_indices in zip(stations, row, strict=True):
            drawn: list[float] = []
            for index in station_indices:
                drawn.extend(block_values[station][int(index)])
            if not drawn:
                raise BootstrapError(
                    f"station {station}",
                    f"has zero masked rows across a comparator replicate's drawn blocks "
                    f"over {window}; the equal-station mean is undefined (R-116's "
                    f"structural guard, applied to the comparator identically)",
                )
            per_station[station] = drawn
        scalar, _ = equal_station_mean(per_station)
        comparator_stats.append(scalar)
    comparator_lower, comparator_upper = percentile_interval(comparator_stats, ci_level=ci_level)
    comparator_width = comparator_upper - comparator_lower  # width ONLY — never bounds

    passed = not (vector_width < comparator_width)
    disclosure: dict[str, Any] | None = None
    if not passed and evaluation_mode == "real_data":
        disclosure = {
            "vector_width": vector_width,
            "comparator_width": comparator_width,
            "comparator_replicates": int(replicates),
            "comparator_derived_seed": comparator_seed_id,
            "block_hours": grid.block_hours,
            "block_scheme": grid.block_scheme,
            "n_blocks": grid.n_blocks,
            "pairwise_correlations": dict(correlations),
            "statement": (
                "the vector time-block interval is not wider than the naive "
                "within-station comparator's on this real dataset; widening follows only "
                "where cross-station paired-error covariance is positive, so read this "
                "beside the measured correlations above (R-120 as amended per "
                "GOV-2026-08-28-FD-01 Rec 23; the G-06 abort policy is the Supervisor's "
                "at G-05)"
            ),
        }
    widening_guard = WideningGuardEvidence(
        vector_width=vector_width,
        comparator_width=comparator_width,
        comparator_replicates=int(replicates),
        comparator_derived_seed=comparator_seed_id,
        passed=passed,
        evaluation_mode=evaluation_mode,
        disclosure=disclosure,
    )  # a fixture-mode failure RAISES inside this constructor (R-120; control (19))

    # --- W-7: assembly — the result carries its own evidence (R-110's pattern) ----------
    return BootstrapResult(
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        ci_level=ci_level,
        interval_method=interval_method,
        block_hours=grid.block_hours,
        block_scheme=grid.block_scheme,
        replicates=int(replicates),
        point_estimate=point_estimate,
        per_station_components=per_station_components,
        seed=int(seed),
        seed_key=seed_key,
        generator_identity=GENERATOR_IDENTITY,
        replicate_hash=vector_hash,
        canonical_form=dict(CANONICAL_FORM_FACTS),
        stream_assignments=dict(STREAM_ASSIGNMENTS),
        replicate_vector=tuple(float(v) for v in replicate_stats),
        widening_guard=widening_guard,
        pairwise_correlations=correlations,
        correlation_series=CORRELATION_SERIES_ID,
        sensitivity=sensitivity,
        mask_id=str(mask.mask_id),
        set_id=str(mask.set_id),
        partition_id=str(mask.partition_id),
        model_id=model_id,
        benchmark_id=benchmark_id,
        n_blocks=grid.n_blocks,
        evaluation_mode=evaluation_mode,
    )


# =======================================================================================
# Append-safe emission (NFR-AUD-01)
# =======================================================================================


def serialize_bootstrap_result(result: BootstrapResult) -> dict[str, Any]:
    """The machine-readable form (WS-17's evidence surface; TA-14's synthetic-case form).

    The widening guard serializes as GUARD EVIDENCE — widths, parameters, outcome, and
    the disclosure where the real-data comparison failed. It carries no comparator
    interval bounds and no comparator CI level, so the Q-27 variant cannot re-enter any
    results artifact, table or notebook as an interval (R-120 quarantine, control (20)).
    """
    return {
        "artifact_class": "bootstrap_result",
        "ci_lower": result.ci_lower,
        "ci_upper": result.ci_upper,
        "ci_level": result.ci_level,
        "interval_method": result.interval_method,
        "block_hours": result.block_hours,
        "block_scheme": result.block_scheme,
        "replicates": result.replicates,
        "point_estimate": result.point_estimate,
        "per_station_components": dict(result.per_station_components),
        "seed": result.seed,
        "seed_key": result.seed_key,
        "generator_identity": result.generator_identity,
        "replicate_hash": result.replicate_hash,
        "canonical_form": dict(result.canonical_form),
        "stream_assignments": dict(result.stream_assignments),
        "replicate_vector": list(result.replicate_vector),
        "widening_guard": {
            "vector_width": result.widening_guard.vector_width,
            "comparator_width": result.widening_guard.comparator_width,
            "comparator_replicates": result.widening_guard.comparator_replicates,
            "comparator_derived_seed": result.widening_guard.comparator_derived_seed,
            "passed": result.widening_guard.passed,
            "evaluation_mode": result.widening_guard.evaluation_mode,
            "disclosure": (
                dict(result.widening_guard.disclosure)
                if result.widening_guard.disclosure is not None
                else None
            ),
        },
        "pairwise_correlations": dict(result.pairwise_correlations),
        "correlation_series": result.correlation_series,
        "sensitivity": {
            "label": result.sensitivity.label,
            "block_hours": result.sensitivity.block_hours,
            "n_blocks": result.sensitivity.n_blocks,
            "ci_lower": result.sensitivity.ci_lower,
            "ci_upper": result.sensitivity.ci_upper,
            "ci_level": result.sensitivity.ci_level,
            "derived_seed": result.sensitivity.derived_seed,
            "run_id": result.sensitivity.run_id,
        },
        "mask_id": result.mask_id,
        "set_id": result.set_id,
        "partition_id": result.partition_id,
        "model_id": result.model_id,
        "benchmark_id": result.benchmark_id,
        "n_blocks": result.n_blocks,
        "emitted_at_utc": dt.datetime.now(dt.UTC).isoformat(),
    }


def write_bootstrap_result(result: BootstrapResult, path: Path) -> Path:
    """Durable, append-safe serialization: a rerun writes a NEW result, never over an old.

    `.tmp` → flush+fsync → atomic `os.replace`, the project idiom; an existing artifact
    refuses (NFR-AUD-01's no-silent-replacement posture — a failed or superseded run
    stays visible; a re-run emits under its own run directory).

    Raises
    ------
    BootstrapError
        the target already exists — append-safe is a check, not a description.
    IntegrityError
        the durable write fails at any step; nothing is then recorded.
    """
    path = Path(path)
    if path.exists():
        raise BootstrapError(
            path,
            "a serialized BootstrapResult already exists at this path; results are never "
            "silently overwritten (NFR-AUD-01) — a rerun writes a NEW result under its "
            "own run directory, and the prior one stays visible",
        )
    payload = (
        json.dumps(serialize_bootstrap_result(result), sort_keys=True, indent=2, default=str)
        + "\n"
    ).encode("utf-8")
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
        os.replace(tmp, path)
    except OSError as exc:
        raise IntegrityError(
            path, f"durable bootstrap-result write failed ({exc}); nothing is recorded"
        ) from exc
    return path
