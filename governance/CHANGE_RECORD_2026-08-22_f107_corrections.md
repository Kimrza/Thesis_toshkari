# Change Record — `CR-2026-08-22-F107-CORRECTIONS`

**Vision §15.2 change-control record.**

| Field | Value |
|---|---|
| **Change record ID** | `CR-2026-08-22-F107-CORRECTIONS` |
| **Date** | 2026-08-22 |
| **Requested by / approved by** | Project decision owner, under the recorded student/supervisor authority equivalence, using owner-supplied wording. No separate supervisor signature artifact exists and none is claimed |
| **Origin** | Governance report `GOV-2026-08-22-DP-01`; two derived contradictions between FR-P1-01-7 and the held provider data |
| **Document amended** | `aidlc/.../inception/requirements-analysis/requirements.md` — FR-P1-01-7 only |

## Correction 1 — the 20 UT claim was wrong

**Before:** *"the **high-spread handling** for the four days whose within-day
spread exceeds 20% of the median, **three of those four contaminated readings
falling at 20 UT, the conventional pick**"*

**After:** *"the **high-spread handling** for the four days whose within-day
spread exceeds 20% of the median — 2022-01-18, 2022-03-31, 2022-08-28, and
2022-08-29 — whose observed outliers occur at 18 UT, 20 UT, 20 UT, and 17 UT,
respectively. Because outliers occur across multiple UT slots, fixed-hour
selection without quality controls can retain contaminated observations."*

**Basis.** Derived 2026-08-22 from
`evidence/audit_ec1_2026-08-15/nrcan_f107/fluxtable.txt`:

| Day | 17/18 UT | 20 UT | 22/23 UT | Outlier at |
|---|---|---|---|---|
| 2022-01-18 | **148.8** | 114.5 | 111.6 | 18 UT |
| 2022-03-31 | 148.7 | **239.5** | 149.8 | 20 UT |
| 2022-08-28 | 151.6 | **251.9** | 133.5 | 20 UT |
| 2022-08-29 | **357.1** | 130.6 | 123.0 | 17 UT |

**Two** at 20 UT, not three.

**Deliberately not claimed.** The stronger statements considered during review —
that *no single slot is clean*, or that *no fixed-hour convention is safe* — are
**not** made. Neither has been independently demonstrated. The consequence stated
is bounded to what the four days show.

## Correction 2 — the outage framing asserted a hazard the data does not show

**Before:** *"The Canadian F10.7 archive is audited from 2022-03-18 onward for the
documented month-long outage; exact missing dates, qualifiers and any
reconstructed values are reported."*

**After:** *"The suspected outage beginning on 2022-03-18 was audited against the
available 2022 source data. No missing calendar day was observed: at least one
observation is present on 365 of 365 calendar days. This finding does not assert
uninterrupted within-day coverage or uninterrupted provider availability."*

**Granularity is stated because the measurement has one.** The audit counted
**calendar days carrying at least one observation**. It did not measure within-day
continuity and did not measure provider-side availability. The result is
therefore **not** described as "zero outage". A related limit is carried in the
same row: the archive has no qualifier, flag or provenance column, so
measured-versus-reconstructed is not determinable from it and is asserted neither
way (EC1-R-4).

## Status update carried in the same amendment

Clauses (a), (b) and (c) moved from open freeze-gate holes to frozen decisions:

- **(a) D-21** — daily value is the **daily median**.
- **(b) D-22** — duplicate UT records take the **mean**, with duplicate logging
  and a quality-control flag; **provider-defined correction semantics take
  precedence when documented**.
- **(c) D-23** — high-spread days are **flagged and retained** using the approved
  daily median.

**The availability constraint is written into the criterion verbatim in
substance:** *the approved daily F10.7 value must not become available to a
forecast before all observations required to compute that value were actually
available.* No same-day look-ahead is introduced.

## Downstream effects

| Artifact | Effect |
|---|---|
| `configs/features.yaml` | Gains three D-numbered values at Bolt 1, each citing D-21/D-22/D-23. The file does not exist yet |
| Tests | **None changed.** FR-P1-01-7's test column remains `UNTESTED`; no acceptance row is added or removed by this amendment |
| Acceptance criteria | Unchanged. The 36-row untested count is unaffected by this amendment (the four-row reduction came from `CR-2026-08-22-LEAKAGE-TA`) |
| FR-P1-04-2 / WS-11 / TA-08 | The availability constraint's enforcement is verified through the existing availability matrix, not by a new row |

## Leakage, frozen decisions and locked December — confirmation

- **No leakage introduced.** The amendment *tightens* the daily-value rule by
  adding an availability constraint and an explicit no-same-day-look-ahead
  statement. Nothing is loosened.
- **No unauthorized frozen-decision change.** D-10.3's previous-day contract, the
  trailing 81-day mean, and the observed-not-adjusted flux choice are all
  unchanged. The three new freezes are D-21/D-22/D-23, approved by the owner.
- **No locked-December violation.** The F10.7 archive sits at
  `evidence/audit_ec1_2026-08-15/nrcan_f107/`, outside
  `evidence/locked_test_restricted/`, and is a time-indexed predictor series —
  not target values, not model performance. One December-dated row (2022-12-08)
  appears in the duplicate-UT list as a property of the driver file;
  `EC1-AUDIT.md` independently records that its year-wide predictor scan touched
  no seal. No access-log row was owed or written.

## Verification performed

- 2022 coverage recomputed from the held file: **365 distinct calendar days**,
  1,101 readings.
- High-spread days recomputed at the 20%-of-median threshold: **four**, with
  per-hour values as tabulated.
- Column inventory of the source file: **seven columns**, no qualifier, flag or
  provenance field.

**No test was executed for this amendment.**

**Correction, 2026-08-22.** An earlier revision of this record stated "no test suite exists in this repository". That was wrong. **Three of the mandated modules exist** — `tests/test_acquisition_window.py`, `tests/test_phase_boundary.py` and `tests/test_release_hashes.py` — and `.pytest_cache` records **226 collected test node IDs** from a run on 2026-08-21 under CPython 3.11 / pytest 8.3.5. What remains true is that **no test was executed for this amendment**, and that the modules this amendment concerns do not exist. The three existing modules were **not** run during this work, deliberately: all three reference `evidence/locked_test_restricted/`, and the `open_restricted` access-log chokepoint that BLK-07 requires does not exist yet, so executing them would perform December reads with no access-log row.
