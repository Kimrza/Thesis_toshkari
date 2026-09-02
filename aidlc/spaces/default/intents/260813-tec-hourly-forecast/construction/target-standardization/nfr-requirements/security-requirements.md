# Security Requirements — `target-standardization`

**Unit** `target-standardization` (Bolt 6) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NOTHING HERE IS CLAIMED SATISFIED — AND ONE CRITERION IS BLOCKED
>
> **FR-P1-03-1's closed-set criterion is BLOCKED on a freeze-gate decision.** *"Only the
> documented transformations"* cannot be checked until the **QC operation list** is frozen
> under a **D-number** (§ SEC-T-01). This is stated as a blocker, not a risk.
>
> **The `02` ordinal collision is a recorded §12 defect, not a resolved one**, and
> `code-generation` **must not invent a `02a`/`02b` convention**.
>
> **G-09 is signed (D-31) with its own preconditions UNMET**; **stage 3.1 remains FAIL**. No
> Python interpreter exists in this environment, so every test is **written-but-unexecuted**
> or unwritten; `configs/` does not exist.
>
> No scientific value is decided here, and TE §18.2's absolute rule stands.

## Sources

- `../functional-design/business-rules.md` — **R-64** (exactly four transformations, and a fifth is a failure), **R-65** (the aggregation statistic resolves to **D-16**, never to a default), **R-66** (the target row carries exactly **D-17's sixteen fields**), **R-67** (the excluded set is asserted, and never substituted), **R-68** (the support thresholds are **D-19's**, and they carry their basis), **R-69** (the label and the lineage caveat both travel with the product), **R-70** (**three definition IDs** on every artifact), **R-71** (data quality: four contents, and *"unexplained"* is doing the work), **R-72** (the uncertainty budget states its bounds rather than truncating), **R-73** (one `02` script per run, selected by `--phase`).
- `../functional-design/business-logic-model.md` — **W-1** (standardizing the Phase 1 hourly target), **W-2** (proving *"only the documented transformations"*, and the **"documented QC" gap**), **W-3** (the D-17 field contract and its schema test), **W-4** (what Phase 1 actually runs), **W-5** (labelling, and the **two mismatch disclosures**), **W-6** (the `02` ordinal collision), **W-7** (the target uncertainty budget, and what this unit does **not** own), **W-8** (the §12 module count), **W-9** (what Bolt 6 builds and what it must not).
- `../../external-products/nfr-requirements/security-requirements.md` — **§ SEC-E-01**, whose half-contract framing this unit's § SEC-T-02 follows.
- `../../../inception/requirements-analysis/requirements.md` — **FR-P1-03-1**, **FR-P1-03-2**, **FR-P1-03-3**, **FR-P1-03-4**, **FR-P1-03-5**, **NFR-TDEF-01**, **NFR-DQ-01**, **NFR-LEAK-01**, **NFR-PHASE-01**.
- `../../../../../../../../PreFlight/vision_document(3)(2)(2).md` — **§6.6** (the Phase 1 prepared-target definition; the **spatial-representativeness mismatch**), **§2.2** (the phase boundary; Phase 2 as a fixed-protocol replication), **§2.5** (the claim boundary).
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§5** (the target contract), **§7.0** (the Phase 1 hard prohibition), **§12**, **§13**, **§18.2–18.3**.
- `evidence/DECISIONS.md` — **D-1** (the half-open floor cell rule), **D-16** (the aggregation statistic), **D-17** (the sixteen target fields), **D-19** (the support thresholds).
- `nfr-requirements-questions.md` — Q1 = A, Q2 = A, and the receipted Consolidated Summary Confirmation.

---

## Scope note

`produces_kinds` excludes `performance-requirements`, `scalability-requirements` and
`reliability-requirements` for a `library` unit. Assessed anyway:

| Category | Assessment for `target-standardization` | Where it lives |
|---|---|---|
| **Performance** | No latency target. The unit standardizes a bounded product — three cells, calendar 2022, hourly. No throughput constraint applies. | — |
| **Scalability** | Bounded and known. No growth projection. | — |
| **Reliability** | **Fail-closed on definition, not on availability**: a fifth transformation is a **failure**, an aggregation statistic that does not resolve to D-16 is a **failure**, a missing D-17 field is a **failure**. The unit's reliability posture is that it would rather produce nothing than produce a target whose definition is uncertain. | § SEC-T-01, § SEC-T-03 |
| **Security** | This artifact — **definitional integrity**, not access control. This unit holds no credential and reaches no restricted root. | — |
| **Observability** | The three definition IDs on every artifact, the data-quality block's four contents, and the uncertainty budget's stated bounds. | § SEC-T-03, § SEC-T-04 |

---

## SEC-T-01 — The transformation set is closed, and it cannot be closed yet

**Requirement (R-64, W-2, Q7 = D).** A value-level diff against the provider bytes shows
**only the documented transformations**, enumerated as a **closed set of exactly four**, and
a **fifth transformation is a failure** rather than something a reviewer must notice.
*"Only"* is a closed-set claim, and an open-ended diff cannot express it — it can show what
changed, not that nothing else was allowed to.

**Requirement (R-65).** The aggregation statistic cited by the run **resolves to D-16**,
never to a library or implementation default.

**The four, and the state of each:**

| # | Transformation | Specified? |
|---|---|---|
| 1 | UTC normalization | **Yes** |
| 2 | Cell selection — **D-1's floor rule, half-open** | **Yes** |
| 3 | Hourly aggregation — **D-16's median** | **Yes** |
| 4 | **"documented QC"** | ⛔ **NO — defined nowhere in scope** |

> ### ⛔ STATUS: BLOCKED — the closed-set claim cannot be checked today
>
> W-2 states it directly: with one member's content unspecified, *"an undocumented change is
> indistinguishable from a QC-attributable one — which is exactly the failure this mechanism
> was written to prevent."* **The closed set is only as closed as its weakest member.**
>
> **Requirement (Q1 = A).** The QC operations are enumerated as a **named list in
> `configs/data.yaml`**, and an operation outside that list **fails as a fifth
> transformation would**. **That list is a scientific constant**: which QC operations may
> touch the target is a choice that **changes target values**. It is therefore **frozen under
> a D-number before any implementation reads it**, and until then it stands as
> **`TBD — freeze gate`**, visible to the §18.3 zero-TBD preflight.
>
> **Consequence, stated rather than discovered at 3.5: FR-P1-03-1's criterion is blocked on
> that freeze.** TE §18.2 forbids an implementer or coding agent from filling such a value by
> convenience, and stage 3.5 must **stop and report** rather than choose a QC list.

## SEC-T-02 — The label and the lineage caveat travel as data

**Requirement (R-69, W-5, Q2 = A).** The **label** and the **lineage caveat** travel with the
product as a **field on the artifact**, alongside `target_definition_id` — not as
documentation — and **a consumer that reports a comparison without it fails**.

**The two disclosures the caveat carries.**

1. The Phase 1 target is **location-sampled gridded VTEC** (Madrigal cell). It is **never**
   labelled receiver-specific station-observed VTEC, and it carries its **own distinct
   `target_definition_id`**.
2. Part of any measured IRI or GIM difference is a **geometry and sampling artefact rather
   than skill** — Phase 1 compares a grid cell against a station-coordinate evaluation,
   Phase 2 an IPP cloud against a zenith estimate (Vision §6.6).

**Requirement.** **No claim of numerical equivalence** between the Phase 1 and Phase 2
targets is permitted. Cross-phase results test **protocol transfer across a target-domain
shift**; agreement is **not** proof that the two estimate the same physical quantity. Phase 2
is a **fixed-protocol replication on a new target lineage, not a second statistically
independent blind test**, and that must be stated at abstract level.

**Why as data rather than documentation.** Vision §6.6 makes the mismatch disclosure
mandatory, and the project has already recorded VAL-05's Phase 2 disclosure as **absent from
every stage artifact** when it was checked. A caveat that depends on each reporting unit
remembering travels less far than the number it qualifies.

**The cost, stated as a half-contract.** Every downstream consumer must handle a field it did
not ask for. **This artifact states only this unit's half** — that the field exists, what it
carries, and that reporting without it is a failure. **The consuming units owe the other
half**, and **this unit does not declare the contract satisfied from one side**. This follows
`external-products` § SEC-E-01's framing for its NFR-IRI-01 limb.

## SEC-T-03 — The target row is exactly D-17's sixteen fields, and the excluded set is asserted

**Requirement (R-66, W-3).** The target row carries **exactly D-17's sixteen fields** — not
fifteen, not seventeen — checked by a **schema test against the contract**, not by review.

**Requirement (R-70, NFR-TDEF-01).** **Three definition IDs** — `phase_id`, `source_id`,
`target_definition_id` — are stamped on **every** dataset, prediction, mask and comparison.

**Requirement (R-67).** The **excluded set is asserted, and never substituted**. A run that
finds a different excluded set than the one declared **fails**; it does not proceed on the
set it found.

**Requirement (R-68).** The support thresholds are **D-19's**, and they **carry their basis**
— frozen from measured **January–November** distributions with **December excluded by
construction**. December must not inform a threshold; the trigger is December being **seen**,
not the lock being opened.

**Requirement (R-71, NFR-DQ-01).** The data-quality block carries **four contents**, and
**"unexplained" is doing the work** — an unexplained discrepancy is recorded as unexplained
rather than attributed to the nearest plausible cause.

**Requirement (R-72).** The uncertainty budget **states its bounds rather than truncating**.
A budget that silently clips is a budget that under-reports.

## SEC-T-04 — Leakage and the phase boundary, and what this unit does not own

**Requirement (NFR-LEAK-01).** Any train-only transformation is fitted on **training
partitions only, per fold, never on the full dataset**.

**Scope, stated rather than assumed.** This unit **defines** the target and its thresholds;
it **does not fit a scaling transform**. NFR-LEAK-01's fitted-transform obligation belongs to
the feature and model units. **This artifact does not claim to satisfy it** — it states the
rule and names where it binds, which is the opposite of assuming it is met here.

**Requirement (NFR-PHASE-01, TE §7.0).** Phase 1 code paths must not import or execute
raw-processing modules, nor produce DCB/STEC/mapping/satellite/arc fields.

**Requirement (R-73, W-6).** A run contains **exactly one `02` script**, selected by
`--phase`, asserted by the clean-run contract. That makes the adopted reading **falsifiable**:
two `02` scripts executing in one run is the failure the reading assumes cannot happen, and
nothing currently detects it.

**Not asserted here, and deliberately.** That `scripts/02_build_vtec_target.py` is
**unreachable under `--phase 1`** is a **phase-boundary** question belonging to
`governance-guards` **R-23**. It is **noted for that unit rather than guarded twice** —
W-6's own words: *"two rules about one fact is how they drift apart."*

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| FR-P1-03-1 | SEC-T-01 | — | ⛔ **BLOCKED** — closed set unavailable until the QC list is frozen |
| FR-P1-03-2 | SEC-T-04 | TA-27 | `Pending` — row owned by `governance-guards` |
| **FR-P1-03-3** | SEC-T-03 | TA-15 | `Pending` — **row owned elsewhere; TA-15 NOT covered** |
| **FR-P1-03-4** | SEC-T-02 | TA-15 | `Pending` — **row owned elsewhere; TA-15 NOT covered** |
| FR-P1-03-5 | SEC-T-03 | — | `Pending` |
| NFR-TDEF-01 | SEC-T-02, SEC-T-03 | — | `Pending` |
| NFR-DQ-01 | SEC-T-03 | — | `Pending` |
| NFR-LEAK-01 | SEC-T-04 | TA-11 | `Pending` — **binds elsewhere**, not claimed here |
| NFR-PHASE-01 | SEC-T-04 | TA-27 | `Pending` — row owned by `governance-guards` |

**Derived and printed**: 4 requirement sections (SEC-T-01…SEC-T-04); **9** coverage rows *(corrected 2026-08-31 on adversarial finding 1, Major; superseded figure preserved: **7**. **FR-P1-03-3** — the three-ID stamping — and **FR-P1-03-4** — the labelling rule — were implemented at SEC-T-03 and SEC-T-02 and cited nowhere. Both are testable requirements of the FR-P1-03 family this unit is chartered against, and both are implemented near-verbatim by R-70 and R-69; their acceptance row TA-15 is owned elsewhere, exactly as FR-P1-03-2's TA-27 is, which the table already lists on that basis.)*;
**0** rows claimed satisfied; **1** requirement recorded as **BLOCKED**; **1** requirement
(NFR-LEAK-01) explicitly stated as **binding elsewhere** rather than met here.

## Assumptions & Open Questions

- **[Q1]** The QC operation list is a **scientific constant**, `TBD — freeze gate`, owed a **D-number**. **FR-P1-03-1's closed-set criterion is blocked until it is frozen**, and stage 3.5 must **stop and report** rather than choose one.
- **[assumption]** Enumerating QC operations is sufficient to close the set. It closes the set **by name**; whether a listed operation's *parameters* also change values is a second question the D-number decision should settle at the same time. **Raised, not resolved** — this artifact does not split "which operations" from "with what parameters", because an operation admitted to the list is admitted to changing values.
- **[Q2]** The caveat field is **one half of a cross-unit contract**. The consuming units owe the other half — where the field is read and what failing to carry it raises. **Not stated by them yet**, and **not claimed satisfied here**.
- **[assumption]** A consumer can be made to fail for omitting the caveat. That requires the reporting path to check for it, which is **the consuming unit's code**, not this unit's — so the enforcement point named in SEC-T-02 exists only once that half lands.
- **Carried, not resolved — the `02` ordinal collision** is a recorded §12 defect. `code-generation` **must not invent a `02a`/`02b` convention**, and the reachability question belongs to `governance-guards` R-23.
- **Carried — the uncertainty budget's other half.** W-7 records what this unit does **not** own; nothing here claims the budget complete.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-31T17:28:50Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `security-requirements.md` § Sources, Requirement coverage; `tech-stack-decisions.md` § Sources, Requirement coverage | `requirements.md` L358–363 defines **FR-P1-03-3** ("stamped with `phase_id`, `source_id`, `target_definition_id`… Test TA-15") and **FR-P1-03-4** ("labelled location-sampled gridded VTEC, never receiver-specific… Test TA-15") as distinct, testable requirements in the same FR-P1-03 family this unit is chartered to cover (crosswalk L912: "FR-P1-03-1…5" share TA-04/TA-15/TA-27). This artifact's own cited rules substantively implement both: `business-rules.md` **R-70** ("three definition IDs on every artifact") is FR-P1-03-3 verbatim, and **R-69** ("the label and the lineage caveat both travel with the product") is FR-P1-03-4 verbatim — both rules are cited in Sources and their content appears in § SEC-T-02/SEC-T-03 (`tech-stack-decisions.md` § TS-T-02/TS-T-03). Yet neither FR-P1-03-3 nor FR-P1-03-4 appears anywhere in either artifact's Sources list or Requirement coverage table — only their NFR counterpart (`NFR-TDEF-01`) is cited for the definition-ID limb, and the labelling limb is cited to no FR ID at all. This breaks the pattern the coverage tables themselves establish: `FR-P1-03-2` is listed even though its acceptance row (TA-27) is "owned by `governance-guards`" — the same treatment FR-P1-03-3/-4 should have received (their acceptance row, TA-15, is likewise owned elsewhere) but did not. The derived-and-printed counts ("7 coverage rows" here, "4" in `tech-stack-decisions.md`) are therefore undercounts of this unit's own scope by the artifacts' own citation pattern, and a reader cannot verify from either coverage table that FR-P1-03-3/FR-P1-03-4 are addressed by this unit at all. | Add FR-P1-03-3 and FR-P1-03-4 as coverage rows in both artifacts (pointing to SEC-T-02/SEC-T-03 and TS-T-02/TS-T-03 respectively, acceptance row TA-15, status `Pending`), and re-derive/re-print both "Derived and printed" counts. |

### Validation Tool Results

No stage-listed validation tool was found on the `nfr-requirements` stage definition (`.claude/aidlc-common/stages/construction/nfr-requirements.md`); this pass is grounded entirely in manual cross-reference against `requirements.md`, `business-rules.md`, and the stage's own `produces_kinds` gate.

### Coverage limits (8-call budget)

Verified directly: stage frontmatter's `produces_kinds` gate (confirms `performance-requirements`/`scalability-requirements`/`reliability-requirements` correctly excluded for this `kind: library` unit, matching both artifacts' own "Scope note" / banner text); the BLOCKED claim's presence in banner, coverage table and rule body of both artifacts (present in all three — no partial-reach defect this time); the QC-list scientific-constant reasoning (defensible — an operation admitted to the list is admitted to changing target values, consistent with TC-03e's treatment of comparable forbidden-choice items); the SEC-T-02/TS-T-03 caveat half-contract framing (stated plainly as one half, not declared satisfied, consuming-unit obligation named; the Parquet-metadata-drop risk is stated in TS-T-03's own body, not only in Assumptions); the `02` ordinal-collision handling (recorded as defect, not resolved, `02a`/`02b` explicitly forbidden, reachability correctly left to `governance-guards` R-23 rather than double-guarded); and all six printed counts (4 sections/7 rows/1 BLOCKED in `security-requirements.md`; 5 sections/4 rows/2 unset values/0 new dependencies in `tech-stack-decisions.md` — all re-derived and matched). Not independently re-verified within budget: the exact wording of `business-logic-model.md` W-1…W-9 beyond what Sources quote; `foundation`'s tech-stack-decisions.md content (referenced, not read, per the library-unit's own "referenced, not restated" framing — permissible since it is this unit's declared upstream, not a sibling unit).

### Summary

One Major finding: two FR-family requirements this unit's own business rules implement (FR-P1-03-3, FR-P1-03-4) are missing from both artifacts' requirement-coverage tables and Sources, against the citation pattern the tables themselves establish for sibling requirement FR-P1-03-2. Everything else probed under the dispatch's six focus areas — the BLOCKED claim's honesty in both directions, the QC-list scientific-constant classification, the caveat half-contract, the no-satisfaction-claims posture, the `02`-collision handling, and all six printed counts — held up under adversarial re-derivation. One Major, zero Critical: below the >2-Major NOT-READY threshold.

READY

## Review — 2026-09-01 confirming pass

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 2 (fresh budget after human gate rejection; artifacts unchanged since the 2026-08-31 READY above — confirming pass, not a re-review of new content)

### Prior finding status

| # | Severity | Finding | Status |
|---|---|---|---|
| 1 | Major | FR-P1-03-3/FR-P1-03-4 missing from coverage tables/Sources in both artifacts | **Resolved** — both IDs now appear in `security-requirements.md`'s Requirement coverage table (rows for FR-P1-03-3, TS-T-03/SEC-T-02/SEC-T-03, TA-15, "row owned elsewhere") and in `tech-stack-decisions.md`'s table (same treatment), each with the count line marked "corrected 2026-08-31 on adversarial finding 1, Major" and the superseded figure preserved rather than silently overwritten (9 vs. superseded 7 here; 6 vs. superseded 4 in `tech-stack-decisions.md`), consistent with `project.md`'s never-silently-overwrite-a-count practice.

### Coverage-completeness sweep (this pass's primary check, per dispatch)

- All five `FR-P1-03-*` IDs (`-1` through `-5`) appear in this artifact's Requirement coverage table; all five also appear in `tech-stack-decisions.md`'s. No gap in the range.
- Of the eleven listed project NFR IDs, this artifact cites and rows `NFR-TDEF-01`, `NFR-DQ-01`, `NFR-LEAK-01`, `NFR-PHASE-01` — confirmed present, contrary to the dispatch's flagged risk that `NFR-TDEF-01`/`NFR-DQ-01` were the likely misses; both are already rowed (SEC-T-02/SEC-T-03 and SEC-T-03 respectively). `tech-stack-decisions.md` rows only `NFR-TDEF-01` and states explicitly, as a printed derivation rather than a silent gap, that `NFR-DQ-01`, `NFR-LEAK-01` and `NFR-PHASE-01` are excluded because they "raise no technology choice" — this satisfies `project.md`'s deliberate-exclusion-must-be-stated rule rather than violating it.
- No acceptance row is truncated to a first row where a requirement has two: FR-P1-03-3 and FR-P1-03-4 both cite TA-15 once each (their only acceptance row per the Sources crosswalk), and FR-P1-03-2/NFR-PHASE-01 both cite TA-27 consistently across both tables.
- Blank acceptance-row cells (FR-P1-03-1, FR-P1-03-5, NFR-TDEF-01, NFR-DQ-01 in `security-requirements.md`) are consistent with those requirements having no dedicated acceptance row in the FR-P1-03/NFR crosswalk this artifact cites — not contradicted by anything read this pass.
- Counts re-derived by inspection against the tables themselves: `security-requirements.md` — 4 sections, 9 rows, 1 BLOCKED, 0 satisfied — match the printed line. `tech-stack-decisions.md` — 5 sections, 6 rows, 0 satisfied, 0 new dependencies, 2 unset values — match the printed line. No stale dependent phrase ("N fewer than M") found miscounted: "three fewer than `security-requirements.md`'s nine" (9 − 6 = 3) checks out arithmetically against the corrected figures on both sides.

### Other dispatch checks

- Q1/Q2 answers carried faithfully: QC operation list stated as a scientific constant, `TBD — freeze gate`, owed a D-number, never filled by convenience (§ SEC-T-01/TS-T-01). Caveat travels as a machine-carried field alongside `target_definition_id`, not as prose (§ SEC-T-02/TS-T-03).
- FR-P1-03-1's closed-set criterion recorded as **BLOCKED** in the banner, the rule body, and the coverage table of both artifacts — not softened.
- No station-observed-VTEC mislabeling found; the location-sampled gridded VTEC / distinct `target_definition_id` framing is intact, and "no claim of numerical equivalence between the Phase 1 and Phase 2 targets is permitted" is stated explicitly (§ SEC-T-02).
- Three-ID stamping (`phase_id`, `source_id`, `target_definition_id`) is required on every dataset/prediction/mask/comparison (R-70, § SEC-T-02/T-03).
- No mechanism overstated outside its claim point: the Parquet-metadata-drop risk to the caveat's enforceability is stated in TS-T-03's own body, not relegated to Assumptions.
- Not-yet-discharged items (G-09 preconditions unmet, stage 3.1 FAIL, absent `configs/`, no Python interpreter, unexecuted/unwritten tests) remain stated as such in the banner of both artifacts; nothing here re-labels any of them as newly discharged.

### Summary

No new findings. The single Major finding from the 2026-08-31 pass was substantively resolved in place (coverage rows added, counts corrected with the superseded figure preserved rather than erased), and this pass's targeted re-sweep of the full `FR-P1-03-*` range and the eleven NFR IDs found no further gap, truncated acceptance-row list, or unstated exclusion. Confirming READY.

READY
