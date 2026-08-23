# Business Rules — `foundation`

**Unit** `foundation` (Bolt 1) · **Kind** `library` · **Depends on** — (dependency root)

> **Re-established three times on 2026-08-23, after three stage-wide redo jumps** — aimed
> respectively at a correction in `acquisition`, corrections in `external-products`, and a
> misread depth policy in `component-methods.md`. **No rule of this unit changed on any of
> the three occasions.**

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
- `functional-design-questions.md` — Q1–Q8, FU-1–FU-3, the TA-03 verification, the three pending amendments.
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

> ## ⚠ THIS RULE IS NOT FULLY ENFORCEABLE UNDER THE APPROVED CONTRACT
>
> `probe_scope`, `measurement_status` and `declared_vs_observed_mismatches` **do
> not exist** in `DeterminismRecord` as approved at stage 2.6 — the contract carries
> **six** fields, derived:
> `awk '/class DeterminismRecord/,/^$/' component-methods.md | grep -cE "^ +[a-z_]+: "` → `6`.
>
> **Amendment B is PENDING and NOT approved.** Until it is approved, the record can
> carry the probe *result* with no recorded *scope* and no measurement *status* —
> exactly the ambiguity Q3 = C was chosen to eliminate.
>
> **Therefore, binding now and not deferred:** no artifact, manifest, registry row
> or report produced by this unit may state or imply that determinism has been
> measured for any operation class, while the fields that would record the scope and
> status of that measurement do not exist. Silence is the correct output, not an
> empty list presented as a clean result.

**Negative control.** Declare an operation as expected-nondeterministic in
configuration that the probe does not observe, and the inverse; both must surface
as mismatches rather than being silently reconciled.

**Acceptance.** **WS-17, TA-13** — **for the probe result only** (*superseded: `TA-13, TA-26`*). No row accepts the
scope or status fields, because they are not yet in the contract.

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

## R-12 — Labels are allocated from a durable ledger and never reused

**Rule (Q6 = D, FU-2 = D).** Human-readable labels are allocated from a
**durable, append-only release history**, not solely by scanning existing
directories. **A previously assigned label is never reused.**

**Constraint.** The ledger is **separate from `experiment_registry.jsonl`**.

**Why not a derived index.** Q6 ruled out directory scanning by name. A derived
index has the same defect: delete a release directory and the rebuilt index forgets
the label, so the next allocation reuses it.

**Why not folded into the registry.** Q4's transition graph would have to filter by
row kind before applying its rules, and a rule whose readers must filter first is a
rule that quietly stops applying to the rows it was written for.

**Negative control.** Delete a release directory and attempt a fresh allocation;
the previously used label must still be refused.

> **Amendment C is PENDING and NOT approved.** The ledger is absent from
> `unit-of-work.md` § 1 `Owns` and from `services.md` § Run record and registry
> ("Two artifacts, one authoritative"). Both approved artifacts are unedited. **No
> TE §12 amendment is needed** — `artifacts/registry/` is already enumerated and the
> tree carries zero file-level entries inside `artifacts/`.

**Acceptance.** TA-15 for the release; **no row accepts the ledger itself** until
Amendment C is approved.

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
| Freeze-gate tagging; D-number on every governed change | **REQ-ENG-7** | ⚠ **No §16/§19 row.** Amendment A pending |
| Per-run environment lock, eight fields populated | **REQ-ENG-10** | ⚠ **No §16/§19 row.** TA-03 verified against all seven §13.1 bullets and covers **none fully**; two partially, both install-time rather than per-run. `requirements.md` records the same conclusion. Amendment A pending |
| Probe scope, measurement status, declared-vs-observed mismatches | Q3 = C / NFR-DET-01 | ⚠ **Fields not in the approved contract.** Amendment B pending |
| Release-label ledger integrity | Q6 / FU-2 | ⚠ **Artifact not in any approved `Owns` list.** Amendment C pending |

**Test specifications for REQ-ENG-7 and REQ-ENG-10**, labelled exactly as Q7 = X
directs:

> **Test specification only — not an approved acceptance row and not evidence of a
> passing result.**

- **REQ-ENG-7.** Reject a change to a governed scientific constant or governed
  configuration file when the required decision identifier is **missing or
  invalid**; verify the applicable freeze-gate tagging requirements.
- **REQ-ENG-10.** Derive the required environment-lock fields **directly from TE
  §13.1** and fail when any required item is **missing, malformed, or not captured**
  for the applicable run. The eight fields and their seven-bullet provenance are
  enumerated in `domain-entities.md` § 5.

Per Q7, design and implementation planning proceed while Amendment A is pending.
**Formal acceptance coverage and gate satisfaction are not claimed** until the
amendment is approved and the tests have executed successfully.

## Assumptions & Open Questions

- **[assumption]** The `RequiredFieldsMap` and `CredentialNameMap` are declarative structures **inside `src/data/config.py`**, not governed config files. They name field and variable *identities*, never values, so they carry no scientific constant and TE §12's "exactly four" is untouched. FU-3's stronger form — a seventh module — has no legal home, since TE §12 fixes six `src/` packages.
- **[assumption]** `foundation` hosting `CredentialNameMap` without consuming it is within the boundary. Stated explicitly in R-14 because, unstated, it reads as a boundary violation.
- **Open — Amendments A, B and C.** All three **PENDING and NOT approved.** Enumerated at this stage's approval gate.
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
