# Code Summary — `external-products`

**Unit** `external-products` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`
**Plan**: `code-generation-plan.md` — all 10 steps executed, checkboxes marked. No `git commit` (governance stop). **No IRI benchmark and no GIM comparator generated** — the gate refusals are the deliverable. No December/restricted-root touch; no scientific value decided.

## Files created

| Path | What |
|---|---|
| `src/external/spaceweather.py` | Driver builders/guards: `trailing_mean` (trailing by construction; TC-20 refusal), `resolve_f107_at_origin` (R-57a stop naming origin + staleness), alignment onto the existing `AlignmentError`, `apply_carry_forward` ≤ 3 h + conservation invariant, time-indexed/identical-across-cells refusals (TC-12), single-grade + eligibility (D-10.1/TC-11), four provenance fields + bounded reanalysed-value check (declared-status-only, never closed), `provenance_stamp` (evidentiary), `write_driver_manifest` (two-tier, `guard_egress`), `refuse_divergent_rerun` (SD-E-07, SEC-A-02 adopted) |
| `src/external/iri.py` | R-59's four limbs: refuses without a passing **pre-declared** validation report; tolerance timestamp must precede comparison; field-by-field report assertion (2000 km, 5–10 official-interface samples, no-future-centering); never silently switched; D-25 carried AS STANDING (amendment not treated as granted); `iricore` import inside the gated path only |
| `src/external/gim.py` | Q-15 refusal (rule UNSET, no default); hand-check + overlap-audit timestamps must precede generation; map-to-map + spatial-mismatch statements emitted by the reporting path itself; comparison with no registered `gim_network_overlap_flag` fails; outside-tuning residual named open |
| `scripts/04_build_external_products.py` | Position 04; six-step entry; `audit_ec1_drivers.py` logic migrated in — the `:184` unconditional `return 0` closed onto the two-tier posture (missing months = machine-readable field naming WHICH months, non-fatal; hash mismatch vs recorded `ec1-audit-report.json` hashes terminates naming file + expectation); registry rows via foundation's writer; `--attempt-benchmark`/`--attempt-comparator`/`--gate-state`/`--render-comparison` paths; original script untouched |
| `tests/test_iri_denial.py` | §12-mandated, **19 tests** — ordered switch (`failed` outranks; unresolved edge → skipped w/ edge; both limbs populated → `passed`; empty limb → `skipped` naming which, JSON-structured reason); complement-defined candidate set over `.py` + ast-parsed `.ipynb` cells; `__init__.py` walked/count-subtracted; transitive; content limb (`iri_*` name fails; **absent provenance fails**). Negative controls: injected field/direct import/transitive import/stripped stamp all caught |
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
