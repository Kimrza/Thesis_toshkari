# Load Test Plan — Performance Validation (4.6)

**Stage:** performance-validation (4.6) · **Lead:** aidlc-quality-agent
**Date:** 2026-09-29 · **HEAD:** `2dd36a7` · **Answers:** `performance-validation-questions.md` (Q1=A, Q2=B via FU-2=A, then FU-3=A (corrective run deferred), Q3=A, Q4=X via FU-1R=A (FU-1=A superseded; it was given on a false fact), Q5=A)

> **Model performance is NOT MEASURED by this stage.** This plan validates *pipeline*
> performance. Every model-performance check is declared in `nfr-validation-matrix.md`
> § B as NOT MEASURED, with its blocking gate. Nothing here opens, reads, or computes any
> quantity on the locked December 2022 set.

## Why "load testing" means something else here

The stage prose assumes a deployed service measured under traffic (CloudWatch, X-Ray,
auto-scaling). This project has none of those (`team.md` § Deployment). The upstream
artifacts this stage consumes are **absent by design**, and nothing is invented in their
place:

| Consumed artifact | Status | Why |
|---|---|---|
| `performance-requirements` | absent for all 12 units | every unit is `kind: library`; `nfr-requirements` `produces_kinds` limits it to `service`/`ui` |
| `scalability-requirements` | absent for all 12 units | limited to `service` by the same rule |
| `performance-design` | absent | its producing requirement does not exist |
| `scalability-design` | absent | its producing requirement does not exist |
| `dashboards` | absent | `observability-setup` is SKIP in `research-pipeline-governed` |

The performance-type requirements that do exist come from the governing documents and
from `construction/build-and-test/performance-test-instructions.md`:

| ID | Requirement | Source |
|---|---|---|
| P-1 | CPU is a complete execution path; GPU is an optional accelerator; no GPU-only dependency | TC-01; TE §9.2; Vision §9.2 |
| P-2 | Runtimes, storage and tolerances are **measured** from the fixtures, then frozen by the Student, never invented | TE §15.1–§15.2; Q-31 |
| P-3 | Determinism under fixed seeds; `PYTHONHASHSEED=0` for the clean-run sequence; nondeterministic ops recorded | NFR-DET-01; TC-21 |
| P-4 | Preflight evidence: install from pins, a completed skeleton run, measured CPU runtime, RAM and storage on the platform(s) that execute governed runs | TE §9.2; TC-03g |
| P-5 | Every run records CPU/GPU type, runtime, peak memory where available, platform and environment hash | TE §9.2 |
| P-6 | Both fixtures pass, in order, before any full-year job | TE §9.2; `project.md` Mandated |

## Platform assumption for this plan (FU-1R = A; D-83 proposed and not enacted)

*Heading corrected 2026-09-30 (`GOV-2026-09-29-PV-02` Rec 24). It read "FU-1 = A", which was
superseded by FU-1R = A. D-83 is now at revision 5 (2026-09-30; repointed under PV-04 Rec 2 from "revision 3"). That revision makes a peak-RSS /
CPU-model capture and a local `scientific_1month` measurement **preconditions of its adoption**
(PV-02 Rec 12), and it lists further code rulings before G-06 and G-07. See
`governance/CHANGE_RECORD_2026-09-29_platform_local_only.md` Revision 5 (§R5-5). *(Repointed 2026-09-30, PV-05 Rec 2; this previously read "Revision 3".)*

The Student chose **local as the sole execution platform** (FU-1 = A). That choice amends
TE §9.1/§9.2 and D-129, so it is drafted as
`governance/CHANGE_RECORD_2026-09-29_platform_local_only.md` (proposed D-83). It is **not
enacted** until the Student adopts it and the Supervisor countersigns. This plan therefore
measures on local only and lists no Kaggle measurement. The TE §9.2 "both platforms" limb
stays **open, pending that ruling**; it is not claimed satisfied.

> **Correction, 2026-09-29 (`GOV-2026-09-29-PV-01` Rec 1).** The FU-1 answer above was given
> on a false fact: that B-01 runs only on Kaggle. D-49 addendum 2 (2026-09-28) already rules
> WSL2 on this laptop in as `local` for B-01, and B-01 ran there on 2026-09-28. The change record
> is **SUSPENDED**, and FU-1 is re-put to the Student as FU-1R. This section is re-issued after
> that answer.

**Re-issued 2026-09-29 after FU-1R = A (answered on corrected facts).** The change record now
carries **revision 2** of the proposed D-83. Under that revision:

- the laptop is the sole platform for new governed runs, in three named environments:
  - native-Windows `tec-thesis-311`;
  - WSL2 `b01_iri`, under D-49 addendum 2;
  - a WSL2 G-07 clean-run environment with the full 3.11 pins;
- Kaggle is **dormant**, not retired, until a local `scientific_1month` measurement exists.

D-83 is still **not enacted**: it needs the Student's adoption, the Supervisor's
countersignature, and a full-board review scoped to G-06 and G-07.

This plan therefore:
- measures on local only;
- names the WSL2 clean-run environment for M-4's reproduction limb;
- plans no Kaggle measurement.

It claims no platform requirement as satisfied, and no locked-test activity on local is planned
(D-83 revision 2 §R3 item 1).

## Measurement plan

### M-1 — Commit-anchored fixture runtime (executed this stage)

Resolves Q2 = B through FU-2 = A.

1. Archive the current `plumbing_7day` derived outputs by rename to
   `*.archived-pv-2026-09-29`, never deleting them. This follows the rename set
   `CR-2026-09-29-Q31-CLOSURE` used for run 1; there are 30 paths.
2. Record `git rev-parse HEAD` and `git status` for `src/`, `scripts/`, `configs/` and
   `tests/`. They must be clean.
3. Run the measuring pass on local CPU in `tec-thesis-311`:
   ```bash
   export PYTHONHASHSEED=0
   python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day \
     --emit-candidate --identity tests/fixtures/plumbing_7day/identity_declaration.yaml \
     --measuring-runs <run 978317da result> --measuring-runs <run 4a959333 result> \
     --table-caption "<the Student's caption, forwarded verbatim from run 4a959333>"
   ```
4. Read runtime and storage from this run's `measuring_result_<run_id>.json`, not from
   console timing. Record the orchestrator's wall time and exit code as well.
5. If any stage refuses, the refusal is the result. It is recorded verbatim and nothing is
   worked around.

> **Correction, 2026-09-29 (`GOV-2026-09-29-PV-01` Rec 8).** The command in step 3 is **the
> command that was executed and failed. It departed from the confirmed summary**, which named
> only `--emit-candidate --identity …`; the two `--measuring-runs` flags were added without
> asking. Step 9 of `run_walking_skeleton.py` (l.1033–1039) already folds in every
> `measuring_result_*.json` under the fixture root. `--measuring-runs` is for results from
> *another environment's* fixture root. Passing the local results through it counted each
> twice, and the NFR-AUD-01 duplicate guard aborted the run after stages 00–07.
>
> Corrected command for any future local measuring run. Do **not** pass `--measuring-runs`
> for results already under the root:
> ```bash
> export PYTHONHASHSEED=0
> python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day \
>   --emit-candidate --identity tests/fixtures/plumbing_7day/identity_declaration.yaml \
>   --table-caption "<the Student's caption, verbatim>"
> ```
> Do not run it before the PV-01 Rec 4 storage ruling and a clean root; otherwise it composes
> archive-contaminated storage and `mask_manifest` values. Whether to run it at all was put to the
> Student as FU-3 (PV-01 Rec 8), who answered **A: deferred**. The run waits for the PV-01 Rec 4 storage
> ruling and the PV-01 Rec 5 CPU-seconds ruling, and for a clean root. It then becomes the Student's
> first designated Q-31 measuring run, using the corrected command above. *(Corrected 2026-09-29
> at the gate's Request Changes. Before, this said the question was still open at the gate.)*
>
> **Preconditions of the designated runs** *(added 2026-09-30, `GOV-2026-09-29-PV-02` Rec 25 = 1)*:
> 1. **Citation corrected.** The step-9 aggregation is at `run_walking_skeleton.py` l.1066–1068.
>    The l.1033–1039 cited above is a comment.
> 2. **"Clean root" is defined** as follows: every prior `measuring_result_*.json` under the
>    fixture root is relocated **by rename**, never deleted, before the first designated run.
>    That covers `…978317da`, `…4a959333` and `…d139bf12`, which carry the contaminated storage
>    values. The relocation goes on record with the same archive-by-rename and manifest
>    discipline as `*.archived-pv-2026-09-29`.
> 3. **The run set is precommitted** *(added 2026-09-30, `GOV-2026-09-30-PV-03` Rec 5)*. Before
>    the first designated run, the Student records the following, and every designated run is
>    included:
>    - the planned run count **K ≥ 2**, a value the Student sets and no one else supplies;
>    - one designated slot per run;
>    - the rule for extra runs if a zero-width refusal occurs, fixed in advance;
>    - **an abort limb** *(PV-04 Rec 12)*: a designated run that aborts or crashes stays on
>      record. It is re-run only under the precommitted extra-run rule, and never replaced by
>      choice.
>
>    **Where the precommitment is recorded** *(PV-04 Rec 12)*: a file committed to git **before**
>    the first designated run starts, so that its commit precedes that run's first registry row.
>    The file carries K, the slots, the extra-run rule, the abort limb and the rejection grounds.
>
>    A rejected run set stays on record. Any replacement set is reported alongside it; it never
>    replaces it silently.
>
>    **At least two designated runs are required.** Step 9 aggregates every result left under
>    the root, and `compose_measurement_ranges` refuses a zero-width range
>    (`fixture_manifest.py` l.1792–1806). A single run on a clean root therefore cannot compose
>    a candidate.
> 4. **Pins must be exact first.** `ml_dtypes==0.5.3` is restored, and a pin check against
>    environment (a)'s recorded identity has passed and is captured in each run's evidence
>    (D-83 revision 5 §R3-5 item 3; the ordering obligation is §R5-5 item 8, per PV-07 Rec 23). *(repointed 2026-09-30 to D-83 revision 5, PV-04 Rec 2; item numbers are unchanged from revision 3)* This keeps the baseline and tolerance from being measured
>    off-pin.
>
>    **Which identity, and which obligation** *(PV-05 Recs 4 and 5, 2026-09-30)*: the check runs
>    against **the post-restore committed identity file** (D-83 §R5-5 item 8), **not** the
>    2026-09-30 pre-restore baseline, which records `ml_dtypes` 0.5.4. The ordering obligation,
>    "restore, then the pin check, before item 4", is §R5-5 item 8.
>
>    **How the pin check is done** *(PV-04 Rec 18)*: the code-level conformance check (D-83 §R5-5
>    item 10) has its pin limb moved to before §R5-5 item 4. It must therefore exist before the
>    designated runs, and it is captured in each run's evidence.

Each designated run writes its candidate manifest **next to** the existing one and never
replaces it. Nothing is frozen. The run is TC-03f smoke evidence, never scientific evidence.

**What the Q-31 act does.** It either promotes the candidate composed from the **designated
clean-root runs**, or rejects that candidate. **A rejection is allowed only on a precommitted,
closed list of grounds** *(PV-04 Rec 12, 2026-09-30)*:
- an integrity failure (hash mismatch, missing manifest, violated invariant);
- contamination of the root or of the inputs;
- a precondition of this list not met at run time.

On any other ground, the candidate is promoted. It does not choose among
candidates after seeing their values. *(Narrowed 2026-09-30, PV-02 Rec 25 = 1. The earlier wording, "chooses which candidate to
promote", allowed choosing a measurement after its result was seen.)*

### M-2 — Suite timings (existing evidence, cited)

The §18.3 selection (b) and the full-suite wall times at `9710daf` and `391a319`, from
`construction/build-and-test/build-test-results.md`. Host load is disclosed, as it was there.

### M-3 — Determinism (existing evidence, cited)

`test_determinism.py`, `test_bootstrap.py` and `test_checkpoint_restore.py` are all inside
the 2455/2459 full-suite pass at `391a319` (0 failed). Nothing is re-run: `2dd36a7` touches
no code.

### M-4 — Local preflight (future, the Student operates)

*Un-gated 2026-09-29 (PV-01 Rec 19): TE §9.2 requires the local limb whether or not D-83 is
adopted.* Run it on the laptop:

1. Install from pins through the project's actual reconstruction path,
   `environment/bootstrap_env.ps1` (`conda-win64.lock` plus `wheels-win64.lock`; see
   `environment/OFFLINE_REBUILD.md`), into a fresh environment. Record the log. The earlier
   wording "from `requirements.txt`" did not match that path (PV-01 Rec 9, BENCH-13). *(PV-05 Rec 6, 2026-09-30: this attribution cannot be verified. The PV-01 report was never persisted, and its rulings record files the M-4 change under Recs 8, 16 and 19. Rec 9's subject, "Environment off-pin", is consistent with BENCH-13's install-path point, so the citation stands and is marked unverified.)* The 2026-09-25/26
   offline rebuild (D-71) is existing evidence; it predates the `ml_dtypes` drift.
2. Run the critical set (§18.3 selection (b)) and the full suite in that fresh env.
3. Run both fixtures in order. `scientific_1month` becomes runnable only after its identity
   and manifest acts (Q-31).
4. Record CPU model, RAM, peak memory, runtime and storage for each run (P-5). Peak RSS and
   CPU model are not captured by the orchestrator today. Capturing them is a code ruling owned by
   the Student (PV-01 Rec 16), or an external measurement during this step.
5. The output becomes the local limb of `environment_and_cpu_preflight_report`.

### M-5 — B-01 on the local route (corrected 2026-09-29, PV-01 Rec 1)

*Superseded text: "Blocked on B-1 in the change record: WSL2 plus a D-49 amendment". That
statement was false.*

**Already in place.**
- **Ruling:** D-49 addendum 2 (2026-09-28) rules WSL2 on this laptop in as `local` for B-01.
- **Run:** the fixture-scale B-01 leg ran there on 2026-09-28 (R-59 `passed`; 2,160 rows;
  `workload_seconds` 535.353).

**Still open before any non-fixture (full-year) B-01 generation.** Owner: the Student.
- **Receipt identity.** Full-year generation needs fixture receipts from the same environment
  identity, but addendum 2 excludes the fixture ladder. The way out is an addendum extending it
  to the B-01 fixture runs, as addendum 1 did for Kaggle, or D-49 option (b).
- **Measured wheel identity.** The install needs `--require-hashes`, or an installed-files check
  against `RECORD`.
- **Runtime versions.** Record the libgfortran and glibc versions.
- **Reference reproduction.** Reproduce the Kaggle smoke value `37.373754526924806` TECU in the
  governed `b01_iri` environment.
- **Config mirror.** Mirror addendum 2 into `configs/experiment.yaml interpreter_exception`.

## Explicitly not done (Q5 = A)

- **No full-year runtime extrapolation.** The fixture uses D-70's fixed apparatus points,
  not the D-121 grid search, so any multiplier would understate the cost by an unknown
  factor. Full-year runtime stays NOT MEASURED.
- No load, stress, soak, latency or throughput testing: nothing serves traffic.
- No GPU benchmarking. TensorFlow 2.21 on native Windows cannot see the RTX 3060, and GPU
  is never a dependency (P-1).
- No locked-test access of any kind.

## Sources

- `performance-validation-questions.md` (this stage's answers and receipts)
- `construction/*/code-generation/code-generation-plan.md` and `code-summary.md`, via `construction/build-and-test/`
- `construction/build-and-test/performance-test-instructions.md`, `build-test-results.md`
- `verification/phase-check-construction.md`
- `tests/fixtures/plumbing_7day/fixture_manifest.candidate_…-4a959333.yaml`
- `governance/CHANGE_RECORD_2026-09-29_Q31_closure.md`, `governance/CHANGE_RECORD_2026-09-29_platform_local_only.md`
- TE §9.1, §9.2, §15.1–§15.2; Vision D-129; `constraint-register.md` TC-01, TC-03c, TC-03f, TC-03g
