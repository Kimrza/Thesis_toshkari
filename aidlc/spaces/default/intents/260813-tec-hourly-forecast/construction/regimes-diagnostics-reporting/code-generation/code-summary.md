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
| `src/evaluation/report_guards.py` | 519 (unchanged at iteration 2) | The TEN SD-R-01 guards exactly as reviewed READY (incl. `require_provenance_block` on W-3 AND W-5, presence then agreement; `require_lineage_caveat` on W-3/W-5/W-7, figure-"present" = caption/metadata — **the W-5 half of this claim was FALSE at iteration 1 and is true from iteration 2**: the call at `diagnostics.py:662` was added on the reviewer's Critical, see § Iteration 2 changes); `ConclusionSurfaceRegistry` fail-closed, write-once atomic; `emit_registered_artifact` as one register-then-write transaction |
| `src/evaluation/diagnostics.py` | 1434 (was 1394 at iteration 1; +41/−1) | Primary table (three difficulty controls co-reported by construction; `beats_model` printed never judged; R-108 fields asserted present, never restated; TEC-06 caveat on IRI/GIM rows; tier-3 row; provenance block; `derived: true` on the §5.5 percentage reduction); breakdown family (D-17 bound from config; top-1%-removed sensitivity labelled; driver-identity caveat; machine-readable shortfalls; **from iteration 2:** TECU units asserted from the metrics artifact's metadata and printed as `units`, and the TEC-06 lineage caveat asserted on every IRI/GIM item in the payload tree, both at the W-5 producing path); DEC regime breakdown (registered count governs; computed count for divergence only); practical relevance (both §5.3 conjuncts, PC-09 ordering, honest demotion per R-128); Dst/RF quarantine (`authoritative = false` render refusal); claims-and-limitations checklist over the registered surface set (D-8/D-7/TC-12 prohibited rows, D-28 disclosure, Phase-2 replication statement, hand-authored-prose residual STATED, never claimed enforced), itself a registered surface |
| `src/evaluation/plots.py` | 271 | Presentation-only BY SIGNATURE (AST-verified: zero aggregation calls, zero arithmetic BinOps); source-data IDs stamped; lineage caveats carried into captions; WS-19-schema manifest through `require_registered_surface`; matplotlib lazy, absence refuses naming the pin surface |
| `notebooks/01_data_and_target_audit.ipynb` | 130 | Governed skeleton: declaration cell first, `src/` imports only, stop on missing inputs, registered conclusion cell, never-executed limit in cell 1 |
| `notebooks/02_processing_and_features_review.ipynb` | 119 | Same discipline |
| `notebooks/03_model_training_review.ipynb` | 120 | Same discipline |
| `notebooks/04_results_and_claims_review.ipynb` | 134 | Same discipline |
| `tests/test_regimes_and_reporting.py` | 1653 (was 1599 at iteration 1; +57/−3) | 82 test functions at iteration 2 (derived: `grep -c "def test_"` → 82; was 81) — classifier boundary controls; counting-path refusals; audit-divergence raise; December-blind signature control; the per-entry render-guard set for W-3/W-5/W-7/W-4; provenance-on-breakdown and scored-window-agreement controls; quarantine controls; checklist controls incl. planted-phrase prohibited-class detection and the stated residual; notebook static scans; AST no-threshold-literal / plots-compute-nothing / no-new-import-edge controls; must-NOT-fire controls; config re-read, never literal; synthetic year 2001 only |

## Key implementation decisions

1. **`RegimeError` not redeclared** — already at foundation's R-01 single declaration site (`src/data/config.py` ~275, in `__all__`); imported and re-exported, raise site here (the `FairnessError` precedent); identity test-asserted.
2. **Config delivery to a fixed signature**: `count_storm_events`' approved contract carries no config parameter and R-15 bars this unit reading `configs/` directly, so the resolved regime block is activated per run via `activate_regime_config(snapshot.experiment)`; an unactivated call refuses fail-closed. Recorded in docstring + change record — widening the approved signature would have been an unauthorised amendment.
3. **No threshold literal in source**: grep and an AST test (zero integer constants in {3, 4, 5, 12, 24} in `regimes.py`) both pass; thresholds live only in the transcribed config block under citation.
4. **One counting path preserved across the unit boundary**: reports READ the registered pre-G-05 audit count; the locally computed count exists only to raise on divergence (control 31).
5. **Fail-closed conclusion surface**: emitting an unregistered conclusion-bearing artifact refuses; the checklist enumerates exactly the registered set and STATES the hand-authored-prose residual.

## Test coverage summary

**Iteration 2 (2026-09-07): 82 test functions, 82 passed, 0 failed, 0 skipped** — see § Iteration 2 changes for the exact runner lines. Iteration 1, as recorded then: 81 test functions, all executed under the scratchpad Python 3.11.16 + pytest shim: **81 passed, 0 skipped, 0 failed** (first run 80/1 — the unit's own AST control caught a set-difference `-` operator in `plots.py`; rewritten to `set.difference()`, re-run green — the control worked). Regressions: `test_common_masks.py` 60/1/0, `test_bootstrap.py` 31/6/0 — unchanged. `compileall` OK; stdlib lint substitute CLEAN (4 over-length lines wrapped); ruff and full pytest owed (PyPI unreachable). **Smoke evidence only, never governed.**

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

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-06T21:23:48Z
**Iteration:** 2

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
