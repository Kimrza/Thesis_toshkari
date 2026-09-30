# Performance Validation — Questions

**Stage:** performance-validation (4.6) · **Lead:** aidlc-quality-agent
**Depth / Test Strategy:** Comprehensive / Comprehensive (`aidlc-state.md`)
**Date:** 2026-09-29 · **HEAD:** `2dd36a7`

## Facts derived before asking (not assumed)

| Fact | Derivation |
|---|---|
| **All five required inputs are absent, all by design.** `performance-requirements`, `scalability-requirements`, `performance-design` and `scalability-design` exist for no unit. `dashboards` does not exist. | All 12 units are `kind: library` (`grep -cE "^    kind: library" unit-of-work-dependency.md` = 12). `nfr-requirements` `produces_kinds` limits the first two to `service`/`ui`. `observability-setup` is SKIP, which removes `dashboards`. See `verification/phase-check-construction.md`. |
| **No service, traffic or deployment target**, so load, latency, throughput and auto-scaling have nothing to attach to | `team.md` § Deployment; `construction/build-and-test/performance-test-instructions.md` § Explicit non-goals |
| **The scope's stated deliverable** is "measured model and pipeline performance against the locked evaluation protocol" | `.claude/scopes/aidlc-research-pipeline-governed.md`, Operation paragraph |
| **Model performance cannot be measured today** | The locked December test needs G-05 signed (G-06, one-shot, hash before metrics). Jan–Nov fold results need a full-year job, and both walking-skeleton fixtures must pass first (`project.md` Mandated). `scientific_1month` has never run: `tests/fixtures/scientific_1month/fixture_manifest.yaml` has `status: candidate` and every measured field is `TBD — freeze gate`. |
| **Pipeline runtime has measured evidence** | `plumbing_7day` candidate manifest `…-20260929T133720Z-4a959333.yaml`, `runtime.cpu_total` 365.156–366.109 s and `storage_total` 14,778,806–17,076,359 bytes, over two measuring runs. `status: candidate`; promotion is the Student's Q-31 act. |
| **Suite timings.** At `9710daf`: full suite 660.7 s, §18.3 selection (b) 105.8 s. At `391a319`: full suite 1007.7 s, attributed to host load, and crit 62.5 s. | `build-test-results.md` § 2026-09-29 addenda |
| **The measuring runs predate the commit that holds their code.** Both ran at 13:30Z and 13:37Z. `9710daf` (src/scripts) landed at 13:57Z. `391a319` and `2dd36a7` touch no `src/` or `scripts/` file. | `git log --format=%ad`; `git show --stat 391a319` |
| **No Kaggle runtime measurement exists.** The only Kaggle runbook covers the B-01 IRI leg alone. | `governance/RUNBOOK_2026-09-26_kaggle_b01_fixture_leg.md` |

## Question 1
The inputs this stage was written for do not exist in this project. Given that, what should this stage validate?

A) Pipeline performance now. Model-performance rows are declared in advance, each marked NOT MEASURED with its blocking gate.
   > **Impact**: The matrix covers what can be measured today: CPU completeness (TC-01), runtime and storage envelopes, determinism (NFR-DET-01), and the Kaggle-session obligation (TC-03g). Model performance appears only as declared checks with a named blocker, and no figure is claimed. Approving the stage completes the AI-DLC workflow. The actual model evaluation then happens as governed runs outside any stage, unless this stage is re-run later by a stage jump.

B) Park the workflow here until Jan–Nov model results exist, then run this stage on model and pipeline performance together.
   > **Impact**: Keeps the scope's stated deliverable inside AI-DLC, where the gate record lives. The workflow stays open for an open-ended time, behind many Student and Supervisor acts: Q-31 fixture freezes, the fixture ladder, the full-year job and the tuning run. Locked-test metrics would still be excluded until G-06. Nothing is produced now.

C) Skip the stage, record the reason, and let the workflow complete.
   > **Impact**: The cheapest option. It is honest about absent-by-design inputs. It leaves no Operation-phase record of the runtime evidence that already exists, and none of the model checks declared in advance. It also contradicts the scope file's rationale, which says this stage is "the deliverable, not an afterthought".

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A. It produces a real, evidence-backed record from what exists today, with every gap named, and it declares the model checks before any result exists, which closes the door on choosing checks after results are seen. B is the right choice if you want AI-DLC itself to hold the model-evaluation gate. The trade-off is an open-ended park with nothing produced now. The risk of A: a completed workflow can be misread as "performance validated". The matrix must therefore say, in its first line, that model performance is NOT MEASURED.

[Answer]: A

## Question 2
Where should the pipeline runtime evidence come from? (Relevant for 1A; also used by 1B later.)

A) Existing evidence only: the two `plumbing_7day` measuring runs, plus the suite timings in `build-test-results.md`.
   > **Impact**: No new run, no new registry rows, fast. The runtime figures stay tied to a pre-commit tree. The code matches `9710daf` by timing only, so the anchoring would rest on a timestamp argument.

B) Existing evidence, plus one fresh `plumbing_7day` run at HEAD `2dd36a7` on this host.
   > **Impact**: Ties a runtime measurement to a known commit, which is the lesson of `GOV-2026-09-29-BT-03` Rec 3. It shows whether the candidate range holds. A third figure outside the range becomes a finding for your Q-31 act, never a change to the range. It costs about 6 min CPU and appends `started`/`completed` registry rows and a run snapshot (NFR-AUD-01). On a loaded host the timing is indicative only.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B. The commit-anchoring gap is exactly what the last full board graded MAJOR, and one smoke-scale run closes it cheaply. The fixture is TC-03f smoke evidence, so the run carries no scientific weight and cannot touch December. Every local timing will carry a host-load note. The frozen envelope stays your Q-31 act, taken from runs you designate.

[Answer]: B

## Question 3
How should model performance appear in `nfr-validation-matrix.md`? (Relevant for 1A.)

A) Declare each check now, marked NOT MEASURED, naming its blocking gate and the evidence that will close it. The checks restate the frozen decisions and never amend them:
- the D-78 estimand;
- D-79 bootstrap;
- D-80 comparison sets and masks;
- D-81 regimes;
- co-reported difficulty controls;
- the binding honesty rule;
- the spatial-representativeness statement;
- `gim_network_overlap_flag` disclosure;
- the Phase 2 non-independence statement.
   > **Impact**: Fixes the check list before any result exists (Vision §8.3; `project.md` Forbidden on post-hoc choices), and gives the G-05 and G-06 reviewers a ready checklist. The risk is that the matrix is read as a protocol document, so it must state that D-78–D-81 and the Vision are authoritative and the matrix only points to them.

B) Pipeline rows only, with one paragraph stating that model performance is out of this stage's reach.
   > **Impact**: The smallest artifact, with no risk of paraphrase drift against D-78–D-81. It leaves the future model evaluation without a declared checklist, which then has to be assembled later, closer to when results are visible.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A. A checklist written while nothing can be seen is worth more than one written at G-06. Every row will cite its D-number or Vision section verbatim by reference, not restate thresholds, to keep paraphrase drift out.

[Answer]: A

## Question 4
TC-03g requires the critical set and both fixtures to run inside the Kaggle session before any governed run there, and no Kaggle runtime figure exists. What should `load-test-plan.md` provide?

A) A Kaggle-session runtime-measuring runbook for you to execute: the critical set and the `plumbing_7day` ladder inside one session, capturing wall/CPU time per stage and the session's hardware identity. Its preconditions build on `RUNBOOK_2026-09-26_kaggle_b01_fixture_leg.md`.
   > **Impact**: Turns the Kaggle budget from unknown into a measurement plan. You operate it, as with the B-01 runbook, because no agent can run inside the Kaggle session. `scientific_1month` stays out until its manifest exists. The matrix's Kaggle rows stay NOT MEASURED until you return the output.

B) No runbook. Kaggle runtime is recorded as an open item only.
   > **Impact**: Less to write now. The Kaggle budget for the full-year job stays unplanned, and it is the platform where the governed runs actually execute.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A. Local timings say nothing reliable about the platform the governed runs execute on (`project.md` Mandated, the TC-03g rule), and a session killed mid-run by a timeout is the failure a measured budget prevents.

[Answer]: X — "i dont want to run anything on kaggle anymore i have both gpu and cpu on my own laptob and i like to do all the code runnings on my local system" (verbatim, 2026-09-29T16:29:08Z; discussed, final ruling in Follow-up FU-1)

## Question 5
Should the stage estimate full-year runtime from the 7-day fixture, for run budgeting? *(Reworded 2026-09-29 before it was answered: "Kaggle session budgeting" became "run budgeting", because Q4's answer puts the platform itself in question. Options unchanged.)*

A) No. Only measured figures; full-year runtime stays NOT MEASURED.
   > **Impact**: Nothing invented. The fixture uses the D-70 fixed apparatus hyperparameters, not the governed grid search (D-121/D-124), so training and tuning cost does not scale linearly with days. Any multiplier would understate cost by an unknown factor. Full-year budgeting waits for a measured run.

B) Yes, as a labelled planning estimate (linear in days, and separately per stage) that never enters any manifest or matrix target.
   > **Impact**: Gives a rough order of magnitude now. The label reduces the risk of it being read as a frozen or measured value but does not remove it, and the estimate is structurally biased low for tuning.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A. TE §15.1 says runtimes are "measured from the fixtures and frozen, never invented". A linear extrapolation across a grid search is closer to invented than measured, and a measured run on the chosen platform (FU-1) is the route to a real figure.

[Answer]: A

## Follow-up FU-1 (from Question 4's answer)
You answered Q4: *"i dont want to run anything on kaggle anymore i have both gpu and cpu on my own laptob and i like to do all the code runnings on my local system"*. That is a change to the governed platform roles, not a load-test-plan detail. Facts checked on this laptop, 2026-09-29:

| Fact | Source / derivation |
|---|---|
| TE §9.1 fixes the roles. **Kaggle** is "Primary compute and Phase 1 acquisition/audit host". **Local** is "Development, small tests, fixture runs, review, artifact inspection". | `PreFlight/Technical_Environment…md` §9.1 |
| TE §9.2 requires the `environment_and_cpu_preflight_report` to show install-from-pins "on **both** Kaggle and local". The Vision's G-07 checklist says "CPU clean-run contract tested on Kaggle and local". | TE §9.2; Vision checklist, CPU budget row |
| Vision **D-129** (Q-29, Approved): "Kaggle plus local only". TC-03c is `binding: hard`. | Vision decision table; `constraint-register.md` |
| **B-01 (the IRI-2016 benchmark) runs only on Kaggle today.** D-49's environment exception (CPython 3.10.12, `iricore==1.8.0` manylinux wheel) is personal to a Kaggle session. `iricore` is **not installed** in `tec-thesis-311`, and no route to it on native Windows has been found. | `find_spec('iricore')` = False; D-49; `RUNBOOK_2026-09-26_kaggle_b01_fixture_leg.md` |
| **The local pins now hold.** `tec-thesis-311`: CPython 3.11.16, `tensorflow` 2.21.0, `matplotlib` 3.9.0, matching `requirements.txt`. | `conda run -n tec-thesis-311 python -c …` |
| **Your RTX 3060 is invisible to TensorFlow here.** TF 2.21 on native Windows reports "GPU support is not available on native Windows for TensorFlow >= 2.11"; `list_physical_devices('GPU')` returns `[]`. GPU would need WSL2. It stays an optional accelerator only (TC-01; TE §9.2 "No GPU-only dependency"). | `nvidia-smi`; TF import on this laptop |

Under `project.md` § Way of Working, a stage answer can narrow what a rule requires, but it cannot relocate a rule the governing documents fix. This stage can therefore draft the change; it cannot enact it. How should it proceed?

A) Draft a platform change record, with proposed D-number text for you to adopt, making **local the sole execution platform** for every remaining run, B-01 included. It needs a Supervisor countersignature, because it amends D-129 and TE §9.1/§9.2. This stage then plans local-only runtime measurement and names two blockers: B-01's local route (WSL2 Ubuntu is the candidate, which also needs a D-49 amendment) and the countersignature.
   > **Impact**: Fully honours your preference. Until it is countersigned, Kaggle stays a governed platform on paper, but nothing forces a run there. B-01 is blocked until a local `iricore` route is proven and ruled. WSL2 would also give TensorFlow your GPU, still only as an accelerator.

B) The same change record, but **Kaggle kept for B-01 only** (the D-49 IRI leg); local for everything else.
   > **Impact**: The narrowest amendment. B-01 keeps its only proven route, so nothing new blocks it. It still needs the countersignature. It does not fully meet "nothing on Kaggle anymore".

C) No platform change now. This stage plans local-only runtime measurement and records the Kaggle limb of TC-03g and TE §9.2 as an open, unplanned item.
   > **Impact**: The least paperwork. It leaves the governing documents saying Kaggle is primary compute while practice says otherwise, which is exactly the kind of documents-versus-practice gap the board keeps grading MAJOR. The G-07 preflight report would then fail its "both platforms" row.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A. It is your stated preference, and it routes the change the only way it can legitimately land: a D-number you adopt plus the Supervisor's countersignature. The B-01 route is the real cost, and naming it as a blocker keeps it visible. Choose B if you would rather not put the IRI benchmark on an unproven local route.

[Answer]: A

## Superseded first summary (confirmed 2026-09-29 before FU-2; kept as record)

**Answers recorded:**
- **Q1 = A:** validate pipeline performance now. Model-performance rows are declared in advance, NOT MEASURED, each with its blocking gate.
- **Q2 = B:** use the existing `plumbing_7day` measuring runs and suite timings, plus one fresh `plumbing_7day` run at HEAD `2dd36a7` on this laptop. The fresh run is smoke evidence, carries a host-load note, and appends registry rows.
- **Q3 = A:** declare the model checks now. D-78 estimand, D-79 bootstrap, D-80 sets and masks, D-81 regimes, difficulty controls, honesty rule, representativeness, GIM-overlap disclosure, Phase 2 non-independence. Each is cited by reference and never restated or amended.
- **Q4 = X, resolved by FU-1 = A:** local becomes the sole execution platform, B-01 included, **proposed, not enacted**. The stage drafts a change record with proposed D-number text for the Student to adopt; it needs a Supervisor countersignature because it amends D-129 and TE §9.1/§9.2. `load-test-plan.md` plans local-only runtime measurement. Named blockers:
  - B-01's local `iricore` route (WSL2 candidate; needs a D-49 amendment);
  - the countersignature.
- **Q5 = A:** no extrapolation. Full-year runtime stays NOT MEASURED.

**Contradiction check:** none found. Q2's fresh run is a fixture run, which TE §9.1 already allows on local, so it does not wait on FU-1's countersignature. FU-1 changes no frozen value and fills no `TBD — freeze gate`.

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct

## Follow-up FU-2 (Q2's fresh run: mechanics found after confirmation)
These were checked after the summary was confirmed. They change what Q2 = B involves, so they come back to you before any run:

| Fact | Source |
|---|---|
| A rerun refuses existing outputs. `04` refuses "gim_comparator.parquet already exists", `05`'s `write_bundle` "refuses an existing directory", and `06` writes "predictions … exactly once". A fresh run first needs the current derived outputs **archived by rename, never deleted**, as `CR-2026-09-29-Q31-CLOSURE` did (`*.archived-q31-…`). | `grep` over `scripts/0*.py`; Q-31 closure CR |
| A plain run compares against the **frozen** reference manifest, which does not exist (the reference `fixture_manifest.yaml` still carries `TBD — freeze gate`). A measuring run (`--emit-candidate --identity`) writes a **new** candidate file next to the existing one. It never writes `frozen`, and the existing candidate is untouched. | `scripts/run_walking_skeleton.py` argparse help |
| **Finding: the runtime evidence names the wrong code.** Both measuring runs (`…133040Z-978317da`, `…133720Z-4a959333`) are recorded in `artifacts/registry/experiment_registry.jsonl` with `code_commit` `208f138…`. They ran on the uncommitted tree that became `9710daf`, which changed `src/data/fixture_outputs.py` (+799), `scripts/07_evaluate_and_report.py` (625 lines) and others. The `code_commit` field is wrong for those two runs. Registry rows are append-only (NFR-AUD-01), so the fix is a disclosure, never an edit. | registry rows; `git show --stat 9710daf` |

How should the fresh run go?

A) Archive the current `plumbing_7day` derived outputs by rename (`*.archived-pv-2026-09-29`), then run one **measuring** run at HEAD `2dd36a7` with `--emit-candidate --identity tests/fixtures/plumbing_7day/identity_declaration.yaml`. It writes a third candidate file next to the existing one, and your Q-31 act chooses which candidate to promote. The `code_commit` finding is disclosed in `load-test-results.md`.
   > **Impact**: Gives a runtime figure correctly anchored to a commit, and closes the gap the finding opens. It renames a set of files, appends registry rows, and adds a candidate file. Nothing is deleted or frozen. About 6 min CPU, with a host-load note. If a stage refuses (for example the D-76 R-13 conflict), the refusal is recorded as the result, not worked around.

B) No fresh run (Q2 falls back to A). Use the existing evidence, with the `code_commit` finding disclosed and the two runs marked "code identity: 9710daf-equivalent by timing only, registry says 208f138".
   > **Impact**: Touches nothing on disk. The runtime evidence stays weakly anchored, and the finding stays open until a later commit-anchored run.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A. Only a commit-anchored run closes the finding, and the archive-by-rename pattern already has a precedent here. Choose B if you would rather not change fixture outputs before your Q-31 act.

[Answer]: A

## Superseded second summary (confirmed 2026-09-29 before GOV-2026-09-29-PV-01; kept as record)

*Re-issued 2026-09-29 after FU-2. The block above was confirmed before the rerun mechanics were known. It stands as a record, and this block supersedes it.*

**Answers recorded:** Q1 = A; Q2 = B, made concrete by FU-2 = A; Q3 = A; Q4 = X resolved by FU-1 = A; Q5 = A. All are as summarised above, with these FU-2 changes:
- **Before the fresh run:** the current `plumbing_7day` derived outputs are archived by rename (`*.archived-pv-2026-09-29`). Nothing is deleted.
- **The run itself:** one measuring run at HEAD `2dd36a7` (`--emit-candidate --identity …/identity_declaration.yaml`). It writes a third candidate file and leaves the existing candidate untouched. It never freezes anything; Q-31 stays your act.
- **If a stage refuses:** the refusal is the recorded result.
- **Disclosure in `load-test-results.md`:** the registry `code_commit` finding. The two earlier measuring runs are recorded under `208f138` but ran on code that became `9710daf`. It is disclosed, never edited, because rows are append-only.

**Contradiction check:** none. The run is fixture-scale local work, which TE §9.1 allows today.

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct

## Correction to FU-1 (2026-09-29, `GOV-2026-09-29-PV-01` Recommendation 1)

*The FU-1 answer above is left standing, unedited. This note records that it was given on a false fact.*

The FU-1 fact table said: *"B-01 (the IRI-2016 benchmark) runs only on Kaggle today. D-49's
environment exception … is personal to a Kaggle session."* Option A's impact said B-01 would be
blocked "until a local `iricore` route is proven and ruled". Option B's impact said B-01 "keeps its
only proven route". **These statements were wrong when written.** The conductor had not checked
the decision register.

| Correct fact | Source |
|---|---|
| **D-49 addendum 2 (2026-09-28)** rules WSL2 (Ubuntu) on this laptop (`LAPTOP-TV4UGFBC`) IN as satisfying D-49's B-01 exception, recorded as the **`local`** platform. It does not extend to model training or the fixture ladder. | `evidence/DECISIONS.md` l.3510 ff. |
| B-01 has **already run on WSL2**: pin check before PASSED; R-59 validation `passed`; 2,160 November rows, 0 errors; pin check after PASSED | `artifacts/exec_evidence/run_2026-09-28_b01_wsl_local/SESSION_A_LOCAL_EXECUTION_RECORD.md`; `artifacts/external/b01/` |
| This stage's own run `d139bf12` consumed those WSL2 B-01 rows | `predictions/FIX-NOV-FOLD-01/B-01.json` |
| **What is genuinely still open for B-01 on the local route:** <br>• the full-year run needs fixture receipts from the same environment identity, but addendum 2 excludes the fixture ladder; <br>• the WSL2 install was not done with `--require-hashes`, and the wheel hash in the report is declared, not measured; <br>• the Fortran runtime and glibc (2.43, not 2.35) are unrecorded in the D-text; <br>• the Kaggle smoke-value reproduction in the governed `b01_iri` environment is not recorded. | `GOV-2026-09-29-PV-01` Recs 1 and 3 |
| `ml_dtypes` is 0.5.4 in `tec-thesis-311` against the pin 0.5.3, so "the local pins now hold" was also wrong | `pip freeze`; `requirements.txt:41` (Rec 9, disclosed) |

## Follow-up FU-1R (FU-1 re-put on the corrected facts)
Given the corrected facts, how should the platform change proceed? Whatever you choose, the drafted D-83 is redrafted, not enacted. It also carries the board's other conditions: custody binding for G-06 (Rec 2), the full authority list (Rec 3), and the feasibility precondition (Rec 16).

A) Local as the sole platform for all remaining runs, B-01 included under D-49 addendum 2. D-83 ratifies addendum 2 and names its open limbs, including the extension to the B-01 fixture runs.
   > **Impact**: Meets "nothing on Kaggle anymore". B-01 stays on the WSL2 route already exercised. Full-year B-01 still needs the fixture-run extension and the identity checks before it can run. Kaggle stays dormant, not retired, until a local `scientific_1month` run measures runtime, RAM and storage (Rec 16).

B) Local for everything except B-01; Kaggle kept for the B-01 leg only.
   > **Impact**: Uses Kaggle, which you said you no longer want. It keeps the receipt path that D-49 addendum 1 already solved on Kaggle. Given that addendum 2 exists and the WSL2 route has run, the "only proven route" argument for this option no longer holds.

C) No platform change for now. Keep TE §9.1's roles on paper and run locally under D-49 addendum 2 where it already applies. Record the Kaggle limb of TE §9.2 as open for G-07.
   > **Impact**: No D-83 to draft or countersign. Documents and practice stay in conflict, and G-07's "both platforms" row cannot be met while you do not use Kaggle.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A. It is your stated preference, the route it relies on already exists in the register, and the board's conditions attach to it cleanly. The real remaining cost is the B-01 fixture-run extension and identity checks, which all three options leave open in some form.

[Answer]: A

## Follow-up FU-3 (the corrective measuring run, `GOV-2026-09-29-PV-01` Rec 8)
Run `d139bf12` aborted before composing a candidate. Any new measuring run today would compose
archive-contaminated storage and `mask_manifest` values (Rec 4), and it would record wall-clock
time as "CPU" (Rec 5). What should happen to the corrective run?

A) Defer it until the Rec 4 and Rec 5 code rulings are made and a clean root exists. It becomes your first designated measuring run toward Q-31, using the corrected command in `load-test-plan.md` M-1.
   > **Impact**: The next run's figures are fit to freeze. Nothing runs now, and no more registry rows or archives are added. The stage closes with the fixture timing evidence as it stands, fully disclosed.

B) Decline it entirely, and let Q-31 designate from the existing runs.
   > **Impact**: The fewest runs. The existing runs' storage and `mask_manifest` values are contaminated and their "CPU" figure is wall time, so Q-31 would then need its own fresh runs anyway.

C) Run it now with the corrected command.
   > **Impact**: A composed candidate today. That candidate would carry the known-invalid storage range and `mask_manifest`, and add another 52-row registry pair and another archive set.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A. A run made before the measurement definitions are fixed produces figures that cannot be frozen.

[Answer]: A

## Consolidated Summary Confirmation

*Re-issued 2026-09-29 after `GOV-2026-09-29-PV-01` and the Student's rulings on it. The two earlier confirmation blocks stand as records, and this block supersedes them.*

**Answers recorded:**
- **Q1 = A:** pipeline performance now; model checks declared in advance. The matrix now states that completing the stage does not validate model performance (Rec 19).
- **Q2 = B via FU-2 = A:** the fresh run executed and aborted; this is disclosed. **FU-3 = A:** the corrective run is deferred until the Rec 4 and Rec 5 code rulings are made and the root is clean. It will be the first designated Q-31 measuring run.
- **Q3 = A:** Section B is re-issued as 22 pointer rows under a non-exhaustive header (Vision §9.5 governs). B-12 points to D-34 only (Rec 11).
- **Q4 = X, FU-1 = A superseded by FU-1R = A (corrected facts):**
  - D-83 is redrafted as revision 2: local is the sole platform, in three named environments, and Kaggle is dormant.
  - It ratifies D-49 addendum 2.
  - Locked-test custody conditions and the G-06 binding are added.
  - Two named blockers: a WSL2 G-07 clean-run environment, and the B-01 fixture-run extension.
  - It is proposed, not enacted, and needs Student adoption plus Supervisor countersignature.
- **Q5 = A:** no extrapolation.
- **Rec 12:** written as D-84.

**Contradiction check:**
- FU-3 = A and FU-1R = A agree: both route measurement to clean, local, designated runs.
- Rec 9 = 2 (disclose the `ml_dtypes` drift only) sits consistently beside D-83 §R5 item 8, which restores the pin before any *governed* run. The disclosure covers the past; the restore is a precondition for the future.

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
