# Functional Design Questions — `inventory-and-registry`

**Unit** `inventory-and-registry` — the source inventory, the station registry, schema
validation of the prepared product, and the performance-blind coverage and regime audit
that **G-P1A** accepts.
**Kind** `library` · **Complexity** M · **Deployment** standalone · **Depends on**
`acquisition`.

Unit **4 of 12**. It owns `src/data/inventory.py`, `src/data/registry.py`,
`scripts/01_inventory_and_registry.py` and `tests/test_station_registry.py`, and it is
the unit that **performs the required pre-G-05 December coverage and regime audit** —
the one December read this project treats as legitimate before the lock opens.

**7 requirements, 2 with no §16/§19 acceptance row** — FR-P1-02-7 and FR-P1-02-8.
Derived from story-map Table 1 and cross-checked against § Per-unit coverage summary,
which reads `inventory-and-registry (2)` with exactly those IDs. It **owns** WS-01,
TA-04 and TA-25, and **supports** WS-18, TA-18 and TA-32.

**Read against `acquisition`'s 7-of-15**, this unit is comparatively well covered — but
its two gaps sit on the registry's §6.2 content and on the four G-P1A prohibitions, and
**FR-P1-02-8's gap was invisible until the fifth revision** because the row cited
`TA-29`, which `requirements.md` itself lists as *"Not applicable in Phase 1 — Phase 2
by definition"*. It counted as covered while nothing tested it, and **four governance
boards passed over it**. That is the clearest evidence in this project that a citation is
not a test.

**Workspace state, read directly on 2026-08-23 rather than cited:** `src/` and `configs/`
**do not exist**. `tests/` holds three modules — `test_acquisition_window.py`,
`test_phase_boundary.py`, `test_release_hashes.py` — and **`tests/test_station_registry.py`,
this unit's mandated test, is not among them.**
`notebooks/madrigal_phase1_coverage_audit.ipynb` holds the station coordinates as an
inline literal whose own `source` field reads
`'IGS network page -- cross-check against site log required'`.

**G-09 is not signed.** No answer here authorises creating any module.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 4 — the `Owns` list, the boundary, the 7 requirements, and the implementation notes.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2 plus § Per-unit coverage summary. **Derived by reading the rows:** 7 requirements, **2** with no acceptance row; **owns** WS-01, TA-04, TA-25; **supports** WS-18, TA-18, TA-32.
- `../../../inception/requirements-analysis/requirements.md` — FR-P1-02-1 through -5, -7, -8; § Known defects rows 3 and 9.
- `../../../inception/application-design/component-methods.md` — `src/data/registry.py`'s `Station`, `load_registry`, `assert_registry_resolved`; `src/data/release.py`'s `write_release`, which validates `source_files` **against `inventory.py`**.
- `../../../inception/application-design/services.md` § The nine stage scripts and § Stage entry contract.
- `../acquisition/functional-design/business-rules.md` — **R-32** and **R-33**, the named-accessor routing this unit's December audit must use. This unit is `acquisition`'s first downstream consumer.
- `../governance-guards/functional-design/business-rules.md` — **R-25** (durable log before read), **R-26** (what counts as a December hit), **R-28** (one path in).
- `evidence/DECISIONS.md` — **D-1** and its **2026-08-21 addendum**, **D-2**, **D-12**, **D-13**, **D-143**, **D-144**.
- Workspace inspection, 2026-08-23: `notebooks/madrigal_phase1_coverage_audit.ipynb`, `tests/`, and the absence of `src/` and `configs/`.
- Absent by scope design: `stories` (2.4 `SKIP`), `mockups` (1.6 and 2.5 `SKIP`). `kind: library`, so `frontend-components.md` is not produced.

---

## Question 1

**`src/data/inventory.py` has no contract.** `unit-of-work.md` § 4 names it in this
unit's `Owns` list, and `component-methods.md`'s `write_release` says `source_files`'
six items *"are validated against `inventory.py` rather than restated as a bare hash"* —
so an approved contract already **depends on** it. But `component-methods.md` defines no
`inventory.py` block at all: no dataclass, no function, no raise-contract.

This is the same shape as the defect the adversarial reviewer caught one unit ago on
`acquisition`, where BLK-07's central accessor was a symbol absent from the approved
contract and flagged nowhere. Here the absence is upstream of this stage rather than
introduced by it.

What is `inventory.py`'s contract, and how is its absence handled?

A) Design it here as a new contract and treat it as settled by this stage
   > **Impact**: Fastest, and this unit owns the module. But `component-methods.md` is an approved stage-2.6 artifact and `write_release` already references `inventory.py` — designing its contract here without a change record repeats exactly the defect just caught, one unit later, with the reviewer's finding still in the previous unit's Review section.

B) Design it here **and** record it as an amendment owed to `component-methods.md`, requiring a change record before stage 3.5 treats it as approved
   > **Impact**: Same design work, with the governance status stated. It matches how `acquisition` records its three amendments, so the two units read consistently. Costs one more amendment on the pile, which is itself worth surfacing at the gate as a pattern rather than a list. **Note added 2026-08-23:** this option's premise — that an amendment is owed at all — does not hold; see the Assumptions entry. The question is preserved as asked.

C) Do not design it; raise the absence as a blocker and stop
   > **Impact**: Strictly correct about authority, and it refuses to build on an unsettled foundation. But `write_release` already depends on the module, so the gap blocks `foundation` too, and stopping here leaves the dependency unstated rather than resolved. Nothing in the blocker register currently names it.

D) B, with the contract deliberately **minimal** — only what `write_release`'s stated dependency and FR-P1-01-6's nine-field inventory actually require, nothing speculative
   > **Impact**: Keeps the amendment as small as it can be, which matters because the change record has to be reviewed by someone. A minimal contract is also easier to widen later than a speculative one is to narrow. Costs leaving obvious conveniences out, and accepting a second amendment when a later unit needs more.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A is ruled out by the finding this project just recorded against itself. C is right about authority and wrong about consequence — the dependency exists in an approved artifact today, so refusing to design leaves `write_release` referencing a module nobody has specified, which is worse than a stated amendment. B and D differ only in scope, and D is the version that keeps the change record reviewable: the two things `inventory.py` demonstrably must do are satisfy `write_release`'s `source_files` validation and hold TE §5.1's nine fields per source entry. Everything else is speculation about units not yet designed.

[Answer]: D

---

## Question 2

FR-P1-02-1 requires station coordinates and the coordinate-to-cell rule to be
*"validated against the **official IGS site logs** before being treated as final."*

**They have not been.** D-1's own Known limitation, quoted: *"Station coordinates are
taken from IGS network pages, **not** from the official IGS site-log PDFs, which rank
higher in the §6.2 evidence hierarchy… Site-log validation remains outstanding."* The
D-1 addendum (2026-08-21) repeats it as **separate and still open**. The notebook literal
says the same thing in its own `source` field:
`'IGS network page -- cross-check against site log required'`.

Meanwhile `assert_registry_resolved` **raises** `RegistryError` when any §6.2 field is
missing, and an unresolved registry **blocks `station_lat` and excludes `lst_sin`/`lst_cos`**.

So: does a registry whose coordinates are unvalidated against site logs count as
**unresolved**?

A) No — `assert_registry_resolved` checks field *presence*, and the coordinates are present
   > **Impact**: The pipeline runs today, and it matches the function's stated raise conditions, which name missing fields, a defaulted IGRF version and averaging — not provenance. But it makes FR-P1-02-1's "before being treated as final" unenforced by anything: the values are already being treated as final, and D-1's limitation becomes a note nobody's code reads.

B) Yes — an unvalidated coordinate is an unresolved field, and the registry raises until site-log validation is recorded
   > **Impact**: Enforces the requirement literally, and it is the reading `assert_registry_resolved`'s blocking role implies. But it halts the whole downstream pipeline **today**, on every station, until someone obtains three site-log PDFs — and nothing else in the plan is sequenced around that.

C) A per-field **provenance** field on `Station`, with the raise conditioned on provenance rather than on presence
   > **Impact**: Makes the distinction explicit and checkable: a coordinate carries where it came from, and the gate decides what provenance is sufficient for what purpose. G-P1A can require site-log provenance while a fixture run does not. Costs a field on an approved dataclass — another amendment — and a decision about which consumers demand which provenance.

D) C, with the sufficiency decision **deferred to the owner** rather than set here, and the default being that **G-P1A requires site-log provenance** while lower gates do not
   > **Impact**: Records the mechanism without this stage adopting a reading on a §18.2 forbidden-choice item — station coordinates are a **Student** forbidden choice and the cell rule a **Student + Supervisor** one, so what counts as sufficient validation is arguably the owner's. The stated default keeps the requirement enforced where it matters most. Risk: a default is still a reading, and stating one may be taken as settling what it defers.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C, with the G-P1A default raised at the gate rather than written in. A leaves FR-P1-02-1 with nothing enforcing it, which is how a requirement quietly becomes a comment. B is the honest literal reading and would stop the project dead on an obligation nothing has scheduled — and D-1's own limitation records that all three stations sit ≈0.14° or further from a cell edge, so no assignment would change. C separates *presence* from *provenance*, which is the actual distinction, and makes the requirement checkable without halting anything. D's instinct about the owner's authority is right, but writing a default is how a deferral stops being one; recommend stating the mechanism in C and putting the sufficiency question to the owner explicitly.

[Answer]: C

---

## Question 3

`assert_registry_resolved` must raise when *"a conflict was resolved by averaging"* —
FR-P1-02-1 quotes Vision §6.2: *"A conflict must be resolved and recorded, never averaged
or ignored."* The acceptance criterion is explicit that **a conflict resolved by
averaging fails**.

The difficulty is that **a number does not carry its own history**. Given a latitude of
40.286, nothing about the value reveals whether it was read from one source, chosen
between two, or averaged across them. A run-time check on the value alone cannot
distinguish the three.

How is "resolved by averaging" detectable?

A) A documented procedure — the operator records how each conflict was resolved
   > **Impact**: Costs nothing to build and is how such rules usually work. But §16 and §19 both state that visual inspection alone is insufficient, and this is a rule whose violation produces a plausible-looking number. An unenforced procedure here means the criterion "a conflict resolved by averaging fails" has nothing that could fail.

B) A **conflict register**: every source value for every field is recorded, and the registry's value must be **identical to one of them**
   > **Impact**: Makes averaging detectable by construction — an averaged value equals no source value, so the identity check fails on exactly the prohibited operation. Cheap, and it makes the check machine-verifiable rather than procedural. Costs recording every source value, and it does not catch a conflict resolved by picking the wrong source.

C) B, plus each resolved field recording **which source it came from and why**, with the "why" required to be non-empty
   > **Impact**: Covers "recorded", which is the other half of §6.2's sentence — *"resolved **and recorded**"* — and it is what a reviewer at G-P1A would actually need to judge whether the resolution was sound. A non-empty rationale is a weak check, but its absence is a strong one. Costs a field per resolved conflict.

D) C, plus a test that **injects** an averaged value and asserts the registry rejects it
   > **Impact**: The negative control this project's affirmed methodology requires for every hard rule — a test proving the violation is caught, not only that the happy path works. Without it, B and C are mechanisms nobody has demonstrated. Costs one test, and it is the cheapest of the four additions.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A cannot satisfy a criterion written as a failure. B is the mechanism that makes averaging detectable at all, and it is the whole trick here — an averaged value is exactly the value that matches no source. C adds §6.2's second half, which B alone drops. D adds the negative control that `team.md` § Testing Posture makes mandatory for every hard rule, and it is one test. The cumulative cost is a conflict register that is useful evidence at G-P1A independently of the check.

[Answer]: D

---

## Question 4

FR-P1-02-3, quoted, with its scope emphasised in the requirement itself: *"An access-log
row with `locked_test_accessed = true` is written **BEFORE any operation that reads a
December 2022 record** — the scope is **access, unqualified**, so it covers derived-artifact
merges, re-derivations, corrections, coverage recounts and schema validations, **not only
a model execution**."*

This unit performs the **required pre-G-05 December coverage and regime audit**, so it is
the first unit whose ordinary work routinely reads December. Three of its own operations
are named in that list: **coverage recounts**, **schema validations**, and
**re-derivations**.

`acquisition`'s **R-32** established the routing shape — named accessors in
`locked_test.py` that delegate to `open_restricted` — and its **R-33** gave restricted
writes their own log-before-write contract.

How does this unit's December audit obtain its access rows?

A) One access row per audit run, written before the run begins
   > **Impact**: Simplest, and it satisfies "before any operation" if the whole audit is treated as one operation. But an audit that reads December across twelve months, three cells and several artifact classes is many operations, and one row makes the log say less than what happened — a reviewer cannot tell which reads occurred.

B) One row per **artifact opened**, through `acquisition`'s named-accessor pattern
   > **Impact**: The log then records what was actually read, which is what makes it evidence rather than a formality. It reuses the routing already designed rather than inventing a second one. Costs a row per artifact, and a busy audit produces a long log — which is arguably the correct outcome.

C) B, with the audit declaring its **intended scope** up front and a post-run assertion that the rows written match it
   > **Impact**: Closes the gap B leaves in the other direction: B proves every read was logged, but nothing proves the audit read what it claimed to. A declared scope plus a reconciliation makes an audit that silently skipped a month detectable — and coverage figures are exactly the numbers a skipped month would quietly distort. Costs a declaration and a reconciliation step.

D) C, plus the audit refusing to run if any required row would be its **first** December access without an authorization reference
   > **Impact**: Ties the mechanism to BLK-07's still-open authorization limb, so a run cannot proceed on routing alone. But BLK-07's authorization is the project decision owner's, and building a refusal keyed to it here would embed this stage's reading of an authorization it does not hold.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A makes the log thinner than the event it records. B is the right mechanism and reuses `acquisition`'s. C adds the limb that matters for an *audit* specifically: this unit's output is a coverage figure that a supervisor accepts at G-P1A, and a silently-skipped month produces a wrong figure that looks right — the reconciliation is what makes that detectable. D's instinct is sound but it would have this stage encode a reading of an authorization the owner has not given; the refusal belongs wherever BLK-07 is finally resolved, not here.

[Answer]: C

---

## Question 5

G-P1A acceptance is decided against **two** thresholds, and FR-P1-02-4 is explicit that
neither substitutes for the other:

- **D-12** (Vision §6.1B, frozen 2026-08-21): at least **90% usable hourly coverage per
  station per month**, as a hard gate.
- **D-2**: **≥95% of calendar days** present per month, and **100% of December days**
  (31/31).

The criterion also states that the decision record *"reports the measured per-station
hourly and day coverage for every month, and **never an unattributed number**."*

Two facts complicate this. **D-2 was set after partial data was seen** — its own
Disclosure records that five of twelve months had already been audited at 100% day
coverage when the threshold was chosen, and says so *"so a reviewer can discount it
accordingly."* And the measured hourly coverage as at 2026-08-21 is recorded as ARUC
99.2–100.0%, BSHM 99.3–100.0%, **NICO 93.2–98.9%** across nine cached non-December
months — every station-month clears 90%, but NICO's margin is thin.

What shape does the G-P1A decision record take?

A) A pass/fail verdict per station-month against both thresholds
   > **Impact**: Directly answers what the gate asks and is easy to read. But a bare verdict is exactly the "unattributed number" the criterion forbids — a reviewer cannot see the measurement behind a `PASS`, and NICO's 93.2% and ARUC's 100.0% would look identical.

B) A, plus the measured hourly and day figure for every station-month, each carrying its D-number
   > **Impact**: Satisfies the criterion literally: every number is attributed to the threshold it is judged against and to the measurement that produced it. It also makes NICO's margin visible rather than hidden inside a `PASS`. Costs a wider table — 3 stations × 12 months × 2 measures.

C) B, plus **D-2's disclosure carried into the record** — that the day threshold was set after five months were seen
   > **Impact**: The disclosure exists precisely so a reviewer can discount the threshold, and a decision record that omits it presents a partly post-hoc threshold as though it were blind. Carrying it is the difference between a record that can be audited and one that has to be cross-referenced to be understood. Costs three sentences and some discomfort.

D) C, plus a **margin column** flagging any station-month within a stated distance of either threshold
   > **Impact**: Turns a pass into a graded pass, which is genuinely useful when NICO sits at 93.2% against a 90% floor — a reviewer sees which cells would fail under a small re-measurement. But "within a stated distance" is a new threshold this stage would be inventing, and Vision §6.1B's minimum is a **supervisor** freeze; adding a second, softer band next to it risks being read as amending it.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A is barred by the criterion's own words. B satisfies them. C adds the one thing that makes the record honest without adding a number: D-2's disclosure was written to be read by whoever judges the gate, and a decision record that leaves it behind defeats the purpose the disclosure was written for. D is attractive and I would not argue against it later, but it invents a soft band beside a supervisor-frozen hard threshold, which is the kind of adjacent-number-that-becomes-the-real-rule this project has already had to correct once.

[Answer]: C

---

## Question 6

FR-P1-02-8 names **four prohibitions at the G-P1A gate**, and its criterion is unusually
specific: *"Each of the four has an injection test that **fails** the pipeline; **four
separate results, not one**."*

1. **Silent imputation**
2. **Source mixing**
3. **Retrospective split redesign after model performance is viewed**
4. **Labelling a map value as station-observed VTEC**

**This row is UNTESTED, and how it got that way is the point.** It previously cited
`TA-29` — a row `requirements.md` itself lists under *"Not applicable in Phase 1 — Phase
2 by definition"*. The citation made it **appear covered** and kept it out of the untested
list that stage 3.2 reads to size the G-05 freeze manifest. **Four governance boards
passed over it**; an advisory reviewer found it on the fifth revision.

Prohibition 3 is the awkward one: it is about an act performed by a **person**, after
seeing something, and this unit is where the gate lives but not where splits are designed.

How are the four proven?

A) Four injection tests owned here, one per prohibition
   > **Impact**: Matches the criterion's wording exactly and keeps the four results together where the gate is. But prohibition 3 concerns split redesign, which `features-and-splits` owns, and prohibition 4 concerns target labelling, which `target-standardization` owns — so two of the four would be tested by a unit that does not own the thing being prohibited.

B) Four tests, each owned by the unit that owns the prohibited act, with this unit asserting all four results are present at the gate
   > **Impact**: Puts each test where the knowledge is and keeps this unit's obligation to what it can actually do — check that four results exist and pass before G-P1A accepts. Costs a cross-unit dependency at the gate, and it means this unit cannot produce all four itself.

C) B, with prohibition 3 handled as an **ordering artifact** rather than a code test — the split definition's hash frozen before any performance figure is produced, and the gate asserting the hash is unchanged
   > **Impact**: Prohibition 3 cannot be caught by injecting a value, because the prohibited thing is a person changing a design after seeing a result. A frozen hash plus a timestamp ordering is the only form of evidence that can distinguish "designed before" from "redesigned after" — the same mechanism `governance-guards`' transition manifest already uses. Costs defining what exactly is hashed and when.
   
D) C, plus the four results being **named individually** in the G-P1A evidence set, so a missing one is visible rather than absorbed into a single pass
   > **Impact**: Directly answers how this requirement got lost in the first place: a single citation stood in for four obligations and nobody could see that three of them were unaddressed. Four named results make absence structural rather than a matter of noticing. Costs four names in the evidence set and the discipline of keeping them.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A misplaces two of the four. B fixes ownership. C fixes prohibition 3, which is genuinely not an injection-testable act — no injected value can prove a person did not redesign a split after seeing a result, and a frozen hash with an ordering claim can. D adds the limb aimed squarely at this requirement's own history: it went untested because **one citation stood for four obligations**, and naming four results is what makes that failure mode structurally impossible rather than something a fifth reviewer has to catch.

[Answer]: D

---

## Question 7

FR-P1-02-2: schema validation covers **parameter names, units, fill values, UTC cadence
and duplicates** for the prepared product. The acceptance is *"the prepared-data schema
report exists and passes."*

Where the expected schema **lives** decides whether this check can drift. `configs/` does
not exist yet, and `project.md` § Forbidden bars hiding a scientific constant in source or
a notebook — but a schema is not obviously a scientific constant, and TE §12 names exactly
**four** governed config files with no fifth.

Where does the expected schema live?

A) In `src/data/inventory.py` as a module-level constant
   > **Impact**: Adjacent to the validator and versioned with it. But it puts a contract the whole pipeline depends on inside one module's source, where a change is invisible to config review — and the four config files exist precisely to make governed values reviewable in one place.

B) In `configs/data.yaml`, as a schema block
   > **Impact**: Governed, versioned, hashable, reachable through `ConfigSnapshot`, and it needs no fifth config file. Units and fill values genuinely are scientific facts about the product. Costs deciding what belongs in a "schema" block versus the data settings already there.

C) B, with the schema block **hashed as part of the transition manifest's protected set**
   > **Impact**: A change to the expected schema would then surface at G-P3C rather than silently changing what "passes" means. But **D-24's protected set is frozen at 17 items and this stage does not reopen it** — adding an eighteenth is a Vision §15.2 amendment, not a design choice, and proposing it here would be reaching into a frozen decision.

D) B, plus the schema report recording **both** the expected schema's digest and the observed values, so a report is interpretable without the config it was run against
   > **Impact**: Makes the report self-contained evidence: a reviewer reading it a year later can tell what it was checked against without reconstructing the config state. It gets most of C's benefit — a changed schema produces a visibly different digest in the report — without touching D-24's frozen set. Costs a digest field in the report.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A puts a pipeline-wide contract where config review cannot see it. B is correct and sufficient for the requirement. C is the right instinct aimed at the wrong artifact: D-24's 17 items are frozen and adding an eighteenth is an amendment this stage has no authority to make, and `governance-guards`' own design says the enumeration does not reopen here. D gets the drift-detection benefit inside this unit's own evidence, where this stage does have authority, and leaves the protected-set question available to raise separately if the owner wants it.

[Answer]: D

---

## Question 8

**WS-01 is a named exception, and the exception is easy to lose.**
`requirements.md` § Known defects row 9 records it: `team.md` § Testing Posture defines
Phase 1's acceptance set as **WS-09 through WS-20**, deferring WS-01–WS-08 to G-P3A — but
**WS-01 is Phase 1-producible**, built by `01_inventory_and_registry.py` and
`test_station_registry.py`, neither of which is a raw-processing module. It was
**retained in Phase 1 as a named exception, approved by the project owner 2026-08-21**;
**WS-02 through WS-08 remain deferred unchanged.**

Without the exception, the Phase 1 station registry — *"the authority for `station_lat`,
the coordinate-to-cell rule and every per-cell statistic"* — would have **no acceptance
row at all**.

This unit owns WS-01. How do its artifacts carry the exception?

A) Cite WS-01 as this unit's acceptance row, as any other row would be cited
   > **Impact**: Accurate about the acceptance and simplest to write. But a later reader comparing this unit against `team.md`'s "WS-09 through WS-20" sees a contradiction with no explanation, and the likeliest repair is to assume WS-01 was cited in error — which would delete the registry's only acceptance row.

B) A, with a one-line note that WS-01 is a named Phase 1 exception
   > **Impact**: Prevents the misreading at minimal cost, and points a reader at the amendment. But a one-liner does not say what the exception's boundary is, and the realistic second failure is someone generalising it — "if WS-01 is in Phase 1, why not WS-04?"
   
C) B, stating the boundary explicitly: **WS-01 only; WS-02 through WS-08 remain deferred to G-P3A**, and the basis is that §7.0's Phase 1 prohibition does not reach a station registry
   > **Impact**: Closes both failure modes — the exception is not lost and it is not widened — and it records *why*, which is what lets a future reader judge a new candidate rather than guess. Costs a short paragraph in each artifact that cites WS-01.

D) C, plus a test asserting that the Phase 1 acceptance set is exactly WS-01 and WS-09–WS-20
   > **Impact**: Makes the boundary machine-checked rather than prose. But the acceptance set is a governance fact recorded in `team.md` and `requirements.md`, not a property of this unit's code, and a test here asserting the shape of a project-wide governance list would place an obligation on this unit that it does not own — the same ownership inversion `acquisition` declined when it refused to pin a sibling's enum.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A risks the exception being "corrected" away, and the thing it protects is the only acceptance row the station registry has. B stops the first misreading and not the second. C states the boundary and the reason, which is what makes it survive a reader who was not here. D's instinct — make it checkable — is the one this project usually rewards, but the acceptance set is governance rather than code, and asserting a project-wide list from inside one unit repeats an ownership inversion this workflow has already declined once.

[Answer]: C

---

## Question 9

The notebook's inline station coordinates are a **§18.2 forbidden-choice item**
(coordinates: **Student**; cell-selection rule: **Student + Supervisor**), and
`team.md` § Code Style fixes the migration order: the current inline constants are
**frozen as a D-number decision first**, and only then moved into `configs/data.yaml`
and `src/data/registry.py` — *"so the migration itself cannot silently change a scientific
value."*

**The cell rule is already frozen: D-1 is the freeze**, and its 2026-08-21 addendum
corrects the earlier belief that no freeze existed — *"The notebook literal is a duplicate
of a frozen decision awaiting migration… not the decision itself."*

**The coordinates are the unsettled half.** D-1 records them in its table, but with the
Known limitation that they came from IGS network pages rather than the site logs — the
same gap Question 2 addresses from the registry's side. So the migration's precondition
is satisfied for the rule and arguably not for the values.

What does this unit's design say about the migration?

A) Migrate both together on D-1's authority, treating the addendum as sufficient
   > **Impact**: D-1 does record the coordinates, and the addendum closes the governance condition for the rule. But it treats a decision carrying an explicit unresolved limitation as a completed freeze, and D-1's own text says site-log validation "remains outstanding" — migrating on that basis moves a value the decision itself does not call final.

B) Migrate the cell rule now on D-1, and hold the coordinates until site-log validation
   > **Impact**: Respects what D-1 actually says about each half. But it splits one migration into two, and it leaves `configs/data.yaml` holding a rule with no coordinates to apply it to — so nothing downstream can run until the second half lands, which is the same halt Question 2's option B produces.

C) Migrate both, with each coordinate carrying its **provenance** and the registry's resolution state derived from it (Question 2's mechanism)
   > **Impact**: One migration, and the unresolved half is represented rather than hidden: the value moves into config, and what is *not yet established about it* moves with it. Downstream consumers that require site-log provenance can refuse; those that do not can run. Costs the provenance field Question 2 introduces, and depends on that answer.

D) C, plus the migration emitting a **diff against the notebook literal**, asserting no value changed in the move
   > **Impact**: Directly enforces `team.md`'s stated reason for freezing first — *"so the migration itself cannot silently change a scientific value"*. A freeze prevents an intentional change; a diff catches an accidental one, which is the likelier failure in a hand migration of three coordinate pairs. Costs one comparison, run once.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A treats a limitation D-1 states plainly as though it were absent. B is faithful and produces a config that cannot be used, halting the project on an obligation nothing has scheduled — the same objection as Question 2's option B. C carries the unresolved provenance into the artifact instead of losing it at the boundary, which is what lets work continue without anyone forgetting what is outstanding. D adds the check that enforces the *stated purpose* of the freeze-first rule rather than only its form, and it costs one comparison over three coordinate pairs. This answer depends on Question 2 landing on the provenance mechanism; if Question 2 goes another way, this reduces to B.

[Answer]: D

---

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence — `foundation` R-01…R-17, `governance-guards` R-18…R-29, `acquisition` R-30…R-43 — so this unit opens at **R-44**. If per-unit numbering was intended, say so at the gate and the artifacts restart.
- **[assumption]** `tests/test_station_registry.py` is this unit's, per `unit-of-work.md` § 4 `Owns`. **It does not exist** — `tests/` holds three modules and that is not one of them.
- **[assumption]** WS-01's Phase 1 retention is settled governance (approved 2026-08-21, `GOV-2026-08-21-RA-01` Rec 12) and this stage records rather than revisits it.
- **[assumption]** `merge_coverage_year.py` migrates here, taking `--config configs/` and its `NN_verb_noun.py` position, and its `sha256_of_file` copy consolidates into `foundation`'s `src/data/release.py`. This stage designs the target shape, not the migration commit.
- **[assumption]** The December regime-count audit's **threshold** is D-13's (at least three independent storm events under Vision §9.3), and the count must come from GFZ Kp/Hp60 at a recorded release grade — **D-11 bars any provisional-Dst-derived figure**. This unit measures; it does not set the threshold.
- **`src/data/inventory.py` is specified by this stage, and owes no amendment.** `component-methods.md` § Depth specifies **cross-package boundary calls only** and its Assumptions name **`functional-design` (3.1)** as where intra-package shapes are specified; `inventory.py` and `release.py` are the **same package**. Question 1's answer (D) stands; its output is this stage's ordinary work. **Corrected 2026-08-23. Superseded reading, preserved:** *"whatever is designed is an amendment owed, not an approved contract."*
- **Open — the amendment count is growing across units.** `acquisition` recorded three owed amendments; Question 1 would make a fourth. Raised at the gate as a pattern worth a single consolidated change record rather than four separate ones.
- **Open — D-1's site-log validation limitation.** Recorded in D-1 and repeated in its addendum as *separate and still open*. Questions 2 and 9 both turn on it; neither closes it.
- **Open — station coordinates are a §18.2 Student forbidden choice and the cell rule a Student + Supervisor one.** What counts as sufficient validation is the owner's, not this stage's.
- **Open — BLK-07's authorization limb**, carried from `acquisition`. This unit's December audit is routed through the mechanism `acquisition` R-32 fixes, and **no run may touch calendar 2022-12 while the authorization limb stands.**
- **Open — `RES-01`**, permitted-read access logging is NOT TESTED, owned by stage 3.2 — and **this unit performs the permitted read** `RES-01` is about.
- **Open — FR-P1-02-8's four prohibitions were untested behind a withdrawn `TA-29` citation** that four governance boards passed over. Question 6 addresses the mechanism; the missing acceptance row is stage 3.2's and change control's.
- **Open — `src/` and `configs/` do not exist**, so every path and field named here is named by an authority document and none is claimed to exist today.
- **G-09 is not signed.** No answer here authorises creating `src/data/inventory.py`, `src/data/registry.py`, `scripts/01_inventory_and_registry.py` or `tests/test_station_registry.py`.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

---

## Consolidated Summary Confirmation

Questions 1–9 are answered above as the recommended option in each case, on the
owner's instruction to apply the recommendations. Consolidated:

| Q | Answer | What it settles |
|---|--------|-----------------|
| 1 | D | `src/data/inventory.py` gets a **minimal** contract — only what `write_release`'s stated dependency and TE §5.1's nine fields require. **Corrected 2026-08-23:** this is **not** an amendment owed — `inventory.py` and `release.py` are the same package, and § Depth names **this stage** as where intra-package shapes are specified. **Superseded:** *"recorded as an amendment owed to `component-methods.md`, not as settled."* The answer letter is unchanged |
| 2 | C | `Station` gains a per-field **provenance** field; `assert_registry_resolved` raises on insufficient *provenance* rather than only on missing *presence*. What provenance G-P1A requires is put to the owner, not defaulted here |
| 3 | D | A **conflict register** records every source value; the registry's value must be identical to one of them (an averaged value matches none); each resolved field records its source and a non-empty rationale; and an **injected averaged value** is tested to be rejected |
| 4 | C | One access row **per artifact opened**, through `acquisition`'s named-accessor routing, plus a **declared audit scope** reconciled against the rows written — so a silently skipped month is detectable rather than producing a wrong figure that looks right |
| 5 | C | The G-P1A decision record carries a verdict **and** the measured hourly and day figure per station-month, each attributed to D-12 or D-2 — **and carries D-2's own disclosure** that the day threshold was set after five months had been seen |
| 6 | D | Four prohibitions, four tests, **each owned by the unit that owns the prohibited act**; prohibition 3 (retrospective split redesign) handled as a **frozen-hash ordering artifact** rather than an injection test; and all four results **named individually** in the G-P1A evidence set |
| 7 | D | The expected schema lives in `configs/data.yaml`; the schema report records **both** the expected schema's digest and the observed values. **D-24's frozen 17-item protected set is not reopened** |
| 8 | C | WS-01 is cited with its boundary stated explicitly — **WS-01 only; WS-02 through WS-08 remain deferred to G-P3A** — and with the reason, so the exception is neither lost nor widened |
| 9 | D | Cell rule and coordinates migrate together, each coordinate carrying its provenance (Q2's mechanism), with the migration emitting a **diff against the notebook literal** asserting no value changed in the move |

**Two answers create obligations outside this unit, stated rather than applied.** Q2 adds a
provenance field to the approved `Station` dataclass — a **cross-package** boundary shape,
so it does owe an amendment; and Q6 places three of its four tests on `features-and-splits`,
`target-standardization` and the units owning those acts. **With `acquisition`'s three, that
is four amendments owed across two units** — raised at the gate as worth one consolidated
change record.

> **Corrected 2026-08-23. Superseded reading, preserved:** *"Three answers create obligations
> outside this unit… Q1 adds an `inventory.py` contract to `component-methods.md`… that is
> five amendments owed to approved stage-2.6 contracts across two units."* Q1's contract is
> **intra-package** and owes nothing — `component-methods.md` § Depth specifies boundary calls
> only and names **this stage** as where intra-package shapes are specified.

**Two answers decline to reach into frozen decisions.** Q7 does not propose an eighteenth
item for D-24's protected set; Q2 does not decide what provenance is sufficient, that
being a §18.2 forbidden-choice item (coordinates: Student; cell rule: Student +
Supervisor).

Carried to the gate, unchanged by these answers: D-1's site-log validation still
outstanding; BLK-07's authorization limb still open, and this unit's December audit runs
through the mechanism it fixes; `RES-01` untested — and **this unit performs the very
permitted read `RES-01` is about**; FR-P1-02-8's missing acceptance row after `TA-29` was
withdrawn; `tests/test_station_registry.py` does not exist; `src/` and `configs/` do not
exist; rule numbering assumed to continue at R-44; G-09 unsigned.

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

### Re-confirmation, 2026-08-23 — after a stage-wide redo jump

A redo jump on `functional-design` reset the receipt floor for every unit of this stage.
No question, option, answer or amendment on this unit changed, and its iteration-2
adversarial verdict was READY with no surviving findings. The summary is re-presented
because the prior confirmation receipt no longer stands.

### Re-confirmation, 2026-08-23 (second) — after a second stage-wide redo jump

A redo jump aimed at correcting `external-products` reset the receipt floor for every unit.
**No question, option, answer or amendment on this unit changed**, and its iteration-2
adversarial verdict was READY with no surviving findings.

### Re-confirmation, 2026-08-23 (third) — after a third stage-wide redo jump, and one applied correction

**No question, option or answer above changed.** One correction was applied to this unit's
artifacts under the cleared receipt.

`component-methods.md` § Depth states: **"Full signatures with types for cross-package
boundary calls. Names and one-line purposes for intra-package functions… Every signature
below is a cross-package boundary."** Its Assumptions add: **"Intra-package helper names are
indicative. `functional-design` (3.1) specifies them per unit."**

`src/data/inventory.py` and `src/data/release.py` are the **same package**, so the absence
of a block for `inventory.py` is that policy, not a gap — and the policy **names this stage
as where the shape is specified**. **Question 1's answer (D) is unchanged**; what changed is
that its output is recorded as this stage's ordinary work rather than as an **amendment
owed**. This unit therefore owes **one** amendment (Q2's `Station.provenance` field, which
modifies an existing boundary dataclass), not two.

### Re-confirmation, 2026-08-23 (fourth) — this file swept to match its own artifacts

**No question, option or answer changed.** The three design artifacts had already been
corrected: `src/data/inventory.py` is **intra-package** (same package as `release.py`), and
`component-methods.md` § Depth specifies **cross-package boundary calls only** while naming
**`functional-design` (3.1)** as where intra-package shapes are specified — so Q1's output
is this stage's ordinary work and **owes no amendment**.

**This file had not been swept with them**, because its receipt was recorded before the
artifact correction was applied. An adversarial pass found it: the Assumptions entry, the
Q1 summary row and the obligations paragraph all still asserted an amendment owed and a
total of "five across two units". All three are corrected here, with the superseded text
preserved. **Corrected total: four owed amendments across two units** — `acquisition` 3,
this unit 1 (Q2's `Station.provenance` field, which modifies an existing boundary
dataclass).

### Re-confirmation, 2026-08-23 (fifth) — after a fifth stage-wide redo jump

A redo jump aimed at `target-standardization` reset the receipt floor for every unit.
**No question, option, answer or amendment on this unit changed.**

**Worth recording here, because the correction was about this unit's rule numbering:**
`target-standardization` had been citing "`inventory-and-registry` R-20" for an open
authority question. This unit's rules run **R-44…R-53** and it has **no R-20**; the rule
carrying that question is **`governance-guards` R-20**. This unit's own **R-49** carries a
related but distinct point — that D-24's protected set is not reopened. **Nothing in this
unit changed**; the misreference was a sibling's. *(Answered `Looks correct`, 2026-08-23;
that receipt belongs to the previous attempt. The live answer tag for this section is the
blank one at its end.)*

### Re-confirmation, 2026-08-24 (sixth) — new stage attempt after the Inception close

**Why this is being re-asked.** Inception closed and Construction opened at
**2026-08-24T11:46:26Z**, starting a fresh `functional-design` attempt and resetting the
receipt floor for every unit. `foundation`, `governance-guards` and `acquisition` have
re-confirmed under this attempt already.

**What changed upstream, and why it leaves this unit's answers untouched.** Two passes ran
on `foundation`, both in `governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md`:
the **amendment pass** (A **declined**; B and C **approved and executed**) and the **sites
9–11 addendum** (three statements still asserting a superseded amendment status, annotated
in place inside `foundation`'s own files).

| What the passes touched | Why this unit is unaffected |
|---|---|
| `component-methods.md` — `DeterminismRecord` **6 → 9** fields (B) | This unit reads `component-methods.md` for `registry.py`'s `Station`, `load_registry` and `assert_registry_resolved`, and for `release.py`'s `write_release`. **`DeterminismRecord` is not among them** |
| `services.md` **§ Run record and registry** — two → three release artifacts (C) | This unit reads **§ The nine stage scripts** and **§ Stage entry contract**. Not the amended section |
| `unit-of-work.md` **§ 1** `Owns` — ledger named (C) | This unit reads **§ 4**. Not the amended section |
| The sites 9–11 annotations | All three are inside `foundation`'s own artifacts and annotate a superseded **status**; no contract, rule or entity changed |
| Amendment **A** — **declined** | **No count moved.** This unit's 7 requirements and **2** with no acceptance row stand; it still owns WS-01, TA-04, TA-25 and supports WS-18, TA-18, TA-32 |

**One adjacency named rather than assumed away.** `write_release` sits next to Amendment C
— C added the release-history ledger and `foundation`'s W-7 label-allocation step. Checked
directly rather than inferred: `write_release`'s signature in `component-methods.md` is
**unchanged**, and the clause this unit actually depends on — that `source_files`' six items
are validated against `inventory.py` — is intact. **R-11 is likewise unchanged**: the
content hash stays authoritative and the label is a citation device.

**Its other upstreams, also unchanged.** `acquisition` **R-32** and **R-33** (the
named-accessor routing this unit's December audit must use) and `governance-guards`
**R-25**, **R-26**, **R-28**, all re-confirmed earlier today with no rule changed.

**What still stands.** Every answer, and everything carried to the gate: **FR-P1-02-8's
replacement acceptance row** open after TA-29's withdrawal; **D-24's protected set not
reopened**; **G-09 unsigned**, so nothing here authorises creating `src/data/inventory.py`,
`src/data/registry.py`, `scripts/01_inventory_and_registry.py` or
`tests/test_station_registry.py`. The § Review verdict of **READY** — with its one Major
finding about this file's own § Assumptions and § Consolidated Summary — belongs to the
previous attempt.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The receipt is recorded for `inventory-and-registry` under this attempt and its three artifacts are re-saved. No answer, contract, count or scientific value changes.

- Request changes
   > **Impact**: No receipt is recorded and nothing is re-saved. Tell me what to change and I re-present first.

> **💡 Recommendation**: **Looks correct** — every amended section is one this unit does not read, the `write_release` adjacency was checked directly and holds, and Amendment A's decline moved no count.

*(Answered `Looks correct` earlier on 2026-08-24; that receipt was reset by the authorised redo jump below. The live answer tag for this section is the blank one at its end.)*


### Re-confirmation, 2026-08-24 (post-redo) — receipt floor reset by an authorised redo jump

**Why this is being re-asked, and it is not about this unit.** The project decision owner
authorised a **redo jump on `functional-design`** at **2026-08-24T14:57:07Z**, so that three
standing reviewer findings on **`models-and-baselines`** (unit 8) could be fixed and
re-reviewed — its adversarial budget had been exhausted at NOT-READY, and the write-freeze on a
terminal review receipt made a redo the only route to a fix. **A redo resets the receipt floor for
every unit of the stage**, which is the stated cost that was accepted when the redo was chosen.

**Nothing in `inventory-and-registry` changed.** No question, option, answer, amendment, rule, entity or
workflow of this unit was touched after its earlier confirmation today. The only artifacts edited
after the redo are `models-and-baselines`'s; its three fixes are confined to its own
files and reach no contract this unit consumes.

**The redo bought what it was for.** `models-and-baselines` returned **READY** on the
second pass of the restored budget, after three further Major findings were fixed. Two residuals
ride that READY verdict and are carried to the stage gate rather than applied.

**Everything this unit carried to the gate still stands, unchanged**, as recorded above.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The receipt is recorded for `inventory-and-registry` under the post-redo floor and its three artifacts are re-saved. No answer, rule, entity, count or scientific value changes.

- Request changes
   > **Impact**: No receipt is recorded and nothing is re-saved. Tell me what to change and I re-present first.

> **💡 Recommendation**: **Looks correct** — this unit is untouched; the reset is a mechanical consequence of a redo taken for a different unit, and that redo achieved what it was authorised for.

*(Answered `Looks correct`, 2026-08-24T15:26:17Z. That receipt was reset by eleven authorised stage-wide redo jumps, all taken for other units, the last at 2026-08-25T17:21:15Z. The live answer tag is the blank one at the end of this file.)*

### Re-confirmation, 2026-08-25 — after eleven receipt-floor resets taken for other units

**Nothing in `inventory-and-registry` changed.** Verified: **7** requirements derived (2 bold/untested:
FR-P1-02-7, FR-P1-02-8), **3** acceptance rows (WS-01, TA-04, TA-25), BLK-07 named, **zero**
Amendment C contamination in all four files. One observation disclosed rather than re-litigated:
WS-01 sits in §16.1's G-P3A set, but the approved `unit-of-work.md` § 4 declares it for this unit
and these artifacts mirror the approved contract.

**One gap, the same cross-unit class as units 2 and 3:** `AuditScopeError`, `SchemaError` and
`InventoryError` are unit-local exceptions with no stated base. Proposed edit after this receipt,
and only this: the standard base-class box — all derive from **`IntegrityError`** under
`foundation` R-01's *"any future integrity-related exception"* clause, with the declaration site
deferred to the same OPEN item as the previous units. Then the reviewer runs.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: Receipt recorded, base-class box applied, artifacts re-saved, reviewer runs.

- Request changes
   > **Impact**: No receipt, nothing edited. Tell me what to change and I re-present first.

> **💡 Recommendation**: **Looks correct** — unchanged and verified clean; the single edit is the same obligation the previous units discharged.

*(Receipt reset by the twelfth authorised redo, 2026-08-26T05:43:39Z, taken for THIS unit's terminal findings. The live answer tag is the blank one below.)*

### Re-confirmation, 2026-08-26 — the terminal pass's five findings, fixed at every named site

The terminal pass found my fixes had again landed on a subset of named sites. This time all mirrors applied: the record-timestamp membership rule + negative control now in **R-50** and **DE § 6** (not only W-6); the two `inventory.py` obligations + controls in **R-44** and **DE § 1** (not only W-1); the "assigned to no other unit" overreach **retracted**; the `suffix_mismatch` surfacing flagged **⚠ PROPOSED**, deferring to stage 3.2's resolution of `acquisition` R-34's Open item; the false "No rule changed" box corrected; CHOSEN→NAMED terminology aligned. Counts unchanged: 7/2/3.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: Receipt recorded, artifacts re-saved, reviewer runs iteration 1 of the fresh budget.

- Request changes
   > **Impact**: Nothing recorded; tell me what to change.

> **💡 Recommendation**: **Looks correct** — every named site is now covered and the one cross-unit conflict is deferred to its owner rather than silently answered.

*(Receipt reset by the fourteenth authorised redo, 2026-08-26T08:18:34Z. The live answer tag is the blank one below.)*

### Re-confirmation, 2026-08-26 — under the fourteenth-redo floor

**One repair to THIS file, none to the design artifacts**: my earlier perl edits had re-encoded this question file latin-1→UTF-8 on each save, layering mojibake across ~146 lines — unreadable exactly where a human reads it, while every ASCII engine token survived so nothing downstream reported it. Repaired 2026-08-26 by iterative latin-1 reversal, verified line-by-line: the header, all 13 💡 Recommendation markers and every em-dash/§ read cleanly again. The three design artifacts were never corrupted. Floor also reset by the fourteenth redo.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: Receipt recorded, artifacts re-saved, review runs (narrow confirm for unchanged units; confirming pass for external-products).

- Request changes
   > **Impact**: Nothing recorded; tell me what to change.

> **💡 Recommendation**: **Looks correct** — mechanical for the unchanged units; for the two repaired question files the repair restores what a gate reader needs and touches no specification.

[Answer]: Looks correct
