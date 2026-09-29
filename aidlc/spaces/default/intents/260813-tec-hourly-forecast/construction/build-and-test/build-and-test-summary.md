# Build and Test Summary

**Stage:** build-and-test (3.6) · **Lead:** aidlc-quality-agent ·
**Support:** aidlc-devsecops-agent
**Date:** 2026-09-24 · **Repository commit:** `41fd109`
*(Body baseline. The current state is in the dated addenda at the foot of this
file, most recently "2026-09-29 re-baseline addendum" at HEAD `9710daf`, and the
`GOV-2026-09-29-BT-03` corrections in `build-test-results.md`.)*
**Test strategy:** Comprehensive

## Overall build status

| Aspect | Status |
|---|---|
| Governed interpreter (CPython 3.11 exact) | ✅ Rebuilt this session (3.11.16, conda-forge) |
| Pin surface | ⚠ Partial: 7 of 9 pinned packages exact; `matplotlib==3.9.0` and `tensorflow==2.21.0` unobtainable from reachable channels (PyPI blocked) — disclosed, not substituted |
| Full test suite (post-remediation, `full_post.xml`) | ⚠ **1575 / 1584 passed, 3 failed, 6 skipped** *(corrected 2026-09-27 under `GOV-2026-09-27-BT-02` R14: re-derived from `full_post.xml`'s attributes, 1584 − 3 failed − 6 skipped = 1575; the earlier "1581" counted skips as passes. The 3 failures were the site-log custody rows, since closed — see the 2026-09-25 addendum)* |
| §18.3 critical set (ten-module selection) | ⚠ 677 / 683 passed — the same 3 failures, all in `test_release_hashes.py` |
| Remaining failures | All three are ONE finding: IGS site logs declared in a committed manifest but never committed (swallowed by the generic `*.log` ignore) — ruled option 1 (re-retrieve + verify + commit); retrieval blocked from this network, never-again mechanism already in place |
| Fixture ladder | Stages 00, 01, 02, 04, 05 complete on `plumbing_7day`; 06/07 not yet run *(superseded — stage 06 has since run on the fixture, 2026-09-26; see the 2026-09-27 addendum below)*; `scientific_1month` **manifest freeze** (measured counts, tolerances, runtimes) still open under Q-31 — the window itself was frozen 2026-08-21 as **D-14** (March 2022). *(Corrected 2026-09-27 under `GOV-2026-09-27-BT-02` R15: the earlier "window still an open Q-31 freeze" misnamed the open act.)* |
| Lint (`ruff check .`) | 63 pre-existing findings tree-wide (advisory; no enforced floor) |

## Test type inventory (what this stage generated)

| Artifact | Contents |
|---|---|
| `build-instructions.md` | Environment reconstruction as the build; 2026-09-24 addendum with the measured conda-forge recipe and the two unobtainable pins |
| `unit-test-instructions.md` | pytest under the governed env; 29 on-disk modules vs the 21-module §12 mandated set *(2026-09-24 baseline; **39** on disk at `9710daf`, of which 18 of the 21 mandated are present and the 3 absent are Phase 2-only; see `build-test-results.md` § 2026-09-29, Rec 16)*; per-module function counts; negative-control-per-rule methodology; no enforced coverage floor (Q5=A) |
| `integration-test-instructions.md` | The fixture ladder as the real integration tier; cross-unit boundary module map; measured ladder state; known blockers |
| `performance-test-instructions.md` | Measured-then-frozen runtime envelopes (TE §15.1/§15.2); CPU completeness (TC-01); determinism checks; explicit non-goals |
| `security-test-instructions.md` | Secret scanning (gitleaks, deny-list, hook); locked-test custody; prohibited-flow negative controls; release integrity; §10.1 reuse governance |
| `build-test-results.md` | Executed results: both suite runs with junit-derived counts, the D-68 pin repair, the site-log custody finding with three proposed dispositions |

## Coverage expectations per unit

No numeric floor is enforced (team.md, Q5=A; `targets` deliberately unset —
the sensor's line 80 / branch 70 defaults are advisory reporting only). The
real bar per unit is its named tests passing plus the §16/§19 pass/fail rows:
Phase 1's acceptance set is **WS-01 plus WS-09–WS-20** (team.md
§ Corrections) and the test-bearing TA rows TA-07–TA-09, TA-11–TA-14, TA-17,
TA-18, TA-22, TA-23, TA-26, TA-27. Per-module function counts are tabulated
in `unit-test-instructions.md`.

## Readiness assessment

- **Build-ready:** yes, with the disclosed partial pin surface. A fresh
  session can rebuild the environment from the recorded recipe without PyPI.
- **Test-ready:** yes — the suite runs end-to-end in ~~145 s~~ on CPU
  *(2026-09-29, `GOV-2026-09-29-BT-03` Rec 8: 145 s was the 29-module run of
  2026-09-24. At `9710daf` the 39-module full suite takes **660.7 s** and §18.3
  selection (b) takes **105.8 s** (`run_2026-09-29_bt_fix/{full,crit}.xml`). The
  `plumbing_7day` fixture adds 365–366 s CPU per measuring run. Budget Kaggle
  and TC-03g sessions from these figures.)*; every red
  row is root-caused and owner-routed.
- **Deployment-ready** ("deployment" = dataset/model releases here): **no** —
  blocked on the site-log custody disposition, the open student freeze acts
  (scientific fixture window, fixture tolerances), stages 06/07 of the
  ladder, the TC-03g Kaggle-session run, and the open supervisor gates
  (G-05, G-06, G-07). None of these is this stage's to close.

## Known limitations and outstanding items

*(Renumbered 2026-09-24 after the `GOV-2026-09-24-BT-01` rulings —
`governance/CHANGE_RECORD_2026-09-24_GOV-BT-01_rulings.md` is the execution
record.)*

1. **Site-log custody finding (Rec 1, ruled option 1)** — the never-again
   half is DONE (`.gitignore` negation + the manifest-vs-gitignore control);
   the retrieval half is **blocked from this network** (every GNSS
   data-centre host times out) — the three `test_release_hashes.py` rows stay
   red until a `files.igs.org`-reachable host runs the recorded retrieval
   spec and the verified bytes are committed.
2. **TF and matplotlib absent locally** — M-06 and plots paths unexercised;
   Kaggle (or a PyPI-reachable host) owes the TE §8.1 both-platform check.
3. **WS-20 / TA-17 remain `Pending`** — no full clean-run reproduction yet.
4. **Cross-unit staleness now DISCLOSED in place per `gf-3`** —
   `acquisition` (D-68 pin fix), `governance-guards`, `models-and-baselines`
   and `foundation` (the Rec 8/9/10/16 and Rec 1 amendments) each carry a
   dated addendum in their `code-summary.md`; prior sessions' carried
   staleness stands as recorded in `build-instructions.md`.
5. **`aidlc-state.md` `Project Root`** stale for this clone (second
   recurrence; diary Open questions).
6. **Rec 47 (GitHub Actions on a third platform)** unresolved pending a
   GitHub check; interacts with the tracked `evidence/locked_test_restricted/`
   root (owner ruling open). *(Corrected 2026-09-27 under `GOV-2026-09-27-BT-02`
   R9: the locked-root git-exposure ruling was MADE on 2026-09-24 —
   `governance/CHANGE_RECORD_2026-09-24_locked_root_git_exposure_ruling.md`,
   ACCEPTABLE, conditioned — and the GitHub-check limb closed 2026-09-25. What
   survives open: Rec 47's Student + Supervisor authorization change record,
   and the residual that ruling did not reach — CI-runner accesses whose
   sidecar access records are destroyed with the runner. See the 2026-09-27
   addendum.)*
7. **The operative §18.3 critical-set selection** (Rec 5) — routed to the
   Student; see `build-test-results.md` § "§18.3 selection reconciliation".
   *(Corrected 2026-09-27 under `GOV-2026-09-27-BT-02` R9: RULED on
   2026-09-25 — selection (b), the ten-module §18.3 homes, is THE
   authoritative critical set;
   `governance/CHANGE_RECORD_2026-09-25_item7_selection_b_ruling.md`, D-69.
   Selections (a) and (c) are superseded for §18.3 purposes.)*
8. **Pre-commit hook now ACTIVE on this clone** (Rec 3, ruled option 2;
   `core.hooksPath=.githooks` set and verified 2026-09-24 this session) —
   commits need the governed environment on `PATH`; procedure in
   `build-instructions.md`.

## 2026-09-25 remediation addendum

*(Full derivation in `build-test-results.md` § "2026-09-25 remediation
addendum"; this section is the summary-level pointer, not a restatement.)*

- **Item 1 (site-log custody) — CLOSED.** All three site logs recovered,
  hash-verified, committed, `.gitignore` negation live,
  `test_release_hashes.py` 235/235. This was the only condition this stage's
  prior CONDITIONAL PASS named by number; it no longer holds the verdict
  down on its own.
- **Item 2 (TF/matplotlib absent) — CLOSED locally.** Both now installed at
  exact governed versions in `tec-thesis-311`; pin surface 9/9. The Kaggle
  both-platform check is still owed and is not this addendum's to close.
- **Item 3 (WS-20/TA-17 clean-run) — still Pending**, confirmed by a fresh
  `test_clean_run.py` skip naming the same unmet precondition
  (scientific-fixture manifest still `TBD — freeze gate`).
- **Item 6 (Rec 47 GitHub check) — investigated, not closed.** The workflow
  IS live on GitHub (49 runs); its latest run, at a commit two behind this
  session's HEAD, failed on the exact site-log defect fixed above. No run
  exists yet against the fix. Closing this needs a push, which this
  session is not authorized to do.
- **Item 8 (pre-commit hook) — reconfirmed active**, unchanged.
- Fresh full-suite counts: **1584 total, 1580 passed, 0 failed, 0 errors, 4
  skipped** (`full.xml`, 424.5 s). Fresh §18.3 ten-module selection (b):
  **685/685 passed, 0 failed, 0 skipped** (`crit.xml`, 55.8 s).
- *(Superseded: the verdict below was later replaced by `GOV-2026-09-27-BT-02`
  = FAIL and then by `GOV-2026-09-29-BT-03` = FAIL; see the 2026-09-29 addendum.)*
- **Overall verdict: still CONDITIONAL PASS**, not upgraded to PASS — the
  remaining open conditions (items 3, 4, 5, 6, 7 above) are unresolved by
  this addendum and several are external to this stage (Student freeze
  acts, a push, the Kaggle run). Reliance on this stage's evidence at a
  freeze gate remains prohibited until those close.

## Sources

- Per-unit `code-generation-plan.md` and `code-summary.md` under
  `<record>/construction/<unit>/code-generation/` — this stage's consumed
  inputs across all twelve units.
- `build-test-results.md` (this stage) for every measured number above.
- TE §8.1, §9.1–9.2, §13.1–13.2, §15, §18.3; team.md § Testing Posture,
  § Walking Skeleton, § Deployment, § Corrections; project.md § Mandated,
  § Forbidden.
- `governance/PENDING_FOLLOWUPS.md`, `governance/REC_13_60_STATUS_2026-09-24.md`,
  `governance/RULING_REQUEST_2026-09-23_CONSTRUCTION_STOPS.md`.

## 2026-09-25 item 9 (new, distinct from the pre-existing item 8) — W-6 step 8

**Item 9 (W-6 step 8 — Kaggle durability measurement) — OPEN, newly tracked.** Full
derivation in `build-test-results.md` § "2026-09-25 item 9 (new)". Discovered while
attempting item 2's Kaggle pin verification: `CHARACTERISED_DURABILITY_PLATFORMS` is a
hardcoded empty set in `src/data/config.py`, so `open_restricted()` refuses every
restricted-root read on Kaggle unconditionally, blocking parts of three §18.3 critical
modules (`test_release_hashes.py`, `test_common_masks.py`, `test_locked_test_guard.py`)
— wider than previously documented. Already owner-ruled (`GOV-2026-09-20-CG-01`
Recommendation 57, dispositions §5 item 10, "Student — before G-05") but not yet
actioned; blocked itself on two further preconditions (in-session-gate wiring;
item 3's Q-31 freeze). Item 2 stays blocked on this dependency, not reclassified.

## 2026-09-27 remediation addendum (GOV-2026-09-27-BT-02)

*(Execution record: `governance/CHANGE_RECORD_2026-09-27_GOV-BT-02_remediation.md`.
All 29 recommendations of the 2026-09-27 full-board review were approved by the
Student; this addendum records what that remediation changed in THIS artifact's
lane. The "Overall build status" table above is the 2026-09-24 state with dated
in-place corrections; this addendum and the results file's 2026-09-27 re-baseline
addendum are the current state.)*

- **Re-baseline at HEAD `69b00c4` (R1), derived programmatically 2026-09-27:**
  the tree is 25 commits past the artifacts' `41fd109` baseline. Test modules
  **34** (was 29; +`test_b01_prediction_adapter.py`, `test_fixture_run_fixes.py`,
  `test_gim_generation.py`, `test_gim_provenance.py`, `test_recorded_presence.py`);
  pinned packages **10** (was 9; +`ml_dtypes==0.5.3`, owner-approved 2026-09-26);
  fixture ladder advanced **through stage 06** on `plumbing_7day` (commit
  `7b4109b`, predictions `FIX-NOV-FOLD-01/02`, registry-stamped
  `evidence_class: smoke_only`); owner decisions D-72–D-76 landed; the governed
  release `artifacts/releases/gim_comparator_C-01_2022/` exists (manifest and
  parquet hash independently re-verified by the 2026-09-27 board). **Suite
  junit now exists**, measured 2026-09-27 on a governed host
  (`tec-thesis-311`, CPython 3.11.16, `PYTHONHASHSEED=0`) at commit `70bb651`:
  full suite **2384 total / 2380 passed / 0 failed / 0 errors / 4 skipped**
  (`full.xml`); §18.3 selection (b) **1417/1417** (`crit.xml`);
  `test_release_hashes.py` **965/965** (`release_hashes.xml`); all three new
  negative controls (R3/R11/R23) pass individually and are proven to bite
  (guard reverted → control fails; guard restored → control passes again).
  Full detail, skip reasons, ruff delta, and the bite-proof log:
  `build-test-results.md` § 2026-09-27 re-baseline addendum.
- **Rec 47 status is two-limbed (R2):** the CI-verification limb is closed
  (workflow green at `7357f35`); the custody limb is OPEN — the workflow's
  authorizing Student + Supervisor change record is still owed, and until this
  remediation the workflow's `pytest tests/` step read the restricted December
  root on every push with access rows destroyed with the runner. As of
  2026-09-27 the restricted-reader modules are deselected from
  `.github/workflows/verify.yml` (R2's approved immediate step); checkout still
  materialises the tracked restricted root, which remains part of the owed
  consolidated ruling (`governance/CHANGE_RECORD_2026-09-27_platform_bound_RULING_REQUEST.md`).

## 2026-09-29 re-baseline addendum (HEAD `9710daf`)

*(The full derivation is in `build-test-results.md`, § "2026-09-29 re-baseline
addendum". This section points there; it does not restate it.)*

- **Suite at `9710daf` plus one test-only fix**, on `tec-thesis-311`: the full
  suite ran **2456 total / 2452 passed / 0 failed / 0 errors / 4 skipped**, and
  §18.3 selection (b) ran **1423/1423**
  (`artifacts/exec_evidence/run_2026-09-29_bt_fix/`).
- **Before the fix, 4 intermittent failures.** They came from a same-tick
  timestamp race in `tests/test_common_masks.py`'s receipt helper. Seven limb 2
  and limb 3 negative controls could pass without exercising their limb. The
  owner ruled Option A; the fix is proven to bite; the guard is unchanged.
- **Scope growth since `70bb651`:** 39 test modules (+5/−0); D-77…D-81 adopted;
  the D-74 amendment; the fixture ladder through stage 07; the `plumbing_7day`
  Q-31 candidate manifest is VALID but **not frozen**.
- **Still open, and none of these is this stage's act:** WS-20/TA-17. *(Corrected
  under `GOV-2026-09-29-BT-03` Rec 4: the first owed act is to promote the
  `plumbing_7day` candidate into `fixture_manifest.yaml`, then the Student's Q-31
  freeze of it, including its positive tolerance, then the `scientific_1month`
  freeze.)* Also still open: the
  TC-03g Kaggle-session run, the supervisor gates G-05/G-06/G-07, the custody
  limb of Rec 47, R7's inferred attributions, and the `aidlc-state.md` Project
  Root question.
- **New `gf-3` carry:** `evaluation-and-comparison`'s code-summary is out of
  date for the test edit.
- **Verdict status:** the last governance verdict on this stage,
  `GOV-2026-09-27-BT-02` (FAIL), stands until a fresh review runs. *(Update: the
  fresh full-board review `GOV-2026-09-29-BT-03`
  (`governance/reviews/GOV-2026-09-29-BT-03.md`) returned **FAIL** with 0 Critical,
  6 High, 4 Medium and 7 Low findings. The single blocking ground is Rec 1, the
  unrecorded `source_id` comparison-identity change in `208f138`. The Student's
  rulings on all 17 findings are recorded in
  `governance/CHANGE_RECORD_2026-09-29_GOV-BT-03_rulings.md`.)*
- **Item 5 (`aidlc-state.md` Project Root)** — third stale recurrence recorded
  (R28); dropping/relativizing the field is the routed owner question, no
  hand-edit made this pass.
