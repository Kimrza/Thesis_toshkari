# Load Test Results — Performance Validation (4.6)

**Stage:** performance-validation (4.6) · **Lead:** aidlc-quality-agent
**Date:** 2026-09-29 · **HEAD:** `2dd36a756e72c2a09e8bc5ecfac6f8bd24f11a4a` · **Plan:** `load-test-plan.md`
**Revision 2, 2026-09-29.** Rewritten under the Student's rulings on `GOV-2026-09-29-PV-01`
(`governance/CHANGE_RECORD_2026-09-29_GOV-PV-01_rulings.md`). Revision 1 understated several
facts, and each correction here is marked with its Recommendation number. Every figure in this
revision was re-derived from disk and printed before being written.

> **Model performance is NOT MEASURED.** This file reports pipeline performance only. No
> December 2022 quantity was opened, read, or computed. The board's Validation Auditor verified
> this independently:
> - `locked_test_accessed` is false on all 1,657 registry rows;
> - nothing was appended to any access log during 16:48–16:55Z;
> - the restricted root is unchanged.

## M-1 — Commit-anchored `plumbing_7day` measuring run

### What was run

| Item | Value |
|---|---|
| Run id | `walking-skeleton-plumbing_7day-20260929T164824Z-d139bf12` |
| Registry status | **`aborted`** (orchestrator `started` → `aborted`) |
| Registry rows appended | **52**: 2 orchestrator rows plus 50 stage rows (25 started/completed pairs). All carry `code_commit 2dd36a75…`, `platform: local`, `locked_test_accessed: false`. *(Corrected, PV-01 Rec 18.)* |
| Code commit | `2dd36a7`. `src/`, `scripts/`, `configs/` and `tests/` were clean at launch; that clean state is recorded in this prose only, in no artifact field (PV-01 Rec 6). |
| Orchestrator exit code | **1** *(added, PV-01 Rec 18)* |
| Wall time | 16:48:10Z → 16:54:44Z, `real 6m33.965s` |
| Platform | local; native Windows 11; `tec-thesis-311`: CPython 3.11.16, TF 2.21.0, CPU only; `PYTHONHASHSEED=0`; `CUDA_VISIBLE_DEVICES=""` |
| Environment pin status | **Off-pin: `ml_dtypes` 0.5.4 installed, pin 0.5.3** (`requirements.txt:41`; `environment/wheels-win64.lock`). Disclosed only, per the Student's ruling on PV-01 Rec 9. The `391a319` suite runs in M-2 are affected too. **Full drift, corrected 2026-09-30 (`GOV-2026-09-29-PV-02` Rec 7 = 2):** the one-pin figure above understated it. The environment was **not built from the committed locks**:<br>• pip layer: 3 of 32 `wheels-win64.lock` entries drift (`ml_dtypes`, `setuptools` 83.0.0 vs 84.0.0, `wheel` 0.47.0 vs 0.48.0), and **6** of 61 pip packages sit in neither lock (`distlib`, `filelock`, `platformdirs`, `python-discovery`, `uv`, `virtualenv`). A further 16 are pinned in `conda-win64.lock`, and two of those drift: `fonttools` 4.65.0 vs 4.66.0 and `pytz` 2026.3.post1 vs 2026.4. *(Corrected 2026-09-30, `GOV-2026-09-30-PV-03` Rec 1. This first read "22 of 61 … in neither lock", because the conda lock was never checked.)*<br>• conda layer: 20 packages installed, against 119 in the lock; **0 of the 20 build strings match the lock**; Full conda-layer drift: 10 version, 7 build-only, 3 absent from the lock; see the snapshot README table (PV-04 Rec 23).<br>• Python build: Anaconda `hb00fc5c_0`, where the lock pins conda-forge `hb12b558_2`.<br>**Accepted consequence (PV-02 Rec 7 = 2):** environment (a) can be *verified* against its recorded identity, but not *rebuilt* from the committed locks or from that record. G-07 evidence must say so (PV-03 Recs 8 and 25).<br>Source: `evidence/environment_identity_2026-09-30_tec-thesis-311/README.md`. |
| IRI input consumed | B-01 rows generated **on WSL2 on 2026-09-28** under D-49 addendum 2 (`artifacts/external/b01/`, `rows_sha256 0035a00f…`). *(Undisclosed in revision 1, PV-01 Rec 1.)*<br>**Wheel identity: declared, not measured** (`GOV-2026-09-29-PV-02` Rec 27 = 2): the install did not use `--require-hashes`, and libgfortran was not recorded. The sidecar note is `artifacts/external/b01.WHEEL_IDENTITY_NOTE.md` (PV-03 Rec 24).<br>**Receipt superseded** (PV-03 Rec 12 = 3): the configs are to be renormalised to `eol=lf`, and the B-01 fixture re-run.<br>**Config hash (PV-02 Rec 31, checked 2026-09-30):** the B-01 identity records `experiment.yaml` as `10028bf0…`, and this run's snapshot recorded `8427794f…`. The difference is line endings only: `10028bf0…` is the CRLF rendering of the `989f290` blob, whose LF hash is `8427794f…`. The content is identical. Because the environment identity (D-49 item 4) hashes config bytes, line-ending churn alone breaks an identity match. Routed as D-83 revision 5 §R5-5 item 13. *(repointed 2026-09-30 to D-83 revision 5, PV-04 Rec 2; item numbers are unchanged from revision 3)* |

### Measured values and what they actually measure

Source: `measuring_result_walking-skeleton-plumbing_7day-20260929T164824Z-d139bf12.json`, SHA-256 `a5014116f36abb89976248022c08e2be9756cdd64a077bf1f544ee34445d95e7`.

| Quantity | This run | Earlier runs (`978317da`, `4a959333`) | Fit for a Q-31 freeze? |
|---|---|---|---|
| `runtime.cpu_total` | 378.75 s | 365.156, 366.109 s | **No, not as labelled.** It is wall-clock time. |
| `runtime.storage_total` | 19,375,740 B | 14,778,806, 17,076,359 B | **No.** It is dominated by archived copies. |

**`cpu_total` is wall-clock time, not CPU time** *(PV-01 Rec 5; revision 1 called it CPU runtime).*
The value is `time.monotonic()` elapsed time (`run_walking_skeleton.py:819, 992, 1042`), whereas
TE §15.2 asks for an expected CPU range. Per-stage wall time comes from each run's
`test_report.json` (the `HEAD` copy is run `4a959333`; the working tree is `d139bf12`):

| Stage | `4a959333` (s) | `d139bf12` (s) | Δ (s) |
|---|---|---|---|
| 00 | 11.046 | 10.953 | −0.09 |
| 01 | 15.407 | 15.390 | −0.02 |
| 02 | 10.922 | 11.000 | +0.08 |
| 04 | 82.640 | 85.641 | **+3.00** |
| 05 | 11.485 | 14.031 | **+2.55** |
| 06 | 210.140 | 216.375 | **+6.24** |
| 07 | 15.250 | 15.328 | +0.08 |
| Sum of stages | 356.89 | 368.72 | +11.83 |

- Where the change sits: in stages 04–06. Stages 00–02 and 07 are within ±0.1 s.
- Why: that is consistent with a wall-clock quantity on a host whose load was not controlled.

**Owed to the Student before Q-31:** a ruling on what §15.2 means:
- process CPU seconds, which needs a code change to record CPU time; or
- wall time on a controlled host.

**`storage_total` mostly measures archive history** *(PV-01 Rec 4; revision 1 said "Not verified").*
`_storage_bytes` (`run_walking_skeleton.py:803-804`) sums every file under the fixture root
with `rglob`. The fixture root's current contents, derived with `find … -printf "%s %p"`:

| Class | Bytes | Share |
|---|---|---|
| `*.archived-*` and `archived_releases/` (11 archive generations) | 15,317,096 | 78.8% |
| of which `archived-pv-2026-09-29`, this stage's archive | 2,153,597 | |
| of which `archived-q31-closure-run1` | 2,150,701 | |
| Historic `releases/plumbing_7day_<ts>` (18 dirs) | 1,554,714 | 8.0% |
| `measuring_result_*.json` (3 files) | 184,851 | 1.0% |
| **Live outputs** | **2,392,814** | 12.3% |
| Total | 19,449,475 | |

- **Growth per run:** +2,297,553 B, then +2,299,381 B. Each matches one archive set (about 2.15 MB), one release directory (86,373 B) and one measuring result.
- **The existing candidate's storage range is contaminated the same way.**
- **Uncounted bytes:** stages 00–02 also write outside the root (`artifacts/acquisition/`, `inventory/`, `prepared_target/`). Those bytes are never counted.

**Owed to the Student before Q-31:**
1. A code ruling on the storage measure: either exclude `*.archived-*`, historic releases and measuring results, or measure only this run's declared outputs. Either option needs a negative control.
2. Fresh runs in a clean root.

**`mask_manifest.json` is contaminated too** *(PV-01 Rec 4; not in revision 1).*
- `07_evaluate_and_report.py:1703-1707` globs `mask_registry/*/mask_*.json`, which also picks up renamed `FIX-NOV-FOLD-0x.archived-*` directories.
- Entry counts across the three runs: 8, 12, 16. Only 4 of them are unique `mask_id`s.
- The candidate classes this output as `exact`, so it is not fit to freeze either.

### Outcome: aborted at candidate composition

> `run_walking_skeleton: aborted: measuring result walking-skeleton-plumbing_7day-20260929T133040Z-978317da: duplicate measuring_run_id across the aggregated results; every measuring run is one recorded execution (NFR-AUD-01; board Rec 5)`
>
> *(Restored to the verbatim program output on 2026-09-30, under `GOV-2026-09-30-PV-05` Rec 1. The prefix script had inserted "PV-01". "board Rec 5" here is the code-generation-era board cited in `scripts/run_walking_skeleton.py:1078`; it is **not** PV-01 Rec 5.)*

- **Cause.** The invocation passed two local results through `--measuring-runs`. Step 9 already aggregates those from the root, so the guard refused correctly.
- **Departure from the confirmed plan.** The confirmed summary did not include that flag (PV-01 Rec 8; see the `load-test-plan.md` M-1 correction).
- **Result.** No third candidate manifest was written.
- **Corrective run: deferred (FU-3 = A, 2026-09-29).** No corrective run happens in this stage. It
  waits for two code rulings, PV-01 Rec 4 (the storage measure) and PV-01 Rec 5 (CPU seconds), and for a
  clean fixture root. It then becomes the Student's first designated Q-31 measuring run, using the
  corrected command in `load-test-plan.md` M-1. *(Corrected 2026-09-29 at the gate's Request Changes.
  Before, this line said the choice was still open at the gate, although FU-3 had already answered it.)*

### Fixture-root custody after the run *(PV-01 Rec 7; revision 1 said only "nothing deleted")*

**What was renamed.**
- No bytes were deleted.
- 30 paths (183 files, 2,153,597 B) were renamed to `*.archived-pv-2026-09-29`.
- 180 of the 183 archive files are git-ignored (`.gitignore:117 *.archived-*`, tracking policy B), so `git status` shows **101 tracked deletions**. All 101 are byte-identical to their archive copies; the Data & Reproducibility seat and the closure verification both checked this.
- **Exception, found by the closure verification:** the 3 files under `releases/gim_comparator_C-01_2022.archived-pv-2026-09-29/` are **not** ignored. `.gitignore` l.119–120 deliberately re-includes archived releases ("An archived RELEASE is still a release: keep it committed", TE §13.3); `git check-ignore -v` shows that l.120 is the rule matching these files. Under policy B they are therefore to be **committed** at the Student's commit (O-5), which now names them:
  - `releases/gim_comparator_C-01_2022.archived-pv-2026-09-29/excluded_rows.json`
  - `releases/gim_comparator_C-01_2022.archived-pv-2026-09-29/gim_comparator.parquet`
  - `releases/gim_comparator_C-01_2022.archived-pv-2026-09-29/release_manifest.json`

  *(Corrected 2026-09-30, `GOV-2026-09-29-PV-02` Rec 26: the line citation previously read l.118–119, and l.118 is the comment.)*

**What was overwritten.**
- **13 tracked files were overwritten in place.**
- Six of them are run-level files with no archive copy: `clean_run_log.json`, `artifact_manifest.json`, `registry_entry.json`, `test_report.json`, `processing_config_snapshot.yaml` and `external/ec1_driver_audit_manifest.json`. Run `4a959333`'s bytes for those six survive only as `9710daf:` and `2dd36a7:` blobs.
- **One of the 13 is a TE §13.3 release object.** *(Disclosed 2026-09-30, `GOV-2026-09-29-PV-02` Rec 26.)*
  - **What changed.** The canonical `releases/gim_comparator_C-01_2022/release_manifest.json` was rewritten in place at its canonical path. It differs from `HEAD` only in `created_at_utc`.
  - **Where the prior bytes are.** The SHA-256 of the `HEAD` content, `0df5558c…`, equals the pv archive copy; the git blob id is `020c6500`. *(Wording corrected 2026-09-30, PV-03 Rec 30.)*
  - **What did not change.** `gim_comparator.parquet` (`738124cd…`) and `excluded_rows.json` (`4f53cda1…`) are byte-identical across the live copy, the archive and `HEAD`.
  - **Consequence.** One `dataset_version` (`f04fc0e27f7d`) now has three distinct manifests. TE §13.3 says a release is "stored under a new version rather than overwritten", so this is a bounded breach of that rule. It is fixture-class, and the prior bytes survive.
  - **Commit.** Both copies are committed at O-5.
  - **No code change.** The Student chose PV-02 Rec 26 option 1, so no code ruling for the release writer follows from this.

**What the live root now describes.**
- The live fixture root describes the **aborted run `d139bf12`**.
- The existing candidate `…-4a959333.yaml` reads its hash listing from the mutable `artifacts/walking_skeleton/plumbing_7day/artifact_manifest.json`, and 6 of its 19 hashes now differ.
- **Do not promote that candidate** until a clean-root run exists.

**Manifest and commit status.**
- Policy B requires a hash manifest for untracked archives. The supplementary manifest `artifacts/untracked_outputs_manifest_2026-09-29_pv.json` now provides it for the pv set.
- **Nothing is committed yet**: not the stage files, the 52 registry rows, the measuring result or the supplementary manifest. Committing them is the Student's act.

## Registry `code_commit` finding, scope corrected *(PV-01 Rec 6; revision 1 named 2 runs)*

**What the registry records.**
- **648 registry rows across 15 walking-skeleton runs** carry `code_commit 208f138…`.
- They span 2026-09-28T17:58Z to 2026-09-29T13:37Z.
- 14 of the 15 runs are `aborted`, including `978317da`; only `4a959333` completed.
- Commit `9710daf` (2026-09-29T13:57Z) later changed `src/` and `scripts/` heavily.
- Derivation: a `bun` pass over `experiment_registry.jsonl`, filtered on `code_commit` prefix `208f138`, gives 648 rows and 15 walking-skeleton `run_id`s.

**What can and cannot be concluded.**
- Which code each of those runs executed cannot be determined per run. The disclosure therefore covers all 15.
- The only corroboration: run `d139bf12`, on code identical to `9710daf`, produced the same `metrics.json` and `predictions.parquet` fingerprints and the same non-runtime measurement blocks as `4a959333`.
- So "`4a959333` ran `9710daf`-equivalent code" is **corroborated, not proven** *(PV-01 Rec 18; revision 1 stated it as fact).*

**Cause** *(PV-01 Rec 6; revision 1 said "the orchestrator passed HEAD").*
- **The operator override.** The operator supplied `--code-commit 208f138…` explicitly, on a machine with a git tree. The flag is documented only for use "where no git tree exists (Kaggle)", and nothing enforces that.
- **The dirty-tree gap.** Independently, `_git_head` (`src/data/config.py:1216`) has no dirty-tree check, so every stage script would record `HEAD` on a dirty tree.

**Owed to the Student:**
1. A dirty-tree guard in `capture_environment_lock`.
2. A `--code-commit` refusal when a git tree exists.
3. A `working_tree_dirty` field.

Each needs a negative control at every entry point. Registry rows stay append-only (NFR-AUD-01), so the fix is a disclosure, never an edit.

## R-20 `exploratory` flag reads two different access logs *(PV-01 Rec 14; not in revision 1)*

- **Two sources.** Script 00 derives `exploratory` from `evidence/test_run_access_log.jsonl`, which is closed and holds test rows. Scripts 01–07 and the orchestrator derive it from `evidence/merge_run_access_log.jsonl`, which **does not exist**.
- **Effect in this run.** In `d139bf12` the 2 acquisition rows are `exploratory: true` and the other 48 are `false`.
- **Effect across the registry.** 172 of 1,657 rows are `true`. Of these, 144 are acquisition rows, driven entirely by test-suite rows. The other 28 were not attributed in this pass.
- **Consequence.** The flag is not reliable custody evidence yet.
- **Owed to the Student before the pre-G-05 audit:** a ruling naming one governed access log, held as a single constant, with a test.

## M-2 — Suite timings (cited, not re-run)

| Code | §18.3 selection (b) | Full suite | Source |
|---|---|---|---|
| `9710daf` **plus an uncommitted test edit** *(PV-01 Rec 18; revision 1 said "at `9710daf`")* | 105.8 s (1423 tests) | 660.7 s (2456 tests) | `build-test-results.md` §§ 2026-09-29 (`run_2026-09-29_bt_fix`) |
| `391a319` | 62.5 s, 1426/1426 | 1007.7 s, 2455 passed / 0 failed / 4 skipped of 2459 | `build-test-results.md` § post-commit re-run |

The two rows differ in suite size and in code. Host load is therefore a plausible explanation
of the difference, not a measured one. Both ran with `ml_dtypes` 0.5.4, off-pin.

## M-3 — Determinism (cited)

- `test_determinism.py`, `test_bootstrap.py` and `test_checkpoint_restore.py` are inside the `391a319` full-suite pass (0 failed).
- Run-level evidence: fingerprints and non-runtime measurement blocks are identical across `978317da`, `4a959333` and `d139bf12` *(PV-01 Rec 18)*.

## IRI-2016 workload timing, Vision §6.11 *(PV-01 Rec 18; not in revision 1)*

- **The only local measurement:** 2,160 calls with `workload_seconds` 535.353 (4.03 calls/s), on WSL2, CPython 3.10, glibc 2.43, November only (`artifacts/external/b01/b01_provenance.json`).
- **Unreconciled:** the session record gives 527.6 s for the same generation.
- **Full workload:** the 26,000-call figure stays **NOT MEASURED** (Q5 = A).

## Not measured

| Item | Why | Owner / due |
|---|---|---|
| Peak RAM, CPU model, GPU type (TE §9.2) | Only `platform.machine()` is recorded (`config.py:1292`), and nothing captures RSS | Student: a code ruling (PV-01 Rec 16) or an external measurement in M-4; before G-07. The RSS / CPU-model capture is also a **precondition of D-83 adoption** (`GOV-2026-09-29-PV-02` Rec 12 = 1; D-83 revision 5 §R5-5 item 3). *(repointed 2026-09-30 to D-83 revision 5, PV-04 Rec 2; item numbers are unchanged from revision 3)* |
| Local preflight install from pins (M-4) | Student-operated; now un-gated from D-83 | Student; before G-07 |
| Full-year B-01 on the local route | Receipt identity and identity checks (plan M-5) | Student; before any full-year B-01 run |
| Kaggle limb of TE §9.2 | FU-1R is answered (A). The limb now depends on the adoption and countersignature of D-83 (revision 5, 2026-09-30), whose adoption is itself gated on the RSS / CPU-model capture and a local `scientific_1month` measurement. *(Corrected 2026-09-30, PV-02 Rec 24: this previously read "Depends on the FU-1R answer".)* | Student and Supervisor |
| `scientific_1month` | Never run; manifest candidate `TBD — freeze gate` | Student (Q-31) |
| Full-year runtime | Q5 = A | First Class C run |
| Any model performance | `nfr-validation-matrix.md` § B | G-05 / G-06 / G-08 |

## Sources

- `load-test-plan.md`; `performance-validation-questions.md`; `governance/CHANGE_RECORD_2026-09-29_GOV-PV-01_rulings.md`
- `artifacts/walking_skeleton/plumbing_7day/measuring_result_…-d139bf12.json`; `test_report.json` (working tree and `HEAD`); `artifacts/registry/experiment_registry.jsonl`
- `artifacts/external/b01/b01_provenance.json`; `evidence/DECISIONS.md` D-49 addendum 2
- `construction/build-and-test/build-test-results.md`; code-generation outputs (`code-generation-plan.md`, `code-summary.md`) via build-and-test
- `scripts/run_walking_skeleton.py` l.803–804, 819, 992, 1033–1080 (the step-9 aggregation glob is at l.1066–1068); `scripts/07_evaluate_and_report.py` l.1703–1707; `src/data/config.py` l.1216, 1292
