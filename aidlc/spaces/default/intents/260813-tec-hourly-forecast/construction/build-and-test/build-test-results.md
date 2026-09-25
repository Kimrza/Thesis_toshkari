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
