# Domain Entities — `models-and-baselines`

**Unit** `models-and-baselines` (Bolt 8) · **Kind** `library` · **Depends on**
`features-and-splits`

The data shapes this unit owns: the six model families' identity, the prediction a model
emits, the confirmatory three-seed mean and the contract three downstream units inherit from
it, the checkpoint that must restore, the tuning and selection records that make two otherwise
untestable requirements checkable, and the ablation registry entry.

**Authored 2026-08-24** against `functional-design-questions.md` Q1–Q8 = **D, D, D, D, D, C, D,
D**. **No scientific value is decided here.** The seed set (**D-122**), the grids (**D-121**),
Vision §8.6's seven fixed LSTM settings, Vision §8.7's selection criterion and TE §7.2's
ablation registry are frozen upstream and are **restated, never chosen**.

**G-09 is not signed and BLK-03 independently bars implementation.** Naming a shape here is not
authority to write a module.

## Sources

- `../../../inception/application-design/component-methods.md` § `src/models` — `Prediction`, `fit_predict`, `three_seed_mean`, `climatology_fit_partition`, `Transform.inverse`. **Every signature below is quoted from it, not re-invented.**
- `../../../inception/units-generation/unit-of-work.md` § 8 — `Owns`, the boundary, BLK-03's register entry, the six implementation notes.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2; **9 requirements, 7 with no acceptance row**; owns WS-14, WS-15, TA-12, TA-13, TA-26; supports TA-20.
- `../../../inception/requirements-analysis/requirements.md` — FR-P1-04-14, FR-P1-05-1…-6, -21, -22.
- `../features-and-splits/functional-design/` — **W-4a** (the provenance stamp), **W-4b** (read-versus-emit), **R-74**'s pairing control. FU-4 = D is what lands E-8 below.
- `../foundation/functional-design/` — `ConfigSnapshot`, the `IntegrityError` base, the two-tier error posture.
- `PreFlight/vision_document(3)(2)(2).md` § Decision register, lines **1206–1207** — **D-121** (exact frozen grids: ridge 6, RF 18, LSTM 16, with fixed training settings; **Approved**) and **D-122** (development seed **42**; final seeds **{1337, 2024, 7}**; the confirmatory prediction is the element-wise three-seed mean; failed runs recorded, never silently rerun. **Approved; supervisor sign-off closed 2026-08-22** by the project owner under the recorded student/supervisor authority equivalence — `CR-2026-08-22-TE-AMEND`, `GOV-2026-08-22-REM-01` Rec 4 — with the note that **no supervisor signature artifact exists and none is claimed**, and the seed values verified unchanged before closure).
  > ⚠ **Two D-number namespaces, and the first draft cited the wrong one.** D-121 and D-122 are **Vision-document** decision IDs. `evidence/DECISIONS.md` is a **separate register running D-1…D-27** and contains neither — verified by enumerating its `D-<n>` headings. The first draft of these artifacts cited `evidence/DECISIONS.md — D-121, D-122`, which resolves to nothing. **Corrected 2026-08-24** (iteration-1 finding 1 — whose framing that the two decisions *"do not exist"* is itself wrong: they exist, in the other register, and both are Approved).

---

## 1. `ModelFamily` — six, closed, and two absences that are evidence

| ID | Family | Seeded | Fitted |
|---|---|---|---|
| **M-01** | Persistence | no | not fitted |
| **M-02** | 24-hour seasonal persistence | no | not fitted |
| **M-03** | Station×month×hour climatology | no | **training partitions only** (§ 6) |
| **M-04** | Ridge — grid of **6** | no | per fold |
| **M-05** | Random Forest — grid of **18**, direct only | no | per fold |
| **M-06** | Compact LSTM — grid of **16**, direct only | **yes, three seeds** | per fold |

**The set is closed** (FR-P1-05-1). **Residual and GRU modules are absent by design, and their
absence is `grep`-evidenced** — TA-12's evidence column names exactly that. **TensorFlow/Keras
is the only NN stack; PyTorch is prohibited** (TE §8.3), and its absence is `grep`-evidenced on
the same row.

> **An absence is evidence only if something looks for it.** The two absences and the PyTorch
> prohibition are **negative controls**, not documentation: a residual or GRU module appearing
> in the tree **fails** TA-12, and so does a PyTorch import. This is the project's mandated
> practice — every hard rule gets a test proving the violation is caught.

**Only M-06 is seeded.** `Prediction.seed` is `int | None`, and `None` is the correct value for
M-01…M-05 — it is not a missing field. The three-seed mean (§ 3) therefore applies to **M-06
alone**, and applying it to an unseeded family is a **`SeedError`**, not a no-op.

## 2. `Prediction` — the approved shape, and why four of its fields are provenance

```python
@dataclass(frozen=True)
class Prediction:
    model_id: str                # "M-01".."M-06"
    seed: int | None             # None for unseeded models
    frame: DataFrame             # station, interval_start_utc, y_hat
    target_definition_id: str
    phase_id: str
    source_id: str
    partition_id: str            # added 2026-08-23 (ADR-11)
    transform_id: str            # added 2026-08-23 (ADR-11)
```

**Quoted from `component-methods.md`; this stage does not amend it.**

`phase_id`, `source_id` and `target_definition_id` are the project-wide stamps the mandated rule
requires on every dataset, prediction, mask and comparison. `partition_id` and `transform_id`
were added under ADR-11 for a stated reason worth repeating because § 3 depends on it:
*"Without them the provenance `FeatureBundle` established dies at `06`: `07` receives
predictions, not bundles, and could not tell which partition's transform produced the numbers it
is about to score. The stamp has to travel the **whole** way, not just to the first consumer."*

## 3. `ConfirmatoryPrediction` — BLK-03's contract, all four limbs

```python
def three_seed_mean(
    predictions: Sequence[Prediction],
    *,
    expected_seeds: frozenset[int],
) -> Prediction: ...
```

**Signature quoted from `component-methods.md`.** What follows is the **contract** BLK-03's
register entry asks for and no signature states. **Authoring it is this stage's job; approving
it is the human's, at the gate.**

### Limb 1 — input type

Exactly **three** `Prediction`s, all with `model_id == "M-06"`, whose `seed` values form a set
**equal to** `expected_seeds`. `expected_seeds` is read from **`ConfigSnapshot.seeds`** at the
call site — never inlined in `src/models` or any implementation file (TC-03e; `project.md`
§ Forbidden). The frozen final set is **{1337, 2024, 7}** (D-122); development seed **42** is not
a confirmatory seed. The bootstrap seed **20221201** belongs to TE §13.6 / TC-19 and is **not**
part of D-122's item set.

> ⚠ **One cited Source still carries the superseded attribution, reported not edited**
> *(iteration-1 finding 5)*. `requirements.md` FR-P1-05-2 still lists bootstrap seed **20221201**
> among D-122's values, a reading `unit-of-work.md` § 8 records as **corrected 2026-08-22** per
> `GOV-2026-08-22-UG-02` Rec 11 — the bootstrap seed is frozen separately by **TE §13.6 / TC-19**
> (Q-27). This unit follows the **corrected** reading. `requirements.md` is an approved upstream
> artifact, and `CHANGE_RECORD_PROCEDURE.md` bars editing one absent owner approval for
> annotate-in-place, so the disagreement is **raised at the gate**.

### Limb 2 — output type

A `Prediction` with:

| Field | Value |
|---|---|
| `model_id` | `"M-06"` |
| `seed` | **`None`** — the mean is not attributable to a seed, and a seed value here would misrepresent it as a single run |
| `frame` | element-wise mean of `y_hat` over the three input frames, on the shared index |
| `partition_id`, `transform_id` | **copied from the inputs, which must agree** (limb 4) |
| `phase_id`, `source_id`, `target_definition_id` | copied from the inputs, which must agree |

**The three input predictions are preserved by the caller.** `three_seed_mean` does not discard
them — `component-methods.md` states this, and § 4's consumption contract depends on it.

### Limb 3 — allowed partitions

A confirmatory prediction may be built on:

| Partition | Allowed | Note |
|---|---|---|
| F1–F4 validation months | **yes** | ordinary validation scoring |
| The January–November final refit | **yes** | FR-P1-04-14's refit |
| **December (locked)** | **yes, and only through the guard** | this is the **G-06** path; the lock is held by `features-and-splits`' locked-partition execution guard against a verified `g05_signature`, **not** by this function |
| A training partition | **no** | a confirmatory prediction over training rows is not a result; **`PartitionError`** |
| A mixture of partitions | **no** | `partition_id` must be identical across the three inputs |

### Limb 4 — failure conditions

| Raise | When |
|---|---|
| **`SeedError`** | fewer than three predictions; more than three; the seed set is not **exactly** `expected_seeds`; any input has `seed is None`; any input's `model_id` is not `"M-06"` |
| **`AlignmentError`** | the three frames do not share an **identical index**. The alignment key is stated explicitly: the ordered pair **(`station`, `interval_start_utc`)**, compared as a set **and** in order. Averaging misaligned predictions silently is the failure this exists for |
| **`PartitionError`** | `partition_id` differs across the three inputs, or names a training partition (limb 3) |
| **`LeakageError`** | `transform_id` differs across the three inputs, or is `None` on any of them |

> **The mean carries its inputs' stamp, or it fails.** `partition_id` and `transform_id` must
> agree across the three inputs and are copied to the output. Without this the stamp reaches
> `06` and dies there — exactly the failure ADR-11 added the two fields to prevent. This is the
> extension of E-8's stamp obligation to the one artifact `07` actually scores.

### The downstream consumption contract

`evaluation-and-comparison`, `statistical-inference` and `regimes-diagnostics-reporting` inherit
BLK-03. What each may rely on, stated **once** here so three units cite rather than re-derive:

1. The confirmatory prediction is the **element-wise mean of three seeds**, never a single-seed
   run and never a best-of-three. **No consumer may substitute a single-seed prediction**, and
   none may select among the three.
2. It carries `partition_id` and `transform_id` identical to its inputs, so a consumer can tell
   which partition's transform produced the numbers.
3. The **three individual predictions remain available** from the caller — a consumer needing
   per-seed spread reads them rather than recomputing.
4. `seed is None` on the mean is **correct and load-bearing**; a consumer treating it as a
   missing value is misreading it.
5. `Transform.inverse(frame)` is the **only** route from model output back to absolute TECU, and
   it travels with `transform_id`. `src/evaluation` uses it **without importing `src/features`**.

## 4. `Checkpoint` — lowest validation RMSE, and restore is the test

| Attribute | Meaning |
|---|---|
| `model_id` | `"M-06"` |
| `seed` | the run's seed |
| `fold_id` | the fold the run belongs to |
| `epoch` | the epoch the checkpoint was taken at |
| `validation_rmse` | the metric it was selected on — **lowest**, not last |
| `payload_ref` | the stored weights |

**Best-checkpoint restoration rather than last epoch** is one of Vision §8.6's seven fixed
settings (§ 7), not a choice made here. **WS-15** and **TA-13** are the acceptance rows;
`tests/test_checkpoint_restore.py` is this unit's module.

**Negative control:** a restore that returns the **last** epoch rather than the lowest-validation
-RMSE epoch **fails**.

## 5. `TuningRecord` — what makes FR-P1-05-4 checkable *(Q3 = D)*

FR-P1-05-4 is `UNTESTED`, and `requirements.md` records why: its trigger is December being
**seen**, not the locked test being **opened**, and WS-18 tests the open channel only — which a
performance-blind coverage audit passes by construction.

| Attribute | Meaning |
|---|---|
| `run_id` | the tuning run |
| `partitions_read` | every partition the run read. **Asserted to exclude December** |
| `criterion_declared_at` | when the selection criterion was declared — **before tuning began** |
| `criterion_hash` | the declared criterion, hashed |
| `criterion_used_hash` | the criterion actually used, hashed. **Must equal `criterion_hash`** — the row above, which holds the *declared* criterion's hash. *(Corrected 2026-08-24, post-redo finding 2: this read "must equal `criterion_declared_at`'s hash", and `criterion_declared_at` is a **timestamp** with no hash. An implementer following it literally would have had to invent one.)* |
| `run_at` | the timestamp of this tuning run itself. **Added 2026-08-24 (iteration-2 finding 3):** R-95's join correlates against it, and the first draft referenced *"`TuningRecord`'s own run timestamp"* while this table declared no such field, leaving an implementer to invent one |
| `audit_access_since_declaration` | whether a December coverage-audit access is recorded between `criterion_declared_at` and `run_at`, read from `governance-guards` **R-25**'s durable access log |

**Three mechanisms**, and the count is stated to match the three rows above and R-95's three
negative controls *(corrected 2026-08-24, iteration-1 finding 4: this paragraph read "Two" while
enumerating three)*. `partitions_read` catches a December partition being read. The criterion-hash
comparison catches a criterion changed after December was seen — which the partition record cannot
see. `audit_access_since_declaration` narrows what neither reaches.

> **The residual, named rather than left implicit.** Neither mechanism reaches a choice informed
> by a December **figure a human carries in their head** — a narrowed grid decided after glancing
> at a coverage number leaves no trace in either. `audit_access_since_declaration` **narrows**
> it: a tuning run whose record post-dates an audit access must state that, so the case becomes
> visible for review rather than invisible. It does not eliminate it. **No mechanism can**, and
> saying so is the point — `requirements.md` already records that no existing row tests this
> requirement's actual trigger, and a candidate TA row is owed via Vision §15.2.

## 6. `FittedPartitionRecord` — M-03's fitting partitions *(Q6 = C)*

```python
def climatology_fit_partition(prediction: Prediction) -> Sequence[str]: ...
```

**Quoted from `component-methods.md`.** Returns the partition identifiers M-03 was **actually**
fitted on, so the negative case fails a test rather than passing a module inventory.

**Asserted:** every returned identifier is a **training** partition. **Negative control:** a
climatology fitted **across all of 2022** **fails** — the case FR-P1-05-21 names in terms.

> **No reading is adopted on TA-11.** `requirements.md` records that whether TA-11's
> *"train-only transforms"* reaches a **model fit** is **unverified**, and explicitly says it is
> not claimed there. This stage claims it no more than upstream did. FR-P1-05-1's criterion is a
> module and `grep` inventory that does not reach a model fit; FR-P1-04-6 covers **scaler**
> fitting, not a model fit. Confirming the TA-11 reading, or adding a row, runs through **Vision
> §15.2** and goes to the gate.
>
> **Option D was declined deliberately**: stamping the fitted partitions onto `Prediction` would
> amend an approved boundary contract — a **ninth** amendment — for something
> `climatology_fit_partition` already delivers.

## 7. `GridSpec` and the seven fixed LSTM settings *(Q4 = D)*

**The grid lives once, in `experiment.yaml`.** What is frozen and compared is its **hash**,
committed before **G-05**.

| Track | Combinations | Source |
|---|---|---|
| Ridge (M-04) | **6** | D-121 |
| Random Forest (M-05) | **18**, direct only | D-121 |
| LSTM (M-06) | **16**, direct only | D-121 |

**Vision §8.6's seven fixed LSTM training settings**, asserted individually:

| # | Setting | Value |
|---|---|---|
| 1 | Dropout | **0.2** |
| 2 | Optimizer | **Adam** |
| 3 | Loss | **MSE** |
| 4 | Maximum epochs | **100** |
| 5 | Early-stopping patience | **10**, monitored on **validation RMSE** |
| 6 | Minimum improvement | **1e-4 TECU** |
| 7 | Checkpoint policy | **best-checkpoint restoration**, not last epoch |

> **Why the hash and not a duplicated list.** `requirements.md` warns that provenance and
> immutability alone *"let a 40-combination LSTM grid be committed before G-05, diff empty
> afterwards, and pass with none of the specified members in it"* — so **cardinality alone is
> not enough**, and content must be falsifiable *"without a second lookup"*. But writing the
> expected membership into a test file would put a scientific constant in **source**, which
> TC-03e and `project.md` § Forbidden prohibit. **The hash is the frozen object**: one copy of
> the grid, no duplicate to drift, no constant inlined — with the three cardinalities and the
> seven settings asserted individually as the content check. The post-G-05 **diff-empty** check
> is then the **same** mechanism, not a second one.

## 8. `AblationEntry` — five named, four reachable in Phase 1 *(Q5 = D)*

| ID | Phase 1 | Constraint |
|---|---|---|
| **`ABL-NODOY`** | **yes** | pre-freeze registry row required |
| **`ABL-DIFF`** | **yes** | **inverse-transforms to absolute TECU before any metric**, via `Transform.inverse` — which requires `transform_id` present on the `Prediction` (§ 2, § 3) |
| **`ABL-NOSW`** | **yes** | pre-freeze registry row required |
| **`ABL-HIST48`** | **yes** | runs **only after the primary configuration is frozen** — checkable against § 7's G-05 hash |
| **`ABL-ZENITH`** | **no — deferred to Phase 2** | it varies the hourly aggregation of the target (zenith-weighted versus IPP median), a choice that **does not exist** on the Phase 1 location-sampled gridded target. Recorded as a **phase deferral**, not an omission |

**Five named, four reachable here.** The count is stated both ways deliberately: dropping
`ABL-ZENITH` to four would understate TE §7.2's registry.

| Attribute | Meaning |
|---|---|
| `ablation_id` | one of the five |
| `run_id` | the registered run |
| `registered_at` | must **precede** the freeze |
| `folds`, `masks`, `tuning_budget` | **identical** to the primary configuration's |
| `phase_deferral` | set only for `ABL-ZENITH` |

**No promotion.** TE §7.2: *"no ablation configuration may be promoted to primary once the
locked test is opened."* Checked as **reported-primary-hash == G-05-frozen-hash**. Vision §2.4's
separate bar — no secondary result replaces the primary conclusion — reaches the **reporting**
unit and is recorded here as a **consumed** obligation, **not a check claimed by this unit**.

**Negative controls:** a **missing** required ablation **fails the check rather than passing
unnoticed**; an ablation **registered after results are seen fails**.

## 9. `HorizonSpec` — config-only, structurally *(Q7 = D)*

`experiment.yaml` exposes **`horizons: [1]`** with **24 implemented and testable but absent from
the default run list** (TE §2.1).

**Horizon travels as a parameter**, from `ConfigSnapshot` through `fit_predict`'s `snapshot`
argument to label construction. **No code path branches on a literal horizon value** — which is
what makes *"building the +24 h label must require no code change, only a config change"*
structural rather than test-enforced only.

**Negative control:** a code path branching on a literal horizon **fails a static check**, in the
pattern `governance-guards` R-28 and `features-and-splits` R-76a's third limb already use. A
`+24 h` path that requires a code edit **fails**.

## 10. `ImportanceFigure` — diagnostic, and the marker is the mechanism *(Q8 = D)*

| Attribute | Meaning |
|---|---|
| `model_id` | `"M-05"` |
| `authoritative` | **always `false`**. A recorded marker, not a convention |
| `payload_ref` | the saved figure |

**No Random Forest importance score adds, removes or ranks a feature into the production feature
set** (FR-P1-05-3; Vision §6.4; TE §6.4).

> **The evidence lives in a sibling, and that is stated rather than glossed.** FR-P1-05-3's
> criterion is *"the feature manifest's provenance shows no importance-derived selection"* — and
> the **feature manifest belongs to `features-and-splits`**. This unit **claims no check over
> it** and records it as a **consumed cross-unit dependency**, the same posture
> `features-and-splits` took toward `inventory-and-registry`'s station registry.
>
> **What this unit can enforce, and does:** an importance score reaching the **production feature
> path** — as distinct from the diagnostic artifact — **fails**, checked on this unit's **own**
> module graph.

## 11. `TransformStampMatch` — the eighth amendment's landing site *(Q1 = D)*

`features-and-splits`' **FU-4 = D** requires `06`/`07` to **refuse** a frame whose provenance
stamp is not `(fold k, evaluate)` when scoring fold *k*'s validation month. **This unit owns
`06`.**

The match is a **named function in `src/models/train.py`**, called by `06` before every scoring
path. It is **not** folded into `fit_predict`: `fit_predict` is a **training** call and cannot
know whether the caller is about to score fold *k*'s validation month, so it can check the stamp
is present and internally consistent but **not** that it matches the scoring intent. And it is
**not** written inline in the script: §7 places reusable logic in `src/` with scripts as
orchestrators.

| Input | Check |
|---|---|
| `bundle.fold_id` | equals the fold being scored |
| `bundle.purpose` | equals `evaluate` |
| `bundle.transform_id` | present — `None` is already `fit_predict`'s `LeakageError` |

**Negative controls**, stated in full to match `business-rules.md` R-90 and
`business-logic-model.md` W-1: a frame stamped **`(fold 4, train)`** reaching **fold 4's
validation scoring** **fails**; a frame stamped **`(fold 2, evaluate)`** reaching **fold 3's**
scoring **fails**; an **unstamped** frame reaching **any** scoring path **fails**.

**Control that must *not* fire:** a frame stamped **`(fold 4, evaluate)`** reaching **fold 4's**
validation scoring → **passes**. That is the ordinary path, and a check blocking it would be the
failure mode `features-and-splits` already hit once — a control that must not fire is as
load-bearing as one that must.

> ⚠ **Corrected 2026-08-24 (post-redo finding 1).** This list previously carried **two** of the
> three negative controls and **omitted the paired must-not-fire control entirely**, while R-90 and
> W-1 both carried all four. § 10 is where an implementer reads raise conditions, so the shortest
> list was in the most-read place. Same cross-representation sweep gap as the two findings before
> it, in a location neither earlier pass checked.

> **A cross-unit contract surface — semantic, not a call edge.** *(Corrected 2026-08-24,
> iteration-1 finding 2.)* The first draft said `features-and-splits`' `test_train_only_transforms.py`
> asserts against this function *"calling it directly rather than replaying a script"*. Its own R-74
> declares that test **manifest-based** — it *"reads the emitted stamps and asserts that refusal"* —
> and explicitly **not** monkeypatch-and-replay. What the sibling asserts is the **refusal's effect
> on emitted artifacts**. Both units still depend on the same match semantics, and neither owns
> them alone; the dependency is semantic rather than a call.
>
> **This covers `06` only.** FU-4 = D names **`06` and `07`**, and `unit-of-work.md` assigns `07`
> to **`evaluation-and-comparison`** — a different unit whose design has not run. `07`'s half of
> the refusal is **unowned and open**, carried to the gate rather than presumed discharged
> *(iteration-1 finding 3)*.

## 12. `IntegrityError` subclasses raised here

| Exception | Raised when |
|---|---|
| `SeedError` | fewer or more than three predictions reach `three_seed_mean`; the seed set is not **exactly** `expected_seeds`; an input has `seed is None`; an input's `model_id` is not `"M-06"`; the three-seed mean is applied to an unseeded family |
| `AlignmentError` | the three frames do not share an identical **(`station`, `interval_start_utc`)** index, as a set **and** in order |
| `PartitionError` | `partition_id` differs across the three inputs; a confirmatory prediction is built on a **training** partition |
| `LeakageError` | `bundle.transform_id is None` at `fit_predict`; `transform_id` differs across the three confirmatory inputs; a frame whose stamp is not `(fold k, evaluate)` reaches fold *k*'s validation scoring; an **unstamped** frame reaches any scoring path |

All four derive from `foundation`'s `IntegrityError` base, so the stage entry contract writes the
`aborted` registry row for any of them.

---

## Requirement coverage

| Requirement | Entities | Acceptance |
|---|---|---|
| FR-P1-04-14 | § 5 `TuningRecord`, § 7 `GridSpec` | ⚠ **NO ACCEPTANCE ROW** — candidate TA row via Vision §15.2 |
| FR-P1-05-1 | § 1 `ModelFamily` | WS-14, TA-12, TA-26 |
| FR-P1-05-2 | § 3 `ConfirmatoryPrediction`, § 4 `Checkpoint` | WS-15, TA-13 |
| FR-P1-05-3 | § 10 `ImportanceFigure` | ⚠ **NO ACCEPTANCE ROW** |
| FR-P1-05-4 | § 5 `TuningRecord` | ⚠ **NO ACCEPTANCE ROW** — WS-18 tests the open channel only |
| FR-P1-05-5 | § 7 `GridSpec` | ⚠ **NO ACCEPTANCE ROW** |
| FR-P1-05-6 | § 8 `AblationEntry` | ⚠ **NO ACCEPTANCE ROW** |
| FR-P1-05-21 | § 6 `FittedPartitionRecord` | ⚠ **NO ACCEPTANCE ROW** |
| FR-P1-05-22 | § 9 `HorizonSpec` | ⚠ **NO ACCEPTANCE ROW** |

**9 requirements, 7 with no §16/§19 acceptance row** — derived by reading the story map's rows,
not carried from prose. This unit **owns** WS-14, WS-15, TA-12, TA-13, TA-26 and **supports**
TA-20.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence, so `business-rules.md` opens at the next free number after `features-and-splits`. If per-unit numbering was intended, say so at the gate and the artifacts restart.
- **[assumption]** The **story map governs** where it and `unit-of-work.md` § 8 disagree, consistent with every sibling. Neither artifact is edited by this stage.
- **[assumption]** `src/models/*` shapes beyond the named boundary calls are **intra-package** and this stage's to specify (`component-methods.md` § Depth). **§ 11's match function is one of them**, so it owes **no** amendment — the total stays **8 across 5 units**, and § 6's Option D was declined precisely to avoid a ninth.
- **Open — BLK-03's contract limbs are an EXIT condition** on this unit and on `evaluation-and-comparison`, `statistical-inference` and `regimes-diagnostics-reporting`. **§ 3 authors the contract; approving it is the human's, at the gate.**
- **Open — BLK-04 ↓ and BLK-09 ↓** inherited from `features-and-splits`. Its 2026-08-24 answers supplied mechanism; **neither blocker is closed**.
- **Open — a new cross-unit contract surface**: § 11's match function, asserted against by `features-and-splits`' `test_train_only_transforms.py`. Two units depend on it; neither owns it alone.
- **Open — 7 of 9 requirements have no acceptance row**, four naming their own candidate TA row via Vision §15.2. **None is added here.**
- **Open — whether TA-11 reaches a model fit is unverified upstream** (§ 6). No reading adopted.
- **Closed, corrected 2026-08-24 — D-122's supervisor sign-off is NOT outstanding.** The first draft carried *"Approved — supervisor sign-off pending"*, which is the status of **D-126** and **D-128**, not D-122. The Vision decision register (line 1207) reads **"Approved; supervisor sign-off closed 2026-08-22"** by the project owner under the recorded student/supervisor authority equivalence (`CR-2026-08-22-TE-AMEND`; `GOV-2026-08-22-REM-01` Rec 4), noting that **no supervisor signature artifact exists and none is claimed** and that the seed values were verified unchanged before closure. `unit-of-work.md` § 8 already recorded the closure. **Found while verifying iteration-1 finding 1 against the source register; the reviewer did not raise it.**
- **G-09 is not signed**, and **BLK-03 independently bars implementation.** No entity here authorises creating any module.
- **Open — `07`'s half of the eighth amendment is UNOWNED.** FU-4 = D names **`06` and `07`**; `unit-of-work.md` assigns `07_evaluate_and_report.py` to **`evaluation-and-comparison`**, whose functional design has not run. This unit discharges `06` only. Raised at the gate so it is not discovered later *(iteration-1 finding 3)*.
- **Open — `requirements.md` FR-P1-05-2 carries TWO superseded clauses on one line, both reported and neither edited.** (a) It attributes bootstrap seed **20221201** to D-122, a reading `unit-of-work.md` § 8 records as corrected 2026-08-22 (`GOV-2026-08-22-UG-02` Rec 11) — the seed is frozen separately by **TE §13.6 / TC-19** (Q-27). (b) It states *"Vision §14.2 marks it 'Approved — supervisor sign-off pending'… still owes a signature at G-05"*, superseded by the same Vision-register closure at line 1207 that these artifacts cite correctly elsewhere — **"Approved; supervisor sign-off closed 2026-08-22"**. This unit follows the **corrected** reading of both. `requirements.md` is an approved upstream artifact and `CHANGE_RECORD_PROCEDURE.md` bars editing one absent owner approval for annotate-in-place, so both are **raised at the gate**. *(Clause (a) was iteration-1 finding 5; clause (b) is iteration-2 finding 2 — flagging one clause of a line and missing its neighbour is the same one-representation-short failure as iteration-2 finding 1, and clause (b) is where this author's own D-122 error originated.)*
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

---

> **Re-saved unchanged 2026-08-26 under the fourteenth-redo re-confirmation receipt** (redo taken
> for `external-products`; floor reset mechanical). **No entity here changed.** **G-09 remains
> unsigned, and BLK-03 independently bars implementation.**
