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

### Gate-floor re-review (2026-09-10)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-10T14:33:47Z
**Iteration:** 1 (fresh verdict after gate-rejection reset the review floor; re-derived
against current HEAD `f0d9e49` plus the uncommitted sibling `acquisition` repair, which
touches no file this unit owns)

**Scope and posture.** Adversarial re-derivation, not a rubber-stamp of the prior
verdicts above. Re-verified repo-wide config state (D-33…D-38), this unit's specific
exposure points named in the dispatch (IRI/GIM boundary, comparison-wide mask, difficulty
controls, the two owner-ruled cross-unit edits, freeze_bundle/apparatus containment), and
executed this unit's tests plus `test_iri_denial.py` independently rather than trusting
the counts already on record.

**Repo-wide state verified first, per dispatch:**
- `configs/features.yaml`: the seven driver rows (`kp_safe`, `ap_safe`, `hp60_safe`,
  `ap60_safe`, `f107_safe`, `f107_81_trailing`, `dst`) are absent — confirmed by direct
  grep, only a comment at line 50 names them as deliberately excluded; `dst` is not
  present as a feature row anywhere in the file.
- `configs/experiment.yaml:26`: `embargo_hours: 24 # D-38 (2026-09-10)` — confirmed.
  `configs/experiment.yaml:275`: `practical_relevance_threshold: "TBD — freeze gate" # D-34:
  DECIDED — no threshold approved` — confirmed as the decided sentinel, not an omission.
- `configs/data.yaml:58`: `cell_rule: "floor-half-open-d1" # D-33 (2026-09-10)` and
  `stations: "TBD — freeze gate"` (line 45, unchanged) — confirmed; a six-entry
  `partitions:` block starting at line 78 (F1…F4, DEC, plus the sixth) — confirmed present.
- `evidence/DECISIONS.md`: `grep -n "^## D-"` shows the register ends at `## D-38`
  (`## D-1 addendum` follows as a countersignature note, not a new decision) — confirmed,
  no decision beyond D-38 exists. D-37 reaffirms D-27; D-38 is the split-configuration
  transcription the dispatch names.

**This unit's specific exposure, verified against code (not description):**
1. **IRI/GIM evaluation-time-only boundary.** `src/evaluation/metrics.py:477`
   (`from src.external import gim`) is the only external-comparator import in this unit's
   files, deferred inside `_gim_disclosure_block` and reached only after the registered-mask
   precondition; `grep -in "iri" src/evaluation/*.py` returns only comment/docstring
   prose (lines 32, 38, 40, 48) — no `from src.external import iri` anywhere. The
   injection-denial mechanism `iri_column_violations` (referenced at
   `src/evaluation/metrics.py` and exercised by `test_iri_denial.py`) is untouched by the
   sibling `fixtures-and-reproducibility` narrowing recorded above in this file — verified
   independently by re-executing `tests/test_iri_denial.py` (below), not merely reading
   the prior review's claim.
2. **Comparison-wide intersection mask.** `src/evaluation/masks.py:397-475`
   (`build_comparison_mask`) computes exactly one mask per declared `set_id` over the
   full membership (stamps → exact declared membership, rejecting duplicate/merged/partial
   membership including "thereby every pairwise attempt", per its own docstring at
   line 413 → matched-window agreement → intersection). `MaskRegistry.register`
   (`masks.py:610-636`) raises `FairnessError` on a second registration for the same
   `set_id` ("computed ONCE per comparison set... a second registration raises") and on
   registration after `freeze_bundle()` — both are executable checks, not comments.
3. **Difficulty controls co-reported.** `configs/experiment.yaml:154-156`: the `primary`
   comparison set's `member_ids` are `["M-01","M-02","M-03","M-06","B-01"]` and
   `benchmark_ids` are `["B-01","M-01","M-02","M-03"]` — with the file's own comment
   naming M-01/M-02/M-03 as "the three difficulty controls" alongside B-01 (IRI) in the
   SAME set. `build_metrics_artifact`'s completeness refusal (control 24, `metrics.py`)
   requires one estimand per declared (model, benchmark) pair over the set's one mask
   before any emission — structurally forcing persistence/seasonal/climatology and IRI
   into the same primary table row-set; this unit does not itself define which model_id is
   "persistence" versus "climatology" (that identity mapping is a sibling unit's
   concern), but the completeness guard is this unit's and is real.
4. **Owner-ruled cross-unit edits (Q2=B / FU-2=A).** `src/data/locked_test.py:178-201`:
   `AccessRecord` carries `mask_bundle_ids`/`mask_registry_hash` as optional fields
   (`= None` defaults); `_containment_fields` (`locked_test.py:278-307`) returns
   `(None, None)` on an absent manifest and raises `LockedTestError` (not silent `None`)
   on a present-but-unparseable one — fail-closed as claimed. `src/models/train.py:1295-1355`
   (`assert_ablation_runnable`) takes `inverse_available: bool = False` and only this
   unit's own `resolve_inverse`/`require_target_space` in `guards.py` ever refuse the
   inverse path; `grep -rn "inverse_available" src/ scripts/` shows the parameter is never
   passed `True` by any caller in the tree — the half-B form stays inert, and no generic
   inverse route exists anywhere, consistent with D-37's reaffirmation.
5. **Fixture/confirmatory registry separation.** `scripts/07_evaluate_and_report.py:593`
   roots the fixture-scale registry at `fixture_root / "mask_registry" / partition.partition_id`
   (per-apparatus-partition) while the confirmatory path (`:669`) roots at
   `workspace / args.evaluation_out / "mask_registry"` — two distinct, non-overlapping
   directories; no code path lets an apparatus registration reach the confirmatory root or
   its `freeze_bundle`.
6. **Code-summary accuracy.** `grep -c "^def test_" tests/test_common_masks.py` → **61**,
   matching the claim exactly; the file is 1250 lines (was 1240 at the prior summary date),
   consistent with the additive cross-unit edit already recorded above (restricted-root
   literal derivation, +10 lines). `git diff --stat` shows **no uncommitted changes** to
   any file this unit owns (`src/evaluation/*`, `scripts/07_evaluate_and_report.py`,
   `tests/test_common_masks.py`, `tests/test_iri_denial.py`, `src/data/locked_test.py`) —
   everything named in the code-summary is already committed at or before `f0d9e49`. The
   sibling `acquisition` repair (uncommitted: `src/data/acquisition.py`,
   `src/data/experiment_registry.py`, `scripts/00_acquire_prepared_vtec.py`,
   `tests/test_acquisition.py`, `tests/test_clean_run.py`) touches none of this unit's
   files.
7. **TBD/constant/credential sweep.** No TBD sentinel in this unit's files was filled by
   convenience (`practical_relevance_threshold`, `stations` remain `"TBD — freeze gate"`
   in the live configs this unit reads, both correctly refused-not-defaulted per
   `read_comparison_sets`/`require_locked_receipt`). `grep -in "credential\|api_key\|
   password\|secret" src/evaluation/*.py scripts/07_evaluate_and_report.py` → no matches.
   `embargo_hours` and window bounds flow as parameters from configuration in every
   call site checked (`guards.py:577`, `masks.py:510`, `metrics.py:379`,
   `scripts/07_evaluate_and_report.py:488,584,686,695`) — no hardcoded scientific
   constant found in this unit's own modules.

**Independent test execution (this review's own run, not carried from the prior pass).**
Environment: no real pytest/pyyaml (PyPI unreachable, confirmed today); ran under the
scratchpad's stdlib pytest stand-in on CPython 3.11.16 (`.../scratchpad/venv/Scripts/python.exe`),
using the existing `run_common_masks_tests.py` harness and an equivalent harness pointed at
`tests.test_iri_denial`:
- `tests/test_common_masks.py` → **60 passed, 0 failed, 1 skipped** (the skip is the
  yaml-gated real-config re-read test, `pyyaml` unavailable — matches the prior claim).
- `tests/test_iri_denial.py` → **22 passed, 0 failed, 0 skipped** — matches the prior
  claim exactly, independently reproduced.
- `tests/test_locked_test_guard.py` (spot-checked, sibling-owned module but load-bearing
  for this unit's SD-C-02 claim): 32/34 non-parametrized test functions passed under this
  review's simple shim; the 2 "failures" are the harness's own lack of `@pytest.mark.
  parametrize` support (`test_constant_only_call_assembly_is_caught`,
  `test_record_rejects_an_empty_required_field` both require parametrize-injected args the
  shim cannot supply) — a runner limitation, not a code defect, consistent with the
  parametrize decorators found at `tests/test_locked_test_guard.py:318,623`.

**Coverage limits of this pass.** graphify CLI confirmed absent from PATH again today
(`which graphify` / `graphify query` both fail) — orientation was direct reads and greps,
per `CLAUDE.md`'s sanctioned fallback. Per the read-scope bound, no sibling unit's
`construction/<unit>/` directory was read; the one cross-unit code check (`src/models/
train.py`'s `assert_ablation_runnable`/`inverse_available`) is a workspace-code spot-check
of an integration point this unit's own summary names (D-27/D-37), not a sweep of a
sibling's design directory. `evidence/locked_test_restricted/` and any December 2022
content were not read.

**Findings:** none survive this pass at any severity — no new defect was introduced by
the repo-wide changes (D-33…D-38, the `permitted_producers` policy, the sibling
`acquisition` repair) relative to this unit's surfaces, and every claim in the existing
code-summary and its two prior review blocks reproduces exactly under independent
re-derivation.

**Summary.** This unit's specific exposure points — the IRI/GIM evaluation-time-only
boundary, the single comparison-wide intersection mask (never pairwise, never
model-specific), the completeness guard that forces the three difficulty controls and
IRI into the same primary table, the two owner-ruled additive cross-unit edits
(`AccessRecord` containment fields, the inert `inverse_available` half-B form), and the
apparatus/confirmatory mask-registry separation — all verified directly against the code
on disk at HEAD `f0d9e49`, not against the prior review's prose. Repo-wide config state
(D-33 through D-38) is consistent with what this unit reads and enforces. Independent
test execution reproduces the claimed counts exactly (61 test functions, 60/0/1 on
`test_common_masks.py`, 22/0/0 on `test_iri_denial.py`). No TBD sentinel was filled by
convenience, no scientific constant was hardcoded, no credential was found, and the
uncommitted sibling `acquisition` repair touches none of this unit's files. READY stands
on independent re-derivation, not as a carried-over verdict.

### Floor-reset re-review (2026-09-11)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-11T14:50:50Z
**Iteration:** 1 (fresh verdict against HEAD `b0b7c1d`, re-derived; not a rubber-stamp of
the three prior verdicts above)

**What changed since the last reviewed HEAD (`f0d9e49`).** `git diff --stat f0d9e49..b0b7c1d`
touches only `acquisition`-lane and `foundation`-lane files (`src/data/acquisition.py`,
`src/data/experiment_registry.py`, `scripts/00_acquire_prepared_vtec.py`,
`tests/test_acquisition.py`, `tests/test_clean_run.py`), eight sibling `code-summary.md`
files, `aidlc-state.md`, and `evidence/test_run_access_log.jsonl` — nothing this unit owns
(`src/evaluation/*`, `scripts/07_evaluate_and_report.py`, `tests/test_common_masks.py`,
`tests/test_iri_denial.py`, `src/data/locked_test.py`) has any diff since `f0d9e49`
(`git diff --stat f0d9e49..b0b7c1d -- <those paths>` is empty; confirmed again against
current `git status --short`, which lists none of this unit's files as modified). One
in-flight, uncommitted change exists in the working tree: `tests/test_locked_test_guard.py`
gained a new "Section 10" (governance-guards' own module, +343 lines) that is the sibling
owner's promised producer-side coverage of this unit's Q2 = B edit to
`src/data/locked_test.py` — read and executed below; `src/data/locked_test.py` itself has
zero diff (`git diff --stat -- src/data/locked_test.py` empty), so this unit's cross-unit
edit is unchanged code being newly tested by its owner, not a code change to re-verify.

**Repo-wide state re-verified first, per dispatch:** `grep -n "^## D-" evidence/DECISIONS.md`
confirms the register ends at `## D-38` (`## D-1 addendum` is a countersignature note, not a
new decision) — D-37 (`## D-37 — D-27 is affirmed; BLK-08's mechanism limb resolves in
D-27's identity form (reaffirmation)`, decided 2026-09-10) explicitly states "D-27 stands,
unreopened and unamended; nothing here replaces, narrows or duplicates it," and affirms the
withholding of a generic inverse route **permanently**. `inverse_available` appears only at
`src/models/train.py:1301` (parameter, default `False`) and `:1348` (the one read site); a
repo-wide grep for callers (`assert_ablation_runnable`) finds it invoked only from
`tests/test_models_smoke.py` — no production caller anywhere passes `True`, so the half-B
form stays inert exactly as the prior review claimed.

**This unit's specific exposure, re-executed and re-read against code, not against prose:**

1. **IRI/GIM evaluation-time-only boundary.** Ran the fixture-capable stand-in harness
   (`pytest_standin/run_tests.py`, which supports `tmp_path`/`monkeypatch`/parametrize,
   superseding the two older ad-hoc runners already on record) against
   `tests.test_iri_denial`: **22 passed, 0 failed, 0 skipped** — matches the claimed count
   exactly, independently reproduced with a harness that actually exercises every
   parametrized case (the older `run_iri_denial_tests.py` fails 15/22 for lack of fixture
   support; that is a harness limitation, not a code defect, and `run_iri_denial_tests2.py`
   / the new stand-in both confirm 22/0/0). `src/evaluation/metrics.py:477` remains the sole
   `from src.external import gim` in this unit's files, function-scope-deferred inside
   `_gim_disclosure_block`; `grep -in "iri" src/evaluation/*.py` still returns only
   comment/docstring prose, no `from src.external import iri`. `iri_column_violations` is
   untouched by the sibling narrowing (already verified two reviews ago; re-confirmed here
   by re-running the module rather than trusting the prior claim).
2. **Comparison-wide intersection mask.** `src/evaluation/masks.py:397-475`
   (`build_comparison_mask`) and `MaskRegistry.register`/`freeze_bundle` (`:610-636`) are
   byte-identical to the last-reviewed state (no diff since `f0d9e49`); re-ran
   `tests.test_common_masks` under the fixture-capable harness: **60 passed, 0 failed, 1
   skipped** (the skip is the pre-existing `pyyaml`-gated re-read test) — exact match.
3. **Difficulty controls co-reported.** `configs/experiment.yaml:154-160`'s `primary` set
   is unchanged: `member_ids: ["M-01","M-02","M-03","M-06","B-01"]`,
   `benchmark_ids: ["B-01","M-01","M-02","M-03"]`, with the file's own comment naming
   M-01/M-02/M-03 as "the three difficulty controls" beside B-01 (IRI) in the same set;
   `build_metrics_artifact`'s completeness refusal (control 24) still requires one estimand
   per declared pair before emission.
4. **Owner-ruled cross-unit edits (Q2=B, SD-C-02).** `src/data/locked_test.py` carries zero
   diff since the last review (confirmed by `git diff --stat`); this pass additionally
   read and ran the sibling's brand-new PRODUCER-side test coverage
   (`tests/test_locked_test_guard.py` Section 10, uncommitted): every violating manifest
   shape (`not JSON`, `no mask_ids key`, `mask_ids not iterable`, `top-level list`,
   `non-UTF-8 bytes`, `empty file`) is driven through the real `open_restricted` entry
   point and asserted to raise `LockedTestError` naming the manifest, with the access
   registry left untouched (no phantom row) — the fail-closed-on-unparseable claim this
   unit's own summary makes is now independently exercised from the producer side, not
   only the consumer side (`require_locked_receipt`) as in the prior two reviews. Ran the
   full module under the fixture-capable harness: `tests.test_locked_test_guard` **57
   passed, 0 failed, 0 skipped** (up from 44 at the last review, consistent with +13 new
   Section 10 tests; the two "failures" the prior review attributed to a parametrize-blind
   shim are gone under this harness, which does support `@pytest.mark.parametrize`).
5. **Fixture/confirmatory registry separation.** `scripts/07_evaluate_and_report.py:593`
   (`MaskRegistry(fixture_root / "mask_registry" / partition.partition_id)`) versus `:669`
   (`MaskRegistry(workspace / args.evaluation_out / "mask_registry")`) — unchanged, two
   non-overlapping roots, re-confirmed by direct read.
6. **Locked-December ordering.** Re-read `scripts/07_evaluate_and_report.py`: the `DEC`
   partition is reachable only via `materialise_locked_partition(..., g05_signature=...)`
   (`:680-682`) then `open_restricted` (`:451`), both inside `_locked_loader`; no path
   computes a metric before this chokepoint. Unchanged since the last review.
7. **Code-summary accuracy.** `grep -c "^def test_" tests/test_common_masks.py` → **61**,
   matching the claim exactly, file unchanged since `f0d9e49`. `git status --short`
   confirms every file this unit's summary lists as created/modified is clean (no
   uncommitted diff) at `b0b7c1d` — the "no commit was made" failure mode named in the
   dispatch (`project.md` `code-generation:c30`) does not apply here: this unit's own
   commits (`8a6cb61` for the Q2=B edit, and the earlier code-generation commit) are
   already landed, and no owner commit occurred mid-generation for this unit specifically.
8. **TBD/constant/credential sweep, re-run.** `configs/experiment.yaml:275`
   (`practical_relevance_threshold: "TBD — freeze gate"`, D-34's decided sentinel) and
   `configs/data.yaml:45` (`stations: "TBD — freeze gate"`) remain unfilled in the live
   configs this unit reads and correctly refuses on, not defaulted.
   `grep -in "credential\|api_key\|password\|secret" src/evaluation/*.py
   scripts/07_evaluate_and_report.py` → no matches, re-confirmed.

**One new, real finding this pass surfaced (Minor, non-blocking).**
`src/evaluation/guards.py:358-359` — `resolve_inverse`'s docstring states
`` `evidence/DECISIONS.md` ends at D-32 with D-27 unreopened (verified 2026-09-06)` ``. The
register now ends at `## D-38` (confirmed by `grep -n "^## D-" evidence/DECISIONS.md`),
six decisions past what the comment claims, and D-27's non-reopening is now affirmed by a
*later* decision, `## D-37` (2026-09-10), that this comment does not cite. The refusal
behaviour is unaffected — nothing in `resolve_inverse` or `require_target_space` executes
a live check against the register's length; the guard raises `InverseTransformError`
unconditionally regardless of what the docstring says, and no test in
`tests/test_common_masks.py` asserts the stale "ends at D-32" text (`grep -n "D-32\|D-27\|
ends at" tests/test_common_masks.py` shows no such assertion) — so this is a stale factual
claim embedded in a live guard module's docstring, not a functional or test-coverage
defect. Given this project's own repeated governance findings about stale D-number/count
claims propagating unchecked (`team.md`'s `fd-team-01`, `project.md`'s
`sweep-derive-sites`/`sweep-numerals-and-surfaces` corrections), this is worth a one-line
fix at the next touch of `guards.py` (cite D-37 and drop the dated "ends at D-32" claim in
favour of "unreopened, most recently reaffirmed by D-37"), but it does not change any
enforced behaviour and does not block readiness.

**Independent test execution, this pass's own run (fixture-capable harness, not the two
narrower ad-hoc runners already on record):**
- `tests.test_common_masks` → **60 passed, 0 failed, 1 skipped**
- `tests.test_iri_denial` → **22 passed, 0 failed, 0 skipped**
- `tests.test_locked_test_guard` → **57 passed, 0 failed, 0 skipped** (sibling-owned,
  load-bearing for this unit's SD-C-02 claim; the two prior "harness-limitation" failures
  are resolved by this harness's parametrize support)
- `tests.test_release_hashes` → **149 passed, 0 failed, 0 skipped** (per dispatch item 9;
  sibling-owned module, run to confirm the release-hash mutation-protection mechanism this
  unit's `MaskRegistry.freeze_bundle` analogy depends on is itself green)
- Environment: no real pytest/pyyaml (PyPI egress blocked, re-verified); stdlib stand-in
  (`.../scratchpad/pytest_standin/run_tests.py`) on CPython 3.11.16 at
  `.../scratchpad/venv/Scripts/python.exe`. Named honestly as a scratchpad harness, never a
  governed CI run.

**Coverage limits of this pass.** graphify CLI confirmed absent from PATH again
(`which graphify` exit 1); orientation was direct reads and greps, per `CLAUDE.md`'s
sanctioned fallback — `graphify-out/graph.json` may be stale for files this unit touches.
Per the read-scope bound, no sibling unit's `construction/<unit>/` design directory was
read; the one integration-point spot-check (`src/models/train.py`'s
`assert_ablation_runnable`/`inverse_available`) is workspace code this unit's own summary
names (D-27/D-37), not a sweep of a sibling's design. `evidence/locked_test_restricted/`
and any December 2022 content were not read. Deep line review this pass was concentrated on
`guards.py`'s `resolve_inverse`/`require_target_space`, `masks.py`'s registry/freeze path,
`scripts/07_evaluate_and_report.py`'s locked-entry chokepoint and fixture/confirmatory
root split, and the new `test_locked_test_guard.py` Section 10; the remainder of
`test_common_masks.py`'s 61 bodies and `metrics.py` were re-confirmed by test execution and
targeted grep rather than a fresh full re-read (both were fully read line-by-line in the
2026-09-10 pass on record above and carry zero diff since).

**Findings:** one Minor (stale D-number citation in a docstring, no functional or test
effect); none survive at Critical or Major severity.

**Summary.** Nothing this unit owns changed between the last reviewed HEAD (`f0d9e49`) and
current HEAD (`b0b7c1d`); the only in-flight change touching this unit's surface is a
sibling's new, additive, producer-side test file for a cross-unit edit whose target module
(`src/data/locked_test.py`) itself carries zero diff. Independent re-execution under a
fixture-capable harness (superseding the two narrower ad-hoc runners on record) reproduces
every claimed count exactly and additionally confirms 57/0/0 on the sibling's new Section
10 and 149/0/0 on `test_release_hashes.py`. D-37's reaffirmation of D-27 and the continued
absence of any caller passing `inverse_available=True` confirm BLK-08's mechanism limb
remains closed as this unit implements it. The one new finding — a stale "ends at D-32"
claim in `guards.py`'s docstring, six decisions behind the current register — is
non-functional and does not block. READY stands on this pass's own independent
re-derivation against `b0b7c1d`.
