# Feasibility Assessment — Hourly VTEC Forecasting (TEC_Project Phase 1 onward)

## Sources

- Upstream: `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/intent-capture/intent-statement.md` (approved 2026-08-13, amended 2026-08-15) — the governing statement of problem, driver contract, success layers, primary estimand, reporting contract and sealing condition. Nothing in this assessment redefines any of them. Referred to below as **the intent statement**.
- Authority: `Project Vision and Research Definition` v4.2, 11 August 2026 (`PreFlight/vision_document(3)(2)(2).md`) — normative core §§1–17, governing per §1.2; and `Technical Environment and Research Implementation` v3.2 (`PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md`) — subordinate implementation authority.
- `[Q1]`–`[Q14]`: confirmed answers in `feasibility-questions.md`. `[Q1]`–`[Q12]` were confirmed at the pre-generation checkpoint on 2026-08-15; `[Q13]`–`[Q14]` record the human's disposition of governance report GOV-2026-08-15-FE-01.
- `[survey]` Workspace survey re-run 2026-08-15: `notebooks/madrigal_phase1_coverage_audit.ipynb`, `scripts/merge_coverage_year.py`, `evidence/DECISIONS.md`, `evidence/audit_evidence_2022-{01..12,FULL}/`, `governance/reviews/` (present but **empty**). No `src/` package, no `tests/`, no dependency lock file (`requirements.txt`, `environment.yml`, `pyproject.toml`, `poetry.lock` all absent).
- `[web]` External findings recorded in the questions file on 2026-08-15: the Penticton/DRAO F10.7 interruption beginning 2022-03-18 is a documented month-long outage caused by a cyberattack on the NRC network (Elvidge & Themens, *Space Weather*, 2023); CDDIS discontinued anonymous FTP in October 2020 and IONEX retrieval requires an Earthdata Login; `iri2016` requires a Fortran compiler and builds on first use; Kaggle CPU sessions run 12 hours with 30 GB RAM.

Market research was not executed for this initiative, so no `competitive-analysis`, `market-trends` or `build-vs-buy` artifact exists to consume; this is a scope property of `research-pipeline-governed`, not a gap.

## Verdict

**Feasible, with the binding constraint being calendar time against a serial chain that contains two supervisor signatures, not technical difficulty.**

Every capability this initiative needs is either already demonstrated in this workspace or is standard, well-documented retrieval and modelling work. No component was found to be technically infeasible on the stated environment. The three genuine feasibility pressures, in order, are:

1. **The foundation does not exist yet.** There is no package, no pinned environment and no test suite `[survey]`, and the initiative has chosen to build all three before acquisition `[Q1]` `[Q4]`. This is the correct sequence but it front-loads work into a semester-bounded schedule `[Q9]`, and the user independently named it the top risk `[Q12]`.
2. **Two signatures sit on the critical path with no known availability.** G-05 gates opening December and G-07 gates final acceptance (intent statement, *Test-set sealing condition* and *Reproducibility standing*); supervisor availability is recorded as Unknown (intent statement, Governance Dependency 6). No amount of engineering removes this.
3. **Two data-source unknowns are measurable but not yet measured** — the Kyoto Dst grade span and the Canadian F10.7 outage extent `[Q5]` — and both are already recorded as obligations upstream that must close before acquisition freeze.

Nothing here justifies changing the initiative's shape. The recommendation is to run the sequence as answered and to move the G-05 freeze-manifest preparation as early as the plan allows, so that the signature wait overlaps with work rather than following it.

## Scope of This Assessment

This assessment covers technical viability, execution environment, compliance and licensing exposure, and schedule realism. It does **not** re-derive the experimental design. The metric set, difficulty controls, model set, forecast horizon, reporting contract and sealing condition are carried forward from governance correction and are binding, per the phase-boundary note in the intent statement. Where they appear below, they appear as constraints to be satisfied, never as choices reopened.

## Technical Feasibility by Capability

| # | Capability | Verdict | Basis |
|---|---|---|---|
| T-01 | Madrigal MAPGPS VTEC for the three cells, calendar 2022 | **Demonstrated** | The audited record set already exists: 223,586 rows, 365/365 days, three cells, twelve per-month SHA-256 manifests `[Q2]`, with the audit notebook and merge script present in the workspace `[survey]`. `[Q2]` promotes this set as the acquisition input rather than re-running acquisition |
| T-02 | Re-derivation of T-01 from a pinned client call (`madrigalWeb`, experiment/kindat discovery, parameter pinning) | **Feasible, uncertain in detail** | Flagged as carrying real technical uncertainty `[Q5]`. The uncertainty is no longer about access — D-3/D-144 is countersigned — but about pinning an exact, replayable query. This matters for reproducibility (G-07), not for whether the data can be obtained |
| T-03 | GFZ Kp, ap3, Hp60, ap60 | **Routine** | Explicitly excluded from the uncertain set `[Q5]`. Hp60/ap60 are the cadence-matched preferred features per the intent statement's driver contract |
| T-04 | Kyoto WDC hourly Dst | **Feasible, grade unmeasured** | Flagged uncertain `[Q5]`. Risk is bounded: the driver contract classifies Dst as diagnostic / hindcast-only and **not** a confirmatory forecast feature, so a grade problem degrades diagnostics, it does not invalidate the primary estimand |
| T-05 | Canadian observed F10.7, including the 2022-03-18 outage | **Feasible, gap unmeasured** | Flagged uncertain `[Q5]`. The outage is externally documented as roughly a month `[web]`, and the intent statement already forbids imputation or substitution until the measured gap is recorded and governed |
| T-06 | Hourly alignment without interpolation, availability timestamps, per-driver lagging | **Feasible; the core engineering** | No external dependency. Difficulty is discipline, not technique: the intent statement bounds carry-forward at ≤ 3 h and forbids smoothing or centring. Correctness here is evidenced by tests, see T-09 |
| T-07 | IRI-2016 benchmark values | **Feasible; runtime unmeasured, volume small** | Nothing exists yet `[Q6]`. `iri2016` needs a Fortran toolchain and builds on first use `[web]`, which on an ephemeral Kaggle session means a rebuild per session. Volume is modest: 3 cells × 744 hours = 2,232 evaluations for the locked December month, 3 × 8,760 = 26,280 for the full year. Even a slow per-call implementation clears this inside one 12-hour session `[web]` |
| T-08 | CODE final GIM contextual comparator | **Feasible; access route needs confirming** | Nothing exists yet `[Q6]`. CDDIS retrieval now requires an Earthdata Login `[web]`, which is a credential-provisioning step, not a barrier. Whether an alternative CODE/AIUB route serves the same final product without that login is **not** established here and is registered as a verification obligation, not asserted |
| T-09 | Leakage-freedom test suite | **Feasible and mandatory** | Nothing exists yet `[survey]`. This is not engineering hygiene: the intent statement makes leakage freedom one of two pass/fail measures and requires it be *verified by executable tests*, so the suite is itself a thesis deliverable |
| T-10 | Model set (persistence, seasonal persistence, climatology, ridge, RF, compact LSTM) | **Routine at this data scale** | Three cells × 8,760 hourly rows is small — roughly 26,000 rows, matching Vision §4.4 — and the binding resource is neither RAM nor CPU. The §4.4 implementation-capacity ceiling was lifted on 2026-08-15 by an approved §15.2 change request (OC-09), so no capability constraint bounds the design; the model set itself was never affected either way, being fixed by the intent statement |
| T-11 | Vector block bootstrap carrying all three stations, 24-hour blocks, 95% | **Routine** | Standard resampling on a small array; cost is negligible relative to T-07 |
| T-12 | Reproducibility package (pinned environment, seeds, hash manifests) | **Feasible; depends entirely on T-13** | Required inside the project-completion success layer per the intent statement and a G-07 input |
| T-13 | Repository, package layout, pinned environment, test runner | **Absent today; first work item** | Confirmed absent by survey `[survey]`; `[Q1]` and `[Q4]` place it first and inside this initiative |

### What the promoted-set decision buys and costs

`[Q2]` keeps D-9 Option B: the audited twelve-month record set is the acquisition input, and the twelve independent per-month manifests are treated as stronger provenance than a single fresh run. From a feasibility standpoint this **removes** the largest single block of runtime risk — a fresh full-year acquisition was estimated at roughly 17 hours `[Q2]`, which does not fit one Kaggle session `[web]` and would need chunking and resumption logic that would then itself need testing.

The cost is that provenance is distributed across twelve manifests rather than one, and that T-02 — a pinned, replayable query — is left as work rather than being a by-product of a fresh run. `[Q2]` explicitly rejects both re-running now (Option A) and scheduling a later single-run re-acquisition as verification (Option C), so the reproducibility story must be carried by the manifests plus a documented query specification. That is achievable, and it is recorded as an obligation below rather than assumed.

## Execution Environment Feasibility

`[Q3]` sets Kaggle as primary compute with a local machine for development and cross-check, the full workflow feasible on CPU, GPU as an optional accelerator only.

| Property | Assessment |
|---|---|
| Compute sufficiency | Ample. The joined dataset is on the order of 10⁴–10⁵ rows; a compact LSTM over it is minutes of CPU, not hours. 30 GB RAM `[web]` is far beyond need |
| Session limit (12 h) `[web]` | Not binding for training or evaluation. It **is** binding for any single long acquisition run, which is precisely the run `[Q2]` avoids |
| Session ephemerality | The real constraint. A Fortran build for `iri2016` `[web]`, plus every dependency, is re-established per session. This makes a pinned, fast-restoring environment a working necessity, not only a G-07 deliverable — and it aligns with the `[Q1]`/`[Q4]` decision to build the environment first |
| Two-environment parity (Kaggle + local) | Requires the environment specification to be the single source of truth for both, and a cheap parity check. This is a design requirement generated by `[Q3]`, carried to the constraint register |
| GPU | Optional by decision `[Q3]`. No result may depend on GPU availability, which also keeps the reproducibility package simpler |

## Compliance and Licensing Feasibility

The compliance surface is narrow, well understood, and carries **no** regulatory framework exposure.

`[Q8]` records that all sources are public scientific measurements. There is therefore **no personal data, no PHI, no export-controlled material**, and consequently no privacy impact assessment, no data-residency constraint, and no applicability of GDPR, HIPAA, PCI-DSS or SOC 2. Recording this negative finding explicitly is deliberate: it is what keeps a later reviewer from re-opening the question.

What does bind, per `[Q7]`:

| ID | Obligation | Nature | Feasibility |
|---|---|---|---|
| C-01 | CEDAR/Madrigal rules-of-the-road: permanent experiment citation and acknowledgement | Attribution | Satisfiable by recording the experiment identifier and acknowledgement text alongside the data manifests. The full rules-of-the-road text must be read and its clauses itemised — this assessment does not restate clauses it has not read |
| C-02 | Kyoto WDC Dst non-commercial-use notice and citation | Attribution + use restriction | A thesis is non-commercial academic use, so the restriction is satisfied by the nature of the work. The notice and citation must be reproduced with the data and in the thesis |
| C-03 | GFZ and Canadian Solar Radio Monitoring Program citation and acknowledgement | Attribution | Routine |
| C-04 | Licence compatibility review for any third-party code reused in the pipeline | Licence review | Applies to `madrigalWeb`, the IRI-2016 wrapper, and any GIM/IONEX reader. Must be done **before** those dependencies are pinned, so that a licence finding does not force a late dependency swap |
| C-05 | Two source families, two sets of obligations | Provenance | The intent statement's join semantics make the VTEC provider **and** the index producers both subject to citation and acknowledgement. The provenance record must therefore be per-family, not per-file |

`[Q7]` does **not** select option D (university or supervisor requirements on data handling, authorship or publication). This assessment reads that as: no institutional requirement *of that kind* has been identified, distinct from the supervisor's decision-gating authority, which is real and is tracked as a governance dependency rather than as a licensing obligation. The two are not in conflict. Confirming the absence of a separate institutional requirement before submission is registered below as an obligation, because an unidentified requirement and an absent one look the same until asked.

## Timeline Feasibility

`[Q9]` sets one academic semester with the empirical chapter due at its end. `[Q11]` records no organisational blockers beyond the countersign dependency already on file.

The chain is largely serial, and that is what makes the schedule the binding constraint:

```
scaffold + pinned environment + test harness   (T-13, T-09 skeleton)   [Q1] [Q4]
  -> promote + verify audited record set        (T-01)                  [Q2]
  -> driver retrieval + gap/grade audits        (T-03, T-04, T-05)      [Q5]
  -> alignment, availability, lagging           (T-06)
  -> leakage tests green                        (T-09)
  -> baselines + models trained on folds        (T-10)
  -> G-05 freeze manifest assembled and SIGNED  <- supervisor
  -> December opened, one write, hash first     (G-06)
  -> evaluation + bootstrap + reporting         (T-07, T-08, T-11)
  -> reproducibility package                    (T-12) -> G-07 <- supervisor
```

Three observations follow from the shape rather than from any estimate:

- **The two signature waits are not parallelisable with the work they gate**, but the *preparation* for them is. The G-05 manifest can be assembled and submitted while model training continues; G-07's package can be built incrementally from the first commit rather than assembled at the end. Both are scheduling choices available now, and both are recorded as constraints.
- **The `[Q1]` sequencing decision is schedule-positive despite being front-loaded.** Building the environment and test harness first means the acquisition and alignment work lands in a governed pipeline immediately, avoiding a later retrofit that would have to re-verify everything already produced. The alternative — acquiring first — would trade a small early delay for a large late one.
- **The audits (T-04, T-05) should run early**, because they are cheap, they are inputs to the acquisition freeze gate, and their outcome could change how the F10.7 gap is handled, which is upstream of every model that uses F10.7 as a feature.

Feasible within a semester on these terms. The honest caveat is that the schedule has little slack for an overturned decision (see R-01 in the RAID log) or a signature delay, and neither is inside the initiative's control.

## Gating Conditions Recorded Here, and Their Inputs

Every condition this stage records is stated with the inputs it depends on, in this stage, so that it is checkable by a reader of this stage alone.

### GC-01 — Scaffold-ready (precondition for acquisition work, from `[Q1]` and `[Q4]`)

Acquisition and alignment work begins only when all of the following exist in the repository:

1. An importable package under `src/` with an explicit module layout (acquisition, alignment, features, models, evaluation kept separate, so that the intent statement's architectural exclusion of IRI/GIM from feature and model code is enforceable by structure).
2. A dependency lock file that pins the full transitive set, resolvable on both Kaggle and the local machine `[Q3]`.
3. A documented, single-command environment restore, plus a recorded restore time on a cold Kaggle session (this is what makes the `iri2016` Fortran build `[web]` a known cost rather than a surprise).
4. A test runner configured and a `tests/` tree present, containing at minimum one executing leakage test — a skeleton that fails for the right reason is sufficient to satisfy this input; a full suite is not required to start acquisition.
5. A hash-manifest verification routine that re-checks the twelve per-month SHA-256 manifests `[Q2]` against the promoted files, exiting non-zero on mismatch.
6. Recorded seeds and a deterministic-run convention.

These six items are the complete input set for GC-01, and no further condition is deferred. **GC-01 supplements the governed environment structure; it does not replace it.** Technical Environment v3.2 already fixes Python 3.11 with exact pins (TA-03), exactly four governed config files, the two fixtures, the governed notebook and script structure (TE §7 production-notebook contract), and the `environment_and_cpu_preflight_report` (EV-14) as the evidence that the CPU path is complete. Those obligations stand in full and are recorded as TC-03d through TC-03g in `constraint-register.md`; GC-01 states only what must exist *before acquisition begins*.

Item 4 is a start threshold, not a test budget: **it does not narrow the critical negative-path test set** — IRI-injection denial, split embargo, train-only transforms, comparison-wide masks, the locked-test guard, release hashes, bootstrap correlation and protected-hash drift — which remains required in full at G-05 and G-07.

### GC-02 — Acquisition-freeze inputs (this stage's contribution to G-P1A)

The intent statement already carries the acquisition-freeze obligations. This stage adds no new requirement and only names, for checkability, the artifacts that must exist: the Kyoto Dst grade-span record for 2022-01-01 to 2022-12-31, the Canadian F10.7 outage audit report giving exact missing dates and any qualifiers or reconstructed values, and the file hashes for both. Their authority and content are fixed upstream, not here.

### GC-03 — G-05 and G-07 are not owned by this stage

The intent statement fixes G-05's authority in Vision §8.3 and assigns the freeze manifest to NFR Requirements (3.2) and the requirement IDs to Requirements Analysis (2.3). This assessment does not restate, narrow, relocate or duplicate that. It records only the schedule consequence — that both signatures sit on the critical path — which is a feasibility fact, not a governance rule.

## Scoped Verification Obligations

Checks this initiative owns and must perform. These are obligations, not assumptions.

| # | Obligation | Precise scope | Source |
|---|---|---|---|
| V-01 | Pinned Madrigal query specification | Record the exact `madrigalWeb` call, experiment identifier, kindat and parameter set that reproduces the promoted record set, sufficient for a reader to replay it. Required because `[Q2]` declines a fresh single-run acquisition, so replayability must be documented rather than demonstrated | `[Q2]` `[Q5]` |
| V-02 | Manifest re-verification of the promoted set | Re-compute and compare all twelve per-month SHA-256 manifests against the promoted files before the set is used as acquisition input; record the result | `[Q2]` `[survey]` |
| V-03 | CODE final GIM retrieval route | Establish and record a working retrieval route for the CODE final GIM. Confirm whether an Earthdata Login is required for the chosen route `[web]`, and provision credentials if so. Do not assume an alternative unauthenticated route exists until one is verified | `[Q6]` `[web]` |
| V-04 | IRI-2016 build and runtime measurement | Build `iri2016` on a cold Kaggle session, record build time and per-call runtime, and confirm the December evaluation volume fits inside one session with margin. Time the full ~26,000-call workload, per Vision §4.4 | `[Q6]` `[Q3]` `[web]`, Vision §4.4 |
| V-04a | IRI-2016 implementation validation | Validate five to ten samples spanning sites, day and night, and quiet and disturbed conditions against the official IRI interface, within a numeric tolerance **predeclared before the comparison is run**. Evidence artifact: `iri_implementation_validation_report`. A working build is not a validated benchmark, and this obligation is what separates the two | Vision §4.4 area |
| V-05 | Environment parity | Demonstrate that the pinned environment restores to the same resolved versions on Kaggle and on the local machine, and record any divergence | `[Q3]` |
| V-06 | Third-party licence review | Review and record the licence of every third-party dependency in the pipeline before pinning, per `[Q7]` option E, and confirm compatibility with thesis publication | `[Q7]` |
| V-07 | Attribution package | Assemble the citation and acknowledgement text for both source families — the VTEC provider and the GFZ / Kyoto WDC / Canadian index producers — including the Madrigal permanent experiment citation and the Kyoto non-commercial-use notice, and read the CEDAR/Madrigal rules-of-the-road in full to itemise any clause beyond citation | `[Q7]` |
| V-08 | Institutional requirement check | Confirm with the university or supervisor that no data-handling, authorship or publication requirement applies beyond the decision gates already tracked. `[Q7]` did not select that option; confirming an absence is cheap and closes it | `[Q7]` |

The Kyoto Dst grade-span record and the Canadian F10.7 outage audit are **not** repeated here as new obligations: they are already carried as obligations 1 and 2 in the intent statement, and duplicating them would create two records that can drift apart.

## Governance Dependencies

Owned outside this initiative. Listed for schedule visibility only; this stage neither discharges nor re-scopes them.

| # | Dependency | Feasibility consequence | Source |
|---|---|---|---|
| G-01 | Supervisor availability for countersign | Unknown; sits directly on the critical path twice (G-05, G-07). The single largest schedule risk that engineering cannot mitigate | intent statement, Governance Dependency 6 |
| G-02 | G-05 signature | December cannot be opened without it; all confirmatory results follow it | intent statement |
| G-03 | G-07 final acceptance | Mandatory full-board gate; an incomplete reproducibility package does not pass it | intent statement |
| G-04 | D-9 and D-10 signature rows still blank | The acquisition route and driver-source corrections remain sole-signed. If either is overturned on review, work built on it is invalidated — the user's second-ranked concern in `[Q12]` in effect | intent statement, `evidence/DECISIONS.md` `[survey]` |
| G-05dep | Technical Environment v3.2 §1.5 still reads *Pending — D-144* | Corrected only through Vision §15.2 change control, outside this workflow | intent statement |
| G-06dep | Board reports not yet persisted under `governance/reviews/` | The directory exists and is empty `[survey]`; GOV-25 remains open | `[survey]`, intent statement |

## Consistency Check Against the Intent Statement

Checked before the approval gate, against the governing artifact rather than only against the questions that produced this one.

| Intent statement provision | This assessment | Status |
|---|---|---|
| IRI-2016 architecturally excluded from model; joined at evaluation only | T-07 treats IRI as evaluation-time only; GC-01 input 1 makes the exclusion structurally enforceable | Consistent, reinforced |
| CODE GIM comparator, evaluation-time only | T-08 treats it as a comparator; V-03 covers retrieval only | Consistent |
| Dst diagnostic / hindcast-only, not a confirmatory feature | T-04 bounds the Dst risk precisely because of this classification | Consistent |
| Hp60/ap60 preferred over Kp alone | T-03 records them as the cadence-matched preferred features | Consistent |
| No imputation for the F10.7 gap until measured and governed | T-05 and GC-02 record the audit as an input, and propose no substitution | Consistent |
| Sealing condition owned by G-05; manifest owned by stage 3.2, IDs by stage 2.3 | GC-03 records the schedule consequence and explicitly does not restate or relocate the requirement | Consistent; the ownership stays where the authority document places it |
| Reproducibility inside the project-completion success layer | T-12, V-01, V-05 treat the package as required work, not optional polish | Consistent |
| Success has three layers; a negative result is not a project failure | The timeline analysis treats a negative result as an outcome, not a schedule failure; `[Q12]` ranks it second among risks, and the RAID log treats it as a risk to the *claim*, not to *completion* | Consistent |
| Two source families carry provenance and licensing obligations | C-05 and V-07 make the attribution record per-family | Consistent |

No contradiction found between this assessment and the intent statement.

### Against the Vision normative core

Checked separately, because the intent statement is downstream of the Vision and consistency with one does not imply consistency with the other.

| Vision v4.2 provision | This assessment | Status |
|---|---|---|
| §4.4 — one academic semester | Timeline analysis; `[Q9]` agrees | Consistent |
| §4.4 — full workflow feasible on CPU, GPU an accelerator not a dependency | TC-01; `[Q3]` agrees | Consistent |
| §4.4 — approximately 10 GB storage | TC-03a, added after governance review | Consistent |
| §4.4 — ~30 Kaggle GPU hours per week available but not required | TC-03b, recorded as headroom only | Consistent |
| §4.4 — two platforms only, Kaggle primary and local | TC-03c; `[Q3]` agrees | Consistent |
| §4.4 — ~26,000 hourly station rows, actual counts reported never assumed | T-01 and T-10 use the audited count of 223,586 source rows and the derived 26,280 hourly cell-hours, both reported rather than assumed | Consistent |
| §4.4 — beginner-to-intermediate Python implementation capacity | **Superseded 2026-08-15.** The §15.2 change request was countersigned by the supervisor, so the clause no longer binds; OC-09 records the amended position. The Vision text itself is not yet updated — tracked at I-12 | **Consistent with the amended authority**; see D-09 (closed) in the RAID log |
| §1.2 — normative core governs; a freeze-gate value must not be guessed by an implementer or agent | No `TBD — freeze gate` value is supplied anywhere in this stage's artifacts | Consistent |
| §15.2 — material change runs through change control | Both change items were routed to §15.2 rather than resolved in-stage. The §4.4 capacity clause was approved there on 2026-08-15; Technical Environment §1.5 remains pending | Consistent |

## Assumptions & Open Questions

None. Every uncertainty identified in this stage is registered either as a scoped verification obligation (V-01 to V-04a, V-08) owned by this initiative, or as a governance dependency (G-01 to G-06dep, D-09) owned outside it.

## Governance Review

Two TEC_Project governance board passes were run against this artifact set under the project overlay, both adaptive mode with five seats active and the Validation Auditor and Implementation Reviewer recorded `N/A` with reason.

| Report | Verdict | Outcome |
|---|---|---|
| `governance/reviews/GOV-2026-08-15-FE-01.md` | FAIL | One BLOCKER — the artifacts recorded the absence of the Vision §4.4 implementation-capacity constraint — plus four MAJOR and two MINOR findings. Dispositioned by the human at `[Q13]` |
| `governance/reviews/GOV-2026-08-15-FE-02.md` | **CONDITIONAL PASS** | Blocker closed; all six other findings closed against verifiable text. Six non-blocking residuals remain, each with an owner and due gate (GOV-R-01 to GOV-R-06) |

One reviewer disagreement is maintained rather than resolved: whether Vision §4.4's beginner-to-intermediate capacity clause understates this project's real capacity. It is now the substance of change request D-09 in `raid-log.md`, which the supervisor decides. The boards recommend only; neither grants academic approval nor authorises locked-test access.
