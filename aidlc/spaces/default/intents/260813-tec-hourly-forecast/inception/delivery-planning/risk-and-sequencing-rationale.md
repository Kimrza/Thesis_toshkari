# Risk and Sequencing Rationale — Hourly VTEC Forecasting (TEC_Project Phase 1)

Stage 2.8 (`delivery-planning`), intent `260813-tec-hourly-forecast`.

## Sources

- `bolt-plan.md` — the twelve-Bolt sequence this document justifies.
- `../units-generation/unit-of-work-dependency.md` — the 23 edges, the one independent pair, and the topological order this sequence is checked against.
- `../units-generation/unit-of-work.md` — the blocker register BLK-01…BLK-07 and the residual obligations RES-01…RES-03, which supply most of the risk register below.
- `../units-generation/unit-of-work-story-map.md` — the 36 requirements with no acceptance row and the per-unit untested breakdown, which is the coverage risk. (Superseded literal, preserved: "the 40 requirements with no acceptance row"; corrected 2026-08-22, a site the `CR-2026-08-22-INC-CORRECTIONS` Rec 5 sweep did not reach.)
- `../application-design/components.md` — the forbidden edges and the import allowlist, whose enforcement points drive the leakage risks.
- `../requirements-analysis/requirements.md` — § Known defects, § Open supervisor gates, § Constraints.
- `../practices-discovery/team-practices.md` — § Walking Skeleton (`skeleton: off` and why), § Testing Posture (§18.3 as the real quality gate), § Deployment.
- Stage answers: `delivery-planning-questions.md` Q2, Q3, Q8, Q9, FU-1, FU-2.
- **Absent by scope design:** `stories` (`../user-stories/stories.md`), `mockups` (`../refined-mockups/`) — stages 2.4, 1.6 and 2.5 are `SKIP`. Their absence is itself a recorded risk (R-06 below), because it leaves the §16 and §19 rows as Construction's only acceptance vocabulary.

## The heuristic, and why not the others

A **Bolt** is one build pass over a piece of the work, ending in something that
runs. The order of the twelve Bolts is **strict dependency order, with risk used
only to break the one tie the graph actually leaves** (Q2=A).

Four heuristics were weighed:

| Heuristic | Origin | Why it was not used |
|---|---|---|
| **WSJF** — score value, time-criticality and risk reduction, divide by job size, ship highest first | Reinertsen, *Principles of Product Development Flow*; SAFe | The graph has 23 edges over 12 units and exactly **one** independent pair, so scores cannot change a single ordering decision. Recording a scoring model that cannot affect the order would put invented value numbers into a governed artifact — the shape `project.md` § Way of Working forbids. |
| **Walking-skeleton first** — build a thin end-to-end slice that proves the architecture, then add features | Cockburn, *Crystal Clear* | Barred in practice, and separately switched off. The scope file declares `skeleton: off`. Even if it did not, a single end-to-end row cannot be produced before the units that enforce the Phase 1 prohibition, the locked-December guard and the fixture ordering contract exist. |
| **Risk-first** — front-load the highest-uncertainty work | Boehm, Spiral Model | Adopted **as the tie-break**, not as the ordering rule, because the graph permits front-loading in exactly one place. Applied there — see the deviation below. |
| **Value-first** — order by what most advances the result | — | Illegal on this graph. Models and evaluation cannot precede features, which cannot precede the target and drivers. It would also invert TC-06. |

**Strict dependency order was chosen because the graph is near-linear and the two
ends are pinned by constraints, not preference.** TC-06 (`binding: hard`) puts the
repository, pinned environment and test suite before any acquisition work, which
fixes `foundation` and `governance-guards` at the front.
`fixtures-and-reproducibility`'s nine incoming edges fix it at the back.

## The one deviation, and the argument for it

**Bolts 5 and 6 swap the presentation order of the upstream artifact:
`external-products` is built before `target-standardization`.** Everything else
follows the dependency order.

This is legal, not a violation. The two units are the graph's **only independent
pair** — neither depends on the other; both depend on `inventory-and-registry`
and nothing else in the fork. Either order is a valid topological order. Choosing
between them is precisely the economic judgment this stage owns, and it is the
only such judgment the graph leaves.

**The argument (Q3=B): front-load the uncertainty you do not own.**

The two units carry asymmetric kinds of risk:

- `external-products` depends on **four outside providers** — GFZ for Kp/ap3 and
  Hp60/ap60, Kyoto WDC for hourly Dst, Canada's Solar Radio Monitoring Program
  for observed F10.7, and the CODE final GIM — plus IRI-2016 generation, which is
  **blocked if its validation report fails**. Its problems are of a kind that is
  discovered only by trying: a documented month-long F10.7 outage from 2022-03-18,
  Dst release grades that must not be mixed within one series, provider version
  drift already observed in this dataset (`g.002` versus `g.003`), and a GIM
  network-overlap audit whose result must be disclosed before any independence
  claim. It is the larger unit (complexity L) and carries **four of its seven
  requirements with no acceptance row** — the second-highest untested proportion
  of any unit in the plan, behind `models-and-baselines` at seven of nine.
  <!-- Corrected 2026-08-22, two separate defects at one site.
       (1) Superseded literal, preserved: "five of its seven requirements with no
       acceptance row". external-products fell 5 → 4 under
       CR-2026-08-22-LEAKAGE-TA, which gave FR-P1-04-17 acceptance row TA-36.
       Derived from unit-of-work-story-map.md Table 1 before assertion:
         awk -F'|' '/NO CURRENT ACCEPTANCE ROW/ {gsub(/[` *]/,"",$3); print $3}' \
           unit-of-work-story-map.md | sort | uniq -c
       -> external-products 4 of 7; per-unit values sum to 36.
       (2) "the highest untested proportion of any unit in the plan" was wrong
       when written, independently of the count: 5/7 = 71% was already below
       models-and-baselines at 7/9 = 78%. At 4/7 = 57% it is further wrong. A
       site the CR-2026-08-22-INC-CORRECTIONS Rec 5 sweep did not reach. -->
<!-- markdownlint-disable-line -->
- `target-standardization` is complexity M, carries six requirements with one
  untested, and its single open blocker (BLK-05, the D-17 target-schema test's
  missing module name) is a **naming decision inside this project's own control**.

Front-loading `external-products` buys a month of schedule warning if a provider
problem is real. Front-loading `target-standardization` would buy nothing
comparable, because its open item cannot be resolved faster by being reached
sooner — it needs a supervisor-authority tree amendment either way.

**Honest cost of the deviation, stated rather than buried.** The D-17 target
contract is the single most-consumed artifact downstream — every feature, model,
metric and figure rests on it — and this order delivers it one Bolt later.
`features-and-splits` therefore waits marginally longer for its primary input,
though not longer overall, since it depends on both units and cannot start until
both are done. And BLK-05's tree amendment is reached later, which is why the plan
raises it as a written request at **Gate 0** rather than waiting for Bolt 6.

### The deviation is conditional, and the condition is now recorded

Added 2026-08-22 against governance finding `DP-TEC-01`, which found the whole
argument above resting on an upstream assumption the rationale never carried.

**The swap is legal only while the two units remain independent.** That
independence is itself an assumption recorded in
`unit-of-work-dependency.md` § Assumptions & Open Questions:
`external-products` takes its edge from `inventory-and-registry` because IRI and
GIM are generated at the registry's pinned coordinates and cells — with the
explicit caveat that if IRI generation instead needs the standardized target's
timestamp set, *"this edge moves and the one independent pair disappears"*.

**Functional design must settle which timestamp set IRI generation requires:**

- **Registry or inventory timestamps** — the assumption holds, the pair stays
  independent, and this Bolt order stands unchanged.
- **The finalized standardized-target timestamp set** — the assumption fails.
  `external-products` gains a dependency on `target-standardization`, the pair is
  no longer independent, and **the dependency relation and the Bolt order must
  both be revised before any dependent implementation begins.** Revising the edge
  is a change to the stage 2.7 dependency artifact and runs through its own
  approval, not through this plan.

**An invalid ordering must not be silently preserved once the assumption
changes.** If the edge moves and the order is not revised, this rationale would
be justifying a dependency-order violation as an economic choice — the failure
mode this finding exists to prevent.

**Independent of which way it resolves.** The final LSTM-versus-IRI comparison
must use the **same eligible timestamps** under a scientifically defensible
alignment contract, joined onto the frozen comparison-wide mask at evaluation
time. That is a comparison-fairness obligation under NFR-FAIR-01, not a
build-order convenience, and it binds whichever timestamp set IRI generation
turns out to need.

## Sequence legality check

The chosen order, checked edge by edge against the 23-edge block rather than
asserted:

| Bolt | Unit | Depends on | All dependencies at a lower Bolt number? |
|---|---|---|---|
| 1 | `foundation` | — | yes (root) |
| 2 | `governance-guards` | `foundation` (1) | yes |
| 3 | `acquisition` | `foundation` (1), `governance-guards` (2) | yes |
| 4 | `inventory-and-registry` | `acquisition` (3) | yes |
| 5 | `external-products` | `inventory-and-registry` (4) | yes |
| 6 | `target-standardization` | `inventory-and-registry` (4) | yes |
| 7 | `features-and-splits` | `target-standardization` (6), `external-products` (5), `governance-guards` (2) | yes |
| 8 | `models-and-baselines` | `features-and-splits` (7) | yes |
| 9 | `evaluation-and-comparison` | `models-and-baselines` (8), `external-products` (5) | yes |
| 10 | `statistical-inference` | `evaluation-and-comparison` (9) | yes |
| 11 | `regimes-diagnostics-reporting` | `statistical-inference` (10) | yes |
| 12 | `fixtures-and-reproducibility` | 3, 4, 5, 6, 7, 8, 9, 10, 11 | yes |

**23 dependency relations checked, 23 satisfied.** No Bolt starts before a unit
it depends on has been built.

## Why Bolts run one at a time

`unit-of-work-dependency.md` § Independent unit sets already records that
independent units will normally be implemented sequentially, because this is a
single-author thesis codebase. With exactly one independent pair, parallel
execution could apply to one pair of Bolts and would save nothing real for one
author — while giving one approval gate covering two unrelated bodies of work, so
a problem in one would be approved alongside the other's success. Serial
execution also forgoes nothing: the Q3 sequencing judgment above only exists
because the pair is built in an order.

Autonomous batches were rejected outright (Q4=A). §18.3 binds an agent to *"stop
and report rather than choose a default"* while a P0 decision is unresolved, and
ten of the twelve units carry an open or inherited blocker. Unattended building is
the wrong mode for this project.

## Why the design steps run across all units before code

Recorded here because it is a sequencing decision, though its mechanism lives in
`bolt-plan.md`. Construction runs **stage-major** — functional design for every
unit and its gate, then NFR requirements and its gate, then NFR design, then code
generation last — rather than designing and building one unit completely before
the next.

The reason is specific rather than stylistic. **Four of the six open blockers
(BLK-03, BLK-04, BLK-06, BLK-07) require cross-unit contracts authored at
functional design**, and three are recorded as **exit conditions on that stage**
for several units at once. Stage-major's functional-design gate fires **before any
code exists**, which is the strongest available reading of G-09's *"before any
affected component is coded"*.

A counter-argument was weighed and does not survive: under either mode, every
contract's **owning** unit precedes all its consumers in the dependency order
(BLK-06 at `governance-guards` #2, BLK-07 at `acquisition` #3, BLK-04 at
`features-and-splits` #7, BLK-03 at `models-and-baselines` #8), so the contract
would exist before it was needed either way. What the unit-at-a-time mode would
have cost is not contract *availability* but human *review timing*: its design
gates fire as a cascade at the very end, after every unit is coded, leaving the
per-unit code-generation plan stop as the only pre-implementation checkpoint.

**The cost of the chosen mode is real and was accepted knowingly: no running code
lands until all twelve units are designed and three approval gates have passed.**
On a thesis timeline that is a genuine loss.

## Risk register

Five risk classes were tracked (Q9, resolved at FU-2 to all five), **ranked by
irreversibility** — whether the damage can be undone once it happens, not by how
likely it is. That ranking is the reason R-01 and R-02 are front-loaded and the
others are tracked without being front-loaded.

### R-01 — An unlogged December read

| Field | Value |
|---|---|
| **Risk** | `acquisition` opens the D-9 input (`audit_evidence_2022-FULL/`, which carries 21,258 December rows) or writes re-acquired December bytes without routing through the access-log chokepoint |
| **Likelihood** | Medium — the routing contract is not yet authored (**BLK-07**), and the restricted root has no filesystem enforcement |
| **Impact** | **Critical** |
| **Why it ranks first** | **Not retrospectively curable.** D-15 records that the restricted root is *"a governance boundary, not an access control"* — no permission, no ACL, no encryption — so it holds only while exactly one code path reaches it. A second sanctioned path is not a weaker boundary; it is none. And **RES-01** records that permitted-read access logging is **NOT TESTED**, so nothing downstream would catch the omission. A December access with no record breaches Vision §8.3, D-15 and FR-P1-02-3, and is curable only as a retrospective entry |
| **Mitigation** | Front-loaded. BLK-07 is discharged at functional design as an **exit** condition on that stage for `acquisition`; **no acquisition run touches calendar 2022-12** while it stands. Bolt 3's Definition of Done requires the routing to be in place and demonstrated with an access-log sample |
| **Affected** | Bolt 3; reaches G-P1A, G-05 and G-06 |

### R-02 — A leaked transform

| Field | Value |
|---|---|
| **Risk** | `fit_transforms` is fitted on more than the named fold's training partition — its `train` argument is typed as an unconstrained DataFrame, so the full-dataset fit stays representable (**BLK-04**) |
| **Likelihood** | Medium — the two-function split prevents the single-call convenience shape and nothing more |
| **Impact** | **Critical** |
| **Why it ranks second** | Every reported number in four downstream units inherits the fit. It is **invisible in validation and fatal on discovery** — the failure mode that most reliably invalidates a forecasting result, and the one NFR-LEAK-01 exists to prevent |
| **Mitigation** | Front-loaded. BLK-04's governed contract is authored at functional design and must define allowed partitions (the named fold's training partition only) and failure conditions — a `LeakageError` when `train`'s index is not a subset of that partition, so the leak is closed **by contract rather than by review**. NFR-LEAK-01's evidence is owed to the supervisor at G-04 and G-05 |
| **Affected** | Bolt 7 owns it; Bolts 8, 9, 10, 11 and 12 inherit it |

**R-02 extended 2026-08-22 — four leakage prohibitions promoted into this risk.**
On the owner's ruling against governance finding `DP-ML-01`, four requirements
previously counted among R-05's undifferentiated 40 are **not** ordinary missing
acceptance rows. Each prohibits a distinct route by which information the model
should not have can reach it, and each is a **prerequisite for trustworthy model
training and evaluation** rather than a documentation gap:

| Requirement | Prohibited behaviour | Why it belongs with R-02 |
|---|---|---|
| **FR-P1-04-12** | Unauthorized feature-dictionary expansion | A field outside the §6.2 dictionary entering training is an input-space breach that no downstream check would catch, because the dictionary *is* the check |
| **FR-P1-04-13** | Invalid carried-forward `vtec_lag_*` values | Carry-forward on a target-derived lag propagates the target across the very boundary the lag exists to enforce. The ≤ 3 h allowance is scoped to external drivers and must never reach it |
| **FR-P1-04-16** | Unapproved support-field inclusion | A support field read at or beyond hour *t*, or used as an input without recorded G-04 approval, is target-hour information entering under another name |
| **FR-P1-04-17** | Driver-interval repetition or propagation | Repeating a Kp value outside its own 3-hour interval, or shifting Dst to a neighbouring hour, moves a value to a timestamp where it was not yet available — future information by construction |

Each is designed as a raise at a named call site, and `bolt-plan.md` Bolt 7 now
carries an explicit **negative-path test specification** for each — a test that
the prohibited behaviour is *detected and rejected*, not that the happy path
works.

**Those are specifications, not results — and the four distinctions must not be
collapsed.** Each of the four now **has** a §19 acceptance row: TA-33, TA-34,
TA-35 and TA-36, created under `CR-2026-08-22-LEAKAGE-TA` on the owner's approval.
None has an **implemented test** — no module exists for any of the four, and
module placement is an open assignment at functional design. None has been
**executed**. None has **passed**. All four §19 rows read `Pending`. Nothing here
may be read as evidence that any of them is tested or passing; a row that tests a
requirement on paper is a different fact from a requirement being tested.

<!-- Corrected 2026-08-22. Superseded text, preserved for the audit trail:
     "**Those are specifications, not results:** none of the four has a §16 or
     §19 acceptance row today, creating one is a Vision §15.2 amendment this
     stage cannot grant, and nothing here may be read as evidence that any of
     them is tested or passing."
     That sentence was true when written and became false the same day, when
     CR-2026-08-22-LEAKAGE-TA created TA-33…TA-36 under the owner's approval. It
     had survived as a direct contradiction of this document's own R-05 entry,
     which records the four leaving the untested list precisely because those
     rows were created. A site the CR-2026-08-22-INC-CORRECTIONS Rec 5 sweep did
     not reach — the sweep searched count literals, and this defect carries no
     count. -->
<!-- markdownlint-disable-line -->

The fifth untested forbidden edge in this unit, FR-P1-04-10, and the balance of
the 36 remain in R-05. (Superseded literal, preserved: "the balance of the 40".)

### R-03 — The confirmatory prediction built on the wrong seeds

| Field | Value |
|---|---|
| **Risk** | `three_seed_mean(predictions)` takes no frozen-seed-set parameter, so it is implementable only by inlining the values (forbidden — no scientific constant in source) or by a weaker distinctness check a wrong-but-distinct triple would pass (**BLK-03**) |
| **Likelihood** | Low — the seed **values** are now frozen and closed (development seed 42; final seeds {1337, 2024, 7}) |
| **Impact** | High |
| **Why it ranks third** | The three-seed element-wise mean **is** the confirmatory prediction, so a wrong seed set changes the thesis result. But the authority limb is closed and only the plumbing remains: the values must reach the function as a parameter from `ConfigSnapshot.seeds` via `configs/seeds.yaml`. Recorded so it is not misread as fully closed — **closing authority is not closing implementation** |
| **Mitigation** | Tracked, not front-loaded. BLK-03's contract is authored at functional design as an exit condition. The bootstrap seed 20221201 is frozen separately and is **not** part of that set |
| **Affected** | Bolt 8 owns it; Bolts 9, 10, 11 and 12 inherit it |

### R-04 — Unverifiable provenance on the acquisition input

| Field | Value |
|---|---|
| **Risk** | `audit_evidence_2022-FULL/` rests on twelve monthly runs whose provenance is **unverifiable in principle** — no provider byte stream exists anywhere in the workspace, and three of the twelve months (2022-04, 2022-07 and 2022-12, the locked month) have no `raw_isprint_cache/` at all |
| **Likelihood** | Realized — this is a present condition, not a possibility |
| **Impact** | High |
| **Why it ranks fourth** | It has **no code fix**; it is retrieval work, deferred by an earlier sequencing decision. It is also already visible as a standing caveat on every artifact produced before the re-acquisition, which is what keeps it from being a silent failure. Its superseded-hash limb is discharged (D-18 re-merged FULL from the corrected months, preserving the prior artifact rather than overwriting it); the provenance limb is untouched by that |
| **Mitigation** | Tracked. Every artifact produced before the re-acquisition carries the caveat, and **FULL must not be relied on at a freeze gate** while the chain stands unrepaired. Re-acquisition must record each file's full provider filename including version suffix, retrieval date and SHA-256, and surface rather than silently accept any suffix mismatch — because re-acquisition produces new bytes and cannot retroactively prove the original ones |
| **Affected** | Bolt 3; reaches G-P1A |

### R-05 — Requirements and forbidden edges that nothing tests

| Field | Value |
|---|---|
| **Risk** | **36 of the 105 requirements carry no §16 or §19 acceptance row.** **Scope narrowed 2026-08-22:** the figure was **40** when this risk was written. Four of those forty — FR-P1-04-12, FR-P1-04-13, FR-P1-04-16 and FR-P1-04-17 — gained acceptance rows TA-33…TA-36 under `CR-2026-08-22-LEAKAGE-TA` and were **promoted into R-02** on the owner's ruling against `DP-ML-01`, because they are leakage prohibitions rather than ordinary coverage gaps. They left this list because a row now tests them **on paper** — none of the four has an implemented test, an execution or a pass, and all four §19 rows read `Pending`. This risk therefore covers 36 requirements plus FR-P1-04-10, the fifth untested forbidden edge. (Superseded literal, preserved: "**40 of the 105 requirements carry no §16 or §19 acceptance row**"; corrected 2026-08-22, a site the `CR-2026-08-22-INC-CORRECTIONS` Rec 5 sweep did not reach) |
| **Likelihood** | Realized — the gap exists today |
| **Impact** | Medium to High, depending on the requirement |
| **Why it ranks fifth** | Discoverable at a gate rather than silently corrupting a result: each of the 36 carries a real pass/fail criterion, and each of the five forbidden edges is designed as a raise at a named call site, so a test *can* assert it. What is missing is the row, not the mechanism. (Superseded literal, preserved: "each of the 40"; corrected 2026-08-22, a site the `CR-2026-08-22-INC-CORRECTIONS` Rec 5 sweep did not reach) |
| **Mitigation** | Tracked, and enumerated per unit upstream so NFR requirements has a concrete work list. Closing any of them needs a Vision §15.2 change-control amendment, which is **not this initiative's to grant** |
| **Affected** | Distributed. The largest concentrations, derived from `unit-of-work-story-map.md` Table 1 rather than carried: `models-and-baselines` (7 of 9), `acquisition` (7 of 15), `regimes-diagnostics-reporting` (7 of 11), `external-products` (4 of 7). The eleven per-unit values sum to 36. (Superseded literal, preserved: "`external-products` (5 of 7)"; corrected 2026-08-22, a site the `CR-2026-08-22-INC-CORRECTIONS` Rec 5 sweep did not reach) |

### R-06 — No user stories, so acceptance vocabulary is fixed and external

| Field | Value |
|---|---|
| **Risk** | Stage 2.4 is `SKIP`, so `stories.md` does not exist and the §16 WS rows and §19 TA rows are the **only** acceptance vocabulary Construction receives |
| **Likelihood** | Certain — a scope decision, not a possibility |
| **Impact** | Medium |
| **Why it is recorded** | It is the structural reason R-05 cannot be fixed inside this initiative: with no story-derived acceptance criteria available, a gap in the WS/TA set has no in-project substitute and every closure runs through external change control |
| **Mitigation** | Recorded rather than mitigated. 13 WS rows and 27 TA rows are mapped to units; 39 have a primary owner and TA-24 has none |
| **Affected** | Every Bolt |

### R-07 — Owner and supervisor decisions with lead time

| Field | Value |
|---|---|
| **Risk** | Four decision-type items are unresolved and cannot be filled by any agent: BLK-02's `plumbing_7day` station identity, BLK-05's D-17 target-schema module name, BLK-06's canonical protected-set enumeration, and the three `features.yaml` F10.7 selection freezes |
| **Likelihood** | Certain — all four are open today |
| **Impact** | High — each blocks a specific Bolt or gate outright |
| **Mitigation** | **Gate 0**, the pre-Construction decision pack required by the Q8 answer: every item presented with its issue, options, recommendation, affected Bolt or gate and the decision required, before any Bolt starts. **No frozen value is invented, inferred or substituted** |
| **Affected** | Bolts 5, 6, 12; gates G-P2 and G-P3C |

### R-08 — Platform and licence dependencies with no substitution path

| Field | Value |
|---|---|
| **Risk** | Kaggle is the only authorised compute host besides local — no third platform is permitted — and the heaviest job (10,000 bootstrap replicates inside a 10.0 GB planning envelope) runs there. Separately, the AGPLv3 Global-TEC-forecasting distribution question is unresolved outside this project and gates G-P2 |
| **Likelihood** | Low to Medium |
| **Impact** | High for the platform limb (no fallback exists); Medium for the licence limb (a defined fallback exists) |
| **Mitigation** | The platform limb is tracked with no substitution available; the envelope is measured at Bolt 1 and re-measured at Bolt 12. The licence limb has a standing default already recorded — **reimplement from the paper with a citation** — so it degrades rather than blocks |
| **Affected** | Bolts 1, 3, 4, 10, 12; gate G-P2 |

## What sequencing cannot mitigate

Two things are worth naming, because a reader could otherwise assume the plan
handles them:

- **The gates are not this initiative's to grant.** Seventeen gates govern the
  project; the ones this plan runs into — G-01, G-04, G-05, G-07, G-09, G-P1A,
  G-P2 — are supervisor-owned or owner-owned. No Bolt order changes when they are
  signed. `external-dependency-map.md` records each with its owner and the Bolt
  it affects.
- **A negative scientific result is not an engineering failure.** Engineering
  acceptance is independent of scientific outcome: a correctly executed negative
  result passes, and a favourable result produced by a pipeline failing a
  leakage, mask, seed or locked-test requirement does not. Recording this is not
  a softening of the bar — it removes the one incentive that most reliably
  corrupts a governed pipeline, which is treating an unfavourable result as an
  engineering defect to be debugged away.

## Assumptions & Open Questions

- **[assumption]** The risk ranking is by **irreversibility** rather than by
  expected loss. That choice is stated because it drives which two risks are
  front-loaded: R-03 has a higher headline severity than R-05 but a closed
  authority limb, while R-01 and R-02 are the two whose damage cannot be undone
  once done.
- **[assumption]** The Q3 deviation argument rests on the judgment that
  provider-side uncertainty is larger than naming-decision uncertainty. That is
  an assessment, not a measurement; if the F10.7, Dst and IRI validation work
  turns out to be routine, the deviation will have bought nothing and cost the
  target contract one Bolt of delay. **Partially tested since:** the F10.7 limb
  came back cleaner than assumed — the held provider file covers 365 of 365 days
  of 2022 with no missing dates, so the "month-long outage from 2022-03-18" is not
  observable in the retrieved data. What remains genuinely open in
  `external-products` is the three F10.7 selection decisions, the Dst release
  grade, and the IRI validation report.
- **[assumption]** The deviation's legality is conditional on the
  `external-products` / `target-standardization` independence holding. Recorded in
  full in § "The deviation is conditional", with the revision obligation if
  functional design finds the edge moves.
- **Open, carried not closed.** BLK-02 through BLK-07, RES-01, RES-02, RES-03,
  the 36 untested requirements, TA-24's missing implementing unit, the `02`
  ordinal collision, WS-13's evidence departure from §16, and the AGPLv3
  question.
- **None** of the above adopts a reading on a supervisor-owned value, and none
  decides a scientific constant.

## Corrections applied on resume, 2026-08-22

Five defects were corrected in this file after the first summary confirmation and
before the approval gate. Each preserves its superseded literal in place, per
`governance/CHANGE_RECORD_PROCEDURE.md` step 1. **No risk is added, removed or
re-ranked; no ordering argument changes; no scientific value is touched.**

| Site | Defect |
|---|---|
| § Sources | "the **40** requirements with no acceptance row" → **36** |
| § The sequencing argument, `external-products` bullet | "**five** of its seven requirements with no acceptance row" → **four**; and "the highest untested proportion of any unit in the plan" → **second-highest**, behind `models-and-baselines` at 7 of 9. The superlative was wrong when written — 5/7 = 71% was already below 78% |
| § R-02 status paragraph | "none of the four has a §16 or §19 acceptance row … this stage cannot grant" — **a direct contradiction of R-05 in this same file**, which records the four leaving the untested list precisely because TA-33…TA-36 were created |
| § R-02 closing line | "the balance of the **40**" → **36** |
| § R-05 Risk and "Why it ranks fifth" cells | "**40** of the 105 requirements carry no §16 or §19 acceptance row" and "each of the **40**" → **36**, with the 40 → 36 history and the four promoted IDs stated in the cell |

**The R-02 defect is the one that mattered.** It was an unresolved contradiction
internal to a single artifact, which `aidlc/spaces/default/memory/phases/inception.md`
§ Requirements Quality forbids carrying forward. Both statements were true when
written and false the same day, once `CR-2026-08-22-LEAKAGE-TA` created the four
rows under the owner's approval.

**Two of the five carry no numeral** — the R-02 claim and the "highest untested
proportion" superlative — so `CR-2026-08-22-INC-CORRECTIONS` Rec 5, which swept
for count literals, could not have found them. Raised at the approval gate.

**Untested total, derived and printed before assertion:** **36**, from two
independent artifacts whose ID lists were set-differenced and found identical.
`external-products` is **4 of 7**. The full per-unit breakdown and the
range-lead derivation caution are recorded in `bolt-plan.md` § Corrections applied
on resume rather than duplicated here — duplicating a derived figure across
artifacts is the drift this correction pass exists to undo.
