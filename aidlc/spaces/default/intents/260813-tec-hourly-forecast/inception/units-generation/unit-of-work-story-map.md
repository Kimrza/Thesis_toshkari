# Unit of Work Story Map — Hourly VTEC Forecasting (TEC_Project Phase 1)

Stage 2.7 (units-generation), intent `260813-tec-hourly-forecast`.

## There are no user stories, and none were invented

Stage 2.4 (`user-stories`) is **`SKIP`** in the `research-pipeline-governed`
scope, so `../user-stories/stories.md` **does not exist**. The stage's
`produces` list fixes this artifact's filename, so what changes is its content,
not its name.

Per Q4 = C, approved requirements and the existing §16/§19 acceptance rows are
used as the authoritative substitutes for story-based mapping. Nothing here is
fabricated: no user story, no acceptance row, no test result and no governance
approval. `team-practices.md` § Testing Posture records why this is the whole
acceptance vocabulary Construction will receive — with 2.4 skipped, TE §16's WS
rows and §19's TA rows are the only source of acceptance criteria.

## Sources

- Requirements: `../requirements-analysis/requirements.md` — the 105 requirement rows mapped in Table 1, and the 40-row untested list.
- Design: `../application-design/components.md` (which module carries which requirement), `../application-design/component-methods.md` (the boundary calls acceptance evidence is asserted against), `../application-design/services.md` (the nine stage scripts and the ordering contract), `../application-design/component-dependency.md` (the forbidden edges and their tests), `../application-design/decisions.md` (ADR-03's split guard, ADR-09's Phase 2 boundary, ADR-10's unsigned amendment).
- Acceptance vocabulary: TE §16 (WS-01…WS-20) and TE §19 (TA-01…TA-32), with Phase 1 applicability fixed by FR-WS-4 and `requirements.md` § Success and acceptance.
- Companion: `unit-of-work.md`, `unit-of-work-dependency.md`.

## Table 1 — Requirement to unit

Every in-scope requirement is assigned to exactly **one** primary implementing
unit. Where responsibility genuinely crosses a boundary, supporting units are
named in § Cross-unit responsibilities below rather than by giving a requirement
two owners.

**Derived when this artifact was written:** 105 requirement rows, 105 assigned,
0 unassigned, 0 assigned twice.

| Requirement | Primary unit | §16/§19 test row |
|---|---|---|
| REQ-ENG-1 | `foundation` | TA-01 |
| REQ-ENG-2 | `foundation` | TA-02 |
| REQ-ENG-3 | `foundation` | TA-03, TA-26 |
| REQ-ENG-4 | `foundation` | TA-09 — bounded, see § Known defects row 8 |
| REQ-ENG-5 | `governance-guards` | WS-10, TA-07, TA-08, TA-12, TA-27 |
| REQ-ENG-6 | `foundation` | TA-22 |
| REQ-ENG-7 | `foundation` | **NO CURRENT ACCEPTANCE ROW** |
| REQ-ENG-8 | `foundation` | TA-16 |
| REQ-ENG-10 | `foundation` | **NO CURRENT ACCEPTANCE ROW** |
| REQ-ENG-11 | `foundation` | TA-17, TA-26 |
| REQ-ENG-9 | `external-products` | **NO CURRENT ACCEPTANCE ROW** |
| REQ-ENG-12 | `regimes-diagnostics-reporting` | TA-16 — re-pointed here, TA-16's content being stated by this requirement rather than assumed by REQ-ENG-8's citation of it |
| REQ-ENG-13 | `acquisition` | TA-16 |
| FR-P1-00-1 | `acquisition` | TA-31 |
| FR-P1-00-2 | `acquisition` | TA-25 |
| FR-P1-01-1 | `acquisition` | TA-32 |
| FR-P1-01-2 | `acquisition` | TA-15 |
| FR-P1-01-3 | `acquisition` | TA-03, TA-15 |
| FR-P1-01-4 | `acquisition` | TA-04, TA-15 |
| FR-P1-01-11 | `acquisition` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-01-5 | `acquisition` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-01-6 | `acquisition` | TA-08 |
| FR-P1-01-7 | `acquisition` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-01-8 | `acquisition` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-01-9 | `acquisition` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-01-10 | `foundation` | TA-22 |
| FR-P1-02-1 | `inventory-and-registry` | WS-01 — retained in Phase 1 as a named exception, see § Known defects row 9; TA-04 |
| FR-P1-02-7 | `inventory-and-registry` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-02-2 | `inventory-and-registry` | TA-04 |
| FR-P1-02-3 | `inventory-and-registry` | WS-18, TA-25 |
| FR-P1-02-4 | `inventory-and-registry` | TA-25 |
| FR-P1-02-5 | `inventory-and-registry` | TA-25 |
| FR-P1-02-8 | `inventory-and-registry` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-02-6 | `governance-guards` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-03-1 | `target-standardization` | TA-04 |
| FR-P1-03-2 | `governance-guards` | TA-27 |
| FR-P1-03-3 | `target-standardization` | TA-15 |
| FR-P1-03-4 | `target-standardization` | TA-15 |
| FR-P1-03-5 | `target-standardization` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-04-1 | `features-and-splits` | WS-10, TA-07 |
| FR-P1-04-2 | `features-and-splits` | WS-11, TA-08 |
| FR-P1-04-3 | `external-products` | WS-11 |
| FR-P1-04-4 | `external-products` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-04-5 | `features-and-splits` | WS-12, TA-11 |
| FR-P1-04-6 | `features-and-splits` | TA-11 |
| FR-P1-04-7 | `evaluation-and-comparison` | WS-16, TA-11 |
| FR-P1-04-8 | `features-and-splits` | WS-13, TA-11 |
| FR-P1-04-9 | `external-products` | WS-09, TA-12 |
| FR-P1-04-18 | `external-products` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-04-10 | `features-and-splits` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-04-11 | `foundation` | TA-15 |
| FR-P1-04-12 | `features-and-splits` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-04-13 | `features-and-splits` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-04-14 | `models-and-baselines` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-04-15 | `external-products` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-04-16 | `features-and-splits` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-04-17 | `external-products` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-05-1 | `models-and-baselines` | WS-14, TA-12, TA-26 |
| FR-P1-05-2 | `models-and-baselines` | WS-15, TA-13 |
| FR-P1-05-3 | `models-and-baselines` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-05-4 | `models-and-baselines` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-05-5 | `models-and-baselines` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-05-6 | `models-and-baselines` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-05-7 | `evaluation-and-comparison` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-05-8 | `statistical-inference` | WS-17, TA-14 |
| FR-P1-05-9 | `regimes-diagnostics-reporting` | TA-20 |
| FR-P1-05-20 | `regimes-diagnostics-reporting` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-05-10 | `regimes-diagnostics-reporting` | TA-19 |
| FR-P1-05-11 | `regimes-diagnostics-reporting` | WS-19 |
| FR-P1-05-16 | `regimes-diagnostics-reporting` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-05-12 | `governance-guards` | WS-18, TA-18 |
| FR-P1-05-13 | `foundation` | TA-10 |
| FR-P1-05-14 | `regimes-diagnostics-reporting` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-05-15 | `regimes-diagnostics-reporting` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-05-17 | `evaluation-and-comparison` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-05-19 | `regimes-diagnostics-reporting` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-05-18 | `regimes-diagnostics-reporting` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-05-21 | `models-and-baselines` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-05-22 | `models-and-baselines` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-06-1 | `governance-guards` | TA-27 |
| FR-P1-06-2 | `governance-guards` | TA-27 |
| FR-P1-06-3 | `governance-guards` | TA-28 |
| FR-P1-06-4 | `governance-guards` | TA-28 |
| FR-WS-1 | `fixtures-and-reproducibility` | WS-20, TA-09 |
| FR-WS-2 | `fixtures-and-reproducibility` | **NO CURRENT ACCEPTANCE ROW** |
| FR-WS-3 | `fixtures-and-reproducibility` | **NO CURRENT ACCEPTANCE ROW** |
| FR-WS-4 | `fixtures-and-reproducibility` | WS-01, WS-09…WS-20 |
| FR-WS-5 | `fixtures-and-reproducibility` | WS-20, TA-17 |
| FR-WS-6 | `fixtures-and-reproducibility` | TA-03, TA-26 |
| FR-WS-7 | `foundation` | TA-23 |
| NFR-IRI-01 | `features-and-splits` | WS-10, TA-07 |
| NFR-LEAK-01 | `features-and-splits` | WS-11, TA-08, TA-11 |
| NFR-FAIR-01 | `evaluation-and-comparison` | WS-16, TA-11 |
| NFR-REP-01 | `fixtures-and-reproducibility` | WS-20, TA-17 |
| NFR-DET-01 | `foundation` | WS-17, TA-13 |
| NFR-DQ-01 | `target-standardization` | TA-19 |
| NFR-AUD-01 | `foundation` | TA-10, TA-21 |
| NFR-SEC-01 | `foundation` | TA-22 |
| NFR-PHASE-01 | `governance-guards` | TA-27 |
| NFR-TDEF-01 | `target-standardization` | TA-15 |
| NFR-LIC-01 | `governance-guards` | TA-28 |
| REQ-NFR-A1 | `acquisition` | **NO CURRENT ACCEPTANCE ROW** |
| REQ-NFR-A2 | `acquisition` | **NO CURRENT ACCEPTANCE ROW** |
| REQ-NFR-A3 | `fixtures-and-reproducibility` | TA-03 |
| REQ-CLAIM-01 | `regimes-diagnostics-reporting` | **NO CURRENT ACCEPTANCE ROW** |

## Table 2 — Acceptance row to unit

Phase 1's acceptance set is **WS-01 (a named exception) plus WS-09 through
WS-20**; WS-02–WS-08 are deferred to G-P3A because TE §7.0's Phase 1 hard
prohibition bars Phase 1 from producing the raw-processing evidence those rows
require (FR-WS-4, countersigned 2026-08-16). The Phase 1-applicable TA set is the
26 rows `requirements.md` § Success and acceptance enumerates, plus TA-27's first
limb, which is Phase 1-applicable while its second limb is accepted at G-P2 and
G-P3C.

**Derived when this artifact was written:** 13 WS rows and 27 TA rows mapped
(26 enumerated Phase 1-applicable TA rows plus TA-27's first limb), of which
39 have an evidence-producing unit and
1 does not.

| Row | What it checks | Evidence-producing unit | Supporting | Evidence |
|---|---|---|---|---|
| WS-01 | Station registry is populated from official site logs with pinned IGRF coordinates; header cross-check shows no unresolved conflict | `inventory-and-registry` | — | `tests/test_station_registry.py`, registry artifact + site-log diff |
| WS-09 | IRI benchmark and GIM comparator sample alignment passes; IRI ceiling and drivers are recorded; GIM overlap audit is present | `external-products` | — | benchmark/comparator manifests, `gim_network_overlap_flag` audit, `iri_implementation_validation` report |
| WS-10 | The IRI-denial test fails when an `iri_*` field is deliberately injected into the ML feature path | `features-and-splits` | `external-products` | `tests/test_iri_denial.py` — must fail on deliberate injection |
| WS-11 | Availability lag assertions pass for every primary feature; F10.7 mean is trailing; Dst is diagnostic-only; SSN is absent | `features-and-splits` | `external-products` | `tests/test_feature_availability.py`, availability matrix, driver manifests |
| WS-12 | F1–F4 splits and the 24 h embargo produce no window crossing a boundary; first 24 h are excluded and counted | `features-and-splits` | — | `tests/test_split_embargo.py`, fold manifests with excluded-row counts |
| WS-13 | Flattened matrix and sequence tensor for a given feature-set ID contain the same underlying window values | `features-and-splits` | — | matched-window parity assertion over one `windows.py` definition |
| WS-14 | M-01, M-02, M-03, M-04, M-05 predictions run | `models-and-baselines` | — | `tests/test_models_smoke.py`, per-model prediction artifacts |
| WS-15 | Minimal M-06 trains and restores its lowest-validation-RMSE checkpoint | `models-and-baselines` | — | `tests/test_checkpoint_restore.py`, checkpoint artifact |
| WS-16 | Comparison-wide intersection masks are stored with stable IDs and row counts; no pairwise mask is produced | `evaluation-and-comparison` | — | `tests/test_common_masks.py`, mask registry with stable IDs |
| WS-17 | Vector time-block bootstrap carries all stations together and reproduces exactly from seed 20221201 | `statistical-inference` | — | `tests/test_bootstrap.py`, replicate hash from seed 20221201 |
| WS-18 | Locked-test guard blocks December performance execution before G-05 and records access | `features-and-splits` | `governance-guards` | `tests/test_locked_test_guard.py`, access-log sample, `locked_test_accessed` registry flag |
| WS-19 | Required prediction, residual, target-support, and quality plots exist | `regimes-diagnostics-reporting` | — | figure set, each carrying its source-data IDs |
| WS-20 | A clean CPU environment reproduces both fixtures within declared tolerances | `fixtures-and-reproducibility` | — | `tests/test_clean_run.py`, clean-run log, both fixture manifests |
| TA-01 | Repository skeleton exists with four configs, six packages, nine phase-aware stage scripts, five notebooks, tests, and artifacts | `foundation` | — | repository tree and code commit |
| TA-02 | All four configuration files exist and every unresolved field is visibly marked `TBD — freeze gate` | `foundation` | — | config inventory + schema validation |
| TA-03 | Python 3.11 and exact pins install successfully on both Kaggle and local | `foundation` | `fixtures-and-reproducibility` | install logs from both platforms, `environment_and_cpu_preflight_report` |
| TA-04 | Station registry, inventory, and hash tooling operate on both fixtures | `inventory-and-registry` | `fixtures-and-reproducibility` | fixture run logs, hash manifests |
| TA-07 | `test_iri_denial.py` fails on deliberate `iri_*` injection, and no module under `src/features` or `src/models` imports `src/external/iri.py` | `features-and-splits` | `governance-guards` | `tests/test_iri_denial.py` + import-boundary check output |
| TA-08 | Availability lag assertions pass; F10.7 mean is trailing; Dst is diagnostic-only; SSN is absent from the codebase | `features-and-splits` | `external-products` | `tests/test_feature_availability.py` + grep evidence for SSN absence |
| TA-09 | Both walking-skeleton fixtures pass all 20 Section 16 checks with evidence links — **bounded** to WS-01 and WS-09…WS-20 per FR-WS-4 and § Known defects row 8 | `fixtures-and-reproducibility` | — | fixture acceptance table with per-row evidence links |
| TA-10 | Experiment registry is operational, append-safe, and records failed as well as successful runs | `foundation` | — | `experiment_registry.jsonl` with an aborted-run row |
| TA-11 | F1–F4 splits, 24 h embargo, train-only transforms, and comparison-wide mask tests pass, including the matched-window assertion | `features-and-splits` | `evaluation-and-comparison` | `test_split_embargo.py`, `test_train_only_transforms.py`, `test_common_masks.py`, parity assertion |
| TA-12 | All required model IDs M-01–M-06 plus B-01 and C-01 are represented in modules and configs; residual and GRU modules are absent from the codebase | `models-and-baselines` | `external-products` | module/config inventory + grep evidence for residual and GRU absence |
| TA-13 | Best-checkpoint restoration and the three-seed element-wise mean are implemented | `models-and-baselines` | `foundation` | `tests/test_checkpoint_restore.py`, three-seed mean artifact with its seed set |
| TA-14 | Vector time-block bootstrap produces reproducible 24-hour output, a 48-hour sensitivity, and cross-station correlation, verified on synthetic correlated data | `statistical-inference` | — | `tests/test_bootstrap.py` incl. synthetic-correlated-data case |
| TA-15 | Dataset release records required provenance, row counts, exclusions, IDs, and SHA-256 hashes | `foundation` | `target-standardization`, `acquisition` | `tests/test_release_hashes.py`, release manifest (ten rows, fourteen fields) |
| TA-16 | Every analysis/review notebook declares expected versions and IDs and calls `src/` modules; the acquisition-notebook exception is limited to download/manifest/ZIP logic and matches the reusable script | `regimes-diagnostics-reporting` | `acquisition` | notebook header declarations + acquisition-notebook/script diff |
| TA-17 | Full ordered clean-run contract succeeds on CPU in a fresh environment within declared runtime, storage, and numerical tolerances | `fixtures-and-reproducibility` | — | `tests/test_clean_run.py`, clean-run log, matched artifacts |
| TA-18 | Locked-test guard prevents December performance execution before G-05; predictions are hashed before metrics; registry records all access | `features-and-splits` | `governance-guards`, `evaluation-and-comparison` | guard test + access-log sample + prediction hash preceding any metric |
| TA-19 | Target uncertainty budget is produced and is reported adjacent to the primary result | `target-standardization` | `regimes-diagnostics-reporting` | uncertainty budget artifact + its placement in the results section |
| TA-20 | Primary results table contains the mandatory difficulty controls (persistence, seasonal persistence, climatology) alongside the IRI benchmark comparison | `regimes-diagnostics-reporting` | `models-and-baselines` | primary results table |
| TA-21 | Traceability matrix connects each implemented requirement to a decision, test/experiment, and evidence artifact | `fixtures-and-reproducibility` | — | traceability matrix artifact |
| TA-22 | Security review confirms no secrets in notebooks, code, configs, logs, or artifacts, and no PII is stored | `foundation` | `acquisition` | secret-scan report over tree, history, configs, logs and artifacts |
| TA-23 | Agent preflight passes: zero `TBD` in required config fields, all gate tests green, supervisor sign-off recorded | `foundation` | `fixtures-and-reproducibility` | `aws_ai_dlc_preflight_report` |
| TA-24 | This document has been checked against the current Vision version and marked superseded if the Vision changed | (none — document control) | — | authority-document version check; an author/supervisor task with no implementing unit |
| TA-25 | ICTP is excluded from training; the approved replacement's 2022 experiment/schema/cells/common timestamps pass G-P1A for all three coordinates, including F1–F4 and December | `inventory-and-registry` | `acquisition` | G-P1A evidence set incl. December coverage audit |
| TA-26 | TensorFlow/Keras is the only NN stack; exact pins install; deterministic seed utility and serialization restore pass locally and on Kaggle | `models-and-baselines` | `foundation`, `fixtures-and-reproducibility` | pins row, `tests/test_determinism.py`, serialization restore on both platforms |
| TA-27 | Phase 1 cannot import raw GNSS modules (first limb — Phase 1-applicable) and Phase 2 cannot change protected forecasting hashes (second limb — accepted at G-P2/G-P3C, not inside Phase 1) | `governance-guards` | `fixtures-and-reproducibility` | `tests/test_phase_boundary.py` + transition-manifest hash-diff test |
| TA-28 | All copied/adapted code has compatible licensing, notices, immutable provenance, modification logs, citations and passing adapter tests | `governance-guards` | — | `tests/test_reuse_registry.py`, §10.1 register rows |
| TA-32 | The replacement acquisition notebook runs only after D-144, retrieves the frozen prepared product, records permanent citations/requests/hashes, verifies schema/cells/common timestamps, and refuses training output until G-P1A passes | `acquisition` | `inventory-and-registry` | notebook run log, `request_manifest.json`, `sha256_manifest.json`, G-P1A refusal path |

**TA-24 has no implementing unit.** It requires this project's Technical
Environment document to be checked against the current Vision version and marked
superseded if the Vision changed. That is author and supervisor document control,
not pipeline work, and no unit can produce its evidence. Recorded as an
unassigned acceptance row rather than attached to a unit that does not own it.

## Per-unit coverage summary

| Unit | Requirements | Untested requirements | Acceptance rows as primary | Supporting on |
|---|---|---|---|---|
| `foundation` | 16 | 2 | TA-01, TA-02, TA-03, TA-10, TA-15, TA-22, TA-23 | TA-13, TA-26 |
| `governance-guards` | 10 | 1 | TA-27, TA-28 | WS-18, TA-07, TA-18 |
| `acquisition` | 15 | 7 | TA-32 | TA-15, TA-16, TA-22, TA-25 |
| `inventory-and-registry` | 7 | 2 | WS-01, TA-04, TA-25 | TA-32 |
| `target-standardization` | 6 | 1 | TA-19 | TA-15 |
| `external-products` | 7 | 5 | WS-09 | WS-10, WS-11, TA-08, TA-12 |
| `features-and-splits` | 11 | 4 | WS-10, WS-11, WS-12, WS-13, WS-18, TA-07, TA-08, TA-11, TA-18 | — |
| `models-and-baselines` | 9 | 7 | WS-14, WS-15, TA-12, TA-13, TA-26 | TA-20 |
| `evaluation-and-comparison` | 4 | 2 | WS-16 | TA-11, TA-18 |
| `statistical-inference` | 1 | 0 | WS-17, TA-14 | — |
| `regimes-diagnostics-reporting` | 11 | 7 | WS-19, TA-16, TA-20 | TA-19 |
| `fixtures-and-reproducibility` | 8 | 2 | WS-20, TA-09, TA-17, TA-21 | TA-03, TA-04, TA-23, TA-26, TA-27 |

Totals derived: 105 requirements across 12 units;
40 of them carry no acceptance row;
39 acceptance rows have a primary owner.

### Requirements with no acceptance row, by unit

These are the concrete input stage 3.2 (`nfr-requirements`) needs when it
assembles the G-05 freeze manifest, and stage 3.1 (`functional-design`) needs
when it plans verification. Each carries a real pass/fail criterion in
`requirements.md`; what is missing is a §16 or §19 row that tests it. Several are
candidates for a new TA row through Vision §15.2 change control.

- `foundation` (2): REQ-ENG-7, REQ-ENG-10
- `governance-guards` (1): FR-P1-02-6
- `acquisition` (7): FR-P1-01-5, FR-P1-01-7, FR-P1-01-8, FR-P1-01-9, FR-P1-01-11, REQ-NFR-A1, REQ-NFR-A2
- `inventory-and-registry` (2): FR-P1-02-7, FR-P1-02-8
- `target-standardization` (1): FR-P1-03-5
- `external-products` (5): REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-17, FR-P1-04-18
- `features-and-splits` (4): FR-P1-04-10, FR-P1-04-12, FR-P1-04-13, FR-P1-04-16
- `models-and-baselines` (7): FR-P1-04-14, FR-P1-05-3, FR-P1-05-4, FR-P1-05-5, FR-P1-05-6, FR-P1-05-21, FR-P1-05-22
- `evaluation-and-comparison` (2): FR-P1-05-7, FR-P1-05-17
- `regimes-diagnostics-reporting` (7): FR-P1-05-14, FR-P1-05-15, FR-P1-05-16, FR-P1-05-18, FR-P1-05-19, FR-P1-05-20, REQ-CLAIM-01
- `fixtures-and-reproducibility` (2): FR-WS-2, FR-WS-3

Units with full acceptance coverage: `statistical-inference`.

**No amendment is proposed here.** If closing one of these gaps requires
amending a governed WS or TA artifact, the proposed amendment is recorded and
approved by the authorized project decision owner before the new criterion is
treated as official.

## Cross-unit responsibilities

Where a requirement or acceptance row spans units, the primary owner is named in
the tables above and the crossing is recorded here.

| Item | Primary | Also involves | Why it crosses |
|---|---|---|---|
| FR-P1-05-12, WS-18, TA-18 (locked-test guard) | `features-and-splits` (test + execution limb) | `governance-guards` (`locked_test.py`, the access-log limb) | ADR-03 splits the guard deliberately into a path/access limb and an execution limb. `tests/test_locked_test_guard.py` exercises both; assigning it to `governance-guards` would close a cycle, since `features-and-splits` already depends on that unit. |
| FR-P1-04-1, NFR-IRI-01, WS-10, TA-07 (IRI denial) | `features-and-splits` | `governance-guards` (independent import-limb check), `external-products` (the products denied entry) | The raise lives at `features.build_features`; the import-boundary check has no owning §12 module and is carried as an independent check. |
| NFR-PHASE-01, TA-27 (phase boundary + protected hashes) | `governance-guards` (first limb) | `fixtures-and-reproducibility` (the hash-diff test's evidence) | The transition-manifest hash-diff test has no §12 module and needs frozen artifacts from every earlier unit. Its second limb is accepted at G-P2 and G-P3C, outside Phase 1. |
| REQ-ENG-5 (a negative-path test per hard rule) | `governance-guards` | `features-and-splits`, `models-and-baselines`, `fixtures-and-reproducibility` | A property of the whole suite; its test links (WS-10, TA-07, TA-08, TA-12, TA-27) spread across four units. |
| REQ-ENG-8 (migrating the two existing scripts and the coverage notebook) | `foundation` | `external-products` (`audit_ec1_drivers.py`), `inventory-and-registry` (`merge_coverage_year.py`), `regimes-diagnostics-reporting` (the coverage notebook) | The scaffold is the migration target; the migrated artifacts land in three other units. |
| NFR-DQ-01, FR-P1-05-10, TA-19 (target uncertainty budget) | `target-standardization` (produces it) | `regimes-diagnostics-reporting` (reports it adjacent to the primary result) | Production and adjacent reporting are separate obligations in the same requirement family. |
| NFR-DET-01, TA-13, TA-26 (controlled randomness) | `foundation` (seeds, `seed_everything`, `test_determinism.py`) | `models-and-baselines` (the three-seed mean), `statistical-inference` (the carved-out bootstrap seed) | ADR-05 centralises determinism and carves out the bootstrap seed on purpose. |
| FR-P1-01-10, NFR-SEC-01, TA-22 (credentials and secrets) | `foundation` | `acquisition` (the consumer that reaches the provider client) | The mechanism is environment and platform-secret-store resolution; the consumer is acquisition. |

## Open verification gaps and their owners

Five of these carry a blocker ID. `unit-of-work.md` § Blocker register holds the
full record for each — affected artifacts, owning unit, downstream units,
required resolution, approval authority and status — and the roll-up showing
which unit's scope each one blocks. Repeated here only as verification gaps,
because that is what this artifact tracks.

| Gap | Blocker | Owner | Status |
|---|---|---|---|
| ADR-10's four-part §12/§13.2 amendment is unsigned; `config.py`, `locked_test.py`, `test_determinism.py` and the `PYTHONHASHSEED` clean-run clause have no authority backing | **BLK-01** | Student + Supervisor | Open. `code-generation` must not create these on the strength of ADR-10 alone. |
| § Known defects row 12 — the `plumbing_7day` station count — blocks that fixture's manifest | **BLK-02** | Supervisor | Open. `fixtures-and-reproducibility` cannot state the fixture identity until it is resolved, and no manifest may be invented, inferred or substituted. |
| `three_seed_mean` has no frozen-seed-set parameter, so it can only be implemented by inlining `{1337, 2024, 7}` (forbidden) or by a weaker distinctness check | **BLK-03** | `models-and-baselines`, via `functional-design`; seed values Supervisor (D-122) | Open, carried from the advisory review of `component-methods.md`. Reaches `evaluation-and-comparison`, `statistical-inference` and `regimes-diagnostics-reporting` downstream. |
| `fit_transforms` types `train` as an unconstrained DataFrame, so the full-dataset fit remains representable | **BLK-04** | `features-and-splits`, via `functional-design`; leakage evidence Supervisor at G-04/G-05 | Open, carried from the advisory review of `component-methods.md` and ADR-01. Reaches every unit downstream of features, since every reported number inherits the fit — including `fixtures-and-reproducibility`, whose clean-run tolerance comparison and TA-21 traceability matrix consume those artifacts. BLK-03 reaches it the same way. |
| The D-17 target-schema test implied by FR-P1-03-5 has no module name and no §12 tree entry | **BLK-05** | `functional-design` names it; the tree amendment is Supervisor | Open. This stage chooses no name. |
| FR-P1-05-18: no criterion tests that the storm-event count comes from GFZ Kp/Hp60 at a recorded release grade | — | `regimes-diagnostics-reporting`; the criterion itself is a `requirements.md` change | Open, advisory NOT-READY carried from stage 2.3. |
| 40 requirements carry no §16/§19 row | — | stages 3.1 and 3.2 | Open by design; enumerated per unit above. |
| TA-24 has no implementing unit | — | author / supervisor document control | Open; recorded rather than assigned. |
| D-122's sign-off still pending per Vision §14.2 | — (input to BLK-03) | Supervisor | Open. |
| The one-month all-station scientific fixture window is unfrozen under Q-31 | — | Student | Open. |
| The AGPLv3 Global-TEC-forecasting distribution question | — | outside this project | Open; the standing default is reimplementation from the paper with a citation. |

## Assumptions & Open Questions

- **[assumption]** Table 1 assigns each requirement to exactly one primary unit even where two units contribute; § Cross-unit responsibilities carries the crossings. The alternative — two owners per requirement — would have made both-direction coverage uncheckable.
- **[assumption]** TA-27 is listed in Table 2 although `requirements.md` § Success and acceptance places it under "evaluated at the phase boundary" rather than in the enumerated 26. Its first limb (Phase 1 cannot import raw GNSS modules) is Phase 1-applicable and carried by FR-P1-03-2, so omitting the row entirely would leave that limb without an evidence owner.
- **Open.** No requirement or acceptance row was added, reworded or reinterpreted here. Every gap above is carried forward, not closed.
- **Correction applied on the second attempt, affecting the companion artifacts and not these tables.** The first attempt described `fixtures-and-reproducibility`'s nine incoming dependencies as reaching "all nine script-owning units". Only seven of the nine own a stage script the clean-run sequence invokes; `statistical-inference` and `regimes-diagnostics-reporting` own none — both are `embedded` and run inside `07_evaluate_and_report.py`, which `evaluation-and-comparison` owns — so their edges rest on the artifacts the clean-run comparison and TA-21's traceability matrix consume. `unit-of-work.md` § 12 and `unit-of-work-dependency.md`'s edge table now state both reasons separately. No requirement assignment, acceptance-row owner or coverage count in this artifact changes: the DAG is still 12 units and 23 edges, still acyclic.
- **None** of the above adopts a reading on a supervisor-owned value.
