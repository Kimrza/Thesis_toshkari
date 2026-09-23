# TEC Hourly Forecast — governed research pipeline (Phase 1)

Hourly VTEC forecasting at ARUC, BSHM and NICO (Madrigal cells), calendar year 2022,
tested on December 2022 only — a single-author thesis codebase (student: Kimia Rezaei;
supervisor: Dr. Reza Saraf Shirazi) governed by
`PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` (the "TE") and
`PreFlight/vision_document(3)(2)(2).md`. Every claim is bounded to those cells, that
year, and that test month (D-8).

## Repository layout (TE §12)

```
configs/          the exactly four governed configs: data.yaml, features.yaml,
                  experiment.yaml, seeds.yaml — every scientific constant lives here,
                  never in source or a notebook (TC-03e). Unfrozen fields carry the
                  literal sentinel `TBD — freeze gate`, which nobody fills by
                  convenience (TE §1.1).
src/              six packages: data, gnss, external, features, models, evaluation.
                  Reusable logic lives here; notebooks never own production logic.
scripts/          stage scripts (NN_verb_noun.py, owned by their units) and tooling
                  (gate_secret_scan.py). Every stage script takes --config configs/.
tests/            the §12 mandated test suite (built ahead of acquisition, TC-06)
                  plus tests/fixtures/ for the two walking-skeleton fixtures.
artifacts/        run snapshots, the experiment registry, dataset releases
                  (artifacts/releases is the single authoritative release root, SD-04).
evidence/         governed evidence and evidence/DECISIONS.md — the D-number record;
                  a decision is not real until it has a D-number. The restricted
                  December root inside it is reachable ONLY via src/data/locked_test.py.
notebooks/        exploration only; frozen values migrate to configs/ (Q11=B).
```

## Two platforms, CPU only

Exactly two execution platforms are authorised (TC-03c): **Kaggle** (primary compute)
and **local** (development, small tests, fixture runs, review). Google Colab is
explicitly removed. CPU is a complete execution path (TC-01): no result may depend on
a GPU. The full workflow, including both walking-skeleton fixtures, completes on CPU.

Platform resolution is `src/data/config.resolve_platform_roots` — set `TEC_PLATFORM`
(`kaggle` | `local`) to force it; anything else refuses with `PlatformError`.

## Environment

Python **3.11** exactly (TS-01/TC-03d; `pyproject.toml` pins `requires-python`).
Install from the single pinned surface:

```
pip install -r requirements.txt
```

TensorFlow **is pinned**, at `tensorflow==2.21.0`, by the project decision owner's ruling
of 2026-09-10 adopted as **D-36**.

*Corrected 2026-09-20 (`GOV-2026-09-20-CG-01` Recommendation 42's corrected fact, swept into
this file). This paragraph previously read "TensorFlow is **excluded** from the pins: its
pin is `TBD — freeze gate` (Q3=A) and is added only under an approved D-number." That was
true under code-generation Q3=A and stopped being true on 2026-09-10 — the D-number the
sentence was waiting for arrived. The pin is frozen; what remains OWED is verification:
PyPI is unreachable from the implementation environment, so installation, import,
API-compatibility and TE §8.1's both-platform (Kaggle AND local) check are unperformed.
Freezing a pin makes the guard pass; it does not make the environment exist.*

One required package is still **unpinned**: `matplotlib` (TE §8.1, Required) executes in
`src/evaluation/plots.py` and is absent from `requirements.txt`, so figures are outside
TE §13.1's environment lock. No repository evidence determines the version — derivation
printed in `requirements.txt`'s own block — and fixing it is a Student act owed before G-07
(`CR-2026-09-20-GOV-CG-01-DISPOSITIONS` §5 item 15; Recommendation 38).

PyTorch, R, Julia and MATLAB are prohibited (TE §8.3).

**On this machine, use the `tec-thesis-311` conda environment — not the machine's
default Python.** Activate it before running anything in this repository:

```
conda activate tec-thesis-311
```

`tec-thesis-311` (Python 3.11.16) already carries every pin in `requirements.txt` at
the pinned version. The machine's default `python` on `PATH` resolves to Python 3.14,
under which `pip install -r requirements.txt` fails: `numpy==1.26.4` has no prebuilt
wheel for Python 3.14 on Windows, and building it from source requires a C/C++
toolchain (`cl`/`gcc`/`clang`) that is not installed here.

**Known gap, not silently worked around:** a from-scratch setup (a new machine, no
`tec-thesis-311` env already present) needs Python 3.11 installed first — `py -3.11`
currently reports no suitable runtime on this machine, so the governed interpreter
pin has no fresh-install path here yet. Provisioning one is unresolved and owed
separately from this note.

## Reproducing a run

**`REPRODUCTION.md`** carries TE §13.2's ordered clean-run contract verbatim — including
`export PYTHONHASHSEED=0`, which is part of the contract and not a convenience. Start there
rather than reading the Technical Environment or a source constant. The guide, the TE fence
and `scripts/run_walking_skeleton.py`'s `PHASE1_SEQUENCE` are bound to each other by a
three-way comparison in `tests/test_clean_run.py`, so none of the three can drift silently.

## Running the test suite

```
export PYTHONHASHSEED=0
python -m pytest tests/
```

Runnable without manual setup. Gate tests run per team practice Q7=D: the full suite runs
locally before every acquisition/training/governed run, and **inside the Kaggle session**
before any governed run executed there (TC-03g) — a Kaggle session carries no git working
tree, so a commit hook cannot fire there and a local run proves nothing about it.

Two qualifications on the commit-time set, both added 2026-09-20:

* **It is narrower than the critical set, deliberately.** `.githooks/pre-commit` deselects
  `tests/test_release_hashes.py`, `tests/test_acquisition_window.py` and
  `tests/test_phase_boundary.py`, each of which reads December restricted content. A
  boundary crossed as a side effect of `git commit` is not a governed access (Vision §8.3;
  Recommendation 30). Those three run in the gate/freeze suite, where an authorization
  exists to be recorded.
* **The hook is not enabled yet.** `git config core.hooksPath` is UNSET and no commit in
  this repository's history has been gated by it (Recommendation 35). Enabling it is a
  Student act (`CR-2026-09-20-GOV-CG-01-DISPOSITIONS` §5 item 4), explicitly sequenced
  after the deselection above, which has now landed.

A full-suite run under the real evidence tree appends access rows to
`artifacts/exec_evidence/test_access_log.jsonl`, a gitignored **test-mode** sidecar.
`evidence/test_run_access_log.jsonl` is reserved for real, governed accesses and is closed
to further appends; its historical rows stand unedited under
`evidence/test_run_access_log.SUPERSEDED_2026-09-20.md` (Recommendation 1). Records are
superseded, never rewritten and never deleted.

## Tooling

* **ruff** (pinned in `requirements.txt`) lints and formats; configured in
  `pyproject.toml`.
* **gitleaks 8.18.4** (pinned) scans for secrets in two modes (SD-01):
  * incremental, on every commit, via the pre-commit hook — a preventive net, never
    evidence. Enable hooks once per clone: `git config core.hooksPath .githooks`
    (**not yet run on this repository** — see § Running the test suite)
  * history-inclusive, before each governed run and freeze gate, via
    `python scripts/gate_secret_scan.py` — the only mode whose output is TA-22
    evidence (tool version, commit range, scope, result). Running it at a gate is a
    human/governed act; the script claims nothing.
* Credentials and secrets reach the process only through platform secret stores or
  environment configuration excluded from version control (TE §10); the `.gitignore`
  deny-list is the exclusion mechanism. No credential value is ever read, returned,
  logged, serialized or persisted by the foundation layer (R-14).

## The foundation layer (Bolt 1)

`src/data/config.py` (C-1 Resolve: configs, preflight, platform, credentials names,
seeding, the eight-item environment lock), `src/data/experiment_registry.py` (C-2: the
twenty-column append-only experiment registry, TE §13.4) and `src/data/release.py`
(C-3: immutable content-addressed dataset releases, TE §13.3, D-29). Every module's
docstring states its purpose, inputs and re-run behaviour (affirmed practice Q12-C).

Governance notes that bind every run: seeds come from `configs/seeds.yaml` (D-122);
failed and aborted runs stay visible in the registry with status and reason
(NFR-AUD-01); a release directory is never overwritten (R-13); December 2022 is locked
— the pre-G-05 coverage audit is performance-blind, and the one-shot evaluation is
hash-before-metrics after G-05 (Vision §8.3, §5.3).
