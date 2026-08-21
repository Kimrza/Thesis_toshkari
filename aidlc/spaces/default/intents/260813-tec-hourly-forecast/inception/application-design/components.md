# Components — Hourly VTEC Forecasting (TEC_Project Phase 1)

Stage 2.6 (application-design), intent `260813-tec-hourly-forecast`.
Depth: Comprehensive. Scope: `research-pipeline-governed`.

## Sources

- [desc] Initial description, carried verbatim in
  `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/intent-capture/intent-statement.md`.
- Requirements: `../requirements-analysis/requirements.md` — 94 requirement rows,
  40 with no §16/§19 test row. Every component below names the requirement IDs it
  carries.
- Affirmed practices: `../practices-discovery/team-practices.md` — `ruff`, the
  `NN_verb_noun.py` convention, the `--config configs/` CLI, two platforms, and
  the rule that a notebook never holds the only copy of production logic.
- Authority: Technical Environment v3.3 §12 (the repository tree, fixed to file
  level), §7.0 (phase prohibition), §13.1–13.7 (run records, releases,
  determinism), §14 (notebooks); Vision v4.3 §6–§9.
- Stage answers: `application-design-questions.md` Q1–Q8, FU-1–FU-3.

## How to read this document

**This stage did not choose an architecture.** TE §12 fixes the repository layout
down to individual files — six `src/` packages, every module named, most with a
stated responsibility. §8.3 fixes Python-only with TensorFlow/Keras as the sole
NN stack. TC-03c fixes two platforms. What follows makes that frozen structure's
**boundaries and ownership explicit**, fills the three responsibilities §12
assigns to no module, and states which modules a Phase 1 command may reach.

Three modules are **additions** to §12's tree, decided at Q2, FU-2 and FU-3.
They are marked **NEW** and carry a governance obligation recorded as ADR-10 in
`decisions.md`. They are not treated as already-approved: no artifact here claims
§12 contains them today.

Layering, outermost first:

| Layer | What lives there | May depend on |
|---|---|---|
| `configs/` | Exactly four governed YAML files. Scientific constants only. | nothing |
| `src/` | Six domain packages. Reusable logic. | `configs/` via `src/data/config.py`, and other `src/` packages subject to the dependency rules |
| `scripts/` | Nine phase-aware stage scripts plus the fixture orchestrator. Orchestration only. | all of `src/` |
| `tests/` | 19 modules and two fixture directories. | all of `src/`, `scripts/` |
| `notebooks/` | Five notebooks. Review and presentation surfaces, plus one approved self-contained acquisition interface. | `src/` (four analysis notebooks); nothing (acquisition notebook, D-144) |

**Nothing in `src/` imports from `scripts/`, `tests/` or `notebooks/`.** The
dependency direction is one-way, outer to inner, with the sole exception that
`scripts/` orchestrates and never implements.

## Component inventory

### `src/data` — provenance, contracts, partitions

Owns everything about *what the data is and where it came from*. It is the only
package that reads `configs/`, and the only one that writes release manifests.

| Module | Responsibility | Phase | Requirements carried |
|---|---|---|---|
| `config.py` **NEW** | Load the four governed configs, snapshot them per run, hash them, and assert no required field is `TBD`. Hosts the determinism helper (Q6). | 1 and 2 | REQ-ENG-2, REQ-ENG-10, FR-WS-7, FR-P1-03-5 |
| `inventory.py` | Source inventory: TE §5.1's nine fields per entry, including the configuration that consumes each source. | 1 and 2 | FR-P1-01-6, FR-P1-01-2 |
| `prepared.py` | Phase 1 provider-file validation and standardization only. Schema, cell coverage, common timestamps. | **1 only** | FR-P1-01-1, FR-P1-01-4, FR-P1-03-1, FR-P1-03-5 |
| `phase_contract.py` | The phase boundary: the runtime import guard (Q3), the transition manifest, and its fourteen protected hashes. | 1 and 2 | FR-P1-03-2, FR-P1-06-1, FR-P1-06-2 |
| `locked_test.py` **NEW** | The December path guard (Q4): one chokepoint for every read under the restricted root, writing the access-log row **before** the read. | 1 and 2 | FR-P1-02-3, FR-P1-02-6, FR-P1-05-12 |
| `registry.py` | Station registry: coordinates, the coordinate-to-cell rule, and Vision §6.2's full content including one pinned IGRF version. | 1 and 2 | FR-P1-02-1, FR-P1-02-7 |
| `splits.py` | F1–F4 folds, the 24-hour embargo, and the December locked partition — the execution half of the locked-test guard (Q4). | 1 and 2 | FR-P1-04-5, FR-P1-05-12 |
| `release.py` | Immutable dataset releases: TE §13.3's ten manifest rows over fourteen fields, SHA-256 hashing, write-protection. The single home of the SHA-256 helper the team practice consolidates. | 1 and 2 | FR-P1-04-11, FR-P1-01-11, FR-P1-05-13 |
| `reuse_registry.py` | The §10.1 external-code register: all fifteen fields, recorded before the code is used. | 1 and 2 | FR-P1-06-3, FR-P1-06-4 |

**Boundary.** `src/data` is the only package permitted to construct a path into
`evidence/`. Every other package receives data as an in-memory structure or a
resolved artifact path handed to it.

### `src/gnss` — raw GNSS processing (Phase 2)

**Phase 1 must not import or execute any module in this package** (§7.0 hard
prohibition; NFR-PHASE-01). Per Q8, this stage records responsibilities and the
externally visible transition interface only — no internal signatures, no
unverified scientific assumptions.

| Module | Responsibility | Phase |
|---|---|---|
| `rinex.py` | GPS L1C/L2W, C1C/C1W/C2W observation parsing at 30 s. | **2 only** |
| `calibration.py` | Arcs, slips, levelling, DCB, mapping. | **2 only** |
| `target.py` | Hourly IPP-median aggregation to the Phase 2 ten-field contract. | **2 only** |
| `verification.py` | Six station-days, two references, sensitivities, uncertainty budget. | **2 only** |

**The Phase 1 → Phase 2 interface is a data contract, not a call surface.** No
Phase 1 code calls into `src/gnss`, so there is no function boundary to specify.
What crosses is `phase_transition_manifest` plus the frozen artifacts it hashes.
`component-methods.md` specifies that manifest's shape; it specifies no `gnss`
signature.

**The two target schemas are held distinct.** Phase 1's row is D-17's contract,
derived from the five-column product that actually exists (`ut1_unix`, `gdlat`,
`glon`, `tec`, `dtec`). Phase 2's is TE §6.1's ten-field row. `target.py` builds
the latter. Nothing in this design imposes the ten-field contract on the Phase 1
product — that inversion is what D-17 exists to prevent, and any transformation
between the two is Phase 2 work needing its own evidence and approval.

### `src/external` — benchmark and comparator products

| Module | Responsibility | Import rule |
|---|---|---|
| `iri.py` | IRI-2016 benchmark generation and its validation report. | **Importable only by `scripts/04_build_external_products.py` and `src/evaluation/`** |
| `gim.py` | CODE final GIM comparator, bilinear-in-space and linear-in-time interpolation with longitude-rotation correction. | same allowlist |
| `spaceweather.py` | Kp/ap3, Hp60/ap60, F10.7 with its trailing 81-day mean ending at the safe-lagged day. | unrestricted within `src/` |

**The allowlist is the rule, not the denylist.** TE §12 states it as *"imported
only by `scripts/04_build_external_products.py` and `src/evaluation/`"*. An
import from `src/data`, `src/gnss`, a training script or a notebook violates it
exactly as an import from `src/features` or `src/models` would. `iri.py` and
`gim.py` are **evaluation-time only** — they never reach training or inference,
and IRI joins only onto the frozen comparison-wide mask (NFR-IRI-01,
FR-P1-04-1).

`spaceweather.py` is deliberately outside that restriction: drivers *are* model
inputs, subject to the availability lags. It is grouped here because the products
are externally sourced, not because it shares the benchmark's isolation.

### `src/features` — the permitted ML input space

| Module | Responsibility | Requirements carried |
|---|---|---|
| `availability.py` | The availability matrix: observation timestamp, publication timestamp, release status and safe lag per feature. Asserts actual lag ≥ declared safe lag. | FR-P1-04-2, FR-P1-04-15, FR-P1-04-16 |
| `build.py` | Feature construction. **Asserts the IRI-free contract** and the closed §6.2 dictionary. | FR-P1-04-1, FR-P1-04-12, FR-P1-04-13, FR-P1-04-17 |
| `transforms.py` | Train-only fitting, per fold. Never fitted on the full dataset. | FR-P1-04-6 |
| `windows.py` | One shared window definition producing both the flattened matrix and the sequence tensor, so every model family sees the same eligible information. | FR-P1-04-8 |

**Boundary.** `src/features` imports `src/data` and `src/external.spaceweather`.
It must not import `src/external.iri`, `src/external.gim` or any `src/gnss`
module. `windows.py` owning both representations is what makes FR-P1-04-8's
matched-window parity checkable rather than aspirational.

### `src/models` — the six model families

| Module | Model | Responsibility |
|---|---|---|
| `persistence.py` | M-01, M-02 | Persistence and 24-hour seasonal persistence. |
| `climatology.py` | M-03 | Station×month×hour climatology, **fitted on training partitions only** (FR-P1-05-21). |
| `ridge.py` | M-04 | Ridge, grid of 6. |
| `random_forest.py` | M-05 | Random Forest, grid of 18, direct only. RF importance is diagnostic and never selects features. |
| `lstm.py` | M-06 | Compact LSTM, grid of 16, direct only. TensorFlow/Keras. |
| `train.py` | — | Training orchestration, the three-seed run, and the element-wise mean as the confirmatory prediction. |
| `checkpoint.py` | — | Lowest-validation-RMSE checkpoint save and restore. |

**Boundary.** `src/models` imports `src/features` and `src/data`. It must not
import `src/external.iri`, `src/external.gim` or `src/evaluation` — the
dependency runs the other way. Residual and GRU modules are **absent by
design**, and TA-08/TA-12 grep for their absence.

### `src/evaluation` — masks, metrics, uncertainty, reporting

| Module | Responsibility | Requirements carried |
|---|---|---|
| `masks.py` | The single comparison-wide intersection mask, computed once per comparison set, plus the IRI-free denial check. | FR-P1-04-7, FR-P1-04-1 |
| `metrics.py` | The paired loss differential — mean within-station difference of squared errors, benchmark minus model, equal-station weighting, positive favours the model. | FR-P1-05-7 |
| `bootstrap.py` | Vector time-block bootstrap: 24-hour blocks carrying all three stations, 10,000 replicates, **its own generator seeded from the separately frozen 20221201**. | FR-P1-05-8 |
| `regimes.py` | Kp/Hp60 strata and the §9.3 storm-event rule. | FR-P1-05-16, FR-P1-05-18 |
| `diagnostics.py` | Quality strata over D-17's measured-available fields, and the top-1%-removed sensitivity. | FR-P1-05-10, FR-P1-05-16 |
| `plots.py` | Figures. Presentation only; computes no reported quantity. | FR-P1-05-11 |

**Boundary.** `src/evaluation` is the **only** `src/` package permitted to import
`src/external.iri` and `src/external.gim`, and it does so at evaluation time
against the frozen mask. It imports `src/data` and `src/models` outputs; nothing
imports it.

**Open item carried in from stage 2.3.** `regimes.py` inherits an advisory
`NOT-READY` finding: FR-P1-05-18 requires the storm-event count to come from GFZ
Kp/Hp60 at a recorded release grade and bars any provisional-Dst-derived figure,
but no criterion tests that source. `component-methods.md` gives `regimes.py` a
signature that makes the source an explicit, checkable argument, which is the
most this stage can do — the missing criterion is a `requirements.md` change and
is not in this stage's produces list.

## Components with no §12 module — resolved here

| Responsibility | Authority | Resolution | Question |
|---|---|---|---|
| Config load, per-run snapshot, config hash, zero-`TBD` assertion | §13.1, §18.3 | **NEW** `src/data/config.py` | Q2 = B |
| Determinism: seeds, TensorFlow op determinism, recording non-guaranteed operations | NFR-DET-01, TC-21 | Helper in `src/data/config.py`, called at every stage entry; bootstrap seed carved out to `src/evaluation/bootstrap.py` | Q6 = X |
| December path guard and access log | FR-P1-05-12, D-15 | **NEW** `src/data/locked_test.py` | FU-2 = A |
| Platform root resolution | TC-03c, §9.1 | Runtime helper in `src/data/config.py`; resolved roots recorded in the run's environment lock | Q7 = C |
| Determinism tests with no home in the mandated set | NFR-DET-01 | **NEW** `tests/test_determinism.py` | FU-3 = B |

Each is a §12 tree amendment. **None is treated as approved.** ADR-10 in
`decisions.md` records the four-part obligation, its countersignature
requirement, and the four places REQ-ENG-4's count must move together.

## Assumptions & Open Questions

- **[assumption]** `spaceweather.py` sits in `src/external` per §12's tree while being a model-input source rather than an evaluation-only product. This design treats §12's placement as authoritative and does **not** move it; the isolation rule is scoped to `iri.py` and `gim.py` by name, as TE §12 states it.
- **[Q8]** `src/gnss` internals are deliberately unspecified. G-P2 checks manifest integrity, schema compatibility, configuration continuity and locked-test protections — not a `gnss` API.
- **Open, carried from 2.3.** `scripts/02_standardize_prepared_target.py` (Phase 1) and `scripts/02_build_vtec_target.py` (Phase 2) share the ordinal `02` in §12's tree. `services.md` records the reading adopted; the collision itself is a §12 defect this stage does not resolve.
- **Open, carried from 2.3.** § Known defects row 12 — the `plumbing_7day` station count — blocks the fixture manifest `run_walking_skeleton.py` reads. `services.md` names it as a precondition rather than designing past it.
- **None** of the above adopts a reading on a supervisor-owned value.
