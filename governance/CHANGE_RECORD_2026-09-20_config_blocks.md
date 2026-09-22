# Change record — `CR-2026-09-20-CONFIG-BLOCKS`

**Date:** 2026-09-20 · **Author:** implementation session, under the project decision owner's
explicit instruction of the same date · **Status:** implemented; two D-numbers owed, one
supervisor freeze outstanding

---

## 1. Scope

Three configuration blocks, written under the owner's stated decisions. **No scientific value
was chosen by the implementer.** Two blocks transcribe rules the owner gave in writing; one
transcribes identifiers already approved elsewhere; one open question is written as sentinels
with the choice stated rather than filled.

Full field-by-field reconciliation of all 23 live sentinels:
`artifacts/exec_evidence/run_2026-09-20/CONFIG_SENTINEL_RECONCILIATION.md`.

## 2. §1 — `experiment.models.climatology` (closes Recommendation 2's config limb)

The owner's decision, as given: *"implement the previously approved station-and-hour mean,
fitted exclusively on each partition's training data. Remove month from the key, retain the
governed time convention, document the seasonal limitation, and fail early for missing
required keys."*

Written as `key: ["station", "hour"]`, `fitted_on: "training_partition_only"`,
`time_convention: "utc_hour_of_interval_start_utc"`, plus the seasonal limitation in full.

`src/models/climatology.py` already implemented exactly this and needed no change: a key field
it cannot compute refuses **by name** (so a month-bearing key cannot be re-adopted by editing
config alone), a key in a different order refuses, and `fitted_on` other than the one token
refuses as a `LeakageError`. Missing keys at prediction time stay missing, never filled.

**Proposed D-number text: reconciliation §F.1. Supervisor countersignature REQUIRED and OPEN.**

## 3. §2 — `experiment.models.refit` (closes Recommendation 5's rule limb)

The owner's decision, as given: *"median best-validation epoch across the predefined
pre-December folds and seeds for the selected configuration, rounded half upward. Derive the
numeric count from actual validation results, then freeze it before final refit and G-05. Do
not require that derived count before the validation runs that produce it."*

Written as `rule: median_best_validation_epoch_across_folds_and_seeds_round_half_up`,
`rule_inputs`, `rounding: half_up`, `december_role: inference_only`, and
**`epochs: "TBD — freeze gate"`**, which is the decided state, not an open question: the value
does not exist until the folds have run. Nothing but the refit itself reads it, so the sentinel
blocks no earlier stage — the validation runs that produce the number run with `epochs` unset.

`src/models/train.py` already implements the rule (`refit_epoch_count`, `REFIT_EPOCH_RULE_ID`)
and `assert_refit_epochs_match_rule` re-derives it from the recorded fold/seed epochs and
refuses a transcribed value that is not the rule's own output. Verified by execution: the rule
over `[5, 7, 8, 10]` returns **8** (median 7.5, rounded half up), and `read_refit_epochs`
refuses today naming `models.refit.epochs`.

**Proposed D-number text: reconciliation §F.2. Supervisor countersignature REQUIRED and OPEN.**

## 4. §3 — `data.target.identity` (transcription; no new approval requested)

The three TEC-05 definition IDs — `phase_id: P1A`, `source_id: GNSS_VTEC`,
`target_definition_id: GRIDDed_VTEC_1H` — are **copied** from the owner's own Q-31 identity
declarations, where they were already approved:

* `tests/fixtures/plumbing_7day/identity_declaration.yaml:39-41`
* `tests/fixtures/scientific_1month/identity_declaration.yaml:37-39`

frozen under D-11 / D-14 / `CR-2026-09-13-000102-FIXTURE-WINDOW`; `target_definition_id` was
already transcribed into `experiment.yaml: benchmark_b01`, where B-01 is scored against that
same target definition. Per the owner's instruction — *"populate values already approved; do
not request the same approval again"* — no approval is requested for these.

**Why it was owed.** TE §13 / R-70 require all three on every dataset, prediction, mask and
comparison, and `resolve_target_identity` refuses while `target:` is absent. Since the
Recommendation 24 remediation routed stage 01's audit path through that resolver, the **required
pre-G-05 December coverage audit was itself unrunnable** (remediation manifest, escalation 2).

**Controls added** (`tests/test_prepared_target_schema.py`): config equals both declarations;
the two declarations equal each other; the resolver's output equals the declaration; and a
negative control proving the resolver still refuses an absent, partial or sentinel identity —
transcribing a value did not disarm R-70.

## 5. §4 — `experiment.reporting.top1pct_sensitivity` (NOT resolved, written as sentinels)

I searched for an existing approved definition and there is none. What is already settled is
implemented and is not re-asked (ranking variable, tie handling, `ceil` row count, recompute-
on-remainder, never merged with the primary result, refusal on a support that would be emptied).

Two values are owed and are written as sentinels with the choice stated at the point of use:
`removed_fraction` (the literal "1%") and `scope` (`comparison_wide` vs `per_station` — material
under equal-station weighting). `read_top1pct_declaration` refuses on either.

**Supervisor, before G-06** (Rec 21; dispositions §5 item 14). Options stated in full at
reconciliation §E.

## 6. Correction made to a test, not to a config

`tests/test_clean_run.py`'s precondition scanner named `experiment.folds` as the clean run's
first unmet precondition and attributed a mechanism to it — *"every stage entry refuses at
`assert_no_tbd`"*. Measured: `folds` is in no `REQUIRED_FIELDS_MAP` entry, so `assert_no_tbd`
never sees it, and D-38 records the owner's 2026-09-10 ruling that it stays unresolved
deliberately. Verified by execution — `scripts/01_inventory_and_registry.py` completed inside
the fixture sequence with `folds` still `TBD — freeze gate`.

The scanner was therefore reporting a permanently unmeetable precondition and masking the real
one. It now reads block-valued fields through pyyaml (installable in this environment since
2026-09-20) and reports `configs/data.yaml: qc_operations`, which is what actually stops the
run. No config value changed to make this true.

## 7. What is still owed

| Item | Who | Due |
|---|---|---|
| Adopt §F.1 and §F.2 as D-numbers in `evidence/DECISIONS.md` | Student | before G-05 |
| Countersign §F.1 and §F.2 | Supervisor | before G-05 |
| Freeze `data.qc_operations` under a D-number (shape at §F.3) | Supervisor | **blocks the fixture run now** |
| Rule on `top1pct_sensitivity.removed_fraction` and `.scope` | Supervisor | before G-06 |
| Adopt dispositions §4.4 (`window_length_hours`) | Student + Supervisor | before features build |

Nothing was written to `evidence/DECISIONS.md`. No supervisor signature is claimed, implied or
backdated anywhere in this record or in the configs it describes.
