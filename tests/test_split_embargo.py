"""FR-P1-04-5 / WS-12 / TA-11: exact calendar folds, the embargo excluded AND counted, the
six-partitions/five-rows rule, both bounds from configuration — and the M10 synthetic
partition fixture (Q12 = C) that `test_train_only_transforms.py` reuses.

PURPOSE. `src/data/splits.py` is exercised against a SYNTHETIC partition table over a
synthetic calendar year (R-80's shape on synthetic dates), because the real values enter
`configs/data.yaml` only at the split-boundary freeze and this module must never carry them.
Every hard rule gets a negative control that proves the violation is CAUGHT (team.md):

* `build_partitions` REFUSES while `data.partitions` / `experiment.embargo_hours` are absent
  or `TBD -- freeze gate` -- the refusal, not a default (R-83; TE 18.3).
* Exactly six partitions come back; the split manifest enumerates exactly five; six rows
  fail and four rows fail (ADR-11 M5).
* The embargo's first `embargo_hours` are EXCLUDED and the count is emitted; a manifest that
  omits a fold's count fails.
* `DEC.train_end != REFIT.train_end` fails (R-80's Recommendation-25 structural bar); a month
  with two evaluation roles fails; a month with none fails; a differing `train_start` fails.
* `assert_membership_from_timestamps` derives nothing and raises on a row filed under the
  wrong partition -- the defect that filed locked-month records by directory name.
* The strict-subset control R-83 names is asserted through `fit_transforms` in
  `test_train_only_transforms.py`; this module proves both bounds are READ from the
  `Partition` and that a `Partition` cannot be built without them.

INPUTS. Synthetic in-memory `ConfigSnapshot`s and record sequences only. No December 2022
content, no restricted-root path, no real config value. RE-RUN: pure functions; the
project's `configs/` and registry are never written.

WHAT NO TEST HERE DISCHARGES. WS-12 and TA-11 stay `Pending`. A passing run on the
interpreter used here is smoke evidence, never governed evidence.

Run: pytest tests/test_split_embargo.py -rs
"""

from __future__ import annotations

import datetime as dt
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import (  # noqa: E402
    TBD_SENTINEL,
    ConfigSnapshot,
    PartitionError,
)
from src.data.splits import (  # noqa: E402
    FITTING_PARTITION_IDS,
    LOCKED_ID,
    PARTITION_IDS,
    REFIT_ID,
    Partition,
    PartitionKind,
    apply_embargo,
    assert_membership_from_timestamps,
    assert_split_manifest,
    build_partitions,
    build_split_manifest,
    embargo_exclusions,
    embargo_window,
    locked_partition_record,
    partition_by_id,
    training_range,
    validation_month_range,
)

UTC = dt.UTC

# --- the M10 synthetic fixture (Q12 = C; authored here, reused by the transforms tests) ---

#: A SYNTHETIC calendar year. R-80's frozen table is calendar 2022 and enters configs/data.yaml
#: only at its freeze; this fixture reproduces the table's SHAPE (four expanding folds, the
#: refit, the locked month) on another year so the contract can be exercised without carrying
#: or touching any 2022 value. The embargo and window values are fixture parameters here.
SYNTH_YEAR = 2001
SYNTH_EMBARGO_HOURS = 24
SYNTH_WINDOW_HOURS = 24


def _d(month: int, day: int) -> str:
    return dt.date(SYNTH_YEAR, month, day).isoformat()


def synthetic_partition_block() -> dict[str, dict[str, Any]]:
    """The six-entry `data.partitions` block over the synthetic year."""
    def entry(kind: str, end: tuple[int, int], month: tuple[int, int] | None) -> dict[str, Any]:
        return {
            "kind": kind,
            "train_start": _d(1, 1),
            "train_end": _d(*end),
            "validation_month": _d(*month) if month else None,
        }

    return {
        "F1": entry("fold", (3, 31), (4, 1)),
        "F2": entry("fold", (6, 30), (7, 1)),
        "F3": entry("fold", (9, 30), (10, 1)),
        "F4": entry("fold", (10, 31), (11, 1)),
        "REFIT": entry("refit", (11, 30), None),
        "DEC": entry("locked", (11, 30), (12, 1)),
    }


def synthetic_snapshot(
    *,
    data: Mapping[str, Any] | None = None,
    features: Mapping[str, Any] | None = None,
    experiment: Mapping[str, Any] | None = None,
) -> ConfigSnapshot:
    """A frozen `ConfigSnapshot` over synthetic values; nothing is read from `configs/`."""
    base_data: dict[str, Any] = {"partitions": synthetic_partition_block()}
    base_experiment: dict[str, Any] = {
        "embargo_hours": SYNTH_EMBARGO_HOURS,
        "window_length_hours": SYNTH_WINDOW_HOURS,
        "grids": TBD_SENTINEL,
    }
    if data:
        base_data.update(data)
    if experiment:
        base_experiment.update(experiment)
    return ConfigSnapshot(
        data=base_data,
        features=dict(features or {}),
        experiment=base_experiment,
        seeds={},
        hashes={},
        snapshot_dir=Path("."),
        resolved_roots={},
        platform="local",
    )


def synthetic_partitions() -> tuple[Partition, ...]:
    return build_partitions(synthetic_snapshot())


def _ts(month: int, day: int, hour: int = 0) -> dt.datetime:
    return dt.datetime(SYNTH_YEAR, month, day, hour, tzinfo=UTC)


# --- refusals while unfrozen (R-83; TE 18.3) --------------------------------------------


def test_partitions_block_absent_refuses_naming_the_field() -> None:
    snapshot = synthetic_snapshot(data={"partitions": None})
    with pytest.raises(PartitionError) as excinfo:
        build_partitions(snapshot)
    assert "configs/data.yaml: partitions" in str(excinfo.value)
    assert "never derived from the data" in str(excinfo.value)


def test_partitions_block_tbd_refuses() -> None:
    snapshot = synthetic_snapshot(data={"partitions": TBD_SENTINEL})
    with pytest.raises(PartitionError):
        build_partitions(snapshot)


def test_embargo_hours_tbd_refuses() -> None:
    snapshot = synthetic_snapshot(experiment={"embargo_hours": TBD_SENTINEL})
    with pytest.raises(PartitionError) as excinfo:
        build_partitions(snapshot)
    assert "embargo_hours" in str(excinfo.value)


@pytest.mark.parametrize("field", ["train_start", "train_end", "kind"])
def test_a_missing_bound_or_kind_refuses(field: str) -> None:
    """Both bounds are READ from configuration; an absent one is a refusal, never Jan-1."""
    block = synthetic_partition_block()
    block["F2"][field] = TBD_SENTINEL
    with pytest.raises(PartitionError) as excinfo:
        build_partitions(synthetic_snapshot(data={"partitions": block}))
    assert f"partitions.F2.{field}" in str(excinfo.value)


def test_real_repository_configs_refuse_today() -> None:
    """The repository's own `configs/` carries no partition block yet: the refusal fires.

    Reads the real files through a bare YAML parse (no snapshot directory is written): this
    is a test of the refusal path, not a governed run.
    """
    yaml = pytest.importorskip("yaml")
    configs = REPO_ROOT / "configs"
    data = yaml.safe_load((configs / "data.yaml").read_text(encoding="utf-8"))
    experiment = yaml.safe_load((configs / "experiment.yaml").read_text(encoding="utf-8"))
    snapshot = ConfigSnapshot(
        data=data,
        features={},
        experiment=experiment,
        seeds={},
        hashes={},
        snapshot_dir=Path("."),
        resolved_roots={},
        platform="local",
    )
    with pytest.raises(PartitionError):
        build_partitions(snapshot)


# --- six partitions, five rows (ADR-11 M5) ----------------------------------------------


def test_build_partitions_returns_exactly_six_in_the_closed_order() -> None:
    partitions = synthetic_partitions()
    assert len(partitions) == 6
    assert tuple(p.partition_id for p in partitions) == PARTITION_IDS
    assert len(PARTITION_IDS) == 6 and len(FITTING_PARTITION_IDS) == 5
    kinds = {p.partition_id: p.kind for p in partitions}
    assert kinds[REFIT_ID] is PartitionKind.refit and kinds[LOCKED_ID] is PartitionKind.locked
    assert all(kinds[f] is PartitionKind.fold for f in ("F1", "F2", "F3", "F4"))


def test_only_the_refit_carries_no_validation_month() -> None:
    partitions = synthetic_partitions()
    without = [p.partition_id for p in partitions if p.validation_month is None]
    assert without == [REFIT_ID]


def test_both_bounds_are_read_from_configuration() -> None:
    """R-83: the Partition carries train_start AND train_end, both from the block."""
    partitions = synthetic_partitions()
    block = synthetic_partition_block()
    for partition in partitions:
        entry = block[partition.partition_id]
        assert partition.train_start.isoformat() == entry["train_start"]
        assert partition.train_end.isoformat() == entry["train_end"]
        assert partition.embargo_hours == SYNTH_EMBARGO_HOURS


def test_partition_dataclass_has_no_embargo_default() -> None:
    """The approved `= 24` default is deliberately not reproduced (project.md Forbidden)."""
    with pytest.raises(TypeError):
        Partition(  # type: ignore[call-arg]
            partition_id="F1",
            kind=PartitionKind.fold,
            train_start=dt.date(SYNTH_YEAR, 1, 1),
            train_end=dt.date(SYNTH_YEAR, 3, 31),
            validation_month=dt.date(SYNTH_YEAR, 4, 1),
        )


def test_split_manifest_enumerates_exactly_five_and_never_dec() -> None:
    partitions = synthetic_partitions()
    counts = {"F1": 24, "F2": 24, "F3": 23, "F4": 24}
    manifest = build_split_manifest(partitions, excluded_embargo_rows=counts)
    ids = [row["partition_id"] for row in manifest["partitions"]]
    assert ids == list(FITTING_PARTITION_IDS)
    assert manifest["partition_count"] == 5
    assert LOCKED_ID not in ids
    assert manifest["partitions"][2]["excluded_embargo_rows"] == 23
    assert manifest["partitions"][4]["excluded_embargo_rows"] is None  # REFIT: scored nowhere
    assert_split_manifest(manifest)


def test_six_row_manifest_fails() -> None:
    partitions = synthetic_partitions()
    manifest = build_split_manifest(
        partitions, excluded_embargo_rows={"F1": 1, "F2": 1, "F3": 1, "F4": 1}
    )
    six = dict(manifest)
    six["partitions"] = [*manifest["partitions"], {"partition_id": LOCKED_ID, "kind": "locked"}]
    with pytest.raises(PartitionError) as excinfo:
        assert_split_manifest(six)
    assert LOCKED_ID in str(excinfo.value)


def test_four_row_manifest_fails() -> None:
    partitions = synthetic_partitions()
    manifest = build_split_manifest(
        partitions, excluded_embargo_rows={"F1": 1, "F2": 1, "F3": 1, "F4": 1}
    )
    four = dict(manifest)
    four["partitions"] = manifest["partitions"][:4]
    with pytest.raises(PartitionError):
        assert_split_manifest(four)


def test_omitting_a_folds_excluded_count_fails() -> None:
    partitions = synthetic_partitions()
    with pytest.raises(PartitionError) as excinfo:
        build_split_manifest(partitions, excluded_embargo_rows={"F1": 1, "F2": 1, "F3": 1})
    assert "excluded-row count omitted" in str(excinfo.value)


def test_locked_record_is_separate_and_names_the_gate_state() -> None:
    partitions = synthetic_partitions()
    record = locked_partition_record(partitions, access_gate_state="G-05 Blocked")
    assert record["partition_id"] == LOCKED_ID
    assert record["recorded_separately_from_split_manifest"] is True
    assert record["evaluated_month"] == _d(12, 1)
    with pytest.raises(PartitionError):
        locked_partition_record(partitions, access_gate_state="   ")


# --- structural rules over the block (no calendar value in the test's logic) --------------


def test_dec_train_end_must_equal_refit_train_end() -> None:
    """R-80 Recommendation 25: a December fit is unrepresentable by the field itself."""
    block = synthetic_partition_block()
    block["DEC"]["train_end"] = _d(11, 15)  # still before the locked month, but not the refit's
    with pytest.raises(PartitionError) as excinfo:
        build_partitions(synthetic_snapshot(data={"partitions": block}))
    assert "DEC.train_end" in str(excinfo.value)


def test_two_evaluation_roles_for_one_month_fails() -> None:
    block = synthetic_partition_block()
    block["F2"]["train_end"] = _d(3, 31)
    block["F2"]["validation_month"] = _d(4, 1)  # same role month as F1
    with pytest.raises(PartitionError) as excinfo:
        build_partitions(synthetic_snapshot(data={"partitions": block}))
    assert "two evaluation roles" in str(excinfo.value)


def test_a_month_with_no_role_fails() -> None:
    """Shrink the refit so a month is neither training-only nor anyone's validation month."""
    block = synthetic_partition_block()
    block["REFIT"]["train_end"] = _d(8, 31)
    block["DEC"]["train_end"] = _d(8, 31)
    with pytest.raises(PartitionError) as excinfo:
        build_partitions(synthetic_snapshot(data={"partitions": block}))
    assert "has NO role" in str(excinfo.value)


def test_validation_month_inside_training_range_fails() -> None:
    block = synthetic_partition_block()
    block["F3"]["validation_month"] = _d(9, 1)
    with pytest.raises(PartitionError):
        build_partitions(synthetic_snapshot(data={"partitions": block}))


def test_non_contiguous_fold_fails() -> None:
    block = synthetic_partition_block()
    block["F1"]["validation_month"] = _d(5, 1)  # leaves April between train_end and validation
    with pytest.raises(PartitionError) as excinfo:
        build_partitions(synthetic_snapshot(data={"partitions": block}))
    assert "contiguous" in str(excinfo.value)


def test_kind_disagreeing_with_id_fails() -> None:
    block = synthetic_partition_block()
    block["F1"]["kind"] = "locked"
    with pytest.raises(PartitionError):
        build_partitions(synthetic_snapshot(data={"partitions": block}))


def test_seventh_partition_id_is_refused() -> None:
    block = synthetic_partition_block()
    block["F5"] = dict(block["F4"])
    with pytest.raises(PartitionError) as excinfo:
        build_partitions(synthetic_snapshot(data={"partitions": block}))
    assert "F5" in str(excinfo.value)


def test_refit_with_a_validation_month_fails() -> None:
    block = synthetic_partition_block()
    block["REFIT"]["validation_month"] = _d(12, 1)
    with pytest.raises(PartitionError):
        build_partitions(synthetic_snapshot(data={"partitions": block}))


def test_partition_by_id_refuses_an_unknown_id() -> None:
    with pytest.raises(PartitionError):
        partition_by_id(synthetic_partitions(), "F9")


# --- the embargo: excluded AND counted ---------------------------------------------------


def test_embargo_window_is_the_first_embargo_hours_of_the_validation_month() -> None:
    f1 = partition_by_id(synthetic_partitions(), "F1")
    start, end = embargo_window(f1)
    assert start == _ts(4, 1, 0)
    assert end - start == dt.timedelta(hours=SYNTH_EMBARGO_HOURS)


def test_embargo_rows_are_excluded_and_counted() -> None:
    f1 = partition_by_id(synthetic_partitions(), "F1")
    first = _ts(4, 1, 0)
    stamps = [first + dt.timedelta(hours=h) for h in range(48)]  # 48 hourly rows into April
    kept, excluded = embargo_exclusions(stamps, f1)
    assert excluded == SYNTH_EMBARGO_HOURS
    assert len(kept) == 48 - SYNTH_EMBARGO_HOURS
    assert min(kept) == SYNTH_EMBARGO_HOURS  # the first kept row is the one after the window


def test_apply_embargo_returns_the_count_beside_the_frame() -> None:
    f4 = partition_by_id(synthetic_partitions(), "F4")
    first = _ts(11, 1, 0)
    rows = [
        {"interval_start_utc": (first + dt.timedelta(hours=h)).isoformat()} for h in range(30)
    ]
    kept, excluded = apply_embargo(rows, f4)
    assert excluded == SYNTH_EMBARGO_HOURS
    assert len(kept) == 30 - SYNTH_EMBARGO_HOURS
    assert all(
        dt.datetime.fromisoformat(r["interval_start_utc"]) >= _ts(11, 2, 0) for r in kept
    )


def test_embargo_on_the_refit_is_refused() -> None:
    refit = partition_by_id(synthetic_partitions(), REFIT_ID)
    with pytest.raises(PartitionError):
        embargo_window(refit)


def test_no_window_crosses_a_boundary() -> None:
    """Training ranges end exactly where validation months begin (end-exclusive datetimes)."""
    for pid in ("F1", "F2", "F3", "F4"):
        partition = partition_by_id(synthetic_partitions(), pid)
        _, train_end = training_range(partition)
        val_start, _ = validation_month_range(partition)
        assert train_end == val_start


# --- membership from record timestamps (never a directory name) --------------------------


def test_membership_passes_rows_inside_the_declared_range() -> None:
    f1 = partition_by_id(synthetic_partitions(), "F1")
    rows = [{"interval_start_utc": _ts(2, 15, h).isoformat()} for h in range(5)]
    assert_membership_from_timestamps(rows, partition=f1, role="train") is None


def test_membership_raises_on_a_row_filed_under_the_wrong_partition() -> None:
    """The `audit_evidence_2022-01/` defect, on synthetic dates: a locked-month row filed
    under a fold fails on its TIMESTAMP, whatever directory it sat in."""
    f1 = partition_by_id(synthetic_partitions(), "F1")
    rows = [
        {"interval_start_utc": _ts(2, 15, 0).isoformat(), "source_dir": "F1"},
        {"interval_start_utc": _ts(12, 5, 0).isoformat(), "source_dir": "F1"},
    ]
    with pytest.raises(PartitionError) as excinfo:
        assert_membership_from_timestamps(rows, partition=f1, role="train")
    assert "row 1" in str(excinfo.value)
    assert "never from the directory" in str(excinfo.value)


def test_membership_score_role_uses_the_validation_month() -> None:
    f1 = partition_by_id(synthetic_partitions(), "F1")
    ok = [{"interval_start_utc": _ts(4, 10, 3).isoformat()}]
    assert_membership_from_timestamps(ok, partition=f1, role="score") is None
    bad = [{"interval_start_utc": _ts(5, 1, 0).isoformat()}]
    with pytest.raises(PartitionError):
        assert_membership_from_timestamps(bad, partition=f1, role="score")


def test_membership_derives_nothing_a_nested_row_passes_every_containing_partition() -> None:
    """R-80's control that must NOT fire: a mid-February row lies in F1..F4 and the refit."""
    row = [{"interval_start_utc": _ts(2, 15, 12).isoformat()}]
    for pid in FITTING_PARTITION_IDS:
        partition = partition_by_id(synthetic_partitions(), pid)
        assert_membership_from_timestamps(row, partition=partition, role="train")


def test_membership_refuses_an_unknown_role_and_a_missing_column() -> None:
    f1 = partition_by_id(synthetic_partitions(), "F1")
    rows = [{"interval_start_utc": _ts(2, 15, 0).isoformat()}]
    with pytest.raises(PartitionError):
        assert_membership_from_timestamps(rows, partition=f1, role="evaluate")
    with pytest.raises(PartitionError):
        assert_membership_from_timestamps([{"other": 1}], partition=f1, role="train")


def test_no_sklearn_splitter_and_no_calendar_constant_in_splits_source() -> None:
    """TS-F-04 / TC-03e: the module uses no scikit-learn splitter and holds no calendar
    year or hard-coded month/embargo value; every calendar value comes from configuration."""
    source = (REPO_ROOT / "src" / "data" / "splits.py").read_text(encoding="utf-8")
    assert "sklearn" not in source and "model_selection" not in source
    assert "2022" not in source and "2001" not in source
    assert "embargo_hours: int = " not in source
