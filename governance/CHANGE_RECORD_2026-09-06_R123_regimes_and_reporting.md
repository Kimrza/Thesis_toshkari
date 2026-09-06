# Change Record — 2026-09-06 — `regimes-diagnostics-reporting` code generation (R-123…R-132)

**Change ID:** `CR-2026-09-06-R123-REGIMES-AND-REPORTING` (proposed D-number pending owner
adoption — no agent writes `evidence/DECISIONS.md`)
**Unit:** `regimes-diagnostics-reporting` (Bolt 11, kind `library`) · **Stage:** `code-generation` (3.5)
**Receipted answers (code-generation-questions.md):** Q1 = A, Q2 = A, Q3 = A.
**Authority:** Vision §9.3 (thresholds, event rule, window); `evidence/DECISIONS.md` D-13
(event definition, independence, demotion threshold, count source), D-11 (provisional Dst
barred from any G-05 regime count), D-17 (target-row contract; observation-quality strata
fields), D-28 (2–31 December 2022, 30 days), D-32 (eight §15.2 rows approved, never run),
D-1 (coordinate-to-cell convention), D-31 (G-09 signed with §18.3 preconditions disclosed
unmet); `GOV-2026-08-28-FD-01` Recs 15/16/17/18/19/20/21/27/43 as landed in the unit's
functional design; nfr-design SD-R-01…SD-R-04 (terminal READY, 2026-09-05).

This record is written FIRST, before any config transcription or module creation in this
pass, per the approved plan's Step 1. It decides **no scientific value**: every number
below is a copy of an already-frozen decision under citation, exactly the D-121/D-122
transcription precedent (`configs/experiment.yaml` grids and estimand blocks).

---

## 1. Q1 = A — the `regimes` block transcribed into `configs/experiment.yaml`

`configs/experiment.yaml` gains one top-level `regimes` block. Every value is a copy:

| Field | Value | Frozen by |
|---|---|---|
| `thresholds.quiet_kp_below` | `4` (quiet: Kp < 4) | Vision §9.3 |
| `thresholds.disturbed_kp_min` | `4` (disturbed: Kp ≥ 4) | Vision §9.3 |
| `thresholds.storm_kp_min` | `5` (storm: Kp ≥ 5) | Vision §9.3 |
| `event_window.pre_hours` | `12` (−12 h) | Vision §9.3 storm event rule |
| `event_window.post_hours` | `24` (+24 h) | Vision §9.3 storm event rule |
| `event_definition` | contiguous interval of Kp ≥ 5 | Vision §9.3; D-13 |
| `independence_min_quiet_hours` | `24` (≥ 24 h of Kp < 4) | Vision §9.3; D-13 |
| `independent_storm_event_threshold` | `3` | D-13 |
| `count_source` | GFZ Kp / Hp60 at a recorded release grade; provisional Dst barred | D-13 "Source of the count"; D-11 |
| `december_day_range` | `TBD — freeze gate` | **routed, not decided** — Student + Supervisor gate item (`GOV-2026-08-28-FD-01` Rec 15; R-124/W-2 point 5) |
| `d17_quality_strata.fields` | `valid_observation_count`, `within_hour_spread_tecu`, `provider_dtec_summary` | D-17 § Observation-quality strata — **referenced by its decision, not re-enumerated as new content**; the sixteen-field row contract itself stays in D-17 |

The classifier and `count_storm_events` read these values through `ConfigSnapshot`
(`src/data/config.py`, R-15) — **no threshold, window, independence or count literal
exists in this unit's source** (TC-03e; FR-P1-05-18 clause 3 by construction). A test in
`tests/test_regimes_and_reporting.py` asserts the copy's exactness against this table —
the copy's exactness is the only new claim Q1 = A makes.

`december_day_range` carries the literal `TBD — freeze gate` sentinel: the *mechanism*
(the comparison count is taken over an explicitly configured, call-site-asserted December
day range) is built in this pass; the *value* is a Student + Supervisor freeze (D-13 is a
supervisor-countersigned demotion threshold; TE §18.3 forbids this stage filling it by
convenience). While the sentinel stands, the audit-count consistency path **refuses
naming the field** rather than defaulting.

## 2. Q2 = A — four governed notebook skeletons

Created as governed skeletons, per the approved plan's names:
`notebooks/01_data_and_target_audit.ipynb`, `02_processing_and_features_review.ipynb`,
`03_model_training_review.ipynb`, `04_results_and_claims_review.ipynb`.

*(R-131's own indicative names differ for 02–04 — `02_processor_verification`,
`03_features_and_splits_review`, `04_results_and_figures`. § Depth Q1 = B fixes that
intra-package names are indicative; the approved plan's names govern this pass and the
divergence is recorded here rather than silently resolved.)*

Each skeleton: first cell is the `src/` declaration-helper call (dataset version, code
commit, config IDs, artifact IDs — TA-16's machine-parsed header) and states the
never-executed limit; imports from `src/` only; reads versioned artifacts; stops with the
stated missing-input message before any later cell runs (REQ-ENG-12 "Run all" semantics by
construction); holds **no only-copy of governed logic** (TE §14, §7); its conclusion cell
registers as a `ConclusionSurfaceArtifact` surface (SD-R-03, Q1 = A at nfr-design).

**Honest limit:** no notebook is executed in this pass or on this clone — no Jupyter
kernel exists here. The skeletons are checkable by static scan only (R-131 controls (29)
mechanism and (30)), and control (29)'s *executed* per-notebook stop assertion remains
owed to an environment with a kernel. The migrated coverage notebook's home (W-9 proposes
`01_data_and_target_audit`; §12 fixes five notebooks and names no sixth) **stays routed to
the gate**.

## 3. Q3 = A — the GATED coverage-notebook migration, and the proposed D-number text

**Gate mechanism (the Step-7/models-and-baselines precedent):** when the migration step is
reached, `evidence/DECISIONS.md` is checked on disk for a D-number **dated on or after
2026-09-06** freezing the inline station coordinates and cell-selection rule of
`notebooks/madrigal_phase1_coverage_audit.ipynb`. If present, the constants move to
`configs/data.yaml` (citing that D-number), the cell-bounds logic to
`src/data/registry.py`, and the notebook is renumbered into §12's five-notebook scheme
with its inline copies removed. If absent, the step stops, ticks nothing, and the
migration stays owed at `team.md` § Code Style. **No agent writes the register.**

**Proposed D-number text (owner adopts or edits verbatim into `evidence/DECISIONS.md`):**

> ## D-3x — Coverage-notebook inline constants frozen for migration (freeze)
>
> **Decision.** The inline constants in `notebooks/madrigal_phase1_coverage_audit.ipynb`
> Cell 3 ("frozen station registry") are frozen, verbatim as they stand in the notebook,
> as the values the team.md § Code Style migration moves into `configs/data.yaml` and
> `src/data/registry.py`:
>
> | Station | `lat` | `lon` | Source note carried in the notebook |
> |---|---|---|---|
> | ARUC | `40.286` | `44.086` | "IGS network page — cross-check against site log required" |
> | BSHM | `32.778987` | `35.022987` | "IGS network page — cross-check against site log required" |
> | NICO | `35.140989` | `33.396450` | "IGS network page — cross-check against site log required" |
>
> and the coordinate-to-cell rule exactly as the notebook's `cell_bounds` function states
> it: a 1° × 1° cell identified by its lower-left floor corner,
> `cell = [floor(lat), floor(lat)+1) × [floor(lon), floor(lon)+1)`, half-open on both
> axes — self-labelled "PROVISIONAL" / "DEFAULT convention adopted here" in the
> notebook's own comments.
>
> **Relationship to D-1, stated so the freeze adds a record, not a number.** D-1 already
> froze the coordinate-to-cell convention and the station→cell table (ARUC 40/44,
> BSHM 32/35, NICO 35/33) with these same coordinates. This decision freezes the
> **notebook's inline copies as exact copies of D-1's values**, so the §18.2
> forbidden-choice items (station coordinates: Student; cell-selection rule: Student +
> Supervisor) migrate without any possibility of a silent value change. Any discrepancy
> found between the notebook's inline values and D-1 at migration time is surfaced and
> stops the migration rather than being resolved by an implementer.
>
> **Post-freeze obligation, named:** validation of all three coordinates against the
> official IGS site-log PDFs (the §6.2 evidence hierarchy's top rank) remains outstanding
> — carried from D-1's Known limitation — and must complete before the migrated values
> are treated as final. The migration itself does not discharge it.
>
> **Approved** — *date and signature are the owner's; nothing here is effective until
> recorded in `evidence/DECISIONS.md` by the owner.*

**Gate check outcome (recorded at Step 8):** see § 5 below.

## 4. What else this pass builds, under the already-approved design

- `src/evaluation/regimes.py` — the one hour-classifier and `count_storm_events` (the
  approved boundary signature, consumed exactly, **no signature amendment**); the
  registered-audit read path with the audit-count consistency raise (control (31)); the
  demotion-ordering assertion; the outside-scored-set exclusion (control (40)).
  **`RegimeError` declaration site, recorded:** `foundation`'s R-01 amendment ruled
  `src/data/config.py` the ONE declaration site, and `RegimeError` **already exists
  there** (its `__all__`, verified 2026-09-06). Exactly as `src/evaluation/guards.py`
  records for `FairnessError`/`InverseTransformError`, `regimes.py` therefore **imports
  and re-exports** `RegimeError` from the R-01 site rather than redeclaring it — a second
  class object with the same name would break catchability. This unit remains its raise
  site; the `domain-entities.md` § 5 "declared here" cell is discharged in that form, and
  the deviation is recorded here rather than hidden.
- `src/evaluation/report_guards.py` — SD-R-01's **ten** render guards, one module, plus
  the fail-closed `ConclusionSurfaceArtifact` registry (write-once atomic idiom;
  registration enforced at every producing path; emission of an unregistered
  conclusion-bearing artifact refuses).
- `src/evaluation/diagnostics.py` — the primary-table producing path, the breakdown
  family, the practical-relevance/post-access pair, the Dst/RF diagnostics quarantine,
  the claims-and-limitations checklist (itself a registered surface), and the notebook
  declaration helper.
- `src/evaluation/plots.py` — presentation-only by signature; manifest = WS-19's
  evidence schema; matplotlib imported lazily, absence refusing and naming the pin
  surface.
- `tests/test_regimes_and_reporting.py` — R-132's one home for controls (1)–(40)'s
  render-side set plus the must-not-fire controls. **Placing this module inside §12's
  tree remains a §12 amendment routed to the gate** (R-132's corrected precedent); the
  module exists beside §12's 21.

## 5. Honest limits — nothing below is discharged by this pass

- **Five D-32 rows are `Pending` — approved 2026-08-28, never run, NOT evidence**
  (FR-P1-05-16, -18, -19, -20, `REQ-CLAIM-01`/`TST-CLAIMS-01`). FR-P1-05-14 and
  FR-P1-05-15 remain genuinely rowless.
- **WS-19, TA-16, TA-20 stay `Pending`**; TA-19's supporting half likewise. No acceptance
  row is run, passed or discharged here.
- **Both SEC-R-02 refusals have never been exercised on real data** — the producing
  halves (`evaluation-and-comparison`'s `feature_set_id` supply is partial: the mask
  carries it, the comparison object's Rec 16 half stays named-not-annexed; the metrics
  artifact carries **no units metadata today**, so `require_units` fires on any real
  table until BLK-08's co-owner adoption lands). First failure is the mechanism working.
- **BLK-03 ↓, BLK-04 ↓, BLK-08 ↓, BLK-09 ↓ stay open exit conditions; G-05 and G-06 stay
  `Blocked`.** G-09 is signed (D-31) **with its TE §18.3 preconditions disclosed unmet**;
  that disclosure travels here.
- **Smoke ≠ governed:** the only interpreter available is a session-scratchpad
  Python 3.11.16 with a pytest stand-in shim (PyPI unreachable — pytest and ruff are not
  installable; `pyyaml` is absent there, so config-reading tests carry a documented
  stdlib fallback parser as test apparatus). Full `pytest` and `ruff` runs are owed to a
  governed environment; a stdlib lint substitute runs instead and its result is recorded
  in the stage summary.
- **The FR-P1-05-18 advisory NOT-READY stays reported, not fixed** (a `requirements.md`
  source-criterion change). **`REQ-CLAIM-01`'s "tested on December 2022 only" boundary
  text stays owed** an owner-approved annotate-in-place or §15.2 amendment — the
  completed-stage artifact is not edited here.
- **The exploratory label's writer** (registry surface) and **§15.2/§12 placement items**
  stay routed to the gate as the plan's Step 11 lists them.
- **No notebook is executed; no real table, breakdown or figure is produced** — no
  metrics artifact exists on this clone.

## 6. Step 8 gate check — outcome

*(Recorded when Step 8 was reached, same pass.)* `evidence/DECISIONS.md` was checked on
disk: the register ends at **D-32 (2026-08-28)** plus the D-1 addendum; **no D-number
dated on or after 2026-09-06 freezing the coverage notebook's inline constants exists.**
Precondition ABSENT → Step 8 stopped, nothing ticked, nothing migrated:
`notebooks/madrigal_phase1_coverage_audit.ipynb`, `configs/data.yaml` and
`src/data/registry.py` are untouched by this pass. The migration stays owed at `team.md`
§ Code Style, gated on the owner adopting § 3's proposed D-number (or an edited form).
