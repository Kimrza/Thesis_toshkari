# CR-2026-09-30-GOV-PV-03-RULINGS: the Student's rulings on GOV-2026-09-30-PV-03

**Status: EXECUTED (documentation), 2026-09-30.**
- No code, config, D-number, commit or run was made.
- The report `GOV-2026-09-30-PV-03` was delivered in chat. It was later persisted as
  `governance/reviews/GOV-2026-09-30-PV-03.md` under PV-04 Rec 3.

**What PV-03 reviewed, and what it found.**
- **Scope A:** closure verification of the PV-02 remediation.
- **Scope B:** a full board on D-83 revision 3.
- **Verdicts:**
  - stage 4.6: CONDITIONAL PASS, on condition that Rec 1 is fixed;
  - D-83 revision 3 as an adoption candidate: FAIL.
- **Findings:** 31 in total. 12 High, 13 Medium, 6 Low.

## 1. Rulings (verbatim, 2026-09-30)

- Recs 1–9: Option 1.
- Rec 10: **Option 2**.
- Rec 11: Option 1.
- Rec 12: **Option 3**.
- Recs 13–14: Option 1.
- Recs 15–31: Approve.

## 2. Executed

| Rec | Change | Where |
|---|---|---|
| 1 | Drift re-derived against both locks and printed. The correct figure is 6 in neither lock, not 22. `fonttools` and `pytz` drift against the conda lock. 0 of 20 conda build strings match the lock. All five sites corrected, with dated notes. | snapshot README; `load-test-results.md`; matrix A-10; D-83 §R1-4; PV-02 rulings §2 |
| 2–4, 6–21, 23, 27–29, 31 | **D-83 revision 4.** Revision 3 is retained verbatim. | `governance/CHANGE_RECORD_2026-09-29_platform_local_only.md` |
| 5 | M-1: K ≥ 2, the run designations, and the extra-run rule are all precommitted. Rejected run sets stay on record. | `load-test-plan.md` |
| 8, 25 | README: section references corrected; "verification, not rebuild" stated. Results l.30 now carries the Rec 7 consequence. | README; results |
| 22, 23, 26 | §3a now reads 49 lines, pattern-bounded, with 2 sites relabelled. The §3b and §3c drafts are revised. The Persistence line is corrected. | `CHANGE_RECORD_2026-09-30_GOV-PV-02_rulings.md` |
| 24 | Sidecar note added. It is marked superseded as a receipt. | `artifacts/external/b01.WHEEL_IDENTITY_NOTE.md` |
| 30 | "HEAD blob" relabelled as a content SHA-256; the git blob id `020c6500` is added. | results |

**Deviation from strict "prefix every reference" (Rec 20).**
- Every bare "Rec N" in D-83 revision 4 was prefixed by script.
- One exception was left as it is: "Rec 47 / P2 record". It names a different record's numbering,
  not PV-01, PV-02 or PV-03.

## 2a. One row per recommendation *(added 2026-09-30, `GOV-2026-09-30-PV-04` Rec 25; supersedes the grouped §2 table for status)*

| Rec | Status |
|---|---|
| 1 | Executed: 5 sites corrected |
| 2 | Executed in text: D-83 rev 4 §R3-4 item 2; code open |
| 3 | Executed in text: §R3-4 item 1(a); code open |
| 4 | Executed in text: §R3-4 item 6. Later re-ruled by PV-04 Rec 7 = 2 |
| 5 | Executed: M-1 precommitment. K is open |
| 6 | Executed in text: §R3-4 item 5 |
| 7 | **Student choice (Option 1).** Executed in text: §R3-4 item 9; code open |
| 8 | Executed in text: §R3-4 items 3 and 9; README |
| 9 | Executed: §R5-4 ordering |
| 10 | **Student choice (Option 2).** Executed: §R3-4 item 7 |
| 11 | Executed in text: §R3-4 item 8; the ruling is open (item 23) |
| 12 | **Student choice (Option 3).** Decided and recorded; **the acts are open** (renormalise, supersede, re-run) |
| 13 | Executed in text: §R3-4 item 2 |
| 14 | Executed in text: §R3-4 item 1(b) |
| 15 | Executed in text: `phase_id` key |
| 16 | Executed in text: TBD fields; config untouched |
| 17 | Executed in text: §R3-4 item 11 |
| 18 | Executed: §R1-4 host row |
| 19 | Executed: §R3-4 item 13; §R5-4 row 17 |
| 20 | Executed: prefixes (one wrong; fixed under PV-04 Rec 1) |
| 21 | Executed: D-text item 10 |
| 22 | Executed: PV-02 rulings §3a (49) |
| 23 | Executed: PV-02 rulings §3c |
| 24 | Executed: sidecar note |
| 25 | Executed: README, results, persistence line |
| 26 | Executed: §3a relabels |
| 27 | Executed: smoke call (quoted verbatim under PV-04 Rec 26) |
| 28 | Executed: §R3-4 item 14 |
| 29 | Executed: §R3-4 item 15 |
| 30 | Executed: results l.123 |
| 31 | Executed: §R3-4 items 1(b) and 2 |

## 3. Open (Student / Supervisor acts)

All open items are in D-83 revision 4 §R5-4, 25 rows in total. The rows new in revision 4:
- **20 and 21:** the PV-01 Rec 4 and Rec 5 code rulings.
- **22:** handling of an aborted run, and the cutoff field.
- **23:** the per-environment critical subset.
- **24:** the scope of the `environment_id` refusal, and its relation to `TEC_PLATFORM`.
- **25:** the loss-rate bound implied by `<N>`.

Also still open:
- **Rec 12 = 3:** renormalise the configs, supersede the November receipt, re-run the B-01 fixture.
- **Rec 5:** set K.
- **Rec 21:** state the envelope's binding status at adoption.
- **Revision 4:** its full-board re-review.
