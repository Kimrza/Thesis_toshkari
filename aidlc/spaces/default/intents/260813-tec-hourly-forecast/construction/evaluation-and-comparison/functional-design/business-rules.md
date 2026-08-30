# Business Rules — `evaluation-and-comparison`

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

**Unit** `evaluation-and-comparison` · **Kind** `library` · **Complexity** M ·
**Deployment** standalone · **Depends on** `models-and-baselines`, `external-products`

The prohibitions this unit enforces, each with what it rejects, what it raises, and the
negative control that proves the rejection happens.

**This project's affirmed methodology is a negative control paired with every hard rule** —
a test that proves the violation is *caught*, not only that the happy path works.

**Every rule here guards a reported number.** This unit computes the confirmatory estimand,
builds the one mask every comparison shares, and performs the G-06 locked evaluation — the
one event that can never be re-run. Its violations do not crash a pipeline; they print a
wrong thesis conclusion with a plausible sign.

**Rule IDs continue the single sequence.** `foundation` R-01…R-17, `governance-guards`
R-18…R-29, `acquisition` R-30…R-43, `inventory-and-registry` R-44…R-53, `external-products`
R-54…R-63 (plus R-54a), `target-standardization` R-64…R-73, `features-and-splits` R-74…R-82
(plus R-76a), `models-and-baselines` R-90…R-102 — so this unit opens at **R-103**. **The
gap between `features-and-splits` and `models-and-baselines` has narrowed to R-85…R-89**
(re-derived 2026-08-28: `features-and-splits` allocated R-83 and R-84 in its same-day
re-entry, so its range now runs R-74…R-84), **and the residual gap is observed, not explained,
and is flagged at the gate**: if it was a reservation, or per-unit numbering was
intended, say so there and these artifacts renumber. This is the numbering assumption stated
in `functional-design-questions.md`.

**BLK-08 is owned here and is an exit condition on this stage for both owners.** R-103
below is the joint contract drafted complete (Q2 = C): this unit's half binding now, the
co-owner's half explicitly marked **pending its owner's adoption**. **BLK-03 ↓, BLK-04 ↓ and
BLK-09 ↓ are inherited open exit conditions** — nothing in this file closes any of the four,
and **no implementation may proceed while any stands** (`GOV-2026-08-22-REM-01` Rec 2,
extended to BLK-08/BLK-09 on 2026-08-23). **G-09 is not signed** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.: no module named here may
be created.

> ### Remediated 2026-08-28 — governance report `GOV-2026-08-28-FD-01`, verdict **FAIL**
>
> Six owner-ruled changes, each carrying a dated note at its own site and every superseded
> reading preserved in place. **No blocker closed, no gate signed, no scientific value
> decided.**
>
> | Rec | Rule(s) touched | What changed |
> |---|---|---|
> | **7**, narrowed to `ABL-DIFF` on **D-27**'s strength | **R-103**, R-104, § Amendments owed | D-27 cited (it was cited **0** times across all four artifacts); the primary path stated to need **no** inverse; the resolver narrowed to `load_inverse -> Inverse`; the round-trip control relocated into `src/features`; the mechanism scoped to `ABL-DIFF`; the import edge recorded as **owed and a gate item, not approved**. |
> | **8** | **R-105**, `domain-entities.md` § 8 | The `partition_id`-mismatch limb now raises **`PartitionError`**, matching R-92; `PartitionError` added as R-01's **fifteenth**; the discriminating rule stated. **This was the standing Major of the 2026-08-27 pass and is now fixed, not merely disclosed.** |
> | **19** | **R-106**, R-107, R-110, R-111 | A **third declared comparison set `{M-04, M-05, M-06}`** with its own mask, making Vision §2.4 tier 3 implementable; no mechanism change, confirmed rule by rule. |
> | **35** | **R-108** | `EstimandResult` gains `phase_id`, `source_id`, `target_definition_id`, `partition_id`, copied from the registered mask at construction, with a control. |
> | **16** (this unit's half) | **R-107** limb 6 | The mask **exposes** `mask_id`, `feature_set_id`, per-station surviving row counts, exclusion counts and the scored-window statement (**D-28**) for the reporting unit to print and never restate. |
> | **41** | **R-110** limb 3 | The GIM overlap disclosure is **re-keyed to "a GIM comparison artifact exists"**, with the audit's timestamp asserted to precede comparator generation. |
>
> **Counts re-derived on 2026-08-28 and printed at their sections, never carried:** rules
> **10** (R-103…R-112, unchanged); negative controls **31** (was 29: −1 relocated, +3 new,
> with number (2) vacated); amendments owed **7 across 5 units** (this unit still owes exactly
> **1**, narrowed in content and now recorded as a gate item; the movement from "6 across 4" is
> **entirely in the co-owner's row**, which changed on disk mid-remediation); requirements
> **4**, **2** untested (unchanged).
>
> **Two facts changed under this remediation while it ran, and are corrected rather than left
> standing** — see the boxes at R-103 and § Amendments owed. (a) `features-and-splits`
> **authored its narrowed half B as R-84** at 02:09–02:21 on 2026-08-28, so the zero-grep
> finding this unit recorded at the start of the pass is now false, and **the two halves agree
> limb for limb**. (b) Its § Amendments owed moved from `0` to `1` (its R-83 BLK-09 package),
> taking the shared total to **7 across 5**.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 9 — the `Owns` list (4 files), the boundary (the IRI/GIM allowlist reach, "not the sole permitted importer"), the 4 requirements, the implementation notes; **BLK-08** with its Required-resolution field and three candidate mechanisms; **BLK-03/BLK-04/BLK-09** with the exit-condition ruling; the § Roll-up row naming `ABL-DIFF` and every TECU-denominated quantity as the blocked scope.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Table 1's four requirement rows, Table 2's WS-16/TA-11/TA-18 rows, § Per-unit coverage summary (4 / 2 / WS-16 / TA-11, TA-18), § Cross-unit responsibilities (the pre-G-05 coverage audit is `inventory-and-registry`'s), § Open verification gaps (BLK-08's row; WS-13's evidence departure, deferred to this stage).
- `../../../inception/requirements-analysis/requirements.md` — FR-P1-04-7, FR-P1-05-7, FR-P1-05-17, NFR-FAIR-01; consulted for context: FR-P1-05-6 (`ABL-DIFF` and the five predeclared ablations), FR-P1-05-9 (the three difficulty controls), FR-P1-05-12 (hash-before-metrics, write-once detection), FR-P1-05-20 (the abstract-level disclosure).
- `../../../inception/application-design/component-methods.md` — § `src/evaluation` (`build_comparison_mask` and its `FairnessError`, `paired_loss_differential`); § `src/models` (`Prediction` with `partition_id`/`transform_id`, `three_seed_mean(..., expected_seeds)`, the `inverse_transform` paragraph BLK-08 was registered against); § `src/data/locked_test.py` (`AccessRecord`, `open_restricted`, log-then-read); § Depth (intra-package shapes are this stage's) and the closing note carrying the two unresolved signature gaps to this stage.
- `../../../inception/application-design/services.md` — `07_evaluate_and_report.py`'s row (reads predictions carrying `partition_id`/`transform_id`, benchmark, mask; writes metrics, bootstrap intervals, breakdowns, figures), § Stage entry contract, the heaviest-CPU note, the derived `experiment_registry.csv` row.
- `../features-and-splits/functional-design/` — R-74 (the identity check and the one enumerated `REFIT` → `DEC` `score` exception), the `Transform`/`FeatureBundle` shapes, **FU-7 = A** (the G-06 locked test scores **2–31 December, 30 days**, first 24 h excluded and counted), § Amendments owed. **Re-read twice on 2026-08-28, because it changed between the two reads:** at the start of this remediation it carried *"5 + 0 = 5 across 3 units"* and zero hits for `inverse`/`BLK-08`/`TECU`/`ABL-DIFF`; after its own re-entry (mtimes 02:09–02:21) it carries **R-83** (the BLK-09 `train_start` package) and **R-84** (BLK-08 half B, narrowed to `ABL-DIFF`, exposing `load_inverse(transform_id) -> Inverse`), and its § Amendments owed reads **`5 + 1 + 1 = 7 across 5 units`**. **The later read is the one this artifact uses**, and the superseded read is preserved at R-103's correction box rather than deleted.
- `../models-and-baselines/functional-design/business-rules.md` — R-90 (`06`'s stamp refusal, closing the eighth amendment's `06` half "and only `06`'s"), R-91 (`three_seed_mean`), R-92 (provenance agreement; the (`station`, `interval_start_utc`) alignment key); the open item "`07`'s half of the eighth amendment is UNOWNED", raised at its gate for this unit.
- `../external-products/functional-design/business-rules.md` — R-55 (the amendment basis: **5 across 3 units**, boundary contracts only), R-56 (the transitive allowlist scan; `src/evaluation/` is a path grant owned by three units), R-60 (the emitted-sentence pattern; `gim_network_overlap_flag`; C-01 labelled generated, not trained), R-62 (Dst diagnostic-only), R-63 (driver series time-indexed only).
- `../governance-guards/functional-design/business-rules.md` — R-25 (the access log is durably appended **before** the December read begins), R-28 (one path into the restricted root; BLK-07 is not this design's to close).
- `../foundation/functional-design/business-rules.md` — R-01 (`IntegrityError` is the single catchable base; every project exception derives from it, and so does *"any future integrity-related exception"*; the cross-unit obligation that each raising unit declares its exceptions as subclasses), R-10's stage-entry catch; § Stage entry contract (the six ordered steps `07` performs). **Its enumeration reads "all fourteen" on disk as of 2026-08-28; `PartitionError` is its fifteenth on the owner's Recommendation 8 ruling, and that amendment is `foundation`'s to write** — see R-105's correction box and `domain-entities.md` § 8.
- `aidlc/spaces/default/memory/project.md` § Mandated/Forbidden — the comparison-wide mask rule (NFR-FAIR-01, TC-16), the estimand (Vision §2.3, TE §1.3), IRI evaluation-time-only (NFR-IRI-01), GIM evaluation-time-only plus the overlap disclosure (TE §5.2), the three difficulty controls co-reported, the beats-the-LSTM disclosure, the spatial-representativeness statement (TEC-06), G-06 hash-before-metrics, `ABL-DIFF` inverse-to-TECU, the `phase_id`/`source_id`/`target_definition_id` stamp.
- Workspace inspection, 2026-08-26: `tests/` holds three modules, none this unit's; `src/` and `configs/` absent.
- `functional-design-questions.md` (**Q1 through Q9**, answered), `business-logic-model.md`, `domain-entities.md`.
- **Added 2026-08-28 for the `GOV-2026-08-28-FD-01` remediation:** `governance/reviews/GOV-2026-08-28-FD-01.md` Recommendations **6, 7, 8, 16, 19, 35, 41** with their owner rulings; `evidence/DECISIONS.md` **D-27** (2026-08-24 — the primary target is not transformed; the inverse obligation is `ABL-DIFF`'s alone) and **D-28** (2026-08-28 — the G-06 locked-test scored set is 2–31 December 2022, 30 days), both read in full; `PreFlight/vision_document(3)(2)(2).md` §2.4 tier 3 (line 172), §8.4's model table (M-04 ridge, M-05 direct RF, M-06 LSTM, lines 774–776) and **§8.9's matched-learned-model clause naming M-04 and M-05** (line 853 — the report cites §8.9 at line 845, which is the section heading; the clause itself is at 853); `PreFlight/…Technical_Environment…md:400` and `vision_document…:751`, the byte-identical `| Locked test | — | — | December 2022 only |` rows D-28 discloses; `requirements.md` **FR-P1-04-9** (criterion: *"overlap audit all exist"*); `component-methods.md:595-600` (*"`apply_transforms` is removed"*) and `:773-781` (the no-`src/features`-edge statement), `:894` (the fourteen-exception `[assumption]`); `component-dependency.md`'s matrix row for `src/evaluation` and its closing note; `models-and-baselines/…/business-rules.md:102-104` (R-92's two-exception split); `statistical-inference/…/business-rules.md:63-65` (R-113 precondition 2); `foundation/…/business-rules.md` R-01 (still "all fourteen" on disk) ⚠ **SWEPT 2026-08-28 on the resume pass — this disk-state claim is SUPERSEDED.** `foundation` R-01 **has been amended** and now reads **fifteen**, with `PartitionError` promoted into the enumeration, the count restated as **derived and printed** rather than carried in prose, and `InverseTransformError` **explicitly disposed** — not a sixteenth, riding R-01's *"any future integrity-related exception"* clause, on the stated ground that the two units raising it agree on its condition and meaning, so nothing needs reconciling. Verified at `foundation/functional-design/business-rules.md` R-01 (the amendment row, the superseded-wording box, and the `InverseTransformError` box). **The dependency this sentence recorded is discharged; any open item stated alongside it is NOT** — see the sentence it accompanies.; `external-products/…/business-rules.md` R-60's Constraint and R-55's derivation at `:26`/`:181`/`:613`; `features-and-splits/…/business-rules.md:789-799`.

---

## R-103 — The BLK-08 joint transform-resolution contract, narrowed to `ABL-DIFF` (one statement, two halves)

> ### ⚠ NARROWED 2026-08-28 — governance report `GOV-2026-08-28-FD-01` **Recommendation 7**
>
> Ruled by the project decision owner as **Recommendation 7's option 1, narrowed to
> `ABL-DIFF` on D-27's strength**. Five things changed, and the superseded text is preserved
> verbatim in the box at the end of this rule.
>
> 1. **D-27 is cited.** `evidence/DECISIONS.md` **D-27 (2026-08-24)** — *"The primary target
>    is not transformed; the inverse obligation is ABL-DIFF's alone"* — **froze** on
>    2026-08-24 the very fact this rule was carrying as a status "stated as a recorded fact
>    rather than an inference", three days before these artifacts were authored. **Derived
>    2026-08-28 before asserting it**: `grep -c "D-27"` over this unit's four artifacts =
>    `business-logic-model.md` 0, `business-rules.md` 0, `domain-entities.md` 0,
>    `functional-design-questions.md` 0 — **zero citations of a decision that had already
>    settled the question this rule reopened.**
> 2. **The resolver narrows** from `load_transform(transform_id) -> Transform` to
>    **`load_inverse(transform_id) -> Inverse`, exposing only `inverse(frame)`**. The board
>    found that returning `Transform` reconstitutes `apply_transforms(frame, transform)` as
>    `load_transform(id).apply(frame)` — the exact surface ADR-11 removed at
>    `component-methods.md:595-600` (*"**`apply_transforms` is removed.** A function that
>    applies a fitted transform to an arbitrary frame **is** the hole"*) — **one package away
>    from the frozen mask and the G-06 path**. R-103's own earlier failed-refutation section
>    examined whether the *edge* contradicts M6; it did not examine whether the *object the
>    edge carries* re-opens the apply hole.
> 3. **The round-trip control relocates into `src/features`**, where `apply` is visible. It
>    cannot be executed from a package that can no longer see `apply` — which is the point of
>    (2). Former control (2) is therefore **vacated here and hosted by half B**; § Negative-control
>    count re-derives the total.
> 4. **The whole mechanism is scoped to `ABL-DIFF` only.** D-27: the reading *"no longer
>    requires a general `src/evaluation` → `src/features` route for the primary path."*
> 5. **The import edge is recorded as an amendment owed AND a gate item, never as approved.**
>    D-27, verbatim: *"**No import-boundary change is authorised by this decision.** The §12
>    rule and its allowlist are untouched."* `component-dependency.md`'s `src/evaluation` row
>    carries `—` for `features` (absent, not forbidden) and its closing note reads *"none
>    should be added without the design naming the lookup"* — this rule names the lookup and
>    asks; it does not grant.

**Rule (Q1 = D, Q2 = C, as narrowed).** This is **the joint contract the BLK-08 register
requires**, drafted complete as one named, citable statement. Downstream artifacts cite
**R-103**; they do not restate it — a restated contract in four places drifts.

**The frozen fact, no longer an open premise: D-27 (2026-08-24).** The **primary
configuration's train-only transform does not touch the target**: it acts on
target-**derived input features**, and **the target itself remains raw TECU**. `ABL-DIFF` is
**the sole configuration that transforms the target**. This is a *reading of already-frozen
text* — TE §7.2's `ABL-DIFF` row, whose **Primary remains** column reads **"Raw TECU"**, and
TE §6.2's normalization column, which scopes the train-only standardization to
**`vtec_lag_1h/2h/3h/24h` and `vtec_seq_24`** — lagged values used as **predictors**, not the
target being predicted. **No scientific value is set, changed or reinterpreted by citing it
here.**

**The consequence D-27 requires stated explicitly, so the `ABL-DIFF` obligation is visibly
satisfied rather than silently assumed:** **the primary path needs no inverse transform.**
Model output is already in raw TECU, so **the paired loss differential (R-108), the vector
time-block bootstrap interval (`statistical-inference`) and the practical-relevance
threshold are computed on the quantity the model emits.** No inverse is resolved, no edge is
traversed and no round-trip is checked on the confirmatory path — which is why the mechanism
below is `ABL-DIFF`'s alone.

**D-27's own limitation, carried not softened:** this is a reading taken before any code
exists. If `code-generation` or `build-and-test` finds a model path that scales the target
contrary to it, that is **a contradiction to surface**, not a licence to adjust the target
contract (TE §18.2's absolute rule). The machine-readable target-touching declaration in
half B is what makes that contradiction *catchable* rather than merely reportable: a primary
transform declaring itself target-touching is refused at every metric entry point unless
inverted (R-104).

**The mechanism, scoped to `ABL-DIFF` only: an `src/evaluation` → `src/features` import edge
that is PROPOSED, not held.** `features-and-splits` persists each fitted `Transform` and
exposes **`load_inverse(transform_id) -> Inverse`**, where `Inverse` exposes **only**
`inverse(frame)` — **no `apply`, no fitted-state access, no route back to a forward
transform.** `src/evaluation` resolves it by the identity ADR-11 already persists
(`Prediction.transform_id`). A `features` → `evaluation` direction is **not available** (it
would invert the dependency); this is the direction the register itself contemplates. The
§12 import-boundary rule is unaffected — the `iri.py`/`gim.py` allowlist constrains a
different pair of modules. **The matching `component-dependency.md` row is an amendment owed
and a gate item** (§ Amendments owed derives the total): **nothing here authorises the edge,
and stage 3.5 may not treat it as approved.** Until it is both change-recorded and ruled at
the gate, **`ABL-DIFF` has no executable inverse path** — which is BLK-08 remaining open,
stated as a fact rather than deferred.

| Half | Owner | Status | Content |
|---|---|---|---|
| **A — resolution and use, `ABL-DIFF` only** | **this unit** | **binding now** | For a target-touching configuration — **`ABL-DIFF`, and no other** — `src/evaluation` obtains the inverse via `load_inverse(transform_id) -> Inverse` and calls `Inverse.inverse(frame)`, producing a **new** `Prediction` whose transform lineage records the inversion (R-104). An unresolvable `transform_id` **raises `InverseTransformError`**. No inverse arithmetic is reimplemented in `src/evaluation` — one copy, owned where the fit lives (§14's one-copy rule). **`src/evaluation` obtains no object exposing `apply`**, so `apply_transforms` is not reconstitutable across the edge. |
| **B — persistence, declaration and the round-trip** | `features-and-splits` | **AUTHORED by its owner 2026-08-28 as its R-84**, agreeing with half A limb for limb; **adoption of the joint contract is still the gate's to rule** | Each fitted `Transform` is persisted retrievably by `transform_id`; **`load_inverse(transform_id) -> Inverse` is exposed from `src/features` and returns an inverse-only object**; `Transform` declares its target-touching status **machine-readably** (`touches_target: bool`, name indicative); and **the round-trip control lives here** — `inverse(apply(x))` within the declared fixture tolerance, hosted in `src/features` because that is the only package where `apply` is visible. |

> ## ⚠ HALF B NOW EXISTS — AND BOTH HALVES AGREE. BLK-08's MECHANISM LIMB STILL DOES NOT CLOSE HERE.
>
> **Correction of fact, recorded rather than quietly absorbed (2026-08-28).** Earlier today
> this box asserted, on a grep run at the start of this remediation, that the co-owner's four
> artifacts carried **0** hits for `BLK-08`, `inverse`, `TECU` and `ABL-DIFF` and that
> `load_inverse` returned **0** across the whole `construction/` tree. **That was true when it
> was run and is now false.** `features-and-splits` authored its narrowed half **during this
> remediation** — file mtimes 2026-08-28 02:09 (`business-rules.md`), 02:15
> (`domain-entities.md`), 02:21 (`business-logic-model.md`) — and the counts re-derived after
> it landed are: `BLK-08` 17 / 13 / 15, `inverse` 16 / 11 / 17, `ABL-DIFF` 12 / 9 / 10,
> `load_inverse` 6 / 4 / 9 across its `business-rules.md` / `business-logic-model.md` /
> `domain-entities.md`. **The stale zero is corrected here rather than left standing**, per
> `project.md` § Way of Working ("verify a fact independently before handing it to another
> reviewer as established input").
>
> **The co-owner's half is `features-and-splits` R-84 — "BLK-08 half B, narrowed to
> `ABL-DIFF`" — and it agrees with half A on every limb**, checked against its text rather
> than assumed:
>
> | Limb | R-84 (co-owner) | R-103 half A/B (here) | Agree? |
> |---|---|---|---|
> | Persistence | fitted `Transform` retrievable by `transform_id` | same | **yes** |
> | Resolution | `src/features` exposes **`load_inverse(transform_id) -> Inverse`**; `Inverse` exposes **`inverse(frame) -> DataFrame` and nothing else** | same | **yes** |
> | Declaration | `touches_target: bool`, machine-readable, so D-27's reading is *"checked, not trusted"* | same | **yes** |
> | Round trip | `inverse(apply(x)) == x` within the fixture tolerance, **hosted inside `src/features`** where `apply` is visible | same; former control (2) vacated here | **yes** |
> | The import edge | *"owed and UNAPPROVED, not adopted"*, `ABL-DIFF` path only, D-27 withheld authorisation *"in terms"* | same | **yes** |
>
> **The divergence R-84 raised is resolved by this edit, not by assertion.** R-84 records a
> *"Divergence from R-103 half A, raised rather than resolved"* — that half A *"names
> `load_transform(transform_id) -> Transform`"* while half B narrows to `load_inverse` /
> `Inverse` — and routes the reconciliation to the gate because, when R-84 was written,
> `evaluation-and-comparison` was *"terminal-READY under a frozen receipt and this stage does
> not edit it."* **A redo jump has since cleared that freeze, and half A above now reads
> `load_inverse(transform_id) -> Inverse`.** The two halves therefore no longer diverge; what
> reaches the gate is one reconciled contract rather than two texts to arbitrate.
>
> **What still does not close.** The register makes the resolution joint and rules that
> *neither owner may exit 3.1 without the contract*. Two things remain outside both owners:
> **the gate's adoption ruling on the joint contract**, and **the import edge's authorisation**
> — which **D-27 expressly withholds** (*"No import-boundary change is authorised by this
> decision"*) and which `component-dependency.md` still carries as `—`. Until both exist,
> **`ABL-DIFF` has no executable inverse path** and **BLK-08's mechanism limb remains an open
> exit condition on stage 3.1 for both owners.** Its **premise limb closes for the primary
> path** on D-27: the primary configuration does not touch the target, so the primary path owes
> no inverse and exercises no edge — the same two-limb split R-84 records. **This stage edits
> no other unit's files.**

**Negative controls.** (1) A `Prediction` whose `transform_id` resolves to no persisted
inverse → **`InverseTransformError`**, naming the identifier and the registry searched.
**(2) — VACATED HERE.** The round-trip control (`inverse(apply(x))` differing from `x` beyond
the declared fixture tolerance in `tests/fixtures/<fixture_id>/fixture_manifest.yaml` §15.2;
no tolerance value is decided here) is **relocated to half B in `src/features`** per
Recommendation 7, because `src/evaluation` no longer obtains an object exposing `apply` and
therefore cannot execute it. The obligation is undiminished; its host changed, and it is
**counted at the co-owner, not here**. Control numbers (1) and (3)–(29) are unchanged so
every existing cross-reference still resolves; the number **(2) stays vacated** rather than
being reused.

**Acceptance.** ⚠ No row — BLK-08 closes at the register, not at a checklist row.

> ### Superseded text, preserved verbatim (2026-08-27 revision, narrowed 2026-08-28)
>
> *"**The mechanism: a permitted `src/evaluation` → `src/features` import edge.**
> `features-and-splits` persists each fitted `Transform`; `src/evaluation` resolves it by the
> identity ADR-11 already persists (`Prediction.transform_id`) and calls
> `Transform.inverse(frame)`. … The matching `component-dependency.md` row is **an amendment
> owed**"*; half A's *"obtains the fitted transform via `load_transform(transform_id) ->
> Transform` and calls `Transform.inverse(frame)`"*; half B's *"the resolver
> `load_transform(transform_id) -> Transform` is exposed from `src/features` … `Transform.inverse`
> round-trips its own `apply` within the declared fixture tolerance"*; and the paragraph
> headed *"**The primary configuration's target-touching status, stated as a recorded fact
> rather than an inference (the register's "states first" question).**"*, which grounded the
> features-only status in TE §7.2 and §6.2 **without citing D-27, which had already frozen
> it.** The grounding was right and the authority was missing.

## R-104 — Inverse-before-metric is enforced at the boundary every caller crosses

**Rule (Q3 = C).** Every metric entry point in `src/evaluation/metrics.py` — the estimand
included — **refuses transformed-space input**: it raises **`InverseTransformError`** unless
the `Prediction`'s resolved transform is declared **non-target-touching**, or the
prediction's transform lineage records that **the inverse has been applied**. `project.md`
§ Mandated: *"`ABL-DIFF` inverse-transforms to absolute TECU before any metric"* — this rule
makes "before any metric" a **checked precondition**, not a remembered call order in
`scripts/07_evaluate_and_report.py` (§7 makes scripts orchestrators precisely so governed
checks do not live in them; a notebook calling `paired_loss_differential` directly must hit
the same wall).

**The inversion is stamped, not remembered.** Applying `Inverse.inverse` (R-103's narrowed
resolver) produces a **new** `Prediction` whose transform lineage records the inversion (the
lineage field is part of the R-103 amendment package) — the same stamp-not-memory principle
ADR-11 settled for the forward direction: *"the stamp has to travel the whole way."* "The
inverse was applied" is thereby a fact on the artifact.

**The primary path clears this boundary without invoking it (D-27, cited 2026-08-28 per
Recommendation 7).** Because the primary configuration's transform is features-only and the
target stays raw TECU, the primary `Prediction`'s resolved transform is declared
non-target-touching and the first disjunct of the rule is satisfied natively: **no inverse is
resolved and no edge is traversed on the confirmatory path.** `ABL-DIFF` is the one
enumerated configuration that reaches the second disjunct — which is exactly why R-103's
mechanism is scoped to it alone.

**B-01 and C-01 pass this boundary natively.** The benchmark and comparator predictions are
generated, not trained, in absolute TECU; their stamps (R-105) carry the reserved literal
`untransformed`, which reads machine-readably as target-space. A control that must **not**
fire: a B-01/C-01 `Prediction` stamped `untransformed` reaching a metric → **passes**.

**Negative controls.** (3) An un-inverted `ABL-DIFF` prediction reaching **any** metric →
**`InverseTransformError`** — the named instance of the rule, and the control the blocked
scope (*"`ABL-DIFF` and every TECU-denominated quantity"*) exists for. (4) Any
`Prediction` whose resolved transform is target-touching and whose lineage records no
inversion, at any metric entry point → **`InverseTransformError`**.

**Acceptance.** ⚠ No row — FR-P1-05-6's criterion is `UNTESTED`; the controls above are the
bar until stage 3.2 proposes a row under Vision §15.2.

## R-105 — `07`'s half of the eighth amendment: the stamp refusal at this unit's boundary

**Rule (Q4 = C).** `features-and-splits` FU-4 = D obliges **`06` and `07`** to refuse
unstamped or wrongly-stamped inputs; `models-and-baselines` R-90 closed `06`'s half *"and
only `06`'s"* and raised the rest at its gate. **This unit owns `07`'s half, at the object
`07` actually receives — `Prediction`s, not frames:**

1. Every `Prediction` entering a comparison carries **non-`None`** `partition_id` and
   `transform_id`; absence **raises `LeakageError`**. An absent stamp is not a disagreement
   between two declarations but the **absence** of one, and its named residual is the
   hand-assembled prediction — the information-flow case, which is why this limb keeps
   `LeakageError` and matches R-92's `transform_id`-disagreement-or-`None` limb. Limb 1 runs
   **before** limb 2, so a `None` `partition_id` is caught here and never reaches the
   mismatch test.
2. All members of one comparison **agree on `partition_id`**; a mismatch **raises
   `PartitionError`** — **the same exception R-92 raises for the same condition**, so the
   two consuming units' accounts of the eighth amendment now actually agree.
3. **The mask carries the stamps too**: the comparison mask records the `partition_id` and
   the **member `transform_id` set** it was built over, and scoring a `Prediction` against
   a mask built for a different partition **raises `FairnessError`** — the refusal extended
   across `07`'s own file-mediated handoff (mask built, then consumed), the same gap class
   FU-4 found between `05` and `06`.

**How B-01 and C-01 are stamped, since `06` never sees them.** The comparison-producing
path stamps them at generation: `partition_id` is the partition being scored (a fold's
validation month, or `DEC` for G-06), `transform_id` is the reserved literal
`untransformed` — non-`None`, and machine-readably native-TECU (R-104). Members of one
comparison therefore agree on `partition_id` while their `transform_id` values may differ;
the mask records the **set**.

**The amendment total is unaffected** — the stamp contract is counted once, by
`features-and-splits`; this rule records the landing site so all three accounts agree.

> ### ⚠ CORRECTED 2026-08-28 — `GOV-2026-08-28-FD-01` **Recommendation 8**; the standing Major of this unit's 2026-08-27 adversarial pass
>
> **Superseded text, preserved verbatim:** *"a mismatch **raises `LeakageError`** — mirroring
> R-92's provenance-agreement rule at this unit's boundary, so the two consuming units'
> accounts of the eighth amendment agree."* The claim was false in its own terms.
> `models-and-baselines` **R-92** reads, byte-checked 2026-08-28 at
> `construction/models-and-baselines/functional-design/business-rules.md:102-104`:
> *"`partition_id` disagreement or a training partition raises **`PartitionError`**;
> `transform_id` disagreement or `None` raises **`LeakageError`**."* This unit raised
> `LeakageError` for **both** limbs while claiming to mirror a rule that separates them — so a
> test asserting `pytest.raises(PartitionError)` would pass at `06` and fail at `07`.
>
> **The owner's ruling (Recommendation 8, option 1 with option 4's discriminating rule made
> explicit): `PartitionError` is promoted to `foundation` R-01's FIFTEENTH project-defined
> exception**, and the discriminating rule is fixed project-wide:
>
> | Condition | Exception | Why |
> |---|---|---|
> | A **declared-identity disagreement** — two members declaring different `partition_id`s | **`PartitionError`** | The declarations disagree; nothing has yet flowed. R-92 drew this distinction deliberately. |
> | A disagreement that **implies information flow** — `transform_id` disagreement, or a `None` stamp | **`LeakageError`** | A fit from one partition reaching another partition's rows is the leak itself. |
> | A member-versus-**mask** partition disagreement (limb 3) | **`FairnessError`** | Not a provenance disagreement among members but scoring against the wrong exam — the fairness class R-107 and `statistical-inference` R-113 already use, unchanged here. |
>
> **The `foundation` amendment is `foundation`'s to author, and it is not on disk yet.**
> Derived 2026-08-28: `foundation`'s `business-rules.md` R-01 still reads *"All fourteen
> project-defined exceptions"* and its enumeration still omits `PartitionError`
> (`grep "PartitionError"` over `foundation/functional-design/*.md` returns only three hits,
> all inside a preserved quotation of a *different* unit's R-96 verdict — none in R-01). This
> rule cites **R-01's amended enumeration** on the owner's ruling and **discloses that the
> amendment is pending at its owner**; no claim is made here that R-01 already reads fifteen.
>
> **This correction propagates downstream.** `statistical-inference` **R-113 precondition 2**
> imports R-105 *"as written"* and currently reads *"absence or mismatch **raises
> `LeakageError`**"* (verified 2026-08-28 at
> `construction/statistical-inference/functional-design/business-rules.md:63-65`). Under this
> correction its **mismatch** limb raises `PartitionError` while its **absence** limb keeps
> `LeakageError`. That edit is `statistical-inference`'s to make; it is raised at the gate
> here and **not made in another unit's files**.

**Negative controls.** (5) Members disagreeing on `partition_id` → **`PartitionError`**
(corrected 2026-08-28, Recommendation 8; superseded: `LeakageError`).
(6) A `Prediction` with an absent (`None`) stamp — a hand-assembled prediction, the exact
residual R-74 names — → **`LeakageError`**. (7) A `Prediction` scored against a mask whose
recorded `partition_id` differs from its own → **`FairnessError`**.

> **The 2026-08-27 pass's Minor finding on this control's R-74 citation is NOT applied and is
> quoted at the gate instead.** That reviewer asked for the specific R-74 sentence to be
> quoted, or *"the exact residual R-74 names"* softened. The owner's ruling covered
> Recommendation 8 (the Major above) and did not reach this Minor, and `project.md`
> § Corrections forbids applying an advisory finding on the strength of the finding alone —
> so the wording stands unchanged and the finding goes to the gate as gate input.

**Control that must *not* fire:** a comparison whose members all carry `(DEC, ...)` stamps
scored against the registered DEC mask → **passes**; that is the G-06 path.

**Acceptance.** Contributes to WS-16 and TA-11 (this unit's rows); module placement of
controls (5)–(7) is stage 3.2's verification planning.

## R-106 — Comparison-set membership is declared configuration, checked exactly

**Rule (Q5 = D, membership limb).** Each comparison set is **named in `experiment.yaml`
with its enumerated member IDs** (TC-03e: membership is a frozen scientific choice, not
code). The mask builder receives the declared set through `ConfigSnapshot` — the read side
is intra-package (§ Depth) — and **raises `FairnessError`** when the passed predictions do
not match the declared set **exactly**: missing member, extra member, or duplicate. The
approved signature's own check (*"detected by the caller passing fewer than the full
comparison set"*) thereby gains the input it compares against, which no artifact previously
defined.

**Three declared sets are PROPOSED for confirmation at the gate — a scientific choice this
stage may propose but not make (TE §18.3):**

- **primary** — {`M-01`, `M-02`, `M-03`, `M-06`, `B-01`}, carrying one mask;
- **GIM comparison** — {`M-06`, `C-01`}, its own set with its own mask, **never merged
  silently** into the primary: R-60's map-to-map framing and the overlap-audit condition
  make C-01 a differently-caveated comparison, and folding it in would shrink the primary
  scored set for a comparator that cannot validate the target.
- **tier-3 learned-model comparison** — {`M-04`, `M-05`, `M-06`}, its own set with its own
  mask (**added 2026-08-28 on the owner's ruling; see the box below**). `M-06` is the model;
  `M-04` (ridge on the shared flattened feature matrix) and `M-05` (direct Random Forest) are
  its two benchmarks, per Vision §8.4's model table.

> ### ⚠ ADDED 2026-08-28 — `GOV-2026-08-28-FD-01` **Recommendation 19**, ruled by the owner
>
> **What was wrong.** Vision §2.4 **tier 3** (line 172) requires *"Secondary learned-model
> comparisons: LSTM versus direct Random Forest and versus ridge regression"*, and Vision
> **§8.9** fixes that *"the flattened matrix supplied to **M-04 and M-05** is the flattened
> form of the identical causal window supplied to M-06"*. **Derived 2026-08-28 before
> asserting it**, `grep -ro` counts over each unit's `functional-design/` directory: `M-04`
> and `M-05` each occur **0** times in this unit, **0** in `statistical-inference`, and **0**
> in `regimes-diagnostics-reporting`; only **two** sets were declared anywhere in the twelve
> unit designs. Because **R-108 raises `FairnessError` unless the mask is a registered frozen
> mask for the members' declared comparison set**, and R-107 registers a mask only for a
> declared set, **tier 3 was not merely unreported — it was unimplementable**: the two ridge/RF
> baselines were trained (`models-and-baselines`), fixture-exercised
> (`fixtures-and-reproducibility`), and then entered no set, received no comparison-wide mask,
> got no matched-window assertion and reached no reported surface.
>
> **The ruling: a third declared set, `{M-04, M-05, M-06}`, with its own mask** — the GIM
> precedent applied exactly, **so that a secondary baseline's availability cannot shrink the
> primary scored set.** Extending the primary set to seven members was rejected for that
> reason: intersecting availability across seven members can only shrink the rows the
> *confirmatory* claim rests on, which is the same harm R-106 already cites for keeping GIM
> separate.
>
> **No mechanism changes — confirmed rule by rule, not asserted:**
>
> | Rule | Handles the third set how | Change needed |
> |---|---|---|
> | **R-106** (membership checked exactly) | The check is *"the passed predictions match the declared set exactly"* — set-generic, with the declared set read from `experiment.yaml` through `ConfigSnapshot`. Control (11) generalises to **any two declared sets merged into one call**. | **None** beyond the third `experiment.yaml` entry and this gate confirmation. |
> | **R-107** (identity, once-only, freeze) | `mask_id` derives from *"the declared set and the masked row content"*; once-only registration is *"once per comparison set"*; the freeze covers *"the registered set"*. A third set registers a third mask under the same rules and sits in the same G-05 bundle. | **None.** |
> | **R-111 / `test_common_masks.py`** | The matched-window assertion is *"every member of a comparison set was scored over the same window length and lag set"* — set-generic. **Control (28) is now instantiated on a set containing `M-04`/`M-05`**, which is the one instance Vision §8.9 spends a clause guaranteeing. | **None** beyond naming that instance. |
> | **R-110 limb 1** (completeness refusal) | Generalised from *"the declared primary comparison set"* to **per declared set**, so a tier-3 artifact missing `M-04` is refused upstream exactly as a primary artifact missing `M-02` is. The primary set's three difficulty controls remain the **named** instance. | **A scope generalisation of the same mechanism**, recorded here rather than left implicit. |
>
> **`benchmark_id` reads as the set's benchmark enumeration**, not a single ID: the primary
> set already carries four benchmarks (`B-01` plus the three difficulty controls) against the
> one model `M-06`, and the tier-3 set carries two (`M-04`, `M-05`). One `EstimandResult` per
> (model, benchmark) pair; R-110 limb 2's *"per benchmark"* field already assumes this shape.
> The field is indicative and intra-package (§ Depth), so no amendment arises.
>
> **Still owned outside this unit:** the membership itself is a §18.2/TC-03e frozen scientific
> choice (Student + Supervisor), so **all three memberships go to the gate as a confirmation**;
> and `regimes-diagnostics-reporting`'s configured breakdown list needs a **tier-3 row** so its
> R-127 completeness refusal reaches the new set. Neither is decided or edited here.

The proposal is grounded in Vision §2.4 (tiers 1–4), §6.10 and §8.9, and D-24 item 17's
protected-baselines enumeration ({M-01, M-02, M-03, B-01, C-01} — which does **not** name
M-04/M-05, so the tier-3 set is grounded on §2.4 and §8.9 rather than on D-24);
**the memberships go to the gate as an explicit confirmation, not a default, and nothing here
presents them as frozen.**

**Negative controls.** (8) A comparison called without a declared member (M-03 quietly
dropped, or M-04 dropped from the tier-3 set) → **`FairnessError`**. (9) An extra member →
**`FairnessError`**. (10) A duplicate member → **`FairnessError`**. (11) **Any two declared
sets merged into one call** — primary + GIM, or primary + tier-3 — → the passed predictions
match **no** declared set → **`FairnessError`**.

**Acceptance.** WS-16, TA-11 (this unit's rows), through FR-P1-04-7 and NFR-FAIR-01.

## R-107 — Mask identity, once-only registration, and the G-05 freeze

**Rule (Q5 = D, freeze-mechanics limb).** The mask FR-P1-04-7 calls *"computed once per
comparison set"* is made executable:

1. **Deterministic identity.** `mask_id` derives deterministically from the declared set
   and the masked row content; recomputation reproduces the same ID **or raises
   `FairnessError`**.
2. **Reported row counts, per station** — WS-16's evidence, recorded on the mask object.
3. **Stamps.** The mask carries `phase_id`, `source_id`, `target_definition_id`
   (`project.md` § Mandated), plus R-105's `partition_id` and member-`transform_id` set.
4. **Once-only registration.** A mask registers once per comparison set; a second
   registration for the same set **raises `FairnessError`**. "Computed once" is thereby a
   check, not a description.
5. **The freeze.** The registered set sits **inside the G-05 frozen bundle**
   (FR-P1-05-17): the mask registry is part of the evaluation artifacts whose hashes the
   G-05 record freezes before December is opened.
6. **The reporting surface, exposed here and printed downstream** *(added 2026-08-28,
   Recommendation 16 — this unit's half)*. The registered mask **exposes, for
   `regimes-diagnostics-reporting` to print and never restate**, exactly five values:

   | Value | Source | Vision §8.9 clause it discharges |
   |---|---|---|
   | `mask_id` | limb 1's deterministic identity | *"the comparison records a stable mask ID and feature-set ID"* |
   | `feature_set_id` | the frozen feature-set identity the masked members were built from | the same clause's second half |
   | per-station **surviving** row counts | limb 2 | *"exclusions and row counts are reported"* |
   | **exclusion counts** — rows dropped by the intersection, per station | the intersection step (W-1 step 3) | the same clause's first half |
   | the **scored-window statement** | the partition being scored; on the `DEC` mask its value is **"2–31 December 2022, 30 days, first 24 h excluded and counted"** (**D-28**, 2026-08-28) | D-8 / Vision §2.5's claim boundary, which `REQ-CLAIM-01` still states as *"tested on December 2022 only"* |

**Why this limb exists, stated as the governance report states it.** Recommendation 16's
finding was not against the 30-day ruling: it was that **a reader cannot tell the ruling was
made.** Derived 2026-08-28 across `regimes-diagnostics-reporting`'s four artifacts,
`grep -ro` counts: `mask_id` **0**, `row count` **0**, `exclusion` **0**, `feature_set_id`
**0**. So §8.9's *"exclusions and row counts are reported"* clause had **no reporting
surface**, and **D-28's 30-day scored set was disclosed on no claim artifact** — a
claim-boundary overstatement produced by *omission*, which `REQ-CLAIM-01`'s prohibited-class
check is structurally blind to because it searches for phrases that are *present*. This unit
already recorded `mask_id` and per-station row counts on the mask (limbs 1–2); what was
missing was the statement that they are **exposed for printing**, plus `feature_set_id`, the
exclusion counts and the scored-window statement. **The printing itself is
`regimes-diagnostics-reporting`'s obligation** (its `PrimaryTableArtifact` and
`BreakdownArtifact` family, its R-125 presence assertions and R-127 completeness refusal);
this limb is the supply side, and the split is stated in both directions. The follow-on
`REQ-CLAIM-01` boundary-text amendment is a Vision §15.2 change owned outside this stage.

**Negative controls.** (12) A recomputed mask whose `mask_id` differs from the registered
one → **fails**. (13) A second registration for the same comparison set →
**`FairnessError`**. (14) A pairwise (two-member, per-pair) mask attempt →
**`FairnessError`** — FR-P1-04-7's own stated criterion. **(31)** A registered mask missing
any of limb 6's five reporting values — `mask_id`, `feature_set_id`, per-station surviving
row counts, exclusion counts, or the scored-window statement — → **fails** the presence
test, so the reporting surface cannot be silently unsupplied *(new 2026-08-28,
Recommendation 16)*.

**Acceptance.** WS-16 (*"mask registry with stable IDs"*, row counts), TA-11.

## R-108 — The estimand is an ordered executable contract, and its result carries its own interpretation

**Rule (Q6 = D).** FR-P1-05-7's estimand is fixed as **one ordered pipeline**, not prose:

1. squared errors per (`station`, hour), **on masked rows only**;
2. per-station mean of paired differences, **benchmark minus model**;
3. **unweighted mean of the three per-station values** (equal-station weighting).

`paired_loss_differential` **raises `FairnessError`** when `mask` is not a **registered
frozen mask for the members' declared comparison set** (R-107's registry supplies the
check) — a metric computed off-mask or on an ad-hoc mask is an error, not a wrong number.

**The result object carries its own interpretation** (`domain-entities.md` § 4): the
scalar, the per-station components, the orientation **`benchmark_minus_model`**, the
weighting **`equal_station`**, and the sign-convention sentence — *"positive values favour
the model: the differential is benchmark minus model"* (Vision §2.3's binding convention) —
machine-readably, so every table built from it downstream inherits the convention as an
assertable field rather than a remembered sentence. `regimes-diagnostics-reporting` asserts
the field's presence; it does not restate the convention.

**The comparison is stamped, because the comparison is one of the four stamp targets**
*(added 2026-08-28, `GOV-2026-08-28-FD-01` **Recommendation 35**)*. `project.md` § Mandated
requires `phase_id`, `source_id` and `target_definition_id` stamped on *"every dataset,
prediction, mask **and comparison**"* (TE §13; Vision §2.2, §6.6). **The mask was stamped
(R-107 limb 3) and the comparison result was not** — verified 2026-08-28 against
`domain-entities.md` § 4, whose fields were `scalar`, `per_station`, `orientation`,
`weighting`, `sign_convention_sentence`, `mask_id`, `set_id`, `model_id`, `benchmark_id`:
**none of the three stamps and no `partition_id`**, on the object every downstream table and
the abstract-level conclusion are built from. `EstimandResult` therefore carries all four —
`phase_id`, `source_id`, `target_definition_id`, `partition_id` — **copied from the registered
mask at construction**, so drift is bounded by construction time and **detectable** through
R-107 limb 1's deterministic `mask_id`. The rule says *stamp the comparison*, not *make its
stamps reachable*: a fold-validation differential and the G-06 locked-test differential must
be distinguishable without dereferencing a second artifact, and Vision §2.2/§6.6's
prohibition on claiming Phase 1 / Phase 2 target equivalence depends on
`target_definition_id` being attached **wherever a differential is reported**.

**Negative controls.** (15) An inverted orientation (model minus benchmark) → **fails** on
a fixture whose true sign is known. (16) A pooled row-weighted aggregation → **fails** on a
fixture with asymmetric per-station row counts (equal-station and pooled disagree there by
construction). (17) A metric call with an unregistered mask → **`FairnessError`**.
**(30)** An `EstimandResult` missing any of `phase_id`, `source_id`, `target_definition_id`
or `partition_id` → **fails**; and one whose four values differ from the registered mask's
→ **fails**, which is the drift the construction-time copy is bounded by *(new 2026-08-28,
Recommendation 35)*.

**Acceptance.** ⚠ No row — FR-P1-05-7 is `UNTESTED`; controls (15)–(17) are the only bar it
gets until stage 3.2 proposes a row under Vision §15.2.

## R-109 — The G-06 evaluation: hash-receipt before metrics, one chokepoint, and exactly 2–31 December

**Rule (Q7 = D).** Three limbs, each executable:

1. **Hash-receipt precondition.** Every metric entry point evaluating the `DEC` partition
   requires a recorded **prediction-hash receipt** (`domain-entities.md` § 5), re-verifies
   the prediction file against it before computing (write-once detection, FR-P1-05-12),
   and **raises `LockedTestError`** when the receipt is absent, the hash mismatches, or
   the receipt timestamp does not precede the metric call. Recording the hash is **`06`'s
   act**; what this unit owns is **refusing to score without it** — the supporting-role
   split TA-18 records.
2. **The chokepoint.** `07`'s December target read arrives **only** through
   `governance-guards`' `open_restricted` with purpose **`"locked_evaluation"`** and a
   G-05 signature reference in `AccessRecord.authorization`, log-then-read (R-25). **This
   unit constructs no path of its own into the restricted root** (R-28's one-door rule) —
   which keeps it out of BLK-07's failure class.
3. **The scored set.** The DEC comparison's mask **asserts the scored range is exactly
   2–31 December 2022 (30 days), first 24 h excluded and counted** — **`evidence/DECISIONS.md`
   D-28 (2026-08-28)**, which ratifies the stage-3.1 ruling FU-7 = A of 2026-08-26 that this
   rule previously cited alone. A 1 December row reaching metrics **raises
   `LockedTestError`** — the 30-day ruling cannot be silently widened back to 31 at
   implementation. **The mask's scored-window statement (R-107 limb 6) is what discloses this
   to a reader of the result**, per D-28's own consequence that *"the scored set is 30 days
   everywhere, and must be disclosed as 30 days."*

   > **D-28's disclosed authority conflict, carried not resolved** *(cited 2026-08-28,
   > Recommendation 6, ratified as D-28)*. Vision:751 and TE:400 are byte-identical —
   > `| Locked test | — | — | December 2022 only |` — assigning the locked-test row **`—`** in
   > the Embargo column, while `requirements.md` FR-P1-04-5, a level-4 artifact, states the
   > 24-hour embargo and cites those very tables. D-28 fixes the operative value at 30 days on
   > three independent grounds (physical: 1 December is December's day furthest from solstice;
   > statistical: losing one of 31 bootstrap blocks widens the interval, erring toward
   > under-claiming; arithmetic and load-bearing: 720 hours divides by both 24 and 48, whereas
   > 744 does not, so the mandatory 48-hour block sensitivity would itself have raised under
   > the 31-day reading) and **records the conflict without pretending it was escalated**. D-28
   > also records that **a revised split manifest is owed at G-05** and that **no supervisor
   > signature artifact exists** — the ratification is the owner's under the recorded
   > equivalence. Nothing here resolves the conflict; this rule implements the value D-28 fixed.

**The two-events boundary, stated in both directions (Q7 = D's boundary statement).**
This unit performs **no pre-G-05 December read of any kind**: the required pre-G-05
coverage and regime audit is **`inventory-and-registry`'s** permitted, performance-blind
read, a **different event under a different purpose** (`"coverage_audit"`), and its
legitimacy is not a breach of the lock. Conversely, any `07` execution against `DEC`
before a verifying `g05_signature` is **blocked upstream** by
`materialise_locked_partition` (R-82) **and additionally refused here** by limbs 1–2 —
redundancy at the locked boundary is by design. The one-shot rule governs the metrics
evaluation alone; the coverage audit is legitimate, earlier, and someone else's.

**Negative controls.** (18) Receipt absent → **`LockedTestError`**. (19) Prediction file
hash mismatching the receipt → **`LockedTestError`**. (20) Receipt timestamp not preceding
the metric call → **`LockedTestError`**. (21) A second write of the prediction file —
detected by the re-verification, per FR-P1-05-12's write-once criterion → **raises**, and
the overwrite is a Validation-Auditor veto condition. (22) A 1 December row in the DEC
scored set → **`LockedTestError`**. (23) A December target read not routed through
`open_restricted` with purpose `"locked_evaluation"` → refused (`LockedTestError`); the
same control covers a pre-signature `07` DEC execution reaching this unit's boundary.

**Control that must *not* fire:** `inventory-and-registry`'s pre-G-05 coverage-audit read
under purpose `"coverage_audit"` → **passes its own door** and touches nothing here; a rule
that blocked it would repeat the "opened exactly once" misreading the team practice records
having already corrected.

**Acceptance.** TA-18 (**supporting** — "prediction hash preceding any metric"); WS-18 is
`features-and-splits`' row (`test_locked_test_guard.py`).

## R-110 — Honesty mechanics: completeness upstream, the disclosure trigger as a field, the caveat emitted by the path

**Rule (Q8 = D).** Three limbs, each a computable precondition only this unit can
guarantee; the tables and abstracts themselves belong to `regimes-diagnostics-reporting`,
and **the split is stated**:

1. **Completeness refusal, per declared set.** The evaluation run computes the estimand for
   **every** member of **each** declared comparison set over that set's one frozen mask, and
   **refuses to emit a results artifact** with any declared member's metric missing — a
   primary table missing M-02, or a tier-3 table missing M-04, becomes impossible
   **upstream** of the table. *(Scope generalised from "the declared primary comparison set"
   on 2026-08-28, Recommendation 19, when the third declared set was added; the mechanism is
   unchanged.)* The three difficulty
   controls (M-01 persistence, M-02 24-hour seasonal persistence, M-03 fitted
   station×month×hour climatology) are thereby computed over the **same frozen mask** and
   present in the emitted artifact; **their co-reporting in the primary table is
   `regimes-diagnostics-reporting`'s obligation** (FR-P1-05-9, TA-20), not this unit's.
2. **The disclosure trigger is a field.** The emitted metrics artifact carries, per
   benchmark, the differential's sign and a derived **`beats_model`** flag — derived from
   R-108's orientation, deciding nothing scientific — so FR-P1-05-20's disclosure check
   downstream asserts a field against the abstract-level text instead of re-deriving
   prose. R-16, the project's highest-rated reporting risk, becomes a field comparison.
3. **The caveat travels with the comparison.** Every serialized IRI or GIM comparison
   artifact **carries the mandated spatial-representativeness sentence, emitted by the
   comparison-producing path itself** — *"Phase 1 compares a grid cell against a
   station-coordinate evaluation, and part of any measured difference is a geometry and
   sampling artefact rather than skill"* (TEC-06; wording fixed by the governing
   documents, not invented here) — R-60's emit-from-the-path pattern, adopted so the two
   units' honesty mechanics are congruent. **The GIM overlap disclosure is keyed to a GIM
   comparison existing, not to the audit having run** *(re-keyed 2026-08-28, Recommendation
   41)*: **emitting or reporting any GIM comparison artifact without a registered
   overlap-audit result and its `gim_network_overlap_flag` value fails**, and **the audit's
   timestamp is asserted to precede comparator generation** — the same ordering assertion
   `external-products` R-60 obligation 2 already makes for the interpolation hand-check
   (*"Generate before the hand-check is recorded → fails, not accepted retrospectively"*).
   Disclosure is mandatory and **no independence claim may precede the audit** (TE §5.2).

> ### ⚠ RE-KEYED 2026-08-28 — `GOV-2026-08-28-FD-01` **Recommendation 41**
>
> **Superseded text, preserved verbatim:** *"The same mechanism carries
> **`gim_network_overlap_flag`'s value wherever GIM is compared** once the overlap audit
> runs"*, with control (26) reading *"A GIM comparison artifact without the
> `gim_network_overlap_flag` value **once the audit has run** → fails."*
>
> **The defect:** the checkers gated on *"the audit has run"*; the requirement gates on *"the
> audit exists"*. `requirements.md` **FR-P1-04-9**'s criterion, quoted from disk 2026-08-28,
> reads *"Tolerance report, config snapshot and **overlap audit all exist**; the flag value
> appears wherever GIM is compared"*, and `external-products` **R-60**'s Constraint states the
> obligation **unconditionally** (*"the `gim_network_overlap_flag` audit is present and its
> result disclosed"*). Under the conditional phrasing, **a GIM comparison emitted before the
> audit exists tripped no control at all** — the condition guarding the check was the very
> thing whose absence was the violation. Vision §6.10 states the ordering (*"No independence
> claim may be made before that audit"*); the design assumed it.
>
> **Narrowness of the live risk, stated rather than used as cover:** R-60 obligation 1 today
> refuses GIM generation outright while the Q-15 interpolation rule is unset, so no comparator
> can currently be produced. That mitigation **expires the moment Q-15 is decided**, which is
> precisely when the risk becomes live — so the re-key is made now rather than relied upon
> later.
>
> **The conditional phrasing was inherited, not invented.** `project.md` § Mandated reads
> *"ALWAYS disclose the `gim_network_overlap_flag` result **once the input-network overlap
> audit runs**"*, so this design and `regimes-diagnostics-reporting` R-126 were both tracking
> the affirmed rule faithfully. This rule now diverges in wording from that memory rule, and
> **a wording correction to `project.md` § Mandated is owed at the §13 learnings ritual** —
> which is human-gated and the only sanctioned write path. **No memory file is edited here**,
> and the divergence is disclosed rather than hidden.

**Negative controls.** (24) Emitting a results artifact with any declared set member's
estimand missing → **refused** (`FairnessError`). (25) A serialized IRI/GIM comparison
artifact without the spatial-representativeness sentence → the presence test **fails**,
because the producing path emits it. **(26, re-keyed 2026-08-28)** A GIM comparison artifact
**emitted or reported** with **no registered overlap-audit result**, or with the result but
without its `gim_network_overlap_flag` value → **fails**. (27) A benchmark row
in the metrics artifact without a `beats_model` field → **fails** the presence test.
**(32)** A GIM comparison whose registered overlap-audit result is timestamped **after**
comparator generation → **fails**, rather than being accepted retrospectively *(new
2026-08-28, Recommendation 41; the ordering R-60 obligation 2 already asserts for the
hand-check)*.

**Acceptance.** ⚠ No row — FR-P1-05-20 is `UNTESTED` and TA-20 is
`regimes-diagnostics-reporting`'s; the presence tests above are design obligations recorded
for stage 3.2.

## R-111 — `tests/test_common_masks.py`: masks plus the matched-window assertion, and the WS-13 proposal

**Rule (Q9 = C).** This unit's one test module is scoped as:

- **Masks** — WS-16's evidence: stable `mask_id`s, per-station row counts, no pairwise
  mask (R-106/R-107's controls land here);
- **plus the matched-window assertion at the comparison boundary**: every member of a
  comparison set was scored over the **same window length and lag set** — NFR-FAIR-01's
  matched-windows limb and TA-11's own phrase (*"comparison-wide mask tests… including the
  matched-window assertion"*). This is a property of **comparisons**, distinct from
  `windows.py`'s representation-parity property (WS-13), which genuinely lives in
  `features-and-splits` — two checks, two properties, one fairness rule, the same
  by-property split the siblings recorded for R-56/R-57.
- **and the assertion runs on a set containing `M-04`/`M-05`** *(added 2026-08-28,
  Recommendation 19)*. Vision §8.9 spends a clause on exactly this pairing — *"the flattened
  matrix supplied to **M-04 and M-05** is the flattened form of the identical causal window
  supplied to M-06"* — and until the tier-3 set `{M-04, M-05, M-06}` was declared (R-106),
  **that clause had no set to assert in.** Control (28) is therefore instantiated on the
  tier-3 set: a tier-3 comparison whose ridge/RF members were scored over a different window
  length or lag set than `M-06` **fails**. The **representation-form** half of §8.9's clause —
  that the flattened matrix is the flattened form of the *same* causal window — remains
  `features-and-splits`' WS-13 `windows.py` parity property, consumed here, not duplicated.

**The WS-13 §16 evidence-column item goes to the gate as ONE complete proposal — recorded,
not resolved:** record WS-13's evidence as the `windows.py` parity assertion, with
`test_common_masks.py` **supporting** via the matched-window limb — a §16 evidence-column
clarification for the owner to route through Vision §15.2 **or decline**. The departure has
been open since 2026-08-22 and expressly deferred to 3.1; this is the single owner decision
it was owed. No reading is adopted here.

**Negative controls (the module's four, named by the ruling).** (14) A pairwise mask
attempt **fails** (FR-P1-04-7's criterion — hosted here, counted once at R-107). (28) A
comparison over mismatched window lengths **fails** — **instantiated on the tier-3 set
`{M-04, M-05, M-06}`** as well as on the primary and GIM sets, per Vision §8.9's M-04/M-05
clause (added 2026-08-28, Recommendation 19). (12) A recomputed mask with a
different `mask_id` **fails** (hosted here, counted once at R-107). **(31)** A registered
mask missing any of R-107 limb 6's five reporting values **fails** (hosted here, counted once
at R-107 — added 2026-08-28, Recommendation 16).

**G-09 is not signed: the module's design is specified; no module is created.**

**Acceptance.** WS-16 (primary), TA-11 (supporting).

## R-112 — IRI and GIM join at evaluation time onto the frozen mask, and this unit narrows nothing

**Rule.** `src/evaluation` imports `src/external/iri.py` and `src/external/gim.py` **at
evaluation time only**, joining their products **onto the already-registered frozen
comparison-wide mask** (NFR-IRI-01; Vision §7.1's binding architectural rule; the
`external-products` Assumptions entry consumed here). CODE final GIM is an
**evaluation-time-only comparator, never a model input and never presumed independent
before the network-overlap audit** (TE §5.2); C-01 is labelled **generated, not trained**
(R-60). **Dst is diagnostic/hindcast-only** and appears in no confirmatory path this unit
computes (R-62); driver series are time-indexed only (R-63) — both consumed, not restated.

**The allowlist is a module-path grant, and this unit asserts no narrowing of TE §12.**
`src/evaluation/` is owned by three units (`external-products` R-56); this unit designs
`masks.py` and `metrics.py` only, and is **not** the sole permitted importer. The
module-graph limb of the IRI rule stays with R-56's transitive scan; the data-flow limb
with `features-and-splits` R-79 (WS-10, TA-07). What is **this** unit's is the join point:
evaluation-time, frozen mask, nothing earlier.

**Negative control.** (29) An IRI or GIM join attempted onto an unregistered or unfrozen
mask → **`FairnessError`** via R-108's precondition — the join point is the check.

**Acceptance.** WS-10/TA-07 are `features-and-splits`' rows; TA-11 reached through R-106/
R-107. No new row claimed here.

---

## Negative-control count, derived not carried

**Re-derived 2026-08-28 after the `GOV-2026-08-28-FD-01` remediation, and printed before
asserted: 31 distinct negative controls.**

Controls are numbered **(1), (3)–(32)** in the rules above. **(2) is vacated, not reused**:
R-103's round-trip control relocated into `src/features` (half B) under Recommendation 7,
because `src/evaluation` no longer obtains an object exposing `apply`. Existing numbers are
left in place so every cross-reference in this artifact set still resolves — which means
**the highest number (32) deliberately exceeds the count (31) by exactly one**, that one being
the vacated (2). (12) and (14) are each hosted in two rules and **counted once**, at R-107;
(31) is likewise hosted at R-107 and named again at R-111, counted once.

Derivation by rule:

| Rule | Controls | Count |
|---|---|---|
| R-103 | (1) — **(2) vacated, relocated to half B** | **1** |
| R-104 | (3), (4) | 2 |
| R-105 | (5), (6), (7) | 3 |
| R-106 | (8), (9), (10), (11) | 4 |
| R-107 | (12), (13), (14), **(31)** | **4** |
| R-108 | (15), (16), (17), **(30)** | **4** |
| R-109 | (18), (19), (20), (21), (22), (23) | 6 |
| R-110 | (24), (25), (26 re-keyed), (27), **(32)** | **5** |
| R-111 | (28) — new there; (12), (14), (31) hosted at R-107 | 1 |
| R-112 | (29) | 1 |
| | 1+2+3+4+4+4+6+5+1+1 | **31** |

**Movement against the 2026-08-27 count of 29**, stated so the difference is auditable:
**−1** (R-103's round-trip control relocated to the co-owner, Recommendation 7)
**+3** ((30) `EstimandResult` stamps, Recommendation 35; (31) mask reporting-surface presence,
Recommendation 16; (32) overlap-audit timestamp ordering, Recommendation 41) → 29 − 1 + 3 =
**31**. Three controls that must **not** fire are listed separately (R-104, R-105, R-109) and
are not in this count.

## Amendments owed

**Re-derived from scratch 2026-08-28 after the `GOV-2026-08-28-FD-01` remediation, and
printed before asserted: 5 + 1 + 1 = 7 across 5 units.** Each input was re-read on disk
rather than carried — and **the co-owner's row changed under this derivation while it was
being written**, which is why the arithmetic below names its source's mtime:

| Source | Owed | Basis, re-verified 2026-08-28 |
|---|---|---|
| `external-products` **R-55** | **5**, across **3** units | Re-read at `external-products/functional-design/business-rules.md:26` and `:613` — *"FIVE owed amendments across three units (`acquisition` 3, `inventory-and-registry` 1, this unit 1), boundary contracts only"*, and its `:181` table row confirming `acquisition`'s three. **Not restated here** beyond the verification; a restated count drifts. |
| `features-and-splits` | **1** | **Corrected 2026-08-28 from `0`.** The `0` was read from its § Amendments owed at `:789-799` (*"5 + 0 = 5"*, 2026-08-26) at the start of this remediation. That unit then re-entered and rewrote the section **during** this remediation (`business-rules.md` mtime 02:09): its own re-derivation now reads **`5 + 1 + 1 = 7, across 5 units`**, the `1` being **the BLK-09 resolution package (its R-83)** — `train_start: date` on `Partition` in `component-methods.md`, plus R-74 element 2's `PartitionError` reassignment for the `spec.partition_id != partition.partition_id` limb that the approved contract at `component-methods.md:642-648` types `LeakageError`. **This total now agrees with the co-owner's, derived independently on both sides.** |
| **This unit** | **1** | **The BLK-08 resolution package (R-103), one consolidated amendment, NARROWED**: the `component-dependency.md` row for the **`ABL-DIFF`-only** `src/evaluation` → `src/features` edge; `component-methods.md`'s resolver surface — **now `load_inverse(transform_id) -> Inverse` exposing only `inverse(frame)`**, replacing `load_transform(transform_id) -> Transform` — and `Transform`'s machine-readable target-touching declaration, both co-owner surfaces now authored as its R-84; and the inversion-lineage field on `Prediction` (R-104). One coherent change record, the same granularity as R-55's one amendment for three `src/external` boundary blocks. **R-84 changes this amendment's content, not its count** — the co-owner's own row says the same, so neither side double-counts the shared surfaces. |
| | **7 across 5 units** | 5 + 1 + 1 |

**The five units, named so the count can be checked rather than trusted:** `acquisition`,
`inventory-and-registry`, `external-products` (R-55's three), `evaluation-and-comparison`
(R-103), `features-and-splits` (R-83).

> **⚠ The "5 units" figure is NOT agreement with the stale one — checked by set difference,
> not by totals.** `models-and-baselines`' frozen artifacts carry *"**8** across **5**
> units"*; this derivation reads *"**7** across **5** units"*. The unit **count** matches and
> the **total** does not, and the two do not describe the same set: the stale figure counted
> three unit-local amendments that dissolved into ADR-11, while this one counts R-55's three
> units plus `evaluation-and-comparison` and `features-and-splits`. Comparing totals would
> call this a disagreement; comparing unit counts would call it agreement; **only the named
> set difference settles it** (`project.md` § Way of Working, c21). The co-owner ran the same
> check independently and reached the same conclusion.

**The superseded totals from this unit's own artifacts, preserved in order:** *"6 across 4
units"* (2026-08-27, and again earlier in this 2026-08-28 pass while the co-owner's section
still read `0`) → **"7 across 5 units"** (2026-08-28, after the co-owner's R-83 landed).
**The change is entirely in the co-owner's row; this unit still owes exactly one.**

**Why THIS unit's own count did not move, stated rather than assumed.** Recommendation 7 narrowed *what*
this unit's single consolidated amendment asks for; it did not split or multiply it. The four
2026-08-28 changes that might each have added a row **do not**, and each reason is checked
against § Depth's intra-package grant rather than presumed:

| 2026-08-28 change | Amendment? | Why |
|---|---|---|
| The resolver narrowing to `load_inverse -> Inverse` (Rec 7) | **No new row** | It is the **same** slot in the same consolidated amendment, with narrower content. A narrowing of an unapproved ask is not a second ask. |
| `EstimandResult` gains four stamps (Rec 35) | **No** | `paired_loss_differential`'s approved return is `tuple[float, Mapping[str, float]]`; the result object's fields are **intra-package** (§ Depth), so four fields cost no boundary change. |
| The mask gains `feature_set_id`, exclusion counts and a scored-window statement (Rec 16) | **No** | `build_comparison_mask`'s approved return travels as `DataFrame` rows; **the mask manifest fields are intra-package** (`domain-entities.md` § 2). |
| A third declared comparison set (Rec 19) | **No** | `experiment.yaml` membership is **configuration content routed to the gate as a confirmation**, not a boundary contract — the same reasoning that already exempted the first two sets. It adds a **gate item**, not an amendment. |
| `PartitionError` promoted to R-01's fifteenth (Rec 8) | **No row in THIS table** | R-01 is a stage-3.1 sibling **rule**, owned by `foundation`, not an approved application-design boundary contract. `component-methods.md:894` carries the fourteen names only as an `[assumption]` that expressly defers placement — *"declared where raised until 3.1 places them"* — so placing a fifteenth is what that assumption anticipates rather than an amendment to it. It is carried instead as a **governance dependency at `foundation`**. |

**What DID change in status, and must not be read as approval.** The
`component-dependency.md` row is now recorded as **an amendment owed AND a gate item**.
`evidence/DECISIONS.md` **D-27** states: *"No import-boundary change is authorised by this
decision. The §12 rule and its allowlist are untouched."* The matrix's `src/evaluation` row
carries `—` for `features` and its closing note reads *"none should be added without the
design naming the lookup"*. R-103 names the lookup; **the edge is unauthorised until both a
change record and a gate ruling exist, and stage 3.5 may not treat it as approved.** Until
then `ABL-DIFF` has **no executable inverse path** — which is BLK-08 open, stated as fact.

**Why Q5 adds no row.** The `experiment.yaml` comparison-set membership exceeds the
intra-package grant, but it is a **frozen scientific choice routed to the gate as a
confirmation** (TE §18.3; R-106) — configuration content, not a boundary contract. **This now
covers three declared sets, not two** (Recommendation 19), and the reasoning is unchanged: the
declared set's **read side** is intra-package per the receipted assumption in
`functional-design-questions.md`, so `build_comparison_mask`'s approved signature is not
amended: the declared-set check is performed by the intra-package mask-registration path
this stage specifies under § Depth, and R-108's registered-mask precondition makes an
unchecked mask unusable for any metric.

**Stale figure raised at the gate, not edited:** `models-and-baselines`' frozen READY
artifacts still carry "8 across 5 units". `features-and-splits` re-derived the basis to
5 across 3 on 2026-08-26, then to **7 across 5** on 2026-08-28 after its own re-entry, and
raised the staleness at the gate. This unit's total **matches the co-owner's**, derived
independently on both sides, and does not touch the frozen artifacts.

## The two requirements whose obligations exist but have no acceptance row

| Requirement | Rules | Why untested, and where the check lands |
|---|---|---|
| **FR-P1-05-7** — the confirmatory estimand and its sign convention | R-108 | **Untested by omission, not by design**: no §16/§19 row covers the estimand. Controls (15)–(17) are contract-level design obligations — the only bar until stage 3.2 proposes an acceptance row under Vision §15.2. The result object's machine-readable convention (R-108) is what makes a future row assertable. |
| **FR-P1-05-17** — evaluation code authored, reviewed and frozen inside the G-05 set before December opens | R-107 (limb 5), R-109 | **Untested by omission**: no row covers evaluation-code completeness, review or freeze. R-107 places the registered mask set inside the G-05 frozen bundle; R-109 requires the freeze-timestamp-precedes-December-access ordering — **an ordering the G-05 record produces, which this stage can require but not manufacture.** |

> **No artifact, manifest or report may state or imply that FR-P1-05-7 or FR-P1-05-17 is
> covered, satisfied or verified.** A design obligation is not a result.

## Requirement coverage

| Requirement | Rules | Acceptance |
|---|---|---|
| FR-P1-04-7 | R-106, R-107, R-111 | WS-16 (primary), TA-11 (supporting) |
| FR-P1-05-7 | R-104, R-108 | `UNTESTED` — see the table above |
| FR-P1-05-17 | R-107, R-109 | `UNTESTED` — see the table above |
| NFR-FAIR-01 | R-106, R-107, R-111 (matched-windows limb), R-112 | WS-16, TA-11 |

**4 requirements, 2 untested — derived from the story map's rows, the two upstream
artifacts agreeing.** TA-18 additionally supports R-109 without carrying a requirement of
this unit's.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence, so this unit opens at **R-103**. **The gap has narrowed to R-85…R-89, verified 2026-08-28**: `features-and-splits` allocated **R-83** (the BLK-09 `train_start` package) and **R-84** (BLK-08 half B) in its 2026-08-28 re-entry, so its range now runs R-74…R-84. The residual **R-85…R-89 gap remains observed, not explained** — if it was a reservation, or per-unit numbering was intended, say so at the gate and these artifacts renumber. This unit's own range is unaffected either way.
- **[assumption]** The `src/evaluation` shapes beyond the four approved boundary calls — the mask registry, the estimand result object, `Transform`'s declared target-touching status, the comparison-set declaration's read side — are intra-package and this stage's to specify (§ Depth, Q1 = B). The two surfaces exceeding that grant are R-103's dependency row (an amendment owed **and a gate item**, D-27 authorising no import-boundary change) and R-106's `experiment.yaml` membership (a gate confirmation, **now three declared sets**), each named as a cost where it arises. **Re-checked 2026-08-28** for the four changes made that day: `EstimandResult`'s four new stamps and the mask's three new reporting values are both intra-package and add no amendment (§ Amendments owed prints the check).
- **[assumption]** This unit designs `masks.py` and `metrics.py` only; `vector_block_bootstrap` and `count_storm_events` sit in `src/evaluation/` but belong to `statistical-inference` and `regimes-diagnostics-reporting` — the allowlist is a module-path grant (R-56), and no unit-level narrowing of TE §12 is asserted (R-112).
- **[assumption]** B-01 and C-01 are producible as `Prediction`s with `seed = None` and generated-not-trained provenance, stamped per R-105's contract with the reserved literal `untransformed`.
- **Verification obligations owned here:** controls **(1) and (3)–(32) — 31 distinct, (2) vacated by relocation** — enumerated per rule and re-derived 2026-08-28 in § Negative-control count; the three presence tests of R-110; `test_common_masks.py`'s **four** module controls (R-111, one of them the tier-3 matched-window instance).
- **Governance dependencies owned outside this unit** *(re-enumerated 2026-08-28)***:** **the gate's adoption ruling on the R-103 joint contract, and the import edge's authorisation** — the co-owner **has now authored half B as its R-84** (mtimes 02:09–02:21 on 2026-08-28) and **the two halves agree limb for limb**, so what the gate arbitrates is one reconciled contract rather than two texts; **D-27 withholds the edge's authorisation in terms**, so the edge needs a change record and a gate ruling before stage 3.5 may use it; **`foundation`'s amendment of R-01's enumeration to fifteen, adding `PartitionError`** (Recommendation 8's owner ruling — `foundation`'s artifacts still read "all fourteen" on disk today); **`statistical-inference`'s correction of R-113 precondition 2**, which imports R-105 "as written" and still raises `LeakageError` for a `partition_id` **mismatch**; **`regimes-diagnostics-reporting`'s printing of R-107 limb 6's five reporting values and its tier-3 breakdown row** (Recommendations 16 and 19); **the `project.md` § Mandated wording correction on the GIM overlap-disclosure trigger, owed at the §13 learnings ritual** (Recommendation 41 — human-gated, and no memory file is edited here); the **`REQ-CLAIM-01` boundary-text amendment** to state the 30-day scored set (Vision §15.2, D-28's follow-on); **D-28's owed revised split manifest** at G-05; BLK-03's limbs (`models-and-baselines`); BLK-04's limbs and BLK-09's `train_start` (`features-and-splits`); the comparison-set membership confirmation for **all three** sets (student/supervisor, R-106); any WS-13 §16 evidence-column change (Vision §15.2, R-111); acceptance rows for FR-P1-05-7 and FR-P1-05-17 (stage 3.2 under Vision §15.2); G-05's freeze of the evaluation code this stage designs (Supervisor); the AGPLv3 distribution question (outside the project).
- **Open — BLK-08's mechanism limb is an exit condition on this stage for both owners.** R-103 authors this unit's half binding **as narrowed to `ABL-DIFF`**, and the co-owner **has now authored the matching half as its R-84** (2026-08-28), agreeing limb for limb — so **the divergence R-84 raised is resolved by this pass**, not left to the gate. What remains outside both owners is **the gate's adoption ruling** and **the import edge's authorisation, which D-27 expressly withholds**; so `ABL-DIFF` has no executable inverse path today and **the blocker does not close on either unit's artifacts alone**. Its **premise limb closes for the primary path** on D-27: no inverse, no edge, on the confirmatory path.
- **Open — BLK-03 ↓, BLK-04 ↓, BLK-09 ↓ remain inherited exit conditions.** Nothing in this file closes them; no implementation may proceed while any stands.
- **Open — FR-P1-05-7 and FR-P1-05-17 carry no acceptance row** (2 of this unit's 4).
- **G-09 is not signed.** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged. No rule here authorises creating `src/evaluation/masks.py`, `src/evaluation/metrics.py`, `scripts/07_evaluate_and_report.py` or `tests/test_common_masks.py`; TE §18.3's stop-and-report rule binds every affected component while any P0 decision is unresolved.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant: R-106's memberships are proposed, not made — **including the new tier-3 set, which is a §18.2/TC-03e frozen scientific choice going to the gate as a confirmation**; R-109's scored set is FU-7 = A's ruling **as ratified by D-28**, cited not decided; D-27 is a reading of frozen text, cited not made; R-103's tolerance is the fixture manifest's, not a value fixed here.

---

> **Re-confirmation receipt, 2026-08-29 — `evaluation-and-comparison`.** The 2026-08-27T21:49:36Z REDO jump reset every unit's
> receipt floor, and this unit's content had already changed after that floor under the 2026-08-28
> post-execution pass (D-29 through D-32; **G-09 signed under D-31 with its TE §18.3 preconditions
> disclosed unmet**). The owner re-confirmed that post-execution content via the Consolidated
> Summary Confirmation at the foot of `functional-design-questions.md`, receipted `2026-08-29`.
> **No line above this marker was touched by this pass**, no count was re-derived, and nothing here
> discharges TA-15, WS-18 or TA-18, creates `aws_ai_dlc_preflight_report`, or alters the fact that
> stage 3.1 remains **FAIL** with no board having passed it.
