# CR-2026-09-29-GOV-PV-01-RULINGS: the Student's rulings on GOV-2026-09-29-PV-01

**Status: PARTLY EXECUTED (updated 2026-09-29 after the closure verification, CONDITIONAL PASS).**
The documentation corrections are applied. O-1 and O-2 are closed (§3a). The items still open in §4 wait for
a Student act, a Supervisor act or a code ruling. **No code was changed** and **nothing was committed**.

**Authority.** The full-board report `GOV-2026-09-29-PV-01` (verdict FAIL) was delivered in chat on 2026-09-29
against AI-DLC stage `performance-validation` (4.6), intent `260813-tec-hourly-forecast`. The
report was not persisted to `governance/reviews/`, because the review skill writes a file only
when asked and no one asked. This record is therefore the durable trace of the recommendations
and the rulings on them. The limitation is stated here rather than repaired by reconstruction
(`project.md` delivery-planning:c12).

## 1. Rulings (verbatim option numbers, 2026-09-29)

| Rec | Subject | Ruling |
|---|---|---|
| 1 | FU-1 and D-83 rest on a false D-49 premise | **1**: correct every representation and put FU-1 back to the Student |
| 2 | D-83 moves G-06 onto the platform the custody guard exempts; one-shot collision | **1**: name the consequence; take a local durability measurement, then a D-number; bind G-06 to CPU-only `tec-thesis-311`; G-07 re-hashes and never regenerates |
| 3 | D-83 scope incomplete | **1**: derive and name every authority surface; add the second clean-run environment, B-01 fixture-run extension, B-01 identity list, CI/transfer/identity clauses |
| 4 | `storage_total` dominated by archives; `mask_manifest` contamination | **1**: record now; code ruling before Q-31; fresh runs in a clean root |
| 5 | `cpu_total` is wall-clock | **1**: disclose, give the per-stage breakdown; Student rules what §15.2 means |
| 6 | `code_commit` defect on 15 runs, shared cause | **1**: enumerated disclosure plus a dirty-tree guard (code ruling) |
| 7 | Archive custody misdescribed | **1**: disclose in full; supplementary untracked-outputs manifest; commit with the registry rows and measuring result; cite `9710daf:`; promote no candidate before a clean run |
| 8 | Run departed from the confirmed summary | **1**: dated corrections to plan and diary; put the corrective-run choice to the Student |
| 9 | Environment off-pin (`ml_dtypes` 0.5.4 vs pin 0.5.3) | **2**: disclose only |
| 10 | Section B omits checks and disclosures | **1**: add pointer rows; name Vision §9.5 as the exhaustive list; split B-8; widen B-7 |
| 11 | B-12 contradicts D-34 | **2**: point to D-34 only |
| 12 | B-5 vs D-55 conflict | **Other**, verbatim: *"We need to formally record that the new decision(D-55) replaces the old definition, and that only the new decision is to be used and applied."* |
| 13 | B-4 omits the H4 record and the coverage limb | **1**: split into B-4a / B-4b |
| 14 | R-20 `exploratory` reads two logs | **1**: one governed access log, one constant, a test (code ruling) |
| 15 | Phase handoff lists 3 of 12 gates | **1**: full 12-row table quoted from Vision §13.1 |
| 16 | Local-compute feasibility unevidenced; RAM unowned | **1**: owner and gate for A-6; peak-RSS / CPU-model capture (code ruling); local `scientific_1month` measurement as a D-83 precondition; Kaggle dormant until then |
| 17 | Section B pointer/blocker errors | **1**: fix every pointer; route the inherited `project.md` errors to §13 |
| 18 | Section A overstatements | **1**: relabel and add the rows |
| 19 | Completion could be misread; D-83 routing gaps | **1**: add the paragraph; un-gate M-4; fallback and equivalence sentences |
| 20 | Conflict and record hygiene | **1**: agent-role voice; add G-06 to D-83 item 4; point B-14 at its sources |

## 2. Executed in this pass (working tree, uncommitted)

| Rec | What changed | Where |
|---|---|---|
| 1 | Correction note beside the FU-1 answer, which is not edited; new question FU-1R put to the Student | `performance-validation-questions.md` |
| 1, 2, 3, 16, 19, 20 | *(Superseded: now at Revision 2, §3a.)* Change record marked **SUSPENDED pending FU-1R**, with a correction box and the redraft list. The redraft waits for the re-answer, because the answer may change its content. | `governance/CHANGE_RECORD_2026-09-29_platform_local_only.md` |
| 4, 5, 6, 7, 9, 14, 18 | Results rewritten. It now carries: <br>• storage decomposition, derived and printed <br>• wall-clock disclosure and per-stage breakdown <br>• 15-run `code_commit` disclosure <br>• full custody account <br>• off-pin disclosure <br>• R-20 split-log disclosure <br>• exit code, row count, aborted status | `load-test-results.md` |
| 8, 16, 19 | M-1 corrected; M-4 un-gated and aligned to `environment/bootstrap_env.ps1`; M-5 corrected | `load-test-plan.md` |
| 10, 11, 13, 16, 17, 18, 19 | Matrix rewritten. Section B now has a non-exhaustive header, pointer rows, B-4a/b, B-8a/b, and B-12 pointing to D-34 only. | `nfr-validation-matrix.md` |
| 15 | 12-gate table; five `verify.yml` commits | `verification/phase-check-construction.md` |
| 8, 20 | Superseded Tradeoff marked; correction entries; agent-role voice | `memory.md` |
| 12 | **D-84** written on the Student's instruction; Supervisor countersignature OPEN | `evidence/DECISIONS.md` |
| 7 | Supplementary untracked-outputs manifest for the `archived-pv-2026-09-29` set | `artifacts/untracked_outputs_manifest_2026-09-29_pv.json` |

## 3. Rec 12: D-84

Written to `evidence/DECISIONS.md` on the Student's instruction. D-55 supersedes the
"station×month×hour" wording in Vision §2.4 tier 2, Vision §8.4, PC-03 and `project.md`
Mandated, and only D-55 is used and applied. The in-place annotations of the Vision and the
constraint register need owner approval per `CHANGE_RECORD_PROCEDURE.md`. The `project.md`
line is corrected only through the §13 ritual.

> **Annotation, 2026-09-30 (`GOV-2026-09-29-PV-02` Rec 17 = 1).** The site list above (four
> passages), and the D-84 amendment's "full, grep-derived set" (seven passages), both cover only
> the authority documents and the memory layers.
>
> A governed-tree sweep found **22 further forward-looking passages**:
> - D-24 item 17 in the same register;
> - 21 passages in AI-DLC stage artifacts.
>
> The sweep, a disposition for every hit, and the proposed further amendment are in
> `governance/CHANGE_RECORD_2026-09-30_GOV-PV-02_rulings.md` §3. Nothing is written to
> `evidence/DECISIONS.md` until the Student adopts it.

## 3a. Closed later the same day

- **O-1 closed.** FU-1R = A (answered on corrected facts).
- **O-2 closed.** FU-3 = A: the corrective run is deferred until the Rec 4 and Rec 5 code rulings and a clean root. It will be the first designated Q-31 measuring run.
- **O-3 drafted.** D-83 revision 2 is in `CHANGE_RECORD_2026-09-29_platform_local_only.md` §R1–§R5. It still needs the Student's adoption, the Supervisor's countersignature and a full-board review (G-06, G-07).
- **Summary re-confirmed.** The stage's summary was re-confirmed ("Looks correct") after the rulings.

## 4. Open (not performable by the agent in this pass)

| # | Item | Owner |
|---|---|---|
| O-1 | ~~Re-answer FU-1 on the corrected facts (FU-1R)~~ **CLOSED**: FU-1R = A | Student |
| O-2 | ~~Corrective measuring run~~ **CLOSED**: FU-3 = A, deferred until the Rec 4 and Rec 5 rulings and a clean root | Student |
| O-3 | Redraft D-83 per Recs 2, 3, 16, 19, 20 after O-1; then Student adoption and Supervisor countersignature. Validation Auditor veto on item 1 stands until Rec 2 closes. | Agent drafts; Student and Supervisor |
| O-4 | Code rulings (each needs a negative control; none are coded): <br>• Rec 4: storage measure excludes archives <br>• Rec 5: CPU seconds <br>• Rec 6: dirty-tree guard in `capture_environment_lock`, `--code-commit` refusal, `working_tree_dirty` <br>• Rec 14: one governed access log <br>• Rec 16: peak RSS and CPU model | Student |
| O-5 | Commit the stage outputs, the 52 registry rows, the d139bf12 measuring result and the supplementary manifest (Rec 7). **Also** commit the three archived GIM release files, which `.gitignore` l.120 deliberately does not ignore (added 2026-09-30, `GOV-2026-09-29-PV-02` Rec 26), together with the in-place-rewritten canonical `releases/gim_comparator_C-01_2022/release_manifest.json`:<br>`artifacts/walking_skeleton/plumbing_7day/releases/gim_comparator_C-01_2022.archived-pv-2026-09-29/{excluded_rows.json, gim_comparator.parquet, release_manifest.json}` | Student |
| O-6 | In-place annotation for D-84 of every forward-looking passage in its 2026-09-29 amendment (Vision l.171, 294, 775; TE l.458; PC-03; `project.md` l.111). The amendment was added after the closure verification, on the Student's approval; Supervisor acknowledgement of D-84 | Student; Supervisor |
| O-7 | §13 corrections: <br>• `project.md` M-03 wording (D-84) <br>• `project.md` pointer errors (Rec 17) <br>• `team.md` "No CI service is used" | Student at the learnings gate |
| O-8 | Local durability measurement (W-6 step 8 on local) before any G-06 or pre-G-05 audit on local (Rec 2) | Student |
