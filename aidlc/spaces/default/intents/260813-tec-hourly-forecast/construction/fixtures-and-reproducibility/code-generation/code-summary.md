# Code Summary — fixtures-and-reproducibility (code-generation)

**Unit:** fixtures-and-reproducibility (Bolt 12)
**Stage:** code-generation (3.5)
**Plan:** `code-generation-plan.md` (approved 2026-09-07; Q1–Q6 = A)
**Sessions:** generation began 2026-09-07 (interrupted after Steps 1–5 and 7); resumed and completed 2026-09-09.

## Files created

| File | Plan step | Purpose |
|---|---|---|
| `governance/CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md` | 1 | Change record FIRST; §11 updated 2026-09-09 with the resume pass's actual Step 6/8/9 outcomes |
| `src/data/fixture_manifest.py` | 2 | F1 manifest schema + the single loader (`load_fixture_scope`, `IdentityDeclaration`); F2 read side; R-133/134/135/137 and R-139 declaration side |
| `src/data/fixture_gate.py` | 3 | F4 + F6: append-safe registry receipts with SD-X-02 Rec 7 tamper binding, in-session gate (`require_in_session_gate`), R-140/R-141 |
| `src/data/fixture_evidence.py` | 4 | F7 evidence emitters (three refusing emitters; D-number agreement checks with sidecar fallback); W-9, R-142, SD-X-01 step 3, SD-X-03 |
| `scripts/run_walking_skeleton.py` | 5 | F3 orchestrator: `--fixture plumbing_7day` / `--fixture scientific_1month`, §13.2-conformant sequencing; W-3/W-4/W-5/W-7 |
| `tests/fixtures/plumbing_7day/`, `tests/fixtures/scientific_1month/` | 7 | Fixture trees with `.gitkeep` + spec-conformant `README.md`; **no `fixture_manifest.yaml` anywhere** — BLK-02 held, no manifest authored by hand |
| `tests/test_clean_run.py` | 8 | §12 mandated module: 49 test functions (count derived and printed by its own final test) hosting the 39 negative controls, 11 must-not-fire controls, per-area §15.2 enumeration, project-wide AST only-copy scan, §13.2 fence parse (membership AND order, flags verbatim, ruled scope argument recognised), and the skip-with-named-reason completion test |

## Files modified (Step 6 — sibling additive edits, Q4=A / Q5=A, each flagged for its owner)

- `scripts/00_acquire_prepared_vtec.py` (owner: acquisition), `01_inventory_and_registry.py` (inventory-and-registry), `02_standardize_prepared_target.py` (target-standardization), `04_build_external_products.py` (external-products): `--fixture-manifest` option, `_stage_entry(..., fixture_manifest=None)` kwarg, one `require_receipts_for_snapshot(...)` call after `assert_lock_complete`.
- `scripts/05_build_features_and_splits.py` (features-and-splits), `06_train_and_predict.py` (models-and-baselines), `07_evaluate_and_report.py` (evaluation-and-comparison): the same three touches plus one early-return in `_run` reaching an additive `_run_fixture_scale` — apparatus partitions from the validated scope (never a frozen id), fixture stamps (`apparatus_partition_id`, `smoke_only`/caveat freight) on every output (embedded payload stamps on 06's predictions; sibling stamp files on 05's bundles and 07's metrics artifacts), apparatus split manifest on 05, no locked path reachable on 06/07, and a parser error for `--fixture-manifest` combined with a frozen `--partition`.
- `scripts/03_verify_processing.py` (owner: target-standardization) — **beyond the plan's seven, recorded in change record §11 for the owner to confirm or reverse**: its `_load_tolerance` carried its own `yaml.safe_load` of a fixture manifest — the second parser R-133 control 4 refuses, predating this unit. Rerouted through `load_fixture_scope`; behaviour strictly narrows (an invalid manifest now refuses at the loader). Without this the mandated project-wide only-copy scan fails on day one.
- `src/data/acquisition.py` (owner: acquisition) — one additive public predicate, `assert_records_within_window`, consumed by `scripts/run_walking_skeleton.py` and `tests/test_clean_run.py` (change record §5, §11). Made in the 2026-09-07 session; omitted from this table's first version and added per reviewer finding 2.
- The seven owners' READY code-summaries go stale under their receipts (tabulated in change record §5); staleness carried to the stage gate.

## Key implementation decisions

- **BLK-02 held throughout**: the apparatus is built; no fixture manifest exists on disk and no measuring run can complete before the `TBD — freeze gate` fields and TensorFlow pin freeze. The two Q-31 freeze acts remain owner acts.
- **BLK-08 mechanism limb** stays a checked refusal (R-139 control 25, TECU/inverse-route refusal in the comparison ledger) — D-27 unreopened.
- **Guard-boundary shape (nfr-design c58/c59)**: `load_fixture_scope` is the single manifest-loading guard home; every public entry point (the seven stage scripts + orchestrator) carries a negative control pushing a violating input through that entry point.
- **Step 10 gated stop is the terminal state for the agent**: the agent made no commit and may not. The repository fact, however (reviewer finding 1, verified by `git log`): owner commit `64c0551` (2026-09-07 12:21 +0400) already carries the Step 1–5/7 outputs, the `acquisition.py` edit and the change record's first version, with an unedited git template message and **no D-number cited** — violating `team.md`'s hard linking rule; the seventh template-message owner commit in the standing pattern (6246907, ec8eacf, 06207c4, da6cb7b, c7e7a05). The resume-pass outputs (Step 6 sibling edits, `tests/test_clean_run.py`, plan ticks, this summary) remain uncommitted. The owed citations — D-11, D-14, D-20, D-28, D-29, D-31 plus `CR-2026-09-07-R133-FIXTURES-AND-REPRODUCIBILITY` — now attach to an amend-or-follow-up decision that is the student's, routed to the stage gate.

## Test results

Environment: uv-managed CPython 3.11.16 in the session scratchpad + a stdlib pytest stand-in; PyPI unreachable (`pyyaml`/`pytest`/`ruff` absent). **Smoke evidence only, session-of-generation only, never governed.**

- `tests/test_clean_run.py`: **46 passed, 0 failed, 3 skipped** — skips all by name: two pyyaml-gated production-loader paths (`require_fixture_receipts` full path incl. the Q5 exemption; control 32's frozen-hash staleness) and the clean-run completion test skipping with the §18.3 stop-and-report reason. It fails (never passes) on a non-zero exit when preconditions hold. WS-20/TA-09/TA-17/TA-21 stay `Pending`.
- Ten named regression modules + test_clean_run: **436 passed, 0 failed, 13 skipped, 0 errors**.
- One self-introduced regression fixed same pass: `test_models_smoke`'s source assertion tripped by the new fixture path; local renamed to `fixture_target`.
- Pre-existing failures reproduced identically on the stashed, unmodified tree (git stash round-trip): `test_external_drivers` 11, `test_iri_denial` 1, `test_locked_test_guard` 1, 4 import-error modules — not caused by this pass.
- `compileall` clean over `scripts/`, `src/`, `tests/`.

## Deviations from the plan

1. `03_verify_processing.py` reroute (above) — owner-reversible, change-record §11.
2. Two controls + the exported-check full path are pyyaml-gated skips; substance exercised at stdlib level through `verify_receipt`/`write_fixture_pass_receipt`/`require_in_session_gate` (controls 26–31 real). Full runs owed to a governed environment.
3. `graphify update .` not run — CLI absent on this clone; owed with `ruff`.
4. 47 over-99-column lines remain in the four 2026-09-07 files (plus one pre-existing in `01`); every line added by the resume pass conforms; real `ruff` owed.

## Routed to the stage gate

Amendment ledger +1 → 8 across 6 owed (`component-methods.md`); the seven sibling edits + stale code-summaries plus the 03 reroute (owner ruling requested); §15.2 REQ-ENG-4 13→12 correction owed in `requirements.md`; the FR-WS-2/FR-WS-3 candidate §15.2 rows and M10 §13.2 placement proposals (change record §§8–9); the two Q-31 freeze acts; BLK-02 open, BLK-08 mechanism limb open; WS-20/TA-09/TA-17/TA-21 `Pending`; TA-03/TA-26 unproducible off Kaggle; TA-15 not covered (foundation's); the stale `team.md` § Walking Skeleton "remains open under Q-31" line (practices-gate-owned); the 47 over-99 lines + owed `ruff`/`graphify` runs; and the commit disposition: owner commit `64c0551` exists with a template message and no D-number (the standing pattern's seventh instance) — the student's ruling is owed on amending it to cite D-11, D-14, D-20, D-28, D-29, D-31 + `CR-2026-09-07-R133-FIXTURES-AND-REPRODUCIBILITY`, or letting it stand with a recorded reason, before the still-uncommitted resume-pass outputs land on top. The agent made no commit.

## Review

**Iteration:** 1
**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-09T16:48:23Z

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | code-summary.md, "Key implementation decisions" / "Routed to the stage gate" | The artifact's central governance claim — "Step 10 gated stop is the terminal state: no commit made" / "No governed commit was made and none may be before the student acts" — is false as of the artifact's own stated completion date (2026-09-09). `git log --oneline -- src/data/fixture_manifest.py src/data/fixture_gate.py src/data/fixture_evidence.py scripts/run_walking_skeleton.py` shows commit `64c0551` (2026-09-07) already contains exactly the Step 1–5/7 artifacts this stage produced (`fixture_manifest.py`, `fixture_gate.py`, `fixture_evidence.py`, `run_walking_skeleton.py`, both fixture-tree READMEs, the change record, and an additive edit to `src/data/acquisition.py`). `git status --short` confirms these four `src/data`/`scripts` files carry zero uncommitted changes — they are already on `main`. The commit message is the unedited git default placeholder text ("Please enter the commit message for your changes...") and cites no D-number, directly violating `team.md` § Way of Working: "Any commit that changes a scientific constant, a config value..., or another governed artifact must cite its D-number in the commit message." The same false claim is echoed in `governance/CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md:244` ("No commit is made here. The student commits, citing D-11, D-14, D-20, D-28, D-29, D-31"). Whether or not the agent itself ran `git commit`, the PRIMARY artifact asserts a repository state that a single `git log` call disproves, and the governed-artifact commit-message discipline the team mandated was not honoured on the commit that exists. | Correct the claim in code-summary.md and the change record to reflect that commit `64c0551` already exists without a D-number citation; either have the student amend that commit's message to cite the relevant D-numbers (D-11, D-14, D-20, D-28, D-29, D-31 per the artifact's own list) before any further work lands on top of it, or explicitly record the gap and route it to the gate as a correction rather than asserting "no commit was made." |
| 2 | Major | code-summary.md "Files modified (Step 6...)" table | The Files-modified table omits `src/data/acquisition.py` entirely, even though the commit that already exists on disk (`64c0551`) and the change record (`governance/CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md` §5, §11) both show this stage added one public predicate there (`assert_records_within_window`), consumed by `run_walking_skeleton.py` and `tests/test_clean_run.py`. `project.md`'s own affirmed corrections mandate deriving the full list of a fact's representations and sweeping every one; the code-summary's own Files-modified table is a representation of "what this stage touched" and it under-reports by one file. The change record discloses it (mitigating this to Major rather than Critical), but the PRIMARY artifact a reader consults first does not. | Add `src/data/acquisition.py` (`assert_records_within_window`) to the Files-modified table with its owner flag, consistent with the other seven sibling edits. |
| 3 | Minor | code-summary.md, "Test results" section | The claimed "39 negative controls, 11 must-not-fire controls" hosted in `tests/test_clean_run.py` is carried from `business-rules.md`'s § Negative-control count rather than derived and printed from the test file itself, contrary to `project.md`'s mandated practice ("ALWAYS derive a count programmatically from the artifact and print it before asserting it"). Grepping the test file for literal control-number citations turns up only 6 distinct numbers (1, 4, 17, 18, 19, 22) against the claimed 39 — this does not prove the other 33 controls are untested (business-rules.md's numbering scheme doesn't require every test to cite its number inline), but the code-summary does not itself demonstrate the 39/11 figures against the file, only the 49-test-function and pass/fail counts (which were independently verified by re-running the suite and do match: 46 passed, 0 failed, 3 skipped). | Add a derived-and-printed count of negative-control and must-not-fire assertions (e.g., a meta-test enumerating `pytest.raises` sites against `business-rules.md`'s (1)-(39) list) alongside the existing `test_function_count_derived_and_printed` check, so the 39/11 claim is machine-checked rather than carried. |

Independently verified and NOT flagged: `load_fixture_scope` is confirmed the single manifest-loading guard home (a repo-wide grep for `safe_load`/`fixture_manifest.yaml` over `src/`, `scripts/` finds no second production parse of a `fixture_manifest.yaml`; the pre-existing second parse in `scripts/03_verify_processing.py` was rerouted through `load_fixture_scope` as claimed and is disclosed as a beyond-plan deviation). `tests/test_clean_run.py`'s completion test (`test_clean_run_completion_or_skip_with_named_reason`) does skip-with-named-reason and fails (never passes) on a non-zero subprocess exit, as claimed. Re-running the suite in the session's uv-managed CPython 3.11.16 reproduced the claimed numbers exactly: `test_clean_run` 46 passed/0 failed/3 skipped; `test_iri_denial` 1 failure reproduced (pre-existing, unrelated to this pass). No `fixture_manifest.yaml` exists anywhere in the repo (BLK-02 holds) and `configs/experiment.yaml`'s `embargo_hours`/`folds` remain the literal `TBD — freeze gate` sentinel (no convenience-fill of a frozen value). `scripts/06_train_and_predict.py`'s parser-error-on-`--fixture-manifest`-plus-frozen-`--partition` and its routing through `load_fixture_scope`/`_run_fixture_scale` were confirmed by direct inspection.

### Suggestions (non-blocking)

- Finding 3's meta-test would also let a future reviewer verify the 39/11 figures without manually reconciling `business-rules.md` prose against the test file's control-number citations.
