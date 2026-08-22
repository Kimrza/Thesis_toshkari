# Functional Design Questions — `governance-guards`

**Unit** `governance-guards` — the runtime prohibitions that must hold before any
scientific work runs, plus the contract that closes Phase 1.
**Kind** `library` · **Complexity** M · **Deployment** shared · **Depends on** `foundation`.

This is unit **2 of 12** in the Functional Design pass, and it is the most
governance-sensitive unit in the plan: it owns the **only** code path into the
locked December root, the phase-boundary prohibition, and the Phase 1 → Phase 2
transition manifest.

**Nothing here decides a scientific value.** Every question is about *mechanism* —
how a hash is computed, where a list is asserted, what aborts a read. The 17
protected items are frozen by **D-24**; this stage does not reopen them.

**G-09 is not signed.** `src/data/phase_contract.py`, `src/data/locked_test.py` and
`src/data/reuse_registry.py` **do not exist**. BLK-01 closed 2026-08-22 granting
**authority only** — authority to name a module is not authority to write one.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 2 `governance-guards` — the `Owns` list, the boundary, the 10 requirements carried, and BLK-06/BLK-07.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2. **Derived, not reasoned:** 10 requirements, **1** with no acceptance row (FR-P1-02-6); tested by TA-07 TA-08 TA-12 TA-18 TA-27 TA-28 WS-10 WS-18; **owns** TA-27 and TA-28; **supports** TA-07, TA-18 and WS-18. Cross-checked against that file's own § Per-unit coverage summary, which agrees.
- `../../../inception/requirements-analysis/requirements.md` — REQ-ENG-5; FR-P1-02-6; FR-P1-03-2; FR-P1-05-12; FR-P1-06-1 through -4; NFR-PHASE-01; NFR-LIC-01.
- `../../../inception/application-design/component-methods.md` — the approved contracts for `phase_contract.py` (`assert_phase_boundary`, `assert_no_raw_fields`, `TransitionManifest`, `build_transition_manifest`, `diff_protected_hashes`) and `locked_test.py` (`RESTRICTED_ROOT`, `AccessRecord`, `open_restricted`, `assert_no_december_outside_restricted`).
- `../../../inception/application-design/component-dependency.md` § Shared resources — the unqualified carve-out: *"nothing else may construct a path into it."*
- `evidence/DECISIONS.md` **D-24** — the canonical protected set: **17 items**, each with a governing artifact and a hashable representation. **D-15** — the relocation of 21 December-bearing files into the restricted root.
- `../../../inception/delivery-planning/bolt-plan.md` § Gate 0 — the permitted/barred boundary before G-09, and the owner's `DP-CHAIR-02` ruling on what functional design may do with an open blocker.
- `../foundation/functional-design/` — unit 1's `IntegrityError` base (R-01), its two-tier error posture, and its `ConfigSnapshot` contract, all of which this unit builds on.
- Absent by scope design: `stories` (2.4 `SKIP`), `mockups` (1.6 and 2.5 `SKIP`). `kind: library`, no user-facing surface, so `frontend-components.md` is not produced.

## What the owner's ruling permits this stage to do with BLK-06

Quoted from `bolt-plan.md` § Gate 0, the `DP-CHAIR-02` ruling:

> Functional design **may begin** while BLK-05 and BLK-06 remain open, **but only
> to analyze those blockers and generate the evidence required for their
> resolution**. Both blockers are presented to the owner with options, supporting
> evidence, risks and a recommendation. **Neither is marked resolved and no
> approval is assumed until the owner explicitly decides.**

**BLK-06's limb status, as the register records it:** the *enumeration* limb is
**RESOLVED** by D-24 at 17 items with the cardinality calculated rather than
assumed. What remains **PENDING** is the **per-item binding to concrete config
fields and file paths** — and the register notes that none of the four config files
or six `src/` packages exists yet. Questions 1 through 3 below produce exactly that
binding evidence. **They do not close BLK-06.**

---

## Question 1

**Eight of D-24's 17 items hash a "config-section"** — items 4, 5, 6, 7, 9, 11, 14, 16. Nothing defines what a section *is*, or how its hash survives a change that alters no value.

> **⚠ THE PREMISE OF THIS QUESTION WAS WRONG, AND THE QUESTION IS PRESERVED AS
> ASKED.** Corrected 2026-08-22 after an adversarial review traced the miscount to
> this line. **Six** items are typed `Config-section hash` — **4, 7, 9, 11, 14, 16**
> — and items **5** and **6** are typed **`Field hash`**, a different mechanism.
> Derived:
> `awk -F'|' '... && $5 ~ /Config-section hash/ {print $2}'` → `4 7 9 11 14 16`;
> `... /Field hash/` → `5 6`.
>
> **The answer below is unaffected.** The question asked *how a config-section hash
> is defined*, and the choice between a byte digest, a canonical serialization and a
> per-item key list does not depend on how many items use it. Option D remains the
> answer for the six that do.
>
> **What the miscount did cost** is now recorded: it caused the artifacts to fold
> items 5 and 6 into the section contract, and fixing that surfaced the wider gap —
> D-24 uses **six** hashable-representation kinds and the first issue of the artifacts
> defined **one**. The full taxonomy is `business-logic-model.md` § W-3a and the
> field-hash contract is § W-3b.

This is the question that decides whether G-P3C is usable: a config-section hash that changes when someone reflows a comment will fail the freeze spuriously, and a team that learns to expect spurious failures stops treating a real one as real.

How is a config-section hash defined?

A) Hash the raw bytes of the section as it appears in the file
   > **Impact**: Trivial to implement and impossible to argue with. But it changes on a comment edit, a key reorder, a quote-style change or a trailing-whitespace fix — none of which alters a governed value. G-P3C would fail on formatting, and the failure would be indistinguishable from a real protected-value change.

B) Hash a canonical serialization of the parsed section — keys sorted, comments dropped, scalars normalised
   > **Impact**: Stable against every formatting change and sensitive to every value change, which is exactly the required behaviour. Costs a canonicaliser that must itself be frozen, because changing *how* you canonicalise changes every hash — so the canonicaliser's own version belongs in the manifest.

C) Hash an explicit field list per item — each protected item names the exact config keys it covers
   > **Impact**: Most precise and most auditable: a reviewer can see exactly which fields item 9 protects. But it is a hand-maintained list per item, which is the `DP-DATA-01` failure mode — a field added to a grid and not added to the list is silently unprotected.

D) B for the hash, plus C as an asserted completeness check — canonical serialization hashed, with a per-item key list asserted to cover the section
   > **Impact**: Stability from B and auditability from C, with the list's completeness machine-checked rather than trusted. Costs both mechanisms and one reconciling test.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D, with the canonicaliser version recorded in the manifest. A raw-byte hash (A) would make the phase freeze unusable in practice, and C alone reintroduces exactly the silent-gap failure this project has now corrected four times. D costs one extra test and buys a freeze that fails only when something real changed — which is the whole point of G-P3C's empty-diff pass condition.

[Answer]: D — canonical serialization hashed (keys sorted, comments dropped, scalars normalised), with a per-item key list asserted to cover the section, and the canonicaliser's own version recorded in the manifest.

---

## Question 2

`build_transition_manifest` must hash all 17 protected items. **Right now none of the governing artifacts exists** — no config file, no `src/` package, no run record. Later, some items will be legitimately absent at a given moment: Phase 2 grids during Phase 1, selected hyperparameters before tuning has run.

What does the manifest do about an item whose governing artifact is absent?

A) Raise — a manifest that cannot hash all 17 items is not a manifest
   > **Impact**: Strongest guarantee at the freeze, and the freeze is the only moment that matters for G-P3C. But it makes the manifest unbuildable at every earlier moment, so it cannot be exercised, tested or demonstrated until the very last Bolt — and a mechanism first run at a freeze gate is a mechanism first debugged at a freeze gate.

B) Record the item with an explicit `absent` sentinel, and raise only when the manifest is built *for a freeze*
   > **Impact**: Buildable and testable from Bolt 2 onward, with the full guarantee retained where it counts. Requires a build mode — draft versus freeze — which is a distinction that must be recorded in the manifest itself so a draft can never be mistaken for a freeze.

C) Record `absent` always, and let `diff_protected_hashes` treat `absent → present` as a difference
   > **Impact**: Uniform and simple, no build modes. But then nothing prevents freezing a manifest with sixteen `absent` entries, and the empty-diff pass condition becomes satisfiable by a manifest that protects nothing.

D) B, plus the freeze-mode build additionally asserting the key list equals D-24's 17 items
   > **Impact**: Closes the last gap — C's failure mode is a *short* list, and only an explicit cardinality-and-membership assertion catches it. This is what `component-methods.md` already demands when it says the key list is asserted equal to the canonical set "so a short list cannot pass silently".

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. The approved design already requires the key-list assertion; B alone leaves it unstated, and C actively defeats it. The draft/freeze distinction is worth its cost because it lets the transition manifest be exercised eleven Bolts before it is relied on — and this project's affirmed posture is that reproducibility and determinism are *executable*, not asserted.

[Answer]: D — record an absent item with an explicit `absent` sentinel so the manifest is buildable and testable from Bolt 2 onward; raise only when the manifest is built **for a freeze**; record the build mode (draft versus freeze) in the manifest itself so a draft can never be mistaken for a freeze; and have the freeze-mode build additionally assert the key list equals D-24's 17 items, so a short list cannot pass silently.

---

## Question 3

`diff_protected_hashes` returns the differing keys, and an empty mapping is the **G-P3C pass condition**. `component-methods.md` carries a standing caution: until BLK-06 is discharged, *"an empty `diff_protected_hashes` result must not be read as proof that no protected item changed."*

Where does the authoritative 17-item list live, so that assertion has something to check against?

A) A literal in `phase_contract.py`
   > **Impact**: Adjacent to the code that uses it and versioned with it. But it is a scientific-governance list in source, and `project.md` § Forbidden prohibits hiding a scientific constant in source code — the 17 items are a governed enumeration, not an implementation detail.

B) In `configs/experiment.yaml`, read via `ConfigSnapshot`
   > **Impact**: Governed, versioned, hashable, and reachable through the existing config path. Consistent with the rule that every scientific constant lives in one of the four config files. But item 12 protects `seeds.yaml` and item 9 protects `experiment.yaml` itself — so the protected-set list would live inside a file it protects, which is circular unless the list is excluded from its own section hash.

C) Derived at run time from D-24 by parsing `evidence/DECISIONS.md`
   > **Impact**: Single source of truth, and D-24 is the actual authority. But it makes a governance prose document a runtime dependency and a parse target, and a decision record's formatting is not a stable interface.

D) B with the circularity resolved explicitly — the list in `configs/experiment.yaml` under a section excluded from item 9's hash, with a test asserting the exclusion
   > **Impact**: Keeps the list governed and hashable while making the one genuine circularity a named, tested exclusion rather than a latent bug. Costs stating the exclusion in two places — the config and the test — which is exactly where a reviewer would look for it.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A is barred by `project.md` § Forbidden. C turns a decision record into a runtime parser target, which will break the first time someone reformats a table. D is B with the circularity handled openly instead of discovered later — and the circularity is real: without the exclusion, adding an item to the list changes the hash of the section that holds the list.

> ⚠ **THE RECOMMENDATION ABOVE IS WRONG AND WAS REJECTED BY THE PROJECT DECISION
> OWNER.** It is preserved unedited because the reasoning error it contains is the
> substance of the correction below. **Do not implement option D as recommended.**

[Answer]: **B, modified — MODIFY, not approval.** The project decision owner rejected the recommended option D and directed the following, which governs:

**Ordinary self-protection is not circularity.** `configs/experiment.yaml` stores **only the authoritative 17 protected-item identifiers**, and the resulting config-section digest is stored **externally, in the transition manifest**. Changing the list therefore simply produces a new digest — **that is correct behaviour and must not be described as a circularity.** A change to the protected-set enumeration is a governed change requiring a Vision §15.2 amendment and a D-number, so it *should* be visible as a manifest difference.

**A genuine self-referential digest is a different case, and gets a narrow rule.** If the hashed section ever stores its **own expected digest**, define an explicit canonicalization rule that removes or normalizes **only the self-referential digest value** — nothing else.

**The complete protected-item list is hashed.** It must **not** be excluded from hashing merely to avoid circularity. Excluding it would leave the enumeration that defines what is protected as the one thing unprotected.

**Required tests**, proving the canonical contract handles each case:

| Mutation | Required behaviour |
|---|---|
| **Deletion** of a protected key | Digest changes **and** the freeze-mode cardinality/membership assertion fails |
| **Addition** of a key | Digest changes **and** the membership assertion fails against D-24's 17 |
| **Duplication** of a key | Rejected — D-24's cardinality of 17 is *calculated from the enumeration*, so a duplicate is a malformed set, not a longer one |
| **Reordering** where semantically irrelevant | Digest **unchanged** — the 17 items are a set, and Q1's canonical form sorts keys |
| **Renaming** a protected key | Digest changes **and** the membership assertion fails, because the name is the identifier |
| Frozen manifest contents | Contains **exactly** the D-24-authorized 17-item set — no more, no fewer, no duplicates |

> **Why the recommendation was wrong, recorded rather than quietly replaced.** It
> conflated *the list living in a file that contains protected sections* with *the
> list living inside the section whose digest it determines*. D-24's five
> `experiment.yaml` items each hash a distinct section — item 5 the history-window
> field, item 9 Grids, item 11 Optimizer/loss policy, item 14 Statistical
> configuration, item 16 Reporting hierarchy — and **none** of them covers a
> `protected_set` section. With the digest stored in the manifest rather than in the
> section, there is no self-reference to resolve. The recommendation then compounded
> the error by proposing to **exclude the enumeration from hashing**, which would
> have left the list that defines the protected set as the only unprotected thing in
> it. This is a **design** error, not a citation error, and it is the fifth
> substantive error of this working session.

---

## Question 4

**FR-P1-02-6 is this unit's one requirement with no §16 or §19 acceptance row** — derived from story-map Table 1, and it is the regression guard `assert_no_december_outside_restricted` implements after D-15 relocated 21 December-bearing files.

The stakes are specific: `project.md` § Forbidden states **"NEVER derive fold or partition membership from an acquisition directory name or a filename"**, after a year-blind predicate filed locked-month records into `audit_evidence_2022-01/`. So what identifies a "December-bearing artifact"?

A) Filename and directory-name pattern matching
   > **Impact**: Fast and needs no parsing. But it is precisely the mechanism `ML-07` forbids and the one that already failed in this project — a December record inside `audit_evidence_2022-01/` is invisible to it, which is the exact case that produced the rule.

B) Content scan — parse each artifact and inspect observation dates
   > **Impact**: Asserts on record dates, which is what the rule requires. Catches the misfiled case that defeated the name-based predicate. Costs parsing every artifact under `evidence/`, and needs a defined behaviour for a file it cannot parse.

C) B, with an unparseable file treated as a **failure** rather than a pass
   > **Impact**: Closes the gap B leaves. An artifact the guard cannot read is exactly where a December record would hide, so treating it as clean is the one answer that cannot be defended. Costs occasional friction on a genuinely irrelevant unparseable file, resolved by an explicit recorded exclusion rather than by silence.

D) C, plus retaining the name-based check as an additional signal that never substitutes for the content scan
   > **Impact**: A name-based hit is cheap early warning; keeping it as a *supplement* costs nothing and catches an obvious mistake fast. The risk is that a future maintainer reads the presence of the name check as sufficient — so its subordinate status has to be stated where the code lives, not only here.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. It satisfies the rule exactly and its unparseable-equals-failure clause closes the only hiding place. D's supplementary name check is defensible and I would not argue against it, but this project has now been bitten four times by a mechanism whose weaker half got mistaken for the whole — and adding a weaker half here buys speed the guard does not need.

[Answer]: C — identify a December-bearing artifact by **content scan on observation dates**, never by filename or directory name, and treat an artifact the guard **cannot parse as a failure** rather than a pass. An unreadable file is exactly where a December record would hide, so a recorded explicit exclusion is the only way past it.

---

## Question 5

`open_restricted` writes the access record **and flushes it** before returning the path, and **raises when the registry write fails** — *"a failed log write must abort the read, not proceed unlogged."* The ordering is the requirement (`VAL-2`, FR-P1-02-3): an access recorded after the fact **fails** the ordering check rather than satisfying it.

How is log-before-read *proven* rather than intended?

A) Code review of the call order
   > **Impact**: Zero machinery. But the ordering is the single most governance-critical sequence in the project, and "we looked at it" is the evidence class this project's affirmed methodology explicitly rejects in favour of executable guards.

B) A test that patches the log writer to fail and asserts the read never happens
   > **Impact**: Proves the abort limb directly, which is the limb that matters — an unlogged read is the breach. Straightforward to write against a synthetic restricted root.

C) B, plus a test asserting the log row is durable on disk before the read is attempted
   > **Impact**: Proves both limbs — abort-on-failure *and* flush-before-read. The second is what distinguishes this contract from one that logs and reads in the same buffered transaction, where a crash loses the row and keeps the read.

D) C, plus an ordering assertion in the access log itself — every row carries a timestamp, and the guard records read-completion separately so the interval is visible
   > **Impact**: Strongest, and it makes a retrospective row detectable in the log rather than only preventable in code. But `experiment_registry.md` already records five retrospective rows from before this guard existed, so the log will contain both kinds and the distinction must be explicit rather than inferred from ordering alone.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. It proves both limbs of the stated contract with two tests and no new fields. D is attractive but its extra value is detecting a violation the code already makes impossible, and it would add a field to a log that already carries retrospective rows — the interpretation burden outweighs the gain. If you want D, the retrospective rows need an explicit marker first.

[Answer]: C, with the ordering stated as a hard precondition — **the access-log append must be durably completed before the December read begins.** A log-write failure **or** a durability failure must **prevent the read**, not merely be reported alongside it. Two tests: patch the log writer to fail and assert the read never happens; and assert the log row is durable on disk before the read is attempted. Log-then-read is the requirement (`VAL-2`, FR-P1-02-3) — an access recorded after the fact fails the ordering check rather than satisfying it.

---

## Question 6

`assert_phase_boundary` (the **import** limb) and `assert_no_raw_fields` (the **produced-field** limb) are, per the approved design, *"separately checkable per FR-P1-03-2's requirement of two independent results"*, and **"neither substitutes for the other."**

The import limb has a defined call site — step 4 of the stage entry contract. The field limb does not.

Where does the produced-field limb run?

A) At every artifact write, inside the release API
   > **Impact**: Universal coverage with one call site — nothing reaches disk unchecked. But it puts a Phase 1 prohibition inside `foundation`'s release path, which inverts the dependency: `governance-guards` depends on `foundation`, not the reverse, and the reverse edge would close a cycle.

B) At each producing stage script, before it writes
   > **Impact**: Respects the dependency direction and keeps the check near the producer that knows its own frame. But it is a per-script obligation, so a new script that forgets it is silently unchecked — the list-versus-rule problem again.

C) B, with a completeness test asserting every Phase 1 producing script calls it
   > **Impact**: Keeps the direction correct and makes the omission a test failure rather than a silent gap. Costs a test that enumerates the producing scripts, which must itself stay current — but it fails loudly when it does not.

D) At the phase-transition manifest build, over every Phase 1 artifact at once
   > **Impact**: One call site, no per-script obligation, and it runs where the freeze happens. But it catches a violation only at the *end* of Phase 1, after every artifact is written and possibly after downstream work has consumed the contaminated frame.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A inverts the dependency and would close a cycle the unit design deliberately avoids; D detects the breach too late to be a guard rather than a post-mortem. C is B with the gap closed, and its enumerating test is the same shape as the `RequiredFieldsMap` completeness assertion `foundation` already adopted — one pattern, used twice.

[Answer]: C — the produced-field limb runs at each producing stage script before it writes, with a completeness test asserting that every Phase 1 producing script calls it. This keeps the dependency direction correct (`governance-guards` depends on `foundation`, never the reverse, which would close a cycle) and makes an omission a test failure rather than a silent gap.

---

## Question 7

The §10.1 reuse register carries **all fifteen fields** and must be recorded **before the code is used** and before gate G-P2. `NFR-LIC-01` is accepted by **TA-28**, which this unit owns.

"Before the code is used" is an ordering claim. How is it enforced?

A) Procedural — the register is filled in when a developer copies code
   > **Impact**: Matches how such registers usually work. But it is unenforced, and the register's whole purpose is licence compliance, where an unrecorded copy is the failure mode with legal consequences rather than merely audit ones.

B) A test asserting every third-party-derived module has a register entry
   > **Impact**: Machine-checkable. But it needs a way to know a module *is* third-party-derived, which is the hard part — an unregistered copy is indistinguishable from original work by inspection.

C) B, keyed on a mandatory provenance marker every adapter module must carry
   > **Impact**: Makes the check tractable: the register is asserted complete against the set of modules carrying the marker, and a module without the marker is asserted to contain no reuse. Costs a convention that must be followed — but the convention's absence is itself detectable at review.

D) C, plus the standing default recorded as the primary control: reimplement from the paper with a citation rather than copy
   > **Impact**: The strongest position, and it matches the affirmed rule already in `project.md` § Forbidden — copying source whose licence is absent, ambiguous or incompatible is prohibited, and reimplementation is the standing default while the AGPLv3 question is open. Under D the register becomes the exception path rather than the expected one.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. The project already has a standing rule that makes reimplementation the default and copying the exception; designing the register as the *exception* path rather than the main road reflects the rule that is actually in force. The AGPLv3 Global-TEC-forecasting repository remains the only approved direct-copy source, and whether its distribution obligations permit that copying is an **unresolved governance dependency this project does not settle** — which is a reason to make copying deliberately harder to reach.

[Answer]: D — a test asserting every third-party-derived module has a register entry, keyed on a mandatory provenance marker every adapter module must carry, with a module lacking the marker asserted to contain no reuse; **and** the standing default recorded as the primary control: reimplement the published method from the paper with a citation rather than copy. The register is the **exception** path, not the expected one. The AGPLv3 Global-TEC-forecasting repository remains the only approved direct-copy source, and whether its distribution obligations permit that copying is an unresolved governance dependency this project does not settle.

---

## Question 8

**BLK-07** records that `acquisition`'s routing through `open_restricted` was not captured, while `component-dependency.md` § Shared resources states without qualification that *"nothing else may construct a path into it."* Four downstream consumers reach the restricted root through this unit's contract: `inventory-and-registry`, `acquisition`, `features-and-splits`, `evaluation-and-comparison`.

How does this unit's design treat the single-chokepoint rule?

A) State the rule and rely on the four consumers to honour it
   > **Impact**: Minimal, and consistent with the rule living in the design rather than the code. But D-15 records *why* the boundary matters: it is a **governance boundary, not an access control**, so it holds only while exactly one code path reaches it — and a rule that depends on four units remembering is not "exactly one path".

B) A static check asserting no module outside `locked_test.py` contains the restricted-root literal
   > **Impact**: Makes the single-path claim machine-checkable across the whole tree, and it is cheap — a grep-class assertion. Catches the accidental second path, which is the realistic failure. Does not catch a path assembled at run time from fragments.

C) B, plus `open_restricted` raising when its own caller is not one of the four recorded consumers
   > **Impact**: Closes the run-time-assembly gap too. But it makes the guard depend on knowing its callers, which couples this root unit to four downstream units and is the coupling the DAG design was arranged to avoid.

D) B, plus BLK-07 raised at this stage's gate as an open item with the four consumers enumerated — not closed here
   > **Impact**: Gets B's enforcement while keeping BLK-07 where it belongs: an open blocker whose resolution is the owner's, since it concerns which units are authorised to reach the locked month. Nothing about it is silently settled by a design document.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. B is the right mechanism and C's extra coverage costs the acyclic dependency structure that keeps this unit a root — a high price for a failure mode (run-time path assembly) that the static check plus code review makes unlikely. BLK-07 is an authorisation question, not a design question, so it goes to the gate rather than getting resolved in an artifact.

[Answer]: D — a static check asserting no module outside `locked_test.py` contains the restricted-root literal, **plus BLK-07 raised at this stage's gate as an open item** with its four consumers enumerated (`inventory-and-registry`, `acquisition`, `features-and-splits`, `evaluation-and-comparison`).

**BLK-07 stays OPEN until the project decision owner receives and approves the specific authorization decision.** Accepting the design mechanism is **not** authorization to open locked December data, and nothing in this unit's artifacts may be read as granting it. The authorization question — which units are authorised to reach the locked month — is the owner's, not a design document's.

---

---

# Step 4 ambiguity analysis

**No answer is vague, and no answer contradicts another.** Two readings had to be
settled and one genuine gap remains open rather than invented.

## Interpretation 1 — Q1's per-item key list and Q3's 17 identifiers are ONE structure

Q1 = D requires *"a per-item key list asserted to cover the section"*. Q3 requires
`configs/experiment.yaml` to hold *"only the authoritative 17 protected-item
identifiers"*. Read carelessly these are two lists, and conflating them is exactly
the mistake that produced the rejected Q3 recommendation.

**Settled as one structure**, because it is the only reading under which both
answers hold simultaneously: a single governed mapping from **protected-item
identifier → the config keys or artifact paths that item covers**. The 17 keys of
that mapping are Q3's identifiers; its values are Q1's per-item coverage lists.

**Consequence, stated so it is not lost:** Q3's rule that the complete
protected-item list is **hashed and never excluded** applies to the whole mapping,
values included. A per-item coverage list that drifted while the identifier stayed
put would otherwise be an unprotected change to what "protected" means.

## Interpretation 2 — the list-plus-completeness-test pattern, now used three times

Q1's per-item key list, Q6's producing-script list, and `foundation`'s
`RequiredFieldsMap` all follow one shape: **a declarative list whose completeness
is asserted by a test, never trusted.** Recorded as a deliberate repetition rather
than three coincidences, because the shared failure it defends against —
`DP-DATA-01`'s silently-exempting list — is the same in all three.

## Open, and deliberately not answered here

**Where does the test that asserts the frozen manifest contains exactly D-24's 17
items get D-24's list from?** The chain is: manifest keys ← `experiment.yaml`'s
mapping ← D-24. Q2's freeze assertion and Q3's required test both compare against
**D-24**, not merely against the config — which is correct, and is what stops the
config and the manifest agreeing with each other while both drift from the
authority.

But the test needs D-24's 17 items from somewhere, and both available routes have a
cost already identified in this file:

- **Hardcode them in the test** — a fourth copy of a governed enumeration, and this
  session has spent its length correcting exactly that class of duplication.
- **Parse `evidence/DECISIONS.md`** — makes a governance prose document a test
  dependency and a parse target, which Q3 option C was rejected for.

**No third option is invented here.** The gap is real, it is narrow, and it is
raised at the approval gate for the owner to direct rather than resolved by
preference. Until it is settled, the test asserting D-24 conformance cannot be
specified completely — and that is stated rather than papered over.

---

# FR-P1-02-6 — explicitly untested, and it stays that way

`FR-P1-02-6` is this unit's **one requirement with no §16 or §19 acceptance row**,
derived from story-map Table 1 and cross-checked against the § Per-unit coverage
summary. It is the regression guard `assert_no_december_outside_restricted`
implements after **D-15** relocated 21 December-bearing files into the restricted
root.

**On the project decision owner's explicit direction, it is preserved as an
explicitly untested obligation until an approved acceptance row exists AND its test
has passed.** Both conditions, not either.

Consequently, and binding on every artifact this unit produces:

- Q4's content-scan design is a **test specification only** — *not an approved
  acceptance row and not evidence of a passing result.*
- No artifact, manifest or report may state or imply that FR-P1-02-6 is covered,
  satisfied, or verified.
- Designing the guard does not test it. Implementing it does not test it. Only an
  approved row plus a passed execution does, and neither exists.

---

# Pending governed amendments — presented, NOT applied

## Amendment D — the stale BLK-06 text in two approved artifacts

**Recorded on the project decision owner's explicit direction: raise the required
governed correction with preserved provenance; do not edit the approved artifacts
silently.**

**What is true now.** **D-24** (2026-08-22, approved by the project decision owner
under the recorded authority equivalence) resolved BLK-06's **enumeration limb** at
**17 items**, with the cardinality *calculated from the enumeration* (14 carried
forward + 3 added) rather than assumed. The blocker register records the
enumeration limb `RESOLVED 2026-08-22 — 17 items`.

**What two approved artifacts still say.** Both carry text written before D-24 and
now superseded:

| Artifact | Stale text, quoted | Status |
|---|---|---|
| `../../../inception/application-design/component-methods.md` — `TransitionManifest.protected_hashes` comment | *"Final enumeration and cardinality are DEFERRED TO STAGE 3.1; this design states neither. See BLK-06"*, and in the surrounding prose *"The final enumeration and its cardinality are deferred to stage 3.1 (`functional-design`); this design states neither, and no number is carried into this artifact."* | **Superseded by D-24.** Stage 2.6 artifact, approved |
| `../../../inception/units-generation/unit-of-work.md` § 2 `governance-guards` | *"whose **final enumeration and cardinality are deferred to stage 3.1** (`functional-design`) — this artifact states neither, and **BLK-06** carries the obligation"* | **Superseded by D-24.** Stage 2.7 artifact, approved |

**Provenance preserved.** Both statements were **correct when written** — they
predate D-24 and were deliberately careful not to invent a cardinality, which is
why they say "states neither" rather than guessing. The correction is that the
deferral they describe has since been discharged for the enumeration limb. What
remains genuinely deferred to this stage is the **per-item binding to concrete
config fields and file paths**, which the register still records as `PENDING`.

**Not applied.** Both are approved-stage artifacts. `CHANGE_RECORD_PROCEDURE.md`
§ "Files a sweep may not edit" reserves a completed stage's artifacts absent owner
approval for annotate-in-place, and the `GOV-2026-08-22-INC-01` Rec 7 precedent is
the route if the owner grants it. **Neither file is edited by this stage.**

**Class.** Approved AI-DLC artifact annotation — *not* a Vision §15.2 amendment.
§15.2 governs the authority documents; D-24's consequent FR-P1-06-1 amendment
(14 → 17) already went through §15.2 and is recorded there.

**Consequence if left unapplied.** A reader of either artifact concludes the
canonical set has no established cardinality, and `component-methods.md`'s standing
caution — *"an empty `diff_protected_hashes` result must not be read as proof that
no protected item changed"* — reads as still fully in force when its enumeration
half has been discharged. That caution's **remaining** half is real and is carried
forward: the per-item binding is pending, so an empty diff is still not proof.

## Amendment E — BLK-07 authorization, the owner's alone

**BLK-07 stays OPEN.** Per the owner's explicit direction: **acceptance of the
design mechanism in Question 8 is not authorization to open locked December data.**

The four consumers reaching the restricted root through `open_restricted` are
`inventory-and-registry` (pre-G-05 coverage audit), `acquisition` (the D-9 input
and any December re-acquisition — the unrecorded routing that *is* BLK-07),
`features-and-splits` (locked partition) and `evaluation-and-comparison` (locked
evaluation).

**Which units are authorised to reach the locked month is a decision the project
decision owner receives and approves.** No artifact this unit produces grants it,
implies it, or treats the static check of Question 8 as a substitute for it.

## Assumptions & Open Questions

- **[assumption]** `tests/test_locked_test_guard.py` is **not** this unit's. ADR-03 splits the guard deliberately — the access-log limb here, the execution limb in `features-and-splits`'s `splits.py` — and the test covering both limbs is owned by `features-and-splits` to keep this unit a root. Story-map Table 2 confirms `features-and-splits` owns WS-18 and TA-18, with this unit supporting.
- **[assumption]** `RAW_MODULES` names **four** `gnss` modules — `rinex`, `calibration`, `target`, `verification` — not the two that FR-P1-03-2's earlier wording listed. `target.py` and `verification.py` were added per finding `IMPL-2`. This stage designs to the four.
- **[assumption]** NFR-PHASE-01's transition-manifest hash-diff test has **no module in the TE §12 tree** and needs frozen artifacts from every later unit. It is carried as an acceptance row on `fixtures-and-reproducibility` (which owns TA-27's evidence chain per Table 2's supporting column) with this unit supporting. Not this unit's to build.
- **Open — BLK-06's per-item binding.** D-24 resolved the enumeration at **17 items** with each item's governing artifact and hashable representation. The **binding to concrete config fields and file paths is PENDING**, and none of the four config files or six `src/` packages exists yet. Questions 1–3 produce the binding evidence; **BLK-06 is not closed by this stage**, per the owner's `DP-CHAIR-02` ruling.
- **Open — BLK-07.** `acquisition`'s routing through `open_restricted` is unrecorded. Question 8 addresses the mechanism; the authorisation question goes to the gate.
- **Open — a stale statement in an approved artifact, reported not edited.** `component-methods.md`'s `TransitionManifest` comment reads *"Final enumeration and cardinality are DEFERRED TO STAGE 3.1; this design states neither"*, and `unit-of-work.md` § 2 says the same. **D-24 has since resolved the enumeration at 17 items.** Both are approved-stage artifacts; per `CHANGE_RECORD_PROCEDURE.md` a sweep reports on those and does not edit them absent owner approval for annotate-in-place. Raised at the gate.
- **Open — the AGPLv3 distribution question.** Whether the Global-TEC-forecasting repository's obligations permit direct copying is a governance dependency **this project does not resolve**. The standing default is reimplementation from the paper with a citation.
- **G-09 is not signed.** No answer here authorises creating `phase_contract.py`, `locked_test.py` or `reuse_registry.py`.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
