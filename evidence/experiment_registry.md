# Experiment registry

Created 2026-08-16 in response to TEC governance board findings VAL-02 (no access
record exists for locked-month retrieval) and IMPL-02 (locked-test-month records on an
unrestricted path with no `locked_test_accessed` record).

`Technical Environment` §13.4 makes `locked_test_accessed` a required registry column
and requires that failed and aborted runs stay visible. No registry file existed before
this one, so §13.4 had no substrate. The rows below are **retrospective** and are marked
as such.

`code_commit` is recorded as `unavailable-pre-git` for every retrospective row. The
workspace was not a git repository when these runs executed, so no commit exists; a
hash attached now would point at code that may have changed since. Recording the
absence is correct, inventing a hash is not (§18.2).

## Locked-month access log

Every occasion on which December 2022 target values were retrieved or read, which is the
fact a G-06 reviewer must be able to establish.

| # | Run | `retrieved_at_utc` | Scope | What was computed | Performance inspected | `locked_test_accessed` | Authorization |
|---|---|---|---|---|---|---|---|
| 1 | December coverage audit (`RUN_MONTHS = [12]`) | 2026-08-12T10:25:30Z | December 2022, ARUC/BSHM/NICO cells | Day counts, hourly-bin counts, coverage percentages | No — none exists to inspect | `true` | Vision §8.3, required pre-G-05 performance-blind coverage audit |
| 2 | January coverage run (`RUN_MONTHS = [1]`) | 2026-08-12T22:41:57Z | 2022-12-31 retrieved unintentionally via the year-blind predicate; 743 ARUC-cell records | `december_days_present` / `december_coverage_pct` in the January summary, since corrected to 0 | No — none exists to inspect | `true` | Within-authorization irregularity per the Validation Auditor seat: same day, same cells, same parameters already lawfully exposed by run 1 twelve hours earlier, and only coverage counting was performed |

Run 2's retrieved extract is preserved at
`evidence/locked_test_restricted/bbox___opt_openmadrigal_madroot_experiments4_2022_gps_31dec22_gps221231g.003.hdf5.txt`.
It is retained rather than deleted because it is the only physical record of the access.
The 743 records were removed from `audit_evidence_2022-01/`'s derived artifacts; see
`evidence/CORRECTION_2026-08-16_acquisition_window.md`.

No model exists, no prediction has been generated, no metric has been computed, and
G-05 and G-06 are both Blocked. Neither access opened the locked test.

## Acquisition runs

Retrospective rows for the twelve monthly coverage runs and the year merge. §13.1's
per-run capture list (`requirements.txt` hash, per-run `pip freeze`, Python/OS/CPU,
config snapshot hashes, platform, nondeterministic operations) was not captured at the
time and cannot be reconstructed; this is recorded as a stated reproducibility
limitation rather than left as a silent absence.

| Run | `code_commit` | Environment capture | Status | Notes |
|---|---|---|---|---|
| `audit_evidence_2022-01` … `-12` (twelve monthly runs) | `unavailable-pre-git` | Not captured (§13.1 gap) | Complete | `madrigalWeb_version` recorded as `"unknown"` in all twelve request manifests — open finding DATA-03 |
| `audit_evidence_2022-FULL` (year merge) | `unavailable-pre-git` | Not captured (§13.1 gap) | Complete, **not re-merged after the 2026-08-16 correction** | Statistics correct (365 days, 100%); provenance now points at superseded per-month hashes |
| `audit_evidence_2022-01`, `-12` corrected extracts | `unavailable-pre-git` | Python 3.14, local | Complete 2026-08-16 | Originals preserved under `superseded_2026-08-16/` |

## Standing obligation

From this point, every run records its `code_commit` and §13.1 capture list, and any
run that reads December 2022 for any purpose adds a row to the locked-month access log
above before the run begins.
