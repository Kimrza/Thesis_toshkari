# Change Record — the fixture-scale grid point becomes an owner-frozen apparatus constant

**Date:** 2026-09-25
**Change ID:** CR-2026-09-25-APPARATUS-HYPERPARAMETERS
**Owning units:** `fixtures-and-reproducibility` (`src/data/fixture_manifest.py`,
`tests/test_clean_run.py`) and `models-and-baselines` (`scripts/06_train_and_predict.py`,
`tests/test_models_smoke.py`). Cross-unit change; both units' `code-summary.md` are now stale
with respect to these modules and that staleness is carried HERE as an explicit disclosure
(`project.md` `code-generation:gf-3`) rather than silently left to their readers.
**Owner instruction:** the Student selected option A on 2026-09-25 ("apparatus hyperparameters
in the fixture identity") after the circular-refusal disclosure reproduced in §1.
**Decision numbers relied on:** D-121 (frozen grids), D-124 (selection rule), D-58 (declared
baseline), D-11/D-20 (fixture identity precedents for a Student-owned apparatus freeze).
**No scientific value moves in this change.** The mechanism lands here; the VALUES land only
after the Student adopts the proposed decision in §6 — that adoption is the gate this record
stops at.

## 1. The defect: a circular refusal, verified in code

At the working tree of commit `0e0377b`:

1. The walking-skeleton orchestrator invokes stage 06 with `--fixture-manifest`, never
   `--tune` (`scripts/run_walking_skeleton.py`, `lifecycle_arguments` / `build_phase1_commands`),
   which dispatches to `_run_fixture_scale` (`scripts/06_train_and_predict.py: _run`).
2. `_run_fixture_scale` called `_selected_params(snapshot, model_id)` for every model in
   `MODEL_IDS`, unconditionally, inside the partition loop.
3. `_selected_params` raises `IntegrityError` for M-04/M-05/M-06 while
   `configs/experiment.yaml: models.selected` reads `TBD — freeze gate` — which it does, by
   design: that field is the governed tuning run's OUTPUT (R-101/D-124), "written by the
   tuning run's selection record, never by an implementer".
4. The governed tuning run is a full-year job, so `require_receipts_for_snapshot` gates it
   (TE §9.2; the exemption applies only WITH a fixture manifest) — it requires BOTH fixtures
   frozen.
5. Frozen fixtures require the fixture pass that (3) refuses. No fixture can pass, so no
   tuning can run, so `models.selected` can never be produced, so no fixture can pass.

Skipping M-04..M-06 at fixture scale is not an escape: TE 15.4's required outputs include
`predictions.parquet` and `metrics.json`, and stage 07's evaluation consumes the full model
set. Relaxing the receipts gate for tuning would violate TE §9.2's hard rule (both fixtures
before any full-year job). This is a specification-level contradiction between TE §9.2 and
R-101/TE §7.0B, surfaced rather than carried silently (`phases/inception.md`).

## 2. The mechanism (option A, owner-selected)

The fixture scope (identity declaration, and the candidate/frozen manifests composed from it)
may carry a new `apparatus_hyperparameters` block: one owner-frozen grid point per fitted
track. It follows the `apparatus_normalization` precedent exactly — an apparatus constant
(R-122), not a scientific value, owner-ruled into the scope file and readable ONLY through a
fixture scope, which a governed run never carries.

Safety properties, each pinned by a negative-control test (§4):

- **Never a second selection.** Every point must be a MEMBER of D-121's frozen grid,
  asserted at use by `assert_in_grid` (R-96's analogue). The apparatus picks among frozen
  members; it can never invent a value or a range (a list posing as a point refuses at the
  schema — "D-121 owns the one grid").
- **Never a default.** An absent block or track REFUSES naming the field (TE 18.3) — exactly
  as `_selected_params` refuses, so nothing became quietly optional.
- **Never uncited.** The schema requires a `citation` carrying the owner's freezing D-number
  and a non-empty `reason`; an uncited grid point is a selection with no record.
- **The governed path is untouched.** `_selected_params` is byte-identical; the governed
  full-year path still reads `models.selected` and still refuses while it is
  `TBD — freeze gate`. The pre-existing negative control
  (`test_the_dec_path_is_unreachable_without_the_g05_guard_and_the_three_arguments`) still
  pins that refusal.
- **Never copied into configs/.** The block lives in the fixture scope only; nothing reads
  it outside `_apparatus_params`, and the D-number text in §6 carries the explicit
  restriction that the apparatus point is not a prior, default, or candidate ranking for the
  governed selection.

## 3. The changes

1. `src/data/fixture_manifest.py`: `APPARATUS_HYPERPARAMETERS_KEY`,
   `APPARATUS_HYPERPARAMETER_TRACKS` (an identity enumeration mirroring
   `src/models/train.py: GRID_TRACKS`, guarded by test — the data layer must not import the
   models layer), `_validate_apparatus_hyperparameters` (shape, tracks, scalar-per-axis,
   reason, D-number citation), properties on `FixtureManifest` and `IdentityDeclaration`,
   wired into `validate_manifest_mapping` and `load_identity_declaration`.
2. `scripts/06_train_and_predict.py`: new `_apparatus_params(scope, snapshot, model_id)`;
   `_run_fixture_scale` now resolves grid-track params through it instead of
   `_selected_params`. `_run_fixture_scale`'s docstring names the one deliberate divergence
   from the full-year path's refusals. **Found by execution against the real config
   (post-adoption, 2026-09-25):** enumerated grid members carry D-121's `fixed` entries
   (`random_forest.max_features: "sqrt"`) and `assert_in_grid` requires exact key-set
   equality, so an axes-only scope point refused. Resolution: the scope declares AXES only
   (exactly D-70's positional rule) and `_apparatus_params` completes the point with the
   track's `fixed` block from the one grid in config — a second transcription in the scope
   would be a copy that can drift; a scope value contradicting a fixed entry survives the
   merge and is refused by the membership check. Pinned by two added test limbs (merge
   case; contradicting-fixed refusal). D-70's adopted text needed no change.
3. `compose_candidate_manifest` extras now carry `apparatus_normalization` and
   `apparatus_hyperparameters` into the composed candidate (see §5, defect A).
4. `--tune`'s target local renamed `tune_target` (see §5, defect B).
5. Tests per §4.

## 4. Verification

Environment: conda env `tec311`, Python 3.11.16 (the governed pin), local Windows platform.

- New negative controls, all passing: unknown track; uncited point; range posing as a point;
  missing reason; valid block validates on both scope kinds; `_apparatus_params` four-limb
  test (M-01..M-03 stay `None`; a declared track resolves with NO `models.selected` present —
  independence is the point; an undeclared track refuses naming
  `apparatus_hyperparameters.<track>` AND teaching the `models.selected` boundary; an
  off-grid point refuses at `assert_in_grid`); track-enumeration drift guard vs `GRID_TRACKS`;
  compose-carries-both-apparatus-blocks.
- Full suite: **1593 collected, 0 failed, 3 skipped, exit 0** (counts derived from the
  captured run output and printed before assertion; skips are the pre-existing
  dependency-presence skips).

## 5. Two pre-existing defects found while making this change, both fixed here

**A. `compose_candidate_manifest` dropped `apparatus_normalization`.** Its extras tuple
carried only `apparatus_partitions` and `fixture_bootstrap`, so a composed candidate silently
LOST the declaration's normalization override — a later comparison run would refuse at
`fit_transforms` on the constant column the override exists for (owner ruling 2026-09-23 §5
option 1 would have been silently undone at candidate scale). Fixed by carrying both
apparatus blocks; pinned by `test_compose_carries_both_apparatus_blocks_into_the_candidate`.

**B. `test_a_dec_iteration_handed_the_pre_loop_target_is_refused` was FAILING at HEAD
`0e0377b`** — not caused by this change. The test's source scan asserts the literal
`target=target` appears nowhere in `06_train_and_predict.py` (the R-102a guard that no
scoring call consumes the DEC path's pre-loop released target). The `--tune` section
committed 2026-09-25 introduced four occurrences via a local variable named `target`, and
the full `test_models_smoke.py` suite was evidently not re-run against the final `--tune`
state before commit. The variable (and `_fit_candidate`'s parameter) is renamed
`tune_target`; the scan passes again. The guard's intent was never violated — the tune-scale
target is the fixture-scale released target, not the DEC object — but the textual control
was defeated, which is exactly what the control exists to catch. Disclosed here because the
prior session's verification claim ("71/72 passing") did not hold at HEAD for this module.

## 6. PROPOSED decision for the Student to adopt (draft — NOT adopted, NOT in force)

**ADOPTED 2026-09-25 as D-70** (`evidence/DECISIONS.md`), verbatim below, on the Student's
explicit instruction; the register row was transcribed by the coding agent on that
instruction, with the transcription attributed inside the row itself. Numbering: the Student
first named D-125; the pre-write collision check found Vision §14.2 already owns D-125
(comparison-wide masks row, Approved, cited by REQ-FAIR-01 and N-06), and the Student
re-ruled the number to D-70, the register's next free number. The draft below is kept
unedited as the text that was adopted.

Nothing below is in force until the Student writes it, with a real D-number and date, into
`evidence/DECISIONS.md`. Per `project.md` (`code-generation:c31`) this draft exists so the
act stays the Student's without the blank-page cost.

> **D-1xx (proposed) — Apparatus hyperparameter points for the walking-skeleton fixtures**
>
> For fixture-scale walking-skeleton runs only, the fixture scope carries one apparatus
> grid point per fitted track, selected by POSITION — the first transcribed element of each
> grid axis in `configs/experiment.yaml` (D-121's transcription order) — with zero
> discretion and before any result of any kind has been observed:
>
> - `ridge` (M-04): `alpha: 0.01`
> - `random_forest` (M-05): `n_estimators: 300`, `max_depth: 8`, `min_samples_leaf: 1`
> - `lstm` (M-06): `layers: 1`, `units: 32`, `learning_rate: 1.0e-3`, `batch_size: 64`
>
> Restrictions, mandatory: these points exercise the plumbing apparatus (TC-03f: smoke
> evidence, never scientific evidence) and are NOT a prior, a default, a ranking signal, or
> a candidate shortlist for the governed selection; `models.selected` remains
> `TBD — freeze gate` until the governed January–November F1–F4 tuning run produces it under
> D-124's rule, and no comparison between these apparatus points and any tuning result may
> be drawn. The positional rule exists so the choice cannot be performance-informed even in
> principle.
>
> Owner: Student (Q-31's class: fixture apparatus is student-owned; no supervisor
> countersignature required per team.md § Walking Skeleton).

Alternative offered and not recommended: the minimum-CPU-cost member per track (faster
plumbing runs). Rejected in this draft because "cheapest" requires a runtime judgment that
is itself a choice, where the positional rule leaves no judgment at all.

## 7. What is gated, and on what

**GATE PASSED 2026-09-25:** D-70 verified on disk in `evidence/DECISIONS.md`; the block was
then written into `tests/fixtures/plumbing_7day/identity_declaration.yaml` citing D-70. The
paragraph below is kept as the gate's original statement.

The `apparatus_hyperparameters` block is NOT yet written into
`tests/fixtures/plumbing_7day/identity_declaration.yaml`. The executor of the next step
checks, on reaching it, that `evidence/DECISIONS.md` carries the adopted decision with a
real D-number and date (`project.md` `code-generation:c5`), writes the block with that
citation only then, and stops if it is absent. After that write, the Phase 1 measuring run
(`--emit-candidate --identity ...`) becomes the first end-to-end attempt — noting, per the
2026-09-25 session disclosure, that the plan's step 1.2 "plain comparison run" cannot
precede 1.3: the reference manifest at `tests/fixtures/plumbing_7day/fixture_manifest.yaml`
is the Recommendation 37 structural skeleton (`status: candidate`, sentinel-laden) and the
one loader refuses it, so the measuring run IS the end-to-end run.
