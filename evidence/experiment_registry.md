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

| 3 | Year merge `audit_evidence_2022-FULL` (`merge_coverage_year.py`) | 2026-08-13T06:27:03Z | December 2022 rows merged into the year artifact, ARUC/BSHM/NICO cells | Day counts, hourly-bin counts and coverage percentages for the full year, December included | No — none exists to inspect | `true` | **Retrospective row, added 2026-08-21.** Not logged at the time. Within the scope Vision §8.3 authorises (coverage counting only), but §8.3 records *access*, unqualified, so a derived-artifact merge that reads December is an access and required a row before the read. Origin: GOV-2026-08-20-RA-01 finding `VAL-2` |
| 4 | December and January corrected extracts (acquisition-window correction) | 2026-08-16 | December 2022 records rewritten in `audit_evidence_2022-12/`; 642 out-of-year rows removed; December statistics recomputed | Corrected day counts and coverage percentages | No — none exists to inspect | `true` | **Retrospective row, added 2026-08-21.** Not logged at the time. The rewrite changed `audit_evidence_2022-12/madrigal_coverage_raw_records.csv` (sha256 `00a7942a…` → `8ed7f406…`); originals preserved under `superseded_2026-08-16/`. See `evidence/CORRECTION_2026-08-16_acquisition_window.md`. Origin: `VAL-2` |

| 5 | Governance review `GOV-2026-08-21-RA-01` — custody verification | 2026-08-21 | December 2022 record **counts** in four unrestricted artifacts (`audit_evidence_2022-12/`, `audit_evidence_2022-FULL/`, and the two `superseded_2026-08-16/` snapshots) | Row counts only, by line match on the observation-date column: 21,258 / 21,258 / 21,258 / 743. No target value was inspected, ranked, plotted or summarised | No — none exists to inspect | `true` | **Retrospective row, added 2026-08-21.** Logged after the read, not before. The read established finding `VAL-1`'s factual basis and was itself an unlogged December access — the exact defect `VAL-2` reports. Recorded rather than omitted; the ordering cannot be repaired |
| 6 | Custody relocation under **D-15** | 2026-08-21 | December-bearing artifacts moved into `evidence/locked_test_restricted/`: `audit_evidence_2022-12/`, `audit_evidence_2022-FULL/`, `audit_evidence_2022-01/superseded_2026-08-16/` | File-level move and post-move hash verification. Records were read only as bytes for SHA-256 verification; no field was parsed, no value inspected, no statistic computed | No — none exists to inspect | `true` | **Written BEFORE the read, as FR-P1-02-3 now requires.** Authorised by the project owner, 2026-08-21, under the recorded student/supervisor authority equivalence. Purpose is custody containment, not analysis: TE §12 requires locked-test artifacts to sit under a restricted path until G-05 is complete |

**Rows 3, 4 and 5 are retrospective; row 6 is not.** Rows 3 and 4 were recorded in § Acquisition runs below, a table with no
`locked_test_accessed` column, so a reviewer reconstructing custody from this log found
two events while the manifests showed four. Row 5 was not recorded anywhere until now.
All three are marked retrospective rather than back-dated: the rows did not exist before
the reads, and no row can be made to have preceded them. The registry itself was created
2026-08-16, after events 1 to 4. What these rows close is the discrepancy; what they
cannot close is the ordering.

**Row 6 is the first December access logged in advance**, which is the standard from this
point (FR-P1-02-3, FR-P1-05-12).

**Not counted as locked-test access, with the reason stated.** Reading Kyoto provisional
Dst for December 2022 (`.dst_summary.json`, orientation for decision D-13) is not a
locked-test access: Dst is a public driver series, not a target value, and no December
*target* record is touched by it. D-11 separately bars any provisional-Dst figure from
becoming a G-05 regime count, so that material cannot enter the freeze set either.
Producing D-12's per-station coverage table likewise did not read December — the table
covers the nine cached non-December months only, and December's own hourly coverage is
left to the required pre-G-05 audit.

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
| `audit_evidence_2022-FULL` (year merge) | `unavailable-pre-git` | Not captured (§13.1 gap) | Complete, **not re-merged after the 2026-08-16 correction** | Statistics correct (365 days, 100%); provenance now points at superseded per-month hashes. **Relocated 2026-08-21 to `evidence/locked_test_restricted/audit_evidence_2022-FULL/` (D-15)** — the merged year holds 21,258 December rows, so reading it is a logged December access |
| `audit_evidence_2022-01`, `-12` corrected extracts | `unavailable-pre-git` | **Python 3.14, local — outside the governed 3.11 pin** (TE §8.1, TC-03d) | Complete 2026-08-16 | Originals preserved under `superseded_2026-08-16/`, both **relocated 2026-08-21 under D-15**: the December snapshot moved with its parent to `evidence/locked_test_restricted/audit_evidence_2022-12/superseded_2026-08-16/`, and the January snapshot — which held 743 December-2022 rows — to `evidence/locked_test_restricted/superseded_2026-08-16_from_2022-01/`. `audit_evidence_2022-12/` itself is now at `evidence/locked_test_restricted/audit_evidence_2022-12/` |

## Standing obligation

From this point, every run records its `code_commit` and §13.1 capture list, and any
run that reads December 2022 for any purpose adds a row to the locked-month access log
above **before the run begins**.

**Scope of "reads December", stated so it is not narrowed again.** The obligation covers
any operation that reads a record whose observation date falls in December 2022 —
including derived-artifact merges, re-derivations, corrections, coverage recounts and
schema validations — not only a model execution or a metrics computation. Requirements
FR-P1-02-3 and FR-P1-05-12 carry the ordering clause as of 2026-08-21
(GOV-2026-08-21-RA-01 Rec 19).

**Observed in practice, 2026-08-21.** While producing D-12's per-station coverage table,
December was deliberately not read, precisely to avoid adding a fifth unlogged access;
the table covers the nine cached non-December months only. December's own hourly
coverage comes from the required pre-G-05 performance-blind audit, with its access row
written first.
