# Business Rules — `governance-guards`

**Unit** `governance-guards` (Bolt 2) · **Kind** `library` · **Depends on** `foundation`

The prohibitions this unit enforces at run time, each with what it rejects, what it
raises, and the negative control that proves the rejection happens.

**This project's affirmed methodology is a negative control paired with every hard
rule** — a test that proves the violation is *caught*, not only that the happy path
works. Every rule below carries its negative control, and where no acceptance row
exists to accept that control, it says so.

## Sources

- `../../../inception/requirements-analysis/requirements.md` — REQ-ENG-5; FR-P1-02-6; FR-P1-03-2; FR-P1-05-12; FR-P1-06-1…-4; NFR-PHASE-01; NFR-LIC-01.
- `../../../inception/units-generation/unit-of-work.md` § 2 — the `Owns` list, the boundary, BLK-06, BLK-07, and ADR-02/ADR-03.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2 plus § Per-unit coverage summary; both derivation paths agree.
- `../../../inception/application-design/component-methods.md` — the raise-contracts for every function named below.
- `../../../inception/application-design/component-dependency.md` § Shared resources — the unqualified single-path carve-out.
- `../../../inception/application-design/services.md` — § Stage entry contract, step 4.
- `evidence/DECISIONS.md` **D-24** (17 protected items) and **D-15** (restricted-root relocation).
- `../foundation/functional-design/business-rules.md` — R-01's `IntegrityError` base and the two-tier posture this unit inherits.
- `functional-design-questions.md` — Q1–Q8, the Step 4 analysis, Amendments D and E.
- `domain-entities.md` and `business-logic-model.md` — the shapes and workflows these rules constrain.

---

## The two tiers, inherited

`foundation` R-01 fixes the hierarchy and `team-practices.md` § Code Style fixes the
posture. Every rule below is an **integrity violation**: it terminates the run
non-zero with a message naming the resource and the violated expectation, raised as
an `IntegrityError` subclass. **No rule in this unit is a completeness shortfall.**
That is not an accident — a guard that degrades to a warning is not a guard.

---

## R-01 — Config-section digests are canonical, not byte-literal

**Rule (Q1 = D).** A config-section digest is computed over a **canonical
serialization** of the parsed section: keys sorted, comments dropped, scalars
normalised. **Six** of D-24's 17 items use one — items **4, 7, 9, 11, 14, 16** —
and item 13 uses one as half of a `Source + config-section hash`.

> **Corrected 2026-08-22.** Superseded text, preserved: *"Eight of D-24's 17 items
> use one — items 4, 5, 6, 7, 9, 11, 14, 16."* Items **5** and **6** are typed
> **`Field hash`** in D-24, a different mechanism, and were silently folded into this
> one. Derived: `... $5 ~ /Config-section hash/` → `4 7 9 11 14 16`;
> `... $5 ~ /Field hash/` → `5 6`. The full six-kind taxonomy covering all 17 items
> is in `business-logic-model.md` § W-3a, and the field-hash contract is § W-3b.

**Rule — the field-hash contract (items 5 and 6).** A field hash resolves the item's
**named field set** (literal names and declared patterns), **asserts the resolved set
is non-empty** — a pattern matching nothing must fail, because a digest over zero
fields would pass every diff — canonicalises the `name → value` pairs with the **same
canonicaliser** as the section path, digests, then applies the item's own assertion:

- **Item 5, history window** (`configs/experiment.yaml`): the value is the frozen
  **24 h** *and* the field appears in **no grid**. Both limbs. The second is what
  stops the window being tuned, which `project.md` § Forbidden makes a defect.
- **Item 6, station encoding** (`configs/features.yaml`): `station_onehot_*` plus
  `station_lat`. **D-24's word "verified" is NOT this unit's verification** — this
  unit hashes the field; whether `station_lat` is verified is
  `inventory-and-registry`'s, via `assert_registry_resolved`.

**Negative controls for the field path.** A pattern matching zero fields → **fails**.
Item 5's field present in a grid → **fails**. Item 5's value changed from 24 h →
digest changes. Item 6 with `station_lat` absent → fails on the non-empty assertion.

**Rule — the parameter-hash contract (the second half of item 15).** D-24 types item
15 as **`Source + parameter hash`** and names the parameters verbatim: *"24-hour
vector blocks, 10,000 replicates, seed 20221201."* A parameter hash is a sibling of
the field hash — same canonicaliser, named set — with two differences:

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

**Negative controls.** Omit any one of the three parameters → **fails** the resolution
assertion. Change the block width from 24 h, the replicate count from 10,000, or the
seed from 20221201 → digest changes in each case.

> **Added 2026-08-22 after the final adversarial pass**, which found item 15's second
> half silently folded into a generic composite bucket with no parameter-hash kind
> defined. Same defect class as the eight-versus-six miscount, on a `TC-19`
> hard-binding item. The full taxonomy is `business-logic-model.md` § W-3a and this
> contract is § W-3c.

**Constraint.** A **per-item key list** is asserted to cover its section, so a field
added to a section and not to the list fails a test rather than going silently
unprotected.

**Constraint.** The **canonicaliser's own version is recorded in the manifest**.
Changing how you canonicalise changes every digest, so the canonicaliser is itself
part of the frozen contract.

**Why not raw bytes.** A byte digest changes on a comment edit, a key reorder, a
quote-style change or a trailing-whitespace fix — none of which alters a governed
value. G-P3C would fail on formatting, and a team that learns to expect spurious
failures stops treating a real one as real.

**Negative controls.** Reflow a comment, reorder keys, change quote style → digest
**unchanged**. Change one governed value → digest **changes**. Add a field to the
section but not the key list → the coverage test **fails**.

**Acceptance.** TA-27 (`governance-guards`).

## R-02 — Changing the protected set produces a new digest, and that is correct

**Rule (Q3 as modified by the owner).** `configs/experiment.yaml` holds **only** the
authoritative 17 protected-item identifiers and their per-item coverage. The
resulting config-section digest is stored **externally, in the transition
manifest** — never inside the section.

**Therefore there is no self-reference.** Changing the list simply produces a new
digest.

> **That is correct behaviour and must not be described as a circularity.** A change
> to the protected-set enumeration is a governed change requiring a Vision §15.2
> amendment and a D-number, so it **should** surface as a manifest difference.
> Calling it circular would be an argument for hiding it.

**Constraint — the complete mapping is hashed, values included.** It is **never**
excluded from hashing to avoid circularity. Excluding it would leave the enumeration
that defines what is protected as the one unprotected thing in the set. Because the
Step 4 analysis settled the identifiers and their coverage lists as **one
structure**, this covers a coverage-list drift as well as an identifier change.

**Constraint — genuine self-reference gets a narrow rule.** *If* the hashed section
ever stores its **own expected digest**, canonicalization removes or normalizes
**only that self-referential digest value**. Nothing else is removed on that
ground.

**Negative control.** Place a digest inside the section, assert canonicalization
neutralises exactly that value and leaves every other key contributing.

**Acceptance.** TA-27.

## R-03 — The canonical contract handles every mutation of the protected set

**Rule (Q3, required tests).** Each mutation below has one required behaviour, and a
test asserts it:

| Mutation | Required behaviour |
|---|---|
| **Deletion** of a protected key | Digest changes **and** the freeze-mode membership assertion fails |
| **Addition** of a key | Digest changes **and** the membership assertion fails against D-24's 17 |
| **Duplication** of a key | **Rejected.** D-24's cardinality of 17 is *calculated from the enumeration*, so a duplicate is a malformed set, not a longer one |
| **Reordering**, semantically irrelevant | Digest **unchanged** — the 17 items are a set, and R-01's canonical form sorts keys |
| **Renaming** a key | Digest changes **and** the membership assertion fails; the name *is* the identifier |
| Frozen manifest contents | **Exactly** D-24's 17-item set — no more, no fewer, no duplicates |

**Why duplication is rejected rather than tolerated.** D-24 states the cardinality
is calculated from its enumeration (14 carried forward + 3 added = 17). A set that
parses to 18 entries with one repeated does not have 18 protected items; it has a
defect. Silently deduplicating it would hide an edit nobody approved.

> **Where this test gets D-24's list from is OPEN.** It must assert against the
> **authority**, not merely against the config — otherwise config and manifest can
> agree with each other while both drift from D-24. Both available routes carry a
> named cost: hardcoding is a fourth copy of a governed enumeration; parsing
> `evidence/DECISIONS.md` makes a governance prose document a test dependency, which
> Q3 option C was rejected for. **No third option is invented.** Until the owner
> directs, this test cannot be specified completely, and that is stated rather than
> papered over.

**Acceptance.** TA-27.

## R-04 — A freeze-mode manifest raises on any absent item; a draft records it

**Rule (Q2 = D).** `build_transition_manifest` records an item whose governing
artifact is absent with an explicit **`absent` sentinel**, and raises **only** when
built for a **freeze**.

**Constraint.** The **build mode** (`draft` | `freeze`) is recorded **in the manifest
itself**, so a draft can never be mistaken for a freeze.

**Constraint.** A freeze-mode build **additionally asserts the key list equals
D-24's 17 items**, so a short list cannot pass silently — which is what
`component-methods.md` already demands.

**Why draft mode exists.** All 17 governing artifacts are absent today. Under a
raise-always rule the manifest could not be built, tested or demonstrated until the
final Bolt — and a mechanism first run at a freeze gate is a mechanism first debugged
at a freeze gate.

**Negative controls.** Freeze-build with one item absent → raises. Freeze-build with
16 keys → raises on the membership assertion. Draft-build with all 17 absent →
succeeds, and the manifest is unmistakably marked `draft`.

**Acceptance.** TA-27.

## R-05 — An empty diff is not yet proof

**Rule.** `diff_protected_hashes` returning an empty mapping is the **G-P3C pass
condition**.

> **Constraint, binding now.** **BLK-06's enumeration limb is RESOLVED by D-24 at 17
> items. Its per-item binding to concrete config fields and file paths is PENDING.**
> Until that binding is discharged **and approved**, **an empty diff must not be read
> as proof that no protected item changed**, and no artifact, manifest or report
> produced by this unit may state or imply otherwise.
>
> `component-methods.md`'s standing caution is **half-discharged, not retired**. See
> `functional-design-questions.md` § Amendment D — the two approved artifacts that
> still describe the enumeration as deferred are reported, not edited.

**Negative control.** A manifest whose `protected_hashes` is missing an item must
fail the membership assertion **before** any diff is computed, so a short set can
never produce a reassuring empty diff.

**Acceptance.** TA-27.

## R-06 — Both phase-boundary limbs run, and neither substitutes for the other

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
`verification.py` were added as raw-processing adapters per finding `IMPL-2`.

**Constraint — the import limb runs inside the session.** It is called at step 4 of
the stage entry contract, because a Kaggle session carries no git working tree, so a
commit hook cannot fire there and a local suite run proves nothing about the
environment the governed run executes in (ADR-02, Q3 = B).

**Negative controls.** Import each of the four modules under `--phase 1` → each
raises, naming that module. Present a frame carrying each of the five forbidden field
classes → each raises, naming the field. Assert neither limb passing implies the
other.

**Acceptance.** TA-27; contributes to WS-10, TA-07, TA-08, TA-12 through REQ-ENG-5
(all owned by other units — `features-and-splits` ×3, `models-and-baselines`).

## R-07 — The produced-field limb runs per producing script, with completeness asserted

**Rule (Q6 = C).** `assert_no_raw_fields` is called by **each Phase 1 producing stage
script before it writes**, and a **completeness test asserts that every Phase 1
producing script calls it**.

**Why not inside the release API.** That would put a Phase 1 prohibition inside
`foundation`'s release path and invert the dependency — `governance-guards` depends
on `foundation`, never the reverse, and the reverse edge would **close a cycle** the
unit design deliberately avoids.

**Why not only at the transition-manifest build.** That detects a violation after
every artifact is written and possibly after downstream work has consumed the
contaminated frame. A guard that fires at the end is a post-mortem.

**Why the completeness test is the rule.** A per-script obligation without it is a
list, and a new script that forgets the call is silently unchecked — the
`DP-DATA-01` failure mode. This is the **third** use of the list-plus-completeness-test
shape in this design (with R-01's key list and `foundation`'s `RequiredFieldsMap`),
and the repetition is deliberate.

**Negative control.** Add a producing script that omits the call → the completeness
test fails.

**Acceptance.** TA-27.

## R-08 — The access log is durably appended BEFORE the December read begins

**Rule (Q5 = C, hardened on the owner's direction).**

> **The access-log append must be DURABLY COMPLETED before the December read
> begins.** A log-write failure **or** a durability failure must **prevent the
> read** — not be reported alongside it, not be retried after it, not be logged as a
> warning while the read proceeds.

**Constraint.** `open_restricted` writes the `AccessRecord` **and flushes it** before
returning the path. **Raises** `LockedTestError` when the registry write fails — *"a
failed log write must abort the read, not proceed unlogged"* — and when `path` is not
under `RESTRICTED_ROOT`, because callers must not route ordinary reads through the
guard.

**Why the ordering is the requirement, not a preference.** `VAL-2` and FR-P1-02-3
make log-then-read the contract: **an access recorded after the fact fails the
ordering check rather than satisfying it.** An unlogged read of the locked month is
the breach this guard exists to prevent, and it cannot be undone once taken.

**Negative controls — two, because the contract has two limbs.** Patch the log writer
to fail → assert the read **never happens**. Assert the log row is **durable on
disk** before the read is attempted, distinguishing this contract from one that logs
and reads in the same buffered transaction, where a crash loses the row and keeps the
read.

**Context that must not be lost.** The access log already holds **five retrospective
rows** predating this guard (`evidence/experiment_registry.md` records rows 3, 4, 5,
8 and 9 as retrospective). The log therefore contains two kinds of row, and the
distinction lives in the register explicitly rather than being inferred from
ordering.

**Acceptance.** Contributes to WS-18 and TA-18 via FR-P1-05-12 — **both owned by
`features-and-splits`**, not by this unit. ADR-03 splits the guard deliberately: the
access-log limb here, the execution limb in `splits.py`, with the test covering both
owned there to keep this unit a DAG root.

## R-09 — A December-bearing artifact is identified by record date, never by name

**Rule (Q4 = C).** `assert_no_december_outside_restricted` walks `evidence/`
**recursively** and identifies a December-bearing artifact by **content scan on
observation dates**. An empty returned sequence is the pass condition.

**Constraint — never by filename or directory name.** `project.md` § Forbidden:
*"NEVER derive fold or partition membership from an acquisition directory name or a
filename."* That rule exists because a year-blind predicate filed locked-month
records into `audit_evidence_2022-01/`, where a name-based check cannot see them.

**Constraint — an unparseable artifact is a FAILURE, not a pass.** A file the guard
cannot read is exactly where a December record would hide. Getting past it requires
an **explicit recorded exclusion**, never silence.

**Constraint — recursive by construction**, because `DATA-01` showed a non-recursive
glob silently stopped checking the artifacts that matter most.

**Negative controls.** Plant a December record inside a non-December-named directory
→ the guard finds it. Plant an unparseable file → the guard **fails**. Run against
the post-D-15 tree → assert the 21 relocated files are inside the restricted root and
none is outside it.

> ## ⚠ FR-P1-02-6 IS EXPLICITLY UNTESTED, AND STAYS THAT WAY
>
> **This rule's requirement has NO §16 or §19 acceptance row** — derived from
> story-map Table 1 and cross-checked against § Per-unit coverage summary. It is this
> unit's one untested requirement.
>
> On the project decision owner's explicit direction, FR-P1-02-6 is preserved as an
> **explicitly untested obligation until an approved acceptance row exists AND its
> test has passed** — both conditions, not either.
>
> Everything above is a **test specification only — not an approved acceptance row
> and not evidence of a passing result.** Designing the guard does not test it.
> Implementing it does not test it. **No artifact, manifest or report may state or
> imply that FR-P1-02-6 is covered, satisfied or verified.**

## R-10 — One path into the restricted root, and BLK-07 is not this design's to close

**Rule.** `open_restricted` is the **only** path into `evidence/locked_test_restricted/`.
`component-dependency.md` § Shared resources states it without qualification:
*"nothing else may construct a path into it."*

**Why absolute.** **D-15** records that the restricted root is a **governance
boundary, not an access control** — it holds only while exactly one code path reaches
it. A second path does not weaken it slightly; it ends it.

**Constraint (Q8 = D).** A **static check asserts no module outside `locked_test.py`
contains the restricted-root literal.**

**Negative control.** Add the literal to another module → the static check fails.

> ## ⚠ BLK-07 IS OPEN AND STAYS OPEN
>
> Four units reach the root through this contract: `inventory-and-registry` (pre-G-05
> coverage audit), `acquisition` (the D-9 input and any December re-acquisition — the
> unrecorded routing that **is** BLK-07), `features-and-splits` (locked partition),
> `evaluation-and-comparison` (locked evaluation).
>
> **Acceptance of this design mechanism is NOT authorization to open locked December
> data.** Which units are authorised to reach the locked month is a decision the
> **project decision owner receives and approves**. Nothing in this unit's artifacts
> grants it, implies it, or substitutes for it — the static check enforces *how many*
> paths exist, never *who* may use one.

**Acceptance.** Contributes to TA-18 (owned by `features-and-splits`).

## R-11 — Reuse is registered before use, and reimplementation is the default

**Rule (NFR-LIC-01, §10.1, Q7 = D).** Any reused or materially adapted third-party
source is recorded in the register with **all fifteen fields**, **before the code is
used** and before gate **G-P2**.

**Constraint — the register is the exception path, not the main road.** The standing
default is **reimplementation from the paper with a citation**. `project.md`
§ Forbidden prohibits copying source whose licence is absent, ambiguous or
incompatible, and that is the rule in force while the AGPLv3 question is open.

**Constraint — completeness is checkable.** Every adapter module carries a mandatory
**provenance marker**; the register is asserted complete against the set of marked
modules, and an unmarked module is asserted to contain **no reuse**. Without the
marker an unregistered copy is indistinguishable from original work by inspection.

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
| R-09 — December-bearing artifacts outside the restricted root | **FR-P1-02-6** | ⚠ **No §16/§19 row.** Preserved as explicitly untested until an approved row exists **and** its test has passed |

**One of ten**, matching the story map's designation exactly.

## Assumptions & Open Questions

- **[assumption]** `tests/test_locked_test_guard.py` is not this unit's — ADR-03 splits the guard, and `features-and-splits` owns the test covering both limbs to keep this unit a DAG root.
- **[assumption]** NFR-PHASE-01's transition-manifest hash-diff test has no §12 module and needs frozen artifacts from every later unit; carried on `fixtures-and-reproducibility` with this unit supporting.
- **[assumption]** Whether `build_mode` and `canonicaliser_version` are new `TransitionManifest` fields or entries in an existing mapping is a stage 3.5 shaping decision. Only semantics are fixed here, so **no approved dataclass contract is changed by this stage.**
- **Open — R-03's D-24 conformance test source.** See the boxed note in R-03. **No option invented.** Raised at the gate.
- **Open — BLK-06's per-item binding.** Enumeration resolved by D-24 at 17; binding **PENDING**. R-05 states the consequence: an empty diff is not yet proof.
- **Open — BLK-07 authorization.** See R-10. The owner's decision, not this design's.
- **Open — Amendment D.** `component-methods.md` and `unit-of-work.md` § 2 carry text superseded by D-24, with provenance preserved. **Neither edited by this stage.**
- **Open — the AGPLv3 distribution question.** Unresolved; the standing default is reimplementation with a citation.
- **G-09 is not signed.** No rule here authorises creating any module.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.
