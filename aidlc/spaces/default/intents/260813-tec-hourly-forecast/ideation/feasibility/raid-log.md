# RAID Log — Hourly VTEC Forecasting (TEC_Project Phase 1 onward)

Risks, Assumptions, Issues, Dependencies. Opened at the Feasibility & Constraint Analysis stage, 2026-08-15; maintained from here on.

## Sources

- Upstream: `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/intent-capture/intent-statement.md` (approved 2026-08-13, amended 2026-08-15).
- Siblings: `feasibility-assessment.md`, `constraint-register.md` (this stage).
- `[Q1]`–`[Q12]`: confirmed answers in `feasibility-questions.md`. `[survey]` workspace survey, 2026-08-15. `[web]` external findings recorded in the questions file, 2026-08-15.

Market research was not executed, so no `competitive-analysis`, `market-trends` or `build-vs-buy` artifact is consumed.

Scoring: **Likelihood** and **Impact** are Low / Medium / High. Impact is judged against the intent statement's three success layers — project completion, statistical evidence, practical relevance — and a risk to the *claim* is scored differently from a risk to *completion*, because a correct negative result is not a project failure.

## Risks

The user's own ranking of the greatest feasibility risk was, in order: R-02, then R-03, then R-04 `[Q12]`. R-01 is ranked first here on governance exposure rather than contradicting that; the two orderings answer different questions, and both are recorded.

| ID | Risk | Likelihood | Impact | Layer at risk | Treatment | Owner |
|---|---|---|---|---|---|---|
| R-01 | D-9 (acquisition route) or D-10 (driver sources) is overturned on supervisor review, invalidating work built on it | Medium | High | Completion | **Mitigate.** Keep each decision individually reversible as `evidence/DECISIONS.md` already does; seek countersign in parallel with the work rather than after it; keep acquisition and alignment code parameterised so a source change is a configuration change, not a rewrite | Student + supervisor |
| R-02 | A correct, leakage-free pipeline with a full test suite cannot be built from a near-empty repository inside one semester | Medium | High | Completion | **Mitigate.** `[Q1]`/`[Q4]` already front-load the scaffold, which is the right treatment. Bound GC-01's test input to one executing leakage test rather than a full suite, so acquisition is not blocked behind a complete harness; grow the suite alongside each pipeline stage | Student |
| R-03 | The model produces a negative or inconclusive result against IRI-2016 | Medium | Low–Medium | Statistical evidence only | **Accept.** The intent statement's three-layer success framework makes this an outcome, not a failure; the binding honesty rule already governs how it is reported. No schedule or design change is warranted, and pursuing a positive result by other means would be the actual failure | Student |
| R-04 | Data gaps — the F10.7 outage, the Dst grade, or cell coverage — prove worse than the audit suggests | **Retired 2026-08-15** | — | — | **Closed by measurement.** Both driver audits ran (`evidence/audit_ec1_2026-08-15/EC1-AUDIT.md`): F10.7 has zero missing dates in 2022 and Dst is single-grade provisional across all twelve months. The risk did not materialise — it inverted. What replaces it is narrower and is tracked as I-13: not missing data, but an unfrozen selection rule over data that is all present | Student |
| R-05 | Supervisor unavailability delays G-05, pushing the December evaluation past the semester boundary | Medium | High | Completion | **Mitigate by sequencing.** Assemble and submit the G-05 freeze manifest as early as the workflow allows so the wait overlaps with model work rather than following it. The manifest is owned by stage 3.2; this log records only the schedule exposure | Student + supervisor |
| R-06 | The G-07 reproducibility package is assembled late and fails the full-board gate | Low–Medium | High | Completion | **Mitigate.** Build the package incrementally from the first commit — pinned environment, seeds and hash manifests are all GC-01 or early-pipeline outputs, not end-of-project work | Student |
| R-07 | The pinned environment does not restore identically on Kaggle and locally, so results differ by machine | Medium | Medium | Completion | **Mitigate.** Verify parity early (V-05) and record any divergence rather than resolving it silently; keep the environment specification the single source of truth for both | Student |
| R-08 | The `iri2016` Fortran build or per-call runtime turns out costly enough to disrupt session planning | Low | Low–Medium | Completion | **Mitigate by measurement (V-04).** Volume is small — 2,232 evaluations for locked December, 26,280 for the full year — so this is a scheduling nuisance rather than a blocker; cache IRI output per evaluation run if measurement warrants | Student |
| R-09 | The CODE final GIM retrieval route requires credentials or access not yet provisioned, delaying the contextual comparison | Low–Medium | Low | Evidence (contextual only) | **Mitigate.** Establish the route and provision any Earthdata Login early (V-03). Impact is bounded: the GIM is a contextual comparator, not the confirmatory benchmark | Student |
| R-10 | A third-party dependency's licence proves incompatible after it has been pinned, forcing a late swap | Low | Medium | Completion | **Avoid.** Review licences before pinning, per RC-05 | Student |
| R-11 | An institutional data-handling, authorship or publication requirement surfaces late that `[Q7]` did not identify | Low | Medium | Completion | **Mitigate.** Confirm the absence explicitly (V-08); an unidentified requirement and an absent one are indistinguishable until asked | Student + supervisor |
| R-12 | The distributed provenance of the promoted record set (twelve manifests, no single acquisition run) is challenged at examination | Low | Medium | Completion | **Mitigate.** Document the pinned query specification (V-01) and re-verify all twelve manifests (V-02). `[Q2]` records that Option A remains available if a reviewer requires single-run provenance, so a route back exists | Student |
| R-13 | Board reports are never persisted under `governance/reviews/`, weakening the audit trail at G-07 | Medium | Low–Medium | Completion | **Mitigate.** The directory exists and is empty `[survey]`; persisting each report as it is produced closes GOV-25 at near-zero cost | Student |

## Assumptions

**None retained.** Every uncertainty raised in this stage is registered either as a scoped verification obligation this initiative owns (V-01 to V-08 in `feasibility-assessment.md`) or as a dependency owned outside it (below). This follows the project rule that assumptions be split into obligations and dependencies rather than kept as one flat list, and matches how the intent statement already disposes of its own.

## Issues

Facts already true that constrain the work now. Distinct from risks, which may or may not occur.

| ID | Issue | Status | Consequence |
|---|---|---|---|
| I-01 | The repository has no `src/` package, no `tests/` tree and no dependency lock file; it contains one audit notebook and one merge script `[survey]` | Open | The whole foundation is work item one, per TC-06 |
| I-02 | No evaluation code exists; it must be authored, reviewed and frozen inside the G-05 set before December opens | Open | Carried from the intent statement (obligation 5) |
| I-03 | Neither IRI-2016 benchmark generation nor CODE GIM retrieval exists, and IRI CPU runtime is unmeasured `[Q6]` | Open | Covered by V-03 and V-04 |
| I-04 | The Canadian F10.7 archive has a documented month-long outage from 2022-03-18, caused by a cyberattack on the NRC network `[web]` | **Closed 2026-08-15 — measured, and the premise did not hold.** The archive has zero missing dates in 2022; the outage is not present as a gap. See `evidence/audit_ec1_2026-08-15/EC1-AUDIT.md` | No imputation is needed because nothing is missing. Whether outage-window values are original measurements is not determinable from `fluxtable.txt`, which carries no provenance column — carried as EC1-R-4 |
| I-05 | Kyoto Dst for 2022 is provisional grade and carries a non-commercial-use notice | **Grade span closed 2026-08-15** — provisional for all twelve months, final grade non-existent, 365/365 days. **Notice still open**: not located on any page retrieved, carried as EC1-R-1 | Bounded: Dst is diagnostic-only (TC-11), so a later grade change cannot disturb the primary estimand |
| I-13 | The driver contract fixes F10.7 as the previous-day observed value but does not state which of the three daily readings is the daily value. The EC-1 audit shows the choice is consequential: three of four flare-contaminated readings in 2022 fall at 20 UT, the conventional daily reading, and 2022-10-23 carries two readings stamped 20 UT | Open | Must be decided and frozen at G-04 before G-05. Carried as EC1-R-2 and EC1-R-3 |
| I-06 | D-9 and D-10 signature rows are blank; the acquisition route and driver corrections are sole-signed | Open | Drives R-01 |
| I-07 | Technical Environment v3.2 §1.5 still reads *Pending — D-144* despite the countersign | Open | Corrected only via Vision §15.2 change control, outside this workflow |
| I-08 | `governance/reviews/` exists but is empty; board reports are not persisted `[survey]` | Open | GOV-25; drives R-13 |
| I-09 | The D-3/D-144 countersign is recorded as reported by the student, with no signature artifact filed in the repository | Open | Noted in the intent statement as something a filed artifact would strengthen |
| I-10 | Any acquisition executed before Technical Environment §1.5 is updated proceeds on the strength of the decision record in `evidence/DECISIONS.md`, while the subordinate implementation authority still reads *Pending — D-144*. The §15.2 update is the closure evidence for this issue | Open | Recorded so the ordering is deliberate and visible, not discovered later |
| I-11 | Vision §4.4 constrained the design to beginner-to-intermediate Python implementation capacity, against the author's position at `[Q10]` and `[Q13]` that no capability ceiling should apply | **Closed 2026-08-15** — the §15.2 change request was countersigned by the supervisor; OC-09 in the constraint register is amended accordingly |
| I-12 | The `PreFlight/vision_document(3)(2)(2).md` text still carries the pre-amendment §4.4 capacity clause and has no v4.3 change-history row, so a reader of the Vision alone sees the superseded wording | Open | Closure evidence: the §15.2 change record applied to the Vision document. Same shape as I-07, which is the equivalent gap for Technical Environment §1.5 |

## Dependencies

Owned outside this initiative. Recorded for visibility; this log does not discharge or re-scope them.

| ID | Dependency | On whom | Blocks | Status |
|---|---|---|---|---|
| D-01 | Supervisor availability for countersign | Supervisor | G-05 and G-07, twice on the critical path | Unknown; no return date recorded |
| D-02 | G-05 experiment-freeze signature | Supervisor | Opening December 2022 | Not signed |
| D-03 | G-07 final acceptance, mandatory full board | Supervisor / board | Project acceptance | Not reached |
| D-04 | D-9 and D-10 countersign | Supervisor | Nothing outright, but leaves R-01 open | Sole-signed |
| D-05 | Technical Environment §1.5, §2 and TA-25 corrections through Vision §15.2 change control | Student + supervisor | Document consistency, not execution | Pending |
| D-06 | Examining-committee communication or reporting requirements | Committee | Possibly the reporting format | Unknown (open question) |
| D-07 | Thesis chapter prose | Authored outside this initiative | Nothing inside the pipeline | By design |
| D-08 | Earthdata Login or equivalent credential, if the chosen GIM route requires it `[web]` | Student, via the provider | The contextual comparison only | Not provisioned; route not yet established (V-03) |
| D-09 | Vision §15.2 change request to amend the §4.4 beginner-to-intermediate implementation-capacity clause, on the evidence of the author's advanced Python capability `[Q10]` `[Q13]` | Supervisor | Nothing | **Closed 2026-08-15 — countersigned by the supervisor**, recorded as reported by the student. No signature artifact is filed in this repository; attaching one would strengthen the record, exactly as noted for D-3/D-144. The residual documentation gap is tracked separately at I-12 |
| D-10dep | Vision §15.2 change record updating Technical Environment §1.5, §2 and TA-25 from Pending/Blocked | Student + supervisor | Document consistency; see I-10 for the execution ordering | Pending |

## Review

No AI-DLC reviewer is configured for this stage, so no reviewer verdict is recorded here.

### Governance board record

- **GOV-2026-08-15-FE-01** — adaptive board, five seats active, Validation Auditor and Implementation Reviewer recorded `N/A` with reason. Verdict **FAIL** on one blocker: the drafted artifacts recorded the absence of an implementation-capacity constraint that Vision v4.2 §4.4 fixes in the normative core. Four MAJOR findings (governed storage envelope absent; scaffold inputs diverging from the governed environment structure; the IRI validation-report obligation omitted; an over-claim of register completeness) and two MINOR findings. All findings were dispositioned by the human at `[Q13]`; the report is filed under `governance/reviews/`.
- **GOV-2026-08-15-FE-02** — re-review of the remediated set, adaptive board. Verdict **CONDITIONAL PASS**. The blocker and all six other findings are closed against verifiable text. Six non-blocking residuals carry owners and due gates: the unraised §15.2 change request (GOV-R-01, tracked here as D-09), the unrecomputed twelve manifests (GOV-R-02, V-02), the unmeasured Dst grade span and F10.7 outage (GOV-R-03), the unestablished GIM route (GOV-R-04, D-08), the still-unpersisted intent-capture board reports IC-01/02/03 (GOV-R-05), and the pending Technical Environment §1.5 / §2 / TA-25 corrections (GOV-R-06, D-10dep). Full report at `governance/reviews/GOV-2026-08-15-FE-02.md`.

One reviewer disagreement was recorded and remains open at board level: the Benchmark & Deployment seat read the §4.4 capacity clause as stale in light of the author's capability, while the Chair and the Data Quality & Reproducibility seat held that staleness of a normative clause is decided through Vision §15.2 and not by a reviewer. That disagreement is what D-09 exists to resolve.
