# NFR Validation Matrix — Performance Validation (4.6)

> **Model performance is NOT MEASURED.**
> - **Section A** covers pipeline performance, measured or cited up to 2026-09-29.
> - **Section B** lists, before any result exists, checks that future model results will be
>   validated against. Every row there is NOT MEASURED.
> - **Section B is not exhaustive.** Vision §9.5 "Required Results" and the Vision §2.4 tier-5
>   sensitivities are the complete list, and they govern. Section B is a pointer checklist over
>   them.
> - This matrix **points to** governing decisions; it never restates or amends them. Where it
>   seems to differ from a D-number, the Vision or the TE, the source document governs.

**Date:** 2026-09-29 · **HEAD:** `2dd36a7` · **Evidence:** `load-test-results.md` (revision 2)
**Revision 2.** Rewritten under the Student's rulings on `GOV-2026-09-29-PV-01`
(`governance/CHANGE_RECORD_2026-09-29_GOV-PV-01_rulings.md`), PV-01 Recs 10, 11, 13, 16, 17, 18 and 19.
**Confirmed basis:** the re-issued Consolidated Summary Confirmation in
`performance-validation-questions.md` ("Looks correct", 2026-09-29), which covers FU-1R = A and
FU-3 = A. The closure verification (CONDITIONAL PASS) found no defect in this file **as it stood then**. That no longer holds: A-10 later carried a stale FU-1R pointer and a wrong drift narrative, and `GOV-2026-09-29-PV-02` found both. They are corrected in place (PV-02 Rec 24, PV-02 Rec 7; 2026-09-30). `GOV-2026-09-30-PV-03` Rec 1 then corrected the A-10 drift count, which read 22 and should read 6.

## What completing this stage does and does not mean *(PV-01 Rec 19)*

Approving Performance Validation completes the AI-DLC workflow for this intent.

**It does not:**
- validate model performance;
- accept any TEC gate;
- satisfy the scope file's stated deliverable ("measured model and pipeline performance against
  the locked evaluation protocol"). That deliverable is **unmet** here, and only the pipeline
  half is addressed.

**Where the model half now lives:** outside any AI-DLC stage, in the governed runs and in these
gates, all reviewed full-board under the TEC governance overlay:
- G-05 experiment freeze;
- G-06 locked evaluation;
- G-08 claims.

Section B is the checklist handed forward to those gates. Every summary of this workflow, such as
an outcomes pack or a replay, must carry this paragraph's meaning and must never say
"performance validated".

## Upstream inputs

`performance-requirements`, `scalability-requirements`, `performance-design`,
`scalability-design` and `dashboards` are absent by design. All 12 units are `kind: library`,
and `observability-setup` is SKIP; see `load-test-plan.md`. Targets come from the governing
documents instead.

## A. Pipeline performance

| # | Requirement (source) | Target | Actual (evidence) | Status / owner |
|---|---|---|---|---|
| A-1 | CPU is a complete execution path (TC-01; TE §9.2) | Fixture ladder and suite complete on CPU | Suite: 2455 passed / 0 failed / 4 skipped at `391a319`, CPU only. Fixture: `plumbing_7day` stages 00–07 completed on CPU, but run `d139bf12` is registry-`aborted` at composition, and `scientific_1month` has never run. | **PARTIAL**: suite and plumbing stages only; the ladder has not run *(PV-01 Rec 18; revision 1 said MET)* |
| A-2 | No GPU-only dependency (TE §9.2) | None | Every run above was CPU only | **MET** |
| A-3 | Fixture runtime measured, then frozen (TE §15.1–§15.2; Q-31) | Range frozen by the Student | Three **wall-clock** figures: 365.156 / 366.109 / 378.75 s. The per-stage Δ sits in 04–06. **Not CPU time** (PV-01 Rec 5). A two-run min–max range has no statistical meaning: a third exchangeable run lands outside it with probability 2/3 (PV-01 Rec 18). | **OPEN.** Not fit to freeze as labelled. Student to rule what §15.2 means, before Q-31. |
| A-4 | Fixture storage measured, then frozen (TE §15.2) | Same as A-3 | 14,778,806 / 17,076,359 / 19,375,740 B. **78.8% of the current root is archived copies**; live outputs are 2,392,814 B (PV-01 Rec 4). | **MEASUREMENT INVALID.** Code ruling before any storage freeze (Student) |
| A-5 | Each run records the correct code commit (TE §13.1, §13.4) | Correct `code_commit` per row | `d139bf12` is correct (clean state recorded only in prose). 648 rows across 15 runs carry `208f138` while the code changed until `9710daf` (PV-01 Rec 6). | **NOT MET** for 15 runs (disclosed). Student: dirty-tree guard ruling, before G-07 |
| A-6 | CPU/GPU type, runtime and **peak memory** recorded per run (TE §9.2) | All recorded | Runtime and platform label are recorded. CPU is recorded only as `platform.machine()` (the ISA). GPU type and peak RSS are not recorded. | **NOT MET.** Owner: Student. Due: before G-07, and before D-83 adoption (PV-01 Rec 16). The Student's `GOV-2026-09-29-PV-02` Rec 12 = 1 confirmed this "before adoption" reading, and D-83 revision 5 now carries it; revision 2 had said "before retiring Kaggle". |
| A-7 | Determinism under fixed seeds (NFR-DET-01; TC-21; WS-17) | Determinism modules green | Green inside the `391a319` full pass. Fingerprints and non-runtime blocks are identical across three runs (PV-01 Rec 18). | **MET** at test and fixture level. Caveat: `ml_dtypes` is off-pin (PV-01 Rec 9, disclosed) |
| A-8 | Critical set green before governed runs (TE §18.3) | 0 failures | 1426/1426 at `391a319`, with `ml_dtypes` off-pin | **MET** for the current commit, with the pin caveat |
| A-9 | Both fixtures pass, in order, before any full-year job (TE §9.2) | Two pass receipts | Neither receipt exists | **NOT MET**: no full-year job is permitted |
| A-10 | Preflight: install from pins plus skeleton run on the governed platform(s) (TE §9.2; TC-03g) | Report per platform | *(Corrected 2026-09-30, `GOV-2026-09-29-PV-02` Recs 7 and 24.)* The D-71 offline from-scratch rebuild of 2026-09-25/26 produced the locked environment **on another host**; `%LOCALAPPDATA%\tec-envs\tec311` does not exist on this laptop. It is **not evidence for this host**. This laptop's `tec-thesis-311` (created 2026-09-18) was **never built from the locks**:<br>• 3 of 32 wheel-lock entries drift;<br>• 6 of 61 pip packages sit in neither lock, and 2 more drift against the conda lock (`fonttools`, `pytz`) *(corrected 2026-09-30, PV-03 Rec 1; this previously read 22)*;<br>• 20 conda packages are installed, against 119 in the lock, with 0 build strings matching; Full conda-layer drift: 10 version, 7 build-only, 3 absent from the lock; see the snapshot README table (PV-04 Rec 23).<br>• the Python build differs from the lock.<br>Under PV-02 Rec 7 = 2 the environment is kept, and its governed identity is its recorded full freeze after the `ml_dtypes` restore (`evidence/environment_identity_2026-09-30_tec-thesis-311/`). The Kaggle limb now depends on D-83 revision 5 being adopted and countersigned, not on FU-1R, which is answered. | **OPEN.** Student runs M-4 (un-gated) before G-07, against the recorded identity |
| A-11 | Full-year runtime | Measured | Not extrapolated (Q5 = A) | **NOT MEASURED**: first Class C run |
| A-12 | Suite wall time | Recorded | 660.7 s at `9710daf` **plus an uncommitted test edit**; 1007.7 s at `391a319`; critical set 62.5–105.8 s | **Recorded**; no target exists |
| A-13 | IRI-2016 workload timed (Vision §6.11) | 26,000-call workload timed | 2,160 calls in 535.353 s on WSL2 (the session record says 527.6 s, unreconciled) | **PARTIAL**: 26,000-call figure NOT MEASURED *(added, PV-01 Rec 18)* |

## B. Model performance: checks declared in advance (all NOT MEASURED)

**Declared 2026-09-29 and re-issued as revision 2 the same day, before any Jan–Nov or December
model result exists.**

Citation conventions:
- **Bare D-numbers** (`D-13`, `D-55`) are in `evidence/DECISIONS.md`.
- **"Vision D-nnn"** refers to the Vision's own §14.2 decision table.

Supervisor status of B-1 to B-4's authorities:
- D-78 to D-81 are owner-approved with no Supervisor row recorded.
- D-82's countersignature is **OPEN**.
- D-84's countersignature is **OPEN**.

All are G-05 inputs (PV-01 Rec 17).

| # | Check (pointer, not restatement) | Authority | Evidence that will close it | Blocked by |
|---|---|---|---|---|
| B-1 | Confirmatory estimand exactly as frozen; sign convention stated in every table; Δ_RMSE% labelled derived and never the evidence basis | D-78; Vision §2.3; TE §3 glossary "Paired loss differential"; TE §18.2; Vision D-126 | Evaluation output computing the D-78 quantity per comparison | Full-year job (A-9) → G-05 (incl. Supervisor countersignature of D-78–D-82) → G-06 |
| B-2 | Frozen vector time-block bootstrap, incl. 48 h sensitivity and cross-station correlation | D-79; TE §13.6; TC-19 | Governed `bootstrap_summary`; seed and replicate count match D-79 | As B-1 |
| B-3 | Comparison sets and one comparison-wide mask per set; identity vs provenance | D-80; D-82; NFR-FAIR-01; TC-16 | Mask manifest, one per D-80 set; `test_common_masks.py` green | As B-1 |
| B-4a | **Pre-G-05 December coverage and regime-count audit**: performance-blind; access row `purpose=coverage_audit`, `performance_inspected=false`; counts over the D-59 day range from GFZ Kp/Hp60 at a recorded release grade, never provisional Dst; **D-13 H4/SRQ-5 status recorded before the G-05 freeze** | Vision §8.3 bullet 1; Vision §9.3; D-81; D-13; D-59; D-11; Vision §12.1 R-13; Vision §13.1 G-05 row | Audit report incl. Kp grade, D-13 event count and outcome, dated before G-05 | Before G-05 |
| B-4b | Post-G-06 regime breakdown using the frozen thresholds and storm rule, labelled **descriptive**, not an additional confirmatory hypothesis | D-81; Vision §9.3; Vision D-128 | Regime report | G-06 |
| B-5 | The three difficulty controls co-reported in the primary table; M-03 is **station-and-hour** with D-55's mandatory limitation wherever reported; persistence is the declared baseline; primary-set membership | Vision §2.4 tier 2; PC-03/PC-04, **as superseded for M-03 by D-55 and D-84**; D-58; D-80 | Primary table with all three controls plus D-55's limitation text | G-06 |
| B-6 | Binding honesty rule: any control that **achieves a lower paired loss than the LSTM on the locked test** is disclosed in the primary table and abstract conclusion | Vision §2.4; PC-04 | Primary table and abstract text | G-06 → G-08 |
| B-7 | Locked test: predictions written once after G-05, hashed before any metric | Vision §8.3 bullets 3–4; Vision D-125; Vision §13.1 G-06 row; OC-03 (as superseded by Vision §8.3 for coverage and regime counts) | `AccessRecord` `purpose=locked_evaluation` with the G-05 signature reference; one locked-evaluation access row per artifact; write-once refusal (`06_train_and_predict.py:725`); `prediction_hash` recorded before the metrics file (R-18 writer role); SD-C-02 mask containment fields | G-05 and **G-P1A** |
| B-8a | IRI joined only at evaluation, on the `primary` mask. Every IRI comparison carries: the D-45 retrospective-inputs, no-operational-superiority disclosure; the Vision §6.11 2000 km ceiling / plasmasphere disclosure; the spatial-representativeness statement | Vision §7.1; Vision §6.6; Vision §6.11; D-45 item 3; NFR-IRI-01; Vision D-114 | Evaluation output with each disclosure; `test_iri_denial.py` green | G-04; full-year B-01 route (plan M-5); G-06 |
| B-8b | GIM joined only at evaluation, on the `gim` mask, described as **map-product to map-product** | Vision §6.10; D-72; D-80 | GIM comparison report | G-06 |
| B-9 | `gim_network_overlap_flag` disclosed per station, for ARUC with D-73's two residuals; no independence claim; December status **undetermined** | D-73; TE §5.2; Vision §6.10 | `gim_interpolation_and_independence_report` | December-scope ruling (extend the audit under the access check, or disclose Jan–Nov applicability) before G-06. The Jan–Nov audit is **complete**. |
| B-10 | Three-seed element-wise mean is the confirmatory prediction; per-seed results and spread reported; failed runs visible | Vision §8.8; Vision D-122; TE §13.5; NFR-DET-01 | Predictions for the `seeds.yaml` seeds, their mean and spread | G-05 → governed training runs |
| B-11 | Model, feature, threshold and hyperparameter selection on Jan–Nov only | Vision §8.3, §8.7; Vision D-124 | Selection record (`models.selected`), no December input | Governed Jan–Nov tuning run |
| B-12 | Practical relevance | **D-34** (governs; not restated) | Per D-34 | Per D-34 *(PV-01 Rec 11, option 2)* |
| B-13 | Phase 2 is a fixed-protocol replication on a new target lineage, not an independent blind test; no numerical equivalence across phases | Vision §3.6.2; TE §7.0B; Vision §6.6; `project.md` Forbidden (TEC-05) | Abstract-level text; `prior_period_exposure=true` in the locked-test access record | G-P2 / G-P3 |
| B-14 | Claims bounded to the frozen scope | D-8; Vision §2.5; D-28 | Claims review | G-08 |
| B-15 | Per-station metrics and paired skill, and the time-weighted pooled summary | Vision §5.5, §8.5, §9.1, §9.5; Vision D-105; Vision D-126 | Per-station tables | G-06 → G-08 |
| B-16 | Top-1%-error-removed sensitivity, incl. per-station removed/retained counts | Vision §2.4 tier 5; Vision §8.10; D-54; Vision D-128 | Sensitivity table | G-06 |
| B-17 | Target uncertainty budget reported **adjacent** to the primary result | Vision §6.9; Vision §9.5 | Primary result section | G-06 → G-08 |
| B-18 | Ablations predeclared, and never replacing, redefining or rescuing the primary comparison | Vision §8.10; Vision §2.4; TE §7.2; Vision D-118 | Ablation registry in `experiment.yaml`; ablation tables labelled subordinate | G-05 → G-06 |
| B-19 | Quality-stratified diagnostics, and validation-fold performance across F1–F4 | Vision §9.4, §9.5 | Diagnostics and fold tables | G-05 / G-06 |
| B-20 | `locked_test_accessed = true` on the G-06 registry entry; any post-access test-driven change labelled exploratory | Vision §8.3 bullets 4–5; Vision D-125 | Registry row; exploratory labels. **Depends on the one-governed-log ruling (PV-01 Rec 14).** | PV-01 Rec 14 ruling → G-06 |

The full-board review under the governance overlay is mandatory at G-05, G-06, G-08 and model
advancement.

## Summary

| Status | Section A | Section B |
|---|---|---|
| MET | 2 (A-2, A-7) | 0 |
| MET with caveat | 1 (A-8) | 0 |
| PARTIAL / recorded | 3 (A-1, A-12, A-13) | 0 |
| OPEN / NOT MET / invalid | 6 (A-3, A-4, A-5, A-6, A-9, A-10) | 0 |
| NOT MEASURED | 1 (A-11) | 22 (B-1–B-3, B-4a, B-4b, B-5–B-7, B-8a, B-8b, B-9–B-20) |

**Totals:** 13 Section A rows and 22 Section B rows (3 + 2 + 3 + 2 + 12).

**Derivation:** `grep -cE "^\| A-[0-9]+ \|"` and `grep -cE "^\| B-[0-9]+[ab]? \|"`, printed
before this table was written.

## Sources

- `load-test-results.md`, `load-test-plan.md`, `performance-validation-questions.md`
- `governance/CHANGE_RECORD_2026-09-29_GOV-PV-01_rulings.md`
- Code-generation outputs (`code-generation-plan.md`, `code-summary.md`) via `construction/build-and-test/`
- `evidence/DECISIONS.md`: D-8, D-11, D-13, D-28, D-34, D-45, D-54, D-55, D-58, D-59, D-72, D-73, D-78–D-82, D-84
- Vision: §§2.3–2.5, 3.6.2, 5.5, 6.6, 6.9–6.11, 7.1, 8.3, 8.5, 8.7, 8.8, 8.10, 9.1, 9.3–9.5, 12.1, 13.1, 14.2 (Vision D-105, D-114, D-118, D-122, D-124, D-125, D-126, D-128)
- TE: §§3, 5.2, 7.0B, 7.2, 9.2, 13.1, 13.5, 13.6, 15.1–15.2, 18.2
- `ideation/feasibility/constraint-register.md`
