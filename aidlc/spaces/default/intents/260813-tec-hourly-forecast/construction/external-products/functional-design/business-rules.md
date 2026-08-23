# Business Rules — `external-products`

**Unit** `external-products` (Bolt 5) · **Kind** `library` · **Depends on**
`inventory-and-registry`

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
- `evidence/DECISIONS.md` — **D-5**, **D-10.1**, **D-10.2**, **D-10.3**, **D-11**, **D-13**, **D-21/22/23**.
- Workspace inspection, 2026-08-23: `scripts/audit_ec1_drivers.py` line 184; `evidence/audit_ec1_2026-08-15/kyoto_dst/dst_provisional_202212.html`; the absence of `src/` and `configs/`.
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
about this unit's untested count or acceptance rows, **the story map governs**, and both
stale statements are **reported at the gate, not edited**.

| Claim | `unit-of-work.md` § 6 | Story map — **governing** |
|---|---|---|
| Untested requirements | **5** (bold list includes FR-P1-04-17) | **4** — REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18 |
| Acceptance rows owned | **1** — WS-09 | **WS-09**, plus TA-36 in § Per-unit coverage summary — reconciled differently in § Cross-unit responsibilities (R-54a) |

**Why the story map.** `TA-36` was approved **2026-08-22** under Vision §15.2
(`CR-2026-08-22-LEAKAGE-TA`) as FR-P1-04-17's negative-path row, and the story map records
the resulting sweep — *"Changed 2026-08-22 by the addition of TA-33…TA-36: untested
40 → 36."* § 6 was not swept with it.

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

> ## ⚠ THIS IS THE THIRD CONSECUTIVE UNIT TO FIND A NAMED MODULE WITH NO CONTRACT
>
> `acquisition`'s named accessors, `inventory-and-registry`'s `inventory.py`, and now **an
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
trailing everywhere except at a boundary — the series start, or across the March F10.7 gap —
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
3. A **grep-level check** finds no interpolation call on any driver series.

**Why limb 3 matters independently.** *"No driver is interpolated, at any stage"* is
absolute, and a grep is the only check that reaches a call site no fixture exercises.
**Building limbs 1 and 2 alone leaves the row partially satisfied while looking complete.**

**Constraint — alignment and carry-forward are TESTED SEPARATELY.** FR-P1-04-17 states it is
*"distinct from FR-P1-04-3's ≤ 3 h carry-forward"*: alignment governs a **present** value,
carry-forward a **missing** one. Two rules governing adjacent behaviour on the same series is
exactly where one test gets counted twice, and this project has already had a requirement
counted as covered on a neighbouring row's evidence.

**Negative controls.** The three limbs above are themselves the negative controls — each
asserts a violation is caught. Additionally: satisfy the carry-forward rule and violate
alignment → **the alignment test still fails**, proving neither passes on the other's
evidence.

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
   for ML features** — observation timestamp, publication timestamp, release status, safe lag.

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

**Negative controls.** Produce a driver value that differs between cells at one epoch → fails.
Join a driver to the cell grid such that the result implies a per-cell measurement → fails.
Build a series from a final archive for a date whose contemporaneous value differs → the
release-status check fails.

**Acceptance.** ⚠ **NO ROW** for FR-P1-04-4.

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
- **Open — FR-P1-04-18's interpolation rule is UNSET** (R-60), a §18.2 Student-owned forbidden choice (Q-15). **Comparator generation refuses while it stands.**
- **Open — four requirements with no acceptance row**: REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18.
- **Open — TA-36 is `Pending`**: approved, never run. Never cited as a result.
- **Open — `unit-of-work.md` § 6 carries stale text**, reported not edited: a five-item bold list including FR-P1-04-17, and `Acceptance rows (1). WS-09`.
- **Open — BLK-07's authorization limb**, carried forward. Nothing here reads the locked month; this unit's IRI/GIM products join at evaluation time onto the frozen comparison-wide mask.
- **G-09 is not signed.** No rule here authorises creating `src/external/spaceweather.py`, `src/external/iri.py`, `src/external/gim.py` or `scripts/04_build_external_products.py`.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.
