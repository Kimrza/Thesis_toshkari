# Unit of Work — Hourly VTEC Forecasting (TEC_Project Phase 1)

Stage 2.7 (units-generation), intent `260813-tec-hourly-forecast`.
Depth: Comprehensive. Scope: `research-pipeline-governed`.

## Sources

- Design: `../application-design/components.md` (the six `src/` packages, module ownership, the three **NEW** modules), `../application-design/component-methods.md` (boundary signatures), `../application-design/services.md` (the nine stage scripts, the stage entry contract, the two platforms), `../application-design/component-dependency.md` (the import allowlist, the forbidden edges, the data flow), `../application-design/decisions.md` (ADR-01…ADR-10).
- Requirements: `../requirements-analysis/requirements.md` — **105** requirement rows, **36** with no §16/§19 test row. *(Corrected 2026-08-23: this read **40**, superseded on 2026-08-22 when `FR-P1-04-12`, `FR-P1-04-13`, `FR-P1-04-16` and `FR-P1-04-17` gained acceptance rows TA-33 through TA-36 under `CR-2026-08-22-LEAKAGE-TA`. `requirements.md` § Requirements with no testing row states 36 directly and records the 40 → 36 change with the four IDs named.)*
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
| 6 | `external-products` | `library` | L | standalone | 7 | **2** | — |
| 7 | `features-and-splits` | `library` | L | standalone | 11 | **12** | BLK-04, BLK-08 (co-owned), BLK-09 |
| 8 | `models-and-baselines` | `library` | L | standalone | 9 | 5 | BLK-03, BLK-04 ↓, BLK-09 ↓ |
| 9 | `evaluation-and-comparison` | `library` | M | standalone | 4 | 1 | BLK-08, BLK-03 ↓, BLK-04 ↓, BLK-09 ↓ |
| 10 | `statistical-inference` | `library` | M | embedded | 1 | 2 | BLK-03 ↓, BLK-04 ↓, BLK-08 ↓, BLK-09 ↓ |
| 11 | `regimes-diagnostics-reporting` | `library` | L | embedded | 11 | 3 | BLK-03 ↓, BLK-04 ↓, BLK-08 ↓, BLK-09 ↓ |
| 12 | `fixtures-and-reproducibility` | `library` | M | standalone | 8 | 4 | BLK-02, BLK-03 ↓, BLK-04 ↓, BLK-08 ↓, BLK-09 ↓ (BLK-01 closed 2026-08-22) |

> **⚠ Acceptance-rows cells corrected 2026-08-23 — rows 6 and 7 read 1 and 9.**
> `FR-P1-04-17` gained **TA-36**, and `FR-P1-04-12`, `FR-P1-04-13`, `FR-P1-04-16`
> gained **TA-33**, **TA-34**, **TA-35**, all on 2026-08-22 under
> `CR-2026-08-22-LEAKAGE-TA`. The per-unit sections were corrected first and this
> table, which summarizes them, was not — the fourth time in this stage that a
> corrected fact stood one section away from an unswept mirror of the superseded one.
>
> *Every cell in this column was re-derived after the fix, not just the two named.*
> Reading the twelve `**Acceptance rows (N).**` lines in document order gives
> **7, 2, 1, 3, 1, 2, 12, 5, 1, 2, 3, 4**, which is exactly this column top to bottom.
> The `Requirements` column was re-derived the same way against the twelve
> `**Requirements carried (N).**` lines and agrees throughout. Both figures in every
> row of this table now match the section they summarize.

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
- **`artifacts/registry/release_history.jsonl`** — the durable, append-only release-history ledger from which human-readable release labels are allocated, kept **separate** from `experiment_registry.jsonl`. *(Added 2026-08-24 under `CR-2026-08-24-FOUNDATION-AMENDMENTS` Amendment C, on the project decision owner's approval. Its authority is `functional-design`'s **Q6=D** — a monotonic, human-readable label alongside the authoritative content hash — and **FU-2=D**, which names the ledger, its ownership and its append-only behaviour. A monotonic label needs durable state, which a directory scan cannot provide: delete a release and a rebuilt index forgets its label. **Release identity remains the content hash** per R-11; this ledger carries the citation label only. No TE §12 amendment was required — `artifacts/registry/` is already enumerated and the tree carries zero file-level entries inside `artifacts/`.)*
- `artifacts/` — the top-level output tree REQ-ENG-1 enumerates and TA-01 checks. Owned here because this unit creates the skeleton and owns the release API that writes into it; every other unit writes its released artifacts *into* this tree without owning it.
- `tests/` tree and shared fixtures/conftest, `tests/test_determinism.py` (**NEW**), `tests/test_release_hashes.py`

**Boundary.** The only unit that reads `configs/`, and (with `acquisition`) one of two permitted to construct a path into `evidence/` — **except `evidence/locked_test_restricted/`, which only `src/data/locked_test.py` may reach**. `component-dependency.md` § Shared resources fixes that carve-out without qualification ("nothing else may construct a path into it"), and D-15 records why it matters: the restricted root is a governance boundary, not an access control, so it holds only while exactly one code path reaches it. See **BLK-07**. Exposes `ConfigSnapshot`, the seeded-run contract, resolved platform roots and the release API. Imports nothing from any other unit — this is the DAG's first root.

**Requirements carried (16).** REQ-ENG-1, REQ-ENG-2, REQ-ENG-3, REQ-ENG-4, REQ-ENG-6, **REQ-ENG-7**, REQ-ENG-8, **REQ-ENG-10**, REQ-ENG-11, FR-P1-01-10, FR-P1-04-11, FR-P1-05-13, FR-WS-7, NFR-AUD-01, NFR-SEC-01, NFR-DET-01

Bold = no §16/§19 test row (2 of 16 here).

**Acceptance rows (7).** TA-01, TA-02, TA-03, TA-10, TA-15, TA-22, TA-23

**Blockers.** **None open. BLK-01 closed 2026-08-22** (`CR-2026-08-22-TE-AMEND`, on `GOV-2026-08-22-REM-01` Recs 1 and 4): `src/data/config.py` and `tests/test_determinism.py` are now named in TE §12. **Authority only** — neither module exists, and creating them stays gated by **G-09**, TE §18.3's stop-and-report rule and stage **3.5 `code-generation`**. This unit's other owned artifacts were never blocked. See § Blocker register.

**Implementation notes and constraints.**

- `src/data/config.py` and `tests/test_determinism.py` now have authority backing: ADR-10's four-part §12/§13.2 amendment was approved 2026-08-22 by the project owner under the recorded student/supervisor authority equivalence and applied to TE §12 under `CR-2026-08-22-TE-AMEND` (TE v3.4). **Authority to name a module is not authority to write one** — neither module exists, and `code-generation` must not create either before G-09.
- ADR-10's third row moved REQ-ENG-4's test-module count 18 → 19, and that move was **applied 2026-08-22**. **Two further same-day amendments then superseded it, and this bullet is corrected accordingly (2026-08-22, `CR-2026-08-22-INC-CORRECTIONS`, per `GOV-2026-08-22-INC-01` Rec 3): the count is 21, not 19.** `CR-2026-08-22-TARGET-SCHEMA-TEST` added `test_prepared_target_schema.py` (19 → 20) and `CR-2026-08-22-LEAKAGE-TA` added `test_feature_leakage_guards.py` (20 → 21); REQ-ENG-4 now reads **21**, re-derived from the amended TE §12 tree by enumerating its `test_*.py` entries rather than carried from prose. **Superseded text, preserved for the audit trail:** *"REQ-ENG-4 now reads 19, re-derived from the amended TE §12 tree"*. The advisory finding on `decisions.md` named only REQ-ENG-4 and the external TE §12 tree as genuine loci of that count; **that claim was inherited without independent verification and is corrected here — there are three.** The third is `requirements.md` § Intent analysis, which read "the remaining fifteen of REQ-ENG-4's eighteen test modules" and was wrong twice against the tree as it then stood; it was corrected 2026-08-22 under `GOV-2026-08-22-UG-02` Rec 3. **Against the tree as it now stands the total is 21 and, with three modules existing, the remainder is 18.** Separately, `team-practices.md` § Testing Posture states a deliberately different figure (17 §12-tree modules), is now stale on it, and **must still not be edited here** — `org.md` reserves that file for the practices-affirmation gate, and the correction is tracked as **RES-02**.
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

**Blockers.** **None open, and none inherited.** This unit owns no blocker, and its `depends_on` reaches only `acquisition`, whose **BLK-07** bounds that unit's own reads under the restricted December root rather than anything this unit consumes: the released source inventory and station registry it produces are unaffected by the routing contract BLK-07 registers. *(Stated explicitly 2026-08-23. This unit previously carried no `**Blockers.**` line at all, expressing "none" by omission where every other unit states it — including `foundation`, which says so in words. Silence and "none" are not the same claim to a stage-3.1 reader, and the summary table and roll-up both already recorded this unit as carrying none.)*

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

**Requirements carried (7).** **REQ-ENG-9**, FR-P1-04-3, **FR-P1-04-4**, FR-P1-04-9, **FR-P1-04-15**, FR-P1-04-17, **FR-P1-04-18**

Bold = no §16/§19 test row (**4** of 7 here). *(Corrected 2026-08-23 from 5: `FR-P1-04-17` gained **TA-36** on 2026-08-22 under `CR-2026-08-22-LEAKAGE-TA` and is no longer untested.)*

**Acceptance rows (2).** WS-09, **TA-36** (`Pending` — the row exists; no test is implemented, executed or passing)

**Implementation notes and constraints.**

- Driver series are time-indexed only — one value per epoch, identical across all three cells. A join must never imply a per-cell measurement, and a station performance difference must never be attributed to local forcing the dataset does not contain.
- No driver may be backfilled from future final or definitive archived values, and Kyoto Dst release grades must never be mixed within one series.
- Dst is diagnostic/hindcast-only and never a confirmatory ML feature. Provisional Dst may characterise fixture selection only — never a modelling input, a frozen tolerance, or a G-05 regime count.
- A centered rolling mean for F10.7 is a defect, not a fallback.
- IRI-2016 generation is blocked if its validation report fails. Nothing in this unit's output may reach training or inference: IRI and GIM join only at evaluation time onto the already-frozen comparison-wide mask.
- `audit_ec1_drivers.py` migrates here, gaining `--config configs/` and its numbered position; its exit-code gap (returning 0 regardless of missing months) is closed at migration.

**Blockers.** **None open, and none inherited.** This unit owns no blocker, and its only dependency is `inventory-and-registry`, which carries none either. Its outputs — the driver series, the IRI-2016 benchmark (B-01) and the CODE final GIM comparator (C-01) — are consumed downstream by units that do carry blockers, but a blocker travels **with a consumed contract**, and none of the open eight names a contract this unit produces. *(Stated explicitly 2026-08-23, for the same reason as `inventory-and-registry` above: this unit expressed "none" by omission where every other unit states it. Note that `FR-P1-04-17`, carried here, gained **TA-36** on 2026-08-22 — an acceptance row, not a blocker.)*

---

## 7. `features-and-splits` — Features and Splits — the permitted ML input space, folds, embargo

**Kind** `library` · **Complexity** L · **Deployment** standalone · **Depends on** `target-standardization`, `external-products`, `governance-guards`

**Responsibility.** Construct the closed ML input space and the partitions that make forecasting honest: the availability matrix asserting actual lag ≥ declared safe lag per feature, feature construction that raises on anything outside the §6.2 dictionary or carrying an `iri_*` field, per-fold train-only transforms, one shared window definition emitting both the flattened matrix and the sequence tensor, the F1–F4 exact calendar folds with their 24-hour embargo, and the December locked partition's execution guard.

**Owns.**

- `src/features/availability.py`, `build.py`, `transforms.py`, `windows.py`
- `src/data/splits.py` — F1–F4, the 24-hour embargo, `materialise_locked_partition` (the execution limb of ADR-03's split guard)
- `scripts/05_build_features_and_splits.py`
- `tests/test_feature_availability.py`, `tests/test_iri_denial.py`, `tests/test_split_embargo.py`, `tests/test_train_only_transforms.py`, `tests/test_locked_test_guard.py`
- **Authorship of the M10 contract fixture** (added 2026-08-23, owner ruling Q12 = C). ADR-11's redesigned leakage boundary cannot be exercised by either mandated walking-skeleton fixture: partitions come from the frozen 2022 calendar boundaries, while D-11 froze the plumbing window at 2022-11-01 to 2022-11-07 and the one-month scientific window is still open under Q-31. This unit therefore authors a **synthetic** fixture over synthetic partition dates, asserting four things — (a) the identity check raises for **every** ordered pair of partition ids except the enumerated `REFIT` → `DEC`, by enumeration rather than sampling; (b) that pair passes with `role="score"` and raises with `role="train"`; (c) `fit_transforms` raises when the bundle's scored range is not exactly the partition's training range; (d) `06`/`07` and `fit_predict` raise on any bundle with `transform_id is None`. It goes in the **existing** mandated modules `test_train_only_transforms.py` and `test_split_embargo.py`, both already owned above — deliberately **not** a new `tests/fixtures/` directory, which would be a §12 tree amendment needing its own change record. Authored here; **run** by `fixtures-and-reproducibility` in the clean-run sequence (Q12 = C's split)

**Boundary.** Imports `target-standardization`, `external-products`'s `spaceweather` only, and `governance-guards`. Must not import `src/external/iri.py`, `src/external/gim.py` or any `src/gnss` module. `windows.py` owning both representations is what makes matched-window parity checkable rather than aspirational.

**Requirements carried (11).** FR-P1-04-1, FR-P1-04-2, FR-P1-04-5, FR-P1-04-6, FR-P1-04-8, **FR-P1-04-10**, FR-P1-04-12, FR-P1-04-13, FR-P1-04-16, NFR-IRI-01, NFR-LEAK-01

Bold = no §16/§19 test row (**1** of 11 here). *(Corrected 2026-08-23 from 4: `FR-P1-04-12`, `FR-P1-04-13` and `FR-P1-04-16` gained **TA-33**, **TA-34** and **TA-35** on 2026-08-22 under `CR-2026-08-22-LEAKAGE-TA` — the same change record behind this document's 40 → 36 headline. Only `FR-P1-04-10` remains untested here.)*

**Acceptance rows (12).** WS-10, WS-11, WS-12, WS-13, WS-18, TA-07, TA-08, TA-11, TA-18, **TA-33**, **TA-34**, **TA-35** (the three added rows are `Pending` — rows that exist, not tests that have run)

**Blockers.** **BLK-04**, **BLK-08** (co-owned), **BLK-09** — this unit carries three of the register's eight open entries, more than any other.

**BLK-04** — owned scope blocked: `src/features/transforms.py`'s `fit_transforms`, and every assertion of NFR-LEAK-01 that runs through it. Downstream units affected: `models-and-baselines`, `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting` — every reported number inherits the fit. Required resolution: a governed cross-unit contract enforcing train-only fitting per **partition**, defining input and output types, alignment requirements, ownership of the fitted state, allowed partitions and failure conditions, so validation and locked-test leakage are prevented by the contract rather than by review. **The mechanism is ADR-11's identity check, not containment**: `build_features` raises `LeakageError` when `transform.partition_id != spec.partition_id`, except the single enumerated pair `REFIT` → `DEC` with `role == "score"`, and `fit_transforms` raises when the bundle's scored range is not exactly its `partition`'s training range, when `role != "train"`, when `partition_id` disagrees, or when the bundle is already transformed. Approval authority: `functional-design` (3.1) for the contract; Supervisor for the leakage evidence at G-04 and G-05. Status: Open. **Exit condition on stage 3.1, not an entry condition — ruled 2026-08-22 by the project decision owner (`GOV-2026-08-22-REM-01` Rec 2).** `features-and-splits` and the downstream units above **may enter** `functional-design` (3.1); that is where the contract is authored. **No affected unit may complete or exit 3.1 without its approved contract**, and **no implementation may proceed** while this blocker stands.

> **⚠ MECHANISM CORRECTED HERE 2026-08-23, one pass after the register entry.** This
> paragraph read: *"train-only fitting per fold … allowed partitions (the named fold's
> training partition only) and failure conditions (`LeakageError` when `train`'s index
> is not a subset of that partition)"*, and closed by restating the same containment
> rule as an unweakened safeguard. **ADR-11 rejected containment outright** — the
> training ranges nest, so F4's transform on April passes every containment test while
> F4's fit saw April. The register entry for BLK-04 was rewritten under the owner's
> Q8 = A ruling; **this paragraph was not**, and for one pass the two disagreed while
> a unit-scoped reader would only ever see this one. Corrected under the owner's
> ruling of 2026-08-23 at the approval gate, together with the summary table and the
> per-unit paragraphs of every unit BLK-08 and BLK-09 reach.

**BLK-08** (co-owned with `evaluation-and-comparison`) — owned scope blocked: `Transform` and its fitted state, which is what `Transform.inverse` would read. The inverse is specified as reachable from `Prediction.transform_id`, a `str`, with no lookup, registry or import edge named, so `ABL-DIFF`'s obligation to inverse-transform to absolute TECU before any metric has no executable path. Whatever 3.1 chooses changes **both** units' contracts. Status: Open; exit condition on 3.1 for both owners.

**BLK-09** — owned scope blocked: `src/data/splits.py`'s `Partition`, which carries no `train_start`. That is the value BLK-04's own newly-stated raises compare against, reachable today only by an unwritten January-1 convention. Deriving it from `train_end` and a hard-coded year is not available — TC-03e forbids a scientific constant in source. Status: Open; exit condition on 3.1.

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

**Blockers.** **BLK-03** — owned scope blocked: `src/models/train.py`'s confirmatory-prediction path, this being the unit that owns confirmatory-prediction construction. Downstream units consuming that prediction: `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`. Required resolution: a governed cross-unit contract defining input and output types, alignment requirements, ownership of the frozen seed set, allowed partitions and failure conditions, with the frozen set arriving as a parameter from `ConfigSnapshot.seeds` — never inlined in `src/models`, never weakened to a distinctness check. Approval authority: `functional-design` (3.1) for the contract. The seed values themselves: **closed 2026-08-22** — D-122's supervisor sign-off was closed by the project owner under the recorded student/supervisor authority equivalence (Vision §14.2; `CR-2026-08-22-TE-AMEND`), with the values verified unchanged before closure: development seed 42 and final seeds {1337, 2024, 7}. The bootstrap seed **20221201** is frozen separately by TE §13.6 / TC-19 (Q-27) and is **not** part of D-122’s item set — attribution corrected 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 11. **That closes authority, not implementation** — the values reach `three_seed_mean` as a parameter from `ConfigSnapshot.seeds` via `configs/seeds.yaml` and **must never be inlined in `src/models` or any other implementation file** (TC-03e; the forbidden pattern this blocker names). **The parameter now exists** — `three_seed_mean(predictions, *, expected_seeds: frozenset[int])`, added 2026-08-23; that limb of BLK-03 is resolved and the contract limbs remain open. **BLK-04 ↓** and **BLK-09 ↓** inherited from `features-and-splits` — the transform fit this unit trains on, and the training range that fit compares against, which no field states (BLK-09 added 2026-08-23). Status: Open. **Exit condition on stage 3.1, not an entry condition — ruled 2026-08-22 by the project decision owner (`GOV-2026-08-22-REM-01` Rec 2).** `models-and-baselines` and the downstream units above **may enter** `functional-design` (3.1); that is where the contract is authored. **No affected unit may complete or exit 3.1 without its approved contract**, and **no implementation may proceed** while this blocker stands. The confirmatory-seed safeguard is unchanged and is not weakened: the frozen set reaches `three_seed_mean` as a parameter from `ConfigSnapshot.seeds`, never inlined in `src/models`, and never weakened to a pairwise-distinctness check.

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

**Blockers.** **BLK-08** (owned), **BLK-03 ↓**, **BLK-04 ↓**, **BLK-09 ↓**.

**BLK-08 is owned here** — added 2026-08-23. `Transform.inverse` is specified as reachable from `Prediction.transform_id`, which is typed `str`; no lookup, registry or resolution step is named anywhere in the 2.6 design, and `component-dependency.md` carries no `src/evaluation` → `src/features` edge. **This unit therefore cannot inverse-transform model output back to TECU** — and `project.md` § Mandated requires `ABL-DIFF` to do exactly that before any metric. It blocks a reported quantity, not an internal detail: the paired loss differential, the bootstrap interval and the practical-relevance threshold are all TECU-denominated. Co-owner: `features-and-splits`, where `Transform` and its fitted state live. Required resolution: 3.1 states first whether the transform touches the target, then either names the resolution mechanism and adds the matching dependency row, or records explicitly that it does not so the obligation is visibly satisfied. Status: Open; exit condition on 3.1 for both owners.

**BLK-03 ↓** — this unit consumes the confirmatory prediction, so its masks and paired loss differential inherit whatever `three_seed_mean`'s contract turns out to permit. **BLK-04 ↓** — every metric it computes inherits the transform fit. **BLK-09 ↓** — those metrics are computed over features whose training range no field states. None of the three is owned here. Approval authority: as recorded on each. Status: Open (inherited). **All are exit conditions on stage 3.1, not entry conditions — ruled 2026-08-22 (`GOV-2026-08-22-REM-01` Rec 2), extended to BLK-08 and BLK-09 on 2026-08-23.** This unit **may enter** `functional-design` (3.1); it **may not complete or exit** 3.1 while any contract is unapproved, and **no implementation may proceed** while they stand.

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

**Blockers.** **BLK-03 ↓**, **BLK-04 ↓**, **BLK-08 ↓**, **BLK-09 ↓** — the bootstrapped differential is computed from the confirmatory prediction over transform-fitted features, so those two inherited contracts bound what this unit's intervals mean. **BLK-08 ↓ bounds their units**: the interval this unit reports is in TECU, and nothing in the current design can invert model output back to it (added 2026-08-23). **BLK-09 ↓** — the fit underlying those features rests on a training range no field states. None is owned here. Approval authority: as recorded on each. Status: Open (inherited). **All are exit conditions on stage 3.1, not entry conditions — ruled 2026-08-22 (`GOV-2026-08-22-REM-01` Rec 2), extended to BLK-08 and BLK-09 on 2026-08-23.** This unit **may enter** `functional-design` (3.1); it **may not complete or exit** 3.1 while any contract is unapproved, and **no implementation may proceed** while they stand.

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

**Blockers.** **BLK-03 ↓**, **BLK-04 ↓**, **BLK-08 ↓**, **BLK-09 ↓** — every reported number, breakdown, figure and claim in this unit derives from the confirmatory prediction and the transform-fitted features, so those inherited contracts bound what may be claimed. **BLK-08 ↓ reaches the claims directly** (added 2026-08-23): the practical-relevance threshold comparison is stated in TECU, and no design path returns model output to TECU. **BLK-09 ↓** — the fit those numbers rest on compares against a training range no field states. None is owned here. Approval authority: as recorded on each. Status: Open (inherited). **All are exit conditions on stage 3.1, not entry conditions — ruled 2026-08-22 (`GOV-2026-08-22-REM-01` Rec 2), extended to BLK-08 and BLK-09 on 2026-08-23.** This unit **may enter** `functional-design` (3.1); it **may not complete or exit** 3.1 while any contract is unapproved, and **no implementation may proceed** while they stand.

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
- **Execution of the M10 contract fixture in the clean-run sequence** (added 2026-08-23, owner ruling Q12 = C). This unit **runs** it; `features-and-splits` **authors** it. Running it here is what puts it inside TA-17's and WS-20's reach, which authorship alone would not

> **⚠ The M10 contract fixture is NOT a third mandated fixture.** It is a **negative
> control on a mechanism**, not evidence about the pipeline, and TC-03f's distinction
> is stated here rather than left to inference. The two mandated walking-skeleton
> fixtures remain exactly two: the seven-day single-station plumbing fixture (smoke
> only, **never** scientific evidence) and the one-month all-station scientific
> fixture. `Technical Environment` §9.2's *"run both walking-skeleton fixtures before
> any full-year job"* is unchanged and unextended by this addition — the contract
> fixture is not one of the "both", and no full-year job gates on it.
>
> **Why it lives across two units.** The owner ruled Q12 = C against a recommendation
> of A (author and run in `features-and-splits`). The recommendation traded coverage
> for lower ceremony; the ruling took the coverage: a fixture authored beside the
> mechanism but run outside the clean-run sequence would never be exercised by TA-17
> or WS-20. The cross-unit contract that split creates is the accepted price, and it
> **adds no dependency edge** — this unit already depends on `features-and-splits`.

**Boundary.** Invokes every stage script; implements no domain logic of its own. Direct edges run to nine units, for two distinct reasons. Seven own a stage script the clean-run sequence invokes directly rather than transitively: `acquisition`, `inventory-and-registry`, `target-standardization`, `external-products`, `features-and-splits`, `models-and-baselines`, `evaluation-and-comparison`. The remaining two, `statistical-inference` and `regimes-diagnostics-reporting`, own **no** stage script — both are `embedded` and run inside `07_evaluate_and_report.py`, which `evaluation-and-comparison` owns — so their edges rest on the artifacts the clean-run tolerance comparison and the traceability matrix consume, not on a script invocation.

**Requirements carried (8).** FR-WS-1, **FR-WS-2**, **FR-WS-3**, FR-WS-4, FR-WS-5, FR-WS-6, NFR-REP-01, REQ-NFR-A3

Bold = no §16/§19 test row (2 of 8 here).

**Acceptance rows (4).** WS-20, TA-09, TA-17, TA-21

**Blockers.** **BLK-02** — owned scope blocked: `tests/fixtures/plumbing_7day/fixture_manifest.yaml` and every capability depending on it. The unit exists in the DAG with its nine dependencies recorded, but the manifest-dependent capability is blocked by `requirements.md` § Known defects row 12 — **on its station-selection limb only**. That row's reading limb was settled by the D-11 clarification of 2026-08-22 and the row was amended in place to record it. **The station was subsequently selected and frozen on 2026-08-22 as BSHM 32/35 (D-20)**, on the only complete observed coverage of the window (168/168 hourly bins). **No manifest may be invented, inferred or substituted**, and this unit still cannot pass its completion gate until the authoritative manifest exists and is hash-verifiable — none exists, and the fixture has never been run. Approval authority: the project owner under Q-31. **BLK-01 closed 2026-08-22** — TE §13.2 now carries the `PYTHONHASHSEED=0` clean-run clause (`CR-2026-08-22-TE-AMEND`), so `test_clean_run.py`, WS-20 and TA-17 test the amended sequence rather than an unamended one. **BLK-03 ↓**, **BLK-04 ↓**, **BLK-08 ↓**, **BLK-09 ↓** — inherited: this unit's `depends_on` includes every unit carrying those blockers (`features-and-splits`, `models-and-baselines`, `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`), and the clean-run tolerance comparison and TA-21's traceability matrix consume their released artifacts, so what those contracts permit bounds what WS-20 and TA-17 can be said to have reproduced. **BLK-08 ↓ and BLK-09 ↓ were added 2026-08-23 by the same stated rule that already brought BLK-03 and BLK-04 here** — it applied to them from the moment they were registered, and the omission was a partial sweep, not a judgement that the rule stops short. BLK-08 in particular bounds the *units* of every tolerance this unit compares: a clean-run tolerance stated in TECU cannot be checked against output no design path returns to TECU. Approval authority: as recorded on each. Status: BLK-02 Open; BLK-03 ↓, BLK-04 ↓, BLK-08 ↓ and BLK-09 ↓ Open (inherited), all **exit conditions on stage 3.1**; BLK-01 **Closed 2026-08-22**.

**This unit also runs the M10 contract fixture** (owner ruling Q12 = C, 2026-08-23), authored by `features-and-splits`. It is a **negative control, not scientific evidence**, and **not** a third mandated walking-skeleton fixture — §9.2's *"both fixtures before any full-year job"* is unchanged and unextended, and no full-year job gates on it.

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
closed; BLK-02 through BLK-09 are open.** **Nine** blockers are registered, and **nine
of the twelve units carry an open blocker row, owned or inherited** — `foundation`,
`inventory-and-registry` and `external-products` carry none. That is the only sense in
which "nine" is meant: BLK-01's `config.py` row named *every* unit as downstream, so a
reading that counted downstream mentions of a closed row would give twelve.

> **⚠ Both figures corrected 2026-08-23, and the second was found by a mechanical
> audit rather than by reading.** This passage read *"BLK-02 through **BLK-07** are
> open. **Seven** blockers are registered, and **ten** of the twelve units carry a
> blocker row … `inventory-and-registry` and `external-products` carry none of their
> own."*
>
> The span and the register size went stale when BLK-08 and BLK-09 were registered on
> 2026-08-23. **The "ten" went stale earlier and by a different route**: it was true
> while BLK-01 was open, because `foundation` carried it; BLK-01 closed on 2026-08-22
> and no sweep asked which *derived* claims that closure invalidated. `foundation`'s
> own row in the summary table has read `— (BLK-01 closed 2026-08-22)` since that day,
> so the two representations had disagreed for a day before either was touched.
>
> **Derived, not carried:** the register's `### BLK-0…` headings → 9; its `| Status |`
> rows, every one beginning `Open` → 8, so 9 entries − 8 open = 1 closed; the summary
> table's Blocker column matched against `BLK-0[2-9]` → 9 of 12 units, with
> `foundation`, `inventory-and-registry` and `external-products` the three that carry
> none.

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
| Affected artifact | `src/models/train.py` — the `three_seed_mean` signature in `component-methods.md`. **Updated 2026-08-23:** the signature is now `three_seed_mean(predictions, *, expected_seeds: frozenset[int])`; the superseded `three_seed_mean(predictions)` is what this blocker was registered against |
| Owning unit | `models-and-baselines` (confirmatory-prediction construction) |
| Downstream units | `evaluation-and-comparison` (masks and the paired loss differential consume the confirmatory prediction), `statistical-inference` (bootstraps that differential), `regimes-diagnostics-reporting` (reports it) |
| Required resolution | A governed cross-unit contract fixing input and output types, alignment requirements, ownership of the frozen seed set, allowed partitions, and failure conditions. The frozen set reaches the function as a parameter sourced from `ConfigSnapshot.seeds` — never inlined, since `{1337, 2024, 7}` in `src/models` is the forbidden pattern, and never weakened to a pairwise-distinctness check a wrong-but-distinct triple would pass. |
| Approval authority | The contract: `functional-design` (3.1) — **still open**. The seed values themselves: **closed 2026-08-22.** D-122's pending supervisor sign-off was closed by the project owner under the recorded student/supervisor authority equivalence (Vision §14.2; `CR-2026-08-22-TE-AMEND`), so the frozen set is authoritative: development seed 42 and final seeds {1337, 2024, 7}. The bootstrap seed **20221201** is frozen separately by TE §13.6 / TC-19 (Q-27) and is **not** part of D-122’s item set — attribution corrected 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 11. **This closes authority, not implementation** — the values are supplied to `three_seed_mean` from `ConfigSnapshot.seeds` via `configs/seeds.yaml` and **must never be inlined in `src/models` or any other implementation file** (TC-03e; the forbidden pattern this blocker names). |
| Status | Open. **Exit condition on stage 3.1, not an entry condition — ruled 2026-08-22 by the project decision owner (GOV-2026-08-22-REM-01 Rec 2).** `models-and-baselines` and the downstream units above **may enter** `functional-design` (3.1); that is where the contract is authored. **No affected unit may complete or exit 3.1 without its approved contract**, and **no implementation may proceed** while this blocker stands. The prior wording ("must be discharged before … enters functional design") was unsatisfiable, since 3.1 is named as the contract's own approval authority. The substantive protection is unchanged and is not weakened: the confirmatory-seed safeguard stands in full — the frozen set reaches `three_seed_mean` as a parameter from `ConfigSnapshot.seeds`, never inlined in `src/models`, and never weakened to a pairwise-distinctness check. |

#### BLK-03 limb status, synchronized 2026-08-23

| Limb | Status | Evidence |
|---|---|---|
| **Seed-set ownership** — the frozen set reaches the function as a parameter rather than an inlined constant | **RESOLVED 2026-08-23** | `component-methods.md` § `src/models` — `expected_seeds: frozenset[int]`, sourced from `ConfigSnapshot.seeds` at the call site. This is the mechanism this blocker's Required-resolution field named, delivered exactly as specified |
| **Input and output types**, **alignment requirements**, **allowed partitions**, **failure conditions** | **OPEN** | No cross-unit contract authored. `AlignmentError` and `SeedError` are named in the design prose but their preconditions are not fixed as a contract between `models-and-baselines` and its three downstream units |
| **Implementation evidence** | **PENDING** | `src/models/train.py` does not exist. Not implemented, not executed, not passing |

**The blocker stays open** on the contract limbs. What closed is the limb the 2.6
advisory reviewer raised, not the contract this entry registers.

### BLK-04 — `fit_transforms` leaves the full-dataset fit representable

| Field | Value |
|---|---|
| Affected artifact | `src/features/transforms.py` — **updated 2026-08-23:** `fit_transforms(bundle: FeatureBundle, *, partition: Partition)`, with `apply_transforms` **removed**. The superseded `fit_transforms(train, *, fold)` / `apply_transforms(...)` pair, and ADR-01's claim about it, are what this blocker was registered against |
| Owning unit | `features-and-splits` |
| Downstream units | `models-and-baselines` (trains on the transformed features), `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting` — every reported number inherits the fit |
| Required resolution | A governed cross-unit contract that enforces train-only fitting per partition: input and output types, alignment requirements, ownership of the fitted state, allowed partitions, and failure conditions. **The mechanism is ADR-11's identity check with one enumerated exception**, not containment: `build_features` raises `LeakageError` when `transform.partition_id != spec.partition_id`, except the single pair `REFIT` → `DEC` with `role == "score"` (the G-06 apply), and `fit_transforms` raises when the bundle's scored range is not exactly its `partition`'s training range, when `role != "train"`, when `partition_id` disagrees, or when the bundle is already transformed. |
| **⚠ Mechanism rewritten 2026-08-23** | **Superseded text, preserved:** *"a `LeakageError` when `train`'s index is not a subset of that partition. The two-function split prevents the single-call convenience shape and nothing more; the contract is what closes the leak."* That prescribed **containment**, which ADR-11 rejected outright after stage 3.1 spent **five** adversarial review cycles on it: the training ranges **nest** (Jan–Mar ⊂ Jan–Jun ⊂ Jan–Sep ⊂ Jan–Oct ⊂ Jan–Nov), so F4's transform applied to April passes every containment test while F4's fit saw April. Leaving the containment wording here would have left this register prescribing the one mechanism the superseding ADR proved cannot work. Rewritten under the owner's ruling of 2026-08-23 (question Q8 = A), discharging the obligation `application-design` deferred to this stage. |
| Approval authority | The contract: `functional-design` (3.1). The leakage evidence it produces: Supervisor, at G-04 and G-05 (NFR-LEAK-01). |
| Status | Open. **Exit condition on stage 3.1, not an entry condition — ruled 2026-08-22 by the project decision owner (GOV-2026-08-22-REM-01 Rec 2).** `features-and-splits` and the downstream units above **may enter** `functional-design` (3.1); that is where the contract is authored. **No affected unit may complete or exit 3.1 without its approved contract**, and **no implementation may proceed** while this blocker stands. The prior wording ("must be discharged before … enters functional design") was unsatisfiable, since 3.1 is named as the contract's own approval authority. The substantive protection is unchanged and is not weakened: the leakage safeguard stands in full — per-partition train-only fitting, with a `LeakageError` raised by the identity check and by `fit_transforms`' range comparison, and NFR-LEAK-01's evidence still owed to the Supervisor at G-04 and G-05. *(This sentence carried the containment wording too; corrected 2026-08-23 with the mechanism row above — sweeping the Required-resolution field alone would have left the same superseded rule standing three rows down.)* |

#### BLK-04 limb status, synchronized 2026-08-23

| Limb | Status | Evidence |
|---|---|---|
| **A mechanism that can execute** — a check the argument closure can compute rather than one stated in prose | **RESOLVED 2026-08-23** | ADR-11 plus its fix pass: `fit_transforms` receives the `Partition`, so the range comparison is computable. `apply_transforms` is removed |
| **The mechanism's real strength, stated honestly** | **RESOLVED 2026-08-23** | ADR-11 § ⚠ THE "UNREPRESENTABLE" CLAIM IS WITHDRAWN. The leak is rejected by an executable raise, **not** unrepresentable in the type — `FrameSpec.partition_id` remains a caller-supplied string. This blocker exists because the earlier overstatement was inherited as fact |
| **Input and output types**, **alignment requirements**, **ownership of the fitted state**, **allowed partitions**, **failure conditions** | **OPEN** | No cross-unit contract authored between `features-and-splits` and its four downstream units |
| **The enumerated negative control** | **OPEN** | `test_train_only_transforms.py` must enumerate every ordered pair of partition ids except `REFIT` → `DEC` `score`, so a second exception cannot be added without a test failing. No test module exists |
| **Implementation evidence** | **PENDING** | `src/features/transforms.py` does not exist. Not implemented, not executed, not passing |

### BLK-05 — the D-17 target-schema test module is mandated but unowned

> **⚠ TITLE AND PREMISE REWRITTEN 2026-08-23 (owner ruling, question Q11 = A).**
> This entry read *"the D-17 target-schema test has no module and no §12 entry"*.
> **Both halves of that condition are now false**: `test_prepared_target_schema.py`
> entered the §12 tree on **2026-08-22** under `CR-2026-08-22-TARGET-SCHEMA-TEST`,
> taking REQ-ENG-4's mandated count to 20 and then, with
> `test_feature_leakage_guards.py`, to **21**. The gap the blocker was registered for
> has **not** closed — it moved: `application-design`'s 2026-08-23 review found the
> module named in **no** module, package or dependency inventory across the five 2.6
> artifacts. It is mandated and unowned. The ID and the owning unit are kept, because
> closing a blocker whose wording was overtaken while its gap persists is the pattern
> this project has corrected repeatedly.

| Field | Value |
|---|---|
| Affected artifact | `tests/test_prepared_target_schema.py` — **in** the §12 tree since 2026-08-22, named by **no** design surface. The D-17 target-schema test implied by FR-P1-03-5's criterion has a module to live in and no module that owns it |
| Owning unit | `target-standardization` |
| Downstream units | `features-and-splits` (consumes the target rows the test would validate) |
| Required resolution | `functional-design` (3.1) for `target-standardization` names the `src/` module whose contract this test asserts, and states which of FR-P1-03-5's criterion limbs each assertion covers. **No further §12 amendment is needed** — that was the superseded premise; the tree entry exists |
| Approval authority | `functional-design` (3.1) for the owning design surface. No §12 amendment, and therefore no §15.2 change record, is required for the module's existence |
| Status | **Open.** Naming, §12-entry and documentation limbs **RESOLVED 2026-08-22**; the **owning-design-surface** limb opened 2026-08-23 and the implementation limb remains pending. See the limb table below. |

#### BLK-05 limb status, synchronized 2026-08-23

**Approving a filename does not resolve the blocker.** Two limbs are complete, and
**three** are not — a limb was **added** 2026-08-23, not merely left open. The table
below carries the two resolved limbs unchanged; the owning-design-surface limb
appears at its foot.

| Limb | Status | Evidence |
|---|---|---|
| **Module naming** | **RESOLVED 2026-08-22** — `tests/test_prepared_target_schema.py` | Approved by the project decision owner; change record `CR-2026-08-22-TARGET-SCHEMA-TEST` |
| **Documentation** — §12 tree entry and downstream artifact updates | **RESOLVED 2026-08-22** | Added to the TE §12 `tests/` tree with its responsibility comment, and to the §12 amendment-provenance table. The tree now enumerates **21** test modules (superseded literal, preserved: "**20** test modules" — see the note below) |

<!--
  "20" → "21" annotated in place 2026-08-22, AFTER this stage's approval gate, on
  the project decision owner's explicit approval at the Gate 0 discharge, under
  the annotate-in-place precedent the owner set at GOV-2026-08-22-INC-01 Rec 7.

  This is a FOURTH site in this file, missed by that record's own Rec 3, which
  corrected three (the ADR-10 bullet, the RES-02 register row, the RES-02
  narrative status). The count's history is 17 → 19 (CR-2026-08-22-TE-AMEND) →
  20 (CR-2026-08-22-TARGET-SCHEMA-TEST) → 21 (CR-2026-08-22-LEAKAGE-TA); every
  value was correct once. "20" entered here from
  CR-2026-08-22-TARGET-SCHEMA-TEST, which computed its own total over one of its
  two amendments — the arithmetic defect Rec 4 corrected in that record without
  reaching this copy of its figure.

  Derived before assertion, not decremented or carried:
    sed -n '675,703p' <TE> | grep -oE 'test_[a-z_]+\.py' | sort -u | wc -l  -> 21

  Recorded in CR-2026-08-22-SWEEP-COMPLETENESS. No blocker limb, status,
  acceptance behaviour or scientific value is changed by this annotation; only
  the module count.
-->
<!-- markdownlint-disable-line -->
| **Owning design surface** | **OPEN — limb added 2026-08-23** | The module is mandated by the §12 tree but named in **no** module, package or dependency inventory across the five `application-design` artifacts. `functional-design` (3.1) for `target-standardization` must name the `src/` module whose contract it asserts. Found by the 2026-08-23 advisory review of `application-design` |
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

### BLK-08 — the inverse transform has no route from the module that needs it

> **Registered 2026-08-23** under the owner's ruling (question Q10 = A), carried
> forward from `application-design`'s approval gate where it was accepted as known
> risk. Same class as BLK-03 and BLK-04: a design surface specified in prose that the
> argument closure cannot execute.

| Field | Value |
|---|---|
| Affected artifact | `component-methods.md` § `src/models` — *"The inverse is therefore a **method on `Transform`** (`Transform.inverse(frame) -> DataFrame`), which travels with the `Prediction`'s `transform_id` and needs no new package edge."* `Prediction.transform_id` is typed `str`. **A string has no method.** No lookup, registry or resolution step is named anywhere in the five 2.6 artifacts, and `component-dependency.md` § Dependency matrix carries **no** `src/evaluation` → `src/features` edge |
| Owning unit | `evaluation-and-comparison` — it is the unit that needs the inverse and cannot reach it |
| Co-owning unit | `features-and-splits` — `Transform` and its fitted state live here, so the resolution mechanism is authored jointly. Whatever 3.1 chooses (a registry keyed by `transform_id`, an `inverse_transform_id` on `Prediction` with a named owner, or a permitted import edge) changes **both** units' contracts |
| Downstream units | `statistical-inference` (bootstraps a differential computed in TECU), `regimes-diagnostics-reporting` (reports it) |
| **What it blocks, stated concretely** | **A reported quantity, not an internal detail.** `project.md` § Mandated requires that *"`ABL-DIFF` inverse-transforms to absolute TECU before any metric"*, and every number the thesis reports — the paired loss differential, the bootstrap interval, the practical-relevance threshold — is in TECU. If the train-only transform touches the target, model output is in transformed space and **nothing in the current design can bring it back** |
| Required resolution | `functional-design` (3.1) states first **whether the transform touches the target**. If it does: name the resolution mechanism, add the matching `component-dependency.md` row, and fix the ownership of the fitted state that `inverse` reads. If it does not: say so explicitly in both `component-methods.md` and ADR-11's consequences, so `ABL-DIFF`'s obligation is visibly satisfied rather than silently assumed |
| Approval authority | The contract: `functional-design` (3.1), jointly for `evaluation-and-comparison` and `features-and-splits`. Any new package edge: the §12 import-boundary rule, which `project.md` § Forbidden constrains — the `iri.py`/`gim.py` allowlist is unaffected, but a `features` → `evaluation` direction would invert the dependency and is not available |
| Status | **Open.** Exit condition on stage 3.1 for both owning units, on the same terms the owner set for BLK-03 and BLK-04 on 2026-08-22: the affected units **may enter** 3.1, and **none may exit** without the contract. No implementation may proceed while it stands |

### BLK-09 — `Partition` cannot state the training range two raises compare against

> **Registered 2026-08-23** under the owner's ruling (question Q10 = A), carried
> forward from `application-design`'s approval gate as accepted risk.

| Field | Value |
|---|---|
| Affected artifact | `component-methods.md` § `src/data/splits.py` — `Partition` carries `partition_id`, `kind`, `train_end`, `validation_month` and `embargo_hours`. It carries **no `train_start`** |
| Owning unit | `features-and-splits` |
| Downstream units | `models-and-baselines`, `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting` — each inherits any fit made against a mis-stated range |
| **Why it matters** | Two raises added on 2026-08-23 compare against *"the partition's training range"*: `fit_transforms` raises when the bundle's scored range is not **exactly** that range, and `build_features` raises when a `train` spec's range is not contained in it. Both are the checks that make ADR-11's mechanism executable — and the value they compare against is not a field. It is reachable only by an **unwritten convention** that every training range starts 1 January 2022. The convention is almost certainly right, and FR-P1-04-5's fold definitions (F1: Jan–Mar; F2: Jan–Jun; F3: Jan–Sep; F4: Jan–Oct; refit: 1 Jan – 30 Nov) do all begin there — but a check that depends on an unstated constant is the defect class this register exists for, and BLK-04's own history is what an unstated rule costs |
| Required resolution | `functional-design` (3.1) either adds `train_start: date` to `Partition`, or states the January-1 rule **explicitly** as a contract term with the authority that fixes it and a test that fails if a partition's training range starts elsewhere. Deriving it from `train_end` and a hard-coded year is **not** available: that would put a scientific constant in source, which TC-03e forbids |
| Approval authority | `functional-design` (3.1) for `features-and-splits`. If the resolution changes any fold boundary — it should not — that is FR-P1-04-5 and a Vision §15.2 change |
| Status | **Open.** Exit condition on stage 3.1 for `features-and-splits`, on the BLK-03/BLK-04 terms |

### Roll-up by unit

| Unit | Blockers | Blocked scope |
|---|---|---|
| `foundation` | — | None open. **BLK-01 closed 2026-08-22**: `src/data/config.py` and `tests/test_determinism.py` are authorized by name only, remain unwritten, and stay gated by G-09 and stage 3.5. |
| `governance-guards` | BLK-06 (implementation limb) | `phase_contract.py`'s `TransitionManifest.protected_hashes` (built by `build_transition_manifest`) and `diff_protected_hashes` (BLK-06) — its `assert_phase_boundary` / `assert_no_raw_fields` limbs and `reuse_registry.py` are unblocked. **BLK-01 closed 2026-08-22**: `src/data/locked_test.py` is authorized by name only and remains unwritten. |
| `acquisition` | BLK-07 | every read or write under `evidence/locked_test_restricted/` — the `open_restricted` routing contract. Its provider-retrieval, provenance, manifest-hashing and NaN-at-acquisition scope is unblocked. |
| `target-standardization` | BLK-05 (implementation limb) | the D-17 schema test only. Module named `tests/test_prepared_target_schema.py` and documented 2026-08-22; **not implemented, not executed**. |
| `features-and-splits` | BLK-04, **BLK-08** (co-owned), **BLK-09** | `transforms.py` and everything asserting NFR-LEAK-01 through it (BLK-04); `Transform`'s fitted state and whatever resolution mechanism reaches its inverse (BLK-08, jointly with `evaluation-and-comparison`); `splits.py`'s `Partition`, whose missing `train_start` is the value BLK-04's own raises compare against (BLK-09). |
| `models-and-baselines` | BLK-03, BLK-04 ↓, **BLK-09 ↓** | `train.py`'s confirmatory-prediction path (BLK-03); the training it performs on transform-fitted features (BLK-04, inherited); any fit made against a training range no field states (BLK-09, inherited). |
| `evaluation-and-comparison` | BLK-03 ↓, BLK-04 ↓, **BLK-08** (owned), **BLK-09 ↓** | anything consuming the confirmatory prediction (BLK-03); every metric computed over transform-fitted features (BLK-04); **`ABL-DIFF` and every TECU-denominated quantity, which cannot be inverse-transformed at all as the design stands** (BLK-08, owned here). |
| `statistical-inference` | BLK-03 ↓, BLK-04 ↓, **BLK-08 ↓**, **BLK-09 ↓** | the bootstrapped differential — and its units, since the interval it reports is in TECU (BLK-08). All inherited. |
| `regimes-diagnostics-reporting` | BLK-03 ↓, BLK-04 ↓, **BLK-08 ↓**, **BLK-09 ↓** | every reported number derived from the above, including the practical-relevance threshold comparison (BLK-08). All inherited. |
| `fixtures-and-reproducibility` | BLK-02 (implementation limb), BLK-03 ↓, BLK-04 ↓, **BLK-08 ↓**, **BLK-09 ↓** | the `plumbing_7day` manifest — hence its completion gate. **Station resolved 2026-08-22 as BSHM (D-20); manifest, execution and measured evidence still pending.** Inherited: the clean-run tolerance comparison and TA-21's traceability matrix consume artifacts from all four units carrying BLK-03 and BLK-04, so what those contracts permit bounds what a clean run can be said to reproduce. **BLK-01 closed 2026-08-22**: TE §13.2 now carries the `PYTHONHASHSEED=0` clause, so the clean-run contract is no longer blocked on its absence. |
| `inventory-and-registry`, `external-products` | — | none of their own; both call `foundation`'s now-authorized stage entry contract, and `inventory-and-registry`'s December coverage audit is already routed through `open_restricted`. |

Roll-up notation matches the `Blockers` column in § Unit definitions and each
unit's `**Blockers.**` line: an unmarked ID is owned here, **↓** is inherited
through a consumed contract.

**Register size, derived from the artifact rather than incremented.** Counting the
`### BLK-0…` headings in this file gives **9** — BLK-01 through BLK-09. Two were
added on 2026-08-23 (BLK-08, BLK-09) under the owner's Q10 = A ruling; the previous
count was 7. The roll-up above carries **11** rows over the twelve units, because
`inventory-and-registry` and `external-products` share one row, having no blockers of
their own. *(Derivation: `grep -c '^### BLK-0' unit-of-work.md` → 9;
`grep -o '^### BLK-0[0-9]'` → the nine IDs listed above with no gap or duplicate. The
roll-up row count is the `| \`` row count inside § Roll-up by unit → 11. Both were run
against this file after the 2026-08-23 edits, not carried from the prior revision.)*

**One of the nine is closed and remains listed** — BLK-01, closed 2026-08-22, whose
heading says so and which carries no `| Status |` row. **Eight stand open.**
*(Derivation: `grep -n '^| Status ' unit-of-work.md` → 8 rows, one each for BLK-02
through BLK-09, every one beginning `Open`. 9 entries − 8 open = 1 closed. Counted
after the 2026-08-23 edits; a first draft of this paragraph asserted "two closed,
seven open" from memory and was wrong, which is why the count is now derived and the
command printed.)*

The two newest — BLK-08 and BLK-09 — both land on `features-and-splits`, which now
carries **three** owned or co-owned blockers (BLK-04, BLK-08 co-owned, BLK-09) and is
the most constrained unit in the register. That concentration is itself an input for
`delivery-planning`: derived from the fenced edge block, `features-and-splits` has
**2 direct dependents** (`models-and-baselines`, `fixtures-and-reproducibility`) and
**5 transitive** ones — those two plus `evaluation-and-comparison`,
`statistical-inference` and `regimes-diagnostics-reporting`. Stated as topology, not
as a sequencing recommendation: what 2.8 does with that concentration is 2.8's
economic decision.

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
| **RES-02** (UG-06) | `team-practices.md` § Testing Posture is stale on two separate figures: it defines the Phase 1 acceptance set as **WS-09 through WS-20**, omitting FR-WS-4's WS-01 exception; and it states **17** §12-tree test modules, where the amended TE §12 tree and REQ-ENG-4 now both read **21** (closure target corrected 19 → 21 on 2026-08-22 under `CR-2026-08-22-INC-CORRECTIONS`, per `GOV-2026-08-22-INC-01` Rec 8; the four modules absent from the affirmed list are `test_acquisition_window.py`, `test_determinism.py`, `test_prepared_target_schema.py` and `test_feature_leakage_guards.py`, three of them leakage/determinism/schema controls) | **Deferred to authorized gate** | Practices-affirmation gate owner | Next authorized **practices-affirmation gate** | The affirmed-practices text amended at that gate to match FR-WS-4's 13-row set **and** the **21**-module count re-derived from the amended TE §12 tree at that time, not restated from this row |
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

### RES-05 — a 3.1 artifact cites a design signature by line number

**Registered 2026-08-23**, carried forward from `application-design`, where it was
finding M14. Recorded as a **residual obligation rather than a blocker**, on the
distinction this register already uses: a blocker names a design surface that cannot
execute as written; this is a citation to repair. Nothing depends on it, and no unit's
3.1 exit turns on it.

| Field | Value |
|---|---|
| Destination artifact | `construction/inventory-and-registry/functional-design/business-logic-model.md`, line 529 — it cites `build_features`'s signature as *"`component-methods.md` line 389"* |
| Why it is stale | The 2026-08-23 amendments to `component-methods.md` moved that anchor. The signature itself also changed: `build_features` now takes `spec: FrameSpec` and `partitions: Sequence[Partition]` and returns a `FeatureBundle` |
| Owner | Architect, at **`functional-design` (3.1)** for the `inventory-and-registry` unit |
| Due | That unit's 3.1 approval gate |
| Acceptance | The re-verification cites the **section heading** rather than a line number, so the anchor cannot go stale again. A line-number citation to a governed design artifact is what made this a defect rather than a routine refresh |

## Assumptions & Open Questions

- **[assumption]** `REQ-ENG-5` ("every hard rule has a negative-path test") is a property of the whole suite rather than of one module. It is assigned to `governance-guards` as the unit that owns the negative-control discipline and the independent checks, with `features-and-splits`, `models-and-baselines` and `fixtures-and-reproducibility` recorded as supporting. No other unit was a better single owner, and leaving it unassigned would have broken both-direction coverage.
- **[assumption]** `FR-P1-01-10` (credentials and secrets) is assigned to `foundation`, which owns the environment and platform-root resolution that supplies them, with `acquisition` supporting as the unit that consumes them. The requirement sits in the FR-P1-01 acquisition group, so this placement follows the mechanism rather than the numbering.
- **Upstream drift, recorded not propagated.** `components.md` states "94 requirement rows"; the count derived from `requirements.md` here is **105**, the difference being IDs added in stage 2.3's fourth through sixth revisions. This stage uses 105.
- **Closed 2026-08-22, recorded so the earlier open status is not carried forward.** ADR-10's four-part §12/§13.2 amendment (**BLK-01** — applied to TE v3.4 under `CR-2026-08-22-TE-AMEND`) and **D-122's sign-off** (closed at Vision §14.2, seed values verified unchanged before closure: development seed 42 and final seeds {1337, 2024, 7}. The bootstrap seed **20221201** is frozen separately by TE §13.6 / TC-19 (Q-27) and is **not** part of D-122’s item set — attribution corrected 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 11). Both closures are **authority only**: none of the four ADR-10 modules exists, and the seed values reach `three_seed_mean` as a parameter from `ConfigSnapshot.seeds` via `configs/seeds.yaml` and **must never be inlined in `src/models` or any other implementation file** (TC-03e). BLK-03's contract limb stays open.
- **Still open — all eight, enumerated rather than sampled** *(count corrected 2026-08-23 from **six**; BLK-08 and BLK-09 were registered that day and this enumeration was not extended with them. Derived from the register's `| Status |` rows — eight, one each for BLK-02 through BLK-09, every one beginning `Open`.)* (Originally corrected 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 6; the earlier bullet named three of six, the shape `project.md` § Way of Working forbids in a handoff.) **Three limbs have since been discharged by frozen decisions; annotated in place 2026-08-22 under `CR-2026-08-22-INC-CORRECTIONS`, per `GOV-2026-08-22-INC-01` Rec 7, on the project owner's approval of the annotate-in-place option.** **BLK-02** — `requirements.md` § Known defects row 12's station-selection limb; the reading was settled and the station was **not** selected when this was written. **Station limb DISCHARGED by D-20** (plumbing fixture station, frozen 2026-08-22 under Q-31); the `fixture_manifest.yaml` limb and its dependent capability remain open. **BLK-03** — the confirmatory-prediction contract limb; the seed *authority* is closed, the contract is not. **Open.** **BLK-04** — the per-fold train-only transform contract. **Open.** **BLK-05** — the D-17 target-schema test had no module name and no §12 entry. **Naming and documentation limbs DISCHARGED**: `tests/test_prepared_target_schema.py` was approved and written into the TE §12 tree 2026-08-22 under `CR-2026-08-22-TARGET-SCHEMA-TEST`; the implementation and execution-evidence limbs remain open, and naming a module is not adding an acceptance row. **BLK-06** — the canonical protected-set derivation and its three unmapped TE §7.0B immutables. **Enumeration limb DISCHARGED by D-24** (seventeen items, cardinality calculated), with FR-P1-06-1 amended 14 → 17 under `CR-2026-08-22-PROTECTED-SET`; per-item binding to config fields and the implementation of `protected_hashes` / `diff_protected_hashes` remain open, so BLK-06 still blocks G-P2 and G-P3C. **BLK-07** — `acquisition`'s `open_restricted` routing contract for reads under the restricted December root. **Open.** **BLK-08** — `Transform.inverse` is reachable only from `Prediction.transform_id`, a `str`, with no lookup, registry or import edge named, so `ABL-DIFF`'s obligation to inverse-transform to absolute TECU before any metric has no executable path. Owned by `evaluation-and-comparison`, co-owned by `features-and-splits`. **Open — registered 2026-08-23.** **BLK-09** — `Partition` carries no `train_start`, so the training range that two of ADR-11's raises compare against rests on an unwritten January-1 convention. Owned by `features-and-splits`. **Open — registered 2026-08-23.** BLK-03, BLK-04, BLK-07, **BLK-08 and BLK-09** are stage 3.1 **exit** conditions; BLK-02 and BLK-05 are owner/supervisor decisions. **No blocker is closed outright by this annotation** — each retains at least one open limb, and the count of open blockers is **eight**. § Blocker register and § Roll-up by unit carry each in full.
- **Closed since this artifact's first draft, corrected 2026-08-22.** The one-month all-station scientific fixture window is **no longer open under Q-31**: it was frozen as **D-14** — March 2022, all three cells — by `CR-2026-08-21-FREEZES`, which also records the mandatory limitation that March is an equinox month reproducing neither December's winter-solstice regime nor its activity distribution. An earlier revision of this artifact carried it as open; the freeze supersedes that. Corrected per governance finding `UG-08` (`GOV-2026-08-21-UG-01`).
- **Open, a recorded textual conflict in the governing texts — not resolved here, and not resolved by inference.** Vision §6.6 and TE §6.1 remain in textual conflict on the Phase 1 target contract: §6.6's "Each row must retain exactly these fields" reads over TE §6.1's Phase 2-shaped ten-field list, which includes `valid_satellite_count` and defines `vtec_tecu` "at observed IPPs", while TE §7.0 requires `test_phase_boundary.py` to fail if Phase 1 produces a satellite field. **D-17 governs the approved practical Phase 1 interpretation** — the contract enumerated from the audited five-column product (`ut1_unix`, `gdlat`, `glon`, `tec`, `dtec`), with `valid_satellite_count` recorded not-applicable in Phase 1 and nothing substituted — and `target-standardization` is defined against D-17 on that basis. The underlying source-text conflict has **not** been silently resolved, amended or adopted by inference; it is recorded at `requirements.md` § Known defects row 10. Any permanent reconciliation of §6.6 and TE §6.1 runs through Vision §15.2 change control. Recorded per governance finding `UG-02`.
- **`RES-02` — status: Deferred to authorized gate.** `team-practices.md` § Testing Posture still defines Phase 1's acceptance set as "WS-09 through WS-20". Approved requirement **FR-WS-4** additionally includes **WS-01 as a named exception** (WS-09–WS-20 countersigned 2026-08-16; the WS-01 exception approved 2026-08-21 under the recorded authority equivalence). **Current and downstream work follows the approved FR-WS-4 interpretation: WS-01 plus WS-09 through WS-20.** `team-practices.md` remains textually stale; correcting it is deferred to the next authorized practices-affirmation gate, `org.md` reserving that file for that gate, and it is **not** edited here or anywhere in this remediation. This discrepancy must **not** be read as an unapproved change to the accepted test set — the accepted set is FR-WS-4's. The separate "17 §12-tree modules" figure in the same file is a **second** stale figure, and it is now stale in a way it was not before: **BLK-01 closed 2026-08-22**, the amended TE §12 tree enumerates **21** test modules, and REQ-ENG-4 was re-derived to 21 from that tree. **Superseded text, preserved for the audit trail:** *"the amended TE §12 tree enumerates **19** test modules, and REQ-ENG-4 was re-derived to 19 from that tree. The 17-versus-19 question is therefore settled in the authority documents"* — written before the two later same-day amendments (`CR-2026-08-22-TARGET-SCHEMA-TEST`, `CR-2026-08-22-LEAKAGE-TA`) took the tree to 21. Corrected 2026-08-22 under `CR-2026-08-22-INC-CORRECTIONS` per `GOV-2026-08-22-INC-01` Rec 3. The 17-versus-**21** question is settled **in the authority documents**; what is not settled is `team-practices.md`, which is **untouched here and must stay untouched** — `org.md` reserves that file for the practices-affirmation gate. Both stale figures are carried on the same `RES-02` row. Recorded per governance finding `UG-06`; tracked as `RES-02` in § Residual governance obligations.
- **`RES-01` — status: Ownership remediated; dedicated test coverage open. This scenario is NOT TESTED.** No dedicated acceptance criterion verifies that a **permitted** December read — including the required pre-G-05 coverage and regime audit — writes its `locked_test_accessed = true` access-log row **before** the first December record is read. Adding `inventory-and-registry` to WS-18's and TA-18's Supporting column assigns evidence ownership and creates **no** test coverage; WS-18 and TA-18 as written test the execution guard against *unauthorized* pre-G-05 performance execution, a different scenario. The candidate criterion is routed to stage **3.2** through **Vision §15.2** change control and must distinguish permitted coverage-audit access from prohibited pre-G-05 performance execution. **No new acceptance criterion is created or approved in this stage** — the required §15.2 authority is not available here. UG-03's durable test gap is **not** closed. Tracked as `RES-01`.
- **`RES-03` — status: Derivation and §15.2 amendment COMPLETE 2026-08-22; per-item binding and implementation PENDING.** **Corrected 2026-08-22 under `CR-2026-08-22-INC-CORRECTIONS`, per `GOV-2026-08-22-INC-01` Rec 7: this bullet contradicted the § Residual governance obligations table row for the same item, which already recorded the derivation as complete.** The canonical protected set was derived item by item from TE §2.2 and TE §7.0B under an explicit deduplication rule and frozen as **D-24 — seventeen items, cardinality calculated rather than assumed**; FR-P1-06-1 was formally amended **14 → 17** through Vision §15.2 under `CR-2026-08-22-PROTECTED-SET`, and `requirements.md` FR-P1-06-1 now reads seventeen. **Superseded text, preserved for the audit trail:** *"FR-P1-06-1 still requires `protected_hashes.keys()` to equal a 'fourteen-item enumeration'"* and the instruction that no replacement cardinality may be assumed before the derivation — both correct when written, both discharged by D-24. What remains open is **not** the derivation: stage **3.1** must bind each of the seventeen items to concrete configuration fields (no config file exists yet), and `protected_hashes` / `diff_protected_hashes` are unwritten and unexecuted. The authority-derived content took precedence over preserving the unsupported count, as this bullet required. Tracked as `RES-03`; see **BLK-06**.
- **Open, a `requirements.md` change.** The advisory NOT-READY finding on FR-P1-05-18 (no criterion tests the storm-event count's source) and the **36** requirements with no §16/§19 row *(corrected 2026-08-23 from **40**, superseded 2026-08-22 by `CR-2026-08-22-LEAKAGE-TA`)*. Both are inputs to stages 3.1 and 3.2, not resolvable here.
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

## Review — 2026-08-23 re-entry pass

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-23T20:05:33Z
**Iteration:** 5 (advisory, single pass)
**Scope reviewed:** `unit-of-work.md`, `unit-of-work-dependency.md`, `unit-of-work-story-map.md` as rewritten under `units-generation-questions.md` Q8–Q12 (2026-08-23 re-entry, ADR-11 reconciliation), against the five `application-design` artifacts and `requirements.md`. Per dispatch, this pass does not reopen the decomposition, the DAG, or Q1–Q7, and does not evaluate build order or critical path — those remain out of scope for stage 2.7 and are stage 2.8's economic decisions.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `unit-of-work.md` line 310 (§7 `features-and-splits`, the unit's own `**Blockers.**` paragraph) | BLK-04's per-unit narrative still states the containment mechanism ADR-11 rejected as the *current, unweakened* safeguard — twice: "failure conditions (`LeakageError` when `train`'s index is not a subset of that partition)" as the Required-resolution text, and "The leakage safeguard is unchanged and is not weakened: per-fold train-only fitting … with a `LeakageError` when `train`'s index is not a subset of that partition." Neither instance is marked superseded, unlike the correctly rewritten § Blocker register entry (lines 623–643, which explicitly withdraws containment and preserves the old wording as a quoted, labelled supersession) and the story-map's BLK-04 row (line 310 of `unit-of-work-story-map.md`, struck through and corrected). A reader who consults only §7's own Blockers paragraph — the first place a `features-and-splits` implementer would look — receives the rejected mechanism as current fact. This is exactly the answer to the dispatch's question 3: the superseded containment rule does survive outside preserved-supersession text. | Rewrite §7's `**Blockers.**` paragraph to ADR-11's identity-check-with-one-exception mechanism, matching the register entry, or replace it with a cross-reference to § Blocker register rather than restating the mechanism a second time. |
| 2 | Major | `unit-of-work.md` § Unit definitions summary table (rows 7–12, lines 51–56) and every affected unit's own `**Blockers.**` paragraph (§§7–12, `features-and-splits` through `fixtures-and-reproducibility`) | BLK-08 and BLK-09 (registered 2026-08-23) were added to § Blocker register and to § Roll-up by unit, but never swept into the two other blocker representations the document itself maintains. The top summary table's Blockers column still reads `BLK-04` for row 7, `BLK-03, BLK-04 ↓` for rows 8/10/11, and `BLK-03 ↓, BLK-04 ↓` for row 9 — none mention BLK-08 or BLK-09 despite the Roll-up table (line 803–807) listing them for five of these six units. Most consequential: `evaluation-and-comparison`'s own `**Blockers.**` paragraph (line 375) says only "BLK-03 ↓, BLK-04 ↓ … Status: Open (inherited)" and never states that this unit *owns* BLK-08 — the blocker the register itself says "blocks a reported quantity, not an internal detail." This recreates, inside this stage's own artifact, precisely the failure mode `units-generation-questions.md` Q10's recommendation cites as the reason to register BLK-08/09 as blockers rather than `RES-` items: "a unit entering 3.1 would not see them in its own row." | Sweep BLK-08 and BLK-09 into the summary table's Blockers column and into each affected unit's `**Blockers.**` paragraph (§§7–12), matching what § Roll-up by unit already states. |
| 3 | Major | `unit-of-work.md` §12 `fixtures-and-reproducibility` (line 486, its `**Blockers.**` paragraph) and § Roll-up by unit (line 808) | `fixtures-and-reproducibility` inherits BLK-03 ↓ and BLK-04 ↓ by an explicitly stated rule: its `depends_on` includes the four units that own or inherit those blockers, and "the clean-run tolerance comparison and TA-21's traceability matrix consume their released artifacts, so what those contracts permit bounds what a clean run can be said to reproduce." `evaluation-and-comparison`, `statistical-inference` and `regimes-diagnostics-reporting` — all three named as sources of that inherited scope — now also carry BLK-08 (owned/inherited) and BLK-09 (inherited), and all three are direct dependencies of `fixtures-and-reproducibility`. The same stated rule therefore implies `fixtures-and-reproducibility` should inherit BLK-08 ↓ and BLK-09 ↓ too, but neither appears in its Blockers paragraph or in its Roll-up row (which still reads only "BLK-02 (implementation limb), BLK-03 ↓, BLK-04 ↓"). The document applies its own inheritance rule inconsistently between the two blocker pairs. | Either add BLK-08 ↓ and BLK-09 ↓ to `fixtures-and-reproducibility`'s Blockers paragraph and Roll-up row for consistency with the stated rule, or state explicitly why the clean-run artifact set is unaffected by these two (e.g., if TA-17/WS-20's tolerance comparison never touches a TECU-denominated or partition-range-dependent quantity) — silence reads as an oversight, not a reasoned exclusion. |
| 4 | Major | `unit-of-work.md` § Sources (line 9), § Assumptions & Open Questions (line 970), the §7 `features-and-splits` and §6 `external-products` "Requirements carried" lines (310, 271) and their "Bold = … (N of M here)" counts (306, 273), and the corresponding rows of the top summary table (lines 50–51) | `unit-of-work.md` was never swept for the 2026-08-22 `CR-2026-08-22-LEAKAGE-TA` change (TA-33–36), unlike `unit-of-work-story-map.md`, which was. Concretely: FR-P1-04-12, FR-P1-04-13 and FR-P1-04-16 are still bolded (marked "no §16/§19 test row") in `features-and-splits`'s Requirements-carried line though TA-33/34/35 now test them, and FR-P1-04-17 is still bolded in `external-products`'s line though TA-36 tests it — a set-difference against `unit-of-work-story-map.md`'s Table 1 (which shows all four with a plain, non-bold TA-3x row) names exactly these four IDs. Consequences, each independently reproduced: (a) `features-and-splits`'s stated "Bold … (4 of 11 here)" should read 1 of 11, and `external-products`'s "(5 of 7 here)" should read 4 of 7 — summing all twelve units' stated Bold counts as printed gives **40**, not the current, independently-confirmed **36** (`requirements.md` lines 842–856: "36 fully untested requirements … the total is now reproducible in one step"); correcting only these two units' counts (4→1, 5→4) closes the gap to exactly 36. (b) The same two units' "Acceptance rows" counts are stale in the same direction: `features-and-splits` states 9 (line 308) where the story-map's per-unit summary (line 234) lists 12 (adding TA-33/34/35), and `external-products` states 1 (line 275) where the story-map lists 2 (adding TA-36); the top summary table's rows 6–7 (lines 50–51) carry the same stale 1/9. This is a third occurrence of the "40 vs 36" stale-count class — distinct from the two the team already flagged as deliberately left unswept (`memory.md` § Deviations, 2026-08-23) because it is internal to `unit-of-work.md` itself (its own per-unit arithmetic reproduces its own stale total) rather than a cross-artifact disagreement, so it was not caught by that flag. | Un-bold FR-P1-04-12/13/16/17 in the two units' "Requirements carried" lines, correct both units' "Bold (N of M)" counts and "Acceptance rows (N)" counts and lists (adding TA-33/34/35 to `features-and-splits`, TA-36 to `external-products`), correct the top summary table's rows 6–7 accordingly, and correct "40" to "36" at § Sources line 9 and § Assumptions line 970. |
| 5 | Minor | `unit-of-work-dependency.md` § Independent unit sets ("`unit-of-work.md` § Blocker register carries BLK-01 through **BLK-07**") and `unit-of-work-story-map.md` § Open verification gaps intro ("Seven of these carry a blocker ID (BLK-01 through BLK-07)") | Both sentences still cap the blocker range at BLK-07, unswept after BLK-08/BLK-09 were registered 2026-08-23. The story-map's own defect table, two lines below its stale intro sentence, already carries rows for BLK-08 and BLK-09 (lines 312–313) — the sentence contradicts the table it introduces. | Update both to "BLK-01 through BLK-09" / "Nine of these carry a blocker ID (BLK-01 through BLK-09)". |
| 6 | Minor | `unit-of-work-dependency.md` § Edge table, row `models-and-baselines` (line 90: "Trains on the feature matrix and sequence tensor over the F1–F4 folds.") | A second, unacknowledged occurrence of the same ADR-11-superseded description the team already flagged and deliberately left open at § Integration points (line 166): ADR-11 replaced the "feature matrix + sequence tensor … F1–F4 folds" contract with `FeatureBundle`s and a six-member `Partition` list. `memory.md`'s 2026-08-23 deviation note names only the § Integration points occurrence; this Edge-table row carries the identical staleness one section earlier and was not named. | When the acknowledged staleness at § Integration points is fixed, sweep this Edge-table row in the same pass — the current deviation note undercounts its own scope by one location. |

### Validation Tool Results

No scripted validation tool is declared for this stage; every check below is a direct derivation against the artifact set and the named upstream contracts, run after the 2026-08-23 edits.

| Check | Method | Result |
|---|---|---|
| Requirement-row count | `grep -oE '^\| [A-Z][A-Za-z0-9-]+ \|' requirements.md`, filtered to `REQ-\|FR-\|NFR-` prefixes, deduplicated for the one ID (`REQ-CLAIM-01`) that also appears in a second, non-definitional crosswalk table | **105** distinct requirement rows — matches `unit-of-work.md` § Sources |
| Current untested-requirement count | `requirements.md` lines 842 and 856 state it directly ("36 fully untested requirements", "36 rows carry `UNTESTED`"); cross-checked against `unit-of-work-story-map.md`'s per-unit coverage summary, whose eleven per-unit "Untested requirements" figures sum to 36 | **36**, confirmed at the source and independently re-summed. `unit-of-work.md`'s own Sources/Assumptions lines and per-unit Bold counts still sum to 40 — see Finding 4 |
| Set-difference on the 4-ID gap (per `project.md`'s reconciliation rule: diff ID lists, never totals) | Compared `unit-of-work-story-map.md` Table 1's non-bold TA-3x rows against `unit-of-work.md`'s bolded IDs in the same units | Exactly `FR-P1-04-12`, `FR-P1-04-13`, `FR-P1-04-16` (`features-and-splits`) and `FR-P1-04-17` (`external-products`) — the four IDs `unit-of-work.md` still marks untested that are in fact tested by TA-33–36 |
| `### BLK-0…` heading count | `grep -c '^### BLK-0' unit-of-work.md` | **9** — reproduces the artifact's own printed derivation exactly |
| Open-blocker `\| Status \|` row count | `grep -c '^\| Status ' unit-of-work.md` | **8** — one per BLK-02…BLK-09, all beginning `Open`; reproduces the artifact's own printed derivation (9 total − 1 closed = 8 open) |
| Roll-up-by-unit row count | Counted `\| \`` rows in § Roll-up by unit | **11** — reproduces the artifact's own printed derivation |
| Edge-block structure | Parsed the fenced `yaml`: 12 units named exactly once, summed `depends_on` list lengths (0+1+2+1+1+1+3+1+2+1+1+9) | **23** edges, acyclic by strictly increasing layering, no self-dependency, every `kind: library` — byte-identical to the 2026-08-21 block; confirms the Q12=C handoff added no edge, matching the artifact's own claim |
| `features-and-splits` direct/transitive dependent count (§ Roll-up by unit closing paragraph) | Traced the edge block forward from `features-and-splits` | **2** direct (`models-and-baselines`, `fixtures-and-reproducibility`), **5** total direct-or-transitive (adding `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`) — matches the artifact's stated figures exactly |
| BLK-04 mechanism, register entry vs. per-unit prose | Compared § Blocker register (lines 623–643) against §7's `**Blockers.**` paragraph (line 310) | Register entry correctly rewritten to ADR-11's identity-check-plus-exception mechanism with superseded containment text explicitly quoted and labelled; §7's own paragraph still asserts the containment mechanism as current, unlabelled — **Finding 1** |
| BLK-08 / BLK-09 owner and downstream assignment against the DAG | Traced `evaluation-and-comparison`'s and `features-and-splits`'s forward reachability in the edge block | BLK-08's downstream (`statistical-inference`, `regimes-diagnostics-reporting`) and BLK-09's downstream (`models-and-baselines`, `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`) both match the actual forward-reachable set from their owning units; BLK-08's "blocks a reported quantity, not an internal detail" claim is accurate — `ABL-DIFF` and every TECU-denominated metric depend on the missing inverse path. Assignment is correct; propagation into other representations is not — **Findings 2–3** |
| Topology-only discipline | Searched all three artifacts for "critical path", "build order", "ship first", "start/begin with", "implement first" | No occurrence states one; every hit is the document's own disclaimer that it does *not* state one (e.g., the register-size closing paragraph's dependent-count observation is explicitly framed as "topology, not … a sequencing recommendation"). No trespass on stage 2.8 found. |
| Q8–Q12 fidelity | Compared `units-generation-questions.md` § RE-ENTRY 2026-08-23 answers and "What I will write" plan against the artifacts | Q8=A, Q9=A, Q11=A and Q12=C are all faithfully reflected in the register and story-map text produced. Q10=A (register BLK-08/BLK-09 as blockers, not `RES-` items) is faithfully reflected in § Blocker register itself, but the plan's own item list (items 1–9) never included sweeping the summary table or per-unit Blockers paragraphs, which is the proximate cause of Findings 2–3 |
| Known-stale-claims cross-check | Re-read `memory.md` § Deviations (2026-08-23) against the two named locations | Both confirmed present and unchanged exactly as described: `unit-of-work-dependency.md` § Integration points line 166 (stale `FeatureBundle`/`Partition` description) and `unit-of-work-story-map.md` line 315 (stale "40 requirements" in § Open verification gaps). No mis-statement found in how the dispatch described them. A third, unacknowledged occurrence of the first claim was found — Finding 6 |

### Summary

The register-level rewrite this pass set out to do — BLK-03/BLK-04's mechanism corrected to ADR-11, BLK-05's premise corrected, BLK-08/BLK-09 registered, the M10 fixture handoff recorded on an existing edge — is accurate and internally sound wherever it landed: the § Blocker register entries, § Roll-up by unit, and the story-map's defect-table rows all state the current mechanism correctly, and every count I could independently re-derive at the register/roll-up level (9 blockers, 8 open, 11 roll-up rows, 23 edges, 105 requirements, the 2/5 dependent count) reproduces the artifact's own printed derivations exactly. What did not happen is a full sweep of that same correction into the document's *other* representations of the same facts: the top-of-file Unit-definitions summary table and six units' own `**Blockers.**` paragraphs never received BLK-08/BLK-09, `features-and-splits` §7's own Blockers paragraph still states the containment mechanism ADR-11 withdrew as current fact, and a pre-existing (2026-08-22) staleness in the same two units' bold/acceptance-row counts — never caught by either this pass or the prior one — inflates `unit-of-work.md`'s own untested-requirement figure from the true 36 to 40, contradicting `requirements.md` and `unit-of-work-story-map.md`. None of this reopens the decomposition, the DAG, or Q1–Q12's rulings, and none of it names a build order or critical path — the topology and the blocker *content* are sound. What `delivery-planning` (2.8) is being handed is a topology it can trust (12 units, 23 edges, acyclic, one independent pair) with a blocker register whose substantive rulings are correct but whose surface is inconsistent across five representations of the same nine blockers in ways that would mislead a reader who consults a unit's own section rather than the register — exactly the failure mode this project's own register was designed to prevent.

## Review — 2026-08-23 propagation sweep

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-23T20:19:40Z
**Iteration:** 6 (advisory, single pass)
**Scope reviewed:** `unit-of-work.md`, `unit-of-work-dependency.md`, `unit-of-work-story-map.md` after the 2026-08-23 propagation sweep dispatched to fix the six-Major/Minor finding set from the 2026-08-23 re-entry pass (`## Review — 2026-08-23 re-entry pass` above). Per dispatch, this pass checks completeness of that sweep by representation, not by entity, and does not reopen the decomposition, the DAG, Q1–Q12's rulings, or stage 2.8's build-order/critical-path territory.

This is an advisory pass: the verdict below is decision support for the human at the approval gate, not a gate itself. The human owner's ruling was "fix all of it, then approve" — the findings below are what a by-representation sweep still finds outstanding against that instruction, for the human to weigh before approving.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `unit-of-work.md` §7 `features-and-splits` (line 304, "Requirements carried") and (line 306, "Bold … (4 of 11 here)"); §7 "Acceptance rows (9)" (line 308); §6 `external-products` (line 271, "Requirements carried") and (line 273, "Bold … (5 of 7 here)"); §6 "Acceptance rows (1)" (line 275); § Unit definitions summary table rows 6–7 (lines 50–51, "Acceptance rows" column) | The 2026-08-23 sweep corrected the two headline occurrences of the untested-requirement count (§ Sources line 9, § Assumptions & Open Questions) from 40 to 36, but did not correct the per-unit representations that produce that total. `features-and-splits`'s "Requirements carried" line still bolds `FR-P1-04-12`, `FR-P1-04-13` and `FR-P1-04-16` as having no §16/§19 test row, and states "(4 of 11 here)"; `external-products` still bolds `FR-P1-04-17` and states "(5 of 7 here)". `requirements.md` (the authoritative source, lines 382–388, 842, 856) confirms all four now carry `TA-33`…`TA-36` and are not `UNTESTED`, and `unit-of-work-story-map.md`'s own per-unit summary (line 234: `features-and-splits` untested = 1, including TA-33/34/35 in its acceptance-row list; line 233: `external-products` untested = 4, including TA-36) was correctly swept. Re-summing all twelve units' printed Bold counts in `unit-of-work.md` as they stand today (2+1+7+2+1+**5**+**4**+7+2+0+7+2) gives **40**, not 36 — the document's own headline correction is directly contradicted by its own per-unit arithmetic, one section away. The same two units' "Acceptance rows (N)" counts (9 and 1) are stale in the same direction and by the same omission — they should be 12 and 2, per the story-map's per-unit list, and the top summary table's rows 6–7 carry the identical stale 1 and 9. This is the same finding class the re-entry pass raised as its own Finding 4, only half-remediated: the sweep fixed the two sentences the finding's Recommendation named last ("correct '40' to '36' at § Sources line 9 and § Assumptions line 970") without the four corrections the same Recommendation named first (un-bold the four IDs; correct both units' Bold and Acceptance-rows counts and lists; correct the summary-table cells). | Un-bold `FR-P1-04-12`, `FR-P1-04-13`, `FR-P1-04-16` in `features-and-splits`'s "Requirements carried" line and `FR-P1-04-17` in `external-products`'s; correct "Bold … (4 of 11 here)" → "(1 of 11 here)" and "(5 of 7 here)" → "(4 of 7 here)"; add `TA-33, TA-34, TA-35` to `features-and-splits`'s Acceptance-rows list (9→12) and `TA-36` to `external-products`'s (1→2); correct the top summary table's Acceptance-rows cells for rows 6 and 7 to 2 and 12. |
| 2 | Minor | `unit-of-work-dependency.md` § Independent unit sets (line 261, "`unit-of-work.md` § Blocker register carries BLK-01 through **BLK-07**") and `unit-of-work-story-map.md` § Open verification gaps intro (line 297, "Seven of these carry a blocker ID (BLK-01 through BLK-07)") | Both sentences still cap the blocker range at BLK-07. This is the re-entry pass's own Finding 5, unaddressed by the sweep: neither location is on the sweep's nine-item scope list, and both remain byte-identical to the prior pass. The story-map's own defect table two lines below its stale intro sentence still carries the BLK-08 and BLK-09 rows (lines 312–313) that the sentence fails to count, and the dependency file's own next sentence (line 262, "Ten of the twelve units carry a blocker row") is consistent with BLK-07 through BLK-09 all being counted, so the "BLK-01 through BLK-07" span contradicts its own paragraph, not only the register. | Update both to "BLK-01 through BLK-09" / "Nine of these carry a blocker ID (BLK-01 through BLK-09)". |
| 3 | Minor | `unit-of-work-dependency.md` § Edge table, row `models-and-baselines` (line 90: "Trains on the feature matrix and sequence tensor over the F1–F4 folds.") | This is the re-entry pass's own Finding 6, unaddressed by the sweep. § Integration points (lines 166, 173–181) was correctly rewritten to `FeatureBundle`s and the six-member `Partition` list with a marked correction box, but the Edge-table row one section earlier, describing the identical `features-and-splits` → `models-and-baselines` contract in the same superseded "feature matrix and sequence tensor … F1–F4 folds" language, was not swept in the same pass. | When the Edge-table row is next touched, correct it to match § Integration points's corrected description, and note in the correction box (or a cross-reference) that both locations described the same superseded contract. |

### Validation Tool Results

No scripted validation tool is declared for this stage; every check below is a direct derivation against the artifact set and the named upstream contracts, run against the text as it stands after the 2026-08-23 propagation sweep.

| Check | Method | Result |
|---|---|---|
| BLK-04 mechanism, §7 own paragraph vs. register | Read `unit-of-work.md` §7 `features-and-splits` "**Blockers.**" paragraph (lines 310–324) and compared to § Blocker register's BLK-04 entry (lines 647–667) | **Fixed.** §7's own paragraph now states ADR-11's identity-check-with-one-exception mechanism verbatim, matching the register, and carries the "⚠ MECHANISM CORRECTED HERE 2026-08-23" box quoting and labelling the superseded containment text. Re-entry Finding 1 is resolved. |
| BLK-08 / BLK-09 sweep into summary table and per-unit paragraphs | Read § Unit definitions rows 7–12 (lines 51–56) and each of §§8–12's own "**Blockers.**" paragraphs (lines 360, 393–397, 427, 457, 508) | **Fixed.** The summary table's Blockers column carries BLK-08/BLK-09 (marked owned or ↓ as appropriate) for all six affected units, and every affected unit's own paragraph states its BLK-08 and/or BLK-09 status explicitly — `evaluation-and-comparison`'s paragraph (line 393) now opens "**BLK-08** (owned), **BLK-03 ↓**, **BLK-04 ↓**, **BLK-09 ↓**" and states the reported-quantity consequence. Re-entry Finding 2 is resolved. |
| `fixtures-and-reproducibility` inheriting BLK-08 ↓ / BLK-09 ↓ by the stated rule | Read §12's "**Blockers.**" paragraph (line 508) and § Roll-up by unit's `fixtures-and-reproducibility` row (line 832) | **Fixed.** Both now carry BLK-08 ↓ and BLK-09 ↓, with an explicit sentence naming the mechanism: "BLK-08 ↓ and BLK-09 ↓ were added 2026-08-23 by the same stated rule that already brought BLK-03 and BLK-04 here … the omission was a partial sweep, not a judgement that the rule stops short," and a concrete consequence (a TECU-denominated tolerance comparison cannot be checked against output no design path returns to TECU). Re-entry Finding 3 is resolved. |
| Untested-requirement count, headline vs. per-unit sum | `requirements.md` lines 842/856 state 36 directly, confirmed by grep (`` `UNTESTED` `` count = 52 total table cells containing the token across all sections, with the dedicated "Requirements with no testing row" enumeration giving 36); `unit-of-work-story-map.md` line 241–247 states 36, re-derived from its own per-unit table; `unit-of-work.md` § Sources (line 9) and § Assumptions (line 994) state 36 | **Headline occurrences fixed; per-unit occurrences not.** Summing `unit-of-work.md`'s own twelve per-unit "Bold = … (N of M)" counts as printed today: 2+1+7+2+1+5+4+7+2+0+7+2 = **40**. The 4-ID set difference (`FR-P1-04-12`, `FR-P1-04-13`, `FR-P1-04-16`, `FR-P1-04-17`) between this sum and the confirmed-correct 36 exactly matches the four IDs `requirements.md` shows now carrying `TA-33`…`TA-36`. Finding 1. |
| Live survival of "40" as a bare numeral or of the superseded containment rule, outside preserved-supersession boxes and prior `## Review` sections | Searched both artifacts for "40" outside `## Review —` sections and outside text explicitly marked "superseded"/"preserved for the audit trail"/quoted-and-labelled; searched for "subset of that partition", "containment" outside labelled supersession boxes | No bare, unlabelled "40" survives as a *live claim* — the only live occurrences are inside the corrected Sources/Assumptions sentences narrating the 40→36 correction itself, and inside prior `## Review` sections (legitimate, per the dispatch's own carve-out). The containment mechanism does not survive live anywhere; every occurrence outside the two marked supersession boxes (§7's box, BLK-04's register box) states ADR-11's identity-check mechanism. **However**, the per-unit Bold/Acceptance-rows counts described above are a *derived* representation, not a textual restatement of "40" — they reproduce 40 by arithmetic rather than asserting it, which is why a text search for the literal does not catch Finding 1. |
| Fenced `yaml` edge block | Re-parsed: 12 units named exactly once; summed `depends_on` list lengths (0+1+2+1+1+1+3+1+2+1+1+9) | **23** edges, byte-identical to both prior passes; acyclic by strictly increasing layering; no self-dependency; every `kind: library`. Unchanged by this sweep, as the dispatch's scope (a documentation-only propagation) implies it should be. |
| `### BLK-0…` heading count / open-`Status` row count / roll-up row count | `grep -c '^### BLK-0' unit-of-work.md`; `grep -nF '\| Status \|' unit-of-work.md \| grep -i open` restricted to the register section; `grep -cF '\| \`' ` over § Roll-up by unit's line range | **9** headings; **8** open-status rows (BLK-02…BLK-09); **11** roll-up rows — all three reproduce the artifact's own printed derivations exactly and are unchanged from the re-entry pass, confirming the register itself was untouched by this sweep (as it should be — the sweep's scope was propagation into other representations, not register content). |
| Topology-only discipline on everything added or edited in this sweep | Read every changed passage (the two correction boxes, the six Blockers paragraphs, the summary table, the two Sources/Assumptions sentences, § Integration points's corrected row) for "critical path", "build order", "ship first", "start with", "before … in the schedule" | No trespass found. `fixtures-and-reproducibility`'s new sentence about BLK-08/BLK-09 states a *scope* consequence (what a tolerance comparison can be said to reproduce), not a *sequencing* one, and every other addition is either a mechanism correction or a count correction. Stage 2.8's territory is intact. |
| BLK-08 reaching `statistical-inference` and `regimes-diagnostics-reporting`; BLK-09 reaching `models-and-baselines`, `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting` | Traced forward reachability from `evaluation-and-comparison` (BLK-08's owner) and `features-and-splits` (BLK-09's owner) in the fenced edge block | Matches exactly in both cases, and matches what each unit's own paragraph now states. The reported-quantity claim (BLK-08: paired loss differential, bootstrap interval, practical-relevance threshold are all TECU-denominated) is accurate against `project.md` § Mandated's `ABL-DIFF` rule and against `component-methods.md`'s `Transform.inverse` signature as quoted in the register. |
| Dependency-file and story-map "BLK-01 through BLK-07" residue, and Edge-table residue | Byte-compared the two sentences and the Edge-table row against the re-entry pass's Findings 5 and 6 | Both unchanged since the re-entry pass — confirmed still present, still stale, still outside the sweep's nine-item scope. |

### Summary

The sweep did what its own nine-item scope described, and did it correctly: BLK-04's mechanism now agrees between the register and `features-and-splits`'s own paragraph (re-entry Finding 1, fixed); BLK-08 and BLK-09 now appear in the summary table and in all six affected units' own `**Blockers.**` paragraphs, including `evaluation-and-comparison`'s ownership statement and `fixtures-and-reproducibility`'s explicit same-rule inheritance (re-entry Findings 2–3, fixed); the two headline occurrences of the untested-requirement count now read 36 (part of re-entry Finding 4); the story-map's defect-table row and the dependency file's § Integration points row were corrected (sweep items 8–9). What the sweep did not do is finish re-entry Finding 4's own scope: the per-unit Bold markers, Bold counts, and Acceptance-rows counts for `features-and-splits` and `external-products` — and the top summary table's Acceptance-rows cells for those same two rows — still carry the pre-`CR-2026-08-22-LEAKAGE-TA` figures, so `unit-of-work.md`'s own per-unit arithmetic still sums to 40 even though its own headline sentences now say 36. That is a new instance of exactly the defect class this whole sweep exists to close — a corrected fact (36) surviving next to an unswept representation of the superseded one (40), just relocated from the register/summary-table axis (closed by this sweep) to the requirements-carried/acceptance-rows axis (not on this sweep's list). Two Minor findings from the re-entry pass (the "BLK-01 through BLK-07" span in two files, and the Edge-table's stale contract description) were also not on the sweep's scope list and remain exactly as they were. None of this reopens the decomposition, the DAG, or Q1–Q12; no build order or critical path was introduced. What `delivery-planning` (2.8) is being handed is the same trustworthy topology as before (12 units, 23 edges, acyclic, one independent pair) and a blocker register whose content is now fully and correctly propagated across every representation the prior pass checked — but `unit-of-work.md` still privately disagrees with itself on the untested-requirement count by four IDs, in a place a reader would only find by re-deriving the sum rather than reading the headline sentence.

## Review — 2026-08-23 summand sweep

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-23T20:31:33Z
**Iteration:** 7 (advisory, single pass)
**Scope reviewed:** `unit-of-work.md`, `unit-of-work-dependency.md`, `unit-of-work-story-map.md` after the final corrective sweep dispatched to close the one Major and two Minor findings standing at the end of `## Review — 2026-08-23 propagation sweep` (above), per the human owner's ruling "fix the Major and both Minors." Per dispatch, every count below is derived programmatically from the artifact text and the method is recorded, not read off adjacent prose. This pass does not reopen the decomposition, the DAG, Q1–Q12's rulings, or stage 2.8's build-order/critical-path territory, and is decision support for the human at the gate, not a gate itself.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `unit-of-work.md` § Unit definitions summary table, "Acceptance rows" column, row 6 `external-products` (line 50, value `1`) and row 7 `features-and-splits` (line 51, value `9`) | The final sweep corrected both units' own per-unit "Acceptance rows (N)" lines (§6 now states `(2)`: WS-09, `TA-36`; §7 now states `(12)`: WS-10…WS-18 plus `TA-33`, `TA-34`, `TA-35` — both counted directly from their listed rows and both correct) and corrected both units' "Requirements carried"/"Bold" lines and counts (§6: `FR-P1-04-17` un-bolded, "Bold … (**4** of 7 here)"; §7: `FR-P1-04-12`/`-13`/`-16` un-bolded, "Bold … (**1** of 11 here)" — both independently re-derived below and both correct). The one cell this dispatch's own Recommendation named ("correct the top summary table's Acceptance-rows cells for rows 6 and 7 to 2 and 12") was not carried out: the summary table at the top of the file still prints `1` for `external-products` and `9` for `features-and-splits`, one section away from the per-unit sections it summarizes and now disagrees with. This is the same defect class flagged in the two prior passes — a corrected fact surviving next to an unswept representation of the superseded one — relocated one representation further down the same finding's own scope list. | Update the summary table's Acceptance-rows column: row 6 (`external-products`) `1` → `2`; row 7 (`features-and-splits`) `9` → `12`. |

### Validation Tool Results

No scripted validation tool is declared for this stage; every check below is a direct, reproducible derivation against the artifact text as it stands after the final corrective sweep, with its method stated.

| Check | Method | Result |
|---|---|---|
| Sum of the twelve units' printed "Bold = … (N of M)" counts | `grep -n "^Bold = " unit-of-work.md`, read the printed N from each of the 12 matches, summed: 2+1+7+2+1+4+1+7+2+0+7+2 | **36** — agrees with the document's own headline (§ Sources line 9, § Assumptions line 994: "36 with no §16/§19 test row"). This is a full fix of the propagation-sweep pass's Finding 1 on the Bold-count axis: `external-products` now prints 4 (was 5), `features-and-splits` now prints 1 (was 4). |
| Independent count of literal bold requirement IDs across the twelve "Requirements carried" lines | `grep "^\*\*Requirements carried" unit-of-work.md`, stripped the leading `**Requirements carried (N).**` label, counted `**ID**`-shaped bold tokens in the remaining text per line with a script (not read from the printed "(N of M)" label), summed the 12 per-line counts: 2+1+7+2+1+4+1+7+2+0+7+2 | **36** — agrees with both the printed Bold-count sum and the document's headline. All three figures (headline 36, summed printed Bold counts 36, independently counted literal bold IDs 36) now agree exactly; this closes the "40 vs 36" discrepancy the prior two passes tracked on the Bold/headline axis. |
| `requirements.md` cross-check: does `FR-P1-04-12`/`-13`/`-16`/`-17` carry `TA-33`/`TA-34`/`TA-35`/`TA-36` respectively, in that order, with status `Pending`, and is `FR-P1-04-10` still correctly untested | Read `requirements.md` lines 380, 382, 383, 387, 388 directly | Confirmed exactly: FR-P1-04-12→**TA-33**, FR-P1-04-13→**TA-34**, FR-P1-04-16→**TA-35**, FR-P1-04-17→**TA-36**, each row's rightmost cell stating "Status `Pending`: the row exists, no test module is implemented, none has been executed, and none has passed" (or the equivalent wording) — matching `unit-of-work.md`'s own `(Pending — the row exists; no test is implemented, executed or passing)` gloss. `FR-P1-04-10` (line 380) carries no TA/WS row and remains `UNTESTED` in `requirements.md`, matching `unit-of-work.md` §7's sole remaining bold ID. |
| `features-and-splits` and `external-products` "Acceptance rows (N)" counts, counted from each unit's own listed rows | Counted the comma-separated tokens in each unit's own "**Acceptance rows (N).**" line: §6 `WS-09, TA-36` = 2 tokens; §7 `WS-10, WS-11, WS-12, WS-13, WS-18, TA-07, TA-08, TA-11, TA-18, TA-33, TA-34, TA-35` = 12 tokens | **2** and **12** — both match the printed `(N)` labels in the two units' own sections exactly. Both per-unit counts are correct; only the top summary table's mirror of these two cells (Finding 1) was not updated to match. |
| Live survival of a bare "40" untested-count claim, a "BLK-01 through BLK-07" span, or the superseded `feature matrix / F1–F4 folds` contract description, outside preserved-supersession text and prior `## Review` sections | `grep -n "\b40\b"` across all three artifacts, then classified every hit by hand; `grep -n "BLK-01 through"` across all three; `grep -n "feature matrix and sequence tensor\|F1–F4 folds\|FeatureBundle"` in `unit-of-work-dependency.md` | No surviving live claim of any of the three. Every "40" hit outside a `## Review —` section is inside a "corrected 2026-08-23 from 40" / "40 → 36" narration sentence (legitimate supersession text) or an unrelated numeral (station-cell IDs "ARUC 40/44"). `unit-of-work-dependency.md` line 261 and `unit-of-work-story-map.md` line 297 both now read "BLK-01 through **BLK-09**" — the propagation sweep's Minor #2 is fixed in both files. `unit-of-work-dependency.md`'s Edge-table row 90 now reads "`FeatureBundle`s … the six-member `Partition` list", with a correction note matching § Integration points' box — the propagation sweep's Minor #3 is fixed. |
| Summary table's Acceptance-rows cells for rows 6 and 7, versus the per-unit sections they summarize | Read `unit-of-work.md` lines 43–51 (the full summary table) directly | Row 6 (`external-products`) states Acceptance rows `1`; row 7 (`features-and-splits`) states `9`. Both disagree with the per-unit sections' own counted values of `2` and `12` (above) and with the story-map's per-unit list. **This is Finding 1** — the summary table was not swept. |
| Fenced `yaml` edge block: parses, 12 units named once, acyclic, edge count | Re-parsed the block in `unit-of-work-dependency.md`; summed `depends_on` list lengths: 0+1+2+1+1+1+3+1+2+1+1+9 | **23** edges over 12 uniquely-named units, byte-identical to every prior pass; strictly-increasing dependency layering confirms acyclicity; no self-dependency; every `kind: library`. Unchanged, as expected of a documentation-only sweep. |
| Topology-only discipline over everything in this sweep's actual scope (the two Minor fixes and the unchanged per-unit sections) | Searched the fixed passages (dependency-file and story-map "BLK-01 through BLK-09" sentences, the Edge-table row and its correction note) for "critical path", "build order", "ship first", "start/begin with", "implement first" | No occurrence states one; the fixed text is a count correction and a contract-description correction, nothing sequencing-shaped. No trespass on stage 2.8's territory. |

### Summary

Of the three items this final sweep was dispatched to close, two are fully and correctly fixed: both Minor findings (the "BLK-01 through BLK-07" span, corrected to BLK-09 in both `unit-of-work-dependency.md` and `unit-of-work-story-map.md`; and the Edge-table's stale `feature matrix / F1–F4 folds` description, corrected to `FeatureBundle`s over the six-member `Partition` list) are resolved, verified by direct re-read against the artifact text. The Major finding is resolved on every axis that determines the headline count itself: `features-and-splits` and `external-products` had their bolded requirement IDs, Bold counts, and per-unit Acceptance-rows counts and lists all corrected, and three independent derivations — the summed printed Bold counts, an independent count of literal bold IDs from the raw text, and the document's own headline sentences — now agree exactly at 36, matching `requirements.md`'s authoritative figure and closing the "40 vs 36" discrepancy this document has carried, in one representation or another, across three consecutive review passes. What survives is a narrower slice of the same Major finding's own Recommendation: the top-of-file Unit-definitions summary table's Acceptance-rows cells for these same two units (rows 6 and 7) still print the pre-correction figures `1` and `9` rather than the now-correct `2` and `12`, one section above the per-unit text it is meant to mirror. This is a one-line, mechanical correction, not a reopening of any content, count methodology, or scientific judgment — but it is the fourth time in this document's revision history that a corrected fact has been left standing next to an unswept mirror of the superseded one, and `project.md`'s own learning from this exact defect class is to sweep every representation, not every instance of the entity carrying it. What `delivery-planning` (2.8) is being handed is a topology unchanged and still trustworthy (12 units, 23 edges, acyclic, one independent pair), a blocker register whose content is fully and consistently propagated across every representation checked across all three passes, and an untested-requirement count that is correct and self-consistent everywhere except two cells in one summary table — a single remaining edit, precisely located, away from full internal consistency.

## Review — 2026-08-23 mirror re-derivation

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-23T20:38:19Z
**Iteration:** 8 (advisory, single pass)
**Scope reviewed:** the two-cell correction to `unit-of-work.md` § Unit definitions summary table (row 6 `external-products` Acceptance-rows `1`→`2`, row 7 `features-and-splits` Acceptance-rows `9`→`12`) and its accompanying marked note (lines 58–70), against the human owner's instruction to re-derive every acceptance-row figure across both representations, not only the two named. Per dispatch, this is decision support for the human at the gate, not a gate itself, and does not reopen the decomposition, the DAG, Q1–Q12's rulings, or stage 2.8's build-order/critical-path territory.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `unit-of-work-dependency.md` § Independent unit sets, line 274–275 (`"BLK-01 is closed" … "BLK-02 through BLK-07 are open."`) | This sentence was not swept when BLK-08 and BLK-09 were registered 2026-08-23. It sits four lines below the sentence this document's own prior-pass fix corrected ("BLK-01 through **BLK-09**", line 260–261, with a dated correction note), in the same paragraph, describing the same register — and it still states the pre-registration span. The register in fact carries eight open blockers (BLK-02 through BLK-09; BLK-01 closed), not six. This is the same defect class the human owner is asking this pass to close: a corrected fact (the nine-blocker, BLK-09 span, fixed two sentences earlier in this exact paragraph) standing next to an unswept mirror of the superseded one (the six-blocker "through BLK-07" span), one paragraph away from its own fix. | Change "BLK-02 through BLK-07 are open" to "BLK-02 through BLK-09 are open" (eight open blockers). |
| 2 | Major | `unit-of-work-story-map.md` § Cross-unit responsibilities, line 323 (the `RES-01` row: `"the 40-row untested count is unchanged: FR-P1-02-3 keeps its existing WS-18, TA-25 test row and does not move into the untested list"`) | This row states the untested-requirement count as a live present-tense fact ("is unchanged") using the superseded figure 40, in the same file whose own § Per-unit coverage summary (lines 241–248) and § Open verification gaps (line 318, explicitly marked "corrected 2026-08-23 from 40") both now state 36. The claim itself (FR-P1-02-3 keeps its `WS-18, TA-25` row and is not among the untested) is still true, but the numeral it is anchored to is the pre-`CR-2026-08-22-LEAKAGE-TA` total and was never updated when the rest of this document's untested-count representations were. This is the same "status claim carrying a stale numeral" pattern `project.md`'s own recorded learning names, occurring in the one artifact of the three where the two prior review passes did not look (their scope was the top-of-file summary table and the per-unit Requirements-carried/Acceptance-rows lines in `unit-of-work.md`). | Change "the 40-row untested count is unchanged" to "the 36-row untested count is unchanged" (or drop the numeral and cite the current count by reference to § Per-unit coverage summary, which will not go stale again on the next such change). |

### Validation Tool Results

No scripted validation tool is declared for this stage; every check below is a direct, reproducible derivation against the artifact text as it stands after the two-cell correction, with its method stated.

| Check | Method | Result |
|---|---|---|
| Summary-table Acceptance-rows cells for rows 6–7 | Read `unit-of-work.md` lines 50–51 directly | Row 6 (`external-products`) now reads `**2**`; row 7 (`features-and-splits`) now reads `**12**`. Both corrected as instructed. |
| Full re-derivation of the Acceptance-rows column, top to bottom, from each unit's own `**Acceptance rows (N).**` line | Read all twelve per-unit lines in document order: foundation (7), governance-guards (2), acquisition (1), inventory-and-registry (3), target-standardization (1), external-products (2), features-and-splits (12), models-and-baselines (5), evaluation-and-comparison (1), statistical-inference (2), regimes-diagnostics-reporting (3), fixtures-and-reproducibility (4) | Series: **7, 2, 1, 3, 1, 2, 12, 5, 1, 2, 3, 4** — matches the summary table's Acceptance-rows column top to bottom exactly, and matches the note's own claimed derivation verbatim. |
| Full re-derivation of the Requirements column, top to bottom, from each unit's own `**Requirements carried (N).**` line | Read all twelve per-unit lines in document order: 16, 10, 15, 7, 6, 7, 11, 9, 4, 1, 11, 8 | Series: **16, 10, 15, 7, 6, 7, 11, 9, 4, 1, 11, 8** — matches the summary table's Requirements column top to bottom exactly, and matches the note's own claimed derivation. Both columns of the table now agree with the sections they summarize, throughout, not only in the two named rows. |
| `external-products` and `features-and-splits` Acceptance-rows token counts, counted from each unit's own listed IDs | `external-products`: `WS-09, TA-36` = 2 tokens. `features-and-splits`: `WS-10, WS-11, WS-12, WS-13, WS-18, TA-07, TA-08, TA-11, TA-18, TA-33, TA-34, TA-35` = 12 tokens | **2** and **12** — both match the corrected summary-table cells and the units' own printed `(N)` labels. |
| `2` and `12` cross-checked against `requirements.md`'s TA-33–TA-36 assignments and status | Read `requirements.md` lines 382–388 directly | `FR-P1-04-12`→**TA-33**, `FR-P1-04-13`→**TA-34**, `FR-P1-04-16`→**TA-35** (all three `features-and-splits`, status `Pending`), `FR-P1-04-17`→**TA-36** (`external-products`, status `Pending`). All four IDs and their unit assignments in `unit-of-work.md` §6/§7 match `requirements.md` exactly; `FR-P1-04-10` (the one requirement `features-and-splits` still bolds as untested) carries no TA/WS row in `requirements.md` and is correctly the sole remaining untested ID there. |
| Untested-requirement count (36) — sweep across all three artifacts for a live, unlabelled "40" | `grep -n "\b40\b"` over `unit-of-work.md`, `unit-of-work-dependency.md`, `unit-of-work-story-map.md`, then classified every hit by hand | `unit-of-work.md` and `unit-of-work-dependency.md`: every hit is either inside a `## Review —` section (legitimate per dispatch's carve-out), an explicitly labelled "corrected … from 40" / "40 → 36" narration sentence, or an unrelated numeral (`ARUC 40/44`). `unit-of-work-story-map.md`: same, **except line 323** (the `RES-01` cross-unit-responsibilities row), which states "the 40-row untested count is unchanged" as a live, unlabelled present-tense claim — **Finding 2**. |
| Blocker span "BLK-01 through BLK-0N" and "BLK-0X through BLK-0Y are open" — sweep across all three artifacts | `grep -n "BLK-01 through\|blocker ID (BLK\|through BLK-07\|BLK-02 through"` over all three files | `unit-of-work.md` line 854 and `unit-of-work-story-map.md` line 297 both correctly state "BLK-01 through BLK-09" / nine total. `unit-of-work-dependency.md` line 260–261 also correctly states "BLK-01 through **BLK-09**" with a dated correction note — **but** the same file's line 274–275, four lines later in the same paragraph, still reads "BLK-02 through BLK-07 are open," never swept to BLK-09 — **Finding 1**. |
| ADR-11 mechanism (identity check, not containment) — sweep for a live, unlabelled containment claim | `grep -n "subset of that partition\|containment"` over all three artifacts under review (excluding `units-generation-questions.md`, out of scope) | No live, unlabelled containment claim survives. The one remaining hit outside `unit-of-work.md`'s labelled correction box (lines 328–333) is `unit-of-work-story-map.md` line 313, which is itself struck through (`~~…~~`) and explicitly marked "mechanism replaced 2026-08-23 by ADR-11" — a legitimate preserved-supersession form, not a live claim. |
| `FeatureBundle` / `Partition` contract — sweep for a live "feature matrix and sequence tensor … F1–F4 folds" claim | `grep -n "feature matrix and sequence tensor\|FeatureBundle"` over `unit-of-work-dependency.md` | No live stale claim. The Edge-table row (line 90) and § Integration points (line 166, 176) both state the corrected `FeatureBundle`/six-member `Partition` contract, with the Edge-table row carrying its own dated correction note cross-referencing § Integration points. |
| Fenced `yaml` edge block | Re-parsed `unit-of-work-dependency.md` lines 100–138: 12 units named exactly once, summed `depends_on` list lengths (0+1+2+1+1+1+3+1+2+1+1+9) | **23** edges over 12 uniquely-named units, byte-identical to every prior pass; strictly increasing dependency layering confirms acyclicity; no self-dependency; every `kind: library`. Unchanged, as expected of a two-cell correction. |
| Topology-only discipline over the corrected text and the note itself | Searched the corrected table row, the marked note (lines 58–70), and both newly-flagged passages for "critical path", "build order", "ship first", "start/begin with", "implement first" | No occurrence states one. The note is a count-correction narration; Findings 1–2 are stale-numeral/stale-span corrections, not sequencing statements. No trespass on stage 2.8's territory. |

### Summary

The two-cell correction the human owner ordered is done and correct: the summary table's Acceptance-rows cells for `external-products` (1→2) and `features-and-splits` (9→12) now read 2 and 12, and — per the owner's instruction to re-derive every cell rather than only the two named — an independent, full top-to-bottom re-derivation of both the Acceptance-rows and Requirements columns from all twelve per-unit sections reproduces the summary table exactly, with no other cell in either column found stale. The four TA-33–TA-36 assignments driving this correction were independently cross-checked against `requirements.md` and are correct. Extending the sweep beyond the two named cells, as the owner's instruction and this project's own recorded learning about sweeping every representation of a corrected fact both require, surfaced two further live mirrors that neither of the two prior review passes checked because their scope was `unit-of-work.md`'s own summary table and per-unit lines: `unit-of-work-dependency.md` line 274–275 still caps the open-blocker span at "BLK-07" four lines below its own correctly-fixed "BLK-09" sentence in the same paragraph, and `unit-of-work-story-map.md` line 323 still asserts "the 40-row untested count is unchanged" as a live present-tense fact. Both are one-line, mechanical corrections with no bearing on the topology, the blocker content, or any scientific judgment — the DAG (12 units, 23 edges, acyclic, one independent pair), the blocker register's substantive content, and the ADR-11/`FeatureBundle` mechanism descriptions are all confirmed sound and consistent everywhere checked. What `delivery-planning` (2.8) would be handed today is a trustworthy DAG and a blocker register whose content is correct throughout, with two remaining stale-numeral mirrors — precisely located, outside the two artifacts the last two passes already exhausted — for the human to weigh at the gate.

## Review — 2026-08-23 full mirror audit

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent (advisory)
**Date:** 2026-08-23T20:48:10Z
**Iteration:** 6 (full mirror audit, per the human owner's ruling after five consecutive advisory passes each found one more instance of the same defect class)
**Scope reviewed:** `unit-of-work.md`, `unit-of-work-dependency.md`, `unit-of-work-story-map.md` in full, including all prior `## Review` sections (read, not re-litigated) and `memory.md`'s diary entries; upstream `../requirements-analysis/requirements.md` and the five `../application-design/` artifacts read read-only for cross-reference. Every fact named in the dispatch was re-derived independently from the artifact text rather than accepted from the two ordered fixes or from the prior passes' own printed derivations.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `unit-of-work.md` § Roll-up by unit, `fixtures-and-reproducibility` row | The row reads "BLK-02 (implementation limb), BLK-03 ↓, BLK-04 ↓" — it omits BLK-08 ↓ and BLK-09 ↓. Three other representations of this unit's blocker exposure all carry both: the § Unit definitions summary table row 12 ("BLK-02, BLK-03 ↓, BLK-04 ↓, BLK-08 ↓, BLK-09 ↓"), the unit's own `**Blockers.**` paragraph (which states explicitly that "BLK-08 ↓ and BLK-09 ↓ were added 2026-08-23 by the same stated rule that already brought BLK-03 and BLK-04 here… the omission was a partial sweep"), and both blockers' own register entries, which name `fixtures-and-reproducibility` as a consumer. This is exactly the defect class the human owner ordered this pass to hunt: a fact corrected in three places and left stale in a fourth — the roll-up table, one of the two places a stage-3.1 reader is most likely to consult for a unit's blocker exposure. | Add ", BLK-08 ↓, BLK-09 ↓" to the `fixtures-and-reproducibility` roll-up row, matching the summary table and the unit's own paragraph. |

### Validation Tool Results

| Check | Method | Raw output / derivation |
|---|---|---|
| Register size (headings) | `grep -c '^### BLK-' unit-of-work.md` | **9** |
| Open-blocker count | `grep -c '^\| Status ' unit-of-work.md` | **8** (one per BLK-02…BLK-09, every row beginning `Open`) — 9 − 8 = 1 closed (BLK-01), reproducing the artifact's own printed arithmetic |
| N-of-twelve carrying an open blocker row | Read § Unit definitions summary table's Blockers column for all 12 rows; a row with only a "— (BLK-01 closed …)" or bare "—" entry counted as carrying none | Carry none (3): `foundation`, `inventory-and-registry`, `external-products`. Carry at least one open ID (9): `governance-guards`, `acquisition`, `target-standardization`, `features-and-splits`, `models-and-baselines`, `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`, `fixtures-and-reproducibility`. Matches the artifact's "nine of the twelve… `foundation`, `inventory-and-registry` and `external-products` carry none" claim exactly, at both its `unit-of-work.md` § Blocker register intro and its `unit-of-work-dependency.md` § Independent unit sets mirror. |
| Untested-requirement total, route 1 (headline) | Read `unit-of-work-story-map.md` § Coverage headline and § Sources | **36**, stated consistently in both places and in `unit-of-work.md` § Sources |
| Untested-requirement total, route 2 (sum of per-unit Untested-requirements column) | 2+1+7+2+1+4+1+7+2+0+7+2 | **36** |
| Untested-requirement total, route 3 (literal count of bold requirement IDs under "Requirements with no acceptance row, by unit") | 2+1+7+2+1+4+1+7+2+7+2 (statistical-inference: 0, full coverage) | **36** |
| Requirements-column cross-check | Summed the Requirements column of the same per-unit table: 16+10+15+7+6+7+11+9+4+1+11+8 | **105**, matching the artifact's own stated total |
| Summary table vs. per-unit sections (Acceptance rows, Requirements) | Read all twelve `**Acceptance rows (N).**` and `**Requirements carried (N).**` lines in document order; compared against the two summary-table columns | Acceptance rows in order: 7, 2, 1, 3, 1, 2, 12, 5, 1, 2, 3, 4 — matches the summary table's column exactly, including the previously-corrected cells (rows 6, 7 now read 2, 12). Requirements column likewise matches throughout. |
| Edge count / unit count / acyclicity | Parsed the fenced `yaml` block programmatically (extracted `name`/`depends_on` pairs; checked uniqueness, self-loops, undeclared references; ran a Kahn topological sort) | 12 units, all unique names; 23 edges; 0 self-loops; 0 undeclared references; topological sort visited all 12 nodes — acyclic. Matches the artifact's own "12 units… 23 edges… acyclic" claim exactly. |
| BLK-span and register-size mirrors | `grep -n "BLK-01 through\|of the twelve units carry\|carry none\|blockers are registered"` across all three artifacts, each hit read in context | `unit-of-work.md`'s live text reads "BLK-01 is closed; BLK-02 through BLK-09 are open… **Nine** blockers are registered, and **nine of the twelve units**…" — correct; the "Seven… ten of the twelve…" text at the same location is inside a labelled `>` correction blockquote, a legitimate preserved supersession. `unit-of-work-dependency.md` reads "BLK-01 through **BLK-09**" and "**Nine** of the twelve units" — live and correct. `unit-of-work-story-map.md` reads "**Nine** of these carry a blocker ID (BLK-01 through **BLK-09**)" — live and correct. No surviving "BLK-01 through BLK-07" or "ten of the twelve" claim outside a labelled supersession box anywhere. |
| 40-row untested-count mirror | `grep -n "40-row\|untested count is unchanged\|40 →\s*36"` across all three artifacts | `unit-of-work-story-map.md` § RES-01 row now reads "the untested count is **unchanged by this row**" (no numeral), with a correction note explaining the rewrite. No live "the 40-row untested count is unchanged" or other bare "40" survives outside narration of the 40→36 correction itself or prior `## Review` sections. |
| ADR-11 identity mechanism vs. superseded containment rule | `grep -n "subset of that partition\|containment"` across all three artifacts, each hit classified by context | Every live occurrence states ADR-11's identity-check-with-one-exception mechanism. The two remaining "containment"/"subset of that partition" hits are both inside labelled correction boxes — legitimate preserved supersession, not live claims. |
| `FeatureBundle`/`Partition` vs. `feature matrix / F1–F4 folds` | `grep -n "feature matrix and sequence tensor\|F1–F4 folds\|FeatureBundle"` in `unit-of-work-dependency.md` | Both the Edge-table row and § Integration points state the corrected `FeatureBundle`s / six-member `Partition` contract, each with its own dated correction note. No live stale occurrence. |
| Roll-up table vs. summary table vs. per-unit paragraphs (full sweep, all 12 units) | Compared § Roll-up by unit's Blockers column against § Unit definitions summary table's Blockers column and each unit's own `**Blockers.**` paragraph, unit by unit | 11 of 12 roll-up rows agree with both other representations. `fixtures-and-reproducibility` disagrees — see Finding 1. |
| Topology-only discipline | `grep -n -i "build order\|critical path\|ship first\|should be built first\|recommend building"` across all three artifacts, every hit read in context | Every hit is the document's own disclaimer that it does not state a build order or critical path. No trespass on stage 2.8's territory found anywhere, including in text added since the last pass. |
| Gate readiness for 3.1/2.8 | Traced `features-and-splits` (the highest-blocker-count unit) end to end: summary table row → roll-up row → own `**Blockers.**` paragraph → § Blocker register entries for BLK-04, BLK-08, BLK-09 | All four representations agree exactly on which blockers this unit owns/co-owns and their status. Every blocker's Status field states "exit condition on stage 3.1, not an entry condition," consistently — no blocker blocks a unit's ability to enter 3.1. |

### Summary

The two ordered fixes are both correctly and fully applied, verified by independent re-derivation: the register genuinely holds 9 blockers with 8 open, the "nine of twelve / three carry none" figure is independently reproducible and correct now that BLK-01 is closed (`foundation` genuinely carries none), and the untested-requirement count is 36 by all three independent routes, agreeing with `requirements.md`. The fenced `yaml` edge block parses cleanly to 12 units and 23 edges with no self-loops, no undeclared references, and a clean topological sort. Topology-only discipline holds throughout. The mechanical mirror audit this pass was ordered to run surfaced exactly one further live defect of the same class the prior five passes were chasing, in a section none of them had swept before: `unit-of-work.md`'s § Roll-up by unit table omits BLK-08 ↓ and BLK-09 ↓ from the `fixtures-and-reproducibility` row, while the summary table and that unit's own paragraph both correctly carry them — a reader consulting only the roll-up table would under-count that unit's blocker exposure by two. This is a single-cell, mechanical correction with no bearing on the topology, the blocker substance, or any scientific ruling. What `delivery-planning` (2.8) is being handed is a DAG it can trust in full (12 units, 23 edges, acyclic, one independent pair, independently re-verified) and a blocker register whose content is sound and, apart from this one cell, fully consistent across every representation checked across this and all five prior passes — close enough to full internal consistency that the verdict is READY, with the one remaining cell named precisely for the human to weigh or wave through at the gate.

## Review — 2026-08-24 three-representation cross-check

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-24T06:00:00Z
**Iteration:** 7 (advisory, single pass)
**Scope reviewed:** the corrected `fixtures-and-reproducibility` roll-up row, plus an independent build of all three blocker representations (§ Unit definitions summary table, each unit's own `**Blockers.**` paragraph, § Roll-up by unit) for all twelve units; the two named traps (`governance-guards`'s BLK-07 cross-reference, the absent `**Blockers.**` paragraphs on `inventory-and-registry` and `external-products`); a re-sweep for live mirrors of every previously-corrected fact; the fenced `yaml` edge block in `unit-of-work-dependency.md`; topology-only discipline; gate readiness for 2.8. `unit-of-work-dependency.md` and `unit-of-work-story-map.md` were read only where the brief's carve-out required it (the edge block; the cross-reference spot-check) — both confirmed unchanged since the last full-mirror-audit pass.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `unit-of-work.md` § Assumptions & Open Questions, the "**Still open — all six, enumerated rather than sampled**" bullet (annotated in place 2026-08-22) | This bullet states, as a live and unlabelled claim, "**the count of open blockers remains six**," and enumerates only BLK-02 through BLK-07. It was written and annotated on 2026-08-22, before BLK-08 and BLK-09 were registered on 2026-08-23, and was never revisited when § Blocker register and § Roll-up by unit were updated for those two new entries. The true open-blocker count, reproducible from the register's own headings and Status rows (verified below), is **eight** (BLK-02 through BLK-09), not six. This is the same "BLK-01 through BLK-07 / seven blockers" staleness class that four prior passes already found and fixed at the register intro, `unit-of-work-dependency.md`, and `unit-of-work-story-map.md` — but this occurrence, in a different section of the same file, was missed by all of them, including the pass immediately prior to this one whose own scope was a full mirror sweep. A reader who consults this bullet rather than the register undercounts open blockers by two, and undercounts which units the "still open" enumeration should name (BLK-08 affects `features-and-splits` and `evaluation-and-comparison`; BLK-09 affects `features-and-splits`). | Add BLK-08 and BLK-09 to the enumeration with their current status ("BLK-08 — the inverse-transform routing mechanism, co-owned by `features-and-splits` and `evaluation-and-comparison`. Open." / "BLK-09 — `Partition`'s missing `train_start`. Open."), and correct "six" to "eight." |
| 2 | Minor | `unit-of-work.md` §4 `inventory-and-registry` and §6 `external-products` — both sections carry no `**Blockers.**` paragraph at all | Every other unit, including `foundation` (which also carries no open blocker), states its blocker status explicitly — `foundation`'s paragraph reads "**Blockers.** **None open. BLK-01 closed 2026-08-22**…". `inventory-and-registry` and `external-products` are the only two of twelve units where the paragraph is missing outright rather than stating "None open." The two units genuinely carry no blocker (confirmed independently below, and stated correctly in both the summary table and the roll-up table, the latter with an explicit justifying sentence), so this is not a factual error — but it breaks the document's own established convention, and a reader consulting only a unit's own section (the failure mode this register exists to prevent, per its own opening paragraph) has no way to distinguish "verified none" from "never checked" for these two units specifically. | Add a `**Blockers.**` paragraph to both units' sections mirroring `foundation`'s wording, e.g. "**Blockers.** None open." |

### Validation Tool Results

| Check | Method | Raw output |
|---|---|---|
| Three-representation blocker set per unit, all 12 units | Read § Unit definitions summary table's Blockers column, each unit's own `**Blockers.**` paragraph (or its absence), and § Roll-up by unit's Blockers column; built one set per unit per representation and diffed them | `foundation`: {} / {} / {} — agree. `governance-guards`: {BLK-06} / {BLK-06} / {BLK-06} — agree (BLK-01 closed, noted identically in all three). `acquisition`: {BLK-07} / {BLK-07} / {BLK-07} — agree. `inventory-and-registry`: {} / *no paragraph* / {} — Finding 2; sets agree, representation missing. `target-standardization`: {BLK-05} / {BLK-05} / {BLK-05} — agree. `external-products`: {} / *no paragraph* / {} — Finding 2; sets agree, representation missing. `features-and-splits`: {BLK-04, BLK-08(co-owned), BLK-09} / same / same — agree. `models-and-baselines`: {BLK-03, BLK-04↓, BLK-09↓} / same / same — agree. `evaluation-and-comparison`: {BLK-08(owned), BLK-03↓, BLK-04↓, BLK-09↓} / same / same — agree. `statistical-inference`: {BLK-03↓, BLK-04↓, BLK-08↓, BLK-09↓} / same / same — agree. `regimes-diagnostics-reporting`: {BLK-03↓, BLK-04↓, BLK-08↓, BLK-09↓} / same / same — agree. `fixtures-and-reproducibility`: {BLK-02, BLK-03↓, BLK-04↓, BLK-08↓, BLK-09↓} / same / same — **agree in full; the ordered fix is applied correctly and all three representations now match.** |
| Is the corrected `fixtures-and-reproducibility` row right under the stated inheritance rule | Read the unit's own paragraph's stated rule ("this unit's `depends_on` includes every unit carrying those blockers") against the `yaml` edge block's `depends_on` list for `fixtures-and-reproducibility` and against which of those nine depended-on units actually carry BLK-08 or BLK-09 | `depends_on` = `[acquisition, inventory-and-registry, target-standardization, external-products, features-and-splits, models-and-baselines, evaluation-and-comparison, statistical-inference, regimes-diagnostics-reporting]`. Of these, `features-and-splits` owns BLK-08 (co-owned) and BLK-09; `evaluation-and-comparison` owns BLK-08; `models-and-baselines`, `statistical-inference`, `regimes-diagnostics-reporting` all inherit BLK-09↓ and/or BLK-08↓. The rule correctly yields BLK-08↓ and BLK-09↓ for `fixtures-and-reproducibility`. **Correction confirmed right.** |
| `governance-guards`'s BLK-07 mention — cross-reference or carried blocker? | Read `governance-guards`'s full `**Blockers.**` paragraph (line 165) and its Status field | BLK-07 appears only inside the sentence naming `acquisition` as a downstream consumer of `governance-guards`'s `open_restricted` contract ("`acquisition` (the D-9 input and any December re-acquisition — **BLK-07**)"). `governance-guards`'s own Status sentence names only BLK-06 as open and BLK-01 as closed; BLK-07's own register entry (§ Blocker register) names its Owning unit as `acquisition`, not `governance-guards`. **The author's reading is correct: cross-reference only, not carried.** |
| Absent `**Blockers.**` paragraph on `inventory-and-registry` / `external-products` — is silence the right way to say "none" in this document? | Compared against `foundation`'s explicit "**Blockers.** **None open.** …" paragraph and the register's own stated design goal ("no unresolved artifact is allowed to read as approved… the register names the files so the boundary is checkable rather than asserted") | The convention this document sets for itself is to state "none open" explicitly, not omit the section. Two of twelve units depart from that convention. Finding 2. |
| Open-blocker count, independently re-derived | `### BLK-0…` headings → 9; `\| Status \|` rows beginning `Open` → 8 (BLK-02 through BLK-09); 9 − 8 = 1 closed (BLK-01) | **8 open, 1 closed, 9 registered** — matches § Blocker register's own corrected figures, and directly contradicts Finding 1's "six." |
| Untested-requirement count (36) — re-derived independently this pass | Read the twelve `Bold = … (N of M)` lines: 2,1,7,2,1,4,1,7,2,0,7,2 → sum 36; read the twelve `**Acceptance rows (N).**` lines: 7,2,1,3,1,2,12,5,1,2,3,4 → sum 43, matches top summary table's Acceptance-rows column cell-for-cell in order; read the twelve `**Requirements carried (N).**` lines: 16,10,15,7,6,7,11,9,4,1,11,8 → sum 105, matches top summary table's Requirements column cell-for-cell | All three counts self-consistent and matching the summary table exactly; no live "40" found outside labelled supersession text or prior `## Review` sections. |
| Fenced `yaml` edge block (`unit-of-work-dependency.md`) | Read the block directly; counted units and `depends_on` list lengths per unit; checked every `depends_on` reference resolves to a declared unit name; checked for self-loops; confirmed the listed order is already a valid topological order (no unit's `depends_on` names a unit later in the list) | 12 units, all uniquely named. Edge-list lengths in file order: 0,1,2,1,1,1,3,1,2,1,1,9 → sum **23**. 0 self-loops. 0 undeclared references. File order is itself a valid topological order (`fixtures-and-reproducibility` last, depending only on units above it) → **acyclic**. Unchanged since the prior full-mirror-audit pass, as stated in the dispatch. |
| ADR-11 identity mechanism / `FeatureBundle`/`Partition` contract — any live stale mirror in `unit-of-work.md` | `grep -n -i "containment\|subset of that partition"` and `grep -n "apply_transforms\|FeatureBundle\|train_start"`, each hit classified by context | Every live occurrence (BLK-04's register entry, `features-and-splits`'s own paragraph, BLK-09's entry, the roll-up row) states ADR-11's identity-check mechanism and the current `fit_transforms(bundle: FeatureBundle, *, partition: Partition)` / `apply_transforms` removed signature. The two "containment"/"subset of that partition" hits are both inside labelled `⚠`/"Superseded text, preserved" boxes — legitimate supersession, not live claims. No stale mirror found. |
| Topology-only discipline | `grep -n -i "build order\|critical path\|ship first\|should be built first\|recommend building"` | Every hit is the document's own disclaimer that it states no build order or critical path (e.g. "no ordering is implied by the row numbers"). No trespass found. |
| Gate readiness for 2.8: does the blocker register now agree with itself, everywhere, and can a 3.1 reader trust the per-unit rows | Aggregate of the above | Twelve-for-twelve agreement across the three per-unit blocker representations (the fixture-row fix holds and is correct); the DAG is acyclic and unchanged; no build-order trespass. One live document-level claim (the "six open blockers" bullet, Finding 1) still disagrees with the register's own count, and two units' per-unit representation is an omission rather than a stated "none" (Finding 2). Neither finding touches the DAG, the per-unit blocker *sets*, or any scientific ruling. |

### Summary

The ordered fix is correct and complete: `fixtures-and-reproducibility`'s roll-up row now carries BLK-08 ↓ and BLK-09 ↓, and all three representations — the summary table, the unit's own paragraph, and the roll-up table — agree exactly for all twelve units under an independently re-derived and confirmed inheritance rule. Both named traps resolve in the author's favor on independent re-check: `governance-guards`'s BLK-07 mention is genuinely a cross-reference to `acquisition`'s own blocker, and `inventory-and-registry`/`external-products` genuinely carry no blocker, correctly reflected in the summary table and the roll-up table. This pass's own independent sweep, going beyond the two named traps, surfaced one further live mirror the prior six passes did not check: § Assumptions & Open Questions still asserts "the count of open blockers remains six," a count that went stale the moment BLK-08 and BLK-09 were registered and was never revisited in that section, while the register itself (correctly) states eight. A second, lower-severity finding is that two units depart from this document's own convention of stating "None open" explicitly, leaving their absence of a blocker paragraph indistinguishable from an unchecked gap to a reader of that section alone. Neither finding reopens the DAG, the blocker register's substantive content, or any scientific ruling; both are precisely located, single-location corrections. What `delivery-planning` (2.8) is being handed is a DAG it can trust in full (12 units, 23 edges, acyclic, unchanged and re-verified), a blocker register whose per-unit content is now fully and correctly propagated across all three of its representations, and one remaining stale headline count outside the register proper, plus one presentation inconsistency, both named precisely for the human to weigh or wave through at the gate.

## Review — 2026-08-24 finding corrections

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-24T10:09:33Z
**Iteration:** 8 (advisory, single pass)
**Scope reviewed:** the two corrections applied to `unit-of-work.md` against the prior pass's Major and Minor findings — the "Still open — all eight" § Assumptions & Open Questions bullet, and the new `**Blockers.** **None open, and none inherited.**` paragraphs on `inventory-and-registry` (§4) and `external-products` (§6) — each independently re-derived rather than accepted from the artifact's own stated derivation. `unit-of-work-dependency.md` and `unit-of-work-story-map.md` are unchanged since the last cross-check pass; both were re-read in full this pass (not merely spot-checked) as part of the live-mirror sweep, since a stage-diary learning of this project's own (`project.md` § Corrections, `cid:units-generation:re-1`) is that sweeping only the entity a fix touches, rather than every representation of the fact, is exactly the defect class this stage has repeatedly produced.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|

None. Both corrections were checked and hold.

### Validation Tool Results

| Check | Method | Raw output |
|---|---|---|
| Open-blocker set, independently re-derived and compared against the corrected bullet | `grep -n '^### BLK-0' unit-of-work.md` for the register's own headings; `grep -n '^\| Status '` for its Status rows; then read § Assumptions & Open Questions line 1025 and listed every `**BLK-0N**` token it names | Headings: 9 (BLK-01 through BLK-09). Status rows: 8, every one beginning `Open` (BLK-02 through BLK-09) → 9 − 8 = 1 closed (BLK-01). The bullet names exactly BLK-02, BLK-03, BLK-04, BLK-05, BLK-06, BLK-07, BLK-08, BLK-09 — eight IDs, an exact match to the derived open set — and closes "the count of open blockers is eight," matching. |
| BLK-08 and BLK-09 one-line statements in the bullet vs. their own register entries | Compared the bullet's BLK-08 clause ("`Transform.inverse` is reachable only from `Prediction.transform_id`, a `str`, with no lookup, registry or import edge named... Owned by `evaluation-and-comparison`, co-owned by `features-and-splits`") and BLK-09 clause ("`Partition` carries no `train_start`... Owned by `features-and-splits`") against § Blocker register's `### BLK-08` (line 823) and `### BLK-09` (line 841) entries | Both match their register entries on affected artifact, mechanism and ownership — no drift introduced by summarizing. |
| Exit-condition sentence — does BLK-08/BLK-09 belong on the same terms as BLK-03/BLK-04/BLK-07 | Read each of BLK-03, BLK-04, BLK-07, BLK-08, BLK-09's own `\| Status \|` field for the "exit condition on stage 3.1" framing, and BLK-02/BLK-05's Status fields for the "owner/supervisor decision" framing; checked BLK-06 was correctly omitted from both categories | BLK-08's Status: "Exit condition on stage 3.1 for both owning units, on the same terms the owner set for BLK-03 and BLK-04." BLK-09's Status: "Exit condition on stage 3.1 for `features-and-splits`, on the BLK-03/BLK-04 terms." Both genuinely carry the same framing as BLK-03/BLK-04/BLK-07. BLK-06 is correctly excluded from the sentence — its own Status field frames it as blocking implementation and G-P2/G-P3C acceptance, not as a stage-3.1 exit condition, and it was excluded from this same sentence's six-blocker predecessor for the identical reason (checked against the propagation-sweep pass's own text). |
| `inventory-and-registry`'s "none inherited" claim vs. BLK-07's own "Downstream units" field, which names `inventory-and-registry` | Read BLK-07's `\| Downstream units \|` field (line 815: "none by import. The block reaches G-P1A, G-05 and G-06... and `inventory-and-registry`, whose G-P1A coverage audit consumes this unit's released artifacts") against `inventory-and-registry`'s new paragraph and against the established document convention for this exact pattern | This is not a contradiction: BLK-07's "Downstream units" field lists gates and units *informationally reached* through a governance-boundary consequence chain ("none by import" is stated first), distinct from roll-up inheritance (↓). The document already uses this same pattern for BLK-06, whose field names `fixtures-and-reproducibility` as "the supporting unit on TA-27's hash-diff evidence" while the Roll-up table correctly does *not* list BLK-06 against that unit — a pattern the 2026-08-23 full mirror audit pass checked and passed. `inventory-and-registry`'s own outputs (`src/data/inventory.py`, `src/data/registry.py`) are not named by BLK-07's Affected-artifact field, and its own December read is separately routed through `open_restricted` per the Roll-up table's own justifying sentence. The summary table, roll-up table and BLK-07's own Owning-unit field (`acquisition`, not `inventory-and-registry`) all agree the unit carries no blocker of its own. |
| `external-products`'s "none inherited" claim vs. BLK-08 | Read BLK-08's Affected-artifact, Owning-unit and Co-owning-unit fields, and searched the full blocker register (lines 581–855) for any mention of `spaceweather.py`, `iri.py`, `gim.py`, `04_build_external_products.py` or `external-products` outside BLK-08's own Approval-authority sentence | BLK-08 is about `Transform.inverse`, owned by `evaluation-and-comparison` and co-owned by `features-and-splits` — no mention of any artifact `external-products` owns. The only register hit for `external-products`'s domain is BLK-08's Approval-authority field noting "the `iri.py`/`gim.py` allowlist is unaffected." No open blocker names a contract `external-products` produces. |
| Live mirror re-sweep: blocker span/count in both files, the `RES-01` untested-count numeral, the two blocker-table figures, ADR-11 identity vs. containment, `FeatureBundle`/`Partition` | Re-read `unit-of-work-dependency.md` § Independent unit sets (lines 273–288) and `unit-of-work-story-map.md` § Open verification gaps (line 297) and § RES-01 (line 323) in full; `grep -n "BLK-01 through\|of the twelve units carry\|\b40\b"` across all three artifacts, each hit classified by hand | Both files state "BLK-01 through **BLK-09**" and "nine of the twelve" / "**Nine** of these carry a blocker ID," live and correct. `unit-of-work-story-map.md`'s RES-01 row now reads "the untested count is **unchanged by this row**" with no numeral (the 2026-08-23 fix holds). Every remaining `\b40\b` hit is inside a labelled "corrected ... from 40" / "40 → 36" narration sentence, a `## Review —` section, or the unrelated "ARUC 40/44" cell label — no live unlabelled "40" survives anywhere. No live "containment" / "subset of that partition" survives outside the two labelled supersession boxes. |
| Summary-table and per-unit Bold/Requirements counts, re-derived independently | `grep -oE` for all twelve `Bold = no §16/§19 test row (N of M here)` lines and summed the N values; summed the twelve `**Requirements carried (N).**` values | Bold sum: 2+1+7+2+1+4+1+7+2+0+7+2 = **36**, matching every headline occurrence. Requirements sum: 16+10+15+7+6+7+11+9+4+1+11+8 = **105**, matching every headline occurrence. Both agree with the top summary table cell-for-cell. |
| Fenced `yaml` edge block (`unit-of-work-dependency.md`) | Parsed programmatically with a Node script: extracted `name`/`depends_on` pairs, checked uniqueness/self-loops/undeclared references, verified the printed order is a valid topological order | 12 uniquely-named units; 23 total edges (per-unit counts 0,1,2,1,1,1,3,1,2,1,1,9); 0 self-loops; 0 undeclared references; 0 order violations against the printed order — acyclic, matching the artifact's own claim. |
| Topology-only discipline | `grep -n -i "build order\|critical path\|ship first\|should be built first\|recommend building"` across all three artifacts, every hit read in context | Every hit is the document's own disclaimer that no build order or critical path is stated (e.g. line 17-18, line 1086). No trespass on stage 2.8's territory anywhere, including in the text corrected for this pass. |
| Gate readiness for 2.8 | Aggregate of the above, plus re-reading `governance-guards`'s BLK-07 cross-reference (already confirmed sound by the prior pass) | Both corrections are verified correct and complete; no new defect surfaced by the independent re-derivation or the live-mirror re-sweep. The DAG, the blocker register's substantive content, and all three of its representations remain internally consistent across all twelve units. |

### Summary

Both corrections ordered by the human owner's "fix findings" ruling are verified correct on independent re-derivation, not merely re-read. The § Assumptions & Open Questions bullet now names exactly the eight open blockers the register itself derives (BLK-02 through BLK-09), states each one-liner accurately against its own register entry, and correctly places BLK-08 and BLK-09 among the stage-3.1 exit conditions on the same terms as BLK-03, BLK-04 and BLK-07 — while correctly leaving BLK-06 out of that framing, since BLK-06's own Status field blocks implementation and the G-P2/G-P3C gates rather than exit from stage 3.1. The two new `**Blockers.** **None open, and none inherited.**` paragraphs on `inventory-and-registry` and `external-products` are both factually sound: BLK-07's mention of `inventory-and-registry` in its own "Downstream units" field is an informational reach through a governance-boundary consequence chain, not a roll-up inheritance — the same pattern this document already uses for BLK-06's mention of `fixtures-and-reproducibility`, which a prior pass already checked — and no open blocker names any artifact `external-products` owns (BLK-08 is entirely about `Transform.inverse`, owned by `evaluation-and-comparison` and co-owned by `features-and-splits`). A full re-sweep for every other fact this stage has previously corrected — the blocker span and count in both companion artifacts, the untested-requirement count by three independent routes, the summary-table Bold/Requirements/Acceptance-rows columns against their per-unit sections, the ADR-11 identity mechanism versus the withdrawn containment reading, and the `FeatureBundle`/`Partition` contract — found no live stale mirror; every prior correction still holds. The fenced `yaml` edge block re-parses cleanly to 12 units and 23 edges with no self-loops, no undeclared references, and a valid topological order, and no build-order or critical-path trespass was found anywhere in the text added by this correction. What `delivery-planning` (2.8) is being handed is a topology it can trust in full and a blocker register — now including its § Assumptions & Open Questions mirror and both previously-silent per-unit sections — that is internally consistent across every representation checked across all eight review passes to date.

