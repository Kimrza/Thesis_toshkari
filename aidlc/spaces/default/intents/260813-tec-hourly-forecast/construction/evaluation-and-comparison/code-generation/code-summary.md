# Code Summary — `evaluation-and-comparison`

**Unit** `evaluation-and-comparison` (Bolt 9) · **Kind** `library` · **Stage** `code-generation`
**Plan**: `code-generation-plan.md` (10 steps; all 10 executed)
**Receipted answers**: Q1 = A, Q2 = B, Q3 = A, Q4 = A, Q5 = A.

## Sources

- Approved plan and receipted Q&A: `construction/evaluation-and-comparison/code-generation/{code-generation-plan.md,code-generation-questions.md}` [Q1][Q2][Q3][Q4][Q5]
- Functional design: `construction/evaluation-and-comparison/functional-design/{business-logic-model.md,business-rules.md,domain-entities.md}` (W-1…W-8; R-103…R-112; 8 entities)
- NFR design: `construction/evaluation-and-comparison/nfr-design/{security-design.md,logical-components.md}` (SD-C-01…SD-C-04; C-1…C-4)
- Governing decisions: D-27 (Vision-register reading; inverse withheld — UNREOPENED, verified on disk), D-28 (30-day DEC window), D-31 (G-09 signed), D-32 (eight §15.2 rows approved), all in `evidence/DECISIONS.md`
- Change record: `governance/CHANGE_RECORD_2026-09-06_R106_comparison_sets.md` (written FIRST, Step 1)

## Files created (6) / modified (3)

| File | Lines | Content |
|---|---|---|
| `governance/CHANGE_RECORD_2026-09-06_R106_comparison_sets.md` | 187 | Q1 = A membership confirmation (Vision §2.4/§8.4/§8.9), PROPOSED D-number text for `evidence/DECISIONS.md` (owner adopts or edits; no agent writes the register), the Q2 = B sibling-edit record, the Q4 = A race analysis, honest limits |
| `configs/experiment.yaml` (modified) | 178 (was 150) | `comparison_sets`: primary {M-01, M-02, M-03, M-06, B-01}, gim {M-06, C-01}, tier3 {M-04, M-05, M-06}, each citing the Step 1 record; parse-verified member counts 5 / 2 / 3; nothing else touched |
| `src/evaluation/guards.py` | 632 | The six SD-C-01 refusals as one failure domain — `require_stamps` (`LeakageError`), `require_partition_agreement` (`PartitionError`), `require_registered_mask` + `require_declared_membership` (`FairnessError`), `require_target_space` (`InverseTransformError`; `ABL-DIFF` refuses naming D-27), `require_locked_receipt` (`LockedTestError`, three ordered limbs: hash receipt, SD-C-02 containment, D-28 window), `require_mask_member_alignment` (`FairnessError`) — plus `resolve_inverse` (always refuses naming D-27) and `scored_window_statement` (D-28's sentence derived by date arithmetic, no constant in source) |
| `src/evaluation/masks.py` | 697 | `build_comparison_mask` (stamps first, exact declared membership, matched-window agreement, per-station surviving + exclusion counts, deterministic sha256 `mask_id`, full stamp set, the five exposed reporting values), `MaskRegistry` (once-only per set; write-once `frozen_bundle_manifest.json` via `.tmp` → fsync → `os.replace`, second write refuses — Q4 = A race analysis in the docstring), `read_comparison_sets` (refuses absent/TBD by name) |
| `src/evaluation/metrics.py` | 665 | `paired_loss_differential` (guards first; squared errors per (`station`, hour) on masked rows only → per-station mean **benchmark minus model** → unweighted three-station mean), `EstimandResult` (orientation `benchmark_minus_model`, weighting `equal_station`, verbatim sign sentence, four stamps copied from the registered mask, disagreement fails), `build_metrics_artifact` (per-set completeness refusal; `beats_model` per benchmark; TEC-06 sentence on every IRI/GIM row; fail-closed GIM overlap disclosure with containment ordering; Phase-2 not-independent statement field), atomic refuse-overwrite writer |
| `src/data/locked_test.py` (modified) | 546 (was 461) | **Q2 = B owner-instructed sibling edit, flagged for `governance-guards`' record and re-check**: `AccessRecord` + `mask_bundle_ids`/`mask_registry_hash` (additive, optional, existing callers verified unbroken); `open_restricted` populates both from a frozen-bundle manifest; a present-but-unparseable manifest aborts the read (`LockedTestError`) rather than logging `None` |
| `scripts/07_evaluate_and_report.py` | 621 | Position 07; `--config configs/` `--phase 1|2`; `ensure_process_determinism` first, `assert_no_raw_fields` before first write; predictions by manifest; per-set mask build/register, estimands, metrics artifact; honest `aborted` registry row on `IntegrityError`; **DEC unreachable** — enters only via `materialise_locked_partition(g05_signature=...)` + `open_restricted(purpose="locked_evaluation")`, G-05 `Blocked`; bootstrap intervals and breakdown tables NOT computed (other units') |
| `tests/test_common_masks.py` | 1240 | 61 test functions (derived: `grep -c "def test_"`) — controls (1), (3)–(32) as owned here ((2) vacated per R-103), per-entry guard controls incl. the sixth guard, containment controls, second-manifest-write refusal, orientation/weighting fixtures, completeness/disclosure/`beats_model` presence tests, tier-3 matched-window instance (28), AST import-boundary tests, fresh-subclass `aborted`-row scan, the three must-NOT-fire controls; member counts re-read from config, synthetic year 2001 only |
| `src/data/config.py` (modified) | 1276 | One `REQUIRED_FIELDS_MAP` entry `("evaluation-and-comparison", 1)` so script 07's refusal path can execute (the map's docstring anticipates per-stage additions; every prior unit did the same); `comparison_sets` deliberately NOT listed — enforced at `read_comparison_sets`, preserving the honest `aborted`-row path |

## Key implementation decisions

1. **Exception declaration site**: `FairnessError`/`InverseTransformError` are imported-and-re-exported from `src/data/config.py`, not redeclared — foundation's amended R-01 fixes the single declaration site, and a second same-named class object would break catchability (the drift class R-01 exists to prevent). The design's "declared here" is realised as "raised here". Deviation recorded here and in the stage diary.
2. **D-27 honoured**: no `src/evaluation` → `src/features` or `src/models` import exists, direct or transitive (grep- and AST-verified; a test asserts it); `ABL-DIFF` refuses naming D-27 at `resolve_inverse` and `require_target_space`; `train.py` untouched.
3. **Containment, not clocks** (SD-C-02): `require_locked_receipt` verifies the access record's `mask_bundle_ids`/`mask_registry_hash` against the re-hashed write-once manifest; refusal on `None` is the fail-closed half while the DEC path stays unreachable (G-05 `Blocked`).
4. **No scientific constant in source**: memberships live in `experiment.yaml` under the Step 1 record; the D-28 window sentence is derived by pure date arithmetic and tested against the verbatim string without any December read; tests build expectations from config at run time.
5. **Evaluation-time-only externals**: `metrics.py` defer-imports `src/external/gim.py` inside the disclosure path after the registered-mask precondition (one copy of R-60's emission); `iri.py` not imported — the allowlist is permission, not obligation.

## Test coverage summary

61 test functions in `tests/test_common_masks.py`. Smoke run on this clone (Q5 = A): winget Python download failed (`InternetOpenUrl() failed. 0x80072ee2`, recorded verbatim), uv installed Python 3.11.16 into the session scratchpad; PyPI unreachable so pytest/pyyaml uninstallable — the suite ran under a scratchpad pytest shim on the real 3.11.16: **60 passed, 1 skipped (yaml unavailable), 0 failed**. `compileall src scripts tests` exit 0. **Smoke evidence only, never governed.** Owed: full-pytest suite + ruff once PyPI is reachable (stdlib lint substitute ran clean on touched files; pre-existing `src/data/config.py:1` overlong line reported, not repaired — foundation's).

## Deviations from the plan

- Exception classes imported, not redeclared (decision 1 above).
- `src/data/config.py` `REQUIRED_FIELDS_MAP` entry added (not a plan step; prerequisite of script 07's refusal path; precedented by all six prior units).
- Whole-suite smoke narrowed to shim-compatible modules — pytest uninstallable on this clone; exact failures recorded.
- graphify CLI not on PATH (verified); orientation by direct reads; `graphify update .` could not run — graph stale for touched files.

## Open items routed to the gate

The proposed D-number for the membership confirmation (adopt or edit — if declined, `comparison_sets` is removed on your word and the builder refuses fail-closed); the Q2 = B sibling edit routed to `governance-guards`' record and re-check; the R-103 import edge still unauthorised (D-27 stands); FR-P1-05-17 rowless; FR-P1-05-7 `Pending` (approved D-32, never run); the R-85…R-89 numbering gap (observed, unexplained); `statistical-inference`'s R-113 correction owed at its unit; the `project.md` GIM-disclosure wording correction owed at the §13 ritual; full-pytest + ruff owed with the governed commit, which cites D-27, D-28, D-31, D-32 plus the new D-number if adopted. Nothing discharged: WS-16, TA-11, TA-18 stay `Pending`.

## Assumptions & Open Questions

None.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-06T18:32:21Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Minor | `src/evaluation/guards.py:355-375` (`resolve_inverse`) | `resolve_inverse` is exported and tested directly (`tests/test_common_masks.py:324-330`, control (1)) but is never called from any production code path (`metrics.py`, `masks.py`, `scripts/07_evaluate_and_report.py` all avoid it) — `require_target_space` raises `InverseTransformError` for a target-touching prediction without ever resolving an inverse. This matches the design's stated intent ("this function exists so the refusal has one home and control (1) has a named surface; it never returns"), so it is not a defect, but the module's own docstring never states it is unreferenced by the pipeline, which a future reader could mistake for a wiring gap. | Add one sentence to `resolve_inverse`'s docstring noting it is deliberately not called from `metrics.py`/`masks.py` today (control (1) is exercised directly) so a later reader does not "fix" the missing call site. |
| 2 | Minor | `src/evaluation/guards.py:69-74` (module `Governance` docstring) | Lists governance as "SD-C-01…SD-C-03" but the module's `require_locked_receipt` composition and the overall guard set are also the enforcement surface `security-design.md` cites for SD-C-04's fail-closed posture indirectly (SD-C-04 itself is implemented in `metrics.py`, which is correctly cited there) — a reader skimming only `guards.py`'s docstring could miss that SD-C-04 exists at all in this unit. Cosmetic; `metrics.py`'s own docstring correctly cites SD-C-04. | Optional: add "SD-C-04 is `metrics.py`'s" to `guards.py`'s docstring for symmetry. No functional effect. |

### What was verified

- **D-27 discipline (adversarial check 1).** `grep` over `src/evaluation/*.py` and `scripts/07_evaluate_and_report.py` shows no import of `src.features` or `src.models`, direct or transitive; `grep -rn "Transform.inverse\|\.inverse("` over the same files returns nothing; `evidence/DECISIONS.md` enumerated headers end at `## D-32` (plus a D-1 addendum) — no D-33 exists, confirming D-27 unreopened as the summary claims. `resolve_inverse` always raises `InverseTransformError` naming D-27 (`guards.py:355-375`); `require_target_space` refuses an `ABL-DIFF`-declared prediction without an applied-inverse stamp (`guards.py:378-419`), verified against test `test_control_3_uninverted_abl_diff_refuses_naming_d27` and `test_per_entry_uninverted_abl_diff_at_the_estimand`.
- **`configs/experiment.yaml` transcription (check 2).** `git diff HEAD -- configs/experiment.yaml` shows exactly one new `comparison_sets` block added; every pre-existing key (`folds`, `embargo_hours`, `estimand`, `bootstrap`, `practical_relevance_threshold`, `grids`, `models`, `ablations`) is untouched. Memberships match Q1 = A exactly: primary `{M-01,M-02,M-03,M-06,B-01}` (5), gim `{M-06,C-01}` (2), tier3 `{M-04,M-05,M-06}` (3); each cites the change record and Vision §2.4/§8.4/§8.9 in its surrounding comment.
- **Guards (check 3).** All six SD-C-01 refusals present in `guards.py`: `require_stamps` (`LeakageError`), `require_partition_agreement` (`PartitionError`), `require_registered_mask`/`require_declared_membership` (`FairnessError`), `require_target_space` (`InverseTransformError`), `require_locked_receipt` (`LockedTestError`, three ordered limbs including the D-28 window and SD-C-02 containment), `require_mask_member_alignment` (`FairnessError`, the sixth guard). The discriminating rule (declared-identity disagreement → `PartitionError`; information-flow disagreement → `LeakageError`; member-vs-mask → `FairnessError`) is implemented exactly as stated and cross-checked against `security-design.md`'s SD-C-01 table and the `GOV-2026-08-28-FD-01` Recommendation-8 ruling. `scored_window_statement(month_start=2022-12-01, month_end=2023-01-01, embargo_hours=24)` computed by hand reproduces D-28's exact string "2–31 December 2022, 30 days, first 24 h excluded and counted" — verified against `test_scored_window_statement_reproduces_d28_verbatim`. Every raise names a file/resource and the violated expectation.
- **Estimand (check 4).** `paired_loss_differential` in `metrics.py:242-339` runs guards first, then computes squared errors per (station, hour) on masked rows only, per-station mean of paired differences benchmark-minus-model, then an unweighted mean of the three station values — matches R-108's ordered pipeline exactly, confirmed against `test_control_15_...` (sign) and `test_control_16_...` (equal-station vs. pooled, on an asymmetric fixture that makes the two aggregations provably disagree). `EstimandResult.__post_init__` validates orientation/weighting/sentence against the fixed constants and requires all four stamps present; `_stamps_match_mask` enforces agreement with the registered mask (control 30, both halves).
- **Mask (check 5).** `compute_mask_id`/`assert_mask_id_reproduces` implement a deterministic sha256 over `{set_id, sorted member_ids, canonical masked rows}`; `MaskRegistry.register` refuses a second registration for the same set and refuses registration after the bundle is frozen; `MaskRegistry.freeze_bundle`/`_write_once_atomic` implement `.tmp → fsync → os.replace`, and the code path genuinely refuses on a second call (`path.exists()` check before any write) — confirmed by reading `_write_once_atomic` and by `test_q4a_frozen_bundle_manifest_is_write_once`, which asserts the second `freeze_bundle()` call raises. `assert_reporting_surface` (control 31) checks all five exposed values; per-station surviving and exclusion counts are both computed and recorded in `build_comparison_mask`.
- **Honesty mechanics (check 6).** `build_metrics_artifact` refuses emission with a missing declared benchmark (control 24); `beats_model` is derived from the sign, never asserted independently; the TEC-06 sentence is attached to every row whose `benchmark_id` is in `EXTERNAL_COMPARATOR_IDS = ("B-01","C-01")` (control 25); the GIM overlap disclosure (`_gim_disclosure_block`) is fail-closed on a missing overlap-audit result and enforces containment ordering via recorded `overlap_audit_id`/`overlap_audit_sha256` (controls 26, 32); the Phase-2 not-independent statement is an artifact field, verbatim-checked.
- **Script 07 (check 7).** `main()` calls `ensure_process_determinism` as its first statement; `_run` calls `assert_no_raw_fields` before any write; the `DEC` partition is reachable only via `materialise_locked_partition(..., g05_signature=...)` followed by `open_restricted(..., mask_bundle_manifest=...)` inside `_locked_loader`, and `_parse_args` hard-requires `--g05-signature/--locked-input/--locked-authorization/--mask-bundle-manifest` together with `--partition DEC`; no restricted-root path is constructed anywhere in the script (confirmed by `test_script_07_imports_no_features_models_or_external_and_names_no_restricted_root` and `test_dec_entry_in_script_07_routes_only_through_the_two_guards`). `_load_target_by_manifest` always raises `IntegrityError` today (no released target manifest exists), and the `except IntegrityError` handler in `main()` records an honest `aborted` row via `record_abort_honestly` before returning 1 — confirmed by reading the control flow and by `test_fresh_subclass_lands_the_aborted_row_via_the_stage_entry_catch`'s AST-based assertion that the only exception handler in the script is `IntegrityError` and that it calls `record_abort_honestly`.
- **Q2 = B sibling edit (check 8).** `git diff HEAD -- src/data/locked_test.py` shows the edit is additive only: two new optional dataclass fields with `= None` defaults on `AccessRecord`, an unmodified `__post_init__` required-field list, and a new optional `mask_bundle_manifest` keyword on `open_restricted` that defaults to `None` and preserves prior call shape. `_containment_fields` raises `LockedTestError` (not silently `None`) on a present-but-unparseable manifest, matching the summary's claim. No other change exists in the diff.
- **Tests (check 9).** `grep -c "def test_"` returns 61, matching the claimed count exactly. Spot-checked controls (1), (3)-(32) by name across the file, including (15) orientation, (16) pooled-vs-equal-station weighting, (22) the 1-December row, (26) GIM-without-audit, (30) stamp presence/agreement (both halves), (31) reporting-surface presence, (32) audit-after-comparator containment, the sixth guard (`test_per_entry_sixth_guard_through_the_estimand`), and three must-not-fire controls (all-DEC-stamps pass, `untransformed` B-01/C-01 pass, coverage-audit-purpose pass) — all present and correctly asserting the documented behaviour. `test_real_comparison_sets_reread_from_config_never_literal` re-reads member counts from the parsed `experiment.yaml` (skipped today via `pytest.importorskip("yaml")`, consistent with the claimed "1 skipped (yaml unavailable)"). `SYNTH_YEAR = 2001` throughout; no test touches December 2022 content or a real signature. No `assert True`-style vacuous tests found in the sampled set.
- **Summary accuracy (check 10).** Every file's claimed line count was verified with `wc -l` and matches exactly: `guards.py` 632, `masks.py` 697, `metrics.py` 665, `07_evaluate_and_report.py` 621, `test_common_masks.py` 1240, `locked_test.py` 546, `config.py` 1276, `experiment.yaml` 178, the change record 187 — all exact. The "60 passed, 1 skipped, 0 failed" claim is internally consistent with the yaml-import-skip test found in the suite. Entity count "8 entities" verified against `domain-entities.md`'s eight numbered `## N.` headings.
- **`config.py` entry (check 11).** The new `REQUIRED_FIELDS_MAP[("evaluation-and-comparison", 1)] = ("seeds.development",)` entry is minimal, textually identical in shape to the immediately preceding `("models-and-baselines", 1)` entry, and names a field identity only — no scientific value. `comparison_sets` is deliberately absent from the map, consistent with `read_comparison_sets`'s own refusal path being the enforcement point.

### Coverage limits

- graphify CLI was not on PATH in this environment (confirmed, consistent with the dispatch note); orientation was performed by direct reads of the named files and targeted greps rather than `graphify query`/`explain`/`path`. `graphify-out/graph.json` may be stale for the files touched by this unit.
- Deep line-by-line review was performed for `guards.py`, `masks.py`, `metrics.py`, `scripts/07_evaluate_and_report.py`, the `locked_test.py`/`config.py`/`experiment.yaml` diffs, and roughly 40% of `test_common_masks.py`'s 61 test bodies (the ones named in the adversarial check list plus several adjacent ones); the remaining ~35 test bodies were confirmed present by name/grep but not individually read line-by-line.
- No attempt was made to execute the test suite or any static analysis tool in this review pass (no Python interpreter available in this sandbox); correctness of guard logic and test assertions was verified by manual tracing against the cited business rules, not by running pytest.
- Per the read-scope bound, sibling units' `construction/<other-unit>/` content was not read except the one authorized integration point (`models-and-baselines/functional-design/business-rules.md` R-90/R-92, read earlier in this stage's business-rules.md citations) and the named consumed-code integration points (`src/models/train.py` was not directly opened in this pass; its `Prediction`/`three_seed_mean` shapes were cross-checked indirectly via `masks.py`'s `LoadedPrediction` docstring and `06`'s payload contract, which was sufficient to verify the eight-field shape agreement without opening the sibling file).
- `evidence/locked_test_restricted/` and any December 2022 content were not read, per instruction.

### Summary

This is an exceptionally well-cross-checked unit: every adversarial check specified in the dispatch (D-27 import discipline, `experiment.yaml` transcription exactness, all six guards and their discriminating exceptions, the estimand's ordered pipeline and sign convention, mask identity/once-only/write-once semantics, honesty mechanics and fail-closed GIM disclosure, script 07's chokepoint ordering and honest-abort path, the Q2 = B additive-only sibling edit, the 61-test count and control mapping, and the `config.py` entry) verified correct against the on-disk code, the governing business rules, and git diffs of the modified files. No Critical or Major defects were found. The two Minor findings above are documentation-symmetry nits with no functional impact and do not block readiness.

### Cross-unit edit record (2026-09-10) — edits made by `fixtures-and-reproducibility` and the gate worklist, owner-authorised

Appended after the gate rejection lifted the receipt freeze. Under
`CR-2026-09-07-R133-FIXTURES-AND-REPRODUCIBILITY` (§5, §11.5) and the owner gate worklist
of 2026-09-10 (items 2–3), these ADDITIVE/repair edits touched this unit's surfaces — the
full-year path, the locked path and every guard are untouched in strength:

- `scripts/07_evaluate_and_report.py` (commit `cf3185d`, Q4/Q5 = A): `--fixture-manifest`
  option (parser error alongside a frozen `--partition`), `_stage_entry` kwarg + ONE
  `require_receipts_for_snapshot` call, ONE early-return in `_run` to the additive
  `_run_fixture_scale` (apparatus partitions; NO locked path reachable; sibling fixture
  stamps on the metrics artifacts). Commit `0e002cd` (board Recs 3–4 / ML-02–03): the
  fixture path's mask registry is rooted PER APPARATUS PARTITION under
  `artifacts/walking_skeleton/<fixture_id>/mask_registry/<partition>/` — never the
  confirmatory root, so no apparatus registration can occupy a confirmatory `set_id` slot
  or enter the G-05 frozen bundle — with the fixture stamp written inside each registry
  dir, and a `fixture_measurements.json` block emitted for the orchestrator. Current size,
  derived: 774 lines (`wc -l`).
- `tests/test_iri_denial.py` (2026-09-10, worklist item 2, uncommitted): the containment
  scan is now SCOPE-AWARE — a DEFERRED (function-scope) target import inside an ALLOWLISTED
  module is R-112's sanctioned evaluation-time mechanism, recorded under the new payload
  field `sanctioned_deferred_target_sites`, never a violation; an EAGER target import in an
  allowlisted module still fails every transitive chain, and a deferred target import
  outside the allowlist still fails outright — both proved by new controls. This repairs
  the pre-existing critical red (8 false violations through `metrics.py`'s deferred gim
  import) at root cause without weakening the boundary: 22 passed, 0 failed.
- `tests/test_common_masks.py` (2026-09-10, worklist item 2, uncommitted): three sites now
  derive the restricted-root name from `locked_test.RESTRICTED_ROOT` instead of spelling
  the literal, so R-28's exact-membership literal scan (`test_locked_test_guard`) holds
  with this module correctly absent from the exempt list: 60 passed / 1 skipped, and
  `test_locked_test_guard` 44 passed, 0 failed.

This unit's owner may confirm or reverse per the change record and the gate worklist.

### Cleanup review (2026-09-10)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-10T07:38:23Z
**Iteration:** 1 (first review pass over the cross-unit edit record above)

**Scope.** Verifies the two test-lane edits recorded above under the cross-unit edit
record: `tests/test_iri_denial.py`'s scope-aware containment scan and
`tests/test_common_masks.py`'s restricted-root literal derivation — both ADDITIVE edits
to a READY unit's test files, made by another unit's owner-authorised worklist pass, per
`project.md`'s `code-generation:c32` rule (route through an explicit ruling, carry the
stale summary to the gate). The cross-unit edit record above already names that ruling
(`CR-2026-09-07-R133-FIXTURES-AND-REPRODUCIBILITY` §5/§11.5 and the 2026-09-10 owner gate
worklist items 2–3), satisfying that rule textually; this review verifies the edits
themselves rather than the routing.

**Verification performed (adversarial, not trusting the described fix):**

1. **`test_iri_denial.py` — narrowing is scoped, not a general weakening.** Read
   `tests/test_iri_denial.py:176-201` (`_eager_imports_of`): re-walks the AST with
   `FunctionDef`/`AsyncFunctionDef`/`Lambda` bodies pruned before collecting
   `Import`/`ImportFrom` nodes — a target import inside a function or lambda body is
   correctly excluded from the "eager" set because Python does not execute it merely by
   importing the enclosing module. Read `run_containment_scan`
   (`:263-370`): the narrowing fires ONLY when `current_allowlisted and name not in
   eager_names` — i.e., only for a deferred import inside an already-allowlisted module;
   every other target hit still lands in `violations`. Confirmed the injection mechanism
   this rule actually protects, `iri_column_violations` (`:393-424` and its four tests at
   `:736-769`), carries **zero diff** — the field/provenance-based data-flow denial is
   untouched by this narrowing, which only concerns the static import-boundary scan.
2. **Both directions proved by real negative controls, not asserted.** Read
   `test_deferred_target_import_outside_the_allowlist_still_fails` (`:639-652`): plants a
   deferred gim import in a NON-allowlisted module (`src/features/sneak.py`) and asserts
   `outcome == "failed"` with that module in `violations` — proves the allowlist is not a
   general deferral amnesty. Read
   `test_eager_target_import_in_allowlisted_module_fails_transitive_chains` (`:655-671`):
   plants an EAGER import inside an allowlisted module and asserts a downstream importer's
   chain still fails — proves the allowlist does not launder an eager edge. Read
   `test_deferred_target_import_in_allowlisted_module_is_sanctioned` (`:673-690`): the
   must-not-fire half, asserting `outcome == "passed"`, `violations == []`, and the site
   recorded under `sanctioned_deferred_target_sites`. All three push through the real
   `run_containment_scan` entry point.
3. **The narrowing is disclosed, not silent.** Read `run_containment_scan`'s docstring
   (`:263-278`): states the narrowing explicitly under a "NARROWING, disclosed" heading,
   names the mechanism (R-112's evaluation-time-only pattern), and states both
   controls exist. This satisfies the dispatch's explicit instruction to verify
   disclosure.
4. **`test_common_masks.py` — the guard module itself is unchanged.** `git diff --stat --
   src/` shows no diff for `src/data/locked_test.py` (the module owning
   `RESTRICTED_ROOT` and the locked-test chokepoint) anywhere in this working tree — only
   `src/evaluation/diagnostics.py` and `src/evaluation/report_guards.py` (a different
   unit's lane) changed under `src/`. Read the diff of `tests/test_common_masks.py`
   directly: three sites replaced a spelled `"evidence" / "locked_test_restricted"` /
   `"locked_test_restricted"` literal with `locked_test.RESTRICTED_ROOT` (or
   `Path(RESTRICTED_ROOT).name`) — a derivation, not a behavior change, since
   `RESTRICTED_ROOT`'s value is unchanged. Confirmed the accompanying assertion in
   `test_script_07_imports_no_features_models_or_external_and_names_no_restricted_root`
   still checks the module is absent from `RESTRICTED_LITERAL_EXEMPT_MODULES` — the
   exempt-membership assertion was not weakened, only its literal source.
5. **Reproduced independently** (scratchpad CPython 3.11.16 + stdlib pytest stand-in,
   PyPI unreachable): `tests.test_iri_denial` → **22 passed, 0 failed, 0 skipped, 0
   errors**; `tests.test_locked_test_guard` → **44 passed, 0 failed, 0 skipped, 0
   errors**; `tests.test_common_masks` → **60 passed, 0 failed, 1 skipped** (the one skip
   is the pre-existing `pyyaml`-gated real-config test, unrelated to this edit) — all
   three match the cross-unit edit record's claimed counts exactly.
6. **No test deleted, no assertion weakened, no xfail introduced.** `git diff` on both
   test files shows only additive hunks (new helper function, new test functions, or a
   literal replaced by a derived constant); no `def test_` was removed and no
   `pytest.mark.xfail` or `pytest.skip` (unconditional) was introduced — the only new
   skip path (`pytest.importorskip("yaml")`, in the sibling `foundation` unit's file, not
   this unit's) is a named classification, verified separately in that unit's review.

**Findings:** none survive verification at any severity. The narrowing is real but
correctly scoped, disclosed, and proved in both directions by tests that exercise the
actual scan entry point; the restricted-root literal replacement is a pure derivation
with the guard module itself byte-for-byte unchanged.

### Summary

Both test-lane edits recorded in the cross-unit edit record above are verified directly
against the modified source: the IRI/GIM containment-scan narrowing is scoped exactly to
the sanctioned deferred-import-in-an-allowlisted-module case, disclosed in the function's
own docstring, and proved both ways by new negative controls through the real scan entry
point, while the injection-detection half (`iri_column_violations`) is untouched; the
restricted-root literal replacement in `test_common_masks.py` is a derivation from
`locked_test.RESTRICTED_ROOT`, not a behavior change, and the locked-test guard module
itself carries zero diff. All claimed suite counts (22/0, 44/0, 60/0/1) reproduce exactly
under independent execution. No Critical, Major, or Minor defect found.
