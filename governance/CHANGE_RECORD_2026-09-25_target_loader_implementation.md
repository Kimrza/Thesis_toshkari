# Change Record — target-manifest loader implemented; `--tune` fixture-scale orchestrator added

**Date:** 2026-09-25
**Change ID:** CR-2026-09-25-TUNE-ORCHESTRATOR
**Owning unit:** `models-and-baselines` (`scripts/06_train_and_predict.py`), edited under that
unit's frozen receipt on the Student's explicit instruction, following the answers given to the
deadlock/location questions asked this session (deadlock resolved as "fixture-scale selection";
orchestrator location resolved as "a `--tune` mode in `06`").

## Background: the fixture / `models.selected` deadlock

`build-and-test` item 3's runbook (this session, earlier) found that a real, governed F1-F4
tuning run cannot execute: TE §9.2's Class C ("full-year scientific processing") requires both
walking-skeleton fixtures to have passed first, but the fixtures' own `06` path calls
`_selected_params()` for every model on every fold, which refuses while `models.selected` is
`TBD — freeze gate` — and `models.selected` is the tuning run's own output. Neither side can go
first.

**Resolution, on the Student's instruction:** run D-124's selection mechanism at fixture scale,
over the fixture's own apparatus folds, writing an advisory result file — never the governed
`configs/experiment.yaml: models.selected` field, which only a real full-year F1-F4 run may
freeze. This breaks the deadlock without pre-empting the owner's freeze act.

## What was found and fixed

### 1. `_load_target_by_manifest` was an unconditional stub

Confirmed by direct reading, not inferred: the function raised `IntegrityError` on every call,
even when the release manifest existed on disk. This is upstream of every path through `06` —
fixture-scale and governed alike — and is the reason no prediction has ever been written for
`plumbing_7day` (confirmed: no prediction files existed under its artifacts tree before this
change). Implemented for real:

- reads the release manifest, calls `src/data/release.py: verify_release()` (the same
  hash/`content_hash`/`dataset_version` check `tests/test_release_hashes.py` runs) before
  trusting a byte;
- reads the declared `output_files` CSV(s) via `csv.DictReader`;
- drops rows with `target_valid != "True"` (a QC-invalid row, per the release manifest's own
  `exclusions_qc_summary`) — dropped, never imputed (D-5);
- returns a frame via `src/features/_frames.py: frame_from_records`, columns matching
  `src/models/train.py`'s `TARGET_TIMESTAMP_COLUMN`/`TARGET_STATION_COLUMN`/`TARGET_VALUE_COLUMN`
  exactly.

**Verified against real data**, not a synthetic fixture: `plumbing_7day`'s actual release
(`artifacts/walking_skeleton/plumbing_7day/releases/phase1_hourly_target/`) loads **158 rows**
(168 total, 10 dropped as QC-invalid — matches the release manifest's own recorded
`exclusions_qc_summary` and `by_qc_stage` counts exactly).

### 2. A second gap found, not fixed: `fit_predict`'s approved signature carries no `CheckpointBackend`

`train.fit_predict()` — the approved generic dispatcher (`component-methods.md`) — has no
`backend` parameter anywhere in its signature. `src/models/lstm.py: fit_state` raises
`IntegrityError` when `backend is None`. This means **M-06 (LSTM) can never be fold-fitted
through the generic `fit_predict()` call as it stands today** — not by this script, not by the
governed path either, since `06`'s own governed-partition loop calls the same `fit_predict()`.
This is a real gap in an *approved* boundary contract, not something to route around silently by
widening it without authorization (the same discipline this project already applies to
`write_release`'s raise-contract, `foundation`'s § Assumptions).

**Disclosed, not fixed here.** `_fit_candidate()` (new, this change) calls `src.models.lstm.
fit_predict_rows` directly for the `lstm` track only, passing an explicit
`_InMemoryCheckpointBackend`, exactly mirroring what `fit_predict()` would do if it forwarded a
backend. Ridge and Random Forest go through the unmodified generic `fit_predict()`. This is a
disclosed workaround for this script's own tuning use, not a change to the approved contract —
whether `fit_predict()`'s signature should be amended to carry a `backend` parameter (which
would also unblock the *governed* fold-fit path for M-06, a separate and larger question) is
routed here as an open item, not decided.

### 3. `--tune` / `--probe` / `--tune-out` added to `06_train_and_predict.py`

- `--tune` requires `--fixture-manifest` (enforced at argument-parse time); runs
  `_run_tune()` instead of the normal fixture or governed path.
- Enumerates all 40 grid points across the three D-121 tracks (`enumerate_grid`), fits each
  against the fixture's own apparatus fold partitions (never `DEC`, never a frozen `F1`-`F4`
  id — `build_apparatus_partitions` only ever returns fixture-declared ids), scores each as a
  `CandidateScore` (`mean_per_fold_skill`, Vision §8.7's `1 - RMSE_model/RMSE_baseline`), and
  calls `select_configuration()` per track — the same D-124 rule this session's step-1 fix made
  readable against the real config.
- Baseline: reads `models.declared_baseline_per_track.all_tracks`, asserts it is `"persistence"`
  (D-58), and maps it to **M-01** — TE line 456's own table (`M-01 | Persistence`), not assumed.
- **Complexity ordering for R-101's "prefer the simpler configuration" tie-break is PROPOSED,
  not committed** — no governed record states a formula (grepped the unit's functional design;
  zero hits). `_proposed_complexity()`: ridge `1/alpha`, random forest
  `n_estimators × (max_depth or 32)`, LSTM `layers × units`. Flagged in the code and here so the
  owner can replace it without touching the selection mechanism.
- Output: a single JSON file (default `<predictions-out>/tuning/tuning_result.json`,
  overridable with `--tune-out`), carrying an explicit `"advisory": true` / `"governed": false`
  flag and a note against copying it into `configs/experiment.yaml` without a real full-year run,
  the per-track winning params, each winner's mean and per-fold skill, and a full
  candidate-by-candidate audit trail (RMSE, baseline RMSE, skill, dropped-row counts, wall time).

### 4. A real bug found and fixed during verification: silent NaN skill

The first real run (LSTM, one candidate, one fold) produced `skill: NaN` with no error. Root
cause: `src/models/persistence.py` legitimately emits `NaN` `y_hat` for rows with no history at
the required lag within a short fixture window (a documented, correct missingness marker, D-5) —
my first `_rmse()` did not filter these before squaring, so one `NaN` silently poisoned the mean.
Fixed: `_rmse()` now drops both classes of missing row (`y_hat` `None`/`NaN`, and a target-series
miss) exactly as the model's own gap convention requires, and returns the dropped-row counts as a
machine-readable field in the per-candidate audit record rather than only a completeness note —
`team.md`'s two-tier posture (integrity violations raise; completeness shortfalls are recorded,
never console-text-only). Re-run after the fix: a real, finite skill value.

## Verification

**Real probe run**, `plumbing_7day` fixture, one LSTM candidate (`layers=1, units=32,
learning_rate=0.001, batch_size=64`), one apparatus fold (`FIX-NOV-FOLD-01`):

```
python scripts/06_train_and_predict.py --config configs/ \
  --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --bundles-root artifacts/walking_skeleton/plumbing_7day/features \
  --predictions-out artifacts/walking_skeleton/plumbing_7day/predictions \
  --tune --probe
```

Result: `rmse=16.1917`, `skill=-3.0040` (negative — expected and not scientifically meaningful at
one candidate / one 7-day fixture fold / development-seed defaults; this run's job was to prove
the mechanism executes, not to produce a real selection). **Wall time: ~35s for the LSTM
fit+predict call itself** (`elapsed` field), **~50s total process time** including one-time
TensorFlow import/CPU-feature-guard startup (paid once per process, not per candidate).

**Ridge path, direct-called** (bypassing the CLI to avoid TF's one-time import cost for a
30-second check): `alpha=0.01`, same fold — `rmse=3.6264`, sub-second. Confirms the
non-LSTM tracks work through the unmodified generic `fit_predict()`.

**Lint:** `ruff check scripts/06_train_and_predict.py` — clean, zero findings, both before this
change (188 pre-existing findings across the whole tree are untouched) and after (this file
alone: 0).

## Not run

The full 40-candidate × 2-apparatus-fold sweep (`--tune` without `--probe`) was **not** run —
scoped out of this pass per the Student's instruction ("Do not execute the full sweep
yourself"). Extrapolated from the probe: 16 LSTM candidates × 2 folds ≈ 32 fits × ~35s ≈ 19
minutes for the LSTM track alone; ridge (6) and random forest (18) candidates × 2 folds are
sub-second each and negligible by comparison, plus one ~15s one-time TF import if any LSTM
candidate runs. Real timing for the full sweep should still be measured, not assumed from one
data point.

## Not changed

`configs/experiment.yaml`; the governed (non-`--tune`, non-fixture) path through `06`; `models.
selected`; `models.refit.epochs`. No commit made by this session; committing is the Student's
act.
