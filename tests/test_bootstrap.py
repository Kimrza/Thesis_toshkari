"""WS-17 / TA-14: the vector time-block bootstrap — every hard rule's negative control.

PURPOSE. `statistical-inference` R-113 ... R-122 (W-8's verification plan): the eight
FR-P1-05-8 mechanical checks plus the named negative controls — the per-entry guard
controls through `vector_block_bootstrap` (this unit's half of the SD-C-01 entry-point
contract: stamp-less prediction, unregistered mask, mask-mismatched `partition_id` set,
member `partition_id` mismatch by discriminated type, receipt-less `DEC` call,
transformed-space `ABL-DIFF` frame), the R-115 grid raises (indivisible range,
boundary-crossing row), the R-116 vector-property and zero-support controls, the R-117
seed/stream controls (same seed → identical hash asserted for EQUALITY, different seed →
different hash, missing `seed` → `TypeError` by signature, stream isolation), the R-119
method refusal naming the config field, the R-120 quarantine / fixture-raise / mandatory
real-data disclosure controls, the R-121 correlation recovery and presence controls, the
SD-S-01 byte-pinned canonical-form controls, and NFR-AUD-01's append-safety.

CONSTANTS CONVENTION (R-122). Synthetic fixture parameters — the planted per-day
difference values, the gap pattern, per-station row counts, the REDUCED replicate counts
of the fixture-mode runs (TE §15.3's timing-execution analogue; R-118 control (17) is
scoped to confirmatory runs, so a reduced fixture count trips nothing), and the apparatus
seeds — are declared constants OF THE TEST APPARATUS, stated as such: explicitly NOT
scientific values. The scientific values (seed 20221201, block length 24, replicate count
10,000, CI level 0.95, the confirmed method/scheme/series) arrive FROM CONFIG in the one
real-config test below (`test_real_config_confirmatory_shape_rereads_never_literal`),
which re-reads `configs/experiment.yaml` and `configs/seeds.yaml` at test time — no
scientific value is asserted from a literal in this file. Once
`tests/fixtures/scientific_1month/fixture_manifest.yaml` exists
(`fixtures-and-reproducibility` owns it), fixture assertion data moves there per §15.2.

INPUTS. In-memory synthetic predictions, targets, masks and registries over a synthetic
year, mirroring `test_common_masks.py`'s stand-in approach: frames are
`src.data.splits.RecordFrame` record sequences, so every stdlib-real check (guards,
declaration refusals, grid arithmetic, hashing, correlations, evidence shapes,
append-safety) runs without `pandas`/`numpy` — smoke evidence only, never governed.
Draw-dependent tests `pytest.importorskip("numpy")` and therefore SKIP BY NAME under the
stdlib shim (numpy is uninstallable here: PyPI unreachable), while the numpy-ABSENCE
refusal path is asserted in every environment by forcing the import to fail
(`sys.modules["numpy"] = None`) and asserting the `BootstrapError` names the
`numpy==1.26.4` pin. **No test touches December 2022 content, the restricted root, or a
real signature** (fixture year 2001).

WHAT NO TEST HERE DISCHARGES. WS-17, TA-13, TA-14 and TA-26 stay `Pending`; no bootstrap
has ever executed on real data; G-05/G-06 stay `Blocked`; D-27 stays unreopened and
`ABL-DIFF` keeps refusing; the G-06 abort policy for a failed widening comparison stays
the Supervisor's at G-05 (Rec 23).

Run: pytest tests/test_bootstrap.py -rs
"""

from __future__ import annotations

import ast
import dataclasses
import datetime as dt
import json
import math
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import (  # noqa: E402
    BootstrapError,
    FairnessError,
    IntegrityError,
    InverseTransformError,
    LeakageError,
    PartitionError,
    TBD_SENTINEL,
)
from src.evaluation import bootstrap as bootstrap_module  # noqa: E402
from src.evaluation.bootstrap import (  # noqa: E402
    BLOCK_SCHEME_FIXED_NONOVERLAPPING,
    CANONICAL_FORM_FACTS,
    CORRELATION_SERIES_ID,
    GENERATOR_IDENTITY,
    INTERVAL_METHOD_PERCENTILE,
    NUMPY_PIN,
    STREAM_ASSIGNMENTS,
    BootstrapResult,
    SensitivityResult,
    VectorBlockDraw,
    WideningGuardEvidence,
    build_block_grid,
    pairwise_pearson,
    percentile_interval,
    read_bootstrap_declaration,
    replicate_hash,
    serialize_bootstrap_result,
    vector_block_bootstrap,
    write_bootstrap_result,
)
from src.evaluation.masks import (  # noqa: E402
    LoadedPrediction,
    MaskRegistry,
    build_comparison_mask,
)
from src.evaluation.metrics import paired_loss_differential  # noqa: E402
from src.data.splits import RecordFrame  # noqa: E402

UTC = dt.UTC
SYNTH_YEAR = 2001  # fixture year; never 2022, so no test can brush the locked month
STATIONS = ("S1", "S2", "S3")
IDENTITY = {"phase_id": "p", "source_id": "s", "target_definition_id": "t"}

# --- apparatus constants (NOT scientific values; see the module docstring) ----------------
APPARATUS_SEED = 1234  # mechanics only; the scientific 20221201 is re-read from seeds.yaml
APPARATUS_SEED_OTHER = 5678
APPARATUS_REPLICATES = 200  # a reduced fixture-mode count (TE §15.3's analogue)
#: The planted per-day paired-difference values (benchmark error = sqrt of these), shared
#: across all three stations so the cross-station paired-error correlation is 1.0 by
#: construction and widening holds by construction (TA-14's synthetic-fixture shape).
PLANTED_DAY_DIFFS: dict[int, float] = {2: 1.0, 3: 9.0, 4: 4.0, 5: 16.0, 6: 25.0, 7: 2.25}
CORRELATION_TOLERANCE = 1e-9  # apparatus tolerance until the fixture manifest exists

#: Synthetic 7-day raw month analogue: scored range = 6 days (144 h) after a 24-h
#: embargo → 6 blocks at 24 h, 3 at 48 h (both divide; apparatus values).
MONTH_START = dt.datetime(SYNTH_YEAR, 4, 1, tzinfo=UTC)
MONTH_END = dt.datetime(SYNTH_YEAR, 4, 8, tzinfo=UTC)
EMBARGO_HOURS = 24

SYNTH_SETS: dict[str, dict[str, Any]] = {
    "setA": {
        "member_ids": ("M-A", "M-B", "M-C"),
        "model_id": "M-C",
        "benchmark_ids": ("M-A", "M-B"),
    },
}


def _declaration(**overrides: Any) -> dict[str, Any]:
    """An apparatus stand-in mirroring the transcribed experiment.yaml bootstrap shape.

    Values here exercise mechanics only; the real transcription is asserted from the
    parsed config in the one real-config test. The reduced replicate count is a fixture
    apparatus constant (control (17) is scoped to confirmatory runs).
    """
    base: dict[str, Any] = {
        "block_hours": 24,
        "replicates": APPARATUS_REPLICATES,
        "confidence_level": 0.95,
        "sensitivity_block_hours": 48,
        "seed_key": "seeds.bootstrap",
        "interval_method": INTERVAL_METHOD_PERCENTILE,
        "block_scheme": BLOCK_SCHEME_FIXED_NONOVERLAPPING,
        "correlation_series": CORRELATION_SERIES_ID,
    }
    base.update(overrides)
    return base


def _experiment(**overrides: Any) -> dict[str, Any]:
    return {"bootstrap": _declaration(**overrides)}


def _ts(day: int, hour: int, *, month: int = 4) -> str:
    return dt.datetime(SYNTH_YEAR, month, day, hour, tzinfo=UTC).isoformat()


def _truth(station: str, day: int, hour: int) -> float:
    return {"S1": 10.0, "S2": 20.0, "S3": 30.0}[station] + day + 0.5 * hour


#: Default scorable universe: six post-embargo days, four hours, three stations.
KEYS = [(s, d, h) for s in STATIONS for d in (2, 3, 4, 5, 6, 7) for h in (0, 6, 12, 18)]


def _prediction(
    model_id: str,
    keys: list[tuple[str, int, int]],
    *,
    partition_id: str = "F1",
    transform_id: str | None = "T-F1",
    error: float = 0.0,
    attrs: dict[str, Any] | None = None,
    per_row_error: dict[tuple[str, int, int], float] | None = None,
) -> LoadedPrediction:
    frame = RecordFrame(
        {
            "station": station,
            "interval_start_utc": _ts(day, hour),
            "y_hat": _truth(station, day, hour)
            + (per_row_error or {}).get((station, day, hour), error),
        }
        for station, day, hour in keys
    )
    frame.attrs.update(attrs or {})
    return LoadedPrediction(
        model_id=model_id,
        seed=None,
        frame=frame,
        target_definition_id=IDENTITY["target_definition_id"],
        phase_id=IDENTITY["phase_id"],
        source_id=IDENTITY["source_id"],
        partition_id=partition_id,
        transform_id=transform_id,  # type: ignore[arg-type]
    )


def _target(keys: list[tuple[str, int, int]]) -> RecordFrame:
    return RecordFrame(
        {
            "station_id": station,
            "interval_start_utc": _ts(day, hour),
            "vtec_tecu": _truth(station, day, hour),
        }
        for station, day, hour in keys
    )


def _planted_members(
    keys: list[tuple[str, int, int]] | None = None,
) -> list[LoadedPrediction]:
    """Model perfect; benchmarks off by sqrt(planted diff) per day — d_s(t) identical
    across stations (planted cross-station correlation 1.0; widening by construction)."""
    keys = keys if keys is not None else KEYS
    per_row = {k: math.sqrt(PLANTED_DAY_DIFFS.get(k[1], 1.0)) for k in keys}
    return [
        _prediction("M-A", keys, per_row_error=per_row),
        _prediction("M-B", keys, error=1.0),
        _prediction("M-C", keys, error=0.0),
    ]


def _registered_mask(tmp_path: Path, members: list[LoadedPrediction], target=None):
    registry = MaskRegistry(tmp_path / "mask_registry")
    mask = build_comparison_mask(
        members,
        set_id="setA",
        declared_sets=SYNTH_SETS,
        target=target if target is not None else _target(KEYS),
        feature_set_id="FS-synth",
        month_start=MONTH_START,
        month_end=MONTH_END,
        embargo_hours=EMBARGO_HOURS,
    )
    registry.register(mask)
    return mask, registry


def _by_id(members: list[LoadedPrediction]) -> dict[str, LoadedPrediction]:
    return {m.model_id: m for m in members}


def _run(
    tmp_path: Path,
    *,
    members: list[LoadedPrediction] | None = None,
    model: LoadedPrediction | None = None,
    benchmark: LoadedPrediction | None = None,
    mask=None,
    registry=None,
    seed: int = APPARATUS_SEED,
    block_hours: int = 24,
    replicates: int = APPARATUS_REPLICATES,
    evaluation_mode: str = "fixture",
    experiment: dict[str, Any] | None = None,
    target=None,
) -> BootstrapResult:
    members = members if members is not None else _planted_members()
    if mask is None or registry is None:
        mask, registry = _registered_mask(tmp_path, members, target=target)
    ids = _by_id(members)
    return vector_block_bootstrap(
        model if model is not None else ids["M-C"],
        benchmark if benchmark is not None else ids["M-A"],
        mask=mask,
        block_hours=block_hours,
        replicates=replicates,
        seed=seed,
        declared_sets=SYNTH_SETS,
        registry=registry,
        experiment=experiment if experiment is not None else _experiment(),
        evaluation_mode=evaluation_mode,
        month_start=MONTH_START,
        month_end=MONTH_END,
        embargo_hours=EMBARGO_HOURS,
    )


# =======================================================================================
# 1. The declaration: every scientific value from config (R-118, R-119; control (18))
# =======================================================================================


def test_real_config_bootstrap_and_estimand_blocks_reread_never_literal() -> None:
    """The one real-config test: the Q4 = A transcription is parsed at test time and
    cross-checked against the code's identity tokens and seeds.yaml — never a literal."""
    yaml = pytest.importorskip("yaml")
    experiment = yaml.safe_load((REPO_ROOT / "configs" / "experiment.yaml").read_text("utf-8"))
    declaration = read_bootstrap_declaration(experiment)
    # the three confirmed identity values match the implemented components (Q1/Q2/Q3 = A)
    assert declaration["interval_method"] == INTERVAL_METHOD_PERCENTILE
    assert declaration["block_scheme"] == BLOCK_SCHEME_FIXED_NONOVERLAPPING
    assert declaration["correlation_series"] == CORRELATION_SERIES_ID
    # the frozen numeric values are integers/floats resolved from config, not TBD
    for name in ("block_hours", "replicates", "confidence_level", "sensitivity_block_hours"):
        assert not isinstance(declaration[name], str)
    assert declaration["sensitivity_block_hours"] != declaration["block_hours"]
    # the seed key resolves against the real seeds.yaml (D-122; ADR-05 carve-out)
    seeds = yaml.safe_load((REPO_ROOT / "configs" / "seeds.yaml").read_text("utf-8"))
    key = str(declaration["seed_key"])
    assert key.startswith("seeds.")
    seed_value = seeds[key.split(".", 1)[1]]
    assert isinstance(seed_value, int)
    # the estimand block matches the sibling's enforced constants (drift caught by test)
    from src.evaluation.metrics import ORIENTATION, SIGN_CONVENTION_SENTENCE, WEIGHTING

    estimand = experiment["estimand"]
    assert estimand["orientation"] == ORIENTATION
    assert estimand["weighting"] == WEIGHTING
    assert estimand["sign_convention_sentence"] == SIGN_CONVENTION_SENTENCE


def test_declaration_absent_or_tbd_refuses_naming_field() -> None:
    with pytest.raises(BootstrapError) as excinfo:
        read_bootstrap_declaration({})
    assert "bootstrap" in str(excinfo.value)
    with pytest.raises(BootstrapError):
        read_bootstrap_declaration({"bootstrap": TBD_SENTINEL})
    with pytest.raises(BootstrapError) as excinfo:
        read_bootstrap_declaration({"bootstrap": _declaration(interval_method=TBD_SENTINEL)})
    assert "interval_method" in str(excinfo.value)


def test_control_18_unrecognised_method_scheme_series_refuse_naming_field() -> None:
    """TE §18.3's stop-and-report made executable: refusal, never a default (R-119)."""
    for field_name, value in (
        ("interval_method", "BCa"),
        ("block_scheme", "moving_block"),
        ("correlation_series", "raw_error_pearson"),
    ):
        with pytest.raises(BootstrapError) as excinfo:
            read_bootstrap_declaration({"bootstrap": _declaration(**{field_name: value})})
        assert field_name in str(excinfo.value)


def test_control_17_confirmatory_echo_drift_refuses(tmp_path: Path) -> None:
    """A real_data (confirmatory) call whose passed values differ from the config-declared
    ones refuses — the dead-default drift channel made visible (R-118)."""
    with pytest.raises(BootstrapError) as excinfo:
        _run(tmp_path, evaluation_mode="real_data", block_hours=12)
    assert "block_hours" in str(excinfo.value)
    second = tmp_path / "replicate_drift"
    second.mkdir()
    with pytest.raises(BootstrapError):
        _run(second, evaluation_mode="real_data", replicates=APPARATUS_REPLICATES + 1)


def test_invalid_evaluation_mode_refuses(tmp_path: Path) -> None:
    with pytest.raises(BootstrapError):
        _run(tmp_path, evaluation_mode="production")


# =======================================================================================
# 2. The block grid (R-115): fixed non-overlapping partition, derived, never truncated
# =======================================================================================


def test_grid_partition_records_scheme_and_realised_count() -> None:
    """A 31-day synthetic month less a 24-h embargo = 720 h → 30 blocks at 24 h and 15 at
    48 h — the D-28 arithmetic, derived from the window, no calendar constant here."""
    month_start = dt.datetime(SYNTH_YEAR, 12, 1, tzinfo=UTC)
    month_end = dt.datetime(SYNTH_YEAR + 1, 1, 1, tzinfo=UTC)
    grid24 = build_block_grid(
        month_start=month_start,
        month_end=month_end,
        embargo_hours=24,
        block_hours=24,
        block_scheme=BLOCK_SCHEME_FIXED_NONOVERLAPPING,
    )
    assert grid24.n_blocks == 30
    assert grid24.block_scheme == BLOCK_SCHEME_FIXED_NONOVERLAPPING
    assert len(grid24.block_boundaries_utc) == 30
    assert grid24.block_boundaries_utc[0] == grid24.scored_range_start_utc
    grid48 = build_block_grid(
        month_start=month_start,
        month_end=month_end,
        embargo_hours=24,
        block_hours=48,
        block_scheme=BLOCK_SCHEME_FIXED_NONOVERLAPPING,
    )
    assert grid48.n_blocks == 15


def test_control_7_indivisible_range_raises() -> None:
    """A 30-day month less a 24-h embargo = 696 h: 29 blocks at 24 h, INDIVISIBLE at 48 h
    (14.5) — the R-115 derivation table's April/November case, refusing by design."""
    month_start = dt.datetime(SYNTH_YEAR, 4, 1, tzinfo=UTC)
    month_end = dt.datetime(SYNTH_YEAR, 5, 1, tzinfo=UTC)
    grid24 = build_block_grid(
        month_start=month_start,
        month_end=month_end,
        embargo_hours=24,
        block_hours=24,
        block_scheme=BLOCK_SCHEME_FIXED_NONOVERLAPPING,
    )
    assert grid24.n_blocks == 29
    with pytest.raises(BootstrapError) as excinfo:
        build_block_grid(
            month_start=month_start,
            month_end=month_end,
            embargo_hours=24,
            block_hours=48,
            block_scheme=BLOCK_SCHEME_FIXED_NONOVERLAPPING,
        )
    assert "not evenly divisible" in str(excinfo.value)


def test_grid_refuses_unrecognised_scheme_naming_config_field() -> None:
    with pytest.raises(BootstrapError) as excinfo:
        build_block_grid(
            month_start=MONTH_START,
            month_end=MONTH_END,
            embargo_hours=EMBARGO_HOURS,
            block_hours=24,
            block_scheme="kunsch_moving_block",
        )
    assert "block_scheme" in str(excinfo.value)


def test_control_8_9_row_outside_scored_range_raises_through_entry_point(
    tmp_path: Path,
) -> None:
    """A masked row inside the excluded first 24 h (the '1 December row' shape) refuses at
    the grid boundary — redundancy at the locked boundary, before any draw (R-115 limb 2).
    Runs entirely pre-numpy, so it asserts under the stdlib shim too."""
    keys = KEYS + [(s, 1, 5) for s in STATIONS]  # day-1 rows inside the embargo
    members = _planted_members(keys)
    with pytest.raises(BootstrapError) as excinfo:
        _run(tmp_path, members=members, target=_target(keys))
    assert "outside the grid's scored range" in str(excinfo.value)


# =======================================================================================
# 3. Interval, hash, correlations (R-119, SD-S-01, R-121) — stdlib-real
# =======================================================================================


def test_percentile_interval_known_values_and_refusals() -> None:
    values = [float(v) for v in range(101)]  # 0..100: quantiles land exactly on 2.5/97.5
    low, high = percentile_interval(values, ci_level=0.95)
    assert low == pytest.approx(2.5)
    assert high == pytest.approx(97.5)
    with pytest.raises(BootstrapError):
        percentile_interval([], ci_level=0.95)
    with pytest.raises(BootstrapError):
        percentile_interval(values, ci_level=1.5)


def test_controls_13_14_hash_equality_and_difference_byte_grounded() -> None:
    """Same vector → identical hash (EQUALITY, not tolerance); different vector →
    different hash; draw order is load-bearing (never sorted before hashing)."""
    first = replicate_hash([1.0, 2.0, 3.5])
    second = replicate_hash([1.0, 2.0, 3.5])
    assert first == second and len(first) == 64
    assert replicate_hash([1.0, 2.0, 3.6]) != first
    assert replicate_hash([3.5, 2.0, 1.0]) != first  # order = draw order, never sorted
    assert set(CANONICAL_FORM_FACTS) == {"dtype", "byte_order", "layout", "replicate_order"}


def test_control_23_pairwise_pearson_recovers_planted_correlation() -> None:
    """Identical planted series → +1.0; an anti-correlated pair → −1.0; all pairs keyed."""
    stamps = [_ts(d, 0) for d in (2, 3, 4, 5, 6, 7)]
    base = [1.0, 9.0, 4.0, 16.0, 25.0, 2.25]
    series = {
        "S1": list(zip(stamps, base, strict=True)),
        "S2": list(zip(stamps, base, strict=True)),
        "S3": list(zip(stamps, [-v for v in base], strict=True)),
    }
    out = pairwise_pearson(series)
    assert set(out) == {"S1-S2", "S1-S3", "S2-S3"}  # all three pairs, sorted names
    assert out["S1-S2"] == pytest.approx(1.0, abs=CORRELATION_TOLERANCE)
    assert out["S1-S3"] == pytest.approx(-1.0, abs=CORRELATION_TOLERANCE)


def test_pearson_degenerate_pairs_refuse() -> None:
    stamps = [_ts(2, 0), _ts(3, 0)]
    with pytest.raises(BootstrapError):  # fewer than two common timestamps
        pairwise_pearson({"S1": [(stamps[0], 1.0)], "S2": [(stamps[1], 2.0)]})
    with pytest.raises(BootstrapError):  # zero variance
        pairwise_pearson(
            {"S1": [(s, 5.0) for s in stamps], "S2": [(s, 1.0 * i) for i, s in enumerate(stamps)]}
        )


# =======================================================================================
# 4. The vector property and the declared missing-pair rule (R-116) — stdlib-real
# =======================================================================================


def test_control_11_vector_draw_shape_cannot_represent_per_station_indices() -> None:
    """TC-19 caught structurally: ONE index sequence per replicate is the entire shape —
    no per-station index field exists to express the Q-27 anti-pattern."""
    names = [f.name for f in dataclasses.fields(VectorBlockDraw)]
    assert names == ["block_indices"]


def test_control_6_replicate_statistic_is_equal_station_not_pooled() -> None:
    """Asymmetric per-station counts: S1 has 8 rows at diff 0, S2 has 2 rows at diff 4 —
    equal-station gives 2.0, pooled row-weighting 0.8; the replicate path must match the
    estimand's weighting (R-114 check 5)."""
    block_values = {"S1": [[0.0] * 8], "S2": [[4.0, 4.0]]}
    draw = VectorBlockDraw(block_indices=(0,))
    stat = bootstrap_module._replicate_statistic(draw, block_values, window="[w)")
    assert stat == pytest.approx((0.0 + 4.0) / 2)
    assert stat != pytest.approx((8 * 0.0 + 2 * 4.0) / 10)


def test_control_10_zero_support_station_raises_naming_it() -> None:
    block_values = {"S1": [[1.0], [2.0]], "S2": [[3.0], []]}  # S2 empty in block 1
    draw = VectorBlockDraw(block_indices=(1, 1))
    with pytest.raises(BootstrapError) as excinfo:
        bootstrap_module._replicate_statistic(draw, block_values, window="[w)")
    assert "S2" in str(excinfo.value)


# =======================================================================================
# 5. Per-entry guard controls THROUGH vector_block_bootstrap (R-113; SD-S-02's half) —
#    all raise before any draw, so they assert under the stdlib shim too
# =======================================================================================


def test_control_15_missing_seed_is_typeerror_by_signature(tmp_path: Path) -> None:
    members = _planted_members()
    mask, registry = _registered_mask(tmp_path, members)
    ids = _by_id(members)
    with pytest.raises(TypeError):
        vector_block_bootstrap(  # type: ignore[call-arg]  # the omission IS the test
            ids["M-C"],
            ids["M-A"],
            mask=mask,
            declared_sets=SYNTH_SETS,
            registry=registry,
            experiment=_experiment(),
            evaluation_mode="fixture",
            month_start=MONTH_START,
            month_end=MONTH_END,
            embargo_hours=EMBARGO_HOURS,
        )


def test_per_entry_stampless_prediction_raises_leakage(tmp_path: Path) -> None:
    members = _planted_members()
    mask, registry = _registered_mask(tmp_path, members)
    stampless = _prediction("M-C", KEYS, transform_id=None)
    with pytest.raises(LeakageError):
        _run(tmp_path, members=members, mask=mask, registry=registry, model=stampless)


def test_per_entry_unregistered_mask_raises_fairness(tmp_path: Path) -> None:
    members = _planted_members()
    registry = MaskRegistry(tmp_path / "mask_registry")  # nothing registered
    mask = build_comparison_mask(
        members,
        set_id="setA",
        declared_sets=SYNTH_SETS,
        target=_target(KEYS),
        feature_set_id="FS-synth",
        month_start=MONTH_START,
        month_end=MONTH_END,
        embargo_hours=EMBARGO_HOURS,
    )
    with pytest.raises(FairnessError):
        _run(tmp_path, members=members, mask=mask, registry=registry)


def test_per_entry_mask_mismatched_partition_set_raises_fairness(tmp_path: Path) -> None:
    """The sixth guard through THIS entry point: a self-consistent member set scored
    against a mask recorded for a different partition (W-4's third failure)."""
    members = _planted_members()
    mask, registry = _registered_mask(tmp_path, members)
    wrong = [
        _prediction(m.model_id, KEYS, partition_id="F2", error=0.0 if m.model_id == "M-C" else 1.0)
        for m in members
    ]
    ids = _by_id(wrong)
    with pytest.raises(FairnessError):
        _run(
            tmp_path,
            members=wrong,
            mask=mask,
            registry=registry,
            model=ids["M-C"],
            benchmark=ids["M-A"],
        )


def test_control_2_member_partition_mismatch_raises_partition_error(tmp_path: Path) -> None:
    """Asserted BY DISCRIMINATED TYPE (Rec 8): a member partition_id mismatch is
    PartitionError, never LeakageError — R-105-as-corrected matching R-92."""
    members = _planted_members()
    mask, registry = _registered_mask(tmp_path, members)
    drifted = _prediction("M-A", KEYS, partition_id="F2", error=1.0)
    with pytest.raises(PartitionError):
        _run(tmp_path, members=members, mask=mask, registry=registry, benchmark=drifted)


def test_per_entry_receiptless_dec_call_refuses_fail_closed(tmp_path: Path) -> None:
    """A DEC-partition mask with no LockedContext never computes (R-113 precondition 3)."""
    members = [
        _prediction(m, KEYS, partition_id="DEC", error=0.0 if m == "M-C" else 1.0)
        for m in SYNTH_SETS["setA"]["member_ids"]
    ]
    mask, registry = _registered_mask(tmp_path, members)
    ids = _by_id(members)
    with pytest.raises(IntegrityError) as excinfo:
        _run(
            tmp_path,
            members=members,
            mask=mask,
            registry=registry,
            model=ids["M-C"],
            benchmark=ids["M-A"],
        )
    assert "LockedContext" in str(excinfo.value)


def test_per_entry_uninverted_abl_diff_raises_inverse_transform(tmp_path: Path) -> None:
    members = _planted_members()
    mask, registry = _registered_mask(tmp_path, members)
    abl = _prediction("M-C", KEYS, attrs={"ablation_id": "ABL-DIFF"})
    with pytest.raises(InverseTransformError) as excinfo:
        _run(tmp_path, members=members, mask=mask, registry=registry, model=abl)
    assert "D-27" in str(excinfo.value)


def test_control_5_point_estimate_inequality_raises(tmp_path: Path) -> None:
    """The exact-equality control (R-114; §13.7): a paired_loss_differential scalar that
    differs by ANY amount from the precomputed-series estimate raises. Drift is injected
    by patching the module's reference — the arithmetic itself has one copy to drift."""
    members = _planted_members()
    mask, registry = _registered_mask(tmp_path, members)
    real = paired_loss_differential(
        _by_id(members)["M-C"],
        _by_id(members)["M-A"],
        mask=mask,
        declared_sets=SYNTH_SETS,
        registry=registry,
    )
    drifted = dataclasses.replace(real, scalar=real.scalar + 1e-12)
    original = bootstrap_module.paired_loss_differential
    bootstrap_module.paired_loss_differential = lambda *a, **k: drifted
    try:
        with pytest.raises(BootstrapError) as excinfo:
            _run(tmp_path, members=members, mask=mask, registry=registry)
        assert "EXACTLY" in str(excinfo.value)
    finally:
        bootstrap_module.paired_loss_differential = original


def test_numpy_absence_refuses_naming_the_pin(tmp_path: Path) -> None:
    """The lazy-import refusal (the sklearn/FU-1 precedent): with every stdlib-real step
    green — guards, declaration, equality control, grid, correlations — the draw step
    refuses naming the pinned numpy==1.26.4, in EVERY environment (forced here)."""
    saved = sys.modules.get("numpy", "<absent>")
    sys.modules["numpy"] = None  # forces `import numpy` to fail regardless of install
    try:
        with pytest.raises(BootstrapError) as excinfo:
            _run(tmp_path)
        assert NUMPY_PIN in str(excinfo.value)
        assert "numpy==1.26.4" in str(excinfo.value)
    finally:
        if saved == "<absent>":
            del sys.modules["numpy"]
        else:
            sys.modules["numpy"] = saved


# =======================================================================================
# 6. Evidence shapes (SD-S-01; R-118; R-120; R-121) — constructor-enforced, stdlib-real
# =======================================================================================


def _guard(**overrides: Any) -> WideningGuardEvidence:
    base: dict[str, Any] = dict(
        vector_width=2.0,
        comparator_width=1.0,
        comparator_replicates=APPARATUS_REPLICATES,
        comparator_derived_seed=f"SeedSequence({APPARATUS_SEED}, spawn_key=(1,))",
        passed=True,
        evaluation_mode="fixture",
        disclosure=None,
    )
    base.update(overrides)
    return WideningGuardEvidence(**base)


def _sensitivity(**overrides: Any) -> SensitivityResult:
    base: dict[str, Any] = dict(
        label="sensitivity",
        block_hours=48,
        n_blocks=3,
        ci_lower=0.0,
        ci_upper=1.0,
        ci_level=0.95,
        derived_seed=f"SeedSequence({APPARATUS_SEED}, spawn_key=(0,))",
        run_id=None,
    )
    base.update(overrides)
    return SensitivityResult(**base)


def _result(**overrides: Any) -> BootstrapResult:
    vector = tuple(float(v) for v in range(APPARATUS_REPLICATES))
    base: dict[str, Any] = dict(
        ci_lower=0.0,
        ci_upper=1.0,
        ci_level=0.95,
        interval_method=INTERVAL_METHOD_PERCENTILE,
        block_hours=24,
        block_scheme=BLOCK_SCHEME_FIXED_NONOVERLAPPING,
        replicates=APPARATUS_REPLICATES,
        point_estimate=0.5,
        per_station_components={"S1": 0.5, "S2": 0.5, "S3": 0.5},
        seed=APPARATUS_SEED,
        seed_key="seeds.bootstrap",
        generator_identity=GENERATOR_IDENTITY,
        replicate_hash=replicate_hash(vector),
        canonical_form=dict(CANONICAL_FORM_FACTS),
        stream_assignments=dict(STREAM_ASSIGNMENTS),
        replicate_vector=vector,
        widening_guard=_guard(),
        pairwise_correlations={"S1-S2": 1.0, "S1-S3": 1.0, "S2-S3": 1.0},
        correlation_series=CORRELATION_SERIES_ID,
        sensitivity=_sensitivity(),
        mask_id="m",
        set_id="setA",
        partition_id="F1",
        model_id="M-C",
        benchmark_id="M-A",
        n_blocks=6,
        evaluation_mode="fixture",
    )
    base.update(overrides)
    return BootstrapResult(**base)


def test_control_21_missing_evidence_fields_fail_at_construction() -> None:
    """A BootstrapResult missing any canonical-form fact, the generator identity, the seed
    key, a stream assignment, or part of its replicate vector is UNCONSTRUCTIBLE."""
    incomplete_form = {k: v for k, v in CANONICAL_FORM_FACTS.items() if k != "dtype"}
    for overrides in (
        {"canonical_form": incomplete_form},
        {"canonical_form": {**CANONICAL_FORM_FACTS, "byte_order": "big-endian"}},
        {"generator_identity": ""},
        {"seed_key": ""},
        {"stream_assignments": {"primary": "block-index draws"}},
        {"replicate_vector": (1.0, 2.0)},  # not materialised in full
        {"pairwise_correlations": {}},
        {"correlation_series": "raw_error_pearson"},
    ):
        with pytest.raises(BootstrapError):
            _result(**overrides)


def test_control_16_sensitivity_labelled_and_never_merged() -> None:
    with pytest.raises(BootstrapError):
        _sensitivity(label="confirmatory")
    with pytest.raises(BootstrapError):  # 48-h result merged onto the 24-h field shape
        _result(sensitivity=_sensitivity(block_hours=24))


def test_control_19_fixture_mode_widening_failure_raises_at_construction() -> None:
    """The fixture-time raise: a narrower vector interval on the synthetic fixture is
    unrepresentable as serialized fixture-mode evidence (R-120 as amended, Rec 23)."""
    with pytest.raises(BootstrapError) as excinfo:
        _guard(vector_width=0.5, comparator_width=1.0, passed=False)
    assert "NARROWER" in str(excinfo.value).upper()
    _guard(vector_width=2.0, comparator_width=1.0, passed=True)  # passing fixture constructs


def test_control_22_real_data_failure_without_disclosure_fails() -> None:
    """The mandatory disclosure proven mandatory: absent, or missing the measured
    correlations, the failed real-data evidence is unconstructible."""
    with pytest.raises(BootstrapError):
        _guard(evaluation_mode="real_data", passed=False, disclosure=None)
    incomplete = {
        "vector_width": 0.5,
        "comparator_width": 1.0,
        "comparator_replicates": APPARATUS_REPLICATES,
        "comparator_derived_seed": "SeedSequence(1234, spawn_key=(1,))",
        "block_hours": 24,
        "block_scheme": BLOCK_SCHEME_FIXED_NONOVERLAPPING,
        "n_blocks": 6,
        # pairwise_correlations deliberately absent — the discriminating quantity
    }
    with pytest.raises(BootstrapError) as excinfo:
        _guard(
            evaluation_mode="real_data",
            passed=False,
            vector_width=0.5,
            comparator_width=1.0,
            disclosure=incomplete,
        )
    assert "pairwise_correlations" in str(excinfo.value)
    complete = {**incomplete, "pairwise_correlations": {"S1-S2": 0.9}}
    evidence = _guard(
        evaluation_mode="real_data",
        passed=False,
        vector_width=0.5,
        comparator_width=1.0,
        disclosure=complete,
    )
    assert evidence.disclosure is not None


def test_control_20_quarantine_comparator_never_a_reported_interval() -> None:
    """The Q-27 variant is width-only everywhere: the evidence shape carries no comparator
    bounds or CI level, and the serialized form carries none either (R-120 point 3)."""
    guard_fields = {f.name for f in dataclasses.fields(WideningGuardEvidence)}
    assert not any("ci" in name or "lower" in name or "upper" in name for name in guard_fields)
    serialized = serialize_bootstrap_result(_result())
    guard_block = serialized["widening_guard"]
    assert set(guard_block) == {
        "vector_width",
        "comparator_width",
        "comparator_replicates",
        "comparator_derived_seed",
        "passed",
        "evaluation_mode",
        "disclosure",
    }


def test_append_safety_second_write_refuses_and_evidence_is_machine_readable(
    tmp_path: Path,
) -> None:
    """NFR-AUD-01: a rerun writes a NEW result — the second write of the same path refuses;
    the serialized artifact carries WS-17's evidence surface machine-readably."""
    result = _result()
    path = tmp_path / "bootstrap_setA.json"
    write_bootstrap_result(result, path)
    with pytest.raises(BootstrapError):
        write_bootstrap_result(result, path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["replicate_hash"] == result.replicate_hash
    assert payload["canonical_form"] == dict(CANONICAL_FORM_FACTS)
    assert payload["generator_identity"] == GENERATOR_IDENTITY
    assert payload["seed_key"] == "seeds.bootstrap"
    assert payload["stream_assignments"]["child_0"] == STREAM_ASSIGNMENTS["child_0"]
    assert len(payload["replicate_vector"]) == payload["replicates"]
    assert payload["sensitivity"]["label"] == "sensitivity"


# =======================================================================================
# 7. Import discipline: numpy lazy, no new package edges (TE §12; D-27) — evidence by AST
# =======================================================================================


def test_bootstrap_module_imports_numpy_lazily_and_adds_no_package_edge() -> None:
    """`numpy` never appears at module scope (lazy import, refusal names the pin), and no
    `src.features`/`src.models`/`src.external`/`src.gnss` import exists anywhere in
    bootstrap.py — module scope OR function bodies (no new import edge; R-112)."""
    path = REPO_ROOT / "src" / "evaluation" / "bootstrap.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    forbidden = ("src.features", "src.models", "src.external", "src.gnss")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import | ast.ImportFrom):
            names = (
                [node.module or ""]
                if isinstance(node, ast.ImportFrom)
                else [a.name for a in node.names]
            )
            for name in names:
                assert not any(
                    name == f or name.startswith(f + ".") for f in forbidden
                ), name
    for node in tree.body:  # module scope: numpy must not appear here (lazy only)
        if isinstance(node, ast.Import | ast.ImportFrom):
            names = (
                [node.module or ""]
                if isinstance(node, ast.ImportFrom)
                else [a.name for a in node.names]
            )
            for name in names:
                assert not name.startswith("numpy"), "numpy must be imported lazily"


# =======================================================================================
# 8. Draw-dependent checks (numpy) — skip BY NAME under the stdlib shim
# =======================================================================================


def test_controls_13_14_same_seed_reproduces_hash_exactly_different_seed_differs(
    tmp_path: Path,
) -> None:
    pytest.importorskip("numpy")
    first = _run(tmp_path)
    second_dir = tmp_path / "again"
    second_dir.mkdir()
    second = _run(second_dir)
    assert first.replicate_hash == second.replicate_hash  # equality, not tolerance (WS-17)
    assert first.replicate_vector == second.replicate_vector
    other_dir = tmp_path / "other"
    other_dir.mkdir()
    other = _run(other_dir, seed=APPARATUS_SEED_OTHER)
    assert other.replicate_hash != first.replicate_hash


def test_stream_isolation_primary_hash_matches_direct_root_stream(tmp_path: Path) -> None:
    """Removing the other consumers cannot perturb the primary draws: the full run's
    replicate vector equals a direct recomputation from the ROOT stream alone (R-117)."""
    np = pytest.importorskip("numpy")
    result = _run(tmp_path)
    members = _planted_members()
    mask, _registry = _registered_mask(tmp_path / "iso", members)
    from src.evaluation.metrics import paired_difference_series

    series = paired_difference_series("M-C", "M-A", mask)
    grid = build_block_grid(
        month_start=MONTH_START,
        month_end=MONTH_END,
        embargo_hours=EMBARGO_HOURS,
        block_hours=24,
        block_scheme=BLOCK_SCHEME_FIXED_NONOVERLAPPING,
    )
    block_values = bootstrap_module._block_values(series, grid)
    rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence(APPARATUS_SEED)))
    indices = rng.integers(0, grid.n_blocks, size=(APPARATUS_REPLICATES, grid.n_blocks))
    direct = [
        bootstrap_module._replicate_statistic(
            VectorBlockDraw(block_indices=tuple(int(i) for i in row)),
            block_values,
            window="[w)",
        )
        for row in indices
    ]
    assert replicate_hash(direct) == result.replicate_hash


def test_widening_holds_on_planted_fixture_and_evidence_records_the_run(
    tmp_path: Path,
) -> None:
    """The TA-14 synthetic shape: planted cross-station correlation 1.0, gaps injected in
    one station — the vector interval is WIDER than the quarantined within-station
    comparator's (the must-not-fire pass of the fixture-time raise; the comparator's
    narrower width is the Q-27 anti-pattern caught behaviourally), the correlations are
    recovered, the scheme/realised block count and stream assignments are recorded, and
    the sensitivity is a distinct labelled 48-hour field."""
    pytest.importorskip("numpy")
    keys = [k for k in KEYS if k != ("S2", 4, 12)]  # the injected gap (ragged, supported)
    members = _planted_members(keys)
    result = _run(tmp_path, members=members, target=_target(keys))
    guard = result.widening_guard
    assert guard.passed is True and guard.evaluation_mode == "fixture"
    assert guard.comparator_width < guard.vector_width  # within-station narrows — caught
    assert guard.comparator_replicates == result.replicates  # like-for-like (Rec 24)
    assert "spawn_key=(1,)" in guard.comparator_derived_seed
    assert guard.disclosure is None  # disclosure exists only on a failed real-data run
    for pair in ("S1-S2", "S1-S3", "S2-S3"):
        assert result.pairwise_correlations[pair] == pytest.approx(
            1.0, abs=1e-6
        )  # planted correlation recovered (apparatus tolerance)
    assert result.block_scheme == BLOCK_SCHEME_FIXED_NONOVERLAPPING  # Rec 26: recorded
    assert result.n_blocks == 6  # realised count on the 144-h apparatus window
    assert result.sensitivity.label == "sensitivity"
    assert result.sensitivity.block_hours == 48 and result.block_hours == 24
    assert result.sensitivity.n_blocks == 3
    assert "spawn_key=(0,)" in result.sensitivity.derived_seed
    assert result.generator_identity == GENERATOR_IDENTITY
    assert len(result.replicate_vector) == result.replicates
    # the full-data point estimate equals the estimand scalar exactly (R-114, in situ)
    ids = _by_id(members)
    mask, registry = _registered_mask(tmp_path / "eq", members, target=_target(keys))
    estimand = paired_loss_differential(
        ids["M-C"], ids["M-A"], mask=mask, declared_sets=SYNTH_SETS, registry=registry
    )
    assert result.point_estimate == estimand.scalar


def test_control_10_zero_support_replicate_raises_through_draws(tmp_path: Path) -> None:
    """S3 carries rows in only one of two blocks: some replicate's drawn blocks exclude it
    and the run refuses naming the station (R-116's structural guard, via real draws)."""
    pytest.importorskip("numpy")
    # 3-day raw window → 2 scored days → 2 blocks at 24 h; sensitivity 48 h → 1 block
    month_start = dt.datetime(SYNTH_YEAR, 5, 1, tzinfo=UTC)
    month_end = dt.datetime(SYNTH_YEAR, 5, 4, tzinfo=UTC)

    def ts(day: int, hour: int) -> str:
        return dt.datetime(SYNTH_YEAR, 5, day, hour, tzinfo=UTC).isoformat()

    keys_full = [(s, d, h) for s in ("S1", "S2") for d in (2, 3) for h in (0, 6, 12)]
    keys_s3 = [("S3", 2, h) for h in (0, 6, 12)]  # S3 in block 0 only
    keys = keys_full + keys_s3
    per_row = {k: 1.0 + 0.25 * k[1] + 0.05 * k[2] for k in keys}  # varying diffs
    members = [
        _prediction("M-A", keys, per_row_error=per_row),
        _prediction("M-B", keys, error=1.0),
        _prediction("M-C", keys, error=0.0),
    ]
    for member in members:
        for row in member.frame:
            day = int(row["interval_start_utc"][8:10])
            hour = int(row["interval_start_utc"][11:13])
            row["interval_start_utc"] = ts(day, hour)
    target = RecordFrame(
        {
            "station_id": s,
            "interval_start_utc": ts(d, h),
            "vtec_tecu": _truth(s, d, h),
        }
        for s, d, h in keys
    )
    registry = MaskRegistry(tmp_path / "mask_registry")
    mask = build_comparison_mask(
        members,
        set_id="setA",
        declared_sets=SYNTH_SETS,
        target=target,
        feature_set_id="FS-synth",
        month_start=month_start,
        month_end=month_end,
        embargo_hours=EMBARGO_HOURS,
    )
    registry.register(mask)
    ids = _by_id(members)
    with pytest.raises(BootstrapError) as excinfo:
        vector_block_bootstrap(
            ids["M-C"],
            ids["M-A"],
            mask=mask,
            block_hours=24,
            replicates=APPARATUS_REPLICATES,
            seed=APPARATUS_SEED,
            declared_sets=SYNTH_SETS,
            registry=registry,
            experiment=_experiment(),
            evaluation_mode="fixture",
            month_start=month_start,
            month_end=month_end,
            embargo_hours=EMBARGO_HOURS,
        )
    assert "S3" in str(excinfo.value)


def test_real_config_confirmatory_shape_rereads_never_literal(tmp_path: Path) -> None:
    """The ONE confirmatory-shaped run: seed, block length, replicate count and CI level
    all RE-READ from configs/seeds.yaml and configs/experiment.yaml at test time (TC-03e —
    the suite itself proves the no-inlined-constant rule), on a synthetic 31-day window
    whose scored range mirrors the D-28 arithmetic (30 blocks / 15 at the sensitivity).
    Control (17)'s positive half: the recorded values echo the config-declared ones."""
    np = pytest.importorskip("numpy")
    yaml = pytest.importorskip("yaml")
    del np
    experiment = yaml.safe_load((REPO_ROOT / "configs" / "experiment.yaml").read_text("utf-8"))
    seeds = yaml.safe_load((REPO_ROOT / "configs" / "seeds.yaml").read_text("utf-8"))
    declaration = read_bootstrap_declaration(experiment)
    seed = seeds[str(declaration["seed_key"]).split(".", 1)[1]]

    month_start = dt.datetime(SYNTH_YEAR, 12, 1, tzinfo=UTC)
    month_end = dt.datetime(SYNTH_YEAR + 1, 1, 1, tzinfo=UTC)

    def ts(day: int) -> str:
        return dt.datetime(SYNTH_YEAR, 12, day, 0, tzinfo=UTC).isoformat()

    days = list(range(2, 32))
    keys = [(s, d, 0) for s in STATIONS for d in days]
    per_row = {k: 1.0 + 0.1 * k[1] for k in keys}  # day-varying planted differences
    members = [
        _prediction("M-A", keys, per_row_error=per_row),
        _prediction("M-B", keys, error=1.0),
        _prediction("M-C", keys, error=0.0),
    ]
    for member in members:
        for row in member.frame:
            row["interval_start_utc"] = ts(int(row["interval_start_utc"][8:10]))
    target = RecordFrame(
        {"station_id": s, "interval_start_utc": ts(d), "vtec_tecu": _truth(s, d, 0)}
        for s, d, _ in keys
    )
    registry = MaskRegistry(tmp_path / "mask_registry")
    mask = build_comparison_mask(
        members,
        set_id="setA",
        declared_sets=SYNTH_SETS,
        target=target,
        feature_set_id="FS-synth",
        month_start=month_start,
        month_end=month_end,
        embargo_hours=24,
    )
    registry.register(mask)
    ids = _by_id(members)
    result = vector_block_bootstrap(
        ids["M-C"],
        ids["M-A"],
        mask=mask,
        block_hours=int(declaration["block_hours"]),
        replicates=int(declaration["replicates"]),
        seed=int(seed),
        declared_sets=SYNTH_SETS,
        registry=registry,
        experiment=experiment,
        evaluation_mode="real_data",
        month_start=month_start,
        month_end=month_end,
        embargo_hours=24,
    )
    # control (17): recorded values equal the config-declared ones on a confirmatory run
    assert result.block_hours == int(declaration["block_hours"])
    assert result.replicates == int(declaration["replicates"])
    assert result.ci_level == float(declaration["confidence_level"])
    assert result.interval_method == str(declaration["interval_method"])
    assert result.seed == int(seed) and result.seed_key == str(declaration["seed_key"])
    assert result.n_blocks == 30  # the D-28-mirroring realised count, derived not carried
    assert result.sensitivity.n_blocks == 15
    assert len(result.replicate_vector) == int(declaration["replicates"])
    assert len(result.replicate_hash) == 64
    # the percentile interval re-derives from the materialised replicate vector alone
    low, high = percentile_interval(
        result.replicate_vector, ci_level=float(declaration["confidence_level"])
    )
    assert (low, high) == (result.ci_lower, result.ci_upper)
    # append-safe emission of the machine-readable evidence (WS-17's surface; Pending)
    out = write_bootstrap_result(result, tmp_path / "bootstrap_confirmatory_shape.json")
    assert out.is_file()
