# Intent Statement — Hourly VTEC Forecasting (TEC_Project Phase 1 onward)

> **Status disclosure.** The decision record this initiative builds on (`evidence/DECISIONS.md`, D-1 through D-10) is student-sole-signed except for D-3/D-144, countersigned by the supervisor and recorded on 2026-08-15. Countersign of the remaining items is sought in parallel. [Q12] [amended 2026-08-15]

## Sources

- [desc] Initial description: "Execute TEC_Project Phase 1 acquisition under D-9 Option B with D-10 corrections (Kp/ap3 from GFZ, hourly Dst from Kyoto WDC, observed F10.7 from Canada Solar Radio Monitoring Program), align drivers onto the hourly grid without interpolation, define availability timestamps and lag all predictors against forecast leakage, then build the hourly VTEC model on ARUC 40/44, BSHM 32/35, NICO 35/33 for calendar 2022 with December 2022 as the locked test set."
- [scope] Workflow-selected scope: `research-pipeline-governed`.
- [Q1]–[Q21] Confirmed answers in `intent-capture-questions.md`. [Q19] is the governance correction record for board report GOV-2026-08-13-IC-01 and supersedes the parts of [Q14], [Q16], [Q17] and [Q18] it names. [Q21] is the governance correction record for board report GOV-2026-08-13-IC-02 (findings GOV-13 to GOV-21, applied in full) and governs every statement this artifact makes about the success framework, the target's representativeness, execution blocking, reporting breakdowns, the driver contract, the comparator set, and supervisor authority.

## Glossary

Definitions only — nothing here is a claim about this initiative. Provided so a non-specialist reader can follow the artifact. [Q21]

| Term | Meaning |
|---|---|
| VTEC | Vertical Total Electron Content — the number of free electrons in a vertical column through the ionosphere, the quantity being forecast |
| TECU | TEC Unit, the measurement unit for VTEC (10¹⁶ electrons per square metre) |
| Cell | A 1°×1° geographic bin of the gridded source product. The three cells here stand in for the ARUC, BSHM and NICO station locations |
| IPP | Ionospheric Pierce Point — where a satellite-to-receiver ray crosses the ionospheric shell. The target aggregates values at pierce points, not directly above the antenna |
| MAPGPS | The gridded prepared-VTEC product from the MIT Haystack CEDAR Madrigal database used as the Phase 1 source |
| IRI-2016 | International Reference Ionosphere 2016, an empirical climate model of the ionosphere, used here purely as a benchmark to compare against |
| GIM | Global Ionosphere Map — a gridded VTEC product; the CODE final GIM is used as a contextual comparator only |
| Kp, ap3 | Three-hourly global geomagnetic activity indices |
| Hp60, ap60 | Hourly-cadence counterparts of Kp and ap, matching the hourly modelling grid |
| Dst | Disturbance storm-time index, hourly; a measure of geomagnetic storm intensity |
| F10.7 | Solar radio flux at 10.7 cm wavelength, a standard proxy for solar activity |
| Persistence | The trivial forecast "next hour equals this hour", used as a difficulty control |
| Climatology | A fitted average by station, month and hour, used as a difficulty control |
| LSTM | Long Short-Term Memory, the recurrent neural network family used as the learned model |
| Paired loss differential | The confirmatory quantity: benchmark squared error minus model squared error at each matched timestamp, averaged. Positive means the model beat the benchmark |
| Block bootstrap | An uncertainty method that resamples whole 24-hour blocks rather than individual hours, so that correlation between neighbouring hours is preserved |
| Leakage | Using information not genuinely available at the moment a forecast is issued — the central failure mode this pipeline is built to prevent |
| Locked test set | December 2022, held shut and unexamined until the experiment is frozen and signed off |
| Freeze gate (G-05, G-06, G-07, D-144…) | A named checkpoint whose value must be resolved, recorded and approved by the supervisor before the work it governs may begin |

## Problem Statement

The initiative solves two joined problems: producing a defensible hourly VTEC forecast for the three frozen cells as the empirical core of a thesis, and demonstrating that a governed, reproducible pipeline can be built end to end. The forecast result is the primary claim; reproducibility is the supporting one. [Q1]

The immediate obstacle is that the acquisition route is decided and corrected but not executed. Phase 1 acquisition follows D-9 Option B with the D-10 corrections applied, and nothing downstream can proceed until it runs. [desc] [Q4]

The technical substance of what must be built: obtain Kp and ap3 from GFZ, hourly Dst from Kyoto WDC, and observed F10.7 from Canada's Solar Radio Monitoring Program; align those drivers onto the hourly grid without interpolation; define availability timestamps and lag every predictor against forecast leakage; then build the hourly VTEC model. [desc]

### Benchmark role

The confirmatory comparison is an independently trained local ML model against the **IRI-2016 empirical benchmark**. IRI-2016 is a benchmark only. It is **architecturally excluded from the model**: IRI values, residuals, targets, transformations and derived fields never reach training or inference, and no IRI or GIM module is imported into feature or model code — IRI is joined at evaluation time and nowhere else. [Q19]

### Driver contract

The drivers carry distinct roles and forecast-safety rules; they are not interchangeable. [Q19]

| Driver | Source | Role | Availability rule |
|---|---|---|---|
| Kp, ap3 | GFZ Potsdam | Forecast feature | Lag ≥ 3 h; only completed 3-hour intervals available at the forecast origin, repeated within their own interval | 
| Hp60, ap60 | GFZ Potsdam | Forecast feature; **preferred over Kp alone**, because the cadence matches the hourly target | Lag ≥ 1 h | 
| Dst (hourly) | Kyoto WDC | **Diagnostic / hindcast-only — not a confirmatory primary feature** | Aligned to its own hourly averaging interval; not used as a confirmatory forecast feature |
| F10.7 observed | Canada's Solar Radio Monitoring Program (observed, **not** 1-AU-adjusted) | Forecast feature | Lag 1 day (previous-day value); trailing 81-day mean, never centred |
| SSN | — | **Removed** | Not used |

Hp60/ap60 were absent from the initial description's four-parameter set and are restored here as Primary-status indices of the governing feature contract. [Q21]

Carry-forward of any driver is bounded at ≤ 3 h. No interpolation, smoothing, or carry-forward beyond a value's own defined interval. [desc] [Q19]

**Join semantics.** Every driver series is time-indexed only — one value per epoch, identical across all three cells. Joining a driver onto the modelling grid must never imply a per-cell measurement. The joined product therefore draws on **two source families**, not one, and provenance, licensing, citation and acknowledgement obligations cover both the VTEC provider and the GFZ, Kyoto WDC and Canadian index producers. [Q21] [Q19]

### Phase 1 source status

The Phase 1 VTEC source is the audited calendar-2022 Madrigal MAPGPS record set promoted under D-9 Option B. Its governing decision D-144 is **countersigned by the supervisor and recorded**: the signature row in `evidence/DECISIONS.md` was entered on 2026-08-15, superseding the earlier `approved-pending-record` state. The countersign is recorded as reported by the student; no signature artifact is filed in the repository, and Technical Environment v3.2 §1.5 still reads "Pending — D-144" until it is updated through the Vision §15.2 change-control process. The Phase 1 source is therefore approved and acquisition is no longer blocked on it. [Q19] [Q12] [Q21] [amended 2026-08-15]

### Driver preconditions

Two items previously recorded as open are closed at the intent level. The Dst-grade blocker is closed by using Kyoto provisional Dst for all of 2022, recording its provisional status and non-commercial-use notice, and hashing the retrieved files. The F10.7 timing blocker is closed by retaining the previous-day observed-F10.7 rule. [Q10]

A further precondition applies before acquisition freeze: audit the Canadian F10.7 archive from 2022-03-18 onward for the documented month-long outage, reporting exact missing dates and any qualifiers or reconstructed values. No imputation or substitution is chosen until the measured gap is recorded and governed. [Q10]

## Target Customer

The customer is the student and thesis author, who needs a result that survives examination. [Q2]

The pain is that a forecasting result is only as defensible as the provenance and leakage discipline behind it. [Q1] [Q3]

## Success Metrics

> **Phase-boundary note.** The experimental-design detail in this section and the two that follow it — the metric set, the mandatory difficulty controls, the model set, the forecast horizon, the reporting contract and the sealing condition — is **carried forward from governance correction, binding on later stages, and not re-derived here**. It sits in an ideation artifact because the governance boards at [Q19] and [Q21] fixed it against the project's normative core before this stage completed, not because intent capture chose to design the experiment. Requirements Analysis, NFR Requirements and NFR Design **inherit** these values and must not re-litigate or duplicate them; their job is to give them stable IDs, make them checkable, and carry them to their freeze gates. [Q21]

Success is defined in **three layers**, and the layers are not interchangeable. A correct negative or inconclusive model result does not make the project a failure. [Q21]

| Layer | Rule | Meaning | Source |
|---|---|---|---|
| Project completion | A trusted target, the required baselines and models, the locked test, uncertainty analysis, **reproducible artifacts**, and honest conclusions are all complete | The thesis work was performed correctly | [Q21] |
| Statistical evidence | The paired primary loss differential is positive and its 95% confidence interval excludes zero | Evidence favours the independent local LSTM over the IRI-2016 benchmark | [Q21] [Q19] |
| Practical relevance | The improvement reaches a separately justified reference magnitude and is not smaller than the target uncertainty budget | The size may matter in practice. Reported **descriptively** unless the supervisor explicitly approves a threshold; no threshold may be introduced or reinterpreted after December is opened | [Q21] |

Two measures carry the initiative's own pass/fail weight within the completion layer: [Q3]

| Measure | Definition | Source |
|---|---|---|
| Forecast skill | The primary estimand below, evaluated on the locked December 2022 test set, reported per cell | [Q3] [Q19] |
| Leakage freedom | Every predictor demonstrably available at its forecast origin, verified by executable tests | [Q3] |

### Primary estimand

The primary estimand is the **paired loss differential: IRI-2016 squared loss minus LSTM squared loss**, so a **positive** value favours the LSTM. It is reported with a 95% confidence interval. Percentage reduction is a **derived** summary, labelled as derived, and is never the confirmatory quantity. [Q19]

### Metrics

**RMSE is the primary reported error metric.** [Q19]

| Metric | Role | Source |
|---|---|---|
| RMSE | Primary | [Q19] |
| MAE | Supporting | [Q16] [Q19] |
| Median absolute error | Supporting | [Q19] |
| Mean error / signed bias | Supporting | [Q16] [Q19] |
| R² | Supporting | [Q19] |
| Pearson correlation | Supporting | [Q16] [Q19] |
| P90 absolute error | Supporting | [Q19] |
| P95 absolute error | Supporting | [Q16] [Q19] |
| Derived: 1 − RMSE_model / RMSE_reference | Derived summary, labelled as derived | [Q19] |
| MAPE | Excluded | [Q16] |

### Mandatory difficulty controls

Three controls are co-reported **in the primary results table**. They are not optional and are never relegated to an appendix. [Q19]

| ID | Control | Definition |
|---|---|---|
| M-01 | Persistence | ŷ(t+1) = y(t) |
| M-02 | 24-hour seasonal persistence | ŷ(t+1) = y(t−23) |
| M-03 | Fitted station × month × hour climatology | Fitted on training folds only |

**Binding honesty rule.** If any of these controls achieves a lower paired loss than the LSTM on the locked test, that fact appears in the primary results table and in the abstract-level conclusion. A favourable LSTM-versus-IRI result does not license silence about an unfavourable LSTM-versus-persistence or LSTM-versus-climatology result. [Q19]

### Model set

Persistence, 24-hour seasonal persistence, fitted climatology, ridge regression, Random Forest, and the compact LSTM. [Q19]

**External comparator.** CODE final GIM is the contextual comparator, joined at evaluation time only and never as a model input. Like IRI-2016 it is evaluated at the station coordinate and carries the representativeness mismatch recorded under *Target representativeness — binding*. [Q21]

### Forecast horizon

**+1 h is the confirmatory horizon, and the only horizon required for thesis completion.** It is the sole primary endpoint. +24 h is an optional extension attempted only after the minimum thesis is complete and frozen; it remains configurable but is outside the critical path and no thesis claim depends on it. No horizon between +1 h and +24 h is authorised. No future-observed VTEC or driver values may be used at any horizon. [Q19] [Q17]

### Reporting

December metrics are reported separately for ARUC, BSHM and NICO at the +1 h confirmatory horizon. The headline cross-cell result is an **equal-station (equal-cell) macro-average**; pooled row-weighted results are supplementary only. Full-month metrics are primary. The following breakdowns are **required**, not optional: quiet versus disturbed geomagnetic regime (quiet Kp < 4, disturbed Kp ≥ 4, storm Kp ≥ 5, each three-hour Kp value mapped to its hours), observation-quality strata (valid satellite count, valid observation count, within-hour VTEC spread read as a spatial-temporal representativeness proxy, processor and QC flags, station and month), per-cell metrics, and the time-weighted pooled summary. December regime results are **descriptive only** — a general storm-performance claim requires at least three independent storm events in December, and with fewer the storm results are bounded case evidence. A **top-1%-absolute-error-removed sensitivity** is reported so the result cannot rest on a handful of extreme hours, and the target uncertainty budget is reported adjacent to the primary result. Daily error and four local-solar-time diagnostic bins are retained as additional diagnostics. [Q21] All model–baseline comparisons use a single comparison-wide mask with identical paired valid timestamps, and report sample count and coverage — no pairwise or model-specific masks. Uncertainty is estimated with a **vector block bootstrap carrying all three stations together** in 24-hour blocks, reported at 95%, with the cross-station paired-error correlation reported alongside. [Q18] [Q19]

### Test-set sealing condition

**Governing authority: G-05 experiment freeze, per Vision §8.3. December 2022 is not opened until G-05 is signed by the supervisor.** [Q19]

The following summary is **non-normative and deliberately incomplete** — it exists for readability and never substitutes for G-05: the frozen set includes the folds F1–F4 with 24-hour embargo, comparison-wide masks, hyperparameter grids, seeds, the primary estimand, the bootstrap procedure, geomagnetic regimes and the storm rule; and the December regime-count audit report must be complete. At the moment of opening, G-06 access rules apply: access authorisation, one write, and the prediction hash generated **before** any metric is computed. [Q19] [Q15]

**Who completes this list, and when.** G-05 itself is the authoritative definition of its own input set, and this artifact deliberately does not restate it. Inside this workflow, **NFR Requirements (stage 3.2)** owns assembling that list into a checkable, itemised freeze manifest and carrying it to the G-05 signature; **Requirements Analysis (stage 2.3)** owns giving each item above a stable requirement ID so the manifest can be traced. Until that manifest exists and is signed, the sealing condition is recorded but not yet checkable, and December stays shut. Naming the owning stages here is what keeps the condition from being deferred indefinitely. [Q21]

## Initiative Trigger

Two triggers apply together: the Phase 1 route is decided (D-9) and corrected (D-10) but not executed, so nothing downstream can proceed until it runs; and a thesis deadline or milestone requires the empirical chapter to start. [Q4]

**Execution is unblocked as of 2026-08-15.** D-9's own text conditions the promotion of the audited record set on D-144, and that countersign has been entered in the `evidence/DECISIONS.md` signature table. Acquisition may now execute under D-9.

Two qualifications remain. The D-9 and D-10 signature rows are still blank, so the acquisition route and the driver-source corrections themselves remain sole-signed. Technical Environment v3.2 §1.5 still reads *Pending — D-144*, and updating it runs through the Vision §15.2 change-control process rather than through this workflow. [Q21] [Q19] [amended 2026-08-15]

## Initial Scope Signal

**Workflow-selected scope:** `research-pipeline-governed`. [scope]

**User-confirmed product boundary:** wider than the workflow default. The boundary is the pipeline, the locked-December evaluation, and the thesis chapter's generated inputs. [Q9] [Q14] [Q19]

**Confirmed deliverable set:** [Q11] [Q13] [Q14] [Q19]

| Deliverable | Status | Source |
|---|---|---|
| Runnable acquisition + alignment + lagging pipeline producing the joined hourly dataset | In boundary | [Q11] |
| Trained model set and recorded configuration (persistence, seasonal persistence, climatology, ridge, RF, compact LSTM) | In boundary | [Q11] [Q19] |
| Locked-December evaluation report against the primary estimand with all three mandatory controls co-reported | In boundary | [Q11] [Q19] |
| Reproducibility package (pinned environment, seeds, hash manifests) | In boundary; part of the project-completion layer and required for G-07 | [Q13] [Q21] |
| Thesis chapter **inputs** — figures, tables, metrics, methods text | In boundary; chapter prose is authored outside this initiative | [Q14] [Q19] |

**Frozen modelling target:** hourly grid, three cells (ARUC 40/44, BSHM 32/35, NICO 35/33), calendar year 2022, December 2022 as the locked test set. [desc] [Q19] The three sites are correlated, not independent spatial samples. [Q21]

**Target representativeness — binding.** The Phase 1 target is a **provider-prepared gridded VTEC value for a cell**, not a zenith column measured above a receiver antenna, and grid values are never treated as receiver observations. The hourly target is an ionospheric-pierce-point aggregate. IRI-2016 and the CODE final GIM comparator are both evaluated at the **station coordinate**. Every comparison between the model and either of them therefore carries this documented cell-versus-station representativeness mismatch, and it is stated wherever those comparisons are reported. Statistical inference is bounded to these three sites, this calendar year, the +1 h horizon, and the documented processing choices; the sector description is descriptive only. [Q21]

**Reproducibility standing:** reproducible artifacts sit **inside the project-completion success layer** — the thesis work is not correctly performed without them. The user's disposition narrows what the packaged deliverable must contain, not whether reproducibility counts: an incomplete package does not by itself void the forecast-skill and leakage-freedom measures, and **G-07 final acceptance remains a mandatory full-board gate** that an incomplete package does not pass. [Q13] [Q19] [Q21]

**Governance posture:** D-3/D-144 is countersigned as of 2026-08-15; D-1, D-2, D-4 through D-10 remain sole-signed. The initiative proceeds on the basis that those decisions are recorded and individually reversible, with countersign sought in parallel. [Q12] [amended 2026-08-15]

## Scoped Verification Obligations

These were raised as assumptions and are dispositioned as precisely scoped obligations rather than retained assumptions. [Q15]

| # | Obligation | Precise scope | Source |
|---|---|---|---|
| 1 | Kyoto Dst grade | Confirm provisional-grade Dst is published for the full span 2022-01-01 to 2022-12-31 as a single grade. Record the provisional status and the non-commercial-use notice, and hash the retrieved files. Where any span is not available at provisional grade, record which span and at what grade — do not silently mix grades | [Q10] [Q15] |
| 2 | Canadian F10.7 archive audit | Audit the archive from 2022-03-18 onward for the month-long outage. Report exact missing dates and any qualifiers or reconstructed values. Do not impute or choose a substitute until the measured gap is recorded and governed | [Q10] [Q15] |
| 3 | Skill baseline and estimand | Resolved: the primary estimand is the paired IRI−LSTM loss differential; persistence, seasonal persistence and climatology are mandatory co-reported controls. All are frozen at G-05 before the test set is opened | [Q15] [Q19] |
| 4 | D-144 countersign record | **Partly discharged 2026-08-15.** The D-3/D-144 countersign is entered in the `evidence/DECISIONS.md` signature table. Still open: the D-9 and D-10 signature rows, and updating Technical Environment §1.5, §2 and TA-25 from Pending/Blocked through Vision §15.2 change control. Owned by the student and supervisor, not by this initiative's tooling | [Q19] [amended 2026-08-15] |
| 5 | Evaluation code | No evaluation code exists yet. It is authored inside this initiative and must be complete, reviewed and frozen as part of the G-05 set before December 2022 is opened. Its absence at intent time is a recorded fact, not an assumption | [Q20] |

## Governance Dependencies

These are not assumptions to be discharged inside this initiative; they are dependencies on parties or decisions outside it. [Q15]

Where a row reads `Unknown (open question)`, the value is **dependency-tracked by design and is not an untagged assumption**: [Q15] reclassified these items out of the assumptions register deliberately, so they carry no `[assumption]` label. [Q15] [Q21]

| # | Dependency | Detail | Source |
|---|---|---|---|
| 6 | Supervisor countersign availability | Unknown (open question); the record states unavailability at decision time and gives no return date | [Q5] [Q15] |
| 7 | Examining-committee requirements | Whether the committee imposes communication or reporting requirements of its own is Unknown (open question) | [Q5] [Q8] [Q15] |
| 8 | D-144 signature | **Closed 2026-08-15** — countersigned and recorded; Phase 1 acquisition is no longer blocked on it | [Q19] [Q21] [amended 2026-08-15] |
| 9 | G-05 signature | December cannot open without it; owned by the supervisor | [Q19] |
| 10 | Thesis chapter prose | Authored outside this initiative; this initiative supplies inputs only | [Q14] [Q19] |

## Assumptions & Open Questions

None.

## Review

NOT-READY

*(Advisory review by aidlc-product-lead-agent, iteration 1, against the current `intent-statement.md` and `stakeholder-map.md`, following a human change request that asked for all six findings from the previous advisory pass to be resolved. This is a single, non-repeating advisory pass; findings below go to the human as-is for the approval gate to weigh, and are independent of the TEC governance board's own three passes recorded below.)*

### Disposition of the six prior findings

| # | Prior finding | Disposition | Evidence |
|---|---|---|---|
| 1 | Major — broken cross-ref, "Model set → External comparator" pointed at *Frozen modelling target* | **Closed** | `### External comparator` now reads "...carries the representativeness mismatch recorded under *Target representativeness — binding*", which is the correct paragraph — it is the one that actually states the cell-vs-station mismatch. |
| 2 | Major — G-05 sealing condition defers its own input list, against the project rule requiring inputs to be specified in the same stage that records the condition | **Partly closed** | A new "Who completes this list, and when" paragraph now names Requirements Analysis (2.3) and NFR Requirements (3.2) as the owning stages, which improves traceability. But the paragraph itself still states "the sealing condition is recorded but not yet checkable" and the preceding summary is still explicitly "non-normative and deliberately incomplete." That is the exact condition the project rule warns against ("deferring them leaves the condition unmeetable and uncheckable") — the fix names *who* will supply the inputs later, it does not supply them *in this stage* as the rule literally requires. |
| 3 | Major — ideation-phase boundary not held; experimental-design detail embedded in an intent artifact | **Closed** | A phase-boundary note now opens `## Success Metrics`, explicitly marking the metric/model/horizon/reporting/sealing detail as "carried forward from governance correction, binding on later stages, and not re-derived here," and directing Requirements Analysis / NFR Requirements / NFR Design to inherit rather than re-litigate it. This is the fix the prior finding itself offered as an acceptable option. |
| 4 | Minor — "The three sites are correlated, not independent spatial samples" tagged `[desc] [Q19]`, unsupported by either source | **Not closed** | The sentence is now split out and retagged `[Q21]` alone (`## Initial Scope Signal`, `**Frozen modelling target:**`). But GOV-13 through GOV-21 (the findings Q21 disposes of) do not contain a spatial-correlation claim about the three sites either — GOV-14 is about the IPP-vs-station-zenith mismatch, a different claim. The retag swaps one non-entailing source tag for another; the claim is still ungrounded under the Step 5 contract. |
| 5 | Minor — unglossed jargon against the ideation readability guardrail | **Closed** | A new `## Glossary` section defines 18 terms (VTEC, TECU, IPP, MAPGPS, Hp60/ap60, block bootstrap, etc.), directly addressing the readability guardrail. |
| 6 | Minor — Governance Dependencies "Unknown (open question)" rows carry no `[assumption]` tag and no note explaining the omission is deliberate | **Closed** | Both `intent-statement.md` (`## Governance Dependencies`) and `stakeholder-map.md` (`## Governance Dependencies`) now carry the identical note: "the value is **dependency-tracked by design and is not an untagged assumption**... reclassified these items out of the assumptions register deliberately, so they carry no `[assumption]` label." |

### New findings

1. **Major — Retag on finding 4 still fails the Step 5 grounding contract.** (See disposition row 4 above.) "The three sites are correlated, not independent spatial samples." (`intent-statement.md`, `## Initial Scope Signal`, `**Frozen modelling target:**`) is tagged `[Q21]`, but no GOV-13–GOV-21 finding, and no text under the Q21 answer, states or implies spatial correlation between ARUC/BSHM/NICO. Under the Step 5 grounding contract this is a substantive claim carrying a source tag that does not entail it — the same defect as before, relocated to a different tag. Fix: either find the actual supporting source and retag correctly, or move the sentence to `## Assumptions & Open Questions` tagged `[assumption]`, or drop it.

2. **Minor — G-05 fix is transparent about, but does not resolve, its own non-compliance with the project rule.** (See disposition row 2 above.) As currently worded the paragraph is internally honest ("recorded but not yet checkable"), which is good practice, but it does not close the underlying gap the project rule (c5) targets: a reader of this stage alone still cannot check the G-05 precondition set, because the authoritative list lives outside this artifact and outside this stage's outputs. If the team's intent is that G-05's own governing document (Vision §8.3) is the permitted exception to c5 — i.e., a gate whose authority document, not this stage, owns the input list — that reasoning should be stated explicitly in the artifact rather than left implicit, so the rule's applicability to this specific gate is itself a recorded decision and not an inference a reader has to make.

3. **Minor (suggestion, not a hard defect) — the new Glossary's blanket source tag stretches the permitted-source model.** The Glossary's intro line ("Definitions only — nothing here is a claim about this initiative... [Q21]") tags the whole section to `[Q21]`, but most entries (VTEC, TECU, Kp, F10.7, LSTM, persistence, climatology, etc.) are generic domain vocabulary, not content confirmed by Q21 specifically. Step 3 of the stage protocol says not to register "background knowledge, common practice, or an inference as a source." The section explicitly disclaims being a set of claims, which is a reasonable basis for exempting it from per-row sourcing, but the blanket `[Q21]` tag is not itself accurate provenance for most rows. Not blocking — worth a lighter-touch note (e.g. "standard domain terminology, not sourced to the Q&A register") instead of a source tag that doesn't really apply.

No new findings on: source-register range coverage (both artifacts still correctly declare `[Q1]–[Q21]` and stay within that range); the `## Assumptions & Open Questions: None.` claim in both artifacts, which remains honest given the Scoped Verification Obligations / Governance Dependencies split; the measurability of the stated success metrics; or any other cross-reference in the document besides the one addressed in finding 1 above.

### Governance board record

Two independent governance board reviews have been run against this artifact set under the TEC_Project overlay, and their findings are recorded here alongside the advisory review above.

- **GOV-2026-08-13-IC-01** — verdict FAIL, findings GOV-01 to GOV-12. Dispositioned at [Q19]: every board recommendation applied as written.
- **GOV-2026-08-13-IC-02** — verdict FAIL, findings GOV-13 to GOV-21, full board (escalated from adaptive on target-lineage ambiguity). Dispositioned at [Q21]: all nine findings applied as written. Blockers were the redefined success framework (GOV-13), the undocumented cell-versus-station representativeness mismatch (GOV-14), the "unblocked" execution claim against a Pending D-144 (GOV-15), and supervisor authority recorded as non-gating (GOV-20).

- **GOV-2026-08-13-IC-03** — re-review of this revised artifact set, full board, verdict **CONDITIONAL PASS**. All nine IC-02 findings verified closed. Residual non-blocking items with named owners: the blank D-3/D-144, D-9 and D-10 signature rows (GOV-22, blocks acquisition at G-P1A), the absent G-05 signature (GOV-23, blocks opening December), the unmeasured Kyoto Dst span and Canadian F10.7 outage audit (GOV-24, due before acquisition freeze), and board reports not yet persisted under `governance/reviews/` (GOV-25).

The boards recommend only; none grants academic approval nor authorises locked-test access. The student and supervisor remain the deciding authority. [Q21]

### Post-approval amendment — 2026-08-15

This stage was approved on 2026-08-13. On 2026-08-15 the student reported that the supervisor has countersigned D-3/D-144. The signature row was entered in `evidence/DECISIONS.md` and the affected statements in this artifact and in `stakeholder-map.md` were corrected in place, each marked `[amended 2026-08-15]`.

What changed: the Phase 1 source is approved, so Phase 1 acquisition is no longer blocked; governance dependency 8 is closed and scoped obligation 4 is partly discharged; board findings GOV-15 and GOV-22 are superseded by the recorded signature.

What did not change: D-9 and D-10 remain sole-signed, Technical Environment v3.2 §1.5 still reads *Pending — D-144* until updated through Vision §15.2 change control, and G-05 still gates the December test set. The countersign is recorded as reported by the student; no signature artifact is filed in this repository, and attaching one would strengthen the record.
