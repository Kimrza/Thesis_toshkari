# Business Rules — `governance-guards`

> ## ✳ G-09 IS SIGNED — 2026-08-28, **D-31** (read this before any G-09 statement below)
>
> The project decision owner **signed and approved G-09 (Agent preflight)** on 2026-08-28,
> recorded as **D-31** in `evidence/DECISIONS.md` with change record
> `governance/CHANGE_RECORD_2026-08-28_G09_signed.md`. **Every statement below of the form
> "G-09 is not signed" / "G-09 stays unsigned" is superseded as to the gate's status**, and
> is left standing as the accurate record of the constraint that applied when it was
> written.
>
> ⚠ **D-31 records the gate's own TE §18.3 preconditions as UNMET, and that disclosure
> travels with the signature.** `configs/`, and until 2026-08-28 `src/`, did not exist, so
> the mandated automated zero-TBD preflight **could not run**; the ten named critical tests
> **cannot be executed in this environment** (no Python interpreter is installed — a
> zero-byte Windows Store stub, no registry entry, no interpreter on disk); and the evidence
> artifact `aws_ai_dlc_preflight_report` **does not exist**. "No failing critical test" is
> therefore **unproven, not proven** — an absence of executions, not an absence of failures.
> This is the owner **opening the gate by authority**, not a record that its evidentiary
> conditions were satisfied, and no reader may infer the second from the first.
>
> **What the signature changes here:** module creation is authorised, and any defect this
> unit deferred *solely* because G-09 barred editing a file is now correctable.
> **What it does NOT change:** G-05 and G-06 remain `Blocked`; G-P1A, G-P2, G-P3A, G-P3C
> and G-07 are unaffected; **TE §18.2's absolute rule stands** — every scientific value this
> unit routed to G-04/G-05 **stays routed**, and no agent may fill a freeze-gate value by
> convenience; and **§18.3's stop-and-report obligation survives its own gate**, being a
> standing rule on implementation rather than a one-time gate condition.

**Unit** `governance-guards` (Bolt 2) · **Kind** `library` · **Depends on** `foundation`

> **Re-established a sixth time 2026-08-24**, on a **new stage attempt** — Inception closed
> and Construction opened at 2026-08-24T11:46:26Z, resetting the receipt floor for every unit.
> **No rule of this unit changed.** `foundation`'s amendment pass of the same day
> (`governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md`) touches no contract this
> unit cites — **A** declined so no count propagated, **B** amended `DeterminismRecord`,
> **C** amended `services.md` § Run record and registry and `unit-of-work.md` § 1, none read
> here. **The READY verdict in § Review belongs to the previous attempt**; a fresh pass
> follows.

> **Re-established a fifth time 2026-08-23**, after a redo correcting a sibling unit's
> cross-references to **R-20 below** — `target-standardization` had been attributing it to
> `inventory-and-registry`, whose rules run R-44…R-53. **No rule of this unit changed.**

> **Re-established 2026-08-23 after a stage-wide redo jump**, which reset the receipt floor
> for every unit of this stage and, for this unit, the **exhausted adversarial reviewer
> budget**. **No rule changed at re-establishment.** The regenerated rules — including
> R-19's reversal and R-19a's mitigation, until now disclosed as unreviewed — receive a
> fresh pass. **That pass returned READY** on its second iteration, having found and had
> corrected one Critical: an arithmetic slip in the taxonomy proof, not a rule. **The
> reversal in R-19 and the mitigation in R-19a were examined and held.**
>
> **Re-established again 2026-08-23** after a further stage-wide redo aimed at
> `external-products`; **no rule changed on that occasion.** **A third re-establishment**
> followed a redo aimed at a misread depth policy in `component-methods.md`; **no rule
> changed then either.** **A fourth** followed a sweep of two sibling question files; **no
> rule changed then either.**

The prohibitions this unit enforces at run time, each with what it rejects, what it
raises, and the negative control that proves the rejection happens.

**This project's affirmed methodology is a negative control paired with every hard
rule** — a test that proves the violation is *caught*, not only that the happy path
works. Every rule below carries its negative control, and where no acceptance row
exists to accept that control, it says so.

**Rule IDs continue `foundation`'s single sequence.** `foundation`'s
`business-rules.md` runs R-01 through R-17, so this unit opens at **R-18**. This is
the numbering assumption stated in `functional-design-questions.md`
§ Assumptions & Open Questions; if per-unit numbering was intended, say so at the
gate and the artifacts will restart at R-01.

## Sources

- `../../../inception/requirements-analysis/requirements.md` — REQ-ENG-5; FR-P1-02-6; FR-P1-03-2; FR-P1-05-12; FR-P1-06-1…-4; NFR-PHASE-01; NFR-LIC-01.
- `../../../inception/units-generation/unit-of-work.md` § 2 — the `Owns` list, the boundary, BLK-06, BLK-07, and ADR-02/ADR-03.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2 plus § Per-unit coverage summary; both derivation paths agree.
- `../../../inception/application-design/component-methods.md` — the raise-contracts for every function named below.
- `../../../inception/application-design/component-dependency.md` § Shared resources — the unqualified single-path carve-out.
- `../../../inception/application-design/services.md` — § Stage entry contract, step 4, and § The nine stage scripts.
- `evidence/DECISIONS.md` **D-24** (17 protected items) and **D-15** (restricted-root relocation).
- `../foundation/functional-design/business-rules.md` — R-01's `IntegrityError` base, the two-tier posture this unit inherits, and R-15/R-16.
- `functional-design-questions.md` — **Q1 through Q9**, Q1's three owner amendments, and the Q3 reversal recorded in R-19.
- `domain-entities.md` and `business-logic-model.md` — the shapes and workflows these rules constrain.

---

## The two tiers, inherited

`foundation` R-01 fixes the hierarchy and `team.md` § Code Style fixes the posture.
Every rule below is an **integrity violation**: it terminates the run non-zero with a
message naming the resource and the violated expectation, raised as an
`IntegrityError` subclass. **No rule in this unit is a completeness shortfall.** That
is not an accident — a guard that degrades to a warning is not a guard.

---

## R-18 — Protected-item digests are canonical, not byte-literal

**Rule (Q1 = D, as amended by the owner).** Every protected-item digest is a
**SHA-256 over a versioned canonical serialization of the parsed YAML value at the
exact granularity D-24 authorizes for that item.** D-24 uses **three** config
granularities across its 17 items, and they are not interchangeable:

| Granularity | Items | Count |
|---|---|---|
| Whole-file config hash | 12 (`configs/seeds.yaml`) | 1 |
| Config-**section** hash | 4, 7, 9, 11, 14, 16 — plus 13 as `Source + config-section hash` | 7 |
| Config-**field** hash | 5 (history window), 6 (station encoding) | 2 |

Derived, not carried from prose:
`... $5 ~ /Config-section hash/` → `4 7 9 11 14 16`; `... $5 ~ /Field hash/` → `5 6`;
item 12 is `Config hash`; item 13 is `Source + config-section hash`. The full
six-kind taxonomy covering all 17 items is `business-logic-model.md` § W-3a.

**Constraint — every protected item has an explicit canonical YAML path and an
asserted key inventory** (owner amendment 1). A **mechanical completeness test**
reconciles that inventory against the parsed governed region, so that **adding,
deleting or renaming a governed key cannot leave it silently unprotected.**

**Constraint — the canonicalisation contract is stated, not left to the
implementer** (owner amendment 2). The canonicaliser identifier and version are
recorded in the transition manifest, and the contract defines:

- mapping-key ordering;
- sequence-order treatment;
- scalar typing and normalization;
- Unicode and encoding;
- duplicate-key **rejection**;
- alias and merge-key handling;
- rejection of unsupported or ambiguous values.

**Required behaviour, both directions.** Comments, whitespace, quote style,
mapping-key order and **workspace relocation** must **not** change a digest —
`foundation` R-16 already forbids machine paths in any governed config, so a
relocation that moved a hash would be a defect here. A governed **value** change
**must** change the digest.

**Constraint — overlap is declared, not forbidden outright** (owner amendment 3,
which modifies the option as recommended). **Undeclared overlap is rejected.**
**Explicit parent-section / child-field overlap is permitted** where D-24
intentionally protects both a section and a field inside it — items 5 and 9 are the
live case, both in `configs/experiment.yaml`. **Every permitted overlap is declared
and tested**, so a change cannot be hidden inside a parent's digest or ambiguously
attributed between the two.

**Constraint — item 13's composition is domain-separated** (owner amendment 4). Its
source hash and config-section hash are computed **independently** and combined using
a **versioned, domain-separated representation** — not concatenated raw, where a
boundary shift between the two halves could produce a colliding pair.

**Constraint — item 12 keeps its approved whole-file semantics** (owner amendment 5,
a raise-don't-assume constraint). If applying semantic YAML canonicalisation to the
whole-file hash would change D-24's meaning, that is **raised as a governed
amendment** — never assumed, and never resolved by the implementer's convenience.

**Constraint — boundaries are stated per item here and verified mechanically.** The
section and field boundaries for all 17 items are stated in this file (§ Per-item
boundaries below) and the complete mapping is **verified mechanically against D-24
before G-P3C**.

**Why canonical rather than byte-literal.** A byte digest changes on a comment edit,
a key reorder, a quote-style change or a trailing-whitespace fix — none of which
alters a governed value. G-P3C would fail on formatting, indistinguishably from a
real change, and a team that learns to expect spurious failures stops treating a real
one as real. Byte-literal also cannot express items 5 and 6 at all.

**Negative controls.** Reflow a comment, reorder keys, change quote style, relocate
the workspace → digest **unchanged**. Change one governed value → digest **changes**.
Add a key to a governed region but not to the inventory → the reconciliation test
**fails**. Declare no overlap where one exists → **fails**. Duplicate a key inside a
governed region → **rejected** by the canonicaliser.

**Acceptance.** TA-27 (`governance-guards`).

### R-18a — The field-hash contract (items 5 and 6)

A field hash resolves the item's **named field set** (literal names and declared
patterns), **asserts the resolved set is non-empty** — a pattern matching nothing
must fail, because a digest over zero fields would pass every diff — canonicalises
the `name → value` pairs with the **same canonicaliser** as the section path,
digests, then applies the item's own D-24 assertion:

- **Item 5, history window** (`configs/experiment.yaml`): the value is the frozen
  **24 h** *and* the field appears in **no grid**. Both limbs. The second is what
  stops the window being tuned, which `project.md` § Forbidden makes a defect. Item 5
  is also the declared parent/child overlap case against item 9 under R-18.
- **Item 6, station encoding** (`configs/features.yaml`): `station_onehot_*` plus
  `station_lat`. **D-24's word "verified" is NOT this unit's verification** — this
  unit hashes the field; whether `station_lat` is verified is
  `inventory-and-registry`'s, via `assert_registry_resolved`.

**Negative controls.** A pattern matching zero fields → **fails**. Item 5's field
present in a grid → **fails**. Item 5's value changed from 24 h → digest changes.
Item 6 with `station_lat` absent → fails the non-empty assertion.

### R-18b — The parameter-hash contract (the second half of item 15)

D-24 types item 15 as **`Source + parameter hash`** and names the parameters
verbatim: *"24-hour vector blocks, 10,000 replicates, seed 20221201."* A parameter
hash is a sibling of the field hash — same canonicaliser, named set — with two
differences:

- **Its parameters may span more than one governing artifact** (`configs/seeds.yaml`
  for the seed, bootstrap parameters for the block width and replicate count), so it
  is scoped to a **named set wherever those names resolve**, and the resolution is
  recorded.
- **Every named parameter must resolve.** A parameter hash over two of three is a
  digest that passes every diff while leaving one unprotected.

**Why it cannot be folded into the config path.** `TC-19` is `binding: hard` on
exactly these values, and `project.md` § Forbidden bars substituting a within-station
or naive bootstrap. Hashing "whatever is in the seeds file" would protect neither the
block construction nor the replicate count.

**Negative controls.** Omit any one of the three parameters → **fails** the
resolution assertion. Change the block width from 24 h, the replicate count from
10,000, or the seed from 20221201 → digest changes in each case.

### Per-item boundaries

Stated here per owner amendment 6; **every path and field name below is named by
D-24 and none is claimed to exist in the workspace today** (D-24 consequence 2 —
no config file and no `src/` package exists). The mechanical verification against
D-24 is a precondition of G-P3C, not of this stage.

| # | Granularity | Governing artifact | Boundary |
|---|---|---|---|
| 1 | Source-file content | model source | Enumerated module set, digested by content |
| 2 | Externally supplied | `models-and-baselines` | Recorded, not computed here |
| 3 | Externally supplied | `foundation` (§13.1 environment) | Recorded, not computed here |
| 4 | Config-section | `configs/features.yaml` | Named section + asserted key inventory |
| 5 | Config-**field** | `configs/experiment.yaml` | History-window field; **declared overlap with item 9** |
| 6 | Config-**field** | `configs/features.yaml` | `station_onehot_*` + `station_lat` |
| 7 | Config-section | `configs/data.yaml` | Named section + asserted key inventory |
| 8 | Externally supplied | `features-and-splits` | Recorded, not computed here |
| 9 | Config-section | `configs/experiment.yaml` | Grids section; **declared parent of item 5** |
| 10 | Externally supplied | `models-and-baselines` run record | Recorded, not computed here |
| 11 | Config-section | `configs/experiment.yaml` | Optimizer/loss policy section |
| 12 | **Whole-file config** | `configs/seeds.yaml` | Entire file; approved semantics preserved (amendment 5) |
| 13 | Source + config-section | `src/evaluation/metrics.py` + config section | **Domain-separated versioned pair** (amendment 4) |
| 14 | Config-section | `configs/experiment.yaml` | Statistical configuration section |
| 15 | Source + **parameter** | `src/evaluation/bootstrap.py` + `configs/seeds.yaml` | R-18b's named parameter set |
| 16 | Config-section | `configs/experiment.yaml` | Reporting hierarchy section |
| 17 | Source + config, **per listed method** | five listed methods | ⚠ scope **OPEN** — see `business-logic-model.md` § Open |

## R-19 — The protected-set list is excluded from every item's section hash, and that exclusion is bounded to exactly one member

**Rule (Q3 = D).** The authoritative 17-item protected-set list lives in
`configs/experiment.yaml`, under a section **excluded from every item's section
hash**. A test asserts **both** limbs: that the exclusion exists, **and** that **no
other section is excluded** — the exclusion list has **exactly one member**.

**Why the second limb carries the rule.** An unbounded exclusion mechanism is a hole,
not a resolution: whatever the first exclusion is for, the mechanism that grants it
can grant a second one silently. The membership-of-exactly-one assertion is what makes
this a named carve-out rather than an escape hatch.

**Why the list lives in a config file at all.** `project.md` § Forbidden bars hiding a
governed enumeration in source, so a literal in `phase_contract.py` is barred outright.
Parsing `evidence/DECISIONS.md` at run time makes a governance prose document a parse
target whose table formatting is not a stable interface. Both were rejected.

> ## ⚠ THIS RULE REVERSES A RECORDED OWNER REFUSAL, ON THE OWNER'S EXPLICIT DECISION
>
> The superseded ruling, preserved verbatim from the previous question set (the
> answer to its Question 3, `git show c58d9ac`):
>
> > **B, modified — MODIFY, not approval.** The project decision owner rejected the
> > recommended option D and directed the following, which governs:
> >
> > **Ordinary self-protection is not circularity.** `configs/experiment.yaml` stores
> > **only the authoritative 17 protected-item identifiers**, and the resulting
> > config-section digest is stored **externally, in the transition manifest**.
> > Changing the list therefore simply produces a new digest — **that is correct
> > behaviour and must not be described as a circularity.** …
> >
> > **The complete protected-item list is hashed.** It must **not** be excluded from
> > hashing merely to avoid circularity. Excluding it would leave the enumeration
> > that defines what is protected as the one thing unprotected.
>
> **What changed.** Nothing in the evidence: the new question set re-asked the same
> question and its recommendation repeated the same argument the owner had already
> refuted. The reversal rests on **an explicit decision by the project decision
> owner**, taken 2026-08-23 after the conflict was put to them with the superseded
> ruling quoted — not on a new argument, and `project.md` § Corrections is satisfied
> by the explicit-decision limb rather than the new-argument limb.
>
> **The superseded reasoning is not answered, and is recorded as a live cost of this
> rule:** the excluded section is the enumeration that defines what "protected"
> means, and under this rule it is the one governed region no item's section hash
> covers. R-19a below is the mitigation the owner's earlier reasoning demands, and it
> is stated as a constraint rather than left implicit.

### R-19a — The excluded section is not therefore unprotected

**Rule.** Excluded from every *item's section hash* is not the same as unhashed. The
protected-set section carries its **own digest, computed by the same canonicaliser
and stored externally in the transition manifest**, so a change to the enumeration or
to any per-item coverage list **still surfaces as a manifest difference**.

**Why this constraint is mandatory rather than optional.** Without it the reversal in
R-19 would land exactly where the superseded ruling warned: the list that defines the
protected set becomes the only unprotected thing in it. The exclusion resolves the
circularity between the list and *other items' hashes*; it must not be read as
removing the list from the freeze.

**Constraint — a change to the enumeration is a governed change.** It requires a
Vision §15.2 amendment and a D-number, so surfacing as a manifest difference is the
required behaviour, not a nuisance.

**Negative controls.** Add an item to the list → the protected-set section's own
digest changes and the manifest diff is non-empty. Change a per-item coverage list
while leaving its identifier alone → same. Exclude a second section → the
exactly-one-member test **fails**. Remove the protected-set section's own digest from
the manifest → **fails**.

**Acceptance.** TA-27.

## R-20 — The canonical contract handles every mutation of the protected set

**Rule (carried unchanged from the owner's directed table).** Each mutation below has
one required behaviour, and a test asserts it:

| Mutation | Required behaviour |
|---|---|
| **Deletion** of a protected key | Digest changes **and** the freeze-mode membership assertion fails |
| **Addition** of a key | Digest changes **and** the membership assertion fails against D-24's 17 |
| **Duplication** of a key | **Rejected.** D-24's cardinality of 17 is *calculated from the enumeration*, so a duplicate is a malformed set, not a longer one |
| **Reordering**, semantically irrelevant | Digest **unchanged** — the 17 items are a set, and R-18's canonical form sorts keys |
| **Renaming** a key | Digest changes **and** the membership assertion fails; the name *is* the identifier |
| Frozen manifest contents | **Exactly** D-24's 17-item set — no more, no fewer, no duplicates |

**Why duplication is rejected rather than tolerated.** D-24 states the cardinality is
calculated from its enumeration (14 carried forward + 3 added = 17). A set that parses
to 18 entries with one repeated does not have 18 protected items; it has a defect.
Silently deduplicating it would hide an edit nobody approved. R-18's canonicalisation
contract rejects duplicate keys, so this is enforced twice by construction.

> **Where this test gets D-24's list from is OPEN.** It must assert against the
> **authority**, not merely against the config — otherwise config and manifest can
> agree with each other while both drift from D-24. Both available routes carry a
> named cost: hardcoding is a fourth copy of a governed enumeration; parsing
> `evidence/DECISIONS.md` makes a governance prose document a test dependency, which
> Q3 option C was rejected for. **No third option is invented.** Until the owner
> directs, this test cannot be specified completely, and that is stated rather than
> papered over.

**Acceptance.** TA-27.

## R-21 — A freeze-mode manifest raises on any absent item; a draft records it

**Rule (Q2 = D).** `build_transition_manifest` records an item whose governing
artifact is absent with an explicit **`absent` sentinel**, and raises **only** when
built for a **freeze**.

**Constraint.** The **build mode** (`draft` | `freeze`) is a **field of
`TransitionManifest` itself**, not a build-time argument, so it survives
serialization and a draft can never be mistaken for a freeze by a later reader or by
`diff_protected_hashes`.

**Constraint.** A freeze-mode build **additionally asserts the key list equals D-24's
17 items** — no missing key, no extra key, and no `absent` value — so a short or
hollow list cannot pass silently, which is what `component-methods.md` already
demands.

**Why draft mode exists.** All 17 governing artifacts are absent today. Under a
raise-always rule the manifest could not be built, tested or demonstrated until the
final Bolt — and a mechanism first run at a freeze gate is a mechanism first debugged
at a freeze gate.

**Negative controls.** Freeze-build with one item absent → raises. Freeze-build with
16 keys → raises on the membership assertion. Freeze-build with 17 keys of which one
is `absent` → raises. Draft-build with all 17 absent → succeeds, and the manifest is
unmistakably marked `draft` in a serialized field.

**Acceptance.** TA-27.

## R-22 — An empty diff is not yet proof

**Rule.** `diff_protected_hashes` returning an empty mapping is the **G-P3C pass
condition**.

> **Constraint, binding now.** **BLK-06's enumeration limb is RESOLVED by D-24 at 17
> items. Its per-item binding to concrete config fields and file paths is PENDING.**
> Until that binding is discharged **and approved**, **an empty diff must not be read
> as proof that no protected item changed**, and no artifact, manifest or report
> produced by this unit may state or imply otherwise.
>
> `component-methods.md`'s standing caution is **half-discharged, not retired**. The
> three approved artifacts that still describe the enumeration as deferred to stage
> 3.1 are **reported at the gate, not edited** — see § Assumptions.

**Negative control.** A manifest whose `protected_hashes` is missing an item must fail
the membership assertion **before** any diff is computed, so a short set can never
produce a reassuring empty diff.

**Acceptance.** TA-27.

## R-23 — Both phase-boundary limbs run, and neither substitutes for the other

**Base class of every exception this unit raises** *(stated 2026-08-25, discharging the cross-unit
obligation `foundation`'s R-01 records; corrected the same day on adversarial finding 1, which was
Major — the first statement enumerated four and this unit raises **five**, omitting
`EvidenceScanError`, R-27's fail-closed December-scan limb, in the very box whose rationale is that
an unenumerated exception exits unrecorded)*: `PhaseBoundaryError`, `LockedTestError`, `ReuseError`,
`ManifestError` **and `EvidenceScanError`** all **derive from `IntegrityError`, imported from
`src/data/config.py`**, so the stage-entry contract's `except IntegrityError` catches each of them
and writes the `aborted` registry row.

**Rule (FR-P1-03-2, NFR-PHASE-01).** Two independent results are required:

- **Import limb** — `assert_phase_boundary(phase, loaded_modules)`: under
  `phase == 1`, no name in `RAW_MODULES` may be present. **Raises**
  `PhaseBoundaryError` naming the offending module.
- **Produced-field limb** — `assert_no_raw_fields(frame, phase)`: a Phase 1 artifact
  may carry **no field in D-17's excluded set** (enumerated immediately below).
  **Raises** `PhaseBoundaryError` naming the field.

> **Amended 2026-08-28 — the produced-field limb now enforces D-17's excluded set, not
> §7.0's five classes.** `GOV-2026-08-28-FD-01` **Recommendation 37** (`TEC-08`, Medium /
> `MINOR`), **board option 1**, approved by the project decision owner. As first written this
> limb enforced *"no DCB, STEC, mapping, satellite or arc field"* — faithful to TE §7.0, which
> names five classes, and **short of the set D-17 froze**. That mattered because this rule is
> the **cross-cutting** guard invoked at step 4 of every Phase 1 stage entry: it is the check
> that runs everywhere, while D-17's broader set was enforced only where each owning unit
> happens to check it. The two quantities missing were **zenith angle or zenith weight** and
> **elevation** — the two geometric inputs a mapping function is built from, and the two D-16
> names as non-computable on the five-column Phase 1 product and not to be reinstated. Derived
> 2026-08-28 by scripted match over all four of this unit's artifacts: `zenith` = **0**
> occurrences, `elevation` = **0**, `IPP` = **0**, `D-17` = **0**. The extension costs nothing
> scientifically because D-17 is frozen — no value is invented here.

**Constraint — the enumeration is D-17's, not §7.0's, and the authority citation says so.**
This limb now enforces **more than TE §7.0 states**, so its authority is
`evidence/DECISIONS.md` **D-17** § *"Explicitly NOT in the Phase 1 row, and not
substituted"* (lines 808–813) **together with** TE §7.0, and a reader must not take the
wider set for the design over-reaching its authority. **Derived 2026-08-28** by splitting
D-17's sentence on its semicolons and printing the result: **8 enumerated exclusions**, of
which **6 name a §7.0 class token** (`valid_satellite_count` and *any per-satellite or
per-IPP quantity* → satellite; DCB; STEC; *mapping function output* → mapping; *arc or
cycle-slip statistics* → arc) and **2 name no §7.0 class at all** (*zenith angle or zenith
weight*; *elevation*). Counted as distinct **quantities** rather than as string matches, §7.0's
five classes leave **3** of D-17's quantities uncovered — **per-IPP quantity** (the half of
exclusion 2 that the word "satellite" does not reach), **zenith angle or zenith weight**, and
**elevation** — and D-17 additionally makes **cycle-slip** explicit inside the arc class.

| # | D-17 exclusion (verbatim) | Named by TE §7.0? |
|---|---|---|
| 1 | `valid_satellite_count` | yes — satellite |
| 2 | any per-satellite or per-IPP quantity | **partly** — satellite yes, **per-IPP no** |
| 3 | zenith angle or zenith weight | **no** |
| 4 | elevation | **no** |
| 5 | DCB | yes |
| 6 | STEC | yes |
| 7 | mapping function output | yes — mapping |
| 8 | arc or cycle-slip statistics | yes — arc (**cycle-slip** made explicit by D-17) |

**Constraint — D-16's zenith finding is the reason exclusions 3 and 4 are not merely
tidy.** D-16 records, measured 2026-08-21, that `parameters_requested` is exactly
`["ut1_unix", "gdlat", "glon", "tec", "dtec"]` for every month and that there is *"no
elevation, no zenith angle, no satellite identifier and no per-IPP record in the Phase 1
data"* — so a zenith-weighted aggregate is **not computable** from this product, and the
sensitivity is declared and **deferred**, not silently dropped. A Phase 1 frame carrying
`zenith_angle` or `elevation` therefore cannot have been measured; it can only have been
invented, imported from Phase 2, or mislabelled — which is precisely what a boundary guard
exists to catch.

**Constraint — this aligns the design with code that already does it, correcting this
unit's own text.** Read from `tests/test_phase_boundary.py` on 2026-08-28 and counted
programmatically: `FORBIDDEN_FIELD_FRAGMENTS` already holds **13** case-insensitive
fragments — `satellite`, `n_sat`, `sat_count`, `prn`, `dcb`, `stec`, `slant`,
`mapping_function`, `arc_`, `cycle_slip`, `elevation`, `zenith`, `ipp` — covering every one
of D-17's 8 exclusions, and `D17_TARGET_FIELDS` holds the **17**-name allow-list with its own
guard (`test_forbidden_*`, line 214) asserting that no Phase 2 quantity can be added to the
contract itself. **The static early-warning limb was already stronger than the run-time limb
this rule specifies.** The amendment closes that inversion in the design's favour rather than
weakening the test, and it is why R-24's declared ordering — static subordinate, run time
authoritative — needed re-checking rather than restating: a subordinate limb must not be the
only limb enforcing three of the eight exclusions.

**Constraint — fragments, not exact names, and the reason is recorded in the code.** The
existing module states it: *"Deliberately fragments, not exact names: a column called
`n_sat_valid` or `sat_count` must trip this as surely as `valid_satellite_count`."* The
run-time limb adopts the same matching discipline, so a renamed column cannot walk past an
exact-name list.

**Constraint, quoted from the approved design.** *"Neither this nor
`assert_phase_boundary` substitutes for the other."*

**Constraint — `RAW_MODULES` is four modules**, not two: `rinex`, `calibration`,
`target`, `verification`. FR-P1-03-2's earlier wording listed two; `target.py` and
`verification.py` were added as raw-processing adapters per finding `IMPL-2`, and the
existing `tests/test_phase_boundary.py` already encodes all four.

**Constraint — the import limb runs inside the session.** It is called at step 4 of
the stage entry contract, because a Kaggle session carries no git working tree, so a
commit hook cannot fire there and a local suite run proves nothing about the
environment the governed run executes in (ADR-02).

**Negative controls — one per D-17 exclusion, plus three.** Import each of the four
modules under `--phase 1` → each raises, naming that module. Present a frame carrying a
field of **each of D-17's 8 exclusions** → **each raises, naming the field** — that is
**8** produced-field controls, not five, and the three added by this amendment are
**per-IPP quantity**, **zenith angle or zenith weight**, and **elevation**. Present a
frame carrying a **renamed** instance of an exclusion (`n_sat_valid`, `zen_wt`,
`elev_deg`) → raises, proving fragment matching rather than exact-name matching.
Present a frame whose only offending column is `cycle_slip_count` → raises, since D-17
makes cycle-slip explicit inside the arc class. Assert neither limb passing implies the
other.

**Constraint — the negative controls specified above target a module that does not yet
exist.** `assert_no_raw_fields`'s run-time controls are a **test specification only**.
`tests/test_phase_boundary.py` exists and already covers all 8 exclusions in its static
limb; the run-time controls arrive with `src/data/phase_contract.py`, whose creation
**G-09 does not authorise**. Nothing here states or implies that the three added
exclusions are covered at run time today.

**Acceptance.** TA-27; contributes to WS-10, TA-07, TA-08, TA-12 through REQ-ENG-5
(all owned by other units — `features-and-splits` ×3, `models-and-baselines`).
**Recommendation 37's closure evidence is partly deferred:** the board asks that
*"`test_phase_boundary.py`'s specification carries a negative control per class"* and
that *"a Phase 1 frame carrying `elevation` or `zenith_angle` raises
`PhaseBoundaryError`"*. The specification limb is discharged here; the raising limb is a
3.5/3.6 obligation on an unbuilt module, and the board's own due gate for this item is
**G-P3C, safe to defer past G-05**.

## R-24 — Run time is authoritative; the static scan is subordinate, and both run

**Rule (Q7 = D).** Both limbs run, with **declared roles**:

- The existing **static `ast` scan** (`tests/test_phase_boundary.py`, 266 lines,
  walking `src/` and `scripts/`) is the **early-warning limb**. It fires before
  anything executes, which is earlier than run time and worth keeping.
- The **run-time assertions** are the **authoritative limb**. `bolt-plan.md`'s
  confidence hypothesis is *"that the prohibitions are enforced at run time, not only
  in tests"*, and a static scan of a local checkout constrains nothing about a Kaggle
  session.
- `assert_no_raw_fields` is called by **each of the eight Phase 1 producing scripts
  before it writes**: `00_acquire_prepared_vtec`, `01_inventory_and_registry`,
  `02_standardize_prepared_target`, `03_verify_processing`,
  `04_build_external_products`, `05_build_features_and_splits`,
  `06_train_and_predict`, `07_evaluate_and_report`.
- A **completeness test asserts every Phase 1 producing script calls it** before its
  first write.

**Constraint — the static scan's subordinate status is recorded where the code
lives** (the Q7 rider). `tests/test_phase_boundary.py` states in its own module
docstring that it is the early-warning limb and **does not discharge FR-P1-03-2's
run-time requirement**, so a future maintainer cannot read its presence as
sufficient. Stating it only in a design document is exactly where it would be missed.

**Why not inside the release API.** That would put a Phase 1 prohibition inside
`foundation`'s release path and invert the dependency — `governance-guards` depends
on `foundation`, never the reverse, and the reverse edge would **close a cycle**.

**Why not only at the transition-manifest build.** That detects a violation after
every Phase 1 artifact is written and possibly consumed. A guard that fires at the end
is a post-mortem, not a guard.

**Why the completeness test is the rule.** A per-script obligation without it is a
list, and a new script that forgets the call is silently unchecked — the `DP-DATA-01`
failure mode. This is the **third** use of the list-plus-completeness-test shape in
this design (with R-18's key inventory and `foundation`'s `RequiredFieldsMap`), and
the repetition is deliberate.

**Negative controls.** Add a producing script that omits the call → the completeness
test fails. Delete the static scan → the run-time limb still fails a forbidden import,
and a test asserts the two results are independent. Remove the subordinate-status
docstring → a documentation test fails.

**Acceptance.** TA-27.

## R-25 — The access log is durably appended BEFORE the December read begins

**Rule (Q6 = C, with the ordering hardened on the owner's earlier direction and
carried forward unchanged).**

> **The access-log append must be DURABLY COMPLETED before the December read
> begins.** A log-write failure **or** a durability failure must **prevent the
> read** — not be reported alongside it, not be retried after it, not be logged as a
> warning while the read proceeds.

**Constraint.** `open_restricted` writes the `AccessRecord` **and flushes it** before
returning the path. **Raises** `LockedTestError` when the registry write fails — *"a
failed log write must abort the read, not proceed unlogged"* — and when `path` is not
under `RESTRICTED_ROOT`, because callers must not route ordinary reads through the
guard and dilute what a log row means.

**Why the ordering is the requirement, not a preference.** `VAL-2` and FR-P1-02-3
make log-then-read the contract: **an access recorded after the fact fails the
ordering check rather than satisfying it.** An unlogged read of the locked month is
the breach this guard exists to prevent, and it cannot be undone once taken.

**Negative controls — two, because the contract has two limbs, and both are owned by
this unit.** (1) Patch the log writer to fail → assert the read **never happens**.
(2) Assert the log row is **durable on disk** before the read is attempted,
distinguishing this contract from one that logs and reads in the same buffered
transaction, where a crash loses the row and keeps the read.

**Context that must not be lost.** The access log already holds **five retrospective
rows** predating this guard (`evidence/experiment_registry.md` records rows 3, 4, 5,
8 and 9 as retrospective). The log therefore contains two kinds of row, and the
distinction lives in the register explicitly rather than being inferred from ordering.

> ## ⚠ `RES-01` REMAINS OPEN — THE PERMITTED READ IS STILL UNTESTED
>
> Story-map Table 2 records `RES-01`: **permitted-read access logging is NOT
> TESTED**, with its candidate §19 criterion owned by **stage 3.2** under Vision
> §15.2. Q6's option D would have closed it here with a positive-path test against a
> **synthetic** restricted root, and that was declined deliberately: such a test
> would produce evidence that looks like coverage of the real pre-G-05 coverage audit
> and is not. `RES-01` is **raised at this stage's gate as still open, not absorbed
> here.**

**Acceptance.** Contributes to WS-18 and TA-18 via FR-P1-05-12 — **both owned by
`features-and-splits`**, not by this unit. ADR-03 splits the guard deliberately: the
access-log limb here, the execution limb in `splits.py`, with the test covering both
owned there to keep this unit a DAG root.

## R-26 — What counts as a December hit, and the bounded driver exclusion

**Rule (Q5 = D).** A **hit** is:

1. a **December 2022 target value** — the case the guard was written for; and
2. a **December-derived target aggregate** — a count *about* December carrying no
   target value, such as `madrigal_coverage_summary.csv`'s `december_days_present`
   and `december_coverage_pct` columns.

**Constraint — case 2 is the channel that matters most.** `project.md` § Forbidden
bars December from informing model selection, feature selection, thresholds or
hyperparameters, with the trigger being December being **seen**, not the lock being
opened. A December coverage figure sitting in an unrestricted summary is December
being seen without an access-log row.

**Constraint — December-dated *driver* captures are excluded, by a recorded and
tested exclusion.** The live instance is
`evidence/audit_ec1_2026-08-15/kyoto_dst/dst_provisional_202212.html` — hourly Dst for
December 2022, a record whose observation date falls in December and which is not a
target value. The exclusion **names the driver classes and states why**: Dst is
diagnostic/hindcast-only and never a confirmatory ML feature (`project.md`
§ Mandated; TC-11), so sweeping it into locked-test custody would route every
ordinary Dst read through `open_restricted` and buy nothing the lock exists for.

**Constraint — the exclusion is pinned to exactly that set.** A test asserts the
driver-exclusion list's membership. This is the limb that makes the rule
enforceable in the direction that matters: **a target file mislabelled as a driver is
detectable**, because the exclusion is an enumerated list a reviewer checks rather
than an unstated omission.

> **Amended 2026-08-28 — the driver-exclusion list is now actually enumerated, at four
> classes.** Consequence of `GOV-2026-08-28-FD-01` **Recommendation 44(b)** (`VAL-08`,
> Medium / `MINOR`), **board option 2**, approved by the project decision owner: relocating
> `.dst_summary.json` under `evidence/` brings a December-bearing **driver-derived** file
> **inside** R-27's scan root, so the exclusion that keeps it from being a hit must name its
> class rather than be reached by silence. Auditing the scan root for that amendment surfaced
> **two further December-bearing driver artifacts already present and never enumerated** —
> stated as a new observation, not carried from the board's report, which named neither.
> As written, the rule *said* it "names the driver classes" while the artifacts named **one
> live instance and no class list at all**: the enumerated-membership test had nothing to
> range over.

**Constraint — the four excluded driver classes, enumerated exhaustively.** Derived
2026-08-28 by walking `evidence/` and reading each candidate's December content
programmatically; every figure below was printed before being written here.

| # | Excluded driver class | Path | December content measured 2026-08-28 |
|---|---|---|---|
| 1 | Raw provisional-Dst monthly capture | `evidence/audit_ec1_2026-08-15/kyoto_dst/dst_provisional_YYYYMM.html` | **12** monthly captures present; `dst_provisional_202212.html` is hourly Dst for December 2022 |
| 2 | Raw F10.7 flux table | `evidence/audit_ec1_2026-08-15/nrcan_f107/fluxtable.txt` | **95** lines dated `202212`; the EC-1 report records the 2022 range as `2022-01-01` → **`2022-12-31`** |
| 3 | Derived driver audit report | `evidence/audit_ec1_2026-08-15/ec1-audit-report.json` | month-keyed `1`…`12`, **12** keys, the `"12"` entry carrying `expected_days: 31`, `day_rows_parsed: 31` |
| 4 | Derived driver summary | `.dst_summary.json` — **class 4 applies only once Recommendation 44(b)'s relocation has happened** ⚠ **NOW UNCONDITIONAL (2026-08-28, D-30)** — the relocation has happened, so class 4 applies without condition.; see R-27 | **12** month keys; `"12"` carries `days_parsed: 31`, `hours: 744`, `min: -68`, `storm50: [7, 27]`, `storm30` with **15** days, `daily_min` with **31** entries |

**Why classes 2 and 3 are a correction and not a widening.** Both files are inside R-27's
scan root today and both carry December-dated driver records, so a guard implemented from
the previous text would have **failed on first run against evidence already on disk** — and
the failure would have looked like a breach rather than an unenumerated exclusion. Naming
them makes the guard runnable and keeps the enumeration checkable; it grants no new licence,
because every one of the four remains a **driver** artifact carrying no target value.

**Constraint — the exclusion is a custody exclusion and never a licence to use the
excluded file.** This must not be read as making an excluded driver artifact fit for a
freeze-set input. **D-11** bars any provisional-Dst-derived figure from becoming a G-05
regime count, a modelling input, or a frozen tolerance, and that restriction rides classes
1, 3 and 4 wherever they go. The control that closes that channel is **not** in this unit:
it is `regimes-diagnostics-reporting` **R-123**, whose `RegimeError` fires when a
provisional-Dst-derived series is offered as the storm-count input, and which names
`.dst_summary.json` as exactly the path of least resistance it closes. *(Rule ID corrected
here: the remediation brief and `GOV-2026-08-28-FD-01` Recommendation 44 both cite this as
"R-122". Derived 2026-08-28 by grepping both units' rule headings — `statistical-inference`
runs R-113…R-122 and `regimes-diagnostics-reporting` opens at **R-123**, which is the rule
carrying the `.dst_summary.json` control at that unit's `business-rules.md:84`.)*

**The tension this rule resolves, stated rather than smoothed over.** FR-P1-02-6's
first sentence says *"Any file containing a December 2022 target value is a
locked-test artifact"* while its criterion says *"a record whose observation date
falls in December 2022."* Those two sentences do not pick out the same set, and the
driver capture is the difference. The owner's earlier direction on the previous
question set said *"content scan on observation dates"*, which reads toward the
literal criterion; the owner was shown that tension on 2026-08-23 and **confirmed the
narrower target-plus-aggregate reading with the bounded driver exclusion.**

**Negative controls.** Plant a December target record outside the restricted root →
hit. Plant a December-derived aggregate column outside the restricted root → hit. Add
a class to the driver-exclusion list → the membership test fails. **Remove** a class from
it → the membership test fails, so the list cannot be quietly narrowed either. Mislabel a
target file as a driver class → fails, because the excluded classes are enumerated and the
file does not belong to one. **Offer any of the four excluded classes as a G-05 regime-count
input** → `RegimeError`, owned by `regimes-diagnostics-reporting` R-123, not by this rule —
named here so the exclusion is never read as clearing the file for use.

**Acceptance.** ⚠ None — see R-27's box. This rule shares FR-P1-02-6's missing
acceptance row.

## R-27 — The guard walks every file, dispatched per artifact class, and an unparseable file is a failure

**Rule (Q4 = C).** `assert_no_december_outside_restricted` walks `evidence/`
**recursively** and opens **every file**, dispatching each to a **declared parser for
its artifact class**. An empty returned sequence is the pass condition.

> **Amended 2026-08-28 — the scan root is now stated explicitly, and it stays at
> `evidence/`.** `GOV-2026-08-28-FD-01` **Recommendation 44(b)** (`VAL-08`, Medium /
> `MINOR`), **board option 2**, approved by the project decision owner. The rule always
> walked `evidence/`; what it never did was **say so as a bounded scan root**, so the reader
> could not see what the guard cannot reach. It cannot reach the **repository root**, and one
> December-bearing artifact sits there.

**Constraint — the scan root is `evidence/`, stated as a boundary rather than left as an
implementation detail.** `assert_no_december_outside_restricted` takes `evidence_root` and
is called with the repository's `evidence/` directory. **Everything outside `evidence/` is
outside this guard by construction**, including the repository root, `src/`, `scripts/`,
`notebooks/`, `artifacts/`, `configs/` and `tests/`. That is a deliberate bound, not an
oversight, and it is written here so a future reader does not mistake "walks recursively" for
"walks everything".

**Constraint — the live instance, and why it is NOT a breach.** `.dst_summary.json` sits at
the **repository root**, is **git-tracked and not gitignored** (both verified 2026-08-28 by
`git ls-files` and `git check-ignore`), and carries December material: month keys `1`…`12`
(**12** keys), the `"12"` entry holding `days_parsed: 31`, `hours: 744`, `min: -68`,
`storm50: [7, 27]`, `storm30` with **15** days, and `daily_min` with **31** entries — every
figure derived and printed 2026-08-28 before being written here. **This design does not call
it a breach, and neither did the board.** Its classification is already correct and
**reasoned** at `evidence/experiment_registry.md:119–123`: reading Kyoto provisional Dst for
December 2022 is *"not a locked-test access: Dst is a public driver series, not a target
value, and no December target record is touched by it"*, and **D-11** separately bars any
provisional-Dst figure from becoming a G-05 regime count. The gap is narrower and purely
mechanical: **the designed guard cannot reach the file its class belongs to.** ⚠ **PERFORMED 2026-08-28 under D-30 — this paragraph describes the state BEFORE the move.** The relocation the board recommended and this design declined to perform was authorised by the project owner on `GOV-2026-08-28-FD-01` Rec 44(b) and executed the same day: `.dst_summary.json` now lives at `evidence/audit_ec1_2026-08-15/kyoto_dst/.dst_summary.json`, **inside R-27s scan root**, verified byte-identical across the move (`sha256 410927a4ff620b6f7597b18e07746f74233cf5aa87bc84d6f5b0ec25b3e9c064`, 5,653 bytes, before and after) on the D-15 method, with **access-log row 12 written BEFORE the read**. Its D-number is **D-30** and its change record is `governance/CHANGE_RECORD_2026-08-28_dst_summary_relocation.md`. **The reasoning above stands unchanged** — the file was never a breach, the gap was mechanical, and relocation rather than a widened scan root was the right fix.

**Constraint — the fix is relocation, not a widened scan root, and this design does NOT
perform it.** The recorded disposition is that `.dst_summary.json` be **relocated under
`evidence/audit_ec1_2026-08-15/kyoto_dst/`**, beside the twelve `dst_provisional_YYYYMM.html`
captures it derives from (all twelve verified present 2026-08-28), so it falls inside the
existing scan root **without widening it**, and so the derived summary sits next to its
source. Two things follow and are stated rather than assumed:

1. **The relocation is a custody-adjacent move and owes its own record** — a D-number and a
   change record under `governance/CHANGE_RECORD_PROCEDURE.md`, on the D-15 precedent, which
   is the only relocation of December-bearing material this project has performed. **This
   stage does not perform the move, does not author that record, and claims no closure from
   it.** Until it happens, the file remains outside the guard and this constraint is the
   disclosure of that fact.
2. **Once relocated it lands inside the scan root, where R-26's enumerated driver exclusion
   must already name its class** — which is why R-26 now enumerates **four** classes with the
   derived summary as class 4. Without that enumeration the relocation would convert a
   file the guard cannot see into a file the guard **flags**, and the exclusion would then be
   reached by an unstated omission rather than by a checkable list.

**Constraint — why the scan root is not widened to the repository (board option 1,
declined).** An exclusion list spanning `.claude/`, `graphify-out/`, `.git/` and any Bolt
worktree is *"the kind of list that rots"*, and it makes the guard slow at the same time.
The counter-consideration is recorded rather than suppressed, because it is this rule's own
argument turned against it: leaving the repository root permanently out of scope (board
option 3) reproduces the **`DATA-01`** lesson this rule already quotes against itself in its
§ *recursive by construction* constraint — *"a narrowed glob silently stopped checking the
artifacts that matter most."* **Relocation is the answer
to that objection**: it removes the live instance from the unscanned region instead of
declaring the unscanned region acceptable. A **future** root-level December artifact is still
outside the guard, and that residual is real and is not closed here.

**Constraint — the loose December artifact is now manifested, which repairs the other half
of `VAL-08`.** `evidence/locked_test_restricted/loose_artifacts_sha256_manifest.json` was
created **2026-08-28** under **Recommendation 44(a)**, on the project decision owner's
authorisation, hashing run 2's preserved raw extract
(`bbox___opt_openmadrigal_madroot_experiments4_2022_gps_31dec22_gps221231g.003.hdf5.txt`):
`sha256 3a164af0864b2effde2e527ca190c1b050f5a47179eaffa3ccab770bb366f557`, **1,666,816
bytes** — both **re-derived independently 2026-08-28** by streaming the file and recomputing
the digest, and both matching the manifest exactly. The manifest also records the provider
filename with its **`g.003` version suffix**, the retrieval timestamp, and the DATA-07
provenance caveat. Access-log **row 11** was written **before** the read, as FR-P1-02-3
requires and as rows 6 and 7 set the standard. Two properties of that act matter to this
rule's integrity story: the file was previously named in **neither** restricted
`sha256_manifest.json`, so a mutation of the one physical record of the run-2 irregularity
would have been undetectable and TA-15's mutation-protection test — which operates on
manifested artifacts — had nothing to bind to; and the read was **bytes-only for hashing**,
with no field parsed, no record counted and no value inspected, so it produced no coverage
figure this guard would then have to police. **This unit did not perform that act and
records it as an input**, not as its own closure.

**Constraint — an unparseable artifact is a FAILURE, not a pass.** A file the guard
cannot read is exactly where a December record would hide, so treating it as clean is
the one answer that cannot be defended. Getting past a genuinely irrelevant
unparseable file requires an **explicit recorded exclusion**, never silence.

**Constraint — identification is by record date, never by filename or directory
name.** `project.md` § Forbidden: *"NEVER derive fold or partition membership from an
acquisition directory name or a filename."* That rule exists because a year-blind
predicate filed locked-month records into `audit_evidence_2022-01/`, where a
name-based check cannot see them.

**Constraint — recursive by construction**, because `DATA-01` showed a narrowed glob
*"silently stopped checking the artifacts that matter most."*

**What the existing green check actually covers, and why this rule widens it.**
`tests/test_acquisition_window.py` sets `RAW_RECORDS = "madrigal_coverage_raw_records.csv"`
and its `_record_csvs_at_any_depth()` helper returns `EVIDENCE_DIR.rglob(RAW_RECORDS)`
minus the restricted root — **one filename, not a content class.** Inventory of
`evidence/` by filename shows 16 instances each of `madrigal_coverage_raw_records.csv`,
`madrigal_coverage_summary.csv`, `madrigal_coverage_monthly.csv`,
`sha256_manifest.json` and `request_manifest.json`; only the first is scanned. Scanned
2026-08-22, every non-zero `december_*` value in the summary CSVs is already under the
restricted root — so **the check is green and the gap is latent, not currently
breached.** A December-bearing `madrigal_coverage_summary.csv` appearing outside the
restricted root tomorrow would pass.

**Constraint — no artifact-class registry is frozen by this stage.** Q4's option D
would additionally assert a declared registry covering every filename present under
`evidence/`. It was declined **with a reason, not by omission**: it would front-load a
registry before any of the artifact classes it enumerates is produced by this
pipeline, and the current 16-instance inventory is all pre-TC-06 evidence.
**Failure-on-unknown gives the same protection**, arriving as a failure the first time
a new class appears rather than as a design-time list. Adding the registry later is
not foreclosed.

**Negative controls.** Plant a December record inside a non-December-named directory →
the guard finds it. Plant an unparseable file → the guard **fails**. Plant a
December-bearing artifact of a class with no declared parser → **fails**. Run against
the post-D-15 tree → assert the 21 relocated files are inside the restricted root and
none is outside it. **Plant a December-bearing artifact at the repository root** → the
guard **does not find it, and a test asserts that it does not** — the scan root's bound
made executable, so the residual is a recorded property rather than a surprise, and the
test fails the day someone silently widens or narrows `evidence_root`. **Call the guard with
an `evidence_root` other than `evidence/`** → fails, so the bound cannot be relaxed by a
call site.

> ## ⚠ FR-P1-02-6 IS EXPLICITLY UNTESTED, AND STAYS THAT WAY
>
> **This rule's requirement has NO §16 or §19 acceptance row** — derived from
> story-map Table 1 and cross-checked against § Per-unit coverage summary. It is this
> unit's one untested requirement of ten. It **is** enforced today, by
> `tests/test_acquisition_window.py::test_locked_month_values_exist_only_under_the_restricted_path`,
> and that test **is** currently green — lacking an acceptance row is a different
> thing from lacking a test, and R-26 and R-27 both narrow or widen what that green
> means.
>
> On the project decision owner's explicit direction, FR-P1-02-6 is preserved as an
> **explicitly untested obligation until an approved acceptance row exists AND its
> test has passed** — both conditions, not either.
>
> Everything above is a **test specification only — not an approved acceptance row and
> not evidence of a passing result.** Designing the guard does not test it.
> Implementing it does not test it. **No artifact, manifest or report may state or
> imply that FR-P1-02-6 is covered, satisfied or verified.**

## R-28 — One path into the restricted root, and BLK-07 is not this design's to close

**Rule (Q9 = D, as narrowed 2026-08-28).** A **static check asserts that no module
outside `locked_test.py` and outside the enumerated `tests/` exemption below contains the
restricted-root literal**, and that the exemption list's membership is **exactly** the ~~four~~
⛔ **five** modules named *(corrected 2026-08-31 on owner approval to annotate in place; superseded
figure preserved. **Five** members in addition to the chokepoint — **six** counting
`locked_test.py`, the convention this rule's own 2026-08-29 box below already uses. The fifth is
`scripts/merge_coverage_year.py`, a **production script, not a test**. This Rule statement was
missed by the 2026-08-29 repair, which swept only the five sites its finding enumerated while
this rule's own box twenty lines below already carried the corrected six — `project.md`
`fd-2026-08-30-sweep-derive-sites`)*. `open_restricted` remains the **only** path through which
restricted **content** is read from `evidence/locked_test_restricted/`.

**Authority, and how the narrowing is reconciled with it.**
`component-dependency.md` § Shared resources states the rule **without qualification**:
*"nothing else may construct a path into it."* `foundation`'s **R-15** states its own side of
that as the absence of a path. The exemption below **does not contradict that sentence; it
fixes its referent.** A test module that holds the literal in order to assert *where the
boundary is* does not "construct a path into" the root in the sense the carve-out protects —
it constructs a path **to check custody**, and where it goes on to read content, the
exemption requires that read to run through `open_restricted` or against a synthetic fixture
root. **The reading taken is that "a path into it" means a route by which restricted content
is obtained**, and that reading is stated here as an assumption rather than assumed silently,
because it is the load-bearing move of this whole amendment. **If the project decision owner
reads the carve-out as governing the literal itself**, the exemption is not available and
board option 2 — refactor every test to obtain the root from `locked_test.py` — is the only
remaining route, with the circularity recorded in row 1 accepted along with it. Raised at the
gate on those terms.

> ## ⚠ A SIXTH HOLDER, FOUND 2026-08-28 BY THE FULL-SCOPE SWEEP — **`scripts/merge_coverage_year.py`**
>
> *(Found on the project decision owners 2026-08-28 instruction to sweep the full repository
> scope rather than assume the boards two sites were the only ones. The
> `GOV-2026-08-28-FD-01` board named **three** test modules; this is a **fourth** file and
> **not a test at all**.)*
>
> `scripts/merge_coverage_year.py` holds the restricted-root literal at its line 55, defines
> `EVIDENCE_ROOTS = (EVIDENCE_DIR, RESTRICTED_DIR)`, **writes** the merged year into the
> restricted root, and **read six restricted content sites with no `AccessRecord`**: the
> per-month `sha256_manifest.json`, the raw records CSV, two `request_manifest.json` reads,
> and two `sha256_of_file` calls.
>
> **This is more serious than the three test modules, and the rule as written did not reach
> it.** R-28s exemption is a **`tests/` exemption**. A production script is outside it
> entirely, so this file was not an exempted holder — it was an **unexempted** one, and the
> static check as specified would have failed against it on first run. The one-door property
> was broken by a production path, not only by test scaffolding.
>
> **Corrected the same day under D-31** (which signed G-09 and authorised editing the file):
> all six reads now route through `src.data.locked_test.open_restricted`, which writes a
> durable `AccessRecord` before returning the path and **aborts the read if the log write
> fails**. The script is added to the enumerated exemption **explicitly** — an exemption a
> reader cannot see is not an exemption, it is a hole — bringing the list to **six**: the
> chokepoint itself, four `tests/` modules, and this one production script whose restricted
> access is legitimate under **D-18** (the year re-merge).
>
> **The exemption is therefore no longer `tests/`-only, and R-28s rule text above is
> narrowed accordingly**: membership is an **exact enumerated list**, not a directory
> predicate. That is a widening of *what may be listed* and a **narrowing of how membership
> is decided** — a substring or prefix exemption remains expressly refused, and
> `tests/test_locked_test_guard.py` asserts exact set membership so a seventh holder
> **fails** rather than being silently admitted.
>
> ⚠ **The guard test is written but has NOT been executed.** No Python interpreter exists in
> this environment (a zero-byte Windows Store stub; no registry entry; no interpreter on
> disk), so every claim above about runtime behaviour is **a claim about code as written,
> not a passing test result**. WS-18 and TA-18 are **not** discharged.


> ## ✳ THE READING IS RULED, 2026-08-28 — THE EXEMPTION STANDS
>
> The project decision owner ruled at the `functional-design` gate that **"a path into it" means a route by which restricted CONTENT is obtained**, which is the reading this rule stated as its load-bearing assumption and raised rather than assumed. **The enumerated `tests/` exemption is therefore available and is now the rules settled form**, and board option 2 — refactoring every test to obtain the root from `locked_test.py`, with the row-1 circularity that entails — is **not** taken.
>
> **What the ruling does NOT relax.** The exemption is **exhaustive and exact**: ~~the three named modules and `locked_test.py`, no fourth~~ ⛔ **SUPERSEDED 2026-08-31 as to the membership only — the 2026-08-29 full-repository sweep found a fifth member, `scripts/merge_coverage_year.py`, so the list is the four `tests/` modules plus that production script, with `locked_test.py` the chokepoint: six counting it. The ruling's substance is untouched — the list stays exhaustive and exact, and "no fourth" becomes "no seventh"** *(annotated in place on owner approval; the dated ruling text is preserved because it records what was ruled on 2026-08-28, before the fifth member was known)*. Any *content* read beneath the restricted root by an exempt module still runs through **`open_restricted`** or against a **synthetic fixture root** — the exemption covers holding the **literal**, never obtaining the **content**. A substring or prefix exemption is expressly refused; the static check asserts **exact list membership**, so a new module holding the literal **fails** rather than being silently admitted.
>
> **The live breach this leaves, stated and not smoothed over.** Two of the three exempt modules read content beneath the root **today** with **no `AccessRecord`** — `tests/test_release_hashes.py:137` and `tests/test_acquisition_window.py:195`. That is `evidence/experiment_registry.md:79-83`s recorded RES-04 hazard *"occurring in fact rather than in principle"*. **The ruling does not cure it**; it fixes which mechanism must cure it. Routing those two reads through `open_restricted` is **owed at stage 3.5** and is a precondition of this rules negative control passing honestly, and G-09 is unsigned so neither module may be edited yet.


> ## ⚠ AMENDED 2026-08-28 — THE ONE-DOOR RULE NOW CARRIES A BOUNDED `tests/` EXEMPTION
>
> `GOV-2026-08-28-FD-01` **Recommendation 2** — the board's **BLOCKER**, finding `VAL-02`,
> on which the **Validation Auditor exercised its veto**. **Board option 1**, approved by the
> project decision owner. This is a **narrowing stated in the open**, not a concession
> smuggled in, and the honest version of the concession is the first sentence of it: **more
> than one module holds the literal, and the rule as first written was false against the
> workspace this unit had already read.**
>
> **What was wrong.** The rule's pass condition was that exactly **one** module holds the
> restricted-root literal. **Four hold it today** — three existing test modules plus the
> future `locked_test.py` — so the design's own negative control was **satisfied by the
> workspace as it stands**. Verified on disk 2026-08-28: `tests/test_acquisition_window.py:46`,
> `tests/test_phase_boundary.py:49` and `tests/test_release_hashes.py:49` each define
> `RESTRICTED_DIR = EVIDENCE_DIR / "locked_test_restricted"`.
>
> **How this unit missed it, stated exactly.** Of the three violating modules, **two were read
> directly** — `test_phase_boundary.py` and `test_acquisition_window.py`, per
> `business-logic-model.md` § Sources — and one of those two had its internals **quoted in
> detail** in R-27's *"what the existing green check actually covers"* paragraph. **The third,
> `tests/test_release_hashes.py`, was never read at all.** So the failure was not a
> misreading of evidence in hand; it was a rule stated over the **whole tree** while the source
> register recorded an inspection of **two of the tree's three** modules. The 2026-08-28
> source line now records all three, and this is the lesson worth keeping: a rule whose pass
> condition ranges over every module owes an inspection that ranges over every module.
>
> **Why it had to be fixed rather than left.** Both outcomes of leaving it were bad and
> nothing chose between them. Implemented as written, the static check **fails against the
> project's own custody tests** and gets relaxed under schedule pressure — most likely to a
> substring exemption broad enough to re-admit arbitrary callers. Implemented with an
> *undeclared* `tests/` exemption, test modules read December bytes with no `AccessRecord`,
> which is the **RES-04** hazard `evidence/experiment_registry.md:79–83` already records as
> *"BLK-07's registered hazard occurring in fact rather than in principle."*
>
> **Board option 3 was rejected by name.** Scoping the check to `src/` only and leaving
> `tests/` out of scope is trivially implementable and *"is what will be chosen by default if
> nothing is decided"* — and it **converts the largest known hole into a permanent blind
> spot.** `evidence/experiment_registry.md:79–83` records that same hazard having already
> fired once in fact, which is why it is refused here rather than weighed again.

**Why the boundary is still absolute where it counts.** **D-15** records that the restricted
root is a **governance boundary, not an access control** — it holds only while exactly one
code path reaches it. **That sentence is retained verbatim, and its scope is now stated
rather than left to inference: a "path" is a route through which restricted CONTENT is
read.** D-15's boundary *"does not weaken slightly; it ends"*, and the exemption below is
built so that nothing about that sentence changes: an exempt module may **name** the root, but
if it **reads content beneath** it, the read goes through `open_restricted` or against a
synthetic fixture root. Holding a string is not an access; reading bytes is.

**Constraint — the exemption is enumerated exhaustively, and membership is asserted
exactly.** This is the **same enumerated-list technique R-26 already uses** for the driver
exclusion — a technique this design already trusts, and which fails in the direction that
matters: an unlisted module holding the literal fails the static check, and a listed module
that stops needing the literal fails the membership test until the list is edited. The list
is **4 modules** (derived and printed 2026-08-28; **3 of the 4 exist on disk today**, the
fourth being unbuilt):

| # | Exempt module | Why it must hold the literal | Route for any CONTENT read beneath the root | On disk today |
|---|---|---|---|---|
| 1 | `tests/test_locked_test_guard.py` | It is the test **of the guard**. Obtaining the root by importing `locked_test.py` — board option 2 — is **circular**: the module under test would supply the constant the test exists to check, and an imported constant still yields a readable path with no `AccessRecord`, so the custody gain is cosmetic | **Synthetic fixture root only.** It never reads the real restricted root. This is consistent with Q6's option D having been **declined**: a positive-path read against the real root would produce evidence that looks like coverage of the pre-G-05 audit and is not, which is exactly why `RES-01` stays open | **No** — unbuilt; owned by `features-and-splits` (R-82) |
| 2 | `tests/test_acquisition_window.py` | `RESTRICTED_DIR` (:46) feeds `EVIDENCE_ROOTS` (:50) so the run-window invariant covers **both** roots, and the custody helper (:195) filters restricted paths out **by ancestry rather than by name**, so a rename of the root cannot silently widen the scan | `_observed_dates()` (:117–122) **opens and `DictReader`-parses** a month's `madrigal_coverage_raw_records.csv`, and `_month_dirs()` (:81) supplies month directories from the restricted root — so this **is** a content read of December's raw records and **owes a pre-read access row** under RES-04. The :195 helper reads nothing beneath the root and owes no route | **Yes** |
| 3 | `tests/test_phase_boundary.py` | :259–261 asserts the produced-field collector **reaches inside** the restricted root — *"a custody boundary is not a checking exemption"*, in the module's own words. Removing the literal would remove that assertion, which is the one guarding against D-15's relocation quietly excusing December from boundary checking | `_phase1_artifacts()` (:133–137) rglobs `madrigal_coverage_*.csv` across **both** roots and the parametrized field test reads each artifact's **CSV header** — a content read beneath the root, **owing a pre-read access row**. The :259–261 ancestry assertion itself reads no content | **Yes** |
| 4 | `tests/test_release_hashes.py` | :137 asserts a manifest was found **under** the restricted root, because *"after D-15 the December and merged-year manifests live there, and a collector that misses them silently stops verifying the locked month"* | `_declared_artifacts()` (:84–91) `read_text`s each manifest and `test_declared_artifact_matches_its_recorded_hash` **streams `_sha256()`** over each declared artifact, both beneath the root — content and byte reads, **owing pre-read access rows**. Access-log rows 6 and 11 set the precedent that a **bytes-only hash read** is logged before the read and inspects no value | **Yes** |

**Constraint — an exempt module that reads content still owes a pre-read access row.** The
exemption composes with the **already-registered RES-04 obligation** and does not displace
it: exemption from the *literal* check is **not** exemption from R-25's ordering rule. Any
read of content beneath the restricted root by an exempt module is a December read, so the
`AccessRecord` must be **durably appended before the read begins**, exactly as R-25 requires
of every other caller. An exempt module that reads content without a prior durable row is a
**failure**, and the control below makes that executable.

> ## ⚠ A LIVE CONSEQUENCE THAT NEEDS AN OWNER RULING, STATED NOT RESOLVED
>
> Modules 2, 3 and 4 **read December content beneath the restricted root today, on every
> suite run, with no access row** — because `open_restricted` does not exist (**G-09 is
> unsigned**) and there is nothing to route through. That is not a hypothetical: it is the
> RES-04 hazard in present tense, and this amendment surfaces it rather than creating it.
> **Nothing here authorises those reads, retro-labels them, or writes a row for them.** Two
> dispositions are available and **this design chooses neither** — the choice belongs to the
> project decision owner:
>
> - **(i)** route each of the three modules' restricted-root content reads to **synthetic
>   fixture roots**, leaving the real root read only through `open_restricted` once it
>   exists; or
> - **(ii)** keep the reads against the real root and record the standing obligation that
>   each is owed an access row from the moment `open_restricted` exists, with the interim
>   period disclosed in the G-05 and G-06 evidence packages alongside the five retrospective
>   rows R-25 already names.
>
> Option (i) is what module 1's route already assumes and is the cheaper of the two to make
> true; option (ii) preserves the three modules' present value as checks against **real**
> evidence, which is what makes them worth exempting at all. **Raised at this stage's gate.**

**Constraint — `test_locked_test_guard.py`'s route answers a question `features-and-splits`
left open.** R-82 assigns that module to `features-and-splits` *"because it exercises **both**
limbs"* and says nothing about how it reaches the restricted root without holding the literal.
**Row 1 above is that answer**: it holds the literal under this exemption and reads only a
synthetic root. The alternative — importing the root from `locked_test.py` — is the circularity
rejected above. The module's **ownership does not move**; only its route is fixed here, and
`governance-guards` remains a DAG root because an exemption-list entry is a name in this unit's
static check, not a dependency edge on `features-and-splits`.

**Why not a caller allow-list inside the guard.** Q9's option C would have
`open_restricted` raise when its caller is not one of the four recorded consumers. That
closes the run-time-path-assembly gap but couples this root unit to four downstream units,
and the reverse edge would **close a cycle** the DAG was arranged to avoid. The residual gap
— a path assembled at run time from fragments — is left open deliberately, because the
static check plus review makes it unlikely and the acyclic structure is worth more.

**Why not a caller allow-list inside the guard.** Q9's option C would have
`open_restricted` raise when its caller is not one of the four recorded consumers.
That closes the run-time-path-assembly gap but couples this root unit to four
downstream units, and the reverse edge would **close a cycle** the DAG was arranged to
avoid. The residual gap — a path assembled at run time from fragments — is left open
deliberately, because the static check plus review makes it unlikely and the acyclic
structure is worth more.

**Negative controls — five, because the narrowed rule has more limbs than the absolute
one did.** (1) Add the restricted-root literal to a module **not** on the exemption list →
the static check **fails**. (2) **Add a module to the exemption list** → the **membership
test fails**, so the list cannot grow silently and every addition is a reviewed edit — the
board's named closure control. (3) **Remove** a module from the list while it still holds
the literal → the static check fails, so the list cannot be narrowed into falsehood either.
(4) Have an exempt module read content beneath the restricted root **without** a durable
prior access row → **fails**, which is the limb that keeps the exemption from becoming the
RES-04 hazard it was granted in spite of. (5) Point `test_locked_test_guard.py` at the
**real** restricted root instead of a synthetic fixture root → **fails**, pinning module 1's
declared route.

**Constraint — every control above is a test specification only.** The static check and the
membership test do not exist; **G-09 authorises no module**, and `src/data/locked_test.py` is
unbuilt. Nothing in this rule states or implies that the exemption is enforced today. What
*is* true today is the observation that motivated the amendment: **four modules hold the
literal and no check exists to notice.**

> ## ⚠ BLK-07 IS OPEN AND STAYS OPEN — AND IS A PRECONDITION OF BOLT 3
>
> Four units reach the root through this contract: `inventory-and-registry` (pre-G-05
> coverage audit), `acquisition` (the D-9 input and any December re-acquisition — the
> unrecorded routing that **is** BLK-07), `features-and-splits` (locked partition),
> `evaluation-and-comparison` (locked evaluation).
>
> **This rule has a live consequence, stated rather than discovered later:**
> `acquisition` **cannot hold its own path** to `audit_evidence_2022-FULL/` once the
> static check exists, because that artifact now lives under the restricted root
> (D-15). **BLK-07's resolution is therefore a precondition of Bolt 3, not a
> formality.**
>
> **Acceptance of this design mechanism is NOT authorization to open locked December
> data.** Which units are authorised to reach the locked month is a decision the
> **project decision owner receives and approves**. Nothing in this unit's artifacts
> grants it, implies it, or substitutes for it — the static check enforces *how many*
> paths exist, never *who* may use one. **No acquisition run may touch calendar
> 2022-12 while BLK-07 stands.**

**Acceptance.** Contributes to TA-18 (owned by `features-and-splits`).

## R-29 — Reuse is registered before use, and reimplementation is the default

**Evidence module, named** *(2026-08-25, adversarial finding 4 of the post-reset pass:
`tests/test_reuse_registry.py` is in this unit's `Owns` and is TA-28's evidence, and appeared in
none of the three artifacts while its sibling `tests/test_phase_boundary.py` is named
throughout)*: this rule and R-30 are proven by **`tests/test_reuse_registry.py`**, which rejects a
marked adapter module with no register entry and an entry missing any of the fifteen fields.

**Rule (NFR-LIC-01, §10.1, Q8 = D).** Any reused or materially adapted third-party
source is recorded in the register with **all fifteen fields**, **before the code is
used** and before gate **G-P2**.

**Constraint — the register is the exception path, not the main road.** The standing
default is **reimplementation from the paper with a citation**. `project.md`
§ Forbidden prohibits copying source whose licence is absent, ambiguous or
incompatible, and that is the rule in force while the AGPLv3 question is open.
Designing the register as the expected path would misrepresent the policy actually in
force, and copying is deliberately harder to reach than reimplementation.

**Constraint — completeness is checkable.** Every adapter module carries a mandatory
**provenance marker**; the register is asserted complete against the set of marked
modules, and an unmarked module is asserted to contain **no reuse**. Without the
marker an unregistered copy is indistinguishable from original work by inspection,
and the completeness assertion has nothing to range over.

**Constraint — the open governance dependency, stated not resolved.** The AGPLv3
Global-TEC-forecasting repository is the only approved direct-copy source today, and
**whether its repository-distribution obligations permit that copying is a governance
dependency this project does not settle.**

**Negative controls.** A marked module with no register entry → fails. A register
entry missing any of the fifteen fields → fails. An unmarked module containing a
recognisable upstream fragment → fails the no-reuse assertion.

**Acceptance.** TA-28 (`governance-guards`).

---

## Rules with no acceptance row — stated, not buried

| Rule | Requirement | Status |
|---|---|---|
| R-26 — what counts as a December hit | **FR-P1-02-6** | ⚠ **No §16/§19 row.** Enforced today and green; preserved as explicitly untested until an approved row exists **and** its test has passed |
| R-27 — the recursive per-class walk | **FR-P1-02-6** | Same requirement, same missing row |

**One requirement of ten**, matching the story map's designation exactly. Two rules
implement it; the count of untested *requirements* is one.

## Assumptions & Open Questions

- **OPEN — which disposition the three existing exempt test modules take** *(added 2026-08-28 under Recommendation 2)*: options (i) synthetic fixture roots or (ii) real-root reads with a standing access-row obligation, set out in R-28's boxed live consequence. **No option is chosen here.** Until it is ruled on, `tests/test_acquisition_window.py`, `tests/test_phase_boundary.py` and `tests/test_release_hashes.py` continue to read December content beneath the restricted root with no access row, and 3.5 must stop and report rather than pick a route (TE §18.3).
- ~~**OPEN — the `.dst_summary.json` relocation is authorised in disposition but not performed**~~ *(added 2026-08-28 under Recommendation 44(b))*: the move to `evidence/audit_ec1_2026-08-15/kyoto_dst/` owes a **D-number and a change record** on the D-15 precedent, and neither exists. **This stage does not perform the move and claims no closure from it.** Until it happens the file is outside R-27's scan root, and R-26's driver-exclusion class 4 is stated as conditional on the move having happened.
- ⚠ **CLOSED 2026-08-28 — the relocation is PERFORMED.** The project owner authorised it on `GOV-2026-08-28-FD-01` Rec 44(b); it is recorded as **D-30** with change record `governance/CHANGE_RECORD_2026-08-28_dst_summary_relocation.md`, and executed the same day: the file is now at `evidence/audit_ec1_2026-08-15/kyoto_dst/.dst_summary.json`, byte-identical across the move (`sha256 410927a4ff620b6f7597b18e07746f74233cf5aa87bc84d6f5b0ec25b3e9c064`, 5,653 bytes), with **access-log row 12 written BEFORE the read**. The file is inside R-27s scan root and **R-26s driver-exclusion class 4 is now unconditional**. The two things this item said were missing — the D-number and the change record — both exist.
- **[assumption]** The exemption list is **exactly five** modules *(corrected 2026-08-29 on adversarial finding 1, Critical; superseded figure preserved: "**exactly four** modules". R-28's own box states the same set as **six** because it counts the chokepoint `src/data/locked_test.py` as well; this list counts members **in addition to** the chokepoint. Both figures describe one set.)* — `test_locked_test_guard.py`, the three `tests/` modules that hold the literal today, **and `scripts/merge_coverage_year.py`**, the production script the 2026-08-28 full-repository sweep found holding the literal and reading six restricted sites with no `AccessRecord`. The three existing test modules are **retained** rather than refactored. Retention is the reading taken because all three are green, all three are in `team.md`'s mandated 17-module set, and TC-06 directs that pre-TC-06 evidence be **re-verified under the new suite rather than re-acquired**, which those three modules are what performs. The fifth member is why the exemption is **no longer `tests/`-only** and why membership is an **exact enumerated list, never a directory predicate**. If the owner prefers refactoring any member out, the list shrinks and the membership test changes with it.
- **[assumption]** R-28's exemption is a **narrowing of D-15's framing**, not a relocation of D-15's requirement. The reading taken is that D-15's "exactly one path" governs routes through which restricted **content is read**, so holding the literal without reading content is outside it. If the owner reads D-15 as governing the literal itself, board option 2 (refactor every test to obtain the root from `locked_test.py`) is the only remaining route and the circularity recorded in R-28 row 1 has to be accepted with it.
- **OPEN — an amendment need on `build_transition_manifest`** *(added 2026-08-25 on adversarial finding 2 of the post-reset pass)*: the approved signature carries no mode parameter, three artifact statements correctly say the mode is not a build-time argument, yet the builder must be told which mode to build. The reconciliation (W-5) records an amendment need — a keyword `mode: Literal["draft","freeze"]` — for the owner, following `foundation`'s `write_release` precedent. Until ruled on, 3.5 must stop and report rather than invent the channel (TE §18.3).
- **[assumption]** Rule IDs continue `foundation`'s single sequence, so this unit opens at **R-18**. If per-unit numbering was intended, say so at the gate and the artifacts restart at R-01.
- **[assumption]** `tests/test_locked_test_guard.py` is not this unit's — ADR-03 splits the guard, and `features-and-splits` owns the test covering both limbs to keep this unit a DAG root.
- **[assumption]** `RAW_MODULES` names **four** `gnss` modules — `rinex`, `calibration`, `target`, `verification` — not the two FR-P1-03-2's earlier wording listed.
- **[assumption]** NFR-PHASE-01's transition-manifest hash-diff test has no §12 module and needs frozen artifacts from every later unit; carried on `fixtures-and-reproducibility` with this unit supporting.
- **[assumption]** TA-27's second limb (Phase 2 cannot change protected forecasting hashes) is accepted at G-P2 and G-P3C, **outside Phase 1**. Only the first limb is acceptable inside this initiative.
- **[assumption]** Whether `canonicaliser_version` is a new `TransitionManifest` field or an entry in an existing mapping is a stage 3.5 shaping decision; `build_mode` is fixed as a field by R-21. Only semantics are fixed here, so **no approved dataclass contract is otherwise changed by this stage.**
- **Open — R-19 reverses a recorded owner refusal on the owner's explicit decision.** The superseded reasoning is preserved verbatim in R-19's box and is **not answered by a new argument**; R-19a is the mitigation it demands. Raised at the gate so the reversal is visible rather than inherited.
- **Open — R-20's D-24 conformance test source.** See the boxed note in R-20. **No option invented.** Raised at the gate.
- **Open — BLK-06's per-item binding.** Enumeration resolved by D-24 at 17; the per-item binding to concrete config fields and file paths is **PENDING**. R-18's § Per-item boundaries produces the binding evidence; **BLK-06 is not closed by this stage**, per `DP-CHAIR-02`.
- **Open — BLK-07 authorization**, and it is a **precondition of Bolt 3**. See R-28. The owner's decision, not this design's.
- **Open — `RES-01`, permitted-read access logging is NOT TESTED.** See R-25's box. Owned by stage 3.2 under Vision §15.2; Q6's option D was declined deliberately rather than closed here with synthetic-root evidence.
- **Open — item 17's per-method "config hash" scope.** D-24 uses the same two words for item 12's whole-file hash and item 17's per-listed-method hash. Not invented here — see `business-logic-model.md` § Open.
- **Open — a stale statement in three approved artifacts, reported not edited.** `component-methods.md`'s `TransitionManifest` comment, `unit-of-work.md` § 2 and `components.md` line 61 all still read that the enumeration and cardinality are deferred to stage 3.1. **D-24 has since resolved the enumeration at 17 items.** Per `CHANGE_RECORD_PROCEDURE.md` a sweep reports on approved-stage artifacts and does not edit them absent owner approval for annotate-in-place. Raised at the gate.
- **Open — the AGPLv3 distribution question.** Unresolved; the standing default is reimplementation with a citation.
- **G-09 is not signed.** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged. No rule here authorises creating `phase_contract.py`, `locked_test.py` or `reuse_registry.py`.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

---

> **Re-saved 2026-08-24 under the post-redo receipt floor.** The project decision owner
> authorised a redo jump on `functional-design` at 2026-08-24T14:57:07Z so that three
> standing reviewer findings on `models-and-baselines` could be fixed and re-reviewed;
> a redo resets the receipt floor for **every** unit of the stage. **No content of this unit
> changed** — not a question, answer, amendment, rule, entity, workflow, count or scientific
> value. The only artifacts edited after the redo were `models-and-baselines`'s, whose
> three fixes are confined to its own files. That unit returned **READY** on the second pass of
> the restored budget, which is what the redo was authorised for. The two residuals riding that
> verdict — R-96's `PartitionError` mechanism and R-95's field label — are carried to the stage
> gate rather than applied, per the rule that a suggestion riding a READY verdict is gate input.

---

> **Re-saved 2026-08-25 under the post-ten-redo receipt.** One addition: the **base-class
> declaration** ahead of the phase-boundary rule — `PhaseBoundaryError`, `LockedTestError`,
> `ReuseError` and `ManifestError` all derive from **`IntegrityError`, imported from
> `src/data/config.py`** — discharging this unit's half of the cross-unit obligation
> `foundation`'s R-01 records. Without it the stage-entry contract's `except IntegrityError`
> would let a phase-boundary violation exit with **no `aborted` registry row**, against
> NFR-PHASE-01 and NFR-AUD-01, in the unit that owns the guard. No rule was added or removed;
> figures re-derived and unchanged (10 requirements, 1 untested, 2 acceptance rows).
> **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved 2026-08-25 after the post-reset iteration-1 remediation.** The base-class declaration
> was corrected to cover **all five** exceptions this unit raises — the first statement enumerated
> four and omitted `EvidenceScanError`, the fail-closed December-scan limb, in the box whose own
> rationale is that an unenumerated exception exits unrecorded (adversarial finding 1, Major).
> R-29 now names **`tests/test_reuse_registry.py`** as TA-28's evidence (finding 4), and
> § Assumptions carries the **amendment need on `build_transition_manifest`'s mode channel**
> (finding 2). No rule added or removed; figures unchanged. **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved unchanged 2026-08-25 under the second receipt** (eleventh redo, taken for
> `acquisition`; floor reset mechanical). **No content of this unit changed** since the terminal
> READY. **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved unchanged 2026-08-26 under the third receipt** (twelfth redo, taken for
> `inventory-and-registry`; floor reset mechanical). **No content of this unit changed.**
> **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved unchanged 2026-08-26 under the fourteenth-redo re-confirmation receipt** (redo taken
> for `external-products`; floor reset mechanical). **No content of this unit changed.**
> **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> ## Re-saved 2026-08-28 — remediation of `GOV-2026-08-28-FD-01`, verdict FAIL
>
> The project decision owner ruled on governance report `governance/reviews/GOV-2026-08-28-FD-01.md`
> (verdict **FAIL**) and authorised three remediations touching this unit. A redo jump cleared
> the write-freeze. **Every `## Review` section and every earlier dated box above is preserved
> unchanged**; the READY verdicts they record **predate these edits** and do not cover them.
>
> | Item | Rule | What changed |
> |---|---|---|
> | **Recommendation 2** (BLOCKER, `VAL-02`, Validation Auditor **veto**) — board option 1 | **R-28** | The one-door rule now carries a bounded, **enumerated `tests/` exemption of 4 modules**, each with its declared route for content reads, stated as a **narrowing** of D-15's framing — with `component-dependency.md`'s unqualified *"nothing else may construct a path into it"* quoted and the narrowing reconciled against it, not around it. Control clauses **1 → 5**. The live RES-04 consequence and its two dispositions are raised at the gate, unchosen |
> | **Recommendation 37** (`TEC-08`) — board option 1 | **R-23** | The produced-field limb now enforces **D-17's 8 enumerated exclusions** instead of §7.0's **5** classes, with the authority citation naming D-17. Field classes requiring a raise **5 → 8**; **2** new control clauses (renamed-instance matching, `cycle_slip`) |
> | **Recommendation 44(b)** (`VAL-08`) — board option 2 · and **44(a)** as recorded input | **R-27**, **R-26** | R-27's scan root **stated explicitly** as `evidence/` and deliberately not widened; the `.dst_summary.json` **relocation** recorded as the fix, with the move itself **not performed here**; the 44(a) loose-artifact manifest cited in R-27's integrity story with its hash independently re-derived. R-26's driver exclusion **enumerated at 4 classes** |
>
> **Counts derived and printed before assertion, per `project.md` § Way of Working.** Rules
> unchanged at **12** top-level (R-18…R-29) plus **3** sub-rules (R-18a, R-18b, R-19a).
> Requirements unchanged at **10**, **1** without an acceptance row (`FR-P1-02-6`), **2**
> acceptance rows owned (TA-27, TA-28). D-17's excluded set: **8** enumerated exclusions,
> **2** naming no §7.0 class token at all, **3** distinct quantities uncovered by §7.0's five.
> Exemption list: **4** modules, **3** present on disk. Driver-exclusion classes: **4**.
> `tests/` on disk: **3** modules, each defining `RESTRICTED_DIR` (`:46`, `:49`, `:49`).
> **Negative-control clauses across all 12 rules: 37 → 47**, derived by counting arrow-form
> clauses per rule against the pre-amendment file — R-23 **2 → 4**, R-26 **4 → 6**, R-27
> **4 → 6**, R-28 **1 → 5**, and the **other eight rules unchanged**, which is the check that
> the amendments touched only the four rules they were authorised to touch.
>
> **What this re-save does NOT do.** **BLK-06 remains open** — the protected-key list's
> derivation from TE §7.0B is untouched and nothing above bears on it. **G-09 remains
> unsigned**, and no rule here authorises creating `phase_contract.py`, `locked_test.py` or
> `reuse_registry.py`. No scientific constant is decided, no supervisor-owned value is read
> into, and no acceptance row is created. The three documentation-class findings riding the
> terminal READY remain **gate input**, unchanged and unapplied.

---

> **Re-confirmation receipt, 2026-08-29.** The 2026-08-27T21:49:36Z REDO jump reset every
> unit's receipt floor. This unit's content had already changed after that floor under the
> G-09 pass (D-29 through D-32; G-09 signed under D-31 with its §18.3 preconditions disclosed
> unmet), so the owner re-confirmed the unchanged post-G-09-pass content via the Consolidated
> Summary Confirmation at the foot of `functional-design-questions.md`, receipted `2026-08-29`.
> No line above this marker was touched by this pass.
