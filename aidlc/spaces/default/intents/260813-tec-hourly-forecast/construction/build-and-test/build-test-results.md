# Build and Test Results

**Stage:** build-and-test (3.6) · **Lead:** aidlc-quality-agent
**Date executed:** 2026-09-24 · **Repository commit:** `41fd109` (working tree additionally
carrying this stage's artifacts, one test amendment listed below, the
`GOV-2026-09-24-BT-01` remediation edits recorded in
`governance/CHANGE_RECORD_2026-09-24_GOV-BT-01_rulings.md`, and one untracked run-snapshot
directory `artifacts/run_snapshots/20260924T192432Z-79c9b825/` — the four governed-config
snapshots written by this session's suite execution; its tracking policy is a separately
owed owner decision, disclosed here per Rec 11)
**Platform:** local (Windows), one of the two authorised platforms (TC-03c). The
TC-03g Kaggle-session run is NOT covered by anything on this page.

## Build result (environment reconstruction)

"Build" in this project is environment reconstruction plus verification
(`build-instructions.md`). Executed this session:

| Step | Result |
|---|---|
| Locate prior governed env (`tec-thesis-311`) | **Gone** — it lived under the Windows Temp tree, cleaned between sessions |
| Network probe | `pypi.org` times out; `repo.anaconda.com` 200; `conda.anaconda.org` (conda-forge) 200; GitHub 200 |
| Miniconda silent install (user-scoped, no PATH change) | exit 0 (first attempt into the long scratchpad path failed with NSIS exit 2; short path succeeded) |
| Env create from conda-forge | **Success**: CPython **3.11.16** (exact governed pin, TS-01/TC-03d) |
| Pins read back from the created env | numpy 1.26.4 · pandas 2.1.4 · pyyaml 6.0.1 · scikit-learn 1.4.2 · pyarrow 16.1.0 · pytest 8.2.2 · ruff 0.4.8 — all exactly as `requirements.txt` |
| `matplotlib==3.9.0` | **Unobtainable** from reachable channels (conda-forge win-64 has no 3.9.0; anaconda main starts at 3.9.2). Not substituted — the pin is owner-frozen (Rec 38). Environment is matplotlib-absent; `src/evaluation/plots.py`'s lazy import refuses by name when reached. |
| `tensorflow==2.21.0` | **Unobtainable** (no Windows conda build at 2.21.0; PyPI unreachable). Environment is TF-absent; the suite asserts both TF states by design. |

The environment lock for this run therefore records a **partial pin surface**
(7 of 9 pinned packages, interpreter exact). This is disclosed, not worked
around; the reconstruction recipe is the dated addendum in
`build-instructions.md`.

## Test results (full suite)

Counts read programmatically from the run's junit XML, never from prose
(`project.md` § Way of Working):

| Run | Total | Passed | Failed | Errors | Skipped | Wall time |
|---|---|---|---|---|---|---|
| Full suite, first pass | 1582 | 1572 | **4** | 0 | 6 | — |
| Full suite, clean re-run (after the fix below; re-run because a `git stash` cycle briefly raced the first pass — stage diary, Deviations) | **1582** | **1573** | **3** | 0 | 6 | 145.5 s |
| §18.3 critical-set modules (ten-module selection listed below) | 683 | 677 | **3** | 0 | 3 | 38.1 s |
| Full suite, POST-remediation (after the `GOV-2026-09-24-BT-01` ruling execution — two new controls collected; persisted as `full_post.xml`) | **1584** | **1575** *(corrected 2026-09-27: 1584 − 3 − 6 = 1575; the earlier "1581" counted skips as passes — `GOV-2026-09-27-BT-02` R14)* | **3** | 0 | 6 | 138.5 s |

Critical-set selection run: `test_prepared_target_schema`,
`test_feature_availability`, `test_iri_denial`, `test_split_embargo`,
`test_train_only_transforms`, `test_common_masks`, `test_checkpoint_restore`,
`test_bootstrap`, `test_release_hashes`, `test_locked_test_guard` — the
module homes of §18.3's ten named items (DCB-sign belongs to Phase 2 and has
no Phase 1 module by design). This selection differs from the 766-test
critical run recorded 2026-09-24 in `governance/PENDING_FOLLOWUPS.md` §1a;
both are stated with their own selections rather than reconciled by
assumption.

Environment note for both runs: `PYTHONHASHSEED=0` set (TE §13.2); the suite
appended test-mode access rows to the **sidecar log**
`artifacts/exec_evidence/test_access_log.jsonl` — not to
`evidence/test_run_access_log.jsonl`, which was closed 2026-09-20 under
GOV-2026-09-20-CG-01 Rec 1 and shows a zero diff. *(Corrected 2026-09-24
under Rec 4 of `GOV-2026-09-24-BT-01`, option 2: the earlier sentence
migrated from a pre-Rec-1 diary entry of 2026-09-18.)*

**§18.3 selection reconciliation (Rec 5, ruled option 1).** Three "critical
set" selections coexist and must not be conflated: (a) the hook's
**commit-time subset** — five modules, restricted readers deselected under
Rec 30 option 1; (b) the ten-module §18.3 selection this stage ran (683
tests); (c) the 766-test selection behind `governance/PENDING_FOLLOWUPS.md`
§1a's "766/766 passed". The 766/766 figure has **no surviving junit
evidence**: the only committed 766-test XML
(`artifacts/exec_evidence/run_2026-09-24/junit_final.xml`, host
LAPTOP-TV4UGFBC, 01:12Z) records 766 tests with **2 failures** — the pre-fix
chokepoint run. Set-differencing (b) against that XML's IDs shows the
766-test selection spans all 29 modules *(29 at 2026-09-24; 39 at `9710daf`)* while (b) is the ten §18.3 module
homes; and the green report was made while the three site-log bytes were
already absent from tracking, so it can only have run against untracked
local bytes or a selection excluding those rows. **Which selection is THE
§18.3 critical run is routed to the Student** — an open decision this
artifact does not make.

## Failure 1 (repaired): stale `PURPOSES` pin vs D-68

`tests/test_acquisition.py::test_purposes_gained_the_two_acquisition_values_compatibly`
failed with `assert 6 == 5`. Derivation: `src/data/locked_test.py:256`'s
`PURPOSES` gained a sixth member, `persistence_history`, when D-68's bounded
1-December lookup mechanism was built and wired on 2026-09-24
(`governance/CHANGE_RECORD_2026-09-24_d28_option_a_mechanism_built.md`); the
test still pinned the pre-D-68 count of 5.

**Repair applied by this stage** (Step 10 fix authority): the pin moved 5 → 6
with `persistence_history` asserted explicitly and D-68 cited in the test's
docstring. This aligns a stale pin with an **existing owner ruling** — no new
decision was made, and the pin still refuses any unruled widening of the
enum. Module re-run after the fix: **69/69 passed**. Lint on the edited file:
the only finding (`I001`, import sort) reproduces byte-for-byte on HEAD's
copy — pre-existing, not introduced.

Cross-unit disclosure (`project.md` `gf-3`): the edit touches `acquisition`'s
test module under that unit's frozen receipt; its `code-summary.md` is
correspondingly staler by one test amendment. Carried here and at the gate,
not silently patched into the receipted record.

## Failure 2 (NOT repairable here): three IGS site logs missing against a committed manifest

`tests/test_release_hashes.py::test_declared_artifact_matches_its_recorded_hash`
fails three times:

```
station_registry_sources_2026-09-19/aruc00arm_20260317.log is declared in
sha256_manifest.json but is absent from the tree. A manifest that names a
missing file cannot verify anything.
```

(and identically for `bshm00isr_20260422.log`, `nico00cyp_20251027.log`.)

Root cause, derived and verified rather than guessed:

- `git check-ignore -v` attributes each `.log` to **`.gitignore:3` — the
  generic `*.log` pattern** (a build-noise rule that predates the evidence
  layout).
- `evidence/station_registry_sources_2026-09-19/sha256_manifest.json` was
  committed 2026-09-20 (`4253d51`) naming the three site logs with their
  SHA-256 hashes; **no commit in history has ever carried the `.log` bytes**
  (`git log --all -- "evidence/station_registry_sources_2026-09-19/*.log"`
  is empty).
- Consequence: the files existed only as untracked bytes on the machine that
  wrote the manifest, and any fresh checkout — including this clone — fails
  TA-15's verification. The test is doing exactly its job; the defect is in
  evidence custody, not in the test or the hashing code.

**Why this stage did not fix it:** the bytes do not exist on this clone and
cannot be invented; the sources are public IGS site logs whose re-retrieval
is an acquisition act with provenance obligations (DATA-07's
version-suffix rule applies by analogy), and the recorded manifest hashes
give the exact verification criterion for any re-retrieved bytes.

**Proposed dispositions for the owner (decision required, not made here):**

1. Re-retrieve the three IGS site logs, verify each against its recorded
   SHA-256 in the manifest, commit them with a `.gitignore` negation
   (`!evidence/**/*.log`) so evidence logs are never swallowed by the
   build-noise pattern again. Verifiable and closes the failure honestly.
2. Amend the manifest to declare only the **two** declared JSON artifacts
   (`rinex_2022_001_listing.json`, `sitelog_index.json` — the directory's
   other two JSONs are the manifest itself and its meta sidecar, which a
   manifest cannot self-hash), moving `sha256_manifest_meta.json`'s
   `hash_count` 5→2 in the same amendment, and recording the site logs'
   absence as a limitation. Removes the failure but weakens the
   station-registry provenance chain — the site logs are what D-65's
   coordinates were validated against. *(Reworded 2026-09-24 under Rec 13:
   the earlier "four JSON artifacts" misdescribed the manifest's contents.)*
3. Leave failing as a standing red row until re-acquisition. Honest but
   leaves §18.3's "no failing critical test" unsatisfiable meanwhile.

## Remediation pass under the 2026-09-24 rulings (GOV-2026-09-24-BT-01)

The Student ruled on all sixteen board recommendations
(`governance/CHANGE_RECORD_2026-09-24_GOV-BT-01_rulings.md` is the full
record). Code changes executed under those rulings, beyond the artifact
corrections visible throughout this document:

| Ruling | Change | Verification |
|---|---|---|
| Rec 1 (never-again clause) | `.gitignore` gains `!evidence/**/*.log`; new control `tests/test_release_hashes.py::test_no_manifest_declared_file_is_gitignored` (no manifest-declared file may be gitignored — catches the class at authoring time) | probe file under `evidence/…` now shows as `??` in `git status`; control green |
| Rec 1 (retrieval) | **BLOCKED from this network** — `files.igs.org`, `igs.org`, `igs.bkg.bund.de`, `epncb.oma.be`, `epncb.eu`, `gnss-metadata.eu` all connect-timeout. Retrieval spec (URLs, SHA-256s, byte counts) stands complete in `sitelog_index.json`; commit deferred until the bytes exist | the three hash rows remain the only red tests |
| Rec 8 | `src/models/persistence.py:29–46` docstring rewritten to the D-68 state (owner-authorized cross-unit amendment) | prose matches `evidence/DECISIONS.md` D-68 and the wiring |
| Rec 9 | `read_persistence_history_lookup` Raises clause + `PERSISTENCE_HISTORY_DAY` comment corrected to the tested drop semantics | `test_ph_condition_i_*` green, unchanged |
| Rec 10 | `run_id` threaded caller→lookup→access row (`locked_test.py`, `scripts/06`, wiring + guard tests); empty/absent refuses | new `test_ph_run_id_is_caller_supplied_and_empty_refuses` green; wiring test asserts the threading |
| Rec 16 | `PURPOSES` leading comment now enumerates six members with the D-68 citation | comment matches the set |

Post-remediation module run (persisted as `rem1.xml`): `test_release_hashes`
+ `test_locked_test_guard` + `test_models_smoke` + `test_acquisition` —
**448 tests, 441 passed, 3 failed** (the site-log rows only), 4 skipped
*(corrected 2026-09-27: 448 − 3 − 4 = 441; the earlier "445" counted skips as
passes — `GOV-2026-09-27-BT-02` R14)*.

Cross-unit disclosure per `gf-3`: these edits touch modules owned by
`governance-guards` (`locked_test.py`, `test_locked_test_guard.py`),
`models-and-baselines` (`persistence.py`, `06_train_and_predict.py`,
`test_models_smoke.py`) and `foundation` (`test_release_hashes.py`) under
their frozen receipts; each unit's `code-summary.md` carries a dated
addendum naming this pass.

## Lint / format state (advisory)

`ruff check .` at `41fd109`: **63 findings**; `ruff format --check .` would
reformat **53 files**. Pre-existing tree-wide state, not introduced by this
stage (earlier sessions' "no new lint findings" claims were per-change
claims). A tree-wide ruff pass would edit governed test modules under frozen
receipts — an owner question, recorded in the stage diary's Open questions.

## What these results do and do not support

- They support: the rebuilt governed-interpreter environment runs the suite;
  1573/1582 green with every failure root-caused; the §18.3 critical set is
  green **except** the three evidence-custody rows above.
- They do not support: WS-20 / TA-17 (clean-run reproduction — stages 06/07
  and the scientific fixture have not run), TC-03g (no Kaggle-session run),
  any TF-dependent claim (TF absent), any plots-path claim (matplotlib
  absent), or G-05/G-06/G-07 evidence (supervisor gates, all open).

## Sources

- Upstream: per-unit `code-generation-plan.md` and `code-summary.md` under
  `<record>/construction/<unit>/code-generation/` (the twelve units named in
  `build-instructions.md` § Upstream inputs).
- junit XML files from this session's runs, **persisted** (Rec 6, option 1) at
  `artifacts/exec_evidence/run_2026-09-24_git-ae-srv/` — `full.xml` (1582/3F/6s),
  `crit.xml` (683/3F/3s), `acq.xml` (69/0F), `rem1.xml` (the post-remediation
  four-module run, 448/3F/4s) — beside `conda_list_export.txt` (the rebuilt
  environment's exact package set) and `requirements_sha256.txt`
  (`8e118c233dd3ceeed1952e70ca9d392e532b5ab3c27e6295a86c931173bad180`). The
  FIRST-pass row (1582/1572/4F/6s) has **no surviving XML** — its file was
  overwritten by the clean re-run before persistence was adopted; that row is
  prose-only evidence and is marked as such. `full_post.xml` (1584/3F/6s) is
  the post-remediation run and the artifact set's operative full-suite figure.
- `governance/PENDING_FOLLOWUPS.md` §1a (the 2026-09-24 766/766 critical run);
  `governance/CHANGE_RECORD_2026-09-24_d28_option_a_mechanism_built.md` (D-68).
- `.gitignore:3`; commit `4253d51`; `evidence/station_registry_sources_2026-09-19/`.

## 2026-09-25 remediation addendum (verified against current HEAD, not overwriting the rows above)

Executed under continued Student authorization (code/doc fixes, evidence
recovery, permitted fixture runs, targeted verification, local commits — no
locked-December access, no governance weakening, no scope change, no
push). Every count below is read programmatically from a fresh junit XML
persisted this session, never carried from prose.

**Site-log custody finding (Rec 1) — CLOSED.** The three IGS site logs
(`aruc00arm_20260317.log`, `bshm00isr_20260422.log`, `nico00cyp_20251027.log`)
are present on disk under `evidence/station_registry_sources_2026-09-19/`,
already committed (`db15880`, prior to this session), and their SHA-256
hashes were independently recomputed this session and match
`sitelog_index.json` exactly (all three, byte-for-byte). *(Custody-channel
disclosure added 2026-09-27, `GOV-2026-09-27-BT-02` R6: the recovery channel of
the `db15880` bytes — who retrieved or copied them, from where, and when — is
UNRECORDED; `db15880`'s commit message is editor boilerplate and no artifact
narrates the act. Their identity therefore rests on hash equality with the
2026-09-20 recorded manifests alone, which four independent 2026-09-27 board
seats re-verified. This is a stated limitation, not a defect in the hashes.)* The `.gitignore:10`
negation (`!evidence/**/*.log`) is in place and verified live —
`git check-ignore` reports no match for any of the three files.
`tests/test_release_hashes.py` (option 1's closing control):
**235/235 passed** (`crit.xml`'s predecessor confirms zero regressions
elsewhere). This closes option 1 of the three dispositions recorded above —
no manifest amendment or standing-red acceptance was needed.

**TF/matplotlib pin surface (readiness item 2) — CLOSED.** This clone's
network reaches `pypi.org` (200) and `files.igs.org` (302) this session,
unlike the prior blocked-network sessions. `pip show` in the governed
`tec-thesis-311` env confirms both previously-unobtainable pins are now
installed at the exact governed versions: `matplotlib==3.9.0`,
`tensorflow==2.21.0`. Combined with the seven pins already exact, the pin
surface is now **9 of 9 exact** (was 7/9). `src/evaluation/plots.py` and
`src/models/lstm.py`'s TF-present paths are now exercisable in this
environment; the TE §8.1 both-platform (Kaggle AND local) check for M-06
still needs its own dedicated exercise run, which this remediation pass did
not additionally perform.

**Full suite, fresh run (`run_2026-09-25_bt-remediation/full.xml`):**
**1584 total, 1580 passed, 0 failed, 0 errors, 4 skipped**, 424.5 s wall
time. Every field sums (1580+0+4=1584) — this resolves the readiness-item-2
count ambiguity in the summary's prior "1584 tests, 1581 passed, 3 failed, 6
skipped" line (which itself summed to 1590, not 1584, and predates this
session's fixes). The four skips, read from the XML's `<skipped>` messages,
not narrated: `test_clean_run.py::test_clean_run_completion_or_skip_with_named_reason`
(the scientific fixture manifest still carries the `TBD — freeze gate`
sentinel — Q-31 freeze owed, WS-20/TA-17 stay Pending, item 3 below),
`test_models_smoke.py::test_ridge_and_forest_refuse_by_name_when_sklearn_is_absent`
and `test_regimes_and_reporting.py::test_render_figure_refuses_naming_pin_surface_when_matplotlib_absent`
(both negative-absence controls now unreachable because the packages ARE
present — an artifact of the pin surface closing, not a weakened
assertion), and `test_release_contract.py::test_missing_required_field_is_refused[dataset_version]`
(a parametrized case whose field is derived, not user-supplied — pre-existing,
unrelated to this remediation).

**§18.3 critical-set, fresh run (`crit.xml`, the same ten-module selection
(b) recorded above):** **685 total, 685 passed, 0 failed, 0 errors, 0
skipped**, 55.8 s. §18.3's "no failing critical test" precondition is
satisfied for selection (b) as of this commit. Selections (a) and (c) are
unchanged by this addendum and remain the Student's to reconcile (Rec 5) —
this addendum verifies (b) only and does not resolve which of (a)/(b)/(c) is
"the" §18.3 run.

**Rec 47 (GitHub check) — investigated, NOT closed; local pass ≠ remote
pass.** With GitHub reachable this session, a read-only check (no push) via
the public Actions API confirms `.github/workflows/verify.yml` **is** pushed
and active on `github.com/Kimrza/Thesis_toshkari` (workflow id `339264561`,
49 runs) — the "committed but not pushed" note above is stale. Its most
recent run (`36139946731`, triggered by commit `29ed3119932410f18d5582f1ddb058c5b13262f7`,
i.e. two commits behind this session's HEAD) **FAILED** at the
"Release-hash verification" step — the exact site-log custody defect closed
above, but at a commit predating that fix (the fix landed in `db15880`,
after `29ed311`). No CI run exists yet against `db15880` or the current HEAD,
because neither has been pushed. Equating this session's local green run
with a GitHub check pass would be exactly the error this task warned
against; it is not made here. **Remaining external action:** push the
current HEAD (student's action, outside this session's authorization) so
`verify.yml` runs against the fixed commit and either confirms or reopens
the finding.

**`run_snapshots/` tracking policy — confirmed already applied, no drift.**
`artifacts/run_snapshots/` is tracked in git (696 files, 19 MB, small
per-run YAML config snapshots only — `data.yaml`, `experiment.yaml`,
`features.yaml`, `seeds.yaml` per run, no data/model bytes), not covered by
any `.gitignore` rule (`git check-ignore` confirms no match). This already
matches the requested policy (track small reproducibility records in git;
large outputs elsewhere) — Rec 11's disclosure-only disposition from
`GOV-2026-09-24-BT-01` stands as the last ruling on this; no further owner
decision or ignore-rule change is owed.

**Fixture stages 06/07 — still blocked, confirmed by inspection, not
executed.** `configs/experiment.yaml` still carries `folds: "TBD — freeze
gate"`, `models.selected: "TBD — freeze gate"`, and `models.lstm.epochs:
"TBD — freeze gate"`. `project.md` § Forbidden bars filling a
`TBD — freeze gate` value by convenience; both `05_build_features_and_splits.py`
and `06_train_and_predict.py` refuse on these fields by design. This is the
same blocker `run_walking_skeleton.py`'s module docstring already documents
for the scientific fixture. Stages 00–05's existing evidence on
`plumbing_7day` is untouched; nothing under this addendum ran, scored, or
otherwise touched locked-December data.

**Readiness items 4, 5, 7 — unchanged by this addendum.** Cross-unit
staleness (item 4) is not newly created by anything in this pass (no
`produces[]` artifact of another unit's frozen receipt was touched). The
`aidlc-state.md` Project Root field (item 5) has no sanctioned direct-write
path from this session (same constraint recorded 2026-08-22) and is left as
is; this session's actual root, `C:\Users\LOTUS\Desktop\Thesis_toshkari`, is
recorded here for the audit trail rather than hand-edited into the state
file. Item 7 (Rec 5's §18.3 selection reconciliation) is unchanged — routed
to the Student, not decided here.

Evidence for this addendum:
`artifacts/exec_evidence/run_2026-09-25_bt-remediation/full.xml`,
`.../crit.xml`; GitHub Actions API responses (`workflows`, `runs`, `jobs`
for run `36139946731`) read live, not persisted as files (no local
credential or token was used — the repository is public).

## 2026-09-25 item 6 (Rec 47 GitHub check) — CLOSED (CI-verification limb ONLY; scoped 2026-09-27)

*(Scope correction 2026-09-27, `GOV-2026-09-27-BT-02` R2: this heading's
unqualified "CLOSED" overstated a two-limb status. What closed is the
CI-verification limb — local pass equals remote pass at the fixed commit. The
CUSTODY limb remains OPEN: the workflow's authorizing Student + Supervisor
change record is still owed (the workflow's own bound annotation records it),
and every push until 2026-09-27 ran the restricted-reader modules on GitHub
runners with access rows destroyed with the runner. The restricted-reader
modules are deselected from `verify.yml` as of 2026-09-27; the consolidated
platform ruling is drafted at
`governance/CHANGE_RECORD_2026-09-27_platform_bound_RULING_REQUEST.md`.)*

Root cause found from Student-supplied full job logs (`.github/workflows/verify.yml` run
`36145238473`, commit `53f1c32`): two workflow-definition bugs, neither a code defect.

- **Ubuntu `exit code 141`:** `git ls-files --eol evidence | head -20` under the runner's
  default `bash -e -o pipefail` — `head` closes the pipe after 20 lines, `git ls-files` gets
  `SIGPIPE`, `pipefail` treats it as failure though the printed diagnostic output was already
  correct. Fixed: appended `|| true` to the pipeline (`.github/workflows/verify.yml`).
- **Windows `15 failed`:** all 15 failures were `ModuleNotFoundError: No module named 'yaml'`
  (or transitively caused by it). The "Install pytest only" step installed bare `pytest`,
  never `pyyaml` or `requirements.txt` — a CI environment gap, invisible locally because the
  governed `tec-thesis-311` env has `pyyaml==6.0.1` per the pin. Fixed: step renamed "Install
  governed dependencies", now runs `pip install --upgrade pip pytest -r requirements.txt`,
  installing the same governed pin surface (TE §13.1) used by every local run in this
  document.

**Pushed and verified.** Student pushed `7357f3504466dd883249eefd9a7064267997e7a3`. Runs
`36160927386` (ubuntu) and `36160926808` (windows) — both **`completed` / `success`**, every
step green including "Full tests/ directory" on both OSes, confirmed via the public Actions
API against this exact commit (not a stale one). Local pass now equals remote pass. Rec 47's
**CI-verification limb** is closed; its **custody limb** (the authorizing change record and
the locked-root materialisation/access-record question) remains open — see the 2026-09-27
scope correction at this section's heading.

## 2026-09-25 item 9 (new) — W-6 step 8: Kaggle durability measurement blocks all restricted-root reads on Kaggle

Discovered while attempting item 2's Kaggle-side pin verification (`kaggle/
kaggle_tf_matplotlib_pin_verification.ipynb`, revisions 1-3). Tracked here as its own
item, distinct from item 2, on the Student's explicit instruction — item 2 stays
blocked on this dependency, not reclassified or closed.

**Exact problem statement:** `CHARACTERISED_DURABILITY_PLATFORMS` (`src/data/config.py:482`)
is a hardcoded empty `frozenset()`. `open_restricted()` (`src/data/locked_test.py:497`)
refuses every call on any platform that is neither `"local"` nor in that set. Kaggle is
refused unconditionally. Confirmed this session: this blocks `test_release_hashes.py`
(at collection), and specific tests inside `test_common_masks.py` and
`test_locked_test_guard.py` (at runtime) — 16 test failures/errors total, all one root
cause.

**Root cause:** the measurement that's supposed to populate
`CHARACTERISED_DURABILITY_PLATFORMS` with `"kaggle"` — an in-Kaggle-session durability
confirmation, per `governance-guards` R-25's pattern — has never been performed.
Tracked as owed since 2026-08-28 (`GOV-2026-08-28-FD-01` Recommendation 39),
reconfirmed by `GOV-2026-09-20-CG-01` Recommendation 57, ruled to the Student "before
G-05" in that governance pass's dispositions (§5 item 10). Two further preconditions
block even attempting it: (a) `emit_in_session_gate_result` isn't wired into
`run_walking_skeleton.py` yet; (b) the scientific fixture can't run locally or on
Kaggle until item 3's Q-31 freeze lands.

**Current status:** open, owner-ruled, not yet actioned. Blocks: full item 2 closure
(Kaggle both-platform check), any freeze-gate reliance on Kaggle-written registry
rows, and — newly discovered this session — a wider slice of the §18.3 critical set on
Kaggle than previously documented (three modules, not one: `test_release_hashes.py`,
`test_common_masks.py`, `test_locked_test_guard.py`).

**Sources:** `governance/reviews/GOV-2026-09-20-CG-01.md` Recommendation 57;
`governance/CHANGE_RECORD_2026-09-20_GOV-CG-01_dispositions.md:120` (§5 item 10);
`aidlc/.../construction/foundation/functional-design/business-logic-model.md` § W-6,
§ Assumptions ("OPEN — Kaggle's durability semantics are characterised nowhere in this
design"); `aidlc/.../construction/foundation/code-generation/code-summary.md:123`;
`kaggle/HOW_TO_RUN_IN_SESSION_GATE.md` (the prepared, not-yet-run discharge runbook);
this session's `crit_kaggle_nine_of_ten.xml` and `test_release_hashes_kaggle.xml`
(2026-09-25).

**Correction 2026-09-27 (`GOV-2026-09-27-BT-02` R8): the two Kaggle junit files
named above were never persisted to the repository** — no such file exists in the
working tree, under `artifacts/exec_evidence/`, or in any commit
(`git log --all --diff-filter=A` on both names is empty, derived 2026-09-27).
Item 9's quantitative claims — "16 test failures/errors total, all one root
cause" and the three-module scope — are therefore **prose-only evidence**,
exactly the class the first-pass 1582/1572 row above is marked as, until the
counts are re-derived and persisted on the next Kaggle session. The finding's
qualitative substance (the empty `CHARACTERISED_DURABILITY_PLATFORMS` set
refusing every restricted-root read on Kaggle) is independently verifiable from
`src/data/config.py:482` and is not affected.

## 2026-09-27 re-baseline addendum (GOV-2026-09-27-BT-02 R1)

Executed under the Student's 2026-09-27 approval of all 29 board
recommendations (`governance/CHANGE_RECORD_2026-09-27_GOV-BT-02_remediation.md`
is the execution record). Every count below is derived programmatically at
HEAD `69b00c4` (2026-09-26) and printed with its derivation; nothing is carried
from prose.

**What changed between the artifact baseline `41fd109` and HEAD `69b00c4`:**
25 commits (`git log --oneline 41fd109..69b00c4 | wc -l` → 25). Materially:

- **Test modules: 34** (`Get-ChildItem tests -Filter "test_*.py"` → 34; the
  unit-test-instructions' 29-module inventory is the `41fd109` state). The five
  additions: `test_b01_prediction_adapter.py`, `test_fixture_run_fixes.py`,
  `test_gim_generation.py`, `test_gim_provenance.py`, `test_recorded_presence.py`.
- **Pin surface: 10 pins** (`requirements.txt` `==` lines → 10). The tenth,
  `ml_dtypes==0.5.3`, was owner-approved 2026-09-26 (commit `12843b5`); the
  addendum's "9 of 9 exact" above is the pre-`12843b5` state.
- **Fixture ladder: through stage 06 on `plumbing_7day`** (commit `7b4109b`;
  `artifacts/walking_skeleton/plumbing_7day/predictions/FIX-NOV-FOLD-01|02`
  exist with `registry_entry.json` stamped `evidence_class: smoke_only`). The
  "Fixture stages 06/07 — still blocked" inspection above was true at its
  2026-09-25 baseline and is superseded. Stage 07 has not run. WS-20/TA-17
  remain Pending (the Q-31 scientific-fixture MANIFEST freeze is still owed;
  the window is frozen as D-14).
- **Owner decisions D-72 through D-76 landed** (D-72 froze Q-15 = rule "C";
  D-73 fixed the overlap-audit result and December's separate access-gated
  status; D-74/D-75/D-76 are the 2026-09-26 fixture/pipeline rulings), and the
  governed release `artifacts/releases/gim_comparator_C-01_2022/` exists —
  produced inside this still-open stage and reviewed by the 2026-09-27 board
  (manifest complete per TE §13.3; parquet + sampled source hashes re-verified).

**Governed-host verification, executed 2026-09-27 on this clone (item 1 of the
execution record's § 7 checklist).** `tec-thesis-311` (CPython 3.11.16 exact),
`PYTHONHASHSEED=0`, measured at commit `70bb651` (the remediation patch,
applied and committed on the authoring clone, pulled here on top of `69b00c4`;
this clone's working tree carries one additional fix on top of `70bb651` —
see the bite-proof note below). Every count is read from the persisted junit's
own `<testsuite>` attributes, never from pytest's terminal summary, and
`passed` is derived as `total − failures − errors − skipped`:

| Run | Total | Passed | Failed | Errors | Skipped | Wall time | XML |
|---|---|---|---|---|---|---|---|
| Three new negative controls (individually) | 3 | 3 | 0 | 0 | 0 | 0.33+0.20+17.19 s | `ctrl_r3.xml`, `ctrl_r11.xml`, `ctrl_r23.xml` |
| `test_release_hashes.py` (R6 closing control) | 965 | 965 | 0 | 0 | 0 | 6.20 s | `release_hashes.xml` |
| §18.3 critical set, selection (b), ten modules | 1417 | 1417 | 0 | 0 | 0 | 62.37 s | `crit.xml` |
| Full suite (34 modules) | **2384** | **2380** | 0 | 0 | 4 | 728.75 s | `full.xml` |

All persisted under `artifacts/exec_evidence/run_2026-09-27_bt02/`.

**Every stale expectation this addendum's predecessor carried forward is
superseded, and superseded upward, not down** — the suite grew between
`db15880` and `70bb651`, it did not shrink: `test_release_hashes.py` was last
measured 235/235 (2026-09-25) and is now **965/965**; the §18.3 selection (b)
was last measured 685/685 (D-69, 2026-09-25) and is now **1417/1417**; the
full suite's prior operative figure (1584 total) is now **2384 total,
2380 passed, 0 failed, 0 errors, 4 skipped** — up from the "expect a higher
total; derive it, don't predict it" note this addendum previously carried.
Zero failures and zero errors across every run; no test was weakened, skipped,
`xfail`-ed, or deleted to reach this. The four skips, read individually from
the XML (never narrated):

1. `test_clean_run.py::test_clean_run_completion_or_skip_with_named_reason` —
   the scientific-fixture manifest still carries the `TBD — freeze gate`
   sentinel on 45+ fields (Q-31 freeze not yet performed); correct refusal,
   not a gap.
2. `test_models_smoke.py::test_ridge_and_forest_refuse_by_name_when_sklearn_is_absent`
   — scikit-learn IS installed in this governed env, so the absence-refusal
   path is not reachable here (environment-conditional by design).
3. `test_regimes_and_reporting.py::test_render_figure_refuses_naming_pin_surface_when_matplotlib_absent`
   — matplotlib IS installed here for the same reason; absence path
   untestable on this host.
4. `test_release_contract.py::test_missing_required_field_is_refused[dataset_version]`
   — `dataset_version` is derived by `write_release`, not a required input
   field; see the D-29 tests.

None of the four skips touch `evidence/locked_test_restricted/` or December
2022 content — this remediation session read no locked-test byte.

**R6 independently reconfirmed** (beyond the passing test): the three IGS
site-log SHA-256 hashes were recomputed by this session directly from the
committed bytes (`hashlib.sha256`, not the test harness) and matched
`sitelog_index.json` exactly for all three files; `git check-ignore -v` on
all three returned exit 1 (no match — none is gitignored).

**`ruff check` on the eight edited files, baselined against `69b00c4`
(pre-patch; all eight files existed there and were clean — `ruff check` on
that copy returns "All checks passed!").** The current tree introduces **6
new advisory findings across 2 of the 8 files** (no enforced floor, Q5=A;
reported, not fixed, since none is a correctness or security-relevant miss
introduced by this remediation's own logic — S603/S607/S105 pre-date this
patch's actual new lines in `gim.py` and are pattern matches on
already-existing `subprocess`/token-constant code the patch's diff did not
touch the shape of):

- `tests/test_determinism.py:71` — `I001` import block un-sorted (new).
- `tests/test_external_drivers.py:1044,1056` — `UP038` `isinstance` tuple
  style (new; 2 occurrences).
- `src/external/gim.py:450,450,1075` — `S603`/`S607`/`S105` (new; the
  subprocess-call and token-naming patterns the R23 edit's surrounding
  function already contained).
- The other 5 edited files (`src/data/config.py`,
  `tests/test_iri_denial.py`, `tests/test_gim_generation.py`,
  `tests/test_gim_provenance.py`, `tests/test_locked_test_guard.py`)
  introduce **zero** new findings.

**Bite-proof (execution record's "CONTROL BITES" idiom), each guard
temporarily reverted then restored, working tree confirmed byte-identical
afterward (`git diff --stat`):**

- **R3**: removed the `_CI_MARKERS` refusal branch in
  `resolve_platform_roots` → `test_ci_runner_markers_are_refused_not_defaulted`
  failed (`DID NOT RAISE PlatformError`). Restored; passes again.
- **R11**: narrowing the name limb to `startswith("iri_")` alone did **not**
  fail the control on the first attempt — a genuine defect in the control,
  not a false alarm: its fabricated provenance string was
  `"fabricated non-IRI stamp"`, whose lowercased form contains the literal
  substring `"non-iri"`, which itself contains `"iri"`, so the predicate's
  separate provenance-content check caught the row regardless of what the
  name limb did, masking whether the name limb was exercised at all. Fixed
  by changing the test's fabricated provenance string to
  `"fabricated clean stamp"` (no `"iri"` substring), which isolates the
  name-limb behaviour; re-run with the limb narrowed then correctly failed
  (`assert [] `, empty violations list). Restored the wide limb; passes
  again with the corrected string. This is a test-data fix, not a guard or
  assertion weakening — `git diff` against `70bb651` on
  `tests/test_iri_denial.py` is exactly this one-string change plus its
  docstring note.
- **R23**: removed the December-2022 refusal clause in `generate_comparator`
  → the control's assertion (`"December 2022" in combined`) correctly
  failed — execution proceeded past the missing clause into a later,
  unrelated grid-interpolation-range refusal with a different message,
  confirming the assertion depends specifically on the December clause, not
  on the subprocess merely exiting non-zero. Restored; passes again.

**Commit-msg hook (R7, Step 5), exercised directly against three temp
messages with `core.hooksPath=.githooks`:** boilerplate editor text → exit 1;
empty message → exit 1; a real message → exit 0. Matches the execution
record's claim.

**R5 (lost `GOV-2026-09-24-BT-01` report) — SUPERSEDED, correcting this
addendum's own earlier statement.** At the time this section was first
written (2026-09-27, commit `4501749`), a machine-wide search on this clone
found nothing, and that was reported as the state. It is no longer the
state: a **different** clone (`GIT-AE-SRV-RDT1`, the one the board actually
ran on — the earlier "LOTUS clone" attribution in the superseded limitation
record was itself wrong, corrected below) recovered the verbatim report text
from its own session transcript and pushed it; this clone fast-forwarded
`main` from `4501749` to `c7b174d` to pick it up (no local commits were
ahead, so the fast-forward was lossless — `git merge --ff-only`, zero
conflicts). Independently re-verified here, this session, before trusting
it: `governance/reviews/GOV-2026-09-24-BT-01.md` carries exactly **16**
`### Recommendation` blocks (`grep -c`), severity **Critical 1 / High 7 /
Medium 7 / Low 1** stated in its own header and matching the stage diary's
2026-09-24T22:10Z entry, review mode **ADAPTIVE** (not "full-board" as the
now-superseded limitation record had assumed), and host
**`GIT-AE-SRV-RDT1`** (not LOTUS). This is recovery of an authentic
transcript artifact, not reconstruction from the citing artifacts — the
`delivery-planning:c12` refusal this addendum invoked never applied to a
genuine recovery and stays intact as project practice for the case it
actually governs. R5 is **CLOSED**; `CHANGE_RECORD_2026-09-27_GOV-BT-01_report_loss.md`
already carries its own supersession header and correction section, and the
execution record's § 1 table already reflects CLOSED — this addendum's prior
"still absent everywhere" sentence was the one artifact left uncorrected,
fixed here rather than left standing as a second, contradicting claim.

**R7 (commit attribution):** no session record or change record was found on
this clone beyond what the execution record's § 3 table already cites; the
three attributions for `576046c`, `0ce2a68`, `69b00c4` remain marked
**inferred**, unchanged, owed to the Student's confirmation at the gate.

## 2026-09-29 re-baseline addendum (HEAD `9710daf`)

This addendum adds to the rows above; it does not overwrite them. It was written
on the LOTUS clone on the owner's "Refresh, then review" instruction. Every count
is read from the persisted junit `<testsuite>` attributes, and `passed` is
derived as `total − failures − errors − skipped`.

**What changed between `70bb651` and `9710daf`.** Ten commits
(`git log --oneline 70bb651..HEAD` → 10). Materially:

- **Test modules: 39.** `git ls-tree` set difference against `70bb651` gives
  **+5 / −0**: `test_bootstrap_fixture_gate.py`,
  `test_budget_artifact_envelope.py`, `test_fixture_outputs.py`,
  `test_gim_comparison_set_fixture_gate.py`,
  `test_reporting_surface_fixture_gate.py`.
- **Pins: 10**, unchanged (`requirements.txt` `==` lines, excluding one comment
  line).
- **Decisions:** D-77 (IRI name-filter widening) and D-78…D-81 (estimand,
  bootstrap, comparison sets, regimes) are adopted in `evidence/DECISIONS.md`,
  and D-74 carries its 2026-09-29 amendment (`bootstrap_summary.json` on
  `plumbing_7day` is exact/schema; candidate-versus-frozen tolerance rule).
- **Fixture ladder:** stages 00–07 run on `plumbing_7day`. The candidate
  manifest
  `tests/fixtures/plumbing_7day/fixture_manifest.candidate_walking-skeleton-plumbing_7day-20260929T133720Z-4a959333.yaml`
  is VALID over two real measuring runs (`CR-2026-09-29-Q31-CLOSURE`). It is a
  **candidate, not frozen**: the positive acceptance tolerance is the Student's
  Q-31 freeze act. The `scientific_1month` manifest freeze is still owed, so
  WS-20 and TA-17 remain **Pending**.

**First pass: 4 failures, all one timing defect in a test fixture.**
Governed env `tec-thesis-311`, CPython 3.11.16, `PYTHONHASHSEED=0`, persisted
under `artifacts/exec_evidence/run_2026-09-29_bt/`:

| Run | Total | Passed | Failed | Errors | Skipped | XML |
|---|---|---|---|---|---|---|
| §18.3 selection (b), ten modules | 1423 | 1421 | 2 | 0 | 0 | `crit.xml` |
| Full suite, 39 modules | 2456 | 2450 | 2 | 0 | 4 | `full.xml` |

All four failures were in `tests/test_common_masks.py`, and all were R-109
limb 1 refusals ("receipt timestamp … does not precede the metric call").
Each run failed on a **different** pair of tests. Root cause: the helper
`_receipted_prediction` stamped the receipt with `datetime.now()`, and
`require_locked_receipt` read `now()` again. On Windows both reads returned the
same microsecond, so the guard's strict `<` refused. The guard behaved
correctly and failed closed. The defect was in the test data.

**A related defect found while diagnosing.** Seven negative controls used a bare
`pytest.raises(LockedTestError)`. When the clock collided, a limb 2 or limb 3
control could pass because limb 1 raised first, without ever exercising the
limb it exists to prove.

**Repair (owner ruling Option A, 2026-09-29; test-only).** This is a cross-unit
edit to `evaluation-and-comparison`'s READY module, made per
`code-generation:c32`. The helper now backdates the receipt by 1 s, and each of
the seven controls now matches its own limb's message. `src/evaluation/guards.py`
is **unchanged**. `test_common_masks.py` changes by +12/−8 lines.

- **Stability:** the module passed 82/82 on five consecutive runs.
- **Bite-proof:** a temporary copy was run with the receipt forced two hours
  into the future. Exactly the five limb 2 and limb 3 controls **FAILED**,
  proving their message checks now bite. The three limb 1 controls (18, 19/21,
  20) passed, as they must. The copy was deleted afterwards.

**Post-repair runs** (`artifacts/exec_evidence/run_2026-09-29_bt_fix/`):

| Run | Total | Passed | Failed | Errors | Skipped | Wall time | XML |
|---|---|---|---|---|---|---|---|
| §18.3 selection (b), ten modules | **1423** | **1423** | 0 | 0 | 0 | 105.8 s | `crit.xml` |
| Full suite, 39 modules | **2456** | **2452** | 0 | 0 | 4 | 660.7 s | `full.xml` |

The four skips are the same four named in the 2026-09-27 addendum, re-read
from the XML: `test_clean_run_completion_or_skip_with_named_reason` (Q-31
scientific-fixture freeze owed), the sklearn-absent and matplotlib-absent
refusal paths (packages present), and `test_missing_required_field_is_refused[dataset_version]`.
§18.3's "no failing critical test" condition holds for selection (b) at
`9710daf` plus this test edit, which is not yet committed.

**Tree state.** The runs mutated no tracked file apart from the AI-DLC audit
shard. The stage's own edits are `tests/test_common_masks.py`, this addendum,
the summary addendum and the stage diary, all uncommitted. There are 131
untracked `artifacts/run_snapshots/*` directories and the
`*.archived-*` fixture outputs, which predate this session; they are left for
the owner.

**Carried to the gate under `gf-3`:** `evaluation-and-comparison`'s
`code-summary.md` is now out of date for this test edit, which is disclosed
here rather than written into that unit's receipted record.

### 2026-09-29 corrections under `GOV-2026-09-29-BT-03` (the Student's rulings)

This block records what the board's findings changed. The paragraphs above
stand as written, and this block supersedes them where the two conflict.

- **Rec 4: the clean-run skip reason, corrected.** The paragraph above
  attributed the `test_clean_run_completion_or_skip_with_named_reason` skip to
  the "Q-31 scientific-fixture freeze owed". That was wrong. The skip message
  in `run_2026-09-29_bt_fix/full.xml` names
  `tests/fixtures/plumbing_7day/fixture_manifest.yaml` as the first unmet
  precondition: that file is still the Recommendation 37 structural skeleton
  and carries the `TBD — freeze gate` sentinel on 46 fields. The first owed
  act is therefore **to promote the VALID `plumbing_7day` candidate into
  `fixture_manifest.yaml`, then the Student's Q-31 freeze**. The
  `scientific_1month` freeze comes after that. WS-20 and TA-17 stay Pending
  until all three are done.
- **Rec 5: the snapshot count, corrected.** The "Tree state" paragraph said
  "131 untracked `artifacts/run_snapshots/*` directories … which predate this
  session". Derived by `git status --porcelain | grep -c '^?? artifacts/run_snapshots/'`,
  the count is **133**. Two of them were created by this stage's own suite
  runs, because `load_configs` writes one snapshot per call:
  `20260929T141802Z-69e1cbb7` (the first pass) and
  `20260929T144927Z-f0912344` (the post-fix pass). The other 131 predate
  this session.
- **Rec 6: untracked release outputs, disclosed.** Seven untracked release
  directories exist under `artifacts/walking_skeleton/plumbing_7day/releases/`:
  six `plumbing_7day_20260929T{080230,080848,082445,085704,093502,101603}Z/`
  and `gim_comparator_C-01_2022.archived-q31-closure-run1/`. There are also
  97 untracked `*.archived-*` paths. None of them is recoverable from version
  control, so TA-15 protects their bytes only while this disk survives. The
  tracking policy for snapshots, archives and releases (`CR-2026-09-19` gate-prep-2,
  item 6) is still **undecided**. It is routed to the Student as a separate
  ruling in `governance/CHANGE_RECORD_2026-09-29_GOV-BT-03_rulings.md`.
- **Rec 7: boundary control added.**
  `test_control_20b_receipt_at_the_same_instant_as_the_call_raises` passes
  `now` equal to the receipt's own timestamp and expects the "does not
  precede" refusal. Bite-proof: with `guards.py:537` temporarily relaxed from
  `<` to `<=`, 20b **FAILED** while control 20 still passed. The guard was
  restored and `git diff -- src/` is empty.
- **Rec 9: the `gf-3` disclosure, widened.** `evaluation-and-comparison`'s
  `code-summary.md` (last committed in `7357f35`) is out of date for three
  changes to modules that unit owns, not one:
  - `208f138` changed `src/evaluation/masks.py`: `source_id` moved from
    `_IDENTITY_KEYS` to `_PROVENANCE_KEYS`, with no decision record yet (Rec 1).
  - `9710daf` changed `masks.py` and `src/evaluation/plots.py` (`render_series_figure`).
  - This stage changed `tests/test_common_masks.py`.
- **Rec 11:** the orphan bytecode
  `tests/__pycache__/test_zz_bite_common_masks.cpython-311-pytest-8.2.2.pyc`
  has been deleted. It was gitignored, and pytest never collected it.
- **Rec 13: the sidecar is anchored.** The access sidecar
  `artifacts/exec_evidence/test_access_log.jsonl` is gitignored by design, so
  the closed log stays closed. Its SHA-256 at the time this block was
  written is recorded in the commit-anchored re-run below (Rec 3).
- **Rec 15: a target-lineage string guard was added.**
  `tests/test_prepared_target_schema.py` gains
  `test_target_definition_id_is_byte_identical_everywhere_it_is_declared`. It
  reads the value from `configs/data.yaml` and never restates it, and it
  compares every declaration in `configs/experiment.yaml` and the fixture
  identity declarations and manifests against that value, case included. It
  also gains a case-variant negative control. Bite-proof: `configs/experiment.yaml`
  was temporarily retyped to `GRIDDED_VTEC_1H`, the test **FAILED** naming
  the file, and the file was restored with `git checkout` (`git diff -- configs/`
  is empty).
- **Rec 16: the §12 mandated set, enumerated.** The mandated modules were
  extracted from TE §12 (lines 610–745) by regular expression and give
  **21**. Set-differenced against `git ls-files tests`: **18 present, 3
  absent**. The absent three, `test_dcb_sign.py`, `test_hourly_target.py`
  and `test_rinex_schema.py`, are all Phase 2-only (TE §7.0), so their
  absence is correct. The phase-transition hash-diff limb is carried by
  `tests/test_phase_contract.py:513`
  (`test_identical_manifests_diff_empty_and_training_is_permitted`) and
  `:522` (`test_a_differing_hash_is_named_and_training_is_refused`).

### 2026-09-29 post-commit re-run at `391a319` (GOV-2026-09-29-BT-03 Rec 3, step 2)

The evidence is now tied to a commit. Every Recommendation 1–17 edit, plus D-82, is
committed in `391a319`. The re-run executed on a clean tree at that HEAD: `git rev-parse HEAD`
returned `391a3191dd2555bf76eb13ee74aa18250d110cda` before the run. Environment: `tec-thesis-311`,
CPython 3.11.16, `PYTHONHASHSEED=0`. Counts are read from the junit `<testsuite>` attributes:

| Run | Total | Passed | Failed | Errors | Skipped | Wall time | XML |
|---|---|---|---|---|---|---|---|
| §18.3 selection (b), ten modules | **1426** | **1426** | 0 | 0 | 0 | 62.5 s | `run_2026-09-29_bt_391a319/crit.xml` |
| Full suite, 39 modules | **2459** | **2455** | 0 | 0 | 4 | 1007.7 s | `run_2026-09-29_bt_391a319/full.xml` |

The previous run had 1423 critical-set tests and 2456 in the full suite. The **+3** is the
three tests this pass added:

- control 20b in `test_common_masks.py`;
- the target-id sweep in `test_prepared_target_schema.py`;
- the case-variant control, also in `test_prepared_target_schema.py`.

The four skips are unchanged. The full-suite wall time of 1007.7 s is longer than the
660.7 s measured before. This host was running other work at the same time, so this
figure reflects machine load and is not a new runtime envelope.

The test-mode access sidecar `artifacts/exec_evidence/test_access_log.jsonl` has SHA-256
`fc03d6f393b82b40de344a583d072739926e4fd6027c4525fee1043d8d825849` after this run
(Rec 13). The closed log `evidence/test_run_access_log.jsonl` is unchanged. The only
file this run changed is the AI-DLC audit shard.
