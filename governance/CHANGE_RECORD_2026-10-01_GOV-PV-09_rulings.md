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

## Still open for the Student (as of the first rulings; closed by the second rulings below)

- ML-01: whether a determinism precondition applies to the tolerance rule.
- ML-05: whether mixed-unit files get a per-field floor.
- DATA-09: the `environment_id` literals and the variable name to pin in the D-text.
- DATA-11: whether the `/mnt/c` receipt path is in scope for measurement. BENCH-04 prefers measuring it.
- DATA-12: the D-number for the §R5-5 item 29 non-comparability ruling.

## Second rulings (2026-10-01, the Student, in session)

Given as written instructions to the agent, before the revision-8 board. Carried into revision 8 as §A8 items 9 to 13 of `governance/CHANGE_RECORD_2026-09-29_platform_local_only.md`.

| # | Finding | Ruling (substance, from the Student's text) | Revision 8 |
|---|---|---|---|
| 5 | ML-01 (Rec 21) | Deterministic runs first: the tolerance check applies only after the deterministic-run precondition is met; the tolerance never rescues nondeterministic variation; a deterministic reproducibility failure and a tolerance/metric failure stay distinct | §A8 item 9 |
| 6 | ML-05 (Rec 22) | A separate tolerance/floor per field or unit; no shared floor across incompatible fields such as TECU and TECU²; a future field cannot silently inherit a floor | §A8 item 10 |
| 7 | DATA-09 (Rec 23) | Variable name `environment_id`; the allowed literals are the ones already established in the governed repository, not new names; comparisons and pins keyed to `environment_id` | §A8 item 11: `tec-thesis-311`, `b01_iri`, `g07-clean-run` |
| 8 | DATA-12 (Rec 24) | Pre-W-4 environment records are not comparable, recorded in D-83 itself; no new D-number unless the governance structure proves D-83 wrong (it does not) | §A8 item 12 |
| 9 | DATA-11 (Rec 14) | The `/mnt/c` receipt path is in scope for BENCH measurement; add it as required evidence with the same governed identity and provenance; if not yet run, record it OPEN / pending; do not weaken scope | §A8 item 13; §R5-8 row 41 OPEN |

The Student also directed: D-83 is **not** adopted by these rulings, and nothing is committed or pushed by the agent.

## Third rulings (2026-10-01, the Student, in session, on `GOV-2026-10-01-PV-10`)

Given as written instructions to the agent after the seven-seat board `GOV-2026-10-01-PV-10` returned CONDITIONAL PASS on revision 8. Each row gives the substance of the Student's text and where revision 8 records it. Execution status is in `governance/reviews/GOV-2026-10-01-PV-10-REMEDIATION-STATUS.md`.

| PV-10 Rec | Ruling (substance) | Revision 8 |
|---|---|---|
| 1 | **Approve.** The Supervisor confirms that the approval already given also covers revision 8 as currently amended, including items 9–13. Treat this as the revision-8 countersignature. Record its scope accurately; invent no signature, timestamp, quote or document | "Supervisor countersignature for revision 8" |
| 2 | **Approve.** Commit the tolerance implementation after fixing the identified defects. Record the SHA where items 9–12 cite code. Do not push | items 9, 12, 14, 17 (`42a1ca1`, `25ad0f7`) |
| 3 | Put the tolerance code on the real runtime path, with no dead wrapper, and add tests proving the real path invokes it | item 17 |
| 4 | Only `cross_environment_tolerance` governs item 11. `cross_run_variation` is either removed from that path or retained for a stated other purpose | item 17 |
| 5 | Create a formal governed field-to-unit table from existing specifications only, with no invented units. A new field must require an explicit governed definition | item 16 |
| 6 | **Approve.** Fix the infinity-floor defect, with regression tests for `+inf`, `-inf`, a finite value against a non-finite one, and normal floors | items 10, 17 |
| 7 | Fix the harness with deterministic, controlled in-write fault injection and explicit outcome classes. Fabricate nothing. If the mechanism guarantees old-or-new, make the criterion match what it can show | item 14 |
| 8 | Define a governed `/mnt/c` pass/fail/inconclusive criterion before the run, then run the campaign if the environment supports it; otherwise record it as pending | item 15 |
| 9 | Correct the stale revision-7 `/mnt/c` wording without rewriting history | "Corrections" (annotations) |
| — | Reconcile governance references; inspect Recs 10, 15, 16 and 19 rather than assume them closed; adopt D-83 if and only if every prerequisite is actually met; do not push | remediation status |
