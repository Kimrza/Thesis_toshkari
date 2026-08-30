# Business Rules — `models-and-baselines`

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

## R-90 — A frame whose spec is not `(partition k, role "score")` never reaches partition *k*'s scoring

**Rule (rewritten 2026-08-28 — `GOV-2026-08-28-FD-01` Recommendation 3, approved).**
`06_train_and_predict.py` calls a **named match function in `src/models/train.py`** before
**every** scoring path. Against the `Partition` being scored, the function checks three things,
each with its own raise:

| Check | Field, as ADR-11 declares it | Raises |
|---|---|---|
| The frame is the one for **this** partition | `bundle.spec.partition_id == partition_being_scored.partition_id` | **`PartitionError`** |
| The frame is a **scored** frame, not a training frame | `bundle.spec.role == "score"` | **`PartitionError`** |
| The frame is transformed, by **this** partition's transform | `bundle.transform_id is not None` **and** equal to the `transform_id` of that partition's own `Transform` | **`LeakageError`** |

The first two are **declared-identity disagreements**; the third **implies information flow**.
That split is R-92's, applied here for the first time, and its discriminating rule is stated once
at R-92 rather than twice.

> ⚠ **REWRITTEN 2026-08-28 — the first text targeted `FeatureBundle` fields ADR-11 had already
> retired.** *(`GOV-2026-08-28-FD-01` Recommendation 3 — `IMPL-01`, Critical, veto exercised;
> owner-approved remediation.)*
>
> **Superseded, preserved verbatim:** *"The function checks `bundle.fold_id` equals the fold being
> scored, `bundle.purpose` equals `evaluate`, and `bundle.transform_id` is present. A mismatch
> raises **`LeakageError`**."*
>
> **Why it was wrong — three names, none of them on the object the function receives.** Verified
> by reading `component-methods.md` directly:
> - **`fold_id`** is not a `FeatureBundle` or `FrameSpec` attribute. It belonged to `FoldSpec`,
>   which ADR-11 **retired on 2026-08-23** (`component-methods.md:309`, inside that file's own
>   ⚠ AMENDED box, because `FoldSpec` could not represent the final refit). The live identity is
>   `FrameSpec.partition_id` (`:541`), matching `Partition.partition_id` (`:332`). *(`fold_id` is
>   not gone from the project — it survives as a TE §13.4 registry column and on this unit's own
>   `Checkpoint`, `domain-entities.md` § 4. It is gone from **this** object.)*
> - **`purpose`** is not a `FeatureBundle` attribute at all. The only `purpose` in the design is
>   on `governance-guards`' locked-test `AccessRecord` (`:270`), and its value set is
>   `"coverage_audit" | "regime_audit" | "locked_evaluation"`. The live field here is
>   `FrameSpec.role: Literal["train", "score"]` (`:542`), reached as `bundle.spec.role`.
> - **`"evaluate"`** is therefore not a value of anything. It is not one of `purpose`'s three
>   literals and not one of `role`'s two.
>
> **What the live contract already said, and this rule now quotes.** `component-methods.md:719`:
> *"`06`/`07` assert that a bundle scored for partition *k* carries `spec.partition_id == k`,
> `spec.role == "score"`, and the `transform_id` of *k*'s own transform."* The rewritten check is
> that sentence, with a raise attached to each limb.
>
> **How it survived.** W-2 (`business-logic-model.md`) has used ADR-11's `Partition`/`partition_id`
> vocabulary correctly since it was authored, so the defect was **internal to this unit** rather
> than an upstream drift. The only review pass run after ADR-11's retirement — the
> `## Review — 2026-08-26 fourteenth-receipt confirming pass` — **scoped itself explicitly to
> regression against the terminal READY** ("No content re-litigation") and therefore never
> re-checked this text against the live contract. That is recorded here as the mechanism, not as
> an excuse: a regression-only pass cannot detect a defect that was already present in the
> baseline it regresses against.

**Why here and not in `fit_predict`.** `fit_predict` is a **training** call. It can check the
stamp is present and internally consistent — and already raises `LeakageError` when
`bundle.transform_id is None` — but it **cannot know which partition the caller is about to
score**, which is the half of the requirement that matters. **Why not inline in the script:** §7
places reusable logic in `src/` and makes scripts orchestrators, so a governed check belongs in
`src/` even when a script is its only caller.

> ⚠ **Vocabulary corrected 2026-08-28 in the same sweep** (Recommendation 3). **Superseded:**
> *"cannot know whether the caller is about to score fold *k*'s validation month"*. Under ADR-11
> the scoring intent is a **`Partition`**, and only F1–F4 have a `validation_month`; `REFIT` carries
> `validation_month=None` and `DEC` carries 2022-12-01 (`component-methods.md:335`). Phrasing the
> gap as "fold *k*'s validation month" left the refit and the locked month outside the sentence —
> the same representational gap that retired `FoldSpec` in the first place.

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

**Negative controls, re-derived 2026-08-28 in ADR-11's vocabulary** (Recommendation 3). Each is
written as the `FrameSpec` the frame actually carries, so an implementer constructs the fixture
from the live dataclass and not from a retired one:

| # | The frame's `spec` | Reaching | Raises | Which limb |
|---|---|---|---|---|
| 1 | `FrameSpec(partition_id="F4", role="train", …)` | **F4's** score path | **`PartitionError`** | role — a training frame is not a scored frame |
| 2 | `bundle.transform_id is None` (untransformed), any `spec` | **any** score path | **`LeakageError`** | transform — the untransformed `raw` bundle is live in the process (`component-methods.md:711`) |
| 3 | `FrameSpec(partition_id="F2", role="score", …)` | **F3's** score path | **`PartitionError`** | identity — F2's frame is not F3's |
| 4 | `role="score"`, `partition_id="F3"`, but carrying **F1's** `transform_id` | **F3's** score path | **`LeakageError`** | transform — correctly *fitted*, wrongly *applied*; the leak R-74 element 4 exists for |

**Control that must *not* fire:** `FrameSpec(partition_id="F4", role="score", …)` carrying **F4's
own** `transform_id`, reaching **F4's** score path → **passes**. That is the ordinary path, and a
rule blocking it would be the failure mode `features-and-splits` already hit once — a control that
must not fire is as load-bearing as one that must.

**Enumerate, do not sample.** `Partition.partition_id` is closed to the **six** ids
`features-and-splits` R-80 fixes — `F1`, `F2`, `F3`, `F4`, `REFIT`, `DEC` (`component-methods.md:332`)
— so control 3 is asserted **by enumeration over ordered pairs of the six**, in the same shape
`component-methods.md` uses for the one enumerated `REFIT` → `DEC` carve-out, rather than on one
sampled pair.

> ⚠ **The controls were rewritten, not merely relabelled — the raise types changed for two of
> them** *(2026-08-28, Recommendation 3)*. **Superseded, preserved verbatim:** *"A frame stamped
> **`(fold 4, train)`** reaching **fold 4's validation scoring** → **`LeakageError`**. An
> **unstamped** frame reaching **any** scoring path → **`LeakageError`**. A frame stamped
> `(fold 2, evaluate)` reaching **fold 3's** scoring → **`LeakageError`**."* and *"a frame stamped
> `(fold 4, evaluate)` reaching **fold 4's** validation scoring → **passes**."*
>
> Controls 1 and 3 now raise **`PartitionError`** rather than `LeakageError`, under the
> discriminating rule stated at R-92. Control 4 is **new**: it is the only one of the four that
> exercises the transform limb on a *stamped* frame, and without it the transform check was
> falsifiable only by the `None` case. A test written against the superseded list would assert
> `pytest.raises(LeakageError)` on controls 1 and 3 and now fails — which is the intended
> consequence of fixing the taxonomy, and is called out here so the change is not discovered as a
> test break at 3.6.

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

> ⚠ **CLOSED 2026-08-28 — `07`'s half is now owned, and the box above is history.** *(Swept under
> `project.md` § Way of Working: extend a correction sweep into the artifacts that consumed the
> corrected fact, and sweep every representation.)* **Superseded, preserved:** *"a **different
> unit,** **whose functional design has not run**"* and *"**`07`'s half is unowned and open**"*.
> `evaluation-and-comparison`'s functional design **has** since run, and its **R-105** — *"`07`'s
> half of the eighth amendment: the stamp refusal at this unit's boundary"* — claims that half
> explicitly at the object `07` actually receives (`Prediction`s, not frames), citing this rule by
> name. `statistical-inference` **R-113** limb 2 then imports R-105. **The amendment total is still
> unaffected**, for the reason the superseded box already gave. **One live disagreement remains,
> and it is not this box's:** R-105 limb 2 raises `LeakageError` for the `partition_id`-mismatch
> condition while stating it *"mirror[s] R-92's provenance-agreement rule"*, and R-92 raises
> `PartitionError` for that condition. See R-92's 2026-08-28 box — the discriminating rule is
> stated there so R-105 has something it can mirror truthfully.

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

> ⚠ **ADDED 2026-08-28 — `PartitionError` is the FIFTEENTH project exception, and this is the
> discriminating rule.** *(`GOV-2026-08-28-FD-01` Recommendation 8 — `CHAIR-05` / `ML-05` /
> `IMPL-02`, High; the project decision owner ruled **option 1**: promote `PartitionError` into
> `foundation` R-01's enumeration as a formal amendment.)*
>
> **What was wrong.** `foundation` R-01 asserts completeness at *"all fourteen project-defined
> exceptions"* and `PartitionError` is not among them, yet it reaches **10 of the 12 units** —
> **23 occurrences in this unit's four artifacts as re-derived immediately before this edit**, the
> largest share of any unit (next: `features-and-splits` 15, `governance-guards` 8), out of **71**
> across all 48 artifacts; the edits in this box raise this unit's own figure, so 23 is stated as
> the measured basis of the finding and not as a live total — with **no
> `[assumption]` tag** and **no reference to R-01's any-future clause**. Two siblings disclosed
> their own additions properly (`fixtures-and-reproducibility` labels `FixtureError` *"a fifteenth,
> named at the gate"*; `statistical-inference` labels `InverseTransformError` unit-local under
> R-01's clause) and this unit disclosed nothing. Counts derived programmatically over all **48**
> artifacts before being asserted here, not carried from the finding's text.
>
> **The amended enumeration — LANDED, and re-verified at the close of this pass.** `PartitionError`
> is declared in **`foundation` R-01** as the **fifteenth**, deriving from `IntegrityError` and
> raised by this unit — so the stage-entry contract's `except IntegrityError` still writes the
> `aborted` registry row for it (R-10), which is the NFR-AUD-01 failure R-01 exists to prevent.
>
> **Verification, 2026-08-28, at the end of this remediation pass.** Mid-pass, `foundation` R-01 read
> *"All fourteen"* and named no `PartitionError`, and this box was first drafted saying the amendment
> was *"in flight in parallel"*. **It has since landed and was re-read directly.** R-01 now reads
> *"**Every project-defined exception derives from `IntegrityError`** … **Fifteen are named in the
> enumeration below** … The other **nine are raised by other units** … and — **added 2026-08-28** —
> **`PartitionError`** (`models-and-baselines`, declared in **`src/models/`** ⚠ **RULED 2026-08-28 — `PartitionError` is declared in `src/data/config.py`.** *(Project decision owner, on the `functional-design` gate, amending the wording of the Rec 8 ruling. **Superseded wording, preserved: declared in `src/models/`.**)* The reason is the one `features-and-splits` raised and the Rec 8 ruling could not have known: `component-dependency.md` marks **`src/features` → `src/models`** and **`src/data` → `src/models`** both as **`—`**, while every `PartitionError` raise in that unit lives in `src/data/splits.py` or `src/features/*` — so on the approved matrix that unit could not have raised the exception at all. `src/data/config.py` is where R-01 already declares `IntegrityError` and the base every unit already imports, so **no dependency-matrix amendment is needed and none is taken**. `models-and-baselines` remains the exceptions **semantic owner** — R-92s discriminating rule is unchanged — but is no longer its declaration site. )"*, under its own
> ✳ AMENDED box citing Recommendation 8 and the owner's option-1 ruling. Its Sources line now cites
> **this unit's § 12 as *"the authority for R-01's fifteenth entry"***, which is why § 12 states the
> discriminating rule in full rather than by reference. **The draft's "in flight" wording is
> superseded and is recorded here rather than left standing.**
>
> **One thing R-01's amendment also did, worth carrying:** it **restated its own count as derived
> rather than asserted**, and records that **33** distinct project-defined `*Error` names exist across
> the twelve units, **15** in the enumeration and **18** riding its *"any future"* clause. This unit
> raises none of those eighteen. **This unit still claims no check over `foundation`'s text.**
>
> **The discriminating rule — which of the two fires, and why.** This rule already drew the
> distinction; it is now named so callers can mirror it rather than guess:
>
> | Condition | Raises | Because |
> |---|---|---|
> | A `partition_id` **disagreement** — across the three confirmatory inputs, or between a frame's `spec.partition_id` and the partition being scored (R-90) | **`PartitionError`** | a **declared-identity** disagreement: two artifacts disagree about *which partition this is*. No information has moved |
> | A **training partition** where a scored one is required — `kind` names a training partition (limb 3), or `spec.role == "train"` on a scoring path (R-90) | **`PartitionError`** | the same class: the frame's **declared role** disagrees with the scoring intent. In-sample numbers, not future information |
> | A `transform_id` **disagreement, or `None`** | **`LeakageError`** | the disagreement **implies information flow**: a transform fitted on other rows has touched these, or none is recorded and the fit is unknown |
>
> **Why this does not contradict `features-and-splits` R-74.** R-74 element 2 raises `LeakageError`
> for `bundle.spec.role != "train"` and element 4 for `transform.partition_id != spec.partition_id`
> — both correct under the rule above, because both are **transform-side** conditions inside
> `fit_transforms`/`build_features`: element 2 governs which rows a transform is *fitted* on, and
> element 4 which rows a fitted transform is *applied* to. Both move information. R-90's and this
> rule's `partition_id` conditions are **frame-versus-intent** and **input-versus-input**
> disagreements at the consumer, where nothing has been fitted or applied. The two units are
> checking different things and correctly raise different types.
>
> **The cross-unit disagreement — RESOLVED, and re-verified at the close of this pass.** Mid-pass,
> `evaluation-and-comparison` **R-105 limb 2** raised `LeakageError` when comparison members disagree
> on `partition_id`, while claiming to *"mirror R-92's provenance-agreement rule … so the two
> consuming units' accounts of the eighth amendment agree"* — and they did not; `statistical-inference`
> **R-113 limb 2** imports R-105 *"as written"*, so a third unit inherited it. **R-105 has since been
> corrected in parallel and was re-read directly.** Its limb 2 now reads: *"All members of one
> comparison **agree on `partition_id`**; a mismatch **raises `PartitionError`** — **the same
> exception R-92 raises for the same condition**"*, and its limb 1 keeps `LeakageError` for an
> **absent** stamp with the ordering stated (*"Limb 1 runs **before** limb 2, so a `None`
> `partition_id` is caught here"*) — a refinement this rule accepts as consistent: an absent stamp is
> not a disagreement, and `None` is the information-flow case. **The two accounts now agree.**
>
> **The hazard this closed**, stated as R-01's rationale states its own: a test asserting
> `pytest.raises(PartitionError)` passed at `06` and failed at `07` on one logical condition.
> **This unit's text is the one R-105 mirrors, and this unit edited no sibling artifact** — the
> correction was made by that unit's own owner, in parallel, on the same owner ruling.

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
2. **`criterion_hash` / `criterion_used_hash`** — the criterion declared **before** tuning equals
   the one used. Catches a criterion changed after December was seen, which the partition record
   cannot see.
3. **`audit_access_since_declaration`**, read from `governance-guards` **R-25**'s durable access
   log: a tuning run whose record post-dates a December coverage-audit access **must state it**.
   **The join is stated, not left as an outcome** (iteration-1 finding 6): R-25's log rows carry an
   `AccessRecord` whose retrieval timestamp is `retrieved_at_utc` and whose `purpose` is one of
   `"coverage_audit" | "regime_audit" | "locked_evaluation"`; the correlation is
   `AccessRecord.retrieved_at_utc > TuningRecord.criterion_declared_at` **and**
   `AccessRecord.retrieved_at_utc < TuningRecord.run_at`, restricted to records whose `purpose` is
   **`"coverage_audit"` or `"regime_audit"`** — the two performance-blind December literals. The
   third literal, `"locked_evaluation"`, is the G-06 event and cannot legitimately precede a tuning
   run at all; an access carrying it inside the window is itself a finding, so it is **included**
   rather than filtered out.

> ⚠ **BOTH FIELD LABELS CORRECTED 2026-08-28, and the fallback withdrawn.** *(Residual carried on
> this unit's terminal READY verdict of 2026-08-24 — the `## Review — 2026-08-26 fourteenth-receipt
> confirming pass` finding 2 re-verified it unapplied and correctly carried it to the gate rather
> than applying it. Applied now under the owner's remediation authority, alongside
> `GOV-2026-08-28-FD-01` Recommendation 3, because both are the same defect class: a rule naming a
> field that does not exist on the object it reads.)*
>
> **Mechanism 2 — superseded:** *"**`criterion_declared_at` / `criterion_used_hash`**"*.
> `criterion_declared_at` is a **timestamp with no hash**, so the pair as written was not
> comparable. `domain-entities.md` § 5's authoritative table already carried this correction (its
> own post-redo finding 2 box, 2026-08-24) and pairs `criterion_used_hash` with **`criterion_hash`**;
> this rule was the one representation the 2026-08-24 fix did not reach — the recorded
> one-representation-short failure mode, for the fourth time in this unit.
>
> **Mechanism 3 — superseded:** *"`AccessRecord.timestamp > TuningRecord.criterion_declared_at`
> **and** `AccessRecord.timestamp < TuningRecord.run_at`"* and *"If `AccessRecord` carries no
> purpose field able to express that restriction, the check degrades to **any** access in the
> window."* **Found in this pass, not previously raised.** `component-methods.md:266–273` declares
> `AccessRecord` as `run_id`, `retrieved_at_utc`, `scope`, `purpose`, `performance_inspected`,
> `locked_test_accessed`, `authorization` — **seven fields, and no `timestamp`**. The retrieval
> timestamp is `retrieved_at_utc`. And `AccessRecord` **does** carry `purpose`, with the three
> literals quoted above, so the degradation fallback was **conditioned on a false premise** and is
> withdrawn rather than left standing as dead text. The join is now fully determined.
>
> **Note for Recommendation 3's reader.** This is the *only* place in this unit that consumes a
> `purpose` field, and it is the correct one: `purpose` is an `AccessRecord` field. R-90's
> superseded text borrowed that name for a `FeatureBundle`, where it never existed — the two errors
> are opposite halves of one confusion, and fixing them together is deliberate.

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
and does enforce, restated 2026-08-28 as the upstream type-closure it actually is:** a second 2022
test period is **not representable** as a `Partition`. `Partition.partition_id` is closed to the
**six** rows `features-and-splits` **R-80** fixes — `F1`, `F2`, `F3`, `F4`, `REFIT`, `DEC`
(`component-methods.md:332`, `"F1".."F4", "REFIT", "DEC"`) — so a seventh test period cannot be
constructed upstream, let alone reach `three_seed_mean`. What **this** unit's own raises then add,
per `domain-entities.md` § 3 limb 4 exactly: `PartitionError` when the three inputs **disagree** on
`partition_id`, and `PartitionError` when the named partition is a **training** partition. A second
test period could therefore not be *scored* here even if it were somehow *declared* elsewhere — but
the closure that guarantees it is **R-80's fixed list**, not a membership check this unit performs.

> ⚠ **MECHANISM RESTATED 2026-08-28 — the claim did not match this unit's own raise conditions.**
> *(Residual carried on the terminal READY verdict of 2026-08-24 and re-verified unapplied by the
> `## Review — 2026-08-26 fourteenth-receipt confirming pass`, finding 2; applied now under the
> owner's remediation authority, per `GOV-2026-08-28-FD-01`'s Discipline direction on this
> residual.)*
>
> **Superseded, preserved verbatim:** *"`domain-entities.md` § 3 limb 3 enumerates the allowed
> partitions for a confirmatory prediction, and a partition outside that enumeration raises
> **`PartitionError`** — so a second test period cannot be *scored* here even though it could be
> *declared* elsewhere."*
>
> **Why it was wrong.** Two defects, one sentence. (1) It cited **limb 3**, which is a table of
> *allowed* partitions; the raise conditions live in **limb 4**, and limb 4 names exactly **two**
> `PartitionError` triggers — cross-input `partition_id` disagreement, and a training partition.
> **There is no "outside the enumeration" trigger anywhere in this unit**, so the sentence asserted
> a check that does not exist. (2) It located the closure **locally**, as though this unit polices
> partition membership. It does not and should not: membership is fixed by R-80's six-row list and
> by `Partition.partition_id`'s own comment, one layer up. Describing an upstream type-closure as a
> local enumeration check both overstates this unit's reach and, worse, would let an implementer
> "satisfy" it by writing a membership test here while the real guarantee — that no seventh
> partition is constructible — went unasserted. **The conclusion the sentence drew was right; its
> stated mechanism was not.**

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

## R-102a — `06` writes the prediction-hash receipt, and refuses to exit without it

> **ADDED 2026-08-28** — `GOV-2026-08-28-FD-01` **Recommendation 1** (`VAL-01`, Critical, veto
> exercised), owner-approved **option 1**: assign the write to `06` in this unit. **Numbered
> `R-102a` rather than `R-103`** because the single project-wide sequence has already allocated
> R-103…R-112 to `evaluation-and-comparison`; the suffix form follows `features-and-splits`' own
> **R-76a** precedent rather than minting a collision.

**Rule.** The **one-shot `DEC` prediction write** in `06_train_and_predict.py` emits a
**`PredictionHashReceipt`** (`domain-entities.md` § 13) carrying `prediction_path`, `sha256`,
`recorded_at_utc`, `run_id` and `partition_id`. Three obligations, each executable:

1. **Hash at first write.** The `sha256` is computed over the prediction file **as written**, and
   `recorded_at_utc` is the moment of that computation — **before** any metric exists to compute.
2. **Durably flushed before `06` exits.** The receipt reaches durable storage, not a buffer the
   process holds. This mirrors `governance-guards` R-25's log-then-read ordering: an ordering
   guarantee that survives only in memory guarantees nothing across the `06` → `07` process
   boundary.
3. **Refusal to exit.** `06` **refuses to exit** with a `DEC` prediction file on disk and no
   durably-flushed receipt for it, raising **`LockedTestError`**. The check runs on `06`'s own exit
   path, so the failure is *`06` aborted*, not *`07` blocked*.

**And on the registry row.** `06`'s run row carries the receipt's `sha256` as **`prediction_hash`** —
TE §13.4's **eighteenth** column of twenty, derived by counting the fenced column list at
`Technical_Environment_and_Research_Implementation(1)(2).md:821–826` and independently confirmed by
`requirements.md` FR-P1-05-13, which enumerates *"TE §13.4's twenty columns"* by name — **joined by
`run_id`**. `foundation` **R-18** owns the row and its write-time schema assertion; this rule owns
the receipt that column 18 is populated from.

**`prior_period_exposure` on a Phase 1 row is `false`, and this rule writes no `true`.** See the
correction box below — this is a **deviation from the approved remediation text**, made because
`foundation` R-18 refuses the value the remediation named and TE §7.0B supports `foundation`.

**Negative control (the one that matters).** A `DEC` prediction file written with **no receipt**
→ **raises in `06`**, at `06`'s exit, **not later in `07`**. Also: a receipt whose `sha256` does not
match the file as written → **raises in `06`**; a receipt written but **not flushed** before exit →
**raises in `06`**.

> **`foundation` R-18 now carries the matching refusal on the registry side, verified 2026-08-28.**
> Its **W-6 step 4**: *"**Refuse a `prediction_hash` presented by the process that computes a metric
> over that prediction** (R-18). `06` writes the receipt; `07` and the bootstrap **may not**."* And
> its R-18 constraint text names `scripts/06_train_and_predict.py` as the writer with this rule's
> exact five fields and the durable flush. **The producer-side rule here and the destination-side
> refusal there interlock**: the receipt cannot be written by a metric caller, and a hash from a
> metric caller cannot be accepted onto the row. Neither half is sufficient alone — R-102a stops the
> receipt being *created* in the wrong process, R-18 stops it being *recorded* from one.
>
> **Why `07` and the bootstrap may NOT be the writer.** `evaluation-and-comparison` **R-109** limb 1
> and `statistical-inference` **R-113** limb 3 both refuse to compute a `DEC` metric unless a
> recorded receipt's `recorded_at_utc` **precedes** the metric call. If the receipt were written
> inside `07_evaluate_and_report.py` — or inside `vector_block_bootstrap` — the **same process that
> computes the metric would be the process that timestamps the receipt**, and "the receipt precedes
> the metric" becomes **self-certifying**: it would be satisfied by construction on every run,
> including a run where the prediction was regenerated after a score was seen. The control would
> pass its own test and detect nothing. Keeping writer and reader in **different processes**, with a
> file and a registry row between them, is the entire mechanism — not an implementation preference.
> This is also why obligation 3 is a refusal **to exit** rather than a refusal to score: a refusal
> to score is exactly the check `07` already owns, and duplicating it here would leave the producer
> side unguarded.
>
> **What this closes.** Three sibling artifacts state the receipt is **`06`'s act** —
> `evaluation-and-comparison` `domain-entities.md` § 5 (*"Recording the receipt is `06`'s act"*) and
> its R-109 limb 1 (*"Recording the hash is **`06`'s act**"*), and `statistical-inference` R-113 limb
> 3, which consumes it as a precondition. Derived over all **48** artifacts before this edit and
> printed rather than carried: `PredictionHashReceipt` = **0** in this unit's four files (5 hits
> total, all in the two consuming units); *"prediction hash"* = **0** here; `prediction_hash` = **0**
> and `prior_period_exposure` = **0** **across all 48**. The obligation had **two consumers and no
> producer**, so as designed **G-06 could not execute at all**: every `DEC` metric entry point would
> raise `LockedTestError` forever. That is fail-closed rather than a breach — the hazard the board
> named is the cheap repair, which is precisely the `07`-side write this rule forbids.
>
> **Whose requirement this is, stated so no coverage is claimed.** **FR-P1-05-12 belongs to
> `governance-guards`** (`unit-of-work-story-map.md:108`, with **WS-18, TA-18**), and it is the
> requirement that names *"predictions are generated and written **once**, and hashed **before** any
> metric is computed"*, the write-once re-verification criterion, and `prior_period_exposure=true`.
> This unit owns the **script that performs the act**, not the requirement or its acceptance rows.
> It is recorded here as a **produced obligation discharging a sibling's requirement** — the mirror
> of the consumed-obligation posture R-97 and R-100 take — and this unit **claims none of WS-18 or
> TA-18's coverage**. Nothing in this rule is added to this unit's own 9-requirement,
> 7-without-a-row tally.
>
> ## ⚠ DEVIATION FROM THE APPROVED REMEDIATION TEXT — `prior_period_exposure` IS `false` HERE, NOT `true`
>
> **The remediation as approved said:** *"the receipt and **`prior_period_exposure = true`** are
> written to the registry row"*. **This rule does not write `true`, and writing it would be
> refused.** Stated as a deviation rather than applied silently, and **flagged for the owner.**
>
> **Why.** `foundation`'s **R-18**, amended 2026-08-28 in parallel on the same governance report,
> carries an explicit constraint headed *"Phase 1's value of `prior_period_exposure` is `false`, and
> that is not a defect"*, and its `write_registry_event` **W-6 step 5** is a hard refusal: *"**Refuse
> `prior_period_exposure = true` on a Phase 1 row** (R-18). Phase 1 *is* the first December exposure;
> `true` belongs to the Phase 2 replication (TE §7.0B)."* R-18 names the reason for the refusal in
> terms: it exists to *"stop an implementer writing `true` on a Phase 1 row to satisfy §7.0B's *shall
> record*"* — which is precisely what the remediation text would have had this rule do.
>
> **The authority supports `foundation`, verified at source.** TE §7.0B
> (`Technical_Environment_and_Research_Implementation(1)(2).md:372`) reads: *"**The Phase 2 December
> run** is a fixed-protocol replication **because Phase 1 has already exposed December**. The
> locked-test guard shall record `prior_period_exposure=true`."* The flag asserts that **a prior
> period was already exposed**. **This unit is Phase 1** (NFR-PHASE-01), so `06`'s `DEC` run is the
> **first** exposure and the true value of the predicate is **`false`**. `true` on this row would be
> a false statement about the run, not a compliance record.
>
> **`06` is not the writer of that field at all.** R-18 also resolves the attribution this rule's
> first draft flagged as an open tension: *"`prior_period_exposure` is likewise **recorded by the
> locked-test guard** (TE §7.0B names the guard, and `governance-guards` owns it) and **carried** by
> this row. This unit is the destination, not the source."* So the field's **source is
> `governance-guards`' `locked_test.py`**, its **destination is `foundation`'s `RegistryEvent`**, and
> **this unit is neither**. R-102a therefore **claims no check over it** and writes no value —
> the same consumed-obligation posture R-97 and R-100 take. *(The first draft of this rule raised the
> attribution as owner-owned and unresolved; it is resolved, by the sibling that owns the row.)*
>
> **`prior_period_exposure` remains outside TE §13.4's twenty columns** — `prediction_hash` is column
> 18; `prior_period_exposure` is absent from the block — and `foundation` R-18 now carries it as one
> of **three named extensions** (`reason`, `prior_period_exposure`, `exploratory`) held deliberately
> outside the twenty *"so the twenty-column assertion stays literally checkable"*. **That extension
> has landed**; the draft's *"in flight in parallel"* wording is superseded.
>
> **Owner ruling requested.** If the intent of Recommendation 1's `prior_period_exposure = true`
> clause was something other than the §7.0B predicate — for instance a marker that December has been
> opened at all — then it needs a different field name, because `foundation` has built a refusal
> around this one and TE §7.0B fixes its meaning. **Nothing is assumed here either way.**
>
> **No amendment owed, and no eleventh file.** The receipt is an **intra-package `src/models` shape**
> under `component-methods.md` § Depth, written by a script already in W-11's build list, hashing via
> `src/data/release.py`'s consolidated SHA-256 helper. It changes **no approved boundary signature**:
> `fit_predict`, `three_seed_mean` and `climatology_fit_partition` are untouched. So **W-11's "Ten
> files" stands** and this unit's amendment ledger stays at **0** — see § Assumptions.
>
> **Nothing here authorises writing it.** **G-09 is not signed** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged. and **BLK-03 independently bars
> implementation.** The `DEC` write this rule governs is additionally barred until **G-05 is
> signed**, by `features-and-splits`' locked-partition execution guard (R-82) and
> `governance-guards`' access chokepoint.

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

- **[assumption]** Rule IDs continue the single sequence, so this unit runs **R-90…R-102**, **plus `R-102a`** added 2026-08-28 (Recommendation 1). **14 rule headings**, derived by counting `^## R-` in this file before asserting. `R-102a` takes the suffix form rather than `R-103`, which `evaluation-and-comparison` already holds; the precedent is `features-and-splits`' own **R-76a**. If per-unit numbering was intended, say so at the gate and the artifacts restart.
- **[assumption]** The **story map governs** where it and `unit-of-work.md` § 8 disagree. Neither is edited by this stage.
- **[assumption]** `src/models/*` shapes beyond the named boundary calls are **intra-package** and this stage's to specify (`component-methods.md` § Depth). **R-90's match function is one of them**, and so is **R-102a's `PredictionHashReceipt`**, so this unit owes **no** amendment; `domain-entities.md` § 6 declined the option that would have made it nine. ⚠ **The figure this line carried — "the total stays 8 across 5 units" — is SUPERSEDED; see the dated box immediately below.** The live chain total is **7 across 5 units**, and **this unit's own contribution is 0 either way**, which is the part of the claim that was never in doubt.

  > ⚠ **AMENDMENT TOTAL ANNOTATED IN PLACE, 2026-08-28 — the superseded figure is preserved above,
  > not deleted.** *(`GOV-2026-08-28-FD-01` **Recommendation 32** — `CHAIR-07`, Medium; owner-approved
  > **option 1**, annotate in place. Pattern per `governance/CHANGE_RECORD_PROCEDURE.md` and
  > `external-products`' precedent; obligation per `project.md` dp-1, learned 2026-08-24.)*
  >
  > **Superseded figure, preserved:** *"the total stays **8 across 5 units**"*, stated here as a
  > live, unqualified `[assumption]`.
  >
  > **Why it went stale — the basis moved, not the arithmetic.** "8 across 5" rested on
  > `external-products` R-55's **5** plus `features-and-splits`' **3**. On **2026-08-26**
  > `features-and-splits` **rebuilt its artifacts onto ADR-11** and **re-derived its own contribution
  > from 3 to 0** — *"its three dissolved into ADR-11"* — which moved the base from 8-across-5 to
  > **5 across 3**. Nothing this unit wrote became wrong; the number it quoted did.
  >
  > **Re-derived, not decremented. Printed before asserted, term by term, each read at its own unit's
  > § Amendments owed:**
  >
  > | Unit | Owed | Running total | Read at |
  > |---|---|---|---|
  > | `external-products` (R-55 basis: `acquisition` 3 + `inventory-and-registry` 1 + `external-products` 1) | **5** | **5 across 3** | `external-products/business-rules.md:184` |
  > | `features-and-splits` | **0** | 5 across 3 | `features-and-splits/business-rules.md:799` (re-derived 2026-08-26) |
  > | `evaluation-and-comparison` (R-103, the BLK-08 package) | **+1** | **6 across 4** | `evaluation-and-comparison/business-rules.md:423` |
  > | `statistical-inference` (R-118 signature amendment) | **+1** | **7 across 5** | `statistical-inference/business-rules.md:401` |
  > | `regimes-diagnostics-reporting` | **0** | 7 across 5 | `regimes-diagnostics-reporting/business-rules.md:435` |
  > | `fixtures-and-reproducibility` | **0** | **7 across 5** | `fixtures-and-reproducibility/business-rules.md:612` |
  > | **This unit** | **0** | **7 across 5 units** | here — R-90's match function and R-102a's receipt are both intra-package |
  >
  > `5 + 0 + 1 + 1 + 0 + 0 + 0 = 7`, across `acquisition`, `inventory-and-registry`,
  > `external-products`, `evaluation-and-comparison`, `statistical-inference` = **5 units**.
  >
  > ⚠ **A correction to the remediation brief, stated rather than absorbed.** The brief and
  > Recommendation 32's evidence line both give the chain as ending **"8 across 6"** at
  > `fixtures-and-reproducibility`. **That unit's live total is 7 across 5**, printed at its
  > `business-rules.md:602` and `:612`. Its four "8 across 6" mentions are all one explicitly
  > **labelled conditional** — *"One honest conditional… If the gate places the manifest loader in
  > `foundation`'s `src/data/` as a cross-unit contract… the ledger takes **+1, to 8 across 6, at
  > that ruling** — counted **then, not now**"* (its R-133). Reading a labelled conditional as a live
  > total is the same class of error this box exists to fix, so the chain is recorded here as
  > terminating at **7 across 5**, with a **conditional +1 → 8 across 6** contingent on an
  > **unmade owner ruling** on R-133's loader home. Derived by scanning **797** Markdown files across
  > the workspace (excluding `.git/`, `node_modules/` and `graphify-out/`) for `across N units` and
  > for the literal `8 across 6`; every hit was read in context before this table was written.
  >
  > **The board's unclassified "8 across 6" in THIS unit, now classified.** It occurs **exactly
  > once** here: `business-logic-model.md:345`, inside the preserved
  > `## Review` iteration-1 findings table, in the reviewer's own remediation text — *"the '8 across
  > 5 units' total may need revisiting once that unit's own 3.1 design lands (it may turn out to be
  > 8 across 6, or a ninth landing site, depending on how `07` implements it)"*. It is a
  > **conditional forward reference**, not a typo and not a third basis — and it was **prescient**:
  > `evaluation-and-comparison`'s design did land and did add +1. It needs **no fix**, and it gets
  > none: it sits inside a `## Review` section preserved byte-for-byte, and it is a true statement
  > about the future made at its own date.
  >
  > **Two siblings raised this figure and correctly declined to edit it** —
  > `features-and-splits/business-logic-model.md:1129–1130` and
  > `evaluation-and-comparison/business-rules.md:435–436` — because these artifacts were
  > terminal-READY under a frozen receipt. Their restraint was right; the residual dp-1 names is that
  > **the consuming line itself carried no marker**. It does now.
  >
  > **Not swept, and outside this remediation's edit scope:** `functional-design-questions.md` still
  > carries the literal "8 across 5" at **6** sites — `:53`, `:207`, `:274`, `:302`, `:342`, `:393`.
  > That file is expressly excluded from this remediation. **Reported at the gate.**
  >
  > ⚠ **This figure was first written here as "4 sites (`:53`, `:274`, `:302`, `:393`)" and corrected
  > to 6 in the same pass, before the file was finalized.** The wrong count came from a regex keyed to
  > the shape `N across M units`, which structurally cannot see `:207` (*"taking the running total
  > from 8 across 5 to 9"*) or `:342` (*"stays at 8 across 5, Q6 = C…"*) — both of which drop the word
  > *units*. Recorded rather than silently fixed because it is a live instance of `project.md`
  > § Way of Working's rule that a count must be derived from the artifact and printed, and of its
  > companion warning that a sweep keyed to one form of a figure is blind to the others: **the second
  > derivation, on the bare literal, found 50% more sites than the first.** The two extra sites are
  > also the two most consequential in that file — `:207` reasons *from* the total to a conditional
  > ninth amendment, and `:342` is the recorded `> **💡 Recommendation**:` line whose stated ground
  > includes the figure.
- **Open — BLK-03's contract limbs are an EXIT condition** on this unit and three downstream units. **Approving this design is not the contract's approval.**
- **Open — BLK-04 ↓ and BLK-09 ↓**, inherited and not closed.
- **Open — R-90's match function is a cross-unit contract surface.** `features-and-splits`' `tests/test_train_only_transforms.py` asserts against it; neither unit owns it alone.
- **Open — 7 of 9 requirements have no acceptance row**: FR-P1-04-14, FR-P1-05-3, -4, -5, -6, -21, -22. Four name their own candidate TA row via **Vision §15.2**. **None is added here.**
- **Open — whether TA-11 reaches a model fit is unverified upstream** (R-98). No reading adopted.
- **Closed, corrected 2026-08-24 — D-122's supervisor sign-off is NOT outstanding.** The first draft carried *"Approved — supervisor sign-off pending"*, which is the status of **D-126** and **D-128**, not D-122. The Vision decision register (line 1207) reads **"Approved; supervisor sign-off closed 2026-08-22"** by the project owner under the recorded student/supervisor authority equivalence (`CR-2026-08-22-TE-AMEND`; `GOV-2026-08-22-REM-01` Rec 4), noting that **no supervisor signature artifact exists and none is claimed** and that the seed values were verified unchanged before closure. `unit-of-work.md` § 8 already recorded the closure. **Found while verifying iteration-1 finding 1 against the source register; the reviewer did not raise it.**
- **Open — FR-P1-05-4's residual**: a choice informed by a December figure a human carries in their head is unreachable by any mechanism (R-95). Narrowed by the audit-access precondition, not eliminated.
- **G-09 is not signed** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged., and **BLK-03 independently bars implementation.** No rule here authorises creating `src/models/persistence.py`, `climatology.py`, `ridge.py`, `random_forest.py`, `lstm.py`, `train.py`, `checkpoint.py`, `scripts/06_train_and_predict.py`, `tests/test_models_smoke.py` or `tests/test_checkpoint_restore.py`.
- ~~**Open — `07`'s half of the eighth amendment is UNOWNED.**~~ **CLOSED 2026-08-28.** *(Superseded text preserved:* "FU-4 = D names **`06` and `07`**; `unit-of-work.md` assigns `07_evaluate_and_report.py` to **`evaluation-and-comparison`**, whose functional design has not run. This unit discharges `06` only. Raised at the gate so it is not discovered later *(iteration-1 finding 3)*." *)* That unit's design **has** since run and its **R-105** claims `07`'s half explicitly, citing R-90 by name; `statistical-inference` R-113 limb 2 then imports it. See R-90's 2026-08-28 closure box. **One live disagreement survives the closure**: R-105 limb 2 raises `LeakageError` for the `partition_id`-mismatch condition it says mirrors R-92, which raises `PartitionError`. Recorded next.
- **CLOSED 2026-08-28 — `PartitionError` is the fifteenth project exception, and `foundation` R-01's amendment HAS LANDED** (R-92's box; Recommendation 8, owner-ruled option 1). Re-read directly at the close of this pass: R-01 names **fifteen**, adds `PartitionError` (`models-and-baselines`, declared in `src/models/`), restates its count as **derived** rather than asserted, and cites **this unit's § 12 as the authority for the fifteenth entry**. *(Mid-pass it still read "All fourteen"; the draft's "in flight" wording is superseded and recorded, not left standing.)* Derived here before this edit: **10 of 12 units**, **71** occurrences across all **48** artifacts, **23** of them here — the largest share of any unit. **This unit still claims no check over `foundation`'s text.**
- **CLOSED 2026-08-28 — the R-105 / R-92 exception-type disagreement is resolved BY THE SIBLING.** R-105 limb 2 now raises **`PartitionError`**, *"the same exception R-92 raises for the same condition"*, with limb 1 keeping `LeakageError` for an **absent** stamp and stating that limb 1 runs first — a refinement R-92 accepts, since an absent stamp is not a disagreement. `statistical-inference` R-113 limb 2, which imports R-105 *"as written"*, inherits the fix. **This unit edited no sibling artifact.**
- ⚠ **DEVIATION FROM THE APPROVED REMEDIATION TEXT, and the one item needing an owner ruling: `prior_period_exposure` is `false` on a Phase 1 row, so R-102a writes no `true`.** The remediation said *"`prior_period_exposure = true`"*; `foundation` **R-18** / **W-6 step 5** **refuses `true` on a Phase 1 row**, and TE §7.0B (`:372`) supports it — the flag asserts *"Phase 1 has already exposed December"*, which is a **Phase 2** predicate, and this unit is Phase 1 (NFR-PHASE-01). R-18 also resolves the attribution: the field's **source is `governance-guards`' locked-test guard**, its **destination is `foundation`'s registry row**, and **this unit is neither** — so R-102a claims no check over it. See R-102a's deviation box. **If Recommendation 1 meant a different predicate, it needs a different field name; nothing is assumed.**
- **CLOSED 2026-08-28 — the registry side of R-102a has landed and interlocks with it.** `foundation` **R-18** carries TE §13.4's twenty columns with `prediction_hash` at **column 18**, names `scripts/06_train_and_predict.py` as the receipt's writer with this rule's exact five fields and durable flush, and its **W-6 step 4 refuses a `prediction_hash` presented by the metric-computing process**. `prior_period_exposure` is held there as one of **three named extensions** outside the twenty *"so the twenty-column assertion stays literally checkable"*. The draft's *"in flight in parallel"* wording for that extension is superseded.
- **Open — R-102a discharges a requirement this unit does not own.** **FR-P1-05-12 belongs to `governance-guards`** (`unit-of-work-story-map.md:108`; **WS-18, TA-18**). This unit owns the script performing the act. **No WS-18 or TA-18 coverage is claimed**, and the 9-requirement / 7-without-a-row tally below is unchanged by R-102a.
- **Applied 2026-08-28 — the two residuals that rode the terminal READY are now RESOLVED, not carried.** R-96's `PartitionError` mechanism is restated as `features-and-splits` **R-80**'s upstream six-row type-closure (the local "outside that enumeration" check it claimed **does not exist** in this unit); R-95 mechanism 2's field pair is corrected to `criterion_hash` / `criterion_used_hash`. **Applied rather than carried** because the redo jump cleared the receipt floor and the owner directed both at the remediation. **A third, previously unraised defect was found in the same sweep and fixed:** R-95 mechanism 3 read `AccessRecord.timestamp`, and `AccessRecord` has **seven** fields, none named `timestamp` (`component-methods.md:266–273`); its retrieval field is `retrieved_at_utc`. The mechanism's `purpose`-absence fallback was **conditioned on a false premise** — `AccessRecord` does carry `purpose` — and is withdrawn.
- **Open — `requirements.md` FR-P1-05-2 carries TWO superseded clauses on one line, both reported and neither edited.** (a) It attributes bootstrap seed **20221201** to D-122, a reading `unit-of-work.md` § 8 records as corrected 2026-08-22 (`GOV-2026-08-22-UG-02` Rec 11) — the seed is frozen separately by **TE §13.6 / TC-19** (Q-27). (b) It states *"Vision §14.2 marks it 'Approved — supervisor sign-off pending'… still owes a signature at G-05"*, superseded by the same Vision-register closure at line 1207 that these artifacts cite correctly elsewhere — **"Approved; supervisor sign-off closed 2026-08-22"**. This unit follows the **corrected** reading of both. `requirements.md` is an approved upstream artifact and `CHANGE_RECORD_PROCEDURE.md` bars editing one absent owner approval for annotate-in-place, so both are **raised at the gate**. *(Clause (a) was iteration-1 finding 5; clause (b) is iteration-2 finding 2 — flagging one clause of a line and missing its neighbour is the same one-representation-short failure as iteration-2 finding 1, and clause (b) is where this author's own D-122 error originated.)*
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

---

> **Re-saved unchanged 2026-08-26 under the fourteenth-redo re-confirmation receipt** (redo taken
> for `external-products`; floor reset mechanical). **No rule here changed.** **G-09 remains
> unsigned, and BLK-03 independently bars implementation.**

> ## ⚠ AMENDED 2026-08-28 — `GOV-2026-08-28-FD-01` REMEDIATION (verdict FAIL)
>
> A redo jump cleared the write-freeze so the owner-approved remediations on this unit could be
> applied. **Four items, each carrying its own dated box at the point of change:**
>
> | Item | Recommendation | Where |
> |---|---|---|
> | The leakage guard rewritten onto ADR-11's live `FeatureBundle` contract | **3** (`IMPL-01`, Critical, **veto**) | **R-90** — rule, controls, and the `fit_predict` vocabulary note |
> | `06` named as the prediction-hash receipt's writer, with refusal-to-exit | **1** (`VAL-01`, Critical, **veto**) | **R-102a** (new); `domain-entities.md` § 13 |
> | `PartitionError` promoted to the fifteenth exception, with the discriminating rule | **8** (`CHAIR-05`/`ML-05`/`IMPL-02`, High) | **R-92**; `domain-entities.md` § 12 |
> | The stale amendment total annotated in place | **32** (`CHAIR-07`, Medium) | § Assumptions & Open Questions |
>
> **Also applied in the same sweep, from this unit's own carried residuals:** R-96's
> `PartitionError` mechanism restated as R-80's upstream type-closure; R-95 mechanism 2's field pair
> corrected; and R-95 mechanism 3's non-existent `AccessRecord.timestamp` field and its
> false-premise fallback fixed — **the third of those was not previously raised by any reviewer.**
>
> **What has NOT changed.** No scientific value, grid, seed, threshold or frozen constant. No
> approved boundary signature — `fit_predict`, `three_seed_mean` and `climatology_fit_partition` are
> untouched, and this unit still owes **0** amendments. No sibling artifact and no
> `functional-design-questions.md` was edited. Every prior `## Review` section and every dated
> ⚠ box is preserved.
>
> **BLK-03 remains an open exit condition and G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged. Nothing above authorises
> creating a module, and nothing above closes BLK-03.**

---

> **Re-confirmation receipt, 2026-08-29 — `models-and-baselines`.** The 2026-08-27T21:49:36Z REDO jump reset every unit's
> receipt floor, and this unit's content had already changed after that floor under the 2026-08-28
> post-execution pass (D-29 through D-32; **G-09 signed under D-31 with its TE §18.3 preconditions
> disclosed unmet**). The owner re-confirmed that post-execution content via the Consolidated
> Summary Confirmation at the foot of `functional-design-questions.md`, receipted `2026-08-29`.
> **No line above this marker was touched by this pass**, no count was re-derived, and nothing here
> discharges TA-15, WS-18 or TA-18, creates `aws_ai_dlc_preflight_report`, or alters the fact that
> stage 3.1 remains **FAIL** with no board having passed it.
