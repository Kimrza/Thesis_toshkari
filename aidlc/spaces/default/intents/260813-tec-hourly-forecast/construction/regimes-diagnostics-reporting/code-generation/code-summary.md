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
| `src/evaluation/report_guards.py` | 519 | The TEN SD-R-01 guards exactly as reviewed READY (incl. `require_provenance_block` on W-3 AND W-5, presence then agreement; `require_lineage_caveat` on W-3/W-5/W-7, figure-"present" = caption/metadata); `ConclusionSurfaceRegistry` fail-closed, write-once atomic; `emit_registered_artifact` as one register-then-write transaction |
| `src/evaluation/diagnostics.py` | 1394 | Primary table (three difficulty controls co-reported by construction; `beats_model` printed never judged; R-108 fields asserted present, never restated; TEC-06 caveat on IRI/GIM rows; tier-3 row; provenance block; `derived: true` on the §5.5 percentage reduction); breakdown family (D-17 bound from config; top-1%-removed sensitivity labelled; driver-identity caveat; machine-readable shortfalls); DEC regime breakdown (registered count governs; computed count for divergence only); practical relevance (both §5.3 conjuncts, PC-09 ordering, honest demotion per R-128); Dst/RF quarantine (`authoritative = false` render refusal); claims-and-limitations checklist over the registered surface set (D-8/D-7/TC-12 prohibited rows, D-28 disclosure, Phase-2 replication statement, hand-authored-prose residual STATED, never claimed enforced), itself a registered surface |
| `src/evaluation/plots.py` | 271 | Presentation-only BY SIGNATURE (AST-verified: zero aggregation calls, zero arithmetic BinOps); source-data IDs stamped; lineage caveats carried into captions; WS-19-schema manifest through `require_registered_surface`; matplotlib lazy, absence refuses naming the pin surface |
| `notebooks/01_data_and_target_audit.ipynb` | 130 | Governed skeleton: declaration cell first, `src/` imports only, stop on missing inputs, registered conclusion cell, never-executed limit in cell 1 |
| `notebooks/02_processing_and_features_review.ipynb` | 119 | Same discipline |
| `notebooks/03_model_training_review.ipynb` | 120 | Same discipline |
| `notebooks/04_results_and_claims_review.ipynb` | 134 | Same discipline |
| `tests/test_regimes_and_reporting.py` | 1599 | 81 test functions (derived: `grep -c "def test_"`) — classifier boundary controls; counting-path refusals; audit-divergence raise; December-blind signature control; the per-entry render-guard set for W-3/W-5/W-7/W-4; provenance-on-breakdown and scored-window-agreement controls; quarantine controls; checklist controls incl. planted-phrase prohibited-class detection and the stated residual; notebook static scans; AST no-threshold-literal / plots-compute-nothing / no-new-import-edge controls; must-NOT-fire controls; config re-read, never literal; synthetic year 2001 only |

## Key implementation decisions

1. **`RegimeError` not redeclared** — already at foundation's R-01 single declaration site (`src/data/config.py` ~275, in `__all__`); imported and re-exported, raise site here (the `FairnessError` precedent); identity test-asserted.
2. **Config delivery to a fixed signature**: `count_storm_events`' approved contract carries no config parameter and R-15 bars this unit reading `configs/` directly, so the resolved regime block is activated per run via `activate_regime_config(snapshot.experiment)`; an unactivated call refuses fail-closed. Recorded in docstring + change record — widening the approved signature would have been an unauthorised amendment.
3. **No threshold literal in source**: grep and an AST test (zero integer constants in {3, 4, 5, 12, 24} in `regimes.py`) both pass; thresholds live only in the transcribed config block under citation.
4. **One counting path preserved across the unit boundary**: reports READ the registered pre-G-05 audit count; the locally computed count exists only to raise on divergence (control 31).
5. **Fail-closed conclusion surface**: emitting an unregistered conclusion-bearing artifact refuses; the checklist enumerates exactly the registered set and STATES the hand-authored-prose residual.

## Test coverage summary

81 test functions, all executed under the scratchpad Python 3.11.16 + pytest shim: **81 passed, 0 skipped, 0 failed** (first run 80/1 — the unit's own AST control caught a set-difference `-` operator in `plots.py`; rewritten to `set.difference()`, re-run green — the control worked). Regressions: `test_common_masks.py` 60/1/0, `test_bootstrap.py` 31/6/0 — unchanged. `compileall` OK; stdlib lint substitute CLEAN (4 over-length lines wrapped); ruff and full pytest owed (PyPI unreachable). **Smoke evidence only, never governed.**

## Deviations from the plan

- **Step 8 NOT executed (designed outcome)**: precondition checked on disk when reached — `evidence/DECISIONS.md` ends at D-32; no D-number dated on/after 2026-09-06 freezing the coverage notebook's constants exists. Nothing migrated; `madrigal_phase1_coverage_audit.ipynb`, `configs/data.yaml`, `src/data/registry.py` untouched; the proposed D-number text sits in the change record.
- `RegimeError` re-export (decision 1); `activate_regime_config` module-state delivery (decision 2); `december_day_range`/`d17_quality_strata` live inside the `regimes` block with sentinel/citation (required by R-124/R-127's config-bound mechanisms; values decided nowhere); configured breakdown/plot lists NOT added to config (gate-routed content; guards take the list as an argument); test-side stdlib YAML fallback parser (pyyaml uninstallable) documented as apparatus.
- graphify CLI not on PATH; direct-read orientation; graph stale for touched files.

## Open items routed to the gate

The proposed D-number for the notebook-constants freeze (Step 8's outcome); which December day range governs D-13's count (Rec 15 — Student+Supervisor; config sentinel refuses meanwhile); the five D-32 rows `not evidence`; FR-P1-05-14/-15 rowless; WS-19/TA-16/TA-20 `Pending` (TA-16's parse and the executed per-notebook stop owed to a kernel environment); the FR-P1-05-18 source-criterion advisory (reported, not fixed); the REQ-CLAIM-01 boundary-text amendment owed; the exploratory label's writer; placing `tests/test_regimes_and_reporting.py` inside §12 (a §12 amendment); the authoritative thesis-text surface (Student); `feature_set_id` supply on the comparison object (evaluation-and-comparison); the §5.5 re-citation (`TEC-14`, Open); full pytest + ruff owed; the governed commit (student's act, none made) citing D-13, D-17, D-11, D-28, D-32 plus the new D-number if adopted. BLK-03/04/08/09 open; G-05/G-06 `Blocked`; nothing discharged.

## Assumptions & Open Questions

None.
