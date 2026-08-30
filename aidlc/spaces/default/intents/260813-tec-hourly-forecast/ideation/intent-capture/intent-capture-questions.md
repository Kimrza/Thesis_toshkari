# Intent Capture & Framing — Questions

**Stage:** intent-capture
**Depth:** Comprehensive

## Sources

- [desc] Initial description: "Execute TEC_Project Phase 1 acquisition under D-9 Option B with D-10 corrections (Kp/ap3 from GFZ, hourly Dst from Kyoto WDC, observed F10.7 from Canada Solar Radio Monitoring Program), align drivers onto the hourly grid without interpolation, define availability timestamps and lag all predictors against forecast leakage, then build the hourly VTEC model on ARUC 40/44, BSHM 32/35, NICO 35/33 for calendar 2022 with December 2022 as the locked test set."
- [scope] Workflow-selected scope: `research-pipeline-governed`.

## Q1. What business or research problem is this initiative solving?

- A. Producing a defensible hourly VTEC forecast for the three frozen cells, as the empirical core of a thesis
- B. Demonstrating that a governed, reproducible pipeline can be built end to end, with the forecast as the vehicle
- C. Both A and B, with the forecast result being the primary claim and reproducibility the supporting one
- D. Something narrower — only completing Phase 1 data acquisition, with modelling deferred
- E. Not yet defined
- X. Other (please specify)

[Answer]:C

## Q2. Who is the customer for this work, and what pain are they experiencing?

- A. The student (thesis author) — needs a result that survives examination
- B. The supervisor and examining committee — need to verify claims against evidence without re-deriving the work
- C. The wider ionospheric-forecasting research community — needs a reproducible baseline over these cells
- D. All of the above, in that order of priority
- E. Not yet defined
- X. Other (please specify)

[Answer]:A

## Q3. What does success look like for this initiative? Which metrics matter?

- A. Forecast skill on the locked December 2022 test set against a stated baseline (e.g. persistence or climatology), reported per cell
- B. Zero forecast leakage — every predictor demonstrably available at its forecast origin, verified by executable tests
- C. Full reproducibility — a third party can re-run the pipeline from the recorded decisions and hashes and obtain the same numbers
- D. All three, and the initiative fails if any one is not met
- E. Not yet defined
- X. Other (please specify)

[Answer]: X. Both options A&B.

## Q4. What triggered this initiative now?

- A. Phase 1 route is decided (D-9) and corrected (D-10) but not executed — the work is unblocked and nothing else can proceed until it runs
- B. A thesis deadline or milestone requires the empirical chapter to start
- C. Both A and B
- D. Not yet defined
- X. Other (please specify)

[Answer]:C

## Q5. Who are the key stakeholders, and what does each care about? (select all that apply)

- A. Student / thesis author (Kimia Rezaei) — owns every decision to date, sole-signed
- B. Supervisor — countersign authority over D-1 through D-10; currently recorded as unavailable
- C. Examining committee / university (Amirkabir University of Technology) — accepts or rejects the final claims
- D. External data providers (Madrigal/CEDAR, GFZ, Kyoto WDC, Canada's Solar Radio Monitoring Program) — citation and acknowledgement obligations
- E. None beyond the student
- X. Other (please specify)

[Answer]:X, options A,B,C are the stakeholders.

## Q6. Who decides scope and priority for this work?

- A. The student alone, with the supervisor countersigning after the fact
- B. The student proposes; the supervisor must approve before execution
- C. Scope is already fixed by D-7 and D-8 and is not open to re-decision in this workflow
- D. Not yet defined
- X. Other (please specify)

[Answer]:A

## Q7. Who influences those decisions without holding decision authority?

- A. The governance review board process defined in this project (`/review-tec-governance`)
- B. Data-provider constraints — what the sources actually publish and at what grade
- C. Both A and B
- D. No influencers identified
- X. Other (please specify)

[Answer]:C

## Q8. Are there communication or reporting requirements for this initiative?

- A. Every decision recorded in `evidence/DECISIONS.md` with a supervisor countersign row, as at present
- B. A governance report per gate, retained as evidence, in addition to the decision record
- C. Periodic supervisor updates on a fixed cadence
- D. No requirement beyond the existing decision record
- E. Not yet defined
- X. Other (please specify)

[Answer]:A

## Q9. The workflow was started with the scope in [scope]. Does that scope match your intended product boundary?

- A. Confirm the workflow-selected scope — the boundary is the pipeline plus the locked-December evaluation, as planned
- B. Different boundary — the deliverable is data acquisition and the joined dataset only; modelling is a separate initiative
- C. Different boundary — the deliverable additionally includes the thesis write-up chapter, not only code and evidence
- D. Not yet defined
- X. Other (please specify)

[Answer]:C

## Q10. Two items are recorded as open and block driver use — Kyoto Dst data grade for 2022, and F10.7 release timing. How should they be treated at the intent level?

- A. Hard preconditions — no driver acquisition begins until both are verified and recorded
- B. Preconditions for Dst grade only; the previous-day F10.7 default (D-10.3) is accepted as-is and the timing question is closed
- C. Neither blocks — proceed under the conservative defaults and record both as stated limitations
- D. Not yet defined
- X. Other (please specify)

[Answer]:X.Close the Dst-grade blocker: use Kyoto provisional Dst for all of 2022, record its provisional status and non-commercial-use notice, and hash the retrieved files.
Close the F10.7 timing blocker by retaining the previous-day observed-F10.7 rule.
Before acquisition freeze, audit the Canadian F10.7 archive from 2022-03-18 onward for the documented month-long outage. Report exact missing dates and any qualifiers or reconstructed values. Do not impute or choose a substitute until the measured gap is recorded and governed.

## Q11. What is the deliverable set that marks this initiative complete? (select all that apply)

- A. A runnable acquisition + alignment + lagging pipeline producing the joined hourly dataset
- B. A trained model and its recorded configuration
- C. A locked-December evaluation report with metrics against a stated baseline
- D. A reproducibility package (pinned environment, seeds, hash manifests) sufficient for third-party re-run
- E. Not yet defined
- X. Other (please specify)

[Answer]:X . All options A&B&C are applicable

## Q12. The decision record states every item is sole-signed and no supervisor has countersigned. How should that affect this initiative?

- A. Proceed — the decisions are recorded and individually reversible; countersign is sought in parallel
- B. Proceed, but every artifact produced here must carry the same unapproved status disclosure
- C. Hold — nothing executes until at least D-9 and D-10 are countersigned
- D. Not yet defined
- X. Other (please specify)

[Answer]:A

## Q13. Follow-up (contradiction): Q1 makes reproducibility a supporting claim, but Q3 omits it from success criteria and Q11 omits the reproducibility package from the deliverables. How should reproducibility be treated?

- A. Restore it fully — reproducibility is a success criterion AND a packaged deliverable (pinned environment, seeds, hash manifests)
- B. Keep it as a claim and a deliverable, but not a pass/fail success criterion — the initiative can succeed with the package incomplete
- C. Keep it as a success criterion only — verified in place, with no separate package produced
- D. Drop it entirely — reproducibility is not claimed, not measured, and not delivered; Q1 is corrected to "forecast result only"
- X. Other (please specify)

[Answer]: B. Keep it as a claim and a deliverable, but not a pass/fail success criterion — the initiative can succeed with the package incomplete

## Q14. Follow-up (contradiction): Q9 puts the thesis write-up chapter inside the product boundary, but Q11 lists only the pipeline, the trained model, and the evaluation report. Which is correct?

- A. Q11 is correct — the boundary is code and evidence only; the write-up is authored separately and is out of scope here
- B. Q9 is correct — add the thesis chapter as a fourth deliverable of this initiative
- C. Partly — this initiative produces the chapter's inputs (figures, tables, metrics, methods text) but not the chapter prose itself
- D. Not yet defined
- X. Other (please specify)

[Answer]: B. Q9 is correct — add the thesis chapter as a fourth deliverable of this initiative

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct

## Assumption Confirmation

Reset after the Q19 governance corrections. The Q15 disposition moved items 1-3 into scoped verification obligations and items 4-6 into governance dependencies; neither category is a retained assumption. The metrics/horizon assumption was resolved by Q16-Q19. One assumption remains:

1. Whether evaluation code exists yet is not established by any recorded answer; the sealing condition treats it as part of the G-05 frozen set regardless of its current state. (intent-statement.md)

- A. Accept assumptions
- B. Convert to follow-up questions

[Answer]: B. Convert to follow-up questions

## Q20. Follow-up (assumption disposition): what is the current state of the December 2022 evaluation code that G-05 must freeze?

- A. None exists yet — the evaluation code is authored inside this initiative and frozen at G-05 before December is opened
- B. Partial — fragments exist (scripts or notebooks) and must be consolidated, reviewed and frozen at G-05
- C. Complete — the evaluation code already exists; only freezing, hashing and G-05 signature remain
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. None exists yet — the evaluation code is authored inside this initiative and frozen at G-05 before December is opened

## Q21. Governance correction record (board report GOV-2026-08-13-IC-02, verdict FAIL): how should findings GOV-13 to GOV-21 be dispositioned?

Findings raised against Vision v4.2 normative core, Technical Environment v3.2, and `evidence/DECISIONS.md`:

- GOV-13 (BLOCKER) success framework redefined to two pass/fail measures; reproducible artifacts demoted out of the Vision 5.3 project-completion layer; practical relevance (Vision 5.4) absent
- GOV-14 (BLOCKER) gridded-cell target described without the IPP-versus-station-zenith mismatch bound by Vision 2.5 to every IRI and GIM comparison
- GOV-15 (BLOCKER) Initiative Trigger declares the work unblocked while Technical Environment 1.5 records the Phase 1 source as Pending — D-144 and the signature table is blank
- GOV-16 (MAJOR) quiet/disturbed regime and observation-quality strata breakdowns omitted from the reporting contract (Vision 5.5, 9.3, 9.4, 9.5)
- GOV-17 (MAJOR) Hp60/ap60 absent from the driver contract despite Primary status and preference over Kp alone (Vision 7.5)
- GOV-18 (MINOR) external CODE final GIM contextual comparator absent from the model set (Vision 2.4 tier 4, 4.1)
- GOV-19 (MINOR) driver join semantics and two-source provenance obligation not recorded (D-9 consequences)
- GOV-20 (BLOCKER) stakeholder map records supervisor authority as non-gating, contradicting the Vision 1.2 freeze-gate rule
- GOV-21 (MINOR) superseded Q16/Q17/Q18 answers carry no in-place supersession marker

- A. Fix all blockers and majors; defer the minors to Requirements Analysis
- B. Fix blockers only
- C. Fix everything — apply all nine findings as written
- D. Stop; the student reviews the report and decides
- X. Other (please specify)

[Answer]: C. Fix everything — apply all nine findings as written

## Q15. Follow-up (assumption disposition): how should each retained assumption be dispositioned?

- A. Accept all six unchanged as labelled assumptions
- B. Resolve or precisely scope some, and reclassify the rest
- X. Other (please specify)

[Answer]: X. Record items 1-3 as resolved or precisely scoped. Treat items 4-6 as explicit governance dependencies. Do not open the December test set until the primary persistence baseline, metrics, horizons, and evaluation code are frozen.

## Q16. Which error metrics should the December 2022 evaluation report? (select all that apply)

- A. RMSE (TECU)
- B. MAE (TECU)
- C. Skill score relative to the persistence baseline, as a percentage improvement
- D. Correlation coefficient between forecast and observed
- E. Not yet defined
- X. Other (please specify)

> **Superseded by Q19** (GOV-03, GOV-04, GOV-05). The recorded answer stands as the historical record; the primary metric is RMSE and the primary estimand is the paired loss differential.

[Answer]: X. December 2022 evaluation will use MAE as the primary metric. Required secondary measures are RMSE, signed mean bias, RMSE skill score against the frozen persistence baseline, Pearson correlation, and P95 absolute error. Results will be reported by cell and forecast horizon and as an equal-cell macro-average, with day-block 95% confidence intervals. MAPE is excluded.

## Q17. Which forecast horizons should the model produce and be evaluated at? (select all that apply)

- A. +1 hour
- B. +3 hours
- C. +6 hours
- D. +24 hours
- E. Not yet defined
- X. Other (please specify)

> **Superseded by Q19** (GOV-02). The recorded answer stands as the historical record; +1 h is the sole confirmatory horizon and +24 h is an optional post-completion extension.

[Answer]: X. The model shall generate direct hourly VTEC forecasts for lead times h=1,...,6 hours. All six horizons will be evaluated on December 2022, with 1-, 3-, and 6-hour results highlighted. Six-hour MAE and persistence skill are the primary endpoints. Forecasts beyond six hours are outside the thesis scope. No future-observed VTEC or driver values may be used.

## Q18. How should metrics be reported across the three cells and across time?

- A. Per cell, aggregated over the whole test month
- B. Per cell per horizon, aggregated over the whole test month
- C. Per cell per horizon, plus a separate breakdown for geomagnetically disturbed hours vs quiet hours
- D. Not yet defined
- X. Other (please specify)

> **Partly superseded by Q19** (GOV-02) and extended by Q21 (GOV-16). The per-horizon portion is void; the equal-cell macro-average, per-cell reporting, common mask and block-bootstrap portions stand.

[Answer]: X. December metrics shall be reported separately for ARUC, BSHM and NICO at every 1-6 h horizon. The headline cross-cell result shall be an equal-cell macro-average; pooled row-weighted results are supplementary only. Full-month metrics are primary, accompanied by daily MAE and four local-solar-time diagnostic bins. All model-baseline comparisons shall use identical paired valid timestamps and report sample count and coverage. Uncertainty shall be estimated with paired UTC-day block bootstrap confidence intervals.

## Q19. Governance correction record (board report GOV-2026-08-13-IC-01, verdict FAIL): how should findings GOV-01 to GOV-12 be dispositioned?

Findings raised against Vision v4.2 normative core and Technical Environment v3.2:

- GOV-01 IRI-2016 benchmark absent from the framing (Vision 2.3, 2.4, 4.2)
- GOV-02 horizon widened to h=1..6; Vision 8.1 and D-103 fix +1 h confirmatory
- GOV-03 primary estimand replaced by persistence skill; Vision 2.3 fixes paired loss differential
- GOV-04 primary metric changed to MAE; Vision 5 fixes RMSE
- GOV-05 seasonal persistence and climatology omitted; Vision 2.4 M-01/M-02/M-03 mandatory
- GOV-06 sealing condition weaker than G-05
- GOV-07 Dst diagnostic-only status and F10.7 trailing 81-day mean absent (D-116)
- GOV-08 D-144 countersign asserted but signature table on disk is blank
- GOV-09 source register under-declares its own citations
- GOV-10 two assertions carry unsupporting source tags
- GOV-11 thesis chapter deliverable untestable as scoped
- GOV-12 reproducibility non-blocking status not cross-referenced to G-07

- A. Apply every board recommendation as written
- B. Apply a subset, naming which
- C. Reject the board findings
- X. Other (please specify)

[Answer]: A. Apply every board recommendation as written. GOV-02 supersedes the Q17 horizon answer and the per-horizon portion of the Q18 reporting answer; GOV-03 and GOV-04 supersede the Q16 primary-metric and primary-endpoint answers; GOV-05 extends the Q16 baseline set; GOV-11 narrows the Q14 chapter deliverable to chapter inputs. GOV-08 is applied as the interim state only: the Phase 1 source is recorded as approved-pending-record until the countersign is entered in evidence/DECISIONS.md by the student or supervisor.
