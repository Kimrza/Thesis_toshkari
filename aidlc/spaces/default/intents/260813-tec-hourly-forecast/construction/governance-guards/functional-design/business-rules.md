# Business Rules — `governance-guards`

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

**Rule (FR-P1-03-2, NFR-PHASE-01).** Two independent results are required:

- **Import limb** — `assert_phase_boundary(phase, loaded_modules)`: under
  `phase == 1`, no name in `RAW_MODULES` may be present. **Raises**
  `PhaseBoundaryError` naming the offending module.
- **Produced-field limb** — `assert_no_raw_fields(frame, phase)`: a Phase 1 artifact
  may carry no DCB, STEC, mapping, satellite or arc field. **Raises**
  `PhaseBoundaryError` naming the field.

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

**Negative controls.** Import each of the four modules under `--phase 1` → each
raises, naming that module. Present a frame carrying each of the five forbidden field
classes → each raises, naming the field. Assert neither limb passing implies the
other.

**Acceptance.** TA-27; contributes to WS-10, TA-07, TA-08, TA-12 through REQ-ENG-5
(all owned by other units — `features-and-splits` ×3, `models-and-baselines`).

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
a class to the driver-exclusion list → the membership test fails. Mislabel a target
file as a driver class → fails, because the excluded classes are enumerated and the
file does not belong to one.

**Acceptance.** ⚠ None — see R-27's box. This rule shares FR-P1-02-6's missing
acceptance row.

## R-27 — The guard walks every file, dispatched per artifact class, and an unparseable file is a failure

**Rule (Q4 = C).** `assert_no_december_outside_restricted` walks `evidence/`
**recursively** and opens **every file**, dispatching each to a **declared parser for
its artifact class**. An empty returned sequence is the pass condition.

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
none is outside it.

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

**Rule (Q9 = D).** A **static check asserts no module outside `locked_test.py`
contains the restricted-root literal.** `open_restricted` is the **only** path into
`evidence/locked_test_restricted/`; `component-dependency.md` § Shared resources
states it without qualification: *"nothing else may construct a path into it."*
`foundation`'s **R-15** already states its own side of that as the absence of a path.

**Why absolute.** **D-15** records that the restricted root is a **governance
boundary, not an access control** — it holds only while exactly one code path reaches
it. A second path does not weaken it slightly; it ends it.

**Why not a caller allow-list inside the guard.** Q9's option C would have
`open_restricted` raise when its caller is not one of the four recorded consumers.
That closes the run-time-path-assembly gap but couples this root unit to four
downstream units, and the reverse edge would **close a cycle** the DAG was arranged to
avoid. The residual gap — a path assembled at run time from fragments — is left open
deliberately, because the static check plus review makes it unlikely and the acyclic
structure is worth more.

**Negative control.** Add the restricted-root literal to another module → the static
check fails.

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
- **G-09 is not signed.** No rule here authorises creating `phase_contract.py`, `locked_test.py` or `reuse_registry.py`.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.
