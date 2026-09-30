# CR-2026-09-30-GOV-PV-04-RULINGS: the Student's rulings on GOV-2026-09-30-PV-04

**Status: EXECUTED (documentation), 2026-09-30.**
- No code, config, D-number, commit or run was made.
- The PV-04 report was delivered in chat. It was later persisted as
  `governance/reviews/GOV-2026-09-30-PV-04.md` on the Student's instruction (4.6 gate, revision cycle 4).

**What PV-04 found:**
- Stage 4.6: **CONDITIONAL PASS**. The conditions are Recs 2 and 3.
- D-83 revision 4 as an adoption candidate: **FAIL**.
- 32 findings: 14 High, 13 Medium, 5 Low.

## 1. Rulings (verbatim, 2026-09-30)

- Recs 1–4: Option 1.
- Rec 5: **Option 2**.
- Rec 6: Option 1.
- Rec 7: **Option 2**. This **re-rules PV-02 Rec 10 and PV-03 Rec 4**: the Kaggle fallback now
  excludes DEC, so the confirmatory set becomes mixed-platform.
- Recs 8–13: Option 1.
- Rec 14: **Option 2**. The default is `hard`, scoped as TC-03's note says.
- Recs 15–32: Approved.

## 2. Executed

| Rec | Change | Where |
|---|---|---|
| 1 | The doubled prefix corrected to "PV-01 Rec 16". **All 138 "PV-0x Rec N" references in revision 5 checked by script:** none out of range for its board (PV-01: 20, PV-02: 31, PV-03: 31, PV-04: 32); none doubled. The RSS, access-log and code-commit subjects each resolve to their PV-01 rulings. | D-83 revision 5 |
| 2 | 7 stale pointers repointed from revision 3 to revision 5, with dated notes. The item numbers are kept. | plan, results, matrix |
| 3 | PV-03 persisted as delivered. | `governance/reviews/GOV-2026-09-30-PV-03.md` |
| 4–11, 13–17, 19–21, 26–28, 30, 32 | **D-83 revision 5.** Revision 4 is retained verbatim. | `governance/CHANGE_RECORD_2026-09-29_platform_local_only.md` |
| 12 | M-1: a closed list of rejection grounds, an abort limb, and the precommitment recorded in a file committed before the first run. | `load-test-plan.md` |
| 18 | The item 10 pin limb moved before item 4. The M-1 text says how the pin check is done. | plan; D-83 §R5-5 item 10 |
| 22 | Dated correction to the README's "reproducible from this record". | README |
| 23 | Full conda-layer table, derived by script: 10 version drifts, 7 build-only, 3 absent from the lock, 0 exact. Pointers added at the other 4 sites. **This differs from the PV-04 Data seat's figure of 13 version drifts;** the README states the derivation. | README; results; matrix; PV-02 rulings; D-83 §R1-5 |
| 24 | Bare "Rec N" in the stage artifacts prefixed by the nearest board mentioned on the same line, otherwise PV-01. 53 references were prefixed. 7 misattributions were then corrected by hand. | plan, results, matrix |
| 25 | A one-row-per-Rec status table, and the persistence line corrected. | PV-03 rulings |
| 29 | README: 62 freeze lines = 61 versioned + 1 `pip @ file`. | README |
| 31 | No action (the untracked evidence set is committed at O-5). | — |

## 3. Open

- Every open item is in D-83 revision 5 §R5-5, now 29 rows. The new rows:
  - **26:** December B-01 generation before or after G-05.
  - **27:** move the test harness to its own log root.
  - **28:** precommit the (c) tolerance rule.
  - **29:** the non-comparability D-number and the list of re-runs it requires.
- The full-board re-review of revision 5.
- The acts from PV-03 Rec 12: renormalise, supersede, re-run.

## 4. Added 2026-09-30 (revision cycle 4, at the Student's request)

- Proposed rulings on §R5-5 items 22, 24–29, K, the (c) run count and the re-run cap are recorded as **PROPOSED, NOT ADOPTED** in D-83 revision 5 §R6-5. The record also lists 3 contradictions and a corrected PV-03 Rec 12 execution plan.
- **Still BLOCKED (insufficient evidence):**
  - the re-run cap;
  - `<N>`;
  - K, until §R5-5 item 20 lands.

## 5. Closure check `GOV-2026-09-30-PV-05` (adaptive; Chair, Data and Implementation), with the Student's rulings of 2026-09-30

All 10 recommendations were approved and applied.

1. The verbatim abort message at results l.94 is restored, with a gloss outside the quote.
2. Plan l.44 is repointed to Revision 5. Every stage artifact was re-grepped for `revision [34]` / `§R?-[34]`: only dated historical notes and diary history remain.
3. README correction: 13 = 10 version + 3 absent. The name-mapped view is 11 / 9 / 0, and it exposes `xz` 5.8.2 against `liblzma` 5.8.3.
4. M-1 now cites §R5-5 item 8.
5. M-1 now names the post-restore identity file.
6. Plan l.197 "PV-01 Rec 9" is marked unverifiable. The PV-01 report was never persisted, and Rec 9's subject is consistent with the cited point.
7. The item 24 versus pin-limb ordering is recorded in D-83 §R5-5 item 24 as open for the revision-5 re-review.
8. D-83's "PV-04 is chat-only" is corrected.
9. No change.
10. **The baseline for "53 prefixed" (PV-04 Rec 24), stated:**
    - 53 is the insertion count that the prefix script printed during its single pass on 2026-09-30.
    - The pre-pass file state was **not** recorded, and the files are untracked, so the count cannot be re-derived.
    - The PV-05 Chair counted 63 "PV-0x Rec N" occurrences afterwards. The balance of 10 is consistent with references already prefixed before the pass, **but this is not verified**.
