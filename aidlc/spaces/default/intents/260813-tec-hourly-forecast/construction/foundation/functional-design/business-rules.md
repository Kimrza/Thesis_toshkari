# Business Rules — `foundation`

**Unit** `foundation` (Bolt 1) · **Kind** `library` · **Depends on** — (dependency root)

> **Addendum re-confirmed 2026-08-24, and this box was itself wrong — corrected 2026-08-25
> on adversarial reviewer finding M-3 (Major).** Sites **9–11** of
> `governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md` § Addendum corrected three
> statements elsewhere in this unit that still asserted a superseded amendment status.
>
> **Superseded wording, preserved:** *"**None of them is in this file** — its
> acceptance-status table and its "This label is now permanent, 2026-08-24" box already read
> correctly, which is what made the three missed sites visible by comparison."*
>
> **Why that was false when written.** This file carried **four** further sites asserting a
> superseded amendment status, none of which the 2026-08-24 sweep reached: § Assumptions'
> all-three-pending bullet (finding M-2), R-06's acceptance reason *"because they are not yet
> in the contract"* (M-4), the *"until the amendment is approved"* condition near the
> acceptance-coverage note (m-1), and R-06's *"NOT FULLY ENFORCEABLE"* heading standing above
> its own *"Amendment B APPROVED"* line (m-2). The two clean sites this box named are clean;
> the generalisation from them to the whole file is what failed, and that self-certification
> is why the file was never swept. **None of the four carries a numeral**, which is why a
> sweep keyed to `DeterminismRecord` *"six fields"* and `services.md` *"two artifacts"* could
> not see them — the failure mode `project.md` § Way of Working already names.
>
> **No rule of this unit changed**, no count moved, and no scientific value was touched by
> either the 2026-08-24 addendum or this correction.

> **Re-established a fifth time 2026-08-23**, after a redo aimed at four stale
> cross-references in `target-standardization`'s question file. **No rule of this unit
> changed.**

> **Re-established three times on 2026-08-23, after three stage-wide redo jumps** — aimed
> respectively at a correction in `acquisition`, corrections in `external-products`, and a
> misread depth policy in `component-methods.md`, and — fourth — a sweep of two question
> files that had fallen stale against their own corrected artifacts. **No rule of this unit
> changed on any of the four occasions.**

The decision rules, validation logic, constraints and invariants this unit
enforces. Each rule states what it rejects, what it raises, and what evidence
proves the rejection actually happens.

**This project's affirmed testing methodology is a negative control paired with
every hard rule** — a test that proves the violation is *caught*, not only that the
happy path works. Every rule below therefore carries its negative control, and
where no acceptance row exists to accept that control, it says so.

## Sources

- `../../../inception/requirements-analysis/requirements.md` — REQ-ENG-1, -2, -3, -4, -6, -7, -8, -10, -11; FR-P1-01-10; FR-P1-04-11; FR-P1-05-13; FR-WS-7; NFR-AUD-01; NFR-SEC-01; NFR-DET-01.
- `../../../inception/units-generation/unit-of-work.md` § 1 `foundation` — the `Owns` list, the boundary, the two-tier error posture, and the `ensure_process_determinism`-first constraint.
- `../../../inception/units-generation/unit-of-work-story-map.md` — the acceptance mapping; 2 of 16 requirements carry no row.
- `../../../inception/application-design/component-methods.md` — the raise-contracts for every function named below.
- `../../../inception/application-design/components.md` and `component-dependency.md` — the import boundaries and § Shared resources' carve-out.
- `../../../inception/application-design/services.md` — § Stage entry contract, § Run record and registry.
- `../../../inception/practices-discovery/team-practices.md` — § Code Style (two-tier error posture, docstring rule), § Testing Posture (§18.3 as the real gate).
- `functional-design-questions.md` — Q1–Q8, FU-1–FU-3, the TA-03 verification, the three amendments — A **declined** and B **approved** (2026-08-24), C **declined as drafted** (2026-08-25, reversing its 2026-08-24 approval). Q6 re-answered as **D′** and FU-2 rendered moot, 2026-08-25.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **the Technical Environment document**, cited throughout these rules (§7.0, §9.1–9.2, §12, §13.1, §13.3, §13.4, §18.2–18.3, §19). *(Added 2026-08-25 on an adversarial residual raised twice: the document was cited ten times here and listed in no § Sources entry, and its derivations used an unresolved `<TE>` placeholder. **The placeholder was resolvable** — the file is at `PreFlight/`, 1158 lines — and the three figures it had blocked now derive and agree: **7** §13.1 bullets, **0** file-level entries under `artifacts/` in the §12 tree, and **36** distinct TA rows, TA-01…TA-36, confirming the §19-at-36 figure these rules had been carrying rather than deriving.)*
- `domain-entities.md` and `business-logic-model.md` — the shapes and workflows these rules constrain.

---

## The two tiers, stated once

`team-practices.md` § Code Style fixes a two-tier posture and every rule below
belongs to exactly one tier:

| Tier | Behaviour | Shape |
|---|---|---|
| **Integrity violation** | Terminate the run non-zero with a message naming **the file and the violated expectation** | Raised as an `IntegrityError` subclass |
| **Completeness shortfall** | Non-fatal, but recorded as a **machine-readable field** in the output manifest — never console text only — with the artifact marked derived and/or partial | Return value or manifest field, **never raised** |

**Q5 = B makes tier membership structural rather than remembered.** A shortfall
cannot accidentally be raised as fatal because it is not in the exception
hierarchy at all.

---

## R-01 — `IntegrityError` is the single catchable base

**Rule.** **All fourteen project-defined exceptions derive from `IntegrityError`**, and so does any
future integrity-related exception. `foundation` owns the base class and **raises six** of them —
`ConfigError`, `PreflightError`, `PlatformError`, `DeterminismError`, `ReleaseError`,
`RegistryError`. The other **eight are raised by other units and derive from the same base**:
`PhaseBoundaryError` and `LockedTestError` (`governance-guards`), `LeakageError` and
`AlignmentError`, `SeedError`, `FairnessError`, `BootstrapError`, `RegimeError`.

**Where the hierarchy is declared** *(decided 2026-08-25 on adversarial finding M-1 of the
ninth-redo iteration 1 — **the enumeration above named fourteen subclasses and no module to hold
the base**, which stops stage 3.5 rather than misleading it)*. `IntegrityError` and the six
subclasses this unit raises are declared in **`src/data/config.py`**.

**Why there and not a new module.** TE §12's `src/data/` tree names **nine** modules and **none for
exceptions**, so a dedicated `src/data/exceptions.py` would be a **§12 amendment** — and this stage
has refused throughout to change an approved contract by assertion. `config.py` is already in this
unit's `Owns`, already the module every stage script imports first for `load_configs` and
`ensure_process_determinism`, and already where W-1's abort path lives; declaring the base there
adds no import that the stage-entry contract does not already make. **The eight exceptions raised by
other units import the base from `src/data/config.py`**, which is a legal direction — every one of
those units already depends on `foundation` — and `component-dependency.md` confirms
`src/features`, `src/models`, `src/evaluation`, `src/gnss` and `src/external` may all import
`data`, so no boundary is crossed and no cycle created.

**What was decided and what was not.** This fixes a **declaration site**, which is what
`component-methods.md` § Assumptions defers to 3.1 — *"they are declared where raised until 3.1
places them"*. It decides **no** scientific value, **no** governed constant and **no** signature, and
**G-09 still forbids writing the module.** A dedicated exceptions module would read better and is
recorded as an open item for the owner, because it needs a §12 amendment this stage may not make.

> **Why the enumeration grew from six to fourteen, and on whose authority** *(corrected 2026-08-25
> on adversarial finding m-1 of the eighth-redo iteration 2 — **the one finding in this unit's review
> history that would have made stage 3.5 build the wrong thing**)*. `component-methods.md`
> § Assumptions states that all fourteen *"are project-defined exceptions **in a shared base**. §12
> names no exceptions module; they are declared where raised **until 3.1 places them**."* **This
> stage is 3.1**, and placing them is therefore its job — but R-01 enumerated only the six this unit
> raises, and `domain-entities.md` § 9 mirrored the same six.
>
> **What that omission would have caused.** W-1 step 4 raises `PhaseBoundaryError`, and R-10 has the
> stage entry contract catch `IntegrityError` to write the `aborted` registry row. With
> `PhaseBoundaryError` outside the enumerated hierarchy, an implementer writing `except
> IntegrityError` would let a **phase-boundary violation exit with no `aborted` row** — precisely
> the event **NFR-PHASE-01** and **NFR-AUD-01** most require recorded, and the one failure this
> unit's two-tier posture exists to make impossible. Six consecutive adversarial passes did not
> examine it: `grep -rn "PhaseBoundaryError"` over this unit returned **one** hit, the diagram edge.
>
> **This is exactly the failure R-01's own rationale predicts** — *"a hand-maintained catch list
> means a seventh subclass added later is silently uncaught"* — arriving as a **missing enumeration
> entry** rather than a missing catch clause. The rule was right and its list was not.
>
> **Cross-unit obligation, recorded rather than assumed.** `foundation` owns `IntegrityError` and
> the stage-entry catch, so it fixes the hierarchy from its own side. The eight exceptions above are
> **raised by other units**, and each of those units' `functional-design` must declare its
> exceptions as `IntegrityError` subclasses. `governance-guards` owns `phase_contract.py` and
> therefore `PhaseBoundaryError`; that unit depends on `foundation`, so importing the base is a
> legal dependency direction and creates no cycle. Listed as an open cross-unit item in
> § Assumptions.

**Constraint.** Every `IntegrityError` **must** carry the affected file or resource
and the violated expectation. The constructor requires both, so the two-tier
message format is enforced by construction rather than by convention.

**Why a base and not fourteen independents** *(count corrected 2026-08-25 with R-01's enumeration; it read "six", which was this unit's own raises rather than the hierarchy)*. The stage entry contract must catch *any*
of them to write the `aborted` registry row. A hand-maintained catch list means a
seventh subclass added later is silently uncaught — the same list-versus-rule
failure `DP-DATA-01` already caught in this project, where an obligation written as
a list silently exempted whatever was not anticipated.

**Negative control.** A test defines a fresh `IntegrityError` subclass not named in
any catch list and asserts the stage entry contract still catches it and still
writes the `aborted` row.

**Acceptance.** Contributes to TA-10 (registry records failed as well as
successful runs).

## R-02 — Preflight rejects both a missing field and a `TBD` field

**Rule (Q1 = B).** `assert_no_tbd` rejects a required field that is **absent** from
the configuration *and* a required field whose value is the `TBD — freeze gate`
sentinel. Both are failures.

**Constraint.** The error names **every** offending field, so a run reports all of
them rather than the first — `component-methods.md`'s stated raise-contract.

**Why both conditions.** REQ-ENG-2 wants both caught. A sentinel-only check is a
tautology: it can only find fields already marked `TBD`, so a required field simply
missing from the config passes.

**Negative control.** Two fixtures, one with a `TBD` field and one with the field
absent; both must raise `PreflightError`, and the message must name the field in
each case.

**Acceptance.** TA-02, and TA-23 as §18.3's preflight gate.

## R-03 — The required-fields map is keyed by `(stage, phase)`

**Rule (FU-1 = C).** Required fields are declared per `(stage_slug, phase)` pair.
Fields that legitimately remain `TBD` in Phase 1 **do not block Phase 1**;
Phase-2-required fields **are enforced in Phase 2**.

**Constraint — the completeness assertion is the rule, not the map.** A test walks
the parsed configuration structure and **fails** when a governed required field
appears in no map entry. The map alone is a list; the test is what makes it a rule.

**Why the phase is in the key.** TE §7.0's Phase 1 hard prohibition makes a
Phase-2 field legitimately unset during Phase 1. A stage-only key forces either
failing Phase 1 on fields it must not fill — which `project.md` § Forbidden
prohibits filling — or weakening the check to the intersection, which silently
drops every Phase-2-only field. A `(stage, phase)` key cannot be forgotten the way
a per-field annotation can be omitted.

**Negative control.** Remove one governed required field from the map; the
completeness test must fail. Run a Phase-1 stage whose Phase-2-only fields are
`TBD`; preflight must **pass**. Run the Phase-2 counterpart with the same fields
`TBD`; preflight must **fail**.

**Acceptance.** TA-02, TA-23.

## R-04 — Authorized `TBD` in Bolt 1 is expected evidence, not a failure

**Rule (Q2 = B).** During Bolt 1 the real governed configs **do** contain
`TBD — freeze gate` sentinels — REQ-ENG-2 requires exactly that, and Gate 0's
permitted list allows creating them before G-09. Their presence is **expected test
evidence, not a foundation-stage failure.**

**Constraint — the real-config test asserts a raise, and asserts *which* fields.**
It asserts that `assert_no_tbd` raises **and** that the error identifies **exactly**
the required fields still carrying the sentinel. The expected set is kept explicit
and updated as each freeze gate closes.

**Why this is worth the maintenance.** It turns the sentinels into positive
evidence: the test states which freeze gates are still open, so closing one becomes
a visible event rather than a silent edit.

**Constraint — synthetic fixtures cover both branches.** Fixtures must cover
failure on `TBD` **and** on a missing required field, **and** successful execution
when all required fields are present and finalized. Without the passing fixture the
clean path stays unexercised until every gate closes.

**Negative control.** The real-config test *is* the negative control. Its inverse —
a fixture with everything resolved — is the positive control that stops the test
passing for the wrong reason.

**Acceptance.** TA-02, TA-23.

## R-05 — Determinism is applied before any graph construction, and re-exec comes first

**Rule (NFR-DET-01, `unit-of-work.md` § 1).** `ensure_process_determinism(argv)` is
the **first statement** of every stage script's `main()`, **before any framework
import**. `seed_everything` enables TensorFlow op determinism **before any graph
construction**.

**Constraint.** `seed_everything` **raises** `DeterminismError` when TensorFlow has
already been initialised — **observed as `"tensorflow" in sys.modules`, evaluated BEFORE `seed_everything` performs its own deferred import** *(defined 2026-08-25, final-pass m-7: the phrase was used four times and defined nowhere, and with the TensorFlow import now deferred into this function, a guard checking after its own import would trip on itself)*. Enabling op determinism afterwards is not equivalent, and
a re-exec after TensorFlow loads is pointless.

**Constraint.** The re-exec is **recorded** in `DeterminismRecord.reexec_performed`
and in the run log, so it is never mistaken for a double run.

**Constraint (added 2026-08-25, reviewer finding m-3, owner-decided).** `reexec_performed` is
read from a **sentinel environment variable** that the parent sets immediately before
`os.execv` and the child reads once: present → `True`, absent → `False`. This carrier is
required for the negative control below to discriminate at all —
`ensure_process_determinism(argv)` returns `None`, so nothing crosses the `exec` boundary in
its return value, and a child cannot otherwise distinguish a re-exec from an externally
exported `PYTHONHASHSEED`. **The variable's name is an implementation identifier**, not a
scientific constant or a governed config field, so it is not subject to TC-03e and lives in
`src/data/config.py`; the approved stage-2.6 `-> None` signature is **unchanged**.

**Constraint — the sentinel is READ ONCE AND UNSET** *(added 2026-08-25 on adversarial reviewer
finding m-3, second pass)*. The child **must remove the sentinel from its environment
immediately after reading it**. The reader is `ensure_process_determinism` itself, at W-1 step 1 —
the first statement of every stage script's `main()` — so the pop happens before any stage logic
runs and therefore before any subprocess this script could launch. *(The earlier phrasing "before
any subprocess is launched" named no actor and was unsatisfiable as a standalone requirement:
corrected 2026-08-25 on adversarial finding m-3 of the restored budget. `reexec_performed` is
held **in module-level state inside `src/data/config.py`** — set by `ensure_process_determinism`
at the moment it pops the sentinel, read when the `DeterminismRecord` is constructed. *(Added
2026-08-25 on adversarial finding m-1 of the restored budget, which found this the **only
implementability gap no open item covered**: the sentinel's journey across the `exec` boundary was
specified, but nothing said where the bit lived **in-process** between the pop at W-1 step 1 and
the record at W-4 step 4. `ensure_process_determinism` returns `None`, `seed_everything(snapshot,
*, stage)` takes no such argument, and `ConfigSnapshot`'s eight approved fields carry no re-exec
bit — so stage 3.5 would have had to invent a holder, which is exactly what naming the sentinel
was meant to prevent.)*

**Why module-level state and not the alternatives.** Both the setter and the reader live in
`src/data/config.py`, which `unit-of-work.md` § 1 gives to this unit, so the hand-off is
**intra-module** and creates no cross-module coupling and no new parameter. The alternatives each
change an **approved stage-2.6 contract** and would need the same amendment this stage demanded
elsewhere: returning `bool` from `ensure_process_determinism` alters its `-> None` signature;
adding a field to `ConfigSnapshot` alters an approved dataclass, and `ConfigSnapshot` is built at
W-1 step 2 — *after* the pop at step 1 — so it cannot receive the bit without reordering the
contract; adding a parameter to `seed_everything` alters its signature. **This is an engineering
decision with no scientific content, no governed value and no config field**, and it is recorded
here as a decision rather than left to 3.5.

The value is then **recorded** into `DeterminismRecord` at W-4 step 4, which reads the value
`ensure_process_determinism` captured rather than re-reading the environment — the variable is
already gone by then, which is the point.)* Without that pop the carrier
is wrong rather than merely imprecise: environment variables are inherited by descendants, and
after a re-exec `PYTHONHASHSEED` is already set, so a subprocess launched from a re-exec'd stage
script does **not** re-exec and yet still sees the sentinel. It would record
`reexec_performed = True` for a process that never re-exec'd, and **this rule's negative control
below would pass for the wrong reason** — the failure mode this project's testing posture exists
to catch. With the pop, the bit that crosses is *this process is a re-exec child*; without it,
the bit that crosses is *some ancestor was*.

**Constraint — `config.py` must not import a framework at module scope** *(stated 2026-08-25 on
adversarial residual r-4, raised in two consecutive passes and derivable but unstated)*.
`seed_everything` lives in `src/data/config.py` and needs TensorFlow, while
`ensure_process_determinism` — in the **same module** — must run *before any framework import*
(FU-1 = D). A module-scope `import tensorflow` would therefore load the framework **at the moment
the stage script imports `config.py`**, which is before `main()`'s first statement executes, and
would defeat the re-exec guarantee the rule exists to provide. **TensorFlow is imported inside
`seed_everything`**, not at module scope. **The same rule binds every stage script** *(added 2026-08-25, final-pass m-6)*: a stage script importing a framework at module scope loads it before `main()`'s first statement, so `ensure_process_determinism` would re-exec after TensorFlow loads — pointless per FU-1=D — and W-4's already-initialised guard would abort every run. Stage scripts import frameworks inside functions or after the entry contract's step 1. **The prohibition is transitive** *(limb restored 2026-08-25 on confirming-pass finding F-2: binding only the script's own imports leaves the by-construction case open — a script importing `src/models/train.py` at module scope complies with the letter while `train.py`'s own module-scope `import tensorflow` aborts every run)*: **no module a stage script imports at module scope may itself import a framework at module scope.** Framework imports live inside the functions that need them, throughout `src/`. This is a consequence of the approved stage-2.6 contract
placing both functions in one module rather than a choice made here, and it is stated because an
implementer following the module layout without noticing the ordering would silently break FU-1 = D.

**Constraint.** `seed_everything` **does not** touch the bootstrap seed. That
carve-out is `src/evaluation/bootstrap.py` by ADR-05 — a design decision, not an
oversight.

**Negative control.** Import TensorFlow, then call `seed_everything`; it must raise
`DeterminismError`. Invoke a stage script with `PYTHONHASHSEED` unset and assert
`reexec_performed` is `True` and exactly one run is recorded.

**Acceptance.** **WS-17, TA-13** (NFR-DET-01) and **TA-10** (FR-P1-05-13), both derived from story-map Table 1. *Superseded: `TA-13, TA-26`.*

## R-06 — An empty `nondeterministic_ops` is never proof of determinism

**Rule (Q3 = C).** `nondeterministic_ops` is populated from **runtime
observation**, cross-checked against any expected set declared in configuration.
The framework version, determinism settings, probe scope and detected mismatches
are all recorded. A mismatch between declared and observed is an **integrity
finding**.

**Constraint.** Where the framework cannot give a complete assessment, the result
is explicitly marked **`partial`**. Where the relevant operations have not yet
executed, they are marked **`not-yet-measured`**. **An empty list is never treated
as proof of determinism.**

> ## ✅ THIS RULE IS ENFORCEABLE UNDER THE APPROVED CONTRACT
>
> *(Heading corrected 2026-08-25 on adversarial reviewer finding m-2. **Superseded heading,
> preserved:** "⚠ THIS RULE IS NOT FULLY ENFORCEABLE UNDER THE APPROVED CONTRACT". It was
> true when written and contradicted its own first line from the moment Amendment B was
> approved on 2026-08-24 — the body below was rewritten then and the heading was not. The
> enforceability conclusion is not being weakened or strengthened to match the heading: it is
> the conclusion the body already reaches and evidences, namely that the three fields exist,
> so the rule's condition is checkable. The equivalent heading in both sibling artifacts was
> rewritten on 2026-08-24; this one was missed, the same heading-versus-body class the change
> record's § Sweep result already reported once.)*
>
> **✅ Amendment B APPROVED 2026-08-24** (`CR-2026-08-24-FOUNDATION-AMENDMENTS`).
> `probe_scope`, `measurement_status` and `declared_vs_observed_mismatches` now exist
> in `DeterminismRecord` — the contract carries **nine** fields, derived:
> `awk '/class DeterminismRecord/,/^$/' component-methods.md | grep -cE "^ +[a-z_]+: "` → `9`.
>
> *Superseded status, preserved:* the three fields *"**do not exist** in
> `DeterminismRecord` as approved at stage 2.6 — the contract carries **six** fields"*,
> and **Amendment B was PENDING and NOT approved**, so the record could carry a probe
> *result* with no recorded *scope* and no measurement *status* — exactly the ambiguity
> Q3 = C was chosen to eliminate. That ambiguity is now closed.
>
> **The prohibition this box carried is now DISCHARGED, because its condition has
> ended.** It read: *"binding now and not deferred: no artifact, manifest, registry
> row or report produced by this unit may state or imply that determinism has been
> measured for any operation class, **while the fields that would record the scope and
> status of that measurement do not exist**. Silence is the correct output, not an
> empty list presented as a clean result."* The fields now exist, so the condition no
> longer holds.
>
> **What replaces it is narrower, not nothing.** A statement that determinism was
> measured is permitted **only** where `probe_scope` records what was examined and
> `measurement_status` is `complete`. Where the status is `partial` or
> `not-yet-measured`, the output says so — it does not fall silent, and it does not
> present an empty list as a clean result. **R-06 is untouched**: an empty
> `nondeterministic_ops` remains no proof of determinism.

**Negative control.** Declare an operation as expected-nondeterministic in
configuration that the probe does not observe, and the inverse; both must surface
as mismatches rather than being silently reconciled.

**Acceptance.** **WS-17, TA-13** — **for the probe result only** (*superseded: `TA-13, TA-26`*). No row accepts the
scope or status fields, because no §16 or §19 row was added or amended to cover them: they are
uncovered **by design and permanently**, not pending.

> *(Reason corrected 2026-08-25 on adversarial reviewer finding M-4 (Major). **Superseded
> reason, preserved:** "because they are not yet in the contract." That was refuted by
> Amendment B, approved 2026-08-24 — `probe_scope` and `measurement_status` **are** in the
> contract, as the box above this rule states and derives (`DeterminismRecord` carries nine
> fields). **The conclusion is unchanged and still holds:** the two field names appear in no
> acceptance-row table anywhere in this workspace — only in `component-methods.md` and
> `governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md`. What changed is why: adding
> a covering row would require a new §19 row, and Amendment A — the only proposal to add rows
> for this unit — was **declined**, with §19 held at 36 rows and TA-37/TA-38 explicitly not to
> be added. So the gap is settled rather than provisional. This site carries no numeral, which
> is why the 2026-08-24 sweep — keyed to "six fields" and "two artifacts" — could not see it.)*

## R-07 — Registry status vocabulary is closed and validated at write time

**Rule (Q4 = D).** `status` is one of exactly **`started`**, **`completed`**,
**`aborted`**, **`failed`**. The writer rejects anything else.

**Constraint.** `aborted` and `failed` **require a non-empty `reason`**.

**Constraint — semantics are not interchangeable.** `aborted` is an intentional or
preflight-triggered stop; `failed` is an execution failure. They carry different
diagnostic stories and must not be collapsed.

**Why validated at write time.** Enum validation needs no read of prior rows, so it
costs nothing against the append-only guarantee. An unenforced vocabulary lets a
typo produce a row no reader groups correctly — and in an append-only file that
corruption is permanent.

**Negative control.** Attempt a write with an unknown status; it must be rejected.
Attempt `aborted` with an empty reason; rejected.

**Acceptance.** **TA-10, TA-21** — NFR-AUD-01 per story-map Table 1. *Superseded: `TA-10` alone.*

## R-08 — Registry writes never read the run history

**Rule (Q4 = D, explicit).** Registry writes are **append-only and do not require a
prior read of the run history.**

**Constraint.** The status **transition graph** is therefore enforced by a
**separate registry-integrity test**, not at write time.

**Why the separation matters.** A log whose write path depends on reading is no
longer a pure append — and that purity is the only reason append-only is
trustworthy. Q4 chose D over C precisely to keep it.

**Legal transitions per `run_id`:** `started → completed`, `started → aborted`,
`started → failed`.

**Rejected by the integrity test:** duplicate `started` rows, repeated terminal
statuses, any transition out of a terminal status, and unknown or malformed rows.

**Constraint — when it runs.** Before TA-10 / G-09 acceptance, and **before
registry contents are relied on as audit evidence.**

**Negative control.** Synthesise each rejected sequence and assert the integrity
test fails on each.

**Acceptance.** **TA-10, TA-21** — NFR-AUD-01 per story-map Table 1. *Superseded: `TA-10` alone.*

## R-09 — A failed or aborted run stays visible

**Rule (NFR-AUD-01).** No registry entry is deleted, overwritten, or silently
re-run. A failed or aborted run **stays visible with its status and reason.**

**Constraint.** Status transitions **append a new row** referencing the run ID
rather than mutating the original.

**Why this holds by construction.** Removing a line would require rewriting a file
nothing rewrites. Two `started` rows with one `completed` is visible in the log, so
a silent rerun cannot hide.

**Negative control.** Attempt an in-place status mutation; it must be impossible
through the API. Assert an aborted run's row survives a subsequent successful run
of the same stage.

**Acceptance.** **TA-10, TA-21** — NFR-AUD-01 per story-map Table 1. *Superseded: `TA-10` alone.*

## R-10 — On an integrity failure, report honestly even when reporting fails

**Rule (Q5 = B).** The stage entry contract catches `IntegrityError`, **attempts**
to append an `aborted` registry row carrying the failure reason, and exits
non-zero.

**Constraint — the part that must not be simplified.** If the registry write
**itself** fails, the original exception is **preserved**, **both** the original
failure and the registry-write failure are reported to stderr, and the process
exits non-zero **without claiming that an aborted record was successfully
written.**

**Why this is a rule and not an implementation detail.** A handler that swallows
its own write failure produces the worst possible artifact: a run that failed, was
not recorded, and reported that it had been recorded. Every downstream audit would
read the absence as "no such run".

**Constraint.** On failure in steps 1–5 of the stage entry contract, the script
exits non-zero with a message naming the file and the violated expectation. **It
does not proceed with a warning** — these are integrity violations.

**Negative control.** Force a preflight raise with the registry path unwritable;
assert both failures reach stderr, the exit is non-zero, and no success is claimed.

**Acceptance.** TA-10, TA-23.

## R-11 — Release identity is the content hash; the label is not authoritative

**Rule (Q6 = D′, re-answered 2026-08-25).** The **content-derived SHA-256 is the authoritative
release identity.** The human-readable `dataset_version` label exists for review and citation
and is **explicitly not authoritative.**

> *(Rule text corrected 2026-08-25 on adversarial reviewer finding M-1, which was Major.
> **Superseded rule, preserved verbatim:** *"**Rule (Q6 = D).** The **content-derived SHA-256 is
> the authoritative release identity.** The **monotonic** human-readable label exists for review
> and citation and is **explicitly not authoritative.**"* Both halves were refuted by this
> stage's own current authority: Q6 was re-answered as **D′**, which states verbatim *"Drop
> 'monotonic.'"*, and R-12 twelve lines below already cited `Q6 = D′` — so two adjacent rules in
> one file cited different authorities for the same decision, and the earlier cited an answer
> that no longer said what it was cited for.
>
> **Why the 2026-08-25 sweep missed it.** Three sites asserted *"**R-11 is unchanged**"*. That
> was true of R-11's **substance** — the hash stays authoritative — and false of its **text**,
> and the assertion stood where the check should have been. Structurally the same
> self-certification as iteration-1's M-3, which this same file had already been corrected for.
> All three sites are now qualified to say substance-unchanged, text-amended.)*

**Constraint.** The authoritative hash is derived from a canonical manifest or
content representation that **excludes** the human-readable label, volatile
metadata, and any self-referential hash field.

**The canonical representation, specified** *(decided 2026-08-25 on adversarial finding M-1 of the
final confirming pass — the one finding of that pass that would mislead stage 3.5: four sites named
the exclusions and none enumerated what is included, whether `created_at_utc` is excluded, or the
serialization, so 3.5 would have had to invent the identity of every release. An engineering
decision with no scientific content, decided on the same basis as the sentinel and the
`IntegrityError` placement; `components.md` sets the precedent by deferring the phase-contract's
canonical set to 3.1 explicitly, and this stage is 3.1)*:

- **Included — twelve of the thirteen caller-supplied §13.3 fields:** `source_manifest_id`;
  `source_files` (its six FR-P1-01-2 items); the whole `processing` group; `schema_version`;
  `units`; `row_counts`; `exclusions_qc_summary`; `fold_ids`; `mask_ids`; `feature_set_ids`;
  `output_files`; `change_record_id`.
- **Excluded — exactly the three categories Q6's answer named, now bound to fields:**
  `dataset_version` (the human-readable label — derived *from* the hash, so including it would be
  circular); `created_at_utc` (**the volatile metadata** — re-releasing identical content at a
  different time MUST reproduce the same identity, or the idempotence property W-7 and R-12 assert
  is silently false); and `content_hash` itself (the self-referential hash field).
- **Serialization:** canonical JSON — UTF-8, lexicographically sorted keys at every level, no
  insignificant whitespace (RFC 8785 profile) — then SHA-256 over those bytes. Chosen because it is
  platform-independent byte-for-byte, which WS-20/TA-17's two-platform reproduction requires of the
  authoritative identity.
- **Array element order** *(added 2026-08-25 on confirming-pass finding F-1, which was Major and
  correct: RFC 8785 canonicalizes object keys and numbers but does NOT reorder arrays, and five of
  the twelve included fields are arrays — `source_files`, `output_files`, `fold_ids`, `mask_ids`,
  `feature_set_ids`. Unordered, a directory listing on Kaggle versus local yields two different
  canonical documents for byte-identical content, which is exactly the failure this specification
  exists to prevent)*: **before serialization, every array-valued included field is sorted
  lexicographically by the RFC 8785 serialization of its elements.** These five fields are
  set-valued in substance — collections of file records and identifiers whose order carries no
  meaning — so sorting loses nothing and removes the only platform-dependent input. A future
  genuinely order-bearing field must be declared as such at the freeze gate before it may join the
  included set unsorted.
- **The determinism control runs across two processes** *(same finding)*: control (1) is executed as
  serialize-in-one-process, re-serialize-in-a-fresh-process (and on the second platform where
  available), comparing bytes — an in-process double serialization cannot detect
  environment-dependent ordering, which is the defect it exists to catch.
- **Negative controls, content→hash** *(the direction R-12's existing controls did not cover)*:
  (1) serialize the same manifest twice → **byte-identical** hash; (2) change any included field →
  **different** hash; (3) change **only** `created_at_utc` → **same** hash, proving the idempotence
  claim rather than asserting it.

**Constraint.** A label/hash mismatch is an **integrity violation** — not a
discrepancy to reconcile.

**Why the hash wins.** Every integrity guarantee in this project is hash-based.
Making the label authoritative would put the weaker identifier in charge. The
project's gates are human-reviewed, so a citable label is needed; stating which one
wins is the part that must not be left implicit.

**Negative control**, owned by `tests/test_release_hashes.py` (TA-15) — **which already exists and
must be EXTENDED, not created** *(recorded 2026-08-25 on adversarial residual r-2 of the restored
budget)*. The file is present at 12,281 bytes and today covers `evidence/audit_evidence_2022-*`
byte integrity; `grep -c dataset_version` over it returns **0**. Its ownership is nonetheless
correct — TE §12's tree names it, TA-15's evidence column is *"Release manifest and
mutation-protection test"*, and `unit-of-work.md` § 1 places it in this unit's `Owns` — so the
control belongs here; what changes is that stage 3.5 adds to an existing module rather than
writing a new one. **A related upstream statement is now stale and is NOT edited here:**
`team-practices.md` § Testing Posture asserts *"No `tests/` directory exists yet in the
workspace"*, which is false. `org.md` reserves that file for the practices-affirmation gate, so it
is reported rather than corrected. Present a manifest binding
a `dataset_version` to a `content_hash` it does not correspond to; the check must reject it.

> **Where this check lives, stated because relocating it orphaned it** *(adversarial finding M-5,
> restored budget, 2026-08-25)*. The previous pass moved this control from the write path to "a
> presented manifest" without naming what performs it. `verify_release(manifest_path) ->
> Sequence[str]` is the only candidate in the approved contracts, and it **does not fit as
> written**: it returns the names of files whose *file hash* does not match and **never raises**,
> so it neither covers label/hash correspondence nor signals failure the way this control
> requires. Rather than invent a contract — which TE §18.3 forbids stage 3.5 from doing — the
> control is specified as a **test** obligation on `tests/test_release_hashes.py`, which is where
> TA-15 already lives and where a negative control needs no production entry point. **If runtime
> enforcement is wanted**, `verify_release` must be amended to check correspondence and to signal
> it; that is recorded as an amendment need in § Assumptions rather than assumed here.

> *(Control corrected 2026-08-25 on reviewer finding m-2. **Superseded control, preserved:**
> *"Bind a label to two different content hashes, and a content hash to two labels; both must
> raise."* Under Q6=D′ the label is a **function** of the content hash, so the second limb — one
> hash bound to two labels — is **unconstructable on the write path**: a function cannot produce
> two outputs for one input. What remains testable, and is what this control now asserts, is a
> **presented** manifest whose label and hash do not correspond, which is the case that actually
> arises when a manifest is read back or hand-edited. The first limb — one label on two different
> hashes — is subsumed by R-12's injectivity obligation and is testable only once the encoding is
> specified; see the open item in § Assumptions.)*

**Acceptance.** TA-15.

## R-12 — `dataset_version` is derived from the release `content_hash`

**Rule (Q6 = D′, re-answered 2026-08-25 — supersedes Q6 = D and moots FU-2 = D).** `dataset_version` is
**derived from the release's `content_hash`**. There is **no release ledger**, no allocation
step and no `ReleaseLedgerEntry`. **The exact hash-to-label encoding is NOT specified here**,
because no approved artifact specifies one — and stage 3.5 must **not** choose one either: per
TE §18.3 it must stop and report rather than pick a default.

**Constraint.** `dataset_version` is never authoritative. Release identity is the
`content_hash` (R-11, unchanged). A `dataset_version` that does not match its release's
`content_hash` is an integrity violation — **rejected on the write path** by `write_release`, and
**detected on read-back by the test control only**, because no approved runtime contract performs
it: `verify_release` returns `Sequence[str]` and never raises. *(Scoped 2026-08-25 on adversarial
finding m-2 of the restored budget; the superseded wording — "…`content_hash` raises" — asserted
an unscoped raise that is true on the write path and unavailable on read-back, contradicting
§ Assumptions item 4, which records exactly that. Closing the read-back hole requires the
`verify_release` amendment listed there.)*

**Constraint — what determinism does and does not replace.** The derivation is a **pure function
of `content_hash`**: there is no allocation step and no state to consult. State exactly what that
buys, because the difference decides whether "never reused" holds:

1. **Idempotence — PROVIDED.** Identical content yields an identical `dataset_version`, by
   construction. This does dispose of the failure the superseded R-12 rejected a derived index
   for: that failure required *allocation from an index* — delete a release directory, the
   rebuilt index forgets the label, the next allocation hands it out again — and a pure
   derivation allocates nothing, so there is no index to forget. Deleting and rebuilding a
   release from the same content reproduces the same label, which is correct behaviour rather
   than a collision.
2. **Injectivity — NOT YET ESTABLISHED, and it is what "never reused" actually requires.**
   Never-reuse is *different content → different label*, which is injectivity, not idempotence,
   and a pure function is not injective in general. The reduction to a SHA-256 collision holds
   **only if the encoding preserves all 256 bits** — and Q6=D′ deliberately keeps the label
   **human-readable and citable**, so any label short enough to cite at a gate is a **lossy**
   encoding of the hash whose collisions are birthday-bounded on the bits it retains, not on 256.
   Since **the encoding is not specified here and stage 3.5 is forbidden to choose one**, the
   property never-reuse depends on is deferred to a decision no artifact is yet permitted to
   make.

> *(Corrected 2026-08-25 on adversarial reviewer finding M-3, which was Major and which refuted
> a claim this design had been asserting as settled. **Superseded text, preserved verbatim:**
> *"**Constraint — determinism, which is what replaces the ledger's guarantee.** … Two
> consequences follow, and they are the reason the never-reused obligation survives the
> reversal: … 2. **A label bound to two different contents reduces to a SHA-256 collision.** It
> is not reachable by any bookkeeping error, because the label is a function of the hash."*
>
> **Why that was wrong.** It proved idempotence and then claimed never-reuse, which is the
> converse. The error was load-bearing rather than cosmetic: this argument was the **sole**
> stated reason Q6=D′ could drop *"monotonic"* while keeping *"never reused"*. The honest
> position is the one this design already takes about monotonicity — state what the mechanism
> provides, and record what it does not as an obligation on whoever specifies the encoding. That
> obligation is now an explicit open item in § Assumptions.)*

**Negative controls.** Three, replacing the ledger-specific set. **None of them establishes
injectivity**, and that limit is stated rather than left for a reader to notice:

- **Correspondence.** Present a manifest whose `dataset_version` does not correspond to its
  `content_hash`; it must be refused. *(This is what discharges FU-2's inconsistent-mapping
  obligation in the form Q6=D′ leaves available.)*
- **Determinism.** Derive twice from the same `content_hash` and require **byte-identical**
  results — asserted, not assumed, the posture NFR-DET-01 takes everywhere else.
- **Non-degeneracy.** Derive from two different `content_hash` values and require **different**
  results. **This catches a degenerate (constant) encoding and nothing more.** It is a
  two-sample test: a **truncating** encoding passes it for essentially every pair while still
  admitting collisions, so it must not be cited as evidence of never-reuse. **Name it
  "non-degeneracy", never "injectivity"** — three earlier sites called it the latter, which is
  the claim it cannot support (adversarial finding m-1, restored budget, 2026-08-25).

**Obligation on whoever specifies the encoding**, recorded here so it travels with the rule: the
encoding must be **injective over the release population in scope**, or its collision bound must
be stated and accepted at a gate. Until then `dataset_version` is a **citation device with
correspondence and determinism guarantees only**, and no artifact, manifest or report produced by
this unit may state or imply that release labels are never reused.

> ## ⚠ WHAT THIS RULE GIVES UP — ONE CAPABILITY DROPPED, AND ONE OBLIGATION STILL OPEN
>
> *(Heading corrected 2026-08-25 on adversarial finding M-1 of the eighth-redo iteration 2.
> **Superseded heading, preserved:** "⚠ WHAT THIS RULE GIVES UP — ONE CAPABILITY, NO LONGER AN
> UNMET OBLIGATION". True when written, above an item 1 that then read "SATISFIED", and stale from
> the moment that item was corrected to "NOT ESTABLISHED" — refuted twenty-six to eighty-three lines
> below by this rule's own body and by § Assumptions' OPEN items. **Why the previous sweep reported
> zero live sites: it matched the words *never-reuse*, and this heading contains neither.** That is
> the seventh appearance of this class in this unit, and the durable remedy applied throughout is to
> name what is open rather than count or characterise it.)*
>
> This rule was **rewritten on 2026-08-25** when the project decision owner **declined
> Amendment C as drafted**, reversing its 2026-08-24 approval. **Superseded rule, preserved
> verbatim:**
>
> > *"**R-12 — Labels are allocated from a durable ledger and never reused.** **Rule (Q6 = D,
> > FU-2 = D).** Human-readable labels are allocated from a **durable, append-only release
> > history**, not solely by scanning existing directories. **A previously assigned label is
> > never reused.** **Constraint.** The ledger is **separate from `experiment_registry.jsonl`**.
> > **Why not a derived index.** Q6 ruled out directory scanning by name. A derived index has
> > the same defect: delete a release directory and the rebuilt index forgets the label, so the
> > next allocation reuses it. **Why not folded into the registry.** Q4's transition graph would
> > have to filter by row kind before applying its rules, and a rule whose readers must filter
> > first is a rule that quietly stops applying to the rows it was written for. **Negative
> > control.** Delete a release directory and attempt a fresh allocation; the previously used
> > label must still be refused."*
>
> **Read that superseded text against the replacement — and note where its objection does not
> transfer.** The superseded rule rejects a *derived index*, and its stated defect is that a
> rebuilt index forgets a label so **the next allocation reuses it**. That defect is a property
> of **allocation from state**, not of derivation: a pure function of `content_hash` allocates
> nothing and consults nothing, so there is no index to forget. The objection was sound against
> the mechanism it was written about and **does not carry** to this one. Of the two Q6=D
> obligations, therefore:
>
> 1. **Never-reused — NOT ESTABLISHED. Contingent on an encoding that does not yet exist.**
>    *(Corrected 2026-08-25 on reviewer finding M-3. **Superseded claim, preserved:** *"**Never-reused
>    — SATISFIED, by a different mechanism.** Not by durable state but by determinism: identical
>    content derives an identical label by construction, and a label bound to two genuinely
>    different contents reduces to a **SHA-256 collision**, unreachable by any bookkeeping
>    error … Three replacement negative controls are stated above, and they are **stronger than a
>    correspondence check alone**: correspondence, derivation determinism, and injectivity against
>    a degenerate encoding."*)* That argument proved **idempotence** and claimed **injectivity**,
>    which is its converse. The collision reduction needs an encoding faithful to all 256 bits,
>    and Q6=D′ keeps the label human-readable and citable — necessarily lossy. The third control
>    catches only a **degenerate** encoding, never a **truncating** one. What *is* true: the
>    superseded negative control (delete a directory, attempt a fresh allocation, expect refusal)
>    is **inapplicable** rather than failed, because nothing allocates, and reproducing the same
>    label from the same content is now correct. **Never-reuse is recorded as an obligation on
>    whoever specifies the encoding**, listed as an open item in § Assumptions, and nothing this
>    unit produces may claim it holds until then.
> 2. **Monotonicity — NO LONGER REQUIRED, and deliberately given up.** A content-addressed
>    label cannot express ordering, and no test recovers it: monotonicity is information about
>    *sequence*, which a function of content alone does not carry. Because that is a property of
>    the mechanism rather than of its implementation, it could be resolved only by restoring
>    durable state — which the ruling forbids — or by changing the requirement. **The
>    requirement was changed: Q6 was re-answered on 2026-08-25 as D′, dropping "monotonic"**,
>    put to the owner explicitly rather than assumed. So this is **not an unmet obligation** and
>    **not an open gap against an answered question** *on monotonicity*; the rule is compliant with Q6=D′ **on monotonicity, which D′ dropped — but NOT on never-reuse, which D′ retains and this design does not establish** *(narrowed 2026-08-25 on adversarial finding M-1/M-3 of the restored budget; the unqualified claim "fully compliant with Q6=D′" appeared at five sites and was false at all five)*.
>
>    **What it costs, disclosed rather than absorbed:** release labels can no longer be
>    **ordered**. A reviewer citing two labels at a human-reviewed gate cannot tell from the
>    labels alone which release came first — that must be read from the run record or the
>    experiment registry, both of which carry timestamps and `run_id`. Nothing else in the
>    design depended on label ordering.
>
> **FU-2's integrity obligation is discharged, and FU-2 itself is moot.** FU-2 existed only to
> locate the ledger Q6=D required; with Q6=D′ there is no ledger to place. Its
> inconsistent-mapping obligation is carried by the three negative controls above. Its
> duplicate-and-reused-label obligation is **vacuous**: with no rows there is nothing to
> duplicate, and with the label a function of the hash, reuse across genuinely different
> content would reduce to a SHA-256 collision **only under a 256-bit-faithful encoding, which a citable label is not — this clause is the withdrawn reduction and is retained only as the superseded record** *(disarmed 2026-08-25 on adversarial residual r-1 of the restored budget; R-12 disarms its own instance of the same sentence, and this one was left armed. The conclusion below is independently supported and unaffected.)*. **So FU-2's obligations are covered — but Q6=D′'s
> never-reuse obligation is NOT**, and this sentence previously said otherwise. *(Corrected
> 2026-08-25 on adversarial finding M-3 of the restored budget; superseded wording preserved: "So
> no obligation of either question is left uncovered.")* The SHA-256-collision reduction quoted
> just above is itself the withdrawn argument — it needs a 256-bit-faithful encoding, and a
> citable label is lossy. **Never-reuse is open**, on whoever specifies the encoding.
>
> **This is a deliberate owner override, not an oversight.** The ruling was given after the
> full conflict was put to them: that `ReleaseLedgerEntry` predated Amendment C, that its
> authority was their own **Q6=D** and **FU-2=D** answers, that a `content_hash`-derived
> `dataset_version` is **Q6 option C which they had read and declined** on exactly the
> monotonicity reasoning above, and that executing the reversal would delete an entity and
> amend a workflow. They chose the full reversal with those consequences stated.
>
> **The two loose ends this paragraph named have since been closed — but the reversal did not leave this rule clean.** *(Corrected 2026-08-25 on adversarial finding M-2 of the restored budget; superseded wording preserved: "**Both loose ends have since been closed, and neither by this stage's own choice.**")* Two OPEN items in this file's own § Assumptions exist **because** of this reversal — the `dataset_version` encoding and its injectivity — and this rule's own box states plainly that never-reuse is open.
> Monotonicity was unresolvable here by construction, so **Q6 was re-presented and re-answered
> as D′ on 2026-08-25**, dropping the requirement — the owner's decision, taken explicitly, not
> a silent amendment. And the **upstream correction is no longer owed**: `unit-of-work.md` § 1
> `Owns` and `services.md` were first *reported* rather than edited, because this stage's scope
> control forbade touching an approved Inception artifact; the owner authorised the edits
> explicitly and both were corrected on 2026-08-25 with their superseded wording preserved.
> **What still stands open against this rule, from that reversal — three items, not two** *(count corrected 2026-08-25 on adversarial finding m-3 of the eighth-redo iteration 2: this roll-up named two while this rule's own Constraint names a third, "Closing the read-back hole requires the `verify_release` amendment" — a roll-up narrower than the body it summarises)*: the `dataset_version` **encoding** (unspecified, and stage 3.5 forbidden to choose one), its **injectivity**, and the **`verify_release` amendment** that would close the read-back hole, on which never-reuse depends. *(Corrected 2026-08-25 on adversarial finding M-2 of the restored budget. **Superseded wording, preserved:** "Nothing about the Amendment C reversal now stands open against this rule." It was false when written and sat eighteen lines below this rule's own "**Never-reuse is open**, on whoever specifies the encoding" — the same sentence had already been superseded in the Q&A and was left standing here.)*
>
> **The rule count is unchanged at 17 (R-01–R-17)** — R-12 was amended, not removed.

> **⛔ Amendment C DECLINED AS DRAFTED 2026-08-25.** The box below records the 2026-08-24
> approval that ruling reversed. It is preserved as the dated record and is **not** the current
> state — in particular its *"three artifacts, one authoritative"* reading of `services.md` is
> now wrong at two. **That correction has since been made** — `services.md` reads "Two artifacts, one authoritative" and the ledger row is removed, superseded wording preserved.
>
> **✅ Amendment C APPROVED 2026-08-24** *(superseded 2026-08-25)* (`CR-2026-08-24-FOUNDATION-AMENDMENTS`).
> *Superseded status, preserved:* *"Amendment C is PENDING and NOT approved. The ledger
> is absent from `unit-of-work.md` § 1 `Owns` and from `services.md` § Run record and
> registry ("Two artifacts, one authoritative"). Both approved artifacts are
> unedited."* Both have been annotated in place on the owner's approval;
> `services.md` now reads **three artifacts, one authoritative**.
>
> **Authority: Q6=D and FU-2=D.** Q6=D requires a *monotonic, human-readable* label
> alongside the authoritative hash — chosen over option C's *"version derived from the
> manifest hash"* — and FU-2=D names the durable append-only ledger with its ownership
> and append behaviour. A monotonic label needs durable state, which is why the
> directory scan R-12 rejects cannot serve.
>
> **No TE §12 amendment was needed** — `artifacts/registry/` is already enumerated and
> the tree carries zero file-level entries inside `artifacts/`.

**Acceptance.** TA-15 for the release. **No §16/§19 row accepts `dataset_version` derivation**
— and none is sought: Amendment A, which would have added acceptance rows for this unit's
uncovered obligations, was **declined** on 2026-08-24, with §19 held at 36 rows and TA-37/TA-38
explicitly not to be added. *(Superseded 2026-08-25: "**No §16/§19 row accepts the ledger
itself** … The ledger's own integrity is asserted by the independent test FU-2=D requires, not
by an acceptance row." There is no ledger, so the independent ledger integrity test FU-2=D
required does not exist. **Its inconsistent-mapping obligation is carried** by this rule's
correspondence control; its duplicate-row obligation is **vacuous** with no rows to duplicate.
What is **not** carried is never-reuse, which needs injectivity over the label encoding — recorded
as an open item in § Assumptions rather than as coverage. *(This sentence itself was corrected
2026-08-25 on reviewer finding M-2, second pass: it previously read "no longer exists either — a
loss of coverage this reversal creates and does not replace, and one more item for the stage
gate", which contradicted § Assumptions' own RESOLVED finding on the same obligation.)*)*

## R-13 — A release directory is never overwritten

**Rule (TE §13.3, TA-15).** `write_release` **rejects an output directory that
already contains a release** and **never overwrites existing release content.**

**Constraint.** Repeated writes are **not** silently treated as successful. That
behaviour would require explicit authorisation through the project's change-control
process, and none has been sought.

**Negative control.** The mutation-protection test: write a release, attempt a
second write to the same directory, assert `ReleaseError` and assert the original
bytes are unchanged.

**Acceptance.** TA-15.

## R-14 — `foundation` declares credential names and never touches a value

**Rule (Q8 = D, FU-3 = A).** Required credential environment-variable **names**
live in one centrally reviewed stage/provider mapping. `foundation` **owns or hosts**
that mapping and **does not read, return, log, serialize, interpolate, or persist
any credential value** — not in `resolve_platform_roots`, not in any
foundation-layer diagnostic.

**Constraint — scope of the precondition.** Only stages that **actually require
authenticated provider access** apply the credential-presence check. Credentials
are **not** required for unrelated stages, for public providers, or for
`foundation` initialization itself.

**Constraint — what a presence check does and does not prove.** Checking that an
environment-variable **name** is present **does not** prove its value is non-empty,
valid, or authorized. The provider client performs value validation **without
exposing the secret.** This is stated because a presence check that is mistaken for
a validity check is worse than no check: it reports readiness that does not exist.

**Negative control.** Synthetic canary secrets in the environment, in a config, in
a log line and in an artifact; the secret scan must find each. Assert no
foundation-layer return value or log line contains a canary. Remove a required name
and assert the failing message identifies it by name.

**Constraint — a precondition, not a claim.** The `.gitignore` credential deny-list
**must exist before the first relevant commit.** `NFR-SEC-01` and `TA-22`
compliance is **not claimed until the required checks have actually passed** — and
`evidence.md` records NFR-SEC-01 as **not satisfied in this workspace today**, so
this is a rule being built rather than one being ratified.

**Acceptance.** TA-22.

## R-15 — Only `foundation` reads `configs/`, and nothing reads the restricted root

**Rule (`unit-of-work.md` § 1 boundary).** `foundation` is the **only** unit that
reads `configs/`. Everything downstream receives resolved values, never a path into
`configs/`.

**Rule (§ Shared resources, unqualified).** `foundation` is, with `acquisition`,
one of two units permitted to construct a path into `evidence/` — **except
`evidence/locked_test_restricted/`, which only `src/data/locked_test.py` may
reach.** *"Nothing else may construct a path into it."*

**Why the carve-out is absolute.** D-15 records that the restricted root is a
**governance boundary, not an access control** — it holds only while exactly one
code path reaches it. A second path does not weaken it slightly; it ends it.

**Negative control.** A static check asserting no `foundation` module constructs a
path containing `locked_test_restricted`.

**Acceptance.** Contributes to TA-18 via `governance-guards`; **`foundation`'s own
side is the absence of a path**, which the check above proves.

## R-16 — No machine path enters a governed config

**Rule (REQ-ENG-3, ADR-07).** No machine path may enter any of the four governed
configs, so **moving a directory never changes a governed hash.**

**Constraint.** Machine paths live in `ConfigSnapshot.resolved_roots`, resolved
from the environment at run time.

**Negative control.** A test asserting no value in any of the four configs parses
as an absolute path, and that relocating the workspace leaves all four config
hashes unchanged.

**Acceptance.** **TA-03, TA-26** — REQ-ENG-3 per story-map Table 1. *Superseded: `TA-02`.*

## R-17 — Every module and script carries a purpose/inputs/re-run docstring

**Rule (`project.md` § Mandated, affirmed practice).** Every script and module has
a docstring stating its **purpose**, its **inputs**, and its **re-run /
reproducibility behaviour.**

**Negative control.** A test asserting each module in this unit has a module-level
docstring containing all three elements.

**Acceptance.** **No acceptance row.** The docstring rule is an affirmed practice (`project.md` § Mandated, interview Q12-C), not one of this unit's sixteen requirements, so it is outside the "2 of 16" count and has no §16/§19 row to cite. *Superseded: `TA-01`, which accepts the repository skeleton and does not check docstrings.*

---

## Rules with no acceptance row — stated, not buried

| Rule | Requirement | Status |
|---|---|---|
| Freeze-gate tagging; D-number on every governed change | **REQ-ENG-7** | ⚠ **No §16/§19 row — and none will be added.** Amendment A **DECLINED 2026-08-24**; untested **by design**, permanently *(superseded status: "Amendment A pending")* |
| Per-run environment lock, eight fields populated | **REQ-ENG-10** | ⚠ **No §16/§19 row.** TA-03 verified against all seven §13.1 bullets and covers **none fully**; two partially, both install-time rather than per-run. `requirements.md` records the same conclusion. Amendment A **DECLINED 2026-08-24**; untested **by design**, permanently *(superseded status: "Amendment A pending")* |
| Probe scope, measurement status, declared-vs-observed mismatches | Q3 = C / NFR-DET-01 | ✅ **Fields now in the approved contract** — `DeterminismRecord` carries nine. Amendment B **APPROVED 2026-08-24** *(superseded status: "Fields not in the approved contract. Amendment B pending")* |
| **R-17** — every module and script carries a purpose/inputs/re-run docstring | Human-selected candidate rule, interview Q12-C | ⚠ **No §16/§19 row accepts it.** The convention is observed in both existing scripts and is mandated in `project.md` § Mandated, but no acceptance row tests it; enforcement rides review rather than a gate *(row added 2026-08-25 on adversarial residual r-2 of the eighth-redo iteration 2: R-17 is the other rule in this file declaring no acceptance row, and this table — whose whole purpose is to state them rather than bury them — omitted it)* |
| `dataset_version` derivation integrity — **correspondence and determinism covered** by two of R-12's negative controls; **never-reuse NOT covered** — its third control detects only a *degenerate* encoding, never a *truncating* one, so injectivity is an **OPEN** obligation on the encoding *(corrected 2026-08-25, adversarial finding M-3 of the restored budget; superseded: "**covered by three negative controls** in R-12 (derivation correspondence, derivation determinism, injectivity against a degenerate encoding)")* | **Q6 = D′** (re-answered 2026-08-25); FU-2 moot | ⚠ **Amendment C DECLINED AS DRAFTED 2026-08-25**, so there is no ledger and no `ReleaseLedgerEntry`. *(Glyph corrected 2026-08-25 on adversarial residual r-1 of the eighth-redo iteration 2: this row carried ✅ while its obligation is partly **uncovered**, and rows 1–2 of this table use ⚠ for exactly that state.)* FU-2's inconsistent-mapping obligation is carried by the correspondence control; its **duplicate-row** obligation is **vacuous** — with no ledger there are no rows to duplicate. Its **reused-label** obligation is **NOT** vacuous: that *is* never-reuse, and it **remains uncovered**, pending the encoding's injectivity. *(Corrected 2026-08-25 on adversarial finding of the eighth-redo iteration 1. **Superseded wording, preserved:** "its duplicate-and-reused-label obligation is **vacuous** — no rows to duplicate, and reuse across genuinely different content reduces to a SHA-256 collision." Two defects in one clause: it deployed the **withdrawn** SHA-256-collision reduction as live fact, where R-12 refutes it and preserves it only as superseded — the r-1 sweep removed one deployment and left this one — and it bundled *duplicate-row* with *reused-label* as jointly vacuous when the second is exactly the open obligation the next sentence concedes.)* *(Corrected 2026-08-25 on adversarial finding M-3 of the restored budget; superseded wording preserved: "Nothing is left uncovered." The third control is non-degeneracy, not injectivity, so it cannot cover never-reuse — an OPEN obligation on the label encoding.)* Both upstream sites were **corrected on 2026-08-25** on the owner's explicit authorisation after this stage first reported rather than edited them: `unit-of-work.md` § 1 `Owns` no longer lists the ledger and `services.md` reads *"Two artifacts, one authoritative"* *(superseded statuses, all preserved: "~~Release-label ledger integrity~~ — obligation withdrawn; `dataset_version` derivation carries no integrity test … uncovered, and not replaced"; "✅ **Artifact now in `unit-of-work.md` § 1 `Owns` and `services.md`.** Amendment C **APPROVED 2026-08-24** on the authority of Q6=D and FU-2=D"; and "Artifact not in any approved `Owns` list. Amendment C pending")* |

**Test specifications for REQ-ENG-7 and REQ-ENG-10**, labelled exactly as Q7 = X
directs:

> **Test specification only — not an approved acceptance row and not evidence of a
> passing result.**
>
> **This label is now permanent, 2026-08-24.** It was provisional while Amendment A —
> the Vision §15.2 request Q7=X directed be raised — was pending. The owner **declined**
> that request, so no §19 row will cover REQ-ENG-7 or REQ-ENG-10. These specifications
> remain what they say they are: design targets for stage 3.5, never acceptance
> evidence, and their absence from §19 is the approved *"Open by design"* state rather
> than an outstanding gap.

- **REQ-ENG-7.** Reject a change to a governed scientific constant or governed
  configuration file when the required decision identifier is **missing or
  invalid**; verify the applicable freeze-gate tagging requirements.
- **REQ-ENG-10.** Derive the required environment-lock fields **directly from TE
  §13.1** and fail when any required item is **missing, malformed, or not captured**
  for the applicable run. The eight fields and their seven-bullet provenance are
  enumerated in `domain-entities.md` § 5.

Per Q7, design and implementation planning proceeded while Amendment A was pending.
**Amendment A was DECLINED on 2026-08-24**, so REQ-ENG-7 and REQ-ENG-10 are **untested by
design and permanently** — 2 of this unit's 16 requirements. **Formal acceptance coverage and
gate satisfaction are never claimed for these two**: their negative-path specifications above
are test specifications only, a settled state rather than a provisional one, and their
enforcement rides §18.3's gate-test list and TA-11 rather than a row of their own.

> *(Condition corrected 2026-08-25 on adversarial reviewer finding m-1. **Superseded wording,
> preserved:** "Per Q7, design and implementation planning proceed while Amendment A is
> pending. **Formal acceptance coverage and gate satisfaction are not claimed** until the
> amendment is approved and the tests have executed successfully." Amendment A was declined,
> not approved, so that condition can never be met and the sentence read as deferral where the
> state is permanent — contradicting the acceptance-status box above it. **No new conditional
> dependency on Amendment A is created, and A is not reopened.** No count moved: 16
> requirements, 2 untested, 7 acceptance rows, §19 at 36 rows.)*

## Assumptions & Open Questions

- **[assumption]** The `RequiredFieldsMap` and `CredentialNameMap` are declarative structures **inside `src/data/config.py`**, not governed config files. They name field and variable *identities*, never values, so they carry no scientific constant and TE §12's "exactly four" is untouched. FU-3's stronger form — a seventh module — has no legal home, since TE §12 fixes six `src/` packages.
- **[assumption]** `foundation` hosting `CredentialNameMap` without consuming it is within the boundary. Stated explicitly in R-14 because, unstated, it reads as a boundary violation.
- **Amendments A, B and C — all three ruled, none pending.** **A: DECLINED** (2026-08-24) — REQ-ENG-7 and REQ-ENG-10 untested by design, permanently; §19 held at 36 rows; TA-37/TA-38 not to be added. **B: APPROVED** (2026-08-24) — the three `DeterminismRecord` fields exist, nine in total. **C: DECLINED AS DRAFTED** (2026-08-25, reversing its 2026-08-24 approval) — no release ledger, `ReleaseLedgerEntry` withdrawn, `dataset_version` derived from `content_hash` with no encoding specified here. **Neither A nor C was approved; no amendment authorises execution of anything, and G-09 remains unsigned.**

  *(Corrected 2026-08-25 on adversarial reviewer finding M-2, which was Major. **Superseded wording, preserved:** "**Open — Amendments A, B and C.** All three **PENDING and NOT approved.** Enumerated at this stage's approval gate." That was refuted in the passed contracts at the time it was read, and both sibling artifacts had swept this same bullet while this file's § Assumptions was not — the omission finding M-3 traces to this file's own self-certification. The bullet carried **no numeral**, which is why the 2026-08-24 sweep, keyed to `DeterminismRecord` "six fields" and `services.md` "two artifacts", could not see it.)*

- **OPEN — a cross-unit obligation on the eight exceptions this unit does not raise.** `foundation` owns `IntegrityError` and the stage-entry catch, and R-01 now places **all fourteen** project-defined exceptions in that hierarchy on the authority of `component-methods.md` § Assumptions. Eight of them are **raised by other units** — `PhaseBoundaryError` and `LockedTestError` (`governance-guards`), `LeakageError`, `AlignmentError`, `SeedError`, `FairnessError`, `BootstrapError`, `RegimeError` — and **each of those units' `functional-design` must declare its own exceptions as `IntegrityError` subclasses**. This unit cannot do it for them, and it is recorded here rather than assumed because the omission it replaces would have let a phase-boundary violation exit with **no `aborted` registry row**, against NFR-PHASE-01 and NFR-AUD-01 *(added 2026-08-25 on adversarial finding m-1 of the eighth-redo iteration 2)*. No cycle is created: every one of those units already depends on `foundation`.
- **OPEN — whether `IntegrityError` should move to a dedicated `src/data/exceptions.py`.** This stage declared the hierarchy in **`src/data/config.py`** because TE §12's `src/data/` tree names **nine** modules and **none for exceptions**, so a dedicated module is a **§12 amendment** this stage may not make by assertion. `config.py` works and crosses no import boundary — every unit raising one of the other eight already depends on `foundation`. But a module whose §12 comment reads *"config load, per-run snapshot, hashes, determinism helper"* is not an obvious home for the project-wide exception base, and the fourteen-subclass hierarchy is now project-wide rather than `foundation`-local. **The owner's decision: accept `config.py`, or amend §12 for `src/data/exceptions.py`** *(added 2026-08-25 on adversarial finding M-1 of the ninth-redo iteration 1, whose fix names this item as recorded here — so not creating it would have been the same claim-without-the-thing defect the last three passes each caught)*.
- **OPEN — the `dataset_version` hash-to-label encoding.** *(Added 2026-08-25 on adversarial reviewer finding M-4, which was Major: this decision was stated as unspecified in all three artifacts while appearing as an open item in none of them, and the Q&A simultaneously asserted "Nothing carried to the stage gate as an open item.")* Q6=D′ requires `dataset_version` to be **derived from the release `content_hash`** and human-readable, and **no approved artifact specifies the encoding**. Per TE §18.3 stage 3.5 must **stop and report** rather than choose one. **This blocks concrete work**, which is why it belongs here rather than in a narrative: `dataset_version` is a §13.3 manifest field, W-7 step 5 must produce it, and `src/data/release.py` plus the §18.3-critical `tests/test_release_hashes.py` cannot be completed without it. **The encoding also carries the never-reuse obligation** below. Resolution is a freeze-gate decision, not an implementation choice.
- **OPEN — injectivity of that encoding, and with it the never-reuse property.** Never-reuse is *different content → different label*. The derivation gives idempotence, not injectivity, and a human-readable label is a lossy encoding of a 256-bit hash. Whoever specifies the encoding must make it **injective over the release population in scope**, or state and have accepted its collision bound. Until then `dataset_version` carries **correspondence and determinism guarantees only**, and nothing this unit produces may claim labels are never reused.
- **OPEN — an amendment need on `write_release`'s approved raise-contract.** `component-methods.md` has `write_release` raise `ReleaseError` *"when a field is absent"* over **all fourteen** §13.3 fields. Deriving `dataset_version` inside `write_release` (Q6=D′) narrows the **caller** precondition to thirteen while leaving the **output** obligation at fourteen. The release still carries all fourteen fields, so what the function writes is unchanged — but the caller contract does change, and this stage demanded a formal amendment for exactly this class when it declined to alter `ensure_process_determinism`'s `-> None` signature. Applying a looser standard here would be inconsistent, so this is **the owner's decision, not a settled contract** *(added 2026-08-25 on adversarial finding m-2 of the restored budget; the rule text claimed it was listed here and it was not)*.
- **OPEN — an amendment need on `verify_release`, or acceptance that the correspondence check is test-only.** R-11's and R-12's correspondence negative control was relocated to *"a presented manifest"* without naming what performs it. The only candidate in the approved contracts, `verify_release(manifest_path) -> Sequence[str]`, **does not fit**: it reports files whose *file hash* mismatches and **never raises**, so it covers neither label/hash correspondence nor failure signalling. The control is therefore specified as a **test** obligation on `tests/test_release_hashes.py` (TA-15), which needs no production entry point. **If runtime enforcement is wanted, `verify_release` must be amended** — the owner's decision *(added 2026-08-25 on adversarial finding M-5 of the restored budget; likewise claimed as listed here and not)*.
- **Closed — the three consequences the Amendment C reversal first appeared to carry.** Two closed on analysis and one on an owner ruling; a fourth, listed above, was missed by that analysis and is now open:
  - **The delete-and-rebuild failure — CLOSED.** The superseded R-12's objection was to *allocation from an index*; a pure function of `content_hash` allocates nothing, so that failure cannot arise. *(Superseded 2026-08-25 on finding M-3: this bullet previously read "**Never-reused — RESOLVED, satisfied by determinism**", which overclaimed — determinism disposes of the delete-and-rebuild failure but does not establish never-reuse. See the **encoding** and **injectivity** items above — named rather than counted, because the list grew to four and "the two open items above" would now mislead *(2026-08-25)*.)*
  - **FU-2's inconsistent-mapping obligation — CLOSED**, carried by R-12's correspondence control; its duplicate-row obligation is **vacuous** with no rows to duplicate. *(Superseded on M-3: previously "discharged by three negative controls … stronger than a correspondence check alone". The third control catches only a **degenerate** encoding, never a truncating one, so it cannot stand in for injectivity.)*
  - **Monotonicity — RESOLVED by re-answering the question, not by a mechanism.** Ordering is information about *sequence*, which a function of content alone cannot carry, so no test recovers it and no implementation choice reaches it. **Q6 was therefore re-presented and re-answered as D′ on 2026-08-25**, dropping "monotonic" — the owner's explicit decision, not an assumed amendment, with the original Q6=D answer preserved verbatim beside it. R-12 is compliant with Q6=D′ **on monotonicity — but NOT on never-reuse, which D′ retains and this design does not establish** *(narrowed 2026-08-25 on adversarial finding M-1/M-3 of the restored budget; this was the fifth and last unqualified "fully compliant with Q6=D′")*. **What was given up on the ordering side, and it is a capability rather than an unmet obligation:** release labels can no longer be ordered, so a reviewer comparing two labels at a gate must read sequence from the run record or the experiment registry instead. Nothing else in this design depended on label ordering. **FU-2 is moot** — it existed only to locate the ledger Q6=D required.
  - **The two upstream artifacts are no longer open.** `unit-of-work.md` § 1 `Owns` and `services.md` both named a ledger this design no longer has; they were first **reported** rather than edited, because this stage's scope control forbade editing an approved Inception artifact, and the owner then authorised the edits explicitly on 2026-08-25. Both were corrected the same day, superseded wordings preserved, and a search across `construction/` confirmed no other unit referenced the ledger.
- **Open** — the concrete contents of both maps cannot be enumerated until the four configs exist. This stage fixes the mechanism; the populated maps are Bolt 1 work products.
- **G-09 is not signed.** No rule here authorises creating any module.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

## Review history

| Pass | Verdict | Effect on this file |
|---|---|---|
| Iteration 1 (adversarial) | **NOT-READY** | Not reached by the finding. Its critical finding was against the two traceability tables in `business-logic-model.md` and `domain-entities.md` |
| Between passes | — | **This file was found to carry the same defect class** in its per-rule `**Acceptance.**` lines and was corrected: R-05, R-06, R-07, R-08, R-09, R-16 and R-17. Every superseded citation preserved inline |
| Iteration 2 (adversarial) | **NOT-READY** | Re-derived this file's acceptance lines cell by cell against story-map Table 1 and **confirmed all now match the source**. Its two new findings were against `domain-entities.md` only |
| Redo jump, 2026-08-22 | — | Budget was exhausted at 2 of 2 with post-review corrections outstanding. The project decision owner directed a re-review of `foundation` before any further unit; the jump reset the iteration budget and the receipt floor |
| Iteration 1 of the fresh budget | ~~*pending*~~ → **NOT-READY**, completed 2026-08-24 | *(Row corrected 2026-08-25 on reviewer finding m-4 — iteration-1 of the 2026-08-25 pass had named this same row's class explicitly and it was left un-swept. Superseded effect cell: "This file is unchanged in substance since iteration 2 cleared its acceptance lines.")* **Four passes have run since**: 2026-08-24 iteration 1 (NOT-READY) and 2 (READY), then 2026-08-25 iteration 1 (NOT-READY, seven findings) and 2 (NOT-READY, five Major). This file is **no longer unchanged in substance**: R-11's rule text, R-12 in full, R-06's heading and acceptance reason, R-05's sentinel constraint, and § Assumptions all changed |

**What iteration 2 explicitly cleared here.** The per-rule acceptance citations, the
two-tier posture, R-14's credential-boundary statement, and the pending-amendment
discipline in R-06 and R-12 — all checked against source and found correct.

---

## Finalized 2026-08-24 — the three amendments are settled

Recorded under `governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md`, after
an independent challenge of each amendment against the approved artifacts.

- **Amendment A — DECLINED.** No project rule requires universal §19 coverage, and the approved position dispositions uncovered requirements as *"Open by design"*. **REQ-ENG-7 and REQ-ENG-10 are untested by design, permanently rather than pending.** No count moved: untested stays 36, this unit's stays 2 of 16, its acceptance rows stay 7, TE §19 stays at 36 rows.
- **Amendment B — APPROVED.** `DeterminismRecord` carries **nine** fields. R-05's prohibition on stating that determinism was measured is **discharged** and replaced by a narrower rule: a measured claim requires `probe_scope` recorded and `measurement_status` = `complete`. **R-06 is unchanged** — an empty `nondeterministic_ops` is never proof of determinism.
- **Amendment C — DECLINED AS DRAFTED 2026-08-25**, reversing its 2026-08-24 approval. No release ledger; `ReleaseLedgerEntry` withdrawn; `dataset_version` derived from `content_hash`, encoding unspecified here. **R-11 is unchanged in substance** — the content hash remains authoritative — though its **rule text was amended 2026-08-25** to cite Q6=D′ and strike "monotonic" (reviewer finding M-1; the earlier blanket "R-11 is unchanged" is exactly what hid that). **R-12 is amended, not deleted**, and records what the derivation provides and what it does not. *(Superseded status, preserved: "**Amendment C — APPROVED**, on the authority of **Q6=D** and **FU-2=D** rather than as an engineering preference. A draft of the change record proposed rejecting it and deriving the label from the content hash; that is Q6 option C, which the owner had read and declined, and it cannot yield the *monotonic* label Q6=D requires. The rejection was withdrawn.")*

  **The withdrawn rejection is now the ruling.** What the superseded text describes as a proposal the owner had already declined — deriving the label from the content hash, Q6 option C — is what the 2026-08-25 ruling mandates. That ruling was given after this exact reasoning, and the owner's own Q6=D and FU-2=D answers, were put to them in full. It is a deliberate override with its consequences stated. **Both items that reasoning left open are now closed**: monotonicity by the Q6=D′ re-answer, and the upstream contradiction by the two authorised corrections of 2026-08-25. **What replaced them as open is narrower and more concrete** — the hash-to-label encoding, and the injectivity that never-reuse depends on; both are listed in § Assumptions.

The negative-path test specifications for REQ-ENG-7 and REQ-ENG-10 keep their
*"Test specification only — not an approved acceptance row"* label as a **settled**
state rather than a provisional one.

**G-09 remains unsigned.** Nothing in this document authorises creating a module, and
no scientific value is decided here.

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

> **Re-saved 2026-08-25 under the sixth post-redo receipt floor.** The stage wedged on
> `models-and-baselines`: its artifacts were written and the adversarial reviewer returned
> READY on iteration 2 of 2 (2026-08-24T15:16:47Z) *before* its summary confirmation was
> recorded (15:32:45Z). The engine requires a produces-artifact write after the confirmation
> receipt, the write-freeze hook refused the re-save because a fresh READY receipt covered the
> unit, and the 2-iteration adversarial budget was spent — a deadlock whose only sanctioned
> exit is a redo jump. The project decision owner authorised one at **2026-08-25T06:30:05Z**,
> which reset the receipt floor for every unit of the stage.
>
> **No rule in this document changed.** The owner directed **evidence-driven revision** for
> this recovery — keep the adversarially-verified text as the baseline and edit only where a
> real defect is found — rather than a blanket re-derive, on the finding that all eight built
> units already carry a READY `## Review` section and that a blanket rewrite would discard
> verified corrections. The unit's figures were re-derived programmatically from the current
> `unit-of-work.md` § 1 — **16** requirements, **2** untested (REQ-ENG-7, REQ-ENG-10), **7**
> acceptance rows — each agreeing with the per-rule acceptance lines below.
>
> **Upstream provenance, enumerated per file** *(corrected 2026-08-25 on reviewer finding m-5;
> **superseded wording, preserved:** "Every consumed upstream file was last modified at 12:26
> UTC, three hours before this unit's 15:27 UTC artifacts and committed unchanged at
> `9c7afd9`" — true of three of the six, and the derivation had never enumerated its scope)*:
>
> | Consumed artifact | Last modified | Commit |
> |---|---|---|
> | `unit-of-work.md` | 2026-08-24 12:26 UTC | `9c7afd9` |
> | `component-methods.md` | 2026-08-24 12:26 UTC | `9c7afd9` |
> | `services.md` | 2026-08-24 12:26 UTC | `9c7afd9` |
> | `unit-of-work-story-map.md` | 2026-08-23 20:40 UTC | `45796f5` |
> | `components.md` | 2026-08-23 19:05 UTC | `45796f5` |
> | `requirements.md` | 2026-08-22 12:37 UTC | `89674b6` |
>
> **The no-drift conclusion is unchanged**: every one of the six predates this unit's 15:27 UTC
> artifacts, so none of them moved under this unit's design.
>
> **The seventeen rules R-01–R-17**, their IDs and their acceptance citations are unchanged.
> *(Count corrected 2026-08-25 on reviewer finding M-1, which was Major. **Superseded wording,
> preserved:** "The thirteen rules, their IDs and their acceptance citations are unchanged."
> Thirteen was carried from the prose of an earlier section rather than derived;
> `grep -cE "^## R-[0-9]+" business-rules.md` returns **17**, and
> `business-logic-model.md` § Implementability already read "the seventeen rules (R-01–R-17)"
> correctly, so the two artifacts contradicted each other. **The rule set did not change — the
> figure was misreported.** No requirement, acceptance or §19 total moved because of this
> correction: 16 requirements, 2 untested, 7 acceptance rows, §19 at 36 rows.)*
>
> **G-09 remains unsigned**, so no rule here authorises creating a module.

---

> **Re-saved 2026-08-25 after the remediation of the iteration-1 findings**, under the receipt
> recorded for this unit at the sixth post-redo floor.
>
> **Rules changed in this file, and only these:**
>
> - **R-12 rewritten.** `dataset_version` is now **derived from the release `content_hash`**, on
>   the authority of **Q6 = D′** (re-answered 2026-08-25; the original Q6 = D is preserved
>   verbatim in the Q&A file). No ledger, no allocation step, no `ReleaseLedgerEntry`, and **no
>   hash-to-label encoding invented here** — none is specified by any approved artifact, and per
>   TE §18.3 stage 3.5 must stop and report rather than choose one. The superseded rule is
>   preserved verbatim in the box beneath it, together with the analysis of which of its
>   objections transfers to a derivation and which does not. **Three negative controls** replace
>   the ledger's: derivation correspondence, derivation determinism, and injectivity against a
>   a degenerate encoding — **not** injectivity, and so **not** never-reuse. **R-11 is unchanged in substance** (the content hash remains authoritative); its rule text was amended 2026-08-25 to cite Q6=D′ and strike "monotonic".
> - **R-05 gained one constraint**, naming the sentinel environment variable that carries
>   `reexec_performed` across the `exec` boundary (reviewer finding m-3, owner-decided). Without
>   it R-05's own negative control could not discriminate.
> - **R-06's heading and acceptance reason corrected** (m-2, M-4); its conclusion is unchanged
>   and re-evidenced.
>
> **The rule count is unchanged at 17 (R-01–R-17)** — R-12 was amended, never removed, and no
> rule was added. Derived, not carried: `grep -cE "^## R-[0-9]+" business-rules.md` → **17**.
>
> **Every other figure is untouched**: 16 requirements, 2 untested, 7 acceptance rows, §19 at 36
> rows with no TA-37/TA-38 added. **G-09 remains unsigned**, and no scientific value was decided
> by any rule in this file.

---

> **Re-saved 2026-08-25 after the iteration-2 remediation**, under the receipt recorded for this
> unit at the **seventh** post-redo floor. That redo was authorised because iteration 2 returned
> NOT-READY with five Major findings and a spent budget, which the terminal receipt would
> otherwise have frozen in place.
>
> **Rules changed in this file, and only these:**
>
> - **R-11 — rule text corrected (Major finding M-1).** It cited `Q6 = D` and required a
>   **monotonic** label; both were refuted by Q6=D′, which states verbatim *"Drop 'monotonic.'"*,
>   while R-12 twelve lines below already cited D′ — two adjacent rules citing different
>   authorities for one decision. Now `Q6 = D′` with "monotonic" struck, superseded rule preserved
>   verbatim. Its **negative control** was corrected too (m-2): the limb binding one hash to two
>   labels is **unconstructable** once the label is a function of the hash, and is replaced by a
>   check on a **presented** manifest. The three earlier assertions that *"R-11 is unchanged"* —
>   true of its substance, false of its text, and standing exactly where the check should have
>   been — are all qualified.
> - **R-12 — the never-reuse claim corrected (Major finding M-3).** The rule had argued that
>   determinism replaced the ledger's never-reuse guarantee. It does not: purity gives
>   **idempotence**, and never-reuse is its converse, **injectivity**. The collision reduction
>   needs an encoding faithful to all 256 bits, and D′ keeps the label human-readable and citable
>   — necessarily lossy — with the encoding unspecified and 3.5 forbidden to choose one. The rule
>   now states plainly what the derivation provides and what it does not; its third negative
>   control is labelled as catching only a **degenerate** encoding rather than a truncating one;
>   and never-reuse is carried as an **obligation on whoever specifies the encoding**. Nothing
>   this unit produces may claim release labels are never reused.
> - **R-05 — one constraint added (m-3), and it fixes a correctness bug.** The sentinel carrying
>   `reexec_performed` must be **unset by the child immediately after reading**. Environment
>   variables are inherited and `PYTHONHASHSEED` is already set after a re-exec, so without the
>   pop a subprocess of a re-exec'd stage script would record `True` without ever re-execing —
>   making this rule's own negative control pass for the wrong reason.
> - **§ Assumptions — two open items added at that time (Major finding M-4); the section carried four as of that pass — it now carries **five** *(the word "now" corrected 2026-08-25 on adversarial finding m-3 of the ninth-redo iteration 1: a dated record may state what was true then, but "now" asserts the present, so the historical-record defence did not hold)*:** the hash-to-label encoding, and
>   its injectivity. Both had been stated as unresolved in the prose of all three artifacts while
>   appearing as an open item in none of them.
> - **§ Sources — the Technical Environment document added.** Cited ten times in these rules and
>   listed in no source entry across two adversarial passes, with an unresolved `<TE>` placeholder
>   in its printed derivations. The path resolves; the three figures it blocked now derive and
>   agree, including **36** §19 rows — a figure this unit had been carrying rather than deriving.
>
> **The rule count is unchanged at 17 (R-01–R-17)** — R-05, R-11 and R-12 were amended, none added
> or removed. Derived: `grep -cE "^## R-[0-9]+" business-rules.md` → **17**.
>
> **Every other figure is untouched**: 16 requirements, 2 untested, 7 acceptance rows, §19 at 36
> rows with no TA-37/TA-38 added. **G-09 remains unsigned**, and no rule here decides a scientific
> value.

---

> **Re-saved 2026-08-25 after remediating the restored budget's iteration-1 findings**, under the
> receipt recorded for this unit at that iteration's floor.
>
> **What changed in these rules:**
>
> - **R-11 — the compliance claim narrowed (M-1/M-3).** It read *"the rule is fully compliant with
>   Q6=D′"* without qualification. Compliance holds **on monotonicity**, which D′ dropped, and
>   **fails on never-reuse**, which D′ retains and this design does not establish. That unqualified
>   sentence appeared at **five** sites across the unit and was false at all five; every one is now
>   narrowed. Its **negative control** also names its owner: `tests/test_release_hashes.py`
>   (TA-15), because relocating the correspondence check to *"a presented manifest"* had left it
>   with **no owning function** — `verify_release` returns `Sequence[str]` and never raises, so it
>   does not fit (M-5).
> - **R-12 — the never-reuse residue swept (M-3).** Two roll-ups in this file still declared
>   *"Nothing is left uncovered"* and *"no obligation of either question is left uncovered"*, both
>   contradicting this rule's own box. Corrected, superseded wording preserved. The third negative
>   control is renamed **non-degeneracy**: calling it *"injectivity against a degenerate **or
>   truncating** encoding"* was **affirmatively false**, since this rule states plainly that a
>   truncating encoding **passes** the two-sample check (m-1).
> - **R-05 — the sentinel's reader and timing named (m-3).** The pop is performed by
>   `ensure_process_determinism` itself at W-1 step 1, the first statement of every stage script's
>   `main()`, so it precedes any stage logic and therefore any subprocess. The earlier *"before any
>   subprocess is launched"* named no actor and was unsatisfiable standing alone.
> - **§ Assumptions — two further open items (m-2, M-5).** An **amendment need on
>   `write_release`**'s approved raise-contract, since deriving `dataset_version` narrows the caller
>   precondition from fourteen fields to thirteen while leaving the output obligation at fourteen;
>   and an **amendment need on `verify_release`**, or acceptance that the correspondence check is
>   test-only. Both had been asserted in the rule text as *"recorded in § Assumptions"* while being
>   absent from it — the same defect class this pass was fixing. This section now carries **four**
>   OPEN items, equal to both sibling artifacts, verified rather than assumed.
>
> **The rule count is unchanged at 17 (R-01–R-17)** — R-05, R-11 and R-12 amended, none added or
> removed. Derived: `grep -cE "^## R-[0-9]+" business-rules.md` → **17**.
>
> **Every other figure is untouched**: 16 requirements, 2 untested, 7 acceptance rows, §19 at 36
> rows with no TA-37/TA-38 added. **G-09 remains unsigned**, and no rule here decides a scientific
> value.

---

> **Re-saved 2026-08-25 after remediating the restored budget's iteration-2 findings**, under the
> receipt recorded at the **eighth** post-redo floor.
>
> **What changed in these rules:**
>
> - **R-05 — the in-process carrier named (m-1), the one finding that blocked implementation.** The
>   sentinel's journey across the `exec` boundary was specified; **where the bit lives between the
>   pop at W-1 step 1 and the record at W-4 step 4 was not.** Nothing available could hold it —
>   `ensure_process_determinism` returns `None`, `seed_everything(snapshot, *, stage)` takes no such
>   argument, and `ConfigSnapshot` is built at step 2, *after* the pop at step 1. Resolved as
>   **module-level state inside `src/data/config.py`**: setter and reader in the same owned module,
>   so the hand-off is intra-module and **no approved stage-2.6 signature changes**. Every
>   alternative alters an approved contract.
> - **R-12 — the mismatch constraint scoped (m-2).** It asserted an unscoped *"raises"* while
>   § Assumptions item 4 records that `verify_release` never raises. Now **rejected on the write
>   path** and **detected on read-back by the test control only**, with that hole named as requiring
>   the `verify_release` amendment. Its **negative control** further records that
>   `tests/test_release_hashes.py` **already exists** — 12,281 bytes, zero `dataset_version`
>   references, verified directly — so stage 3.5 **extends** rather than creates; and that
>   `team-practices.md`'s *"No `tests/` directory exists yet in the workspace"* is consequently
>   **stale, reported here rather than corrected**, because `org.md` reserves that file for the
>   practices-affirmation gate.
> - **Two live sentences corrected (M-2).** *"Both loose ends have since been closed"* and
>   *"**Nothing about the Amendment C reversal now stands open against this rule**"* — the second
>   standing eighteen lines below this rule's own *"Never-reuse is open"*, in a file whose
>   § Assumptions lists two OPEN items created by that very reversal. Both superseded in place, and
>   the second now names what **does** stand open.
> - **One surplus justification disarmed (r-1).** The withdrawn SHA-256-collision reduction was
>   still deployed as support in one place, where R-12 disarms its own instance of the same
>   sentence. The conclusion it decorated is independently supported and unaffected.
>
> **The rule count is unchanged at 17 (R-01–R-17)** — R-05 and R-12 amended, none added or removed.
> Derived: `grep -cE "^## R-[0-9]+" business-rules.md` → **17**. **§ Assumptions carries four OPEN
> items**, equal to both siblings and verified rather than assumed.
>
> **Every other figure is untouched**: 16 requirements, 2 untested, 7 acceptance rows, §19 at 36
> rows, no TA-37/TA-38. **G-09 remains unsigned**, and no rule here decides a scientific value.

---

> **Re-saved 2026-08-25 after remediating the eighth-redo iteration-1 findings.** That pass returned
> **zero Majors** — the first on this unit — and confirmed **R-05's module-level carrier sound** on
> four independent angles, including that it is set in the child rather than the parent and that it
> improves testability over an inherited environment variable.
>
> **Two corrections land in this file, both on the same subject:**
>
> - **The r-1 sweep was half-done.** § Rules with no acceptance row still asserted the **withdrawn**
>   SHA-256-collision reduction **as live fact**, in the row a human reads at the gate, while R-12
>   refutes it and preserves it only as superseded. The reviewer derived the half-sweep as
>   `git show HEAD | grep -c` → **3** against a working tree of **2**. The same cell also
>   **self-contradicted**: it called the *duplicate-row* and *reused-label* obligations jointly
>   *"vacuous"* when a **reused label *is* never-reuse**, which its own next sentence concedes as
>   uncovered. Now split — duplicate-row **is** vacuous with no ledger and no rows; reused-label is
>   **not**, and remains uncovered pending the encoding's injectivity. The collision clause is
>   preserved as superseded.
> - **Three stale count-in-prose references, fixed by naming.** *"See the two open items above"* now
>   names the **encoding** and **injectivity** items, and the two dated records of *"two open items
>   added"* now read **added at that time; the section carried four as of that pass — it now carries **five** *(the word "now" corrected 2026-08-25 on adversarial finding m-3 of the ninth-redo iteration 1: a dated record may state what was true then, but "now" asserts the present, so the historical-record defence did not hold)***. Each was accurate when
>   written and went stale silently when the list grew from two to four. **A count embedded in prose
>   cannot be swept reliably; a name can** — which is the actual remedy for the class that has
>   recurred through six passes on this unit.
>
> **No rule changed.** The count stays **17 (R-01–R-17)**; derived:
> `grep -cE "^## R-[0-9]+" business-rules.md` → **17**. § Assumptions still carries **four** OPEN
> items, equal to both siblings.
>
> **Every other figure is untouched**: 16 requirements, 2 untested, 7 acceptance rows, §19 at 36
> rows, no TA-37/TA-38. **G-09 remains unsigned**, and no rule here decides a scientific value.

---

> **Re-saved 2026-08-25 after remediating the eighth-redo iteration-2 findings**, under the receipt
> recorded at the **ninth** post-redo floor. *(A further re-save the same day, under the final
> acceptance receipt, follows in the box at the end of this file.)*
>
> **R-01's enumeration was wrong, and it was the one defect in this unit that would have propagated
> into code.** It named **six** `IntegrityError` subclasses. W-1 step 4 raises `PhaseBoundaryError`,
> and R-10 has the stage entry contract catch `IntegrityError` to write the `aborted` registry row —
> so with `PhaseBoundaryError` outside the enumerated hierarchy, an `except IntegrityError` would let
> a **phase-boundary violation exit with no `aborted` row**, precisely the event **NFR-PHASE-01** and
> **NFR-AUD-01** most require recorded. Six adversarial passes did not examine it.
>
> **Settled from upstream authority, not judgement.** `component-methods.md` § Assumptions places
> **fourteen** project-defined exceptions in a shared base and defers placement *"until 3.1 places
> them"* — and this stage **is** 3.1. R-01 now names all fourteen: **six raised here**
> (`ConfigError`, `PreflightError`, `PlatformError`, `DeterminismError`, `ReleaseError`,
> `RegistryError`) and **eight raised by other units on the same base** (`PhaseBoundaryError`,
> `LockedTestError`, `LeakageError`, `AlignmentError`, `SeedError`, `FairnessError`,
> `BootstrapError`, `RegimeError`). Its *"why a base and not six independents"* rationale — which had
> inherited the wrong count — now reads **fourteen**. **This is the failure R-01's own rationale
> predicted**, arriving as a missing **enumeration entry** rather than a missing catch clause.
>
> **Four further corrections in this file:**
>
> - **R-12's box heading** read *"ONE CAPABILITY, NO LONGER AN UNMET OBLIGATION"*, refuted by its own
>   body twenty-six lines below. The previous sweep reported zero live sites because **it matched the
>   words *never-reuse* and this heading contains neither** — the seventh appearance of this class,
>   and the reason the durable remedy is to **name** what is open rather than characterise it.
> - **R-12's roll-up** named two open items where its own Constraint names a third, the
>   `verify_release` read-back hole. Now three.
> - **§ Rules with no acceptance row** gained **R-17**, the other rule in this file declaring no
>   acceptance row, which a table whose stated purpose is *"stated, not buried"* had omitted; and the
>   ⚠ glyph now marks the row whose obligation is uncovered, matching rows 1–2.
> - **§ Assumptions gained a fifth OPEN item**: the cross-unit obligation that the eight exceptions
>   other units raise must be declared as `IntegrityError` subclasses **by those units**. This unit
>   cannot do it for them, and `governance-guards` owns `PhaseBoundaryError`. No cycle — each of those
>   units already depends on `foundation`.
>
> **No rule was added or removed.** The count stays **17 (R-01–R-17)**; derived:
> `grep -cE "^## R-[0-9]+" business-rules.md` → **17**. R-01 and R-12 were amended.
> **§ Assumptions now carries five OPEN items (5/5/5 across the artifacts)** — the boxes above say
> *"four"*, which was true when each was written and is not a current-state claim.
>
> **Every other figure is untouched**: 16 requirements, 2 untested, 7 acceptance rows, §19 at 36
> rows, no TA-37/TA-38. **G-09 remains unsigned**, and no rule here decides a scientific value.


---

> **Re-saved 2026-08-25 under the final acceptance receipt.** The project decision owner ruled to
> accept this unit with its defects disclosed and move to unit 2; one confirming reviewer pass
> records the final state. **Six OPEN items stand in § Assumptions (6/6/6 across the artifacts)**,
> including the two decided-here engineering placements (`IntegrityError` declared in
> `src/data/config.py`; the sentinel and its module-level in-process carrier) and the four that
> await the owner or another unit. The rule count is unchanged at **17 (R-01–R-17)**. A reader at
> the stage gate should treat § Assumptions and this box as authoritative and any count embedded in
> older prose as historical. **G-09 remains unsigned.** *(This box was first appended by a script
> write and is re-saved here with the native tooling so the acceptance state carries its audit
> event — the same discipline `project.md` § Corrections records for shell-written artifacts.)*

---

> **Re-saved 2026-08-25 under the tenth-redo receipt.** The final confirming pass found one genuine
> specification gap — the canonical representation `content_hash` is computed over — and the owner
> ruled to fix it alone. **R-11 now specifies it in full**: twelve included caller-supplied fields;
> `dataset_version`, `created_at_utc` and `content_hash` itself excluded; RFC 8785 canonical JSON
> then SHA-256; three content→hash negative controls, including change-only-`created_at_utc` → same
> hash, which proves the idempotence claim. **R-05/W-4's guard is now observable**
> (`"tensorflow" in sys.modules`, checked before `seed_everything`'s own deferred import) and the
> **module-scope framework-import prohibition binds every stage script**, not only `config.py`. The
> rule count is unchanged at **17**; the final pass's documentation findings stand unfixed per the
> ruling, recorded in `business-logic-model.md`'s final `## Review`. **G-09 remains unsigned.**

---

> **Re-saved unchanged 2026-08-25 under the twelfth receipt** (eleventh redo, taken for
> `acquisition`; floor reset mechanical). Byte-identical to the terminal-READY state.
> **G-09 remains unsigned.**

---

> **Re-saved unchanged 2026-08-26 under the thirteenth receipt** (twelfth redo, taken for
> `inventory-and-registry`; floor reset mechanical). **No content of this unit changed.**
> **G-09 remains unsigned.**

---

> **Re-saved unchanged 2026-08-26 under the fourteenth-redo re-confirmation receipt** (redo taken
> for `external-products`; floor reset mechanical). **No content of this unit changed.**
> **G-09 remains unsigned.**