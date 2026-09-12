# Code Summary — `models-and-baselines`

**Unit** `models-and-baselines` (Bolt 8) · **Kind** `library` · **Stage** `code-generation`
**Plan**: `code-generation-plan.md` (11 steps; Steps 1–6, 8–11 executed; Step 7 gated and NOT executed — see § Deviations)
**Receipted answers**: Q1 = A, FU-1 = C (supersedes Q2), Q3 = A, FU-2 = B (supersedes Q4), Q5 = A.

## Sources

- Approved plan and receipted Q&A: `construction/models-and-baselines/code-generation/{code-generation-plan.md,code-generation-questions.md}` [Q1][Q2][Q3][Q4][Q5]
- Functional design: `construction/models-and-baselines/functional-design/{business-logic-model.md,business-rules.md,domain-entities.md}` (W-1…W-12; R-90…R-102, R-102a)
- NFR design: `construction/models-and-baselines/nfr-design/security-design.md` (SD-M-00…SD-M-07)
- Governing decisions: `evidence/DECISIONS.md` D-121 (grids), D-122 (seeds), D-27 (inverse withheld), D-31 (G-09)
- Change record: `governance/CHANGE_RECORD_2026-09-06_BLK03_confirmatory_contract.md` (written FIRST, Step 1)

## Files created (10) / modified (2)

| File | Lines | Content |
|---|---|---|
| `src/models/persistence.py` | 135 | M-01 persistence, M-02 24-h seasonal persistence (no fitted state) |
| `src/models/climatology.py` | 235 | M-03 station×month×hour climatology, training-partitions-only fit, `FittedPartitionRecord`; validation/`DEC` row in fitting input raises `LeakageError` |
| `src/models/ridge.py` | 145 | M-04 Ridge over the D-121 six-value `alpha` grid; lazy `scikit-learn` import, absence refuses naming the `requirements.txt` pin |
| `src/models/random_forest.py` | 188 | M-05 RF (direct only) over the 18-combination grid; importance emitted only as diagnostic-marked `ImportanceFigure`, never on a selection path |
| `src/models/checkpoint.py` | 182 | Backend-neutral checkpoint SELECTION on lowest validation RMSE over a recorded epoch history; restore returns that checkpoint (last-epoch restore fails) |
| `src/models/lstm.py` | 367 | M-06 against the tf.keras 2.21.0 candidate API; every `tensorflow` import inside `_require_frozen_pin()`-guarded code refusing while `requirements.txt` carries no frozen `tensorflow==` line (FU-1 = C); 16-combination grid and seven §8.6 settings asserted from config, never in source |
| `src/models/train.py` | 1487 | `fit_predict` (closed M-01…M-06 set), `assert_stamp_match` (R-90, named function, three checks), `three_seed_mean` (all four limbs; `expected_seeds` from `ConfigSnapshot.seeds`, never inlined), `tune` (January–November only; `TuningRecord` seven fields + three attestation fields, attestation UNCONDITIONAL per SD-M-01 Q1 = C), R-96 grid content+hash freeze, `select` (R-101, refit changes no hyperparameter), five-ablation registry from `experiment.yaml` (R-97: `ABL-HIST48` refuses before primary freeze; `ABL-DIFF` refuses naming D-27), `HorizonSpec` config-only (R-99) |
| `scripts/06_train_and_predict.py` | 741 | Position 06; `ensure_process_determinism` first, `assert_no_raw_fields` before first write; `assert_stamp_match` before EVERY scoring path; three-seed run per fitting-capable partition; W-12/R-102a one-shot `DEC` write path in full (write once → sha256 → `PredictionHashReceipt` → `.tmp`→fsync→rename → registry column 18 → refuse-to-exit) and UNREACHABLE today behind `materialise_locked_partition`'s G-05 signature guard; honest `aborted` registry row on `IntegrityError`; `prior_period_exposure` never written |
| `tests/test_models_smoke.py` | 1221 | 54 test functions (count derived: `grep -c "def test_"`) — closed-set refusal, residual/GRU/PyTorch absence scan, M-01…M-03 happy paths + training-only control, M-04/M-05 refusal-by-name + grid-content controls (6/18/16 re-read from config), four R-90 controls (control 3 by enumeration over R-80's six ids) + must-not-fire control, the full `three_seed_mean` negative-control set (incl. wrong-but-distinct triple built from config at test time, never literal), tuning refusals (December partition, criterion-hash mismatch, missing attestation), ablation registration + refusals, horizon config-only, RF importance marker, M-06 pin-guard refusal + seven-settings-from-config, `06` receipt controls through a synthetic non-`DEC` fixture with the `DEC` guard asserted to refuse |
| `tests/test_checkpoint_restore.py` | 209 | 12 test functions — lowest-validation-RMSE selection, restore-returns-that-checkpoint, last-epoch restore fails, tie and NaN handling, fake-backend round trip |
| `requirements.txt` (modified) | +6 | `scikit-learn==1.4.2` added under the scientific-base block citing the change record (Q3 = A); TensorFlow EXCLUDED with a comment naming the `TBD — freeze gate` rule |
| `configs/experiment.yaml` (modified) | +133/− | D-121 grids transcribed verbatim (Ridge 6, RF 18, LSTM 16, each block citing D-121/Vision §8.6), `models.lstm_fixed_settings` (seven §8.6 settings, `source_text` quoted), `ablations` as the five TE §7.2 named entries; nothing D-121/§8.6/§7.2 does not fix was written (Q5 = A) |

Plus Step 1's governance record: `governance/CHANGE_RECORD_2026-09-06_BLK03_confirmatory_contract.md` (353 lines) — BLK-03 contract approval, the sklearn pin, the D-121 transcription, the FU-1 = C posture, and the PROPOSED D-number text for FU-2 = B (owner adopts or edits; not written into `evidence/DECISIONS.md` by any agent).

## Key implementation decisions

1. **FU-1 = C realised**: no `tensorflow` import at module scope anywhere; the Keras construction lives behind `_require_frozen_pin()`, whose refusal names TS-M-01 and the pin. No TBD sentinel was filled.
2. **Confirmatory contract (BLK-03, Q1 = A)**: `three_seed_mean` enforces all four limbs of `domain-entities.md` § 3 — `SeedError` / `AlignmentError` on the ordered (`station`, `interval_start_utc`) index (set AND order) / `PartitionError` / `LeakageError` — with provenance copied and `seed = None` on output. Change record exists FIRST, as the plan ordered.
3. **No scientific constant in source**: seeds, grids, the seven LSTM settings and ablation identities reach code only from `configs/`; tests re-read the counts 6/18/16 from `experiment.yaml` and never hold a real seed/grid value as a literal.
4. **Two-tier errors** throughout: integrity violations raise typed exceptions naming file and expectation; completeness shortfalls land as machine-readable manifest fields.
5. **Import boundary held**: `src/models` imports none of `src/external/iri.py`, `src/external/gim.py`, `src/evaluation`, or PyTorch; absence tested by identifier scan.

## Test coverage summary

66 test functions total (54 + 12, derived by count). Every hard rule carries a negative control (team.md mandated practice): pin guard, closed model set, stamp match ×4, seed limbs, tuning attestation, ablation refusals, `DEC` guard, receipt failure modes. Full suite ran in the generating session (2026-09-06T14:01Z; `evidence/test_run_access_log.jsonl` rows for `test_release_hashes` in the same run) — **smoke evidence only, never governed** (stdlib stand-in; pins not installable there).

## Deviations from the plan

- **Step 7 NOT executed (designed outcome)**: precondition checked on disk — `evidence/DECISIONS.md` ends at D-32 (2026-08-28); no D-number dated on/after 2026-09-06 reopening D-27 exists. Per the approved plan: no inverse was added to `src/features/transforms.py` (verified: none exists), no `src/evaluation` → `src/features` edge added, and `ABL-DIFF` refuses naming D-27. The proposed D-number text sits in the change record for the owner to adopt; if adopted later, Step 7 runs under a fresh ruling.
- **No smoke re-run on this clone**: no Python interpreter exists here (Store stubs only). The generating session's suite run stands as the smoke evidence; nothing was re-executed on resume.
- **Owner commit da6cb7b** (2026-09-06 18:04 +0400, template message) carries this unit's entire code set and two governed-artifact changes with no D-number cited — team.md's linking rule requires D-121/change-record citation. Human act outside the stage; routed to the gate (fourth instance of the pattern: 06207c4, ed5808b, 6246907).

## Open items routed to the gate

BLK-03 evidence limb open at G-05; TensorFlow pin unfrozen (M-06 Keras path written-but-unexecutable; TA-26 `Pending`); sklearn install evidence owed; pyarrow pin carried; FR-P1-05-2 bootstrap-seed attribution disagreement (raised, not edited); `prior_period_exposure` deviation note (R-102a); da6cb7b commit-message disposition; WS-14, WS-15, TA-12, TA-13, TA-26 all `Pending`; nothing discharged.

## Assumptions & Open Questions

None.

## Review

**Verdict**: READY
**Reviewer**: aidlc-architecture-reviewer-agent
**Date**: 2026-09-06T17:28:23Z
**Iteration**: 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Minor | `code-summary.md:12` | The Sources line reads "Governing decisions: `evidence/DECISIONS.md` D-121 (grids), D-122 (seeds), D-27 (inverse withheld), D-31 (G-09)" — attributing D-121 and D-122 to `evidence/DECISIONS.md`. Verified by grep: neither `## D-121` nor `## D-122` (nor any mention of either ID) appears anywhere in `evidence/DECISIONS.md`, which runs D-1…D-32. This unit's own `nfr-design/security-design.md` (line 47-48) already identifies and corrects this exact misattribution ("Citation corrected 2026-09-04 on adversarial finding 2, Major: this line previously also attributed D-121 and D-122 to `evidence/DECISIONS.md`, which ends at D-32 and contains neither"), establishing that D-121/D-122 belong to "Vision §14.2's own decision register — a register distinct from `evidence/DECISIONS.md`." `code-summary.md`'s own Sources line reproduces the already-corrected error as a new representation of the fact, which `project.md`'s learned rule ("sweep every REPRESENTATION of a corrected fact... not every instance you happen to look at") exists to prevent. The governed artifact `configs/experiment.yaml` itself is cited correctly (`decision: "D-121"`, `source: "Vision §8.6, grid table; Vision §14.2 line 1206"`, no `evidence/DECISIONS.md` claim) — only this summary line is wrong. | Correct the Sources line to attribute D-121/D-122 to "Vision §14.2's decision register" and keep D-27/D-31 attributed to `evidence/DECISIONS.md` (both verified present there). |

### Validation checks performed (evidence-grounded, no tool failures to report — no validation tooling was named in the stage definition beyond manual cross-reference)

| Check | Result |
|---|---|
| TensorFlow import guard: no `tensorflow` import at module scope anywhere under `src/models/*.py`; every import sits inside `require_frozen_pin()`-gated function bodies (`lstm.py:175,203,291`); `requirements.txt` carries no non-comment `tensorflow==` line; `test_the_pin_guard_refuses_against_the_real_requirements_and_a_commented_pin` and `test_m06_fit_refuses_at_the_guard_before_any_tensorflow_import` exercise the refusal and name TS-M-01 | PASS |
| scikit-learn: lazy import in `ridge.py`/`random_forest.py` behind `require_sklearn()`; `requirements.txt:25` pins `scikit-learn==1.4.2`; refusal names the pin and TS-M-03 | PASS |
| Scientific constants: no D-121 grid value, D-122 seed, or Vision §8.6 setting value appears as a literal in `src/models/*` or the tests (`test_the_frozen_seed_set_never_appears_in_src_models` static-scans for 3-int literal collections; grep for `1337`/`2024`/`20221201` under `src/models/` returns nothing); `configs/experiment.yaml` grids transcribe exactly Ridge 6 / RF 18 / LSTM 16 and the seven fixed LSTM settings verbatim from Vision §8.6, matching `business-rules.md` R-96 | PASS |
| Import boundary: no `src.external.iri`, `src.external.gim`, `src.evaluation`, or `torch` import anywhere under `src/models/*.py`, enforced by AST-walking tests (`test_src_models_never_imports_iri_gim_or_evaluation_and_frameworks_only_lazily`, `test_the_two_removed_architectures_and_a_second_dl_stack_are_absent_from_src_models`) | PASS |
| R-90 stamp match: `assert_stamp_match` (`train.py:520`) implements the three named checks (`PartitionError` ×2, `LeakageError`) exactly as `business-rules.md` R-90's rewritten table states; tests cover all 4 controls plus control 3 by enumeration over the 6 partition ids (25 pairs, asserted count) plus the must-not-fire control | PASS |
| `three_seed_mean` four limbs: matches `domain-entities.md` §3 limbs 1-4 exactly, including the wrong-but-distinct-triple control, AlignmentError on set-and-order, PartitionError on training-role/partition disagreement, LeakageError on transform disagreement; `expected_seeds` read from `ConfigSnapshot.seeds` only at the call site (`06_train_and_predict.py:595`), never inlined in `src/models` | PASS |
| Tuning (R-95/SD-M-01): `record_tuning` implements exactly the two runnable mechanisms SD-M-01 specifies (partitions_read excludes December; criterion_hash == criterion_used_hash) plus the SD-M-01 unconditional attestation; `audit_access_since_declaration` is correctly left as a passthrough field per SD-M-01's explicit design ("no window computation; no read of R-25's log" — R-25's durable access log does not exist, BLK-07 open) — this is the documented design, not a gap | PASS |
| Script 06: six-step entry order present (`ensure_process_determinism` first in `main()`; `assert_no_raw_fields` before first write via `_assert_phase1_field_contract`); `assert_stamp_match` called before every scoring path (once per partition, again per model/seed iteration); DEC path gated behind `materialise_locked_partition`'s G-05 signature guard and unreachable via default `--partition` list; aborted registry row written on `IntegrityError` (all typed exceptions subclass `IntegrityError`, confirmed via `grep "class.*Error" src/data/config.py`); `prior_period_exposure` not written anywhere in the script | PASS |
| Ablations: exactly the five named entries transcribed in `configs/experiment.yaml`, matching TE §7.2; `ABL-HIST48` refuses before primary freeze; `ABL-DIFF` refuses naming D-27 (confirmed: no `Transform.inverse` in `src/features/transforms.py`, no new D-number reopening D-27 in `evidence/DECISIONS.md`, which ends at D-32 with nothing dated on/after 2026-09-06) | PASS |
| Checkpoint: selection on lowest validation RMSE with earliest-epoch tie-break; restore returns that checkpoint; last-epoch restore fails `assert_restored_is_best`; NaN/negative RMSE refused | PASS |
| Summary accuracy: file line counts (135/235/145/188/182/367/1487/741/1221/209/353) and test counts (54 + 12 = 66) in `code-summary.md` all verified exact via `wc -l` / `grep -c "^def test_"` | PASS (except finding #1) |
| Security/NFR: no credential or secret found in generated files; no December 2022 content read by any test; no real G-05 signature used in any test (`DEC` path tests use `g05_signature=None` and assert refusal) | PASS |

### Summary

This is an unusually thorough, contract-disciplined implementation: every named business rule (R-90…R-102a), every domain-entity shape (Prediction, TuningRecord, Checkpoint, AblationEntry, PredictionHashReceipt, ConfirmatoryPrediction's four limbs), the TBD-freeze-gate discipline for the TensorFlow pin (FU-1 = C), the D-27/Step-7 gating (FU-2 = B), and the D-121/Vision §8.6 grid transcription (Q5 = A) were independently re-derived from the functional-design and NFR-design contracts and matched exactly against the generated code and its 66 negative-control-bearing tests. The one defect found is a Minor citation error in `code-summary.md`'s own Sources line — a documentation-only recurrence of an error this same unit's `security-design.md` had already identified and corrected — and does not affect any executable behavior, test, or governed artifact. No Critical or Major implementation defect was found.

### Correction (2026-09-10): `scripts/06_train_and_predict.py`'s line count, derived not carried

The Files table's `741` was exact at this summary's writing time and is SUPERSEDED by
cross-unit growth. Derived by `git show <commit>:scripts/06_train_and_predict.py | wc -l`
and printed before assertion: **741** (summary time) → **806** at `64c0551` → **944** at
`cf3185d` → **999** at `0e002cd` and in the working tree (`wc -l` = 999). The review-noted
"794-vs-806" figures were intermediate states of the same growth. The deltas are the
fixtures unit's owner-authorised additive edits recorded below; no full-year line of this
unit's own logic changed. Derived alongside: `tests/test_models_smoke.py` now carries
**56** test functions (`grep -c "^def test_"`; the table's 54 is superseded), of which 55
pass and 1 skips by name on this clone.

### Cross-unit edit record (2026-09-10) — edits made by `fixtures-and-reproducibility`, owner-authorised

Appended after the gate rejection lifted the receipt freeze. Under
`CR-2026-09-07-R133-FIXTURES-AND-REPRODUCIBILITY` (§5, §11.5; the owner's "apply the
recommended option" ruling), the fixtures unit made these ADDITIVE edits to
`scripts/06_train_and_predict.py` — the full-year path and the W-12/R-102a locked path are
untouched:

- Commit `cf3185d` (Q4/Q5 = A): `--fixture-manifest` option (a `--partition` alongside it
  is a parser error), `_stage_entry` kwarg + ONE `require_receipts_for_snapshot` call after
  `assert_lock_complete`, and ONE early-return in `_run` reaching the additive
  `_run_fixture_scale`: the same per-partition fit/predict sequence over the scope's
  APPARATUS partitions, the fixture stamp embedded in every prediction payload, and NO
  locked path reachable (an apparatus partition is never `locked`).
- Commit `0e002cd` (board Rec 4 / ML-03): `_fixture_bundle_root` validates against 05's
  actual fixture output (`apparatus_split_manifest.json`, by name); fixture predictions
  land directly under `--predictions-out` (deterministic hand-off to 07; a re-run refuses
  at the write-once prediction); a machine-readable `fixture_measurements.json` (scored
  prediction rows) is emitted for the orchestrator's candidate folding. One rename inside
  the fixture path (`fixture_target`) keeps this unit's own
  `test_a_dec_iteration_handed_the_pre_loop_target_is_refused` source assertion exact.

Tests live in `tests/test_clean_run.py`. This unit's owner may confirm or reverse per the
change record.

### Owner-rulings implementation review (2026-09-10)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-10T11:33:57Z
**Iteration:** Owner-rulings implementation review (2026-09-10)

#### Findings

None survive verification at any severity for this unit.

#### Verification performed

- **TensorFlow pin (owner ruling 5: `tensorflow == 2.21.0`).** `requirements.txt` and
  `src/models/lstm.py` diffs read in full. Grepped the whole repository for
  `tensorflow==`/`tf==`/version strings: the only non-comment pin is
  `requirements.txt: tensorflow==2.21.0`, and every other mention (docstrings, test
  synthetic-file fixtures) is textually consistent with it — no stale or conflicting pin
  found anywhere, and `configs/experiment.yaml` carries no TensorFlow field to sync (
  confirmed by grep: no match). `src/models/lstm.py`'s stale "pin is TBD" docstring
  prose was corrected to reflect the frozen pin while still stating "the ENVIRONMENT is
  not verified" (PyPI unreachable) — an honest, not overclaiming, correction.
  `require_frozen_pin`, `build_keras_model`, and `determinism_check` all gained a
  `requirements_path: Path | None = None` parameter (verified at lines 109, 170/176,
  199/203) used by the re-pointed tests to inject an unpinned synthetic file — the guard
  logic itself is otherwise unchanged, and no `tensorflow` import happens outside a
  `require_frozen_pin()`-gated path (still true after this diff).
- **`tests/test_models_smoke.py` (+39/−12) re-pointed controls**, read in full: the
  absent/commented-pin negative controls still raise `IntegrityError` naming `TS-M-01` and
  `TBD` on synthetic files (unchanged assertion strength); a new assertion additionally
  proves the guard reads the real, now-frozen `requirements.txt` and returns
  `"tensorflow==2.21.0"`;
  `test_m06_fit_refuses_at_the_guard_before_any_tensorflow_import` was extended, not
  weakened — it now separately proves the guard still fires on an injected unpinned file
  AND that, with the real (frozen) file, the next failure is `ModuleNotFoundError` (an
  environment fact — TensorFlow is not installed — correctly distinguished from a guard
  failure). Full-module run: `test_models_smoke: 55 passed, 0 failed, 1 skipped, 0 errors`
  — the skip is a `pytest.importorskip("yaml")` on this pyyaml-less clone, matching the
  claim.
- **D-27/BLK-08 (owner ruling 6).** This unit's own `ABL-DIFF` gating (referenced in its
  original review's "Ablations" check, row 85 above) was re-verified unaffected: `git diff
  HEAD -- src/data/fixture_manifest.py` is empty (R-139 control 25 byte-unchanged), and
  `evidence/DECISIONS.md` still ends at D-32 with nothing dated 2026-09-10 — confirming no
  duplicate or reopened decision landed, consistent with the change record's draft D-E
  being unadopted.
- **Test totals**: full-suite run (26 modules, stdlib stand-in) reproduces exactly
  `1134 passed, 0 failed, 39 skipped, 0 errors`.

#### Summary

The TensorFlow pin freeze is transcribed consistently across `requirements.txt` and
`src/models/lstm.py` with no stale or conflicting version string anywhere in the
repository, and the re-pointed pin-guard tests genuinely strengthen (not weaken) the
guard-vs-import distinction. This unit's own D-27-dependent ablation gating (`ABL-DIFF`)
is confirmed untouched. No defect found in this unit's exposure to the pass.

### Floor-reset re-review (2026-09-11)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-11T14:44:56Z
**Iteration:** Floor-reset re-review (2026-09-11), fresh verdict against HEAD `b0b7c1d`

#### Scope and method

Re-derived independently against the current repository state (`git status` shows no
pending changes to any file this unit owns; the last commit touching this
`code-summary.md` is `17e0767`, three commits behind `b0b7c1d`, and `scripts/06_train_and_predict.py`
is byte-identical at `0e002cd` and `HEAD`, confirmed via `git show <rev>:... | wc -l` = 999 both
times). No `graphify` executable is on PATH (`which graphify` → not found; per `CLAUDE.md`'s
2026-09-10 verification), so file reads/greps were used as the sanctioned fallback. Ran the
requested test modules with the stdlib pytest stand-in against a real CPython 3.11.16
interpreter (no third-party packages installed; PyPI unreachable, consistent with prior runs).

#### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Minor | `code-summary.md:44` ("66 test functions total (54 + 12, derived by count)") | Stale count, not caught by the 2026-09-10 correction box. `grep -c "^def test_" tests/test_models_smoke.py` = **56** and `tests/test_checkpoint_restore.py` = **12** today, total **68**, not 66. The 2026-09-10 correction (line ~102-104) restated the smoke-test count as 56 but never propagated that into this "Test coverage summary" section's own total, which still reads the pre-correction 54+12=66. This is exactly the failure mode `project.md`'s "sweep every REPRESENTATION" rule targets: one representation of the count was corrected, a second (the section total) was not. | Update line 44 to state 68 (56+12), derived and printed, or mark the figure superseded the way the line-count correction below it already does. |

No Critical or Major finding survives verification. Every item this dispatch named as the
unit's specific exposure was re-checked directly against source, not carried from prior
review prose:

- **Frozen grids (D-121):** `configs/experiment.yaml:43-68` — ridge axes product = 6 (one
  axis, 6 values), RF = 2×3×3 = 18, LSTM = 2×2×2×2 = 16, each matching its own `combinations:`
  field. `src/models/train.py:998-1025` (`assert_grid_content`) recomputes the product via
  `enumerate_grid`/`itertools.product` and raises `IntegrityError` naming R-96 if the
  enumerated count and the declared `combinations` disagree — content is asserted, not only
  immutability, confirmed by reading the function body, not just its docstring.
- **Seeds:** `configs/seeds.yaml` carries `development: 42`, `final: [1337, 2024, 7]`,
  `bootstrap: 20221201` (D-122) and no seed value appears as a literal anywhere under
  `src/models/` (`grep` for the digits returns nothing outside `seeds.yaml`/tests-that-read-config).
  `three_seed_mean` (`train.py:690-750`) takes `expected_seeds` as a parameter and the only
  call sites (`scripts/06_train_and_predict.py:737,843`) read it via `_final_seeds(snapshot)`
  from `ConfigSnapshot.seeds` — never inlined.
- **Seven fixed LSTM settings:** transcribed verbatim in `configs/experiment.yaml:76-89`
  (`lstm_fixed_settings`, `source_text` quoted from Vision §8.6) and read by
  `fixed_settings()` in `src/models/lstm.py:137-150` — no literal `0.2`/`"Adam"`/`100`/etc.
  hardcoded in source.
- **Locked-December unreachability:** `_dec_target` in `scripts/06_train_and_predict.py:605-663`
  calls `materialise_locked_partition`, uses the frame it RETURNS (`loaded`), and explicitly
  refuses (`LockedTestError`) if that returned frame is `None` or is the same object as the
  pre-loop `released_target` — the earlier Critical (discarding the returned frame and
  scoring against the pre-loop target) is not present in the code at HEAD.
- **`ABL-DIFF`/D-27:** `src/models/train.py:1313,1352` and `src/features/transforms.py:31,101`
  confirm no `inverse`/`apply` method exists on any transform, and `evidence/DECISIONS.md`'s
  final entry is **D-38** (D-37 reaffirms D-27's withholding as permanent, "the refusal IS the
  mechanism," no generic inverse route created) — `ABL-DIFF` still refuses, naming D-27, and no
  post-2026-09-06 decision reopens it.
- **Phase 1 → Phase 2 weight carry-over:** no Phase 2 training/checkpoint-carry code exists
  anywhere in `src/models/` for this rule to violate; not applicable to the code as it stands.
- **TBD sentinels:** `configs/experiment.yaml:93,94,99` — `models.declared_baseline_per_track`,
  `models.selection`, and `models.selected` all still read `"TBD — freeze gate"`.
  `scripts/06_train_and_predict.py:456-471` (`_selected_params`) and
  `src/models/train.py:_read_selection_block` (~1153-1174) both raise `IntegrityError` naming
  the unfilled field rather than defaulting or filling it.
- **Credentials/secrets/hardcoded constants:** none found under `src/models/`,
  `scripts/06_train_and_predict.py`, or `requirements.txt` (grepped for API-key/secret/token
  patterns and for literal seed/grid values — no matches outside config and tests-that-read-config).
- **Test execution** (stdlib stand-in, CPython 3.11.16, real venv interpreter, no third-party
  packages — honestly not a governed pytest run):
  - `tests/test_models_smoke.py`: **55 passed, 0 failed, 1 skipped** (skip:
    `test_real_experiment_yaml_transcription_is_internally_consistent`, `pytest.importorskip("yaml")`
    on this pyyaml-less environment) — matches the 2026-09-10 correction's claimed figures exactly.
  - `tests/test_checkpoint_restore.py`: **12 passed, 0 failed, 0 skipped**.
  - `tests/test_determinism.py`: **12 passed, 0 failed, 23 skipped** (all 23 skips are
    `pytest.importorskip("yaml")`; this module is not one this unit's `Files created` table
    lists, so its skip count is reported for completeness, not scored against this unit).

#### Summary

No Critical or Major defect survives this fresh pass. The specific risk areas this dispatch
named — grid-content assertion, seed provenance, the seven LSTM settings, locked-December
frame handling, the D-27/`ABL-DIFF` refusal, TBD-sentinel discipline, and credential/constant
hygiene — all check out against the code at HEAD `b0b7c1d`, not merely against prior review
prose. The one Minor finding is a stale total in this artifact's own "Test coverage summary"
section, left unfixed by the 2026-09-10 correction that fixed the same fact elsewhere in the
file; it does not affect any executable behavior, governed artifact, or test result.
