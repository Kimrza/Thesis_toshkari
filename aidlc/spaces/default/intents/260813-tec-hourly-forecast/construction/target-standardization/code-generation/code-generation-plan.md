# Code Generation Plan — `target-standardization`

**Unit** `target-standardization` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`
**Inputs**: `functional-design/` (W-1…W-7; R-64…R-73), `nfr-design/security-design.md` (SD-T-00…SD-T-06), `nfr-design/logical-components.md`, `unit-of-work.md` §5, `requirements.md`. Answers: Q1=A (`StandardizationError` declared), Q2=A (refuse to RUN while `qc_operations` is TBD) — receipted.
**Authority**: G-09 signed (D-31). `src/data/prepared.py`, scripts 02/03, and `tests/test_prepared_target_schema.py` (name per `CR-2026-08-22-TARGET-SCHEMA-TEST`) all tree-named — no naming amendment.

## Ground rules binding every step

Same as prior units (3.11 target; in-place edits; no scientific constant in source; two-tier errors; docstrings; ruff clean; negative control per hard rule; nothing discharged; smoke ≠ governed; **no git commit**). Plus this unit's own: **no standardized target is produced** (Q2=A refuse-to-RUN while the QC list is `TBD — freeze gate` — the refusal is the deliverable); Phase 1 only — **never** a DCB/STEC/mapping/satellite/arc field; the product is **location-sampled gridded VTEC**, never labelled receiver-specific station-observed; no numerical Phase-1/Phase-2 equivalence claim anywhere; **no `02a`/`02b` convention**; December never informs a threshold (D-19's basis is January–November by construction); the float diff tolerance is NOT chosen (fixture-manifest value, TE §15.2).

## Recorded input — nfr-design review Minors (human ruling 2026-09-05)

Record-only Minors ride this unit's terminal READY review (the re-dated interpreter-reachability note; banner corrections). No code step derives from them; quoted at the stage gate.

## Steps

- [x] **Step 1 — `StandardizationError` in `src/data/config.py` (in place)** [Q1=A; DISC-T-1]
  IntegrityError subclass, `__all__`, any-future clause. Raise contract for the QC gate: resource = `configs/data.yaml` `qc_operations`; expectation = **frozen under a D-number** (never mere non-emptiness — a list filled by convenience satisfies "non-empty" and is what §18.2 forbids).

- [x] **Step 2 — `src/data/prepared.py` (new)** [FR-P1-03-1/3/4, NFR-TDEF-01, NFR-DQ-01 production half; SD-T-01…SD-T-04; R-64…R-72; D-16, D-17, D-1, D-19]
  Standardization engine: the **closed four-transformation set** (UTC normalization; D-1 floor-rule half-open cell selection; D-16 median hourly aggregation; frozen QC ops) — a fifth transformation **fails**; an aggregation statistic that does not resolve to D-16 **fails**; Q2=A refuse-to-RUN gate (scope bound: target-producing runs only). **D-17 sixteen-field row contract** with schema check; `phase_id`/`source_id`/`target_definition_id` stamped on every artifact; **lineage-caveat COLUMN** on every row carrying the two disclosures (location-sampled gridded VTEC with its own `target_definition_id`; geometry/sampling-artefact statement), preserved through this unit's own write path (round-trip test); **excluded set asserted, never substituted** (a run finding a different set fails, does not adopt); D-19 support thresholds read from config **with their January–November basis carried** (never inlined, never December-informed); data-quality block (four contents; unexplained recorded AS unexplained); uncertainty budget **states its bounds rather than truncating**. No new package dependency — if a schema library seems needed, STOP and report to 3.2.

- [x] **Step 3 — `scripts/02_standardize_prepared_target.py` (new)** [W-1; §12/§13.2]
  Position 02, `--config configs/`, `--phase 1` (the ordinal collision with Phase 2's `02_build_vtec_target.py` is a recorded §12 defect — `--phase` disambiguates; nothing invented); six-step entry (`ensure_process_determinism` first, `assert_no_raw_fields` before first write); orchestrates Step 2; registry rows via foundation's writer; refusal path (QC TBD) exercised and its `aborted` row honest.

- [x] **Step 4 — `scripts/03_verify_processing.py` (new, Phase 1 scope)** [FR-P1-03-1 verification half; SD-T-03; W-2]
  **Value-level** closed-set diff against provider bytes showing only the documented transformations (schema-level comparison explicitly insufficient); float tolerance read from the fixture manifest — **unset → stop naming the TE §15.2 field**, never a `numpy.isclose` default; Phase 1 scope thinner than §12's prose (the four Phase-2 uncertainty contents barred — per functional-design's settlement); verification evidence written with the three IDs + caveat column.

- [x] **Step 5 — `tests/test_prepared_target_schema.py` (new, tree-named)** + unit tests
  Negative controls: fifth transformation fails; non-D-16 statistic fails; missing D-17 field fails (16 exactly — not 15, not 17); missing ID stamp fails; caveat column absent fails; round-trip preserves the column through this unit's operations; substituted excluded set fails; QC-TBD refusal fires naming field + expectation; receiver-specific label refused; D-19 threshold without basis refused; tolerance-unset stop.

- [x] **Step 6 — Full-suite smoke + lint** *(executed 2026-09-06: 726 passed, 2 skipped under 3.11.9 — smoke only; ruff check clean on all five touched files)* — green under 3.11.9 (smoke only); ruff clean on touched files.

- [x] **Step 7 — Governance stop before commit (student acts)** *(the stop is honoured: gate items restated verbatim in the code-generation report; nothing decided; NO commit made)*
  Gate items restated (none decided here): the D-17 **authority** question (assert against the authority, not only the config — R-20's shape); foundation's run-manifest **executed-scripts** field (owed dependency for the one-`02`-per-run assertion `fixtures-and-reproducibility` will write); the consumer half of the caveat contract (features-and-splits/reporting units); `unit-of-work.md` §5's stale "19" (annotate-in-place decision). Commit cites **D-16, D-17, D-19, D-1** as touched context. **No governed commit before the records exist.**

## Out of scope

Producing any standardized target (Q2=A), freezing the QC list or the diff tolerance (supervisor/fixture-manifest items), the consumer-side caveat failure check, `test_clean_run.py`'s one-`02` assertion (fixtures-and-reproducibility's), any Phase 2 target work, every acceptance-row discharge (TA-19 stays `Pending`; FR-P1-03-5 stays rowless; FR-P1-03-1 stays BLOCKED until the freeze).
