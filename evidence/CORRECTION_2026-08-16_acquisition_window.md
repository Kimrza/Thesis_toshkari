# Correction record — acquisition-window defect (2026-08-16)

Raised by the TEC governance board (full seven-seat review of AI-DLC stage 2.2
practices-discovery). Findings IMPL-01, IMPL-02, IMPL-03, DATA-01, DATA-02, ML-07,
TEC-09, VAL-01, VAL-02. Remediation authorised by the student on 2026-08-16.

## Defect

`notebooks/madrigal_phase1_coverage_audit.ipynb`, Cell 10, selected experiments with:

```python
if exp.startmonth not in RUN_MONTHS and exp.endmonth not in RUN_MONTHS:
    continue
```

The enclosing `getExperiments` call spans the whole audit year, so it legitimately
returns every experiment that **overlaps** 2022 — including the 31-December-2021
experiment (ends 2022-01-01) and the 31-December-2022 experiment (ends 2023-01-01).
Testing month without year admits a 31-December experiment from either year:

- with `RUN_MONTHS = [1]`, the 31-Dec-**2022** experiment matched on `endmonth == 1`
  and was filed into `audit_evidence_2022-01/`;
- with `RUN_MONTHS = [12]`, the 31-Dec-**2021** experiment matched on
  `startmonth == 12` and was filed into `audit_evidence_2022-12/`.

The merge script's downstream year guard could not catch this. It tests calendar-year
membership; the defect is run-window membership. The 2022-12-31 rows *are* year 2022
and passed the guard untouched — which is exactly why `audit_evidence_2022-FULL/`
stayed correct while the January per-month summary did not.

## Fix

`AUDIT_YEAR = 2022` is now bound in Cell 10 and the predicate tests `(year, month)`:

```python
_RUN_TARGETS = {(AUDIT_YEAR, m) for m in RUN_MONTHS}
...
if ((exp.startyear, exp.startmonth) not in _RUN_TARGETS
        and (exp.endyear, exp.endmonth) not in _RUN_TARGETS):
    continue
```

This preserves the intended one-preceding-day straddle in every month (30-Nov-2022
still matches `(2022, 12)` on its end; 31-Dec-2021 still matches `(2022, 1)` on its
end) and excludes exactly the two misfiled experiments. No other line changed.

## Owning test

`tests/test_acquisition_window.py` — **a new module.** `Technical Environment` §12
enumerates an exhaustive seventeen-module `tests/` tree and none of them asserts
run-window conformance, so adding this module **amends §12 and requires supervisor
countersignature**, alongside the WS acceptance split and the §1.3 script-count
reading. It is recorded as new rather than presented as already mandated.

It asserts run-window membership over every month folder, at most one straddle day per
month, and that December-2022 records appear only in their own folder; it unit-tests the
corrected predicate on a synthetic boundary set; and it carries a negative control that
proves the year-blind predicate admits both intruders, so the suite cannot pass
vacuously. Before the fix: 5 failed, 23 passed. After: 28 passed.

## Evidence changes

Originals were **preserved, never deleted** — each corrected folder carries a
`superseded_2026-08-16/` copy of all five files as they stood before this correction.

**`audit_evidence_2022-01/`** — 743 records dated 2022-12-31 removed from
`madrigal_coverage_raw_records.csv` (20808 rows kept). The 2021-12-31 straddle is
retained: it is January's legitimate preceding-day straddle and was already excluded
from statistics by the year guard. Derived statistics recomputed with the **same
semantics as the original run** (aggregates over in-audit-year rows only; verified by
reproducing the original figures exactly before regenerating):

| | before | after |
|---|---|---|
| `unique_days` (all stations) | 32 | 31 |
| `coverage_pct_days` | 8.767 | 8.493 |
| `december_days_present` | 1 | 0 |
| `december_coverage_pct` | 3.226 | 0.0 |
| `madrigal_coverage_monthly.csv` | rows for months 1 and 12 | row for month 1 only |
| `records_in_cell` ARUC / BSHM / NICO | 6619 / 8235 / 6055 | 6396 / 7962 / 5808 |

**`audit_evidence_2022-12/`** — 642 records dated 2021-12-31 removed. **Its statistics
are unchanged** (`unique_days = 32`, `december_days_present = 31`,
`december_coverage_pct = 100.0`, months 11 and 12 present), because the year guard had
already excluded those rows from every aggregate. The `month 11` row is the documented
2022-11-30 straddle and is correct. No December science changed.

`sha256_manifest.json` regenerated in both folders over their four declared artifacts.

## Locked-month custody

The misfiled locked-month extract
`bbox___opt_openmadrigal_madroot_experiments4_2022_gps_31dec22_gps221231g.003.hdf5.txt`
was **moved, not deleted**, from `audit_evidence_2022-01/raw_isprint_cache/` to
`evidence/locked_test_restricted/`. Deleting it would destroy the only record of the
access. See `evidence/experiment_registry.md` for the retrospective access entry.

The Validation Auditor seat classified the access itself as a **within-authorization
irregularity, not an unauthorized access event**: manifest timestamps show the
authorized Vision §8.3 performance-blind December coverage audit ran at
2026-08-12T10:25:30Z and the January run at 2026-08-12T22:41:57Z, so the January run
exposed no locked-month information not already lawfully in hand, and what was computed
on it was day counts and coverage percentages — the class §8.3 permits. No model,
prediction, or metric exists; G-05 and G-06 are both Blocked. The seat recorded that
had the January run been the *first* December contact, its determination would differ.

## Still open after this correction

1. **`audit_evidence_2022-FULL/` has not been re-merged.** Its statistics were and
   remain correct (365 days, 100%, all three stations), but its provenance now points at
   the superseded per-month hashes. Re-merging changes the artifact D-9 promoted as
   Phase 1 acquisition input, so it is left for the student to decide rather than done
   silently.
2. `madrigalWeb_version` is `"unknown"` in all twelve request manifests (DATA-03).
3. `raw_isprint_cache/` contains isprint text extractions, **not** provider `.hdf5`
   bytes (DATA-04), and is absent for 2022-04, 2022-07 and 2022-12.
4. `merge_coverage_year.py` still copies eight provenance fields under an unverified
   identity assertion (DATA-06).
5. The new test module's amendment of §12 needs supervisor countersignature.
