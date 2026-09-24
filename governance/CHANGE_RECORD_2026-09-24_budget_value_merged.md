# Change record — 2026-09-24 — `budget_value` merged D-number (statistic + combination)

**Purpose.** Combines the two prior same-day drafts —
`governance/CHANGE_RECORD_2026-09-24_budget_value_statistic.md` and
`governance/CHANGE_RECORD_2026-09-24_budget_value_combination.md` — into one D-number, since
both set fields of the same single §18.2 forbidden-choice item
(`configs/data.yaml: target.uncertainty_budget`). Neither prior draft is deleted; each now
carries a one-line pointer to this file. **Still a draft — not written to
`evidence/DECISIONS.md`.**

## Where `decision` actually lives — checked directly, not assumed

```
$ sed -n '281,296p' configs/data.yaml
  uncertainty_budget:
    ...
    decision: "TBD — freeze gate"
    statistic: "p95"
    combination: "sum"
```

**`decision` is a third sub-field of the same `target.uncertainty_budget` block** —
`resolve_budget_rule` (`src/data/prepared.py`) reads all three (`decision`, `statistic`,
`combination`) from this one mapping and requires all three set before returning a usable
rule; `decision` specifically must be a string starting with `"D-"` (verified by reading the
function). It is not a separate config location or a downstream item — it is this same block's
own citation field, currently the sentinel.

**Consequence: this D-number is what fills `decision`.** Once ruled and its number written
into `configs/data.yaml: target.uncertainty_budget.decision`, all three fields are set and
`resolve_budget_rule` returns a usable rule for the first time — `budget_value` stops being
`None`, and `practical_relevance_statement` stops refusing. **Until then, this draft existing
does not close the item** — the D-number must actually be ruled and its citation written into
the config field itself.

## The merged rule

| Field | Value | Status |
|---|---|---|
| `statistic` | `p95` | Set in config, this D-number is the pending citation |
| `combination` | `sum` | Set in config, this D-number is the pending citation |
| `decision` | *(this D-number, once assigned)* | **Still `TBD — freeze gate`** — the one remaining gap |

## Full rationale (both halves, literature preserved from both prior drafts)

### `statistic = p95`

Per-content summary statistic, applied over standardized rows, before the two per-content
scalars are combined. Forecast-verification practice for practical-relevance/decision
thresholds favours tail-aware, decision-relevant statistics over central tendency:
[Bouttier et al. (2024)](https://consensus.app/papers/details/571419dc7b7659b0900fef05315e3f8a/?utm_source=claude_desktop)
explicitly optimise decision thresholds rather than reporting mean/median error for a
"practically meaningful" question, and the MET/METplus toolkit
([Brown et al. 2020](https://consensus.app/papers/details/b5c9557092ce5684b901f760cb3fb182/?utm_source=claude_desktop))
is built around threshold-based statistics for this class of question. `p95` was chosen over
`max` (single-point fragility — one anomalous standardized row should not set the whole
practical-relevance bar) and over `median` (too permissive for a *budget* concept, which by
its own name should lean conservative rather than describe the typical case).

### `combination = sum`

How the two per-content TECU scalars (Phase 1, Phase 2) become one `budget_value`. Two
converging lines of evidence:

**Domain-specific**: GNSS-derived TEC/VTEC products share a well-documented common systematic
error source — differential code bias (DCB) estimation — across processing levels and
products:
[Chen et al. (2026)](https://consensus.app/papers/details/6dcc64144644599db0819d5b08e65c52/?utm_source=claude_desktop)
confirm systematic TEC-map bias "primarily stems from ... DCB estimation strategy and choice
of mapping function"; [Zhang et al. (2018)](https://consensus.app/papers/details/1cf7c2a93f8258aca2279d9174da756f/?utm_source=claude_desktop)/[(2023)](https://consensus.app/papers/details/806b64787d305afa94ae9059fb06e99c/?utm_source=claude_desktop)
and [Li et al. (2018)](https://consensus.app/papers/details/984c32a0c6e75c27929e93aae0c58b27/?utm_source=claude_desktop)
show DCB errors propagate measurably into VTEC accuracy across products;
[Hernández-Pajares et al. (2017)](https://consensus.app/papers/details/6c9fd1e894a65cfdb38649b8d071d4b6/?utm_source=claude_desktop)
report significant correlation between error metrics of two independently-computed VTEC
assessment methods over the same physical ionosphere.

**General metrology (GUM)**: quadrature (root-sum-square) is the standard combination only
for genuinely independent/uncorrelated components —
[Fröhner (2003)](https://consensus.app/papers/details/fab8b70c41ef56ccb17b990e1bcc47b1/?utm_source=claude_desktop):
*"common ('systematic') and uncorrelated ('random') errors are to be added in quadrature"*
(the converse implication: correlated components are not); correlated or
undetermined-correlation contributions require covariance treatment or, as the conservative
upper bound, linear summation —
[Ferrero et al. (2013)](https://consensus.app/papers/details/7e9026dcdac950939fe1660d88507f0a/?utm_source=claude_desktop),
[Warsza & Clarkson (2020)](https://consensus.app/papers/details/a1ba0bae4cdb51cba55e861e8149c1c0/?utm_source=claude_desktop).
Assuming independence when it is not established risks materially underestimating combined
uncertainty —
[Dixson et al. (2026)](https://consensus.app/papers/details/6a49d4b0e1d05ef09026393197f5a980/?utm_source=claude_desktop):
a model assuming consistency/independence understated total uncertainty "by as much as a
factor of five" versus one accounting for possible correlation.

**This project's own existing Mandated rules independently corroborate non-independence**:
`project.md` § Mandated already states Phase 2 is "not a second statistically independent
blind test" of Phase 1, and separately that the two phases carry a documented "geometry and
sampling artefact" overlap — facts already affirmed before this literature review, not
introduced by it.

**quadrature was rejected** because it requires an independence assumption this project's own
governing documents already contradict, and the domain literature gives no reason to think
Phase 1/Phase 2 VTEC uncertainty content escapes the shared-DCB pattern documented broadly
across GNSS-derived TEC products.

## Proposed D-number text (for the owner to adopt, with a real number)

> **D-6? `budget_value`: `statistic = p95`, `combination = sum` (§18.2 forbidden-choice item, GOV-2026-09-20-CG-01 Recommendation 20 / dispositions §4.5)**
>
> | Countersignature | Date | Rationale |
> |---|---|---|
> | *(owner fills — Student for `statistic`/`combination`; Supervisor for the independence judgment behind `combination`, per this item's original routing)* | *(owner fills)* | Sets both content fields of `configs/data.yaml: target.uncertainty_budget`: `statistic = p95` (forecast-verification, decision-relevant tail statistic, avoiding both `max`'s single-point fragility and `median`'s permissiveness for a budget concept — [Bouttier 2024](https://consensus.app/papers/details/571419dc7b7659b0900fef05315e3f8a/?utm_source=claude_desktop), [Brown et al. 2020](https://consensus.app/papers/details/b5c9557092ce5684b901f760cb3fb182/?utm_source=claude_desktop)) and `combination = sum` (correlated-component treatment, since Phase 1/Phase 2 VTEC uncertainty content share a documented common systematic error source — GNSS DCB estimation — [Chen 2026](https://consensus.app/papers/details/6dcc64144644599db0819d5b08e65c52/?utm_source=claude_desktop), [Zhang 2018/2023](https://consensus.app/papers/details/1cf7c2a93f8258aca2279d9174da756f/?utm_source=claude_desktop), [Hernández-Pajares 2017](https://consensus.app/papers/details/6c9fd1e894a65cfdb38649b8d071d4b6/?utm_source=claude_desktop) — corroborated by this project's own existing Mandated rules on non-independence of the two phases; general GUM practice reserves quadrature for established-independent components — [Fröhner 2003](https://consensus.app/papers/details/fab8b70c41ef56ccb17b990e1bcc47b1/?utm_source=claude_desktop), [Dixson 2026](https://consensus.app/papers/details/6a49d4b0e1d05ef09026393197f5a980/?utm_source=claude_desktop)). **Closes Recommendation 20 / the §18.2 item in full**: `decision`, `statistic` and `combination` are now all set in `configs/data.yaml: target.uncertainty_budget`, `resolve_budget_rule` returns a usable rule for the first time, and `practical_relevance_statement` stops refusing. Verified before this citation was written: `resolve_budget_rule` on the real config returned `None` with `decision` as the sole unset field — confirming this D-number's own citation is the last gap, not an assumption. |

## Verification performed 2026-09-24 (unchanged from the two prior drafts, re-confirmed together)

- `configs/data.yaml`: `statistic = "p95"`, `combination = "sum"`, `decision` still
  `"TBD — freeze gate"`.
- `resolve_budget_rule(real_config) is None` — confirmed by direct execution, both before and
  after this merge (no config change made by the merge itself).
- 250 passed, 1 skipped across every test module touching this code path
  (`test_prepared_target_schema.py`, `test_common_masks.py`, `test_regimes_and_reporting.py`),
  governed `tec-thesis-311` (Python 3.11.16) environment.

> ## ✅ RULED 2026-09-24 — D-67, written into `evidence/DECISIONS.md`
>
> Countersignature: Student — Approved by instruction, 2026-09-24, no separate supervisor
> signature claimed. `configs/data.yaml: target.uncertainty_budget.decision = "D-67"`.
> `resolve_budget_rule` on the real config now returns
> `{'decision': 'D-67', 'statistic': 'p95', 'combination': 'sum'}` — a usable rule for the
> first time. Recommendation 20 / the §18.2 item is closed in full.
