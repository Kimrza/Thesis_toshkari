# Code Generation Plan — `fixtures-and-reproducibility`

**Unit** `fixtures-and-reproducibility` (Bolt 12 — the last unit, the DAG's terminal node) · **Kind** `library` · **Stage** `code-generation`
**Inputs**: `functional-design/` (W-1…W-10; R-133…R-142; entities 1–7; 39 negative controls + 11 must-not-fire, derived there), `nfr-design/` (SD-X-01…SD-X-03; components F1–F7), `nfr-requirements/` (SEC-X-01…04; TS-X-01…05), `unit-of-work.md` § 12 (Owns: `scripts/run_walking_skeleton.py`; the two `fixture_manifest.yaml`s; `tests/test_clean_run.py`; the traceability matrix and `environment_and_cpu_preflight_report`; execution of the M10 contract fixture), `requirements.md` (FR-WS-1…6, NFR-REP-01, REQ-NFR-A3 carried; REQ-ENG-4 and FR-WS-7 discharge onto this unit's rows but are `foundation`'s). Consumed code: `src/data/config.py` (`ConfigSnapshot`, `load_configs`, `assert_no_tbd`, `assert_declared_sources_exist`, `resolve_platform_roots`, `capture_environment_lock`, `assert_lock_complete`, `ensure_process_determinism`, the `IntegrityError` hierarchy), `src/data/release.py` (`sha256_of_file` — the single hashing home), `src/data/experiment_registry.py` (`append_registry_event`), `src/data/splits.py` (`PARTITION_IDS`, `FITTING_PARTITION_IDS`, `REFIT_ID`, `LOCKED_ID`), `src/data/acquisition.py` (R-31 record-date membership), `src/data/phase_contract.py` (`assert_phase_boundary`), `src/features/transforms.py` (`assert_transform_identity`), the seven Phase 1 stage scripts, `tests/test_acquisition_window.py`, `tests/test_train_only_transforms.py`, `tests/test_split_embargo.py`, `evidence/audit_evidence_2022-11/`, `evidence/audit_evidence_2022-03/`.
**Answers (receipted)**: Q1 = A (build the apparatus now, blockers as checked refusals), Q2 = A (loader in `src/data/fixture_manifest.py`; amendment ledger +1 owed), Q3 = A (§15.2 `not_applicable` reading), Q4 = A (fixture scale via apparatus partitions; `05`/`06`/`07` gain `--fixture-manifest`), Q5 = A (`require_fixture_receipts` in all seven scripts' `_stage_entry`, exempt on fixture runs), Q6 = A (base `IntegrityError`; receipts as registry rows; `fixture_bootstrap` as apparatus constants).
**Authority**: TE §9.1/§9.2 (both fixtures before any full-year job; in-session rule), §13.1 (eight lock items), §13.2 as amended (`PYTHONHASHSEED=0`; the seven Phase 1 invocations; Phase 2 deferred to G-P2), §13.7 (exact classes; no silent update), §15.1–§15.4, §18.3 (stop-and-report); D-11 (window; limitation; provisional-Dst restriction), D-14 (March 2022; limitation in both clauses), D-20 (BSHM 32/35), D-28, D-29, D-31; TC-01, TC-03f, TC-03g. G-05/G-06/G-07 `Blocked`; **BLK-02 open on implementation; BLK-08 ↓ mechanism limb open; BLK-03/04/09 contracts approved by change record.**

## Ground rules binding every step

Same as prior units (Python 3.11; in-place edits, no duplicates; no scientific constant in
source — window, station, month, seeds, partitions, thresholds reach code ONLY from
`configs/`, the frozen D-number records, or the fixture manifest; two-tier errors — an
integrity violation raises naming file and violated expectation, a completeness shortfall is a
machine-readable field; docstrings stating purpose, inputs, re-run behaviour; ruff or the
stdlib substitute; **a negative control per hard rule, pushed through the real entry point**
(nfr-design:c58/c59 — the regimes-diagnostics-reporting iteration-2 finding is the fresh
example of a guard with no call site); nothing discharged; smoke ≠ governed; **no commit**).
Plus this unit's own: **no measured value is stated, inferred or substituted anywhere** —
every row-count range, tolerance, runtime and storage figure exists only as a manifest field
carrying its measuring run's registry id, and **no `fixture_manifest.yaml` is authored by
hand**: neither fixture tree receives a manifest this pass (BLK-02; the freeze acts are the
owner's under Q-31); ONE schema and ONE validating loader, the only read path — a second YAML
parse of a fixture manifest anywhere in `src/`, `scripts/` or `tests/` fails an only-copy
check; identity by citation (D-11/D-14/D-20), never re-derived; `status: candidate | frozen`
with the human act between and nothing here writing `frozen`; every evidence emitter refuses a
`candidate` manifest; `evidence_class: smoke_only` stamped by the producing path on every
`plumbing_7day` artifact and its absence asserted on every evidence surface; `data07_caveat`
and `december_representativeness: not_representative` on every fixture-derived figure, both
fixtures; December excluded on RECORD DATES (consuming R-31 and `test_acquisition_window.py`'s
predicate, no third copy); apparatus partition ids quarantined both ways from the six frozen
ids; exactly TWO receipts (the M10 result is clean-run evidence, never a third); the clean run
executes §13.2's Phase 1 enumeration verbatim in order on CPU with no GPU visible, the Phase 2
segment deferred to G-P2 and a Phase-2-only invocation raising `PhaseBoundaryError`; `exact`
classes compared by equality and never updated; TECU tolerance for an output whose producing
path declares no inverse route refused (BLK-08 ↓ checked, control 25); the three evidence
artifacts generated, never hand-assembled; `aws_ai_dlc_preflight_report` is `foundation`'s and
is built nowhere here; TA-27 first-limb only; no import of `src/external/iri.py` or `gim.py`;
`re-implements no hashing` — `release.sha256_of_file` is the only digest.

**What this pass cannot make run (TE §18.3, stated once here and in every affected
docstring)**: `configs/experiment.yaml` `folds`/`embargo_hours` and `configs/data.yaml`
`stations`/`cell_rule` are `TBD — freeze gate`, so every stage entry — including
`run_walking_skeleton.py`'s — refuses at `assert_no_tbd` today and writes an `aborted` registry
row; the plumbing fixture's §15.3 minimal M-06 refuses on the unfrozen TensorFlow pin; and this
clone has no `numpy`/`pandas`/`pyyaml`/`pytest`. The clean-run completion test therefore
SKIPS with the named stop-and-report reason (never passes on an abort, never fails the
suite for a gate the owner has not signed), and WS-20/TA-09/TA-17/TA-21 stay `Pending`.

## Steps

- [x] **Step 1 — Change record FIRST: `governance/CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md`** [Q1–Q6]
  The blocker state limb by limb (BLK-03/04/09 approved — records cited; BLK-08 mechanism limb
  open — D-27 unreopened, checked by control 25; BLK-02 open — no manifest, no run, no measured
  value); Q2's loader home with the amendment ledger **+1 → 8 across 6 owed, not applied**
  (one boundary surface: the fixture-apparatus API under `src/data/`); Q3's §15.2
  `not_applicable` reading recorded as the owner-approved reading; Q4's data-scope ruling
  (fixture scale via apparatus partitions; the runtime tolerance later frozen at this scope
  bounds nothing about a confirmatory run — stated for the manifest's Runtime block); the
  cross-unit additive edits of Q4 and Q5 tabulated per owning unit (`features-and-splits`
  `05`; `models-and-baselines` `06`; `evaluation-and-comparison` `07`; `acquisition` `00`;
  `inventory-and-registry` `01`; `target-standardization` `02`; `external-products` `04`) with
  the note that their READY code-summaries go stale under their receipts; Q6's three defaults;
  the §15.2 **12-not-13** REQ-ENG-4 correction reported (a `requirements.md` change, not
  applied); the **FR-WS-2 / FR-WS-3 candidate Vision §15.2 acceptance rows** proposed as text
  (evidence columns: the `smoke_only` absence-assertion result; the record-date
  assembly-assertion result); the **M10 §13.2 placement proposal** (a named step after the
  plumbing fixture; gates no full-year job; not a third receipt); honest limits.

- [x] **Step 2 — `src/data/fixture_manifest.py` (new; F1 + the F2 read side)** [W-1, W-2, W-3 limb 1, W-5 limb 1; R-133, R-134, R-135, R-137, R-139 declaration side; FR-WS-1, FR-WS-5, NFR-REP-01]
  The one schema: the **twelve TE §15.2 areas by name** as required blocks (Identity, Inputs,
  Processing, Expected schema, Units, Row-count ranges, Support/missingness, Timestamp
  tolerances, Independent reference checks, Required outputs, Runtime, Numerical variation);
  Q3's reading — a Phase 2-only quantity recorded `not_applicable` with reason, a missing
  block fails, `not_applicable` on a Phase-1-applicable quantity fails. `status: candidate |
  frozen`; identity by citation (`window_citation` D-11/D-14, `station_citation` D-20 for
  `plumbing_7day` only, `selection_rule`, `creator`, `approval_status`) with the **verbatim
  limitations block** (D-11's not-representative-of-December limitation and provisional-Dst
  restriction; D-14's clauses (i) and (ii)) and `aruc_shortfall_status: dormant` with its
  reactivation condition; eligibility-evidence block distinct from expected-assertion blocks;
  **every measured field carries `measuring_run_id`** (a measured field without one is
  unrepresentable → refuses); the **§15.4 cross-reference** (`artifact_manifest_ref`;
  Required-outputs complete against the enumeration — 20 for `scientific_1month`, 19 for
  `plumbing_7day`; hash-listing agrees with disk via `release.sha256_of_file`); **one
  comparison-ledger entry per required output** (`comparison_class: exact | toleranced`,
  `units`, `fp_tolerance` iff toleranced, `runtime_range`/`storage_range` on run-level
  entries, `tolerance_provenance`); the **TECU-without-inverse-route refusal** (a
  `toleranced` entry declaring TECU for an output whose declared `producing_path` carries no
  `inverse_route` is not freezable — control 25); the `fixture_bootstrap` block on
  `scientific_1month` only (`replicates`, `scored_range`, `block_counts` at 24 h and 48 h;
  absence fails; an indivisible `scored_range` fails at freeze — control 37); the **apparatus
  partition declaration** (ids distinct from the six frozen ids; a frozen id fails — control
  15). **The only read path**: `load_fixture_manifest(path) -> FixtureManifest` validates on
  read; on `status: frozen` it requires the sibling `fixture_manifest.sha256` and refuses on
  mismatch (SD-X-01 step 1; a `candidate` carrying a sibling raises); the D-number agreement
  check belongs to Step 6 (F7), not here. Every refusal raises the base `IntegrityError`
  naming file and violated expectation (Q6 (i)). `pyyaml` + `hashlib` only (TS-X-01); no
  schema package. Docstring names the unenforced-chokepoint limit and the only-copy control
  that narrows it.

- [x] **Step 3 — `src/data/fixture_gate.py` (new; F4 + F6)** [W-7, W-8; R-140, R-141; FR-WS-1, FR-WS-6, REQ-NFR-A3]
  **Receipts as append-safe registry rows** (Q6 (ii); SD-X-02 Rec 7): `write_fixture_pass_receipt(...)`
  appends via `experiment_registry.append_registry_event` a row carrying `fixture_id`,
  `frozen_manifest_hash`, `result`, `registry_run_id`, `completed_at_utc`, `platform`, the
  §13.1 lock items in force, and — for `scientific_1month` — the plumbing receipt it found
  (identity by citation); **refused at write time from a `candidate` manifest** (control 29).
  **The exported check** `require_fixture_receipts(registry_path, *, manifests, lock)`: both
  receipts present, plumbing before scientific (from the citation, not timestamps), each
  hash equal to the frozen manifest in force (a re-freeze invalidates old receipts —
  control 28), lock-bound validity (SD-X-02: a receipt is accepted iff its recorded lock
  matches the caller's own §13.1 lock), raising the base `IntegrityError` on each of the four
  bypass routes (26–29); exempt when the caller passes a fixture manifest (a fixture run is
  not a full-year job — Q5). **The in-session gate result** (R-141): `emit_in_session_gate_result(snapshot, lock, critical_test_results, fixture_results, started, completed)`
  with `platform` read from `ConfigSnapshot.platform` (never caller-asserted), the eight lock
  items, both frozen manifest hashes in force, per-test and per-fixture results, and
  `measured_total_runtime` (recorded against no ceiling); `require_in_session_gate(result,
  lock, manifests)` refuses a `local` stamp, a lock disagreement, and a result predating the
  frozen manifests (controls 30–32). Written as registry rows too, for the same reason.

- [x] **Step 4 — `src/data/fixture_evidence.py` (new; F7)** [W-9; R-142; SD-X-01 step 3; SD-X-03; FR-WS-2, FR-WS-4]
  Three **generated paths that refuse**: `build_traceability_matrix(...)` (TA-21 — three
  mandatory links per row; completeness against the implemented-requirement list; a row citing
  a test module absent from the workspace raises — control 33; presence, not coverage, stated
  in the docstring with the TA-15 disclosure); `build_acceptance_table(...)` (TA-09 — bounded
  by construction to WS-01 + WS-09…WS-20; any WS-02…WS-08 row raises — control 35; `PASS`
  without an evidence link raises — control 34; the G-P3A deferral stated on the table);
  `build_environment_and_cpu_preflight_report(...)` (G-07 — the eight lock items, platform,
  CPU-only completion record, runtime/storage against measured ranges, matched-artifact
  result, two receipt references, `measured_total_runtime`, both caveat fields wherever a
  coverage figure appears — control 36). All three refuse a `candidate` manifest (control 5),
  refuse any `smoke_only` input (control 13), and refuse a coverage figure lacking
  `data07_caveat` or `december_representativeness` (11, 38). `FixtureArtifactStamp` helpers
  (`stamp_fixture_artifact`, `assert_not_smoke_only`, `assert_caveats_present`) live here for
  the emitters and the orchestrator. **The sibling/D-number agreement check**
  `assert_freeze_record_agrees(manifest_path)`: parses `evidence/DECISIONS.md` for the freeze
  D-number's `fixture_manifest_sha256:` line and asserts equality with the sibling `.sha256`,
  naming both sites on disagreement; the machine-readable sidecar fallback is implemented
  behind the same function and its use recorded. `aws_ai_dlc_preflight_report` is named in
  the docstring as `foundation`'s and not built.

- [x] **Step 5 — `scripts/run_walking_skeleton.py` (new; the orchestrator; F3)** [W-3, W-4, W-5, W-7; R-135, R-136, R-137, R-140; FR-WS-1, FR-WS-2, FR-WS-3]
  `--config configs/ --fixture plumbing_7day|scientific_1month [--emit-candidate]`; the
  six-step stage entry exactly as the seven scripts do (determinism first via
  `ensure_process_determinism`, then `load_configs` → `assert_no_tbd` →
  `assert_declared_sources_exist` → `assert_phase_boundary` → `seed_everything` →
  `capture_environment_lock`/`assert_lock_complete`) — so today it refuses at step 2 and
  writes an honest `aborted` row naming the first `TBD` field; the manifest read ONLY
  through Step 2's loader (a missing manifest refuses naming the path — the state this pass
  leaves both trees in); **ordering enforced**: `scientific_1month` requires the plumbing
  receipt via Step 3's check (control 26); **plumbing lineage**: the four declared November
  artifacts verified against `evidence/audit_evidence_2022-11/sha256_manifest.json` BEFORE
  the run (control 12), BSHM-only assembly with a foreign-station record raising (9) and a
  non-D-20 manifest station raising (10); **record-date assertion** on every input record
  against the window and the December exclusion, consuming `acquisition`'s R-31 membership
  and `test_acquisition_window.py`'s predicate (exposed once, imported, never copied), with
  the folder name ignored (control 14 and its mislabelled-folder must-not-fire); the
  **seven Phase 1 stage scripts invoked as subprocesses** in §13.2's order with `--config
  configs/` and, on `05`/`06`/`07`, `--fixture-manifest <path>` (Q4) — the §15.3 ladder
  (fixture 1: M-01…M-05 + minimal M-06 + B-01/C-01 samples; fixture 2: the complete ladder,
  pooled masks, full benchmark join, the reduced-replicate fixture bootstrap from the
  manifest's `fixture_bootstrap` block); **every output stamped** (`evidence_class:
  smoke_only` on plumbing; `fixture_id`; `data07_caveat`; `december_representativeness`;
  `apparatus_partition_id`; `phase_id`/`source_id`/`target_definition_id`); the §15.4
  `artifact_manifest.json` hash-listing over the required outputs (`release.sha256_of_file`)
  and the fixture run log; **`--emit-candidate`** writes a `status: candidate` manifest whose
  measured fields carry this run's registry id and never a `frozen` one; **the receipt**
  written only from a `frozen` manifest (control 29); **the M10 step** after the plumbing
  fixture: `python -m pytest tests/test_train_only_transforms.py tests/test_split_embargo.py`,
  its result recorded in the run log as clean-run evidence, never a receipt (R-137
  must-not-fire). No domain logic; no import of `iri.py`/`gim.py`.

- [x] **Step 6 — Sibling stage scripts, additive edits only (Q4 = A, Q5 = A), each flagged for its owner's record**
  `05_build_features_and_splits.py`, `06_train_and_predict.py`, `07_evaluate_and_report.py`
  gain `--fixture-manifest <path>` (default `None`): when present, the apparatus partitions
  are built from the loader's declaration (never a frozen id; a frozen id in a fixture
  artifact refuses — control 15; a fixture id offered to `assert_transform_identity` raises
  like any mismatched pair, no seventh exception — control 16), `apparatus_partition_id` is
  stamped on every output, and the scope is fixture-scale. **All seven** Phase 1 scripts'
  `_stage_entry` gain one call, `require_fixture_receipts(...)`, immediately after
  `assert_lock_complete`, exempt when `--fixture-manifest` is given (Q5). Nothing else in any
  sibling script changes; each edit is one additive option and/or one call, recorded in the
  Step 1 table with the owning unit named.

- [x] **Step 7 — The two fixture trees, without manifests** [W-10; BLK-02]
  `tests/fixtures/plumbing_7day/` and `tests/fixtures/scientific_1month/` created with a
  `.gitkeep` each and NO `fixture_manifest.yaml` — the manifests come from a measuring run
  (`--emit-candidate`) that cannot complete today, and the freeze act is the owner's. A
  `README.md` in each names the loader, the two states, the citation the identity block
  will carry (D-11 + D-20; D-14) and the fact that no file here is a manifest. Nothing is
  invented.

- [x] **Step 8 — `tests/test_clean_run.py` (new; §12's mandated module)** [W-6, W-10; R-138, R-139; the 39 controls and 11 must-not-fire; WS-20, TA-17 as skipped evidence]
  Synthetic trees only (`tmp_path`; synthetic manifests, receipts, registry rows, planted
  records, mislabelled directories, single-bit plants — apparatus constants, R-122; no real
  config value). Hosts, by rule: R-133 (1)–(4), (37) incl. the per-area enumeration (one case
  per area) and the **only-copy check** (an AST/grep scan of `src/`, `scripts/`, `tests/` for a
  YAML parse of a fixture manifest outside the loader); R-134 (5)–(8); R-135 (9)–(12), (38);
  R-136 (13)–(14) + the mislabelled-folder admission; R-137 (15)–(17); R-138 (18)–(20), (39):
  **the executed command list is compared to §13.2's Phase 1 enumeration parsed from the TE
  fence** (order AND membership, names and flags verbatim, the ruled scope argument
  recognised), `PYTHONHASHSEED` unset-or-late fails, a GPU-dependent completion fails (the
  run executes with `CUDA_VISIBLE_DEVICES=""`), a Phase-2-only script raises
  `PhaseBoundaryError`; R-139 (21)–(25) incl. the silent-update refusal and the TECU
  refusal; R-140 (26)–(29) on synthetic receipt trees; R-141 (30)–(32); R-142 (33)–(36).
  The **clean-run completion test** (must-not-fire) runs the real sequence when the
  preconditions hold and otherwise **skips with the exact stop-and-report reason** (the first
  `TBD — freeze gate` field, the unfrozen TensorFlow pin, absent `numpy`/`pandas`/`pyyaml`,
  absent manifests) — recorded as `not run` in the summary; it never passes on an abort. The
  count of test functions is derived (`grep -c "def test_"`) and printed before it is asserted.

- [x] **Step 9 — Smoke + lint** — scratchpad Python 3.11.16 + the stdlib pytest stand-in:
  `tests.test_clean_run`; regressions on every module a Step 6 edit can reach
  (`test_train_only_transforms`, `test_split_embargo`, `test_common_masks`, `test_bootstrap`,
  `test_regimes_and_reporting`, `test_models_smoke`, `test_checkpoint_restore`,
  `test_acquisition_window`, `test_phase_boundary`, `test_import_boundary`); `compileall`;
  stdlib line-length substitute against `pyproject.toml`'s 99; ruff and real pytest owed
  (PyPI unreachable); `graphify update .` after the code change (CLI present on this clone);
  exact results recorded — **smoke evidence only, never governed**.

- [ ] **Step 10 — Governance stop before commit (student acts)**
  Step 1's record exists FIRST. Gate items: the amendment ledger **+1 → 8 across 6**
  (`component-methods.md`, owed); the seven sibling scripts' additive edits and their
  owners' stale code-summaries; the §15.2 **REQ-ENG-4 correction** (13 → 12; enumerates 9)
  owed in `requirements.md`; the **FR-WS-2 / FR-WS-3 candidate §15.2 rows** (Vision §15.2,
  owner/supervisor); the **M10 §13.2 placement proposal**; the **two freeze acts** (Q-31;
  nothing here performs them — and no `candidate` manifest exists either, since no measuring
  run can complete before the `TBD — freeze gate` fields and the TensorFlow pin are frozen);
  **BLK-02 open; BLK-08 ↓ mechanism limb open**; WS-20, TA-09, TA-17, TA-21 `Pending`;
  TA-03/TA-26 in-session evidence unproducible off Kaggle; TA-15 not covered (recorded,
  `foundation`'s); the stale `team.md` § Walking Skeleton "remains open under Q-31" line
  (D-14; practices-gate-owned); commit citing **D-11, D-14, D-20, D-28, D-29, D-31** plus the
  Step 1 change record. **No governed commit before the records exist.**

## Out of scope

Authoring or freezing any `fixture_manifest.yaml`; running either fixture or the clean run to
completion (blocked by `TBD — freeze gate` fields, the TensorFlow pin and the absent
interpreter dependencies — stated, not worked around); any measured value; editing
`requirements.md`, `services.md`, `component-methods.md`, TE §13.2/§15.2 or any completed-stage
artifact; `aws_ai_dlc_preflight_report` (`foundation`'s); TA-27's hash-diff limb (G-P2/G-P3C);
the `raw_isprint_cache/` re-acquisition; any acceptance-row discharge; any commit.
