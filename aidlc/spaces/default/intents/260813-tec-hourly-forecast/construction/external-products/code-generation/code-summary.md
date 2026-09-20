# Code Summary — `external-products`

**Unit** `external-products` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`
**Plan**: `code-generation-plan.md` — Steps 1–9 executed, checkboxes marked; **Step 10 (added 2026-09-13) was WITHDRAWN as already-discharged and never executed** — see § "Correction, 2026-09-13" below. **No IRI benchmark and no GIM comparator generated** — the gate refusals are the deliverable. No December/restricted-root touch; no scientific value decided.

**Repository state, re-derived 2026-09-13 at HEAD `1670ac8`** — this header previously read "No `git commit` (governance stop)", which is **false as a statement about the current repository** and is corrected here rather than left for a reader of the header to trust. This unit's code IS committed: `src/external/iri.py` and `src/external/gim.py` in **`ed5808b`** (unedited git template message, no D-number), `scripts/04_build_external_products.py` most recently in **`0e002cd`** ("Governance disposition + board remediation…" — a real subject line, but citing no D-number), `tests/test_iri_denial.py` in **`cdc61f7`**. `team.md` § Way of Working requires any commit touching a governed artifact to cite its D-number. **No commit, amend or revert was made by this stage** — the commit is the student's act, and the amend-or-follow-up disposition is routed to the gate as part of the standing commit-message ruling.

## Correction, 2026-09-13 — the `test_iri_denial.py` count, and Step 10's withdrawal

*Written into the body rather than filed as a review addendum, per `project.md`
(`code-generation:fr-2`): a correction filed only at the foot leaves the stale claim
standing for its own reader.*

**The count.** The Files-created row for `tests/test_iri_denial.py` asserted **19 tests**.
Re-derived 2026-09-13: `grep -c "^def test_" tests/test_iri_denial.py` = **22**. The file
has carried 22 since commit `cdc61f7` (2026-09-10 11:41:01), which added a scope-aware
containment-scan narrowing for `src/evaluation/metrics.py`'s deferred import — a commit
that landed **eight minutes after** the review then verifying the figure, and was never
reflected here. That commit's message records that dated cross-unit edit records were
appended to eight other owners' code-summaries; **no equivalent disclosure was made to
this unit's own code-summary for the edit to its own owned test file.** The Files row is
corrected above. The two verification rows in § "Independent verification" that record
"19" are left standing unedited — they truthfully record what was counted on the date
those passes ran, and `project.md` forbids editing a signed record to match a later
derivation. Read them as historical, not current: **the current figure is 22.**

**Step 10.** Added to the plan on 2026-09-13 to route the non-fixture subprocess
invocations through `--fixture-manifest`, then **withdrawn the same day** on the owner's
ruling that **Q5 = Choice B stands** (ruled 2026-09-10, already implemented). Zero files
were modified by it. The plan's § "Step 10 withdrawal" carries the full grounds, the
corrected call-site derivation (**11 non-fixture invocations, not nine** — `--evidence-root`
is an input-path option, not a fixture scope), and a **new CRITICAL gate finding**: script
`04` cannot pass the walking-skeleton fixture ladder at all, so the plumbing fixture's
receipt can never be written and **WS-20 and TA-17 are unreachable rather than merely
`Pending`**. The owner ruled on 2026-09-13 to record that finding and rule on the remedy
later; no code moved on it.

## Files created

| Path | What |
|---|---|
| `src/external/spaceweather.py` | Driver builders/guards: `trailing_mean` (trailing by construction; TC-20 refusal), `resolve_f107_at_origin` (R-57a stop naming origin + staleness), alignment onto the existing `AlignmentError`, `apply_carry_forward` ≤ 3 h + conservation invariant, time-indexed/identical-across-cells refusals (TC-12), single-grade + eligibility (D-10.1/TC-11), four provenance fields + bounded reanalysed-value check (declared-status-only, never closed), `provenance_stamp` (evidentiary), `write_driver_manifest` (two-tier, `guard_egress`), `refuse_divergent_rerun` (SD-E-07, SEC-A-02 adopted) |
| `src/external/iri.py` | R-59's four limbs: refuses without a passing **pre-declared** validation report; tolerance timestamp must precede comparison; field-by-field report assertion (2000 km, 5–10 official-interface samples, no-future-centering); never silently switched; D-25 carried AS STANDING (amendment not treated as granted); `iricore` import inside the gated path only |
| `src/external/gim.py` | Q-15 refusal (rule UNSET, no default); hand-check + overlap-audit timestamps must precede generation; map-to-map + spatial-mismatch statements emitted by the reporting path itself; comparison with no registered `gim_network_overlap_flag` fails; outside-tuning residual named open |
| `scripts/04_build_external_products.py` | Position 04; six-step entry; `audit_ec1_drivers.py` logic migrated in — the `:184` unconditional `return 0` closed onto the two-tier posture (missing months = machine-readable field naming WHICH months, non-fatal; hash mismatch vs recorded `ec1-audit-report.json` hashes terminates naming file + expectation); registry rows via foundation's writer; `--attempt-benchmark`/`--attempt-comparator`/`--gate-state`/`--render-comparison` paths; original script untouched |
| `tests/test_iri_denial.py` | §12-mandated, **22 tests** (re-derived 2026-09-13: `grep -c "^def test_" tests/test_iri_denial.py` = 22; **was 19** here and at the two verification rows below, stale since commit `cdc61f7`, 2026-09-10 11:41:01, which added a scope-aware containment-scan narrowing for `src/evaluation/metrics.py`'s deferred import and landed eight minutes after this file's then-latest review — see § "Correction, 2026-09-13" below) — ordered switch (`failed` outranks; unresolved edge → skipped w/ edge; both limbs populated → `passed`; empty limb → `skipped` naming which, JSON-structured reason); complement-defined candidate set over `.py` + ast-parsed `.ipynb` cells; `__init__.py` walked/count-subtracted; transitive; content limb (`iri_*` name fails; **absent provenance fails**). Negative controls: injected field/direct import/transitive import/stripped stamp all caught |
| `tests/test_external_drivers.py` | **51 tests** — every refusal negative-controlled incl. centered-mean caught by the shift property, 4 h gap excluded, per-cell join refused, mixed grades refused, TBD-composition stop, both-injection exit-code pair, and 11 subprocess controls exercising the IRI/GIM refusals **through the allowlisted script** (tests never import iri/gim) |
| `governance/CHANGE_RECORD_2026-09-05_R55_external_contracts.md` | DRAFT — boundary-contract blocks for the three modules; applied only on owner approval; no application-design artifact edited |

## Files modified in place

| Path | What |
|---|---|
| `src/data/config.py` | Q1=A: `ImportBoundaryError` (expectation names the full reachability chain), `FeatureAvailabilityError`, `BenchmarkError`, `ComparatorError` — IntegrityError subclasses, `__all__`, any-future clause. **`DriverError` NOT declared** (contested Finding 9; reason in docstring; would-be conditions raise the `IntegrityError` base). Plus minimal `("external-products", 1): ("seeds.development",)` in `REQUIRED_FIELDS_MAP` (script otherwise cannot run at all; no scientific value) |

## Test and lint results (smoke evidence only — never governed)

- **Full suite: 664 passed, 2 skipped, 0 failed** — Python 3.11.9; **re-run independently by the orchestrating session, same counts** (+70 over the 594 baseline). Both skips pre-existing.
- One transient dev-time failure: script 04's docstring initially held the restricted-root literal and `test_locked_test_guard`'s R-28 scan caught it — removed; the guard did its job.
- `ruff check`: all checks passed on the 7 touched files.

## Key decisions

1. **Refusals tested through the allowlisted importer** — `tests/*` is not allowlisted, so all IRI/GIM behaviour is exercised by subprocessing script 04; `--render-comparison`/`--gate-state` CLI surface added beyond the plan's letter because the plan's mandated negative controls are otherwise unreachable. Injection mode refuses even when fully satisfied — it never generates.
2. **Target files excluded from the candidate-importer set** (objects of containment, not risk surface); `spaceweather.py` remains a candidate.
3. **Clause-4 pin re-expressed**: the plan's "today's skipped state" was changed by the plan's own Steps 3–4 creating the targets; the real-tree scan now reaches a genuine clause-3 `passed`, and the skipped-naming-target-limb behaviour is pinned over a synthetic candidate set instead.
4. **Domain complement excludes `.git`/`__pycache__`/venv and the AI-DLC shell** (`.claude/`, `aidlc/`) — documented against team.md's workflow-infrastructure ruling and SD-E-00's own 18-file derivation.
5. Would-be `DriverError` conditions raise the `IntegrityError` base until the domain-entities reconciliation.
6. The migrated audit still covers all 12 Dst months including the plain-root provisional December driver file the approved original reads today; no restricted path constructed (R-28 one-door test green).

## Deviations

- `--render-comparison` CLI + `REQUIRED_FIELDS_MAP` entry (additive; required to make plan-mandated behaviour executable; recorded, not silent).
- Clause-4 pin re-expression (above).
- graphify CLI unavailable — graph stale for touched files; `graphify update .` owed.
- `ruff format` applied to new files only (`config.py` HEAD had pre-existing format drift; `ruff check` is the standing bar).

## Governance stop — owed before any commit (student acts; cumulative)

- `CHANGE_RECORD_2026-09-05_R55_external_contracts.md` is **DRAFT — NOT APPLIED**.
- Gate-routed items restated: `tests/*` blanket row (owner discrepancy in `component-dependency.md`), foundation-preflight structured-skip dependency (FR-WS-7 must read the skip reason, not count non-failures), provenance-default enlargement (features-and-splits' assertion half unstated), `DriverError` reconciliation, D-25's ungranted §15.2 amendment, `audit_ec1_drivers.py` retirement.
- Commit cites **D-25, D-21** as touched context. **No governed commit before the records exist.**
- Nothing discharged: WS-09, WS-10, WS-11, TA-07, TA-36 stay `Pending`; REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18 stay rowless/`UNTESTED`; no independence claim precedes the overlap audit.

## Review — 2026-09-05 (code-generation, iteration 1)

**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T18:19:38Z
**Iteration:** 1

### Findings

None survived adversarial verification.

### Verified and held (adversarial checks run, evidence machine-checked)

| Angle | Check performed | Result |
|---|---|---|
| Containment — real tests | `tests/test_iri_denial.py` contains no `import` of `src.external.iri`/`gim`; all 19 tests confirmed present by count (`grep -c "^def test_"` = 19); ordered-switch clauses 1–4 read in `run_containment_scan` match SD-E-01's precedence exactly (found path > unresolved edge > both-populated-pass > empty-limb-skip) | Matches claim |
| Containment — real-tree scan | `test_containment_scan_over_real_tree_is_never_vacuous` reaches clause 3 `passed` today because `iri.py`/`gim.py` now exist and `spaceweather.py` populates the risk surface; `test_clause4_target_limb_pinned_over_the_real_candidate_set` independently pins the clause-4 skip by scanning for absent target names, over the real candidate set (`walked_count > 0`) | Confirmed; the "clause-3 pin re-expression" deviation is honestly described |
| Containment — evasions attempted | Traced the ast walk's domain/allowlist/candidate logic by hand: `.ipynb` cells are parsed: `_parse_units`; `__init__.py` is walked but subtracted only from the cardinality count; a named-but-absent target still fires clause 1 (name-matching, not file resolution); third-party/stdlib imports are excluded from the edge graph so all-`pytest`-importing test files can't false-positive to clause 2 | No evasion route found; negative-control tests for direct import, transitive import (with full chain), notebook-cell import, and `__init__.py`-carried import all assert `failed` |
| Provenance limb | `iri_column_violations`: absent/blank provenance → fails (`ABSENT provenance fails`); present-and-not-IRI → admitted; `iri_*` name → fails regardless of provenance content. Tests `test_stripped_provenance_stamp_is_caught`, `test_present_non_iri_provenance_is_admitted`, `test_iri_named_column_fails_even_with_innocent_provenance` all present and assert the stated outcomes | Confirmed; the evidentiary-not-cryptographic framing is stated in both the docstring and `provenance_stamp`'s own text, matching the recorded Minor |
| Trailing mean / shift property | `trailing_mean` computes `[end_day-(window-1), end_day]` only; `test_shifted_input_shifts_output_with_it` and `test_centered_mean_variant_is_caught_by_both_limbs` construct an actual centered-window function and prove it diverges on both the definitional and perturbation limbs; missing/NaN day raises `IntegrityError` naming TC-20 | Confirmed by reading the property tests, not just the docstring |
| Carry-forward / cell-shape / grade rules | `apply_carry_forward` excludes beyond `bound_h`; `test_injected_four_hour_gap_excludes_the_row` present; `assert_time_indexed_shape`/`assert_identical_across_cells` refuse `_CELL_KEYS`-bearing rows and cross-cell divergence; `assert_single_grade`/`assert_grade_eligible` refuse mixed grades and provisional-for-barred-uses; `carry_forward_composition` TBD/absent → `FeatureAvailabilityError` via `resolve_f107_at_origin`, filled-but-uninterpreted value → base `IntegrityError` (never silently applied) | Confirmed against source and the corresponding negative-control tests |
| IRI benchmark gate (R-59) | `generate_benchmark` refuses at limb 1 with no report; `evaluate_generation_gates`→`assert_validation_report` enforces status, all 7 content areas, 2000 km ceiling, both driver confirmations, 5–10 samples spanning site/day-night/quiet-disturbed with official-interface values, and `declared_at_utc < comparison_ran_at_utc` (strict `>=` fails); `injection_mode=True` raises its own terminal refusal **before** reaching `import iricore`, so a fully-satisfied injected state never attempts the unavailable import — traced this path by hand since it is the one place a wrong ordering could turn a "refusal" into an uncaught `ModuleNotFoundError` | Confirmed safe; `test_benchmark_fully_satisfied_injection_still_refuses_generation` exercises exactly this path through the subprocess and asserts exit 1 with the injection-refusal text |
| GIM comparator gate (R-60) | `generate_comparator` refuses at obligation 1 while `interpolation_rule_from` returns `None` for absent/TBD; obligation-2 and overlap-audit ordering both use strict `>=`-fails-forward comparisons (a same-instant timestamp fails, consistent with "must precede"); `render_comparison_report`'s overlap-flag disclosure is keyed to the comparison's existence, not the audit's result, and fires even for a deliberately non-informative flag value | Confirmed; `test_comparison_without_registered_audit_fails_on_existence` and `test_comparison_report_emits_statements_and_flag_itself` both present and pass |
| Migrated audit / two-tier posture | `_verify_recorded_hashes` runs before `_audit_dst`/`_audit_f107` (integrity tier first); a missing month is appended to `missing_months` (named, non-fatal) while a recorded-hash mismatch raises `IntegrityError` naming the file and both hashes; both outcomes exercised in opposite directions by `test_script_missing_month_continues_and_names_which` (exit 0) and `test_script_hash_mismatch_terminates_naming_file_and_expectation` (exit 1) via actual subprocess runs against a synthetic workspace; all 12 Dst months and both GFZ series are accounted for (present, missing-file, or never-retrieved) | Confirmed; `audit_ec1_drivers.py` itself is untouched (not in the modified-files set; script 04 is a new file) |
| Restricted-root / R-28 one-door | `scripts/04_build_external_products.py` contains no `locked_test_restricted`/`audit_evidence_2022-FULL` literal (grep-confirmed); the repo-wide `tests/test_locked_test_guard.py::test_restricted_literal_holders_are_exactly_the_enumerated_exemption` scans `src/`, `tests/`, `scripts/` (including `.ipynb` cells) against an exact-membership exemption list that does **not** include script 04, so script 04 is genuinely covered by an existing cross-cutting test, not merely asserted in prose | Confirmed; resolves an initial concern that "R-28 one-door test green" for script 04 might be an overclaim (it isn't — the covering test is `test_locked_test_guard.py`'s, not one of this unit's own new files, but it does exist and does run) |
| Exceptions / `config.py` | `BenchmarkError`, `ComparatorError` declared as `IntegrityError` subclasses with docstrings citing R-59/R-60; `DriverError` genuinely absent from `config.py`; `REQUIRED_FIELDS_MAP[("external-products", 1)]` is exactly `("seeds.development",)`, matching the "field identities only, no scientific value" claim | Confirmed by direct read |
| Scope / authority honesty | `git status` confirms no `application-design/{components,component-methods,component-dependency}.md` is modified; `configs/` untracked-but-unmodified by this unit (pre-existing untracked state from prior units); `governance/CHANGE_RECORD_2026-09-05_R55_external_contracts.md` opens with `**Status: DRAFT — NOT APPLIED...**` | Confirmed |
| Suite / lint integrity | Re-ran the full suite independently under the pinned `tec311` interpreter with `--junitxml`: **666 tests, 0 errors, 0 failures, 2 skipped → 664 passed / 2 skipped**, exact match to the claimed count. `ruff check` on all 7 touched files: all checks passed. `test_external_drivers.py` and `test_iri_denial.py` test-function counts independently counted at 51 and 19 respectively, matching both claims | Confirmed independently, not taken on the summary's word |
| Test-file containment (meta) | Confirmed `tests/test_external_drivers.py` imports only `subprocess`/`ast`/stdlib plus `src.data.config` and `src.external.spaceweather` (the deliberately-outside-restriction module) — no import of `src.external.iri`/`gim` anywhere in either new test file | Confirmed; the "tests never import iri/gim" claim holds |

### Coverage limits (this pass did not additionally verify)

- The `iricore`-gated code path beyond the `import` statement itself (the 26,000-call workload, the Fortran rebuild) is genuinely unreachable in this environment and was not and could not be exercised — this matches the artifact's own claim that it is unimplemented, unreachable work.
- `features-and-splits`' own half of the SD-E-03 provenance contract (the feature-matrix-side assertion) was not read; this unit's own text and the plan both already route that half to the gate as owed, not claimed satisfied here.
- The carve-out for `acquisition/nfr-design/security-design.md` §SD-A-02 (the `guard_egress`/SEC-A-02 integration this unit's `refuse_divergent_rerun` and `write_driver_manifest` adopt unchanged) was spot-checked only by import (`from src.data.acquisition import guard_egress`) and by the fact that the full suite — which includes acquisition's own tests of that contract — passes; the contract's own internal correctness in `acquisition` was not re-derived here, consistent with the carve-out's scope.
- Did not independently re-verify every one of the ~10 SD-E-00…SD-E-07 coverage-table rows against `logical-components.md`; spot-checked the ones with executable teeth (SD-E-01, SD-E-03, SD-E-04, SD-E-05, SD-E-06, SD-E-07) since those are what code-generation had to implement.

### Summary

Every adversarial angle in the dispatch — containment evasions, the provenance flip, the trailing-mean/carry-forward/grade rules, both refusal gates' ordering checks, the migrated audit's two-tier posture, and the governance/authority-honesty claims — was traced against the actual source and, where a test existed, re-run rather than taken on faith. The full suite count (664 passed / 2 skipped) and ruff-clean claim both reproduced exactly under independent execution. No discrepancy between what the plan/summary claims and what is on disk was found; the one initial suspicion (an "R-28 one-door test green" claim for a script with no test of its own naming it) resolved in the artifact's favor once the repo-wide `test_locked_test_guard.py` scan was traced to confirm it does cover `scripts/04_build_external_products.py`. This is an unusually well self-verified unit.

**Verdict: READY**

<!-- superseded by the dated review blocks below; left standing per project.md's
never-edit-a-signed-record correction -->


### Cross-unit edit record (2026-09-10) — edits made by `fixtures-and-reproducibility`, owner-authorised

Appended after the gate rejection lifted the receipt freeze. Under
`CR-2026-09-07-R133-FIXTURES-AND-REPRODUCIBILITY` (§5, §6.1, §6.2, §11.5; the owner's
"apply the recommended option" ruling), the fixtures unit made these ADDITIVE edits to
`scripts/04_build_external_products.py` — nothing on the full-year path changed:

- Commit `cf3185d`: `--fixture-manifest` option (the visible Q5 = A exemption carrier),
  `_stage_entry(..., fixture_manifest=None)` kwarg, and ONE `require_receipts_for_snapshot`
  call after `assert_lock_complete` (TE §9.2's two-receipt gate; exempt on a fixture run).
- Commit `0e002cd` (board Rec 2 / ML-01): `_declared_data_window()` derives the declared
  window from the migrated audit's own `_AUDIT_YEAR` (calendar year), so a fixture-flagged
  invocation of the FULL-YEAR audit refuses against every fixture scope — the board's live
  ML-01 case.
- STANDING ROUTED ITEM (CR §6.2, unchanged): in a pyyaml-bearing environment
  `tests/test_external_drivers.py`'s nine non-fixture subprocess invocations refuse at the
  receipts gate before the paths they assert; the choice (pass `--fixture-manifest` in the
  smoke invocations, assert the new refusal, or ask the gate to narrow Q5) is this unit's
  owner's. On this clone those tests fail earlier, at the pyyaml preflight (11 failures,
  pre-existing and reproduced on the unmodified tree).

Tests live in `tests/test_clean_run.py` (`test_rec2_04_full_year_audit_exemption_refuses`).
This unit's owner may confirm or reverse per the change record.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-10T11:33:57Z
**Iteration:** Owner-rulings implementation review (2026-09-10)

### Findings

None survive verification at any severity for this unit.

### Verification performed

- **Q5 = Choice B** (this unit owns `04_build_external_products.py` and its test file).
  `tests/test_external_drivers.py` diff (+159/−49) reproduced under the stdlib pytest
  stand-in on scratchpad CPython 3.11.16: `test_external_drivers: 51 passed, 0 failed, 0
  skipped, 0 errors` — matches the claimed 51/0 exactly. Test-function count is unchanged
  at 51 before and after (`grep -c "^def test_"` on `git show HEAD:` vs. working tree),
  ruling out silent deletion.
  `_assert_gate_fails_closed` was read in full: it asserts `returncode != 0` (a genuine
  fail-closed check, not loosened to accept success) and requires the stderr to contain
  one of a small, specific marker set (`fixture`, `receipt`, `pyyaml is required`, plus
  each caller's own pre-Q5 marker via `also_accepts`) — not "any stderr". Confirmed against
  `scripts/04_build_external_products.py`'s `_stage_entry`/`main()` (read directly) that
  `main()` unconditionally calls `_stage_entry` — including for `--render-comparison` —
  so the dual-branch structure in `test_comparison_report_emits_statements_and_flag_itself`
  reflects real, existing script behaviour (not this unit's diff) rather than test-side
  fabrication. `test_manifest_stamps_every_series_and_names_missing_months` (unchanged)
  independently confirms the REQ-ENG-9 missing-month/partial semantics the rewritten
  subprocess test no longer asserts directly, so that coverage was moved, not dropped.
  `test_script_missing_month_continues_and_names_which` additionally now asserts no audit
  manifest is left behind on a refused run — verified present in the diff, not merely
  claimed.
- **No fabricated fixture manifest or receipt** anywhere in the diff — confirmed by
  reading the full diff hunk; no new fixture/receipt JSON files appear in
  `git status`/`git diff --stat`.
- **TensorFlow pin (item 5)** and **`practical_relevance_threshold` (item 3)** do not
  touch this unit's owned files; verified at the repo level (see the `foundation`,
  `features-and-splits`, and `models-and-baselines` units' review blocks) and cross-checked
  here only for absence of any conflicting reference to `04_build_external_products.py`.
  None found.
- **Test totals**: full-suite run (26 modules, stdlib stand-in) reproduces exactly
  `1134 passed, 0 failed, 39 skipped, 0 errors`, matching the claim.
- **`src/data/locked_test.py`**: `git diff HEAD` is empty (0 lines) — zero diff confirmed
  independently.
- **`evidence/DECISIONS.md`**: ends at D-32 (`git diff HEAD` empty) — no D-number was
  minted by this pass; all five drafts (D-A…D-E) live only inside
  `governance/CHANGE_RECORD_2026-09-10_owner_rulings_implementation.md`, unadopted.

### Summary

This unit's cross-cutting exposure is the Q5 receipt-gate contract in
`tests/test_external_drivers.py`, and the rewritten assertions are genuine fail-closed
checks against real subprocess exit codes and stderr text, not loosened placeholders —
verified by independent reproduction of the exact claimed pass count and by reading the
gated script's control flow directly. No fabricated evidence, no deleted tests, no
scope creep into this unit's other owned modules.

## Floor-reset re-review (2026-09-11)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-11T14:17:46Z
**Iteration:** Adversarial floor-reset re-review, against HEAD `b0b7c1d`

Re-derived from scratch against the current tree — no earlier verdict in this file was
taken on faith. Environment: no real pytest/pyyaml (PyPI egress blocked, confirmed);
ran both owned test modules under the stdlib pytest stand-in
(`.../scratchpad/pytest_standin/run_tests.py`) on the scratchpad's CPython 3.11.16 venv.

### Verification performed

- **Read all four owned source files in full**: `src/external/spaceweather.py`,
  `src/external/iri.py`, `src/external/gim.py`, `scripts/04_build_external_products.py`.
  Traced the trailing-mean window (`[end_day-(window_days-1), end_day]`, no future day
  can enter it — no `centered` implementation anywhere in the module; the only two hits
  for "centered" are the docstring's own negative statement), the ≤3h carry-forward
  bound with `excluded_epochs` beyond it (`apply_carry_forward`), the conservation
  invariant, the R-59/R-60 gate orderings (`declared_at >= comparison_at` and
  `checked_at/audited_at >= generation_attempt_utc` both fail-closed on `>=`, not `>`),
  and `generate_benchmark`/`generate_comparator`'s injection-mode terminal refusal
  placed BEFORE the gated `import iricore` line — confirmed the import is unreachable
  even when injected state satisfies every prior gate.
- **Import-boundary walk (not grep alone, TA-07)**: `grep -rn "^\s*from src.external import\|^\s*import src.external" src` across the whole `src/` tree returns exactly one
  real import site — `src/evaluation/metrics.py:477`, `from src.external import gim`,
  indented inside a function body (deferred/evaluation-time-only, matching that
  module's own docstring claim, spot-checked as the one named integration point outside
  this unit). No import of `src.external.iri` exists anywhere in `src/`. `src/features`
  and `src/models` carry only docstring mentions of the boundary rule, never a live
  import statement.
- **D-35's seven deferred driver rows** (`kp_safe`, `ap_safe`, `hp60_safe`, `ap60_safe`,
  `f107_safe`, `f107_81_trailing`, `dst`): confirmed genuinely absent from
  `configs/features.yaml: permitted_producers` with the exact D-35 rationale
  transcribed in the surrounding comment — this unit's code does not fabricate a
  producer identity for any of them; `REQUIRED_FIELDS_MAP[("external-products", 1)]`
  in `src/data/config.py:577` is exactly `("seeds.development",)`, matching the "no
  scientific value, field identities only" claim.
- **Governance stop still open**: `governance/CHANGE_RECORD_2026-09-05_R55_external_contracts.md`
  still opens `Status: DRAFT — NOT APPLIED`; no credential/secret pattern in any of the
  four owned/modified files.
- **Fixture-gate integration** (`src/data/fixture_gate.require_receipts_for_snapshot`,
  the one named external integration point besides `metrics.py`): read in full;
  confirmed the call site in `scripts/04_build_external_products.py`'s `_stage_entry`
  matches the real signature exactly (`fixture_manifest=`, `declared_window=`,
  `declared_window_resource=`), and that `_declared_data_window()` only returns a
  value (thereby engaging the Rec-2/ML-01 window-bound check) when
  `fixture_manifest is not None` — a full-year invocation with no `--fixture-manifest`
  gets no `declared_window` and is not exempted, consistent with the script's own
  docstring claim.
- **Test re-execution, independently, not taken on the summary's word**:
  `tests/test_iri_denial.py`: **22 passed, 0 failed, 0 skipped, 0 errors**.
  `tests/test_external_drivers.py`: **51 passed, 0 failed, 0 skipped, 0 errors**.
  The 51/0 for `test_external_drivers.py` matches the code-summary's claim exactly.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `code-summary.md` line 14 (Files-created table) | The artifact still asserts **"19 tests"** for `tests/test_iri_denial.py`, and both prior review passes (2026-09-05, 2026-09-10T11:33:57Z) treated 19 as independently confirmed. The file has carried **22** `test_` functions since commit `cdc61f7` ("Gate-worklist cleanup…", 2026-09-10 11:41:01, whose own message states "test_iri_denial: … 22/0" and adds a scope-aware containment-scan narrowing for the `src/evaluation/metrics.py` deferred-import case) — a commit landed **after** this file's last review timestamp (11:33:57Z, eight minutes earlier) and never reflected here. Independently re-derived by count (`git show ed5808b:tests/test_iri_denial.py \| grep -c "^def test_"` = 19 at creation vs. `git show cdc61f7:...` = 22 now) and by execution (22 passed, 0 failed under the stand-in) — the number itself is not in question, only that this artifact still states the superseded figure. The commit's own message records that "dated cross-unit edit records" were appended to eight other owners' code-summaries for this same commit; no equivalent update or disclosure was made to this unit's own code-summary for the edit to its own owned test file. This is the same failure mode `project.md`'s count-derivation and cross-unit-disclosure corrections (`application-design:count-derivation`, `code-generation:gf-3`) were written to catch, now recurring against this unit's own artifact rather than a sibling's. No functional or gate-safety defect follows from it — the containment-scan narrowing itself is real, correctly scoped (verified against `src/evaluation/metrics.py`'s actual deferred import), and negative-controlled both directions — but a reader of this "READY"-verdicted summary is told a stale count for the unit's second-most-scrutinised test file. | Correct "19 tests" to "22 tests" in the Files-created table, and append a short dated note (mirroring the existing cross-unit-edit-record convention already used elsewhere in this file) recording the `cdc61f7` narrowing and its test-count effect. |

### Coverage limits (this pass did not additionally verify)

- Did not re-derive whether the `sanctioned_deferred_target_sites` narrowing changes any
  of the other 21 tests' pass/fail boundary beyond re-running the suite (which shows
  0 failures) — correctness of the containment-scan logic itself was read, not
  independently re-implemented against a second scan.
- Did not re-verify `tests/test_feature_availability.py` (a `features-and-splits`-owned
  file) beyond running it as instructed by the dispatch (54 passed, 2 skipped — both
  skips are pre-existing `pyyaml`-import skips, not this unit's concern).
- The `iricore`-gated code path and the 26,000-call IRI workload remain genuinely
  unreachable in this environment, as in the prior review.

### Summary

No Critical finding and one Major finding survive this floor-reset pass. The
import-boundary, gate-ordering, carry-forward, trailing-mean, and driver-row-deferral
claims were all independently re-traced against source and re-executed against the real
test suite rather than re-taken from the prior review's word, and all held. The one
Major finding is a stale test-count claim and a missed disclosure opportunity in this
unit's own artifact following a post-review commit to its own owned test file — a
documentation-integrity defect, not a correctness or gate-safety defect: the code
behind the claim is sound, fail-closed, and the actual current count (22/0) is more
favorable than what is claimed, not less. One Major does not, on its own, move this
unit's stage output to NOT-READY.

**Verdict: READY**

## Adversarial re-review (2026-09-13) — against the rejected stage gate

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-13T10:35:01Z
**Iteration:** Adversarial re-review at the REJECTED `code-generation` gate, HEAD `1670ac8`

Re-derived every load-bearing claim from the three 2026-09-13 changes (the 19→22 count
closure, the header commit-state correction, Step 10's withdrawal) against source and git
history directly; nothing here is taken on the artifact's word.

### Verification performed

- **Commit-state header.** `git log -- src/external/iri.py src/external/gim.py` = `ed5808b`
  only; `git log -- scripts/04_build_external_products.py` = `0e002cd, cf3185d, ed5808b`
  (most recent `0e002cd`); `git log -- tests/test_iri_denial.py` = `cdc61f7, ed5808b` (most
  recent `cdc61f7`). All three match the corrected header exactly. Confirmed against
  baseline `1670ac8`.
- **The 22-count closure.** `grep -c "^def test_" tests/test_iri_denial.py` = **22** today;
  `git show ed5808b:tests/test_iri_denial.py | grep -c "^def test_"` = **19** at creation;
  `git show cdc61f7:tests/test_iri_denial.py | grep -c "^def test_"` = **22**. The Files-created
  row (line 46) states 22 correctly. The two historical rows under "Independent verification"
  (2026-09-05 pass, 2026-09-10T11:33:57Z pass) still read "19" — swept for every other site:
  no other representation in this artifact, the plan, or the functional-design/nfr-design
  files asserts "19" as a *current* fact (all other "test_iri_denial.py" hits in
  `nfr-design/*` and `nfr-requirements/*` predate the file's existence and correctly assert
  it did not yet exist at that stage). **Leaving the two historical rows unedited, marked
  historical, is the right call** under `project.md`'s never-edit-a-signed-record correction:
  each is a dated, already-signed verification record of what a specific pass counted on its
  date, and the reader-facing authoritative row (the Files-created table) carries the current
  figure. This is not the `code-generation:fr-2` failure mode (a correction filed only at the
  foot while the body keeps asserting the stale fact) — here the body's own primary table
  was corrected; only the dated historical records were left standing, which is what the
  never-edit-a-signed-record rule asks for.
- **`test_external_drivers.py`: 51 tests**, confirmed by `grep -c "^def test_"` today and at
  `ed5808b`.
- **Step 10 withdrawal's Q5 grounds.** Read `governance/CHANGE_RECORD_2026-09-10_owner_rulings_implementation.md`
  §0 row 1 and §1 directly: both quotations in the withdrawal (`"Q5 = Choice B"`, the
  fails-closed contract description, and the Board-Rec-2 foreclosure of option 1) match the
  source verbatim. `_assert_gate_fails_closed` occurs **12** times in
  `tests/test_external_drivers.py` — one definition (`:789`) and **11 call sites** — confirmed
  by direct grep; read the definition in full: it asserts `returncode != 0` and a specific
  marker-set match on stderr, a genuine fail-closed check, not a loosened one. None of the 11
  call sites pass `--fixture-manifest` (confirmed: zero hits for that string in the file), so
  all 11 are genuine non-fixture invocations already asserting the refusal — **the negative
  control Step 10's item 5 asked for already exists**, exactly as claimed; adding one would
  duplicate it. **Grounds for the withdrawal hold.**
- **The corrected call-site count (11, not nine).** `grep -c "_run_script("
  tests/test_external_drivers.py` = 12, less the definition at `:725` = **11 call sites**,
  matching the withdrawal's own list of line numbers exactly
  (`:839,:862,:877,:889,:985,:999,:1012,:1041,:1065,:1079,:1101`). `--evidence-root` (script
  04, `:197-202`) is confirmed to be a distinct, ordinary input-path option — not
  `--fixture-manifest` (`:251`) — and `_stage_entry` calls `require_receipts_for_snapshot`
  unconditionally regardless of which is passed (confirmed by reading
  `scripts/04_build_external_products.py:277-320` and
  `src/data/fixture_gate.py:683-706`), so all 11, including the two `--evidence-root`
  invocations, do reach the gate. **The "11, not nine" correction itself is right.**
- **The withdrawal's stated REASON for the nine/eleven mismatch is wrong** — see Finding 2
  below. This does not disturb the 11-count's correctness or the CRITICAL finding.
- **The CRITICAL gate finding, independently re-derived link by link:**
  `scripts/run_walking_skeleton.py:184` — confirmed `("04_build_external_products.py", 1)`
  sits in `PHASE1_SEQUENCE`. `build_phase1_commands` (`:513-533`) — confirmed line 529,
  `argv += [FIXTURE_SCOPE_OPTION, str(scope_path)]`, executes unconditionally inside the
  `for script, phase in PHASE1_SEQUENCE` loop, for every script including "04".
  `lifecycle_arguments` (`:487-510`) — confirmed it returns `[]` for any script not prefixed
  `05_`/`06_`/`07_`, so nothing narrows "04"'s invocation. `_declared_data_window()`
  (`04:265-274`) — confirmed it returns a hardcoded `(Jan 1, Dec 31)` of `_AUDIT_YEAR` with no
  CLI-supplied narrowing, and is only engaged (`04:306`) when `fixture_manifest is not None`
  — which, per the chain above, is now always true on the walking-skeleton ladder.
  `assert_declared_window_within_scope` (`src/data/fixture_gate.py:209-251`) — confirmed it
  raises `IntegrityError` unless both declared endpoints lie inside the fixture scope's cited
  window via `assert_records_within_window`. The fixture scopes are `plumbing_7day` (7 days)
  and `scientific_1month` (1 month; both identities confirmed in
  `src/data/fixture_manifest.py:152-155`), and neither can contain a full calendar year.
  **Every link in the chain verifies.** The conclusion follows: on the walking-skeleton
  ladder, "04" is armed with `--fixture-manifest` unconditionally, its declared window is
  always the full year, and the window-scope check always fails — so "04" can never
  complete inside either fixture run, no plumbing-fixture receipt is ever written, and
  **WS-20 and TA-17 are correctly stated as unreachable, not merely `Pending`.** This is a
  real, currently-unremediated Critical against the project's own reproducibility gate
  (G-07) and TE §13.2's seven-invocation clean-run contract, independent of who authored the
  conflicting pieces (board Rec 2 vs. CR-2026-09-07 §6.1) or which unit owns the remedy.
- **IRI/GIM invariants, spot-checked directly**: `grep -rln "iri_" src/features src/models`
  hits only `src/features/build.py`, and reading those hits (`:17,:272,:331,:334`) shows they
  are the denial guard's own refusal logic (`if lowered.startswith("iri_")... raise`), not a
  leaked field. `grep -rn "^\s*from src.external import\|^\s*import src.external" src`
  returns exactly one hit, `src/evaluation/metrics.py:477`, a deferred `gim` import inside a
  function body — matching the claimed single, evaluation-time-only integration point. No
  import of `src.external.iri` exists anywhere in `src/`.
- **Attribution.** `tests/test_determinism.py`, `tests/test_phase_boundary.py`,
  `tests/test_phase_contract.py`, `src/evaluation/guards.py`, and sibling `code-summary.md`
  files appear modified in `git status` but are not referenced anywhere in this unit's
  `code-summary.md` or plan — confirmed no credit or blame is misattributed here.
- **Execution honesty.** No verification in this pass ran a real interpreter; every count
  above is a static `grep`/`git show` derivation, and every test-execution figure quoted from
  the artifact (22/0, 51/0, 664/2) is carried as the artifact's own claim, re-derived here
  only for function counts, not re-executed. Bounded as smoke evidence only, consistent with
  the artifact's own framing.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | `code-generation-plan.md` "Gate finding, raised 2026-09-13" | Independently re-verified and CONFIRMED: `scripts/04_build_external_products.py` cannot pass the walking-skeleton fixture ladder. `run_walking_skeleton.py:529` appends `--fixture-manifest` unconditionally to every `PHASE1_SEQUENCE` script including "04" (`:184`); `lifecycle_arguments` (`:487-510`) does not narrow "04"'s invocation; `_declared_data_window()` (`04:265-274`) returns a hardcoded full-calendar-year window, engaged whenever `fixture_manifest is not None` (`04:306`); `assert_declared_window_within_scope` (`fixture_gate.py:209-251`) refuses unless both endpoints lie inside the fixture scope's window (7 days or 1 month). No remedy has been applied — the owner ruled "record it, rule later" on 2026-09-13, and zero code has moved. As things stand, no plumbing-fixture receipt can ever be written while "04" is in the ladder, so **WS-20 and TA-17 remain unreachable** and `team.md`'s "both fixtures must pass, in order, before any full-year job" cannot currently be satisfied end-to-end. A verified, currently-open Critical against the pipeline's own reproducibility gate blocks READY regardless of how well-scoped the disclosure is. | Owner selects one of the three named remedies (parameterize "04"'s window under a fixture scope with its own D-number; drop "04" from the fixture ladder, which changes what TE §13.2's clean-run contract certifies; or accept "04" cannot participate until (a) lands) before this unit can be re-scored READY. |
| 2 | Major | `code-generation-plan.md` "Step 10 withdrawal", the count-correction paragraph beginning "**Count correction, derived and printed.**" | The stated REASON for the nine-vs-eleven mismatch — *"the nine traces to CR-2026-09-07 §6.2 counting test functions (9 functions, 11 invocations, three functions calling twice or in multi-line form)"* — does not hold. Re-derived directly: `tests/test_external_drivers.py` has had exactly **11 distinct functions**, each calling `_run_script` **exactly once**, at every commit from its creation (`ed5808b`, 2026-09-06) through `17e0767` (2026-09-10) and today — confirmed by re-running the same `awk`-based function/call-site mapping against `git show ed5808b:...` and the working tree, both times yielding the identical 11 function names with no duplicates. There is no function calling `_run_script` twice, at any point in this file's history. `governance/CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md` §6.2 itself says "9 tests via its `_run_script`" against a file that, on the date §6.2 was written (after `ed5808b`, 2026-09-06), already had 11 call sites in 11 functions — so §6.2's "9" was a plain miscount at the time it was written, not a functions-vs-invocations artifact. This does not change the correct headline figure (11, independently confirmed above) or the CRITICAL finding, which stands on its own chain of evidence unrelated to this count. It is exactly the failure mode `project.md`'s count-derivation rule exists to catch — a specific, checkable "why" is asserted with the same confidence as the (correct) "what," in a passage whose entire purpose is to model careful count derivation, and it does not hold up. | Drop the "three functions calling twice or in multi-line form" explanation; state plainly that CR-2026-09-07 §6.2 miscounted at the time it was written (11 call sites existed in the file from its creation, before §6.2 was authored). |

### Coverage limits (this pass did not additionally verify)

- Did not re-execute any test suite; all figures above are static derivations (`grep`,
  `git show`), consistent with "no Python interpreter on this clone" and the standing
  smoke-only bound.
- Did not re-open `component-dependency.md`'s `tests/*` blanket-row discrepancy (owned by
  `inception/application-design`, outside this unit's read scope) beyond confirming this
  artifact discloses it as gate-routed rather than claiming it resolved.
- Did not re-verify the ~10 SD-E-00…SD-E-07 coverage-table rows beyond the prior passes'
  spot-checks; nothing in the 2026-09-13 changes touches that surface.

### Summary

The withdrawal of Step 10 is correctly grounded: Q5 = Choice B is genuinely already
implemented (12 `_assert_gate_fails_closed` sites covering all 11 non-fixture invocations,
none of which pass `--fixture-manifest`), and Step 10's own item-5 negative control would
have duplicated existing coverage. The 19→22 count closure is correct and completely swept;
leaving the two historical verification rows unedited is the right call under the
never-edit-a-signed-record rule. But the newly-raised CRITICAL gate finding is independently
verified true and unremedied — "04" cannot currently complete inside the walking-skeleton
ladder, so the plumbing fixture's receipt can never be written and WS-20/TA-17 are
unreachable — and that alone is sufficient to withhold READY no matter how honestly it is
disclosed. A second, narrower defect survives in the withdrawal's own reasoning: its
explanation for why CR-2026-09-07 counted "nine" is fabricated rather than derived, though it
does not affect the correct 11-count or the CRITICAL finding.

**Verdict: NOT-READY**

## Adversarial re-review (2026-09-13) — iteration 2, TERMINAL (budget exhausted)

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-13T10:41:19Z
**Iteration:** 2 (terminal — this verdict stands as recorded and is what reaches the human gate)

Re-derived, from scratch and independently of the artifact's own text, both items iteration 1
left to verify: the Major's correction and the Critical's chain. Also re-swept counts,
repository state/attribution, and the standing invariants named in the dispatch.

### Verification performed

- **The Major's correction, independently re-derived.** Wrote a function-body-scoped scan of
  `tests/test_external_drivers.py` (tracking indentation via "next top-level `def` closes the
  previous function's scope," since a naive per-`def test_` reset mis-attributes the
  module-level `_run_script` helper definition itself, line 725, to whichever test function
  happened to be open before it — a bug in a first attempt, caught and corrected before
  trusting the result). Corrected scan: **51 test functions total, 11 `_run_script(` call
  sites, each attributed to a distinct function, zero functions calling it more than once** —
  at both `ed5808b` (creation) and HEAD. This independently confirms the artifact's corrected
  text: the withdrawal's replacement explanation ("CR-2026-09-07 §6.2 miscounted at the time
  it was written") is the only claim now standing, the invented "three functions calling
  twice" explanation is gone, and no second wrong derivation was installed in its place.
- **The Critical, independently re-traced link by link, reading each cited line directly**
  (not taking the artifact's line numbers on faith):
  `scripts/run_walking_skeleton.py` — `PHASE1_SEQUENCE` (~line 184) includes
  `("04_build_external_products.py", 1)`; `build_phase1_commands` appends
  `FIXTURE_SCOPE_OPTION` (`--fixture-manifest`) unconditionally inside the `for script, phase
  in PHASE1_SEQUENCE` loop, for every script; `lifecycle_arguments` returns `[]` for any
  script not prefixed `05_`/`06_`/`07_`, so "04" gets no narrowing.
  `scripts/04_build_external_products.py` — `_declared_data_window()` returns a hardcoded
  `(Jan 1, Dec 31)` of `_AUDIT_YEAR` with no CLI-supplied narrowing; `_stage_entry` computes
  `declared_window = _declared_data_window() if fixture_manifest is not None else None` — read
  directly, confirming the window is engaged exactly when a fixture manifest is passed, which
  the ladder now always does for every Phase-1 script.
  `src/data/fixture_gate.py` — `require_receipts_for_snapshot` forwards to
  `require_fixture_receipts`, which calls `assert_declared_window_within_scope` whenever
  `declared_window is not None`; that function raises `IntegrityError` unless both declared
  endpoints lie inside `scope.window`.
  `src/data/fixture_manifest.py` — the only two fixture scopes are `plumbing_7day` (7 days)
  and `scientific_1month` (1 month); neither can contain a full calendar year.
  **Every link verifies independently.** The conclusion holds exactly as stated: "04" is
  armed with the full-year window on every walking-skeleton invocation and the window check
  always fails, so no plumbing-fixture receipt can ever be written and WS-20/TA-17 are
  correctly stated as unreachable rather than merely `Pending`.
- **Counts re-swept.** `tests/test_iri_denial.py`: `grep -c "^def test_"` = **22** today;
  `git show ed5808b:...` = **19** (at creation); `git show cdc61f7:...` = **22** — matches the
  artifact's Files-created row exactly, and the two historical "19" rows remain correctly
  marked as dated historical records rather than current fact. `tests/test_external_drivers.py`
  = **51** `def test_` functions at both `ed5808b` and HEAD, matching every claimed instance.
  No site outside the two marked-historical rows asserts "19" as current, and no "9" appears
  anywhere in the artifact as a current call-site count — every instance of "nine" is inside
  the withdrawn Step 10 text or the correction narrative that supersedes it.
- **Repository state and attribution, re-derived at HEAD `1670ac8`.** `git log --oneline` on
  `src/external/iri.py`/`gim.py` = `ed5808b` only; on `scripts/04_build_external_products.py`
  = `0e002cd, cf3185d, ed5808b` (latest `0e002cd`); on `tests/test_iri_denial.py` =
  `cdc61f7, ed5808b` (latest `cdc61f7`) — all three match the header exactly.
  `git status --porcelain` confirms `tests/test_determinism.py`, `tests/test_phase_boundary.py`,
  `tests/test_phase_contract.py`, `src/evaluation/guards.py`, and several sibling
  `code-summary.md` files (foundation, acquisition, evaluation-and-comparison,
  governance-guards, models-and-baselines, regimes-diagnostics-reporting,
  statistical-inference, target-standardization) are modified in the working tree — none of
  them is referenced anywhere in this unit's own `code-summary.md` or plan, so no credit or
  blame is misattributed to this unit for a sibling's uncommitted diff.
- **Standing invariants, spot-checked directly.** `grep -rn "iri_" src/features src/models`
  hits only `src/features/build.py`'s own denial-guard logic (raises on `iri_*`), not a leaked
  field. `grep -rn "^\s*from src.external import\|^\s*import src.external" src` returns exactly
  one hit, `src/evaluation/metrics.py:477` (`from src.external import gim`, deferred,
  evaluation-time-only) — no import of `src.external.iri` anywhere in `src/`.
  `src/external/spaceweather.py`'s `trailing_mean` docstring and window arithmetic
  (`[end_day-(window_days-1), end_day]`) confirm the trailing-only construction; no `centered`
  implementation exists. No acceptance row (WS-09, WS-10, WS-11, TA-07, TA-36) is claimed
  discharged anywhere in the artifact — the "Nothing discharged" line still lists all five as
  `Pending`.

### Judgment on the disposition (point 3 of the dispatch)

The competing reading — that a fully-disclosed, not-self-caused, not-remediable-within-this-unit
Critical that the decision owner has explicitly deferred becomes a gate item rather than an
artifact defect — is a real and defensible position, and I considered adopting it. I do not
adopt it, for a reason specific to what READY certifies in this framework: READY is not a
statement about this unit's authorial diligence (which is exemplary here — the finding was
self-discovered, fully chained, honestly disclosed, and the owner was given real remedy
options rather than a false one). READY is a statement that "a developer could build from
this without guessing" and, by the chain this artifact's own text draws, that the pipeline's
own reproducibility gate (G-07) and TE §13.2's seven-invocation clean-run contract are
currently satisfiable end-to-end. They are not: the artifact itself proves that no plumbing-
fixture receipt can be written today. Deferring the remedy does not defer the fact — WS-20 and
TA-17 remain genuinely unreachable at this exact moment, not "reachable once the owner rules."
A gate is exactly where the owner's three-way choice belongs; a READY verdict a few lines above
that choice would misstate, to any later reader of this file who does not also read the gate
transcript, that the construction-stage artifact is currently sound end-to-end. It is not —
by its own, independently-verified admission. NOT-READY is therefore the correct record of the
artifact's current state; it is not a verdict on whether the owner handled the finding well
(they did), and it does not imply this unit's own authored code is defective (it is not — no
new finding touches `spaceweather.py`, `iri.py`, `gim.py`, or either owned test file this pass).
It is scoped precisely to the one thing READY asserts that is not yet true: the pipeline can
complete its mandated fixture ladder.

### Disclosure check (point 4)

Confirmed honest and complete: the artifact states unreachability, not `Pending`, in three
places (code-summary.md's own Step-10 correction section, the plan's Step 10 withdrawal, and
the plan's "Gate finding" section); names all three remedies as owner decisions with their
respective costs (a D-numbered scope change, a fixtures-and-reproducibility-owned ladder
change, or indefinite non-participation); and states plainly that "no code moves on it in this
pass." Nothing reads as resolved.

### Coverage limits (this pass did not additionally verify)

- Did not re-execute any test suite (no interpreter on this clone, PyPI egress blocked); every
  figure above is a static `grep`/`git show`/`git log` derivation, per the standing smoke-only
  bound.
- Did not re-open `component-dependency.md`'s `tests/*` blanket-row discrepancy or the ~10
  SD-E-00…SD-E-07 coverage-table rows beyond the prior passes' spot-checks; nothing in this
  iteration's changes touches that surface.

### Summary

Both open items from iteration 1 hold under independent re-derivation: the Major's correction
is right (11 call sites, 11 distinct functions, none calling twice, at both the creation
commit and HEAD), and the Critical is right (the full five-link chain from
`run_walking_skeleton.py`'s unconditional `--fixture-manifest` injection through
`assert_declared_window_within_scope`'s scope-window refusal verifies exactly as stated). The
Critical remains unremedied — the owner deferred the remedy choice, and zero code has moved on
it. Disclosure is honest and complete: unreachability is stated plainly in three places, not
softened to `Pending`, and the deferral is not presented as a resolution. This is a well-run,
exemplary self-review process wrapped around a genuinely open Critical; the process quality
does not convert an unresolved end-to-end reproducibility gap into a closed one. NOT-READY
stands, as the terminal verdict for this budget.

**Verdict: NOT-READY**

## Post-receipt amendment — 2026-09-19 (D-43/D-44/D-45 scientific decisions; `CR-2026-09-19-SCI-DECISIONS`, item 6 of the 2026-09-19 owner authorization)

*Appended under `project.md` `code-generation:gf-3` ("update the owning unit's
code-summary when a repair edits a module that unit owns"). Nothing above is rewritten;
the NOT-READY verdict and its rationale stand as history — this amendment does not touch
the Critical it names, does not change the terminal verdict, and does not claim
readiness. Authority: `evidence/DECISIONS.md` D-43, D-44, D-45; D-43/D-45 are Student +
Supervisor items (TE §18.2 Q-16; TE §18.3 "the IRI role"): supervisor approval REPORTED
by the student 2026-09-19, countersignature artifact PENDING
(`governance/COUNTERSIGNATURE_REQUEST_2026-09-19.md`).*

| Module | What changed (measured, `git diff --numstat` vs `18843aa`) |
|---|---|
| `src/external/spaceweather.py` | +342 / −33 (cumulative this session; this pass's share: the lagged-selection machinery). New: `select_lagged_series` (D-43/D-44 — the single place a safe lag is applied to an interval-valued index: Kp/ap at completion + 3 h, Hp60/ap60 at completion + 1 h, both provider interval boundaries preserved on every row), `assert_lagged_selection` (traceability, no double lag, latest-eligible-interval, no dropped present value), `availability_rows_from_selection`, `daily_medians_from_readings` (D-21/D-22/D-23's project-derived F10.7 daily value; this module owns the driver-product arithmetic, `features-and-splits` owns the enforcement raise — R-54a's allocation, unchanged). `resolve_f107_at_origin` implements D-46's reading B and now returns `F107Selection`, a breaking return-type change from the prior bare tuple. |
| `src/external/iri.py` | +48 / −16. `assert_benchmark_drivers_in_matrix`'s R-59 limb-4 driver-input check replaced per the PREPARED-then-APPLIED D-45 patch (`governance/proposed/P-3_iri_report_confirmations.patch`, applied 2026-09-19 on the recorded decision owner's explicit authorisation after verifying it matches D-45): the old `no_future_centering_confirmed`/`available_at_target_time_confirmed` pair (both `True` required) is replaced by `index_inputs_retrospective_centered` (`True` required — a recorded disclosure, not a false confirmation), a refusal if `no_future_centering_confirmed` is still `True` for a standard-index run, and three new required fields (`index_files_sha256`, `iri_version` must equal 16, `oarr_overrides` must be empty). Module docstring and error text (already corrected 2026-09-19 P-5 for the EV-12 grant status) updated again to state the D-45 status accurately: reported approval, countersignature pending, this patch's application does not itself pass G-04. `generate_benchmark`/R-59 limbs 1–3 unchanged; `iricore` remains uninstalled in the governed environment (see `governance/CHANGE_RECORD_2026-09-19_scientific_decisions_p2.md` §2 for the exhaustive Windows-wheel/build-toolchain diagnosis) so no benchmark can be generated regardless of this patch. |
| `scripts/audit_gfz_drivers.py` | Docstring only (part of the +217/-line design-and-script sweep this session): the `gfz-comparison-report.json` integer-key rationale corrected to state that D-48's structural December detection, not the integer encoding, is what now keeps the file out of custody by validated content and provenance (R-26 class 5). No behaviour change. |

Runs (governed pin, conda `tec-thesis-311`, CPython 3.11.16): `tests/test_external_drivers.py`
(65 tests) and `tests/test_iri_denial.py` (22 tests) green; combined focused run with
`test_feature_availability.py`/`test_locked_test_guard.py` (228 tests total) green, 0
failed. `ruff check`/`ruff format` clean on both touched modules.

**What this amendment does NOT do.** It does not discharge the Critical this unit's
terminal NOT-READY verdict names; does not generate an IRI benchmark (still blocked at
R-59 limb 1: no passing validation report exists, and `iricore` cannot be installed in
this environment — see the pip-failure diagnosis); does not pass G-04; does not create a
producer artifact.

## Post-receipt amendment — 2026-09-19 (2) (D-43 drift guard; Kaggle IRI-2016 verification notebook; `CR-2026-09-19-SCI-DECISIONS-P3`)

*Appended under `project.md` `code-generation:gf-3`. Nothing above is rewritten.
Authority: owner instruction 2026-09-19, items 2 (configuration enforcement) and 3–5
(Kaggle notebook).*

| Module | What changed (measured, `git diff --numstat` vs `18843aa`) |
|---|---|
| `src/external/spaceweather.py` | +367 / −33 (cumulative this session; this pass's share: the drift guard). `assert_lagged_selection` gains `expected_reference_instant`: the function only ever implements `LAG_REFERENCE_INSTANT_INTERVAL_END` (D-43, hardcoded); a caller-declared value that differs is refused rather than silently miscomputed, closing the enforcement loop for `configs/features.yaml`'s `lag_reference_instant` field (D-43's countersignature: reported 2026-09-19 in the prior pass, countersigned 2026-09-19 later the same day — see `evidence/DECISIONS.md` D-43). |
| `kaggle/kaggle_iri2016_verification.ipynb` (new) | Self-contained Kaggle notebook (17 cells) verifying the D-45-selected `iricore` release actually installs and runs on Kaggle's Linux/CPU environment. Selects `iricore==1.8.0` — re-verified exhaustively against PyPI as the newest release with a Linux wheel (1.8.1–1.9.0 publish macOS-arm64 only); detects Kaggle's real Python before installing anything; isolates into a Python-3.10 venv (creating one via `apt-get` if needed) *[superseded 2026-09-19 by the second revision: a three-rung ladder — `virtualenv` against the image `python3.10`, then `uv`-managed CPython 3.10.21, then `apt-get` + stdlib `venv`; rung 1 is what succeeded on Kaggle, see amendment (3) below]* to protect the pinned `numpy==1.26.4`/`fortranformat==2.0.3`/`pymap3d==3.2.0`; installs via `pip --require-hashes` against real PyPI-published SHA-256 hashes; runs one reusable inner verification script (provenance, index-file hashing before/after, a single non-December ARUC-coordinate smoke-test call repeated once for repeatability, reconciliation against the earlier source inspection); packages a diagnostic-only report+logs+hashes bundle under `/kaggle/working`. Stops with a precise diagnosis if Python 3.10 cannot be obtained — no from-source build attempted. |
| `kaggle/HOW_TO_RUN.md` (new) | Upload/settings/run/return instructions, and an explicit list of what this session verified locally (syntax, structure, date-parsing logic against a real index file, the failure-reporting path) versus what remains pending actual Kaggle execution. *[2026-09-19, amendment (3): Kaggle execution is no longer pending — see below.]* |

**Local validation performed (no Kaggle access in this session):** notebook parses as
valid nbformat 4 JSON; every code cell and the embedded inner script parse as valid
Python independently; the inner script's coverage-parsing/date-selection logic was run
against a real `apf107.dat`; the `vtec()` call signature was cross-checked against
`iricore`'s own upstream test suite; the failure-reporting path was executed end to end
locally (with `iricore` genuinely absent) and confirmed to produce a well-formed JSON
diagnosis with exit code 1.

**What this amendment does NOT do.** It does not claim Kaggle execution, a successful
install, or a verified IRI runtime — all of that is explicitly marked pending in
`kaggle/HOW_TO_RUN.md` until the student runs the notebook. It does not discharge this
unit's terminal NOT-READY verdict; does not pass G-04; does not register a producer
artifact or a benchmark result.

## Post-receipt amendment — 2026-09-19 (3) (Kaggle IRI-2016 verification executed — PASS; `CR-2026-09-19-SCI-DECISIONS-P3` §3.6)

*Appended under `project.md` `code-generation:gf-3` and `code-generation:fr-2` (the
stale "pending" claims in amendment (2)'s table are corrected in place above, not only
here). Nothing else above is rewritten.*

**Files changed by this amendment (measured):** none under `src/`, `scripts/`, `tests/`
or `configs/`. `kaggle/kaggle_iri2016_verification.ipynb` is **unchanged** (SHA-256
`b8399c98f248749fca3b6e5acebec9543c262ec0cc83dde2dab0042460d564fa`, frozen as the
producer of the returned evidence). `kaggle/HOW_TO_RUN.md` gains the third/fourth-run
account. New evidence directory `evidence/iri2016_kaggle_verification_2026-09-19/`
(returned zip, its three members, `sha256_manifest.json`, `sha256_manifest_meta.json`,
`RETURN_RECORD.md`).

**What the fourth Kaggle run established** (all values from the returned
`verification_report.json`; runs 1–3 stopped in Step 3 — run 1 a notebook defect since
fixed, runs 2–3 the Kaggle Internet toggle OFF): kernel Python 3.12.13 on glibc 2.35;
`virtualenv` against the image `python3.10` (3.10.12) succeeded at rung 1;
`iricore==1.8.0`, `numpy==1.26.4`, `fortranformat==2.0.3`, `pymap3d==3.2.0` installed
under `--require-hashes`, exit 0; installed `DEFAULT_IRI_VERSION == 20` (explicit
`version=16` remains necessary); `vtec()` at the D-1 ARUC coordinate, `htop=2000`,
`version=16`, on 2024-01-06T12:00Z = `37.373754526924806` TECU, bit-identical on repeat;
shipped `apf107.dat` (`cdf4d5df…`) and `ig_rz.dat` (`fbbed304…`) unchanged after the
calls; `apf107.dat` ends **2024-03-06** — not the 2024-06-17 the earlier `master`-branch
inspection recorded, so the D-45 freeze pins are the 1.8.0 wheel's hashes (proposed D-45
annotation routed to the owner in `CR-…-P3` §3.6; D-45 not edited).

**What this amendment does NOT do.** It does not discharge this unit's terminal
NOT-READY verdict; does not pass G-04; does not touch R-59 limb 1; does not register a
producer artifact, a `permitted_producers` entry or a benchmark result; makes no commit.

## Post-receipt amendment — 2026-09-19 (4) (D-45 annotation; index-file coverage and comparison; notebook revision 3; `CR-2026-09-19-SCI-DECISIONS-P3` §3.7)

*Appended under `project.md` `code-generation:gf-3`. Authority: the owner's instruction of
2026-09-19 approving a dated D-45 annotation subject to evidence checks.*

**Files changed (measured):** none under `src/`, `scripts/`, `tests/` or `configs/`.
`evidence/DECISIONS.md` — annotation block appended under D-45 (original text preserved)
and a pointer in the D-45 summary row. `kaggle/kaggle_iri2016_verification.ipynb` —
**revision 3**, SHA-256 `0e4d4478f256c37737038388b52e2a29960909657ee4fa4672774974911d2a34`,
19 cells; revision 2 (`b8399c98…`, the producer of the returned bundle) preserved
byte-exactly under `evidence/iri2016_kaggle_verification_2026-09-19/`, which also gained
the two installed and two historical index files, `iri_index_checks.py`,
`index_comparison_report.json`, and a 12-file manifest. `kaggle/HOW_TO_RUN.md` — revision-3
section.

**Established (all from the installed wheel bytes, hash-equal to the Kaggle-reported
values):** `apf107.dat` 24,172 contiguous rows 1958-01-01 → 2024-03-06; `ig_rz.dat` updated
2024-03-07, range 1958-01 → 2024-10, 804 values; every row/month/window IRI-2016 reads for
any 2022 target time present and full-window; the historically inspected copies
(`master`@`92c6d8c7`, 1.9.0 sdist) differ only from 2023-09-08 / 2023-09 — **2022 inputs
identical**. `iri.py`'s R-59 confirmations and `src/external/iri.py` are untouched by this
amendment; whether the recorded hashes should also be asserted by that module at run time
is a design question for the unit's next pass, not decided here.

**What this amendment does NOT do.** No 2022 IRI value computed; R-59 limb 1 untouched;
G-04 not passed; no producer artifact, `permitted_producers` entry or benchmark result; no
commit; revision 3 not run on Kaggle. **Repository state (re-verified):** owner commit `60cdabd` (2026-09-19 21:48:35 +0330) captured amendment (3), the D-45 annotation and revision 2 (blob `ba499531…` = `b8399c98…` LF-normalized); everything in this amendment (4), including revision 3, is uncommitted working-tree change at writing time.

## Post-receipt amendment — 2026-09-19 (5) (B-01 production path; `CR-2026-09-19-SCI-DECISIONS-P3` §3.8)

*Appended under `project.md` `code-generation:gf-3`. Authority: the owner's "final preparation"
instruction of 2026-09-19.*

**Files changed (measured, `git diff --numstat` vs `60cdabd`):** `src/external/iri.py`
(+562 / −9 lines, measured: execution contract reader, runtime pin verification before/after a session,
target grid, workload with per-row error capture, R-59 report builder, limb-4 driver rows,
`run_gated_generation`; existing gate functions unchanged; `generate_benchmark`'s terminal
message reworded, contract unchanged); `scripts/04_build_external_products.py` (three
production flags; TE 9.2 receipt gate scoped to full-year jobs and kept on every generation
run; the real attempt path names `BENCHMARK_DRIVER_IDS`); `configs/experiment.yaml`
(`benchmark_b01` block — every value from D-45 as annotated; tolerance TBD for the student);
`tests/test_external_drivers.py` (+14 tests); `tests/test_locked_test_guard.py` (inventory:
two prose files); `pyproject.toml` (`kaggle/*` subprocess-lint posture as `scripts/*`). New:
`kaggle/kaggle_iri2016_benchmark.ipynb`, `kaggle/build_b01_package.py`,
`kaggle/b01_validation_samples.TEMPLATE.json`, `kaggle/dist/tec_b01_package.zip` (build
output). Full suite (junit-counted): 1330 tests, 0 failures, 0 errors, 4 pre-existing skips. **Still NOT-READY / not passed:** this unit's
terminal verdict; G-04; R-59 limb 1 (no passing report exists — the student's samples and
tolerance are the inputs); no producer artifact, `permitted_producers` entry, benchmark
result, commit or push. The B-01 path is implemented and gated, not executed.

## Post-receipt amendment — 2026-09-19 (6) (D-49 interpreter exception; registry transcription; reference-sample sheet; tolerance proposal; custody disposition; `CR-2026-09-19-SCI-DECISIONS-P3` §3.9)

*Appended under `project.md` `code-generation:gf-3`. Authority: the owner's seven-item
instruction of 2026-09-19.*

**Files changed:** `configs/data.yaml` (`stations` transcribed with per-field provenance;
`igrf_version: "IGRF-13"`), `configs/experiment.yaml` (`benchmark_b01.runtime.interpreter_exception`),
`evidence/DECISIONS.md` (D-49; D-1 annotation; D-49 summary row), `src/external/iri.py`
(report samples carry `official_interface_top` / `official_interface_header`),
`tests/test_external_drivers.py` (one precondition fix), `kaggle/build_b01_package.py`
(broader content; `tree_sha256`), `kaggle/kaggle_iri2016_benchmark.ipynb` (fixture step with
a governed 3.11 `uv` environment; `RUN_FULL_YEAR = False`; structural-test labelling),
`kaggle/b01_validation_samples.TEMPLATE.json` (the eight selected cases). New:
`kaggle/b01_official_reference_collection_sheet.md`, `governance/proposed/B01_TOLERANCE_PROPOSAL_2026-09-19.md`,
`evidence/station_registry_sources_2026-09-19/`, `evidence/iri2016_official_reference_2026-09-19/`
(both manifested). Full suite: 1346 tests, 0 failures, 4 pre-existing skips.
**Not done / still blocked:** no official reference value retrieved (interface refused
automation; manual sheet); tolerance not declared (proposal awaiting approval); no fixture
manifest frozen, no receipt; the fixture/B-01 environment-identity coupling unresolved
(D-49 item 4); `observable_codes` absent (features path). G-04 not passed; no producer
artifact; no commit.