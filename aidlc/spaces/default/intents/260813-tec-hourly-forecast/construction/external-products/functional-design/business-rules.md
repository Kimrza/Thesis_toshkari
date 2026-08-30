# Business Rules — `external-products`

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

**Unit** `external-products` (Bolt 5) · **Kind** `library` · **Depends on**
`inventory-and-registry`

> **Re-established a sixth time 2026-08-24**, on a **new stage attempt** (Construction opened
> 2026-08-24T11:46:26Z, resetting every unit's receipt floor). **No rule of this unit
> changed.** Both `foundation` passes of that day touch nothing this unit reads, and the
> absence of an `src/external` block in `component-methods.md` was re-verified directly.
> Amendment A was declined, so **no count moved**. **The READY verdict in § Review belongs
> to the previous attempt.**

> **Re-established a fifth time 2026-08-23**, after a redo aimed at a sibling unit's stale
> cross-references. **No rule of this unit changed.**

The prohibitions this unit enforces, each with what it rejects, what it raises, and the
negative control that proves the rejection happens.

**This project's affirmed methodology is a negative control paired with every hard rule** —
a test that proves the violation is *caught*, not only that the happy path works. Every rule
below carries its negative control, and where no acceptance row exists to accept that
control, it says so.

> **Corrected and re-established 2026-08-23**, after two adversarial passes and a redo jump.
> **R-54a is new** — TA-36's primary acceptance test is `features-and-splits`', not this
> unit's — and **R-55's amendment count is now derived** at **five** across three units,
> boundary contracts only, rather than carried from prose. Every superseded reading is
> preserved in place. **No answer to any question changed.**
>
> The count reached five through **two** corrections: from "four across four" with
> `open_d9_input` misattributed, then from "six across three" once `component-methods.md`
> § Depth was read — it specifies **cross-package boundary calls only** and names **this
> stage** as where intra-package shapes are specified.
>
> **A fourth redo** then swept this unit's **question file**, which still asserted the
> superseded total in five live places while these rules already read five. **No rule
> changed.**

**Rule IDs continue the single sequence.** `foundation` ran R-01…R-17, `governance-guards`
R-18…R-29, `acquisition` R-30…R-43 and `inventory-and-registry` R-44…R-53, so this unit
opens at **R-54**. This is the numbering assumption stated in
`functional-design-questions.md`; if per-unit numbering was intended, say so at the gate and
the artifacts restart at R-01.

## Sources

- `../../../inception/requirements-analysis/requirements.md` — REQ-ENG-9; FR-P1-04-3, -4, -9, -15, -17, -18.
- `../../../inception/units-generation/unit-of-work.md` § 6 — the `Owns` list, the module-path allowlist, the implementation notes.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2 plus § Per-unit coverage summary; **the governing source where § 6 disagrees**, see R-54's box.
- `../../../inception/application-design/components.md` § `src/external`.
- `../../../inception/application-design/component-methods.md` — **which carries no `src/external` block**.
- `../../../inception/application-design/services.md` § The nine stage scripts, § Stage entry contract.
- `../inventory-and-registry/functional-design/business-rules.md` — R-44, R-45, R-51.
- `../governance-guards/functional-design/business-rules.md` — R-23, R-24 (the data-flow IRI rule and the subordinate-scan framing this unit's R-56 deliberately departs from), R-26.
- `evidence/DECISIONS.md` — **D-5**, **D-10.1**, **D-10.2**, **D-10.3**, **D-11**, **D-13**, **D-21/22/23**, **D-25, D-26** *(added 2026-08-28, Recommendation 46 — both were already cited operatively in this file, D-25 at R-59 limb 4 and D-25/D-26 at R-57's boundary note, while neither appeared in this register; the same defect `acquisition` fixed on its own finding F2)*.
- Workspace inspection, 2026-08-23: `scripts/audit_ec1_drivers.py` line 184; `evidence/audit_ec1_2026-08-15/kyoto_dst/dst_provisional_202212.html`; the absence of `src/` and `configs/`. **Re-inspected 2026-08-28** (Recommendation 14): `evidence/audit_ec1_2026-08-15/` contains exactly `EC1-AUDIT.md`, `ec1-audit-report.json`, `kyoto_dst/` and `nrcan_f107/` — **no GFZ directory, so Kp/ap3 and Hp60/ap60 have never been retrieved**.
- `functional-design-questions.md` (**Q1 through Q9**), `domain-entities.md`, `business-logic-model.md`.

---

## The two tiers, inherited

`foundation` R-01 fixes the hierarchy and `team.md` § Code Style fixes the posture.
**Integrity violations** terminate the run non-zero, naming the resource and the violated
expectation. **Completeness shortfalls** are non-fatal but recorded as **machine-readable
fields** in the output manifest, never console text.

**This unit's rules sit in both tiers, and R-61 is where the split is load-bearing**: a
month absent from the provider is a fact to record; a hash that does not match invalidates
everything downstream of it.

---

## R-54 — The story map governs this unit's coverage figures

**Rule (Q2 = D).** Where `unit-of-work.md` § 6 and `unit-of-work-story-map.md` disagree
about this unit's untested count or acceptance rows, **the story map governs**, and any
stale statement is **reported at the gate, not edited**.

> **⛔ THE DISAGREEMENT THIS RULE WAS WRITTEN FOR NO LONGER EXISTS** *(marked 2026-08-26 on
> adversarial finding 8, Critical — the 2026-08-26 correction had reached one file's one section
> while this rule still stated the trigger as live)*. **§ 6 was swept**: the current file reads
> **4** untested and `Acceptance rows (2). WS-09, TA-36 (Pending …)`, present since commit
> `45796f5` (2026-08-24). The table and paragraphs below are the **dated record of the conflict
> as it stood when this rule resolved it**, and the rule itself remains standing should the two
> artifacts diverge again. **Nothing is currently reported to the gate under this rule.**

| Claim | `unit-of-work.md` § 6 | Story map — **governing** |
|---|---|---|
| Untested requirements | **5** (bold list includes FR-P1-04-17) | **4** — REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18 |
| Acceptance rows owned | **1** — WS-09 | **WS-09**, plus TA-36 in § Per-unit coverage summary — reconciled differently in § Cross-unit responsibilities (R-54a) |

**Why the story map.** `TA-36` was approved **2026-08-22** under Vision §15.2
(`CR-2026-08-22-LEAKAGE-TA`) as FR-P1-04-17's negative-path row, and the story map records
the resulting sweep — *"Changed 2026-08-22 by the addition of TA-33…TA-36: untested
40 → 36."* § 6 was not swept with it **at the time this was written; it has been since** (see
the ⛔ box above).

**Why reported and not edited.** `CHANGE_RECORD_PROCEDURE.md` reserves approved-stage
artifacts: a sweep reports, absent owner approval for annotate-in-place.

**Constraint — the stale text is named exactly**, because one half of it carries no numeral:
§ 6's five-item bold list, and the line **`Acceptance rows (1). WS-09`**. `project.md` § Way
of Working records that a sweep keyed to a superseded number is structurally blind to a
stale claim of exactly that shape.

**Constraint — TA-36 is cited with its status, always.** **`Pending`: the row exists; it is
not implemented, not executed, not passing.** A row that exists but has never run is the
shape of the defect that let FR-P1-02-8 look covered behind a withdrawn `TA-29` for five
revisions, past four governance boards.

**Negative control.** A statement in any artifact of this unit citing TA-36 without its
status, citing five untested requirements, or claiming this unit **owns** TA-36's primary
test (R-54a), fails review.

**Acceptance.** ⚠ No row — R-54 is a stage-discipline rule, not a requirement.

## R-54a — TA-36's primary acceptance test is NOT this unit's

**Rule.** The story map makes **two different statements** about TA-36, and
**§ Cross-unit responsibilities is the reconciling one**:

| Where | What it says |
|---|---|
| § Per-unit coverage summary | `external-products` — `Acceptance rows as primary: WS-09, TA-36` |
| Table 2, TA-36's row | primary `external-products`, supporting `features-and-splits` |
| **§ Cross-unit responsibilities** | **`features-and-splits` — "enforcement and the primary negative-path acceptance test"**; `external-products` — **"upstream data production"** |

It says so in its own words: *"Reconciled 2026-08-22… Both were right about different
things."* **Four ownerships**, of which this unit holds two — neither the primary test:

| Ownership | Unit |
|---|---|
| **Data production** — driver series carrying their own interval semantics, no interpolation at any stage | **`external-products`** |
| **Enforcement** — the raise at `features.build_features` | `features-and-splits` |
| **Primary acceptance test** — TA-36, in `tests/test_feature_leakage_guards.py` | `features-and-splits` |
| **Upstream evidence / data-contract responsibility** — driver manifests recording per-series interval semantics and release grade | **`external-products`** |

**Constraint — the clause that decides what R-58 builds**, quoted: any upstream contract
test is *"documented separately and **not** replacing the primary rejection test."* R-58's
three limbs are this unit's **upstream contract evidence**, not TA-36's primary test.

**Constraint — this stage does NOT reallocate.** The reconciliation states the allocation
*"is the **default** and stands unless functional design produces verified evidence for a
better one; if it reallocates, it updates **both** artifacts."* This unit has produced no
such evidence, so the default stands and neither artifact is edited.

**Negative control.** Any artifact of this unit stating that it owns, builds or satisfies
TA-36's primary test fails review.

> **Corrected 2026-08-23 after an adversarial pass.** The first issue read **"owns WS-09 and
> TA-36"** flatly in all three files, citing § Per-unit coverage summary and Table 2 and never
> reaching § Cross-unit responsibilities. That would have had this unit build a primary
> acceptance test sited in a module owned by `features-and-splits` — an ownership overreach
> arriving from reading one table and stopping.

**Acceptance.** ⚠ No row — a stage-discipline rule.

## R-55 — `src/external` gets contracts here, and they are an amendment owed

**Rule (Q1 = D).** The contracts for `spaceweather.py`, `iri.py` and `gim.py` are designed
in this unit's artifacts and recorded as **one amendment owed** to `component-methods.md`,
needing a change record before stage 3.5 treats any of them as approved.

**Why an amendment at all.** `components.md` § `src/external` names the three modules and
states the importable-only rule. `component-methods.md` carries boundary-call blocks for
`src/features`, `src/models` and `src/evaluation` — and **nothing for `src/external`**: no
signature, no dataclass, no raise-contract.

> ## ⚠ A RECURRING PATTERN: NAMED MODULES WITH NO BOUNDARY CONTRACT
>
> *(Heading and lead corrected 2026-08-26, finding 6: the lead still listed `inventory.py` as a
> missing-contract finding, which the table below itself rules "intra-package and owed nothing" —
> and carried the typo "an three".)* `acquisition`'s named accessors, and now **this unit's
> three boundary-importable modules**. The total is **five owed amendments across three
> units**, derived by re-checking each claim against `component-methods.md`'s stated depth
> policy:
>
> | Unit | Owed amendments (boundary contracts only) | Count |
> |---|---|---|
> | `acquisition` | the named accessors (`open_d9_input` and the restricted writer); the `AccessRecord.purpose` extension plus a restricted-write function; `write_release`'s `identity_fields` parameter | **3** |
> | `inventory-and-registry` | `Station`'s provenance field — **`inventory.py`'s contract is intra-package and owed nothing** | **1** |
> | `external-products` (this unit) | boundary blocks for `iri.py`, `gim.py` and `spaceweather.py` | **1** |
> | **Total** | | **5 across 3 units** |
>
> > **Corrected 2026-08-23 after an adversarial pass. Two errors, both in a passage arguing
> > that a pattern be counted.** Superseded text, preserved: *"`governance-guards`'
> > `open_d9_input`… that is four owed amendments across four consecutive units… four
> > coincidences."* First, `open_d9_input` is **`acquisition`'s** finding about
> > `governance-guards`' module — `governance-guards`' own artifacts record **no**
> > missing-contract finding. Second, the total was **carried from prose rather than derived**:
> > `inventory-and-registry`'s own artifacts already read *"five owed amendments across two
> > units"* before this unit added its package.
>
> ## ⚠ CORRECTED 2026-08-23 — THE "PATTERN" WAS PARTLY A MISREADING
>
> `component-methods.md` § Depth states its own policy: **"Full signatures with types for
> cross-package boundary calls. Names and one-line purposes for intra-package functions…
> Every signature below is a cross-package boundary."** Its Assumptions add: **"[Q1]
> Intra-package helper names are indicative. `functional-design` (3.1) specifies them per
> unit and may rename freely — only the signatures above are contracts."**
>
> **So an absent block is not automatically a gap** — for an intra-package module it is the
> artifact's stated design, naming **this stage** as where the shape is specified. Re-checked
> against that policy:
>
> | Claimed gap | Verdict |
> |---|---|
> | `acquisition`'s named accessors; the `AccessRecord.purpose` extension; `write_release`'s `identity_fields` | **Real** — new or changed symbols in **boundary blocks that exist**, `scripts/` to `src/data` being cross-package |
> | `inventory-and-registry`'s `inventory.py` contract | **NOT an amendment** — `inventory.py` and `release.py` are the **same package** |
> | `inventory-and-registry`'s `Station` provenance field | **Real** — modifies an existing boundary dataclass |
> | **this unit's `src/external`** | **Real but NARROWER than first stated** — `iri.py` and `gim.py` are importable from `scripts/` and `src/evaluation/`, and `spaceweather.py` feeds `src/features`, so **those are boundary calls**. "An entire package with no contract" overstated it |
>
> **Corrected total: FIVE across three units**, not six. **Superseded text, preserved:**
> *"the amendment total is six across three units… the third consecutive unit whose design
> finds a named module with no contract."* The recurrence is real for boundary calls and was
> **not** the systemic under-specification the first issue argued; the consolidated-change-record
> proposal below is offered on the corrected footing.
>
> This stage therefore **proposes** — and does not take — that the **five** be carried as
> **ONE consolidated change record**, so a reviewer judges them as a set.
>
> **That proposal is the owner's to accept or decline.** This unit's amendment is recorded
> either way.

**Negative control.** Stage 3.5 attempting to implement any `src/external` module while the
change record is unapproved → the amendment's unapproved status is the refusal.

**Acceptance.** ⚠ No row.

## R-56 — The import allowlist is enforced transitively, and the static check is authoritative

**Rule (Q3 = D).** A **transitive static reachability scan** over the import graph asserts
that **no module outside the allowlist can reach `iri` or `gim`, directly or through
intermediaries.**

**The allowlist, at module-path granularity**: `scripts/04_build_external_products.py`, and
modules under `src/evaluation/`. An import from `src/data`, `src/features`, `src/models`,
`src/gnss`, a training script or a notebook violates it **identically**.

**Constraint — a path, never a unit.** `src/evaluation/` is owned by **three** units:
`evaluation-and-comparison` (`masks.py`, `metrics.py`), `statistical-inference`
(`bootstrap.py`), `regimes-diagnostics-reporting` (`regimes.py`, `diagnostics.py`,
`plots.py`). The allowlist grants an authorized path, never a whole unit's unrelated code.

**Why transitive rather than direct.** `project.md` § Forbidden states the constraint as
*"directly or transitively"*. A direct-import check **does not implement the rule its own
citation states**: a helper in `src/features` importing a shim that imports `gim` satisfies
a direct check and violates the rule.

**Constraint — this static check is AUTHORITATIVE, and the asymmetry with
`governance-guards` R-24 is deliberate.** A **module graph is a property of the source
tree**; a **loaded module is a property of a running process**, which is why
`assert_phase_boundary` reads `sys.modules`. **A static analysis is the right authority for a
static property.** The asymmetry is stated because an unexplained inconsistency between two
neighbouring designs reads as an oversight.

> **R-24's own rationale is different, and is not restated as this one.** R-24 argues from
> **Kaggle-versus-local-checkout** — a static scan of a local tree constrains nothing about
> the session a governed run executes in. The source-tree-versus-process framing above is
> **this rule's** argument, not a paraphrase of R-24's. Corrected 2026-08-23 after an
> adversarial pass found the first issue attributing it to R-24.

**⚠ Constraint — what this scan CANNOT see, stated rather than assumed away.** A **dynamic
import** — `importlib.import_module("src.external.gim")`, `__import__`, or a module path
assembled from a string — is invisible to an `ast` reachability walk. Two partial controls
and one residual:

1. A **grep-class check** for `importlib` and `__import__` in every module outside the
   allowlist, so a dynamic-import site is at least **visible** rather than silent — the same
   grep-evidence pattern this project already uses for SSN, residual and GRU absence.
2. Any such site outside the allowlist is a **review item**, not an automatic pass.
3. **Residual, uncovered and named:** a dynamic import whose target is computed at run time
   and whose call site uses neither literal. **No static check reaches it.** A run-time caller
   check was declined for the coupling reason below, so **this gap is accepted, not closed.**

**A run-time caller check inside `iri.py` and `gim.py` was declined**, with its reason: it
would make the two guarded modules aware of three sibling units' paths — the coupling
`governance-guards` R-28 declined for the same reason — and it would catch the violation
later than a scan does.

**Constraint — `spaceweather.py` is deliberately outside the restriction.** Drivers **are**
model inputs, subject to the availability lags.

**Constraint — distinct from the data-flow IRI rule.** `project.md` § Forbidden and
`governance-guards` R-23 govern whether an `iri_*` value reaches training. **Neither
substitutes for the other.**

**Negative controls.** Add a direct `iri` import to `src/features` → fails. Add a shim under
`src/data` that imports `gim`, and import the shim from `src/models` → **fails on
transitivity**. Import `iri` from a notebook → fails. Add an `importlib.import_module` call in
a module outside the allowlist → the grep-class check **surfaces it for review**. Import
`spaceweather` from `src/features` → **passes**, and a test asserts it does.

**Acceptance.** Contributes to WS-09 (**owned by this unit**) and TA-12 (owned by
`models-and-baselines`).

## R-57 — The F10.7 mean is trailing, proven as a property

**Rule (`project.md` § Forbidden, quoted).** *"NEVER use a centered rolling/trailing window
for F10.7 — only the trailing 81-day mean ending at the safe-lagged day is permitted; a
centered mean uses future days and is a defect, not a fallback."*

**Two limbs (Q4 = C):**

1. **Definitional** — the 81-day mean at day *d* equals the mean of the 81 days **ending at**
   the safe-lagged day.
2. **Future-independence** — perturbing **any** day after the safe-lagged day leaves the
   computed mean **unchanged**.

**Why limb 2 carries the rule.** Limb 1 tests the value at chosen days; a window that is
trailing everywhere except at a boundary — the series start *(the "March F10.7 gap" formerly
named here is corrected 2026-08-26, finding 2: D-21 and D-26 measure **365/365 day presence**;
what D-26 records for March–April is an **unresolved provenance question**, not missing days)* —
passes a spot check. **Limb 2 is a property that holds at every index**, and it is exactly
what *"uses future days"* means, stated so a test can fail on it. It covers boundary handling
and gap fill without enumerating them.

**Why this needs a property rather than review.** A centered mean produces a smoother,
entirely plausible series and every downstream check passes. **The failure is invisible in
validation** — it surfaces as unexplained optimism against a benchmark, or not at all.

**Not generalised to the other drivers**, with a reason: Kp/ap3, Hp60/ap60 and Dst are
governed by D-10.2's **alignment** contract rather than a window, and R-58 already tests that
with two named negative controls and an approved row. A second, differently-shaped guarantee
over the same series would be two rules about one fact.

**Constraint — F10.7's frozen selection choices are applied, not decided**: D-21 (daily
median), D-22 (duplicate UT records take the mean, with a QC flag; provider-defined
correction semantics take precedence when documented), D-23 (the four high-spread days
flagged and retained with the median as representative).

**Negative controls.** Compute a centered mean → limb 1 fails at every index and limb 2 fails
on perturbation. Perturb a day after the safe-lagged day → the mean **must not move**. Shift
the window by one day at the series start → limb 2 fails where limb 1 alone would pass.

**Acceptance.** Contributes to WS-11 and TA-08 (both owned by `features-and-splits`).

## R-57a — Missing driver values carry forward at most 3 hours, then the row is excluded

**Rule (FR-P1-04-3; TC-09, `binding: hard` — the register names this the central
leakage-prevention rule; TE §6.2's dictionary column "Carry-forward <= 3 h, then exclude").**
A missing external-driver value at an epoch may be filled by carrying the last observed value
forward for **at most 3 hours**; beyond that bound the row is **excluded**, never filled.
The bound is read from `configs/features.yaml`, never hardcoded.

**Negative control (FR-P1-04-3's own criterion).** Inject a 4-hour gap into a driver series →
the affected rows are **excluded**, and a carry-forward of 4 hours anywhere → fails.

### Constraint — the bound has NO STATED MEANING on the one daily-cadence series, and this rule RAISES rather than guesses

*(Added 2026-08-28 on **Recommendation 13** (reviewer finding `TEC-01`, `MAJOR`). The bound
above is written for an **epoch-indexed** series; **F10.7's alignment is `Daily`** (R-58's
table). D-21 makes the composition binding — F10.7's carry-forward *"composes with, and does
not override, the ≤ 3 h carry-forward bound on external drivers"* — and **no rule in this
artifact set states what a 3-hour bound means on a series whose native step is 24 hours.**
This unit's own iteration-1 adversarial pass recorded the gap at `business-logic-model.md`
§ Review — 2026-08-26, iteration 1, and R-57a, added on **finding 4 of that same review**,
did not reach the daily case. Derived 2026-08-28 over all **48** `functional-design`
artifacts: the only text joining `3 h` to `daily`/`F10.7` was that unremediated review note.)*

**The mechanism, which is all this stage has authority to fix.** Where the **next daily
F10.7 median is not yet available** at a forecast origin — `availability_ts(median(D)) =
00:00 UTC on D+1` per **D-25**, so unavailability is a real, derivable state and not a
hypothetical — driver-series availability resolution **raises `FeatureAvailabilityError`,
naming the origin timestamp, the last available median's day, and the elapsed staleness in
BOTH units (clock hours and whole daily steps)**, and **stops**. It does **not** silently
carry forward, and it does **not** silently exclude.

This is **TE §18.3's mandated posture, quoted**: *"Claude Code or any equivalent agent must
not implement an affected component while its P0 decision is unresolved, and must stop and
report rather than choose a default."* The raise is the report.

**The substantive answer is a PROPOSAL PUT TO THE STUDENT AT G-04, and this rule does not
choose between the two readings.** Both are stated so the gate rules on a scope it can see:

| # | Reading | What it means for a day *D* whose `median(D-1)` is unavailable | Cost |
|---|---|---|---|
| **A — tabled as the proposal** | Bound staleness in the **series' own axis**: **one daily step = one carry-forward step**, the row excluded beyond one missing day | The day's rows survive on the previous median; a second consecutive missing median excludes | Re-expresses a frozen numeral in a **different unit**, which is §18.2-adjacent and needs the Student's explicit freeze. A one-day-stale median is **48 h old at hour 23** |
| **B — the alternative** | Apply the bound **literally in clock hours**: rows beyond **hour 03** of day *D* are excluded, and the excluded count is recorded as a **split-manifest field** | **20 of 24 scored rows lost per affected day, in all three cells at once** | Changes no frozen numeral and is the most conservative reading; thins the December scored set for a reason **unrelated to the ionosphere**, on a driver that is constant across cells (R-63) |

**Why A is the tabled proposal and not this stage's decision.** "≤ 3 h" bounds staleness in
the **series' own resolution** — three hours is exactly **one step** of a 3-hourly Kp series,
and the daily analogue of one step is one day; **D-10.2 already treats F10.7's alignment as
`Daily`** rather than as an hourly series with gaps. That is an argument, not an authority.
**Choosing between A and B here would be an agent filling a §18.2 item by convenience**, which
`project.md` § Forbidden prohibits outright. **The freeze is the Student's, at G-04.**

**The trigger is live, not hypothetical.** **D-26** records F10.7 **March–April 2022
provenance as UNRESOLVED**, and **D-25**'s convention delays every value **1 to 2 hours**
beyond observation completion (measured: completion at 22 UT on 120 days and 23 UT on 245 days
of 2022), so the unavailability window is a designed property of the series rather than an
outage scenario.

**`configs/features.yaml` gains the composition rule as a NAMED FIELD —
`carry_forward_composition`** — not a constant buried in `spaceweather.py` (TC-03e and
`project.md` § Forbidden: no scientific constant lives in source or a notebook). The field
carries the adopted reading (A or B), and the §18.3 preflight asserts it is **not `TBD`** before
any component that applies the bound is implemented. Until the gate fills it, the field is `TBD`
and the raise above is what runs. The field is mirrored on `DriverSeries` at
`domain-entities.md` § 1.

**Negative control, for whichever reading the gate adopts** (specification for
`test_feature_availability.py`, whose primary siting is `features-and-splits`'):

- **While the field is `TBD`:** inject an origin at which no daily median is available →
  **`FeatureAvailabilityError`**, naming the origin and the staleness in both units. A
  carry-forward or an exclusion that proceeds **silently** → **fails**.
- **If A is adopted:** two consecutive missing medians → the rows **exclude**; one missing
  median → the rows **survive** on the previous median. Both directions asserted, because a
  single-direction test lets the other half regress silently (R-61's shape).
- **If B is adopted:** hours 04–23 of the affected day **exclude**, hours 00–03 **survive**,
  and the **excluded count appears as a split-manifest field** — a bare pass is not evidence.

> **This rule decides no scientific value.** It fixes the failure mode (**stop and report**)
> and routes the value (**the composition's unit**) to the Student at **G-04**.

**Acceptance.** ⚠ No §16/§19 row of its own; enforced through §18.3's gate-test list.
*(Rule added 2026-08-26 on adversarial finding 4, which was Major: this unit carries
FR-P1-04-3 and no rule, mechanism, entity field or negative control existed for it in any of
the three artifacts — W-5, where the requirement-to-workflow map routed it, disclaims it.)*
*(Constraint added 2026-08-28 on Recommendation 13; the daily composition remains an **open
G-04 freeze item** and is reported as such, not closed here.)*

## R-58 — Driver alignment, and its three limbs

**Rule (FR-P1-04-17, D-10.2, Q5 = D).** How a **present** value maps onto the hourly grid:

| Series | Rule |
|---|---|
| Kp / ap3 | Repeated **only within its own defined 3-hour interval** |
| Dst | Aligned to **its own hourly averaging interval** — *"not shifted to a neighbouring hour for convenience"* |
| F10.7 | Daily |
| **All** | **No driver is interpolated, at any stage** |

**Three limbs, all of TA-36's criterion:**

1. Kp repeated **outside** its 3-hour interval → **fails**.
2. Dst **shifted to a neighbouring hour** → **fails**.
3. An **AST-level scan over a named token set**, plus a **NaN/fill conservation invariant**,
   finds no interpolation on any driver series *(limb 3 rewritten 2026-08-28 —
   **Recommendation 38**; superseded text: "A **grep-level check** finds no interpolation call
   on any driver series.")*

**Why limb 3 matters independently.** *"No driver is interpolated, at any stage"* is
absolute, and a static scan is the only check that reaches a call site no fixture exercises.
**Building limbs 1 and 2 alone leaves the row partially satisfied while looking complete.**

### Constraint — limb 3's mechanism: a NAMED token set, an AST-level scan, and a CONSERVATION INVARIANT

*(Added 2026-08-28 on **Recommendation 38** (reviewer finding `DATA-06`). The prior limb 3 was
a grep with **no declared token list and no conservation invariant**, and its stated rationale
— *"a grep is the only check that reaches a call site no fixture exercises"* — is true of the
class of check and false of the spelling. **TC-09 is `binding: hard` and the register names it
the CENTRAL leakage-prevention rule**, so a spot check is not enough here. The sibling
`acquisition` **R-37** already states this exact miss class in writing — *"An alias, or a
vectorised expression that fills without naming a fill function"* — and closes it with
**NaN-count conservation**; the mechanism was in hand, so deferring would have left a gap with
the answer already written one unit over.)*

**1. The token set, named rather than implied.** The scan flags, at minimum:

| Spelling | Why it is listed separately |
|---|---|
| `.interpolate(` | The obvious case, and the only one the old limb plausibly caught |
| `.ffill(` / `.bfill(` / `.pad(` / `.backfill(` | Method-name fills that contain no substring of "interpolate" |
| `.fillna(` — **any** call, `method=` or not | A `value=`-form `fillna` fills just as effectively |
| `.reindex(..., method=…)` / `.asfreq(..., method=…)` | Fill hidden in an **index operation** rather than a fill call |
| `.resample(...).interpolate(` / `.resample(...).ffill(` / `.upsample`-style chains | Fill hidden behind a **resample**, which reads as an aggregation |
| `np.interp`, `numpy.interp` | Function-level, no method receiver to key on |
| `scipy.interpolate.*` — including `interp1d`, `griddata`, `splrep`/`splev`, `PchipInterpolator`, `CubicSpline` | A whole module, not one name |
| `pandas.Series.combine_first`, `.update(`, `.where(...).fillna` composites | Fills by **merging another series in**, naming no fill function |

**The list is a floor, not a ceiling, and that is why it is not the whole mechanism.** A
`getattr`-dispatched call, a fill reached through an alias bound earlier in the module, or a
vectorised boolean-mask assignment (`s[s.isna()] = <expr>`) **names none of these tokens**.

**2. The scan is AST-LEVEL, not textual.** It resolves the call target through the module's
import bindings and local aliases, so `import pandas as pd` / `f = pd.Series.interpolate` /
`f(s)` is **reached**, and a token appearing inside a string literal or comment is **not**
flagged. A textual grep gets both of those wrong in opposite directions.

**3. The conservation invariant, which is what actually carries the rule.** This is the limb
that holds regardless of spelling, and it makes `carry_forward_h` **load-bearing rather than
decorative** (`domain-entities.md` § 1):

> For every driver series, **the count of epochs carrying a value that is not an observation
> at that epoch EQUALS the count of epochs recorded as carried-forward under R-57a.** Any
> value present at an epoch with **no observation and no recorded carry-forward FAILS.**

Carried as the machine-readable manifest field **`carried_forward_epochs`** (per series,
`domain-entities.md` § 8), asserted equal to `DriverSeries.carry_forward_h`'s recorded count. A
**manifest field rather than only a test result** is deliberate, for the reason `acquisition`
R-37 gives: **FR-P1-04-17's row (TA-36) is `Pending` and FR-P1-04-3 has no row at all**, so a
field is evidence that survives the absence of a gate, where a test result is not — nothing is
obliged to run it.

Stated as a law rather than a scan, this catches **any** fill — aliased, vectorised, dispatched
or not yet invented — because it constrains the **emitted series** rather than the source text.
It is `acquisition` R-37's third row applied to the alignment side of the same contract.

**4. How the invariant distinguishes the SANCTIONED fill from a prohibited one, by
construction.** R-57a's ≤ 3 h carry-forward **is a permitted fill**, so a naive token scan
**false-positives on the project's own approved mechanism** — a collision the old limb 3 did
not address. The invariant resolves it without an exclusion list: a carried-forward epoch is
permitted **precisely because it is recorded** in `carry_forward_h`; an unrecorded filled epoch
is prohibited **precisely because it is not**. The distinction is the record, not the spelling.
The token scan is therefore scoped to **`src/external/spaceweather.py` and the driver path**,
and R-57a's carry-forward is implemented as a **recorded** operation rather than as a
fill-function call, so it does not trip the scan.

**Negative controls for limb 3** — three, because the first two each miss what the third
catches, mirroring `acquisition` R-37's table:

| # | Injection | Expected |
|---|---|---|
| 1 | Add `.interpolate()` on a driver series | **The AST scan fails**, naming the module, line and resolved call target |
| 2 | Add a fill through an **alias** (`f = pd.Series.ffill; f(s)`) or a `getattr` dispatch | **The AST scan fails** — this is the case a textual grep passes |
| 3 | Add a **vectorised** fill that names no fill function (`s[s.isna()] = s.shift(1)[s.isna()]`) | **The AST scan MISSES it and the conservation invariant FAILS** — asserted in that order, so the test proves the invariant is doing the work rather than riding the scan |

**Where the primary test lives.** TC-09 and NFR-LEAK-01 are enforced at the feature-building
boundary: the primary test is **`features-and-splits`' `tests/test_feature_leakage_guards.py`**
per **R-54a**. **The three controls above are this unit's UPSTREAM CONTRACT EVIDENCE**, and the
conservation invariant's own manifest field is emitted here. **This unit does not own TA-36's
row** and a passing control here does not satisfy it.

**Constraint — alignment and carry-forward are TESTED SEPARATELY.** FR-P1-04-17 states it is
*"distinct from FR-P1-04-3's ≤ 3 h carry-forward"*: alignment governs a **present** value,
carry-forward a **missing** one. Two rules governing adjacent behaviour on the same series is
exactly where one test gets counted twice, and this project has already had a requirement
counted as covered on a neighbouring row's evidence.

**Negative controls.** The three limbs above are themselves the negative controls — each
asserts a violation is caught, **and limb 3 carries three of its own** (the AST-scan,
alias/`getattr`, and vectorised-fill injections in the Constraint above, added 2026-08-28 on
Recommendation 38). Additionally: satisfy the carry-forward rule and violate alignment → **the
alignment test still fails**, proving neither passes on the other's evidence.

**Acceptance.** **TA-36** — ⚠ status **`Pending`: the row exists; not implemented, not
executed, not passing.** **Its PRIMARY test is `features-and-splits`'**, sited at the
feature-building enforcement boundary in `tests/test_feature_leakage_guards.py`. **The three
limbs above are this unit's UPSTREAM CONTRACT EVIDENCE**, *"documented separately and not
replacing the primary rejection test"* — see R-54a.

## R-59 — IRI generation is blocked without a passing, complete, pre-declared validation

**Rule (FR-P1-04-15, Q6 = D).** *"A validation failure **blocks** benchmark generation rather
than warning."* Four limbs:

1. **Generation refuses without a passing report.**
2. **The tolerance carries a timestamp preceding the comparison**; generation refuses if the
   ordering is violated.
3. **The report's seven content areas are asserted field by field.**
4. **The benchmark's own drivers appear as rows in the same frozen availability matrix used
   for ML features** — observation timestamp, **publication timestamp or, absent one, the
   approved conservative convention (for F10.7: D-25's 00:00 UTC on D+1, never same-day) with
   the documented absence and an unverified-latency statement** (`CR-2026-08-22-EV-12`; corrected
   2026-08-26, finding 2), release status, safe lag.

**Why limb 2.** *"A passing report exists"* is satisfiable by a report whose tolerance was
chosen **after** the comparison ran — the failure the **predeclared** clause exists to
prevent, invisible to any presence check. A frozen value plus a timestamp is the only evidence
class that distinguishes *declared before* from *fitted after*, and it is the shape
`inventory-and-registry` R-52 adopted for retrospective split redesign.

**Why limb 3.** The seven areas: the pinned package/build with **exact version or commit**;
all model switches and the topside option; **the altitude ceiling stated explicitly as
2000 km**; units and output extraction; the coordinate, time, solar and geomagnetic driver
inputs **with confirmation that no driver is future-centered or unavailable at target time**;
**five to ten samples** spanning sites, day and night, quiet and disturbed, validated against
the **official IRI interface**; and the predeclared tolerance. A report missing the ceiling or
the driver-availability confirmation would otherwise **pass on presence** — the same defect
class as a short protected-set list passing a membership check.

**Why limb 4 has scientific consequence.** *A benchmark fed better-timed drivers than the
model gets is not a benchmark.* FR-P1-04-15's criterion states this limb explicitly.

> **The availability matrix is `features-and-splits`' artifact.** This unit **states the
> obligation and does not own the row.**

**Constraint — the 26,000-call workload is timed** and its measured runtime recorded; the
`iri2016` Fortran build **re-establishes from pins on a cold session** (TC-04).

**Constraint — B-01 is labelled generated, not trained**, and appears in the model/config
inventory. Never fitted.

**Negative controls.** Fail validation and attempt generation → **blocked**, not warned. Omit
any one of the seven content areas → fails. Record the tolerance after the comparison ran →
fails on ordering. Generate with the benchmark's drivers absent from the availability matrix
→ fails.

**Acceptance.** ⚠ **NO ROW.** FR-P1-04-15's blocking behaviour, report completeness and
predeclared tolerance are all unrowed. **Designing this is not testing it.**

## R-60 — The GIM comparator: four obligations, one blocked

**Rule (FR-P1-04-18, Vision §6.10, Q7 = D).**

| # | Obligation | Enforcement |
|---|---|---|
| 1 | Interpolation is **bilinear in space, linear in time, with a longitude-rotation correction** — §18.2 **Student-owned forbidden choice** (Q-15) | ⚠ **UNSET. Generation REFUSES while it is unset** |
| 2 | *"One sample interpolation must be hand-checked against the code"*; **EV-11 places the hand-calculation BEFORE comparator generation** | The hand-check's **timestamp must precede** generation; **a comparator generated before the hand-check FAILS rather than being accepted retrospectively** |
| 3 | The Phase 1 GIM comparison *"is explicitly a map-product-to-map-product comparison … cannot validate receiver-level station VTEC or serve as an independent target check"*, stated **wherever the comparison is reported** | **Emitted by the reporting path itself** |
| 4 | The comparator is **never tuned and then claimed independent** | **A partial grep-class control** (below), plus a reporting-discipline rule. **Not fully checkable**, and said so |

**Why obligation 1 is blocked rather than specified.** TE §18.2: *"No implementer or coding
agent may fill such a value by convenience."* Specifying the mechanism while leaving the
**value** implicitly fillable is exactly what that prohibits. Refusing to generate while it is
unset is the zero-TBD preflight's shape.

**Why obligation 3 is emitted by the code.** It is a rule about **every** report — including
ones nobody has written yet. A sentence a human must remember does not survive a new report
being added; one emitted from the path that produces the comparison does.

**Obligation 4: a partial control, and an honestly named residual.** *"Never tuned and then
claimed independent"* is a claim about what was **not** done, and **no injected value proves a
negation of that kind.** But *fully* unprovable and *wholly* uncheckable are different
things, and this project already uses grep-evidence for absence claims — SSN, residual and
GRU modules are all asserted absent that way (TA-08, TA-12).

| Limb | Reaches |
|---|---|
| **Grep-class check**: no fitting, tuning, optimiser or parameter-search call appears in `gim.py` | A tuning step **left in the comparator module** — the realistic case |
| **The report states no tuning occurred**, and the independence claim cites the overlap audit | The claim being made without its evidence |
| **⚠ Residual, uncovered** | Tuning performed **outside** `gim.py` and its result pasted in as a constant. No check reaches it; it is a **reporting-discipline obligation** and is named as such |

> **Corrected 2026-08-23 after an adversarial pass.** The first issue declared obligation 4
> **fully uncheckable** and offered nothing — giving up one level too early, in a project that
> uses grep-evidence for exactly this class of absence claim elsewhere in this same artifact
> set. The residual above is real; the whole obligation was not.

**Constraint — FR-P1-04-9's separate obligations**: the **`gim_network_overlap_flag` audit is
present and its result disclosed**; **no independence claim precedes the audit**; the **flag
value appears wherever GIM is compared**; and **C-01 is labelled generated, not trained** in
the model/config inventory.

### Constraint — the disclosure obligation is UNCONDITIONAL, and this unit's framing is confirmed rather than relaxed

*(Confirmed and strengthened 2026-08-28 on **Recommendation 41** (reviewer finding `BENCH-07`).
The board found this unit's framing **correct** and two sibling units' conditional; nothing here
was wrong, so nothing here is reversed — the strengthening below states the ordering the
conditional phrasing left implicit.)*

**The authority is unconditional.** Vision **§6.10** line 599: *"The project **must** audit
whether ARUC, BSHM, or NICO appear in the GIM input network and disclose any overlap as
dependence. **No independence claim may be made before that audit.**"* `requirements.md`
**FR-P1-04-9**'s criterion is that the tolerance report, config snapshot and **overlap audit
ALL EXIST** — an existence condition, not a condition on the audit having been run at some
later moment.

**The distinction that matters, stated plainly.** *"Disclose the flag **once the audit has
run**"* and *"an audit must exist before any GIM comparison is emitted"* are **not the same
obligation**. The first is satisfied vacuously while no audit exists — a GIM comparison emitted
before the audit **trips no control at all**. The second is the one §6.10 states. **This unit
asserts the second**, and asserts it on the **existence of a GIM comparison artifact**, not on
the audit's having run:

> **Emitting, serializing or reporting ANY GIM comparison with no registered overlap-audit
> result and its flag value FAILS.** The trigger is the comparison's existence.

**Ordering, enforced the same way obligation 2 already enforces the hand-check.** The **overlap
audit's recorded timestamp must PRECEDE comparator generation**, exactly as obligation 2
requires of the interpolation hand-check, and generation **fails** if the ordering is violated
rather than accepting the audit retrospectively. Obligation 2 already establishes that a
timestamp-ordering assertion is the enforceable form here; this reuses it rather than inventing
a second shape.

**⚠ Obligation 1's generation refusal is a MITIGATION THAT EXPIRES, and must not be read as
closing this.** Today no GIM comparator can be produced at all, because obligation 1 refuses
generation while the **Q-15** interpolation rule is unset (a §18.2 Student-owned forbidden
choice). That refusal is **absolute today and gone the moment Q-15 is decided** — the ordering
risk becomes live at precisely the moment the mitigation disappears. **The residual outlives the
mitigation**, so the ordering is enforced above rather than left to obligation 1.

**The conditional phrasing was INHERITED, not invented.** `project.md` § Mandated itself reads
*"ALWAYS disclose the `gim_network_overlap_flag` result **once the input-network overlap audit
runs**"*, so the sibling units track the affirmed rule faithfully; the defect is in the affirmed
wording, not in their fidelity to it. **A wording correction to `project.md` § Mandated is owed
at the §13 learnings ritual** — human-gated, and **reported here rather than applied**: no stage
edits a memory file directly (`org.md` § Mandated). Derived 2026-08-28: the conditional phrasing
appears **7 times** across `evaluation-and-comparison` and `regimes-diagnostics-reporting`
(2 in `evaluation-and-comparison/business-rules.md`, 1 each in that unit's
`business-logic-model.md` and `domain-entities.md`, and 1 in each of
`regimes-diagnostics-reporting`'s three) — **not the 5 the recommendation states**; the
correction is recorded rather than carried forward.

**Negative controls for this constraint.** Emit a GIM comparison artifact with **no registered
overlap-audit result** → **fails**, keyed to the comparison's existence. Register an audit whose
timestamp **follows** comparator generation → **fails** on ordering, not accepted
retrospectively. Make an independence claim with the audit absent → **fails** (already stated
below). Produce a GIM comparison whose report **omits the flag value** → **fails**.

**Negative controls.** Attempt generation with the interpolation rule unset → **refused**.
Generate before the hand-check is recorded → **fails**, not accepted retrospectively. Produce
a comparison report without the map-to-map sentence → fails, because the reporting path emits
it. Make an independence claim before the overlap audit → fails. Add a fitting or
parameter-search call to `gim.py` → the grep-class control **fails** (obligation 4's partial
limb).

**Acceptance.** ⚠ **NO ROW** for FR-P1-04-18. FR-P1-04-9 is accepted by WS-09 (**owned by this
unit**) and TA-12.

## R-61 — A missing month is recorded; a hash mismatch terminates

**Rule (REQ-ENG-9, Q8 = D).**

| Condition | Tier | Behaviour |
|---|---|---|
| A missing month | **Completeness shortfall** | **Non-fatal.** Recorded as a machine-readable manifest field **naming which months** |
| A hash mismatch | **Integrity violation** | **Terminates** the run non-zero, **naming the file and the violated expectation** |

**The workspace fact this closes:** `scripts/audit_ec1_drivers.py` **line 184 returns `0`
regardless of missing months.**

**Why not simply return non-zero on missing months.** That reads the gap as an exit-code bug
when it is a **tier question**, and it collapses the two-tier posture: a month absent from the
provider is a fact to record; a hash that does not match invalidates everything downstream of
it. **Making an ordinary partial retrieval abort the run is how a guard gets worked around.**

**Why the field names the months rather than counting them.** A count says something is wrong;
the list says what to do. This unit's outputs feed G-P1A's coverage decision, where
`inventory-and-registry` **R-51** forbids *"an unattributed number"* — a bare count is that
same shape.

**Negative controls — two, asserting OPPOSITE outcomes**, because REQ-ENG-9's criterion names
both and a single test covers half the requirement while letting the other half regress
silently. Inject a missing month → **the run continues** and the manifest names it. Inject a
hash mismatch → **the run stops** non-zero with a naming message.

**Acceptance.** ⚠ **NO ROW.**

## R-62 — Dst's three restrictions are kept apart, and eligibility is a property of the data

**Rule (D-10.1, D-11, D-13, TC-11, Q9 = D).**

| # | Restriction | Enforcement |
|---|---|---|
| 1 | **Diagnostic/hindcast-only** — never a confirmatory ML feature | Enforced downstream by `features-and-splits`; **stated here** |
| 2 | **Release grades never mixed** within one series; the grade for calendar 2022 recorded before use | A **grade field**; **mixed grades fail at construction** |
| 3 | **Provisional Dst may characterise fixture selection only** — never a modelling input, never a frozen tolerance, **never a G-05 regime count** | The **provisional grade renders the series ineligible** for those three, **asserted at the point of use** |

**Why eligibility is a property of the data rather than a rule about it.** A rule that depends
on three units remembering is the shape **D-15** warns about for the restricted root. Making
the consumer read the grade is the only form that survives a consumer nobody has written yet —
and it makes the **permitted** fixture-characterisation use explicitly distinguishable from
the three that are not.

**The live trap, present in the workspace today.**
`evidence/audit_ec1_2026-08-15/kyoto_dst/dst_provisional_202212.html` exists; **D-11** used
provisional Dst to characterise the fixture window, which is **permitted**; and **D-13**
requires the December regime count to come from **GFZ Kp/Hp60 at a recorded release grade**,
explicitly barring any provisional-Dst-derived figure.

**Negative controls.** Mix two grades in one series → **fails at construction**. Feed a
provisional-graded series to a modelling input → refused. Freeze a tolerance from a
provisional-graded series → refused. **Compute a regime count from a provisional-graded series
→ FAILS**, naming D-13's GFZ Kp/Hp60 requirement. Use a provisional-graded series to
characterise a fixture window → **permitted**, and a test asserts it is.

**Why the regime-count control is not optional.** It is the restriction with a **concrete
artifact already present to get wrong**, and a named G-05 consequence. This project's
methodology pairs a negative control with **every** hard rule rather than with the convenient
ones.

**A fourth consequence, not restated as a rule here:** `governance-guards` **R-26** names Dst
as the driver class excluded from the December-hit definition, on the grounds that it is
diagnostic-only.

**Acceptance.** Contributes to WS-11 and TA-08 (both owned by `features-and-splits`).

## R-63 — Driver series are time-indexed only

**Rule (FR-P1-04-4, TC-12).** One value per epoch, **identical across all three cells**.

**Constraint — the consequence, stated because it is the reason the rule exists**: a join must
**never imply a per-cell measurement**, and **a station performance difference must never be
attributed to local forcing the dataset does not contain.**

**Constraint — no driver is backfilled** from future final or definitive archived values.
NFR-LEAK-01 governs *timing* only: a series can satisfy its declared lag while being built
from reanalysed values, **invisible to every existing check and fatal on discovery**.

### Constraint — the DRIVER-PRODUCT half of the reanalysed-value check, with its verifiability limits stated per series

*(Added 2026-08-28 on **Recommendation 14** (reviewer finding `TEC-05`, `MAJOR`). Derived over
all **48** `functional-design` artifacts: the phrase `reanalysed-value check` appears **3 times,
all three in `acquisition`** — `business-logic-model.md:601`, `business-rules.md:482` and
`business-rules.md:610` — **and the check is defined nowhere.** `requirements.md` **FR-P1-01-8**
carries it as a criterion with status **`UNTESTED`**. `acquisition` is being amended in parallel
to define the check itself; **this constraint carries the driver-product half only** and does
not restate `acquisition`'s. Of every leakage guard in this design, this was the one that was a
**name rather than a property with a negative control**.)*

**What every driver manifest records, per series** (`domain-entities.md` § 8):

| Field | Why it is required |
|---|---|
| `release_status` | The **declared** grade — real-time / provisional / final. One per series for 2022, never mixed (D-10.1) |
| `retrieval_date` | Fixes **when** the bytes were obtained, which bounds which provider revision could have been served |
| **Full provider product identity, INCLUDING any version suffix** | Version drift is **already observed in this dataset** (`g.002` versus `g.003`), so a product name without its suffix cannot be compared against anything later. Composes with the already-affirmed re-acquisition version-suffix obligation (`team.md` § Walking Skeleton, DATA-07) |
| `sha256` | Binds the recorded identity to the actual bytes |

**What the check ASSERTS, on this unit's side.** Internal consistency of those four fields, and
that the **declared status matches the CONTEMPORANEOUS grade the feature contract requires** —
not merely that a status is present. A series declared `final` where the feature contract
requires a contemporaneous operational value **fails**, because `project.md` § Forbidden makes
final archived values non-equivalent to what a 2022 forecast origin could have seen.

**Where the file carries no provenance column, the SANCTIONED evidence is the absence plus an
explicit unverified-status statement** — the same shape **D-25** uses for publication latency and
the shape the project already approved under `CR-2026-08-22-EV-12`. Recording the absence is
evidence; **inferring a grade from silence is not.**

**⚠ Verifiability limits, stated PER SERIES rather than as one blanket claim.** On the evidence
held today the check is **not substantively executable on any of the four series**, and saying so
is part of the mechanism:

| Series | Held today | Verifiability | Consequence |
|---|---|---|---|
| **F10.7** (NRCan) | `fluxtable.txt` | **DECLARED-STATUS ONLY.** **D-22** records the file as having *"exactly seven columns … and **no correction, revision, version or provenance column**"*; **D-21** records the provider's publication latency as *"not derivable"* from it | **No detection is possible from the bytes.** The declared status plus the documented absence and an unverified-status statement is the whole of the evidence, and is labelled as such |
| **Dst** (Kyoto WDC) | `dst_provisional_2022MM.html` | **DECLARED-STATUS ONLY.** The grade is inferable **from the filename alone**, and **D-10.1**'s open item on the 2022 Kyoto grade *"remains unchecked"* per **D-11** | Same as F10.7. A filename is not a provenance column; recorded as declared, not verified |
| **Kp / ap3** (GFZ) | ⚠ **NEVER RETRIEVED** | **SUBSTANTIVE DETECTION IS SPECIFIABLE NOW** | See below |
| **Hp60 / ap60** (GFZ) | ⚠ **NEVER RETRIEVED** | **SUBSTANTIVE DETECTION IS SPECIFIABLE NOW** | See below |

**For the two UNRETRIEVED GFZ series, acquisition retrieves BOTH the near-real-time and the
definitive product and asserts them against each other value by value.** GFZ publishes distinct
definitive and near-real-time products, so a disagreement is **detectable rather than declared**:
a value matching the definitive product where the near-real-time product differs **fails**, which
is the actual backfill this rule exists to catch.

**Why this must be specified NOW and not after acquisition.** It costs almost nothing while the
retrieval is unwritten and **everything if retrofitted**, because a provider archive is not
guaranteed to retain an earlier-grade 2022 product once the definitive one supersedes it. This is
exactly the ordering error `project.md` § Way of Working names — *"ALWAYS raise a targeted
follow-up when an answer would require building something before the work that specifies its
contents"* — read forward rather than backward. **It is a specification against the deferred
retrieval, not a claim that the retrieval has happened.**

**Negative controls, re-worded to assert ONLY what the mechanism can catch.** *(The
`acquisition`-side control as written — *"Backfill a value from a final archive → the
reanalysed-value check fails"* — **cannot fire** on F10.7 or Dst, because nothing in either
byte stream distinguishes a reanalysed value from a contemporaneous one. Asserting an
undetectable failure is how a requirement reads as designed while remaining unenforceable.)*

| # | Injection | Expected |
|---|---|---|
| 1 | Declare `release_status` **inconsistent with the recorded provider product identity** (e.g. `final` against a `dst_provisional_*` filename) → | **FAILS.** This is the detectable form, and it replaces the undetectable-backfill wording |
| 2 | Omit `release_status`, `retrieval_date`, the **version suffix**, or `sha256` from any driver manifest → | **FAILS** on manifest completeness |
| 3 | Record a status for a file carrying **no provenance column** *without* the documented-absence and unverified-status statement → | **FAILS.** The absence must be **stated**, not implied by silence |
| 4 | Mix two release grades within one series → | **FAILS at construction** (D-10.1, already asserted at R-62) |
| 5 | **GFZ only:** supply a value matching the **definitive** product where the **near-real-time** product for that epoch differs → | **FAILS.** The one substantive backfill detection this design can offer |

> **Stated as a residual, not discharged.** For **F10.7 and Dst** the rule's own failure mode —
> a reanalysed value that satisfies every lag, alignment and carry-forward assertion — remains
> **BOUNDED RATHER THAN CLOSED**, and no artifact may report it as closed. The verifiability
> limit is the finding, and it is carried to **G-04** with the EV-12/`EC1-R-4` provider-
> documentation limb, which is owned outside this project.

**Negative controls.** Produce a driver value that differs between cells at one epoch → fails.
Join a driver to the cell grid such that the result implies a per-cell measurement → fails.
Build a series from a final archive for a date whose contemporaneous value differs → **for the
two GFZ series the near-real-time cross-assertion fails; for F10.7 and Dst this is NOT
DETECTABLE and control 1 above is what fires instead** *(control re-worded 2026-08-28 on
Recommendation 14 — the superseded wording, "the release-status check fails", asserted a failure
the mechanism cannot produce on either held series)*.

**Acceptance.** ⚠ **NO ROW** for FR-P1-04-4. The reanalysed-value criterion belongs to
**FR-P1-01-8**, status **`UNTESTED`**, whose check `acquisition` defines; this unit's half is the
manifest contract above and is **likewise unrowed**.

---

## The four requirements with no acceptance row

**4 of this unit's 7**, derived from story-map § Per-unit coverage summary, which reads
`external-products (4)`. **Not 5** — see R-54. No §19 criterion is drafted; §19 rows are owned
by stage 3.2 and change control.

| Requirement | Rule | Evidence that would close it |
|---|---|---|
| **REQ-ENG-9** | R-61 | An approved row plus **two** passing results asserting opposite outcomes — an injected missing month yields a non-silent machine-readable record naming the months and the run continues; an injected hash mismatch yields a non-zero exit naming the file and the violated expectation |
| **FR-P1-04-4** | R-63 | An approved row plus a passing schema test asserting one value per epoch, identical across all three cells |
| **FR-P1-04-15** | R-59 | An approved row plus passing results for all four limbs: generation blocked on a failing report; tolerance timestamp preceding the comparison; the seven content areas present; the benchmark's drivers in the frozen availability matrix — plus the recorded 26,000-call runtime |
| **FR-P1-04-18** | R-60 | An approved row plus a `gim_interpolation_and_independence_report` carrying the interpolation rule, the hand-checked sample **with its worked arithmetic**, and the map-to-map statement, with the hand-check timestamp **preceding** generation. **Blocked on the Student's Q-15 decision** for the interpolation rule itself |

> **No artifact, manifest or report may state or imply that any of the four is covered,
> satisfied or verified.** Designing the mechanism is not a test; implementing it is not a row.

> **TA-36 is separate and is not one of the four.** It is an **approved** row whose status is
> **`Pending`** — not implemented, not executed, not passing. FR-P1-04-17 therefore has a row
> and no result, which is a different condition from having neither. **And its primary test is
> `features-and-splits`'** (R-54a): this unit holds data production and upstream evidence, so
> even a passing upstream contract test here would not satisfy TA-36.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence, so this unit opens at **R-54**. If per-unit numbering was intended, say so at the gate.
- **[assumption]** The **story map governs** where it and `unit-of-work.md` § 6 disagree (R-54). Neither artifact is edited by this stage.
- **[assumption]** The availability matrix R-59 limb 4 requires is **`features-and-splits`' artifact**; obligation stated, row not owned.
- **[assumption]** `audit_ec1_drivers.py` migrates here with `--config configs/` and its numbered position. Target shape designed; migration commit not made.
- **Open — `src/external` has no contract block** for any of its three modules (R-55). **One amendment owed**, not approved.
- **Open — FIVE owed amendments across three units** (`acquisition` 3, `inventory-and-registry` 1, this unit 1), **boundary contracts only**. R-55 **proposes** one consolidated change record; the owner accepts or declines. **Corrected twice on 2026-08-23**: from "four across four" with `open_d9_input` misattributed; then from "six across three", after § Depth was found to specify boundary calls only and to name this stage as where intra-package shapes are specified.
- **Open — TA-36's primary acceptance test is `features-and-splits`'** (R-54a), not this unit's. This unit holds data production and upstream evidence. The story map's § Per-unit coverage summary and § Cross-unit responsibilities disagree; the reconciliation governs, and this stage does **not** reallocate.
- **Open — the import-allowlist scan cannot see a run-time-computed dynamic import** (R-56). Two partial controls are built; the residual is **accepted, not closed**.
- **Open — FR-P1-04-18 obligation 4 is only partially checkable** (R-60): tuning performed outside `gim.py` and pasted in as a constant reaches no check.
- **Open — FR-P1-04-18's interpolation rule is UNSET** (R-60), a §18.2 Student-owned forbidden choice (Q-15). **Comparator generation refuses while it stands.** *(Added 2026-08-28, Recommendation 41: that refusal is a **mitigation that EXPIRES the moment Q-15 is decided**, and must not be read as closing the overlap-audit ordering — which R-60's new Constraint now enforces on the existence of a GIM comparison artifact instead.)*
- **Open — the F10.7 daily carry-forward composition is a G-04 FREEZE ITEM, not decided here** (R-57a's new Constraint, added 2026-08-28 on Recommendation 13). D-21 makes the composition binding and no rule stated what a **3-hour** bound means on a series whose native step is **24 hours**. Reading **A** (one daily step = one carry-forward step) is **tabled as the proposal**; reading **B** (literal clock hours, excluding beyond hour 03 and recording the excluded count as a split-manifest field) is stated as the alternative. **This stage chooses neither** — choosing would be an agent filling a §18.2 item by convenience. Until the Student freezes it, `configs/features.yaml`'s **`carry_forward_composition`** field is `TBD` and driver-availability resolution **raises `FeatureAvailabilityError` and stops**. Owner: **Student**, §18.2 Q-16/Q-17, at **G-04**.
- **Open — the reanalysed-value check is BOUNDED, NOT CLOSED, for F10.7 and Dst** (R-63's new Constraint, added 2026-08-28 on Recommendation 14). Both are **declared-status-only**: no detection is possible from the bytes (D-22's seven columns with no provenance column; D-21's non-derivable publication latency; Kyoto's grade inferable from the filename alone, with D-10.1's 2022-grade item still unchecked per D-11). For the two **unretrieved** GFZ series the design specifies **now** that acquisition retrieve the near-real-time product alongside the definitive one and assert them value by value. The rule's own failure mode remains **bounded rather than closed** and **no artifact may report it as closed**. Owner: **Student**, with the provider-documentation limb (**EV-12 / EC1-R-4**) owned outside this project, at **G-04**.
- **Open — `FeatureAvailabilityError`'s DECLARATION SITE**, on the same open item as this unit's other unit-local exceptions (`domain-entities.md` § 9): a cross-unit agreement into `src/data/config.py`, or the `src/data/exceptions.py` §12 amendment. It derives from `foundation` R-01's `IntegrityError` base under that rule's *"any future integrity-related exception"* clause and is **not** claimed as one of R-01's named fifteen.
- **Open — four requirements with no acceptance row**: REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18.
- **Open — TA-36 is `Pending`**: approved, never run. Never cited as a result.
- **Closed 2026-08-26 (finding 8): the § 6 conflict no longer exists — the file was swept 2026-08-24; kept as the dated record.** *(Superseded bullet:)*  — `unit-of-work.md` § 6 carries stale text**, reported not edited: a five-item bold list including FR-P1-04-17, and `Acceptance rows (1). WS-09`.
- **Open — BLK-07's authorization limb**, carried forward. Nothing here reads the locked month; this unit's IRI/GIM products join at evaluation time onto the frozen comparison-wide mask.
- **G-09 is not signed.** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged. No rule here authorises creating `src/external/spaceweather.py`, `src/external/iri.py`, `src/external/gim.py` or `scripts/04_build_external_products.py`.
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

> **Re-saved 2026-08-25/26 under the post-twelve-redo receipt.** No rule changed; figures
> re-derived and unchanged (7 requirements, 4 untested, 2 acceptance rows). The exception base is
> named explicitly in `domain-entities.md` § 9. **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved 2026-08-26 under the thirteenth-redo receipt, after the terminal-pass remediation.**
> In this file: **R-54's trigger and table marked historical** (⛔ box — the § 6 conflict no
> longer exists, swept 2026-08-24; nothing currently reported to the gate under this rule); its
> "not swept" sentence dated; the Open bullet closed as a dated record; **R-57a stands** as
> FR-P1-04-3's rule; R-55's lead corrected. Figures unchanged (7/4/2).
> **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved unchanged 2026-08-26 under the fourteenth-redo receipt** (the redo finished the
> gate-record sweep in the sibling files; no rule here changed). **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved unchanged 2026-08-26 under the fourteenth-redo re-confirmation receipt** (finding 17's
> mojibake repair touched the question file only; no rule here changed). **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved 2026-08-28 under the post-redo receipt, on the project decision owner's ruling
> against `governance/reviews/GOV-2026-08-28-FD-01.md` (verdict FAIL).** The owner's ruling for
> the science items was **mechanism written, value routed to the gate**: this stage writes the
> executable mechanism and the stop-and-report raise, and the **value goes to the
> Student/Supervisor at G-04**. **No scientific value is decided here.**
>
> **Five items applied in this file, each with its Recommendation number at the point of change:**
>
> | Rec | Change | Where |
> |---|---|---|
> | **13** | R-57a gains a **daily-cadence Constraint**: a `FeatureAvailabilityError` stop-and-report raise on an unavailable daily median, reading **A tabled as the G-04 proposal** and reading **B** stated as the alternative with its 20-of-24-rows cost, **neither chosen**; `configs/features.yaml` gains the composition rule as a **named field**; negative controls specified for either adopted reading | R-57a |
> | **14** | R-63 gains the **driver-product half of the reanalysed-value check**: the four manifest fields including the **full provider product identity with version suffix**, the contemporaneous-grade assertion, the documented-absence-plus-unverified-status evidence shape, **per-series verifiability limits** (F10.7 and Dst **declared-status-only**), the **GFZ near-real-time cross-assertion specified now**, and five controls asserting **only what the mechanism can catch** | R-63 |
> | **38** | R-58 **limb 3 rewritten**: a **named token set**, an **AST-level** scan rather than a textual grep, and a **conservation invariant** binding filled epochs to `carry_forward_h`, with the sanctioned ≤ 3 h carry-forward distinguished **by construction** rather than by grep exclusion; three controls including the **vectorised** case | R-58 |
> | **41** | R-60's unconditional framing **confirmed and strengthened**: the control is keyed to a **GIM comparison artifact existing**, the audit timestamp must **precede** comparator generation, and obligation 1's refusal is labelled a **mitigation that expires when Q-15 is decided**. The conditional phrasing was **inherited from `project.md` § Mandated**; a wording correction there is **owed at the §13 learnings ritual and reported, not applied** | R-60 |
> | **46** | **D-25 and D-26 added to § Sources**, dated, in the form `acquisition` used on its own finding F2 | § Sources |
>
> **Counts re-derived programmatically 2026-08-28, not carried from prose:** **12** rule headings
> (`R-54`, `R-54a`, `R-55`…`R-57`, `R-57a`, `R-58`…`R-63`) — **unchanged, no rule added or
> renumbered**; **4** new `### Constraint` sections (one per science item, at R-57a, R-58, R-60,
> R-63); **15** new negative controls across them (**R-57a 3** bullets, **R-58 3** rows,
> **R-60 4**, **R-63 5** rows); **7** requirements, **4** with no acceptance row, **2** acceptance
> rows (**WS-09** owned, **TA-36** `Pending`) — all unchanged.
>
> **Corrections to the dispatched brief, recorded rather than propagated:** the brief placed the
> operative D-25 citation at **R-60** line 404 — line 404 is inside **R-59** limb 4 (R-59 opens at
> 393, R-60 at 443); the brief placed R-60's FR-P1-04-9 Constraint at **486-489** — it was at
> **480-483**, with 486-489 being that rule's Negative-controls paragraph; and the conditional
> GIM phrasing counts **7** across the two sibling units, **not 5**.
>
> **IRI and CODE GIM remain evaluation-time-only comparators; Dst remains diagnostic-only; D-11
> continues to bar provisional Dst from any G-05 regime count. G-09 remains unsigned** ⚠ **G-09
> IS SIGNED as of 2026-08-28 (D-31)** *(annotation added 2026-08-29 on adversarial finding 1,
> Critical: this was the ONE live "G-09 remains unsigned" statement in this file the 2026-08-28
> annotation pass missed — the closing line of this same governance-remediation box — while the
> 2026-08-29 receipt below it certified that only the G-09 banner and its operative-clause
> annotations had changed. The other three comparator clauses in this sentence are untouched and
> remain in force.)* — module creation is authorised, **and nothing else changes**. D-31's
> disclosure travels with the signature: the TE §18.3 zero-TBD preflight **never ran**, `configs/`
> does not exist, the ten critical tests are **unexecuted in this environment**, and
> `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE
> §18.2 and §18.3's stop-and-report rule are unchanged. Nothing
> here authorises creating `src/external/spaceweather.py`, `src/external/iri.py`,
> `src/external/gim.py` or `scripts/04_build_external_products.py` **as a design decision of this
> rule**; that is now a G-09-authorised implementation act for stage 3.5, still bound by §18.3.

---

> **Re-confirmation receipt, 2026-08-29.** The 2026-08-27T21:49:36Z REDO jump reset every
> unit's receipt floor. This unit's only change after that floor was the **G-09 (D-31)
> supersession banner and its operative-clause annotations** — no design content moved, and
> Recs 13, 14, 38, 41 and 46 stand as remediated. The owner re-confirmed that content via the
> Consolidated Summary Confirmation at the foot of `functional-design-questions.md`, receipted
> `2026-08-29`. No line above this marker was touched by this pass.
