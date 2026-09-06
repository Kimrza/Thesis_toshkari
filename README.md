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

TensorFlow is **excluded** from the pins: its pin is `TBD — freeze gate` (Q3=A) and is
added only under an approved D-number. PyTorch, R, Julia and MATLAB are prohibited
(TE §8.3).

## Running the test suite

```
python -m pytest tests/
```

Runnable without manual setup. Gate tests run per team practice Q7=D: the pre-commit
hook runs the critical set on every commit; the full suite runs locally before every
acquisition/training/governed run, and **inside the Kaggle session** before any
governed run executed there (TC-03g).

## Tooling

* **ruff** (pinned in `requirements.txt`) lints and formats; configured in
  `pyproject.toml`.
* **gitleaks 8.18.4** (pinned) scans for secrets in two modes (SD-01):
  * incremental, on every commit, via the pre-commit hook — a preventive net, never
    evidence. Enable hooks once per clone: `git config core.hooksPath .githooks`
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
