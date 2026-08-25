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

**Rule.** `ConfigError`, `PreflightError`, `PlatformError`, `DeterminismError`,
`ReleaseError` and `RegistryError` all derive from `IntegrityError`, and so does
any future integrity-related exception.

**Constraint.** Every `IntegrityError` **must** carry the affected file or resource
and the violated expectation. The constructor requires both, so the two-tier
message format is enforced by construction rather than by convention.

**Why a base and not six independents.** The stage entry contract must catch *any*
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
already been initialised. Enabling op determinism afterwards is not equivalent, and
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

**Rule (Q6 = D).** The **content-derived SHA-256 is the authoritative release
identity.** The monotonic human-readable label exists for review and citation and
is **explicitly not authoritative.**

**Constraint.** The authoritative hash is derived from a canonical manifest or
content representation that **excludes** the human-readable label, volatile
metadata, and any self-referential hash field.

**Constraint.** A label/hash mismatch is an **integrity violation** — not a
discrepancy to reconcile.

**Why the hash wins.** Every integrity guarantee in this project is hash-based.
Making the label authoritative would put the weaker identifier in charge. The
project's gates are human-reviewed, so a citable label is needed; stating which one
wins is the part that must not be left implicit.

**Negative control.** Bind a label to two different content hashes, and a content
hash to two labels; both must raise.

**Acceptance.** TA-15.

## R-12 — `dataset_version` is derived from the release `content_hash`

**Rule (Q6 = D′, re-answered 2026-08-25 — supersedes Q6 = D and moots FU-2 = D).** `dataset_version` is
**derived from the release's `content_hash`**. There is **no release ledger**, no allocation
step and no `ReleaseLedgerEntry`. **The exact hash-to-label encoding is NOT specified here**,
because no approved artifact specifies one — and stage 3.5 must **not** choose one either: per
TE §18.3 it must stop and report rather than pick a default.

**Constraint.** `dataset_version` is never authoritative. Release identity is the
`content_hash` (R-11, unchanged). A `dataset_version` that does not match its release's
`content_hash` raises.

**Constraint — determinism, which is what replaces the ledger's guarantee.** The derivation is a
**pure function of `content_hash`**: identical content yields an identical `dataset_version`,
and there is no allocation step and no state to consult. Two consequences follow, and they are
the reason the never-reused obligation survives the reversal:

1. **The delete-and-rebuild failure the superseded R-12 rejected a derived index for cannot
   occur here.** That failure required *allocation from an index*: delete a release directory,
   the rebuilt index forgets the label, and the next allocation hands it out again. A pure
   derivation allocates nothing and consults nothing, so there is no index to forget and no
   next allocation to corrupt. Deleting and rebuilding a release from the same content
   reproduces the same label **by construction** — which is the correct behaviour, not a
   collision.
2. **A label bound to two different contents reduces to a SHA-256 collision.** It is not
   reachable by any bookkeeping error, because the label is a function of the hash.

**Negative controls.** Three, replacing the ledger-specific set:

- Present a manifest whose `dataset_version` does not correspond to its `content_hash`; it must
  be refused. *(This is the derivation-correspondence check, and it is what discharges FU-2=D's
  integrity obligation in the form the ruling leaves available.)*
- Derive twice from the same `content_hash` and require **byte-identical** results —
  determinism asserted, not assumed, the same posture NFR-DET-01 takes everywhere else.
- Derive from two different `content_hash` values and require **different** results, so a
  degenerate or truncating encoding is caught rather than passing silently.

> ## ⚠ WHAT THIS RULE GIVES UP — ONE CAPABILITY, NO LONGER AN UNMET OBLIGATION
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
> 1. **Never-reused — SATISFIED, by a different mechanism.** Not by durable state but by
>    determinism: identical content derives an identical label by construction, and a label
>    bound to two genuinely different contents reduces to a **SHA-256 collision**, unreachable
>    by any bookkeeping error. The superseded negative control (delete a directory, attempt a
>    fresh allocation, expect refusal) is not *failed* — it is **inapplicable**, because nothing
>    allocates; reproducing the same label from the same content is now the correct outcome.
>    Three replacement negative controls are stated above, and they are **stronger than a
>    correspondence check alone**: correspondence, derivation determinism, and injectivity
>    against a degenerate encoding.
> 2. **Monotonicity — NO LONGER REQUIRED, and deliberately given up.** A content-addressed
>    label cannot express ordering, and no test recovers it: monotonicity is information about
>    *sequence*, which a function of content alone does not carry. Because that is a property of
>    the mechanism rather than of its implementation, it could be resolved only by restoring
>    durable state — which the ruling forbids — or by changing the requirement. **The
>    requirement was changed: Q6 was re-answered on 2026-08-25 as D′, dropping "monotonic"**,
>    put to the owner explicitly rather than assumed. So this is **not an unmet obligation** and
>    **not an open gap against an answered question**; the rule is fully compliant with Q6=D′.
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
> content reduces to a SHA-256 collision. So no obligation of either question is left uncovered.
>
> **This is a deliberate owner override, not an oversight.** The ruling was given after the
> full conflict was put to them: that `ReleaseLedgerEntry` predated Amendment C, that its
> authority was their own **Q6=D** and **FU-2=D** answers, that a `content_hash`-derived
> `dataset_version` is **Q6 option C which they had read and declined** on exactly the
> monotonicity reasoning above, and that executing the reversal would delete an entity and
> amend a workflow. They chose the full reversal with those consequences stated.
>
> **Both loose ends have since been closed, and neither by this stage's own choice.**
> Monotonicity was unresolvable here by construction, so **Q6 was re-presented and re-answered
> as D′ on 2026-08-25**, dropping the requirement — the owner's decision, taken explicitly, not
> a silent amendment. And the **upstream correction is no longer owed**: `unit-of-work.md` § 1
> `Owns` and `services.md` were first *reported* rather than edited, because this stage's scope
> control forbade touching an approved Inception artifact; the owner authorised the edits
> explicitly and both were corrected on 2026-08-25 with their superseded wording preserved.
> Nothing about the Amendment C reversal now stands open against this rule.
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
by an acceptance row." There is no ledger, so **the independent integrity test FU-2=D required
no longer exists either** — a loss of coverage this reversal creates and does not replace, and
one more item for the stage gate.)*

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
| `dataset_version` derivation integrity — **covered by three negative controls** in R-12 (derivation correspondence, derivation determinism, injectivity against a degenerate encoding) | **Q6 = D′** (re-answered 2026-08-25); FU-2 moot | ✅ **Amendment C DECLINED AS DRAFTED 2026-08-25**, so there is no ledger and no `ReleaseLedgerEntry`. FU-2's inconsistent-mapping obligation is carried by the correspondence control; its duplicate-and-reused-label obligation is **vacuous** — no rows to duplicate, and reuse across genuinely different content reduces to a SHA-256 collision. **Nothing is left uncovered.** Both upstream sites were **corrected on 2026-08-25** on the owner's explicit authorisation after this stage first reported rather than edited them: `unit-of-work.md` § 1 `Owns` no longer lists the ledger and `services.md` reads *"Two artifacts, one authoritative"* *(superseded statuses, all preserved: "~~Release-label ledger integrity~~ — obligation withdrawn; `dataset_version` derivation carries no integrity test … uncovered, and not replaced"; "✅ **Artifact now in `unit-of-work.md` § 1 `Owns` and `services.md`.** Amendment C **APPROVED 2026-08-24** on the authority of Q6=D and FU-2=D"; and "Artifact not in any approved `Owns` list. Amendment C pending")* |

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

- **Open — one item only, and it is with the owner rather than with this stage.** Of the three consequences the Amendment C reversal first appeared to carry, two are resolved and one is not:
  - **Never-reused — RESOLVED, satisfied by determinism.** The superseded R-12's objection was to *allocation from an index*; a pure function of `content_hash` allocates nothing, so the delete-and-rebuild failure cannot arise. See the box under R-12.
  - **FU-2=D's integrity obligation — RESOLVED, discharged by three negative controls** (derivation correspondence, derivation determinism, injectivity against a degenerate encoding), which are stronger than a correspondence check alone. The ledger's duplicate-row checks are vacuous once no rows exist and the label is a function of the hash.
  - **Monotonicity — RESOLVED by re-answering the question, not by a mechanism.** Ordering is information about *sequence*, which a function of content alone cannot carry, so no test recovers it and no implementation choice reaches it. **Q6 was therefore re-presented and re-answered as D′ on 2026-08-25**, dropping "monotonic" — the owner's explicit decision, not an assumed amendment, with the original Q6=D answer preserved verbatim beside it. R-12 is fully compliant with Q6=D′. **What was given up, and it is a capability rather than an unmet obligation:** release labels can no longer be ordered, so a reviewer comparing two labels at a gate must read sequence from the run record or the experiment registry instead. Nothing else in this design depended on label ordering. **FU-2 is moot** — it existed only to locate the ledger Q6=D required.
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
| Iteration 1 of the fresh budget | *pending* | This file is unchanged in substance since iteration 2 cleared its acceptance lines |

**What iteration 2 explicitly cleared here.** The per-rule acceptance citations, the
two-tier posture, R-14's credential-boundary statement, and the pending-amendment
discipline in R-06 and R-12 — all checked against source and found correct.

---

## Finalized 2026-08-24 — the three amendments are settled

Recorded under `governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md`, after
an independent challenge of each amendment against the approved artifacts.

- **Amendment A — DECLINED.** No project rule requires universal §19 coverage, and the approved position dispositions uncovered requirements as *"Open by design"*. **REQ-ENG-7 and REQ-ENG-10 are untested by design, permanently rather than pending.** No count moved: untested stays 36, this unit's stays 2 of 16, its acceptance rows stay 7, TE §19 stays at 36 rows.
- **Amendment B — APPROVED.** `DeterminismRecord` carries **nine** fields. R-05's prohibition on stating that determinism was measured is **discharged** and replaced by a narrower rule: a measured claim requires `probe_scope` recorded and `measurement_status` = `complete`. **R-06 is unchanged** — an empty `nondeterministic_ops` is never proof of determinism.
- **Amendment C — DECLINED AS DRAFTED 2026-08-25**, reversing its 2026-08-24 approval. No release ledger; `ReleaseLedgerEntry` withdrawn; `dataset_version` derived from `content_hash`, encoding unspecified here. **R-11 is unchanged** — the content hash remains authoritative. **R-12 is amended, not deleted**, and records the two Q6=D obligations left without a mechanism. *(Superseded status, preserved: "**Amendment C — APPROVED**, on the authority of **Q6=D** and **FU-2=D** rather than as an engineering preference. A draft of the change record proposed rejecting it and deriving the label from the content hash; that is Q6 option C, which the owner had read and declined, and it cannot yield the *monotonic* label Q6=D requires. The rejection was withdrawn.")*

  **The withdrawn rejection is now the ruling.** What the superseded text describes as a proposal the owner had already declined — deriving the label from the content hash, Q6 option C — is what the 2026-08-25 ruling mandates. That ruling was given after this exact reasoning, and the owner's own Q6=D and FU-2=D answers, were put to them in full. It is a deliberate override with its consequences stated, and both the monotonicity gap and the upstream contradiction are carried to the stage gate rather than closed here.

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
>   degenerate encoding. **R-11 is unchanged** — the content hash remains authoritative.
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
