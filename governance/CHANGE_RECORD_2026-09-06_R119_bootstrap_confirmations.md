# Change Record — the three bootstrap scientific confirmations (R-119 interval method, R-115 block scheme, R-121 correlation series) and the estimand/bootstrap config transcription

**Record ID:** `CR-2026-09-06-R119-BOOTSTRAP-CONFIRMATIONS`
**Date:** 2026-09-06 (rulings receipted); record filed 2026-09-06 at the start of the
`statistical-inference` code-generation pass, BEFORE any module of this unit was written
(plan Step 1; the plan's own ordering rule).
**Ruling:** Project decision owner, at the `statistical-inference` code-generation plan gate
(Q1 = A, Q2 = A, Q3 = A, Q4 = A; receipted in
`aidlc/spaces/default/intents/260813-tec-hourly-forecast/construction/statistical-inference/code-generation/code-generation-questions.md`,
Consolidated Summary Confirmation `Looks correct`, Plan Approval `Approve Plan`).
**Change class:** (1) The owner's confirmation of three scientific protocol values that
`functional-design` expressly **routed to the gate as §18.2/TE §18.3 confirmations this
stage may propose but not make** — the interval-construction method (R-119), the
block-resampling scheme (R-115; `GOV-2026-08-28-FD-01` Recommendation 26's fifth gate
item), and the correlation series (R-121) — confirmed under the recorded owner-equivalence
precedent (D-122's seeds transcription; D-28's ratification; `CR-2026-09-06-R106-COMPARISON-SETS`),
with ONE proposed D-number text below covering all three for `evidence/DECISIONS.md` that
the owner adopts or edits (**no agent writes the register**). (2) One transcription of the
already-frozen `estimand` and `bootstrap` values plus the three confirmations into a
governed config (`configs/experiment.yaml`'s two `TBD — freeze gate` sentinels are
replaced; nothing else in the file is touched) — Q4 = A.

## What was owed, and by whom

`configs/experiment.yaml` carried `estimand: "TBD — freeze gate"` and
`bootstrap: "TBD — freeze gate"`, and the file's own header routes both to
"statistical-inference/evaluation-and-comparison" for transcription under a D-number.
TE §18.3 bars any implementer from filling either by convenience, and this unit's design
made three of the bootstrap block's values **explicit gate confirmations, proposed not
decided** (R-119; R-115 as amended under Recommendation 26; R-121). TE §18.3's
stop-and-report posture is why they were questions at this gate rather than defaults: had
3.5 been reached with any of the three unconfirmed, the affected component would have been
built refusal-only (the Q1 = B / Q2 = B / Q3 = B postures).

## The rulings this record implements

### Q1 = A — the interval method is CONFIRMED: the percentile interval

The 95% confidence interval is constructed as the **2.5th and 97.5th percentiles of the
replicate statistics** (linear interpolation over the ordered replicate set). Grounding:
TE §13.6 says *"report 95% confidence intervals"* and names **no** construction method
(verified against the source at functional-design and re-verified by the adversarial
reviewer's failed refutation attempt of 2026-08-27); percentile/basic/BCa differ materially
on 10,000 replicates of a skewed statistic, so the choice is a scientific protocol value
(TE §18.2). The percentile interval is the only method exactly reproducible **from the
replicate set alone**, which keeps WS-17's hashed replicate vector sufficient evidence to
re-derive the interval. The interval component reads the method from
`configs/experiment.yaml` (`bootstrap.interval_method`) and refuses fail-closed on any
unrecognised, absent, or unconfirmed value naming the config field (R-119 control (18)) —
a later BCa ruling changes one component and is a visible protocol change, never an edit.

### Q2 = A — the block-resampling scheme is CONFIRMED: the fixed non-overlapping 24-hour partition

The scored range is partitioned into **contiguous, non-overlapping `block_hours`-hour
blocks aligned to the scored range's start**, each block carrying **all three stations
together** (the vector property, TC-19); a replicate draws exactly N blocks with
replacement, N being the number of whole blocks in the range. On the D-28 DEC scored set
(2–31 December 2022, 720 h) this yields **exactly 30 blocks** at 24 h and **15** at the
48-hour sensitivity — the arithmetic D-28 itself cites. This closes the Rec 26 gate item
(the fifth entry of the functional-design § Gate items list): the moving-block (Künsch)
alternative (697 overlapping candidate blocks over the same 720 h, derived and printed at
R-115) is **not** adopted. R-115's two structural raises are implemented as designed: an
indivisible scored range refuses rather than truncating or padding, and a block extending
outside the mask's scored range refuses. The scheme and the realised block count are
recorded on every `BootstrapResult` (`block_scheme = "fixed_nonoverlapping"`, `n_blocks`),
so the partition actually used is auditable, not inferred from `block_hours`.

### Q3 = A — the correlation series is CONFIRMED: cross-station paired-error Pearson, all three pairs

TE §13.6's mandated *"report the cross-station paired-error correlation"* is computed as
the **pairwise Pearson correlation of the per-station paired squared-error difference
series d_s(t)** (benchmark minus model — the estimand's own step-1 series), over **common
masked timestamps of each pair**, **all three pairs reported** (ARUC–BSHM, ARUC–NICO,
BSHM–NICO), carried machine-readably on `BootstrapResult`
(`correlation_series = "paired_error_pearson_all_pairs"`). The series is load-bearing
twice (Recommendation 23): as TE §13.6's mandated disclosure, and as the discriminating
quantity inside R-120's mandatory real-data disclosure — widening follows only where
cross-station paired-error covariance is positive, so a failed widening comparison is
interpretable only with the measured correlations beside it. R-121 conditions nothing on
them: the correlation is reported and disclosed, never a gate on the raise.

### Q4 = A — the transcription scope: BOTH `experiment.yaml` blocks

- **`estimand`** — orientation `benchmark_minus_model`, weighting `equal_station`, and the
  binding sign-convention sentence ("positive values favour the model: the differential is
  benchmark minus model"), citing **Vision §2.3 / TE §1.3**. These are copies of frozen
  decisions already enforced in code (`src/evaluation/metrics.py`'s `EstimandResult`
  refuses any other orientation/weighting/sentence), so config-versus-code drift is caught
  by test.
- **`bootstrap`** — the frozen values `block_hours: 24`, `replicates: 10000`,
  `confidence_level: 0.95`, `sensitivity_block_hours: 48` (TE §13.6; TC-19
  `binding: hard`), `seed_key: seeds.bootstrap` (D-122; the ADR-05 carve-out —
  `seed_everything` never touches the bootstrap seed), plus the three confirmations above:
  `interval_method: percentile` (Q1), `block_scheme: fixed_nonoverlapping` (Q2),
  `correlation_series: paired_error_pearson_all_pairs` (Q3).

**Nothing either authority does not fix is written**: no sensitivity `run_id` (the owner's
TE §7.2 registration act, exactly as the ablation entries' `run_id` fields remain
`TBD — freeze gate`), no reduced fixture replicate count (an apparatus constant of
`tests/fixtures/scientific_1month/fixture_manifest.yaml`, owned by
`fixtures-and-reproducibility` per Recommendation 24 — expressly NOT a fifth
`experiment.yaml` field), no practical-relevance threshold, no fold or grid value. Every
other key of `configs/experiment.yaml` keeps its current value untouched.

**What this confirmation is, and is not.** It is the set of scientific confirmations the
design routed to the gate, made by the project decision owner at that gate under the
recorded authority equivalence — the same act pattern as D-122's seeds, D-121's grids
(`CR-2026-09-06-BLK03-CONFIRMATORY-CONTRACT`), and the R-106 memberships
(`CR-2026-09-06-R106-COMPARISON-SETS`). Honestly stated: **no supervisor signature
artifact exists and none is claimed.** The §18.2 assignment of these choices is
Student + Supervisor; the proposed D-number below records that limitation on its face,
exactly as D-28 recorded its own.

## Proposed decision text for the owner to adopt (NOT a decision)

> **This section is a DRAFT for the owner's consideration. It has no authority. It becomes
> a decision only when the project decision owner writes it — adopted, edited, or
> replaced — into `evidence/DECISIONS.md` under the next free D-number, dated on or after
> 2026-09-06. The developer does not write it there.**

```
## D-<n> — The bootstrap interval method, block-resampling scheme and correlation series
are FROZEN as configuration (R-119, R-115, R-121)

**Decision date:** <date ≥ 2026-09-06>. **Decided by:** the project decision owner under
the recorded authority equivalence, at the statistical-inference code-generation gate
(Q1 = A, Q2 = A, Q3 = A). **Authority:** TE §13.6 (24-hour vector blocks carrying all
three stations, 10,000 replicates, 95% confidence intervals, cross-station paired-error
correlation reported); TC-19 (binding: hard; the within-station variant rejected at Q-27);
D-122 (bootstrap seed 20221201, seeds.yaml, ADR-05 carve-out); D-28 (the 2–31 December
scored set whose 720 h the block arithmetic divides); TE §18.2/§18.3 (the three values are
scientific protocol choices no implementer may default).
**Raised by:** statistical-inference functional-design R-119, R-115 (as amended under
GOV-2026-08-28-FD-01 Recommendation 26) and R-121, each of which proposed its value and
routed the confirmation to the gate.

**Decision.** Three values are frozen into configs/experiment.yaml under `bootstrap`:

- interval_method = percentile — the 95% interval is the 2.5th/97.5th percentiles of the
  replicate statistics, exactly re-derivable from the hashed replicate vector (WS-17);
- block_scheme = fixed_nonoverlapping — contiguous non-overlapping 24-hour blocks aligned
  to the scored range's start, all three stations travelling together per block; exactly
  30 blocks on the DEC scored set at 24 h and 15 at the 48-hour sensitivity; an
  indivisible range or a boundary-crossing block refuses rather than truncating;
- correlation_series = paired_error_pearson_all_pairs — pairwise Pearson correlation of
  the per-station paired squared-error difference series (benchmark minus model) over
  common masked timestamps, all three station pairs, reported beside the interval and
  inside the widening guard's mandatory real-data disclosure.

The same transcription records the already-frozen estimand orientation/weighting
(benchmark_minus_model, equal_station — Vision §2.3, TE §1.3) and bootstrap parameters
(24-hour blocks, 10,000 replicates, 0.95 level, 48-hour sensitivity, seed key
seeds.bootstrap under D-122). A later change to any of the three confirmed values is a
visible protocol change requiring a new decision, never an edit.

**Limitation, recorded on the decision's face.** The §18.2 assignment of these choices is
Student + Supervisor. No supervisor signature artifact exists for this confirmation; the
ratification is the owner's under the recorded equivalence, exactly as D-28 recorded for
the scored window. The supervisor's countersignature remains owed at G-05, where the
evaluation code and the frozen bootstrap declaration are hashed into the frozen bundle.

**What is NOT decided.** No bootstrap has run, no interval exists, no gate opens; G-05 and
G-06 remain Blocked; the G-06 abort policy for a failed widening comparison at the locked
evaluation remains owed to the Supervisor at G-05 (Recommendation 23); the R-118 signature
amendment and the R-120 raise-contract amendment remain proposed at the gate, not applied.
```

**If the owner declines**, the `estimand`/`bootstrap` blocks transcribed by this pass lose
their confirmation basis and are restored to `TBD — freeze gate` on the owner's word; the
interval component, grid builder and correlation emission then refuse fail-closed naming
the missing fields (the Q1 = B / Q2 = B / Q3 = B postures), and every dependent test
asserts refusals only.

## Honest limits — nothing below is changed by this record

- **G-05 and G-06 remain `Blocked`.** No bootstrap executes in this pass (no released
  features or predictions exist); no DEC read, no DEC metric, no mask freeze occurs.
- **WS-17, TA-13, TA-14 and TA-26 stay `Pending`.** `tests/test_bootstrap.py` is written
  this pass but its acceptance rows are discharged only by governed runs that have never
  happened; the smoke execution under the scratchpad interpreter is smoke evidence only,
  never governed (numpy is uninstallable here — PyPI unreachable — so every draw-dependent
  test skips by name and the numpy-absence refusal path is what executes).
- **The G-06 abort policy for a failed widening comparison at the locked evaluation stays
  owed to the Supervisor at G-05** (`GOV-2026-08-28-FD-01` Recommendation 23). No artifact
  of this pass decides it; the comparator's evidence and mandatory real-data disclosure
  are built, the policy over a real failure is not.
- **No supervisor signature artifact exists or is claimed** for the three confirmations;
  the proposed D-number records that limitation.
- **The R-118 signature amendment** (remove `block_hours=24` / `replicates=10_000` from
  the approved `vector_block_bootstrap` signature) and **the R-120 raise-contract
  amendment** (raise at fixture time, mandatory disclosure on real data, comparator
  tracking its primary's replicate count) remain **proposed at the gate, not applied**:
  the approved `component-methods.md` contract is implemented as quoted (defaults present,
  never exercised) with the amended failure semantics carried per the owner-ruled
  Recommendation 23/24 remediation of this unit's functional design.
- **The Rec 40 change record against `services.md` and `unit-of-work.md`** (the TE §9.3
  storage-versus-memory conflation) remains **owed by those artifacts' owners, not made
  here**; neither file is edited by this pass.
- **TE §15.3's reduced replicate count** remains an apparatus constant owed to
  `tests/fixtures/scientific_1month/fixture_manifest.yaml` by
  `fixtures-and-reproducibility`; this pass declares nothing for it.
- **The TA-21 ownership dispute** stays carried as `nfr-requirements` recorded it.
- **BLK-08's `ABL-DIFF` limb stays open** (D-27 unreopened — verified 2026-09-06:
  `evidence/DECISIONS.md` ends at D-32); the primary interval's TECU status is D-27's
  recorded fact and R-113 precondition 4 stays as the check.
- **No commit is made by this pass.** The governed commit is the student's act and cites
  **D-122, D-28, TC-19** plus the new D-number if adopted. **No governed commit before
  this record and the adopted/declined D-number ruling exist.**

## Propagation sweep (`CHANGE_RECORD_PROCEDURE.md`)

This record changes one governed-artifact content (`configs/experiment.yaml`: the
`estimand` and `bootstrap` `TBD — freeze gate` sentinels are replaced with the frozen
values and the three confirmations; **no other key is touched** — `folds`,
`embargo_hours`, `grids`, `models`, `comparison_sets`, `ablations`,
`practical_relevance_threshold` all keep their current values). Two new modules are
created (`src/evaluation/bootstrap.py`, `tests/test_bootstrap.py` — the unit's § 10 Owns
list, module creation authorised under D-31). One implementation consequence is recorded
rather than hidden: **R-114's one-copy rule requires the estimand's step-1 differencing
and steps-2–3 aggregation to be importable pieces**, so `src/evaluation/metrics.py`'s
inline arithmetic is extracted into named module functions
(`paired_difference_series`, `equal_station_mean`) that `paired_loss_differential` itself
now calls — a behaviour-preserving extraction (same arithmetic, same iteration order, same
raises, `paired_loss_differential`'s signature and results unchanged), made so
`bootstrap.py` can **import and reuse the pieces rather than reimplement them**. This
in-place edit to the sibling's module is **flagged for `evaluation-and-comparison`'s
record and re-check at its next touch**, the same disposition
`CR-2026-09-06-R106-COMPARISON-SETS` applied to the Q2 = B `locked_test.py` edit; the
sibling's own owed item (naming `vector_block_bootstrap` among its guarded entry points)
remains owed at that same touch, and **no completed sibling markdown artifact is edited**.
`BootstrapError` is **not declared anywhere new**: it already exists at `foundation`
R-01's single declaration site (`src/data/config.py`, verified this pass), named in R-01's
enumeration among those raised by other units; `src/evaluation/bootstrap.py` imports and
re-exports it and is its raise site, exactly the pattern `guards.py` documents for
`FairnessError`/`InverseTransformError`. No count, ID range or cardinality asserted
elsewhere changes: this unit's rules stay 10 (R-113…R-122), negative controls stay 24,
entities stay 8, amendments owed stay 8 across 5 units. Sites that state the three values
as "proposed, not decided" (`functional-design/*.md`, `nfr-design/*.md` of this unit) are
**not edited** — completed-stage artifacts under receipts; their statements were true when
written and are superseded as to status by this record, exactly the disposition applied to
the BLK-03 and R-106 banners.
