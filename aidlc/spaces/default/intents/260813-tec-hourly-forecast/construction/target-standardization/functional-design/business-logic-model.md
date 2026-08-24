# Business Logic Model — `target-standardization`

**Unit** `target-standardization` (Bolt 6) · **Kind** `library` · **Depends on**
`inventory-and-registry`

> **Re-established a sixth time 2026-08-24**, on a **new stage attempt** — Inception closed
> and Construction opened at 2026-08-24T11:46:26Z, resetting the receipt floor for every
> unit. **No content of this unit changed.** Both `foundation` passes of that day (the
> amendment pass and the sites 9–11 addendum, in
> `governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md`) touch nothing this unit
> reads. **Stated because this unit leans on it hardest:** `component-methods.md` **§ Depth**
> — the cross-package-boundary-calls-only policy that makes intra-package shapes this
> stage's to specify — is **not** what Amendment B changed; B added fields to a `foundation`
> entity. Amendment A was declined, so **no count moved**. **The READY verdict in § Review
> belongs to the previous attempt.**

> **Corrected and re-established 2026-08-23, after two adversarial passes.** Iteration 1
> found a **Critical** — nine citations of "`inventory-and-registry` R-20", a unit whose
> rules run R-44…R-53 and which has no R-20 — and a **Major**: **"documented QC"**, one of
> the four permitted transformations, is defined nowhere in scope, which defeated the
> closed-set claim as first stated. Both are fixed here, with the superseded readings
> preserved; the citations now point at **`governance-guards` R-20**, the rule that actually
> boxes the inherited question. A fifth redo then swept the four remaining stale citations
> out of this unit's **question file**, which had been locked when the artifacts were
> corrected. **No answer to any question changed.**

The workflows this unit implements: turning validated provider files into the Phase 1
hourly target rows under **D-17**'s contract, stamping the three definition IDs on every
row, labelling the product **location-sampled gridded VTEC**, and producing the Phase 1
portion of the verification and target-uncertainty evidence.

**Phase 1 only.** This unit must never produce a DCB, STEC, mapping, satellite or arc
field, and must never label the gridded product a receiver-specific station observation.

**It decides no scientific value.** The aggregation statistic is **D-16**, the cell rule
**D-1**, the field contract **D-17**, the four support values **D-19** — all frozen
elsewhere and applied here.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 5 — the `Owns` list, the boundary, the 6 requirements, the implementation notes; and **BLK-05** with its four-limb status table.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2 plus § Per-unit coverage summary. **Derived by reading the rows:** 6 requirements, **1** with no acceptance row (FR-P1-03-5); **owns** TA-19; **supports** TA-15. § Cross-unit responsibilities carries the NFR-DQ-01 / FR-P1-05-10 / TA-19 crossing.
- `../../../inception/requirements-analysis/requirements.md` — FR-P1-03-1…-5; NFR-TDEF-01; NFR-DQ-01; FR-P1-05-10; § Known defects rows 10 and 11.
- `../../../inception/application-design/components.md` — `prepared.py`'s row and § Assumptions' record of the `02` ordinal collision.
- `../../../inception/application-design/component-methods.md` § Depth — **cross-package boundary calls only**; intra-package shapes are **this stage's** to specify.
- `../../../inception/application-design/services.md` § The nine stage scripts, § Stage entry contract.
- `../inventory-and-registry/functional-design/business-rules.md` — R-45's registry and R-49's prepared-product schema.
- `../governance-guards/functional-design/business-rules.md` — **R-23**, **R-24**.
- `evidence/DECISIONS.md` — **D-1**, **D-16**, **D-17**, **D-19**.
- Workspace inspection, 2026-08-23: `tests/` holds three modules, none this unit's; `src/` and `configs/` absent.
- `functional-design-questions.md` (**Q1 through Q9**), `domain-entities.md`, `business-rules.md`.

---

## W-1 — Standardizing the Phase 1 hourly target

```
INPUT   validated provider files; the station registry; config: ConfigSnapshot
OUTPUT  Phase 1 target rows under D-17's 16-field contract
RAISES  StandardizationError; PhaseBoundaryError (through the stage entry contract)
```

**Exactly four transformations are permitted** (FR-P1-03-1), and no fifth:

1. **Documented QC**
2. **UTC normalization**
3. **Cell selection** — `cell = (floor(lat), floor(lon))`, half-open `[floor, floor+1)`
   (D-1)
4. **The hourly aggregation** — **D-16**: the **median** of the valid provider VTEC samples
   inside the UTC hour for the station's frozen cell

**Provider values are preserved.** Every row carries `phase_id`, `source_id` and
`target_definition_id` (FR-P1-03-3).

**Enters through `foundation`'s six-step stage entry contract**, whose **step 4** is
`governance-guards.assert_phase_boundary` — `02_standardize_prepared_target.py` is Phase 1
and does not skip it.

## W-2 — Proving "only the documented transformations"

FR-P1-03-1's criterion has **two limbs**, and the second exists because the first is not
enough:

> *"A value-level diff against the provider bytes shows only the documented
> transformations, **and** the aggregation statistic cited by the run resolves to **D-16**
> rather than to a default."*

**Limb 1 — the diff enumerates the four permitted transformations and fails on a fifth**
(Q7 = D). *"Only"* is a closed-set claim, and an open-ended diff cannot express it: it can
show what changed, not that nothing else was allowed to. Enumerating makes a fifth
transformation a **failure** rather than something a reviewer must notice.

> ## ⚠ "DOCUMENTED QC" IS NOT DEFINED UPSTREAM, AND THE CLOSED SET IS ONLY AS CLOSED AS ITS WEAKEST MEMBER
>
> **Corrected 2026-08-23 after an adversarial pass.** Three of the four permitted
> transformations are fully specified — **UTC normalization**, **cell selection** (D-1's
> floor rule, half-open), **the hourly aggregation** (D-16's median). The fourth,
> **"documented QC"**, is named by FR-P1-03-1 and **defined nowhere in scope** — not in this
> unit's artifacts, not upstream.
>
> **That defeats the closed-set claim as first stated.** A value-level diff can only fail on
> "a fifth transformation" if it can attribute each observed change to one of four **known**
> operations. With one member's content unspecified, an undocumented change is
> indistinguishable from a QC-attributable one — which is exactly the failure this mechanism
> was written to prevent.
>
> **The fix, and it is this stage's to make:** the QC operations are **enumerated as a named
> list in `configs/data.yaml`**, so "documented QC" becomes a closed sub-set rather than an
> open category, and **an operation outside that list fails like a fifth transformation
> would**. `component-methods.md` § Depth assigns intra-package specification to this stage,
> so enumerating them here is in scope.
>
> **What is NOT settled here: which operations belong on that list.** No upstream document
> enumerates them, and this stage does not invent a set of QC operations for a product whose
> quality characteristics are recorded in D-19 rather than in a QC catalogue. **The
> enumeration's membership is raised at the gate**, and until it is fixed the closed-set
> check is **specified but not yet satisfiable** — stated rather than claimed.


**Limb 2 — the statistic is resolved from `configs/data.yaml` citing D-16, and a run cannot
proceed on a default.** *"Recording which statistic it used"* is satisfiable by a run that
recorded a default; refusing to run without an explicit D-16 citation is the zero-TBD
preflight's shape, and the same treatment `external-products` gave FR-P1-04-18's unset
interpolation rule.

> **Zenith-weighted aggregation is DEFERRED as not computable, and nothing is substituted.**
> The Phase 1 product carries five columns — `ut1_unix`, `gdlat`, `glon`, `tec`, `dtec` —
> with **no elevation, zenith angle or satellite identifier**. TE §18.2 lists the
> aggregation statistic as a **Student + Supervisor forbidden choice**, exercised under the
> recorded authority delegation. **A later implementer with a richer product may not
> reinstate zenith weighting as an improvement**: it would silently change a §18.2 item.

**A correction worth carrying, from the requirement's own history.** An earlier revision
*"asserted 'the frozen hourly aggregation' when no decision had frozen it; that false
statement was corrected first, and the freeze recorded second, as two explicit stages."* The
order matters: a claim of frozen-ness is not the freeze.

## W-3 — The D-17 field contract, and the schema test against it

**Sixteen fields, counted from D-17's enumeration** and matching BLK-05's own *"exactly
D-17's approved 16 fields"*:

| # | Field | # | Field |
|---|---|---|---|
| 1 | `interval_start_utc` | 9 | `within_hour_spread_tecu` |
| 2 | `station_id` | 10 | `largest_internal_gap_s` |
| 3 | `cell_gdlat` | 11 | `provider_dtec_summary` |
| 4 | `cell_glon` | 12 | `aggregation_config_id` |
| 5 | `cell_lat_bounds` | 13 | `target_valid` |
| 6 | `cell_lon_bounds` | 14 | `phase_id` |
| 7 | `vtec_tecu` (median, D-16) | 15 | `source_id` |
| 8 | `valid_observation_count` | 16 | `target_definition_id` |

**Excluded and NEVER substituted**: `valid_satellite_count`, any per-satellite or per-IPP
quantity, zenith angle or weight, elevation, DCB, STEC, mapping output, arc or slip
statistics. *"None is derivable from a five-column gridded product"*, audited 2026-08-21
across all twelve request manifests.

**`processor_qc_flags` carries aggregation flags only.** The package, DCB, arc, elevation,
slip and mapping classes are **Phase 2 and recorded not-applicable rather than emitted
empty**.

**The check (Q5 = D), three ordered steps:**

```mermaid
graph TD
  C["configs/data.yaml:<br/>the 16-field set"]
  D17["D-17 (the freeze)"]
  A{"config set == D-17?"}
  R["row under test"]
  B{"required 16 present?<br/>excluded set absent?"}
  OK["pass"]
  X1["SchemaError:<br/>the CONFIG drifted"]
  X2["SchemaError:<br/>the ROW is wrong"]
  C --> A
  D17 --> A
  A -->|no| X1
  A -->|yes| B
  R --> B
  B -->|yes| OK
  B -->|no| X2
```

Text fallback: the field set is read from config; before any row is compared, the config set
is asserted equal to D-17's; only then is the row checked for the sixteen required fields
and for the absence of every excluded one. A config drift and a row defect fail differently
and say which layer broke.

**Why the config-equals-D-17 assertion.** A config-sourced field list can drift from the
decision that froze it, and then **every row passes against the wrong contract** — config
and artifact agreeing while both drift from the authority.

> **The open half, inherited rather than re-solved:** where step 2 reads D-17 **from**.
> **`governance-guards` R-20** carries the same question for D-24 and states it exactly:
> *"it must assert against the **authority**, not merely against the config — otherwise
> config and manifest can agree with each other while both drift."* Its two routes each
> carry a named cost, and **no third option is invented** there or here.

**Why the excluded set is asserted, not only the required one.** BLK-05's approved
acceptance behaviour names **both**: an **excluded or additional** field fails, and a
**missing required** field fails. A required-only assertion catches the second and misses the
first — and the first is exactly where a Phase 2 quantity would appear. `governance-guards`
**R-23**'s produced-field limb guards the same boundary independently; **two checks on that
boundary is the design's intent, not duplication.**

> ## ⚠ BLK-05 — TWO LIMBS RESOLVED, TWO OPEN, AND THIS STAGE DISCHARGES NEITHER OPEN ONE
>
> | Limb | Status |
> |---|---|
> | Module naming — `tests/test_prepared_target_schema.py` | **RESOLVED 2026-08-22** (`CR-2026-08-22-TARGET-SCHEMA-TEST`) |
> | Documentation — §12 tree entry and provenance table | **RESOLVED 2026-08-22** |
> | **Test implementation** | **PENDING** — the module **does not exist**; gated by G-09 and stage 3.5 |
> | **Execution evidence** | **PENDING** — **never run.** *"No result of any kind is claimed"* |
>
> The register states that *"approving a filename does not resolve the blocker."* **The
> symmetric statement is made here: approving this design does not resolve it either.** The
> two open limbs survive this stage's approval unchanged.
>
> Every citation of the module in this unit's artifacts carries its non-existence. A module
> or row cited without its status reads as coverage — the failure that let FR-P1-02-8 sit
> behind a withdrawn `TA-29` for five revisions, and that had TA-36 cited without `Pending`.

## W-4 — Verification: what Phase 1 actually runs

`unit-of-work.md` § 5: *"`03_verify_processing.py`'s Phase 1 scope is thinner than its §12
description implies… `functional-design` settles exactly what it runs."*

**Vision §6.9 lists six uncertainty-budget contents. Four are Phase 2 quantities** — per
satellite, per IPP, or geometry — that the five-column product cannot yield (§ Known defects
row 11).

| Content | Phase 1 | Treatment |
|---|---|---|
| The two applicable contents | ✅ | **Produced** |
| The **asymmetry statement** | ✅ | **Produced**, stated below |
| The four Phase 2 quantities | ❌ | **Recorded not-applicable with their reason**, never emitted empty |

**The asymmetry statement, quoted** (FR-P1-05-10): a slowly varying per-station-day bias
partially cancels in the paired difference but *"does not cancel in the derived percentage
summary, because it inflates the reference denominator."*

**The budget asserts its own completeness against the Phase 1-applicable set** (Q3 = D).
FR-P1-05-10's failure condition is *"a budget file that exists and states nothing"*, and a
completeness assertion is what turns that from a reading into a check.

> **§6.9's list is UNQUALIFIED in the source.** Row 11 records it: *"§6.9 states the list
> without a phase qualifier"*, and *"adding the phase qualifier to §6.9 runs through Vision
> §15.2."* A reader who checks §6.9 finds six required items and this unit producing two —
> **without this note that reads as non-compliance rather than a recorded, governed gap.**

## W-5 — Labelling, and the mismatch disclosure

**FR-P1-03-4**: the Phase 1 target is labelled **location-sampled gridded VTEC**, *"never
receiver-specific station-observed VTEC, everywhere it is described."*
**NFR-TDEF-01** adds that the **grid-cell-versus-IPP mismatch is disclosed**.

**Its criterion is a review, not a test** — *"a claims-checklist review over every artifact
and figure caption finds no mislabelling"* — over artifacts that mostly do not exist yet.

**Three limbs (Q8 = D), and one stated gap:**

1. **The label is emitted by the code that writes the target**, travelling with the rows the
   way `target_definition_id` already does. This removes the commonest cause of
   mislabelling: a writer who does not know which product they have.
2. **The grid-cell-versus-IPP mismatch statement is emitted by the reporting path.**
   `project.md` § Mandated requires the spatial-representativeness statement *"at the point
   where any IRI or GIM comparison is reported"* — a rule about **every future report**,
   which `external-products` W-7 answers the same way and for the same reason.
3. **A grep-class check** that the prohibited phrasing does not appear in this unit's
   outputs — the pattern this project already uses for SSN, residual and GRU absence.
4. **⚠ Stated gap:** a **figure caption inside a notebook image** reaches none of the three.
   That case stays with the claims-checklist review, and saying so is the difference between
   a bounded mechanism and an overclaimed one.

**Why not the review alone.** §16 and §19 both hold that visual inspection is insufficient,
and this rule governs artifacts nobody has written.

## W-6 — The `02` ordinal collision

`scripts/02_standardize_prepared_target.py` (Phase 1, this unit) and
`scripts/02_build_vtec_target.py` (Phase 2) share the ordinal in §12's tree.

**The adopted reading**, quoted from `unit-of-work.md` § 5: *"the ordinal denotes the
pipeline position and `--phase` selects exactly one, so a clean run contains one `02` per
phase."*

**This is a recorded §12 defect, not a resolved one.** Both `unit-of-work.md` § 5 and
`components.md` § Assumptions say so, and the register adds that **`code-generation` must
not invent a `02a`/`02b` convention.**

**Mechanism (Q4 = C):** the clean-run contract asserts that a run contains **exactly one**
`02` script, selected by `--phase`. That makes the adopted reading **falsifiable** — two
`02` scripts executing in one run is the failure the reading assumes cannot happen, and
nothing currently detects it — and it makes the `02a`/`02b` workaround visibly unnecessary,
because the ambiguity it would resolve is already resolved by `--phase`.

> **Not asserted here:** that `02_build_vtec_target.py` is unreachable under `--phase 1`.
> That script is the one which **skips step 4** and asserts `phase == 2` instead, so its
> reachability is a **phase-boundary** question belonging to `governance-guards` R-23.
> **Noted for that unit rather than guarded twice** — two rules about one fact is how they
> drift apart.

## W-7 — The target uncertainty budget, and what this unit does not own

**NFR-DQ-01 has four contents**, not one:

| # | Content | Built here |
|---|---|---|
| 1 | Units, times, signs and fill values **documented** | ✅ |
| 2 | **Unexplained negative VTEC rejected** | ✅ |
| 3 | Missingness and support reported **by cell and month** | ✅ |
| 4 | Target uncertainty budget **produced** | ✅ |

**Content 2's operative word is "unexplained".** A negative VTEC is not a small value but an
**impossible** one, so an explained negative requires a **recorded explanation** rather than
silent acceptance; an unexplained one is rejected.

**Content 3 is keyed to the same cell and month identifiers `inventory-and-registry`'s
G-P1A record uses** (Q9 = D). The two artifacts describe the same coverage from different
sides, and a G-P1A reviewer reading both must be able to line them up. Different keying is
how two reports about one dataset become impossible to reconcile.

> **TA-19 has two halves and this unit owns one.** § Cross-unit responsibilities:
> *"`target-standardization` (produces it)"*; *"`regimes-diagnostics-reporting` (reports it
> adjacent to the primary result)"* — *"Production and adjacent reporting are separate
> obligations in the same requirement family."* TA-19's evidence is *"uncertainty budget
> artifact **+ its placement in the results section**"*, and **the placement half is not this
> unit's**.
>
> Stated because the symmetric error was made two units ago: `external-products` claimed
> TA-36's primary test while it was sited in `features-and-splits`' module.

## W-8 — The §12 module count, and a file that contradicts itself

`unit-of-work.md` § 5 says FR-P1-03-5's test *"exists in none of the **19** modules TE §12's
amended tree enumerates."* **The same file's BLK-05 limb table says 21.**

**Derived, not carried** (Q2 = D):

| Source | Count |
|---|---|
| `unit-of-work.md` § 5 | **19** — froze at the first of three same-day amendments |
| `unit-of-work.md` BLK-05 limb table | **21**, with the history 17 → 19 → 20 → 21 and its derivation command |
| `requirements.md` REQ-ENG-4 | **21**, *"re-derived from that amended tree on 2026-08-22 by listing its `test_*.py` entries"* |

**Two independent sources read 21.** This unit uses **21**.

**The BLK-05 comment records that its own "20" was itself a fourth stale site**, missed by a
prior sweep's Rec 3 — so § 5's 19 is that file's second known stale-count site, not an
isolated slip.

**Reported at the gate for an annotate-in-place decision**, not edited:
`CHANGE_RECORD_PROCEDURE.md` reserves approved-stage artifacts, and the owner **has** granted
annotate-in-place before, at `GOV-2026-08-22-INC-01` Rec 7 — the precedent is recorded in the
very comment documenting the last such correction.

## W-9 — What Bolt 6 builds, and what it must not

**Permitted before G-09**: module structure, interfaces, placeholder CLI definitions,
configuration wiring, safe fail-fast behaviour, and this unit's `tests/` scaffolding.

**Barred until G-09 is signed for the affected component**: implementing any component whose
P0 decision is unresolved; filling any `TBD — freeze gate` field; executing any governed
run; generating code for a unit carrying an open blocker on that scope.

> **`src/data/prepared.py`, `scripts/02_standardize_prepared_target.py`,
> `scripts/03_verify_processing.py` and `tests/test_prepared_target_schema.py` DO NOT
> EXIST**, and neither does `src/` or `configs/`.
>
> **The zero-TBD preflight is NOT YET RUNNABLE on this component**, because `configs/` does
> not exist. D-19's four values are **a decision made, never a check passed**.
>
> **No numerical equivalence may be claimed between the Phase 1 and Phase 2 targets.**
> Cross-phase results test protocol transfer across a **target-domain shift**.

---

## Requirement-to-workflow map

Acceptance derived from story-map Table 1; owners from Table 2's `primary` cell, with
§ Cross-unit responsibilities consulted for the TA-19 crossing.

| Requirement | Workflow | Tested by (Table 1) | Row primary owner |
|---|---|---|---|
| FR-P1-03-1 | W-1, W-2 | TA-04 | `inventory-and-registry` |
| FR-P1-03-2 | W-1 (through the stage entry contract) | TA-27 | `governance-guards` |
| FR-P1-03-3 | W-1, W-3 | TA-15 | `foundation` |
| FR-P1-03-4 | W-5 | TA-15 | `foundation` |
| **FR-P1-03-5** | W-3 | ⚠ **NO ACCEPTANCE ROW** | — |
| NFR-TDEF-01 | W-5 | TA-15 | `foundation` |
| NFR-DQ-01 | W-7 | TA-19 | **`target-standardization`** — **production half only**; placement is `regimes-diagnostics-reporting`'s |

**6 requirements, 1 without an acceptance row.** This unit **owns** TA-19 and **supports**
TA-15.

### The one without a row, and what would close it

No §19 criterion is drafted — §19 rows are owned by stage 3.2 and change control.

| Requirement | Evidence that would close it |
|---|---|
| **FR-P1-03-5** | An approved §19 row asserting D-17's field contract — a valid 16-field row passes, an excluded or additional field fails, a missing required field fails — plus a **passing result** from `tests/test_prepared_target_schema.py`. **Both limbs are open**: the row does not exist, and neither does the module |

> **Why it has no row today, stated so the gap is legible.** WS-05 — the only field-contract
> row — is **deferred to G-P3A by FR-WS-4**. FR-P1-03-5 is enforced by the D-17 schema test
> and `tests/test_phase_boundary.py`; **neither is an acceptance row**, and one of the two
> does not exist.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence — `foundation` R-01…R-17, `governance-guards` R-18…R-29, `acquisition` R-30…R-43, `inventory-and-registry` R-44…R-53, `external-products` R-54…R-63 — so `business-rules.md` opens at **R-64**. If per-unit numbering was intended, say so at the gate.
- **[assumption]** `src/data/prepared.py` is **intra-package** and its shape is **this stage's to specify** (`component-methods.md` § Depth). **No amendment is owed**, and the running total stays **five across three units**.
- **[assumption]** The §12 tree enumerates **21** test modules; § 5's **19** is stale. See W-8.
- **[assumption]** D-17's field count is **16**, counted from its enumeration and matching BLK-05's own wording.
- **Open — BLK-05's implementation and execution limbs.** The module does not exist and has never been run. **Approving this stage discharges neither.**
- **Open — where the D-17 conformance check reads the frozen field set from.** W-3 asserts config-equals-D-17, which raises the same authority question **`governance-guards` R-20** already carries for D-24: *"it must assert against the **authority**, not merely against the config — otherwise config and manifest can agree with each other while both drift."* **No third option is invented**; carried to the gate. **Citation corrected 2026-08-23**: the first issue read *"`inventory-and-registry` R-20"*, a unit whose rules run R-44…R-53 and which has no R-20; the rule carrying this question is `governance-guards`'. `inventory-and-registry` **R-49** carries a related but distinct point — that D-24's protected set is not reopened.
- **Open — `unit-of-work.md` § 5's stale "19"**, reported for an annotate-in-place decision, not edited.
- **Open — the `02` ordinal collision**, a recorded §12 defect. **No `02a`/`02b` convention.** The Phase-2-script reachability check is left to `governance-guards` R-23.
- **Open — Vision §6.9's content list is unqualified in the source.** The phase qualifier runs through **Vision §15.2**.
- **Open — the zero-TBD preflight is not yet runnable** on this component; D-19 is a decision made, not a check passed.
- **Open — the notebook-caption case of FR-P1-03-4 reaches no machine check** and stays with the claims-checklist review.
- **Open — an obligation stated on a sibling:** W-7's cell-and-month keying must agree with `inventory-and-registry`'s G-P1A record.
- **G-09 is not signed.** No workflow here authorises creating any module.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-23T07:03:44Z
**Iteration:** 2 (final)

### Disposition of iteration-1 findings

| # | Iteration-1 finding | Disposition | How verified |
|---|---|---|---|
| 1 | Critical — every "`inventory-and-registry` R-20" cross-reference is broken (no R-20 in that unit; R-49 carries the content). Recommended: repoint to `inventory-and-registry` R-49. | **Resolved — and my recommendation was the near-miss, correctly not taken.** Read both candidate rules directly. `governance-guards` R-20 ("The canonical contract handles every mutation of the protected set") carries an open box worded *"Where this test gets D-24's list from is OPEN… It must assert against the **authority**, not merely against the config — otherwise config and manifest can agree with each other while both drift from D-24"* — this is verbatim the same structural question `target-standardization`'s W-3/R-66/§5 raise for D-17 (config-vs-authority drift on a frozen field/protected set). `inventory-and-registry` R-49 ("Schema validation runs against a governed schema") carries a different point in its own box — that D-24's 17-item protected set is **not reopened** as an 18th item — which is not the question being inherited. The correction (repoint to `governance-guards` R-20, with an inline note distinguishing it from R-49) is the correct referent; R-49 would have been a wrong fix compounding the original error. | Read `governance-guards/functional-design/business-rules.md` R-20 (l.280-309) and `inventory-and-registry/functional-design/business-rules.md` R-49 (l.253-281) in full, in the two carved-out sibling files, and compared each rule's own boxed open question against the exact open-question wording repeated at every corrected citation site in this unit's four artifacts. |
| 2 | Major — "Documented QC" is one of four enumerated permitted transformations in the closed-set diff check (R-64/W-2) but is never defined anywhere in scope, so the closed-set claim is unimplementable as designed. | **Resolved as an honest, bounded disclosure — not a restatement of the gap.** The added box states plainly that three of four transformations are fully specified and the fourth is not, that this "defeats the closed-set claim as first stated," names the fix (`configs/data.yaml` enumerates the QC operations as a named list, so an out-of-list operation fails like a fifth transformation), cites the correct authority for assigning that specification to this stage (`component-methods.md` § Depth), and explicitly declines to invent the list's membership, stating it is "specified but not yet satisfiable" and raised at the gate. This mirrors the project's own accepted pattern for supervisor/authority-owned gaps elsewhere in the same artifact (the R-20 authority question, the `02` ordinal collision) — flagged, mechanism specified, membership left to the gate rather than invented by convenience, consistent with `project.md` § Forbidden's rule against filling a TBD value by convenience. R-64's negative controls gained two matching cases ("Apply a QC operation absent from the enumerated QC list → fails like a fifth transformation" and "Leave the QC list unset → the closed-set check is not satisfiable, and the run says so rather than passing vacuously"), which actually make the new state testable rather than merely asserting it away. | Reread the box and the surrounding W-2/R-64/§4 text in all three affected artifacts (`business-logic-model.md` l.72-96, `business-rules.md` l.58-96, `domain-entities.md` l.158-194) and confirmed the box's wording, the negative-control additions, and the § Depth citation are identical and consistent across all three. Checked the box does not contradict its own body (it doesn't: the body still calls the diff "what turns only into a check," and the box narrows that claim rather than negating it). |

### New findings (this iteration)

None survived verification. One item is deliberately not yet fixed and is reported for visibility rather than as a defect: `functional-design-questions.md` still carries four stale "`inventory-and-registry` R-20" citations (Q5's option-C impact line l.234, the Q5 recommendation l.242, and two `## Assumptions & Open Questions` entries l.416 and l.450) because that file's confirmation receipt is locked and a redo jump would be required to edit it — a known, deliberate deferral, not an undiscovered defect. It is a live stale reference and should be corrected the next time this file's receipt is reopened, but it does not block this stage: the three artifacts actually under construction-design authority here (`business-logic-model.md`, `business-rules.md`, `domain-entities.md`) all carry the corrected `governance-guards` R-20 citation with an inline note recording and explaining the correction, so an implementer reading the design (rather than the interview transcript) sees the right reference. No other live stale reference, duplicated/mangled text, orphaned heading, or box-body contradiction was found in the three primary artifacts.

### Failed refutation attempts

- **Re-litigating disposition 1 the other way.** Attempted to construct a reading under which `inventory-and-registry` R-49 was in fact the intended referent (e.g., treating "protected set not reopened" as loosely the same idea as "assert against authority not config"). It isn't: R-49's box is about declining to add an eighteenth protected item, a scope-boundary decision, not an assertion-source mechanism; R-20's box is about where a conformance check reads its authoritative list from. The two boxes answer different questions, and only R-20's wording matches what W-3/R-66/§5 quote verbatim.
- **Re-litigating disposition 2 as evasion.** Attempted to treat "specified but not yet satisfiable" as a restatement dressed up in new language. It isn't: the box adds a concrete mechanism (a named config list), a concrete authority for who specifies it (`component-methods.md` § Depth), and two new negative-control cases that make the interim state (list absent, or an operation outside the list) itself testable — none of which existed in the pre-correction text, which only asserted the enumeration and said nothing about how to close it.
- **§12 module count (21 vs. 19), D-17's 16 fields, D-19's four values, the TA-19 split, the 6/1 requirement/acceptance arithmetic, R-73's `02` mechanism, and the workspace facts (`tests/` three modules, `src/`/`configs/` absent).** Re-spot-checked; none of the underlying artifact text in these sections changed between iterations, and the workspace facts checked directly against the filesystem still hold exactly as iteration 1 recorded them.
- **A fresh defect from the correction pass itself.** Compared the "Documented QC" box and the "Citation corrected" notes word-for-word across all three files where each appears (`business-logic-model.md`, `business-rules.md`, `domain-entities.md`); found no divergence, no duplicated paragraph, and no heading left orphaned by the edit.

### Summary

Both iteration-1 findings resolve correctly on independent verification, not merely on trust in the correction pass. The Critical cross-reference now points at `governance-guards` R-20, and reading both candidate rules directly confirms that is the right unit and the right rule — R-20's own boxed open question is worded almost identically to the question this unit inherits for D-17, while `inventory-and-registry` R-49 (my own iteration-1 recommendation) turns out to carry a different, unrelated point; had the correction gone the way I recommended, it would have traded one broken reference for a plausible-looking wrong one. The Major "Documented QC" gap is now an honest, bounded disclosure: three of four permitted transformations remain fully specified, the fourth is named as unspecified with a concrete fix (a governed named list in `configs/data.yaml`), the fix is attributed to the correct authority (`component-methods.md` § Depth), the list's membership is explicitly not invented and is raised at the gate, and two new negative-control cases make the interim state testable rather than merely asserted. This is consistent with the project's own accepted pattern for authority-owned open items elsewhere in the same design (the R-20 authority question itself, the `02` ordinal collision) and with `project.md` § Forbidden's bar on filling a TBD value by convenience. The single residual issue — four stale "`inventory-and-registry` R-20" citations remaining in `functional-design-questions.md` because that file's receipt is locked pending a redo jump — is a known, deliberate deferral rather than an undiscovered defect, and does not appear in any of the three artifacts that carry this stage's actual design authority. No fresh defect from the correction pass itself was found: the added boxes and correction notes are word-for-word consistent across all three files where each appears, with no duplication, no orphaned heading, and no box contradicting its surrounding body. The design is implementable as stated, with its remaining open points (the D-17 authority-source question, the QC-list membership, the `02` ordinal collision) correctly carried to the gate rather than resolved by invention.
