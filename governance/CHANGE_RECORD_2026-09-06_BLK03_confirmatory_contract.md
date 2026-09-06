# Change Record — the confirmatory-prediction contract approved as the governed BLK-03 contract

**Record ID:** `CR-2026-09-06-BLK03-CONFIRMATORY-CONTRACT`
**Date:** 2026-09-06 (rulings receipted); record filed 2026-09-06 at the start of the
`models-and-baselines` code-generation pass, BEFORE any module of that unit was written.
**Ruling:** Project decision owner, at the `models-and-baselines` code-generation plan gate
(Q1 = A, Q2 = B superseded by FU-1 = C, Q3 = A, Q4 = B superseded by FU-2 = B, Q5 = A; receipted in
`aidlc/spaces/default/intents/260813-tec-hourly-forecast/construction/models-and-baselines/code-generation/code-generation-questions.md`,
Consolidated Summary Confirmation `Looks correct`, Plan Approval `Approve Plan`).
**Change class:** Change-control acceptance of a functional-design contract that was authored at
stage 3.1 and never separately approved — the acceptance `GOV-2026-08-22-REM-01`'s exit ruling
(`REM-02`, options 1 + 3) made a precondition of exiting stage 3.1 for every affected unit. This
record is that acceptance for **BLK-03** (the confirmatory-prediction contract). It also records
**two engineering-pin decisions** (Q3 = A; FU-1 = C), **one transcription of an approved decision
into a governed config** (Q5 = A), and **one gated step whose precondition is an owner act this
record does NOT perform** (FU-2 = B).

## What was owed, and by whom

`GOV-2026-08-22-REM-01` `REM-02` reworded BLK-03/BLK-04 from entry conditions to **exit
conditions** on stage 3.1: an affected unit may enter `functional-design`, where the contract is
authored, but *"no affected unit may complete or exit 3.1 without its approved contract, and no
implementation may proceed while this blocker stands."* Every stage-3.1 and nfr-design artifact of
`models-and-baselines` repeats *"authoring is not approving"* and *"BLK-03 independently bars
implementation."* The blocker register (`inception/units-generation/unit-of-work.md` § 8) names the
required resolution: *"a governed cross-unit contract defining input and output types, alignment
requirements, ownership of the frozen seed set, allowed partitions and failure conditions, with the
frozen set arriving as a parameter from `ConfigSnapshot.seeds` — never inlined in `src/models`, never
weakened to a distinctness check."*

The contract itself was fully authored at 3.1:

- **`domain-entities.md` § 3** — `ConfirmatoryPrediction`, four limbs (input type; output type;
  allowed partitions; failure conditions) plus the five-point downstream consumption contract.
- **`business-rules.md` R-91** (the three-seed mean and nothing substituted), **R-92** (provenance
  agreement; the `PartitionError` / `LeakageError` discriminating rule), **R-93** (the seed is never
  selected).

Two of BLK-03's three limbs closed earlier: the **seed values** on 2026-08-22 (D-122 — *"Approved;
supervisor sign-off closed 2026-08-22"*, Vision §14.2 line 1207) and the **mechanism** on 2026-08-23
(`expected_seeds: frozenset[int]` added to `three_seed_mean`, `component-methods.md`). What was
missing was the change-control act on the **contract limbs**: an owner ruling that accepts them as
the governed cross-unit contract, recorded in `governance/` before any commit.

## The rulings this record implements

### Q1 = A — the confirmatory-prediction contract is APPROVED as the governed BLK-03 contract

Exactly as `domain-entities.md` § 3 states it:

**Limb 1 — input type.** Exactly **three** `Prediction`s, all with `model_id == "M-06"`, whose
`seed` values form a set **equal to** `expected_seeds`. `expected_seeds` is read from
**`ConfigSnapshot.seeds`** at the call site — never inlined in `src/models` or any implementation
file (TC-03e; `project.md` § Forbidden). The frozen final set is D-122's, lives in
`configs/seeds.yaml`, and reaches the function as a parameter. Development seed **42** is not a
confirmatory seed; bootstrap seed **20221201** belongs to TE §13.6 / TC-19 and is not part of
D-122's item set.

**Limb 2 — output type.** A `Prediction` with `model_id = "M-06"`, `seed = None` (the mean is not
attributable to a seed), `frame` = the element-wise mean of `y_hat` over the three input frames on
the shared index, and `partition_id`, `transform_id`, `phase_id`, `source_id`,
`target_definition_id` **copied from the inputs, which must agree**. The three input predictions
are preserved by the caller.

**Limb 3 — allowed partitions.** F1–F4 validation months: yes. The January–November final refit:
yes. December (locked): **yes, and only through the guard** — `features-and-splits`'
`materialise_locked_partition(snapshot, *, g05_signature)` against a verified G-05 signature, not
this function. A training partition: **no** (`PartitionError`). A mixture of partitions: **no**
(`partition_id` identical across the three inputs).

**Limb 4 — failure conditions.** `SeedError` — fewer or more than three; the seed set not exactly
`expected_seeds`; any input with `seed is None`; any input whose `model_id` is not `"M-06"`.
`AlignmentError` — the three frames do not share an identical index on the ordered pair
**(`station`, `interval_start_utc`)**, compared as a set **and** in order. `PartitionError` —
`partition_id` differs across the inputs, or names a training partition (a declared-identity
disagreement). `LeakageError` — `transform_id` differs across the inputs, or is `None` on any
(a disagreement that implies information flow).

**The five-point downstream consumption contract**, inherited by `evaluation-and-comparison`,
`statistical-inference` and `regimes-diagnostics-reporting`: (1) the confirmatory prediction is the
element-wise mean of three seeds, never a single-seed run and never a best-of-three, and no consumer
may substitute or select among the three; (2) it carries `partition_id` and `transform_id`
identical to its inputs; (3) the three individual predictions remain available from the caller;
(4) `seed is None` on the mean is correct and load-bearing; (5) `Transform.inverse(frame)` is the
only route from model output back to absolute TECU and travels with `transform_id` — `src/evaluation`
uses it without importing `src/features`. **Point 5 names a method that does not exist today**; see
FU-2 = B below.

**R-91, R-92 and R-93 are approved with the contract**, including R-92's discriminating rule
(which `evaluation-and-comparison` R-105 mirrors and `statistical-inference` R-113 imports) and
R-90's four negative controls, whose raise types the same rule fixes.

**What this approval is, and is not.** It is the change-control acceptance the blocker register
requires for the contract's **mechanism**; it approves no new science — the seed values were closed
under D-122 before it. It does **not** discharge WS-15 or TA-13 (both stay `Pending`), does not
close BLK-04's or BLK-09's evidence limbs, and does not alter any gate: G-05, G-06, G-P1A, G-P2,
G-P3A, G-P3C and G-07 are unaffected.

### Q3 = A — `scikit-learn==1.4.2` is added to `requirements.txt` as an ENGINEERING pin

TS-M-03 requires `scikit-learn` for M-04 Ridge and M-05 Random Forest, and `requirements.txt` is the
single governed pin surface whose hash enters every run's environment lock (TE §13.1). The pin is
engineering, not scientific — foundation pinned `numpy==1.26.4`, `pandas==2.1.4` and
`pyyaml==6.0.1` the same way — but it is a change to a governed artifact, and this record is its
change-control trail. `1.4.2` is a release supporting Python 3.11 and numpy 1.26. `ridge.py` and
`random_forest.py` import it **lazily**, inside the fit path, and refuse by name when it is absent at
run time. `scikit-learn`'s CV splitters are never used (fold construction is
`features-and-splits`'). **Honest limit:** PyPI is unreachable on the machine this pass ran on, so
the pin could not be installed or exercised; the sklearn-backed paths are written and their refusal
is tested, and M-04/M-05 fits stay unrun until the pins are installable.

### FU-1 = C — M-06 is written against the tf.keras 2.21.0 candidate API; the pin stays `TBD — freeze gate`

Q2 = B ("freeze the TensorFlow pin now") was **not acted on**: it contradicted Vision §1.2 / TE §1.1
(*"No implementer or coding agent may fill such a value by convenience"*) and TE §8.1's sequencing
(the pin is frozen **after** the Kaggle and local fixture runs, neither of which has run). The owner's
follow-up ruling is **C**: the Keras construction is written against the API of TE §8.1's
**candidate** 2.21.0, but **every `tensorflow` import lives inside a guard** (`_require_frozen_pin`
in `src/models/lstm.py`) that refuses — naming TS-M-01 and the pin — unless `requirements.txt`
carries a frozen, non-comment `tensorflow==<version>` line. **No governed value is filled.** The
`requirements.txt` TensorFlow entry stays a comment carrying `TBD — freeze gate`. The
version-agnostic parts of M-06 — grid enumeration from config, the seven-setting assertion from
config, lowest-validation-RMSE checkpoint selection and restore over a recorded epoch history through
a backend-neutral interface — are real and tested with a fake backend. **Honest limits:** no
TensorFlow code can execute on this machine or anywhere until the pin is frozen; code written against
an unfrozen API version may need rework when the pin lands; TA-26 stays `Pending`.

### Q5 = A — D-121's grids and Vision §8.6's seven fixed LSTM settings are TRANSCRIBED into `configs/experiment.yaml`

`configs/data.yaml`'s own rule — *"only values frozen under an approved D-number are transcribed
here, citing that D-number"* — is applied to `configs/experiment.yaml`. **D-121** (Vision §14.2,
line 1206: *"Exact frozen grids: ridge 6, RF 18, LSTM 16 combinations, with fixed training
settings"*, status **Approved**) is the approved decision; **Vision §8.6** (lines 809–822) states its
contents. The transcription copies, verbatim and with citations:

- `grids.ridge` — `alpha ∈ {0.01, 0.1, 1, 10, 100, 1000}`, 6 combinations;
- `grids.random_forest` — `n_estimators ∈ {300, 600}` × `max_depth ∈ {8, 16, None}` ×
  `min_samples_leaf ∈ {1, 5, 20}`, `max_features = sqrt`, 18 combinations, direct only;
- `grids.lstm` — `layers ∈ {1, 2}` × `units ∈ {32, 64}` × `learning_rate ∈ {1e-3, 3e-4}` ×
  `batch_size ∈ {64, 256}`, 16 combinations, direct only;
- `models.lstm_fixed_settings` — dropout 0.2, Adam optimizer, MSE loss, maximum 100 epochs,
  early-stopping patience 10 epochs monitored on validation RMSE, minimum improvement tolerance
  1e-4 TECU, best-checkpoint restoration rather than last epoch (§8.6's fixed-settings sentence);
- `ablations` — TE §7.2's **five named entries** (`ABL-NODOY`, `ABL-DIFF`, `ABL-NOSW`, `ABL-HIST48`,
  `ABL-ZENITH`) with their identities, Phase-1 reachability, the §7.2 question and configuration
  change quoted, the `ABL-DIFF` inverse-before-metric and `ABL-HIST48` after-primary-freeze
  constraints, and `ABL-ZENITH`'s Phase 2 deferral. Every parameter §7.2 does **not** fix — each
  entry's `run_id` and `registered_at` — stays `TBD — freeze gate`.

**Nothing that D-121 / §8.6 / §7.2 does not fix is written.** In particular: the per-track declared
baseline (Vision §8.7 / D-124), the 1% simplicity tolerance (§8.7 / D-124), `horizons: [1]`
(TE §2.1) and every other `TBD — freeze gate` field in `experiment.yaml` (`folds`, `embargo_hours`,
`estimand`, `bootstrap`, `practical_relevance_threshold`) are **untouched** by this pass; the code
that needs them refuses naming the field. **Transcription changes no value** — the exactness of the
copy is the only thing this pass asserts about it, and a test re-reads the counts 6 / 18 / 16 from
config and compares them with the enumerated product of the transcribed axes, so a drift between the
two D-121 facts fails.

### FU-2 = B — the inverse is GATED on an owner act that this record does not perform

Q4 = B ("build the inverse here") was **not acted on**: **D-27** withheld the inverse mechanism and
stated *"no import-boundary change is authorised by this decision"*; `features-and-splits`'
code-generation Q4 = A (receipted 2026-09-06) confirmed that deferral and built `Transform` with no
inverse; and `project.md` § Way of Working forbids reopening a recorded refusal *"merely because the
material it refused is now within reach"* — reversal needs a new argument or an explicit human
decision that honours the original reasoning. The owner's follow-up ruling is **B**: **the owner
reopens D-27 first**, by a new D-number in `evidence/DECISIONS.md`, and only then does the developer
add `Transform.inverse(frame)` to `src/features/transforms.py`.

**The gate, as executed by this pass.** Plan Step 7 checks `evidence/DECISIONS.md` on disk when it
is reached: it proceeds only if a D-number **dated on or after 2026-09-06** exists that explicitly
reopens D-27's inverse withholding, states its new argument, honours D-27's reasoning, and settles
the naming. If present, `Transform.inverse(frame) -> frame` is added **additively** to the sibling
module (flagged for `features-and-splits`' record and re-check), the import graph stays unchanged
(the method travels with `transform_id`; no `src/evaluation` → `src/features` edge), `ABL-DIFF`
becomes runnable through it, and the inverse's negative controls are added. **If absent, the pass
stops at that step, ticks nothing there, reports the absence, and `ABL-DIFF` refuses — naming the
absent inverse and D-27 — exactly as it would under Q4 = A.** Nothing else in the plan waits on it.

**This record does NOT reopen D-27, does NOT edit `evidence/DECISIONS.md`, and does NOT add the
inverse.** The next section drafts text the owner may adopt or edit; drafting it is not deciding it.

## Proposed decision text for the owner to adopt (NOT a decision)

> **This section is a DRAFT for the owner's consideration. It has no authority. It becomes a
> decision only when the project decision owner writes it — adopted, edited, or replaced — into
> `evidence/DECISIONS.md` under the next free D-number, dated on or after 2026-09-06. The developer
> does not write it there, and Step 7 of the code-generation plan reads `evidence/DECISIONS.md`, not
> this file.**

```
## D-<n> — D-27's inverse withholding is REOPENED for ABL-DIFF: Transform.inverse(frame) is built (mechanism)

**Decision date:** <date ≥ 2026-09-06>. **Decided by:** the project decision owner under the
recorded authority equivalence, at the `models-and-baselines` code-generation gate.
**Authority:** TE §7.2 (`ABL-DIFF` inverse-transforms to absolute TECU before any metric);
TE §12 (import-boundary rule, unchanged); D-27 (reopened in part, reasoning honoured).
**Raised by:** `models-and-baselines` code-generation FU-2 = B (2026-09-06); BLK-08's
mechanism limb, co-owned by `features-and-splits` and `evaluation-and-comparison`.

**Decision.** `Transform.inverse(frame) -> frame` is added to `src/features/transforms.py`
as a method on `Transform`, ADDITIVELY: it maps a frame whose columns were standardised by
this transform back to the original scale, and it refuses (`InverseTransformError`) a frame
that carries no `transform_id`, or a `transform_id` that is not this transform's own. It is
the ONLY route from model output back to absolute TECU (consumption contract point 5), and
it travels with `Prediction.transform_id`.

**What D-27 decided, honoured in full.** The primary configuration's train-only transform
does not touch the target; the target stays raw TECU; the primary path needs no inverse;
and NO import-boundary change is authorised. All four statements stand. This decision
changes none of them.

**The new argument — why reopen.** D-27 narrowed the inverse obligation to `ABL-DIFF` and
left its MECHANISM open with `functional-design` (3.1). Stage 3.1 has since run for both
co-owners: `component-methods.md` names the method (`Transform.inverse(frame) -> DataFrame`,
"a method on `Transform`, which travels with the `Prediction`'s `transform_id` and needs no
new package edge"), and `models-and-baselines` `domain-entities.md` § 3 point 5 makes it the
consumption contract's only TECU route — a contract this same gate approved (Q1 = A). The
argument is therefore not "the material is within reach" but that the mechanism limb D-27
deliberately left to 3.1 has now been designed by 3.1, and the approved contract names it. A
method on `Transform` adds no `src/evaluation` -> `src/features` import: `src/evaluation`
receives a `Transform` (or resolves one by `transform_id` through the bundle store it already
reads) and calls the method — the import graph D-27 protected is unchanged.

**Naming (R-84 / R-103 divergence settled).** The method is `Transform.inverse(frame)`, as
`component-methods.md` names it. `load_inverse` / `Inverse` (R-84) and `load_transform` /
`Transform` (R-103 half A) are NOT introduced by this decision; whichever loader
`evaluation-and-comparison` builds resolves a `Transform` and calls `.inverse`.

**Error propagation** through the inverse (TE §7.2: "recorded") is `evaluation-and-comparison`'s
at the metric; this decision supplies the mechanism only.

**What is NOT decided.** No scientific value; `ABL-DIFF` is not approved or scheduled (it stays
a predeclared entry needing its own `run_id` registered before the freeze); the TE §12 import
allowlist is untouched; BLK-08's remaining limb (where error propagation is recorded) stays
with `evaluation-and-comparison`.
```

**If the owner declines**, nothing is owed: `ABL-DIFF` stays registered from `experiment.yaml` and
refuses naming D-27, which is the Q4 = A outcome the recommendation favoured.

## Blocker-register consequences — ROUTED TO THE GATE, NOT APPLIED

The blocker register lives in `inception/units-generation/unit-of-work.md`, an approved Inception
artifact. `governance/CHANGE_RECORD_PROCEDURE.md` permits annotate-in-place only with owner approval
for the specific item, so the status updates below are **recorded here and put to the owner at the
code-generation gate**, not written into the register by this pass:

| Blocker | Consequence of this record | Register action owed |
|---|---|---|
| **BLK-03** | Contract (`domain-entities.md` § 3 four limbs + consumption contract; R-91/R-92/R-93) approved. WS-15 / TA-13's **evidence** stays owed at G-05; approval governs the mechanism, not the evidence | Annotate: contract approved 2026-09-06 (Q1 = A); status remains open on the evidence limb |
| **BLK-04 ↓ / BLK-09 ↓** | Inherited; approved 2026-09-05 (`CR-2026-09-05-R74-R83-LEAKAGE-CONTRACTS`); nothing changes here | None new — the sibling record's annotations stand |
| **BLK-08** | Deferred per D-27 unless the owner adopts the D-number above; the inverse is gated on it (FU-2 = B) | Annotate only if the D-number is adopted: mechanism limb closed for `ABL-DIFF` by D-<n>; error-propagation limb stays with `evaluation-and-comparison` |

## Propagation sweep (`CHANGE_RECORD_PROCEDURE.md`)

This record amends a **status** (BLK-03's contract: authored, unapproved → approved), **two
governed-artifact contents** (`requirements.txt`: one pin added; `configs/experiment.yaml`: three
`TBD — freeze gate` scalars — `grids`, `models`, `ablations` — replaced by transcribed blocks), and
**no count, ID range or cardinality**. The superseded literals are: the phrase **"BLK-03 independently
bars implementation"** and its variants (*"authoring is not approving"*, *"approving this design is
not the contract's approval"*) as applied to the confirmatory-prediction contract; and the three
`experiment.yaml` values `grids: "TBD — freeze gate"`, `models: "TBD — freeze gate"`,
`ablations: "TBD — freeze gate"`.

Sites found (grep over the active intent's `construction/models-and-baselines/` artifacts, the
sibling units that cite BLK-03, `configs/`, `requirements.txt`, and `governance/`, 2026-09-06), with
disposition:

| Site | Disposition |
|---|---|
| `construction/models-and-baselines/functional-design/{domain-entities,business-rules,business-logic-model}.md` — the G-09/BLK-03 banners, § 3 / W-3 / R-91…R-93 "authoring is not approving" boxes, § Assumptions BLK-03 bullets | **Not edited** — completed-stage artifacts under frozen receipts; the statements were true when written. Superseded by this record as to the contract's status. Gate item: one annotate-in-place decision. |
| `construction/models-and-baselines/nfr-requirements/*.md`, `nfr-design/{security-design,logical-components}.md` — "BLK-03 is an open exit condition and independently bars implementation" | Same disposition. |
| `construction/{evaluation-and-comparison,statistical-inference,regimes-diagnostics-reporting,fixtures-and-reproducibility}/` — "BLK-03 ↓ inherited, open" | **Not edited** — terminal-READY under frozen receipts. Their inherited-open statements remain accurate on the evidence limb; the contract-approval fact is carried by this record. |
| `inception/units-generation/unit-of-work.md` § 8 blocker text and the summary table row 8 (`BLK-03, BLK-04 ↓, BLK-09 ↓`) | **Not edited** — approved Inception artifact; annotate-in-place routed to the gate (table above). |
| `configs/experiment.yaml` header comment (*"grids and model configuration: models-and-baselines"*, *"ablations: TE §7.2 named runs"*) | **Consistent** with this pass — the header already assigns those blocks to this unit; the three sentinel scalars are replaced by this pass (Step 2). |
| `configs/experiment.yaml` sentinel scalars `folds`, `embargo_hours`, `estimand`, `bootstrap`, `practical_relevance_threshold` | **Not edited** — owned by other units or unfrozen; outside Q5 = A. |
| `requirements.txt` header comment (TensorFlow excluded; pin `TBD — freeze gate`) | **Consistent** with FU-1 = C — unchanged; only the `scikit-learn==1.4.2` line is added (Step 2). |
| `configs/seeds.yaml` header comment (*"status 'Approved — supervisor sign-off pending at G-05'"*) | **Not edited** — a stale status quote (Vision §14.2 line 1207 reads *"Approved; supervisor sign-off closed 2026-08-22"*), found by this sweep, in a governed config this pass does not own. **Reported at the gate**; not in this record's scope. |
| `aidlc/spaces/default/memory/*.md` | Swept; no site names BLK-03's approval status or the `experiment.yaml` sentinels. Memory layers are never edited by a sweep. |
| `governance/CHANGE_RECORD_2026-09-05_R74_R83_leakage_contracts.md` (BLK-08 row: *"Deferred per D-27 (Q4 = A); nothing changes"*) | **Not edited** — a filed record; FU-2 = B's gate is stated above and does not alter that record's truth at its date. |

The **counts this record does not change**, stated so a later sweep does not re-derive them against
it: `build_partitions` returns **6**; the split manifest enumerates **5**; `Partition.partition_id`
is closed to **6** values; § Amendments owed stays **7 across 5 units** (this record is the
change-control trail for BLK-03's contract, not an amendment — every `src/models` shape beyond the
approved boundary calls is intra-package under `component-methods.md` § Depth); W-11's build list
stays **ten files**; `Prediction` keeps **8** fields; `ConfigSnapshot` keeps **8** fields; the D-121
cardinalities are **6 / 18 / 16**; the fixed LSTM settings are **seven**; the ablation registry is
**five named, four reachable in Phase 1**.

## What this record does NOT do

- It does **not** fill any `TBD — freeze gate` field by convenience. The only sentinels replaced are
  the three Q5 = A transcribes under D-121 / Vision §8.6 / TE §7.2 with citations; every parameter
  those sources do not fix keeps the sentinel.
- It does **not** freeze the TensorFlow pin, reopen D-27, edit `evidence/DECISIONS.md`, or add
  `Transform.inverse` — the last is gated on an owner act recorded elsewhere.
- It does **not** discharge any acceptance row: WS-14, WS-15, TA-12, TA-13, TA-26 stay `Pending`;
  the seven rowless requirements (FR-P1-04-14, FR-P1-05-3, -4, -5, -6, -21, -22) stay rowless.
- It does **not** execute `DEC`, write a `DEC` prediction, or touch December 2022 content: the
  one-shot write path is built and stops at `materialise_locked_partition`'s G-05 signature guard.
- It does **not** close BLK-03's evidence limb, BLK-04's or BLK-09's evidence limbs, or BLK-08's
  error-propagation limb, and changes no gate status.
- It does **not** edit `component-methods.md`, `requirements.md` (whose FR-P1-05-2 line still carries
  the superseded bootstrap-seed attribution and the superseded "sign-off pending" status — both
  raised at the gate, neither edited), or any sibling unit's record artifact.
- It does **not** train any model: no released feature bundle exists, the permitted-producer list is
  unset, and no `pandas`, `numpy`, `scikit-learn` or `tensorflow` is installable here.

## Evidence (created by the pass this record precedes)

- `src/models/train.py` — `Prediction` (approved 8 fields); `fit_predict` (approved signature;
  `LeakageError` on an untransformed bundle; closed model set); `assert_stamp_match` (R-90's three
  checks); `three_seed_mean` (all four limbs); `TuningRecord` (seven approved fields + the three
  SD-M-01 attestation fields) with the unconditional attestation; grid content + hash (R-96);
  selection (R-101); the five-entry ablation registry read from config (R-97) with `ABL-HIST48` and
  `ABL-DIFF` refusals; `HorizonSpec` (R-99); `PredictionHashReceipt` and its durable write (R-102a).
- `src/models/persistence.py`, `climatology.py`, `ridge.py`, `random_forest.py`, `checkpoint.py`,
  `lstm.py` — M-01…M-06 with the boundaries this record states.
- `scripts/06_train_and_predict.py` — the six-step entry, the stamp match before every scoring path,
  the one-shot `DEC` write with receipt and refusal-to-exit, reached only through
  `materialise_locked_partition`.
- `tests/test_models_smoke.py`, `tests/test_checkpoint_restore.py` — the negative controls named in
  R-90…R-102a, over synthetic frames and synthetic seeds/grids; no real seed, grid or setting value
  as a literal; no December content; no real signature.
- `requirements.txt` (+1 line), `configs/experiment.yaml` (three blocks transcribed).
- Suite results are **smoke evidence only, never governed evidence** (interpreter and environment
  limits are recorded in the code-generation summary).

## Owed list, carried by this record (recorded, not discharged)

- **The TensorFlow pin** — `TBD — freeze gate`; frozen after the Kaggle and local fixture runs
  (TE §8.1) under a D-number by its owner; M-06's Keras path is unexecutable until then; TA-26
  `Pending`.
- **The `scikit-learn==1.4.2` install evidence** — the pin is written; installing and exercising it
  is owed the first time PyPI is reachable (`pip install -r requirements.txt` on the 3.11 pin).
- **The `pyarrow` pin** — carried from `features-and-splits`; `06` cannot load a bundle without it.
- **The owner's D-number reopening D-27** — adopted or declined; Step 7's outcome is reported in the
  code-generation summary.
- **`horizons: [1]` (TE §2.1), the per-track declared baseline and the 1% simplicity tolerance
  (Vision §8.7 / D-124)** — frozen text whose config transcription is outside Q5 = A; the code
  refuses naming each field until its owner transcribes it.
- **The `prior_period_exposure` deviation** from the approved remediation text (R-102a) — `false`
  on a Phase 1 row; this unit writes no value; owner ruling requested.
- **`requirements.md` FR-P1-05-2's two superseded clauses** — reported, not edited.
- **The `configs/seeds.yaml` header's stale D-122 status quote** — found by this sweep; not this
  unit's file; reported.
- **The governed commit** for this pass cites **D-121, D-122, D-27, D-31** as touched context, plus
  the new D-number if adopted. **No governed commit before this record exists** — it exists first,
  and the commit is the student's act, not the agent's. The repository HEAD at the start of this pass
  was `ec8eacf` (an owner commit with the unedited git template as its message); this pass makes no
  commit and does not touch it.
