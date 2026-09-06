# Code Summary — `inventory-and-registry`

**Unit** `inventory-and-registry` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`
**Plan**: `code-generation-plan.md` — all 9 steps executed, checkboxes marked. No `git commit` (governance stop). The December audit was NOT executed (BLK-07 refusal live and tested); no §18.2 value entered anywhere; `configs/data.yaml` untouched.

## Files created

| Path | What |
|---|---|
| `src/data/inventory.py` | W-1 source inventory (nine §5.1 fields, per-entry failure naming entry + field; verbatim `acknowledgment_notice` distinct from access notes; every value through `acquisition.guard_egress`); W-5 governed-schema validation (stdlib-only digest, self-contained `SchemaReport`, per-class `SchemaError`); the importable December-audit engine — Check 1 scope-vs-reference before any read; two-class **record-date** routing with class/residency disagreement = stop-and-report naming the file; `new_audit_run_id()` = `audit-<UTCstamp>-<8uuid>`; reconciliation 3a per-`run_id` + 3b all twelve months (December included); `data07_caveat` from `provenance_class`, absent source = §18.3 stop; `finalize_audit_reports` all-or-nothing (no report on failure, rows stand); `build_gp1a_record`/`assert_gp1a_record` (D-12 **and** D-2 verdicts, figures D-number-attributed, D-2 post-hoc disclosure on the record, no soft margin); `assert_prohibition_results` (four separately named results; this unit's two: silent imputation, source mixing). `GateError` declared here |
| `src/data/registry.py` | Approved `Station`/`load_registry`/`assert_registry_resolved` signatures matched (+ `provenance` field per R-46); Q2=A runtime refusals (stations/cell_rule/igrf `TBD` → `RegistryError`; absent IGRF **fails, never falls back**; "default"-marked IGRF refused); named-source conflict resolution (R-47, coincidence residual pinned); `migration_diff`/`assert_migration_unchanged` (R-48) |
| `scripts/01_inventory_and_registry.py` | Position 01; six-step entry (`ensure_process_determinism` first, `assert_no_raw_fields` before first write); registry rows via foundation's writer; default path writes the source inventory (honestly empty today, machine-readable `missing_entries`); `--build-registry` refuses (TBD); `--audit` **refuses naming BLK-07**; `merge_coverage_year.py` logic migrated in — sha256 consolidated onto `release.sha256_of_file`, `retrieved_at_utc` placeholder replaced (DISC-I-2 discharged in the migrated copy); original script untouched |
| `tests/test_import_boundary.py` | Limb A (direct imports over `src/data/*` + script 01; unparseable fails) + Limb B (transitive closure from audit entry point; cycles terminate; computed imports reported); two separately named injection controls. `PHASE1_PERMITTED_PACKAGES` untouched |
| `tests/test_station_registry.py`, `tests/test_december_audit.py` | Every Step 1–4 refusal negative-controlled — averaged-conflict, coincidence residual, short scope refused pre-read, ordinary path never logged, both stop-and-reports, interrupted audit leaves no report, per-`run_id` 3a, December in 3b, caveat-less `derived_only` failure, unattributed figure failure, four prohibition results, BLK-07 script refusal |
| `governance/CHANGE_RECORD_2026-09-05_import_boundary_matrix.md` | **DRAFT** — the 3 `component-dependency.md` edits (the `scripts/*` carve-out listed first as the largest deviation); matrix **not** edited; owner approval at the gate applies it |

## Files modified in place

| Path | What |
|---|---|
| `src/data/config.py` | `InventoryError`, `SchemaError`, `AuditScopeError` added (Q1=A; `IntegrityError` subclasses; `__all__`; R-01 any-future clause cited; `AuditScopeError`'s resource = declared scope, never a file path); `RegistryError` docstring widened to both registries discriminated by `resource` (`StationRegistryError` route named, not taken); **one un-itemised addition**: minimal `("inventory-and-registry", 1): ("seeds.development",)` in `REQUIRED_FIELDS_MAP` — without it no path of script 01 can run; deliberately excludes stations/cell_rule/igrf (Q2=A fixes their enforcement point in registry code; comment records this) |

## Test and lint results (smoke evidence only — never governed)

- **Full suite: 594 passed, 2 skipped, 0 failed** — Python 3.11.9; **re-run independently by the orchestrating session, same counts.** New modules: 97 passed. Both skips pre-existing.
- `ruff check`: all checks passed on the seven touched files. `merge_coverage_year.py`'s 4 pre-existing findings remain (file read-only by plan).

## Key decisions

1. **`GateError` declared in `inventory.py`, not `config.py`** — Q1=A's receipted scope named exactly three names; adding a fourth would widen an owner ruling to an item they were not shown. Declaration-site OPEN item recorded in the docstring.
2. **D-12/D-2 thresholds not inlined and not transcribed** — `gp1a_thresholds_from` reads a `gp1a` config block and stop-and-reports when absent; transcription of frozen values into the governed config is the owner's act, cited by D-number.
3. **No pre-read probe in routing**: a content probe deriving the class would itself be an unlogged December read; residency is the routing hypothesis, record-date verification follows the logged read, either disagreement stops naming the file (the TEC-09 shape).
4. **No restricted-root literal in any new file**; synthetic locked months `(2021, 6)` execute every December-modeling control; no test reads `evidence/`.
5. `build_regime_report` derives month-end from the calendar (December = 31; D-28's 2–31 preserved) so synthetic controls execute.

## Deviations

- `REQUIRED_FIELDS_MAP` entry (above) — necessary and minimal; recorded here rather than silent.
- `GateError` placement (above).
- graphify CLI unavailable — graph stale for touched files; `graphify update .` owed.

## Governance stop — owed before any commit (student acts; cumulative)

- `CHANGE_RECORD_2026-09-05_import_boundary_matrix.md` is **DRAFT — NOT APPLIED**; owner approval at this stage's gate applies the 3 matrix edits.
- Gate-routed rulings restated: **W-6's two-class wording** (amend upstream by change record vs narrowing recorded in the gate record alone); **FR-P1-02-8's replacement acceptance row** (TA-29 withdrawn; row is 3.2's/change control's); **SchemaError Q1=A** recorded in the draft's context; **`GateError` declaration site** open item.
- Commit cites **D-12, D-2, D-15** as touched. **No governed commit before the records exist.**
- Nothing discharged: WS-01, TA-04, TA-25 stay `Pending`; FR-P1-02-7/-8 stay rowless; FR-P1-01-2's `suffix_mismatch` surfacing stays ⚠ PROPOSED (3.2's).

## Review — 2026-09-05 (code-generation, iteration 1)

**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T17:15:35Z
**Iteration:** 1

### Findings

| # | Severity | Where | What | Recommended action |
|---|---|---|---|---|
| 1 | Minor | `configs/data.yaml` | The file carries no `igrf_version`, `prepared_schema` or `gp1a` keys at all (not even as `TBD — freeze gate` stubs), while `src/data/inventory.py` and `src/data/registry.py`'s own docstrings and error text describe the runtime state as "`configs/data.yaml` keeps its `TBD — freeze gate` sentinels" for these fields. Functionally inert — `expected_schema_from`, `load_registry` and `gp1a_thresholds_from` all treat "absent" and "`TBD` sentinel present" identically and refuse either way (verified: `data.get(...) is None` short-circuits before the sentinel-string check in every case) — but the code's own narrative is not quite what is on disk. | No code change needed. If a later Bolt transcribes any of these blocks, note that today's absence, not a stale sentinel, is what the refusal is actually keyed on. |

### Verified and held (adversarial checks that did NOT surface a finding)

- **December discipline.** No new file (`inventory.py`, `registry.py`, `01_inventory_and_registry.py`, the three new test modules) contains the restricted-root literal `evidence/locked_test_restricted` or constructs a path into it — grepped directly, zero hits. `RESTRICTED_LITERAL_EXEMPT_MODULES` (owned by `governance-guards`, `src/data/locked_test.py`) is untouched by this unit; none of this unit's files appear in it. No test reads `evidence/` — all December-modeling fixtures use `tmp_path` synthetics and `locked_test._repo_root` monkeypatching. `scripts/01_inventory_and_registry.py --audit` genuinely refuses first, before any scope declaration or read — ran `_require_december_authorization()` via `tests/test_december_audit.py::test_audit_entry_point_refuses_naming_blk07`, confirmed `LockedTestError` naming `BLK-07` and `2022-12`.
- **Record-date class test.** `route_audit_path` treats restricted-root residency as the routing HYPOTHESIS (computed from the record-date class before any read), never the definition; `assert_record_date_class_agreement` verifies by record date AFTER the logged read, and either direction of disagreement raises `LockedTestError` naming the file (confirmed in `src/data/inventory.py:route_audit_path`/`assert_record_date_class_agreement` and exercised by `test_december_bearing_class_outside_root_is_a_stop_and_report`, `test_ordinary_class_inside_root_is_a_stop_and_report`, and the realized-TEC-09-shape control `test_ordinary_read_carrying_a_locked_month_record_stops_and_reports`). No path-or-directory-name-based membership decision found anywhere in the reviewed files — `is_december_bearing`/`attribute_records_by_month` decide strictly off a parsed `timestamp` field and fail closed on an unparseable one.
- **Check 1/3 completeness.** `assert_scope_equals_reference` raises `AuditScopeError` on an eleven-month declaration before any read (`resource == "declared audit scope"`, never a file path) — confirmed by `test_eleven_month_declaration_fails_before_any_read`. `reconcile_audit`'s 3b explicitly checks all twelve `AUDIT_MONTHS` including December (`test_reconciliation_3b_covers_all_twelve_months_december_included`), and `finalize_audit_reports` writes nothing before every check passes, leaving access rows standing on failure (`test_interrupted_audit_leaves_no_report_while_rows_stand`). Per-`run_id` reconciliation (3a) is genuinely per-attempt: `test_reconciliation_3a_is_per_run_id` shows a stale row from a different `run_id` is correctly ignored.
- **Registry refusals.** Absent `igrf_version` fails and never falls back (`test_absent_igrf_version_fails_and_never_falls_back`, distinct from the separately-tested TBD and "default"-marker cases). Averaged conflicts are refused via named-source equality, including the three-source case an existence check would pass (`test_three_source_average_equal_to_a_non_named_source_is_rejected`), and the coincidence residual is pinned rather than silently claimed caught (`test_coincidence_case_passes_and_is_pinned_as_the_stated_residual`). `TBD` sentinels refuse the build at three separate points (stations, cell_rule, igrf_version). The approved `Station`/`load_registry`/`assert_registry_resolved` signatures are reproduced without widening, `provenance` being the one stated R-46 amendment.
- **data07_caveat.** Absent `provenance_class` is a stop-and-report (`PreflightError`, never an uncaveated figure) — `test_absent_provenance_class_is_a_stop_and_report_never_an_uncaveated_figure`. A `derived_only` figure without the caveat fails at both the report-producing surface (`assert_figures_caveated`) and the G-P1A record surface (`assert_gp1a_record`/`test_derived_only_record_entry_without_caveat_fails`) — two independent enforcement points, not one. `build_gp1a_record` attributes every figure to D-12 or D-2 by name and carries `D2_DISCLOSURE` verbatim on the record. All four `PROHIBITION_RESULT_NAMES` are asserted present and passing individually (`test_removing_any_one_of_the_four_prohibition_results_fails_the_gate` iterates all four).
- **Import boundary.** Ran both limbs directly: Limb A (`test_limb_a_src_data_and_audit_script_import_no_models_or_evaluation`) and Limb B (`test_limb_b_audit_entry_point_closure_excludes_models_and_evaluation`) pass over the real tree. The two negative controls are genuinely separately named results — `test_limb_a_catches_injected_direct_import` and `test_limb_b_catches_injected_two_hop_chain` — the latter specifically exercising the case Limb A structurally cannot see (a chain leaving the constrained set through an unconstrained package). An unparseable file fails via `pytest.fail` (preserved from `_imported_modules`), and a computed/dynamic import target is reported rather than assumed clean (`test_dynamic_computed_import_is_reported_never_assumed_clean`). `test_phase_boundary.py`'s `PHASE1_PERMITTED_PACKAGES`-based tests still pass unchanged (part of the 594-passed full-suite run).
- **Scope/authority honesty.** `REQUIRED_FIELDS_MAP`'s new `("inventory-and-registry", 1)` entry carries exactly one field identity (`seeds.development`) — no scientific value, no `TBD` filled, and deliberately excludes stations/cell_rule/igrf per the docstring's own stated rationale. `GateError` is declared in `src/data/inventory.py`, not silently folded into `config.py`'s Q1=A ruling — its docstring records the declaration-site question as a standing open item, matching the code-summary's claim. `component-dependency.md` has zero uncommitted changes (`git status --porcelain` empty for that path) — the change record is genuinely DRAFT and unapplied. No `TBD — freeze gate` value was filled anywhere in `configs/data.yaml` this pass (untouched relative to its pre-existing state; see finding 1 for the one documentation-vs-disk nuance found).
- **Claim honesty / plan vs. disk.** All 9 code-generation-plan steps have corresponding on-disk artifacts. `merge_coverage_year.py`'s hashing/merge logic is migrated into `scripts/01_inventory_and_registry.py` (`_read_month_records`, `_dedup`, `_month_dirs`) with the triplicated SHA-256 helper consolidated onto `release.sha256_of_file` and the `retrieved_at_utc` placeholder genuinely replaced with a real call-time value (verified: no `"recorded-at-call-time-by-the-runner"` string anywhere in `src/` or `scripts/`, and `test_restricted_class_read_is_logged_before_and_placeholder_is_gone` asserts the real timestamp format). The original `scripts/merge_coverage_year.py` is untouched (`git status --porcelain` shows no modification to that path). No governed commit exists yet, consistent with the stated governance stop.
- **Suite/lint integrity.** Re-ran the full suite independently: **594 passed, 2 skipped, 0 failed** — exact match to the claim. Re-ran the three new test modules in isolation: **97 passed** — exact match to the claim. `ruff check` on all seven touched files: all checks passed, no findings.

### Coverage limits

This pass read only the files named in the dispatch (this unit's functional-design, nfr-design, the named contracts, and the two sibling security-design carve-outs for `acquisition` and `governance-guards`); no other sibling unit's `construction/` directory was accessed. Business-rules identifiers (W-1…W-9, R-44…R-53, SD-I-00…SD-I-08) were cross-checked against the code and the security-design excerpt quoted above (SD-I-04's corrected two-limb wording), not against every clause of `business-logic-model.md`/`business-rules.md` line by line.

**Verdict: READY**
