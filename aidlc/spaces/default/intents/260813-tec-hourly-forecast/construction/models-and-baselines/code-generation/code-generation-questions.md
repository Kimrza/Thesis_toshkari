# Code Generation Questions — `models-and-baselines`

**Unit** `models-and-baselines` (Bolt 8) · **Kind** `library` · **Stage** `code-generation`

This unit is barred by **BLK-03**, an open exit condition: the confirmatory-prediction
contract (`domain-entities.md` § 3's four limbs; R-91, R-92, R-93) was authored at
functional-design and never separately approved — every artifact repeats "authoring is not
approving." Its inherited blockers BLK-04 and BLK-09 were approved on 2026-09-05 at the
`features-and-splits` pass (`governance/CHANGE_RECORD_2026-09-05_R74_R83_leakage_contracts.md`),
so the transform this unit trains on and the training range it compares against now exist as
governed contracts. Two governed pins are also unresolved and bite here specifically: the
**TensorFlow pin** is `TBD — freeze gate` (TS-M-01; TE §8.1 freezes it only after fixture runs),
and **`scikit-learn` carries no pin at all** in `requirements.txt` although TS-M-03 requires it
for M-04/M-05. TE §18.3's stop-and-report rule is why the five items below are questions rather
than defaults.

**Recorded input (human ruling, 2026-09-05)**: this unit's terminal READY nfr-design review
(2026-09-04 iteration 2, re-affirmed 2026-09-05) carries **no Minor findings** ("Findings:
None"); the earlier passes' Majors (attestation field group not in `domain-entities.md` § 5;
D-121/D-122 attribution; D-122 status quote) were fixed before the terminal verdict. Nothing to
list as record-only; stated so the plan's "Recorded input" line is not mistaken for an omission.

---

## Question 1
**BLK-03** — approve the confirmatory-prediction contract as the governed cross-unit contract:
`domain-entities.md` § 3's four limbs (input: exactly three M-06 `Prediction`s whose seeds equal
`expected_seeds` read from `ConfigSnapshot.seeds`; output: a `Prediction` with `seed = None`,
element-wise mean on the shared index, provenance copied; allowed partitions: F1–F4 validation
months, the January–November refit, December only through the locked-partition guard, a training
partition refused; failure conditions: `SeedError` / `AlignmentError` on the ordered
(`station`, `interval_start_utc`) index / `PartitionError` / `LeakageError`), the five-point
downstream consumption contract, and R-91/R-92/R-93 — recorded as a change record in
`governance/` before any module is written?

A) Approve now — change record written FIRST; implementation of this unit proceeds under it
   > **Impact**: Unblocks this unit and the three downstream units (evaluation-and-comparison, statistical-inference, regimes-diagnostics-reporting) whose designs cite this contract rather than re-derive it. The seed VALUES are already closed (D-122); this approves the mechanism's contract, not new science.

B) Defer — the unit stays barred; skip its code generation this Bolt
   > **Impact**: `src/models/train.py`'s confirmatory path and everything downstream stay unbuildable; the Bolt ends at seven of twelve units.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the contract survived the functional-design review cycles and an adversarial nfr-design pass; the register names 3.1 as its authoring authority and the owner as its approver, which is this ruling. Honestly stated: this is the change-control acceptance the register requires, and the record must exist before any commit.

[Answer]: A

## Question 2
**The TensorFlow pin is `TBD — freeze gate`** (TS-M-01). M-06's serialization contract,
checkpoint format and determinism settings are version-dependent, and TE §8.1 freezes the exact
pin only after the fixture runs on Kaggle and local — so no implementer may fill it now. What
does this run build for M-06?

A) Build everything that does not depend on the pin; M-06 refuses fail-closed — `lstm.py` and `checkpoint.py` are written with NO `tensorflow` import at module scope: the LSTM fit path raises naming the unfrozen pin (TE §18.3), while the version-agnostic parts are real and tested (grid enumeration against D-121's 16 combinations and the seven §8.6 settings from config; lowest-validation-RMSE checkpoint SELECTION and restore logic over a recorded epoch history, exercised in `test_checkpoint_restore.py` through a backend-neutral interface with a fake backend; the frozen-settings assertion)
   > **Impact**: M-01…M-05, `train.py` (stamp match, three-seed mean, tuning with the unconditional attestation), `06` and both mandated test modules are all real; only the Keras model construction and its serialized checkpoint bytes wait for the pin. WS-14/WS-15/TA-13/TA-26 stay `Pending` either way. When the pin freezes, one module gains its backend and the tests gain the real-checkpoint cases.

B) Freeze the TensorFlow pin now at TE §8.1's candidate 2.21.0 under a new D-number and build M-06 fully
   > **Impact**: Contradicts TE §8.1's own sequencing (pin frozen after fixture runs) and Vision §1.2 / TE §1.1 (no implementer fills a `TBD — freeze gate` value); the fixtures cannot run here (PyPI unreachable, no TensorFlow installable), so the freeze would rest on no measurement. Not recommended.

C) Defer the whole unit until the pin is frozen
   > **Impact**: Five families that need no TensorFlow, the confirmatory mean, the stamp match and `06`'s receipt mechanism all wait on one unrelated pin; three downstream units stay blocked with them.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the same fail-closed-at-the-unfrozen-value posture every prior unit took (the permitted-producer refusal, the calendar-value refusal); the refusal is the deliverable for M-06's fit path, and everything version-independent is built and tested now.

[Answer]: B

## Question 3
**`scikit-learn` has no pin in `requirements.txt`** although TS-M-03 requires it for M-04 Ridge
and M-05 Random Forest, and `requirements.txt` is the single governed pin surface whose hash
enters every run's environment lock (TE §13.1). This is an engineering pin, not a scientific
value — foundation pinned numpy 1.26.4 / pandas 2.1.4 / pyyaml 6.0.1 the same way — but it is a
change to a governed artifact. How is it handled?

A) Add `scikit-learn==1.4.2` to `requirements.txt` now (a release supporting Python 3.11 and numpy 1.26), recorded in this unit's change record; `ridge.py` / `random_forest.py` import it lazily and refuse with a message naming the pin if it is absent at run time
   > **Impact**: The pin surface is complete for the five non-TensorFlow families; the environment-lock hash changes once, cited in the record. Honestly stated: PyPI is unreachable on this machine, so the pin cannot be installed or exercised here — the sklearn-backed paths are written and their refusal is tested, but M-04/M-05 fits remain unrun until the pins are installable (smoke evidence only either way).

B) Leave `requirements.txt` untouched; `ridge.py` / `random_forest.py` import lazily and refuse naming the MISSING pin; the pin lands later under a separate ruling
   > **Impact**: No governed-artifact change this pass, but two mandated families cannot run anywhere until a second ruling adds the pin, and the environment lock's completeness claim (TE §13.1) stays false for this unit.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the pin is engineering, its precedent is foundation's own pins, and leaving it open buys nothing but a second ruling. If you prefer a different version, name it under X.

[Answer]: A

## Question 4
**`Transform.inverse` does not exist.** `domain-entities.md` § 3's consumption contract (point 5)
and `component-methods.md` name `Transform.inverse(frame)` as the only route from model output
back to absolute TECU, but `features-and-splits` built `Transform` with NO inverse path (its
Q4 = A; BLK-08 deferred under D-27, narrowed to `ABL-DIFF`). This unit's only inverse consumer is
the `ABL-DIFF` ablation. Confirm: this run registers all five ablations as named entries read
from `experiment.yaml` (R-97) and `ABL-DIFF` refuses to run — naming the absent inverse and D-27 —
while the other three Phase-1-reachable ablations are runnable?

A) Confirm — `ABL-DIFF` is a predeclared entry with a fail-closed refusal; no inverse is built here and no `src/evaluation` → `src/features` edge is added
   > **Impact**: Consistent with D-27's explicit withholding and the never-reopen-a-refusal rule; `ABL-HIST48` additionally refuses until the primary configuration is frozen (R-97). The inverse lands at evaluation-and-comparison's pass or a later change record, as already recorded.

B) Build the inverse in this unit now
   > **Impact**: Directly contradicts D-27's recorded withholding and puts a `src/features` shape's method in `src/models`; would need an explicit reversal argument. Not recommended.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — D-27 already ruled and features-and-splits' pass honoured it; nothing new argues for reopening it here.

[Answer]: B

## Question 5
**Grid and LSTM-setting transcription into `configs/experiment.yaml`.** `grids` and `models`
are `TBD — freeze gate` today. Vision §14.2 records **D-121 (status: Approved)** — "Exact frozen
grids: ridge 6, RF 18, LSTM 16 combinations, with fixed training settings" — and Vision §8.6
states the exact contents: Ridge `alpha ∈ {0.01, 0.1, 1, 10, 100, 1000}`; RF `n_estimators ∈
{300, 600}` × `max_depth ∈ {8, 16, None}` × `min_samples_leaf ∈ {1, 5, 20}`, `max_features =
sqrt`; LSTM `layers ∈ {1, 2}` × `units ∈ {32, 64}` × `learning_rate ∈ {1e-3, 3e-4}` ×
`batch_size ∈ {64, 256}`; fixed LSTM settings dropout 0.2, Adam, MSE, max 100 epochs,
early-stopping patience 10 on validation RMSE, min-improvement 1e-4 TECU, best-checkpoint restore.
`configs/data.yaml`'s own rule is "only values frozen under an approved D-number are transcribed
here, citing that D-number." Transcribe now?

A) Transcribe exactly the D-121 / Vision §8.6 text into `experiment.yaml` (`grids`, `models.lstm_fixed_settings`), citing D-121 and §8.6 line-for-line; the code asserts grid CONTENT against config (R-96) and never holds a grid value in source; everything §8.6 does not fix stays `TBD — freeze gate`
   > **Impact**: R-96's content assertion and W-6's grid freeze become executable against real config; the grid hash committed before G-05 has a subject. Transcription changes no value — a copy of an approved decision under its D-number is the `seeds.yaml` precedent. Any drift between the transcription and §8.6 is caught by a test that re-reads the counts 6/18/16 from config.

B) Leave `grids` / `models` as `TBD — freeze gate`; the code refuses at every grid read; transcription waits for a separate freeze act
   > **Impact**: Mirrors features-and-splits' calendar-value deferral, but that deferral had no D-number behind the values; D-121 is Approved. Every grid-dependent test would have only a refusal to assert until the later act.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — D-121 is an approved decision with its contents fixed in the governing document; transcribing it with its citation is exactly what `seeds.yaml` did for D-122, and it is what makes R-96 testable. Honestly stated: the transcription is a copy, and the copy's exactness is the only thing this pass asserts about it.

[Answer]: A

---

## Follow-up questions — contradictions in the Q2 and Q4 answers

Two answers contradict recorded rules, so neither is acted on until resolved here (stage
protocol § 3, contradiction detection; project.md § Way of Working: a recorded refusal is not
reopened without a new argument or an explicit decision that honours the original reasoning).

## Follow-up 1 (Q2 = B)
You chose **"Freeze TF 2.21.0 now"**. Side by side with the record: Vision §1.2 / TE §1.1 —
*"No implementer or coding agent may fill such a value by convenience"*; values marked
`TBD — freeze gate` need explicit student-and-supervisor approval before dependent work begins.
TE §8.1 sequences the TensorFlow pin freeze **after** the Kaggle and local fixture runs, and no
fixture can run here (PyPI unreachable; TensorFlow not installable). D-122 was closed under the
recorded student/supervisor authority equivalence (`CR-2026-08-22-TE-AMEND`), so an owner
freeze is procedurally possible — but it would also deviate from TE §8.1's sequencing and would
rest on no measurement. Which path?

A) Return to Q2 = A — fail-closed M-06 (no `tensorflow` import; fit path refuses naming the unfrozen pin; grid enumeration, checkpoint selection/restore logic and the seven-settings assertion real and tested through a fake backend)
   > **Impact**: Nothing is filled by convenience; TE §8.1's sequencing stands; the refusal is the deliverable for M-06's fit path, as for every other unfrozen value in this project. The Keras model itself lands when the pin is frozen after the fixture runs.

B) Freeze the pin yourself, first: you write a new D-number in `evidence/DECISIONS.md` freezing `tensorflow==2.21.0`, invoking the authority equivalence and recording the deviation from TE §8.1's after-fixtures sequencing with your rationale; only then does the developer add the pin to `requirements.txt` (cited by that D-number) and build M-06 against the tf.keras 2.21 API — with the honest limit that no TensorFlow code can be executed on this machine, so every M-06 path is written-but-unexecuted and TA-26 stays `Pending`
   > **Impact**: M-06 code exists in full, but unrun; the freeze is an owner act with a recorded deviation, not an agent act. If a later fixture run shows 2.21.0 lacks a deterministic kernel this project needs, the freeze must be reopened under a further D-number — the risk TE §8.1's ordering exists to avoid.

C) Write M-06 against the tf.keras API of the 2.21.0 candidate now, but keep the pin `TBD — freeze gate`: the Keras construction lives behind a guard that refuses unless `requirements.txt` carries a frozen `tensorflow==` pin, and the import happens only inside that guarded path
   > **Impact**: No governed value is filled; more M-06 code exists than under A, but code written against an unfrozen API version may need rework when the pin lands, and none of it can be executed here either. The version-agnostic parts are tested exactly as under A.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it is the only path that fills nothing and deviates from nothing, and M-06's unexecutable code buys no evidence today. If you want the Keras code on disk regardless, C keeps the pin unfrozen; B is procedurally yours to take but should be a deliberate, recorded deviation, not a side effect of a plan question.

[Answer]: C

## Follow-up 2 (Q4 = B)
You chose **"Build the inverse here"**. Side by side with the record: **D-27** withheld the
inverse mechanism and stated *"no import-boundary change is authorised by this decision"*;
features-and-splits' code-generation Q4 = A (receipted 2026-09-06) confirmed that deferral and
built `Transform` with no inverse; project.md forbids reopening a recorded refusal *"merely
because the material it refused is now within reach"* — reversal needs a new argument or an
explicit human decision that honours the original reasoning. Also: the inverse is a method on
`Transform`, which lives in `src/features/transforms.py` — **features-and-splits' module, not
this unit's** — and the R-84 / R-103 naming divergence (`load_inverse`/`Inverse` vs
`load_transform`/`Transform`) is still open. Which path?

A) Return to Q4 = A — `ABL-DIFF` registered from `experiment.yaml` and refusing, naming the absent inverse and D-27; no inverse built; no edge added
   > **Impact**: D-27 stands as recorded; the inverse lands at evaluation-and-comparison's pass or a later change record, where its owner and naming are settled together.

B) Reopen D-27 explicitly, first: you record a new D-number reversing the withholding, stating the new argument and honouring D-27's reasoning; then the developer adds `Transform.inverse(frame)` to `src/features/transforms.py` (a sibling unit's module, edited in place under your instruction and flagged for features-and-splits' record), keeps the import graph unchanged (the method travels with `transform_id`; no `src/evaluation` → `src/features` import), and makes `ABL-DIFF` runnable through it; the R-84/R-103 naming divergence is resolved in the same D-number
   > **Impact**: `ABL-DIFF` becomes executable and the consumption contract's point 5 becomes true; cost is an owner decision reversing a recorded one, a cross-unit edit to a module whose unit was reviewed READY this morning, and a naming ruling taken here rather than at evaluation-and-comparison's pass.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — no new argument for the inverse has appeared since D-27, and `ABL-DIFF` is an ablation that is not on Bolt 8's path; if you do want it now, B makes the reversal yours and recorded, which is the only form the never-reopen rule allows.

[Answer]: B

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Q1 = A — **BLK-03 contract approved**: `domain-entities.md` § 3's four limbs, the five-point consumption contract and R-91/R-92/R-93 become the governed cross-unit contract. Change record written to `governance/` FIRST, before any module.
- Q2 = B superseded by **Follow-up 1 = C** — the TensorFlow pin stays `TBD — freeze gate`; NOTHING is frozen. M-06 is written against the tf.keras 2.21.0 candidate API, but the Keras construction and every `tensorflow` import live behind a guard that refuses unless `requirements.txt` carries a frozen `tensorflow==` pin; the guard's refusal is tested; the version-agnostic parts (grid enumeration from config, lowest-validation-RMSE checkpoint selection and restore over a recorded epoch history through a backend-neutral interface, the seven-settings assertion) are real and tested with a fake backend. Honest limit: no TensorFlow code can execute on this machine or anywhere until the pin is frozen; TA-26 stays `Pending`; the Keras code may need rework when the pin lands.
- Q3 = A — **`scikit-learn==1.4.2` added to `requirements.txt`**, cited in the change record; `ridge.py` / `random_forest.py` import lazily and refuse naming the pin if absent. Cannot be installed here (PyPI unreachable), so M-04/M-05 fits stay unrun; refusal paths tested.
- Q4 = B superseded by **Follow-up 2 = B** — **you reopen D-27 first**: a new D-number in `evidence/DECISIONS.md`, written by you, reversing the inverse withholding with a stated new argument that honours D-27's reasoning, and settling the R-84/R-103 naming (`Transform.inverse(frame)` as `component-methods.md` names it, unless you rule otherwise). The change record carries a proposed text for that D-number for you to adopt or edit. **The inverse step is gated on that D-number existing on disk when the developer reaches it**: if present, `Transform.inverse(frame)` is added to `src/features/transforms.py` (features-and-splits' module, edited in place, flagged for that unit's record and re-check), the import graph stays unchanged (no `src/evaluation` → `src/features` import), and `ABL-DIFF` becomes runnable through it; if absent, the developer stops at that step and reports, and `ABL-DIFF` refuses naming D-27 exactly as under Q4 = A. Nothing else in the plan waits on it.
- Q5 = A — **D-121 grids and Vision §8.6's seven fixed LSTM settings transcribed** into `configs/experiment.yaml` (`grids`, `models.lstm_fixed_settings`) verbatim, citing D-121 / §8.6; a test re-reads the counts 6 / 18 / 16 from config; no grid value in source (R-96 content assertion against config).
- Build set: `src/models/{persistence,climatology,ridge,random_forest,lstm,train,checkpoint}.py`, `scripts/06_train_and_predict.py`, `tests/test_models_smoke.py`, `tests/test_checkpoint_restore.py` (W-11's ten files, plus `Transform.inverse` in the sibling module only under the gated step); `three_seed_mean` with `expected_seeds` from `ConfigSnapshot.seeds` (never inlined); the R-90 stamp match as a named function in `train.py` with the four negative controls, control 3 by enumeration over R-80's six ids; `TuningRecord` with the seven approved fields plus the three attestation fields (Q1 = C at nfr-design), attestation unconditional; M-03 fitted on training partitions only; the W-12 / R-102a one-shot `DEC` write with `PredictionHashReceipt`, fsync-then-rename, registry column 18, refusal to exit — with **no `DEC` execution** (the path exists and stops at `materialise_locked_partition`'s G-05 signature guard); five ablations registered from `experiment.yaml`, `ABL-HIST48` refusing until the primary configuration is frozen; the +24 h horizon config-only; RF importance diagnostic-only marker; residual/GRU/PyTorch absence tests.
- No model is trained here (no pandas/numpy/sklearn/TensorFlow installable); every suite run is smoke evidence only under the stdlib stand-in; ruff owed; no commit.

- Looks correct
- Request changes

[Answer]: Looks correct

---

## Plan Approval

The code-generation plan for `models-and-baselines` is at
`construction/models-and-baselines/code-generation/code-generation-plan.md` —
11 steps: BLK-03 change record + proposed D-number text FIRST (1), pins and D-121
transcription (2), persistence + climatology (3), ridge + random forest with lazy
sklearn (4), checkpoint + pin-guarded LSTM (5), train.py with stamp match, three-seed
mean, tuning attestation, grids, ablations (6), GATED Transform.inverse on your
D-number reopening D-27 (7), script 06 with the W-12 receipt and no DEC execution (8),
the two mandated test modules with negative controls (9), smoke + lint (10),
governance stop (11).

- Approve Plan
- Request Changes

[Answer]: Approve Plan
