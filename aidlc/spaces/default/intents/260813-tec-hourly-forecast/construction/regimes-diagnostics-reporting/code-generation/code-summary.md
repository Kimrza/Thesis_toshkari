# Code Summary — `regimes-diagnostics-reporting`

**Unit** `regimes-diagnostics-reporting` (Bolt 11) · **Kind** `library` · **Stage** `code-generation`
**Plan**: `code-generation-plan.md` (11 steps; Steps 1–7, 9–11 executed; Step 8 GATED and NOT executed — precondition absent, see § Deviations)
**Receipted answers**: Q1 = A (regimes block transcribed), Q2 = A (four notebook skeletons), Q3 = A (gated migration).

## Sources

- Approved plan and receipted Q&A: `construction/regimes-diagnostics-reporting/code-generation/{code-generation-plan.md,code-generation-questions.md}` [Q1][Q2][Q3]
- Functional design: `construction/regimes-diagnostics-reporting/functional-design/` (R-123…R-132; W-1…W-10)
- NFR design: `construction/regimes-diagnostics-reporting/nfr-design/{security-design.md,logical-components.md}` (SD-R-01…SD-R-04; the ten render guards)
- Governing decisions: Vision §9.3 (thresholds, window), D-13, D-17, D-11, D-28, D-32, D-8 — cited, not decided
- Change record: `governance/CHANGE_RECORD_2026-09-06_R123_regimes_and_reporting.md` (written FIRST, Step 1)

## Files created (10) / modified (1)

| File | Lines | Content |
|---|---|---|
| `governance/CHANGE_RECORD_2026-09-06_R123_regimes_and_reporting.md` | 197 | Q1 transcription record; Q2 decision (notebook-name divergence from R-131's indicative names recorded); Q3's PROPOSED D-number text quoting the coverage notebook's Cell-3 constants verbatim (ARUC 40.286/44.086, BSHM 32.778987/35.022987, NICO 35.140989/33.396450; floor half-open cell rule), IGS-site-log validation named as the post-freeze obligation; honest limits |
| `configs/experiment.yaml` (modified) | 247 (was 212) | ONE `regimes` block: thresholds quiet `Kp<4` / disturbed `Kp>=4` / storm `Kp>=5`, window −12/+24 h, contiguous-`Kp>=5` event definition, ≥24 h-of-`Kp<4` independence, D-13 demotion threshold, `count_source` GFZ (D-11), `december_day_range: "TBD — freeze gate"` (Rec 15 — Student+Supervisor), `d17_quality_strata` citing D-17; nothing else touched; copy exactness test-asserted |
| `src/evaluation/regimes.py` | 607 | ONE classifier (`classify_hours`, December-blind by signature — params exactly `{kp, config}`), `count_storm_events` with the approved signature (`source`/`release_grade` required; non-GFZ / absent-or-TBD grade / Dst-derived input each raise `RegimeError` naming `.dst_summary.json`/D-11); registered-audit read path with the control-(31) divergence raise; `read_december_day_range` refuses on the TBD sentinel by field name |
| `src/evaluation/report_guards.py` | 519 (unchanged at iteration 2; 522 from the 2026-09-10 gate-reopened repair — see § Gate-reopened repair) | The TEN SD-R-01 guards exactly as reviewed READY (incl. `require_provenance_block` on W-3 AND W-5, presence then agreement; `require_lineage_caveat` on W-3/W-5/W-7, figure-"present" = caption/metadata — **the W-5 half of this claim was FALSE at iteration 1 and is true from iteration 2**: the call at `diagnostics.py:662` was added on the reviewer's Critical, see § Iteration 2 changes); `ConclusionSurfaceRegistry` fail-closed, write-once atomic; `emit_registered_artifact` as one register-then-write transaction |
| `src/evaluation/diagnostics.py` | 1434 (was 1394 at iteration 1; +41/−1; 1596 from the 2026-09-10 gate-reopened repair — see § Gate-reopened repair) | Primary table (three difficulty controls co-reported by construction; `beats_model` printed never judged; R-108 fields asserted present, never restated; TEC-06 caveat on IRI/GIM rows; tier-3 row; provenance block; `derived: true` on the §5.5 percentage reduction); breakdown family (D-17 bound from config; top-1%-removed sensitivity labelled; driver-identity caveat; machine-readable shortfalls; **from iteration 2:** TECU units asserted from the metrics artifact's metadata and printed as `units`, and the TEC-06 lineage caveat asserted on every IRI/GIM item in the payload tree, both at the W-5 producing path); DEC regime breakdown (registered count governs; computed count for divergence only); practical relevance (both §5.3 conjuncts, PC-09 ordering, honest demotion per R-128); Dst/RF quarantine (`authoritative = false` render refusal); claims-and-limitations checklist over the registered surface set (D-8/D-7/TC-12 prohibited rows, D-28 disclosure, Phase-2 replication statement, hand-authored-prose residual STATED, never claimed enforced), itself a registered surface |
| `src/evaluation/plots.py` | 271 | Presentation-only BY SIGNATURE (AST-verified: zero aggregation calls, zero arithmetic BinOps); source-data IDs stamped; lineage caveats carried into captions; WS-19-schema manifest through `require_registered_surface`; matplotlib lazy, absence refuses naming the pin surface |
| `notebooks/01_data_and_target_audit.ipynb` | 130 | Governed skeleton: declaration cell first, `src/` imports only, stop on missing inputs, registered conclusion cell, never-executed limit in cell 1 |
| `notebooks/02_processing_and_features_review.ipynb` | 119 | Same discipline |
| `notebooks/03_model_training_review.ipynb` | 120 | Same discipline |
| `notebooks/04_results_and_claims_review.ipynb` | 134 | Same discipline |
| `tests/test_regimes_and_reporting.py` | 1653 (was 1599 at iteration 1; +57/−3; 1810 with 88 test functions from the 2026-09-10 gate-reopened repair — see § Gate-reopened repair) | 82 test functions at iteration 2 (derived: `grep -c "def test_"` → 82; was 81) — classifier boundary controls; counting-path refusals; audit-divergence raise; December-blind signature control; the per-entry render-guard set for W-3/W-5/W-7/W-4; provenance-on-breakdown and scored-window-agreement controls; quarantine controls; checklist controls incl. planted-phrase prohibited-class detection and the stated residual; notebook static scans; AST no-threshold-literal / plots-compute-nothing / no-new-import-edge controls; must-NOT-fire controls; config re-read, never literal; synthetic year 2001 only |

## Key implementation decisions

1. **`RegimeError` not redeclared** — already at foundation's R-01 single declaration site (`src/data/config.py` ~275, in `__all__`); imported and re-exported, raise site here (the `FairnessError` precedent); identity test-asserted.
2. **Config delivery to a fixed signature**: `count_storm_events`' approved contract carries no config parameter and R-15 bars this unit reading `configs/` directly, so the resolved regime block is activated per run via `activate_regime_config(snapshot.experiment)`; an unactivated call refuses fail-closed. Recorded in docstring + change record — widening the approved signature would have been an unauthorised amendment.
3. **No threshold literal in source**: grep and an AST test (zero integer constants in {3, 4, 5, 12, 24} in `regimes.py`) both pass; thresholds live only in the transcribed config block under citation.
4. **One counting path preserved across the unit boundary**: reports READ the registered pre-G-05 audit count; the locally computed count exists only to raise on divergence (control 31).
5. **Fail-closed conclusion surface**: emitting an unregistered conclusion-bearing artifact refuses; the checklist enumerates exactly the registered set and STATES the hand-authored-prose residual.

## Test coverage summary

**Gate-reopened repair (2026-09-10): 88 test functions, 88 passed, 0 failed, 0 skipped —
see § Gate-reopened repair.** Iteration 2 (2026-09-07): 82 test functions, 82 passed, 0 failed, 0 skipped — see § Iteration 2 changes for the exact runner lines. Iteration 1, as recorded then: 81 test functions, all executed under the scratchpad Python 3.11.16 + pytest shim: **81 passed, 0 skipped, 0 failed** (first run 80/1 — the unit's own AST control caught a set-difference `-` operator in `plots.py`; rewritten to `set.difference()`, re-run green — the control worked). Regressions: `test_common_masks.py` 60/1/0, `test_bootstrap.py` 31/6/0 — unchanged. `compileall` OK; stdlib lint substitute CLEAN (4 over-length lines wrapped); ruff and full pytest owed (PyPI unreachable). **Smoke evidence only, never governed.**

## Deviations from the plan

- **Step 8 NOT executed (designed outcome)**: precondition checked on disk when reached — `evidence/DECISIONS.md` ends at D-32; no D-number dated on/after 2026-09-06 freezing the coverage notebook's constants exists. Nothing migrated; `madrigal_phase1_coverage_audit.ipynb`, `configs/data.yaml`, `src/data/registry.py` untouched; the proposed D-number text sits in the change record.
- `RegimeError` re-export (decision 1); `activate_regime_config` module-state delivery (decision 2); `december_day_range`/`d17_quality_strata` live inside the `regimes` block with sentinel/citation (required by R-124/R-127's config-bound mechanisms; values decided nowhere); configured breakdown/plot lists NOT added to config (gate-routed content; guards take the list as an argument); test-side stdlib YAML fallback parser (pyyaml uninstallable) documented as apparatus.
- graphify CLI not on PATH; direct-read orientation; graph stale for touched files.

## Open items routed to the gate

The proposed D-number for the notebook-constants freeze (Step 8's outcome); which December day range governs D-13's count (Rec 15 — Student+Supervisor; config sentinel refuses meanwhile); the five D-32 rows `not evidence`; FR-P1-05-14/-15 rowless; WS-19/TA-16/TA-20 `Pending` (TA-16's parse and the executed per-notebook stop owed to a kernel environment); the FR-P1-05-18 source-criterion advisory (reported, not fixed); the REQ-CLAIM-01 boundary-text amendment owed; the exploratory label's writer; placing `tests/test_regimes_and_reporting.py` inside §12 (a §12 amendment); the authoritative thesis-text surface (Student); `feature_set_id` supply on the comparison object (evaluation-and-comparison); the §5.5 re-citation (`TEC-14`, Open); full pytest + ruff owed; the governed commit (student's act, none made) citing D-13, D-17, D-11, D-28, D-32 plus the new D-number if adopted. BLK-03/04/08/09 open; G-05/G-06 `Blocked`; nothing discharged.

## Assumptions & Open Questions

None.

## Iteration 2 changes

**Trigger.** The adversarial review below (iteration 1) returned NOT-READY with ONE Critical —
`require_lineage_caveat` never called from the W-5 producing path `build_breakdown_artifact`,
and the test claiming to cover it calling the bare guard instead of the entry point — plus two
non-blocking suggestions. This is a targeted repair pass, 2026-09-07: nothing else was reworked,
no commit was made (the student commits), and nothing below is claimed discharged.

**Files changed** (derived from `git diff --numstat` against `HEAD`, printed before assertion;
identical to the delta against a pre-pass snapshot of the same two files):

| File | +/− | What changed |
|---|---|---|
| `src/evaluation/diagnostics.py` | +41 / −1 (1394 → 1434 lines) | New helper `_irigim_items` (L574): walks a breakdown `payload` tree and returns every mapping whose `benchmark_id` is in `EXTERNAL_COMPARATOR_IDS` or that carries `is_irigim_comparison` — the guard's own membership test, so no second copy of the rule. In `build_breakdown_artifact` (L598): `require_units(metrics_artifact, …)` at **L660**; `for item in _irigim_items(artifact["payload"]): require_lineage_caveat(item, surface=surface, kind="row")` at **L661–662**; the checked units value printed onto the artifact as `units` (never assumed); docstring extended to name both refusals. `require_lineage_caveat`'s signature and refusal semantics untouched; `build_breakdown_artifact`'s approved signature untouched. |
| `tests/test_regimes_and_reporting.py` | +57 / −3 (1599 → 1653 lines) | `test_per_entry_caveatless_gim_into_w5_raises` (**L915**) rewritten to push a caveat-less `C-01` row THROUGH `build_breakdown_artifact` and assert `RegimeError` naming `C-01` and "lineage caveat" from that entry point; a must-NOT-fire half (same payload WITH the caveat renders, row printed unchanged); a nested per-station `comparisons` placement of a caveat-less `B-01` row also refuses (the walker is the mechanism, not a top-level key); a non-IRI/GIM row without the sentence does NOT refuse. New `test_per_entry_unitless_metrics_artifact_into_w5_raises` (**L955**): units metadata absent → refuses naming TECU; `"TECU/10"` → refuses (not rescaled); TECU → renders with `units == "TECU"`. |

Record files (this file and the change record) are updated in place; `code-generation-plan.md`,
`code-generation-questions.md`, every `memory.md`, `requirements.md`, `configs/*` and
`evidence/DECISIONS.md` are untouched.

**Test results, exact runner lines** (scratchpad Python 3.11.16 + stdlib pytest stand-in; PyPI
unreachable so real `pytest`/`ruff` stay owed; **smoke evidence only, never governed**):

```
grep -c "def test_" tests/test_regimes_and_reporting.py      → 82   (was 81)
tests.test_regimes_and_reporting                              → 82 passed, 0 failed, 0 skipped
tests.test_common_masks tests.test_bootstrap                  → 91 passed, 0 failed, 7 skipped
                                                                (60+31 passed, 1+6 skipped — identical to iteration 1)
python -m compileall -q src/evaluation tests/test_regimes_and_reporting.py → OK
stdlib line-length scan (ruff limit 99, from pyproject.toml)  → 0 over-length lines in the two edited files
```

**How the Critical is closed.** The design's Called-by cell for `require_lineage_caveat` reads
"W-3, W-5, W-7" (`nfr-design/security-design.md:47`, Governance Rec 9); the W-5 call now exists
at `diagnostics.py:662` inside the one generic W-5 producing function, and the per-entry control
`security-design.md:81-85` mandates ("a caveat-less GIM comparison into W-5") now pushes the
violating row through that function (`tests/test_regimes_and_reporting.py:915`). The guard being
correct was already proven once; the guard being invoked at W-5 is now proven at the path
(`project.md` corrections `nfr-design:c58`/`c59`). The delivery line for `report_guards.py` in
§ Files above claimed "`require_lineage_caveat` on W-3/W-5/W-7" at iteration 1 while the code
contradicted it; the claim is true from this pass and the row is annotated rather than silently
left standing.

**Design reading behind the placement.** R-127 and `business-logic-model.md` § W-5 give breakdown
rows no `units` field of their own (the only "units" token in R-127 is the D-17 field name
`within_hour_spread_tecu`), and the breakdown's comparison rows live under `payload` with no
single mandated key (`rows`, `comparisons`, per-station sub-mappings). Hence: the lineage guard
walks the payload tree rather than trusting one key, and the units assertion at W-5 is made on
the metrics artifact's units metadata — the one object every breakdown value derives from and the
same object W-3 asserts — with the checked value printed onto the breakdown. No approved signature
widened; no scientific constant introduced.

**Suggestion 1 — `require_units` at W-5 (`security-design.md:48`): DONE**, as above (call at
`diagnostics.py:660`; per-entry negative control at `tests/…:955`). It is not a vacuous call: it
refuses a TECU-less or non-TECU metrics artifact at the breakdown path exactly as W-3 does at the
table path, and on today's real metrics artifact (which carries no units metadata — BLK-08) it
fires, which is the design's stated fail-closed cost, now at W-5 as well as W-3/W-6.
`scripts/07_evaluate_and_report.py` does not call the W-5 builders (grep), so no live path
changes behaviour.

**Suggestion 2 — AST call-graph test of documented "Called by" vs actual call sites: NOT ADDED,
derivation recorded instead.** The derivation was run (AST over `diagnostics.py`/`plots.py`,
documented sets parsed from `report_guards.py`'s module docstring, W-id → producing-function
mapping from `business-logic-model.md` § W-3…W-7), printed, and shows **4 further mismatches
outside this finding's scope**, none repaired here:

| Guard | Documented Called-by | Actual calling functions (AST) | Gap |
|---|---|---|---|
| `require_estimand_fields` | W-3, W-5 | `build_primary_table:L408` | **@ W-5: no call** in any W-5 producer |
| `require_registered_surface` | W-3, W-5, W-7, W-4 | `_conclusion_surfaces:L1017` (W-4), `plots.build_plot_manifest_entry:L134` (W-7) | **@ W-3, @ W-5: no call** in the table/breakdown builders — mapping-dependent: registration for those paths happens through `report_guards.emit_registered_artifact`, which the design may intend as the W-3/W-5 emission site; the docstring's Called-by does not say which |
| `require_derived_label` | W-5 | `build_primary_table:L415` (W-3), `practical_relevance_statement:L821` (W-6) | **@ W-5: no call**; the §5.5 derived reduction the design places on W-5 (item 9) is computed and labelled on the W-3 table path instead |
| `require_lineage_caveat`, `require_units`, `require_d17_bound`, `require_provenance_block`, `require_driver_caveat`, `require_complete_members`, `require_beats_model` | as documented | all documented W-ids have a call in that W-id's producer | none |

A robust version of the suggested test would therefore fail today on pre-existing drift whose
repair is a design-placement question (W-3 vs W-5 for the derived label and estimand fields; where
"registration" is called for W-3/W-5), not a targeted fix, and the test would have to encode a
W-id → function mapping the design leaves implicit. Adding a version that passes would mean
either editing the documented Called-by sets or exempting the four rows — both outside this
pass. **The four rows are routed to the reviewer and the gate as same-class residuals**, not
fixed and not claimed absent.

**Residuals I could not close in this pass, stated so they are not misread as closed:**

- The four Called-by mismatches above.
- The W-4 checklist's after-the-fact TEC-06 scan (`diagnostics.py` L1187–1189, "TEC-06 sentence
  on every serialized IRI/GIM comparison") reads `artifact.get("rows", artifact.get("comparisons"))`
  at the TOP level of each reported artifact, while `build_breakdown_artifact` emits comparison
  rows under `payload`. The render-time guard added here catches a caveat-less row at
  construction; the checklist's independent presence row would not see payload-nested rows on a
  breakdown. Not changed (outside the finding); recorded for the reviewer.
- Real `pytest`, `ruff`, and a governed-environment run stay owed; WS-19/TA-16/TA-20 stay
  `Pending`; BLK-03/04/08/09 open; G-05/G-06 `Blocked`; nothing discharged.

## Review

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-06T21:01:35Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | `src/evaluation/diagnostics.py:574-626` (`build_breakdown_artifact`, the W-5 producing path); `src/evaluation/report_guards.py:279-328` (`require_lineage_caveat`); `tests/test_regimes_and_reporting.py:915-919` | `require_lineage_caveat` is never called from the W-5 breakdown-producing path (`build_breakdown_artifact` is, by its own docstring at `diagnostics.py:585`, "the generic W-5 producing function", and calls `assert_breakdown_stamps`, `assert_headline_role`, `require_provenance_block`, and — when `per_station` — `require_driver_caveat`, but never `require_lineage_caveat`; a full grep of `diagnostics.py` for `require_lineage_caveat` returns exactly one hit, at line 409, inside the W-3 table-building function). Yet the consumed NFR design this unit is supposed to implement explicitly widens this guard to W-5: `nfr-design/security-design.md:47` states `require_lineage_caveat`'s Called-by column as "W-3, W-5, **W-7**" (Governance Recommendation 9, itself independently re-verified there as "VERIFIED, landed correctly" at line 309), and `security-design.md:81-85` names the mandated per-entry negative control set as "a caveat-less GIM comparison into W-5" alongside the W-3/W-7/W-4 controls. This unit's own `code-generation-plan.md` ground rules (line 23) and `code-summary.md`'s own delivery line ("`require_lineage_caveat` on W-3/W-5/W-7, figure-'present' = caption/metadata") both assert this was implemented — a claim the code contradicts. Worse, the test purporting to cover it, `test_per_entry_caveatless_gim_into_w5_raises` (`tests/test_regimes_and_reporting.py:915-919`), does not push a GIM-carrying row through `build_breakdown_artifact` (the actual W-5 entry point) at all; it calls `require_lineage_caveat(gim_row, surface="breakdown", kind="row")` directly as a bare function call, bypassing the entry point it claims to test. This is exactly the failure mode `project.md`'s own learned rule `nfr-design:c58` names ("a guard module alone fails open on a forgotten call... one negative control per public entry point pushes a violating input through THAT entry point") and the one `nfr-design:c59` extends ("a row whose other cells were derived buys false confidence in the carried cell"). The gap is reachable, not merely theoretical: the checklist's own scan at `diagnostics.py:1147-1149` iterates `artifact.get("rows", artifact.get("comparisons", ()))` across every "reported" artifact (which includes breakdowns) checking `benchmark_id in EXTERNAL_COMPARATOR_IDS` — the very code confirms breakdown artifacts are expected to carry IRI/GIM comparison rows at some point in this design. A breakdown built with an IRI/GIM row today would render with no `spatial_representativeness_sentence` check at construction time; only the after-the-fact W-4 checklist audit would (if run) catch it, defeating the render-time refusal SD-R-01/Rec-9 exists to provide, and the test suite reports 81/81 green while giving no actual coverage of this call site. | Add a `require_lineage_caveat(item, surface=..., kind="row")` call inside `build_breakdown_artifact` (or at every call site that assembles a `rows`/`comparisons` list on a breakdown artifact) for any item matching `EXTERNAL_COMPARATOR_IDS`, then rewrite `test_per_entry_caveatless_gim_into_w5_raises` to call `build_breakdown_artifact(...)` with a caveat-less GIM row embedded in its payload and assert the raise from that entry point, not from the bare guard function. |

### Verification run

```
cd "C:/Users/s_inv/Desktop/New folder/Th/Th-1"
PY=".../scratchpad/tec311/Scripts/python.exe"; SHIM=".../scratchpad/shim"

PYTHONPATH="$SHIM:." "$PY" "$SHIM/pytest.py" tests.test_regimes_and_reporting
  → 81 passed, 0 failed, 0 skipped   (matches the claimed count; does not surface finding #1 — see above)

PYTHONPATH="$SHIM:." "$PY" "$SHIM/pytest.py" tests.test_common_masks tests.test_bootstrap
  → 91 passed, 0 failed, 7 skipped (SKIP: numpy/yaml unimportable) — matches claimed 60/1 + 31/6

"$PY" -m compileall -q src/evaluation tests/test_regimes_and_reporting.py
  → COMPILE_OK

AST check, src/evaluation/plots.py: 1 BinOp total (a `ConclusionSurfaceRegistry | None` type
  annotation, BitOr — not arithmetic); Call-target names contain no aggregation function
  (sum/mean/average/median/std/var/reduce/np absent) → "computes no reported quantity" claim
  holds by this check.

grep RegimeError src/data/config.py → line 150 (__all__), line 275 (class RegimeError(IntegrityError))
  → single declaration site confirmed; src/evaluation/regimes.py imports it (line 70), does not
  redeclare it — decision 1 in § Key implementation decisions holds.

grep '\b(3|4|5|12|24)\b' src/evaluation/regimes.py → every hit is inside a docstring or an
  f-string error message citing Vision §9.3/D-13/TE §18.3; none is a bare code-level threshold
  literal → "no threshold literal in source" claim holds for this module.

grep '^## D-' evidence/DECISIONS.md → last entries D-31, D-32, then "D-1 addendum" (no new
  top-level D-number) → confirms the Step 8 gate precondition ("evidence/DECISIONS.md ends at
  D-32") and the resulting skip is accurate.

grep 'regimes:|quiet_kp_below|...|december_day_range|d17_quality_strata' configs/experiment.yaml
  → block present with quiet=4/disturbed=4/storm=5, independence=24, threshold=3,
  december_day_range: "TBD — freeze gate" — matches the design and R-124's refuse-on-sentinel
  behaviour in regimes.py:read_december_day_range.

grep for the ten report_guards.py functions inside diagnostics.py + plots.py call sites:
  require_provenance_block → lines 453 (W-3 table) and 623 (W-5 build_breakdown_artifact) — both
    present, matches "W-3 AND W-5" claim.
  require_lineage_caveat → diagnostics.py line 409 only (W-3); plots.py lines 179, 213 (W-7) —
    NEVER called inside build_breakdown_artifact (W-5) — see finding #1.
  require_registered_surface → plots.py:134 (W-7), diagnostics.py:977 (W-4 checklist) — both
    present; W-3/W-5 registration-adjacent calls not separately verified beyond scope of this
    finding.
  require_units → diagnostics.py lines 402 (W-3), 772/773 (W-6 practical relevance) — no hit
    inside build_breakdown_artifact (W-5), despite security-design.md:48 claiming "W-3, W-5,
    W-6" — same pattern as finding #1, at lower observed consequence (breakdown artifacts built
    here do not carry a `units` field to check), noted but not raised as a separate finding.

Read tests/test_regimes_and_reporting.py:915-919 directly — confirms the bare-function-call
  pattern described in finding #1 (no build_breakdown_artifact() call in that test).
```

### Suggestions (non-blocking)

- The `require_units` Called-by gap at W-5 noted above (security-design.md:48 claims it, code
  does not call it there) is the same category of docstring/code drift as finding #1 but at
  lower observed risk today since no breakdown artifact built by this unit's code currently
  carries a `units` field. Worth closing in the same pass as finding #1's fix, with its own
  per-entry negative control through `build_breakdown_artifact`, to avoid a second silent gap
  surfacing later the way finding #1's did.
- `report_guards.py`'s own module docstring "Called by" annotations (lines 17-39) should be
  treated as a live contract, not prose: consider a lightweight AST or call-graph test (in the
  spirit of `nfr-design:c59`) that fails when a guard's actual call sites diverge from its
  documented Called-by set, so a future drift is caught mechanically rather than by a human
  reviewer's grep.

## Review

**Verdict:** READY (superseded by the gate-reopened repair pass below — see
"Iteration 1 (gate-reopened repair attempt, 2026-09-10)")
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-06T21:23:48Z
**Iteration:** 2 (of the prior attempt — history below is unmodified)

### Iteration 1 finding disposition

**Finding 1 (Critical, `require_lineage_caveat` never called from the W-5 breakdown path) —
CONFIRMED REPAIRED, verified independently, not by trusting the described fix.**

- `git diff HEAD --numstat -- src/evaluation/diagnostics.py tests/test_regimes_and_reporting.py`
  → `41  1  src/evaluation/diagnostics.py` / `57  3  tests/test_regimes_and_reporting.py` —
  matches the summary's claimed delta exactly.
- Read `diagnostics.py:574-666` directly: the new `_irigim_items` helper (L574-595) walks
  the breakdown `payload` tree (mappings, lists and tuples; strings as leaves) using the
  guard's own membership test (`is_irigim_comparison` flag or `benchmark_id` in
  `EXTERNAL_COMPARATOR_IDS`); `build_breakdown_artifact` (L598-666) now calls
  `require_units(metrics_artifact, surface=surface)` at L660 and
  `for item in _irigim_items(artifact["payload"]): require_lineage_caveat(item, surface=surface, kind="row")`
  at L661-662, both **before** `return artifact`. Confirmed `EXTERNAL_COMPARATOR_IDS =
  ("B-01", "C-01")` in `src/evaluation/metrics.py:147` and that `require_lineage_caveat`'s
  own membership test (`report_guards.py:297-299`) is byte-identical in logic to
  `_irigim_items`'s — no second, divergent copy of the rule.
- Confirmed via `git diff HEAD -- src/evaluation/diagnostics.py` that no other line in
  `build_breakdown_artifact` or elsewhere changed beyond the two guard calls, the helper,
  the new `units` field, and docstring text — `build_breakdown_artifact`'s parameter list
  (`breakdown_id`, `metrics_artifact`, `mask`, `role_label`, `aggregation`, `per_station`,
  `payload`, `completeness_shortfalls`) and both guards' signatures
  (`require_units(mapping, *, surface)`, `require_lineage_caveat(item, *, surface, kind="row")`,
  `report_guards.py:279-281,331`) are unchanged — no approved signature was widened.
- **My own probe, independent of the repair's tests** (`PYTHONPATH=.` `python -c`, run
  against the real module, not a fixture copy): a caveat-less `C-01` row nested three
  levels deep (`{"per_station": {"ARUC": {"comparisons": [{"wrap": [row]}]}}}`) pushed
  through `build_breakdown_artifact` **raised `RegimeError`** naming `C-01` and "no
  lineage caveat"; the identical row carrying
  `metrics.SPATIAL_REPRESENTATIVENESS_SENTENCE` **rendered** with `units == "TECU"`; a row
  flagged `is_irigim_comparison=True` under a benchmark ID outside the named pair also
  **raised**. All three match the design's stated mechanism at arbitrary nesting depth,
  not only the depth the rewritten test happens to exercise.
- Re-read the rewritten test (`tests/test_regimes_and_reporting.py:915-973`) directly:
  `test_per_entry_caveatless_gim_into_w5_raises` now calls `build_breakdown_artifact(...)`
  (the actual W-5 entry point) with the violating row embedded in `payload`, not the bare
  guard — closing the exact defect iteration 1 named (`nfr-design:c58`). The new
  `test_per_entry_unitless_metrics_artifact_into_w5_raises` does the same for
  `require_units`, including the "rescaled-but-wrong-unit" negative case
  (`"TECU/10"` refuses, not silently rescaled).
- Ran the full suite and the two regression modules myself (below): counts match the
  summary's claims exactly (82 test functions, 82 passed; 91 passed / 7 skipped on the
  numpy/yaml-unavailable regression modules — unchanged from iteration 1).

**Verdict on finding 1: repaired as claimed, at the actual entry point, with no signature
change and no regression.**

**Suggestion 1 (`require_units` at W-5) — independently confirmed DONE**, same call site
and same per-entry negative control verified above.

**Suggestion 2 (AST Called-by drift test) — NOT ADDED; the derivation the repair recorded
instead is INCOMPLETE, and re-deriving it myself surfaces one of its four "same-class
residuals" as an unflagged Critical (finding 2 below) and elevates a second (finding 3).**
The repair's own table in § Iteration 2 changes correctly identifies that
`require_estimand_fields` and `require_registered_surface` have no call in any W-5
producer and that `require_derived_label` has no call in `build_breakdown_artifact`, but
frames all three as one undifferentiated "design-placement question," deferring the
judgement this stage's own dispatch brief asked for. Adjudicating each against the
functional design each one actually cites (not against the summary's own hedge) changes
the picture for two of the three — see findings 2 and 3.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 2 | Critical | `src/evaluation/diagnostics.py` (no breakdown-family producing function exists; `compute_member_metrics`/`derived_rmse_reduction`/`require_derived_label` called only at `diagnostics.py:406-415` inside `build_primary_table`, W-3, and once more at `diagnostics.py:821` inside `practical_relevance_statement`, W-6); `functional-design/business-logic-model.md:129` ("breakdown functions (W-5): ... RMSE + derived reduction, tier-3, driver-identity caveat emitted") and `:868` (mapping table row "unlabelled derived reduction" → "W-5 / R-127 ... **(34)**"); `functional-design/business-rules.md` R-127 point 1 (Rec 20: "the §5.5 metric set enters the configured breakdown list ... RMSE per member; the derived percentage reduction ... carrying an explicit `derived: true` label ... an unlabelled derived field fails, control (34)") | **The §5.5 metric set (RMSE per member, the `derived: true`-labelled percentage reduction, and the six supporting metrics) that R-127 explicitly and unambiguously assigns to the breakdown family (W-5) is not implemented on any breakdown path at all — not merely unguarded, but never computed there.** `compute_member_metrics` (the function that produces RMSE and the six §5.5 supporting metrics) and `derived_rmse_reduction` (the function that produces the `derived: true`-labelled percentage reduction `require_derived_label` checks) are each called from exactly two places in the whole file: inside `build_primary_table` (the W-3 table path) and, for the reduction alone, inside `practical_relevance_statement` (W-6). Neither is called from `build_breakdown_artifact` (the generic W-5 producing function this same repair pass just touched) or from any other function. `build_breakdown_artifact` takes an arbitrary caller-supplied `payload`, so even a future caller cannot obtain a correctly-labelled §5.5 metric row for a breakdown from this unit's own code — the building block R-127 point 1 requires does not exist, so control (34)'s stated risk ("a derived percentage-reduction field emitted without its explicit `derived: true` label") is not merely uncaught at W-5, it has no producing path to be caught at. This is not a disclosed gap: `code-summary.md`'s own Files table describes "`derived: true` on the §5.5 percentage reduction" only under "Primary table," lists the breakdown family's contents without it, and the "Open items routed to the gate" section names only an upstream *citation* gap (`TEC-14`, FR-P1-05-16's `[Vision §5.5]` re-citation) — never this implementation gap. The design citation is unambiguous and specific to this exact code shape (line 129's own W-5 node names "RMSE + derived reduction" as a W-5 output, and line 868 maps the unlabelled-derived-reduction risk to W-5/R-127 control (34) by name), so per this stage's own adjudication criterion this is the same failure class as iteration 1's Critical: a business-rule-mandated per-entry mechanism, cited with its own control number, absent from its producing path — here, absent as a producing path at all. | Add a breakdown-family function (or extend `build_breakdown_artifact`'s caller contract) that computes `compute_member_metrics`/`derived_rmse_reduction` per breakdown member, calls `require_derived_label` on the labelled reduction before packaging it into the breakdown payload, and add a per-entry negative control pushing an unlabelled reduction through that path — mirroring the W-3 pattern already built for `build_primary_table`. |
| 3 | Major | `security-design.md:51` (`require_registered_surface` Called-by "W-3, W-5, W-7, W-4") and `:115-123` (§ SD-R-03: "Registration is enforced at the producing path: emitting a conclusion-bearing artifact (table, breakdown, figure set, notebook conclusion cell) without registering it is a `require_registered_surface` refusal ... so the registry grows with the surface automatically"); `src/evaluation/diagnostics.py` (`build_primary_table` at L371, `build_breakdown_artifact` at L598 — neither calls `require_registered_surface` or any registration function; `require_registered_surface` is called only once, inside `_conclusion_surfaces`/the W-4 checklist path at L1017); `src/evaluation/report_guards.py:227` (`emit_registered_artifact` defined but, confirmed by grep of the whole `src/evaluation/` package, called nowhere) | **Neither of the two mechanisms the design names for enforcing registration "at the producing path" is invoked from the table (W-3) or breakdown (W-5) builders, so a table or breakdown can be built and emitted by this unit's own code today with no registration step at all** — contradicting § SD-R-03's stated architecture and this artifact's own Key Implementation Decision 5 ("Fail-closed conclusion surface: emitting an unregistered conclusion-bearing artifact refuses"), which is true only of the W-4 checklist-emission path, not of W-3/W-5 emission itself. The iteration-2 repair's own Suggestion-2 derivation (§ Iteration 2 changes) raised this exact gap for `require_registered_surface` but closed the question with "mapping-dependent — registration for those paths happens through `report_guards.emit_registered_artifact`, which the design may intend as the W-3/W-5 emission site; the docstring's Called-by does not say which." That hedge is empirically resolved, not merely undecided: `emit_registered_artifact` has zero call sites anywhere in `src/evaluation/` (confirmed by grep), so neither candidate mechanism actually runs at W-3/W-5 — the ambiguity was never "which of two mechanisms applies," it was "neither does." Consequence: the checklist (W-4) only inspects the registered set, so an unregistered table or breakdown reaching a reader is invisible to the very inspection SD-R-03's registered-surface design exists to guarantee ("a location added later is not automatically inspected" is exactly the gap SD-R-03 claims to close, and does not, at these two paths). Rated Major rather than Critical because (a) the gap is pre-existing design debt already partially surfaced by the repair's own derivation rather than newly introduced, and (b) unlike finding 2 it does not by itself cause a *wrong* value to render — it is a completeness/traceability gap in the registration net, not a silent incorrect claim. | Call `require_registered_surface` (or `emit_registered_artifact`, whichever the design intends — state which) from `build_primary_table` and `build_breakdown_artifact` at emission time, with a per-entry negative control (an unregistered table/breakdown artifact refuses) alongside the existing W-4/W-7 controls; if the intended mechanism differs from both, document it explicitly rather than leaving the Called-by column's claim unmet by either. |

### Verification run

```
git diff HEAD --numstat -- src/evaluation/diagnostics.py tests/test_regimes_and_reporting.py
  → 41  1  src/evaluation/diagnostics.py
    57  3  tests/test_regimes_and_reporting.py        (matches claimed delta exactly)

PYTHONPATH="$SHIM:." "$PY" "$SHIM/pytest.py" tests.test_regimes_and_reporting
  → 82 passed, 0 failed, 0 skipped                    (matches claimed 82; was 81 at iteration 1)

PYTHONPATH="$SHIM:." "$PY" "$SHIM/pytest.py" tests.test_common_masks tests.test_bootstrap
  → 91 passed, 0 failed, 7 skipped (numpy/yaml unimportable) — unchanged from iteration 1

"$PY" -m compileall -q src/evaluation tests/test_regimes_and_reporting.py
  → COMPILE_OK

grep -c "def test_" tests/test_regimes_and_reporting.py → 82   (matches claimed count)

Read tests/test_regimes_and_reporting.py:915-973 directly — confirms both new/rewritten
  tests push their violating input through build_breakdown_artifact (the real W-5 entry
  point), not through a bare guard call.

grep 'EXTERNAL_COMPARATOR_IDS\s*=' src/evaluation/metrics.py → ("B-01", "C-01") — matches
  the membership test _irigim_items and require_lineage_caveat both apply.

Independent probe (PYTHONPATH=. python -c ..., against the real modules, own fixtures not
  the test file's):
  - a caveat-less C-01 row nested under per_station -> comparisons -> a wrapping dict/list
    pushed through build_breakdown_artifact -> RegimeError raised, naming C-01 and "no
    lineage caveat".
  - the same row carrying the real SPATIAL_REPRESENTATIVENESS_SENTENCE constant -> renders,
    units == "TECU".
  - a row with is_irigim_comparison=True and an out-of-set benchmark_id, caveat-less ->
    RegimeError raised.
  All three confirm the fix at arbitrary payload nesting, not only the shapes the rewritten
  test itself exercises.

grep 'require_estimand_fields|require_registered_surface|require_derived_label|require_provenance_block'
  src/evaluation/diagnostics.py -n
  → require_estimand_fields: line 408 only (W-3). require_derived_label: lines 415 (W-3),
    821 (W-6) only. require_provenance_block: lines 453 (W-3), 663 (W-5) — both present,
    matching the design's already-widened Called-by for this guard.
    require_registered_surface: line 1017 only (inside _conclusion_surfaces, W-4).
  → confirms the repair's own derivation table for these four guards, and grounds
    findings 2 and 3 above.

grep 'compute_member_metrics' src/evaluation/diagnostics.py -n
  → defined at 259; called at 406 and 411, both inside build_primary_table. No call from
    build_breakdown_artifact or any other function — grounds finding 2.

grep 'emit_registered_artifact\(' across src/evaluation/*.py
  → one hit: the definition in report_guards.py:227. Zero call sites anywhere in the
    package — grounds finding 3's "neither mechanism runs" claim.

Read functional-design/business-logic-model.md:129,868 and functional-design/
  business-rules.md R-127 point 1 directly — both explicitly assign the §5.5 metric set /
  derived-reduction label (control (34)) to the breakdown family (W-5), grounding finding
  2's severity as the same class as iteration 1's Critical.

Read nfr-design/security-design.md:51,115-123 (§ SD-R-01 Called-by row; § SD-R-03) directly
  — both explicitly assign registration enforcement "at the producing path" to W-3 and W-5,
  grounding finding 3.
```

### Suggestions (non-blocking)

- The repair's own derivation for the four Called-by mismatches (§ Iteration 2 changes,
  Suggestion 2) is good practice — printed, evidenced, and honest about what it did not
  resolve — but treating all four as one undifferentiated "design-placement question"
  understates two of them. A future pass should adjudicate each mismatch against the
  specific functional-design citation it traces to (as this review did) before routing it
  to the gate as equally uncertain; `require_estimand_fields`'s W-5 gap remains a genuine
  Minor documentation drift (no rule in `business-rules.md` assigns an estimand-orientation
  check to breakdown rows, unlike R-127's explicit assignment of control (34) to W-5), and
  should not be conflated with findings 2 and 3 above.
- Building the AST/call-graph test iteration 1 suggested (still not added) would have
  caught finding 2 and 3's gaps mechanically rather than requiring a second human read of
  `business-logic-model.md`'s W-5 node and mapping table — worth prioritizing now that two
  of the four "residuals" the derivation surfaced turned out to be real defects rather than
  design ambiguity.

### Iteration 1 (gate-reopened repair attempt, 2026-09-10)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-10T06:26:46Z
**Iteration:** 1 of max 2 on the new (gate-reopened) attempt

**Scope.** Verifies the repair described in § Gate-reopened repair (2026-09-10) below
against the terminal NOT-READY of the prior attempt (iteration 2 above): Critical —
the §5.5 metric set (`compute_member_metrics`, `derived_rmse_reduction`) implemented
on no breakdown (W-5) path; Major — `require_registered_surface` never called from the
W-3/W-5 builders and `emit_registered_artifact` with zero call sites in
`src/evaluation/`; plus the two Called-by mismatches (`require_estimand_fields` @ W-5,
`require_derived_label` @ W-5).

**Verification performed (adversarial, evidence-grounded, not trusting the described fix):**

1. **§5.5 metric set derivation vs implementation.** Derived the required field set
   independently from `functional-design/domain-entities.md:170-174,359-362` and
   `functional-design/business-rules.md:517-523` (R-127 point 1): per member `rmse`; the
   derived relative summary `1 - RMSE_model/RMSE_reference` carrying an explicit
   `derived: true` label; and six supporting metrics `mae`, `median_absolute_error`,
   `mean_error_bias`, `r_squared`, `correlation`, `pct90_95_absolute_error`. Read
   `diagnostics.py:262-347` (`_percentile`, `compute_member_metrics`,
   `derived_rmse_reduction`) directly: every one of the eight field names is present,
   spelled identically to the design's own field names (no set difference). Read
   `diagnostics.py:747-824` (`build_member_metrics_breakdown`): computes
   `compute_member_metrics` for the model and every declared benchmark, computes
   `derived_rmse_reduction` per benchmark, calls `require_derived_label` on each
   reduction before packaging, and delegates to `build_breakdown_artifact` so the
   breakdown gets its stamps/provenance/registration. This is a genuine new producing
   path on W-5, not a relabelled W-3 call — `compute_member_metrics` and
   `derived_rmse_reduction` are unchanged pure functions now called from a second,
   independent site.
2. **`require_estimand_fields` / `require_derived_label` at the real W-5 entry point,
   derived from each control's own scope statement (c59), not narrative.**
   `nfr-design/security-design.md:46` states `require_estimand_fields`'s Called-by as
   "W-3 table, W-5 breakdowns" verbatim; `:54` states `require_derived_label`'s Called-by
   as "W-5" verbatim (its *mandated* home, per R-127 control (34)). Read
   `diagnostics.py:799-807` directly: `require_estimand_fields(row, surface=surface)` runs
   inside the `for row in rows` loop of `build_member_metrics_breakdown`, and
   `require_derived_label(reduction, surface=surface)` runs immediately after each
   `derived_rmse_reduction` call, before the reduction is placed in the payload. Both
   calls are on `build_member_metrics_breakdown` itself (the real W-5 entry point), not
   on a helper the entry point merely imports.
3. **`require_registered_surface` / `emit_registered_artifact` call sites.**
   `grep -n "emit_registered_artifact\|require_registered_surface" src/evaluation/*.py`
   (run directly, not taken from the summary) shows `emit_registered_artifact` now called
   at `diagnostics.py:379` (inside the new `_register_reported_artifact` helper) in
   addition to its pre-existing use in `plots.py:134` (W-7, untouched by this repair), and
   `require_registered_surface` called at `diagnostics.py:377` and `:390` — both inside
   `_register_reported_artifact`, which is itself invoked from `build_primary_table`
   (`:522`, the true last step of W-3) and `build_breakdown_artifact` (`:741`, the true
   last step of W-5, and therefore also of `build_member_metrics_breakdown` and
   `build_dec_regime_breakdown`, both of which delegate to it). Read
   `_register_reported_artifact` (`:350-390`) directly: a `None` registry hits
   `require_registered_surface(artifact_id, registry=None, surface=surface)` immediately,
   which raises `RegimeError` (registry-existence check fails first) — fail-closed, no
   silent skip. A non-`None` registry without `emit_path` calls `registry.register(...)`
   directly; with `emit_path`, `emit_registered_artifact` runs the register-then-write
   transaction; either way the function re-asserts with `require_registered_surface`
   afterward, so an artifact cannot leave registered-but-unguarded (a duplicate
   registration would already have raised inside `register`, and a missing registration
   would fail the final assert) — no path found that leaves a producing artifact
   unregistered.
4. **Six new negative controls, real entry points, not bare guards.** Read
   `tests/test_regimes_and_reporting.py:999-1127` directly:
   `test_member_metrics_breakdown_w5_producing_path`,
   `test_per_entry_fieldless_estimand_into_w5_raises`,
   `test_per_entry_unlabelled_reduction_into_w5_raises`,
   `test_per_entry_unregistered_table_emission_refuses`,
   `test_per_entry_unregistered_breakdown_emission_refuses`, and
   `test_w3_w5_emission_register_then_write` all call `build_member_metrics_breakdown`,
   `build_primary_table`, or `build_breakdown_artifact` directly — none calls a guard
   function in isolation for its assertion. `test_per_entry_unlabelled_reduction_into_w5_raises`
   monkeypatches `diagnostics.derived_rmse_reduction` itself (not `require_derived_label`)
   to strip the label, proving the guard is actually invoked on the real return value at
   the real call site, not merely proven correct in the abstract.
   **Reproduced independently** (real Python interpreter, not trusted from the summary):
   built a minimal stdlib-only stand-in for the subset of `pytest` this module uses
   (`raises`, `approx`, `fixture`, `monkeypatch`/`tmp_path` fixture support — PyPI
   unreachable in this environment, same constraint the repair itself recorded) against a
   cached CPython 3.11.16 (`uv python list` showed one already provisioned in this
   session's scratchpad), imported the real `tests/test_regimes_and_reporting.py` against
   the real `src/evaluation` package, and executed all discovered `test_*` functions:
   **88 passed, 0 failed, 0 errored out of 88 discovered** — matches the repair's claimed
   count and result exactly. `grep -c "def test_" tests/test_regimes_and_reporting.py` → 88
   (derived, not carried from prose).
5. **Disk-vs-claim reconciliation.** `wc -l src/evaluation/diagnostics.py
   src/evaluation/report_guards.py tests/test_regimes_and_reporting.py` → 1596 / 522 / 1810
   — matches the code-summary's claimed line counts exactly (the 1596/1597 reader
   off-by-one is a trailing-newline artifact of `wc -l`, not a discrepancy). `git log
   --oneline -1` → `0e002cd`, matching the summary's stated `HEAD`; `git status --short`
   shows the repair uncommitted alongside pre-existing modifications to `aidlc-state.md`,
   the audit shard, and `evidence/test_run_access_log.jsonl` not made by this pass — the
   summary's "no commit was made by this pass" claim holds (project.md `code-generation:c30`
   honoured: repository state re-verified at summary-writing time, not carried from an
   earlier read).
6. **Non-coupling / regression check.** `grep -n "diagnostics\.\|from src.evaluation" 
   scripts/07_evaluate_and_report.py` shows only `src.evaluation.masks` and
   `src.evaluation.metrics` imports — this unit's builders (`diagnostics.py`) are not
   called from that script, so the repair adds no new coupling and the fixtures-unit's
   board remediation (the unrelated `0e002cd` commit) is undisturbed. The pre-existing
   `require_provenance_block`/`require_units`/`require_lineage_caveat`/`require_driver_caveat`
   call sites and the W-3 estimand/units/beats-model/lineage/budget checks in
   `build_primary_table` are byte-for-byte unchanged except for the new
   `registry`/`emit_path` parameters and the `_register_reported_artifact` call appended
   at the end — confirmed by reading the full function (`:424-525`) rather than only the
   diff hunks, so no prior guard was silently narrowed or removed to make room for the new
   registration step.

**Findings:** none survive verification at Critical or Major severity. The two prior
terminal findings and the two Called-by mismatches are each closed at their real
producing/entry paths, confirmed by direct code reading, cross-reference against
`domain-entities.md`/`business-rules.md`/`security-design.md`'s own field names and
Called-by text, and independent test execution rather than by trusting the repair's own
narrative.

**Minor (non-blocking):** `build_claims_checklist` (W-4) — also named in
`security-design.md:51`'s Called-by for `require_registered_surface` — checks that its
*input* `conclusion_surface` is registered (`_conclusion_surfaces`,
`diagnostics.py:1163-1197`) but the checklist artifact it itself emits is not passed
through `_register_reported_artifact`; this is pre-existing scope (untouched by this
repair, and outside the Critical/Major this pass was dispatched to fix) and is noted for
a future pass rather than blocking this one.

### Summary

Both terminal findings from the prior attempt — the §5.5 metric set's absent W-5
producing path (Critical) and the unwired `require_registered_surface`/
`emit_registered_artifact` registration mechanism (Major) — are repaired at their real
call sites, independently verified against the functional design's own field names and
the security design's own Called-by text (not the repair's paraphrase of either), and
covered by six new per-entry negative controls that push violations through the actual
producing functions. All 88 test functions pass under an independently-reproduced run.
No new Critical or Major defect was introduced by the repair.

## Gate-reopened repair (2026-09-10)

**Trigger.** The owner reopened the stage gate (Request Changes, 2026-09-10) to repair the
iteration-2 review's standing terminal findings: **finding 2 (Critical)** — the §5.5 metric
set assigned to W-5 (`compute_member_metrics`, `derived_rmse_reduction`) implemented on no
breakdown path — and **finding 3 (Major)** — `require_registered_surface` never called from
the W-3/W-5 builders and `emit_registered_artifact` with zero call sites in
`src/evaluation/`, contradicting SD-R-03's producing-path registration mandate. The two
remaining Called-by mismatches from the iteration-2 derivation table
(`require_estimand_fields` @ W-5, `require_derived_label` @ W-5) are repaired on the same
surface. The gate rejection lifts the receipt freeze; this section is appended, the verdict
history above is not rewritten.

**Files changed** (derived from `git diff --numstat` against `HEAD` = `0e002cd`, printed
before assertion):

| File | +/− | What changed |
|---|---|---|
| `src/evaluation/diagnostics.py` | +171 / −9 (1434 → 1596 lines) | New `build_member_metrics_breakdown` — W-5 point 9's producing function (Rec 20): `compute_member_metrics` per member (RMSE + the six §5.5 supporting metrics) and `derived_rmse_reduction` per benchmark with its `derived: true` label, packaged as one stamped breakdown via `build_breakdown_artifact`; `require_estimand_fields` runs on every comparison row and `require_derived_label` on every reduction AT this W-5 entry point. New `_register_reported_artifact` — SD-R-03's producing-path registration, called from `build_primary_table` (W-3) and `build_breakdown_artifact` (W-5): registers the artifact (write-once), routes an `emit_path` through `emit_registered_artifact`'s register-then-write transaction, then asserts with `require_registered_surface`; a call without a registry refuses fail-closed. `build_primary_table`, `build_breakdown_artifact`, `build_dec_regime_breakdown` gain keyword-only `registry` / `emit_path` (default `None` → the designed fail-closed refusal, never a silent skip). Module docstring and per-function docstrings updated. |
| `src/evaluation/report_guards.py` | +4 / −1 (519 → 522 lines) | Module-docstring Called-by row for `require_derived_label` corrected to the live call set: W-5 (mandated home, from this pass) plus the pre-existing W-3/W-6 sites. No guard logic changed. |
| `tests/test_regimes_and_reporting.py` | +159 / −2 (1653 → 1810 lines; 88 test functions, was 82) | Six new per-entry controls (below); `_mem_registry()` apparatus (fresh write-once registry per build); existing successful builder call sites now pass `registry=` (raising call sites unchanged — every other guard runs before registration, so their raises still fire first). |

**How each finding is closed.**

- **Critical (§5.5 on no breakdown path)**: `build_member_metrics_breakdown` is the
  breakdown-family producing function the reviewer's recommendation names — it computes the
  §5.5 set per member ON the W-5 path and its `breakdown_id` enters the configured
  breakdown list, so point 8's inventory refusal reaches a missing metric row (asserted in
  the happy-path test). The paired loss differential remains the confirmatory estimand; the
  W-3 table's own §5.5 fields (W-3 point 7) are untouched.
- **Major (producing-path registration)**: the design's intended mechanism is stated per
  the recommendation: registration happens AT the builder (`registry.register`, or
  `emit_registered_artifact` when a file is emitted — giving it its first real call sites
  in `src/evaluation/`), and `require_registered_surface` then asserts it, so an artifact
  cannot leave W-3/W-5 registered-but-unguarded or guarded-but-unregistered (the nfr-design
  transaction note honoured). The registry grows with the surface automatically (SD-R-03
  consequence 2); Key Implementation Decision 5's claim is true of W-3/W-5 from this pass.
- **`require_estimand_fields` @ W-5**: called on every comparison row inside
  `build_member_metrics_breakdown` — the W-5 surface that renders estimand values, derived
  per c59 from the guard's own scope statement ("an estimand value without…"), not
  blanket-applied to payloads carrying none.
- **`require_derived_label` @ W-5**: called on every reduction inside
  `build_member_metrics_breakdown` before packaging (R-127 control (34)); no longer moot,
  because the Critical's repair gives it its producing path.

**New negative controls, each through the REAL entry point (c58):**

| Control | Entry point | Violation pushed |
|---|---|---|
| `test_per_entry_fieldless_estimand_into_w5_raises` | `build_member_metrics_breakdown` | a comparison row with `orientation` deleted |
| `test_per_entry_unlabelled_reduction_into_w5_raises` | `build_member_metrics_breakdown` | `derived_rmse_reduction` monkeypatched to drop the `derived` label |
| `test_per_entry_unregistered_table_emission_refuses` | `build_primary_table` | no registry supplied (fail-closed); must-NOT-fire half registers and renders |
| `test_per_entry_unregistered_breakdown_emission_refuses` | `build_breakdown_artifact` | no registry supplied (fail-closed); must-NOT-fire half registers and renders |
| `test_w3_w5_emission_register_then_write` | both builders with `emit_path` | duplicate emission refuses (write-once); file + registry entry asserted |
| `test_member_metrics_breakdown_w5_producing_path` | `build_member_metrics_breakdown` | must-NOT-fire happy path + the inventory refusal reaching `member_metrics` |

**Test results, exact runner lines** (scratchpad CPython 3.11.16 + stdlib pytest stand-in;
PyPI unreachable so real `pytest`/`ruff` stay owed; **smoke evidence only, never governed**):

```
grep -c "def test_" tests/test_regimes_and_reporting.py          → 88   (was 82)
tests.test_regimes_and_reporting                                  → 88 passed, 0 failed, 0 skipped
tests.test_clean_run                                              → 57 passed, 0 failed, 3 skipped
tests.test_common_masks + tests.test_bootstrap                    → 91 passed, 0 failed, 7 skipped (unchanged)
all 26 tests/ modules                                             → 947 passed, 13 failed, 15 skipped, 4 import errors
python -m compileall -q src/evaluation tests/test_regimes_and_reporting.py → OK
stdlib line-length scan (ruff limit 99)                           → 0 over-length lines in the three edited files
```

The 13 failures and 4 import errors (`test_external_drivers` 11, `test_iri_denial` 1,
`test_locked_test_guard` 1; import errors in `test_acquisition`, `test_december_audit`,
`test_determinism`, `test_experiment_registry`) were re-run with this repair stashed and
reproduce **identically without it** — pre-existing on `main` at `0e002cd`, owned by other
units' lanes, not introduced or touched here.

**Repository fact at summary-writing time** (c30): `git log -1` = `0e002cd` (an owner
commit for the fixtures unit's board remediation, made outside this pass); working tree
carries this repair uncommitted, plus pre-existing modifications to `aidlc-state.md`, the
audit shard and `evidence/test_run_access_log.jsonl` not made by this pass. **No commit was
made by this pass** — the governed commit remains the student's act.

**Plan state**: no step changed state (Steps 1–7, 9–11 remain executed; Step 8 remains
GATED and not executed — `evidence/DECISIONS.md` was not touched); the plan file is
therefore unannotated by this pass.

**Residuals, stated so they are not misread as closed:** the W-4 checklist's after-the-fact
TEC-06 scan still reads top-level `rows`/`comparisons` and would not see payload-nested
rows (recorded at iteration 2, unchanged); `scripts/07_evaluate_and_report.py` does not
call these builders (fixtures remediation respected — no coupling added); the four
`_checklist`-built tables register in per-call fresh registries, so a checklist's
`inspected_registered_set` in tests carries only the conclusion surface (apparatus, not a
claim); real `pytest`/`ruff` and a governed-environment run stay owed; WS-19/TA-16/TA-20
stay `Pending`; the five D-32 rows stay `not evidence`; BLK-03/04/08/09 open; G-05/G-06
`Blocked`; graphify CLI absent (`command not found`) so orientation was by direct reads and
the graph is stale for the touched files; nothing is discharged.

### Addition (2026-09-10, gate worklist item 1): W-4 registers its own emission

The fresh READY review noted that `build_claims_checklist` (W-4) verified its INPUT
conclusion surface was registered but never registered the checklist artifact it emits.
Repaired on the owner's worklist ruling, uncommitted in this pass's working tree:

- `src/evaluation/diagnostics.py`: `build_claims_checklist` gained `emit_path` and now ends
  with `_register_reported_artifact(checklist, ...)` — the SAME SD-R-03 register-then-write
  convention as W-3/W-5; `inspected_registered_set` is captured BEFORE the self-
  registration, so the checklist never inspects itself, and the docstring states both.
- `tests/test_regimes_and_reporting.py`: `test_checklist_emitted_as_registered_surface_
  write_once` reworked to the producing-path convention with the negative control through
  the real entry point (a second build of the same checklist id against the same registry
  refuses — NFR-AUD-01 once-only) and the must-not-fire half (the builder's own
  registration passes `require_registered_surface`);
  `test_checklist_inspects_exactly_the_registered_set` now asserts the before/after
  registry states. Module result on this clone: **88 passed, 0 failed, 0 skipped**
  (previously 82). The residual bullet above about per-call fresh registries is thereby
  PARTIALLY superseded: the checklist now registers itself; the TEC-06 payload-nesting
  residual is unchanged.

### Cleanup review (2026-09-10)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-10T07:38:23Z
**Iteration:** cleanup pass over the "Addition (2026-09-10, gate worklist item 1)" section
above, which postdates and was not covered by the "Iteration 1 (gate-reopened repair
attempt, 2026-09-10)" review earlier in this file.

**Scope.** Verifies today's W-4 self-registration addition to `build_claims_checklist`:
`inspected_registered_set` captured before self-registration, the checklist itself now
routed through `_register_reported_artifact`, and the two new/reworked tests
(`test_checklist_emitted_as_registered_surface_write_once`,
`test_checklist_inspects_exactly_the_registered_set`).

**Verification performed (adversarial, not trusting the described fix):**

1. Read `src/evaluation/diagnostics.py:1236-1238,1492-1516` directly. `registered_set =
   registry.ids() if registry is not None else ()` is assigned at line 1238, before any
   later code path — including the trailing `_register_reported_artifact(checklist, ...)`
   call at line 1510 — can register the checklist. The `inspected_registered_set` field
   written into the checklist dict at line 1496 is the pre-registration snapshot, so the
   claim "captured BEFORE its own registration" holds by direct read, not by trusting the
   docstring.
2. Read `_register_reported_artifact` (`:350-390`): a `None` registry raises via
   `require_registered_surface(artifact_id, registry=None, ...)` immediately (fail-closed,
   same mechanism already verified for W-3/W-5); a non-`None` registry without `emit_path`
   calls `registry.register(...)` (write-once, duplicate raises inside `register`); with
   `emit_path`, `emit_registered_artifact` runs register-then-write. `build_claims_checklist`
   calls this exactly once, at the end, after every row is built — no earlier return path
   bypasses it.
3. Reproduced independently (scratchpad CPython 3.11.16 + stdlib pytest stand-in,
   `pytest_standin/run_tests.py`, PyPI unreachable): `tests.test_regimes_and_reporting` →
   **88 passed, 0 failed, 0 skipped, 0 errors** — matches the addition's claimed count and
   the whole-module claim in the code-summary table exactly.
4. Read `test_checklist_emitted_as_registered_surface_write_once`
   (`tests/test_regimes_and_reporting.py:1598-1625`) directly: the negative control is a
   SECOND `_checklist(...)` build against the SAME registry and DIFFERENT `emit_path`,
   which must raise `RegimeError` — this exercises the real producing entry point
   (`build_claims_checklist`), not a bare call to `require_registered_surface` or
   `registry.register`. A second assertion additionally confirms the old bypass surface
   (`emit_registered_artifact` called directly against an already-registered ID) still
   refuses. The must-not-fire half (`registry.lookup("claims_checklist") is not None` plus
   `require_registered_surface(...)` passing, plus the emitted file's `artifact_class`)
   precedes the negative control in the same test, matching this project's affirmed
   practice of pairing every hard rule with both a must-fire and a must-not-fire proof.
5. Read `test_checklist_inspects_exactly_the_registered_set`
   (`tests/test_regimes_and_reporting.py:1450-1464`): asserts
   `tuple(checklist["inspected_registered_set"]) == before` (the pre-registration
   snapshot) and separately `set(registry.ids()) == {*before, checklist["artifact_id"]}`
   (the post-call registry state) — both directions of the "never inspects itself" claim
   are asserted, not merely described.
6. `git diff --stat -- src/` confirms only `src/evaluation/diagnostics.py` (+201/−? per
   the earlier full diff) and `src/evaluation/report_guards.py` (+5/−2, docstring only —
   no guard logic changed, confirmed by reading the hunk) changed in this unit's `src/`
   surface; `src/data/locked_test.py` (the locked-test guard) carries no diff at all.
7. Checked for scope creep: `build_claims_checklist`'s new `emit_path` parameter is
   keyword-only with a `None` default, so every pre-existing call site (including every
   test built before this addition) is unaffected; the `PROHIBITED_CLASS_ROWS`/disclosure
   scan logic above the registration call is byte-for-byte unchanged from the version the
   "Iteration 1 (gate-reopened repair attempt)" review above already verified.

**Findings:** none survive verification at any severity. The one item flagged as an open
residual by the prior review's Minor note ("the checklist artifact it itself emits is not
passed through `_register_reported_artifact`") is exactly what this addition closes, and
the closure is independently confirmed rather than taken on faith.

### Summary

The 2026-09-10 W-4 self-registration addition is verified against direct reads of
`diagnostics.py` and an independent 88/0/0 test execution: the checklist's inspected set is
captured strictly before its own registration, the registration itself runs through the
same fail-closed, write-once `_register_reported_artifact` convention already verified for
W-3/W-5, and both the must-fire and must-not-fire halves of the new negative control push
through the real `build_claims_checklist` entry point. No Critical, Major, or Minor defect
found in this addition.
