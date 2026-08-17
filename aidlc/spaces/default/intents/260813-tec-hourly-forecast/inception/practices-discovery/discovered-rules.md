# Discovered Rules — Hourly VTEC Forecasting (TEC_Project Phase 1 onward)

Only hard constraints traceable to the workspace's own normative documents
(`PreFlight/vision_document(3)(2)(2).md` — normative core §§1–17 — and
`PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md`, its
subordinate implementation authority) or to `evidence/DECISIONS.md`'s frozen
decisions are listed here. Per this stage's constraint, a human's disposition can
narrow what a rule requires but cannot relocate a rule the governing normative core
fixes — these rules are written as the authority document states them, not
reinterpreted into a different layer.

## Mandated

- ALWAYS keep IRI-2016 values, residuals, and any IRI-derived field out of ML
  training and inference; join IRI only at evaluation time onto the frozen
  comparison-wide mask. (Vision §7.1 "binding architectural rule"; Technical
  Environment NFR-IRI-01; enforced by the required `tests/test_iri_denial.py`, which
  must fail on deliberate injection.)
- ALWAYS keep CODE final GIM as an evaluation-time-only comparator, never a model
  input and never presumed independent before the network-overlap audit. (Vision
  §6.10; Technical Environment §5.2, TC-08 in
  `aidlc/.../ideation/feasibility/constraint-register.md`.)
- ALWAYS lag every predictor to its actual availability timestamp before it can be
  used at a forecast origin: Kp/ap3 ≥ 3 h, Hp60/ap60 ≥ 1 h, F10.7 at previous-day
  observed value with a **trailing** (never centered) 81-day mean. (Vision §6 feature
  contract; Technical Environment §6.2; `evidence/DECISIONS.md` D-10.3; TC-10.)
- ALWAYS treat Dst as diagnostic/hindcast-only — never a confirmatory ML feature.
  (Vision glossary "Dst"; Technical Environment §6.2; TC-11.)
- ALWAYS run both required walking-skeleton fixtures — the seven-day single-station
  plumbing fixture and the one-month all-station scientific fixture — before any
  full-year job, and never treat the seven-day fixture as scientific evidence.
  (Technical Environment §9.2, glossary "Walking skeleton"; TC-03f.)
- ALWAYS fit any train-only transformation (scaling/standardization) on training
  partitions only, per fold, never on the full dataset. (Vision §6.4 processing
  strategy items; Technical Environment §6.2 dictionary "Normalization" column;
  NFR-LEAK-01.)
- ALWAYS use a single comparison-wide intersection mask, computed once per
  comparison set, for every model-versus-baseline comparison; never a pairwise or
  model-specific mask. (Vision glossary "Comparison-wide mask"; Technical
  Environment NFR-FAIR-01; TC-16.)
- ALWAYS keep the required pre-G-05 December coverage and regime audit
  performance-blind, and record it: December 2022 target values may be audited for
  coverage and regime counts without inspecting any model performance, and this audit
  is a precondition of G-05, not a violation of the lock. (Vision §8.3; Vision §11 and
  R-13, which make the December regime-count audit a required G-05 input.)
- ALWAYS generate and write the locked-test predictions exactly once, after G-05 is
  signed, and hash them before computing any metric. This is a separate event from the
  coverage audit above and is the only event the "open it once" rule governs.
  (Vision §5.3 and the "Locked evaluation" gate table row G-06; Technical Environment
  §1.4; `constraint-register.md` OC-03, whose "unexamined" wording is superseded by
  Vision §8.3 for coverage and regime counts.)
- ALWAYS record and use fixed seeds from `seeds.yaml`, with the three-seed
  element-wise mean as the confirmatory prediction; record nondeterministic
  operations where determinism cannot be guaranteed. (Technical Environment
  NFR-DET-01; TC-21.)
- ALWAYS co-report the three mandatory difficulty controls — persistence, 24-hour
  seasonal persistence, fitted station×month×hour climatology (trained on training
  partitions only) — in the same primary results table as the LSTM-vs-IRI
  comparison; never relegate them to an appendix. (Vision §2.4 tier 2, "Binding
  honesty rule"; `constraint-register.md` PC-03, PC-04.)
- ALWAYS disclose any baseline that beats the LSTM on the locked test in the primary
  results table and the abstract-level conclusion — a favourable LSTM-vs-IRI result
  never licenses silence about an unfavourable LSTM-vs-persistence or
  LSTM-vs-climatology result. (Vision §2.4 "Binding honesty rule"; PC-04.)
- ALWAYS keep credentials and secrets out of notebooks, source, configs, logs, and
  registry notes — provision them through platform secret stores or environment
  configuration excluded from version control. (Technical Environment §10; Technical
  Environment NFR-SEC-01.)
- ALWAYS store data gaps as explicit NaN at acquisition time; never interpolate,
  smooth, or fill at acquisition. (`evidence/DECISIONS.md` D-5, extended to driver
  series by D-10.2.)
- ALWAYS keep the full workflow runnable on CPU as a complete execution path; GPU
  may only be an optional accelerator, never a dependency of any result.
  (Vision §9.2 "CPU is a complete execution path, not an emergency mode"; Technical
  Environment §9.2; `constraint-register.md` TC-01.)
- ALWAYS restrict full-year GNSS-derived VTEC construction, RINEX parsing, DCB
  handling, STEC calculation, and mapping to Phase 2; Phase 1 code paths must not
  import or execute these modules. (Vision §2.2 "Phase Boundary"; Technical
  Environment §7.0 "Phase 1 hard prohibition"; enforced by the required
  `test_phase_boundary.py`, which must fail if violated; NFR-PHASE-01.)
- ALWAYS bound every claim to the frozen scope: hourly VTEC forecasting at ARUC
  40/44, BSHM 32/35, NICO 35/33 cells, calendar year 2022, tested on December 2022
  only — no generalisation beyond these cells, this year, or this test month.
  (`evidence/DECISIONS.md` D-8; Vision §2.5 "Study Population and Claim Boundary";
  `constraint-register.md` TC-17.)
- ALWAYS treat any scientific question requiring 5-minute resolution at NICO as out
  of reach on this dataset — it must not be claimed, because NICO holds 53.8% of its
  native 5-minute slots against 96.4% of its hourly bins. (`evidence/DECISIONS.md`
  D-7 "Consequence".)
- ALWAYS treat the December 2022 window as an exact fixed calendar boundary
  (F1: Jan–Mar/Apr; F2: Jan–Jun/Jul; F3: Jan–Sep/Oct; F4: Jan–Oct/Nov; December
  locked), each with a 24-hour embargo, and never use random or shuffled
  cross-validation. (Technical Environment §7.1; Vision §8.2 as referenced there.)
- ALWAYS surface an integrity failure (hash mismatch, missing manifest,
  violated invariant) with an explicit exit and a human-readable message
  naming the file and the violated expectation; never continue silently past a
  failed hash or integrity check. (Human-selected candidate rule, interview
  Q12-B; observed practice in `scripts/merge_coverage_year.py`'s
  hash-verification block.)
- ALWAYS give every script and module a docstring stating its purpose, its
  inputs, and its re-run/reproducibility behaviour. (Human-selected candidate
  rule, interview Q12-C; observed convention in both existing scripts.)
- ALWAYS record any reused or materially adapted third-party source in the
  §10.1 External Method and Code-Reuse Register — provenance, immutable
  commit/tag, licence/SPDX ID, modifications, tests, citation, notice
  location — before the code is used. (Technical Environment §10.1; NFR-LIC-01;
  gate G-P2; enforced by `tests/test_reuse_registry.py`; human-selected
  candidate rule, interview Q12-E.)

- ALWAYS use the paired loss differential as the confirmatory estimand: the mean
  within-station difference of squared errors, **benchmark minus model**, combined with
  **equal-station weighting**, where a positive value favours the model. (Vision §2.3;
  Technical Environment §1.3. Added 2026-08-16 per board finding ML-03.)
- ALWAYS compute uncertainty with the vector time-block bootstrap: 24-hour blocks
  carrying all three stations together, 10,000 replicates, seed 20221201, 95% confidence
  interval, with the cross-station paired-error correlation reported. The within-station
  2,000-replicate variant was rejected at Q-27. (Technical Environment §13.6;
  `constraint-register.md` TC-19, `binding: hard`. Added 2026-08-16 per ML-03.)
- ALWAYS predeclare ablations as named runs registered in `experiment.yaml` with a run
  ID, executed on the frozen January-November folds with identical folds, masks and
  tuning budget; `ABL-DIFF` inverse-transforms to absolute TECU before any metric, and
  `ABL-HIST48` runs only after the primary configuration is frozen. (Technical
  Environment §7.2. Added 2026-08-16 per ML-04.)
- ALWAYS bound missing external driver values to a carry-forward of at most 3 hours,
  and exclude the row beyond that. (Vision §6 feature contract; Technical Environment
  §6.2 dictionary "Carry-forward <= 3 h, then exclude"; `constraint-register.md` TC-09,
  which the register names the central leakage-prevention rule. Added 2026-08-16 per
  board finding TEC-03.)
- ALWAYS stamp `phase_id`, `source_id` and `target_definition_id` on every dataset,
  prediction, mask and comparison. (Technical Environment §13; Vision §2.2, §6.6. Added
  2026-08-16 per TEC-05.)
- ALWAYS state the documented spatial-representativeness mismatch at the point where any
  IRI or GIM comparison is reported: Phase 1 compares a grid cell against a
  station-coordinate evaluation, Phase 2 an IPP cloud against a zenith estimate, and part
  of any measured difference is a geometry and sampling artefact rather than skill.
  (Vision §6.6; Technical Environment §5. Added 2026-08-16 per TEC-06.)
- ALWAYS treat driver series as time-indexed only: one value per epoch, identical across
  all three cells. A join must never imply a per-cell measurement, and a station
  performance difference must never be attributed to local forcing the dataset does not
  contain. (`constraint-register.md` TC-12, `binding: hard`. Added 2026-08-16 per
  TEC-11.)
- ALWAYS disclose the `gim_network_overlap_flag` result once the input-network overlap
  audit runs; disclosure is mandatory and no independence claim may precede the audit.
  (Technical Environment §5.2. Added 2026-08-16 per TEC-10.)
- ALWAYS state in the abstract-level interpretation that Phase 2 is a fixed-protocol
  replication on a new target lineage, **not a second statistically independent blind
  test**, because it reuses the December timestamps after Phase 1 has already reported
  them. (Vision §2.2 and §7.0B. Added 2026-08-16 per board finding VAL-05, which found
  this mandatory disclosure absent from every stage artifact.)
- ALWAYS run the critical test set and both walking-skeleton fixtures **inside the Kaggle
  session** before any governed run executed there, capturing the result in that run's
  evidence record. A Kaggle session carries no git working tree, so a commit hook cannot
  fire there and a local suite run proves nothing about the environment the governed run
  actually executes in. (Technical Environment §9.1, §9.2; `constraint-register.md`
  TC-03g, `binding: hard`; TA-03, TA-26. Added 2026-08-16 per board finding BENCH-01.)
- ALWAYS record a reused third-party source with the full §10.1 register: `reuse_id`,
  repository URL, immutable commit or tag, upstream file and line or function, retrieval
  date, licence and SPDX ID, copied-versus-adapted status, destination file, scientific
  purpose, modifications, tests, original citation, notice location, reviewer, and
  approval date. (Technical Environment §10.1; NFR-LIC-01. Added 2026-08-16 per findings
  BENCH-05 and IMPL-07; supersedes the abbreviated field list previously implied.)

## Forbidden

- NEVER let an `iri_*` field, an IRI-derived residual, or any IRI-computed value
  reach ML training or inference in the confirmatory experiment. (Vision §7.1;
  Technical Environment NFR-IRI-01.)
- NEVER let Phase 1 code import or execute raw-processing modules
  (`src/gnss/rinex.py`, `src/gnss/calibration.py`) or produce DCB/STEC/mapping/
  satellite/arc fields. (Technical Environment §7.0 "Phase 1 hard prohibition";
  NFR-PHASE-01.)
- NEVER use a centered rolling/trailing window for F10.7 — only the trailing
  81-day mean ending at the safe-lagged day is permitted; a centered mean uses
  future days and is a defect, not a fallback. (Technical Environment §6.2 dictionary
  row `f107_81_trailing`; Technical Environment §10 "Centered means are a defect,
  not a fallback.")
- NEVER use any Random Forest importance score to add, remove, or rank features
  into the production feature set; RF importance may only be saved as a
  non-authoritative diagnostic figure. (Vision §6.4 matched-representation rule,
  Technical Environment §6.4.)
- NEVER treat a favourable LSTM result as license to omit an unfavourable
  baseline comparison from the primary results table or the abstract-level
  conclusion. (Vision §2.4 "Binding honesty rule".)
- NEVER introduce, change, or reinterpret a practical-relevance threshold after
  the December locked test is opened. (Vision §5.4; `constraint-register.md` PC-09.)
- NEVER impute, substitute, or reconstruct a value for the F10.7 outage window
  until the measured gap is recorded and governed. (`constraint-register.md` TC-20.)
- NEVER label the Phase 1 gridded (Madrigal cell) target as receiver-specific
  station-observed VTEC; it is location-sampled gridded VTEC and must be described
  as such, with its distinct `target_definition_id`. (Vision §6.6 "Phase 1
  prepared-target definition — conditional"; Technical Environment glossary.)
- NEVER commit a credential, API key, or secret to a notebook, source file,
  configuration snapshot, log, or registry note. (Technical Environment §10;
  NFR-SEC-01.) This also matches the org-level Construction-phase guardrail in
  `aidlc/spaces/default/memory/phases/construction.md` § Security ("Never hardcode
  credentials, API keys, or secrets").
- NEVER let a coding agent or implementer fill a value marked **"TBD — freeze
  gate"** by convenience; such values require explicit student-and-supervisor
  approval before the dependent work begins. (Vision §1.2; Technical Environment
  §1.1 "No implementer or coding agent may fill such a value by convenience.")
- NEVER hide a scientific constant in source code or a notebook; every
  scientific constant lives in `data.yaml`, `features.yaml`, `experiment.yaml`,
  or `seeds.yaml`. (TC-03e; Technical Environment §12; human-selected candidate
  rule, interview Q12-D.)
- NEVER import `src/external/iri.py` or `src/external/gim.py`, directly or
  transitively, from any module under `src/features/` or `src/models/`; the
  only permitted importers are `scripts/04_build_external_products.py` and
  `src/evaluation/`. (Technical Environment §12 import-boundary rule; §19
  TA-07; human-selected candidate rule, interview Q12-A. This is a
  module-graph constraint distinct from, and additional to, the IRI
  data-flow rule above.)
- NEVER change a scientific value after seeing any result, validation or
  otherwise — the agent may not adjust a frozen value in response to what a
  run produced. (Technical Environment §18.2, "absolute rule".)
- NEVER carry Phase 1 fitted model weights into Phase 2, and never let a
  Phase 1 result motivate a Phase 2 model or evaluation change, unless a
  separately approved, exploratory-labelled transfer-learning experiment
  exists. (Technical Environment §7.0B.)
- NEVER delete, overwrite, or silently re-run an experiment-registry entry; a
  failed or aborted run stays visible with its status and reason. (NFR-AUD-01;
  Technical Environment §13.4; gate TA-10.)

- NEVER let December inform model selection, feature selection, thresholds or
  hyperparameters: all four use **January-November only**. The trigger is December being
  **seen**, not the locked test being opened — the required pre-G-05 coverage and regime
  audit means December is legitimately seen earlier, and that is precisely the channel
  this rule closes. (Vision §8.3. Added 2026-08-16 per board finding ML-02.)
- NEVER change a grid range after December is seen; grids are exact and committed to
  configuration before G-05. NEVER select a second 2022 test period after results are
  observed. (Vision §8.7, §8.10; Technical Environment §7.1. Added 2026-08-16 per
  ML-02.)
- NEVER select a seed on validation or after seeing December; the three-seed element-wise
  mean is the confirmatory prediction. (Vision §8.6; Technical Environment §13.5. Added
  2026-08-16 per ML-05.)
- NEVER substitute a within-station or naive bootstrap for the vector time-block
  construction — it produces systematically narrower intervals. (Technical Environment
  §13.6; TC-19. Added 2026-08-16 per ML-03.)
- NEVER invent an ablation after results are seen, and NEVER introduce raw longitude as a
  predictor; longitude enters only through `lst_sin` and `lst_cos`. (Technical
  Environment §7.2. Added 2026-08-16 per ML-04.)
- NEVER backfill a driver from future final or definitive archived index values. Final
  archived values are not equivalent to the contemporaneous operational values available
  at a 2022 forecast origin, and a series can satisfy its stated lag while still being
  built from reanalysed indices — invisible in validation, fatal on discovery. Record the
  release status of every driver, not only its lag. (Technical Environment §10 driver
  table, "never backfill from future final values"; Vision §6; R-09. Added 2026-08-16 per
  board finding TEC-04.)
- NEVER mix Kyoto Dst release grades (real-time, provisional, final) within one series;
  record the grade for calendar 2022 before use. (`evidence/DECISIONS.md` D-10.1. Added
  2026-08-16 per TEC-02.)
- NEVER claim numerical equivalence between the Phase 1 and Phase 2 targets. Cross-phase
  results test protocol transfer across a target-domain shift; agreement is not proof
  that the two estimate the same physical quantity. (Vision §2.2, §6.6; Technical
  Environment §5. Added 2026-08-16 per TEC-05.)
- NEVER derive fold or partition membership from an acquisition directory name or a
  filename. Membership is derived from record timestamps, year and month, and every
  per-month statistic excludes out-of-month and out-of-year records. (Added 2026-08-16
  per board finding ML-07, after the year-blind acquisition predicate filed
  locked-test-month records into `audit_evidence_2022-01/`; see
  `evidence/CORRECTION_2026-08-16_acquisition_window.md`. Enforced by
  `tests/test_acquisition_window.py`.)
- NEVER copy or materially adapt third-party source whose licence is absent, ambiguous,
  or incompatible. Reimplement the published method from the paper with a citation
  instead. This is the standing default while the AGPLv3 distribution question remains
  open, not a decision deferred to discretion. (Technical Environment §10.1; NFR-LIC-01;
  gate G-P2. Added 2026-08-16 per findings BENCH-05 and IMPL-07.)

## Sources

- `PreFlight/vision_document(3)(2)(2).md` — §1.2 (freeze-gate authority), §2.4
  (comparison hierarchy, binding honesty rule), §2.5 (claim boundary), §5.3–§5.4
  (success layers, practical-relevance reference), §6.2, §6.4, §6.6, §6.10, §7.1
  (IRI-free boundary), §8.2, §9.2 (CPU-complete path), §13.1 (gate table).
- `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — §1.1
  (freeze-gate obligation language), §6.2 (feature dictionary, lag rules, and
  the binding rule requiring `tests/test_iri_denial.py` to fail on violation —
  corrects the earlier miscitation to §7.1, which is the split-configuration
  (F1–F4 fold) table and contains no reference to that test; quality review
  finding N.2), §6.4 matched-representation rule, §7.0 (Phase 1 hard
  prohibition, `test_phase_boundary.py`), §7.0B (Phase 2 weight/decision
  isolation from Phase 1), §7.2 (ablation rules), §9.2 (CPU posture), §10
  (credential handling), §11 (NFR-IRI-01, NFR-LEAK-01, NFR-FAIR-01,
  NFR-REP-01, NFR-DET-01, NFR-PHASE-01, NFR-SEC-01, NFR-LIC-01, NFR-AUD-01),
  §12 (`tests/` tree, import-boundary rule), §13.4 (registry integrity, TA-10),
  §18.2 (forbidden-choice table; the absolute no-post-hoc-change rule), §18.3
  (preflight gate), §19 (TA-07, TA-10).
- `evidence/DECISIONS.md` — D-5 (gap policy), D-7 (hourly resolution, claim
  consequence), D-8 (claim scope), D-10.2/D-10.3 (driver alignment and leakage
  control).
- `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/feasibility/constraint-register.md` —
  TC-01, TC-03f, TC-08, TC-10, TC-11, TC-16, TC-17, TC-20, TC-21, OC-03, PC-03,
  PC-04, PC-09, all marked `binding: hard` and traced to the same normative
  documents (cross-checked, not independently authoritative).
- `aidlc/spaces/default/memory/phases/construction.md` § Security — cross-checked
  as consistent with, not a source of, the credential-handling rule above.

## Assumptions & Open Questions

- None of the above are inferred; each is either a direct quotation/close
  paraphrase of a normative-document clause or a decision recorded in
  `evidence/DECISIONS.md`. Where the constraint register (`constraint-register.md`)
  independently restates a normative-document rule, this file cites the normative
  document as the authority and the register as a cross-check, consistent with the
  project-level rule that a stage answer cannot relocate a requirement the
  governing normative core fixes.
- Corrected 2026-08-16 after the governance board's ML-01 finding: the locked-test
  rule previously read "open it only once, after G-05 is signed", which forbade the
  pre-G-05 December coverage audit that Vision §8.3 REQUIRES and would have made G-05
  unreachable through a compliant `tests/test_locked_test_guard.py`. It is now split
  into the two events Vision §8.3 distinguishes. This restores the authority text
  rather than choosing between competing readings, so it needs no supervisor
  countersignature to stand; it is recorded here as a correction, affirmed by the
  student on 2026-08-16, and `team-practices.md` § Testing Posture already carried the
  correct two-event reading.
- Resolved at the interview: the human selected all five candidate hard rules
  offered at Q12 (import-boundary ban, explicit-exit-on-integrity-failure,
  mandatory docstrings, no-scientific-constant-outside-config, and the
  third-party reuse register), all five now present above under § Mandated /
  § Forbidden. No numeric coverage floor was added (Q5=A) — the named tests
  and the §16/§19 pass/fail rows remain the operative bar; see
  `team-practices.md` § Testing Posture.
- Left open: several Vision/Technical-Environment values are explicitly
  **"TBD — freeze gate"** (e.g., the numerical minimum for prepared-data coverage
  acceptance in Vision §6.1B, the sensor thresholds in Technical Environment §6.7,
  the mapping/shell/cutoff configuration in Vision §6.5). These are not listed
  above as Mandated/Forbidden rules because they are not yet resolved values — they
  are gating obligations owned by the supervisor, tracked separately in the
  initiative brief's "Open Supervisor Gates" table, not invented here.
