# Code Generation Questions — `statistical-inference`

**Unit** `statistical-inference` (Bolt 10) · **Kind** `library` · **Stage** `code-generation`

State on disk, verified 2026-09-06: `src/evaluation/` now carries the sibling's
`guards.py`/`masks.py`/`metrics.py` (built this session, reviewer READY), so the SD-S-02
shared-guard import has a real target. `configs/seeds.yaml` carries `bootstrap: 20221201`
(D-122). `configs/experiment.yaml` carries `estimand: "TBD — freeze gate"` and
`bootstrap: "TBD — freeze gate"` — the file's own header routes both to
"statistical-inference/evaluation-and-comparison" for transcription under a D-number.
Three scientific confirmations this unit's design expressly routes to you are still open:
the **interval method** (R-119, percentile proposed), the **block-resampling scheme**
(R-115, fixed non-overlapping 24-hour partition proposed; Rec 26), and the **correlation
series** (R-121, proposed). TE §18.3: if 3.5 is reached with any unconfirmed, the posture
is stop-and-report — which is why they are questions here, not defaults.

**Recorded input**: this unit's terminal nfr-design READY (2026-09-05, two passes) closed
its Major (the mask-vs-member check now lives in the sibling's sixth guard,
`require_mask_member_alignment` — verified present in `src/evaluation/guards.py` this
session). One cosmetic Minor rides (the delegation sentence describes rather than names the
sixth guard). The sibling's half of the entry-point contract — naming
`vector_block_bootstrap` among its guarded entry points — stays OWED at the sibling's next
touch; this unit's half (per-entry controls through `vector_block_bootstrap`) is built in
`tests/test_bootstrap.py` this pass, and no completed sibling artifact is edited.

---

## Question 1
**The interval method is a scientific protocol value, unconfirmed.** TE §13.6 says "report
95% confidence intervals" and names no construction method; percentile/basic/BCa differ
materially on 10,000 replicates of a skewed statistic. R-119 proposes the **percentile
interval** (2.5th/97.5th of the replicate set — exactly re-derivable from WS-17's hashed
replicate vector) and routes the confirmation to you. Confirm?

A) Confirm the percentile interval now — recorded in this unit's change record with a
   proposed D-number text for `evidence/DECISIONS.md` (you adopt or edit), transcribed into
   `experiment.yaml`'s bootstrap block beside the 0.95 level; the interval component reads
   the method from config and a later change is a visible protocol change
   > **Impact**: The interval component is buildable and testable against a confirmed method; WS-17's replicate-hash evidence suffices to re-derive the interval. Honestly stated: this is the student/supervisor confirmation R-119 routes to the gate, made under the recorded owner-equivalence; no supervisor signature artifact exists or is claimed.

B) Leave unconfirmed — the method-parametric component is built, `experiment.yaml` keeps no
   method value, and interval construction refuses fail-closed naming the config field
   (R-119's control (18)); the confirmation lands under a later ruling
   > **Impact**: No scientific value is confirmed this pass; every interval-dependent test asserts only the refusal; WS-17/TA-14 evidence stays unproducible until a second ruling.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — percentile is the only method exactly reproducible from the replicate set alone (keeping WS-17's evidence sufficient), it was the proposal the READY design carried through two review passes, and the method-parametric component means a later BCa ruling changes one component, not the unit.

[Answer]: A

## Question 2
**The block-resampling scheme is proposed, not decided** (R-115; Rec 26 made it an explicit
gate item). Proposed: a **fixed non-overlapping 24-hour partition** of the scored window,
aligned over `features-and-splits`' folds/embargo, each block carrying all three stations
together (the vector property, TC-19). Confirm?

A) Confirm the fixed non-overlapping 24-hour partition now — same change record + proposed
   D-number; the block-grid builder implements it with R-115's boundary-violation raises
   > **Impact**: The grid is buildable and its negative controls real; 720 hours divides exactly into 30 blocks on the D-28 window (and the 48-hour sensitivity into 15), which is the arithmetic D-28 itself cites. Same honesty statement as Q1.

B) Leave proposed — the grid builder refuses fail-closed naming the unconfirmed scheme
   > **Impact**: The heaviest-CPU component of the pipeline stays unbuildable-in-effect; the widening guard and sensitivity have no grid to run on; a second ruling owed.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the proposal is the only scheme consistent with the frozen 24-hour block length, the vector property, and D-28's own divisibility argument; nothing else was ever on the table in the governing documents.

[Answer]: A

## Question 3
**The correlation series is proposed, not decided** (R-121). Proposed: the cross-station
**paired-error correlation** — Pearson correlation of the per-hour paired loss differences
(benchmark minus model) between each station pair, all three pairs, computed on the same
masked rows the estimand uses, reported alongside the interval (and inside R-120's failure
disclosure, where it is the discriminating quantity). Confirm?

A) Confirm the paired-error-difference series now — same change record + proposed D-number;
   R-121's emission and R-120's disclosure both read from it
   > **Impact**: The widening guard's disclosure carries its discriminating quantity; the mandated "cross-station paired-error correlation reported" (team.md § Mandated, TE §13.6) becomes a computed field. Same honesty statement as Q1.

B) Leave proposed — correlation emission refuses fail-closed; the disclosure ships without
   its discriminating quantity until a later ruling
   > **Impact**: R-120's failure disclosure is structurally incomplete (its most informative field absent); a second ruling owed.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the mandated rule already names "the cross-station paired-error correlation reported"; the proposal only fixes the operational series (per-hour paired differences, all three pairs), which is the reading the whole R-120 variance argument is built on.

[Answer]: A

## Question 4
**Config transcription scope.** `experiment.yaml` carries `estimand: "TBD — freeze gate"`
and `bootstrap: "TBD — freeze gate"`; the header routes both to this unit and the sibling.
The bootstrap parameters are already frozen (24-hour blocks, 10,000 replicates, seed key
`seeds.bootstrap` = 20221201 under D-122, 95% level, 48-hour sensitivity — TE §13.6, TC-19),
and the estimand's orientation/weighting are frozen (Vision §2.3, TE §1.3, already encoded
in the sibling's `EstimandResult`). What is transcribed this pass?

A) Both blocks — `bootstrap` (frozen values + the Q1–Q3 confirmations, citing TE §13.6 /
   TC-19 / D-122 / the change record) and `estimand` (orientation `benchmark_minus_model`,
   weighting `equal_station`, the sign sentence, citing Vision §2.3 / TE §1.3), each value
   citing its authority; nothing either authority does not fix is written
   > **Impact**: The four-config zero-TBD preflight moves two fields closer to passable; both blocks are copies of frozen decisions under citation (the D-121/seeds.yaml precedent); the sibling's code already asserts the estimand values, so drift between config and code is caught by test.

B) `bootstrap` only — `estimand` stays TBD for a separate evaluation-and-comparison ruling
   > **Impact**: One more ruling owed later for values that are already frozen and already enforced in code; the preflight keeps failing on `estimand`.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — both are transcriptions of already-frozen text under citation, exactly the class the header anticipates; leaving `estimand` TBD buys a second ruling for nothing new.

[Answer]: A

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Q1 = A — **Percentile interval confirmed**: 2.5th/97.5th percentiles of the 10,000
  replicate statistics; recorded in the change record with a proposed D-number text for
  `evidence/DECISIONS.md` (you adopt or edit); transcribed into `experiment.yaml` beside the
  0.95 level; the interval component reads the method from config (a later BCa ruling
  changes one component).
- Q2 = A — **Fixed non-overlapping 24-hour partition confirmed** as the block-resampling
  scheme (Rec 26 gate item closed by your ruling); each block carries all three stations
  together; R-115's boundary-violation raises implemented; 30 blocks on the D-28 window,
  15 at the 48-hour sensitivity.
- Q3 = A — **Cross-station paired-error correlation series confirmed**: Pearson correlation
  of per-hour paired loss differences (benchmark minus model) per station pair, all three
  pairs, on the estimand's masked rows; emitted beside the interval and inside R-120's
  failure disclosure.
- Q4 = A — **Both config blocks transcribed**: `bootstrap` (24-hour blocks, 10,000
  replicates, seed key `seeds.bootstrap` / D-122, 0.95 level, 48-hour sensitivity, plus the
  Q1–Q3 confirmed values, citing TE §13.6 / TC-19 / D-122 / the change record) and
  `estimand` (orientation `benchmark_minus_model`, weighting `equal_station`, the sign
  sentence, citing Vision §2.3 / TE §1.3). Nothing either authority does not fix is written.
- Fixed context riding every step: seed 20221201 read ONLY from `seeds.yaml` via
  `ConfigSnapshot` (ADR-05 carve-out — `seed_everything` never touches it), passed as a
  required parameter, `TypeError` by signature when absent; PCG64 generator with
  seed-sequence spawns (child 0 = 48-hour sensitivity, child 1 = widening comparator);
  SD-S-01 replicate hash over raw IEEE-754 bytes with the four canonical-form facts recorded
  beside it in `BootstrapResult`; preconditions via the sibling's `src/evaluation/guards.py`
  (SD-S-02, intra-package import — this unit's per-entry controls in `test_bootstrap.py`;
  the sibling's naming of `vector_block_bootstrap` stays OWED at its next touch, no
  completed sibling artifact edited); local `BootstrapError` refusals (block-grid violation,
  unhandled missing pair, unconfirmed method, fixture-time widening raise); the widening
  comparator exact and quarantined (never serialized as a reported interval; guard evidence
  only; real-data failure = mandatory machine-readable disclosure carrying the Q3
  correlations); replicate vector materialised in full (80,000 bytes, printed); numpy
  imported lazily, absence refuses naming the `numpy==1.26.4` pin (the sklearn/FU-1
  precedent); build set: `src/evaluation/bootstrap.py`, `tests/test_bootstrap.py`, the
  config transcription, the change record; runs inside script 07, owns no stage script; no
  commit; smoke via the scratchpad 3.11.16 + shim, full pytest owed.
- Nothing discharged: WS-17, TA-13, TA-14, TA-26 stay `Pending`; BLK-08's ABL-DIFF limb
  stays open (D-27 unreopened); the G-06 abort policy for a failed widening comparison stays
  owed to the Supervisor at G-05 (Rec 23).

- Looks correct
- Request changes

[Answer]: Looks correct

---

## Plan Approval

The code-generation plan for `statistical-inference` is at
`construction/statistical-inference/code-generation/code-generation-plan.md` — 6 steps:
confirmations change record + proposed D-number FIRST (1), estimand + bootstrap config
transcription (2), bootstrap.py with the vector block bootstrap, spawned streams, byte-pinned
replicate hash and quarantined widening comparator (3), test_bootstrap.py with W-8's checks +
per-entry guard controls (4), smoke + lint under the scratchpad interpreter (5), governance
stop (6).

- Approve Plan
- Request Changes

[Answer]: Approve Plan
