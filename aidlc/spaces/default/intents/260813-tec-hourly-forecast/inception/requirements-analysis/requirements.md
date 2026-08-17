# Requirements — Hourly VTEC Forecasting (TEC_Project Phase 1)

Stage 2.3 (requirements-analysis), intent `260813-tec-hourly-forecast`.
Depth: Comprehensive. Scope: `research-pipeline-governed`.

## Sources

- [desc] Initial description, carried verbatim in
  `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/intent-capture/intent-statement.md`
  § Sources.
- [scope] Workflow-selected scope: `research-pipeline-governed`. This scope
  ships no `scope-document` artifact — `scope-definition` (1.4) produced its
  boundary inside the intent statement's `## Initial Scope Signal` section
  instead, which is where the product boundary, deliverable set and frozen
  modelling target are read from below. The `consumes` entry for
  `scope-document` is therefore satisfied by that section, not by a separate
  file; this is recorded rather than left as a silent gap.
- [intent] `ideation/intent-capture/intent-statement.md` — problem statement,
  driver contract, benchmark role, success layers, primary estimand, metric
  set, mandatory difficulty controls, model set, forecast horizon, reporting
  contract, sealing condition, scoped verification obligations, governance
  dependencies.
- [practices] `inception/practices-discovery/team-practices.md` and its
  companion `evidence.md` — affirmed way of working, testing posture,
  deployment posture, code style, and the observed-workspace evidence facts
  those practices rest on.
- [rules] `inception/practices-discovery/discovered-rules.md` and
  `aidlc/spaces/default/memory/project.md` — the 58 affirmed hard rules.
- [Vision] `PreFlight/vision_document(3)(2)(2).md` v4.2.
- [TE] `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` v3.2.
- [D-n] `evidence/DECISIONS.md`.
- [Q1]–[Q10] Confirmed answers in `requirements-analysis-questions.md`.

## How to read this document

`requirements.md` is a **decomposition layer**, not a restatement and not an
index. [Q1] Each requirement carries:

1. a **stable ID** that later stages cite unchanged;
2. a **pass/fail criterion** — a condition an artifact, a test, or a named
   report either meets or does not;
3. an **inline source tag** naming the authority it derives from [Q7];
4. a **test link** to the §16 walking-skeleton row (`WS-nn`) or §19 technical
   approval row (`TA-nn`) that tests it.

`user-stories` (2.4) is SKIP in this scope, so WS-09–WS-20 and TA-01–TA-32 are
the **only** acceptance vocabulary Construction inherits. [practices] A
requirement with no WS or TA row is marked **`UNTESTED`** and listed in
§ Requirements with no testing row. No test row is invented to fill a gap. [Q1]

Functional decomposition follows the Technical Environment §7.0 Phase 1 stage
table P1-00 through P1-06, so requirements map onto the pipeline's own stages
rather than onto the `src/` package layout or an abstract dimension list. [Q2]
[TE §7.0]

**Phase-boundary discipline.** The intent statement's `## Success Metrics`
phase-boundary note binds this stage: the metric set, difficulty controls,
model set, horizon, reporting contract and sealing condition are **inherited,
not re-derived**. This stage's job is to give each a stable ID and a checkable
criterion. [intent] Nothing below re-opens a value the authority documents fix.

## Constraints inherited, not restated

Binding constraints live where they were affirmed. This document cites them and
does not copy them, so a later correction has exactly one place to land. [Q8]

| Constraint body | Where it lives | What it governs here |
|---|---|---|
| 58 affirmed hard rules (`ALWAYS`/`NEVER`) | `aidlc/spaces/default/memory/project.md` §§ Forbidden, Mandated; mirrored in `inception/practices-discovery/discovered-rules.md` | Every requirement below; a requirement never weakens one |
| Affirmed team practices — way of working, testing posture, deployment, code style | `inception/practices-discovery/team-practices.md` | REQ-ENG-*, and the acceptance model in § Success and acceptance |
| Observed-workspace evidence facts (13 facts, incl. the `raw_isprint_cache/` provenance finding) | `inception/practices-discovery/evidence.md` | FR-P1-01-*, REQ-DEF-* |
| Constraint register TC/OC/PC rows | `ideation/feasibility/constraint-register.md` | Cited inline as `[TC-nn]` etc. |
| Acquisition-window correction (year-blind predicate) | `evidence/CORRECTION_2026-08-16_acquisition_window.md` | FR-P1-01-4, FR-P1-04-2 |
| Governance board reports GOV-2026-08-13-IC-01/-02/-03, GOV-2026-08-15-FE-01 | `governance/reviews/` (GOV-25: not all are persisted yet) | § Known defects in the authority documents |
| D-1 … D-11 scientific and governance decisions | `evidence/DECISIONS.md` | Cited inline as `[D-n]` |
| Supervisor gate table (G-05, G-06, G-07, G-P1A, G-P2, G-P3A/C) | Vision §13.1 | § Open supervisor gates |

## Intent analysis

**What the student is trying to achieve.** Two joined goals, in stated
priority order. [intent]

1. **Primary — a defensible hourly VTEC forecast** for the three frozen cells
   (ARUC 40/44, BSHM 32/35, NICO 35/33), calendar 2022, +1 h confirmatory
   horizon, evaluated once on locked December 2022. The claim that must
   survive examination is the paired loss differential (IRI-2016 squared loss
   minus LSTM squared loss, positive favours the model) with a 95% confidence
   interval, co-reported with three mandatory difficulty controls.
   [Vision §2.3] [TE §1.3]
2. **Supporting — a governed, reproducible pipeline** that demonstrably
   prevented leakage, recorded its own provenance, and reproduces on CPU from
   a clean environment.

**The goal behind the goal.** A forecast number is worth only the provenance
and leakage discipline behind it. [intent] Every requirement below exists to
make one of two statements checkable: *this predictor was genuinely available
at its forecast origin*, and *this artifact came from these exact bytes under
this exact configuration*.

**What is being requested now.** The immediate work is not model research. It
is: build the repository scaffold, pins and test suite (TC-06); re-acquire and
provenance the Phase 1 source; align the drivers onto the hourly grid without
interpolation; lag every predictor against its availability timestamp; then
build features, splits, masks, models and the evaluation. [desc] [TE §7.0]

**Type and complexity.** New build on a partially populated workspace
(two scripts, one notebook, twelve months of derived audit evidence, no
`tests/`, no `src/`, no `configs/`, no `pyproject.toml`). System-wide scope,
complex domain, heavy external governance. Depth: Comprehensive.

---

## Functional requirements

Decomposed by the Technical Environment §7.0 Phase 1 stage table. [Q2] [TE §7.0]

### REQ-ENG — Repository scaffold, pins and tests (precondition to P1-01)

TC-06 places the scaffold, pinned environment and test suite **before any
further acquisition work, inside this initiative**. [TC-06] These are therefore
requirements of this initiative, not of a later one.

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| REQ-ENG-1 | The repository skeleton exists: `pyproject.toml` at root, four configs under `configs/` (`data.yaml`, `features.yaml`, `experiment.yaml`, `seeds.yaml`), six `src/` packages (`data`, `gnss`, `external`, `features`, `models`, `evaluation`), nine phase-aware stage scripts, five notebooks, `tests/`, `artifacts/` | Repository tree matches the §12 layout; the tree and its commit are recorded | [TE §12] | TA-01 |
| REQ-ENG-2 | All four configuration files exist and every unresolved field is visibly marked `TBD — freeze gate` | Config inventory plus schema validation returns no unmarked hole | [TE §12] [Vision §1.2] | TA-02 |
| REQ-ENG-3 | Python 3.11 with exact pins installs on **both** Kaggle and local; no third platform is used | Lock file, install log and environment hash from both platforms | [TE §8.1, §9.1] [TC-03c, TC-03d] | TA-03, TA-26 |
| REQ-ENG-4 | The 17 mandated test modules exist under `tests/`, plus the two fixture directories `tests/fixtures/plumbing_7day/` and `tests/fixtures/scientific_1month/` | Each named module is present and collectible; fixture assertion data lives in `fixture_manifest.yaml`, never hardcoded in test bodies | [TE §12, §15.2] [practices] | TA-09 |
| REQ-ENG-5 | Every hard rule in `discovered-rules.md` has a **negative-path** test proving the violation is caught — not only a happy-path test | For each such rule, a test exists that fails when the violation is injected | [practices] [Vision §7.1] | WS-10, TA-07, TA-08, TA-12, TA-27 |
| REQ-ENG-6 | Git is initialized before any further acquisition work, on `main`, with a credential/secret deny-list in `.gitignore` (`.env`, `*.key`, `kaggle.json`, `.netrc`, `credentials*`) present **before the first commit** | `git log` exists; a secret scan over the tree and history returns clean | [practices] [TE §10] [NFR-SEC-01] | TA-22 |
| REQ-ENG-7 | Each freeze gate (G-05, G-06, each phase transition) is tagged, and any commit changing a scientific constant or a governed config cites its D-number | Tag list covers the signed gates; commit-message audit shows a D-number on every governed change | [practices] | `UNTESTED` |
| REQ-ENG-8 | The two existing scripts and the coverage notebook migrate onto the §12 structure: `--config configs/` (and `--phase 1|2` where applicable), a numbered `NN_verb_noun.py` position, the triplicated SHA-256 helper consolidated into `src/data/release.py`, the notebook's inline station coordinates and coordinate-to-cell rule moved into `configs/data.yaml` and `src/data/registry.py` **only after** those current values are frozen under a D-number | Migration complete; `grep` shows no scientific constant remaining in source or notebook; the freeze D-number exists and precedes the move | [practices] [TE §12, §14] [TC-03e] [Q11] | TA-16 |
| REQ-ENG-9 | `audit_ec1_drivers.py`'s exit-code gap is closed: a completeness shortfall is recorded as a machine-readable field in the output manifest, an integrity violation terminates the run naming the file and the violated expectation | Injecting a missing month yields a non-silent, machine-readable record; injecting a hash mismatch yields a non-zero exit with a naming message | [practices] `scripts/audit_ec1_drivers.py:184` | `UNTESTED` |

### FR-P1-00 — Close the rejected-source audit

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-00-1 | The ICTP source-failure evidence is immutable and machine-readable: `source_status=REJECTED_COVERAGE`, coverage recorded as ARUC 27/365, BSHM 35/365, NICO 0/365, decision stored as D-143 | The evidence set exists, hashes verify, and the status field is machine-readable | [TE §7.0 P1-00] [D-143] | TA-31 |
| FR-P1-00-2 | No ICTP artifact enters target construction or training | An import/data-lineage check shows no ICTP artifact reachable from the target or feature path | [TE §7.0 P1-00] [Vision R-23] | TA-25 |

### FR-P1-01 — Acquire the Phase 1 prepared VTEC product

This stage carries the deferred `raw_isprint_cache/` re-acquisition. FU-1=B
sequenced it **after** this requirements pass; per [Q4] it is specified now so
the deferred work has a specification when it runs, together with the
acceptance evidence that closes DATA-03 and DATA-04.

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-01-1 | Acquisition retrieves the supervisor-approved Madrigal MAPGPS `gps` binned-VTEC product under D-144, with the exact experiment and kindat/parameters frozen, and applies **no** scientific transformation at retrieval | The frozen experiment/kindat/parameter set is recorded; a diff of retrieved against stored values shows no transformation | [TE §7.0 P1-01] [D-144] | TA-32 |
| FR-P1-01-2 | Every retrieved file records provider, permanent citation, **full provider filename including its version suffix** (e.g. `g.002` vs `g.003`), retrieval date and SHA-256; a mismatch against a previously recorded suffix is surfaced, never silently accepted | `request_manifest.json` carries all five fields per provider file; an injected suffix mismatch raises | [TE §13.3] [practices; DATA-07] | TA-15 |
| FR-P1-01-3 | The `madrigalWeb` client version is pinned and recorded — never `"unknown"` — and the exact web-service interface is recorded alongside it. **This is the acceptance evidence that closes DATA-03.** | No `request_manifest.json` written after this requirement takes effect contains `madrigalWeb_version: "unknown"`; the pin appears in the lock file | [TE §8.1, §10, §13.3] [evidence fact 5] [NFR-REP-01] | TA-03, TA-15 |
| FR-P1-01-4 | Native provider byte streams are retained, and `sha256_manifest.json` hashes **one entry per provider file**, not only the four derived artifacts. **This is the acceptance evidence that closes DATA-04.** | `find` locates provider files for every acquired month; each month's manifest hash count equals its provider-file count plus its derived-artifact count; the twelve pre-TC-06 months are re-verified under the new test suite rather than re-acquired from scratch | [TE §10, §13.3] [evidence fact 6] | TA-04, TA-15 |
| FR-P1-01-5 | Acquisition membership is derived from **record timestamps**, never from an acquisition directory name or filename; every per-month statistic excludes out-of-month and out-of-year records | `tests/test_acquisition_window.py` passes, including the case that produced the original defect (December records filed under `audit_evidence_2022-01/`) | [project.md § Forbidden] [`evidence/CORRECTION_2026-08-16_acquisition_window.md`] | `UNTESTED` — no WS/TA row covers the acquisition-window predicate; see § Requirements with no testing row |
| FR-P1-01-6 | Driver acquisition follows the frozen contract: Kp/ap3 and Hp60/ap60 from GFZ, hourly Dst from Kyoto WDC at a **single recorded release grade** for all of 2022, observed (not 1-AU-adjusted) F10.7 from Canada's Solar Radio Monitoring Program. SSN is absent | Each series carries its source, release grade and retrieval record; a grep confirms SSN is absent from the codebase | [intent driver contract] [D-10.1, D-10.3] [Vision §6] | TA-08 |
| FR-P1-01-7 | The Canadian F10.7 archive is audited from 2022-03-18 onward for the documented month-long outage; exact missing dates, qualifiers and any reconstructed values are reported. **No imputation, substitution or reconstruction occurs until the measured gap is recorded and governed.** | The audit report exists with exact dates; no filled value exists in the series before the governing decision | [intent obligation 2] [TC-20] | `UNTESTED` |
| FR-P1-01-8 | No driver is backfilled from future final or definitive archived index values; the **release status** of every driver is recorded, not only its lag | Each driver's manifest carries a release-status field; a reanalysed-value check passes | [TE §10] [project.md § Forbidden; TEC-04] | `UNTESTED` |
| FR-P1-01-9 | Data gaps are stored as explicit `NaN` at acquisition time; no interpolation, smoothing or fill occurs at acquisition | An injected gap survives acquisition as `NaN` | [D-5, D-10.2] | `UNTESTED` |
| FR-P1-01-10 | Credentials and secrets are supplied through platform secret stores or environment configuration excluded from version control, and appear in no notebook, source file, configuration snapshot, log or registry note | Secret scan over tree, history and artifacts returns clean | [TE §10] [NFR-SEC-01] | TA-22 |

### FR-P1-02 — Inventory, registry and the G-P1A coverage gate

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-02-1 | Station coordinates and the coordinate-to-cell rule are validated against the **official IGS site logs** before being treated as final, and live in `configs/data.yaml` / `src/data/registry.py` rather than in a notebook literal | Registry values match the site logs; header cross-check shows no unresolved conflict | [TE §7.0 P1-02] [§18.2 forbidden-choice items] | WS-01, TA-04 |
| FR-P1-02-2 | Schema validation covers parameter names, units, fill values, UTC cadence and duplicates for the prepared product | The prepared-data schema report exists and passes | [TE §7.0 P1-02] | TA-04 |
| FR-P1-02-3 | File, cell, day, month and common-timestamp coverage is audited **including December**, without inspecting any model performance | The coverage report covers all twelve months; no performance figure appears in it or in its execution log | [TE §7.0 P1-02] [Vision §8.3] | WS-18, TA-25 |
| FR-P1-02-4 | **G-P1A acceptance is decided against Vision §6.1B's numerical coverage minimum.** That value is currently `TBD — supervisor freeze gate` and is **not** supplied by this stage. Until it is recorded under its own D-number in `evidence/DECISIONS.md`, acceptance operates on D-2's existing interim rule: ≥95% of calendar days per month, 100% of December | The G-P1A decision record cites either the frozen §6.1B value **or**, explicitly, the D-2 interim rule and the fact that §6.1B is unfrozen — never an unattributed number | [Vision §6.1B] [D-2] [Q3] | TA-25 |
| FR-P1-02-5 | Silent imputation, source mixing, retrospective split redesign after model performance is viewed, and labelling a map value as station-observed VTEC are each prohibited at this gate | Each prohibited action has an injection test that fails the pipeline | [Vision §6.1B] | TA-25, TA-29 |

### FR-P1-03 — Standardize the prepared hourly target

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-03-1 | Provider values are preserved; only documented QC, UTC normalization, cell selection and the frozen hourly aggregation are applied | A value-level diff against the provider bytes shows only the documented transformations | [TE §7.0 P1-03] | TA-04 |
| FR-P1-03-2 | Phase 1 never estimates DCB or STEC, never maps `los` observations, and never silently interpolates a missing cell; Phase 1 code cannot import or execute `src/gnss/rinex.py` or `src/gnss/calibration.py` | `tests/test_phase_boundary.py` fails when the import is introduced | [TE §7.0 hard prohibition] [NFR-PHASE-01] | TA-27 |
| FR-P1-03-3 | Every dataset, prediction, mask and comparison is stamped with `phase_id`, `source_id` and `target_definition_id` | Schema test asserts all three on every such artifact | [TE §13] [NFR-TDEF-01] | TA-15 |
| FR-P1-03-4 | The Phase 1 target is labelled **location-sampled gridded VTEC**, never receiver-specific station-observed VTEC, everywhere it is described | A claims-checklist review over every artifact and figure caption finds no mislabelling | [Vision §6.6] [NFR-TDEF-01] | TA-15 |

### FR-P1-04 — External products, features, splits, masks

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-04-1 | No `iri_*` field, IRI-derived residual, or IRI-computed value reaches ML training or inference; IRI and GIM join **only at evaluation time** on the frozen comparison-wide mask; no module under `src/features/` or `src/models/` imports `src/external/iri.py` or `src/external/gim.py`, directly or transitively | `tests/test_iri_denial.py` **fails** on deliberate `iri_*` injection, and the import-boundary check passes | [Vision §7.1] [NFR-IRI-01] [TE §12] | WS-10, TA-07 |
| FR-P1-04-2 | Every predictor is lagged to its actual availability timestamp: Kp/ap3 ≥ 3 h, Hp60/ap60 ≥ 1 h, F10.7 at the previous-day observed value with a **trailing** (never centered) 81-day mean; Dst is diagnostic/hindcast-only; SSN is absent | The availability matrix asserts actual lag ≥ declared safe lag for every primary feature; a centered-mean injection fails | [Vision §6] [TE §6.2] [D-10.3] [TC-10, TC-11] | WS-11, TA-08 |
| FR-P1-04-3 | Missing external driver values carry forward at most 3 hours; beyond that the row is excluded | An injected 4-hour gap excludes the row | [TE §6.2] [TC-09] | WS-11 |
| FR-P1-04-4 | Driver series are time-indexed only — one value per epoch, identical across all three cells; a join never implies a per-cell measurement | Schema test asserts a single value per epoch across cells | [TC-12] | `UNTESTED` |
| FR-P1-04-5 | Folds are exact fixed calendar boundaries (F1: Jan–Mar/Apr; F2: Jan–Jun/Jul; F3: Jan–Sep/Oct; F4: Jan–Oct/Nov; December locked), each with a 24-hour embargo; no random or shuffled cross-validation; the first 24 h are excluded and counted | No window crosses a boundary; the split manifest records the excluded count | [TE §7.1] [Vision §8.2] | WS-12, TA-11 |
| FR-P1-04-6 | Any scaling or standardization is fitted on training partitions only, per fold, never on the full dataset | A full-dataset fit injected into the pipeline is caught | [Vision §6.4] [NFR-LEAK-01] | TA-11 |
| FR-P1-04-7 | A **single comparison-wide intersection mask** is computed once per comparison set and used for every model-versus-baseline comparison; masks carry stable IDs and reported row counts; no pairwise or model-specific mask is produced | Mask manifest shows one mask per comparison set with a stable ID; a pairwise mask attempt fails | [Vision glossary] [NFR-FAIR-01] [TC-16] | WS-16, TA-11 |
| FR-P1-04-8 | The flattened matrix and the sequence tensor for a given feature-set ID contain the same underlying window values | Matched-window assertion passes | [TE §16 WS-13] | WS-13, TA-11 |
| FR-P1-04-9 | The IRI benchmark and GIM comparator sample alignment passes; the IRI ceiling and drivers are recorded; the **`gim_network_overlap_flag` audit is present and its result disclosed**, and no independence claim precedes the audit | Tolerance report, config snapshot and overlap audit all exist; the flag value appears wherever GIM is compared | [TE §5.2] [Vision §6.10] [TC-08] | WS-09 |
| FR-P1-04-10 | Raw longitude never enters as a predictor; longitude enters only through `lst_sin` and `lst_cos` | Feature manifest contains no raw-longitude column | [TE §7.2] | `UNTESTED` |
| FR-P1-04-11 | Every dataset release records version, source manifest, SHA-256 hashes, schema, row counts, exclusions and fold/mask identifiers, and is write-protected or stored under a new version rather than overwritten | `tests/test_release_hashes.py` mutation-protection test passes | [TE §13.3] | TA-15 |

### FR-P1-05 — Models, prediction, evaluation

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-05-1 | The model set is persistence (M-01), 24-hour seasonal persistence (M-02), fitted station×month×hour climatology trained on training folds only (M-03), ridge (M-04), Random Forest (M-05) and the compact LSTM (M-06); **residual and GRU modules are absent from the codebase**; TensorFlow/Keras is the only NN stack | All required model IDs are present in modules and configs; grep evidence shows residual and GRU absent, and PyTorch absent | [intent model set] [TE §8.3] | WS-14, TA-12, TA-26 |
| FR-P1-05-2 | M-06 trains and restores its lowest-validation-RMSE checkpoint; the **three-seed element-wise mean** from `seeds.yaml` is the confirmatory prediction; no seed is selected on validation or after seeing December | Checkpoint-restore and seed tests pass; the seeds are fixed in config, not chosen at runtime | [NFR-DET-01] [TC-21] [Vision §8.6] | WS-15, TA-13 |
| FR-P1-05-3 | No Random Forest importance score adds, removes or ranks a feature into the production feature set; RF importance is saved only as a non-authoritative diagnostic figure | The feature manifest's provenance shows no importance-derived selection | [Vision §6.4] [TE §6.4] | `UNTESTED` |
| FR-P1-05-4 | Tuning uses **January–November only**; model selection, feature selection, thresholds and hyperparameters are never informed by December. The trigger is December being **seen**, not the locked test being opened | The tuning record shows no December-derived input, including after the required pre-G-05 coverage audit | [Vision §8.3] [project.md § Forbidden; ML-02] | WS-18 |
| FR-P1-05-5 | Hyperparameter grids are exact and committed to configuration **before G-05**, and no grid range changes after December is seen; no second 2022 test period is selected after results are observed | `experiment.yaml` grids are frozen at the G-05 commit; a post-G-05 grid diff is empty | [Vision §8.7, §8.10] [TE §7.1] | `UNTESTED` |
| FR-P1-05-6 | Ablations are **predeclared** as named runs registered in `experiment.yaml` with a run ID, executed on the frozen January–November folds with identical folds, masks and tuning budget; `ABL-DIFF` inverse-transforms to absolute TECU before any metric; `ABL-HIST48` runs only after the primary configuration is frozen | Each ablation has a pre-freeze registry row; no ablation is registered after results are seen | [TE §7.2] | `UNTESTED` |
| FR-P1-05-7 | The confirmatory estimand is the **paired loss differential — mean within-station difference of squared errors, benchmark minus model — with equal-station weighting**, positive favouring the model, reported at 95% | The evaluation module computes exactly this quantity; percentage reduction is computed only as a labelled derived summary | [Vision §2.3] [TE §1.3] | `UNTESTED` |
| FR-P1-05-8 | Uncertainty uses the **vector time-block bootstrap**: 24-hour blocks carrying all three stations together, 10,000 replicates, seed 20221201, 95% CI, with the cross-station paired-error correlation reported. A within-station or naive bootstrap is not substituted | The bootstrap reproduces exactly from seed 20221201 on synthetic correlated data; a 48-hour sensitivity is produced | [TE §13.6] [TC-19] | WS-17, TA-14 |
| FR-P1-05-9 | The three mandatory difficulty controls (M-01, M-02, M-03) are co-reported **in the primary results table**, never in an appendix; any baseline that beats the LSTM appears in that table **and** in the abstract-level conclusion | The primary results table contains all three controls plus the IRI comparison; a review of the abstract confirms disclosure | [Vision §2.4 binding honesty rule] [PC-03, PC-04] | TA-20 |
| FR-P1-05-10 | The target uncertainty budget is produced and reported **adjacent to** the primary result; a top-1%-absolute-error-removed sensitivity is reported | `target_uncertainty_budget.json` exists and appears beside the primary result | [NFR-DQ-01] [intent reporting] | TA-19 |
| FR-P1-05-11 | Required reporting breakdowns are produced: per-cell metrics at +1 h, equal-station macro-average as the headline, pooled row-weighted as supplementary, quiet/disturbed/storm regime split, observation-quality strata, daily error and four local-solar-time diagnostic bins; December regime results are **descriptive only** unless at least three independent storm events occur | Each named breakdown exists in the results artifact; the storm-claim guard is enforced | [intent reporting] [Vision §11] | WS-19 |
| FR-P1-05-12 | The **locked-test guard** blocks December performance execution before G-05 is signed, records every access, and sets `locked_test_accessed = true` in the experiment registry; predictions are generated and written **once**, and hashed **before** any metric is computed | `tests/test_locked_test_guard.py` blocks a pre-G-05 December run; the access log and prediction hash both precede the metrics | [Vision §5.3, §8.3] [OC-03] | WS-18, TA-18 |
| FR-P1-05-13 | The experiment registry is operational, append-safe and atomic; failed and aborted runs remain visible with status and reason; no entry is deleted, overwritten or silently re-run | Registry tests pass, including a failed-run sample that remains visible | [NFR-AUD-01] [TE §13.4] | TA-10 |
| FR-P1-05-14 | Any test-driven change made to the pipeline **after** locked-test access is labelled exploratory | Every post-access change carries the exploratory label in the registry | [Vision §8.3] | `UNTESTED` |
| FR-P1-05-15 | No practical-relevance threshold is introduced, changed or reinterpreted after December is opened | The threshold record's timestamp precedes G-06 | [Vision §5.4] [PC-09] | `UNTESTED` |

### FR-P1-06 — Phase transition freeze

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-06-1 | `phase_transition_manifest` hashes and freezes the model source, environment, architecture, feature manifest, target contract, splits/masks, grids, hyperparameters and seeds; Phase 2 refuses to train if any protected hash differs | `tests/test_phase_boundary.py` **and** a transition-manifest hash-diff test both pass; G-P3C confirms protected hashes unchanged | [TE §2.2, §7.0B] [NFR-PHASE-01] | TA-27 |
| FR-P1-06-2 | Phase 1 fitted weights are never carried into Phase 2, and no Phase 1 result motivates a Phase 2 model or evaluation change, unless a separately approved, exploratory-labelled transfer-learning experiment exists | Phase 2 initializes from new weights; the change log shows no Phase 1-motivated change | [TE §7.0B] | TA-27 |
| FR-P1-06-3 | Every reused or materially adapted third-party source is recorded in the §10.1 register with the **full field set** — `reuse_id`, repository URL, immutable commit/tag, upstream file and line/function, retrieval date, licence and SPDX ID, copied-versus-adapted status, destination file, scientific purpose, modifications, tests, original citation, notice location, reviewer, approval date — **before** the code is used and before G-P2 | `tests/test_reuse_registry.py` passes; no adapter exists without a complete register row | [TE §10.1] [NFR-LIC-01] | TA-28 |
| FR-P1-06-4 | Third-party source whose licence is absent, ambiguous or incompatible is **not** copied or materially adapted; the published method is reimplemented from the paper with a citation instead. This is the standing default while the AGPLv3 distribution question remains open | The register contains no row with an unresolved licence status | [TE §10.1] [BENCH-05, IMPL-07] | TA-28 |

### FR-WS — Walking-skeleton fixtures and clean run

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-WS-1 | Both fixtures run, in order, **before any full-year job**: the seven-day single-station plumbing fixture (frozen by D-11 as 2022-11-01 to 2022-11-07, all three cells) and the one-month all-station scientific fixture (window still open under Q-31) | Fixture run log shows plumbing before scientific before any full-year job | [TE §9.2] [TC-03f] [D-11] | WS-20, TA-09 |
| FR-WS-2 | The seven-day fixture is **never** treated as scientific evidence | No result artifact cites the plumbing fixture as evidence | [TC-03f] | `UNTESTED` |
| FR-WS-3 | No record whose **observation date** falls in December 2022 enters either fixture — asserted on record dates, never on the folder a file was filed under | `tests/test_acquisition_window.py` passes | [practices] [ML-07] | `UNTESTED` |
| FR-WS-4 | Phase 1's acceptance set is **WS-09 through WS-20**; WS-01–WS-08 are explicitly deferred to G-P3A because §7.0's Phase 1 hard prohibition bars Phase 1 from producing the raw-processing evidence those rows require. (Supervisor-countersigned 2026-08-16.) | All twelve of WS-09–WS-20 PASS with evidence links; no Phase 1 artifact claims a WS-01–WS-08 result | [TE §16, §16.1] [practices Q6=A] | WS-09…WS-20 |
| FR-WS-5 | A clean **CPU** environment reproduces both fixtures within declared tolerances, following the §13.2 ordered clean-run command sequence; GPU is an optional accelerator only and no result depends on it | `tests/test_clean_run.py` passes on a fresh CPU environment; the clean-run log and artifact comparison report exist | [TE §13.2] [NFR-REP-01] [TC-01] | WS-20, TA-17 |
| FR-WS-6 | The critical test set **and both fixtures** run **inside the Kaggle session** before any governed run executed there; the result is captured in that run's evidence record | The Kaggle run's evidence record contains an in-session test and fixture result, not a local one | [TE §9.1, §9.2] [TC-03g] [BENCH-01] | TA-03, TA-26 |
| FR-WS-7 | The §18.3 preflight gate passes before an affected component is implemented: **zero unresolved P0 fields and no failing critical test**, an automated assertion confirms no required field in the four configs is `TBD`, and supervisor sign-off covers the scientific hierarchy, IRI role, horizons, estimand, seeds and locked-test protocol | `aws_ai_dlc_preflight_report` shows all three preconditions met. An agent **stops and reports** rather than choosing a default when a P0 decision is unresolved | [TE §18.3] | TA-23 |

---

## Non-functional requirements

The Technical Environment §11 NFRs are **adopted by reference with their
existing IDs**. They are not renumbered and not restated; each gains a
pass/fail criterion and a test mapping here. [Q5]

**Correction to the question text.** `requirements-analysis-questions.md` Q5
enumerated nine §11 NFRs. §11 carries **twelve**: the nine named there plus
**NFR-DQ-01** (data quality and target uncertainty), **NFR-TDEF-01**
(target-definition integrity) and **NFR-REP-01**, which the question listed but
the practices artifacts under-cite. All twelve are adopted. [TE §11]

| ID | Adopted meaning (not restated — see §11) | Pass/fail criterion here | Test |
|---|---|---|---|
| NFR-IRI-01 | IRI boundary integrity | `test_iri_denial.py` fails on deliberate injection; import-boundary check passes | WS-10, TA-07 |
| NFR-LEAK-01 | Forecast safety | Availability matrix asserts actual lag ≥ declared safe lag for every primary feature; no centered mean, no all-data scaling, no target-hour QC field as a feature | WS-11, TA-08, TA-11 |
| NFR-FAIR-01 | Fair comparisons | One comparison-wide mask per comparison set, stable ID, reported row counts, same window length and lag set | WS-16, TA-11 |
| NFR-REP-01 | Clean CPU reproducibility | The §13.2 ordered sequence completes on CPU from a clean environment | WS-20, TA-17 |
| NFR-DET-01 | Controlled randomness | Seeds fixed in `seeds.yaml`; three-seed element-wise mean is the confirmatory prediction; nondeterministic ops recorded | WS-17, TA-13 |
| NFR-DQ-01 | Data quality and target uncertainty | Units, times, signs and fill values documented; unexplained negative VTEC rejected; missingness and support reported by cell and month; target uncertainty budget produced | TA-19 |
| NFR-AUD-01 | Auditability and versioning | Stable IDs connect inputs to claims; registry is append-safe; failed runs stay visible | TA-10, TA-21 |
| NFR-SEC-01 | Secret protection and privacy | Secret scan over tree, history, configs, logs and artifacts returns clean; no PII stored | TA-22 |
| NFR-PHASE-01 | Phase-boundary integrity | `test_phase_boundary.py` plus the transition-manifest hash-diff test both pass | TA-27 |
| NFR-TDEF-01 | Target-definition integrity | Every target/prediction carries phase/source/definition IDs; no gridded value labelled a station observation; the grid-cell-versus-IPP mismatch disclosed | TA-15 |
| NFR-LIC-01 | Reuse and licensing integrity | Every adapted fragment has a complete §10.1 register row before use | TA-28 |

### NFRs the §11 set does not cover [Q5=C]

Three gaps were found. Each is proposed here with a **new** ID in a distinct
namespace so it cannot be confused with a §11 ID, and each is flagged as
requiring supervisor acceptance before it is treated as binding.

| ID | Requirement | Rationale — why §11 does not cover it | Pass/fail criterion | Test |
|---|---|---|---|---|
| REQ-NFR-A1 | **Driver release-grade integrity.** Every driver series records its release status (real-time / provisional / final), grades are never mixed within a series, and no value is backfilled from a future final archive | §11 has no driver-provenance NFR. NFR-LEAK-01 governs *timing*; a series can satisfy its declared lag while being built from reanalysed values — invisible to every existing check | Each driver manifest carries a single recorded grade for calendar 2022; a mixed-grade injection fails | `UNTESTED` |
| REQ-NFR-A2 | **Acquisition-window integrity.** Fold and partition membership derives from record timestamps only, never from a directory name or filename | §11 has no acquisition-provenance NFR. This gap already produced a realized defect: the year-blind predicate filed locked-test-month records under `audit_evidence_2022-01/` | `tests/test_acquisition_window.py` passes | `UNTESTED` |
| REQ-NFR-A3 | **Platform-parity of the gate.** The critical test set and both fixtures execute inside the platform where the governed run executes, not only locally | NFR-REP-01 governs *a* clean environment; it does not require the gate to run where the governed run runs. A Kaggle session carries no git working tree, so a commit hook cannot fire there | The Kaggle evidence record contains an in-session result | TA-03 |

---

## Constraints

**Technical.** Python 3.11 exactly; TensorFlow/Keras as the only NN stack;
PyTorch prohibited; R, Julia and MATLAB prohibited for the pipeline
[TE §8.1, §8.3]. Exactly two execution platforms — Kaggle and local; Google
Colab and Google Drive removed as governed platforms [TC-03c]. CPU is a
complete execution path, not an emergency mode [TC-01]. Exactly four governed
config files; no scientific constant in source or a notebook [TC-03e]. Notebooks
do not own production logic [TE §7, §14]. `ruff` for lint and format, configured
in `pyproject.toml` [practices].

**Data.** Three cells only, calendar 2022 only, December 2022 locked. NICO holds
53.8% of its native 5-minute slots against 96.4% of its hourly bins, so any
question requiring 5-minute resolution at NICO is out of reach on this dataset
and must not be claimed [D-7]. `evidence/audit_evidence_2022-FULL/` rests on
twelve monthly runs whose provenance is **unverifiable in principle** — no
provider byte stream exists in the workspace, and three months (2022-04,
2022-07 and **2022-12, the locked-test month**) have no `raw_isprint_cache/` at
all. Every artifact produced before the re-acquisition carries that caveat, and
FULL must not be relied on at a freeze gate while its provenance chain points
at superseded per-month hashes [practices; DATA-07].

**Organizational.** Single-author thesis codebase; the supervisor signs at named
freeze gates rather than reviewing merges [practices]. No CI service is used;
`ci-pipeline` (3.7) is SKIP in this scope. `user-stories` (2.4) is SKIP, so
WS/TA rows are the only acceptance vocabulary. No implementer or coding agent
may fill a `TBD — freeze gate` value by convenience [Vision §1.2] [TE §1.1].

---

## Success and acceptance

Vision's success framework is **adopted by reference**; only the measurable
engineering acceptance criteria are stated here. [Q9] The three success layers
(project completion, statistical evidence, practical relevance) and the
comparison hierarchy with its three mandatory difficulty controls live in
Vision §5 and §2.4 and in the intent statement's `## Success Metrics`.

**Engineering acceptance is independent of scientific outcome.** [Q9=C] The
pipeline passes engineering acceptance when its requirements above are met with
their evidence — regardless of whether the LSTM beats IRI-2016 or the
difficulty controls. **A correctly executed negative result passes engineering
acceptance.** A result that favours the model but was produced by a pipeline
failing a leakage, mask, seed or locked-test requirement does **not**.

Recording this separation is not a softening of the bar. It removes the one
incentive that most reliably corrupts a governed pipeline: the temptation to
treat an unfavourable result as an engineering defect to be debugged away.

**Engineering acceptance criterion.** WS-09 through WS-20 all `PASS` with
evidence links [FR-WS-4], the §18.3 preflight gate green [FR-WS-7], and the
applicable TA rows `Pass`. Visual inspection alone is insufficient at every
row [TE §16, §19].

### Open supervisor gates

Enumerated in full, not only those on the visible critical path. [project.md
§ Way of Working]

| Gate | What it accepts | Status | Owner |
|---|---|---|---|
| G-P1A | Prepared-data acceptance, incl. the §6.1B coverage minimum | Blocked — §6.1B value unfrozen; replacement audit pending | Supervisor |
| G-05 | Experiment freeze; December cannot open without it | Open | Supervisor |
| G-06 | Locked-test access; one write, hash before metrics | Blocked on G-05 | Supervisor |
| G-07 | Reproducibility — clean-run log, matched artifacts, `environment_and_cpu_preflight_report` | Blocked; due before thesis submission | Supervisor / reviewer |
| G-P2 | Code-reuse and licence approval | Open | Supervisor |
| G-P3A | WS-01–WS-08 raw-processing acceptance (deferred from Phase 1) | Deferred to Phase 2 | Supervisor |
| G-P3C | Protected hashes unchanged across the phase transition | Not yet reached | Supervisor |

---

## Out of scope

Three lists, kept separate because the three exclusions have three different
reasons and conflating them would hide why. [Q6]

**A. Future (Vision §3.5)** — excluded because they are later work, not because
they are prohibited: operations, real-time ingestion, monitoring, service
deployment. Models here are versioned artifacts with a registry, not deployed
services [TE §7.0A stage 6, §8.2].

**B. Phase 2 (§7.0 hard prohibition)** — excluded because Phase 1 code is
**barred** from them: full-year GNSS-derived VTEC construction, RINEX parsing,
DCB handling, STEC calculation, mapping, satellite and arc fields. Phase 1 code
paths must not import or execute `src/gnss/rinex.py` or
`src/gnss/calibration.py` [NFR-PHASE-01].

**C. Out-of-claim (D-8)** — excluded because no claim may extend there:
generalisation beyond ARUC 40/44, BSHM 32/35 and NICO 35/33; beyond calendar
2022; beyond December 2022 as the test month; beyond the +1 h confirmatory
horizon. The +24 h horizon is an optional extension outside the critical path,
and no thesis claim depends on it [intent]. No horizon between +1 h and +24 h
is authorised.

**D. What a reader might expect but will not get** [Q6=C] — stated so its
absence is not read as an oversight:

- **5-minute resolution at NICO.** Out of reach on this dataset; must not be
  claimed [D-7].
- **Receiver-specific station-observed VTEC.** The Phase 1 target is
  location-sampled gridded VTEC. Every IRI or GIM comparison carries a
  documented spatial-representativeness mismatch — a grid cell against a
  station-coordinate evaluation in Phase 1, an IPP cloud against a zenith
  estimate in Phase 2 — and part of any measured difference is a geometry and
  sampling artefact rather than skill [Vision §6.6] [TE §5].
- **Numerical equivalence between the Phase 1 and Phase 2 targets.** Cross-phase
  results test protocol transfer across a target-domain shift; agreement is not
  proof the two estimate the same physical quantity [Vision §2.2].
- **A second statistically independent blind test in Phase 2.** Phase 2 is a
  fixed-protocol replication on a new target lineage, because it reuses the
  December timestamps after Phase 1 has already reported them. This must be
  stated in the abstract-level interpretation [Vision §2.2, §7.0B; VAL-05].
- **Thesis chapter prose.** This initiative supplies figures, tables, metrics
  and methods text; the chapter is authored outside it [intent].

---

## Known defects in the authority documents

Every known defect this document relies on is recorded with the reading adopted
and its status, so a later reader is not misled by the source. [Q10]

| # | Defect | Reading adopted here | Status |
|---|---|---|---|
| 1 | **§16 vs §16.1 contradiction.** §16 states acceptance requires all 20 WS rows `PASS`; §16.1 assigns WS-01–WS-08 to the Phase 2 gate G-P3A, and §7.0's Phase 1 hard prohibition bars Phase 1 from producing the evidence those rows need. A Phase 1 fixture run cannot satisfy "all 20" without violating NFR-PHASE-01 | Phase 1's acceptance set is **WS-09 through WS-20**; WS-01–WS-08 deferred to G-P3A. See FR-WS-4 | **Resolved.** Supervisor-countersigned 2026-08-16, recorded on the student's report. Residual, recorded so it is not later misread as a coverage gap: no WS row covers train-only transforms in either subset; NFR-LEAK-01 is enforced through §18.3's gate-test list and TA-11 instead |
| 2 | **§1.3 stale counts.** The script and notebook counts in §1.3 do not match the §12 tree and §19 TA-01 | TA-01's enumeration (four configs, six packages, nine phase-aware stage scripts, five notebooks, tests, artifacts) is authoritative for REQ-ENG-1 | **Open.** Correction runs through Vision §15.2 change control, not through this workflow |
| 3 | **OC-03 over-broad wording.** Its "unexamined" phrasing, read flatly, forbids the pre-G-05 December coverage and regime audit that Vision §8.3 makes **required** | Two distinct events: the coverage/regime audit is required and performance-blind; the metrics evaluation is the one-shot, hash-gated G-06 event. Vision §8.3 supersedes OC-03's wording for coverage and regime counts. See FR-P1-02-3 and FR-P1-05-12 | **Open in the source; resolved in practice.** The reading is affirmed in `team-practices.md` § Testing Posture |
| 4 | **Vision §14.2 D-130 supersession pointers carry no counts.** The pointers name what supersedes what but not the affected row counts, so a reader cannot verify the supersession is complete | No requirement here depends on a D-130 count. Where a count is needed, the underlying artifact is counted directly | **Open.** Non-blocking for this stage |
| 5 | **TE §1.5 reads `Pending — D-144`** although D-3/D-144 was countersigned and recorded 2026-08-15 | D-144 is countersigned; Phase 1 acquisition is not blocked on it. The countersign is recorded as reported by the student; no signature artifact is filed in the repository | **Open in the source.** Updating §1.5, §2 and TA-25 runs through Vision §15.2 change control [GOV-22] |
| 6 | **Q5 of this stage's own question set under-enumerated §11 as nine NFRs.** §11 carries twelve | All twelve adopted; see § Non-functional requirements | **Resolved here** |
| 7 | **`scripts/merge_coverage_year.py`'s hash check verifies derived artifacts, not retrieval.** Every `sha256_manifest.json` hashes exactly four derived files and never the contents of `raw_isprint_cache/` — and that cache holds isprint text extractions, not provider `.hdf5` bytes | Fixture eligibility is judged on **derived-artifact** verification, not retrieval verification. Retrieval-level verification is unavailable until the re-acquisition [FR-P1-01-4] | **Open.** Closes when FR-P1-01-4 is satisfied |

---

## Assumptions & Open Questions

**Assumptions carried, with rationale.**

1. **[assumption] Supervisor approval reported at Q3 does not itself supply the
   §6.1B numerical coverage minimum.** The student states supervisor approval is
   held and asked that it not be re-raised. No numeric value accompanied that
   statement, and `project.md` § Forbidden bars any agent from filling a
   `TBD — freeze gate` value by convenience. FR-P1-02-4 is therefore written
   with the threshold as an explicit named hole and operates on D-2's interim
   rule (≥95% of calendar days per month, 100% of December) until the frozen
   number is recorded under its own D-number. **Recording that D-number is the
   student's action, not this stage's.** [Q3]
2. **[assumption] The one-month all-station scientific fixture window is still
   open** under Q-31. Only the seven-day plumbing window is frozen (D-11:
   2022-11-01 to 2022-11-07, all three cells). FR-WS-1 is complete in form and
   blocked in one value.
3. **[assumption] The twelve already-acquired months are re-verified under the
   new test suite rather than re-acquired from scratch** (Q8=A of
   practices-discovery). Existing bytes stay; the checks that validate them are
   rebuilt. This assumption is what makes FR-P1-01-4's "re-verified" clause
   meaningful rather than a second full acquisition.

**Open questions carried forward.**

1. **§1.3's script/notebook count** — affects how the pipeline decomposes into
   units at `units-generation` (2.7). Defect #2 above.
2. **The coordinate-to-cell rule** — a §18.2 forbidden-choice item requiring
   Student **and** Supervisor approval, currently a self-labelled "PROVISIONAL"
   inline function in the coverage notebook. FR-ENG-8 sequences the freeze
   before the migration; the freeze itself is not this stage's to make.
3. **The AGPLv3 distribution question** on the Global-TEC-forecasting
   repository — a governance dependency this project does not resolve on its
   own. FR-P1-06-4 states the standing default (reimplement from the paper)
   while it remains open.
4. **D-9 and D-10 signature rows remain blank**, so the acquisition route and
   the driver-source corrections are sole-signed [GOV-22].

## Requirements with no testing row

Listed rather than invented. [Q1] Each carries a real pass/fail criterion above;
what is missing is a §16 or §19 row that tests it. These are the concrete input
`nfr-requirements` (3.2) needs when it assembles the G-05 freeze manifest, and
several are candidates for a new TA row through Vision §15.2 change control.

REQ-ENG-7, REQ-ENG-9, FR-P1-01-5, FR-P1-01-7, FR-P1-01-8, FR-P1-01-9,
FR-P1-04-4, FR-P1-04-10, FR-P1-05-3, FR-P1-05-5, FR-P1-05-6, FR-P1-05-7,
FR-P1-05-14, FR-P1-05-15, FR-WS-2, FR-WS-3, REQ-NFR-A1, REQ-NFR-A2.

Two of these are worth naming as the most consequential gaps: **FR-P1-05-7**
(the confirmatory estimand itself has no TA row — TA-14 tests the bootstrap
that carries it, not the estimand's definition) and **FR-P1-01-5 /
REQ-NFR-A2** (the acquisition-window predicate, which has already produced one
realized defect and is guarded today only by a project-authored test).

## Traceability

Inline source tags appear on every requirement above; this table is the audit
view of the same mapping. [Q7]

| Requirement group | Primary authority | Ideation origin | Test rows |
|---|---|---|---|
| REQ-ENG-1…9 | TE §12, §8.1, §10, §18.3; TC-06, TC-03d | intent § Initial Scope Signal (deliverable: runnable pipeline); practices § Way of Working, § Code Style | TA-01, TA-02, TA-03, TA-09, TA-16, TA-22, TA-26 |
| FR-P1-00-1…2 | TE §7.0 P1-00; D-143; Vision R-23 | intent § Phase 1 source status | TA-25, TA-31 |
| FR-P1-01-1…10 | TE §7.0 P1-01, §10, §13.3; D-144, D-5, D-10.1/.2/.3 | intent § Driver contract, § Driver preconditions, obligations 1–2 | TA-03, TA-04, TA-08, TA-15, TA-22, TA-32 |
| FR-P1-02-1…5 | TE §7.0 P1-02; Vision §6.1B; D-2 | intent § Frozen modelling target | WS-01, WS-18, TA-04, TA-25 |
| FR-P1-03-1…4 | TE §7.0 P1-03, §7.0 prohibition, §13; NFR-PHASE-01, NFR-TDEF-01 | intent § Target representativeness — binding | TA-04, TA-15, TA-27 |
| FR-P1-04-1…11 | Vision §6, §6.4, §7.1, §8.2; TE §5.2, §6.2, §7.1, §13.3; TC-08–TC-16 | intent § Benchmark role, § Driver contract | WS-09…WS-13, WS-16, TA-07, TA-08, TA-11, TA-15 |
| FR-P1-05-1…15 | Vision §2.3, §2.4, §5.3, §8.3, §8.6, §8.7; TE §1.3, §7.2, §13.4, §13.6 | intent § Primary estimand, § Metrics, § Mandatory difficulty controls, § Model set, § Reporting, § Test-set sealing condition | WS-14, WS-15, WS-17, WS-18, WS-19, TA-10, TA-12, TA-13, TA-14, TA-18, TA-19, TA-20 |
| FR-P1-06-1…4 | TE §2.2, §7.0B, §10.1; NFR-LIC-01 | intent § Governance Dependencies (G-P2) | TA-27, TA-28 |
| FR-WS-1…7 | TE §9.1, §9.2, §13.2, §16, §16.1, §18.3; D-11; TC-01, TC-03f, TC-03g | practices § Walking Skeleton, § Testing Posture | WS-09…WS-20, TA-03, TA-09, TA-17, TA-23, TA-26 |
| NFR-IRI-01 … NFR-LIC-01 | TE §11 (adopted by reference, IDs unchanged) | intent § Success Metrics phase-boundary note | as tabulated in § Non-functional requirements |
| REQ-NFR-A1…A3 | Gaps found against TE §11; TE §10 driver table, §9.1 | practices § Testing Posture; board findings TEC-04, ML-07, BENCH-01 | mostly `UNTESTED` |

**Traceability rule honoured.** No requirement above is new. Each derives from
Vision v4.2, Technical Environment v3.2, a D-number decision, the constraint
register, the intent statement, or the affirmed practices — and says which.
[phases/inception.md § Traceability] The three REQ-NFR-A items are the single
exception class, and each is explicitly marked as a **proposed** addition
requiring supervisor acceptance, with its origin (the board finding that
exposed the gap) named.

## Review

READY

*(Advisory review by aidlc-product-lead-agent, iteration 1, single non-repeating pass. Findings below go verbatim to the human approval gate.)*

### Findings

1. **Major — the "Correction to the question text" NFR count is internally inconsistent and inflates §11's actual count.** (§ Non-functional requirements, lines 246–250.) The text states: *"`requirements-analysis-questions.md` Q5 enumerated nine §11 NFRs. §11 carries **twelve**: the nine named there plus **NFR-DQ-01**..., **NFR-TDEF-01**..., and **NFR-REP-01**, which the question listed but the practices artifacts under-cite. All twelve are adopted."* But the Q5 question stem it is "correcting" already lists `NFR-REP-01` among its nine IDs ("NFR-IRI-01, NFR-LEAK-01, NFR-FAIR-01, **NFR-REP-01**, NFR-DET-01, NFR-PHASE-01, NFR-SEC-01, NFR-LIC-01 and NFR-AUD-01" — `requirements-analysis-questions.md` line 76), so counting it a second time as one of the "plus" three double-counts it: 9 + 2 genuinely-new IDs (`NFR-DQ-01`, `NFR-TDEF-01`) = 11, not 12. This matches the source: `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §11 (lines 533–543) defines exactly eleven NFR IDs (`NFR-IRI-01`, `NFR-LEAK-01`, `NFR-FAIR-01`, `NFR-REP-01`, `NFR-DET-01`, `NFR-DQ-01`, `NFR-AUD-01`, `NFR-SEC-01`, `NFR-PHASE-01`, `NFR-TDEF-01`, `NFR-LIC-01`), and the artifact's own adoption table two paragraphs later (lines 252–264) lists exactly eleven rows — the table and its own preceding prose disagree by one. This is precisely the kind of authority-document-defect bookkeeping error Q10 was answered "A" to catch and record; here the artifact introduces a new one of its own, uncaught. Fix: change "twelve" to "eleven" and "the nine named there plus NFR-DQ-01, NFR-TDEF-01 and NFR-REP-01" to "the nine named there plus NFR-DQ-01 and NFR-TDEF-01," or otherwise reconcile the prose with the eleven-row table.

2. **Major — TA-09's own wording still requires "all 20" WS rows, and the artifact cites TA-09 as a test link for Phase-1-scope requirements without flagging the resulting contradiction with FR-WS-4.** `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` line 1014 defines TA-09 verbatim as: *"Both walking-skeleton fixtures pass **all 20** Section 16 checks with evidence links."* The artifact's § Known defects table (item 1, lines 404) records and resolves the **§16 vs §16.1** contradiction (§16 says "all 20 PASS"; §16.1 defers WS-01–WS-08 to G-P3A) by adopting FR-WS-4: "Phase 1's acceptance set is WS-09 through WS-20." But TA-09 is a separate, §19 row that independently repeats "all 20," and it is not named in the Known-defects table at all. The artifact nonetheless cites TA-09 as the test link for REQ-ENG-4 (line 128) and FR-WS-1 (line 230) — both Phase-1-scope requirements — and § Success and acceptance (line 331) states engineering acceptance requires "the applicable TA rows `Pass`," which would include TA-09 as written. A reader cannot tell whether TA-09 is (a) also superseded by the WS-09–20 reading, (b) genuinely unsatisfiable in Phase 1 the way §16 was, or (c) satisfied some other way — the artifact is silent. Fix: add TA-09 to § Known defects (or extend defect #1) with an explicit reading, e.g. "TA-09 is read as bounded by the same WS-09–WS-20 acceptance set as §16.1," and note its status (open/resolved) the way defect #1 does.

3. **Minor — Scoped Verification Obligation #5 from the intent statement (evaluation code must be authored, reviewed, and frozen as part of the G-05 set) has no corresponding requirement ID.** `ideation/intent-capture/intent-statement.md` § Scoped Verification Obligations, row 5: *"No evaluation code exists yet. It is authored inside this initiative and must be complete, reviewed and frozen as part of the G-05 set before December 2022 is opened."* This is a binding, checkable obligation ("complete, reviewed and frozen ... before December is opened") but no `FR-P1-05-*` or other requirement in this document states it as a pass/fail criterion with its own ID — the closest, FR-P1-05-12 (locked-test guard) and FR-P1-05-5 (grid freeze before G-05), cover adjacent but different content (access blocking and hyperparameter grids, not evaluation-code completeness/review/freeze). Under Q1's own rule ("Requirements with no testing row are flagged rather than invented"), the expected treatment for a sourced-but-uncovered obligation is a requirement ID in § Requirements with no testing row, not silent omission. Fix: add a requirement (e.g. `FR-P1-05-16`) stating the evaluation-code completeness/review/freeze obligation, sourced to the intent statement's obligation 5, and list it under § Requirements with no testing row if no WS/TA row covers it.

4. **Minor — TA-12's `B-01`/`C-01` model-ID and "generated, not trained" evidence scope is not decomposed into its own requirement.** `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` line 1017 defines TA-12 as covering *"All required model IDs M-01–M-06 plus **B-01 and C-01**"* (B-01 = IRI-2016 benchmark, C-01 = GIM comparator, both "generated, not trained" per line 424–425). FR-P1-05-1 (line 201), which is the requirement citing TA-12 as its test link, states only the M-01–M-06 model set and says nothing about B-01/C-01 or the generated-not-trained distinction TA-12 also checks. FR-P1-04-9 covers IRI/GIM evaluation-time usage but not this specific TA-12 grep-evidence scope. This leaves part of what TA-12 tests unaccounted for by any single requirement's stated criterion.

No findings on: Q3's handling of the unfrozen §6.1B coverage minimum (FR-P1-02-4 correctly writes the threshold as a named hole per the Forbidden-rule bar on filling TBD values, matching the Consolidated Summary's Q3 reading); the Q2 decomposition-by-P1-00..P1-06 structure (matches `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §7.0's stage table verbatim); the §16/§16.1 contradiction itself (correctly identified and resolved per the supervisor-countersigned FR-WS-4); the Q4/DATA-03/DATA-04 closure requirements (FR-P1-01-3 and FR-P1-01-4 explicitly name the DATA-03/DATA-04 items they close); or the out-of-scope, traceability-table, or "constraints inherited" sections, which are internally consistent and correctly sourced.
