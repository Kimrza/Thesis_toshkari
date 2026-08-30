# Business Rules — `acquisition`

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

**Unit** `acquisition` (Bolt 3) · **Kind** `library` · **Depends on** `foundation`,
`governance-guards`

> **Re-established a sixth time 2026-08-24**, on a **new stage attempt** — Inception closed
> and Construction opened at 2026-08-24T11:46:26Z, resetting the receipt floor for every
> unit. **No rule of this unit changed.** Both `foundation` passes of that day touch nothing
> this unit reads (`DeterminismRecord` is not consumed here, no `release.py` signature was
> amended, the amended `services.md` and `unit-of-work.md` sections are not the ones read
> here, and Amendment A was declined so **no count moved**), and its `governance-guards`
> upstream **R-25**–**R-28** re-confirmed with no rule changed. **The READY verdict in
> § Review belongs to the previous attempt.**

> **Re-established a fifth time 2026-08-23**, after a redo aimed at a sibling unit's stale
> cross-references. **No rule of this unit changed.**

> **Re-established 2026-08-23 after a redo jump taken to correct this unit.** R-40's TA-08
> acceptance line was corrected under the cleared receipt at the project decision owner's
> explicit direction, with both superseded readings recorded in place; the summary was
> re-confirmed; a fresh adversarial pass reviews the corrected text. **No rule's content
> changed** beyond that acceptance line.
>
> **Re-established a second time 2026-08-23** after a further stage-wide redo aimed at
> `external-products`. **No rule changed then**; the correction applied was to this unit's
> **question file**, which had still carried the false *"largest untested share in the plan"*
> superlative because its receipt was locked.
>
> **Re-established a third time 2026-08-23** after a redo aimed at a misread depth policy in
> `component-methods.md`. **No rule changed**; that re-reading **confirms** this unit's three
> owed amendments as genuine cross-package boundary changes. **A fourth** followed a sweep of
> two sibling question files; **no rule changed then either.**

The prohibitions this unit enforces, each with what it rejects, what it raises, and the
negative control that proves the rejection happens.

**This project's affirmed methodology is a negative control paired with every hard
rule** — a test that proves the violation is *caught*, not only that the happy path
works. Every rule below carries its negative control, and where no acceptance row exists
to accept that control, it says so.

**Rule IDs continue the single sequence.** `foundation` ran R-01…R-17 and
`governance-guards` R-18…R-29, so this unit opens at **R-30**. This is the numbering
assumption stated in `functional-design-questions.md`; if per-unit numbering was
intended, say so at the gate and the artifacts restart at R-01.

## Sources

- `../../../inception/requirements-analysis/requirements.md` — REQ-ENG-13; FR-P1-00-1, -2; FR-P1-01-1…-9, -11; REQ-NFR-A1, REQ-NFR-A2; FR-P1-04-11.
- `../../../inception/units-generation/unit-of-work.md` § 3 — the `Owns` list, the boundary, and **BLK-07**'s register entry.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2 plus § Per-unit coverage summary; both derivation paths agree.
- `../../../inception/application-design/component-methods.md` — `src/data/locked_test.py`, `src/data/release.py`, the §10 credential rule.
- `../../../inception/application-design/component-dependency.md` § Shared resources.
- `../../../inception/application-design/services.md` § The nine stage scripts, § Stage entry contract, § Execution platforms.
- `../governance-guards/functional-design/business-rules.md` — **R-25**, **R-26**, **R-27**, **R-28**. This unit is the first consumer of all four.
- `../foundation/functional-design/business-rules.md` — R-01's `IntegrityError` base and the two-tier posture.
- `evidence/DECISIONS.md` — D-5, D-6, D-9, D-10.1/.2/.3, D-15, D-18, D-21, D-22, D-23, **D-25, D-26** *(added 2026-08-25, finding F2)*, D-3/D-144, and **D-143** *(a **Vision-register** number — the ICTP rejection; `evidence/DECISIONS.md` runs D-1…D-27 and cites it inside D-3. An iteration-2 note here briefly denied it existed; corrected on terminal finding N1)*.
- `functional-design-questions.md` (**Q1 through Q9**), `domain-entities.md`, `business-logic-model.md`.

---

## The two tiers, inherited

`foundation` R-01 fixes the hierarchy and `team.md` § Code Style fixes the posture.
**Integrity violations** terminate the run non-zero with a message naming the resource
and the violated expectation, raised as an `IntegrityError` subclass. **Completeness
shortfalls** are non-fatal but must be recorded as **machine-readable fields** in the
output manifest — never console text — with the artifact marked derived and/or partial.

**This unit is the first with rules in both tiers**, and the split is load-bearing here:
provider version drift and retrieval shortfalls are normal events that must not halt
acquisition, while an unlogged December access or a leaked credential must.

**Base class of the exceptions this unit raises** *(stated 2026-08-25, discharging the cross-unit
obligation `foundation`'s R-01 records)*: **`AcquisitionError` and `CredentialEgressError` derive
from `IntegrityError`, imported from `src/data/config.py`**, under R-01's *"any future
integrity-related exception"* clause — so the stage-entry contract's `except IntegrityError`
catches each and writes the `aborted` registry row. Without it, a credential-egress violation
would exit unrecorded, in the unit that owns the redaction boundary. **Declaration site** *(finding
F6)*: this unit owns no `src/` module — its deliverables are scripts `00`/`01` and data artifacts —
the declaration site is **an OPEN item for the owner** *(re-scoped 2026-08-25 on terminal finding
N4: the iteration-2 text placed both subclasses "in `src/data/config.py` beside the base" — but
that module is `foundation`'s Bolt-1 deliverable, and its R-01 enumerates its contents as the base
plus the six subclasses **that unit** raises, with other units *importing* the base. Directing 3.5
to edit a sibling's deliverable with no change record answers the counting question and not the
ownership one.)* **The two stated options:** (a) `foundation` accepts the two additional
declarations into `config.py` via a recorded cross-unit agreement, or (b) the owner approves
`src/data/exceptions.py` (the §12 amendment already OPEN at `foundation`), which dissolves the
ownership question for every unit at once. Until ruled, 3.5 must stop and report (TE §18.3);
what IS settled is the base class and the import direction.

---

## R-30 — Retrieval applies no scientific transformation

**Rule (FR-P1-01-1).** `00_acquire_prepared_vtec.py` retrieves the D-144-approved
Madrigal MAPGPS `gps` binned-VTEC product with the frozen experiment, kindat and
parameter set resolved from `configs/data.yaml`, and stores what the provider returned.

**Why terminal rather than recorded.** A transformation applied at retrieval is
**unrecoverable**: the provider's bytes are gone and nothing downstream can determine
what was changed. This is an integrity violation.

**Constraint — the frozen set is read from config, never chosen here.** D-144 fixes it;
`project.md` § Forbidden bars hiding a scientific constant in source or a notebook.

**Negative control.** Introduce a unit conversion, a rounding, or a rescale between
retrieval and write → a diff of retrieved against stored values fails.

**Acceptance.** TA-32 (**owned by this unit**).

> **Two of D-144's four attached freezes remain open** (`requirements.md` § Known
> defects row 5). This design builds to D-144 as approved and resolves neither.

## R-31 — Membership derives from record timestamps, never from a name

**Rule (FR-P1-01-5, REQ-NFR-A2).** Acquisition membership, and every per-month
statistic, derives from **record timestamps** — never from an acquisition directory name
or a filename. Every per-month statistic **excludes out-of-month and out-of-year
records**.

**Why absolute.** `project.md` § Forbidden states it, and it exists because of a
**realized defect**: a year-blind predicate filed locked-test-month records under
`audit_evidence_2022-01/`, where no name-based check could see them.

**Negative control — and it already exists and is green.**
`tests/test_acquisition_window.py` passes, **including the case that produced the
original defect**. It is one of only three test modules in the workspace.

**Acceptance.** ⚠ **No §16/§19 row** for either requirement — see § The seven. Both are
**Class 1: tested without a row.**

## R-32 — Every restricted-root access is routed through a named accessor

**Rule (Q1 = D, BLK-07's mechanism limb).** `acquisition` names an **artifact**, never a
path. `governance-guards`' `locked_test.py` exposes named accessors —
`open_d9_input(record)` and a restricted writer — which own the join. **`acquisition`
holds no fragment of the restricted root.**

**Constraint — each accessor COMPOSES `open_restricted` and none reimplements it.** A
thin named wrapper resolves the artifact name to a path under `RESTRICTED_ROOT` and
**delegates**; the append, flush, durability confirmation and raise stay in the one
approved function. This is what makes BLK-07's required resolution — routing *"through
`governance-guards.open_restricted`"*, by name — true rather than merely resembled, and
it keeps **"one path in" a claim about code paths**: three wrappers each with their own
write-flush-return would be three paths reading as one.

> ⚠ **`open_d9_input` IS NOT IN THE APPROVED CONTRACT.** `component-methods.md`'s
> `src/data/locked_test.py` block defines only `RESTRICTED_ROOT`, `AccessRecord`,
> `open_restricted` and `assert_no_december_outside_restricted`. The accessors are an
> **amendment owed**, alongside R-33's enum extension and write function and R-35's
> `identity_fields` parameter — three, not two. **Until that change record clears,
> BLK-07's routing contract is PROPOSED, not approved**, and the exit condition is not
> discharged by this artifact alone. **Corrected 2026-08-23 after an adversarial pass**,
> which found the accessors flagged nowhere while their two siblings in the same file
> were.

**Why named rather than a constructed path.** `governance-guards` **R-28** asserts by
static check that no module outside `locked_test.py` contains the restricted-root
literal. A named accessor satisfies that **by construction** — there is no string here
for the check to find — rather than by care.

**Constraint — the notebook is covered, and this is not optional.** D-144 approved
`notebooks/00_acquire_phase1_vtec.ipynb` as **self-contained, importing nothing from
`src/`**, so it cannot import `locked_test.py`. Its copy of the access step is covered
by the **declared equivalence scope** (R-38), riding REQ-ENG-13's already-mandated test.
Without this limb the one file exempt from the import rules — and the file that actually
performs acquisition — would have **no sanctioned route** and would duplicate the path
or read unlogged: the exact breach BLK-07 exists to prevent, arriving through the one
exempt caller.

**Negative controls.** Place any restricted-root fragment in an `acquisition` module →
R-28's static check fails. Patch the access-record writer to fail → the read never
begins (R-25's abort limb, exercised through this unit's call site). Remove the access
step from the notebook → the equivalence test fails.

> ## ⚠ THE MECHANISM LIMB ONLY — BLK-07's AUTHORIZATION LIMB IS NOT CLOSED
>
> BLK-07's `Approval authority` row assigns **the contract** to `functional-design`
> (3.1) and assigns nothing else. **Which units may reach the locked month, and when, is
> the project decision owner's decision.** Nothing in this unit's artifacts grants,
> implies or substitutes for it. `governance-guards` R-28 states the same split from the
> other side: the static check enforces *how many* paths exist, never *who* may use one.
>
> **No acquisition run may touch calendar 2022-12 while BLK-07 stands.**

**Acceptance.** Contributes to TA-18 (owned by `features-and-splits`) through R-25's
contract; BLK-07's discharge itself is a gate item, not a test row.

## R-33 — A restricted WRITE logs before it writes, and has its own contract

**Rule (Q2 = C).** A write under the restricted root uses a **separate entry point**
with **log-before-WRITE** ordering. A log-write or durability failure **prevents the
write** — before any byte is written.

**Why not borrow the read contract.** `open_restricted`'s approved wording is built
around *"before the read"*, and the two failures are not equivalent: **a partially
written December artifact with no access row** creates December bytes nobody recorded
creating, which is worse than a blocked read and cannot be undone.

**Constraint — `AccessRecord` needs values it does not have.** The approved `purpose`
enum is `"coverage_audit" | "regime_audit" | "locked_evaluation"`; `authorization` is
typed as *"the G-05 signature reference, or the audit authority"*. **None fits an
acquisition read, and none fits a write at all.** The enum gains `acquisition_read` and
`acquisition_write`; `authorization` widens to name a D-number.

**Why a knowingly wrong value was rejected.** Reusing `"coverage_audit"` would write a
governance-log row describing an audit that never happened. The access log's entire
value is that a G-05 reviewer can read its rows as meaning what they say.

**Negative controls.** Patch the access-record writer to fail → **no byte is written**.
Assert the row is durable on disk before the first write. Attempt a restricted write
through the read accessor → refused.

> **An amendment owed to an approved stage-2.6 contract, stated not applied.**
> `component-methods.md`'s `src/data/locked_test.py` block is approved; this stage
> records the requirement and edits neither it nor the file. A change record is the
> route.
>
> **Raised for `governance-guards`, not built here:** an enum-membership test pinning
> the declared `purpose` values exactly, so a future value cannot be added silently.
> That enum is a sibling unit's; pinning it from here inverts ownership.

**Acceptance.** ⚠ No row of its own. Contributes to TA-18.

## R-34 — A version-suffix mismatch is recorded at retrieval and refused at release

**Rule (FR-P1-01-2, Q3 = C).** Three steps, deliberately not uniform:

1. **Non-fatal at retrieval.** Provider reissue is normal in this dataset — `g.002`
   versus `g.003` is already observed. Halting on a normal event is how a guard gets
   worked around.
2. **Recorded as a machine-readable `suffix_mismatch` field** on the manifest — never
   console text. This is the completeness-shortfall tier.
3. **`write_release` refuses** a release carrying an **unresolved** mismatch.

**Why the refusal sits at release.** It puts the stop where the consequence is:
retrieving a reissued file is fine, **releasing it as though it were the recorded one is
not**, and a release is what a later reader cites. This is what makes FR-P1-01-2's
*"surfaced, never silently accepted"* into a behaviour rather than a field nobody is
required to read.

**Constraint — five fields per retrieved file**: provider, permanent citation, **full
provider filename including its version suffix**, retrieval date, SHA-256. **`source_files`
carries all six of TE §13.3's items — provider; permanent citation or request; **location/date**
*(the dropped item, restored in this file 2026-08-25 on terminal finding N3 — the iteration-2 fix
reached `domain-entities.md` only, leaving this file's five-field constraint juxtaposed with an
all-six claim, the exact DATA-09 mechanism)*; filename; retrieval date; SHA-256 — not five** — the
earlier five-item list fixed a
truncated count as the bar (`DATA-09`).

**A per-file D-number was declined**, with a reason: right in principle, but a
twelve-month re-acquisition would generate a decision per file, and a ritual that heavy
gets batched, which defeats it.

**Negative controls.** Inject a suffix mismatch → the manifest field is set and the run
continues. Attempt a release carrying an unresolved mismatch → `ReleaseError`. Omit any
of the five fields → fails.

> **Noted for stage 3.2, not changed here.** FR-P1-04-11 enumerates §13.3's fourteen
> release fields and **`suffix_mismatch` is not among them**, so the release manifest's
> input contract does not currently carry what this refusal reads.

**Acceptance.** TA-15 (owned by `foundation`, this unit supporting).

## R-35 — An absent `madrigalWeb_version` fails exactly as `"unknown"` fails, and agreement is verified

**Rule (FR-P1-01-3).** **Two** checks, because *"a single string test was satisfiable by
omission"*:

1. Every `request_manifest.json` carries a **non-empty** `madrigalWeb_version`, and an
   **absent key fails exactly as `"unknown"` fails.** The pin also appears in the lock
   file.
2. A derived release **verifies** that its identity fields agree across every source
   manifest rather than asserting they do.

**Constraint — check 2 is enforced inside `write_release`, with the field set as a
declared parameter** (Q4 = C). Guarding the artifact where it is created is the only
placement no caller can route around; supplying the field set as a parameter keeps the
domain knowledge with the caller that has it, rather than putting acquisition-specific
knowledge into a shared API every unit depends on. **An empty `identity_fields` is
refused**, so a caller cannot satisfy the check by passing nothing.

**The live failure is in the workspace today.**
`evidence/locked_test_restricted/audit_evidence_2022-FULL/request_manifest.json` has
**no `madrigalWeb_version` key**, because `merge_coverage_year.py` copies eight identity
fields and drops that one. The eight fields *do* agree across the twelve months — but
nothing checked it.

**Negative controls.** Omit the key → fails identically to `"unknown"`. Pass an empty
`identity_fields` → `ReleaseError`. Perturb one identity field in one source manifest →
the agreement check fails.

> ⚠ **Testing against the real FULL manifest is DEFERRED and attached to `RES-04`.** It
> sits under the restricted root, so reading it is a logged December access owing R-32's
> contract. Building it now would need authorization this stage cannot give, or would
> read the root unlogged — the breach BLK-07 exists to prevent. It becomes available
> once R-32's contract exists, and it is `RES-04`'s shape rather than a new obligation.

> **An amendment owed to an approved contract, stated not applied.**
> `src/data/release.py`'s `write_release` signature is stage 2.6's.

**Acceptance.** TA-03, TA-15 (both owned by `foundation`).

## R-36 — Hashing covers provider files, and pre-TC-06 months say what they are

**Rule (FR-P1-01-4, Q5 = C).**

| Scope | Behaviour |
|---|---|
| Newly acquired months | **One manifest entry per provider file plus one per derived artifact**; each month's hash count equals the sum |
| The twelve pre-TC-06 months | **Re-verified under the new suite, not re-acquired**, and each manifest carries **`provenance_class = derived_only`** |
| Any re-verification | Records the **`producing_interpreter`**, and marks an out-of-envelope artifact as such |

**Why the twelve cannot satisfy the arithmetic.** Every existing `sha256_manifest.json`
hashes exactly **four derived files** and never the contents of `raw_isprint_cache/` —
and that cache holds isprint **text extractions**, not provider `.hdf5` bytes. **No
provider byte stream exists anywhere in the workspace**, and three of the twelve months
— 2022-04, 2022-07 and **2022-12, the locked month** — have no `raw_isprint_cache/` at
all. The provider-side term is zero.

**Why `provenance_class` is a field and not a document.** Without it the manifest format
means two different things depending on when a month was acquired, with nothing in the
artifact saying which. With it, G-P1A, a release or a freeze gate can **refuse** a
`derived_only` month where full provenance is required.

**Why `producing_interpreter` is recorded.** `evidence/experiment_registry.md` records
the 2026-08-16 corrected extracts as produced under **Python 3.14, local** — outside the
governed 3.11 pin. Without the field, a passing hash on those files reads as evidence
the envelope held. It did not.

**Negative controls.** A newly acquired month whose hash count omits a provider file →
fails. A pre-TC-06 month with no `provenance_class` → fails. Re-verify an
out-of-envelope artifact → it is marked, not silently passed.

> **The freeze-gate refusal is NOT written here.** `team.md`'s caveat moved when **D-18
> (2026-08-21) re-merged FULL**, discharging the **superseded-hash** limb; the
> **provenance** limb stands and is **FR-P1-01-11's**. A second, coarser rule here would
> be two rules about one fact, and they drift.

> ⚠ **THE RELEASE-SIDE REFUSAL THIS RULE PROMISES HAS NO FIELD TO READ** *(added 2026-08-28,
> `GOV-2026-08-28-FD-01` Recommendation 28, option 1)*. This rule's own justification above
> is that with `provenance_class` *"G-P1A, **a release** or a freeze gate can **refuse** a
> `derived_only` month"* — and the field reaches **no other unit**. ⛔ **THAT CLAUSE IS
> SUPERSEDED — REBASED 2026-08-29. The field reaches TWO units.** *(Corrected on adversarial
> finding F1 of the 2026-08-29 re-confirmation pass, Critical: the rebase was written into
> `business-logic-model.md` § Assumptions on 2026-08-28 and **never swept into this box, this
> file's Open item, or `domain-entities.md`**, so both sibling artifacts went on asserting the
> pre-remediation figures as live fact. This box was additionally **self-contradictory within
> its own paragraph**, stating the field reaches no other unit while naming
> `inventory-and-registry`'s R-50 as reading it.)* **The current figures, and why they are a
> dated observation rather than a live invariant**: derived over the 48 stage artifacts
> immediately before the rebase note was written, and writing such a note itself adds
> occurrences of each token — `provenance_class` **43**, `derived_only` **38**,
> `producing_interpreter` **17**, split `acquisition` **25 / 21 / 11** and
> `inventory-and-registry` **18 / 17 / 6**. `inventory-and-registry` acquired the field under
> `GOV-2026-08-28-FD-01` **Recommendation 29**, which gave that unit a `data07_caveat` sourced
> from it. **The two stable facts to rely on, which no edit to any note can move: the fields
> reach exactly 2 units, and `foundation` carries all three ZERO times.** The second is the
> one this rule's argument actually rests on, and it is **unchanged** — which is why the Open
> item below stays open and nothing here is discharged. The superseded figures are preserved
> in place below because they record what was found at the opening of the remediation.
> Derived 2026-08-28 across
> all **48** artifacts of this stage: `provenance_class` = **9**, `derived_only` = **7**,
> `producing_interpreter` = **3**, every one of them in this unit; **0 in `foundation`**,
> which owns `src/data/release.py`, `write_release` and the §13.3 contract, and whose
> fourteen §13.3 fields do not include it. Since `write_release` raises `ReleaseError` on an
> absent §13.3 field and `source_files` **cannot** be populated with provider identity for
> the twelve months — the provider-side term is zero — 3.5 would face an unstated choice
> between **no writable Phase 1 release** and **a release accepting placeholder provider
> terms**, which would launder provenance `team.md` calls *unverifiable in principle* into an
> immutable release with no marker. **TE §18.3 forbids an agent choosing**, so the seam is
> **recorded as an Open item for stage 3.2 and the amendment routed to G-P1A** rather than
> resolved here; adding a fifteenth field would be a TE amendment plus a `requirements.md`
> change this stage may not make by assertion, and `foundation` declined exactly that kind of
> unilateral change for **D-24's protected set**. **Nothing here asserts the refusal is
> implemented.** `inventory-and-registry`'s R-50 DATA-07 caveat field reads this same
> `provenance_class` and is sequenced behind this seam.

**Acceptance.** TA-04, TA-15 (both owned by `foundation`).

## R-37 — Gaps are NaN at acquisition, and the count is conserved

**Rule (D-5, D-10.2, FR-P1-01-9, Q6 = C).** Gaps are stored as explicit `NaN` at
acquisition; **no interpolation, smoothing or fill occurs at acquisition.** Three limbs,
because one is not enough:

| Limb | Catches | Misses |
|---|---|---|
| Injected-gap round trip | The realistic regression — a `fillna` added for convenience | A fill on a branch the fixture does not exercise |
| Static scan for fill-class calls in this unit's modules | Branches a fixture misses | An alias, or a vectorised expression that fills without naming a fill function |
| **NaN-count conservation** — `gaps_at_retrieval == gaps_in_artifact`, carried on the manifest | **Any** fill, on any branch, named or not | Nothing in this class |

**Why the conservation limb carries the rule.** It is a law rather than a spot check,
and it produces a **machine-readable manifest field** rather than only a passing test.
That matters here specifically: **FR-P1-01-9 has no §16/§19 acceptance row**, so a
manifest field is evidence that survives the absence of a gate, where a test result is
not — nothing is obliged to run it.

**A per-day, per-series breakdown was declined**, with a reason: genuinely useful for
TC-20's measured-gap obligation, but that obligation belongs to FR-P1-01-7's audit
report, which exists and carries exact dates.

**Negative controls.** Inject a gap → it survives as `NaN`. Add a `fillna` on any branch
→ the conservation assertion fails. Add an aliased or vectorised fill → the static scan
misses it and the conservation assertion still fails.

**Acceptance.** ⚠ **No §16/§19 row.** **Class 2** — see § The seven.

## R-38 — The notebook and the script are behaviourally equivalent within a declared scope

**Rule (REQ-ENG-13, Q7 = D).** Both are run against a **recorded-response fixture** —
never the live provider — and the produced manifests and file hashes are asserted
identical. A **declared equivalence scope** names what must match:

| Must match | Need not match |
|---|---|
| `request_manifest.json` contents | Display and progress output |
| `sha256_manifest.json` contents | Cell structure |
| File hashes | Ordering of non-semantic output |
| NaN handling and the R-37 gap accounting | — |
| Refusal paths — missing input, Internet-access failure, G-P1A refusal | — |
| **The restricted-artifact access step (R-32)** | — |

**Why the scope is part of the rule.** Without it, "behaviourally equivalent" is
renegotiated every time the test fails, which is how such a test ends up relaxed until
it proves nothing.

**Why not a textual diff**, which is TA-16's literal evidence wording: two
implementations can be behaviourally identical and textually different — the notebook
has cell structure and display calls the script does not — so a diff either fails
constantly or is relaxed until it proves nothing.

**Why not extract the shared logic to a generated notebook.** It would remove the drift
rather than detect it, which is stronger — but D-144 approved a **self-contained**
notebook, and whether a generated one still qualifies is the owner's reading, not a
design decision.

**Constraint — the notebook's six declarations** (distinct from REQ-ENG-12's four): its
own version, year and stations, source URLs, retrieval timestamp, destination paths,
resulting hashes.

**Constraint — four prohibitions, each with a check that FAILS when the prohibited
operation is introduced**: no TEC/VTEC calculation from observations, no `los` mapping,
no model-feature creation, no training.

**Constraint — "Run all" either succeeds from declared inputs or stops** with a clear
missing-artifact or Internet-access message, rather than proceeding on partial state.

**Negative controls.** Introduce each of the four prohibited operations → each check
fails. Change a manifest field in one of the pair → the equivalence test fails. Remove a
declaration → fails. Remove a declared input → "Run all" stops with the stated message.

**Acceptance.** TA-16 (owned by `regimes-diagnostics-reporting`, this unit supporting).

## R-39 — Credentials cannot leave through this unit's outputs

**Rule (§10, NFR-SEC-01, Q8 = D).** Credentials reach the provider client **directly
from the environment via `foundation`'s resolution** — never through a config file, log,
registry note or notebook. Egress is closed two ways:

1. **One declared redaction serializer.** Every value this unit writes to a manifest,
   log or notebook output passes through it, and it **refuses unredacted
   credential-shaped values.**
2. **Notebook outputs cleared as a precondition of commit.**

**The two realistic carriers, named rather than left abstract**: a **signed request
URL** and an **auth header**. An acquisition client has both in hand naturally, and both
are things a manifest or log would carry without anyone deciding to put them there.

**Why one serializer.** A checkable chokepoint instead of a rule repeated at every write
site — the same one-path shape as `governance-guards` R-28 — and directly testable.
**"Credential-shaped" is heuristic**, stated rather than hidden.

**Why the commit precondition.** A saved notebook **output cell** is a committed
artifact, and it is where §10's *"never in a notebook"* would be breached in practice —
the one egress a serializer inside the process cannot reach.
`notebooks/madrigal_phase1_coverage_audit.ipynb` exists in the workspace today.
`team.md` § Way of Working already commits this project to a pre-commit hook once git
exists, so the mechanism has a home.

**Why not rely on TA-22's scan alone.** It covers tree, history, configs, logs and
artifacts — but it is detection **after** the artifact exists, and it is owned by
`foundation`. Relying on it alone would make this unit depend on a sibling's gate to
catch its own leak.

**Negative controls.** Hand the serializer a token-shaped value → refused. Put a signed
URL into a manifest field → refused. Commit a notebook with populated output cells → the
precondition fails.

**Acceptance.** TA-22 (owned by `foundation`, this unit supporting).

## R-40 — Driver acquisition follows the frozen contract, at one recorded grade

**Rule (FR-P1-01-6, REQ-NFR-A1).** Four series: **Kp/ap3** and **Hp60/ap60** from GFZ,
**hourly Dst** from Kyoto WDC at a **single recorded release grade for all of 2022**,
**observed (not 1-AU-adjusted) F10.7** from Canada's Solar Radio Monitoring Program.
**SSN is absent**, and a `grep` confirms it.

**Constraint — all nine of TE §5.1's inventory fields**, not three: provider, role,
filename or product identifier, coverage, retrieval date, checksum, version or release
status, licence and access notes, **and the configuration that consumes it.** A series
carrying fewer than nine **fails**.

**Constraint — grades are never mixed within a series, and no value is backfilled from a
future final or definitive archive.** NFR-LEAK-01 governs *timing* only: a series can
satisfy its declared lag while being built from reanalysed values — invisible to every
existing check and fatal on discovery.

**Constraint — THE REANALYSED-VALUE CHECK, DEFINED** *(added 2026-08-28,
`GOV-2026-08-28-FD-01` Recommendation 14, adopting its split recommendation: option 1 for
F10.7 and Dst, option 2 for the two GFZ series)*. **As found at the opening of this
remediation** (derived 2026-08-28 over all **48** `functional-design` artifacts of this
stage), the phrase `reanalysed-value check` appeared **3 times, all three in this unit** —
`business-logic-model.md:601`, `business-rules.md:482` and `business-rules.md:610` — **and
the check was defined nowhere**, while `requirements.md` **FR-P1-01-8** carried it as a
criterion with status **`UNTESTED`**. It is defined here as a **declared-status check with a
stated verifiability limit**, the **D-25 pattern** this project already sanctioned in
`CR-2026-08-22-EV-12` for an unobtainable provider field.

> **Coordination with `external-products`, stated so the two do not drift.**
> `external-products` R-63 was amended on the **same day, on the same recommendation**, and
> declares itself *"the **driver-product half** only"*, expressly not restating this unit's.
> The division of labour, recorded here at the point of use because R-36's own reasoning
> warns that *"a second, coarser rule … would be two rules about one fact, and they drift"*:
> **this rule is authoritative for the check's definition** — its inputs, its three
> assertions, its failure condition and its negative controls, which are what FR-P1-01-8's
> closure row reads. **`external-products` R-63 is authoritative for the driver-product
> manifest surface** those fields are recorded on, and for the feature-contract side of the
> contemporaneous-grade question. The two agree on substance as at 2026-08-28 — the same four
> fields, the same per-series limits, the same GFZ cross-assertion, the same
> recorded-absence-plus-unverified-status evidence shape. **Any future change to the check's
> definition is made here and mirrored there**, not the reverse; a divergence between them is
> a defect in this pair, not a matter of interpretation, and is raised at the stage gate. The
> phrase count above therefore describes the **pre-remediation** state and is not a
> present-tense claim.

**Inputs — what each driver manifest records, and the check reads.** These are **not new
fields beyond the nine**: `release_status` and `provider_product_identity` give asserted
meaning to TE §5.1's *"version or release status"* and *"filename or product identifier"*
slots, and `retrieval_date` and `checksum`/`sha256` are §5.1's own. The **nine-field count is
unchanged**; what changes is that four of them are now **read by a defined check** rather
than merely present.

| Field | Content |
|---|---|
| `release_status` | The grade the series is **declared** to be — real-time, provisional, or final/definitive — in the provider's own vocabulary |
| `retrieval_date` | When the bytes were retrieved |
| `provider_product_identity` | The **full** provider filename or product identifier, **including any version suffix**. `g.002` versus `g.003` drift is already observed in this project's data, and `team.md` § Walking Skeleton already binds re-acquisition to record the suffix |
| `sha256` | Digest of the retrieved bytes |

**What the check asserts.** **(a) Internal consistency** — exactly **one** `release_status`
for the whole of calendar 2022, no mixing within a series, and that status **agrees with the
recorded `provider_product_identity`**. **(b) Contract agreement** — the declared status is
the **contemporaneous** grade the feature contract requires at a 2022 forecast origin, not a
later reanalysed grade. **(c) The stated limit** — where the held file carries **no
correction, revision, version or provenance column**, that **absence recorded explicitly,
together with an unverified-status statement**, is the **sanctioned evidence**. Silence is
not evidence; a recorded absence is.

**Failure condition.** A missing or empty `release_status`; more than one status within a
series for 2022; a declared status disagreeing with the recorded
`provider_product_identity`; an identity recorded without its version suffix where the
provider publishes one; or an absent provenance column recorded **without** the accompanying
unverified-status statement. Any of these **fails**, under this project's mandated
integrity-failure posture — an explicit exit naming the file and the violated expectation.

**Per-series verifiability, stated rather than implied — detection is BOUNDED, NOT CLOSED:**

| Series | What the held or obtainable evidence supports | The limit |
|---|---|---|
| **F10.7** (NRCan) | Declared status only. **D-22** records `fluxtable.txt` as carrying exactly seven columns and **no correction, revision, version or provenance column**; **D-21** records the publication latency as **not derivable** from the held file | **A reanalysed value cannot be detected from these bytes.** The check records a claim about the value; it does not detect one. **D-25** already governs availability as an *explicit project assumption*, not a demonstrated fact |
| **hourly Dst** (Kyoto WDC) | Declared status, inferable **from the filename only** — the held files are `dst_provisional_2022MM.html` | **D-10.1's open item on the 2022 Kyoto grade remains unchecked** (per D-11). Grade *mixing* is detectable; a reanalysed *substitution* is not |
| **Kp/ap3** (GFZ) | **Substantive detection** — specified now, because these bytes have **never been retrieved** | See the re-acquisition constraint below |
| **Hp60/ap60** (GFZ) | **Substantive detection**, same reason | See the re-acquisition constraint below |

**Constraint — the two GFZ series are re-acquired in BOTH grades and asserted against each
other, value by value.** **GFZ Kp/ap3 and Hp60/ap60 have never been retrieved** —
`evidence/audit_ec1_2026-08-15/` holds only `kyoto_dst/` and `nrcan_f107/`. Because the
retrieval has not happened, substantive detection can be designed in at no retrofit cost,
and is required: re-acquisition retrieves the provider's **near-real-time product alongside
the definitive one** for calendar 2022 and asserts the two **against each other, value by
value**; **a mismatch raises** rather than being silently accepted. Both products record
their own `provider_product_identity`, `retrieval_date` and `sha256`. This is the **only**
limb that detects a backfill rather than recording a claim about one — and it costs almost
nothing specified now and everything retrofitted after acquisition.

> ⚠ **WHAT THIS CHECK DOES AND DOES NOT CLOSE.** `project.md` § Forbidden states this rule's
> failure mode exactly: *"a series can satisfy its stated lag while still being built from
> reanalysed indices — **invisible in validation, fatal on discovery**."* For the two GFZ
> series the mechanism above **detects** it. For **F10.7 and Dst it does not**, and on the
> bytes held **no mechanism can** — this rule says so rather than implying otherwise.
> Detection for those two is **bounded, not closed**; the residual is carried as an open
> verification obligation against **G-04**, not presented as discharged. **No scientific
> value is decided here.** Which grade each series' feature contract requires at a 2022
> forecast origin, and whether the recorded F10.7 and Dst statuses are acceptable, are
> **Student + Supervisor** items — and **EC1-R-4's provider-documentation limb is owned
> outside this project**. TE §18.3 bars this stage from filling either.

**Constraint — two citation obligations discharged before G-P1A, not left uncollected**:
the **Kyoto non-commercial-use notice recorded verbatim** (D-6, EC1-R-1) and the **CEDAR
rules-of-the-road and acknowledgment** attached to `madrigalWeb`. **A notice recorded by
reference rather than verbatim fails.**

**Constraint — Dst is diagnostic/hindcast-only**, never a confirmatory ML feature. It is
also the series `governance-guards` **R-26** names in its bounded driver exclusion, so a
December-dated Dst capture is not a December hit.

**Negative controls.** Inject a mixed grade into one series → fails. Omit any of the nine
fields → fails. Record a notice by reference → fails. Introduce SSN → the `grep` check
fails.

**Negative controls for the reanalysed-value check** *(re-worded 2026-08-28, Recommendation
14, so each control asserts only what the mechanism can actually catch)*. A declared
`release_status` **disagreeing with the recorded `provider_product_identity`** → the check
**fails**. A `provider_product_identity` recorded **without its version suffix** where the
provider publishes one → **fails**. **More than one `release_status`** within a series for
2022 → **fails**. A held file with **no provenance column** whose manifest carries **no
explicit unverified-status statement** → **fails**. For the two GFZ series, a
**near-real-time value disagreeing with the definitive value** at any epoch → **raises**.

> **Superseded posing, preserved:** *"Backfill a value from a final archive → the
> reanalysed-value check fails."* That control asserted a detection the mechanism **cannot
> perform** for F10.7 or Dst — on the bytes held there is no provenance column to compare a
> backfilled value against — so it read as designed while being structurally unable to fire.
> It survives, correctly, **only** as the GFZ two-product control above. The honest statement
> is that detection is **bounded, not closed**, for F10.7 and Dst.

**Acceptance.** TA-08 for FR-P1-01-6 — **primary owner `features-and-splits`**, with
`external-products` supporting. **This unit is NOT a supporting unit on TA-08**: story-map
Table 2 lists only `external-products`, and this unit supports TA-15, TA-16, TA-22 and
TA-25. **Corrected twice, 2026-08-23**: the first issue reversed primary and supporting;
the iteration-1 fix corrected the primary and introduced the opposite error by adding this
unit to the supporting list, which the iteration-2 pass caught. Both superseded readings
are recorded here rather than replaced silently. ⚠ **REQ-NFR-A1 has no row** —
**Class 2**.

## R-41 — The F10.7 window is measured before anything is reconstructed

**Rule (FR-P1-01-7, TC-20).** The audit found **no missing calendar day**: at least one
observation on **365 of 365**. It asserts neither measured nor reconstructed status for
within-day coverage — the held archive carries no qualifier, flag or provenance column,
so that is **not determinable from it**.

**Constraint — the three selection choices are frozen and transcribed into
`features.yaml` when Bolt 1 creates it, each citing its D-number:**

| Choice | Value | Decision |
|---|---|---|
| Daily value | The **daily median** of that UT day's observed readings | **D-21** |
| Duplicate UT records | The **mean** of the duplicated measurements, with duplicate logging and a QC flag; **provider-defined correction semantics take precedence when documented** | **D-22** |
| High-spread days | The four days whose within-day spread exceeds 20% of the median — **2022-01-18, 2022-03-31, 2022-08-28, 2022-08-29** — are flagged and retained with the approved daily median as representative | **D-23** |

**Constraint — availability, binding (D-21 as SUPPLEMENTED BY D-25, with D-26's provenance flag).**
*(Corrected 2026-08-25 on adversarial finding F2 of the post-reset pass: this rule cited D-21 alone,
and D-25 — decided 2026-08-22, "supplements D-21" — froze the STRICTER convention that a daily
median becomes available no earlier than **00:00 UTC on day D+1**, an explicit project assumption
rather than a demonstrated publication latency; D-21's own wording would permit 22–23 UT on day D.
D-26 separately records the March–April provenance as UNRESOLVED with a thesis reporting
obligation. Both were absent from all three artifacts and both § Sources lists; inherited from
requirements.md FR-P1-01-7, which carries the same gap — reported upstream, not edited there.)*
The approved daily F10.7 value `median(D)` becomes available **no earlier than 00:00 UTC on day
D+1** — D-25's conservative convention, an explicit project assumption rather than a demonstrated
publication latency. **No same-day availability, ever**, even when every observation of day D has
completed intra-day. *(Operative sentence corrected 2026-08-25 on terminal finding N2.
**Superseded wording, preserved:** "must not become available to a forecast before all
observations required to compute it were actually available" — D-21's observation-completion
rule, which permits 22–23 UT on day D and which D-25 froze narrower on 2026-08-22.)*

**Constraint — no imputation, substitution or reconstruction** occurs until the measured
gap is recorded and governed.

**Negative controls.** A run whose `features.yaml` leaves any of the three unset →
**fails the zero-TBD preflight** rather than resolving it by convention. Introduce an
imputed value before the gap is recorded → fails.

**Acceptance.** ⚠ **No row.** **Class 2.** The availability constraint's enforcement is
verified through the FR-P1-04-2 availability matrix (WS-11, TA-08) rather than by a row
of its own.

## R-42 — A derived release's provenance is current, or re-pointed by a D-number

**Rule (FR-P1-01-11).** A derived multi-month release either **re-merges from the current
months** or **carries a D-number re-pointing its provenance**. A release whose digests
predate a regeneration of any source month **fails rather than being relied on**.

**Why it is a requirement rather than a paragraph.** `PROVENANCE_NOTICE.md` stated it as
prose — *"Do not rely on this artifact at a freeze gate while this notice stands… Either
re-merge from the corrected months, or record an explicit decision re-pointing FULL's
provenance"* — with no ID, criterion or test link, so nothing checked it.

**Status today, both limbs stated separately because they are different facts.**
**Satisfied by D-18**, whose re-merge is the first branch: FULL's `merged_at_utc` moved
from 2026-08-13T06:27:03Z to 2026-08-21T09:25:59Z and its `source_runs` digests onto
current per-month hashes, with the prior artifact preserved at
`superseded_2026-08-21_audit_evidence_2022-FULL/` rather than overwritten; all twelve
per-month manifests verified first. **The provenance limb is untouched by that re-merge
and still stands**: no provider byte stream exists, so FULL's provenance remains
**unverifiable in principle** — not merely unverified — until the re-acquisition.

**Negative control.** Regenerate one source month and leave the release untouched → the
digest-equality assertion fails, and no D-number covers it.

**Acceptance.** ⚠ **No row.** **Class 2.**

## R-43 — ICTP is rejected, recorded immutably, and unreachable from the target path

**Rule (FR-P1-00-1, FR-P1-00-2).** The ICTP source-failure evidence is **immutable and
machine-readable**: `source_status = REJECTED_COVERAGE`, coverage recorded as **ARUC
27/365, BSHM 35/365, NICO 0/365**, decision stored as **D-143**. **No ICTP artifact
enters target construction or training.**

**Constraint — reachability, not filenames.** FR-P1-00-2's check is an
import/data-lineage check showing no ICTP artifact **reachable** from the target or
feature path, for the same reason R-31 gives: a name-based check cannot see what a
year-blind predicate misfiled.

**Negative controls.** Mutate the evidence set → hash verification fails. Make an ICTP
artifact reachable from the target path → the lineage check fails. Replace the
machine-readable status with prose → fails.

**Acceptance.** TA-31 and TA-25 (`inventory-and-registry` primary on TA-25, this unit
supporting).

---

## The seven requirements with no acceptance row — two classes, stated not buried

**7 of this unit's 15** have no §16/§19 acceptance row, derived from story-map
§ Per-unit coverage summary. **Corrected 2026-08-23 after an adversarial pass:** the
first issue called this *"the largest untested share of any unit in the plan"*, which
that same table contradicts — **`acquisition` 7/15, `models-and-baselines` 7/9,
`regimes-diagnostics-reporting` 7/11**, a three-way tie on the raw count of 7 and, by
share, `acquisition` the **smallest** of the three. The two classes below are named
wherever the count **7** appears, so a later sweep keyed to the numeral does not miss the
qualitative claim.

**Class 1 — tested without a row (2).** Both discharge onto
`tests/test_acquisition_window.py`, which **exists and is green**. They lack a row, not a
test.

| Requirement | Rule | Evidence that would close it |
|---|---|---|
| FR-P1-01-5 | R-31 | An approved §19 row asserting membership derives from record timestamps, with the existing green test cited as its result |
| REQ-NFR-A2 | R-31 | The same row, or a sibling scoped to fold and partition membership |

**Class 2 — untested and unrowed (5).** Each states **what evidence would close it**. **No
§19 criterion is drafted**: a drafted criterion in a functional-design artifact is
indistinguishable, months later, from an approved one, and §19 rows are owned by stage
3.2 and change control.

| Requirement | Rule | Evidence that would close it |
|---|---|---|
| FR-P1-01-7 | R-41 | The audit report with exact dates (exists), **plus** a passing check that `features.yaml` carries D-21, D-22 and D-23's three choices and that the zero-TBD preflight fails when any is unset |
| FR-P1-01-8 | R-40 | A passing reanalysed-value check per driver — **defined in R-40 as at 2026-08-28** (declared-status check: inputs, failure condition, per-series verifiability limit, and the GFZ two-product value-by-value assertion) — plus each driver manifest carrying a populated `release_status`. **The check's detection is bounded, not closed, for F10.7 and Dst**, and that residual is an open verification obligation against **G-04**, not something this evidence discharges |
| FR-P1-01-9 | R-37 | A passing injected-gap round trip **and** a NaN-count conservation assertion over a fixture month |
| FR-P1-01-11 | R-42 | A passing digest-equality assertion, **or** a D-number re-pointing provenance and cited at G-P1A — D-18 satisfies the first branch today |
| REQ-NFR-A1 | R-40 | A passing mixed-grade injection test per series, and a single recorded grade for calendar 2022 |

> **No artifact, manifest or report may state or imply that any of the seven is covered,
> satisfied or verified.** For Class 1 the test passing is not a row; for Class 2
> designing the mechanism is not a test, and implementing it is not a test.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence, so this unit opens at **R-30**. If per-unit numbering was intended, say so at the gate.
- **[assumption]** `tests/test_acquisition_window.py` is this unit's, per `unit-of-work.md` § 3 `Owns`. It exists and is green; R-31 designs around it rather than proposing to rewrite it.
- **[assumption]** The re-acquisition is future work outside this stage's scope; its December limb is barred while BLK-07 stands.
- **[assumption]** `scripts/audit_ec1_drivers.py` migrates onto the §12 structure here; **`audit_ec1_drivers.py:184` returning `0` regardless of missing months** is a known gap against the two-tier posture, fixed at migration. This stage designs the target shape, not the migration commit.
- **Open — BLK-07 is an EXIT condition on this stage.** R-32 authors the **mechanism** limb. The **authorization** limb is the project decision owner's, and no rule here grants, implies or substitutes for it.
- **Open — THREE amendments owed to approved stage-2.6 contracts, stated not applied.** (1) **R-32's named accessors** — `open_d9_input` and the restricted writer — are absent from `component-methods.md`'s approved `src/data/locked_test.py` block, and they are BLK-07's central mechanism, so **BLK-07's routing contract is proposed rather than approved until this clears change control**. (2) R-33 extends `AccessRecord.purpose` and adds a restricted-write function to the same file. (3) R-35 adds an `identity_fields` parameter to `src/data/release.py`'s `write_release`. All three need change records. **Corrected 2026-08-23 after an adversarial pass** found the first omitted.
- **Open — noted for stage 3.2:** `suffix_mismatch` is not among FR-P1-04-11's fourteen release fields, which R-34's refusal reads.
- **Open — noted for stage 3.2:** `provenance_class` is not among FR-P1-04-11's fourteen release fields, which **R-36's release-side refusal reads** *(added 2026-08-28, `GOV-2026-08-28-FD-01` Recommendation 28, option 1 — the same form as the `suffix_mismatch` bullet above)*. R-36 states the field's purpose as letting *"G-P1A, **a release** or a freeze gate … **refuse** a `derived_only` month"*, and establishes that for the twelve pre-TC-06 months **no provider byte stream exists anywhere in the workspace** — the provider-side term is **zero** — with **2022-04, 2022-07 and 2022-12** holding no `raw_isprint_cache/` at all. ⛔ **REBASED 2026-08-29 — the "all in this unit" clause is superseded; the field reaches TWO units.** *(Corrected on adversarial finding F1, Critical — the 2026-08-28 rebase reached only `business-logic-model.md` § Assumptions and was never swept here.)* **Current figures, a dated observation and never a live invariant** (derived over the 48 stage artifacts immediately before the rebase note was written; writing such a note adds occurrences of each token): `provenance_class` **43**, `derived_only` **38**, `producing_interpreter` **17**, split `acquisition` **25 / 21 / 11** and `inventory-and-registry` **18 / 17 / 6** — that unit acquired the field under `GOV-2026-08-28-FD-01` **Recommendation 29**, which gave it a `data07_caveat` sourced from it. **The two stable facts: the fields reach exactly 2 units, and `foundation` carries all three ZERO times.** The second is what this item's argument rests on and is **unchanged**, which is why the item stays Open. Superseded figures preserved: Derived 2026-08-28 across all **48** artifacts of this stage: `provenance_class` = **9**, `derived_only` = **7**, `producing_interpreter` = **3**, **all in this unit; 0 in every other unit, `foundation` included** — and `foundation` owns `src/data/release.py`, `write_release` and the §13.3 contract, whose fourteen fields its `domain-entities.md` enumerates without this one. **`write_release` therefore faces an unstated choice** that §18.3 forbids an agent to make: either no Phase 1 release is writable at all, or `source_files` is accepted with empty or placeholder provider terms — laundering provenance `team.md` calls **unverifiable in principle** into an immutable release with no marker on it. **Neither branch is chosen here, and the field is deliberately NOT added to the release manifest by this stage**: §13.3's field set and FR-P1-04-11's fourteen are **approved artifacts**, so adding a fifteenth is a TE amendment plus a `requirements.md` change this stage may not make by assertion — `foundation` declined an analogous unilateral change for **D-24's protected set**, and doing it here would apply a looser standard than the same stage applied to itself. **The amendment is routed to G-P1A / stage 3.2**; `code-generation` must **stop and report** rather than pick a branch. **`foundation`'s half** — one sentence in its release rules naming the unspecified `derived_only` case — is that unit's to write and is **raised at this stage's gate, not edited into its files**.
- **Open — raised for `governance-guards`:** an enum-membership test pinning `AccessRecord.purpose` exactly. Not built here, because that enum is a sibling unit's.
- **Open — `RES-04`.** Not started and deliberately not attempted; the three existing test modules all reach the restricted root by recursive traversal, and running them before the chokepoint exists would manufacture the breach. R-35's real-artifact test is the same shape and defers to it.
- **Open — `RES-01`**, permitted-read access logging is NOT TESTED, owned by stage 3.2. This unit is a consumer of the untested contract.
- **Open — FULL's provenance limb**, unverifiable in principle. D-18 discharged only the superseded-hash limb. Owned by R-42 / FR-P1-01-11.
- **Open — two of D-144's four attached freezes.**
- **Open — the F10.7 measured gap**, to be recorded and governed before any imputation, substitution or reconstruction.
- **Open — the Kyoto and CEDAR notices**, to be recorded **verbatim**, not by reference, before G-P1A.
- **G-09 is not signed.** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged. No rule here authorises creating `scripts/00_acquire_prepared_vtec.py` or any module.
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

> **Re-saved 2026-08-25 under the eleventh-redo receipt, after the terminal-pass remediation.**
> Three rules changed in this file: **R-41's operative sentence** now states D-25's convention
> (available no earlier than 00:00 UTC on day D+1, never same-day; D-21's observation-completion
> wording preserved as superseded — terminal finding N2); **R-34** now enumerates all six §13.3
> `source_files` items including `location/date` (N3); and the exception **declaration site** is
> re-scoped as an OPEN item with two stated options rather than directing 3.5 to edit
> `foundation`'s module (N4). The Sources list carries the **two-register note** — D-143 is the
> Vision-register ICTP rejection (N1). Figures unchanged: 15 requirements, 7 untested, 1 acceptance
> row. **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved unchanged 2026-08-26 under the third receipt** (twelfth redo, taken for
> `inventory-and-registry`; floor reset mechanical). **No content of this unit changed** since its
> READY. **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved unchanged 2026-08-26 under the fourteenth-redo re-confirmation receipt** (redo taken
> for `external-products`; floor reset mechanical). **No content of this unit changed.**
> **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved 2026-08-28 under the post-redo receipt, remediating `GOV-2026-08-28-FD-01`
> (verdict FAIL) on the project decision owner's ruling — mechanism written, value routed to
> the gate.** Two recommendations reach this unit; a third (**Recommendation 46**) is
> `external-products`' and is deliberately **not** duplicated here — this unit's § Sources
> already carries **D-25, D-26** from its own finding-F2 fix of 2026-08-25.
>
> **In this file, Recommendation 14:** **R-40 gained the definition of the
> `reanalysed-value check`**, which was named three times in this unit and defined nowhere in
> any of this stage's **48** artifacts. It is defined as a **declared-status check with a
> stated verifiability limit** (the **D-25** pattern, sanctioned by `CR-2026-08-22-EV-12`):
> four recorded inputs (`release_status`, `retrieval_date`, `provider_product_identity`
> **including any version suffix**, `sha256`), three assertions (single 2022 status; status
> agrees with recorded product identity; status is the **contemporaneous** grade the feature
> contract requires), an explicit failure condition, and a **per-series verifiability table**.
> The two **unretrieved** GFZ series additionally carry the substantive limb — re-acquisition
> retrieves the **near-real-time product alongside the definitive one** and asserts them
> **value by value**, a mismatch raising. **R-40's negative controls were re-worded** so each
> asserts only what the mechanism can catch; the superseded posing (*"Backfill a value from a
> final archive → the reanalysed-value check fails"*) is **preserved and labelled**, because
> it asserted a detection impossible on the held bytes. **Detection is stated as bounded, not
> closed, for F10.7 and Dst**, with the residual carried against **G-04**. The **FR-P1-01-8
> closure row** now names the definition and the bound.
>
> **In this file, Recommendation 28:** **one Open item added** — `provenance_class` is not
> among FR-P1-04-11's fourteen release fields, which R-36's release-side refusal reads — in
> the **exact form** used one bullet earlier for `suffix_mismatch`, plus a ⚠ box **at R-36
> itself** so the seam is visible at the point of use. **The field was deliberately NOT added
> to the release manifest**: §13.3's set and FR-P1-04-11's fourteen are approved artifacts,
> and `foundation` declined the analogous unilateral change for **D-24's protected set**. The
> amendment is **routed to G-P1A / stage 3.2**; `foundation`'s own half is **gate input**, not
> an edit to a sibling's files.
>
> **Counts derived 2026-08-28, printed before assertion.** Rules **14** (R-30…R-43) —
> unchanged, none added or removed. Requirements without an acceptance row **7** (2 Class 1 +
> 5 Class 2) — unchanged. Negative-control blocks in this file: **14 → 15**. In-unit field
> counts across this stage's 48 artifacts: `provenance_class` **9**, `derived_only` **7**,
> `producing_interpreter` **3**, `reanalysed-value check` **3** — all still confined to this
> unit, which is precisely what Recommendation 28's Open item records. **No scientific value
> was decided**: not a release grade, not a feature-contract grade requirement, not a release
> field. **G-09 remains unsigned**; **BLK-07's authorization limb remains open**; membership
> stays derived from **record timestamps**, never from a directory name (D-2 / ML-07 / TEC-09).

---

> **Re-confirmation receipt, 2026-08-29.** The 2026-08-27T21:49:36Z REDO jump reset every
> unit's receipt floor. This unit's content had already changed after that floor — provenance_class
> figures rebased with basis stated, G-09 signed under D-31 with its §18.3 preconditions
> disclosed unmet — so the owner re-confirmed the unchanged post-rebase content via the
> Consolidated Summary Confirmation at the foot of `functional-design-questions.md`, receipted
> `2026-08-29`. No line above this marker was touched by this pass.
