# Code Generation Questions — `fixtures-and-reproducibility`

**Unit** `fixtures-and-reproducibility` (Bolt 12, the last unit and the DAG's terminal node) · **Kind** `library` · **Stage** `code-generation`

State on disk, verified 2026-09-07 (this clone): none of this unit's owned files exists —
no `scripts/run_walking_skeleton.py`, no `tests/test_clean_run.py`, `tests/fixtures/` holds
only a `.gitkeep`, and no `fixture_manifest.yaml` (neither `candidate` nor `frozen`). The
consumed surfaces the design assumed absent now exist: `configs/` (four files),
`src/data/config.py` with `ConfigSnapshot.platform`, `resolve_platform_roots`,
`capture_environment_lock`/`assert_lock_complete` (the §13.1 eight-item lock),
`experiment_registry.append_registry_event` (the append-safe registry rows SD-X-02 Rec 7
prefers for receipts), `release.sha256_of_file` (the single hashing home), and all seven
Phase 1 stage scripts `00`–`07` with the six-step stage-entry contract inline in each
(`_stage_entry`: `load_configs` → `assert_no_tbd` → `assert_declared_sources_exist` →
`assert_phase_boundary` → `seed_everything` → `capture_environment_lock`). The M10 contract
fixture is authored in `tests/test_train_only_transforms.py` and `tests/test_split_embargo.py`.
`evidence/audit_evidence_2022-11/` and `2022-03/` each carry the four declared derived
artifacts plus `sha256_manifest.json`. The exception hierarchy at R-01's single site now
holds 25 classes (counted from `src/data/config.py` `^class .*Error`), none fixture-specific.

**Blocker state, verified against `governance/`**: BLK-03 approved 2026-09-06
(`CHANGE_RECORD_2026-09-06_BLK03_confirmatory_contract.md`); BLK-04 and BLK-09 approved
2026-09-05 (`CHANGE_RECORD_2026-09-05_R74_R83_leakage_contracts.md`); **BLK-08's mechanism
limb stays open** (D-27 unreopened; `evidence/DECISIONS.md` ends at D-32) — R-139 control (25)
is what makes that a checked refusal at this unit's tolerance surface; **BLK-02 (owned) stays
open on implementation**: no measured value exists and none may be invented, so no `frozen`
manifest can exist after this pass either — the two freeze acts are the owner's under Q-31.

**What cannot execute here, stated up front (TE §18.3 stop-and-report)**: the clean-run
sequence refuses today at stage-entry step 2 — `configs/experiment.yaml` carries
`folds` / `embargo_hours` `TBD — freeze gate` and `configs/data.yaml` carries `stations` /
`cell_rule` `TBD — freeze gate`; the plumbing fixture's §15.3 minimal M-06 refuses on the
unfrozen TensorFlow pin; and this clone has no `numpy`/`pandas`/`pyyaml`/`pytest` (PyPI
unreachable — the stdlib pytest stand-in and Python 3.11.16 are the only runner). Every
test this pass writes therefore runs on synthetic trees; **no fixture runs, no measured
value appears, nothing is discharged.**

**Recorded input (nfr-design terminal READY, 2026-09-05 post-gate pass)**: one Minor —
`logical-components.md`'s Failure-domains table says "never a wrong result" for F4 while
SD-X-02 (Rec 7) discloses the uncontained receipt-tamper case. Addressed in the plan by
recording receipts through the append-safe registry (SD-X-02's routed fix), not by editing
the completed design artifact.

---

## Question 1
**The creation bar.** All three design artifacts state "Creation remains barred on the
blocker ground" — BLK-03/04/08/09 as exit conditions on 3.1 — and "no module, manifest,
receipt, emitter or `tests/fixtures/` directory is created". Since then BLK-03, BLK-04 and
BLK-09 were approved by change record, and the four sibling units carrying the same
inherited blockers (`models-and-baselines` under BLK-03; `evaluation-and-comparison`,
`statistical-inference`, `regimes-diagnostics-reporting` under BLK-08 ↓) were built under
explicit plan approvals with the open limbs carried as checked refusals. BLK-08's
mechanism limb and BLK-02 remain open. Build this unit's apparatus now?

A) Build the apparatus now — the manifest schema + one validating loader, the two-state
   manifest machinery (a measuring run may emit `candidate`; nothing here writes `frozen`),
   `run_walking_skeleton.py`, receipts + the exported two-receipt check, the in-session
   gate result, the three evidence emitters, and `tests/test_clean_run.py` with the 39
   controls on synthetic trees — with every evidence path refusing fail-closed until a
   Q-31 freeze exists, and BLK-08 ↓ a checked refusal (control 25). No manifest is
   authored by hand; the change record states the blocker state limb by limb
   > **Impact**: The last unit lands with its siblings' precedent (BLK-03 at models-and-baselines; BLK-08 ↓ at three units): the mechanism is real and testable today, and the owner's freeze act is the only thing that can make a fixture run count. Cost: the unit ends this pass with zero fixture runs and both manifests absent — stated, never claimed otherwise.

B) Defer — the unit stays barred until BLK-08's mechanism limb closes (D-27 reopened by
   a new D-number) and a `candidate` manifest exists from a measuring run
   > **Impact**: Nothing this unit owns exists; G-07's evidence path, the §9.2 ordering gate and TA-21's matrix stay prose; the Bolt ends at eleven of twelve units and a later pass re-opens this unit for artifacts its plan already owes. The measuring run that would produce a `candidate` manifest cannot happen without `run_walking_skeleton.py`, so B is circular on its own terms.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the bar's stated grounds have moved (three of four blocker contracts approved), the fourth is made a checked refusal by this unit's own R-139, and the deferral option is circular: the `candidate` manifest the design requires can only come from the orchestrator this option would not build. Honestly stated: BLK-02 does not close this pass and no fixture runs.

[Answer]: A

## Question 2
**The manifest loader's home** (R-133; routed to the gate with both candidates named). TE §12
names no module for it; `run_walking_skeleton.py` (a script), `tests/test_clean_run.py` and
the sibling tests R-122 points at the `tests/fixtures/<fixture_id>/fixture_manifest.yaml`
convention must all read through one loader. Where does it live?

A) `src/data/fixture_manifest.py` — a module in `foundation`'s package, imported by the
   orchestrator and the tests like the exception base is; the amendment ledger takes +1
   (8 across 6, recorded in the change record as owed, not applied); the only-copy
   "second YAML parse of a fixture manifest" check scopes project-wide
   > **Impact**: Reusable logic lives in `src/` (team.md § Code Style: scripts orchestrate, `src/` holds logic; notebooks and scripts hold no only-copy), the sibling tests import it the same way they import `src.data.splits`, and R-15 is untouched (a fixture manifest is not `configs/`). Cost: test-apparatus loading enters a production package, and a `component-methods.md` amendment is owed.

B) `tests/fixtures/_manifest.py` — a test-apparatus helper; `run_walking_skeleton.py`
   imports from the test tree; no amendment owed; the only-copy check scopes to this unit
   > **Impact**: No ledger entry, but a `scripts/` module imports from `tests/` — which §12 does not forbid and no other script does — and the sibling modules under `src/` that read manifest tolerances (`src/features/windows.py` already names the manifest path) would import test code from production.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — `src/features/windows.py` already consumes the manifest's tolerance by name from production code, so a test-tree home would put a production import edge into `tests/`; the ledger cost is one owed row, stated.

[Answer]: A

## Question 3
**Three §15.2 blocks name Phase 2 quantities Phase 1 may not produce** — Inputs (RINEX/CRX,
DCB), Processing (`gnss-tec` version, calibration commit), Independent reference checks
(STEC/VTEC intermediates, the hand-worked DCB pass). Requiring them non-empty on a Phase 1
manifest re-creates the §16 "all 20" contradiction. The design proposed, and did not apply,
a reading. Which does the schema enforce?

A) Apply the proposed reading — every one of the twelve blocks is required PRESENT; a
   Phase 2-only quantity inside a block is recorded `not_applicable` with its reason (the
   FR-P1-03-5 precedent); a missing block still fails, and `not_applicable` on a
   Phase-1-applicable quantity fails. Recorded in the change record as a §15.2 reading the
   owner approved at this gate
   > **Impact**: A Phase 1 manifest can validate without demanding raw-processing evidence §7.0 bars, and the block set stays the named twelve (the "thirteen" in REQ-ENG-4 stays a reported `requirements.md` correction, not applied here). Cost: an owner-approved reading of an authority table, recorded as such.

B) Require all twelve blocks non-empty as §15.2 literally reads — the Phase 1 manifests
   cannot validate until Phase 2, and the loader refuses them naming the three blocks
   > **Impact**: Faithful to the table's letter, unmeetable in Phase 1: neither fixture can ever validate before G-P2, so WS-20/TA-09/TA-17 have no Phase 1 evidence path at all.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it is the reading the design proposed, it mirrors an already-approved precedent (FR-P1-03-5), and B makes the unit's primary acceptance rows unreachable in the phase they belong to.

[Answer]: A

## Question 4
**The Phase 1 segment's data scope in the clean run, and how stages 05–07 reach fixture
scale** (R-137, R-138 — the gate item the design says must be ruled BEFORE any runtime
tolerance is frozen). The scientific fixture is March 2022 (D-14); under R-80's frozen list a
March-only frame can lawfully neither fit nor score, so the design proposes fixture-local
apparatus partitions (ids distinct from F1–F4/`REFIT`/`DEC`). But `05_build_features_and_splits.py`
takes `--partition` from `FITTING_PARTITION_IDS` only — no script can today run against an
apparatus partition. What does this pass build?

A) Fixture scale via apparatus partitions, with the scripts driven as scripts: the
   scientific manifest declares the apparatus partition set; `05`, `06` and `07` gain one
   additive option `--fixture-manifest <path>` that builds the apparatus partitions from the
   loader (never a frozen id), stamps `apparatus_partition_id` on every output and refuses a
   frozen id in a fixture artifact; `run_walking_skeleton.py` invokes the seven scripts with
   it. Three sibling scripts edited additively — flagged for `features-and-splits`,
   `models-and-baselines`, `evaluation-and-comparison`'s records (the Q2 = B sibling-edit
   precedent); the M10 step runs after the plumbing fixture; the clean run contains no
   full-year job, so control (27) is asserted on a synthetic tree
   > **Impact**: WS-12/WS-13/WS-16/WS-17 get a scientific-fixture path and the boundary "invokes every stage script" holds. Cost: three cross-unit additive edits whose READY code-summaries go stale under their receipts, carried to the gate; the runtime tolerance later frozen at fixture scale says nothing about confirmatory runtime (stated on the manifest).

B) Fixture scale, but `run_walking_skeleton.py` drives `src/` functions directly for 05–07
   with apparatus partitions — no sibling script is edited
   > **Impact**: No cross-unit edit, but the fixture never exercises the scripts' six-step stage-entry contract, TA-03/TA-26's "same sequence on both platforms" reads weaker, and the orchestrator re-implements the scripts' wiring — a second copy of orchestration the boundary forbids.

C) Full-year scope (January–November by construction, R-82 leaving December
   unmaterialised) — no apparatus partitions; the seven scripts run as written
   > **Impact**: Lawful before G-05 and no sibling edit, but the longest candidate, its runtime range changes again after G-06 adds December (a second freeze act later), and the scientific fixture itself still cannot fit or score under R-80 — WS-12/WS-13 evidence starvation returns through the side door.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it is the only candidate that keeps §15.3's "complete ladder" AND the unit boundary; the sibling edits are additive options with a refusal, on the precedent the owner set at evaluation-and-comparison. Honestly stated: the runtime tolerance that will eventually be frozen at this scope bounds nothing about a confirmatory run, and the manifest records that.

[Answer]: A

## Question 5
**Where the two-receipt check is called in full-year jobs** (R-140; routed to the gate).
`run_walking_skeleton.py` enforces order only for runs it starts; nothing yet stops a direct
full-year stage-script invocation, and a Kaggle session has no memory of a local run. The
exported check function exists either way; the question is its call site.

A) In-script assertion adopted by contract: each of the seven Phase 1 stage scripts calls
   `require_fixture_receipts(...)` inside `_stage_entry` right after `assert_lock_complete`,
   exempt when the run carries a fixture manifest (a fixture run is not a full-year job);
   seven additive one-call edits, flagged for the owning units' records
   > **Impact**: The §9.2 rule becomes a gate on every entry point, not a convention — including a direct invocation on Kaggle after a rebuild. Cost: seven sibling edits; and every full-year run refuses until both fixtures have passed under frozen manifests, which is exactly §9.2's intent but bites immediately.

B) Formalise a seventh stage-entry step in `services.md` (foundation's approved six-step
   surface) — an amendment this stage may not make; record it as owed, call site unbuilt
   > **Impact**: Cleanest contract, but nothing enforces the rule this pass; the amendment is the owner's and waits for foundation's next touch.

C) Exported check only; `run_walking_skeleton.py` calls it before the scientific fixture
   and before any full-year job it launches; direct stage-script invocations stay
   unchecked, recorded as the open gap
   > **Impact**: No sibling edit and honest about the hole — but it is the hole R-140 exists to close ("a convention, not a gate").

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the design's own argument against A's alternatives is that enforcement inside the orchestrator "reaches only runs it starts"; the in-script call is one line per script, exempt on fixture runs, and the Q2 = B precedent covers additive sibling edits under an owner ruling.

[Answer]: A
## Question 6
**Three design defaults, confirmed or changed in one place.** (i) Exceptions: violations raise
the base `IntegrityError` naming file and violated expectation — no `FixtureError` minted
(minting obliges the "fourteen"-representation sweep, and the base now counts 25 subclasses
anyway). (ii) Receipts: recorded as append-safe experiment-registry rows via
`append_registry_event` (SD-X-02 Rec 7), not free files, so they inherit NFR-AUD-01's
integrity. (iii) §15.3's reduced-replicate fixture bootstrap: declared in the scientific
manifest as apparatus constants (`fixture_bootstrap.replicates`/`scored_range`/`block_counts`,
board option 2), never in `experiment.yaml`.

A) Adopt all three defaults as designed
   > **Impact**: No READY text changes, receipts gain tamper-evidence for free, and R-118's control (17) is not collided with. Cost: a receipt lives in a registry row rather than a file a reader can `cat` — the check function reads the registry.

B) Adopt (ii) and (iii), but mint `FixtureError(IntegrityError)` at R-01's single site
   > **Impact**: Sharper catch lists for this unit's refusals; obliges the cross-representation sweep of every "fourteen" (already stale at 25) — recorded as owed, since the READY texts carrying it are completed-stage artifacts.

C) Adopt (i) and (ii), but register the fixture bootstrap as a predeclared
   `experiment.yaml` named run (board option 1 — a replicate count is protocol wherever it appears)
   > **Impact**: Consistent with R-118's pattern, but a config transcription of a value that does not exist yet (`TBD — freeze gate` sentinel until measured), and a timing smoke-test then appears in the registry as a scientific run.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — each default was argued in the design with its cost stated, the nfr-design gate ruled Rec 7 onto (ii), and neither alternative buys a control the defaults lack.

[Answer]: A
---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Q1 = A — **Build the apparatus now**: schema + one validating loader, the
  `candidate`/`frozen` machinery (nothing here writes `frozen`), `run_walking_skeleton.py`,
  receipts + the exported two-receipt check, the in-session gate result, the three evidence
  emitters, and `tests/test_clean_run.py` hosting the 39 controls and 11 must-not-fire on
  synthetic trees. Every evidence path refuses fail-closed until a Q-31 freeze exists;
  BLK-08 ↓ is a checked refusal (control 25); no `fixture_manifest.yaml` is authored by hand;
  BLK-02 stays open and no fixture runs this pass.
- Q2 = A — **Loader home `src/data/fixture_manifest.py`** (with `fixture_gate.py` and
  `fixture_evidence.py` beside it as one fixture-apparatus API); the amendment ledger takes
  **+1 → 8 across 6, owed not applied**; the only-copy YAML-parse check scopes project-wide.
- Q3 = A — **§15.2 `not_applicable` reading**: all twelve blocks required present; a Phase
  2-only quantity recorded `not_applicable` with reason; a missing block fails; `not_applicable`
  on a Phase-1-applicable quantity fails. Recorded as the owner-approved reading.
- Q4 = A — **Fixture scale via apparatus partitions, scripts driven as scripts**: the
  scientific manifest declares apparatus partition ids distinct from F1–F4/`REFIT`/`DEC`;
  `05`/`06`/`07` gain one additive `--fixture-manifest <path>` option; the orchestrator
  invokes the seven Phase 1 scripts in §13.2's order with it; the M10 step runs after the
  plumbing fixture; the clean run contains no full-year job (control 27 on a synthetic tree);
  the runtime tolerance later frozen at this scope bounds nothing about a confirmatory run.
- Q5 = A — **`require_fixture_receipts` called in all seven scripts' `_stage_entry`** right
  after `assert_lock_complete`, exempt on a fixture run; seven additive one-call edits
  flagged for their owners; every full-year run refuses until both fixtures pass under frozen
  manifests.
- Q6 = A — **Three defaults adopted**: refusals raise the base `IntegrityError` (no
  `FixtureError`); receipts and gate results are append-safe experiment-registry rows;
  `fixture_bootstrap` (`replicates`, `scored_range`, 24 h / 48 h `block_counts`) declared in
  the scientific manifest as apparatus constants.
- Fixed context riding every step: identity by citation (D-11, D-20, D-14 with both
  limitation clauses verbatim; `aruc_shortfall_status: dormant`); every measured field carries
  its measuring run's registry id; the §15.4 cross-check (20/19 outputs) and the per-output
  comparison ledger (`exact` by equality, never updated; `toleranced` with units); the
  sibling `.sha256` on `frozen` only and the D-number agreement check in F7; `smoke_only`
  stamped by the producing path on every plumbing artifact and its absence asserted on every
  evidence surface; `data07_caveat` + `december_representativeness` on every fixture-derived
  figure, both fixtures; December excluded on record dates via R-31 and
  `test_acquisition_window.py`'s predicate (no third copy); BSHM-only assembly after the
  four November artifacts verify; exactly two receipts; the executed command list compared
  to §13.2's Phase 1 enumeration parsed from the TE fence, `PYTHONHASHSEED=0` first, no GPU
  visible, a Phase-2-only invocation raising `PhaseBoundaryError`; TA-09 bounded to WS-01 +
  WS-09…WS-20 with any WS-02…WS-08 row a raise; TA-27 first-limb only;
  `aws_ai_dlc_preflight_report` built nowhere here; no `iri.py`/`gim.py` import; hashing only
  via `release.sha256_of_file`; the two fixture trees created WITHOUT manifests; change
  record FIRST; smoke via the scratchpad 3.11.16 + stdlib stand-in; no commit.
- Honest limits: the clean-run completion test SKIPS with the named stop-and-report reason
  (`TBD — freeze gate` fields in `experiment.yaml`/`data.yaml`, the unfrozen TensorFlow pin,
  absent `numpy`/`pandas`/`pyyaml`, absent manifests); WS-20, TA-09, TA-17, TA-21 stay
  `Pending`; TA-15 not covered; the §15.2 12-not-13 REQ-ENG-4 correction, the FR-WS-2/FR-WS-3
  candidate §15.2 rows and the M10 §13.2 placement are gate proposals, not applied; BLK-02
  and BLK-08 ↓'s mechanism limb stay open; nothing discharged.

- Looks correct
- Request changes

[Answer]: Looks correct

---

## Plan Approval

The code-generation plan for `fixtures-and-reproducibility` is at
`construction/fixtures-and-reproducibility/code-generation/code-generation-plan.md` —
10 steps: change record FIRST with the blocker state, the owed amendment, the §15.2 reading,
the data-scope ruling, the cross-unit edit table, the two candidate §15.2 rows and the M10
placement proposal (1); `src/data/fixture_manifest.py` — the one schema and the one
validating loader, sibling-hash check on `frozen`, the comparison ledger, `fixture_bootstrap`
and the apparatus partitions (2); `src/data/fixture_gate.py` — receipts as registry rows, the
exported two-receipt check, the in-session gate result (3); `src/data/fixture_evidence.py` —
the matrix, the 13-row acceptance table, the G-07 preflight report, the stamps and the
D-number agreement check (4); `scripts/run_walking_skeleton.py` — the orchestrator, plumbing
lineage, record-date exclusion, the seven scripts as subprocesses at fixture scale, the M10
step, `--emit-candidate` (5); additive edits to the seven sibling scripts (6); the two fixture
trees without manifests (7); `tests/test_clean_run.py` with the 39 controls and the
skip-with-reason completion test (8); smoke + regression + lint (9); governance stop (10).

- Approve Plan
- Request Changes

[Answer]: Approve Plan
