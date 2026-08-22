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

| 7 | Year re-merge under **D-18** (`scripts/merge_coverage_year.py`) | 2026-08-21 | December 2022 rows re-read from `evidence/locked_test_restricted/audit_evidence_2022-12/` and merged into a regenerated year artifact | Deduplicated record union, per-day/per-month coverage counts and hashes for the full year, December included | No — none exists to inspect | `true` | **Written BEFORE the read.** Discharges the `PROVENANCE_NOTICE.md` obligation: the previous FULL was merged 2026-08-13T06:27:03Z, before the 2026-08-16 correction of the January and December folders, so its provenance pointed at superseded per-month hashes. Authorised by the project owner, 2026-08-21. The prior FULL is preserved, not overwritten |

| 8 | Governance re-review of AI-DLC stage 2.8 (`GOV-2026-08-22-DP-01` remediation) — restricted-root inspection | **Access: 2026-08-22, during the session; exact clock time not captured per command.** **This row created: 2026-08-22T10:47:50Z** | `evidence/locked_test_restricted/` — a directory listing (entry names, sizes, modification times), and a recursive string search over `*.md` / `*.json` / `*.jsonl` that reached `sha256_manifest.json` files beneath the restricted root | **Nothing computed.** No coverage statistic, no day count, no record count, no hash. The string search was for the literal `locked_test_accessed` and returned no match beneath the restricted root | No — none exists to inspect | `true` | **Retrospective row, created 2026-08-22. Logged AFTER the read, not before** — the same ordering defect row 5 records. Actor: the AI assistant conducting the governance re-review, on the project owner's instruction. **Scope: metadata and manifest-class file contents only. No December VTEC target value, coverage figure or performance quantity was read, parsed, computed, ranked, plotted or summarised.** Authorization: governance verification directed by the project owner; the purpose is custody assessment, not analysis, which is the class Vision §8.3 permits performance-blind. **The pre-read logging obligation was not met, and this row does not repair that** |

| 9 | Governance review of the AI-DLC **Inception phase** (`GOV-2026-08-22-INC-01`) — restricted-root inspection | **Access: 2026-08-22, during the session; exact clock time not captured per command.** **This row created: 2026-08-22, after the read** | `evidence/locked_test_restricted/` — a **directory listing only** (`ls`), returning five entry names: `audit_evidence_2022-12`, `audit_evidence_2022-FULL`, `bbox___opt_openmadrigal_madroot_experiments4_2022_gps_31dec22_gps221231g.003.hdf5.txt`, `superseded_2026-08-16_from_2022-01`, `superseded_2026-08-21_audit_evidence_2022-FULL`. No file beneath the restricted root was opened, and no recursive content search was run under it | **Nothing computed.** No coverage statistic, no day count, no record count, no hash, no manifest content. Narrower in scope than row 8, which additionally read `sha256_manifest.json` contents | No — none exists to inspect | `true` | **Retrospective row, created 2026-08-22. Logged AFTER the read, not before** — the same ordering defect rows 5 and 8 record. Actor: the AI assistant conducting the Inception-phase governance review, on the project owner's instruction to review the phase. **Scope: directory-entry names only. No December VTEC target value, coverage figure or performance quantity was read, parsed, computed, ranked, plotted or summarised.** Authorization: governance verification directed by the project owner; purpose is custody assessment, not analysis — the class Vision §8.3 permits performance-blind. **The pre-read logging obligation was not met, and this row does not repair that.** The board disclosed the access in its own report (`GOV-2026-08-22-INC-01` Rec 9) and did not write this row itself; it was written on the owner's approval of that recommendation |

**Rows 3, 4, 5, 8 and 9 are retrospective; rows 6 and 7 are not.** Rows 3 and 4 were recorded in § Acquisition runs below, a table with no
`locked_test_accessed` column, so a reviewer reconstructing custody from this log found
two events while the manifests showed four. Row 5 was not recorded anywhere until now.
**Rows 8 and 9 were both added 2026-08-22**, each recording a governance
reviewer's own inspection of the restricted root. All five are marked retrospective rather than back-dated:
the rows did not exist before the reads, and no row can be made to have preceded them. The
registry itself was created 2026-08-16, after events 1 to 4. What these rows close is the
discrepancy; what they cannot close is the ordering.

**Row 8 records a metadata-and-manifest read, not a data read**, and the distinction is
kept because collapsing it would make the log less useful rather than more cautious. What
a G-06 reviewer needs to establish is when December *target values* were seen. Row 8 saw
none. It is logged anyway because FR-P1-02-3's scope is *access*, unqualified, and row 6
set the precedent of logging even a byte-level hash read where no field was parsed.

### Evidence gap — the 2026-08-21 test-suite run is NOT logged, and deliberately so

Recorded 2026-08-22 as a **governance finding rather than an access-log row**, because the
access event cannot be substantiated to the standard this log requires.

**What is established.** Three test modules exist — `tests/test_acquisition_window.py`,
`tests/test_phase_boundary.py`, `tests/test_release_hashes.py`. Each resolves a
`RESTRICTED_DIR` path, and each reaches it through a **recursive** traversal rooted at
`evidence/`, so the restricted root is inside their search scope by construction rather
than by intent. Their reads are content reads, not metadata: `csv.DictReader` over
`madrigal_coverage_raw_records.csv`, `csv.reader` over `madrigal_coverage_*.csv`, and
`hashlib.sha256` over whole artifacts opened in binary. `__pycache__` holds bytecode dated
2026-08-21 13:24–13:25 under CPython 3.11 / pytest 8.3.5, and `.pytest_cache/v/cache/nodeids`
records **226 collected node IDs**, last written 2026-08-21T16:09. No `lastfailed` file
exists, which is consistent with a last run carrying no failures.

**What is NOT established, and why no row was written.** *Which assertions executed.* The
cache proves collection and a completed run; it does not prove that any particular test
body ran, and several of these tests `pytest.skip(...)` when their subject is absent. **No
run log, no captured output, no report and no evidence record exists for that run.** So
the access is **highly likely on the code path and unproven in execution**. Inventing a
row — with an access time, a scope and an authorization basis — would fabricate exactly the
fields this register exists to make trustworthy. The owner's instruction is explicit: where
the event cannot be substantiated, register an evidence gap, not an access record.

**Why it matters anyway.** If those reads did execute, they were December reads with **no
access-log row**, since `governance-guards.open_restricted` — the chokepoint BLK-07
requires — does not exist. That is BLK-07's registered hazard occurring in fact rather than
in principle, and it is the second independent reason RES-01's "permitted-read logging is
NOT TESTED" matters.

**What would close this gap — tracked as `RES-04`.** A rerun producing a captured report,
executed **after** the `open_restricted` chokepoint exists and **after** its access-log row
is written — never before. **The tests were deliberately NOT executed during the 2026-08-22
re-review**, for precisely this reason: running them then would have manufactured the
breach rather than documented it.

The obligation is registered with an owner, a hard prerequisite and a due gate in
`aidlc/spaces/default/intents/260813-tec-hourly-forecast/inception/units-generation/unit-of-work.md`
§ RES-04. Its required sequence: establish authorization; **write and preserve the
access-log entry before opening**; **fail closed if logging fails**; execute the permitted
inspection; capture the report as new evidence; record the **actual** rerun date and time;
and link that report back to this gap **without rewriting this record**.

**Preferred route, and most of the suite qualifies:** the intended behaviour of
`test_release_hashes.py` and `test_phase_boundary.py` is verifiable in full against the
**unrestricted** months (2022-01 to 2022-11) and synthetic fixtures, and
`test_acquisition_window.py`'s primary assertion — that no December-dated record appears in
a non-December folder — is verifiable **entirely on unrestricted months**, that being the
defect it was written for. What genuinely needs the restricted root is narrower: confirming
that the root's own artifacts pass the same checks. **That part waits until the applicable
gate explicitly permits the access.**

**A passing rerun will never be evidence that the 2026-08-21 event was properly logged.**
This record stands as written, and no future report amends it.

**Owner decision this gap does not take.** Whether the 2026-08-21 run constituted an
unauthorized December access is **not resolved here**. Retrospective logging would not
resolve it either — an unauthorized access stays unauthorized once logged. The scope, had
it executed, is coverage-record and byte-level hash reading, which is the performance-blind
class Vision §8.3 permits; what is missing is the pre-read record, not the authority.

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
