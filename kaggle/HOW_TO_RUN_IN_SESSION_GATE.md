# How to run the TC-03g in-session gate on Kaggle

**Nothing in this file has been executed by an agent.** No Kaggle account, API key or
network session exists in the local environment. This is the runbook for the act
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

## Precondition that is NOT yet met — read before booking the session

`src/data/fixture_gate.py: emit_in_session_gate_result` exists, is tested, and has **no
production caller** (`src/data/fixture_evidence.py:682` states this in its own comment:
"callers only in `tests/test_clean_run.py` — no stage script and no notebook calls it").
`scripts/run_walking_skeleton.py` takes no `--in-session-gate` option. **Wiring that call
site is code work that must land before the session is worth booking** — otherwise the
session runs the tests and the fixtures but writes no gate artifact, and
`require_in_session_gate` has nothing to judge. This is Recommendation 28's open limb and
it is stated here rather than worked around.

A second, independent precondition: **the fixture ladder does not yet complete.** As of
2026-09-21 the sequence reaches stage 05 and stops at `features-and-splits`'
`_load_release_inputs`, which refuses by design (TE §18.3 stop-and-report) because the
release-input reader has not been built. Until it completes locally under the 3.11 pin,
a Kaggle session cannot produce a fixture result either.

**Therefore: do not book the Kaggle session yet.** The order is (1) wire the gate emitter
into `run_walking_skeleton.py`; (2) make both fixtures pass locally; (3) then run the
session below.

## The session, once those two preconditions are met

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

Run these in one notebook, top to bottom, with `TEC_PLATFORM=kaggle` set so the
snapshot's platform label is `kaggle` (the gate refuses a `local` stamp —
`fixture_gate.py:835`), and `--code-commit` passed explicitly (a Kaggle session has no git
working tree, so the lock cannot read `HEAD`):

```bash
export TEC_PLATFORM=kaggle
export CUDA_VISIBLE_DEVICES=""          # TC-01: no GPU visible
export PYTHONHASHSEED=0                 # TE §13.2 determinism
COMMIT=<the exact commit sha the uploaded tree was taken from>

# 1. the critical test set, IN SESSION — junit is the machine-readable result
python -m pytest -q tests/ \
  --ignore=tests/test_release_hashes.py \
  --ignore=tests/test_acquisition_window.py \
  --ignore=tests/test_phase_boundary.py \
  -p no:cacheprovider --junitxml=/kaggle/working/junit_in_session.xml

# 2. both fixtures, IN SESSION, in order (TE §9.2: plumbing first, never as evidence)
python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day      --code-commit "$COMMIT"
python scripts/run_walking_skeleton.py --config configs/ --fixture scientific_1month  --code-commit "$COMMIT"

# 3. the environment lock and the G-09 preflight report, from THIS session's junit
python scripts/gate_preflight_report.py --config configs/ --phase 1 \
  --junit /kaggle/working/junit_in_session.xml \
  --signoff governance/G09_SUPERVISOR_SIGNOFF_RECORD.yaml \
  --code-commit "$COMMIT" \
  --output /kaggle/working/aws_ai_dlc_preflight_report_kaggle.json
```

The three December-reading modules are deselected in step 1 for the same reason the
pre-commit hook deselects them (`.githooks/pre-commit` §2, Recommendation 30): they read
bytes under the restricted root, which is not uploaded and must not be. Their evidence
belongs to an authorised local gate occasion, not to a Kaggle session.

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
