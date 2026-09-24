# Change record — 2026-09-24 — `budget_value.combination = sum` (draft D-number, partial freeze)

> **SUPERSEDED 2026-09-24** — merged with the sibling `statistic` draft into one D-number,
> since both set fields of the same §18.2 item: `governance/CHANGE_RECORD_2026-09-24_budget_value_merged.md`.
> Left standing rather than deleted, per this project's history-preserving convention.

**Purpose.** Draft only. Not written to `evidence/DECISIONS.md`. `configs/data.yaml`'s
`target.uncertainty_budget.combination` has been set to `"sum"`; `decision` stays
`"TBD — freeze gate"`. Combined with the earlier `statistic = p95` partial freeze
(`governance/CHANGE_RECORD_2026-09-24_budget_value_statistic.md`), **both content fields of
the §18.2 forbidden-choice item are now set** — only the citing D-number itself remains
unwritten, and `resolve_budget_rule` (re-verified 2026-09-24 against the real, edited config)
still correctly returns `None` for that reason alone.

## The question this resolves

Whether the Phase 1 (gridded, station-agnostic) and Phase 2 (station-based) target-uncertainty
contents that `budget_value` combines share a common systematic error source. If independent
→ quadrature (root-sum-square) is the standard GUM combination. If correlated/undetermined →
sum is the metrology-correct conservative treatment. Left open in the prior session pending
literature review; resolved here.

## Literature review (Consensus, 2026-09-24)

**Domain-specific: GNSS-derived TEC/VTEC products share a well-documented common systematic
error source — differential code bias (DCB) estimation — across processing levels and
products.**

- [Chen et al. (2026), "Investigating the Causes and Variations of Systematic Bias in MIT TEC Maps"](https://consensus.app/papers/details/6dcc64144644599db0819d5b08e65c52/?utm_source=claude_desktop): confirms *"the systematic bias in MIT TEC primarily stems from its DCB estimation strategy and choice of mapping function"* — a bias reaching up to 30 TECU at low latitude, present across multiple comparison references (radio occultation, other GIMs).
- [Zhang et al. (2018)](https://consensus.app/papers/details/1cf7c2a93f8258aca2279d9174da756f/?utm_source=claude_desktop) and [Zhang et al. (2023)](https://consensus.app/papers/details/806b64787d305afa94ae9059fb06e99c/?utm_source=claude_desktop) both show DCB estimation errors propagate directly and measurably into VTEC map accuracy across GPS/GLONASS-derived products.
- [Li et al. (2018)](https://consensus.app/papers/details/984c32a0c6e75c27929e93aae0c58b27/?utm_source=claude_desktop) and [Zha et al. (2019)](https://consensus.app/papers/details/bde9a7b2451752fabac64533c14c210d/?utm_source=claude_desktop) show receiver DCB variability (including short-term, temperature-correlated drift) impacts TEC retrieval at the multi-TECU level, and this variability is a property of the underlying GNSS processing chain, not of any one product's target definition.
- [Hernández-Pajares et al. (2017)](https://consensus.app/papers/details/6c9fd1e894a65cfdb38649b8d071d4b6/?utm_source=claude_desktop) directly report *significant correlation* between error metrics of two independently-computed VTEC assessment methods over the same physical ionosphere, exactly the shared-source pattern relevant here.

**General metrology: when correlation status is unknown or "indeterminate," assuming
independence risks materially underestimating combined uncertainty.**

- [Dixson et al. (2026), "Titanic overconfidence — dark uncertainty can sink hybrid metrology..."](https://consensus.app/papers/details/6a49d4b0e1d05ef09026393197f5a980/?utm_source=claude_desktop): directly on point. Comparing a model that assumes consistency/independence (underestimates total uncertainty "by as much as a factor of five") against one that accounts for possible correlation/inconsistency ("dark uncertainty"), the paper's explicit conclusion is to avoid "titanic overconfidence" by not assuming independence when it is not established.
- This generalizes the earlier session's GUM-literature finding ([Fröhner 2003](https://consensus.app/papers/details/fab8b70c41ef56ccb17b990e1bcc47b1/?utm_source=claude_desktop); [Ferrero et al. 2013](https://consensus.app/papers/details/7e9026dcdac950939fe1660d88507f0a/?utm_source=claude_desktop)): quadrature is only the *correct* combination for genuinely independent/uncorrelated components; correlated or undetermined-correlation components are combined by (linear) summation as the conservative, defensible upper bound.

**This project's own existing Mandated rules independently point the same direction.**
`project.md` § Mandated already states the two phases are *not* independent by construction:
*"Phase 2 is a fixed-protocol replication on a new target lineage, not a second statistically
independent blind test"*, and separately: *"Phase 1 compares a grid cell against a
station-coordinate evaluation, Phase 2 an IPP cloud against a zenith estimate, and part of any
measured difference is a geometry and sampling artefact rather than skill."* Both are existing,
already-affirmed project facts, not new claims introduced by this literature review — they
independently corroborate the domain literature's finding that Phase 1/Phase 2 content are not
cleanly separable, independent error sources.

## Decision

**`combination = sum`.** The convergence of domain-specific evidence (DCB is a documented,
pervasive shared systematic error source across GNSS-derived TEC products at every processing
level) and general metrology guidance (don't assume independence when it isn't established,
and correlated components are correctly summed, not combined in quadrature) both point the
same way, and this project's own existing Mandated rules already describe the two phases as
non-independent. Quadrature was rejected — it would require an independence assumption this
project's own governing documents already contradict.

## Proposed D-number text (for the owner to adopt, with a real number)

> **D-6? `budget_value.combination = sum` (partial freeze — combination only; `statistic` set
> separately, this decision's own citation remains open)**
>
> | Countersignature | Date | Rationale |
> |---|---|---|
> | *(owner fills — Supervisor, per the original independence judgment this item was routed for)* | *(owner fills)* | Sets `configs/data.yaml: target.uncertainty_budget.combination` to `sum`. **Literature and project basis**: GNSS-derived TEC/VTEC products share a documented common systematic error source (differential code bias estimation) across processing levels — [Chen et al. 2026](https://consensus.app/papers/details/6dcc64144644599db0819d5b08e65c52/?utm_source=claude_desktop), [Zhang et al. 2018/2023](https://consensus.app/papers/details/1cf7c2a93f8258aca2279d9174da756f/?utm_source=claude_desktop), [Li et al. 2018](https://consensus.app/papers/details/984c32a0c6e75c27929e93aae0c58b27/?utm_source=claude_desktop), [Hernández-Pajares et al. 2017](https://consensus.app/papers/details/6c9fd1e894a65cfdb38649b8d071d4b6/?utm_source=claude_desktop). General metrology practice treats correlated or undetermined-correlation uncertainty components with (conservative) linear summation, not quadrature, which is reserved for genuinely independent components — [Fröhner 2003](https://consensus.app/papers/details/fab8b70c41ef56ccb17b990e1bcc47b1/?utm_source=claude_desktop), [Ferrero et al. 2013](https://consensus.app/papers/details/7e9026dcdac950939fe1660d88507f0a/?utm_source=claude_desktop); assuming independence without establishing it risks materially underestimating combined uncertainty — [Dixson et al. 2026](https://consensus.app/papers/details/6a49d4b0e1d05ef09026393197f5a980/?utm_source=claude_desktop). This project's own existing Mandated rules already describe Phase 1 and Phase 2 as non-independent (`project.md`: Phase 2 is "not a second statistically independent blind test"; the two phases carry a documented "geometry and sampling artefact" overlap) — the literature review corroborates rather than introduces this position. **Combined with the separate `statistic = p95` freeze, both content fields of the §18.2 item are now set; only this D-number's own citation, written into `configs/data.yaml: target.uncertainty_budget.decision`, remains to fully discharge Recommendation 20.** Verified 2026-09-24: `resolve_budget_rule` still correctly returns `None` on the real config, because `decision` remains `TBD — freeze gate` — `budget_value` stays `None` and `practical_relevance_statement` continues to refuse honestly until this D-number is actually assigned and cited. |

## Verification performed 2026-09-24

- `configs/data.yaml` diff: `combination: "TBD — freeze gate"` → `combination: "sum"`.
  `decision` unchanged, still `"TBD — freeze gate"`.
- `"sum"` confirmed a member of `BUDGET_COMBINATIONS` (`src/data/prepared.py`) — no code
  change needed for the value itself.
- Directly verified against the real, edited config: `resolve_budget_rule(real_config) is None`
  — confirmed by execution. Both content fields (`statistic`, `combination`) are now set and
  the rule still correctly refuses, because `decision` is the remaining gate.
- Test suite: 250 passed, 1 skipped across every module touching this code path
  (`test_prepared_target_schema.py`, `test_common_masks.py`, `test_regimes_and_reporting.py`),
  under the governed `tec-thesis-311` (Python 3.11.16) environment.

**Decision required — Approve / Reject / Modify / Postpone**, on the `combination` value
itself, and — since both content fields are now set — whether to write ONE combined D-number
covering both `statistic` and `combination` together (recommended, since they're one §18.2
item) rather than two separate ones.
