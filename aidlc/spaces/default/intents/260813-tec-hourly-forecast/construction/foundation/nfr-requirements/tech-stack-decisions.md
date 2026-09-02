# Tech Stack Decisions — `foundation`

**Unit** `foundation` (Bolt 1) · **Kind** `library` · **Depends on** — (dependency root)
· **Stage** `nfr-requirements`

> ## ⚠ THIS ARTIFACT TRANSCRIBES AN APPROVED STACK; IT DOES NOT SELECT ONE
>
> TE §8 fixes this project's stack as a **normative** table, not a recommendation. Almost
> every row below is therefore a transcription with its rationale, not a decision this
> stage took. Where TE §8 leaves a value unfrozen — the TensorFlow pin — it stays
> **`TBD — freeze gate`**, because **TE §18.2 forbids an implementer or coding agent from
> filling such a value by convenience**.
>
> **Nothing is claimed installed.** `configs/`, `src/`, `pyproject.toml` and
> `requirements.txt` do not exist as a completed set; **no Python interpreter exists in
> this environment** (a zero-byte Windows Store stub, no registry entry, no interpreter on
> disk). **TA-03 is `Pending`** and no install has been evidenced on either platform.

## Sources

- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§8.1** (approved components), **§8.2** (model implementation ownership), **§8.3** (prohibited stack), **§9.1** (exactly two platforms), **§9.2** (compute posture), **§12** (repository tree), **§13.1** (the per-run environment lock), **§13.2** (the ordered clean-run contract), **§18.2–18.3**, **§19** (TA-01, TA-03, TA-16, TA-26).
- `../functional-design/business-logic-model.md` — **W-9** (what Bolt 1 builds and what it must not), **W-2**/**W-3** (config load, snapshot, hash; the preflight), **W-4** (`seed_everything` and the determinism probe), **W-8** (platform resolution), **W-10** (fixture-scale only).
- `../functional-design/business-rules.md` — **R-01** (`IntegrityError` as the single catchable base), **R-05**/**R-06** (determinism applied before graph construction; an empty `nondeterministic_ops` is never proof), **R-16** (no machine path in a governed config), **R-17** (every module and script carries a purpose/inputs/re-run docstring).
- `../../../inception/requirements-analysis/requirements.md` — **REQ-ENG-1**, **REQ-ENG-2**, **REQ-ENG-3**, **REQ-ENG-8**, **REQ-ENG-10**, **REQ-ENG-11**, **REQ-ENG-12**, **NFR-DET-01**.
- `../../../inception/practices-discovery/team-practices.md` — § Code Style (`ruff` for lint and format; the `NN_verb_noun.py` convention; the four governed configs), § Testing Posture.
- `nfr-requirements-questions.md` — Q3 = A and the receipted Consolidated Summary Confirmation.

---

## TS-01 — Language and runtime

| Decision | Value | Status | Authority |
|---|---|---|---|
| Language | **Python 3.11, exact version** | Approved, normative | TE §8.1; TC-03d |
| Second language | **None** | Prohibited | TE §8.3 — R, Julia, MATLAB prohibited for the pipeline |

**`aidlc-state.md` records `Languages: Python 3.11`**, corrected by hand on 2026-08-22
under `GOV-2026-08-21-UG-01`. The TypeScript under `.claude/tools/` and `.claude/hooks/`
is the AI-DLC framework's own workflow infrastructure and **never a project deliverable** —
`team.md` § Corrections carries this because the stale value had already propagated into a
governance board's dispatch brief.

**Why Python-only is a rule and not a preference.** TE §8.3 lists R, Julia and MATLAB as
**Prohibited**, each with its stated reason — a second language or runtime. This is not a
tie broken on convenience.

## TS-02 — The forecasting stack, and the one value that stays unfrozen

| Component | Pin | Status |
|---|---|---|
| `tensorflow` / `tf.keras` | **`TBD — freeze gate`** | **UNFROZEN** — candidate **2.21.0** |

**Decision (Q3 = A).** The TensorFlow version is recorded as **`TBD — freeze gate`**, with
**2.21.0** carried as TE §8.1's **named candidate** rather than as the decision.

**Why.** TE §8.1 states the freeze condition in the same sentence that names the
candidate: *"TensorFlow 2.21.0 is the current Python 3.11-compatible candidate; the exact
compatible pin is frozen only after Kaggle/local fixture installation passes."* **Neither
walking-skeleton fixture has run.** Recording 2.21.0 as the pin would contradict the
source the number came from, and TE §18.2 states the prohibition absolutely. A pin that
installs is not evidence the pin was approved.

**Consequence, stated rather than worked around.** `requirements.txt` **cannot be
completed** until the fixtures install on both platforms. TA-03 ("Python 3.11 and exact
pins install successfully on both Kaggle and local") stays `Pending`, which it already
was. The sentinel is deliberately visible to the **TE §18.3 zero-TBD preflight**, which is
the mechanism that will eventually force the freeze rather than let it lapse.

**One stack, both phases.** TE §8.1 requires `tensorflow` / `tf.keras` as **one forecasting
stack for both phases**, and TE §8.3 prohibits **PyTorch** in the governed pipeline —
stated reason: avoiding a second deep-learning stack and a framework-change confound
between phases. **CPU is sufficient** (TE §8.1).

**The row that will evidence the one-stack rule is TA-26**, not TA-03: *"TensorFlow/Keras
is the only NN stack; exact pins install; deterministic seed utility and serialization
restore pass locally and on Kaggle."* TA-03 evidences the **install** of Python 3.11 and
the pins on both platforms. Both are `Pending`, and TA-26 additionally cannot be evidenced
until TS-07's determinism utility exists. Named separately because the two are easy to
conflate, and because §8.1's pin freeze is a precondition of both.

## TS-03 — Approved components, transcribed from TE §8.1

| Component | Status | Approved use |
|---|---|---|
| `numpy` | Required | Arrays, deterministic numerics, bootstrap implementation |
| `pandas` | Required | Tabular data, timestamps, manifests, registry, aggregation |
| `pyarrow` | Required | Parquet artifacts |
| `pyyaml` | Required | The four configuration files |
| `scikit-learn` | Required | Ridge (M-04), Random Forest (M-05), preprocessing, metrics, grid search |
| `gnss-tec` | Required — primary GNSS path | RINEX parsing and STEC groundwork; **not** a complete GNSS-to-VTEC processor on its own |
| `iricore` | Required | IRI-2016 **benchmark** generation, explicit 2000 km ceiling |
| `matplotlib` | Required | Reproducible figures and diagnostics |
| `pytest` | Required | Unit, integration, leakage, schema, denial and fixture checks |
| stdlib `urllib`, `hashlib`, `csv`, `json`, `zipfile` | Required | HTTPS retrieval, manifests, SHA-256 checksums, packaging — **no scientific TEC transformation** |
| `seaborn`, `tqdm`, `requests` | Preferred | Diagnostic plots; progress; controlled downloads where provider terms permit |
| `madrigalWeb` client/API | **Conditional on D-144 approval** | Experiment/file discovery, parameter-filtered prepared `gps` retrieval, permanent citation |
| `h5py` and/or `netCDF4` | **Conditional on the approved export format** | Read provider-exported prepared VTEC without recomputing TEC; frozen after the schema audit |
| `georinex` | Conditional | RINEX/IONEX parsing or inspection cross-check only |

**Conditional is not approved.** `madrigalWeb` awaits **D-144**; the HDF5/netCDF choice
awaits the schema audit. Neither is treated as settled here.

**A package listed is not permission to bypass a freeze gate** — TE §8.1's own sentence,
carried because it is the rule this artifact is most likely to be misread against.

## TS-04 — Prohibited, and why each is prohibited

| Item | Status | Reason (TE §8.3) |
|---|---|---|
| Any **IRI-derived** ML feature or target | **Prohibited** in the confirmatory experiment | Would convert the independent comparison into learned post-processing of IRI |
| IRI-residual RF / IRI-residual LSTM | **Removed** | Not the author-confirmed primary question |
| **GRU** | **Removed; gate closed** | Absent from the approved ladder; adding it needs a scope-change record |
| **PyTorch** | **Prohibited** | A second deep-learning stack and a framework-change confound between phases |
| Transformer, attention, BiLSTM, GNN, architecture search | Out of scope | Excluded by Vision §4.2 |
| **R**, **Julia**, **MATLAB**, Theano | Prohibited | A second language/runtime; obsolescence |
| GLONASS | Prohibited in the primary product | FDMA inter-frequency biases; larger DCB disagreement than GPS |
| Galileo | Not in the primary product | Optional post-completion sensitivity only |
| GPS-TEC (Seemala) as a production processor | Prohibited | Closed and platform-bound; breaks the Kaggle path |
| Bernese / GAMIT / full custom GNSS workflow | Out of scope | Disproportionate to a bachelor thesis |
| **Docker / container as a required deliverable** | **Gate closed** | Exact pins are sufficient; revisit only if lock-based reproduction fails |
| **Google Colab, Google Drive as governed platforms** | **Removed** | Multiplies platform drift and transfer governance for no scientific gain |

**Enforcement is by test, not by intention.** TA-08 and TA-12 require **grep evidence**
that SSN, residual modules and GRU modules are **absent from the codebase**; TA-26 requires
that TensorFlow/Keras is the only NN stack. All are `Pending` and unexecuted.

## TS-05 — Platforms

**Exactly two execution environments** (TE §9.1; TC-03c). No third platform is authorised;
W-8 raises `PlatformError` on anything else.

| Platform | Role | Operating rule |
|---|---|---|
| **Local** | Development, small tests, fixture runs, review, artifact inspection | Same Python 3.11 and **exact pins** |
| **Kaggle** | Primary compute; Phase 1 acquisition/audit host | Internet enabled for the approved acquisition notebook; outputs under `/kaggle/working`; executed notebook, provider files and manifests saved; governed outputs copied back **with hashes and registry entries** |

An artifact moving between them moves **with a SHA-256 manifest**, and the transfer is
recorded.

**CPU is a complete execution path, not an emergency mode** (Vision §9.2; TE §9.2;
TC-01). GPU may be an **optional accelerator only** and never a dependency of any result.

**The in-Kaggle obligation is a condition on the session, not a Bolt number.** Any Bolt
performing a governed run inside a Kaggle session must first evidence that the required
critical tests and applicable fixtures passed **inside that same session** — a Kaggle
session carries no git working tree, so a local suite run proves nothing about the
environment the governed run executes in. **Bolt 1 performs no governed run**, so the
obligation does not bind it.

## TS-06 — Repository structure and tooling

**Mandated by TE §12; TA-01 gates the skeleton's acceptance on it.** `pyproject.toml` at
the repository root, four configs under `configs/`, six `src/` packages (`data`, `gnss`,
`external`, `features`, `models`, `evaluation`), nine phase-aware stage scripts, five
notebooks, `tests/`, `artifacts/`, and `requirements.txt` with exact pins for Python 3.11.

| Decision | Value | Authority |
|---|---|---|
| Linter **and** formatter | **`ruff`**, configured in `pyproject.toml` | `team.md` § Code Style (Q10 = A) — adopted now, before the nine stage scripts are written |
| Stage script naming | `NN_verb_noun.py`, two-digit ordinal prefix | TE §12, §13.2 |
| Stage script CLI | every stage script takes `--config configs/`; phase-aware stages also `--phase 1\|2` | TE §13.2 |
| Skeleton orchestrator CLI | `--fixture plumbing_7day` / `--fixture scientific_1month` | TE §13.2 |
| Test naming | `test_<subject>.py` | TE §12 |
| Notebook naming | `NN_topic.ipynb` | TE §12 |
| Governed configs | exactly four — `data.yaml`, `features.yaml`, `experiment.yaml`, `seeds.yaml` | TE §12; TC-03e |
| Docstrings | every module and script states purpose, inputs and re-run behaviour | R-17; `project.md` § Mandated |

**No scientific constant lives in source or a notebook** (TC-03e). Every one lives in one
of the four governed configs.

**The `tests/` mandated set is 21 modules**, not the 17 `team.md` § Testing Posture
enumerates — that figure is superseded, derived 2026-08-28 by enumerating TE §12's tree
and set-differenced against the affirmed 17 as **+4 / −0**. `team.md` § Corrections carries
the correction; § Testing Posture's own rewrite is owed to the next
practices-affirmation gate.

**Migration obligation, recorded not deferred.** `scripts/audit_ec1_drivers.py`,
`scripts/merge_coverage_year.py` and `notebooks/madrigal_phase1_coverage_audit.ipynb` move
onto the §12 structure (REQ-ENG-8, TA-16). The notebook's inline station coordinates and
its coordinate-to-cell rule are **§18.2 forbidden-choice items** and must be **frozen under
a D-number first**, so the migration cannot silently change a scientific value. The
triplicated SHA-256 helper consolidates into `src/data/release.py`.

## TS-07 — Determinism and the environment lock

**Requirement (NFR-DET-01, TC-21).** Seeds are fixed in `seeds.yaml`; the **three-seed
element-wise mean** is the confirmatory prediction; nondeterministic operations are
**recorded** where determinism cannot be guaranteed. No seed is selected on validation or
after seeing December.

**Frozen seed values, carried with their own status.** Development **42**; final
**{1337, 2024, 7}**; bootstrap **20221201** (Vision §8.6, D-122; TE §13.5). **D-122's
status is carried, not hidden:** Vision §14.2 marks it *"Approved — supervisor sign-off
pending"* — frozen for implementation, still owing a signature at G-05.

**Mechanism (TE §9.3/§13.5).** Python, NumPy, scikit-learn and TensorFlow seeds are set
through **one tested utility** using `tf.keras.utils.set_random_seed`, with
`tf.config.experimental.enable_op_determinism()` enabled where supported. R-05 requires
determinism to be applied **before any graph construction**, re-exec first. **R-06: an
empty `nondeterministic_ops` is never proof of determinism.**

**Per-run environment lock (REQ-ENG-10, TE §13.1) — eight items in seven bullets.**

1. the `requirements.txt` hash **and** a per-run `pip freeze` — **two items in one bullet**;
2. Python, OS, CPU and key library versions;
3. the code commit;
4. configuration snapshot hashes for **all four** configs;
5. input dataset and manifest versions;
6. the platform;
7. any known nondeterministic operations.

**The 7-versus-8 discrepancy is stated rather than smoothed over.** TE §13.1 renders as
**seven** bullets — `functional-design` § Sources derives exactly that
(`awk 'NR>=749 && NR<=760 && /^- /' <TE> | wc -l` → **7**) — while REQ-ENG-10 calls them
**eight items**. Both are right: bullet 1 carries two separately capturable artifacts, the
pinned manifest and its realised freeze, which is why REQ-ENG-10's acceptance criterion
reads "a registry row exists carrying **all eight** fields, populated — not `unavailable`".
Counting them as seven would let a row satisfy the check while capturing the pin file and
never the `pip freeze`.

**REQ-ENG-10 is `UNTESTED` by design** — no WS or TA row covers the §13.1 capture list, and
Amendment A was **declined 2026-08-24**. The thirteen existing acquisition runs are
recorded as **violating** it (`evidence/experiment_registry.md`: the §13.1 list *"was not
captured at the time and cannot be reconstructed"*), so it binds **from the next run
forward**.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| REQ-ENG-1 | TS-06 | TA-01 | `Pending` |
| REQ-ENG-2 | TS-06 | TA-02 | `Pending` |
| REQ-ENG-3 | TS-01, TS-02, TS-03 | **TA-03, TA-26** | `Pending` — **no install evidenced** |
| REQ-ENG-8 | TS-06 | TA-16 | `Pending` |
| REQ-ENG-10 | TS-07 | **none** | **UNTESTED by design** — Amendment A declined |
| REQ-ENG-11 | TS-07 | **TA-17, TA-26** | `Pending` |
| REQ-ENG-12 | TS-06 | TA-16 | `Pending` |
| NFR-DET-01 | TS-07 | **WS-17 (supporting), TA-13** | `Pending` |

**Derived and printed**: 7 decision sections (TS-01…TS-07); 8 coverage rows; **1**
requirement untested by design; **0** rows claimed satisfied; **1** value left
`TBD — freeze gate` (the TensorFlow pin).

## Assumptions & Open Questions

- **[Q3]** The TensorFlow pin stays `TBD — freeze gate` until both walking-skeleton fixtures install and pass on **both** platforms. 2.21.0 is TE §8.1's named candidate and is **not** adopted here.
- **[assumption]** TE §8.1's list is complete for Bolt 1's purposes. It names no dependency-management or lock tool beyond `requirements.txt` with exact pins, and none is introduced here — `pyproject.toml` carries the `ruff` configuration and the project metadata TE §12 mandates, not a second, competing lock format.
- **[assumption]** `ruff` is compatible with the eventual pinned environment. It is a development tool rather than a governed runtime dependency, so it is not in TE §8.1's table; `team.md` § Code Style adopts it. If a pinned-environment conflict emerges, that is a `team.md` question, not a TE §8 amendment.
- **Open, and not this stage's to close — the `IntegrityError` module home.** R-01 declares the hierarchy in **`src/data/config.py`** because TE §12's `src/data/` tree names **nine** modules and **none for exceptions**, so a dedicated `src/data/exceptions.py` would be a **§12 amendment this stage may not make by assertion**. `config.py` works and crosses no import boundary — every unit raising one of the other subclasses already depends on `foundation` — but a module whose §12 comment reads *"config load, per-run snapshot, hashes, determinism helper"* is not an obvious home for a project-wide exception base. **The owner's decision: accept `config.py`, or amend §12.**
- **Open, and cross-unit.** Nine of R-01's named subclasses are **raised by other units**, and each of those units' `functional-design` must declare its own exceptions as `IntegrityError` subclasses. A further **18** project-defined subclasses ride R-01's any-future clause. Without those declarations the stage-entry catch lets a violation exit with **no `aborted` registry row**, against NFR-PHASE-01 and NFR-AUD-01.
- **Observed upstream, not corrected here.** `../functional-design/business-logic-model.md` asserts "module creation is authorised" in its lead G-09 box and `§ Assumptions` bullet while **W-9's barred list** and the BLK-01 note state creation stays gated. Reported rather than fixed — editing a completed stage's artifact is outside this stage's produces. This artifact takes the conservative reading: **nothing here authorises creating a module.**
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row, install or test as discharged.
