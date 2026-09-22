# Change record — `CR-2026-09-21-TOP1PCT`

**Date:** 2026-09-21 · **Decided by:** the project decision owner, explicitly, on that date ·
**Status:** written to config and implemented; one sub-choice remains open; proposed `D-54`
owed to `evidence/DECISIONS.md`

Closes `GOV-2026-09-20-CG-01` **Recommendation 21** / dispositions §5 item 14, which routed
the scope question to the gate because FR-P1-05-10 says *"top 1% of absolute errors removed"*
without saying **whose** top 1%.

---

## 1. The decision, as given

* `removed_fraction: 0.01`
* `scope: comparison_wide`
* preserve the established ranking variable, tie handling and rounding rule
* apply the **same retained rows to all compared models**
* recompute the established **equal-station-weighted** metrics
* report **removed/retained counts per station**
* **refuse an undefined comparison** if a station loses all support
* keep it a **supplementary sensitivity** — it never changes the primary results, selects a
  model, or tunes a parameter
* recorded **before** locked evaluation

## 2. What was already settled and is unchanged

| Element | Value | Source |
|---|---|---|
| Ranking variable | absolute error \|ŷ − y\| of each masked row | FR-P1-05-10's own wording |
| Tie handling | `(station, interval_start_utc)` ascending — deterministic on both platforms | WS-17 posture |
| Rounding | `k = ceil(removed_fraction × n)`; never `round` or `floor` | implemented |
| Exclusion procedure | removed rows dropped, metrics **recomputed** on the remainder | implemented |
| Empty-remainder guard | a support the rule would empty refuses | implemented |

## 3. The consequence of `comparison_wide`, recorded rather than glossed

Ranking all three stations together is the literal reading of the requirement. It is also
**not proportionate**: a station with systematically larger errors loses a larger share of its
rows, so the equal-station mean is then taken over **unequal per-station supports**. That is
precisely why the owner made the per-station removed/retained counts **mandatory output** — the
asymmetry is made visible to a reader instead of left to be inferred.

## 4. What had to be built, because the decision required behaviour that did not exist

`top1pct_removed_keys` ranks **a single member's** own errors, so each model would have been
scored on a **different support** — the very thing the comparison-wide mask exists to prevent
(NFR-FAIR-01). Four additions to `src/evaluation/diagnostics.py`:

| Added | What it does |
|---|---|
| `top1pct_comparison_removed_keys` | computes **one** removed set for the whole comparison and applies it to every member |
| `_assert_no_station_emptied` | refuses when any station retains no rows — under equal-station weighting such a station contributes no figure, so the comparison is **undefined**, not merely smaller, and is refused rather than averaged over the survivors |
| `top1pct_station_counts` | removed and retained counts per station |
| `top1pct_comparison_block` | the whole sensitivity: one removed set, every member recomputed, carrying `role: supplementary_sensitivity_only` and `may_inform_selection_or_tuning: false` **as data**, so a downstream consumer reads the bound rather than having to know it |

## 5. The one sub-choice the decision does not settle — `combination`

The decision fixes that the retained rows are **shared**. It does not fix **how** several
members' rankings become that one set, and the two available rules differ materially:

| Option | Behaviour | Trade-off |
|---|---|---|
| `union_of_member_top_k` | remove the union of each member's own top-`k`; a row that is any model's worst goes for all | Favours no model. The effective removed fraction then **exceeds 0.01** — reported as `effective_removed_fraction`, never hidden. |
| `rank_by_max_member_error` | rank each row once by its worst error across members, remove the top `k` | Exactly `k` rows go, so the declared 1% holds **exactly**, and no single member's ranking decides the set alone. |

Written as `combination: "TBD — freeze gate"`.
`top1pct_comparison_removed_keys` **refuses** while it is unset rather than defaulting to
either (TE §18.3). **This is the only remaining decision on this item.**

## 6. Controls (7, all synthetic, in `tests/test_regimes_and_reporting.py`)

`test_the_comparison_removes_one_shared_set_not_a_set_per_member` (on a fixture where the
members genuinely disagree about which rows are worst — the flat mask could not exercise the
defect), `test_rank_by_max_member_error_removes_exactly_k_rows`,
`test_the_combination_rule_is_declared_and_never_defaulted` (negative control),
`test_per_station_removed_and_retained_counts_are_reported`,
`test_a_station_left_with_no_retained_row_refuses_the_comparison` (negative control),
`test_the_block_recomputes_every_member_on_the_shared_remainder`,
`test_the_union_reports_its_effective_fraction_rather_than_hiding_it`.

## 7. Owed

`D-54` is a **proposed** number; the register entry is the student's to write. The decision is
recorded here and in `configs/experiment.yaml` **before locked evaluation**, as required. No
supervisor signature is claimed.
