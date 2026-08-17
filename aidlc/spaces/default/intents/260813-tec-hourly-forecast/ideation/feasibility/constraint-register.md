# Constraint Register — Hourly VTEC Forecasting (TEC_Project Phase 1 onward)

## Sources

- Upstream: `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/intent-capture/intent-statement.md` (approved 2026-08-13, amended 2026-08-15). Constraints marked **inherited** are fixed there or in the documents it names; this register does **not** restate their authority, narrow them, or move them.
- Authority: `Project Vision and Research Definition` v4.2 (`PreFlight/vision_document(3)(2)(2).md`), normative core §§1–17; `Technical Environment and Research Implementation` v3.2 (`PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md`), subordinate implementation authority.

**Scope of this register.** It covers the constraints that are material to *feasibility* — what the initiative can be built with, on, and under. It is **not** an exhaustive restatement of the normative core. The experiment-freeze parameter set in particular — the F1–F4 folds and their 24-hour embargo, train-only transforms, the frozen hyperparameter grids, the development and final seeds, the bootstrap replicate count and seed and its 48-hour sensitivity, and the GPS-only observable scope — is fixed by the Vision normative core and assembled into a checkable manifest by Requirements Analysis (2.3) and NFR Requirements (3.2). Those stages own it; this register does not duplicate it.
- Sibling: `feasibility-assessment.md` (this stage) — the reasoning behind each constraint.
- `[Q1]`–`[Q12]`: confirmed answers in `feasibility-questions.md`.
- `[survey]` Workspace survey, 2026-08-15. `[web]` External findings recorded in the questions file, 2026-08-15.

Market research was not executed, so no `competitive-analysis`, `market-trends` or `build-vs-buy` artifact is consumed.

## How to Read This Register

**Origin** says where a constraint comes from and therefore who may change it:

- `inherited` — fixed by the intent statement or the normative documents it cites. Not negotiable inside this workflow.
- `decided` — settled by a confirmed answer in this stage. Changeable only by revisiting that answer.
- `environmental` — imposed by a source, tool or platform outside the project's control.

**Binding** says what happens if the constraint is violated: `hard` blocks a gate or invalidates a result; `firm` requires a recorded decision to depart from; `soft` is a preference.

## Technical Constraints

| ID | Constraint | Origin | Binding | Notes |
|---|---|---|---|---|
| TC-01 | The full workflow must run on CPU. GPU is an optional accelerator only, and no result may depend on GPU availability | decided `[Q3]` | hard | Also simplifies the reproducibility package |
| TC-02 | Kaggle is the primary compute environment, with a local machine for development and cross-check. The pinned environment must restore on both | decided `[Q3]` | hard | Parity is verified by V-05 in the assessment |
| TC-03 | Any single unattended run must complete within a 12-hour session on 30 GB RAM | environmental `[web]` | hard | Not binding for training or evaluation; it is the reason a fresh ~17-hour acquisition is avoided `[Q2]` |
| TC-03a | Approximately 10 GB of storage | inherited — Vision §4.4 | hard | The governed storage envelope, covering provider files, manifests, IRI output, model artifacts and the reproducibility package together. Outranks any platform allowance observed at runtime |
| TC-03b | Approximately 30 Kaggle GPU hours per week are available but **not required**; no result may depend on them | inherited — Vision §4.4; `[Q3]` | hard | The user records a 30-hour Kaggle allowance. It is recorded as headroom, never as a dependency — TC-01 keeps the complete path on CPU |
| TC-03c | Two execution platforms only: Kaggle as primary compute, local for development and cross-check | inherited — Vision §4.4 | hard | Matches `[Q3]`; no third platform is authorised |
| TC-03d | Python 3.11 with exact pins, installing successfully on both Kaggle and local, with per-run environment capture | inherited — Technical Environment v3.2, TA-03 | hard | Names the version that TC-02's "pinned environment" must pin to |
| TC-03e | Exactly four governed config files; no scientific constant hidden in source or notebooks | inherited — Technical Environment v3.2 | hard | Constrains the scaffold's shape, so GC-01 cannot produce a structure that fails acceptance |
| TC-03f | Two fixtures — a 7-day plumbing fixture and a 1-month scientific fixture. The seven-day LSTM run is a smoke test and never scientific evidence | inherited — Technical Environment v3.2 | hard | |
| TC-03g | An `environment_and_cpu_preflight_report` demonstrating install-from-pins on both platforms, a completed skeleton run, and measured CPU runtime, RAM and storage, with no GPU-only dependency | inherited — Technical Environment v3.2, EV-14 | hard | This is the evidence that TC-01 and TC-03a are actually met, not merely intended |
| TC-04 | Every dependency, including the `iri2016` Fortran build, must be re-established from the pinned specification on a cold session | environmental `[web]` | hard | Makes environment restore time a measured quantity, not an assumption |
| TC-05 | The acquisition input is the promoted audited calendar-2022 record set (223,586 rows, 365/365 days, three cells, twelve per-month SHA-256 manifests). No fresh full-year re-acquisition is scheduled | decided `[Q2]` | firm | Option A remains available if a reviewer requires single-run provenance; departing from this is a recorded decision, not a silent change |
| TC-06 | Repository structure, pinned environment and test suite are built **before** any acquisition work, inside this initiative | decided `[Q1]` `[Q4]` | hard | Input set enumerated as GC-01 in the assessment |
| TC-07 | IRI-2016 values, residuals, targets, transformations and derived fields never reach training or inference; no IRI or GIM module is imported into feature or model code. IRI is joined at evaluation time only | inherited | hard | Enforced structurally by the module layout required in GC-01 |
| TC-08 | CODE final GIM is a contextual comparator joined at evaluation time only, never a model input | inherited | hard | |
| TC-09 | Drivers are aligned onto the hourly grid without interpolation or smoothing; carry-forward is bounded at ≤ 3 h and never beyond a value's own defined interval | inherited | hard | The central leakage-prevention rule |
| TC-10 | Every predictor is lagged against its availability timestamp: Kp/ap3 ≥ 3 h, Hp60/ap60 ≥ 1 h, F10.7 previous-day observed with a trailing (never centred) 81-day mean | inherited | hard | |
| TC-11 | Dst is diagnostic / hindcast-only and is not a confirmatory forecast feature | inherited | hard | Bounds the impact of any Dst grade problem |
| TC-12 | Driver series are time-indexed only — one value per epoch, identical across all three cells. A join must never imply a per-cell measurement | inherited | hard | |
| TC-13 | +1 h is the confirmatory horizon and the only horizon required. +24 h is optional and off the critical path; no horizon between them is authorised | inherited | hard | |
| TC-14 | No future-observed VTEC or driver values may be used at any horizon | inherited | hard | |
| TC-15 | Leakage freedom must be demonstrated by executable tests, not by assertion | inherited | hard | Makes the test suite a thesis deliverable, not hygiene |
| TC-16 | All model–baseline comparisons use a single comparison-wide mask with identical paired valid timestamps; no pairwise or model-specific masks | inherited | hard | |
| TC-17 | The three cells are the frozen modelling target: ARUC 40/44, BSHM 32/35, NICO 35/33, calendar 2022, December 2022 locked | inherited | hard | |
| TC-18 | The Phase 1 target is a provider-prepared gridded cell value, not a zenith column above an antenna; IRI-2016 and CODE GIM are evaluated at the station coordinate, so every such comparison carries the documented cell-versus-station representativeness mismatch and states it wherever reported | inherited | hard | |
| TC-19 | Uncertainty uses a vector block bootstrap carrying all three stations together in 24-hour blocks, reported at 95%, with cross-station paired-error correlation reported alongside | inherited | hard | |
| TC-20 | No imputation, substitution or reconstruction for the F10.7 outage until the measured gap is recorded and governed | inherited | hard | The audit is an acquisition-freeze input |
| TC-21 | Seeds are recorded and runs are deterministic under the recorded configuration | inherited (reproducibility package) | firm | |

## Organisational and Schedule Constraints

| ID | Constraint | Origin | Binding | Notes |
|---|---|---|---|---|
| OC-01 | One academic semester, with the empirical chapter due at its end | decided `[Q9]` | hard | The binding constraint on the initiative overall |
| OC-02 | Supervisor countersign is required at G-05 (before December opens) and at G-07 (final acceptance); availability is Unknown | inherited | hard | Twice on the critical path; not mitigable by engineering |
| OC-03 | December 2022 stays shut and unexamined until G-05 is signed; at opening, G-06 access rules apply — access authorisation, one write, prediction hash generated **before** any metric is computed | inherited | hard | |
| OC-04 | The G-05 freeze manifest is owned by NFR Requirements (3.2); requirement IDs by Requirements Analysis (2.3). This stage does not assemble or restate it | inherited | hard | Ownership stays where the authority document places it |
| OC-05 | No organisational blockers beyond the recorded countersign dependency | decided `[Q11]` | soft | Recorded so a later blocker is visibly new |
| OC-06 | D-9 and D-10 remain sole-signed; the acquisition route and driver-source corrections are individually reversible on review | inherited, `[survey]` | firm | Drives R-01 in the RAID log |
| OC-07 | Technical Environment v3.2 §1.5 is corrected only through Vision §15.2 change control, outside this workflow | inherited | hard | |
| OC-08 | Thesis chapter prose is authored outside this initiative; this initiative supplies figures, tables, metrics and methods text only | inherited | hard | |
| OC-09 | **Lifted 2026-08-15.** No implementation-capacity ceiling constrains the design. The Vision §4.4 beginner-to-intermediate clause is superseded by an approved §15.2 change request, countersigned by the supervisor | inherited — Vision §4.4 as amended by the §15.2 change record | — | See the note below. The Vision document text itself still carries the pre-amendment wording until the change record is applied to it |

### Note on OC-09 — implementation capacity, change request approved

`[Q10]` answered that no capability ceiling constrains the design, and the author's stated reason is recorded verbatim: *"i choose records no capability ceiling on the design because i wanted to have the best outome possible even if my skill is advanceed"*.

At the time, Vision §4.4 stated "Beginner-to-intermediate Python implementation capacity" inside the normative core, and Vision §1.2 provides that the core governs while §15.2 is the only route by which it changes. A stage answer could not lift it, so the clause was recorded as binding and the author's position as the evidence for a change request rather than a change already made.

**That request is now approved.** The supervisor countersigned the §15.2 change request on 2026-08-15, recorded as reported by the student. The capacity clause no longer constrains this project's design, and OC-09 above reflects the amended position.

Two things this does **not** change. First, the design is still bounded by everything §4.4 does speak to and by the reproducibility requirement — sophistication that a reviewer cannot follow or a clean run cannot reproduce fails the project-completion success layer regardless of who wrote it. Second, the `PreFlight/vision_document(3)(2)(2).md` text still carries the pre-amendment §4.4 wording and no v4.3 change-history row; applying the change record to the Vision itself runs through §15.2 and is not done by this workflow. Until it is applied, a reader of the Vision alone sees the superseded clause. Tracked as governance dependency D-09 in `raid-log.md`.

## Regulatory, Licensing and Data-Handling Constraints

| ID | Constraint | Origin | Binding | Notes |
|---|---|---|---|---|
| RC-01 | No personal, restricted or export-controlled data is involved; all sources are public scientific measurements | decided `[Q8]` | hard | Recorded as an explicit negative finding: no PIA, no data-residency constraint, and no applicability of GDPR, HIPAA, PCI-DSS or SOC 2 |
| RC-02 | CEDAR/Madrigal rules-of-the-road apply, including permanent experiment citation and acknowledgement | decided `[Q7]` | hard | The full rules text must be read and its clauses itemised (V-07) |
| RC-03 | Kyoto WDC Dst carries a non-commercial-use notice and a citation requirement; the notice is reproduced with the data and in the thesis | decided `[Q7]` | hard | Academic thesis use satisfies the restriction |
| RC-04 | GFZ and the Canadian Solar Radio Monitoring Program require citation and acknowledgement | decided `[Q7]` | hard | |
| RC-05 | Every third-party dependency undergoes a licence compatibility review **before** it is pinned | decided `[Q7]` | firm | Reviewing after pinning risks a late forced dependency swap |
| RC-06 | Provenance, licensing, citation and acknowledgement records are kept per source family — the VTEC provider and the index producers are two families, not one | inherited | hard | |
| RC-07 | Retrieved files are hashed and their grade or qualifier status recorded at retrieval time | inherited | hard | Applies to Dst provisional grade and to the F10.7 archive |
| RC-08 | Data access credentials (for example an Earthdata Login, if the chosen GIM route requires one) are provisioned outside the repository and never committed | environmental `[web]` | hard | Standard secret-handling; also an org-level construction guardrail |

## Reporting Constraints

Inherited in full from the intent statement's reporting contract. Recorded here because they constrain what the pipeline must be able to produce, and therefore what it must be built to compute.

| ID | Constraint | Binding |
|---|---|---|
| PC-01 | The primary estimand is the paired loss differential, IRI-2016 squared loss minus LSTM squared loss, positive favouring the LSTM, reported with a 95% confidence interval. Percentage reduction is derived and labelled derived, never confirmatory | hard |
| PC-02 | RMSE is the primary reported error metric; MAE, median absolute error, signed bias, R², Pearson correlation, P90 and P95 absolute error are supporting; MAPE is excluded | hard |
| PC-03 | Three difficulty controls — persistence, 24-hour seasonal persistence, and fitted station × month × hour climatology (training folds only) — are co-reported in the primary results table, never in an appendix | hard |
| PC-04 | If any control beats the LSTM on the locked test, that fact appears in the primary results table and in the abstract-level conclusion | hard |
| PC-05 | December metrics are reported per cell at +1 h; the headline cross-cell result is an equal-station macro-average, with pooled row-weighted results supplementary. Full-month metrics are primary | hard |
| PC-06 | Required breakdowns: quiet/disturbed/storm geomagnetic regime (quiet Kp < 4, disturbed Kp ≥ 4, storm Kp ≥ 5, each three-hour Kp mapped to its hours), observation-quality strata, per-cell metrics, and the time-weighted pooled summary | hard |
| PC-07 | December regime results are descriptive only; a general storm-performance claim requires at least three independent December storm events, and with fewer the results are bounded case evidence | hard |
| PC-08 | A top-1%-absolute-error-removed sensitivity is reported, and the target uncertainty budget is reported adjacent to the primary result | hard |
| PC-09 | Practical relevance is reported descriptively unless the supervisor explicitly approves a threshold; no threshold may be introduced or reinterpreted after December is opened | hard |

## Governance Review

Reviewed under the TEC_Project overlay: `governance/reviews/GOV-2026-08-15-FE-01.md` (FAIL) and `governance/reviews/GOV-2026-08-15-FE-02.md` (CONDITIONAL PASS). OC-09, TC-03a through TC-03g and the scope paragraph at the top of this register were all added or rewritten in response to those findings.

## Assumptions & Open Questions

None. Constraints whose exact content is not yet measured — the Kyoto Dst grade span, the Canadian F10.7 outage extent, the GIM retrieval route, the IRI build and runtime cost, environment parity — are carried as verification obligations in `feasibility-assessment.md` (V-01 to V-08) and as risks in `raid-log.md`, not as assumptions here.
