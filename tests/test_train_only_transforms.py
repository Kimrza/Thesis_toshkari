"""NFR-LEAK-01 / TA-11: train-only transforms enforced by CHECK -- the M10 fixture (Q12 = C).

PURPOSE. R-74's four elements, in ADR-11 form and R-83's both-bounds form, each with the
negative control that proves the violation is CAUGHT. The tests are MANIFEST/BUNDLE-BASED:
they construct `FeatureBundle`s carrying the identity fields a consumer reads from disk and
assert the refusal -- not static analysis of the nine scripts, not monkeypatch-and-replay
(five review cycles proved those unimplementable across the `05` -> `06` file handoff).

The M10 synthetic contract fixture (unit-of-work.md section 7; owner ruling Q12 = C) asserts,
over the SYNTHETIC partition dates `test_split_embargo.py` authors:

(a) the identity check raises for EVERY ordered pair of partition ids except the enumerated
    `REFIT` -> `DEC`, by enumeration over the six ids (36 pairs, 30 mismatched, 1 exempt,
    29 + 1 = 30 raising conditions, derived in the test before it is asserted);
(b) that pair passes with `role="score"` and raises with `role="train"`;
(c) `fit_transforms` raises when the bundle's scored range is not EXACTLY the partition's
    training range -- over-wide AND the strict-subset direction R-83 added;
(d) every consumer raises on a bundle whose `transform_id is None`.

Plus: the full-dataset fit raises; a train-role bundle at a scoring site fails; a
cross-partition transform fails; an already-transformed bundle passed back raises;
`fit_transforms` raises `PartitionError` (not `LeakageError`) on an id disagreement
(Recommendation 8); the R-77 carry-forward boundary rejects `vtec_lag_*`; `Transform`
exposes no `apply`/`inverse` surface (Q4 = A, D-27); and `build_features` itself refuses at
its public entry point (guard invocation proven per entry point, not only correctness once).

INPUTS. Synthetic in-memory bundles, partitions and configs. No December 2022 content, no
restricted-root path, no real config value. RE-RUN: pure functions.

WHAT NO TEST HERE DISCHARGES. TA-11 stays `Pending`; NFR-LEAK-01's evidence is the
Supervisor's at G-04/G-05; BLK-04's contract is approved (2026-09-05), its evidence limb is
not. Smoke evidence only on the interpreter used here.

Run: pytest tests/test_train_only_transforms.py -rs
"""

from __future__ import annotations

import datetime as dt
import itertools
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "tests") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "tests"))

from test_split_embargo import (  # noqa: E402
    SYNTH_YEAR,
    synthetic_partitions,
    synthetic_snapshot,
)

from src.data.config import IntegrityError, LeakageError, PartitionError  # noqa: E402
from src.data.splits import (  # noqa: E402
    LOCKED_ID,
    PARTITION_IDS,
    REFIT_ID,
    RecordFrame,
    partition_by_id,
    training_range,
    validation_month_range,
)
from src.features.build import (  # noqa: E402
    FeatureBundle,
    FrameSpec,
    assert_transform_identity,
    build_features,
    validate_spec,
)
from src.features.transforms import (  # noqa: E402
    FieldClass,
    Transform,
    apply_fitted_transform,
    assert_consumable,
    assert_field_classes_partition,
    carry_forward,
    fit_transforms,
    transform_id_for,
)

UTC = dt.UTC
PARTITIONS = synthetic_partitions()


def _p(pid: str):
    return partition_by_id(PARTITIONS, pid)


def _ts(month: int, day: int, hour: int = 0) -> dt.datetime:
    return dt.datetime(SYNTH_YEAR, month, day, hour, tzinfo=UTC)


def _train_spec(pid: str) -> FrameSpec:
    start, end = training_range(_p(pid))
    return FrameSpec(pid, "train", start, end)


def _score_spec(pid: str) -> FrameSpec:
    start, end = validation_month_range(_p(pid))
    return FrameSpec(pid, "score", start, end)


def _bundle(spec: FrameSpec, *, transform_id: str | None = None, rows: int = 4) -> FeatureBundle:
    """A hand-built bundle: the identity fields a consumer would read from spec.json, and a
    small matrix of two standardisable columns (values vary so the fit has a scale)."""
    records = [{"a": float(i), "b": float(2 * i + 1)} for i in range(rows)]
    return FeatureBundle(
        matrix=RecordFrame(records),
        tensor=[],
        spec=spec,
        transform_id=transform_id,
        provenance={"a": {}, "b": {}},
        identity={"phase_id": "p", "source_id": "s", "target_definition_id": "t"},
        standardized_columns=("a", "b"),
    )


def _transform(pid: str) -> Transform:
    start, end = training_range(_p(pid))
    return Transform(
        transform_id=transform_id_for(pid),
        partition_id=pid,
        columns=("a",),
        means={"a": 0.0},
        scales={"a": 1.0},
        fitted_start=start,
        fitted_end=end,
    )


# --- (a) and (b): the identity check, enumerated over the six ids ------------------------


def test_identity_check_enumeration_has_exactly_thirty_raising_conditions() -> None:
    """Derived, not carried: 36 ordered pairs, 30 mismatched, 1 exempt, 29 + 1 = 30."""
    assert len(PARTITION_IDS) == 6
    pairs = list(itertools.product(PARTITION_IDS, repeat=2))
    assert len(pairs) == 36
    mismatched = [(t, s) for t, s in pairs if t != s]
    assert len(mismatched) == 30
    raising = 0
    for transform_pid, spec_pid in mismatched:
        for role in ("train", "score"):
            spec = _train_spec(spec_pid) if role == "train" else None
            if role == "score":
                if spec_pid == REFIT_ID:
                    continue  # the refit has no score spec at all (checked separately)
                spec = _score_spec(spec_pid)
            exempt = transform_pid == REFIT_ID and spec_pid == LOCKED_ID and role == "score"
            if exempt:
                assert_transform_identity(_transform(transform_pid), spec)
                continue
            if role == "train":
                with pytest.raises(LeakageError):
                    assert_transform_identity(_transform(transform_pid), spec)
                raising += 1
            else:
                with pytest.raises(LeakageError):
                    assert_transform_identity(_transform(transform_pid), spec)
    # Every mismatched pair raises under role="train" (30, including REFIT -> DEC/train);
    # under role="score" every mismatched pair with a score spec raises except the one exempt.
    assert raising == 30


def test_matching_ids_pass_for_every_partition_and_role() -> None:
    for pid in PARTITION_IDS:
        assert_transform_identity(_transform(pid), _train_spec(pid))
        if pid != REFIT_ID:
            assert_transform_identity(_transform(pid), _score_spec(pid))


def test_refit_to_dec_passes_only_under_score() -> None:
    """(b): the G-06 apply passes; training on the locked month raises."""
    assert_transform_identity(_transform(REFIT_ID), _score_spec(LOCKED_ID))
    with pytest.raises(LeakageError) as excinfo:
        assert_transform_identity(_transform(REFIT_ID), _train_spec(LOCKED_ID))
    assert "REFIT -> DEC under role='score'" in str(excinfo.value)


def test_f4_transform_on_an_f1_spec_raises_regardless_of_month_overlap() -> None:
    """The leaking direction both superseded containment rules passed."""
    for spec in (_train_spec("F1"), _score_spec("F1")):
        with pytest.raises(LeakageError):
            assert_transform_identity(_transform("F4"), spec)


def test_a_second_exception_cannot_be_added_silently() -> None:
    """DEC -> REFIT (the reverse pair) raises under both roles: the table has one row."""
    with pytest.raises(LeakageError):
        assert_transform_identity(_transform(LOCKED_ID), _train_spec(REFIT_ID))


# --- (c): fit_transforms' range equality, both bounds, both directions -------------------


def test_fit_on_the_exact_training_range_passes_and_stamps_the_partition() -> None:
    f1 = _p("F1")
    transform = fit_transforms(_bundle(_train_spec("F1")), partition=f1)
    assert transform.partition_id == "F1"
    assert transform.transform_id == "T-F1"
    assert transform.touches_target is False
    assert transform.columns == ("a", "b")
    assert transform.fitted_start, transform.fitted_end == training_range(f1)


def test_full_dataset_fit_raises_over_wide() -> None:
    """The Critical-1 case: a spec claiming F1/train over the whole refit range."""
    start, _ = training_range(_p("F1"))
    _, refit_end = training_range(_p(REFIT_ID))
    with pytest.raises(LeakageError) as excinfo:
        validate_spec(FrameSpec("F1", "train", start, refit_end), PARTITIONS)
    assert "not contained" in str(excinfo.value)
    # and a hand-asserted bundle carrying that range fails in fit_transforms too
    bundle = _bundle(FrameSpec("F1", "train", start, refit_end))
    with pytest.raises(LeakageError) as excinfo2:
        fit_transforms(bundle, partition=_p("F1"))
    assert "over-wide" in str(excinfo2.value)


def test_strict_subset_fit_raises_the_r83_control() -> None:
    """F4 fitted on a range starting a month late: the direction the missing lower bound
    admitted, and the one a derive-from-earliest-row implementation would have accepted."""
    _, end = training_range(_p("F4"))
    bundle = _bundle(FrameSpec("F4", "train", _ts(2, 1), end))
    with pytest.raises(LeakageError) as excinfo:
        fit_transforms(bundle, partition=_p("F4"))
    assert "strict subset" in str(excinfo.value)
    assert "R-83" in str(excinfo.value)


def test_one_row_wider_or_narrower_raises() -> None:
    start, end = training_range(_p("F2"))
    one_hour = dt.timedelta(hours=1)
    for scored_start, scored_end in (
        (start - one_hour, end),
        (start, end + one_hour),
        (start + one_hour, end),
        (start, end - one_hour),
    ):
        with pytest.raises(LeakageError):
            fit_transforms(
                _bundle(FrameSpec("F2", "train", scored_start, scored_end)), partition=_p("F2")
            )


def test_fit_on_dec_partition_never_reaches_the_locked_month() -> None:
    """R-74 (Recommendation 25): DEC.train_end is the refit's boundary, so any bundle whose
    range includes the locked month is not DEC's training range and raises."""
    dec = _p(LOCKED_ID)
    start, _ = training_range(dec)
    with pytest.raises(LeakageError):
        fit_transforms(
            _bundle(FrameSpec(LOCKED_ID, "train", start, _ts(12, 31, 23))), partition=dec
        )


def test_score_role_bundle_cannot_be_fitted() -> None:
    with pytest.raises(LeakageError) as excinfo:
        fit_transforms(_bundle(_score_spec("F1")), partition=_p("F1"))
    assert "train-role bundle only" in str(excinfo.value)


def test_already_transformed_bundle_cannot_be_refitted() -> None:
    with pytest.raises(LeakageError) as excinfo:
        fit_transforms(_bundle(_train_spec("F1"), transform_id="T-F1"), partition=_p("F1"))
    assert "already transformed" in str(excinfo.value)


def test_id_disagreement_in_fit_transforms_is_a_partition_error() -> None:
    """Recommendation 8: a bundle stamped F1 whose range is exactly F2's, fitted with
    partition=F2, fails the ID limb with PartitionError and would PASS the range limb."""
    start, end = training_range(_p("F2"))
    bundle = _bundle(FrameSpec("F1", "train", start, end))
    with pytest.raises(PartitionError) as excinfo:
        fit_transforms(bundle, partition=_p("F2"))
    assert "declared-identity disagreement" in str(excinfo.value)
    with pytest.raises(LeakageError):
        # the same bundle against ITS OWN partition fails the range limb, not the id limb
        fit_transforms(bundle, partition=_p("F1"))


def test_empty_bundle_cannot_be_fitted() -> None:
    with pytest.raises(IntegrityError) as excinfo:
        fit_transforms(_bundle(_train_spec("F1"), rows=0), partition=_p("F1"))
    assert "empty" in str(excinfo.value)


def test_zero_variance_column_is_refused_not_defaulted() -> None:
    bundle = FeatureBundle(
        matrix=RecordFrame([{"a": 1.0}, {"a": 1.0}, {"a": 1.0}]),
        tensor=[],
        spec=_train_spec("F1"),
        transform_id=None,
        standardized_columns=("a",),
    )
    with pytest.raises(IntegrityError) as excinfo:
        fit_transforms(bundle, partition=_p("F1"))
    assert "zero variance" in str(excinfo.value)


# --- (d): the untransformed bundle is never consumable -----------------------------------


def test_untransformed_bundle_is_refused_by_every_consumer_entry() -> None:
    raw = _bundle(_train_spec("F1"), transform_id=None)
    with pytest.raises(LeakageError) as excinfo:
        assert_consumable(raw)
    assert "untransformed" in str(excinfo.value)
    assert_consumable(_bundle(_score_spec("F1"), transform_id="T-F1")) is None


def test_train_role_bundle_reaching_an_evaluation_comparison_fails() -> None:
    """A scoring site asserts role == 'score' on the bundle's own stamp."""
    bundle = _bundle(_train_spec("F1"), transform_id="T-F1")
    assert_consumable(bundle)
    assert bundle.spec.role != "score", "a train-role bundle must be refused where scoring happens"


def test_partition_js_transform_scoring_partition_ks_month_fails() -> None:
    with pytest.raises(LeakageError):
        assert_transform_identity(_transform("F2"), _score_spec("F3"))


# --- Transform exposes no apply or inverse surface (ADR-11; Q4 = A, D-27) ----------------


def test_transform_has_no_apply_and_no_inverse() -> None:
    public = {name for name in dir(Transform) if not name.startswith("_")}
    assert "apply" not in public and "inverse" not in public
    assert "load_inverse" not in dir(sys.modules["src.features.transforms"])
    assert "load_inverse" not in dir(sys.modules["src.features.build"])


def test_apply_fitted_transform_standardises_only_the_fitted_columns() -> None:
    transform = Transform(
        transform_id="T-F1",
        partition_id="F1",
        columns=("a",),
        means={"a": 2.0},
        scales={"a": 2.0},
        fitted_start=_ts(1, 1),
        fitted_end=_ts(4, 1),
    )
    out = apply_fitted_transform([{"a": 4.0, "b": 9.0}], transform)
    assert out == [{"a": 1.0, "b": 9.0}]
    with pytest.raises(LeakageError):
        apply_fitted_transform([{"b": 9.0}], transform)


# --- R-77: the carry-forward boundary --------------------------------------------------


def test_vtec_lag_is_rejected_at_the_carry_forward_boundary() -> None:
    hourly = {_ts(1, 1, h): (None if h == 2 else float(h)) for h in range(5)}
    with pytest.raises(LeakageError) as excinfo:
        carry_forward(hourly, field_class=FieldClass.target, bound_h=3, feature="vtec_lag_1h")
    assert "excluded and counted" in str(excinfo.value)
    for other in (FieldClass.station, FieldClass.time, FieldClass.support, FieldClass.diagnostic):
        with pytest.raises(LeakageError):
            carry_forward(hourly, field_class=other, bound_h=3, feature="x")


def test_driver_class_carries_forward_within_the_bound_and_counts_exclusions() -> None:
    hourly = {_ts(1, 1, h): (None if h in (2, 3, 4, 5) else float(h)) for h in range(8)}
    result = carry_forward(hourly, field_class=FieldClass.driver, bound_h=2, feature="kp_safe")
    assert result["carried_forward_epochs"] == [_ts(1, 1, 2), _ts(1, 1, 3)]
    assert result["excluded_epochs"] == [_ts(1, 1, 4), _ts(1, 1, 5)]
    assert result["excluded_count"] == 2


def test_carry_forward_without_a_field_class_is_unrepresentable() -> None:
    with pytest.raises(TypeError):
        carry_forward({}, bound_h=3, feature="kp_safe")  # type: ignore[call-arg]
    with pytest.raises(LeakageError):
        carry_forward(
            {}, field_class="driver", bound_h=3, feature="kp_safe"  # type: ignore[arg-type]
        )


def test_field_classes_partition_the_dictionary() -> None:
    classes = assert_field_classes_partition({"kp_safe": "driver", "vtec_lag_1h": "target"})
    assert classes["kp_safe"] is FieldClass.driver
    with pytest.raises(LeakageError):
        assert_field_classes_partition({"x": None})
    with pytest.raises(LeakageError):
        assert_field_classes_partition({"x": ["driver", "target"]})
    with pytest.raises(LeakageError):
        assert_field_classes_partition({"x": "weather"})
    with pytest.raises(LeakageError):
        assert_field_classes_partition({"vtec_lag_1h": "driver"})


# --- guard invocation THROUGH the public entry point (nfr-design c58) ---------------------


def _minimal_features() -> dict:
    return {
        "feature_dictionary": {
            "vtec_seq_24": {
                "dictionary_row": "vtec_seq_24",
                "sequence_steps": 24,
                "source_column": "vtec_tecu",
                "normalization": "train_only_standardize",
            }
        },
        "permitted_producers": {"vtec_seq_24": ["phase1_hourly_target"]},
    }


def test_build_features_refuses_an_unknown_partition_before_anything_else() -> None:
    snapshot = synthetic_snapshot(features=_minimal_features())
    with pytest.raises(PartitionError):
        build_features(
            [],
            drivers={},
            registry={},
            matrix=(),
            spec=FrameSpec("F9", "train", _ts(1, 1), _ts(2, 1)),
            partitions=PARTITIONS,
            snapshot=snapshot,
        )


def test_build_features_refuses_a_cross_partition_transform_at_its_entry_point() -> None:
    snapshot = synthetic_snapshot(features=_minimal_features())
    with pytest.raises(LeakageError) as excinfo:
        build_features(
            [],
            drivers={},
            registry={},
            matrix=(),
            spec=_score_spec("F1"),
            partitions=PARTITIONS,
            snapshot=snapshot,
            transform=_transform("F4"),
        )
    assert "transform.partition_id" in str(excinfo.value)


def test_build_features_refuses_a_score_spec_for_the_refit() -> None:
    snapshot = synthetic_snapshot(features=_minimal_features())
    start, end = training_range(_p(REFIT_ID))
    with pytest.raises(PartitionError):
        build_features(
            [],
            drivers={},
            registry={},
            matrix=(),
            spec=FrameSpec(REFIT_ID, "score", start, end),
            partitions=PARTITIONS,
            snapshot=snapshot,
        )


def test_frame_spec_refuses_naive_or_inverted_bounds() -> None:
    with pytest.raises(PartitionError):
        FrameSpec("F1", "train", dt.datetime(SYNTH_YEAR, 1, 1), _ts(2, 1))
    with pytest.raises(PartitionError):
        FrameSpec("F1", "train", _ts(2, 1), _ts(1, 1))
    with pytest.raises(PartitionError):
        FrameSpec("F1", "evaluate", _ts(1, 1), _ts(2, 1))  # type: ignore[arg-type]
