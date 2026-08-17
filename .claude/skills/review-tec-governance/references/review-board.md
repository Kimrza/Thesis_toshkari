# TEC_Project review board

## Operating model

Use a compact five-seat board by default. Add two independent seats for full-board reviews. Reviewers recommend; the student or supervisor approves.

Anyone who built, tuned, selected, or materially changed the artifact or model may present evidence but must not chair its final validation decision. Record conflicts before review. If the nominal Chair is conflicted, assign an independent human decision owner; the AI board still has advisory authority only.

## Five-seat board

| Seat | Evidence focus | Blocking concerns |
|---|---|---|
| Review Chair / Decision Owner | Gate scope, acceptance criteria, authority order, conflicts, consolidated decision, locked-set governance | Missing approver, authority conflict, unclosed blocker, informal waiver, conflicted chair, unauthorized gate progression |
| TEC & Space-Weather Expert | TEC physics, IPP target meaning, DCB/mapping/QC, station behavior, Kp/ap/Hp60/ap60/F10.7 timing, Dst diagnostic-only, seasonal/diurnal plausibility | Implausible target or behavior, unsupported target definition, future-aware driver, unexplained station offset, physical mismatch hidden from interpretation |
| ML & Statistical Methods Reviewer | Leakage, feature contract, folds/embargo, train-only transforms, grids, seeds, masks, ablations, paired estimand, bootstrap, uncertainty | IRI contamination, temporal leakage, test-driven selection, pairwise masks, wrong sign/weighting/bootstrap, statistically unsupported promotion |
| Data Quality & Reproducibility Reviewer | Source inventory, schema/units/time, missingness, station coverage, manifests/hashes, experiment registry, clean run | Mixed or untraceable target sources, silent imputation, mutable release, missing failed runs, non-reproducible evidence, missing provenance |
| Benchmark & Deployment Reviewer | IRI and GIM separation/validation, persistence ladder, compute/storage/runtime, operational usefulness and claim boundary | Missing difficulty controls, unfair comparison, unvalidated benchmark, GPU-only path, operational claim without evidence, resource infeasibility |

## Full-board additions

| Seat | Exclusive focus | Veto condition |
|---|---|---|
| Validation Auditor | Sole independent custody review for December 2022, access log, write-once prediction generation, pre-metric hash, frozen masks/configs, Phase 2 prior-period exposure | Any unauthorized access, missing access record, post-result change, overwritten prediction, absent pre-metric hash, or false second-blind-holdout claim |
| Implementation Reviewer | Code boundaries, tests, dependency pins, maintainability, runtime, phase-transition hash enforcement, reuse adapters and license controls | Protected Phase 1 protocol drift, raw/forecasting boundary violation, missing critical tests, unpinned environment, incompatible or unattributed reused code |

## Activation rules

| Artifact or decision | Required reviewers |
|---|---|
| Scientific framing, hypotheses, scope, claims | Chair; TEC; ML/Statistics; Benchmark |
| Prepared-source, station registry, target/QC | Chair; TEC; Data/Reproducibility |
| Features, splits, masks, tuning, metrics | Chair; ML/Statistics; Data/Reproducibility; TEC when space-weather or target fields are involved |
| Architecture, code, tests, environment | Chair; Data/Reproducibility; Implementation; add ML/Statistics for model/evaluation code and TEC for GNSS code |
| IRI/GIM, persistence ladder, compute or usefulness | Chair; Benchmark; TEC; ML/Statistics when metrics or fairness are involved |
| G-05, G-06, G-P2, G-P3, locked test, model advancement, final claims | All seven |

For an ordinary stage, require the Chair plus at least two relevant independent specialist passes. Full-board reviews require all seven passes. An unavailable required reviewer makes the review `NOT REVIEWABLE`; do not replace expertise with a generic majority vote.

## Deliberation rules

1. Preserve reviewer independence until individual findings are recorded.
2. Do not decide by vote alone. A supported veto in the reviewer's exclusive domain blocks `PASS`.
3. Require evidence to downgrade severity or close a finding.
4. Record unresolved disagreements and the authority clause that governs them.
5. Let the Chair consolidate, not erase, dissent.
6. Keep optional improvements separate from gate obligations.
