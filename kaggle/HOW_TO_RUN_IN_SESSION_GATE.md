# How to run the TC-03g in-session gate on Kaggle

**Updated 2026-09-27 (GOV-2026-09-27-BT-02 continuation session).** The two
preconditions this file originally named (below) are **partly stale** — verified
against the current repository rather than assumed. Read the corrected status
before booking anything.

**Nothing in this file has been executed by an agent against a real Kaggle
session.** No Kaggle account, API key or network session exists in this local
environment. Local, non-December, bounded dry-runs WERE executed this session
to verify the commands below are accurate — never a governed run, never
December content. This is the runbook for the act
`CR-2026-09-20-GOV-CG-01-DISPOSITIONS` §5 item 10 assigns to the Student
(`GOV-2026-09-20-CG-01` Recommendations 28 and 57): the in-Kaggle session that discharges
**TC-03g** (`binding: hard`) and W-6 step 8's durability measurement.

## What TC-03g actually requires, quoted from its own rule

`project.md` § Mandated: *"ALWAYS run the critical test set and both walking-skeleton
fixtures **inside the Kaggle session** before any governed run executed there, capturing
the result in that run's evidence record. A Kaggle session carries no git working tree, so
a commit hook cannot fire there and a local suite run proves nothing about the environment
the governed run actually executes in."* (TE §9.1, §9.2; `constraint-register.md` TC-03g;
TA-03, TA-26.)

So three things must happen **in one Kaggle session, in this order**: the critical test
set runs; both fixtures run; the result is recorded as
`in_session_gate_result.json` with the session's own environment lock.

## Precondition status, corrected 2026-09-27

**Precondition 1 (gate-emitter wiring) — RESOLVED**, but by a different mechanism
than this file originally planned. `scripts/gate_in_session.py` now exists (added
after this file was written): a dedicated orchestrator that runs the critical set,
runs both fixtures, and calls `emit_in_session_gate_result` itself — no wiring into
`run_walking_skeleton.py` was needed or done. Use `scripts/gate_in_session.py`
directly; do not use `run_walking_skeleton.py` alone for this gate.

**Precondition 2 (fixture ladder) — PARTIALLY ADVANCED, and a NEW blocker was found
in `gate_in_session.py` itself, verified locally 2026-09-27 (bounded dry-runs, no
December, no Kaggle):**

1. The fixture ladder now reaches stage 07 (not stage 05) when invoked with
   `--emit-candidate --identity <fixture>/identity_declaration.yaml`
   (`CHANGE_RECORD_2026-09-25_apparatus_hyperparameters.md` §7a item 6, 2026-09-26:
   "stages 00–06 complete end-to-end... 07 runs to the R-106 exact-set refusal").
   That refusal is **structural**: comparison set `primary` declares member `B-01`
   (the IRI-2016 benchmark), and no B-01 payload can be generated locally — it
   requires `iricore`, Linux-only, which is exactly the Kaggle B-01 leg below.
2. **`gate_in_session.py`'s own fixture invocation does NOT pass `--emit-candidate`**
   (`fixture_command()`, line ~142): it calls plain
   `run_walking_skeleton.py --config … --fixture <id> --code-commit <sha>` with no
   `--emit-candidate` or `--identity` flag. Verified locally 2026-09-27: plain mode
   refuses immediately — `tests/fixtures/plumbing_7day/fixture_manifest.yaml` still
   carries the `TBD — freeze gate` sentinel on 46 fields and is "measured from a
   fixture run and frozen, never compared against an unmeasured placeholder" (TE
   15.1). **As shipped today, `gate_in_session.py` cannot pass either fixture** —
   it will hit this same refusal for both `plumbing_7day` and `scientific_1month`
   (the latter's `fixture_manifest.yaml` is also `status: candidate` with its own
   `TBD` fields). This is a real gap in the script, not a Kaggle-environment
   problem, and it is not yet fixed on this clone.
3. The B-01 Kaggle leg's runbook (below) states a "known remaining blocker":
   `gim_comparator.parquet` generation refusing on Q-15 (`TBD`). **That line is now
   stale** — Q-15 was frozen as D-72 (2026-09-26, bilinear spatial interpolation)
   and a governed release, `artifacts/releases/gim_comparator_C-01_2022/`, already
   exists and was independently re-verified by the 2026-09-27 board. Do not expect
   this blocker; if it recurs, that is a regression worth reporting, not the
   expected state.
4. **A stale/conflicting local artifact state was found and restored, not fixed
   forward**: an `--emit-candidate` dry run this session hit a DIFFERENT, later
   refusal at stage 02 — a published `phase1_hourly_target` release whose committed
   content hash disagrees with this run's freshly computed one (R-13's
   conflict-refusal, working as designed — TE §13.3 "a new version rather than an
   overwrite"). This is evidence that **the repository's fixture-run artifacts are
   not currently in a clean, freshly-reproducible state** — some prior local run
   left a release version the Student has not yet resolved via D-76's Option A
   procedure. Resolve this (or start from a clean `artifacts/walking_skeleton/` and
   `artifacts/releases/` state) before trusting any fixture run, local or Kaggle.

**Therefore: do not book the Kaggle session for the in-session gate yet.** The
corrected order is: (1) the B-01 Kaggle leg (below) — this one IS ready to book;
(2) the local bridge step; (3) fix `gate_in_session.py` to pass
`--emit-candidate --identity <path>` per fixture (a small, verifiable code change —
not done on this clone this session, since it was outside this task's scope); (4)
resolve the R-13 stale-release conflict; (5) confirm both fixtures pass **locally**
first (never assume Kaggle will succeed where local has not been tried); (6) only
then book the in-session-gate Kaggle session.

## Step 0 — the B-01 Kaggle leg (THIS one is ready to book now)

This is a **separate, smaller Kaggle session** from the TC-03g in-session gate
below, and does not depend on any of the four items above. It produces the B-01
(IRI-2016) benchmark payload the fixture ladder needs to clear the R-106
refusal. Full runbook: `governance/RUNBOOK_2026-09-26_kaggle_b01_fixture_leg.md`
(verified current 2026-09-27, except its own "known remaining blocker" note on
Q-15/`gim_comparator.parquet`, which is stale — see item 3 above). Summary,
commands verified against the repository as it stands today:

- Environment: CPython **3.10.12** (D-49's exception, this benchmark only —
  NOT the 3.11 governed pin), `iricore==1.8.0` (Linux-only wheel, this is why
  Kaggle and not local), pinned index files `apf107.dat` / `ig_rz.dat` by the
  SHA-256s D-49/D-45 already record. **Never run `iricore.update()`.**
- Pin check before and after (D-45 annotation item 2):
  ```bash
  python scripts/04_build_external_products.py --config configs/ --phase 1 \
    --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
    --code-commit <HASH> --verify-runtime
  ```
- R-59 validation report (needs the Student's own samples file, R-59's seven
  areas; tolerance predeclared in `configs/experiment.yaml: benchmark_b01.validation_report`):
  ```bash
  python scripts/04_build_external_products.py --config configs/ --phase 1 \
    --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
    --code-commit <HASH> --build-validation-report <your_samples.json>
  ```
  A `failed` report is written as-is and generation stays blocked — never switch
  implementations to make it pass.
- Generation (November only — the fixture month):
  ```bash
  python scripts/04_build_external_products.py --config configs/ --phase 1 \
    --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
    --code-commit <HASH> --generate-benchmark \
    --validation-report artifacts/external/b01/iri_implementation_validation_report.json \
    --months 11
  ```
  Then repeat the pin check (pins AFTER — a drifted pin invalidates the session, D-49).
- **Bring back** from `artifacts/external/b01/`: `b01_runtime_identity.json`,
  `iri_implementation_validation_report.json`, `b01_iri2016_rows.jsonl`,
  `b01_provenance.json`, `sha256_manifest.json`.
- **Local bridge step, back on this machine, after verifying the returned files
  against their `sha256_manifest.json`** (agent-runnable, not a Kaggle act):
  ```bash
  python scripts/04_build_external_products.py --config configs/ --phase 1 \
    --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
    --emit-prediction-payload artifacts/walking_skeleton/plumbing_7day/predictions \
    --benchmark-rows <returned b01_iri2016_rows.jsonl> \
    --benchmark-provenance <returned b01_provenance.json>
  ```
  This re-verifies R-59 at consumption and writes one stamped `B-01.json` per
  apparatus fold (one adapter call per fold — the fold windows overlap, per
  `test_overlapping_apparatus_folds_bucket_correctly_only_via_per_fold_calls`).

After this leg, re-attempt the local `--emit-candidate` dry run for
`plumbing_7day` (after resolving item 4's R-13 conflict) to confirm stage 07
now clears — **do this locally before spending a second Kaggle session on the
in-session gate below.**

## The session, once items 1–5 above are resolved (the in-session gate itself)

### Upload

The whole repository working tree, as a **private Kaggle dataset** (not a notebook
attachment of loose files): `configs/`, `src/`, `scripts/`, `tests/`,
`requirements.txt`, `pyproject.toml`, `tests/fixtures/`, and the `evidence/` months the
fixture manifests cite. **Do not upload `evidence/locked_test_restricted/`** — the locked
December root must not leave the governed machine, and no Kaggle path may reach it
(Vision §8.3; D-15).

### Kaggle settings

| Setting | Value | Why |
|---|---|---|
| Accelerator | **None / CPU** | TC-01: CPU is a complete execution path; a GPU result is not the governed one |
| Internet | **ON** | needed to `pip install -r requirements.txt`; needs a phone-verified account |
| Environment | default "Latest environment" | the notebook detects its own interpreter; see the 3.10/3.11 note below |
| Dataset | the private dataset above | no other attachment |

### Environment

`requirements.txt` pins the governed set exactly (`numpy==1.26.4`, `pandas==2.1.4`,
`pyyaml==6.0.1`, `scikit-learn==1.4.2`, `tensorflow==2.21.0`, `matplotlib==3.9.0`,
`pyarrow==16.1.0`, `pytest==8.2.2`, `ruff==0.4.8`). TC-03d pins **Python 3.11**; D-49's
extension covers a 3.10 environment for the B-01 benchmark only. If the Kaggle image is
not 3.11, build a 3.11 environment and run everything inside it — do not silently run the
governed suite on another interpreter, and record the interpreter version in the evidence
either way.

### The commands, in order

**Use `scripts/gate_in_session.py`, not manual pytest/`run_walking_skeleton.py`
calls.** It exists now (it did not when this file was first written) and does
steps 1, 2 and the gate-emission in one orchestrated, write-once, audit-logged
run — it already deselects the three restricted readers by name and already
refuses a non-`kaggle` platform stamp before running anything. **Precondition:
its `fixture_command()` must first be patched to pass
`--emit-candidate --identity <fixture>/identity_declaration.yaml`** (item 2
above) — without that fix it will abort at the same fixture-manifest refusal
verified locally this session, inside the Kaggle session, wasting the booking.

```bash
export TEC_PLATFORM=kaggle
export CUDA_VISIBLE_DEVICES=""          # TC-01: no GPU visible
export PYTHONHASHSEED=0                 # TE §13.2 determinism
COMMIT=<the exact commit sha the uploaded tree was taken from>

python scripts/gate_in_session.py --config configs/ --phase 1 --code-commit "$COMMIT"
```

That single command runs the critical set (junit at
`artifacts/exec_evidence/in-session-gate-<UTC>/junit_in_session.xml`), then both
fixtures in order (plumbing first, TE §9.2), then emits
`artifacts/walking_skeleton/in_session_gate_result.json` and immediately
self-checks it through `require_in_session_gate`. Exit 0 only if the result was
both emitted and accepted. If it aborts, the registry row it appends (status
`aborted`, with a `reason`) says why — read that before re-running; the gate
result is write-once, so a second run in the same workspace needs a moved or
versioned prior result, never an overwrite.

**Separately, for the G-09 preflight report** (not part of `gate_in_session.py`,
a distinct artifact per `src/data/fixture_evidence.py: build_environment_and_cpu_preflight_report`,
which reads the gate result above as its input):
```bash
python scripts/gate_preflight_report.py --config configs/ --phase 1 \
  --junit artifacts/exec_evidence/in-session-gate-<UTC>/junit_in_session.xml \
  --signoff governance/G09_SUPERVISOR_SIGNOFF_RECORD.yaml \
  --code-commit "$COMMIT" \
  --output /kaggle/working/aws_ai_dlc_preflight_report_kaggle.json
```

The three December-reading modules are deselected by `gate_in_session.py` for
the same reason the pre-commit hook deselects them (`.githooks/pre-commit` §2,
Recommendation 30): they read bytes under the restricted root, which is not
uploaded and must not be. Their evidence belongs to an authorised local gate
occasion, not to a Kaggle session.

### What to bring back, and where it goes

Download from the Output pane and commit into the repository:

| File | Goes to | What it evidences |
|---|---|---|
| `junit_in_session.xml`, the pytest console log | `artifacts/exec_evidence/run_<UTC>/` | the critical set ran **in session** (TA-03, TA-26) |
| `artifacts/walking_skeleton/*/` (both fixture roots, `clean_run_log.json`, `artifact_manifest.json`, `test_report.json`) | same paths in the repo | both fixtures ran in session (TE §9.2) |
| `artifacts/walking_skeleton/in_session_gate_result.json` | same path | **the TC-03g artifact itself** — platform, environment lock and hash, frozen manifest hashes, per-test and per-fixture results, measured total runtime |
| the appended `artifacts/registry/experiment_registry.jsonl` rows | merge, append-only | NFR-AUD-01: every run visible with status and reason |
| `pip freeze`, `python -V` | `artifacts/exec_evidence/run_<UTC>/` | the session's actual environment, beside the declared pins |
| `aws_ai_dlc_preflight_report_kaggle.json` | `artifacts/preflight/` | G-09 / TA-23 evidence produced in the governed execution environment |

Record the session in the run's evidence record and in the experiment registry. A failed
or aborted session stays visible with its status and reason — never delete a row and never
silently re-run (NFR-AUD-01; `project.md` § Forbidden).

### What the session does NOT do

It does not open the locked December set, does not pass G-05 or G-06, and does not by
itself sign G-09 — the preflight report is evidence for that gate, and the gate is the
supervisor's (Vision §13.1). No credential may appear in the notebook, in any output, or
in any registry note (TE §10; NFR-SEC-01): Kaggle credentials come from Kaggle's own
secrets, never from a cell.
