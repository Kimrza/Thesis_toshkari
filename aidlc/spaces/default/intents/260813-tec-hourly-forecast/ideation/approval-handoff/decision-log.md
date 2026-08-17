# Decision Log — Ideation Phase

Every decision taken across the Ideation phase of this initiative, drawn from three registers per `[Q8]`: the AI-DLC stage decisions, the D-series decisions in `evidence/DECISIONS.md` cross-referenced to them, and the governance board findings with their dispositions.

## Sources

- `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/intent-capture/intent-statement.md` and `.../intent-capture/stakeholder-map.md` — the intent-capture decisions.
- `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/feasibility/feasibility-assessment.md`, `.../feasibility/constraint-register.md` and `.../feasibility/raid-log.md` — the feasibility decisions.
- `evidence/DECISIONS.md` — D-1 through D-10, with the signature table.
- `governance/reviews/` — the two filed feasibility board reports; the three intent-capture reports are referenced in the intent statement but not yet filed (entry condition EC-2).
- `[Q1]`–`[Q10]` in `approval-handoff-questions.md` — this stage's decisions.

## 1. AI-DLC Stage Decisions

### Intent Capture (approved 2026-08-13, amended 2026-08-15)

| # | Decision | Source |
|---|---|---|
| IC-1 | The initiative solves two joined problems: a defensible hourly VTEC forecast as the thesis empirical core, and demonstration of a governed reproducible pipeline. The forecast is the primary claim; reproducibility is the supporting one | `[Q1]` |
| IC-2 | The customer is the student and thesis author, distinct from the wider stakeholder set | `[Q2]` |
| IC-3 | The student decides scope and priority alone; the supervisor countersigns after the fact, and gates every freeze gate | `[Q6]` `[Q21]` |
| IC-4 | Success is defined in three non-interchangeable layers — project completion, statistical evidence, practical relevance. A correct negative or inconclusive result is not a project failure | `[Q21]` |
| IC-5 | The primary estimand is the paired loss differential, IRI-2016 squared loss minus LSTM squared loss, positive favouring the LSTM, with a 95% confidence interval. Percentage reduction is derived and never confirmatory | `[Q19]` |
| IC-6 | IRI-2016 is a benchmark only and is architecturally excluded from the model; it is joined at evaluation time and nowhere else | `[Q19]` |
| IC-7 | The driver contract: Kp/ap3 as forecast features lagged ≥ 3 h; Hp60/ap60 preferred for cadence match, lagged ≥ 1 h; Dst diagnostic and hindcast-only; observed F10.7 lagged one day with a trailing 81-day mean; SSN removed | `[Q19]` `[Q21]` |
| IC-8 | Three difficulty controls — persistence, 24-hour seasonal persistence, fitted station × month × hour climatology — are mandatory and co-reported in the primary results table, with a binding honesty rule if any beats the LSTM | `[Q19]` |
| IC-9 | +1 h is the confirmatory horizon and the only one required; +24 h is optional and off the critical path | `[Q19]` `[Q17]` |
| IC-10 | The target is a provider-prepared gridded cell value, not a zenith column; the cell-versus-station representativeness mismatch is stated wherever a comparison is reported | `[Q21]` |
| IC-11 | Deliverable set confirmed: pipeline, model set, locked-December evaluation report, reproducibility package, thesis chapter inputs. Chapter prose is out of boundary | `[Q11]` `[Q13]` `[Q14]` |
| IC-12 | Reproducible artifacts sit inside the project-completion success layer; G-07 remains a mandatory full-board gate | `[Q13]` `[Q21]` |
| IC-13 | Assumptions are split into scoped verification obligations this initiative owns and governance dependencies owned outside it; nothing is retained as a flat assumption | `[Q15]` |
| IC-14 | **Amendment 2026-08-15** — D-3/D-144 is countersigned and recorded; the Phase 1 source is approved and acquisition is no longer blocked. D-9 and D-10 remain sole-signed and Technical Environment §1.5 still reads *Pending* | `[Q12]` |

### Feasibility & Constraints (approved 2026-08-15)

| # | Decision | Source |
|---|---|---|
| FE-1 | Pipeline scaffolding first: repository structure, pinned environment and test suite before any acquisition, so acquired data lands in a governed pipeline | `[Q1]` |
| FE-2 | D-9 Option B stands — the promoted audited record set is the acquisition input; the twelve independent per-month manifests are treated as stronger provenance than one fresh run. No re-acquisition is scheduled | `[Q2]` |
| FE-3 | Kaggle as primary compute plus a local machine, the full workflow feasible on CPU, GPU an optional accelerator only | `[Q3]` |
| FE-4 | The repository, environment and test suite are a first-class construction task inside this initiative, not a prerequisite built outside it | `[Q4]` |
| FE-5 | Genuine technical uncertainty is confined to Madrigal VTEC retrieval, the Canadian F10.7 archive and Kyoto Dst; the GFZ indices are routine | `[Q5]` |
| FE-6 | Neither IRI-2016 generation nor CODE GIM retrieval exists; both must be built and the IRI CPU cost is unmeasured | `[Q6]` |
| FE-7 | Binding obligations: CEDAR/Madrigal rules-of-the-road, the Kyoto non-commercial-use notice, GFZ and Canadian acknowledgement, and a third-party licence compatibility review | `[Q7]` |
| FE-8 | No personal, restricted or export-controlled data; all sources are public scientific measurements | `[Q8]` |
| FE-9 | Timeline is one academic semester with the empirical chapter due at its end | `[Q9]` |
| FE-10 | No organisational blockers beyond the recorded countersign dependency | `[Q11]` |
| FE-11 | Greatest feasibility risks, ranked: building a correct leakage-free pipeline and test suite from a near-empty repository within the timeline; a negative or inconclusive result against IRI-2016; data gaps worse than the audit suggests | `[Q12]` |
| FE-12 | **Post-review** — the Vision §4.4 implementation-capacity clause is recorded as binding until changed; the author's contrary position becomes the evidence for a §15.2 change request (D-09) rather than a change already made | `[Q10]` `[Q13]` |
| FE-13 | **Post-review** — the governance report is persisted under `governance/reviews/` | `[Q14]` |

### Approval & Handoff (this stage)

| # | Decision | Source |
|---|---|---|
| AH-1 | **Go** — Ideation is complete; proceed to Inception | `[Q1]` |
| AH-2 | The scope boundary carried into Inception is the intent statement's confirmed deliverable set, unchanged | `[Q2]` |
| AH-3 | All thirteen RAID risks carry forward as recorded; the brief singles out none for special tracking | `[Q3]` |
| AH-4 | Change request D-09 is carried into Inception as an open dependency; work proceeds under Vision §4.4 as written meanwhile | `[Q4]` |
| AH-5 | Two hard entry conditions gate Inception's first stage: the two data audits (EC-1) and persistence of the three intent-capture board reports (EC-2). The GC-01 scaffold is **not** an entry condition and keeps its role as the acquisition precondition | `[Q5]` `[Q10]` |
| AH-6 | The initiative brief is a working document for the author | `[Q6]` |
| AH-7 | The team is one author and one countersigning supervisor; no other party | `[Q7]` |
| AH-8 | This decision log draws on the AI-DLC stage decisions, the D-series decisions and the governance findings together | `[Q8]` |
| AH-9 | Nothing is recorded as explicitly deferred beyond what the RAID log carries | `[Q9]` |

## 2. D-Series Decisions, Cross-Referenced

From `evidence/DECISIONS.md`, decided 2026-08-13 by the student. Signature status is read from that document's signature table.

| ID | Decision | Countersigned | Where it binds this initiative |
|---|---|---|---|
| D-1 | A station maps to the 1°×1° Madrigal bin at its lower-left floor corner, `cell = (floor(lat), floor(lon))`, half-open on both axes | No | Fixes the three cells named in IC-10 and constraint TC-17 |
| D-2 | Coverage gate: ≥ 95% of calendar days present per month per cell, and 100% of December days (31/31) | No | The gate the promoted record set passes; underpins FE-2 |
| D-3 / D-144 | Phase 1 source replacement — the audited Madrigal MAPGPS set | **Yes, 2026-08-15 (recorded)** | The countersign that unblocked acquisition; IC-14. Recorded as reported by the student, with no signature artifact filed |
| D-4 | Acquire `ut1_unix, gdlat, glon, tec, dtec, kp, dst, f10.7, ap3` | No | Superseded in part by D-10's driver-source corrections; see below |
| D-5 | Gaps stored as explicit NaN; no interpolation, smoothing or filling at acquisition time. Imputation is a downstream modelling decision, recorded separately | No | The acquisition-time half of constraint TC-09; also why the F10.7 gap cannot be filled before it is measured (TC-20) |
| D-6 | Cite the standard MAPGPS reference plus the date range used, with the CEDAR Madrigal acknowledgement, rather than per-day permanent experiment citations | No | Gives obligation C-01 and V-07 their concrete form |
| D-7 | The model is built on an **hourly** grid; native 5-minute binning is aggregated before modelling. Evidence: hourly completeness 96.4–99.9% per cell against 53.8–89.9% at 5 minutes, with no gap anywhere exceeding 2.6 h | No | Fixes the modelling resolution the whole initiative assumes. **Consequence recorded:** any question requiring 5-minute resolution is out of reach for NICO and must not be claimed |
| D-8 | Claims are limited to hourly VTEC forecasting at the three frozen cells for calendar 2022, tested on December 2022. No generalisation beyond these cells, this year, or this test month | No | The claim boundary the governance overlay enforces; consistent with IC-10 and TC-18 |
| D-9 | Acquisition route: promote the audited rows; drivers from canonical sources | No | FE-2 keeps Option B. **Its own signature row is blank — this is risk R-01** |
| D-10 | Correction and addendum to D-9: driver sources, alignment and leakage control | No | The source of the driver contract at IC-7. **Also blank — R-01** |

**Cross-register note.** D-4's parameter list is the acquisition-time field set; D-10 then corrects *where the drivers come from* — Kp/ap3 from GFZ, hourly Dst from Kyoto WDC, observed F10.7 from Canada — rather than taking the co-located HDF5 columns as the modelling drivers. Where the two appear to differ, D-10 governs, and the driver contract in the intent statement is the operative statement.

## 3. Governance Board Findings and Dispositions

### Intent Capture

| Report | Verdict | Disposition |
|---|---|---|
| GOV-2026-08-13-IC-01 | FAIL, findings GOV-01 to GOV-12 | Every recommendation applied as written, recorded at `[Q19]` |
| GOV-2026-08-13-IC-02 | FAIL, findings GOV-13 to GOV-21, full board | All nine applied as written, recorded at `[Q21]`. Blockers were the redefined success framework, the undocumented cell-versus-station mismatch, an "unblocked" claim against a Pending D-144, and supervisor authority recorded as non-gating |
| GOV-2026-08-13-IC-03 | CONDITIONAL PASS, full board | All IC-02 findings verified closed. Residual: blank signature rows (GOV-22), absent G-05 signature (GOV-23), unmeasured Dst span and F10.7 outage (GOV-24), board reports not persisted (GOV-25) |

An advisory product-lead review of the same artifact set returned NOT-READY with three findings, recorded in the intent statement's `## Review` section and carried to the human at that stage's gate. GOV-15 and GOV-22 are superseded in part by the 2026-08-15 countersign.

**These three reports are not yet filed under `governance/reviews/`.** That is entry condition EC-2.

### Feasibility

| Report | Verdict | Disposition |
|---|---|---|
| GOV-2026-08-15-FE-01 | FAIL — one blocker, four major, two minor | Blocker: the artifacts recorded the absence of the Vision §4.4 capacity constraint. Major: the ~10 GB storage envelope absent; scaffold inputs diverging from the governed environment structure; the IRI validation-report obligation omitted; an over-claim of register completeness. All dispositioned by the student at `[Q13]` |
| GOV-2026-08-15-FE-02 | **CONDITIONAL PASS** | Blocker and all six other findings closed against verifiable text. Six non-blocking residuals with owners: GOV-R-01 the unraised §15.2 change request, GOV-R-02 the unrecomputed manifests, GOV-R-03 the unmeasured Dst span and F10.7 outage, GOV-R-04 the unestablished GIM route, GOV-R-05 the unpersisted intent-capture reports, GOV-R-06 the pending Technical Environment corrections |

One reviewer disagreement is maintained rather than resolved: whether Vision §4.4's capacity clause understates this project's real capacity. It is now the substance of change request D-09. Governing clause: Vision §1.2 and §15.2.

The boards recommend only. Neither grants academic approval nor authorises locked-test access; the student and supervisor remain the deciding authority.

## 4. Standing of This Log as Gate Evidence

Vision §13.1 lists G-01 Scientific framing's required evidence as "Sections 2, 4, 5 and **decision log**". **This document is that decision log.** It is recorded here so the link is visible rather than inferred; G-01 remains Pending sign-off and this log does not advance it by itself.

## 5. Governance Review of This Stage

`governance/reviews/GOV-2026-08-15-AH-01.md` — adaptive board, five seats active, verdict **CONDITIONAL PASS**. No blocker. Five MINOR findings and one NOTE, all applied to the handoff package before the approval gate: the open-gate enumeration (AH-F-01), the D-7 claim exclusion in the brief (AH-F-02), this section (AH-F-03), the phase-check verdict wording (AH-F-04), the entry-condition owner and checkpoint (AH-F-05), and the qualification on the retired-risk phrasing (AH-F-06).

## Assumptions & Open Questions

None. This log records decisions already taken. Open items live in `raid-log.md` as risks, issues and dependencies, and in `feasibility-assessment.md` as verification obligations.
