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

### Cross-unit edit record (2026-09-10) — edits made by `fixtures-and-reproducibility`, owner-authorised

Appended after the gate rejection lifted the receipt freeze. Under
`CR-2026-09-07-R133-FIXTURES-AND-REPRODUCIBILITY` (§5, §6.1, §11.5; the owner's "apply the
recommended option" ruling), the fixtures unit made these ADDITIVE edits to
`scripts/01_inventory_and_registry.py` — nothing on the full-year path changed:

- Commit `cf3185d`: `--fixture-manifest` option (the visible Q5 = A exemption carrier),
  `_stage_entry(..., fixture_manifest=None)` kwarg, and ONE `require_receipts_for_snapshot`
  call after `assert_lock_complete` (TE §9.2's two-receipt gate; exempt on a fixture run).
- Commit `0e002cd` (board Rec 2 / ML-01): `_declared_data_window` (the inventory walks
  acquisition's outputs, so its declared window IS `acquisition.window_start`/`window_end`
  in `configs/data.yaml`; undeclared → the fixture exemption refuses, TE §18.3), and
  `_refuse_fixture_audit` — `--audit` combined with `--fixture-manifest` refuses outright,
  because the December coverage/regime audit lies outside every fixture window by
  construction; `_stage_entry` gained the `audit` flag to carry that check.

Tests live in `tests/test_clean_run.py` (`test_rec2_01_...`). This unit's owner may
confirm or reverse per the change record.

## Gate-floor re-review (2026-09-10)

**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-10T14:09:54Z
**Iteration:** 2 (gate-floor reset; fresh verdict against current repository state, HEAD
`f0d9e49` plus the uncommitted sibling `acquisition` repair pass to
`src/data/experiment_registry.py`, `src/data/acquisition.py`, `tests/test_acquisition.py`,
`tests/test_clean_run.py`)

### What changed since the 2026-09-05 verdict, verified against disk

- `configs/data.yaml`: `cell_rule` transcribed to `"floor-half-open-d1"` under **D-33**
  (2026-09-10) — supervisor countersignature explicitly recorded as **NOT YET GIVEN**
  (`evidence/DECISIONS.md:2124`, `configs/data.yaml:46-58`). `stations` unchanged, still
  `TBD — freeze gate`. New `partitions:` block (D-38); not read by this unit's code.
- `src/data/experiment_registry.py`: new `REDACTED_FREE_TEXT_FIELDS = ("notes", "reason")`
  and `_guard_free_text_egress`, called from `append_registry_event` before every append
  (lines 154, 241-263, 380). This unit's registry rows (`scripts/01_inventory_and_registry.py:
  _registry_row`) write `notes` as a fixed literal and `reason` only as `str(exc)` from this
  unit's own `IntegrityError`/`LockedTestError` messages — no operator-supplied or
  provider-transport text reaches either column from this unit's code path.
- Board Rec 2 exemption code (`_declared_data_window`, `_refuse_fixture_audit`,
  `--fixture-manifest`) already present from the prior iteration, now re-verified against
  the current test file.

### Attack-point findings

1. **`code-summary.md` vs. disk.** File counts and claims re-derived: `src/data/inventory.py`,
   `src/data/registry.py`, `scripts/01_inventory_and_registry.py`,
   `tests/test_import_boundary.py`, `tests/test_station_registry.py`,
   `tests/test_december_audit.py`, `governance/CHANGE_RECORD_2026-09-05_import_boundary_matrix.md`
   all present and matching the described content. No count claim to re-derive beyond the
   file list itself (this summary makes no numeric test/line-count assertion needing a
   printed derivation). No stale claim found in the body text.

2. **`assert_registry_resolved` / `cell_rule` interaction — no defect.** Traced
   `load_registry` (`src/data/registry.py:250-302`): the `stations` check runs FIRST and
   raises unconditionally while the sentinel is `TBD — freeze gate`, before the `cell_rule`
   check is ever reached. Reproduced directly against a `ConfigSnapshot` built from the
   ACTUAL current `configs/data.yaml` values (`stations="TBD — freeze gate"`,
   `cell_rule="floor-half-open-d1"`, `igrf_version` absent):
   `RegistryError` raised naming `configs/data.yaml:stations`, citing the correct field.
   **No path resolves the registry today** — `cell_rule` being frozen (even without its
   required supervisor countersignature) is inert while `stations` blocks. Latent
   observation, not a live defect: `load_registry` has no check that a populated
   `cell_rule` also carries its TE §18.2 supervisor countersignature — if `stations` is
   filled by a future freeze before that countersignature lands, the registry would
   resolve `cell_rule` on the identifier match alone. Not actionable now (no such path
   exists while `stations` is TBD) and D-33 itself states the countersignature gap is a
   recorded, accepted limitation of the freeze, not a mechanism this unit's code was asked
   to enforce — noted for the record, not raised as a finding.

3. **Board Rec 2 window exemption — genuinely fail-closed; the 01/02/04 vs. 00 asymmetry is
   honestly disclosed, not a hidden gap.** `_refuse_fixture_audit` and `_declared_data_window`
   are both exercised by REAL invocation in `test_rec2_01_out_of_window_inventory_and_audit_refuse`
   (direct calls, not AST) — confirmed `--audit` + `--fixture-manifest` raises `IntegrityError`
   naming the December-outside-every-fixture-window rationale, `--audit` alone with no
   manifest is unaffected (gated instead by the separate BLK-07 check), and an out-of-window
   declared window is rejected by `assert_declared_window_within_scope`. What is NOT present
   for script 01 (unlike script 00's `test_rec2_00_stage_entry_real_invocation_refuses_out_of_window`)
   is a genuine end-to-end invocation of `_stage_entry` itself with real config directories;
   instead `_assert_entry_passes_declared_window` is an AST wiring check, and the final
   assertion is a literal source-substring check. This asymmetry is stated verbatim in the
   test file's own docstring (`tests/test_clean_run.py:1955-1959`, "adversarial re-review
   2026-09-10, Finding 2") — it is disclosed, not silently narrower. Read `_stage_entry`
   directly (`scripts/01_inventory_and_registry.py:276-314`): the wiring is a single
   straight-line call (`declared_window = _declared_data_window(snapshot) if fixture_manifest
   is not None else None`, passed straight to `require_receipts_for_snapshot`), not
   conditional logic complex enough for the AST+unit-level coverage to plausibly miss a
   wiring defect. Verdict: an honest, disclosed asymmetry, not a gap this unit needs to close
   to be READY — but it is not yet reflected in this unit's OWN code-summary, only in the
   test file's docstring; noted as a Minor finding below.

4. **`_refuse_fixture_audit` / December — refusal is real, negative-controlled, and
   redundant with BLK-07.** `--audit` is refused twice, independently: `_require_december_
   authorization()` (BLK-07, unconditional, first statement of `_run_audit`) and
   `_refuse_fixture_audit` (only when `--fixture-manifest` is also given). Both paths were
   exercised directly (`test_audit_entry_point_refuses_naming_blk07`,
   `test_rec2_01_out_of_window_inventory_and_audit_refuse`). No path today lets `--audit`
   through regardless of fixture-manifest state.

5. **Free-text egress guard — safe interaction, no fail-open, no newly-refused legitimate
   row.** `_guard_free_text_egress` runs before every `append_registry_event` append and
   covers exactly `notes`/`reason`. This unit's `_registry_row` (`scripts/01_inventory_and_
   registry.py:330-358`) sets `notes` to the fixed literal `"inventory-and-registry run
   (P1-02)"` and `reason` only from `str(exc)` on this unit's own templated
   `IntegrityError`/`LockedTestError` messages (no external provider text, no credential-
   shaped content ever appears in either). Ran the full suite; `test_acquisition.py`'s
   printed egress-coverage derivation (`registry egress coverage derived: refused-by-egress
   ['notes', 'reason']; refused-by-schema ['status']; written unguarded [...]`) confirms the
   claimed coverage matches the code. No legitimate row from this unit is at risk of a false
   refusal, and no path bypasses the guard.

6. **TBD sentinels, scientific constants, credentials, weakened guards.** No TBD sentinel
   filled by this unit's code. `CELL_RULE_ID` is a rule IDENTIFIER (a string label), not a
   numeric scientific constant — consistent with the 2026-09-05 review's finding and D-33's
   own framing ("the rule's IDENTIFIER is validated here; its numeric consequences enter
   only through config"). No credential literal found in any touched or read file. No guard
   found weakened relative to the 2026-09-05 pass; `_guard_free_text_egress` is additive
   (new, not a replacement of a stronger check).

7. **Test run — exact counts, printed.** Environment: CPython 3.11.16 via the stdlib
   pytest stand-in at the scratch path (never called "pytest"; `pyyaml`/`numpy`/`tensorflow`
   unavailable, PyPI egress blocked, verified today).
   - This unit's modules: `test_station_registry` 29 passed; `test_experiment_registry` 49
     passed; `test_import_boundary` 6 passed; `test_december_audit` 62 passed — **146
     passed, 0 failed, 0 skipped, 0 errors** across the four.
   - Full repository suite (26 `test_*.py` modules present on disk today — Phase-2-only
     modules `test_rinex_schema`/`test_dcb_sign`/`test_hourly_target` do not exist yet, as
     expected for Phase 1): **1144 passed, 0 failed, 39 skipped, 0 errors**. All 39 skips
     are `pyyaml`/`numpy` import-unavailability skips on this clone (verified by message),
     none touching this unit's own modules.

### New findings (this pass)

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Minor | `src/data/registry.py:14-20`; `scripts/01_inventory_and_registry.py:21-23`; `src/data/config.py:561-568` (comment) | All three still assert "`configs/data.yaml` keeps its `TBD — freeze gate` sentinels" for "the coordinate-to-cell rule" collectively with stations/IGRF. This is now factually wrong for `cell_rule` specifically: D-33 (2026-09-10) transcribed it to `"floor-half-open-d1"`; only `stations` and `igrf_version` remain TBD. Functionally inert today (traced and reproduced in finding 2: `stations` still blocks unconditionally before `cell_rule` is read), but the docstrings now misdescribe the disk state across three separate files/representations. | On the next touch of any of these three files, narrow the claim to name `stations` and `igrf_version` only, and state `cell_rule`'s actual status (frozen under D-33, supervisor countersignature outstanding) rather than grouping it with the still-TBD fields. No code change required to reach READY. |
| 2 | Minor | `aidlc/.../inventory-and-registry/code-generation/code-summary.md` (this file, prior to this edit) | The known, test-file-disclosed asymmetry between script 00's real end-to-end `_stage_entry` invocation test and scripts 01/02/04's AST-wiring-only check (`tests/test_clean_run.py:1955-1959`) was not previously carried into this unit's own code-summary, only into the test file's docstring — a reader of this artifact alone would not know the coverage is narrower for script 01 than for script 00. | Recorded here now (finding 3 of the attack-point list above); no further action needed for READY since the asymmetry is honestly disclosed at its source and the wiring itself is simple, direct, and covered by real invocation of its two constituent calls. |

### Verdict

**READY.** Zero Critical, zero Major, two Minor (both documentation/disclosure gaps with
no runtime consequence, independently reproduced not to affect current behaviour). The
registry's `stations`-first refusal ordering was reproduced directly against today's actual
`configs/data.yaml` values and continues to refuse for the correct, named reason regardless
of `cell_rule`'s new frozen-but-uncountersigned state. The Board Rec 2 fixture/audit
exemption is fail-closed on every path exercised, including the December-audit combination,
and its one known test-coverage asymmetry against script 00 is disclosed at its source
rather than hidden. The new free-text egress guard in `experiment_registry.py` does not
interact adversely with this unit's registry writes (traced and confirmed by the suite's own
printed coverage derivation). Full suite re-run independently: 1144 passed, 0 failed, 39
skipped (all pre-existing import-unavailability skips), 0 errors; this unit's four test
modules: 146 passed, 0 failed, 0 errors.

### Coverage limits (this pass)

Read: this unit's own record directory; `configs/data.yaml`, `configs/experiment.yaml`
(referenced, not modified by this unit); `evidence/DECISIONS.md` D-33 through D-38;
`src/data/registry.py`, `src/data/inventory.py` (not re-read line-by-line this pass, no
change since 2026-09-05), `scripts/01_inventory_and_registry.py`,
`src/data/experiment_registry.py`, `src/data/acquisition.py` (diff only), `src/data/config.py`
(`REQUIRED_FIELDS_MAP` section); `tests/test_station_registry.py`,
`tests/test_experiment_registry.py`, `tests/test_import_boundary.py`,
`tests/test_december_audit.py`, `tests/test_clean_run.py` (Rec 2 section);
`governance-guards`/`acquisition` `construction/` directories were NOT read, per the
per-unit read-scope bound — the free-text guard's origin was verified only through the
diff and this unit's own consumption of it.
