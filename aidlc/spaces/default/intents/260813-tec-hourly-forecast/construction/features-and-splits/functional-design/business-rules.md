# Business Rules — `features-and-splits`

**Unit** `features-and-splits` (Bolt 7) · **Kind** `library` · **Depends on**
`target-standardization`, `external-products`, `governance-guards`

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
- `../../../inception/application-design/component-methods.md` — `src/features`' and `src/data/splits.py`'s boundary calls; § Depth.
- `../../../inception/application-design/services.md` § The nine stage scripts, § Stage entry contract.
- `../target-standardization/functional-design/business-rules.md` — the D-17 target contract consumed here.
- `../external-products/functional-design/business-rules.md` — **R-56**, **R-57**, **R-58**.
- `../governance-guards/functional-design/business-rules.md` — **R-19** (the exactly-one-member exclusion shape), **R-23**, **R-25**, **R-28**.
- `evidence/DECISIONS.md` — **D-10.3**, **D-11**, **D-13**.
- Workspace inspection, 2026-08-23: `tests/` holds three modules, none this unit's; `src/` and `configs/` absent.
- `functional-design-questions.md` (**Q1 through Q9**), `domain-entities.md`, `business-logic-model.md`.

---

## R-74 — BLK-04: train-only fitting, enforced by check rather than by shape

**Rule (Q1 = D).** Four elements, and the register names all four as required:

| # | Element | Mechanism |
|---|---|---|
| 1 | **Allowed partitions** | The **named fold's training partition only** |
| 2 | **Fitting failure** | `LeakageError` when `train`'s index is **not a subset** of that partition |
| 3 | **Ownership of the fitted state** | `Transform` **carries its `FoldSpec`** — the resolved boundaries, not a bare `fold_id` string |
| 4 | **Applying failure** | `apply_transforms` raises `LeakageError` when **any row's timestamp falls outside the transform's own scope** (that fold's training range, embargo and validation month; for the refit, Jan–Nov **and December**), or when the frame is **empty** |

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
> **The mechanism, and it still needs no signature change.** `component-methods.md` leaves
> `Transform` *"referenced as a type and left unspecified: … intra-package"* — this stage's to
> specify, so carrying the `FoldSpec` on it costs **no amendment**, and the count of owed
> amendments stays **five across three units**. `apply_transforms` tests every row's timestamp
> against the transform's **own** scope:
>
> | Transform fitted on | Rows accepted |
> |---|---|
> | Fold *k*'s training partition | Fold *k*'s training range, its **24-h embargo**, its **validation month** |
> | The final refit (1 Jan – 30 Nov) | 1 Jan – 30 Nov **and December** |
>
> **December is not excluded here, it is routed.** Applying the **final-refit** transform to
> December **is** the G-06 path. The lock is held by **R-82's execution guard** — December rows
> reach `apply_transforms` only inside a frame materialised against a **verified
> `g05_signature`** — not by this rule. The second text duplicated the lock in the wrong place
> and would have made **G-06 unreachable** and the **FR-P1-04-14 final refit**
> untransformable.
>
> **The fit side of the refit is the same open decision, not a second one.** `fit_transforms`
> is typed `(train, *, fold: FoldSpec)`, and R-80 records that **the final refit is not a
> `FoldSpec`** — so *"the refit's transform"* has no fitting path until that representation is
> settled. **This rule and R-80's open shape question are one decision**, raised at the gate
> **together**. Element 4 is complete for F1–F4 and **conditional on that resolution** for the
> refit and therefore for G-06.
>
> **`assert_membership_from_timestamps` is cited for what it does**, not as the derivation:
> `(frame) -> None` validates a row against the partition it is **filed under**. It returns
> nothing and derives nothing; the second text was wrong to lean on it.
>
> **Which representation.** Transforms apply to the **timestamped frame**; `windows.py` builds
> **both** representations from a frame that has already passed this check. The `NDArray`
> tensor carries no timestamps and is **never transformed directly**, so element 4 sits
> **upstream of both** — including the sequence tensor M-06 consumes.

**Constraint — stated once, consumed by name.** BLK-04 calls it a *"governed cross-unit
contract"*. The four downstream units **cite** this rule; they do not restate it. A restated
contract in four places drifts, and this stage has already corrected four counts that drifted
between restatements.

**Negative controls.** Fit on the full dataset with a fold named → **`LeakageError`**. Fit on
F1's training partition and apply to **F3's validation month (October)** → **`LeakageError`**,
October being outside F1's scope. Fit on a superset of the training partition by one row →
`LeakageError`. Apply an **F1** transform to a frame carrying **one December row** →
`LeakageError`. Reach `apply_transforms` with an **empty or timestamp-less frame** →
`LeakageError`, so a check that never fired cannot pass for one that did.

**Negative controls that must *not* fire** — as load-bearing as the ones that must, since a
check blocking a lawful path is the failure mode the second correction fixed. Fit and apply
**within one fold, spanning its training range, embargo and validation month** → **passes**.
Apply the **final-refit** transform to **December** → **passes**; that is G-06, gated by
R-82's execution guard and not by this rule.

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

**Rule (FR-P1-04-5, Q9 = D).**

| Partition | Range |
|---|---|
| **F1** | Jan–Mar, validation Apr |
| **F2** | Jan–Jun, validation Jul |
| **F3** | Jan–Sep, validation Oct |
| **F4** | Jan–Oct, validation Nov |
| **Final refit** | **1 Jan – 30 Nov** |
| **December** | **Locked** |

Each fold carries a **24-hour embargo**; the first 24 h are **excluded and counted**. **No
random or shuffled cross-validation.** No window crosses a boundary.

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

> **Open shape decision, stated not assumed: the final refit is not a `FoldSpec`.** That
> dataclass carries `validation_month`; the final refit has none. Its representation
> alongside the four folds is raised at the gate.

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

**Rule (FR-P1-04-8).** `windows.py` emits **both** the flattened matrix and the sequence
tensor for a feature-set ID, so parity is *"structural rather than asserted"*.

**Constraint — transforms run before either representation is built** (added 2026-08-23,
because R-74 element 4 depends on it). `apply_transforms` is typed `DataFrame -> DataFrame`
and element 4 needs **record timestamps**, which the `NDArray` tensor does not carry. Both
representations are therefore built from a frame that has **already passed** element 4; the
tensor is never transformed directly. **Negative control:** build a tensor from a frame that
has not passed element 4, or one carrying rows outside its transform's scope → **fails**.
Without this ordering the fit/apply leak survives on **exactly the representation M-06
consumes**.

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

---

## The four requirements whose rows exist but have never run

| Requirement | Rule | Row | Status |
|---|---|---|---|
| FR-P1-04-12 | R-76 | **TA-33** | **`Pending`** — *"the row exists, no test module is implemented, none has been executed, and none has passed"* |
| FR-P1-04-13 | R-77 | **TA-34** | **`Pending`** |
| FR-P1-04-16 | R-78 | **TA-35** | **`Pending`** |
| FR-P1-04-17 | — (`external-products` R-58) | **TA-36** | **`Pending`** — supported here, owned there |

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
> rules; TA-36 covers driver-interval repetition and is **`external-products`'** row.
> **Remainder: FR-P1-04-10 alone.**

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence, so this unit opens at **R-74**. If per-unit numbering was intended, say so at the gate.
- **[assumption]** The **story map governs** where it and `unit-of-work.md` § 7 disagree. `business-logic-model.md` § The `unit-of-work.md` sweep shows **ten of twelve sections agree**, and the two that do not are exactly the two `CR-2026-08-22-LEAKAGE-TA` touched — so this is **one change record that missed two sections**, not a pattern in the file.
- **[assumption]** `src/features/*` and `src/data/splits.py` shapes beyond the named boundary calls are **intra-package** and this stage's to specify. **No amendment owed**; the total stays **five across three units**.
- **[assumption]** `tests/test_locked_test_guard.py` is this unit's, per § 7.
- **Open — BLK-04 is an EXIT condition** on this unit and on `models-and-baselines`, `evaluation-and-comparison`, `statistical-inference` and `regimes-diagnostics-reporting`. **R-74 is the contract; approving this design is not its approval.** NFR-LEAK-01's evidence is owed to the **Supervisor at G-04 and G-05**.
- **Open — TA-33, TA-34, TA-35 and TA-36 are `Pending`.**
- **Open — `unit-of-work.md` §§ 6 and 7 are stale on coverage figures, and § 5 on a module count.** Reported at the gate for one annotate-in-place decision; **not edited**.
- **Open — WS-13's departure from TE §16** (R-81). No reading adopted, here or upstream.
- **Open — the final refit is not a `FoldSpec`** (R-80). Representation stated at the gate.
- **Open — FR-P1-04-10 has no acceptance row.**
- **Open — an unresolved station registry blocks `station_lat` and excludes `lst_sin`/`lst_cos`** (R-76). Consumed from `inventory-and-registry` R-45/R-46; **not decided here**.
- **G-09 is not signed**, and **BLK-04 independently bars implementation.**
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.
