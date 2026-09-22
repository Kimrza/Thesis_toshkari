# Configuration sentinel reconciliation — 2026-09-20

Every `TBD — freeze gate` field live in the four governed configs, the stage that reads it,
whether an approved value already exists, and the authority for that.

**Derived programmatically and printed before assertion** (`yaml.safe_load` over all four
configs, recursive scan for the literal sentinel). **23 live sentinel fields**, not the 25 I
reported at the end of the previous session — that figure counted five sentinel mentions in
*comments* as fields and missed the two this session added under `reporting`. The per-file
split is experiment.yaml **20**, features.yaml **3**, data.yaml **0**, seeds.yaml **0**.

`configs/data.yaml` now carries **no** sentinel at all: its one former mention was a comment.

---

## A. Not open questions — the sentinel IS the decided state (3)

Nothing is owed on these. They must not be "resolved".

| Field | Stage that reads it | Authority |
|---|---|---|
| `experiment.folds` | **none — no reader exists** in `src/` or `scripts/` | Owner ruling 2026-09-10, recorded in **D-38**: leave TBD, do not remove, so `configs/data.yaml: partitions` stays the single source of truth for the split calendar. |
| `experiment.practical_relevance_threshold` | reporting | **D-34** (2026-09-10): no numeric threshold is approved; the *rule* is the frozen object. A number would need explicit supervisor approval and its own D-number, and is barred once December is opened. |
| `experiment.models.refit.epochs` | the final refit only | **Decided this session** (§C below): the RULE is frozen; the NUMBER is its output and cannot exist until the pre-December folds have run. Frozen under its own D-number before the refit and before G-05. |

**One correction carried from execution.** `tests/test_clean_run.py`'s precondition scanner
named `folds` as the clean run's first unmet precondition and attributed a mechanism to it —
"every stage entry refuses at `assert_no_tbd`". That is false: `folds` appears in no
`REQUIRED_FIELDS_MAP` entry, so `assert_no_tbd` never sees it. Verified by execution —
`scripts/01_inventory_and_registry.py` ran to completion with `folds` still unresolved. The
scanner was reporting a permanently unmeetable precondition and masking the real blocker
beneath it; it now reads block-valued fields through pyyaml (installable here since this
session) and names `configs/data.yaml: qc_operations`, which is what actually stops the run.

## B. Written by a run, never by a human or an implementer (11)

These acquire values as outputs of governed runs. A sentinel here is correct until that run
happens, and none of them blocks an earlier stage.

| Field(s) | Stage that writes it | Note |
|---|---|---|
| `experiment.models.selected` | the tuning run's selection record | R-101: chosen on mean per-fold skill over F1–F4, January–November only. `06_train_and_predict.py` refuses while unset. |
| `experiment.ablations.entries.*.run_id` (5)<br>`experiment.ablations.entries.*.registered_at` (5) | the owner's registration act, before the freeze | R-97 / TE §7.2: ablations are predeclared named runs. Identities, the §7.2 question and the configuration change are already transcribed; only the registration stamps are owed. |

## C. Resolved this session (3 blocks, from already-approved values or the owner's stated rules)

| Field | Stage | Value written | Authority |
|---|---|---|---|
| `data.target.identity.phase_id` | 01 inventory, every stamping stage | `P1A` | **Transcription of an already-approved value.** All three appear identically in both owner-authored Q-31 identity declarations (`tests/fixtures/plumbing_7day/identity_declaration.yaml:39-41`, `scientific_1month/identity_declaration.yaml:37-39`) under D-11 / D-14 / `CR-2026-09-13-000102-FIXTURE-WINDOW`, and `target_definition_id` was **already transcribed** into `experiment.yaml: benchmark_b01`. No new approval requested. |
| `data.target.identity.source_id` | ” | `GNSS_VTEC` | ” |
| `data.target.identity.target_definition_id` | ” | `GRIDDed_VTEC_1H` | ” |
| `experiment.models.climatology` | M-03 fit | `key: [station, hour]`, `fitted_on: training_partition_only`, `time_convention: utc_hour_of_interval_start_utc`, seasonal limitation recorded | **Owner decision of 2026-09-20.** Closes Rec 2. Month removed from the key. |
| `experiment.models.refit` | final refit | `rule: median_best_validation_epoch_across_folds_and_seeds_round_half_up`, `rounding: half_up`, `december_role: inference_only`; `epochs` stays sentinel | **Owner decision of 2026-09-20.** Closes Rec 5's rule limb. |

Three controls added in `tests/test_prepared_target_schema.py` bind the transcription to its
source: config must equal both declarations, the declarations must equal each other, and the
resolver's output must equal the declaration. A negative control proves the resolver still
refuses an absent, partial or sentinel identity — transcribing a value did not disarm R-70.

## D. Genuinely unresolved — a human decision is owed (9 fields, 5 questions)

Nothing was invented for any of these. Each carries a sentinel and each reader refuses by name.

| # | Field(s) | Who | Due | What is owed |
|---|---|---|---|---|
| Q1 | `data.qc_operations` **(absent, not sentinel)** | Supervisor freeze | **blocks the fixture run now** | The enumerated documented-QC operation list, **frozen under a D-number**. `assert_qc_operations_frozen` requires a D-number citation *and* a non-empty list — explicitly "never mere non-emptiness, since a list filled by convenience satisfies 'non-empty'". This is the current first unmet precondition of the clean run. |
| Q2 | `experiment.window_length_hours` | Student freeze + countersignature | before features build | 24 h, per Vision §8.1 ("history length is not a tuned hyperparameter") and TE §7.2's own ablation table (ABL-HIST48: "48 h window … primary remains 24 h"). Draft already prepared at dispositions **§4.4**; it needs adoption, not drafting. |
| Q3 | `experiment.models.declared_baseline_per_track`, `experiment.models.selection` | Owner transcription | before tuning | Vision §8.7 / D-124's per-track declared baseline and the mean-per-fold-skill + 1%-simplicity selection rule. Both exist upstream; neither is transcribed. |
| Q4 | `experiment.regimes.december_day_range` | **Student + Supervisor** | before G-05 | Which December day range governs D-13's comparison count (`GOV-2026-08-28-FD-01` Rec 15). Mechanism written; value routed. |
| Q5 | `experiment.reporting.top1pct_sensitivity.removed_fraction`, `.scope` | Supervisor | before G-06 | See §E. |
| — | `features.feature_set_id`, `features.feature_dictionary`, `features.normalization` | owning unit's transcription | before features build | Enforced at their own entry points (`load_feature_dictionary`, `build_features`), which refuse by name; not preflight-gated, so they block only the stage that reads them. |

## E. Q5 in full — the top-1% sensitivity (Recommendation 21)

I searched for an existing approved definition and **there is none**: `FR-P1-05-10` says "top
1% of absolute errors removed" and settles no more than that. What is already settled and is
**not** being re-asked, because it is implemented in `src/evaluation/diagnostics.py`:

* **Ranking variable** — the absolute error `|ŷ − y|` of each masked row. Fixed by the
  requirement's own wording.
* **Tie handling** — ties break by `(station, interval_start_utc)` ascending, so the removal is
  deterministic on both governed platforms (WS-17 posture).
* **How many rows** — `k = ceil(removed_fraction × n)`: `ceil`, never `round` or `floor`, so a
  declared removal never silently removes nothing on a small support.
* **Exclusion and comparison procedure** — removed rows are dropped, every metric is
  **recomputed** on the remainder, and the result is reported as its own labelled figure,
  never merged with the primary result (Vision §2.4 honesty rule).
* A support on which the rule would remove every row **refuses**; the remainder must be
  non-empty for the recomputed metrics to exist.

**Two values are owed.**

**Q5a — `removed_fraction`.** The "1%" as a literal fraction. `0.01` is the obvious reading,
but a scientific literal belongs in a freeze act, not an implementer's edit (TC-03e; TE §18.3).

**Q5b — `scope`: whose top 1%?** This is the material one, and under equal-station weighting
(Vision §2.3) the two readings genuinely differ:

| Option | What it does | Consequence |
|---|---|---|
| **A. `comparison_wide`** | Rank every masked row across all three stations together; drop the largest `removed_fraction`. | The literal reading of the requirement's wording. A station with systematically larger errors loses a larger share of its rows, so the equal-station mean is then taken over **unequal per-station supports** — which is in tension with the equal-station weighting the estimand fixes. |
| **B. `per_station`** | Rank within each station; drop that station's own largest `removed_fraction`. | Supports stay proportionate and equal-station weighting keeps its meaning, but the rows removed are **not the comparison's largest errors**, which is what the requirement's wording most directly names. |

`comparison_wide` is the module's coded **default** because it is the literal reading. It is a
default, not a decision; the configured field is what the gate rules on. **Supervisor, before
G-06** (dispositions §5 item 14).

---

## F. Exact amendments prepared, for adoption

Drafted here; **not** written into `evidence/DECISIONS.md`, which is the student's register. No
supervisor signature is claimed or implied for any of them.

### F.1 — proposed D-number: M-03 climatology key *(supervisor countersignature required)*

> **Decision.** M-03's climatology key is the mean of the target grouped by **station and
> hour**, fitted exclusively on each partition's own training data. **Month is removed from
> the key.**
>
> **Why.** A month-bearing key can predict for **no** scored month: under the expanding-window
> splits (D-38 / R-80) every partition's validation month lies strictly after its own training
> range, so every scored row looked up a key the training data cannot contain. M-03 is one of
> the three mandatory difficulty controls (Vision §2.4 tier 2; PC-03/PC-04), so an M-03 that
> yields no prediction empties the comparison-wide mask for every comparison it belongs to
> (`GOV-2026-09-20-CG-01` Recommendation 2).
>
> **Limitation, mandatory wherever M-03 is reported.** A station-and-hour mean carries no
> seasonal term. It cannot represent December's diurnal amplitude or level differing from the
> January–November training mean, and it is not a seasonal climatology. This is the deliberate
> cost of a key that can predict for every scored month at all.
>
> **Time convention.** `hour` is the UTC hour of `interval_start_utc`, unchanged from D-16/D-17.
> No local-solar-time variant is introduced; longitude reaches the model only through
> `lst_sin`/`lst_cos` (TE §7.2).

### F.2 — proposed D-number: refit epoch rule *(supervisor countersignature required)*

> **Decision.** The final refit's epoch count is the **median best-validation epoch across the
> predefined pre-December folds (F1–F4) and the final seeds, for the selected configuration,
> rounded half upward**. The rule is frozen now; the number is its output.
>
> **Derivation and freeze.** The inputs are the epochs the fold fits actually restored
> (`Checkpoint.epoch`, the lowest-validation-RMSE epoch, R-94), one per (fold, seed) pair, all
> pre-December. The resulting integer is transcribed into `experiment.models.refit.epochs`
> under its own D-number **before the final refit and before G-05**. It is not required before
> the validation runs that produce it.
>
> **December's role.** The refit trains for exactly that many epochs on the permitted
> January–November REFIT training data, with **no validation set and no early stopping**, so no
> December row can reach a stopping decision. December is inference-only
> (`GOV-2026-09-20-CG-01` Recommendation 5).

### F.3 — exact amendment owed for Q1, `data.qc_operations`

The field must be added to `configs/data.yaml` in this shape, with the list enumerated by the
freeze act and the citation naming the D-number that performs it:

```yaml
qc_operations:
  decision: "D-<n>"          # the D-number that freezes the list; a citation is REQUIRED
  operations: [ ... ]        # the enumerated documented-QC operations, non-empty
```

`assert_qc_operations_frozen` refuses a bare string, a mapping without a D-number citation, and
an empty list. The four permitted *transformations* (`documented_qc`, `utc_normalization`,
`cell_selection`, `hourly_aggregation`) are already closed in code (FR-P1-03-1; R-64); what is
owed is the enumeration of the operations **inside** `documented_qc`.
