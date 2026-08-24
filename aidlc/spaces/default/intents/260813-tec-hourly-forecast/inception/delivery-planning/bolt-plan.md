# Bolt Plan — Hourly VTEC Forecasting (TEC_Project Phase 1)

Stage 2.8 (`delivery-planning`), intent `260813-tec-hourly-forecast`.
Depth: Comprehensive. Scope: `research-pipeline-governed`.

## Sources

- Topology, consumed as fixed input: `../units-generation/unit-of-work.md` (the twelve units, their owned artifacts, the blocker register BLK-01…**BLK-09** and the residual obligations RES-01…**RES-05**), `../units-generation/unit-of-work-dependency.md` (23 edges, the one independent pair, the forbidden edges), `../units-generation/unit-of-work-story-map.md` (requirement-to-unit and acceptance-row-to-unit mapping).
- Design: `../application-design/components.md` — the six `src/` packages, the three **NEW** modules, and the one-way layering rule this plan's build order follows.
- Requirements: `../requirements-analysis/requirements.md` — the seventeen governing gates, § Success and acceptance, § Known defects, § Constraints.
- Affirmed practices: `../practices-discovery/team-practices.md` — § Way of Working (git on `main`, freeze-gate tags, D-number commit linkage), § Walking Skeleton, § Testing Posture, § Deployment.
- Stage answers: `delivery-planning-questions.md` Q1–Q12 and FU-1–FU-2.
- **Absent by scope design, named so the gap is visible:** `stories` (`../user-stories/stories.md`) — stage 2.4 is `SKIP`, so the §16 WS rows and §19 TA rows are the whole acceptance vocabulary this plan can use. `mockups` (`../refined-mockups/`) — stages 1.6 and 2.5 are `SKIP`; this pipeline has no user-facing surface, so nothing is missing in substance.

## Vocabulary used in this document

A **Bolt** is one build pass over a piece of the work, ending in something that
runs and can be shown. Each Bolt here wraps exactly one unit of work.

A **walking skeleton** — the practice of building a thin end-to-end slice first
to prove the architecture hangs together — **is not used in this plan**. The
active scope file declares `skeleton: off`, and `team-practices.md`
§ Walking Skeleton records why: the data contract is frozen and the pipeline
stages attach to a known input surface, so there is nothing to bootstrap
end-to-end first. Bolt 1 runs like any other Bolt, and the usual "how should the
remaining Bolts run?" prompt does not fire.

This is a **separate fact** from the two required fixtures, and the two must not
be blurred. Technical Environment §9.2's rule — run the seven-day single-station
plumbing fixture and the one-month all-station scientific fixture, in that order,
before any full-year job — is a pipeline-enforced sequencing contract, not the
AI-DLC ceremony, and it survives `skeleton: off` untouched. It is enforced inside
`scripts/run_walking_skeleton.py`, which Bolt 12 owns.

## How this plan was chosen

Stage 2.7 fixed the dependency graph. This stage picks a path through it.

The graph leaves almost no room: 23 edges over 12 units with exactly one
independent pair, TC-06 pinning the front (repository, pins and test suite before
any acquisition work) and `fixtures-and-reproducibility`'s nine incoming edges
pinning the back. So the build order below is the dependency order, with **one
deliberate deviation** at positions 5 and 6, argued in
`risk-and-sequencing-rationale.md`.

Bolts run **strictly one at a time**. This is a single-author thesis codebase,
and `unit-of-work-dependency.md` § Independent unit sets already records that
independent units will normally be implemented sequentially.

## Construction iteration — stage-major

The per-unit Construction stages run **stage-major**: functional design for
every unit, then its approval gate; then NFR requirements for every unit, then
its gate; then NFR design; then code generation last. This is the framework
default and needs no state write.

It was chosen over the alternative (design and build one unit completely before
the next) for one specific reason. **Six of the eight** open blockers — BLK-03,
BLK-04, BLK-06, BLK-07, **BLK-08** and **BLK-09** — require **cross-unit contracts
authored at functional design**, and five of them are recorded as **exit conditions
on that stage** for several units at once. *(Counts corrected 2026-08-24 from "four
of the six": BLK-08 and BLK-09 were registered 2026-08-23 and both are cross-unit
contract blockers of exactly this kind — BLK-08 spans `evaluation-and-comparison`
and `features-and-splits`, BLK-09 binds `features-and-splits` and the four units
inheriting its fit. The argument this sentence makes is **strengthened** by them,
not weakened: the case for stage-major rests on how many units a contract blocker
spans, and the answer grew.)* Stage-major puts every affected unit inside functional
design together, and — decisively — its gate fires **before any code exists**,
which is the strongest available reading of G-09's "before any affected component
is coded".

The cost is stated plainly rather than buried: **no running code lands until all
twelve units are designed and three approval gates have passed.** On a thesis
timeline that is a real loss, and it was accepted knowingly at FU-1.

## Gate 0 — the pre-Construction decision pack

**This is not a Bolt. Nothing is built here.** It is a decision gate that runs
before Bolt 1, required by the Q8 answer.

> ## GATE 0 — DISCHARGED 2026-08-22, WITH NO LIVE DECISION OUTSTANDING
>
> Annotated in place after this stage's approval gate, on the project decision
> owner's explicit approval, under the annotate-in-place precedent set at
> `GOV-2026-08-22-INC-01` Rec 7.
>
> **Every item Gate 0 was built to present had already been decided** by the time
> it ran. The pack was assembled and found empty — which is a discharge, not a
> skip, and the difference is recorded so a later reader does not mistake one for
> the other:
>
> | Item | Resolution | Record |
> |---|---|---|
> | BLK-02 — `plumbing_7day` fixture station | **BSHM 32/35** — the only candidate cell with 168/168 hourly bins across D-11's window | **D-20** |
> | F10.7 (a) — which reading is the daily value | **Daily median**, with its availability rule | **D-21** |
> | F10.7 (b) — duplicate-UT tie-break | **Mean**, with duplicate logging and a QC flag; provider-defined correction semantics take precedence where documented | **D-22** |
> | F10.7 (c) — high-spread days | **Flag and retain**, using the approved daily median | **D-23** |
> | BLK-05 — D-17 target-schema module name | **`tests/test_prepared_target_schema.py`** | `CR-2026-08-22-TARGET-SCHEMA-TEST` |
> | FR-P1-01-7 — amendment wording | **Applied** | `CR-2026-08-22-F107-CORRECTIONS` |
>
> **What remains open is not decidable at Gate 0, by design — and this is the
> `DP-CHAIR-03` distinction, restated at the moment it matters:**
>
> - **G-09** (agent preflight) — **surfaced, not signed.** Its §18.3 preconditions
>   require an automated preflight over `data.yaml`, `features.yaml`,
>   `experiment.yaml` and `seeds.yaml`, none of which exists until Bolt 1 creates
>   them. A gate whose evidence is produced by Bolt 1 cannot gate Bolt 1. The
>   permitted/barred boundary below governs what may proceed meanwhile.
> - **G-01** (scientific framing) — **surfaced, not signed.** Pending owner
>   sign-off, due before the implementation freeze. Not this initiative's to grant.
> - **BLK-06** — per-item config binding and implementation, **decided at the
>   functional-design gate** under the `DP-CHAIR-02` ruling. Its enumeration limb
>   is discharged by **D-24**.
> - **BLK-03, BLK-04, BLK-07** — resolved *during* functional design; they do not
>   block its start, and no affected Bolt or gate completes until its exit
>   conditions are satisfied.
> - **BLK-08's mechanism limb, and BLK-09** — same treatment, added 2026-08-24.
>   The resolution mechanism for `Transform.inverse`, and whether `Partition` gains
>   a `train_start` field or an explicitly stated January-1 contract term, are both
>   authored at functional design and are **exit** conditions on the Bolts that own
>   them, never entry conditions.
>
> **The open-blocker count is eight** *(corrected 2026-08-24 from **six**; BLK-08
> and BLK-09 were registered 2026-08-23 and this passage predates them. Derived from
> the register's `| Status |` rows — eight, one each for BLK-02 through BLK-09, every
> one beginning `Open`.)* Several blockers have a limb discharged; none is closed
> outright. Discharging Gate 0 authorises **no implementation** — G-09 still stands
> before any affected component is coded.

> ## ⚠ GATE 0 RE-OPENED 2026-08-24 — ONE LIVE ITEM
>
> **The discharge above stands exactly as recorded.** Every item it lists was
> genuinely decided, and nothing here reverses or amends it. What follows is a **new**
> item that did not exist on 2026-08-22: `application-design` was re-entered on
> 2026-08-23, produced **ADR-11**, and its review registered two blockers — **BLK-08**
> and **BLK-09** — which `units-generation` then carried into the register this plan
> consumes as fixed input.
>
> Under the owner's ruling of 2026-08-24 (question Q13 = C), **BLK-08 splits**, on the
> precedent BLK-06 set when its enumeration limb was separated from its implementation
> limb.
>
> | Item | Why it is a Gate 0 decision rather than a design one | Owner | Due |
> |---|---|---|---|
> | **BLK-08, scientific limb** — *does the train-only transform touch the target?* | It is answerable **now** from the frozen TE §6.2 feature contract, and it is a scientific reading rather than an interface choice. If the transform touches the target, model output is in transformed space, and `ABL-DIFF`'s obligation to *"inverse-transform to absolute TECU before any metric"* (`project.md` § Mandated) needs a path back that the design does not currently express. If it does not, that must be **stated**, so the obligation is visibly satisfied rather than silently assumed. Deferring it would have Bolt 9's designer settle a scientific question mid-design | Project decision owner, under the recorded student/supervisor authority equivalence | **ANSWERED 2026-08-24** — see below |

> ## ✅ BLK-08 SCIENTIFIC LIMB — ANSWERED 2026-08-24
>
> **The ruling: NO.** The primary configuration's train-only transform does **not**
> touch the target. Taken by the project decision owner at this stage's approval gate,
> under the recorded student/supervisor authority equivalence.
>
> **The evidence it was read from**, all frozen before this stage ran:
>
> | # | Source | What it says |
> |---|---|---|
> | 1 | **TE §7.2 ablation table, `ABL-DIFF` row** | Its **Primary remains** column reads **"Raw TECU"**. The first-difference target is an ablation-only change: *"Target becomes y(t+1) − y(t); predictions inverse-transformed to absolute TECU before any metric is computed"* |
> | 2 | **TE §6.2 dictionary** | It is the **feature** table. The only train-only standardization on anything target-derived applies to **inputs** — `vtec_lag_1h/2h/3h/24h` and `vtec_seq_24`, *"Train-only standardization for ridge/LSTM; none for RF"*. Those are lagged values used as predictors, not the y being predicted |
> | 3 | **Both governing documents** | Neither states anywhere that the target itself is scaled. The only normalization applied to it at P1-03 is **UTC** normalization — timestamps, not magnitudes |
> | 4 | **NFR-LEAK-01** | Its *"no all-data scaling"* prohibition is a constraint on features |
>
> **What follows, and what does not.**
>
> - **The primary path needs no inverse.** Model output is already in raw TECU, so the paired loss differential, the bootstrap interval and the practical-relevance threshold are computed on the quantity the model emits. This must be **stated explicitly** in `component-methods.md` and in ADR-11's consequences — the obligation is satisfied by a recorded fact, not by silence.
> - **`ABL-DIFF` keeps its inverse obligation in full.** It is the one configuration that transforms the target, and TE §7.2 requires the inverse **before** metrics *"so every ablation is scored on the same quantity in the same units as the primary"*, with **error propagation through the inverse transform recorded**. The inverse belongs to the ablation's target differencing, which the ablation configuration owns, rather than to `src/features`' train-only scaler.
> - **BLK-08's mechanism limb narrows but does not close.** Functional design still names how `ABL-DIFF`'s inverse is reached and where its error propagation is recorded. It no longer needs a general `src/evaluation` → `src/features` route for the primary path, which is the design pressure that made the original finding Critical.
>
> **Numbered as D-27, 2026-08-24.** `team.md` § Way of Working holds that a scientific
> or governance decision *"is not real until it has a D-number"*, and
> `evidence/DECISIONS.md` is authoritative for those. That file is **outside this
> stage's produces list**, so it was written on the owner's explicit instruction at
> this approval gate rather than as stage output. **D-27** carries the ruling, the four
> pieces of evidence it was read from, its consequences, an explicit statement of what
> is *not* asserted, and the limitation that a contradicting model path found later is
> a contradiction to surface rather than a licence to adjust the target contract
> (TE §18.2). The decision is **real and numbered**, not recorded-but-unnumbered.
>
> **What this does not re-open.** BLK-08's **mechanism** limb — a registry keyed by
> `transform_id`, an `inverse_transform_id` on `Prediction` with a named owner, or a
> permitted import edge — is functional design's work and is listed above. **BLK-09**
> does not reach Gate 0 at all: it is an interface question with no scientific limb,
> and the January-1 reading it depends on is already fixed by FR-P1-04-5's fold
> definitions.
>
> **What it blocked meanwhile — now moot.** Nothing permitted on 2026-08-22 became
> barred, and Bolts 1–6 were never touched by BLK-08. The scientific limb was
> **answered at this stage's approval gate on 2026-08-24** (see below), so Bolt 7's and
> Bolt 9's functional design now enter with the reading settled rather than carrying it.



Before any Bolt starts, every unresolved owner decision and entry-blocking
condition is collected and presented — the issue, the available options, a
recommendation, the Bolt or gate it affects, and the decision required. The
project decision owner resolves them. **No frozen value is invented, inferred or
substituted**, in keeping with `project.md` § Forbidden and with BLK-02's own
wording that no manifest may be invented, inferred or substituted.

The items are enumerated with their owners and lead times in
`external-dependency-map.md`. They fall into two kinds, and the distinction is
not cosmetic:

- **Decidable now, with no design work behind them** — BLK-02's `plumbing_7day`
  station identity, and the three `features.yaml` F10.7 selection freezes (which
  of the three daily readings is the daily value; the duplicate-UT tie-break; the
  high-spread handling). These are presented at Gate 0 and decided there.
- **Presented now, decided at functional design's gate** — BLK-05's D-17
  target-schema module name and BLK-06's canonical protected-set enumeration.
  Both are named in the Q8 answer, and both are recorded in the blocker register
  as work **functional design itself performs**: BLK-06's required resolution is
  an item-by-item derivation from Technical Environment §2.2 and §7.0B under an
  explicit deduplication rule, and BLK-05 says outright that stage 3.1 names the
  module. So Gate 0 presents the question, the options and the authority; the
  concrete value is approved at the functional-design gate, which under
  stage-major still precedes all implementation.

**Owner ruling, 2026-08-22 — this is no longer an interpretation.** Against
governance finding `DP-CHAIR-02` (`GOV-2026-08-22-DP-01`), the project decision
owner ruled the split explicitly, and the ruling governs:

> Functional design **may begin** while BLK-05 and BLK-06 remain open, **but only
> to analyze those blockers and generate the evidence required for their
> resolution**. Both blockers are presented to the owner with options, supporting
> evidence, risks and a recommendation. **Neither is marked resolved and no
> approval is assumed until the owner explicitly decides.** No dependent
> implementation, code generation, governed execution or downstream activity may
> begin until the corresponding blocker decision is approved and recorded.

This is recorded against the Q8 instruction in `delivery-planning-questions.md`
and carried identically in `external-dependency-map.md` § A2. It narrows what
functional design may do with these two blockers rather than relocating them:
the analysis is permitted, the decision remains the owner's, and the
implementation stays barred. BLK-03, BLK-04, BLK-07, **BLK-08's mechanism limb and
BLK-09** are unaffected — they keep the 2026-08-22 exit-condition ruling recorded in
the blocker register, extended to the two newer blockers on 2026-08-24.

### G-09 and G-01 — surfaced at Gate 0, signed later

Also collected at Gate 0: **G-09** (agent preflight) and **G-01** (scientific
framing). Both are **surfaced** here for visibility because they bind
implementation rather than any single Bolt. Neither is **signed** here, and the
distinction is load-bearing — corrected 2026-08-22 against governance finding
`DP-CHAIR-03`.

**G-09 cannot be signed at Gate 0, and requiring it there would be
unsatisfiable.** Its own preconditions, quoted from Technical Environment §18.3,
include *"an automated preflight asserts that no required field in `data.yaml`,
`features.yaml`, `experiment.yaml`, or `seeds.yaml` is `TBD`, that every declared
source and hash exists, and that all gate tests pass."* None of those four files
exists until Bolt 1 creates them. A gate whose evidence is produced by Bolt 1
cannot gate Bolt 1.

**What the authority permits before G-09 — derived, not assumed.** The owner
directed that no bootstrap exception be assumed silently. None is needed: §18.3
is **component-scoped**, not global. Its opening line reads *"Before the agent
implements **an affected component**"*, its first precondition is *"All P0
decision-register entries **for that component** are resolved"*, and its binding
sentence is *"must not implement **an affected component** while **its** P0
decision is unresolved."* The gate therefore attaches to a component carrying an
unresolved P0 decision — not to every keystroke in the repository. Two
independent confirmations that scaffold work is expected to precede it: REQ-ENG-2
requires the four configs to **exist with unresolved fields visibly marked
`TBD — freeze gate`**, which is impossible if no config may be created before the
gate that reads those sentinels; and TC-06 (`binding: hard`) places the
repository, pinned environment and test suite **before any acquisition work**,
which is itself pre-G-09 activity.

**The boundary line, stated so it can be checked rather than argued.**

Permitted before G-09 is signed:

- Creating the §12 directory tree, `pyproject.toml`, `requirements.txt`,
  `README.md` and the `ruff` configuration.
- Creating the four governed config **files** with every unresolved scientific
  field carrying a visible `TBD — freeze gate` sentinel. Writing a sentinel is
  not choosing a value.
- Transcribing into a config only those values already frozen under an approved
  D-number, citing that D-number.
- Creating the `tests/` tree, its conftest and shared fixtures.
- Initializing git on `main` with the credential deny-list.
- Installing the pinned environment on both platforms and capturing install logs.

Barred until G-09 is signed for the affected component:

- Implementing any component whose P0 decision is unresolved.
- Filling any `TBD — freeze gate` field.
- Executing any governed run, on either platform.
- Generating code for a unit carrying an open blocker on that scope.

**Stub stage scripts — settled by owner ruling, 2026-08-22.** TA-01 requires nine
phase-aware stage scripts to exist in the tree, and whether a stub counts as
scaffold was not settled by §18.3's text. The owner ruled:

> A minimal stub stage script is **scaffolding only when it contains none of**:
> scientific implementation, governed execution, full-year processing, data
> acquisition logic, feature-generation logic, model-training logic, or
> unauthorized December access.
>
> Permitted scaffolding may include **module structure, interfaces, placeholder
> CLI definitions, configuration wiring, and safe fail-fast behaviour.**

Two limits ride with it. **The one-unit-per-Bolt rule is preserved**, and
**scaffolding may not be used to implement another unit early** — a stub that
starts carrying a downstream unit's logic has stopped being a stub and has taken
that unit's work out of its own Bolt. And a stub that would perform any governed
execution is not a stub: fail-fast on a missing input is scaffold, running the
stage is not.

**G-01** is likewise surfaced, not signed: it is pending sign-off and due before
the implementation freeze. Neither gate is this initiative's to grant.

**Contract-type blockers are explicitly out of Gate 0's scope.** BLK-03, BLK-04,
BLK-07, **BLK-08's mechanism limb and BLK-09** are resolved *during* functional
design and do not block its start — that is the 2026-08-22 ruling recorded in the
blocker register, extended to the two newer blockers on 2026-08-24, which corrected
an earlier wording that made them unsatisfiable. **BLK-08's scientific limb is the
one exception**, and it is in Gate 0's scope by the owner's Q13 = C ruling: see
§ Gate 0 § ⚠ GATE 0 RE-OPENED. What they do bind: **no affected
Bolt or gate is marked complete until its applicable exit conditions are
satisfied**, and no implementation proceeds while they stand.

---

## The Bolt sequence

Twelve Bolts, one per unit, strictly serial. Complexity is relative only — no
calendar estimate is implied. Derived from the unit table: **105 requirements and
43 primary acceptance rows** distributed across the twelve Bolts (both figures
recomputed by summing the per-unit rows below, not carried from the upstream
prose).

> **⚠ Acceptance rows corrected 2026-08-24 — the total read 39, and two cells fed it.**
> Bolt 5 `external-products` read **1** and Bolt 7 `features-and-splits` read **9**.
> Those are the figures superseded on **2026-08-22** by `CR-2026-08-22-LEAKAGE-TA`,
> which gave `FR-P1-04-17` **TA-36** and `FR-P1-04-12`, `FR-P1-04-13`, `FR-P1-04-16`
> **TA-33**, **TA-34** and **TA-35**. `units-generation` corrected its own copies; this
> downstream plan was written from the pre-correction figures and no sweep crossed the
> stage boundary to reach it.
>
> *Derived, not carried:* this table's twelve Acceptance-rows cells now read
> `7, 2, 1, 3, 2, 1, 12, 5, 1, 2, 3, 4`, summing to **43**. That is the same 43 the
> upstream `unit-of-work.md` column sums to, though the two orders differ — this table
> places `external-products` at position 5 and `target-standardization` at 6, the
> reverse of the unit table, so the series are checked element-by-unit rather than
> position-by-position. The **105** requirements figure was re-derived the same way
> and is unchanged.
>
> The four new rows are `Pending`: acceptance rows that exist, not tests that have
> been implemented, executed or passed.

| # | Bolt | Unit | Complexity | Requirements | Acceptance rows | Open blockers |
|---|---|---|---|---|---|---|
| 1 | Foundation | `foundation` | M | 16 | 7 | — |
| 2 | Governance guards | `governance-guards` | M | 10 | 2 | BLK-06 |
| 3 | Acquisition | `acquisition` | L | 15 | 1 | BLK-07 |
| 4 | Inventory and registry | `inventory-and-registry` | M | 7 | 3 | — |
| 5 | External products | `external-products` | L | 7 | **2** | — |
| 6 | Target standardization | `target-standardization` | M | 6 | 1 | BLK-05 |
| 7 | Features and splits | `features-and-splits` | L | 11 | **12** | BLK-04, **BLK-08** (co-owned), **BLK-09** |
| 8 | Models and baselines | `models-and-baselines` | L | 9 | 5 | BLK-03, BLK-04 ↓, **BLK-09 ↓** |
| 9 | Evaluation and comparison | `evaluation-and-comparison` | M | 4 | 1 | **BLK-08**, BLK-03 ↓, BLK-04 ↓, **BLK-09 ↓** |
| 10 | Statistical inference | `statistical-inference` | M | 1 | 2 | BLK-03 ↓, BLK-04 ↓, **BLK-08 ↓**, **BLK-09 ↓** |
| 11 | Regimes, diagnostics, reporting | `regimes-diagnostics-reporting` | L | 11 | 3 | BLK-03 ↓, BLK-04 ↓, **BLK-08 ↓**, **BLK-09 ↓** |
| 12 | Fixtures and reproducibility | `fixtures-and-reproducibility` | M | 8 | 4 | BLK-02, BLK-03 ↓, BLK-04 ↓, **BLK-08 ↓**, **BLK-09 ↓** |

**↓** marks a blocker inherited through a consumed contract rather than owned.
An unmarked ID is owned by that Bolt's unit. **BLK-01 is closed** (2026-08-22,
`CR-2026-08-22-TE-AMEND`) and appears nowhere above; its closure was authority
only — the three modules it authorized still do not exist and remain gated by
G-09 and code generation.

### What every Bolt owes, regardless of unit

Fixed by the Q6 and Q10 answers, so it is not repeated in each entry below:

1. The unit's modules exist and its **owned test modules pass locally**.
2. Every acceptance row the unit owns as primary has its **evidence artifact** —
   not an assertion that it would pass. Visual inspection alone is insufficient
   at every row.
3. **Every blocker naming that unit's scope is discharged**, or the Bolt does not
   close. A blocked unit is not marked accepted, Ready or complete.
4. **Measured fixture-manifest fields are recorded as the Bolt completes** — row
   counts, support and missingness limits, timestamp tolerances, expected CPU
   runtime range — rather than reconstructed at the end. §15.1 requires these to
   be measured and frozen, never invented, and the cheapest guarantee of a
   measured value is to record it when it is measured. Bolt 12 assembles and
   freezes them.

   **Both fixture identities are now frozen, so this obligation is unbounded from
   Bolt 3 onward.** The scientific fixture is D-14 (March 2022, all three cells);
   the plumbing fixture is D-11's window (2022-11-01 to 2022-11-07) on **BSHM
   32/35**, frozen as **D-20** on 2026-08-22 — selected on the only complete
   measured coverage of that window, 168/168 hourly bins with 7/7 day presence.
   **BLK-02's station limb is discharged.**

   The `BLOCKED` rule is retained for any field that remains unresolved: a
   station-dependent field with no frozen basis is **recorded as `BLOCKED — <id>`,
   never estimated, inferred, or filled from the three-cell window**. D-20 supplies
   the fixture's *identity* only — every count, tolerance, row-count range,
   support and missingness limit and CPU runtime range is still **measured from a
   fixture run that has not happened**, and none may be written before it does.
5. Any commit changing a scientific constant or a governed config **cites its
   D-number**; freeze gates are tagged.

6. **Every demonstration and preliminary execution stays fixture-scale until both
   walking-skeleton fixtures have actually passed.** Added 2026-08-22 against
   governance finding `DP-BENCH-01`, which found that §9.2's ordering contract
   has no enforcement point between Bolt 3 and Bolt 11 because
   `run_walking_skeleton.py` — the script that enforces it — is written in
   Bolt 12. Three categories, kept distinct because they carry different rules:

   | Category | Permitted before both fixtures pass | Rule |
   |---|---|---|
   | **Raw data already held, or newly acquired** | Yes | Acquisition and retention of provider bytes is not a processing run. **Existing data is not re-downloaded without a justified, recorded need** — the twelve months already held are re-verified under the new test suite, not re-acquired. |
   | **Fixture-scale development runs** | Yes | Bounded to D-11's window (2022-11-01 to 2022-11-07) or D-14's month (March 2022). This is what every Bolt's expected demo means. |
   | **Full-year scientific processing, feature generation, model training, evaluation** | **No** | Barred until both fixtures have passed, in order, with real evidence. Not "assumed to pass" and not "will pass" — passed. |

   **December 2022 is protected throughout all three categories.** No record whose
   observation date falls in December 2022 enters either fixture, asserted on
   record dates and never on the folder a file was filed under. No development
   activity of any category reads under `evidence/locked_test_restricted/` except
   through `governance-guards.open_restricted`, which writes the access-log row
   before the read.

   **The term is now defined in the authority, so the table above is no longer
   provisional.** Technical Environment §9.2 used "full-year job" — and §7
   "full-year generation", the §10 source table "full-year processing" — without
   defining any of them. Amended 2026-08-22 under Vision §15.2
   (`CR-2026-08-22-SCOPE-DEFS`) to carry the same three classes: **A** raw
   acquisition, secure storage, integrity verification and minimal inventory;
   **B** fixture-scale development and testing; **C** full-year scientific
   processing, standardization, feature generation, training, prediction,
   bootstrap and evaluation. **Only class C is a full-year job requiring prior
   fixture evidence.**

   Class A is not a licence: every locked-December restriction applies to it
   unchanged — no analytical inspection of December target values, no December
   performance quantity computed or examined, and every access under the
   restricted root routed through the chokepoint that logs before it reads.
   Integrity verification of December bytes is custody work, not analysis, and
   that is what class A turns on.

**The demo differs by deployment class**, per the Q10 answer:

- **`standalone` units (8: Bolts 3, 4, 5, 6, 7, 8, 9, 12)** — a runnable stage
  script producing a hashed release plus an experiment-registry row. That is what
  a deliverable is here: `team-practices.md` § Deployment records that
  "deployment" in this project means immutable dataset and model releases with
  version, manifest, SHA-256 hashes, schema, row counts, exclusions and fold
  identifiers.
- **`shared` units (2: Bolts 1, 2)** — passing tests plus the approved contract,
  demonstrated through the released artifacts their consumers identify by release
  ID and hash.
- **`embedded` units (2: Bolts 10, 11)** — passing tests plus the released
  artifacts they produce inside `07_evaluate_and_report.py`, which Bolt 9's unit
  owns.

**The in-Kaggle rule is conditional on the execution session, not on a Bolt
number.** Corrected 2026-08-22 against governance finding `DP-DATA-01`, which
found that a fixed list silently exempts whichever Bolt was not anticipated —
Bolt 8 trains six model families and Bolt 10 runs 10,000 bootstrap replicates
described upstream as the pipeline's heaviest CPU cost, and neither was on the
list. The rule as it now stands:

> **Any Bolt that performs a governed run inside a Kaggle session must first
> provide evidence that the required critical tests and the applicable
> walking-skeleton fixtures passed inside that same session.**

Four consequences, stated so the rule cannot be satisfied by a technicality:

1. **The obligation attaches to the execution environment and session**, never to
   a Bolt number. Any Bolt may acquire it, and a Bolt may acquire it later than
   planned without the rule needing a revision.
2. **A new session, or a materially changed execution environment, requires fresh
   evidence.** A pass from a previous session does not carry: a Kaggle session
   carries no git working tree, so a commit hook cannot fire there and neither a
   local pass nor an earlier session's pass proves anything about the environment
   the governed run actually executes in.
3. **Pure-library work that performs no governed Kaggle run owes nothing**, and
   must not open a Kaggle session merely to satisfy the rule. This preserves the
   carve-out the Q6 answer chose.
4. **Currently anticipated to acquire the obligation:** Bolts 3, 4 and 12, and —
   newly identified by this correction — Bolts 8 and 10 if their training and
   bootstrap runs execute on Kaggle. This list is illustrative of today's
   expectation and is **not** the rule; the rule is the conditional sentence
   above.

Bolt 1 is a separate case: it needs install logs from both platforms because
TA-03 requires it, not because of this rule.

---

### Bolt 1 — Foundation

**Unit** `foundation` · **Deployment** shared · **Depends on** nothing (first dependency root) · **Open blockers** none

**What it bundles.** The repository itself and the run-time services every stage
entry needs before any domain work: the §12 tree, the pinned environment, the four
governed configuration files with their load/snapshot/hash path and zero-`TBD`
assertion, the determinism helper, platform-root resolution, the run record and
experiment registry, and immutable dataset releases with their SHA-256 hashing.

**Definition of Done.**

- The §12 repository tree exists item for item — `pyproject.toml`,
  `requirements.txt`, `README.md`, the four configs under `configs/`, six `src/`
  packages, nine phase-aware stage scripts, five notebooks, `tests/`,
  `artifacts/`, `scripts/run_walking_skeleton.py`. Module *content* belongs to
  later Bolts; **existence** of the tree is this Bolt's obligation, because TA-01
  gates on it.
- Every unresolved config field is visibly marked `TBD — freeze gate`. No field
  is filled by convenience.
- Python 3.11 with exact pins installs on **both** Kaggle and local, with install
  logs and environment hashes from each; every governed run records a `platform`
  value from {Kaggle, local} and a run outside that set fails.
- Git is initialized on `main` with the credential/secret deny-list present in
  `.gitignore` **before the first commit**; a secret scan over the working tree
  returns clean, and the pre-existing history breach is recorded separately
  rather than folded into that check.
- **Per the Q11 answer:** the `tests/` tree, its shared fixtures and conftest
  exist and run, together with the test modules whose subject exists at this
  point — `test_release_hashes.py` and `test_determinism.py`. The remaining
  sixteen modules are written inside their own unit's Bolt.
- An experiment-registry row exists carrying all eight §13.1 environment-lock
  items populated — not `unavailable`.

**Acceptance rows owned (7).** TA-01, TA-02, TA-03, TA-10, TA-15, TA-22, TA-23.

**Confidence hypothesis — what shipping this proves.** That the pinned
environment installs identically on both authorised platforms and that a run's
configuration can be snapshotted and hashed. Every later Bolt's evidence is tied
to an environment lock produced here; if the pins do not reproduce on Kaggle,
every downstream reproducibility claim is affected, and the cheapest place to
discover that is before any domain code exists.

**Expected demo.** Install logs from both platforms with matching environment
hashes; a registry row with all eight lock items populated; a release manifest
with its ten rows over fourteen fields verifying by hash; and
`run_walking_skeleton.py` failing **cleanly** with a named missing-artifact
message rather than a traceback — which is itself evidence of the two-tier error
posture.

**Note on `test_determinism.py`.** BLK-01's closure authorized this module **by
name only**. It does not exist, and creating it stays gated by G-09 and by code
generation. Authority to name a module is not authority to write one.

---

### Bolt 2 — Governance guards

**Unit** `governance-guards` · **Deployment** shared · **Depends on** `foundation` · **Open blockers** BLK-06

**What it bundles.** The runtime prohibitions that must hold before any
scientific work runs: the phase-boundary import limb and produced-field limb, the
single chokepoint for every read under the restricted December root with its
access-log-before-read ordering, and the §10.1 external-code reuse register.

**Definition of Done.**

- `assert_phase_boundary` and `assert_no_raw_fields` implemented and called at
  step 4 of every stage script's six-step entry contract;
  `test_phase_boundary.py` passes, including its second independent result on the
  produced-field limb.
- `open_restricted` is the **only** path into `evidence/locked_test_restricted/`,
  and it writes the access-log row carrying `locked_test_accessed = true`
  **before** the read.
- The §10.1 reuse register records all fifteen fields before any reused code is
  used; `test_reuse_registry.py` passes.
- **The canonical protected set is frozen as D-24 (2026-08-22) — BLK-06's
  enumeration limb is discharged.** `TransitionManifest.protected_hashes` carries
  the **17-item** deduplicated union of TE §2.2 (12 items) and §7.0B (16 items),
  with `history window`, `station encoding` and `baselines` added explicitly
  because each mapped onto nothing in the previous fourteen. **The cardinality
  was calculated from the enumeration, not assumed.** `baselines` protects M-01,
  M-02, M-03, **B-01 the IRI-2016 benchmark with its 2000 km ceiling**, and C-01
  the CODE GIM comparator with its interpolation rule — the omission that would
  otherwise have let a Phase 2 baseline change pass G-P3C's empty-diff condition
  undetected. FR-P1-06-1 was amended 14 → 17 under Vision §15.2
  (`CR-2026-08-22-PROTECTED-SET`).
- **Still blocked, and the Bolt does not close on it:** the **implementation** of
  `protected_hashes` and `diff_protected_hashes`. Naming the set is not writing
  the code. Binding each of the 17 items to a concrete config field completes at
  functional design, because none of the four config files exists yet, and
  creation stays gated by G-09 and code generation.

**Acceptance rows owned (2).** TA-27 (first limb — Phase 1 cannot import raw GNSS
modules; the second limb is accepted at G-P2 and G-P3C, outside Phase 1),
TA-28.

**Confidence hypothesis.** That the prohibitions are enforced at **run time**,
not only in tests. This matters because a Kaggle session carries no git working
tree: a commit hook cannot fire there, so a guard that lives only in the test
suite proves nothing about the environment a governed run executes in.

**Expected demo.** A deliberate injection of a `src/gnss` import failing at stage
entry with a message naming the module and the violated expectation; an
`open_restricted` call showing the access-log row written before the first byte
is read.

---

### Bolt 3 — Acquisition

**Unit** `acquisition` · **Deployment** standalone · **Depends on** `foundation`, `governance-guards` · **Open blockers** BLK-07 · **In-Kaggle critical test run required**

**What it bundles.** Retrieval of the approved Madrigal MAPGPS `gps` binned-VTEC
product under D-144 and the three driver series, full provenance for every
retrieved file including its provider version suffix, retention of native byte
streams, one manifest hash entry per provider file, gaps stored as explicit NaN,
and closure of the ICTP rejected-source audit.

**Definition of Done.**

- Every retrieved file records provider, permanent citation, **full provider
  filename including its version suffix**, retrieval date and SHA-256; an
  injected suffix mismatch is surfaced, never silently accepted.
- `sha256_manifest.json` hashes **one entry per provider file**, not only the
  four derived artifacts.
- Membership derives from **record timestamps** only, never from a directory name
  or filename; `tests/test_acquisition_window.py` passes, including the case that
  produced the original defect.
- Gaps survive acquisition as explicit NaN. No interpolation, smoothing or fill.
- Credentials reach the provider client from the environment only — never through
  a config file, log, registry note or notebook.
- **BLK-07 discharged:** every read or write under
  `evidence/locked_test_restricted/` — including the `audit_evidence_2022-FULL/`
  artifact D-9 promotes as the Phase 1 input — routes through
  `governance-guards.open_restricted`. **No acquisition run touches calendar
  2022-12 while this stands.**

**Acceptance rows owned (1).** TA-32.

**Confidence hypothesis.** That the six external providers can actually be
retrieved from under the governed constraints, with provenance complete enough to
be re-verified. Seven of this unit's fifteen requirements have no acceptance row —
tied for the largest untested **count**, though not the largest **proportion** —
so what this Bolt proves is mostly demonstrated rather than asserted by a test.
<!-- Corrected 2026-08-22. Superseded literal, preserved: "the largest untested
     share of any unit". Wrong when written and an internal contradiction: the
     models-and-baselines Bolt below claims the "joint largest untested share"
     for 7 of 9, and two sites cannot both hold the largest. Derived from
     unit-of-work-story-map.md Table 1: three units tie at 7 untested
     (acquisition 7/15, models-and-baselines 7/9, regimes-diagnostics-reporting
     7/11), so acquisition ties on count at 7 while its proportion, 47%, ranks
     fifth of eleven behind models-and-baselines (78%),
     regimes-diagnostics-reporting (64%), external-products (57%) and
     evaluation-and-comparison (50%). Count and proportion are now named
     separately rather than conflated in the word "share". A site the
     CR-2026-08-22-INC-CORRECTIONS Rec 5 sweep did not reach — it carries no
     stale numeral, only a stale superlative. -->
<!-- markdownlint-disable-line -->

**Expected demo.** A retrieval run inside the Kaggle session producing
`request_manifest.json` and `sha256_manifest.json` with per-provider-file hashes;
an access-log sample showing the row written before the D-9 input was opened.

**Standing caveat this Bolt cannot discharge.** `audit_evidence_2022-FULL/` rests
on twelve monthly runs whose provenance is **unverifiable in principle** — no
provider byte stream exists anywhere in the workspace, and three of the twelve
months have no `raw_isprint_cache/` at all. Every artifact produced before the
re-acquisition carries that caveat, and FULL must not be relied on at a freeze
gate while its provenance chain stands unrepaired.

---

### Bolt 4 — Inventory and registry

**Unit** `inventory-and-registry` · **Deployment** standalone · **Depends on** `acquisition` · **Open blockers** none · **In-Kaggle critical test run required**

> **`RES-05` — a residual obligation, not a blocker** (registered 2026-08-23, carried
> from `application-design` finding M14). This unit's own 3.1 artifact,
> `construction/inventory-and-registry/functional-design/business-logic-model.md`
> line 529, cites `build_features`'s signature by **line number** —
> *"`component-methods.md` line 389"* — an anchor the 2026-08-23 amendments moved, and
> a signature that itself changed (`build_features` now takes `spec: FrameSpec` and
> `partitions: Sequence[Partition]` and returns a `FeatureBundle`). Due at this Bolt's
> functional-design gate; the re-verification cites the **section heading** rather than
> a line number, so the anchor cannot go stale again. It is a citation to repair, not a
> design surface that cannot execute — which is why it is a `RES-` item and does not
> appear in this Bolt's Open-blockers field.

**What it bundles.** The source inventory (nine fields per entry, including which
configuration consumes each source), the station registry, schema validation of
the prepared product, and the performance-blind coverage and regime audit that
G-P1A accepts.

**Definition of Done.**

- Station coordinates and the coordinate-to-cell rule are **frozen under a
  D-number first**, then moved into `configs/data.yaml` and `src/data/registry.py`
  and validated against the official IGS site logs. A conflict is resolved and
  recorded, **never averaged or ignored** — and a conflict resolved by averaging
  fails.
- Every source inventory entry carries all nine fields; the Kyoto
  non-commercial-use notice is recorded **verbatim**, and the CEDAR
  rules-of-the-road acknowledgment is attached.
- The **December coverage and regime audit** runs performance-blind, through
  `open_restricted`, with its access-log row written first. This is required
  before G-05 and is a **different event** from the one-shot locked evaluation.
- `merge_coverage_year.py` migrates here with `--config configs/` and its numbered
  position; its `sha256_of_file` copy consolidates into `foundation`'s
  `release.py`.

**Acceptance rows owned (3).** WS-01, TA-04, TA-25.

**Confidence hypothesis.** That the prepared product passes G-P1A's coverage
minimum (D-12: ≥90% usable hourly coverage per station per month, with D-2's day
rule) across all three cells for the full year. This is the first Bolt whose
result could stop the thesis rather than delay it: if coverage fails, no amount of
downstream work rescues it.

**Expected demo.** The G-P1A evidence set including the December coverage audit,
with per-cell per-month coverage figures and the access-log sample.

**Recorded, not tested (RES-01).** No dedicated acceptance criterion verifies
that a **permitted** December read writes its access-log row before the first
record is read. WS-18 and TA-18 test the *execution* guard against unauthorized
pre-G-05 performance execution — a different scenario. The candidate criterion is
owned by NFR requirements and routed through Vision §15.2 change control.

---

### Bolt 5 — External products

**Unit** `external-products` · **Deployment** standalone · **Depends on** `inventory-and-registry` · **Open blockers** none

**Sequenced ahead of `target-standardization`** — the one deviation from the
upstream presentation order, argued in `risk-and-sequencing-rationale.md`.

**This placement is conditional, and the condition is stated rather than
assumed.** Added 2026-08-22 against governance finding `DP-TEC-01`. The swap is
legal **only while `external-products` and `target-standardization` remain
independent**. That independence rests on a recorded upstream assumption:
`external-products` takes its edge from `inventory-and-registry` because IRI and
GIM are generated at the registry's pinned coordinates and cells. **Functional
design must determine which timestamp set IRI generation actually requires:**

- **the registry or inventory timestamps** — the assumption holds, the pair stays
  independent, and this Bolt order stands; or
- **the finalized standardized-target timestamp set** — the assumption fails,
  `external-products` gains a dependency on `target-standardization`, the pair
  stops being independent, and **the dependency relation and the Bolt order must
  both be revised before any dependent implementation begins.**

An invalid ordering must **not** be silently preserved after the assumption
changes. Revising the edge is a change to the stage 2.7 dependency artifact and
runs through its own approval, not through this plan.

**Independently of which way that resolves:** the final LSTM-versus-IRI
comparison must use the **same eligible timestamps** under a scientifically
defensible alignment contract, joined onto the frozen comparison-wide mask at
evaluation time. Timestamp alignment is a comparison-fairness obligation
(NFR-FAIR-01), not merely a build-order convenience, and it holds whichever
timestamp set IRI generation turns out to need.

**What it bundles.** The three externally sourced product families: the driver
series with their availability semantics, the IRI-2016 benchmark with its
pre-generation validation, and the CODE final GIM comparator with its
interpolation and network-overlap audit.

**Definition of Done.**

- Driver series are **time-indexed only** — one value per epoch, identical across
  all three cells. A join never implies a per-cell measurement.
- F10.7 uses the previous-day observed value with a **trailing** 81-day mean
  ending at the safe-lagged day. A centered mean is a defect, not a fallback.
- Kyoto Dst carries a **single recorded release grade** for all of 2022; no
  driver is backfilled from future final or definitive archived values, and each
  driver's **release status** is recorded, not only its lag.
- **The three F10.7 selection decisions, frozen 2026-08-22, are implemented as
  decided** — not re-opened here:
  - **D-21 — daily value is the daily median** of that UT day's observed readings.
    Its **availability rule is enforced, not assumed**: the value used at a
    forecast origin is the most recent daily median whose observation-completion
    time is strictly earlier than that origin. Under D-10.3's previous-day
    contract that is `median(D-1)`, complete by 23 UT on *D-1* at the latest —
    at least one hour before the earliest origin on day *D*. **`median(D)` is
    never used at any origin on day *D*.** Where the next median is not yet
    available, the most recent previously available approved value carries
    forward and the carry-forward is recorded. The 81-day mean is trailing over
    daily medians, never centered.
  - **D-22 — duplicate UT timestamps take the mean** of the duplicated
    measurements, with the duplicate count logged and a QC flag set. **If provider
    documentation later establishes one duplicate as an official correction, the
    provider's correction semantics take precedence over the mean.** That clause
    is currently unexercisable: the held file has no correction, revision or
    provenance column. No affected day is discarded.
  - **D-23 — high-spread days are flagged and retained**, with the D-21 median as
    the representative value and every affected date, spread and flag recorded.
    None is excluded from the primary dataset. **The QC flag is not a model
    feature** without separate approval and a causality check, and FR-P1-04-12's
    closed-input-space assertion is what keeps it out.
- **The suspected 2022-03-18 outage, stated at its measurement granularity
  (corrected 2026-08-22).** The suspected outage was audited against the available
  2022 source data. **No missing calendar day was observed: at least one
  observation is present on 365 of 365 calendar days.** This finding does **not**
  assert uninterrupted within-day coverage or uninterrupted provider availability,
  and is not described as "zero outage". No imputation, substitution or
  reconstruction therefore arises at day granularity. What the file cannot
  establish — and what is **not** claimed — is whether values spanning the
  incident were measured, recovered or reconstructed: it carries no qualifier,
  flag or provenance column. Asking NRCan is an optional obligation (EC1-R-4).
- **Publication latency — a conservative convention, frozen as D-25.** The held
  archive carries **no publication timestamp**, so actual publication latency is
  **unverified**. Rather than block on a provider response, a conservative
  convention is approved: **a daily F10.7 median becomes available no earlier than
  `00:00 UTC` on the following day**, so `median(D)` is never available at any
  origin on day *D* and same-day look-ahead is prevented by construction. Measured
  observation completion is 22 UT on 120 days and 23 UT on 245 days of 2022, so
  the convention delays availability by 1–2 hours beyond it in every case.
  **This is an explicit project assumption. It does not prove historical
  publication availability, and no operational real-time availability claim rests
  on it.**
- **What this Bolt writes into the F10.7 row of the availability matrix.** Fixed by
  the EV-12 amendment approved and applied 2026-08-22 (`CR-2026-08-22-EV-12`), so
  **this Bolt is not forced to proceed with an incomplete row and fills no field by
  convenience.** In place of a provider publication timestamp, the row records
  three things:
  1. **The approved conservative availability convention** — D-25.
  2. **The documented absence** of a provider publication timestamp in the held
     archive, evidenced by its seven-column inventory (`fluxdate`, `fluxtime`,
     `fluxjulian`, `fluxcarrington`, `fluxobsflux`, `fluxadjflux`, `fluxursi`).
  3. **An explicit statement that actual publication latency is unverified.**

  The same three-part form applies to any other series whose archive supplies no
  publication timestamp. Where a provider **does** supply one, it is recorded as
  before — the amendment adds a fallback, it does not replace the rule.
- **March–April 2022 provenance — unresolved, data retained (D-26).** Whether
  values spanning the suspected outage were measured, reconstructed, interpolated
  or provider-corrected is **not determinable** from the held file, which carries
  no qualifier, flag or provenance column. **Asserted in no direction.** The data
  is retained — no governing rule requires exclusion — and the limitation carries
  into the thesis reporting obligations.
- IRI-2016 generation is **blocked if its validation report fails**. The GIM
  network-overlap audit runs and `gim_network_overlap_flag` is disclosed; no
  independence claim precedes it.
- `audit_ec1_drivers.py` migrates here and its exit-code gap closes — a
  completeness shortfall becomes a machine-readable manifest field, an integrity
  violation terminates the run naming the file and the violated expectation.

**Acceptance rows owned (1).** WS-09.

**Confidence hypothesis.** That the four outside providers behave as the frozen
contract assumes — that the drivers exist at a single release grade, that the
F10.7 gap is what the audit says it is, and that IRI-2016 validates. Four of this
unit's seven requirements have no acceptance row, so this Bolt is where provider
reality is discovered by trying rather than by testing.
<!-- Superseded literal, preserved: "Five of this unit's seven requirements have
     no acceptance row". external-products fell 5 → 4 under
     CR-2026-08-22-LEAKAGE-TA, which gave FR-P1-04-17 acceptance row TA-36.
     Derived from unit-of-work-story-map.md Table 1 before assertion; the eleven
     per-unit values sum to 36. A site the CR-2026-08-22-INC-CORRECTIONS Rec 5
     sweep did not reach. -->
<!-- markdownlint-disable-line -->

**Expected demo.** Benchmark and comparator manifests, the
`iri_implementation_validation` report, the `gim_network_overlap_flag` audit
result, and driver manifests each carrying one recorded release grade.

---

### Bolt 6 — Target standardization

**Unit** `target-standardization` · **Deployment** standalone · **Depends on** `inventory-and-registry` · **Open blockers** BLK-05

**What it bundles.** Turning validated provider files into the Phase 1 hourly
target rows under D-17's contract — documented QC, UTC normalization, cell
selection and the stated hourly aggregation only, with provider values preserved.

**Definition of Done.**

- Every row carries `phase_id`, `source_id` and `target_definition_id`.
- The product is labelled **location-sampled gridded VTEC** and never described
  as receiver-specific station-observed VTEC.
- No DCB, STEC, mapping, satellite or arc field is produced — the Phase 1 hard
  prohibition, enforced by Bolt 2's guard.
- **BLK-05 discharged:** the D-17 target-schema test has a module name, approved
  as a §12 tree amendment. This stage chooses no name and neither does this plan.

**Acceptance rows owned (1).** TA-19.

**Confidence hypothesis.** That the five-column product actually available
(`ut1_unix`, `gdlat`, `glon`, `tec`, `dtec`) yields the hourly target contract
every downstream unit consumes, without any transformation being smuggled in at
standardization.

**Expected demo.** The released target rows with their stamped IDs, plus the
Phase 1 portion of the verification and target-uncertainty evidence.

**Carried defect, not resolved here.** `scripts/02_standardize_prepared_target.py`
and Phase 2's `scripts/02_build_vtec_target.py` share the ordinal `02`. The
adopted reading is that the ordinal denotes pipeline position and `--phase`
selects exactly one, so a clean run contains one `02` per phase. Code generation
must **not** invent a `02a`/`02b` convention.

---

### Bolt 7 — Features and splits

**Unit** `features-and-splits` · **Deployment** standalone · **Depends on** `target-standardization`, `external-products`, `governance-guards` · **Open blockers** BLK-04, **BLK-08** (co-owned with Bolt 9), **BLK-09**

> **⚠ Two blockers added 2026-08-24, and this Bolt now carries the most of any.**
> **BLK-08** (co-owned): `Transform` and its fitted state live in this unit, so
> whatever mechanism reaches the inverse changes this Bolt's contract as well as
> Bolt 9's. Its **scientific limb was answered 2026-08-24 — no**, the primary
> transform does not touch the target (TE §7.2: *Primary remains, Raw TECU*), so this
> unit's train-only scaler acts on **target-derived inputs** and no primary-path
> inverse is owed. Its **mechanism limb stays open and narrows to `ABL-DIFF`**, the one
> configuration that does transform the target, authored here at functional design
> jointly with Bolt 9. **BLK-09**: `Partition` carries no `train_start`, so the training range that
> two of ADR-11's raises compare against rests on an unwritten January-1 convention.
> Deriving it from `train_end` and a hard-coded year is not available — TC-03e forbids
> a scientific constant in source.
>
> **Three of the eight open blockers land here**, against 2 direct and 5 transitive
> dependent units. That concentration does not change this Bolt's position — it
> already sits after its dependencies and before its dependents, and no available
> order reduces it — and it is recorded as accepted risk in
> `risk-and-sequencing-rationale.md` under the owner's Q15 = A ruling. All three
> remain **exit** conditions on functional design, never entry conditions.

**This Bolt authors the M10 contract fixture** (owner ruling Q12 = C at
units-generation, 2026-08-23). Neither mandated walking-skeleton fixture can exercise
ADR-11's redesigned leakage boundary — partitions come from the frozen 2022 calendar
boundaries, while D-11 froze the plumbing window at 2022-11-01 to 2022-11-07 — so this
Bolt writes a **synthetic** fixture over synthetic partition dates asserting four
things: (a) the identity check raises for every ordered pair of partition ids except
the enumerated `REFIT` → `DEC`, by enumeration rather than sampling; (b) that pair
passes with `role="score"` and raises with `role="train"`; (c) `fit_transforms` raises
when the bundle's scored range is not exactly the partition's training range; (d)
`06`/`07` and `fit_predict` raise on any bundle with `transform_id is None`. It goes in
the **existing** mandated modules `test_train_only_transforms.py` and
`test_split_embargo.py` — deliberately not a new `tests/fixtures/` directory, which
would be a §12 tree amendment needing its own change record. **Bolt 12 runs it** in the
clean-run sequence; this Bolt does not.

The densest Bolt in the plan — nine acceptance rows, more than any other unit.

**What it bundles.** The closed ML input space and the partitions that make
forecasting honest: the availability matrix, feature construction, per-fold
train-only transforms, one shared window definition emitting both the flattened
matrix and the sequence tensor, the F1–F4 exact calendar folds with their 24-hour
embargo, and the December locked partition's execution guard.

**Definition of Done.**

- The availability matrix asserts **actual lag ≥ declared safe lag** for every
  primary feature: Kp/ap3 ≥ 3 h, Hp60/ap60 ≥ 1 h, F10.7 at the previous-day
  observed value with its trailing mean.
- `build_features` **raises** on anything outside the §6.2 dictionary, on any
  `iri_*` field, on a carried-forward `vtec_lag_*` value, on a driver repeated
  outside its own interval, and on a support field used as a model input without
  G-04 approval. `test_iri_denial.py` **must fail on deliberate injection**.
- Transforms are fitted on the named fold's training partition only, per fold,
  never on the full dataset.
- F1–F4 are exact fixed calendar boundaries with a 24-hour embargo; no window
  crosses a boundary, and the first 24 hours are excluded and counted. No random
  or shuffled cross-validation.
- Missing driver values carry forward at most 3 hours, then the row is excluded.
- Raw longitude never enters as a predictor — longitude enters only through
  `lst_sin` and `lst_cos`.
- **BLK-04 discharged:** the governed cross-unit transform contract is approved,
  fixing input and output types, alignment, ownership of the fitted state,
  allowed partitions (the named fold's training partition only) and failure
  conditions — a `LeakageError` when `train`'s index is not a subset of that
  partition.

**Acceptance rows owned (9).** WS-10, WS-11, WS-12, WS-13, WS-18, TA-07, TA-08,
TA-11, TA-18.

**Confidence hypothesis.** That the leakage paths are closed by mechanism rather
than by review — that an injected `iri_*` field is caught, that a boundary-
crossing window cannot be produced, and that a full-dataset fit raises. Every
number the thesis reports rests on this Bolt being right.

**Expected demo.** The injection test failing as designed; fold manifests with
excluded-row counts; the matched-window parity assertion over one `windows.py`
definition.

**Leakage prerequisites — promoted out of the ordinary untested set, 2026-08-22.**
Against governance finding `DP-ML-01`, the owner ruled that four of this unit's
untested requirements are **not** ordinary missing acceptance rows: they are
leakage controls, and each is a **prerequisite for trustworthy model training and
evaluation**. A negative-path test is specified for each below, demonstrating
that the prohibited behaviour is *detected and rejected* rather than that the
happy path works. Each specification is derived from the requirement's own
existing pass/fail criterion — no new scientific rule is created here.

| Requirement | Prohibited behaviour | Negative-path test specification |
|---|---|---|
| **FR-P1-04-12** — closed input space | Unauthorized feature-dictionary expansion | Inject a field absent from the TE §6.2 dictionary into feature construction; `build_features` **must raise**, not pass silently. Second limb: set `experiment.yaml`'s window length into a grid; the run **must fail** rather than tune it, the primary history window being a frozen constant at 24 h and not a hyperparameter. |
| **FR-P1-04-13** — target-derived lag contract | Invalid carried-forward VTEC lag values | Inject a carried-forward `vtec_lag_*` value; construction **must fail**. Second limb: present an incomplete 24-step `vtec_seq_24` window; it **must be excluded and counted**, not filled. The ≤ 3 h carry-forward allowance is scoped to external drivers and **must never reach `vtec_lag_*`** — the test asserts that boundary directly. |
| **FR-P1-04-16** — support-field rules | Unapproved support-field inclusion | Use a support field as a model input with no recorded G-04 approval ID; construction **must fail**. Second limb: read a support field at or beyond hour *t*; **must fail**. Target-hour quality fields stay permanently forbidden as features. |
| **FR-P1-04-17** — driver alignment contract | Driver-interval repetition or propagation that could carry future information | Two negative controls in one test: a Kp value repeated **outside** its own 3-hour interval **must fail**, and a Dst value shifted to a neighbouring hour **must fail**. Third limb: a check finds **no interpolation call on any driver series**, at any stage. |

**Status, stated exactly — four distinctions, none of them collapsible.** These
are **test specifications, not test results.** Each of the four now **has** a §19
acceptance row — **TA-33, TA-34, TA-35 and TA-36**, created under
`CR-2026-08-22-LEAKAGE-TA` on the project decision owner's explicit approval. None
has an **implemented test**: no module exists for any of the four, and module
placement is an open assignment at functional design. None has been **executed**.
None has **passed**. All four §19 rows read `Pending`. Nothing here may be read as
evidence that any of the four is tested or passing — a row that tests a
requirement on paper is a different fact from a requirement being tested.

<!-- Corrected 2026-08-22. Superseded text, preserved for the audit trail:
     "These are **test specifications, not test results and not acceptance
     rows.** None of the four has a §16 or §19 row today, and creating one is a
     Vision §15.2 amendment that this stage cannot grant — it is carried to the
     owner as a named decision."
     True when written; false the same day, once CR-2026-08-22-LEAKAGE-TA created
     TA-33…TA-36 under the owner's approval. A site the
     CR-2026-08-22-INC-CORRECTIONS Rec 5 sweep did not reach — that sweep
     searched count literals, and this defect carries no count. -->
<!-- markdownlint-disable-line -->

**Remaining recorded gap.** The fifth untested forbidden edge in this unit —
FR-P1-04-10 — and the balance of the 36 untested requirements stay in the
ordinary set handed to NFR requirements.

**Open evidence question (WS-13).** Table 2 of the story map gives WS-13's
evidence as a matched-window parity assertion, while §16's WS-13 row names
`test_common_masks.py` — owned by a different unit. Neither reading was adopted
upstream; functional design owns the choice, and any change to §16's evidence
column runs through Vision §15.2.

---

### Bolt 8 — Models and baselines

**Unit** `models-and-baselines` · **Deployment** standalone · **Depends on** `features-and-splits` · **Open blockers** BLK-03, BLK-04 ↓

**What it bundles.** The six model families — persistence, 24-hour seasonal
persistence, station×month×hour climatology fitted on training partitions only,
Ridge with its grid of 6, Random Forest with its grid of 18 (direct only), and
the compact LSTM with its grid of 16 (direct only) — plus training orchestration,
the three-seed run, checkpointing and restore, and the predeclared ablations.

**Definition of Done.**

- The three-seed element-wise mean is the confirmatory prediction, and the frozen
  seed set reaches it **as a parameter from `ConfigSnapshot.seeds`** via
  `configs/seeds.yaml` — never inlined in `src/models`, never weakened to a
  pairwise-distinctness check.
- Tuning uses **January–November only**. The trigger is December being *seen*,
  not the locked test being opened.
- No Random Forest importance score adds, removes or ranks a feature into the
  production feature set; RF importance is a non-authoritative diagnostic figure.
- Grids are exact and committed to configuration before G-05, and never change
  after December is seen. No seed is selected on validation or after seeing
  December.
- Residual and GRU modules are **absent by design**, and their absence is
  grep-evidenced. TensorFlow/Keras is the only NN stack; PyTorch is prohibited.
- Ablations are predeclared as named runs in `experiment.yaml`; `ABL-DIFF`
  inverse-transforms to absolute TECU before any metric, and `ABL-HIST48` runs
  only after the primary configuration is frozen.
- **BLK-03 discharged:** the governed cross-unit contract for the confirmatory
  prediction is approved.

**Acceptance rows owned (5).** WS-14, WS-15, TA-12, TA-13, TA-26.

**Confidence hypothesis.** That all six families train and predict on the frozen
folds, and that the confirmatory prediction is reproducible from the frozen seed
set. Seven of this unit's nine requirements have no acceptance row — tied for the
largest untested **count** at seven, and the largest untested **proportion** of
any unit at 78% — so the demo carries most of the weight.
<!-- Clarified 2026-08-22. Superseded literal, preserved: "the joint largest
     untested share". "Joint" was right about the count and silent about the
     proportion, where this unit is not joint but outright first. Derived from
     unit-of-work-story-map.md Table 1; see the acquisition Bolt above for the
     full ranking. -->
<!-- markdownlint-disable-line -->

**Expected demo.** Per-model prediction artifacts, a checkpoint restored from
lowest validation RMSE, and the three-seed mean artifact carrying its seed set.

---

### Bolt 9 — Evaluation and comparison

**Unit** `evaluation-and-comparison` · **Deployment** standalone · **Depends on** `models-and-baselines`, `external-products` · **Open blockers** **BLK-08** (owned), BLK-03 ↓, BLK-04 ↓, **BLK-09 ↓**

> **⚠ This Bolt now OWNS a blocker, added 2026-08-24 — and it blocks a reported
> quantity rather than an internal detail.** **BLK-08**: `Transform.inverse` is
> specified as reachable from `Prediction.transform_id`, which is typed `str`. A string
> has no method, no lookup or registry is named anywhere in the 2.6 design, and
> `component-dependency.md` carries no `src/evaluation` → `src/features` edge. So this
> unit — the one that needs the inverse — has **no route to it**.
>
> What that blocks, concretely: `project.md` § Mandated requires `ABL-DIFF` to
> *"inverse-transform to absolute TECU before any metric"*, and every number this Bolt
> produces or feeds downstream is TECU-denominated — the paired loss differential, and
> through Bolts 10 and 11 the bootstrap interval and the practical-relevance threshold
> comparison. If the train-only transform touches the target, model output is in
> transformed space and nothing in the current design returns it to TECU.
>
> **Split by the owner's Q13 = C ruling — and the scientific limb is now answered.**
>
> **Scientific limb: ANSWERED 2026-08-24 — no.** The primary configuration's train-only
> transform does not touch the target. TE §7.2's `ABL-DIFF` row states **Primary
> remains: Raw TECU**; TE §6.2 standardizes target-derived *inputs* (`vtec_lag_*`,
> `vtec_seq_24`) rather than the y being predicted; nothing in either governing
> document scales the target. **So this Bolt's primary outputs are already in raw
> TECU** and the paired loss differential needs no inverse. That fact must be stated
> explicitly in the design rather than left implicit.
>
> **Mechanism limb: open, and narrower than when registered.** `ABL-DIFF` remains the
> one configuration that transforms the target, and TE §7.2 requires its inverse
> **before** metrics with **error propagation recorded**. Functional design names how
> that inverse is reached and where the propagation is recorded — jointly with Bolt 7,
> which co-owns it because `Transform` and its fitted state live there. What the ruling
> removes is the need for a general `src/evaluation` → `src/features` route on the
> primary path, which was the design pressure behind the original Critical finding.
> This Bolt **may enter** functional design and **may not complete** it without the
> mechanism limb resolved.

**What it bundles.** One comparison-wide intersection mask computed once per
comparison set with a stable ID and reported row counts, the IRI-free denial check
applied at join time, and the confirmatory estimand — the mean within-station
difference of squared errors, benchmark minus model, equal-station weighting,
positive favouring the model.

**Definition of Done.**

- **One** comparison-wide mask per comparison set. Never pairwise, never
  model-specific.
- IRI and GIM join **only at evaluation time**, onto the already-frozen mask, and
  never reach training or inference.
- The locked-test predictions are generated and written **exactly once**, after
  G-05 is signed, and **hashed before any metric is computed**.
- Evaluation code is authored, reviewed and frozen as part of the G-05 set before
  December is opened.

**Acceptance rows owned (1).** WS-16.

**Confidence hypothesis.** That the comparison is fair by construction — that the
mask is computed once and shared, so no model can be advantaged by a mask fitted
to it.

**Expected demo.** The mask registry with stable IDs and row counts; the paired
loss differential computed on the frozen mask.

---

### Bolt 10 — Statistical inference

**Unit** `statistical-inference` · **Deployment** embedded · **Depends on** `evaluation-and-comparison` · **Open blockers** BLK-03 ↓, BLK-04 ↓

Owns no stage script — its logic runs inside `07_evaluate_and_report.py`, which
Bolt 9's unit owns.

**What it bundles.** The vector time-block bootstrap: 24-hour blocks carrying all
three stations together, 10,000 replicates, its own generator seeded from the
separately frozen 20221201, a 95% confidence interval, a 48-hour sensitivity, and
the cross-station paired-error correlation.

**Definition of Done.**

- The vector construction is used. A within-station or naive bootstrap is
  **never** substituted — it produces systematically narrower intervals, and the
  within-station 2,000-replicate variant was rejected at Q-27.
- The seed is a **required parameter** read from `seeds.yaml`, never defaulted and
  never inlined. It is frozen separately from the three model seeds.
- The run stays inside the 10.0 GB hard planning envelope on the CPU path.

**Acceptance rows owned (2).** WS-17, TA-14.

**Confidence hypothesis.** That the heaviest computation in the pipeline —
10,000 replicates over vector blocks — completes on CPU inside the storage
envelope and reproduces exactly from its seed. CPU is a complete execution path
here, not an emergency mode, so this is the Bolt where that claim is tested
rather than asserted.

**Expected demo.** The replicate hash from seed 20221201 reproducing exactly, the
48-hour sensitivity, and the cross-station correlation, verified on synthetic
correlated data.

**This is the only unit with full acceptance coverage** — its single requirement
has a test row. Every other unit carries at least one requirement that nothing
tests.

---

### Bolt 11 — Regimes, diagnostics and reporting

**Unit** `regimes-diagnostics-reporting` · **Deployment** embedded · **Depends on** `statistical-inference` · **Open blockers** BLK-03 ↓, BLK-04 ↓

**What it bundles.** Everything between a computed interval and a defensible
statement: Kp/Hp60 regime strata and the storm-event rule, quality strata with the
top-1%-removed sensitivity, the required plots each carrying its source-data IDs,
the primary results table, the mandated disclosures, and the
claims-and-limitations checklist.

**Definition of Done.**

- The three mandatory difficulty controls — persistence, 24-hour seasonal
  persistence, and fitted station×month×hour climatology — are co-reported in the
  **same primary results table** as the LSTM-versus-IRI comparison, never
  relegated to an appendix.
- **Any baseline that beats the LSTM on the locked test appears in the primary
  results table and in the abstract-level conclusion.** A favourable
  LSTM-versus-IRI result never licenses silence about an unfavourable
  LSTM-versus-persistence or LSTM-versus-climatology result.
- The spatial-representativeness mismatch is stated wherever an IRI or GIM
  comparison is reported.
- The abstract-level interpretation states that Phase 2 is a **fixed-protocol
  replication on a new target lineage, not a second statistically independent
  blind test**.
- Every claim is bounded to the frozen scope: hourly VTEC at ARUC 40/44,
  BSHM 32/35, NICO 35/33, calendar 2022, tested on December 2022 only. No
  question requiring 5-minute resolution at NICO is claimed.
- No practical-relevance threshold is introduced, changed or reinterpreted after
  December is opened; any test-driven pipeline change made after locked-test
  access is labelled exploratory.

**Scientific reporting obligations, added 2026-08-22** against governance finding
`DP-ML-02`, which found these present in the surrounding prose but absent from
the list that actually gates the Bolt:

- **The primary result is calculated on the complete predefined evaluation set** —
  the frozen comparison-wide intersection mask, whole and unfiltered.
- **The top-1%-error-removed analysis is a separate sensitivity analysis.** It is
  reported alongside the primary result and **never replaces it, never improves
  it, and is never presented as the headline number.** A sensitivity that looks
  better than the primary result is still the sensitivity.
- **The target uncertainty budget is displayed adjacent to the primary reported
  result** — not in an appendix, not in a separate document. Production of the
  budget is Bolt 6's obligation under TA-19; its adjacency here is this Bolt's.
- **Station-specific results are reported for ARUC, BSHM and NICO** wherever the
  approved evaluation design requires them, so an aggregate gain driven by one
  station is visible rather than hidden. Equal-station weighting in the estimand
  does not discharge this: weighting governs how the aggregate is formed, and
  this governs what is shown.

**Acceptance rows owned (3).** WS-19, TA-16, TA-20.

**Confidence hypothesis.** That the honesty rules are enforceable as artifacts
rather than as intentions — that the results table structurally cannot omit a
control, and that the claims checklist records, class by class, that no artifact
asserts a prohibited claim.

**Expected demo.** The primary results table with all three controls present; the
figure set, each figure carrying its source-data IDs; the claims-and-limitations
checklist.

**Carried finding.** FR-P1-05-18 requires the storm-event count to come from GFZ
Kp/Hp60 at a recorded release grade and bars any provisional-Dst-derived figure,
but no criterion tests that source. The designed signature makes the source an
explicit required argument so a test *can* assert it; writing the criterion is a
`requirements.md` change.

---

### Bolt 12 — Fixtures and reproducibility

**Unit** `fixtures-and-reproducibility` · **Deployment** standalone · **Depends on** nine units · **Open blockers** BLK-02, BLK-03 ↓, BLK-04 ↓, **BLK-08 ↓**, **BLK-09 ↓** · **In-Kaggle critical test run required**

> **⚠ BLK-08 ↓ and BLK-09 ↓ added 2026-08-24**, by the same inheritance rule that
> already brought BLK-03 and BLK-04 here: this Bolt's `depends_on` reaches every unit
> carrying them, and the clean-run tolerance comparison and TA-21's traceability matrix
> consume their released artifacts. **BLK-08 ↓ bounds the units of every tolerance this
> Bolt compares** — a clean-run tolerance stated in TECU cannot be checked against
> output that no design path returns to TECU.

**This Bolt runs the M10 contract fixture** (owner ruling Q12 = C at units-generation,
2026-08-23), authored by Bolt 7. Running it here is what puts it inside TA-17's and
WS-20's reach, which authorship alone would not.

> **⚠ The M10 contract fixture is NOT a third mandated fixture.** It is a **negative
> control on a mechanism**, not evidence about the pipeline, and TC-03f's distinction is
> stated here rather than left to inference. The two mandated walking-skeleton fixtures
> remain exactly two: the seven-day single-station plumbing fixture (smoke only, never
> scientific evidence) and the one-month all-station scientific fixture. Technical
> Environment §9.2's *"run both walking-skeleton fixtures before any full-year job"* is
> unchanged and unextended, and **no full-year job gates on the contract fixture**.

The closing Bolt. Depends directly on nine units for two distinct reasons: seven
own a stage script the clean-run sequence invokes, and two (`statistical-inference`,
`regimes-diagnostics-reporting`) own none — their edges rest on the released
artifacts the clean-run tolerance comparison and the traceability matrix consume.

**What it bundles.** The two fixtures and their manifests, the orchestrator that
enforces both-in-order before any full-year job, and the ordered clean-run
contract reproduced on CPU.

**Definition of Done.**

- Both fixture manifests carry all thirteen §15.2 content areas — identity, input
  hashes, expected schema, row-count ranges, support and missingness limits,
  timestamp tolerances, required outputs, expected CPU runtime range **measured
  before freeze**, and permitted floating-point tolerances. **Per the Q12 answer,
  these are assembled from the measured fields each earlier Bolt recorded**, not
  reconstructed here.
- `run_walking_skeleton.py` enforces plumbing-then-scientific-then-full-year. The
  seven-day fixture is **never** treated as scientific evidence — not cited, not
  plotted as a result, not interpreted as skill.
- **No record whose observation date falls in December 2022 enters either
  fixture**, asserted on record dates rather than on the folder a file was filed
  under.
- The ordered clean-run sequence completes on CPU from a clean environment;
  §13.7's exact-equality classes hold **exactly** — hashes, schemas, partition
  membership, IDs and deterministic CPU transformations compare for equality, not
  tolerance, and a mismatch **must not silently update the expected value**.
- The critical test set and both fixtures run **inside the Kaggle session** before
  any governed run executed there.
- **BLK-02 station limb discharged 2026-08-22 (D-20): the `plumbing_7day` fixture
  runs on BSHM 32/35**, selected on complete measured coverage (168/168 hourly
  bins, 7/7 days) of D-11's window. ARUC's unexplained one-bin shortfall on five
  of seven days does **not** need discharging, because ARUC is not selected; that
  obligation revives only if ARUC is later chosen for this fixture. ARUC and NICO
  are the right candidates for **separate** missing-data and robustness tests,
  where their gaps are the subject rather than a confound.
- **Still open on the manifest:** identity is frozen, content is not. **No
  manifest value is invented, inferred or substituted** — every §15.2 content
  area is measured from a fixture run that has not yet happened.

**Acceptance rows owned (4).** WS-20, TA-09, TA-17, TA-21.

**Confidence hypothesis.** That the whole pipeline reproduces from nothing on a
clean CPU environment within declared tolerances — the claim G-07 accepts, and the
one a thesis examiner is most likely to test.

**Expected demo.** The clean-run log with matched artifacts, both fixture
manifests, the `environment_and_cpu_preflight_report` with its four measured
elements inside the 10.0 GB envelope, and the traceability matrix connecting each
implemented requirement to a decision, a test and an evidence artifact.

**Frozen fixture windows, for the record.** The seven-day plumbing window is
D-11: 2022-11-01 to 2022-11-07 inclusive. The one-month all-station scientific
window is D-14: March 2022, all three cells. Both carry the mandatory limitation
that they reproduce neither December's winter-solstice regime nor its activity
distribution, and neither is representative of the locked month.

---

## Infrastructure Design is `SKIP` — where its obligations went

Added 2026-08-22 against governance finding `DP-CHAIR-04`. Stage 3.4
(`infrastructure-design`) is `SKIP` in this scope and **stays `SKIP`** — no
separate stage is needed, because this pipeline provisions nothing: two fixed
platforms, no deployment target, no infrastructure to design. What that skip does
remove is the usual **carrier** of a set of obligations that remain fully binding.
Each is mapped below to the Bolt that owns it, the evidence that discharges it,
and the gate that accepts it, so no obligation is left without an address.

| Obligation | Owning Bolt | Required evidence | Gate |
|---|---|---|---|
| **Local versus Kaggle execution responsibilities** — exactly two authorised platforms; a governed run whose recorded `platform` is neither **fails** | Bolt 1 (records `platform` per run); every Bolt that executes a governed run | Registry `platform` values a subset of {Kaggle, local}; install logs from both platforms | G-07, G-09 |
| **Configuration handling** — exactly four governed configs, no scientific constant in source or notebook, zero-`TBD` assertion | Bolt 1 | Config inventory, schema validation, the automated zero-`TBD` preflight | G-09 (TA-02, TA-23) |
| **Secrets handling** — credentials via platform secret store or environment configuration excluded from version control; none in notebook, source, config snapshot, log or registry note | Bolt 1 (mechanism), Bolt 3 (the consumer that reaches the provider client) | Secret scan over tree, history, configs, logs and artifacts; `.gitignore` deny-list present before the first commit | G-09 (TA-22) |
| **Data-transfer hashes and provenance** — §9.1's inter-platform transfer rule: a SHA-256 manifest accompanies every artifact crossing between platforms, and the transfer itself is recorded | Bolt 1 (the release and hashing API), each Bolt that transfers | Transfer manifests and recorded transfer events | G-07 (TA-03, TA-15) |
| **Storage and memory limits** — the 10.0 GB hard planning envelope; recorded use at or below it **fails** the check rather than warning | Bolt 1 (first measurement), Bolt 10 (heaviest job), Bolt 12 (re-measurement) | `environment_and_cpu_preflight_report` with measured CPU runtime, peak RAM and storage | G-07 (REQ-ENG-11, TA-17) |
| **CPU execution as a complete path** — GPU is an optional accelerator only; no result depends on it | Bolt 10, Bolt 12 | Clean-run log on a CPU-only environment | G-07 (TA-17, WS-20) |
| **Clean-run requirements** — the §13.2 ordered sequence completing from a clean environment, with §13.7's exact-equality classes holding exactly | Bolt 12 | `tests/test_clean_run.py`, clean-run log, matched artifacts | G-07 (TA-17) |
| **Session-specific Kaggle test evidence** — the conditional rule stated in § "What every Bolt owes" | Any Bolt performing a governed Kaggle run | In-session critical-test and fixture results in that run's evidence record | G-07, G-09 (TA-03, TA-26) |

**Nothing here is new.** Every row restates an obligation already carried by a
requirement or acceptance row; the table exists so a reader checking 3.4's
coverage finds a forwarding address rather than a skipped stage.

## What this plan does not decide

- **No scientific constant, and no supervisor-owned value.** BLK-02's station,
  BLK-05's module name and BLK-06's enumeration appear here only as *scheduling*
  facts — when the request is raised and what the Bolt does while it waits.
- **No requirement, acceptance row or dependency edge is added, reworded or
  reinterpreted.** The 36 requirements with no acceptance row and TA-24's absent
  implementing unit are carried forward, not closed.
  <!-- Superseded literal, preserved for the audit trail: "The 40 requirements
       with no acceptance row". Corrected 2026-08-22 — a site the
       CR-2026-08-22-INC-CORRECTIONS Rec 5 sweep did not reach. The figure moved
       40 → 36 under CR-2026-08-22-LEAKAGE-TA, whose four new rows (TA-33…TA-36)
       removed FR-P1-04-12, -13, -16 and -17 from the untested list. Re-derived
       before assertion, two independent artifacts agreeing on 36 and their ID
       lists set-differenced to identical; see
       governance/reviews/GOV-2026-08-22-DP-01.md § DP-ML-01 for the derivation
       and for the range-lead pitfall that makes a naive count read 40. -->
<!-- markdownlint-disable-line -->
- **No amendment to any governed artifact.** Where closing a gap needs a §16 or
  §19 change, it runs through Vision §15.2 change control.

## Assumptions & Open Questions

- **Resolved 2026-08-22, no longer an assumption.** Gate 0's two-kind split was
  carried as an interpretation of the Q8 answer. The project decision owner ruled
  it explicitly against `DP-CHAIR-02`: functional design may begin on BLK-05 and
  BLK-06 **only to analyze them and produce the evidence their resolution needs**,
  neither is resolved without an explicit owner decision, and no dependent
  implementation, code generation, governed execution or downstream activity
  begins until that decision is approved and recorded. See § Gate 0.
- **[assumption]** Bolt 1's Definition of Done reads REQ-ENG-1 as requiring the
  §12 tree to **exist** item for item, with module content belonging to the Bolt
  that owns each module. TA-01's evidence column is "repository tree and code
  commit", which supports this reading, but no artifact states it explicitly.
- **[assumption]** The Q11 answer's narrower reading of TC-06's "test suite" —
  the tree, conftest and the modules whose subject exists, rather than all
  twenty-one up front (nineteen when this assumption was written; the TE §12 tree
  reached twenty-one later the same day) — is recorded here and flagged for the next
  practices-affirmation gate alongside RES-02's two stale figures. This stage
  cannot edit `team-practices.md`; `org.md` reserves that file for that gate.
- **Open, carried not closed.** BLK-02 through **BLK-09** (**eight** open blockers),
  RES-01 through **RES-05**, the 36 untested requirements, TA-24's missing
  implementing unit, the `02` ordinal collision, WS-13's evidence departure, and
  the AGPLv3 distribution question. Each is enumerated with an owner in
  `external-dependency-map.md` or in the upstream blocker register. *(Counts
  corrected 2026-08-24 from "BLK-02 through BLK-07 (six open blockers)" and
  "RES-01, RES-02 and RES-03": BLK-08 and BLK-09 were registered 2026-08-23, RES-04
  and RES-05 likewise. Derived from the register's `| Status |` rows — eight, every
  one beginning `Open` — and its `### RES-0…` headings.)*
- **Closed 2026-08-24 — BLK-08's scientific limb.** Returned to the owner under the
  Q13 = C ruling rather than absorbed, and **answered at this stage's approval gate**:
  **no**, the primary configuration's train-only transform does not touch the target,
  which stays raw TECU; `ABL-DIFF` alone transforms it and keeps its inverse
  obligation. Gate 0 carries **no live item** again. Numbered **D-27** in
  `evidence/DECISIONS.md` on 2026-08-24, on the owner's explicit instruction at this
  gate — see § Gate 0 § ✅ BLK-08 SCIENTIFIC LIMB.
- **Open, narrowed not closed.** **BLK-08's mechanism limb** — how `ABL-DIFF`'s
  inverse is reached and where its error propagation is recorded — resolved at
  functional design, jointly by Bolts 7 and 9. The 2026-08-24 ruling removes the need
  for a general primary-path inverse, which was the pressure that made the original
  finding Critical.
- **None** of the above adopts a reading on a supervisor-owned value, and none
  decides a scientific constant.

## Corrections applied on resume, 2026-08-22

Four defects were corrected in this file after the first summary confirmation and
before the approval gate. Each preserves its superseded literal in place, per
`governance/CHANGE_RECORD_PROCEDURE.md` step 1. **None changes a Bolt, a sequence,
a Definition of Done, an owner, a gate, an acceptance row or a scientific value.**

| Site | Defect | Reach of the Rec 5 sweep |
|---|---|---|
| § What this plan does not decide | "The **40** requirements with no acceptance row" → **36** | Missed — a count literal the sweep did not reach |
| § Bolt 3 confidence hypothesis | "**Five** of this unit's seven requirements have no acceptance row" → **four** (`external-products` fell 5 → 4 under `CR-2026-08-22-LEAKAGE-TA`, which gave FR-P1-04-17 row TA-36) | Missed — same |
| § Bolt 3 confidence hypothesis | "the largest untested **share** of any unit" — wrong when written, and a direct contradiction of § Bolt 10's "joint largest" claim in this same file. Count and proportion are now named separately | **Out of reach** — a stale superlative carrying no numeral |
| § Bolt 7 status paragraph | "none of the four has a §16 or §19 row today, and creating one is a Vision §15.2 amendment that this stage cannot grant" — TA-33…TA-36 were created the same day under the owner's approval | **Out of reach** — a stale claim carrying no numeral |

The last two are the ones worth noting as a class: `CR-2026-08-22-INC-CORRECTIONS`
Rec 5 swept for **count literals**, so it was structurally unable to see a stale
superlative or a stale claim with no number in it. The procedure that record
established inherits the same blind spot at its step 2 ("sweep the workspace for
that literal"). Raised at the approval gate rather than corrected there, because
that record is a completed change record and `CHANGE_RECORD_PROCEDURE.md` reserves
those from sweep edits.

**Derivations, printed before assertion** (`project.md` § Way of Working). The
untested total is **36**, derived twice from two independent artifacts whose ID
lists were then set-differenced and found **identical**:

```
grep -c "NO CURRENT ACCEPTANCE ROW" ../units-generation/unit-of-work-story-map.md   -> 36
grep "UNTESTED" ../requirements-analysis/requirements.md \
  | grep -vE "^\| *\*{0,2}(REQ|FR|NFR)-[A-Z0-9-]+…" \
  | grep -oE "(REQ|FR|NFR)-[A-Z0-9-]+" | sort -u | wc -l                            -> 36
```

Per-unit untested counts, derived from story-map Table 1 and summing to 36:
`models-and-baselines` 7/9 · `acquisition` 7/15 · `regimes-diagnostics-reporting`
7/11 · `external-products` 4/7 · `inventory-and-registry` 2/7 · `foundation` 2/18
· `fixtures-and-reproducibility` 2/8 · `evaluation-and-comparison` 2/4 ·
`target-standardization` 1/6 · `governance-guards` 1/11 · `features-and-splits`
1/12.

> **Caution for anyone re-deriving the 36.** The second command above must exclude
> rows whose lead is an ID *range*. Four crosswalk rows in `requirements.md`
> (`FR-P1-03-1…5`, `FR-P1-04-1…18`, `FR-P1-05-1…22`, `REQ-ENG-1…13`) mention
> `UNTESTED` for one member of the range, so a naive extraction attributes it to
> the range's first ID and the count reads **40**. That error surfaced here only on
> set-differencing the two ID lists — comparing the two totals showed a difference
> and gave no indication which side was wrong.
