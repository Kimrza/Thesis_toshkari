# Business Rules — `inventory-and-registry`

**Unit** `inventory-and-registry` (Bolt 4) · **Kind** `library` · **Depends on**
`acquisition`

> **Re-established a sixth time 2026-08-24**, on a **new stage attempt** (Construction opened
> 2026-08-24T11:46:26Z, resetting every unit's receipt floor). **No rule of this unit
> changed.** Both `foundation` passes of that day touch nothing this unit reads;
> `write_release`'s signature and its `source_files`/`inventory.py` validation clause were
> checked directly and hold; Amendment A was declined, so **no count moved**. **The READY
> verdict in § Review belongs to the previous attempt.**

> **Re-established a fifth time 2026-08-23.** **No rule of this unit changed.** The redo
> corrected a sibling's citations of "`inventory-and-registry` R-20": **the rules below run
> R-44…R-53 and there is no R-20 here.** The rule carrying the open authority question is
> `governance-guards` R-20; **R-49** below carries the distinct point that D-24's protected
> set is not reopened.

> **Re-established 2026-08-23 after a stage-wide redo jump** aimed at a correction in
> `acquisition`. **No rule changed** — this unit's iteration-2 adversarial verdict was
> READY with no surviving findings. **Re-established again 2026-08-23** after a further
> stage-wide redo aimed at `external-products`; **no rule changed then either.**
>
> **A third re-establishment DID change this file.** `component-methods.md` § Depth specifies
> **cross-package boundary calls only** and names **`functional-design` (3.1)** as where
> intra-package shapes are specified; `inventory.py` and `release.py` are the **same
> package**, so R-44's contract is this stage's ordinary work, **not an amendment owed**.
> **No rule's substance changed**; this unit owes **one** amendment — R-46's provenance
> field — not two.
>
> **A fourth re-establishment** swept this unit's **question file**, which had not been
> corrected alongside these rules because its receipt was recorded first. **No rule
> changed.**

The prohibitions this unit enforces, each with what it rejects, what it raises, and the
negative control that proves the rejection happens.

**This project's affirmed methodology is a negative control paired with every hard
rule** — a test that proves the violation is *caught*, not only that the happy path
works. Every rule below carries its negative control, and where no acceptance row exists
to accept that control, it says so.

**Rule IDs continue the single sequence.** `foundation` ran R-01…R-17,
`governance-guards` R-18…R-29 and `acquisition` R-30…R-43, so this unit opens at
**R-44**. This is the numbering assumption stated in `functional-design-questions.md`; if
per-unit numbering was intended, say so at the gate and the artifacts restart at R-01.

## Sources

- `../../../inception/requirements-analysis/requirements.md` — FR-P1-02-1…-5, -7, -8; § Known defects rows 3 and 9.
- `../../../inception/units-generation/unit-of-work.md` § 4 — the `Owns` list, the boundary, the implementation notes.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2 plus § Per-unit coverage summary; both derivation paths agree.
- `../../../inception/application-design/component-methods.md` — `src/data/registry.py`'s raise-contract; `src/data/release.py`'s `write_release`.
- `../../../inception/application-design/services.md` § The nine stage scripts, § Stage entry contract.
- `../acquisition/functional-design/business-rules.md` — **R-32**, **R-33**.
- `../governance-guards/functional-design/business-rules.md` — **R-25**, **R-26**, **R-28**.
- `evidence/DECISIONS.md` — **D-1** and its 2026-08-21 addendum, **D-2**, **D-12**, **D-13**, **D-143**, **D-144**.
- Workspace inspection, 2026-08-23: `notebooks/madrigal_phase1_coverage_audit.ipynb`, `tests/`, and the absence of `src/` and `configs/`.
- `functional-design-questions.md` (**Q1 through Q9**), `domain-entities.md`, `business-logic-model.md`.

---

## The two tiers, inherited

`foundation` R-01 fixes the hierarchy and `team.md` § Code Style fixes the posture.
**Integrity violations** terminate the run non-zero with a message naming the resource and
the violated expectation. **Completeness shortfalls** are non-fatal but recorded as
machine-readable fields, never console text.

**Every rule in this unit is an integrity violation.** That is not an accident: this unit
produces the evidence a supervisor accepts at G-P1A, and a gate whose inputs degrade to
warnings is not a gate.

---

## R-44 — A source entry carries all nine §5.1 fields, or it fails

**Rule (`unit-of-work.md` § 4 Responsibility — *"the source inventory (TE §5.1's nine
fields per entry, including which configuration consumes each source)"*).** Provider, role, filename or
product identifier, coverage, retrieval date, checksum, version or release status, licence
and access notes, **and the configuration that consumes it**. Fewer than nine **fails**.

**Constraint — consumed by release ID and hash, never by path.** `unit-of-work.md` § 4
fixes the boundary: this unit reads `acquisition`'s *released* artifacts, so an upstream
change surfaces as a hash mismatch rather than as silently different content.

**Negative controls.** Omit any of the nine → fails. Present an artifact whose bytes do
not match its release hash → fails.

> ## `src/data/inventory.py` — SPECIFIED HERE BY DESIGN, NOT AN AMENDMENT
>
> `component-methods.md`'s `write_release` states that `source_files`' six items *"are
> validated against `inventory.py` rather than restated as a bare hash"*. **Q1 = D designs
> it MINIMALLY** — only what that stated dependency and TE §5.1's nine fields require,
> nothing speculative.
>
> ## ⚠ CORRECTED 2026-08-23 — THIS IS NOT AN AMENDMENT OWED
>
> `component-methods.md` § Depth states its own policy: **"Full signatures with types for
> cross-package boundary calls. Names and one-line purposes for intra-package functions…
> Every signature below is a cross-package boundary."** Its Assumptions add: **"[Q1]
> Intra-package helper names are indicative. `functional-design` (3.1) specifies them per
> unit and may rename freely — only the signatures above are contracts."**
>
> **`src/data/inventory.py` and `src/data/release.py` are the same package.** The reference
> from `write_release` is therefore **intra-package**, and the absence of a block is the
> artifact's **stated design**, which **names this stage (3.1) as where the shape is
> specified**. Nothing is owed and no change record is needed.
>
> **Superseded reading, preserved:** that the absence was a gap of the same class as
> `acquisition`'s `open_d9_input` — a new symbol in a boundary block that exists and omits
> it, `scripts/` to `src/data` being genuinely cross-package. That one is real; **this one
> was a misreading of a stated depth policy.**
>
> **Consequence for the count:** this unit owes **one** amendment, not two — R-46's
> `Station.provenance` field, which modifies an existing boundary dataclass.


**Acceptance.** TA-04 (**owned by this unit**), TA-15 (owned by `foundation`).

## R-45 — The registry carries §6.2 in full, with the IGRF version pinned and never defaulted

**Rule (FR-P1-02-1, FR-P1-02-7).** `assert_registry_resolved` **raises** `RegistryError`
when any §6.2 field is missing, or when `igrf_version` is **a default rather than a pin**.

The seven items beyond coordinates: ellipsoidal height; DOMES or full identifier;
receiver, antenna and firmware intervals **covering all of 2022**; sampling interval;
available observable codes; any 2022 hardware change; and **one pinned IGRF version**.

**Constraint — an unresolved registry BLOCKS `station_lat` and EXCLUDES
`lst_sin`/`lst_cos`.** `features.build` calls `assert_registry_resolved` before
constructing either, so this rule gates feature construction rather than merely
documenting the registry.

**Constraint — `cell = (floor(lat), floor(lon))`, half-open `[floor, floor+1)` on both
axes** (D-1). A station exactly on a boundary belongs to the higher-indexed cell; none is
counted twice. ARUC 40/44, BSHM 32/35, NICO 35/33.

**Negative controls.** Omit any of the seven → raises. Supply a defaulted IGRF version →
raises. Attempt to build `station_lat` or `lst_*` against an unresolved registry → fails
rather than proceeding.

**Acceptance.** WS-01 (**owned by this unit**, a named Phase 1 exception — see § WS-01)
and TA-04 for the coordinates, cell rule and header cross-check. ⚠ **FR-P1-02-7 has NO
row**: WS-01 reaches the registry's existence and the header cross-check only.

## R-46 — Presence is not provenance

**Rule (Q2 = C).** Each `Station` field carries a **provenance** value, and
`assert_registry_resolved` raises on **insufficient provenance**, not only on missing
presence.

**Why the rule exists.** FR-P1-02-1 requires validation against the **official IGS site
logs** *"before being treated as final"*, and **that has not happened**. D-1's Known
limitation, quoted: *"Station coordinates are taken from IGS network pages, **not** from
the official IGS site-log PDFs, which rank higher in the §6.2 evidence hierarchy… Site-log
validation remains outstanding."* The 2026-08-21 addendum repeats it as **separate and
still open**, and the notebook literal records it in its own data:
`'IGS network page -- cross-check against site log required'`.

**Two readings rejected, with reasons:**

| Rejected reading | Why |
|---|---|
| Presence only | FR-P1-02-1 would have **nothing enforcing it**; the values are already treated as final, and D-1's limitation becomes a note no code reads |
| Insufficient provenance ⇒ unresolved, universally | Literally faithful and **halts the entire downstream pipeline today**, on an obligation nothing in the plan is sequenced around — while D-1 records all three stations sit ≈0.14° or further from a cell edge, so **no assignment would change** |

**Negative controls.** Present a coordinate with network-page provenance to a consumer
requiring site-log provenance → raises. Present the same coordinate to a consumer that
does not → proceeds. Omit the provenance value entirely → raises.

> **What provenance is SUFFICIENT is not decided by this rule.** Station coordinates are a
> §18.2 **Student** forbidden-choice item and the coordinate-to-cell rule a **Student +
> Supervisor** one. The mechanism is fixed here and the **sufficiency question goes to the
> owner at the gate** — writing a default is how a deferral stops being one.

> **The one amendment this unit owes, stated not applied**: the provenance field is an addition to the
> approved `Station` dataclass in `component-methods.md`.

**Acceptance.** Contributes to WS-01 and TA-04.

## R-47 — A resolved conflict equals some recorded source value, and carries a rationale

**Rule (FR-P1-02-1, Vision §6.2, Q3 = D).** *"A conflict must be resolved and recorded,
never averaged or ignored."* Four limbs:

1. **A conflict register** records **every source value** for every field.
2. **The registry's value must be identical to the value of the source it NAMES** — not
   merely to *some* recorded source value.
3. Each resolved field records **which source it came from** and a **non-empty
   rationale**.
4. An **injected averaged value** is tested to be **rejected**, including the **three-or-more
   source case chosen so the mean coincides with a recorded source value.**

**Why limb 2 is an equality against a NAMED source, not an existence check.** A number
carries no history: given 40.286, nothing about the value reveals whether it was read,
chosen, or averaged. An existence check — *"equals some recorded source value"* — is sound
only for **two** sources, where `(a+b)/2 == a` forces `a == b`. **With three or more it is
not:** sources 0, 3 and 6 average to 3, which **is** a recorded source value, so an
existence check passes an averaged resolution. Binding the value to the **named** source
narrows that: the resolution asserts a provenance claim the value must satisfy, rather than
asserting only that the value appears somewhere in the register.

> **Corrected 2026-08-23 after an adversarial pass.** The first issue stated limb 2 as
> *"identical to one of them"* and claimed averaging was caught *"by construction"* —
> **a stronger guarantee than the mechanism delivers**, unqualified, on the
> acceptance-critical path behind WS-01 and TA-04. The unqualified claim is withdrawn.

**The residual case, stated rather than hidden.** When a mean **coincides exactly with the
named source's value**, the stored value *is* that source's value bit for bit, and **no
check on the value can distinguish it from a legitimate resolution.** Nothing in this rule
claims otherwise. What reaches that case is limb 3's rationale, read by a human at G-P1A —
which is why the rationale is required rather than optional, and why limb 4 must exercise
the coincidence case so the boundary is demonstrated rather than assumed.

**What limb 2 also does not catch:** a conflict resolved by **picking the wrong source**.
The identity check proves nothing was **invented**; the rationale is what a reviewer judges.

**Why the rationale must be non-empty.** §6.2 states two obligations — *"resolved **and
recorded**"*. A non-empty rationale is a weak check; its **absence** is a strong one.

**Why limb 4 is mandatory.** `team.md` § Testing Posture makes a negative control
mandatory for every hard rule, and this criterion is written as a failure: *"a conflict
resolved by **averaging** fails."* Without an injection test, limbs 1–3 are a mechanism
nobody has demonstrated.

**Negative controls.** Inject a two-source average → **rejected**. Inject a **three-source**
average chosen so the mean equals a recorded source value **other than the named one** →
**rejected** (the named-source equality catches what an existence check would pass). Inject
a three-source average chosen so the mean equals **the named source's** value → the check
**passes**, and the test asserts that it does — **pinning the stated limit rather than
leaving it to be discovered.** Supply a value matching no recorded source → rejected.
Resolve a conflict with an empty rationale → rejected.

**Acceptance.** WS-01, TA-04.

## R-48 — The migration moves values without changing them, and carries what is unresolved

**Rule (Q9 = D).** The cell rule and the coordinates migrate from the notebook literal into
`configs/data.yaml` and `src/data/registry.py` **together**; each coordinate carries its
**provenance** (R-46); and the migration **emits a diff against the notebook literal,
asserting no value changed in the move.**

**Constraint — freeze first, then migrate.** `team.md` § Code Style: the inline constants
are frozen as a D-number decision **first**, *"so the migration itself cannot silently
change a scientific value."* **The cell rule is already frozen — D-1 is the freeze**, and
its addendum states it directly: *"The notebook literal is a duplicate of a frozen decision
awaiting migration… not the decision itself."*

**Why the diff and not the freeze alone.** A freeze prevents an **intentional** change. The
likelier failure in a hand migration of three coordinate pairs is an **accidental** one — a
transposed digit — and only a comparison catches that. The diff enforces the freeze-first
rule's **stated purpose** rather than only its form.

**Why the coordinates are not held back until site-log validation.** It would leave
`configs/data.yaml` holding a cell rule with no coordinates to apply it to, halting
everything downstream on an obligation nothing has scheduled. Carrying the unresolved
provenance forward lets work continue **without anyone forgetting what is outstanding** —
which is the point of recording it.

**Negative controls.** Alter one digit during migration → the diff fails. Migrate a
coordinate without its provenance → R-46 raises.

**Acceptance.** WS-01, TA-04.

## R-49 — Schema validation runs against a governed schema, and the report is self-contained

**Rule (FR-P1-02-2, Q7 = D).** Validation covers **parameter names, units, fill values,
UTC cadence and duplicates** for the **D-144-approved** prepared product. The expected schema lives in **`configs/data.yaml`**, and the
**report records both the expected schema's digest and the observed values.**

**Why the config and not module source.** `configs/` exists to make governed values
reviewable in one place; a pipeline-wide contract inside one module's source is invisible
to config review. Units and fill values are genuinely facts about the product. TE §12 names
exactly four config files and this needs no fifth.

**Why the digest is in the report.** A report is read later, by someone who cannot
reconstruct the config state it ran against. Recording the expected schema's digest makes
the report **self-contained evidence**, and a changed expected schema produces a visibly
different digest.

**Negative controls.** Rename a parameter, change a unit, alter a fill value, break the UTC
cadence, or introduce a duplicate → each fails separately. Run against a modified expected
schema → the report's digest differs.

> **D-24's protected set is NOT reopened.** Hashing the schema block as an **eighteenth**
> protected item would surface a schema change at **G-P3C** — the stronger design — but
> D-24 is **frozen at 17 items, cardinality calculated from its enumeration**, and adding
> one is a Vision §15.2 amendment, not a design choice. `governance-guards`' own artifacts
> state the enumeration does not reopen at this stage. The digest-in-report gets the
> drift-detection benefit **where this stage has authority**, and leaves the protected-set
> question available to raise separately.

**Acceptance.** TA-04 (**owned by this unit**).

## R-50 — The December audit logs per artifact, and reconciles against a declared scope

**Rule (FR-P1-02-3, Q4 = C).** Three checks, in order:

1. **Declared-versus-REQUIRED, before the audit runs.** The declared scope must **equal a
   governed reference set** — the **twelve 2022 months**, **all three cells** (ARUC 40/44,
   BSHM 32/35, NICO 35/33), and the artifact classes FR-P1-02-3 names. The reference set is
   derived from the release inventory (R-44), **never from the audit's own declaration.** A
   short declaration **fails before anything is read**.
2. **Log-before-read, per artifact.** The audit opens **each artifact** through
   `acquisition`'s named accessor, which writes a **durable access row before the read**
   (R-32, R-33, and `governance-guards` R-25).
3. **Declared-versus-EXECUTED, when it finishes.** The rows actually written are reconciled
   against the declared scope; a mismatch **fails**.

> **Check 1 added 2026-08-23 after an adversarial pass.** The first issue carried only
> checks 2 and 3, so **an audit that declared eleven months and executed exactly eleven
> reconciled cleanly and raised nothing** — while this rule's own stated purpose is that *"a
> silently skipped month produces a wrong figure that looks right."* Declared-versus-executed
> proves internal consistency; only declared-versus-required proves **completeness**.
> FR-P1-02-3's own criterion — *"the coverage report covers all twelve months"* — is what
> check 1 enforces inside this unit rather than leaving to an external row.

**Constraint — the scope of FR-P1-02-3 is `access`, unqualified**, and the requirement
enumerates it: *"derived-artifact merges, re-derivations, corrections, coverage recounts
and schema validations, **not only a model execution**."* Three of those are this unit's
ordinary work.

**Constraint — performance-blind, and checkable.** **No performance figure appears in the
coverage report or in its execution log.**

**Constraint — this unit constructs NO path into the restricted root.** Routing is
`acquisition`'s R-32, and `governance-guards` R-28's static check asserts no module outside
`locked_test.py` holds the literal.

> ⚠ **The routing this rule depends on is PROPOSED, not approved.** `acquisition` R-32's
> named accessors (`open_d9_input` and the restricted writer) are **absent from
> `component-methods.md`'s approved `src/data/locked_test.py` block** and are amendment (1)
> of that unit's three. **This rule inherits that status**: until the change record clears,
> the mechanism this audit routes through is a proposal. Stated at the point of use so a
> builder does not read the dependency as settled.

**Why one row per artifact rather than one per run.** An audit spanning twelve months,
three cells and several artifact classes is many operations. One row makes the log say less
than what happened, and a reviewer cannot tell which reads occurred.

**Why all three checks, and why none of them substitutes.** Per-artifact rows (check 2)
prove **every read was logged**. Check 3 proves **the audit read what it declared**. Only
check 1 proves **it declared everything required** — and this unit's output is a coverage
figure a supervisor accepts, so **a silently skipped month produces a wrong figure that
looks right.** Checks 2 and 3 alone are satisfiable by an audit that never intended to read
the twelfth month.

**Negative controls, one per check.** **Declare eleven months and read exactly eleven** →
`AuditScopeError` **before any read** (check 1 — the case checks 2 and 3 cannot see). Read a
December record with no preceding row → **fails rather than proceeding** (check 2). Declare
twelve months and read eleven → `AuditScopeError` (check 3). Omit a cell, or an artifact
class, from the declaration → fails (check 1). Emit any performance figure into the report
or its log → fails.

> **BLK-07's authorization limb is open**, and this audit runs through the mechanism it
> fixes. **No run may touch calendar 2022-12 while it stands.** A refusal keyed to that
> authorization is deliberately **not** built here: it is the project decision owner's, and
> encoding this stage's reading of an authorization it does not hold would substitute for
> the decision.

> **`RES-01` is open and is about exactly this rule.** Permitted-read access logging is
> **NOT TESTED**, with its candidate §19 criterion owned by stage **3.2** under Vision
> §15.2 — and **this unit performs the permitted read.**

**Acceptance.** TA-25 (**owned by this unit**); contributes to WS-18 (owned by
`features-and-splits`).

## R-51 — G-P1A is decided against two thresholds, and every number is attributed

**Rule (FR-P1-02-4, FR-P1-02-5, Q5 = C).** Both must pass; **neither substitutes for the
other**. §6.12's exception-plus-claim-limitation path **does not apply at G-P1A**.

| Threshold | Value | Decision |
|---|---|---|
| Hourly | **≥ 90% usable hourly coverage per station per month**, hard gate | **D-12** |
| Day | **≥ 95% of calendar days** per month, and **100% of December days** (31/31) | **D-2** |

**Constraint — never an unattributed number.** The record carries a verdict per
station-month **and** the measured hourly and day figure for every station-month, **each
attributed to the D-number it is judged against**. A bare `PASS` makes ARUC's 100.0% and
NICO's 93.2% look identical.

**Constraint — D-2's own disclosure is carried into the record.** D-2 states that **five of
twelve months had already been audited at 100% day coverage when the threshold was
chosen** — *"It was **not** set blind. It is stated here so a reviewer can discount it
accordingly."* A decision record that omits it presents a partly post-hoc threshold as
blind, defeating the purpose the disclosure was written for.

**Measured as at 2026-08-21**, straddle days excluded, across the nine cached non-December
months: ARUC 99.2–100.0%, BSHM 99.3–100.0%, **NICO 93.2–98.9%**. Every station-month clears
90%; **NICO's margin is thin**, and the record shows it rather than absorbing it into a
verdict.

**A soft margin band was declined**, with a reason: flagging station-months near a
threshold is genuinely useful at 93.2%, but *"near"* would be a number **this stage
invented beside a supervisor-frozen threshold**, and an adjacent number that becomes the
real rule is a failure this project has already had to correct.

**Negative controls.** A station-month passing the day rule and failing the hourly gate →
the record fails, not passes. A verdict with no measured figure → fails. A figure with no
D-number attribution → fails. A record omitting D-2's disclosure → fails.

**Acceptance.** TA-25 (**owned by this unit**).

## R-52 — Four prohibitions, four separately named results

**Rule (FR-P1-02-8, Q6 = D).**

| # | Prohibition | Proven by | Owned by |
|---|---|---|---|
| 1 | **Silent imputation** | Injection test — an imputed value must fail | This unit |
| 2 | **Source mixing** | Injection test — a mixed-source artifact must fail | This unit |
| 3 | **Retrospective split redesign after model performance is viewed** | **Frozen-hash ordering artifact** | `features-and-splits` |
| 4 | **Labelling a map value as station-observed VTEC** | Injection test — the mislabel must fail | `target-standardization` |

**Constraint — four separate results, not one.** All four are **named individually** in the
G-P1A evidence set, and **this unit asserts all four are present and passing before G-P1A
accepts.**

**Why 3 cannot be an injection test.** The prohibited act is **a person changing a design
after seeing a result**. No injected value proves that did not happen. A **hash of the
split definition frozen before any performance figure is produced**, plus a timestamp
ordering, is the only evidence class that distinguishes *designed before* from *redesigned
after* — the same mechanism `governance-guards`' transition manifest already uses.

**Why 3 and 4 are owned elsewhere.** This unit is where the **gate** lives, not where
splits are designed or targets labelled. Each test belongs with the unit that owns the
prohibited act.

**Negative controls.** Inject an imputed value → fails. Inject a mixed-source artifact →
fails. Present a split whose frozen hash post-dates a performance figure → fails. Label a
map value as station-observed VTEC → fails. Remove any one of the four results from the
evidence set → the gate assertion fails.

> ## ⚠ WHY THIS RULE IS SHAPED AS FOUR NAMED RESULTS
>
> FR-P1-02-8 previously cited **`TA-29`** — a row `requirements.md` itself lists under
> *"Not applicable in Phase 1 — Phase 2 by definition"*. The citation made the row **appear
> covered** and kept it out of the untested list **stage 3.2 reads to size the G-05 freeze
> manifest**. **Four governance boards passed over it**; an advisory reviewer found it on
> the fifth revision.
>
> The cause was **one citation standing for four obligations**. Four individually named
> results make a missing one **structural** rather than something a fifth reviewer has to
> notice.

**Acceptance.** ⚠ **NO ROW.** `TA-29` is **withdrawn**; the replacement is stage 3.2's and
change control's. **A mechanism is not an acceptance row**, and nothing here may be read as
covering FR-P1-02-8.

## R-53 — ICTP stays out, by reachability

**Rule (FR-P1-00-2, consumed here at the gate).** The G-P1A evidence set includes an
import/data-lineage check showing **no ICTP artifact reachable** from the target or feature
path. The rejection itself is **D-143**, recorded with the coverage that produced it —
ARUC 27/365, BSHM 35/365, NICO 0/365 — and `source_status = REJECTED_COVERAGE`. `acquisition` R-43 owns the rule; this unit asserts its result at the gate, because
**TA-25 is this unit's row.**

**Constraint — reachability, not filenames**, for the same reason R-31 gives: a name-based
check cannot see what a year-blind predicate misfiled.

**Negative control.** Make an ICTP artifact reachable from the target path → the lineage
check fails and G-P1A does not accept.

**Acceptance.** TA-25 (**owned by this unit**).

---

## WS-01 — a named Phase 1 exception, with its boundary stated

`team.md` § Testing Posture defines Phase 1's acceptance set as **WS-09 through WS-20**,
deferring WS-01–WS-08 to G-P3A. **WS-01 is retained in Phase 1 as a named exception**,
approved by the project owner **2026-08-21** (`GOV-2026-08-21-RA-01` Rec 12).

**The basis:** WS-01 is Phase 1-producible — built by `01_inventory_and_registry.py` and
`test_station_registry.py`, neither a raw-processing module — and **§7.0's Phase 1 hard
prohibition, the stated basis for the deferral, does not reach a station registry.**

**The boundary: WS-01 only. WS-02 through WS-08 remain deferred to G-P3A, unchanged.**

**Both failure modes are live, which is why the boundary is stated rather than assumed.**
Without the exception, the station registry — *"the authority for `station_lat`, the
coordinate-to-cell rule and every per-cell statistic"* — would have **no acceptance row at
all**, and a reader comparing this unit against `team.md`'s "WS-09 through WS-20" would
most likely repair the apparent contradiction by deleting the citation. Without the
boundary, a later reader generalises the exception to WS-04.

**A test asserting the acceptance set's shape was declined.** Making the boundary
machine-checked is this project's usual instinct, but the acceptance set is a **governance
fact** recorded in `team.md` and `requirements.md`, not a property of this unit's code —
and asserting a project-wide governance list from inside one unit repeats the ownership
inversion `acquisition` declined when it refused to pin a sibling's enum.

## The two requirements with no acceptance row

**2 of this unit's 7**, derived from story-map § Per-unit coverage summary, which reads
`inventory-and-registry (2)`. No §19 criterion is drafted — §19 rows are owned by stage
3.2 and change control, and a drafted criterion in a functional-design artifact is
indistinguishable, months later, from an approved one.

| Requirement | Rule | Evidence that would close it |
|---|---|---|
| **FR-P1-02-7** | R-45 | An approved §19 row asserting all seven §6.2 items beyond coordinates — ellipsoidal height, DOMES, receiver/antenna/firmware intervals covering 2022, sampling interval, observable codes, 2022 hardware changes, **and a pinned (never defaulted) IGRF version** — are present and match the site logs; plus a passing result. A defaulted or absent IGRF version must fail |
| **FR-P1-02-8** | R-52 | An approved §19 row replacing the withdrawn `TA-29`, carrying **four separately named results**, plus passing results for all four |

> **No artifact, manifest or report may state or imply that either is covered, satisfied or
> verified.** Designing the mechanism is not a test, and implementing it is not a row.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence, so this unit opens at **R-44**. If per-unit numbering was intended, say so at the gate.
- **[assumption]** `tests/test_station_registry.py` is this unit's per `unit-of-work.md` § 4. **It does not exist** — `tests/` holds three modules and that is not one of them.
- **[assumption]** WS-01's Phase 1 retention is settled governance; this stage records rather than revisits it.
- **[assumption]** D-13 owns the December regime-count threshold — three independent storm events under Vision §9.3, counted from **GFZ Kp/Hp60 at a recorded release grade**, with **D-11 barring any provisional-Dst-derived figure**. This unit measures against it.
- **[assumption]** `merge_coverage_year.py` migrates here with `--config configs/` and its `NN_verb_noun.py` position; its `sha256_of_file` copy consolidates into `foundation`'s `src/data/release.py`. This stage designs the target shape, not the migration commit.
- **Corrected 2026-08-23 — `src/data/inventory.py` is NOT an amendment owed.** § Depth specifies boundary calls only and names **`functional-design` (3.1)** as where intra-package shapes are specified; `inventory.py` and `release.py` are the same package. R-44's contract is this stage's ordinary work.
- **Open — the amendment count, corrected 2026-08-23.** **One** here (R-46's `Station.provenance` field), not two. With `acquisition`'s three that is **four across two units**. **Superseded reading, preserved:** *"Five owed amendments… across two units."*
- **Open — what provenance is sufficient**, a §18.2 forbidden-choice question. R-46 fixes the mechanism; sufficiency goes to the owner.
- **Open — D-1's site-log validation limitation**, recorded in D-1 and repeated in its addendum as *separate and still open*. R-46 and R-48 both turn on it; neither closes it.
- **Open — BLK-07's authorization limb**, carried from `acquisition`. **No run may touch calendar 2022-12 while it stands.**
- **Open — `RES-01`**, permitted-read access logging is NOT TESTED — and **this unit performs the permitted read it is about.**
- **Open — FR-P1-02-8's replacement acceptance row** after `TA-29`'s withdrawal.
- **Open — D-24's protected set is not reopened.** The schema-block-as-eighteenth-item question is available to raise separately; it is not proposed here.
- **G-09 is not signed.** No rule here authorises creating `src/data/inventory.py`, `src/data/registry.py`, `scripts/01_inventory_and_registry.py` or `tests/test_station_registry.py`.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.
