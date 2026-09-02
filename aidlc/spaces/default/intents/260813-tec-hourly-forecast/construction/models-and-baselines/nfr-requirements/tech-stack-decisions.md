# Tech Stack Decisions — `models-and-baselines`

**Unit** `models-and-baselines` (Bolt 8) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ THIS IS THE UNIT THE UNFROZEN PIN BLOCKS
>
> The governed stack is fixed by **TE §8** and transcribed at
> `../../foundation/nfr-requirements/tech-stack-decisions.md`. This unit adds **none** — and
> it is the unit that **cannot proceed without the one pin that is unfrozen**: the
> **TensorFlow version**, `TBD — freeze gate`, with **2.21.0** named as TE §8.1's candidate
> and frozen only after Kaggle/local fixture installation passes. **Neither fixture has run.**
>
> **No model has ever been trained.** No runtime, no memory figure, no convergence behaviour
> has been measured, and none is claimed. **WS-14, WS-15, TA-12, TA-13, TA-26 are
> undischarged**; **7 of this unit's 9 requirements have no acceptance row**; **G-09** is
> signed (D-31) with preconditions UNMET; stage 3.1 remains **FAIL**; `configs/` does not
> exist; no Python interpreter exists here.

## Sources

- `../../foundation/nfr-requirements/tech-stack-decisions.md` — the governed stack, the prohibitions, the platform rules, and the `TBD — freeze gate` TensorFlow pin. Referenced, not restated.
- `../functional-design/business-rules.md` — **R-91**, **R-93**, **R-94**, **R-96**, **R-97**, **R-99**, **R-100**, **R-101**, **R-102**, **R-102a**.
- `../functional-design/business-logic-model.md` — **W-2** (fit and predict over six families), **W-4** (checkpointing and restore), **W-6** (the grid freeze), **W-7** (the ablations), **W-8** (the +24 h horizon), **W-12** (the one-shot `DEC` write).
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§8.1** (`tensorflow`/`tf.keras` required, **CPU is sufficient**; `scikit-learn` for M-04/M-05; `numpy`, `pandas`, `pyarrow` required), **§8.2** (model implementation ownership), **§8.3** (**GRU removed; PyTorch prohibited**; Transformer/attention/BiLSTM/GNN out of scope), **§9.2** (CPU a complete execution path), **§9.3**/**§13.5** (the seed utility and op determinism), **§7.1**, **§7.2**, **§18.2**.
- `../../../inception/requirements-analysis/requirements.md` — **NFR-PHASE-01** *(cited 2026-09-01 on a pre-dispatch self-sweep: TS-M-04's "Serialization is a phase-transition asset" paragraph reproduces this requirement's substance — the `phase_transition_manifest` hashing the architecture serialization among its protected items, and **Phase 2 refusing to train if any protected hash differs** — while citing only TE §7.0B and this unit's own R-102. Acceptance row **TA-27**, owned by `governance-guards`.)*.
- `evidence/DECISIONS.md` — **D-121** (grid sizes), **D-122** (seeds; *"Approved — supervisor sign-off pending"*).
- `nfr-requirements-questions.md` — Q1 = A, Q2 = B, and the receipted Consolidated Summary Confirmation.

---

## TS-M-01 — One forecasting stack, and the pin this unit waits on

| Component | TE §8.1 status | Use here |
|---|---|---|
| `tensorflow` / `tf.keras` | **Required; one forecasting stack for both phases**. Pin **`TBD — freeze gate`**, candidate **2.21.0** | M-06 compact LSTM; SavedModel/`.keras` checkpoints; deterministic settings |
| `scikit-learn` | **Required** | M-04 Ridge, M-05 Random Forest, preprocessing, metrics, grid search |
| `numpy`, `pandas`, `pyarrow` | **Required** | Arrays, tabular handling, Parquet artifacts |

**This unit is where the unfrozen pin bites.** `foundation` records the pin as
`TBD — freeze gate`; **this is the unit that cannot build without it**. M-06's architecture
serialization contract, its checkpoint format and its determinism settings are all
version-dependent, and **TE §8.1 freezes the exact pin only after Kaggle/local fixture
installation passes**. Neither fixture has run. **No version is named here**, and TE §18.2
forbids naming one by convenience.

**One stack, both phases — and the reason is scientific, not operational.** TE §8.3 prohibits
**PyTorch** *"to avoid a second deep-learning stack and a framework-change confound between
phases"*. A framework change between Phase 1 and Phase 2 would make the cross-phase comparison
uninterpretable, so this prohibition protects a result rather than a build.

**TA-26 is the row that evidences it** — *"TensorFlow/Keras is the only NN stack; exact pins
install; deterministic seed utility and serialization restore pass locally and on Kaggle."*
`Pending`, and unrunnable until the pin is frozen.

## TS-M-02 — Determinism is a utility and a recorded absence

**Decision, transcribed from TE §9.3/§13.5.** Python, NumPy, scikit-learn and TensorFlow seeds
are set through **one tested utility** using `tf.keras.utils.set_random_seed`, with
`tf.config.experimental.enable_op_determinism()` enabled **where supported**.

**"Where supported" is a version-dependent surface**, and the version is unfrozen. Which
operations lack deterministic kernels differs across TensorFlow releases, so **the set of
recorded nondeterministic operations cannot be enumerated until the pin is frozen**. That is
stated rather than deferred silently: `nondeterministic_ops` is a **measured output of the
frozen environment**, not a list this stage can write.

**An empty `nondeterministic_ops` is never proof of determinism** (`foundation` R-06). An
empty list is equally consistent with a determinism check that never ran.

**Performance cost is accepted, not measured.** Enabling op determinism is documented to slow
training. **CPU is a complete execution path** (TE §9.2) and **GPU may be an optional
accelerator only, never a dependency of any result** — so a determinism setting that costs
speed cannot be traded away for a faster GPU path, because no result may depend on the GPU
path existing.

## TS-M-03 — `scikit-learn` for the baselines, with two things it must not be used for

**Decision.** M-04 Ridge and M-05 Random Forest use **`scikit-learn`** (TE §8.2). M-01, M-02
and M-03 are **project modules** — `src/models/persistence.py` and `src/models/climatology.py`
— because a transparent index operation and a fitted station×month×hour climatology are
**unit-testable project logic**, not library calls.

**Two prohibitions that are library-shaped, and therefore easy to trip.**

1. **`scikit-learn`'s cross-validation splitters are not used for fold construction.** They
   shuffle by default, and TE §7.1 requires **exact fixed calendar boundaries**. The folds come
   from `features-and-splits`; this unit **consumes partitions, it does not derive them**.
2. **`RandomForest.feature_importances_` is diagnostic only** (R-100). It is one attribute
   access away from being a selection input, and the rule that forbids it is a `project.md`
   **NEVER**. The negative control in § SEC-M-06 exists because the misuse is a single line.

**Grid search is bounded by content, not just by API.** `scikit-learn`'s search tools accept
any grid; **D-121 fixes the counts — ridge 6, RF 18, LSTM 16** — and R-96 asserts **content**
as well as immutability. A library that would happily accept a nineteenth RF combination is
exactly why the assertion is separate.

## TS-M-04 — Checkpoints, serialization, and the horizon that must stay config-only

**Decision (R-94, W-4).** M-06 checkpoints in TensorFlow's **SavedModel or `.keras`** format
(TE §8.1) and **restores its lowest-validation-RMSE checkpoint, not its last epoch**. The
restore path is a **tested behaviour** — `test_checkpoint_restore.py` in the mandated set —
because last-epoch restore is the library default shape and the correct behaviour is the one
that needs proving.

**Serialization is a phase-transition asset** (**NFR-PHASE-01**, TE §7.0B, TA-27). The
`phase_transition_manifest` hashes the **architecture serialization** among its protected items,
and **Phase 2 refuses to train if any protected hash differs**. *(ID cited 2026-09-01 — the
paragraph already stated the requirement's substance and named only the TE section.)* **Phase 2
also carries no Phase 1 fitted weights forward**: it retrains from newly initialized weights
unless a separately approved, exploratory-labelled transfer-learning experiment exists, and **no
Phase 1 result may motivate a Phase 2 model or evaluation change**. The acceptance row **TA-27 is
`governance-guards`'** — cited here as an obligation on this unit's serialization choice, not
claimed as discharged from this side. The serialization format is therefore not a free implementation
choice at 3.5 — changing it changes a protected hash.

**Decision (R-99, W-8).** The **+24 h horizon is structurally config-only**: producing it
requires **no code change**. Stated as a stack decision because the natural implementation —
a second training script, or a branch on horizon — would make the horizon a code fact and give
a later run an occasion to alter the model while "just adding a horizon".

## TS-M-05 — Two absences the stack must be able to prove

**Decision.** **GRU is removed with the gate closed**; **residual modules** (IRI-residual RF,
IRI-residual LSTM) are removed; **SSN is absent as a feature**; **PyTorch is prohibited**;
Transformer, attention, BiLSTM, GNN and broad architecture search are **out of scope**
(TE §8.3, Vision §4.2).

**These are tested absences, not documented ones.** **TA-08 and TA-12 require grep evidence**
that the named modules are absent from the codebase. That makes "we did not build it" a
**checkable property of the tree** rather than a claim, and it is why adding any of them later
would fail a test rather than merely contradict a document.

**Consequence for dependency choice.** Adding a package that bundles a prohibited
architecture — or that makes one a one-line import — would not itself violate TE §8.3, but it
would make the grep evidence harder to interpret. **No such package is added.**

## TS-M-06 — Platform posture

Unchanged from `foundation`: **exactly two platforms**; artifacts move between them **with a
SHA-256 manifest**; the transfer is recorded.

**CPU is a complete execution path, not an emergency mode** (Vision §9.2, TE §9.2, TC-01).
**GPU is an optional accelerator only and never a dependency of any result** — so M-06 must
train to completion on CPU, and any GPU parity check is **optional evidence within a frozen
tolerance** (EV-18), never the primary path.

**The in-Kaggle obligation binds this unit's governed runs.** Any Bolt performing a governed
run inside a Kaggle session must first evidence that the **required critical tests and the
applicable fixtures passed inside that same session** — a Kaggle session carries no git working
tree, so a local suite run proves nothing about the environment the training actually ran in.
**This unit performs the project's largest governed runs**, so the obligation is live here in a
way it is not for Bolt 1.

**Nothing has been measured.** No training runtime, no peak memory, no convergence behaviour.
TE §9.3's planning envelope is a **storage** budget, and **no numeric memory ceiling exists in
the authorities** — a conflation recorded elsewhere in this project and not repeated here.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| FR-P1-05-1 | TS-M-01, TS-M-03, TS-M-05 | WS-14, TA-12, TA-26 | `Pending` — **pin unfrozen** |
| FR-P1-05-2 | TS-M-02, TS-M-04 | WS-15, TA-13 | `Pending` |
| **FR-P1-05-5** | TS-M-03 | ⚠ **NO ROW** — proposed | control required |
| **FR-P1-05-6** | TS-M-04 | ⚠ **NO ROW** — proposed | control required |
| **FR-P1-05-22** | TS-M-04 | ⚠ **NO ROW** — proposed | control required |
| NFR-DET-01 | TS-M-02 | WS-17 (supporting), TA-13 | `Pending` |
| **NFR-PHASE-01** | TS-M-04 | **TA-27** — row owned by `governance-guards` | `Pending` |

**Derived and printed**: 6 decision sections (TS-M-01…TS-M-06); **7** coverage rows *(count
re-derived 2026-09-01 on a pre-dispatch self-sweep; superseded figure preserved: **6**)* — **not a subset of**
`security-requirements.md`'s **thirteen**, and the relation is printed as a decomposition rather
than as an "N fewer" phrase *(re-derived twice on 2026-09-01: first on a pre-dispatch self-sweep,
then again when NFR-AUD-01 was added to that file on adversarial finding 1. Superseded: "six
fewer than thirteen", "six fewer than twelve", and before those "five fewer than twelve". **All
three were wrong in the same way** — they treated this table as a subset of that one, which it
has not been since NFR-PHASE-01 was added here alone, so no single subtraction can describe the
relation. The subtraction is what kept going stale; the decomposition cannot.)*:

- **13 − 7 = 6 rows shared.** The **seven** rows carried in `security-requirements.md` only —
  FR-P1-04-14, FR-P1-05-3, FR-P1-05-4, FR-P1-05-21, NFR-LEAK-01, NFR-IRI-01 and **NFR-AUD-01**
  — raise **no technology choice**.
- **+1 row carried here only** — **NFR-PHASE-01** — giving **7**. **NFR-PHASE-01 is the seventh row and appears in this file only** — its
substance is a serialization-format consequence, which is a stack fact rather than a security
requirement, so it is correctly absent from `security-requirements.md` rather than missing from
it. *(Stated because a silent asymmetry between the two tables is what a reader has to
reconstruct, and three of this stage's coverage defects were silent gaps of exactly that shape.)* **0** rows claimed
satisfied; **0** new dependencies; **1** value left `TBD — freeze gate` (the TensorFlow pin,
`foundation`'s, and **blocking for this unit**); **1** list that **cannot be written until the
pin is frozen** (`nondeterministic_ops`).

## Assumptions & Open Questions

- **[TS-M-01]** **The TensorFlow pin blocks this unit specifically.** M-06's serialization contract, checkpoint format and determinism settings are all version-dependent. Nothing here names a version.
- **[TS-M-02]** **`nondeterministic_ops` cannot be enumerated until the pin is frozen** — which operations lack deterministic kernels is version-dependent. It is a **measured output of the frozen environment**, not a list this stage writes.
- **[assumption]** `tf.config.experimental.enable_op_determinism()` is available and effective on the eventual pin. TE §8.1 says *"where supported"*, which concedes it may not be for every operation. **If a required operation has no deterministic kernel, NFR-DET-01's guarantee narrows** and the narrowing must be recorded rather than absorbed.
- **[assumption]** CPU training of M-06 completes in a tolerable time. **Unmeasured** — nothing has been trained. If it does not, the response is **not** to make GPU a dependency: TC-01 forbids that, and the constraint would return here.
- **[Q2 / cross-unit]** The December-window **block** reads `governance-guards` R-25's log, which **does not exist** — **BLK-07 is open**. The block is **specified and unrunnable today**.
- **Carried — the prediction-hash receipt** is a two-half contract with `foundation`; **not satisfied from one side**.
- **Carried — D-122's seed set owes a supervisor signature at G-05**, and the grid hash must be **committed before G-05**.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row, install or test as discharged.
