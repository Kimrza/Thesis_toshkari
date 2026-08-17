# Initiative Brief — Hourly VTEC Forecasting (TEC_Project Phase 1 onward)

**Decision requested:** approve the Ideation phase and hand off to Inception.
**Recommendation: GO, with two entry conditions.**
**Audience:** the student and thesis author, as a working decision record `[Q6]`. Written so that a reader who was not present can follow it.

## Sources

- `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/intent-capture/intent-statement.md` — problem, driver contract, success layers, primary estimand, reporting contract, sealing condition, confirmed deliverable set.
- `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/intent-capture/stakeholder-map.md` — who decides what, and which authority is the supervisor's.
- `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/feasibility/feasibility-assessment.md` — capability verdicts, environment, compliance, timeline, gating conditions, verification obligations.
- `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/feasibility/constraint-register.md` — the constraints this initiative is built under.
- `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/feasibility/raid-log.md` — risks, issues, dependencies.
- `[Q1]`–`[Q10]` — confirmed answers in `approval-handoff-questions.md`.
- Authority: `Project Vision and Research Definition` v4.2 and `Technical Environment and Research Implementation` v3.2, both under `PreFlight/`.
- Governance: `governance/reviews/GOV-2026-08-15-FE-01.md`, `GOV-2026-08-15-FE-02.md`.

`market-research`, `scope-definition`, `team-formation` and `rough-mockups` are not executed in this workflow, so no `competitive-analysis`, `scope-document`, `intent-backlog`, `team-assessment` or `wireframes` exists. Their absence is a property of how much process this initiative needs, not a gap in the brief.

## Intent and Problem

Two joined problems: produce a defensible hourly VTEC forecast for three frozen cells as the empirical core of a thesis, and demonstrate that a governed, reproducible pipeline can be built end to end. The forecast result is the primary claim; reproducibility is the supporting one.

The work is to obtain Kp and ap3 plus Hp60 and ap60 from GFZ, hourly Dst from Kyoto WDC, and observed F10.7 from Canada's Solar Radio Monitoring Program; align them onto the hourly grid without interpolation; define availability timestamps and lag every predictor against forecast leakage; then build the hourly VTEC model on ARUC 40/44, BSHM 32/35 and NICO 35/33 for calendar 2022, with December 2022 held as the locked test set.

The confirmatory comparison is an independently trained local LSTM against the IRI-2016 empirical benchmark, which is architecturally excluded from the model and joined only at evaluation. The primary estimand is the paired loss differential, IRI squared loss minus LSTM squared loss, so a positive value favours the LSTM.

## Market Validation

Not applicable and not claimed. This is thesis research, not a product; `market-research` is out of scope for this workflow and no market claim is made anywhere in this brief.

## Feasibility and Risk Highlights

The feasibility assessment returns **feasible**. The binding constraint is calendar time against a largely serial chain that contains two supervisor signatures — not technical difficulty. No capability was found infeasible on the stated CPU-only Kaggle-plus-local environment.

What is already demonstrated: the Phase 1 VTEC record set exists and is audited — 223,586 rows, 365/365 days, three cells, twelve per-month SHA-256 manifests — and is promoted as the acquisition input under D-9 Option B, which removes a fresh ~17-hour acquisition run that would not fit a single Kaggle session.

What does not exist yet: the repository package, the pinned environment, the test suite, the evaluation code, IRI-2016 benchmark generation and the CODE GIM comparator retrieval. All are inside this initiative's boundary.

What is measurable but unmeasured: the Kyoto Dst grade span for 2022, the extent of the Canadian F10.7 outage beginning 2022-03-18, the IRI build and runtime cost on CPU, and environment parity between Kaggle and local.

Per `[Q3]`, all thirteen risks in `raid-log.md` carry forward as recorded, and this brief singles out none of them for special tracking. The three the assessment treats as the sharpest — an overturned D-9 or D-10 (R-01), building a leakage-free pipeline and full test suite from a near-empty repository inside one semester (R-02), and supervisor unavailability delaying G-05 (R-05) — are named here for the reader's orientation only, and carry no different status from the other ten.

Compliance exposure is narrow. All sources are public scientific measurements, so there is no personal, restricted or export-controlled data, no privacy impact assessment, no data-residency constraint, and no applicability of GDPR, HIPAA, PCI-DSS or SOC 2. What binds is attribution and licensing: CEDAR/Madrigal rules-of-the-road with permanent experiment citation, the Kyoto WDC non-commercial-use notice, GFZ and Canadian Solar Radio Monitoring Program acknowledgement, and a licence compatibility review of every third-party dependency before it is pinned.

## Scope Boundary

Confirmed unchanged from the intent statement `[Q2]`.

| Deliverable | Standing |
|---|---|
| Runnable acquisition, alignment and lagging pipeline producing the joined hourly dataset | In boundary |
| Trained model set and recorded configuration — persistence, seasonal persistence, climatology, ridge, Random Forest, compact LSTM | In boundary |
| Locked-December evaluation report against the primary estimand, with all three mandatory difficulty controls co-reported | In boundary |
| Reproducibility package — pinned environment, seeds, hash manifests | In boundary; inside the project-completion success layer and required for G-07 |
| Thesis chapter **inputs** — figures, tables, metrics, methods text | In boundary |
| Thesis chapter **prose** | **Out of boundary** — authored outside this initiative |

Frozen modelling target: hourly grid, three cells, calendar 2022, December 2022 locked. The three sites are correlated, not independent spatial samples, and the target is a provider-prepared gridded cell value rather than a zenith column above an antenna — a representativeness mismatch that is stated wherever a model-versus-IRI or model-versus-GIM comparison is reported.

**Claim exclusion carried from D-7.** The hourly grid is a decision with a consequence: NICO holds 53.8% of its native 5-minute slots against 96.4% of its hourly bins, so any scientific question requiring 5-minute resolution is out of reach for NICO on this dataset and **must not be claimed**. Claims are bounded per D-8 to hourly VTEC forecasting at the three frozen cells for calendar 2022, tested on December 2022, with no generalisation beyond these cells, this year, or this test month.

## Concept Visuals

None. `rough-mockups` is out of scope for this workflow; there is no user interface in the deliverable set.

## Team Plan

One author and one countersigning supervisor `[Q7]`. No mob composition, no role split, no staffing schedule.

| Party | Role | Authority |
|---|---|---|
| Student / thesis author | Decision-maker | Decides scope and priority alone; the supervisor countersigns after the fact |
| Supervisor | Decision-maker at freeze gates only | Does not gate day-to-day scope and priority. **Does** gate every freeze gate: D-144 Phase 1 source adoption (satisfied 2026-08-15), G-05 experiment freeze, G-06 locked evaluation, G-07 final reproducibility acceptance, G-P2, G-P3, and the final claims decision |
| Examining committee | Accepts or rejects the final claims | Requirements of its own are Unknown, tracked as a dependency |

Neither the governance board process nor the data providers hold decision authority; both are influencers.

## Entry Conditions for Inception

`[Q5]` as resolved at `[Q10]`. These are **hard**: Inception's first stage does not run until both are satisfied.

| # | Condition | Status | Why it gates |
|---|---|---|---|
| EC-1 | The two data audits are complete — the Kyoto Dst grade span recorded for 2022-01-01 to 2022-12-31, and the Canadian F10.7 archive audited from 2022-03-18 with exact missing dates and any qualifiers or reconstructed values | **SATISFIED 2026-08-15** — `evidence/audit_ec1_2026-08-15/EC1-AUDIT.md`, fifteen files hashed, reproducible via `scripts/audit_ec1_drivers.py` | Both are acquisition-freeze inputs already carried by the intent statement, and the F10.7 result can change how the gap is handled, which is upstream of every model using F10.7 as a feature |
| EC-2 | The three intent-capture governance board reports (GOV-2026-08-13-IC-01, IC-02, IC-03) are persisted under `governance/reviews/` | **OPEN** | Closes GOV-25. The three feasibility and handoff reports are already filed; the directory otherwise misrepresents the review history |

**What EC-1 returned.** Dst is single-grade provisional across all twelve months of 2022, with 365/365 days and no final grade in existence — so no grade mixing is possible. The F10.7 result inverts the premise the condition was written on: the archive has **zero missing dates in 2022**, and the documented March 2022 outage does not appear as a gap. No imputation is needed. What the audit found instead is four flare-contaminated readings and five duplicate-timestamp days, and through them a decision nobody had recorded — which of the three daily readings is *the* observed daily F10.7 value, given that three of the four contaminated readings sit at 20 UT, the conventional choice. That decision belongs in the frozen feature contract at G-04, and is tracked as I-13 with residuals EC1-R-1 through EC1-R-4 in the audit report.

**Not an entry condition:** the GC-01 repository scaffold. It keeps its stated role as the precondition for **acquisition**, because Inception's stages — practices discovery, requirements analysis, application design, units generation, delivery planning — are the work that determines what the repository should contain `[Q10]`.

**Owner and checkpoint.** The student owns both conditions, and the checkpoint is the first prompt of Inception's first stage: the workflow advances on this stage's approval and cannot itself enforce EC-1 or EC-2, so they are checked there rather than left to memory.

## Open Supervisor Gates Carried Into Inception

Vision §13.1 records twelve gates, of which none is yet signed. They are listed here so the handoff carries the whole set rather than only the two that touch the critical path most visibly. **Requirements Analysis (2.3) owns giving each a stable requirement ID; NFR Requirements (3.2) owns assembling the G-05 freeze manifest.** This brief enumerates, it does not schedule.

| Gate | Approver | Status in Vision §13.1 | Due |
|---|---|---|---|
| G-01 Scientific framing | Supervisor | Pending sign-off | Before implementation freeze. **Evidence includes the decision log produced by this stage** (`decision-log.md`) |
| G-02 Station/data viability | Supervisor consulted | Open | Before package freeze |
| G-03 GNSS target | Supervisor | Open | Before full-year processing — Phase 2 relevant |
| G-04 Feature safety | Supervisor for ambiguous inputs | Open | Before model tuning |
| G-05 Experiment freeze | Supervisor | Open | Before December access — dependency D-02 |
| G-06 Locked evaluation | Student | Blocked | After G-05 |
| G-07 Reproducibility | Supervisor / reviewer | Blocked | Before thesis submission — dependency D-03 |
| G-08 Claims | Supervisor | Blocked | Before thesis submission |
| G-09 Agent preflight | Supervisor | Open | Before any affected component is coded |
| G-P1 Prepared-data MVP | Supervisor | Blocked — ICTP failed, replacement pending | Before the phase transition |
| G-P2 Phase transition | Supervisor | Blocked | Before Phase 2 raw processing |
| G-P3 Raw-target acceptance | Supervisor | Blocked | Before Phase 2 model training |

## Open Dependency Carried Into Inception

Change request **D-09** — the Vision §4.4 clause constraining the design to beginner-to-intermediate Python implementation capacity — is **closed as of 2026-08-15**. The supervisor countersigned the §15.2 change request, recorded as reported by the student, and the clause no longer constrains the design. `[Q4]` carried it into Inception as an open dependency; that carry is discharged before Inception begins.

One documentation gap remains from it, tracked at `raid-log.md` I-12: the Vision document text still shows the pre-amendment §4.4 wording and carries no v4.3 change-history row, so a reader of the Vision alone sees the superseded clause. Applying the change record to the Vision runs through §15.2 and is not this workflow's to do. No signature artifact is filed in the repository, matching how D-3/D-144 is recorded.

## Go / No-Go Recommendation

**GO** `[Q1]`, subject to EC-1 and EC-2.

The recommendation rests on four things. The Phase 1 source is approved and its data already exists in audited form, so the largest single execution risk is retired before Inception begins — with the qualification recorded at `raid-log.md` I-07 and I-10 that Technical Environment §1.5 still reads *Pending — D-144* and Vision §13.1 still records G-P1 as blocked, so acquisition would execute on the strength of the decision record ahead of the implementation authority's update. The scientific design is fixed and governance-corrected, so Inception inherits its parameters rather than re-deriving them. The compliance surface is narrow and fully identified. And the two remaining unknowns that could change the shape of the work — the Dst grade span and the F10.7 outage extent — are exactly what EC-1 requires be measured before Inception starts, so the phase does not begin on top of an unmeasured input.

The honest caveat is the one the feasibility assessment names: the schedule has little slack for an overturned decision or a signature delay, and neither is inside this initiative's control. Nothing in Ideation can fix that; the mitigation available is sequencing, and the assessment recommends assembling the G-05 freeze manifest as early as the plan allows so the signature wait overlaps with model work rather than following it.

## Assumptions & Open Questions

None. Every uncertainty is registered as a verification obligation this initiative owns (V-01 to V-08 in `feasibility-assessment.md`), a governance dependency owned outside it (D-01 to D-10dep in `raid-log.md`), or an entry condition above. Per `[Q9]`, nothing is recorded as explicitly deferred beyond what the RAID log already carries.
