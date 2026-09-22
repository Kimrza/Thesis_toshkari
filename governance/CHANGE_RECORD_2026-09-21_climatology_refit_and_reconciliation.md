# Change record — `CR-2026-09-21-CLIMATOLOGY-REFIT` and `CR-2026-09-21-RECONCILIATION`

**Date:** 2026-09-21 · **Authorized by:** the project decision owner, explicitly, on that date ·
**Status:** written to config; four proposed D-numbers owed to `evidence/DECISIONS.md`

---

## `CR-2026-09-21-CLIMATOLOGY-REFIT`

### §1 — M-03 climatology (proposed **D-55**)

The owner reaffirmed on 2026-09-21: the previously approved **station/hour, training-only**
climatology. Already written to `configs/experiment.yaml: models.climatology` on 2026-09-20
under `CR-2026-09-20-CONFIG-BLOCKS` §1; this record updates its `decision` field from
"pending" to the owner's approval of 2026-09-21. No value changed.

### §2 — refit epoch rule (proposed **D-56**)

The owner reaffirmed: **median best-validation epoch across the predefined pre-December folds
and seeds for the selected configuration, rounded half upward**. Already written to
`models.refit`; `epochs` correctly remains `TBD — freeze gate` because the value is the rule's
output and does not exist until the folds have run. Verified by execution: the rule over
`[5, 7, 8, 10]` returns **8** (median 7.5, rounded half up).

### §3 — the supervisor countersignature, recorded honestly

The owner states the supervisor **has approved and countersigned** both. That statement is
recorded here **as reported by the student**, which is this register's established form for
such an approval — D-46 carries the identical wording (*"supervisor countersigned 2026-09-19
per the student's report"*), as does D-19's note that the supervisor role is exercised under
the recorded delegation with no signature claimed.

**What is recorded:** the owner's approval of 2026-09-21, and the owner's report that the
supervisor countersigned the same day.
**What is NOT claimed:** a separate signed artifact. None exists in the workspace, none was
created, and nothing was backdated. If a countersigned document is expected as G-05 evidence,
producing that artifact is the outstanding requirement — the *statement* is recorded; the
*artifact* is not, and this record does not pretend otherwise.

---

## `CR-2026-09-21-RECONCILIATION`

Reconciling the remaining sentinels against existing decisions, per the owner's instruction to
transcribe approved values without asking again.

### §1 — `experiment.window_length_hours` → **24** (proposed **D-57**)

**Transcribed, not chosen.** Vision §8.1: *"History window: 24 hours primary, with a 48-hour
sensitivity evaluated only after the primary configuration is frozen … **History length is not
a tuned hyperparameter**."* TE §7.2's ablation table carries the same 24 as ABL-HIST48's
`primary_remains`. Same class of act as D-38 (`embargo_hours`) and D-51 (`horizons`).

Verified: `read_window_length(snapshot, sequence_steps=24)` returns 24, and the leakage guard
still refuses a mismatched sequence length (`sequence_steps=48` raises `LeakageError`), so
transcribing the value did not disarm the check that protected it.

### §2 — `experiment.models.selection` → D-124's rule (transcription)

**D-124 is recorded as Approved** in Vision §14.2: *"Select on mean per-fold skill versus a
declared baseline across F1–F4; prefer the simpler configuration within 1%; refit without
changing hyperparameters."* Vision §8.7 adds that no December result may influence the
criterion. Transcribed as a structured block (`criterion`, `folds: [F1…F4]`,
`simplicity_margin: 0.01`, `refit_changes_no_hyperparameter: true`,
`december_may_influence: false`) citing D-124.

### §3 — Still open, with the evidence and a concrete proposal for each

| Field | Evidence found | Proposed choice |
|---|---|---|
| `models.declared_baseline_per_track` | Vision §8.7 approves the **rule** ("the declared baseline per track is named in configuration before tuning begins") but **names no baseline anywhere**. Not a transcription. | **Persistence** as the declared baseline for every track — it is already a mandatory difficulty control (Vision §2.4 tier 2), is defined for every partition, and needs no fit. *Owner act, before tuning begins.* |
| `regimes.december_day_range` | **D-28** fixes the locked **scored set** as **2–31 December 2022 (30 days)**. Whether D-13's *comparison count* uses that same range is what `GOV-2026-08-28-FD-01` Rec 15 routed — a **Student + Supervisor** gate item, distinct from D-28. | **`2022-12-02..2022-12-31`**, matching D-28's scored set, so the regime count describes exactly the set that is scored. *Student + Supervisor, before G-05.* |
| `features.feature_set_id`, `features.feature_dictionary`, `features.normalization` | No approved value found anywhere in `evidence/DECISIONS.md` or the authority documents. Each is enforced at its own entry point, which refuses by name. | No proposal offered: the feature dictionary is the feature contract itself, and naming it is a design act, not a transcription. *Owning unit's transcription, before features are built.* |
| `reporting.top1pct_sensitivity.combination` | See `CR-2026-09-21-TOP1PCT` §5. | Either rule is defensible; `rank_by_max_member_error` holds the declared 1% exactly. *Owner/supervisor, before G-06.* |

### §4 — Proposed D-numbers owed

`D-53` (qc_operations), `D-54` (top-1% sensitivity), `D-55` (climatology), `D-56` (refit rule),
`D-57` (window length). All five are **proposed numbers**; `evidence/DECISIONS.md` was not
written by this session, because the register is the student's.
