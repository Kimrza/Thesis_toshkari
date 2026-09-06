# Code Summary — `target-standardization`

**Unit** `target-standardization` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`
**Plan**: `code-generation-plan.md` — all 7 steps executed, checkboxes marked. No `git commit` (governance stop). **No standardized target artifact exists** — Q2=A's refuse-to-RUN is the deliverable; production waits on the supervisor's `qc_operations` freeze under a D-number. `configs/data.yaml` untouched.

## Files created

| Path | What |
|---|---|
| `src/data/prepared.py` | The standardization engine (stdlib + approved packages only): `assert_qc_operations_frozen` FIRST statement of `standardize_hourly_target` (raise names `configs/data.yaml qc_operations` + "frozen under a D-number… never mere non-emptiness" — a non-empty list without a D-number citation also refuses); `PERMITTED_TRANSFORMATIONS` exactly four (fifth fails AND missing member fails); D-16 statistic resolves from config requiring `statistic == "median"` AND `decision == "D-16"` (absent → refused, non-median fails); two-layer D-17 contract (`assert_d17_config_matches` — "the CONFIG drifted" — vs `assert_row_conforms` — "the ROW is wrong"); excluded set asserted by set-equality, never adopted; `lineage_caveat` COLUMN on every row (SD-T-02's two disclosures + no-numerical-equivalence statement; detectability, not survival, is what is claimed); D-19 threshold VALUES/basis/`basis_window`/`decision` all config-read (missing basis fails; December-referencing basis fails); data-quality block (four contents; unexplained kept unexplained); uncertainty budget states bounds; `load_released_provider_rows` consumes releases via `verify_release` + per-file re-hash |
| `scripts/02_standardize_prepared_target.py` | Position 02, `--config configs/`, `--phase choices=(1,)` — no `02a`/`02b`; six-step entry (`ensure_process_determinism` first; `assert_phase_boundary`; `assert_no_raw_fields` before first write); registry rows via foundation's writer; honest `aborted` row on the QC refusal |
| `scripts/03_verify_processing.py` | Phase 1 scope; value-level closed-set diff (schema-level insufficient); `--fixture-manifest` supplies the TE §15.2 tolerance — unset → stop naming the field, never a `numpy.isclose` default; the four Phase-2 uncertainty contents recorded not-applicable; evidence carries the three IDs + label + caveat |
| `tests/test_prepared_target_schema.py` | Tree-named per `CR-2026-08-22-TARGET-SCHEMA-TEST`; **62 tests** — every plan-named negative control (fifth transformation; non-D-16 statistic; 15/17-field failures both directions; missing ID; caveat absent/altered; round-trip preservation; substituted excluded set; QC-TBD refusal naming field + expectation; receiver-specific label refused; D-19 basis controls; tolerance-unset stop; script-identity checks) |

## Files modified in place

| Path | What |
|---|---|
| `src/data/config.py` | Q1=A: `StandardizationError` (IntegrityError subclass, `__all__`, any-future clause); minimal `("target-standardization", 1): ("seeds.development",)` in `REQUIRED_FIELDS_MAP` with a comment recording why `data.qc_operations` is NOT listed (its enforcement point is the target-producing run; a blanket preflight entry would bar the refusal path that is the deliverable) |

## Test and lint results (smoke evidence only — never governed)

- **Full suite: 726 passed, 2 skipped, 0 failed** — Python 3.11.9; **re-run independently by the orchestrating session, same counts** (+62 over the 664 baseline, exactly the new module). Both skips pre-existing — one of them (`test_phase_boundary.py:247`) skips precisely because no target exists, as Q2=A requires.
- `ruff check`: all checks passed on the five touched files; three new files format-clean (`config.py` left unformatted — repository baseline).

## Key decisions

1. **Verification refuses identically**: `verify_value_level` recomputes through the same engine, so the QC gate binds both scripts (tested).
2. **Caveat column vs R-66's "an additional field fails"**: `lineage_caveat` treated as the NFR-TDEF-01 declared companion (nfr-design Q1=A postdates R-66); any OTHER extra field still fails. Stated in the docstring; **flagged for the gate**.
3. **Exception scope kept to the receipted ruling**: `domain-entities.md` §9's `SchemaError`/`TargetQualityError`/`BudgetError` are NOT separately raised/declared — those conditions raise `StandardizationError` with the config-vs-row distinction carried in messages. **Routed to the gate** (widening a ruling to items the owner was not shown is the corrected failure).
4. **Budget content labels** derived from D-17's own uncertainty-bearing fields (provider `dtec` summary; within-hour spread) — labels from the product, not new scientific values.
5. The grep-class prohibited-phrasing check skips strings exactly equal to the caveat constant (it quotes the prohibition in negation) — documented in code.

## Deviations

- Script 03's `--fixture-manifest` flag beyond §13.2's fixed pair — precedented (script 01's flags); the tolerance must come from the fixture manifest by design.
- `REQUIRED_FIELDS_MAP` entry (minimal; recorded, not silent).
- graphify CLI unavailable — graph stale for touched files; `graphify update .` owed.

## Governance stop — owed before any commit (student acts; cumulative)

- Gate items restated (none decided): the **D-17 authority question** (assert against the authority, not only the config — R-20's shape); foundation's run-manifest **executed-scripts** field (owed for fixtures-and-reproducibility's one-`02` assertion); the **consumer half of the caveat contract**; `unit-of-work.md` §5's stale "19" (annotate-in-place decision); the **exception-scope deviation** (decision 3) and the **caveat/R-66 reconciliation** (decision 2) proposed for explicit acknowledgment.
- **New gate-worthy observation from this pass**: `tests/test_phase_boundary.py:95`'s `D17_TARGET_FIELDS` carries **17** names including `processor_qc_flags`, against D-17's enumerated **16** (re-derived from `evidence/DECISIONS.md` this pass). Its conformance test currently skips (no artifact exists), so no runtime conflict — but the day a target is produced, a 16+caveat artifact would fail that 17-field set. Not edited (outside this plan); **a reconciliation ruling is owed before any target-producing run**.
- Commit cites **D-16, D-17, D-19, D-1** as touched context. **No governed commit before the records exist.**
- Nothing discharged: TA-19 stays `Pending`; FR-P1-03-5 stays rowless; FR-P1-03-1 stays BLOCKED; BLK-05's execution limb remains open (module exists, smoke-run only).

## Review — 2026-09-06 (code-generation, iteration 1)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T21:23:39Z
**Iteration:** 1

### Findings

| # | Severity | Where | What | Recommended action |
|---|---|---|---|---|
| 1 | Minor | `configs/data.yaml` | The file's own header assigns transcription of "target contract, support thresholds" to this unit's Bolt, and the sibling `stations`/`cell_rule` keys (owned by `inventory-and-registry`) were stubbed with the `TBD — freeze gate` sentinel — but `qc_operations`, `target.aggregation`, `target.contract`, `target.support_thresholds` and `target.identity` are entirely absent from `data.yaml` rather than stubbed. Functionally harmless today (`assert_qc_operations_frozen` and the four `resolve_*`/`assert_d17_config_matches` functions treat "absent" and "TBD" identically, and `REQUIRED_FIELDS_MAP`'s minimal entry deliberately excludes `qc_operations` from preflight), but it breaks the established convention that an owning unit's Bolt stubs its own unfrozen fields as sentinels rather than omitting the keys outright, leaving no scaffold in the governed config for the supervisor to fill at freeze time. | Add `qc_operations: "TBD — freeze gate"` and stub `target.aggregation` / `target.contract` / `target.support_thresholds` / `target.identity` nodes (each field `TBD — freeze gate`) to `configs/data.yaml`, matching the `stations`/`cell_rule` precedent, or explicitly record in this unit's plan why stubbing was intentionally deferred. |
| 2 | Minor | `tests/test_phase_boundary.py:95` (not owned by this unit) | `D17_TARGET_FIELDS` there enumerates 17 names (including `processor_qc_flags`) against D-17's frozen 16 (independently re-derived from `evidence/DECISIONS.md` D-17's field table: 16 named rows, `processor_qc_flags` is a data-quality-block content, never a row field). Confirmed real and correctly *not* silently edited by this unit (the file belongs to another unit); correctly routed to the governance stop as owed before any target-producing run, since a produced 16+caveat artifact would fail that assertion's `missing` check the day a target exists. | No action needed from this unit; keep the reconciliation ruling on the gate list as already recorded. |

### Verified and held (adversarial checks that survived)

- **Q2=A gate is genuinely unbypassable before any write in both scripts.** `assert_qc_operations_frozen` is the first statement of `standardize_hourly_target` (prepared.py:967) and is called in script 02's `_run_standardize` (line 267) before `load_released_provider_rows` and before any output path is touched; script 03 checks target-artifact existence first and its `verify_value_level` recomputation re-invokes the same gate. Live-executed: a non-empty `qc_operations.operations` list *without* a D-number `decision` citation is refused, not accepted (confirmed by direct call).
- **`configs/data.yaml` is genuinely untouched by this unit's own work**: git shows it fully untracked (`??`) with no history at all — consistent with "before the first commit" governance stance — and its content carries no `qc_operations`/`target.*` keys at all (see Finding 1), confirming no scientific value was inlined or silently adopted.
- **Closed transformation set**: live-executed — a fifth transformation fails, a missing permitted member fails, a non-D-16 statistic is refused by `resolve_aggregation_statistic`.
- **Excluded-set token/compound detection**: live-executed against `stec_mean`, `dcb_applied`, `sat_count`, `n_sat_valid`, `zen_wt` — all caught; `station_id`/`vtec_tecu` correctly pass through (no false positive).
- **D-17's sixteen-field enumeration**: independently re-derived from `evidence/DECISIONS.md` D-17's field table (16 named rows: `interval_start_utc`, `station_id`, `cell_gdlat`, `cell_glon`, `cell_lat_bounds`, `cell_lon_bounds`, `vtec_tecu`, `valid_observation_count`, `within_hour_spread_tecu`, `largest_internal_gap_s`, `provider_dtec_summary`, `aggregation_config_id`, `target_valid`, `phase_id`, `source_id`, `target_definition_id`) — matches `D17_FIELDS` in `prepared.py` exactly, same order.
- **No scientific value inlined as a literal**: D-16/D-17/D-19 thresholds, statistics and identities are all read from `data_config`/`target.*` paths with citation checks; module constants carry only identities (field names, statistic names, decision-citation strings), never numeric thresholds.
- **Caveat column**: `LINEAGE_CAVEAT_TEXT` is a single fixed constant emitted on every row and every JSON artifact envelope by the unit's own write paths (`write_target_rows_csv`, `write_json_artifact`); `assert_row_conforms` fails a row whose caveat is absent or altered; the grep-class `assert_no_prohibited_phrasing` correctly skips the caveat constant itself (it quotes the prohibited phrasing in negation) while still catching the phrasing elsewhere; only detectability through this unit's own write path is claimed, not survival — matches SD-T-02's corrected scope.
- **Verification is value-level, not schema-level**: `verify_value_level` recomputes the full target through the same engine and diffs every float/exact field against tolerance; tolerance is exclusively sourced from `--fixture-manifest` via `resolve_float_tolerance`/`_load_tolerance`, which stop naming the TE §15.2 field when unset — no `numpy.isclose`-style default found anywhere in the two new scripts or `prepared.py`.
- **Phase discipline**: script 02/03 both assert `--phase choices=(1,)`; no `02a`/`02b` file exists; `assert_phase_boundary`/`assert_no_raw_fields` run before any write in both scripts; no DCB/STEC/mapping/satellite/arc-shaped field appears in either script's `PRODUCED_FIELDS` tuple.
- **Scope/authority honesty**: `StandardizationError` is the only new exception declared in `config.py`, correctly positioned as riding R-01's any-future clause and not an enumeration entry; `SchemaError`/`TargetQualityError`/`BudgetError` from `domain-entities.md` §9 are confirmed *not* declared, with the deviation stated in code-summary decision 3 and routed to the gate rather than silently absorbed; `REQUIRED_FIELDS_MAP`'s new `("target-standardization", 1)` entry is minimal (`seeds.development` only) with `qc_operations` deliberately excluded and the reason recorded in-line.
- **Claim honesty / plan vs. disk**: all 7 plan steps' claimed work exists on disk; no `hourly_target*.csv` or other standardized-target artifact exists anywhere in the workspace (confirmed via the `test_phase_boundary.py` skip and no matching file found); nothing in `unit-of-work.md`/acceptance rows is claimed discharged.
- **Suite/lint integrity, independently re-run**: full suite collected 728 tests (per-file `-q` collect-only counts sum to 728: 47+29+62+35+49+51+6+19+36+6+53+36+62+32+149+27+29), executed with exit code 0 and exactly 2 skips (`test_phase_boundary.py:247`, `test_release_contract.py:139` — both pre-existing, matching the claimed reasons verbatim); the new module (`tests/test_prepared_target_schema.py`) collects exactly 62 tests as claimed, giving 726 passed + 2 skipped = 728, matching the claim precisely. `ruff check` on all five touched files: all checks passed, matching the claim.

### Coverage limits

This pass verified the unit's own artifacts, the passed functional-design/nfr-design/units-generation contracts, `evidence/DECISIONS.md` D-16/D-17/D-19, and the single sibling file (`tests/test_phase_boundary.py`) that this unit's own artifacts named as an integration point (per the spot-check carve-out). No other sibling unit's construction directory was read.

### Summary

The code matches its receipted Q1/Q2 answers and its plan precisely: the refuse-to-RUN gate fires before any output path in both scripts and cannot be bypassed by a convenience non-empty list; the closed four-transformation set, the D-17 sixteen-field contract (independently re-derived and confirmed correct against a stale 17-field sibling test), the asserted-never-substituted excluded set, and the value-level verification with a fixture-manifest-only tolerance are all implemented as designed and hold under adversarial probing; the test-suite and lint claims are independently reproduced exactly. The only two findings are Minor: an inconsistency in whether unfrozen config keys should be stubbed as `TBD` sentinels versus omitted outright (harmless today, a convention gap), and a pre-existing sibling-file discrepancy this unit correctly did not touch and correctly routed to the gate. Neither blocks READY under this project's verdict rule.
