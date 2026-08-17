# Feasibility & Constraints — Questions

**Stage:** feasibility
**Depth:** Comprehensive

## Sources

- Upstream: `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/intent-capture/intent-statement.md` (approved 2026-08-13, amended 2026-08-15)
- Workspace survey (2026-08-13): `notebooks/madrigal_phase1_coverage_audit.ipynb`, `scripts/merge_coverage_year.py`, `evidence/audit_evidence_2022-{01..12,FULL}/`. No `src/` package, no environment lock file, no test suite present.
- Governance change (2026-08-15): **D-3/D-144 is countersigned by the supervisor and recorded** in `evidence/DECISIONS.md`. Phase 1 acquisition is no longer blocked. D-9 and D-10 remain sole-signed, and Technical Environment v3.2 §1.5 still reads *Pending — D-144* until updated through Vision §15.2 change control. Q1, Q2 and Q12 below were rewritten on 2026-08-15 to match; Q3–Q11 are unchanged from the 2026-08-13 draft.
- External findings (2026-08-15, web): the Penticton/DRAO F10.7 outage beginning 2022-03-18 is a documented month-long interruption caused by a cyberattack on the NRC network (Elvidge & Themens, *Space Weather*, 2023). CDDIS discontinued anonymous FTP in October 2020; IONEX retrieval requires an Earthdata Login. `iri2016` requires a Fortran compiler and builds on first run. Kaggle CPU sessions run 12 hours with 30 GB RAM.

Every question below is answerable with a "not yet defined" or "none" option where that is the honest answer. Do not select invented detail.

## Q1. D-3/D-144 is countersigned as of 2026-08-15, so Phase 1 acquisition is no longer blocked. What should lead?

- A. Acquisition first — execute Phase 1 under D-9 Option B immediately, then build the pipeline around the acquired dataset
- B. Pipeline scaffolding first — repository structure, pinned environment and test suite before any acquisition, so the acquired data lands in a governed pipeline
- C. In parallel — acquisition and scaffolding proceed together as independent tracks
- D. Not yet defined
- X. Other (please specify)

[Answer]:B

## Q2. D-9 chose Option B: promote the audited calendar-2022 record set (223,586 rows, 365/365 days, three cells, twelve per-month SHA-256 manifests) to acquisition input rather than re-running a fresh ~17-hour acquisition. D-9 notes Option A "remains available if a reviewer requires every byte of the dataset to trace to a single acquisition run with a single manifest." Now that the source is approved, which stands?

- A. Option B stands — use the promoted audit set; the twelve independent manifests are stronger provenance than one fresh run
- B. Switch to Option A — re-run the full-year acquisition now that approval exists, so provenance traces to a single acquisition run
- C. Both — keep the promoted set as the working input and schedule a single-run re-acquisition as a later verification step
- D. Not yet defined
- X. Other (please specify)

[Answer]:A

## Q3. What is the actual execution environment, and is a CPU-only path genuinely required?

- A. Kaggle as primary compute plus a local machine for development and cross-check, with the full workflow feasible on CPU and GPU as an optional accelerator only
- B. Local machine only
- C. Kaggle only
- D. Not yet defined
- X. Other (please specify)

[Answer]:A

## Q4. There is currently no environment lock file, no `src/` package, and no test suite in the repository — only one audit notebook and one merge script. How should that gap be treated?

- A. As a first-class construction task: the repository structure, pinned environment and test suite are built as part of this initiative before any modelling
- B. As a prerequisite to be completed before this workflow reaches Construction, tracked as a dependency but built outside it
- C. As acceptable — work continues in notebooks and the packaging question is deferred
- D. Not yet defined
- X. Other (please specify)

[Answer]:A

## Q5. Which of these acquisition paths carry real technical uncertainty for you, as opposed to being routine? (select all that apply)

- A. Madrigal VTEC retrieval (`madrigalWeb` client, experiment/kindat discovery, parameter pinning) — unblocked by the D-144 countersign; the uncertainty is technical, not governance
- B. GFZ indices — Kp, ap3, and the Hp60/ap60 hourly series
- C. Kyoto WDC hourly Dst, including its provisional grade and non-commercial-use notice
- D. Canada's Solar Radio Monitoring Program observed F10.7, including the archive gap from 2022-03-18
- E. None of these are uncertain — all four are routine retrievals
- X. Other (please specify)

[Answer]:A,D,C

## Q6. The evaluation needs IRI-2016 values as the benchmark and CODE final GIM as the contextual comparator, both joined at evaluation time. What is the state of that capability?

- A. Neither exists yet; both must be built, and the IRI runtime cost on CPU is unmeasured
- B. IRI generation is understood; the GIM retrieval is not
- C. Both are understood and routine
- D. Not yet defined
- X. Other (please specify)

[Answer]:A

## Q7. What compliance and licensing obligations bind this work? (select all that apply)

- A. CEDAR/Madrigal rules-of-the-road, permanent experiment citation and acknowledgement
- B. Kyoto WDC Dst non-commercial-use notice and citation
- C. GFZ and Canadian Solar Radio Monitoring Program citation and acknowledgement
- D. University or supervisor requirements on data handling, authorship or publication
- E. Licence compatibility review for any third-party code reused in the pipeline
- F. None beyond ordinary academic citation
- X. Other (please specify)

[Answer]:A, B, C, E

## Q8. Is any personal, restricted or export-controlled data involved?

- A. No — all sources are public scientific measurements with citation obligations only
- B. Yes, in some form (please specify under X)
- C. Not yet defined
- X. Other (please specify)

[Answer]:A

## Q9. What is the timeline constraint, concretely?

- A. One academic semester, with the empirical chapter due at its end
- B. A specific dated deadline (please give the date under X)
- C. No fixed external deadline; the constraint is the supervisor's availability
- D. Not yet defined
- X. Other (please specify)

[Answer]:A

## Q10. What is the implementation skill profile this work must fit?

- A. Beginner-to-intermediate Python; the design should favour readable, conventional code over sophistication
- B. Comfortable intermediate Python including pandas, numpy and Keras
- C. Advanced — no capability constraint on the design
- D. Not yet defined
- X. Other (please specify)

[Answer]:C

## Q11. Beyond the recorded supervisor unavailability, are there organisational blockers?

- A. None beyond the supervisor countersign dependency already recorded
- B. Competing academic obligations that will interrupt this work
- C. Institutional access or approval processes not yet started
- D. Not yet defined
- X. Other (please specify)

[Answer]:A

## Q12. What is the single greatest feasibility risk in your own judgement — the thing most likely to stop this initiative?

- A. The remaining unsigned decisions (D-9 acquisition route, D-10 driver sources) being overturned on review, invalidating work already built on them
- B. Data gaps (the F10.7 outage, Dst grade, or cell coverage) proving worse than the audit suggests
- C. Building a correct, leakage-free pipeline and a full test suite from a near-empty repository within the timeline
- D. The model producing a negative or inconclusive result against IRI-2016
- E. Not yet defined
- X. Other (please specify)

[Answer]:C,D,B

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct

## Q13. Governance review GOV-2026-08-15-FE-01 returned FAIL. Its blocker: the drafted artifacts record "no capability ceiling constrains the design" from Q10, while Vision v4.2 §4.4 states "Beginner-to-intermediate Python implementation capacity" as normative core. How should this be resolved?

- A. Remediate inside this stage — restate the Vision §4.4 constraint as binding and inherited, record the Q10 answer as author capability context that does not lift it, and fix the four MAJOR and two MINOR findings; then re-review before the approval gate
- B. Pause this stage and take the capacity clause to the supervisor as a Vision §15.2 change request before anything is rewritten
- C. Both tracks — remediate as in A now, and raise the §15.2 change request in parallel, recorded as an open governance dependency
- D. Not yet defined
- X. Other (please specify)

[Answer]: X. For GOV-F-01: "i choose records no capability ceiling on the design because i wanted to have the best outome possible even if my skill is advanceed". For GOV-F-02: "for kaggle i have 30hr limit". For GOV-F-03: "state that GC-01 supplements rather than replaces them and name the section." For GOV-F-04: "Extend V-04, or add a sibling obligation, naming the sample count, the tolerance-is-predeclared requirement, and iri_implementation_validation_report." For GOV-F-05: "Replace the completeness phrasing with an explicit scope sentence — this register covers feasibility-material constraints; the experiment-freeze parameter set is fixed by Vision §§ and assembled by stages 2.3 and 3.2." For GOV-F-06: "One sentence stating the start threshold does not narrow the critical-test set required at G-05 / G-07." For GOV-F-07: "One line in the RAID log recording that any acquisition executed before the §15.2 update proceeds on the decision record, and that the update is the closure evidence."

## Q14. Should the governance report GOV-2026-08-15-FE-01 be persisted under `governance/reviews/`? The directory exists and is empty; GOV-25 records that no board report has been persisted.

- A. Yes — write it now, beginning to close GOV-25
- B. No — keep it in conversation only for this pass
- C. Not yet defined
- X. Other (please specify)

[Answer]: A
