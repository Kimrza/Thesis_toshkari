# Delivery Planning — Questions

Stage 2.8 (`delivery-planning`), intent `260813-tec-hourly-forecast`.
Depth: Comprehensive. Scope: `research-pipeline-governed`.

## Sources

- Units and topology: `../units-generation/unit-of-work.md` (12 units, the blocker register BLK-01…BLK-07, the residual obligations RES-01…RES-03), `../units-generation/unit-of-work-dependency.md` (23 edges, one independent pair, the forbidden edges), `../units-generation/unit-of-work-story-map.md` (105 requirements to units, 13 WS + 27 TA acceptance rows, 40 requirements with no test row).
- Design: `../application-design/components.md` (six `src/` packages, the three **NEW** modules, the layering rule).
- Requirements: `../requirements-analysis/requirements.md` (the seventeen governing gates, § Known defects, § Constraints, § Success and acceptance).
- Affirmed practices: `../practices-discovery/team-practices.md` (§ Way of Working, § Walking Skeleton, § Testing Posture, § Deployment).
- Absent by scope design, and named so the gap is visible rather than silent: `stories` (`../user-stories/stories.md`) — stage 2.4 is `SKIP`; `mockups` (`../refined-mockups/`) — stages 1.6 and 2.5 are `SKIP`. This pipeline has no user-facing surface, so no mockup input is missing in substance.

## What this stage is deciding

A **Bolt** is one build pass over a piece of the work, ending in something that
runs and can be shown. Stage 2.7 fixed the dependency graph — what can depend on
what. This stage picks the path through that graph: which piece is built first,
what each one must prove, and what could hold it up. The graph is a fact; the
order is a judgment, and it is yours.

Twelve pieces of work are already defined, and the graph between them is almost a
straight line — exactly one pair (`target-standardization` and
`external-products`) can legally swap. So the questions below are less about
re-ordering than about **granularity, what counts as finished, and how the ten
pieces that carry an open blocker are handled**.

---

## Question 1

How big should one Bolt be — one build pass over a piece of the work, ending in something that runs?

A) One Bolt per unit of work — 12 Bolts
   > **Impact**: Each Bolt has one owner unit, one dependency set, and one blocker set, so a blocked piece stalls only itself. Ten of the twelve units carry an open or inherited blocker (`unit-of-work.md` § Roll-up by unit), so isolation is doing real work here. Twelve build passes is the most bookkeeping of the three options.

B) Bundle into about five Bolts along pipeline phases (roots / acquisition+inventory / target+external / features+models / evaluation+reporting+fixtures)
   > **Impact**: Fewer, larger passes and fewer checkpoints. But nearly every bundle would contain at least one blocked unit, and `unit-of-work.md` § Blocker register states that a blocked unit is "not sequenced for implementation and not marked accepted, Ready or complete until its named blocker is discharged" — so a bundle's Definition of Done would be unreachable while any member is blocked.

C) Hybrid: bundle the two dependency roots (`foundation` + `governance-guards`) into Bolt 1 to satisfy TC-06 as a single Definition of Done, then one Bolt per unit for the remaining ten
   > **Impact**: Makes "TC-06 is satisfied" one checkable outcome instead of two. But `governance-guards` carries **BLK-06** (the canonical protected set is not derived), so Bolt 1's Definition of Done would be partly blocked from the start, and the scaffold — which is not blocked — would be held behind it.

D) Thin slices that cut across units (for example, "one end-to-end row through the whole pipeline")
   > **Impact**: This is the walking-skeleton shape. It is barred here in practice: §7.0's Phase 1 prohibition, the locked-December guard and the fixture ordering contract all mean a single end-to-end row cannot be produced before the units that enforce them exist. It would also cut across the unit boundaries that the blocker register and the acceptance-row ownership are both keyed to.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — one Bolt per unit. The decisive fact is that ten of twelve units carry a blocker, and blockers are scoped to *files inside* a unit rather than to whole units. One Bolt per unit is the only granularity where a blocked piece of scope stops exactly one Bolt. The extra bookkeeping is real but cheap; an unreachable Definition of Done is neither.

[Answer]: A

---

## Question 2

What heuristic decides the Bolt order — and how much should it be allowed to deviate from the dependency graph?

A) Strict dependency order, with risk used only to break ties where the graph allows a genuine choice
   > **Impact**: Honest to the graph and cheap to justify. The graph is near-linear (23 edges over 12 units, exactly one independent pair), so there is almost no room to deviate anyway — and TC-06 pins the front (scaffold and tests before acquisition) while `fixtures-and-reproducibility`'s nine incoming edges pin the back. The cost is that no explicit value scoring is recorded.

B) WSJF — score each unit on value, time-criticality and risk reduction, divide by size, ship highest first
   > **Impact**: Produces a defensible numeric ranking and a recorded scoring model. On this graph it would be ceremony: with one legal swap available, the scores cannot change the order, and inventing value scores for internal pipeline stages of a thesis codebase would put invented numbers into a governed artifact.

C) Risk-first — front-load the highest-uncertainty units as far as the graph legally allows
   > **Impact**: Surfaces unknowns earliest, which matters because the F10.7 outage, the driver release grades and the IRI/GIM allowlist all sit in `external-products`. But the graph permits very little front-loading, so in practice this collapses to option A with a different label on the one tie-break.

D) Value-first — order by what most advances the thesis result
   > **Impact**: Would front-load models and evaluation. Illegal on this graph: neither can be built before features, which cannot be built before the target and the drivers. It would also invert TC-06.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — strict dependency order with risk as the tie-break. Naming WSJF here would record a scoring model that cannot affect a single ordering decision, and `project.md` § Way of Working forbids exactly that shape of unsupported detail. The one place judgment genuinely applies is Question 3.

[Answer]: A

---

## Question 3

The graph permits exactly one swap: `target-standardization` and `external-products` do not depend on each other. Which is built first?

A) `target-standardization` first
   > **Impact**: The D-17 target contract is the single most-consumed artifact downstream — every feature, model, metric and figure rests on it. Building it first means `features-and-splits` gets its primary input earliest. It also surfaces **BLK-05** (the D-17 target-schema test has no module name and no §12 tree entry) sooner, and that blocker needs a supervisor-authority tree amendment, which has lead time.

B) `external-products` first
   > **Impact**: This is the risk-first choice. `external-products` is the larger unit (complexity L), carries five requirements with no acceptance row, and holds the highest-uncertainty work: the F10.7 outage window, Kyoto Dst release grades, the IRI-2016 validation report and the GIM network-overlap audit. Front-loading it surfaces provider and driver problems before the target work commits to a schedule. The cost is that `features-and-splits` waits longer for the target rows.

C) Treat them as a parallel batch
   > **Impact**: Legal on the graph but not useful here — this is a single-author codebase, and `unit-of-work-dependency.md` § Independent unit sets says so explicitly ("independent units will normally be implemented sequentially"). It would also give one gate covering two unrelated bodies of work.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B — `external-products` first. This is the one place in the whole plan where sequencing can actually reduce risk, and the risk is asymmetric: `external-products` depends on four outside providers whose problems (an outage window, a mixed release grade, a failed IRI validation report) are discovered only by trying, whereas `target-standardization`'s open item (BLK-05) is a naming decision inside this project's own control. Front-load the uncertainty you do not own. Honest cost: BLK-05's tree amendment starts later, so raise it as a written request when Bolt 4 starts rather than waiting for its Bolt.

[Answer]: B

---

## Question 4

Can Bolts run at the same time, or strictly one after another?

A) Strictly serial — one Bolt at a time
   > **Impact**: Matches the single-author reality recorded in `team-practices.md` § Way of Working ("a single-author thesis codebase (student: Kimia Rezaei)") and in `unit-of-work-dependency.md`. Each Bolt gets its own checkpoint. No parallel-merge machinery, no worktree conflicts, no batch-level gate that hides one Bolt's problem behind another's success.

B) Serial, except the one independent pair, which runs as a parallel batch
   > **Impact**: Saves nothing real with one author, and a batch gate covers both Bolts at once — so a problem in one is approved alongside the other. It also forgoes the sequencing decision made in Question 3.

C) Autonomous batches — build the remaining Bolts without stopping for approval between them
   > **Impact**: Directly against this project's governance posture. Every stage here has a human approval gate, and `team-practices.md` § Testing Posture quotes §18.3's binding rule that an agent "must not implement an affected component while its P0 decision is unresolved, and must stop and report rather than choose a default." Ten units carry open blockers; unattended building is the wrong mode.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — strictly serial. One author, one checkpoint per piece of work, and a governance regime that stops and asks rather than proceeding on a default. Note that `.claude/scopes/aidlc-research-pipeline-governed.md` declares `skeleton: off`, so the usual "how should the rest run?" prompt after the first Bolt does not fire — this answer is the standing one.

[Answer]: A

---

## Question 5

Should Construction design one unit completely and build it before starting the next, or run each design step across all units before moving to the next step?

A) One unit at a time — its functional design, NFR requirements and NFR design, then its code, then the next unit
   > **Impact**: The first working code lands after one unit's design instead of after all twelve. Matches one-Bolt-per-unit cleanly, and a blocked unit stops only its own block. The cost is decisive here: **BLK-03, BLK-04, BLK-06 and BLK-07 all require cross-unit contracts authored at functional design.** BLK-04's transform contract spans `features-and-splits` and the four units downstream of it; under this mode `features-and-splits` would finish its design before `models-and-baselines` starts, so the contract would be written without its consumers in the room.

B) One design step at a time across all units — all functional designs, then all NFR requirements, and so on, with code last
   > **Impact**: The four cross-unit contracts get authored while every affected unit is in scope, which is what BLK-03, BLK-04, BLK-06 and BLK-07 each require ("a governed cross-unit contract defining input and output types, alignment requirements, ownership… and failure conditions"). Approval gates stay one per step. The cost is that no code exists until every design is done — a long stretch with nothing runnable.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B. This reverses what one-Bolt-per-unit would suggest, and the reason is specific rather than stylistic: four of the six open blockers are *cross-unit contracts*, and three of them (BLK-03, BLK-04, BLK-07) are recorded as **exit conditions on functional design** for several units at once. Authoring a contract that binds five units while four of them have not yet entered the step is how a contract ends up describing one unit's convenience. Delayed running code is a real cost; a leakage contract written in isolation is a worse one. This is also the framework default, so nothing extra is recorded.

[Answer]: A

> **Follow-up raised — see FU-1.** This answer selects unit-major iteration. It
> interacts with the Question 8 answer in a way that changes when you get to
> approve anything, so FU-1 puts the consequence in front of you before the plan
> is written. FU-1's answer governs; this tag is not re-interpreted here.

---

## Question 6

What has to be true for a Bolt to count as done, given there is no CI service in this scope?

A) The unit's modules and its owned test modules exist and pass locally; every acceptance row it primarily owns has its evidence artifact; every blocker naming its scope is discharged
   > **Impact**: Ties Definition of Done to the acceptance vocabulary the project actually has (13 WS rows and 27 TA rows — `user-stories` is `SKIP`, so these are the only acceptance criteria Construction receives). Strict: ten units carry blockers, so several Bolts cannot close until an owner or supervisor decision lands.

B) Option A, plus the critical test set run **inside the Kaggle session** for that Bolt
   > **Impact**: FR-WS-6 and REQ-NFR-A3 require the critical tests and both fixtures to run inside Kaggle before any *governed run* executed there — because a Kaggle session carries no git working tree, so a commit hook cannot fire and a local pass proves nothing about that environment. Applying it to every Bolt would demand a Kaggle session for units that never execute a governed run there, which is cost without evidence.

C) Modules and tests only; acceptance-row evidence gathered later in one evidence Bolt
   > **Impact**: Cheapest per Bolt and the most dangerous. Evidence collected after the fact is reconstructed rather than measured, and §15.1 states that exact counts, tolerances and runtimes are measured from the fixtures and frozen, never invented. It would also let a Bolt close while an acceptance row it owns has nothing behind it.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A, with B's in-Kaggle requirement attached **only** to the Bolts whose unit actually executes a governed run on Kaggle (`acquisition`, `inventory-and-registry`, and `fixtures-and-reproducibility`). That keeps FR-WS-6 satisfied where it bites without demanding a Kaggle session from a unit that is a pure library.

[Answer]: Option A, with B's in-Kaggle requirement attached only to the Bolts whose unit actually executes a governed run on Kaggle (acquisition, inventory-and-registry, and fixtures-and-reproducibility). That keeps FR-WS-6 satisfied where it bites without demanding a Kaggle session from a unit that is a pure library.

---

## Question 7

Which outside-this-project items should the plan track as things that can hold a Bolt up? (select all that apply)

A) Owner and supervisor freeze decisions still open — the `plumbing_7day` station (BLK-02), the D-17 schema test module name (BLK-05), the canonical protected-set enumeration (BLK-06), and the three `features.yaml` F10.7 selection freezes
   > **Impact**: These have real lead time and no workaround: `project.md` § Forbidden bars any agent from filling a `TBD — freeze gate` value by convenience, and BLK-02 says outright that no manifest may be invented, inferred or substituted. Tracking them means naming who decides and what the Bolt does while it waits.

B) External data providers — Madrigal (MAPGPS `gps` under D-144), GFZ (Kp/ap3, Hp60/ap60), Kyoto WDC (hourly Dst at one release grade), Canada's Solar Radio Monitoring Program (observed F10.7), CODE final GIM, IRI-2016
   > **Impact**: Six providers, each with its own availability, citation obligation and version drift. The F10.7 archive has a documented month-long outage from 2022-03-18, and provider version drift is already observed in this dataset (`g.002` versus `g.003`). A retrieval that silently returns a different version is worse than one that fails.

C) Kaggle platform availability and its session quota
   > **Impact**: Kaggle is the only authorised compute host besides local (TC-03c — Colab and Drive are explicitly removed), and the heaviest single job (10,000 bootstrap replicates inside a 10.0 GB planning envelope) runs there. No third platform is permitted as a fallback, so a quota problem has no substitution path.

D) The AGPLv3 Global-TEC-forecasting licence question
   > **Impact**: Unresolved outside this project and gating G-P2. The standing default is already recorded — reimplement from the paper with a citation — so this one has a defined fallback rather than an open wait.

E) All of the above
   > **Impact**: The complete map, with an owner, a lead time, the Bolt it blocks and a fallback for each. Longest to write; nothing left implicit.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option E. `project.md` § Way of Working already requires that a gating condition's inputs be specified in the same stage that records the condition, and that a phase handoff enumerate every open gate rather than only those on the visible critical path. A partial dependency map is the failure mode that rule exists to prevent.

[Answer]: E

---

## Question 8

Ten of the twelve units carry an open blocker. How should their Bolts be sequenced?

A) Keep dependency order; each Bolt runs up to its blocked artifact and stops there with its gate held open
   > **Impact**: Nothing waits unnecessarily — a unit's unblocked scope still gets built. But it leaves several Bolts half-finished at once, and `unit-of-work.md` is explicit that a blocked unit is "not marked accepted, Ready or complete" — so the plan would carry several Bolts in a permanently ambiguous state.

B) Defer each blocked unit's Bolt entirely until its blocker is discharged
   > **Impact**: Every Bolt that starts can finish. But BLK-03, BLK-04 and BLK-07 are **exit** conditions on functional design, not entry conditions — the 2026-08-22 ruling says those units "may enter" that step, because that is where the contract is authored. Deferring them would make the blockers unsatisfiable, which is exactly the defect that ruling corrected.

C) Split by blocker type: front-load the owner/supervisor decisions (BLK-02, BLK-05, BLK-06) as written requests before Construction starts, and let the cross-unit contracts (BLK-03, BLK-04, BLK-07) be discharged inside functional design as their own ruling requires
   > **Impact**: Matches how each blocker is actually written. The decision-type blockers have lead time and no workaround, so asking early is the only lever available. The contract-type blockers are named as functional design's own work product, so they cannot and should not be front-loaded. The cost is that three written decision requests must be raised now.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. The blocker register distinguishes the two kinds carefully and gives each a different approval authority; treating them uniformly discards that. BLK-06 in particular blocks G-P2 and G-P3C rather than a Bolt, so it needs a request raised early even though no Bolt waits on it directly.

[Answer]: X — Before starting any Construction Bolt, identify and present all unresolved owner decisions and other true entry-blocking conditions that could stop project execution or prevent a later gate from being passed, including BLK-02, BLK-05, BLK-06, the F10.7 selection freezes, and any comparable unresolved items. For each, explain the issue, available options, recommendation, affected Bolt or gate, and the decision required from me. I will resolve and approve these decisions first. Do not invent, infer, or substitute frozen values. Once all decision-type and entry-blocking conditions are discharged and recorded, begin Construction. Contract-type blockers such as BLK-03, BLK-04, and BLK-07 must be resolved during functional design and do not block its start, but no affected Bolt or gate may be marked complete until its applicable exit conditions are satisfied.

> **Owner clarification recorded 2026-08-22**, against governance finding
> `DP-CHAIR-02` (`GOV-2026-08-22-DP-01`). The board found that this instruction
> names BLK-05 and BLK-06 among the decisions to resolve first, while the blocker
> register assigns both to functional design's own work product — so the literal
> reading was unsatisfiable for BLK-06, whose resolution *is* the derivation
> functional design performs. The owner ruled:
>
> **Functional design may begin while BLK-05 and BLK-06 remain open, but only to
> analyze those blockers and generate the evidence required for their
> resolution.** Both are presented to the owner with options, supporting evidence,
> risks and a recommendation. **Neither is marked resolved and no approval is
> assumed until the owner explicitly decides.** No dependent implementation, code
> generation, governed execution or downstream activity may begin until the
> corresponding blocker decision is approved and recorded.
>
> This narrows what functional design may *do* with these two blockers; it does
> not relocate them, close them, or alter the ruling that BLK-03, BLK-04 and
> BLK-07 are exit conditions on that stage. Carried identically in
> `bolt-plan.md` § Gate 0 and `external-dependency-map.md` § A2.

---

## Question 9

What worries you most about this build, so it gets tackled early? (select all that apply)

A) An unlogged December read — `acquisition` opens the D-9 input (`audit_evidence_2022-FULL/`, 21,258 December rows) without routing through the access-log chokepoint (BLK-07)
   > **Impact**: Not retrospectively curable. D-15 records that the restricted root is "a governance boundary, not an access control" — no permission, no ACL — so it holds only while exactly one code path reaches it, and RES-01 records that permitted-read logging is **NOT TESTED**, so nothing downstream would catch the omission.

B) A leaked transform — `fit_transforms` fitted on more than the named fold's training partition (BLK-04)
   > **Impact**: Every reported number inherits the fit, across four downstream units. It is invisible in validation and fatal on discovery, and NFR-LEAK-01's evidence is owed to the supervisor at both G-04 and G-05.

C) The confirmatory prediction built on the wrong seeds (BLK-03)
   > **Impact**: The three-seed element-wise mean *is* the confirmatory prediction. The seed values are now frozen, but the contract that gets them from `configs/seeds.yaml` into the function is not — and the two implementations available without it are both forbidden or weaker.

D) Provenance — FULL's twelve monthly runs are unverifiable in principle (no provider byte stream exists anywhere in the workspace; three months have no `raw_isprint_cache/` at all), and the re-acquisition that would fix it is still deferred
   > **Impact**: Every artifact produced before the re-acquisition carries that caveat, and FULL must not be relied on at a freeze gate while it stands. This one has no code fix — it is retrieval work.

E) The 40 requirements with no acceptance row, and the five forbidden edges that a criterion states but nothing tests
   > **Impact**: Each is a real pass/fail criterion with no §16 or §19 row behind it. Closing any of them requires a Vision §15.2 change-control amendment, which has lead time and is not this initiative's to grant.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Options A and B. Both are the kind of failure that is silent when it happens and unfixable afterwards — an unlogged December access cannot be un-taken, and a leaked fit invalidates every number computed on top of it. C, D and E are all serious, but each is either already partly closed (C), visible as a standing caveat (D), or discoverable at a gate rather than corrupting the result (E). Say so if you weigh them differently — this answer drives what the sequencing rationale front-loads.

[Answer]: E

> **Follow-up raised — see FU-2.** This question is multi-select and its option E
> is one specific item (the 40 untested requirements and the five untested
> forbidden edges), **not** an "all of the above" like Question 7's option E. A
> bare `E` therefore reads two ways. FU-2 resolves which; this tag is not
> re-interpreted here.

---

## Question 10

What should each Bolt produce that you can actually look at?

A) A runnable stage script producing a hashed release plus an experiment-registry row, for the units that own one; passing tests plus the approved contract, for the shared and embedded units
   > **Impact**: Matches this project's actual notion of a deliverable — `team-practices.md` § Deployment records that "deployment" here means immutable dataset and model releases with version, manifest, SHA-256 hashes, schema, row counts, exclusions and fold identifiers. Seven units own a stage script; five do not, and demanding one from them would be inventing work.

B) Passing tests only
   > **Impact**: Simplest and weakest. It would let a unit close without ever producing the released artifact its downstream consumers identify by release ID and hash — which is how units communicate here, since there is no database, no queue and no shared state.

C) Evidence-linked acceptance rows only
   > **Impact**: Closest to what the gates ultimately want, but several units' acceptance rows need artifacts from units built later (TA-21's traceability matrix, TA-27's hash-diff test), so this cannot be a per-Bolt bar without making early Bolts unclosable.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A. It is the only one of the three that distinguishes the seven script-owning units from the five that are shared or embedded, and that distinction is already load-bearing in the dependency graph — `fixtures-and-reproducibility`'s nine incoming edges exist for two different reasons for exactly this reason.

[Answer]: A

---

## Question 11

TC-06 requires the repository, pins **and test suite** before any acquisition work. But `acquisition` is the third unit in dependency order, and 16 of the 19 mandated test modules test units built after it. How is that squared?

A) Bolt 1 delivers the `tests/` tree, shared fixtures and conftest, plus the test modules whose subject exists at that point; every other test module is written inside its own unit's Bolt
   > **Impact**: Satisfies TC-06's checkable content — repository structure, pinned environment, and a working test suite exists and runs before acquisition — without requiring tests for modules that do not exist. Records the reading explicitly rather than leaving the tension buried.

B) All 19 test modules written in Bolt 1, failing or skipped until their subject exists
   > **Impact**: The most literal reading of TC-06. It would produce 16 modules asserting against absent code, which `phases/construction.md` forbids directly ("Do not generate tests that always pass regardless of implementation"), and a skipped test is not evidence of anything. It would also freeze test design before the design stages that specify the behaviour have run.

C) Treat TC-06 as satisfied by the scaffold and pins alone; the test suite is built per unit with no Bolt-1 test obligation
   > **Impact**: The loosest reading, and it drops the word "test suite" from a `binding: hard` constraint that `team-practices.md` § Testing Posture affirmed as binding from now on. It would also lose the guard tests that are genuinely buildable up front.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A. This is a real contradiction in the governing constraints rather than an ambiguity, and `phases/inception.md` forbids carrying an unresolved contradiction forward silently — so whichever way you rule, it gets written into the sequencing rationale with its reasoning. Option A is recommended because it keeps every checkable part of TC-06 (structure, pins, a suite that runs) while declining to produce tests that assert nothing. Honest cost: this is a narrower reading of "test suite" than the words alone carry, and it should be flagged at the next practices-affirmation gate alongside the two stale figures already tracked as RES-02.

[Answer]: A

---

## Question 12

`fixtures-and-reproducibility` depends on nine units, so the graph puts it last — yet its fixture manifests must record measured values (row counts, tolerances, CPU runtime) rather than invented ones. When is it built?

A) Strictly last, as one Bolt after the other eleven
   > **Impact**: Honest to the graph and simplest to sequence. But §15.2's thirteen manifest content areas would all be measured at the very end, and an expected CPU runtime range "measured before freeze" is easiest to get wrong when reconstructed months after the stage that produced it ran.

B) Split the unit — orchestrator skeleton early (right after `foundation`), manifests and clean run last
   > **Impact**: Gets `run_walking_skeleton.py` into existence early. But it splits one unit across two Bolts, which breaks the one-unit-per-Bolt rule from Question 1 and gives the unit two Definitions of Done and two blocker states.

C) Last as a single Bolt, but each earlier Bolt records its own measured fixture-manifest fields as it completes, and Bolt 12 assembles and freezes them
   > **Impact**: Keeps the unit whole and the graph edge honest, while the measurements are taken when each stage first becomes runnable rather than reconstructed at the end. Adds a small recording obligation to every earlier Bolt's Definition of Done. Does not touch **BLK-02** — the `plumbing_7day` station is still unselected, so the manifest still cannot state its identity regardless of when it is assembled.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. §15.1 is explicit that exact counts, tolerances and runtimes are measured from the fixtures and frozen, never invented — and the cheapest way to guarantee a measured value is to record it at the moment it is measured. The added per-Bolt obligation is one line of evidence, not a second deliverable.

[Answer]: C

---

## Follow-up questions

Two answers need one more turn before the plan can be written. Neither is a
re-ask: FU-1 is a consequence of Q5 and Q8 read together that was not visible
when either was asked, and FU-2 is a genuine ambiguity in how a bare `E` reads
on a multi-select question whose option E is not "all of the above".

### FU-1

Q5=A selects unit-major iteration — each unit is designed **and built** before
the next begins. Q8=X requires that "no affected Bolt or gate may be marked
complete until its applicable exit conditions are satisfied", and names the
contract-type blockers (BLK-03, BLK-04, BLK-07) as things functional design
discharges. Those two interact in a way worth seeing before it is written down.

**What unit-major actually does to the approval points**, stated precisely
rather than dramatically:

- The four per-stage approval gates are **unchanged in count**, but they fire
  **late and in a cascade at the very end** — after the whole (stage × unit)
  grid, code-generation included, is settled. So the functional-design gate,
  which is where a discharged BLK-04 contract would be put in front of you, does
  not fire until all twelve units are designed **and coded**.
- There **is** still a per-unit human stop before any code is written: each
  unit's code-generation hard-stops for plan approval before it generates. So
  you are not blind — but what you approve there is that unit's implementation
  plan, not its design artifacts at their formal gate.
- Under stage-major (the alternative), functional design runs for all twelve
  units and then presents **one gate before anything else happens** — so every
  cross-unit contract is approved by you before a single line of code exists.

The reason this matters to Q8 specifically: G-09 is worded "before any affected
component is coded", and §18.3 binds an agent to "stop and report rather than
choose a default" while a P0 decision is unresolved. Under unit-major those
protections rest on the per-unit code-generation plan stop; under stage-major
they rest on a formal design gate that precedes all implementation.

One thing that is **not** a problem either way, recorded so it does not get
re-litigated: every contract-type blocker is owned by a unit that comes **before**
all of its consumers in the dependency order (BLK-06 at `governance-guards` #2,
BLK-07 at `acquisition` #3, BLK-04 at `features-and-splits` #7, BLK-03 at
`models-and-baselines` #8). So under either mode the owning unit authors the
contract before any consumer needs it. The concern raised in Question 5's
recommendation was that consumers would not be "in the room"; the dependency
order answers it.

A) Switch to stage-major — each design step runs across all twelve units, one gate each, code last
   > **Impact**: Every cross-unit contract and every design artifact is formally approved by you before any implementation exists, which is the strongest available reading of G-09's "before any affected component is coded". Costs a long stretch with nothing runnable — no working code until all twelve units are designed and three gates have passed.

B) Keep unit-major, relying on the per-unit code-generation plan stop as the pre-implementation checkpoint
   > **Impact**: First working code lands after one unit's design instead of after twelve, and each unit stays coherent end to end. The pre-code checkpoint is a plan approval rather than a design gate, and the design gates arrive as a cascade at the end — so a design problem found at the gate is found after code was written against it.

C) Keep unit-major, but stop after the first unit (`foundation`) and re-decide with real experience
   > **Impact**: Buys evidence cheaply — `foundation` is the least blocked unit and its design is the most mechanical, so it is a fair trial. Costs one extra decision point, and the mode is recorded in workflow state so switching mid-Construction is a deliberate change rather than a drift.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — switch to stage-major. Your Q8 answer asks for every entry-blocking decision to be surfaced, explained and approved by you before Construction begins; stage-major is the same posture applied to the contract-type blockers, which are the ones your answer leaves inside functional design. Honest cost, stated plainly: you will not see running code for a long time, and that is a real loss on a thesis timeline. If that cost is the binding constraint, Option C gets you most of the safety while still landing `foundation` early.

[Answer]: A — Switch to stage-major. **This supersedes Q5=A.** Construction iteration stays `stage-major` (the framework default), so no `set-construction-iteration` write is made.

### FU-2

Q9 is multi-select, and its option E names one specific item — the 40
requirements with no acceptance row and the five forbidden edges nothing tests.
It is **not** an "all of the above" option, which Question 7's option E was. So a
bare `E` reads two ways.

A) Option E only — the untested requirements and forbidden edges are the priority; A–D are not front-loaded
   > **Impact**: Narrowest reading. It would leave the unlogged-December-read risk (BLK-07) and the leakage-contract risk (BLK-04) out of the sequencing rationale's front-loaded set, even though both are recorded elsewhere as blockers. Coherent only if you judge the coverage gap to dominate.

B) All five — A, B, C, D and E are all tracked and front-loaded
   > **Impact**: Matches the posture of your Q7=E and Q8=X answers, both of which asked for complete enumeration rather than a selection. The rationale artifact then ranks all five, and no risk is dropped for being ranked lower. Costs nothing except a longer risk register.

C) A and B only — the two irreversible ones
   > **Impact**: Sharpest prioritisation. An unlogged December access cannot be un-taken and a leaked transform invalidates every number computed on it; C, D and E are each either partly closed, already carried as a standing caveat, or discoverable at a gate. The other three would still be recorded, just not front-loaded.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B. Your other two answers on this axis (Q7=E, Q8=X) both chose full enumeration over selection, and `project.md` § Way of Working requires a phase handoff to enumerate every open item rather than only the visible ones. The rationale artifact will still rank them — A and B first, on irreversibility — so you get the prioritisation of option C without dropping anything.

[Answer]: B — All five. **This resolves Q9=E** as A, B, C, D and E together, ranked by irreversibility with A and B first.

---

## Assumptions & Open Questions

- **[assumption]** These questions treat the twelve units and the 23 dependency edges as settled input, not as open for revision here. Stage 2.7 owns topology; this stage chooses a path through it. If an answer below would require a different graph, that is a change to stage 2.7's artifacts and runs through its own approval, not through this file.
- **[assumption]** No question here asks for a value that is supervisor-owned or scientific. The blockers naming such values (BLK-02's station, BLK-05's module name, BLK-06's enumeration) appear only as *scheduling* questions — when the request is raised and what the Bolt does while it waits — never as a request to choose the value.
- **Open.** Whether the narrower reading of TC-06's "test suite" recommended at Question 11 needs recording at the next practices-affirmation gate alongside RES-02's two stale figures. This stage cannot edit `team-practices.md`; `org.md` reserves that file for the affirmation gate.

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
