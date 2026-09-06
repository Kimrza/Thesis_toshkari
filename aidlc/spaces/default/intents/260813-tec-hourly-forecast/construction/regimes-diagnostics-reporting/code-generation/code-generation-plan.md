# Code Generation Plan — `regimes-diagnostics-reporting`

**Unit** `regimes-diagnostics-reporting` (Bolt 11) · **Kind** `library` · **Stage** `code-generation`
**Inputs**: `functional-design/` (R-123…R-132; W-1…W-10), `nfr-design/` (SD-R-01…SD-R-04, the TEN render guards; C/R components), `unit-of-work.md` § 11 (Owns: `src/evaluation/regimes.py`, `diagnostics.py`, `plots.py`, the four analysis notebooks, the claims-and-limitations checklist), `requirements.md` (11 carried IDs; 19 in the nfr coverage set). Consumed code: `src/evaluation/{guards,masks,metrics,bootstrap}.py`, `src/data/config.py` (`ConfigSnapshot`, exception hierarchy), `configs/experiment.yaml`.
**Answers (receipted)**: Q1 = A (regimes block transcribed), Q2 = A (four notebook skeletons), Q3 = A (coverage-notebook migration as a GATED step on a proposed D-number).
**Authority**: Vision §9.3 (thresholds, window), D-13 (event definition, independence, demotion), D-17 (sixteen-field breakdown bound), D-11 (no provisional-Dst figure in a G-05 regime count), D-28 (scored-window statement), D-32 (five rows approved, never run — `not evidence`), D-8 (claim boundary). G-05/G-06 `Blocked`; BLK-03/04/08/09 open.

## Ground rules binding every step

Same as prior units (3.11; in-place edits; no scientific constant in source — thresholds,
window, D-13 parameters, D-17 field list reach code ONLY from `configs/`/the registered
artifacts; two-tier errors; docstrings; ruff or substitute; a negative control per hard
rule; nothing discharged; smoke ≠ governed; **no commit**). Plus this unit's own: ONE
classifier and ONE counting path in `regimes.py` (`RegimeError` declared there per R-01's
any-future clause; `source` and `release_grade` required arguments; non-GFZ source, absent
grade, or a provisional-Dst-derived input each raise, the `.dst_summary.json` path named in
the fixture); December-blind by signature; regime PERFORMANCE breakdowns post-receipt by
construction; the storm count reaching any report is READ from the registered pre-G-05
audit artifact, never recomputed, with the audit-count consistency control raising on
divergence; `plots.py` presentation-only by signature (computes no reported quantity; axis
units and captions from artifact metadata); the ten render guards in ONE module with
per-entry controls (W-3 table, W-5 breakdowns, W-7 plots manifest, W-4 checklist);
`require_provenance_block` on W-3 AND W-5; `require_lineage_caveat` on W-3/W-5/W-7 with
"present" = caption or figure metadata; emission of an unregistered conclusion-bearing
artifact refuses (`ConclusionSurfaceArtifact`, fail-closed); RF-importance renders only
from `authoritative = false` metadata; the widening comparator has no registered surface;
the binding honesty rule (three difficulty controls co-reported in the primary table; any
baseline beating the LSTM appears in table AND abstract-level conclusion; `beats_model`
printed, never judged); Phase-2 replication statement carried as a field; every claim
bounded to D-8's frozen scope (ARUC 40/44, BSHM 32/35, NICO 35/33, 2022, December-only
test; no 5-minute NICO claim); no practical-relevance threshold introduced or
reinterpreted; hand-authored-prose residual stated, never claimed closed; notebooks hold no
only-copy of governed logic.

## Steps

- [x] **Step 1 — Change record FIRST: `governance/CHANGE_RECORD_2026-09-06_R123_regimes_and_reporting.md`** [Q1–Q3]
  Records the Q1 regimes transcription (a copy of Vision §9.3 / D-13 under citation), the
  Q2 notebook-skeleton decision, and Q3's GATED migration with a **proposed D-number text**
  freezing `madrigal_phase1_coverage_audit.ipynb`'s inline station coordinates and
  cell-selection rule (owner adopts or edits; no agent writes the register; validation
  against the official IGS site logs named as the post-freeze obligation). Honest limits
  (five D-32 rows `not evidence`; WS-19/TA-16/TA-20 `Pending`; both SEC-R-02 refusals never
  exercised on real data).

- [x] **Step 2 — Config transcription: `configs/experiment.yaml` gains `regimes`** [Q1 = A; R-123; TC-03e]
  Thresholds (quiet `Kp<4`, disturbed `Kp>=4`, storm `Kp>=5`), event window −12 h/+24 h,
  D-13 event definition (contiguous `Kp>=5`) and independence rule (>=24 h `Kp<4`), each
  citing Vision §9.3 / D-13 / the Step 1 record; the D-17 sixteen-field breakdown bound
  referenced by its decision, not re-enumerated as new content; nothing else touched.

- [x] **Step 3 — `src/evaluation/regimes.py` (new)** [R-123, R-124; W-1, W-2]
  The one classifier (thresholds/window from config; boundary-exact labelling) and
  `count_storm_events` (D-13 definition + independence; `source`/`release_grade` required;
  refusals per R-123; `RegimeError` declared here under R-01's any-future clause);
  December-blind by signature (no date filtering hidden inside; partition object in,
  labels out); the registered-audit read path with the count-consistency raise.

- [x] **Step 4 — `src/evaluation/report_guards.py` (new)** [SD-R-01's ten guards; Q2 = A at nfr-design]
  All ten refusals exactly as the READY table specifies, one module, distinct exceptions
  per the design (reusing the declared hierarchy; no new exception type beyond `RegimeError`
  in Step 3): `require_estimand_fields`, `require_lineage_caveat` (W-3/W-5/W-7; figure
  "present" = caption/metadata), `require_units`, `require_complete_members`,
  `require_d17_bound`, `require_registered_surface`, `require_beats_model`,
  `require_provenance_block` (W-3 AND W-5; presence then agreement),
  `require_derived_label`, `require_driver_caveat`. `ConclusionSurfaceArtifact` registry
  (fail-closed absence; registration enforced at every producing path; write-once
  atomic idiom).

- [x] **Step 5 — `src/evaluation/diagnostics.py` (new)** [R-125…R-130; W-3…W-6, W-8]
  The primary-table path (co-reported difficulty controls; `beats_model` printed;
  provenance block; sign-convention field asserted present, never restated; TEC-06 caveat
  on IRI/GIM rows; tier-3 row); the breakdown family (D-17 bound; §5.5 metric set with
  `derived: true` on the percentage reduction; driver-identity caveat; provenance block on
  every breakdown; top-1%-removed quality sensitivity per its rule); the quarantine
  (RF `authoritative = false` render refusal; Dst grade labels never crossing the lane);
  the claims-and-limitations checklist over the registered surface set (stdlib presence
  checks with stated limits; D-8 scope bounds; the prohibited-class rows incl. the D-28
  scored-set disclosure; Phase-2 replication statement field; honest-demotion path per
  R-128); the checklist ARTIFACT emitted as a registered surface itself.

- [x] **Step 6 — `src/evaluation/plots.py` (new)** [W-7; TS-R-02]
  Presentation-only by signature: prediction/residual/target-support/quality plot builders
  that consume registered artifacts, compute no reported quantity, stamp source-data IDs
  into captions/metadata, carry the lineage caveat into captions where the artifact carries
  it, and emit a plots manifest through `require_registered_surface`. Matplotlib imported
  lazily; absence refuses naming the pin surface (headless-safe; no display).

- [x] **Step 7 — Four analysis notebooks (new, governed skeletons)** [Q2 = A; R-131; TE §14]
  `notebooks/01_data_and_target_audit.ipynb`, `02_processing_and_features_review.ipynb`,
  `03_model_training_review.ipynb`, `04_results_and_claims_review.ipynb` (final numbering
  per §12's five-notebook scheme, leaving the coverage notebook's slot to Step 8): each
  opens with the declaration cell (dataset version, code commit, config IDs, artifact IDs),
  imports from `src/` only, reads versioned artifacts, stops with a clear message on
  missing inputs, holds no only-copy logic, and its conclusion cell registers as a surface.
  Never executed here — stated in each notebook's first cell and the summary.

- [ ] **Step 8 — GATED: coverage-notebook migration** [Q3 = A; team.md § Code Style; the Step-7 mechanism]
  **Precondition, checked on disk when reached**: `evidence/DECISIONS.md` carries a new
  D-number (dated on/after 2026-09-06) freezing the inline station coordinates and
  cell-selection rule. **If present**: constants move to `configs/data.yaml` (citing the
  D-number), cell-bounds logic to `src/data/registry.py` (in-place, flagged for
  foundation's record), the notebook renumbered into the §12 scheme with its inline copies
  removed (no only-copy rule). **If absent**: STOP at this step, tick nothing, report the
  absence; the migration stays owed. Nothing else waits on it.

- [x] **Step 9 — `tests/test_regimes_and_reporting.py` (new)** [R-132's one home; the unit's controls]
  Classifier boundary controls (a `Kp>=4` hour labelled quiet fails; wrong window fails);
  counting-path refusals (non-GFZ source, absent grade, provisional-Dst input naming
  `.dst_summary.json`); audit-count divergence raises; December-blind signature control;
  the per-entry render-guard set (field-less estimand into W-3; caveat-less GIM into W-5
  AND a caveat-less figure through W-7; unregistered artifact through W-7 and W-4;
  out-of-bound breakdown; missing `beats_model`; provenance block missing on table AND on
  breakdown; scored-window disagreement; unlabelled derived field; missing driver caveat);
  quarantine controls (RF figure without `authoritative = false` refuses; comparator has no
  registered surface); checklist controls (registered-set enumeration; prohibited-class
  rows; the hand-authored-prose residual STATED in the artifact, asserted present);
  notebook static scans (declaration cell first, no only-copy logic, `src/` imports only);
  must-NOT-fire controls (a complete, provenanced, caveated table renders; a GFZ-sourced
  graded count returns). Config values re-read, never literal; synthetic year only.

- [x] **Step 10 — Smoke + lint** — scratchpad 3.11.16 + shim; regression re-run of
  `test_common_masks.py` and `test_bootstrap.py`; `compileall`; stdlib lint substitute;
  ruff owed; exact results recorded.

- [x] **Step 11 — Governance stop before commit (student acts)**
  Step 1's record exists FIRST. Gate items: the proposed D-number for the notebook-constants
  freeze (Step 8's outcome either way); the five `not evidence` D-32 rows; WS-19/TA-16/TA-20
  `Pending`; the FR-P1-05-18 source-criterion advisory (reported, not fixed — a
  `requirements.md` change owed); the REQ-CLAIM-01 "tested on December 2022 only"
  boundary-text amendment owed (completed-stage artifact, not edited); the exploratory
  label's writer and §15.2 proposals as routed; commit citing **D-13, D-17, D-11, D-28,
  D-32** plus the new D-number if adopted. **No governed commit before the records exist.**

## Out of scope

Running any notebook; producing any real table/breakdown/figure (no metrics artifact
exists); the pre-G-05 December coverage audit (inventory-and-registry's); editing
`requirements.md` or any completed-stage artifact; the fixtures
(fixtures-and-reproducibility's); any acceptance-row discharge.
