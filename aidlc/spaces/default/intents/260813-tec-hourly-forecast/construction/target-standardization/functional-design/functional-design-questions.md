# Functional Design Questions — `target-standardization`

**Unit** `target-standardization` — the Phase 1 hourly target and its verification.
**Kind** `library` · **Complexity** M · **Deployment** standalone · **Depends on**
`inventory-and-registry`.

Unit **6 of 12**, running in the same batch as `external-products` (both depend only on
`inventory-and-registry`). It owns `src/data/prepared.py`,
`scripts/02_standardize_prepared_target.py`, `scripts/03_verify_processing.py` (Phase 1
scope) and the D-17 target-schema test.

**It emits the target rows every downstream unit consumes.** Turn validated provider files
into Phase 1 hourly target rows under D-17's contract — **documented QC, UTC
normalization, cell selection and the stated hourly aggregation only, with provider values
preserved** — stamp `phase_id`, `source_id` and `target_definition_id` on every row, and
label the product **location-sampled gridded VTEC**.

**6 requirements, 1 with no §16/§19 acceptance row** — FR-P1-03-5. Derived from story-map
Table 1 and cross-checked against § Per-unit coverage summary, which reads
`target-standardization (1)` with exactly that ID. It **owns** TA-19 and **supports**
TA-15.

**BLK-05 is open on implementation, and two of its four limbs are already resolved.**
Naming (`tests/test_prepared_target_schema.py`) and documentation (the §12 tree entry) were
approved **2026-08-22** under `CR-2026-08-22-TARGET-SCHEMA-TEST`. **Test implementation**
and **execution evidence** are **PENDING**: the module does not exist and has never been
run. **No result of any kind is claimed.**

**One upstream figure is stale, and its own file contradicts it.** `unit-of-work.md` § 5
says FR-P1-03-5's criterion implies a test *"that exists in none of the **19** modules TE
§12's amended tree enumerates."* **BLK-05's own limb table in the same file says 21**, with
a derivation comment recording the history 17 → 19 → 20 → 21 and the command that produces
it. `requirements.md` REQ-ENG-4 independently reads **21**. Question 2 decides what this
stage does about that; it edits no approved artifact.

**G-09 is not signed.** `src/`, `configs/` and every module named here are absent.
`tests/` holds three modules — `test_acquisition_window.py`, `test_phase_boundary.py`,
`test_release_hashes.py` — and this unit's is not among them.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 5 — the `Owns` list, the boundary, the 6 requirements, the implementation notes; and **BLK-05** with its four-limb status table.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2 plus § Per-unit coverage summary. **Derived by reading the rows:** 6 requirements, **1** with no acceptance row (FR-P1-03-5); **owns** TA-19; **supports** TA-15. § Cross-unit responsibilities carries the NFR-DQ-01 / FR-P1-05-10 / TA-19 crossing.
- `../../../inception/requirements-analysis/requirements.md` — FR-P1-03-1, -2, -3, -4, -5; NFR-TDEF-01; NFR-DQ-01; FR-P1-05-10; § Known defects rows 10 and 11.
- `../../../inception/application-design/components.md` — `prepared.py`'s row (**Phase 1 only**; schema, cell coverage, common timestamps) and § Assumptions' record of the `02` ordinal collision.
- `../../../inception/application-design/component-methods.md` § Depth — **cross-package boundary calls only**; intra-package shapes are **this stage's** to specify.
- `../../../inception/application-design/services.md` § The nine stage scripts, § Stage entry contract.
- `../inventory-and-registry/functional-design/business-rules.md` — R-45's registry and R-49's prepared-product schema, both consumed here.
- `../governance-guards/functional-design/business-rules.md` — **R-23**, **R-24** (the phase-boundary limbs this unit must not violate).
- `evidence/DECISIONS.md` — **D-1** (cell rule), **D-16** (hourly aggregation statistic), **D-17** (the 16-field target contract), **D-19** (the four frozen support values).
- Workspace inspection, 2026-08-23: `tests/` holds three modules, none this unit's; `src/` and `configs/` absent.
- Absent by scope design: `stories` (2.4 `SKIP`), `mockups` (1.6 and 2.5 `SKIP`). `kind: library`, so `frontend-components.md` is not produced.

---

## Question 1

**BLK-05's four limbs, and what remains for this stage.**

| Limb | Status |
|---|---|
| Module naming — `tests/test_prepared_target_schema.py` | **RESOLVED 2026-08-22** |
| Documentation — §12 tree entry and provenance table | **RESOLVED 2026-08-22** |
| **Test implementation** | **PENDING** — the module does not exist; gated by G-09 and stage 3.5 |
| **Execution evidence** | **PENDING** — never run; *"No result of any kind is claimed"* |

The register is explicit that *"approving a filename does not resolve the blocker."* It also
fixes the **approved acceptance behaviour**, *"recorded so implementation cannot narrow
it"*: a valid row containing exactly D-17's approved **16** fields **passes**; a row
containing an **excluded or additional** field **fails**; a row **missing any required
field** **fails**.

What does this stage produce against BLK-05?

A) Restate the approved acceptance behaviour and stop there
   > **Impact**: Faithful to what is settled, and it invents nothing. But the register places the *design* of this test in this stage's scope, and restating three sentences leaves stage 3.5 to invent the field-set source, the comparison and the failure messages — the guessing the register's "recorded so implementation cannot narrow it" exists to prevent.

B) A, plus a full test specification — the field set's source, the exact comparison, and what each of the three failure modes reports
   > **Impact**: Gives stage 3.5 something it can implement without judgement calls, which is what a design stage owes a build stage. The three behaviours are already fixed, so specifying them adds no new decision. Costs stating where the 16-field set is read from, which Question 5 settles.

C) B, plus asserting the module **does not exist** and that no result is claimed, wherever this unit's artifacts cite it
   > **Impact**: Directly answers how FR-P1-02-8 and TA-36 went wrong elsewhere in this stage — a row or module cited without its status reads as coverage. BLK-05's own table already says it twice; carrying it into every citation is cheap and makes the omission structural rather than a matter of noticing. Costs a status label per citation.
   
D) C, plus recording that BLK-05's **implementation and execution limbs remain the blocker**, so approving this stage does not discharge it
   > **Impact**: The register says approving a filename does not resolve the blocker; the symmetric risk is that approving a *design* is read as resolving it. Stating that the two open limbs survive this stage's approval keeps the blocker where it is. Costs one sentence at the gate and one in the artifacts.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A leaves the build stage guessing at exactly the point the register wanted fixed. B is the design work owed. C adds the status discipline this stage has already been bitten by twice — FR-P1-02-8 behind a withdrawn `TA-29`, TA-36 cited without `Pending`. D closes the symmetric misreading: two limbs of this blocker are resolved and two are not, and a stage approval touches neither of the open ones.

[Answer]: D

---

## Question 2

**`unit-of-work.md` contradicts itself about the §12 test-module count, in two places about this unit.**

| Where | Says |
|---|---|
| § 5 `target-standardization` | FR-P1-03-5's test *"exists in none of the **19** modules TE §12's amended tree enumerates"* |
| **BLK-05's limb table, same file** | *"The tree now enumerates **21** test modules"* — with a comment recording 17 → 19 → 20 → 21 and the `sed`/`grep`/`wc` command that derives it |
| `requirements.md` REQ-ENG-4 | **21**, *"re-derived from that amended tree on 2026-08-22 by listing its `test_*.py` entries"* |

**Two independent sources read 21; § 5's 19 froze at the first of three same-day
amendments.** The BLK-05 comment even records that its own "20" was a fourth site missed by
a prior sweep's Rec 3 — so this is the same file's second known stale-count site.

What does this stage do?

A) Use 21 and say nothing
   > **Impact**: Correct, and it avoids adding noise. But a later reader opening § 5 sees 19 with no signal, and the likeliest repair is to assume this stage was wrong — the same trap WS-01's exception carries in `inventory-and-registry`.

B) Use 21 and note the discrepancy in passing
   > **Impact**: Cheap and prevents the misreading. But it does not say which is right or why, so a reader still has to re-derive it.

C) B, with the derivation shown and both sources named
   > **Impact**: `project.md` § Way of Working requires a count be derived and printed before being asserted. Showing the derivation makes the claim checkable rather than another asserted number in a chain that has already produced four wrong ones. Costs three lines.
   
D) C, plus reporting the stale § 5 text at the gate for an annotate-in-place decision
   > **Impact**: `CHANGE_RECORD_PROCEDURE.md` reserves approved-stage artifacts — a sweep reports, it does not edit, absent owner approval. The BLK-05 comment records that the owner **has** granted annotate-in-place before, at `GOV-2026-08-22-INC-01` Rec 7, so the route exists. Costs a gate item, and the owner may decline.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A and B both leave a reader to discover the contradiction unaided. C satisfies this project's own derive-before-asserting rule, which exists precisely because this chain of counts has been wrong four times. D adds the one thing that could actually fix the source rather than working around it — and the precedent for annotate-in-place is recorded in the very comment that documents the last such correction.

[Answer]: D

---

## Question 3

**`03_verify_processing.py`'s Phase 1 scope is thinner than §12's description implies**, and
`unit-of-work.md` § 5 states that *"`functional-design` settles exactly what it runs."*

Vision §6.9's uncertainty-budget content list has **six** items. § Known defects row 11
records that **four are per-satellite, per-IPP or geometry quantities the five-column Phase
1 product cannot yield** (`ut1_unix`, `gdlat`, `glon`, `tec`, `dtec`), and that §6.9 states
the list **without a phase qualifier**. FR-P1-05-10 requires the **two applicable** contents
plus the **asymmetry statement**, with the four recorded **not-applicable rather than
emitted empty**.

The asymmetry statement, quoted: a slowly varying per-station-day bias partially cancels in
the paired difference but *"does not cancel in the derived percentage summary, because it
inflates the reference denominator."*

What does verification run in Phase 1?

A) The two applicable contents and the asymmetry statement
   > **Impact**: Exactly FR-P1-05-10's requirement, and no more. But "a budget file that exists and states nothing fails" is that requirement's own bar, and four silently absent items look like an incomplete budget rather than a bounded one.

B) A, with the four Phase 2 items **recorded not-applicable with their reason**
   > **Impact**: What row 11 actually directs — not-applicable rather than empty — and the reason is the same measured basis D-17 used: the product has five columns and no satellite, elevation or zenith information. A reader can then tell a bounded budget from a truncated one. Costs four short entries.

C) B, plus the budget asserting its own completeness against the Phase 1-applicable set
   > **Impact**: Turns "states nothing fails" into a check rather than a reading. The same list-plus-completeness-test shape used four times already in this stage. Costs one assertion and the enumeration it ranges over.
   
D) C, plus recording that §6.9's list is **unqualified in the source** and that adding the phase qualifier runs through Vision §15.2
   > **Impact**: Row 11 states this explicitly — the defect is *"documented; the source list is unqualified as written."* A reader who checks §6.9 finds six required items and this unit producing two, and without the note that looks like non-compliance rather than a recorded, governed gap. Costs one sentence.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A is the literal minimum and reads as a truncated budget. B follows row 11's direction. C makes the boundedness checkable, which matters because FR-P1-05-10's failure condition is a budget that exists and says nothing. D adds the limb that protects the reader who goes to the source: §6.9 is unqualified as written, the amendment route is Vision §15.2, and saying so is the difference between a governed gap and an apparent breach.

[Answer]: D

---

## Question 4

**The `02` ordinal is shared.** `scripts/02_standardize_prepared_target.py` (Phase 1, this
unit) and `scripts/02_build_vtec_target.py` (Phase 2) both carry it in §12's tree.

`unit-of-work.md` § 5 records the reading adopted upstream: *"the ordinal denotes the
pipeline position and `--phase` selects exactly one, so a clean run contains one `02` per
phase."* It is equally explicit that this is **a recorded §12 defect, not a resolved one**,
and that *"`code-generation` must not invent a `02a`/`02b` convention."*

`components.md` § Assumptions carries the same: *"the collision itself is a §12 defect this
stage does not resolve."*

How does this unit's design treat the collision?

A) Follow the adopted reading and say nothing further
   > **Impact**: Consistent with two upstream artifacts, and it invents nothing. But both of them explicitly flag the collision as unresolved, and a design that reads as though it were settled removes the flag a later reader needs.

B) A, restating that the collision is a recorded §12 defect this stage does not resolve
   > **Impact**: Keeps the flag attached where the code will be written. Cheap. But it does not stop the specific thing the register warns about — an implementer inventing `02a`/`02b` to make the tree unambiguous.

C) B, plus an assertion that a clean run contains **exactly one** `02` script, selected by `--phase`
   > **Impact**: Turns the adopted reading into a check: two `02` scripts executing in one run is the failure the reading assumes cannot happen, and nothing currently detects it. It also makes the `02a`/`02b` workaround visibly unnecessary, because the ambiguity it would resolve is already resolved by `--phase`. Costs one assertion in the clean-run contract.
   
D) C, plus `02_build_vtec_target.py` being asserted **unreachable** under `--phase 1`
   > **Impact**: The Phase 2 script is the one that skips the stage entry contract's step 4 — it asserts `phase == 2` instead — so its reachability under Phase 1 is exactly a phase-boundary question, and `governance-guards` R-23's import limb already covers `src/gnss` modules but not this script. Risk: it edges into `governance-guards`' rule rather than this unit's, and duplicating a guard is how two rules about one fact appear.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A drops a flag two upstream artifacts deliberately raised. B keeps it but changes nothing. C makes the adopted reading falsifiable — one `02` per run, selected by `--phase` — which is the cheapest way to stop the collision becoming an invented convention. D's instinct is right but it reaches into `governance-guards`' phase-boundary rule; better to note the gap for that unit than to write a second guard here.

[Answer]: C

---

## Question 5

**D-17's target row carries exactly 16 fields**, defined *"from the product that exists
rather than from TE §6.1's Phase 2-shaped list"*: `interval_start_utc`; `station_id`;
`cell_gdlat`; `cell_glon`; `cell_lat_bounds`; `cell_lon_bounds`; `vtec_tecu`;
`valid_observation_count`; `within_hour_spread_tecu`; `largest_internal_gap_s`;
`provider_dtec_summary`; `aggregation_config_id`; `target_valid`; `phase_id`; `source_id`;
`target_definition_id`.

**Excluded and never substituted:** `valid_satellite_count`, any per-satellite or per-IPP
quantity, zenith angle or weight, elevation, DCB, STEC, mapping output, arc or slip
statistics — *"none is derivable from a five-column gridded product."*

`processor_qc_flags` carries **aggregation flags only**; the package, DCB, arc, elevation,
slip and mapping classes are **Phase 2 and recorded not-applicable rather than emitted
empty**.

Where does the schema test read the 16-field set from?

A) A literal in the test module
   > **Impact**: Simplest, and the set is frozen by D-17 so it will not drift on its own. But `project.md` § Forbidden bars hiding a governed constant in source, and a 16-item governed enumeration in a test body is exactly that — with no config review reaching it.

B) From `configs/data.yaml`, alongside the prepared-product schema `inventory-and-registry` R-49 already puts there
   > **Impact**: Governed, versioned, hashable, reviewed in one place, and it reuses a home this stage's sibling already established rather than inventing a second. But it makes the schema test depend on config resolution, so a config failure and a schema failure become harder to tell apart.

C) B, with the test asserting the config set **equals D-17's** before comparing any row
   > **Impact**: Closes B's real gap: a config-sourced field list can drift from the decision that froze it, and then every row passes against the wrong contract. Asserting config-against-D-17 first makes the failure say which layer broke. Costs the same authority question **`governance-guards` R-20** raises for D-24 — where the check reads the frozen decision from.
   
D) C, with the excluded set asserted explicitly too, not only the required one
   > **Impact**: D-17's contract has two halves, and the acceptance behaviour names both: an **excluded or additional** field fails, and a **missing required** field fails. A required-only assertion catches the second and not the first, and the first is where a Phase 2 quantity would appear. Costs enumerating the exclusions, which D-17 already does.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A is barred by § Forbidden. B is the right home and leaves the drift gap. C closes it and inherits the open authority question already raised at **`governance-guards` R-20** — where the check reads the frozen decision from — which is worth carrying, not re-solving. D adds the half that matters most here: the excluded set is where a satellite or IPP field would show up, and that is the exact failure `governance-guards` R-23's produced-field limb also guards. Two independent checks on that boundary is the design's intent, not duplication.

[Answer]: D

---

## Question 6

**D-19 froze four support values on 2026-08-21**, from measured January–November
distributions with December excluded by construction:

| Field | Statistic | Threshold | Measured basis |
|---|---|---|---|
| `valid_observation_count` | minimum | **3** | keeps 95.24% of 23,709 deduplicated cell-hours |
| `within_hour_spread_tecu` | **range (max − min)** | **10.0 TECU** | p99 = 9.616 |
| `largest_internal_gap_s` | maximum | **1800 s** | keeps 93.39%; median gap 300 s confirms the 5-minute cadence |
| `provider_dtec_summary` | **median of `dtec`** | **1.5 TECU** flag | p99 = 1.314 |

They *"move into `configs/data.yaml` carrying that provenance when the REQ-ENG scaffold is
built."* **`configs/` does not exist**, so the zero-TBD preflight is **not yet runnable on
this component** — the requirement is explicit that until then *"this row claims a decision
made, never a check passed."*

**TE §6.1's provisional `valid_observation_count >= 20` is superseded for Phase 1** because
it retains **zero** cell-hours: the deduplicated maximum is 12, the product's native cadence
being 5-minutely.

How does this unit's design carry D-19?

A) Cite the four values and their thresholds
   > **Impact**: Accurate and minimal. But it drops the measured basis, and a threshold without its basis is indistinguishable from a chosen one — which matters because TE §6.1's superseded value looks equally authoritative until you know it retains zero rows.

B) A, with each value carrying its **measured basis** into `configs/data.yaml`
   > **Impact**: What the requirement directs — *"carrying that provenance"* — and it lets a reviewer judge the threshold rather than accept it. Costs four provenance strings.

C) B, plus recording that the zero-TBD preflight is **not yet runnable** and that this is a decision made, not a check passed
   > **Impact**: Prevents the strongest available misreading: four frozen values with provenance look like a component that has passed its gate. The requirement says the opposite in its own words, and this stage's artifacts are where a reader would look. Costs one sentence.
   
D) C, plus recording **why** TE §6.1's `>= 20` is superseded — that it retains zero cell-hours against a deduplicated maximum of 12
   > **Impact**: A superseded threshold that is still written in the governing document will be found by someone, and "superseded" without a reason invites reinstatement. The reason is a measured fact and is short. Costs one more sentence, and it is the sentence that makes the supersession defensible rather than asserted.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A leaves four numbers unjudgeable. B carries the provenance the requirement asks for. C blocks the "frozen means passed" misreading, which this stage has already had to block twice for rows and modules. D is the cheapest defence against a superseded value being reinstated by someone reading TE §6.1 alone — and the reason is one measured sentence.

[Answer]: D

---

## Question 7

FR-P1-03-1: *"Provider values are preserved; only documented QC, UTC normalization, cell
selection and the hourly aggregation are applied."* Its criterion has **two** limbs: *"a
value-level diff against the provider bytes shows only the documented transformations,
**and** the aggregation statistic cited by the run resolves to **D-16** rather than to a
default."*

**D-16 (2026-08-21)** freezes the statistic: **the median of the valid provider VTEC samples
inside the UTC hour for the station's frozen cell.** TE §18.2 lists it as a **Student +
Supervisor forbidden choice**, exercised under the recorded authority delegation.

The requirement also records a correction worth carrying: an earlier revision *"asserted 'the
frozen hourly aggregation' when no decision had frozen it; that false statement was corrected
first, and the freeze recorded second, as two explicit stages."*

**Zenith-weighted aggregation is deferred as not computable** — the five-column product has
no elevation, zenith angle or satellite identifier — and **nothing is substituted**.

How are the two limbs proven?

A) A value-level diff, and the run recording which statistic it used
   > **Impact**: Both limbs, literally. But "recording which statistic it used" is satisfiable by a run that recorded a default, and the criterion's second limb exists precisely because a default would otherwise pass.

B) A, with the statistic **resolved from `configs/data.yaml` citing D-16**, and a run that cannot proceed on a default
   > **Impact**: Implements "resolves to D-16 rather than to a default" as a refusal rather than a record — the zero-TBD preflight's shape, and the same treatment `external-products` gave FR-P1-04-18's unset interpolation rule. Costs the config entry, which D-19's values need anyway.

C) B, plus the diff enumerating the **four permitted transformations** and failing on any fifth
   > **Impact**: "Only the documented transformations" is a closed set — QC, UTC normalization, cell selection, hourly aggregation — and an open-ended diff cannot express "only". Enumerating makes a fifth transformation a failure rather than something a reviewer must notice. Costs naming the four, which the requirement already does.
   
D) C, plus recording that **zenith weighting is deferred as not computable and nothing is substituted**
   > **Impact**: The requirement states this and gives the measured reason. Without it, a later reader with a richer product might implement zenith weighting as the "better" statistic and silently change a Student + Supervisor forbidden choice. Costs one sentence, and it names a §18.2 item that no implementer may fill.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A satisfies the words and not the second limb's purpose. B makes the default impossible rather than merely visible. C makes "only" checkable, which an unenumerated diff cannot do. D guards the §18.2 item: the statistic is a forbidden choice, zenith weighting is the tempting alternative, and the record of why it is deferred is what stops it being reinstated as an improvement.

[Answer]: D

---

## Question 8

FR-P1-03-4: the Phase 1 target is labelled **location-sampled gridded VTEC**, *"never
receiver-specific station-observed VTEC, everywhere it is described."* NFR-TDEF-01 adds that
**the grid-cell-versus-IPP mismatch is disclosed**.

Its criterion is *"a claims-checklist review over every artifact and figure caption finds no
mislabelling"* — **a review, not a test**, over artifacts and captions that mostly do not
exist yet.

`project.md` § Forbidden states the same prohibition, and `governance-guards` designs no
mechanism for it.

How is the labelling rule enforced?

A) The claims-checklist review, as the criterion states
   > **Impact**: Exactly the requirement, and it is how claims review works elsewhere in this project. But §16 and §19 both hold that visual inspection alone is insufficient, and this rule governs every future artifact and caption — a review catches what is reviewed.

B) A, plus the label emitted from the code that writes the target, so the artifact carries it
   > **Impact**: The stamped `target_definition_id` already travels with every row; carrying the human-readable label the same way means an artifact cannot be described without it. It does not stop someone writing the wrong words in prose, but it removes the commonest cause — a writer who does not know which product they have.

C) B, plus a grep-class check that the prohibited phrase does not appear in this unit's outputs
   > **Impact**: The same grep-evidence pattern this project uses for SSN, residual and GRU absence, and for `external-products`' obligation 4. Catches the phrase where it is machine-readable. Costs defining the prohibited forms, and it cannot reach a figure caption in a notebook image.
   
D) C, with the **grid-cell-versus-IPP mismatch statement** emitted by the same path, so it appears wherever the comparison is described
   > **Impact**: NFR-TDEF-01 requires the mismatch disclosed, and `project.md` § Mandated requires the spatial-representativeness statement *"at the point where any IRI or GIM comparison is reported"* — a rule about every future report, which `external-products` W-7 answers the same way by emitting from the reporting path. Consistent treatment of the same problem shape. Costs coupling one sentence to the output path.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A is the criterion and cannot reach artifacts nobody has written. B removes the commonest cause of mislabelling. C catches the machine-readable cases and its limit is stated rather than hidden. D applies the same mechanism `external-products` chose for the map-to-map sentence, and for the same reason: a rule about every future report survives only if the path that writes reports emits it. Recommend also stating plainly that the notebook-caption case reaches no check and stays with the claims review.

[Answer]: D

---

## Question 9

**NFR-DQ-01 and TA-19 are this unit's only owned acceptance row**, and the story map's
§ Cross-unit responsibilities splits the obligation: *"`target-standardization` (produces
it)"* and *"`regimes-diagnostics-reporting` (reports it adjacent to the primary result)"* —
*"Production and adjacent reporting are separate obligations in the same requirement
family."*

TA-19's evidence is *"uncertainty budget artifact + its placement in the results section."*
**The placement half is not this unit's.**

NFR-DQ-01's own content: units, times, signs and fill values documented; **unexplained
negative VTEC rejected**; missingness and support reported **by cell and month**; target
uncertainty budget produced.

What does this unit build for TA-19?

A) The budget artifact, and cite TA-19 as its acceptance row
   > **Impact**: Accurate about production. But TA-19's evidence has two halves and one is `regimes-diagnostics-reporting`'s, so citing the row flatly reads as owning both — the exact error corrected at `external-products` for TA-36, where this stage claimed a primary test sited in another unit's module.

B) A, with the split stated: this unit **produces**, `regimes-diagnostics-reporting` **places**
   > **Impact**: Matches § Cross-unit responsibilities and avoids repeating the TA-36 error one unit later. Costs a sentence, and it makes the dependency visible to whoever assembles the evidence at the gate.

C) B, plus NFR-DQ-01's other three contents built and checked here — documented units/times/signs/fill values, **unexplained negative VTEC rejected**, missingness and support **by cell and month**
   > **Impact**: NFR-DQ-01 is four obligations and the budget is one of them; building only the budget leaves three of four unaddressed under a row this unit owns. The negative-VTEC rejection is the one with a physical meaning — a negative VTEC is not a small value but an impossible one — and "unexplained" is the operative word, so an explained negative needs a recorded explanation rather than silent acceptance. Costs three more checks.
   
D) C, plus the missingness and support report keyed to the **same cell and month** identifiers `inventory-and-registry`'s G-P1A record uses
   > **Impact**: The two artifacts describe the same coverage from different sides, and a G-P1A reviewer reading both should be able to line them up. Different keying is how two reports about one dataset become impossible to reconcile — the exact failure `project.md` records for counts compared by total rather than set-differenced. Costs agreeing one key with a sibling unit's already-designed record.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A repeats the TA-36 ownership error this stage corrected two units ago. B fixes it. C addresses the three-quarters of NFR-DQ-01 that the budget alone leaves out, including the negative-VTEC rule whose "unexplained" qualifier is doing real work. D makes this unit's coverage report reconcilable with the G-P1A record that accepts it — cheap now, and the alternative is discovering at the gate that two reports about one dataset cannot be compared.

[Answer]: D

---

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence — `foundation` R-01…R-17, `governance-guards` R-18…R-29, `acquisition` R-30…R-43, `inventory-and-registry` R-44…R-53, `external-products` R-54…R-63 — so this unit opens at **R-64**. If per-unit numbering was intended, say so at the gate and the artifacts restart.
- **[assumption]** `src/data/prepared.py` is **intra-package** and its shape is **this stage's to specify** — `component-methods.md` § Depth specifies cross-package boundary calls only and its Assumptions name `functional-design` (3.1) as where intra-package shapes are specified. **No amendment is owed for it.**
- **[assumption]** The §12 tree enumerates **21** test modules; `unit-of-work.md` § 5's **19** froze at the first of three same-day amendments. Question 2 decides how that is recorded.
- **[assumption]** D-17's field count is **16**, counted from its enumeration and matching BLK-05's own *"exactly D-17's approved 16 fields"*.
- **[assumption]** TA-19's placement half belongs to `regimes-diagnostics-reporting`; this unit produces the budget.
- **Open — BLK-05's implementation and execution limbs.** Naming and documentation are resolved; the module **does not exist** and has **never been run**, and no result of any kind is claimed. **Approving this stage discharges neither open limb.**
- **Open — where the D-17 conformance check reads the frozen field set from.** The same authority question **`governance-guards` R-20** raises for D-24: *"it must assert against the **authority**, not merely against the config."* **No third option is invented here**; carried to the gate. **Citation corrected 2026-08-23** from *"`inventory-and-registry` R-20"* — that unit's rules run R-44…R-53 and it has no R-20; `inventory-and-registry` **R-49** carries the distinct point that D-24's protected set is not reopened.
- **Open — the `02` ordinal collision**, a recorded §12 defect neither `unit-of-work.md` § 5 nor `components.md` resolves. `code-generation` **must not invent a `02a`/`02b` convention**.
- **Open — Vision §6.9's content list is unqualified in the source.** Four of six items are Phase 2 quantities; adding the phase qualifier runs through **Vision §15.2**.
- **Open — the zero-TBD preflight is not yet runnable on this component**, because `configs/` does not exist. D-19 is a decision made, not a check passed.
- **Open — the notebook-caption case of FR-P1-03-4 reaches no machine check** and stays with the claims-checklist review.
- **Open — FR-P1-03-5 has no §16/§19 acceptance row.** WS-05, the only field-contract row, is deferred to G-P3A by FR-WS-4; the requirement is enforced by the D-17 schema test and `tests/test_phase_boundary.py`, neither of which is an acceptance row.
- **Open — no numerical equivalence may be claimed between the Phase 1 and Phase 2 targets.** Cross-phase results test protocol transfer across a target-domain shift.
- **G-09 is not signed.** No answer here authorises creating `src/data/prepared.py`, `scripts/02_standardize_prepared_target.py`, `scripts/03_verify_processing.py` or `tests/test_prepared_target_schema.py`.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

---

## Consolidated Summary Confirmation

Questions 1–9 are answered above as the recommended option in each case, on the
owner's instruction to apply the recommendations. Consolidated:

| Q | Answer | What it settles |
|---|--------|-----------------|
| 1 | D | BLK-05: full test specification for `tests/test_prepared_target_schema.py`, its non-existence and no-result-claimed status carried into **every** citation, and the record that **approving this stage discharges neither open limb** |
| 2 | D | The §12 tree enumerates **21** test modules, derivation shown, both sources named; `unit-of-work.md` § 5's stale **19** reported at the gate for an annotate-in-place decision, on the precedent already recorded at `GOV-2026-08-22-INC-01` Rec 7 |
| 3 | D | Verification runs Vision §6.9's **two Phase 1-applicable** contents plus the **asymmetry statement**; the four Phase 2 items recorded **not-applicable with their reason**; a completeness assertion over the applicable set; and the record that §6.9's list is **unqualified in the source**, amendable only through Vision §15.2 |
| 4 | C | The `02` collision is restated as an unresolved §12 defect, with an assertion that a clean run contains **exactly one** `02` script selected by `--phase`. **No `02a`/`02b` convention.** The Phase-2-script-unreachable check is left to `governance-guards` rather than duplicated here |
| 5 | D | The schema test reads D-17's 16 fields from `configs/data.yaml`, asserts that config set **equals D-17** before comparing any row, and asserts the **excluded** set as well as the required one — the half where a Phase 2 quantity would appear |
| 6 | D | D-19's four values carry their **measured basis** into config; the zero-TBD preflight is recorded as **not yet runnable** — a decision made, not a check passed; and TE §6.1's superseded `>= 20` carries **why** it is superseded (it retains zero cell-hours against a deduplicated maximum of 12) |
| 7 | D | Two limbs: a value-level diff **enumerating the four permitted transformations** and failing on a fifth; and the statistic **resolved from config citing D-16**, with a run that cannot proceed on a default. Zenith weighting recorded as **deferred, not computable, nothing substituted** — a §18.2 forbidden choice |
| 8 | D | The **location-sampled gridded VTEC** label and the **grid-cell-versus-IPP mismatch statement** are emitted by the writing and reporting paths; a grep-class check covers the machine-readable cases; the notebook-caption case is stated as reaching **no check** and staying with the claims review |
| 9 | D | This unit **produces** the uncertainty budget; `regimes-diagnostics-reporting` **places** it — TA-19's two halves, split. NFR-DQ-01's other three contents built here, including **unexplained negative VTEC rejected**, with the missingness and support report keyed to the **same cell and month identifiers** `inventory-and-registry`'s G-P1A record uses |

**One answer deliberately does not reach into a sibling unit.** Q4 declines to assert the
Phase 2 script unreachable under `--phase 1`, because that is `governance-guards`'
phase-boundary rule; the gap is noted for that unit rather than guarded twice here.

**One answer inherits an open authority question rather than re-solving it.** Q5's
config-equals-D-17 assertion raises the same question **`governance-guards` R-20** already
carries for D-24 — where a conformance check reads a frozen decision from. **No third
option is invented.**

**One answer states an obligation on a sibling.** Q9's cell-and-month keying must agree with
`inventory-and-registry`'s G-P1A record. Stated, not claimed.

**Nothing here owes an amendment.** `src/data/prepared.py` is **intra-package**, and
`component-methods.md` § Depth names this stage as where intra-package shapes are specified.
The running total stays **five owed amendments across three units** — `acquisition` 3,
`inventory-and-registry` 1, `external-products` 1.

Carried to the gate, unchanged by these answers: BLK-05's implementation and execution limbs
open, and **not discharged by approving this stage**; `unit-of-work.md` § 5's stale 19; the
D-17 conformance-check authority question; the `02` ordinal collision; Vision §6.9's
unqualified list; the zero-TBD preflight not yet runnable; the notebook-caption case
unreachable by any check; FR-P1-03-5 with no acceptance row; no numerical equivalence
claimable between the Phase 1 and Phase 2 targets; rule numbering assumed to continue at
R-64; G-09 unsigned.

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

### Re-confirmation, 2026-08-23 — this file's four stale citations corrected

**No question, option or answer changed.** The three design artifacts had already been
corrected after an adversarial pass found the citation wrong in nine places; **this file
carried four of them** and could not be swept at the time because its receipt was locked.

**The correction:** every "`inventory-and-registry` R-20" now reads **"`governance-guards`
R-20"**. That unit's rules run R-44…R-53 and it has **no R-20**, so the citation contradicted
the numbering scheme these artifacts themselves assert. The rule that actually boxes the
inherited question is `governance-guards` R-20 — *"it must assert against the **authority**,
not merely against the config"* — while `inventory-and-registry` **R-49** carries the
distinct point that D-24's protected set is not reopened. **The reviewer's own recommendation
had been R-49, and it verified the repoint to R-20 as the correct referent on the following
pass.**

**Also settled since this file's last confirmation, and unchanged by it:** the adversarial
pass found that **"documented QC"** — one of Q7's four permitted transformations — is defined
nowhere in scope, which defeated the closed-set claim as first stated. The artifacts now
require the QC operations enumerated as a named list in `configs/data.yaml`, decline to
invent that list's membership, and state the check as **"specified but not yet
satisfiable"** until the list is fixed. **Q7's answer letter (D) is unchanged.**
*(Answered `Looks correct`, 2026-08-23; that receipt belongs to the previous attempt. The
live answer tag for this section is the blank one at its end.)*

### Re-confirmation, 2026-08-24 (sixth) — new stage attempt after the Inception close

**Why this is being re-asked.** Inception closed and Construction opened at
**2026-08-24T11:46:26Z**, starting a fresh `functional-design` attempt and resetting the
receipt floor for every unit.

**What changed upstream, and why it leaves this unit's answers untouched.** Two passes ran
on `foundation`, both in `governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md`:
the **amendment pass** (A **declined**; B and C **approved and executed**) and the **sites
9–11 addendum** (three superseded-status statements annotated in place inside `foundation`'s
own files).

| What the passes touched | Why this unit is unaffected |
|---|---|
| `component-methods.md` — `DeterminismRecord` **6 → 9** fields (B) | This unit reads `component-methods.md` **§ Depth** only — the cross-package-boundary-calls-only policy that makes intra-package shapes **this stage's** to specify. It consumes no `DeterminismRecord` field |
| `services.md` **§ Run record and registry** (C) | This unit reads **§ The nine stage scripts** and **§ Stage entry contract** |
| `unit-of-work.md` **§ 1** `Owns` (C) | This unit reads **§ 5**, including **BLK-05**'s four-limb status table |
| The sites 9–11 annotations | Inside `foundation`'s own artifacts; they annotate a superseded **status**, changing no contract, rule or entity |
| Amendment **A** — **declined** | **No count moved.** This unit's 6 requirements and **1** with no acceptance row (FR-P1-03-5) stand; it still owns TA-19 and supports TA-15 |

**Worth stating, because a past redo turned on exactly this file's cross-references.** The
§ Depth policy is the one upstream clause this unit leans on hardest, and it is **not** what
Amendment B changed — B added fields to a `foundation` entity, leaving the depth policy
untouched. The misreading of § Depth that prompted an earlier stage-wide redo is a separate,
already-closed matter.

**Its other upstreams, also unchanged.** `inventory-and-registry` **R-45** (registry) and
**R-49** (prepared-product schema), and `governance-guards` **R-23** and **R-24** (the
phase-boundary limbs this unit must not violate) — all re-confirmed or carried unchanged.

**What still stands.** Every answer, including **Q7=D** with *"documented QC"* enumerated as
a named list in `configs/data.yaml` and the check stated as **"specified but not yet
satisfiable"** until that list is fixed. **BLK-05** open; **FR-P1-03-5** with no acceptance
row; **G-09 unsigned**. The § Review verdict of **READY** belongs to the previous attempt.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The receipt is recorded for `target-standardization` under this attempt and its three artifacts are re-saved. No answer, contract, count or scientific value changes.

- Request changes
   > **Impact**: No receipt is recorded and nothing is re-saved. Tell me what to change and I re-present first.

> **💡 Recommendation**: **Looks correct** — the one upstream clause this unit depends on most, `component-methods.md` § Depth, is not what Amendment B changed, and every other amended section is one this unit does not read.

*(Answered `Looks correct` earlier on 2026-08-24; that receipt was reset by the authorised redo jump below. The live answer tag for this section is the blank one at its end.)*


### Re-confirmation, 2026-08-24 (post-redo) — receipt floor reset by an authorised redo jump

**Why this is being re-asked, and it is not about this unit.** The project decision owner
authorised a **redo jump on `functional-design`** at **2026-08-24T14:57:07Z**, so that three
standing reviewer findings on **`models-and-baselines`** (unit 8) could be fixed and
re-reviewed — its adversarial budget had been exhausted at NOT-READY, and the write-freeze on a
terminal review receipt made a redo the only route to a fix. **A redo resets the receipt floor for
every unit of the stage**, which is the stated cost that was accepted when the redo was chosen.

**Nothing in `target-standardization` changed.** No question, option, answer, amendment, rule, entity or
workflow of this unit was touched after its earlier confirmation today. The only artifacts edited
after the redo are `models-and-baselines`'s; its three fixes are confined to its own
files and reach no contract this unit consumes.

**The redo bought what it was for.** `models-and-baselines` returned **READY** on the
second pass of the restored budget, after three further Major findings were fixed. Two residuals
ride that READY verdict and are carried to the stage gate rather than applied.

**Everything this unit carried to the gate still stands, unchanged**, as recorded above.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The receipt is recorded for `target-standardization` under the post-redo floor and its three artifacts are re-saved. No answer, rule, entity, count or scientific value changes.

- Request changes
   > **Impact**: No receipt is recorded and nothing is re-saved. Tell me what to change and I re-present first.

> **💡 Recommendation**: **Looks correct** — this unit is untouched; the reset is a mechanical consequence of a redo taken for a different unit, and that redo achieved what it was authorised for.

*(Receipt reset by the fourteenth authorised redo, 2026-08-26T08:18:34Z. The live answer tag is the blank one below.)*

### Re-confirmation, 2026-08-26 — under the fourteenth-redo floor

**Nothing in this unit changed** since its terminal READY (2026-08-23T07:03:44Z, iteration 2). Derived this pass: **10 rules** (`R-64`…`R-73`), **9 workflows** (`W-1`…`W-9`), **9 entities**, **9 questions** all answered, **6 requirements / 1 without an acceptance row** (owns TA-19, supports TA-15), zero mojibake. The four `[Q&A] inventory-and-registry R-20` citations the READY flagged as deferred were already corrected in this file on 2026-08-23 (the correction record sits at its § “The correction”). Floor reset by the fourteenth redo (2026-08-26T08:18:34Z, taken for `external-products`).

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: Receipt recorded, artifacts re-saved natively, narrow confirming review runs.

- Request changes
   > **Impact**: Nothing recorded; tell me what to change.

> **💡 Recommendation**: **Looks correct** — mechanical: this unit is untouched and its terminal READY adjudicated content already.

*(Receipt superseded 2026-08-28 by the governance remediation below.)*

### Re-confirmation, 2026-08-28 — after the governance remediation

The full-board governance review of this stage (`governance/reviews/GOV-2026-08-28-FD-01.md`)
returned **FAIL** on 49 findings, and you ruled: resolve them. One reaches this unit.

**Recommendation 18 (High) — two physically different mismatches had been merged and
discharged by one mechanism.** NFR-TDEF-01 requires the **grid-cell-versus-IPP** mismatch
disclosed — a *cross-phase target-lineage* fact. TEC-06 requires the
**spatial-representativeness** statement wherever an IRI or GIM comparison is reported — a
*comparison-geometry* fact. Both were routed exclusively through the comparison-reporting
path, so a Phase 1 release, target artifact or coverage report carrying no comparison
disclosed the lineage mismatch **nowhere** — and that is the moment it matters most, because
Phase 2 compares against Phase 1's reported December timestamps.

**Applied:** the two statements are separated, each with its own emitting path and its own
negative control. The lineage statement now travels on the **target-writing path, beside the
`location-sampled gridded VTEC` label**, so it cannot be separated from the label. TEC-06's
sentence stays on the comparison-producing path — which is **not this unit's** (that is
`evaluation-and-comparison` R-110 limb 3). A new control fails a target artifact written
without the lineage statement; a further control fails emitting one statement in place of the
other. Board option 2 (one broadened trigger carrying both strings) is rejected on the record,
because it would close the coverage gap while preserving the conflation.

**Two corrections found while applying it, both strengthening the basis:**

1. **Q8 = D's literal text already placed the statement on the target-writing path** — option
   D reads "C, with the grid-cell-versus-IPP mismatch statement emitted by **the same path**",
   and that path in options B and C is "the code that writes the target". The conflation entered
   through D's **impact line**, which had imported `project.md`'s comparison trigger. So this
   restores your answered option's own reading rather than overriding it, and **no answer letter
   changes**.
2. **The superseded limb claimed an emission this unit does not own.** This unit produces no
   IRI/GIM comparison artifact, so the fix also removes a false ownership claim.

**Recorded, not resolved:** `regimes-diagnostics-reporting`'s claims-and-limitations checklist
owes an **NFR-TDEF-01 row** and an **FR-P1-03-4 row** — R-69's routing currently points at a
destination that does not exist. That unit is being remediated in parallel; the dependency is
stated here rather than annexed.

**Unchanged and verified in place:** 9 workflows, 10 rules (`R-64`…`R-73`), 9 entity sections,
6 requirements / 1 without an acceptance row. All three pre-existing open items stay open and
correctly routed — the "documented QC" enumeration's membership, the D-17 conformance
authority source (`governance-guards` R-20), and the `02` ordinal collision. D-1's cell rule,
D-16's median and D-17's sixteen fields are applied, never reinterpreted. **G-09 remains
unsigned; BLK-05's limbs stay open.**

**Four items the agent raised for you rather than deciding** (none applied): the QC-membership
item appears in no file's Assumptions register, only inside the rule boxes; the "6
requirements" figure sits under a 7-row courtesy table; no `IntegrityError` subclass is named
for a missing label or lineage statement; and NFR-TDEF-01 stays concentrated in this one unit
until the sibling adds its two checklist rows.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: Receipt recorded, the three artifacts re-saved with a dated provenance note, and an adversarial pass reviews the remediated text.

- Request changes
   > **Impact**: Nothing recorded; tell me what to change and I re-present first.

> **💡 Recommendation**: **Looks correct** — the fix restores the literal reading of the option you already answered, separates two facts a later reviewer would otherwise have to separate again, and adds the control that was missing rather than changing any decision.

[Answer]: Looks correct
