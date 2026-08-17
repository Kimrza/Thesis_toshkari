# Stakeholder Map — Hourly VTEC Forecasting (TEC_Project)

## Sources

- [desc] Initial description: "Execute TEC_Project Phase 1 acquisition under D-9 Option B with D-10 corrections (Kp/ap3 from GFZ, hourly Dst from Kyoto WDC, observed F10.7 from Canada Solar Radio Monitoring Program), align drivers onto the hourly grid without interpolation, define availability timestamps and lag all predictors against forecast leakage, then build the hourly VTEC model on ARUC 40/44, BSHM 32/35, NICO 35/33 for calendar 2022 with December 2022 as the locked test set."
- [scope] Workflow-selected scope: `research-pipeline-governed`.
- [Q1]–[Q21] Confirmed answers in `intent-capture-questions.md`. [Q19] is the governance correction record for board report GOV-2026-08-13-IC-01; [Q21] is the correction record for board report GOV-2026-08-13-IC-02 and governs the supervisor authority row below.

## Stakeholders and Interests

| Stakeholder | Interest | Source |
|---|---|---|
| Student / thesis author (Kimia Rezaei) | Owns every decision to date, sole-signed; needs a result that survives examination | [Q5] [Q2] |
| Supervisor | Holds countersign authority over the recorded decisions; currently recorded as unavailable | [Q5] |
| Examining committee / Amirkabir University of Technology | Accepts or rejects the final claims | [Q5] |

The customer of the work is the student specifically, distinct from the wider stakeholder set above. [Q2]

External data providers were offered as a stakeholder category and were not selected; they are therefore not recorded here as stakeholders. Citation and acknowledgement obligations remain a technical constraint on the pipeline rather than a stakeholder relationship in this map. [Q5]

## Decision-Makers vs. Influencers

| Party | Role | Authority | Source |
|---|---|---|---|
| Student | Decision-maker | Decides scope and priority alone; the supervisor countersigns after the fact. This authority does not extend to freeze gates, which require supervisor approval before the affected work begins | [Q6] [Q21] |
| Supervisor | Decision-maker | **Does not** gate day-to-day scope and priority decisions, which the student takes alone and the supervisor countersigns after the fact. **Does** gate every freeze gate: D-144 Phase 1 source adoption, G-05 experiment freeze, G-06 locked evaluation, G-07 final reproducibility acceptance, G-P2, G-P3, and the final claims decision. A freeze-gate value must be resolved, recorded and approved before the affected work begins, and no agent or implementer may supply one | [Q6] [Q12] [Q21] |
| `/review-tec-governance` board process | Influencer | Shapes decisions without holding decision authority | [Q7] |
| Data-provider constraints (what the sources publish, and at what grade) | Influencer | Shapes decisions without holding decision authority | [Q7] |

D-3/D-144 is countersigned as of 2026-08-15, so the Phase 1 source freeze gate is satisfied. The remaining decisions (D-1, D-2, D-4 through D-10) proceed without a countersign in place, on the basis that they are individually reversible and countersign is sought in parallel. That basis covers planning and design work only; it does not license execution past any other freeze gate, and G-05 still gates the December test set. [Q12] [Q21] [amended 2026-08-15]

## Communication Requirements

| Requirement | Detail | Cadence | Source |
|---|---|---|---|
| Decision record | Every decision recorded in `evidence/DECISIONS.md` with a supervisor countersign row, as at present | Per decision | [Q8] |

No periodic supervisor update cadence was selected, and no per-gate governance report was selected as an additional communication requirement. Neither is recorded as an obligation here. [Q8]

## Governance Dependencies

These are dependencies on parties outside this initiative rather than assumptions to be discharged inside it. [Q15]

Where a row reads `Unknown (open question)`, the value is **dependency-tracked by design and is not an untagged assumption**: [Q15] reclassified these items out of the assumptions register deliberately, so they carry no `[assumption]` label. [Q15] [Q21]

| Dependency | Detail | Party | Source |
|---|---|---|---|
| Supervisor countersign availability | Unknown (open question) — the record states unavailability at decision time, and no return date has been given | Supervisor | [Q5] [Q15] |
| Examining-committee requirements | Whether the committee imposes communication or reporting requirements of its own is Unknown (open question) | Examining committee / Amirkabir University of Technology | [Q5] [Q8] [Q15] |
| D-144 countersign record | **Closed 2026-08-15** — countersigned by the supervisor and entered in the `evidence/DECISIONS.md` signature table; Phase 1 acquisition is no longer blocked. Technical Environment v3.2 §1.5 still reads *Pending* until updated through Vision §15.2 change control | Student and supervisor | [Q19] [Q21] [amended 2026-08-15] |
| G-05 experiment-freeze signature | December 2022 cannot be opened without it | Supervisor | [Q19] |
| Thesis chapter prose | Authored outside this initiative; this initiative supplies chapter inputs only | Student | [Q14] [Q19] |

## Assumptions & Open Questions

None.

## Governance board record

Reviewed under the TEC_Project governance overlay at GOV-2026-08-13-IC-01 (FAIL), GOV-2026-08-13-IC-02 (FAIL, finding GOV-20 against the supervisor authority row) and GOV-2026-08-13-IC-03 (CONDITIONAL PASS, GOV-20 verified closed). The board recommends only; the student and supervisor remain the deciding authority. [Q21]
