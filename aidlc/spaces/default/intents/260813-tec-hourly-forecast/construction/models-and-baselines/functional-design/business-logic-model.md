# Business Logic Model — `models-and-baselines`

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

The workflows this unit implements: the stamp match that guards every scoring path, the six
model families' fit-and-predict path, the three-seed confirmatory prediction and the contract
three downstream units inherit from it, checkpointing and restore, tuning and selection under a
criterion declared before December could be seen, the grid freeze, the predeclared ablations, the
config-only horizon, the two evidence obligations that belong to siblings, and the one-shot `DEC`
write whose hash receipt must precede any metric.

**Authored 2026-08-24** against `functional-design-questions.md` Q1–Q8 = **D, D, D, D, D, C, D,
D**. Unit **8 of 12**, the first designed from contracts rather than carried forward.

**No workflow here decides a scientific value.** D-121's grids, D-122's seeds, Vision §8.6's seven
fixed LSTM settings, Vision §8.7's selection criterion and TE §7.2's ablation registry are frozen
upstream and are **restated, never chosen**.

> ## ⚠ AMENDED 2026-08-28 — `GOV-2026-08-28-FD-01` REMEDIATION (verdict FAIL)
>
> A redo jump cleared the write-freeze so the project decision owner's approved remediations on this
> unit could be applied. **This box is placed at the head of the file, not the tail, because the
> tail is a preserved `## Review` section.** Every change carries its own dated box at the point of
> change; nothing is deleted, and every superseded sentence is preserved verbatim beside its
> replacement.
>
> | # | Change | Recommendation | Where in this file |
> |---|---|---|---|
> | 1 | The stamp-match guard rewritten onto ADR-11's live contract — `spec.partition_id`, `spec.role`, `transform_id`, replacing the retired `fold_id`/`purpose`/`"evaluate"` | **3** (`IMPL-01`, Critical, **veto**) | **W-1** — signature block, checks, and the four negative controls |
> | 2 | New workflow: `06` writes the prediction-hash receipt and refuses to exit without it | **1** (`VAL-01`, Critical, **veto**) | **W-12** (new) |
> | 3 | `PartitionError` as the fifteenth exception, with the `PartitionError`/`LeakageError` discriminating rule | **8** (High) | W-1's raises; stated once at `domain-entities.md` § 12 and `business-rules.md` R-92 |
> | 4 | The stale amendment total re-derived and annotated in place, superseded figure preserved | **32** (Medium) | § Sources, W-1's cost box, § Amendments owed, § Assumptions |
>
> **Also swept in the same pass**, under `project.md`'s rule to correct every *representation* of a
> corrected fact: two boxes asserting that `evaluation-and-comparison`'s design *"has not run"* and
> that *"`07`'s half is unowned and open"* are dated as history — **R-105 owns `07`'s half now** —
> and this unit's two carried READY residuals (R-96's mechanism framing, R-95's field label) are
> **applied rather than carried**, together with a **third field-label defect no reviewer had
> raised** (`AccessRecord.timestamp`, which does not exist). Details in `business-rules.md`.
>
> **What did NOT change.** No scientific value, grid, seed, threshold or frozen constant. **No
> approved boundary signature** — `fit_predict`, `three_seed_mean`, `climatology_fit_partition` and
> `Prediction` are still quoted from `component-methods.md` unmodified — so this unit still owes
> **0** amendments and W-11's **"Ten files"** stands. **All five `## Review` sections are preserved
> byte-for-byte**, as is every prior dated ⚠ box. No sibling unit's artifact and no
> `functional-design-questions.md` was edited.
>
> **BLK-03 remains an open exit condition and G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.** Nothing in this file — W-12
> included — authorises creating a module, and nothing in it closes BLK-03.

## Sources

- `../../../inception/application-design/component-methods.md` § `src/models` — `Prediction`, `fit_predict(model_id, *, bundle, partition, snapshot)`, `three_seed_mean(predictions, *, expected_seeds)`, `climatology_fit_partition(prediction)`, `Transform.inverse(frame)`. **Quoted, not re-invented.**
- `../../../inception/application-design/services.md` § The nine stage scripts — `06_train_and_predict.py` **reads** features and folds, **writes** predictions; § Stage entry contract; § Execution platforms, which records that a Kaggle session carries **no git working tree**.
- `../../../inception/units-generation/unit-of-work.md` § 8 — `Owns`, boundary, **BLK-03**, the six implementation notes.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2; **9 requirements, 7 with no acceptance row**; owns WS-14, WS-15, TA-12, TA-13, TA-26; supports TA-20.
- `../../../inception/requirements-analysis/requirements.md` — FR-P1-04-14, FR-P1-05-1…-6, -21, -22, each read with its `UNTESTED` note.
- `../features-and-splits/functional-design/` — **W-4a**, **W-4b**, **R-74**, **R-80**'s six-partition list, ~~§ Amendments owed at **8 across 5 units**~~ ⚠ **re-derived there to 5 across 3 on 2026-08-26** and to a live chain total of **7 across 5** here (see § Amendments owed). FU-4 = D lands W-1 below.
- `../foundation/functional-design/` — `ConfigSnapshot`, the stage entry contract, the two-tier error posture.
- `PreFlight/vision_document(3)(2)(2).md` § Decision register, lines **1206–1207** — **D-121** (exact frozen grids: ridge 6, RF 18, LSTM 16, with fixed training settings; **Approved**) and **D-122** (development seed **42**; final seeds **{1337, 2024, 7}**; the confirmatory prediction is the element-wise three-seed mean; failed runs recorded, never silently rerun. **Approved; supervisor sign-off closed 2026-08-22** by the project owner under the recorded student/supervisor authority equivalence — `CR-2026-08-22-TE-AMEND`, `GOV-2026-08-22-REM-01` Rec 4 — with the note that **no supervisor signature artifact exists and none is claimed**, and the seed values verified unchanged before closure).
  > ⚠ **Two D-number namespaces, and the first draft cited the wrong one.** D-121 and D-122 are **Vision-document** decision IDs. `evidence/DECISIONS.md` is a **separate register running D-1…D-27** and contains neither — verified by enumerating its `D-<n>` headings. The first draft of these artifacts cited `evidence/DECISIONS.md — D-121, D-122`, which resolves to nothing. **Corrected 2026-08-24** (iteration-1 finding 1 — whose framing that the two decisions *"do not exist"* is itself wrong: they exist, in the other register, and both are Approved).

---

## W-1 — The stamp match, before every scoring path

```
INPUT   bundle: FeatureBundle, partition_being_scored: Partition
OUTPUT  None — proceeds, or raises
RAISES  PartitionError, LeakageError
```

A **named function in `src/models/train.py`**, called by `06_train_and_predict.py` before every
scoring path. Against the `Partition` being scored it checks three things, each with its own raise:

| Check, in ADR-11's live vocabulary | Raises |
|---|---|
| `bundle.spec.partition_id == partition_being_scored.partition_id` | **`PartitionError`** |
| `bundle.spec.role == "score"` | **`PartitionError`** |
| `bundle.transform_id` not `None` **and** equal to that partition's own `Transform.transform_id` | **`LeakageError`** |

This is `component-methods.md:719` made executable, verbatim: *"`06`/`07` assert that a bundle
scored for partition *k* carries `spec.partition_id == k`, `spec.role == "score"`, and the
`transform_id` of *k*'s own transform."* The two-type split follows `domain-entities.md` § 12's
discriminating rule — the first two are **declared-identity** disagreements, the third **implies
information flow**.

> ⚠ **REWRITTEN 2026-08-28 — the first text checked three `FeatureBundle` fields ADR-11 retired.**
> *(`GOV-2026-08-28-FD-01` **Recommendation 3** — `IMPL-01`, Critical, veto exercised;
> owner-approved. The full derivation is in `business-rules.md` R-90's box; this is the workflow
> mirror.)*
>
> **Superseded, preserved verbatim:** the `RAISES LeakageError` line, the `INPUT bundle,
> fold_being_scored` line, and *"It checks `bundle.fold_id` equals the fold being scored,
> `bundle.purpose` equals `evaluate`, and `bundle.transform_id` is present."*
>
> `fold_id` left `FeatureBundle` when ADR-11 retired `FoldSpec` on 2026-08-23; `purpose` is a
> **`governance-guards` `AccessRecord`** field, never a `FeatureBundle` attribute; `"evaluate"` is a
> value of neither `purpose` nor `role`. **The inconsistency was internal to this unit:** W-2 below
> has used `Partition`/`partition_id` correctly since it was authored, and the only pass run after
> the retirement — `## Review — 2026-08-26 fourteenth-receipt confirming pass` — **scoped itself to
> regression against the terminal READY** and so never re-checked this text against the live
> contract. A regression-only pass cannot find a defect already present in its own baseline.

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
reusable logic in `src/` and makes scripts orchestrators, so a governed check belongs in `src/`
even when one script is its only caller.

> ⚠ **Corrected 2026-08-24 (iteration-1 finding 2).** The first draft added a second justification —
> that `features-and-splits`' `tests/test_train_only_transforms.py` *"needs a function it can call,
> not a script it must replay"*. **That misdescribed the sibling's test**, whose own R-74 declares it
> **manifest-based**, reading the emitted stamps, and explicitly **not** monkeypatch-and-replay.
> Calling this function directly is nearer the shape the sibling rejected than the one it chose. The
> sibling asserts the **refusal's effect on emitted artifacts**; the two units share **match
> semantics**, not a call edge. The `src/` placement rests on §7 alone, which is sufficient.

**Negative controls** (R-90), **four**, re-derived 2026-08-28 in ADR-11's vocabulary:
`FrameSpec(partition_id="F4", role="train")` reaching F4's score path → **`PartitionError`**; an
**untransformed** bundle (`transform_id is None`) reaching any score path → **`LeakageError`**;
`FrameSpec(partition_id="F2", role="score")` reaching F3's score path → **`PartitionError`**,
asserted by **enumeration over ordered pairs of R-80's six `partition_id` values**; and a
`role="score"` F3 frame carrying **F1's** `transform_id` → **`LeakageError`**. **Must not fire:** an
F4 `role="score"` frame carrying **F4's own** `transform_id`, reaching F4's score path → **passes**.

> ⚠ **Superseded controls, preserved verbatim** *(2026-08-28, Recommendation 3)*: *"`(fold 4, train)`
> reaching fold 4's validation scoring → **fails**; an **unstamped** frame reaching any scoring path
> → **fails**; `(fold 2, evaluate)` reaching fold 3's scoring → **fails**. **Must not fire:**
> `(fold 4, evaluate)` reaching fold 4's scoring → **passes**."* Two of the three raise types changed
> and a fourth control was added — see `business-rules.md` R-90.

> **Cost, and where it is counted.** The match function is an **intra-package** `src/models` shape
> under `component-methods.md` § Depth, so it adds **no ninth amendment**; the stamp contract is
> counted once, by `features-and-splits`, as **8 across 5 units**.
>
> ⚠ **But "the fifth unit" is two units, and this workflow discharges one** *(corrected 2026-08-24,
> iteration-1 finding 3)*. `features-and-splits` names its fifth landing site *"the pair of consuming
> scripts"* — **`06` and `07`**. `unit-of-work.md` assigns **`06` to this unit** and
> **`07_evaluate_and_report.py` to `evaluation-and-comparison`**, whose functional design has not
> run. **`07`'s half of the refusal is unowned and open**, and is carried to the gate and into
> § Assumptions & Open Questions rather than left for that unit to discover. The total is unchanged;
> what was wrong was the first draft's implication that this workflow completed the amendment.

> ⚠ **BOTH claims in the box above are now dated, 2026-08-28.**
>
> **(a) The figure.** *"**8 across 5 units**"* is **superseded**; the live chain total is
> **7 across 5 units**, re-derived term by term in `business-rules.md` § Assumptions & Open Questions
> under **Recommendation 32**. Cause: `features-and-splits` re-derived its own contribution from
> **3 to 0** on 2026-08-26 when it rebuilt onto ADR-11. **The load-bearing half of this box is
> unaffected** — the match function adds **no ninth amendment**, and this unit still owes **0**.
>
> **(b) `07`'s ownership.** *"whose functional design has not run"* and *"**`07`'s half of the
> refusal is unowned and open**"* are **superseded**. `evaluation-and-comparison`'s design has run;
> **R-105** claims `07`'s half at the object `07` receives and cites R-90 by name, and
> `statistical-inference` **R-113** limb 2 imports it. **This workflow still discharges `06` only.**
> What remains open is a **type** disagreement, not an ownership gap: R-105 limb 2 raises
> `LeakageError` where R-92 raises `PartitionError` for the same `partition_id`-mismatch condition.
> **That was corrected by the sibling in parallel and re-verified 2026-08-28**: R-105 limb 2 now
> raises `PartitionError`, *"the same exception R-92 raises for the same condition"*. **This unit
> edits no sibling artifact.**

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

> **BLK-03's seed-value limb closed 2026-08-22** (D-122 — *"Approved; supervisor sign-off closed
> 2026-08-22"*, values verified unchanged, no signature artifact claimed) and its
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

**Three** mechanisms, in `domain-entities.md` § 5 and enforced by R-95 — a count now stated
identically in all three artifacts *(iteration-1 finding 4: § 5 and R-95 both read "Two" while
enumerating three)*:

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

> **Nothing above authorises building any of it.** **G-09 is not signed** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged., and **BLK-03
> independently bars implementation** while its contract limbs stand unapproved.

## W-12 — The one-shot `DEC` write, and the receipt that must precede any metric

> **ADDED 2026-08-28** — `GOV-2026-08-28-FD-01` **Recommendation 1** (`VAL-01`, Critical, veto
> exercised), owner-approved **option 1**. Entity at `domain-entities.md` § 13; rule at
> `business-rules.md` **R-102a**. **Workflow count W-1…W-12 = 12**, derived by counting `^## W-` in
> this file. It adds **no eleventh file** to W-11's build list: the writer is
> `scripts/06_train_and_predict.py`, already there.

```
INPUT   prediction file (DEC), run_id, partition_id
OUTPUT  PredictionHashReceipt, durably flushed; sha256 -> registry column 18
RAISES  LockedTestError
```

**The sequence, and why its order is the control:**

1. `06` writes the `DEC` prediction file **once**.
2. `06` computes `sha256` over the file **as written**, and stamps `recorded_at_utc` — **at a moment
   when no metric exists**.
3. `06` **durably flushes** the receipt; its `sha256` becomes **`prediction_hash`**, TE §13.4's
   column **18** of twenty, on `06`'s own registry row, joined by `run_id`. **`foundation` R-18 owns
   that row**; this workflow owns the receipt it is populated from. **`prior_period_exposure` is not
   written here** — on a Phase 1 row its value is **`false`**, and its source is `governance-guards`'
   locked-test guard. See the deviation note below.
4. `06` **refuses to exit** if step 1 happened and steps 2–3 did not: **`LockedTestError`**, on
   `06`'s own exit path, so the failure reads *`06` aborted* rather than *`07` blocked*.
5. Only then may `07` or the bootstrap score, and each re-verifies the file against `sha256` and
   refuses on a `recorded_at_utc` that does not precede its own call
   (`evaluation-and-comparison` R-109 limb 1; `statistical-inference` R-113 limb 3).

**Rejected alternative, with the reason — this is the whole design.** *Writing the receipt inside
`07_evaluate_and_report.py`*, or inside `vector_block_bootstrap`, is the cheapest way to satisfy the
two consuming rules and is **prohibited**: both are metric callers, so the process that computes the
metric would also be the process that timestamps the receipt. *"The receipt precedes the metric"*
then holds **by construction on every run** — including a run where the prediction was regenerated
after a score was seen. The control would pass its own test and detect nothing. **Writer and reader
in different processes, with a file and a registry row between them, is the mechanism.** For the
same reason step 4 is a refusal **to exit** and not a refusal to score: a refusal to score is the
check `07` already owns, and duplicating it would leave the producer side unguarded.

**Negative controls.** A `DEC` prediction file with **no receipt** → **raises in `06`**, not in
`07`. A receipt whose `sha256` **does not match** the file as written → **raises in `06`**. A receipt
written but **not flushed** before exit → **raises in `06`**.

> **Why this workflow did not exist until now.** Derived over all **48** artifacts before this edit:
> `PredictionHashReceipt` = **0** across this unit's four files (**5** hits project-wide, all in the
> two consuming units), *"prediction hash"* = **0** here, and `prediction_hash` = **0** and
> `prior_period_exposure` = **0** **across all 48**. Three sibling passages state the write is
> **`06`'s act** — `evaluation-and-comparison` `domain-entities.md` § 5 and R-109 limb 1, and
> `statistical-inference` R-113 limb 3 — and this unit, which owns `06`, mentioned it **zero** times.
> The obligation had **two consumers and no producer**, so **G-06 could not execute**: every `DEC`
> metric entry point would raise `LockedTestError` forever.
>
> **Whose requirement, so no coverage is claimed.** **FR-P1-05-12 is `governance-guards`'**
> (`unit-of-work-story-map.md:108`; **WS-18, TA-18**). This workflow performs the `06`-side act of a
> sibling's requirement — a **produced** cross-unit obligation, the mirror of W-10's two **consumed**
> ones — and **claims no WS-18 or TA-18 coverage**. § Requirement-to-workflow map below is unchanged:
> **9 requirements, 7 with no §16/§19 acceptance row.**
>
> ⚠ **DEVIATION FROM THE APPROVED REMEDIATION TEXT — `prior_period_exposure` is `false` here, and
> this workflow writes no `true`.** The remediation said *"`prior_period_exposure = true`"*.
> `foundation`'s **W-6 step 5**, amended 2026-08-28 on the same report, is a hard refusal:
> *"**Refuse `prior_period_exposure = true` on a Phase 1 row** … Phase 1 *is* the first December
> exposure; `true` belongs to the Phase 2 replication (TE §7.0B)."* TE §7.0B's own sentence
> (`:372`) makes the flag a **Phase 2** predicate — *"The Phase 2 December run is a fixed-protocol
> replication **because Phase 1 has already exposed December**"* — and **this unit is Phase 1**
> (NFR-PHASE-01). `true` here would be a false statement about the run. `foundation` R-18 also
> settles the attribution: the field's **source is `governance-guards`' locked-test guard**, its
> **destination is `foundation`'s registry row**, and **this unit is neither**, so this workflow
> claims no check over it. **Raised for the owner** at `business-rules.md` R-102a: if
> Recommendation 1 meant a different predicate, it needs a different field name.
>
> **The registry side has landed and interlocks with this workflow.** `foundation` **R-18** carries
> the twenty columns with `prediction_hash` at **18**, names `scripts/06_train_and_predict.py` as the
> receipt's writer with these exact five fields and the durable flush, and its **W-6 step 4 refuses a
> `prediction_hash` presented by the metric-computing process** — the destination-side complement to
> step 4 above. Neither half suffices alone: this workflow stops the receipt being *created* in a
> metric process, R-18 stops it being *recorded* from one.
>
> **Nothing here authorises writing it.** **G-09 is not signed** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged., **BLK-03 independently bars
> implementation**, and the `DEC` write is additionally barred until **G-05 is signed** by
> `features-and-splits` **R-82** and `governance-guards`' access chokepoint.

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
| ~~`features-and-splits` § Amendments owed~~ | ~~**8**, across **5** units~~ ⚠ **SUPERSEDED 2026-08-28** → the **live chain** total is **7 across 5 units** | Superseded basis, preserved: *"Derived there, after its own FU-4 = D re-derivation from 7-across-4. **Not restated** — a restated count drifts, which is the failure this row exists to avoid."* The warning was right and the mechanism it warned about is exactly what happened: **`features-and-splits` re-derived its own contribution from 3 to 0 on 2026-08-26** when it rebuilt onto ADR-11, moving the base to **5 across 3**. |
| **This unit** | **0** | W-1's match function and **W-12's `PredictionHashReceipt`** are both **intra-package** `src/models` shapes under `component-methods.md` § Depth. `domain-entities.md` § 3's contract **describes** the approved `three_seed_mean` and `Prediction` without changing either signature; § 13 adds a shape without touching one. § 6's Option D — stamping fitted partitions onto `Prediction` — was **declined precisely to avoid a ninth**. |
| | ~~**8 across 5 units**~~ → **7 across 5 units** | ~~8 + 0~~ → `5 + 0 + 1 + 1 + 0 + 0 + 0 = 7` |

> ⚠ **RE-DERIVED 2026-08-28, not decremented.** *(`GOV-2026-08-28-FD-01` **Recommendation 32** —
> `CHAIR-07`, Medium; owner-approved **option 1**, annotate in place, per
> `governance/CHANGE_RECORD_PROCEDURE.md` and `project.md` dp-1.)* **The full term-by-term
> derivation, with the source line for each unit, is printed once** in `business-rules.md`
> § Assumptions & Open Questions and is **deliberately not restated here** — restating it is the
> drift this table's own basis column warns against. In summary: `external-products` R-55 **5**
> (across `acquisition`, `inventory-and-registry`, `external-products`), `features-and-splits` **0**,
> `evaluation-and-comparison` **+1** (R-103), `statistical-inference` **+1** (R-118),
> `regimes-diagnostics-reporting` **0**, `fixtures-and-reproducibility` **0**, **this unit 0** →
> **7 across 5 units**.
>
> ⚠ **A correction to the remediation brief.** The brief gave the chain as ending **"8 across 6"** at
> `fixtures-and-reproducibility`. That unit's **live** total is **7 across 5** (its
> `business-rules.md:602`, `:612`); its four *"8 across 6"* mentions are one **explicitly labelled
> conditional** — *"+1, to 8 across 6, **at that ruling** — counted **then, not now**"* — contingent
> on an **unmade** owner ruling on its R-133 manifest-loader home. The chain is therefore recorded as
> terminating at **7 across 5**, with a conditional **+1 → 8 across 6** pending that ruling.
>
> **This unit's own contribution was never in doubt and is unchanged at 0.** What was stale was the
> **quoted base**.

**`features-and-splits` counted its fifth landing site as *"the pair of consuming scripts"* — `06`
and `07`. That is two units, not one.** `unit-of-work.md` assigns **`06` to this unit** and
**`07_evaluate_and_report.py` to `evaluation-and-comparison`**, whose functional design has not
run. **This unit discharges `06`'s half; `07`'s half is unowned and open** — see W-1 and
§ Assumptions & Open Questions. **The total is unaffected either way**: the stamp contract is
counted once, by `features-and-splits`, and nothing here adds to it.

> ⚠ **Corrected 2026-08-24, iteration-2 finding 1 (Critical).** This paragraph previously read
> *"**This unit is the fifth**, as `features-and-splits` counted it: `06` and `07` are where the
> stamp is refused. Nothing here adds to the total."* — reasserting the pre-correction claim
> **twenty lines below** the W-1 fix that had already corrected it, and doing so **inside
> § Amendments owed**, which is the section a gate reader checks for exactly this. The
> iteration-1 fix reached W-1's body and all three § Assumptions lists and **stopped one
> representation short**. That is the failure mode `project.md` § Way of Working already records
> twice: *"sweep every REPRESENTATION of a corrected fact, not every instance of the entity that
> carries it."* Found by the reviewer, not by the sweep that was supposed to catch it.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence, so `business-rules.md` runs **R-90…R-102**. If per-unit numbering was intended, say so at the gate and the artifacts restart.
- **[assumption]** The **story map governs** where it and `unit-of-work.md` § 8 disagree. Neither is edited by this stage.
- **[assumption]** `src/models/*` shapes beyond the named boundary calls are **intra-package** and this stage's to specify. **W-1's match function is one of them**, and so is **W-12's `PredictionHashReceipt`** — no amendment owed by this unit. ⚠ ~~total stays **8 across 5**~~ **SUPERSEDED 2026-08-28**: the live chain total is **7 across 5 units** (§ Amendments owed; `business-rules.md` § Assumptions carries the term-by-term derivation). **This unit's 0 is unchanged.**
- **[assumption]** Workflows run **W-1…W-12** — **12**, derived by counting `^## W-` before asserting. **W-12 added 2026-08-28** (Recommendation 1). The `## Review` sections below recorded **11** at their own dates and remain correct as of those dates; they are preserved unedited.
- **CLOSED 2026-08-28 — `PartitionError` is the fifteenth project exception; `foundation` R-01's amendment HAS LANDED** (Recommendation 8, owner-ruled option 1; the discriminating rule is at `business-rules.md` R-92 and `domain-entities.md` § 12). Re-read directly at the close of this pass: R-01 names **fifteen**, adds `PartitionError`, restates its count as **derived**, and cites **this unit's § 12 as the authority for the fifteenth entry**. *(Mid-pass it read "All fourteen"; the draft's "in flight" wording is superseded and recorded.)* Derived before this edit: **10 of 12 units**, **71** occurrences across **48** artifacts, **23** here.
- **CLOSED 2026-08-28 — the R-105 / R-92 disagreement is resolved by the sibling.** R-105 limb 2 now raises **`PartitionError`**, matching R-92, with limb 1 keeping `LeakageError` for an absent stamp and running first. `statistical-inference` R-113 limb 2 inherits the fix. **This unit edited no sibling artifact.**
- **Open — W-12 discharges FR-P1-05-12, which belongs to `governance-guards`** (`unit-of-work-story-map.md:108`; WS-18, TA-18). This unit owns the script, not the requirement. **No WS-18/TA-18 coverage claimed**; the 9-requirement, 7-without-a-row tally is unchanged.
- ⚠ **DEVIATION FROM THE APPROVED REMEDIATION TEXT — the one item needing an owner ruling.** The remediation said `prior_period_exposure = true`; **W-12 writes no `true`**, because `foundation` **W-6 step 5** refuses `true` on a **Phase 1** row and TE §7.0B (`:372`) makes the flag a **Phase 2** predicate. R-18 also settles the attribution — source `governance-guards`, destination `foundation`'s row, **this unit neither** — so W-12 claims no check over it. Full reasoning at `business-rules.md` R-102a's deviation box. **If a different predicate was intended, it needs a different field name; nothing is assumed.**
- **CLOSED 2026-08-28 — R-102a/W-12's registry side has landed and interlocks.** `foundation` **R-18** carries TE §13.4's twenty columns with `prediction_hash` at **18**, names `scripts/06_train_and_predict.py` as the receipt writer with W-12's exact five fields and durable flush, and **W-6 step 4 refuses a `prediction_hash` presented by the metric-computing process**. The *"in flight"* wording in the draft of this list is superseded.
- **Resolved 2026-08-28 — the two residuals that rode this unit's terminal READY are applied, not carried.** `business-rules.md` R-96's `PartitionError` mechanism is restated as `features-and-splits` **R-80**'s upstream six-value type-closure (the local *"outside that enumeration"* check it claimed **does not exist** in this unit), and R-95 mechanism 2's field pair is corrected to `criterion_hash` / `criterion_used_hash`. **A third defect, previously unraised by any reviewer, was found in the same sweep and fixed:** R-95 mechanism 3 read `AccessRecord.timestamp`, and `AccessRecord` has **seven** fields with no `timestamp` (`component-methods.md:266–273`) — the retrieval field is `retrieved_at_utc`; its `purpose`-absence fallback rested on a false premise and is withdrawn.
- **Open — BLK-03's contract limbs are an EXIT condition** on this unit and on `evaluation-and-comparison`, `statistical-inference` and `regimes-diagnostics-reporting`. **W-3 authors the contract; approving it is the human's, at the gate.**
- **Open — BLK-04 ↓ and BLK-09 ↓** inherited from `features-and-splits`; its 2026-08-24 answers supplied mechanism, **neither is closed**.
- **Open — W-1's match function is a cross-unit contract surface**, asserted against by `features-and-splits`' `tests/test_train_only_transforms.py`. Neither unit owns it alone.
- **Open — 7 of 9 requirements have no acceptance row.** Four name their own candidate TA row via **Vision §15.2**; **none is added here**.
- **Open — whether TA-11 reaches a model fit is unverified upstream** (W-9). No reading adopted.
- **Closed, corrected 2026-08-24 — D-122's supervisor sign-off is NOT outstanding.** The first draft carried *"Approved — supervisor sign-off pending"*, which is the status of **D-126** and **D-128**, not D-122. The Vision decision register (line 1207) reads **"Approved; supervisor sign-off closed 2026-08-22"** by the project owner under the recorded student/supervisor authority equivalence (`CR-2026-08-22-TE-AMEND`; `GOV-2026-08-22-REM-01` Rec 4), noting that **no supervisor signature artifact exists and none is claimed** and that the seed values were verified unchanged before closure. `unit-of-work.md` § 8 already recorded the closure. **Found while verifying iteration-1 finding 1 against the source register; the reviewer did not raise it.**
- **Open — FR-P1-05-4's residual** (W-5): a December figure carried in a human's head is unreachable by any mechanism. Narrowed by the audit-access precondition, **not eliminated**.
- **G-09 is not signed** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged., and **BLK-03 independently bars implementation.** No workflow here authorises creating any of W-11's ten files.
- ~~**Open — `07`'s half of the eighth amendment is UNOWNED.**~~ **CLOSED 2026-08-28.** *(Superseded text preserved:* "FU-4 = D names **`06` and `07`**; `unit-of-work.md` assigns `07_evaluate_and_report.py` to **`evaluation-and-comparison`**, whose functional design has not run. This unit discharges `06` only. Raised at the gate so it is not discovered later *(iteration-1 finding 3)*." *)* That unit's design has run and its **R-105** claims `07`'s half, citing R-90 by name. **This unit still discharges `06` only** — that half stands. What survives is the **type** disagreement recorded above.
- **Open — `requirements.md` FR-P1-05-2 carries TWO superseded clauses on one line, both reported and neither edited.** (a) It attributes bootstrap seed **20221201** to D-122, a reading `unit-of-work.md` § 8 records as corrected 2026-08-22 (`GOV-2026-08-22-UG-02` Rec 11) — the seed is frozen separately by **TE §13.6 / TC-19** (Q-27). (b) It states *"Vision §14.2 marks it 'Approved — supervisor sign-off pending'… still owes a signature at G-05"*, superseded by the same Vision-register closure at line 1207 that these artifacts cite correctly elsewhere — **"Approved; supervisor sign-off closed 2026-08-22"**. This unit follows the **corrected** reading of both. `requirements.md` is an approved upstream artifact and `CHANGE_RECORD_PROCEDURE.md` bars editing one absent owner approval for annotate-in-place, so both are **raised at the gate**. *(Clause (a) was iteration-1 finding 5; clause (b) is iteration-2 finding 2 — flagging one clause of a line and missing its neighbour is the same one-representation-short failure as iteration-2 finding 1, and clause (b) is where this author's own D-122 error originated.)*
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

## Review

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-24T13:58:07Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | All three artifacts' Sources sections; `business-logic-model.md` L15–17, 28, 162; `business-rules.md` L14–16, 26, 99, 157; `domain-entities.md` L13–14, 27, 99, 236, 241 | **D-121 and D-122 do not exist in `evidence/DECISIONS.md`.** All three artifacts cite D-121 as the frozen source for the grid cardinalities (ridge 6, RF 18, LSTM 16) and D-122 as the frozen source for the seed set ({1337, 2024, 7}, dev seed 42), repeatedly asserting "no workflow here decides a scientific value... frozen upstream." I grepped `evidence/DECISIONS.md` (1466 lines) for every `D-<number>` occurrence: the file runs D-1 through D-27 only (plus an unrelated `D-144` that is a *Technical Environment* section/gate cross-reference, not a decision-log entry). Neither `D-121` nor even the bare substrings `121`/`122` occur anywhere in the file. `team.md` designates this file as the authoritative decision ledger — "a decision is not real until it has a D-number" — so the artifacts' central premise (nothing here decides a scientific value because D-121/D-122 already froze it) is currently unverifiable against the project's own single source of truth. This is inherited from `unit-of-work.md` and `requirements.md`, which already assert D-122 as "closed 2026-08-22," but this stage repeats the citation as settled without flagging that the ledger itself does not show it — contrary to `project.md`'s own mandated practice, "ALWAYS verify a fact independently before handing it to another reviewer as established input." | Before this stage exits, confirm whether D-121/D-122 exist under different numbers or in an un-synced ledger update, and either correct every citation or open a blocking item at the gate. Do not let G-05/G-09 rely on an unverifiable freeze citation. |
| 2 | Critical | `business-logic-model.md` L47–49, 56–57, 291; `business-rules.md` L42–43, 58; `domain-entities.md` L348–350 | **Mischaracterizes the sibling's own test design.** All three artifacts state that `features-and-splits`' `tests/test_train_only_transforms.py` "needs a function it can **call**, not a script it must replay" and "calls it directly rather than replaying a script" — used as part of the rationale for building W-1 as a named, callable function. But `features-and-splits/functional-design/business-rules.md` (line 161–164, in the carve-out I was granted) states the opposite in its own words: *"The test, with its kind declared — `tests/test_train_only_transforms.py` is **manifest-based**: it reads the emitted stamps and asserts that refusal. **Not** static analysis...; **not** monkeypatch-and-replay, which verifies a replay rather than what a real run emits."* Monkeypatch-and-replay is exactly what "calling the function directly" in a test would be — the sibling explicitly rules it out. The reviewed unit's designated "cross-unit contract surface" is therefore based on a factually wrong reading of what the consuming test actually does. | Re-read `features-and-splits`' R-74/FU-4=D text before finalizing W-1's placement rationale. If the sibling's test is genuinely manifest-based (reads emitted artifacts/logs, not a direct function call), restate the justification for a named `src/models/train.py` function accordingly, and drop the "the sibling's test calls it directly" claim from all three files and from the Assumptions & Open Questions entries that repeat it. |
| 3 | Major | `business-logic-model.md` L44–49, 64–68, 280–282; `business-rules.md` L54–58; `domain-entities.md` L326–350 | **"The fifth unit" silently conflates two different owning units, and the other half is left unflagged.** `features-and-splits`' own § Amendments owed states: *"The fifth unit is the pair of consuming scripts [06 and 07], whose own units have not designed yet."* But `unit-of-work.md` § 8 Owns assigns `06_train_and_predict.py` to `models-and-baselines` and § 9 Owns assigns `07_evaluate_and_report.py` to `evaluation-and-comparison` — two distinct units. This unit's W-1/R-90 designs only `06`'s refusal. Every one of the three artifacts closes with "This unit is the fifth... Nothing here adds to the total," reading as though the slot is now fully discharged, but `07`'s half of FU-4=D remains completely undesigned, owned by a unit that has not yet reached 3.1, and there is no entry anywhere in any of the three Assumptions & Open Questions sections flagging that gap. | Add an explicit Open Question stating that `07`'s half of FU-4=D's refusal is owed by `evaluation-and-comparison`, is not designed here, and that the "8 across 5 units" total may need revisiting once that unit's own 3.1 design lands (it may turn out to be 8 across 6, or a ninth landing site, depending on how `07` implements it). |
| 4 | Major | `business-rules.md` L129 vs L131–140; `domain-entities.md` L194 vs L186–204; `business-logic-model.md` L145 | **Unswept stale count: "Two mechanisms" vs. three enumerated items, and disagreement between artifacts.** `business-rules.md` R-95 opens with "**Two mechanisms**, one per reachable channel *(Q3 = D)*:" then lists three parallel numbered items (`partitions_read`, the criterion-hash comparison, and `audit_access_since_declaration`) and three matching negative controls. `domain-entities.md` § 5 repeats "**Two mechanisms**, because one channel each" immediately above a `TuningRecord` table carrying the same three fields. `business-logic-model.md` W-5, covering identical content, instead says "**Three mechanisms**." Two of the three reviewed artifacts assert a count of two for content that is, by their own enumeration and by the third artifact's count, three. This is exactly the class of defect `project.md` records this project has repeatedly made ("derive a count programmatically... never carry a count from adjacent prose"). | Change "Two mechanisms" to "Three mechanisms" in `business-rules.md` R-95 and `domain-entities.md` § 5 (or, if `audit_access_since_declaration` is deliberately not counted as a "mechanism" catching a channel, say so explicitly and explain why it still gets a negative control of its own). |
| 5 | Major | `domain-entities.md` L99–101; `business-rules.md` L74–79; cf. `requirements.md` FR-P1-05-2 | **A contradiction between this unit's own cited Sources is followed silently rather than flagged.** `requirements.md`'s FR-P1-05-2 pass/fail criterion states the seed values are "asserted against the frozen set: development seed **42**, final seeds **{1337, 2024, 7}**, **bootstrap seed 20221201** (Vision §8.6, D-122; TE §13.5)" — i.e. bootstrap seed 20221201 is part of D-122. `unit-of-work.md` § 8's BLK-03 entry instead records that this attribution was **corrected** 2026-08-22 under `GOV-2026-08-22-UG-02` Rec 11: "The bootstrap seed 20221201 is frozen separately by TE §13.6/TC-19 (Q-27) and is **not** part of D-122's item set." The reviewed unit follows the corrected reading (correctly) but never notes that one of its own listed Sources — `requirements.md` — still carries the superseded attribution, leaving a live contradiction between two upstream sources this unit cites side by side. | Add a one-line note (as the artifacts already do for other superseded readings) that `requirements.md`'s FR-P1-05-2 text predates the `GOV-2026-08-22-UG-02` correction and should not be read as re-including the bootstrap seed in D-122's item set. |
| 6 | Minor | `domain-entities.md` L192, L198–204; `business-rules.md` L135–140 | **`audit_access_since_declaration`'s query mechanism is asserted as an outcome, not specified as a mechanism.** The field is described as "read from `governance-guards` R-25's durable access log," but no accessible artifact states the log's record schema or how a specific tuning run's `criterion_declared_at` is correlated against a logged December-audit-access event (by run ID? by timestamp range? by a shared declaration ID?). `FR-P1-05-12` (requirements.md) does establish that all December accesses, including non-execution reads, are logged before-the-read, which partially substantiates that the data exists — but the join/query logic itself is not stated. | State explicitly what field of R-25's log is compared against what field of `TuningRecord` (e.g., a timestamp-range comparison against `criterion_declared_at`), so an implementer does not have to invent the join. |

### Validation tool results

No stage-specified validation tooling was listed for this stage in the dispatch; none was run. All findings above were derived by direct cross-reading of the three artifacts under review against the passed contracts (`unit-of-work.md`, `requirements.md`, `component-methods.md`, `services.md`), the granted sibling carve-out (`features-and-splits/functional-design/business-rules.md`, `business-logic-model.md`), and `evidence/DECISIONS.md`, using Grep/Read rather than an automated checker.

### Counts and enumerations re-derived independently

| Claim | Derivation | Result |
|---|---|---|
| "9 requirements, 7 with no acceptance row" | Counted rows in the Requirement-to-workflow map (L255–265): 9 requirement rows; rows flagged "⚠ NO ACCEPTANCE ROW": FR-P1-04-14, FR-P1-05-3, -4, -5, -6, -21, -22 = 7; remainder FR-P1-05-1, FR-P1-05-2 = 2. 7+2=9. Cross-checked against `unit-of-work.md` §8 ("Requirements carried (9)... Bold = no test row (7 of 9 here)"). | **Confirmed correct.** |
| "Owns WS-14, WS-15, TA-12, TA-13, TA-26 (5); supports TA-20" | Listed 5 distinct IDs in the map's Acceptance column; cross-checked against `unit-of-work.md` §8 "Acceptance rows (5)" — same 5 IDs; TA-20 confirmed owned by `regimes-diagnostics-reporting` (§11) with this unit merely producing the three controls it reports. | **Confirmed correct.** |
| "Five named, four reachable" ablations | Counted TE §7.2 registry as quoted in `requirements.md` FR-P1-05-6: ABL-NODOY, ABL-DIFF, ABL-NOSW, ABL-HIST48, ABL-ZENITH = 5; ABL-ZENITH deferred to Phase 2 = 4 reachable. | **Confirmed correct.** |
| Grid cardinalities "ridge 6, RF 18, LSTM 16" | Matched verbatim against `requirements.md` FR-P1-05-5. | **Confirmed correct as a restatement — but see Finding 1: its cited source D-121 does not exist in `evidence/DECISIONS.md`.** |
| "Seven fixed LSTM settings" | Counted the list in `requirements.md` FR-P1-05-5: (1) dropout 0.2 (2) Adam (3) MSE loss (4) max 100 epochs (5) patience 10 (6) min improvement 1e-4 TECU (7) best-checkpoint restoration = 7. | **Confirmed correct as a restatement — same D-121/122 caveat as above for the seed set.** |
| "Amendments owed: 8 across 5 units, 0 added here" | Re-summed `features-and-splits`' own table: 5 (external-products R-55) + 1 (R-74) + 1 (R-81) + 1 (pairing control/W-4a) = 8. Arithmetic confirmed. | **Arithmetic correct, but the "5 units" figure is suspect — see Finding 3: the sibling's own text names the fifth slot as "the pair of consuming scripts," which are two different owning units (`models-and-baselines` for `06`, `evaluation-and-comparison` for `07`), not one.** |
| FR-P1-05-4's mechanism count | `business-rules.md` R-95 and `domain-entities.md` §5 each say "Two mechanisms" while enumerating three items and three negative controls; `business-logic-model.md` W-5 says "Three mechanisms" for the same content. | **Contradiction found — see Finding 4.** |
| D-121 / D-122 existence in `evidence/DECISIONS.md` | Grepped the full 1466-line file for `D-<number>` and for bare `121`/`122`. Highest sequential decision is D-27; a separate `D-144` is a cross-reference to a different document's section, not a decision-log entry. Zero occurrences of D-121 or D-122. | **Not found — see Finding 1.** |

### Failed refutation attempts

- Attempted to find a drifted or re-invented signature for `Prediction`, `fit_predict`, `three_seed_mean`, or `climatology_fit_partition` against `component-methods.md` — all four are quoted verbatim, including the `partition_id`/`transform_id` fields added under ADR-11. Held.
- Attempted to find a circular dependency in the declared unit DAG — `models-and-baselines` depends only on `features-and-splits`, matching `unit-of-work.md` §8 exactly; no cycle in the declared graph itself (the real cross-unit problem found is Finding 2/3, not a DAG cycle).
- Attempted to show the `R-76a`/static-check citation for the horizon and grid checks was fabricated — confirmed `features-and-splits/functional-design/business-rules.md` line 294–329 does carry an R-76a "static check over the source tree" of the claimed shape.
- Attempted to show the G-05 grid-hash mechanism (W-6/R-96) was an outcome-only remedy rather than a specified mechanism — held up: it correctly separates "hash catches post-freeze drift" from "individually asserted cardinalities/settings catch wrong-content-at-freeze," which is a coherent two-part mechanism, not a vague promise.
- Attempted to show FR-P1-04-14's "ties under 1%, refit without changing any hyperparameter" was invented — matches `requirements.md` FR-P1-04-14 verbatim.
- Attempted to show the "no reading adopted on TA-11" posture was an unsupported dodge — `requirements.md` FR-P1-05-21 itself states the same unverified-upstream posture in the same words, so this is a faithful restatement, not a new gap invented here.
- Attempted to show the module-boundary rule (must not import `src/external/iri.py`, `gim.py`, or `src/evaluation`) was inconsistent with the approved boundary — matches `unit-of-work.md` §8 Boundary text exactly.

### Summary

The mechanism-level design in these three artifacts is largely careful and internally disciplined — signatures are quoted rather than reinvented, most counts check out against their sources, and several genuinely good practices (negative controls paired with every hard rule, explicit "no reading adopted" postures, explicit unowned-obligation framing) are followed correctly in most places. But two Critical defects and three further Major defects survive scrutiny: the artifacts' foundational claim that nothing here decides a scientific value rests on two decision IDs (D-121, D-122) that do not exist in the project's own authoritative decision ledger; the stated rationale for W-1's placement mischaracterizes the sibling unit's own test design (asserting a direct function call where the sibling explicitly states a manifest-based check and rules out exactly that pattern); the "fifth unit" amendment-accounting silently treats a two-unit obligation (`06` in this unit, `07` in `evaluation-and-comparison`) as fully discharged by this unit alone, with no open item naming the remainder; and a stale mechanism count ("two" vs. three enumerated items) is left unswept in two of the three files while the third correctly says three. None of these is cosmetic: the D-121/D-122 gap undermines the entire "restated, never chosen" premise this design leans on for gate readiness, and the sibling-test mischaracterization undermines the stated justification for where the leakage-refusal logic lives.

**Verdict: NOT-READY.**

## Review — Iteration 2

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-24T14:11:34Z
**Iteration:** 2

### Status of the iteration-1 findings

| # | Iteration-1 severity | Disposition claimed | My independent basis | My verdict on disposition |
|---|---|---|---|---|
| 1 | Critical | Disputed/corrected — D-121/D-122 exist in the Vision register, not `evidence/DECISIONS.md` | Read `PreFlight/vision_document(3)(2)(2).md` lines 1195–1216 directly: line 1206 is D-121 ("Exact frozen grids: ridge 6, RF 18, LSTM 16... Approved"), line 1207 is D-122 (seeds, "Approved; supervisor sign-off closed 2026-08-22..."), verbatim. Grepped `evidence/DECISIONS.md` for `D-[0-9]+`: runs D-1…D-27 plus D-144/D-1-addendum, zero occurrences of 121 or 122. Both claims check out. | **Correctly disposed.** |
| 2 | Critical | Accepted — sibling test is manifest-based, not called directly | Read `features-and-splits/functional-design/business-rules.md` lines 160–165 directly (within the granted carve-out): confirms verbatim "manifest-based: it reads the emitted stamps... **Not**... monkeypatch-and-replay". The corrected text in all three artifacts matches this exactly. | **Correctly disposed.** |
| 3 | Major | Accepted — `07`'s half is unowned and open; Open Question added | Read `unit-of-work.md` §8/§9 directly: `06_train_and_predict.py` → `models-and-baselines`, `07_evaluate_and_report.py` → `evaluation-and-comparison`, two distinct units, confirmed. The W-1/R-90/§11 body text and the Assumptions & Open Questions entries in all three files now state this correctly. **However**, `business-logic-model.md` line 298 ("This unit is the fifth... `06` and `07` are where the stamp is refused. Nothing here adds to the total.") was left unedited and still asserts the pre-correction framing this finding required fixing. | **Partially disposed — a surviving contradiction found; new finding below.** |
| 4 | Major | Accepted — "Two" → "Three" in `business-rules.md` R-95 and `domain-entities.md` §5 | Grepped all three files for "Two mechanism": zero hits outside the Review section's own historical quotation of the defect. All three now read "Three mechanisms" for this content. The only other "Two" in the files is R-101's unrelated "Two mechanical comparisons" (selection-criterion hash pair + refit-hyperparameter equality), which is a different count and correctly stated. | **Correctly disposed, no regression.** |
| 5 | Major | Accepted as report-not-edit — Open Question added noting `requirements.md` FR-P1-05-2 still misattributes the bootstrap seed to D-122 | Read `requirements.md` line 395 directly: confirms it still lists "bootstrap seed **20221201**" as part of D-122's asserted values. The note in `domain-entities.md` §3 limb 1 and the matching Open Questions in all three files accurately describe this and correctly say the corrected reading (TE §13.6/TC-19) is followed instead. **But the same `requirements.md` line 395 also asserts a second, unflagged stale fact**: "Vision §14.2 marks it 'Approved — supervisor sign-off pending'... still owes a signature at G-05" — directly contradicted by Vision register line 1207 ("closed 2026-08-22"), which these same three artifacts elsewhere rely on and correctly restate. No Open Question in any of the three files names this second contradiction against the same cited Source. | **Partially disposed — the fix was applied to one half of the stale row and not the other; new finding below.** |
| 6 | Minor | Accepted — R-95 mechanism 3's join stated explicitly (`AccessRecord.timestamp` vs `TuningRecord.criterion_declared_at` and "TuningRecord's own run timestamp") | Read `domain-entities.md` §5's `TuningRecord` attribute table directly: it defines `run_id`, `partitions_read`, `criterion_declared_at`, `criterion_hash`, `criterion_used_hash`, `audit_access_since_declaration` — no field named or described as "the run's own timestamp" exists anywhere in the entity. The join as stated in `business-rules.md` R-95 and restated in `business-logic-model.md` W-5 references an attribute the entity model never defines. | **Partially disposed — the join is now stated in prose but references an undeclared field; new finding below.** |
| Un-raised (D-122 sign-off) | — | Corrected — "Approved — supervisor sign-off pending" replaced with "closed 2026-08-22" in all three artifacts' own prose | Verified against Vision register line 1207 directly: matches verbatim, including "no supervisor signature artifact exists and none is claimed" and the CR/GOV citations. D-126 (line 1214) and D-128 (line 1216) do read "Approved — supervisor sign-off pending", confirming the artifacts' claim about whose status that phrase actually belongs to. | **Correctly disposed — and correctly attributed as a defect the iteration-1 reviewer did not catch.** |

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | `business-logic-model.md` L298–299, contradicting L76–82 and the Assumptions & Open Questions entry at L314 (same file) | **The "Amendments owed" section — the specific section a gate reviewer checks for amendment-completeness — reverts to the pre-correction claim iteration-1 finding 3 required fixed.** Immediately after the corrected table (L288–296, which correctly shows "This unit | 0" and "8 across 5 units | 8 + 0"), the closing sentence reads: *"**This unit is the fifth**, as `features-and-splits` counted it: `06` and `07` are where the stamp is refused. Nothing here adds to the total."* This directly contradicts the correction 20 lines earlier in the same file (L76–82): *"'the fifth unit' is two units, and this workflow discharges one... `07`'s half of the refusal is unowned and open."* A reader who reads only the Amendments-owed section — which is exactly what a gate approver checking "is the amendment accounting closed" would read — is told this single unit fully constitutes the fifth landing site and that "nothing here adds to the total," with no cross-reference to the correction or to the Open Question three sections later. The two statements cannot both be true: either this unit is "the fifth" (implying `07`'s half is covered here), or `07`'s half is unowned and open (implying this unit is only half of a two-unit fifth slot). This is the exact defect class `project.md`'s own Corrections log twice as this project's recurring failure mode ("sweep every REPRESENTATION of a corrected fact, not every instance of the entity that carries it") — the correction reached the W-1 narrative and the Open Questions list but not the Amendments-owed closing sentence, which is arguably the most load-bearing of the three for a gate decision. | Rewrite L298–299 to read consistently with L76–82: e.g. "This unit discharges `06`'s half of the fifth landing site; `07`'s half remains open and unowned by any 3.1 design. Nothing designed here adds a new amendment to the total, but the total's completeness depends on `evaluation-and-comparison`'s own 3.1 design for `07`." Do this in `business-logic-model.md` specifically — `business-rules.md` and `domain-entities.md` do not carry this contradiction. |
| 2 | Major | `requirements.md` L395 (cited as a Source by all three artifacts), unflagged in `business-logic-model.md` L311, `business-rules.md` L334, `domain-entities.md` L414 | **A second stale claim on the same cited-Source row that iteration-1 finding 5 already flagged for a different clause is left unflagged.** `requirements.md` FR-P1-05-2's acceptance criterion states, verbatim: *"D-122's own status is carried, not hidden: Vision §14.2 marks it 'Approved — supervisor sign-off pending,' so the seed set is frozen for implementation and still owes a signature at G-05."* This is the exact same superseded status ("Approved — supervisor sign-off pending") that all three artifacts under review correctly identify and correct **in their own prose** (Assumptions & Open Questions: *"D-122's supervisor sign-off is NOT outstanding... The first draft carried 'Approved — supervisor sign-off pending'..."*), citing Vision register line 1207's actual text ("closed 2026-08-22"). But none of the three artifacts' Open Questions name `requirements.md` itself as still carrying this exact superseded claim, even though `requirements.md` is one of their own listed Sources and even though the immediately adjacent clause on the same row (the bootstrap-seed misattribution) *is* flagged this way per finding 5's fix. The sweep that caught one stale clause on this row missed the other stale clause on the same row. | Add a second Open Question (or extend the existing bootstrap-seed one) stating that `requirements.md` FR-P1-05-2 also still asserts D-122's sign-off as "pending," which is superseded by the Vision register's 2026-08-22 closure and by `unit-of-work.md` §8's own recorded closure; this unit follows the corrected reading and reports rather than edits the upstream artifact, exactly as done for the bootstrap-seed clause. |
| 3 | Minor | `business-rules.md` L160–165; `domain-entities.md` §5 table, L194–201; restated in `business-logic-model.md` W-5 | **The finding-6 fix specifies a join against a field the entity model never declares.** R-95 mechanism 3's stated correlation is `AccessRecord.timestamp > TuningRecord.criterion_declared_at` **and** `AccessRecord.timestamp < TuningRecord's own run timestamp`. `domain-entities.md` §5's `TuningRecord` table lists exactly six attributes — `run_id`, `partitions_read`, `criterion_declared_at`, `criterion_hash`, `criterion_used_hash`, `audit_access_since_declaration` — none of which is "the run's own timestamp" or any synonym (`completed_at`, `run_timestamp`, etc.). An implementer following the join as literally stated has no attribute to bind the upper bound of the comparison to, and would have to invent one — precisely what finding 6 was raised to prevent ("state explicitly what field... is compared against what field... implementer does not have to invent the join"). The fix narrowed the gap (the lower bound and the purpose-based fallback are now genuinely well specified) but did not close it fully. | Add a `run_timestamp` (or equivalent) attribute to `domain-entities.md` §5's `TuningRecord` table, or restate the upper bound in terms of an attribute that already exists (e.g., `criterion_used_hash`'s associated timestamp, if one is implied elsewhere) so the join is fully closed against the declared schema. |

### Validation tool results

No stage-specified validation tooling was listed for this stage's dispatch; none was run (unchanged from iteration 1). All findings above were derived by direct Read/Grep cross-reading of the three artifacts under review against: `PreFlight/vision_document(3)(2)(2).md` (lines 1195–1216, read directly), `evidence/DECISIONS.md` (grepped for every `D-[0-9]+` occurrence), `requirements.md` (FR-P1-05-2 row read directly), `unit-of-work.md` §8/§9 (read directly), `unit-of-work-story-map.md` (grepped for every requirement/acceptance-row ID named in the three artifacts), and the granted sibling carve-out `features-and-splits/functional-design/business-rules.md` (R-74 and § Amendments owed read directly).

### Counts and enumerations re-derived independently

| Claim | Derivation | Result |
|---|---|---|
| D-121/D-122 exist, Vision-register lines 1206–1207, both Approved | Read the two lines directly | **Confirmed exactly as the artifacts state, including the D-122 closure wording.** |
| `evidence/DECISIONS.md` runs D-1…D-27, no D-121/D-122 | Grepped every `D-[0-9]+` occurrence in the file and sorted | **Confirmed** — highest is D-27; D-144/D-1-addendum are the only outliers and are not decision-log entries in the D-121/D-122 range. |
| "9 requirements, 7 with no acceptance row" | Counted the Requirement-to-workflow map (9 rows, 7 marked ⚠); cross-checked against `unit-of-work-story-map.md` L91–116 and its own summary row L235 ("9", "7") | **Confirmed correct in all three artifacts.** |
| Owns WS-14, WS-15, TA-12, TA-13, TA-26 (5); supports TA-20 | Cross-checked against `unit-of-work-story-map.md` L235 and the individual WS/TA rows (L179, L180, L195, L196, L203, L209) | **Confirmed correct.** |
| Grid "ridge 6, RF 18, LSTM 16" and "seven LSTM settings" | Matched against `requirements.md` L398 and Vision line 1206 | **Confirmed correct as restatements; source now correctly cited to the Vision register.** |
| "Five named, four reachable" ablations | Counted TE §7.2 registry as restated in `requirements.md` L399: NODOY, DIFF, NOSW, HIST48, ZENITH = 5; ZENITH deferred = 4 reachable | **Confirmed correct.** |
| Rules R-90…R-102 | Grepped `## R-` headers in `business-rules.md`: R-90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102 — 13 headers, sequential, no gaps or duplicates | **Confirmed: 13 rules, all present and sequential.** |
| Domain-entities §§ 1…12 | Grepped `## <n>.` headers in `domain-entities.md` during the full read: sections 1 through 12 present in order | **Confirmed.** |
| "Three mechanisms" (R-95 / §5 / W-5) | Grepped "Two mechanism" across all three files: zero live occurrences outside the Review section's historical quotation | **Confirmed — finding 4's fix is clean, no regression.** |
| "07's half is unowned" stated consistently | Grepped "unowned" / "the fifth" across all three files | **Inconsistent — present correctly in W-1/R-90/§11 bodies and in all three Assumptions & Open Questions lists, but contradicted by `business-logic-model.md` L298 — see Finding 1.** |
| `unit-of-work.md` §8's "six implementation notes" all reach a workflow/rule/entity | Read §8's bullet list (three-seed parameter, Jan–Nov tuning, RF-importance non-authority, seed/grid freeze, ablation predeclaration, +24h config-only) against W-2…W-9 / R-91…R-99 / §§3,5,6,7,8,9 | **Confirmed — no orphaned implementation note.** |

### Failed refutation attempts

- Attempted to find a further drifted signature for `Prediction`, `fit_predict`, `three_seed_mean`, `climatology_fit_partition` against `component-methods.md` on this pass — none found; the four continue to match verbatim including the ADR-11 fields.
- Attempted to find a new circular dependency or DAG mismatch — `models-and-baselines` still depends only on `features-and-splits`, matching `unit-of-work.md` §8 exactly; no new edge introduced by the iteration-1 fixes.
- Attempted to show the newly-added "D-122 sign-off closed" correction was itself inaccurate or overstated (e.g., that it silently drops the "no signature artifact exists" caveat) — it does not; all three artifacts carry that caveat verbatim alongside the closure claim, matching Vision line 1207 exactly.
- Attempted to show the R-90/W-1 "semantic, not a call edge" rewrite (finding 2's fix) introduced a new claim about the sibling's test that isn't supported by `features-and-splits`' R-74 — re-read R-74 (L160–165) again on this pass; the rewritten text's characterization ("reads the emitted stamps and asserts that refusal... not monkeypatch-and-replay") is a closer paraphrase than iteration 1's own summary of it, not a looser one. Held.
- Attempted to show the grid/seed cardinality restatements had silently drifted from the Vision register's actual wording since iteration 1 — re-read Vision lines 1206–1207 character-by-character against the artifacts' restatement; no drift found.
- Attempted to find a stale "5 units" or "8 across 5" figure anywhere that should now read differently given the `07` correction — found none stated as a hard number needing revision; the artifacts consistently treat the *count* (8, 5) as unaffected by *which* unit discharges the fifth slot's `06` half, which is internally coherent even though the closing sentence at L298 contradicts it (Finding 1) — the count itself was not shown to be wrong, only that one sentence about it is.

### Summary

The two Critical and two of the three Major defects from iteration 1 are now correctly and verifiably resolved against the source documents I re-checked directly (the Vision register lines 1206–1207, `evidence/DECISIONS.md`'s D-1…D-27 range, and `features-and-splits`' own R-74 text). The previously-unraised D-122 sign-off correction also checks out exactly against the Vision register. But the sweep was incomplete in exactly the way this project has now logged as its own recurring failure mode twice in `project.md`'s Corrections: fixing a claim in one representation (a body paragraph, an Open Question) while leaving another representation of the same claim standing elsewhere. `business-logic-model.md` L298 still asserts, in the artifact's own most gate-relevant accounting section, that this unit "is the fifth" and that `06`/`07` are jointly where the stamp is refused "with nothing here adding to the total" — the precise pre-correction framing finding 3 required fixed, standing 20 lines below the correction that fixed it everywhere else. Separately, `requirements.md`'s FR-P1-05-2 row carries a second stale clause (the D-122 "sign-off pending" text) on the same line where finding 5 already required flagging a first stale clause (the bootstrap-seed misattribution) — the fix reached one clause and not its neighbour on the same row. A third, more minor gap: the R-95/§5 join specification added for finding 6 references a `TuningRecord` field ("the run's own timestamp") that the entity table never declares, so an implementer still cannot build the join exactly as stated without inventing an attribute.

**Verdict: NOT-READY.**

## Review — Post-redo pass

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-24T14:59:08Z
**Iteration:** 1 of the fresh budget

### Status of the iteration-2 findings

| # | Iteration-2 severity | Fix claimed | My independent basis | Disposition |
|---|---|---|---|---|
| 1 | Critical | `business-logic-model.md` § Amendments owed rewritten to state `06`/`07` as two units, this unit discharging `06` only, total unaffected; superseded wording preserved in a dated warning box | Read `business-logic-model.md` § Amendments owed directly: the closing sentence now reads "This unit discharges `06`'s half; `07`'s half is unowned and open... The total is unaffected either way." Grepped the pre-Review body of all three files for `fifth`/`07's half`: the only place "This unit is the fifth... Nothing here adds to the total" still appears is inside the dated warning box that explicitly quotes it as the superseded wording being corrected — not asserted as current fact. Cross-checked against `unit-of-work.md` §8/§9 (read directly): `06_train_and_predict.py` maps to `models-and-baselines`, `07_evaluate_and_report.py` maps to `evaluation-and-comparison`, confirming the "two units" framing is accurate. | Correctly and fully resolved. |
| 2 | Major | All three artifacts' Open Questions now name both clause (a) (bootstrap seed) and clause (b) (sign-off status) of `requirements.md` FR-P1-05-2's stale line | Read `requirements.md` FR-P1-05-2 directly: verbatim carries the bootstrap-seed-20221201-attributed-to-D-122 clause and the "Vision §14.2 marks it Approved, supervisor sign-off pending... still owes a signature at G-05" clause. Both clauses are present exactly as the artifacts describe. Grepped all three files' Assumptions & Open Questions for the identical two-clause paragraph: present verbatim and identically in all three files. Cross-checked the Vision register directly: D-122 reads "Approved; supervisor sign-off closed 2026-08-22"; D-126/D-128 read "Approved, supervisor sign-off pending" — confirming the artifacts' claim about which decision that phrase actually belongs to. | Correctly and fully resolved, consistently across all three artifacts. |
| 3 | Minor | `run_at` added to `domain-entities.md` §5's `TuningRecord` table; R-95's join now names `TuningRecord.run_at` | Read `domain-entities.md` §5's table directly: `run_at` is present, described as the timestamp of the tuning run itself, with a note that R-95's join correlates against it. Read `business-rules.md` R-95 mechanism 3 directly: the join is now stated as an access-timestamp window bounded below by `TuningRecord.criterion_declared_at` and above by `TuningRecord.run_at`, both operands resolving to declared fields. No orphaned field reference remains for this specific join. | Correctly resolved for this specific join — but see new Finding 2 below: a different, pre-existing field-reference defect in the same table (`criterion_used_hash`) was not caught by this fix and still stands. |

All three redo fixes hold under independent re-derivation; no regression was found in the specific text each fix touched. The sweep did not, however, extend to two adjacent defects in the same sections, plus one gap in a rule examined closely for the first time this pass — see the three Findings below.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `domain-entities.md` §11 negative controls for the stamp-match mechanism, versus `business-rules.md` R-90 and `business-logic-model.md` W-1 | `domain-entities.md`'s own copy of the negative-control set for the eighth-amendment stamp match is incomplete, and drops the paired "must not fire" control entirely. All three artifacts describe the identical mechanism (the match function checking fold ID, purpose, and transform-ID presence before scoring). `business-rules.md` R-90 and `business-logic-model.md` W-1 each state three negative controls — a train-stamped frame reaching that fold's validation scoring fails; an unstamped frame reaching any scoring path fails; a frame stamped for one fold's evaluate purpose reaching a different fold's scoring fails — plus the paired "must not fire" control (a frame correctly stamped for the fold actually being scored must pass). `domain-entities.md` §11 states only the first two of these; the third negative control and the entire "must not fire" control are missing from the entity artifact that is supposed to be this mechanism's authoritative shape statement. This is the same representation-sweep failure class `project.md` records twice already, occurring in a location the two prior iterations did not check — they verified the prose fix to W-1/R-90's placement rationale, not whether the entity page's own control list stayed in sync with it. | Add the missing negative control (a frame stamped for one fold's evaluate purpose reaching a different fold's scoring path) and the "must not fire" control (the ordinary matching case passes) to `domain-entities.md` §11, matching `business-rules.md` R-90 and `business-logic-model.md` W-1 exactly. |
| 2 | Major | `domain-entities.md` §5 `TuningRecord` table, the `criterion_used_hash` row; echoed ambiguously in `business-rules.md` R-95 mechanism 2 | `criterion_used_hash`'s stated equality target is a field that does not carry a hash. The `TuningRecord` table defines `criterion_declared_at` as a timestamp — when the selection criterion was declared, before tuning began — and `criterion_hash` as the declared criterion, hashed. Immediately below, `criterion_used_hash` is specified as the criterion actually used, and required to equal `criterion_declared_at`'s hash — but `criterion_declared_at` is a timestamp field with no declared hash value; the field that actually holds "the declared criterion, hashed" is `criterion_hash`, one row up in the same table. An implementer following the table as literally written has no attribute named or computable as `criterion_declared_at`'s hash, and must either invent one or guess that the intended comparison is against `criterion_hash` instead — precisely the class of ambiguity iteration-1 finding 6 was raised to eliminate from this same table, and which this redo's fix (adding `run_at`) did not touch because it targeted a different field pair entirely. `business-rules.md` R-95 mechanism 2 is looser in wording but reads consistently with the same conflation, naming `criterion_declared_at` alongside `criterion_used_hash` as the compared pair rather than `criterion_hash`. | In `domain-entities.md` §5, change `criterion_used_hash`'s definition to require equality with `criterion_hash`, not with `criterion_declared_at`. In `business-rules.md` R-95 mechanism 2, name the compared pair explicitly as `criterion_hash` and `criterion_used_hash`, keeping `criterion_declared_at` only as the ordering anchor mechanism 3 already uses it for. |
| 3 | Major | `business-rules.md` R-96's Rule paragraph, second sentence; no corresponding mechanism anywhere in `domain-entities.md` §7 | R-96's second named prohibition — no second 2022 test period is selected after results are observed — has neither an owned mechanism, a negative control, nor a cross-unit consumed-obligation disclaimer, unlike every other cross-unit-owned obligation in these three artifacts. R-96's Rule paragraph states two prohibitions together: no grid range changes after December is seen, and no second 2022 test period is selected after results are observed. The first half is fully mechanised — all four of R-96's negative controls test grid content and immutability. None of them, nor any other text in R-96, tests or even mentions the test-period clause. Every other place these three artifacts state a rule this unit does not itself enforce, they say so explicitly and record it as a consumed cross-unit dependency — the RF-importance evidence obligation and Vision's honesty-bar obligation both carry this exact disclaimer elsewhere in the same documents. R-96 gives the test-period clause no such treatment: it is stated as this unit's Rule, with no note that test-period/partition selection belongs to another unit, and no negative control of any kind. A reader of R-96 alone cannot tell whether this is a deliberate scoping choice or a gap in this unit's own coverage. | Either add a negative control for the test-period clause, checked against whichever unit owns partition/test-period definitions, or add the same disclaimer pattern used elsewhere in these artifacts: state explicitly that test-period selection is a consumed obligation owned by another unit's mechanism, and that R-96 restates the prohibition without claiming a check over it. |

### Validation tool results

No stage-specified validation tooling was listed for this stage's dispatch; none was run (unchanged from iterations 1 and 2). All findings above were derived by direct Read/Grep re-derivation against: the Vision document's decision register (read directly, including D-121, D-122, D-126, D-128, and the seven-fixed-LSTM-settings line), `evidence/DECISIONS.md` (grepped every decision-number occurrence across the full file), `requirements.md` (FR-P1-05-2 and surrounding rows read directly), `unit-of-work.md` (§8 and §9 read directly), `component-methods.md` (the `src/models` section read directly for `Prediction`, `fit_predict`, `three_seed_mean`), and the granted sibling carve-out `features-and-splits/functional-design/business-rules.md` (§ Amendments owed and the R-74/FU-4=D text read directly).

### Counts and enumerations re-derived independently

| Claim | Derivation | Result |
|---|---|---|
| Rules R-90 through R-102 present and sequential | Grepped rule headers in `business-rules.md`: R-90 through R-102, 13 headers, no gaps or duplicates | Confirmed: 13 rules. |
| Entity sections 1 through 12 | Grepped numbered section headers in `domain-entities.md`: 1 through 12, all present in order | Confirmed. |
| 9 requirements, 7 without acceptance rows | Counted the Requirement-to-workflow map in `business-logic-model.md` (9 rows, 7 flagged) and the Requirement coverage table in `domain-entities.md` (same 9 rows, same 7 flagged); cross-checked against `unit-of-work.md` §8's own count, read directly | Confirmed correct and consistent across all three artifacts and the upstream contract. |
| Ablations: 5 named, 4 reachable | Counted `domain-entities.md` §8 and `business-rules.md` R-97: five named ablation IDs, one deferred to Phase 2 | Confirmed correct. |
| Grid cardinalities 6/18/16 | Matched against the Vision register's D-121 row, read directly | Confirmed correct, verified against the primary source, not a restatement. |
| Seven fixed LSTM settings | Read the Vision document's fixed-settings sentence directly and counted its comma-separated items | Confirmed correct, verified against the primary Vision-document source rather than `requirements.md`'s restatement, for the first time across all three review iterations. |
| Amendment total 8 across 5 units | Re-summed `features-and-splits/functional-design/business-rules.md` § Amendments owed directly: five (external-products) plus one plus one plus one equals eight; "5 units" read directly as three (from the external-products count) plus `features-and-splits` itself plus "the fifth" (the `06`/`07` pair, stated as one by the sibling but actually two owning units per `unit-of-work.md` §8/§9) | Arithmetic for 8 confirmed correct. The "5 units" figure is internally inconsistent by the sibling's own text once `06`/`07` are counted as the two distinct units they are — already flagged as an open item in all three artifacts under review, not a new defect. |
| `TuningRecord` field count (post-fix) and usage | Counted `domain-entities.md` §5's table directly: seven fields, up from six before the `run_at` fix. Checked each against `business-rules.md` usage: all seven are referenced by name somewhere, except that `criterion_used_hash`'s stated comparison target names the wrong field — see Finding 2 | Seven fields, all used, one used against a mis-specified comparison target. |
| `06`/`07`'s owning units | Read `unit-of-work.md` §8 and §9 directly | Confirmed: `06_train_and_predict.py` belongs to this unit; `07_evaluate_and_report.py` belongs to `evaluation-and-comparison`, a different, not-yet-designed unit. |
| "07's half of the eighth amendment is unowned" stated consistently, nowhere contradicted | Grepped the pre-Review body of all three files for the relevant terms | Consistent in all three artifacts' body text and Assumptions & Open Questions. The one instance of the pre-correction wording left standing is inside a dated warning box explicitly quoting it as superseded — not asserted as current fact. No live contradiction found. |
| Signatures for `Prediction`, `fit_predict`, `three_seed_mean`, `climatology_fit_partition` | Read `component-methods.md`'s `src/models` section directly | All four quoted verbatim in all three artifacts, including the ADR-11 provenance fields and the `expected_seeds` parameter. No drift. |

### Failed refutation attempts

- Attempted to show the iteration-2 Critical fix left any live restatement of the pre-correction "fifth unit" framing outside a dated historical quotation — grepped the full pre-Review body of all three files; the only surviving instance is inside the warning box explicitly framed as the superseded wording being corrected. Held: no regression.
- Attempted to show `requirements.md`'s FR-P1-05-2 line had drifted further, or that the artifacts' restatement of it had drifted, since iteration 2 — read it directly; matches the iteration-2 record exactly, and both stale clauses are now named identically across all three artifacts' Open Questions. Held.
- Attempted to find a second orphaned-field defect introduced specifically by the `run_at` fix itself — none found; the fix is clean for the specific join it targeted. The `criterion_used_hash` defect (Finding 2) is independent, predates this redo's fix, and was not introduced by it.
- Attempted to show the Vision-register grid cardinalities or seven LSTM settings had drifted from source between iterations — re-read the Vision document directly against all three artifacts' restatements; exact match, no drift.
- Attempted to find a new circular dependency or DAG mismatch introduced by any of the three fixes — this unit still depends only on `features-and-splits` per `unit-of-work.md` §8, unchanged.
- Attempted to show the `run_at` field addition itself broke a downstream consumer entity — `run_at` is scoped to `TuningRecord` only and does not collide with any field in the `Prediction` or `Checkpoint` entities.
- Attempted to show R-101's "two mechanical comparisons" was itself miscounting or conflicting with R-95's "three mechanisms" — re-read both directly: R-101 counts a disjoint pair of checks from R-95's three-mechanism December-tuning-residual set. No conflict, no regression.

### Summary

All three findings this redo pass was authorised to fix are independently verified fixed, with no regression in the specific text each fix touched: the Amendments-owed paragraph now states the `06`/`07` split consistently with the rest of the document and preserves the superseded wording only as a dated, clearly labelled historical quotation; all three artifacts now name both stale clauses of `requirements.md` FR-P1-05-2 rather than one; and `domain-entities.md` §5 now declares `run_at`, closing the specific join gap iteration-2 finding 6 identified. The Vision-register citations, the grid cardinalities, and the seven LSTM settings were re-verified against the primary source document directly rather than against `requirements.md`'s restatement, for the first time across the three review passes, and all check out exactly. However, the sweep that fixed these three items did not extend to two adjacent, pre-existing defects sitting in the same sections it touched, plus one long-standing gap in a rule examined closely for the first time this pass: `domain-entities.md` §11 carries an incomplete copy of the negative-control set for the identical mechanism `business-rules.md` R-90 and `business-logic-model.md` W-1 state in full; the same §5 table that was just repaired for one field-reference gap still names the wrong field as `criterion_used_hash`'s comparison target; and R-96's "no second test period" clause has neither a mechanism, a negative control, nor the consumed-obligation disclaimer this project uses everywhere else for a rule it states but does not itself enforce. None of the three is a re-emergence of a previously-fixed defect, and none rises to Critical — but three Major findings, each independently verified against primary sources and each fitting this project's own documented recurring failure mode of a fix reaching one representation and stopping short of an adjacent one, together exceed this stage's readiness bar.

**Verdict: NOT-READY.**

## Review — Post-redo pass, iteration 2

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-24T15:15:00Z
**Iteration:** 2 of the fresh budget (final)

### Status of the post-redo findings

| # | Post-redo severity | Fix claimed | My independent basis | Disposition |
|---|---|---|---|---|
| 1 | Major | `domain-entities.md` §11 now lists all three negative controls plus the must-not-fire control, matching `business-rules.md` R-90 and `business-logic-model.md` W-1 exactly, with a dated ⚠ box naming the gap | Read `domain-entities.md` §11 directly (lines 357–365): all four controls present — `(fold 4, train)`→fails, unstamped→fails, `(fold 2, evaluate)` on fold 3→fails, and the must-not-fire `(fold 4, evaluate)` on fold 4→passes. Diffed word-for-word against R-90's and W-1's control lists: identical in substance and ordering. | **Correctly and fully resolved.** |
| 2 | Major | `domain-entities.md` §5's `criterion_used_hash` row now reads "must equal `criterion_hash`" with the correction recorded inline | Read the table directly (line 200): `criterion_used_hash` → "the criterion actually used, hashed. **Must equal `criterion_hash`**..." with an inline note naming the prior defect. `criterion_hash` (the row above) is defined as "the declared criterion, hashed" — the two now form a coherent, checkable pair. `business-rules.md` R-95 mechanism 2 (line 154) still labels the item `criterion_declared_at` / `criterion_used_hash` and says "the criterion declared before tuning equals the one used" — looser prose than the table, but no longer asserts a false equality; see Finding 1 below for the residual ambiguity this leaves. | **Correctly resolved at the entity table (the authoritative location); a non-blocking wording residual survives elsewhere — see Finding 1.** |
| 3 | Major | R-96 now separates the two prohibitions, records the second as a consumed obligation owned by `features-and-splits` (`PartitionList`), cites D-8 and Vision §2.5's claim boundary, and names the enforceable limb (§3 limb 3's enumeration, `PartitionError`) | Read `business-rules.md` R-96 directly (lines 194–205) and `domain-entities.md` §3 limbs 3–4 directly. Read `evidence/DECISIONS.md` D-8 directly (lines 234–261): confirms "tested on December 2022" and "no claim... beyond this test month" — the ownership premise (December 2022 is the fixed test period) is real, not invented. Read the sibling carve-out `features-and-splits/functional-design/business-rules.md` R-80 directly (lines 487–553): confirms `features-and-splits` owns the closed six-row partition list (five partitions + the locked month), calendar-timestamp-derived, with its own exactly-one-partition-per-timestamp assertion — the ownership half of fix 3's claim is **true and independently verified**, not asserted on faith. The enforcement half is weaker than claimed — see Finding 2 below. | **Ownership claim verified true and well-grounded. The claimed enforcement mechanism does not match what `domain-entities.md` §3 Limb 4 actually specifies — new finding, not a reopening of the post-redo finding.** |

All three post-redo fixes hold at the location they were applied to, and none regressed. Fix 3's disclaimer is an improvement over the silence it replaced (per `project.md`'s "reversal needs a new argument" standard, this is a new argument — D-8 and R-80 read directly, not merely cited on trust) — but the sentence describing what this unit *can* enforce overstates what Limb 4 actually checks; see Finding 2.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `domain-entities.md` § 3 Limb 3 ("Allowed partitions" table) and Limb 4 ("Failure conditions" table), lines 127–146; consumed by `business-rules.md` R-96, lines 202–205 | **R-96's claimed enforcement ("a partition outside that enumeration raises `PartitionError`") is not what Limb 4 actually specifies.** Limb 3 lists three "yes" categories (F1–F4 validation months, the January–November refit, December through the guard) and two "no" categories ("a training partition" → `PartitionError`; "a mixture of partitions" → covered by the AlignmentError/PartitionError split). Limb 4, which is the contract's own authoritative statement of when `three_seed_mean` raises, lists exactly two conditions for `PartitionError`: "`partition_id` differs across the three inputs, or names a training partition (limb 3)." Neither condition is "partition_id is not one of the enumerated allowed values." A hypothetical fourth `partition_id` — say, a second locked-test-month value that all three seed-inputs agree on and that is not literally labelled a training partition — would satisfy both of Limb 4's stated conditions (no disagreement, not a training partition) and would **not** raise `PartitionError` under the text as written, contradicting R-96's claim that "a second test period cannot be *scored* here." This gap is masked in practice only by a fact neither R-96 nor domain-entities.md §3 states: `features-and-splits` R-80 (verified directly, in the sibling carve-out) closes `partition_id`'s entire value space to exactly six calendar-timestamp-derived values, so a genuinely novel partition value cannot arise without `features-and-splits` first editing its own frozen table — which is the real reason a second test period "cannot be scored here." R-96 asserts a check exists in this unit's own mechanism where the real safeguard is an upstream type-closure this unit's design never names. An implementer building `three_seed_mean` from Limb 4 alone, taken literally, has no instruction to reject an unrecognised `partition_id`, and the design's own stated rationale for why the prohibition is "enforced" here does not survive a literal reading of the one table it cites. | Either (a) add a Limb 4 condition that raises `PartitionError` for a `partition_id` not among Limb 3's enumerated "yes" categories (making the enumeration self-enforcing rather than descriptive), or (b) rewrite R-96's enforcement sentence to state the true mechanism: `partition_id`'s value space is closed by `features-and-splits`' R-80 partition list, so no fourth category can exist without a change to that sibling's frozen artifact, and `three_seed_mean` therefore never needs to (and currently does not) check for an "unknown" partition. Option (b) is cheaper and matches what the design actually relies on. |
| 2 | Minor | `business-rules.md` R-95, mechanism item 2 (line 154), versus `domain-entities.md` §5's now-corrected `criterion_used_hash` row | **A wording residual from the fixed post-redo finding 2 survives one representation over.** The entity table (the authoritative location) now correctly states `criterion_used_hash` "must equal `criterion_hash`". `business-rules.md` R-95's mechanism 2, covering identical content, still labels the item "`criterion_declared_at` / `criterion_used_hash`" and describes it only as "the criterion declared before tuning equals the one used" — never naming `criterion_hash` as the actual comparison target. This is not a false claim (it does not assert an equality between `criterion_declared_at` and `criterion_used_hash` the way the pre-fix entity table did), but it is the same field pairing that produced the original defect, restated loosely enough that a reader of `business-rules.md` alone, without cross-referencing the entity table, could still reconstruct the wrong comparison. Non-blocking: the authoritative table is correct and an implementer working from `domain-entities.md` §5 has the right instruction. | Rename the mechanism-2 label in `business-rules.md` R-95 to "`criterion_hash` / `criterion_used_hash`", matching the entity table exactly, so the rule text and the entity shape name the same pair. |

### Validation tool results

No stage-specified validation tooling was listed for this stage's dispatch; none was run (unchanged from all three prior passes). All findings above were derived by direct Read/Grep re-derivation against: `domain-entities.md` §3 Limbs 3–4 and §5's `TuningRecord` table (read directly), `business-rules.md` R-90, R-95, and R-96 (read directly), `evidence/DECISIONS.md` D-8 (read directly, lines 234–261), and the granted sibling carve-out `features-and-splits/functional-design/business-rules.md` R-80 (read directly, lines 487–553) — the only two sibling files in scope, and no other `construction/<other-unit>/` path was accessed.

### Counts and enumerations re-derived independently

| Claim | Derivation | Result |
|---|---|---|
| Rules R-90…R-102 present and sequential | Grepped `^## R-` in `business-rules.md`: R-90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102 — 13 headers, no gaps or duplicates | **Confirmed: 13 rules.** |
| Entity sections 1…12 | Grepped `^## [0-9]` in `domain-entities.md`: sections 1 through 12, all present in order | **Confirmed.** |
| Workflows W-1…W-11 | Grepped `^## W-` in `business-logic-model.md`: W-1 through W-11, all present in order | **Confirmed.** |
| "9 requirements, 7 with no acceptance row" | Counted the Requirement-to-workflow map in `business-logic-model.md` (9 rows; ⚠-flagged: FR-P1-04-14, -05-3, -4, -5, -6, -21, -22 = 7; unflagged: FR-P1-05-1, -05-2 = 2; 7+2=9) and the Requirement coverage table in `domain-entities.md` (identical 9 rows, identical 7 flagged) | **Confirmed correct and identical across both artifacts.** |
| `TuningRecord` field count and usage | Counted `domain-entities.md` §5's table directly: `run_id`, `partitions_read`, `criterion_declared_at`, `criterion_hash`, `criterion_used_hash`, `run_at`, `audit_access_since_declaration` = 7 fields. Checked each against R-95's three mechanisms: all seven referenced, `criterion_used_hash` now against the correct target (`criterion_hash`), `run_at` against mechanism 3's upper bound | **Confirmed: 7 fields, all used, no orphaned or mis-targeted field remaining in the entity table.** |
| Ablations: 5 named, 4 reachable | Counted `domain-entities.md` §8 and `business-rules.md` R-97: `ABL-NODOY`, `ABL-DIFF`, `ABL-NOSW`, `ABL-HIST48`, `ABL-ZENITH` = 5; `ABL-ZENITH` deferred = 4 reachable | **Confirmed correct, no drift from the post-redo count.** |
| Grid cardinalities 6/18/16 and the seven LSTM settings | Matched `domain-entities.md` §7 and `business-rules.md` R-96 against each other, character for character | **Confirmed identical between the two artifacts; unchanged from the post-redo pass, which verified both against the Vision register directly.** |
| Amendment total 8 across 5 units | Re-read `business-logic-model.md` § Amendments owed directly: "8, across 5 units" (from `features-and-splits`) + "0" (this unit) = "8 across 5 units", with the `06`/`07` two-unit correction stated consistently in the same paragraph and in the Assumptions & Open Questions list | **Confirmed unchanged and internally consistent; no reversion to the pre-iteration-2 wording found anywhere in the pre-Review body.** |
| Partition list: "five partitions plus the locked month" (six rows) | Read `features-and-splits/functional-design/business-rules.md` R-80 directly: F1, F2, F3, F4, Final refit, December = 6 rows, stated there as "five partitions... plus the locked month" | **Confirmed — R-96's restatement matches the sibling's own count exactly.** |
| D-8's test-month claim boundary | Read `evidence/DECISIONS.md` D-8 directly (lines 234–261): "tested on December 2022... No claim of generalisation beyond... this test month" | **Confirmed — R-96 cites D-8 accurately, not on trust.** |

### Failed refutation attempts

- Attempted to find a fourth negative control or must-not-fire control missing from `domain-entities.md` §11 after the fix — re-diffed against R-90 and W-1 line by line; all four controls present and matching. Held: no regression.
- Attempted to show the `criterion_used_hash` fix introduced a new orphaned reference elsewhere (e.g., in `business-logic-model.md` W-5's restatement of R-95) — read W-5 directly (lines 154–174): it restates the three mechanisms at a summary level without naming individual field-to-field comparisons, so it carries no risk of the same defect. No new instance found.
- Attempted to show the R-96 fix's ownership claim was fabricated or unverifiable — read D-8 and R-80 directly rather than accepting the citation; both check out exactly as R-96 states them. Held as a genuine, evidenced fix, not a plausible-sounding but ungrounded one.
- Attempted to find a second location asserting the "a partition outside the enumeration raises `PartitionError`" claim that Finding 1 disputes — grepped for "PartitionError" across all three artifacts: it appears in `domain-entities.md` Limb 4, §12's exception table, `business-rules.md` R-92 and R-96, and `business-logic-model.md` W-3's outline. Only R-96's sentence makes the "outside the enumeration" claim; the others correctly restate Limb 4's actual two conditions (mismatch, training partition). The overstatement is localized to one sentence, not systemic.
- Attempted to show the amendment-accounting regression from iteration 2 (finding 1, "This unit is the fifth... nothing adds to the total") had resurfaced anywhere in the current text — grepped `business-logic-model.md` for "is the fifth" and "nothing here adds": the only live occurrence is the corrected sentence ("This unit discharges `06`'s half... `07`'s half is unowned and open... total is unaffected either way"); the superseded wording survives only inside the dated ⚠ box quoting it as historical. No reversion.
- Attempted to re-open the D-121/D-122 citation question from iteration 1 given fresh eyes — re-grepped `evidence/DECISIONS.md` for `121`/`122`: still absent; the artifacts still correctly cite the Vision register instead. No regression.
- Attempted to find a circular dependency or DAG change introduced by any of the three post-redo fixes — `models-and-baselines` still depends only on `features-and-splits` per `unit-of-work.md` §8, unchanged by any of the three fixes, none of which touched a dependency edge.

### Summary

All three Major findings from the post-redo pass are independently verified fixed at the location the fix targeted, with no regression in the touched text: `domain-entities.md` §11 now carries the complete four-control set matching R-90 and W-1; `domain-entities.md` §5's `criterion_used_hash` row now names the correct comparison target; and R-96 now separates the two prohibitions, and its ownership claim — that `features-and-splits`' R-80 partition list, not this unit, is where a second test period would have to be created, and that December 2022 is D-8's fixed test month — was checked against both cited sources directly and holds. One new, non-recurring Major finding surfaced on this pass: R-96's closing sentence claims a `PartitionError` check over "partitions outside the enumeration" that `domain-entities.md` §3 Limb 4 does not actually specify — Limb 4's own two stated conditions (cross-input disagreement, or a training partition) would not catch a hypothetical novel partition value, and the real reason no such value can arise is an upstream type-closure (R-80's fixed six-row list) that R-96 never names as the actual mechanism. This is a genuine gap between a claimed check and the cited contract's literal text, but it is narrowly scoped to one sentence's framing, has a cheap fix (restate the mechanism as upstream closure rather than a local enumeration check, or add the missing Limb 4 condition), and does not undermine the ownership analysis it sits inside — which is independently correct. A second, Minor, non-blocking wording residual (R-95's mechanism-2 label still pairs `criterion_declared_at` with `criterion_used_hash` rather than `criterion_hash`) survives in a non-authoritative location while the authoritative entity table is fully correct. One Major and one Minor finding, both narrowly scoped, neither reopening a previously "fixed" defect, together fall under this stage's ≤2-Major READY threshold, and an implementer working from the authoritative tables (domain-entities.md §§3, 5, 11) would build the correct behaviour for every mechanism this pass checked except the one-sentence overstatement in R-96, which is reporting-quality rather than implementation-blocking: the actual enforcement path (upstream partition-list closure) exists and is sound even though the sentence describing it points at the wrong table.

**Verdict: READY.**

---

> **Re-saved unchanged 2026-08-26 under the fourteenth-redo re-confirmation receipt** (redo taken
> for `external-products`; floor reset mechanical). **No content of this unit changed.** The two
> residuals riding the READY — R-96's `PartitionError` mechanism and R-95's field label — remain
> carried to the stage gate rather than applied. **G-09 remains unsigned, and BLK-03 independently
> bars implementation.**

## Review — 2026-08-26 fourteenth-receipt confirming pass

**Reviewer:** aidlc-architecture-reviewer-agent

**Verdict:** READY

### Scope and method

Narrow confirming pass under the fourteenth-redo re-confirmation receipt. No content
re-litigation — only regression against the terminal `## Review — Post-redo pass, iteration 2`
(READY, 2026-08-24T15:15:00Z) fails this pass. Read all four in-scope files in full and ran
scripted checks (`bun -e`) rather than perl.

### Findings

1. **Provenance blockquote, all three artifacts.** Each of `business-logic-model.md`,
   `business-rules.md`, `domain-entities.md` carries exactly one "Re-saved unchanged 2026-08-26
   under the fourteenth-redo re-confirmation receipt" blockquote, immediately after its terminal
   READY content, and nothing else was added or removed (grepped for `2026-08-26`: one hit per
   file, at the tail). No regression.
2. **The two residuals remain unapplied, verified at their named locations.**
   `business-rules.md` R-96's closing sentence still claims a `PartitionError` check over "a
   partition outside that enumeration"; `domain-entities.md` § 3 Limb 4 still states only two
   `PartitionError` triggers (cross-input `partition_id` disagreement, or a training partition) —
   the enumeration-membership condition the closing sentence implies is not there, exactly as the
   terminal READY described. `business-rules.md` R-95 mechanism 2 still labels the compared pair
   `criterion_declared_at` / `criterion_used_hash` rather than `criterion_hash` /
   `criterion_used_hash`, while `domain-entities.md` § 5's authoritative table correctly pairs
   `criterion_used_hash` with `criterion_hash`. Both residuals are correctly carried to the gate,
   not applied.
3. **Re-derived counts, independently, all match the questions file's re-confirmation claim.**
   `business-rules.md`: `R-90`…`R-102`, 13 headers, sequential, no gaps. `business-logic-model.md`:
   `W-1`…`W-11`, 11 headers. `domain-entities.md`: sections `1.`…`12.`, 12 headers.
   `functional-design-questions.md`: `Question 1`…`Question 8`, all 8 answered (`D, D, D, D, D, C,
   D, D`).
4. **Questions file's new re-confirmation section is well-formed.** "### Re-confirmation,
   2026-08-26 — under the fourteenth-redo floor" carries an `> **Impact**:` line under each of its
   two options (`Looks correct`, `Request changes`), a single `> **💡 Recommendation**:` line
   placed after both options and before `[Answer]:`, and the filled answer is the literal `Looks
   correct`, matching the recommendation.
5. **Zero mojibake across all four files.** Scripted scan (`bun -e`) for `Ã`/`Â` byte-run
   artifacts and for C1 control characters (U+0080–U+009F) found zero hits in any of the four
   files.

No regression found against the terminal READY. G-09 remains unsigned and BLK-03 independently
bars implementation — this pass adjudicates artifact regression only, not gate authority.

READY
