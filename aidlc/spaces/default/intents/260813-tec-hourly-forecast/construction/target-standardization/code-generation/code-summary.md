# Code Summary — `target-standardization`

**Unit** `target-standardization` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`
**Plan**: `code-generation-plan.md` — all 7 steps executed, checkboxes marked. **No standardized target artifact exists** — Q2=A's refuse-to-RUN is the deliverable; production waits on the supervisor's `qc_operations` freeze under a D-number. `configs/data.yaml` untouched.

**Repository state, re-derived 2026-09-13 at HEAD `1670ac8`.** This header previously read
"No `git commit` (governance stop)", and § "Governance stop" carried the parallel claim "No
governed commit before the records exist". **Both are false as statements about the current
repository** — flagged as a Major on 2026-09-11 — and are corrected here in the body rather
than in a review addendum, per `project.md` (`code-generation:fr-2`). This unit's five files
(plus the four `configs/`) were introduced in **`ed5808b`**, whose message is the unedited
git placeholder and cites none of D-16/D-17/D-19/D-1;
`scripts/02_standardize_prepared_target.py` was further modified in **`cf3185d`** and
**`0e002cd`**, neither citing a D-number either (`0e002cd`'s subject line at least names
"board remediation"). `team.md` § Way of Working makes the D-number citation mandatory for
any commit touching a governed artifact. Per `project.md`'s never-edit-a-signed-record rule
and `c30`, **no amend, revert or re-commit was made** — the discrepancy is stated and the
remediation choice (amend; a follow-up commit citing the D-numbers; or an explicit owner
waiver) is routed to the gate as part of the standing commit-message ruling.

**D-17 field-contract reconciliation — CLOSED 2026-09-13.** This unit carried, across four
consecutive passes, a correctly-scoped Minor that `tests/test_phase_boundary.py:95`'s
`D17_TARGET_FIELDS` enumerated **17** names (the extra being `processor_qc_flags`) against
D-17's frozen **16**, correctly declining to edit a sibling's file and routing a
reconciliation ruling as owed before any target-producing run. The owner ruled on
2026-09-13 (**Option 4**): D-17's sixteen are authoritative, `processor_qc_flags` is a
data-quality-block key (R-71/NFR-DQ-01, W-3) and not a row field, **and** the same test was
stale a second way this unit had not detected — its assertion is a set equality in both
directions, so `extra` would equally have flagged `lineage_caveat`, which the producer
emits by contract (`src/data/prepared.py:1324`) and its own row guard permits (`:791`).
Both limbs were repaired in `governance-guards`' modules (that unit owns them), along with
a drift guard pinning `D17_TARGET_FIELDS` against `prepared.D17_FIELDS`. **No file owned by
this unit changed**, and this unit's own `D17_FIELDS` (16) was already correct.

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

## Governance stop — owed at the gate (student acts; cumulative)

> **Heading and bullets corrected 2026-09-13** after the re-review returned a Critical. This
> section was headed "owed **before any commit**" and its commit bullet read "**No governed
> commit before the records exist**" — a second representation of the same false claim the
> header above had just corrected, left standing three lines below it. That is precisely the
> sweep failure `project.md` (`fd-2026-08-30-sweep-derive-sites`) names, reproduced inside
> the repair meant to close it. The commits already exist (`ed5808b`, `cf3185d`, `0e002cd`);
> what is owed is no longer "commit only after the records" but the remediation choice on
> commits already made without their D-number citations.

- Gate items restated (none decided): the **D-17 authority question** (assert against the authority, not only the config — R-20's shape); foundation's run-manifest **executed-scripts** field (owed for fixtures-and-reproducibility's one-`02` assertion); the **consumer half of the caveat contract**; `unit-of-work.md` §5's stale "19" (annotate-in-place decision); the **exception-scope deviation** (decision 3) and the **caveat/R-66 reconciliation** (decision 2) proposed for explicit acknowledgment.
- ~~**New gate-worthy observation from this pass**: `tests/test_phase_boundary.py:95`'s `D17_TARGET_FIELDS` carries **17** names including `processor_qc_flags`, against D-17's enumerated **16** (re-derived from `evidence/DECISIONS.md` this pass). Its conformance test currently skips (no artifact exists), so no runtime conflict — but the day a target is produced, a 16+caveat artifact would fail that 17-field set. Not edited (outside this plan); **a reconciliation ruling is owed before any target-producing run**.~~ **CLOSED 2026-09-13 by the owner's Option 4 ruling** — see the D-17 paragraph in the header. The ruling also found the second stale limb this unit had not detected (`extra` would equally have flagged `lineage_caveat`); both were repaired in `governance-guards`' modules, and `D17_TARGET_FIELDS` now enumerates 16. The original text is struck rather than deleted, as the record of what this unit correctly raised across four passes.
- **The commits exist and cite none of D-16, D-17, D-19, D-1** — `ed5808b` (unedited git placeholder message), `cf3185d` (same), `0e002cd` (a real subject line naming "board remediation", but no D-number). Re-derived 2026-09-13. The owed act is therefore the **remediation choice on commits already made** — amend, a follow-up commit citing the four decisions, or an explicit recorded waiver — not the "no governed commit before the records exist" precondition this bullet previously asserted, which was already false when written.
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

### Cross-unit edit record (2026-09-10) — edits made by `fixtures-and-reproducibility`, owner-authorised

Appended after the gate rejection lifted the receipt freeze. Under
`CR-2026-09-07-R133-FIXTURES-AND-REPRODUCIBILITY` (§5, §6.1, §11.1, §11.5; the owner's
"apply the recommended option" ruling), the fixtures unit made these ADDITIVE edits to this
unit's scripts — nothing on the full-year path changed:

- `scripts/02_standardize_prepared_target.py` (commit `cf3185d`): `--fixture-manifest`
  option (the visible Q5 = A exemption carrier), `_stage_entry(..., fixture_manifest=None)`
  kwarg, and ONE `require_receipts_for_snapshot` call after `assert_lock_complete`
  (TE §9.2's two-receipt gate; exempt on a fixture run).
- `scripts/02_standardize_prepared_target.py` (commit `0e002cd`, board Rec 2 / ML-01):
  `_declared_data_window` (the standardizer consumes acquisition's retrieved product, so
  its declared window IS `acquisition.window_start`/`window_end` in `configs/data.yaml`;
  undeclared → the fixture exemption refuses, TE §18.3).
- `scripts/03_verify_processing.py` (commit `cf3185d`): `_load_tolerance`'s direct
  `yaml.safe_load` of a fixture manifest was REROUTED through the one validating loader
  (`src.data.fixture_manifest.load_fixture_scope`, R-133) — the second-parser case
  R-133 control 4's project-wide only-copy scan exists to refuse; behaviour strictly
  narrows (an invalid manifest now refuses at the loader instead of being parsed loosely
  for one field). Current sizes, derived: `02` 428 lines, `03` 386 lines (`wc -l`).

Tests live in `tests/test_clean_run.py` (`test_rec2_02_...`, `test_control_4_only_copy_...`).
This unit's owner may confirm or reverse per the change record.

## Review — 2026-09-10 (code-generation, gate-floor re-review, iteration 2)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-10T14:19:48Z
**Iteration:** 2 (fresh review against current state; the earlier READY was reset by a
gate rejection unrelated to this unit's own artifacts, per the dispatch brief)

### Scope of this pass

Re-derived from scratch against HEAD `f0d9e49` plus the uncommitted sibling
`acquisition` repair (`_guard_free_text_egress` in `src/data/experiment_registry.py`,
new controls in `tests/test_acquisition.py`/`tests/test_clean_run.py`). Confirmed this
unit's own files (`src/data/prepared.py`, `scripts/02_standardize_prepared_target.py`,
`scripts/03_verify_processing.py`, `tests/test_prepared_target_schema.py`,
`src/data/config.py`) carry **no uncommitted changes** (`git status --porcelain` shows
only `acquisition`/`governance-guards`/`inventory-and-registry` code-summaries and the
acquisition-unit source/tests as dirty) — this unit's own work is exactly the
already-committed state the prior review examined, plus the owner-authorised
cross-unit edits already disclosed in the "Cross-unit edit record" section above.

### Findings

None new. The two Minor findings from the 2026-09-05 review (unstubbed
`qc_operations`/`target.*` keys in `configs/data.yaml`; the stale 17-field
`D17_TARGET_FIELDS` in the sibling `tests/test_phase_boundary.py:95`) are **unresolved,
still present, and correctly not this unit's to fix** — re-verified below.

| # | Severity | Where | Status |
|---|---|---|---|
| 1 | Minor | `configs/data.yaml` | Still absent (confirmed by direct grep: no `qc_operations`/`target.*` key anywhere in the file even after the D-33/D-38 additions of `cell_rule`/`partitions`/`embargo_hours`). Harmless — `assert_qc_operations_frozen` treats absent and TBD identically and still refuses correctly (live-executed below). Carried forward, not blocking. |
| 2 | Minor | `tests/test_phase_boundary.py:95` (sibling file, not owned by this unit) | Still 17 fields (`processor_qc_flags` extra) against D-17's frozen 16; independently re-derived from `evidence/DECISIONS.md` D-17's field table this pass (16 rows counted: `interval_start_utc, station_id, cell_gdlat, cell_glon, cell_lat_bounds, cell_lon_bounds, vtec_tecu, valid_observation_count, within_hour_spread_tecu, largest_internal_gap_s, provider_dtec_summary, aggregation_config_id, target_valid, phase_id, source_id, target_definition_id`). Still routed to the gate as owed before any target-producing run; correctly not touched by this unit. |

### Adversarial checks run this pass, with evidence

- **`scripts/03_verify_processing.py`'s `_load_tolerance` reroute (the brief's named
  hardest-attack surface) does strictly narrow, verified directly, not just read.**
  Diffed the pre-reroute version (`ed5808b:scripts/03_verify_processing.py`) against
  HEAD: the old path was `yaml.safe_load(text)` → `isinstance(..., Mapping)` check →
  `resolve_float_tolerance(loaded)` directly on the raw parsed dict — i.e. it accepted
  *any* mapping carrying `permitted_floating_point_tolerances.value_level_diff_tecu`,
  full TE §15.2 manifest or not. The new path calls
  `src.data.fixture_manifest.load_fixture_scope`, which (read directly,
  `fixture_manifest.py:1750-1772`) dispatches to either `load_fixture_manifest` (full
  12-content-area TE §15.2 validation) or `load_identity_declaration`
  (`kind == "identity_declaration"`), **both fully validating**, and only then hands
  `resolve_float_tolerance` the *same* `scope.data` raw mapping the old code used
  (`FixtureManifest.data`/`IdentityDeclaration.data` are the unmodified parsed dict,
  confirmed at `fixture_manifest.py:410,1621`). So the new accept-set (full manifest ∧
  tolerance-key resolves) is a strict subset of the old accept-set (any-mapping ∧
  tolerance-key resolves) — nothing the old code accepted and the new code rejects
  fails to also be structurally invalid by TE §15.2, and nothing the new code accepts
  was rejected by the old code. Exception-type check: old code raised only
  `StandardizationError`; new code can raise `IntegrityError` (from the loader) or
  `StandardizationError` (from `resolve_float_tolerance`) — both are caught by the
  same `except IntegrityError` at `scripts/03_verify_processing.py:359`, confirmed
  live: `StandardizationError` is declared as an `IntegrityError` subclass in
  `src/data/config.py` (code-summary decision 1), so no caller-visible behavior change
  from the exception-type widening. **No widening found.**
- **Script 03 confirmed Phase-1-only and unreachable from Phase 1's own boundary
  rule**: `--phase` has `choices=(1,)` (`scripts/03_verify_processing.py:158`),
  matching script 02 (`scripts/02_standardize_prepared_target.py:176`); no `03a`/`03b`
  variant file exists.
- **Q2=A refuse-to-RUN gate live-executed this pass, not merely re-read**, against
  three probes built from the current `assert_qc_operations_frozen` signature:
  absent `qc_operations` key (matches the current `configs/data.yaml` state exactly)
  → refuses naming the field and "FROZEN UNDER A D-NUMBER... never mere
  non-emptiness"; a non-empty operations list without a `decision` D-number citation →
  refuses identically (the convenience-fill bypass attempt fails); a list *with* a
  D-number citation → passes. All three matched the documented contract exactly.
- **D-5 (never impute/interpolate/fill) verified by direct search**: no
  `interpolate`/`fillna`/`ffill`/`bfill`/`impute` call anywhere in `prepared.py` or
  scripts 02/03 — the only matches are the docstring/comment sentences stating the
  prohibition, not code that violates it.
- **D-17's 16-field contract and the 8-class excluded set independently re-derived
  from `evidence/DECISIONS.md` this pass** (not carried from the prior review's
  count): both match `prepared.py`'s `D17_FIELDS` and `DECLARED_EXCLUDED_SET` exactly,
  same order, same count.
- **Location-sampled gridded VTEC labeling verified**: `TARGET_LABEL =
  "location-sampled gridded VTEC"`, `_PROHIBITED_FRAGMENTS = ("station-observed",
  "receiver-specific")`, and `target_definition_id` stamped on every row
  (`prepared.py:136-153,653,1383`) — the mislabeling this project forbids does not
  occur.
- **No TBD sentinel filled by this unit, no scientific constant hardcoded, no
  credential/secret** — grepped `prepared.py` and both scripts: every `TBD_SENTINEL`
  reference is refusal logic (raises on encountering the literal), not a fill; no
  `api_key`/`secret`/`password`/token-literal pattern found.
- **Sibling `acquisition` repair's blast radius on this unit, checked directly (this
  unit imports `guard_egress` from `src/data/acquisition.py` and
  `append_registry_event`/`record_abort_honestly` from
  `src/data/experiment_registry.py`)**: `git diff --stat` confirms the repair is
  additive (168 insertions, 8 deletions across the two files); `guard_egress` still
  exists unchanged at `acquisition.py:480`; `append_registry_event`/
  `record_abort_honestly` still exist unchanged in `experiment_registry.py`. The new
  `_guard_free_text_egress` now routes `notes`/`reason` through
  `guard_egress_free_text` before every registry append — **live-tested against this
  unit's actual message strings** (script 03's fixed `notes` text, a real
  `StandardizationError` string, the QC-refusal message, a Windows file-path
  `IntegrityError` string): none triggered a false-positive `CredentialEgressError`.
  No regression to this unit's registry-write path.
- **`code-summary.md` line-count claims re-verified against disk, printed before
  asserting**: `wc -l scripts/02_standardize_prepared_target.py
  scripts/03_verify_processing.py` → 428 / 386, exactly matching both this document's
  own claim and the cross-unit edit record's claim.
- **Test counts independently re-executed** with a purpose-built stand-in runner
  (real pytest/pyyaml unreachable — PyPI blocked, verified again this pass; CPython
  3.11.16 via the scratchpad venv) that expands `@pytest.mark.parametrize` cases
  (the shipped stand-in shim no-ops parametrize, which would have undercounted):
  `tests/test_prepared_target_schema.py` → **62 passed, 0 failed, 0 errored**,
  matching the claimed 62 exactly; `tests/test_phase_boundary.py` → **52 passed, 0
  failed, 1 skipped** (the skip is `test_target_artifact_conforms_to_d17_when_it_exists`
  at line 247, matching the claimed pre-existing skip reason verbatim: no target
  artifact exists). Combined: 114 passed, 0 failed, 1 skipped, 0 errored across both
  files — no regression.

### Repo-wide config changes checked for spillover into this unit

- `configs/data.yaml`'s new `cell_rule` (D-33, supervisor countersignature not yet
  given) and `partitions` (D-38) blocks, and `configs/experiment.yaml`'s new
  `embargo_hours` (D-38): none of these keys are read by `prepared.py` or scripts
  02/03 (grepped; the standardization engine reads only `qc_operations`, `target.*`,
  and the D-16/D-17/D-19 paths, none of which changed). `stations` and
  `practical_relevance_threshold` remain `TBD — freeze gate`, correctly unread here.
  No TBD was silently resolved by this unit's code path as a side effect of the
  sibling transcriptions.

### Coverage limits (unchanged from iteration 1, restated)

This pass verified the unit's own artifacts, the passed functional-design/nfr-design/
units-generation contracts, `evidence/DECISIONS.md` D-16/D-17/D-19, `configs/data.yaml`
and `configs/experiment.yaml`, `governance/CHANGE_RECORD_2026-09-07_R133_...md` §11.5
(the reroute's own change record), and the single sibling files this unit's own
artifacts or the dispatch brief named as integration points
(`tests/test_phase_boundary.py`, `src/data/acquisition.py`,
`src/data/experiment_registry.py`) — resolved to their owning locations rather than
browsed. No other sibling unit's construction directory was read.

### Summary

Nothing has regressed and nothing new was silently introduced: this unit's own five
files are byte-identical to the already-reviewed committed state: the sibling
`acquisition` repair touches only files this unit imports from, additively, and its
new credential-egress guard was live-tested against this unit's actual log strings
without a false-positive refusal. The specific attack the brief named hardest — the
`03_verify_processing.py` tolerance-loader reroute — was verified directly against the
pre-reroute git history rather than taken on the change record's word, and the
strictly-narrows claim holds: the new accept-set is a proper subset of the old one, and
the exception-type change is absorbed by an existing subclass relationship with no
caller-visible effect. The Q2=A gate was re-executed live against three probes and
discriminates absent/unfrozen/frozen states exactly as designed. Both named test files
were independently re-run with parametrize expansion and match the claimed counts
exactly, with zero failures. The two Minor findings from the prior review are
confirmed still present, still correctly unfixed by this unit (one belongs to a
sibling file, one is a disclosed convention gap with no functional effect), and
neither individually nor together rises to blocking under this project's verdict
rule. READY stands on independent re-derivation, not on re-reading the prior verdict.

## Floor-reset re-review (2026-09-11)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-11T00:00:00Z (see repo evidence below for exact commands/output; wall-clock
date taken from session context, not machine-derived)
**Iteration:** 3 (fresh re-derivation against HEAD `b0b7c1d`, per this floor-reset dispatch;
prior verdicts not rubber-stamped)

### Scope of this pass

This unit's own five files (`src/data/prepared.py`, `scripts/02_standardize_prepared_target.py`,
`scripts/03_verify_processing.py`, `tests/test_prepared_target_schema.py`,
`src/data/config.py`) are confirmed **byte-identical** to the state iteration 2 reviewed:
`git status --porcelain` against all five returns nothing, and `git log f0d9e49..HEAD` for
those paths returns zero commits. The repo-wide uncommitted diff at HEAD touches only
`tests/test_locked_test_guard.py` (+362/-4) and four sibling units' code-summaries plus
`evidence/test_run_access_log.jsonl` — none imported by or referenced from this unit's code
(grepped `tests/test_locked_test_guard.py` for `prepared`/`target_standard`/`02_standardize`/
`03_verify`: zero matches). D-33..D-38 (repo-wide context) touch no key this unit's code
reads (`qc_operations`, `target.*`, D-16/D-17/D-19 paths unchanged; `stations`,
`practical_relevance_threshold` still `TBD` and unread here) — re-confirmed by grep, not
carried from the prior review's claim.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `code-summary.md:4` vs. git history | The artifact's headline claim — "No `git commit` (governance stop)" — is **false as a statement about the current repository**, and self-contradicts the same document's own iteration-2 text ("this unit's own work is exactly the already-committed state," line ~127). `git log --oneline -1 -- src/data/prepared.py` → `ed5808b`; this unit's five files (plus `configs/data.yaml`/`experiment.yaml`/`features.yaml`/`seeds.yaml`) were introduced in commit `ed5808b`, whose message is the unedited git placeholder ("Please enter the commit message for your changes...") — not a real message, and it cites none of D-16/D-17/D-19/D-1. `scripts/02_standardize_prepared_target.py` was further modified in `cf3185d` and `0e002cd`, neither of which cites a D-number either, though `0e002cd`'s subject line at least names "board remediation." This is exactly the failure class `project.md` corrections c30/gf-1 exist to catch (re-verify commit state before asserting a claim about it) — the commit didn't just happen, it happened three times without the D-number citation team.md's Way of Working makes mandatory ("Any commit that changes a scientific constant, a config value..., or another governed artifact must cite its D-number in the commit message"). | Correct line 4 (and the parallel claim at line 44, "No governed commit before the records exist") to state the actual fact: this unit's code IS committed (`ed5808b`, further touched by `cf3185d`/`0e002cd`), and none of those commits cites D-16/D-17/D-19/D-1 as team.md requires. Per `project.md`'s "never edit a human-signed record" and c30, do not amend/re-commit — state the discrepancy and route a remediation choice (an amend, or a follow-up commit that cites the D-numbers, or an explicit owner waiver) to the gate. |
| 2 | Minor (carried forward, unresolved, correctly not this unit's to fix) | `configs/data.yaml` | `qc_operations`/`target.*` keys still entirely absent (re-confirmed by direct grep this pass) rather than stubbed `TBD — freeze gate` like the `stations`/`cell_rule` precedent. Harmless: `assert_qc_operations_frozen` treats absent and TBD identically and still refuses correctly (re-verified live below). | No new action; already on the gate list. |
| 3 | Minor (carried forward, unresolved, correctly not this unit's to fix) | `tests/test_phase_boundary.py:95` (sibling file) | `D17_TARGET_FIELDS` still enumerates 17 fields (`processor_qc_flags` extra) against D-17's frozen 16, re-derived this pass directly from `evidence/DECISIONS.md` D-17's field table (counted 16 distinct names: `interval_start_utc, station_id, cell_gdlat, cell_glon, cell_lat_bounds, cell_lon_bounds, vtec_tecu, valid_observation_count, within_hour_spread_tecu, largest_internal_gap_s, provider_dtec_summary, aggregation_config_id, target_valid, phase_id, source_id, target_definition_id`) and cross-checked byte-for-byte against `prepared.py`'s `D17_FIELDS` tuple (16 entries, same order). Still routed to the gate; still not this unit's file to edit. | No new action; already on the gate list. |

### Adversarial checks run this pass, independently re-derived (not carried from iteration 2)

- **Q2=A gate is still the literal first statement**: read `standardize_hourly_target` body directly (`prepared.py:967`, `assert_qc_operations_frozen(data_config)  # Q2 = A: ALWAYS first`) — confirmed by direct read, not grep alone.
- **Script 02 wiring re-confirmed by direct read** (`scripts/02_standardize_prepared_target.py`): `require_receipts_for_snapshot` called at line 255 (after `assert_phase_boundary` at 250, before `assert_qc_operations_frozen`'s call inside `standardize_hourly_target` at 331); `assert_no_raw_fields(PRODUCED_FIELDS, phase=PHASE)` present at line 155.
- **`scripts/03_verify_processing.py`'s `_load_tolerance` reroute** (the brief's named hardest attack surface) re-confirmed present and unchanged by direct read: `load_fixture_scope` import and call at lines 272/274-275, `resolve_float_tolerance(scope.data)` at 275 — matches iteration 2's directly-verified strictly-narrows analysis; no regression possible since the file has zero commits since that analysis (`git log f0d9e49..HEAD -- scripts/03_verify_processing.py` → empty).
- **Target label discipline re-confirmed by direct read**: `TARGET_LABEL = "location-sampled gridded VTEC"` (`prepared.py:137`), `_PROHIBITED_FRAGMENTS = ("station-observed", "receiver-specific")` (`prepared.py:141`), enforced by `assert_no_prohibited_phrasing`/label checks (`prepared.py:824-863`); `target_definition_id` stamped and asserted present (`prepared.py:653,800,805`).
- **D-5/D-10.2 (never impute/interpolate/fill) re-verified by direct grep this pass**: `interpolate|fillna|ffill|bfill|impute` across `src/data/prepared.py`, `scripts/02_standardize_prepared_target.py`, `scripts/03_verify_processing.py` → the only matches are prose ("interpolates, smooths and fills NOTHING" / "No value is interpolated, smoothed or filled") — zero executable occurrences.
- **D-17 sixteen-field contract independently re-counted from `evidence/DECISIONS.md` this pass** (see Finding 3) and matched exactly against `D17_FIELDS` in `prepared.py:195-211` (16 entries, same order) — not carried from the prior review's count.
- **No TBD sentinel filled, no credential/secret, no scientific constant hardcoded**: `configs/data.yaml` still carries no `qc_operations`/`target.*` key at all (Finding 2); grep for `api_key|secret|password|token\s*=` across this unit's three code files returns only a local variable literally named `token` used for text tokenization (`prepared.py:727,733`) — not a credential.
- **Line-count and test-count claims independently re-executed, not re-read**: `wc -l` → `scripts/02_standardize_prepared_target.py` 428, `scripts/03_verify_processing.py` 386, `src/data/prepared.py` 1555, `tests/test_prepared_target_schema.py` 741 — the first two match the code-summary's own claim exactly. Ran the scratchpad's parametrize-expanding stand-in runner (`run_target_std_tests.py`, stdlib-only, CPython 3.11.16; real pytest/pyyaml unreachable, PyPI egress blocked, reconfirmed) against both named test files: `tests/test_prepared_target_schema.py` → **62 passed, 0 failed, 0 errored, 0 skipped**; `tests/test_phase_boundary.py` → **52 passed, 0 failed, 0 errored, 1 skipped** (`test_target_artifact_conforms_to_d17_when_it_exists`, skip reason: no target artifact exists, matching the Q2=A design). Combined **114 passed, 0 failed, 1 skipped** — matches the code-summary's and iteration 2's claimed counts exactly.
- **Repo-wide D-33..D-38 spillover re-checked**: none of `cell_rule`, `partitions`, `embargo_hours` is read by this unit's code (grepped `prepared.py` and both scripts for each key name — zero matches); `stations` and `practical_relevance_threshold` remain `TBD — freeze gate` and are correctly unread here.

### Coverage limits

Same bound as iteration 2: this unit's own artifacts, the passed functional-design/
nfr-design/units-generation contracts, `evidence/DECISIONS.md` (D-16/D-17/D-19 re-derived;
D-33/D-34/D-35/D-36/D-37/D-38 read for spillover only), `configs/data.yaml`/
`configs/experiment.yaml`, and the sibling files this unit's own artifacts name as
integration points (`tests/test_phase_boundary.py`) or that the dispatch brief named for a
blast-radius check (`tests/test_locked_test_guard.py`, checked for references only, not
reviewed as a unit). No other sibling unit's construction directory was read.

### Summary

Nothing has regressed: this unit's five owned files are unchanged since the iteration-2
review (zero commits, zero uncommitted diff), and every adversarial check re-derived this
pass — the Q2=A refuse-first gate, the script-03 tolerance-loader narrowing, the D-17
sixteen-field contract, the target-label discipline, the imputation ban, and the test/line
counts — reproduces exactly, independently, without carrying forward any prior count. The
two carried-forward Minor findings remain correctly unowned by this unit and non-blocking.
One new finding this pass is Major, not Critical: the artifact's own headline claim ("No
git commit") is stale and self-contradicting against its own later text and against git
history — this unit's code has in fact been committed three times (`ed5808b`, `cf3185d`,
`0e002cd`), and none of those commits cites the D-16/D-17/D-19/D-1 context the team's Way
of Working makes mandatory for a commit touching a governed artifact. This is a
documentation-accuracy and commit-hygiene defect, not a functional or architectural one —
no code path, test, or gate mechanism is affected — so under this project's stated verdict
rule (zero Critical, ≤2 Major) it does not block READY, but it must be corrected at the
artifact level and the D-number-citation gap routed to the gate rather than silently
amended.

## Adversarial re-review (2026-09-13, code-generation, REJECTED-gate re-review, iteration 4)

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-13T10:04:49Z
**Iteration:** 4 (fresh re-derivation against HEAD `1670ac8`; prior verdicts not rubber-stamped)

### Scope of this pass

Re-derived the repository commit state directly (`git log`, `git show --stat`, `git show
-1 --format=%B` on `ed5808b`/`cf3185d`/`0e002cd`), re-verified this unit's five owned files
are byte-identical to HEAD (`git status --porcelain` on all five returns nothing), re-derived
the D-17 sixteen-field contract from both `src/data/prepared.py:195-212` and
`tests/test_phase_boundary.py:106-123` directly, and swept this artifact end-to-end for every
representation of the two 2026-09-13 corrections (the commit-state fact and the D-17
reconciliation), not only the two sites the header names.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | `code-summary.md:69,73` (§ "Governance stop — owed before any commit") | The 2026-09-13 repair fixed only the header (line 4) and added the two new paragraphs at lines 6–33. It left a **second, un-swept representation of the exact same false claim** standing three lines below the correction: the section heading itself, "## Governance stop — owed before any commit," and its first bullet, "Commit cites **D-16, D-17, D-19, D-1** as touched context. **No governed commit before the records exist.**" — both still assert, in the present tense and as current fact, that no commit has happened. This is precisely the "parallel claim" the 2026-09-11 (iteration-3) Major finding named for correction ("Correct line 4 (and the parallel claim … 'No governed commit before the records exist.')"), and it was not touched: `git diff HEAD` on this file (verified this pass) shows only the header/new-paragraph edit, nothing at lines 69–74. The artifact therefore now **contradicts itself within 50 lines**: the header correctly states three commits exist (`ed5808b`, `cf3185d`, `0e002cd`, re-verified this pass via `git log`/`git show`, none citing D-16/D-17/D-19/D-1), while § "Governance stop" still reads as though no commit has occurred at all. This is exactly the failure class `project.md` corrections `fd-2026-08-30-sweep-derive-sites` and `fr-2` exist to catch — a repair scoped to a finding's named site (the header) left a sibling representation of the identical fact standing, and here the sibling representation is the one the *prior finding itself explicitly named*, not merely one this pass discovered independently. | Rewrite the section heading (e.g. "Governance stop — items owed before the next commit") and the bullet at line 73 to state the actual fact: this unit's code IS committed (`ed5808b`, further touched by `cf3185d`/`0e002cd`), none of those three commits cites D-16/D-17/D-19/D-1, and what remains owed is the remediation choice (amend / follow-up commit / owner waiver) already routed to the gate by the new header paragraph — not a claim that "no governed commit" exists. |

### Verified and held (adversarial checks that survived)

- **Commit-state re-derivation, independent of the artifact's own claim.** `git log -1 --format=%B ed5808b/cf3185d/0e002cd` confirms: `ed5808b`'s message is the unedited git placeholder, introducing this unit's five files plus all four `configs/*.yaml` (confirmed via `git show --stat`) and citing no D-number; `cf3185d`'s message is also the unedited placeholder, modifying `scripts/02_standardize_prepared_target.py` (+31/-…) and `scripts/03_verify_processing.py` (+24/-…); `0e002cd` carries a real message citing D-11/D-14/D-20/D-28/D-29/D-31 (none of D-16/D-17/D-19/D-1) and modifies only `scripts/02_standardize_prepared_target.py` (43 lines), not `scripts/03`. All three claims in the new header paragraph (lines 6–19) match exactly.
- **D-17 reconciliation, both limbs, independently verified against current source, not taken on the artifact's word.** `src/data/prepared.py:195-212`'s `D17_FIELDS` holds exactly 16 names in D-17's order. `tests/test_phase_boundary.py:106-123`'s `D17_TARGET_FIELDS` now also holds exactly 16 names, identical set — `processor_qc_flags` is gone (a code comment at lines 100-105 states it was "carried here in error from commit `b844a4d`… and removed 2026-09-13"). The second limb — the symmetric-`extra` staleness against `lineage_caveat` — is also present and fixed: `DECLARED_CAVEAT_FIELD = "lineage_caveat"` (line 130) is pinned against the producer's `LINEAGE_CAVEAT_FIELD`, excluded from both the drift-guard equality check (line 327) and the header/`extra` diff (lines 339-374), mirroring `prepared.py`'s own row guard (`extra = sorted(names - set(D17_FIELDS) - {LINEAGE_CAVEAT_FIELD})`, `prepared.py:791`). A new drift-guard test (`test_d17_target_fields_match_the_producer_contract`, `test_phase_boundary.py:298`) now fails the two copies apart. This work is entirely inside `tests/test_phase_boundary.py`, owned by `governance-guards`, not this unit — confirmed by `git status --porcelain` showing none of this unit's five owned files touched.
- **No file owned by this unit changed.** `git status --porcelain -- src/data/prepared.py scripts/02_standardize_prepared_target.py scripts/03_verify_processing.py tests/test_prepared_target_schema.py src/data/config.py` returns nothing; `wc -l` on the four size-bearing files (428/386/1555/741) matches every prior-iteration and this artifact's own claimed counts exactly.
- **Standing invariants hold.** No `hourly_target*.csv` or other standardized-target artifact exists anywhere in the workspace (searched); `configs/data.yaml` still carries no `qc_operations`/`target.*` key (grepped directly); no touch to `evidence/locked_test_restricted/`; no credential/secret pattern found in this unit's files (not re-swept this pass beyond the prior iterations' grep, no new code was added to re-check).
- **Attribution boundary respected.** The four other dirty files in this working tree (`tests/test_determinism.py`, `tests/test_phase_boundary.py`, `tests/test_phase_contract.py`, `src/evaluation/guards.py`) and the sibling `code-summary.md` files are correctly not credited to or blamed on this unit anywhere in this artifact; the D-17 fix is correctly attributed to `governance-guards` throughout, including in the new 2026-09-13 paragraph.
- **Execution honesty.** No Python interpreter is reachable on this clone this pass (`python`/`python3` both resolve to the Microsoft Store app-execution-alias stub, confirmed non-functional) and PyPI egress remains blocked per the artifact's own prior-iteration statements; every test-count claim in this artifact remains correctly bounded under the "smoke evidence only — never governed" heading, and this pass did not re-execute any test (no interpreter available) — it re-derived only what is directly readable from source and git history.

### Coverage limits

This pass verified the unit's own five files, the commit history for `ed5808b`/`cf3185d`/`0e002cd`, the single sibling file this unit's own artifact names as an integration point (`tests/test_phase_boundary.py`, resolved to its owning location per the spot-check carve-out — not browsed), `configs/data.yaml`, and this artifact's own text end-to-end for internal self-consistency. No other sibling unit's construction directory was read.

### Summary

The two 2026-09-13 corrections are each independently true and well-evidenced — the commit-state fact (three commits, none citing the required D-numbers) and the D-17 reconciliation (both limbs, verified against current source in both `prepared.py` and the sibling `test_phase_boundary.py`) both hold under direct re-derivation. But the repair is incomplete: it corrected the header and stopped, leaving the artifact's own § "Governance stop" section — the exact site the prior Major finding named as the "parallel claim" requiring correction — still asserting in the present tense that no commit exists. A reader who reaches line 69 before line 6 (or who reads only the Governance-stop bullet list, which is what a gate reviewer scanning for open items would naturally do) is told the opposite of what the header now says. This is a self-contradiction inside the primary artifact, not a stale-but-harmless residual, and it reproduces — inside the very repair meant to close it — the sweep-completeness failure `project.md` has flagged repeatedly (`fd-2026-08-30-sweep-derive-sites`, `fr-2`). One Critical finding is sufficient to block READY under this project's stated verdict rule.

**Verdict: NOT-READY**

## Adversarial re-review (2026-09-13, code-generation, terminal re-review, iteration 5)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-13T00:00:00Z (see repo evidence below for exact commands/output)
**Iteration:** 5 (TERMINAL — budget exhausted after this pass; fresh re-derivation against HEAD `1670ac8`, prior verdicts not rubber-stamped)

### Scope of this pass

Verified whether the iteration-4 Critical (self-contradicting "Governance stop" section)
is genuinely closed at its named location; re-derived the three commits' messages and
diffs directly; re-derived `D17_FIELDS`/`D17_TARGET_FIELDS` from current source on both
sides of the contract; re-derived the git diff of this unit's five owned files against
`1670ac8`; re-derived the `62 tests` claim by counting `def test_` functions and
`@pytest.mark.parametrize` expansions separately; swept the full document for every
remaining representation of the "no commit"/"17-field" claims, distinguishing frozen
historical review blocks and quoted-for-correction text from live current-state claims.

### Findings

None. The iteration-4 Critical is closed and no new defect was found.

### Verification of the iteration-4 Critical

The section previously headed "## Governance stop — owed before any commit" (line 69) now
reads "## Governance stop — owed at the gate," with a dated blockquote (lines 71–78)
stating exactly what the heading and its commit bullet previously said and why both were
wrong. The former commit bullet — "No governed commit before the records exist" — is
replaced (line 82) by: "**The commits exist and cite none of D-16, D-17, D-19, D-1**,"
naming `ed5808b`/`cf3185d`/`0e002cd`, correctly stating none cites the required D-numbers,
and correctly reframing the owed act as the remediation choice on commits already made. `git
diff HEAD` on this file was not needed to confirm this — the current on-disk text at lines
69–82, re-read directly this pass, no longer asserts "no commit" anywhere. The self-
contradiction the prior Critical named (header saying commits exist; three lines below,
the section heading and its first bullet saying none did) is gone: both now agree.

**Sweep for every other representation, not just the two the finding named.** Grepped the
whole document for `governance stop`, `No governed commit`, `processor_qc_flags`,
`D17_TARGET_FIELDS`, and `17 field`/`17 names`. Every hit outside the live "current state"
section (lines 1–83) falls inside a dated, headed historical review block (the 2026-09-06
iteration-1 review at lines 85–120, the 2026-09-10 iteration-2 review at 147–302, the
2026-09-11 iteration-3 review at 304–375, the 2026-09-13 iteration-4 review at 377–415) —
each of these correctly records what was true, or what a finding asserted, at the time it
was written (e.g. line 7 quotes the superseded header text specifically to correct it; line
97/178/334 are iteration-1/2/3 findings correctly describing the 17-field state that existed
before the 2026-09-13 fix). None of these is a live claim a current reader would mistake for
present fact — each sits under its own dated `## Review`/iteration heading. No live
(non-historical) site anywhere in the document still asserts "no commit" or "17 fields."

### Re-attack of both 2026-09-13 corrections' substance, independently derived

- **Commit-state fact, re-derived from git directly, not taken on the artifact's word.**
  `git show -s --format=%B` on all three: `ed5808b` and `cf3185d` are both the unedited
  git placeholder ("Please enter the commit message for your changes...", with the
  `git status` boilerplate captured verbatim as the message body) — confirmed neither
  cites any D-number. `0e002cd` carries a real subject line ("Governance disposition +
  board remediation for fixtures-and-reproducibility (3.5)") citing D-11, D-14, D-20,
  D-28, D-29, D-31 — none of D-16/D-17/D-19/D-1, exactly as claimed. `git show --stat`
  confirms `ed5808b` introduces this unit's five files plus all four `configs/*.yaml`;
  `cf3185d` modifies both `scripts/02_standardize_prepared_target.py` and
  `scripts/03_verify_processing.py`; `0e002cd` modifies only `scripts/02` (43 lines per
  its stat), not `scripts/03` — all three details in the artifact's header match exactly.
- **D-17 reconciliation, both limbs, independently re-derived from current source.**
  `src/data/prepared.py:195-212`'s `D17_FIELDS` tuple holds exactly 16 names in D-17's
  order (counted directly). `tests/test_phase_boundary.py:106-121`'s `D17_TARGET_FIELDS`
  frozenset now also holds exactly 16 names, the identical set — `processor_qc_flags` is
  gone, with a code comment (lines 100–105) recording it was carried in from commit
  `b844a4d` in error and removed 2026-09-13. The second limb (the symmetric `extra`
  staleness against `lineage_caveat`) is also fixed: `missing = D17_TARGET_FIELDS - header`
  (line 371, still demands all sixteen) and `extra = header - D17_TARGET_FIELDS -
  {DECLARED_CAVEAT_FIELD}` (line 370, permits `lineage_caveat`) — read directly, not
  taken on the artifact's description. This work is entirely inside
  `tests/test_phase_boundary.py`, confirmed still not one of this unit's five owned files.
- **No file owned by this unit differs from HEAD `1670ac8`.** `git diff 1670ac8 --stat --
  src/data/prepared.py scripts/02_standardize_prepared_target.py
  scripts/03_verify_processing.py tests/test_prepared_target_schema.py src/data/config.py`
  returns empty, and `git status --porcelain` on the same five paths returns nothing.
- **The `62 tests` claim, re-derived by counting mechanism rather than re-reading the
  number.** `grep -c "^def test_"` on `tests/test_prepared_target_schema.py` gives **55**
  distinct test functions, not 62 — but four of those 55 carry
  `@pytest.mark.parametrize` with 2, 4, 3, and 2 cases respectively (11 parametrized cases
  total, replacing the 4 base functions they decorate): 55 − 4 + 11 = **62** collected
  test cases under pytest's own counting convention (one collected item per parametrize
  expansion). The artifact's "62 tests" is the collected-case count, not the function
  count, and it is arithmetically exact — not a stale or inflated figure.
- **`configs/data.yaml` still carries no `qc_operations` or `target.*` key** (grepped
  directly, zero matches) — the standing Minor from every prior iteration remains
  correctly unresolved and non-blocking; `assert_qc_operations_frozen` treats absent and
  unfrozen identically, so this has no functional effect.
- **No December/restricted-root touch, no credential.** No reference to
  `evidence/locked_test_restricted/` in this unit's files; grep for
  `api_key|secret|password|token\s*=` across the five owned files returns only a local
  tokenization-loop variable literally named `token` (`prepared.py:727,733`) and two
  prose sentences about supplying secrets via a platform store (`config.py:708,986`) —
  no credential literal.
- **Nothing wrongly claimed discharged.** TA-19/FR-P1-03-5/FR-P1-03-1/BLK-05 are still
  stated as open/pending/blocked at line 83 — matches the standing state.

### Attribution boundary respected

The working tree's other dirty files this session — `tests/test_determinism.py`,
`tests/test_phase_boundary.py`, `tests/test_phase_contract.py`, `src/evaluation/guards.py`,
and several sibling `code-summary.md` files — are correctly not credited to or blamed on
this unit anywhere in the document; the D-17 fix is attributed to `governance-guards`
throughout, consistent with `git status --porcelain` showing none of those files among
this unit's own five.

### Execution honesty

No Python interpreter is reachable on this clone this pass (`python`/`python3` both
resolve to the non-functional Microsoft Store app-execution-alias stub, re-confirmed);
no test was executed this pass. Every test-count claim in this artifact remains correctly
bounded under its own "smoke evidence only — never governed" heading, and this pass adds
no execution claim beyond that bound — only static re-derivation from source and git
history.

### Coverage limits

This pass verified the unit's own five files, the commit history and diffs for
`ed5808b`/`cf3185d`/`0e002cd`, the single sibling file this unit's own artifact names as
an integration point (`tests/test_phase_boundary.py`, resolved to its owning location per
the spot-check carve-out — not browsed), `configs/data.yaml`, and this artifact's own text
end-to-end for internal self-consistency across all five prior review blocks. No other
sibling unit's construction directory was read.

### Summary

The iteration-4 Critical is closed at its named location: the "Governance stop" heading
and its commit bullet no longer contradict the corrected header, and a full-document sweep
(not just the two sites the finding named) turns up no other live representation of either
superseded claim — every remaining occurrence sits inside a dated historical review block
that correctly records what was true when it was written. Both 2026-09-13 corrections
re-verify true under independent re-derivation: the three commits and their D-number
citations (or lack thereof), and the D-17 sixteen-field contract on both sides (producer
and sibling test), both hold exactly as newly stated. No file owned by this unit differs
from HEAD. The "62 tests" figure is exact once parametrize expansion is counted, not a
stale carry-forward. Standing invariants (no target artifact produced, no `qc_operations`/
`target.*` key in `configs/data.yaml`, no credential, no wrongly-discharged acceptance row,
correct attribution boundary against four sibling-owned dirty files) all hold. Zero
Critical, zero Major, two carried-forward Minors (both non-blocking, both correctly not
this unit's to fix). This pass is terminal.

**Verdict: READY**

---

## Post-receipt amendment — 2026-09-20 (`GOV-2026-09-20-CG-01`, consequential only)

*Written into the body, not filed as a review addendum, per `project.md`
(`code-generation:fr-2`). The stage receipt and the `READY` verdict above are **frozen and
untouched**. **No module this unit owns was edited** — `src/data/prepared.py` and
`scripts/02_standardize_prepared_target.py` both show a **zero diff against `ff5c683`**,
measured with `git diff --numstat` at the moment this section was written. This section
exists because two changes made elsewhere reach this unit, and because one of its test
modules WAS edited.*

⚠ **UNEXECUTED.** No test or script was run — no usable Python interpreter exists on this
clone. Every statement below is **static**. `git log -1` = **`ff5c683`**; everything below
is uncommitted working tree and no git state-changing command was run.

### 1. `resolve_target_identity` gained three new callers outside this unit

Board **Recommendation 24** (TEC-05 stamps absent from every acquisition-side manifest)
made `phase_id`/`source_id`/`target_definition_id` required on five writers at stages 00
and 01. Rather than add a second transcription, all of them resolve through **this unit's**
`prepared.resolve_target_identity` — now called from
`scripts/00_acquire_prepared_vtec.py::_resolve_stamps`,
`scripts/01_inventory_and_registry.py::_resolve_stamps` and
`scripts/audit_gfz_drivers.py::_resolve_stamps`. The function itself is **unchanged**; what
changed is that it is now the single identity resolver for the whole provenance chain
rather than for stage 02 alone.

**Consequence to read carefully.** `resolve_target_identity` raises while
`configs/data.yaml` carries no `target.identity` block — which it does not. That refusal
was previously reachable only on this unit's own path. It is now also reachable on a
non-fixture stage-00 acquisition run, on the stage-01 source-inventory path, and on the
stage-01 **`--audit`** path, which is the required pre-G-05 December coverage and regime
audit. The owner's `target:` transcription is now a precondition of all four, not one.
This is the TE §18.3 stop-and-report behaving as designed; it is recorded here so a reader
of this unit's record knows that its resolver's blast radius grew.

### 2. `tests/test_prepared_target_schema.py` was edited — +11 / −3

Board **Recommendation 46** made `acquisition.parse_record_date_utc` the one record-date
derivation and, in doing so, made it **refuse a naive timestamp** rather than assume UTC.
The fixture-window control in this unit's test module
(`test_…_declared_window…`, ≈ line 765) fed three **naive** `interval_start_utc` literals
to `assert_records_within_window`. Left alone, its in-window assertion would have raised on
the **parse**, and its out-of-window half would have raised for the wrong reason while
still matching its `2022-11-03` fragment — a control that fails, or passes, for a reason
other than the one it names. The three literals now carry a trailing `Z`, which is the
shape `prepared.hour_start_utc` actually emits (`"%Y-%m-%dT%H:00:00Z"`).

**Production is unaffected.** Every real `interval_start_utc` is `Z`-suffixed by
`hour_start_utc`, and the month files' `date` column is a bare `YYYY-MM-DD`, which
`parse_record_date_utc` accepts explicitly because it carries no offset to misread.

No December content was read, no restricted-root path touched, no scientific constant
decided, and `configs/data.yaml` remains untouched. The gate verdict for
`GOV-2026-09-20-CG-01` stands at **`FAIL`**; nothing here advances it.
