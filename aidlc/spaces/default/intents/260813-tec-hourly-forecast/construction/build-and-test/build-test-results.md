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
| Full suite, POST-remediation (after the `GOV-2026-09-24-BT-01` ruling execution — two new controls collected; persisted as `full_post.xml`) | **1584** | **1581** | **3** | 0 | 6 | 138.5 s |

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
766-test selection spans all 29 modules while (b) is the ten §18.3 module
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
**448 tests, 445 passed, 3 failed** (the site-log rows only), 4 skipped.

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
`sitelog_index.json` exactly (all three, byte-for-byte). The `.gitignore:10`
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

## 2026-09-25 item 6 (Rec 47 GitHub check) — CLOSED

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
API against this exact commit (not a stale one). Local pass now equals remote pass. Rec 47
is closed.

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
