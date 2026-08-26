# Functional Design Questions — `models-and-baselines`

**Unit** `models-and-baselines` — the six model families, training orchestration, the
three-seed confirmatory prediction, checkpointing, and the predeclared ablations.
**Kind** `library` · **Complexity** L · **Deployment** standalone · **Depends on**
`features-and-splits`.

Unit **8 of 12**, and the first with **no artifacts from any previous attempt** — units 1–7
carried forward and were re-confirmed; this one is designed from its contracts.

**Nothing here decides a scientific value.** The seed set, the grids, the LSTM training
settings, the selection criterion and the ablation registry are all **frozen upstream** — by
**D-121**, **D-122**, Vision §8.6, §8.7 and TE §7.2 — and this stage does not reopen any of
them. Every question below is about **mechanism**: what a contract's types are, where a check
runs, what a record contains, what fails.

**Two blockers are live on this unit, and one of them is an exit condition on this stage.**

- **BLK-03** — the confirmatory-prediction contract. Its **seed-value limb closed 2026-08-22**
  (D-122, values verified unchanged: development seed **42**, final seeds **{1337, 2024, 7}**);
  its **mechanism limb closed 2026-08-23** (`three_seed_mean` gained
  `expected_seeds: frozenset[int]`). **The contract limbs — input and output types, alignment
  requirements, allowed partitions, failure conditions — are open, and authoring them is this
  stage's job.** Approval authority: `functional-design` (3.1). **No affected unit may complete
  or exit 3.1 without it**, and three downstream units inherit it:
  `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`.
- **BLK-04 ↓** and **BLK-09 ↓**, inherited from `features-and-splits` — the transform fit this
  unit trains on, and the training range that fit compares against, which no field states.

**What arrived in this unit's inbox two hours before this file was written.**
`features-and-splits` answered **FU-4 = D** on 2026-08-24, which requires every emitted feature
artifact to carry a `fold_id`/`purpose`/`transform_id` **provenance stamp** and requires
**`06_train_and_predict.py` — a module this unit owns — to refuse a frame whose stamp is not
`(fold k, evaluate)` when scoring fold *k*'s validation month**. That is a requirement written
into this unit's design before this unit designed. It is **Question 1**, raised rather than
absorbed silently.

**The bolded requirement counts, derived by reading the rows rather than carried from prose:**
**9** requirements carried, **7** with no §16/§19 acceptance row (FR-P1-04-14, FR-P1-05-3,
FR-P1-05-4, FR-P1-05-5, FR-P1-05-6, FR-P1-05-21, FR-P1-05-22). **Owns** WS-14, WS-15, TA-12,
TA-13, TA-26. **Supports** TA-20.

**G-09 is not signed.** `src/models/` does not exist, nor does `src/`, `configs/` or `tests/`
beyond three modules. Naming a module here is not authority to write one.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 8 — the `Owns` list, the boundary, the 9 requirements, BLK-03's full register entry with its closed and open limbs, and the six implementation notes.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2 plus § Per-unit coverage summary. **Derived by reading the rows:** 9 requirements, **7** with no acceptance row; **owns** WS-14, WS-15, TA-12, TA-13, TA-26; **supports** TA-20. § Cross-unit responsibilities carries the REQ-ENG-5 and NFR-DET-01/TA-13/TA-26 crossings.
- `../../../inception/requirements-analysis/requirements.md` — FR-P1-04-14; FR-P1-05-1 through -6; FR-P1-05-21; FR-P1-05-22. Read in full, including each `UNTESTED` note, which is where four of this unit's mechanism questions come from.
- `../../../inception/application-design/component-methods.md` § `src/models` — the approved contracts: `Prediction` (with `partition_id` and `transform_id`, added 2026-08-23 under ADR-11), `fit_predict(model_id, *, bundle, partition, snapshot)`, `three_seed_mean(predictions, *, expected_seeds)`, `climatology_fit_partition(prediction)`, and `Transform.inverse(frame)`.
- `../../../inception/application-design/services.md` § The nine stage scripts — `06_train_and_predict.py`, its reads and writes; § Stage entry contract; § Execution platforms.
- `../features-and-splits/functional-design/` — **W-4a** (the provenance stamp), **W-4b** (read-versus-emit rows), **R-74**'s pairing control, **R-81**, and § Amendments owed at **8 across 5 units**, the fifth being this unit's `06` and `07`. Answered **FU-4 = D**, **FU-5 = D**, **FU-6 = A** on 2026-08-24.
- `../foundation/functional-design/` — `ConfigSnapshot` (the source of `expected_seeds`), the `IntegrityError` base, the two-tier error posture, and the stage entry contract.
- `evidence/DECISIONS.md` — **D-121** (the grids), **D-122** (the seed set, closed 2026-08-22 under the recorded student/supervisor authority equivalence).
- Workspace inspection, 2026-08-24: `src/`, `configs/` and `src/models/` **absent**; `tests/` holds `test_acquisition_window.py`, `test_phase_boundary.py`, `test_release_hashes.py` — none of them this unit's.
- Absent by scope design: `stories` (2.4 `SKIP`), `mockups` (1.6 and 2.5 `SKIP`). `kind: library`, so `frontend-components.md` is not produced.

---

## Question 1

`features-and-splits`' **FU-4 = D** requires `06_train_and_predict.py` — this unit's module — to
**refuse** a feature frame whose provenance stamp is not `(fold k, evaluate)` when scoring fold
*k*'s validation month. `fit_predict` already **raises `LeakageError`** when
`bundle.transform_id is None`, and `Prediction` already carries `partition_id` and
`transform_id`. What does this unit commit to, and where does the refusal live?

A) **`fit_predict` refuses; the stamp check joins its existing `transform_id is None` raise**
   > **Impact**: one raise site, already established, and the check sits where the bundle is first consumed. But `fit_predict` is a **training** call — it does not know whether the caller is about to score fold *k*'s validation month, so it can only check that the stamp is *present and internally consistent*, not that it *matches the scoring intent*. Half the requirement lands; the other half has nowhere to go.

B) **`06`'s orchestration refuses, and `fit_predict` keeps only its `transform_id is None` raise**
   > **Impact**: the script knows what it is about to score, so the full `(fold k, evaluate)` match is checkable there. Puts a governed check in a **stage script** rather than in `src/`, which sits awkwardly against §7's rule that reusable logic lives in `src/` and scripts orchestrate — the check would be orchestration-level policy, not reusable logic.

C) **A named function in `src/models/train.py` performs the match; `06` calls it before every scoring path**
   > **Impact**: the logic is reusable and testable in `src/`, the script stays an orchestrator, and `tests/test_train_only_transforms.py` — owned by `features-and-splits` — can call the same function directly rather than replaying a script. Costs one more named symbol in this unit's `Owns` list, and that symbol is a **cross-unit contract surface** since `features-and-splits`' test asserts against it.

D) **Option C, and the refusal is stated as a rule of this unit with its own negative control**
   > **Impact**: everything in C, plus this unit's `business-rules.md` carries the refusal as a numbered rule with the control — a frame stamped `(fold 4, train)` reaching fold 4's validation scoring **fails**; an **unstamped** frame reaching any scoring path **fails** — so the obligation is visible in the artifact a builder of *this* unit reads, not only in the sibling that requested it. Also records that this is the **eighth amendment**'s landing site, so the two units' accounts of it agree.

X) **Other (please specify)**
   > **Impact**: Depends on your specific choice. Any option must say **where** the `(fold k, evaluate)` match runs, since `fit_predict` alone cannot know the scoring intent.

> **💡 Recommendation**: **Option D** — C is the only placement that satisfies §7's `src/`-versus-scripts separation *and* gives `features-and-splits`' manifest-based test something to call, and D adds the part that keeps the two units from drifting: the obligation written as a rule with a control in the unit that must honour it. `project.md` § Way of Working requires exactly this — sweeping every *representation* of a fact, not only the artifact that first stated it.

[Answer]: D
## Question 2

**BLK-03's open contract limbs.** The seed values and the `expected_seeds` parameter are
settled; what is not is the **contract** — input and output types, alignment requirements,
allowed partitions, and failure conditions — which three downstream units inherit. What does
this stage author?

A) **Restate the approved signatures and their raises, and call the contract discharged**
   > **Impact**: cheapest, and everything restated would be true. But BLK-03's register entry names four limbs, and *"allowed partitions"* and *"alignment requirements"* are not stated by any approved signature — `three_seed_mean` raises `AlignmentError` on a non-identical index without saying what the index **is**, and nothing says which partitions a confirmatory prediction may be built from. Restating would leave the blocker's own words unanswered while marking it closed.

B) **A contract section fixing all four limbs, with the frozen set arriving as a parameter**
   > **Impact**: input is `Sequence[Prediction]` of exactly three, one per seed in `expected_seeds`, read from `ConfigSnapshot.seeds`; output is a `Prediction` with `seed = None` and the three inputs preserved by the caller; the alignment key is named explicitly; allowed partitions are enumerated; failure conditions are `SeedError` and `AlignmentError` with their exact triggers. Closes what the register asked for. Does **not** close BLK-03 — approval is the human's, at the gate.

C) **Option B, plus the downstream consumption contract the three inheriting units need**
   > **Impact**: B, and additionally what a consumer may rely on — that `partition_id` and `transform_id` travel on the mean, that the three individual predictions remain available, and that a single-seed prediction is never substitutable. The three downstream units then cite one contract instead of each re-deriving it. More text now; removes three chances to drift later.

D) **Option C, and the mean's own provenance stamp is stated explicitly**
   > **Impact**: C, plus the rule that the element-wise mean carries the **same** `partition_id` and `transform_id` as its three inputs and **fails** if they disagree — which is the natural extension of Question 1's stamp obligation to the artifact `07` actually scores. Without it the stamp travels to `06` and dies there, which is the exact failure `component-methods.md` cites as the reason `Prediction` gained the two fields.

X) **Other (please specify)**
   > **Impact**: Depends on your specific choice. Any option must address all four limbs the register names, since a partially-answered exit condition reads as closed.

> **💡 Recommendation**: **Option D** — the register names four limbs and D is the only option that answers all four *and* keeps the provenance chain unbroken through the one artifact three downstream units consume. `component-methods.md`'s own words are that the stamp *"has to travel the whole way, not just to the first consumer"*; the mean is where "the whole way" is either honoured or lost.

[Answer]: D
## Question 3

**FR-P1-05-4 has no acceptance row, and `requirements.md` explains why: its trigger is
December being *seen*, not the locked test being opened.** WS-18 tests the open-channel only,
which a performance-blind coverage audit passes by construction. How does this unit make
*"tuning used January–November only"* checkable?

A) **A tuning record listing the partitions each tuning run read, asserted to exclude December**
   > **Impact**: mechanical and falsifiable — the record names partitions, the check reads it. Its weakness is honest: it proves no December **partition** was read, not that no December-derived **number** informed a choice. A human who looked at a December coverage figure and then narrowed a grid leaves no trace in it.

B) **A declared-before-tuning criterion hash, compared against the criterion actually used**
   > **Impact**: this is FR-P1-04-14's mechanism, and it catches the case A misses — a criterion changed after December was seen fails the comparison. But it says nothing about grid ranges or feature choices, which FR-P1-05-5 covers separately, so alone it under-covers this requirement.

C) **Both: the partition record and the pre-tuning declaration, with the residual named**
   > **Impact**: covers both channels a mechanism can reach, and states plainly what neither reaches — a choice informed by a December figure a human carries in their head. Naming that residual is what keeps the requirement from being reported as fully tested when it is not. Costs a candidate TA row still being owed via Vision §15.2.

D) **Option C, and the December coverage audit's own performance-blindness recorded as this unit's precondition**
   > **Impact**: C, plus this unit's rules record that the required pre-G-05 December audit is **performance-blind** and that any tuning run whose record post-dates an audit access must state it. Ties the residual to the one place it is reachable — the audit access log — rather than leaving it as an unmitigated gap. Costs a dependency on `governance-guards`' access record, which exists (R-25's durable log).

X) **Other (please specify)**
   > **Impact**: Depends on your specific choice. Any option must state what it does **not** reach, since `requirements.md` already records that no existing row tests this requirement's actual trigger.

> **💡 Recommendation**: **Option D** — C is the honest floor and D adds the one thing that narrows the residual instead of merely disclosing it. `project.md` § Way of Working requires the inputs a gating condition depends on to be specified in the stage that records the condition; the audit access log is that input, and it already exists.

[Answer]: D
## Question 4

**FR-P1-05-5 requires the grid *content* asserted, not just its immutability** —
*"ridge 6, RF 18, LSTM 16"* combinations (D-121) with Vision §8.6's fixed LSTM settings
(dropout 0.2, Adam, MSE loss, max 100 epochs, early-stopping patience 10 on validation RMSE,
minimum improvement 1e-4 TECU, best-checkpoint restoration). `requirements.md` names the reason:
provenance and immutability alone would let a 40-combination LSTM grid pass. Where does the
assertion live, and against what?

A) **A test asserting the grid cardinalities — 6, 18, 16 — read from `experiment.yaml`**
   > **Impact**: simple and catches the 40-combination case. But cardinality is not content: a 16-member LSTM grid with the wrong members passes, and `requirements.md` warns against exactly this shape of check when it says provenance and immutability *"let a grid pass with none of the specified members in it"*.

B) **A test asserting grid membership element-by-element against `experiment.yaml`**
   > **Impact**: catches wrong members. But it needs the expected membership written somewhere to compare against — and if that somewhere is the test file, the frozen values now live in **source**, which TC-03e and `project.md` § Forbidden prohibit outright.

C) **Membership asserted against `experiment.yaml`, with the frozen expectation also in configuration**
   > **Impact**: the expectation lives in config beside the grid — never in source — and the test compares the two, so a drifted grid fails and no scientific constant is inlined. Requires the design to say **which** config field holds the expectation and how it differs from the grid itself, or the check becomes a tautology comparing a value to itself.

D) **Option C, with the expectation held as the G-05 frozen hash rather than a duplicate list**
   > **Impact**: the grid lives once in `experiment.yaml`; what is frozen and compared is its **hash**, committed before G-05, plus the cardinalities and the seven named LSTM settings asserted individually as the falsifiable content check `requirements.md` asks for. No duplicated list to drift, no constant in source, and the post-G-05 diff-empty check becomes the same mechanism rather than a second one.

X) **Other (please specify)**
   > **Impact**: Depends on your specific choice. Any option must avoid both failure modes named upstream — a constant inlined in source, and a check that cardinality alone can satisfy.

> **💡 Recommendation**: **Option D** — C is correct but invites the tautology it warns of; D avoids duplicating the frozen list at all by making the hash the frozen object, while still asserting the content `requirements.md` insists be falsifiable *"without a second lookup"*. It also unifies FR-P1-05-5's two halves — content and immutability — into one mechanism.

[Answer]: D
## Question 5

**FR-P1-05-6's ablation registry is five named runs** — `ABL-NODOY`, `ABL-DIFF`, `ABL-NOSW`,
`ABL-HIST48`, `ABL-ZENITH` — and `ABL-ZENITH` is **deferred to Phase 2** because it varies an
aggregation choice that does not exist on the Phase 1 target. `ABL-DIFF` must inverse-transform
to absolute TECU before any metric, via `Transform.inverse`. What does this unit's design fix?

A) **Four Phase 1 registry rows, with `ABL-ZENITH` recorded as a phase deferral**
   > **Impact**: matches the requirement exactly and keeps the count honest — five named, four reachable here. Says nothing about `ABL-HIST48`'s ordering constraint or `ABL-DIFF`'s inverse, both of which are mechanism this stage owns.

B) **Option A, plus `ABL-HIST48`'s ordering and `ABL-DIFF`'s inverse-transform stated as rules**
   > **Impact**: A, and `ABL-HIST48` runs only after the primary configuration is frozen (checkable against the G-05 frozen hash from Question 4), and `ABL-DIFF` calls `Transform.inverse` before any metric — which needs `transform_id` present on the `Prediction`, tying it to Question 2. Covers the mechanism; still silent on promotion.

C) **Option B, plus the no-promotion rule and its check**
   > **Impact**: B, and TE §7.2's *"no ablation configuration may be promoted to primary once the locked test is opened"* becomes checkable — the reported primary configuration's hash equals the one frozen at G-05, which `requirements.md` names as the criterion. Also carries Vision §2.4's bar on any secondary result replacing the primary conclusion, which reaches the reporting unit rather than this one and is therefore recorded as a **consumed** obligation, not a claimed check.

D) **Option C, with a missing-required-ablation negative control**
   > **Impact**: C, plus the control `requirements.md` asks for in terms — a missing required ablation **fails the check rather than passing unnoticed** — and its mirror, an ablation registered **after** results are seen fails. Matches this project's mandated practice that every hard rule gets a test proving the violation is caught, not only that the happy path works.

X) **Other (please specify)**
   > **Impact**: Depends on your specific choice. Any option must keep `ABL-ZENITH` counted as one of five while unreachable in Phase 1, since dropping it to four would understate the registry.

> **💡 Recommendation**: **Option D** — `team.md` § Testing Posture makes negative controls this project's actual methodology, and D is the only option carrying one. It also keeps the five-versus-four distinction explicit, which is the kind of count this stage has already had to correct four times elsewhere.

[Answer]: D
## Question 6

**FR-P1-05-21 — M-03's fitting partition.** `climatology_fit_partition(prediction)` returns the
partition identifiers M-03 was actually fitted on, *"so the negative case — a climatology fitted
across all of 2022 — **fails** a test rather than passing a module inventory."* The requirement
is `UNTESTED`, and `requirements.md` records that whether TA-11's *"train-only transforms"*
reaches a **model fit** is **unverified** and must not be claimed. What does this unit specify?

A) **A record of the fitted partitions, asserted to be training partitions only**
   > **Impact**: directly what the approved signature returns, and directly what the requirement asks. It does not address the unverified TA-11 reading, which stays open either way.

B) **Option A, with the negative control the requirement names**
   > **Impact**: A, plus an M-03 fitted across all of 2022 **fails** — the exact case the requirement says must fail rather than pass a module inventory. This is the same negative-control practice as Question 5.

C) **Option B, and the TA-11 question raised at the gate rather than resolved here**
   > **Impact**: B, and this unit's artifacts state plainly that whether TA-11 covers a model fit is **unverified upstream**, adopt no reading, and carry it to the gate — where confirming the reading or adding a row runs through Vision §15.2. Keeps this stage from silently inheriting an acceptance row it has no authority to claim.

D) **Option C, and the fitted-partition record stamped onto the `Prediction` itself**
   > **Impact**: C, plus M-03's `Prediction` carries its fitting partitions so the check reads an artifact rather than re-deriving from a call. Attractive symmetry with Question 1's stamp — but `Prediction`'s field set is an **approved boundary contract**, so this would be a **further amendment**, taking the running total from 8 across 5 to 9, and `climatology_fit_partition` already exists precisely to answer this without one.

X) **Other (please specify)**
   > **Impact**: Depends on your specific choice. Any option must not claim TA-11 as coverage, since `requirements.md` records that reading as unverified.

> **💡 Recommendation**: **Option C** — B is the substance and C adds the discipline this project has repeatedly needed: adopt no reading on an upstream ambiguity, and say so at the gate. D is the tempting one to refuse — it pays a ninth amendment for something the approved `climatology_fit_partition` already delivers.

[Answer]: C
## Question 7

**FR-P1-05-22 — the +24 h horizon must be implemented and testable but excluded from the
default run list, and *"building the +24 h label must require no code change, only a config
change."*** The requirement is `UNTESTED` and names its own criterion: a test builds the +24 h
label **from configuration alone**. How is that made real?

A) **`experiment.yaml` exposes `horizons: [1]` with 24 available; a test asserts the exposure**
   > **Impact**: satisfies the config-shape half. But asserting that `24` is *available* is not asserting that building it needs no code change — a path that raises `NotImplementedError` for horizon 24 would pass this.

B) **A test that builds the +24 h label by changing only configuration, and asserts it succeeds**
   > **Impact**: tests the actual obligation — the one TE §2.1 states — and fails a +1 h-only implementation. Needs the design to say what "builds the label" means concretely at fixture scale, or the test has no defined success condition.

C) **Option B, with the horizon carried as a parameter through the training path**
   > **Impact**: B, and the design states that horizon flows from `ConfigSnapshot` through `fit_predict`'s `snapshot` parameter to the label construction, so no code path branches on a literal `1`. Makes the requirement structural rather than test-enforced only — which is the same *"structural rather than asserted"* posture `features-and-splits` uses for window parity.

D) **Option C, plus a negative control on a hardcoded horizon**
   > **Impact**: C, plus a control: a code path that branches on a literal horizon value **fails** a static check, in the manner `governance-guards` uses for the restricted-root literal. Catches the regression that would silently reintroduce a +1 h-only path after the test was written.

X) **Other (please specify)**
   > **Impact**: Depends on your specific choice. Any option must test that building +24 h needs **no code change**, not merely that configuration mentions it.

> **💡 Recommendation**: **Option D** — the requirement's stated failure mode is *"a +24 h path that requires a code edit fails"*, and only C and D reach it structurally; D adds the static control that keeps it reached. The static-check pattern is already established in this project by `governance-guards` R-28 and `features-and-splits` R-76a's third limb.

[Answer]: D
## Question 8

**FR-P1-05-3 — no Random Forest importance score may add, remove or rank a feature into the
production feature set.** The stated criterion is that *"the feature manifest's provenance shows
no importance-derived selection"* — but the **feature manifest belongs to `features-and-splits`,
not to this unit.** What does this unit commit to, given it cannot check another unit's artifact?

A) **A rule that RF importance is saved only as a non-authoritative diagnostic figure**
   > **Impact**: states the prohibition where the importance is actually computed, which is this unit. It does not produce the evidence the requirement names, and does not say what "non-authoritative" is enforced by.

B) **Option A, with the diagnostic artifact marked non-authoritative in its own metadata**
   > **Impact**: A, plus the figure carries a recorded flag saying it is diagnostic, so a downstream consumer treating it as a selection input is doing so against a stated marker rather than an unstated convention. Still no cross-unit check.

C) **Option B, and the manifest-provenance obligation recorded as a consumed cross-unit dependency**
   > **Impact**: B, and this unit's artifacts state that the requirement's **evidence** lives in `features-and-splits`' feature manifest, name it as a consumed dependency, and claim no check over it. Honest about the split and leaves a named seam rather than a silent gap — the same posture `features-and-splits` took toward `inventory-and-registry`'s station registry.

D) **Option C, plus a negative control this unit can actually run**
   > **Impact**: C, plus a control inside this unit's reach: an importance score reaching the **production feature path** — as opposed to the diagnostic artifact — **fails**. The check is on this unit's own module graph, not on a sibling's manifest, so it is enforceable here while the manifest evidence stays the sibling's.

X) **Other (please specify)**
   > **Impact**: Depends on your specific choice. Any option must not claim a check over an artifact this unit does not own.

> **💡 Recommendation**: **Option D** — C is the honest description of the split and D adds the one control this unit can enforce without reaching into a sibling. Claiming the manifest check here would be the mistake: `project.md` records that this project has already had one unit claim a sibling's coverage row and have it corrected.

[Answer]: D
---

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence — `foundation` R-01…R-17, `governance-guards` R-18…R-29, `acquisition` R-30…R-43, `inventory-and-registry` R-44…R-53, `external-products` R-54…R-63, `target-standardization` R-64…R-73, `features-and-splits` R-74…R-8x — so this unit opens at the next free number. If per-unit numbering was intended, say so at the gate and the artifacts restart.
- **[assumption]** The **story map governs** where it and `unit-of-work.md` § 8 disagree, consistent with every sibling unit's treatment. Neither artifact is edited by this stage.
- **[assumption]** `src/models/*` shapes beyond the named boundary calls are **intra-package** and this stage's to specify (`component-methods.md` § Depth). Whether Question 1's named match function and Question 2's contract additions cross that boundary is **decided by those answers**, and § Amendments owed will be derived from them rather than assumed.
- **Open — BLK-03's contract limbs are an EXIT condition on this stage**, and on `evaluation-and-comparison`, `statistical-inference` and `regimes-diagnostics-reporting`. **Approving this design is not the contract's approval.**
- **Open — BLK-04 ↓ and BLK-09 ↓ are inherited from `features-and-splits`** — the transform fit this unit trains on, and the training range that fit compares against. `features-and-splits` supplied their mechanism on 2026-08-24 (FU-4/5/6) but **neither blocker is closed**.
- **Open — the eighth amendment lands here.** `features-and-splits`' FU-4 = D requires `06`/`07` to refuse a mismatched provenance stamp. This unit owns `06`. Question 1 decides how; the amendment total of **8 across 5 units** already counts it.
- **Open — 7 of this unit's 9 requirements have no §16/§19 acceptance row**: FR-P1-04-14, FR-P1-05-3, FR-P1-05-4, FR-P1-05-5, FR-P1-05-6, FR-P1-05-21, FR-P1-05-22. Four of them name their own candidate TA row via Vision §15.2; none is added by this stage.
- **Open — whether TA-11's "train-only transforms" reaches a model fit is unverified upstream.** `requirements.md` records it as unverified; this stage adopts no reading (Question 6).
- **Open — FR-P1-04-14's selection protocol has no acceptance row.** Mean per-fold skill score across F1–F4; raw mean RMSE and row-count weighting both barred; the declared baseline named in configuration before tuning; ties under 1% resolved to the **simpler** configuration; refit on January–November **without changing any hyperparameter**. Its two mechanical comparisons are stated by the requirement and are carried into the artifacts; the missing row goes to the gate.
- **Open — D-122's signature.** The seed values are frozen for implementation and their **authority** was closed 2026-08-22 under the recorded student/supervisor equivalence, but Vision §14.2 marks D-122 *"Approved — supervisor sign-off pending"*, so a signature is still owed at **G-05**.
- **G-09 is not signed.** No answer here authorises creating `src/models/persistence.py`, `climatology.py`, `ridge.py`, `random_forest.py`, `lstm.py`, `train.py`, `checkpoint.py`, `scripts/06_train_and_predict.py`, `tests/test_models_smoke.py` or `tests/test_checkpoint_restore.py`. **BLK-03 independently bars implementation.**
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant. The seed set, the grids, the LSTM settings, the selection criterion and the ablation registry are all frozen upstream and are **restated, never chosen, here**.

---

## Consolidated Summary Confirmation

All eight questions were answered on **2026-08-24** — **D, D, D, D, D, C, D, D** — on the
owner's instruction to apply the recommendations. Consolidated:

| Q | Answer | What it settles |
|---|---|---|
| 1 | **D** | The stamp refusal is a **named function in `src/models/train.py`**, called by `06` before every scoring path — reusable and testable in `src/` per §7, and callable directly by `features-and-splits`' manifest-based `test_train_only_transforms.py`. Stated as a numbered rule of this unit **with its own negative controls**: a frame stamped `(fold 4, train)` reaching fold 4's validation scoring **fails**; an **unstamped** frame reaching any scoring path **fails**. Recorded as the **eighth amendment's landing site**, so both units' accounts agree |
| 2 | **D** | **BLK-03's four contract limbs authored**: input `Sequence[Prediction]` of exactly three, one per seed in `expected_seeds` read from `ConfigSnapshot.seeds`; output a `Prediction` with `seed = None`, the three inputs preserved by the caller; the alignment key named explicitly; allowed partitions enumerated; failure conditions `SeedError` and `AlignmentError` with exact triggers. Plus the **downstream consumption contract** the three inheriting units cite, and the rule that the mean carries the **same** `partition_id` and `transform_id` as its inputs and **fails** if they disagree — so the stamp travels *"the whole way"* rather than dying at `06` |
| 3 | **D** | FR-P1-05-4 gets **both reachable mechanisms** — a tuning record naming the partitions each run read, and a criterion declared before tuning compared against the one used — with the residual **named**: a choice informed by a December figure a human carries in their head. Narrowed, not merely disclosed, by making an audit-access precondition of any tuning run whose record post-dates a December coverage-audit access, against `governance-guards` **R-25**'s durable log |
| 4 | **D** | The **G-05 frozen hash is the frozen object** — the grid lives once in `experiment.yaml`, no duplicated list to drift, no constant in source — with the cardinalities (**ridge 6, RF 18, LSTM 16**) and the **seven named LSTM settings** asserted individually as the falsifiable content check. FR-P1-05-5's two halves, content and immutability, become one mechanism |
| 5 | **D** | **Four Phase 1 ablation rows** plus `ABL-ZENITH`'s **phase deferral** (five named, four reachable — the count stays honest); `ABL-HIST48` runs only after the primary configuration is frozen, checkable against Q4's hash; `ABL-DIFF` calls `Transform.inverse` before any metric, which needs `transform_id` on the `Prediction` and so ties to Q2; the **no-promotion** rule checked as reported-primary-hash = G-05-frozen-hash, with Vision §2.4's bar recorded as a **consumed** obligation of the reporting unit rather than a claimed check here; and the negative controls — a **missing** required ablation **fails**, an ablation registered **after results are seen fails** |
| 6 | **C** | M-03's fitted-partition record via `climatology_fit_partition`, asserted training-partitions-only, **with the negative control** the requirement names — a climatology fitted across all of 2022 **fails**. **No reading adopted** on whether TA-11's *"train-only transforms"* reaches a model fit; `requirements.md` records that as unverified, and confirming it or adding a row runs through **Vision §15.2** at the gate. **Option D was declined**: stamping fitted partitions onto `Prediction` would pay a **ninth** amendment for what the approved `climatology_fit_partition` already delivers |
| 7 | **D** | Horizon flows from `ConfigSnapshot` through `fit_predict`'s `snapshot` parameter to label construction, so **no code path branches on a literal `1`** — structural rather than test-enforced only — plus a **static check** that a code path branching on a literal horizon **fails**, in the pattern `governance-guards` R-28 and `features-and-splits` R-76a's third limb already use. `experiment.yaml` exposes `horizons: [1]` with `24` available and absent from the default run list |
| 8 | **D** | RF importance is **diagnostic-only** by rule, the diagnostic artifact carries a **non-authoritative** marker in its own metadata, the feature manifest's provenance evidence is recorded as a **consumed cross-unit dependency** of `features-and-splits` with **no check claimed over it**, and the one control this unit can enforce is stated: an importance score reaching the **production feature path** **fails**, checked on this unit's own module graph |

### What these answers cost, derived rather than carried

**§ Amendments owed stays at 8 across 5 units.** Q1 = D lands the eighth amendment — it does
not add a ninth, because the named match function lives in `src/models/train.py`, an
**intra-package** shape this stage may specify under `component-methods.md` § Depth, and the
stamp fields themselves were already counted by `features-and-splits`. Q6 = D was **declined
precisely to avoid a ninth**. Q2 = D's contract additions describe the approved
`three_seed_mean` and `Prediction` rather than changing either signature.

**One new cross-unit contract surface**, named rather than left implicit: the match function
Q1 = D creates is asserted against by `features-and-splits`' `test_train_only_transforms.py`,
so it is a surface two units depend on and neither owns alone.

### What is carried to the gate, unchanged by these answers

**BLK-03's contract limbs are an EXIT condition on this stage** and on
`evaluation-and-comparison`, `statistical-inference` and `regimes-diagnostics-reporting`.
**Authoring the contract is not approving it** — that is the human's, at the gate.
**BLK-04 ↓ and BLK-09 ↓** inherited from `features-and-splits`, neither closed by its 2026-08-24
answers. **7 of 9 requirements have no §16/§19 acceptance row**, four naming their own candidate
TA row via Vision §15.2, none added here. **FR-P1-04-14's selection protocol** — mean per-fold
skill score across F1–F4, raw mean RMSE and row-count weighting both barred, the declared
baseline named in configuration before tuning, ties under **1%** resolved to the **simpler**
configuration, refit on January–November **without changing any hyperparameter** — carried into
the artifacts with its missing row reported. **Whether TA-11 reaches a model fit: unverified
upstream, no reading adopted.** **D-122's supervisor signature still owed at G-05**, Vision §14.2
marking it *"Approved — supervisor sign-off pending"*. **G-09 unsigned**, and **BLK-03
independently bars implementation** — nothing here authorises creating any of this unit's ten
named files.

**No answer decides a scientific constant.** The seed set, the grids, the seven LSTM settings,
the selection criterion and the ablation registry are frozen upstream and are **restated here,
never chosen**.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The receipt is recorded for `models-and-baselines` and its three artifacts are generated against these eight answers, then put through an adversarial reviewer pass. BLK-03's contract is authored, not approved — it goes to the gate.

- Request changes
   > **Impact**: No receipt and no artifacts. Tell me what to change — any of the eight answers, the derived amendment total, or the reading of BLK-03's four limbs — and I re-present first.

> **💡 Recommendation**: **Looks correct** — the eight answers are mechanism only, the amendment total was re-derived rather than carried and stays at 8 across 5, Q6 = C declines the one option that would have added a ninth for no gain, and every frozen scientific value is restated from its upstream decision rather than chosen here.

*(Answered `Looks correct` earlier on 2026-08-24, before the artifacts were reviewed. That receipt
was reset by the redo jump taken for this unit's own benefit. The live answer tag for this section
is the blank one at its end.)*

### Re-confirmation, 2026-08-24 (post-redo) — the unit the redo was taken for

**Why this is being re-asked, and unlike the seven siblings it is not merely mechanical.** The
first artifact set was reviewed adversarially, reached **NOT-READY** with the 2-iteration budget
spent, and the write-freeze on a terminal receipt made a redo the only route to a fix. The project
decision owner authorised a redo jump on `functional-design` at **2026-08-24T14:57:07Z**. **This
unit's content then changed** — twice.

### The four reviewer passes, and what each changed

| Pass | Verdict | What it found, and what was done |
|---|---|---|
| **Iteration 1** | NOT-READY | 2 Critical, 3 Major, 1 Minor. The Critical *"D-121/D-122 do not exist"* was **disputed and partly rejected on evidence**: both exist in the **Vision** decision register (lines 1206–1207), Approved; `evidence/DECISIONS.md` is a separate register running D-1…D-27. The real defect was **citing the wrong file**, corrected in all three artifacts. The sibling-test mischaracterisation, the `06`/`07` conflation, the "Two mechanisms" count and the unswept `requirements.md` clause were all accepted and fixed |
| **Iteration 2** | NOT-READY | Budget exhausted. Three new findings, two of them **fixes that stopped one representation short** — a § Amendments owed paragraph still asserting the superseded claim 20 lines below its own correction, and a second stale clause on the same `requirements.md` line as the one already flagged. This is the failure mode `project.md` records twice |
| **Post-redo, iteration 1** | NOT-READY | All three redo fixes verified to hold with **no regression**. Three **fresh** Major findings in places the earlier passes had not reached: § 11's negative-control list missing one control and the whole must-not-fire control; `criterion_used_hash` pointing at a **timestamp** field rather than `criterion_hash`; and R-96 mechanising one of its two prohibitions with neither a check nor a disclaimer for the other |
| **Post-redo, iteration 2** | **READY** | All three fixes verified from source. R-96's new ownership claim was **checked against primary sources rather than trusted** — D-8 read directly, and `features-and-splits` R-80 confirmed as owner of the closed six-row partition list. Every count re-derived independently with no drift |

### One error the reviewer never raised, found while checking its Critical

Verifying finding 1 against the Vision register turned up a **second author error**: all three
artifacts had said D-122's supervisor signature was *"still owed at G-05"*. Line 1207 reads
**"Approved; supervisor sign-off closed 2026-08-22"** — by the project owner under the recorded
student/supervisor authority equivalence, with the explicit note that **no supervisor signature
artifact exists and none is claimed**. *"Approved — supervisor sign-off pending"* is **D-126's and
D-128's** status. Corrected in all three artifacts and recorded as found-outside-the-review.

### Two residuals ride the READY verdict, and are NOT applied

Per the rule that a suggestion riding a READY verdict is **gate input, never an edit**:

| Severity | Residual |
|---|---|
| **Major** | R-96's closing sentence says `domain-entities.md` § 3 limb 3/4 raises `PartitionError` for *"a partition outside that enumeration"*, but limb 4's two stated conditions — cross-input disagreement, or a training partition — do not literally cover an **unrecognised** partition value. The real safeguard is upstream **type-closure** (`features-and-splits` R-80 fixing `partition_id` to six values), which R-96 never names as the mechanism |
| **Minor** | R-95's mechanism 2 still labels the pair `criterion_declared_at`/`criterion_used_hash` rather than `criterion_hash`/`criterion_used_hash`. Non-blocking: the authoritative entity table is correct |

**Neither was fixed**, deliberately. Both go to the stage gate for your ruling.

### What still stands, unchanged by any of it

**BLK-03's contract limbs are an EXIT condition** on this unit and on `evaluation-and-comparison`,
`statistical-inference` and `regimes-diagnostics-reporting`. `domain-entities.md` § 3 **authors**
the contract; **approving it is yours, at the gate**. **BLK-04 ↓ and BLK-09 ↓** inherited and not
closed. **`07`'s half of the eighth amendment is unowned** — it belongs to
`evaluation-and-comparison`, whose design has not run. **7 of 9 requirements have no acceptance
row.** **TA-11's reach into a model fit stays unverified**, no reading adopted. **G-09 unsigned**,
and **BLK-03 independently bars implementation**. **Amendments owed: 8 across 5 units**, nothing
added here.

Does this all look correct before the stage proceeds?

- Looks correct
   > **Impact**: The receipt is recorded for `models-and-baselines` under the post-redo floor and its three artifacts are re-saved. The READY verdict stands and the two residuals travel to the stage gate as input for your ruling.

- Request changes
   > **Impact**: No receipt is recorded and nothing is re-saved. Use this to challenge any of the four passes' dispositions, to direct that either residual be applied now rather than at the gate, or to reopen one of the eight answers.

> **💡 Recommendation**: **Looks correct** — the redo achieved what it was authorised for, the disputed Critical was resolved on evidence rather than accepted, one author error the review missed was found and corrected, and the two residuals are left for your ruling rather than quietly applied.

*(Receipt reset by the fourteenth authorised redo, 2026-08-26T08:18:34Z. The live answer tag is the blank one below.)*

### Re-confirmation, 2026-08-26 — under the fourteenth-redo floor

**Nothing in this unit changed** since its terminal READY (2026-08-24T15:15:00Z, post-redo iteration 2). Derived this pass: **13 rules** (`R-90`…`R-102`), **11 workflows**, **12 entities**, **8 questions** all answered, zero mojibake. The two residuals riding that READY — **R-96’s `PartitionError` mechanism** (§3 limb 4 weaker than claimed) and **R-95’s field label** (looser prose than the entity table) — remain carried to the stage gate as input, not applied. Floor reset by the fourteenth redo.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: Receipt recorded, artifacts re-saved natively, narrow confirming review runs.

- Request changes
   > **Impact**: Nothing recorded; tell me what to change.

> **💡 Recommendation**: **Looks correct** — mechanical: this unit is untouched and its terminal READY adjudicated content already.

[Answer]: Looks correct
