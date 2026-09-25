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
| `src/models/persistence.py` | **170** (re-derived 2026-09-20 by `wc -l`; the cell read 135) | M-01 persistence, M-02 24-h seasonal persistence (no fitted state — the only two families not persisted, and therefore the only two reachable on the locked partition directly). Accepts `validation_bundle` for a uniform family signature and ignores it: neither family selects anything |
| `src/models/climatology.py` | **606** (re-derived 2026-09-20 by `wc -l` on the working tree; the cell read 235) | M-03 **station×hour** climatology — the key was **station×month×hour** until the owner's Recommendation 2 ruling of 2026-09-20 (see § Remediation 2026-09-20 below); training-partitions-only fit, `FittedPartitionRecord`; validation/`DEC` row in fitting input raises `LeakageError`; key read from `configs/experiment.yaml` `models.climatology` (TC-03e) and a fit that cannot produce a key the scored bundle demands raises at FIT time; adds the persist/load surface (`fit_state`, `climatology_from_state`, `predict_rows_from_state`) the locked path predicts through |
| `src/models/ridge.py` | **226** (re-derived 2026-09-20 by `wc -l`; the cell read 145) | M-04 Ridge over the D-121 six-value `alpha` grid; lazy `scikit-learn` import, absence refuses naming the `requirements.txt` pin. Split into `fit_state` / `predict_rows_from_state` under Recommendation 6 so the locked path can load a REFIT-persisted model and predict |
| `src/models/random_forest.py` | **277** (re-derived 2026-09-20 by `wc -l`; the cell read 188) | M-05 RF (direct only) over the 18-combination grid; importance emitted only as diagnostic-marked `ImportanceFigure`, never on a selection path. Split into `fit_state` / `predict_rows_from_state` under Recommendation 6, same as Ridge |
| `src/models/checkpoint.py` | 182 | Backend-neutral checkpoint SELECTION on lowest validation RMSE over a recorded epoch history; restore returns that checkpoint (last-epoch restore fails) |
| `src/models/lstm.py` | **626** (re-derived 2026-09-20 by `wc -l` on the working tree; 373 was exact at 2026-09-13 HEAD `1670ac8`, and 367 before that) | M-06 against the tf.keras **2.21.0** API; every `tensorflow` import inside `require_frozen_pin()`-guarded code. **The pin is FROZEN (`requirements.txt:36`, `tensorflow==2.21.0`, D-36) and the guard PASSES** — the refusal still fires for any requirements file carrying no non-comment `tensorflow==` line, which is what the negative controls inject; what blocks an M-06 run is the unverified ENVIRONMENT, not the guard (TA-26 `Pending`). 16-combination grid and seven §8.6 settings asserted from config, never in source. Split into `fit_state` / `predict_rows_from_state` under Recommendation 5: early stopping, per-epoch validation RMSE and checkpoint restore read an explicitly named `validation_bundle`, never the scored bundle; the REFIT fit names none and trains for the frozen `models.refit.epochs` count |
| `src/models/train.py` | **2068** (re-derived 2026-09-20 by `wc -l` on the working tree; the cell read 1487) | Adds under Recommendations 5 and 6: `assert_not_locked_fit`, `assert_validation_bundle`, `refit_epoch_count` / `read_refit_epochs` / `assert_refit_epochs_match_rule`, and the persist/load surface `FittedStateBackend` / `JsonStateBackend` / `FittedModelRecord` / `fit_and_persist` / `load_fitted_model` / `assert_fitted_payload_unchanged` / `predict_from_fitted`. Pre-existing: `fit_predict` (closed M-01…M-06 set), `assert_stamp_match` (R-90, named function, three checks), `three_seed_mean` (all four limbs; `expected_seeds` from `ConfigSnapshot.seeds`, never inlined), `tune` (January–November only; `TuningRecord` seven fields + three attestation fields, attestation UNCONDITIONAL per SD-M-01 Q1 = C), R-96 grid content+hash freeze, `select` (R-101, refit changes no hyperparameter), five-ablation registry from `experiment.yaml` (R-97: `ABL-HIST48` refuses before primary freeze; `ABL-DIFF` refuses naming D-27), `HorizonSpec` config-only (R-99) |
| `scripts/06_train_and_predict.py` | **1289** (re-derived 2026-09-20 by `wc -l` on the working tree; 999 was exact at 2026-09-13, before that 741 → 806 → 944) | Position 06; `ensure_process_determinism` first, `assert_no_raw_fields` before first write; `assert_stamp_match` before EVERY scoring path; three-seed run per fitting-capable partition; W-12/R-102a one-shot `DEC` write path in full (write once → sha256 → `PredictionHashReceipt` → `.tmp`→fsync→rename → registry column 18 → refuse-to-exit), reachable only behind `materialise_locked_partition`'s G-05 signature guard; honest `aborted` registry row on `IntegrityError`; `prior_period_exposure` never written. **Recommendations 5 and 6:** the `REFIT` iteration is no longer skipped — `_refit_and_persist` fits every fitted family on January–November and persists it hashed; the `DEC` iteration (`_locked_predictions`) LOADS those records and predicts, and no `model.fit` is reachable on it |
| `tests/test_models_smoke.py` | **1895** (re-derived 2026-09-20 by `wc -l` on the working tree AFTER this pass's own docstring corrections; it read 1890 before them, 1393 at 2026-09-13, and 1221 before that) | **67** test functions (re-derived 2026-09-20: `grep -c "^def test_"` = 67; superseding 56, and 54 before that). One is parametrized over the four `FITTED_MODEL_IDS`, so the collected-case count is **70** (67 − 1 + 4) — stated separately because the two figures are not interchangeable. New on 2026-09-20 under Recommendations 2, 5 and 6: the `(station, hour)` key and coverage controls, the fit-time coverage refusal, the config-only-key control, the three inference-only negative controls (a) fit-on-`DEC` refused for every fitted family, (b) a `DEC` bundle offered as the validation set refused, (c) an absent persisted model refused rather than refitted, the frozen-epoch-rule control, the tampered-payload hash control, the unpersistable-state refusal, the **end-to-end locked-path success control on synthetic December data**, and the `05 --partition DEC` guarded-branch control. Pre-existing: closed-set refusal, residual/GRU/PyTorch absence scan, M-01…M-03 happy paths + training-only control, M-04/M-05 refusal-by-name + grid-content controls (6/18/16 re-read from config), four R-90 controls (control 3 by enumeration over R-80's six ids) + must-not-fire control, the full `three_seed_mean` negative-control set (incl. wrong-but-distinct triple built from config at test time, never literal), tuning refusals (December partition, criterion-hash mismatch, missing attestation), ablation registration + refusals, horizon config-only, RF importance marker, M-06 pin-guard refusal + seven-settings-from-config, `06` receipt controls through a synthetic non-`DEC` fixture with the `DEC` guard asserted to refuse |
| `tests/test_checkpoint_restore.py` | 209 | 12 test functions — lowest-validation-RMSE selection, restore-returns-that-checkpoint, last-epoch restore fails, tie and NaN handling, fake-backend round trip |
| `requirements.txt` (modified) | +6 at Step 6 | `scikit-learn==1.4.2` added under the scientific-base block citing the change record (Q3 = A). **The Step-6 state — "TensorFlow EXCLUDED with a comment naming the `TBD — freeze gate` rule" — is SUPERSEDED.** This unit's own later self-edit, commit `17e0767`, added the frozen pin; `requirements.txt:36` now reads `tensorflow==2.21.0` under D-36 (2026-09-10), which states verbatim that it "supersedes the earlier `TBD — freeze gate` state". The `+6` figure covers Step 6 only and was never updated for that self-edit. Installability on either governed platform is still unverified, so TA-26 stays `Pending` — that part of D-36 is not superseded |
| `configs/experiment.yaml` (modified) | +133/− | D-121 grids transcribed verbatim (Ridge 6, RF 18, LSTM 16, each block citing D-121/Vision §8.6), `models.lstm_fixed_settings` (seven §8.6 settings, `source_text` quoted), `ablations` as the five TE §7.2 named entries; nothing D-121/§8.6/§7.2 does not fix was written (Q5 = A) |

Plus Step 1's governance record: `governance/CHANGE_RECORD_2026-09-06_BLK03_confirmatory_contract.md` (353 lines) — BLK-03 contract approval, the sklearn pin, the D-121 transcription, the FU-1 = C posture, and the PROPOSED D-number text for FU-2 = B (owner adopts or edits; not written into `evidence/DECISIONS.md` by any agent).

## Key implementation decisions

1. **FU-1 = C realised**: no `tensorflow` import at module scope anywhere; the Keras construction lives behind `require_frozen_pin()`, whose refusal names TS-M-01 and the pin. No TBD sentinel was filled. *(Updated 2026-09-20, Recommendation 42: the pin has since been frozen at `tensorflow==2.21.0` under D-36, so against the governed `requirements.txt` the guard now PASSES. The structural property — no import outside a guarded path — is unchanged and still tested; the obstacle to an M-06 run is the unverified environment.)*
2. **Confirmatory contract (BLK-03, Q1 = A)**: `three_seed_mean` enforces all four limbs of `domain-entities.md` § 3 — `SeedError` / `AlignmentError` on the ordered (`station`, `interval_start_utc`) index (set AND order) / `PartitionError` / `LeakageError` — with provenance copied and `seed = None` on output. Change record exists FIRST, as the plan ordered.
3. **No scientific constant in source**: seeds, grids, the seven LSTM settings and ablation identities reach code only from `configs/`; tests re-read the counts 6/18/16 from `experiment.yaml` and never hold a real seed/grid value as a literal.
4. **Two-tier errors** throughout: integrity violations raise typed exceptions naming file and expectation; completeness shortfalls land as machine-readable manifest fields.
5. **Import boundary held**: `src/models` imports none of `src/external/iri.py`, `src/external/gim.py`, `src/evaluation`, or PyTorch; absence tested by identifier scan.

## Test coverage summary

**79 test functions total (67 + 12)**, re-derived 2026-09-20 on the working tree and printed
before assertion: `grep -c "^def test_" tests/test_models_smoke.py` = **67**,
`grep -c "^def test_" tests/test_checkpoint_restore.py` = **12**. Collected cases are **82**,
not 79: `tests/test_models_smoke.py` carries one `@pytest.mark.parametrize` over the four
`FITTED_MODEL_IDS` (67 − 1 + 4 = 70; 70 + 12 = 82). The two figures are stated separately
because they are not interchangeable.

This line has now been stale twice and is corrected in the body rather than in a review
addendum, per `project.md` (`code-generation:fr-2`): it read "66 (54 + 12)" until
2026-09-13, then "68 (56 + 12)" until this pass. Every hard rule carries a negative control
(team.md mandated practice): pin guard, closed model set, stamp match ×4, seed limbs,
tuning attestation, ablation refusals, `DEC` guard, receipt failure modes, and — new on
2026-09-20 — the M-03 key-coverage refusal, the three December-inference-only controls, the
frozen-epoch-rule refusal, the persisted-payload hash mismatch, and the `05 --partition DEC`
signature refusal.

**Execution status, stated plainly: NOTHING in this unit has been executed since
2026-09-06.** The generating session's run (2026-09-06T14:01Z) remains the only suite run,
it predates every change recorded in this artifact after that date, and it was **smoke
evidence only, never governed** (stdlib stand-in; pins not installable there). No test
written or amended on 2026-09-13, 2026-09-19 or 2026-09-20 has ever run: no usable Python
interpreter exists on this clone (`python.exe` is a zero-byte Windows Store alias stub) and
PyPI is unreachable. Every behavioural claim in this artifact dated after 2026-09-06 is
**static**, read from source. None of it may be read as "verified passing".

## Deviations from the plan

- **Step 7 NOT executed (designed outcome)**: precondition checked on disk — `evidence/DECISIONS.md` ends at D-32 (2026-08-28); no D-number dated on/after 2026-09-06 reopening D-27 exists. Per the approved plan: no inverse was added to `src/features/transforms.py` (verified: none exists), no `src/evaluation` → `src/features` edge added, and `ABL-DIFF` refuses naming D-27. The proposed D-number text sits in the change record for the owner to adopt; if adopted later, Step 7 runs under a fresh ruling.
- **No smoke re-run on this clone**: no Python interpreter exists here (Store stubs only). The generating session's suite run stands as the smoke evidence; nothing was re-executed on resume.
- **Owner commit da6cb7b** (2026-09-06 18:04 +0400, template message) carries this unit's entire code set and two governed-artifact changes with no D-number cited — team.md's linking rule requires D-121/change-record citation. Human act outside the stage; routed to the gate (fourth instance of the pattern: 06207c4, ed5808b, 6246907).

## Open items routed to the gate

BLK-03 evidence limb open at G-05; **TensorFlow pin FROZEN at `tensorflow==2.21.0` (D-36, `requirements.txt:36`) — the earlier "pin unfrozen / M-06 Keras path written-but-unexecutable" claim here is SUPERSEDED and was corrected 2026-09-20 under Recommendation 42; what remains owed is installability and Kaggle/local compatibility verification, so TA-26 stays `Pending`**; **two `configs/experiment.yaml` keys OWED and absent today — `models.climatology` (key `[station, hour]`, `fitted_on: training_partition_only`) and `models.refit` (`rule`, `epochs`) — without which `read_climatology_key` and `read_refit_epochs` refuse and no M-03 fit or refit can run (see § Remediation 2026-09-20)**; sklearn install evidence owed; pyarrow pin carried; FR-P1-05-2 bootstrap-seed attribution disagreement (raised, not edited); `prior_period_exposure` deviation note (R-102a); da6cb7b commit-message disposition; WS-14, WS-15, TA-12, TA-13, TA-26 all `Pending`; nothing discharged.

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

### Adversarial re-review at REJECTED gate (2026-09-13)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-13T10:15:11Z
**Iteration:** Adversarial re-review at REJECTED gate (2026-09-13), fresh verdict against HEAD `1670ac8`

#### Scope and method

Re-derived every count in this artifact independently against HEAD `1670ac8` before
reading any prior review's conclusion, per `project.md` (`code-generation:fr-2`). No
`graphify` executable is on PATH on this clone (verified again today); direct reads/greps
used as the sanctioned fallback per `CLAUDE.md`. No Python interpreter is installed on
this clone and PyPI is unreachable — no test was (re-)executed this pass; every test
result cited anywhere in this artifact is bounded as smoke evidence only, never governed,
consistent with prior passes.

#### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `code-summary.md:60` ("TensorFlow pin unfrozen") and `code-summary.md:29` (`requirements.txt` Files-table cell: "TensorFlow EXCLUDED with a comment naming the `TBD — freeze gate` rule") | Both are stale, current-body (non-historical) claims. `requirements.txt:36` carries `tensorflow==2.21.0` as a non-comment pin, and `evidence/DECISIONS.md` `## D-36` (decided 2026-09-10) states verbatim: "`requirements.txt` carries **`tensorflow==2.21.0`**... This supersedes the earlier `TBD — freeze gate` state." This artifact's own "Owner-rulings implementation review (2026-09-10)" section (line ~150) already independently confirmed the frozen, non-conflicting pin — but that finding was never swept into the "Open items" line or the Files table's description of `requirements.txt`, both of which still assert the pre-freeze (Step-6-time) state. Traced via `git log -- requirements.txt`: commit `17e0767` ("Implement owner rulings: ... TF pin ...") is this unit's own edit that added the pin, so the Files-table `+6` cell for `requirements.txt` (Step 6 only) was never updated to reflect this unit's own later self-edit either. This is the same "sweep every REPRESENTATION" failure mode `project.md` names repeatedly (`fd-2026-08-30-sweep-derive-sites`, `code-generation:fr-2`): one representation of the TF-pin fact was corrected (the 2026-09-10 review prose), two others were not (Open items; Files table). Note `TA-26 Pending` in the same Open-items clause is NOT stale — D-36 itself states the pin freeze "does not make the environment exist... TA-26 stays `Pending`," so only the "unfrozen" characterization is wrong, not the surrounding Pending status. | Rewrite `code-summary.md:60` to read "TensorFlow pin frozen at `tensorflow==2.21.0` (D-36); installability/Kaggle-compatibility verification owed, TA-26 `Pending`" and rewrite the Files-table `requirements.txt` cell to state the pin is now frozen (citing D-36), noting the freeze landed via a later self-edit (`17e0767`) after the original Step 6 `+6`. |
| 2 | Major | `code-summary.md:54` ("Deviations from the plan" — "`evidence/DECISIONS.md` ends at D-32 (2026-08-28)") | Stale current-body claim. `evidence/DECISIONS.md`'s tail is now **D-38** (`## D-38 — The split configuration is transcribed into the live configs`), with `## D-33` through `## D-38` added after 2026-08-28 — including `## D-37` (2026-09-10, "D-27 is affirmed; BLK-08's mechanism limb resolves in D-27's identity form"), which is exactly the D-27-adjacent decision this Deviations paragraph is about. The artifact's own "Floor-reset re-review (2026-09-11)" section (line ~244) already independently re-derived the correct tail ("`evidence/DECISIONS.md`'s final entry is **D-38**") but that correction was never swept back into the primary Deviations paragraph two review iterations later. The paragraph's *conclusion* is still correct in substance — no entry among D-33…D-38 reopens D-27; D-37 reaffirms it as permanently withheld, so Step 7 remains correctly unexecuted — but the artifact now contradicts itself between its own sections about how many decisions exist. | Update `code-summary.md:54` to state the current tail (D-38) and cite D-37 by name as the reaffirmation that keeps Step 7 gated, rather than restating the 2026-08-28 snapshot as if current. |

No further Critical, Major, or Minor finding survives verification. Every count and
commit-state claim in the artifact was re-derived, not carried:

- **Every Files-table line count matches exactly at HEAD `1670ac8`** (re-derived via `wc -l`,
  not carried from any prior review): `persistence.py`=135, `climatology.py`=235,
  `ridge.py`=145, `random_forest.py`=188, `checkpoint.py`=182, `lstm.py`=**373**,
  `train.py`=1487, `scripts/06_train_and_predict.py`=**999**,
  `tests/test_models_smoke.py`=**1393**, `tests/test_checkpoint_restore.py`=209. All ten
  match the table's current (non-superseded) cell values exactly.
- **Test-function counts**, distinguished from executed-case counts as the dispatch
  requires: `grep -c "^def test_" tests/test_models_smoke.py` = **56** (a `def test_`
  count, not a parametrized-case count — no `@pytest.mark.parametrize` collection
  expansion is claimed anywhere in this artifact for this file);
  `tests/test_checkpoint_restore.py` = **12**. Total **68** (56+12), matching the
  "Test coverage summary" section's already-corrected line 44 exactly — the 66/54 figures
  appearing at lines 44 (quoted, as superseded), 46-47 (quoted, as superseded), 93 and 179
  (both inside frozen 2026-09-06/2026-09-11 historical review blocks, correctly describing
  those blocks' own point-in-time derivations) are all either explicit corrections quoting
  the old figure to fix it, or frozen historical record — none asserts 66/54/367/741/1221/794
  as CURRENT fact. This sweep is clean.
- **Repository/commit state, re-derived, not carried**: `git status` shows this
  `code-summary.md` itself as the only uncommitted change touching this unit's own
  directory (this pass's in-progress edit); no other file this unit owns is uncommitted.
  `da6cb7b` (2026-09-06, unedited template commit message) is confirmed via
  `git show --stat` to carry `scripts/06_train_and_predict.py` (new), all six
  `src/models/*.py` files (new), both test files (new), plus modified `requirements.txt`
  and `configs/experiment.yaml` (governed) — with no D-number cited in the message,
  matching the artifact's own claim exactly. The uncommitted sibling-owned files visible in
  `git status` (`tests/test_determinism.py`, `tests/test_phase_boundary.py`,
  `tests/test_phase_contract.py`, `src/evaluation/guards.py`, and other units'
  `code-summary.md` files) belong to other units' in-flight work and are not attributed to
  this unit anywhere in this artifact — correctly.
- **Gated Step 7**: confirmed still unexecuted. `src/features/transforms.py` carries no
  `inverse`/`apply` method on any transform (grep confirms only `apply_fitted_transform`,
  the forward path); `ABL-DIFF`'s refusal in `src/models/train.py` still names D-27; no
  entry in `evidence/DECISIONS.md` after 2026-09-06 reopens D-27 — `## D-37` (2026-09-10)
  explicitly reaffirms it as permanent ("the refusal IS the mechanism"), and `## D-38`
  (split-configuration transcription) is unrelated to D-27.
- **TensorFlow pin substance** (distinct from the stale-claim finding above): the pin is
  genuinely frozen (`requirements.txt:36`, `tensorflow==2.21.0`, D-36) and genuinely
  unverified (no install has ever succeeded on either governed platform per D-36's own
  text) — both facts hold simultaneously and the code (`_require_frozen_pin()` guard,
  no module-scope `tensorflow` import) is unaffected by the artifact's stale prose.
- **Grids re-confirmed**: `configs/experiment.yaml` `combinations:` fields read 6 / 18 / 16
  for Ridge/RF/LSTM, matching the Files table and the D-121 citation.
- **Standing invariants held**: no `GRU`/`residual`/`torch` identifier anywhere under
  `src/models/`; no credential/secret/API-key pattern in `src/models/`,
  `scripts/06_train_and_predict.py`, or `requirements.txt` (the only "secret" hits are a
  comment header and a cross-reference to the separate secret-scanning script); no
  December 2022 data content in either test file (only test names/comments describing the
  exclusion control); `configs/experiment.yaml`'s three freeze-gate fields
  (`declared_baseline_per_track`, `selection`, `selected`) still read literal
  `"TBD — freeze gate"`, unfilled by convenience; WS-14, WS-15, TA-12, TA-13, TA-26 remain
  named `Pending` and are not claimed discharged anywhere in the artifact.

#### Summary

Two Major findings survive this pass, both of the same class this project's memory
repeatedly names (`project.md` `fd-2026-08-30-sweep-derive-sites`,
`code-generation:fr-2`): a fact was corrected in one representation of this artifact (the
2026-09-10 and 2026-09-11 review sections) and never swept into the primary,
currently-read body (the "Open items" line, the Files table, and the "Deviations"
paragraph). Both are documentation-accuracy defects that misstate governance-critical
state at the point a human reads this artifact to approve the gate — one understates
progress already made (the TensorFlow pin IS frozen under D-36, only its installability
is outstanding), the other understates how many decisions have since been recorded (the
register runs to D-38, not D-32, and D-37 is the specific reaffirmation that keeps Step 7
correctly gated). Neither affects executable code, a test result, or a governed artifact's
content — every count, grid value, commit attribution, and standing invariant re-derived
this pass matches the artifact's current claims exactly, and Step 7 remains correctly
unexecuted. With 0 Critical and exactly 2 Major findings, this clears the stated
verdict bar (`≤2 Major` is READY) but both should be corrected before the next reader
relies on this artifact's "Open items" or "Deviations" sections at face value.

---

## Remediation 2026-09-20 — `GOV-2026-09-20-CG-01` Recommendations 2, 5, 6 and 42

Filed under `CR-2026-09-20-GOV-CG-01-DISPOSITIONS`. The receipted `## Review` verdict block
above is a human-signed record and is **left standing untouched**; this block records what
changed after it, and the Files table, § Test coverage summary and § Open items above have
been corrected in the body so a reader who never reaches this block is not misinformed
(`project.md` `code-generation:fr-2`). Recommendation 42's owner ruling was explicitly
**"annotate in place"**, which is the authority for editing this completed-stage artifact.

**Nothing below was executed.** No interpreter exists on this clone. Every statement about
behaviour is static, read from source.

### Recommendation 2 — M-03 climatology key (owner ruling, verbatim)

> "Redefine M-03 as the mean VTEC by **station and hour**, calculated exclusively from each
> partition's training data. Remove month from the key, document the seasonal limitation,
> and fail early if a required key is missing. Record the definition before G-05 and verify
> it without accessing the locked test."

`src/models/climatology.py` now reads the key from `configs/experiment.yaml`
`models.climatology.key` (TC-03e — the key is never spelled as a constant in source);
implements `("station", "hour")` exactly and refuses any other configured key **by name**,
so a month-bearing key cannot be re-adopted by a config edit alone; refuses a `fitted_on`
other than `training_partition_only`; and raises at **fit** time — `assert_keys_cover_scored_rows`,
one guard home called from `fit_climatology` (fold path) and `predict_rows_from_state`
(persist path) — naming the missing keys, the fitting range and the config field. The
seasonal limitation travels on `Climatology.limitation` and on every prediction frame as
`climatology_limitation`, so it cannot be dropped between fit and report.

### Recommendation 5 — refit epoch count (owner ruling, verbatim)

> "Determine the final epoch count from the median best-validation epoch across the
> predefined pre-December folds and seeds, rounding half upward. Freeze this rule and its
> resulting value before G-05. Retrain from scratch on January–November, save and hash the
> models, and make December strictly inference-only. Verify the complete path using
> synthetic data; December must never influence training or model selection."

The rule is implemented as `train.refit_epoch_count` (integer median, half rounded UP by
`-(-(a+b)//2)` rather than `round()`, which rounds half to even); its identifier is
`train.REFIT_EPOCH_RULE_ID`; the value it produced is read from
`configs/experiment.yaml` `models.refit.epochs` and **refused while that field is
`TBD — freeze gate`** rather than defaulted. `assert_refit_epochs_match_rule` re-derives the
value from the recorded fold epochs so a transcription cannot drift from the rule.
`lstm.fit_state` takes an explicit `validation_bundle` — on a fold, early stopping and the
lowest-validation-RMSE restore read that bundle; on the refit there is none, and the model
trains for exactly the frozen count with no selection at all. Both structural guards live in
`train` (`assert_not_locked_fit`, `assert_validation_bundle`) and run from `fit_predict` and
`fit_and_persist`, so no fitted family can be fitted on `DEC` and no `DEC` bundle can be
offered as a validation set.

### Recommendation 6 — the G-06 path executes (owner ruling: option 2)

`scripts/05_build_features_and_splits.py` gains a `--partition DEC` branch behind the same
`materialise_locked_partition` G-05 signature guard, requiring `--g05-signature`,
`--locked-input`, `--locked-authorization` and `REFIT` in the same run; it never names the
restricted root and reads December only through `locked_test.open_restricted`, which writes
the `AccessRecord`. `scripts/06`'s `REFIT` iteration now fits and persists (hashed) instead
of being skipped, and the `DEC` iteration loads those records and predicts. *(That `05`
change is code this unit's summary does not own — `scripts/05` belongs to
`features-and-splits`, whose own record is stale for it; carried to the gate as a disclosure
item rather than edited here.)*

### Recommendation 42 — the stale TensorFlow claims

Corrected in the Files table, § Key implementation decisions item 1 and § Open items above.
Derivation printed: `grep -n tensorflow requirements.txt` → the pin is at **line 36**
(`tensorflow==2.21.0`); line 29 is its explanatory comment. The two source docstrings
(`src/models/lstm.py`, `scripts/06_train_and_predict.py`) were corrected in the same
remediation, as were two stale sites inside `tests/test_models_smoke.py` (the module
docstring and the § 11 section header) that the finding did not enumerate.

### What is owed before this is closed

1. **Two `configs/experiment.yaml` keys, absent today.** `models.climatology`
   (`key: [station, hour]`, `fitted_on: training_partition_only`) and `models.refit`
   (`rule: median_best_validation_epoch_across_folds_and_seeds_round_half_up`,
   `epochs: "TBD — freeze gate"` until the folds have run). Verified absent 2026-09-20 by
   `grep -n "climatology\|refit" configs/experiment.yaml` — zero matches for the former, one
   comment-only match for the latter. Until they exist, `read_climatology_key` and
   `read_refit_epochs` refuse and neither an M-03 fit nor the refit can run. The config file
   is outside this remediation's write scope; the keys are reported as owed, not written.
2. **Two D-numbers**, drafted for the owner at `CR-2026-09-20-GOV-CG-01-DISPOSITIONS`
   §4.1 (M-03 key) and §4.2 (refit epoch rule), both requiring supervisor countersignature
   before G-05.
3. **Execution.** Nothing here has run. `ruff check` and the full suite in the governed
   Python 3.11 environment are the first execution any of this code will have had.

## Post-receipt amendment — 2026-09-24 (D-28 option (b) / D-68: wiring the bounded 1-December persistence-history lookup)

*Appended under `project.md` `code-generation:gf-3`. Nothing above is rewritten; the READY
receipt stands as history. Authority: Student ruling — D-68 ruled, then explicit
authorization same day to connect the mechanism to the live prediction path.*

**What changed, measured (`git diff --numstat` vs the receipted state).** One file this
unit owns: `scripts/06_train_and_predict.py`. New import
(`PERSISTENCE_HISTORY_CALLERS`, `read_persistence_history_lookup` from
`src.data.locked_test`); new helper `_persistence_history_augmented_target(...)`; three
new optional keyword parameters on `_locked_predictions` (`g05_signature`, `locked_input`,
`access_log`, all defaulting to `None`); the one production call site updated to pass
`args.g05_signature`, `Path(args.locked_input)`, `access_log` — the same three values the
script's existing DEC loader already uses for `materialise_locked_partition`, reused
rather than re-derived.

**Why.** D-68 (`evidence/DECISIONS.md`) authorizes the mechanism
(`src.data.locked_test.read_persistence_history_lookup`, built in `governance-guards`'
own file, disclosed in that unit's code-summary); this amendment connects it so M-01/M-02
actually receive the 1-December lookup history during a real DEC iteration, recovering the
full D-28/D-59 30-day scored set. Full design and rationale:
`governance/CHANGE_RECORD_2026-09-24_d28_option_a_wiring.md`.

**Verified, not merely reasoned.** New test
`tests/test_models_smoke.py::test_persistence_history_augments_only_m01_m02_and_only_with_all_three_inputs`
(monkeypatches the mechanism itself to isolate the wiring from its own already-tested 5
conditions): confirms a non-M-01/M-02 model_id is untouched and the lookup is never
invoked; M-01/M-02 with all three inputs receive an augmented frame carrying exactly the
extra row(s); M-01/M-02 with any input missing raises rather than silently falling back.
Full `tests/test_models_smoke.py`: 71/71 passed (70 existing + 1 new), 1 skipped
(pre-existing, unrelated). `ruff check` on the modified file: clean — confirmed the initial
run's one finding (a literal restricted-root path string tripping the R-28 one-door
scanner) was in the TEST file, not this script, and was fixed there. Full §18.3 critical
set plus every module touching this script, re-run together: submitted, see the wiring
change record for the completed result.

**What this amendment does NOT do.** It does not change `locked_target` itself or any
FITTED family's target — `predict_from_fitted` still receives the plain, unaugmented
`locked_target`; only M-01/M-02's own `fit_predict` call receives the augmented copy, built
fresh per call and never persisted or mutated in place. It does not touch D-28 or D-59.
It does not weaken any of D-68's 5 conditions, all still enforced inside
`read_persistence_history_lookup` itself (owned and tested in `governance-guards`' own
file) — this amendment only supplies real call-site arguments.

---

## Addendum 2026-09-24 — GOV-2026-09-24-BT-01 remediation (post-receipt amendment, gf-3)

Under the Student's rulings (`governance/CHANGE_RECORD_2026-09-24_GOV-BT-01_rulings.md`):
`src/models/persistence.py:29–46` — Rec 8: the module docstring's "history is NOT supplied
today… a supervisor question, routed separately" was the negation of the live D-68 state and is
rewritten to describe the D-68 lookup (student-ruled, wired, post-G-05-gated, killable), with the
module's own lookup-only behaviour explicitly unchanged. `scripts/06_train_and_predict.py` —
Rec 10: `run_id` threaded through `_locked_predictions` → `_persistence_history_augmented_target`
→ the D-68 lookup; absent/empty refuses for M-01/M-02. `tests/test_models_smoke.py` — wiring test
extended: asserts the run_id threading and the absent-run_id refusal. Verification:
`rem1.xml` (445/448, failures elsewhere). Disclosure only; the receipt stands.

## 2026-09-25 cross-unit staleness addendum (gf-3, build-and-test item 4)

Following the 2026-09-24 addendum above (Rec 8 docstring rewrite, Rec 10 `run_id`
threading into `src/models/persistence.py` / `scripts/06_train_and_predict.py` /
`tests/test_models_smoke.py`), one further build-and-test event touches this unit's
evidence disclosure:

- **TF/matplotlib pin surface (readiness item 2) — CLOSED locally, 2026-09-25.**
  `tensorflow==2.21.0` is now installed at the exact governed version in
  `tec-thesis-311` (was unobtainable as of the 2026-09-24 run). This unit's
  `src/models/lstm.py` TF-present paths are now exercisable in this environment for
  the first time; no M-06 fit has run under this closure, and the TE §8.1
  both-platform (Kaggle AND local) check remains outstanding (batched with item 3's
  Q-31 freeze — see `build-test-results.md`'s Kaggle runbook). This does not change
  any claim this unit's own artifact makes about M-06's fit status, which stays
  `Pending`.

This addendum discloses per `project.md` `gf-3`; the receipt stands as history and is
not reopened.

## 2026-09-25 cross-unit edit addendum (gf-3, build-and-test item 3)

`src/models/train.py: _read_selection_block()` and one line of `select_configuration()` now read
the owner-transcribed key names — `models.selection.simplicity_margin` (D-124, via
`CR-2026-09-21-RECONCILIATION` §2) and the sibling `models.declared_baseline_per_track.all_tracks`
(D-58) — instead of `selection.simplicity_tolerance_fraction` and `selection.declared_baseline`,
which this unit wrote while all three fields were still `TBD — freeze gate` and which no governed
record ever named. Against the real config the old names made `select_configuration()` refuse.
`tests/test_models_smoke.py`: one synthetic snapshot updated to the transcribed names, and one new
control, `test_selection_reads_the_real_transcribed_config_keys`, which reads the real file and pins
the retired names as refused. Module run: **72 tests, 71 passed, 0 failed, 1 skipped**
(pre-existing sklearn-present skip); the new control fails against HEAD's `train.py`, proving it
bites. Full record: `governance/CHANGE_RECORD_2026-09-25_selection_block_key_names.md`. Edited
under this unit's frozen receipt on the Student's explicit instruction (`project.md`
`code-generation:c32`); the receipt stands as history and is not reopened. Test-count claims
above this addendum (e.g. "55 passed") predate it and are not current.

## 2026-09-25 second cross-unit edit addendum — target loader implemented, --tune added

`scripts/06_train_and_predict.py: _load_target_by_manifest` was an unconditional stub (refused
even when the release manifest existed) -- implemented for real this session: reads the
manifest, calls `src/data/release.py: verify_release()`, reads the declared CSV(s), drops
`target_valid != "True"` rows (D-5), returns a real frame. Verified against `plumbing_7day`'s
actual release: 158/168 rows load (10 QC-dropped, matching the manifest's own recorded counts).

Added `--tune`/`--probe`/`--tune-out` to the same script: a fixture-scale D-124 selection
orchestrator (enumerate_grid -> fit_predict/lstm.fit_predict_rows -> CandidateScore ->
select_configuration), resolving the fixture/models.selected deadlock per the Student's chosen
option (fixture-scale, advisory-only, never written to configs/experiment.yaml). Disclosed, not
fixed: `fit_predict()`'s approved signature carries no `CheckpointBackend` parameter, so LSTM
cannot be fold-fitted through it at all (governed or fixture path) -- `_fit_candidate()` calls
`lstm.fit_predict_rows` directly for that one track, in-memory backend, mirroring what
`fit_predict` would do if it forwarded one. Complexity ordering for R-101's simplicity tie-break
is PROPOSED (no governed record states a formula) and flagged as such in the code.

Real probe run, plumbing_7day, one LSTM candidate/one fold: skill=-3.0040 (mechanism check, not
a scientific result), ~35s per LSTM fit, ~50s total incl. one-time TF import. Ridge path
direct-called, sub-second. A real bug (silent NaN skill from unfiltered persistence-model gap
rows) was found and fixed during this verification. Full record:
`governance/CHANGE_RECORD_2026-09-25_target_loader_implementation.md`. Edited under this unit's
frozen receipt on the Student's explicit instruction; the receipt stands as history and is not
reopened.
