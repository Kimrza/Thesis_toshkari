# Change record — audit and remediation of GOV-2026-08-20-RA-01's non-blocking findings

Vision §15.2 change record. Six required fields, in order. One record covers the
whole disposition because the 43 findings were audited in one pass and approved
as one decision.

| Field | Value |
|---|---|
| Record ID | `CR-2026-08-21-RA-AUDIT` |
| Date | 2026-08-21 |
| Approver | Kimia Rezaei, project owner, acting under the recorded student/supervisor authority equivalence |
| Effective version | Vision v4.3 / TE v3.3 — no authority-document row is amended by this record; it governs stage 2.3's artifact only |
| Governance origin | `governance/reviews/GOV-2026-08-20-RA-01.md` MAJOR 1–30 and MINOR/NOTE 1–13; `governance/reviews/GOV-2026-08-21-RA-01.md`, whose Rec set was already applied |

## 1. Requested change and reason

`requirements.md`'s revision record asserted flatly that
`GOV-2026-08-20-RA-01`'s "MAJOR and MINOR sets are unworked". A resume-time
verification pass on 2026-08-21 established that this was wrong in both
directions: the 08-21 board's recommendations had incidentally closed some of
them, and ten more were half-closed with no account of which limb remained. A
blanket "unworked" is not a safe record of either state — the closed ones invite
duplicated work, and the half-closed ones are the ones most easily read as done.

Three further defects were found in the same pass, neither board having raised
them:

1. **The "Still open" paragraph contradicted its own document on four counts.**
   It stated that the four support thresholds remain `TBD`, that the `TEC-05`
   §16.1 sub-gate residue and the `ML-01` 24-hour-window residue were unworked,
   and that "no pytest run has occurred — no Python interpreter is available in
   this environment". D-19 froze the thresholds; the four §16.1 sub-gates are in
   the gate table; FR-P1-04-12 carries the window; and the suite was re-run at
   resume on CPython 3.11.9 — **224 passed, 2 skipped**, matching commit
   `13d5796` exactly.
2. **D-18 was absent from the revision record entirely**, although it is the
   re-merge that discharges the `PROVENANCE_NOTICE` obligation `DATA-08` raised
   and moves FULL's `source_runs` digests onto current per-month hashes.
3. **FR-P1-03-5 asserted the D-19 thresholds are "recorded in `data.yaml` … so
   the zero-TBD preflight now passes on this component".** No `configs/data.yaml`
   exists anywhere in the workspace: there is no `configs/`, no `src/` and no
   `pyproject.toml`, the REQ-ENG scaffold being unbuilt. The values are in
   `evidence/DECISIONS.md`. This is the failure mode `project.md` § Way of
   Working names — a gating condition whose input does not exist.

## 2. Alternatives

Three dispositions were put to the owner.

- **(a) Work all 38 open-or-partial findings inside stage 2.3.** Chosen.
- **(b) Fix the 20 items in groups A–C and defer the 18 group-D accuracy items
  to stage 3.2** with their owning gates recorded. Rejected: the group-D items
  are defects in *this* artifact, and 3.2's authority is the NFR set, not this
  document's accuracy.
- **(c) Fix group A only, then re-board immediately** to get a current verdict
  before committing to the rest. Rejected as slower overall for the same end
  state, though it would have put a fresh verdict on record soonest.

A fourth option — approving the stage with `FAIL` standing — was not offered.
`CLAUDE.md` bars approving or advancing a stage while a governance verdict is
`FAIL`.

## 3. Decision

**Audit result: 7 fully closed, 9 partially closed, 27 open, of 43.**

**Fully closed (7).** `ML-07`+`TEC-12` (five ablations enumerated, `ABL-ZENITH`
deferred to Phase 2 on a recorded phase call); `ML-08` (FR-P1-04-13's
target-lag carry-forward prohibition); `TEC-06` (Vision §6.12's 90% rule, via
D-12); `DATA-19` (`scripts/run_walking_skeleton.py` named in REQ-ENG-1);
`VAL-9` (the H4/SRQ-5 demotion record, now FR-P1-05-18); and two the audit
initially misread as open, corrected on a second look — `TEC-15` (Vision §6.2's
affirmative characterisation, present in § Out of scope C but wrapped across a
line break, which defeated a keyword search) and `BENCH-05` (the 10.0 GB
envelope and the four `binding: hard` TC-03 rows, present inside REQ-ENG-11
rather than in § Constraints, where the first pass looked for them).

**That near-miss set the audit's method.** Two false negatives out of 43 on a
keyword pass is a poor error rate for a record that governs what gets built, so
every other verdict was established by reading the requirement row rather than
by grepping for a phrase, and the two corrections are recorded here rather than
quietly folded into the totals.

**Partially closed (9), with the surviving limb named** so it cannot pass as
done:

| Finding | Closed limb | Surviving limb |
|---|---|---|
| `ML-10`+`VAL-5`+`VAL-6`+`TEC-10` | Regime-count audit, D-13 threshold, demotion ordering | §9.3's three regime thresholds; the −12 h/+24 h event window |
| `VAL-4`+`BENCH-08`+`IMPL-11` | Phase 2 disclosure (FR-P1-05-19) | `prior_period_exposure` — grep returns zero |
| `DATA-14`+`IMPL-12`+`BENCH-10` | §10.1 full field set (FR-P1-06-3) | TE §5.1's nine-field inventory; Kyoto and CEDAR notices; adapter and no-paste rules |
| `BENCH-09` | TE §13.1's `platform` field is already a registry column | REQ-ENG-3's third-platform claim is unfalsifiable by its own evidence; §9.1's inter-platform transfer rule |
| `BENCH-07` | M-03's training-fold restriction is in the requirement text | Its criterion is still a module/grep inventory |
| `IMPL-9`+`DATA-18`+`VAL-10` | `test_acquisition_window.py`'s §12 standing (REQ-ENG-4) | § Intent analysis still asserts "no `tests/`" |
| `ML-12` | Breakdowns split into FR-P1-05-16 | Vision §9.5's F1–F4 fold table; per-seed three-seed stability |
| `VAL-8` | Access-log ordering (FR-P1-05-12) | Write-once has no detection criterion |
| `VAL-11` | The provisional-Dst bar is recorded | `.dst_summary.json` is still tracked, unmanifested and unhashed at the repository root |
| `DATA-11`+`IMPL-5` | D-14 froze the scientific window | FR-WS-1's "single-station … all three cells" contradiction is unrecorded; §15.2's thirteen content areas |

**Approved disposition: fix all 38 open-or-partial findings inside stage 2.3,
plus the three defects above, in four ordered groups.** The ordering is by
consequence, not by convenience.

- **Group A — false assurance (8).** A stated criterion or test link promises
  coverage the project does not have: `ML-03`, `ML-04`+`IMPL-6`, `DATA-07`,
  `DATA-13`+`IMPL-10`, `BENCH-06`, `BENCH-07`, `IMPL-8`, `VAL-8`.
- **Group B — an open leakage or integrity path (7).** Construction could build
  the defect: `ML-09`, `ML-06`, `DATA-10`, `TEC-13`, `DATA-09`, `DATA-17`,
  `IMPL-3`.
- **Group C — an invisible or unfrozen scientific choice (5).** `DATA-15`,
  `TEC-07`, `TEC-08`+`BENCH-03`, `TEC-09`, and `ML-10`'s residue.
- **Group D — accuracy and completeness (16).** `ML-05`, `ML-11`, `ML-12`r,
  `ML-13`, `VAL-4`r, `DATA-08`, `DATA-11`r, `DATA-14`r, `DATA-16`, `DATA-20`,
  `BENCH-09`, `IMPL-7`, `IMPL-9`r, `IMPL-13`, `TEC-14`, `VAL-11`r. Eighteen when
  the disposition was approved; `TEC-15` and `BENCH-05` left the group when the
  audit corrected itself.

**Deferred, and only these two.** Both are recorded in the artifact rather than
dropped:

| Deferred item | Why it is not a stage 2.3 defect | Owner / gate |
|---|---|---|
| `VAL-11`'s file custody — manifest or remove `.dst_summary.json` | A workspace custody action, not a requirement. The substantive risk, that it becomes the source of a regime count D-11 prohibits, is already closed in the artifact | Student / before G-05 |
| `DATA-14`'s thesis-appendix inclusion and notice-location mechanics | Governed at G-P2 and restated by stage 3.2's licence NFR; the acquisition-time obligations are fixed here | Student / G-P2 |

No scientific value is changed by this record. Every value it touches was
already frozen under D-1 through D-19 or is recorded as a named hole.

## 4. Affected artifacts

- `aidlc/spaces/default/intents/260813-tec-hourly-forecast/inception/requirements-analysis/requirements.md`
  — the only artifact rewritten. Fourth revision.
- `aidlc/spaces/default/intents/260813-tec-hourly-forecast/inception/requirements-analysis/memory.md`
  — the stage diary carries the audit's full per-finding result.
- No authority document, no config, no test, no evidence artifact.

## 5. Verification

- The audit was performed per finding against the artifact's own requirement
  rows, not against its revision record. Every "closed" verdict was checked by
  reading the row rather than by grepping for a keyword, several findings being
  worded differently in the artifact than in the board report.
- The pytest claim was re-established by execution rather than inherited:
  224 passed, 2 skipped, on CPython 3.11.9, the governed pin.
- The absence of `configs/data.yaml` was checked by a filesystem search over the
  whole workspace, not by reading the §12 tree.
- The advisory reviewer receipt is stale by fingerprint — `READY` was recorded
  against `sha256:d214b9ed…` and the artifact is now `sha256:4a621275…` — so a
  fresh reviewer pass and a full-board re-review both run before the stage gate.

## 6. Residual risk

- The 36 remediated findings are corrections to a specification, and a
  specification correction is not evidence that the specified behaviour exists.
  Every criterion added here is testable but untested until Construction builds
  the component; the `UNTESTED` markers and § Requirements with no testing row
  carry that gap explicitly rather than hiding it.
- `GOV-2026-08-20-RA-01` and `GOV-2026-08-21-RA-01` both stand at `FAIL` until a
  board is rerun against this revision. This record authorizes the remediation;
  it does not close either verdict, and it does not open any TEC gate.
- Vision §6.6 and TE §6.1 remain in textual conflict for Phase 1. D-17 lets work
  proceed without adopting a reading; correcting the source sentences runs
  through Vision §15.2 and is not attempted here.

---

## Addendum — fifth revision, remediating `GOV-2026-08-21-RA-02`

| Field | Value |
|---|---|
| Record ID | `CR-2026-08-21-RA-AUDIT-A1` |
| Date | 2026-08-21 |
| Approver | Kimia Rezaei, project owner, under the recorded student/supervisor authority equivalence |
| Governance origin | `governance/reviews/GOV-2026-08-21-RA-02.md` — full board, verdict `FAIL`, 3 BLOCKER / 3 MAJOR / 2 MINOR / 1 NOTE |

The fourth revision was put to a full board, which found three blocking defects.
**Two were defects in the fourth revision's own remediation** — recorded here in
that form rather than as neutral findings, because the pattern matters more than
the individual errors: a remediation pass can reintroduce, in miniature, the exact
defect class it was written to fix.

| Finding | Severity | Disposition |
|---|---|---|
| `CHAIR-03` — the reviewing agent authored the revision it reviewed | `BLOCKER` | **Disclosed, not closed.** Structural; no edit can close it. The human is the decision owner under `review-board.md`'s stated remedy, and the report's `PASS` rows are recorded as weaker evidence than an independent board's |
| `ML-14` — `ML-05` recorded as closed while none of its values appeared in the artifact | `BLOCKER` | **Closed.** Vision §8.6's grid counts (ridge 6, RF 18, LSTM 16), its fixed LSTM settings, and D-122's seeds (42; {1337, 2024, 7}; 20221201) are now named in FR-P1-05-2 and FR-P1-05-5. No value is changed — D-121 and D-122 approved them; the document merely states them. D-122's pending supervisor sign-off is carried rather than hidden |
| `IMPL-15` — REQ-ENG-12 contradicted D-144's approval of the self-contained acquisition notebook | `BLOCKER` | **Closed.** Split into REQ-ENG-12 (the four analysis/review notebooks: import from `src/`, four declarations, no-only-copy) and REQ-ENG-13 (the acquisition notebook: six declarations, four prohibitions, self-contained under D-144) |
| `DATA-21` — "thirteen field groups" and `source_files` reduced to "SHA-256 hashes" | `MAJOR` | **Closed.** Restated as §13.3's ten rows naming fourteen fields; `source_files` cross-references FR-P1-01-2's six items |
| `DATA-23` — FR-P1-02-1 carried two verdicts in one pass/fail cell | `MAJOR` | **Closed.** Split; FR-P1-02-7 created; every requirement now carries exactly one verdict and the untested count is 39 with no partials |
| `IMPL-16` — "behavioural" for the authority's "behavioral", and an over-broad equivalence scope | `MAJOR` | **Closed.** Spelling restored and the test scoped to the named notebook/script pair |
| `CHAIR-04` — § Known defects rows ran 1,2,3,4,5,6,10,8,9,7,11,12,13 | `MINOR` | **Closed.** Reordered 1–13; three requirements cite these rows by number |
| `DATA-24` — FR-P1-01-7's `features.yaml` freeze had no stated dependency | `MINOR` | **Closed.** Sequenced behind REQ-ENG-1 |
| `BENCH-12` — the constellation report and GPS+Galileo escalation are unrequired | `NOTE` | **Recorded, no change.** Phase 2-scoped and out of this document's declared scope; recorded so a Phase 2 reader does not read it as covered |

### Verification of this addendum

- The `ML-14` values were checked present after the edit, and against Vision line
  819 (fixed LSTM settings), line 838 (final seeds), line 888 (bootstrap seed),
  §14.2 D-121 and D-122, and TE line 743 — the last of which is where `seeds.yaml`
  is specified.
- `DATA-21`'s count was established by reading TE §13.3's table directly: ten
  rows, fourteen field names. Neither number is thirteen.
- Requirement-ID uniqueness, table column consistency, and the untested count
  (39 full, 0 partial) were recomputed after the edits rather than asserted.
- The § Known defects reorder was applied by a script that asserted the rows were
  contiguous and that the sorted set equalled the original set before writing.

### Residual risk carried forward

- `CHAIR-03` is unclosed by construction. Every `PASS` row in
  `GOV-2026-08-21-RA-02`, and in any further board this session produces, carries
  the same conflict. Independent validation of this artifact requires a board
  that did not author it.
- § Known defects rows 12 (the `plumbing_7day` station count) and 13
  (NFR-SEC-01 versus the Madrigal identity requirement) remain open with **no
  reading adopted**, by design. Both are supervisor calls.
- The specification is now more complete and no more built: `src/`, `configs/`
  and `pyproject.toml` still do not exist, and 15 of REQ-ENG-4's 18 test modules
  are unwritten.
