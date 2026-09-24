# Change record — 2026-09-24 — `budget_value.statistic = p95` (draft D-number, partial freeze)

> **SUPERSEDED 2026-09-24** — merged with the sibling `combination` draft into one D-number,
> since both set fields of the same §18.2 item: `governance/CHANGE_RECORD_2026-09-24_budget_value_merged.md`.
> Left standing rather than deleted, per this project's history-preserving convention.

**Purpose.** Draft only. Not written to `evidence/DECISIONS.md`. `configs/data.yaml`'s
`target.uncertainty_budget.statistic` field has been set to `"p95"`; `decision` and
`combination` are left `"TBD — freeze gate"`. This is a **partial** freeze of a §18.2
forbidden-choice item — it does not close the item, and `resolve_budget_rule` (verified
2026-09-24 against the real, edited config) still correctly returns `None` because `decision`
and `combination` remain unset.

## Proposed D-number text (for the owner to adopt, with a real number, into `evidence/DECISIONS.md`)

> **D-6? `budget_value.statistic = p95` (partial freeze — statistic only; `combination` and
> this decision's own citation remain open)**
>
> | Countersignature | Date | Rationale |
> |---|---|---|
> | *(owner fills — Student, and Supervisor if the full item is to close together)* | *(owner fills)* | Sets the per-content summary statistic `resolve_budget_rule` reads from `configs/data.yaml: target.uncertainty_budget.statistic` to `p95`, one of two fields the §18.2 forbidden-choice item (`GOV-2026-09-20-CG-01` Recommendation 20 / dispositions §4.5) requires. **Literature basis** (Consensus search, 2026-09-24): forecast-verification practice for practical-relevance/decision thresholds favours tail-aware, decision-relevant statistics over central tendency — [Bouttier et al. (2024)](https://consensus.app/papers/details/571419dc7b7659b0900fef05315e3f8a/?utm_source=claude_desktop) explicitly optimise decision thresholds rather than reporting mean/median error for a "is this practically meaningful" question, and the MET/METplus forecast-verification toolkit ([Brown et al. 2020](https://consensus.app/papers/details/b5c9557092ce5684b901f760cb3fb182/?utm_source=claude_desktop)) is built around threshold-based rather than central-tendency statistics for this class of question. `p95` was chosen over `max` (single-point fragility — one anomalous standardized row should not set the whole practical-relevance bar) and over `median` (too permissive for a *budget* concept, which by its own name should lean conservative rather than describe the typical case). **This is a partial freeze only.** `resolve_budget_rule` requires `decision`, `statistic` AND `combination` to all be set before it returns a usable rule (verified 2026-09-24 against the real config: with `statistic` set alone, it still returns `None`); `practical_relevance_statement` continues to refuse, honestly, exactly as before this change. **This D-number does not by itself discharge Recommendation 20 or the §18.2 item** — `combination` (sum vs. quadrature vs. max) remains open pending the Supervisor's judgment on whether Phase 1 and Phase 2 uncertainty contents share a common systematic error source (literature basis for that question is in `governance/` search notes from the same session: quadrature is the standard GUM combination for independent components — [Fröhner 2003](https://consensus.app/papers/details/fab8b70c41ef56ccb17b990e1bcc47b1/?utm_source=claude_desktop), [Farrance et al. 2012](https://consensus.app/papers/details/c5042f2c740851fa9605f1de9945991e/?utm_source=claude_desktop) — while sum is the standard treatment for correlated/undetermined-correlation components — [Ferrero et al. 2013](https://consensus.app/papers/details/7e9026dcdac950939fe1660d88507f0a/?utm_source=claude_desktop), [Warsza & Clarkson 2020](https://consensus.app/papers/details/a1ba0bae4cdb51cba55e861e8149c1c0/?utm_source=claude_desktop)). Until `combination` and this decision's own D-number citation are both filled, `budget_value` stays `None` and Vision §5.3's second conjunct fails visibly rather than silently never running, exactly as designed. |

## Verification performed 2026-09-24

- `configs/data.yaml` diff: `statistic: "TBD — freeze gate"` → `statistic: "p95"`; `decision`
  and `combination` unchanged, still `"TBD — freeze gate"`.
- `resolve_budget_rule` (`src/data/prepared.py`) has no hardcoded fallback for any of its
  three required fields — confirmed by reading the function; it returns `None` if *any* of
  `decision`/`statistic`/`combination` is unset, with no special-casing.
- Ran directly against the real, edited config: `resolve_budget_rule(real_config) is None` —
  **confirmed**, printed above.
- `p95`, the literal now in the config, is one of the three values `_statistic()`
  (`src/data/prepared.py`) already implements (`median`/`p95`/`max`) — no new code needed for
  the value itself, only for the gate to actually open once `combination`+`decision` land.
- Test suite: 14/14 budget-specific tests pass (`test_prepared_target_schema.py`,
  `test_common_masks.py`, `test_regimes_and_reporting.py`); full `test_prepared_target_schema.py`:
  74/74 pass. All run under the governed `tec-thesis-311` (Python 3.11.16) environment.

**Decision required — Approve / Reject / Modify / Postpone**, on both the `statistic` value
itself and whether to write this D-number now (partial) or hold it until `combination` is
also ready, closing both fields under one D-number instead.
