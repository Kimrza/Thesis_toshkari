# Units Generation — Questions

Stage 2.7 (units-generation), intent `260813-tec-hourly-forecast`.
Depth: Comprehensive. Scope: `research-pipeline-governed`.

**What this stage decides, and what it does not.** 2.7 produces the dependency
**topology**; 2.8 (Delivery Planning) chooses the economic path through it. So
none of these questions asks what to build first, what the critical path is, or
whether to go value-first or risk-first — those are 2.8's. What follows asks only
how to cut the design into units and what may depend on what.

**Two ordering constraints are facts, not preferences**, and will appear as DAG
edges regardless of the answers below: `constraint-register.md` **TC-06**
(binding: hard) — "Repository structure, pinned environment and test suite are
built before any acquisition work, inside this initiative" — and **TE §9.2** — both
walking-skeleton fixtures pass, in order, before any full-year job. Neither is an
economic choice, so neither trespasses on 2.8.

**Not re-asked.** Deployment model: `team-practices.md` § Deployment settles it —
there is no staging/production split, "deployment" means immutable dataset and
model releases, and models are versioned artifacts with a registry rather than
deployed services. Integration contracts: `component-dependency.md` settles them —
units communicate through **hashed released artifacts** identified by release ID,
with no database, lock file, message queue or shared mutable state.

Answer each by filling the `[Answer]:` tag with the option letter.

---

## Q1 — What is a unit here?

Four candidate cuts, each defensible against a different artifact.

- A. **By pipeline stage** — one unit per TE §7.0 row (P1-00…P1-06), plus a scaffold unit for the TC-06 precondition.
  *Impact:* units map 1:1 onto the nine stage scripts and onto `requirements.md`'s own FR-P1-0n decomposition (Q2=A in stage 2.3), so a requirement's unit is readable from its ID. Cross-cutting modules (`config.py`, the determinism helper, `phase_contract.py`, `locked_test.py`, `release.py`) have no natural home and end up duplicated across units or arbitrarily assigned.
- B. **By `src/` package** — `data`, `external`, `features`, `models`, `evaluation`, plus scaffold.
  *Impact:* units map onto the code structure and onto `components.md`'s ownership boundaries, so the cross-cutting modules land naturally inside `data`. But a single pipeline stage then spans several units — `05_build_features_and_splits.py` touches `data`, `external` and `features` — so no unit delivers a runnable stage on its own.
- C. **Hybrid: a foundation unit, cross-cutting units, then pipeline-stage units.**
  *Impact:* the foundation (scaffold, pins, config, determinism) and the two governance guards become explicit dependency roots that everything else depends on, which is what they actually are; the remaining units still map onto runnable pipeline stages. More units, and two of them are infrastructural rather than scientific.
- D. **By governance gate** — units aligned to what a supervisor signs (G-P1A, G-04, G-05, G-06, G-07).
  *Impact:* each unit completes a gate's evidence set, which is attractive in a project this gate-driven. But gates span the whole pipeline — G-07 reproducibility touches every module — so the units would overlap heavily and the DAG would be near-complete rather than sparse.

**Recommendation: C.** A and B each break on the same fact from different sides:
the cross-cutting modules are dependency *roots* — `config.py` is imported by all
nine scripts, and the phase and locked-test guards are called by every stage
entry — and a DAG that hides its roots inside leaf units misstates the topology.
C makes them visible, keeps the remaining units runnable, and costs only two extra
units.

[Answer]: C

**Refinement supplied by the human (authoritative over the option text):**

Use a hybrid unit decomposition consisting of explicit dependency-root units followed by runnable pipeline-stage units.

Define a unit as a cohesive, independently testable implementation slice with a clear responsibility, owned artifacts, entry and exit criteria, dependencies, mapped requirements, and acceptance evidence. A unit is not necessarily identical to a Python package, source file, stage script, or governance gate.

Create explicit root units for:

1. Project scaffold, dependency pins, and TC-06 preconditions.
2. Configuration loading, snapshotting, hashing, platform resolution, and deterministic execution setup.
3. Phase-boundary enforcement and transition-contract handling.
4. Locked-test access and execution protection.

Then define the remaining scientific and processing units around the runnable Phase 1 pipeline stages, preserving traceability to the corresponding FR-P1-0n requirements and stage scripts.

Assign each shared module to exactly one owning root unit. Downstream stage units may consume its public contract but must not duplicate its implementation. Represent those relationships explicitly in the unit dependency DAG.

Treat governance gates as acceptance checkpoints over one or more units rather than as implementation units themselves. This avoids overlapping ownership while preserving gate-level evidence traceability.

For each unit, record:
- responsibility and scope;
- owned modules and scripts;
- upstream and downstream dependencies;
- mapped requirements and decisions;
- public boundary contracts;
- tests and negative controls;
- required evidence;
- completion and failure criteria.

This decomposition keeps cross-cutting controls visible as dependency roots while allowing the downstream units to deliver runnable, testable pipeline stages.

---

## Q2 — How many units?

Granularity, given Q1's cut. Counts assume C; A or B would shift them by two or
three.

- A. **Coarse — 6 to 7 units.** Foundation, acquisition, target, features-and-splits, models, evaluation, fixtures.
  *Impact:* fewest hand-offs and the smallest DAG. Each unit is large: "evaluation" would carry masks, metrics, the vector bootstrap, regimes and diagnostics — five §12 modules and eight requirements — so a single Construction gate covers a lot.
- B. **Medium — 9 to 12 units.** As above, but cross-cutting guards split out and evaluation split into comparison-mechanics and reporting.
  *Impact:* each unit is reviewable in one sitting and maps to at most three §12 modules. The design stages (3.1–3.3) run per unit, so this multiplies gate count by roughly the unit count.
- C. **Fine — 15 or more units**, roughly one per §12 module group.
  *Impact:* maximum parallelism visible in the DAG and the smallest possible blast radius per unit. For a single author it is mostly overhead: `project.md` records this as a single-author thesis codebase, so parallel development opportunity has no one to allocate to.

**Recommendation: B.** C's parallelism is worth nothing here — there is one
author — and its cost is real, because every Construction design stage runs per
unit. A's evaluation unit is the problem case: it would put the confirmatory
estimand, the vector bootstrap and the regime rule behind one gate, and those are
three of the project's most governance-sensitive items.

[Answer]: B

**Refinement supplied by the human (authoritative over the option text):**

Use a medium-granularity decomposition of approximately 9-12 units, consistent with the hybrid architecture selected in Q1.

Define units around meaningful ownership boundaries and reviewable acceptance criteria rather than forcing an arbitrary count.

Separate the principal cross-cutting controls, including:

- Foundation and dependency management.
- Configuration, platform resolution, and determinism.
- Phase-boundary enforcement.
- Locked-test protection.

Organize the remaining units around coherent, runnable Phase 1 pipeline capabilities, including acquisition, target preparation, feature construction and splits, models and baselines, evaluation, statistical inference, reporting, and reproducibility.

Avoid concentrating the confirmatory LSTM-versus-IRI comparison, bootstrap inference, regime analysis, and reporting within a single oversized evaluation unit. Split these responsibilities where doing so provides distinct acceptance evidence and reduces governance risk.

Each unit should have one clear owner, explicit upstream dependencies, mapped requirements, owned artifacts, negative controls where applicable, and independently reviewable completion criteria.

Keep the dependency graph sparse, avoid duplicate module ownership, and minimize unnecessary Construction gates. Because this is a single-author thesis project, do not create additional units solely to expose theoretical parallelism.

Select the final count based on actual module boundaries and governance-sensitive responsibilities; 9-12 units is the target range, not a requirement to manufacture unnecessary units.

---

## Q3 — Where do the cross-cutting modules live?

`config.py` (with the determinism helper), `phase_contract.py`,
`locked_test.py` and `release.py` are called by every stage. ADR-10's amendment
covering two of them is **unsigned**.

- A. **One "foundation" unit** holding scaffold, pins, configs, `config.py`, the determinism helper and `release.py`; the two guards as a second "governance-guards" unit.
  *Impact:* two clean dependency roots. The guards unit carries both unsigned-amendment files (`locked_test.py` plus `test_determinism.py`), so the amendment's exposure is contained in one unit a reviewer can see.
- B. **All of it in one foundation unit.**
  *Impact:* a single root and the simplest DAG. That unit then owns the scaffold, the config loader, determinism, both governance guards and release hashing — the largest unit in the plan, and it gates everything.
- C. **Each cross-cutting module folded into the unit that first needs it.**
  *Impact:* no infrastructural units at all. `config.py` would land in acquisition because that runs first, which makes every later unit depend on acquisition for a reason that has nothing to do with acquisition — a false edge in the DAG.
- D. **A and B's split, plus `release.py` in its own unit** because release integrity is gated separately (TA-15).
  *Impact:* release hashing is independently reviewable, which suits a project where hash integrity has already failed once (`DATA-01`). Three infrastructural units before any science.

**Recommendation: A.** C is the one to avoid: it manufactures dependency edges
that misdescribe why a unit is blocked, which is precisely what the DAG exists to
get right. D is defensible on the `DATA-01` history, but `release.py` is small and
sits naturally with the hashing the foundation already owns.

[Answer]: A

**Refinement supplied by the human (authoritative over the option text, and it overrides option A's placement of `test_determinism.py`):**

Define two explicit cross-cutting dependency-root units: Foundation and Governance Guards.

The Foundation unit owns:

- Project scaffold and dependency pins.
- Approved configuration files and `config.py`.
- Configuration loading, snapshotting, and hashing.
- Determinism and seed-management helpers.
- Platform/path-resolution helpers.
- `release.py` and shared release-integrity hashing.
- Foundation-owned tests, including `test_determinism.py`.

The Governance Guards unit owns:

- `phase_contract.py` and phase-boundary enforcement.
- `locked_test.py` and governed locked-test access.
- Independent import-limb and produced-field checks.
- Pre-G-05 access logging and evaluation restrictions.
- The corresponding guard and negative-control tests.

Map downstream scientific stage units explicitly to these root units according to the contracts they consume. Do not assign shared modules to the first pipeline stage that happens to import them, because doing so creates misleading dependencies and ownership.

Keep `release.py` within Foundation unless TA-15 demonstrably requires an independently gated release unit.

Track ADR-10 approval separately from module ownership. Identify every file covered by the unsigned amendment, associate each with its correct owning unit, and prevent affected units from being marked fully approved until the amendment is formally recorded and approved by the authorized project decision owner.

Do not move `test_determinism.py` into Governance Guards merely to concentrate amendment exposure; its ownership must remain aligned with the Foundation determinism capability.

---

## Q4 — What does `unit-of-work-story-map.md` contain, with no stories?

`user-stories` (2.4) is **SKIP** in this scope, so no `stories.md` exists. The
stage's `produces` list fixes the filename, so the question is what fills it.
`team-practices.md` records that §16's WS rows and §19's TA rows are consequently
the only acceptance vocabulary Construction will receive.

- A. **Map requirement IDs to units** — every `REQ-ENG-*`, `FR-P1-*`, `FR-WS-*`, `REQ-NFR-*` and `REQ-CLAIM-01` assigned to its implementing unit, with coverage verified both ways.
  *Impact:* directly usable by 3.1, which needs to know which requirements a unit must satisfy. 94 rows to assign, and it says nothing about *acceptance*.
- B. **Map WS and TA acceptance rows to units** — WS-09…WS-20 and the applicable TA rows assigned to the unit that produces their evidence.
  *Impact:* each unit gains an explicit acceptance set, which is what a Construction gate actually checks. Leaves the 40 requirements with no §16/§19 row unmapped — and those are the ones most at risk of being dropped.
- C. **Both, as two tables**: requirement-to-unit for completeness, and acceptance-row-to-unit for verification, with the untested-requirement list called out per unit.
  *Impact:* every requirement has a home and every unit has an acceptance set, and the per-unit view of untested requirements is exactly what `nfr-requirements` (3.2) needs for the G-05 freeze manifest. The largest of the three artifacts.
- X. Other (please specify)

**Recommendation: C.** B alone would silently drop the 40 untested requirements,
which is the failure this project's governance has caught repeatedly — a row that
looks covered because nothing lists it as uncovered. A alone gives Construction no
acceptance criteria, and with 2.4 skipped there is no other source for them.

[Answer]: C

**Refinement supplied by the human (authoritative over the option text):**

Populate `unit-of-work-story-map.md` with two complementary traceability tables instead of inventing user stories.

Explicitly state that user-stories stage 2.4 was intentionally skipped and that no `stories.md` artifact exists. Use approved requirements and existing acceptance rows as the authoritative substitutes for story-based mapping.

Table 1: Requirement-to-unit traceability.

Assign every applicable `REQ-ENG-*`, `FR-P1-*`, `FR-WS-*`, `REQ-NFR-*`, `REQ-CLAIM-01`, and other approved in-scope requirement to exactly one primary implementing unit. Record any supporting units separately where responsibility genuinely crosses boundaries.

Table 2: Acceptance-to-unit traceability.

Map every applicable WS-09 through WS-20 and each applicable TA row to the unit responsible for producing its acceptance evidence. Identify the required tests, artifacts, gate, and evidence location where known.

Include a per-unit coverage summary identifying:

- Assigned requirements.
- Applicable WS and TA acceptance rows.
- Requirements without an existing acceptance row.
- Acceptance rows without an assigned evidence owner.
- Cross-unit dependencies.
- Open verification gaps and their responsible owners.

Do not fabricate user stories, acceptance rows, test results, or governance approvals. Mark requirements lacking existing acceptance coverage explicitly as NO CURRENT ACCEPTANCE ROW and carry them forward to functional-design 3.1 and nfr-requirements 3.2 for verification planning.

If closing a verification gap requires amending governed WS or TA artifacts, record the proposed amendment and obtain approval from the authorized project decision owner before treating the new criterion as official.

Validate coverage in both directions: every in-scope requirement must have an implementing owner, and every applicable acceptance row must have an evidence-producing owner.

---

## Q5 — Do Phase 2 modules become units now?

`src/gnss` is in §12's tree, Phase 1 is barred from executing it (§7.0), and
ADR-09 designed its **boundary only** — responsibilities and the transition
contract, no internals.

- A. **No Phase 2 units.** The DAG covers Phase 1 plus one "phase-transition" unit owning `phase_contract.py`'s manifest and the G-P2 checks.
  *Impact:* the DAG describes work that can actually start, and the transition unit gives G-P2 an owner. Phase 2 gets its own units when it is designed, which is consistent with ADR-09 declining to specify interiors.
- B. **Include `src/gnss` units, marked Phase 2 and blocked.**
  *Impact:* the whole two-phase shape is visible in one DAG. Those units cannot be estimated or designed — ADR-09 deliberately left their interiors unspecified — so they would carry no complexity estimate and no design artifacts, which makes them placeholders rather than units.
- C. **One single "phase-2-raw-processing" unit** as an explicit placeholder.
  *Impact:* one honest marker that Phase 2 exists and is out of scope, without pretending to decompose it. Adds a unit that Construction will never build.

**Recommendation: A.** B's units would be undesignable by construction, and 2.8
would then have to sequence work it cannot estimate. The phase-transition unit is
the part that genuinely belongs to Phase 1 — the manifest is produced *by* Phase 1,
and G-P2 gates on it.

[Answer]: A

**Refinement supplied by the human (authoritative over the option text, and it overrides option A's separate phase-transition unit):**

Do not create executable or planned implementation units for Phase 2 `src/gnss` modules during the current Phase 1 decomposition.

Limit the unit dependency graph to work that is in scope, sufficiently specified, independently reviewable, and eligible to begin under the current phase restrictions.

Represent Phase 2 only through its approved transition boundary: the Phase 1 handoff artifacts, observed schemas, artifact hashes, configuration hashes, frozen decisions, provenance, locked-test protections, and G-P2 transition checks.

Maintain consistency with Q3: `phase_contract.py` remains owned by the Governance Guards unit. Assign responsibility for producing the phase-transition manifest and associated G-P2 evidence to that unit unless a separately justified transition unit is introduced with explicit, non-overlapping module ownership.

Do not create blocked `src/gnss` implementation units or a placeholder Construction unit for work whose internal design, estimates, and acceptance criteria are intentionally undefined under ADR-09.

Document `src/gnss` modules as Phase 2 responsibilities outside the current implementation scope. Generate their actual units only when Phase 2 is formally authorized and its internal functional design can be specified from approved, evidence-backed requirements.

The current DAG must include the Phase 1 transition boundary but must not imply authorization to import, execute, design internally, or implement Phase 2 raw-processing modules.

---

## Q6 — Which `kind` does each unit carry?

`kind` drives which Construction design artifacts apply: a `spec` owes no
scalability document, a `packaging` unit no business-logic model. The allowed
values are `service | spec | ui | packaging | library`. This pipeline has **no
deployed executable and no frontend**, so `service` and `ui` do not apply.

- A. **`library` for every `src/` unit, `packaging` for the foundation/scaffold unit.**
  *Impact:* accurate — the `src/` packages are reusable code with no standalone runtime, and the scaffold is build and distribution artefacts. Every `src/` unit then receives the full library design-artifact matrix.
- B. **As A, plus `spec` for the configuration-contract and phase-transition units.**
  *Impact:* the four governed configs and the transition manifest are consumed-in-place contracts rather than code, so `spec` fits and correctly relieves them of runtime design artifacts. Requires those to be separate units, which Q3=A and Q5=A both give.
- C. **Leave `kind` off entirely.**
  *Impact:* every unit receives the full design-artifact matrix, so nothing is under-designed. Also means each unit owes design documents that do not apply — a scalability document for a YAML contract — which is how a stage produces filler.

**Recommendation: B.** It is the most accurate description of what each unit *is*,
and `kind` exists precisely to stop a unit owing artifacts that make no sense for
it. C's failure mode is filler, which is worse than a missing document because it
looks like coverage.

[Answer]: X

**Human-specified `kind` assignment rule (supersedes options A, B and C):**

Assign each unit `kind` according to its actual owned artifacts and executable responsibilities, rather than labeling units by the presence of configuration files or manifests.

Use:

- `packaging` for a unit limited to project scaffold, dependency pins, installation, build, and distribution artifacts.

- `library` for any unit that owns executable Python code, reusable modules, runtime guards, configuration loaders, determinism helpers, release hashing, model logic, evaluation logic, or phase-transition validation.

- `spec` only for a genuinely separate, non-executable unit that owns schemas, governed configuration contracts, manifest definitions, or other consumed-in-place specifications without implementing runtime behavior.

Do not classify a unit containing `config.py` as `spec`: configuration loading, validation, snapshotting, hashing, and seed initialization are executable responsibilities requiring applicable library design and test artifacts.

Likewise, do not classify the existing Governance Guards unit as `spec` merely because `phase_contract.py` produces or validates a transition manifest. Runtime phase enforcement and locked-test protection remain library responsibilities.

Preserve the ownership decisions from Q3 and Q5. If the Foundation unit continues to own both packaging artifacts and executable shared code, classify it as `library` or split it into distinct packaging and foundation-library units only when the additional unit is justified.

Do not create artificial `spec` units solely to reduce Construction documentation. Existing YAML files and manifests can remain specification artifacts owned by a `library` unit without changing that unit's `kind`.

Never use `service` or `ui` for this project unless the approved scope changes to include a deployed service or a user interface.

---

## Q7 — Does the DAG record parallel-development opportunities?

The stage asks for "sets of units with no dependency between them". `project.md`
records this as a single-author thesis codebase.

- A. **Yes, record them.** The DAG states which units are mutually independent, whoever ends up building them.
  *Impact:* a property of the topology, true regardless of staffing, and it is what 2.8 needs to know which orderings are legal. Costs nothing and presumes nothing.
- B. **No** — with one author there is no parallelism to exploit, so recording it is noise.
  *Impact:* smaller artifact. Also withholds from 2.8 the information it needs to choose among valid orderings, and quietly bakes a staffing assumption into a topology document.

**Recommendation: A.** Independence is a fact about the graph; who works on it is
2.8's and the author's business. B would encode a staffing assumption in the wrong
artifact.

[Answer]: A

**Refinement supplied by the human (authoritative over the option text):**

Record independent unit sets as a property of the dependency graph, without implying that development will occur in parallel.

Identify units that can legally begin once their shared prerequisites are satisfied and that do not depend on each other's implementation, artifacts, approvals, or acceptance evidence.

Use these independence sets to inform stage 2.8 sequencing, alternative valid implementation orders, and recovery options when one unit is temporarily blocked.

Explicitly state that this is a single-author thesis project and that independent units will normally be implemented sequentially. Independence describes permissible ordering, not staffing, concurrent execution, or a commitment to parallel development.

Do not mark units as independent when they share an unresolved governance prerequisite, require an unsigned amendment, depend on locked-test authorization, or would violate Phase 1 boundaries.

Keep the DAG sparse and evidence-backed: include genuine dependency edges, identify valid independent sets, and avoid manufacturing parallelism or adding false edges for administrative convenience.

---

## Consolidated Summary Confirmation

**Mode:** self-guided (answers supplied by the human in chat, written back to this file verbatim).

### Answers as recorded

- **Q1 = C** (hybrid) — a unit is a cohesive, independently testable implementation slice with owned artifacts, entry/exit criteria, dependencies, mapped requirements and acceptance evidence; explicitly *not* necessarily a Python package, source file, stage script or governance gate. Four capability roots named: scaffold/pins/TC-06, configuration+determinism, phase-boundary, locked-test. Each shared module has exactly one owning root unit; downstream units consume its public contract and never duplicate it. Governance gates are acceptance checkpoints over units, never units themselves.
- **Q2 = B** (9–12 units, as a target range and not a quota). Cross-cutting controls separated; remaining units organised around runnable Phase 1 capabilities: acquisition, target preparation, features and splits, models and baselines, evaluation, statistical inference, reporting, reproducibility. The confirmatory comparison, bootstrap inference, regime analysis and reporting must not sit in one oversized evaluation unit. No unit created solely to expose theoretical parallelism.
- **Q3 = A**, with an override: two root units, **Foundation** (scaffold, pins, configs + `config.py`, snapshot/hash, determinism and seed helpers, platform/path resolution, `release.py`, and `test_determinism.py`) and **Governance Guards** (`phase_contract.py`, `locked_test.py`, import-limb and produced-field checks, pre-G-05 access logging, guard and negative-control tests). `test_determinism.py` stays in Foundation — option A had placed it in the guards unit and that placement is rejected. `release.py` stays in Foundation unless TA-15 demonstrably requires an independently gated release unit. ADR-10 approval is tracked separately from ownership: every file the unsigned amendment covers is identified and associated with its owning unit, and no affected unit is marked fully approved until the amendment is recorded and approved by the authorized project decision owner.
- **Q4 = C** — `unit-of-work-story-map.md` states plainly that 2.4 was skipped and no `stories.md` exists, then carries two tables: requirement-to-unit (every in-scope requirement to exactly one primary implementing unit, supporting units recorded separately) and acceptance-to-unit (WS-09…WS-20 and each applicable TA row to its evidence-producing unit, with tests, artifacts, gate and evidence location where known). A per-unit coverage summary lists assigned requirements, applicable WS/TA rows, requirements with **NO CURRENT ACCEPTANCE ROW**, acceptance rows with no evidence owner, cross-unit dependencies, and open verification gaps with owners. Nothing fabricated; gaps carry forward to 3.1 and 3.2. Any amendment to governed WS/TA artifacts needs approval before it counts as official. Coverage validated in both directions.
- **Q5 = A**, with an override: no executable or planned Phase 2 `src/gnss` units, and **no separate phase-transition unit** — `phase_contract.py` stays owned by Governance Guards, which also owns the phase-transition manifest and G-P2 evidence unless a separately justified transition unit with non-overlapping ownership is introduced later. Phase 2 is represented only through its approved transition boundary (handoff artifacts, observed schemas, artifact and configuration hashes, frozen decisions, provenance, locked-test protections, G-P2 checks). No blocked `src/gnss` units and no placeholder Construction unit. The DAG includes the transition boundary but implies no authorization to import, execute, design internally, or implement Phase 2 raw-processing modules.
- **Q6 = X** (human-specified rule, superseding A/B/C) — `kind` follows actual owned artifacts and executable responsibilities: `packaging` only for a unit limited to scaffold/pins/install/build/distribution; `library` for any unit owning executable Python (runtime guards, config loaders, determinism helpers, release hashing, model logic, evaluation logic, phase-transition validation); `spec` only for a genuinely separate non-executable unit owning schemas, governed config contracts or manifest definitions. A unit containing `config.py` is never `spec`. Governance Guards is never `spec` merely because `phase_contract.py` emits a manifest. No artificial `spec` units to shed Construction documentation; YAML files and manifests can remain specification artifacts owned by a `library` unit. `service` and `ui` are never used unless the approved scope changes.
- **Q7 = A**, framed as topology rather than staffing: record independent unit sets (units that may legally begin once shared prerequisites are met and do not depend on each other's implementation, artifacts, approvals or acceptance evidence), for 2.8 sequencing, alternative valid orders and recovery when a unit is blocked; state explicitly that this is a single-author thesis project and independent units will normally be implemented sequentially. Units are **not** independent when they share an unresolved governance prerequisite, need the unsigned amendment, depend on locked-test authorization, or would breach Phase 1 boundaries.

### Reconciliations I will apply when writing the artifacts

These follow from the answers rather than adding to them, and are listed so they are confirmed rather than assumed:

1. **Q1's four capability roots become Q3's two units.** Q1 names four cross-cutting capabilities; Q3 answers at unit level and groups them as Foundation (roots 1 and 2) and Governance Guards (roots 3 and 4). Q3 governs the unit count.
2. **Foundation's `kind` is `library`, not split.** Q3 puts scaffold and pins inside Foundation alongside executable shared code, and Q6 says such a unit is `library` and is split only when the extra unit is justified. No justification exists yet, so Foundation is one `library` unit and no `packaging` unit is created.
3. **Determinism primitives and the reproducibility unit are different things.** Foundation owns the seed/determinism helpers and `test_determinism.py` (Q3). Q2's reproducibility unit owns the ordered clean-run contract (TE §13.2), `test_clean_run.py`, WS-20 and TA-17 — orchestration evidence over the whole pipeline, not the primitives.
4. **No `spec` unit is expected to exist.** Under Q6's rule the four governed configs are specification artifacts owned by Foundation (a `library` unit), and the transition manifest is owned by Governance Guards (also `library`). If the final decomposition produces a genuinely non-executable unit, it will carry `spec`; otherwise every unit is `library`.
5. **TC-06 and TE §9.2 appear as DAG edges only.** Both are ordering facts, so they become dependency edges; no critical path, build order or sequencing recommendation appears in any 2.7 artifact — that is 2.8's decision.

6. **Corrected on the second attempt.** The first attempt described `fixtures-and-reproducibility`'s edges as reaching "all nine script-owning units". Nine units is right; "script-owning" is not. Seven of them own a stage script the clean-run sequence invokes directly; `statistical-inference` and `regimes-diagnostics-reporting` own no stage script at all — their logic runs inside `07_evaluate_and_report.py`, which `evaluation-and-comparison` owns — so their two edges exist because the clean run consumes their released artifacts and evidence. The DAG is unchanged: still 12 units and 23 edges, still acyclic.

### Carried to the gate, not resolved here

- ADR-10's §12/§13.2 amendment is unsigned, so units owning `src/data/config.py`, `src/data/locked_test.py` and `tests/test_determinism.py` have no authority backing for those files yet (Q3 requires this be tracked per unit).
- `application-design` § Known defects row 12 blocks the `plumbing_7day` fixture manifest that the fixture unit must read.
- The two `application-design` signature defects (`three_seed_mean`, `fit_transforms`) sit inside units this stage draws.

---

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
