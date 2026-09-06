"""WS-16 / TA-11: masks, estimand, locked chokepoint, honesty — every hard rule's control.

PURPOSE. `evaluation-and-comparison` R-103 ... R-112, each with the negative control that
proves the violation is CAUGHT (team.md § Testing Posture): controls (1) and (3)-(32) as
owned by this unit ((2) is vacated — relocated to `src/features` with R-103's narrowing),
the per-entry guard controls of SD-C-01 (Q3 = A: for EACH public entry point, one control
pushes a violating input through THAT entry point and asserts the raise), the Q4 = A
write-once-manifest refusal, and the three must-NOT-fire controls (the
all-DEC-stamps-vs-DEC-mask pass, the `untransformed` B-01/C-01 pass, the
coverage-audit-purpose pass). Member counts 5 / 2 / 3 are RE-READ from
`configs/experiment.yaml` (the one test that touches the real config builds its
expectations from the parsed file at test time); no declared member list is asserted
against a literal from this file.

INPUTS. In-memory synthetic predictions, targets, masks and registries over a synthetic
year, mirroring `test_models_smoke.py`'s stand-in approach: frames are
`src.data.splits.RecordFrame` record sequences (the plain-record fallback the governed
frame helpers fall back to on a stdlib-only interpreter), so every check runs without
`pandas`/`numpy` — smoke evidence only, never governed. **No test touches December 2022
content, the restricted root, or a real signature**: locked-path tests run against
`tmp_path` roots through `locked_test._repo_root`'s documented seam, and the D-28 window
statement is verified by pure date arithmetic, not by reading anything.

WHAT NO TEST HERE DISCHARGES. WS-16, TA-11 and TA-18 stay `Pending`; FR-P1-05-7 stays
`Pending` (row approved under D-32, never run); FR-P1-05-17 stays `UNTESTED`; G-05/G-06
stay `Blocked`; D-27 stays unreopened and `ABL-DIFF` keeps refusing.

Run: pytest tests/test_common_masks.py -rs
"""

from __future__ import annotations

import ast
import dataclasses
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import (  # noqa: E402
    FairnessError,
    IntegrityError,
    InverseTransformError,
    LeakageError,
    LockedTestError,
    PartitionError,
)
from src.data.splits import RecordFrame  # noqa: E402
from src.evaluation.guards import (  # noqa: E402
    UNTRANSFORMED,
    require_declared_membership,
    require_locked_receipt,
    require_mask_member_alignment,
    require_partition_agreement,
    require_stamps,
    require_target_space,
    resolve_inverse,
    scored_window_statement,
)
from src.evaluation.masks import (  # noqa: E402
    ComparisonMask,
    LoadedPrediction,
    MaskRegistry,
    assert_mask_id_reproduces,
    assert_reporting_surface,
    build_comparison_mask,
    compute_mask_id,
    prediction_from_payload,
    read_comparison_sets,
)
from src.evaluation.metrics import (  # noqa: E402
    PHASE2_NOT_INDEPENDENT_STATEMENT,
    SIGN_CONVENTION_SENTENCE,
    SPATIAL_REPRESENTATIVENESS_SENTENCE,
    EstimandResult,
    LockedContext,
    assert_metrics_artifact,
    build_metrics_artifact,
    paired_loss_differential,
    write_metrics_artifact,
)

UTC = dt.UTC
SYNTH_YEAR = 2001  # fixture year; never 2022, so no test can brush the locked month
STATIONS = ("S1", "S2", "S3")
IDENTITY = {"phase_id": "p", "source_id": "s", "target_definition_id": "t"}

# Synthetic declared sets — FIXTURE declarations exercising the mechanics, never an
# assertion about the real config (the real memberships are re-read from
# configs/experiment.yaml in the one config-reading test below). The gim/iri/tier3
# fixtures reuse the identity tokens the disclosure logic keys on (B-01/C-01/M-04/M-05),
# which are identities, not values.
SYNTH_SETS: dict[str, dict[str, Any]] = {
    "setA": {
        "member_ids": ("M-A", "M-B", "M-C"),
        "model_id": "M-C",
        "benchmark_ids": ("M-A", "M-B"),
    },
    "setB": {"member_ids": ("M-C", "X-1"), "model_id": "M-C", "benchmark_ids": ("X-1",)},
    "gimset": {"member_ids": ("M-C", "C-01"), "model_id": "M-C", "benchmark_ids": ("C-01",)},
    "iriset": {"member_ids": ("M-C", "B-01"), "model_id": "M-C", "benchmark_ids": ("B-01",)},
    "tier3s": {
        "member_ids": ("M-04", "M-05", "M-06"),
        "model_id": "M-06",
        "benchmark_ids": ("M-04", "M-05"),
    },
}

MONTH_START = dt.datetime(SYNTH_YEAR, 4, 1, tzinfo=UTC)
MONTH_END = dt.datetime(SYNTH_YEAR, 5, 1, tzinfo=UTC)
EMBARGO_HOURS = 24
DEC_MONTH_START = dt.datetime(SYNTH_YEAR, 12, 1, tzinfo=UTC)
DEC_MONTH_END = dt.datetime(SYNTH_YEAR + 1, 1, 1, tzinfo=UTC)


def _ts(day: int, hour: int, *, month: int = 4) -> str:
    return dt.datetime(SYNTH_YEAR, month, day, hour, tzinfo=UTC).isoformat()


def _truth(station: str, day: int, hour: int) -> float:
    return {"S1": 10.0, "S2": 20.0, "S3": 30.0}[station] + day + 0.5 * hour


def _target(keys: list[tuple[str, int, int]], *, month: int = 4) -> RecordFrame:
    return RecordFrame(
        {
            "station_id": station,
            "interval_start_utc": _ts(day, hour, month=month),
            "vtec_tecu": _truth(station, day, hour),
        }
        for station, day, hour in keys
    )


def _prediction(
    model_id: str,
    keys: list[tuple[str, int, int]],
    *,
    partition_id: str = "F1",
    transform_id: str | None = "T-F1",
    error: float = 0.0,
    month: int = 4,
    attrs: dict[str, Any] | None = None,
    per_row_error: dict[tuple[str, int, int], float] | None = None,
) -> LoadedPrediction:
    frame = RecordFrame(
        {
            "station": station,
            "interval_start_utc": _ts(day, hour, month=month),
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


#: The default scorable universe: two days after the embargo, three hours, three stations.
KEYS = [(s, d, h) for s in STATIONS for d in (2, 3) for h in (0, 1, 2)]


def _members(set_id: str, **overrides: LoadedPrediction) -> list[LoadedPrediction]:
    """Default fixture: the set's model is perfect (error 0), benchmarks are off by 1 —
    a known-sign fixture (benchmark minus model positive) unless a test overrides it."""
    declared = SYNTH_SETS[set_id]
    out = []
    for member_id in declared["member_ids"]:
        if member_id in overrides:
            out.append(overrides[member_id])
            continue
        transform = UNTRANSFORMED if member_id in ("B-01", "C-01") else "T-F1"
        error = 0.0 if member_id == declared["model_id"] else 1.0
        out.append(_prediction(member_id, KEYS, transform_id=transform, error=error))
    return out


def _mask(set_id: str = "setA", *, members=None, target=None, **kwargs: Any) -> ComparisonMask:
    return build_comparison_mask(
        members if members is not None else _members(set_id),
        set_id=set_id,
        declared_sets=SYNTH_SETS,
        target=target if target is not None else _target(KEYS),
        feature_set_id="FS-synth",
        month_start=kwargs.pop("month_start", MONTH_START),
        month_end=kwargs.pop("month_end", MONTH_END),
        embargo_hours=kwargs.pop("embargo_hours", EMBARGO_HOURS),
        **kwargs,
    )


def _registered(tmp_path: Path, set_id: str = "setA", **mask_kwargs: Any):
    registry = MaskRegistry(tmp_path / "mask_registry")
    mask = _mask(set_id, **mask_kwargs)
    registry.register(mask)
    return mask, registry


# =======================================================================================
# 1. The declared sets: configuration, not source (R-106; Q1 = A)
# =======================================================================================


def test_real_comparison_sets_reread_from_config_never_literal() -> None:
    """The one real-config test: counts and containments derived from the parsed file at
    test time (5 / 2 / 3 are re-read, not asserted from a literal member list here)."""
    yaml = pytest.importorskip("yaml")
    parsed = yaml.safe_load((REPO_ROOT / "configs" / "experiment.yaml").read_text("utf-8"))
    snapshot = type("S", (), {"experiment": parsed})()
    declared = read_comparison_sets(snapshot)
    raw = parsed["comparison_sets"]
    expected_ids = [k for k in raw if k not in ("decision", "source")]
    assert sorted(declared) == sorted(expected_ids)
    for set_id in expected_ids:
        expected_members = [str(m) for m in raw[set_id]["member_ids"]]
        entry = declared[set_id]
        # counts re-read from config and compared with the enumerated list itself
        assert len(entry["member_ids"]) == len(expected_members)
        assert len(set(entry["member_ids"])) == len(entry["member_ids"])  # no duplicate
        assert entry["model_id"] in entry["member_ids"]
        assert set(entry["benchmark_ids"]) <= set(entry["member_ids"])
        assert entry["model_id"] not in entry["benchmark_ids"]
        # a mask over the REAL declared membership builds with exactly that many members
        members = [
            _prediction(m, KEYS, transform_id=UNTRANSFORMED if m in ("B-01", "C-01") else "T-F1")
            for m in entry["member_ids"]
        ]
        mask = build_comparison_mask(
            members,
            set_id=set_id,
            declared_sets=declared,
            target=_target(KEYS),
            feature_set_id="FS-synth",
            month_start=MONTH_START,
            month_end=MONTH_END,
            embargo_hours=EMBARGO_HOURS,
        )
        assert len(mask.member_ids) == len(expected_members)


def test_comparison_sets_absent_refuses_naming_the_field() -> None:
    snapshot = type("S", (), {"experiment": {}})()
    with pytest.raises(IntegrityError) as excinfo:
        read_comparison_sets(snapshot)
    assert "comparison_sets" in str(excinfo.value)


# =======================================================================================
# 2. The guards, per condition (R-104, R-105; SD-C-01's discriminating rule)
# =======================================================================================


def test_control_6_none_stamp_raises_leakage() -> None:
    stampless = _prediction("M-A", KEYS, transform_id=None)
    with pytest.raises(LeakageError):
        require_stamps([stampless])
    no_partition = dataclasses.replace(_prediction("M-A", KEYS), partition_id=None)
    with pytest.raises(LeakageError):
        require_stamps([no_partition])


def test_transform_outside_recorded_set_raises_leakage() -> None:
    foreign = _prediction("M-A", KEYS, transform_id="T-F2")
    with pytest.raises(LeakageError):
        require_stamps([foreign], recorded_transform_ids=("T-F1", UNTRANSFORMED))


def test_control_5_partition_mismatch_raises_partition_error() -> None:
    a = _prediction("M-A", KEYS, partition_id="F1")
    b = _prediction("M-B", KEYS, partition_id="F2")
    with pytest.raises(PartitionError):
        require_partition_agreement([a, b])


def test_control_7_member_vs_mask_partition_raises_fairness(tmp_path: Path) -> None:
    """The sixth guard: agreeing members, wrong exam (W-4's third failure)."""
    mask, _ = _registered(tmp_path)
    wrong = [_prediction(m, KEYS, partition_id="F2") for m in SYNTH_SETS["setA"]["member_ids"]]
    require_partition_agreement(wrong)  # self-consistent — this guard passes
    with pytest.raises(FairnessError):
        require_mask_member_alignment(mask, wrong)


def test_controls_8_9_10_membership_missing_extra_duplicate() -> None:
    for member_ids in (
        ("M-A", "M-B"),  # (8) missing member
        ("M-A", "M-B", "M-C", "M-X"),  # (9) extra member
        ("M-A", "M-A", "M-B", "M-C"),  # (10) duplicate member
    ):
        with pytest.raises(FairnessError):
            require_declared_membership(member_ids, set_id="setA", declared_sets=SYNTH_SETS)


def test_control_11_two_declared_sets_merged_raises() -> None:
    merged = tuple(SYNTH_SETS["setA"]["member_ids"]) + ("X-1",)  # setA + setB's X-1
    with pytest.raises(FairnessError) as excinfo:
        require_declared_membership(merged, set_id="setA", declared_sets=SYNTH_SETS)
    assert "merged" in str(excinfo.value)


def test_control_14_pairwise_mask_attempt_refuses() -> None:
    """FR-P1-04-7's own criterion: a two-member per-pair subset of a declared set."""
    with pytest.raises(FairnessError):
        require_declared_membership(("M-A", "M-C"), set_id="setA", declared_sets=SYNTH_SETS)


def test_control_1_unresolvable_inverse_names_identifier_and_d27() -> None:
    with pytest.raises(InverseTransformError) as excinfo:
        resolve_inverse("T-ABLDIFF-F1")
    message = str(excinfo.value)
    assert "T-ABLDIFF-F1" in message and "D-27" in message


def test_control_3_uninverted_abl_diff_refuses_naming_d27() -> None:
    abl = _prediction("M-C", KEYS, attrs={"ablation_id": "ABL-DIFF"})
    with pytest.raises(InverseTransformError) as excinfo:
        require_target_space(abl)
    assert "D-27" in str(excinfo.value)


def test_control_4_declared_target_touching_without_lineage_refuses() -> None:
    touching = _prediction("M-C", KEYS, attrs={"touches_target": True})
    with pytest.raises(InverseTransformError):
        require_target_space(touching)
    inverted = _prediction(
        "M-C", KEYS, attrs={"touches_target": True, "inverse_applied": True}
    )
    require_target_space(inverted)  # lineage records the inversion — passes


def test_must_not_fire_untransformed_b01_c01_pass_target_space() -> None:
    for model_id in ("B-01", "C-01"):
        require_target_space(_prediction(model_id, KEYS, transform_id=UNTRANSFORMED))


# =======================================================================================
# 3. Mask construction, identity, registration, freeze (R-106, R-107; W-1; Q4 = A)
# =======================================================================================


def test_mask_builds_with_reporting_surface_and_per_station_counts() -> None:
    gap_member = _prediction("M-A", [k for k in KEYS if k != ("S2", 3, 2)], error=1.0)
    mask = _mask(members=_members("setA", **{"M-A": gap_member}))
    assert_reporting_surface(mask)  # all five exposed values present
    assert mask.row_counts["S1"] == 6 and mask.row_counts["S3"] == 6
    assert mask.row_counts["S2"] == 5  # the gapped row dropped by the intersection
    assert mask.exclusion_counts["S2"] == 1 and mask.exclusion_counts["S1"] == 0
    assert mask.scored_window_statement  # derived, non-empty (D-28's mechanism)
    assert sorted(mask.member_transform_ids)  # the recorded transform SET travels


def test_mask_id_deterministic_and_control_12_recompute_mismatch_fails() -> None:
    first, second = _mask(), _mask()
    assert first.mask_id == second.mask_id  # recomputation reproduces the ID
    assert_mask_id_reproduces(first)
    tampered = dataclasses.replace(first, mask_id="0" * 64)
    with pytest.raises(FairnessError):
        assert_mask_id_reproduces(tampered)


def test_control_13_second_registration_for_same_set_raises(tmp_path: Path) -> None:
    mask, registry = _registered(tmp_path)
    with pytest.raises(FairnessError):
        registry.register(mask)


def test_control_31_missing_reporting_value_fails() -> None:
    mask = _mask()
    for field_name, empty in (
        ("feature_set_id", ""),
        ("scored_window_statement", ""),
        ("row_counts", {}),
        ("exclusion_counts", {}),
    ):
        broken = dataclasses.replace(mask, **{field_name: empty})
        with pytest.raises(FairnessError):
            assert_reporting_surface(broken)


def test_q4a_frozen_bundle_manifest_is_write_once(tmp_path: Path) -> None:
    mask, registry = _registered(tmp_path)
    manifest = registry.freeze_bundle()
    assert mask.mask_id in manifest["mask_ids"]
    with pytest.raises(FairnessError):
        registry.freeze_bundle()  # the second write of the write-once manifest REFUSES
    late = _mask("setB")
    with pytest.raises(FairnessError):
        registry.register(late)  # no registration after the freeze


def test_control_28_mismatched_windows_fail_instantiated_on_tier3() -> None:
    """Vision §8.9's M-04/M-05 clause: the tier-3 set is the named instance."""
    members = _members("tier3s")
    members[0].frame.attrs.update({"window_length_hours": 24, "lag_set": ("1h", "24h")})
    members[2].frame.attrs.update({"window_length_hours": 48, "lag_set": ("1h", "24h")})
    with pytest.raises(FairnessError):
        _mask("tier3s", members=members)
    agreeing = _members("tier3s")
    for member in agreeing:
        member.frame.attrs.update({"window_length_hours": 24, "lag_set": ("1h", "24h")})
    mask = _mask("tier3s", members=agreeing)  # matched windows pass, recorded on the mask
    assert mask.window_length_hours == 24 and mask.lag_set == ("1h", "24h")


def test_per_entry_stampless_prediction_into_mask_build_raises() -> None:
    """SD-C-01 per-entry control: W-1's entry point invokes the guard."""
    members = _members("setA", **{"M-A": _prediction("M-A", KEYS, transform_id=None)})
    with pytest.raises(LeakageError):
        _mask(members=members)


def test_mask_build_refuses_merged_sets_at_its_own_entry() -> None:
    members = _members("setA") + [_prediction("X-1", KEYS)]
    with pytest.raises(FairnessError):
        _mask(members=members)


# =======================================================================================
# 4. The estimand (R-108; W-2; FR-P1-05-7 stays Pending — nothing here runs its row)
# =======================================================================================


def test_control_15_known_sign_fixture_orientation_benchmark_minus_model(
    tmp_path: Path,
) -> None:
    """Model perfect, benchmark off by 1 → benchmark minus model = +1: positive favours
    the model. An inverted (model-minus-benchmark) implementation fails this by sign."""
    model = _prediction("M-C", KEYS, error=0.0)
    benchmark = _prediction("M-A", KEYS, error=1.0)
    members = _members("setA", **{"M-C": model, "M-A": benchmark})
    registry = MaskRegistry(tmp_path / "mask_registry")
    mask = _mask(members=members)
    registry.register(mask)
    result = paired_loss_differential(
        model, benchmark, mask=mask, declared_sets=SYNTH_SETS, registry=registry
    )
    assert result.scalar == pytest.approx(1.0)
    assert result.orientation == "benchmark_minus_model"
    assert result.weighting == "equal_station"
    assert result.sign_convention_sentence == SIGN_CONVENTION_SENTENCE
    assert set(result.per_station) == set(STATIONS)


def test_control_16_equal_station_not_pooled_on_asymmetric_counts(tmp_path: Path) -> None:
    """S1 carries 8 rows at diff 0; S2 carries 2 rows at diff ~+3 (error 0 vs sqrt-free
    constant offsets). Equal-station and pooled aggregation disagree by construction."""
    keys_s1 = [("S1", d, h) for d in (2, 3) for h in (0, 1, 2, 3)]
    keys_s2 = [("S2", 2, 0), ("S2", 2, 1)]
    keys = keys_s1 + keys_s2
    per_row = {k: 2.0 for k in keys_s2}  # benchmark off by 2 only on S2 rows
    model = _prediction("M-C", keys, error=0.0)
    benchmark = _prediction("M-A", keys, per_row_error=per_row)
    third = _prediction("M-B", keys, error=1.0)
    sets = {"duo": {"member_ids": ("M-A", "M-B", "M-C"), "model_id": "M-C",
                    "benchmark_ids": ("M-A", "M-B")}}
    registry = MaskRegistry(tmp_path / "mask_registry")
    mask = build_comparison_mask(
        [benchmark, third, model],
        set_id="duo",
        declared_sets=sets,
        target=_target(keys),
        feature_set_id="FS-synth",
        month_start=MONTH_START,
        month_end=MONTH_END,
        embargo_hours=EMBARGO_HOURS,
    )
    registry.register(mask)
    result = paired_loss_differential(
        model, benchmark, mask=mask, declared_sets=sets, registry=registry
    )
    equal_station = (0.0 + 4.0) / 2  # per-station means: S1 = 0, S2 = 2² = 4
    pooled = (8 * 0.0 + 2 * 4.0) / 10
    assert result.scalar == pytest.approx(equal_station)
    assert result.scalar != pytest.approx(pooled)


def test_control_17_unregistered_mask_raises(tmp_path: Path) -> None:
    registry = MaskRegistry(tmp_path / "mask_registry")  # nothing registered
    mask = _mask()
    model = _prediction("M-C", KEYS)
    benchmark = _prediction("M-A", KEYS, error=1.0)
    with pytest.raises(FairnessError):
        paired_loss_differential(
            model, benchmark, mask=mask, declared_sets=SYNTH_SETS, registry=registry
        )


def test_control_29_external_join_onto_unregistered_mask_raises(tmp_path: Path) -> None:
    """R-112: the join point IS the registered-mask check — instantiated on the GIM set."""
    registry = MaskRegistry(tmp_path / "mask_registry")
    members = _members("gimset")
    mask = _mask("gimset", members=members)
    with pytest.raises(FairnessError):
        paired_loss_differential(
            members[0], members[1], mask=mask, declared_sets=SYNTH_SETS, registry=registry
        )


def test_per_entry_sixth_guard_through_the_estimand(tmp_path: Path) -> None:
    """Agreeing-but-mask-mismatched partition set pushed through W-2's entry point."""
    mask, registry = _registered(tmp_path)
    model = _prediction("M-C", KEYS, partition_id="F2")
    benchmark = _prediction("M-A", KEYS, partition_id="F2", error=1.0)
    with pytest.raises(FairnessError):
        paired_loss_differential(
            model, benchmark, mask=mask, declared_sets=SYNTH_SETS, registry=registry
        )


def test_per_entry_uninverted_abl_diff_at_the_estimand(tmp_path: Path) -> None:
    mask, registry = _registered(tmp_path)
    abl = _prediction("M-C", KEYS, attrs={"ablation_id": "ABL-DIFF"})
    benchmark = _prediction("M-A", KEYS, error=1.0)
    with pytest.raises(InverseTransformError):
        paired_loss_differential(
            abl, benchmark, mask=mask, declared_sets=SYNTH_SETS, registry=registry
        )


def test_control_30_estimand_missing_stamp_fails() -> None:
    with pytest.raises(FairnessError):
        EstimandResult(
            scalar=1.0,
            per_station={"S1": 1.0},
            orientation="benchmark_minus_model",
            weighting="equal_station",
            sign_convention_sentence=SIGN_CONVENTION_SENTENCE,
            mask_id="m",
            set_id="setA",
            model_id="M-C",
            benchmark_id="M-A",
            phase_id="p",
            source_id="s",
            target_definition_id="t",
            partition_id="",  # the missing fourth stamp
        )


def test_control_30_estimand_stamp_disagreeing_with_mask_fails(tmp_path: Path) -> None:
    mask, registry = _registered(tmp_path)
    model = _prediction("M-C", KEYS)
    result = paired_loss_differential(
        model,
        _prediction("M-A", KEYS, error=1.0),
        mask=mask,
        declared_sets=SYNTH_SETS,
        registry=registry,
    )
    drifted = dataclasses.replace(result, partition_id="F9")
    second = paired_loss_differential(
        model,
        _prediction("M-B", KEYS, error=1.0),
        mask=mask,
        declared_sets=SYNTH_SETS,
        registry=registry,
    )
    with pytest.raises(FairnessError):
        build_metrics_artifact(
            set_id="setA",
            declared_sets=SYNTH_SETS,
            mask=mask,
            registry=registry,
            estimands=[drifted, second],
        )


def test_inverted_orientation_and_pooled_weighting_are_refused_as_fields() -> None:
    """The convention travels as DATA: a result declaring the wrong orientation or
    weighting cannot even be constructed (R-108's machine-readable convention)."""
    common: dict[str, Any] = dict(
        scalar=1.0,
        per_station={"S1": 1.0},
        sign_convention_sentence=SIGN_CONVENTION_SENTENCE,
        mask_id="m",
        set_id="setA",
        model_id="M-C",
        benchmark_id="M-A",
        phase_id="p",
        source_id="s",
        target_definition_id="t",
        partition_id="F1",
    )
    with pytest.raises(FairnessError):
        EstimandResult(orientation="model_minus_benchmark", weighting="equal_station", **common)
    with pytest.raises(FairnessError):
        EstimandResult(orientation="benchmark_minus_model", weighting="pooled_rows", **common)


# =======================================================================================
# 5. The locked chokepoint (R-109; W-5; SD-C-02/SD-C-03) — synthetic year, no December 2022
# =======================================================================================

DEC_KEYS = [(s, d, h) for s in STATIONS for d in (2, 3) for h in (0, 1, 2)]


def _dec_mask(tmp_path: Path, *, freeze: bool = True):
    members = [
        _prediction(m, DEC_KEYS, partition_id="DEC", month=12, error=(0.0 if m == "M-C" else 1.0))
        for m in SYNTH_SETS["setA"]["member_ids"]
    ]
    registry = MaskRegistry(tmp_path / "mask_registry")
    mask = build_comparison_mask(
        members,
        set_id="setA",
        declared_sets=SYNTH_SETS,
        target=_target(DEC_KEYS, month=12),
        feature_set_id="FS-synth",
        month_start=DEC_MONTH_START,
        month_end=DEC_MONTH_END,
        embargo_hours=EMBARGO_HOURS,
    )
    registry.register(mask)
    manifest = registry.freeze_bundle() if freeze else None
    return mask, registry, manifest


def _receipted_prediction(tmp_path: Path) -> tuple[Path, Path]:
    prediction_path = tmp_path / "M-C_confirmatory.json"
    prediction_path.write_text(json.dumps({"rows": []}), encoding="utf-8")
    receipt_path = tmp_path / "M-C_confirmatory.receipt.json"
    receipt = {
        "prediction_path": str(prediction_path),
        "sha256": hashlib.sha256(prediction_path.read_bytes()).hexdigest(),
        "recorded_at_utc": dt.datetime.now(UTC).isoformat(),
        "run_id": "synthetic-run",
        "partition_id": "DEC",
    }
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
    return prediction_path, receipt_path


def _access_record(mask, registry: MaskRegistry, *, with_fields: bool = True):
    from src.data.locked_test import AccessRecord

    fields: dict[str, Any] = {}
    if with_fields:
        manifest_bytes = registry.manifest_path.read_bytes()
        fields = {
            "mask_bundle_ids": (mask.mask_id,),
            "mask_registry_hash": hashlib.sha256(manifest_bytes).hexdigest(),
        }
    return AccessRecord(
        run_id="synthetic-run",
        retrieved_at_utc=dt.datetime.now(UTC).isoformat(),
        scope="synthetic locked evaluation fixture",
        purpose="locked_evaluation",
        performance_inspected=False,
        locked_test_accessed=True,
        authorization="synthetic G-05 reference (fixture; no real signature exists)",
        **fields,
    )


def _locked_kwargs(mask, registry, prediction_path, receipt_path, record) -> dict[str, Any]:
    return dict(
        mask=mask,
        prediction_path=prediction_path,
        receipt_path=receipt_path,
        access_record=record,
        mask_bundle_manifest=registry.manifest_path,
        month_start=DEC_MONTH_START,
        month_end=DEC_MONTH_END,
        embargo_hours=EMBARGO_HOURS,
    )


def test_must_not_fire_all_dec_stamps_vs_dec_mask_pass(tmp_path: Path) -> None:
    """The G-06 shape at guard level: DEC-stamped members, the registered DEC mask, a
    verifying receipt and containment — every limb green, nothing fires."""
    mask, registry, _ = _dec_mask(tmp_path)
    members = [
        _prediction(m, DEC_KEYS, partition_id="DEC", month=12)
        for m in SYNTH_SETS["setA"]["member_ids"]
    ]
    require_stamps(members, recorded_transform_ids=mask.member_transform_ids)
    require_partition_agreement(members)
    require_mask_member_alignment(mask, members)
    prediction_path, receipt_path = _receipted_prediction(tmp_path)
    record = _access_record(mask, registry)
    require_locked_receipt(
        **_locked_kwargs(mask, registry, prediction_path, receipt_path, record)
    )


def test_control_18_receipt_absent_raises(tmp_path: Path) -> None:
    mask, registry, _ = _dec_mask(tmp_path)
    prediction_path, receipt_path = _receipted_prediction(tmp_path)
    receipt_path.unlink()
    record = _access_record(mask, registry)
    with pytest.raises(LockedTestError):
        require_locked_receipt(
            **_locked_kwargs(mask, registry, prediction_path, receipt_path, record)
        )


def test_controls_19_21_hash_mismatch_and_detected_second_write(tmp_path: Path) -> None:
    mask, registry, _ = _dec_mask(tmp_path)
    prediction_path, receipt_path = _receipted_prediction(tmp_path)
    record = _access_record(mask, registry)
    # (21) a second write of the prediction file AFTER the receipt — detected, not assumed
    prediction_path.write_text(json.dumps({"rows": [], "tampered": True}), encoding="utf-8")
    with pytest.raises(LockedTestError):
        require_locked_receipt(
            **_locked_kwargs(mask, registry, prediction_path, receipt_path, record)
        )


def test_control_20_receipt_not_preceding_the_call_raises(tmp_path: Path) -> None:
    mask, registry, _ = _dec_mask(tmp_path)
    prediction_path, receipt_path = _receipted_prediction(tmp_path)
    record = _access_record(mask, registry)
    kwargs = _locked_kwargs(mask, registry, prediction_path, receipt_path, record)
    kwargs["now"] = dt.datetime.now(UTC) - dt.timedelta(hours=1)  # call "before" the receipt
    with pytest.raises(LockedTestError):
        require_locked_receipt(**kwargs)


def test_control_23_no_access_record_refuses(tmp_path: Path) -> None:
    mask, registry, _ = _dec_mask(tmp_path)
    prediction_path, receipt_path = _receipted_prediction(tmp_path)
    with pytest.raises(LockedTestError):
        require_locked_receipt(
            **_locked_kwargs(mask, registry, prediction_path, receipt_path, None)
        )


def test_containment_fields_absent_refuses_fail_closed(tmp_path: Path) -> None:
    """The Q2 = B half-contract's refusing half: a record without the two fields."""
    mask, registry, _ = _dec_mask(tmp_path)
    prediction_path, receipt_path = _receipted_prediction(tmp_path)
    record = _access_record(mask, registry, with_fields=False)
    with pytest.raises(LockedTestError) as excinfo:
        require_locked_receipt(
            **_locked_kwargs(mask, registry, prediction_path, receipt_path, record)
        )
    assert "mask_bundle_ids" in str(excinfo.value)


def test_containment_manifest_hash_mismatch_refuses(tmp_path: Path) -> None:
    mask, registry, _ = _dec_mask(tmp_path)
    prediction_path, receipt_path = _receipted_prediction(tmp_path)
    from src.data.locked_test import AccessRecord

    record = AccessRecord(
        run_id="synthetic-run",
        retrieved_at_utc=dt.datetime.now(UTC).isoformat(),
        scope="synthetic",
        purpose="locked_evaluation",
        performance_inspected=False,
        locked_test_accessed=True,
        authorization="synthetic",
        mask_bundle_ids=(mask.mask_id,),
        mask_registry_hash="0" * 64,  # does not re-verify
    )
    with pytest.raises(LockedTestError):
        require_locked_receipt(
            **_locked_kwargs(mask, registry, prediction_path, receipt_path, record)
        )


def test_containment_mask_not_in_bundle_refuses(tmp_path: Path) -> None:
    """A mask 'registered' after the access cannot appear in the record — containment."""
    mask, registry, _ = _dec_mask(tmp_path)
    prediction_path, receipt_path = _receipted_prediction(tmp_path)
    manifest_bytes = registry.manifest_path.read_bytes()
    from src.data.locked_test import AccessRecord

    record = AccessRecord(
        run_id="synthetic-run",
        retrieved_at_utc=dt.datetime.now(UTC).isoformat(),
        scope="synthetic",
        purpose="locked_evaluation",
        performance_inspected=False,
        locked_test_accessed=True,
        authorization="synthetic",
        mask_bundle_ids=("some-other-mask-id",),
        mask_registry_hash=hashlib.sha256(manifest_bytes).hexdigest(),
    )
    with pytest.raises(LockedTestError):
        require_locked_receipt(
            **_locked_kwargs(mask, registry, prediction_path, receipt_path, record)
        )


def test_control_22_day1_row_in_the_locked_scored_set_raises(tmp_path: Path) -> None:
    """A row inside the excluded first 24 h of the locked month — the '1 December row'."""
    mask, registry, _ = _dec_mask(tmp_path)
    prediction_path, receipt_path = _receipted_prediction(tmp_path)
    record = _access_record(mask, registry)
    day1 = {
        "station": "S1",
        "interval_start_utc": dt.datetime(SYNTH_YEAR, 12, 1, 5, tzinfo=UTC).isoformat(),
        "y_true": 1.0,
        "y_hats": {m: 1.0 for m in SYNTH_SETS["setA"]["member_ids"]},
    }
    widened = dataclasses.replace(mask, masked_rows=(*mask.masked_rows, day1))
    with pytest.raises(LockedTestError):
        require_locked_receipt(
            **_locked_kwargs(widened, registry, prediction_path, receipt_path, record)
        )


def test_scored_window_statement_reproduces_d28_verbatim() -> None:
    """Pure date arithmetic: the real locked month's statement equals D-28's mandated
    disclosure, with no December read and no scientific constant chosen in source."""
    statement = scored_window_statement(
        dt.datetime(2022, 12, 1, tzinfo=UTC),
        dt.datetime(2023, 1, 1, tzinfo=UTC),
        embargo_hours=24,
    )
    assert statement == "2–31 December 2022, 30 days, first 24 h excluded and counted"


def test_dec_estimand_without_locked_context_refuses(tmp_path: Path) -> None:
    """W-2's DEC entry fails closed: a DEC mask with locked=None never computes."""
    mask, registry, _ = _dec_mask(tmp_path)
    model = _prediction("M-C", DEC_KEYS, partition_id="DEC", month=12)
    benchmark = _prediction("M-A", DEC_KEYS, partition_id="DEC", month=12, error=1.0)
    with pytest.raises(IntegrityError):
        paired_loss_differential(
            model, benchmark, mask=mask, declared_sets=SYNTH_SETS, registry=registry,
            locked=None,
        )


def test_dec_estimand_passes_only_with_full_locked_context(tmp_path: Path) -> None:
    mask, registry, _ = _dec_mask(tmp_path)
    prediction_path, receipt_path = _receipted_prediction(tmp_path)
    record = _access_record(mask, registry)
    model = _prediction("M-C", DEC_KEYS, partition_id="DEC", month=12)
    benchmark = _prediction("M-A", DEC_KEYS, partition_id="DEC", month=12, error=1.0)
    locked = LockedContext(
        prediction_path=prediction_path,
        receipt_path=receipt_path,
        access_record=record,
        mask_bundle_manifest=registry.manifest_path,
        month_start=DEC_MONTH_START,
        month_end=DEC_MONTH_END,
        embargo_hours=EMBARGO_HOURS,
    )
    result = paired_loss_differential(
        model, benchmark, mask=mask, declared_sets=SYNTH_SETS, registry=registry,
        locked=locked,
    )
    assert result.partition_id == "DEC" and result.scalar == pytest.approx(1.0)


# =======================================================================================
# 6. The Q2 = B sibling edit: AccessRecord fields and open_restricted population
# =======================================================================================


def test_access_record_containment_fields_are_additive_and_optional() -> None:
    from src.data.locked_test import AccessRecord

    record = AccessRecord(
        run_id="r",
        retrieved_at_utc="2001-01-01T00:00:00+00:00",
        scope="s",
        purpose="coverage_audit",
        performance_inspected=False,
        locked_test_accessed=True,
        authorization="a",
    )
    assert record.mask_bundle_ids is None and record.mask_registry_hash is None


def test_open_restricted_populates_containment_fields_from_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The populating half of SD-C-02, against a SYNTHETIC root through the documented
    `_repo_root` seam — no real restricted path, no December 2022 content."""
    from src.data import locked_test

    monkeypatch.setattr(locked_test, "_repo_root", lambda: tmp_path)
    restricted_dir = tmp_path / "evidence" / "locked_test_restricted"
    restricted_dir.mkdir(parents=True)
    artifact = restricted_dir / "synthetic_fixture.json"
    artifact.write_text("[]", encoding="utf-8")
    manifest = tmp_path / "frozen_bundle_manifest.json"
    manifest.write_text(json.dumps({"mask_ids": ["mask-1", "mask-2"]}), encoding="utf-8")
    registry_log = tmp_path / "access_log.jsonl"
    record = locked_test.AccessRecord(
        run_id="r",
        retrieved_at_utc=dt.datetime.now(UTC).isoformat(),
        scope="synthetic",
        purpose="locked_evaluation",
        performance_inspected=False,
        locked_test_accessed=True,
        authorization="synthetic",
    )
    opened = locked_test.open_restricted(
        artifact, record=record, registry=registry_log, mask_bundle_manifest=manifest
    )
    assert Path(opened) == artifact.resolve()
    row = json.loads(registry_log.read_text(encoding="utf-8").splitlines()[0])
    assert row["mask_bundle_ids"] == ["mask-1", "mask-2"]
    assert row["mask_registry_hash"] == hashlib.sha256(manifest.read_bytes()).hexdigest()


def test_must_not_fire_coverage_audit_purpose_passes_its_own_door(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The pre-G-05 coverage audit is a DIFFERENT event: no manifest, fields stay None,
    nothing in this unit blocks it (blocking it would repeat the corrected 'opened
    exactly once' misreading)."""
    from src.data import locked_test

    monkeypatch.setattr(locked_test, "_repo_root", lambda: tmp_path)
    restricted_dir = tmp_path / "evidence" / "locked_test_restricted"
    restricted_dir.mkdir(parents=True)
    artifact = restricted_dir / "synthetic_fixture.json"
    artifact.write_text("[]", encoding="utf-8")
    registry_log = tmp_path / "access_log.jsonl"
    record = locked_test.AccessRecord(
        run_id="r",
        retrieved_at_utc=dt.datetime.now(UTC).isoformat(),
        scope="synthetic coverage audit",
        purpose="coverage_audit",
        performance_inspected=False,
        locked_test_accessed=True,
        authorization="synthetic",
    )
    locked_test.open_restricted(artifact, record=record, registry=registry_log)
    row = json.loads(registry_log.read_text(encoding="utf-8").splitlines()[0])
    assert row["purpose"] == "coverage_audit"
    assert row["mask_bundle_ids"] is None and row["mask_registry_hash"] is None


# =======================================================================================
# 7. Honesty mechanics (R-110; W-6; SD-C-04)
# =======================================================================================


def _artifact_inputs(tmp_path: Path, set_id: str = "setA"):
    registry = MaskRegistry(tmp_path / "mask_registry")
    members = _members(set_id)
    by_id = {m.model_id: m for m in members}
    mask = _mask(set_id, members=members)
    registry.register(mask)
    declared = SYNTH_SETS[set_id]
    model = by_id[declared["model_id"]]
    estimands = [
        paired_loss_differential(
            model, by_id[b], mask=mask, declared_sets=SYNTH_SETS, registry=registry
        )
        for b in declared["benchmark_ids"]
    ]
    return mask, registry, estimands


def _synthetic_audit() -> dict[str, Any]:
    return {
        "audit_id": "overlap-audit-1",
        "gim_network_overlap_flag": True,
        "recorded_at_utc": dt.datetime.now(UTC).isoformat(),
    }


def _provenance_for(audit: dict[str, Any]) -> dict[str, Any]:
    canonical = json.dumps(audit, sort_keys=True, separators=(",", ":"), default=str)
    return {
        "overlap_audit_id": audit["audit_id"],
        "overlap_audit_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
    }


def test_control_24_incomplete_emission_refused_per_declared_set(tmp_path: Path) -> None:
    mask, registry, estimands = _artifact_inputs(tmp_path)
    with pytest.raises(FairnessError):
        build_metrics_artifact(
            set_id="setA",
            declared_sets=SYNTH_SETS,
            mask=mask,
            registry=registry,
            estimands=estimands[:-1],  # one declared benchmark's estimand missing
        )


def test_artifact_complete_with_beats_model_and_statement(tmp_path: Path) -> None:
    mask, registry, estimands = _artifact_inputs(tmp_path)
    artifact = build_metrics_artifact(
        set_id="setA", declared_sets=SYNTH_SETS, mask=mask, registry=registry,
        estimands=estimands,
    )
    assert_metrics_artifact(artifact, declared_sets=SYNTH_SETS)
    for row in artifact["comparisons"]:
        # model perfect, benchmarks off by 1 → positive differential → benchmark loses
        assert row["beats_model"] is False and row["scalar"] > 0
    assert artifact["phase2_not_independent_statement"] == PHASE2_NOT_INDEPENDENT_STATEMENT
    # the five exposed reporting values travel on the artifact (R-107 limb 6)
    for key in ("mask_id", "feature_set_id", "row_counts", "exclusion_counts",
                "scored_window_statement"):
        assert artifact[key]


def test_beats_model_true_when_the_benchmark_wins(tmp_path: Path) -> None:
    registry = MaskRegistry(tmp_path / "mask_registry")
    model = _prediction("M-C", KEYS, error=1.0)  # model worse
    winning_benchmark = _prediction("X-1", KEYS, error=0.0)  # benchmark perfect
    members = _members("setB", **{"M-C": model, "X-1": winning_benchmark})
    mask = _mask("setB", members=members)
    registry.register(mask)
    benchmark = members[1]
    result = paired_loss_differential(
        model, benchmark, mask=mask, declared_sets=SYNTH_SETS, registry=registry
    )
    artifact = build_metrics_artifact(
        set_id="setB", declared_sets=SYNTH_SETS, mask=mask, registry=registry,
        estimands=[result],
    )
    row = artifact["comparisons"][0]
    assert result.scalar < 0 and row["beats_model"] is True


def test_control_25_missing_tec06_sentence_fails(tmp_path: Path) -> None:
    mask, registry, estimands = _artifact_inputs(tmp_path, "iriset")
    artifact = build_metrics_artifact(
        set_id="iriset", declared_sets=SYNTH_SETS, mask=mask, registry=registry,
        estimands=estimands,
    )
    row = artifact["comparisons"][0]
    assert row["spatial_representativeness_sentence"] == SPATIAL_REPRESENTATIVENESS_SENTENCE
    del row["spatial_representativeness_sentence"]
    with pytest.raises(FairnessError):
        assert_metrics_artifact(artifact, declared_sets=SYNTH_SETS)


def test_control_27_missing_beats_model_fails(tmp_path: Path) -> None:
    mask, registry, estimands = _artifact_inputs(tmp_path)
    artifact = build_metrics_artifact(
        set_id="setA", declared_sets=SYNTH_SETS, mask=mask, registry=registry,
        estimands=estimands,
    )
    del artifact["comparisons"][0]["beats_model"]
    with pytest.raises(FairnessError):
        assert_metrics_artifact(artifact, declared_sets=SYNTH_SETS)


def test_phase2_statement_tampering_fails(tmp_path: Path) -> None:
    mask, registry, estimands = _artifact_inputs(tmp_path)
    artifact = build_metrics_artifact(
        set_id="setA", declared_sets=SYNTH_SETS, mask=mask, registry=registry,
        estimands=estimands,
    )
    artifact["phase2_not_independent_statement"] = "a second independent blind test"
    with pytest.raises(FairnessError):
        assert_metrics_artifact(artifact, declared_sets=SYNTH_SETS)


def test_control_26_gim_comparison_without_registered_audit_fails(tmp_path: Path) -> None:
    mask, registry, estimands = _artifact_inputs(tmp_path, "gimset")
    with pytest.raises(FairnessError):
        build_metrics_artifact(
            set_id="gimset", declared_sets=SYNTH_SETS, mask=mask, registry=registry,
            estimands=estimands, gim_overlap_audit=None,
        )


def test_control_32_audit_after_comparator_containment_fails(tmp_path: Path) -> None:
    """A comparator with no (or mismatched) audit containment evidence fails — an audit
    registered after generation cannot appear in the comparator's provenance."""
    mask, registry, estimands = _artifact_inputs(tmp_path, "gimset")
    audit = _synthetic_audit()
    with pytest.raises(FairnessError):
        build_metrics_artifact(
            set_id="gimset", declared_sets=SYNTH_SETS, mask=mask, registry=registry,
            estimands=estimands, gim_overlap_audit=audit, gim_comparator_provenance=None,
        )
    mismatched = {"overlap_audit_id": audit["audit_id"], "overlap_audit_sha256": "0" * 64}
    with pytest.raises(FairnessError):
        build_metrics_artifact(
            set_id="gimset", declared_sets=SYNTH_SETS, mask=mask, registry=registry,
            estimands=estimands, gim_overlap_audit=audit,
            gim_comparator_provenance=mismatched,
        )


def test_gim_disclosure_happy_path_carries_flag_and_containment(tmp_path: Path) -> None:
    mask, registry, estimands = _artifact_inputs(tmp_path, "gimset")
    audit = _synthetic_audit()
    artifact = build_metrics_artifact(
        set_id="gimset", declared_sets=SYNTH_SETS, mask=mask, registry=registry,
        estimands=estimands, gim_overlap_audit=audit,
        gim_comparator_provenance=_provenance_for(audit),
    )
    assert_metrics_artifact(artifact, declared_sets=SYNTH_SETS)
    block = artifact["comparisons"][0]["gim_overlap_disclosure"]
    assert block["gim_network_overlap_flag"] is True
    assert block["overlap_audit_id"] == audit["audit_id"]
    assert block["overlap_audit_sha256"]


def test_metrics_artifact_write_is_refuse_to_overwrite(tmp_path: Path) -> None:
    mask, registry, estimands = _artifact_inputs(tmp_path)
    artifact = build_metrics_artifact(
        set_id="setA", declared_sets=SYNTH_SETS, mask=mask, registry=registry,
        estimands=estimands,
    )
    path = tmp_path / "metrics_setA.json"
    write_metrics_artifact(artifact, path)
    with pytest.raises(FairnessError):
        write_metrics_artifact(artifact, path)


# =======================================================================================
# 8. The hierarchy, the aborted row, and the import boundary — evidence by construction
# =======================================================================================


def test_fresh_subclass_lands_the_aborted_row_via_the_stage_entry_catch() -> None:
    """R-01's fresh-subclass control: `InverseTransformError` derives from
    `IntegrityError`, and script 07's ONLY abort handler catches `IntegrityError` — so the
    unit-local exception lands the `aborted` registry row with no hand-maintained list."""
    assert issubclass(InverseTransformError, IntegrityError)
    assert issubclass(FairnessError, IntegrityError)
    tree = ast.parse(
        (REPO_ROOT / "scripts" / "07_evaluate_and_report.py").read_text(encoding="utf-8")
    )
    handler_names: list[str] = []
    abort_calls: list[bool] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is not None:
            names = (
                [node.type.id]
                if isinstance(node.type, ast.Name)
                else [e.id for e in node.type.elts if isinstance(e, ast.Name)]
                if isinstance(node.type, ast.Tuple)
                else []
            )
            handler_names.extend(names)
            body_src = ast.unparse(node)
            abort_calls.append("record_abort_honestly" in body_src)
    assert "IntegrityError" in handler_names
    assert any(abort_calls), "no handler routes to record_abort_honestly"


def test_src_evaluation_never_imports_features_models_and_defers_external() -> None:
    """D-27 / TE §12: no `src.features` or `src.models` import anywhere under
    `src/evaluation` (module scope OR function bodies — the transitive edge is the point);
    `src.external` appears ONLY inside function bodies (evaluation time, R-112)."""
    eval_dir = REPO_ROOT / "src" / "evaluation"
    forbidden = ("src.features", "src.models")
    for path in sorted(eval_dir.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
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
                    ), (path, name)
        for node in tree.body:  # module scope: src.external must not appear here
            if isinstance(node, ast.Import | ast.ImportFrom):
                names = (
                    [node.module or ""]
                    if isinstance(node, ast.ImportFrom)
                    else [a.name for a in node.names]
                )
                for name in names:
                    assert not name.startswith("src.external"), (path, name)


def test_script_07_imports_no_features_models_or_external_and_names_no_restricted_root() -> None:
    """The script is an orchestrator over `src/data` + `src/evaluation` only, and it is
    NOT a member of R-28's restricted-literal exempt list, so it must never name the
    restricted root."""
    path = REPO_ROOT / "scripts" / "07_evaluate_and_report.py"
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import | ast.ImportFrom):
            names = (
                [node.module or ""]
                if isinstance(node, ast.ImportFrom)
                else [a.name for a in node.names]
            )
            for name in names:
                for forbidden in ("src.features", "src.models", "src.external", "src.gnss"):
                    assert not name.startswith(forbidden), (path, name)
    assert "locked_test_restricted" not in source
    from src.data.locked_test import RESTRICTED_LITERAL_EXEMPT_MODULES

    assert "scripts/07_evaluate_and_report.py" not in RESTRICTED_LITERAL_EXEMPT_MODULES


def test_dec_entry_in_script_07_routes_only_through_the_two_guards() -> None:
    """No DEC execution path outside `materialise_locked_partition` + `open_restricted`:
    the script calls both, requires the locked-path arguments for DEC, and contains no
    other December read."""
    source = (REPO_ROOT / "scripts" / "07_evaluate_and_report.py").read_text(encoding="utf-8")
    assert "materialise_locked_partition(" in source
    assert "open_restricted(" in source
    assert 'purpose="locked_evaluation"' in source
    assert "--partition DEC requires --g05-signature" in source


def test_prediction_from_payload_round_trips_the_eight_fields() -> None:
    payload = {
        "model_id": "M-C",
        "seed": None,
        "partition_id": "F1",
        "transform_id": "T-F1",
        "phase_id": "p",
        "source_id": "s",
        "target_definition_id": "t",
        "rows": [{"station": "S1", "interval_start_utc": _ts(2, 0), "y_hat": 1.0}],
    }
    loaded = prediction_from_payload(payload, resource="synthetic")
    assert loaded.model_id == "M-C" and loaded.partition_id == "F1"
    broken = dict(payload)
    del broken["transform_id"]
    with pytest.raises(IntegrityError):
        prediction_from_payload(broken, resource="synthetic")


def test_mask_id_recompute_is_pure_over_content() -> None:
    mask = _mask()
    assert compute_mask_id(mask.set_id, mask.member_ids, mask.masked_rows) == mask.mask_id
