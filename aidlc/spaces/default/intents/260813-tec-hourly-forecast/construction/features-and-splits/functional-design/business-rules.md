# Business Rules — `features-and-splits`

**Unit** `features-and-splits` (Bolt 7) · **Kind** `library` · **Depends on**
`target-standardization`, `external-products`, `governance-guards`

> **Regenerated 2026-08-24, on a new stage attempt — and this unit's rules did change.**
> Construction opened at 2026-08-24T11:46:26Z; both `foundation` passes of that day touch
> nothing this unit reads. The substantive change is this unit's own **NOT-READY** verdict after
> five adversarial iterations, and the three decisions taken against it: **FU-4 = D** replaces
> R-74's unobservable pairing predicate with a **provenance stamp refused at the consumer** and
> a **manifest-based** test; **FU-5 = D** derives each call's row set from `fold` and `purpose`,
> letting `evaluate` **read** the causal history the 24-hour window needs while **emitting** only
> the validation month, which keeps **1 December** in the G-06 locked test; **FU-6 = A** states
> **three** calls per fold with the fitting call's outputs never emitted. R-81 and the § Amendments
> owed table are updated accordingly — **8 across 5 units**. Iteration-5 findings 4–7 are applied
> as mechanical corrections. **BLK-04 is not closed**, and the verdict below predates all of it.

> ## ⚠ REBUILT 2026-08-26 ON THE ADR-11 CONTRACT — OWNER RULING
>
> The fourteenth-receipt review (preserved at the end of `business-logic-model.md`) found the
> box above — and every mechanism of the 2026-08-24/26 waves — targeting an interface
> `component-methods.md` retired on **2026-08-23**: **ADR-11** removed `apply_transforms`,
> replaced `FoldSpec`/`build_folds` with **`Partition`**/`build_partitions`, returned a single
> **`FeatureBundle`** (matrix + tensor + `spec` + `transform_id`, one persisted object), and
> made the leak check an **identity comparison** (`LeakageError` when
> `transform.partition_id != spec.partition_id`; one enumerated exception, `REFIT` → `DEC`
> under `role="score"`, the G-06 apply). On the owner's authorization this file's rules are
> rebuilt on that contract, **rule ids R-74…R-82 plus R-76a and their subject matter
> unchanged** — `models-and-baselines` cites R-80 and R-76a's third limb by name under a
> frozen READY receipt, and both citations remain valid. **Every dated ⚠ box below is
> preserved as history of the retired `apply_transforms` lineage, not as contract.**
> § Amendments owed re-derives to **5 across 3 units** (this unit owes none); the "8 across
> 5" figure in `models-and-baselines`' frozen artifacts is raised at the gate as stale, not
> edited there. One element of FU-5 = D is defeated by ADR-11's `lead_in_hours` removal —
> see `business-logic-model.md` W-4b; R-74's `score`-side statement below follows the
> approved contract. **BLK-04 remains an open exit condition; G-09 remains unsigned.**

> ## ⚠ REMEDIATED 2026-08-28 ON GOVERNANCE REPORT `GOV-2026-08-28-FD-01` — OWNER RULINGS
>
> Verdict **FAIL**. Five rulings reach this unit, and each is applied with a dated note
> citing its Recommendation number. **Nothing below closes BLK-04, and G-09 remains
> unsigned.**
>
> - **Recommendation 4** (Critical; `CHAIR-03` and `ML-01`, two seats independently) — the
>   blocker. **BLK-09 was unmet *and* de-labelled here**, while the artifacts asserted an
>   unexecutable check was executable. Derived across all four files before the fix:
>   `BLK-09` = **0**, `train_start` = **0**, `BLK-08` = **0**, `inverse` = **0**. Board
>   option 1 applied: **`Partition` gains `train_start: date`**, sourced from
>   `configs/data.yaml`; both bounds are read from the `Partition`; **new R-83** authors the
>   contract and carries its status; a **strict-subset** negative control is added.
> - **Recommendation 25** (High; `ML-06`) — `DEC.train_end` was unspecified, so ADR-11's one
>   enumerated carve-out could not be shown necessary. Board option 1 applied: **`train_end`
>   is specified for all six partitions** in R-80's table, with **`DEC.train_end =
>   2022-11-30`**, and the carve-out is **retained for interface clarity rather than
>   necessity**. The **30** raising conditions are enumerated.
> - **Recommendation 7, as narrowed to `ABL-DIFF` on the strength of D-27** (High;
>   `CHAIR-04`, `ML-02`) — **new R-84** authors BLK-08 half B: `load_inverse` / `Inverse`
>   rather than `load_transform` / `Transform`, the round trip hosted inside `src/features`,
>   and **D-27 cited** with its required explicit statement that **the primary path needs no
>   inverse transform**. The `src/evaluation` → `src/features` edge is recorded as **owed and
>   unapproved** — D-27 withheld authorisation.
> - **Recommendation 6 / D-28** (Critical; `CHAIR-01`, `CHAIR-02`, `VAL-04`) — the FU-5
>   December item is **closed**, ratified as **D-28**. Superseded FU-5 = D wording is kept as
>   the dated history it already is.
> - **Recommendation 8** (High; three seats) — **`PartitionError` is `foundation` R-01's
>   fifteenth**. R-74's fitting-failure row and `domain-entities.md` § 10 are reconciled with
>   the discriminating rule: `PartitionError` for a **declared-identity disagreement**,
>   `LeakageError` where the disagreement implies **information flow**.
>
> **Rule ids R-74…R-82 plus R-76a keep their ids, subject matter and limb structure** —
> `models-and-baselines` cites **R-80** and **R-76a's third limb** by name under a frozen
> READY receipt, and both citations remain valid. **R-83** and **R-84** are additive, taking
> the head of the observed R-83…R-89 gap; no existing id moves. § Amendments owed re-derives
> to **7 across 5 units**, arithmetic printed.

The prohibitions this unit enforces, each with what it rejects, what it raises, and the
negative control that proves the rejection happens.

**This project's affirmed methodology is a negative control paired with every hard rule** —
a test that proves the violation is *caught*, not only that the happy path works.

**Every rule here is an integrity violation.** This unit defines what may enter the model at
all, and its violations are the ones with **no downstream symptom**: a leaked transform
produces *better* validation numbers and raises nothing.

**Rule IDs continue the single sequence.** `foundation` R-01…R-17, `governance-guards`
R-18…R-29, `acquisition` R-30…R-43, `inventory-and-registry` R-44…R-53, `external-products`
R-54…R-63 and `target-standardization` R-64…R-73, so this unit opens at **R-74**. This is the
numbering assumption stated in `functional-design-questions.md`; if per-unit numbering was
intended, say so at the gate and the artifacts restart at R-01.

## Sources

- `../../../inception/requirements-analysis/requirements.md` — FR-P1-04-1, -2, -5, -6, -8, -10, -12, -13, -16; NFR-IRI-01; NFR-LEAK-01.
- `../../../inception/units-generation/unit-of-work.md` § 7 — the `Owns` list, the boundary, the implementation notes; **BLK-04**.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2, § Per-unit coverage summary, § Open verification gaps.
- `../../../inception/application-design/component-methods.md` — `src/features`' boundary calls **as redesigned 2026-08-23 (ADR-11)**: `FrameSpec`, `Transform`, `FeatureBundle`, `build_features(...) -> FeatureBundle`, `fit_transforms(bundle, *, partition)`, the identity-based leak check with its one enumerated `REFIT`→`DEC` exception, the `lead_in_hours` removal; `src/data/splits.py`'s `Partition`/`build_partitions` and the six-partitions/five-manifest-rows rule; § Depth. *(Sources line rewritten 2026-08-26 — the prior line cited this file without naming the redesign.)*
- `../../../inception/application-design/services.md` § The nine stage scripts (`05` writes **`FeatureBundle`s**; M9 bundle addressing; M13 three-constructions cost), § Stage entry contract.
- `../target-standardization/functional-design/business-rules.md` — the D-17 target contract consumed here.
- `../external-products/functional-design/business-rules.md` — **R-56**, **R-57**, **R-58**.
- `../governance-guards/functional-design/business-rules.md` — **R-19** (the exactly-one-member exclusion shape), **R-23** and **R-24** (the two phase-boundary limbs). **Corrected 2026-08-26, iteration-5 finding 10 (iteration-4 finding 10):** R-24 is cited in this artifact's body and was absent here; **R-25** (access-log ordering) and **R-28** (restricted root) were listed and drawn on nowhere, and are removed — the same correction `business-logic-model.md` and `domain-entities.md` received on 2026-08-23, which this file had been left out of.
- `evidence/DECISIONS.md` — **D-10.3**, **D-11**, **D-13**; **D-27** (2026-08-24, the primary target is not transformed; the inverse obligation is `ABL-DIFF`'s alone) and **D-28** (2026-08-28, the G-06 locked-test scored set is 2–31 December 2022, 30 days). *(Added 2026-08-28 per Recommendations 7 and 6.)*
- `governance/reviews/GOV-2026-08-28-FD-01.md` — the full-board stage-3.1 review, verdict **FAIL**: Recommendations **4**, **6**, **7**, **8** and **25** reach this unit. *(Added 2026-08-28.)*
- `../evaluation-and-comparison/functional-design/business-rules.md` — **R-103** (the BLK-08 joint contract; half A binding there, half B authored here as R-84) and **R-104** (inverse-before-metric at the boundary). *(Added 2026-08-28 per Recommendation 7.)*
- `../../../inception/application-design/component-dependency.md` — § Dependency matrix: `src/evaluation` → `src/features` is **`—`**, and `src/features` → `src/models` is **`—`** in both directions. *(Added 2026-08-28; both facts are load-bearing for R-84 and for § 10's exception routing.)*
- Workspace inspection, 2026-08-23: `tests/` holds three modules, none this unit's; `src/` and `configs/` absent.
- `functional-design-questions.md` (**Q1 through Q9**, and **FU-7**), `domain-entities.md`, `business-logic-model.md`.

---

## R-74 — BLK-04: train-only fitting, enforced by check rather than by shape

**Rule (Q1 = D, mapped onto ADR-11, 2026-08-26).** Four elements, and the register names all
four as required:

| # | Element | Mechanism |
|---|---|---|
| 1 | **Allowed partitions** | A transform is fitted only on the named partition's **training range, exactly** — ADR-11 strengthens the register's *"not a subset"* to **range equality**. The range is **`[partition.train_start, partition.train_end]`**, both bounds fields of the `Partition` **since 2026-08-28** (**R-83**, BLK-09, Recommendation 4). Taking the `Partition` in scope is necessary but was **not sufficient**: until `train_start` existed the comparison had no lower bound |
| 2 | **Fitting failure** | `fit_transforms` raises **`LeakageError`** when `bundle.spec.role != "train"`; when `bundle.transform_id is not None` (already transformed); or when `[scored_start, scored_end]` is not exactly `[partition.train_start, partition.train_end]` — **in either direction**, over-wide or strict subset. It raises **`PartitionError`** when `bundle.spec.partition_id != partition.partition_id`, that being a **declared-identity disagreement** rather than information flow *(reassigned 2026-08-28 per Recommendation 8; see `domain-entities.md` § 10 for the discriminating rule and the amendment this reassignment carries)* |
| 3 | **Ownership of the fitted state** | `Transform` carries **`transform_id` and `partition_id`** — an identity persisted with the data (`FeatureBundle.transform_id`; `Prediction.partition_id`/`transform_id`), so ownership survives the `05`→`06`→`07` file handoffs |
| 4 | **Applying failure** | **`apply_transforms` is removed** — transforms are applied **only inside `build_features`**, which raises `LeakageError` when `transform.partition_id != spec.partition_id` (identity, immune to the nested ranges), with exactly **one enumerated exception**: `REFIT` → `DEC` under `spec.role == "score"`, the G-06 apply; the same pair under `role="train"` **raises**. `build_features` independently validates the spec against the partition list: scored range **contained in** the training range for `train`, in the `validation_month` for `score` |

> **⚠ The refit conditionality is discharged (noted 2026-08-26) — the four downstream units
> that cite this table by name inherit no condition any more.** The superseded condition box
> read: elements 1–4 *"complete and executable for F1–F4"*, conditional for the final refit
> because *"`fit_transforms` takes a `FoldSpec` and R-80 records that the refit is not one."*
> ADR-11's `Partition` represents the refit (`REFIT`, `validation_month=None`) and the locked
> month (`DEC`, 2022-12-01), and both `fit_transforms` and `build_features` take `Partition`s —
> so the elements are complete and executable for **all six partitions**, and G-06's apply is
> the enumerated `REFIT` → `DEC`/`score` pair. See R-80's dated box.

> **Historical box, preserved (rebuilt 2026-08-26): the interface it diagnoses was retired by
> ADR-11 on 2026-08-23**, and `component-methods.md` now preserves the same diagnosis itself.
>
> ## ⚠ THE APPROVED INTERFACE DOES NOT PREVENT WHAT IT CLAIMS TO
>
> `component-methods.md` states that a single `fit_transform(all_data)` is *"unrepresentable
> in this interface, which is how NFR-LEAK-01 is enforced by shape rather than by review."*
>
> **It is not.** `fit_transforms(train, *, fold)` types `train` as an **unconstrained
> DataFrame**, so `fit_transforms(all_data, fold=F1)` **type-checks**. BLK-04's own
> implementation note agrees: the two-function split *"prevents the single-call convenience
> shape but not the underlying full-dataset fit."*
>
> **This is the violation with no downstream symptom.** A transform fitted on all data
> produces *better* validation numbers and raises nothing anywhere. **Four downstream units
> inherit it** — `models-and-baselines`, `evaluation-and-comparison`, `statistical-inference`,
> `regimes-diagnostics-reporting` — because *"every reported number inherits the fit."*

**Why element 4 is not optional.** Element 2 stops a transform being **fitted** on the wrong
rows. Nothing in it stops one **correctly** fitted on F1 being **applied** to F3's validation
month — **the same leakage by a different route**. *"Ownership of the fitted state"* is in the
register's required list precisely for this.

> **Historical box, preserved (rebuilt 2026-08-26 on ADR-11).** Everything inside the box
> below — its `purpose` tables, its pairing control, its residual, its December routing and
> its refit finding — mechanised element 4 on the retired `apply_transforms` interface and is
> **history, not contract**. The live element-4 mechanism is the identity check in the table
> above; the live mapping of the box's load-bearing content follows immediately after it.
>
> ## ⚠ ELEMENT 4 — MECHANISM CORRECTED TWICE, 2026-08-23
>
> **First text, superseded:** *"`apply_transforms` **refuses** a transform whose fold does not
> match the frame's partition."* — a **claim, not a check**, the identical defect this rule
> diagnoses in the approved interface one box above: the signature carries no fold or partition
> parameter and `frame` carries no partition tag.
>
> **Second text, also superseded:** *"derives each row's partition from its record timestamps
> … a row belonging to any other fold, to the final refit, or to December raises
> `LeakageError`."* — **it derives a label that does not exist, and it blocks two lawful
> paths.** Both found by adversarial passes, **inside the remedy for the leak with no
> downstream symptom**.
>
> **Why per-row derivation is impossible.** R-80's training ranges **nest**: Jan–Mar ⊂ Jan–Jun
> ⊂ Jan–Sep ⊂ Jan–Oct ⊂ Jan–Nov. A **15 February** row lies in **five** of that table's six
> rows, so *"this row's partition"* is **not single-valued**. **The check never needed a
> label** — it needed containment in a **named** scope.
>
> **Third text, also superseded — and this one needed an amendment.** It read: the transform
> accepts *"that fold's training range, its 24-h embargo, its validation month"*, the refit
> *"1 Jan – 30 Nov and December"*. **Those five sets are strictly nested prefixes** — F1 to 30
> Apr ⊂ F2 to 31 Jul ⊂ F3 to 31 Oct ⊂ F4 to 30 Nov ⊂ refit to 31 Dec — so the rule collapsed
> to *"not later than this transform's validation month"*: **an upper bound, not a leakage
> check**. **F4's** transform (fitted Jan–Oct) applied to **April passed, and F4's fit saw
> April.** The one worked example given was the **non-leaking** direction. Third adversarial
> pass.
>
> **Why no row-level rule could have worked.** Leakage here is a property of **what the call
> is for**, not of where the row sits: April is legitimately in F4's training data, so
> transforming it *as training* is correct and *as F1's evaluation* is the leak. Neither
> `apply_transforms` nor `FoldSpec` carried the use.
>
> ### The amendment — approved by the owner, 2026-08-23
>
> ```
> apply_transforms(frame: DataFrame, *, transform: Transform,
>                  purpose: ApplyPurpose) -> DataFrame
> ```
>
> `purpose` is **required, with no default** — an implicit default is where the leak would
> re-enter — and each value carries a **different, tight** accepted set:
>
> | `purpose` | Fold *k*'s transform accepts | The refit's transform accepts |
> |---|---|---|
> | `train` | Fold *k*'s **training partition**, embargo rows **excluded and counted** | 1 Jan – 30 Nov |
> | `evaluate` | **Exactly fold *k*'s validation month** as the **emittable** set; the 24-h embargo rows are **readable as causal history only, never emitted** (W-4b) — an embargo row **emitted** under `evaluate` raises `LeakageError`, the control § 10's row carries | **December only**, through R-82's guard |
>
> *(Evaluate row completed 2026-08-26, iteration-5 finding 9 / iteration-4 finding 9: the
> embargo term previously sat only on the `train` row, where embargo rows are outside the
> training partition by construction and the qualifier binds nothing — the row where an
> embargo row would appear if not dropped was silent. W-4b's read/emit split is what
> reconciles the finding's remedy with the causal-history window: the same 24 hours must be
> readable for the first `vtec_seq_24` window and must never appear as an emitted row.)*
>
> **`Transform` carrying its `FoldSpec` still costs nothing** — `component-methods.md` leaves
> it *"referenced as a type and left unspecified: … intra-package"*. **The `purpose` parameter
> does cost**: it is a **cross-package boundary amendment**, the **sixth** this stage owes.
> **The total is no longer five across three units** — see § Amendments owed, which derives it.
>
> **What `purpose` does NOT bound.** It bounds **which rows a transform may touch under a
> declared use**; it does **not** bound what the caller does with the returned frame.
>
> **The consequence, named.** `purpose=train` accepts a fold's **whole** training partition,
> and those nest — so **10 of the 39 accepted `train` cells** touch a month that is **another
> fold's validation month** (F2→Apr; F3→Apr, Jul; F4→Apr, Jul, Oct; refit→Apr, Jul, Oct, Nov).
> Each is **truthful** and **correct as training**. The leak is in **reusing that output as an
> evaluation**, at a different call site.
>
> **The pairing control — restated 2026-08-24 on FU-4 = D.** The previous formulation asserted
> that a scored frame *"came from a call"* with `transform = T_k` and `purpose=evaluate`, and
> rested on the nine stage scripts being a closed set. The set **is** closed (nine, counted
> from `services.md`), but the predicate was **unobservable**: `05` writes the features and
> `06`/`07` read them from **artifacts**, so `apply_transforms` is called only in `05`, no
> scoring site calls it, and nothing recorded the fold or the purpose on what was emitted.
> *(Iteration-5 finding 1.)* The control now has three named parts:
>
> 1. **The stamp** — every emitted feature artifact carries `fold_id`, `purpose` and
>    `transform_id` as recorded fields (`domain-entities.md` § 5; W-4a).
> 2. **The refusal, at the consumer** — `06` and `07` reject a frame whose stamp is not
>    `(fold k, evaluate)` when scoring fold *k*'s validation month.
> 3. **The test, with its kind declared** — `tests/test_train_only_transforms.py` is
>    **manifest-based**: it reads the emitted stamps and asserts that refusal. **Not** static
>    analysis of the nine scripts, which cannot follow a file-mediated handoff; **not**
>    monkeypatch-and-replay, which verifies a replay rather than what a real run emits.
>
> **Residual, correctly described:** an **unstamped or hand-assembled frame** — one that never
> passed through `build_features` and so carries no stamp to refuse. The earlier wording named
> *"a false `purpose=train` declaration outside the nine enumerated scripts"*, which pointed at
> an exotic path while the real gap was the **ordinary `05`→`06` handoff inside them**.
>
> **Cost:** the stamp crosses into `06`/`07`, so the amendment total re-derives to **8 across
> 5 units** — declared here, not left to a later sweep.
>
> **December is not excluded here, it is routed.** Applying the **final-refit** transform to
> December **is** the G-06 path. The lock is held by **R-82's execution guard** — December rows
> reach `apply_transforms` only inside a frame materialised against a **verified
> `g05_signature`** — not by this rule. The second text duplicated the lock in the wrong place
> and would have made **G-06 unreachable** and the **FR-P1-04-14 final refit**
> untransformable.
>
> **The refit has no path on EITHER side, and it is one open decision.** `fit_transforms` is
> typed `(train, *, fold: FoldSpec)` **and so is `build_features`** — R-80 records that the
> final refit **is not a `FoldSpec`**, so today the refit can neither have a transform fitted
> for it nor have its features built, and December inherits both gaps. **Corrected 2026-08-23**
> from a statement naming only the `fit_transforms` side. All of it turns on R-80's open shape
> question and goes to the gate **once**, with it. Element 4 is **complete for F1–F4** and
> **conditional** for the refit and therefore **G-06**.
>
> **`assert_membership_from_timestamps` is cited for what it does**, not as the derivation:
> `(frame) -> None` validates a row against the partition it is **filed under**. It returns
> nothing and derives nothing; the second text was wrong to lean on it.
>
> **Which representation.** `build_features` applies the `Transform` to the **assembled
> feature frame before windowing**, so both representations inherit it from **one** definition,
> and the `NDArray` tensor — carrying no timestamps — is **never transformed directly**. Element
> 4 therefore sits upstream of both, including the sequence tensor M-06 consumes. *(Reworded
> 2026-08-24, iteration-5 finding 6: the previous sentence was the one R-81 § Resolution quotes
> as **unexecutable**, since no transformed frame exists before windowing, so stating it here as
> the contract contradicted its own refutation two rules later.)*

**The element-4 lineage, mapped onto ADR-11** *(rebuilt 2026-08-26)*:

- **The `purpose` parameter and its accepted-set tables → dissolved.** The role is a declared
  spec field (`FrameSpec.role`, `train` | `score`) validated by `build_features` against the
  partition list, and the leakage decision is the **identity check** — ADR-11's own finding is
  that *"the constraint cannot be expressed over rows."* The `train` rows survive as
  containment in the training range (embargo rows excluded and counted); the `evaluate` rows
  as `score`-role containment in the `validation_month` — with the December read/emit
  consequence changed by ADR-11's `lead_in_hours` removal (see `business-logic-model.md`
  W-4b's conflict box, raised at the gate).
- **The pairing control → native** (FU-4 = D dissolved): `FeatureBundle` persists the spec and
  `transform_id` with the data; `06`/`07` assert them and raise on `transform_id is None`;
  `tests/test_train_only_transforms.py` stays **manifest/bundle-based**. Residual: a
  **bundle-less frame** that never passed through `build_features`.
- **The 39-cell consequence → still true** (re-derived programmatically 2026-08-26): a
  `train`-role bundle for partition *k* lawfully carries *k*'s whole training range — 3 + 6 +
  9 + 10 + 11 = **39** month-cells across the five fitting-capable partitions, **10** of them
  another partition's validation month (F2→Apr; F3→Apr, Jul; F4→Apr, Jul, Oct; REFIT→Apr,
  Jul, Oct, Nov). Reuse as an evaluation now fails structurally: scoring sites assert
  `spec.role == "score"`, and a cross-partition `score` spec fails the identity check.
- **December is routed, not excluded** — the G-06 apply is the enumerated
  `REFIT` → `DEC`/`score` pair; the lock is held by R-82's execution guard.
- **The refit-has-no-path finding → resolved** by `Partition` (R-80's dated box); G-06's
  dependency is discharged.

**Constraint — stated once, consumed by name.** BLK-04 calls it a *"governed cross-unit
contract"*. The four downstream units **cite** this rule; they do not restate it. A restated
contract in four places drifts, and this stage has already corrected four counts that drifted
between restatements.

**Negative controls** *(restated 2026-08-26 in ADR-11 form; the retired-interface controls
they replace are preserved in the box above; four added 2026-08-28 per Recommendations 4, 8
and 25 and marked)*. Build a bundle whose spec claims F1/`train`
over Jan–Nov (the full-dataset fit) → `build_features` **raises** on containment, and a
hand-asserted bundle **raises in `fit_transforms`** because the scored range is not exactly
F1's training range. Fit on a range one row wider or narrower than the training range →
`LeakageError` (equality, not subset). **[Added 2026-08-28, Recommendation 4]** Fit on a
**strict subset** of the declared training range — F4 (`2022-01-01`…`2022-10-31`) fitted on
`2022-02-01`…`2022-10-31` → **`LeakageError`**: the lower-bound direction the missing
`train_start` admitted, and the one a derive-from-earliest-row implementation would have
accepted silently. **[Added 2026-08-28, Recommendation 25]**
`fit_transforms(bundle, partition=DEC)` for **any** bundle whose range includes a December
2022 date → **`LeakageError`**, because `DEC.train_end` is **2022-11-30** (R-80's table), so a
December fit is unrepresentable by the field itself. Apply **F4's** transform to a spec
claiming **F1**
(any role) → `LeakageError` on identity — the leaking direction the two superseded rules both
passed, now failing **regardless of which months overlap**. Every mismatched ordered pair of
the six partition ids that is not `REFIT` → `DEC` → `LeakageError`, **asserted by enumeration
over the six ids**, so a second exception cannot be added without a test failing. `REFIT` →
`DEC` under `role="train"` → `LeakageError`. **[Added 2026-08-28, Recommendation 25 — the
enumeration's size, derived rather than asserted]** Six ids give **36** ordered pairs, of
which **30** are mismatched (36 − 6 identical); **1** is exempt (`REFIT` → `DEC` under
`role="score"`), so **29** mismatched pairs raise; plus `REFIT` → `DEC` under `role="train"`
= **30 raising conditions**, and the test enumerates all 30. **[Added 2026-08-28,
Recommendation 8]** `fit_transforms` called with a bundle whose `spec.partition_id` names a
different partition than the `partition` argument → **`PartitionError`**, not `LeakageError`
— the same logical condition `models-and-baselines` R-92 raises `PartitionError` on, so a
test written at `06` does not fail at `05`. A bundle with `transform_id is None` reaching
`fit_predict`, `06` or `07` → **raises**. An already-transformed bundle passed back to
`fit_transforms` → `LeakageError`. An **empty assembled frame** inside `build_features` →
raises (intra-package rule, this stage's under § Depth: a check that never fired must not
pass for one that did).

**Controls that must *not* fire** — as load-bearing as the ones that must. A `train`-role
bundle for **F4 carrying April** → **passes** (April is genuinely in F4's training range). A
`score`-role spec for **F1 contained in April** → **passes**. The **`REFIT` transform on the
`DEC` `score` spec** → **passes**: that is G-06, gated by R-82's execution guard and not by
the identity rule. A `score` spec covering **seven days inside November** (the D-11 fixture
window) → **passes** — containment, not equality, is the validation, which is what keeps
WS-12/WS-13/WS-20 representable.

> **⚠ One earlier control is withdrawn, not silently dropped.** It read: *"fit and apply within
> one fold, spanning its training range, embargo and validation month → passes … that is the
> ordinary path and must not be blocked."* Under ADR-11 a **single** spanning call is likewise
> unlawful — a spec's scored range must sit inside what its one declared `role` permits — so
> the caller makes separate `train` and `score` calls. The withdrawal, first recorded for the
> retired `purpose` mechanism, carries over unchanged in substance.

> ## ⚠ BLK-04 IS AN EXIT CONDITION, AND THIS DESIGN DOES NOT DISCHARGE IT
>
> The register's ruling: this unit and the four downstream units **may enter** stage 3.1;
> **none may complete or exit without its approved contract**; and **no implementation may
> proceed** while it stands. **Approving this design is not that approval.**
>
> **NFR-LEAK-01's evidence is owed to the Supervisor at G-04 and G-05**, unchanged by
> anything here.

**Acceptance.** TA-11 (**owned by this unit**), through FR-P1-04-6.

## R-75 — Every predictor is lagged, and the anchor is a third limb

**Rule (FR-P1-04-2, NFR-LEAK-01).** `assert_lags_safe` **raises** when
`actual_lag_hours < safe_lag_hours`; when a driver's `release_status` indicates a
**backfilled final value** where the contemporaneous grade was required; or when
**`f107_81_trailing`'s window does not end at the safe-lagged day**.

**The lags** (D-10.3): Kp/ap3 **≥ 3 h**; Hp60/ap60 **≥ 1 h**; F10.7 at the **previous-day
observed** value with a **trailing** 81-day mean. **Dst is diagnostic/hindcast-only. SSN is
absent**, confirmed by `grep`.

**Constraint — the anchor is a third limb, and FR-P1-04-2 says why:** *"a trailing 81-day
mean **ending at day t** passes both the not-centered check and the lag assertion while
including same-day F10.7."*

**Constraint — the mean is recomputed from the anchor and compared** (Q4 = D). A recorded end
date is a **claim**; the recomputation is the **check**. Without it, a series whose recorded
anchor is right and whose values came from a different window passes.

> **Deliberate overlap with `external-products` R-57, stated rather than left looking like
> duplication.** R-57's future-independence property is strictly **stronger** — it holds at
> every index. **The split is by property:** R-57's is a **series-level** property of the
> driver product; the anchor recomputation is a **value-level** property of the mean built
> here, checkable only where it is built, and it catches a **recorded-but-wrong anchor** that
> R-57's framing does not spell out. Two checks over one fact.
>
> **Corrected twice, 2026-08-23.** From *"R-57's are `Pending`"* — R-57 is a **rule**, and the
> rows it contributes to are these same two, with `external-products` the **supporting** unit
> rather than the owner of a separate row. Then from *"would make this unit's acceptance
> depend on a module in another unit"*, which **proves too much**: R-79 delegates the
> module-graph limb of NFR-IRI-01 to `external-products` R-56 while WS-10/TA-07 stay this
> unit's rows. The by-property reason survives both cases.

**Negative controls.** Inject a centered mean → fails. Anchor the trailing window at day *t*
→ **fails on the third limb**, where the first two pass. Record the correct anchor and supply
values from a different window → **fails on the recomputation**. Backfill a driver from a
final archive → fails on `release_status`.

**Acceptance.** WS-11, TA-08 (**both owned by this unit**).

## R-76a — TA-36's enforcement raise and primary test are THIS unit's

> **The `R-76a` id and its filing position are kept deliberately** *(stated 2026-08-26,
> iteration-5 finding 11a / iteration-4 finding 11a)*. The suffix does not claim kinship with
> R-76 (dictionary closure) the way `external-products` R-54a claims kinship with R-54; it
> records only that the rule was **added between** existing ids after the single sequence
> R-74…R-82 was already cited downstream. Renumbering to R-83 now would break live cross-unit
> citations: `models-and-baselines` cites "`features-and-splits` R-76a's third limb" in both
> its business-rules and domain-entities artifacts, and that unit is terminal-READY under a
> frozen receipt. A broken citation in two READY artifacts costs more than a non-sequential id
> whose referent is unambiguous.
>
> **⚠ Added 2026-08-23, correcting the opposite claim in all three artifacts.** They stated
> TA-36 was *"`external-products`' row, not this unit's"* — read off the story map's
> § Per-unit coverage summary and Table 2, and **stopped there**. `external-products` **R-54a**
> already reconciled this against § Cross-unit responsibilities, **which is the reconciling
> statement**, and carries the control that any artifact claiming the wrong side *"fails
> review"*. R-54a exists because this same error was made and corrected once already — **read
> one table and stopped** — and this unit then reproduced it from the other direction. Found
> by an adversarial pass; verified against R-54a directly.

**Rule (FR-P1-04-17, TA-36).** The story map's § Cross-unit responsibilities splits **four**
ownerships, of which **this unit holds two**:

| Ownership | Unit |
|---|---|
| Data production — driver series carrying their own interval semantics | `external-products` |
| **Enforcement — the raise at `features.build_features`** | **this unit** |
| **Primary acceptance test — TA-36, in `tests/test_feature_leakage_guards.py`** | **this unit** |
| Upstream evidence — driver manifests recording interval semantics and release grade | `external-products` |

**Constraint — the raise, which no raise list here previously carried.** `build_features`
**raises `AlignmentError`** on a driver value repeated **outside its own defined interval**
(Kp/ap3 beyond its 3-hour interval) and on a value **shifted to a neighbouring hour** (Dst off
its own hourly averaging interval). These are R-58's limbs **1 and 2** arriving as **rejection
at the consumer**, not as upstream contract evidence — R-54a quotes the deciding clause: an
upstream contract test is *"documented separately and **not** replacing the primary rejection
test."*

**Constraint — limb 3 is a grep, not a raise** (corrected 2026-08-23). *"No driver is
interpolated, at any stage"* is **absolute**, and R-58 says why a runtime check cannot carry
it: a grep *"is the only check that reaches a call site no fixture exercises."* An interpolated
value is **indistinguishable at runtime** from a genuine one — there is no signal in the data
for `build_features` to raise on. So limb 3 is a **static check over the source tree**, run in
the same test module, asserting **no interpolation call on any driver series**. The first
statement of R-76a asked `build_features` to raise on it, which is **not implementable**; it
is corrected rather than quietly dropped, because R-58 warns that *"building limbs 1 and 2
alone leaves the row partially satisfied while looking complete."*

**Constraint — the test module is named**, because it was named nowhere: TA-36's primary
negative-path test is **`tests/test_feature_leakage_guards.py`**, built here. It was absent
from § 12's seventeen-module list, which predates `CR-2026-08-22-LEAKAGE-TA`; that gap goes to
the gate rather than being resolved here.

**Constraint — no reallocation.** R-54a records that the allocation *"is the default and
stands unless functional design produces verified evidence for a better one; if it
reallocates, it updates **both** artifacts."* This unit has produced no such evidence, so the
default stands and **`external-products` is not edited**.

**Negative controls.** Kp repeated outside its 3-hour interval → **`AlignmentError`**. Dst
shifted to a neighbouring hour → **`AlignmentError`**. Add an interpolation call on a driver
series anywhere under `src/` → **the static limb-3 check fails**, with no runtime raise
involved and none possible.

**Acceptance.** **TA-36** — **`Pending`**: the row exists, is not implemented, not executed,
not passing. Approved 2026-08-22 under `CR-2026-08-22-LEAKAGE-TA`.

## R-76 — The ML input space is closed

**Rule (FR-P1-04-12).** The feature set is **exactly** the TE §6.2 dictionary — *"no field
outside that table, and no derived tensor built from one, enters training or inference."*
`build_features` **raises** on any field outside it.

**Constraint — window length is a frozen constant, not a hyperparameter.** One value per
feature-set ID, shared across all model families; the primary history window is **24 hours**
(Vision §8.1: *"History length is not a tuned hyperparameter"*). **`experiment.yaml`'s window
length equals 24 and appears in no grid.**

**Constraint — raw longitude is never a predictor** (FR-P1-04-10). Longitude enters **only**
through `lst_sin` and `lst_cos`.

**Constraint — an unresolved station registry blocks `station_lat` and excludes
`lst_sin`/`lst_cos`**, consumed from `inventory-and-registry` R-45/R-46. **What provenance is
sufficient is not decided here.**

**Negative controls.** Inject a field absent from §6.2 → **raises**, not passes silently.
Build a derived tensor from such a field → raises. Place the window length in an
`experiment.yaml` grid → **fails**. Introduce a raw-longitude column → raises.

**Acceptance.** **TA-33** — ⚠ **`Pending`: the row exists, no test module is implemented,
none has been executed, and none has passed.** FR-P1-04-10's longitude limb has **no row at
all**.

## R-77 — Two carry-forward rules, opposite behaviour, one partition

**Rule (FR-P1-04-13 against FR-P1-04-3, Q7 = D).**

| Rule | Scope | Behaviour |
|---|---|---|
| FR-P1-04-3 | **External drivers only** | Carry forward **≤ 3 h**, then **exclude the row** |
| FR-P1-04-13 | **`vtec_lag_*`** | **Carry-forward prohibited**; the **window is excluded** |

FR-P1-04-13: the ≤3 h allowance *"is scoped to external drivers only and **must never be read
as reaching `vtec_lag_*`**."*

**Three parts:**

1. **The field class is a required argument** to the carry-forward path; `vtec_lag_*` is
   **rejected at that boundary**.
2. **The two classes partition the dictionary** — every field is exactly one of
   driver-derived or target-derived. Part 1 stops a target lag entering the driver path; a
   field belonging to **neither** class, or to **both**, escapes both rules without this. The
   classification is owed to R-76's closure anyway.
3. **Every excluded window is counted.** FR-P1-04-13 and FR-P1-04-5 both say *"excluded **and
   counted**"*. A silent exclusion and a counted one are **indistinguishable at the
   artifact**; the count is how a reviewer tells a working exclusion from one that never
   fired.

> **Part 1 is a runtime check, not a type — and this unit has the proof that matters.** R-74
> shows an approved interface claimed to make a leak *"unrepresentable"* that does not.
> Shape-based prevention is worth having and is never the whole check.

**Constraint — the target-derived contract** (FR-P1-04-13): `vtec_lag_1h/2h/3h/24h` are
**strictly causal at exact lags `[1,2,3,24]`**; `vtec_seq_24` is a 24-step causal sequence
**excluded when incomplete**; the pooled model carries `station_onehot_ARUC/BSHM/NICO` plus
**verified** `station_lat`.

**Negative controls.** Carry a `vtec_lag_*` value forward → **fails**. Call the carry-forward
path without a field class → fails. Add a dictionary field belonging to neither class → the
partition assertion fails. Leave an incomplete `vtec_seq_24` window in → fails. Exclude one
without counting it → **fails**.

**Acceptance.** **TA-34** — ⚠ **`Pending`**.

## R-78 — Support fields are diagnostic by default

**Rule (FR-P1-04-16, Q8 = D).** Four rules, four separate failures:

| # | Rule | Enforcement |
|---|---|---|
| 1 | **Diagnostic by default** | **The default**: excluded from the feature set **unless an approval ID is present** |
| 2 | Readable over **hours ≤ t** only | A read at or beyond hour *t* **fails** |
| 3 | Model use requires **G-04 approval recorded before the feature-set freeze** | The approval's **timestamp must precede the freeze** |
| 4 | **Target-hour quality fields permanently forbidden** as features | Asserted separately |

**Why rule 1 is implemented as a default rather than as a rule.** The failure mode is a
support field drifting into the feature set **by inclusion rather than by decision**. A
default-exclude makes that **impossible** instead of detectable — and it makes rule 3's
approval **the only entry path**.

**Why rule 3's ordering is asserted.** A presence check passes an approval recorded
**afterwards**, which is exactly what *"recorded before"* exists to prevent. Same
frozen-value-plus-timestamp evidence class as `inventory-and-registry` R-52 and
`external-products` R-59/R-60.

**Why four separate failures.** TA-35's criterion names two explicitly. **Several obligations
behind one check is the FR-P1-02-8 failure** — four obligations sat behind a withdrawn
`TA-29` citation for five revisions.

**Negative controls.** Use a support field as a model input with no approval ID → **fails**.
Record the approval **after** the feature-set freeze → **fails on ordering**. Read a support
field at hour *t* → fails. Use a target-hour quality field → fails. Include a support field
without an approval → **it is not in the feature set at all**.

**Acceptance.** **TA-35** — ⚠ **`Pending`**.

## R-79 — IRI denial: the data-flow limb is this unit's

**Rule (FR-P1-04-1, NFR-IRI-01, Q6 = D).** `tests/test_iri_denial.py` **must fail on
deliberate `iri_*` injection** into the ML feature path. No `iri_*` field, IRI-derived
residual, or IRI-computed value reaches ML training or inference.

**Constraint — the two limbs are different properties, split by property rather than by
unit:**

| Limb | Question | Owner |
|---|---|---|
| **Data flow** | Did an `iri_*` value reach the feature path? | **This unit** |
| **Module graph** | Can a module reach `iri.py` at all? | **`external-products` R-56** — transitive static reachability |

`governance-guards` R-23/R-24 draw the same line, and it puts each check where it can
actually be run.

**Constraint — the allowlist is NOT a denylist**, and FR-P1-04-1 is emphatic. TE §12 states
it as *"imported only by `scripts/04_build_external_products.py` and `src/evaluation/`"*, so
an import from `src/data/`, `src/gnss/`, **a training script or a notebook** violates it
**exactly as** one from `src/features/` or `src/models/` does.

**So the permitted-importer set is asserted to have exactly those two members.** A check that
only forbids `src/features` and `src/models` **passes a notebook import** — the same
exactly-one-member-exclusion shape `governance-guards` **R-19** uses, and what makes
"allowlist" true rather than aspirational.

**Constraint — IRI and GIM join only at evaluation time**, onto the **already-frozen
comparison-wide mask**.

**Negative controls.** Inject an `iri_*` field into the feature path → the denial test
**fails**, which is the required behaviour. Inject an IRI-derived residual → fails. Import
`iri` from a **notebook** → the allowlist assertion fails, where a denylist would pass. Add a
third name to the permitted set → the exactly-two assertion fails.

**Acceptance.** WS-10, TA-07 (**both owned by this unit**).

## R-80 — Folds are exact calendar boundaries, and the partition list has five partitions plus the locked month

**Rule (FR-P1-04-5, Q9 = D).** *(Columns `kind`, `train_start`, `train_end` and
`validation_month` added 2026-08-28 per Recommendations 4 and 25; the `Partition` and `Range`
columns are unchanged, and no fold boundary moves.)*

| Partition | `kind` | Range | `train_start` | `train_end` | `validation_month` |
|---|---|---|---|---|---|
| **F1** | `fold` | Jan–Mar, validation Apr | `2022-01-01` | `2022-03-31` | `2022-04-01` |
| **F2** | `fold` | Jan–Jun, validation Jul | `2022-01-01` | `2022-06-30` | `2022-07-01` |
| **F3** | `fold` | Jan–Sep, validation Oct | `2022-01-01` | `2022-09-30` | `2022-10-01` |
| **F4** | `fold` | Jan–Oct, validation Nov | `2022-01-01` | `2022-10-31` | `2022-11-01` |
| **Final refit** (`REFIT`) | `refit` | **1 Jan – 30 Nov** | `2022-01-01` | `2022-11-30` | `None` |
| **December** (`DEC`) | `locked` | **Locked** | `2022-01-01` | **`2022-11-30`** | `2022-12-01` |

Each fold carries a **24-hour embargo**; the first 24 h are **excluded and counted**. **No
random or shuffled cross-validation.** No window crosses a boundary.

> ## ⚠ `train_end` IS NOW SPECIFIED FOR ALL SIX PARTITIONS — RECOMMENDATION 25, 2026-08-28
>
> **What was wrong.** Derived across all twelve units on 2026-08-28: `train_end` appeared
> **6** times, every one a restatement of the `Partition` field list, and **no value was
> specified for any partition** — `DEC` and `REFIT` included. All six occurrences were inside
> this unit (4 / 1 / 1 across its three design artifacts), which is why the specification is
> owed here.
>
> **Why it mattered.** ADR-11's one enumerated carve-out (`REFIT` → `DEC` under
> `role="score"`) is justified at `component-methods.md:609-613` by the claim that the only
> alternative a pure identity permits is *"a `DEC`-stamped transform, i.e. **fitting on
> December**, which is the thing the lock exists to prevent."* That is true **only if
> `DEC.train_end` falls inside December.** ADR-11 states its own cost at `:628-635`: the
> invariant becomes *"'ids must match, or be the one enumerated pair' — **strictly weaker**,
> and a weaker invariant needs its own evidence."* An unspecified field therefore left the
> necessity of the one weakening unverifiable in either direction.
>
> **What is decided, and what is not.** F1–F4's and `REFIT`'s bounds are **restatements of
> FR-P1-04-5's frozen fold table** (F1 Jan–Mar … refit 1 Jan – 30 Nov) and D-8's calendar-2022
> boundary — no value is chosen here. **`DEC.train_end = 2022-11-30`** is the one genuine
> specification, applied on the owner's Recommendation 25 ruling (board option 1). It changes
> **no fold boundary, no test date and no scored range**: D-28's 2–31 December scored set
> governs `scored_start`/`scored_end`, which is a different field pair, and `DEC` is **never a
> fitting scope**.
>
> **What it buys.** A December fit becomes **unrepresentable by the field itself** — a second
> structural bar on the lock, independent of `materialise_locked_partition`'s signature guard
> (R-82) and of `locked_test.open_restricted`'s logged read. The carve-out is **retained for
> interface clarity rather than necessity**, exactly as option 1 directs: the G-06 apply stays
> the one legible enumerated pair at the gate rather than becoming an ordinary identity match.
>
> **The wart, stated rather than hidden.** `train_end` now means something different for `DEC`
> (a boundary it never fits up to) than for the folds (the boundary they do). And because both
> bounds are specified, a Jan–Nov `DEC`-stamped `train` bundle becomes **shape-representable**
> although **no call in R-81's three-call sequence and no stage script builds one** — the
> redundancy Recommendation 25's own comparison names against option 2. Closing that gap
> structurally would need a `kind == "locked"` bar on `role == "train"`, which is board option
> 3 — **not** the option ruled, and not adopted here. **Recorded as a residual for the owner at
> the gate.**
>
> **The counts this does not change, derived rather than assumed.** The fitting-capable set
> stays **five** (`F1`–`F4`, `REFIT`), so R-74's month-cell figures are unchanged:
> 3 + 6 + 9 + 10 + 11 = **39** lawful `train` month-cells, of which **10** are another
> partition's validation month (F2→Apr; F3→Apr, Jul; F4→Apr, Jul, Oct; REFIT→Apr, Jul, Oct,
> Nov). Re-derived programmatically 2026-08-28, not carried from the 2026-08-26 text.
> `build_partitions` still returns **6** and the split manifest still enumerates **5**.

**Constraint — the final refit's six freeze preconditions.** November enters **only after all
features, hyperparameters, masks, seeds, thresholds and analysis rules are frozen**. Each is
asserted with a **timestamp preceding the refit**.

**Constraint — exactly one partition per target timestamp** (Vision §8.1), **asserted over the
list's disjoint reading**: each month's **evaluation role** — Apr (F1), Jul (F2), Oct (F3),
Nov (F4), December (**locked**), training-only for the rest. It catches an **overlap** and a
**gap**, and it is the check the corrected list was added to make possible: FR-P1-04-5 records
that the omission *"left Vision §8.1's rule… with no list to check November against."*

> **⚠ The assertion cannot run over the training ranges, corrected 2026-08-23.** This
> previously read *"asserted over the complete list"*. The training ranges are an **expanding
> window** and **nest** — Jan–Mar ⊂ Jan–Jun ⊂ Jan–Sep ⊂ Jan–Oct ⊂ Jan–Nov — so **every**
> January–November timestamp belongs to two or more, and the assertion would **fail on
> ordinary 2022 data**, taking the negative control below (*"a timestamp belonging to two
> partitions → fails"*) with it. Found by an adversarial pass.
>
> **Reading adopted, and the residual.** Exactly-one holds over **evaluation role**, disjoint
> by construction, and that is what FR-P1-04-5's complaint was about — November had no role to
> check against. **This is a reading of a frozen Vision §8.1 rule, not a decision this stage
> may take**, and is raised at the gate. If §8.1 is meant literally over the training ranges it
> is **unsatisfiable as written** — a defect in the governing document, not in this design.
> **Flagged, not resolved.**

**Count, derived by reading the table above: six rows.** FR-P1-04-5 says *"enumerates all
**five** partitions"*, and both are right — **five partitions** (F1–F4, the final refit) plus
the **locked month**, which is a partition of the calendar but never a fitting scope.
Reconciled 2026-08-23.

**Constraint — membership derives from record timestamps.**
`assert_membership_from_timestamps` raises on any row whose month or year disagrees with its
partition — the defect that filed locked-month records into `audit_evidence_2022-01/`.

> ## ⚠ THE OPEN SHAPE DECISION IS DISCHARGED BY ADR-11 — NOTED 2026-08-26
>
> **Superseded open item, preserved:** *"the final refit is not a `FoldSpec`. That dataclass
> carries `validation_month`; the final refit has none. Its representation alongside the four
> folds is raised at the gate — together with R-74's element 4, since `fit_transforms` takes a
> `FoldSpec` and the refit's transform has no fitting path until this is settled. One decision,
> not two, and G-06 depends on it."*
>
> **Resolved upstream, 2026-08-23:** ADR-11's **`Partition`** (`partition_id`,
> `kind: fold | refit | locked`, `train_end`, `validation_month: date | None`,
> `embargo_hours=24`) represents all six rows of this rule's table — `None` means **the final
> refit alone**, and `DEC` carries **2022-12-01** — and `build_partitions(snapshot)` returns
> exactly them. Both `fit_transforms` and `build_features` take `Partition`s, so the refit has
> a fitting path and G-06's apply is the enumerated `REFIT` → `DEC`/`score` pair (R-74).
> **This rule's closed six-row value space is unchanged** — which is what
> `models-and-baselines` relies on it for: `partition_id` cannot take a seventh value without
> this table changing first.
>
> **The two counts, from ADR-11's M5 amendment:** `build_partitions` returns **6**; the
> **split manifest FR-P1-04-5 gates on enumerates 5** (`F1`–`F4`, `REFIT`, each with training
> range, validation month and excluded count); the locked partition record (`DEC`, its
> evaluated month, its access-gate state) is recorded **separately**, because it is
> access-gated and the manifest is not. A split manifest carrying six rows **fails**
> FR-P1-04-5, and so does one carrying four.

**Negative controls.** Let a window cross a fold boundary → fails. Omit the excluded-row count
→ fails. Run the final refit before any of the six freezes → **fails on ordering**. Give one
month **two evaluation roles**, or leave a 2022 month with **none**, → **the exactly-one
assertion fails**. Derive membership from a directory name → fails.

**Control that must *not* fire** (corrected 2026-08-23): a **15 February** timestamp lying in
F1's, F2's, F3's, F4's **and** the refit's training ranges → **passes**. That is the expanding
window working as designed, and the previous wording — *"a timestamp belonging to two
partitions … fails"* — made it a defect, which would have failed the assertion on every
January–November row in the dataset.

**Acceptance.** WS-12, TA-11 (**both owned by this unit**).

## R-81 — One window definition, and WS-13's evidence question stays open

**Rule (FR-P1-04-8, restated 2026-08-26 on ADR-11).** `windows.py` emits **both** the
flattened matrix and the sequence tensor for a feature-set ID, and the two travel **in one
`FeatureBundle`** — `component-methods.md`: *"Both representations come from **one** window
definition in `windows.py` and now travel in one object, so FR-P1-04-8 holds by construction
rather than by assertion."*

**Constraint — transforms reach both representations natively.** The `NDArray` tensor carries
no record timestamps, so no row-level check can reach it; ADR-11 applies the `Transform` to
the assembled feature frame **inside `build_features`, before windowing**, and `build_features`
is the **only** producer of either representation — *"a transformed matrix beside an
untransformed tensor is no longer constructible."* The `transform` parameter is part of the
approved signature; **the amendment this constraint previously cost dissolved into ADR-11**
(§ Amendments owed).

> **Historical boxes and superseded amendment, preserved (rebuilt 2026-08-26).** The two dated
> ⚠ notes below record the retired lineage — the unexecutable first statement and the
> `transform`+`purpose` amendment this rule owed on the retired interface.
>
> **⚠ The first statement was unexecutable.** It read *"both representations are built from a
> frame that has already passed element 4"*. But `build_features(...) -> tuple[DataFrame,
> NDArray]` emits **both in one call that takes no `Transform`**, and the transform is fitted
> on the features **that call produces** — no transformed frame exists before windowing.
>
> **Resolution as previously stated, superseded:** `build_features` gains
> `transform: Transform | None = None` and `purpose: ApplyPurpose | None = None`, travelling
> together, supplying one without the other raising.
>
> **⚠ `purpose` was missing from the first statement** (corrected 2026-08-23): a `transform`
> with no `purpose` meant the tensor path either **bypassed element 4** or had **no
> determinable accepted set**.

**Three calls per partition, and the call count is unchanged by the redesign** *(FU-6 = A,
re-derived 2026-08-26 against ADR-11)*. The approved sequence for partition *k* is three
`build_features` calls plus one `fit_transforms`: `raw` (`transform=None`, `transform_id`
`None`) over the training range, the bundle `fit_transforms` is fitted on; `train`
(`transform=T_k`) over the same range; `score` (`transform=T_k`) over the validation month.
`services.md`'s M13 box counts all three constructions in the cost envelope, and its M9 box
gives each bundle a distinct address (`<partition_id>__<role>__<transform_id>/`, literal
`untransformed` for `None`), so the artifact inventory and the call count agree.

**The fitting call's output is consumable by nobody.** FU-6 = A's *"never emitted, never
persisted"* limb is modified by the approved contract — the raw bundle **may persist,
visibly, at its `untransformed` address** (M9: so a reviewer can see one was produced) — and
its load-bearing limb survives strengthened: **consuming it is a contract raise**, since
`fit_predict`, `06` and `07` raise `LeakageError` on any bundle whose `transform_id is None`.
**Negative control (ADR-11 form):** a bundle with `transform_id is None` — or an identity-less,
bundle-less frame — reaching **M-06 fails**.

**Which rows are scored is declared, not derived** *(FU-5 = D mapped; one element defeated —
see `business-logic-model.md` W-4b)*. `FrameSpec.scored_start`/`scored_end` declare the scored
range; `build_features` validates containment — training range for `role="train"`,
`validation_month` for `role="score"` — and the emitted bundle's rows are the scored range.
**Control:** a `score` spec exceeding the validation month → **raises**. Windows reaching
before `scored_start` are **excluded and counted** (FR-P1-04-5; ADR-11's `lead_in_hours`
removal), which is the December consequence the W-4b conflict box raises at the gate.

**Two emitting calls are not the rejected "double call".** What W-4 rejects is transforming the
matrix of a single call while that call's tensor stays untransformed — one feature-set ID, two
disagreeing representations. Here each emitting call emits both representations already
transformed and consistent, inside one bundle. Re-windowing would create a second definition;
the tensor cannot be transformed directly. **Nothing here owes an amendment** — the "seventh"
and "eighth" this paragraph previously declared dissolved into ADR-11 (§ Amendments owed).

**Negative controls.** Build a tensor from a frame carrying rows outside its transform's
permitted set → **fails**. Emit a transformed matrix beside an untransformed tensor for one
feature-set ID → **fails** on parity.

**Constraint — parity is asserted anyway.** Structural does not mean unverified: the two
representations for a given feature-set ID must contain the same underlying window values.

> **WS-13's evidence departs from TE §16, and no reading is adopted — here or upstream.**
> TE §16 names `test_common_masks.py`, owned by **`evaluation-and-comparison`**. The story map
> substitutes *"matched-window parity assertion over one `windows.py` definition"* and records
> that *"the substitution is defensible… but **no reading is adopted here**."* **This stage
> adopts none either** (Q5 = D) and carries the departure to the gate.
>
> **The question is narrower than it looks: `test_common_masks.py` is already required here
> through TA-11**, whose evidence column names it alongside `test_split_embargo.py`,
> `test_train_only_transforms.py` and the parity assertion — and **TA-11 is this unit's row**.
> So the mask test runs whichever way WS-13 resolves. What is open is which row cites it.

**Negative controls.** Emit a flattened matrix and a sequence tensor whose window values
disagree → the parity assertion fails. Build the two from separate window definitions → the
one-definition property fails.

**Acceptance.** WS-13, TA-11 (**both owned by this unit**).

## R-82 — The locked partition materialises only against a verified signature

**Rule (FR-P1-04-5's December limb, WS-18).** `materialise_locked_partition` materialises the
December partition **only** when `g05_signature` is **present and verifies**. **Raises
`LockedTestError`** when it is `None` or fails verification — the **pre-G-05 execution
block**.

**Constraint — two guards, deliberately separate (ADR-03).** A **read** for the required
pre-G-05 coverage audit does **not** come through here; it comes through `governance-guards`'
`locked_test.open_restricted`. **The coverage audit is a required read; the metrics run is
barred until after G-05.**

**Constraint — `tests/test_locked_test_guard.py` is owned here** because it exercises **both**
limbs and this unit already depends on `governance-guards`; assigning it there would **close a
cycle**. `governance-guards` supports WS-18 and TA-18.

**Negative controls.** Materialise December with `g05_signature=None` → **raises**. With a
signature that fails verification → raises. With a verified signature → materialises, and a
test asserts it does. Route a coverage-audit read through this function → it is the wrong
door; the read belongs to `open_restricted`.

**Acceptance.** WS-18, TA-18 (**both owned by this unit**).

## R-83 — `Partition` states BOTH bounds of the training range (BLK-09)

> **Added 2026-08-28 on `GOV-2026-08-28-FD-01` Recommendation 4 (board option 1), the
> stage-3.1 exit condition `unit-of-work.md:867` assigns to this unit **solely** and `:857`
> records as *"Open. Exit condition on stage 3.1"*.** The id takes the head of the **observed
> R-83…R-89 gap** between this unit (R-74…R-82 plus R-76a) and `models-and-baselines`
> (R-90…R-102) — four sibling units record that gap as *"observed, not explained"*, and
> nothing occupies it. **No existing rule id moves**, so `models-and-baselines`' live
> citations of **R-80** and **R-76a's third limb** are untouched. R-76a's preserved box
> reasons about renumbering *itself* to R-83; that hypothetical target is now taken, which
> strengthens its conclusion rather than weakening it.

**The defect, stated before the rule.** `Partition` carried `partition_id`, `kind`,
`train_end`, `validation_month` and `embargo_hours` — and **no `train_start`**. R-74 elements
1 and 2 compare a bundle's scored range against *"the partition's training range"*, and the
approved contract's own closing note says what that cost, quoted from
`component-methods.md:904-906`: *"`Partition` carries no `train_start`, so the training-range
comparisons in `fit_transforms` and `build_features` rest on an unwritten January-1 convention
(Major)."* With only an upper bound in scope, `[scored_start, scored_end] == training range`
**had no lower bound to compare against**, while this unit's own live text asserted the
equality *"is checkable"*. The blocker was not merely unresolved: it had been **de-labelled**
— `BLK-09` appeared **0** times in all four of this unit's artifacts, derived 2026-08-28 by
two board seats independently and re-derived here before the fix.

**Rule.** `Partition` carries **`train_start: date`** alongside `train_end`, and both
`fit_transforms` and `build_features` read **both** bounds from the `Partition`:

```
@dataclass(frozen=True) Partition:
    partition_id: str
    kind: str                      # fold | refit | locked
    train_start: date              # ADDED 2026-08-28 — R-83, BLK-09
    train_end: date
    validation_month: date | None
    embargo_hours: int = 24
```

**Constraint — the value is configuration, not source.** `build_partitions(snapshot)` reads
`train_start` and `train_end` from **`configs/data.yaml`**, so **TC-03e is satisfied**. A
hard-coded `2022-01-01` in `src/data/splits.py` is **barred** — `project.md` § Forbidden:
*"NEVER hide a scientific constant in source code or a notebook"* — and the §18.3 preflight
`TBD` assertion covers the field before any component that reads it is implemented.

**Constraint — it is never derived from the data.** Deriving `train_start` from the earliest
row present would make the equality check **compare the range against itself**: a tautology, a
check that can never fire, indistinguishable from one that passes. That is this unit's own
stated anti-pattern — R-74's empty-frame control exists because *"a check that never fired
must not pass for one that did"* — and Recommendation 4 names it as one of the three
implementer paths this rule closes. Under it, a transform fitted on a strict subset of the
declared training range would be accepted, stamped with the partition id, pass the apply-side
identity check, and produce standardization constants differing from the declared fold
protocol **with no downstream symptom**.

**No scientific value is decided here.** Every bound is already frozen: FR-P1-04-5's fold
table and D-8's calendar-2022 claim boundary put `train_start` at **2022-01-01** for all six
partitions (R-80's table). What this rule changes is **where the value lives** — a field
sourced from config rather than an unwritten convention — and **what reads it**.

**Negative controls.**
- A `train` bundle whose scored range is a **strict subset** of the partition's training
  range — F4 (`2022-01-01`…`2022-10-31`) fitted on `2022-02-01`…`2022-10-31` →
  **`LeakageError`**. This is the direction the missing lower bound admitted.
- A `train` bundle whose scored range is **over-wide** — F1 fitted through `2022-11-30` →
  **`LeakageError`** (unchanged; `train_end` already bounded this direction).
- `train_start` absent or `TBD` in `configs/data.yaml` → the §18.3 preflight assertion
  **fails**, before the component that reads it is implemented.
- `train_start` hard-coded in source → the TC-03e scientific-constant check **fails**.
- `train_start` derived from the data's earliest row → the strict-subset control above
  **passes when it must fail**, which is how the tautology is detected rather than reasoned
  about.

**Why both directions raise `LeakageError` and not one each.** Range equality is **one
condition with two directions**. The over-wide direction is information flow outright; the
strict-subset direction is a fit that silently departs from the declared protocol every
downstream number then inherits. Splitting one condition across two exception types would
reintroduce exactly the cross-caller ambiguity Recommendation 8 exists to remove, so both
raise `LeakageError` and the **identity** disagreement — a different condition — raises
`PartitionError`.

**Amendment owed, and its granularity.** `train_start` is a field of a **cross-package** shape
(`src/data/splits.py`'s `Partition`, consumed by `src/features` and `src/models`), so it is an
amendment to the approved `component-methods.md` — **not** an intra-package shape § Depth
grants this stage. It is bundled with R-74 element 2's `PartitionError` reassignment as **one**
consolidated change record, the granularity precedent being R-55's one amendment for three
`src/external` boundary blocks and R-103's one amendment for four surfaces. See § Amendments
owed, which prints the arithmetic.

**Status.** **BLK-09 remains an open exit condition on stage 3.1 for this unit** until that
amendment is approved. This rule authors the contract the register requires; **approving this
design is not that approval**, on the same terms BLK-04 carries. Five sibling units record the
resolution as owed here — `evaluation-and-comparison`, `fixtures-and-reproducibility`,
`models-and-baselines`, `regimes-diagnostics-reporting`, `statistical-inference` (derived
2026-08-28); **three** of them name the `train_start` field itself.

**Acceptance.** TA-11, through FR-P1-04-6 and NFR-LEAK-01 — the same row R-74 carries. **No
new row is claimed**, and none is available: NFR-LEAK-01's evidence is owed to the
**Supervisor at G-04 and G-05**.

## R-84 — BLK-08 half B, narrowed to `ABL-DIFF` (this unit's half of the joint contract)

> **Added 2026-08-28 on `GOV-2026-08-28-FD-01` Recommendation 7, as narrowed to `ABL-DIFF` by
> the project decision owner on the strength of **D-27** (2026-08-24).**
> `unit-of-work.md:842` makes BLK-08 an exit condition *"for both owning units … none may
> exit without the contract"*, and `:416` names this unit co-owner *"where `Transform` and its
> fitted state live"*. Derived 2026-08-28 before this rule existed: across all four of this
> unit's artifacts `BLK-08` = **0**, `inverse` = **0**, `TECU` = **0**, `ABL-DIFF` = **0**,
> `D-27` = **0** — the co-owner's half existed nowhere, exactly as
> `evaluation-and-comparison` R-103's own dated box records. **D-27 is cited zero times in
> `evaluation-and-comparison` and `statistical-inference` too** (derived); those two units are
> receipted and this stage does not edit them, so the omission is raised at the gate.

**First, the register's "states first" question — answered by citing the freeze, not by
inferring it.** **D-27** froze the premise: *"The **primary configuration's train-only
transform does not touch the target.** It acts on target-**derived input features**; the
target itself remains **raw TECU**."* Its evidence is TE §7.2's `ABL-DIFF` row, whose
**Primary remains** column reads **"Raw TECU"**, and TE §6.2's dictionary, whose only
train-only standardization on anything target-derived applies to the **inputs**
(`vtec_lag_1h/2h/3h/24h`, `vtec_seq_24` — *"Train-only standardization for ridge/LSTM; none
for RF"*).

**Stated explicitly, as D-27's Consequences require: the primary path needs no inverse
transform.** Model output is already in raw TECU, so the paired loss differential, the vector
time-block bootstrap interval and the practical-relevance threshold are computed on the
quantity the model emits. D-27 requires this *"stated explicitly … in the design so the
`ABL-DIFF` obligation is visibly satisfied rather than silently assumed"*; this paragraph is
that statement on this unit's side of the joint contract.

**Rule — half B, and it is `ABL-DIFF`'s alone.** `ABL-DIFF` is the one predeclared
configuration that transforms the target (TE §7.2: the target becomes a first difference and
*"predictions inverse-transformed to absolute TECU before any metric is computed"*). For that
configuration and no other:

| # | Obligation | Shape |
|---|---|---|
| 1 | **Persistence** | Each fitted `Transform` is persisted **retrievably by `transform_id`**, alongside the bundle carrying that id (`<partition_id>__<role>__<transform_id>/`, M9) |
| 2 | **Resolution** | `src/features` exposes **`load_inverse(transform_id) -> Inverse`**. `Inverse` exposes **`inverse(frame) -> DataFrame`** and **nothing else** |
| 3 | **Declaration** | `Transform` declares its target-touching status **machine-readably** (`touches_target: bool`, name indicative), so D-27's reading is **checked, not trusted** |
| 4 | **Round trip** | `inverse(apply(x)) == x` within the declared fixture tolerance (`tests/fixtures/<fixture_id>/fixture_manifest.yaml`, §15.2 — **no tolerance value is decided here**), hosted **inside `src/features`**, where `apply` is visible |

**Why `load_inverse` and not `load_transform`.** R-103 half A as drafted exposes
`load_transform(transform_id) -> Transform`, and a `Transform` carries `apply`. ADR-11's own
words at `component-methods.md:595-600`: *"**`apply_transforms` is removed.** A function that
applies a fitted transform to an arbitrary frame **is** the hole"* — five review cycles
established that its constraint *"cannot be expressed over rows"*. Handing a `Transform`
across a package boundary reconstitutes `apply_transforms(frame, transform)` one package away
from the frozen comparison-wide mask and the G-06 path, **invisible to the identity check**,
which lives inside `build_features` rather than on `Transform`. **`Inverse` is therefore a
distinct, apply-less type**: the leak stays structurally unrepresentable rather than
prohibited by review — the trade ADR-11 refused, and R-103's own failed-refutation section
examined the *edge* without examining the *object the edge carries*.

**Why the round trip runs here.** `apply` is reachable only inside `src/features` under
ADR-11, so a round-trip control hosted in `src/evaluation` would have no `apply` to call.
Hosting it here is where it can execute — the same **split-by-property** reasoning R-75 uses
against `external-products` R-57 and R-79 against R-56.

**Constraint — the import edge is owed and UNAPPROVED, not adopted.** `src/evaluation` →
`src/features` is **`—`** in `component-dependency.md` § Dependency matrix, and **D-27
withheld authorisation in terms**: the reading *"no longer requires a general
`src/evaluation` → `src/features` route for the primary path"*, and *"**No import-boundary
change is authorised by this decision.** The §12 rule and its allowlist are untouched."* The
edge is therefore recorded as **an amendment owed and a gate item**, on the `ABL-DIFF` path
only. Nothing here grants it, and **no module is created**.

**Divergence from R-103 half A, raised rather than resolved.** `evaluation-and-comparison` is
terminal-READY under a frozen receipt and **this stage does not edit it**. Its half A names
`load_transform(transform_id) -> Transform`; this half B narrows the exposed surface to
`load_inverse` / `Inverse`. The two halves must agree before BLK-08 closes, so the
reconciliation is **an owner item at the gate** — and R-103's own box already anticipates it:
half B is *"not binding until the owner rules how `features-and-splits`' receipted artifacts
take it (re-entry, addendum, or annexed contract)."*

**Status — the two limbs, kept apart.** BLK-08's **premise limb closes for the primary path**:
the primary configuration does not touch the target (D-27), so the primary path owes no
inverse and exercises no edge. BLK-08's **mechanism limb stays open, narrowed to `ABL-DIFF`**,
in D-27's own words — *"BLK-08's mechanism limb narrows and stays open."* **BLK-08 remains an
open exit condition on stage 3.1 for both owners.**

**Negative controls.** A `Prediction` whose `transform_id` resolves to no persisted transform
→ **raises**, naming the identifier and the store searched (R-103 half A's
`InverseTransformError`, raised at the caller). A resolved inverse whose `inverse(apply(x))`
differs from `x` beyond the declared fixture tolerance → **fails**. An `Inverse` exposing any
method that applies a transform to an arbitrary frame → the **surface assertion fails**
(`Inverse` has exactly one public method — the same exactly-one-member shape R-79 and
`governance-guards` R-19 use). A `.apply(` call on any `load_*`-obtained object **outside
`src/features`** → the **static source check fails**, with no runtime raise involved and none
possible — the same static-check class R-76a's limb 3 uses, and the closure evidence
Recommendation 7 names. A primary-configuration `Transform` declaring `touches_target = True`
→ **refused at every metric entry point unless inverted** (R-103 half A, R-104), so a wrong
recording of D-27's reading is caught rather than believed.

**Acceptance.** ⚠ **No row** — BLK-08 closes at the register, not at a checklist row, the same
posture R-103 records. TA-07's import-boundary evidence at **G-P2** covers the edge **if** the
owner grants it.

---

## The four requirements whose rows exist but have never run

| Requirement | Rule | Row | Status |
|---|---|---|---|
| FR-P1-04-12 | R-76 | **TA-33** | **`Pending`** — *"the row exists, no test module is implemented, none has been executed, and none has passed"* |
| FR-P1-04-13 | R-77 | **TA-34** | **`Pending`** |
| FR-P1-04-16 | R-78 | **TA-35** | **`Pending`** |
| FR-P1-04-17 | **R-76a** (the `build_features` raise) | **TA-36** | **`Pending`** — story-map **supporting** unit, but **this unit owns TA-36's primary test**; see R-76a |

**All four were approved 2026-08-22** under Vision §15.2 (`CR-2026-08-22-LEAKAGE-TA`), and
they cover this unit's **leakage-sensitive controls**.

> **No artifact, manifest or report may state or imply that FR-P1-04-12, -13 or -16 is
> covered, satisfied or verified.** A row is not a result.

## FR-P1-04-10 — the one requirement with no acceptance row

**1 of this unit's 11**, derived from story-map § Per-unit coverage summary, which reads
`features-and-splits (1)`.

| Requirement | Rule | Evidence that would close it |
|---|---|---|
| **FR-P1-04-10** | R-76 | An approved §19 row asserting **raw longitude never enters as a predictor** and that longitude enters **only** through `lst_sin` and `lst_cos`, **plus a passing result**. The feature manifest containing no raw-longitude column is the criterion; **a manifest check is not a row** |

> **§ 7's "five forbidden edges with no row" is superseded — derived, not recounted.** TA-33
> covers dictionary closure; **TA-34 covers both** the `vtec_lag_*` carry-forward prohibition
> **and** the target-lag contract, which are one requirement; TA-35 covers the support-field
> rules; TA-36 covers driver-interval repetition — story-map **primary `external-products`**,
> but its **enforcement raise and primary negative-path test are this unit's** (R-76a,
> reconciled at `external-products` R-54a). **Corrected 2026-08-23** from *"is
> `external-products`' row"*, which read one table and stopped.
> **Remainder: FR-P1-04-10 alone.**

## Amendments owed

**Re-derived from scratch, 2026-08-28, after Recommendations 4 and 7** — the arithmetic is
printed before it is asserted: **5 + 1 + 1 = 7, across 5 units**. *(The 2026-08-26
re-derivation, `5 + 0 = 5 across 3 units`, was correct on the day it was written; it is
superseded because this unit now owes one amendment again — see the row below.)*

| Source | Owed | Basis |
|---|---|---|
| `external-products` **R-55** | **5**, across **3** units | Derived there (`acquisition` 3, `inventory-and-registry` 1, `external-products` 1), boundary contracts only. **Not restated here**; a restated count drifts. None of its five rows touches the surface ADR-11 redesigned. |
| `evaluation-and-comparison` **R-103** | **1**, **1** unit | Derived there and **not recounted here**: *"the BLK-08 resolution package (R-103), one consolidated amendment"* — the `component-dependency.md` row for the `src/evaluation` → `src/features` edge, `component-methods.md`'s resolver surface, `Transform`'s target-touching declaration, and `Prediction`'s inversion-lineage field. **R-84 changes that amendment's *content*, not its count**: the resolver narrows from `load_transform(...) -> Transform` to `load_inverse(...) -> Inverse`, and the round-trip control relocates into `src/features`. Counting a second amendment for the same package would double-count the co-owner surfaces R-103 already carries as *"pending adoption"*. |
| **This unit** | **1** | **The BLK-09 resolution package (R-83), one consolidated change record**: `train_start: date` added to `src/data/splits.py`'s `Partition` in `component-methods.md`, **and** R-74 element 2's `PartitionError` reassignment for the `spec.partition_id != partition.partition_id` limb, which the approved contract at `component-methods.md:642-648` currently types `LeakageError`. One coherent record, the same granularity as R-55's one amendment for three `src/external` boundary blocks and R-103's one for four surfaces. |
| | **7 across 5 units** | 5 + 1 + 1 |

**The five units, named so the count can be checked rather than trusted:** `acquisition`,
`inventory-and-registry`, `external-products` (R-55's three), `evaluation-and-comparison`
(R-103), `features-and-splits` (R-83).

**What owes nothing, and why — stated so a later sweep does not add it back.** R-80's six
`train_end` and `train_start` **values** are `configs/data.yaml` content, not a boundary
shape, so they add no amendment: the field pair itself is the amendment (R-83), and the values
that fill it are configuration. This follows `evaluation-and-comparison`'s own § Amendments
owed reasoning for its Q5 — *"configuration content, not a boundary contract"*.

> **⚠ The 5-unit coincidence is NOT agreement — checked, because it invites exactly the error
> this project has recorded twice.** The stale figure in `models-and-baselines`' frozen
> artifacts is *"**8** across **5** units"*; this re-derivation is *"**7** across **5**
> units"*. The unit **count** matches and the **total** does not, and the two figures do not
> describe the same set: the stale one counted three unit-local amendments that dissolved into
> ADR-11 and reached `models-and-baselines`/`evaluation-and-comparison` through FU-4's stamp;
> this one counts R-55's three units plus `evaluation-and-comparison` and this unit. A sweep
> comparing totals would have called this a disagreement and a sweep comparing unit counts
> would have called it agreement; **only the named set-difference settles it**
> (`project.md` § Way of Working, c21).

> **The superseded totals, preserved in order:** *"five across three"* (the first two
> element-4 remedies, which avoided a signature change and did not work) → *"7 across 4"* →
> *"8 across 5"* (FU-4 = D's stamp) → *"5 across 3"* (2026-08-26, the ADR-11 rebuild, when
> all three unit-local amendments had dissolved) → **"7 across 5"** (2026-08-28, R-83's
> `train_start` package plus R-103's counted-there BLK-08 package). All three of the 2026-08-24
> unit-local amendments mechanised the retired interface; ADR-11 absorbed their substance.
> **R-83's amendment is new, not a revival of any of them.**

> **Raised at the gate, not edited (frozen READY artifacts):** `models-and-baselines`'
> `business-rules.md` and `domain-entities.md` both state, in their Assumptions, *"the total
> stays **8 across 5 units**."* That figure is stale — the correct
> total is **7 across 5 units** *(updated 2026-08-28; it read "5 across 3 units" from
> 2026-08-26 until R-83 was added)* — but those artifacts are terminal-READY under a frozen
> receipt and this stage does not edit them. Their citations of **R-80** and **R-76a's third
> limb** remain valid: both rules keep their ids, subject matter and limb structure, and R-80's
> table gains columns without moving a boundary. `evaluation-and-comparison`'s own
> § Amendments owed derives *"6 across 4 units"*, which was correct there on 2026-08-26 and is
> now **7 across 5** by the same arithmetic once R-83 is counted; that unit is receipted and is
> **not edited** either, so the reconciliation is a gate item.

**What § Depth's intra-package carve-out still covers, and what therefore owes nothing:**
`Transform`'s fitted state, `windows.py`'s internals, the excluded-row counters, and every
other `src/features/*` / `src/data/splits.py` shape beyond the named boundary calls.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence, so this unit opens at **R-74**. If per-unit numbering was intended, say so at the gate. *(Extended 2026-08-28: this unit now closes at **R-84**, taking the head of the observed **R-83…R-89** gap between R-82 and `models-and-baselines`' R-90. Derived — nothing occupies R-83…R-89, and four sibling units record the gap as "observed, not explained". No existing id moves, so `models-and-baselines`' **R-80** and **R-76a's third limb** citations are untouched.)*
- **[assumption]** **`PartitionError` is declared where `src/features` and `src/data` can import it.** Recommendation 8's ruling promotes it to `foundation` R-01's **fifteenth** and states it is declared in **`src/models/`** — but `component-dependency.md` § Dependency matrix marks **`src/features` → `src/models`** and **`src/data` → `src/models`** as **`—`** (no import in either direction), and every `PartitionError` raise in this unit lives in `src/data/splits.py` or `src/features/*`. **On the matrix as approved this unit cannot raise it at all.** The natural declaration site is **`src/data/config.py`**, where R-01 already declares `IntegrityError` and `foundation`'s six and which every unit already imports. This artifact is written on that reading; **the declaration site needs an owner ruling at the gate**, and if it stays in `src/models/` the alternative is that this unit's raises revert to `LeakageError` and the R-92/R-105 taxonomy disagreement is resolved at `models-and-baselines` instead. *(Raised 2026-08-28 per Recommendation 8; `foundation` R-01 on disk still reads "all fourteen" and names no `PartitionError`, so the amended enumeration is cited as ruled, not as written.) ⚠ **SWEPT 2026-08-28 on the resume pass — this disk-state claim is SUPERSEDED.** `foundation` R-01 **has been amended** and now reads **fifteen**, with `PartitionError` promoted into the enumeration, the count restated as **derived and printed** rather than carried in prose, and `InverseTransformError` **explicitly disposed** — not a sixteenth, riding R-01's *"any future integrity-related exception"* clause, on the stated ground that the two units raising it agree on its condition and meaning, so nothing needs reconciling. Verified at `foundation/functional-design/business-rules.md` R-01 (the amendment row, the superseded-wording box, and the `InverseTransformError` box). **The dependency this sentence recorded is discharged; any open item stated alongside it is NOT** — see the sentence it accompanies.*
- **[assumption]** The **story map governs** where it and `unit-of-work.md` § 7 disagree. `business-logic-model.md` § The `unit-of-work.md` sweep shows **ten of twelve sections agree**, and the two that do not are exactly the two `CR-2026-08-22-LEAKAGE-TA` touched — so this is **one change record that missed two sections**, not a pattern in the file.
- **[assumption]** `src/features/*` and `src/data/splits.py` shapes beyond the named boundary calls are **intra-package** and this stage's to specify — **still true, but this unit now owes one boundary amendment again**: R-83's `train_start` field on `Partition` is a **named boundary shape**, not an intra-package detail, so § Depth's carve-out does not reach it. Running total **7 across 5 units**, re-derived in § Amendments owed with the arithmetic printed. *(Rewritten 2026-08-28 per Recommendation 4. The three amendments this entry recorded as dissolved into ADR-11 stay dissolved; R-83's is new. The entry read "5 across 3 units" from 2026-08-26 and "8 across 5 units" before that; every superseded total is preserved in § Amendments owed's box.)*
- **[assumption]** `tests/test_locked_test_guard.py` is this unit's, per § 7.
- **Open — BLK-04 is an EXIT condition** on this unit and on `models-and-baselines`, `evaluation-and-comparison`, `statistical-inference` and `regimes-diagnostics-reporting`. **R-74 is the contract; approving this design is not its approval.** NFR-LEAK-01's evidence is owed to the **Supervisor at G-04 and G-05**.
- **Open — BLK-09 is an EXIT condition on THIS unit, solely** (`unit-of-work.md:867`; `:857` "Open. Exit condition on stage 3.1"; `:333` "no affected unit may complete or exit 3.1 without its approved contract", per `GOV-2026-08-22-REM-01` REM-02). **R-83 is the contract**, authored 2026-08-28 per Recommendation 4 — `train_start: date` on `Partition`, sourced from `configs/data.yaml`, with both bounds read from the `Partition` and a strict-subset negative control. **Approving this design is not the amendment's approval**, and until it is approved the blocker stands. Recorded here because the earlier artifacts had **de-labelled** it: `BLK-09` = 0 across all four files before this remediation.
- **Open — BLK-08 is an EXIT condition on this unit and on `evaluation-and-comparison`, for both owners** (`unit-of-work.md:842`). **R-84 is this unit's half B**, narrowed to `ABL-DIFF` on **D-27**. Its **premise limb closes for the primary path** (the primary transform does not touch the target, so no inverse and no edge are needed there) and its **mechanism limb stays open, narrowed**, in D-27's own words. Two items ride it to the gate: the `src/evaluation` → `src/features` edge, **owed and unapproved** because D-27 states *"no import-boundary change is authorised by this decision"*; and the divergence between R-84's `load_inverse` / `Inverse` and R-103 half A's `load_transform` / `Transform`, which this stage cannot resolve because `evaluation-and-comparison` is receipted.
- **Open — `PartitionError`'s declaration site** (see the `[assumption]` above). On the approved dependency matrix, a `src/models/` declaration is unreachable from this unit's modules.
- **Open — a Jan–Nov `DEC`-stamped `train` bundle is shape-representable and built by no call**, the residual of Recommendation 25's option 1 (R-80's dated box). Closing it structurally is board option 3, which was not ruled; carried to the gate rather than adopted.
- **Open — TA-33, TA-34, TA-35 and TA-36 are `Pending`.**
- **Open — `unit-of-work.md` §§ 6 and 7 are stale on coverage figures, and § 5 on a module count.** Reported at the gate for one annotate-in-place decision; **not edited**.
- **Open — WS-13's departure from TE §16** (R-81). No reading adopted, here or upstream.
- **CLOSED 2026-08-28 by D-28 — the FU-5/ADR-11 December conflict.** Formerly *"Open — FU-5 = D's December consequence conflicts with ADR-11's `lead_in_hours` removal (two owner decisions; see `business-logic-model.md` W-4b)"*. **D-28** (2026-08-28, project decision owner under the recorded authority equivalence, on `GOV-2026-08-28-FD-01` Recommendation 6) freezes the G-06 locked-test scored set as **2–31 December 2022 inclusive, 30 days**, first 24 h **excluded and counted**, with the Vision §8.2 / TE §7.1 `—`-cell authority conflict **disclosed and carried to G-05, not resolved**. The superseded FU-5 = D wording stays as the dated history it already is, in the W-4b box and in R-74's boxes. What D-28 adds is the record, not the number — and it adds two obligations this unit does not own: a **revised split manifest** at G-05 (Vision §8.2), and the 30-day disclosure on every claim surface (Recommendation 16, open elsewhere).
- **Discharged 2026-08-26 — the final-refit representation** (R-80's dated box): ADR-11's `Partition` resolves the former *"final refit is not a `FoldSpec`"* open item. Kept in this list so the gate sees the item closed rather than vanished.
- **Open — FR-P1-04-10 has no acceptance row.**
- **Open — an unresolved station registry blocks `station_lat` and excludes `lst_sin`/`lst_cos`** (R-76). Consumed from `inventory-and-registry` R-45/R-46; **not decided here**.
- **G-09 is not signed**, and **BLK-04 independently bars implementation.**
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
> gate rather than applied. **R-80 below is named in one of them**: `models-and-baselines` records
> the no-second-test-period prohibition as an obligation **this** unit owns, because R-80 fixes the
> partition list to six closed rows. The reviewer verified that ownership claim directly.

---

> **Re-saved 2026-08-26 under the fourteenth-redo re-confirmation receipt, after completing the
> iteration-5 remediation.** In this file: the Sources list corrected (finding 10 — R-24 in,
> R-25/R-28 out, matching the siblings' 2026-08-23 correction); R-74's accepted-set `evaluate`
> row completed with the read/emit split and its dated note (finding 9); the element-4 table's
> applying-failure row aligned with W-4b; R-76a's id and filing position kept with the reason
> stated (finding 11a). **BLK-04 remains an open exit condition. G-09 remains unsigned.**

---

> **Rebuilt 2026-08-26 on the ADR-11 contract (owner ruling), after the fourteenth-receipt
> adversarial pass returned NOT-READY on the headline Critical that every mechanism above
> targeted the retired `apply_transforms` interface.** In this file: R-74's four elements, its
> negative controls and its must-not-fire controls restated on `FeatureBundle`/`Partition` and
> the identity check; R-80's open refit-shape item discharged by `Partition` with the
> six-partitions/five-manifest-rows rule added; R-81 restated on the single-producer bundle
> with the FU-6 call-count re-derivation; § Amendments owed re-derived to **5 across 3 units**
> with the stale "8 across 5" in `models-and-baselines`' frozen artifacts raised at the gate;
> the FU-5/ADR-11 December conflict raised, not resolved. Rule ids, subject matter and limb
> structures unchanged; every prior dated box preserved as history. **BLK-04 remains an open
> exit condition. G-09 remains unsigned.**

---

> **Re-saved 2026-08-26 under the post-rebuild re-confirmation receipt. The December conflict is
> now RESOLVED by FU-7 = A**: the G-06 locked test scores 2–31 December (30 days) per ADR-11 and
> FR-P1-04-5; FU-5 = D's December clause is superseded as dated history (owner ruling 2026-08-26,
> recorded under the authority equivalence). The conflict boxes above stand as the record of how
> it was raised. **BLK-04 remains an open exit condition. G-09 remains unsigned.**

---

> **Remediated 2026-08-28 under the post-redo receipt floor, on governance report
> `GOV-2026-08-28-FD-01` (verdict FAIL) and the project decision owner's rulings.** In this
> file: the header remediation box added; Sources extended with D-27, D-28, the governance
> report, R-103/R-104 and `component-dependency.md`; **R-74** element 1 rewritten on both
> bounds and element 2 split between `LeakageError` and `PartitionError`; **R-74**'s negative
> controls extended with the strict-subset control, the `partition=DEC` control, the
> 30-condition enumeration and the `PartitionError` control; **R-80**'s table given `kind`,
> `train_start`, `train_end` and `validation_month` columns with a dated Recommendation-25 box
> (the `DEC.train_end = 2022-11-30` specification, the retained carve-out, the residual, and the
> unchanged 39/10 figures re-derived); **R-83** added (BLK-09's `train_start` contract) and
> **R-84** added (BLK-08 half B, narrowed to `ABL-DIFF` on D-27); § Amendments owed re-derived
> to **7 across 5 units** with the arithmetic printed and the 5-unit coincidence explicitly
> distinguished from agreement; Assumptions extended with BLK-09, BLK-08, the
> `PartitionError` declaration-site item and the `DEC`-train residual, and the FU-5 item marked
> **closed by D-28**. **Rule ids R-74…R-82 and R-76a are unchanged in id, subject matter and
> limb structure; R-83 and R-84 are additive.** Every prior dated box is preserved as history.
> **BLK-04 remains an open exit condition, BLK-08 and BLK-09 remain open exit conditions, and
> G-09 remains unsigned; nothing here authorises implementation or the creation of a module.**
