# CR-2026-10-01-GOV-PV-09-RULINGS: the Student's rulings on `GOV-2026-09-30-PV-09`

**Date:** 2026-10-01. **Decided by:** the Student (project decision owner), in session, answering
four structured questions put after the seven-seat full board `GOV-2026-09-30-PV-09` returned
**FAIL** on D-83 revision 7 and its §W7 implementation (CHAIR FAIL, TEC FAIL, IMPL FAIL; ML, DATA,
BENCH, VAL CONDITIONAL PASS).

This record states the rulings. It does not edit revision 7. The rulings are carried into D-83
**revision 8**, which will be drafted as a delta on revision 7 and reviewed by the full board
before the D-83 entry is written to `evidence/DECISIONS.md`.

## Rulings (verbatim option chosen)

| # | Finding(s) | Question | Ruling |
|---|---|---|---|
| 1 | CHAIR-01 | Revision 7 names §R5-5 items 3, 4 and 7 as adoption preconditions; items 3 and 4 are open | **"Amend preconditions"**: the preconditions become §R5-5 items 2 and 7 only; items 3 and 4 move to the due dates of their §W7 rows (W-7; W-4/W-8 and the item-4 run) |
| 2 | CHAIR-04, IMPL-11 | How the D-83 entry records the Supervisor's approval | **"Record as countersigned"**. The approval was given verbally and reported by the Student on 2026-09-30 ("i have it but verbally consider it equal to a signature"); no written artifact exists. By the Student's direction it is recorded as the countersignature. The form of the approval is stated alongside it so the register never implies a written signature |
| 3 | CHAIR-05, BENCH-01, VAL-01 | Power-loss trials not run; revision 7 gates §R5-5 item 11 and December re-acquisition on all 330 trials | **"Kill-only admission"**: the 300 kill-fault trials plus detection admit, with the limitation stated (no power-loss evidence; kill faults do not exercise `fsync` against page-cache loss). This is a policy change. It needs its own board review (revision 8) |
| 4 | TEC-01 | Signing G-05 writes into `data.yaml`, so the two B-01 halves can never carry equal config hashes | **"Diff allows only gates"**: assembly allows `data.yaml` to differ only under the `gates` key and records the structural diff in the assembly manifest; every other config must be equal. The §R4-7 item 4 wording changes accordingly |

## Board findings that the board itself noted need no human decision

These are remediated in the code, with a negative control for each, and re-reviewed:

- CHAIR-02, TEC-04 and IMPL-01;
- CHAIR-03 and BENCH-08;
- TEC-02, TEC-03, TEC-05 and TEC-06;
- VAL-02, VAL-03 and VAL-04;
- BENCH-02 to BENCH-07 and BENCH-09;
- IMPL-02 to IMPL-10;
- DATA-01 to DATA-08 and DATA-10;
- ML-02, ML-03, ML-04, ML-06 and ML-07.

Their status is recorded in the PV-09 report and the implementation record.

## Still open for the Student

- ML-01: whether a determinism precondition applies to the tolerance rule.
- ML-05: whether mixed-unit files get a per-field floor.
- DATA-09: the `environment_id` literals and the variable name to pin in the D-text.
- DATA-11: whether the `/mnt/c` receipt path is in scope for measurement. BENCH-04 prefers measuring it.
- DATA-12: the D-number for the §R5-5 item 29 non-comparability ruling.
