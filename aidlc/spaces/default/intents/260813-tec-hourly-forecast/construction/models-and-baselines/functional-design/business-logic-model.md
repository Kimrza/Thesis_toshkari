# Business Logic Model — `models-and-baselines`

**Unit** `models-and-baselines` (Bolt 8) · **Kind** `library` · **Depends on**
`features-and-splits`

The workflows this unit implements: the stamp match that guards every scoring path, the six
model families' fit-and-predict path, the three-seed confirmatory prediction and the contract
three downstream units inherit from it, checkpointing and restore, tuning and selection under a
criterion declared before December could be seen, the grid freeze, the predeclared ablations, the
config-only horizon, and the two evidence obligations that belong to siblings.

**Authored 2026-08-24** against `functional-design-questions.md` Q1–Q8 = **D, D, D, D, D, C, D,
D**. Unit **8 of 12**, the first designed from contracts rather than carried forward.

**No workflow here decides a scientific value.** D-121's grids, D-122's seeds, Vision §8.6's seven
fixed LSTM settings, Vision §8.7's selection criterion and TE §7.2's ablation registry are frozen
upstream and are **restated, never chosen**.

## Sources

- `../../../inception/application-design/component-methods.md` § `src/models` — `Prediction`, `fit_predict(model_id, *, bundle, partition, snapshot)`, `three_seed_mean(predictions, *, expected_seeds)`, `climatology_fit_partition(prediction)`, `Transform.inverse(frame)`. **Quoted, not re-invented.**
- `../../../inception/application-design/services.md` § The nine stage scripts — `06_train_and_predict.py` **reads** features and folds, **writes** predictions; § Stage entry contract; § Execution platforms, which records that a Kaggle session carries **no git working tree**.
- `../../../inception/units-generation/unit-of-work.md` § 8 — `Owns`, boundary, **BLK-03**, the six implementation notes.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2; **9 requirements, 7 with no acceptance row**; owns WS-14, WS-15, TA-12, TA-13, TA-26; supports TA-20.
- `../../../inception/requirements-analysis/requirements.md` — FR-P1-04-14, FR-P1-05-1…-6, -21, -22, each read with its `UNTESTED` note.
- `../features-and-splits/functional-design/` — **W-4a**, **W-4b**, **R-74**, § Amendments owed at **8 across 5 units**. FU-4 = D lands W-1 below.
- `../foundation/functional-design/` — `ConfigSnapshot`, the stage entry contract, the two-tier error posture.
- `evidence/DECISIONS.md` — **D-121**, **D-122**.

---

## W-1 — The stamp match, before every scoring path

```
INPUT   bundle, fold_being_scored
OUTPUT  None — proceeds, or raises
RAISES  LeakageError
```

A **named function in `src/models/train.py`**, called by `06_train_and_predict.py` before every
scoring path. It checks `bundle.fold_id` equals the fold being scored, `bundle.purpose` equals
`evaluate`, and `bundle.transform_id` is present.

**Why it exists at all.** `features-and-splits` answered **FU-4 = D** on 2026-08-24: its pairing
control asserted a scored frame *"was obtained from a call"* with `transform = T_k` and
`purpose=evaluate`, and that predicate turned out to be **unobservable** — `services.md` puts the
producing call in `05` and every scoring site in `06`/`07`, which read their frames from
**artifacts**. The remedy was a **provenance stamp** on the emitted artifacts and a **refusal at
the consumer**. This unit owns `06`. **This workflow is that refusal.**

**Why not folded into `fit_predict`.** `fit_predict` is a **training** call. It already raises
`LeakageError` when `bundle.transform_id is None`, and it can check the stamp is present and
internally consistent — but it **cannot know whether the caller is about to score fold *k*'s
validation month**, which is the half that matters. **Why not written inline in `06`.** §7 places
reusable logic in `src/` and makes scripts orchestrators; and `features-and-splits`'
manifest-based `tests/test_train_only_transforms.py` needs a function it can **call**, not a
script it must replay.

**Negative controls** (R-90): `(fold 4, train)` reaching fold 4's validation scoring → **fails**;
an **unstamped** frame reaching any scoring path → **fails**; `(fold 2, evaluate)` reaching fold
3's scoring → **fails**. **Must not fire:** `(fold 4, evaluate)` reaching fold 4's scoring →
**passes**.

> **Cost, and where it is counted.** This is the **eighth amendment's landing site**, already
> counted by `features-and-splits` as **8 across 5 units** with this unit as the fifth. The match
> function itself is an **intra-package** shape under `component-methods.md` § Depth, so it adds
> **no ninth**. But it **is** a cross-unit contract surface — a sibling's test asserts against it —
> and that is recorded rather than left implicit.

## W-2 — Fit and predict, over six families

```
fit_predict(model_id, *, bundle: FeatureBundle,
            partition: Partition, snapshot: ConfigSnapshot) -> Prediction
RAISES  LeakageError
```

**Quoted from `component-methods.md`.** It takes the **`FeatureBundle`** so the two
representations arrive together as `build_features` emitted them, and **raises `LeakageError`
when `bundle.transform_id is None`** — an untransformed bundle reaching training is the leak the
three-call sequence would otherwise leave live. `partition: Partition` replaces the earlier
`fold: FoldSpec` so **the refit and the locked month are expressible**.

The six families and their seeding are in `domain-entities.md` § 1. **Only M-06 is seeded**;
`Prediction.seed is None` for M-01…M-05 is **correct**, not a missing field.

**The horizon travels here** (W-8): from `snapshot` through to label construction, so no code
path branches on a literal horizon value.

**Boundary.** `src/models` imports `features-and-splits` and `foundation`. It **must not** import
`src/external/iri.py`, `src/external/gim.py` or `src/evaluation` — that dependency runs the other
way (R-102).

## W-3 — The confirmatory prediction, and BLK-03's four limbs

```
three_seed_mean(predictions, *, expected_seeds: frozenset[int]) -> Prediction
RAISES  SeedError, AlignmentError, PartitionError, LeakageError
```

The contract's four limbs are authored in full at `domain-entities.md` § 3 and enforced by R-91,
R-92 and R-93. In outline:

| Limb | What it fixes |
|---|---|
| **Input** | exactly three M-06 predictions whose seeds equal `expected_seeds`, read from **`ConfigSnapshot.seeds`** — never inlined in `src/models` |
| **Output** | a `Prediction` with `seed = None`, the element-wise mean on the shared index, provenance copied from the inputs; **the three inputs preserved by the caller** |
| **Allowed partitions** | F1–F4 validation months; the January–November refit; **December only through the locked-partition guard**, which is the G-06 path. **A training partition is refused** |
| **Failure conditions** | `SeedError`, `AlignmentError` on a non-identical **(`station`, `interval_start_utc`)** index, `PartitionError`, `LeakageError` |

**The mean carries its inputs' stamp or it fails.** `partition_id` and `transform_id` must agree
across the three inputs and are copied to the output. Without that the provenance dies at `06`,
which is the failure ADR-11 added the two fields to prevent — *"the stamp has to travel the whole
way, not just to the first consumer."*

**The downstream consumption contract** — five points three units cite rather than re-derive — is
at `domain-entities.md` § 3.

> **BLK-03's seed-value limb closed 2026-08-22** (D-122, values verified unchanged) and its
> **mechanism limb closed 2026-08-23** (`expected_seeds` added). **The contract limbs are what
> this workflow authors, and authoring is not approving.** BLK-03 remains an **exit condition** on
> this stage and on `evaluation-and-comparison`, `statistical-inference` and
> `regimes-diagnostics-reporting`.

## W-4 — Checkpointing and restore

M-06 checkpoints on **lowest validation RMSE** and restores that checkpoint, **not the last
epoch** — one of Vision §8.6's seven fixed settings (W-6), not a choice made here.
`domain-entities.md` § 4 gives the shape; R-94 gives the control.

**Acceptance: WS-15, TA-13**, `tests/test_checkpoint_restore.py`. **Negative control:** a restore
returning the last epoch → **fails**.

**TA-26** additionally requires the deterministic seed utility and serialization restore to pass
**locally and on Kaggle**. `services.md` § Execution platforms records that a Kaggle session
carries **no git working tree**, which is why the project's mandated rule runs the critical tests
**inside** the Kaggle session rather than relying on a commit hook.

## W-5 — Tuning, and the channel that stays open

Tuning uses **January–November only**. **The trigger is December being *seen*, not the locked test
being opened** — the required pre-G-05 coverage audit means December is legitimately seen earlier,
and that is precisely the channel this closes.

Three mechanisms, in `domain-entities.md` § 5 and enforced by R-95:

1. `partitions_read` excludes December.
2. The criterion **declared before tuning** equals the criterion **used** — hash against hash.
3. `audit_access_since_declaration`, read from `governance-guards` **R-25**'s durable log: a
   tuning run post-dating a December audit access **must state it**.

> **The residual, stated rather than buried.** A choice informed by a December **figure a human
> carries in their head** leaves no trace in any of the three. Mechanism 3 makes the overlap
> **visible for review**; it does not eliminate it, and no mechanism can.
> **FR-P1-05-4 is `UNTESTED`** and `requirements.md` records that **no existing row tests its
> actual trigger** — WS-18 tests the open channel only and stays on FR-P1-05-12, where it does test
> the thing named. A candidate TA row is owed via **Vision §15.2** and goes to the gate.

## W-6 — The grid freeze, content and immutability as one mechanism

The grid lives **once**, in `experiment.yaml`. What is frozen and compared is its **hash**,
committed before **G-05**. Asserted individually: **ridge 6, RF 18, LSTM 16** (D-121) and the
**seven** fixed LSTM settings — dropout **0.2**, **Adam**, **MSE** loss, max **100** epochs,
early-stopping patience **10** on validation RMSE, minimum improvement **1e-4 TECU**,
**best-checkpoint restoration**.

**Rejected alternatives, with reasons.** *Cardinality alone* lets a 16-member LSTM grid with the
wrong members pass — `requirements.md` warns against exactly this. *An expected membership list in
the test file* would inline a scientific constant in **source**, which TC-03e and `project.md`
§ Forbidden prohibit. *A duplicated expectation in config* invites a tautology comparing a value to
itself. **The hash avoids all three**, and makes the **post-G-05 diff-empty** check the same
mechanism rather than a second one.

**No grid range changes after December is seen; no second 2022 test period is selected after
results are observed.** Controls at R-96.

## W-7 — The ablations: five named, four reachable

`domain-entities.md` § 8 and R-97. `ABL-NODOY`, `ABL-DIFF`, `ABL-NOSW`, `ABL-HIST48` are Phase 1;
**`ABL-ZENITH` is deferred to Phase 2** because it varies the hourly aggregation of the target — a
choice that **does not exist** on the Phase 1 location-sampled gridded target. **Five named, four
reachable**, stated both ways so the count is not quietly reduced to four.

`ABL-DIFF` **inverse-transforms to absolute TECU before any metric** via `Transform.inverse`,
which needs `transform_id` on the `Prediction` — the same field W-3 protects. `ABL-HIST48` runs
**only after** the primary configuration is frozen, checkable against W-6's hash.

**No promotion once the locked test is opened**, checked as reported-primary-hash ==
G-05-frozen-hash. **Vision §2.4's bar** — no secondary result replaces the primary conclusion —
reaches `regimes-diagnostics-reporting` and is recorded here as a **consumed** obligation, **not a
check this unit claims**.

## W-8 — The +24 h horizon, structurally config-only

`experiment.yaml` exposes **`horizons: [1]`** with **24 implemented and testable but absent from
the default run list** (TE §2.1). Horizon travels as a **parameter** from `ConfigSnapshot` through
`fit_predict`'s `snapshot` to label construction, so **no code path branches on a literal horizon
value** — making *"building the +24 h label must require no code change"* structural rather than
test-enforced only, the same posture `features-and-splits` uses for window parity.

**Negative controls** (R-99): a literal-horizon branch → **fails a static check**; a `+24 h` path
requiring a code edit → **fails**; a `+24 h` path raising `NotImplementedError` → **fails** — the
case a config-shape assertion alone would pass.

## W-9 — M-03's fitting partition, and the reading not adopted

`climatology_fit_partition(prediction)` returns the partitions M-03 was **actually** fitted on;
every one must be a **training** partition. **Negative control:** a climatology fitted **across all
of 2022** → **fails** — which is the point, since such a climatology would **stop functioning as a
difficulty control** while passing every other stated check.

> **No reading adopted on TA-11.** Whether TA-11's *"train-only transforms"* reaches a **model
> fit** is **unverified upstream**; `requirements.md` declines to claim it and so does this stage.
> Confirming it, or adding a row, runs through **Vision §15.2** at the gate.
>
> **The tempting amendment was refused.** Stamping the fitted partitions onto `Prediction` would
> amend an approved boundary contract — a **ninth** amendment — for something the approved
> `climatology_fit_partition` already delivers.

## W-10 — Two evidence obligations that belong to siblings

**RF importance** (R-100). The figure is saved with `authoritative = false` **in its own
metadata**. But FR-P1-05-3's stated evidence is *"the feature manifest's provenance"*, and the
**feature manifest is `features-and-splits`'**. This unit records that as a **consumed cross-unit
dependency** and **claims no check over it** — the posture `features-and-splits` itself took toward
`inventory-and-registry`'s station registry. What this unit **can** enforce, and does: an
importance score reaching the **production feature path** → **fails**, checked on this unit's own
module graph.

**The primary results table** (TA-20). This unit **supports** it; `regimes-diagnostics-reporting`
owns it. The three mandatory difficulty controls — persistence, 24-hour seasonal persistence, and
the training-partition-only climatology — are **produced here** and **co-reported there**. The
binding honesty rule that a baseline beating the LSTM must appear in the primary results table and
the abstract-level conclusion is likewise the reporting unit's to honour; this unit's obligation is
to **produce all three controls**, which W-2 does.

## W-11 — What Bolt 8 builds, and what it must not

**Builds:** `src/models/persistence.py`, `climatology.py`, `ridge.py`, `random_forest.py`,
`lstm.py`, `train.py` (including W-1's match function), `checkpoint.py`;
`scripts/06_train_and_predict.py`; `tests/test_models_smoke.py`,
`tests/test_checkpoint_restore.py`. **Ten files.**

**Must not:** import `src/external/iri.py`, `src/external/gim.py` or `src/evaluation`; contain a
residual or GRU module; import PyTorch; inline the seed set, the grids or any of the seven LSTM
settings.

> **Nothing above authorises building any of it.** **G-09 is not signed**, and **BLK-03
> independently bars implementation** while its contract limbs stand unapproved.

---

## Requirement-to-workflow map

| Requirement | Workflow | Acceptance |
|---|---|---|
| FR-P1-04-14 | W-5, W-6 (R-101) | ⚠ **NO ACCEPTANCE ROW** |
| FR-P1-05-1 | W-2 (R-102) | WS-14, TA-12, TA-26 |
| FR-P1-05-2 | W-3, W-4 | WS-15, TA-13 |
| FR-P1-05-3 | W-10 (R-100) | ⚠ **NO ACCEPTANCE ROW** |
| FR-P1-05-4 | W-5 (R-95) | ⚠ **NO ACCEPTANCE ROW** |
| FR-P1-05-5 | W-6 (R-96) | ⚠ **NO ACCEPTANCE ROW** |
| FR-P1-05-6 | W-7 (R-97) | ⚠ **NO ACCEPTANCE ROW** |
| FR-P1-05-21 | W-9 (R-98) | ⚠ **NO ACCEPTANCE ROW** |
| FR-P1-05-22 | W-8 (R-99) | ⚠ **NO ACCEPTANCE ROW** |

**9 requirements, 7 with no §16/§19 acceptance row** — derived by reading the story map's rows,
printed before being asserted, not carried from prose. **Owns** WS-14, WS-15, TA-12, TA-13, TA-26.
**Supports** TA-20.

## Amendments owed

**Derived here, not carried.**

| Source | Owed | Basis |
|---|---|---|
| `features-and-splits` § Amendments owed | **8**, across **5** units | Derived there, after its own FU-4 = D re-derivation from 7-across-4. **Not restated** — a restated count drifts, which is the failure this row exists to avoid. |
| **This unit** | **0** | W-1's match function is an **intra-package** `src/models` shape under `component-methods.md` § Depth. `domain-entities.md` § 3's contract **describes** the approved `three_seed_mean` and `Prediction` without changing either signature. § 6's Option D — stamping fitted partitions onto `Prediction` — was **declined precisely to avoid a ninth**. |
| | **8 across 5 units** | 8 + 0 |

**This unit is the fifth**, as `features-and-splits` counted it: `06` and `07` are where the stamp
is refused. Nothing here adds to the total.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence, so `business-rules.md` runs **R-90…R-102**. If per-unit numbering was intended, say so at the gate and the artifacts restart.
- **[assumption]** The **story map governs** where it and `unit-of-work.md` § 8 disagree. Neither is edited by this stage.
- **[assumption]** `src/models/*` shapes beyond the named boundary calls are **intra-package** and this stage's to specify. **W-1's match function is one of them** — no amendment owed, total stays **8 across 5**.
- **Open — BLK-03's contract limbs are an EXIT condition** on this unit and on `evaluation-and-comparison`, `statistical-inference` and `regimes-diagnostics-reporting`. **W-3 authors the contract; approving it is the human's, at the gate.**
- **Open — BLK-04 ↓ and BLK-09 ↓** inherited from `features-and-splits`; its 2026-08-24 answers supplied mechanism, **neither is closed**.
- **Open — W-1's match function is a cross-unit contract surface**, asserted against by `features-and-splits`' `tests/test_train_only_transforms.py`. Neither unit owns it alone.
- **Open — 7 of 9 requirements have no acceptance row.** Four name their own candidate TA row via **Vision §15.2**; **none is added here**.
- **Open — whether TA-11 reaches a model fit is unverified upstream** (W-9). No reading adopted.
- **Open — D-122's supervisor signature** is owed at **G-05**; Vision §14.2 marks it *"Approved — supervisor sign-off pending"*.
- **Open — FR-P1-05-4's residual** (W-5): a December figure carried in a human's head is unreachable by any mechanism. Narrowed by the audit-access precondition, **not eliminated**.
- **G-09 is not signed**, and **BLK-03 independently bars implementation.** No workflow here authorises creating any of W-11's ten files.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.
