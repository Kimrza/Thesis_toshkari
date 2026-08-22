# Project Vision and Research Definition

## Modeling and Error Reduction in Ionospheric TEC Estimation Using GNSS Data and Machine Learning

**Author:** Kimia Rezaei  
**Supervisor:** Dr. Reza Saraf Shirazi  
**Institution:** Amirkabir University of Technology, Faculty of Electrical Engineering  
**Document version:** 4.3 — Custody Remediation, Target-Definition Freeze and Reproducibility Safeguards  
**Date:** 11 August 2026  
**Status:** Project-owner-approved configuration; scientific readiness gates require the approvals listed in Section 13

---

## 1. Document Authority and Use

### 1.1 Purpose

This document is the single source of truth for the thesis preflight. It defines the project's scientific question, boundaries, data contract, experiment hierarchy, evaluation rules, implementation constraints, decision record, readiness gates, and acceptable claims.

### 1.2 Authority

- Sections 1–17 are the **normative core**. "Must," "shall," and "required" indicate binding project rules.
- Appendices are **nonnormative supporting material**. They explain evidence and rationale but cannot override the normative core.
- If an appendix conflicts with the normative core, the core governs.
- A parameter labeled **freeze gate** must be resolved, recorded, and approved before the affected work begins. It must not be guessed by an implementer or AI coding agent.
- A material change after the locked test is opened makes the affected analysis exploratory unless a new untouched test period is approved.
- The approved proposal is immutable and is never edited by this document.

### 1.3 Approval Meaning

This version adopts the answers recorded in the *TEC Project Finalization Decision Questionnaire* (Q-01 through Q-33, author-confirmed 7 August 2026). It is final as a preflight specification, but it does not falsely claim that data-dependent settings have already been measured or that the academic supervisor has signed every readiness gate.

### 1.4 Change History

| Version | Date | Change | Status |
|---|---|---|---|
| 0.1 | June 2026 | Initial Vision Document | Superseded |
| 1.0 | 28 July 2026 | Combined preflight draft | Superseded |
| 2.0 | 28 July 2026 | Applied P-01–P-34 recommendations; created normative core and appendices | Superseded |
| 3.0 | 8 August 2026 | Applied Q-01–Q-33 questionnaire decisions. Primary story changed to independent local ML versus IRI benchmark; residual-correction models and GRU removed; climatology baseline added; GPS-only scope; F4 fold added; paired-loss estimand; vector block bootstrap; horizons split into required +1 h and optional +24 h | Superseded |
| 4.0 | 11 August 2026 | Adopted Recommendations 1–8: one TensorFlow/Keras forecasting stack; prepared-data Phase 1 and raw-observation Phase 2; ICTP prepared VTEC source with an explicit coverage gate and Madrigal fallback; Phase 1 model/protocol freeze; cross-processor validation; external-method and code-reuse register; direct code reuse with licensing controls; Phase 2 acceptance gates | Superseded |
| 4.1 | 11 August 2026 | Approved a student-executed Kaggle notebook as the Phase 1 ICTP acquisition interface; fixed its output, provenance, integrity, and coverage-gate evidence; retained the standalone Python downloader as the reusable automation companion | Superseded |
| 4.2 | 11 August 2026 | Recorded the executed ICTP audit as a failed G-P1A source gate; rejected ICTP for confirmatory Phase 1 training; recommended MIT Haystack Madrigal MAPGPS binned VTEC as the single-source replacement candidate, subject to supervisor approval, exact 2022 coverage/schema audit, and explicit gridded-target limitations | Superseded |
| 4.3 | 21 August 2026 | Approved D-144 (§14.2, §17 annotated); froze the §6.1B numerical coverage minimum at ≥90% usable hourly coverage per station per month alongside D-2's day rule (**D-12**); fixed the §5.2 H4/SRQ-5 demotion threshold to §9.3's three-independent-storm-event rule (**D-13**). Amendments were applied **in place with inline annotations** naming their change records rather than by rewriting sections, so each amended row states its own provenance. Change records: `governance/CHANGE_RECORD_2026-08-21_D-144.md`, `governance/CHANGE_RECORD_2026-08-21_freezes.md`. Approved by the project owner under the recorded student/supervisor authority equivalence; no supervisor signature artifact exists and none is claimed | **Current** |

### 1.5 What Changed in Version 3.0

This is a material change under Section 15.2. The locked test has not been accessed. No model has been trained. No result has been observed. The change is therefore preregistration, not post-hoc revision.

| Area | v2.0 | v3.0 | Source |
|---|---|---|---|
| Primary comparison | Direct LSTM versus persistence | Independent local ML versus IRI-2016 benchmark, with persistence, seasonal persistence and climatology as mandatory co-reported difficulty controls | Q-01, Q-20 |
| IRI role | Baseline **and** residual anchor **and** model input | External benchmark only; architecturally excluded from every ML feature and target | Q-01, Q-02 |
| Residual models | M-07, M-08 required | Removed from the required ladder | Q-01, Q-20 |
| Climatology | Absent | Fitted station×month×hour climatology required | Q-20 |
| GRU | Not authorised, gate open | Gate closed; removed | Q-20, Q-33 |
| Horizons | +1 h only | +1 h confirmatory required; +24 h optional post-completion extension | Q-03 |
| Constellations | Unspecified | GPS-only L1/L2 at 30 s | Q-07 |
| Folds | F1–F3 | F1–F4 (November validation added) | Q-23 |
| Primary estimand | Percentage RMSE reduction | Paired loss differential with 95% CI; percentage reduction is a derived summary | Q-26 |
| Bootstrap | Within-station blocks, 2,000 replicates | Vector time-block bootstrap carrying all stations together, 10,000 replicates, seed 20221201 | Q-27 |
| Seeds | Three seeds reported | Three-seed element-wise mean is the confirmatory prediction | Q-22 |
| Tuning | "No more than 20 trials" | Exact frozen grids: ridge 6, RF 18, LSTM 16 | Q-21 |
| SSN | Candidate feature | Removed | Q-16 |
| Dst | Candidate primary feature | Diagnostic / hindcast-only | Q-16 |
| Platforms | Kaggle + Colab + Drive + local | Kaggle + local only; CPU is a complete path | Q-29 |

### 1.6 Approved Two-Phase Amendment (11 August 2026)

This amendment was approved before any locked-test performance was viewed. It changes implementation order and software ownership, but it does not relax the IRI-free information boundary, fair-comparison rules, chronological evaluation, or bounded claims.

| Recommendation | Approved decision | Normative effect |
|---|---|---|
| R-01 | Use **TensorFlow/Keras for both phases** | The same forecasting implementation is retained across phases. Phase 2 raw GNSS processing remains framework-independent. PyTorch is not used in the governed pipeline. |
| R-02 | Approve the two-phase program | Phase 1 validates the ML hypothesis using prepared VTEC; Phase 2 builds and validates the raw-to-VTEC pipeline and retrains the frozen model. |
| R-03 | Approve a credentialed 2022 prepared-data source | ICTP was the initial candidate, conditional on §6.1B. The executed audit failed; ICTP is now retained only as source-rejection evidence and cannot supply confirmatory Phase 1 training data. |
| R-04 | Approve the transition rule | Architecture, features, splits, baselines, metrics, seeds, and tuning protocol freeze after Phase 1. Target lineage changes in Phase 2; if Madrigal is adopted, the predeclared grid-cell-to-IPP target-domain shift is also carried explicitly rather than treated as equivalence. |
| R-05 | Approve cross-processor validation | Independently produced Phase 2 VTEC is compared against Phase 1 prepared VTEC and external references on matched timestamps before model retraining. |
| R-06 | Approve an external-method/code register | Every reused method or code fragment records repository, commit, purpose, modifications, validation, citation, and license. |
| R-07 | **Option 1 — direct code reuse** | Useful code may be copied when its license is compatible; notices and attribution are preserved and copied code is isolated and tested. |
| R-08 | Approve phase-specific acceptance gates | Phase 2 may begin only after the Phase 1 evidence package and protocol freeze pass; Phase 2 model results are inadmissible until raw-target validation passes. |
| R-09 | Use the supplied Kaggle notebook for Phase 1 acquisition | The student runs `00_ictp_phase1_download_kaggle.ipynb` with Kaggle Internet enabled. The resulting ZIP, expanded files, manifests, checksums, coverage summary, and executed notebook are retained as acquisition evidence. Download success does not waive §6.1B. |

### 1.7 Measured Source Failure and Replacement Recommendation (11 August 2026)

#### Recommendation 10

**Category**
- Requirements
- Architecture
- Data
- QA

**Severity**
- Critical

**Issue**

The executed ICTP audit found 27 non-empty ARUC days (7.397%), 35 non-empty BSHM days (9.589%), and no NICO 2022 directory (HTTP 404). The archive passed ZIP integrity, but the source cannot support the fixed January–November folds, the December locked test, or a three-location pooled experiment.

**Importance**

Training on this audit archive would invalidate the planned experiment. Removing NICO would not repair the missing seasonal coverage, and mixing providers would change the target definition by station.

**Risk**

If unchanged, the thesis would train on a sparse, seasonally clustered subset, omit a required location, and make performance estimates that cannot answer the preregistered question.

**Possible Solutions**

1. Use MIT Haystack Madrigal MAPGPS `gps` binned VTEC for all three station coordinates in 2022, after a file-, cell-, and timestamp-level coverage audit.
2. Audit IONOLAB-TEC station products; access requires login and availability for all three stations has not been established.
3. Change the station set or year to obtain one complete station-level prepared product.
4. Use an IGS analysis-center GIM, accepting its coarser grid/cadence and redesigning the target, horizon, and comparator roles.

**Comparison**

| Option | Advantages | Disadvantages |
|---|---|---|
| Madrigal MAPGPS binned VTEC | Public research infrastructure; prepared VTEC; 1°×1° cells at 5-minute cadence; global archive since 2000; API and permanent citation support | A map-cell target, not receiver-specific IPP-median VTEC; missing cells remain possible; CODE GIM becomes a map-to-map comparator rather than independent validation |
| IONOLAB-TEC | Potentially closest to station-level prepared VTEC | Login required; ARUC/BSHM/NICO 2022 coverage and automated access are unverified |
| Change station/year | Can preserve station-derived physical target | Changes the approved geographic or temporal scope and may reduce comparability with Phase 2 plans |
| IGS GIM | Credentialed, stable, global coverage | Coarser spatial/temporal product; conflicts with the existing GIM comparator and +1 h target contract |

**Recommendation**

Use **MIT Haystack Madrigal MAPGPS `gps` binned VTEC as the preferred replacement candidate**, sampled consistently at the three frozen station coordinates and aggregated to the hourly modeling interface. This recommendation is conditional: it becomes the Phase 1 source only after the supervisor approves the map-cell target definition and a target-independent audit confirms adequate 2022 coverage in all three cells, including December. The `los` product is not the Phase 1 replacement because converting line-of-sight TEC to VTEC would move Phase 2 scientific processing into Phase 1.

**Decision Required**

The student and supervisor must **Approve, Reject, Modify, or Postpone** this replacement. Until approval and the new source gate pass, Phase 1 training remains blocked.

---

## 2. Executive Research Definition

### 2.1 Core Problem

Empirical ionospheric products such as IRI-2016 are climatological. They may differ substantially from quality-controlled station-level VTEC, especially when local conditions depart from climatology. A machine-learning model may predict local VTEC more accurately, but a one-year, three-station dataset can create misleading results through temporal leakage, benchmark contamination, unfair baselines, weak target construction, excessive tuning, or geographic overclaiming. The two-phase design first tests the forecasting hypothesis on a provider-prepared target, then tests whether the conclusion survives when the project independently constructs the target from raw observations.

### 2.2 Primary Research Question

> Under a leakage-free chronological protocol, does a pooled compact TensorFlow/Keras LSTM trained **only** on VTEC history and predeclared causal non-IRI predictors produce more accurate one-hour-ahead VTEC forecasts than the IRI-2016 empirical benchmark at ARUC, BSHM, and NICO on the locked December 2022 test—and is that conclusion consistent when the prepared Phase 1 target is replaced by the independently produced Phase 2 target?

The model must stand on its own. It must not learn to adjust IRI, and it must never receive an IRI-derived value as an input or a target.

### 2.3 Primary Estimand

The confirmatory quantity is the **paired loss differential**, evaluated on the frozen comparison mask:

\[
\Delta_{L} = \overline{\left(L^{\mathrm{IRI\text{-}2016}}_{i} - L^{\mathrm{LSTM}}_{i}\right)}
\]

where \(L_i\) is the squared error at eligible row \(i\), the mean is taken within station and then combined with **equal-station weighting**, and a 95% confidence interval is produced by the vector time-block bootstrap of Section 9.2.

**Sign convention: positive values favour the LSTM.** This convention is binding and must be stated in every table.

The derived, non-confirmatory summary is:

\[
\Delta_{\mathrm{RMSE}\%} =
\left(1-\frac{\mathrm{RMSE}_{\mathrm{LSTM}}}{\mathrm{RMSE}_{\mathrm{IRI\text{-}2016}}}\right)\times 100\%.
\]

Percentage reduction is reported for readability only. It has an unstable denominator in small strata and shall never be the basis of the statistical evidence claim.

### 2.4 Comparison Hierarchy

1. **Primary confirmatory comparison:** direct compact LSTM versus IRI-2016 benchmark.
2. **Mandatory difficulty controls, co-reported in the primary results table:** LSTM versus persistence, versus 24-hour seasonal persistence, and versus fitted station×month×hour climatology. These are not optional and may not be relegated to an appendix. Their purpose is to prevent success being defined solely by beating a climatological benchmark.
3. **Secondary learned-model comparisons:** LSTM versus direct Random Forest and versus ridge regression.
4. **Contextual comparison:** external GIM comparator.
5. **Declared sensitivities:** no-DOY ablation, differenced-target ablation, forecast-safe space-weather ablation, 48-hour history, 48-hour bootstrap blocks, top-1%-error-removed.

No secondary result may replace, redefine, or rescue the primary conclusion after December results are opened.

**Binding honesty rule.** If any baseline in tier 2 achieves a lower paired loss than the LSTM on the locked test, that fact must appear in the primary results table and in the abstract-level conclusion. A favourable LSTM-versus-IRI result does not license silence about an unfavourable LSTM-versus-persistence or LSTM-versus-climatology result.

### 2.5 Study Population and Claim Boundary

The study covers:

- ARUC, BSHM, and NICO — described as **three IGS stations in the mid-latitude Eastern Mediterranean–South Caucasus sector**;
- calendar year 2022;
- one-hour-ahead, station-level VTEC forecasts;
- the timestamps that survive the frozen quality and comparison masks.

The sector name is **descriptive only**. Statistical inference is bounded strictly to these three stations, this year, this forecast horizon, and the documented processing choices. The three sites form a coherent geometric triangle but are strongly correlated and do not constitute independent spatial sampling.

The results do not establish performance for all of Iran, the whole Eastern Mediterranean–South Caucasus sector, arbitrary locations, other solar-cycle phases, other forecast horizons, or operational real-time use.

The hourly target is an **ionospheric-pierce-point aggregate**, not a zenith column above the antenna. See Section 6.4. All comparisons with IRI and GIM, which are evaluated at the station coordinate, carry this documented mismatch.

---

## 3. Vision, Objectives, and Capability Map

### 3.1 Long-Term Vision

Create a reproducible regional research framework that can ingest calibrated GNSS observations, produce quality-controlled station VTEC, compare an independently trained local model against empirical and data-driven references fairly, and later expand to additional years, stations, horizons, and positioning-domain validation.

### 3.2 MVP Vision

Deliver an auditable **Phase 1 MVP** using a prepared 2022 VTEC product for ARUC, BSHM, and NICO. The MVP shall determine whether an independently trained local ML model improves on the IRI-2016 benchmark while simultaneously reporting persistence, seasonal persistence, climatology, ridge, and Random Forest. Phase 1 validates the forecasting hypothesis; it does not claim that this project extracted TEC from raw satellite observations.

### 3.3 Research Objectives

1. **Phase 1:** select, audit, and standardize a prepared VTEC product without parsing or calculating TEC from raw GNSS files.
2. Implement one pooled direct compact LSTM in TensorFlow/Keras, trained on an architecturally IRI-free information set.
3. Evaluate the Phase 1 LSTM against IRI-2016 and the complete baseline ladder using a locked chronological test.
4. Freeze the Phase 1 model and evaluation protocol after the evidence package passes its acceptance gate.
5. **Phase 2:** independently produce validated hourly GNSS-derived VTEC from raw observations using an established package plus a transparent, tested project calibration layer.
6. Cross-validate the Phase 2 target against the prepared Phase 1 product and external references on matched timestamps.
7. Retrain the frozen TensorFlow/Keras model on the Phase 2 target and compare it fairly with Phase 1 and the baselines.
8. Report overall, per-station, quiet/disturbed, target-quality-stratified, and cross-phase results with paired uncertainty.
9. Produce reproducible data, code, experiment, provenance, licensing, and evidence artifacts.

### 3.4 Technical Objectives

- UTC-normalized, provenance-rich hourly data.
- Forecast-time-safe features with machine-testable publication lags.
- An architecturally enforced IRI-free ML information set.
- Train-only fitting of transformations.
- Configuration-driven experiments across exactly four configuration files.
- Common comparison-wide evaluation-mask manifests.
- Bounded frozen search grids and deterministic settings where feasible.
- Versioned datasets, models, predictions, metrics, and figures.
- A clean-run reproduction contract within the available compute and storage limits, on CPU.

### 3.5 Required Capabilities

| Group | Required capability | MVP status |
|---|---|---|
| Domain | STEC/VTEC, DCB, mapping, IPP geometry, station metadata, geomagnetic regimes | Required |
| Data | Phase 1 prepared-VTEC ingestion; Phase 2 RINEX/CRX processing, QC, hourly aggregation; GIM/IRI alignment | Required by phase |
| Forecasting | Causal windows, availability-safe features, chronological splits | Required |
| Models | Persistence, seasonal persistence, climatology, ridge, RF, compact LSTM | Required |
| Benchmarks | IRI-2016 generation and matched evaluation; GIM comparator | Required |
| Evaluation | Comparison-wide masks, paired metrics, vector block bootstrap, station/regime reporting | Required |
| Reproducibility | Configs, manifests, hashes, registry, clean-run test | Required |
| Communication | Traceable tables, figures, decisions, limitations | Required |
| Operations | Real-time ingestion, monitoring, service deployment | Future |
| Advanced ML | Transformers, attention, GRU, BiLSTM, GNNs, broad architecture search | Future |

### 3.6 Two-Phase Implementation Contract

| Dimension | Phase 1 — Prepared-data MVP | Phase 2 — Raw-to-VTEC pipeline |
|---|---|---|
| Precise objective | Test the forecasting hypothesis quickly and rigorously using ready-to-use VTEC, establishing whether the proposed model merits full pipeline development. | Demonstrate that the project can independently derive a scientifically defensible VTEC target from raw satellite observations, then test whether the frozen Phase 1 model remains effective. |
| In scope | Source selection; licensing/provenance; coverage and schema audit; cleaning; hourly harmonization; causal features; chronological splits; TensorFlow/Keras training and tuning; fair baseline comparison; uncertainty analysis. | Raw-file acquisition and inventory; parsing; observable/cadence checks; slips/arcs; DCB handling; STEC; mapping to VTEC; QC; external validation; hourly target construction; frozen-model retraining; cross-phase comparison. |
| Out of scope | RINEX/CRX parsing, satellite geometry, DCB estimation/application, STEC calculation, STEC-to-VTEC mapping, or modification of the provider's calibration. | New architecture search, new feature families, different folds or metrics, test-driven hyperparameter changes, or silently substituting a different target definition. |
| Primary input | Provider-processed VTEC plus station/time metadata and documented QC/provenance fields. | Raw dual-frequency satellite observations, navigation/orbit information as required, station logs, DCB products, and frozen processing configuration. |
| Primary output | Versioned prepared-target release, frozen TensorFlow/Keras model protocol, predictions, metrics, confidence intervals, and an MVP go/no-go report. | Versioned independently produced target, processor-verification and uncertainty reports, retrained-model results, 2×2 cross-target evaluation, and a final reproducibility package. |
| Success criterion | The pipeline is leakage-free and reproducible, all mandatory models sit the same exam, and the result—positive, negative, or inconclusive—is statistically interpretable. Meaningful improvement requires the §5.3 evidence rule. | Raw-target acceptance gates pass; the same model/protocol is retrained; comparisons use common timestamps and masks; target shift is separated from model shift; conclusions remain within the three-station 2022 boundary. |

#### 3.6.1 Correct Step Order, Inputs, and Outputs

| Order | Phase | Step | Input | Measurable output |
|---:|---|---|---|---|
| 1 | 1 | Close the failed ICTP audit; obtain supervisor approval for one replacement; audit its 2022 product, cells, timestamps, rights, and station-coordinate mapping | ICTP audit evidence, replacement-provider catalog/documentation, authoritative station coordinates, and approved acquisition code | ICTP source-rejection record; replacement decision; executed acquisition/audit record; file hashes; access record; cell/day/month coverage matrix |
| 2 | 1 | Validate schema, units, timestamps, duplicates, missingness, range, and QC flags | Downloaded prepared files | Data-quality report; immutable source manifest and hashes |
| 3 | 1 | Standardize the prepared target and build causal features | Accepted prepared VTEC | Hourly target release; feature manifest; leakage-test report |
| 4 | 1 | Freeze chronological splits, embargo, comparison sets, metrics, and seeds | Target/feature release | Signed experiment configuration and locked-test guard |
| 5 | 1 | Fit baselines and tune learned models on training/validation only | Frozen folds and grid | Validation registry; selected hyperparameters; failed-run log |
| 6 | 1 | Refit, open the locked test once, and evaluate | Frozen protocol | Predictions hash; paired metrics and CIs; MVP decision report |
| 7 | Transition | Freeze the forecasting protocol | Complete Phase 1 evidence package | `phase_transition_manifest` and supervisor approval |
| 8 | 2 | Inventory and inspect raw files and metadata | Raw observations, station logs | Coverage/observable/cadence report; source hashes |
| 9 | 2 | Parse observations and compute calibrated STEC | Raw observations and frozen processor config | Arc-level calibrated STEC plus QC fields |
| 10 | 2 | Map STEC to VTEC and aggregate hourly | Valid STEC, geometry, mapping configuration | Candidate hourly VTEC plus support and uncertainty fields |
| 11 | 2 | Cross-validate and accept/reject the raw target | Candidate VTEC, prepared VTEC, GIM/second reference | Matched-timestamp error report, uncertainty budget, target acceptance decision |
| 12 | 2 | Retrain the **unchanged** TensorFlow/Keras model and all baselines | Accepted Phase 2 target and frozen model protocol | Phase 2 predictions and model artifacts |
| 13 | 2 | Compare phases and interpret | Both phase releases and predictions | Common-mask 2×2 cross-target analysis, limitations, final conclusion |

#### 3.6.2 Hard Boundary and Transition Rule

Phase 1 ends at the signed `phase_transition_manifest`. Before that signature, no Phase 1 code may derive TEC/VTEC from raw observations. Phase 2 begins with raw-file inventory and may not alter the Phase 1 forecasting protocol. The following freeze across phases: target cadence and forecast horizon, feature definitions and safe lags, history window, station representation, architecture, loss, optimizer policy, hyperparameter values, splits, embargo, baselines, metrics, seeds, masks, and statistical procedure. The **target-production lineage changes**, and—if the recommended Madrigal map product is approved—the physical target changes from location-sampled gridded VTEC in Phase 1 to receiver-derived IPP-median VTEC in Phase 2. That difference is a predeclared target-domain shift, not an equivalence. Any post-freeze model change is a separately labelled exploratory experiment and cannot replace the confirmatory cross-phase result.

Because both phases are restricted to 2022, Phase 2 reuses the December timestamps after Phase 1 has already reported them. The frozen protocol prevents performance-driven model changes, but Phase 2 is therefore a **fixed-protocol replication on a new target lineage, not a second statistically independent blind test**. This limitation must appear in the abstract-level interpretation. A genuinely independent confirmation requires a later untouched year or station set and is future work.

---

## 4. Scope and Non-Claims

### 4.1 In Scope

- One supervisor-approved prepared 2022 VTEC product sampled consistently for the ARUC, BSHM, and NICO coordinates in Phase 1, subject to the §6.1B source, coverage, and target-definition gates.
- ARUC, BSHM, and NICO raw station observations for Phase 2.
- GPS-only L1/L2 observations at 30-second cadence in Phase 2.
- An established GNSS package plus a transparent, unit-tested project calibration layer, with a frozen and verified configuration.
- Hourly station-level GNSS-derived VTEC defined as an IPP-median aggregate.
- One-hour-ahead causal forecasting as the confirmatory horizon.
- One pooled learned model family with station identity or verified station features.
- Persistence, 24-hour seasonal persistence, fitted station×month×hour climatology, ridge regression, Random Forest, and compact LSTM.
- IRI-2016 as an external benchmark; CODE final GIM as an external comparator.
- Availability-safe lagged VTEC, cyclical time, local solar time, station, and forecast-safe geomagnetic and solar features.
- Fixed chronological validation across F1–F4 and one locked December test.
- Station, regime, and observation-quality diagnostics.
- Paired vector time-block bootstrap uncertainty.
- A modular repository and reproducible research package.

### 4.2 Out of Scope

- Any extraction or calculation of TEC/VTEC from raw satellite files during Phase 1.
- Any IRI-derived value as a machine-learning input or target in the confirmatory experiment.
- Residual-correction modelling of the IRI–GNSS difference as a required deliverable.
- GRU, Transformer, attention, BiLSTM, GNN, or broad architecture searches.
- Galileo, GLONASS, or other non-GPS constellations in the primary product.
- A real-time production service.
- A full positioning-domain experiment.
- Claims of improved GNSS positioning accuracy.
- Claims for all of Iran, all regional stations, the whole named sector, or arbitrary locations.
- Multi-year or solar-cycle generalization.
- Multi-step operational forecasting as a required deliverable; +24 h is an optional post-completion extension only.
- Full GNSS-processing algorithm development from scratch, and large geodetic suites such as Bernese or GAMIT; Phase 2 integrates and verifies established components instead.
- Commercial validation, user-market validation, UI development, or deployment.

### 4.3 Future-Impact Language

The project **may support** later research on regional ionospheric monitoring, GNSS correction, or operational services. It does not prove operational readiness, commercial value, positioning benefit, or user demand.

### 4.4 Constraints

- One academic semester.
- Approximately 30 Kaggle GPU hours per week are **available but not required**. The full workflow shall be feasible on CPU; GPU is an accelerator, not a dependency.
- Approximately 10 GB storage.
- Up to one year of source data at three stations, approximately 26,000 hourly station rows before quality exclusions **only if the source-coverage gate passes**; actual counts must be reported, never assumed.
- Beginner-to-intermediate Python implementation capacity.
- Two execution platforms only: Kaggle (primary compute) and local (development and cross-check).

---

## 5. Research Questions, Hypotheses, and Success

### 5.1 Secondary Research Questions

1. Does the LSTM outperform persistence, 24-hour seasonal persistence, and fitted climatology under the same information and evaluation mask?
2. Does the LSTM outperform direct RF and ridge under the same information and evaluation mask?
3. Do forecast-safe space-weather features improve validation and locked-test performance beyond lagged VTEC and time features?
4. Is the model ranking consistent across the three stations?
5. Does model ranking differ between quiet and disturbed conditions?
6. Are large forecast errors associated with weak observational support or QC flags?
7. How sensitive is derived VTEC to the bounded preprocessing alternatives approved under the GNSS verification contract?
8. Does December skill depend on a day-of-year encoding that the model has seen only once (no-DOY ablation)?
9. How large is the IRI–GNSS discrepancy attributable to the documented topside/plasmaspheric and IPP-versus-zenith mismatches, as opposed to forecast skill?

### 5.2 Hypotheses

- **H1 — Primary:** The direct LSTM has a positive paired loss differential relative to the IRI-2016 benchmark on the locked test.
- **H2 — Secondary:** The direct LSTM has a lower paired loss than persistence, seasonal persistence, and fitted climatology.
- **H3 — Secondary:** The direct LSTM has a lower paired loss than direct RF and ridge.
- **H4 — Secondary:** Forecast-safe space-weather features improve disturbed-condition performance more than quiet-condition performance.
- **H5 — Secondary:** Pooled-model skill is not driven by only one station.
- **H6 — Evidence condition:** Any claimed improvement survives the defined vector time-block bootstrap and is not driven solely by a few extreme hours, as demonstrated by the top-1%-removed sensitivity.

Failure to confirm a hypothesis is a valid scientific result.

**Predeclaration for H4.** Before the G-05 freeze, the December regime and coverage audit permitted by Section 8.3 shall be completed. The supervisor-approved minimum is **frozen as of 2026-08-21 (D-13)**: H4 and secondary research question 5 remain confirmatory only if December 2022 contains **at least three independent storm events**, using §9.3's definitions unchanged — a storm event is a contiguous interval of \(Kp\ge5\), and two events are independent if separated by at least 24 hours of \(Kp<4\). With fewer than three, H4 and SRQ-5 are predeclared as **validation-fold-only** hypotheses and are reported as such. No separate disturbed-hour count is introduced: the threshold reuses the storm-event rule §9.3 already freezes, so H4's fate and the general storm-claim rule turn on the same measured quantity. This demotion is legitimate only if it is recorded before the freeze. Approved by the project owner under the recorded authority equivalence; change record `governance/CHANGE_RECORD_2026-08-21_freezes.md`. *[Amended in place 2026-08-21; effective version v4.3, issued 2026-08-21 — consistent with this document's revision table and with `CR-2026-08-21-FREEZES`, whose effective-version field records the same issuance. The former "not yet issued" wording is corrected 2026-08-22 per governance finding `UG-06`; no scientific content and no amendment history changed.]*

### 5.3 Three Success Layers

| Layer | Rule | Meaning |
|---|---|---|
| Project completion | Trusted target, required baselines/models, locked test, uncertainty analysis, reproducible artifacts, and honest conclusions are complete | The thesis work was performed correctly |
| Statistical evidence | The paired primary loss differential is positive and its 95% confidence interval excludes zero | Evidence favours the independent local LSTM over the IRI-2016 benchmark |
| Practical relevance | The improvement reaches a separately justified reference magnitude and is not smaller than the stated target uncertainty budget | The size may matter in practice |

A correct negative or inconclusive model result does not make the project a failure.

### 5.4 Practical-Improvement Reference

Ten percent RMSE reduction is a **named reference magnitude, not a pass/fail rule** and not a hypothesis. Practical relevance is reported descriptively unless the supervisor explicitly approves a threshold.

Two binding constraints apply:

1. The approved reference or threshold shall not correspond to an RMSE difference smaller than the **target uncertainty budget** of Section 6.9. If it does, practical relevance is reported descriptively only.
2. No threshold may be introduced, changed, or reinterpreted after December is opened.

### 5.5 Metrics

- **Confirmatory:** paired loss differential with 95% CI (Section 2.3).
- **Primary reported error metric:** RMSE.
- **Supporting:** MAE, median absolute error, mean error/bias, \(R^2\), correlation, and 90th/95th percentile absolute error.
- **Derived relative summary:** \(1-\mathrm{RMSE}_{model}/\mathrm{RMSE}_{reference}\).
- **Required breakdowns:** overall equal-station summary, time-weighted pooled summary, each station, quiet/disturbed regime, and observation-quality strata.

MAPE is excluded because it becomes unstable when VTEC is small.

---

## 6. Data Sources, Station Boundary, and Target Construction

### 6.1 Source Inventory

| Source | Role | Required provenance |
|---|---|---|
| **ICTP Calibrated GNSS TEC Service** | **Rejected Phase 1 candidate; retained only as acquisition and source-failure evidence** | Executed notebook, retrieval timestamp, station/date inventory, original filename, file size, checksum, archive hash, and failure decision |
| **MIT Haystack CEDAR Madrigal MAPGPS `gps` binned VTEC** | **Recommended Phase 1 replacement candidate; not approved until §6.1B passes** | Experiment/file permanent citation, instrument/kindat, selected parameters, station-coordinate-to-cell rule, dates, format, checksum, API version, and rules-of-the-road contact/acknowledgment |
| IONOLAB-TEC | Change-controlled alternative if Madrigal fails; coverage and access unverified | Account/access record, station identity, product definition, dates, cadence, files, checksums, citation and usage terms |
| GPS RINEX/CRX observations | Raw observational input | Provider, station, date, filename, checksum, retrieval date |
| Station logs | Coordinates and hardware history | Version/date and detected changes |
| GNSS package and DCB source | Derive station VTEC | Exact release/commit, configuration, dependency versions |
| IRI-2016 implementation | **External benchmark only** | Exact build/version, switches, inputs, altitude ceiling, units |
| CODE final GIM (IONEX) | **External comparator only** | Analysis center, product/version, interpolation rule |
| Space-weather indices | Exogenous features and regime labels | Provider, observation time, release status, retrieval time |

### 6.1A Phase 1 Prepared-VTEC Source Decision

The [ICTP Calibrated GNSS TEC Service](https://arplsrv.ictp.it/) was the initial station-product candidate. The approved `00_ictp_phase1_download_kaggle.ipynb` was executed and produced valid acquisition evidence, but the **source failed G-P1A**:

| Station | Directory result | Discovered | Accepted non-empty files | Unique 2022 days | Coverage |
|---|---:|---:|---:|---:|---:|
| ARUC | HTTP 200 | 28 | 27 | 27/365 | 7.397% |
| BSHM | HTTP 200 | 35 | 35 | 35/365 | 9.589% |
| NICO | HTTP 404 | 0 | 0 | 0/365 | 0.000% |

The ARUC day-278 file was rejected at zero bytes. The audit ZIP passed integrity, contained 66 members, and had a size of 41,180,233 bytes. Those results prove that the downloader worked; they do **not** make the dataset scientifically usable. The sparse and seasonally clustered ARUC/BSHM dates, absence of NICO, lack of adequate common-date coverage, and absence of December data cannot support the frozen January–November folds or locked December test. Therefore ICTP is rejected for Phase 1 training. Its notebook, ZIP, manifests, hashes, coverage summary, and console output remain in the evidence package under decision D-143.

The recommended replacement candidate is [MIT Haystack CEDAR Madrigal MAPGPS](https://www.haystack.mit.edu/geospace/geospace-projects/using-gnss-to-measure-ionospheric-tec/) using the prepared **`gps` binned VTEC** product. Published service metadata describe the standard product as 1° latitude × 1° longitude VTEC bins at 5-minute cadence and identify kind-of-data code 3500 for the binned product. Madrigal supports scriptable retrieval and permanent citations through its [official web-service API](https://github.com/MITHaystack/madrigalWeb). The Phase 1 release shall use only one experiment/product and one frozen extraction rule for all three coordinates.

Adoption remains conditional. Before download for training, the supervisor must approve: the exact experiment and kind-of-data identifier; returned VTEC parameter, units, and fill-value semantics; a deterministic cell-selection rule for each authoritative station coordinate; the hourly aggregation rule; and the coverage minimum. A target-independent audit must then verify readable 2022 data in all three selected cells, adequate common timestamps for F1–F4 and December, no unexplained product discontinuity, and compliant citation/acknowledgment. Exact files, requests, API/package version, permanent citations, parameters, coordinates, cell indices, and SHA-256 hashes are retained.

This replacement changes the Phase 1 target meaning. It is **location-sampled gridded VTEC**, not a receiver-specific station observation and not the Phase 2 IPP-median target. The target release shall carry a stable `target_definition_id`, cell center/bounds, cell-selection method, native cadence, and hourly aggregation identifier. Missing cells shall remain missing; spatial/temporal interpolation or mixing another provider into the confirmatory target is prohibited unless separately approved before performance is viewed. The larger `los` product is not selected because deriving VTEC from receiver/satellite line-of-sight observations would introduce Phase 2 processing into Phase 1.

IONOLAB-TEC is the preferred second-choice candidate because it may preserve a station-product interpretation, but authenticated access and exact 2022 ARUC/BSHM/NICO coverage must be verified. It is not an automatic fallback. A station/year scope change is the third option if neither single provider passes. No confirmatory training begins until one option is approved and passes §6.1B.

The [NASA CDDIS IGS Analysis-Center VTEC product](https://data.nasa.gov/dataset/global-navigation-satellite-system-gnss-igs-analysis-center-ac-ionosphere-vertical-total-e) is authoritative and complete as a global product, but it is not selected as the Phase 1 station target: its 2-hour, 5° longitude × 2.5° latitude grid is too coarse for a station-level claim and it is already conceptually close to the external GIM comparator.

### 6.1B Prepared-Data Acceptance Gate

Before Phase 1 training, the following pass/fail evidence is required for **each** station coordinate and its selected provider product/cell:

- a supervisor-approved provider, experiment/product identifier, target definition, access/usage record, acquisition program/notebook, archive or file SHA-256, request manifest, and retrieval timestamp;
- official four-character station-code match and coordinate cross-check;
- file/cell-level 2022 inventory with SHA-256 hashes, non-zero size, readable schema, UTC timestamps, units, cadence, fill values, and duplicate checks;
- a frozen and tested station-coordinate-to-cell rule when the product is gridded, with selected cell centers/bounds recorded;
- monthly counts of expected, present, readable, QC-valid, and hourly-valid samples;
- enough common-date coverage to support the frozen F1–F4 folds and untouched December test after the 24-hour history/embargo rules;
- no undocumented mixture of ICTP, Madrigal, GIM, or independently calculated VTEC within one confirmatory target;
- a single physical target definition across ARUC, BSHM, and NICO.

The numerical minimum for acceptable coverage is **frozen as of 2026-08-21: at least 90% usable hourly coverage per station per month, applied as a hard pass/fail gate, together with D-2's day rule (≥95% of calendar days present per month, 100% of December days).** This promotes §6.12's 90% hourly figure from an aspiration to a gate; §6.12's exception-plus-claim-limitation path no longer applies at G-P1A, and no coverage below 90% hourly is acceptable at this gate. Recorded as **D-12** in `evidence/DECISIONS.md`; approved by the project owner under the recorded student/supervisor authority equivalence; change record `governance/CHANGE_RECORD_2026-08-21_freezes.md`. Fixed before any model performance was viewed — no model, prediction or metric exists. *[Amended in place 2026-08-21; effective version v4.3, issued 2026-08-21 — consistent with this document's revision table and with `CR-2026-08-21-FREEZES`, whose effective-version field records the same issuance. The former "not yet issued" wording is corrected 2026-08-22 per governance finding `UG-06`; no scientific content and no amendment history changed.]* ICTP has failed this gate. Madrigal MAPGPS `gps` is the recommended replacement but must pass the gate independently; if it fails, the project must formally approve IONOLAB-TEC or a station/year redesign. Silent imputation, source mixing, retrospective split redesign after model performance is viewed, or treating a map value as station-observed VTEC is prohibited.

### 6.2 Station Registry and Geographic Claim Gate

Before full processing, the following table must be completed from authoritative station logs. Values must not be inferred from station names, from a single RINEX header, or from post-2022 coordinate solutions.

| Station | Geodetic coordinates | Geomagnetic coordinates (IGRF, pinned version) | Receiver/antenna/firmware history | 2022 coverage | Selection reason | Status |
|---|---|---|---|---|---|---|
| ARUC | Freeze gate | Freeze gate | Freeze gate | Audit required | Documented availability and study relevance | Open |
| BSHM | Freeze gate | Freeze gate | Freeze gate | Audit required | Documented availability and study relevance | Open |
| NICO | Freeze gate | Freeze gate | Freeze gate | Audit required | Documented availability and study relevance | Open |

Required registry contents: latitude, longitude, ellipsoidal height, DOMES or full station identifier, receiver/antenna/firmware intervals covering 2022, sampling interval, available observable codes, and any 2022 hardware change. Geomagnetic coordinates are computed with one pinned IGRF version.

Evidence sources are ranked: official site log first, RINEX headers as a cross-check, prior review tables as a cross-check only. A conflict must be resolved and recorded, never averaged or ignored. Receiver changes are treated as potential DCB discontinuities.

Monthly coverage is audited file by file. The evidence artifact is `station_registry_and_coverage_report`.

The thesis shall describe this as a bounded three-station study in the mid-latitude Eastern Mediterranean–South Caucasus sector, not a statistically representative regional sample.

### 6.3 Constellation, Observables, and Cadence

The primary VTEC product is **GPS-only**.

- Carrier phase: L1C and L2W.
- Code: C1C, C1W, C2W, subject to per-station availability.
- Cadence: 30 seconds. Higher-rate files are decimated to 30 s; days with a lower native cadence are flagged and rejected from the primary product.

GLONASS is excluded because its FDMA inter-frequency biases are channel-dependent and materially harder to calibrate. Galileo is excluded from the primary product and is permitted only as an optional post-completion sensitivity under Section 4.2 and the extension boundary of Section 14.

If the coverage audit shows GPS-only support is inadequate against the Section 6.6 thresholds, GPS+Galileo must be evaluated as an evidence-driven alternative before full-year processing, and the change recorded. The evidence artifact is `constellation_observable_cadence_report`.

### 6.4 GNSS Processing Strategy

The project shall use an established GNSS package for RINEX and STEC groundwork, plus a **transparent, unit-tested project calibration layer** implementing arc handling, levelling, DCB application, mapping, and aggregation. The project shall not implement the complete low-level GNSS-to-VTEC algorithm from scratch, and shall not adopt a large geodetic suite.

**Primary strategy:** `gnss-tec` plus a project calibration layer estimated at 300–500 lines.  
**Predeclared contingency:** an established self-calibrating processor such as TayAbsTEC or tec-suite, wrapped by project code, adopted only if the primary strategy fails its time-boxed trial by the frozen contingency date.  
**Cross-check only:** GPS-TEC (Seemala) on representative days. It is not a production path, because it is closed and platform-bound.

The trial is time-boxed to one week and must produce STEC/VTEC, a plausible diurnal curve, support fields, and one external comparison. The evidence artifact is `processor_trial_decision_report`.

Before full-year processing:

1. Select and freeze the package name, exact release or commit, dependencies, and machine-readable configuration.
2. Freeze the observable requirements, DCB source and sign convention, cycle-slip rules, arc rules, elevation cutoff, mapping function, shell height, satellite-level QC, and aggregation settings.
3. Select representative station-days by a documented rule before viewing comparison results.
4. Include ordinary conditions, data-quality difficulty, and a disturbed interval.
5. Independently inspect or reproduce important intermediate calculations on the selected samples, including one hand-calculated satellite pass.
6. Compare sample output with **two** external references, without optimizing the pipeline to force agreement.
7. Run the declared sensitivities of Section 6.5.
8. Define quantitative or supervisor-reviewed acceptance criteria before results are viewed.
9. Use the verified configuration unchanged for the full-year run.
10. Treat any later processing change as a new dataset release.

#### 6.4.1 DCB Product, Receiver Bias, and Sign Convention

**Primary:** published **satellite and receiver** biases, preferring CAS or DLR Bias-SINEX `.BSX`, or CODE monthly `.DCB`, provided all three stations have receiver entries. The exact file, version, hash, unit, and sign convention are pinned.

**Predeclared fallback:** if receiver entries are absent for any station, estimate receiver DCB per station-day by VTEC-dispersion minimization, disclose the estimated bias, and propagate its uncertainty into Section 6.9.

**Prohibited:** allowing an external tool to download and apply biases without a transparent, recorded convention.

Sign verification is mandatory and is not satisfied by visual plausibility. It requires: explicit unit conversion; one hand-calculated satellite pass carried from raw observables through biased and unbiased STEC; and a **reversed-sign negative control that must clearly fail**. The evidence artifact is `dcb_availability_and_sign_worked_example`.

Independent TEC algorithms are known to disagree by more than 10 TECU, so agreement with a single smooth-looking curve is not evidence.

### 6.5 Mapping, Shell, Cutoff, Slips, and Arcs

**This configuration is a deferred freeze gate. It shall not be guessed, and no value below may be treated as settled until the sensitivity evidence is produced.**

Recommended starting configuration, to be confirmed or revised by evidence:

| Setting | Recommended primary | Declared sensitivity |
|---|---|---|
| Mapping function | Modified single-layer model | — |
| Shell height | 450 km | 350 km |
| Elevation cutoff | 30° | 20° |
| Cycle-slip detection | Geometry-free + Melbourne–Wübbena | — |
| Slip handling | Restart arc | — |
| Minimum arc length | 20 min | 30 min |
| Levelling | Elevation-weighted phase-to-code | — |
| Hourly aggregation | Median | Mean; zenith-weighted (Section 6.6) |

Accepting the selected package's defaults without evidence is explicitly **not** an approved option.

The sensitivity run holds everything else fixed and compares bias and RMSE against two references, negative-value rate, within-hour spread, coverage, and diurnal smoothness. The decision rule is to adopt the strictest configuration whose reference disagreement is acceptable and whose support remains sufficient for Section 6.7. The evidence artifact is `gnss_processing_sensitivity_report`.

### 6.6 Hourly VTEC Target Contract

One target row represents one station and one UTC interval \([h,h+1)\), labeled by interval start \(h\).

**Phase 2 physical definition — binding.** The hourly receiver-derived target is the **median of valid VTEC values at the ionospheric pierce points observed from that station during that hour**. It is *not* the zenith VTEC column above the station coordinate. Within one hour the pierce points form a cloud extending hundreds of kilometres around the site. IRI and GIM are evaluated at the station coordinate, so every ML-versus-IRI and GNSS-versus-GIM comparison carries a documented spatial representativeness mismatch that must be stated wherever those comparisons are reported.

**Phase 1 prepared-target definition — conditional.** If Madrigal MAPGPS `gps` is approved, each nominal station row represents the frozen gridded VTEC cell selected from that station's authoritative coordinate, aggregated from the product's native cadence to the same UTC hourly interval. The exact cell-selection and hourly statistic are **frozen as of 2026-08-21, superseding this row's former "TBD — supervisor freeze gate" marker: the cell-selection rule is frozen by D-1 with its countersignature closed by the D-1 addendum, and the hourly statistic is frozen by D-16 as the median of the valid provider VTEC samples inside the UTC hour for the station's frozen cell.** Zenith-weighted aggregation is a separately declared sensitivity, authorised only before training and only if the data supports it; it is deferred as not computable, the audited Phase 1 product carrying five columns (`ut1_unix`, `gdlat`, `glon`, `tec`, `dtec`) with no elevation, zenith angle or satellite identifier, and nothing is substituted for the unavailable information. The Phase 1 target-row contract these produce is frozen by **D-17**. Recorded in `evidence/DECISIONS.md` as D-16, D-17 and the D-1 addendum; approved by the project owner under the recorded student/supervisor authority equivalence; change record `governance/CHANGE_RECORD_2026-08-21_freezes.md` § Addendum, which records all three as closed later the same day. *[Amended in place 2026-08-22 applying the 2026-08-21 approved records; effective version v4.3, issued 2026-08-21. No new scientific decision, aggregation rule or cell-selection criterion is introduced here.]* **Still open and not closed by this annotation:** this row's "Each row must retain exactly these fields" sentence remains in textual conflict with TE §6.1's Phase 2-shaped ten-field list — see `requirements.md` § Known defects row 10; D-17 governs the approved practical Phase 1 interpretation, and reconciling the two source texts runs through §15.2 change control. The row is labelled by station ID only as a stable location key; it must also retain the grid-cell coordinates/bounds and `target_definition_id`. It shall be described as *location-sampled gridded VTEC*, never receiver-derived station VTEC. Cross-phase results therefore test protocol transfer across a target-domain shift and do not establish numerical equivalence between targets.

The default aggregation statistic is the median, chosen for robustness against residual cycle slips. A **zenith-weighted aggregate is a declared sensitivity** under Section 6.5; adopting it as primary requires representative-day evidence and approval before model training. Fitting a local spatial field to recover a true station-zenith value is out of scope.

Each row must retain exactly these fields:

- station ID;
- UTC interval start;
- aggregated VTEC in TECU;
- valid observation count;
- valid satellite count;
- within-hour spread;
- largest internal gap;
- relevant processor/QC flags;
- aggregation configuration ID;
- target-valid indicator.

`within_hour_spread_tecu` is designated the **representativeness-uncertainty field** and must be reported, not merely stored.

### 6.7 Hourly Support Thresholds

Provisional fixed floors, subject to a mandatory audit before freezing:

| Threshold | Provisional value |
|---|---|
| Minimum distinct valid satellites | `n_sat ≥ 4` |
| Minimum valid observations | `n_obs ≥ 20` |
| Maximum largest internal gap | `≤ 20 min` |
| Spread limit | Retained as a flag; threshold to be set by audit |

Fixed common floors are preferred over station-specific percentile thresholds because they preserve cross-station comparability and pooled-mask coherence.

The audit uses January–November distributions of observation count, distinct satellites, largest gap, spread, and invalidity by station, month, and hour. It plots coverage and external-reference error by support bin. The decision rule is to choose the lowest common fixed floor that avoids clearly unreliable support without unacceptable or uneven coverage loss, with explicit attention to whether stricter floors preferentially delete storm hours. The evidence artifact is `target_support_threshold_report`.

Target values shall not be imputed for primary evaluation. Hours that fail the frozen target contract are excluded and documented.

### 6.8 Processor Verification Design

Six representative station-days are predeclared before any comparison result is viewed:

- two ordinary days, one near an equinox and one near a solstice;
- two poorest-support days from the training period;
- two highest-Kp days from the training period.

Verification uses **two external references with dependence audited**, preferably CODE GIM plus a station-level product such as IONOLAB-TEC, with GPS-TEC as an additional representative-day cross-check. ICTP cannot provide the required 2022 coverage. If Madrigal MAPGPS supplies the Phase 1 target, it may be used as a matched cross-target reference but is not an independent station-level truth. A single GIM comparison is insufficient because the GIM may ingest these very stations.

Tolerances are predeclared before results are viewed. Acceptance requires no unexplained negative VTEC, physically plausible curves, and biases and RMSE within tolerance against both references, or discrepancies fully resolved and documented. The evidence artifact is `gnss_processor_verification_report`.

### 6.9 Target Uncertainty Budget

A **target uncertainty budget** is a required artifact, produced from the Section 6.4 representative-day audit and the Section 6.5 sensitivities. Minimum contents:

- estimated carrier-to-code levelling error;
- receiver-DCB stability across a day, and estimation uncertainty if the Section 6.4.1 fallback is used;
- within-hour spread distribution as representativeness uncertainty;
- negative-VTEC incidence;
- the resulting stated uncertainty range in TECU;
- the spread between the two configurations tested in Section 6.5.

The budget must be reported next to the primary result. Section 5.4 is floored by it.

The budget must also state the following asymmetry honestly. Because all models are scored against the same target on the same mask, a slowly varying per-station-day bias inflates every model's absolute error roughly equally and partially cancels in the **paired difference**. It does not cancel in the derived percentage summary, because it inflates the reference denominator. The paired estimand of Section 2.3 is therefore the more robust quantity, which is one reason it is confirmatory.

### 6.10 GIM Role

GIM is an **external comparator**, never a forecasting input, never ground truth, and not presumed statistically independent.

If Madrigal binned VTEC is adopted as the Phase 1 target, the Phase 1 comparison with CODE GIM is explicitly a **map-product-to-map-product comparison**. It can measure agreement between products but cannot validate receiver-level station VTEC or serve as an independent target check. Phase 2 therefore still requires a second receiver/station-level reference if available, plus full network-overlap disclosure.

The product is CODE **final** IONEX. Interpolation is bilinear in space and linear in time between maps, with longitude-rotation correction. One sample interpolation must be hand-checked against the code.

The project must audit whether ARUC, BSHM, or NICO appear in the GIM input network and disclose any overlap as dependence. **No independence claim may be made before that audit.** GIM shall not be used to tune GNSS preprocessing and then be presented as independent validation. The evidence artifact is `gim_interpolation_and_independence_report`.

### 6.11 IRI-2016 Benchmark Configuration Gate

IRI-2016 is generated **solely as an external benchmark**. It is never an ML input, never an ML target, never a residual anchor, and never a component of any ML architecture.

Implementation: `iricore`, IRI-2016, with an **explicit 2000 km altitude ceiling** and forecast-safe drivers. Before generating the full benchmark, freeze:

- package/build and exact version or commit;
- all model switches and the topside option;
- the altitude ceiling, stated explicitly;
- coordinate, time, solar, and geomagnetic driver inputs, and confirmation that no driver is future-centered or unavailable at target time;
- units and output extraction;
- sample cases and expected values/tolerances.

Five to ten samples spanning sites, day and night, and quiet and disturbed conditions must be validated against the official IRI interface within a predeclared numeric tolerance, and the 26,000-call workload timed. The evidence artifact is `iri_implementation_validation_report`.

**Required disclosure.** GNSS-derived TEC extends farther into the plasmasphere than a 2000 km IRI ceiling. Reported IRI–GNSS discrepancies therefore contain a physical, structured, time-varying component that is not forecast error. This must be disclosed wherever the primary comparison is interpreted, and it is why the mandatory difficulty controls of Section 2.4 tier 2 exist.

### 6.12 Data Quality Criteria

- Units, coordinates, timestamps, sign conventions, and time zones are documented.
- Impossible or unexplained negative VTEC does not survive final QC.
- Cycle-slip, short-arc, low-elevation, DCB, and mapping behavior is recorded.
- Missingness and target support are summarized by station and month.
- At least 90% usable hourly coverage per station is an aspiration; any lower coverage requires an explicit supervisor-approved exception and claim limitation.
- GNSS, IRI, and GIM values remain separately derived, separately stored, and separately versioned.
- Representative-day processing verification passes before full-year generation.

### 6.13 Dataset Releases

Every immutable dataset release must record:

- dataset version and creation date;
- raw-source manifest and SHA-256 hashes;
- package and configuration version;
- schema and units;
- row counts by station, month, split, and QC stage;
- exclusions and QC summary;
- fold and mask identifiers;
- final file hashes.

Parent-release lineage chains are not required. The dataset used for final results shall never be silently overwritten.

---

## 7. Forecast Information and Feature Contract

### 7.1 The IRI-Free Information Boundary

**Binding architectural rule.** No IRI value, no IRI-derived residual, and no field computed from IRI may enter any machine-learning feature table, target, transformation, or inference path in the confirmatory experiment. The rule is enforced in code and by a test that must fail if any `iri_*` field or IRI-derived target reaches ML training or inference.

IRI values live in a separate benchmark table, joined only at evaluation time on the frozen comparison mask.

Any model that consumes IRI as a predictor is a **model-assisted** model, not an independent one. It may be built only as a sequential secondary extension after the primary experiment is complete and frozen (Section 14, Q-33 boundary), must carry a separate experiment ID, and is prohibited from using independent-outperformance language.

### 7.2 Forecast Time

At issue time \(t\), a forecast for \(t+1\) may use only information genuinely available by \(t\). Final historical values published later cannot be used in the primary forecasting track.

If an external feature's publication timing cannot be established, the feature must either use a conservative lag justified by its release process, be removed from the primary feature set, or be used only in a clearly labeled retrospective hindcast sensitivity.

### 7.3 Availability Matrix

Before feature construction, create a frozen matrix with:

| Field | Required content |
|---|---|
| Feature | Stable feature name |
| Meaning/unit | Scientific definition and unit |
| Source | Provider/product |
| Observation timestamp | Time represented by the value |
| Publication timestamp | Earliest time actually available |
| Cadence | Update frequency |
| Status | Provisional, forecast, or final |
| Safe lag | Minimum allowed lag at issue time |
| Missing rule | Exclude, carry-forward within limit, or other approved rule |
| Track | Forecast-safe primary or hindcast-only |

A test must assert that the actual applied lag is greater than or equal to the declared safe lag for every primary feature.

### 7.4 Frozen Feature Dictionary

Every input column must record its name, definition, unit, source, timestamp, allowed lag, transformation, normalization rule, missing-value rule, and forecast-time status.

The bounded families are:

- **Causal VTEC lags:** `[1, 2, 3, 24]` hours, plus the 24-step sequence for the LSTM.
- **Cyclical UTC time:** hour sine/cosine; day-of-year sine/cosine.
- **Local solar time:** \((UTC\ hour + longitude/15)\bmod 24\), sine/cosine encoded. Longitude enters the model **only** through local solar time.
- **Station representation:** station one-hot identity plus verified latitude.
- **Forecast-safe space weather**, per Section 7.5.
- **QC/support fields:** diagnostic-only by default; any model use requires explicit G-04 approval and is restricted to hours at or before \(t\).

Feature selection and scaling are fit using training data only. Random Forest importance scores are non-authoritative diagnostics and may never add, remove, or rank features into the production feature set.

### 7.5 Forecast-Safe Space-Weather Contract

| Index | Status | Safe lag / form |
|---|---|---|
| Kp, ap | Primary | Last **completed** 3-hour interval; lag ≥ 3 h |
| Hp60, ap60 | Primary | Lag ≥ 1 h; preferred over Kp alone because the cadence matches the hourly target |
| F10.7 (observed) | Primary | Lag 1 day |
| F10.7 81-day mean | Primary | **Trailing** mean only. The conventional centered 81-day mean uses future days and is prohibited. |
| Dst | **Diagnostic / hindcast-only** | Not a confirmatory primary feature |
| SSN | **Removed** | Not used |

Missing external values may be carried forward for at most 3 hours; beyond that the row is excluded. Final archived index values are not equivalent to contemporaneous operational values, and this distinction is what the safe lags encode. No result-driven feature selection is permitted.

### 7.6 Missing Inputs, Boundaries, and Scaling

- Do not impute primary targets.
- If \(y[t]\) is invalid, persistence produces no prediction and the row leaves that comparison mask.
- Exclude, and explicitly count, the first 24 hours of the series that lack sufficient causal history.
- Permit short input gaps only under the frozen causal carry-forward rule and flag them.
- Exclude windows with insufficient causal history.
- Never interpolate an input using observations after the forecast issue time.
- Fit all scalers, encoders, and imputers on the training partition of each fold only, and serialize them per fold.
- LSTM and ridge inputs are standardized; Random Forest inputs are unscaled. This is a family-specific *representation* of one shared information set, not a different information set.
- QC and support fields are diagnostic-only and restricted to hours at or before \(t\); target-hour quality fields are future information and are never forecast features.
- Report coverage changes after each exclusion or imputation stage.

---

## 8. Experiment Protocol

### 8.1 Dataset Grain, Horizon, and Windowing

The modeling table has one row per station per UTC hour, approximately 26,000 rows before exclusions. Each target timestamp belongs to exactly one partition.

- **Confirmatory horizon: +1 h.** This is the only horizon required for thesis completion.
- **+24 h is an optional extension** that may be attempted only after the minimum thesis is complete and frozen. It remains configurable in code but is outside the critical path, and no thesis claim depends on it.

**History window: 24 hours primary**, with a 48-hour sensitivity evaluated only after the primary configuration is frozen. A 24-hour embargo separates training from each validation window so a 24-hour input window cannot cross a boundary. History length is not a tuned hyperparameter.

### 8.2 Fixed Chronological Splits

| Fold | Training interval | Embargo | Validation interval |
|---|---|---|---|
| F1 | 1 January–31 March 2022 | 24 hours | April 2022 |
| F2 | 1 January–30 June 2022 | 24 hours | July 2022 |
| F3 | 1 January–30 September 2022 | 24 hours | October 2022 |
| **F4** | **1 January–31 October 2022** | **24 hours** | **November 2022** |
| Final refit | 1 January–30 November 2022 | Boundary protected by frozen manifest | — |
| Locked test | — | — | December 2022 only |

F4 is required because April, July, and October do not test a winter-like regime, and November is the closest available seasonal rehearsal for December.

- December 2022 is the **only locked test period**.
- November enters the final refit only after all features, hyperparameters, masks, seeds, thresholds, and analysis rules are frozen.
- Random or shuffled cross-validation is scientifically unacceptable for this time series and is prohibited.
- If coverage makes a stated fold invalid, dates may be adjusted only before tuning, using target-independent coverage evidence, with supervisor approval and a revised split manifest.
- No second storm holdout shall be selected from 2022 after results are observed.

### 8.3 Locked-Test Rules

- December target values may be audited for coverage and regime counts without inspecting model performance. This audit is **required** before G-05 (Section 5.2).
- Model selection, feature selection, thresholds, and hyperparameters use January–November only.
- Test predictions are generated **once**, hashed **before** any metric is computed, and written once.
- Locked-test access is recorded in the experiment registry with `locked_test_accessed = true`.
- Any test-driven change is labeled exploratory.

### 8.4 Required Models

| ID | Model | Role | Trained? |
|---|---|---|---|
| M-01 | Persistence, \(\hat y_{t+1}=y_t\) | Mandatory difficulty control | No |
| M-02 | 24-hour seasonal persistence, \(\hat y_{t+1}=y_{t-23}\) | Mandatory difficulty control | No |
| M-03 | Fitted station×month×hour climatology | Mandatory difficulty control | Yes, training folds only |
| M-04 | Ridge regression on the shared flattened feature matrix | Simple learned baseline | Yes |
| M-05 | Direct Random Forest | Secondary learned baseline | Yes |
| M-06 | Direct compact LSTM | **Primary learned model** | Yes |
| B-01 | IRI-2016 at \(t+1\) | **External benchmark; primary comparison reference** | No |
| C-01 | CODE final GIM at \(t+1\) | External comparator only | No |

M-03 is fitted on training partitions only and is never fitted using validation or December data.

**Removed from v2.0:** IRI-residual Random Forest, IRI-residual compact LSTM. **Closed:** the GRU gate.

**Model ID crosswalk from v2.0**

| v2.0 | v3.0 | Note |
|---|---|---|
| M-01 Persistence | M-01 | Role upgraded to mandatory difficulty control |
| M-02 Seasonal persistence | M-02 | Role upgraded to mandatory difficulty control |
| M-03 Ridge | M-04 | Renumbered |
| M-04 IRI-2016 | B-01 | Reclassified from baseline to primary comparison benchmark |
| M-05 Direct RF | M-05 | Unchanged |
| M-06 Direct LSTM | M-06 | Unchanged; now compared against B-01 as primary |
| M-07 Residual RF | — | Removed |
| M-08 Residual LSTM | — | Removed |
| — | M-03 Climatology | New |
| — | C-01 GIM | Formalised as comparator-only |

Ridge is required only if it reuses the shared feature and evaluation pipeline. If that reuse is technically impossible, removal requires an explicit change record.

### 8.5 Pooled Model Requirement

The learned models are pooled across all three stations and include station one-hot identity plus verified latitude. Pooling is required because a single station provides roughly 8,700 hourly rows, which is weak for a sequence model, whereas pooling provides roughly 26,000.

Performance must be reported separately for ARUC, BSHM, and NICO. Separate station-specific models are optional post-completion sensitivities, not required deliverables.

### 8.6 Frozen Hyperparameter Grids

Grids are exact, committed to configuration before G-05, and identical in structure across families. No broad automated architecture optimization is permitted, and no range may be changed after December is seen.

| Family | Grid | Combinations |
|---|---|---|
| Ridge | `alpha ∈ {0.01, 0.1, 1, 10, 100, 1000}` | 6 |
| Random Forest | `n_estimators ∈ {300, 600}` × `max_depth ∈ {8, 16, None}` × `min_samples_leaf ∈ {1, 5, 20}`, `max_features = sqrt` | 18 |
| LSTM | `layers ∈ {1, 2}` × `units ∈ {32, 64}` × `learning_rate ∈ {1e-3, 3e-4}` × `batch_size ∈ {64, 256}` | 16 |

Fixed LSTM training settings: dropout 0.2, Adam optimizer, MSE loss, maximum 100 epochs, early-stopping patience 10 epochs monitored on validation RMSE, minimum improvement tolerance 1e-4 TECU, best-checkpoint restoration rather than last epoch.

All families receive the same folds and the same eligible information for each matched comparison.

### 8.7 Tuning Criterion and Final Refit

Configurations are selected by the **mean per-fold skill score** across F1–F4:

\[
S = \frac{1}{4}\sum_{f=1}^{4}\left(1-\frac{\mathrm{RMSE}^{f}_{\mathrm{model}}}{\mathrm{RMSE}^{f}_{\mathrm{declared\ baseline}}}\right)
\]

Raw mean RMSE is not used, because it is naturally larger in high-TEC seasons and lets one fold dominate. Row-count weighting is not used, because it rewards easier data availability.

The declared baseline per track is named in configuration before tuning begins. Where mean skill differs by less than 1%, the simpler configuration is selected. The selected configuration is then refit on January–November **without changing any hyperparameter**. No December result may influence this criterion.

### 8.8 Randomness, Confirmatory Prediction, and Failed Runs

- Development seed: **42**, used for tuning only.
- Final seeds, predeclared: **{1337, 2024, 7}**.
- **The confirmatory prediction is the element-wise mean of the three final-seed predictions.** Selecting the best seed after seeing December, or selecting a seed on validation, is prohibited.
- Every seed's individual result is reported, plus mean and spread.
- Each seed is a separate registry run with its own checkpoint, predictions, and metrics.
- Failed and aborted runs are recorded with status and reason. Silent reruns are prohibited.
- Deterministic library settings are enabled where supported, and any remaining nondeterministic operation is named in the run manifest with its expected variation.

### 8.9 Common Information and Comparison-Wide Evaluation Masks

For every declared comparison **set**, availability is intersected across **all** included models **once**, producing a comparison-wide mask with a stable ID and recorded row counts. Pairwise or model-specific masks are prohibited, because they cause different models to sit different exams and make aggregate rankings incomparable.

For every comparison:

- models use the same eligible target timestamps;
- models use the same target values;
- matched learned models use the same allowed information set **and the same input window length and lag set**; the flattened matrix supplied to M-04 and M-05 is the flattened form of the identical causal window supplied to M-06;
- paired errors are calculated on the stored comparison-wide intersection;
- exclusions and row counts are reported;
- the comparison records a stable mask ID and feature-set ID;
- the IRI-free feature-denial check passes for every ML model in the set.

### 8.10 Required Ablations and Sensitivities

- Forecast-safe space-weather features versus no space-weather features.
- **No-DOY ablation**, testing whether December skill depends on a seasonal encoding seen only once in a one-year dataset.
- **Differenced-target ablation**, comparing raw TECU against first-difference targets. Raw TECU remains primary.
- 48-hour history sensitivity, after the primary configuration is frozen.
- Zenith-weighted aggregation sensitivity (Section 6.6).
- 48-hour bootstrap block sensitivity (Section 9.2).
- Top-1%-error-removed sensitivity (Section 9.5).
- Station-specific models are optional and cannot delay primary deliverables.

Ablations are sensitivity results. They may inform interpretation but can never replace the preregistered primary comparison after December.

---

## 9. Evaluation and Statistical Protocol

### 9.1 Weighting

The main cross-station summary uses **equal-station weighting**, so a station with more valid hours cannot decide the thesis. Time-weighted pooled results and per-station results are reported as required secondary views.

### 9.2 Vector Time-Block Bootstrap

The three stations share the same solar-driven ionosphere. Their errors are not three independent experiments, and resampling each station separately would produce confidence intervals that are too narrow.

For the primary and all major secondary comparisons:

- resample **24-hour blocks on the common timeline, carrying all three stations together as a vector**;
- use **10,000 replicates**;
- use fixed bootstrap seed **20221201**;
- combine station estimates with equal-station weighting;
- report 95% confidence intervals;
- repeat the main comparison with **48-hour blocks** as one sensitivity;
- **report the cross-station paired-error correlation** so the reader can judge how much dependence is present.

Independent within-station bootstraps and IID station-hour bootstraps are prohibited. Report effect sizes and confidence intervals, not only p-values.

### 9.3 Geomagnetic Regimes and Storm Events

- Quiet: \(Kp<4\).
- Disturbed: \(Kp\ge4\).
- Storm: \(Kp\ge5\).

Each three-hour Kp value maps to its corresponding hours. Hp60 is used where hourly resolution is preferable.

**Storm event rule, frozen before any model result is inspected:** a storm event is a contiguous interval of \(Kp\ge5\); two events are independent if separated by at least 24 hours of \(Kp<4\). The reporting window for each event is −12 h to +24 h around it.

December regime results are **descriptive**. They are not an additional confirmatory hypothesis, because the December storm sample is small and stratified percentages have unstable denominators. A general storm-performance claim requires at least three independent storm events in December; with fewer, storm results are descriptive case evidence only.

### 9.4 Observation-Quality Diagnostics

Without changing the training objective, report error against:

- valid satellite count;
- valid observation count;
- within-hour VTEC spread, explicitly interpreted as a spatial-temporal representativeness proxy;
- important processor/QC flags;
- station and month.

These diagnostics distinguish model failure from weak target support.

### 9.5 Required Results

- Primary paired loss differential with 95% CI, equal-station weighted.
- Derived percentage RMSE reduction, clearly labeled as derived.
- Mandatory tier-2 difficulty controls in the same table: LSTM versus persistence, seasonal persistence, and climatology.
- Time-weighted pooled summary.
- Per-station metrics and paired skill.
- Quiet/disturbed counts and metrics.
- Storm event count and appropriately bounded claims.
- Validation-fold performance across F1–F4.
- Three-seed LSTM stability, per seed plus mean and spread.
- Bootstrap intervals at 24 h and 48 h blocks, plus cross-station paired-error correlation.
- **Top-1%-absolute-error-removed sensitivity**, to show the result is not driven by a handful of extreme hours.
- Model and benchmark predictions for comparison-wide masks.
- Quality-stratified diagnostics.
- Feature and target ablation results.
- Target uncertainty budget, reported adjacent to the primary result.

---

## 10. Software and Repository Specification

### 10.1 Minimum Structure

The repository is deliberately simplified. Repository complexity is the largest schedule risk and directly competes with the high-risk GNSS verification work.

```text
configs/          # exactly four files
src/              # six domain packages
scripts/          # nine phase-aware stages plus one fixture orchestrator
tests/
notebooks/        # five: one acquisition notebook plus four analysis/review notebooks
artifacts/
```

Scientific choices belong in versioned configuration files, not scattered through notebooks or source code. Notebooks are for exploration and presentation; reusable processing, training, and evaluation logic belongs in modules.

### 10.2 Configuration Groups

Exactly four configuration files:

| File | Contents |
|---|---|
| `data.yaml` | Source inventory, station registry, constellation/observables/cadence, package and calibration settings, DCB source and sign, mapping/shell/cutoff/slip/arc settings, hourly target contract and support thresholds, IRI benchmark configuration and ceiling, GIM product and interpolation rule |
| `features.yaml` | Availability matrix, feature dictionary, safe lags, missing rules, transformations, IRI-free denial list |
| `experiment.yaml` | Splits and embargo, comparison sets and masks, model ladder, search grids, tuning criterion, metrics, weighting, bootstrap, regimes, storm-event rule |
| `seeds.yaml` | Development seed, three final seeds, bootstrap seed, deterministic flags |

Every unresolved field must be visibly marked `TBD — freeze gate`. No implementer or coding agent may fill such a field by convenience.

### 10.3 Experiment Registry

A CSV or JSONL registry shall record: run ID and timestamp, status, code commit, environment lock hash, platform, dataset version, fold and mask ID, feature-set ID, model ID, hyperparameters, seed, validation metric, artifact paths, `locked_test_accessed`, and notes. Failed and aborted runs remain visible.

### 10.4 Clean-Run Contract

A clean environment must be able to follow one documented ordered command sequence from a declared starting dataset and configuration to the required outputs, **on CPU**.

The contract records: environment lock, operating/runtime and hardware notes, input versions, commands, expected schema and row counts/ranges, required output files, numerical tolerances, expected runtime range, and known nondeterminism.

A container is **not** required. The container decision gate is closed. It may be revisited only if lock-based clean reproduction proves insufficient.

### 10.5 Required Reproducibility Artifacts

- dependency lock with exact pins;
- source and processed-data manifests;
- configuration snapshots;
- split, fold, mask, and feature-set manifests;
- experiment registry;
- model checkpoints;
- predictions, prediction hashes, and paired errors;
- metric/bootstrap outputs;
- figures and tables;
- tested reproduction guide.

Milestone artifacts are copied with a SHA-256 manifest. Parent-release lineage chains are not required.

---

## 11. Traceability

### 11.1 Stable IDs

| Type | Prefix | Example |
|---|---|---|
| Requirement | REQ | REQ-EVAL-01 |
| Decision | D | D-101 |
| Experiment | EXP | EXP-PRIMARY-01 |
| Test/check | TST | TST-LEAK-01 |
| Dataset | DATA | DATA-VTEC-2022-v1 |
| Feature set | FEAT | FEAT-SAFE-v1 |
| Evaluation mask | MASK | MASK-PRIMARY-v1 |
| Artifact/evidence | ART | ART-PRIMARY-METRICS |

### 11.2 Core Traceability Matrix

| Requirement | Decision | Experiment/check | Required evidence | Status |
|---|---|---|---|---|
| REQ-TARGET-01: trusted hourly GNSS VTEC | D-108, D-111 | TST-GNSS-VERIFY | Package config, sample checks, QC report | Freeze gate |
| REQ-IRIFREE-01: architecturally IRI-free ML inputs | D-101, D-102 | TST-IRI-DENIAL | Failing test on any `iri_*` field reaching ML | Defined |
| REQ-LEAK-01: forecast-safe inputs | D-116, D-119 | TST-AVAILABILITY | Availability matrix and lag assertions | Freeze gate |
| REQ-SPLIT-01: chronological selection | D-123 | TST-SPLIT | Hash-stable F1–F4 split manifest | Defined |
| REQ-PRIMARY-01: LSTM vs IRI benchmark | D-101, D-126 | EXP-PRIMARY-01 | Paired December predictions and metrics | Defined |
| REQ-CONTROL-01: mandatory difficulty controls co-reported | D-120 | EXP-CONTROL-01 | Primary table containing persistence/seasonal/climatology | Defined |
| REQ-FAIR-01: comparison-wide masks and matched windows | D-125 | TST-MASK | Mask manifests and row counts | Defined |
| REQ-UNC-01: dependent uncertainty | D-127 | EXP-BOOT-01 | 24 h and 48 h vector bootstrap outputs, cross-station correlation | Defined |
| REQ-STATION-01: bounded pooled study | D-105, D-104 | EXP-STATION-01 | Station registry and per-station metrics | Freeze gate |
| REQ-BENCH-01: reproducible IRI benchmark | D-114 | TST-IRI-01 | Config, ceiling, driver safety, sample validation | Freeze gate |
| REQ-TUNC-01: target uncertainty budget | D-111, D-109 | ART-TARGET-UNC | Budget artifact adjacent to primary result | Freeze gate |
| REQ-REPRO-01: clean rerun | D-129, D-130 | TST-CLEAN-01 | Clean-run log and dataset hashes | Defined |
| REQ-AGENT-01: human-owned scientific freezes | D-132 | TST-PREFLIGHT | Preflight report with zero TBD in required fields | Freeze gate |
| REQ-CLAIM-01: bounded claims | D-104, D-128 | TST-CLAIMS-01 | Final claims checklist | Defined |

The implementation shall expand this matrix rather than invent a separate traceability system.

---

## 12. Canonical RAID Register

This is the only authoritative RAID register. Other sections may summarize it but must link back here.

### 12.1 Risks

| ID | Risk | Probability | Impact | Trigger | Response | Owner | Due/status | Residual risk |
|---|---|---:|---:|---|---|---|---|---|
| R-01 | RINEX/CRX cannot be parsed reliably | Medium | High | Sample failure or missing observables | Test versions early; pre-decompression/second parser | Student | Before target gate — Open | Medium |
| R-02 | DCB sign or magnitude biases VTEC | High | High | Large offsets or implausible VTEC | Published receiver DCBs; hand-worked pass; reversed-sign negative control | Student/Supervisor | Before full-year processing — Open | Medium |
| R-03 | Mapping/elevation choices bias VTEC | Medium | High | Elevation-dependent residuals | Deferred freeze with declared 450/350 km and 30°/20° sensitivities | Student | Before target freeze — Open | Medium |
| R-04 | Cycle slips or short arcs contaminate targets | Medium | High | Abrupt jumps/heavy tails | GF+MW detection, arc restart, ≥20 min arcs, median aggregation | Student | Before target freeze — Open | Medium |
| R-05 | Hourly target has weak support | Medium | Medium | Few satellites/observations | Support thresholds after audit; quality diagnostics | Student | Before target freeze — Open | Low–Medium |
| R-06 | Coordinate/time mismatch | Low–Medium | High | Systematic phase shift | Unit tests and sample cross-checks; pinned IGRF | Student | Walking skeleton — Open | Low |
| R-07 | GIM interpolation is wrong | Medium | High | Discontinuity or implausible values | Hand-check one sample; longitude-rotation correction | Student | Walking skeleton — Open | Low–Medium |
| R-08 | IRI benchmark setup differs from intended | Medium | High | Sample disagreement | Pin `iricore`/IRI-2016/2000 km ceiling; validate 5–10 samples | Student/Supervisor | Before benchmark run — Open | Low–Medium |
| R-09 | External features leak future values | Medium | High | Final or centered index used | Availability matrix; trailing F10.7 mean; lag assertions | Student/Supervisor | Before feature freeze — Open | Low |
| R-10 | Temporal leakage crosses partitions | Low after controls | High | Overlapping windows or all-data scaling | Split/embargo tests; train-only transforms | Student | Before tuning — Open | Low |
| R-11 | IRI contamination of the ML pipeline | Medium | **Critical** | Any `iri_*` field or IRI-derived target in ML input | Architectural separation plus a failing denial test | Student | Before feature freeze — Open | Low |
| R-12 | LSTM overfits one year | High | Medium | Training improves while validation worsens | Compact frozen grid, early stopping, F4, no-DOY ablation | Student | During validation — Open | Medium |
| R-13 | December has too few storm or disturbed hours | Medium | High for regime claims | Fewer than three independent events, or few Kp≥4 hours | Pre-freeze December regime audit; predeclared H4 demotion; descriptive reporting | Supervisor | **Before G-05** — Open | Low |
| R-14 | Aggregate gain is driven by one station | Medium | High | Per-station failure | Equal-station and per-station reporting | Student | Final analysis — Open | Medium |
| R-15 | Improvement is statistically unstable | Medium | High | CI includes zero | Report inconclusive result | Student | Final analysis — Open | Low |
| R-16 | Beating a climatological benchmark is mistaken for forecast skill | **High** | **High** | LSTM beats IRI but not persistence or climatology | Mandatory tier-2 controls in the primary table; binding honesty rule (§2.4) | Student/Supervisor | Final analysis — Open | Low |
| R-17 | Target uncertainty exceeds the claimed effect | Medium | High | Budget range ≥ claimed RMSE difference | Target uncertainty budget; Section 5.4 floor | Student/Supervisor | Before claims — Open | Medium |
| R-18 | Practical reference encourages test tuning | Medium | High | Repeated post-test changes | 10% is a named reference, not pass/fail; locked test | Supervisor | Before test — Open | Low |
| R-19 | Scope expands to advanced models or constellations | Medium | Medium | Core pipeline delay | Enforce out-of-scope list and extension boundary | Supervisor | Continuous — Open | Low |
| R-20 | Positioning or geographic benefit is overstated | Medium | High | Unsupported thesis language | Claims checklist; sector name is descriptive only | Student/Supervisor | Before submission — Open | Low |
| R-21 | Clean-run reproduction fails | Medium | Medium | Hidden path/manual step | Modular scripts, exact pins, CPU clean-run test | Student | Before final reporting — Open | Low–Medium |
| R-22 | Coding agent invents a scientific constant | Medium | **Critical** | Any required config field silently filled | Hard preflight; zero-TBD check; forbidden-choice list | Student/Supervisor | Before implementation — Open | Low |
| R-23 | ICTP prepared VTEC is incomplete for the 2022 three-location protocol | **Realized** | **Critical for Phase 1 protocol** | ARUC 27/365 days; BSHM 35/365; NICO 0/365 (HTTP 404); no locked-test support | ICTP rejected for training; retain audit evidence; approve and audit one replacement under §6.1B | Student/Supervisor | Closed as realized source failure — D-143 | None if ICTP is not used |
| R-24 | Phase 1 and Phase 2 targets have different physical definitions or masks | Medium | High | Coordinate/IPP, cadence, aggregation, or timestamp mismatch | Freeze target contract; matched-timestamp processor validation; 2×2 cross-target evaluation | Student/Supervisor | Before Phase 2 retraining — Open | Low–Medium |
| R-25 | Framework change is mistaken for a data-pipeline effect | Low after controls | High | Different NN library or model code used in Phase 2 | One TensorFlow/Keras implementation and checkpoint contract across both phases | Student | Continuous — Open | Low |
| R-26 | Copied research code violates license or obscures original contribution | Medium | High | Missing notice, commit, citation, modification log, or incompatible copyleft | Source-reuse register, isolated adapter, preserved notices, license compatibility review and tests | Student/Supervisor | Before code is copied — Open | Low–Medium |
| R-27 | Phase 2 reuses December after Phase 1 exposes the period | Certain by design | Medium–High | Phase 2 is described as a second independent test | Freeze the full forecasting protocol; prohibit model changes; label Phase 2 a fixed-protocol target-lineage replication; require a future untouched-year validation for independent confirmation | Student/Supervisor | Final claims — Open | Medium |
| R-28 | Kaggle acquisition fails, is interrupted, or is mistaken for data validation | Medium | High | Network-disabled notebook, partial ZIP, missing manifest, or training begins immediately after download | Require ZIP integrity, per-file hashes, retained executed notebook, rerunnable standalone script, and the independent §6.1B gate | Student | Phase 1 acquisition — Open | Low–Medium |
| R-29 | Recommended Madrigal Phase 1 product has missing cells, unsuitable schema, or is mistaken for receiver-derived station VTEC | Medium | **Critical for Phase 1 protocol and claims** | §6.1B audit fails, selected cells lack common 2022/December timestamps, or thesis labels grid values as station observations | Require supervisor approval, exact experiment/kindat/schema and cell audit, frozen `target_definition_id`, no imputation/source mixing, and explicit target-domain-shift reporting | Student/Supervisor | Before replacement adoption — Open | Medium |

### 12.2 Assumptions, Issues, and Dependencies

| ID | Type | Item | Validation/control | Owner | Due/status |
|---|---|---|---|---|---|
| A-01 | Assumption | Three stations have usable dual-frequency GPS 2022 coverage | Monthly coverage matrix | Student | Before package freeze — Open |
| A-02 | Assumption | Station metadata is stable and knowable from official logs | Inspect authoritative logs | Student | Before full parsing — Open |
| A-03 | Assumption | Published receiver DCBs exist for all three stations | Check CAS/DLR `.BSX` and CODE `.DCB` | Student | Before target freeze — Open |
| A-04 | Assumption | IRI and GIM cover all eligible timestamps | Walking skeleton | Student | Before dataset freeze — Open |
| A-05 | Assumption | Space-weather publication times can be established | Availability matrix | Student | Before feature freeze — Open |
| A-06 | Assumption | Hourly IPP median is scientifically acceptable | Representative-day audit; supervisor approval | Student/Supervisor | Before target freeze — Open |
| A-07 | Assumption | CPU is sufficient for the full workflow | Environment and CPU preflight benchmark | Student | Before full run — Open |
| I-01 | Issue | GNSS package trial not yet run | Time-boxed one-week trial with contingency date | Student/Supervisor | Open |
| I-02 | Issue | Hourly support thresholds not yet measured | Jan–Nov support audit | Student/Supervisor | Open |
| I-03 | Issue | Station metadata table is incomplete | Complete station registry | Student | Open |
| I-04 | Issue | Mapping/shell/cutoff/arc configuration deliberately deferred | Run declared sensitivities | Student/Supervisor | Open |
| I-05 | Issue | Practical-relevance policy needs supervisor confirmation | Confirm 10% is a reference, not a test | Supervisor | Open |
| I-06 | Issue | Supervisor has not yet confirmed the IRI-benchmark-only role | Present clarified question and IRI role statement | Supervisor | Open |
| I-07 | Issue | +24 h scope decision not yet confirmed | Present run-count estimate | Supervisor | Open |
| DEP-01 | Dependency | RINEX archive and station logs | Immutable cache and checksums | Student | Active |
| DEP-02 | Dependency | `gnss-tec` and DCB products | Pin exact version/source | Student | Open |
| DEP-03 | Dependency | CODE final IONEX | Cache exact product/version | Student | Open |
| DEP-04 | Dependency | `iricore` / IRI-2016 | Pin and validate against official interface | Student/Supervisor | Open |
| DEP-05 | Dependency | Space-weather products including Hp60 | Archive raw values and metadata | Student | Open |
| DEP-06 | Dependency | Kaggle and local Python 3.11 environment | Exact pins; CPU path proven | Student | Open |
| DEP-07 | Dependency | Second receiver/station-level TEC reference for Phase 2 verification | Confirm IONOLAB-TEC or equivalent; ICTP lacks coverage and Madrigal gridded VTEC is cross-target evidence rather than receiver-level truth | Student | Open |
| DEP-08 | Dependency | Scientific approvals | Gate table and evidence links | Supervisor | Open |
| DEP-09 | Dependency | ICTP prepared TEC/VTEC access and usable common-date 2022 coverage for ARUC, BSHM, NICO | Executed notebook, archive/manifests and failure decision | Student | Closed — failed G-P1A; D-143 |
| DEP-10 | Dependency | TensorFlow/Keras Python 3.11-compatible pinned environment | Install and deterministic CPU/GPU fixture test | Student | Before Phase 1 tuning — Open |
| DEP-11 | Dependency | External code licenses and citations | Source-reuse register and license review | Student/Supervisor | Before copying — Open |
| DEP-12 | Dependency | Kaggle Internet access and sufficient `/kaggle/working` storage for ICTP acquisition audit | Retain executed notebook, run metadata, archive hash and output manifest | Student | Completed for source audit; source itself failed |
| DEP-13 | Dependency | Supervisor approval, API access, exact 2022 schema, and common-cell coverage for the Madrigal MAPGPS `gps` candidate | Freeze experiment/kindat/parameters/cell rule; run target-independent file/cell/month audit and preserve permanent citations | Student/Supervisor | Phase 1 replacement gate — Open |

---

## 13. Readiness Gates and Walking Skeleton

### 13.1 Gate Ownership

| Gate | Student responsibility | Approver | Required evidence | Due | Status |
|---|---|---|---|---|---|
| G-01 Scientific framing | Prepare final question, IRI-role statement, hierarchy, claims, horizon scope | Supervisor | Sections 2, 4, 5 and decision log | Before implementation freeze | Pending sign-off |
| G-02 Station/data viability | Audit site logs, headers, coverage, observables, cadence | Supervisor consulted | `station_registry_and_coverage_report`, `constellation_observable_cadence_report` | Before package freeze | Open |
| G-03 GNSS target | Trial and configure package; verify DCB sign; run sensitivities | Supervisor | `processor_trial_decision_report`, `dcb_availability_and_sign_worked_example`, `gnss_processing_sensitivity_report`, `gnss_processor_verification_report`, `target_support_threshold_report`, target uncertainty budget | Before full-year processing | Open |
| G-04 Feature safety | Build availability matrix and dictionary; prove IRI-free contract | Supervisor for ambiguous inputs | Leakage checks, lag assertions, IRI-denial test, feature manifest | Before model tuning | Open |
| G-05 Experiment freeze | Freeze folds, masks, grids, seeds, estimand, bootstrap, regimes, storm rule; complete December regime audit | Supervisor | Signed config bundle, traceability table, **December regime-count audit report** | Before December access | Open |
| G-06 Locked evaluation | Execute write-once, hash-before-metrics December run | Student | Registry entry, prediction hash, metrics, artifact hashes | After G-05 | Blocked |
| G-07 Reproducibility | Perform CPU clean run | Supervisor/reviewer | `environment_and_cpu_preflight_report`, clean-run log, matched artifacts | Before thesis submission | Blocked |
| G-08 Claims | Match conclusions to evidence | Supervisor | Claims checklist, limitations, target uncertainty budget | Before thesis submission | Blocked |
| **G-09 Agent preflight** | Complete all P0 freezes; run automated zero-TBD check | Supervisor | `aws_ai_dlc_preflight_report` | Before any affected component is coded | Open |
| **G-P1 Prepared-data MVP** | Preserve the failed ICTP audit; obtain approval and audit one replacement provider/product; complete the Phase 1 locked evaluation only after G-P1A passes | Supervisor | ICTP rejection evidence; replacement approval; prepared-source manifest, cell/day/month coverage matrix, target-definition record, quality report, predictions hash, paired results and MVP decision | Before the phase transition | **Blocked — ICTP failed; replacement pending** |
| **G-P2 Phase transition** | Freeze the complete forecasting protocol and approve raw-pipeline work | Supervisor | Signed `phase_transition_manifest`, Phase 1 evidence package, source-reuse register | Before Phase 2 raw processing | Blocked |
| **G-P3 Raw-target acceptance** | Validate independently produced Phase 2 VTEC before retraining | Supervisor | Processor tests, two-reference matched comparison, target uncertainty budget, coverage/mask report | Before Phase 2 model training | Blocked |

### 13.2 Two-Stage Walking Skeleton

A seven-day software demo proves that files connect but cannot expose monthly DCB, arc, IRI, or seasonal problems. Two fixtures are therefore required.

**Fixture 1 — seven-day plumbing fixture.** One station, seven contiguous UTC days, provisionally NICO in March 2022 subject to coverage. Selected before viewing any model performance, using a documented target-independent coverage rule.

**Fixture 2 — one-month scientific fixture.** One full calendar month outside December, all three stations, exercising monthly bias products, IRI generation over a realistic span, missingness patterns, support distributions, and pooled masks.

**Binding limitation.** The seven-day LSTM result is a smoke test and is explicitly **not** scientific evidence.

Each fixture manifest must define: fixture ID, station(s), exact UTC dates, selection rule, creator, approval status; exact input files with SHA-256; package name/version and full config ID; expected schema at every stage; units; row-count ranges; support and missingness limits; timestamp tolerances; independent reference checks including sample IRI and GIM values; required outputs; expected runtime; and permitted numerical variation.

The evidence artifact is `walking_skeleton_acceptance_report`.

### 13.3 Walking-Skeleton Pass/Fail Checks

- [ ] CRX/RINEX parse matches the fixture manifest.
- [ ] Package version and full configuration are captured.
- [ ] DCB sign worked example passes and the reversed-sign control fails.
- [ ] Hourly VTEC and all support/QC columns match schema and tolerances.
- [ ] Important intermediate calculations pass independent checks.
- [ ] Two external references are generated without forced agreement.
- [ ] IRI benchmark and GIM comparator sample alignment passes.
- [ ] The IRI-free denial test fails when an `iri_*` field is deliberately injected.
- [ ] Availability lag assertions pass for every primary feature.
- [ ] Persistence, seasonal persistence, climatology, ridge, and RF predictions run.
- [ ] A minimal direct LSTM trains and restores its lowest-validation-RMSE checkpoint.
- [ ] A chronological mini-split produces comparison-wide-mask metrics with no boundary leakage.
- [ ] Vector block bootstrap reproduces from the fixed seed.
- [ ] Required prediction, residual, target-support, and quality plots exist.
- [ ] A clean CPU runtime reproduces both fixtures within declared tolerances.

Every item must link to machine-readable or reviewable evidence. Visual inspection alone is insufficient. Acceptance occurs only when all rows pass, evidence targets exist, hashes match, and no failure is waived informally.

---

## 14. Decision Log

Decisions D-000 through D-036 were adopted in v2.0. Those that conflict with the questionnaire are marked superseded below. Decisions D-101 through D-133 implement questionnaire answers Q-01 through Q-33. "Approved" means adopted into this project specification; academic gate approval remains governed by Section 13.

### 14.1 Superseded v2.0 Decisions

| v2.0 ID | Original content | Status in v3.0 | Superseded by |
|---|---|---|---|
| D-001 | Direct LSTM versus persistence is the sole primary comparison | **Superseded** | D-101, D-120 |
| D-003 | Three fixed folds and one locked December test | **Amended** | D-123 (four folds) |
| D-013 | Bounded fair tuning budgets, 20 trials | **Superseded** | D-121 (exact grids) |
| D-015 | One development seed and three predeclared final seeds | **Amended** | D-122 (three-seed mean is confirmatory) |
| D-017 | Paired moving-block bootstrap, within station | **Superseded** | D-127 (vector bootstrap) |
| D-020 | Pin and verify one IRI-2016 implementation as baseline and residual anchor | **Amended** | D-114 (benchmark only) |
| D-024 | Add one ridge baseline | Retained | — |
| D-026 | Bounded target-quality error diagnostics | Retained and strengthened | D-111 |
| All others (D-000, D-002, D-004–D-012, D-014, D-016, D-018, D-019, D-021–D-023, D-025, D-027–D-036) | — | Retained | — |

### 14.2 Questionnaire Decisions

| ID | Question | Adopted decision | Status |
|---|---|---|---|
| D-101 | Q-01 | Independent local ML is the primary story; IRI is an external benchmark only, never an input, target, residual component, or architectural element | Approved — supervisor confirmation pending |
| D-102 | Q-02 | Hard IRI exclusion from every ML feature and target, enforced by a failing test; an IRI-feature model is permitted only as a sequential, separately labeled model-assisted extension after the primary results are frozen | Approved |
| D-103 | Q-03 | +1 h is the required confirmatory horizon; +24 h is an optional extension after minimum thesis completion, configurable but off the critical path | Approved — supervisor scope confirmation pending |
| D-104 | Q-04 | Name the mid-latitude Eastern Mediterranean–South Caucasus sector descriptively; bound all inference to the three stations, 2022, and declared horizons | Approved |
| D-105 | Q-05 | Retain ARUC, BSHM, NICO for 2022 with pooled primary models and station identity; per-station results are mandatory diagnostics | Approved |
| D-106 | Q-06 | Freeze the station registry from official site logs plus a monthly coverage audit and pinned IGRF; headers and prior tables are cross-checks only | Approved — audit required |
| D-107 | Q-07 | GPS-only L1/L2 at 30 s; GLONASS excluded for FDMA bias risk; Galileo only as an optional later sensitivity | Approved — coverage evidence gate remains |
| D-108 | Q-08 | `gnss-tec` plus a transparent 300–500 line project calibration layer; TayAbsTEC/tec-suite as a dated contingency; GPS-TEC as a representative-day cross-check only | Approved — time-boxed trial required |
| D-109 | Q-09 | Published satellite **and receiver** DCBs with a hand-verified sign and a reversed-sign negative control; per-station-day estimation is the predeclared fallback | Approved — verification required |
| D-110 | Q-10 | Mapping, shell, cutoff, slip, arc, and levelling configuration is **deferred to Type C evidence**; the 450 km/30°/20 min configuration is the recommendation, and processor defaults are explicitly rejected | **Deferred — experiment-dependent** |
| D-111 | Q-11 | The target is the hourly median over valid IPP VTEC, explicitly not station-zenith VTEC; within-hour spread is the representativeness-uncertainty field; zenith weighting is a declared sensitivity | Approved — supervisor approval and sensitivity required |
| D-112 | Q-12 | Provisional fixed floors `n_sat ≥ 4`, `n_obs ≥ 20`, gap `≤ 20 min`, frozen only after the Jan–Nov support audit | Approved — audit required |
| D-113 | Q-13 | Six predeclared station-days spanning ordinary, poorest-support, and highest-Kp conditions, verified against two independent references | Approved |
| D-114 | Q-14 | `iricore`, IRI-2016, explicit 2000 km ceiling, forecast-safe drivers, validated against the official interface on 5–10 samples; topside/plasmasphere mismatch disclosed | Approved — validation experiment required |
| D-115 | Q-15 | CODE final IONEX with bilinear-space and linear-time interpolation, longitude-rotation correction, hand-checked sample, and mandatory network-overlap disclosure | Approved — audit required |
| D-116 | Q-16 | Forecast-safe index contract: Kp/ap lag ≥3 h, Hp60/ap60 lag ≥1 h, observed F10.7 lag 1 day, trailing 81-day mean, Dst diagnostic-only, SSN removed, carry-forward ≤3 h | Approved |
| D-117 | Q-17 | 24 h primary history with lags `[1,2,3,24]` and 24-step sequences; 48 h is a post-freeze sensitivity; IRI excluded from every ML input | Approved |
| D-118 | Q-18 | Raw TECU primary target with required no-DOY and differenced-target ablations; longitude acts only through local solar time | Approved — ablations required |
| D-119 | Q-19 | Strict common rules for missingness, boundaries, train-only scaling, family-specific representation, and diagnostic-only QC fields | Approved |
| D-120 | Q-20 | Focused ladder: persistence, seasonal persistence, fitted climatology, ridge, direct RF, compact direct LSTM, IRI benchmark, GIM comparator; residual RF/LSTM and GRU removed; difficulty controls are mandatory and co-reported | Approved |
| D-121 | Q-21 | Exact frozen grids: ridge 6, RF 18, LSTM 16 combinations, with fixed training settings | Approved |
| D-122 | Q-22 | Development seed 42; final seeds {1337, 2024, 7}; the confirmatory prediction is the element-wise three-seed mean; failed runs recorded, never silently rerun | **Approved; supervisor sign-off closed 2026-08-22** by the project owner under the recorded student/supervisor authority equivalence (`CR-2026-08-22-TE-AMEND`; `GOV-2026-08-22-REM-01` Rec 4). No supervisor signature artifact exists and none is claimed. Seed values unchanged — verified against this row and TE §12's `configs/seeds.yaml` description before closure |
| D-123 | Q-23 | F1–F4 expanding chronological windows with 24 h embargo, adding November validation; final refit Jan–Nov; December remains the only locked test | Approved |
| D-124 | Q-24 | Select on mean per-fold skill versus a declared baseline across F1–F4; prefer the simpler configuration within 1%; refit without changing hyperparameters | Approved |
| D-125 | Q-25 | Stored comparison-wide intersection masks, IRI-free feature denial, one hashed December prediction release, registry access flag | Approved |
| D-126 | Q-26 | Paired loss differential with 95% CI is confirmatory; percentage reduction is derived; equal-station weighting primary, time-weighted and per-station secondary; MAPE excluded | Approved — supervisor sign-off pending |
| D-127 | Q-27 | Vector time-block bootstrap carrying all three stations together, 24 h blocks, 10,000 replicates, seed 20221201, 48 h sensitivity, cross-station correlation reported | Approved |
| D-128 | Q-28 | Descriptive December strata; frozen storm-event rule; top-1%-removed sensitivity; 10% is a named reference, not pass/fail | Approved — supervisor sign-off pending |
| D-129 | Q-29 | Python 3.11 with exact pins and per-run freeze; Kaggle plus local only; CPU sufficient; Colab, Drive, and the container gate closed | Approved — CPU benchmark required |
| D-130 | Q-30 | Simplified repository: four configs, six packages, seven scripts, four notebooks, focused tests, concise manifest, registry; critical NFRs only | Approved in v3; exact script count superseded by D-135 and notebook count superseded by D-142 |
| D-131 | Q-31 | Two-stage skeleton: seven-day plumbing fixture plus one-month scientific fixture; seven-day LSTM output is not evidence | Approved — fixture selection from coverage required |
| D-132 | Q-32 | Hard preflight with human-owned freezes; the agent implements configs, contracts, and tests only, and may never choose a scientific value or change one after seeing results | Approved — preflight required |
| D-133 | Q-33 | No extension until the recommended scope is complete and frozen; ordered priority: IRI-feature extension, 48 h history, GPS+Galileo, per-station models, additional years/stations | Approved |

### 14.3 Freeze-Gate Closure Crosswalk

| Original gate | Closed by |
|---|---|
| TQ-01 | D-108 (Q-08) |
| TQ-02 | D-109 (Q-09) |
| TQ-03 | D-107, D-110 (Q-07, Q-10) |
| TQ-04 | D-113 (Q-13) |
| TQ-05 | D-131 (Q-31) |
| TQ-06 | D-112 (Q-12) |
| TQ-07 | D-106 (Q-06) |
| TQ-08 | D-114 (Q-14) |
| TQ-09 | D-115 (Q-15) |
| TQ-10 | D-116 (Q-16) |
| TQ-11 | D-127 (Q-27) |
| TQ-12–TQ-15 | D-121, D-122 (Q-21, Q-22) |
| TQ-16, TQ-17 | D-128 (Q-28) |
| TQ-18, TQ-19 | D-129 (Q-29) |
| TQ-20, TQ-21 | D-129, D-130 — closed as separate gates |
| TQ-22 | D-120, D-133 — GRU gate closed |
| N-01 | D-122 |
| N-02 | D-117 |
| N-03, N-04 | D-107 |
| N-05 | D-111 |
| N-06 | D-119, D-125 |
| N-07, N-08 | D-118, D-119 |
| N-09 | D-119 |
| N-10 | D-126 |
| N-11 | D-122 |
| N-12 | D-115 |
| N-13 | D-103 |

### 14.4 Two-Phase Amendment Decisions

| Decision | Recommendation | Decision | Status |
|---|---|---|---|
| D-134 | R-01 | TensorFlow/Keras is the sole governed neural-network implementation in Phase 1 and Phase 2; the raw GNSS pipeline is independent of the ML framework | Approved |
| D-135 | R-02 | Implement the thesis as a prepared-VTEC MVP followed by a raw-observation pipeline | Approved |
| D-136 | R-03 | ICTP Calibrated GNSS TEC Service is the primary prepared-data candidate, subject to the non-negotiable §6.1B coverage gate; Madrigal is a change-controlled fallback | **Superseded by D-143 and D-144** |
| D-137 | R-04 | Freeze the model and evaluation protocol at the phase transition; target lineage changes, and any predeclared physical target-definition difference must remain explicit in manifests and cross-phase interpretation | Approved; clarified by D-144 |
| D-138 | R-05 | Require matched-timestamp cross-processor validation and a target uncertainty budget before Phase 2 retraining | Approved |
| D-139 | R-06 | Maintain a source-method-code reuse register | Approved |
| D-140 | R-07 | Permit direct code copying with compatible licensing, preserved notices, exact source commit, modification log, isolation, and tests | Approved — Option 1 |
| D-141 | R-08 | Enforce G-P1, G-P2, and G-P3 as blocking acceptance gates | Approved |
| D-142 | R-09 | The student executes the supplied self-contained Kaggle notebook to acquire available ICTP ARUC/BSHM/NICO 2022 files and a ZIP; the executed notebook, archive/per-file hashes, manifests, and coverage evidence are retained, and §6.1B remains blocking | Executed; acquisition mechanics passed, source gate failed |
| D-143 | R-03/R-09 | The measured ICTP audit is authoritative: ARUC 27/365 non-empty days, BSHM 35/365, NICO 0/365 with HTTP 404; ICTP is rejected for confirmatory Phase 1 training and retained only as audit evidence | **Approved by observed gate outcome** |
| D-144 | R-10 | MIT Haystack Madrigal MAPGPS `gps` binned VTEC is the recommended single-source Phase 1 replacement, subject to supervisor approval of the gridded target and a successful §6.1B experiment/schema/cell/coverage audit | **Approved 2026-08-21** — granted by the project owner under the recorded student/supervisor authority equivalence; no supervisor signature artifact exists and none is claimed. The §6.1B experiment/schema/cell/coverage audit remains a separate open condition, so TA-25 stays `Blocked`. *[Amended in place 2026-08-21 per `governance/CHANGE_RECORD_2026-08-21_D-144.md`; effective version v4.3, not yet issued.]* |

---

## 15. Decision Rights and Change Control

### 15.1 Decision Rights

| Decision | Student | Supervisor |
|---|---|---|
| Code organization within Section 10 | May decide | No approval unless scope changes |
| Plot style and minor reporting detail | May decide | No |
| Values inside an already frozen grid | May execute | Grid approved at G-05 |
| Target, horizon, stations, primary estimand, test dates | May recommend | Approval required |
| The IRI benchmark-only role and the IRI-free feature contract | May recommend | **Approval required** |
| Package, DCB, mapping, hourly target, IRI configuration | Prepare evidence | Approval required |
| Add/remove required models or features | May recommend | Approval required |
| Adding a constellation beyond GPS | May recommend with evidence | Approval required |
| Change after December exposure | Cannot preserve confirmatory status alone | Approval plus explicit exploratory label/new test |
| Expand geographic, operational, positioning, or commercial claims | No | New evidence and approval required |
| **Any scientific constant left `TBD`** | **May not fill** | **Must be frozen by a human with evidence** |

### 15.2 Change Record

Every material change records:

1. requested change and reason;
2. alternatives;
3. affected requirements, data, code, experiments, schedule, and claims;
4. whether the locked test has been accessed;
5. required regeneration or invalidation;
6. approver, date, and effective version.

---

## 16. Required Deliverables

1. Approved final preflight specification (this document, v4.2).
2. **ICTP source-rejection evidence plus an approved Phase 1 replacement decision, rights/usage record, location/cell/file inventory, metadata registry, common-date coverage report, and immutable source manifest.**
3. Constellation, observable, and cadence report.
4. Package trial decision report and calibration-layer source with tests.
5. DCB availability and hand-worked sign example, including the reversed-sign control.
6. GNSS processing sensitivity report and processor verification report.
7. **Target uncertainty budget.**
8. Separate versioned Phase 1 prepared-VTEC and Phase 2 independently produced VTEC releases with data dictionaries and lineage.
9. IRI benchmark validation report and GIM interpolation/independence report.
10. Feature availability matrix, frozen feature dictionary, and IRI-free denial test evidence.
11. Split, fold, comparison-wide mask, and comparison-set manifests.
12. Modular code repository and tests.
13. Baseline, benchmark, and model artifacts.
14. Experiment registry including failed runs.
15. Locked-test predictions with pre-metric hash, and uncertainty-aware results.
16. Station/regime/quality diagnostic figures and tables, including the top-1%-removed sensitivity.
17. Canonical RAID and decision logs.
18. CPU clean-run reproduction guide and evidence.
19. Agent preflight report.
20. Thesis claims and limitations checklist.
21. Signed `phase_transition_manifest` freezing the TensorFlow/Keras model and evaluation protocol.
22. Matched-timestamp cross-processor and **2×2 cross-target/model** comparison report.
23. External method/code reuse register, copied-code notices, license compatibility record, modification log, and citations.

### 16.1 Proposed Thesis Chapter Structure

1. **Introduction and research problem** — motivation, objective, research questions, contributions, and bounded claims.
2. **Scientific and technical background** — ionosphere, GNSS observables, TEC/STEC/VTEC, DCB, mapping, forecasting, and leakage-free time-series evaluation.
3. **Related work and reusable methods** — baseline methods, neural forecasting literature, raw-processing literature, code provenance, and the gap addressed by this thesis.
4. **Two-phase research methodology** — common target contract, stations/year, fair-comparison protocol, metrics, uncertainty, transition freeze, and reproducibility.
5. **Phase 1: prepared-data MVP** — measured ICTP rejection, replacement-source decision and audit, prepared-target definition, preprocessing, TensorFlow/Keras model, hyperparameter tuning, baselines, and locked evaluation.
6. **Phase 1 results and MVP decision** — overall/per-station results, confidence intervals, ablations, limitations, and go/no-go evidence.
7. **Phase 2: raw-observation TEC/VTEC pipeline** — raw sources, parsing, calibration, DCB, STEC, mapping, QC, validation, and target uncertainty.
8. **Phase 2 retraining and cross-phase results** — frozen-model retraining, common-mask comparisons, 2×2 cross-target analysis, and processor/model attribution.
9. **Discussion** — scientific meaning, robustness, target mismatch, source coverage, licensing/reuse, generalization limits, and threats to validity.
10. **Conclusion and future work** — answered questions, contributions, limitations, and controlled extensions.

Appendices should contain configuration manifests, station coverage, full hyperparameter grids, source-reuse register, license notices, extra diagnostics, and reproducibility commands.

---

## 17. Pre-Implementation Freeze Checklist

### Scientific

- [x] Primary question, IRI-benchmark-only role, and hierarchy defined.
- [x] Mandatory difficulty controls defined as non-optional.
- [x] Three-layer success framework defined.
- [x] Claim boundary and descriptive sector wording defined.
- [x] Confirmatory horizon fixed at +1 h; +24 h scoped as optional.
- [ ] Supervisor sign-off recorded for the IRI role, horizon scope, estimand, seeds, and locked-test protocol.

### Data

- [x] ICTP 2022 file-level coverage/non-zero-size audit executed separately for ARUC, BSHM, and NICO; G-P1A failed and ICTP was rejected for training.
- [x] Supervisor decides D-144 and, if approved, freezes the Madrigal experiment/kindat, VTEC parameter/units, coordinate-to-cell rule, hourly aggregation and numerical coverage minimum. *[Discharged 2026-08-21; this annotation corrected 2026-08-22. **D-144 approved** (see §14.2). All five attached freezes are now closed: experiment/kindat and VTEC parameter/units by **D-4**; the coordinate-to-cell rule by **D-1**, whose countersignature is closed by the **D-1 addendum** under the recorded student/supervisor authority equivalence; the **hourly aggregation statistic** (§6.6) by **D-16** (median of valid provider VTEC samples inside the UTC hour for the station's frozen cell), with the resulting Phase 1 target-row contract frozen by **D-17**; and the **numerical coverage minimum** (§6.1B) by **D-12** (at least 90% usable hourly coverage per station per month, as a hard pass/fail gate, together with D-2's day rule). Change records: `governance/CHANGE_RECORD_2026-08-21_D-144.md`; `governance/CHANGE_RECORD_2026-08-21_freezes.md` and its § Addendum. The prior annotation stated that §6.6's aggregation statistic and §6.1B's coverage minimum "remain `TBD — supervisor freeze gate`"; both had already been frozen when it was written, and §6.1B's own text was amended the same day, so that annotation contradicted this document's §6.1B and its revision table. Corrected per governance finding `UG-02` (`GOV-2026-08-21-UG-01`).]*
  - **Genuinely unresolved, and not closed by the correction above** — listed so no reader mistakes this ticked line for a clean slate: Vision §6.6's "Each row must retain exactly these fields" sentence and TE §6.1's Phase 2-shaped provisional minima remain in textual conflict for Phase 1 (`requirements.md` § Known defects row 10; D-17 governs the approved practical interpretation, and reconciling the source texts runs through §15.2); D-1's IGS site-log validation limitation remains separately open; **G-P1A itself remains `Blocked`** on the Madrigal replacement audit, which is a different question from whether its threshold is frozen; and TA-25 stays `Blocked` on that same audit.
- [ ] Approved replacement passes the 2022 file/cell/schema/units/common-date/December audit for all three coordinates.
- [ ] Phase 1 prepared target uses one provider/product and one physical definition across all locations; the `target_definition_id` and gridded-versus-receiver limitation are recorded.
- [ ] Station registry completed from official site logs with pinned IGRF.
- [ ] File inventory, checksums, and monthly coverage matrix completed.
- [ ] Constellation, observable, and cadence support confirmed for GPS-only.
- [ ] GNSS package trial completed by the frozen contingency date.
- [ ] DCB product confirmed for all three stations; sign hand-verified; reversed-sign control fails.
- [ ] Mapping, shell, cutoff, slip, arc, and levelling settings frozen **after** the declared sensitivities.
- [ ] Hourly support thresholds frozen after the Jan–Nov audit.
- [ ] Six representative station-days verified against two independent references.
- [ ] **Target uncertainty budget produced.**
- [ ] IRI-2016 implementation, switches, and 2000 km ceiling frozen and validated.
- [ ] GIM provenance, interpolation, and network-overlap disclosure verified.
- [ ] Immutable dataset release created.

### Features and Evaluation

- [ ] Availability matrix completed with publication timestamps.
- [ ] Feature dictionary frozen; SSN removed; Dst marked diagnostic-only; F10.7 mean trailing.
- [ ] **IRI-free denial test implemented and proven to fail on injection.**
- [ ] F1–F4 fold and embargo manifest frozen.
- [ ] Comparison-wide masks and comparison sets frozen.
- [ ] Search grids frozen exactly (ridge 6, RF 18, LSTM 16).
- [ ] Tuning criterion and refit rule frozen.
- [ ] Development seed, three final seeds, three-seed averaging rule, and bootstrap seed frozen.
- [ ] Paired-loss estimand and sign convention approved.
- [ ] Vector bootstrap parameters frozen (24 h, 10,000, seed 20221201, 48 h sensitivity).
- [ ] Storm-event separation rule frozen.
- [ ] Practical-relevance policy recorded as a named reference.
- [ ] **December regime and coverage audit completed; H4 status predeclared.**

### Technical and Governance

- [x] TensorFlow/Keras selected as the one forecasting framework for both phases; PyTorch excluded from the governed pipeline.
- [ ] TensorFlow/Keras exact compatible pins and deterministic settings pass the CPU/GPU fixture tests.
- [ ] External method/code reuse register exists; direct-copy license checks and notices are complete.
- [ ] G-P1 passes and the signed `phase_transition_manifest` exists before Phase 2 starts.
- [ ] G-P3 raw-target acceptance passes before Phase 2 model retraining.
- [ ] Both walking-skeleton fixtures pass all measurable checks.
- [ ] Repository structure and four configs created with visible `TBD — freeze gate` markers.
- [ ] Registry and traceability table operational.
- [ ] RAID owners and due dates confirmed.
- [ ] CPU clean-run contract tested on Kaggle and local.
- [ ] **Agent preflight passes with zero unresolved P0 fields and no failing critical test.**

---

# Appendix A — Targeted Literature Review

**Authority:** Nonnormative. The normative protocol is in Sections 1–17.

## A.1 Review Question

What does peer-reviewed research imply about appropriate targets, models, baselines, benchmarks, data requirements, validation, metrics, and defensible contribution for a one-hour-ahead VTEC study using three GNSS stations and one year of data?

## A.2 Reproducible Search Method Requirement

Before thesis submission, the literature-review record shall include databases searched, exact search strings, search date, publication-year range, inclusion and exclusion rules, screening procedure, final included-study list, and a DOI or stable bibliographic identifier for each source.

The review is a **targeted/structured review**, not a systematic review. Citation counts, if retained, are contextual metadata and not quality scores.

## A.3 Evidence Summary

The literature supports:

- LSTM as a credible nonlinear temporal model;
- tree ensembles as serious forecasting competitors whose ranking against LSTM is regime-dependent;
- chronological rather than random evaluation;
- comparisons with persistence, climatology, and empirical models;
- separate station and geomagnetic-regime reporting;
- careful treatment of GNSS-derived VTEC uncertainty, including levelling and receiver-DCB error of order 1 TECU or more;
- block resampling that preserves both serial and cross-sectional dependence.

The literature does not justify assuming:

- that LSTM will beat RF, climatology, or persistence on one year of data;
- that beating IRI demonstrates forecast skill, since IRI is a climatology with no access to recent observations and is routinely outperformed by learned models by 40–70% in published comparisons;
- that RMSE below 2 TECU is a universal success threshold;
- that one month establishes storm or seasonal generalization;
- that GIM or GNSS-derived VTEC is error-free truth;
- **that GNSS-derived VTEC targets are accurate to better than the effect size being claimed;**
- that reduced TEC error proves improved positioning.

## A.4 Literature-Informed Contribution

The defensible contribution is a reproducible, uncertainty-aware three-station comparison in which an ML model trained on a provably IRI-free local information set is evaluated against the IRI-2016 benchmark, while simultaneously being held to persistence and climatology controls, with correct dependence-respecting uncertainty and an explicit target uncertainty budget. It is not a claim of a novel universal architecture, and it is not a claim that beating a climatological benchmark alone constitutes forecast skill.

---

# Appendix B — Decision Rationale

**Authority:** Nonnormative. Section 14 contains the adopted decisions.

- A single primary comparison prevents post-test cherry-picking.
- Making IRI a benchmark rather than an input is what allows the thesis to claim an *independently trained local model*, rather than learned post-processing of IRI.
- Because IRI is a climatology with no access to \(y_t\), beating it is a weak result on its own. This is precisely why persistence, seasonal persistence, and climatology are mandatory co-reported controls rather than optional extras, and why Section 2.4 contains a binding honesty rule.
- Forecast-safe features prevent information from the future entering the model; the trailing F10.7 mean matters because the conventional centered mean literally uses future days.
- Repeated chronological validation reduces dependence on one lucky month, and F4 supplies the only winter-like rehearsal available before December.
- One December holdout protects the final test; hashing predictions before metrics separates generation from evaluation.
- Separating completion, evidence, and practical value makes negative results valid.
- Bounded station claims prevent unsupported geographic generalization; naming the sector descriptively satisfies the proposal without implying spatial sampling.
- An established package plus a transparent calibration layer keeps GNSS preprocessing feasible without blind trust in a black box.
- Stating that the target is an IPP median rather than a zenith column is what makes the IRI and GIM comparisons interpretable.
- The target uncertainty budget exists because levelling and receiver-DCB errors are plausibly the same size as the effect being claimed.
- Comparison-wide masks make model comparisons paired and fair; matched input windows make H3 a test of architecture rather than of window length.
- Small equal frozen grids prevent one model from receiving an unfair advantage and remove researcher degrees of freedom.
- Best-checkpoint restoration and a three-seed mean reduce overfitting and seed luck.
- Vector block resampling respects the fact that three stations under one ionosphere are not three independent experiments.
- A pooled model with per-station reporting balances scope and interpretability at 26,000 rows.
- Modular code, four configs, manifests, hashes, registries, and traceability make the result auditable without letting framework construction compete with GNSS verification.
- Human-owned scientific freezes keep the coding agent an implementer rather than an unrecorded scientist.
- One normative core prevents background material from silently becoming a requirement.

---

# Appendix C — Implementation Freeze Register

These items remain deliberately unresolved because they require data inspection, tool trial, or supervisor judgment. Their unresolved status does not reopen the adopted policy.

| Item | Required decision/evidence | Must be frozen before |
|---|---|---|
| Phase 1 replacement source | Decision D-144; exact provider, experiment, kindat/product, access and rights | Replacement acquisition |
| Phase 1 gridded target | VTEC parameter/units, fill values, station-coordinate-to-cell rule, cell centers/bounds, hourly aggregation, `target_definition_id` | Phase 1 target construction |
| Phase 1 replacement coverage | Common valid timestamps across all three cells, F1–F4 feasibility, December support, numerical minimum | Phase 1 model training |
| Station registry | Verified coordinates, DOMES, hardware intervals, coverage, IGRF coordinates | Full-year processing |
| Constellation support | GPS-only adequacy against support thresholds | Walking skeleton |
| GNSS package | Trial outcome, release/commit, dependencies, configuration | Walking skeleton |
| DCB | Product availability for all three stations, units, sign, worked example | Processor verification |
| GNSS settings | Mapping, shell, cutoff, slips, arcs, levelling — after declared sensitivities | Full-year processing |
| Hourly target | Minimum observations/satellites, gap and spread limits | Model training |
| Aggregation statistic | Median confirmed, or zenith-weighted adopted on evidence | Model training |
| Representative samples | Six station-days and acceptance tolerances | Full-year processing |
| Second reference | IONOLAB-TEC or equivalent receiver/station product; independence and 2022 availability | Processor verification |
| Target uncertainty budget | Levelling, DCB stability, spread, negative-VTEC rate, configuration spread | Claims and threshold policy |
| IRI benchmark | Implementation, switches, ceiling, drivers, sample tolerances | Benchmark generation |
| GIM | Product, interpolation check, network-overlap audit | Comparator generation |
| External features | Release latency, safe lag, missing rule, Hp60 availability | Feature construction |
| Fixtures | Exact seven days and exact month, expected counts/tolerances/runtime | Walking-skeleton test |
| December regime audit | Kp/Hp60 histogram and disturbed-hour count | G-05 |
| Practical value | Named reference confirmed, or descriptive-only rule | December access |
| CPU budget | Benchmark runtime, RAM, storage on Kaggle and local | Full clean run |

---

# Bibliography

- **[REF-01]** Chen et al. (2022). "Prediction of Global Ionospheric TEC Based on Deep Learning." *Space Weather*.
- **[REF-02]** Srivani, Prasad, and Ratnam (2019). "A Deep Learning-Based Approach to Forecast Ionospheric Delays for GPS Signals." *IEEE Geoscience and Remote Sensing Letters*.
- **[REF-03]** Ruwali et al. (2021). "Implementation of Hybrid Deep Learning Model (LSTM-CNN) for Ionospheric TEC Forecasting Using GPS Data." *IEEE Geoscience and Remote Sensing Letters*.
- **[REF-04]** Iluore and Lu (2022). "Long Short-Term Memory and Gated Recurrent Neural Networks to Predict the Ionospheric Vertical Total Electron Content." *Advances in Space Research*.
- **[REF-05]** Kaselimi et al. (2020). "A Causal Long Short-Term Memory Sequence to Sequence Model for TEC Prediction Using GNSS Observations." *Remote Sensing*, 12, 1354.
- **[REF-06]** Tang et al. (2022). "An Ionospheric TEC Forecasting Model Based on a CNN-LSTM-Attention Mechanism Neural Network." *Remote Sensing*, 14, 2433.
- **[REF-07]** Natras, Soja, and Schmidt (2022). "Ensemble Machine Learning of Random Forest, AdaBoost and XGBoost for Vertical Total Electron Content Forecasting." *Remote Sensing*, 14, 3547. — Supports the tree-ensemble baseline, chronological validation, 1 h/24 h horizon comparison, and differencing sensitivity.
- **[REF-08]** Liu, Zou, and Yao (2020). "Forecasting Global Ionospheric TEC Using Deep Learning Approach." *Space Weather*, 18. — Reports first-hour RMSE of 0.86–1.27 TECU and describes learned performance as competitive with, not superior to, persistence.
- **[REF-09]** Wang, Zhu, and Hu (2023). "Ionosphere Total Electron Content Modeling and Multi-Type Differential Code Bias Estimation Using Multi-Mode and Multi-Frequency GNSS Observations." *Remote Sensing*, 15, 4607.
- **[REF-10]** Yasyukevich et al. (2023). "Klobuchar, NeQuickG, BDGIM, GLONASS, IRI-2016, IRI-2012, IRI-Plas, NeQuick2, and GEMTEC Ionospheric Models: A Comparison in Total Electron Content and Positioning Domains." *Sensors*, 23.
- **[REF-11]** Cerqueira, Torgo, and Mozetič (2019). "Evaluating Time Series Forecasting Models: An Empirical Study on Performance Estimation Methods." *Machine Learning*, 109, 1997–2028.
- **[REF-12]** Yasyukevich, Mylnikova, and Vesnin (2020). "GNSS-Based Non-Negative Absolute Ionosphere Total Electron Content, its Spatial Gradients, Time Derivatives and Differential Code Biases." *Sensors*, 20. — Supports DCB care, GPS-first scope, two-reference verification, and explicit target uncertainty; documents inter-algorithm disagreement exceeding 10 TECU.
- **[REF-13]** Cherniak and Zakharenkova (2019). "Evaluation of the IRI-2016 and NeQuick electron content specification by COSMIC GPS radio occultation, ground-based GPS and Jason-2 joint altimeter/GPS observations." *Advances in Space Research*. — Supports treating topside/plasmaspheric mismatch as a physical source of IRI–GNSS disagreement.
- **[REF-14]** Sulungu (2024). "Performance of IRI 2016 model in predicting total electron content (TEC) compared with GPS-TEC over East Africa during 2019–2021." *Scientific Reports*, 14. — Supports evaluating structured, time-varying IRI bias rather than assuming constant model error.
- **[REF-15]** Gonçalves (2011). "The Moving Blocks Bootstrap for Panel Linear Regression Models with Individual Fixed Effects." *Econometric Theory*, 27, 1048–1082. — Supports resampling the vector of station observations together to preserve serial and cross-sectional dependence.
- **[REF-16]** Ciraolo et al. (2007). "Calibration errors on experimental slant total electron content (TEC) determined with GPS." *Journal of Geodesy*. — Levelling errors of 1.4–5.3 TECU and intra-day receiver bias variation of 1.4–8.8 TECU; basis for the target uncertainty budget.
- **[REF-17]** Nie et al. (2018). "Revisit the calibration errors on experimental slant total electron content (TEC) determined with GPS." *GPS Solutions*. — Daily-constant receiver DCB introduces mis-modelling error of at least several tenths of a TECU.
- **[REF-18]** Uga et al. (2026). "Regime-dependent predictability of high-latitude ionospheric TEC: A comparative machine learning study." *Physics of Plasmas*. — RF beats LSTM in one regime, a simple smoother beats all ML in another, and persistence is the weakest benchmark; basis for the mandatory difficulty controls.
- **[REF-19]** Faruna et al. (2024). "Comparative analysis of single station-based and network-based VTEC modeling approaches in Nigeria using orthogonal transformation." *Scientific African*. — Supports single-receiver VTEC at 1-hour resolution.
- **[REF-20]** Risbey et al. (2021). "Standard assessments of climate forecast skill can be misleading." *Nature Communications*. — Forecast-skill assessments are strongly determined by baseline choice; supports the binding honesty rule.
- **[REF-21]** Rideout and Coster (2006). "Automated GPS processing for global total electron content data." *GPS Solutions*, 10, 219–228. — Describes the MAPGPS processing underlying Madrigal GNSS TEC products.
- **[REF-22]** MIT Haystack Observatory. "Using GNSS to Measure Ionospheric Total Electron Content." — Official MAPGPS/Madrigal product overview, access route, and processing context; retrieval date and permanent experiment/file citations must be recorded in the dataset manifest.
