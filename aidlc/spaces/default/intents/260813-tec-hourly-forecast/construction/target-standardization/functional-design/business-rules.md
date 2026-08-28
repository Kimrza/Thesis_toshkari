# Business Rules — `target-standardization`

**Unit** `target-standardization` (Bolt 6) · **Kind** `library` · **Depends on**
`inventory-and-registry`

> **Re-established a sixth time 2026-08-24**, on a **new stage attempt** (Construction opened
> 2026-08-24T11:46:26Z, resetting every unit's receipt floor). **No rule of this unit
> changed.** Both `foundation` passes of that day touch nothing this unit reads — in
> particular `component-methods.md` **§ Depth**, the clause this unit depends on most, is not
> what Amendment B changed. Amendment A was declined, so **no count moved**. **The READY
> verdict in § Review belongs to the previous attempt.**

> **Corrected and re-established 2026-08-23**, after two adversarial passes. **R-66**'s
> citations repointed to **`governance-guards` R-20**; **R-64**'s closed-set claim narrowed
> once **"documented QC"** was found undefined upstream, and now states itself *"specified
> but not yet satisfiable"* until the QC list is enumerated. A fifth redo swept the same
> citations out of this unit's question file. **No rule's answer letter changed.**

The prohibitions this unit enforces, each with what it rejects, what it raises, and the
negative control that proves the rejection happens.

**This project's affirmed methodology is a negative control paired with every hard rule** —
a test that proves the violation is *caught*, not only that the happy path works. Every rule
below carries its negative control, and where no acceptance row exists to accept that
control, it says so.

**Rule IDs continue the single sequence.** `foundation` R-01…R-17, `governance-guards`
R-18…R-29, `acquisition` R-30…R-43, `inventory-and-registry` R-44…R-53 and
`external-products` R-54…R-63, so this unit opens at **R-64**. This is the numbering
assumption stated in `functional-design-questions.md`; if per-unit numbering was intended,
say so at the gate and the artifacts restart at R-01.

## Sources

- `../../../inception/requirements-analysis/requirements.md` — FR-P1-03-1…-5; NFR-TDEF-01; NFR-DQ-01; FR-P1-05-10; § Known defects rows 10 and 11.
- `../../../inception/units-generation/unit-of-work.md` § 5 — the `Owns` list, the boundary, the implementation notes; **BLK-05**'s four-limb table.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2, § Per-unit coverage summary, § Cross-unit responsibilities.
- `../../../inception/application-design/components.md` and `component-methods.md` § Depth.
- `../../../inception/application-design/services.md` § The nine stage scripts, § Stage entry contract.
- `../inventory-and-registry/functional-design/business-rules.md` — **R-45** (the registry) and **R-49** (schema against a governed schema; D-24's protected set not reopened).
- `../governance-guards/functional-design/business-rules.md` — **R-23**, **R-24**, and **R-20**, which carries the open authority question R-66 inherits: *"it must assert against the **authority**, not merely against the config."*
- `evidence/DECISIONS.md` — **D-1**, **D-16**, **D-17**, **D-19**.
- Workspace inspection, 2026-08-23: `tests/` holds three modules, none this unit's; `src/` and `configs/` absent.
- `functional-design-questions.md` (**Q1 through Q9**), `domain-entities.md`, `business-logic-model.md`.
- `governance/reviews/GOV-2026-08-28-FD-01.md` — the full-board stage-3.1 review, verdict **FAIL**; **Recommendation 18** is this unit's. *(Added 2026-08-28, re-saved under the post-remediation receipt.)*

---

## The two tiers, inherited

`foundation` R-01 fixes the hierarchy and `team.md` § Code Style fixes the posture.
**Integrity violations** terminate the run non-zero, naming the resource and the violated
expectation. **Completeness shortfalls** are non-fatal but recorded as machine-readable
fields.

**Most rules here are integrity violations**, because this unit emits the rows every
downstream unit consumes: a wrong target row is not a degraded input, it is a wrong answer
propagated. **R-71's coverage shortfalls are the exception** and sit in the second tier.

---

## R-64 — Exactly four transformations, and a fifth is a failure

**Rule (FR-P1-03-1).** Provider values are preserved. Only these are applied:

1. **Documented QC**
2. **UTC normalization**
3. **Cell selection** — `cell = (floor(lat), floor(lon))`, half-open `[floor, floor+1)`
   (D-1)
4. **The hourly aggregation** — **D-16**: the **median** of the valid provider VTEC samples
   inside the UTC hour for the station's frozen cell

**Constraint — the diff ENUMERATES the four and fails on a fifth** (Q7 = D). *"Only the
documented transformations"* is a **closed-set** claim, and an open-ended value diff cannot
express it: it shows what changed, not that nothing else was permitted. Enumerating makes a
fifth transformation a **failure** rather than something a reviewer must notice.

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


**Negative controls.** Introduce a unit conversion, a rounding or a rescale → the diff fails
on the unenumerated transformation. Alter a provider value outside the four → fails. Apply a
QC operation absent from the enumerated QC list → fails **like a fifth transformation**.
**Leave the QC list unset → the closed-set check is not satisfiable, and the run says so
rather than passing vacuously.**

**Acceptance.** TA-04 (owned by `inventory-and-registry`).

## R-65 — The aggregation statistic resolves to D-16, never to a default

**Rule (FR-P1-03-1's second limb).** The statistic is **resolved from `configs/data.yaml`
citing D-16**, and a run **cannot proceed on a default**.

**Why a refusal rather than a record.** The criterion says the statistic must *"resolve to
D-16 rather than to a default"*. A run that merely **records** which statistic it used
satisfies the words and not the purpose — a recorded default passes. Refusing to run is the
zero-TBD preflight's shape, and the same treatment `external-products` R-60 gave
FR-P1-04-18's unset interpolation rule.

**Constraint — the statistic is a §18.2 Student + Supervisor forbidden choice**, exercised
under the recorded authority delegation. **No implementer may fill it by convenience.**

> ## ⚠ ZENITH WEIGHTING IS DEFERRED AS NOT COMPUTABLE, AND NOTHING IS SUBSTITUTED
>
> The Phase 1 product carries five columns — `ut1_unix`, `gdlat`, `glon`, `tec`, `dtec` —
> with **no elevation, zenith angle or satellite identifier**. Zenith-weighted aggregation is
> *"a separately declared sensitivity, authorised only before training and only if the data
> supports it"*, and it is **deferred as not computable**.
>
> **A later implementer with a richer product may not reinstate it as an improvement.** It
> would silently change a §18.2 forbidden choice.

**A correction carried from the requirement's own history, because the ordering is the
lesson.** An earlier revision *"asserted 'the frozen hourly aggregation' when no decision had
frozen it; that false statement was corrected first, and the freeze recorded second, as two
explicit stages."* **A claim of frozen-ness is not the freeze.**

**Negative controls.** Run with no statistic configured → **refused**, not defaulted. Run
with a statistic configured but no D-16 citation → refused. Substitute a zenith-weighted
statistic → fails.

**Acceptance.** TA-04.

## R-66 — The target row carries exactly D-17's sixteen fields

**Rule (FR-P1-03-5, D-17).** Sixteen fields, no more and no fewer:
`interval_start_utc`; `station_id`; `cell_gdlat`; `cell_glon`; `cell_lat_bounds`;
`cell_lon_bounds`; `vtec_tecu`; `valid_observation_count`; `within_hour_spread_tecu`;
`largest_internal_gap_s`; `provider_dtec_summary`; `aggregation_config_id`; `target_valid`;
`phase_id`; `source_id`; `target_definition_id`.

**Constraint — the check runs in three ordered steps** (Q5 = D):

1. Read the field set from **`configs/data.yaml`**, beside the prepared-product schema
   `inventory-and-registry` **R-49** already puts there.
2. **Assert that config set equals D-17** — **before** any row is compared.
3. Check the row: all sixteen required present, **and** every excluded field absent.

**Why step 2.** A config-sourced field list can drift from the decision that froze it, and
then **every row passes against the wrong contract** — config and artifact agreeing while
both drift from the authority. Step 2 also makes a config drift and a row defect **fail
differently**, so the message says which layer broke.

> **Open, and inherited rather than re-solved:** where step 2 reads D-17 **from**. The same
> authority question **`governance-guards` R-20** carries for D-24, stated there exactly:
> *"it must assert against the **authority**, not merely against the config — otherwise
> config and manifest can agree with each other while both drift."* **No third option is
> invented here**; carried to the gate.
>
> **Citation corrected 2026-08-23.** The first issue read *"`inventory-and-registry` R-20"*.
> That unit's rules run **R-44…R-53** and it has no R-20; by this artifact set's own stated
> numbering scheme R-20 falls in `governance-guards`' range, so the citation contradicted the
> numbering it asserts. `inventory-and-registry` **R-49** carries a related but distinct
> point — that D-24's protected set is not reopened.

**Negative controls.** A row missing any of the sixteen → fails. A row carrying an
additional field → fails. A config set differing from D-17 by one field → **step 2 fails
before any row is read**.

**Acceptance.** ⚠ **NO ROW** — see § FR-P1-03-5.

## R-67 — The excluded set is asserted, and never substituted

**Rule (FR-P1-03-5).** **Never present, and never substituted**: `valid_satellite_count`;
any per-satellite or per-IPP quantity; zenith angle or weight; elevation; DCB; STEC; mapping
output; arc or slip statistics.

**The reason is measured.** *"None is derivable from a five-column gridded product"* —
audited **2026-08-21 across all twelve request manifests**.

**Constraint — `processor_qc_flags` carries aggregation flags only.** The package, DCB, arc,
elevation, slip and mapping classes are **Phase 2 and recorded not-applicable rather than
emitted empty**.

**Why the excluded set is asserted and not only the required one.** BLK-05's approved
acceptance behaviour names **both** failure modes — an **excluded or additional** field
fails, and a **missing required** field fails. A required-only check catches the second and
misses the first, and **the first is where a Phase 2 quantity would appear**.

**Constraint — this is a second, independent check on a boundary `governance-guards` also
guards.** R-23's produced-field limb asks *has Phase 1 emitted a forbidden class*; this asks
*is this row D-17-shaped*. **Neither substitutes for the other**, and the duplication is the
design's intent rather than an oversight.

**Negative controls.** Add `valid_satellite_count` to a row → fails here **and** at R-23.
Add a zenith weight → fails. Emit a Phase 2 QC class as an empty field rather than recording
it not-applicable → fails.

**Acceptance.** ⚠ **NO ROW.**

## R-68 — The support thresholds are D-19's, and they carry their basis

**Rule (D-19, frozen 2026-08-21** from measured January–November distributions, December
excluded by construction**).**

| Field | Statistic | Threshold | Measured basis |
|---|---|---|---|
| `valid_observation_count` | minimum | **3** | keeps **95.24%** of 23,709 deduplicated cell-hours |
| `within_hour_spread_tecu` | **range (max − min)** | **10.0 TECU** | p99 = **9.616** |
| `largest_internal_gap_s` | maximum | **1800 s** | keeps **93.39%**; median gap 300 s |
| `provider_dtec_summary` | **median of `dtec`** | **1.5 TECU** flag | p99 = **1.314** |

**Constraint — each value carries its measured basis into config.** A threshold without its
basis is indistinguishable from a chosen one.

> **TE §6.1's provisional `valid_observation_count >= 20` is SUPERSEDED for Phase 1, and the
> reason is measured:** it retains **zero** cell-hours. The deduplicated maximum is **12**,
> the native cadence being 5-minutely. Recorded because a superseded threshold still written
> in the governing document **will be found by someone**, and *"superseded"* without a reason
> invites reinstatement.
>
> **`valid_satellite_count`'s provisional minimum of 4 is NOT APPLICABLE in Phase 1** rather
> than open — R-67 excludes the field.

> ## ⚠ A DECISION MADE, NEVER A CHECK PASSED
>
> **`configs/` does not exist**, so the **zero-TBD preflight (REQ-ENG-2, FR-WS-7) is not yet
> runnable on this component.** The requirement says it in its own words: *"until then this
> row claims a decision made, never a check passed."* Four frozen values with provenance look
> like a component that has passed its gate. **It has not.**

**Negative controls.** A cell-hour below any threshold → `target_valid` is false, and the
reason is recorded. A threshold present in config without its basis → fails. Reinstate
`>= 20` → the measured-basis check shows it retains zero rows.

**Acceptance.** ⚠ **NO ROW** for FR-P1-03-5's support limb.

## R-69 — The label and the lineage caveat both travel with the product

**Rule (FR-P1-03-4, NFR-TDEF-01).** The Phase 1 target is labelled **location-sampled
gridded VTEC**, *"never receiver-specific station-observed VTEC, everywhere it is
described"*, and the **grid-cell-versus-IPP mismatch is disclosed** — on **every artifact
that describes or carries the Phase 1 target**, not only where a comparison is reported.

> ## ⚠ TWO PHYSICALLY DIFFERENT MISMATCHES, SEPARATED 2026-08-28 — ONE MECHANISM WAS DISCHARGING BOTH
>
> **Corrected 2026-08-28 per `governance/reviews/GOV-2026-08-28-FD-01.md` Recommendation 18**
> (`High`, finding `TEC-06`), **owner-ruled `FAIL`.** The superseded limb 3 read: *"The
> mismatch statement is emitted by the reporting path… `project.md` § Mandated requires the
> spatial-representativeness statement 'at the point where any IRI or GIM comparison is
> reported'."* That merged two physically different mismatches into one mechanism, so a Phase
> 1 artifact carrying **no** IRI/GIM comparison disclosed the target-lineage one through **no
> mechanism at all**.
>
> | | **Comparison-geometry mismatch** | **Cross-phase target-lineage mismatch** |
> |---|---|---|
> | Required by | `project.md` § Mandated / **TEC-06**; Vision §6.6; TE §5 | `requirements.md` **NFR-TDEF-01**; Vision §6.6, §2.2 |
> | What differs | the Phase 1 **target grid cell** against the **station-coordinate evaluation** the comparator is sampled at | the Phase 1 **grid-cell target population** against the Phase 2 **IPP target population** |
> | Trigger | *"at the point where any IRI or GIM comparison is reported"* | **every artifact that describes or carries the Phase 1 target** |
> | Emitting path | the **comparison-producing** path — **not this unit's**; `evaluation-and-comparison` **R-110 limb 3** | the **target-writing** path — **this unit's** (limb 3 below) |
> | Negative control | a comparison report without the spatial-representativeness sentence → **fails** (`evaluation-and-comparison` control 25) | a target artifact written without the grid-cell-versus-IPP statement → **fails** (this rule) |
>
> **The lineage mismatch is neither of TEC-06's two limbs** — TEC-06's are grid cell versus
> station-coordinate (Phase 1) and IPP cloud versus zenith estimate (Phase 2); NFR-TDEF-01's
> is grid cell versus IPP — so routing it through the comparison path discharged it on
> comparison reports and on nothing else.
>
> **This is what `project.md` § Forbidden protects:** *"NEVER claim numerical equivalence
> between the Phase 1 and Phase 2 targets… agreement is not proof that the two estimate the
> same physical quantity."* Phase 2 compares against Phase 1's **reported December
> timestamps**, so **the moment the lineage mismatch matters most is the moment no comparison
> report is in scope.**
>
> **Q8 = D's literal reading is restored, not overridden.** Option D reads *"C, with the
> grid-cell-versus-IPP mismatch statement emitted by **the same path**"*, and the path in
> options B and C is *"the code that writes the target"*. The conflation entered through D's
> impact line, which imported § Mandated's comparison trigger. **No rule's answer letter
> changes.**
>
> **The board's option 2 was rejected on the record:** one broadened trigger stating both
> mismatches in one string closes the coverage gap while **preserving the conflation**, so a
> comparison report would carry a cross-phase caveat it does not need and a Phase-1-only table
> a comparison-geometry caveat that does not apply.

**Five limbs, and one stated gap** (Q8 = D; the mismatch limb split in two on 2026-08-28):

1. **`target_definition_id`** — the machine-readable half — is stamped on every row (R-70).
   It keeps the two target lineages distinguishable **by machine**; limbs 2 and 3 are what
   make them distinguishable **by a human reader**, which is what NFR-TDEF-01 requires.
2. **The human-readable label is emitted by the writing path**, so an artifact cannot be
   described without it. This removes the commonest cause of mislabelling: a writer who does
   not know which product they have.
3. **The grid-cell-versus-IPP lineage statement is emitted by that same writing path**,
   beside the label, so the caveat **travels with the product** and cannot be separated from
   the label it qualifies. It fires on a dataset release, a target artifact, a coverage report
   and a results table alike — **a comparison is not its trigger.** This is the
   emit-from-the-path pattern `external-products` R-60 obligation 3 uses, re-anchored to the
   path that produces **this** unit's artifact, which is the writer, because this unit
   produces no IRI/GIM comparison.
4. **TEC-06's spatial-representativeness sentence is NOT emitted here.** It stays on the
   comparison-producing path, which belongs to `evaluation-and-comparison` **R-110 limb 3**,
   in the wording the governing documents fix: *"Phase 1 compares a grid cell against a
   station-coordinate evaluation, and part of any measured difference is a geometry and
   sampling artefact rather than skill."* Recorded so the obligation is visible rather than
   guarded twice — **two rules about one fact is how they drift apart.**
5. **A grep-class check** that the prohibited phrasing does not appear in this unit's
   machine-readable outputs — the pattern used for SSN, residual and GRU absence.

> **⚠ Stated gap: a figure caption inside a notebook image reaches none of these.** That case
> stays with FR-P1-03-4's **claims-checklist review**. Saying so is the difference between a
> bounded mechanism and an overclaimed one.
>
> **Widened 2026-08-28 per Recommendation 18: that review has no destination row yet.** ⚠ **As-found, and correct when written — SUPERSEDED 2026-08-28 on the resume pass**: both rows were written into that unit that day (its `domain-entities.md` § 2 and `business-rules.md` R-126 addition 4). See § Assumptions & Open Questions for the closure and its stated bound (those artifacts carry no review receipt yet). The
> checklist is `regimes-diagnostics-reporting`'s, and its `reference` enumeration lists
> **FR-P1-05-19, FR-P1-05-20, VAL-05, TEC-06, D-8, D-7** — **no NFR-TDEF-01 row and no
> FR-P1-03-4 row.** That unit's claims-and-limitations checklist **owes both**: an
> **NFR-TDEF-01** row (the lineage statement present on every artifact that describes or
> carries the Phase 1 target) and an **FR-P1-03-4** row (the label present and the prohibited
> receiver-specific phrasing absent, everywhere the target is described). **Stated as a
> dependency on that unit, which is being remediated in parallel; not edited here.** Until
> both rows exist the notebook-caption residue is **routed but not yet landable**.

**Why not the review alone.** §16 and §19 both hold that visual inspection is insufficient,
and this rule governs artifacts nobody has written yet.

**Negative controls — one per emitting path, and they are not interchangeable.** Write a
target artifact without the label → fails. **Write a target artifact without the
grid-cell-versus-IPP lineage statement → fails, because the writing path emits it** (the
control added 2026-08-28; it is the one no mechanism carried before). Produce a comparison
report without the **spatial-representativeness** sentence → fails, because the
comparison-producing path emits it — **`evaluation-and-comparison` control 25, not this
unit's.** Emit the lineage statement **instead of** the spatial-representativeness sentence
on a comparison report, or the reverse on a target artifact → **fails**; substituting one for
the other is the defect this split repairs. Put *"station-observed VTEC"* into a
machine-readable output → the grep-class check fails.

**Acceptance.** TA-15 (owned by `foundation`).

## R-70 — Three definition IDs on every artifact

**Rule (FR-P1-03-3, NFR-TDEF-01).** Every dataset, prediction, mask and comparison carries
`phase_id`, `source_id` and `target_definition_id`.

**Constraint — no numerical equivalence may be claimed between the Phase 1 and Phase 2
targets.** Cross-phase results test **protocol transfer across a target-domain shift**;
agreement is not proof that the two estimate the same physical quantity. The three IDs are
what make the distinction machine-readable rather than a matter of prose.

**The IDs are the machine-readable half only, and NFR-TDEF-01 requires both** (stated
2026-08-28 per Recommendation 18). The **human-readable** half of the same obligation is
**R-69 limb 3**'s grid-cell-versus-IPP lineage statement, emitted by the target-writing path.
A stamped `target_definition_id` a human never reads does not disclose a mismatch; **neither
half substitutes for the other.**

**Negative controls.** Emit any of the four artifact classes missing any of the three IDs →
fails. Compare a Phase 1 and a Phase 2 artifact carrying different `target_definition_id`
values and assert numerical equivalence → fails.

**Acceptance.** TA-15.

## R-71 — Data quality: four contents, and "unexplained" is doing the work

**Rule (NFR-DQ-01).** Four contents, all built here:

| # | Content | Tier |
|---|---|---|
| 1 | Units, times, signs and fill values **documented** | Integrity |
| 2 | **Unexplained negative VTEC rejected** | Integrity |
| 3 | Missingness and support reported **by cell and month** | **Completeness** — recorded, non-fatal |
| 4 | Target uncertainty budget **produced** | Integrity |

**Content 2's operative word is "unexplained".** A negative VTEC is not a small value but an
**impossible** one. An **explained** negative requires a **recorded explanation**; an
unexplained one is **rejected**, never accepted quietly.

**Constraint — content 3 is keyed to the same cell and month identifiers
`inventory-and-registry`'s G-P1A record uses.** The two artifacts describe the same coverage
from different sides, and a G-P1A reviewer reading both must be able to line them up.
**Different keying is how two reports about one dataset become impossible to reconcile.**

**Negative controls.** Emit a negative VTEC with no recorded explanation → **rejected**.
Emit one **with** an explanation → accepted, and the explanation is recorded. Report coverage
keyed differently from the G-P1A record → the reconciliation check fails. Omit any of the
four documented items → fails.

**Acceptance.** TA-19 — **production half only**; see § TA-19.

## R-72 — The uncertainty budget states its bounds rather than truncating

**Rule (FR-P1-05-10, Vision §6.9, § Known defects row 11, Q3 = D).**

| §6.9 content | Phase 1 |
|---|---|
| The two applicable contents | **Produced** |
| The **asymmetry statement** | **Produced** |
| Four per-satellite / per-IPP / geometry quantities | **Recorded not-applicable with their reason** — never emitted empty |

**The asymmetry statement, quoted**: a slowly varying per-station-day bias partially cancels
in the paired difference but *"does not cancel in the derived percentage summary, because it
inflates the reference denominator."*

**Constraint — the budget asserts its own completeness** against the Phase 1-applicable set.
FR-P1-05-10's failure condition is *"a budget file that exists and states nothing"*, and a
completeness assertion is what turns that from a reading into a check.

> **§6.9's list is UNQUALIFIED in the source.** Row 11: *"§6.9 states the list without a
> phase qualifier"*, and adding one *"runs through Vision §15.2."* A reader who checks §6.9
> finds six required items and this unit producing two — **without this note that reads as
> non-compliance rather than a recorded, governed gap.**

**Negative controls.** Emit a budget missing an applicable content → fails. Emit a Phase 2
quantity as an empty field rather than recording it not-applicable → fails. Emit a budget
that exists and states nothing → fails on the completeness assertion.

**Acceptance.** TA-19 — production half.

## R-73 — One `02` script per run, selected by `--phase`

**Rule (Q4 = C).** The clean-run contract asserts that a run contains **exactly one** `02`
script, selected by `--phase`.

**The collision, and its status.** `scripts/02_standardize_prepared_target.py` (Phase 1,
this unit) and `scripts/02_build_vtec_target.py` (Phase 2) share the ordinal in §12's tree.
The adopted reading, quoted: *"the ordinal denotes the pipeline position and `--phase`
selects exactly one, so a clean run contains one `02` per phase."*

**Constraint — this is a recorded §12 defect, NOT a resolved one.** Both `unit-of-work.md`
§ 5 and `components.md` § Assumptions say so, and the register adds that **`code-generation`
must not invent a `02a`/`02b` convention.**

**Why the assertion.** It makes the adopted reading **falsifiable** — two `02` scripts
executing in one run is the failure the reading assumes cannot happen, and nothing currently
detects it — and it makes the `02a`/`02b` workaround visibly unnecessary, because the
ambiguity it would resolve is already resolved by `--phase`.

> **Not asserted here: that `02_build_vtec_target.py` is unreachable under `--phase 1`.**
> That script **skips step 4** and asserts `phase == 2` instead, so its reachability is a
> **phase-boundary** question belonging to `governance-guards` **R-23**. **Noted for that
> unit rather than guarded twice** — two rules about one fact is how they drift apart.

**Negative controls.** Execute both `02` scripts in one run → the clean-run assertion fails.
Rename either to `02a`/`02b` → the §12 tree conformance check fails.

**Acceptance.** ⚠ No row — a run-contract rule.

---

## BLK-05 — two limbs resolved, two open, and this stage discharges neither open one

| Limb | Status | Evidence |
|---|---|---|
| **Module naming** — `tests/test_prepared_target_schema.py` | **RESOLVED 2026-08-22** | `CR-2026-08-22-TARGET-SCHEMA-TEST` |
| **Documentation** — §12 tree entry and provenance table | **RESOLVED 2026-08-22** | The tree now enumerates **21** test modules |
| **Test implementation** | **PENDING** | **The module does not exist.** Gated by G-09 and stage 3.5 |
| **Execution evidence** | **PENDING** | **Never run.** *"No result of any kind is claimed"* |

**Approved acceptance behaviour**, fixed by the owner *"so implementation cannot narrow
it"*, and implemented by R-66 and R-67: a valid row containing exactly D-17's **16** fields
**passes**; a row containing an **excluded or additional** field **fails**; a row **missing
any required field** **fails**.

> **The register states that *"approving a filename does not resolve the blocker."* The
> symmetric statement is made here: approving this design does not resolve it either.** The
> two open limbs survive this stage's approval unchanged.
>
> **Every citation of the module in this unit's artifacts carries its non-existence.** A
> module or row cited without its status reads as coverage — the failure that let FR-P1-02-8
> sit behind a withdrawn `TA-29` for five revisions, and that had TA-36 cited without
> `Pending`.

## TA-19 — two halves, and this unit owns one

§ Cross-unit responsibilities: *"`target-standardization` (produces it)"*;
*"`regimes-diagnostics-reporting` (reports it adjacent to the primary result)"* —
*"Production and adjacent reporting are separate obligations in the same requirement
family."*

TA-19's evidence is *"uncertainty budget artifact **+ its placement in the results
section**"*. **The placement half is not this unit's.**

Stated because the symmetric error was made two units ago, when `external-products` claimed
TA-36's primary test while it was sited in `features-and-splits`' module.

## FR-P1-03-5 — the one requirement with no acceptance row

**1 of this unit's 6**, derived from story-map § Per-unit coverage summary, which reads
`target-standardization (1)`.

| Requirement | Rules | Evidence that would close it |
|---|---|---|
| **FR-P1-03-5** | R-66, R-67, R-68 | An approved §19 row asserting D-17's field contract — a valid 16-field row passes, an excluded or additional field fails, a missing required field fails — **plus a passing result** from `tests/test_prepared_target_schema.py`. **Both limbs open**: the row does not exist, and neither does the module |

> **Why it has no row today.** WS-05 — the only field-contract row — is **deferred to G-P3A
> by FR-WS-4**. FR-P1-03-5 is enforced by the D-17 schema test and
> `tests/test_phase_boundary.py`; **neither is an acceptance row**, and the first does not
> exist.
>
> **No artifact, manifest or report may state or imply that FR-P1-03-5 is covered, satisfied
> or verified.** Designing the check is not testing it, and implementing it is not a row.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence, so this unit opens at **R-64**. If per-unit numbering was intended, say so at the gate.
- **[assumption]** `src/data/prepared.py` is **intra-package**; `component-methods.md` § Depth names this stage as where its shape is specified. **No amendment owed**; the running total stays **five across three units** (`acquisition` 3, `inventory-and-registry` 1, `external-products` 1).
- **[assumption]** The §12 tree enumerates **21** test modules; `unit-of-work.md` § 5's **19** is stale, contradicted by BLK-05's own limb table in the same file and by `requirements.md` REQ-ENG-4. Reported at the gate for an annotate-in-place decision, **not edited**.
- **[assumption]** D-17's field count is **16**, counted from its enumeration and matching BLK-05's own wording.
- **Open — BLK-05's implementation and execution limbs**, neither discharged by approving this stage.
- **Open — where R-66 step 2 reads D-17 from**, the same authority question **`governance-guards` R-20** carries for D-24. **No third option invented.** **Citation corrected 2026-08-23** from *"`inventory-and-registry` R-20"*, which named a unit whose rules run R-44…R-53.
- **Open — the `02` ordinal collision** (R-73), a recorded §12 defect. **No `02a`/`02b` convention.** The Phase-2-script reachability check is left to `governance-guards` R-23.
- **Open — Vision §6.9's list is unqualified in the source** (R-72); the phase qualifier runs through Vision §15.2.
- **Open — the zero-TBD preflight is not yet runnable** (R-68); D-19 is a decision made, not a check passed.
- **Open — R-69's notebook-caption case reaches no machine check** and stays with the claims-checklist review. **Widened 2026-08-28 per Recommendation 18:** that checklist is `regimes-diagnostics-reporting`'s and carries **no NFR-TDEF-01 row and no FR-P1-03-4 row**, so the routing has **no destination**. Both rows are **owed by that unit**, remediated in parallel; **the dependency is stated, not edited here**. ⚠ **CLOSED on the 2026-08-28 resume pass.** Both rows were written into `regimes-diagnostics-reporting` that day (`domain-entities.md` § 2 and `business-rules.md` R-126 addition 4, plus its W-4 mirror): `NFR-TDEF-01` as the **cross-phase target-lineage** disclosure row, kept distinct from the TEC-06 comparison-geometry row and required on **every reported artifact describing the Phase 1 target**, not only serialized IRI/GIM comparisons; `FR-P1-03-4` as the notebook-caption row with `human_residue` recorded. The routing now has a destination. **Bound, stated rather than assumed:** those artifacts carry **no review receipt and no adversarial pass yet** — the rows exist in draft and the stage verdict is still **FAIL**, so this is a closed *dependency*, not a discharged *obligation*.
- **Open — NFR-TDEF-01 is now discharged by two obligations rather than one** (R-69, corrected 2026-08-28 per Recommendation 18): the machine-readable stamp (R-70) and the human-readable lineage statement on the target-writing path (R-69 limb 3). TEC-06's comparison-geometry sentence is **`evaluation-and-comparison` R-110 limb 3's**, recorded here so the split is legible; **no obligation is created on that unit by this stage**.
- **Open — an obligation stated on a sibling:** R-71's cell-and-month keying must agree with `inventory-and-registry`'s G-P1A record.
- **G-09 is not signed.** No rule here authorises creating `src/data/prepared.py`, `scripts/02_standardize_prepared_target.py`, `scripts/03_verify_processing.py` or `tests/test_prepared_target_schema.py`.
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

> **Re-saved unchanged 2026-08-26 under the fourteenth-redo re-confirmation receipt** (redo taken
> for `external-products`; floor reset mechanical). **No content of this unit changed.**
> **G-09 remains unsigned.**

---

> ## Remediation, 2026-08-28 — GOV-2026-08-28-FD-01 Recommendation 18
>
> **The project decision owner ruled `FAIL` on Recommendation 18** (`High`, finding `TEC-06`)
> and directed the board's **option 1 plus option 3's checklist rows**. A redo jump cleared
> the write-freeze. **Only `R-69`, one paragraph added to `R-70`, and two
> `## Assumptions & Open Questions` bullets changed in this file.** Every dated provenance box
> above is unchanged.
>
> **What changed.** NFR-TDEF-01's **cross-phase target-lineage** disclosure (grid-cell target
> population versus IPP target population) is separated from TEC-06's **comparison-geometry**
> disclosure (grid cell versus station-coordinate evaluation) and moved onto the
> **target-writing** path beside the `location-sampled gridded VTEC` label. Each statement now
> has **its own emitting path and its own negative control**: a target artifact written
> without the grid-cell-versus-IPP statement **fails** (new, R-69); a comparison report
> without the spatial-representativeness sentence **fails** (existing, and
> `evaluation-and-comparison` R-110 limb 3's, not this unit's). The two rows
> `regimes-diagnostics-reporting`'s claims-and-limitations checklist owes — **NFR-TDEF-01**
> and **FR-P1-03-4** — are recorded as a dependency; **that unit is not edited here.** The
> board's option 2 was **rejected on the record**.
>
> **What did not change.** No question, no answer letter, no rule ID, no entity, no count, no
> scientific value. **G-09 remains unsigned**; **BLK-05 stands as it is**, both open limbs
> intact; Phase 1 still produces no DCB, STEC, mapping, satellite or arc field; the gridded
> product is still never labelled a receiver-specific station observation. **D-1's cell rule,
> D-16's median and D-17's sixteen fields are applied, not reinterpreted.** The three open
> items the terminal READY carried to the gate — the **"documented QC"** enumeration's
> membership, the **D-17 conformance check's authority source** (`governance-guards` R-20),
> and the **`02` ordinal collision** — are **all still open and unresolved**, verified in
> place.
>
> **Derived counts, re-checked after the edit and unchanged:** **10** rules (`R-64`…`R-73`),
> **9** workflows (`W-1`…`W-9`), **9** numbered entity sections, **6** requirements with
> **1** (`FR-P1-03-5`) carrying no acceptance row.
