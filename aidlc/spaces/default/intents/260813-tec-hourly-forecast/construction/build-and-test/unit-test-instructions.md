# Unit Test Instructions

**Stage:** build-and-test (3.6) · **Lead:** aidlc-quality-agent
**Date:** 2026-09-24 · **Repository commit at authoring:** `41fd109`
**Test strategy:** Comprehensive (from `aidlc-state.md`)

These instructions cover the per-module (unit-level) test suite. They are
derived from the twelve units' `code-generation/code-summary.md` records and
their `code-generation-plan.md` files (this stage's consumed inputs), from
`team.md` § Testing Posture, and from the current on-disk `tests/` tree —
not from the framework's generic tiers. The project's own quality gate is
TE §18.3 ("zero unresolved P0 fields and no failing critical test"), not a
coverage percentage.

## Framework and configuration

| Item | Value | Source |
|---|---|---|
| Framework | `pytest==8.2.2` | `requirements.txt`; TC-06 |
| Interpreter | CPython 3.11 exactly | TS-01 / TC-03d; TE §8.1 |
| Config | `pyproject.toml` at repo root | §12; TA-01 |
| Determinism | `PYTHONHASHSEED=0` before any run | TE §13.2; ADR-10 |
| Environment | rebuildable from conda-forge when PyPI is blocked (see `build-instructions.md` § environment reconstruction) | this stage, measured |

## How to run

From the repository root, inside the governed 3.11 environment:

```bash
# whole suite
python -m pytest tests/ -q

# one module
python -m pytest tests/test_feature_availability.py -q

# one test by keyword
python -m pytest tests/ -k "iri_denial" -q
```

Notes that matter on this repository specifically:

- Running the suite appends test-mode access rows to the **sidecar log**
  `artifacts/exec_evidence/test_access_log.jsonl` — NOT to
  `evidence/test_run_access_log.jsonl`, which was **closed on 2026-09-20**
  under GOV-2026-09-20-CG-01 Rec 1 (see
  `evidence/test_run_access_log.SUPERSEDED_2026-09-20.md`) and is reserved
  for real governed December accesses. The sidecar is expected to grow on
  every run and is part of the audit surface. *(Corrected 2026-09-24 under
  Rec 4 of `GOV-2026-09-24-BT-01`, ruled option 2: the earlier sentence here
  migrated from a pre-Rec-1 stage-diary entry of 2026-09-18 and misdirected
  the reader to the closed governed log.)*
- Some determinism tests spawn fresh processes (`tests/_fresh_process.py`);
  they are one-process-per-stage by design and slower than the rest.
- The locked-test guard tests exercise refusal paths against
  `evidence/locked_test_restricted/`; they never open December content and
  every access attempt is recorded.

## The mandated module set (21 modules) and what exists

TE §12 mandates **21** test modules (`team.md` § Corrections — the earlier
"17" figure is superseded). Three of the 21 (`test_rinex_schema.py`,
`test_dcb_sign.py`, `test_hourly_target.py`) attach to Phase 2 raw-processing
stages that Phase 1 is barred from running (§7.0, NFR-PHASE-01) and therefore
do not exist yet by design. The on-disk tree currently carries **29 test
modules** — every Phase 1-reachable mandated module plus project-grown
modules the construction work added (`test_determinism.py`,
`test_feature_leakage_guards.py`, `test_import_boundary.py`,
`test_in_session_gate.py`, `test_preflight_report.py`,
`test_phase_contract.py`, `test_release_contract.py`,
`test_december_audit.py`, `test_external_drivers.py`,
`test_merge_script_restricted_reads.py`, and others).

Test-function counts per module (derived by grep at `41fd109`; authoritative
collected-case counts come from the pytest run recorded in
`build-test-results.md`):

| Module | fn count | Unit (owner) |
|---|---|---|
| test_regimes_and_reporting.py | 102 | regimes-diagnostics-reporting |
| test_feature_availability.py | 86 | features-and-splits |
| test_clean_run.py | 86 | fixtures-and-reproducibility |
| test_external_drivers.py | 81 | external-products |
| test_december_audit.py | 74 | inventory-and-registry |
| test_common_masks.py | 73 | evaluation-and-comparison |
| test_models_smoke.py | 68 | models-and-baselines |
| test_acquisition.py | 65 | acquisition |
| test_prepared_target_schema.py | 64 | target-standardization |
| test_locked_test_guard.py | 57 | governance-guards |
| test_determinism.py | 46 | foundation |
| test_station_registry.py | 37 | foundation |
| test_bootstrap.py | 37 | statistical-inference |
| test_train_only_transforms.py | 35 | features-and-splits |
| test_split_embargo.py | 34 | features-and-splits |
| test_release_contract.py | 32 | foundation |
| test_experiment_registry.py | 26 | foundation |
| test_phase_contract.py | 25 | governance-guards |
| test_feature_leakage_guards.py | 23 | features-and-splits |
| test_iri_denial.py | 22 | external-products |
| test_release_hashes.py | 16 | foundation |
| test_reuse_registry.py | 13 | foundation |
| test_phase_boundary.py | 13 | governance-guards |
| test_checkpoint_restore.py | 12 | models-and-baselines |
| test_in_session_gate.py | 10 | governance-guards |
| test_preflight_report.py | 9 | governance-guards |
| test_acquisition_window.py | 7 | acquisition |
| test_merge_script_restricted_reads.py | 6 | governance-guards |
| test_import_boundary.py | 6 | external-products |

## Methodology: a negative control per hard rule

The project's affirmed testing methodology (team.md § Testing Posture) is a
**negative control paired with every hard rule**, not positive-path testing
alone. When adding or reviewing unit tests, the bar is:

- every hard rule in `discovered-rules.md` gets a test that proves the
  violation is **caught**, not only that the happy path works;
- WS-10's operational form: the IRI-denial suite passes by proving the
  denial mechanism rejects a deliberately injected `iri_*` field;
- the reversed-sign DCB negative control (WS-04/TA-07) is Phase 2 work;
- mutation probes against pre-repair HEAD ("CONTROL BITES") are the local
  idiom for proving a new control actually bites — several are recorded in
  the stage diary and change records.

## Coverage expectations

**No enforced numeric coverage floor** (team.md, Q5=A). The
`aidlc-coverage-threshold` sensor's embedded line 80 / branch 70 defaults are
advisory reporting only; `test-pro-coverage-summary.json.targets` is
deliberately left unset. The real bar is the §18.3 critical set — ten items:
target contract and DCB sign; availability lags; IRI-free denial; split
embargo; train-only transforms; comparison-wide masks and matched windows;
checkpoint restore; vector bootstrap; release hashes; locked-test access
guard — plus the Phase 1 WS rows (WS-01, WS-09–WS-20) and the test-bearing
TA rows (TA-07–TA-09, TA-11–TA-14, TA-17, TA-18, TA-22, TA-23, TA-26, TA-27).

## When the suite must run

Per team.md (Q7=D): the pre-commit hook (`.githooks/pre-commit`) runs the
**commit-time subset** of the critical set on every commit — five modules
(`test_determinism`, `test_experiment_registry`, `test_release_contract`,
`test_locked_test_guard`, `test_merge_script_restricted_reads`); the three
restricted-root readers are deliberately deselected from commits (Rec 30,
option 1) and run in the gate suite instead, so the hook is a subset, never
the whole §18.3 selection. The full suite runs locally before every
acquisition or training run and before every governed run, with the result
captured in that run's evidence record; the critical set and both fixtures
run **inside the Kaggle session** before any governed run executed there
(TC-03g, hard). No CI service is used.

Hook activation state, measured on this clone 2026-09-24 (Rec 3 of
`GOV-2026-09-24-BT-01`, ruled option 2): `git config --get core.hooksPath`
→ `.githooks` — activated this session under that ruling (the earlier
"verified 2026-09-24" here was carried from a different clone state and was
false when written; the hook file existed but `core.hooksPath` was unset, so
prior commits on this clone ran ungated). The hook needs `python`+`pytest`
on `PATH` — see `build-instructions.md` addendum for the commit procedure.
