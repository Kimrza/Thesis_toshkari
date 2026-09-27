# Change record — 2026-09-27: the GOV-2026-09-24-BT-01 board report — SUPERSEDED BY RECOVERY

> **STATUS: SUPERSEDED, same day (2026-09-27), by successful recovery.** The report is
> now on disk, verbatim, at `governance/reviews/GOV-2026-09-24-BT-01.md`. This record is
> retained rather than deleted, per the project's append-never-replace discipline, because
> it states two facts that were WRONG when written and a reader of the citing artifacts
> must not inherit them. See § Correction below. The limitation this record declared —
> that the board's findings text and severity assignments are unauditable — **no longer
> holds.**

**Authorization:** GOV-2026-09-27-BT-02 Recommendation 5, approved by the Student
2026-09-27 (options sequential: commit the original verbatim if it can be found; else
record the loss explicitly and do NOT reconstruct). The recovery below is option 1 —
executed after this record had already fallen back to option 2.

## What actually happened

The report was **never lost, because it was never persisted.** It was delivered IN CHAT on
2026-09-24 and no file was ever written — which is the `/review-tec-governance` output
contract's own default: *"Write a report file only when explicitly asked to create an
artifact; otherwise return it in chat."* Every earlier search was therefore looking for a
file that never existed, and correctly found nothing.

The verbatim text survives in this clone's session transcript and was recovered from it on
2026-09-27:

- source: `~/.claude/projects/C--Users-s-sch-Desktop-test-Thesis-toshkari-main-Thesis-toshkari-main/9ccb10d0-9cac-4b10-818c-e1daaaa5296e.jsonl`, line 432, `type=assistant`, `model=claude-fable-5`, timestamp `2026-09-24T19:42:32.442Z`;
- 31,019 characters; **16** `### Recommendation` blocks, matching the rulings record's "all sixteen board recommendations";
- severity counts re-derived from the blocks themselves — Critical 1 / High 7 / Medium 7 / Low 1 — equal to the counts the report states and to the stage diary's 2026-09-24T22:10Z entry;
- the first extraction was discarded: Windows PowerShell 5.1's `Get-Content` read the UTF-8 transcript as CP1252 and mangled every en-dash. Re-extracted with an explicit UTF-8 reader and verified zero mojibake before writing.

This is recovery of the authentic text, **not** reconstruction. The prohibition this record
invoked below stands untouched and was never breached.

## Correction — two claims in the superseded body were wrong

1. **"full-board governance report"** — it was **`ADAPTIVE`** mode (the recovered
   Decision table states it; three seats active, four recorded `N/A` with reasons).
   The stage's CONDITIONAL PASS therefore rests on an adaptive pass, not a seven-seat one.
2. **"The 2026-09-24 board ran on the LOTUS clone"** — it ran on **this** clone,
   `GIT-AE-SRV-RDT1` (the `hostname` attribute of that session's own
   `artifacts/exec_evidence/run_2026-09-24_git-ae-srv/full_post.xml`, and the location of
   the recovering transcript). The LOTUS attribution was inferred from the artifacts' root
   disclosures and was wrong; it also sent GOV-2026-09-27-BT-02's own R5 remediation
   looking at the wrong machine.

Both errors are corrected here rather than by editing the superseded text below.

---

## SUPERSEDED BODY (retained verbatim; every factual claim in it is now either satisfied or corrected above)

### The fact

The full-board governance report `GOV-2026-09-24-BT-01` — whose verdict
(FAIL, 1 Critical / 7 High / 7 Medium / 1 Low, per the stage diary's
2026-09-24T22:10Z entry) and whose closure-verification lift to CONDITIONAL
PASS the entire build-and-test artifact set relies on — **exists nowhere in
this repository**. Verified 2026-09-27 at HEAD `69b00c4`: a tree-wide glob for
`GOV-2026-09-24-BT-01*` returns no file; `governance/reviews/` ends at
`GOV-2026-09-20-CG-01.md`; a grep finds 17 files CITING the report ID, none of
them the report.

### What survives (the secondary record)

- `governance/CHANGE_RECORD_2026-09-24_GOV-BT-01_rulings.md` — the Student's
  dispositions on all sixteen recommendations (the authoritative record of what
  was RULED, not of what the board WROTE);
- the quotations and per-recommendation references embedded across the
  build-and-test artifact set and the stage diary's 2026-09-24 entries;
- the remediation evidence itself (junit XMLs, `.gitignore` negation, the new
  controls), which stands on its own hashes.

### What is NOT done, and why

The report is **not reconstructed** from the citing artifacts. Reconstructing a
lost governance report from the artifacts it judged would be circular
self-evidence — the refusal recorded at `CR-2026-08-22-INC-CORRECTIONS` and
affirmed as project practice (`project.md`, learned 2026-08-22:
`delivery-planning:c12`). A reconstruction would also carry the authority of a
board that cannot re-sign it.

### Open path (option 1)

The 2026-09-24 board ran on the LOTUS clone
(`C:\Users\LOTUS\Desktop\Thesis_toshkari`, per the artifacts' own root
disclosures). If the original report file exists there, the Student commits it
VERBATIM as `governance/reviews/GOV-2026-09-24-BT-01.md` with a message citing
GOV-2026-09-27-BT-02 R5, and this limitation record is then annotated (never
deleted) as superseded-by-recovery.

### Standing limitation until then

The verdict's findings text, severity assignments, and closure-verification
reasoning are unauditable. Every artifact statement of the form "per
GOV-2026-09-24-BT-01 Rec <n>" traces to the rulings CR and the citing artifacts
only. Gate readers weigh the build-and-test stage knowing this.

---

## Residual — CLOSED same day (2026-09-27)

The **closure-verification pass** that lifted FAIL → CONDITIONAL PASS was likewise
chat-only, recorded durably in nothing but the stage diary's 2026-09-24T23:00Z entry. On
the Student's explicit instruction ("recover the closure-verification pass too") it was
recovered by the same method and written to
`governance/reviews/GOV-2026-09-24-BT-01-CLOSURE-VERIFICATION.md`: the verifier's returned
text verbatim (9,171 chars, 16 closure rows, the "Lift FAIL to CONDITIONAL PASS"
recommendation and its single condition), plus its dispatch brief as a labelled appendix —
that brief being what shows the pass was mandated as an INDEPENDENT ADVERSARIAL check
rather than a confirmation, which is the basis of its authority.

Two facts surfaced by that recovery, recorded rather than reconciled:

- **The pass ran 2026-09-25T08:23–08:33Z**, not 2026-09-24T23:00Z as the diary dates it.
  The diary is never hand-edited and stands; the transcript timestamp is the measured one.
- **Its one condition is now satisfied** — the three site logs were committed 2026-09-25
  (`db15880`) and their hashes independently re-verified by four seats on 2026-09-27 — so
  the Rec 1 `PARTIAL` that the CONDITIONAL PASS hung on is CLOSED.

The verifier's own working record (52 tool uses) survives at
`agent-ac4887d88ddbc8a55.jsonl` in the same transcript directory, should anyone need to
audit how a particular closure was checked.

**Process lesson, for the §13 ritual to consider:** a governance verdict the project relies
on should be persisted as a file at the time it is issued, not left in a chat transcript.
The output contract permits chat-only delivery; this project's gates cite report IDs as
authority, so for THIS project the report should be written. Two of the board's own
findings (R5 here, and R8's never-persisted Kaggle junit) are the same defect class:
load-bearing evidence that was produced but never written down.
