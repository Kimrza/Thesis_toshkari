# Project-Level Rules

> Project-specific specialisation and corrections. Loaded after `org.md` and
> `team.md` as strict-additive guidance; contradictions with broader policy
> are rejected. Populated by practices-discovery and the self-learning loop.
>
> Use sparingly: most teams don't need a project layer. Reach for it
> only when this specific project needs stable, durable guidance beyond the
> team practice (for example, package-specific release checks or an additional
> regression suite for a legacy component).

## Way of Working

<!-- Project-specific specialisation. Example: -->
<!-- This monorepo requires package-scoped branch names and a package owner -->
<!-- review in addition to the team's normal merge policy. -->

- ALWAYS specify the inputs a gating condition depends on in the same stage that records the condition; deferring them leaves the condition unmeetable and uncheckable. (learned 2026-08-13) <!-- cid:intent-capture:c5 -->
- ALWAYS split raised assumptions into verification obligations this project must check and governance dependencies owned outside it, rather than one flat assumptions list. (learned 2026-08-13) <!-- cid:intent-capture:c3 -->
- ALWAYS honour a human's disposition by narrowing what a rule requires, never by relocating a rule that the governing normative core fixes; a stage answer cannot move a requirement out of the layer the authority document places it in. (learned 2026-08-13) <!-- cid:intent-capture:c7 -->
- ALWAYS check the drafted artifact against the governing normative core before the approval gate, not only the questions that produced it; contradictions between an artifact and the authority document are invisible to question-level checking. (learned 2026-08-13) <!-- cid:intent-capture:c4 -->
- ALWAYS raise a targeted follow-up when an answer would require building something before the work that specifies its contents; reinterpreting such an answer silently hides an ordering error that only surfaces once the wrong thing is built. (learned 2026-08-15) <!-- cid:approval-handoff:c3 -->
- ALWAYS enumerate every open supervisor gate from the governing authority's gate table in a phase handoff, not only the gates on the visible critical path; a partial list makes the unlisted gates invisible to the receiving phase. (learned 2026-08-15) <!-- cid:approval-handoff:c1 -->
- ALWAYS verify a fact independently before handing it to another reviewer as established input; a wrong fact promoted to established status is built upon rather than questioned, and the reviewer's conclusion inherits the error. (learned 2026-08-16) <!-- cid:practices-discovery:c-board-1 -->
- ALWAYS derive a count programmatically from the artifact and print it before asserting it; never carry a count from adjacent prose, from a finding's text, or from an earlier revision. Three counts asserted this way in one session were all wrong (a release-manifest field count, an untested-requirement list size, and a test-module count claimed to appear in four places when it appears in two), while every count derived from the artifact was right. (learned 2026-08-21) <!-- cid:application-design:application-design:count-derivation -->
## Walking Skeleton

<!-- Project-specific specialisation. Example: -->
<!-- The walking skeleton must exercise the legacy service adapter as well -->
<!-- as the new service boundary. -->

## Testing Posture

<!-- Project-specific specialisation. -->

## Deployment

<!-- Project-specific specialisation. -->

## Code Style

<!-- Project-specific specialisation. -->

## Tech Stack

<!-- Technology choices locked for this project. -->

## Decided

<!-- Decisions made in earlier stages that should not be re-asked. -->
<!-- Format: DECIDED: [decision] (Stage [slug], [date]) -->

## Scope Overrides

<!-- Custom scope rules for this project. -->

## Forbidden

<!-- Populated by practices-discovery affirmation gate. -->
<!-- Format: NEVER [behavior] (affirmed [date]) -->
<!-- Example: NEVER throw exceptions across service layer boundaries (affirmed 2026-05-17) -->

- NEVER let an `iri_*` field, an IRI-derived residual, or any IRI-computed value reach ML training or inference in the confirmatory experiment. (Vision §7.1; Technical Environment NFR-IRI-01.) (affirmed 2026-08-16)
- NEVER let Phase 1 code import or execute raw-processing modules (`src/gnss/rinex.py`, `src/gnss/calibration.py`) or produce DCB/STEC/mapping/ satellite/arc fields. (Technical Environment §7.0 "Phase 1 hard prohibition"; NFR-PHASE-01.) (affirmed 2026-08-16)
- NEVER use a centered rolling/trailing window for F10.7 — only the trailing 81-day mean ending at the safe-lagged day is permitted; a centered mean uses future days and is a defect, not a fallback. (Technical Environment §6.2 dictionary row `f107_81_trailing`; Technical Environment §10 "Centered means are a defect, not a fallback.") (affirmed 2026-08-16)
- NEVER use any Random Forest importance score to add, remove, or rank features into the production feature set; RF importance may only be saved as a non-authoritative diagnostic figure. (Vision §6.4 matched-representation rule, Technical Environment §6.4.) (affirmed 2026-08-16)
- NEVER treat a favourable LSTM result as license to omit an unfavourable baseline comparison from the primary results table or the abstract-level conclusion. (Vision §2.4 "Binding honesty rule".) (affirmed 2026-08-16)
- NEVER introduce, change, or reinterpret a practical-relevance threshold after the December locked test is opened. (Vision §5.4; `constraint-register.md` PC-09.) (affirmed 2026-08-16)
- NEVER impute, substitute, or reconstruct a value for the F10.7 outage window until the measured gap is recorded and governed. (`constraint-register.md` TC-20.) (affirmed 2026-08-16)
- NEVER label the Phase 1 gridded (Madrigal cell) target as receiver-specific station-observed VTEC; it is location-sampled gridded VTEC and must be described as such, with its distinct `target_definition_id`. (Vision §6.6 "Phase 1 prepared-target definition — conditional"; Technical Environment glossary.) (affirmed 2026-08-16)
- NEVER commit a credential, API key, or secret to a notebook, source file, configuration snapshot, log, or registry note. (Technical Environment §10; NFR-SEC-01.) This also matches the org-level Construction-phase guardrail in `aidlc/spaces/default/memory/phases/construction.md` § Security ("Never hardcode credentials, API keys, or secrets"). (affirmed 2026-08-16)
- NEVER let a coding agent or implementer fill a value marked **"TBD — freeze gate"** by convenience; such values require explicit student-and-supervisor approval before the dependent work begins. (Vision §1.2; Technical Environment §1.1 "No implementer or coding agent may fill such a value by convenience.") (affirmed 2026-08-16)
- NEVER hide a scientific constant in source code or a notebook; every scientific constant lives in `data.yaml`, `features.yaml`, `experiment.yaml`, or `seeds.yaml`. (TC-03e; Technical Environment §12; human-selected candidate rule, interview Q12-D.) (affirmed 2026-08-16)
- NEVER import `src/external/iri.py` or `src/external/gim.py`, directly or transitively, from any module under `src/features/` or `src/models/`; the only permitted importers are `scripts/04_build_external_products.py` and `src/evaluation/`. (Technical Environment §12 import-boundary rule; §19 TA-07; human-selected candidate rule, interview Q12-A. This is a module-graph constraint distinct from, and additional to, the IRI data-flow rule above.) (affirmed 2026-08-16)
- NEVER change a scientific value after seeing any result, validation or otherwise — the agent may not adjust a frozen value in response to what a run produced. (Technical Environment §18.2, "absolute rule".) (affirmed 2026-08-16)
- NEVER carry Phase 1 fitted model weights into Phase 2, and never let a Phase 1 result motivate a Phase 2 model or evaluation change, unless a separately approved, exploratory-labelled transfer-learning experiment exists. (Technical Environment §7.0B.) (affirmed 2026-08-16)
- NEVER delete, overwrite, or silently re-run an experiment-registry entry; a failed or aborted run stays visible with its status and reason. (NFR-AUD-01; Technical Environment §13.4; gate TA-10.) (affirmed 2026-08-16)
- NEVER let December inform model selection, feature selection, thresholds or hyperparameters: all four use **January-November only**. The trigger is December being **seen**, not the locked test being opened — the required pre-G-05 coverage and regime audit means December is legitimately seen earlier, and that is precisely the channel this rule closes. (Vision §8.3. Added 2026-08-16 per board finding ML-02.) (affirmed 2026-08-16)
- NEVER change a grid range after December is seen; grids are exact and committed to configuration before G-05. NEVER select a second 2022 test period after results are observed. (Vision §8.7, §8.10; Technical Environment §7.1. Added 2026-08-16 per ML-02.) (affirmed 2026-08-16)
- NEVER select a seed on validation or after seeing December; the three-seed element-wise mean is the confirmatory prediction. (Vision §8.6; Technical Environment §13.5. Added 2026-08-16 per ML-05.) (affirmed 2026-08-16)
- NEVER substitute a within-station or naive bootstrap for the vector time-block construction — it produces systematically narrower intervals. (Technical Environment §13.6; TC-19. Added 2026-08-16 per ML-03.) (affirmed 2026-08-16)
- NEVER invent an ablation after results are seen, and NEVER introduce raw longitude as a predictor; longitude enters only through `lst_sin` and `lst_cos`. (Technical Environment §7.2. Added 2026-08-16 per ML-04.) (affirmed 2026-08-16)
- NEVER backfill a driver from future final or definitive archived index values. Final archived values are not equivalent to the contemporaneous operational values available at a 2022 forecast origin, and a series can satisfy its stated lag while still being built from reanalysed indices — invisible in validation, fatal on discovery. Record the release status of every driver, not only its lag. (Technical Environment §10 driver table, "never backfill from future final values"; Vision §6; R-09. Added 2026-08-16 per board finding TEC-04.) (affirmed 2026-08-16)
- NEVER mix Kyoto Dst release grades (real-time, provisional, final) within one series; record the grade for calendar 2022 before use. (`evidence/DECISIONS.md` D-10.1. Added 2026-08-16 per TEC-02.) (affirmed 2026-08-16)
- NEVER claim numerical equivalence between the Phase 1 and Phase 2 targets. Cross-phase results test protocol transfer across a target-domain shift; agreement is not proof that the two estimate the same physical quantity. (Vision §2.2, §6.6; Technical Environment §5. Added 2026-08-16 per TEC-05.) (affirmed 2026-08-16)
- NEVER derive fold or partition membership from an acquisition directory name or a filename. Membership is derived from record timestamps, year and month, and every per-month statistic excludes out-of-month and out-of-year records. (Added 2026-08-16 per board finding ML-07, after the year-blind acquisition predicate filed locked-test-month records into `audit_evidence_2022-01/`; see `evidence/CORRECTION_2026-08-16_acquisition_window.md`. Enforced by `tests/test_acquisition_window.py`.) (affirmed 2026-08-16)
- NEVER copy or materially adapt third-party source whose licence is absent, ambiguous, or incompatible. Reimplement the published method from the paper with a citation instead. This is the standing default while the AGPLv3 distribution question remains open, not a decision deferred to discretion. (Technical Environment §10.1; NFR-LIC-01; gate G-P2. Added 2026-08-16 per findings BENCH-05 and IMPL-07.) (affirmed 2026-08-16)
## Mandated

<!-- Populated by practices-discovery affirmation gate. -->
<!-- Format: ALWAYS [behavior] (affirmed [date]) -->
<!-- Example: ALWAYS use Result<T,E> for fallible operations in service layer (affirmed 2026-05-17) -->

- ALWAYS keep IRI-2016 values, residuals, and any IRI-derived field out of ML training and inference; join IRI only at evaluation time onto the frozen comparison-wide mask. (Vision §7.1 "binding architectural rule"; Technical Environment NFR-IRI-01; enforced by the required `tests/test_iri_denial.py`, which must fail on deliberate injection.) (affirmed 2026-08-16)
- ALWAYS keep CODE final GIM as an evaluation-time-only comparator, never a model input and never presumed independent before the network-overlap audit. (Vision §6.10; Technical Environment §5.2, TC-08 in `aidlc/.../ideation/feasibility/constraint-register.md`.) (affirmed 2026-08-16)
- ALWAYS lag every predictor to its actual availability timestamp before it can be used at a forecast origin: Kp/ap3 ≥ 3 h, Hp60/ap60 ≥ 1 h, F10.7 at previous-day observed value with a **trailing** (never centered) 81-day mean. (Vision §6 feature contract; Technical Environment §6.2; `evidence/DECISIONS.md` D-10.3; TC-10.) (affirmed 2026-08-16)
- ALWAYS treat Dst as diagnostic/hindcast-only — never a confirmatory ML feature. (Vision glossary "Dst"; Technical Environment §6.2; TC-11.) (affirmed 2026-08-16)
- ALWAYS run both required walking-skeleton fixtures — the seven-day single-station plumbing fixture and the one-month all-station scientific fixture — before any full-year job, and never treat the seven-day fixture as scientific evidence. (Technical Environment §9.2, glossary "Walking skeleton"; TC-03f.) (affirmed 2026-08-16)
- ALWAYS fit any train-only transformation (scaling/standardization) on training partitions only, per fold, never on the full dataset. (Vision §6.4 processing strategy items; Technical Environment §6.2 dictionary "Normalization" column; NFR-LEAK-01.) (affirmed 2026-08-16)
- ALWAYS use a single comparison-wide intersection mask, computed once per comparison set, for every model-versus-baseline comparison; never a pairwise or model-specific mask. (Vision glossary "Comparison-wide mask"; Technical Environment NFR-FAIR-01; TC-16.) (affirmed 2026-08-16)
- ALWAYS keep the required pre-G-05 December coverage and regime audit performance-blind, and record it: December 2022 target values may be audited for coverage and regime counts without inspecting any model performance, and this audit is a precondition of G-05, not a violation of the lock. (Vision §8.3; Vision §11 and R-13, which make the December regime-count audit a required G-05 input.) (affirmed 2026-08-16)
- ALWAYS generate and write the locked-test predictions exactly once, after G-05 is signed, and hash them before computing any metric. This is a separate event from the coverage audit above and is the only event the "open it once" rule governs. (Vision §5.3 and the "Locked evaluation" gate table row G-06; Technical Environment §1.4; `constraint-register.md` OC-03, whose "unexamined" wording is superseded by Vision §8.3 for coverage and regime counts.) (affirmed 2026-08-16)
- ALWAYS record and use fixed seeds from `seeds.yaml`, with the three-seed element-wise mean as the confirmatory prediction; record nondeterministic operations where determinism cannot be guaranteed. (Technical Environment NFR-DET-01; TC-21.) (affirmed 2026-08-16)
- ALWAYS co-report the three mandatory difficulty controls — persistence, 24-hour seasonal persistence, fitted station×month×hour climatology (trained on training partitions only) — in the same primary results table as the LSTM-vs-IRI comparison; never relegate them to an appendix. (Vision §2.4 tier 2, "Binding honesty rule"; `constraint-register.md` PC-03, PC-04.) (affirmed 2026-08-16)
- ALWAYS disclose any baseline that beats the LSTM on the locked test in the primary results table and the abstract-level conclusion — a favourable LSTM-vs-IRI result never licenses silence about an unfavourable LSTM-vs-persistence or LSTM-vs-climatology result. (Vision §2.4 "Binding honesty rule"; PC-04.) (affirmed 2026-08-16)
- ALWAYS keep credentials and secrets out of notebooks, source, configs, logs, and registry notes — provision them through platform secret stores or environment configuration excluded from version control. (Technical Environment §10; Technical Environment NFR-SEC-01.) (affirmed 2026-08-16)
- ALWAYS store data gaps as explicit NaN at acquisition time; never interpolate, smooth, or fill at acquisition. (`evidence/DECISIONS.md` D-5, extended to driver series by D-10.2.) (affirmed 2026-08-16)
- ALWAYS keep the full workflow runnable on CPU as a complete execution path; GPU may only be an optional accelerator, never a dependency of any result. (Vision §9.2 "CPU is a complete execution path, not an emergency mode"; Technical Environment §9.2; `constraint-register.md` TC-01.) (affirmed 2026-08-16)
- ALWAYS restrict full-year GNSS-derived VTEC construction, RINEX parsing, DCB handling, STEC calculation, and mapping to Phase 2; Phase 1 code paths must not import or execute these modules. (Vision §2.2 "Phase Boundary"; Technical Environment §7.0 "Phase 1 hard prohibition"; enforced by the required `test_phase_boundary.py`, which must fail if violated; NFR-PHASE-01.) (affirmed 2026-08-16)
- ALWAYS bound every claim to the frozen scope: hourly VTEC forecasting at ARUC 40/44, BSHM 32/35, NICO 35/33 cells, calendar year 2022, tested on December 2022 only — no generalisation beyond these cells, this year, or this test month. (`evidence/DECISIONS.md` D-8; Vision §2.5 "Study Population and Claim Boundary"; `constraint-register.md` TC-17.) (affirmed 2026-08-16)
- ALWAYS treat any scientific question requiring 5-minute resolution at NICO as out of reach on this dataset — it must not be claimed, because NICO holds 53.8% of its native 5-minute slots against 96.4% of its hourly bins. (`evidence/DECISIONS.md` D-7 "Consequence".) (affirmed 2026-08-16)
- ALWAYS treat the December 2022 window as an exact fixed calendar boundary (F1: Jan–Mar/Apr; F2: Jan–Jun/Jul; F3: Jan–Sep/Oct; F4: Jan–Oct/Nov; December locked), each with a 24-hour embargo, and never use random or shuffled cross-validation. (Technical Environment §7.1; Vision §8.2 as referenced there.) (affirmed 2026-08-16)
- ALWAYS surface an integrity failure (hash mismatch, missing manifest, violated invariant) with an explicit exit and a human-readable message naming the file and the violated expectation; never continue silently past a failed hash or integrity check. (Human-selected candidate rule, interview Q12-B; observed practice in `scripts/merge_coverage_year.py`'s hash-verification block.) (affirmed 2026-08-16)
- ALWAYS give every script and module a docstring stating its purpose, its inputs, and its re-run/reproducibility behaviour. (Human-selected candidate rule, interview Q12-C; observed convention in both existing scripts.) (affirmed 2026-08-16)
- ALWAYS record any reused or materially adapted third-party source in the §10.1 External Method and Code-Reuse Register — provenance, immutable commit/tag, licence/SPDX ID, modifications, tests, citation, notice location — before the code is used. (Technical Environment §10.1; NFR-LIC-01; gate G-P2; enforced by `tests/test_reuse_registry.py`; human-selected candidate rule, interview Q12-E.) (affirmed 2026-08-16)
- ALWAYS use the paired loss differential as the confirmatory estimand: the mean within-station difference of squared errors, **benchmark minus model**, combined with **equal-station weighting**, where a positive value favours the model. (Vision §2.3; Technical Environment §1.3. Added 2026-08-16 per board finding ML-03.) (affirmed 2026-08-16)
- ALWAYS compute uncertainty with the vector time-block bootstrap: 24-hour blocks carrying all three stations together, 10,000 replicates, seed 20221201, 95% confidence interval, with the cross-station paired-error correlation reported. The within-station 2,000-replicate variant was rejected at Q-27. (Technical Environment §13.6; `constraint-register.md` TC-19, `binding: hard`. Added 2026-08-16 per ML-03.) (affirmed 2026-08-16)
- ALWAYS predeclare ablations as named runs registered in `experiment.yaml` with a run ID, executed on the frozen January-November folds with identical folds, masks and tuning budget; `ABL-DIFF` inverse-transforms to absolute TECU before any metric, and `ABL-HIST48` runs only after the primary configuration is frozen. (Technical Environment §7.2. Added 2026-08-16 per ML-04.) (affirmed 2026-08-16)
- ALWAYS bound missing external driver values to a carry-forward of at most 3 hours, and exclude the row beyond that. (Vision §6 feature contract; Technical Environment §6.2 dictionary "Carry-forward <= 3 h, then exclude"; `constraint-register.md` TC-09, which the register names the central leakage-prevention rule. Added 2026-08-16 per board finding TEC-03.) (affirmed 2026-08-16)
- ALWAYS stamp `phase_id`, `source_id` and `target_definition_id` on every dataset, prediction, mask and comparison. (Technical Environment §13; Vision §2.2, §6.6. Added 2026-08-16 per TEC-05.) (affirmed 2026-08-16)
- ALWAYS state the documented spatial-representativeness mismatch at the point where any IRI or GIM comparison is reported: Phase 1 compares a grid cell against a station-coordinate evaluation, Phase 2 an IPP cloud against a zenith estimate, and part of any measured difference is a geometry and sampling artefact rather than skill. (Vision §6.6; Technical Environment §5. Added 2026-08-16 per TEC-06.) (affirmed 2026-08-16)
- ALWAYS treat driver series as time-indexed only: one value per epoch, identical across all three cells. A join must never imply a per-cell measurement, and a station performance difference must never be attributed to local forcing the dataset does not contain. (`constraint-register.md` TC-12, `binding: hard`. Added 2026-08-16 per TEC-11.) (affirmed 2026-08-16)
- ALWAYS disclose the `gim_network_overlap_flag` result once the input-network overlap audit runs; disclosure is mandatory and no independence claim may precede the audit. (Technical Environment §5.2. Added 2026-08-16 per TEC-10.) (affirmed 2026-08-16)
- ALWAYS state in the abstract-level interpretation that Phase 2 is a fixed-protocol replication on a new target lineage, **not a second statistically independent blind test**, because it reuses the December timestamps after Phase 1 has already reported them. (Vision §2.2 and §7.0B. Added 2026-08-16 per board finding VAL-05, which found this mandatory disclosure absent from every stage artifact.) (affirmed 2026-08-16)
- ALWAYS run the critical test set and both walking-skeleton fixtures **inside the Kaggle session** before any governed run executed there, capturing the result in that run's evidence record. A Kaggle session carries no git working tree, so a commit hook cannot fire there and a local suite run proves nothing about the environment the governed run actually executes in. (Technical Environment §9.1, §9.2; `constraint-register.md` TC-03g, `binding: hard`; TA-03, TA-26. Added 2026-08-16 per board finding BENCH-01.) (affirmed 2026-08-16)
- ALWAYS record a reused third-party source with the full §10.1 register: `reuse_id`, repository URL, immutable commit or tag, upstream file and line or function, retrieval date, licence and SPDX ID, copied-versus-adapted status, destination file, scientific purpose, modifications, tests, original citation, notice location, reviewer, and approval date. (Technical Environment §10.1; NFR-LIC-01. Added 2026-08-16 per findings BENCH-05 and IMPL-07; supersedes the abbreviated field list previously implied.) (affirmed 2026-08-16)
## Corrections

<!-- Project-specific corrections from human feedback. -->
<!-- Format: NEVER/ALWAYS [behavior] (learned [date]) -->
