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

## 11. Step 9 outcome (recorded when reached; completed on the 2026-09-09 resume pass)

The 2026-09-07 session ended after Steps 1–5 and 7; Steps 6, 8 and 9 were completed on
2026-09-09 by the resume dispatch. What changed on disk after this record was first written:

- **Step 6 as tabulated in § 5**: the seven Phase 1 stage scripts gained `--fixture-manifest`
  plus the one `require_receipts_for_snapshot` call after `assert_lock_complete`; `05`/`06`/`07`
  gained `_run_fixture_scale` behind one early-return line. `src/data/acquisition.py`'s
  `assert_records_within_window` was already present from the 2026-09-07 session.
- **One consequence beyond § 5's table, recorded for its owner to confirm or reverse** (the
  § 6.1 pattern): `scripts/03_verify_processing.py` (`target-standardization`; Phase 2 only)
  carried its own `yaml.safe_load` of a fixture manifest in `_load_tolerance` — exactly the
  second parser R-133 control 4 exists to refuse, predating this unit. Its read was rerouted
  through `load_fixture_scope` (the one loader), strictly narrowing behaviour: an invalid
  manifest now refuses at the loader instead of being parsed loosely for one field. Without
  this the project-wide only-copy scan Q2 = A mandates would have failed on day one.
- **Step 8**: `tests/test_clean_run.py` — 49 test functions (`grep -c "def test_"` printed
  before assertion by its own final test), hosting the 39 controls, the 11 must-not-fire
  controls, the per-area enumeration, the AST only-copy scan, the TE §13.2 fence parse
  (membership AND order), and the completion test.
- **Step 9, executed 2026-09-09** on the session-scratchpad Python 3.11.16 + a stdlib pytest
  stand-in (PyPI unreachable; pyyaml/numpy/pandas/pytest/ruff uninstallable — attempted and
  recorded): `tests.test_clean_run` **46 passed, 0 failed, 3 skipped** (skips by name:
  two pyyaml-gated production-loader paths; the clean-run completion test skipping with the
  stop-and-report reason "pyyaml is not importable on this clone"). Regressions on the ten
  named sibling modules: **436 passed, 0 failed, 13 skipped, 0 errors** in total with
  `test_clean_run` included; every skip is by name. `compileall` clean over `scripts/`, `src/`,
  `tests/`. Stdlib 99-column scan: every line added by this pass conforms; **47 pre-existing
  over-99 lines remain in the 2026-09-07 files** (`run_walking_skeleton.py`,
  `fixture_manifest.py`, `fixture_gate.py`, `fixture_evidence.py`, one in
  `01_inventory_and_registry.py`) — recorded here; real `ruff` is owed to a governed
  environment. `graphify` is not on this clone's PATH (`command not found`); the graph update
  is owed alongside ruff. Pre-existing failures NOT caused by this pass, verified by re-running
  on the stashed (unmodified) tree: `test_external_drivers` 11 (pyyaml preflight, § 6.2's
  routed item), `test_iri_denial` 1 (containment scan), `test_locked_test_guard` 1
  (`test_common_masks.py` restricted-root literal), and 4 import-error modules
  (`test_acquisition`, `test_experiment_registry`, `test_determinism`, `test_december_audit`).
  **Smoke evidence only, never governed.**

### §11.1 — Correction, 2026-09-09: the commit state (§10's last bullet is superseded)

§10's bullet "**No commit is made here.** The student commits, citing D-11, D-14, D-20,
D-28, D-29, D-31 and this change ID" is left standing above as the record of the intent when
written, and is **superseded as to the repository fact**: owner commit **`64c0551`**
(2026-09-07 12:21 +0400, an unedited git template message, **no D-number cited**) already
carries the Step 1–5/7 outputs (`src/data/fixture_manifest.py`, `fixture_gate.py`,
`fixture_evidence.py`, `scripts/run_walking_skeleton.py`, the two fixture trees), the
`src/data/acquisition.py` additive edit (`assert_records_within_window`) and this change
record's first version. The **resume-pass outputs remain uncommitted**: the Step 6 sibling
edits (the seven stage scripts and the `03_verify_processing.py` reroute),
`tests/test_clean_run.py`, the plan checkbox ticks, §11 and this correction. The owed
D-number citations (**D-11, D-14, D-20, D-28, D-29, D-31** plus
`CR-2026-09-07-R133-FIXTURES-AND-REPRODUCIBILITY`) now attach to an
**amend-or-follow-up decision that is the student's**, routed to the stage gate.
*(Added 2026-09-09 per the adversarial review's commit-state finding; appended rather than
rewritten, per this record's dated-update convention.)*

### §11.2 — Addition, 2026-09-09: the 39/11 figure is now machine-checked, not carried

Per the same review's Finding 3: `tests/test_clean_run.py` now carries a machine-readable
control ledger (`CONTROL_HOSTS`, `MUST_NOT_FIRE_HOSTS`, `MNF_HOSTED_ELSEWHERE`) and a
derivation meta-test (`test_control_counts_derived_from_business_rules_not_carried`) that
parses the (1)–(39) enumeration and the 1+1+1+1+2+2+1+1+1 = 11 must-not-fire derivation
from `functional-design/business-rules.md` § Negative-control count, SET-DIFFERENCES the ID
lists (never totals), and prints both counts plus any missing/extra ids before asserting.
One must-not-fire control is hosted elsewhere by design and asserted present there:
R-137's November `score` containment pass (R-74's inherited control) lives in
`tests/test_train_only_transforms.py` — no third copy is written.

### §11.3 — Correction, 2026-09-09 (governance board Rec. 1): §11.1's commit state is itself superseded

§11.1's sentence "The **resume-pass outputs remain uncommitted**" is left standing above as
the fact at its writing time and is **superseded**: owner commit **`cf3185d`**
(2026-09-09 20:54 +0400, an unedited git template message, **no D-number cited**) already
carries the resume-pass governed outputs — the seven Step 6 stage-script edits including the
`03_verify_processing.py` reroute, `tests/test_clean_run.py`, the code-summary, the
`evidence/test_run_access_log.jsonl` rows, and §11/§11.1/§11.2 of this record — committed
**before** the fixtures unit's iteration-2 READY verdict timestamp (2026-09-09T17:40Z). It is
the eighth template-message, D-number-less commit of governed artifacts in this stage's window.
Per the governance board's Recommendation 1 (preferred option (a), applied on the owner's
"apply the recommended option" ruling of 2026-09-09): the disposition is **one combined
follow-up commit** citing **D-11, D-14, D-20, D-28, D-29, D-31** plus
`CR-2026-09-07-R133-FIXTURES-AND-REPRODUCIBILITY` and naming both `64c0551` and `cf3185d`;
no history is rewritten. The matching code-summary annotation the board recommended is
deliberately NOT applied: the code-summary sits under the unit's terminal READY receipt and a
post-receipt write would invalidate it — this section and the stage gate record carry the fact
instead.

### §11.4 — Corrections, 2026-09-09 (board Recs. 8–9): two counts restated from fresh derivation

- §11 Step 8's "49 test functions (`grep -c "def test_"` …)" and Step 9's "46 passed …
  436 passed" are superseded by the post-meta-test state: **50** test functions — derived by
  the ANCHORED form `grep -c "^def test_" tests/test_clean_run.py` (the unanchored command
  quoted in §11 now returns 53 on the current file and reproduces neither figure; the
  implemented derivation in `test_function_count_derived_and_printed` is the anchored one) —
  with `tests.test_clean_run` at **47 passed, 0 failed, 3 skipped** and the ten-module
  regression total at **437 passed, 0 failed, 13 skipped, 0 errors**.
- §11 Step 9's "**47 pre-existing over-99 lines**" is superseded: fresh derivation
  (CRLF-stripped, `len > 99`, per file: `run_walking_skeleton.py` 21, `fixture_manifest.py` 10,
  `fixture_gate.py` 6, `fixture_evidence.py` 14, `01_inventory_and_registry.py` 1) gives
  **52**. Every resume-pass file still contains zero over-99 lines. Closure note:
  `pyproject.toml` ignores `E501`, so these lines will never surface via `ruff check`; closure
  runs through `ruff format` (or a scoped `E501` re-enable) in the governed environment.

### §11.5 — Addition, 2026-09-09 (board Recs. 2–5, 10): apparatus remediation, owner-authorised

On the owner's "apply the recommended option" ruling over the governance board's report, the
following remediation was implemented as a separate pass after the review (board Recs. 2–5
preferred options; the cross-unit edits into READY-receipted scripts are covered by that
explicit ruling and flagged here for each owner's record):

- **Rec. 2 (ML-01)** — the TE §9.2 receipt-gate exemption on `scripts/00/01/02/04` is bound to
  the fixture scope's cited window (record-date assertion reusing
  `assert_records_within_window`), no longer granted on a validating flag alone; one negative
  control per script proves a full-scale invocation carrying a valid scope but out-of-window
  inputs refuses.
- **Rec. 3 (ML-02)** — `scripts/07`'s fixture path roots its mask registry under the fixture
  tree (`artifacts/walking_skeleton/<fixture_id>/mask_registry`) and stamps each apparatus
  registration; negative controls prove a post-fixture confirmatory registration succeeds and
  `freeze_bundle` enumerates no apparatus `partition_id`.
- **Rec. 4 (ML-03)** — the orchestrator's `build_phase1_commands` passes explicit output roots
  under the fixture root and a deterministic run id through 05/06/07; 06's fixture path reads
  the apparatus split manifest by its own name; stage fixture paths emit machine-readable
  measurement blocks the orchestrator folds into candidate `measurements`; a dry-run
  integration test (synthetic frozen configs, the `parsed=` injection pattern) asserts the
  chain connects and a complete candidate validates from orchestrator-collectable measurements.
- **Rec. 5 (ML-04)** — `--emit-candidate` composes `min`/`max` over N measuring runs (each
  stamped with its run id) and refuses a zero-width runtime/storage range at composition.
- **Rec. 10 (DR-03)** — the only-copy scan's claim is qualified here and in
  `src/data/fixture_manifest.py`'s docstring: the AST scan flags `yaml.*load` calls whose
  argument subtree **textually references** `fixture_manifest`; an intermediate-variable parse
  is outside its reach, which remains a convention backed by review, per the module's
  honest-limits paragraph. The §2 and §10 sentences claiming "any such parse fails the scan"
  are superseded to that qualified form.

Board Recs. 6–7 are gate-record conditions, applied at the AI-DLC stage gate: approval scope
excludes W-5 breakdown production and the SD-R-03 registration net (blocked on
`regimes-diagnostics-reporting`'s standing terminal NOT-READY), and the two pre-existing
critical-suite reds (`test_iri_denial` containment scan; `test_locked_test_guard` restricted-
root literal in `test_common_masks.py`) are registered verbatim as named preconditions of the
next governed run.

### §11.6 — Addition, 2026-09-10 (owner gate worklist): the Rec-6/7 preconditions are repaired; deltas of the worklist pass

The two pre-existing critical reds §11.5's closing paragraph registered as named
preconditions are REPAIRED at root cause on the owner's 2026-09-10 gate worklist
(uncommitted at this writing; none of the repairs touches a fixtures-unit file):

- `tests/test_iri_denial.py` — the containment scan's 8 violations were all one root
  cause: the transitive walk flagged `src/evaluation/metrics.py`'s DEFERRED
  (function-scope) gim import — R-112's sanctioned evaluation-time mechanism — for every
  chain that reached the allowlisted module. The scan is now scope-aware (eager vs
  deferred), records such sites under `sanctioned_deferred_target_sites`, and keeps full
  strength both ways (new controls: a deferred target import OUTSIDE the allowlist still
  fails; an EAGER target import inside an allowlisted module still fails every chain).
  Result: **22 passed, 0 failed**.
- `tests/test_locked_test_guard.py` — the flagged holder (`tests/test_common_masks.py`)
  now derives the restricted-root name from `locked_test.RESTRICTED_ROOT` at three sites
  instead of spelling the literal; the guard itself is UNCHANGED and both membership
  directions hold. Result: **44 passed, 0 failed** (test_common_masks: 60 passed / 1 skip).
- The four import-error modules (§11 Step 9's list) are resolved: two were purely a
  session-tooling gap (`@pytest.fixture` support added to the scratchpad stand-in —
  `test_acquisition` **47 passed**, `test_experiment_registry` **49 passed**,
  `test_december_audit` **62 passed**); `test_determinism` gained named
  `pytest.importorskip("yaml")` classification at its config-parsing surfaces
  (**12 passed / 23 skipped by name / 0 failed**, all 35 run in a pyyaml environment).
- Staleness sweep of this record after those repairs: §11.4's counts stand (52 over-99
  lines unchanged — PyPI re-verified unreachable 2026-09-10, `ruff`/`pyyaml`/`pytest`
  uninstallable, fresh timeouts recorded; graphify remains a skill, not a CLI: no
  executable on PATH, `npx` cannot resolve one); `tests/test_clean_run.py` is unchanged by
  this pass (**57 passed / 3 skipped by name; 39/11 reconciliation empty both ways**).
  The seven owning units' code-summaries and `models-and-baselines`' 741→806→944→999
  line-count chain now carry dated cross-unit records (worklist item 4).

### §11.7 — Addition, 2026-09-10 (second gate worklist): over-99 closure, in-session doc, decision requests

- **§11.4's over-99 count is CLOSED**: the four 2026-09-07 fixture modules plus the one
  line in `scripts/01_inventory_and_registry.py` were manually reformatted
  (behavior-preserving wraps only; no `pyproject.toml` change). Re-derived after: **0**
  over-99 lines across all five files; `compileall` clean; the full suite re-run
  reproduces the pre-reformat per-module counts exactly (behavior preserved). Real `ruff`
  STILL could not run — a fresh `uv pip install` retry on 2026-09-10 timed out against
  PyPI again; the stdlib scan is the substitute of record.
- **TA-03/TA-26 documentation gap closed**: both fixture READMEs now carry "The Kaggle
  in-session sequence" (critical set → both fixtures → `emit_in_session_gate_result`,
  `--code-commit` required in-session); both rows stay `Pending` — no evidence is claimed.
- **Rec 10's qualification swept** to `tests/fixtures/plumbing_7day/README.md`'s only-copy
  sentence (the last unqualified representation found).
- **Decision requests prepared, none decided**:
  `governance/FREEZE_DECISION_REQUEST_2026-09-10.md` — the complete 16-row
  `TBD — freeze gate` inventory with per-field refusal probes (all fire), the Q-31 freeze
  sequence (declarations → ≥2 measuring runs → the owner's two freeze acts), the D-27 /
  BLK-08 mechanism-limb options (recommendation: affirm withholding, adopt R-103's joint
  contract in D-27's identity form), the TensorFlow pin flagged as UNDECIDED (no D-number
  anywhere; candidate `tensorflow==2.21.0` from the implemented M-06 API, recommendation
  only), and the Q5/`test_external_drivers` options with recommendation (b) — the 11
  failures stand pending the owner's ruling.
- **CLAUDE.md's graphify section corrected (documentation only)**: the `graphify <verb>`
  rules are now conditioned on an installed CLI (none exists on this clone — verified
  again 2026-09-10; the `/graphify` skill remains the rebuild path).
