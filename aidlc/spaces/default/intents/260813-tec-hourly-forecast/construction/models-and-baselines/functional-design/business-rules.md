# Business Rules — `models-and-baselines`

**Unit** `models-and-baselines` (Bolt 8) · **Kind** `library` · **Depends on**
`features-and-splits`

The prohibitions this unit enforces, each with what it rejects, what it raises, and the
**negative control that proves the rejection happens**. `team.md` § Testing Posture makes that
pairing this project's actual methodology: every hard rule gets a test proving the violation is
caught, not only one proving the happy path works.

**Authored 2026-08-24** against `functional-design-questions.md` Q1–Q8 = **D, D, D, D, D, C, D,
D**. Rules continue the single sequence and open at **R-90**.

**No rule here decides a scientific value.** D-121's grids, D-122's seeds, Vision §8.6's seven
fixed LSTM settings, Vision §8.7's selection criterion and TE §7.2's ablation registry are frozen
upstream and are **restated, never chosen**.

## Sources

- `../../../inception/application-design/component-methods.md` § `src/models` — every signature quoted below.
- `../../../inception/units-generation/unit-of-work.md` § 8 — `Owns`, boundary, **BLK-03**, the six implementation notes.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2; 9 requirements, **7** with no acceptance row.
- `../../../inception/requirements-analysis/requirements.md` — FR-P1-04-14, FR-P1-05-1…-6, -21, -22.
- `../features-and-splits/functional-design/business-rules.md` — **R-74**'s pairing control and its FU-4 = D restatement, which R-90 below is the consumer half of.
- `../foundation/functional-design/` — the `IntegrityError` base and the two-tier error posture.
- `PreFlight/vision_document(3)(2)(2).md` § Decision register, lines **1206–1207** — **D-121** (exact frozen grids: ridge 6, RF 18, LSTM 16, with fixed training settings; **Approved**) and **D-122** (development seed **42**; final seeds **{1337, 2024, 7}**; the confirmatory prediction is the element-wise three-seed mean; failed runs recorded, never silently rerun. **Approved; supervisor sign-off closed 2026-08-22** by the project owner under the recorded student/supervisor authority equivalence — `CR-2026-08-22-TE-AMEND`, `GOV-2026-08-22-REM-01` Rec 4 — with the note that **no supervisor signature artifact exists and none is claimed**, and the seed values verified unchanged before closure).
  > ⚠ **Two D-number namespaces, and the first draft cited the wrong one.** D-121 and D-122 are **Vision-document** decision IDs. `evidence/DECISIONS.md` is a **separate register running D-1…D-27** and contains neither — verified by enumerating its `D-<n>` headings. The first draft of these artifacts cited `evidence/DECISIONS.md — D-121, D-122`, which resolves to nothing. **Corrected 2026-08-24** (iteration-1 finding 1 — whose framing that the two decisions *"do not exist"* is itself wrong: they exist, in the other register, and both are Approved).

---

## R-90 — A frame whose stamp is not `(fold k, evaluate)` never reaches fold *k*'s scoring

**Rule.** `06_train_and_predict.py` calls a **named match function in `src/models/train.py`**
before **every** scoring path. The function checks `bundle.fold_id` equals the fold being scored,
`bundle.purpose` equals `evaluate`, and `bundle.transform_id` is present. A mismatch raises
**`LeakageError`**.

**Why here and not in `fit_predict`.** `fit_predict` is a **training** call. It can check the
stamp is present and internally consistent — and already raises `LeakageError` when
`bundle.transform_id is None` — but it **cannot know whether the caller is about to score fold
*k*'s validation month**, which is the half of the requirement that matters. **Why not inline in
the script:** §7 places reusable logic in `src/` and makes scripts orchestrators, so a governed
check belongs in `src/` even when a script is its only caller.

> ⚠ **Corrected 2026-08-24 (iteration-1 finding 2).** The first draft also justified the `src/`
> placement by saying `features-and-splits`' `tests/test_train_only_transforms.py` *"needs a
> function it can call rather than a script it must replay"*. **That misdescribed the sibling's
> test.** Its own `business-rules.md` R-74 declares the test **manifest-based** — it *"reads the
> emitted stamps and asserts that refusal"* — and explicitly **not** monkeypatch-and-replay,
> *"which verifies a replay rather than what a real run emits"*. Calling this function directly is
> nearer the rejected shape than the chosen one. **What the sibling's test actually asserts is the
> refusal's effect on emitted artifacts, not this function's return value.** The function is still
> a cross-unit contract surface — both units depend on the same match semantics — but the
> dependency is **semantic**, not a call edge, and the `src/` placement rests on §7 alone.

**Negative controls.** A frame stamped **`(fold 4, train)`** reaching **fold 4's validation
scoring** → **`LeakageError`**. An **unstamped** frame reaching **any** scoring path →
**`LeakageError`**. A frame stamped `(fold 2, evaluate)` reaching **fold 3's** scoring →
**`LeakageError`**.

**Control that must *not* fire:** a frame stamped `(fold 4, evaluate)` reaching **fold 4's**
validation scoring → **passes**. That is the ordinary path, and a rule blocking it would be the
failure mode `features-and-splits` already hit once.

> **This rule closes `06`'s half of the eighth amendment — and only `06`'s.**
> `features-and-splits` FU-4 = D put the obligation on **`06` and `07`**, and names its fifth
> landing site as *"the pair of consuming scripts"*. But `unit-of-work.md` assigns **`06` to this
> unit** and **`07_evaluate_and_report.py` to `evaluation-and-comparison`** — a **different unit,**
> **whose functional design has not run.** So the sibling's "fifth unit" is in fact **two** units,
> and this rule discharges one of them.
>
> **`07`'s half is unowned and open** (recorded 2026-08-24, iteration-1 finding 3). It is carried
> to the gate and into § Assumptions & Open Questions rather than left to be discovered when
> `evaluation-and-comparison` designs. **The amendment total is unaffected** — the stamp contract
> is counted once, by `features-and-splits`, and nothing here adds to it; what was wrong was the
> claim that this rule completed it.

## R-91 — The confirmatory prediction is the three-seed mean, and nothing may be substituted for it

**Rule.** `three_seed_mean(predictions, *, expected_seeds)` takes exactly three M-06
`Prediction`s whose seeds equal `expected_seeds`, read from **`ConfigSnapshot.seeds`**. The
element-wise mean is **the confirmatory prediction** (NFR-DET-01; TC-21; Vision §8.6).

**Raises `SeedError`** on: fewer or more than three; a seed set not exactly `expected_seeds`;
any input with `seed is None`; any input whose `model_id` is not `"M-06"`.

**Negative controls.** A **single-seed** prediction offered as confirmatory → **`SeedError`**. A
**best-of-three** selection → **`SeedError`**, since the substituted single run fails the count.
A **wrong-but-distinct** triple, e.g. `{1338, 2024, 7}` → **`SeedError`**, which is precisely
what a pairwise-distinctness check would have let through.

> **The frozen set never enters source.** `{1337, 2024, 7}` (D-122) lives in `seeds.yaml` and
> reaches this function as a parameter. Inlining it in `src/models` is the pattern **TC-03e** and
> `project.md` § Forbidden prohibit outright, and weakening the check to "three, pairwise
> distinct" is the other rejected implementation BLK-03 names. Development seed **42** is not a
> confirmatory seed; bootstrap seed **20221201** belongs to TE §13.6 / TC-19 and is **not** part
> of D-122's item set.

## R-92 — A confirmatory mean whose inputs disagree on provenance fails

**Rule.** The three inputs must share `partition_id`, `transform_id`, `phase_id`, `source_id`
and `target_definition_id`; the mean **copies** them. `partition_id` disagreement or a training
partition raises **`PartitionError`**; `transform_id` disagreement or `None` raises
**`LeakageError`**.

**Raises `AlignmentError`** when the three frames do not share an identical index. The key is
stated so an implementer needs no second lookup: the ordered pair **(`station`,
`interval_start_utc`)**, compared as a set **and** in order.

**Negative controls.** Three predictions from **different partitions** → **`PartitionError`**.
Three whose frames differ by **one row** → **`AlignmentError`**. Three with **identical row sets
in different orders** → **`AlignmentError`**, because averaging them element-wise would silently
pair the wrong rows.

> **The stamp must travel the whole way.** ADR-11 added `partition_id` and `transform_id` to
> `Prediction` because *"`07` receives predictions, not bundles, and could not tell which
> partition's transform produced the numbers it is about to score."* If the mean dropped them,
> the provenance would die at exactly the step this unit owns.

## R-93 — The seed is never selected, and never selected on December

**Rule.** No seed is chosen on validation performance, and none after December is seen. The
three-seed set is **fixed in configuration**, and its **values** are asserted against the frozen
set — *"fixed in config" is satisfied by any three numbers*, which is why FR-P1-05-2 names them.

**Negative control.** A run whose seed set is chosen at runtime, or differs from
`ConfigSnapshot.seeds`, → **`SeedError`**.

> **D-122's sign-off is closed, and the first draft said otherwise.** *(Corrected 2026-08-24.)*
> The Vision decision register line 1207 reads **"Approved; supervisor sign-off closed 2026-08-22"**
> — by the project owner under the recorded student/supervisor authority equivalence, with the
> explicit note that **no supervisor signature artifact exists and none is claimed**. The first
> draft carried *"Approved — supervisor sign-off pending"*, which is **D-126's and D-128's** status,
> not D-122's. The seed values are frozen and their authority is closed; **what remains owed at
> G-05 is the gate itself, not this decision's signature.**

## R-94 — M-06 restores its lowest-validation-RMSE checkpoint, not its last epoch

**Rule.** Checkpointing selects on **lowest validation RMSE**; restore returns that checkpoint.
This is one of Vision §8.6's seven fixed settings (R-96), not a choice made here.

**Negative control.** A restore returning the **last** epoch → **fails**. Acceptance: **WS-15**,
**TA-13**, `tests/test_checkpoint_restore.py`.

## R-95 — Tuning reads January–November only, and the residual is named

**Rule.** Model selection, feature selection, thresholds and hyperparameters are **never**
informed by December. **The trigger is December being *seen*, not the locked test being opened**
(Vision §8.3; `project.md` § Forbidden).

**Three mechanisms** *(Q3 = D)* — two closing one channel each, and a third narrowing the residual:

1. **`TuningRecord.partitions_read`** excludes December. Catches a December partition being read.
2. **`criterion_declared_at` / `criterion_used_hash`** — the criterion declared **before** tuning
   equals the one used. Catches a criterion changed after December was seen, which the partition
   record cannot see.
3. **`audit_access_since_declaration`**, read from `governance-guards` **R-25**'s durable access
   log: a tuning run whose record post-dates a December coverage-audit access **must state it**.
   **The join is stated, not left as an outcome** (iteration-1 finding 6): R-25's log rows carry an
   `AccessRecord` with its **access timestamp** and **purpose**; the correlation is
   `AccessRecord.timestamp > TuningRecord.criterion_declared_at` **and**
   `AccessRecord.timestamp < TuningRecord.run_at` — the field `domain-entities.md` § 5 declares for
   this purpose — restricted to records whose purpose
   is a **December coverage or regime audit**. If `AccessRecord` carries no purpose field able to
   express that restriction, the check degrades to **any** access in the window — which is stricter,
   not weaker, and is the fallback this rule adopts rather than leaving the join undefined.

**Negative controls.** A tuning run reading a December partition → **fails**. A run whose used
criterion hash differs from its declared one → **fails**. A run post-dating an audit access with
no such statement → **fails**.

> **What no mechanism reaches, stated plainly.** A choice informed by a December **figure a human
> carries in their head** — a grid narrowed after glancing at a coverage number — leaves no trace
> in any of the three. Item 3 **narrows** it by making the overlap visible for review; it does not
> eliminate it, and nothing can. `requirements.md` already records that **no existing row tests
> this requirement's actual trigger**; WS-18 stays on FR-P1-05-12 where it does test the thing
> named. A candidate TA row is owed via **Vision §15.2** and goes to the gate.
>
> **The required pre-G-05 December coverage audit is performance-blind and legitimate.** This rule
> closes the channel that audit opens; it does not forbid the audit, which is a **precondition of
> G-05**.

## R-96 — Grid content is asserted, not only grid immutability

**Rule.** The grid lives **once**, in `experiment.yaml`. What is frozen and compared is its
**hash**, committed before **G-05**. Asserted individually: cardinalities **ridge 6, RF 18,
LSTM 16** (D-121), and Vision §8.6's seven fixed LSTM settings — **dropout 0.2**, **Adam**,
**MSE loss**, **max 100 epochs**, **early-stopping patience 10 on validation RMSE**, **minimum
improvement 1e-4 TECU**, **best-checkpoint restoration rather than last epoch**.

**No grid range changes after December is seen** — mechanised by the hash comparison above and
controlled below.

**No second 2022 test period is selected after results are observed** (Vision §8.7, §8.10;
TE §7.1). *(Post-redo finding 3: the first draft stated this prohibition alongside the grid one
and mechanised only the grid, giving it neither an owned check nor a consumed-obligation
disclaimer — the only cross-unit obligation in these artifacts left in that position.)* **Its
mechanism, and its owner:** the test period is **December 2022, fixed by D-8 and Vision §2.5's
claim boundary**, and selecting a *second* one is a change to the **partition list**, which
`features-and-splits` owns (its `PartitionList`, five partitions plus the locked month). This unit
therefore **claims no check over it** and records it as a **consumed obligation** — the same
posture R-97 takes toward Vision §2.4 and R-100 toward the feature manifest. **What this unit can
and does enforce:** `domain-entities.md` § 3 limb 3 enumerates the allowed partitions for a
confirmatory prediction, and a partition outside that enumeration raises **`PartitionError`** — so
a second test period cannot be *scored* here even though it could be *declared* elsewhere.

**Negative controls.** A **40-combination** LSTM grid committed before G-05 with an empty diff
afterwards → **fails** on cardinality. A 16-member LSTM grid with the **wrong members** → **fails**
on hash. A post-G-05 grid diff that is **non-empty** → **fails**. Patience changed from 10 → **fails**.

> **Why a hash rather than a duplicated expectation.** `requirements.md` warns that provenance and
> immutability alone let a grid *"pass with none of the specified members in it"*, so cardinality
> is not content. But writing the expected membership into a **test file** would inline a
> scientific constant in source — **TC-03e** and `project.md` § Forbidden. The hash is the frozen
> object: one copy, nothing to drift, no constant in source, and the **post-G-05 diff-empty check
> becomes the same mechanism** rather than a second one.

## R-97 — Ablations are predeclared, five named, four reachable in Phase 1

**Rule.** Every ablation is a **named run registered in `experiment.yaml` with a run ID before
the freeze**, executed on the frozen January–November folds with **identical folds, masks and
tuning budget**. TE §7.2's registry is **five**: `ABL-NODOY`, `ABL-DIFF`, `ABL-NOSW`,
`ABL-HIST48`, `ABL-ZENITH`.

- **`ABL-DIFF`** inverse-transforms to **absolute TECU before any metric**, via
  `Transform.inverse` — which requires `transform_id` present on the `Prediction` (R-92).
- **`ABL-HIST48`** runs **only after the primary configuration is frozen**, checkable against
  R-96's G-05 hash.
- **`ABL-ZENITH` is deferred to Phase 2**: it varies the hourly aggregation of the target
  (zenith-weighted versus IPP median, Vision §6.6), a choice that **does not exist** on the Phase
  1 location-sampled gridded target. A recorded **phase deferral**, not an omission. **Five named,
  four reachable** — stated both ways so the count is not quietly reduced.

**No promotion.** *"No ablation configuration may be promoted to primary once the locked test is
opened"* (TE §7.2), checked as **reported-primary-hash == G-05-frozen-hash**.

**Negative controls.** A **missing** required ablation → **fails the check rather than passing
unnoticed**. An ablation **registered after results are seen** → **fails**. `ABL-DIFF` metricised
**before** its inverse transform → **fails**. `ABL-HIST48` run **before** the primary freeze →
**fails**.

> **Vision §2.4's bar is consumed, not claimed.** *"No secondary result replaces the primary
> conclusion"* reaches the **reporting** unit, `regimes-diagnostics-reporting`. This unit records
> it as a consumed obligation and **claims no check over it**.

## R-98 — M-03 is fitted on training partitions only

**Rule.** The station×month×hour climatology is fitted on **training partitions only** and never
using validation or December data (Vision §8.4, quoted at FR-P1-05-21).
`climatology_fit_partition(prediction)` returns the partitions it was **actually** fitted on;
every returned identifier must be a training partition.

**Negative control.** A climatology fitted **across all of 2022** → **fails** — the exact case the
requirement names, and the reason it must fail *a test* rather than pass a module inventory. A
climatology fitted on all of 2022 would otherwise **stop functioning as a difficulty control**
while passing every other stated check.

> **No reading is adopted on TA-11.** Whether TA-11's *"train-only transforms"* reaches a **model
> fit** is **unverified upstream** and `requirements.md` declines to claim it. This stage declines
> too. FR-P1-05-1's criterion is a module and `grep` inventory that never reaches a model fit;
> FR-P1-04-6 covers **scaler** fitting. Confirming the reading, or adding a row, runs through
> **Vision §15.2** at the gate.

## R-99 — The +24 h horizon needs no code change

**Rule.** `experiment.yaml` exposes **`horizons: [1]`** with **24 implemented and testable but
absent from the default run list** (TE §2.1). Horizon travels as a **parameter** from
`ConfigSnapshot` through `fit_predict`'s `snapshot` argument to label construction, so **no code
path branches on a literal horizon value**.

**Negative controls.** A code path branching on a **literal** horizon → **fails a static check**,
in the pattern `governance-guards` R-28 and `features-and-splits` R-76a's third limb use. A
`+24 h` path that **requires a code edit** → **fails**. A `+24 h` path raising
`NotImplementedError` → **fails**, which is the case a config-shape assertion alone would pass.

## R-100 — Random Forest importance is diagnostic, and never a selection input

**Rule.** No RF importance score adds, removes or ranks a feature into the **production feature
set**. The figure is saved with `authoritative = false` recorded **in its own metadata**, not left
to convention (Vision §6.4; TE §6.4).

**Negative control, inside this unit's reach.** An importance score reaching the **production
feature path** — as distinct from the diagnostic artifact — → **fails**, checked on this unit's
**own module graph**.

> **The requirement's stated evidence belongs to a sibling.** FR-P1-05-3's criterion is *"the
> feature manifest's provenance shows no importance-derived selection"*, and the **feature manifest
> is `features-and-splits`'**. This unit records that as a **consumed cross-unit dependency** and
> **claims no check over it** — the same posture `features-and-splits` took toward
> `inventory-and-registry`'s station registry. Claiming a sibling's coverage is a mistake this
> project has already had to correct once.

## R-101 — Selection is on mean per-fold skill score, and the refit changes no hyperparameter

**Rule** (FR-P1-04-14; Vision §8.7). Configurations are selected on the **mean per-fold skill
score across F1–F4**. **Raw mean RMSE is not used. Row-count weighting is not used.** The declared
baseline per track is named in configuration **before tuning begins**. Where mean skill differs by
less than **1%**, the **simpler** configuration is selected. The selected configuration is then
refit on **January–November without changing any hyperparameter**.

**Two mechanical comparisons**, as the requirement states them: the selection record's criterion
equals the criterion configured before tuning (R-95's hash pair); and the refit hyperparameters
equal the selected ones.

**Negative controls.** A selection made on **raw mean RMSE** → **fails**. A selection using
**row-count weighting** → **fails**. A refit that **alters any hyperparameter** → **fails**. A run
with **no pre-tuning declared baseline** → **fails**.

> ⚠ **FR-P1-04-14 has no §16/§19 acceptance row.** `requirements.md` records it as `UNTESTED` with
> a candidate TA row owed via Vision §15.2. The rule and its controls are stated here; the missing
> row is **reported at the gate, not invented**.

## R-102 — The model set is closed, and two absences are evidence

**Rule.** Exactly **M-01…M-06** (FR-P1-05-1). **Residual and GRU modules are absent from the
codebase and their absence is `grep`-evidenced**; **TensorFlow/Keras is the only NN stack** and
**PyTorch is prohibited** (TE §8.3). This unit **must not import** `src/external/iri.py`,
`src/external/gim.py` or `src/evaluation` — that dependency runs the other way.

**Negative controls.** A **residual** or **GRU** module present in the tree → **fails** TA-12. A
**PyTorch** import → **fails**. An import of `src/external/iri.py`, `src/external/gim.py` or
`src/evaluation` from `src/models` → **fails** a static import-boundary check.

---

## ⚠ BLK-03 IS AN EXIT CONDITION, AND THIS DESIGN DOES NOT DISCHARGE IT

`domain-entities.md` § 3 **authors** the confirmatory-prediction contract's four limbs — input
and output types, alignment requirements, allowed partitions, failure conditions — which is what
BLK-03's register entry asks this stage for. **Authoring is not approving.** The register's
ruling stands: this unit and `evaluation-and-comparison`, `statistical-inference` and
`regimes-diagnostics-reporting` **may enter** stage 3.1; **none may complete or exit without the
approved contract**; and **no implementation may proceed** while the blocker stands.

**BLK-04 ↓ and BLK-09 ↓** are inherited from `features-and-splits`. Its 2026-08-24 answers
supplied their mechanism; **neither is closed**.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence, so this unit runs **R-90…R-102**. If per-unit numbering was intended, say so at the gate and the artifacts restart.
- **[assumption]** The **story map governs** where it and `unit-of-work.md` § 8 disagree. Neither is edited by this stage.
- **[assumption]** `src/models/*` shapes beyond the named boundary calls are **intra-package** and this stage's to specify (`component-methods.md` § Depth). **R-90's match function is one of them**, so it owes **no** amendment: the total stays **8 across 5 units**, and `domain-entities.md` § 6 declined the option that would have made it nine.
- **Open — BLK-03's contract limbs are an EXIT condition** on this unit and three downstream units. **Approving this design is not the contract's approval.**
- **Open — BLK-04 ↓ and BLK-09 ↓**, inherited and not closed.
- **Open — R-90's match function is a cross-unit contract surface.** `features-and-splits`' `tests/test_train_only_transforms.py` asserts against it; neither unit owns it alone.
- **Open — 7 of 9 requirements have no acceptance row**: FR-P1-04-14, FR-P1-05-3, -4, -5, -6, -21, -22. Four name their own candidate TA row via **Vision §15.2**. **None is added here.**
- **Open — whether TA-11 reaches a model fit is unverified upstream** (R-98). No reading adopted.
- **Closed, corrected 2026-08-24 — D-122's supervisor sign-off is NOT outstanding.** The first draft carried *"Approved — supervisor sign-off pending"*, which is the status of **D-126** and **D-128**, not D-122. The Vision decision register (line 1207) reads **"Approved; supervisor sign-off closed 2026-08-22"** by the project owner under the recorded student/supervisor authority equivalence (`CR-2026-08-22-TE-AMEND`; `GOV-2026-08-22-REM-01` Rec 4), noting that **no supervisor signature artifact exists and none is claimed** and that the seed values were verified unchanged before closure. `unit-of-work.md` § 8 already recorded the closure. **Found while verifying iteration-1 finding 1 against the source register; the reviewer did not raise it.**
- **Open — FR-P1-05-4's residual**: a choice informed by a December figure a human carries in their head is unreachable by any mechanism (R-95). Narrowed by the audit-access precondition, not eliminated.
- **G-09 is not signed**, and **BLK-03 independently bars implementation.** No rule here authorises creating `src/models/persistence.py`, `climatology.py`, `ridge.py`, `random_forest.py`, `lstm.py`, `train.py`, `checkpoint.py`, `scripts/06_train_and_predict.py`, `tests/test_models_smoke.py` or `tests/test_checkpoint_restore.py`.
- **Open — `07`'s half of the eighth amendment is UNOWNED.** FU-4 = D names **`06` and `07`**; `unit-of-work.md` assigns `07_evaluate_and_report.py` to **`evaluation-and-comparison`**, whose functional design has not run. This unit discharges `06` only. Raised at the gate so it is not discovered later *(iteration-1 finding 3)*.
- **Open — `requirements.md` FR-P1-05-2 carries TWO superseded clauses on one line, both reported and neither edited.** (a) It attributes bootstrap seed **20221201** to D-122, a reading `unit-of-work.md` § 8 records as corrected 2026-08-22 (`GOV-2026-08-22-UG-02` Rec 11) — the seed is frozen separately by **TE §13.6 / TC-19** (Q-27). (b) It states *"Vision §14.2 marks it 'Approved — supervisor sign-off pending'… still owes a signature at G-05"*, superseded by the same Vision-register closure at line 1207 that these artifacts cite correctly elsewhere — **"Approved; supervisor sign-off closed 2026-08-22"**. This unit follows the **corrected** reading of both. `requirements.md` is an approved upstream artifact and `CHANGE_RECORD_PROCEDURE.md` bars editing one absent owner approval for annotate-in-place, so both are **raised at the gate**. *(Clause (a) was iteration-1 finding 5; clause (b) is iteration-2 finding 2 — flagging one clause of a line and missing its neighbour is the same one-representation-short failure as iteration-2 finding 1, and clause (b) is where this author's own D-122 error originated.)*
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.
