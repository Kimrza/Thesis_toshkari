# Domain Entities — `target-standardization`

**Unit** `target-standardization` (Bolt 6) · **Kind** `library` · **Depends on**
`inventory-and-registry`

> **Corrected and re-established 2026-08-23**, after two adversarial passes: the R-20
> citations repointed to **`governance-guards`**, and **"documented QC"** disclosed as
> undefined upstream, with the closed-set check stated as *"specified but not yet
> satisfiable"* until the QC list is fixed. A fifth redo then swept the same citations out of
> this unit's question file. **No answer to any question changed.**

The data shapes this unit owns: the **D-17 target row** in its sixteen-field entirety, the
support thresholds that decide `target_valid`, the transformation ledger that makes
"only the documented transformations" checkable, the Phase 1 uncertainty budget, and the
coverage report keyed to reconcile with the G-P1A record.

**Nothing here is a scientific value.** These shapes *carry* governed values — D-16's
aggregation statistic, D-1's cell rule, D-17's field contract, D-19's four thresholds — and
record what is and is not derivable from the product that exists.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 5 — the `Owns` list, the boundary, the 6 requirements, the implementation notes; **BLK-05** with its four-limb table.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2, § Per-unit coverage summary, § Cross-unit responsibilities. **Derived by reading the rows:** 6 requirements, **1** with no acceptance row; **owns** TA-19 (production half); **supports** TA-15.
- `../../../inception/requirements-analysis/requirements.md` — FR-P1-03-1…-5; NFR-TDEF-01; NFR-DQ-01; FR-P1-05-10; § Known defects rows 10 and 11.
- `../../../inception/application-design/components.md` — `prepared.py`'s row; § Assumptions on the `02` collision.
- `../../../inception/application-design/component-methods.md` § Depth — cross-package boundary calls only.
- `../../../inception/application-design/services.md` § The nine stage scripts, § Stage entry contract.
- `../inventory-and-registry/functional-design/domain-entities.md` — `Station`, `PreparedSchema`, the G-P1A record's keying.
- `../governance-guards/functional-design/business-rules.md` — **R-20**, which carries the open authority question § 5 inherits.
- `../governance-guards/functional-design/domain-entities.md` — the produced-field limb this unit's excluded set is checked against independently.
- `evidence/DECISIONS.md` — **D-1**, **D-16**, **D-17**, **D-19**.
- Workspace inspection, 2026-08-23: `tests/` holds three modules, none this unit's; `src/` and `configs/` absent.
- `functional-design-questions.md` (**Q1 through Q9**), `business-logic-model.md`, `business-rules.md`.

---

## Entity map

```mermaid
graph TD
  PF["provider files<br/>(5 columns)"]
  TL["TransformationLedger<br/>(exactly 4 permitted)"]
  TR["TargetRow<br/>(D-17: 16 fields)"]
  ST["SupportThresholds<br/>(D-19: 4 frozen values)"]
  TV["target_valid"]
  UB["UncertaintyBudget<br/>(2 of 6 + asymmetry)"]
  CR["CoverageReport<br/>(cell + month keyed)"]
  SC["SchemaCheck<br/>(config == D-17, then row)"]
  EX["ExcludedFieldSet<br/>(never substituted)"]

  PF --> TL --> TR
  ST --> TV --> TR
  TR --> SC
  EX --> SC
  TR --> UB
  TR --> CR
  CR -.->|"same cell+month keys"| GP["G-P1A record<br/>(inventory-and-registry)"]
```

Text fallback: provider files pass through exactly four permitted transformations into the
D-17 target row; the four frozen support thresholds decide `target_valid`; the schema check
asserts the config field set equals D-17 before checking any row, against both the required
and the excluded sets; the row feeds the uncertainty budget and the coverage report, and the
coverage report is keyed to reconcile with `inventory-and-registry`'s G-P1A record.

---

## 1. `TargetRow` — D-17's sixteen fields, and the set that is never substituted

**Sixteen fields**, counted from D-17's enumeration and matching BLK-05's own *"exactly
D-17's approved 16 fields"*:

| # | Field | Meaning |
|---|---|---|
| 1 | `interval_start_utc` | The UTC hour the row aggregates |
| 2 | `station_id` | ARUC / BSHM / NICO |
| 3 | `cell_gdlat` | The frozen cell's latitude index (D-1) |
| 4 | `cell_glon` | The frozen cell's longitude index (D-1) |
| 5 | `cell_lat_bounds` | Half-open `[floor, floor+1)` (D-1) |
| 6 | `cell_lon_bounds` | Half-open `[floor, floor+1)` (D-1) |
| 7 | `vtec_tecu` | **The median** of valid provider samples in the hour (**D-16**) |
| 8 | `valid_observation_count` | Support count; threshold **3** (D-19) |
| 9 | `within_hour_spread_tecu` | **Range (max − min)**; threshold **10.0 TECU** (D-19) |
| 10 | `largest_internal_gap_s` | Maximum **1800 s** (D-19) |
| 11 | `provider_dtec_summary` | **Median of `dtec`**; flag at **1.5 TECU** (D-19) |
| 12 | `aggregation_config_id` | Which config produced the aggregation |
| 13 | `target_valid` | Whether the row clears § 2's thresholds |
| 14 | `phase_id` | FR-P1-03-3 |
| 15 | `source_id` | FR-P1-03-3 |
| 16 | `target_definition_id` | FR-P1-03-3; the label's machine-readable half |

**Defined from the product that exists**, not from TE §6.1's Phase 2-shaped list.

**`processor_qc_flags` carries aggregation flags only.** The package, DCB, arc, elevation,
slip and mapping classes are **Phase 2 and recorded not-applicable rather than emitted
empty**.

## 2. `ExcludedFieldSet` — the half that catches a Phase 2 quantity

**Never present, and never substituted**: `valid_satellite_count`; any per-satellite or
per-IPP quantity; zenith angle or weight; elevation; DCB; STEC; mapping output; arc or slip
statistics.

**The reason is measured, not stylistic.** *"None is derivable from a five-column gridded
product"* — `ut1_unix`, `gdlat`, `glon`, `tec`, `dtec` — **audited 2026-08-21 across all
twelve request manifests**.

**Why this set is asserted and not merely the required one.** BLK-05's approved acceptance
behaviour names **both** failure modes — an **excluded or additional** field fails, and a
**missing required** field fails. A required-only check catches the second and misses the
first, and **the first is where a Phase 2 quantity would appear**.

**`governance-guards` R-23's produced-field limb guards the same boundary independently.**
Two checks on that boundary is the design's intent: one asks *is this row D-17-shaped*, the
other asks *has Phase 1 emitted a forbidden class*. Neither substitutes for the other.

## 3. `SupportThresholds` — D-19's four frozen values, with their measured basis

Frozen **2026-08-21** from measured January–November distributions, **December excluded by
construction**:

| Field | Statistic | Threshold | Measured basis |
|---|---|---|---|
| `valid_observation_count` | minimum | **3** | keeps **95.24%** of 23,709 deduplicated cell-hours |
| `within_hour_spread_tecu` | **range (max − min)** | **10.0 TECU** | p99 = **9.616** |
| `largest_internal_gap_s` | maximum | **1800 s** | keeps **93.39%**; median gap 300 s confirms the 5-minute cadence |
| `provider_dtec_summary` | **median of `dtec`** | **1.5 TECU** flag | p99 = **1.314** |

**Each carries its measured basis into `configs/data.yaml`.** A threshold without its basis
is indistinguishable from a chosen one — which matters here specifically, because a
superseded value in the governing document looks equally authoritative until you know why it
was superseded.

> **TE §6.1's provisional `valid_observation_count >= 20` is SUPERSEDED for Phase 1, and the
> reason is a measured fact:** it retains **zero** cell-hours. The deduplicated maximum is
> **12**, the product's native cadence being 5-minutely. Recorded because a superseded
> threshold still written in the source will be found by someone, and *"superseded"* without
> a reason invites reinstatement.
>
> **`valid_satellite_count`'s provisional minimum of 4 is NOT APPLICABLE in Phase 1**, rather
> than open — the field is in § 2's excluded set.

> ## ⚠ A DECISION MADE, NEVER A CHECK PASSED
>
> These four values *"move into `configs/data.yaml` carrying that provenance when the
> REQ-ENG scaffold is built."* **`configs/` does not exist**, so the **zero-TBD preflight
> (REQ-ENG-2, FR-WS-7) is not yet runnable on this component.** The requirement states it in
> its own words: *"until then this row claims a decision made, never a check passed."*
>
> Four frozen values with provenance look like a component that has passed its gate. It has
> not.

## 4. `TransformationLedger` — what makes "only" checkable

The **four permitted transformations**, enumerated (FR-P1-03-1): **documented QC**, **UTC
normalization**, **cell selection** (D-1), **the hourly aggregation** (**D-16**: the median
of valid provider VTEC samples inside the UTC hour for the station's frozen cell).

**A fifth transformation is a failure.** *"Only the documented transformations"* is a
closed-set claim, and an open-ended value diff cannot express it — it can show what changed,
not that nothing else was permitted to. The ledger is what turns *only* into a check.

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


**The statistic resolves from config citing D-16, and a run cannot proceed on a default.**
FR-P1-03-1's second limb requires the statistic to *"resolve to D-16 rather than to a
default"*; a run that merely **records** which statistic it used satisfies the words and not
the purpose.

> **Zenith-weighted aggregation: DEFERRED as not computable. Nothing is substituted.** The
> product has **no elevation, zenith angle or satellite identifier**. TE §18.2 lists the
> aggregation statistic as a **Student + Supervisor forbidden choice**, exercised under the
> recorded authority delegation. **A later implementer with a richer product may not
> reinstate it as an improvement.**

> **From the requirement's own history, carried because the ordering is the lesson.** An
> earlier revision *"asserted 'the frozen hourly aggregation' when no decision had frozen it;
> that false statement was corrected first, and the freeze recorded second, as two explicit
> stages."* A claim of frozen-ness is not the freeze.

## 5. `SchemaCheck` — three ordered steps, two distinguishable failures

1. Read the sixteen-field set from **`configs/data.yaml`**, alongside the prepared-product
   schema `inventory-and-registry` **R-49** already puts there.
2. **Assert the config set equals D-17** — before any row is compared.
3. Check the row: all sixteen required present, **and** every § 2 excluded field absent.

**Why step 2 exists.** A config-sourced field list can drift from the decision that froze it,
and then **every row passes against the wrong contract** — config and artifact agreeing
while both drift from the authority. Step 2 also makes the two failures say which layer
broke: a config drift and a row defect are different problems.

> **Open, and inherited rather than re-solved:** where step 2 reads D-17 **from**. This is the
> same authority question **`governance-guards` R-20** carries for D-24 — asserting against
> config alone lets config and manifest agree while both drift. **No third option is invented
> here.** **Citation corrected 2026-08-23** from *"`inventory-and-registry` R-20"*; that
> unit's rules run R-44…R-53 and it has no R-20.

> ## ⚠ THE MODULE THAT RUNS THIS DOES NOT EXIST
>
> `tests/test_prepared_target_schema.py` — **named and documented 2026-08-22**
> (`CR-2026-08-22-TARGET-SCHEMA-TEST`), **not implemented, never run.** *"No result of any
> kind is claimed."* Creation is gated by **G-09** and stage 3.5.
>
> **BLK-05's implementation and execution limbs stay open, and approving this design does not
> discharge them** — the symmetric statement to the register's own *"approving a filename does
> not resolve the blocker."*

## 6. `UncertaintyBudget` — two of six, plus the asymmetry statement

| Vision §6.9 content | Phase 1 |
|---|---|
| The two applicable contents | **Produced** |
| The **asymmetry statement** | **Produced** |
| Four per-satellite / per-IPP / geometry quantities | **Recorded not-applicable with their reason** — never emitted empty |

**The asymmetry statement, quoted** (FR-P1-05-10): a slowly varying per-station-day bias
partially cancels in the paired difference but *"does not cancel in the derived percentage
summary, because it inflates the reference denominator."*

**The budget asserts its own completeness against the Phase 1-applicable set.**
FR-P1-05-10's failure condition is *"a budget file that exists and states nothing"* — a
completeness assertion is what makes that a check rather than a reading.

> **§6.9's list is UNQUALIFIED in the source.** § Known defects row 11: *"§6.9 states the
> list without a phase qualifier"*, and adding one *"runs through Vision §15.2."* A reader
> who checks §6.9 finds six required items and this unit producing two; without this note
> that reads as non-compliance rather than a recorded, governed gap.

## 7. `CoverageReport` — keyed to reconcile with G-P1A

NFR-DQ-01 requires missingness and support reported **by cell and month**.

**Keyed to the same cell and month identifiers `inventory-and-registry`'s `GP1ADecisionRecord`
uses.** The two artifacts describe the same coverage from different sides, and a G-P1A
reviewer reading both must be able to line them up. **Different keying is how two reports
about one dataset become impossible to reconcile** — the shape `project.md` records for
counts compared by total rather than set-differenced.

**Also NFR-DQ-01's, and built here:** units, times, signs and fill values **documented**; and
**unexplained negative VTEC rejected**.

**"Unexplained" is doing the work.** A negative VTEC is not a small value but an
**impossible** one. An **explained** negative requires a **recorded explanation**; an
unexplained one is **rejected**, not accepted quietly.

## 8. `TargetLabel` — and the mismatch that travels with it

**Location-sampled gridded VTEC.** Never receiver-specific station-observed VTEC,
*"everywhere it is described"* (FR-P1-03-4).

**`target_definition_id` is the machine-readable half** and already travels on every row
(§ 1). **The human-readable label is emitted by the same writing path**, so an artifact
cannot be described without it — which removes the commonest cause of mislabelling, a writer
who does not know which product they have.

**The grid-cell-versus-IPP mismatch statement is emitted by the reporting path**
(NFR-TDEF-01, and `project.md` § Mandated's requirement that the spatial-representativeness
statement appear *"at the point where any IRI or GIM comparison is reported"*). A rule about
**every future report** survives only if the path that writes reports emits it —
`external-products` W-7 answers the same problem the same way.

**A grep-class check** covers the machine-readable outputs, the pattern this project uses for
SSN, residual and GRU absence.

> **⚠ Stated gap:** a **figure caption inside a notebook image** reaches none of these. That
> case stays with FR-P1-03-4's **claims-checklist review**, and saying so is the difference
> between a bounded mechanism and an overclaimed one.

## 9. `IntegrityError` subclasses raised here

Deriving from `foundation`'s base, each naming the affected resource and the violated
expectation:

| Exception | Raised when |
|---|---|
| `StandardizationError` | A fifth transformation appears in the ledger; the aggregation statistic resolves to a default rather than to D-16; a provider value is altered outside the four permitted transformations |
| `SchemaError` | The config field set does not equal D-17; a required field is missing; an **excluded** field is present |
| `TargetQualityError` | An **unexplained** negative VTEC is encountered |
| `BudgetError` | The uncertainty budget omits an applicable content, or emits a Phase 2 quantity empty rather than recording it not-applicable |
| `PhaseBoundaryError` | Raised **through** the stage entry contract's step 4, and independently by `governance-guards` R-23's produced-field limb |

Catching `foundation`'s base is what lets the stage entry contract write the `aborted`
registry row for any of them.

---

## Requirement coverage

Acceptance derived from story-map Table 1; owners from Table 2's `primary` cell, with
§ Cross-unit responsibilities consulted for the TA-19 crossing.

| Requirement | Entities | Tested by (Table 1) | Row primary owner |
|---|---|---|---|
| FR-P1-03-1 | `TransformationLedger`, `TargetRow` | TA-04 | `inventory-and-registry` |
| FR-P1-03-2 | (through the stage entry contract) | TA-27 | `governance-guards` |
| FR-P1-03-3 | `TargetRow` fields 14–16 | TA-15 | `foundation` |
| FR-P1-03-4 | `TargetLabel` | TA-15 | `foundation` |
| **FR-P1-03-5** | `TargetRow`, `ExcludedFieldSet`, `SchemaCheck` | ⚠ **NO ROW** | — |
| NFR-TDEF-01 | `TargetLabel` | TA-15 | `foundation` |
| NFR-DQ-01 | `UncertaintyBudget`, `CoverageReport` | TA-19 | **`target-standardization`** — **production half only** |

**6 requirements, 1 without an acceptance row.** **Owns** TA-19 (production); **supports**
TA-15.

> ## TA-19 HAS TWO HALVES AND THIS UNIT OWNS ONE
>
> § Cross-unit responsibilities: *"`target-standardization` (produces it)"*;
> *"`regimes-diagnostics-reporting` (reports it adjacent to the primary result)"* —
> *"Production and adjacent reporting are separate obligations in the same requirement
> family."*
>
> TA-19's evidence is *"uncertainty budget artifact **+ its placement in the results
> section**"*. **The placement half is not this unit's.**
>
> Stated because the symmetric error was made two units ago, when `external-products` claimed
> TA-36's primary test while it was sited in `features-and-splits`' module.

> **FR-P1-03-5 has no row, and the reason is legible.** WS-05 — the only field-contract row —
> is **deferred to G-P3A by FR-WS-4**. The requirement is enforced by the D-17 schema test and
> `tests/test_phase_boundary.py`; **neither is an acceptance row**, and the first **does not
> exist**. Closing it needs an approved §19 row **and** a passing result: both limbs open.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence, so `business-rules.md` opens at **R-64**. If per-unit numbering was intended, say so at the gate.
- **[assumption]** `src/data/prepared.py` is **intra-package**; `component-methods.md` § Depth names this stage as where its shape is specified. **No amendment owed**; the running total stays **five across three units**.
- **[assumption]** The §12 tree enumerates **21** test modules; `unit-of-work.md` § 5's **19** is stale — see `business-logic-model.md` § W-8.
- **[assumption]** D-17's field count is **16**, counted from its enumeration.
- **Open — BLK-05's implementation and execution limbs**, neither discharged by approving this stage.
- **Open — where the D-17 conformance check reads the frozen field set from** (§ 5), the same authority question **`governance-guards` R-20** carries for D-24. **No third option invented.** **Citation corrected 2026-08-23.**
- **Open — `unit-of-work.md` § 5's stale "19"**, reported for annotate-in-place, not edited.
- **Open — the `02` ordinal collision.** **No `02a`/`02b` convention**; the Phase-2-script reachability check is left to `governance-guards` R-23.
- **Open — Vision §6.9's list is unqualified in the source**; the phase qualifier runs through Vision §15.2.
- **Open — the zero-TBD preflight is not yet runnable**; D-19 is a decision made, not a check passed.
- **Open — the notebook-caption case reaches no machine check** and stays with the claims-checklist review.
- **Open — an obligation stated on a sibling:** § 7's cell-and-month keying must agree with `inventory-and-registry`'s G-P1A record.
- **G-09 is not signed.** No entity here authorises creating `src/data/prepared.py`, `scripts/02_standardize_prepared_target.py`, `scripts/03_verify_processing.py` or `tests/test_prepared_target_schema.py`.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.
