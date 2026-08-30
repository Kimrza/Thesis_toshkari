# Functional Design Questions — `evaluation-and-comparison`

**Unit** `evaluation-and-comparison` — the comparison mechanics: masks and the confirmatory
estimand.
**Kind** `library` · **Complexity** M · **Deployment** standalone · **Depends on**
`models-and-baselines`, `external-products`.

Unit **9 of 12**. It owns `src/evaluation/masks.py`, `src/evaluation/metrics.py`,
`scripts/07_evaluate_and_report.py` and `tests/test_common_masks.py` — **4 owned files,
derived by counting § 9's `Owns` list**, not carried. Its responsibility is the one
comparison-wide intersection mask computed once per comparison set with a stable ID and
reported row counts, the IRI-free denial applied at join time, and the confirmatory
estimand: the mean within-station difference of squared errors, **benchmark minus model**,
equal-station weighting, positive favouring the model.

**BLK-08 is OWNED here and is an EXIT condition on this stage.** The register is explicit:
`Transform.inverse` is specified as reachable from `Prediction.transform_id`, a `str` —
*"a string has no method"* — with no lookup, registry or resolution step named anywhere in
the five 2.6 artifacts, and no `src/evaluation` → `src/features` dependency row. It blocks
**a reported quantity, not an internal detail**: `ABL-DIFF` must inverse-transform to
absolute TECU before any metric (`project.md` § Mandated), and the paired loss differential,
the bootstrap interval and the practical-relevance threshold are all TECU-denominated.
Co-owner: `features-and-splits`, where `Transform` and its fitted state live. **BLK-03 ↓,
BLK-04 ↓ and BLK-09 ↓ are inherited** — this unit consumes the confirmatory prediction and
every metric it computes inherits the transform fit and the training range no field states.
All four are **exit conditions on stage 3.1, not entry conditions** (`GOV-2026-08-22-REM-01`
Rec 2, extended to BLK-08/BLK-09 on 2026-08-23): this unit may enter, **may not complete or
exit** 3.1 while any contract is unapproved, and **no implementation may proceed** while
they stand.

**4 requirements, 2 untested — derived by reading the story map's rows, and the two
upstream artifacts agree here**: FR-P1-04-7 (WS-16, TA-11), **FR-P1-05-7** (no acceptance
row), **FR-P1-05-17** (no acceptance row), NFR-FAIR-01 (WS-16, TA-11). Per-unit coverage
summary row: 4 requirements, 2 untested, **primary WS-16 (1 row)**, **supporting TA-11 and
TA-18 (2 rows)**. The untested pair is consequential: FR-P1-05-7 is the confirmatory
estimand itself, and FR-P1-05-17 is the obligation that the evaluation code this stage
designs is authored, reviewed and frozen inside the G-05 set before December is opened.

**G-09 is not signed.** Workspace inspection 2026-08-26: `tests/` holds three modules
(`test_acquisition_window.py`, `test_phase_boundary.py`, `test_release_hashes.py`) — none
this unit's; `src/` and `configs/` are absent. No answer here authorises creating any
module.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 9 — the `Owns` list (4 files), the boundary (IRI/GIM allowlist reach, "not the sole permitted importer"), the 4 requirements, the implementation notes; **BLK-08** (owned, with its Required-resolution field and the three candidate mechanisms), **BLK-03/BLK-04/BLK-09** (inherited, each with the exit-condition ruling); the § Roll-up by unit row naming `ABL-DIFF` and every TECU-denominated quantity as the blocked scope.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Table 1's four requirement rows, Table 2's WS-16/TA-11/TA-18 rows, § Per-unit coverage summary (4 / 2 / WS-16 / TA-11, TA-18), § Cross-unit responsibilities (FR-P1-02-3's audit ownership by `inventory-and-registry`), § Open verification gaps (BLK-08's row; **WS-13's evidence departs from TE §16 and names `test_common_masks.py`, owned here**, with no reading adopted).
- `../../../inception/requirements-analysis/requirements.md` — FR-P1-04-7, FR-P1-05-7 (sign convention in every table), FR-P1-05-17 (freeze timestamp precedes any December access), NFR-FAIR-01; consulted for context: FR-P1-05-6 (`ABL-DIFF`), FR-P1-05-9/-20 (honesty rules), FR-P1-05-12 (hash-before-metrics, write-once detection).
- `../../../inception/application-design/component-methods.md` § `src/evaluation` — `build_comparison_mask` (raises `FairnessError` "detected by the caller passing fewer than the full comparison set"), `paired_loss_differential`, `vector_block_bootstrap` (owned by `statistical-inference`), `count_storm_events`; § `src/models` — `Prediction` (with `partition_id`, `transform_id`), `fit_predict`, `three_seed_mean(..., expected_seeds)`, the `inverse_transform` paragraph BLK-08 was registered against; § `src/data/locked_test.py` — `AccessRecord` (purpose `"locked_evaluation"`), `open_restricted` (log-then-read, flush before return); § Depth (intra-package shapes are this stage's to specify) and the closing note carrying the two unresolved signature gaps to this stage.
- `../../../inception/application-design/services.md` — `07_evaluate_and_report.py`'s row (reads predictions carrying `partition_id`/`transform_id`, benchmark, mask; writes metrics, bootstrap intervals, breakdowns, figures), § Stage entry contract, the resource-envelope note that `07` carries the heaviest CPU cost, and the registry-artifact table (`07` regenerates the derived CSV).
- `../features-and-splits/functional-design/` — the ADR-11 contract this unit consumes: R-74 (identity check, one enumerated `REFIT` → `DEC` `score` exception), `Transform` as `(transform_id, partition_id)` persisted with the data, `FeatureBundle`, FU-4 = D (the provenance stamp `06`/`07` must refuse), **FU-7 = A** (the G-06 locked test scores **2–31 December, 30 days**, first 24 h excluded and counted). **Derived and printed 2026-08-26: `grep -c "inverse"` returns 0 in each of its four artifacts, and `BLK-08` appears in none** — the co-owner's finalized functional design carries no half of the joint contract this stage must author.
- `../models-and-baselines/functional-design/` — R-90 (the stamp refusal, closing `06`'s half of the eighth amendment "and only `06`'s"), R-91 (`three_seed_mean` contract), R-92 (provenance-agreement raises, the (`station`, `interval_start_utc`) alignment key); the open item stated identically in all three artifacts: **"`07`'s half of the eighth amendment is UNOWNED"**, raised at that unit's gate for this unit to own or decline.
- `../external-products/functional-design/business-rules.md` — R-54a (TA-36 not this unit's), R-56 (transitive import allowlist; `src/evaluation/` owned by three units, the allowlist is a path grant), R-59 (IRI generation validation, the 2000 km ceiling), R-60 (GIM comparator: map-to-map sentence **emitted by the reporting path itself**; `gim_network_overlap_flag` disclosure; C-01 labelled generated, not trained), R-62 (Dst diagnostic-only), R-63 (driver series time-indexed only); its Assumptions entry that IRI/GIM products join at evaluation time onto the frozen comparison-wide mask.
- `aidlc/spaces/default/memory/project.md` § Mandated/Forbidden — the comparison-wide mask rule (NFR-FAIR-01, TC-16), the estimand (Vision §2.3, TE §1.3), IRI evaluation-time-only (NFR-IRI-01), GIM evaluation-time-only + overlap disclosure (TE §5.2), the three difficulty controls co-reported, the beat-the-LSTM disclosure, the spatial-representativeness statement (TEC-06), G-06 hash-before-metrics, `ABL-DIFF` inverse-to-TECU, the `phase_id`/`source_id`/`target_definition_id` stamp.
- Workspace inspection, 2026-08-26: `tests/` holds three modules, none this unit's; `src/` and `configs/` absent.
- Absent by scope design: `stories` (2.4 `SKIP`), `mockups` (1.6 and 2.5 `SKIP`). `kind: library`.

---

## Question 1

**BLK-08's resolution is this stage's to author, and the register names the decision
sequence.** Quoted from the Required-resolution field:

> *"3.1 states first **whether the transform touches the target**. If it does: name the
> resolution mechanism, add the matching `component-dependency.md` row, and fix the
> ownership of the fitted state that `inverse` reads. If it does not: say so explicitly in
> both `component-methods.md` and ADR-11's consequences, so `ABL-DIFF`'s obligation is
> visibly satisfied rather than silently assumed."*

**The "does not touch the target" exit is not fully available.** Even if the primary
configuration's train-only transforms are features-only (model output natively in TECU),
`ABL-DIFF` is *defined* by a transformed target — TE §7.2 requires it to inverse-transform
to absolute TECU before any metric — so at least one predeclared run needs an executable
inverse path. The register's three candidate mechanisms: a registry keyed by
`transform_id`; an `inverse_transform_id` on `Prediction` with a named owner; or a
permitted import edge. A `features` → `evaluation` direction is recorded as **not
available** (it would invert the dependency); an `evaluation` → `features` edge is the
direction the register contemplates.

How does `src/evaluation` reach the fitted inverse?

A) Declare the primary configuration's transforms features-only, and record that no inverse path exists for any target-touching configuration
   > **Impact**: Satisfies the register's second branch for the primary path — the obligation is visibly satisfied for the headline numbers. But it leaves `ABL-DIFF` unimplementable as predeclared, and FR-P1-05-6 requires all five ablations to hold pre-freeze registry rows: an ablation the design cannot execute would have to be withdrawn through Vision §15.2, a scientific-protocol change this stage cannot make.

B) Reimplement the inverse arithmetic inside `src/evaluation`, reading the persisted transform parameters by `transform_id`, with no new import edge
   > **Impact**: No dependency change. But it creates a second copy of the fit/inverse mathematics in a different package — the drift class §14's one-copy rule exists to prevent — and a fit whose inverse is maintained separately can silently disagree with it, which no test would catch until the round-trip is asserted.

C) A permitted `src/evaluation` → `src/features` import edge: `features-and-splits` persists each fitted `Transform` and exposes a resolver (`load_transform(transform_id) -> Transform`), `src/evaluation` calls `Transform.inverse(frame)`, and the matching `component-dependency.md` row is recorded as an amendment owed
   > **Impact**: One copy of the inverse, owned where the fit lives, resolved by the identity ADR-11 already persists (`Prediction.transform_id`). Costs a boundary amendment and touches the co-owner's contract: the resolver and the persisted fitted state are `features-and-splits` surfaces its finalized artifacts do not yet carry (see Question 2). The §12 import-boundary rule is unaffected — the `iri.py`/`gim.py` allowlist constrains a different pair of modules.

D) C, plus the primary-path statement and the round-trip control: state explicitly (here and in the co-owner's contract) **whether the primary configuration's transform touches the target**, so the primary path's TECU status is a recorded fact rather than an inference; require a `Transform` to declare its target-touching status machine-readably; and pair the mechanism with a negative control — a `Prediction` whose `transform_id` resolves to no persisted transform **raises**, and a resolved inverse must round-trip (`inverse(apply(x)) == x` within declared tolerance) on a fixture
   > **Impact**: Delivers both halves of the register's sequence in one contract: the target-touching question answered explicitly for every configuration, and the mechanism named with the control that proves a broken resolution is caught rather than silently producing transformed-space metrics. Costs the same amendment as C plus a declared-status field on `Transform` — an intra-package shape `component-methods.md` § Depth already assigns to 3.1.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A is foreclosed by `ABL-DIFF`'s definition; B trades a dependency row for duplicated scientific arithmetic, the worse debt. C is the register's own contemplated mechanism in the available direction. D adds what this project's affirmed methodology demands — a negative control paired with the hard rule — and answers the register's "states first" question explicitly instead of leaving the primary path's TECU status to inference. The dependency-row amendment is the honest price; BLK-08 exists because the previous design claimed the price was zero.

[Answer]: D

---

## Question 2

**BLK-08's co-owner has finalized its functional design without the joint contract.** The
register makes the resolution joint: *"the contract: `functional-design` (3.1), jointly for
`evaluation-and-comparison` and `features-and-splits`"*, and neither owner *"may exit
without the contract"*. But `features-and-splits`' four functional-design artifacts were
re-saved 2026-08-26 under a re-confirmation receipt, and — **derived, not assumed**:
`grep -c "inverse"` returns **0** in each of the four, and neither `BLK-08` nor
`train_start` (BLK-09, also owned there) appears in any of them. Whatever Question 1
chooses, the co-owner's side — the persisted fitted state, the resolver, the
target-touching declaration — lives on surfaces that unit's frozen artifacts do not carry.

Where does the joint contract's text land?

A) Author both halves here, in this unit's artifacts, and record that `features-and-splits` is bound by citation
   > **Impact**: Fastest, and the contract exists in one place. But it writes another unit's obligations into artifacts that unit's builder does not read — the exact failure `project.md`'s representation-sweep learning records (BLK-08/BLK-09 "reached no per-unit paragraph at all, which defeated the stated reason for registering them as blockers"). A frozen READY receipt on the sibling also means nothing there acknowledges being bound.

B) Author this unit's half here; raise the co-owner's half at the gate as a named cross-unit obligation, for the owner to rule on how `features-and-splits`' artifacts take their half (re-entry, addendum, or annexed contract)
   > **Impact**: Respects the write-freeze on the sibling's receipted artifacts — this stage edits no other unit's files — while making the gap a gate decision instead of a discovery at code-generation. The precedent exists: `models-and-baselines` raised "07's half is unowned" at its own gate rather than writing into this unit. Costs the contract being split across a gate ruling until the owner acts.

C) B, plus the joint contract drafted as one named, citable statement inside this unit's `business-rules.md` — both halves stated, this unit's half binding now, the co-owner's half explicitly marked "pending its owner's adoption" — so the gate ruling has a complete text to adopt rather than a description of one
   > **Impact**: One statement consumed by name cannot drift (the reason `features-and-splits`' own Q1 = D chose the same shape for BLK-04), and the pending-adoption marking keeps the sibling's frozen artifacts unedited while making the obligation impossible to overlook. Costs the drafting, and the marked half is not binding until adopted — which must be stated honestly, since BLK-08 does not close for either owner until it is.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A repeats the register's own documented failure mode and edits nothing it may edit anyway; B is correct but hands the gate a gap instead of a text. C gives the owner one decision over a complete draft, keeps every write inside this unit's produced artifacts, and states plainly that BLK-08 remains open for both owners until the co-owner adopts its half — which is also the honest reading of "exit condition on 3.1 for both owning units".

[Answer]: C

---

## Question 3

**Where is `ABL-DIFF`'s inverse-before-metric rule enforced?** `project.md` § Mandated:
*"`ABL-DIFF` inverse-transforms to absolute TECU before any metric."* Question 1 supplies
the mechanism; this question fixes the enforcement point — because a mechanism that exists
but is not demanded is a convention, and the blocked scope named for this unit is
*"`ABL-DIFF` and every TECU-denominated quantity"*.

A) Enforce by call order in `scripts/07_evaluate_and_report.py`: the script applies the inverse before calling any metric
   > **Impact**: Works when the script is the only caller, but §7 makes scripts orchestrators of `src/` logic precisely so governed checks do not live in them; a notebook or test calling `paired_loss_differential` directly would bypass the rule with no error.

B) The metric functions refuse transformed-space input: `paired_loss_differential` (and every metric entry point) raises unless the `Prediction`'s resolved transform is declared non-target-touching or an inverse has been applied
   > **Impact**: Moves the check to the boundary every caller crosses. Requires the target-space status to be determinable from the `Prediction` — which Question 1 option D's declared-status field supplies — and makes "before any metric" a checked precondition rather than a remembered ordering.

C) B, plus the inverse application is itself stamped: applying `Transform.inverse` produces a new `Prediction` whose transform lineage records the inversion, so "the inverse was applied" is a fact on the artifact rather than a memory of a call — with the negative control that an `ABL-DIFF` prediction reaching any metric un-inverted **raises**
   > **Impact**: The same stamp-not-memory principle ADR-11 settled for the forward direction (`transform_id` travels because "the stamp has to travel the whole way"). The negative control is the project's affirmed methodology; without it the rule has only a happy-path proof. Costs one lineage field on an object this stage already specifies.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A restores the class of gap ADR-11 spent five review cycles removing — an obligation satisfied only when one specific caller behaves. B is the right boundary; C makes the satisfied obligation observable on the artifact and pairs it with the violation-is-caught control, exactly parallel to how `fit_predict` refuses an untransformed bundle on the forward path.

[Answer]: C

---

## Question 4

**`07`'s half of the eighth amendment is unowned, and this unit must now own it or decline
it.** `features-and-splits` FU-4 = D requires **`06` and `07`** to refuse a frame whose
provenance stamp is not `(fold k, evaluate)` when scoring fold *k*'s validation month.
`models-and-baselines` R-90 closed `06`'s half — *"and only `06`'s"* — and raised the rest
at its gate: *"`07`'s half of the eighth amendment is UNOWNED… `unit-of-work.md` assigns
`07_evaluate_and_report.py` to `evaluation-and-comparison`, whose functional design has not
run."* It has now run this far. One fact narrows the question: `07` receives
**`Prediction`s, not frames** — ADR-11 routed the stamps onto `Prediction.partition_id` and
`Prediction.transform_id` for exactly this reason ("the stamp has to travel the whole way").

A) Declare ADR-11's `Prediction` fields sufficient: the stamp refusal happened at `06`, and `07` adds no check
   > **Impact**: Trusts every producer of a `Prediction`. A hand-assembled prediction, or the B-01/C-01 comparator products which `06` never sees, would enter comparisons unchecked — the unstamped-frame case is precisely the negative control R-90 fires on at `06`, reproduced here with nothing firing.

B) Own it: every `Prediction` entering a comparison must carry non-`None` `partition_id` and `transform_id`, all members of one comparison must agree on `partition_id`, and a mismatch or absence **raises** — mirroring `models-and-baselines` R-92's provenance-agreement rule at this unit's boundary
   > **Impact**: Closes `07`'s half at the object `07` actually receives. Cheap — the fields exist since ADR-11 — and consistent with R-92, so the two consuming units' accounts of the eighth amendment agree. Requires stating how benchmark/comparator `Prediction`s (B-01, C-01) are stamped, since they are generated, not trained.

C) B, plus the mask carries the stamp too: the comparison mask records the `partition_id` and the member `transform_id` set it was built over, and scoring a `Prediction` against a mask built for a different partition **raises** — with negative controls for the mismatched-stamp, absent-stamp and wrong-mask cases
   > **Impact**: Extends the refusal across `07`'s own file-mediated handoff (mask built, then consumed), the same gap class FU-4 found between `05` and `06`. The amendment total is unaffected — the stamp contract is counted once, by `features-and-splits` — and this unit's artifacts record the landing site so all three accounts agree. Costs stamp fields on the mask object this stage specifies anyway (Question 5).

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A leaves the raised-at-gate item to be rediscovered at code generation with the comparator products as the unguarded path. B is the minimum that makes FU-4 = D true as stated. C applies the sibling's own lesson — provenance must survive every handoff, including this unit's internal one — and closes the eighth amendment's last open half with the controls that prove it.

[Answer]: C

---

## Question 5

**"The full comparison set" is undefined, and `build_comparison_mask` cannot detect what is
not declared.** The approved signature raises `FairnessError` when called per-pair,
*"detected by the caller passing fewer than the full comparison set"* — but no artifact
states what the full set **is**, so the check as designed compares against nothing.
Membership also has a scientific consequence: the mask is an **intersection** over its
members' availability, so adding a member shrinks the scored rows for every comparison in
the set. The governing documents fix pieces: the primary results table co-reports M-01,
M-02, M-03 with the LSTM-vs-IRI comparison on matched windows (Vision §2.4, NFR-FAIR-01);
C-01 GIM is *"explicitly a map-product-to-map-product comparison"* that *"cannot validate
receiver-level station VTEC"* (R-60); D-24's item 17 enumerates the protected baselines as
M-01, M-02, M-03, B-01 and C-01.

How is comparison-set membership defined and where does the mask freeze?

A) Membership is the caller's list: whatever `Sequence[Prediction]` arrives defines the set, and `FairnessError` fires only on a length-two call
   > **Impact**: Implements the letter of the signature and nothing else. A comparison quietly run without M-03 would pass, and NFR-FAIR-01's "computed once per comparison set" is unenforceable when the set is whatever was passed — the pairwise-mask defect readmitted through membership instead of through masks.

B) Membership is declared configuration: each comparison set is named in `experiment.yaml` with its enumerated member IDs, `build_comparison_mask` receives the declared set through `ConfigSnapshot` and **raises** when the passed predictions do not match it exactly — missing member, extra member, or duplicate
   > **Impact**: Makes "full comparison set" checkable and keeps the membership out of source (TC-03e — it is a frozen scientific choice, not code). Requires the enumerated memberships to be confirmed at the gate, since fixing them is a scientific decision this stage may propose but not silently make.

C) B, with two declared sets proposed for confirmation: the **primary set** {M-01, M-02, M-03, M-06, B-01} carrying one mask, and the **GIM comparison** {M-06, C-01} as its own set with its own mask — never merged silently — because R-60's map-to-map framing and the overlap-audit condition make C-01 a differently-caveated comparison, while folding it into the primary mask would shrink the primary scored set for a comparator that cannot validate the target
   > **Impact**: One mask per comparison set, both computed once, both stable — NFR-FAIR-01 satisfied per set rather than diluted across an unjustified union. The membership split is a proposal grounded in Vision §2.4/§6.10 and goes to the gate as an explicit confirmation, not a default (TE §18.3's stop-and-report posture: this is a value the student and supervisor own).

D) C, plus the mask's identity and freeze mechanics: `mask_id` derived deterministically from the declared set and the masked row content (recomputation reproduces the same ID or raises), row counts recorded per station, `phase_id`/`source_id`/`target_definition_id` and the Question 4 stamps carried on the mask, the mask registered once — a second registration for the same comparison set **raises** — and the whole registered set inside the G-05 frozen bundle (FR-P1-05-17)
   > **Impact**: Delivers WS-16's evidence ("mask registry with stable IDs", row counts) as designed behaviour rather than convention, makes "computed once" executable, and ties the masks to the freeze FR-P1-05-17 requires. Costs specifying the registry shape — intra-package, this stage's to specify per § Depth.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A leaves the signature's own stated check without an input. B is the minimum that makes it real. C states the membership question honestly as the scientific choice it is and routes it to the gate instead of deciding it in code — the recommendation itself (two sets, GIM separate) follows Vision §6.10's framing, and the owner may rule otherwise. D adds the identity, once-only and freeze mechanics that WS-16, NFR-FAIR-01 and FR-P1-05-17 respectively demand, each as a check rather than a description.

[Answer]: D

---

## Question 6

**The estimand pipeline needs its aggregation order, its mask precondition and its sign
convention fixed as contract.** FR-P1-05-7: the confirmatory estimand is the paired loss
differential — mean within-station difference of squared errors, **benchmark minus model**,
equal-station weighting, positive favouring the model — and *"every table reporting the
differential states the sign convention"*, because *"a signed differential printed without
it inverts the conclusion for any reader who assumes the opposite orientation"*. The
approved signature returns the scalar and per-station components and takes `mask` as a
required keyword. Left unspecified: the aggregation order as an executable definition, what
happens when the mask is not the frozen registered one, and how the sign convention reaches
tables this unit does not build (`regimes-diagnostics-reporting` owns them).

A) Implement the signature as approved, with the aggregation order documented in prose
   > **Impact**: The estimand is the project's single most protected number and FR-P1-05-7 is already `UNTESTED`; prose ordering leaves equal-station versus pooled weighting — a difference that changes the headline value — to the implementer's reading.

B) Fix the pipeline as ordered contract: squared errors per (station, hour) on masked rows only → per-station mean of paired differences (benchmark minus model) → unweighted mean of the three per-station values; and the function **raises** when `mask` is not a registered frozen mask for the members' declared comparison set (Question 5's registry supplies the check)
   > **Impact**: The aggregation becomes one executable definition — the same move `windows.py` made for FR-P1-04-8 — and a metric computed off-mask or on an ad-hoc mask becomes an error instead of a wrong number. Costs depending on the mask registry, which this unit owns anyway.

C) B, plus the result object carries its own interpretation: the returned value is a shape (this stage's to specify) recording the scalar, per-station components, the orientation (`benchmark_minus_model`), the weighting (`equal_station`), and the sign-convention sentence — so any table built from it inherits the convention machine-readably rather than restating it
   > **Impact**: FR-P1-05-7's every-table obligation becomes checkable downstream: `regimes-diagnostics-reporting` asserts the field's presence instead of remembering a sentence. One statement consumed by name cannot drift — the same reasoning the sibling units applied to their cross-unit contracts.

D) C, plus the negative controls: an inverted orientation (model minus benchmark) fails on a fixture whose true sign is known; a pooled row-weighted aggregation fails on a fixture with asymmetric station counts; a metric call with an unregistered mask **raises**
   > **Impact**: Pairs the hard rule with the tests that prove violations are caught — the affirmed methodology. The two fixtures are synthetic and CPU-trivial; they are the difference between the estimand being defined and the estimand being defended.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. The estimand and its sign convention are the exact place a silent implementation choice inverts a thesis conclusion; FR-P1-05-7 has no acceptance row today, so these contract-level controls are the only bar it gets until stage 3.2 proposes one. B fixes the number, C makes the convention travel, D proves both.

[Answer]: D

---

## Question 7

**The locked-test evaluation path: three orderings, one boundary, one scored-set rule.**
This unit's `07` performs the G-06 evaluation. The governing rules: predictions are
generated and written **exactly once** after G-05 is signed and **hashed before any
metric** (G-06, FR-P1-05-12 — TA-18 names this unit supporting on "prediction hash
preceding any metric"); every December access is routed through
`governance-guards.open_restricted` with a log-then-read `AccessRecord` (purpose
`"locked_evaluation"`); the **pre-G-05 coverage audit is NOT this unit's** —
`inventory-and-registry` performs it, performance-blind (story map § Cross-unit
responsibilities); and **FU-7 = A** fixes the scored set: the G-06 locked test scores
**2–31 December (30 days)**, first 24 h excluded and counted.

A) Document the G-06 protocol in this unit's artifacts; the orderings are operator procedure
   > **Impact**: The team practice is explicit that locked-test discipline is "an executable guard, not only a signature". Procedure alone reproduces the class of gap WS-18/TA-18 exist to close, on the one event that can never be re-run.

B) Make hash-before-metrics executable: every metric entry point evaluating the DEC partition requires a recorded prediction-hash receipt, re-verifies the prediction file against it before computing (write-once detection per FR-P1-05-12), and **raises** when the receipt is absent, the hash mismatches, or the receipt timestamp does not precede the metric call
   > **Impact**: The ordering becomes a checked precondition at this unit's boundary. The hash recording itself is `06`'s act; what this unit owns is refusing to score without it — the supporting-role split TA-18 already records.

C) B, plus the access boundary and the scored set: `07`'s December target read arrives only through `open_restricted` with purpose `"locked_evaluation"` and a G-05 signature reference (this unit constructs no path into the restricted root — the chokepoint rule); and the DEC comparison's mask **asserts the scored range is exactly 2–31 December** with the first 24 h excluded and counted — a 1 December row reaching metrics **raises**
   > **Impact**: Encodes FU-7 = A where it bites — the mask that defines the scored rows — so the 30-day ruling cannot be silently widened back to 31 days at implementation. The chokepoint routing keeps this unit out of BLK-07's failure class. Costs one range assertion and the `open_restricted` consumption already contemplated for this unit.

D) C, plus the boundary statement in both directions: this unit's artifacts record that it performs **no** pre-G-05 December read of any kind — the coverage audit is `inventory-and-registry`'s permitted read, a different event under a different purpose — and that any `07` execution against DEC before a verifying `g05_signature` is blocked upstream by `materialise_locked_partition` and is additionally refused here
   > **Impact**: States the one-shot rule and the audit's legitimacy as separate facts — the distinction the team practice was explicitly corrected to preserve — so neither obligation is misread as the other. Costs two sentences and one redundant refusal, and redundancy at the locked boundary is by design, not waste.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. B and C are the executable minimum for an event with no retry. D's boundary statement is what keeps this unit from repeating the "opened exactly once" misreading the team practice records having already corrected once — the coverage audit is legitimate, earlier, and someone else's; the metrics evaluation is one-shot, hash-gated, and this unit's.

[Answer]: D

---

## Question 8

**The honesty-rule mechanics: which limbs are checks here, and which are documented
obligations owned downstream?** Three mandated rules land near this unit: the three
difficulty controls co-reported in the primary results table (FR-P1-05-9, TA-20 — owned by
`regimes-diagnostics-reporting`); any baseline beating the LSTM disclosed in the table
**and** the abstract-level conclusion (FR-P1-05-20, `UNTESTED`); the
spatial-representativeness mismatch stated wherever an IRI or GIM comparison is reported
(TEC-06 — Phase 1 compares a grid cell against a station-coordinate evaluation, and part of
any measured difference is a geometry and sampling artefact rather than skill). This unit
builds none of the tables — but it computes every number they contain.

A) All three are reporting obligations: record them as constraints on `regimes-diagnostics-reporting` and compute numbers only
   > **Impact**: Leaves the table able to omit a control because the metric was never computed — a gap no reporting-side check can close, since it cannot assert the presence of a number that does not exist.

B) Guarantee completeness upstream: the evaluation run computes the estimand for **every** member of the declared primary comparison set over the one frozen mask, and refuses to emit a results artifact with any declared member's metric missing
   > **Impact**: Makes the co-reporting rule satisfiable by construction — a primary table missing M-02 becomes impossible upstream of the table, not detectable after it. Rests on Question 5's declared membership; without it "every member" is unenforceable.

C) B, plus the machine-readable disclosure trigger: the emitted metrics artifact carries, per benchmark, the differential's sign and a derived `beats_model` flag — so FR-P1-05-20's disclosure check downstream has a field to assert against the abstract-level text rather than prose to re-derive
   > **Impact**: Turns the project's highest-rated reporting risk (R-16) from a reading exercise into a field comparison. The flag is derived from the sign convention Question 6 fixes; it decides nothing scientific, it only makes the already-computed fact impossible to overlook.

D) C, plus the spatial-representativeness sentence emitted by the comparison-producing path itself: every serialized IRI or GIM comparison artifact carries the mandated mismatch statement (grid cell versus station-coordinate evaluation), the way `external-products` R-60 emits the map-to-map sentence — because a rule about every report, including reports nobody has written yet, survives only when the producing code emits it
   > **Impact**: The disclosure cannot be dropped by a new report or notebook, and the same mechanism carries `gim_network_overlap_flag`'s value wherever GIM is compared (TE §5.2). Costs an emitted field and its presence test; the sentence's wording is fixed by the governing documents, not invented here.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. The division of labour is real — tables and abstracts belong downstream — but each limb has a computable precondition that only this unit can guarantee: the number exists (B), the trigger is a field (C), the caveat travels with the comparison (D). R-60 already proved the emit-from-the-path pattern on this project; adopting it here keeps the two units' honesty mechanics congruent.

[Answer]: D

---

## Question 9

**`tests/test_common_masks.py` is this unit's one test module, and TE §16 names it as
evidence for a row this unit does not produce.** The story map records the departure and
adopts no reading: WS-13 (matrix/tensor window parity) lists evidence *"matched-window
parity assertion over one `windows.py` definition — departs from TE §16's stated evidence
for this row, which names `test_common_masks.py` (owned by `evaluation-and-comparison`, not
by this row's evidence-producing unit)"*. `features-and-splits` (its Q5 = D) built the
parity assertion and carried the departure to the gate unresolved — noting
`test_common_masks.py` is required here through TA-11 regardless. TA-11's own text names
*"comparison-wide mask tests… including the matched-window assertion"*. Stage 3.1 owns
verification planning for this gap (story map § Open verification gaps); any change to
§16's evidence column runs through Vision §15.2.

What is `test_common_masks.py`'s scope?

A) Masks only: WS-16's evidence (stable IDs, row counts, no pairwise mask) and nothing else; the WS-13 departure is left exactly as the story map records it
   > **Impact**: Clean ownership, but it leaves §16's WS-13 evidence column naming a module that deliberately tests nothing about WS-13, and leaves TA-11's "matched-window assertion" phrase without a named home in the module TA-11 cites.

B) Masks plus the matched-window assertion at the comparison boundary: the module additionally asserts that every member of a comparison set was scored over the **same window length and lag set** (NFR-FAIR-01's matched-windows limb, TA-11's phrase) — a property of comparisons, distinct from `windows.py`'s representation-parity property
   > **Impact**: Gives TA-11's citation a real referent inside this module without claiming WS-13, whose parity property genuinely lives in `windows.py`. The two checks test different properties of one fairness rule, the same by-property split the siblings recorded for R-56/R-57 overlaps.

C) B, plus the negative controls and the departure put to the gate as one item with a stated recommendation: a pairwise mask attempt **fails** (FR-P1-04-7's criterion); a comparison over mismatched window lengths **fails**; a recomputed mask with a different ID **fails**; and the gate item proposes recording WS-13's evidence as the `windows.py` parity assertion with `test_common_masks.py` supporting via the matched-window limb — a §16 evidence-column clarification for the owner to route through Vision §15.2 or decline
   > **Impact**: The module's scope is settled by its properties, the controls prove the mask rules catch violations, and the two-unit ambiguity gets one owner decision over a complete proposal instead of two units each waiting for the other. Costs the controls and one gate item; the §15.2 change itself is proposed, not made.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A leaves a governed checklist row citing a module that ignores it; B resolves the citation by the only reading under which both artifacts are right (two properties, two homes). C adds the violation-is-caught controls the affirmed methodology requires and finally gives the WS-13 departure — open since 2026-08-22, expressly deferred to 3.1 — the single complete proposal the owner has been owed.

[Answer]: C

---

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence — `foundation` R-01…R-17 through `target-standardization` R-64…R-73, `features-and-splits` R-74…R-82, `models-and-baselines` R-90…R-102 (ranges derived by grepping each unit's `business-rules.md` headings) — so this unit opens at **R-103**. The R-83…R-89 gap between two siblings is observed, not explained; if it was a reservation, or per-unit numbering was intended, say so at the gate and the artifacts renumber.
- **[assumption]** The `src/evaluation` shapes beyond the four approved boundary calls — the mask registry, the estimand result object, `Transform`'s declared target-touching status, the comparison-set declaration's read side — are **intra-package** and this stage's to specify (`component-methods.md` § Depth, Q1 = B). Question 1's dependency row and Question 5's `experiment.yaml` membership are the two surfaces that exceed that grant, and both are named as costs in their questions rather than assumed free.
- **[assumption]** `vector_block_bootstrap` and `count_storm_events` sit in `src/evaluation/` but belong to `statistical-inference` and `regimes-diagnostics-reporting` respectively — the allowlist is a module-path grant and `src/evaluation/` is owned by three units (`external-products` R-56). This unit designs `masks.py` and `metrics.py` only, and asserts no unit-level narrowing of TE §12.
- **[assumption]** The benchmark and comparator `Prediction`s (B-01 IRI, C-01 GIM) are producible in the `Prediction` shape with `seed = None` and generated-not-trained provenance; how their `partition_id`/`transform_id` stamps are populated is part of Question 4's contract, since `06` never sees them.
- **Verification obligations owned here:** the round-trip inverse control (Q1); the un-inverted-`ABL-DIFF` raise (Q3); the mismatched/absent-stamp and wrong-mask raises (Q4); the membership-exactness, once-only-registration and stable-`mask_id` checks with the pairwise negative control (Q5); the orientation and weighting fixtures and the unregistered-mask raise (Q6); the hash-receipt precondition, the 2–31 December range assertion and the chokepoint routing (Q7); the completeness refusal, `beats_model` field and emitted disclosure sentences with presence tests (Q8); `test_common_masks.py`'s three negative controls (Q9).
- **Governance dependencies owned outside this unit:** BLK-03's contract limbs (`models-and-baselines`, 3.1); BLK-04's contract limbs and enumerated negative control, and BLK-09's `train_start` resolution (`features-and-splits`, 3.1 — **neither appears in its finalized artifacts; derived: 0 grep hits**); the co-owner's adoption of BLK-08's other half (Question 2's gate item); the comparison-set memberships' confirmation (Question 5 — a student/supervisor-owned scientific choice, proposed not decided); any §16 evidence-column change for WS-13 (Vision §15.2); acceptance rows for FR-P1-05-7 and FR-P1-05-17 (stage 3.2 under Vision §15.2); G-05's freeze of the evaluation code this stage designs (Supervisor); the AGPLv3 distribution question (outside the project).
- **Open — BLK-08 is an EXIT condition on this stage for both owners.** Questions 1–3 author this unit's half; the blocker does not close until the co-owner's half is adopted (Question 2). **BLK-03 ↓, BLK-04 ↓, BLK-09 ↓ remain open exit conditions inherited here** — nothing in this file closes them, and no implementation may proceed while any stands.
- **Open — FR-P1-05-7 and FR-P1-05-17 carry no acceptance row** (2 of this unit's 4, derived from the story map's rows). The contract-level controls in Questions 6 and 7 are design obligations, not acceptance rows; adding rows is stage 3.2's under Vision §15.2.
- **Open — FR-P1-05-17's freeze evidence is partly outside this unit's control**: the modules' hashes sit inside the G-05 frozen bundle and the freeze timestamp must precede any December access — an ordering the G-05 record produces, which this stage can require but not manufacture.
- **G-09 is not signed.** No answer here authorises creating `src/evaluation/masks.py`, `src/evaluation/metrics.py`, `scripts/07_evaluate_and_report.py` or `tests/test_common_masks.py`, and TE §18.3's stop-and-report rule binds every affected component while any P0 decision is unresolved.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant. Where a question touches one — Question 5's membership, Question 7's scored set — the value is either already frozen (FU-7 = A) or expressly routed to the gate.

---

## Consolidated Summary Confirmation (superseded by the 2026-08-28 post-execution pass below)

Questions 1–9 are answered above: **Q1 = D, Q2 = C, Q3 = C, Q4 = C, Q5 = D, Q6 = D, Q7 = D,
Q8 = D, Q9 = C**. This is the pre-generation summary stop: before the three design artifacts
are generated, this section states the whole of what those answers commit to, and nothing else
is generated from them.

### What will be generated

Three artifacts, in this directory:

- **`business-logic-model.md`** — the workflows: comparison-mask construction and once-only
  registration (Q5); the estimand pipeline in its ordered form — squared errors per
  (station, hour) on masked rows only → per-station mean of paired differences, **benchmark
  minus model** → unweighted mean of the three per-station values (Q6); the inverse/`ABL-DIFF`
  path via the `src/evaluation` → `src/features` resolver, with the round-trip control and
  the metric-boundary refusal (Q1, Q3); the G-06 locked-test evaluation path — hash-receipt
  precondition, `open_restricted` chokepoint with purpose `"locked_evaluation"`, the
  2–31 December range assertion (Q7); the honesty mechanics — completeness refusal,
  `beats_model` flag, disclosure sentences emitted by the comparison-producing path (Q8);
  and `07`'s stamp refusal closing the eighth amendment's last open half (Q4).
- **`business-rules.md`** — rules opening at **R-103**, continuing the single sequence per
  the numbering assumption; **the R-83…R-89 gap** between `features-and-splits` (R-74…R-82)
  and `models-and-baselines` (R-90…R-102) **is observed, not explained, and is flagged at the
  gate** — if it was a reservation, or per-unit numbering was intended, the artifacts
  renumber. This artifact also carries the **BLK-08 joint contract** drafted as one named,
  citable statement (Q2 = C, § The blockers below).
- **`domain-entities.md`** — the intra-package shapes `component-methods.md` § Depth assigns
  to this stage: the **mask object** (deterministic `mask_id`, per-station row counts,
  `phase_id`/`source_id`/`target_definition_id` plus the Q4 stamps); the **estimand result
  object** (scalar, per-station components, orientation `benchmark_minus_model`, weighting
  `equal_station`, the sign-convention sentence carried machine-readably); the **prediction
  hash receipt** consumed as a metric precondition; and the **transform-resolution shapes**
  (the `load_transform(transform_id)` resolver contract, `Transform`'s machine-readable
  target-touching declaration, the inversion-lineage field on `Prediction`).

The one test module scoped here is **`tests/test_common_masks.py`** (Q9 = C): WS-16's mask
evidence plus the matched-window assertion at the comparison boundary (TA-11's phrase), with
three negative controls — a pairwise mask attempt **fails**, mismatched window lengths
**fail**, a recomputed mask with a different ID **fails**. Its design is specified;
**no module is created** — G-09 is not signed.

### Each answer, one line

| Q | Answer | Design consequence |
|---|---|---|
| 1 | D | The inverse mechanism is a permitted `src/evaluation` → `src/features` import edge with a `load_transform(transform_id)` resolver; the target-touching status is stated explicitly for every configuration and declared machine-readably on `Transform`; an unresolvable `transform_id` **raises** and a resolved inverse must round-trip on a fixture. The `component-dependency.md` row is recorded as an amendment owed |
| 2 | C | This unit's half of BLK-08 is authored here; the joint contract is drafted complete in `business-rules.md`, the co-owner's half marked pending adoption; one gate decision over a complete text |
| 3 | C | `ABL-DIFF`'s inverse-before-metric rule is enforced at the boundary every caller crosses — metric entry points refuse transformed-space input — and the applied inverse is stamped on the `Prediction`'s transform lineage, with the un-inverted-`ABL-DIFF`-reaches-a-metric **raise** as the negative control |
| 4 | C | `07`'s half of the eighth amendment is owned: every `Prediction` entering a comparison carries non-`None` stamps, all members agree on `partition_id`, the mask carries the stamps too, and mismatch, absence or wrong-mask each **raise** — with the B-01/C-01 stamping stated, since `06` never sees them |
| 5 | D | Comparison-set membership is declared configuration in `experiment.yaml`, checked exactly (missing, extra or duplicate member **raises**); two sets proposed for gate confirmation — primary {M-01, M-02, M-03, M-06, B-01}, GIM {M-06, C-01}, never merged silently; plus the freeze mechanics: deterministic `mask_id`, per-station row counts, once-only registration, the registered set inside the G-05 frozen bundle (FR-P1-05-17) |
| 6 | D | The estimand is an ordered executable contract with the mask precondition (an unregistered mask **raises**); the result object carries orientation, weighting and the sign-convention sentence machine-readably; negative controls: an inverted orientation and a pooled row-weighted aggregation each **fail** on fixtures with known answers |
| 7 | D | Hash-before-metrics is a checked precondition (receipt present, file re-verified, timestamp precedes); December reads arrive only through `open_restricted`; the DEC mask asserts the scored set is exactly **2–31 December** with the first 24 h excluded and counted, a 1 December row **raises**; and the boundary is stated in both directions — this unit performs no pre-G-05 December read of any kind, the coverage audit being `inventory-and-registry`'s |
| 8 | D | Completeness is guaranteed upstream — the run refuses to emit a results artifact with any declared primary member's metric missing; the per-benchmark `beats_model` flag gives FR-P1-05-20's disclosure a field to assert against; the spatial-representativeness sentence and `gim_network_overlap_flag` are emitted by the comparison-producing path itself, R-60's pattern |
| 9 | C | `test_common_masks.py` is scoped as masks plus the matched-window assertion, with the three negative controls; the WS-13 §16 evidence-column clarification goes to the gate as one complete proposal for the owner to route through Vision §15.2 or decline |

### The blockers

- **BLK-08 (owned here)** — Questions 1–3 author this unit's half. Per Q2 = C, the joint
  contract is drafted **complete** in this unit's `business-rules.md`: both halves stated as
  one named, citable statement; this unit's half binding now; the co-owner's half — the
  persisted fitted state, the resolver, the target-touching declaration — explicitly marked
  **pending its owner's adoption**, so `features-and-splits`' receipted artifacts are not
  edited. Raised at the gate as **one decision** over a complete text. **BLK-08 is not
  closable on this unit's artifacts alone**: it remains an exit condition on stage 3.1 for
  both owners until the co-owner adopts its half.
- **BLK-03 ↓, BLK-04 ↓, BLK-09 ↓ (inherited)** — exit conditions inherited here, **not
  closed by anything in this file**; this unit may not complete or exit 3.1 while any
  contract is unapproved, and no implementation may proceed while they stand.

### The figures, derived not carried

- **4 owned files** — counted from § 9's `Owns` list: `src/evaluation/masks.py`,
  `src/evaluation/metrics.py`, `scripts/07_evaluate_and_report.py`,
  `tests/test_common_masks.py`.
- **4 requirements, 2 untested** — read from the story map's rows, the two upstream artifacts
  agreeing: FR-P1-04-7 (WS-16, TA-11), **FR-P1-05-7** (no acceptance row),
  **FR-P1-05-17** (no acceptance row), NFR-FAIR-01 (WS-16, TA-11).
- **Acceptance rows** — **WS-16 primary** (1 row); **TA-11 and TA-18 supporting** (2 rows).
- **Comparison sets** — primary **{M-01, M-02, M-03, M-06, B-01}** and GIM **{M-06, C-01}**,
  going to the gate as a **scientific confirmation, not a default** (Q5's option C limb; a
  student/supervisor-owned choice this stage proposes and does not make).
- **The scored December set** — **2–31 December, 30 days** (FU-7 = A, ruled 2026-08-26),
  first 24 h excluded and counted; encoded in the DEC mask's range assertion (Q7).

### What is NOT decided here

- **No scientific value.** Where an answer touches one — Question 5's membership, Question
  7's scored set — the value is either already frozen (FU-7 = A) or expressly routed to the
  gate; nothing in the artifacts fixes a constant, a threshold or a membership on its own
  authority.
- **No module creation.** G-09 is not signed; `tests/` holds three modules, none this
  unit's, and `src/` and `configs/` are absent. The artifacts specify design only.
- **Two gate items are decisions, not defaults**: the comparison-set membership confirmation
  (Q5) and the WS-13 §16 evidence-column clarification (Q9) — each presented as one complete
  proposal the owner may adopt, route through Vision §15.2, or decline.

### Assumptions and open questions, summarized

- **Assumptions carried into the artifacts**: rule numbering opens at R-103 with the
  R-83…R-89 gap flagged; the `src/evaluation` shapes beyond the four approved boundary calls
  are intra-package and this stage's to specify, with Q1's dependency row and Q5's
  `experiment.yaml` membership named as the only two surfaces exceeding that grant; this unit
  designs `masks.py` and `metrics.py` only (`vector_block_bootstrap` and
  `count_storm_events` belong to siblings); B-01/C-01 are producible as `Prediction`s with
  generated-not-trained provenance, stamped per Q4's contract.
- **Verification obligations owned here** — the checks this design must prove: the
  round-trip inverse control; the un-inverted-`ABL-DIFF` raise; the mismatched/absent-stamp
  and wrong-mask raises; membership exactness, once-only registration and stable `mask_id`
  with the pairwise control; the orientation and weighting fixtures and the unregistered-mask
  raise; the hash-receipt precondition, the 2–31 December range assertion and the chokepoint
  routing; the completeness refusal, `beats_model` field and disclosure presence tests;
  `test_common_masks.py`'s three negative controls.
- **Governance dependencies owned outside**: BLK-03's, BLK-04's and BLK-09's limbs at their
  owning units; the co-owner's adoption of BLK-08's other half; the comparison-set
  membership confirmation (student/supervisor); any WS-13 §16 change (Vision §15.2);
  acceptance rows for FR-P1-05-7 and FR-P1-05-17 (stage 3.2); G-05's freeze of the evaluation
  code this stage designs, whose timestamp ordering this stage requires but cannot
  manufacture; the AGPLv3 distribution question.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The receipt is recorded, the three design artifacts are generated on these answers, and the adversarial review follows.

- Request changes
   > **Impact**: Nothing is recorded or generated; state what to change and the summary is re-presented.

> **💡 Recommendation**: **Looks correct** — every figure above is derived from this file's own sources rather than carried, every scientific choice is either already frozen (FU-7 = A) or routed to the gate as a confirmation, and all four blockers stay open exactly as the register rules them.

[Answer]: Looks correct

---

## Consolidated Summary Confirmation

**What changed in this unit since the last receipt.** Stale `foundation`-fourteen claim swept at three sites; **FR-P1-05-7 and FR-P1-05-20 acceptance rows approved under D-32**, so R-108 and R-110 gain the §16/§19 rows they lacked; **G-09 signed (D-31)**.

**Governance recorded this pass.** **D-29** (`dataset_version` = first 12 hex of
`content_hash`, verify-on-write), **D-30** (`.dst_summary.json` relocation, performed and
hash-verified), **D-31** (**G-09 signed**, with its §18.3 preconditions recorded as
**unmet**), **D-32** (**all eight Vision §15.2 acceptance rows approved**, board option 1,
none deferred). Change records: `CHANGE_RECORD_2026-08-28_G09_signed.md`,
`CHANGE_RECORD_2026-08-28_dst_summary_relocation.md`.

**Execution evidence, and its exact limits.** Python **3.11.16** — the governed pin (TE §8.1, TC-03d) — obtained via `uv` and used to run the suites: **277 passed, 0 failed, 0 errors, 2 skipped** (both skips justified and recorded). Evidence packaged at `artifacts/exec_evidence/` with a SHA-256 manifest. **The runner was not pytest**: PyPI is unreachable in this environment, so a harness providing the pytest API surface was used; it has no plugins, no conftest and no assertion rewriting, and it **errors** rather than passes on an unsupported fixture. Two defects were found *by execution*: the access log could not evidence its own ordering (fixed — the guard now stamps `logged_at_utc` itself; 37 rows, 37 distinct monotonic instants), and the one-door assertion **failed against a file this session had just written**, which is the behaviour R-28 specifies.

⚠ **What is still NOT discharged, and this receipt does not claim otherwise:** TA-15, WS-18 and TA-18 have passing tests against **current** code, but their acceptance rows are discharged only at their own gates; `aws_ai_dlc_preflight_report` does not exist; `configs/` and the §18.3 zero-TBD preflight are unbuilt; and **D-31 records G-09's own preconditions as unmet**. Stage 3.1 remains **FAIL** and no board has passed it.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: Receipt recorded, this unit's artifacts re-saved, and a fresh adversarial review dispatched against the post-execution state.

- Request changes
   > **Impact**: Nothing recorded for this unit; name what to change and it is corrected before any receipt is taken.

- Other (please specify)
   > **Impact**: Depends on what you specify.

> **💡 Recommendation**: **Looks correct** — every claim above is either a recorded decision, a hash-verified act, or a test result from a run whose runner limitations are stated; nothing here asserts a gate is discharged.

[Answer]: Looks correct
