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
| `tests/test_clean_run.py` | 8 | §12 mandated module: 50 test functions (count derived from source and printed by its own final test) hosting the 39 negative controls and 11 must-not-fire controls — both figures machine-checked by `test_control_counts_derived_from_business_rules_not_carried`, which parses `business-rules.md`'s enumeration and set-differences it against the file's `CONTROL_HOSTS`/`MUST_NOT_FIRE_HOSTS` ledger (empty in both directions; `R-137:mnf1` hosted in `tests/test_train_only_transforms.py`, presence-asserted) — plus the per-area §15.2 enumeration, project-wide AST only-copy scan, §13.2 fence parse (membership AND order, flags verbatim, ruled scope argument recognised), and the skip-with-named-reason completion test |

## Files modified (Step 6 — sibling additive edits, Q4=A / Q5=A, each flagged for its owner)

- `scripts/00_acquire_prepared_vtec.py` (owner: acquisition), `01_inventory_and_registry.py` (inventory-and-registry), `02_standardize_prepared_target.py` (target-standardization), `04_build_external_products.py` (external-products): `--fixture-manifest` option, `_stage_entry(..., fixture_manifest=None)` kwarg, one `require_receipts_for_snapshot(...)` call after `assert_lock_complete`.
- `scripts/05_build_features_and_splits.py` (features-and-splits), `06_train_and_predict.py` (models-and-baselines), `07_evaluate_and_report.py` (evaluation-and-comparison): the same three touches plus one early-return in `_run` reaching an additive `_run_fixture_scale` — apparatus partitions from the validated scope (never a frozen id), fixture stamps (`apparatus_partition_id`, `smoke_only`/caveat freight) on every output (embedded payload stamps on 06's predictions; sibling stamp files on 05's bundles and 07's metrics artifacts), apparatus split manifest on 05, no locked path reachable on 06/07, and a parser error for `--fixture-manifest` combined with a frozen `--partition`.
- `scripts/03_verify_processing.py` (owner: target-standardization) — **beyond the plan's seven, recorded in change record §11 for the owner to confirm or reverse**: its `_load_tolerance` carried its own `yaml.safe_load` of a fixture manifest — the second parser R-133 control 4 refuses, predating this unit. Rerouted through `load_fixture_scope`; behaviour strictly narrows (an invalid manifest now refuses at the loader). Without this the mandated project-wide only-copy scan fails on day one.
- `src/data/acquisition.py` (owner: acquisition) — one additive public predicate, `assert_records_within_window`, consumed by `scripts/run_walking_skeleton.py` and `tests/test_clean_run.py` (change record §5, §11). Made in the 2026-09-07 session; omitted from this table's first version and added per reviewer finding 2.
- The seven owners' READY code-summaries go stale under their receipts (tabulated in change record §5); staleness carried to the stage gate.

## Key implementation decisions

- **BLK-02 held throughout**: the apparatus is built; no fixture manifest exists on disk and no measuring run can complete before the `TBD — freeze gate` fields and TensorFlow pin freeze. The two Q-31 freeze acts remain owner acts.
- **BLK-08 mechanism limb — CLOSED by D-37 (2026-09-10), reaffirming D-27** (updated after
  the owner's adoption; the line previously read "stays a checked refusal … D-27 unreopened").
  The checked refusal REMAINS the mechanism: R-139 control 25 still refuses a `toleranced`
  TECU entry whose producing path declares no `inverse_route`, at full strength. D-27 stands
  unreopened; the primary path's citable route is `identity (D-27: primary target
  untransformed)`; `ABL-DIFF` keeps the only real inverse. **BLK-02 stays OPEN.**
- **Guard-boundary shape (nfr-design c58/c59)**: `load_fixture_scope` is the single manifest-loading guard home; every public entry point (the seven stage scripts + orchestrator) carries a negative control pushing a violating input through that entry point.
- **Step 10 gated stop is the terminal state for the agent**: the agent made no commit and may not. The repository fact, however (reviewer finding 1, verified by `git log`): owner commit `64c0551` (2026-09-07 12:21 +0400) already carries the Step 1–5/7 outputs, the `acquisition.py` edit and the change record's first version, with an unedited git template message and **no D-number cited** — violating `team.md`'s hard linking rule; the seventh template-message owner commit in the standing pattern (6246907, ec8eacf, 06207c4, da6cb7b, c7e7a05). The resume-pass outputs (Step 6 sibling edits, `tests/test_clean_run.py`, plan ticks, this summary) remain uncommitted. The owed citations — D-11, D-14, D-20, D-28, D-29, D-31 plus `CR-2026-09-07-R133-FIXTURES-AND-REPRODUCIBILITY` — now attach to an amend-or-follow-up decision that is the student's, routed to the stage gate.

## Test results

Environment: uv-managed CPython 3.11.16 in the session scratchpad + a stdlib pytest stand-in; PyPI unreachable (`pyyaml`/`pytest`/`ruff` absent). **Smoke evidence only, session-of-generation only, never governed.**

- `tests/test_clean_run.py`: **47 passed, 0 failed, 3 skipped** (46/0/3 at first completion; +1 after the reviewer-driven control-count meta-test was added) — skips all by name: two pyyaml-gated production-loader paths (`require_fixture_receipts` full path incl. the Q5 exemption; control 32's frozen-hash staleness, now also carrying the R-141 must-not-fire acceptance limb) and the clean-run completion test skipping with the §18.3 stop-and-report reason. It fails (never passes) on a non-zero exit when preconditions hold. WS-20/TA-09/TA-17/TA-21 stay `Pending`.
- Derived counts printed by the meta-test (verbatim): `negative controls: enumerated 39 ((1)-(39), sum 39); annotated 39; missing []; extra []; duplicated []` and `must-not-fire: derived 11 (1+1+1+1+2+2+1+1+1 over ['R-133' … 'R-141']); annotated 11 (of which 1 hosted elsewhere); missing []; extra []`.
- Ten named regression modules + test_clean_run: **437 passed, 0 failed, 13 skipped, 0 errors**.
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

## Review — Iteration 2

**Iteration:** 2 (terminal)
**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-09T17:40:24Z

### Verification of iteration-1 findings

| # | Status | Evidence |
|---|---|---|
| 1 (Critical) | **Resolved** | `code-summary.md` "Key implementation decisions" and "Routed to the stage gate" now state the true repository fact instead of the false "no commit made" claim: owner commit `64c0551` (2026-09-07 12:21 +0400, unedited git template message, no D-number) carries Steps 1–5/7 plus the `acquisition.py` edit; verified this is still the actual, unamended commit (`git log -1 --format="%B" 64c0551` unchanged from iteration 1 — no history rewrite, consistent with the project's "never edit a signed record" posture). The new claim additionally names six prior same-pattern commits (`6246907`, `ec8eacf`, `06207c4`, `da6cb7b`, `c7e7a05`) as a "standing pattern" — verified independently: all six exist, all six carry the identical unedited git placeholder message with no D-number, so `64c0551` is genuinely the seventh instance, not an invented aggravating detail. `governance/CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md` gained a dated `§11.1` correction that supersedes `§10`'s original "no commit is made here" bullet without rewriting it in place (`§10` line 244 stands untouched, labelled superseded by `§11.1`) — consistent with `project.md`'s "never edit a human-signed record" correction discipline. The decision (amend the existing commit's message vs. let it stand with a recorded reason) is correctly routed to the student rather than resolved by the agent. |
| 2 (Major) | **Resolved** | `code-summary.md`'s Files-modified table now lists `src/data/acquisition.py` (owner: acquisition, `assert_records_within_window`), matching what the change record already disclosed. |
| 3 (Minor) | **Resolved** | `tests/test_clean_run.py` gained `CONTROL_HOSTS`/`MUST_NOT_FIRE_HOSTS`/`MNF_HOSTED_ELSEWHERE` ledgers and `test_control_counts_derived_from_business_rules_not_carried`, which parses `business-rules.md`'s `(1)-(39)` enumeration and its `1+1+1+1+2+2+1+1+1=11` must-not-fire derivation, set-differences (never totals) the annotated host lists against it, and prints counts plus missing/extra before asserting. Re-ran the full file in the session's uv-managed CPython 3.11.16 (`run_tests.py . test_clean_run`): output is `negative controls: enumerated 39 ((1)-(39), sum 39); annotated 39; missing []; extra []; duplicated []` and `must-not-fire: derived 11 (...); annotated 11 (of which 1 hosted elsewhere); missing []; extra []`, and the suite reports `47 passed, 0 failed, 3 skipped` — this matches `code-summary.md`'s claimed figures and printed derivation string exactly, character for character. The `R-137:mnf1`-hosted-elsewhere presence check against `tests/test_train_only_transforms.py` passed rather than being skipped, so the claimed disclosed indirection is real, not merely asserted. |

### New finding (introduced by the fix; does not block)

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 4 | Minor | `governance/CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md:263,269,272` (§10, Step 8 log) vs. `code-summary.md` lines 18, 39, 41 | Adding the iteration-1 Finding-3 meta-test grew the suite by one test function and one passing test (49→50 functions, `test_clean_run` 46→47 passed, the ten-sibling-modules-plus-`test_clean_run` total 436→437), and `code-summary.md` was updated to the new figures throughout — but the change record's own `§10` "Step 8" log still asserts the superseded `49`/`46 passed`/`436 passed` figures, and unlike `§11.1` (which explicitly named both the old and new commit-state facts), the new `§11.2` addendum documents the *mechanism* added (the control ledger and derivation meta-test) without restating the count delta, so a reader comparing `§10` against `code-summary.md` meets two disagreeing totals with no signpost reconciling them. This is the same class of gap `project.md`'s correction-sweep rules target (a corrected fact's superseded representation left standing without a pointer to the correction), just on a fact of low consequence (a test-count delta of one, not a governance claim). | Add one sentence to `§11.2` (or a `§11.3`) stating the delta explicitly — "Step 8's `49`/`46 passed`/`436 passed` are superseded by `50`/`47 passed`/`437 passed` after this addition" — mirroring how `§11.1` restated the commit-state delta, so the two artifacts' totals reconcile without the reader having to re-derive which figure is current. |

### Suite re-verification (this iteration)

Re-ran in the session's uv-managed CPython 3.11.16 (PyPI unreachable, as before): `test_clean_run` alone reproduces `47 passed, 0 failed, 3 skipped` with the exact derived-count print lines quoted above. A combined run of the ten named regression modules plus `test_clean_run` reproduces the same pre-existing, disclosed `test_iri_denial` failure (1) seen in iteration 1 and unaffected by this pass; the exact "10 modules" partition behind the claimed `437/0/13` total could not be independently reconstructed byte-for-byte from the artifact (it does not name the ten modules), which mirrors an ambiguity already present and not flagged in iteration 1 rather than a new defect, so it is noted here but not raised as a fresh finding.

### Verdict rationale

Zero Critical, zero Major, two Minor (the pre-existing iteration-1 Minor is resolved; one new Minor surfaced by the fix itself). Per the stated verdict rule (READY if zero Critical, ≤2 Major, any number of Minor), and with the iteration budget exhausted, this unit is **READY**.

## Reformat + decision-request review (2026-09-10)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-10T08:31:21Z
**Scope:** second gate-worklist pass (repo HEAD `cdc61f7`, working tree uncommitted) — the
five-file reformat, `governance/FREEZE_DECISION_REQUEST_2026-09-10.md` (new), the CLAUDE.md
graphify correction, the fixture-README Kaggle in-session sections, and CR `§11.7`.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Minor | `code-summary.md` lines 51 and 55 (Deviations item 4; "Routed to the stage gate") | These lines still assert "47 over-99-column lines remain … real `ruff` owed" and "the 47 over-99 lines + owed `ruff`/`graphify` runs," which was true when iteration 2 closed but is now superseded: this pass's reformat (recorded in `governance/CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md` `§11.7`) reduced the count to 0 across all five files, independently re-verified line-by-line (`src/data/fixture_manifest.py`, `fixture_gate.py`, `fixture_evidence.py`, `scripts/run_walking_skeleton.py`, `scripts/01_inventory_and_registry.py`; character-accurate count, not the byte count a naive `awk`/`wc -c` produces on the em-dash-heavy lines here). `code-summary.md` is the PRIMARY artifact a reader consults first, and per `project.md`'s repeatedly-affirmed correction ("sweep every REPRESENTATION of a corrected fact, not every instance… a register entry, the owning unit's own paragraph… are different representations"), the CR closing the count does not itself sweep the code-summary's own two representations of the stale "47 remain" fact. `ruff` itself is still correctly reported as owed (CR `§11.7`: "Real `ruff` STILL could not run") — only the line-count clause is stale. | Add one line to `code-summary.md` (a `§` note or an edit to Deviations item 4) stating the over-99 count is now 0 per CR `§11.7`, distinct from the still-open `ruff`/`graphify` obligations, so the two artifacts agree without a reader having to cross-reference dates. |

### Verified and NOT flagged

- **Reformat is behavior-preserving.** Re-derived the over-99-column count independently (UTF-8-character-aware, not byte-count — an em-dash-heavy line under-counts by 2 bytes/char and produced a false-positive 52/4-remaining on a naive byte-count pass, corrected before reporting): HEAD `48` (10+5+12+20+1 across the five files, matching the artifact's stated starting figure) → working tree `0` (matching CR `§11.7`'s "0" and the artifact's "reformatted to 0" claim). Read every hunk of all five diffs (`git diff HEAD`): every change is a parenthesis/argument wrap, a string split at whitespace (word contents unchanged when concatenated), or in `fixture_evidence.py` one trivial local-variable extraction (`smoke = scope.fixture_id == PLUMBING_FIXTURE_ID`) — no exception-message text, docstring meaning, or control flow changed. `pyproject.toml` has a zero-line diff against HEAD (confirmed via `git diff HEAD -- pyproject.toml`). Four residual lines sit at 100–101 raw bytes but ≤99 characters (em-dashes are 3 UTF-8 bytes/1 character) — not a defect, and this review's own first pass on it was the false positive, caught and corrected before write-up.
- **`governance/FREEZE_DECISION_REQUEST_2026-09-10.md` adopts no value.** `git diff HEAD -- configs/` is empty (zero lines) — none of the 16 inventoried `TBD — freeze gate` fields was filled. Independently swept `configs/data.yaml`, `configs/experiment.yaml`, `configs/features.yaml` for the literal sentinel and reconciled by grouping (the five-ablation-fields row groups 10 sentinel keys into one inventory row, `requirements.txt`'s TF-pin gap is the 16th): 16 rows confirmed, matching the file's own count. `evidence/DECISIONS.md` register end confirmed at `D-32`; `D-27` confirmed still reading "resolved (2026-08-24)" with no reopening text — matches `§2`'s framing exactly. `§3`'s Q5 options (a/a2/b/c) and its routing to `external-products`' owner were checked against `governance/CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md` `§6.2`, which states the identical routing and the identical "Nothing is changed in that test module by this pass" disclosure — consistent.
- **CLAUDE.md correction is documentation-only and scoped.** `git diff HEAD -- CLAUDE.md` touches only the `## graphify` section's Rules block (conditions each `graphify <verb>` rule on an installed CLI, keeps the mandate, adds the skill/direct-read fallback); no other section of the file is touched.
- **README additions match implemented CLI shape.** `scripts/run_walking_skeleton.py` accepts `--config`, `--fixture` (`choices=FIXTURE_IDS`), and `--code-commit`, exactly as the new "Kaggle in-session sequence" section describes; `src/data/fixture_gate.py` exports `emit_in_session_gate_result` and `require_in_session_gate`, exactly as cited. Both README additions state "nothing here claims TA-03/TA-26 discharged" / "both stay Pending" — no evidence-of-completion is claimed, matching TA-03/TA-26's actual status.
- **No guard weakened.** Every diff hunk across the three `src/data/*.py` files and both scripts is a pure reformat or the one extraction noted above; no `raise`/`_refuse` call was removed, no exception type downgraded, no condition inverted or loosened. `evidence/test_run_access_log.jsonl`'s new entries are additional performance-blind `coverage_audit` rows from re-running `test_release_hashes`/`test_acquisition_window` during this pass (`performance_inspected: false` throughout) — consistent with the claimed full-suite re-run, not a new access class. No test file was deleted or shortened in `git status`.
- **CR `§11.7` is accurate** on every point checked above; it derives and prints its own "0" rather than carrying a stale figure, and its Q5/decision-request summary matches the underlying files it describes.

### Verdict rationale

One Minor (a staleness gap in the PRIMARY artifact's own Deviations/routing text, superseded by this pass's own change record but not swept back into `code-summary.md`), zero Critical, zero Major. This unit remains **READY**.

## Gate-floor re-review (2026-09-10)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-10T14:47:09Z
**Scope:** fresh floor re-derivation against HEAD `f0d9e49` + uncommitted working tree, after
a gate rejection reset the review floor. Working-tree changes since the last verdict: a
sibling `acquisition` repair touching `src/data/experiment_registry.py`, `src/data/acquisition.py`,
`scripts/00_acquire_prepared_vtec.py`, `tests/test_acquisition.py`, and — in this unit's own
lane — `tests/test_clean_run.py`; plus `configs/data.yaml` (`partitions:` block, D-38) and
`configs/experiment.yaml` (`embargo_hours: 24`, D-38); plus `evidence/DECISIONS.md` D-37/D-38.
Environment: no real pytest/ruff/pyyaml (PyPI egress blocked, re-verified 2026-09-10);
ran the stdlib pytest stand-in at
`...\26ca41ab-0b23-424c-a7c3-a767d4b33251\scratchpad\pytest_standin\run_tests.py` under uv-managed
CPython 3.11.16 — a stand-in, not real pytest; named honestly.

### Re-derived facts (printed, not carried)

- **Suite run** (`run_tests.py <repo> test_clean_run`): `58 passed, 0 failed, 3 skipped, 0 errors`.
  The 3 skips are all pyyaml-gated (`test_exported_check_full_path_requires_yaml`,
  `test_control_32_gate_result_predating_the_frozen_manifests_fails`, and the clean-run
  completion test skipping with its named §18.3 reason: *"clean-run completion NOT RUN —
  first unmet precondition: pyyaml is not importable on this clone... TS-X-01"*). The
  completion test's skip/execute transition is still honest: it did NOT flip to executing or
  to claiming WS-20/TA-17 evidence merely because `configs/data.yaml`'s `partitions:` and
  `configs/experiment.yaml`'s `embargo_hours` cleared two of its precondition fields —
  pyyaml unavailability is a separate, still-unmet precondition, and the printed reason
  names exactly that one.
- **39/11 reconciliation, printed by the file's own meta-test**: `negative controls:
  enumerated 39 ((1)-(39), sum 39); annotated 39; missing []; extra []; duplicated []` /
  `must-not-fire: derived 11 (1+1+1+1+2+2+1+1+1 over [R-133..R-141]); annotated 11 (of which
  1 hosted elsewhere); missing []; extra []`. Both set-differences are empty in both
  directions. The sibling repair's new real-invocation test,
  `test_rec2_00_stage_entry_real_invocation_refuses_out_of_window`, is confirmed present
  only in `BEYOND_ENUMERATION_CONTROLS` (`tests/test_clean_run.py:1904-1906`) — it does not
  appear in, and was not counted toward, the 39/11 enumerated ledger.
- **`grep -c "^def test_" tests/test_clean_run.py` → 61** (was 50 at the last verdict; 60 at
  committed HEAD per the change record's own `§11.6` count, +1 for the sibling's new
  real-invocation test). `58` of 61 pass, matching the runner.
- **BLK-02**: `find . -iname fixture_manifest.yaml` → no hits anywhere in the repository.
  No measured value is stated, inferred or substituted; `configs/experiment.yaml: folds`
  stays the literal `TBD — freeze gate` sentinel; only `embargo_hours` was filled, and only
  under D-38's disclosed joint owner+supervisor authorization, not by convenience.
- **`evidence/DECISIONS.md` tail confirmed at D-38**, D-37 immediately before it. D-37: *"D-27
  stands, unreopened and unamended... R-139 control 25 preserved at full strength... BLK-08's
  mechanism limb is CLOSED by this decision; BLK-02 stays OPEN."* Cross-checked against
  `business-rules.md` R-139 control (25)'s own text (line 642: a `toleranced` entry declaring
  TECU units for an output whose producing path declares no `inverse_route` fails) — unchanged,
  and `tests/test_clean_run.py::test_control_25_tecu_tolerance_without_inverse_route_is_not_freezable`
  is present, unmodified in the diff, and passing.
- **`load_fixture_scope` single-guard-home scan**: `test_control_4_only_copy_yaml_parse_scan_project_wide`
  (an AST scan, not a substring grep) passes; independently re-grepped `safe_load`/`yaml.load`
  across `src/`, `scripts/`, `tests/` for `fixture_manifest` mentions — the only hits are inside
  `src/data/fixture_manifest.py` itself (the one loader) and a doc-comment in
  `scripts/03_verify_processing.py` describing the reroute, not a second parse call. The scan's
  disclosed limit (it flags only calls whose argument subtree textually mentions
  `fixture_manifest`) is stated honestly in the test's own docstring
  (`tests/test_clean_run.py:493-526`) and is not overclaimed anywhere in `code-summary.md`.
- **Multi-run composition / freeze-write guards** (`src/data/fixture_manifest.py`):
  `compose_measurement_ranges` still refuses a zero-width `runtime.cpu_total`/`storage_total`
  range (lines 1501-1508); `write_candidate_manifest` still refuses any `data["status"] !=
  CANDIDATE` (lines 1571-1576) — the owner's Q-31 freeze act stays unreachable from this code.
- **Over-99-column count, re-derived character-aware** (not byte-count): `0` across
  `src/data/fixture_manifest.py`, `fixture_gate.py`, `fixture_evidence.py`,
  `scripts/run_walking_skeleton.py`, `scripts/01_inventory_and_registry.py` — matches the
  prior "Reformat + decision-request review" pass's derivation.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `code-summary.md` "Test results" section (lines 44-49) and `governance/CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md` §11.6-§11.7 | Both of this unit's own governing artifacts describe `tests/test_clean_run.py` as it stood before the sibling `acquisition` repair: `code-summary.md` still asserts "47 passed, 0 failed, 3 skipped" / "50 test functions"; the change record's last word on the file (`§11.6`) says "unchanged by this pass (57 passed / 3 skipped by name)". The actual current file (working tree) has 61 `test_` functions and passes 58 of them (re-derived and printed above), because a sibling unit's repair added `test_rec2_00_stage_entry_real_invocation_refuses_out_of_window` to a module this unit owns, and neither of this unit's artifacts records that edit at all — not the fact that the file changed, not the new count, not the new test's purpose. `project.md`'s repeatedly-affirmed corrections (`fd-2026-08-30-sweep-derive-sites`, `code-generation:c32`) require exactly this: a cross-unit edit to an owned module gets an explicit ruling and the owning unit's now-stale artifact is carried to the gate under its frozen receipt, disclosed — not silently left to assert a superseded count. | Add a dated note to `code-summary.md`'s Test results section and a new change-record entry (e.g. `§11.8`) stating: `tests/test_clean_run.py` was edited by the `acquisition` unit's 2026-09-10 adversarial-re-review repair (Finding 2), adding one real-invocation test; current counts are 61 functions / 58 passed / 0 failed / 3 skipped, reconciliation still empty both ways. This is disclosure, not a fix owed by this unit — the edit itself is sound and already independently reviewed by the sibling's own re-review per the test's docstring. |
| 2 | Minor (unresolved, carried from the 2026-09-10 "Reformat + decision-request" review) | `code-summary.md` lines 56 and 60 (Deviations item 4; "Routed to the stage gate") | Still asserts "47 over-99-column lines remain … real `ruff` owed" and "the 47 over-99 lines + owed `ruff`/`graphify` runs." Re-derived independently this pass (character-aware, not byte-count): the actual count is `0` across all five files named in the prior review's own derivation (`fixture_manifest.py`, `fixture_gate.py`, `fixture_evidence.py`, `run_walking_skeleton.py`, `01_inventory_and_registry.py`), consistent with `governance/CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md` §11.7's closure. This Minor was flagged in the prior review pass and remains unswept in `code-summary.md` itself. | Same as previously recommended: add one line to `code-summary.md` stating the over-99 count is 0 per CR §11.7, distinct from the still-open `ruff`/`graphify` obligations. |

### Verified and NOT flagged

- BLK-02 holds (no `fixture_manifest.yaml` anywhere; no measured value stated/inferred/substituted).
- BLK-08's mechanism limb is CLOSED by D-37, reaffirming D-27 unreopened; R-139 control 25
  is unchanged and at full strength; BLK-02 stays OPEN — all four facts consistent across
  `evidence/DECISIONS.md`, `business-rules.md`, `tests/test_clean_run.py`, and
  `code-summary.md`'s own "Key implementation decisions" section.
- `load_fixture_scope` remains the single manifest-loading guard home project-wide; the
  scan's disclosed textual-mention limit is stated honestly, not overclaimed.
- The clean-run completion test's skip/execute transition stays honest after D-38 filled two
  of its precondition fields — it still skips on the pyyaml precondition and does not claim
  WS-20/TA-17 evidence.
- No TBD sentinel was filled by convenience; no scientific constant lives in source; no
  credential found in the touched files; no guard was weakened (every diff hunk inspected in
  the sibling's edit to `tests/test_clean_run.py`, `src/data/acquisition.py`,
  `src/data/experiment_registry.py` adds a check or a structural AST assertion — none removes
  a `pytest.raises`, downgrades an exception type, or loosens a condition).
- The zero-width multi-run range refusal and the `status != CANDIDATE` freeze-write refusal
  in `src/data/fixture_manifest.py` are both unchanged and still exercised by passing tests.

### Verdict rationale

Zero Critical, one Major (Finding 1: this unit's own artifacts are silent about a sibling
edit to a module this unit owns, understating the current test count — a disclosure gap,
not a code defect; the edit itself was independently reviewed by the sibling's own
adversarial re-review per the new test's docstring), one Minor carried forward unresolved
(Finding 2, the stale over-99 line count). Per the stated verdict rule (READY if zero
Critical, ≤2 Major, any Minor), this unit is **READY**, with Finding 1 routed to the stage
gate for disclosure rather than blocking: the hard invariants this re-review was dispatched
to attack — BLK-02, BLK-08/D-27, the 39/11 reconciliation, the single guard home, the
zero-width and freeze-write refusals, TBD-sentinel discipline — all hold at full strength
against the current tree.
