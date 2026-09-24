# Change record — 2026-09-24 — D-28 option (b) / D-68: wiring into the live prediction path

**Authority:** Student ruling — explicit authorization to (1) rule and write D-67
(`budget_value`), (2) rule and write D-68 (persistence-history mechanism) with `authorized:
true`, and (3) connect the mechanism to the live M-01/M-02 prediction path. All three
executed 2026-09-24, in that order.

---

## What was ruled

- **D-67** (`evidence/DECISIONS.md`): `budget_value.statistic = p95`, `combination = sum`.
  `configs/data.yaml: target.uncertainty_budget.decision = "D-67"`. Verified:
  `resolve_budget_rule` on the real config now returns
  `{'decision': 'D-67', 'statistic': 'p95', 'combination': 'sum'}` — a usable rule, for the
  first time.
- **D-68** (`evidence/DECISIONS.md`): the bounded 1-December persistence-history lookup.
  `configs/experiment.yaml: persistence_history_lookup = {authorized: true, decision: "D-68"}`.
  `src/data/locked_test.py`'s docstring updated to reflect the ruled state (previously said
  "not yet ruled"). Verified: `tests/test_locked_test_guard.py`'s real-config test
  (renamed `test_ph_the_real_config_reflects_its_actual_authorization_state`) now asserts
  `authorized is True` / `decision == "D-68"` and exercises a real end-to-end call against
  the actual committed config — passing.

## What was wired

`scripts/06_train_and_predict.py` (owned by `fixtures-and-reproducibility`/
`models-and-baselines` — the mechanism itself, in `governance-guards`' file, is untouched by
this step beyond the docstring update above):

- New `_persistence_history_augmented_target(...)` helper: for `model_id in
  PERSISTENCE_HISTORY_CALLERS` (M-01/M-02) only, calls
  `read_persistence_history_lookup` and returns a NEW `RecordFrame` — the original
  `locked_target` rows plus the 1-December lookup rows — WITHOUT mutating or re-scoring
  from `locked_target` itself. For every other model, or for M-01/M-02 when any of
  `g05_signature`/`locked_input`/`access_log` is missing, it raises rather than silently
  falling back (an unauthorized-but-silent skip would misreport why the scored set came up
  short — exactly what D-28's own disclosure guard exists to prevent).
- `_locked_predictions(...)` gains three new optional keyword parameters
  (`g05_signature`, `locked_input`, `access_log`, all defaulting to `None` — every existing
  caller, including every test, is unaffected) and now builds a per-model `model_target`
  via the helper above before each `fit_predict` call, instead of always using the shared
  `locked_target`.
- The one production call site (inside the DEC-partition branch of the stage's main loop)
  now passes `g05_signature=args.g05_signature`, `locked_input=Path(args.locked_input)`,
  `access_log=access_log` — the same three values the DEC loader itself already uses for
  `materialise_locked_partition`, reused rather than re-derived.

## Verification performed 2026-09-24

- `ast.parse` + `ruff check` on `scripts/06_train_and_predict.py`: clean.
- New wiring test, `tests/test_models_smoke.py::test_persistence_history_augments_only_m01_m02_and_only_with_all_three_inputs`
  (monkeypatches `read_persistence_history_lookup` to isolate the WIRING from the
  mechanism's own already-tested 5 conditions): confirms (a) a non-M-01/M-02 model_id is
  untouched and the lookup is never invoked; (b) M-01/M-02 with all three inputs receive an
  augmented frame carrying exactly the extra 1-Dec row(s), with the original row(s)
  unchanged; (c) M-01/M-02 with any of the three inputs missing raises rather than silently
  returning the unaugmented frame. **Passed.**
- Full `tests/test_models_smoke.py`: 71/71 passed (70 + 1 new), 1 skipped (pre-existing,
  unrelated).
- `ruff check` confirms the 4 pre-existing findings in `tests/test_models_smoke.py` (lines
  57, 61, 92, 1291) are all outside this change's diff (verified via `git diff`, which
  starts at line 1669) — none introduced by this pass.
- Full §18.3 critical set plus the two expanded modules
  (`test_locked_test_guard.py`, `test_models_smoke.py`) re-run together with
  `test_clean_run.py`: submitted as a background run; result appended below once complete.

## What this does NOT do

- Does not touch `D-28` or `D-59` — both remain exactly as originally frozen; this recovers
  the disclosed 30-day scored set through an additive lookup, not a redefinition.
- Does not change `locked_target` itself, nor any FITTED family's target (`predict_from_fitted`
  still receives the plain `locked_target`, unaugmented) — only M-01/M-02's own `fit_predict`
  call receives the augmented copy.
- Does not weaken any of D-68's 5 conditions — every condition is still enforced inside
  `read_persistence_history_lookup` itself; this wiring only supplies real call-site
  arguments where the mechanism was previously only reachable from tests.
