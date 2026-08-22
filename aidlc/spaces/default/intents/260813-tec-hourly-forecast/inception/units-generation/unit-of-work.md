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
| 1 | `foundation` | `library` | M | shared | 16 | 7 | — (BLK-01 closed 2026-08-22) |
| 2 | `governance-guards` | `library` | M | shared | 10 | 2 | BLK-06 (BLK-01 closed 2026-08-22) |
| 3 | `acquisition` | `library` | L | standalone | 15 | 1 | BLK-07 |
| 4 | `inventory-and-registry` | `library` | M | standalone | 7 | 3 | — |
| 5 | `target-standardization` | `library` | M | standalone | 6 | 1 | BLK-05 |
| 6 | `external-products` | `library` | L | standalone | 7 | 1 | — |
| 7 | `features-and-splits` | `library` | L | standalone | 11 | 9 | BLK-04 |
| 8 | `models-and-baselines` | `library` | L | standalone | 9 | 5 | BLK-03, BLK-04 ↓ |
| 9 | `evaluation-and-comparison` | `library` | M | standalone | 4 | 1 | BLK-03 ↓, BLK-04 ↓ |
| 10 | `statistical-inference` | `library` | M | embedded | 1 | 2 | BLK-03 ↓, BLK-04 ↓ |
| 11 | `regimes-diagnostics-reporting` | `library` | L | embedded | 11 | 3 | BLK-03 ↓, BLK-04 ↓ |
| 12 | `fixtures-and-reproducibility` | `library` | M | standalone | 8 | 4 | BLK-02, BLK-03 ↓, BLK-04 ↓ (BLK-01 closed 2026-08-22) |

Blocker column: an unmarked ID is a blocker whose affected artifacts this unit
owns; **↓** marks one inherited through a contract this unit consumes. **BLK-01,
closed 2026-08-22, formerly reached every unit** through the six-step stage entry
contract and was listed only against the two units that owned its files; its
closure is recorded in § Blocker register and the column no longer carries it as
open. § Blocker register below carries each blocker in full — affected
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
- `artifacts/` — the top-level output tree REQ-ENG-1 enumerates and TA-01 checks. Owned here because this unit creates the skeleton and owns the release API that writes into it; every other unit writes its released artifacts *into* this tree without owning it.
- `tests/` tree and shared fixtures/conftest, `tests/test_determinism.py` (**NEW**), `tests/test_release_hashes.py`

**Boundary.** The only unit that reads `configs/`, and (with `acquisition`) one of two permitted to construct a path into `evidence/` — **except `evidence/locked_test_restricted/`, which only `src/data/locked_test.py` may reach**. `component-dependency.md` § Shared resources fixes that carve-out without qualification ("nothing else may construct a path into it"), and D-15 records why it matters: the restricted root is a governance boundary, not an access control, so it holds only while exactly one code path reaches it. See **BLK-07**. Exposes `ConfigSnapshot`, the seeded-run contract, resolved platform roots and the release API. Imports nothing from any other unit — this is the DAG's first root.

**Requirements carried (16).** REQ-ENG-1, REQ-ENG-2, REQ-ENG-3, REQ-ENG-4, REQ-ENG-6, **REQ-ENG-7**, REQ-ENG-8, **REQ-ENG-10**, REQ-ENG-11, FR-P1-01-10, FR-P1-04-11, FR-P1-05-13, FR-WS-7, NFR-AUD-01, NFR-SEC-01, NFR-DET-01

Bold = no §16/§19 test row (2 of 16 here).

**Acceptance rows (7).** TA-01, TA-02, TA-03, TA-10, TA-15, TA-22, TA-23

**Blockers.** **None open. BLK-01 closed 2026-08-22** (`CR-2026-08-22-TE-AMEND`, on `GOV-2026-08-22-REM-01` Recs 1 and 4): `src/data/config.py` and `tests/test_determinism.py` are now named in TE §12. **Authority only** — neither module exists, and creating them stays gated by **G-09**, TE §18.3's stop-and-report rule and stage **3.5 `code-generation`**. This unit's other owned artifacts were never blocked. See § Blocker register.

**Implementation notes and constraints.**

- `src/data/config.py` and `tests/test_determinism.py` now have authority backing: ADR-10's four-part §12/§13.2 amendment was approved 2026-08-22 by the project owner under the recorded student/supervisor authority equivalence and applied to TE §12 under `CR-2026-08-22-TE-AMEND` (TE v3.4). **Authority to name a module is not authority to write one** — neither module exists, and `code-generation` must not create either before G-09.
- ADR-10's third row moved REQ-ENG-4's test-module count 18 → 19, and that move was **applied 2026-08-22**: REQ-ENG-4 now reads 19, re-derived from the amended TE §12 tree by enumerating its `test_*.py` entries rather than carried from prose. The advisory finding on `decisions.md` named only REQ-ENG-4 and the external TE §12 tree as genuine loci of that count; **that claim was inherited without independent verification and is corrected here — there are three.** The third is `requirements.md` § Intent analysis, which read "the remaining fifteen of REQ-ENG-4's eighteen test modules" and was wrong twice against the amended tree (the total is 19, and with three modules existing the remainder is 16); it was corrected 2026-08-22 under `GOV-2026-08-22-UG-02` Rec 3. Separately, `team-practices.md` § Testing Posture states a deliberately different figure (17 §12-tree modules), is now stale on it, and **must still not be edited here** — `org.md` reserves that file for the practices-affirmation gate, and the correction is tracked as **RES-02**.
- `ensure_process_determinism` must be the first statement of every stage script's `main()`, before any framework import — a re-exec after TensorFlow loads is pointless (FU-1 = D).
- No machine path may enter the four governed configs, so moving a directory never changes a governed hash (ADR-07).
- Two-tier error posture: integrity violations exit non-zero naming the file and the violated expectation; completeness shortfalls are recorded as machine-readable manifest fields.

---

## 2. `governance-guards` — Governance Guards — phase boundary, locked-test access, reuse register

**Kind** `library` · **Complexity** M · **Deployment** shared · **Depends on** `foundation`

**Responsibility.** The runtime prohibitions that must hold before any scientific work runs, and the transition contract that closes Phase 1: the phase-boundary import limb and produced-field limb, the transition manifest over the **canonical protected set derived from the union of TE §2.2 and TE §7.0B**, whose **final enumeration and cardinality are deferred to stage 3.1** (`functional-design`) — this artifact states neither, and **BLK-06** carries the obligation — the single chokepoint for every read under the restricted December root with its access-log-before-read ordering, and the §10.1 external-code reuse register.

**Owns.**

- `src/data/phase_contract.py` — `assert_phase_boundary`, `assert_no_raw_fields`, and the `phase_transition_manifest` artifact TE §2.2 names (built by `build_transition_manifest(...) -> TransitionManifest`, whose `protected_hashes` field carries the keys; `diff_protected_hashes` compares them — `component-methods.md` defines no function called `phase_transition_manifest`, and the design surface is named here so stage 3.1 searches for the right symbol) over the canonical protected set derived from TE §2.2 ∪ TE §7.0B; **final enumeration and cardinality deferred to stage 3.1** — this artifact states neither — **BLK-06**
- `src/data/locked_test.py` — **NEW**: `open_restricted`, the access-log row written **before** the read
- `src/data/reuse_registry.py` — the §10.1 register, all fifteen fields, recorded before the code is used
- `tests/test_phase_boundary.py`, `tests/test_reuse_registry.py`

**Boundary.** Called at every stage entry (step 4 of the stage entry contract) and at every restricted read. Imports `foundation` for the config snapshot the manifest hashes; imports nothing downstream, which is what keeps it a root. Its acceptance evidence, unlike its implementation, completes only after later units exist — recorded on the supporting-unit column rather than as a DAG edge, because the reverse edge would close a cycle.

**Requirements carried (10).** REQ-ENG-5, **FR-P1-02-6**, FR-P1-03-2, FR-P1-05-12, FR-P1-06-1, FR-P1-06-2, FR-P1-06-3, FR-P1-06-4, NFR-PHASE-01, NFR-LIC-01

Bold = no §16/§19 test row (1 of 10 here).

**Acceptance rows (2).** TA-27, TA-28

**Blockers.** **BLK-06** — owned scope blocked: `src/data/phase_contract.py`'s `TransitionManifest.protected_hashes` (built by `build_transition_manifest`; the `phase_transition_manifest` artifact of TE §2.2) and `diff_protected_hashes`, whose protected-key list has no stated derivation from TE §7.0B. Status: Open. **BLK-01 closed 2026-08-22** (`CR-2026-08-22-TE-AMEND`): `src/data/locked_test.py` is now named in TE §12 — **authority only**, the module does not exist and creating it stays gated by G-09 and stage 3.5. Its downstream consumers through the `open_restricted` contract are `inventory-and-registry` (pre-G-05 coverage audit), `acquisition` (the D-9 input and any December re-acquisition — **BLK-07**), `features-and-splits` (locked partition) and `evaluation-and-comparison` (locked evaluation). `reuse_registry.py` and the `assert_phase_boundary` / `assert_no_raw_fields` limbs carry no blocker.

**Implementation notes and constraints.**

- `src/data/locked_test.py` gained its authority backing on 2026-08-22 with the rest of ADR-10's amendment (TE §12, `CR-2026-08-22-TE-AMEND`). It remains unwritten and gated by G-09.
- `open_restricted` is the **only** path into `evidence/locked_test_restricted/`. `component-dependency.md` § Shared resources states the rule without qualification — "nothing else may construct a path into it" — and **BLK-07** carries the one unit whose routing through it was not recorded.
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

**Boundary.** The producer of every raw input the pipeline consumes. Hands downstream units resolved artifact paths and release IDs, never provider clients or credentials. Credentials reach the provider client directly from the environment via `foundation`'s resolution — never through a config file, log, registry note or notebook. It may construct a path into `evidence/` but **never directly into `evidence/locked_test_restricted/`**: every read or write under that root goes through `governance-guards.open_restricted`, which writes the access-log row before the read. That routing contract is **BLK-07** and is not yet authored.

**Requirements carried (15).** REQ-ENG-13, FR-P1-00-1, FR-P1-00-2, FR-P1-01-1, FR-P1-01-2, FR-P1-01-3, FR-P1-01-4, **FR-P1-01-5**, FR-P1-01-6, **FR-P1-01-7**, **FR-P1-01-8**, **FR-P1-01-9**, **FR-P1-01-11**, **REQ-NFR-A1**, **REQ-NFR-A2**

Bold = no §16/§19 test row (7 of 15 here).

**Acceptance rows (1).** TA-32

**Blockers.** **BLK-07** — owned scope blocked: every read or write this unit performs under `evidence/locked_test_restricted/`, including the `audit_evidence_2022-FULL/` artifact D-9 promotes as Phase 1's acquisition input and any re-acquisition touching calendar 2022-12. Required resolution: a governed contract routing all such access through `governance-guards.open_restricted`, so the `locked_test_accessed = true` row is written **before** the first December record is read. Approval authority: `functional-design` (3.1) for the contract. Status: Open — an **exit** condition on stage 3.1, and **no acquisition run may touch calendar 2022-12** while it stands. This unit's provider-retrieval, provenance, manifest-hashing and NaN-at-acquisition scope is unblocked.

**Implementation notes and constraints.**

- The `evidence/locked_test_restricted/audit_evidence_2022-FULL/` artifact D-9 promotes as Phase 1's acquisition input rests on twelve monthly runs whose provenance is unverifiable in principle: no provider byte stream exists in the workspace, and three of the twelve months (2022-04, 2022-07, and 2022-12, the locked month) have no `raw_isprint_cache/` at all. Every artifact produced before the re-acquisition carries that caveat, and FULL must not be relied on at a freeze gate while its provenance chain points at superseded per-month hashes.
- **Reading that D-9 input is a logged December access.** D-15 relocated FULL under `evidence/locked_test_restricted/` on 2026-08-21 and states the consequence directly: FULL carries 21,258 December rows, so *"any consumer that opens it must write an access-log row first."* D-15 is equally explicit that the restricted root is *"a governance boundary, not an access control"* — no permission, no ACL, no encryption — so the boundary holds only while exactly one code path reaches it. **BLK-07** carries the routing obligation, and **RES-01** records that permitted-read access logging is **NOT TESTED**, so nothing downstream would catch an omission.
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
- the D-17 target-schema test — **unnamed, and deliberately so: see BLK-05.** FR-P1-03-5's criterion implies a test that exists in none of the **19** modules TE §12's amended tree enumerates (`CR-2026-08-22-TE-AMEND`, TE v3.4 — the count re-derived from that tree by listing its `test_*.py` entries, not carried from prose; `test_acquisition_window.py` and `tests/test_determinism.py` are both inside it, the first as an already-approved 2026-08-16 countersignature applied late, the second as a newly approved ADR-10 entry). Naming it is a §12 tree amendment and therefore supervisor-owned; this stage records the obligation and chooses no name.

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

**Boundary.** The allowlist is stated at **module-path** granularity, exactly as TE §12's import-boundary rule states it: IRI/GIM imports are permitted only in `scripts/04_build_external_products.py` and modules under `src/evaluation/`, subject to all applicable evaluation-stage, frozen-mask and locked-test restrictions. Modules under `src/evaluation/` are owned by **three** distinct units — `evaluation-and-comparison` (`masks.py`, `metrics.py`), `statistical-inference` (`bootstrap.py`) and `regimes-diagnostics-reporting` (`regimes.py`, `diagnostics.py`, `plots.py`) — so the allowlist grants an authorized *path*, never a whole unit's unrelated code. An import from `src/data`, `src/features`, `src/models`, `src/gnss`, a training script or a notebook violates it identically. `spaceweather.py` is deliberately outside that restriction: drivers are model inputs subject to the availability lags.

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

**Blockers.** **BLK-04** — owned scope blocked: `src/features/transforms.py`'s `fit_transforms` / `apply_transforms` pair, and every assertion of NFR-LEAK-01 that runs through it. Downstream units affected: `models-and-baselines`, `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting` — every reported number inherits the fit. Required resolution: a governed cross-unit contract enforcing train-only fitting per fold, defining input and output types, alignment requirements, ownership of the fitted state, allowed partitions (the named fold's training partition only) and failure conditions (`LeakageError` when `train`'s index is not a subset of that partition), so validation and locked-test leakage are prevented by the contract rather than by review. Approval authority: `functional-design` (3.1) for the contract; Supervisor for the leakage evidence at G-04 and G-05. Status: Open. **Exit condition on stage 3.1, not an entry condition — ruled 2026-08-22 by the project decision owner (`GOV-2026-08-22-REM-01` Rec 2).** `features-and-splits` and the downstream units above **may enter** `functional-design` (3.1); that is where the contract is authored. **No affected unit may complete or exit 3.1 without its approved contract**, and **no implementation may proceed** while this blocker stands. The leakage safeguard is unchanged and is not weakened: per-fold train-only fitting on the named fold's training partition only, with a `LeakageError` when `train`'s index is not a subset of that partition, and NFR-LEAK-01's evidence still owed to the Supervisor at G-04 and G-05.

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

**Blockers.** **BLK-03** — owned scope blocked: `src/models/train.py`'s confirmatory-prediction path, this being the unit that owns confirmatory-prediction construction. Downstream units consuming that prediction: `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`. Required resolution: a governed cross-unit contract defining input and output types, alignment requirements, ownership of the frozen seed set, allowed partitions and failure conditions, with the frozen set arriving as a parameter from `ConfigSnapshot.seeds` — never inlined in `src/models`, never weakened to a distinctness check. Approval authority: `functional-design` (3.1) for the contract. The seed values themselves: **closed 2026-08-22** — D-122's supervisor sign-off was closed by the project owner under the recorded student/supervisor authority equivalence (Vision §14.2; `CR-2026-08-22-TE-AMEND`), with the values verified unchanged before closure: development seed 42 and final seeds {1337, 2024, 7}. The bootstrap seed **20221201** is frozen separately by TE §13.6 / TC-19 (Q-27) and is **not** part of D-122’s item set — attribution corrected 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 11. **That closes authority, not implementation** — the values reach `three_seed_mean` as a parameter from `ConfigSnapshot.seeds` via `configs/seeds.yaml` and **must never be inlined in `src/models` or any other implementation file** (TC-03e; the forbidden pattern this blocker names). **BLK-04 ↓** inherited from `features-and-splits`. Status: Open. **Exit condition on stage 3.1, not an entry condition — ruled 2026-08-22 by the project decision owner (`GOV-2026-08-22-REM-01` Rec 2).** `models-and-baselines` and the downstream units above **may enter** `functional-design` (3.1); that is where the contract is authored. **No affected unit may complete or exit 3.1 without its approved contract**, and **no implementation may proceed** while this blocker stands. The confirmatory-seed safeguard is unchanged and is not weakened: the frozen set reaches `three_seed_mean` as a parameter from `ConfigSnapshot.seeds`, never inlined in `src/models`, and never weakened to a pairwise-distinctness check.

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

**Boundary.** Owns two of the modules the IRI/GIM allowlist authorizes — `src/evaluation/masks.py` and `src/evaluation/metrics.py` — and imports `src/external/iri.py` and `src/external/gim.py` at evaluation time against the already-frozen mask. The allowlist is a module-path grant covering `scripts/04_build_external_products.py` and every module under `src/evaluation/` (TE §12), so it also reaches `statistical-inference`'s `bootstrap.py` and `regimes-diagnostics-reporting`'s `regimes.py`, `diagnostics.py` and `plots.py`; this unit is **not** the sole permitted importer, and no unit-level narrowing of TE §12 is asserted here. Imports `models-and-baselines` outputs; nothing imports it except the two units whose logic runs inside its script.

**Requirements carried (4).** FR-P1-04-7, **FR-P1-05-7**, **FR-P1-05-17**, NFR-FAIR-01

Bold = no §16/§19 test row (2 of 4 here).

**Acceptance rows (1).** WS-16

**Blockers.** **BLK-03 ↓** — this unit consumes the confirmatory prediction, so its masks and paired loss differential inherit whatever `three_seed_mean`'s contract turns out to permit. **BLK-04 ↓** — every metric it computes inherits the transform fit. Neither is owned here. Approval authority: as recorded on BLK-03 and BLK-04. Status: Open (inherited). **Both are exit conditions on stage 3.1, not entry conditions — ruled 2026-08-22 (`GOV-2026-08-22-REM-01` Rec 2).** This unit **may enter** `functional-design` (3.1); it **may not complete or exit** 3.1 while either contract is unapproved, and **no implementation may proceed** while they stand.

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

**Blockers.** **BLK-03 ↓**, **BLK-04 ↓** — the bootstrapped differential is computed from the confirmatory prediction over transform-fitted features, so both inherited contracts bound what this unit's intervals mean. Neither is owned here. Approval authority: as recorded on BLK-03 and BLK-04. Status: Open (inherited). **Both are exit conditions on stage 3.1, not entry conditions — ruled 2026-08-22 (`GOV-2026-08-22-REM-01` Rec 2).** This unit **may enter** `functional-design` (3.1); it **may not complete or exit** 3.1 while either contract is unapproved, and **no implementation may proceed** while they stand.

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

**Blockers.** **BLK-03 ↓**, **BLK-04 ↓** — every reported number, breakdown, figure and claim in this unit derives from the confirmatory prediction and the transform-fitted features, so both inherited contracts bound what may be claimed. Neither is owned here. Approval authority: as recorded on BLK-03 and BLK-04. Status: Open (inherited). **Both are exit conditions on stage 3.1, not entry conditions — ruled 2026-08-22 (`GOV-2026-08-22-REM-01` Rec 2).** This unit **may enter** `functional-design` (3.1); it **may not complete or exit** 3.1 while either contract is unapproved, and **no implementation may proceed** while they stand.

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

**Blockers.** **BLK-02** — owned scope blocked: `tests/fixtures/plumbing_7day/fixture_manifest.yaml` and every capability depending on it. The unit exists in the DAG with its nine dependencies recorded, but the manifest-dependent capability is blocked by `requirements.md` § Known defects row 12 — **on its station-selection limb only**. That row's reading limb was settled by the D-11 clarification of 2026-08-22 and the row was amended in place to record it. **The station was subsequently selected and frozen on 2026-08-22 as BSHM 32/35 (D-20)**, on the only complete observed coverage of the window (168/168 hourly bins). **No manifest may be invented, inferred or substituted**, and this unit still cannot pass its completion gate until the authoritative manifest exists and is hash-verifiable — none exists, and the fixture has never been run. Approval authority: the project owner under Q-31. **BLK-01 closed 2026-08-22** — TE §13.2 now carries the `PYTHONHASHSEED=0` clean-run clause (`CR-2026-08-22-TE-AMEND`), so `test_clean_run.py`, WS-20 and TA-17 test the amended sequence rather than an unamended one. **BLK-03 ↓**, **BLK-04 ↓** — inherited: this unit's `depends_on` includes all four units carrying those blockers (`models-and-baselines`, `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`), and the clean-run tolerance comparison and TA-21's traceability matrix consume their released artifacts, so what those two contracts permit bounds what WS-20 and TA-17 can be said to have reproduced. Approval authority: as recorded on BLK-03 and BLK-04. Status: BLK-02 Open; BLK-03 ↓ and BLK-04 ↓ Open (inherited), both **exit conditions on stage 3.1**; BLK-01 **Closed 2026-08-22**.

**Implementation notes and constraints.**

- **Blocked — on the station selection, not on the reading.** `requirements.md` § Known defects row 12's reading limb is settled: the **D-11 clarification of 2026-08-22** records D-11's `Stations:` line as the **eligibility evidence** for the frozen window and retains TE §15.1's **one-station execution scope**, and row 12 was amended in place on 2026-08-22 to record it (`GOV-2026-08-22-UG-02` Rec 7). **The station was selected and frozen on 2026-08-22 as BSHM 32/35 (D-20)**, so the fixture can now state its identity. What remains open is the manifest itself: it does not exist, the fixture has never been run, and **no measured value may be invented, inferred or substituted.** ARUC's one-bin shortfall on five of the seven days is **dormant, not discharged** — it attaches to ARUC, which is not selected.
- The seven-day fixture is never scientific evidence — it may not be cited, plotted as a result, or interpreted as skill.
- D-11 froze the plumbing window as 2022-11-01 to 2022-11-07 inclusive, all three cells, with measured completeness ARUC 163/168, BSHM 168/168, NICO 155/168 and 7/7 day presence in every cell, carrying the limitation that it reproduces neither December's winter-solstice regime nor its activity distribution. The one-month all-station scientific window is **frozen as D-14 — March 2022, all three cells** (`CR-2026-08-21-FREEZES`), carrying its own mandatory limitation that March is an equinox month reproducing neither December's regime nor its activity distribution; it is no longer open under Q-31 (corrected 2026-08-22, finding `UG-08`).
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

Nothing in this register is resolved by this stage. Every row names the authority
that discharges it, and where a row has since been discharged the register records
the act, its date and its change record rather than deleting the row. **BLK-01 is
closed; BLK-02 through BLK-07 are open.** Seven blockers are registered, and **ten of
the twelve units carry a blocker row, owned or inherited** — `inventory-and-registry`
and `external-products` carry none of their own. That is the only sense in which "ten"
is meant: BLK-01's `config.py` row names *every* unit as downstream, so a reading that
counted downstream mentions would give twelve.

### BLK-01 — ADR-10's §12/§13.2 amendment (unsigned at registration; **closed 2026-08-22**)

Tracked per unit **and** per file, because approval arrives for the amendment as
a whole and a partially-built unit must not read as covered.

| Affected artifact | Owning unit | Downstream units | Status |
|---|---|---|---|
| `src/data/config.py` | `foundation` | every unit — the six-step stage entry contract calls `load_configs`, `assert_no_tbd` and `resolve_platform_roots` before any domain work | **Closed 2026-08-22** — in TE §12 under `CR-2026-08-22-TE-AMEND`. Authority only; the module does not exist and creation stays gated by G-09 and stage 3.5 |
| `tests/test_determinism.py` | `foundation` | `models-and-baselines` (TA-26's deterministic seed utility and serialization restore), `statistical-inference` | **Closed 2026-08-22** — in TE §12 under `CR-2026-08-22-TE-AMEND`. Authority only; the module does not exist and creation stays gated by G-09 and stage 3.5 |
| `src/data/locked_test.py` | `governance-guards` | `inventory-and-registry` (the pre-G-05 coverage audit), `features-and-splits` (the locked partition), `evaluation-and-comparison` (the locked evaluation) | **Closed 2026-08-22** — in TE §12 under `CR-2026-08-22-TE-AMEND`. Authority only; the module does not exist and creation stays gated by G-09 and stage 3.5 |
| TE §13.2's `PYTHONHASHSEED` clean-run clause | `fixtures-and-reproducibility` | none — terminal, but `test_clean_run.py`, WS-20 and TA-17 test the sequence **as written** | **Closed 2026-08-22** — `PYTHONHASHSEED=0` added to TE §13.2 under `CR-2026-08-22-TE-AMEND`; `test_clean_run.py`, WS-20 and TA-17 now test the amended sequence |

- **Required resolution.** ADR-10's four-part amendment recorded and countersigned as one change record, the way `test_acquisition_window.py`'s addition was countersigned on 2026-08-16. REQ-ENG-4's test-module count moves 18 → 19 in its two genuine loci (REQ-ENG-4 itself and the external TE §12 tree); `team-practices.md` § Testing Posture states a deliberately different figure and is not one of them.
- **Approval authority.** The authorized project decision owner — student, with supervisor countersignature. `project.md` § Forbidden bars an agent from filling a supervisor-owned value by convenience, and a tree amendment is that class of change.
- **Consequence while open.** `code-generation` must not create these three modules or the amended clean-run command on the strength of ADR-10 alone.

#### BLK-01 status: **CLOSED 2026-08-22**

Approved by the project owner under the recorded student/supervisor authority equivalence and applied under change record **`CR-2026-08-22-TE-AMEND`** (`governance/CHANGE_RECORD_2026-08-22_TE_amendment.md`), on governance report `GOV-2026-08-22-REM-01` Recommendations 1 and 4. Closure is claimed because every required amendment and the traceability update **have actually landed in the authoritative documents** — each verified in place:

| Required item | Landed | Where |
|---|---|---|
| `src/data/config.py` | ✅ | TE §12 tree, `src/data/` |
| `src/data/locked_test.py` | ✅ | TE §12 tree, `src/data/` |
| `tests/test_determinism.py` | ✅ | TE §12 tree, `tests/` |
| `PYTHONHASHSEED` clean-run clause | ✅ | TE §13.2, set before the first command, with its WS-20 / TA-17 / `test_clean_run.py` implication recorded |
| REQ-ENG-4 count 18 → 19 | ✅ | `requirements.md` REQ-ENG-4, **re-derived from the amended tree** by enumerating its `test_*.py` entries and counting them — not assumed |
| `requirements.md` § Intent analysis count | ✅ | **Added 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 3.** The sentence read "the remaining fifteen of REQ-ENG-4's eighteen test modules" and survived the first closure unpropagated — wrong twice against the amended tree. Corrected to sixteen of nineteen. **The original closure asserted "every" amendment had landed while this site had not, and that over-claim is recorded here rather than quietly dropped.** |
| TE §1.2 change-history row | ✅ | v3.4, 22 August 2026 |

A finding raised during closure and fixed in the same act: the **2026-08-16 countersigned** amendment adding `tests/test_acquisition_window.py` had **never been written into TE §12** (`REM-01`). It is now applied, and TE §12's provenance table keeps it distinct from the newly approved ADR-10 entries — an already-approved historical amendment applied late, not a new approval.

- **What closure does NOT authorize.** **Authority to name a module is not authority to write one.** None of the four modules exists. Creating them remains gated by **G-09** ("before any affected component is coded"), by TE §18.3's rule that an agent must stop and report rather than choose a default, and by stage **3.5 `code-generation`**. The workflow is at stage 2.8; nothing here advances it.
- **Related but separate, still open.** BLK-05's D-17 target-schema module is a **further** §12 tree amendment, not covered by this closure, and no module for it may be created until stage 3.1 names it and its own amendment is approved.

### BLK-02 — the `plumbing_7day` fixture manifest cannot state its identity

| Field | Value |
|---|---|
| Affected artifact | `tests/fixtures/plumbing_7day/fixture_manifest.yaml` |
| Owning unit | `fixtures-and-reproducibility` |
| Downstream units | none — the unit is terminal. The block reaches WS-20, TA-09 and TA-17, and through TE §9.2's intra-unit ordering contract it reaches every full-year job. |
| Required resolution | **Partly discharged 2026-08-22; the remainder is open.** The §15.1-versus-D-11 reading is now settled by the **D-11 clarification of 2026-08-22** (`evidence/DECISIONS.md`, approved by the project owner under the recorded authority equivalence, on `GOV-2026-08-22-REM-01` Rec 3 option C): D-11's `Stations:` line is the **eligibility evidence** for the frozen window, and TE §15.1's **one-station execution scope is retained**. `requirements.md` § Known defects row 12 was **amended in place on 2026-08-22** to record it (`GOV-2026-08-22-UG-02` Recommendation 7, option 2, approved by the project owner; the board had recommended tracking it as a residual instead, and the owner ruled for direct amendment). **Station selected and frozen 2026-08-22 — BSHM 32/35 (D-20).** What remains open: the authoritative manifest must exist and be hash-verifiable, and the fixture must actually run. Neither has happened. |
| Approval authority | The station identity: **the project owner under Q-31** (TE §18.2 assigns fixture station, dates and tolerances to the Student), exercised under the recorded student/supervisor authority equivalence. |
| Status | **Open on implementation; station-selection limb RESOLVED 2026-08-22.** See the limb table below. |

#### BLK-02 limb status, synchronized 2026-08-22

| Limb | Status | Evidence |
|---|---|---|
| §15.1-versus-D-11 reading | **Resolved** 2026-08-22 | D-11 clarification; §15.1's one-station execution scope retained |
| **Station selection** | **RESOLVED 2026-08-22 — BSHM 32/35** | **D-20**. Selected on the only complete observed coverage of D-11's window: **168/168 hourly bins**, 7/7 days present, 1,810 records, from `evidence/audit_evidence_2022-11/madrigal_coverage_raw_records.csv` |
| ARUC's one-bin shortfall on five of seven days | **DORMANT — conditional, and explicitly NOT resolved** | See the dormancy rule below |
| Fixture manifest implementation | **PENDING** | `tests/fixtures/plumbing_7day/fixture_manifest.yaml` does not exist |
| Fixture execution | **PENDING** | The fixture has never been run |
| Measured evidence (row counts, tolerances, support and missingness limits, timestamp tolerances, CPU runtime range) | **PENDING** | §15.1 requires these measured from a run and frozen. **No value exists and none is claimed.** Selecting a station supplies identity, not content |

**ARUC and NICO** remain the appropriate candidates for **separate** missing-data and
robustness tests, where their gaps are the subject rather than a confound in a plumbing
smoke test.

#### The ARUC dormancy rule, recorded 2026-08-22

D-11 observed that **ARUC 40/44 is short exactly one hourly bin on five of the seven days
of the frozen window (3–7 November 2022)** — 163/168 bins — and called the uniformity
suggestive of *"a systematic single-bin gap rather than random loss"*, requiring it to be
explained before the manifest is frozen.

**Status: DORMANT. It is NOT resolved, and must not be recorded as resolved.**

- **Why it is dormant:** BSHM was selected as the plumbing-fixture station (**D-20**), so
  the obligation — which attaches to ARUC — does not gate the current fixture.
- **Reactivation condition:** the obligation **revives in full** the moment ARUC is
  proposed for any fixture whose evidence depends on the affected coverage.
- **What reactivation requires:** an **evidence-backed explanation** of the systematic
  single-bin gap — not an acknowledgement, not an assumption, and not a tolerance widened
  to absorb it — recorded **before** that fixture's manifest is frozen.
- **What dormancy does not do:** it does not close the finding, does not discharge D-11's
  pre-freeze obligation, and does not license using ARUC's window coverage figures as
  though the gap were understood.

### BLK-03 — `three_seed_mean` cannot express the frozen-seed check

| Field | Value |
|---|---|
| Affected artifact | `src/models/train.py` — the `three_seed_mean(predictions)` signature in `component-methods.md` |
| Owning unit | `models-and-baselines` (confirmatory-prediction construction) |
| Downstream units | `evaluation-and-comparison` (masks and the paired loss differential consume the confirmatory prediction), `statistical-inference` (bootstraps that differential), `regimes-diagnostics-reporting` (reports it) |
| Required resolution | A governed cross-unit contract fixing input and output types, alignment requirements, ownership of the frozen seed set, allowed partitions, and failure conditions. The frozen set reaches the function as a parameter sourced from `ConfigSnapshot.seeds` — never inlined, since `{1337, 2024, 7}` in `src/models` is the forbidden pattern, and never weakened to a pairwise-distinctness check a wrong-but-distinct triple would pass. |
| Approval authority | The contract: `functional-design` (3.1) — **still open**. The seed values themselves: **closed 2026-08-22.** D-122's pending supervisor sign-off was closed by the project owner under the recorded student/supervisor authority equivalence (Vision §14.2; `CR-2026-08-22-TE-AMEND`), so the frozen set is authoritative: development seed 42 and final seeds {1337, 2024, 7}. The bootstrap seed **20221201** is frozen separately by TE §13.6 / TC-19 (Q-27) and is **not** part of D-122’s item set — attribution corrected 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 11. **This closes authority, not implementation** — the values are supplied to `three_seed_mean` from `ConfigSnapshot.seeds` via `configs/seeds.yaml` and **must never be inlined in `src/models` or any other implementation file** (TC-03e; the forbidden pattern this blocker names). |
| Status | Open. **Exit condition on stage 3.1, not an entry condition — ruled 2026-08-22 by the project decision owner (GOV-2026-08-22-REM-01 Rec 2).** `models-and-baselines` and the downstream units above **may enter** `functional-design` (3.1); that is where the contract is authored. **No affected unit may complete or exit 3.1 without its approved contract**, and **no implementation may proceed** while this blocker stands. The prior wording ("must be discharged before … enters functional design") was unsatisfiable, since 3.1 is named as the contract's own approval authority. The substantive protection is unchanged and is not weakened: the confirmatory-seed safeguard stands in full — the frozen set reaches `three_seed_mean` as a parameter from `ConfigSnapshot.seeds`, never inlined in `src/models`, and never weakened to a pairwise-distinctness check. |

### BLK-04 — `fit_transforms` leaves the full-dataset fit representable

| Field | Value |
|---|---|
| Affected artifact | `src/features/transforms.py` — the `fit_transforms(train, *, fold)` / `apply_transforms(...)` pair in `component-methods.md`, and ADR-01's claim about it |
| Owning unit | `features-and-splits` |
| Downstream units | `models-and-baselines` (trains on the transformed features), `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting` — every reported number inherits the fit |
| Required resolution | A governed cross-unit contract that enforces train-only fitting per fold: input and output types, alignment requirements, ownership of the fitted state, allowed partitions (the named fold's training partition only), and failure conditions — a `LeakageError` when `train`'s index is not a subset of that partition. The two-function split prevents the single-call convenience shape and nothing more; the contract is what closes the leak. |
| Approval authority | The contract: `functional-design` (3.1). The leakage evidence it produces: Supervisor, at G-04 and G-05 (NFR-LEAK-01). |
| Status | Open. **Exit condition on stage 3.1, not an entry condition — ruled 2026-08-22 by the project decision owner (GOV-2026-08-22-REM-01 Rec 2).** `features-and-splits` and the downstream units above **may enter** `functional-design` (3.1); that is where the contract is authored. **No affected unit may complete or exit 3.1 without its approved contract**, and **no implementation may proceed** while this blocker stands. The prior wording ("must be discharged before … enters functional design") was unsatisfiable, since 3.1 is named as the contract's own approval authority. The substantive protection is unchanged and is not weakened: the leakage safeguard stands in full — per-fold train-only fitting on the named fold's training partition only, with a `LeakageError` when `train`'s index is not a subset of that partition, and NFR-LEAK-01's evidence still owed to the Supervisor at G-04 and G-05. |

### BLK-05 — the D-17 target-schema test has no module and no §12 entry

| Field | Value |
|---|---|
| Affected artifact | the D-17 target-schema test implied by FR-P1-03-5's criterion — present in no mandated test-module set |
| Owning unit | `target-standardization` |
| Downstream units | `features-and-splits` (consumes the target rows the test would validate) |
| Required resolution | `functional-design` (3.1) names the module. Because TE §12 fixes the tree to file level, adding it is a further tree amendment whose count impact is tracked the way ADR-10's 18 → 19 is tracked. |
| Approval authority | Project decision owner under the recorded student/supervisor authority equivalence — a §12 tree amendment |
| Status | **Open on implementation; naming and documentation limbs RESOLVED 2026-08-22.** See the limb table below. |

#### BLK-05 limb status, synchronized 2026-08-22

**Approving a filename does not resolve the blocker.** Two limbs are complete, two are not.

| Limb | Status | Evidence |
|---|---|---|
| **Module naming** | **RESOLVED 2026-08-22** — `tests/test_prepared_target_schema.py` | Approved by the project decision owner; change record `CR-2026-08-22-TARGET-SCHEMA-TEST` |
| **Documentation** — §12 tree entry and downstream artifact updates | **RESOLVED 2026-08-22** | Added to the TE §12 `tests/` tree with its responsibility comment, and to the §12 amendment-provenance table. The tree now enumerates **20** test modules |
| **Test implementation** | **PENDING** | The module does not exist. Creation stays gated by **G-09** and stage 3.5 |
| **Execution evidence** | **PENDING** | The test has never been run. **No result of any kind is claimed** |

**Approved acceptance behaviour**, fixed by the owner and recorded so implementation
cannot narrow it: a valid row containing exactly D-17's approved 16 fields **passes**; a
row containing an excluded or additional field **fails**; a row missing any required field
**fails**.

### BLK-06 — the canonical protected set is not established; enumeration and cardinality deferred to stage 3.1

| Field | Value |
|---|---|
| Affected artifact | `src/data/phase_contract.py` — the `protected_hashes` key list on `TransitionManifest`, built by `build_transition_manifest` (this is the `phase_transition_manifest` **artifact** TE §2.2 names; `component-methods.md` defines no function of that name, and the design surface is given here so stage 3.1 searches the right symbol), and `diff_protected_hashes`' pass condition |
| Owning unit | `governance-guards` |
| Downstream units | none by import. The block reaches **G-P2** and **G-P3C**, whose pass condition is an empty protected-hash diff, and `fixtures-and-reproducibility` as the supporting unit on TA-27's hash-diff evidence. |
| What this stage states | **Nothing about the enumeration or its size.** Every artifact in this stage, and the 2.6 design artifacts it consumes, now refer only to "the canonical protected set derived from the union of TE §2.2 and TE §7.0B". **The final enumeration and cardinality are deferred to stage 3.1** by direction of the authorized project decision owner, 2026-08-22. **No cardinality for the canonical set is stated, invented or carried.** Source-document item counts appearing in the rows below (§2.2's twelve, §7.0B's sixteen, FR-P1-06-1's fourteen) are quoted as facts about those documents, never as the canonical size — scoped 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 5, the earlier wording having read as an unqualified "no number" that the next rows appeared to contradict. |
| Current approved candidate, recorded not adopted | `requirements.md` **FR-P1-06-1** carries a fourteen-item candidate list — model source; TensorFlow/Keras environment; architecture serialization; feature manifest; target contract; split/mask manifests; grids; selected hyperparameters; optimizer/loss policy; seeds; metrics; statistical configuration; bootstrap; reporting hierarchy — origin `IMPL-1` (`GOV-2026-08-20-RA-01`). It is named here as the starting point 3.1 must validate, **not** as the canonical set. FR-P1-06-1 is an approved requirement and is **not** edited by this stage. |
| Why it is a candidate rather than the canonical set | FR-P1-06-1 states the set as "the union of TE §2.2 and §7.0B" but records no deduplication or subsumption rule, and §7.0B names immutables its list does not visibly carry. Derived against the authority: TE §2.2's `phase_transition_manifest` sentence lists **12** items; TE §7.0B's post-Phase-1 immutables sentence lists **16**; (both cited by anchor text rather than line number — the line numbers this row carried, 121 and 333, pointed at §2.2's *Exit evidence* row and the §7.0A heading respectively after v3.4's line shifts, and were corrected 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 4) FR-P1-06-1's list is §2.2's twelve plus `bootstrap` and `reporting hierarchy`. **`history window`**, **`station encoding`** and **`baselines`** appear in §7.0B and in none of its items. `history window` and `station encoding` are plausibly inside `feature manifest`, and `embargo` inside `split/mask manifests`, but no artifact says so; **`baselines` has no plausible home in that list at all.** |
| Consequence while open | `diff_protected_hashes` can return the empty mapping that *is* G-P3C's pass condition while a Phase 2 confirmatory run has changed a baseline definition (M-01 persistence, M-02 seasonal persistence, M-03 climatology), a history window or a station encoding. That is protected-protocol drift passing undetected at a full-board gate. |
| Required resolution — stage 3.1 (`functional-design`), before it designs `phase_contract.py` | (a) **Extract** every protected item from TE §2.2 and TE §7.0B. (b) **Define and document the deduplication rule**, including every subsumption it relies on. (c) **Produce the canonical item-by-item protected enumeration.** (d) **Calculate the actual cardinality from that enumeration** — derived and printed, never carried from prose, a finding's text or an earlier revision. (e) Ensure **`protected_hashes.keys()` exactly matches the canonical protected set**. (f) **Fail validation if any protected item is missing, extra, renamed or changed.** (g) **Require approval of the canonical enumeration before the phase-transition gate (G-P2, and G-P3C's "protected hashes unchanged" condition) can pass.** |
| Recorded tension — status **amendment conditionally required** | FR-P1-06-1's acceptance criterion asserts the hash-diff test's key list "equal to the fourteen-item enumeration". If 3.1's canonical enumeration differs from that list in content or cardinality, FR-P1-06-1 must be amended through **Vision §15.2** change control before the difference is treated as official. This stage adopts no reading on which is right, **does not silently reinterpret or rewrite FR-P1-06-1**, and amends neither the requirement nor the Technical Environment. |
| Precedence, where the two disagree | **The canonical authority-derived content takes precedence over preserving an unsupported count.** The derived set must **not** be forced to equal fourteen merely to keep FR-P1-06-1 intact, and no replacement cardinality may be assumed or hard-coded before the derivation is performed. Precedence settles what the manifest must hash; it does **not** waive the reconciliation — FR-P1-06-1 must still be formally amended under §15.2 before the phase-transition gate can pass. |
| What this blocker does and does not block | It does **not** block stage 3.1 from performing the derivation — that is the work 3.1 is obliged to do. It **does** block (a) implementing `TransitionManifest.protected_hashes`' key list to any fixed size before the derivation exists, and (b) final acceptance at **G-P2** and **G-P3C** until the canonical set either matches FR-P1-06-1 or FR-P1-06-1 is amended under §15.2. Tracked as **RES-03** in § Residual governance obligations. |
| Approval authority | The canonical enumeration: the authorized project decision owner, under the recorded student/supervisor authority equivalence. Any change to FR-P1-06-1's item set or to TE §2.2/§7.0B: Vision §15.2 change control, as with every other governed-artifact amendment in this project. No governing document makes a separate supervisor signature mandatory for either step beyond that equivalence. |
| Status | **Open. Enumeration-method and enumeration limbs RESOLVED 2026-08-22; implementation limb open.** See the limb table below. Registered 2026-08-22 per governance finding `UG-01` (`GOV-2026-08-21-UG-01`). |

#### BLK-06 limb status, synchronized 2026-08-22

**BLK-06 is NOT fully closed.** Four limbs are resolved and two are not.

| Limb | Status | Evidence |
|---|---|---|
| **Canonical enumeration approach** — deduplicated union of the authoritative lists | **RESOLVED 2026-08-22** | **D-24**. Deduplication rule stated explicitly; §2.2 (12 items) and §7.0B (16 items) both enumerated by hand from the authority |
| **Required additions** — `history window`, `station encoding`, `baselines` | **RESOLVED 2026-08-22** | D-24. Each mapped onto no item of the previous fourteen; `baselines` had no plausible home at all, which is why a Phase 2 baseline change could otherwise pass G-P3C's empty-diff condition |
| **Final canonical list and actual cardinality** | **RESOLVED 2026-08-22 — 17 items** | D-24's enumeration. **Cardinality calculated from that enumeration** (14 carried forward + 3 added), not assumed |
| **FR-P1-06-1 amendment** | **APPLIED 2026-08-22** | Vision §15.2, change record `CR-2026-08-22-PROTECTED-SET`. Amended 14 → 17; prior text preserved in an inline audit comment |
| **Precise protected artifacts — per-item binding to concrete config fields and file paths** | **PENDING** | D-24 names each item's governing artifact and intended hashable representation. **None of the four config files or six `src/` packages exists**, so no field path is claimed to exist today. Binding completes at functional design |
| **Implementation evidence** | **PENDING** | `TransitionManifest.protected_hashes` and `diff_protected_hashes` do not exist. Not implemented, not executed, not passing. Creation stays gated by **G-09** and stage 3.5 |

**Baselines — what item 17 protects**, enumerated as D-24 requires: M-01 persistence,
M-02 24-hour seasonal persistence, M-03 station×month×hour climatology, **B-01 the
IRI-2016 benchmark with its frozen generation configuration including the 2000 km
ceiling**, and C-01 the CODE final GIM comparator with its frozen product identity and
interpolation rule.

### BLK-07 — `acquisition`'s access under the restricted December root is not routed through the chokepoint

| Field | Value |
|---|---|
| Affected artifact | `scripts/00_acquire_prepared_vtec.py` and `notebooks/00_acquire_phase1_vtec.ipynb` — every read or write under `evidence/locked_test_restricted/`, including the `audit_evidence_2022-FULL/` artifact D-9 promotes as Phase 1's acquisition input, and any re-acquisition touching calendar 2022-12 |
| Owning unit | `acquisition` |
| Downstream units | none by import. The block reaches **G-P1A**, **G-05** and **G-06** through the access record every December read owes, and `inventory-and-registry`, whose G-P1A coverage audit consumes this unit's released artifacts |
| Required resolution | A governed contract routing **every** `acquisition` read or write under `evidence/locked_test_restricted/` through `governance-guards.open_restricted`, so the access-log row carrying `locked_test_accessed = true` is written **before** the first December record is read. `acquisition` constructs no path into the restricted root directly. |
| Why it exists | Stage 2.6 fixes the rule without qualification (`component-dependency.md` § Shared resources): `evidence/locked_test_restricted/` is owned by `data.locked_test` and **"nothing else may construct a path into it"**, serialised through one chokepoint. This artifact previously granted `foundation` and `acquisition` unqualified path construction into `evidence/` with no carve-out for the restricted subtree, and omitted `acquisition` from the `open_restricted` consumer list — while naming FULL, which sits under that root, as acquisition's D-9 input. **D-15** states the consequence directly: *"Reading the D-9 input is now a logged December access. FULL contains 21,258 December rows, so any consumer that opens it must write an access-log row first."* |
| What makes it consequential | D-15 records that the restricted root is **"a governance boundary, not an access control"** — no filesystem permission, no ACL, no encryption. The boundary holds only while exactly one code path reaches it; a second sanctioned path is not a weaker boundary, it is none. **RES-01** separately records that permitted-read access logging is **NOT TESTED**, so no downstream check would catch the omission. |
| Consequence while open | An implemented `acquisition` could open the D-9 input, or write re-acquired December bytes, with no access-log row — a December access with no record, in breach of Vision §8.3, D-15 and FR-P1-02-3, discoverable only after the fact and not retrospectively curable except as a retrospective entry, as D-15's own rows 3, 4 and 5 already are. |
| Approval authority | The contract: `functional-design` (3.1). The artifact statements applied 2026-08-22: the authorized project decision owner. |
| Status | **Open. Exit condition on stage 3.1, on the BLK-03 / BLK-04 pattern.** `acquisition` **may enter** `functional-design` (3.1); it **may not complete or exit** 3.1 without the approved routing contract, and **no acquisition run may touch calendar 2022-12** while this blocker stands. Registered 2026-08-22 per governance finding `UG2-01` (`GOV-2026-08-22-UG-02` Recommendation 1, option 2, approved by the project owner). **No December record was opened in raising or applying it.** |

### Roll-up by unit

| Unit | Blockers | Blocked scope |
|---|---|---|
| `foundation` | — | None open. **BLK-01 closed 2026-08-22**: `src/data/config.py` and `tests/test_determinism.py` are authorized by name only, remain unwritten, and stay gated by G-09 and stage 3.5. |
| `governance-guards` | BLK-06 (implementation limb) | `phase_contract.py`'s `TransitionManifest.protected_hashes` (built by `build_transition_manifest`) and `diff_protected_hashes` (BLK-06) — its `assert_phase_boundary` / `assert_no_raw_fields` limbs and `reuse_registry.py` are unblocked. **BLK-01 closed 2026-08-22**: `src/data/locked_test.py` is authorized by name only and remains unwritten. |
| `acquisition` | BLK-07 | every read or write under `evidence/locked_test_restricted/` — the `open_restricted` routing contract. Its provider-retrieval, provenance, manifest-hashing and NaN-at-acquisition scope is unblocked. |
| `target-standardization` | BLK-05 (implementation limb) | the D-17 schema test only. Module named `tests/test_prepared_target_schema.py` and documented 2026-08-22; **not implemented, not executed**. |
| `features-and-splits` | BLK-04 | `transforms.py` and everything asserting NFR-LEAK-01 through it. |
| `models-and-baselines` | BLK-03, BLK-04 ↓ | `train.py`'s confirmatory-prediction path (BLK-03); the training it performs on transform-fitted features (BLK-04, inherited). |
| `evaluation-and-comparison` | BLK-03 ↓, BLK-04 ↓ | anything consuming the confirmatory prediction (BLK-03); every metric computed over transform-fitted features (BLK-04). Both inherited. |
| `statistical-inference` | BLK-03 ↓, BLK-04 ↓ | the bootstrapped differential. Both inherited. |
| `regimes-diagnostics-reporting` | BLK-03 ↓, BLK-04 ↓ | every reported number derived from the above. Both inherited. |
| `fixtures-and-reproducibility` | BLK-02 (implementation limb), BLK-03 ↓, BLK-04 ↓ | the `plumbing_7day` manifest — hence its completion gate. **Station resolved 2026-08-22 as BSHM (D-20); manifest, execution and measured evidence still pending.** Inherited: the clean-run tolerance comparison and TA-21's traceability matrix consume artifacts from all four units carrying BLK-03 and BLK-04, so what those contracts permit bounds what a clean run can be said to reproduce. **BLK-01 closed 2026-08-22**: TE §13.2 now carries the `PYTHONHASHSEED=0` clause, so the clean-run contract is no longer blocked on its absence. |
| `inventory-and-registry`, `external-products` | — | none of their own; both call `foundation`'s now-authorized stage entry contract, and `inventory-and-registry`'s December coverage audit is already routed through `open_restricted`. |

Roll-up notation matches the `Blockers` column in § Unit definitions and each
unit's `**Blockers.**` line: an unmarked ID is owned here, **↓** is inherited
through a consumed contract.

Per Q7, no unit above may be described as independent-and-ready while a blocker
naming it stands, and independence in `unit-of-work-dependency.md` § Independent
unit sets is a statement about the graph, never about readiness.

## Residual governance obligations — carried to stages 3.1 and 3.2

**Four** obligations are **not** discharged by this stage's remediation — three from
`GOV-2026-08-21-UG-01` and **RES-04**, added 2026-08-22 from `GOV-2026-08-22-DP-01`. The
original three from `GOV-2026-08-21-UG-01` are **not** discharged by this
stage's remediation. Each is recorded here with a truthful status, an owner and
the closure evidence that would actually discharge it. **None is closed,
verified, resolved or fully tested**, and none may be described in those terms
until the closure evidence in its row exists. This section is a handoff record:
stage 2.8 (`delivery-planning`) carries it into Construction, and stages 3.1
(`functional-design`) and 3.2 (`nfr-requirements`) are its named consumers.

| ID | Obligation | Status | Owner | Due stage / gate | Closure evidence required |
|---|---|---|---|---|---|
| **RES-01** (UG-03 option C) | No dedicated acceptance criterion verifies that a **permitted** December read — including the required pre-G-05 coverage and regime audit — writes its access-log row **before** the first December record is read | **Ownership remediated; dedicated test coverage open.** This scenario is explicitly **NOT TESTED** | `inventory-and-registry` performs the read; the criterion is authored by stage **3.2** (`nfr-requirements`) | Candidate §19 TA row routed through **Vision §15.2** change control and the 3.2 / G-05 freeze-manifest workflow; due before **G-05** | An approved §19 TA row that (a) distinguishes permitted coverage-audit access from prohibited pre-G-05 performance execution, and (b) asserts `locked_test_accessed = true` is recorded **before** the first December record is read; plus a passing test result against it |
| **RES-02** (UG-06) | `team-practices.md` § Testing Posture is stale on two separate figures: it defines the Phase 1 acceptance set as **WS-09 through WS-20**, omitting FR-WS-4's WS-01 exception; and it states **17** §12-tree test modules, where the amended TE §12 tree and REQ-ENG-4 now both read **19** | **Deferred to authorized gate** | Practices-affirmation gate owner | Next authorized **practices-affirmation gate** | The affirmed-practices text amended at that gate to match FR-WS-4's 13-row set **and** the 19-module count re-derived from the amended TE §12 tree |
| **RES-04** (GOV-2026-08-22-DP-01) | No captured report exists for the 2026-08-21 run of the three existing test modules, all of which reach the restricted December root by recursive traversal | **Open — not started.** Deliberately not attempted; running them before `open_restricted` exists would manufacture the breach | `governance-guards` (mechanism); execution at build-and-test (3.6) and the Bolt 12 in-Kaggle run | Prerequisite: `open_restricted` exists and enforces. Due before **G-05** | A captured rerun report, with the access-log entry written **before** the read, fail-closed on logging failure, real date and time recorded, and linked to the historical gap without rewriting it. Preferred route: unrestricted months and synthetic fixtures, which cover most of the intended behaviour |
| **RES-03** (UG-01) | FR-P1-06-1 required `protected_hashes.keys()` to equal a "fourteen-item enumeration" while the canonical protected set had not been derived from TE §2.2 and TE §7.0B | **Derivation and amendment COMPLETE 2026-08-22; implementation binding PENDING** | Derived and frozen as **D-24** (17 items, cardinality calculated); FR-P1-06-1 amended 14 → 17 under `CR-2026-08-22-PROTECTED-SET`; per-item binding and implementation owned by stage **3.1** and gated by G-09 | Binding before `phase_contract.py` is designed; implementation evidence before **G-P2** and G-P3C |  Closed limbs: the item-by-item enumeration with its explicit deduplication rule, the calculated cardinality, and the §15.2 amendment — all recorded in D-24 and the change record. Open limbs: per-item binding to concrete config fields (no config file exists) and the implementation of `protected_hashes` / `diff_protected_hashes` (not written, not executed) |

### RES-04 — documented rerun of the three existing test modules under `open_restricted`

Registered 2026-08-22 by project-owner decision, against the evidence gap recorded in
`evidence/experiment_registry.md`.

| Field | Value |
|---|---|
| **Obligation** | A **new, independently documented rerun** of `tests/test_acquisition_window.py`, `tests/test_phase_boundary.py` and `tests/test_release_hashes.py`, producing a captured report as new evidence |
| **Why it exists** | The 2026-08-21 run left **no run log, no captured output and no evidence record**. All three modules reach `evidence/locked_test_restricted/` through recursive traversal rooted at `evidence/`, and their reads are content reads. Whether those reads executed is **unproven**, and the `open_restricted` chokepoint did not exist |
| **Status** | **Open — not started, and deliberately not attempted.** The tests were **not** run during the 2026-08-22 governance work: executing them then would have manufactured the breach rather than documented it |
| **Owner** | `governance-guards` owns the `open_restricted` mechanism the rerun depends on; execution sits with whoever runs the suite at **build-and-test (3.6)** and the Bolt 12 in-Kaggle run |
| **Prerequisite — hard** | `src/data/locked_test.py`'s `open_restricted` **exists and enforces** the approved access procedure. That module is unwritten and gated by **G-09** and stage 3.5, and its routing contract is **BLK-07**, an exit condition on functional design |
| **Due gate** | Before **G-05**, alongside RES-01, whose test gap this rerun is the practical counterpart of |

**What the rerun must do, in order.** Each step is a requirement, not a description:

1. **Establish that the requested access is authorized** — recorded before anything opens.
2. **Write and preserve the access-log entry BEFORE the restricted artifact is opened.**
3. **Fail closed if logging fails.** No read proceeds on a failed or unwritten log entry.
4. **Execute the permitted inspection or verification** — the performance-blind class only.
5. **Capture the resulting report as new evidence**, retained rather than transient.
6. **Record the actual rerun date and time** — the real ones, at the time it runs.
7. **Link the new report to the historical evidence gap** without rewriting the historical
   record.

**Preferred route — synthetic or non-December first, and most of it can be.** Assessed
2026-08-22 against what each module actually does:

- `test_release_hashes.py` — hashes `sha256_manifest.json` artifacts. Verifiable in full
  against the **unrestricted** months (2022-01 through 2022-11) and synthetic fixtures.
- `test_phase_boundary.py` — checks forbidden field names against the D-17 contract.
  Verifiable against unrestricted artifacts and synthetic rows carrying deliberately
  forbidden fields.
- `test_acquisition_window.py` — asserts record dates fall inside declared windows.
  Its **primary** assertion (no December-dated record appears in a non-December folder) is
  verifiable **entirely on unrestricted months**, which is precisely the defect it was
  written for.

**What genuinely needs the restricted root** is narrower than the whole suite: confirming
that the restricted root's *own* artifacts pass the same checks. **That part is not
performed until the applicable gate explicitly permits the access**, and it is not
performed to satisfy this obligation early.

**What this obligation does not do.** It does **not** repair the 2026-08-21 gap, does not
retrospectively authorize that run, and **a passing rerun is never evidence that the
original event was properly logged.** The historical record stands as written.

**RES-01 — what must not be claimed.** Adding `inventory-and-registry` to the
Supporting column of WS-18 and TA-18 assigns **evidence ownership only**. It does
**not** create dedicated test coverage for permitted-read logging, and UG-03's
durable test gap is **not** closed by it. WS-18 and TA-18 as written test the
execution guard — they block *unauthorized* pre-G-05 December performance
execution — which is a different scenario from an *authorized* coverage-audit
read that must still be logged before access. No new acceptance criterion is
created or approved in this stage: the required Vision §15.2 authority is not
available here.

**RES-03 — the derivation rules, stated so 3.1 cannot shortcut them.** No
replacement cardinality may be assumed or hard-coded before the derivation is
performed. The canonical set is derived item by item from TE §2.2 and TE §7.0B
under an explicit deduplication rule, and its cardinality is calculated from the
resulting enumeration. **The derived set must not be forced to equal fourteen
merely to preserve FR-P1-06-1.** Where the two disagree, the
**authority-derived content takes precedence over preserving an unsupported
count** — and FR-P1-06-1 must still be formally reconciled through Vision §15.2
before the phase-transition gate can pass. FR-P1-06-1 is **not** silently
reinterpreted or rewritten by this stage.

**RES-03 — what FR-P1-06-1 does and does not block.** It does **not** block
stage 3.1 from performing the derivation; the derivation is precisely the work
3.1 is obliged to do, and nothing in FR-P1-06-1 forbids it. It **does** block
(a) implementing `TransitionManifest.protected_hashes`' key list to any fixed size before
the derivation exists, and (b) final acceptance at **G-P2** and **G-P3C** until
either the canonical set is shown to match FR-P1-06-1 or FR-P1-06-1 is amended
under §15.2. See **BLK-06**.

## Assumptions & Open Questions

- **[assumption]** `REQ-ENG-5` ("every hard rule has a negative-path test") is a property of the whole suite rather than of one module. It is assigned to `governance-guards` as the unit that owns the negative-control discipline and the independent checks, with `features-and-splits`, `models-and-baselines` and `fixtures-and-reproducibility` recorded as supporting. No other unit was a better single owner, and leaving it unassigned would have broken both-direction coverage.
- **[assumption]** `FR-P1-01-10` (credentials and secrets) is assigned to `foundation`, which owns the environment and platform-root resolution that supplies them, with `acquisition` supporting as the unit that consumes them. The requirement sits in the FR-P1-01 acquisition group, so this placement follows the mechanism rather than the numbering.
- **Upstream drift, recorded not propagated.** `components.md` states "94 requirement rows"; the count derived from `requirements.md` here is **105**, the difference being IDs added in stage 2.3's fourth through sixth revisions. This stage uses 105.
- **Closed 2026-08-22, recorded so the earlier open status is not carried forward.** ADR-10's four-part §12/§13.2 amendment (**BLK-01** — applied to TE v3.4 under `CR-2026-08-22-TE-AMEND`) and **D-122's sign-off** (closed at Vision §14.2, seed values verified unchanged before closure: development seed 42 and final seeds {1337, 2024, 7}. The bootstrap seed **20221201** is frozen separately by TE §13.6 / TC-19 (Q-27) and is **not** part of D-122’s item set — attribution corrected 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 11). Both closures are **authority only**: none of the four ADR-10 modules exists, and the seed values reach `three_seed_mean` as a parameter from `ConfigSnapshot.seeds` via `configs/seeds.yaml` and **must never be inlined in `src/models` or any other implementation file** (TC-03e). BLK-03's contract limb stays open.
- **Still open — all six, enumerated rather than sampled** (corrected 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 6; the earlier bullet named three of six, the shape `project.md` § Way of Working forbids in a handoff). **BLK-02** — `requirements.md` § Known defects row 12's station-selection limb; the reading is settled, the single station is not selected. **BLK-03** — the confirmatory-prediction contract limb; the seed *authority* is closed, the contract is not. **BLK-04** — the per-fold train-only transform contract. **BLK-05** — the D-17 target-schema test has no module name and no §12 entry. **BLK-06** — the canonical protected-set derivation and its three unmapped TE §7.0B immutables. **BLK-07** — `acquisition`'s `open_restricted` routing contract for reads under the restricted December root. BLK-03, BLK-04 and BLK-07 are stage 3.1 **exit** conditions; BLK-02 and BLK-05 are owner/supervisor decisions; BLK-06 blocks G-P2 and G-P3C. § Blocker register and § Roll-up by unit carry each in full.
- **Closed since this artifact's first draft, corrected 2026-08-22.** The one-month all-station scientific fixture window is **no longer open under Q-31**: it was frozen as **D-14** — March 2022, all three cells — by `CR-2026-08-21-FREEZES`, which also records the mandatory limitation that March is an equinox month reproducing neither December's winter-solstice regime nor its activity distribution. An earlier revision of this artifact carried it as open; the freeze supersedes that. Corrected per governance finding `UG-08` (`GOV-2026-08-21-UG-01`).
- **Open, a recorded textual conflict in the governing texts — not resolved here, and not resolved by inference.** Vision §6.6 and TE §6.1 remain in textual conflict on the Phase 1 target contract: §6.6's "Each row must retain exactly these fields" reads over TE §6.1's Phase 2-shaped ten-field list, which includes `valid_satellite_count` and defines `vtec_tecu` "at observed IPPs", while TE §7.0 requires `test_phase_boundary.py` to fail if Phase 1 produces a satellite field. **D-17 governs the approved practical Phase 1 interpretation** — the contract enumerated from the audited five-column product (`ut1_unix`, `gdlat`, `glon`, `tec`, `dtec`), with `valid_satellite_count` recorded not-applicable in Phase 1 and nothing substituted — and `target-standardization` is defined against D-17 on that basis. The underlying source-text conflict has **not** been silently resolved, amended or adopted by inference; it is recorded at `requirements.md` § Known defects row 10. Any permanent reconciliation of §6.6 and TE §6.1 runs through Vision §15.2 change control. Recorded per governance finding `UG-02`.
- **`RES-02` — status: Deferred to authorized gate.** `team-practices.md` § Testing Posture still defines Phase 1's acceptance set as "WS-09 through WS-20". Approved requirement **FR-WS-4** additionally includes **WS-01 as a named exception** (WS-09–WS-20 countersigned 2026-08-16; the WS-01 exception approved 2026-08-21 under the recorded authority equivalence). **Current and downstream work follows the approved FR-WS-4 interpretation: WS-01 plus WS-09 through WS-20.** `team-practices.md` remains textually stale; correcting it is deferred to the next authorized practices-affirmation gate, `org.md` reserving that file for that gate, and it is **not** edited here or anywhere in this remediation. This discrepancy must **not** be read as an unapproved change to the accepted test set — the accepted set is FR-WS-4's. The separate "17 §12-tree modules" figure in the same file is a **second** stale figure, and it is now stale in a way it was not before: **BLK-01 closed 2026-08-22**, the amended TE §12 tree enumerates **19** test modules, and REQ-ENG-4 was re-derived to 19 from that tree. The 17-versus-19 question is therefore settled **in the authority documents**; what is not settled is `team-practices.md`, which is **untouched here and must stay untouched** — `org.md` reserves that file for the practices-affirmation gate. Both stale figures are carried on the same `RES-02` row. Recorded per governance finding `UG-06`; tracked as `RES-02` in § Residual governance obligations.
- **`RES-01` — status: Ownership remediated; dedicated test coverage open. This scenario is NOT TESTED.** No dedicated acceptance criterion verifies that a **permitted** December read — including the required pre-G-05 coverage and regime audit — writes its `locked_test_accessed = true` access-log row **before** the first December record is read. Adding `inventory-and-registry` to WS-18's and TA-18's Supporting column assigns evidence ownership and creates **no** test coverage; WS-18 and TA-18 as written test the execution guard against *unauthorized* pre-G-05 performance execution, a different scenario. The candidate criterion is routed to stage **3.2** through **Vision §15.2** change control and must distinguish permitted coverage-audit access from prohibited pre-G-05 performance execution. **No new acceptance criterion is created or approved in this stage** — the required §15.2 authority is not available here. UG-03's durable test gap is **not** closed. Tracked as `RES-01`.
- **`RES-03` — status: Pending canonical derivation; amendment conditionally required.** FR-P1-06-1 still requires `protected_hashes.keys()` to equal a "fourteen-item enumeration". Stage **3.1** must derive the canonical protected set item by item from TE §2.2 and TE §7.0B under an explicit deduplication rule; **no replacement cardinality may be assumed or hard-coded before that derivation**, and the derived set must **not** be forced to equal fourteen merely to preserve FR-P1-06-1. Where the canonical set differs in content or cardinality, the **authority-derived content takes precedence over preserving an unsupported count**, and FR-P1-06-1 must still be formally amended through §15.2 before the phase-transition gate can pass. FR-P1-06-1 is **not** silently reinterpreted or rewritten here. Tracked as `RES-03`; see **BLK-06**.
- **Open, a `requirements.md` change.** The advisory NOT-READY finding on FR-P1-05-18 (no criterion tests the storm-event count's source) and the 40 requirements with no §16/§19 row. Both are inputs to stages 3.1 and 3.2, not resolvable here.
- **Open, a §12 defect.** The `02` ordinal collision between the Phase 1 and Phase 2 target scripts, carried from `services.md` unresolved.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-21T15:52:15Z
**Iteration:** 4 (advisory, single pass)

> **Scope annotation added 2026-08-22 — this receipt does not cover the current text.**
>
> The verdict above was issued against the **2026-08-21 revision** of these artifacts.
> The set has since been materially rewritten twice: on 2026-08-22 under
> `CR-2026-08-22-TE-AMEND` / `GOV-2026-08-22-REM-01` (BLK-01 closed, BLK-02 partly
> discharged, BLK-03 and BLK-04 reworded from entry to exit conditions, BLK-06
> registered, the D-14 fixture-window correction applied), and again on 2026-08-22
> under `GOV-2026-08-22-UG-02` Recommendations 1–8 (BLK-07 registered, BLK-01 and
> D-122 closures propagated, the restricted-root carve-out stated, `requirements.md`
> row 12 amended).
>
> **No re-review has been run against the current text**, and the verdict above must
> not be read as covering it. The statements below that are stale by that change are
> **preserved rather than edited**, because a reviewer's receipt is a record and not a
> working document. Enumerated rather than counted (an earlier version of this
> annotation asserted "two", underived, in an annotation whose whole subject is
> unreliable counts — corrected 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 8):
>
> 1. the BLK-01 count caveat, which the register has since closed;
> 2. **D-122**, listed among "carried-forward open items", closed 2026-08-22;
> 3. **the Q-31 fixture window**, listed as open, frozen as **D-14** (March 2022);
> 4. the roll-up table's line reference (563), which has moved to 613–624;
> 5. the `**Blockers.**` prose line reference (463–464), now 468;
> 6. the story-map gaps-table line reference (280–291), now roughly 283–297.
>
> A fresh advisory pass is an outstanding item recorded in `GOV-2026-08-22-UG-02`
> § Human decisions still required; the owner approved Recommendation 5 option 3 —
> annotate now, re-review after remediation lands.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| — | — | — | None. | — |

### Validation Tool Results

No scripted validation tool is declared for this stage; checks below were performed by direct derivation against the artifact set and the named upstream contracts.

- **The two carried-forward fixes hold.** `fixtures-and-reproducibility`'s `Blockers` column (line 56), its `**Blockers.**` prose (lines 463–464), the roll-up table (line 563), and `unit-of-work-story-map.md`'s "Open verification gaps" table (lines 280–291) all now carry `BLK-01, BLK-02, BLK-03 ↓, BLK-04 ↓` consistently. `artifacts/` (line 106) is owned by `foundation` with a stated reason ("this unit creates the skeleton and owns the release API that writes into it"), consistent with `components.md`'s layering (no package owns it either) and with TA-01/REQ-ENG-1's enumeration.
- **Ownership exhaustively checked.** Enumerated every §12 tree item from `components.md` (six `src/` packages' modules), `services.md` (nine stage scripts + orchestrator, five notebooks), and `team.md`'s 17+2 mandated test modules against every unit's `Owns` list. Every Phase-1-applicable item resolves to exactly one owning unit, none twice. The four `src/gnss/*` modules, `scripts/02_build_vtec_target.py`, and the three Phase-2-only test modules (`test_rinex_schema.py`, `test_dcb_sign.py`, `test_hourly_target.py`) are correctly unowned — they are Phase 2 scope, and this document's title and every source package it draws on (`requirements.md`'s 105 FR-P1-* rows) are Phase 1 only.
- **Counts independently derived, not carried.** Grepped `requirements.md` for exact-match `| <ID> |` rows: **105** distinct requirement IDs, matching the document's claim. Independently extracted the 40 `UNTESTED` rows by ID: **40**, matching both `unit-of-work.md` and the story-map's per-unit "no acceptance row" list ID-for-ID (summed the per-unit breakdown: 2+1+7+2+1+5+4+7+2+7+2 = 40). Per-unit requirement totals sum to 105; per-unit "Requirements carried… Bold" counts match the per-unit untested breakdown exactly. Acceptance-row primary-owner count sums to 39 (7+2+1+3+1+1+9+5+1+2+3+4). WS rows in Table 2: 13, distinct. TA rows: 27, distinct (26 enumerated + TA-27's first limb). Edge block: counted `depends_on` list lengths — 0+1+2+1+1+1+3+1+2+1+1+9 = **23** edges over 12 uniquely-named units, matching the claimed figure.
- **DAG structure.** The edge block is acyclic by construction (a strictly increasing dependency layering with no back-edge), every `depends_on` name is a declared unit, no self-dependency, every `kind` is `library` (matches the Q6=X rule stated and applied). The one independent pair (`target-standardization` ∥ `external-products`) was verified by tracing reachability in both directions — no other pair in the 12-unit graph lacks a directed path either way.
- **Blocker correctness against upstream.** `BLK-03`'s and `BLK-04`'s cited signatures (`three_seed_mean(predictions: Sequence[Prediction]) -> Prediction`, `fit_transforms(train: DataFrame, *, fold: FoldSpec) -> Transform`) match `component-methods.md` lines 386–387 and 419 verbatim in shape. `BLK-01`'s ADR-10 count caveat ("only REQ-ENG-4 and the external TE §12 tree are genuine loci… `team-practices.md` states a deliberately different figure and must not be edited to 19") matches `decisions.md`'s own Major finding at line 439 word for word in substance. No blocker is discharged by convenience: BLK-02 names no station count, BLK-03 names no seed values, BLK-05 names no test module — each explicitly declines to choose.
- **Stage-boundary discipline.** No build order or critical path is stated anywhere in the three artifacts; both TC-06 and TE §9.2 are explicitly and correctly distinguished as an inter-unit edge versus an intra-unit ordering contract, per the project-level learning this stage itself produced on the prior iteration.
- **Q&A fidelity.** Q1=C (hybrid), Q2=B (12, within the 9–12 band), Q3=A override (`test_determinism.py` stays in `foundation` — confirmed in `foundation`'s Owns list), Q5=A override (no separate phase-transition unit — `phase_contract.py` lives in `governance-guards`, confirmed), Q6=X (the stated `kind` rule is applied uniformly), Q7=A (independence framed as a graph property, not readiness, in both `unit-of-work-dependency.md` and the blocker register's cross-reference) all check out against the questions file.
- **Carried-forward open items** — FR-P1-05-18's advisory NOT-READY, the `02` ordinal collision, the 40 untested requirements, TA-24's missing owner, D-122, the Q-31 fixture window, and the AGPLv3 question — are all present and unresolved-as-stated in `unit-of-work.md` § Assumptions & Open Questions and the story-map's § Open verification gaps, none silently dropped or resolved by convenience.

### Summary

Both Major findings from the prior pass are fixed and consistent across all five blocker representations and the `artifacts/` ownership fix. An exhaustive re-derivation of every count (105 requirements, 40 untested, 23 edges, 13 WS/27 TA rows, 1 independent pair) reproduces the artifact's own figures exactly, and ownership coverage across the §12 tree has no double- or un-owned Phase-1 item. No new Critical or Major issue surfaced this pass; the artifact set is implementable as topology without further architectural guidance.

