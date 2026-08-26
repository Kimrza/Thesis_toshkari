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
- `../governance-guards/functional-design/business-rules.md` — **R-19** (the exactly-one-member exclusion shape), **R-23** and **R-24** (the two phase-boundary limbs). **Corrected 2026-08-26, iteration-5 finding 10 (iteration-4 finding 10):** R-24 is cited in this artifact's body and was absent here; **R-25** (access-log ordering) and **R-28** (restricted root) were listed and drawn on nowhere, and are removed — the same correction `business-logic-model.md` and `domain-entities.md` received on 2026-08-23, which this file had been left out of.
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
| 4 | **Applying failure** | `apply_transforms` takes a **required `purpose`** (`train` \| `evaluate`, no default) and raises `LeakageError` when the frame leaves the set that `purpose` permits **for that transform's own fold** — its training partition for `train`; for `evaluate`, its validation month **plus the causal history the frozen 24-hour window requires, readable but never emitted** (W-4b; *aligned 2026-08-26*) — or when the frame is **empty** |

> **⚠ Read this table with its condition — the four downstream units cite it by name.**
> Elements 1–4 are **complete and executable for F1–F4**. For the **final refit** they are
> **conditional**: `fit_transforms` takes a `FoldSpec` and R-80 records that the refit **is not
> one**, so the refit's transform has no fitting path until that shape is settled at the gate.
> **G-06 depends on that resolution**, and a unit consuming this contract inherits the
> condition, not just the four rows.

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

**Constraint — stated once, consumed by name.** BLK-04 calls it a *"governed cross-unit
contract"*. The four downstream units **cite** this rule; they do not restate it. A restated
contract in four places drifts, and this stage has already corrected four counts that drifted
between restatements.

**Negative controls.** Fit on the full dataset with a fold named → **`LeakageError`**. Fit on
F1's training partition and apply to **F3's validation month (October)** → **`LeakageError`**.
Fit on a superset of the training partition by one row → `LeakageError`. Apply an **F1**
transform to a frame carrying **one December row** → `LeakageError`. Reach `apply_transforms`
with an **empty or timestamp-less frame** → `LeakageError`, so a check that never fired
cannot pass for one that did. Call `apply_transforms` **without `purpose`** → **`TypeError` at
the call site**, which is the point of having no default.

**The leaking direction, which the two superseded rules both passed** — the control that
exists because its absence was the defect. **F4's** transform (fitted Jan–Oct),
`purpose=evaluate`, applied to **April** → **`LeakageError`**: F4's validation month is
**November**, and F4's fit saw April. The mirror case, **F2's** transform with
`purpose=evaluate` on **April** → **`LeakageError`** likewise. Any fold *k*'s transform
evaluated on any month that is not exactly fold *k*'s validation month → **`LeakageError`**.

**The `train`-purpose cells, which no control previously exercised.** **T_refit**/`train` on
**November** → **passes**; November is genuinely in the refit's training partition and this is
the ordinary refit path. **The same frame then reaching an evaluation comparison as F4's
validation scoring → fails**, caught by the pairing control, not by `apply_transforms`. Same
pair for **F4**/`train` on **October** against F3's evaluation, and for the other eight of the
ten nested cells. **This is the control the artifact promised and did not carry** until
2026-08-23.

**Negative controls that must *not* fire** — as load-bearing as the ones that must, since a
check blocking a lawful path was the failure mode of the second correction. **F4**/`train` on
**April** → **passes**; April is genuinely in F4's training partition. **F1**/`evaluate` on
**April** → **passes**. Apply the **final-refit** transform to **December** under
`purpose=evaluate` → **passes**; that is G-06, gated by R-82's execution guard and not by this
rule.

> **⚠ One earlier control is withdrawn, not silently dropped.** It read: *"fit and apply within
> one fold, spanning its training range, embargo and validation month → passes … that is the
> ordinary path and must not be blocked."* Under `purpose`, `evaluate` accepts **exactly** the
> validation month, so a **single** spanning call is no longer lawful under either value — the
> caller makes **two** calls, one per purpose. That is a real change to the calling pattern and
> is stated here rather than left as a contradiction between two controls.

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
> dataclass carries `validation_month`; the final refit has none. Its representation alongside
> the four folds is raised at the gate — **together with R-74's element 4**, since
> `fit_transforms` takes a `FoldSpec` and the refit's transform has no fitting path until this
> is settled. **One decision, not two**, and G-06 depends on it.

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

**Constraint — transforms reach both representations, and that costs an amendment** (added
2026-08-23, corrected the same day). `apply_transforms` is typed `DataFrame -> DataFrame` and
R-74's element 4 tests **record timestamps**, which the `NDArray` tensor does not carry — so
without a mechanism the fit/apply leak survives on **exactly the representation M-06
consumes**.

> **⚠ The first statement was unexecutable.** It read *"both representations are built from a
> frame that has already passed element 4"*. But `build_features(...) -> tuple[DataFrame,
> NDArray]` emits **both in one call that takes no `Transform`**, and the transform is fitted
> on the features **that call produces** — no transformed frame exists before windowing.

**Resolution.** `build_features` gains **two parameters that travel together** —
`transform: Transform | None = None` and `purpose: ApplyPurpose | None = None`. Both `None`
emits the untransformed features `fit_transforms` is fitted on; both supplied applies the
transform **under that purpose**, running R-74's element 4 inside `build_features` **before**
windowing, so both representations inherit it from **one** definition and parity is untouched.
**Supplying one without the other raises** — a default would reinstate the hole.

> **⚠ `purpose` was missing from the first statement** (corrected 2026-08-23): a `transform`
> with no `purpose` meant the tensor path either **bypassed element 4** or had **no
> determinable accepted set**.

**Three calls per fold, not two** *(restated 2026-08-24 on FU-6 = A; iteration-5 finding 3).*
The sequence is `build_features(transform=None, purpose=None)` over the training partition to
produce the frame `fit_transforms` is fitted on; then a `train` call over that same partition;
then an `evaluate` call over the validation month. The earlier text described only *"two calls
over disjoint months"* — but the **fitting call covers the same months as the `train` call**,
so it was neither of the two, and it emits **both** representations **untransformed**. Since
`05` writes what each call emits, three `(matrix, tensor)` pairs per partition could reach disk
with nothing distinguishing them.

**The fitting call's outputs are a fitting input only** — never emitted, never persisted, never
consumed. **Negative control:** an **untransformed tensor reaching M-06 → fails**. Only calls 2
and 3 emit, and both are stamped (W-4a).

**Which rows each call may read** is derived inside `build_features` from `fold` and `purpose`
— the approved signature carries no row-range parameter — and for `purpose="evaluate"` the
readable set is fold *k*'s validation month **plus the causal history the frozen 24-hour window
requires**, of which **only the validation-month rows are emitted** (FU-5 = D; W-4b).
**Control:** emitted rows exceeding the validation month under `purpose="evaluate"` → **fails**.

**Two calls emitting is not the rejected "double call".** What W-4 rejects is transforming the
matrix of a single call while that call's tensor stays untransformed — one feature-set ID, two
disagreeing representations. Here each emitting call emits both representations already
transformed and consistent. Re-windowing would create a second definition; the tensor cannot be
transformed directly. **This is the seventh owed amendment** — a different function in a
different boundary from R-74's sixth — and W-4a's stamp is the **eighth**.

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

**Derived, not carried** — every count this stage carried from adjacent prose was wrong.

| Source | Owed | Basis |
|---|---|---|
| `external-products` **R-55** | **5**, across **3** units | Derived there, boundary contracts only. **Not restated here**; a restated count drifts. |
| **R-74** | **1** | `apply_transforms` gains a required `purpose: ApplyPurpose`. Owner-approved 2026-08-23. |
| **R-81** | **1** | `build_features` gains `transform: Transform \| None = None` **and** `purpose: ApplyPurpose \| None = None`. **One function, one amendment** — the two travel together and supplying one without the other raises. |
| **R-74's pairing control** (W-4a) | **1** | The **provenance stamp** — `fold_id`, `purpose`, `transform_id` as recorded fields on every emitted feature artifact, **refused at the consumer** by `06_train_and_predict.py` and `07_evaluate_and_report.py`. Added 2026-08-24 on **FU-4 = D**. One bundled contract change refused at both consumers, counted as **1** on R-55's own basis — its rows already bundle a dataclass field with a function, and one row covers three modules' blocks. |
| | **8 across 5 units** | 5 + 1 + 1 + 1 |

All three of this unit's touch **cross-package boundary calls or artifacts**, outside § Depth's
intra-package carve-out. That carve-out still covers `Transform`'s internals, `ApplyPurpose`'s
definition, and every other `src/features/*` / `src/data/splits.py` shape beyond the named
boundary calls.

**The fifth unit is the pair of consuming scripts**, whose own units have not designed yet.
Writing a requirement into their inbox is deliberate: BLK-04 is an exit condition on them too.

> **Superseded, preserved:** *"nothing here owes an amendment; the running total stays five
> across three units."* True of the first two element-4 remedies — both of which avoided a
> signature change and **neither of which worked**.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence, so this unit opens at **R-74**. If per-unit numbering was intended, say so at the gate.
- **[assumption]** The **story map governs** where it and `unit-of-work.md` § 7 disagree. `business-logic-model.md` § The `unit-of-work.md` sweep shows **ten of twelve sections agree**, and the two that do not are exactly the two `CR-2026-08-22-LEAKAGE-TA` touched — so this is **one change record that missed two sections**, not a pattern in the file.
- **[assumption]** `src/features/*` and `src/data/splits.py` shapes beyond the named boundary calls are **intra-package** and this stage's to specify — **still true, and still owes nothing**. But **three boundary changes** are owed: R-74's required `purpose` on `apply_transforms`; R-81's `transform` **and** `purpose` on `build_features`, which travel together; and W-4a's `fold_id`/`purpose`/`transform_id` stamp on every emitted feature artifact, refused at `06`/`07`. Running total **8 across 5 units**, derived in § Amendments owed. **Corrected 2026-08-23** from *"no amendment owed; the total stays five across three units"*, and **again 2026-08-24** when FU-4 = D added the stamp.
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
