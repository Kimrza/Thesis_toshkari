# CR-2026-09-30-GOV-PV-07-RULINGS: the Student's rulings on GOV-2026-09-30-PV-07

**Status: stage part EXECUTED; D-83 part RECORDED for revision 6 on its own track (2026-09-30).**
No code, config, D-number, commit or run was made.

**The review.** `GOV-2026-09-30-PV-07` was delivered in chat and later persisted as `governance/reviews/GOV-2026-09-30-PV-07.md`. It covered:
- a full-board review of D-83 revision 5;
- the PV-06 fix-check leftovers.

**Verdicts:**
- Stage 4.6: **CONDITIONAL PASS**, conditioned on Recs 22 and 23.
- D-83 revision 5 as an adoption candidate: **FAIL** (a TEC BLOCKER on December B-01).

**Findings:** 25 in total — 1 Critical, 13 High, 9 Medium, 2 Low.

**Validation Auditor veto, modified:**
- **Lifted:** a DEC read on Kaggle.
- **Kept:**
  - the G-05 exemption loophole (Rec 4);
  - `_access_timestamp` (Rec 5);
  - the uncoded December B-01 one-shot (Rec 1).
- It stays reserved on §R5-5 item 11.

## 1. Ruling (verbatim, 2026-09-30)

> "all of your recommendations are approved with the option you recomend"

The ruling covers Recs 1–25, each with its recommended option. It also covers the process
recommendation, **route (a)**: close stage 4.6, and continue D-83 as its own governed track.

## 2. Executed now (stage 4.6)

| Rec | Change |
|---|---|
| 22 | `load-test-plan.md` l.44: the stray `*` is removed. |
| 23 | `load-test-plan.md` l.157: now adds "the ordering obligation is §R5-5 item 8". |

## 3. Recorded for D-83 revision 6 (its own track; not drafted here)

These are the approved changes, each with its recommended option (full text in the PV-07 report):

| Rec | What revision 6 must do |
|---|---|
| 1 | Split B-01 into a pre-G-05 January–November run and a post-G-05 December-only run. In code: a month-12 refusal unless `verify_g05_signature` passes; write-once output; a receipt in (b) at generation, re-verified in (a); a one-shot refusal per `phase_id` with `script_id="04_build_external_products"`; the missing-field-as-match rule; negative controls. **Owners: Student and Supervisor.** |
| 2 | D-text item 11, "Precommitted values", carrying the four Student decisions. |
| 3 | Label the re-rulings of the PV-04 Rec 11 cap limb and of the earlier board Rec 5 / ML-04. Add a new §R5-5 row: convert the test; a frozen zero-width refusal; `len(measuring_run_ids) ≥ 2`; `cpu_total` stays non-zero; a frozen-width schema field. |
| 4 | Delete the §R3-5 1(a) admitted-environment exemption. Admission is by lock hash only. |
| 5 | Code ruling: `_access_timestamp` uses `logged_at_utc` only, with a forged-timestamp control. |
| 6 | The Kaggle fallback: the recommendation offered two alternatives, so **the variant is still the Student's choice**: add `k_kaggle_fallback`, or declare it dormant in code until its own D-number. Agreed in either case: a closed list of infrastructure triggers; at most one invocation per `phase_id`; both draws reported; a tolerance leg on invocation. |
| 7 | `environment_lock_hash` derived from `fields(RunRecord)`; a registry `environment_id` extension; the snapshot sites; control 31 widened. |
| 8 | One pin rule per layer (conda compared on exact URL plus md5). `environment_id`, the `--all` capture and D-number 29 land together, before item 4. The D-number act lives only in item 29, and item 24's ordering question is answered: **earlier**. |
| 9 | The PV-03 Rec 12 plan: a forced renormalisation rewrite; a commit and clean-tree step; reinstall **before** measuring; a D-number for the `interpreter_exception` edit; re-record the config hashes. |
| 10 | Precommit the (c) tolerance statistic, the quantities it covers, and the zero→positive mapping. Record (c) = 2 as a Student decision. Define the "cause fixed" evidence standard. **The values are the Student's.** |
| 11 | A storage margin/floor precommitted in the M-1 file, plus three extra negative controls. **The value is the Student's.** |
| 12 | Cite `phase_id` from `data.yaml target.identity.phase_id`, with an equality assertion. |
| 13 | `REQUIRED_FIELDS_MAP`: the recommendation named no default, so **the choice between an entry-point refusal and a mode-scoped key is still the Student's.** |
| 14 | Re-cite the script-04 table to `_generate_benchmark` → `run_gated_generation`, and list the second `verify_runtime` call. |
| 15 | Dated supersession notes on all the stale text. |
| 16 | N per fault × write type × filesystem; a named injection method; exact bounds (2.95% and 25.9%); a limitation clause in D-number 11. |
| 17 | A §R5-5 row for executing the durability measurement. |
| 18 | D-text item 3 gains its three statements; the provenance adds PV-04; "Rec 47" gets its prefix. |
| 19 | Restate item 27: enumerate the governed logs, exclude the closed log by path, add a closure guard. |
| 20 | `script_id` required only on `locked_evaluation`. |
| 21 | December re-acquisition from (a) only. |
| 24 | A TC-03 limit-derivation rule before G-07. |
| 25 | The authority-level-6 qualifier on the 2.3 GB figure. |

**Still open for the Student, as values or variant choices:** Rec 6 (the variant), Rec 10 (the statistic,
the quantities and the mapping), Rec 11 (the margin), and Rec 13 (the approach).
