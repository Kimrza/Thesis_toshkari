# Code Generation Questions — `regimes-diagnostics-reporting`

**Unit** `regimes-diagnostics-reporting` (Bolt 11) · **Kind** `library` · **Stage** `code-generation`

State on disk, verified 2026-09-06: `src/evaluation/` carries the siblings'
`guards.py`/`masks.py`/`metrics.py`/`bootstrap.py` (all built this session, reviewer READY);
this unit's `regimes.py`/`diagnostics.py`/`plots.py` and the render-guard module do not
exist. `configs/experiment.yaml` carries no `regimes` block — R-123's three thresholds
(quiet `Kp<4`, disturbed `Kp>=4`, storm `Kp>=5`), the −12 h/+24 h event window and D-13's
event/independence parameters are frozen values with no config home yet. The four analysis
notebooks do not exist; `notebooks/madrigal_phase1_coverage_audit.ipynb` still carries its
inline PROVISIONAL station constants (team.md § Code Style migration obligation: D-number
freeze FIRST, then migration). The nfr-design's ten render guards
(`src/evaluation/report_guards.py`, naming owed to 3.5) are fully specified; both SEC-R-02
producing halves now EXIST on disk (the sibling's `EstimandResult` records orientation/
weighting; the TEC-06 caveat field is emitted by `metrics.py`) — the refusals gain real
producing halves this pass. One Minor rides the terminal READY (the "TEC-06 'wherever
reported'" paraphrase-as-quote), recorded input only.

---

## Question 1
**The regime configuration has no config home.** R-123 mandates the classifier read its
thresholds and window from `experiment.yaml` via `ConfigSnapshot` — "encoding frozen
values, deciding nothing" — but no `regimes` block exists. The values are frozen upstream
(Vision §9.3's thresholds and window; D-13's event definition — contiguous `Kp>=5` — and
independence rule — >=24 h of `Kp<4`). Transcribe now?

A) Transcribe the `regimes` block into `experiment.yaml` — thresholds, window, D-13
   event/independence parameters, each citing its authority (Vision §9.3, D-13) via this
   unit's change record; the classifier asserts content against config, no literal in source
   > **Impact**: The classifier and `count_storm_events` are buildable and their boundary controls real; the transcription is a copy of frozen decisions under citation (the D-121 precedent). No scientific value is decided — a copy's exactness is the only new claim, and a test asserts it.

B) Leave the block absent — classifier and counting path refuse fail-closed naming the
   missing config; transcription under a later ruling
   > **Impact**: Every regime/breakdown path asserts only refusals; WS-19/TA-16 evidence unproducible; a second ruling owed for values already frozen.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the values are frozen in the governing documents and D-13; R-123's whole design assumes the config home exists; the copy is testable and the change record carries the citations.

[Answer]: A

## Question 2
**The four analysis notebooks are in this unit's owns list** (§12's `NN_topic.ipynb`
convention; R-131/TE §14: declaration helper first — dataset version, code commit, config
IDs, artifact IDs — imports from `src/`, no only-copy of governed logic, clear stop on
missing inputs; conclusion cells are registered surfaces). No notebook can execute here
(no jupyter, no kernel). Create them this pass?

A) Create all four as governed skeletons — declaration cell, `src/` imports, versioned
   artifact reads, explicit stop-with-message on missing inputs, registered conclusion
   cells; honest limit recorded: never executed on this clone
   > **Impact**: The owns list is delivered; the notebooks are runnable the day inputs exist; R-131's negative posture (no only-copy logic) is checkable by AST scan now. Cost: unexecuted cells until a real environment.

B) Defer the notebooks to a later pass; build only the three modules + guards + tests
   > **Impact**: The unit's produces are partially delivered; a later pass must re-open this unit for artifacts its plan already owed; the checklist's registered-surface enumeration has fewer real surfaces to bind.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — skeletons are cheap, testable by static scan, and deferring them re-opens the unit later for no gain.

[Answer]: A

## Question 3
**The coverage notebook's migration is owed and gated on a student act.** team.md § Code
Style: `notebooks/madrigal_phase1_coverage_audit.ipynb`'s inline station coordinates and
cell-selection rule (both §18.2 forbidden-choice items) are frozen as a D-number decision
FIRST; only then do the values move into `configs/data.yaml` and the cell-bounds logic into
`src/data/registry.py`, and the notebook gains its `NN_topic` position. The functional
design routes "the coverage notebook's home" to the gate. How does this pass handle it?

A) Gated step, the Step-7 pattern — the change record carries a PROPOSED D-number text
   freezing the inline constants (adopt or edit; no agent writes the register); when the
   developer reaches the migration step it checks `evidence/DECISIONS.md` on disk: if the
   D-number exists, the constants move to `configs/data.yaml` + `src/data/registry.py` and
   the notebook is renumbered; if absent, the step stops, nothing ticks, and the migration
   stays owed
   > **Impact**: The student act stays the gate; the migration executes the moment the freeze exists; nothing silently changes a scientific value. Identical to the models-and-baselines Step 7 mechanism (which correctly did not execute — D-27 was never reopened).

B) Out of scope this pass — the migration stays owed at team.md, untouched here
   > **Impact**: No gated machinery; the obligation stays prose; a later pass or foundation's next touch owns it.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the gated-step mechanism is proven (Step 7), costs one plan step, and converts a standing prose obligation into an executable, student-gated action.

[Answer]: A

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Q1 = A — **`regimes` block transcribed into `experiment.yaml`**: thresholds quiet `Kp<4`
  / disturbed `Kp>=4` / storm `Kp>=5`, event window −12 h/+24 h, D-13's contiguous-`Kp>=5`
  event definition and >=24 h-of-`Kp<4` independence rule — each citing Vision §9.3 / D-13
  via this unit's change record; the classifier asserts content from config, no threshold
  literal in source; a test asserts the copy.
- Q2 = A — **Four analysis notebooks created as governed skeletons** (`NN_topic.ipynb`):
  declaration cell first (dataset version, code commit, config IDs, artifact IDs), imports
  from `src/`, versioned artifact reads, explicit stop-with-message on missing inputs,
  registered conclusion cells; never executed on this clone, stated honestly.
- Q3 = A — **Coverage-notebook migration as a GATED step** (Step-7 mechanism): the change
  record carries a proposed D-number text freezing the inline station coordinates and
  cell-selection rule; the migration step checks `evidence/DECISIONS.md` on disk — if the
  D-number exists, constants move to `configs/data.yaml` + cell-bounds logic to
  `src/data/registry.py` and the notebook is renumbered; if absent, the step stops, ticks
  nothing, and the migration stays owed.
- Fixed context riding every step: the TEN render guards land in
  `src/evaluation/report_guards.py` (SD-R-01's table as reviewed READY, incl.
  `require_provenance_block` on W-3 AND W-5 and `require_lineage_caveat` on W-7 with
  "present" defined for figures); one classifier + one counting path in `regimes.py`
  (`RegimeError` declared there per R-01's any-future clause; `source`/`release_grade`
  required arguments; a provisional-Dst-derived input refuses naming D-11, the
  `.dst_summary.json` path in the fixture); December-blind by signature, storm counts READ
  from the registered pre-G-05 audit artifact, never recomputed (one counting path);
  `plots.py` presentation-only by signature, computes no reported quantity; the
  `ConclusionSurfaceArtifact` registry fail-closed (emission of an unregistered
  conclusion-bearing artifact refuses); RF-importance figures render only from
  `authoritative = false` metadata; the widening comparator has no registered surface;
  the claims-and-limitations checklist inspects exactly the registered set, with the
  hand-authored-prose residual stated, never claimed closed; the primary table co-reports
  the three difficulty controls and any baseline that beats the LSTM (binding honesty
  rule); Phase-2 described as fixed-protocol replication, never a second independent blind
  test; every claim bounded to D-8's frozen scope; tests in
  `tests/test_regimes_and_reporting.py` (R-132's one home) with per-entry controls for
  W-3/W-5/W-7/W-4; build set: `src/evaluation/{regimes,diagnostics,plots,report_guards}.py`,
  the checklist artifact/module, four notebooks, the config transcription, the change
  record, the test module; no commit; smoke via scratchpad 3.11.16 + shim, full pytest owed.
- Nothing discharged: WS-19, TA-16, TA-20 stay `Pending`; the five D-32 rows stay
  `not evidence` (approved, never run); BLK-03/04/08/09 open; both SEC-R-02 halves now have
  producing fields on disk but no refusal is claimed exercised on real data.

- Looks correct
- Request changes

[Answer]: Looks correct

---

## Plan Approval

The code-generation plan for `regimes-diagnostics-reporting` is at
`construction/regimes-diagnostics-reporting/code-generation/code-generation-plan.md` —
11 steps: change record + proposed D-number FIRST (1), regimes config transcription (2),
regimes.py with the one classifier + one counting path (3), report_guards.py with the ten
render refusals + the fail-closed conclusion-surface registry (4), diagnostics.py with the
primary table, breakdown family, quarantine and claims checklist (5), plots.py
presentation-only (6), four governed notebook skeletons (7), GATED coverage-notebook
migration on your D-number (8), test_regimes_and_reporting.py with the full control set (9),
smoke + regression + lint (10), governance stop (11).

- Approve Plan
- Request Changes

[Answer]: Approve Plan
