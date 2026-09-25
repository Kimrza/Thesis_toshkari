# Build Instructions

**Stage:** build-and-test (3.6) · **Lead:** aidlc-quality-agent · **Support:** aidlc-devsecops-agent
**Date:** 2026-09-13 · **Repository commit at authoring:** `615a367`

This project has no compile, bundle or transpile step. "Build" here means
exactly two things: **reconstructing the pinned environment**, and **verifying
that the reconstruction matches the governed pin**. Everything downstream — the
test suite, the fixture ladder, any governed run — is gated on those two
succeeding, so they are treated as the build.

## Scope and platform rules

Exactly two execution platforms are authorised (TC-03c, `team.md` § Deployment):
**Kaggle** (primary compute and the Phase 1 acquisition/audit host) and **local**
(development, small tests, fixture runs, review). No third platform is
authorised; Google Colab and Google Drive were removed as governed platforms.

The two platforms are **not interchangeable for evidence**. TC-03g (`binding:
hard`) requires the critical test set and both walking-skeleton fixtures to run
**inside the Kaggle session** before any governed run executed there, because a
Kaggle session carries no git working tree and therefore cannot fire a commit
hook. A local suite run proves nothing about the environment a governed run
actually executes in. § "Kaggle-session procedure" below is the operational form
of that requirement; it was written from this clone and **has never been
executed from it**.

There is a second, sharper reason the platforms must not be conflated, and it
was found by execution during this stage rather than by reading: until commit
`19b6e12`, every stage script and the walking-skeleton orchestrator **discarded
its own exit code on Windows** and reported success regardless of outcome, while
behaving correctly on Kaggle's Linux. That defect is repaired (see
`build-test-results.md` § "R-05"), but it is the reason this document states a
platform for every command rather than assuming one.

## Prerequisites

| Item | Requirement | Source |
|---|---|---|
| Interpreter | **CPython 3.11 exactly** | TS-01 / TC-03d; `pyproject.toml` `requires-python = "==3.11.*"`; TE §8.1 |
| Dependency manifest | `requirements.txt` at the repository root — the single governed pin surface | TE §13.1; TA-02 |
| Tooling config | `pyproject.toml` at the repository root (ruff + pytest configuration) | TE §12; TA-01 |
| Governed configs | `configs/data.yaml`, `configs/features.yaml`, `configs/experiment.yaml`, `configs/seeds.yaml` — all four, every run | TE §12; TC-03e |
| Secret scanner | `gitleaks` **8.18.4**, pinned by comment in `requirements.txt` (a Go binary, not a pip package) | SD-01; TA-22 |

A different interpreter may run the suite as **smoke evidence only, never
governed evidence**. `pyproject.toml` states this in its own comment and it is
repeated here because it is the single most common way a number from this
pipeline could be misread.

## Step 1 — Reconstruct the environment

Local (Windows or POSIX), from the repository root:

```bash
python3.11 -m venv .venv
# POSIX:    source .venv/bin/activate
# Windows:  .venv\Scripts\activate
python -V                      # must print Python 3.11.x
pip install -r requirements.txt
```

If `python3.11` is not present, `uv` will fetch the exact interpreter without
touching the system Python:

```bash
uv python install 3.11
uv venv --python 3.11 .venv
uv pip install --python .venv -r requirements.txt
```

`uv` is a convenience for obtaining the interpreter, not a governed tool: the pin
that matters is `requirements.txt`, and the environment lock hashes that file
(TE §13.1, REQ-ENG-10).

## Step 2 — Verify the reconstruction

```bash
python -V                      # Python 3.11.x, else STOP
python -c "import numpy, pandas, yaml, sklearn, tensorflow; print('imports OK')"
pip freeze > artifacts/exec_evidence/pip_freeze_$(date -u +%Y%m%dT%H%M%SZ).txt
python -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('requirements.txt').read_bytes()).hexdigest())"
```

The `pip freeze` output and the `requirements.txt` SHA-256 are both **required
columns of the per-run environment lock** (TE §13.1), not optional diagnostics.
A run whose lock is incomplete fails rather than completing silently — that
behaviour is itself tested (`tests/test_determinism.py::test_incomplete_lock_fails_rather_than_completing_silently`).

**The `tensorflow==2.21.0` pin is frozen but unverified.** `requirements.txt`
states this in its own comment: the version was selected by the project decision
owner's ruling of 2026-09-10 and adopted as **D-36**, but PyPI has been
unreachable from every implementation environment used so far, so installation,
import, API compatibility, and TE §8.1's both-platform check are **owed**.
Freezing the pin makes `models-and-baselines`' M-06 guard pass; it does not make
the environment exist. The first host that can reach PyPI must run Step 2 in
full and record the result.

## Step 3 — Lint and format check

`ruff` is the affirmed tool for **both** linting and formatting (`team.md`
§ Code Style, Q10=A), configured in `pyproject.toml` — `target-version = "py311"`,
`line-length = 99`, rule sets `E`, `F`, `I`, `B`, `UP`, `S`.

```bash
ruff check .
ruff format --check .
```

`ruff`'s `S` (bandit) rules provide static security signal; they are **not** the
secret scanner. The scanner is `gitleaks`, covered in
`security-test-instructions.md`.

## Step 4 — Build verification (what "build passes" means here)

The build is verified when all four hold:

1. `python -V` reports 3.11.x.
2. `pip install -r requirements.txt` completed and every pinned package imports.
3. `ruff check .` and `ruff format --check .` exit 0.
4. The full test suite runs (see `unit-test-instructions.md`) with zero failures
   and zero collection errors.

There is no artifact to produce and no binary to ship. Item 4 is deliberately
part of the build definition rather than a separate phase: `constraint-register.md`
TC-06 (`binding: hard`) places repository structure, pinned environment **and
test suite** before any acquisition work, and `team.md` § Corrections fixes the
reading of "test suite" as the **full §12 mandated set**, not the subset a given
initiative happens to need.

## Step 5 — The preflight gate (TE §18.3)

Before any affected component is implemented or any governed run starts, an
automated assertion confirms **no required field** in the four governed configs
is `TBD`. The decision criterion is quoted verbatim from TE §18.3: *"zero
unresolved P0 fields and no failing critical test."*

```bash
python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day
```

**A refusal here is correct behaviour, not a build failure** (Q2 = A). TE §18.3
binds agents explicitly: *"Claude Code or any equivalent agent must not implement
an affected component while its P0 decision is unresolved, and must stop and
report rather than choose a default."* `project.md` § Forbidden puts the same
rule the other way round — never let an implementer fill a value marked
**"TBD — freeze gate"** by convenience; those values require explicit
student-and-supervisor approval.

So: if the preflight refuses, **record which fields refused and stop**. Do not
diagnose-and-fix it under the framework's generic two-attempt rule. The refusing
fields and the refusal text belong in `build-test-results.md` and, at a governed
run, in the `aws_ai_dlc_preflight_report`.

**Reading the exit code.** Since `19b6e12` the orchestrator and all nine stage
scripts propagate their exit status on both platforms: `0` on success, non-zero
on refusal or failure. Before that commit they exited `0` unconditionally on
Windows, so **any exit code recorded from a local Windows run at or before
`1670ac8` is not evidence of anything** and must not be cited.

## Step 6 — Fixture ladder ordering

TE §9.2 is a pipeline-enforced sequencing rule that survives the scope file's
`skeleton: off` untouched (`team.md` § Walking Skeleton): **both** fixtures run,
in order, before any full-year job.

```bash
python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day
python scripts/run_walking_skeleton.py --config configs/ --fixture scientific_1month
```

The seven-day single-station fixture is a **plumbing smoke test and never
scientific evidence** (TC-03f). The one-month all-station fixture is the
scientific one. The orchestrator threads the fixture scope into each stage script
through `--fixture-manifest`, and executes TE §13.2's Phase 1 fence verbatim:
`00_acquire_prepared_vtec.py`, `01_inventory_and_registry.py`,
`02_standardize_prepared_target.py`, `04_build_external_products.py`,
`05_build_features_and_splits.py`, `06_train_and_predict.py`,
`07_evaluate_and_report.py`. `02_build_vtec_target.py` and
`03_verify_processing.py` are Phase 2 only and run only after G-P2.

**Outstanding prerequisites for the ladder, as of this commit.** The ladder has
never completed on any host available to this initiative. Blocking it are: a host
that can install `pyyaml` (every attempt from this clone refuses at
`configs/data.yaml: pyyaml is required to parse governed configs`), the student's
two fixture-manifest freezes under Q-31, and the owner's `acquisition.window_*`
transcription. WS-20 and TA-17 stay blocked until those clear.

## Step 7 — Kaggle-session procedure (TC-03g)

**This procedure has never been executed.** It is written here because
`project.md` § Way of Working requires the inputs a gating condition depends on
to be specified in the same stage that records the condition, and TA-03 / TA-26
are gating conditions with no other operational home.

In the Kaggle notebook, first cell:

```python
!python -V                                  # must report 3.11.x
!pip install -r requirements.txt
!python -c "import numpy, pandas, yaml, sklearn, tensorflow; print('imports OK')"
!pip freeze > /kaggle/working/pip_freeze_kaggle.txt
```

Second cell — the critical test set, in-session:

```python
!python -m pytest tests/ -q
```

Third cell — both fixtures, in order:

```python
!python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day
!python scripts/run_walking_skeleton.py --config configs/ --fixture scientific_1month
```

Fourth cell — capture the evidence the session cannot otherwise carry:

```python
import json, subprocess, datetime
print(json.dumps({
    "platform": "kaggle",
    "utc": datetime.datetime.now(datetime.UTC).isoformat(),
    "python": subprocess.run(["python","-V"],capture_output=True,text=True).stdout.strip(),
    "code_commit": "<paste the commit SHA the notebook was run against>",
}, indent=2))
```

`code_commit` must be **pasted by hand**. A Kaggle session has no git working
tree, which is the whole reason TC-03g exists; the commit cannot be derived
in-session and an omitted one makes the run unattributable. Every output of these
four cells belongs in that run's evidence record, and the suite + fixture results
additionally in the `aws_ai_dlc_preflight_report` where applicable.

## Troubleshooting

| Symptom | Cause and response |
|---|---|
| `preflight refusal: configs\data.yaml: pyyaml is required to parse governed configs` | `pyyaml` is absent. This is an environment failure, **not** the §18.3 gate and **not** a scientific refusal. Fix the environment; never work around the config loader. |
| `uv pip install` times out on `https://pypi.org/simple/...` | PyPI is unreachable from this network. Do **not** substitute a mirror or vendor a package without a §10.1 reuse-register entry first (NFR-LIC-01; see `security-test-instructions.md` § "Third-party code"). |
| A stage script prints a refusal but the shell reports success | You are at or before commit `1670ac8` on Windows. Rebase onto `19b6e12` or later. The exit code from the older tree is meaningless. |
| `ruff` rewrites a file under `evidence/` or `artifacts/` | It should not — both are in `extend-exclude`. If it happens, the exclusion list has drifted; governed evidence bytes are never rewritten by a formatter. |
| A hash-verification step fails | Stop. `project.md` § Mandated: surface an integrity failure with an explicit exit and a message naming the file and the violated expectation. Never continue silently past a failed hash. |

## Upstream inputs

This stage consumes two artifacts per unit, and both were read across all twelve
units before these instructions were written:

- **`code-generation-plan.md`** — at
  `<record>/construction/<unit>/code-generation/code-generation-plan.md`. Supplies
  the intended module layout, the gated steps whose preconditions are owner acts,
  and the declared build/test entry points each unit expected.
- **`code-summary.md`** — at
  `<record>/construction/<unit>/code-generation/code-summary.md`. Supplies the
  files each unit actually owns, its test modules, and its recorded counts.

The twelve units are `acquisition`, `evaluation-and-comparison`,
`external-products`, `features-and-splits`, `fixtures-and-reproducibility`,
`foundation`, `governance-guards`, `inventory-and-registry`,
`models-and-baselines`, `regimes-diagnostics-reporting`, `statistical-inference`
and `target-standardization`.

**Six of those `code-summary.md` records are stale against the current tree** and
are carried to this stage's approval gate as an explicit finding rather than
edited under their frozen receipts (`project.md` § Corrections, `gf-3`):
`foundation`, `external-products`, `acquisition`, `inventory-and-registry`,
`target-standardization` and `fixtures-and-reproducibility`. Each describes the
state before one of the three owner-ruled repairs in `19b6e12`, `8d4297d` and
`615a367`. A reader building from a stale record will find more test functions
and different module bodies than it describes.

## Sources

- `Technical_Environment_and_Research_Implementation(1)(2).md` §8.1 (interpreter
  pin), §8.3 (Python-only; PyTorch prohibited), §9.1–§9.2 (platforms, fixture
  ordering), §10 (credentials), §12 (repository tree, four governed configs),
  §13.1 (environment lock), §13.2 (ordered clean-run contract), §18.3 (preflight
  gate).
- `aidlc/spaces/default/memory/team.md` § Way of Working, § Walking Skeleton,
  § Testing Posture, § Deployment, § Code Style.
- `aidlc/spaces/default/memory/project.md` § Forbidden, § Mandated, § Corrections.
- `aidlc/.../ideation/feasibility/constraint-register.md` TC-01, TC-03c, TC-03d,
  TC-03e, TC-03f, TC-03g, TC-06.
- `governance/CHANGE_RECORD_2026-09-13_R05_windows_exit_code.md`,
  `governance/CHANGE_RECORD_2026-09-13_04_fixture_window.md`,
  `governance/CHANGE_RECORD_2026-09-13_00_01_02_fixture_window.md`.
- `requirements.txt` and `pyproject.toml` as read at commit `615a367`.
- Per-unit `code-generation-plan.md` and `code-summary.md` under
  `<record>/construction/<unit>/code-generation/`.

---

## Addendum 2026-09-24 — environment reconstruction when PyPI is blocked (measured on this clone)

Everything above this line was written 2026-09-13 at `615a367`. Measured again
2026-09-24 at `41fd109`:

- The governed environments earlier sessions used on this machine (conda
  `tec-thesis-311` and its scratchpad siblings) lived under the Windows Temp
  tree and **no longer exist** — Temp was cleaned between sessions. The
  `README.md` note directing `conda activate tec-thesis-311` is therefore
  aspirational on a fresh session until the environment is rebuilt.
- Network split, re-probed this session: `pypi.org` times out;
  `repo.anaconda.com` and `conda.anaconda.org` (conda-forge) return 200;
  GitHub reachable. `pip install -r requirements.txt` is therefore
  **not executable** here, and the working reconstruction path is conda-forge.

**Reconstruction recipe (this session's measured path):**

```powershell
# 1. Miniconda, silent, user-scoped, no PATH changes
Invoke-WebRequest https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -OutFile miniconda.exe
Start-Process miniconda.exe -ArgumentList "/S","/InstallationType=JustMe","/AddToPath=0","/RegisterPython=0","/D=<env-root>\mc3" -Wait

# 2. The governed pin set from conda-forge (PyPI-free) — the command that actually
#    succeeded this session, byte-for-byte (Rec 2 of GOV-2026-09-24-BT-01, ruled
#    option 1: an earlier draft of this addendum printed matplotlib-base=3.9.0 inside
#    this command, which cannot resolve — see the refused install below)
<env-root>\mc3\Scripts\conda.exe create -p <env-root>\tec311 -c conda-forge --override-channels -y `
  python=3.11.16 numpy=1.26.4 pandas=2.1.4 pyyaml=6.0.1 scikit-learn=1.4.2 `
  pyarrow=16.1.0 pytest=8.2.2 ruff=0.4.8

# 3. Attempted and REFUSED, recorded separately: matplotlib 3.9.0 does not exist for
#    win-64 on conda-forge (jumps 3.8.4 -> later) nor on anaconda main (starts at 3.9.2).
#    The pin is owner-frozen (Rec 38): do NOT substitute 3.9.2. The rebuilt environment
#    is matplotlib-absent until a PyPI-reachable host supplies the exact pin.
#    (dry-run evidence: PackagesNotFoundInChannelsError: matplotlib-base=3.9.0)
```

**Known deviation, disclosed:** `tensorflow==2.21.0` has **no Windows
conda-forge build** and PyPI is unreachable, so a locally rebuilt environment
is TF-absent. The suite is written to run in both TF states
(TF-absence-dependent tests assert the refusal path); M-06 training work and
the TE §8.1 both-platform TF check remain owed to a host that can install the
pinned wheel (Kaggle can). The environment lock for any run from a rebuilt
environment must record this absence rather than imply the full pin set.

The verified reconstruction outcome for this session, with versions read back
from the created environment, is recorded in `build-test-results.md`.

Three further corrections under the Student's 2026-09-24 rulings on
`GOV-2026-09-24-BT-01` (`CR-2026-09-24-GOV-BT-01-RULINGS`):

- **Step 6's ladder-state paragraph in the 2026-09-13 body is SUPERSEDED** (Rec 14):
  the ladder is no longer "never completed on any host" and pyyaml is no longer the
  blocker — stages 00, 01, 02, 04 and 05 have completed on the `plumbing_7day`
  fixture path. See `integration-test-instructions.md` § Tier 1 for the measured
  2026-09-24 ladder state.
- **The body's pointer to `build-test-results.md` § "R-05" is dead** (Rec 15): that
  section does not exist in the rewritten results file. The R-05 Windows exit-code
  account lives in `governance/CHANGE_RECORD_2026-09-13_R05_windows_exit_code.md`.
- **Commit procedure under the now-active pre-commit hook** (Rec 3, ruled option 2):
  `core.hooksPath` is set to `.githooks` on this clone. The hook needs `python` with
  `pytest` importable on `PATH`; this machine's default `python` is a Windows Store
  stub, so prefix the governed environment for any commit, e.g. (Git Bash)
  `PATH="/c/<env-root>/tec311:$PATH" git commit ...`. A commit from a bare shell is
  blocked by the hook's own no-python message — by design (Q7=D), not a defect.
