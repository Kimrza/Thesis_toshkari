# Domain Entities — `models-and-baselines`

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

> ⚠ **What this table does NOT do, stated 2026-08-28 because a rule elsewhere claimed it did.**
> This is a table of **allowed** partitions; the raise conditions are **limb 4's**, and limb 4 names
> exactly **two** `PartitionError` triggers for `three_seed_mean` — cross-input `partition_id`
> disagreement, and a training partition. **There is no "partition outside the enumeration"
> trigger**, here or anywhere in this unit. `business-rules.md` **R-96** previously implied one; its
> mechanism is restated there, in its own dated box, as the **upstream type-closure** it really is:
> `Partition.partition_id` is closed to the **six** values `features-and-splits` **R-80** fixes —
> `F1`, `F2`, `F3`, `F4`, `REFIT`, `DEC` (`component-methods.md:332`) — so a seventh test period is
> **not constructible upstream** and never arrives to be rejected. The guarantee is real; it just
> does not live in this unit. *(Residual carried on this unit's terminal READY of 2026-08-24 and
> re-verified unapplied by the 2026-08-26 confirming pass, finding 2; applied now under the owner's
> remediation authority.)*

### Limb 4 — failure conditions

| Raise | When |
|---|---|
| **`SeedError`** | fewer than three predictions; more than three; the seed set is not **exactly** `expected_seeds`; any input has `seed is None`; any input's `model_id` is not `"M-06"` |
| **`AlignmentError`** | the three frames do not share an **identical index**. The alignment key is stated explicitly: the ordered pair **(`station`, `interval_start_utc`)**, compared as a set **and** in order. Averaging misaligned predictions silently is the failure this exists for |
| **`PartitionError`** | `partition_id` differs across the three inputs, or names a training partition (limb 3) — a **declared-identity** disagreement (§ 12) |
| **`LeakageError`** | `transform_id` differs across the three inputs, or is `None` on any of them — a disagreement that **implies information flow** (§ 12) |

**The discriminating rule between the last two is stated once, at § 12**, and R-90 and
`business-rules.md` R-92 cite it rather than restating it. It matters across a unit boundary:
`evaluation-and-comparison` **R-105** limb 2 currently raises `LeakageError` for the
`partition_id`-mismatch condition it describes as mirroring R-92, and is being corrected in
parallel to raise `PartitionError`. *(Added 2026-08-28, `GOV-2026-08-28-FD-01` Recommendation 8.)*

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
stamp is not `(partition k, role "score")` when scoring partition *k*. **This unit owns `06`.**

The match is a **named function in `src/models/train.py`**, called by `06` before every scoring
path. It is **not** folded into `fit_predict`: `fit_predict` is a **training** call and cannot know
which partition the caller is about to score, so it can check the stamp is present and internally
consistent but **not** that it matches the scoring intent. And it is **not** written inline in the
script: §7 places reusable logic in `src/` with scripts as orchestrators.

**The three checks, against the `Partition` being scored**, quoted from ADR-11's live contract
(`component-methods.md:719`) and matching `business-rules.md` R-90 exactly:

| Input, as ADR-11 declares it | Check | Raises |
|---|---|---|
| `bundle.spec.partition_id` (`FrameSpec.partition_id`, `component-methods.md:541`) | equals `partition_being_scored.partition_id` | **`PartitionError`** |
| `bundle.spec.role` (`Literal["train", "score"]`, `:542`) | equals **`"score"`** | **`PartitionError`** |
| `bundle.transform_id` | not `None`, **and** equal to that partition's own `Transform.transform_id` | **`LeakageError`** |

The split follows § 12's discriminating rule: the first two are **declared-identity**
disagreements, the third **implies information flow**.

**Negative controls**, stated in full to match `business-rules.md` R-90 and
`business-logic-model.md` W-1 — **four now, not three**:

| # | The frame's `spec` | Reaching | Raises |
|---|---|---|---|
| 1 | `FrameSpec(partition_id="F4", role="train", …)` | F4's score path | **`PartitionError`** |
| 2 | `transform_id is None`, any `spec` | **any** score path | **`LeakageError`** |
| 3 | `FrameSpec(partition_id="F2", role="score", …)` | F3's score path | **`PartitionError`** |
| 4 | `role="score"`, `partition_id="F3"`, carrying **F1's** `transform_id` | F3's score path | **`LeakageError`** |

Control 3 is asserted **by enumeration over ordered pairs of R-80's six `partition_id` values** —
`F1`, `F2`, `F3`, `F4`, `REFIT`, `DEC` (`component-methods.md:332`) — not on one sampled pair.

**Control that must *not* fire:** `FrameSpec(partition_id="F4", role="score", …)` carrying **F4's
own** `transform_id`, reaching **F4's** score path → **passes**. That is the ordinary path, and a
check blocking it would be the failure mode `features-and-splits` already hit once — a control that
must not fire is as load-bearing as one that must.

> ⚠ **REWRITTEN 2026-08-28 — this table named three `FeatureBundle` fields ADR-11 retired.**
> *(`GOV-2026-08-28-FD-01` **Recommendation 3** — `IMPL-01`, Critical, veto exercised; owner-approved.
> This section is the **mirror** the report cites at `domain-entities.md:353`; the primary is R-90,
> whose box carries the full derivation.)*
>
> **Superseded table, preserved verbatim:**
>
> | Input | Check |
> |---|---|
> | `bundle.fold_id` | equals the fold being scored |
> | `bundle.purpose` | equals `evaluate` |
> | `bundle.transform_id` | present — `None` is already `fit_predict`'s `LeakageError` |
>
> **Superseded controls, preserved verbatim:** *"a frame stamped **`(fold 4, train)`** reaching
> **fold 4's validation scoring** **fails**; a frame stamped **`(fold 2, evaluate)`** reaching
> **fold 3's** scoring **fails**; an **unstamped** frame reaching **any** scoring path **fails**"*
> and *"a frame stamped **`(fold 4, evaluate)`** reaching **fold 4's** validation scoring →
> **passes**"*. Superseded heading clause: *"a frame whose provenance stamp is not `(fold k,
> evaluate)` when scoring fold *k*'s validation month"*.
>
> **In one line:** `fold_id` left `FeatureBundle` with `FoldSpec`'s retirement on 2026-08-23
> (`component-methods.md:309`) and lives on now only as a TE §13.4 registry column and on § 4's
> `Checkpoint`; `purpose` is a **`governance-guards` `AccessRecord`** field (`:270`) whose three
> literals are `"coverage_audit" | "regime_audit" | "locked_evaluation"`, never a `FeatureBundle`
> attribute; and `"evaluate"` is a value of neither `purpose` nor `role`. The live triple is
> `spec.partition_id`, `spec.role`, `transform_id`.
>
> **Two of the four controls also changed raise type** — 1 and 3 now raise `PartitionError` under
> § 12's rule — and **control 4 is new**, so that the transform limb is falsifiable on a *stamped*
> frame and not only on the `None` case.

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

> ⚠ **The paragraph above is HISTORY as of 2026-08-28 — `07`'s half is owned.** *(Superseded:*
> "a different unit whose design has not run" *and* "`07`'s half of the refusal is **unowned and
> open**"*.)* `evaluation-and-comparison`'s design has run; its **R-105** claims `07`'s half at the
> object `07` receives (`Prediction`s, not frames) and cites R-90 by name, and
> `statistical-inference` **R-113** limb 2 imports it. **This section still covers `06` only** — that
> half of the sentence stands. The live residual is a **type** disagreement, not an ownership gap:
> R-105 limb 2 raises `LeakageError` for the `partition_id`-mismatch condition it says mirrors R-92,
> and § 12's rule assigns `PartitionError`. **That was corrected by the sibling in parallel and
> re-verified 2026-08-28**: R-105 limb 2 now raises `PartitionError`, *"the same exception R-92 raises
> for the same condition"*, with limb 1 keeping `LeakageError` for an **absent** stamp and running
> first — a refinement § 12 accepts, since an absent stamp is not a disagreement. **This unit edits
> no sibling artifact.**

## 12. `IntegrityError` subclasses raised here

| Exception | Raised when |
|---|---|
| `SeedError` | fewer or more than three predictions reach `three_seed_mean`; the seed set is not **exactly** `expected_seeds`; an input has `seed is None`; an input's `model_id` is not `"M-06"`; the three-seed mean is applied to an unseeded family |
| `AlignmentError` | the three frames do not share an identical **(`station`, `interval_start_utc`)** index, as a set **and** in order |
| `PartitionError` | `partition_id` differs across the three confirmatory inputs; a confirmatory prediction is built on a **training** partition; **`bundle.spec.partition_id` differs from the partition being scored** (§ 11, R-90); **`bundle.spec.role != "score"` on a scoring path** (§ 11, R-90) |
| `LeakageError` | `bundle.transform_id is None` at `fit_predict`; `transform_id` differs across the three confirmatory inputs; **a frame reaching a scoring path carries no `transform_id`, or one that is not that partition's own** (§ 11, R-90) |
| `LockedTestError` | **`06` would exit with a `DEC` prediction file on disk and no durably-flushed `PredictionHashReceipt` for it**; a receipt whose `sha256` does not match the file as written (§ 13, R-102a) |

**Five**, all deriving from `foundation`'s `IntegrityError` base, so the stage entry contract writes
the `aborted` registry row for any of them.

**The discriminating rule between `PartitionError` and `LeakageError`**, stated once here and cited
by R-90 and R-92 rather than restated:

| The disagreement is about… | Raises | Because |
|---|---|---|
| **Which partition this is** — a `partition_id` mismatch, input-versus-input or frame-versus-intent | **`PartitionError`** | a **declared-identity** disagreement. Two artifacts disagree about an identity; no information has moved |
| **Whether these are training rows** — a training partition, or `spec.role == "train"` where a scored frame is required | **`PartitionError`** | the same class: a **declared-role** disagreement. In-sample numbers, not future information |
| **Which rows the fit saw** — `transform_id` absent, or not this partition's own | **`LeakageError`** | it **implies information flow**: a transform fitted elsewhere has touched these rows, or the fit is unrecorded and therefore unknown |

> ⚠ **AMENDED 2026-08-28 — `PartitionError` is the FIFTEENTH project exception; the table grew from
> four rows to five; and the `LeakageError` row's retired vocabulary was replaced.**
> *(`GOV-2026-08-28-FD-01` **Recommendation 8** — `CHAIR-05`/`ML-05`/`IMPL-02`, High; owner ruled
> **option 1**. And **Recommendation 1** for the `LockedTestError` row.)*
>
> **Superseded rows, preserved verbatim:**
> - `PartitionError` — *"`partition_id` differs across the three inputs; a confirmatory prediction is
>   built on a **training** partition"*
> - `LeakageError` — *"`bundle.transform_id is None` at `fit_predict`; `transform_id` differs across
>   the three confirmatory inputs; a frame whose stamp is not `(fold k, evaluate)` reaches fold *k*'s
>   validation scoring; an **unstamped** frame reaches any scoring path"*
> - the roll-up sentence — *"**All four** derive from `foundation`'s `IntegrityError` base"*
>
> **What was wrong, three things.** (1) The `LeakageError` row carried R-90's retired
> `(fold k, evaluate)` vocabulary — Recommendation 3's defect, mirrored here. (2) Both rows omitted
> R-90's conditions as **conditions**, so this table — the place an implementer reads raise
> conditions — under-enumerated the guard it shares with § 11. (3) `PartitionError` itself sat
> outside `foundation` R-01's asserted *"all fourteen"* with **no `[assumption]` tag and no reference
> to R-01's any-future clause**, while reaching **10 of 12 units** (**71** occurrences across all
> **48** artifacts; **23** here before this edit, the largest share of any unit — all derived
> programmatically and printed before assertion).
>
> **The amendment — LANDED, and re-verified at the close of this pass.** `PartitionError` is declared
> in **`foundation` R-01** as the **fifteenth**. Mid-pass R-01 still read *"All fourteen"* and this
> box was first drafted saying the amendment was *"in flight in parallel"*; **it has since landed and
> R-01 was re-read directly.** It now reads *"**Every project-defined exception derives from
> `IntegrityError`** … **Fifteen are named in the enumeration below** … and — **added 2026-08-28** —
> **`PartitionError`** (`models-and-baselines`, declared in **`src/models/`** ⚠ **RULED 2026-08-28 — `PartitionError` is declared in `src/data/config.py`.** *(Project decision owner, on the `functional-design` gate, amending the wording of the Rec 8 ruling. **Superseded wording, preserved: declared in `src/models/`.**)* The reason is the one `features-and-splits` raised and the Rec 8 ruling could not have known: `component-dependency.md` marks **`src/features` → `src/models`** and **`src/data` → `src/models`** both as **`—`**, while every `PartitionError` raise in that unit lives in `src/data/splits.py` or `src/features/*` — so on the approved matrix that unit could not have raised the exception at all. `src/data/config.py` is where R-01 already declares `IntegrityError` and the base every unit already imports, so **no dependency-matrix amendment is needed and none is taken**. `models-and-baselines` remains the exceptions **semantic owner** — R-92s discriminating rule is unchanged — but is no longer its declaration site. )"*, and its Sources line
> cites **this section as *"the authority for R-01's fifteenth entry"*** — which is why the
> discriminating rule is stated here in full rather than by reference. **The draft's "in flight"
> wording is superseded and recorded, not left standing.** R-01 also **restated its own count as
> derived rather than asserted**, and records **33** distinct project-defined `*Error` names across
> the twelve units — **15** enumerated, **18** riding the any-future clause. **This unit raises none
> of the eighteen**, and still **claims no check** over `foundation`'s text. Two siblings modelled the
> right disclosure discipline — `fixtures-and-reproducibility` labels `FixtureError` *"a fifteenth,
> named at the gate"* (a label whose numeral now needs correcting, which is **that unit's** to do),
> `statistical-inference` labels `InverseTransformError` unit-local under R-01's clause — and this
> unit had modelled none.
>
> **`LockedTestError` is raised here for the first time.** R-01 attributes it to
> `governance-guards`. R-102a raises it at `06`'s exit deliberately, so that producer and consumer
> refusal carry **one type** across the `06` → `07` boundary — `evaluation-and-comparison` R-109
> limb 1 and `statistical-inference` R-113 limb 3 both raise `LockedTestError` for the absent
> receipt. It derives from `IntegrityError`, so R-10's `aborted` row still gets written. Per
> `foundation`'s own open cross-unit obligation — *"each of those units' `functional-design` must
> declare its own exceptions as `IntegrityError` subclasses"* — **this row is that declaration.**

## 13. `PredictionHashReceipt` — hash-before-metrics, written by `06`

> **ADDED 2026-08-28** — `GOV-2026-08-28-FD-01` **Recommendation 1** (`VAL-01`, Critical, veto
> exercised), owner-approved **option 1**. Rules at **R-102a**. **Section count 12 → 13**, derived by
> counting `^## \d+\.` in this file.

**Fields, matching `evaluation-and-comparison` `domain-entities.md` § 5 exactly** — that unit
declared the shape as a consumable precondition and this section is the **producer** half, so the
field list is quoted rather than re-invented:

| Attribute | Meaning |
|---|---|
| `prediction_path` | the `DEC` prediction file this receipt is for |
| `sha256` | its hash, computed over the file **as written** |
| `recorded_at_utc` | when that hash was computed — **before any metric exists** |
| `run_id` | the `06` run that wrote it, joining to the registry row |
| `partition_id` | **`"DEC"`** for the one-shot locked evaluation |

**Who writes it, and who may not.** `06_train_and_predict.py`, at the one-shot `DEC` prediction
write, **durably flushed before `06` exits**. `06` **refuses to exit** with a `DEC` prediction file
and no receipt, raising **`LockedTestError`** (§ 12). **`07_evaluate_and_report.py` and
`vector_block_bootstrap` may not be the writer**, and the reason is the whole mechanism: both are
metric callers, and a receipt timestamped by the process that computes the metric makes *"the
receipt precedes the metric"* **self-certifying** — satisfied by construction on every run,
including one where the prediction was regenerated after a score was seen. Writer and reader must
sit in **different processes**, with a file and a registry row between them.

**On the registry row.** The receipt's `sha256` becomes **`prediction_hash`** — TE §13.4's
**eighteenth** column of **twenty**, derived by counting the fenced list at
`Technical_Environment_and_Research_Implementation(1)(2).md:821–826` — on `06`'s own row, **joined by
`run_id`**. `foundation` **R-18** owns the row and its write-time twenty-column assertion; this
section owns the receipt column 18 is populated from. **`prior_period_exposure` is not written by
this unit**, and on a Phase 1 row its value is **`false`** — see the deviation box below.

**Who consumes it.** `evaluation-and-comparison` § 5 and **R-109** limb 1; `statistical-inference`
**R-113** limb 3. Both re-verify the file against `sha256` before computing (write-once
*detection*, not assumed absence) and raise `LockedTestError` on absence, mismatch, or a
`recorded_at_utc` not preceding the call.

> **Why this section exists at all — the obligation had two consumers and no producer.** Derived
> across all **48** artifacts before this edit and printed rather than carried:
> `PredictionHashReceipt` = **0** in this unit's four files (**5** hits project-wide, all in the two
> consuming units); *"prediction hash"* = **0** here; **`prediction_hash` = 0** and
> **`prior_period_exposure` = 0** across **all 48**. Three sibling passages state the write is
> **`06`'s act** — this unit's own script — and this unit mentioned it **zero** times. As designed,
> **G-06 could not execute**: every `DEC` metric entry point raises `LockedTestError` forever.
>
> **No amendment, and no eleventh file.** An **intra-package `src/models` shape** under
> `component-methods.md` § Depth, written by a script already in `business-logic-model.md` W-11's
> build list, hashing via `src/data/release.py`'s consolidated SHA-256 helper. **No approved boundary
> signature changes** — `fit_predict`, `three_seed_mean` and `climatology_fit_partition` are
> untouched — so this unit's amendment ledger stays at **0** and W-11's **"Ten files"** stands.
>
> **Whose requirement, so no coverage is claimed.** **FR-P1-05-12 is `governance-guards`'**
> (`unit-of-work-story-map.md:108`; **WS-18, TA-18**). This unit owns the script that performs the
> act, not the requirement or its rows. **No WS-18 or TA-18 coverage is claimed**, and § Requirement
> coverage below is unchanged: still **9 requirements, 7 without a §16/§19 row**.
>
> ⚠ **DEVIATION FROM THE APPROVED REMEDIATION TEXT — `prior_period_exposure` is `false` on a Phase 1
> row, so this section writes no `true`.** The remediation said *"`prior_period_exposure = true`"*.
> `foundation` **W-6 step 5**, amended 2026-08-28 on the same report, **refuses `true` on a Phase 1
> row**: *"Phase 1 *is* the first December exposure; `true` belongs to the Phase 2 replication (TE
> §7.0B)."* TE §7.0B (`:372`) makes the flag a **Phase 2** predicate — *"The Phase 2 December run is a
> fixed-protocol replication **because Phase 1 has already exposed December**"* — and **this unit is
> Phase 1** (NFR-PHASE-01), so `true` would be a false statement about the run. R-18 also settles the
> attribution the first draft raised as open: **source `governance-guards`' locked-test guard**,
> **destination `foundation`'s registry row**, **this unit neither** — so this section claims no check
> over it. **Raised for the owner** at `business-rules.md` R-102a: if Recommendation 1 meant a
> different predicate, it needs a different field name. Nothing is assumed.
>
> **The registry side has landed and interlocks with this section.** `foundation` **R-18** carries TE
> §13.4's twenty columns with `prediction_hash` at **column 18**, names
> `scripts/06_train_and_predict.py` as the receipt's writer with **these exact five fields** and the
> durable flush, and its **W-6 step 4 refuses a `prediction_hash` presented by the metric-computing
> process** — the destination-side complement to this section's producer-side rule.
> `prior_period_exposure` is held there as one of **three named extensions** outside the twenty *"so
> the twenty-column assertion stays literally checkable"*. The draft's *"in flight in parallel"*
> wording is superseded.
>
> **Naming a shape here is not authority to write it.** **G-09 is not signed** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged., **BLK-03
> independently bars implementation**, and the `DEC` write is additionally barred until **G-05 is
> signed** by `features-and-splits` **R-82** and `governance-guards`' access chokepoint.

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
- **[assumption]** `src/models/*` shapes beyond the named boundary calls are **intra-package** and this stage's to specify (`component-methods.md` § Depth). **§ 11's match function is one of them**, and so is **§ 13's `PredictionHashReceipt`**, so this unit owes **no** amendment; § 6's Option D was declined precisely to avoid a ninth. ⚠ **The figure this line carried — "the total stays 8 across 5 units" — is SUPERSEDED.** The live chain total is **7 across 5 units**; **this unit's own contribution is 0 either way.** The full re-derivation, term by term with the source line for each, is in `business-rules.md` § Assumptions & Open Questions, annotated in place under `GOV-2026-08-28-FD-01` **Recommendation 32** rather than restated here — a restated count drifts, which is the failure the § Amendments owed table has warned about since it was written.
- **[assumption]** Entity sections run **1…13** — **13**, derived by counting `^## \d+\.` in this file before asserting. § 13 was added 2026-08-28 (Recommendation 1). The `## Review` sections in `business-logic-model.md` recorded **12** at their own dates and remain correct as of those dates.
- **CLOSED 2026-08-28 — `PartitionError` is the fifteenth project exception; `foundation` R-01's amendment HAS LANDED** (§ 12's box; Recommendation 8, owner-ruled option 1). Re-read directly at the close of this pass: R-01 names **fifteen**, adds `PartitionError` (`models-and-baselines`, ~~declared in `src/models/`~~ ⚠ **RULED 2026-08-28: declared in `src/data/config.py`** — *annotation added 2026-08-30 on adversarial finding 1, Major; this bullet restated the superseded location verbatim while § 12's box already carried the ruling, and the § Assumptions section is the one a gate approver actually reads*. The owner amended the Rec 8 wording because `component-dependency.md` marks **`src/features` → `src/models`** and **`src/data` → `src/models`** both **`—`**, so the unit raising it could not have imported from `src/models/` at all; `src/data/config.py` is where R-01 already declares `IntegrityError`, so **no matrix amendment is needed**. **This unit remains the exception's SEMANTIC OWNER — R-92's discriminating rule is unchanged — but is no longer its DECLARATION SITE**), restates its count as **derived**, and cites **§ 12 above as the authority for the fifteenth entry**. *(Mid-pass it read "All fourteen"; the draft's "in flight" wording is superseded and recorded.)* Derived before this edit: **10 of 12 units**, **71** occurrences across all **48** artifacts, **23** here.
- ⚠ **DEVIATION FROM THE APPROVED REMEDIATION TEXT — the one item needing an owner ruling.** The remediation said `prior_period_exposure = true`; **§ 13 writes no `true`**, because `foundation` **W-6 step 5** refuses `true` on a **Phase 1** row and TE §7.0B (`:372`) makes the flag a **Phase 2** predicate. R-18 settles the attribution — source `governance-guards`, destination `foundation`'s row, **this unit neither**. Reasoning at § 13's deviation box and `business-rules.md` R-102a. **Nothing is assumed either way.**
- **Open — R-01's eighteen any-future exceptions are a residual this unit does not carry.** `foundation`'s amended R-01 records **33** distinct project-defined `*Error` names, **15** enumerated and **18** on the any-future clause, each still owing its own subclass declaration. **This unit raises none of the eighteen**: its **five** — `SeedError`, `AlignmentError`, `PartitionError`, `LeakageError`, `LockedTestError` — are all enumerated in R-01 and all declared at § 12.
- **Open — this unit now raises `LockedTestError`** (§ 12, § 13, R-102a), which `foundation` R-01 attributes to `governance-guards`. Chosen deliberately so producer and consumer refusal carry **one type** across `06` → `07`. § 12's row is this unit's declaration under `foundation`'s open cross-unit obligation.
- **Open — `prior_period_exposure`: contested writer, and a column that does not yet exist** (§ 13's box). TE §7.0B and FR-P1-05-12 attribute the record to *"the locked-test guard"*; the owner's ruling puts it on `06`'s registry row. And it is **not** among TE §13.4's twenty columns. Both go to the gate.
- **Open — FR-P1-05-12 is `governance-guards`', not this unit's.** § 13 discharges the `06`-side act only; **no WS-18 or TA-18 coverage is claimed** and § Requirement coverage is unchanged at **9 requirements, 7 without a row**.
- **Resolved 2026-08-28 — the two residuals that rode the terminal READY.** § 3 limb 3's box now records that no *"outside the enumeration"* `PartitionError` trigger exists in this unit and that R-80's six-row list is the real closure (R-96's mechanism, restated there); and `business-rules.md` R-95's field pair is corrected to `criterion_hash` / `criterion_used_hash`, matching § 5's authoritative table, which had carried the correction since 2026-08-24. **A third defect, previously unraised, was found in the same sweep:** R-95 mechanism 3 read `AccessRecord.timestamp`; `AccessRecord` has **seven** fields and none is `timestamp` (`component-methods.md:266–273`) — the retrieval field is `retrieved_at_utc`, and the `purpose`-absence fallback was conditioned on a false premise and is withdrawn.
- **Open — BLK-03's contract limbs are an EXIT condition** on this unit and on `evaluation-and-comparison`, `statistical-inference` and `regimes-diagnostics-reporting`. **§ 3 authors the contract; approving it is the human's, at the gate.**
- **Open — BLK-04 ↓ and BLK-09 ↓** inherited from `features-and-splits`. Its 2026-08-24 answers supplied mechanism; **neither blocker is closed**.
- **Open — a new cross-unit contract surface**: § 11's match function, asserted against by `features-and-splits`' `test_train_only_transforms.py`. Two units depend on it; neither owns it alone.
- **Open — 7 of 9 requirements have no acceptance row**, four naming their own candidate TA row via Vision §15.2. **None is added here.**
- **Open — whether TA-11 reaches a model fit is unverified upstream** (§ 6). No reading adopted.
- **Closed, corrected 2026-08-24 — D-122's supervisor sign-off is NOT outstanding.** The first draft carried *"Approved — supervisor sign-off pending"*, which is the status of **D-126** and **D-128**, not D-122. The Vision decision register (line 1207) reads **"Approved; supervisor sign-off closed 2026-08-22"** by the project owner under the recorded student/supervisor authority equivalence (`CR-2026-08-22-TE-AMEND`; `GOV-2026-08-22-REM-01` Rec 4), noting that **no supervisor signature artifact exists and none is claimed** and that the seed values were verified unchanged before closure. `unit-of-work.md` § 8 already recorded the closure. **Found while verifying iteration-1 finding 1 against the source register; the reviewer did not raise it.**
- **G-09 is not signed** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged., and **BLK-03 independently bars implementation.** No entity here authorises creating any module.
- ~~**Open — `07`'s half of the eighth amendment is UNOWNED.**~~ **CLOSED 2026-08-28.** *(Superseded text preserved:* "FU-4 = D names **`06` and `07`**; `unit-of-work.md` assigns `07_evaluate_and_report.py` to **`evaluation-and-comparison`**, whose functional design has not run. This unit discharges `06` only. Raised at the gate so it is not discovered later *(iteration-1 finding 3)*." *)* That unit's design has run and its **R-105** claims `07`'s half, citing R-90 by name. **This unit still discharges `06` only** — that half of the superseded entry stands. What survives is a **type** disagreement, recorded above and at § 11's closure box, not an ownership gap.
- **Open — `requirements.md` FR-P1-05-2 carries TWO superseded clauses on one line, both reported and neither edited.** (a) It attributes bootstrap seed **20221201** to D-122, a reading `unit-of-work.md` § 8 records as corrected 2026-08-22 (`GOV-2026-08-22-UG-02` Rec 11) — the seed is frozen separately by **TE §13.6 / TC-19** (Q-27). (b) It states *"Vision §14.2 marks it 'Approved — supervisor sign-off pending'… still owes a signature at G-05"*, superseded by the same Vision-register closure at line 1207 that these artifacts cite correctly elsewhere — **"Approved; supervisor sign-off closed 2026-08-22"**. This unit follows the **corrected** reading of both. `requirements.md` is an approved upstream artifact and `CHANGE_RECORD_PROCEDURE.md` bars editing one absent owner approval for annotate-in-place, so both are **raised at the gate**. *(Clause (a) was iteration-1 finding 5; clause (b) is iteration-2 finding 2 — flagging one clause of a line and missing its neighbour is the same one-representation-short failure as iteration-2 finding 1, and clause (b) is where this author's own D-122 error originated.)*
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

---

> **Re-saved unchanged 2026-08-26 under the fourteenth-redo re-confirmation receipt** (redo taken
> for `external-products`; floor reset mechanical). **No entity here changed.** **G-09 remains
> unsigned, and BLK-03 independently bars implementation.**

> ## ⚠ AMENDED 2026-08-28 — `GOV-2026-08-28-FD-01` REMEDIATION (verdict FAIL)
>
> A redo jump cleared the write-freeze so the owner-approved remediations could be applied. **What
> changed in this file:**
>
> | Change | Recommendation | Section |
> |---|---|---|
> | § 11's three-field check rewritten onto ADR-11's `spec.partition_id` / `spec.role` / `transform_id`; four negative controls, two with new raise types | **3** (`IMPL-01`, Critical, **veto**) | **§ 11** |
> | New entity: `PredictionHashReceipt`, written by `06`, refusal-to-exit | **1** (`VAL-01`, Critical, **veto**) | **§ 13** (new) |
> | `PartitionError` as the fifteenth exception; the discriminating rule; `LockedTestError` added; table four rows → **five** | **8** (High) | **§ 12**, § 3 limb 4 |
> | Stale amendment total marked superseded, pointing at `business-rules.md`'s in-place re-derivation | **32** (Medium) | § Assumptions |
> | R-96's mechanism recorded as R-80's upstream type-closure, not a local enumeration check | carried residual | § 3 limb 3 |
>
> **Section count 12 → 13**, derived. **No approved boundary signature changed** — `Prediction`
> (§ 2), `fit_predict`, `three_seed_mean` (§ 3), `climatology_fit_partition` (§ 6) and
> `Transform.inverse` are all still quoted from `component-methods.md` unmodified, and this unit
> still owes **0** amendments. **No scientific value, grid, seed, threshold or frozen constant
> changed.** No sibling artifact and no `functional-design-questions.md` was edited. Every prior
> dated ⚠ box is preserved.
>
> **BLK-03 remains an open exit condition and G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged. Naming a shape here — § 13
> included — is not authority to write a module, and nothing above closes BLK-03.**

---

> **Re-confirmation receipt, 2026-08-29 — `models-and-baselines`.** The 2026-08-27T21:49:36Z REDO jump reset every unit's
> receipt floor, and this unit's content had already changed after that floor under the 2026-08-28
> post-execution pass (D-29 through D-32; **G-09 signed under D-31 with its TE §18.3 preconditions
> disclosed unmet**). The owner re-confirmed that post-execution content via the Consolidated
> Summary Confirmation at the foot of `functional-design-questions.md`, receipted `2026-08-29`.
> **No line above this marker was touched by this pass**, no count was re-derived, and nothing here
> discharges TA-15, WS-18 or TA-18, creates `aws_ai_dlc_preflight_report`, or alters the fact that
> stage 3.1 remains **FAIL** with no board having passed it.
