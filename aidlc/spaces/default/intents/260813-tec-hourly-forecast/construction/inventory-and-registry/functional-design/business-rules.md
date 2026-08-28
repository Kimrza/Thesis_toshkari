# Business Rules — `inventory-and-registry`

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
- `../../../inception/application-design/components.md` — the component map assigning `inventory.py` its two obligations *(added 2026-08-26, finding M4)*.
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
>
> **Two obligations of `inventory.py`, mirrored here from W-1 on terminal finding N2 (2026-08-26)**
> — `components.md` maps them to the module this unit owns:
>
> 1. **FR-P1-01-6's verbatim Kyoto/CEDAR acknowledgment notice**, carried per source whose
>    provider requires it, due before the G-P1A gate this unit hosts. **Negative control:** an
>    inventory entry for a notice-requiring provider whose notice text is absent or paraphrased
>    → fails.
> 2. **Surfacing `acquisition`'s recorded `suffix_mismatch` field** to `write_release`'s validation
>    read. **⚠ PROPOSED, not settled** *(retraction on terminal finding N3: the earlier W-1 text
>    claimed these obligations were "assigned to no other unit", which `acquisition`'s artifacts
>    refute — its R-34 specifies FR-P1-01-2 fully and holds the release-manifest carriage of the
>    field **Open for stage 3.2**. This clause proposes the inventory as the surfacing path and
>    defers to 3.2's resolution rather than silently answering it)*.

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

## R-47 — A resolved value equals the single value of its NAMED source, and carries a rationale

*(Terminology aligned 2026-08-26, terminal finding N5: the 2026-08-25 heading fix introduced
"CHOSEN" beside the body's, § 3's and W-3's "NAMED" for the same field; NAMED is the term the
entity contract uses.)*

*(Heading corrected 2026-08-25 on adversarial finding 5: it read "equals **some** recorded source value" — the existence-check semantics this rule's own body withdraws with the {0,3,6} counterexample. Superseded heading preserved here.)*

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

**Rule (`project.md` § Forbidden, stated here as this workflow's own hard rule — mirrored from W-6 on
terminal finding N1, 2026-08-26, which found it in the workflow narrative and not in the rule that
carries this audit's negative controls).** **Membership derives from record timestamps, never from
a directory name or filename**: every coverage count and every regime count attributes a record by
its observation timestamp, and out-of-month and out-of-year records are excluded from every
per-month statistic. The realized defect behind the rule is this project's own: a year-blind
predicate filed locked-month records under `audit_evidence_2022-01/`.

**Negative control (added with the rule; re-posed 2026-08-26 on finding M1 of this budget's
iteration 1, which was Major and introduced by the first posing).** In a **synthetic fixture tree
OUTSIDE `evidence/`** — never the live workspace — place a record whose observation timestamp
falls in month *M+1* inside a directory named for month *M*, and run the audit against that tree:
the record must be attributed to *M+1* and month *M*'s count must not move. A directory-keyed
implementation fails both limbs. *(Superseded posing, preserved: "Place a record whose observation
timestamp is 2022-12-15 inside a directory named `audit_evidence_2022-01/` and run the audit…" —
read literally, that instructed planting a December record in a **live** directory outside the
restricted root, which is `governance-guards` R-26 case 1, the exact act R-27's own negative
control exists to catch, the realized TEC-09 defect, a run barred by this rule's own BLK-07
clause, and a fixture violation under `team.md` § Walking Skeleton. December is what the control
**models**; the synthetic months are what it **executes**.)*

**Rule (FR-P1-02-3, Q4 = C).** Three checks, in order:

1. **Declared-versus-REQUIRED, before the audit runs.** The declared scope must **equal a
   governed reference set** — the **twelve 2022 months** with **December carried at day
   granularity as 1–31 December 2022, 31 days** *(day range added 2026-08-28, Recommendation
   15; the reference set previously carried December at month granularity only)*, **all three
   cells** (ARUC 40/44, BSHM 32/35, NICO 35/33), and the artifact classes FR-P1-02-3 names.
   The reference set is derived from the release inventory (R-44), **never from the audit's
   own declaration.** A short declaration **fails before anything is read** — including a
   December cell declared at fewer than 31 days.
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

**Constraint — the two December reads BIND their `purpose` literal, and the third is
refused** *(added 2026-08-28, `GOV-2026-08-28-FD-01` Recommendation 11, option 1)*. This
audit is **two separately logged reads**, not one, and each binds an
`AccessRecord.purpose` value from `governance-guards`' approved enum
(`domain-entities.md:238` — `coverage_audit` | `regime_audit` | `locked_evaluation`):

| Limb | `purpose` | `performance_inspected` | `authorization` |
|---|---|---|---|
| **Coverage figures** — the per-station-month counts § 7's G-P1A record judges against D-12 and D-2 | **`"coverage_audit"`** | **`false`** | a reference to **Vision §8.3** |
| **Regime-event counts** — D-13's independent-storm-event tally | **`"regime_audit"`** | **`false`** | a reference to **Vision §8.3** |

`locked_test_accessed` is `True` on **both** rows, as it is for every read under
`RESTRICTED_ROOT`.

**Why two rows rather than one.** Vision §8.3 describes the audit in a single sentence
covering coverage *and* regime counts, so one row is a defensible reading of the prose — but
the enum carries **three** members, and Vision §13.1 names the coverage report and the
December regime-count report as **separate** G-05 evidence artifacts. Folding both limbs
into `"coverage_audit"` would leave `"regime_audit"` a sanctioned-but-unused member of a
custody enum — the kind of value that later gets repurposed — and would label the
regime-count report's provenance row a coverage audit. Two typed rows give a G-05 auditor
one dated row per required evidence artifact.

**Why this unit binds the literal rather than leaving it to `code-generation`.** Sibling
controls key on the value **this unit writes**, and before 2026-08-28 this unit wrote none —
derived across its four artifacts, **`"coverage_audit"` = 0 bare uses**, all five substring
hits being the notebook filename `madrigal_phase1_coverage_audit.ipynb`, with `"regime_audit"`
and `"locked_evaluation"` likewise **0**. Meanwhile: `../evaluation-and-comparison/functional-design/business-rules.md`
R-109's **two-events boundary** (*"a different event under a different purpose"*) and its
**control that must *not* fire** (*"passes its own door"*) both name `"coverage_audit"`
(verified 2026-08-28 at that file's lines **516-524** and **534-537**); and
`../models-and-baselines/functional-design/business-rules.md`'s **ML-02** correlation
restricts its `AccessRecord` join to **`"coverage_audit"` or `"regime_audit"`** — *"the two
performance-blind December literals"* — with `"locked_evaluation"` deliberately included as
itself a finding (verified 2026-08-28 at that file's lines **309-315**, as amended that day).
**Line numbers are cited as verified on 2026-08-28 and sibling units are being amended in
parallel**, so the quoted anchor phrases, not the numbers, are what identify the text. A
typed separation the producer never commits to is a convention, not a control. TE §18.3
separately bars an implementer from choosing a governed default, and a value sibling controls
read is governed.

**Negative control — the third literal is refused.** An audit read attempted under
`purpose="locked_evaluation"` → **refused**. That literal is **G-06's**, and an audit
carrying it would trip `evaluation-and-comparison` R-109's must-not-fire control and
**block the read Vision §8.3 requires** — the *"opened exactly once"* misreading `team.md`
§ Testing Posture records this project having already had to correct once.

> ⚠ **ONE CONSEQUENCE STATED FOR THE GATE, NOT FIXED HERE.** `evaluation-and-comparison`
> R-109's control that must *not* fire names **`"coverage_audit"` only**. With the regime
> limb now typed `"regime_audit"`, that control does not name the second read, so a rule
> keyed to it would not recognise the regime-count read as legitimate. The fix is one
> literal in a **sibling unit's** file: it is **raised at this stage's gate rather than
> applied**, because editing another unit's rules is not this unit's to do and
> `project.md` § Corrections forbids applying a finding on the strength of the finding
> alone. `acquisition` separately carries an Open item raising an enum-membership test
> pinning `AccessRecord.purpose` exactly, which is where that pin belongs.

**Constraint — this unit constructs NO path into the restricted root.** Routing is
`acquisition`'s R-32, and `governance-guards` R-28's static check asserts no module outside
`locked_test.py` holds the literal.

> ⚠ **The routing this rule depends on is PROPOSED, not approved.** `acquisition` R-32's
> named accessors (`open_d9_input` and the restricted writer) are **absent from
> `component-methods.md`'s approved `src/data/locked_test.py` block** and are amendment (1)
> of that unit's three. **This rule inherits that status**: until the change record clears,
> the mechanism this audit routes through is a proposal. Stated at the point of use so a
> builder does not read the dependency as settled.

**Constraint — the audit's December day range is FULL CALENDAR DECEMBER, 1–31, for both
limbs** *(added 2026-08-28, `GOV-2026-08-28-FD-01` Recommendation 15, option 2)*. The
declared scope's December cell is **1–31 December 2022, 31 days**. Check 1's governed
reference set carries that day range explicitly, so a December cell declared at anything
less **fails before anything is read**. The coverage limb must read all 31 days regardless:
**D-2** requires **100% of December days (31/31)**, which § 7's G-P1A record judges against.
The regime limb reads the same 31 days so that December's activity distribution is
characterised as a property of **the month**, not of a scored subset.

**The window mismatch is RECORDED, not left to be discovered.** The G-06 scored set is
**2–31 December 2022, 30 days**, first 24 h excluded and counted — ruled FU-7 = A on
2026-08-26 and recorded as **D-28** (2026-08-28), whose own consequences list names *"the
regime-count audit's relationship to the scored set"* as still open. This audit's count
window therefore **exceeds the scored window by exactly one day**, and **both reports state
that in those terms** rather than leaving the reader to compute it.

**Constraint — an event lying WHOLLY outside the scored set is reported separately and does
NOT count toward D-13's threshold.** D-13 makes H4's and SRQ-5's confirmatory status turn on
December 2022 containing **≥3 independent storm events**. A storm event whose entire extent
— the `Kp>=5` interval **and** its −12 h pre-event window — falls outside **2–31 December**
is **reported as a separately labelled December-regime observation** and is **excluded from
the ≥3 tally**. The reason is exact: an interval confined to **1 December** would otherwise
promote H4 and SRQ-5 to confirmatory and lift the descriptive-only label while contributing
**zero scored rows** to the confirmatory test; an event beginning early on 2 December whose
pre-event window reaches back into 1 December has the same shape in reverse. D-13's stated
virtue is *one* measured quantity instead of two thresholds that could disagree, and that is
defeated if the quantity is measured over hours the test never scores.

> ⚠ **WHICH DAY RANGE GOVERNS THE THRESHOLD IS A SUPERVISOR-OWNED VALUE, ROUTED TO THE
> GATE.** This rule fixes the **mechanism** — a 31-day read, a disclosed one-day excess, and
> per-event scored/unscored attribution. It does **not** decide the demotion: whether the ≥3
> threshold is judged over 1–31 or 2–31 December is **Student + Supervisor's**, because D-13
> is a supervisor-countersigned demotion threshold and TE §18.3 bars an implementer from
> filling a freeze-gate value. **This unit measures; it does not demote.** The carve-out
> above is the conservative posture pending that ruling — an unscored event is counted
> **nowhere** toward promotion — so no reading of the ruling is pre-empted upward here.
>
> **Nobody can currently check whether the case is live.** **GFZ Kp/ap3 and Hp60/ap60 have
> never been retrieved** (`evidence/audit_ec1_2026-08-15/` holds only `kyoto_dst/` and
> `nrcan_f107/`), and **D-11 bars any provisional-Dst-derived figure** from standing in.
> That is the argument for fixing the window in the design rather than discovering it at
> G-05. `regimes-diagnostics-reporting` R-124 runs `count_storm_events` over *"the window the
> registered audit covers"* and therefore inherits this range; that unit's consistency
> control asserting the range rather than inheriting it is **raised at the gate**, not
> edited here.

**Constraint — every coverage figure carries the DATA-07 provenance caveat as a
MACHINE-READABLE field** *(added 2026-08-28, `GOV-2026-08-28-FD-01` Recommendation 29,
option 1)*. The coverage report carries a **`data07_caveat`** field on every station-month
figure it emits, **sourced from that month's `provenance_class`** (`acquisition` R-36 and its
§ 4) rather than restated: a month classed **`derived_only`** emits the caveat populated; a
month classed **`full`** does not, because it does not carry the defect.

**Negative control.** Emit a coverage figure for a **`derived_only`** month with **no
`data07_caveat` field** → **fails**.

**Why a field and not prose.** `team.md` § Walking Skeleton's DATA-07 caveat is
unconditional — *"Every artifact produced before the re-acquisition carries that caveat and
must state it wherever FULL's coverage figures are relied on"* — and this rule's entire
output **is** FULL's coverage figures over the twelve 2022 months and all three cells.
`acquisition` R-42 confirms the **provenance limb is untouched** by D-18's re-merge and
still stands. Prose has already been measured and failed here: R-42 records that
`PROVENANCE_NOTICE.md` stated this same obligation as prose *"with no ID, criterion or test
link, so nothing checked it"*. Nor is the mechanism invented here —
`fixtures-and-reproducibility`, a **downstream consumer** of this unit's figures, already
carries the caveat as a machine-readable manifest field propagated onto every artifact
bearing a coverage figure, with a caveat-less figure raising (its § 5, control (11)). This
rule applies the same field at the **producing** surface, which is the one place it was
missing.

**What the supervisor accepting G-P1A must be able to read off the report.** Three facts,
each established in a sibling's design and none of them previously on this unit's output:
**(a)** the twelve months' provenance is **unverifiable in principle, not merely
unverified** — no provider byte stream exists anywhere in the workspace, and the
provider-side term of R-36's hash arithmetic is **zero**; **(b)** three of the twelve —
**2022-04, 2022-07 and 2022-12, the locked month** — hold **no `raw_isprint_cache/` at
all**; **(c)** the **2026-08-16 corrected extracts were produced under Python 3.14, local**,
outside the governed **3.11** pin, which is why R-36 records a `producing_interpreter` — a
passing hash on those files otherwise reads as evidence the envelope held, and it did not.
`team.md` adds the limit this report must not overstate: **FULL must not be relied on at a
freeze gate while its provenance chain points at superseded per-month hashes.**

> ⚠ **THE SOURCE FIELD IS SEQUENCED BEHIND `acquisition`'s OPEN SEAM.** `provenance_class`
> is `acquisition`'s field. **As found at the opening of this remediation** — derived
> 2026-08-28 over all **48** `functional-design` artifacts of this stage — it reached **no
> other unit**: `provenance_class` = **9**, `derived_only` = **7**, `producing_interpreter` =
> **3**, every one of them inside `acquisition`. Those three figures are **pre-remediation**;
> what remains true after it is the load-bearing part — **`foundation`, which owns
> `src/data/release.py`, `write_release` and the §13.3 contract, still carries the field zero
> times**, and it is **not among FR-P1-04-11's fourteen release fields**, which `acquisition`
> now carries as an Open item for stage 3.2 under the same governance report
> (Recommendation 28). Until that seam is
> settled the field this caveat reads is **specified but not carried across the unit
> boundary**, and this constraint is **proposed on that dependency** — stated at the point of
> use, exactly as the R-32 routing dependency is stated above, so a builder does not read it
> as settled. **What is NOT deferred is the obligation.** If `provenance_class` is
> unavailable at implementation, this rule requires a **stop-and-report under TE §18.3**, not
> a coverage figure emitted without a caveat.

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

**Negative controls added 2026-08-28 with the three constraints above.** Write either
December read under `purpose="locked_evaluation"` → **refused** (Recommendation 11). Write
the regime-count read under `purpose="coverage_audit"`, or the coverage read under
`purpose="regime_audit"` → **fails**: the limb and its literal are paired, not
interchangeable. Declare a December cell shorter than **31 days** → `AuditScopeError` at
check 1 (Recommendation 15). Count toward D-13's ≥3 tally a storm event lying **wholly**
outside 2–31 December → **fails**; it must appear as a separately labelled observation
instead. Emit a regime-count report that does **not** state the day range its count was
taken over → **fails**. Emit a coverage figure for a `derived_only` month with **no
`data07_caveat` field** → **fails** (Recommendation 29).

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

**Constraint — the DATA-07 caveat travels onto the G-P1A record with the figures** *(added
2026-08-28, `GOV-2026-08-28-FD-01` Recommendation 29, option 1)*. The measured figures above
**are** FULL's coverage figures — the nine cached non-December months are pre-TC-06 months
classed **`derived_only`** (the two absent from the nine, **2022-04** and **2022-07**, are
absent precisely because they hold no `raw_isprint_cache/`). `team.md` § Walking Skeleton
binds the caveat to appear *"wherever FULL's coverage figures are relied on"*, and this
record is the surface a **supervisor** relies on them at. Each station-month figure therefore
carries R-50's **`data07_caveat`** field, sourced from that month's `provenance_class`, and
the record states in its own text that the provenance is **unverifiable in principle, not
merely unverified**; that **2022-04, 2022-07 and 2022-12** hold no retrieval cache; that the
**2026-08-16 corrected extracts were produced under Python 3.14**, outside the governed
**3.11** pin; and that **FULL must not be relied on at a freeze gate while its provenance
chain points at superseded per-month hashes**. A record carrying a `derived_only` figure with
no caveat field **fails**, the same control R-50 states — this rule adds no second mechanism,
it names the surface the one mechanism must reach.

**Negative controls.** A station-month passing the day rule and failing the hourly gate →
the record fails, not passes. A verdict with no measured figure → fails. A figure with no
D-number attribution → fails. A record omitting D-2's disclosure → fails. **A
`derived_only` station-month figure carried into the record with no `data07_caveat` field →
fails** *(added 2026-08-28)*.

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
- **[assumption]** WS-01's Phase 1 retention rests on an **interim reading** — the cited Rec 12 reads "APPLIED as an interim reading… not yet held", its item 3 is still Open with no closure record *(overstatement corrected 2026-08-25 on adversarial finding 4; superseded: "settled governance")*; this stage records rather than revisits it.
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
- **Open — WHICH December day range governs D-13's ≥3 threshold** *(added 2026-08-28, `GOV-2026-08-28-FD-01` Recommendation 15)*. R-50 fixes the **mechanism**: a 31-day read for both limbs, the one-day excess over D-28's 2–31 scored set stated in both reports, and an event lying wholly outside the scored set reported separately and excluded from the tally. **Whether the threshold itself is judged over 1–31 or 2–31 December is Student + Supervisor's** — D-13 is a supervisor-countersigned demotion threshold and TE §18.2/§18.3 bar an implementer from filling a freeze-gate value. **This unit measures; it does not demote.** Nothing here can be checked against December's actual event distribution yet: **GFZ Kp/ap3 and Hp60/ap60 have never been retrieved**, and **D-11 bars any provisional-Dst-derived figure** from standing in.
- **Open — the DATA-07 caveat's SOURCE FIELD crosses no unit boundary today** *(added 2026-08-28, Recommendation 29)*. R-50, R-51, § 6 and § 7 require a machine-readable `data07_caveat` sourced from each month's `provenance_class`. **As found at the opening of this remediation**, derived 2026-08-28 across all **48** artifacts of this stage: `provenance_class` = **9**, `derived_only` = **7**, `producing_interpreter` = **3**, **all inside `acquisition`**. ⚠ **Those three figures are pre-remediation and this bullet's own edits invalidated them** *(rebased 2026-08-28 on the resume pass; the R-50 box at `:521` was rebased at the time and these three sites were not — the representation-sweep gap `project.md` names)*. **Re-derived after the remediation. Basis stated, because it moves**: the figures below were derived over the 48 stage artifacts **immediately before this note was written**, and writing the note itself adds occurrences of each token — which is the same self-invalidation the superseded figures fell into, so the raw counts are recorded as a **dated observation, never as a live invariant**: `provenance_class` **43**, `derived_only` **38**, `producing_interpreter` **17**, split `acquisition` **25 / 21 / 11** and `inventory-and-registry` **18 / 17 / 6**. **The two stable facts, which no edit to this note can change, are the ones to rely on**: the fields reach exactly **2** units, and `foundation` carries all three **zero** times. **What survives the rebasing is the load-bearing half**: `foundation` — which owns `src/data/release.py`, `write_release` and the §13.3 contract — carries all three fields **zero** times, so the field still crosses no boundary to the unit that must read it; and `provenance_class` is **not among FR-P1-04-11's fourteen release fields**, which `acquisition` now carries as its own Open item for stage 3.2 under Recommendation 28. The **obligation** is not deferred — an absent source field requires a **stop-and-report under TE §18.3**, never an uncaveated coverage figure — but the field's arrival at this unit's boundary is `acquisition`'s and stage 3.2's to settle.
- **Open — raised for `evaluation-and-comparison`, not applied:** R-109's control that must *not* fire names **`"coverage_audit"` only**, so it does not name the regime-count read R-50 now types **`"regime_audit"`**. One literal in a sibling unit's file; **gate input, not an edit** *(added 2026-08-28, Recommendation 11)*.
- **Open — raised for `regimes-diagnostics-reporting`, not applied:** R-124 runs `count_storm_events` over *"the window the registered audit covers"* and so inherits R-50's 1–31 December range rather than asserting it. Recommendation 15's closure evidence asks that unit to assert the range; that edit is its own.
- **G-09 is not signed.** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged. No rule here authorises creating `src/data/inventory.py`, `src/data/registry.py`, `scripts/01_inventory_and_registry.py` or `tests/test_station_registry.py`.
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

> **Re-saved 2026-08-25 under the post-eleven-redo receipt.** ~~No rule changed~~ *(corrected
> 2026-08-26, terminal finding N4: R-47's heading was rewritten that same day, so this box was
> false when written)*; figures re-derived
> and unchanged (7 requirements, 2 untested, 3 acceptance rows). The exception base is named
> explicitly in `domain-entities.md`'s preamble (**`IntegrityError`**, R-01's "any future" clause;
> declaration site the standing OPEN item). **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved 2026-08-26 under the twelfth-redo receipt, after the terminal-pass remediation.**
> In this file: **R-50 gained the record-timestamp membership rule and its negative control**
> (N1's mirror — the rule was in W-6's narrative only); **R-44's box gained the two
> `inventory.py` obligations** with the ⚠ PROPOSED flag on the `suffix_mismatch` surfacing
> (N2/N3); the false *"No rule changed"* box corrected (N4); **R-47's heading aligned on
> NAMED** (N5). Figures unchanged: 7 requirements, 2 untested, 3 acceptance rows.
> **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved unchanged 2026-08-26 under the fourteenth-redo re-confirmation receipt** (the unit's
> question file was repaired from mojibake; no design artifact changed). **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved 2026-08-28 under the post-redo receipt, remediating `GOV-2026-08-28-FD-01`
> (verdict FAIL) on the project decision owner's ruling — mechanism written, value routed to
> the gate.** Three recommendations reach this unit, all three landing on the December audit.
> **In this file: R-50 gained three constraints** — (a) **Recommendation 11**: the two December
> reads bind their `AccessRecord.purpose` literal, `"coverage_audit"` for the coverage limb and
> `"regime_audit"` for the regime-count limb, each `performance_inspected=false` with a Vision
> §8.3 `authorization`, and `"locked_evaluation"` refused on either; (b) **Recommendation 15**:
> the December day range fixed at **full calendar 1–31**, the one-day excess over D-28's 2–31
> scored set stated in both reports, and an event lying wholly outside the scored set reported
> separately and excluded from D-13's ≥3 tally; (c) **Recommendation 29**: every coverage figure
> carries **`data07_caveat`** as a machine-readable field sourced from each month's
> `provenance_class`. **R-50's negative-control block gained six controls** and **R-51 gained the
> caveat constraint plus one control**, because R-51 is where FULL's measured figures reach a
> supervisor. **Four Open items added**: the threshold day range (**Student + Supervisor**), the
> caveat's cross-unit source field (`acquisition` / stage 3.2), and two sibling edits raised as
> **gate input rather than applied** — `evaluation-and-comparison` R-109's must-not-fire literal
> and `regimes-diagnostics-reporting` R-124's window assertion.
>
> **Counts derived 2026-08-28, printed before assertion.** Rules **10** (R-44…R-53) — unchanged,
> no rule added or removed. Requirements **7**, untested **2**, acceptance rows **3** —
> unchanged. Negative-control blocks in this file: **12 → 15** (three added to R-50; R-51's
> existing block extended by one control rather than a block added). **No scientific value was
> decided here**: not the demotion threshold's window, not a coverage threshold, not a fixture
> value. **G-09 remains unsigned**, **BLK-07's authorization limb remains open** — no run may
> touch calendar 2022-12 while it stands — and membership stays derived from **record
> timestamps**, never from a directory name (D-2 / ML-07 / TEC-09).
