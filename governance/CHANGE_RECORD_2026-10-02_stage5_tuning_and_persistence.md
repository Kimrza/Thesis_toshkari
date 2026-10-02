# CR-2026-10-02-STAGE5 — governed full-year tuning, the M-06 fold and refit paths, refit persistence, and Fixture 2's budget output

**Date:** 2026-10-02. **Author:** the agent, under the Student's mandate for autonomous closure
(Stage 5) and the rulings recorded in **D-89**. **Decision class:** implementation of approved
decisions (D-124, D-58, D-121, D-56, D-89).
- No scientific value is chosen here.
- `configs/` is not touched.
- No value is written into `models.selected` or `models.refit.epochs`.

## Why

Planning the full-year tuning against the code surfaced five gaps. None had been exercised,
because the fixture path skips the refit and `--tune` ran at fixture scale only:

1. **No governed tuning run existed.** `06 --tune` refused without `--fixture-manifest`.
   CR-2026-09-25 recorded that `models.selected` may be frozen "only [by] a real full-year
   F1-F4 run".
2. **The governed F1-F4 path could not fit M-06.** It called `train.fit_predict("M-06")`, which
   carries no `CheckpointBackend`, and `lstm.fit_state` refuses without one. This is the
   "second gap" CR-2026-09-25 recorded and did not fix.
3. **REFIT and DEC could not persist or load M-04, M-05 or M-06.** `JsonStateBackend` refuses a
   fitted estimator or Keras weights as "a governed choice that does not exist yet". The
   Student made that choice on 2026-10-02 (D-89: `.keras` and joblib).
4. **`assert_refit_epochs_match_rule` had no caller.** A transcribed `models.refit.epochs` was
   never checked against the fold epochs it is derived from.
5. **Fixture 2's `target_uncertainty_budget.json` had no producer.** TE §15.4 lists it as
   "fixture 2 only". Scientific rehearsal 6 (2026-10-02) reached the artifact listing and
   refused there.

## What changed

**`src/models/train.py`**
- `select_configuration` applies D-89:
  - an absolute margin, strictly less than `simplicity_margin`;
  - complexity first, then higher mean skill, then the params string.
- `complexity_proxy` replaces the PROPOSED ordering, with the identifiers
  `SELECTION_MARGIN_RULE` and `COMPLEXITY_PROXY_RULE`.
- `ModelFileStateBackend` (D-89):
  - M-03 is stored as JSON; M-04/M-05 as joblib; M-06 as `.keras` plus a JSON sidecar
    carrying the `.keras` SHA-256;
  - every file is write-once;
  - `predict_from_fitted` re-hashes the record's payload before `load_state`, and the sidecar
    path re-hashes the `.keras` file before loading.
- `fit_and_persist` and `predict_from_fitted` take a separate `checkpoint_backend`, forwarded
  to the family as its `backend`.

**`src/models/lstm.py`**
- `save_keras_model` rebuilds the model with `build_keras_model` (the one architecture
  definition), sets the selected weights, and writes a `.keras` file once.
- `KerasFileCheckpointBackend` is inference-only: it loads weights from a persisted `.keras`
  file and refuses to save.

**`scripts/06_train_and_predict.py`**
- The governed `--tune` (no `--fixture-manifest`) runs over the D-124 F1-F4 folds:
  - Precondition: the criterion declaration and the Student's attestation are read and
    checked through `record_tuning` (R-95, SD-M-01).
  - Precondition: a logged December performance read since the declaration refuses the run.
    The scan reads the active governed and test-suite logs; the closed log cannot gain rows.
  - Precondition: the two fixture receipts (TE 9.2).
  - Every grid point of every track is fitted per fold, with the development seed for M-06
    (Vision line 837).
  - Each (track, fold) is scored against M-01 on one comparison-wide mask (NFR-FAIR-01).
  - Selection uses `select_configuration`.
  - The D-56 rule is then evaluated over the selected LSTM on F1-F4 with the final seeds.
  - It writes a write-once tuning record with a SHA-256 sidecar, and a per-fit progress log.
  - It never writes `configs/`.
- The fixture `--tune` uses the development seed and `complexity_proxy`.
- The governed F1-F4 path fits M-06 through `lstm.fit_predict_rows` with the in-memory
  backend. It collects each (fold, seed) restored epoch.
- REFIT first re-derives D-56's value from those epochs (`_assert_refit_epochs_from_folds`),
  then persists through `ModelFileStateBackend`.
- DEC loads through `ModelFileStateBackend`, with the `.keras` loader for M-06.
- An M-06 per-seed prediction payload carries its `checkpoint` facts (restored epoch, RMSE,
  epochs run). This is additive; `predictions.parquet` reads identity columns only.

**`scripts/07_evaluate_and_report.py`**
- Fixture 2 writes `target_uncertainty_budget.json` as a write-once byte copy of the
  `--budget-artifact` its reporting layer already reads. Nothing is recomputed.

**`tests/test_stage5_tuning_and_persistence.py`** (new) covers:
- the selection rules: absolute margin, strictness, tie-break, zero margin, the proxy values;
- the joblib round trip, write-once refusal and tamper refusal before load;
- the `.keras` round trip and tamper refusal, run in a fresh interpreter (R-05);
- the governed tune's mask RMSE, its December-access scan, and the D-56 re-derivation guard.

## Verification

- The full suite ran in the dev clone, excluding the three restricted December readers, which
  run in the governed tree so the access log stays in one place. The single failure
  (`test_governed_access_logs`: a script may not name the closed log) was fixed by reading the
  `locked_test` constants.
- `ruff`: no new findings.
- **Plumbing (D-88)** is re-verified at this commit in both environments before any
  scientific run (P-1 rule).

## Effect

- **Leakage:** stronger. Tuning reads F1-F4 only, refuses after a December performance read,
  and binds its criterion to a declared and attested hash. REFIT checks its epoch count
  against fresh fold fits.
- **Comparability:** every tuning comparison uses one mask per (track, fold).
- **Claim:** none.
- **Knowledge graph:** `graphify-out/` is stale for the touched files; no `graphify` CLI is
  installed.
