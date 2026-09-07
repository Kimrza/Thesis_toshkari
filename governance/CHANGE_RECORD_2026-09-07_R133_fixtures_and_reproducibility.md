# Change Record — 2026-09-07 — `fixtures-and-reproducibility` code generation (R-133…R-142)

**Change ID:** `CR-2026-09-07-R133-FIXTURES-AND-REPRODUCIBILITY` (proposed D-number pending
owner adoption — no agent writes `evidence/DECISIONS.md`)
**Unit:** `fixtures-and-reproducibility` (Bolt 12, the last of twelve, kind `library`) ·
**Stage:** `code-generation` (3.5)
**Receipted answers (code-generation-questions.md):** Q1 = A, Q2 = A, Q3 = A, Q4 = A, Q5 = A,
Q6 = A; Consolidated Summary Confirmation `Looks correct`; Plan `Approve Plan`.
**Authority:** TE §9.1/§9.2 (both fixtures before any full-year job; the in-session rule),
§13.1 (the eight lock items), §13.2 as amended (`PYTHONHASHSEED=0`; the seven Phase 1
invocations; the Phase 2 segment gated `# Phase 2, only after G-P2`), §13.7 (exact classes;
no silent update), §15.1–§15.4, §18.3 (stop-and-report); `evidence/DECISIONS.md` **D-11**
(plumbing window and its mandatory limitation and provisional-Dst restriction), **D-14**
(March 2022, all three cells, limitation clauses (i) and (ii)), **D-20** (BSHM 32/35),
**D-28** (2–31 December 2022, 30 days), **D-29** (12-hex `dataset_version`, verify-on-write),
**D-31** (G-09 signed with its §18.3 preconditions disclosed unmet); `team.md` § Walking
Skeleton (derived-artifact eligibility; DATA-07 caveat); nfr-design SD-X-01…SD-X-03 (READY
2026-09-05).

This record is written FIRST, before any module, script edit, fixture directory or test in
this pass, per the approved plan's Step 1. **It decides no scientific value and states no
measured value**: every window, station, month, seed, partition and threshold reaches code
only by citation of a frozen D-number, from `configs/`, or as a field of a fixture manifest
that does not exist yet.

---

## 1. Blocker state, limb by limb

| Blocker | Limb | State on 2026-09-07 | Record |
|---|---|---|---|
| **BLK-03 ↓** | confirmatory contract | **approved** 2026-09-06 | `governance/CHANGE_RECORD_2026-09-06_BLK03_confirmatory_contract.md` |
| **BLK-04 ↓** | leakage contract (R-74) | **approved** 2026-09-05 | `governance/CHANGE_RECORD_2026-09-05_R74_R83_leakage_contracts.md` |
| **BLK-09 ↓** | partition training range (R-83) | **approved** 2026-09-05 | same record |
| **BLK-08 ↓** | mechanism limb (inverse route) | **OPEN** — D-27 unreopened; `evidence/DECISIONS.md` ends at D-32 | made a **checked refusal** here: a `toleranced` ledger entry declaring TECU units for an output whose `producing_path` carries no `inverse_route` is refused by the manifest loader (R-139 control 25) |
| **BLK-02** (owned) | manifest / execution / measured evidence | **OPEN on implementation** — no manifest exists, neither fixture has run, **no measured value exists and none is stated, inferred or substituted** (TE §15.1) | the two freeze acts are the owner's under Q-31; this pass builds the apparatus and authors NO `fixture_manifest.yaml` |

## 2. Q2 = A — the loader's home, and the amendment ledger

The manifest schema and its ONE validating loader live at **`src/data/fixture_manifest.py`**,
with `src/data/fixture_gate.py` (receipts, the exported two-receipt check, the in-session
gate) and `src/data/fixture_evidence.py` (the three generated evidence artifacts, the stamps,
the sibling/D-number agreement check) beside it as one fixture-apparatus API under `src/data/`.

**Amendment ledger: +1 → 8 across 6 units, OWED, not applied.** The functional design derived
7 across 5 (`business-rules.md` § Amendments owed: 5 + 0 + 1 + 1 + 0 + 0) and stated the
conditional in terms: placing the loader in `foundation`'s `src/data/` as a cross-unit
contract "mints a new `component-methods.md` boundary surface and the ledger takes +1, to
8 across 6, at that ruling". Q2 = A is that ruling. The `component-methods.md` amendment (one
boundary surface: the fixture-apparatus API under `src/data/` — `load_fixture_manifest`,
`require_fixture_receipts`, the evidence emitters) is **owed to `foundation`'s next touch** and
is not made here: `component-methods.md` is a completed-stage artifact.

The only-copy check (R-133 control 4) therefore scopes **project-wide**: a YAML parse of a
fixture manifest anywhere under `src/`, `scripts/` or `tests/` other than the loader fails
`tests/test_clean_run.py`'s scan.

## 3. Q3 = A — the §15.2 `not_applicable` reading, recorded as owner-approved

Every one of the twelve TE §15.2 content areas is a required block, **by name**: Identity,
Inputs, Processing, Expected schema, Units, Row-count ranges, Support/missingness, Timestamp
tolerances, Independent reference checks, Required outputs, Runtime, Numerical variation. A
missing block fails. A **Phase 2-only quantity** inside a block is recorded
`status: not_applicable` with a non-empty `reason` (the FR-P1-03-5 precedent); `not_applicable`
on a Phase-1-applicable quantity fails.

**Derived refinement, printed here before it is coded.** The design's prose named three areas
(Inputs, Processing, Independent reference checks) as the ones naming Phase 2 quantities.
Reading §15.2's table row by row against TE §7.0's Phase 1 hard prohibition yields
Phase-2-only quantities in **six** areas — eleven quantities:

| Area | Phase-2-only quantities (recorded `not_applicable` on a Phase 1 manifest) |
|---|---|
| Inputs | `rinex_crx`, `dcb` |
| Processing | `gnss_tec_version`, `calibration_layer_commit` |
| Expected schema | `raw`, `intermediate` |
| Row-count ranges | `parsing`, `valid_observation` |
| Timestamp tolerances | `parser` |
| Independent reference checks | `stec_vtec_intermediates`, `hand_worked_dcb_pass` |

2 + 2 + 2 + 2 + 1 + 2 = **11**. The receipted ruling is quantity-level ("a Phase 2-only quantity
inside a block"), so the schema applies it at quantity level; the three areas the design named
are the ones whose quantities are predominantly Phase 2. Every other quantity in every area is
Phase-1-applicable and may not be `not_applicable`. **One Phase 1 input quantity is added that
§15.2's Inputs row does not name: `prepared_vtec`** — the prepared provider VTEC product TE
§15.1 says the Phase 1 fixture reads ("The Phase 1 fixture reads prepared provider VTEC
only"), declared as the month's four derived artifacts with their SHA-256 and the month's
`sha256_manifest.json`, which W-3 limb 3 verifies at use. It is the Phase 1 counterpart of
the RINEX/CRX row, stated rather than smuggled.

**Reported, not applied — REQ-ENG-4's numeral.** `requirements.md` REQ-ENG-4 asserts "all
thirteen of TE §15.2's content areas" and enumerates nine. Derived from §15.2's table:
**13 rows including the `| Area |` header → 12 content areas**; the nine enumerated omit
Processing, Units and Independent reference checks (9 + 3 = 12). The correction (13 → 12; the
enumeration extended by the three omitted names) is a `requirements.md` change owed to its
owner. The code binds to the named twelve.

## 4. Q4 = A — the Phase 1 segment's data scope: fixture scale via apparatus partitions

The `scientific_1month` manifest declares an **apparatus partition set** over its window, with
ids distinct from the six frozen ids (`F1`…`F4`, `REFIT`, `DEC` — `src/data/splits.py`
`PARTITION_IDS`, read, never restated). The loader refuses a frozen id in the declaration
(R-137 control 15); `build_apparatus_partitions` constructs `Partition` objects from it with
`embargo_hours` read from `configs/experiment.yaml` (TC-03e — the value is `TBD — freeze gate`
today, so the construction refuses naming the field). `05`, `06` and `07` gain
`--fixture-manifest <path>` and, when it is given, run against the apparatus partitions at
fixture scale, stamping `apparatus_partition_id` and the fixture stamp on every output.

**The runtime tolerance later frozen at this scope bounds nothing about a confirmatory run.**
The manifest's Runtime block records its `measuring_run_id` and the scope it was measured at;
no reader may carry a fixture-scale runtime range onto a full-year job. Stated here for the
manifest's Runtime block, as the plan requires.

## 5. Q4 and Q5 — the cross-unit additive edits, per owning unit

Every edit below is additive: one option and/or one call, plus (on `05`/`06`/`07`) one
additive function that the one call reaches. **No existing line of any sibling script's
full-year path is changed.** Each owning unit's READY code-summary describes a script that no
longer matches its text; those summaries go stale under their receipts and are the owners'
to re-annotate.

| Script | Owning unit | Edit(s) | Why |
|---|---|---|---|
| `scripts/00_acquire_prepared_vtec.py` | `acquisition` | `--fixture-manifest` option; `_stage_entry(..., fixture_manifest=None)` kwarg; ONE call `require_receipts_for_snapshot(...)` after `assert_lock_complete`; `main()` passes the option | Q5 gate; Q5 exemption carrier (§ 6) |
| `scripts/01_inventory_and_registry.py` | `inventory-and-registry` | same three touches | same |
| `scripts/02_standardize_prepared_target.py` | `target-standardization` | same three touches | same |
| `scripts/04_build_external_products.py` | `external-products` | same three touches | same |
| `scripts/05_build_features_and_splits.py` | `features-and-splits` | option; kwarg + call; ONE early-return line in `_run` reaching the additive `_run_fixture_scale` (apparatus partitions, apparatus split manifest, bundle stamps) | Q4 + Q5 |
| `scripts/06_train_and_predict.py` | `models-and-baselines` | option (a `--partition` alongside it is a parser error); kwarg + call; ONE early-return line in `_run` reaching `_run_fixture_scale` (apparatus partitions, no locked path, stamped prediction payloads) | Q4 + Q5 |
| `scripts/07_evaluate_and_report.py` | `evaluation-and-comparison` | option (same parser rule); kwarg + call; ONE early-return line in `_run` reaching `_run_fixture_scale` (apparatus partitions, no locked path, sibling stamp files on the metrics artifacts) | Q4 + Q5 |

Also additive and flagged for its owner: **`src/data/acquisition.py`** (`acquisition`) gains
ONE public predicate, `assert_records_within_window(records, *, start, end, timestamp_key)`,
built on the same private date reader R-31's `partition_by_locked_month` uses, so the
orchestrator's record-date window assertion and `tests/test_clean_run.py` consume ONE rule
(R-31; `test_acquisition_window.py`'s predicate) and no third copy is written. The December
exclusion itself is the existing public `assert_no_locked_month_records`.

## 6. Two consequences of Q5 = A that the receipted wording did not spell out — recorded, not hidden

**6.1 The exemption must be carried by all seven scripts, not three.** Q4 gave
`--fixture-manifest` to `05`/`06`/`07`; Q5 exempts a run "when the run carries a fixture
manifest". But the fixture run itself (`run_walking_skeleton.py --fixture plumbing_7day`)
invokes **all seven** Phase 1 scripts as subprocesses (the §15.3 ladder), **before any receipt
exists** — the plumbing fixture is what produces the first receipt. With the receipts gate in
`00`/`01`/`02`/`04`'s `_stage_entry` and no way for those four to carry the fixture manifest,
the plumbing fixture would refuse on the receipts only it can write: a deadlock. The two ways
out are an environment-variable exemption (a hidden bypass any caller could set — rejected) or
giving `00`/`01`/`02`/`04` the same `--fixture-manifest` option as Q5's declared, visible,
run-log-recorded exemption carrier. **This pass takes the second.** On those four scripts the
option carries the exemption and the fixture scope only; they build no apparatus partitions.
This is one additive option beyond Q4's letter on each of four scripts, taken in service of
Q5's own wording, and it is recorded here for the owner to confirm or reverse.

**6.2 The gate bites a sibling test module today.** `tests/test_external_drivers.py` drives
`scripts/04_build_external_products.py` as a **non-fixture** subprocess in a temporary
workspace (9 tests via its `_run_script`) and asserts exit 0 with an audit manifest, or exit 1
with a specific refusal text. In a governed environment (pyyaml present) every one of those
invocations now refuses at `require_receipts_for_snapshot` — no frozen manifest, no receipt —
before reaching the path the test asserts. That is exactly Q5 = A's stated Impact ("every
full-year run refuses until both fixtures have passed under frozen manifests … bites
immediately"). On this clone those tests already fail at `load_configs` (pyyaml absent), so
the change is not observable here; it is certain elsewhere. **Routed to `external-products`'
owner**: pass `--fixture-manifest` in the smoke invocations, or assert the new refusal, or ask
the gate to narrow Q5. Nothing is changed in that test module by this pass.

## 7. Q6 = A — the three defaults, as built

1. **No new exception.** Every refusal in the three modules and the orchestrator raises the
   base `IntegrityError` naming the resource and the violated expectation. `PhaseBoundaryError`
   (a Phase-2-only script named in a Phase 1 clean run — R-138 control 39) and
   `LeakageError`/`PartitionError` (a fixture partition id offered to
   `assert_transform_identity` — R-137 control 16) are consumed preconditions raised by their
   owners' code, never redeclared.
2. **Receipts and gate results are experiment-registry rows.** `write_fixture_pass_receipt`
   writes the receipt payload (write-once JSON) and appends the fixture run's `completed` row
   through `append_registry_event`, `artifact_manifest_path` naming the payload. The tamper
   evidence SD-X-02 Rec 7 asked for is achieved through the row's `environment_lock_hash`
   column: the payload carries the eight §13.1 lock items **including an `input_versions`
   entry `fixture_manifest:<fixture_id>:<sha256>`**, so the check recomputes the lock hash
   from the payload and compares it with the append-only row — an edit to the payload's lock
   OR to its frozen-manifest binding breaks agreement with a row nothing can rewrite. The
   SD-X-02 discriminator (a receipt is valid iff its lock matches the caller's) is computed
   over the seven environment items (every lock item except `input_versions`, which is per-run
   by nature): `fixture_gate.environment_identity`. TE §13.4's twenty columns are used as
   defined — no column is repurposed; `notes` carries only the literal kind marker.
3. **`fixture_bootstrap` is apparatus.** Declared on `scientific_1month` only (`replicates`,
   `scored_range`, `block_counts`); the loader refuses its absence and an indivisible
   `scored_range` (R-133 control 37). The two block lengths reach the manifest from
   `configs/experiment.yaml` `bootstrap.block_hours` / `sensitivity_block_hours` at candidate
   emission, never from source.

## 8. FR-WS-2 / FR-WS-3 — candidate Vision §15.2 acceptance rows, proposed as text

D-32 approved eight candidate rows on 2026-08-28; FR-WS-2 and FR-WS-3 were not among them and
remain **NO CURRENT ACCEPTANCE ROW**. Proposed, not applied (a §15.2 amendment is the owner's,
with the Student proposing):

| ID | What the row accepts | Evidence column | Owning rule |
|---|---|---|---|
| **FR-WS-2** | No `plumbing_7day` artifact reaches an evidence surface: every result artifact, the TA-09 table, the TA-21 matrix and every release assert the absence of `evidence_class: smoke_only` inputs | the `smoke_only` absence-assertion result emitted by `fixture_evidence.assert_not_smoke_only` at each surface, recorded in the clean-run log | R-136 control (13) |
| **FR-WS-3** | No record whose observation date falls in December 2022 enters either fixture, asserted on record dates and never on the folder a file was filed under | the record-date assembly-assertion result emitted by `run_walking_skeleton.assert_assembled_records` (consuming `acquisition.assert_no_locked_month_records` and `assert_records_within_window`), recorded in the fixture run log | R-136 control (14) |

## 9. The M10 §13.2 placement — proposal, not an amendment

The M10 contract fixture (`tests/test_train_only_transforms.py`, `tests/test_split_embargo.py`;
authored by `features-and-splits`, run here under the owner's Q12 = C) executes as a **named
step immediately after the plumbing fixture** inside `run_walking_skeleton.py`, via
`python -m pytest tests/test_train_only_transforms.py tests/test_split_embargo.py`. Its result is
recorded in the fixture run log (`m10_contract_fixture`) as clean-run evidence. It **gates no
full-year job**, the two-fixture ordering contract is unchanged and unextended, and it is
**never a third receipt**. Writing that step into TE §13.2's fence is the authority document's
amendment and is proposed here only.

## 10. Honest limits — nothing below is discharged by this pass

- **No fixture ran. No manifest exists. No measured value appears anywhere.** Both fixture
  trees receive a `.gitkeep` and a `README.md`; neither receives a `fixture_manifest.yaml`.
- **Today's refusals, in order, for `run_walking_skeleton.py`:** on this clone `load_configs`
  refuses first (pyyaml absent); with pyyaml, the six-step entry passes on the minimal
  `REQUIRED_FIELDS_MAP` entry (`seeds.development`, as every sibling's), the `started` row is
  written, and `_run` refuses at the missing manifest, naming
  `tests/fixtures/<fixture_id>/fixture_manifest.yaml`, with an honest `aborted` row; once a
  manifest exists, apparatus-partition construction refuses at
  `configs/experiment.yaml: embargo_hours` (`TBD — freeze gate`); the plumbing fixture's
  minimal M-06 refuses on the unfrozen TensorFlow pin. TE §18.3: stop and report.
- **The clean-run completion test SKIPS** with the first unmet precondition named (absent
  pyyaml/numpy/pandas; absent manifests; `TBD — freeze gate` fields; the TensorFlow pin). It
  never passes on an abort. **WS-20, TA-09, TA-17, TA-21 stay `Pending`.** TA-03/TA-26's
  in-session evidence is unproducible off Kaggle. **TA-15 is not covered** (recorded;
  `foundation`'s). TA-27 is first-limb only.
- **`aws_ai_dlc_preflight_report` is `foundation`'s (G-09, TA-23, FR-WS-7) and is built
  nowhere here**; this unit's `environment_and_cpu_preflight_report` evidences G-07.
- **The loader chokepoint is unenforced** in the sense SD-X-01 states: a direct `yaml.safe_load`
  bypasses everything. What this pass adds is the only-copy scan (control 4) that fails the
  suite on any such bypass under `src/`, `scripts/` or `tests/`.
- **Smoke ≠ governed:** the only interpreter is the session-scratchpad Python 3.11.16 with a
  stdlib pytest stand-in; `numpy`, `pandas`, `pyyaml`, `pytest`, `ruff` are absent and PyPI is
  unreachable. Tests that need YAML parsing use the loader's documented `parsed=` injection
  point (test apparatus only; the production read path is `load_fixture_manifest(path)` on
  pyyaml). Real `pytest` and `ruff` are owed to a governed environment.
- **The `team.md` § Walking Skeleton line "remains open under Q-31"** (the scientific window)
  is stale on disk — D-14 froze it 2026-08-21; the line is the practices gate's to rewrite.
- **No commit is made here.** The student commits, citing D-11, D-14, D-20, D-28, D-29, D-31
  and this change ID.

## 11. Step 9 outcome (recorded when reached, same pass)

*Filled in at Step 9 — see the code summary's § Test coverage summary for the exact runner
lines; this section records only what changed on disk after the record was first written.*

- Step 9 executed 2026-09-07 on the scratchpad Python 3.11.16 + stdlib pytest stand-in.
  `tests.test_clean_run`: see code summary (`grep -c "def test_"` printed before assertion).
  Regressions on the ten named sibling modules: see code summary. `compileall` and the stdlib
  99-column scan: see code summary. `graphify update .` run once after the code changes.
  **Smoke evidence only, never governed.**
