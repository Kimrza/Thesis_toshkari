# TEC_Project review criteria

## Immediate blockers

Block `PASS` for any of the following:

- a required value remains `TBD — freeze gate`, or an agent/default supplied it without evidence and human approval;
- the current Vision is missing, superseded, contradicted, or not tied to the artifact;
- an IRI value, residual, target, transformation, or derived field reaches ML training or inference;
- an IRI/GIM module is imported into feature/model code rather than joined at evaluation;
- December 2022 performance was accessed before G-05, predictions were regenerated/overwritten, or metrics preceded the prediction hash;
- a December-informed feature, model, threshold, hyperparameter, mask, seed, or analysis change is presented as confirmatory;
- random/shuffled validation, boundary-crossing windows, future-aware interpolation, centered F10.7 mean, all-data scaling, or target-hour QC leakage appears;
- folds are not F1–F4 with the governed 24-hour embargo and December-only locked test, absent an approved pre-tuning change record;
- models sit different exams through pairwise/model-specific masks or unequal eligible information/windows;
- persistence, 24-hour seasonal persistence, or fitted climatology is omitted from the primary results table;
- the paired-loss sign is reversed or unstated, equal-station weighting is missing, or the vector block bootstrap does not carry all stations together;
- a Phase 2 confirmatory run changes a protected Phase 1 model/protocol hash, carries fitted Phase 1 weights without an exploratory label, or calls December a second blind holdout;
- a target silently mixes providers/products, substitutes GIM for missing station VTEC, imputes primary targets, or obscures IPP-versus-station-zenith mismatch;
- a dataset/model/prediction/config release lacks provenance, identifiers, immutable hashes, or required failed-run records;
- copied/adapted code lacks a compatible license decision, source commit, notices, modification record, citation, isolation, or tests;
- a geographic, operational, positioning, commercial, multi-year, or arbitrary-location claim exceeds the approved three-station 2022 +1-hour boundary.

## Scientific and data checks

- Preserve ARUC, BSHM, and NICO as three correlated stations, not independent spatial samples.
- Require official station logs as registry authority; use headers only as cross-checks.
- Require one common Phase 1 provider/product/physical definition and an explicit coverage decision before training.
- Preserve GPS-only primary scope and governed observables/cadence unless a change record approves otherwise.
- Require transparent DCB source, units, sign, hand-worked pass, and reversed-sign negative control.
- Treat mapping, shell, cutoff, slips, arcs, levelling, support thresholds, fixture dates, and processor tolerances as evidence-frozen values.
- Require two independent reference checks and a target uncertainty budget before accepting Phase 2 VTEC.
- Keep Dst diagnostic/hindcast-only, SSN absent, Kp/ap lag at least 3 h, Hp60/ap60 lag at least 1 h, observed F10.7 lag 1 day, and its 81-day mean trailing.

## ML and statistical checks

- Confirm +1-hour horizon, 24-hour primary history, lags `[1,2,3,24]`, pooled models, station one-hot plus verified latitude, and longitude only through local solar time.
- Confirm exact frozen grids: ridge 6, RF 18, LSTM 16; development seed 42; final seeds 1337, 2024, 7; bootstrap seed 20221201.
- Confirm the three-seed element-wise mean is the confirmatory LSTM prediction and failed runs remain visible.
- Confirm the primary estimand is IRI squared loss minus LSTM squared loss, so positive favors LSTM.
- Confirm 10,000 24-hour vector block replicates, a 48-hour sensitivity, and reported cross-station paired-error correlation.
- Keep ablations predeclared and subordinate to the frozen primary analysis.
- Require top-1%-error-removed sensitivity and target uncertainty adjacent to the primary result.

## Model-advancement test

Issue `ADVANCE` only when all are true on frozen evidence:

1. The approved primary statistical evidence rule is satisfied for LSTM versus IRI.
2. LSTM improves over persistence on the same comparison-wide mask.
3. Seasonal persistence and climatology results are co-reported and do not contradict the proposed claim.
4. Aggregate gain is not driven by one station; each station is reported and any weakness is scientifically explained without concealment.
5. Behavior across diurnal, seasonal, geomagnetic, and support strata is physically defensible.
6. The effect is interpreted against the target uncertainty budget and not rescued by post-test ablations or extreme hours.

If any condition fails, issue `DO NOT ADVANCE` and state whether the evidence is negative, inconclusive, or invalid. A valid `DO NOT ADVANCE` result may still receive a process-gate `PASS`.

## Reproducibility and implementation checks

- Require Python 3.11 exact pins, per-run environment capture, local and Kaggle evidence, and a complete CPU path.
- Require exactly four governed configs and visible sentinels for unresolved non-applicable work; no scientific constant hidden in source or notebooks.
- Require the two fixtures and their measurable evidence; the seven-day LSTM is a smoke test, never scientific evidence.
- Require critical negative-path tests: IRI injection, reversed DCB sign, phase boundary, split embargo, train-only transforms, common masks, locked guard, release hashes, bootstrap correlation, and protected-hash drift.
- Require atomic/append-safe registry behavior and preserved failed/aborted runs.
- Keep notebooks as review/presentation surfaces that call reusable modules.

## Severity guide

| Severity | Meaning |
|---|---|
| BLOCKER | Violates authority, scientific validity, locked-test integrity, human freeze ownership, phase integrity, or required gate evidence; prevents `PASS` |
| MAJOR | Material risk to correctness, reproducibility, fairness, or defensible interpretation; normally prevents `PASS` until fixed |
| MINOR | Bounded non-blocking defect with a clear owner and closure point |
| NOTE | Observation or optional improvement with no gate effect |
