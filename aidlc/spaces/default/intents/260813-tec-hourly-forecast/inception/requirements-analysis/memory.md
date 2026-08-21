# Requirements Analysis — Stage Memory

Observation diary for stage 2.3 (requirements-analysis). Maintained while the
stage runs; read by the §13 learnings ritual before the approval gate.

## Interpretations

- 2026-08-16T16:20:00Z — Treated this stage as decomposition and traceability rather than elicitation. Vision v4.2 §§1-17 and Technical Environment v3.2 already fix the research question, estimand, feature contract, evaluation protocol, claim boundary and NFRs; `constraint-register.md` carries TC/OC/PC rows and `discovered-rules.md` carries 58 affirmed hard rules. Inventing new requirements here would breach `phases/inception.md` § Traceability ("do not introduce new requirements in inception without documenting their origin"). Questions therefore target what the authority documents leave genuinely open or leave un-decomposed, not what they already settle.
- 2026-08-16T16:20:00Z — `user-stories` (2.4) is SKIP in this scope, so §16's WS-09-WS-20 and §19's TA rows are the only acceptance vocabulary Construction will receive. Requirements written here must carry pass/fail criteria that map onto those rows, or Construction inherits requirements it cannot test against.

## Deviations

- 2026-08-17T00:00:00Z — Q3 was answered with free text ("i have my supervisors approval do not ask again") rather than an option letter, and the answer barred a follow-up. Step 9 would normally raise a targeted follow-up on exactly this kind of ambiguity. Honoured the instruction instead: did not re-ask, adopted a stated reading (write the requirement, threshold as a named hole citing Vision 6.1B, operating on D-2's interim rule), and surfaced that reading at the Consolidated Summary Confirmation, which is a separate human stop where it could still be corrected. The human answered "Looks correct".
- 2026-08-17T00:00:00Z — Q10 arrived unanswered in the batch (the user supplied Q1-Q9 for a ten-question file). Asked Q10 alone as a structured question rather than proceeding on partial answers, per Step 8 item 2. Answered A.

## Tradeoffs

- 2026-08-17T00:00:00Z — Q2=A decomposes by the P1-00..P1-06 pipeline stages. That leaves the repository scaffold, pins and test suite without a home, since TC-06 places them before P1-01 and no P1 row covers them. Added a REQ-ENG-* group ahead of FR-P1-00 rather than forcing the scaffold into P1-00 (which is the ICTP audit closure) or dropping it. Alternative considered and rejected: decompose by the six src/ packages (Q2=B), which would have housed the scaffold naturally but would have detached requirements from the stage table that Construction actually executes.
- 2026-08-17T00:00:00Z — Chose to list untested requirements explicitly (18 of them) in their own section rather than silently omitting them or inventing WS/TA rows. Q1=A mandates flagging over inventing; the section doubles as concrete input for NFR Requirements (3.2) when it assembles the G-05 freeze manifest.

## Open questions

- 2026-08-16T16:20:00Z — Two supervisor gates remain open that bear on requirements: the §1.3 script/notebook count (affects how the pipeline decomposes into units) and D-144's two unfrozen sub-values, the coordinate-to-cell rule and the numerical coverage minimum. The coverage minimum in particular is a `TBD — supervisor freeze gate` that a G-P1A acceptance requirement would otherwise need to cite.
- 2026-08-17T00:00:00Z — The question file's Q5 enumerated nine TE section-11 NFRs; the document carries twelve (NFR-DQ-01 and NFR-TDEF-01 were omitted, and the practices artifacts under-cite them too). Adopted all twelve and recorded the under-enumeration as authority-chain defect 6. Worth checking whether the nine-item list has propagated elsewhere in the workflow.
- 2026-08-17T00:00:00Z — FR-P1-05-7, the confirmatory estimand itself, has no WS or TA row. TA-14 tests the bootstrap that carries it, not its definition. This is the most consequential of the eighteen untested requirements and is a candidate for a new TA row through Vision section 15.2 change control.

## Session resume 2026-08-21 — pre-gate verification

### Interpretations

- 2026-08-21T14:10:00Z — On resume, read the artifact tree, this diary, the merged audit shards and `aidlc-state.md` in the recovery protocol's order before touching anything. The stage stands at: artifacts written, advisory reviewer `READY` recorded 2026-08-17, learnings ritual and approval gate not yet run. Did not re-run the question flow: the `SUMMARY_CONFIRMATION_RECORDED` receipt and the filled `[Answer]: Looks correct` are both present from the prior attempt.
- 2026-08-21T14:10:00Z — Treated the `review-tec-governance` rule "Never modify the reviewed artifact during the review … wait for the student or supervisor to approve, reject, defer, or request remediation" as controlling over a literal reading of the `CLAUDE.md` clause "do not … mutate the reviewed artifact while a governance verdict is FAIL". A literal reading would make remediation of a FAIL impossible. Therefore: surfaced the defects found below and stopped, rather than repairing them unasked.

### Deviations

- 2026-08-21T14:10:00Z — Verified the artifact's own claims against the live workspace rather than accepting the revision record, per `project.md` § Way of Working ("ALWAYS verify a fact independently before handing it to another reviewer as established input"). This is beyond what Step 8's ambiguity scan requires, and it is what surfaced the five defects below.

### Tradeoffs

- 2026-08-21T14:10:00Z — Re-ran the real test suite (CPython 3.11.9 from the prior session's scratchpad, vendored pytest 8.3.5) rather than trusting commit 13d5796's reported result: 224 passed, 2 skipped, matching the commit exactly. Cost one command; the alternative was carrying an unverified test claim into a governance gate, which is the failure mode `GOV-2026-08-20-RA-01` finding `DATA-01` already caught once.

### Open questions

- 2026-08-21T14:10:00Z — Five defects found pre-gate, none yet repaired. (1) The § revision-record "Still open" paragraph is stale on four counts contradicted by the body of the same document and by verified workspace state: the four support thresholds (frozen as D-19), the `TEC-05` §16.1 sub-gate residue (now in the gate table), the `ML-01` 24-hour-window residue (now in FR-P1-04-12), and "no pytest run has occurred" (224 passed / 2 skipped, verified). (2) D-18, the year re-merge that discharges the `PROVENANCE_NOTICE` obligation `DATA-08` raised, is absent from the revision record entirely. (3) FR-P1-03-5 asserts the D-19 thresholds are "recorded in `data.yaml` … so the zero-TBD preflight now passes on this component"; no `configs/data.yaml` exists anywhere in the workspace — the REQ-ENG scaffold is unbuilt and the values live in `evidence/DECISIONS.md`. (4) The advisory reviewer receipt is stale: `READY` was recorded against fingerprint `sha256:d214b9ed…`; the artifact is now `sha256:4a621275…` after two 2026-08-21 commits. (5) `GOV-2026-08-20-RA-01`'s MAJOR (30) and MINOR/NOTE (13) sets are partially, not wholly, unworked — spot-checks confirm MAJOR 5 and 19 closed while MAJOR 9, 12, 21, 30 and MINOR `TEC-13` remain open. An accurate accounting needs a pass over all 43.

### Audit of GOV-2026-08-20-RA-01's non-blocking sets (2026-08-21, owner-directed)

- 2026-08-21T14:40:00Z — Checked all 43 non-blocking findings (30 MAJOR, 13 MINOR/NOTE) against the current artifact rather than against the revision record. Result: **5 fully closed, 10 partially closed, 28 open**. The artifact's blanket "MAJOR and MINOR sets are unworked" was therefore wrong in both directions — it understated what the 08-21 board's recommendations had incidentally closed, and it gave no account of the ten half-closed ones, which are the easiest to misread as done.
- 2026-08-21T14:40:00Z — Fully closed: `ML-07`+`TEC-12` (five ablations enumerated, with `ABL-ZENITH` deferred to Phase 2 on a recorded phase call), `ML-08` (FR-P1-04-13's target-lag carry-forward prohibition), `TEC-06` (Vision §6.12 via D-12), `DATA-19` (`run_walking_skeleton.py` named in REQ-ENG-1), `VAL-9` (H4/SRQ-5 demotion, now FR-P1-05-18).
- 2026-08-21T14:40:00Z — Partially closed, and each residue named so it cannot pass as done: `ML-10` (audit, D-13 and demotion ordering in; §9.3's three regime thresholds and the −12 h/+24 h event window out), `VAL-4` (Phase 2 disclosure in as FR-P1-05-19; `prior_period_exposure` absent, grep zero), `DATA-14` (§10.1 full field set in; TE §5.1's nine-field inventory, the Kyoto and CEDAR notices, and the adapter/no-paste rules out), `BENCH-05` (REQ-ENG-11 carries §9.2's four elements; TC-03/03a/03b/03g absent from § Constraints and the 10.0 GB envelope absent entirely), `BENCH-07` (M-03's training-fold restriction is in the requirement text but its criterion is still a module/grep inventory), `IMPL-9` (`test_acquisition_window.py`'s §12 standing recorded in REQ-ENG-4; § Intent analysis still asserts "no `tests/`", which three test modules now contradict), `ML-12` (breakdowns split into FR-P1-05-16; Vision §9.5's F1–F4 fold table and per-seed three-seed stability out), `VAL-8` (access-log ordering in; write-once still has no detection criterion), `VAL-11` (the provisional-Dst bar is recorded; `.dst_summary.json` is still tracked, unmanifested and unhashed at the repository root), `DATA-11` (D-14 froze the scientific window; FR-WS-1 still says "single-station … all three cells" in one sentence and § Known defects carries no row for it).
- 2026-08-21T14:40:00Z — Judgement offered to the owner: only two of the 38 open-or-partial findings are genuinely downstream-owned — `VAL-11`'s file custody (a workspace action, not a requirement) and `DATA-14`'s thesis-appendix and notice-location mechanics (G-P2, restated at 3.2). The other 36 are defects in this artifact, so a deferral split would be manufactured rather than found. Recommended fixing all of them here in four ordered groups: false assurance (8), open leakage or integrity path (7), invisible or unfrozen scientific choice (5), cheap accuracy and completeness (18).

### Remediation applied (2026-08-21, groups A-D)

- 2026-08-21T15:30:00Z — Applied the owner-approved disposition. All edits were made by exact-match replacement with a single-occurrence assertion, so a pattern that matched zero or two places aborted before writing rather than silently mis-editing a 776-line governed artifact. Governance record: `governance/CHANGE_RECORD_2026-08-21_RA_audit.md`.
- 2026-08-21T15:30:00Z — Nine new requirements: FR-P1-01-11 (derived-release provenance currency), FR-P1-04-16 (support-field rules), FR-P1-04-17 (driver alignment), FR-P1-04-18 (GIM interpolation and independence), FR-P1-05-20 (the PC-04 disclosure limb split from FR-P1-05-9), FR-P1-05-21 (M-03's fitting partition), FR-P1-05-22 (the config-only +24 h horizon), REQ-ENG-12 (TE §14's notebook obligations), and three § Known defects rows (11, 12, 13). Rows 12 and 13 deliberately adopt **no reading**: both are conflicts between a frozen decision and an authority sentence, where resolving either way would re-open a freeze or rewrite an authority clause by inference.
- 2026-08-21T15:30:00Z — FR-P1-05-4 moved **out** of the tested set, the only requirement to lose a test link in this revision: WS-18 cannot test the trigger the requirement names. Making a document honestly less covered than it claimed is the point of the `ML-03` finding, and the untested list grew from 30 to 38 for the same reason.

### Deviations

- 2026-08-21T15:30:00Z — The audit's first pass used keyword search and produced **two false negatives out of 43**: `TEC-15` was present in § Out of scope C but wrapped across a line break, and `BENCH-05` was present inside REQ-ENG-11 rather than in the § Constraints section the search looked at. Both were caught by re-checking against whitespace-normalized text and by reading rows rather than grepping phrases. Recorded rather than quietly folded into the totals, because a 2-in-43 error rate on a keyword pass is the finding: the counts reported to the owner were corrected from 5/10/28 to 7/9/27 mid-remediation.

### Tradeoffs

- 2026-08-21T15:30:00Z — Rejected a deferral split larger than two items. Group D looked deferrable by severity, but every group-D item is a defect in *this* artifact rather than work belonging to a downstream stage, and stage 3.2's authority is the NFR set, not this document's accuracy. Manufacturing a larger deferral would have moved 16 known defects out of sight under a governance-shaped label.
- 2026-08-21T15:30:00Z — Two pre-existing defects were fixed while in the file, neither from any board: `` `--phase 1|2` `` carried an unescaped pipe inside a code span, which splits the cell and made REQ-ENG-8 render with an extra column; and the § Requirements with no testing row paragraph claimed "23 entries" while listing 30 and "five entries added (bold)" while bolding twelve. The counts are now computed from the test-row column rather than maintained by hand.

### Open questions

- 2026-08-21T15:30:00Z — The advisory reviewer receipt is stale by fingerprint and this stage's review class is `advisory` with `reviewer_max_iterations: 1`, so a second `REVIEW_REQUESTED` may be refused by design. If it is, the stage carries a `READY` verdict recorded against an artifact 40,000 characters smaller than the one at the gate. That is a real gap in the receipt chain and belongs in front of the human rather than being worked around.
- 2026-08-21T15:30:00Z — § Known defects row 12 (the `plumbing_7day` station count) is recorded as **blocking for the fixture manifest**: `fixture_manifest.yaml` cannot state its identity while the count is contested, and REQ-ENG-4 now requires that manifest to carry §15.2's thirteen areas. This is the one new remediation that creates a fresh dependency rather than closing one.

### Full-board re-review and fifth revision (2026-08-21)

- 2026-08-21T17:00:00Z — `GOV-2026-08-21-RA-02` returned `FAIL` on the fourth revision: 3 BLOCKER, 3 MAJOR, 2 MINOR, 1 NOTE. **Two of the three blockers were defects in my own remediation** — `ML-14` (`ML-05` recorded as closed while the artifact contained zero occurrences of any of its values) and `IMPL-15` (REQ-ENG-12 contradicting D-144's approval of the self-contained acquisition notebook). All eight actionable findings remediated in a fifth revision; `GOV-2026-08-21-RA-03` returned `CONDITIONAL PASS`.
- 2026-08-21T17:00:00Z — The re-review's verification pass caught **two further regressions introduced by the fifth revision itself**: `DATA-25` (the FR-P1-02-1 split left its requirement text broader than its narrowed criterion — the very shape `DATA-23` existed to remove) and `IMPL-17` (the REQ-ENG-12/13 scope split silently dropped TE §14's "Run all" rule from the four analysis notebooks). Both fixed before the report closed, and both recorded in it as closed findings rather than quietly repaired.

### Interpretations

- 2026-08-21T17:00:00Z — Recorded `CHAIR-03` as a `BLOCKER` rather than a disclosure note. `review-board.md` lists "conflicted chair" among the Chair seat's own blocking concerns, and I authored the revisions I then reviewed. The rule's remedy — an independent human decision owner, with the AI board advisory — is what the verdict rests on, so `GOV-2026-08-21-RA-03` is `CONDITIONAL PASS` rather than `PASS`. A conflicted board issuing an unqualified `PASS` on its own work is exactly what that rule prevents.

### Tradeoffs

- 2026-08-21T17:00:00Z — Chose to record the two self-inflicted regressions in the governance report rather than only in the change record. They are the strongest available evidence for what `CHAIR-03` costs: an independent board would have found them without the author needing to look twice. Omitting them would have made the fifth revision read cleaner than it was.

### Open questions

- 2026-08-21T17:00:00Z — Three self-inflicted defects across two remediation passes (`ML-14`, `IMPL-15`, plus `DATA-21`'s uncounted "thirteen"), and two regressions from the fix pass itself. The pattern is consistent and worth naming as a practice candidate at the §13 ritual: **a remediation pass reintroduces, in miniature, the defect class it was written to remove** — a false closure claim while closing false closure claims, a truncated field list inside the fix for a truncated field list, a scope error while correcting a scope error. The mitigation that actually worked was re-reading the edited row against the authority rather than trusting the edit, and re-deriving every count from the artifact rather than from the finding text.

### Sixth revision, and a framework deadlock (2026-08-21)

- 2026-08-21T18:10:00Z — The fifth-revision advisory pass returned `READY` with two findings, both verified independently and both fixed in a sixth revision: FR-P1-02-5 cited `TA-29`, a row this document's own § Success and acceptance lists as "Not applicable in Phase 1", so the row counted as covered while nothing tested it — **four governance boards had passed over it**. Fixed by splitting the row (FR-P1-02-5 keeps the gate and TA-25; new FR-P1-02-8 carries the four prohibitions, `UNTESTED`). FR-P1-05-18's criterion covered two of its four obligations; extended to four numbered clauses. Untested count 39 → 40, still 0 partial, 94 requirement rows.
- 2026-08-21T18:10:00Z — The sixth-revision advisory pass returned **`NOT-READY`** with a Major that lands harder than its severity suggests: FR-P1-05-18's four new clauses test audit existence, demotion ordering, the regime thresholds and the event window — but **not the storm-event count's source**, which the requirement text states as "must come from GFZ Kp/Hp60 at a recorded release grade; D-11 bars any provisional-Dst-derived figure". The `VAL-11` deferral of `.dst_summary.json` is justified in this document by that risk being "already closed in FR-P1-05-18". The requirement says it; no criterion tests it. Sixth instance of the pattern, and the first one holding up a deferral.

### Deviations

- 2026-08-21T18:10:00Z — Did not fix the sixth-revision findings. `review_class: advisory` makes both verdicts terminal, so the findings go verbatim to the human gate rather than back to the builder. Recorded here because the temptation to fix a verified defect immediately is exactly what that rule exists to stop.

### Open questions

- 2026-08-21T18:10:00Z — **A hard framework deadlock blocks the gate on this clone, confirmed rather than inferred.** `aidlc-write-audit-log.ts:75-76` gates on `fileNorm.startsWith(recordRoot + '/')` where `recordRoot` derives from `CLAUDE_PROJECT_DIR` (`c:\...`, lowercase drive as the harness supplies it); `aidlc-lib.ts`'s summary-confirmation guard compares `resolvePath(projectDir, recordedFile)` against `resolvePath(artifact)`, the latter resolving against `process.cwd()` (`C:\...`, uppercase as Node reports it). `path.resolve` preserves drive-letter case, and both comparisons are case-sensitive. So a **lowercase**-path write is recorded but rejected by the guard, and an **uppercase**-path write satisfies the guard's comparison but is never recorded. No write can satisfy both, and `report --result awaiting-approval` therefore cannot succeed here. Demonstrated with a four-line reproduction. Two redos were spent before the second half of the mechanism was understood; the first redo's diagnosis (path case on one side only) was incomplete and the plan built on it could not have worked.
- 2026-08-21T18:10:00Z — The escapes are: `AIDLC_SKIP_SUMMARY_CONFIRMATION_GUARD=1` for one `report` call, whose substantive precondition is genuinely satisfied (the human confirmed twice and the artifact was written after each confirmation); or a case-insensitive path comparison at both ends, which is the actual fix but is a change to the framework rather than to this project. Fabricating the missing `ARTIFACT_UPDATED` event was considered and rejected: that event is hook-owned, and writing it from prose would forge an audit record.
