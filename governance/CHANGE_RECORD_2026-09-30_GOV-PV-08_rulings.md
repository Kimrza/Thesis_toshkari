# CR-2026-09-30-GOV-PV-08-RULINGS: the Student's rulings on GOV-2026-09-30-PV-08

**Status: RECORDED and carried into D-83 revision 7 (2026-09-30).** D-83 stays a draft: no
D-number has been written, and no run was made.

**The review.** `GOV-2026-09-30-PV-08` — a full board on D-83 revision 6, persisted as
`governance/reviews/GOV-2026-09-30-PV-08.md`. Verdict: CONDITIONAL PASS, 7 of 7 seats; no FAIL, no
BLOCKER. 22 findings: High 11, Medium 10, Low 1. VAL veto limbs 1 and 2 lifted as text; limb 3
(December B-01 one-shot) maintained; reservation on §R5-5 item 11 stands.

## 1. Rulings (verbatim, 2026-09-30)

> "1. Recommendation 1-22 = Approve
> 2. b
> 3. commit yourelf & do the Rec 10 floor, the Rec 11 margin and the TC-03 values."

- **Recs 1–22:** approved, each with its preferred fix.
- **Process:** route **(b)**. Policy fixes go into the D-text; mechanism fixes go into a governed
  code-generation work package reviewed with its code. D-83 is adopted on its policy text; the
  Validation Auditor's code-level reservation is carried into the work package.
- **Blocked values:** the Student instructed Claude to set them. They are drafted as proposed rules
  with derivations in D-83 revision 7 §A7 items 8 (floor), 16 (margin) and 11 (TC-03), and bind
  only through the Student's adoption act and the Supervisor's countersignature of D-83.
- **Commit:** authorised; made by Claude after this record (see git history).

## 2. Where each Rec landed

| Rec | Revision 7 site | Kind |
|---|---|---|
| 1 | §A7 item 1; §R4-7 items 3–4; §W7 W-1 | policy + mechanism |
| 2 | §A7 item 2; §R4-7 item 4; §W7 W-2 | mechanism |
| 3 | §A7 item 3; §R4-7 item 4; §W7 W-3 | policy + mechanism |
| 4 | §A7 item 4; §R4-7 item 3; §W7 W-4 | policy + mechanism |
| 5 | §A7 item 5; §R5-7 rows 7R, 20R, 25R | policy |
| 6 | §A7 item 6; §R4-7 items 1, 11; §W7 W-6 | policy + mechanism |
| 7 | §A7 item 7; §R5-7 row 35 | policy |
| 8 | §A7 item 8; §R4-7 item 11 | policy (floor value) |
| 9 | §A7 item 9; §R4-7 item 11 | policy |
| 10 | §A7 item 10; §R4-7 item 2; §W7 W-5 | policy + mechanism |
| 11 | §A7 item 11; §R4-7 item 10; §W7 W-7 | policy (TC-03 values) |
| 12 | §A7 item 12; §R4-7 items 3–5, 11 | policy |
| 13 | §A7 item 13 | policy |
| 14 | §A7 item 14; §R4-7 item 1; §W7 W-4 | policy + mechanism |
| 15 | §A7 item 15 | policy |
| 16 | §A7 item 16; §R4-7 item 11; §W7 W-8 | policy (margin value) |
| 17 | §A7 item 17 | policy |
| 18 | §A7 item 18; §W7 W-9 | policy + mechanism |
| 19 | §A7 item 19; §R4-7 item 8 | policy |
| 20 | §A7 item 20; §R5-7 row 36; §W7 W-10 | policy + mechanism |
| 21 | §A7 item 21 | policy |
| 22 | §A7 item 22; §R4-7 item 11 | policy |

## 3. Disclosures carried with the values

- **Floor:** a rule (2⁻²³ × max|x| per file), fixed before any (c) run exists. The (a) statistic of
  0.0 was already seen.
- **Margin:** m = max(max − min, ⌈0.10 × max⌉). The plumbing storage values were seen before the rule
  was set. No frozen range may be computed until `storage_total` excludes archived copies (W-8);
  on the existing runs the illustrative range is already exceeded by `d139bf12` (by 1,828 B).
- **TC-03:** the 12 h runtime limb is TC-03's inherited value; the RAM limb is anchored to the (c)
  WSL2 VM MemTotal recorded at G-07 (no `.wslconfig`; 15.67 GiB installed, checked 2026-09-30).
  Peak RSS is not captured yet (W-7).
