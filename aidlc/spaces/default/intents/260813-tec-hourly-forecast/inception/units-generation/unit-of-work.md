# Unit of Work — Hourly VTEC Forecasting (TEC_Project Phase 1)

Stage 2.7 (units-generation), intent `260813-tec-hourly-forecast`.
Depth: Comprehensive. Scope: `research-pipeline-governed`.

## Sources

- Design: `../application-design/components.md` (the six `src/` packages, module ownership, the three **NEW** modules), `../application-design/component-methods.md` (boundary signatures), `../application-design/services.md` (the nine stage scripts, the stage entry contract, the two platforms), `../application-design/component-dependency.md` (the import allowlist, the forbidden edges, the data flow), `../application-design/decisions.md` (ADR-01…ADR-10).
- Requirements: `../requirements-analysis/requirements.md` — **105** requirement rows, **40** with no §16/§19 test row.
- `stories` (`../user-stories/stories.md`) is **absent by scope design**: stage 2.4 (user-stories) is `SKIP` in `research-pipeline-governed`. See `unit-of-work-story-map.md` for what replaces it.
- Affirmed practices: `../practices-discovery/team-practices.md`.
- Stage answers: `units-generation-questions.md` Q1–Q7.

## What this stage decided, and what it did not

This document is **topology only**. It states what each unit owns, what it may
depend on, and how much work it looks like. It does **not** pick a build order,
name a critical path, or say which unit ships first — those are stage 2.8's
economic decisions, made using this DAG as input.

Two ordering constraints appear here as facts rather than as recommendations,
and they are **not** the same kind of fact:

- `constraint-register.md` **TC-06** (repository structure, pinned environment
  and test suite before any acquisition work, inside this initiative) is an
  **inter-unit dependency edge**: it is what puts `foundation` and
  `governance-guards` upstream of `acquisition` in the DAG.
- **TE §9.2** (both walking-skeleton fixtures pass, in order, before any
  full-year job) is an **intra-unit ordering contract** owned by
  `fixtures-and-reproducibility` and enforced inside
  `scripts/run_walking_skeleton.py`. It is not an edge between two units and
  appears nowhere in the 23-edge block — a reader should not look for one.

Neither is an economic choice, and neither is stated here as advice.

## Unit definitions

**12 units.** Cut per Q1 = C (hybrid): explicit dependency-root units
first, then units that map onto runnable Phase 1 pipeline stages. Every shared
module has exactly one owning unit; downstream units consume its public contract
and never duplicate its implementation.

| # | Unit | Kind | Complexity | Deployment | Requirements | Acceptance rows | Blockers |
|---|---|---|---|---|---|---|---|
| 1 | `foundation` | `library` | M | shared | 16 | 7 | BLK-01 |
| 2 | `governance-guards` | `library` | M | shared | 10 | 2 | BLK-01 |
| 3 | `acquisition` | `library` | L | standalone | 15 | 1 | — |
| 4 | `inventory-and-registry` | `library` | M | standalone | 7 | 3 | — |
| 5 | `target-standardization` | `library` | M | standalone | 6 | 1 | BLK-05 |
| 6 | `external-products` | `library` | L | standalone | 7 | 1 | — |
| 7 | `features-and-splits` | `library` | L | standalone | 11 | 9 | BLK-04 |
| 8 | `models-and-baselines` | `library` | L | standalone | 9 | 5 | BLK-03, BLK-04 ↓ |
| 9 | `evaluation-and-comparison` | `library` | M | standalone | 4 | 1 | BLK-03 ↓, BLK-04 ↓ |
| 10 | `statistical-inference` | `library` | M | embedded | 1 | 2 | BLK-03 ↓, BLK-04 ↓ |
| 11 | `regimes-diagnostics-reporting` | `library` | L | embedded | 11 | 3 | BLK-03 ↓, BLK-04 ↓ |
| 12 | `fixtures-and-reproducibility` | `library` | M | standalone | 8 | 4 | BLK-01, BLK-02 |

Blocker column: an unmarked ID is a blocker whose affected artifacts this unit
owns; **↓** marks one inherited through a contract this unit consumes. **BLK-01
additionally reaches every unit** through the six-step stage entry contract and
is listed only against the two units that own its files, so the column stays
readable. § Blocker register below carries each blocker in full — affected
artifact, owning unit, downstream units, required resolution, approval authority
and status — with a per-unit roll-up of exactly which scope is blocked. A unit
with a blocker is present in this DAG and is **not** ready.

Complexity legend: S = one sitting, M = a few sessions, L = a substantial block of work, XL = would have been split. Relative only — no calendar estimate is implied,
and no ordering is implied by the row numbers, which are presentation order.

Deployment model, in this project's sense (`team-practices.md` § Deployment:
"deployment" means immutable dataset and model releases, and models are versioned
artifacts with a registry rather than deployed services):
**`shared`** = a library imported by other units, owning no stage script;
**`standalone`** = owns at least one of the nine phase-aware stage scripts, so it
can be run;
**`embedded`** = its logic executes inside another unit's stage script.

### Why every unit is `kind: library`

Q6 = X fixed the rule: `kind` follows a unit's actual owned artifacts and
executable responsibilities. `packaging` applies only to a unit limited to
scaffold, pins, install, build and distribution artifacts; `foundation` also owns
`config.py`, the determinism helper and `release.py`, so it is `library` and is
split only when the extra unit is justified — no justification exists yet.
`spec` applies only to a genuinely non-executable unit; the four governed configs
are specification artifacts owned by a `library` unit, and the transition manifest
is produced and validated by runtime code, so neither creates a `spec` unit.
`service` and `ui` are never used: this pipeline has no deployed executable and
no frontend.

---

## 1. `foundation` — Foundation — scaffold, configuration, determinism, releases

**Kind** `library` · **Complexity** M · **Deployment** shared · **Depends on** — (dependency root)

**Responsibility.** The repository itself and the run-time services every stage entry needs before any domain work: the §12 tree, the pinned environment, the four governed configuration files, their load/snapshot/hash path, the zero-`TBD` assertion, the determinism helper, platform-root resolution, the run record and experiment registry, and immutable dataset releases with their SHA-256 hashing.

**Owns.**

- `pyproject.toml`, `requirements.txt`, `README.md`, the `ruff` configuration
- `configs/data.yaml`, `configs/features.yaml`, `configs/experiment.yaml`, `configs/seeds.yaml`
- `src/data/config.py` — **NEW**: `load_configs`, per-run snapshot, config hash, `assert_no_tbd`, `assert_declared_sources_exist`, the `seed_everything` determinism helper, `ensure_process_determinism`, `resolve_platform_roots`
- `src/data/release.py` — TE §13.3's ten manifest rows over fourteen fields, SHA-256 hashing, write-protection; the single home of the hashing helper the team practice consolidates
- the run record and `experiment_registry.jsonl` append-only writer
- `tests/` tree and shared fixtures/conftest, `tests/test_determinism.py` (**NEW**), `tests/test_release_hashes.py`

**Boundary.** The only unit that reads `configs/`, and (with `acquisition`) one of two permitted to construct a path into `evidence/`. Exposes `ConfigSnapshot`, the seeded-run contract, resolved platform roots and the release API. Imports nothing from any other unit — this is the DAG's first root.

**Requirements carried (16).** REQ-ENG-1, REQ-ENG-2, REQ-ENG-3, REQ-ENG-4, REQ-ENG-6, **REQ-ENG-7**, REQ-ENG-8, **REQ-ENG-10**, REQ-ENG-11, FR-P1-01-10, FR-P1-04-11, FR-P1-05-13, FR-WS-7, NFR-AUD-01, NFR-SEC-01, NFR-DET-01

Bold = no §16/§19 test row (2 of 16 here).

**Acceptance rows (7).** TA-01, TA-02, TA-03, TA-10, TA-15, TA-22, TA-23

**Blockers.** **BLK-01** — owned scope blocked: `src/data/config.py`, `tests/test_determinism.py`. Approval authority: the authorized project decision owner (student, supervisor countersignature). Status: Open. This unit is present in the DAG and its blocked scope is **not** Ready, Approved or complete; its other owned artifacts are unblocked.

**Implementation notes and constraints.**

- `src/data/config.py` and `tests/test_determinism.py` have **no authority backing** until ADR-10's four-part §12/§13.2 amendment is countersigned. `code-generation` must not create them on the strength of ADR-10 alone.
- ADR-10's third row moves REQ-ENG-4's test-module count 18 → 19. Per the advisory finding on `decisions.md`, only REQ-ENG-4 and the external TE §12 tree are genuine loci of that count; `team-practices.md` § Testing Posture states a deliberately different figure (17 §12-tree modules) and must not be edited to 19.
- `ensure_process_determinism` must be the first statement of every stage script's `main()`, before any framework import — a re-exec after TensorFlow loads is pointless (FU-1 = D).
- No machine path may enter the four governed configs, so moving a directory never changes a governed hash (ADR-07).
- Two-tier error posture: integrity violations exit non-zero naming the file and the violated expectation; completeness shortfalls are recorded as machine-readable manifest fields.

---

## 2. `governance-guards` — Governance Guards — phase boundary, locked-test access, reuse register

**Kind** `library` · **Complexity** M · **Deployment** shared · **Depends on** `foundation`

**Responsibility.** The runtime prohibitions that must hold before any scientific work runs, and the transition contract that closes Phase 1: the phase-boundary import limb and produced-field limb, the transition manifest with its fourteen protected hashes, the single chokepoint for every read under the restricted December root with its access-log-before-read ordering, and the §10.1 external-code reuse register.

**Owns.**

- `src/data/phase_contract.py` — `assert_phase_boundary`, `assert_no_raw_fields`, `phase_transition_manifest` and its fourteen protected hashes
- `src/data/locked_test.py` — **NEW**: `open_restricted`, the access-log row written **before** the read
- `src/data/reuse_registry.py` — the §10.1 register, all fifteen fields, recorded before the code is used
- `tests/test_phase_boundary.py`, `tests/test_reuse_registry.py`

**Boundary.** Called at every stage entry (step 4 of the stage entry contract) and at every restricted read. Imports `foundation` for the config snapshot the manifest hashes; imports nothing downstream, which is what keeps it a root. Its acceptance evidence, unlike its implementation, completes only after later units exist — recorded on the supporting-unit column rather than as a DAG edge, because the reverse edge would close a cycle.

**Requirements carried (10).** REQ-ENG-5, **FR-P1-02-6**, FR-P1-03-2, FR-P1-05-12, FR-P1-06-1, FR-P1-06-2, FR-P1-06-3, FR-P1-06-4, NFR-PHASE-01, NFR-LIC-01

Bold = no §16/§19 test row (1 of 10 here).

**Acceptance rows (2).** TA-27, TA-28

**Blockers.** **BLK-01** — owned scope blocked: `src/data/locked_test.py`. Downstream units affected through its contract: `inventory-and-registry` (pre-G-05 coverage audit), `features-and-splits` (locked partition), `evaluation-and-comparison` (locked evaluation). Approval authority: the authorized project decision owner. Status: Open. `phase_contract.py` and `reuse_registry.py` are unblocked; the unit as a whole is **not** Approved while `locked_test.py` stands unbacked.

**Implementation notes and constraints.**

- `src/data/locked_test.py` is the second module with no authority backing until ADR-10 is countersigned.
- ADR-03 splits the locked-test guard deliberately: the access-log limb here, the execution limb in `features-and-splits`'s `splits.py`. `tests/test_locked_test_guard.py` covers both limbs and is owned by `features-and-splits` to keep this unit a root.
- The guard is at run time, not only in tests, because a Kaggle session carries no git working tree and a local suite run proves nothing about the environment a governed run executes in (ADR-02, Q3 = B).
- NFR-PHASE-01's transition-manifest hash-diff test has no module in the §12 tree and needs frozen artifacts from every later unit; it is carried as an acceptance row on `fixtures-and-reproducibility` with this unit supporting.
- The AGPLv3 Global-TEC-forecasting repository is the only approved direct-copy source today, and whether its distribution obligations permit that copying is an unresolved governance dependency; the standing default is reimplementation from the paper with a citation.

---

## 3. `acquisition` — Acquisition — prepared VTEC product, drivers, provenance

**Kind** `library` · **Complexity** L · **Deployment** standalone · **Depends on** `foundation`, `governance-guards`

**Responsibility.** Retrieve the approved Madrigal MAPGPS `gps` binned-VTEC product under D-144 and the three driver series (GFZ Kp/ap3 and Hp60/ap60, Kyoto WDC hourly Dst at one recorded release grade, Canadian observed F10.7), record full provenance for every retrieved file including its provider version suffix, retain native byte streams, hash one manifest entry per provider file, store gaps as explicit NaN, and close the ICTP rejected-source audit.

**Owns.**

- `scripts/00_acquire_prepared_vtec.py`
- `notebooks/00_acquire_phase1_vtec.ipynb` — the narrowly approved self-contained acquisition interface under D-144, importing nothing from `src/`
- `request_manifest.json` and `sha256_manifest.json` writers
- `tests/test_acquisition_window.py`

**Boundary.** The producer of every raw input the pipeline consumes. Hands downstream units resolved artifact paths and release IDs, never provider clients or credentials. Credentials reach the provider client directly from the environment via `foundation`'s resolution — never through a config file, log, registry note or notebook.

**Requirements carried (15).** REQ-ENG-13, FR-P1-00-1, FR-P1-00-2, FR-P1-01-1, FR-P1-01-2, FR-P1-01-3, FR-P1-01-4, **FR-P1-01-5**, FR-P1-01-6, **FR-P1-01-7**, **FR-P1-01-8**, **FR-P1-01-9**, **FR-P1-01-11**, **REQ-NFR-A1**, **REQ-NFR-A2**

Bold = no §16/§19 test row (7 of 15 here).

**Acceptance rows (1).** TA-32

**Implementation notes and constraints.**

- The `evidence/locked_test_restricted/audit_evidence_2022-FULL/` artifact D-9 promotes as Phase 1's acquisition input rests on twelve monthly runs whose provenance is unverifiable in principle: no provider byte stream exists in the workspace, and three of the twelve months (2022-04, 2022-07, and 2022-12, the locked month) have no `raw_isprint_cache/` at all. Every artifact produced before the re-acquisition carries that caveat, and FULL must not be relied on at a freeze gate while its provenance chain points at superseded per-month hashes.
- Re-acquisition must record each file's full provider filename including version suffix (`g.002` vs `g.003`), retrieval date and SHA-256, and surface rather than silently accept any mismatch against a previously recorded suffix.
- Membership is derived from record timestamps only — never from a directory name or filename. The year-blind predicate that filed locked-month records into `audit_evidence_2022-01/` is the realized defect this rule closes.
- `audit_ec1_drivers.py` and `merge_coverage_year.py` migrate onto the §12 structure here and in `external-products`/`inventory-and-registry` respectively; `audit_ec1_drivers.py:184` returning 0 regardless of missing months is a known gap against the two-tier error posture, to be fixed at migration.
- The F10.7 outage window from 2022-03-18 must have its measured gap recorded and governed before any imputation, substitution or reconstruction is considered.

---

## 4. `inventory-and-registry` — Inventory and Station Registry — sources, stations, the G-P1A coverage gate

**Kind** `library` · **Complexity** M · **Deployment** standalone · **Depends on** `acquisition`

**Responsibility.** The source inventory (TE §5.1's nine fields per entry, including which configuration consumes each source), the station registry (coordinates, the coordinate-to-cell rule, Vision §6.2's full content with one pinned IGRF version), schema validation of the prepared product, and the performance-blind coverage and regime audit that G-P1A accepts — including December, with an access-log row written first.

**Owns.**

- `src/data/inventory.py`, `src/data/registry.py`
- `scripts/01_inventory_and_registry.py`
- `tests/test_station_registry.py`

**Boundary.** Consumes `acquisition`'s released artifacts by release ID and hash. Publishes the station registry and the source inventory that `target-standardization` and `external-products` both read. Does not transform provider values.

**Requirements carried (7).** FR-P1-02-1, FR-P1-02-2, FR-P1-02-3, FR-P1-02-4, FR-P1-02-5, **FR-P1-02-7**, **FR-P1-02-8**

Bold = no §16/§19 test row (2 of 7 here).

**Acceptance rows (3).** WS-01, TA-04, TA-25

**Implementation notes and constraints.**

- The notebook's inline ARUC/BSHM/NICO coordinates and its coordinate-to-cell rule are self-labelled PROVISIONAL and are §18.2 forbidden-choice items (coordinates: Student; cell-selection rule: Student + Supervisor). Per the affirmed practice they are frozen as a D-number decision **first**, and only then moved into `configs/data.yaml` and `src/data/registry.py` and validated against the official IGS site logs.
- The December coverage and regime audit is required before G-05 and is performance-blind. It is a different event from the one-shot locked evaluation, and the "open it once" rule governs only the latter.
- G-P1A acceptance is decided against Vision §6.1B's coverage minimum, frozen 2026-08-21 as D-12.
- `merge_coverage_year.py` migrates here, taking `--config configs/` and its `NN_verb_noun.py` position; its `sha256_of_file` copy consolidates into `foundation`'s `src/data/release.py`.

---

## 5. `target-standardization` — Target Standardization — the Phase 1 hourly target and its verification

**Kind** `library` · **Complexity** M · **Deployment** standalone · **Depends on** `inventory-and-registry`

**Responsibility.** Turn validated provider files into the Phase 1 hourly target rows under D-17's contract — documented QC, UTC normalization, cell selection and the stated hourly aggregation only, with provider values preserved — stamp `phase_id`, `source_id` and `target_definition_id` on every row, label the product location-sampled gridded VTEC, and produce the Phase 1 portion of the verification and target-uncertainty evidence.

**Owns.**

- `src/data/prepared.py`
- `scripts/02_standardize_prepared_target.py`
- `scripts/03_verify_processing.py` (Phase 1 scope)
- the D-17 target-schema test — **unnamed, and deliberately so: see BLK-05.** FR-P1-03-5's criterion implies a test that exists in none of the mandated test-module sets (the 17 in TE §12's tree, `test_acquisition_window.py` as the countersigned 18th, `tests/test_determinism.py` as ADR-10's proposed 19th). Naming it is a §12 tree amendment and therefore supervisor-owned; this stage records the obligation and chooses no name.

**Boundary.** Phase 1 only. Reads validated provider files and the registry; emits the target rows every downstream unit consumes. Must never produce a DCB, STEC, mapping, satellite or arc field, and must never label the gridded product a receiver-specific station observation.

**Requirements carried (6).** FR-P1-03-1, FR-P1-03-3, FR-P1-03-4, **FR-P1-03-5**, NFR-TDEF-01, NFR-DQ-01

Bold = no §16/§19 test row (1 of 6 here).

**Acceptance rows (1).** TA-19

**Blockers.** **BLK-05** — owned scope blocked: the D-17 target-schema test, which has no module name and no §12 tree entry. Downstream unit: `features-and-splits`, which consumes the target rows the test would validate. Required resolution: `functional-design` (3.1) names the module; the resulting §12 tree amendment is tracked the way ADR-10's count is. Approval authority: Supervisor. Status: Open — this stage chooses no name.

**Implementation notes and constraints.**

- The `02` ordinal is shared with Phase 2's `scripts/02_build_vtec_target.py`. The reading adopted upstream: the ordinal denotes the pipeline position and `--phase` selects exactly one, so a clean run contains one `02` per phase. This is a recorded §12 defect, not a resolved one, and `code-generation` must not invent a `02a`/`02b` convention.
- `03_verify_processing.py`'s Phase 1 scope is thinner than its §12 description implies: four of Vision §6.9's six uncertainty contents are Phase 2 quantities barred from Phase 1. `functional-design` settles exactly what it runs.
- No numerical equivalence may be claimed between the Phase 1 and Phase 2 targets; cross-phase results test protocol transfer across a target-domain shift.

---

## 6. `external-products` — External Products — drivers, the IRI benchmark, the GIM comparator

**Kind** `library` · **Complexity** L · **Deployment** standalone · **Depends on** `inventory-and-registry`

**Responsibility.** Build the three externally sourced product families: the driver series with their availability semantics (Kp/ap3 within its own 3-hour interval, Dst on its hourly interval, F10.7 at the previous-day observed value with a trailing 81-day mean ending at the safe-lagged day), the IRI-2016 benchmark with its pre-generation validation, and the CODE final GIM comparator with its interpolation and network-overlap audit.

**Owns.**

- `src/external/spaceweather.py`, `src/external/iri.py`, `src/external/gim.py`
- `scripts/04_build_external_products.py`

**Boundary.** `iri.py` and `gim.py` are importable by exactly two places — this unit's own `scripts/04_build_external_products.py` and `evaluation-and-comparison`'s `src/evaluation/` — stated as an allowlist, so an import from `src/data`, `src/gnss`, a training script or a notebook violates it identically. `spaceweather.py` is deliberately outside that restriction: drivers are model inputs subject to the availability lags.

**Requirements carried (7).** **REQ-ENG-9**, FR-P1-04-3, **FR-P1-04-4**, FR-P1-04-9, **FR-P1-04-15**, **FR-P1-04-17**, **FR-P1-04-18**

Bold = no §16/§19 test row (5 of 7 here).

**Acceptance rows (1).** WS-09

**Implementation notes and constraints.**

- Driver series are time-indexed only — one value per epoch, identical across all three cells. A join must never imply a per-cell measurement, and a station performance difference must never be attributed to local forcing the dataset does not contain.
- No driver may be backfilled from future final or definitive archived values, and Kyoto Dst release grades must never be mixed within one series.
- Dst is diagnostic/hindcast-only and never a confirmatory ML feature. Provisional Dst may characterise fixture selection only — never a modelling input, a frozen tolerance, or a G-05 regime count.
- A centered rolling mean for F10.7 is a defect, not a fallback.
- IRI-2016 generation is blocked if its validation report fails. Nothing in this unit's output may reach training or inference: IRI and GIM join only at evaluation time onto the already-frozen comparison-wide mask.
- `audit_ec1_drivers.py` migrates here, gaining `--config configs/` and its numbered position; its exit-code gap (returning 0 regardless of missing months) is closed at migration.

---

## 7. `features-and-splits` — Features and Splits — the permitted ML input space, folds, embargo

**Kind** `library` · **Complexity** L · **Deployment** standalone · **Depends on** `target-standardization`, `external-products`, `governance-guards`

**Responsibility.** Construct the closed ML input space and the partitions that make forecasting honest: the availability matrix asserting actual lag ≥ declared safe lag per feature, feature construction that raises on anything outside the §6.2 dictionary or carrying an `iri_*` field, per-fold train-only transforms, one shared window definition emitting both the flattened matrix and the sequence tensor, the F1–F4 exact calendar folds with their 24-hour embargo, and the December locked partition's execution guard.

**Owns.**

- `src/features/availability.py`, `build.py`, `transforms.py`, `windows.py`
- `src/data/splits.py` — F1–F4, the 24-hour embargo, `materialise_locked_partition` (the execution limb of ADR-03's split guard)
- `scripts/05_build_features_and_splits.py`
- `tests/test_feature_availability.py`, `tests/test_iri_denial.py`, `tests/test_split_embargo.py`, `tests/test_train_only_transforms.py`, `tests/test_locked_test_guard.py`

**Boundary.** Imports `target-standardization`, `external-products`'s `spaceweather` only, and `governance-guards`. Must not import `src/external/iri.py`, `src/external/gim.py` or any `src/gnss` module. `windows.py` owning both representations is what makes matched-window parity checkable rather than aspirational.

**Requirements carried (11).** FR-P1-04-1, FR-P1-04-2, FR-P1-04-5, FR-P1-04-6, FR-P1-04-8, **FR-P1-04-10**, **FR-P1-04-12**, **FR-P1-04-13**, **FR-P1-04-16**, NFR-IRI-01, NFR-LEAK-01

Bold = no §16/§19 test row (4 of 11 here).

**Acceptance rows (9).** WS-10, WS-11, WS-12, WS-13, WS-18, TA-07, TA-08, TA-11, TA-18

**Blockers.** **BLK-04** — owned scope blocked: `src/features/transforms.py`'s `fit_transforms` / `apply_transforms` pair, and every assertion of NFR-LEAK-01 that runs through it. Downstream units affected: `models-and-baselines`, `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting` — every reported number inherits the fit. Required resolution: a governed cross-unit contract enforcing train-only fitting per fold, defining input and output types, alignment requirements, ownership of the fitted state, allowed partitions (the named fold's training partition only) and failure conditions (`LeakageError` when `train`'s index is not a subset of that partition), so validation and locked-test leakage are prevented by the contract rather than by review. Approval authority: `functional-design` (3.1) for the contract; Supervisor for the leakage evidence at G-04 and G-05. Status: Open — must be discharged **before** this unit or any downstream unit above enters functional design or implementation.

**Implementation notes and constraints.**

- Five forbidden edges here have no §16/§19 row — dictionary closure, the `vtec_lag_*` carry-forward prohibition, driver-interval repetition, support-field rules, and the target-lag contract. Each is designed as a raise at a named call site so a test *can* assert it; writing those criteria is a `requirements.md` change and is carried forward to 3.2.
- `fit_transforms(train, *, fold=...)` types `train` as an unconstrained DataFrame, so the two-function split prevents the single-call convenience shape but not the underlying full-dataset fit. Per the advisory finding on `decisions.md`, either narrow the claim or add a runtime assertion that `train`'s index is a subset of the fold's training partition, raising `LeakageError` otherwise.
- `tests/test_locked_test_guard.py` is owned here because it exercises both limbs and this unit already depends on `governance-guards`; assigning it there would close a cycle. `governance-guards` is the supporting unit on WS-18 and TA-18.
- Raw longitude never enters as a predictor — longitude enters only through `lst_sin` and `lst_cos`.
- Missing driver values carry forward at most 3 hours, then the row is excluded.

---

## 8. `models-and-baselines` — Models and Baselines — six families, three seeds, checkpoints

**Kind** `library` · **Complexity** L · **Deployment** standalone · **Depends on** `features-and-splits`

**Responsibility.** Implement and run the six model families — persistence (M-01), 24-hour seasonal persistence (M-02), station×month×hour climatology fitted on training partitions only (M-03), Ridge with its grid of 6 (M-04), Random Forest with its grid of 18, direct only (M-05), and the compact LSTM with its grid of 16, direct only (M-06) — plus training orchestration, the three-seed run whose element-wise mean is the confirmatory prediction, lowest-validation-RMSE checkpointing and restore, and the predeclared ablations.

**Owns.**

- `src/models/persistence.py`, `climatology.py`, `ridge.py`, `random_forest.py`, `lstm.py`, `train.py`, `checkpoint.py`
- `scripts/06_train_and_predict.py`
- `tests/test_models_smoke.py`, `tests/test_checkpoint_restore.py`

**Boundary.** Imports `features-and-splits` and `foundation`. Must not import `src/external/iri.py`, `src/external/gim.py` or `src/evaluation` — that dependency runs the other way. Residual and GRU modules are absent by design and their absence is grep-evidenced. TensorFlow/Keras is the only NN stack; PyTorch is prohibited.

**Requirements carried (9).** **FR-P1-04-14**, FR-P1-05-1, FR-P1-05-2, **FR-P1-05-3**, **FR-P1-05-4**, **FR-P1-05-5**, **FR-P1-05-6**, **FR-P1-05-21**, **FR-P1-05-22**

Bold = no §16/§19 test row (7 of 9 here).

**Acceptance rows (5).** WS-14, WS-15, TA-12, TA-13, TA-26

**Blockers.** **BLK-03** — owned scope blocked: `src/models/train.py`'s confirmatory-prediction path, this being the unit that owns confirmatory-prediction construction. Downstream units consuming that prediction: `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`. Required resolution: a governed cross-unit contract defining input and output types, alignment requirements, ownership of the frozen seed set, allowed partitions and failure conditions, with the frozen set arriving as a parameter from `ConfigSnapshot.seeds` — never inlined in `src/models`, never weakened to a distinctness check. Approval authority: `functional-design` (3.1) for the contract; Supervisor for the seed values, D-122's sign-off still pending per Vision §14.2. **BLK-04 ↓** inherited from `features-and-splits`. Status: Open — BLK-03 must be discharged **before** this unit or any downstream unit above enters functional design or implementation.

**Implementation notes and constraints.**

- `three_seed_mean(predictions)` as designed takes no seeds parameter yet claims to raise when the seeds are not exactly the frozen set. Per the advisory finding on `component-methods.md`, add a frozen-seed-set parameter sourced from `ConfigSnapshot.seeds` at the call site — otherwise the only implementations are an inlined `{1337, 2024, 7}` (forbidden: no scientific constant in source) or a weaker pairwise-distinctness check that a wrong-but-distinct triple would pass.
- Tuning uses January–November only. The trigger is December being **seen**, not the locked test being opened — the required pre-G-05 coverage audit means December is legitimately seen earlier, and that is precisely the channel this rule closes.
- No Random Forest importance score may add, remove or rank a feature into the production feature set; RF importance is a non-authoritative diagnostic figure only.
- No seed is selected on validation or after seeing December. Grids are exact and committed to configuration before G-05 and never change after December is seen.
- Ablations are predeclared as named runs in `experiment.yaml`; `ABL-DIFF` inverse-transforms to absolute TECU before any metric, and `ABL-HIST48` runs only after the primary configuration is frozen.
- The +24 h horizon is implemented and testable, excluded only from the default run list.

---

## 9. `evaluation-and-comparison` — Evaluation and Comparison — masks and the confirmatory estimand

**Kind** `library` · **Complexity** M · **Deployment** standalone · **Depends on** `models-and-baselines`, `external-products`

**Responsibility.** The comparison mechanics: one comparison-wide intersection mask computed once per comparison set with a stable ID and reported row counts, the IRI-free denial check applied at join time, and the confirmatory estimand — the mean within-station difference of squared errors, benchmark minus model, with equal-station weighting, positive favouring the model.

**Owns.**

- `src/evaluation/masks.py`, `src/evaluation/metrics.py`
- `scripts/07_evaluate_and_report.py`
- `tests/test_common_masks.py`

**Boundary.** The only unit permitted, with `external-products`'s own build script, to import `src/external/iri.py` and `src/external/gim.py`, and it does so at evaluation time against the already-frozen mask. Imports `models-and-baselines` outputs; nothing imports it except the two units whose logic runs inside its script.

**Requirements carried (4).** FR-P1-04-7, **FR-P1-05-7**, **FR-P1-05-17**, NFR-FAIR-01

Bold = no §16/§19 test row (2 of 4 here).

**Acceptance rows (1).** WS-16

**Blockers.** **BLK-03 ↓** — this unit consumes the confirmatory prediction, so its masks and paired loss differential inherit whatever `three_seed_mean`'s contract turns out to permit. **BLK-04 ↓** — every metric it computes inherits the transform fit. Neither is owned here; both must be discharged before this unit enters functional design or implementation. Approval authority: as recorded on BLK-03 and BLK-04. Status: Open (inherited).

**Implementation notes and constraints.**

- Never a pairwise or model-specific mask. One comparison-wide mask per comparison set, or the comparison is not fair.
- Evaluation code is authored, reviewed and frozen as part of the G-05 set before December is opened. No evaluation code exists at intent time.
- The spatial-representativeness mismatch must be stated wherever an IRI or GIM comparison is reported: Phase 1 compares a grid cell against a station-coordinate evaluation, and part of any measured difference is a geometry and sampling artefact rather than skill.
- The locked-test predictions are generated and written exactly once, after G-05 is signed, and hashed before any metric is computed.

---

## 10. `statistical-inference` — Statistical Inference — the vector time-block bootstrap

**Kind** `library` · **Complexity** M · **Deployment** embedded · **Depends on** `evaluation-and-comparison`

**Responsibility.** Uncertainty on the confirmatory estimand: the vector time-block bootstrap with 24-hour blocks carrying all three stations together, 10,000 replicates, its own generator seeded from the separately frozen 20221201, a 95% confidence interval, a 48-hour sensitivity, and the cross-station paired-error correlation reported.

**Owns.**

- `src/evaluation/bootstrap.py`
- `tests/test_bootstrap.py`

**Boundary.** Runs inside `scripts/07_evaluate_and_report.py`; owns no stage script of its own. Takes its seed as a required parameter read from `seeds.yaml`, never defaulted and never inlined.

**Requirements carried (1).** FR-P1-05-8

Bold = no §16/§19 test row (0 of 1 here).

**Acceptance rows (2).** WS-17, TA-14

**Blockers.** **BLK-03 ↓**, **BLK-04 ↓** — the bootstrapped differential is computed from the confirmatory prediction over transform-fitted features, so both inherited contracts bound what this unit's intervals mean. Neither is owned here. Approval authority: as recorded on BLK-03 and BLK-04. Status: Open (inherited) — discharge required before functional design or implementation.

**Implementation notes and constraints.**

- A within-station or naive bootstrap must never be substituted — it produces systematically narrower intervals. The within-station 2,000-replicate variant was rejected at Q-27.
- This unit carries the heaviest CPU cost in the pipeline: 10,000 replicates over 24-hour vector blocks, inside TE §9.3's 10.0 GB hard planning envelope, on a CPU path that is complete rather than an emergency mode.
- Its seed is carved out from `foundation`'s centralised determinism by ADR-05 on purpose; the carve-out is a design decision, not an oversight.

---

## 11. `regimes-diagnostics-reporting` — Regimes, Diagnostics and Reporting — breakdowns, figures, claims

**Kind** `library` · **Complexity** L · **Deployment** embedded · **Depends on** `statistical-inference`

**Responsibility.** Everything between a computed interval and a defensible statement: Kp/Hp60 regime strata and the §9.3 storm-event rule, quality strata over the measured-available fields with the top-1%-removed sensitivity, the required prediction/residual/target-support/quality plots each carrying its source-data IDs, the primary results table with its three mandatory difficulty controls, the mandated disclosures, and the claims-and-limitations checklist.

**Owns.**

- `src/evaluation/regimes.py`, `diagnostics.py`, `plots.py`
- `notebooks/01_data_and_target_audit`, `02_proc...`, `03_...`, `04_...` — the four analysis/review notebooks
- the claims-and-limitations checklist artifact

**Boundary.** Runs inside `scripts/07_evaluate_and_report.py` and the four review notebooks; owns no stage script. `plots.py` is presentation only and computes no reported quantity. The notebooks declare expected versions and IDs and call `src/` modules — a notebook never holds the only copy of parsing, calibration, feature, split, training, evaluation or bootstrap logic.

**Requirements carried (11).** REQ-ENG-12, FR-P1-05-9, FR-P1-05-10, FR-P1-05-11, **FR-P1-05-14**, **FR-P1-05-15**, **FR-P1-05-16**, **FR-P1-05-18**, **FR-P1-05-19**, **FR-P1-05-20**, **REQ-CLAIM-01**

Bold = no §16/§19 test row (7 of 11 here).

**Acceptance rows (3).** WS-19, TA-16, TA-20

**Blockers.** **BLK-03 ↓**, **BLK-04 ↓** — every reported number, breakdown, figure and claim in this unit derives from the confirmatory prediction and the transform-fitted features, so both inherited contracts bound what may be claimed. Neither is owned here. Approval authority: as recorded on BLK-03 and BLK-04. Status: Open (inherited) — discharge required before functional design or implementation.

**Implementation notes and constraints.**

- The advisory NOT-READY finding carried from 2.3 lands here: FR-P1-05-18 requires the storm-event count to come from GFZ Kp/Hp60 at a recorded release grade and bars any provisional-Dst-derived figure, but no criterion tests that source. The designed signature makes the source an explicit required argument so a test *can* assert it; writing the criterion is a `requirements.md` change.
- Any baseline that beats the LSTM on the locked test appears in the primary results table **and** in the abstract-level conclusion. A favourable LSTM-versus-IRI result never licenses silence about an unfavourable LSTM-versus-persistence or LSTM-versus-climatology result.
- The three difficulty controls are co-reported in the same primary table, never relegated to an appendix.
- Phase 2 must be described in the abstract-level interpretation as a fixed-protocol replication on a new target lineage, **not** a second statistically independent blind test.
- Every claim is bounded to the frozen scope: hourly VTEC at ARUC 40/44, BSHM 32/35, NICO 35/33, calendar 2022, tested on December 2022 only. Any question requiring 5-minute resolution at NICO is out of reach on this dataset and must not be claimed.
- No practical-relevance threshold may be introduced, changed or reinterpreted after December is opened; any test-driven pipeline change made after locked-test access is labelled exploratory.

---

## 12. `fixtures-and-reproducibility` — Fixtures and Reproducibility — the two walking-skeleton fixtures and the clean run

**Kind** `library` · **Complexity** M · **Deployment** standalone · **Depends on** `acquisition`, `inventory-and-registry`, `target-standardization`, `external-products`, `features-and-splits`, `models-and-baselines`, `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`

**Responsibility.** The ordering contract and its evidence: the seven-day single-station plumbing fixture (smoke only), the one-month all-station scientific fixture, their manifests carrying identity, input hashes, expected schema, row-count ranges, support and missingness limits, timestamp tolerances, required outputs, measured CPU runtime range and permitted floating-point tolerances, the orchestrator that enforces both-in-order before any full-year job, and the §13.2 ordered clean-run contract reproduced on CPU.

**Owns.**

- `scripts/run_walking_skeleton.py`
- `tests/fixtures/plumbing_7day/fixture_manifest.yaml`, `tests/fixtures/scientific_1month/fixture_manifest.yaml`
- `tests/test_clean_run.py`
- the traceability matrix and the `environment_and_cpu_preflight_report`

**Boundary.** Invokes every stage script; implements no domain logic of its own. Direct edges run to nine units, for two distinct reasons. Seven own a stage script the clean-run sequence invokes directly rather than transitively: `acquisition`, `inventory-and-registry`, `target-standardization`, `external-products`, `features-and-splits`, `models-and-baselines`, `evaluation-and-comparison`. The remaining two, `statistical-inference` and `regimes-diagnostics-reporting`, own **no** stage script — both are `embedded` and run inside `07_evaluate_and_report.py`, which `evaluation-and-comparison` owns — so their edges rest on the artifacts the clean-run tolerance comparison and the traceability matrix consume, not on a script invocation.

**Requirements carried (8).** FR-WS-1, **FR-WS-2**, **FR-WS-3**, FR-WS-4, FR-WS-5, FR-WS-6, NFR-REP-01, REQ-NFR-A3

Bold = no §16/§19 test row (2 of 8 here).

**Acceptance rows (4).** WS-20, TA-09, TA-17, TA-21

**Blockers.** **BLK-02** — owned scope blocked: `tests/fixtures/plumbing_7day/fixture_manifest.yaml` and every capability depending on it. The unit exists in the DAG with its nine dependencies recorded, but the manifest-dependent capability is blocked by `application-design` § Known defects row 12; **no manifest may be invented, inferred or substituted**, and this unit cannot pass its completion gate until the defect is resolved and the authoritative manifest is available and hash-verifiable. Approval authority: Supervisor. **BLK-01** — owned scope blocked: TE §13.2's `PYTHONHASHSEED` clean-run clause, which `test_clean_run.py`, WS-20 and TA-17 test as written. Approval authority: the authorized project decision owner. Status: both Open.

**Implementation notes and constraints.**

- **Blocked.** § Known defects row 12 — the `plumbing_7day` station count — is contested: TE §15.1 mandates one station, D-11 froze the window across all three cells, and no reading is adopted. The fixture manifest cannot state its identity until a supervisor resolves it, and `run_walking_skeleton.py` reads that manifest.
- The seven-day fixture is never scientific evidence — it may not be cited, plotted as a result, or interpreted as skill.
- D-11 froze the plumbing window as 2022-11-01 to 2022-11-07 inclusive, all three cells, with measured completeness ARUC 163/168, BSHM 168/168, NICO 155/168 and 7/7 day presence in every cell, carrying the limitation that it reproduces neither December's winter-solstice regime nor its activity distribution. The one-month all-station scientific window remains open under Q-31.
- No record whose observation date falls in December 2022 may enter either fixture, asserted on record dates rather than on the folder a file was filed under.
- The critical test set and both fixtures must run **inside the Kaggle session** before any governed run executed there — a Kaggle session carries no git working tree, so a commit hook cannot fire and a local suite run proves nothing about the environment the governed run executes in.
- NFR-PHASE-01's transition-manifest hash-diff test is carried here as an acceptance row, with `governance-guards` supporting: the test has no §12 module and its evidence needs the frozen artifacts every earlier unit produces.

---

## Blocker register — structural presence is not readiness

**The distinction this section exists to hold.** A unit may be present in the
DAG, carry documented dependencies and ownership, and still be blocked. A
blocked unit is **not** sequenced for implementation and **not** marked
accepted, Ready or complete until its named blocker is discharged. No blocked
unit is omitted from the DAG to make the topology look clean, and no unresolved
artifact is allowed to read as approved. Where a blocker touches only part of a
unit, the affected scope is what is blocked — the unit's other work is not
blessed by the narrowness, and the register names the files so the boundary is
checkable rather than asserted.

Nothing in this register is resolved here. Every row names the authority that
discharges it.

### BLK-01 — ADR-10's §12/§13.2 amendment is unsigned

Tracked per unit **and** per file, because approval arrives for the amendment as
a whole and a partially-built unit must not read as covered.

| Affected artifact | Owning unit | Downstream units | Status |
|---|---|---|---|
| `src/data/config.py` | `foundation` | every unit — the six-step stage entry contract calls `load_configs`, `assert_no_tbd` and `resolve_platform_roots` before any domain work | Open — no authority backing |
| `tests/test_determinism.py` | `foundation` | `models-and-baselines` (TA-26's deterministic seed utility and serialization restore), `statistical-inference` | Open — no authority backing |
| `src/data/locked_test.py` | `governance-guards` | `inventory-and-registry` (the pre-G-05 coverage audit), `features-and-splits` (the locked partition), `evaluation-and-comparison` (the locked evaluation) | Open — no authority backing |
| TE §13.2's `PYTHONHASHSEED` clean-run clause | `fixtures-and-reproducibility` | none — terminal, but `test_clean_run.py`, WS-20 and TA-17 test the sequence **as written** | Open — clause not yet amended |

- **Required resolution.** ADR-10's four-part amendment recorded and countersigned as one change record, the way `test_acquisition_window.py`'s addition was countersigned on 2026-08-16. REQ-ENG-4's test-module count moves 18 → 19 in its two genuine loci (REQ-ENG-4 itself and the external TE §12 tree); `team-practices.md` § Testing Posture states a deliberately different figure and is not one of them.
- **Approval authority.** The authorized project decision owner — student, with supervisor countersignature. `project.md` § Forbidden bars an agent from filling a supervisor-owned value by convenience, and a tree amendment is that class of change.
- **Consequence while open.** `code-generation` must not create these three modules or the amended clean-run command on the strength of ADR-10 alone.

### BLK-02 — the `plumbing_7day` fixture manifest cannot state its identity

| Field | Value |
|---|---|
| Affected artifact | `tests/fixtures/plumbing_7day/fixture_manifest.yaml` |
| Owning unit | `fixtures-and-reproducibility` |
| Downstream units | none — the unit is terminal. The block reaches WS-20, TA-09 and TA-17, and through TE §9.2's intra-unit ordering contract it reaches every full-year job. |
| Required resolution | `application-design` § Known defects row 12 resolved: TE §15.1 mandates one station, D-11 froze the window across all three cells, and no reading is adopted. The authoritative manifest must then be available and hash-verifiable. |
| Approval authority | Supervisor |
| Status | Open. **No manifest may be invented, inferred or substituted**, and the unit cannot pass its completion gate until the defect is discharged. |

### BLK-03 — `three_seed_mean` cannot express the frozen-seed check

| Field | Value |
|---|---|
| Affected artifact | `src/models/train.py` — the `three_seed_mean(predictions)` signature in `component-methods.md` |
| Owning unit | `models-and-baselines` (confirmatory-prediction construction) |
| Downstream units | `evaluation-and-comparison` (masks and the paired loss differential consume the confirmatory prediction), `statistical-inference` (bootstraps that differential), `regimes-diagnostics-reporting` (reports it) |
| Required resolution | A governed cross-unit contract fixing input and output types, alignment requirements, ownership of the frozen seed set, allowed partitions, and failure conditions. The frozen set reaches the function as a parameter sourced from `ConfigSnapshot.seeds` — never inlined, since `{1337, 2024, 7}` in `src/models` is the forbidden pattern, and never weakened to a pairwise-distinctness check a wrong-but-distinct triple would pass. |
| Approval authority | The contract: `functional-design` (3.1). The seed values themselves: Supervisor — D-122's sign-off is still pending per Vision §14.2. |
| Status | Open. Must be discharged **before** `models-and-baselines` or any downstream unit above enters functional design or implementation. |

### BLK-04 — `fit_transforms` leaves the full-dataset fit representable

| Field | Value |
|---|---|
| Affected artifact | `src/features/transforms.py` — the `fit_transforms(train, *, fold)` / `apply_transforms(...)` pair in `component-methods.md`, and ADR-01's claim about it |
| Owning unit | `features-and-splits` |
| Downstream units | `models-and-baselines` (trains on the transformed features), `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting` — every reported number inherits the fit |
| Required resolution | A governed cross-unit contract that enforces train-only fitting per fold: input and output types, alignment requirements, ownership of the fitted state, allowed partitions (the named fold's training partition only), and failure conditions — a `LeakageError` when `train`'s index is not a subset of that partition. The two-function split prevents the single-call convenience shape and nothing more; the contract is what closes the leak. |
| Approval authority | The contract: `functional-design` (3.1). The leakage evidence it produces: Supervisor, at G-04 and G-05 (NFR-LEAK-01). |
| Status | Open. Must be discharged **before** `features-and-splits` or any downstream unit above enters functional design or implementation. |

### BLK-05 — the D-17 target-schema test has no module and no §12 entry

| Field | Value |
|---|---|
| Affected artifact | the D-17 target-schema test implied by FR-P1-03-5's criterion — present in no mandated test-module set |
| Owning unit | `target-standardization` |
| Downstream units | `features-and-splits` (consumes the target rows the test would validate) |
| Required resolution | `functional-design` (3.1) names the module. Because TE §12 fixes the tree to file level, adding it is a further tree amendment whose count impact is tracked the way ADR-10's 18 → 19 is tracked. **This stage chooses no name.** |
| Approval authority | Supervisor — a §12 tree amendment |
| Status | Open |

### Roll-up by unit

| Unit | Blockers | Blocked scope |
|---|---|---|
| `foundation` | BLK-01 | `src/data/config.py`, `tests/test_determinism.py`. The unit's other owned artifacts are unblocked. |
| `governance-guards` | BLK-01 | `src/data/locked_test.py`. `phase_contract.py` and `reuse_registry.py` are unblocked. |
| `target-standardization` | BLK-05 | the D-17 schema test only. |
| `features-and-splits` | BLK-04 | `transforms.py` and everything asserting NFR-LEAK-01 through it. |
| `models-and-baselines` | BLK-03 | `train.py`'s confirmatory-prediction path. |
| `evaluation-and-comparison` | BLK-03 (downstream) | anything consuming the confirmatory prediction. |
| `statistical-inference` | BLK-03, BLK-04 (downstream) | the bootstrapped differential. |
| `regimes-diagnostics-reporting` | BLK-03, BLK-04 (downstream) | every reported number derived from the above. |
| `fixtures-and-reproducibility` | BLK-01, BLK-02 | the clean-run clause and the `plumbing_7day` manifest — jointly, its completion gate. |
| `acquisition`, `inventory-and-registry`, `external-products` | — | none of their own; both depend on BLK-01's artifacts through the stage entry contract. |

Per Q7, no unit above may be described as independent-and-ready while a blocker
naming it stands, and independence in `unit-of-work-dependency.md` § Independent
unit sets is a statement about the graph, never about readiness.

## Assumptions & Open Questions

- **[assumption]** `REQ-ENG-5` ("every hard rule has a negative-path test") is a property of the whole suite rather than of one module. It is assigned to `governance-guards` as the unit that owns the negative-control discipline and the independent checks, with `features-and-splits`, `models-and-baselines` and `fixtures-and-reproducibility` recorded as supporting. No other unit was a better single owner, and leaving it unassigned would have broken both-direction coverage.
- **[assumption]** `FR-P1-01-10` (credentials and secrets) is assigned to `foundation`, which owns the environment and platform-root resolution that supplies them, with `acquisition` supporting as the unit that consumes them. The requirement sits in the FR-P1-01 acquisition group, so this placement follows the mechanism rather than the numbering.
- **Upstream drift, recorded not propagated.** `components.md` states "94 requirement rows"; the count derived from `requirements.md` here is **105**, the difference being IDs added in stage 2.3's fourth through sixth revisions. This stage uses 105.
- **Open, supervisor-owned.** ADR-10's four-part §12/§13.2 amendment; D-122's sign-off; § Known defects row 12 (the `plumbing_7day` station count); the one-month all-station scientific fixture window (Q-31).
- **Open, a `requirements.md` change.** The advisory NOT-READY finding on FR-P1-05-18 (no criterion tests the storm-event count's source) and the 40 requirements with no §16/§19 row. Both are inputs to stages 3.1 and 3.2, not resolvable here.
- **Open, a §12 defect.** The `02` ordinal collision between the Phase 1 and Phase 2 target scripts, carried from `services.md` unresolved.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

