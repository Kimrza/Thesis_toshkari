"""TA-33..TA-36: the four leakage-sensitive negative controls at the feature-building
enforcement boundary (TE §12; TE §19; `CR-2026-08-22-LEAKAGE-TA`).

PURPOSE. This module is the mandated §12 home of the four negative-path controls TE §19
rows TA-33, TA-34, TA-35 and TA-36 name, and TA-36's row fixes the boundary explicitly:
*"the primary rejection test sits at the feature-building enforcement boundary
(`features.build_features`)"*. Every control here therefore pushes a VIOLATING INPUT
THROUGH `build_features` (or, where the rule's own home is a different public entry point,
through THAT entry point) and asserts the raise — never through a private helper and never
by re-implementing the check. A guard module alone fails open on a forgotten call
(`nfr-design:c58`), so what is proven here is INVOCATION, not only correctness.

    TA-33  feature-dictionary closure (FR-P1-04-12) ....... a field outside the §6.2
           dictionary reaching the builder, and a tuned history window
    TA-34  target-derived lag contract (FR-P1-04-13) ...... a carried-forward `vtec_lag_*`
           value, and an incomplete `vtec_seq_24` window admitted rather than excluded
    TA-35  support-field rules (FR-P1-04-16) .............. a support field used as a model
           input with no recorded approval, and one read at or beyond hour t
    TA-36  driver alignment (FR-P1-04-17, D-10.2) ......... a present value mapped outside
           its own interval, a value interpolated while still satisfying its declared lag,
           and the code-level no-interpolation check

Plus the three wired-guard controls for the driver-consuming boundary declared in
`src/external/spaceweather.py`'s "Boundary split" section: the duplicate-epoch refusal in
the one driver ingest path, and TC-12's joined-grid identity check.

RELATION TO `tests/test_feature_availability.py`. That module is unit `features-and-splits`'
own R-76/R-77/R-78 coverage and overlaps some of these conditions. It is not a substitute:
TE §19 names THIS file as each of the four rows' evidence artifact, and TA-36's row requires
the primary rejection at the builder boundary specifically. The duplication is deliberate.

INPUTS. Synthetic in-memory records, partitions and `ConfigSnapshot`s over the synthetic
year `test_split_embargo.py` authors. No December 2022 content, no restricted-root path, no
real configuration value, no file written. RE-RUN: pure functions; deterministic.

WHAT NO TEST HERE DISCHARGES. TA-33, TA-34, TA-35 and TA-36 stay `Pending`: their evidence
is EXECUTED negative-path test output captured in a governed run, and a passing run on the
interpreter used here is smoke evidence, never governed evidence. NFR-LEAK-01's evidence
remains the Supervisor's at G-04/G-05.

RESIDUAL LIMIT, recorded rather than silently worked around (TA-36). `build_features`
alignment-checks a driver series only when the producer attached `attrs["observations"]`
(`src/features/build.py` `_assert_driver_alignment`: *"Both need `attrs['observations']`; a
series without them is not checked here (the matrix limbs still apply), never relabelled"*).
A raw driver frame supplied WITHOUT its observations is therefore admitted unchecked on the
own-interval limb, so TA-36's rejection depends on the producer attaching them. That is a
pre-existing, documented design decision of the builder, not a defect introduced here, and
changing it is a behaviour change outside this remediation's approved scope.

Run: pytest tests/test_feature_leakage_guards.py -rs
"""

from __future__ import annotations

import ast
import datetime as dt
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "tests") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "tests"))

from test_split_embargo import (  # noqa: E402
    SYNTH_WINDOW_HOURS,
    SYNTH_YEAR,
    synthetic_partitions,
    synthetic_snapshot,
)

from src.data.config import (  # noqa: E402
    AlignmentError,
    IntegrityError,
    LeakageError,
)
from src.data.splits import RecordFrame  # noqa: E402
from src.external.spaceweather import (  # noqa: E402
    SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG,
    assert_identical_across_cells,
    select_lagged_series,
)
from src.features._frames import records_of  # noqa: E402
from src.features.availability import AvailabilityRow  # noqa: E402
from src.features.build import (  # noqa: E402
    SECTION_6_2_ROWS,
    FrameSpec,
    build_features,
)
from src.features.transforms import FieldClass, carry_forward  # noqa: E402

UTC = dt.timezone.utc
PARTITIONS = synthetic_partitions()

#: A SHORT scored range CONTAINED in F1's training range (`validate_spec` requires
#: containment, not equality — equality is `fit_transforms`' rule, exercised elsewhere).
#: Seven days keeps every control's frame small enough to read in a failure message.
SCORED_START = dt.datetime(SYNTH_YEAR, 1, 1, tzinfo=UTC)
SCORED_HOURS = 168
SCORED_END = SCORED_START + dt.timedelta(hours=SCORED_HOURS)
#: The one driver interval width used by the alignment controls: Kp's own 3-hour interval.
KP_INTERVAL_HOURS = 3


def _spec() -> FrameSpec:
    return FrameSpec("F1", "train", SCORED_START, SCORED_END)


# --- the harness: one happy build, mutated one thing at a time ----------------------------


def _dictionary(**extra: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "vtec_lag_1h": {
            "dictionary_row": "vtec_lag",
            "lag_hours": 1,
            "source_column": "vtec_tecu",
            "normalization": "train_only_standardize",
        },
        "vtec_lag_3h": {
            "dictionary_row": "vtec_lag",
            "lag_hours": 3,
            "source_column": "vtec_tecu",
            "normalization": "train_only_standardize",
        },
        "vtec_seq_24": {
            "dictionary_row": "vtec_seq_24",
            "sequence_steps": SYNTH_WINDOW_HOURS,
            "source_column": "vtec_tecu",
            "normalization": "train_only_standardize",
        },
        "utc_hour_sin": {"dictionary_row": "utc_hour_sin", "normalization": "none"},
        "utc_hour_cos": {"dictionary_row": "utc_hour_cos", "normalization": "none"},
        "kp_safe": {"dictionary_row": "kp_safe", "source_series": "kp", "normalization": "none"},
    }
    base.update(extra)
    return base


def _producers(**extra: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "vtec_lag": ["phase1_hourly_target"],
        "vtec_seq_24": ["phase1_hourly_target"],
        "utc_hour_sin": ["record_timestamp"],
        "utc_hour_cos": ["record_timestamp"],
        "kp_safe": ["gfz_kp_provisional"],
    }
    base.update(extra)
    return base


def _features(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "feature_dictionary": _dictionary(),
        "permitted_producers": _producers(),
        "carry_forward_bound_hours": 3,
    }
    base.update(overrides)
    return base


def _matrix() -> tuple[AvailabilityRow, ...]:
    return (
        AvailabilityRow(
            feature="kp_safe",
            observation_timestamp="x",
            publication_timestamp="y",
            release_status="provisional",
            safe_lag_hours=3.0,
            actual_lag_hours=3.5,
        ),
    )


def _target(*, stations: tuple[str, ...] = ("S1",), drop_hours: tuple[int, ...] = ()) -> Any:
    """The D-17-shaped hourly target frame. `drop_hours` punches holes so an incomplete
    window can be shown EXCLUDED AND COUNTED rather than filled (TA-34)."""
    frame = RecordFrame(
        {
            "interval_start_utc": (SCORED_START + dt.timedelta(hours=h)).isoformat(),
            "station_id": station,
            "vtec_tecu": 10.0 + (h % 17) * 0.5,
            "valid_observation_count": 5 + (h % 3),
            "phase_id": "phase1",
            "source_id": "synthetic",
            "target_definition_id": "synthetic-gridded",
        }
        for station in stations
        for h in range(SCORED_HOURS)
        if h not in drop_hours
    )
    frame.attrs["producing_artifact"] = "phase1_hourly_target"
    return frame


def _kp_rows(values: dict[int, float] | None = None) -> list[dict[str, Any]]:
    """One row per hour, the value constant across each 3-hour source interval — the
    correctly aligned series. `values` overrides individual hours to build a mutant."""
    override = values or {}
    return [
        {
            "interval_start_utc": (SCORED_START + dt.timedelta(hours=h)).isoformat(),
            "value": override.get(h, float(100 + h // KP_INTERVAL_HOURS)),
        }
        for h in range(SCORED_HOURS)
    ]


def _kp_observations() -> list[dict[str, Any]]:
    """The provider's own 3-hour intervals, whose values `_kp_rows` reproduces exactly."""
    return [
        {
            "value": float(100 + k),
            "interval_start": SCORED_START + dt.timedelta(hours=KP_INTERVAL_HOURS * k),
            "interval_end": SCORED_START + dt.timedelta(hours=KP_INTERVAL_HOURS * (k + 1)),
        }
        for k in range(SCORED_HOURS // KP_INTERVAL_HOURS)
    ]


def _kp(rows: list[dict[str, Any]] | None = None, *, observations: Any = None) -> Any:
    frame = RecordFrame(rows if rows is not None else _kp_rows())
    frame.attrs["producing_artifact"] = "gfz_kp_provisional"
    if observations is not None:
        frame.attrs["observations"] = observations
    return frame


def _build(
    *,
    features: dict[str, Any] | None = None,
    experiment: dict[str, Any] | None = None,
    target: Any = None,
    drivers: dict[str, Any] | None = None,
    matrix: Any = None,
    spec: FrameSpec | None = None,
) -> Any:
    """The ONE call every control in this module goes through: the designated enforcement
    boundary, with exactly one input mutated per test."""
    snapshot = synthetic_snapshot(
        features=features if features is not None else _features(), experiment=experiment
    )
    return build_features(
        target if target is not None else _target(),
        drivers=drivers if drivers is not None else {"kp": _kp()},
        registry={},
        matrix=_matrix() if matrix is None else matrix,
        spec=spec or _spec(),
        partitions=PARTITIONS,
        snapshot=snapshot,
        parity_tolerance=0.0,
    )


def test_harness_happy_path_builds_so_every_mutant_below_isolates_one_change() -> None:
    """The control control: without a mutant the boundary PASSES, so each raise below is
    attributable to the single injected violation and not to a broken fixture."""
    bundle = _build()
    assert bundle.transform_id is None
    assert bundle.excluded_counts["excluded_before_scored_start"] == SYNTH_WINDOW_HOURS
    assert bundle.excluded_counts["excluded_incomplete_windows"] == 0


# =========================================================================================
# TA-33 — feature-dictionary closure (FR-P1-04-12; R-76)
#
# TE §19: "Prohibited: a field outside the §6.2 dictionary, or a tensor derived from one,
# entering training or inference; and a tuned history window. ... Expected: construction
# RAISES rather than passing silently, and the tuned-window run FAILS rather than
# proceeding."
# =========================================================================================


@pytest.mark.parametrize(
    ("mutant_name", "mutant_entry", "bites"),
    [
        pytest.param(
            "cloud_cover",
            {"dictionary_row": "cloud", "normalization": "none"},
            "outside the TE 6.2 dictionary",
            id="ta33-row-outside-the-closed-table",
        ),
        pytest.param(
            "iri_vtec",
            {"dictionary_row": "kp_safe", "source_series": "kp", "normalization": "none"},
            "IRI-derived field",
            id="ta33-iri-prefixed-field-on-a-legitimate-row",
        ),
        pytest.param(
            # The project's OWN canonical IRI field name (TE 6.2 row identity;
            # `configs/experiment.yaml` `benchmark_b01.output_field`). It neither starts
            # with `iri_` nor tokenises to a bare `iri`, so the narrower name filter that
            # shipped before this module let it through — and on the `target_support` row
            # it would have reached the dictionary intact. See ENFORCEMENT ADDED.
            "iri2016_t_plus_1_tecu",
            {
                "dictionary_row": "target_support",
                "source_column": "valid_observation_count",
                "normalization": "none",
                "lag_hours": 1,
            },
            "IRI-derived field",
            id="ta33-canonical-iri2016-name-on-the-unconstrained-support-row",
        ),
        pytest.param(
            "ssn_daily",
            {"dictionary_row": "ssn", "normalization": "none"},
            "REMOVED",
            id="ta33-removed-ssn-row",
        ),
        pytest.param(
            "glon",
            {"dictionary_row": "station_lat", "normalization": "none"},
            "raw longitude",
            id="ta33-raw-longitude-column",
        ),
    ],
)
def test_ta33_a_field_outside_the_dictionary_is_refused_at_the_builder(
    mutant_name: str, mutant_entry: dict[str, Any], bites: str
) -> None:
    """MUTANT: one extra dictionary field that is not a §6.2 row identity — an invented row,
    an IRI-derived field wearing a legitimate row, the REMOVED `ssn` row, and a raw-longitude
    column (longitude enters ONLY through `lst_sin`/`lst_cos`).

    BITES: a builder that admitted a field on the strength of its NAME, or that treated an
    unknown row as an unremarkable pass-through. The input space is closed BY ROW.
    """
    features = _features(feature_dictionary=_dictionary(**{mutant_name: mutant_entry}))
    with pytest.raises(LeakageError) as excinfo:
        _build(features=features)
    assert bites in str(excinfo.value)
    assert mutant_name in str(excinfo.value)


def test_ta33_a_tuned_history_window_fails_rather_than_proceeding() -> None:
    """MUTANT: `experiment.yaml` places `window_length_hours` inside a hyperparameter grid.

    BITES: a run that tuned the history length. Vision §8.1 — "History length is not a tuned
    hyperparameter": the window is ONE frozen value per feature-set ID, shared across every
    model family, and it appears in NO grid (R-76; TS-F-03). The run must FAIL, not proceed.
    """
    with pytest.raises(LeakageError) as excinfo:
        _build(
            experiment={"grids": {"M-06": {"units": [32, 64], "window_length_hours": [24, 48]}}}
        )
    message = str(excinfo.value)
    assert "grid" in message and "window_length_hours" in message

    # and the sibling mutant: a grid axis named for the window under another spelling
    with pytest.raises(LeakageError):
        _build(experiment={"grids": {"M-06": {"history_window": [24, 48]}}})


def test_ta33_no_emitted_column_escapes_the_closed_table() -> None:
    """The positive limb of closure, asserted over the ACTUAL output rather than assumed:
    every provenance stamp on the emitted bundle names a row from the closed §6.2 table, and
    the provenance key set EQUALS the matrix column set — so a column cannot reach a model
    without a row identity, and a stamp cannot go missing (SD-F-02)."""
    bundle = _build()
    from src.features._frames import columns_of

    keys = {"interval_start_utc", "station_id"}
    feature_columns = {c for c in columns_of(bundle.matrix) if c not in keys}
    assert feature_columns == set(bundle.provenance)
    for column, stamp in bundle.provenance.items():
        assert stamp["dictionary_row"] in SECTION_6_2_ROWS, column


# =========================================================================================
# TA-34 — target-derived lag contract (FR-P1-04-13; R-77)
#
# TE §19: "Prohibited: a carried-forward `vtec_lag_*` value, and an incomplete `vtec_seq_24`
# window admitted rather than excluded. ... Expected: the carried-forward value FAILS; the
# incomplete window is EXCLUDED AND COUNTED. The <= 3 h carry-forward allowance is scoped to
# external drivers and must never reach `vtec_lag_*`."
# =========================================================================================


def test_ta34_a_vtec_lag_field_cannot_be_routed_onto_the_driver_carry_forward_path() -> None:
    """MUTANT: a dictionary field NAMED `vtec_lag_2h` declared on a DRIVER row (`kp_safe`) —
    the only route by which a target lag could reach the bounded carry-forward at all, since
    a field's class is resolved from its declared row and not from anything the config says
    about it.

    BITES: a builder that resolved the field class from a config-supplied label, or that
    matched `vtec_lag` by prefix and let the declared row disagree. The route is closed at
    the name/row agreement check, before any value is carried.
    """
    features = _features(
        feature_dictionary=_dictionary(
            vtec_lag_2h={
                "dictionary_row": "kp_safe",
                "source_series": "kp",
                "normalization": "none",
            }
        )
    )
    with pytest.raises(LeakageError) as excinfo:
        _build(features=features)
    assert "disagrees with its declared row" in str(excinfo.value)


def test_ta34_every_target_derived_field_resolves_to_the_target_class_not_driver() -> None:
    """The invariant the route above depends on, asserted directly rather than trusted: the
    class of `vtec_lag` and `vtec_seq_24` comes from the CODE's closed row table, so no
    configuration can reclassify a target lag as a driver."""
    assert SECTION_6_2_ROWS["vtec_lag"] is FieldClass.target
    assert SECTION_6_2_ROWS["vtec_seq_24"] is FieldClass.target


def test_ta34_the_carry_forward_boundary_itself_refuses_a_target_lag() -> None:
    """MUTANT: a target-class series handed straight to the carry-forward entry point, the
    guard's OWN public surface — invocation proven at each boundary, not once in the middle.

    BITES: reading FR-P1-04-3's "<= 3 h, then exclude" as a general gap-filling allowance.
    It is scoped to external drivers; a target-derived window is EXCLUDED and counted.
    """
    hourly = {
        SCORED_START + dt.timedelta(hours=h): (None if h == 2 else float(h)) for h in range(6)
    }
    with pytest.raises(LeakageError) as excinfo:
        carry_forward(hourly, field_class=FieldClass.target, bound_h=3, feature="vtec_lag_1h")
    assert "excluded and counted" in str(excinfo.value)
    for other in (FieldClass.station, FieldClass.time, FieldClass.support, FieldClass.diagnostic):
        with pytest.raises(LeakageError):
            carry_forward(hourly, field_class=other, bound_h=3, feature="vtec_lag_1h")


def test_ta34_an_incomplete_sequence_window_is_excluded_and_counted_never_filled() -> None:
    """MUTANT: a hole punched in the target series, so the 24 rows whose window reaches the
    missing hour cannot be completed.

    BITES: a builder that filled the gap — by carry-forward, by interpolation, or by
    shortening the window — and produced a row that LOOKS like a 24-step history. The rows
    must be ABSENT from the matrix and PRESENT in the exclusion count; a silent fill and a
    correct exclusion are indistinguishable from the metric alone.

    The expected count is DERIVED from the window length, never carried: a hole at hour H
    makes exactly `window_length` rows (H+1 .. H+window_length) incompletable, and row H
    itself is absent because its record is the one removed.
    """
    hole = 60
    assert hole > SYNTH_WINDOW_HOURS  # the hole is inside the scored, non-excluded region
    assert hole + SYNTH_WINDOW_HOURS < SCORED_HOURS  # ... and its whole shadow fits inside

    bundle = _build(target=_target(drop_hours=(hole,)))
    assert bundle.excluded_counts["excluded_incomplete_windows"] == SYNTH_WINDOW_HOURS

    emitted = {row["interval_start_utc"] for row in records_of(bundle.matrix)}
    shadow = {
        (SCORED_START + dt.timedelta(hours=h)).isoformat()
        for h in range(hole, hole + SYNTH_WINDOW_HOURS + 1)
    }
    assert emitted & shadow == set(), "an incompletable window was admitted rather than excluded"
    # the rows on either side of the shadow are untouched: the exclusion is bounded, not a
    # silent truncation of the frame
    first_recovered = hole + SYNTH_WINDOW_HOURS + 1
    assert (SCORED_START + dt.timedelta(hours=hole - 1)).isoformat() in emitted
    assert (SCORED_START + dt.timedelta(hours=first_recovered)).isoformat() in emitted


# =========================================================================================
# TA-35 — support-field rules (FR-P1-04-16; R-78)
#
# TE §19: "Prohibited: a support field used as a model input without a recorded G-04
# approval ID, and a support field read at or beyond hour t. ... Expected: feature
# construction FAILS in both cases; target-hour quality fields remain permanently forbidden."
# =========================================================================================

_FREEZE = "2001-02-01T00:00:00Z"
_APPROVAL = {"approval_id": "G-04-001", "recorded_utc": "2001-01-01T00:00:00Z"}


def _support(**fields: Any) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "dictionary_row": "target_support",
        "source_column": "valid_observation_count",
        "normalization": "none",
        "lag_hours": 1,
    }
    entry.update(fields)
    return entry


def _with_support(entry: dict[str, Any], *, freeze: str | None = _FREEZE) -> dict[str, Any]:
    features = _features(
        feature_dictionary=_dictionary(support_count=entry),
        permitted_producers=_producers(target_support=["phase1_hourly_target"]),
    )
    if freeze is not None:
        features["feature_set_freeze_utc"] = freeze
    return features


def test_ta35_an_unapproved_support_field_never_enters_the_model_input_set() -> None:
    """MUTANT: a support field declared with NO approval block at all.

    BITES: a builder whose default was "admit unless told otherwise". R-78 rule 1 makes the
    DEFAULT the mechanism: the field is diagnostic, it is silently excluded from the input
    set, and no model can see it. Asserted on the emitted bundle, not on an intention.
    """
    bundle = _build(features=_with_support(_support()))
    assert "support_count" not in bundle.provenance
    from src.features._frames import columns_of

    assert "support_count" not in set(columns_of(bundle.matrix))


def test_ta35_an_approval_without_a_recorded_id_or_timestamp_fails_separately() -> None:
    """MUTANT: an approval block ASSERTED but incomplete — first with no `approval_id`, then
    with no `recorded_utc`.

    BITES: a presence check on the word "approval". The ID is the record of the G-04
    decision, and the timestamp is what makes "recorded BEFORE the freeze" assertable; a
    build that accepted either as optional would admit a support field on a claim rather
    than on a decision. Two separate assertions, two separate failures.
    """
    with pytest.raises(LeakageError) as no_id:
        _build(features=_with_support(_support(approval={"recorded_utc": "2001-01-01T00:00:00Z"})))
    assert "approval_id" in str(no_id.value)

    with pytest.raises(LeakageError) as no_stamp:
        _build(features=_with_support(_support(approval={"approval_id": "G-04-001"})))
    assert "recorded_utc" in str(no_stamp.value)


def test_ta35_an_approval_recorded_after_the_feature_set_freeze_fails_on_ordering() -> None:
    """MUTANT: a complete, well-formed approval — recorded AFTER the feature-set freeze.

    BITES: exactly what a presence check passes. An approval granted after the feature set
    was frozen is a retrofit, and "recorded before the freeze" exists to prevent it.
    """
    entry = _support(approval={"approval_id": "G-04-001", "recorded_utc": "2001-03-01T00:00:00Z"})
    with pytest.raises(LeakageError) as excinfo:
        _build(features=_with_support(entry))
    assert "PRECEDE" in str(excinfo.value)


def test_ta35_a_support_field_read_at_or_beyond_hour_t_fails() -> None:
    """MUTANT: an APPROVED support field with `lag_hours: 0` — read at the target hour.

    BITES: the leak the approval machinery would otherwise launder. A support field is
    readable over hours <= t only; a read at hour t is the target hour's own quality
    information, and approval does not make it causal (R-78 rule 2).
    """
    with pytest.raises(LeakageError) as excinfo:
        _build(features=_with_support(_support(lag_hours=0, approval=dict(_APPROVAL))))
    assert "hours <= t" in str(excinfo.value)


def test_ta35_a_target_hour_quality_field_is_forbidden_even_when_properly_approved() -> None:
    """MUTANT: a target-hour quality field with a VALID approval recorded before the freeze —
    every other rule satisfied.

    BITES: treating the approval gate as a universal override. R-78 rule 4 is PERMANENT:
    target-hour quality is future information and no approval reaches it.
    """
    entry = _support(support_kind="target_hour_quality", approval=dict(_APPROVAL))
    with pytest.raises(LeakageError) as excinfo:
        _build(features=_with_support(entry))
    assert "permanently forbidden" in str(excinfo.value)


def test_ta35_a_correctly_approved_lagged_support_field_does_enter() -> None:
    """The discriminating positive: the four refusals above are not a blanket ban. A support
    field with an approval ID, recorded before the freeze, read at t-1, enters WITH its
    provenance — so the negative controls prove a rule, not an accident."""
    bundle = _build(features=_with_support(_support(approval=dict(_APPROVAL))))
    assert bundle.provenance["support_count"]["dictionary_row"] == "target_support"


# =========================================================================================
# TA-36 — driver alignment contract (FR-P1-04-17, D-10.2)
#
# TE §19: "Prohibited: a Kp value repeated outside its own 3-hour interval; a Dst value
# shifted to a neighbouring hour; any interpolation of a driver series at any stage. ...
# Expected: each FAILS; a code-level check finds no interpolation call on any driver series.
# ... the PRIMARY REJECTION TEST [sits] AT THE FEATURE-BUILDING ENFORCEMENT BOUNDARY."
# =========================================================================================


def test_ta36_a_value_repeated_outside_its_own_interval_is_refused_at_the_builder() -> None:
    """MUTANT: interval 0's value held for six hours instead of three, so hours 3, 4 and 5
    carry interval 0's value while interval 1's own value covers them.

    BITES: a producer that "repeated the last reading" across an interval boundary. A present
    value maps onto the hourly grid ONLY within its own defined interval (D-10.2). Distinct
    from FR-P1-04-3's carry-forward, which governs a MISSING value — the two are tested
    separately so neither passes on the other's evidence.
    """
    repeated = {h: 100.0 for h in range(KP_INTERVAL_HOURS, 2 * KP_INTERVAL_HOURS)}
    frame = _kp(_kp_rows(repeated), observations=_kp_observations())
    with pytest.raises(AlignmentError) as excinfo:
        _build(drivers={"kp": frame})
    assert "outside the interval" in str(excinfo.value)


def test_ta36_a_value_shifted_to_a_neighbouring_hour_is_refused_at_the_builder() -> None:
    """MUTANT: a single hour carrying the NEXT interval's value — the Dst-style one-hour
    shift, indistinguishable from correct data by any completeness or range check.

    BITES: "shifted to a neighbouring hour for convenience" (D-10.2). One hour is enough:
    the check is per epoch, not per series.
    """
    shifted_hour = 10
    next_interval_value = float(100 + (shifted_hour // KP_INTERVAL_HOURS) + 1)
    frame = _kp(_kp_rows({shifted_hour: next_interval_value}), observations=_kp_observations())
    with pytest.raises(AlignmentError) as excinfo:
        _build(drivers={"kp": frame})
    assert (SCORED_START + dt.timedelta(hours=shifted_hour)).isoformat() in str(excinfo.value)


def test_ta36_an_interpolated_value_that_still_satisfies_its_declared_lag_is_refused() -> None:
    """THE SUBTLE ONE. MUTANT: a properly lagged `*_safe` series — produced by the one
    lagged-selection owner, declaring the same 3 h lag the availability matrix declares, every
    row's `available_at_utc` exactly source-end + lag and at or before its origin — in which
    ONE row's value has been replaced by the midpoint of two neighbouring observations.

    BITES: every lag-based check there is. The series satisfies its declared lag, its
    availability arithmetic reconciles, and the interpolated value sits inside the plausible
    range; a lag assertion cannot see it. What catches it is TRACEABILITY — the value must
    equal the observation on the source interval the row itself records. A series can satisfy
    its stated lag while being built from interpolated or reanalysed values, which is
    invisible in validation and fatal on discovery.
    """
    observations = _kp_observations()
    epochs = [SCORED_START + dt.timedelta(hours=h) for h in range(SCORED_HOURS)]
    rows = select_lagged_series(observations, epochs=epochs, safe_lag_hours=KP_INTERVAL_HOURS)

    def _lagged(rows_in: list[dict[str, Any]]) -> Any:
        frame = RecordFrame([dict(r) for r in rows_in])
        frame.attrs["producing_artifact"] = "gfz_kp_provisional"
        frame.attrs["observations"] = observations
        frame.attrs["selection"] = {
            "rule": SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG,
            "safe_lag_hours": KP_INTERVAL_HOURS,
        }
        return frame

    matrix = (
        AvailabilityRow(
            feature="kp_safe",
            observation_timestamp="x",
            publication_timestamp="y",
            release_status="provisional",
            safe_lag_hours=float(KP_INTERVAL_HOURS),
            actual_lag_hours=float(KP_INTERVAL_HOURS),
            selection_rule=SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG,
            lag_reference_instant="interval_end_utc",
        ),
    )

    # the unmutated series passes: the refusal below is the interpolation, nothing else
    _build(drivers={"kp": _lagged(rows)}, matrix=matrix)

    victim = next(index for index, row in enumerate(rows) if row["value"] is not None)
    interpolated = list(rows)
    original = float(interpolated[victim]["value"])
    interpolated[victim] = {**interpolated[victim], "value": original + 0.5}  # a midpoint fill

    with pytest.raises(AlignmentError) as excinfo:
        _build(drivers={"kp": _lagged(interpolated)}, matrix=matrix)
    message = str(excinfo.value)
    assert "does not trace to an observation on the recorded source interval" in message

    # ... and the lag limb it defeats is genuinely intact: the SAME row, unmutated, has an
    # `available_at_utc` of exactly source end + the declared lag, at or before its origin.
    row = rows[victim]
    source_end = dt.datetime.fromisoformat(str(row["source_interval_end_utc"]))
    available_at = dt.datetime.fromisoformat(str(row["available_at_utc"]))
    origin = dt.datetime.fromisoformat(str(row["interval_start_utc"]))
    assert available_at == source_end + dt.timedelta(hours=KP_INTERVAL_HOURS)
    assert available_at <= origin


#: Call names that would interpolate, pad or reconstruct a driver series. `apply_carry_forward`
#: is NOT here: it is the one SANCTIONED fill, bounded by configuration and recorded epoch by
#: epoch, and R-58 limb 3's conservation invariant is what keeps it honest.
_INTERPOLATION_CALLS: frozenset[str] = frozenset(
    {
        "interp",
        "interpolate",
        "fillna",
        "ffill",
        "bfill",
        "pad",
        "backfill",
        "reindex",
        "resample",
        "nan_to_num",
        "asfreq",
        "rolling",
    }
)

#: The driver code path TA-36's code-level check covers: everything that touches a driver
#: series between the provider bytes and the model input space.
_DRIVER_PATH_MODULES: tuple[Path, ...] = (
    REPO_ROOT / "src" / "features",
    REPO_ROOT / "src" / "external" / "spaceweather.py",
)


def test_ta36_no_interpolation_call_exists_anywhere_on_the_driver_path() -> None:
    """TA-36's third limb, which is a CODE-LEVEL check by its own terms: "a code-level check
    finds no interpolation call on any driver series".

    An AST walk over every `Call` on the driver path, resolving the callee name, because a
    text grep cannot tell `# never backfill from future final values` (prose, and there is
    plenty of it here) from `series.backfill()` (the violation). Any hit is reported with its
    file and line, naming the violated expectation.
    """
    offenders: list[str] = []
    modules = sorted(
        {
            path
            for root in _DRIVER_PATH_MODULES
            for path in (root.rglob("*.py") if root.is_dir() else [root])
        }
    )
    assert modules, "the driver-path module list is empty; the scan would pass vacuously"
    for module in modules:
        tree = ast.parse(module.read_text(encoding="utf-8"), filename=str(module))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            name = (
                func.attr
                if isinstance(func, ast.Attribute)
                else func.id
                if isinstance(func, ast.Name)
                else None
            )
            if name in _INTERPOLATION_CALLS:
                offenders.append(
                    f"{module.relative_to(REPO_ROOT).as_posix()}:{node.lineno}: {name}()"
                )
    assert offenders == [], (
        f"interpolation-class call(s) found on the driver path: {offenders}; any "
        f"interpolation of a driver series at any stage is prohibited (TA-36, FR-P1-04-17, "
        f"D-10.2) — the only sanctioned fill is the bounded, recorded carry-forward"
    )


# =========================================================================================
# The driver-CONSUMING guards declared in `spaceweather.py`'s "Boundary split" section
# (TC-12, `binding: hard`; R-63's negative control). Wired here, so proven here.
# =========================================================================================


def test_tc12_a_duplicate_driver_epoch_is_refused_and_the_epoch_is_named() -> None:
    """MUTANT: two driver rows at ONE epoch, the second carrying a different value.

    BITES: the single silent failure in the codebase's driver ingest. `_hourly_series` built
    its `{epoch: value}` index by plain assignment, so the second row won with no trace, and
    `build_features` then broadcast that winner to every station's row — a changed number
    with no record anywhere. The same codebase already refuses this shape twice elsewhere
    (`windows.build_windows` on a duplicate `(station, epoch)`; `spaceweather.
    align_interval_series` on a second value mapping onto one epoch, "because a silent winner
    would shift a value outside its own interval"); this was the one path that did neither.
    """
    rows = _kp_rows()
    duplicate = dict(rows[7])
    duplicate["value"] = 999.0
    with pytest.raises(IntegrityError) as excinfo:
        _build(drivers={"kp": _kp([*rows, duplicate])})
    message = str(excinfo.value)
    assert "duplicate epoch" in message
    assert (SCORED_START + dt.timedelta(hours=7)).isoformat() in message
    assert "TC-12" in message
    # the BASE class, deliberately: `DriverError` is not declared while its scope is
    # contested upstream (`spaceweather.py` module docstring, Q1 = A), and a subclass here
    # would pre-empt that reconciliation.
    assert type(excinfo.value) is IntegrityError


def test_tc12_a_driver_value_differing_across_cells_at_one_epoch_is_refused() -> None:
    """MUTANT: a post-join frame in which one epoch carries a different driver value in one
    cell than in another.

    BITES: any per-cell driver path — a per-station interpolation, a per-cell fallback, a
    join that silently produced a cartesian product of partly-differing rows. TC-12
    (`binding: hard`): driver series are time-indexed ONLY, one value per epoch, identical
    across all three cells; a station performance difference must never be attributable to
    local forcing the dataset does not contain.

    Asserted by DIRECT CALL on the guard's own public surface, because the production join
    broadcasts a single epoch-keyed value to every station and so cannot produce a divergent
    frame without editing production code. The companion test below proves that
    `build_features` actually INVOKES this guard — correctness here, invocation there, since
    a guard module alone fails open on a forgotten call.
    """
    epoch = SCORED_START.isoformat()
    joined = [
        {"interval_start_utc": epoch, "station_id": "S1", "kp_safe": 100.0},
        {"interval_start_utc": epoch, "station_id": "S2", "kp_safe": 100.5},
    ]
    with pytest.raises(IntegrityError) as excinfo:
        assert_identical_across_cells(
            joined, epoch_key="interval_start_utc", value_key="kp_safe", cell_key="station_id"
        )
    assert "differ across cells" in str(excinfo.value)

    identical = [{**row, "kp_safe": 100.0} for row in joined]
    assert (
        assert_identical_across_cells(
            identical, epoch_key="interval_start_utc", value_key="kp_safe", cell_key="station_id"
        )
        is None
    )


def test_tc12_build_features_invokes_the_joined_grid_guard_on_the_post_join_frame(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The invocation half. A spy wraps the guard at `build_features`' own import site and
    then DELEGATES to the real function, so the build still checks while the call is recorded.

    Asserted: the guard runs once per driver field, and the rows it is handed are the
    POST-JOIN frame — they carry both stations at a shared epoch. Handing it the pre-join
    `{epoch: value}` mapping would satisfy the rule vacuously, which is the mistake this
    assertion exists to catch.
    """
    seen: list[dict[str, Any]] = []
    real = assert_identical_across_cells

    def spy(joined_rows: Any, **kwargs: Any) -> None:
        seen.append({"rows": list(joined_rows), **kwargs})
        real(joined_rows, **kwargs)

    monkeypatch.setattr("src.features.build.assert_identical_across_cells", spy)
    _build(target=_target(stations=("S1", "S2")))

    assert len(seen) == 1, "the guard must run once per driver field"
    call = seen[0]
    assert call["value_key"] == "kp_safe"
    assert call["cell_key"] == "station_id"
    stations_by_epoch: dict[str, set[str]] = {}
    for row in call["rows"]:
        stations_by_epoch.setdefault(row["interval_start_utc"], set()).add(row["station_id"])
    assert any(
        cells == {"S1", "S2"} for cells in stations_by_epoch.values()
    ), "the guard was handed a frame with no shared epoch across cells; it would pass vacuously"
