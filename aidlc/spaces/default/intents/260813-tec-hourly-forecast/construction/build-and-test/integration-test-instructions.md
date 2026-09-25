# Integration Test Instructions

**Stage:** build-and-test (3.6) · **Lead:** aidlc-quality-agent
**Date:** 2026-09-24 · **Repository commit at authoring:** `41fd109`

Integration testing in this project is not a separate test framework tier —
it is the **walking-skeleton fixture ladder** (TE §9.2) plus the cross-unit
boundary tests already inside `tests/`. Both are required before any
full-year job. Sources: the twelve units' `code-generation-plan.md` /
`code-summary.md` (this stage's consumed inputs), TE §9.2/§13.2/§15,
`team.md` § Walking Skeleton.

## Tier 1 — the fixture ladder (the real integration test)

Two fixtures, run in order, both required before any full-year job
(TC-03f; hard, pipeline-enforced):

1. **`plumbing_7day`** — one station (BSHM, D-20), 2022-11-01 to 2022-11-07
   (D-11). Smoke test only, never scientific evidence.
2. **`scientific_1month`** — all three stations, one month. Window still
   open under Q-31 (a student freeze act, not an implementation choice).

```bash
export PYTHONHASHSEED=0
python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day
python scripts/run_walking_skeleton.py --config configs/ --fixture scientific_1month
```

**Measured ladder state at authoring (2026-09-24):** stages 00, 01, 02, 04
and 05 complete on the plumbing fixture path
(`artifacts/walking_skeleton/plumbing_7day/` holds the acquisition release,
registry entry, standardized target, four driver releases and eight feature
bundles plus `apparatus_split_manifest.json` and `fixture_measurements.json`;
WS-13 value-level parity measured 0.0 TECU, status *measured, not frozen*).
Stages **06 and 07 have not yet run** on the fixture (no
`models/`/`predictions/`/`evaluation/` outputs exist under the fixture root).
The scientific fixture has never run. WS-20 / TA-17 therefore remain
`Pending`.

Fixture runs write under `artifacts/walking_skeleton/<fixture_id>/releases/`,
never the governed `artifacts/releases/` root (release-root split, ruled
2026-09-23). A bundle is never overwritten (TE §13.3): re-running stage 05
against existing bundle directories refuses by design — that refusal is
correct behaviour, not a failure.

## Tier 2 — cross-unit boundary tests inside the suite

These modules exercise contracts **between** units and must be green in any
integration claim:

| Boundary | Module(s) |
|---|---|
| 02 → 05: standardized target consumed by feature build | `test_prepared_target_schema.py`, `test_feature_availability.py` |
| 04 → 05: driver releases resolved via permitted-producer identities (D-63) | `test_external_drivers.py`, `test_feature_availability.py` (incl. the D-66 `source_series` collision negative control) |
| 05 → 06: feature bundles, folds, embargo | `test_split_embargo.py`, `test_train_only_transforms.py`, `test_models_smoke.py` |
| 06 → 07: predictions, masks, estimand | `test_common_masks.py`, `test_bootstrap.py`, `test_regimes_and_reporting.py` |
| Clean-run contract agreement (REPRODUCTION.md ⇄ TE §13.2 ⇄ `PHASE1_SEQUENCE`) | `test_clean_run.py` |
| Locked-test custody across every entry point | `test_locked_test_guard.py`, `test_phase_boundary.py`, `test_merge_script_restricted_reads.py` |
| Registry integrity (append-safe, failed runs visible) | `test_experiment_registry.py` |
| Environment/preflight gate (§18.3) | `test_preflight_report.py`, `test_in_session_gate.py` |

Run them together:

```bash
python -m pytest tests/test_clean_run.py tests/test_external_drivers.py \
  tests/test_feature_availability.py tests/test_split_embargo.py \
  tests/test_common_masks.py tests/test_models_smoke.py -q
```

## Environment and data setup

- Governed CPython 3.11 environment (see `build-instructions.md`). CPU is a
  complete execution path (TC-01) — no GPU is ever required.
- Fixture assertion data lives in
  `tests/fixtures/<fixture_id>/fixture_manifest.yaml` and
  `identity_declaration.yaml`, never hardcoded in test bodies (§15.2). Exact
  counts, tolerances and runtimes are **measured from the fixtures and
  frozen, never invented** (§15.1); several tolerance fields still carry
  `TBD — freeze gate` sentinels awaiting the student's freeze acts.
- No record whose observation date falls in December 2022 may enter either
  fixture, asserted on record dates (`tests/test_acquisition_window.py`).

## Known blockers to a full ladder pass

Carried to the approval gate rather than worked around:

1. Stages 06/07 on the fixture require the `models.climatology` /
   `models.refit` and `reporting:` blocks in `configs/experiment.yaml` —
   owner transcription acts (some now landed via D-67/D-68; verify at run
   time with the §18.3 preflight, which refuses on any `TBD`).
2. The scientific fixture window is an open Q-31 student freeze.
3. TC-03g's Kaggle-session run has never been executed from this clone.
