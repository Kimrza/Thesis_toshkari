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

- Requirements: `../requirements-analysis/requirements.md` — the 105 requirement rows mapped in Table 1, and the untested list — 40 rows when this artifact was written, **36 since TA-33…TA-36 were approved on 2026-08-22**.
- Design: `../application-design/components.md` (which module carries which requirement), `../application-design/component-methods.md` (the boundary calls acceptance evidence is asserted against), `../application-design/services.md` (the nine stage scripts and the ordering contract), `../application-design/component-dependency.md` (the forbidden edges and their tests), `../application-design/decisions.md` (ADR-03's split guard, ADR-09's Phase 2 boundary, ADR-10's §12/§13.2 amendment — unsigned when this artifact was first written, **approved and applied 2026-08-22** under `CR-2026-08-22-TE-AMEND`).
- Acceptance vocabulary: TE §16 (WS-01…WS-20) and TE §19 (TA-01…TA-36, the last four added 2026-08-22 under `CR-2026-08-22-LEAKAGE-TA`), with Phase 1 applicability fixed by FR-WS-4 and `requirements.md` § Success and acceptance.
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
| FR-P1-04-12 | `features-and-splits` | TA-33 |
| FR-P1-04-13 | `features-and-splits` | TA-34 |
| FR-P1-04-14 | `models-and-baselines` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-04-15 | `external-products` | **NO CURRENT ACCEPTANCE ROW** |
| FR-P1-04-16 | `features-and-splits` | TA-35 |
| FR-P1-04-17 | `external-products` | TA-36 |
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

**Derived when this artifact was written, and re-derived 2026-08-22:** **13 WS
rows and 31 TA rows** mapped (30 enumerated Phase 1-applicable TA rows plus
TA-27's first limb) — **44 acceptance rows in total**, of which **43** have an
evidence-producing unit and **1** (TA-24) does not.

**The change, 2026-08-22.** TA-33, TA-34, TA-35 and TA-36 were approved under
Vision §15.2 (`CR-2026-08-22-LEAKAGE-TA`) as negative-path controls for the four
leakage-sensitive requirements FR-P1-04-12, -13, -16 and -17. TA rows moved
**27 → 31**, total acceptance rows **40 → 44**, and requirements with no
acceptance row **40 → 36**. Every figure was recomputed from these tables rather
than adjusted by hand.

**All four carry status `Pending` in TE §19.** A requirement now having an
acceptance criterion is not a test being implemented, not a test being executed,
and not a test passing. No module exists for any of the four, and their placement
is assigned at functional design.

| Row | What it checks | Evidence-producing unit | Supporting | Evidence |
|---|---|---|---|---|
| WS-01 | Station registry is populated from official site logs with pinned IGRF coordinates; header cross-check shows no unresolved conflict | `inventory-and-registry` | — | `tests/test_station_registry.py`, registry artifact + site-log diff |
| WS-09 | IRI benchmark and GIM comparator sample alignment passes; IRI ceiling and drivers are recorded; GIM overlap audit is present | `external-products` | — | benchmark/comparator manifests, `gim_network_overlap_flag` audit, `iri_implementation_validation` report |
| WS-10 | The IRI-denial test fails when an `iri_*` field is deliberately injected into the ML feature path | `features-and-splits` | `external-products` | `tests/test_iri_denial.py` — must fail on deliberate injection |
| WS-11 | Availability lag assertions pass for every primary feature; F10.7 mean is trailing; Dst is diagnostic-only; SSN is absent | `features-and-splits` | `external-products` | `tests/test_feature_availability.py`, availability matrix, driver manifests |
| WS-12 | F1–F4 splits and the 24 h embargo produce no window crossing a boundary; first 24 h are excluded and counted | `features-and-splits` | — | `tests/test_split_embargo.py`, fold manifests with excluded-row counts |
| WS-13 | Flattened matrix and sequence tensor for a given feature-set ID contain the same underlying window values | `features-and-splits` | — | matched-window parity assertion over one `windows.py` definition — **departs from TE §16's stated evidence for this row, which names `test_common_masks.py`** (owned by `evaluation-and-comparison`, not by this row's evidence-producing unit). The substitution is defensible, parity being a `windows.py` property, but no reading is adopted here and the departure is recorded rather than resolved: see § Open verification gaps. Pre-existing; surfaced 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 12 |
| WS-14 | M-01, M-02, M-03, M-04, M-05 predictions run | `models-and-baselines` | — | `tests/test_models_smoke.py`, per-model prediction artifacts |
| WS-15 | Minimal M-06 trains and restores its lowest-validation-RMSE checkpoint | `models-and-baselines` | — | `tests/test_checkpoint_restore.py`, checkpoint artifact |
| WS-16 | Comparison-wide intersection masks are stored with stable IDs and row counts; no pairwise mask is produced | `evaluation-and-comparison` | — | `tests/test_common_masks.py`, mask registry with stable IDs |
| WS-17 | Vector time-block bootstrap carries all stations together and reproduces exactly from seed 20221201 | `statistical-inference` | — | `tests/test_bootstrap.py`, replicate hash from seed 20221201 |
| WS-18 | Locked-test guard blocks December performance execution before G-05 and records access | `features-and-splits` | `governance-guards`, `inventory-and-registry` | `tests/test_locked_test_guard.py`, access-log sample, `locked_test_accessed` registry flag |
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
| TA-18 | Locked-test guard prevents December performance execution before G-05; predictions are hashed before metrics; registry records all access | `features-and-splits` | `governance-guards`, `evaluation-and-comparison`, `inventory-and-registry` | guard test + access-log sample + prediction hash preceding any metric |
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
| TA-33 | **Leakage-sensitive negative control (FR-P1-04-12).** A field outside the §6.2 dictionary injected into feature construction **raises**; an `experiment.yaml` placing the window length in a grid **fails** | `features-and-splits` | — | Executed negative-path test output showing both rejections; feature manifest enumerating only §6.2 fields; window length 24, absent from every grid |
| TA-34 | **Leakage-sensitive negative control (FR-P1-04-13).** A carried-forward `vtec_lag_*` value **fails**; an incomplete `vtec_seq_24` window is **excluded and counted** | `features-and-splits` | — | Executed negative-path test output showing both behaviours; feature manifest carrying lags `[1,2,3,24]`, the 24-step sequence, station one-hot and verified latitude; excluded-window count |
| TA-35 | **Leakage-sensitive negative control (FR-P1-04-16).** A support field used as a model input with no recorded G-04 approval ID **fails**; one read at or beyond hour *t* **fails** | `features-and-splits` | — | Executed negative-path test output showing both rejections; feature manifest marking every support field diagnostic unless an approval ID is present |
| TA-36 | **Leakage-sensitive negative control (FR-P1-04-17, D-10.2).** A Kp value repeated outside its own 3-hour interval **fails**; a Dst value shifted to a neighbouring hour **fails**; no interpolation call exists on any driver series | `external-products` | `features-and-splits` (the enforcement raise sits at `features.build_features`) | Executed negative-path test output carrying both negative controls; driver manifests recording per-series interval semantics; the no-interpolation check result |

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
| `inventory-and-registry` | 7 | 2 | WS-01, TA-04, TA-25 | WS-18, TA-18, TA-32 |
| `target-standardization` | 6 | 1 | TA-19 | TA-15 |
| `external-products` | 7 | 4 | WS-09, TA-36 | WS-10, WS-11, TA-08, TA-12 |
| `features-and-splits` | 11 | 1 | WS-10, WS-11, WS-12, WS-13, WS-18, TA-07, TA-08, TA-11, TA-18, TA-33, TA-34, TA-35 | TA-36 |
| `models-and-baselines` | 9 | 7 | WS-14, WS-15, TA-12, TA-13, TA-26 | TA-20 |
| `evaluation-and-comparison` | 4 | 2 | WS-16 | TA-11, TA-18 |
| `statistical-inference` | 1 | 0 | WS-17, TA-14 | — |
| `regimes-diagnostics-reporting` | 11 | 7 | WS-19, TA-16, TA-20 | TA-19 |
| `fixtures-and-reproducibility` | 8 | 2 | WS-20, TA-09, TA-17, TA-21 | TA-03, TA-04, TA-23, TA-26, TA-27 |

Totals re-derived 2026-08-22: 105 requirements across 12 units;
**36** of them carry no acceptance row;
**43** acceptance rows have a primary owner (44 mapped; TA-24 has none).

Changed 2026-08-22 by the addition of TA-33…TA-36: untested **40 → 36**, TA rows
**27 → 31**, total acceptance rows **40 → 44**, `features-and-splits` untested
**4 → 1**, `external-products` untested **5 → 4**. Every figure recomputed from
the tables above.

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
- `external-products` (4): REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18
- `features-and-splits` (1): FR-P1-04-10
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
| FR-P1-02-3, WS-18, TA-18 (the **permitted** G-05 December coverage audit) | `inventory-and-registry` (performs the audit) | `governance-guards` (`open_restricted`, which writes the access-log row), `features-and-splits` (owns the guard test both limbs run through) | `inventory-and-registry` performs the pre-G-05 December coverage and regime audit — a **permitted** read, required by Vision §8.3 and performance-blind — through `governance-guards.open_restricted`. **An access-log row carrying `locked_test_accessed = true` must exist before the first December record is read**; FR-P1-02-3's scope is *access*, unqualified, so it covers derived-artifact merges, re-derivations, corrections, coverage recounts and schema validations, not only a model execution. This is a **different event** from WS-18's execution-guard scenario, which blocks *unauthorized* December performance execution before G-05. The unit responsible for producing the access evidence is `inventory-and-registry`; the authority that approves G-05 itself is the **Supervisor** — evidence ownership and gate approval are not the same thing and are not merged here. Added 2026-08-22 per governance finding `UG-03`. **This row assigns evidence ownership only and creates no test coverage: permitted-read access logging is NOT TESTED**, tracked as `RES-01` in `unit-of-work.md` § Residual governance obligations, with its candidate §19 criterion owned by stage 3.2 under Vision §15.2. |
| FR-P1-04-1, NFR-IRI-01, WS-10, TA-07 (IRI denial) | `features-and-splits` | `governance-guards` (independent import-limb check), `external-products` (the products denied entry) | The raise lives at `features.build_features`; the import-boundary check has no owning §12 module and is carried as an independent check. |
| NFR-PHASE-01, TA-27 (phase boundary + protected hashes) | `governance-guards` (first limb) | `fixtures-and-reproducibility` (the hash-diff test's evidence) | The transition-manifest hash-diff test has no §12 module and needs frozen artifacts from every earlier unit. Its second limb is accepted at G-P2 and G-P3C, outside Phase 1. |
| REQ-ENG-5 (a negative-path test per hard rule) | `governance-guards` | `features-and-splits`, `models-and-baselines`, `fixtures-and-reproducibility` | A property of the whole suite; its test links (WS-10, TA-07, TA-08, TA-12, TA-27) spread across four units. |
| REQ-ENG-8 (migrating the two existing scripts and the coverage notebook) | `foundation` | `external-products` (`audit_ec1_drivers.py`), `inventory-and-registry` (`merge_coverage_year.py`), `regimes-diagnostics-reporting` (the coverage notebook) | The scaffold is the migration target; the migrated artifacts land in three other units. |
| NFR-DQ-01, FR-P1-05-10, TA-19 (target uncertainty budget) | `target-standardization` (produces it) | `regimes-diagnostics-reporting` (reports it adjacent to the primary result) | Production and adjacent reporting are separate obligations in the same requirement family. |
| NFR-DET-01, TA-13, TA-26 (controlled randomness) | `foundation` (seeds, `seed_everything`, `test_determinism.py`) | `models-and-baselines` (the three-seed mean), `statistical-inference` (the carved-out bootstrap seed) | ADR-05 centralises determinism and carves out the bootstrap seed on purpose. |
| FR-P1-01-10, NFR-SEC-01, TA-22 (credentials and secrets) | `foundation` | `acquisition` (the consumer that reaches the provider client) | The mechanism is environment and platform-secret-store resolution; the consumer is acquisition. |
| FR-P1-04-17, TA-36 (driver alignment) | `external-products` — **upstream data production** | `features-and-splits` — **enforcement and the primary negative-path acceptance test** | **Reconciled 2026-08-22.** This artifact assigned the requirement to `external-products` while `unit-of-work-dependency.md` put the enforcement raise in `features.build_features`, owned by `features-and-splits`. Both were right about different things. Four ownerships are now distinguished: **data production** (`external-products` — driver series carrying their own interval semantics, no interpolation at any stage); **enforcement** (`features-and-splits` — the raise at `features.build_features`); **primary acceptance test** (`features-and-splits` — TA-36, sited at the feature-building enforcement boundary in `tests/test_feature_leakage_guards.py`); and **upstream evidence / data-contract responsibility** (`external-products` — driver manifests recording per-series interval semantics and release grade, with any upstream contract test documented separately and **not** replacing the primary rejection test). This allocation is the **default** and stands unless functional design produces verified evidence for a better one; if it reallocates, it updates **both** artifacts. Full table in `unit-of-work-dependency.md` § "FR-P1-04-17 — ownership reconciliation". |

## Open verification gaps and their owners

Seven of these carry a blocker ID (BLK-01 through BLK-07); **BLK-01 is closed** and its row is
retained as a closed row so the record is not lost. `unit-of-work.md` § Blocker register holds the
full record for each — affected artifacts, owning unit, downstream units,
required resolution, approval authority and status — and the roll-up showing
which unit's scope each one blocks. Repeated here only as verification gaps,
because that is what this artifact tracks.

| Gap | Blocker | Owner | Status |
|---|---|---|---|
| ADR-10's four-part §12/§13.2 amendment was unsigned; `config.py`, `locked_test.py`, `test_determinism.py` and the `PYTHONHASHSEED` clean-run clause had no authority backing | **BLK-01** | Project owner, under the recorded student/supervisor authority equivalence | **Closed 2026-08-22** (`CR-2026-08-22-TE-AMEND`, TE v3.4). **Authority only** — none of the four modules exists, and `code-generation` must not create any of them before **G-09** and stage 3.5. |
| `acquisition` reads and writes under `evidence/locked_test_restricted/` — the D-9 input `audit_evidence_2022-FULL/` and any December re-acquisition — without a contract routing that access through `governance-guards.open_restricted`, contradicting `component-dependency.md` § Shared resources ("nothing else may construct a path into it") and D-15's rule that any consumer opening FULL must write an access-log row first | **BLK-07** | `acquisition`, via `functional-design` (3.1) | Open. **Exit** condition on 3.1, and **no acquisition run may touch calendar 2022-12** while it stands. Registered 2026-08-22 per finding `UG2-01` (`GOV-2026-08-22-UG-02`). |
| `requirements.md` § Known defects row 12 — the `plumbing_7day` **station selection** blocks that fixture's manifest | **BLK-02** | Project owner under Q-31 | **Station-selection limb RESOLVED 2026-08-22 — BSHM 32/35 (D-20)**, selected on the only complete observed coverage of D-11's window (168/168 hourly bins, 7/7 days, 1,810 records). The reading limb was settled earlier by the D-11 clarification of 2026-08-22 (§15.1's one-station execution scope retained). **Still PENDING:** the fixture manifest does not exist, the fixture has never been run, and **no measured value — row count, tolerance, support or missingness limit, timestamp tolerance or CPU runtime range — exists or is claimed.** Selecting a station supplies identity, not content; **no manifest may be invented, inferred or substituted.** ARUC's one-bin shortfall on five of seven days is **dormant, not discharged** — it attaches to ARUC, which is not selected, and revives only if ARUC is later chosen. |
| `three_seed_mean` has no frozen-seed-set parameter, so it can only be implemented by inlining `{1337, 2024, 7}` (forbidden) or by a weaker distinctness check | **BLK-03** | `models-and-baselines`, via `functional-design`; **seed values closed 2026-08-22** (D-122) | Open **on the contract limb**; an **exit** condition on stage 3.1. D-122's sign-off closed 2026-08-22 with values verified unchanged (development seed 42 and final seeds {1337, 2024, 7}. The bootstrap seed **20221201** is frozen separately by TE §13.6 / TC-19 (Q-27) and is **not** part of D-122’s item set — attribution corrected 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 11) — **authority only: the values reach `three_seed_mean` from `ConfigSnapshot.seeds` via `configs/seeds.yaml` and must never be inlined in `src/models` or any other implementation file** (TC-03e). Carried from the advisory review of `component-methods.md`. Reaches `evaluation-and-comparison`, `statistical-inference` and `regimes-diagnostics-reporting` downstream. |
| `fit_transforms` types `train` as an unconstrained DataFrame, so the full-dataset fit remains representable | **BLK-04** | `features-and-splits`, via `functional-design`; leakage evidence Supervisor at G-04/G-05 | Open. **Exit condition on stage 3.1, not an entry condition** (`GOV-2026-08-22-REM-01` Rec 2): the affected units **may enter** 3.1, **may not complete or exit** it without the approved contract, and **no implementation may proceed** while it stands. The leakage safeguard is unchanged — per-fold train-only fitting on the named fold's training partition only, with a `LeakageError` when `train`'s index is not a subset of that partition. (This row carried no entry/exit statement until 2026-08-22, when the ruling reached the register and the per-unit lines but not this table; corrected per `GOV-2026-08-22-UG-02` Rec 1.) Carried from the advisory review of `component-methods.md` and ADR-01. Reaches every unit downstream of features, since every reported number inherits the fit — including `fixtures-and-reproducibility`, whose clean-run tolerance comparison and TA-21 traceability matrix consume those artifacts. BLK-03 reaches it the same way. |
| The D-17 target-schema test implied by FR-P1-03-5 has no module name and no §12 tree entry | **BLK-05** | Project decision owner; §12 tree amendment | **Naming and documentation limbs RESOLVED 2026-08-22 — `tests/test_prepared_target_schema.py`** (`CR-2026-08-22-TARGET-SCHEMA-TEST`). **Implementation and execution PENDING**: the module does not exist and has never been run. FR-P1-03-5 remains untested — naming a module is not adding an acceptance row. |
| FR-P1-05-18: no criterion tests that the storm-event count comes from GFZ Kp/Hp60 at a recorded release grade | — | `regimes-diagnostics-reporting`; the criterion itself is a `requirements.md` change | Open, advisory NOT-READY carried from stage 2.3. |
| 40 requirements carry no §16/§19 row | — | stages 3.1 and 3.2 | Open by design; enumerated per unit above. |
| TA-24 has no implementing unit | — | author / supervisor document control | Open; recorded rather than assigned. |
| ~~D-122's sign-off still pending per Vision §14.2~~ | — (input to BLK-03) | Project owner, under the recorded student/supervisor authority equivalence | **Closed 2026-08-22** (Vision §14.2; `CR-2026-08-22-TE-AMEND`; `GOV-2026-08-22-REM-01` Rec 4). Seed values verified unchanged before closure: development seed 42 and final seeds {1337, 2024, 7}. The bootstrap seed **20221201** is frozen separately by TE §13.6 / TC-19 (Q-27) and is **not** part of D-122’s item set — attribution corrected 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 11. **Authority only** — the values reach `three_seed_mean` as a parameter from `ConfigSnapshot.seeds` via `configs/seeds.yaml` and **must never be inlined in `src/models` or any other implementation file** (TC-03e). BLK-03's contract limb stays open. |
| ~~The one-month all-station scientific fixture window is unfrozen under Q-31~~ | — | — | **Closed.** Frozen as **D-14** — March 2022, all three cells — by `CR-2026-08-21-FREEZES`, carrying the mandatory limitation that March is an equinox month reproducing neither December's winter-solstice regime nor its activity distribution. Corrected 2026-08-22 per finding `UG-08`; an earlier revision of this artifact carried it open after the freeze. |
| **`RES-03`** — the canonical protected set. Registered 2026-08-22 per finding `UG-01` because FR-P1-06-1 required a "fourteen-item enumeration" with no stated deduplication rule, while three §7.0B immutables — **history window**, **station encoding**, **baselines** — mapped onto none of its items | **BLK-06** | Enumeration approved by the project decision owner; FR-P1-06-1 amended under Vision §15.2; implementation owned by `governance-guards` via `functional-design` (3.1) | **Enumeration limbs RESOLVED 2026-08-22; implementation limb OPEN.** The canonical set is frozen as **D-24**: the deduplicated union of TE §2.2 (12 items) and §7.0B (16), with the three unmapped items added explicitly — **17 items, the cardinality calculated from the enumeration, not assumed**. `baselines` is enumerated to M-01, M-02, M-03, **B-01 IRI-2016 with its 2000 km ceiling**, and C-01 CODE GIM. FR-P1-06-1 amended 14 → 17 under `CR-2026-08-22-PROTECTED-SET`. **Still PENDING:** per-item binding to concrete config fields (no config file exists), and the implementation of `protected_hashes` / `diff_protected_hashes` — not written, not executed, gated by G-09. Until the implementation limb closes, an empty `diff_protected_hashes` result still cannot be read as proof that no protected item changed. |
| **`RES-01` — no dedicated acceptance criterion covers access logging for a *permitted* December read.** WS-18 and TA-18 test the execution guard ("blocks December performance execution before G-05 and records access"); the pre-G-05 coverage audit is a permitted read by a different unit. Adding `inventory-and-registry` to those rows' Supporting column assigns evidence ownership — it does **not** create a criterion that tests permitted-read logging. **This scenario is NOT TESTED** | — | `inventory-and-registry` performs the read; criterion authored by stage **3.2** (`nfr-requirements`), routed through **Vision §15.2** change control and the G-05 freeze-manifest workflow | **Ownership remediated; dedicated test coverage open.** Registered 2026-08-22 per finding `UG-03` option C. **No TA row is added or approved here** — the required §15.2 authority is not available in this stage — and the 40-row untested count is unchanged: FR-P1-02-3 keeps its existing `WS-18, TA-25` test row and does not move into the untested list. The future criterion must distinguish permitted coverage-audit access from prohibited pre-G-05 performance execution and must assert `locked_test_accessed = true` is written before the first December record is read. UG-03's durable test gap is **not** closed. |
| **WS-13's evidence departs from TE §16 without a recorded reading.** Table 2 gives "matched-window parity assertion over one `windows.py` definition"; TE §16's WS-13 row names `test_common_masks.py`, owned by `evaluation-and-comparison` while WS-13's evidence-producing unit is `features-and-splits`, and WS-13 carries no Supporting entry. Two defensible readings exist — name §16's module and add the Supporting unit, or keep the parity assertion and record why it substitutes — and **this stage adopts neither**, the choice being about which evidence actually tests WS-13 | — | stage **3.1** (`functional-design`), which owns verification planning; any change to §16's evidence column runs through Vision §15.2 | Open. Pre-existing — **not** introduced by either 2026-08-22 remediation round. Registered 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 12 option 3, the human decision being expressly deferred rather than taken. |
| The AGPLv3 Global-TEC-forecasting distribution question | — | outside this project | Open; the standing default is reimplementation from the paper with a citation. |

## Assumptions & Open Questions

- **[assumption]** Table 1 assigns each requirement to exactly one primary unit even where two units contribute; § Cross-unit responsibilities carries the crossings. The alternative — two owners per requirement — would have made both-direction coverage uncheckable.
- **[assumption]** TA-27 is listed in Table 2 although `requirements.md` § Success and acceptance places it under "evaluated at the phase boundary" rather than in the enumerated 26. Its first limb (Phase 1 cannot import raw GNSS modules) is Phase 1-applicable and carried by FR-P1-03-2, so omitting the row entirely would leave that limb without an evidence owner.
- **Open.** No requirement or acceptance row was added, reworded or reinterpreted here. Every gap above is carried forward, not closed.
- **Correction applied on the second attempt, affecting the companion artifacts and not these tables.** The first attempt described `fixtures-and-reproducibility`'s nine incoming dependencies as reaching "all nine script-owning units". Only seven of the nine own a stage script the clean-run sequence invokes; `statistical-inference` and `regimes-diagnostics-reporting` own none — both are `embedded` and run inside `07_evaluate_and_report.py`, which `evaluation-and-comparison` owns — so their edges rest on the artifacts the clean-run comparison and TA-21's traceability matrix consume. `unit-of-work.md` § 12 and `unit-of-work-dependency.md`'s edge table now state both reasons separately. No requirement assignment, acceptance-row owner or coverage count in this artifact changes: the DAG is still 12 units and 23 edges, still acyclic.
- **None** of the above adopts a reading on a supervisor-owned value.
