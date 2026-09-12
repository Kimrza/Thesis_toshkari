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
| `tests/test_clean_run.py` | 8 | §12 mandated module: **64 test functions** (corrected in place 2026-09-12; was `50`, superseded first by the sibling `acquisition` repair of 2026-09-10 and then by this unit's own 2026-09-12 precondition repair — count derived from source and printed by its own final test: `def test_ count derived from source: 64; collected: 64`) hosting the 39 negative controls and 11 must-not-fire controls — both figures machine-checked by `test_control_counts_derived_from_business_rules_not_carried`, which parses `business-rules.md`'s enumeration and set-differences it against the file's `CONTROL_HOSTS`/`MUST_NOT_FIRE_HOSTS` ledger (empty in both directions; `R-137:mnf1` hosted in `tests/test_train_only_transforms.py`, presence-asserted) — plus the per-area §15.2 enumeration, project-wide AST only-copy scan, §13.2 fence parse (membership AND order, flags verbatim, ruled scope argument recognised), and the skip-with-named-reason completion test |

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

- `tests/test_clean_run.py`: **61 passed, 0 failed, 3 skipped, 0 errors** over **64 test functions** — figures re-derived and printed 2026-09-12, correcting **in this section's own body** the superseded `47 passed / 50 functions` that three consecutive review passes flagged and that was only ever corrected in a `## Review` addendum (`project.md` `code-generation:fr-2`). The trail, stated so no reader has to reconstruct it: `46/0/3` at first completion → `47/0/3` after the control-count meta-test → `58/0/3` over 61 functions after the sibling `acquisition` unit's 2026-09-10 repair added `test_rec2_00_stage_entry_real_invocation_refuses_out_of_window` to this module → `61/0/3` over 64 functions after this unit's own 2026-09-12 precondition repair added three beyond-enumeration controls (see § Precondition check corrected (2026-09-12) below). Skips all by name: two pyyaml-gated production-loader paths (`require_fixture_receipts` full path incl. the Q5 exemption; control 32's frozen-hash staleness, now also carrying the R-141 must-not-fire acceptance limb) and the clean-run completion test skipping with the §18.3 stop-and-report reason. It fails (never passes) on a non-zero exit when preconditions hold. WS-20/TA-09/TA-17/TA-21 stay `Pending`.
- Derived counts printed by the meta-test (verbatim): `negative controls: enumerated 39 ((1)-(39), sum 39); annotated 39; missing []; extra []; duplicated []` and `must-not-fire: derived 11 (1+1+1+1+2+2+1+1+1 over ['R-133' … 'R-141']); annotated 11 (of which 1 hosted elsewhere); missing []; extra []`.
- ~~Ten named regression modules + test_clean_run: **437 passed, 0 failed, 13 skipped, 0 errors**.~~ **Superseded 2026-09-12.** This figure is not reproducible from the artifact, because the artifact never names which ten modules it partitions (a reviewer recorded the same ambiguity on 2026-09-10 without raising it as a finding). Replaced with a partition that IS reproducible — **every `tests/test_*.py` module in the repository, 26 modules: 1160 passed, 0 failed, 39 skipped, 0 errors** (2026-09-12, same stand-in runner). The pre-existing failures line below is likewise superseded by that run: the four import-error modules and the `test_external_drivers` / `test_iri_denial` / `test_locked_test_guard` failures it records are all green on the current tree.
- One self-introduced regression fixed same pass: `test_models_smoke`'s source assertion tripped by the new fixture path; local renamed to `fixture_target`.
- Pre-existing failures reproduced identically on the stashed, unmodified tree (git stash round-trip): `test_external_drivers` 11, `test_iri_denial` 1, `test_locked_test_guard` 1, 4 import-error modules — not caused by this pass.
- `compileall` clean over `scripts/`, `src/`, `tests/`.

## Deviations from the plan

1. `03_verify_processing.py` reroute (above) — owner-reversible, change-record §11.
2. Two controls + the exported-check full path are pyyaml-gated skips; substance exercised at stdlib level through `verify_receipt`/`write_fixture_pass_receipt`/`require_in_session_gate` (controls 26–31 real). Full runs owed to a governed environment.
3. `graphify update .` not run — CLI absent on this clone; owed with `ruff`.
4. **0 over-99-column lines remain** — corrected in place 2026-09-12, superseding "47 … remain in the four 2026-09-07 files (plus one pre-existing in `01`)", which the 2026-09-07 reformat (change record §11.7) had already closed and which three consecutive review passes flagged as unswept HERE. Re-derived character-aware (never byte-count: an em dash is 3 UTF-8 bytes and 1 character) over the same five files every prior derivation used — `src/data/fixture_manifest.py` 0, `src/data/fixture_gate.py` 0, `src/data/fixture_evidence.py` 0, `scripts/run_walking_skeleton.py` 0, `scripts/01_inventory_and_registry.py` 0, **total 0** — and additionally over `tests/test_clean_run.py` itself after the 2026-09-12 repair: **0**. Real `ruff` remains owed and is a separate, still-open obligation; the line-count clause alone is what is closed.

## Routed to the stage gate

Amendment ledger +1 → 8 across 6 owed (`component-methods.md`); the seven sibling edits + stale code-summaries plus the 03 reroute (owner ruling requested); §15.2 REQ-ENG-4 13→12 correction owed in `requirements.md`; the FR-WS-2/FR-WS-3 candidate §15.2 rows and M10 §13.2 placement proposals (change record §§8–9); the two Q-31 freeze acts; BLK-02 open, BLK-08 mechanism limb open; WS-20/TA-09/TA-17/TA-21 `Pending`; TA-03/TA-26 unproducible off Kaggle; TA-15 not covered (foundation's); the stale `team.md` § Walking Skeleton "remains open under Q-31" line (practices-gate-owned); the owed `ruff`/`graphify` runs (the over-99 line count that used to be routed here alongside them is **0**, re-derived 2026-09-12 — see Deviations item 4; only the tool runs remain owed); and the commit disposition: owner commit `64c0551` exists with a template message and no D-number (the standing pattern's seventh instance) — the student's ruling is owed on amending it to cite D-11, D-14, D-20, D-28, D-29, D-31 + `CR-2026-09-07-R133-FIXTURES-AND-REPRODUCIBILITY`, or letting it stand with a recorded reason, before the still-uncommitted resume-pass outputs land on top. The agent made no commit.

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

## Floor-reset re-review (2026-09-11)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-11T15:07:51Z
**Scope:** fresh floor derivation against HEAD `b0b7c1d` + uncommitted working tree
(`git status --short`: this unit's own record files are UNCHANGED since the last verdict —
only sibling code-summaries, `evidence/test_run_access_log.jsonl`, and
`tests/test_locked_test_guard.py` — a `governance-guards`-owned module, out of this unit's
lane — are modified). Environment re-verified: no real pytest/ruff/pyyaml (PyPI egress
blocked); ran the stdlib pytest stand-in at
`...\26ca41ab-0b23-424c-a7c3-a767d4b33251\scratchpad\uv-pythons\cpython-3.11.16-windows-x86_64-none\python.exe`
against `...\scratchpad\pytest_standin\run_tests.py` — a stand-in, not real pytest.

### Re-derived facts (printed by the tools, not carried)

- **`grep -c "^def test_" tests/test_clean_run.py` → 61** (file byte-for-byte unchanged
  from the last verdict; not touched by this floor's working-tree diff).
- **Suite run**: `test_clean_run: 58 passed, 0 failed, 3 skipped, 0 errors`. The three skips
  are the same named pyyaml-gated ones as the last verdict, including the completion test's
  named §18.3 reason.
- **39/11 reconciliation, printed by the file's own meta-test**: `negative controls:
  enumerated 39 ((1)-(39), sum 39); annotated 39; missing []; extra []; duplicated []` /
  `must-not-fire: derived 11 (1+1+1+1+2+2+1+1+1 over [R-133..R-141]); annotated 11 (of
  which 1 hosted elsewhere); missing []; extra []`. The board-remediation control
  `test_rec2_00_stage_entry_real_invocation_refuses_out_of_window` sits only in
  `BEYOND_ENUMERATION_CONTROLS` (`tests/test_clean_run.py:1904-1915`, ten board-added
  controls total, Rec 2–5), verified via
  `test_beyond_enumeration_controls_exist_and_do_not_touch_the_ledger`
  (`tests/test_clean_run.py:1918-1923`), which asserts each is callable AND `not in
  CONTROL_HOSTS` — it is structurally excluded from the enumerated ledger, not merely
  claimed to be.
- **BLK-02**: `find . -iname fixture_manifest.yaml` → no hits anywhere in the repository.
  `configs/experiment.yaml: folds` and `configs/data.yaml: stations` remain the literal
  `TBD — freeze gate` sentinel.
- **`evidence/DECISIONS.md` tail confirmed at D-38**, D-37 immediately before it, text
  unchanged from the last verdict's quotation. R-139 control 25
  (`tests/test_clean_run.py:1068`, `business-rules.md` line 642) is present, unmodified,
  and passing — BLK-08's mechanism limb reads CLOSED by D-37 (reaffirming D-27
  unreopened); BLK-02 stays OPEN.
- **Guard-home scan**: `grep -rn "safe_load\|yaml.load" src/ scripts/ tests/ | grep -i
  fixture_manifest` finds exactly one production call site
  (`src/data/fixture_manifest.py:493`, inside `load_fixture_scope` itself) plus its own
  docstring's description of the chokepoint's disclosed limit, and a doc-comment in
  `scripts/03_verify_processing.py:244` describing the reroute (not a second parse call).
  No second manifest-loading guard home exists.
- **Multi-run/freeze-write refusals** (`src/data/fixture_manifest.py`):
  `compose_measurement_ranges` still raises `_refuse` on `float(min) == float(max)`
  (lines 1501–1508, unchanged); `write_candidate_manifest` still raises `_refuse` on any
  `data["status"] != CANDIDATE` (lines 1571–1576, unchanged).
- **Over-99-column count, re-derived character-aware over the same five files as every
  prior pass**: `0` (`fixture_manifest.py` 0, `fixture_gate.py` 0, `fixture_evidence.py`
  0, `run_walking_skeleton.py` 0, `01_inventory_and_registry.py` 0; total 0).
- **No credential/secret pattern** (`api[_-]?key|password|secret|kaggle\.json|token\s*=`)
  found in `src/data/fixture_manifest.py`, `fixture_gate.py`, `fixture_evidence.py`,
  `scripts/run_walking_skeleton.py`, or `tests/test_clean_run.py`.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `code-summary.md` "Test results" section (lines 44–49) | **Unresolved for the third consecutive review pass.** These lines still assert "47 passed, 0 failed, 3 skipped" and "50 test functions," a fact superseded twice over: first by the 2026-09-10 "Reformat + decision-request" pass's own line-count correction, then explicitly named stale by the 2026-09-10 "Gate-floor re-review" (its own Finding 1), which derived and printed the true figures (61 functions / 58 passed). The current working tree is unchanged from that state — `tests/test_clean_run.py` still has 61 `def test_` functions and 58 pass (re-derived above) — yet the PRIMARY artifact's Test results section, the section a reader consults first, has not been edited to match either the prior review's own printed derivation or this one. `project.md`'s repeatedly-affirmed correction ("sweep every REPRESENTATION of a corrected fact... a register entry, the owning unit's own paragraph... are different representations") applies here a third time without effect: the correction lives only in two `## Review` addenda, never in the artifact body it corrects. | Edit the "Test results" section itself (not another review addendum) to state 61 functions / 58 passed / 0 failed / 3 skipped, and cite the sibling `acquisition` edit that added the 61st function, before this reaches the gate a third time with the same stale numbers. |
| 2 | Major | `tests/test_clean_run.py:1598-1612` (`_completion_preconditions`, the `configs/*.yaml` TBD-field loop) | The per-field TBD check is a substring co-occurrence test, not a per-field value check: `if field in text and "TBD" in text` returns true whenever the field's NAME appears anywhere in the file's text AND the literal string `"TBD"` appears ANYWHERE else in that same file — it never isolates the specific field's assigned value. Today this coincidentally reports the correct blocking field only because the genuinely-unresolved field is listed FIRST in each pair (`("folds", "embargo_hours")`, `("stations", "cell_rule")`) and short-circuits before the second field is ever evaluated: verified `configs/data.yaml:45` `stations: "TBD — freeze gate"` (genuinely unresolved) precedes `configs/data.yaml:58` `cell_rule: "floor-half-open-d1"` (genuinely resolved, D-33) in the checked tuple, and `configs/experiment.yaml:20` `folds: "TBD — freeze gate"` precedes `configs/experiment.yaml:26` `embargo_hours: 24` (resolved, D-38). If `stations` or `folds` resolves before the paired field, or if any other `TBD` sentinel remains anywhere else in either file's prose (both files carry multiple explanatory `TBD — freeze gate` comments even outside the checked fields), this check will misattribute the block to a field that is actually resolved — violating the org/team Mandated rule that an integrity failure must be surfaced "naming the file and the violated expectation," which this project treats as a hard practice for exactly this class of gate (§18.3 stop-and-report). The defect is currently dormant: the outer `yaml`/`numpy`/`pandas` import check (lines 1582–1589) short-circuits before this loop is ever reached on this clone (pyyaml is unavailable), so no wrong reason has actually been printed yet, and the check still fails SAFE in aggregate (it never claims completion when a real TBD blocks it) — but it is a genuine correctness defect in code this project relies on for a supervisor-facing reproducibility gate (G-07), not merely a documentation staleness issue. | Replace the substring check with a per-field value read (parse the field's own line/value, or — once pyyaml is available — load the mapping and check the specific key's value against the literal sentinel) so the named "first unmet precondition" is always the field actually holding the sentinel, independent of file-wide TBD prose or tuple ordering. |
| 3 | Minor (unresolved, carried across two prior reviews) | `code-summary.md` lines 56 and 60 (Deviations item 4; "Routed to the stage gate") | Still asserts "47 over-99-column lines remain … real `ruff` owed" and "the 47 over-99 lines + owed `ruff`/`graphify` runs." Re-derived independently this pass (character-aware, not byte-count) over the same five files named in every prior derivation: `0`. This Minor was flagged in both the 2026-09-10 "Reformat + decision-request" review and the 2026-09-10 "Gate-floor re-review," and remains unswept in `code-summary.md` itself through this third pass. | Same as previously recommended: edit lines 56/60 to state the over-99 count is 0 per CR §11.7, distinct from the still-open `ruff`/`graphify` obligations. |

### Verified and NOT flagged

- BLK-02 holds; no `fixture_manifest.yaml` anywhere; no measured value stated, inferred,
  or substituted; no TBD sentinel filled by convenience.
- BLK-08's mechanism limb is CLOSED by D-37, reaffirming D-27 unreopened; R-139 control 25
  is unchanged and at full strength; BLK-02 stays OPEN — consistent across
  `evidence/DECISIONS.md`, `business-rules.md`, `tests/test_clean_run.py`, and
  `code-summary.md`'s own "Key implementation decisions" section.
- `load_fixture_scope` remains the single manifest-loading guard home project-wide; no
  second production parse of a `fixture_manifest.yaml` exists.
- The zero-width multi-run range refusal (`compose_measurement_ranges`) and the
  `status != CANDIDATE` freeze-write refusal (`write_candidate_manifest`) are both
  unchanged and still exercised by passing tests.
- No credential, API key, or secret pattern found in this unit's five owned modules.
- The 39/11 negative-control/must-not-fire reconciliation is empty in both directions,
  independently re-run and printed, and the board-remediation controls added by the
  sibling `acquisition` re-review are structurally confirmed excluded from that ledger.
- `tests/test_locked_test_guard.py` (modified in the current working tree) is
  `governance-guards`'s module, not this unit's — out of lane, not reviewed here.

### Verdict rationale

Zero Critical, two Major (Finding 1: the Test-results disclosure gap, now unresolved
across three consecutive review passes though independently re-derived and printed each
time; Finding 2: a newly-found, currently-dormant substring-matching defect in the
completion precondition's TBD-field naming), one Minor carried forward unresolved
(Finding 3, the stale over-99 line count, also unresolved across three passes). Per the
stated verdict rule (READY if zero Critical, ≤2 Major, any Minor), this unit remains
**READY** — every hard invariant this floor-reset was dispatched to attack (BLK-02,
BLK-08/D-27 and R-139 control 25, the single guard-home, the zero-width and freeze-write
refusals, the 39/11 reconciliation, TBD-sentinel and credential discipline) holds at full
strength against the current tree, and neither Major finding is a runtime or scientific
defect — one is chronic documentation staleness in the PRIMARY artifact, the other is a
dormant code defect that fails safe today and has not yet produced an incorrect result.
Both should be closed before this unit's next gate encounter; a fourth consecutive pass
finding #1 unresolved would warrant escalating it past Major.

---

## Precondition check corrected (2026-09-12)

**Scope.** The owner reopened the code-generation gate to fix exactly one correctness
defect — Finding 2 of the 2026-09-12 floor-reset re-review (Major, real but dormant). No
other code change was made, no guard was weakened, no locked December data was accessed,
no `TBD — freeze gate` sentinel was filled, and no evidence was fabricated. The existing
review history above is untouched; the stale claims this repair uncovered were corrected
**in the body sections that make them** (the Files-created row for
`tests/test_clean_run.py`, § Test results, § Deviations item 4, § Routed to the stage
gate), per `project.md` `code-generation:fr-2` — a correction filed only in a review
addendum leaves the stale claim standing for its own reader.

### The defect as found

`tests/test_clean_run.py`, `_completion_preconditions`, at HEAD `c8c63d2` lines 1598–1612:

```python
for config_name, fields in (
    ("experiment.yaml", ("folds", "embargo_hours")),
    ("data.yaml", ("stations", "cell_rule")),
):
    ...
    for field in fields:
        if field in text and "TBD" in text:
            return f"configs/{config_name}: {field} is `TBD — freeze gate`; ..."
```

`if field in text and "TBD" in text` is a **whole-file substring co-occurrence test**. It
asks "does this field's NAME appear anywhere in the file, AND does the string `TBD` appear
anywhere in the file" — never "is THIS field's own value the sentinel". It therefore named
the correct blocking field only by tuple-order coincidence, and would misattribute as soon
as that order or the files changed — which they already have: **D-38** resolved
`embargo_hours` to `24` and **D-33** resolved `cell_rule` to `floor-half-open-d1`, while
`folds` and `stations` remain the sentinel. It is dormant on this clone only because the
pyyaml-import precondition short-circuits ahead of it.

Probe against the real `configs/`, printed — the offender each form names, in both tuple
orders:

| Checked order | Old form names | New form names |
|---|---|---|
| `("folds", "embargo_hours")` | `folds` | `folds` |
| `("embargo_hours", "folds")` | **`embargo_hours`** (resolved by D-38) | `folds` |
| `("stations", "cell_rule")` | `stations` | `stations` |
| `("cell_rule", "stations")` | **`cell_rule`** (resolved by D-33) | `stations` |

The two reversed-order rows are the defect realised: the old form names a field a signed
decision has already resolved.

### The fix

Three stdlib-only helpers replace the co-occurrence test with a **per-field value check**,
and `_completion_preconditions` now delegates to them:

| Symbol | Role |
|---|---|
| `_scalar_on_key_line(rest)` | Strips an inline YAML comment without a parser: a `#` ends the scalar only when it is outside quotes AND preceded by whitespace (YAML's own rule), so a `#` inside a quoted value is preserved rather than truncating the value. |
| `_config_field_state(text, field)` | Classifies ONE top-level `field:` line's OWN value as `_RESOLVED`, `_UNRESOLVED` (equal to `TBD_SENTINEL`) or `_UNDETERMINED`, returning a stated reason in every case. |
| `_config_tbd_reason(config_name, text, fields)` | The reason for the FIRST of `fields` that does not resolve, or `None`. The order of `fields` decides which offender is reported first; it never decides WHICH field is named. |

Design points, each deliberate:

- **Stdlib only.** pyyaml is unavailable (PyPI egress blocked, verified) and this check runs
  ahead of the pyyaml precondition it guards, so no YAML parser may be used. The reader is
  narrow by construction: it reads a top-level `field: <scalar>` line and nothing else.
- **It says so rather than guessing.** Where it cannot read a field's own value — key
  absent, declared more than once at top level, or block-valued — it returns
  `_UNDETERMINED` with the reason named, and `_config_tbd_reason` turns that into a
  stop-and-report skip reason naming the field. A value containing `TBD` that is not the
  sentinel is also `_UNDETERMINED`, never silently resolved. This strengthens the check:
  the old form treated every one of those cases as "resolved".
- **The sentinel literal is no longer duplicated.** The check imports `TBD_SENTINEL` from
  `src/data/config.py` (the R-01 single declaration site) instead of re-spelling
  `TBD — freeze gate` in the test, so the test and `assert_no_tbd` cannot drift.
- **Nothing was weakened.** The precondition chain's ORDER is unchanged (pyyaml/numpy/pandas
  → fixture manifests → config fields → TensorFlow pin), the skip-with-named-reason
  behaviour is unchanged, the TBD reason string is byte-identical to the old one, and
  `test_clean_run_completion_or_skip_with_named_reason` still `pytest.fail`s on a non-zero
  subprocess exit when every precondition holds. **It claims no WS-20/TA-17 evidence: those
  rows stay `Pending`, and the completion test still skips on this clone.**

### New controls (three, all outside the (1)-(39) ledger)

Registered in `BEYOND_ENUMERATION_CONTROLS`, not `CONTROL_HOSTS`, exactly as the governance
board's Rec 2–5 rows are — so the 39/11 reconciliation is untouched by construction, and
`test_beyond_enumeration_controls_exist_and_do_not_touch_the_ledger` asserts each is hosted
and absent from the ledger. All three use synthetic field names (R-122): no governed config
is read and no config value is stated in them.

| Control | What it proves |
|---|---|
| `test_precondition_names_the_field_whose_own_value_is_the_sentinel` | The misattribution is fixed. An EARLIER-checked field is resolved (`apparatus_alpha: 24`, with `TBD` planted in its inline comment) and a LATER one carries the sentinel; the reason must name `apparatus_beta` and must NOT contain `apparatus_alpha`. The test also asserts the replaced form's own condition holds on that same text (`"apparatus_alpha" in text and "TBD" in text`), so it is an explicit regression witness for the defect, not merely a check of the new behaviour. |
| `test_precondition_does_not_fire_when_every_checked_field_resolves` | The must-not-fire half. With every checked field resolved — including one whose inline comment spells the full sentinel and one whose quoted value contains a `#` — `_config_tbd_reason` returns `None`, so the completion test is never skipped for a TBD reason the checker invented. |
| `test_precondition_reports_an_unreadable_field_instead_of_guessing` | TE §18.3 applied to the reader itself. For each of absent / block-valued / declared-twice, the state is `_UNDETERMINED`, the detail names the specific reason, and the returned reason names the field and says it *cannot be read* — and does not claim the sentinel. Without this the new reader could fail open the way the old one did. |

### Results (derived and printed, never carried)

Runner, named honestly: **uv-managed CPython 3.11.16 in the session scratchpad plus the
stdlib pytest stand-in** (`pytest_standin/run_tests.py`). **Real `pytest` did not run and
real `ruff` did not run** — PyPI is unreachable on this clone; both remain owed to a
governed environment. Smoke evidence only, never governed.

- `tests/test_clean_run.py`: **61 passed, 0 failed, 3 skipped, 0 errors** over **64 test
  functions** (58/0/3 over 61 before this repair: +3 passed, +3 functions, exactly the three
  new controls). The file's own derivation printed: `def test_ count derived from source:
  64; collected: 64`.
- The three skips are unchanged and all named: two pyyaml-gated production-loader paths, and
  the completion test skipping with `pyyaml is not importable on this clone (PyPI
  unreachable); the production read path refuses by name (TS-X-01)` — the first unmet
  precondition, i.e. the repaired config check is still not the one reached on this clone.
- **39/11 reconciliation, printed verbatim after the change — EMPTY in both directions:**
  - `negative controls: enumerated 39 ((1)-(39), sum 39); annotated 39; missing []; extra []; duplicated []`
  - `must-not-fire: derived 11 (1+1+1+1+2+2+1+1+1 over ['R-133', 'R-134', 'R-135', 'R-136', 'R-137', 'R-138', 'R-139', 'R-140', 'R-141']); annotated 11 (of which 1 hosted elsewhere); missing []; extra []`
- Full suite, all 26 `tests/test_*.py` modules: **1160 passed, 0 failed, 39 skipped, 0
  errors**.
- Over-99-column lines, re-derived character-aware after the change: **0** in
  `tests/test_clean_run.py` and **0** across the five files every prior derivation used.

### Residuals, stated precisely

1. **The repaired path is still not exercised against the real `configs/` by the suite on
   this clone.** `_completion_preconditions` short-circuits at the pyyaml import, so the
   config-field branch is reached only by the three synthetic controls and by the probe
   recorded above. This is the same environment limit that makes WS-20/TA-17 `Pending`; it
   is not closed by this repair and must not be read as closed.
2. **`ruff` and `graphify update .` remain owed** — both tools are absent on this clone. No
   formatter or linter verified these lines; the 99-column figure above is a hand-derived
   character count, not a `ruff` result. The graph under `graphify-out/` is stale for
   `tests/test_clean_run.py`.
3. **The reader is deliberately narrow.** It handles top-level scalar fields only. If a
   checked field ever becomes nested or block-valued, the check reports `_UNDETERMINED` and
   the clean-run test skips naming it — correct and safe, but it means a future nested
   required field needs a real parser rather than an extension of this helper.
4. **`evidence/test_run_access_log.jsonl` grew by 37 append-only rows** during the
   full-suite run, written by the locked-test guard on behalf of `test_acquisition_window`
   and `test_release_hashes` (pre-existing modules; `purpose: coverage_audit`,
   `performance_inspected: false`). No row came from `tests/test_clean_run.py` or from any
   control added here, no December content was inspected, and the log was not edited or
   truncated — it is append-only by design (WS-18 / TA-18).
5. **Repository state at the time of writing, re-verified** (`git log -1`, `git status` —
   `project.md` `code-generation:c30`): HEAD is `c8c63d2`; `tests/test_clean_run.py` and this
   file are modified and **uncommitted**; `aidlc-state.md`, the audit shard and
   `evidence/test_run_access_log.jsonl` are also modified in the working tree. **The agent
   made no commit and no push**, as instructed. The commit disposition routed at § Routed to
   the stage gate is unchanged and still the student's.

---

## Precondition-fix review (2026-09-12)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-12T11:48:54Z
**Scope:** adversarial re-verification of the one Major fix ("Precondition check corrected
(2026-09-12)" above), repo HEAD `c8c63d2` + uncommitted `tests/test_clean_run.py` and this
file. Environment re-verified: no real pytest/ruff/pyyaml/numpy/pandas (PyPI egress
blocked); ran the stdlib pytest stand-in
(`...\26ca41ab-0b23-424c-a7c3-a767d4b33251\scratchpad\pytest_standin\run_tests.py`) under
the scratchpad's uv-managed CPython 3.11.16 venv — a stand-in, not real pytest, named
honestly.

### Independent reproduction of the fix's own demonstration

Wrote a standalone probe importing `_config_field_state`/`_config_tbd_reason` from
`tests/test_clean_run.py` alongside a literal reimplementation of the replaced
`if field in text and "TBD" in text` form, run against the real `configs/data.yaml` and
`configs/experiment.yaml`. Confirmed first, independent of the artifact's own claim, that
`configs/data.yaml:45` reads `stations: "TBD — freeze gate"` (genuinely unresolved) and
`configs/data.yaml:58` reads `cell_rule: "floor-half-open-d1"  # D-33 …` (resolved);
`configs/experiment.yaml:20` reads `folds: "TBD — freeze gate"` and
`configs/experiment.yaml:26` reads `embargo_hours: 24  # D-38 …` (resolved). With the tuple
order reversed:

| Order | Old form (reimplemented) | New form (`_config_tbd_reason`) |
|---|---|---|
| `("cell_rule", "stations")` | names `cell_rule` (resolved by D-33) | names `stations` |
| `("embargo_hours", "folds")` | names `embargo_hours` (resolved by D-38) | names `folds` |

This matches the artifact's table exactly and is not a case of `_UNDETERMINED` masquerading
as stricter behaviour — both `stations` and `folds` really are the literal sentinel today,
and `_config_field_state` reports `_RESOLVED` for `cell_rule`/`embargo_hours` in the same
probe, so the new form's correctness is a genuine fix, not an artifact of over-caution.

**Adversarial attacks on `_scalar_on_key_line`/`_config_field_state`, all held:**
- `#` inside a quoted value (`"value # not comment"  # real comment`) is preserved verbatim;
  only the real trailing comment is stripped.
- A resolved field whose own inline comment spells the sentinel text
  (`folds: 4  # TBD — freeze gate is what this USED to say`) is still reported `_RESOLVED`
  — immune to the exact co-occurrence trap the fix targets.
- A quoted value containing the sentinel plus extra characters
  (`"TBD — freeze gate extra"`) is reported `_UNDETERMINED` with a stated non-sentinel-TBD
  reason, never silently treated as either resolved or the sentinel — correctly
  conservative rather than fooled.
- A field whose value **is** the exact sentinel but carries a trailing comment claiming
  otherwise is still `_UNRESOLVED` on the value alone — comment content never overrides the
  value. No path found that flips a genuinely-unresolved field to `_RESOLVED`, or vice
  versa, by comment or quoting tricks.

Chain order (`yaml`/`numpy`/`pandas` import → fixture manifests → `experiment.yaml` then
`data.yaml`, same field-tuple order → `requirements.txt`) is unchanged from the pre-fix
version (diffed against `git show HEAD:tests/test_clean_run.py`, formerly at lines
1579–1615). The `_UNRESOLVED` reason string is byte-identical to the replaced form's
(`f"configs/{config_name}: {field} is \`{TBD_SENTINEL}\`; every stage entry refuses at
assert_no_tbd…"` — `TBD_SENTINEL` resolves to the same literal `"TBD — freeze gate"` the old
code hardcoded). `TBD_SENTINEL` is now imported from `src/data/config.py` (R-01's single
declaration site) rather than duplicated — confirmed at import block lines 63–69. No path
in the fixed code or its three new tests claims WS-20/TA-17 evidence; the completion test
(`test_clean_run_completion_or_skip_with_named_reason`) still skips on this clone with the
named `pyyaml is not importable` reason, confirmed by direct run below.

### New controls and reconciliation

`test_precondition_names_the_field_whose_own_value_is_the_sentinel` independently confirmed
to assert the OLD form's own condition holds on its apparatus text
(`"apparatus_alpha" in text and "TBD" in text`) before asserting the NEW form names the
correct field — a genuine regression witness, not a check of new behaviour alone.
`test_precondition_does_not_fire_when_every_checked_field_resolves` and
`test_precondition_reports_an_unreadable_field_instead_of_guessing` reproduce as described.
All three are registered only in `BEYOND_ENUMERATION_CONTROLS`, confirmed absent from
`CONTROL_HOSTS` by direct grep, and asserted so by
`test_beyond_enumeration_controls_exist_and_do_not_touch_the_ledger`.

Re-ran the file's own reconciliation meta-test: `negative controls: enumerated 39
((1)-(39), sum 39); annotated 39; missing []; extra []; duplicated []` /
`must-not-fire: derived 11 (…); annotated 11 (of which 1 hosted elsewhere); missing [];
extra []` — both empty in both directions, independently reproduced, matching
`business-rules.md` § Negative-control count's own printed derivation (checked by reading
that section directly: `5+4+5+2+3+4+5+4+3+4 = 39`, `1+1+1+1+2+2+1+1+1 = 11`).

### Re-derived counts (all reproduced independently via the stand-in runner)

- `tests/test_clean_run.py`: **61 passed, 0 failed, 3 skipped, 0 errors** over **64**
  `def test_` functions (`grep -c "^def test_"` → 64, matching `collected: 64`). Matches the
  artifact's claim exactly.
- Full suite, all 26 `tests/test_*.py` modules present in the repo: **1160 passed, 0
  failed, 39 skipped, 0 errors** — matches the artifact's claim exactly.
- Over-99-character lines (character-aware, not byte-count): **0** across
  `src/data/fixture_manifest.py`, `fixture_gate.py`, `fixture_evidence.py`,
  `scripts/run_walking_skeleton.py`, `scripts/01_inventory_and_registry.py`, and
  `tests/test_clean_run.py` itself — matches Deviations item 4 and the Routed-to-gate line
  exactly.

### Verification of the five claimed body corrections

All five verified accurate against the working-tree diff (`git diff HEAD`) and independent
re-derivation, and none is a rewrite of prior review history — the diff is purely additive
after the last existing `## Review` block, plus the five targeted body edits themselves:

1. Files-created row for `tests/test_clean_run.py`: `50` → **64**, correct (re-derived).
2. § Test results: `47 passed / 0 failed / 3 skipped` → **61/0/3 over 64**, with the
   `46→47→58→61` trail stated; correct and internally consistent with the three prior
   review passes' own printed figures (47 after the control-count meta-test, 58/61 after
   the sibling `acquisition` repair).
3. The un-reproducible "ten named regression modules… 437 passed" line struck through and
   replaced with the reproducible 26-module partition, **1160/0/39/0** — correct
   (re-derived above), and the strikethrough preserves the original text rather than
   deleting it, consistent with the project's "never edit a signed record" posture applied
   here to its own prior claim.
4. § Deviations item 4: `47 over-99` → **0**, correct (re-derived above), with the
   superseded figure's context (four 2026-09-07 files plus one in `01`) preserved in the new
   text rather than erased.
5. § Routed to the stage gate: the `47 over-99 lines` clause replaced with a pointer to
   Deviations item 4's `0`, leaving the still-open `ruff`/`graphify` obligations distinct
   and intact — correct.

No existing `## Review` block's text, verdict, or findings table was altered; the new
material is appended after the "Floor-reset re-review (2026-09-11)" section and its own
`---` separator, exactly as the artifact claims.

### Also checked, held

- BLK-02: `find . -iname fixture_manifest.yaml` → no hits anywhere in the repository;
  `git diff HEAD -- configs/` is a zero-line diff — no TBD sentinel filled, no scientific
  constant touched.
- R-139 control 25 (`test_control_25_tecu_tolerance_without_inverse_route_is_not_freezable`)
  present, unmodified in the diff, still annotated `(25,)` in `CONTROL_HOSTS`.
- `load_fixture_scope` (`src/data/fixture_manifest.py:493`) remains the only production
  `yaml.safe_load` of a `fixture_manifest`-named artifact in `src/`, `scripts/`, `tests/`;
  `scripts/03_verify_processing.py:244` carries only a doc-comment describing the reroute.
- `compose_measurement_ranges` (zero-width refusal) and `write_candidate_manifest`
  (freeze-write refusal) both still `raise _refuse(...)` at their prior line numbers,
  unmodified in the diff.
- No credential/secret pattern (`api[_-]?key|password|secret|kaggle\.json|token\s*=`) in the
  `tests/test_clean_run.py` diff. No guard removed, no exception downgraded, no condition
  loosened anywhere in the diff — every hunk either adds the three helpers/three tests or
  swaps the one loop body for a delegated call with an unchanged reason string.
- `evidence/test_run_access_log.jsonl`'s new rows are all `purpose: coverage_audit`,
  `performance_inspected: false` — no locked-December performance inspection reachable from
  this change, consistent with every prior pass.
- Full suite run reproduced with zero failures, so no regression was introduced by the fix
  outside the one module it touches.

### Verdict rationale

Zero Critical, zero Major, zero Minor newly found. The one Major this reopening was
dispatched to fix (`_completion_preconditions`'s whole-file substring co-occurrence test) is
resolved: independently reproduced with the real `configs/` files, adversarially probed for
comment/quoting-based fooling with no success found, chain order and reason-string byte
identity confirmed unchanged, and the three new negative/must-not-fire controls verified to
prove what they claim without touching the existing 39/11 reconciliation. All five stale
body representations flagged by the dispatch are corrected accurately and in place, with no
rewriting of prior signed review history. Full 1160-test suite green; no TBD filled, no
credential, no guard weakened, no locked-December reachability introduced. **READY.**
