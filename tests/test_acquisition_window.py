"""Acquisition-window conformance for the Madrigal coverage audit.

WHY THIS MODULE IS NEW. `Technical_Environment_and_Research_Implementation` §12
enumerates an exhaustive seventeen-module `tests/` tree, and none of those modules
asserts that the records retrieved for a run window are the records that window asked
for. `test_release_hashes.py` proves bytes are unmutated -- misfiled bytes hash
correctly and it passes. `test_locked_test_guard.py` (WS-18) guards December
*execution*, not acquisition. `test_station_registry.py` covers registry and coverage
population, not the retrieval predicate. Adding this module therefore AMENDS §12's
tree and requires the same supervisor countersignature the project already tracks for
the WS acceptance split and the §1.3 script-count reading. It is recorded as new, not
presented as if it were already mandated.

WHAT IT CATCHES. The audit notebook selects experiments from a whole-year
`getExperiments` window, which legitimately returns experiments that OVERLAP the audit
year at both ends. Selecting from that set on month alone is year-blind: with
`RUN_MONTHS = [1]` the 31-December-2022 experiment matches on `endmonth == 1`, and with
`RUN_MONTHS = [12]` the 31-December-2021 experiment matches on `startmonth == 12`. Each
was filed into the wrong month's evidence folder. A downstream calendar-year guard
cannot express this invariant: the 2022-12-31 rows ARE year 2022 and pass it untouched,
which is why the merged year artifact is correct while the January per-month summary is
not.

The invariant asserted here is run-window membership, not calendar-year membership:
every record in `evidence/audit_evidence_<YEAR>-<MM>/` falls in that month, except for
at most one documented preceding-day straddle. Madrigal experiments straddle UTC day
boundaries, so the day before a month's first day is expected and intended; a second
straddle day, or any other out-of-month date, is not.

Run: pytest tests/test_acquisition_window.py
"""

from __future__ import annotations

import calendar
import csv
import datetime as dt
import re
from pathlib import Path

import pytest

AUDIT_YEAR = 2022
EVIDENCE_DIR = Path(__file__).resolve().parent.parent / "evidence"
MONTH_DIR_RE = re.compile(r"^audit_evidence_(\d{4})-(\d{2})$")
RAW_RECORDS = "madrigal_coverage_raw_records.csv"


def _month_dirs() -> list[tuple[int, Path]]:
    """Every per-month evidence folder as (month, path). Ignores the merged -FULL dir."""
    found = []
    if not EVIDENCE_DIR.is_dir():
        return found
    for path in sorted(EVIDENCE_DIR.iterdir()):
        match = MONTH_DIR_RE.match(path.name)
        if not match or not path.is_dir():
            continue
        year, month = int(match.group(1)), int(match.group(2))
        if year != AUDIT_YEAR:
            continue
        if (path / RAW_RECORDS).is_file():
            found.append((month, path))
    return found


def _allowed_dates(month: int) -> tuple[set[dt.date], dt.date]:
    """Dates a run for `month` may legitimately produce, and its one straddle day.

    The straddle day is the calendar day immediately preceding the month's first day.
    For January that day falls in the previous calendar year, which is expected and is
    the reason a plain year filter is not a substitute for this check.
    """
    days_in_month = calendar.monthrange(AUDIT_YEAR, month)[1]
    in_month = {dt.date(AUDIT_YEAR, month, d) for d in range(1, days_in_month + 1)}
    straddle = dt.date(AUDIT_YEAR, month, 1) - dt.timedelta(days=1)
    return in_month | {straddle}, straddle


def _observed_dates(records_csv: Path) -> set[dt.date]:
    with records_csv.open(newline="", encoding="utf-8") as handle:
        return {
            dt.date.fromisoformat(row["date"])
            for row in csv.DictReader(handle)
            if row.get("date")
        }


# --- the invariant, asserted against the acquisition evidence on disk ----------------


@pytest.mark.parametrize("month,path", _month_dirs(), ids=lambda v: getattr(v, "name", v))
def test_no_record_outside_the_run_window(month: int, path: Path) -> None:
    """No record in a month's folder falls outside that month plus one straddle day."""
    allowed, straddle = _allowed_dates(month)
    observed = _observed_dates(path / RAW_RECORDS)
    intruders = sorted(observed - allowed)
    assert not intruders, (
        f"{path.name} contains {len(intruders)} out-of-window date(s): "
        f"{[d.isoformat() for d in intruders]}. Allowed: {AUDIT_YEAR}-{month:02d} "
        f"plus the single straddle day {straddle.isoformat()}."
    )


@pytest.mark.parametrize("month,path", _month_dirs(), ids=lambda v: getattr(v, "name", v))
def test_at_most_one_straddle_day(month: int, path: Path) -> None:
    """Exactly one preceding-day straddle is documented behaviour; a second is not."""
    _, straddle = _allowed_dates(month)
    observed = _observed_dates(path / RAW_RECORDS)
    out_of_month = sorted(d for d in observed if (d.year, d.month) != (AUDIT_YEAR, month))
    assert len(out_of_month) <= 1, (
        f"{path.name} carries {len(out_of_month)} out-of-month days "
        f"{[d.isoformat() for d in out_of_month]}; at most one is permitted and it must "
        f"be {straddle.isoformat()}."
    )


def test_locked_test_month_records_appear_only_in_their_own_folder() -> None:
    """December 2022 is the locked test month. Its records belong in audit_evidence_2022-12
    and nowhere else -- a copy filed under another month puts locked-month values on an
    unrestricted path with no access record."""
    offenders = {}
    for month, path in _month_dirs():
        if month == 12:
            continue
        december = sorted(
            d for d in _observed_dates(path / RAW_RECORDS)
            if (d.year, d.month) == (AUDIT_YEAR, 12)
        )
        if december:
            offenders[path.name] = [d.isoformat() for d in december]
    assert not offenders, (
        f"Locked-test-month (December {AUDIT_YEAR}) records found outside their own "
        f"folder: {offenders}"
    )


# --- the selection predicate itself, on a synthetic experiment list ------------------


class _Experiment:
    """The fields the audit notebook's selection predicate reads."""

    def __init__(self, name: str, start: dt.date, end: dt.date) -> None:
        self.name = name
        self.startyear, self.startmonth = start.year, start.month
        self.endyear, self.endmonth = end.year, end.month

    def __repr__(self) -> str:  # pragma: no cover - diagnostic only
        return self.name


def _select(experiments: list[_Experiment], run_months: list[int]) -> list[str]:
    """The corrected predicate from the audit notebook, Cell 10."""
    targets = {(AUDIT_YEAR, m) for m in run_months}
    return [
        e.name
        for e in experiments
        if (e.startyear, e.startmonth) in targets or (e.endyear, e.endmonth) in targets
    ]


def _year_blind_select(experiments: list[_Experiment], run_months: list[int]) -> list[str]:
    """The defective predicate, kept as the negative control this test exists to catch."""
    return [
        e.name
        for e in experiments
        if e.startmonth in run_months or e.endmonth in run_months
    ]


BOUNDARY_EXPERIMENTS = [
    # A whole-year getExperiments window returns experiments overlapping either end.
    _Experiment("gps211231", dt.date(2021, 12, 31), dt.date(2022, 1, 1)),
    _Experiment("gps220101", dt.date(2022, 1, 1), dt.date(2022, 1, 2)),
    _Experiment("gps221130", dt.date(2022, 11, 30), dt.date(2022, 12, 1)),
    _Experiment("gps221201", dt.date(2022, 12, 1), dt.date(2022, 12, 2)),
    _Experiment("gps221231", dt.date(2022, 12, 31), dt.date(2023, 1, 1)),
]


def test_january_run_excludes_the_locked_month_experiment() -> None:
    selected = _select(BOUNDARY_EXPERIMENTS, [1])
    assert "gps221231" not in selected, (
        "A January run selected the 31-December-2022 experiment. This is the defect: "
        "its endmonth is 1, so a month-only test admits it."
    )
    assert "gps211231" in selected, "January's documented preceding-day straddle was dropped."
    assert "gps220101" in selected


def test_december_run_excludes_the_previous_year_experiment() -> None:
    selected = _select(BOUNDARY_EXPERIMENTS, [12])
    assert "gps211231" not in selected, (
        "A December run selected the 31-December-2021 experiment. Its startmonth is 12, "
        "so a month-only test admits it."
    )
    assert "gps221130" in selected, "December's documented preceding-day straddle was dropped."
    assert {"gps221201", "gps221231"} <= set(selected)


def test_negative_control_the_year_blind_predicate_admits_both_intruders() -> None:
    """Proves this suite fails on the defect rather than passing vacuously.

    Every hard rule gets a test that catches the violation, not only one that shows the
    happy path works. If this assertion ever stops holding, the negative control has
    stopped exercising the defect and the tests above prove less than they appear to.
    """
    assert "gps221231" in _year_blind_select(BOUNDARY_EXPERIMENTS, [1])
    assert "gps211231" in _year_blind_select(BOUNDARY_EXPERIMENTS, [12])
