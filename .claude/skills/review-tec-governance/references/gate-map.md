# AI-DLC v2 to TEC_Project gate map

Use the active `aidlc-state.md`, stage directory, artifact index, and approval prompt as the AI-DLC source. Review only stages selected by the active AI-DLC scope. Initialization stages 0.1–0.3 run automatically and have no approval gate; review their outputs only when a later artifact depends on them.

## AI-DLC stage routing

| AI-DLC stage or boundary | Primary TEC review | Typical evidence |
|---|---|---|
| 1.1 Intent Capture; 1.3 Feasibility; 1.4 Scope; 1.7 Handoff; Ideation → Inception | G-01, G-02, G-09 | Research question, IRI role, scope/non-claims, constraints, RAID, authority and approval records |
| 1.2 Market Research; 1.5 Team; 1.6 Mockups | Claims/resource relevance only; mark scientific checks N/A with reason | Source quality, resource assumptions, role conflicts; UI artifacts are normally out of scope |
| 2.1 Reverse Engineering | G-02, G-07, G-09 | Existing repository, data/code inventory, protected artifacts, gaps and undocumented behavior |
| 2.2 Practices Discovery | G-07, G-09 | Reproducibility, provenance, testing, secret, licensing and human-freeze practices |
| 2.3 Requirements Analysis | G-01–G-05, G-09, G-P1/P2/P3 as applicable | Stable IDs, normative requirements, evidence obligations, acceptance criteria, traceability |
| 2.4 User Stories / Personas | G-09 and traceability only | Researcher/supervisor actions, locked-test custody, no invented end-user or operational scope |
| 2.5 Refined Mockups | Usually N/A | Review only if a scientific dashboard/table could distort interpretation |
| 2.6 Application Design | G-03–G-05, G-07, G-09, phase boundary | Four configs, package boundaries, IRI isolation, target interfaces, manifests, tests, transition hashes |
| 2.7 Units Generation; 2.8 Delivery Planning; Inception → Construction | All affected TEC gates | Gate order, dependencies, evidence owners, freeze-before-build constraints, Phase 1 before Phase 2 |
| 3.1 Functional Design | Gate governing the affected unit | Data/target/model/evaluation contracts and testable acceptance criteria |
| 3.2 NFR Requirements; 3.3 NFR Design | G-04, G-07, G-09 | IRI integrity, leakage, fairness, auditability, determinism, phase and license integrity |
| 3.4 Infrastructure Design | G-07, G-09 | Local/Kaggle roles, CPU path, 10 GB plan, secrets, transfer hashes |
| 3.5 Code Generation; each Bolt gate | Gate governing the code unit | Diff, tests, configs, manifests, no unauthorized scientific default; walking skeleton uses all WS checks |
| 3.6 Build and Test | G-02–G-07, G-09, phase gate in scope | Test reports, fixtures, release hashes, registry, negative-path tests, locked-test guard |
| 3.7 CI Pipeline; Construction → Operation | G-07, G-09, G-P2/P3 when applicable | Critical-test enforcement, artifact immutability, phase hash checks, secret/license scans |
| 4.1–4.7 Operation | G-07/G-08 plus project scope check | Packaging, environment validation, runtime/cost, feedback records; operational service/deployment claims remain out of scope unless separately approved |

## TEC gate minimums

| TEC gate | Review focus | Mode |
|---|---|---|
| G-01 Scientific framing | Question, estimand, IRI-benchmark-only role, comparison hierarchy, claims | Adaptive |
| G-02 Station/data viability | ARUC/BSHM/NICO identity, official logs, 2022 coverage, observables/cadence | Adaptive |
| G-03 GNSS target | Package trial, DCB sign/negative control, mapping/QC sensitivities, two references, uncertainty | Adaptive; full board if accepting target |
| G-04 Feature safety | Availability matrix, safe lags, IRI denial, causal windows, train-only transforms | Adaptive |
| G-05 Experiment freeze | F1–F4, embargo, masks, grids, seeds, estimand, bootstrap, regimes, December audit, signatures | Full board |
| G-06 Locked evaluation | Access authorization, one write, prediction hash before metrics, registry, no post-test changes | Full board |
| G-07 Reproducibility | Exact pins, CPU runs local/Kaggle, manifests, hashes, tolerances, registry | Adaptive; full board for final acceptance |
| G-08 Claims | Required controls, uncertainty, station/year/horizon boundary, negative/inconclusive honesty | Full board |
| G-09 Agent preflight | Zero applicable P0 TBDs, critical tests, supervisor-owned values | Adaptive; full board when it opens a major freeze |
| G-P1 Prepared-data MVP | Source viability, immutable target, safe evaluation, complete positive/negative/inconclusive reporting | Full board at MVP decision |
| G-P2 Phase transition | Signed protected-hash manifest and reuse/license register; raw work remains blocked until approval | Full board |
| G-P3 Raw-target acceptance | Raw pipeline, two-reference matched validation, pre-frozen thresholds, uncertainty, unchanged forecasting protocol | Full board |

## Review timing

Run the overlay after the AI-DLC stage artifact exists and before the human approves that stage. At phase boundaries, review the consolidated phase evidence after AI-DLC verification and before handoff. At Construction, always review the walking-skeleton gate; if AI-DLC autonomous mode is selected, still require TEC reviews at every TEC gate and any full-board trigger.
