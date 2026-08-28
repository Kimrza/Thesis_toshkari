# Functional Design Questions — `statistical-inference`

**Unit** `statistical-inference` — uncertainty on the confirmatory estimand: the vector
time-block bootstrap.
**Kind** `library` · **Complexity** M · **Deployment** embedded · **Depends on**
`evaluation-and-comparison`.

Unit **10 of 12**. It owns `src/evaluation/bootstrap.py` and `tests/test_bootstrap.py` —
**2 owned files, derived by counting § 10's `Owns` list**, not carried. It owns no stage
script: it runs inside `scripts/07_evaluate_and_report.py`, which `evaluation-and-comparison`
owns, and it carries **the heaviest CPU cost in the pipeline** — 10,000 replicates over
24-hour vector blocks, inside TE §9.3's 10.0 GB hard planning envelope, on a CPU path that
is complete rather than an emergency mode. Its responsibility: the vector time-block
bootstrap with 24-hour blocks carrying **all three stations together**, 10,000 replicates,
its own generator seeded from the separately frozen **20221201**, a 95% confidence
interval, a 48-hour sensitivity, and the cross-station paired-error correlation reported.
The within-station 2,000-replicate variant was **rejected at Q-27** (TE §13.6; TC-19,
`binding: hard`), and a within-station or naive bootstrap must never be substituted — it
produces systematically narrower intervals.

**Four inherited exit conditions stand on this stage: BLK-03 ↓, BLK-04 ↓, BLK-08 ↓,
BLK-09 ↓.** None is owned here. The bootstrapped differential is computed from the
confirmatory prediction over transform-fitted features, so those contracts bound what this
unit's intervals mean; **BLK-08 ↓ bounds their units** — the interval this unit reports is
in TECU, and until the inverse path `evaluation-and-comparison`'s R-103 drafted is adopted
by its co-owner, nothing in the design returns model output to TECU; **BLK-09 ↓** — the fit
underlying those features rests on a training range no field states. All four are **exit
conditions on stage 3.1, not entry conditions** (`GOV-2026-08-22-REM-01` Rec 2, extended to
BLK-08/BLK-09 on 2026-08-23): this unit may enter, **may not complete or exit** 3.1 while
any contract is unapproved, and **no implementation may proceed** while they stand.

**1 requirement, 0 untested — derived by reading the story map's rows, and the two upstream
artifacts agree**: FR-P1-05-8 (WS-17, TA-14). Per-unit coverage summary row: 1 requirement,
0 untested, **primary WS-17 and TA-14 (2 rows)**, supporting none. The story map names this
the one unit with **full acceptance coverage** — which cuts the other way: FR-P1-05-8's
criterion is **eight mechanical checks, not two** (TE §13.6's seven plus the widening
control), and every one of the eight must land in a designed behaviour or the coverage is
nominal. The determinism rows TA-13 and TA-26 belong to `foundation` and
`models-and-baselines` (NFR-DET-01); this unit's carved-out bootstrap seed is named there
as context, not as an acceptance row here.

**G-09 is not signed.** Workspace inspection 2026-08-27: `tests/` holds three modules
(`test_acquisition_window.py`, `test_phase_boundary.py`, `test_release_hashes.py`) — none
this unit's; `src/` and `configs/` are absent. No answer here authorises creating any
module.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 10 — the `Owns` list (2 files), the boundary (runs inside `07`, seed a required parameter read from `seeds.yaml`, never defaulted and never inlined), the 1 requirement, the acceptance rows, the three implementation notes (Q-27 rejection, heaviest CPU cost inside TE §9.3's 10.0 GB envelope, the ADR-05 seed carve-out as a design decision); **BLK-03/BLK-04/BLK-08/BLK-09** (all inherited, each with the exit-condition ruling and BLK-08's TECU reach into this unit's interval).
- `../../../inception/units-generation/unit-of-work-story-map.md` — Table 1 row FR-P1-05-8 → WS-17, TA-14; Table 2's WS-17 row (evidence: `tests/test_bootstrap.py`, **replicate hash from seed 20221201**) and TA-14 row (reproducible 24-hour output, a 48-hour sensitivity, cross-station correlation, **verified on synthetic correlated data**); § Per-unit coverage summary (1 / 0 / WS-17, TA-14 / —); § Cross-unit responsibilities (NFR-DET-01's row: `foundation` owns seeds and `seed_everything`, this unit holds **the carved-out bootstrap seed** per ADR-05).
- `../../../inception/requirements-analysis/requirements.md` FR-P1-05-8 — the **eight enumerated mechanical checks**: (1) pairing per station-hour before differencing; (2) the resampling unit is a vector block carrying all three stations at the same timestamps, never one station resampled independently; (3) block length 24 h; (4) 10,000 replicates; (5) equal-station weighting matching the estimand; (6) exact reproduction from seed 20221201 on synthetic correlated data; (7) a block holding a missing paired prediction is **handled by the declared rule** rather than silently dropped; (8) the interval is **wider** than the same data run through a naive within-station bootstrap — check 8 is why the other seven are not enough. A 48-hour block-length sensitivity is produced as well.
- `../../../inception/application-design/component-methods.md` § `src/evaluation` — the approved boundary call `vector_block_bootstrap(model: Prediction, benchmark: Prediction, *, mask: DataFrame, block_hours: int = 24, replicates: int = 10_000, seed: int) -> BootstrapResult`: `seed` **required and passed in** (TE §13.5, TC-03e), the function builds **its own local generator**, and it **raises `BootstrapError`** when a block does not carry all three stations at the same timestamps, when a paired prediction is missing and no declared rule handled it, or when the resulting interval is narrower than a naive within-station bootstrap on the same data — **the widening control, "which is what makes the other checks sufficient"**; § Open — **`BootstrapResult` is referenced as a type and left unspecified**, an intra-package shape under § Depth (Q1 = B, this stage's to specify); the exceptions assumption (fourteen project exceptions, declared where raised until 3.1 places them).
- `../../../inception/application-design/services.md` — `07_evaluate_and_report.py`'s row (reads predictions carrying `partition_id`/`transform_id`, benchmark, mask; writes metrics, **bootstrap intervals**, breakdowns, figures) and the resource-envelope note (`07` carries the heaviest CPU cost: 10,000 bootstrap replicates over 24-hour vector blocks; measured peak memory checked against the 10.0 GB envelope).
- `../evaluation-and-comparison/functional-design/` — **JUST finalized, READY**: R-106 (comparison-set membership declared in `experiment.yaml`, checked exactly), R-107 (mask identity, once-only registration, G-05 freeze), R-108 (the estimand as an ordered executable contract — squared errors per (station, hour) on masked rows only → per-station mean of paired differences, **benchmark minus model** → unweighted mean of the three per-station values — and `EstimandResult` carrying orientation `benchmark_minus_model`, weighting `equal_station`, the sign-convention sentence machine-readably), R-109 (hash-receipt before metrics, the `open_restricted` chokepoint with purpose `"locked_evaluation"`, **exactly 2–31 December**), R-104 (inverse-before-metric refused at the boundary every caller crosses), R-110 (the emit-from-the-producing-path disclosure pattern), R-112 (the IRI/GIM allowlist is a path grant; `src/evaluation/` is owned by three units and `vector_block_bootstrap` is expressly recorded as **belonging to this unit**); `domain-entities.md` § 5 (`PredictionHashReceipt`), § 8 (the exception-placement table: `FairnessError` declared in `src/evaluation` by that unit, `LockedTestError` imported from `governance-guards`, the unit-local `InverseTransformError` under R-01's any-future clause). Rule IDs there run **R-103…R-112, derived by grepping its `business-rules.md` headings**.
- `../features-and-splits/functional-design/` — **FU-7 = A**: the G-06 locked test scores **2–31 December 2022, 30 days**, first 24 h excluded and counted; block construction over the scored set must respect it.
- `../models-and-baselines/functional-design/` — R-91 (`three_seed_mean(predictions, *, expected_seeds)` with `expected_seeds` from `ConfigSnapshot.seeds` — the shape `vector_block_bootstrap(seed: int)` already used, cited there as the reason); BLK-03's open contract limbs on the confirmatory prediction this unit's differential consumes.
- `../foundation/functional-design/business-rules.md` R-01 — all fourteen project exceptions derive from `IntegrityError` (base in `src/data/config.py`); **`BootstrapError` is one of the fourteen, raised by this unit**, importing the base; every raise names the file or resource and the violated expectation.
- `aidlc/spaces/default/memory/project.md` § Mandated/Forbidden and `team.md` — the vector time-block bootstrap rule (TE §13.6; TC-19 `binding: hard`; Q-27's rejection), NEVER substitute a within-station or naive bootstrap, the estimand (Vision §2.3, TE §1.3), seeds from `seeds.yaml` (NFR-DET-01, TC-21), no scientific constant in source (TC-03e), the negative-control-per-hard-rule methodology, CPU as a complete execution path (TC-01), TE §18.3's stop-and-report posture.
- `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §13.6 (the procedure verbatim — resample 24-hour blocks **on the common timeline** carrying all three stations as a vector; 10,000 replicates; fixed seed 20221201; equal-station weighting; **report 95% confidence intervals** — no interval-construction method is named; repeat with 48-hour blocks as a sensitivity; report the cross-station paired-error correlation; the required tests, and the synthetic dataset with known cross-station and temporal correlation that must confirm widening relative to a naive within-station bootstrap); §13.7 (exact equality for deterministic CPU transformations; fixture-derived tolerances for floats); §9.3 (the 10.0 GB envelope).
- Workspace inspection, 2026-08-27: `tests/` holds three modules, none this unit's; `src/` and `configs/` absent.
- Absent by scope design: `stories` (2.4 `SKIP`), `mockups` (1.6 and 2.5 `SKIP`). `kind: library`.

---

## Question 1

**What the bootstrap consumes, and which sibling preconditions bind at its boundary.** The
approved signature takes two `Prediction`s and `mask` — raw inputs, not the differential.
`evaluation-and-comparison` has since made three things checkable at exactly this kind of
boundary: R-107's registry (a mask is registered and frozen for its declared comparison
set, or metrics raise), R-105's stamp refusal (non-`None` `partition_id`/`transform_id`,
members agreeing), and R-109/R-104's metric-entry-point preconditions for the `DEC`
partition (hash receipt verified, transformed-space input refused). The bootstrap interval
is a reported, TECU-denominated quantity — BLK-08's register names it in this unit's
blocked scope — and the G-06 interval is computed on the locked test. Nothing yet states
whether `vector_block_bootstrap` is a "metric entry point" under those rules or a trusted
internal callee of `07`.

A) Trusted callee: `07` calls the bootstrap only after `paired_loss_differential` has passed its checks, and the bootstrap re-asserts nothing
   > **Impact**: No duplicated checks, but the guarantee holds only for one caller's call order — the class of gap R-104 was written to close. A notebook or test calling `vector_block_bootstrap` directly (TE §14 expressly reads bootstrap artifacts into `04_results_and_figures.ipynb`) would compute an interval off an unregistered mask or unverified prediction with nothing firing.

B) The bootstrap asserts the mask and stamp preconditions itself: `mask` must be a registered frozen mask for the members' declared comparison set (R-107's check, raising `FairnessError`), and both `Prediction`s must carry non-`None`, mutually agreeing stamps (R-105's rule)
   > **Impact**: The interval inherits the same fairness floor as the point estimate, whatever the caller. Costs importing the registry check this unit's sibling owns — an intra-`src/evaluation` call, no new dependency edge.

C) B, plus the bootstrap is declared a metric entry point in full: evaluating the `DEC` partition requires the recorded prediction-hash receipt re-verified before any draw (R-109 limb 1, raising `LockedTestError`), and transformed-space input is refused unless the resolved transform is declared non-target-touching or the inversion lineage shows the inverse applied (R-104) — so the interval is TECU-denominated **by check**, not by assumption
   > **Impact**: Closes the loophole where the point estimate is guarded and the uncertainty statement around it is not; the interval and the scalar it brackets provably describe the same data in the same units. Costs two imported precondition checks, and makes this unit's dependence on BLK-08's resolved inverse path explicit rather than silent.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. The bootstrap interval is the thesis's uncertainty statement on its single most protected number; an interval computed off-mask, off-receipt, or in transformed space is wrong in exactly the ways the sibling's R-104/R-107/R-109 exist to catch, and A restores the one-specific-caller gap for the artifact `04_results_and_figures.ipynb` reads directly. C is two imported checks, not new machinery.

[Answer]: C

---

## Question 2

**One copy of the estimand arithmetic: what a replicate recomputes.** FR-P1-05-8 check 5
requires the bootstrap's station weighting to **match the estimand**, and R-108 has fixed
that estimand as one ordered pipeline: squared errors per (station, hour) on masked rows
only → per-station mean of paired differences, benchmark minus model → unweighted mean of
the three per-station values. Each of the 10,000 replicates computes this same statistic
over a resampled set of blocks. A bootstrap that reimplements the differencing privately
can drift from the estimand it claims to bracket — the second-copy failure class §14's
one-copy rule and the sibling's rejection of its own option B (reimplementing the inverse
arithmetic) both name.

A) `bootstrap.py` implements its own squared-error differencing and aggregation, documented as equivalent in prose
   > **Impact**: Self-contained, but "equivalent" is asserted, not checked: a pooled-versus-equal-station divergence or a sign flip in the private copy silently produces an interval that does not bracket the reported scalar, and no test compares the two paths until someone thinks to.

B) Precompute once, resample the precomputed: the per-(station, hour) paired squared-error differences are computed **once**, on masked rows only, through the same step-1 code path R-108's `paired_loss_differential` uses; replicates resample **blocks of those precomputed differences** and reapply only steps 2–3 (per-station mean, benchmark minus model orientation preserved; unweighted three-station mean)
   > **Impact**: One copy of the scientific arithmetic, owned where R-108 put it; the replicate statistic is the estimand by construction, not by review. Also the cheap shape: differencing runs once, not 10,000 times — material for the pipeline's heaviest CPU unit.

C) B, plus the equality control: the bootstrap's own full-data point estimate must equal `paired_loss_differential`'s scalar on the same mask **exactly** (a deterministic CPU transformation under §13.7's exact-equality rule) or `BootstrapError` is raised; and the negative control that a pooled row-weighted replicate statistic **fails** on a fixture with asymmetric per-station row counts — the same fixture R-108's control (16) uses, applied to the replicate path
   > **Impact**: The one-copy claim becomes a checked invariant instead of an architecture diagram, and check 5 gets its violation-is-caught proof per the affirmed methodology. Costs one equality assertion and one fixture reuse.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. The interval's entire meaning is "uncertainty of *this* estimand"; B makes that true by construction and is simultaneously the cheapest implementation, and C's equality check is the only line that proves the bracketing claim rather than trusting it. A is the drift class this project has now rejected twice by name.

[Answer]: C

---

## Question 3

**Block construction over the scored range: alignment, count, and what a boundary
violation raises.** TE §13.6 fixes "24-hour blocks on the common timeline" and FU-7 = A
fixes the G-06 scored set at **2–31 December 2022, 30 days** — which divides into exactly
**30 whole 24-hour blocks** (and exactly **15** at the 48-hour sensitivity). Unstated: are
blocks a fixed partition of the scored range or a moving-block scheme with overlapping
starts; how many blocks a replicate draws; and what happens when a block would cross the
scored-range boundary or the range does not divide evenly.

A) Moving-block bootstrap: blocks may start at any hour, overlapping, drawn until the replicate reaches the scored length
   > **Impact**: A recognised construction in the time-series literature, but a further reading of "blocks on the common timeline" than the frozen text states, with more choices to freeze (start-index distribution, wrap policy) — each an unfrozen protocol value §18.3 would stop on — and a harder exact-reproduction story for WS-17's replicate hash.

B) Fixed non-overlapping partition: the scored range is partitioned into contiguous 24-hour blocks aligned to its start (for DEC: 00:00 UTC block boundaries, 30 blocks); a replicate draws exactly N blocks with replacement, N being the number of whole blocks in the range; a scored range not evenly divisible by the block length **raises `BootstrapError`** rather than silently truncating or padding a partial block
   > **Impact**: The plainest reading of §13.6's fixed-block wording, deterministic to reproduce, and the divisibility raise makes the partial-block case impossible instead of policy-laden. For the frozen ranges it never fires (30/1 and 30/2 both divide); it exists so a changed range surfaces as an error, not a quiet reweighting.

C) B, plus the boundary controls: any block extending outside the mask's scored range **raises `BootstrapError`**; the DEC range assertion is inherited as a precondition — the mask already asserts exactly 2–31 December with the first 24 h excluded and counted (R-109 limb 3), so a 31-block December containing 1 December is unrepresentable upstream of the bootstrap and additionally refused here; negative controls for the misaligned-block and boundary-crossing cases in `tests/test_bootstrap.py`
   > **Impact**: Encodes FU-7 = A where this unit touches it and makes the block grid an assertable fact. Redundancy with the sibling's mask assertion is by design at the locked boundary, and the cost is two raises and their fixtures.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A adds unfrozen protocol choices to a procedure whose every named parameter is already frozen; B is the reading under which every frozen number (24 h, 30 days, 15 two-day blocks) is exact with nothing invented. Block alignment is stated at the gate as a derivation from the frozen texts, not decided silently — if the owner reads §13.6 otherwise, this question is where it surfaces.

[Answer]: C

---

## Question 4

**The vector property as an executable rule, and the declared rule for missing pairs —
NICO's missingness makes this the unit's hardest case.** Check 2: the resampling unit is a
vector block carrying all three stations at the same timestamps, never one station
resampled independently. Check 7: a block holding a missing paired prediction is handled by
**the declared rule** rather than silently dropped — and no artifact declares that rule
yet. The comparison-wide mask is an intersection per (station, hour), so within masked rows
every pair is complete; but a station can be absent from the mask at hours where another is
present (NICO holds 96.4% of hourly bins, not 100%), so a 24-hour window generally holds a
**ragged** three-station vector. The signature raises `BootstrapError` "when a block does
not carry all three stations at the same timestamps" — which cannot mean triple-complete
timestamps everywhere, or December's measured coverage would make every real run raise.

A) Complete vectors by construction: intersect across stations too, so the bootstrap's timeline holds only timestamps where all three stations are masked
   > **Impact**: Makes every block vector-complete, but silently narrows the scored row set relative to the frozen comparison-wide mask — the interval would bracket a different data set than the point estimate reports, a scientific change this stage cannot make and R-107's mask freeze exists to prevent.

B) Ragged blocks under a declared rule: a block carries, per station, exactly the masked rows falling inside its window; "all three stations together" is enforced as **same resampled block indices applied to all three stations simultaneously** — the property that preserves cross-station dependence, and the thing a within-station resampler breaks; per-replicate per-station means use whatever masked rows the drawn blocks contain; a replicate in which any station ends with **zero** masked rows raises `BootstrapError` (the equal-station mean is undefined), recorded as a structural guard that December's measured coverage makes practically unreachable
   > **Impact**: The interval and the point estimate describe the same frozen mask; check 7's "declared rule" is finally declared, and declared as arithmetic on what the mask already says rather than as a new exclusion policy. The zero-support raise is the only new failure mode, and it names the station and window per R-01's constructor contract.

C) B, plus the controls that prove both properties: the TA-14 synthetic fixture — known cross-station and temporal correlation, with gaps injected in one station's series — confirms blocks travel together (recovered correlation within declared tolerance) and that gap handling follows the declared rule; and the negative control that independently resampled per-station block indices (the Q-27 anti-pattern, named) are **caught** — directly by a same-indices assertion in the test, and behaviourally by check 8's widening guard firing on the narrower interval it produces
   > **Impact**: The vector property gets the violation-is-caught proof the affirmed methodology demands, with the rejected Q-27 variant explicitly the thing the control resurrects in order to catch. Costs the synthetic fixture TA-14 already requires.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A changes the scored population — the one move this unit must never make silently; B is the only reading under which the signature's raise, the mask's semantics, and NICO's real coverage are simultaneously satisfiable, and it turns check 7's undefined "declared rule" into a stated one. C adds the fixture TA-14 requires anyway and points it at the exact substitution TC-19 forbids.

[Answer]: C

---

## Question 5

**Seed sourcing, generator identity, and what "reproduces exactly" pins.** The seed is
required and passed in — read from `seeds.yaml` (the separately frozen **20221201**, TE
§13.6/§13.5; not part of D-122's item set) via `ConfigSnapshot.seeds` at the call site,
never defaulted and never inlined — and the function builds its own local generator, the
ADR-05 carve-out unit-of-work.md records as deliberate. WS-17's evidence is a **replicate
hash from seed 20221201**, and §13.7 demands exact equality for deterministic CPU
transformations. But a seed alone does not pin a bit stream: two correct implementations
using different generators (or consuming draws in different orders) produce different
replicate sets from the same seed, and "reproduces exactly" silently becomes
"reproduces on the machine that wrote the hash".

A) Generator choice left to implementation; the contract pins only the seed
   > **Impact**: WS-17's replicate hash becomes an implementation accident — any refactor that reorders draws or swaps generators changes the hash while every scientific property still holds, and the acceptance row can neither be written down in advance nor survive a rewrite.

B) Pin the generator and the draw discipline in the contract: NumPy `default_rng(seed)` (PCG64), block-index draws as the **only** consumer of the primary stream, and the 48-hour sensitivity and the widening comparator (Question 8) drawing from **deterministically derived child streams** (seed-sequence spawn) so no consumer can perturb another's draws
   > **Impact**: Exact reproduction becomes implementation-independent and refactor-stable. The pins are engineering contracts, not scientific constants — the scientific value (20221201) stays in `seeds.yaml`, satisfying TC-03e; the generator name is no more a scientific constant than the language pin.

C) B, plus the recorded evidence and controls: `BootstrapResult` records the seed key consumed, the generator identity, and the replicate hash (WS-17's evidence emitted by the producing path, the R-110 pattern); negative controls: a different seed produces a different replicate hash, and a same-seed rerun reproduces the hash exactly — both in `tests/test_bootstrap.py`; and the test asserts the seed arrived as a parameter (a call without `seed` is a `TypeError` by signature — the never-defaulted rule is unrepresentable rather than checked)
   > **Impact**: WS-17 becomes an assertable artifact fact rather than a log line, and the carve-out's purpose — a model-seed change can never move a bootstrap draw — is testable because the streams are independent by construction. Costs three result fields and two fixtures.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. "Reproduces exactly from seed 20221201" is this unit's primary acceptance row; A leaves it unfalsifiable in advance, B makes it true by contract, and C makes it evidenced the way this project's other determinism claims are — recorded, hashed, and paired with the control that a wrong seed visibly fails.

[Answer]: C

---

## Question 6

**Where the frozen numbers live: the signature's defaults versus the four governed
configs — and the 48-hour sensitivity's mechanics.** The approved signature defaults
`block_hours=24` and `replicates=10_000`. Both are frozen scientific protocol values (TE
§13.6), and TC-03e places scientific constants in the four governed configs, not source —
the exact reasoning that made `seed` a required parameter, with component-methods.md
noting the seed shape was adopted "for the identical reason". The defaults are therefore an
inconsistency inside the approved contract, and changing an approved contract by assertion
is refused practice on this project. Separately, the 48-hour sensitivity is required output
(TE §13.6; TA-14) and nothing yet states how it is invoked or kept apart from the
confirmatory interval.

A) Keep the defaults as approved; `07` calls with them and the sensitivity flips `block_hours=48` at the call site
   > **Impact**: Two frozen scientific values live in source as defaults — the pattern TC-03e forbids and this unit's own seed parameter was reshaped to avoid — and a caller omitting the arguments cannot be distinguished from a caller choosing them.

B) Values declared in `experiment.yaml` and passed explicitly from `ConfigSnapshot` at every call; the signature defaults remain but are never exercised
   > **Impact**: The governed copy exists, but a dead default is a drift channel: a config/signature disagreement is invisible until someone calls the function bare, and the source still prints the constants TC-03e says it must not hold.

C) B, plus the signature amendment raised at the gate: remove both defaults, making `block_hours` and `replicates` required keywords like `seed` — recorded as an **amendment owed to `component-methods.md`**, proposed not applied (the sibling's dependency-row precedent); and the 48-hour sensitivity fixed as a **predeclared named run** in `experiment.yaml` (the ablation discipline applied to a required sensitivity), same seed 20221201 on its own derived child stream, its result labelled sensitivity and **never merged into or substituted for** the 24-hour confirmatory interval
   > **Impact**: The frozen values live only in config, a bare call is a `TypeError`, and the amendment goes through the front door. The sensitivity becomes invocable, auditable and un-confusable with the confirmatory number. Costs one gate item and two config fields the gate must confirm.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. The project already ruled on this exact shape once — the seed — and left the neighbouring two parameters behind; C finishes the thought under the same rule, and routes the signature change as an amendment rather than an assertion. The sensitivity's predeclaration is the only mechanism this project uses for named runs, and reusing it costs nothing new.

[Answer]: C

---

## Question 7

**The 95% confidence interval's construction method is nowhere frozen.** TE §13.6 says
"report 95% confidence intervals" and stops; FR-P1-05-8's eight checks constrain pairing,
blocks, replicates, weighting, seed, missing-pair handling and widening — not the interval
estimator. Percentile, basic, and BCa intervals can differ materially on 10,000 replicates
of a skewed statistic, so the choice changes the reported bracket. It is a scientific
protocol value: §18.2 bars an implementer filling such a value by convenience, and §18.3's
posture is stop-and-report rather than choose a default.

A) Leave the method to stage 3.5's implementer
   > **Impact**: The thesis's uncertainty statement gets decided by whichever function name the implementer reaches for — precisely the convenience-fill §18.2 forbids on a value this consequential.

B) Propose the **percentile interval** (2.5th and 97.5th percentiles of the 10,000 replicate statistics) and route it to the gate as an explicit scientific confirmation, to be recorded in `experiment.yaml` beside the 0.95 level once confirmed
   > **Impact**: The standard estimator for block bootstraps; exactly reproducible from the replicate set alone (no auxiliary estimation), which keeps WS-17's replicate-hash evidence sufficient to re-derive the interval. The confirmation is the owner's: this stage proposes, the student/supervisor freeze.

C) Propose **BCa** (bias-corrected and accelerated) at the gate instead
   > **Impact**: Corrects median bias and skew, but its acceleration term needs a jackknife whose block analogue is itself an unfrozen methodological choice — a second estimator decision hidden inside the first, with no governing text naming either.

D) Stop and report now: treat the method as a TBD freeze-gate value and suspend this unit's design until ruled
   > **Impact**: The most literal §18.3 reading, but this project's affirmed pattern for exactly this situation is propose-and-route (the sibling's comparison-set membership went to its gate the same way); stopping the whole unit buys no additional safety over a gate item the owner rules on before any implementation exists anyway (G-09 unsigned).

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B. It is the simplest estimator consistent with every frozen fact, adds no hidden second choice as C does, and reaches the same human authority D would — at the gate this file already stops at. The design carries the confirmed method as a frozen config value, so a later change is a visible protocol change, not an edit.

[Answer]: B

---

## Question 8

**The widening control's mechanics: the rejected method as the yardstick that must be
beaten.** Check 8 and the approved signature make this a **runtime raise**: `BootstrapError`
when the resulting interval is narrower than a naive within-station bootstrap **on the same
data**. The comparator is, by construction, the method Q-27 rejected — it exists in the
code solely to be beaten. Unstated: the comparator's parameters (replicates, seed), where
its numbers may appear, and the cost of running it inside the pipeline's heaviest CPU unit.

A) Demote the check to test-time: a fixture proves widening once, and the runtime raise is dropped
   > **Impact**: Contradicts the approved boundary contract (the raise is in the signature) and FR-P1-05-8's check 8, which names the same-data comparison — an approved-contract change by assertion, the move this project refuses. A regression that narrows real intervals after the fixture passes would ship silently.

B) Runtime comparator, fully specified: same masked data, same block length, **same replicate count (10,000)**, seed drawn from a deterministically derived child stream of the primary seed (Question 5's discipline); interval-width comparison at the same confidence level; narrower-or-equal raises `BootstrapError`; and the comparator's numbers are **never serialized as a reported interval** — the Q-27 variant may not re-enter any results artifact, table or notebook
   > **Impact**: The guard is exact (same data, same size — no small-sample excuse for a narrow comparator; the rejected variant's 2,000-replicate parameter is not resurrected), deterministic, and quarantined from reporting. Costs roughly a second bootstrap per evaluation run.

C) B, plus the cost and evidence mechanics: the comparator's width, replicate count and derived seed are recorded in `BootstrapResult` as **guard evidence** (machine-readable, the emit-from-the-path pattern — evidence of the check, expressly not a reported interval); the doubled CPU cost is stated against TE §9.3's 10.0 GB envelope with the runtime measured at fixture time and frozen into the fixture manifest per §15.2, never invented; negative control: a deliberately within-station-resampled primary **fails the guard** on the TA-14 synthetic fixture
   > **Impact**: The guard's firing conditions become auditable after the fact, the cost is measured where this project measures costs, and the control proves the raise actually catches the substitution TC-19 names. Costs three result fields and one fixture case Question 4 already builds.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. Check 8 is the check "which is what makes the other checks sufficient" — the one line standing between this unit and the systematically-narrower-intervals failure the register calls TC-19's named failure. B makes it exact and quarantined; C makes it evidenced and proven, and books the honest CPU price the way this project books every cost: measured, then frozen.

[Answer]: C

---

## Question 9

**The cross-station paired-error correlation: which series, computed how, reported
where.** TE §13.6 mandates "report the cross-station paired-error correlation" without
fixing the series or the statistic; TA-14 requires it verified on synthetic correlated
data. The candidate series are the per-station paired squared-error difference series
d_s(t) — the estimand's own series, whose cross-station correlation is precisely the
quantity that justifies the vector construction (correlated d_s(t) is why within-station
resampling narrows intervals) — or the raw per-station errors before differencing. Three
station pairs exist (ARUC–BSHM, ARUC–NICO, BSHM–NICO).

A) Compute it in the results notebook at reporting time, from the serialized predictions
   > **Impact**: A reporting obligation with no producing field — the gap class the sibling's R-110 closed. The notebook could omit it, compute it on a different series each run, and §14 forbids a notebook holding the only copy of bootstrap logic.

B) Defined and emitted by the producing path: pairwise Pearson correlation of the per-station paired-error difference series d_s(t), over common masked timestamps of each pair, **all three pairs reported**, carried machine-readably on `BootstrapResult`; `regimes-diagnostics-reporting` asserts the field's presence and restates nothing
   > **Impact**: The mandated disclosure travels with the artifact that owns it (R-110's pattern), and the chosen series is the one that explains the method: the correlation reported is the correlation the vector bootstrap exists to respect. Costs three floats and a definition sentence.

C) B, plus the definitional routing and the control: the series choice (paired differences, not raw errors) is stated at the gate as a proposal — the governing sentence names "paired-error correlation" without fixing the series, so the reading is confirmed, not assumed; and the TA-14 synthetic fixture plants a known cross-station correlation and asserts the reported values recover it within a declared tolerance (§13.7's fixture-derived-tolerance discipline)
   > **Impact**: The one ambiguous word in the frozen sentence gets an owner-confirmed reading instead of a silent one, and TA-14's "verified on synthetic correlated data" becomes a concrete pass/fail case. Costs one gate item and one fixture assertion.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. B's emit-from-the-path shape is settled practice next door; the series question is genuinely underdetermined by the frozen text, and the difference matters scientifically, so it goes to the gate as a stated reading — the cheap honesty this project's learning rules keep demanding. The recommendation inside the proposal is the paired-difference series, the only reading under which the reported number is the one the method's own justification cites.

[Answer]: C

---

## Question 10

**`tests/test_bootstrap.py`'s scope: eight checks, two acceptance rows, and the negative
controls that make full coverage real.** This is the story map's one unit with full
acceptance coverage, so this module is where that claim is either earned or hollow. WS-17's
evidence: the replicate hash from seed 20221201. TA-14's: reproducible 24-hour output, the
48-hour sensitivity, cross-station correlation, verified on synthetic correlated data. TE
§13.6 names the required tests: pairing, vector construction across stations, block length,
replicate count, weighting, seed reproducibility, behaviour with missing paired
predictions, plus the synthetic-data widening confirmation. The affirmed methodology adds:
every hard rule gets a test proving the violation is **caught**.

A) Positive-path coverage: the eight FR-P1-05-8 checks asserted on synthetic data, plus the WS-17 hash
   > **Impact**: Satisfies §13.6's list as written but not the affirmed negative-control methodology — a suite that never proves the within-station substitution, the wrong seed, or the boundary-crossing block are caught leaves TC-19's named failure undetectable by construction.

B) The eight checks plus the named negative controls from Questions 1–9, each asserted to raise or fail: within-station substitution caught (the widening guard fires — Q8); wrong seed → different replicate hash, same seed → identical hash (Q5); misaligned or boundary-crossing block raises (Q3); indivisible scored range raises (Q3); zero-support station in a replicate raises (Q4); unregistered mask and mismatched stamps raise (Q1); pooled-weighting replicate statistic fails the asymmetric fixture, and the full-data point estimate equals the estimand scalar exactly (Q2); planted correlation recovered within tolerance (Q9)
   > **Impact**: Every hard rule this unit carries gets its violation-is-caught pair, and the module's scope is derived from this file's own questions rather than invented at 3.5. Costs the fixtures — all synthetic and CPU-trivial.

C) B, plus the fixture and evidence mechanics: synthetic fixture parameters (planted correlation, gap pattern, per-station row counts) are declared constants **of the test apparatus**, stated as such — the scientific values (seed, block length, replicate count, CI level) arrive from config even under test, so the suite itself proves the no-inlined-constant rule; and the module emits WS-17's replicate hash and TA-14's synthetic-case results as machine-readable evidence suitable for the acceptance rows' evidence columns
   > **Impact**: The acceptance evidence is produced by the named module exactly as the two rows state it, and the test/scientific constant boundary is explicit instead of litigated later. Costs a documented convention inside one file.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. Full acceptance coverage on paper is this unit's headline and its risk: A would leave the two rows technically citable and substantively empty. B is the affirmed methodology applied to this unit's own question set; C makes the evidence land where WS-17 and TA-14 say it lands, with the constants question answered before a reviewer has to ask it.

[Answer]: C

---

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence: `evaluation-and-comparison` closes at **R-112** (derived 2026-08-27 by grepping its `business-rules.md` headings: R-103…R-112), so this unit opens at **R-113**. The sibling's flagged R-83…R-89 gap is inherited as observed, not explained; if per-unit numbering was intended, say so at the gate and the artifacts renumber.
- **[assumption]** `BootstrapResult` is an intra-package shape and this stage's to specify (`component-methods.md` § Open and § Depth, Q1 = B). The fields accumulated by this file's questions — interval bounds and level, point estimate with its equality-checked link to `EstimandResult`, per-station components, seed key and generator identity and replicate hash (Q5), comparator guard evidence (Q8), the three pairwise correlations (Q9), the 48-hour sensitivity's labelled result (Q6), and the mask/stamp identifiers it was computed over — are proposed shapes, finalized in `domain-entities.md` after the gate.
- **[assumption]** Exception placement follows `foundation` R-01 and the sibling's § 8 table: **`BootstrapError` is one of the fourteen**, declared **here** (`src/evaluation/bootstrap.py`, this unit's raise site), importing `IntegrityError` from `src/data/config.py`; `FairnessError` (declared by `evaluation-and-comparison` in `src/evaluation`) and `LockedTestError` (declared by `governance-guards`) are imported for the preconditions Question 1 adopts, not redeclared. Every raise names the file or resource and the violated expectation.
- **[assumption]** `vector_block_bootstrap` lives in `src/evaluation/` under the TE §12 allowlist as a **path grant owned by three units** (`evaluation-and-comparison` R-112, `external-products` R-56); this unit designs `bootstrap.py` only and asserts no narrowing of TE §12.
- **[assumption]** The seed 20221201 reaches this unit as `ConfigSnapshot.seeds`' bootstrap entry from `configs/seeds.yaml` — the separately frozen value (TE §13.6; TC-19; **not** part of D-122's item set, attribution per `GOV-2026-08-22-UG-02` Rec 11) — through `07`'s call site. The `seeds.yaml` key name is `foundation`'s surface; this unit consumes whatever key that unit's config schema fixes.
- **Verification obligations owned here:** the mask/stamp/receipt/TECU preconditions at the bootstrap boundary (Q1); the point-estimate equality check and the pooled-weighting control (Q2); the divisibility, misalignment and boundary-crossing raises (Q3); the same-indices vector assertion, the zero-support raise and the gap-following-declared-rule fixture (Q4); the same-seed/different-seed replicate-hash controls and the recorded generator identity (Q5); the never-merged separation of the 48-hour sensitivity (Q6); the widening guard with its quarantined comparator and its caught-substitution control (Q8); the planted-correlation recovery assertion (Q9); `tests/test_bootstrap.py`'s full negative-control set and its evidence emission (Q10).
- **Governance dependencies owned outside this unit:** BLK-03's contract limbs (`models-and-baselines`, 3.1); BLK-04's contract limbs and BLK-09's `train_start` resolution (`features-and-splits`, 3.1); BLK-08's co-owner adoption (the R-103 joint contract's pending half — until it is adopted, no design path returns model output to TECU and this unit's interval inherits that bound); the signature amendment removing the two defaults (Q6 — an amendment owed to `component-methods.md`, ruled at the gate); the CI-method confirmation (Q7) and the correlation-series reading (Q9) — scientific protocol values the student/supervisor freeze, proposed here, never decided here; `experiment.yaml`'s bootstrap fields (block hours, replicates, CI level, the predeclared 48-hour sensitivity run) — config content confirmed at the gate and frozen under the four-config regime; acceptance-row evidence formats for WS-17/TA-14 (stage 3.2 territory if any row text needs amendment, via Vision §15.2); G-05's freeze of the evaluation code this stage designs (Supervisor).
- **Open — all four inherited blockers are EXIT conditions on this stage.** BLK-03 ↓, BLK-04 ↓, BLK-08 ↓, BLK-09 ↓ remain open; nothing in this file closes any of them, this unit may not complete or exit 3.1 while any stands, and no implementation may proceed while they stand.
- **Open — the CPU and memory budget is measured, not asserted.** The doubled cost of Q8's runtime comparator and the 10,000-replicate primary run are stated against TE §9.3's 10.0 GB envelope, but §15.1 fixes that exact counts and runtimes are **measured from the fixtures and frozen, never invented** — the numbers this design books are placeholders until fixture time, and no tolerance or runtime figure in this unit's artifacts may be invented before then.
- **G-09 is not signed.** No answer here authorises creating `src/evaluation/bootstrap.py` or `tests/test_bootstrap.py`, and TE §18.3's stop-and-report rule binds every affected component while any P0 decision is unresolved.
- **None** of the above decides a scientific value. Where a question touches one — the block alignment reading (Q3), the interval method (Q7), the correlation series (Q9), the `experiment.yaml` fields (Q6) — the value is either already frozen (24 h, 10,000, 20221201, 95%, 2–31 December) or expressly routed to the gate as a proposal.

---

## Consolidated Summary Confirmation

Questions 1–10 are answered above: **Q1 = C, Q2 = C, Q3 = C, Q4 = C, Q5 = C, Q6 = C,
Q7 = B, Q8 = C, Q9 = C, Q10 = C**. This is the pre-generation summary stop: before the
three design artifacts are generated, this section states the whole of what those answers
commit to, and nothing else is generated from them.

### What will be generated

Three artifacts, in this directory:

- **`business-logic-model.md`** — the workflows: the input/precondition boundary — the
  bootstrap as a metric entry point in full, asserting R-107's registered-mask check,
  R-105's stamp agreement, R-109's hash receipt on `DEC`, and R-104's transformed-space
  refusal, so the interval is TECU-denominated by check (Q1); the precompute-once estimand
  reuse — per-(station, hour) paired squared-error differences computed **once** through
  R-108's step-1 path, replicates resampling blocks of the precomputed differences and
  reapplying only steps 2–3, with the exact-equality control against
  `paired_loss_differential`'s scalar (Q2); the fixed non-overlapping 24-hour partition —
  30 whole blocks over the DEC scored set, 15 at the 48-hour sensitivity, N-blocks-with-
  replacement draws, indivisibility and boundary-crossing raising `BootstrapError` (Q3);
  the ragged vector blocks under the declared rule — same resampled block indices applied
  to all three stations simultaneously, per-station masked rows as the mask states them,
  the zero-support raise (Q4); the seed/generator discipline — `default_rng(seed)` (PCG64),
  block-index draws the only consumer of the primary stream, child streams spawned for the
  sensitivity and the comparator (Q5); the widening guard — the runtime same-data,
  same-replicate-count within-station comparator, narrower-or-equal raising, its numbers
  quarantined from every results artifact (Q8); and the correlation emission — pairwise
  Pearson on the paired-difference series d_s(t), all three pairs, emitted by the producing
  path (Q9).
- **`business-rules.md`** — rules opening at **R-113**, continuing the single sequence:
  the siblings end at **R-112**, derived 2026-08-27 by grepping
  `evaluation-and-comparison`'s `business-rules.md` headings (R-103…R-112, ten headings);
  the R-83…R-89 gap is inherited as observed, not explained, per the receipted assumption.
- **`domain-entities.md`** — the intra-package shapes `component-methods.md` § Open and
  § Depth assign to this stage: **`BootstrapResult`** carrying the interval bounds and
  level, the equality-checked point estimate, the per-station components, the **seed key
  consumed, generator identity, and replicate hash** (Q5, WS-17's evidence emitted by the
  producing path), the **comparator guard evidence** — width, replicate count, derived
  seed, expressly not a reported interval (Q8), the **three pairwise correlation fields**
  (Q9), the labelled 48-hour sensitivity result never merged into the confirmatory
  interval (Q6), and the mask/stamp identifiers it was computed over; plus the block
  shapes — the fixed-partition block grid and the ragged per-station block contents as
  assertable facts (Q3, Q4).

The one test module scoped here is **`tests/test_bootstrap.py`** (Q10 = C): the eight
FR-P1-05-8 checks plus the named negative controls from Questions 1–9, each asserted to
raise or fail; fixture parameters declared constants of the test apparatus while the
scientific values arrive from config even under test; WS-17's replicate hash and TA-14's
synthetic-case results emitted as machine-readable acceptance evidence. Its design is
specified; **no module is created** — G-09 is not signed.

### Each answer, one line

| Q | Answer | Design consequence |
|---|---|---|
| 1 | C | The bootstrap is a metric entry point in full: registered-mask and stamp preconditions asserted itself (R-107, R-105), the `DEC` hash receipt re-verified before any draw (R-109, `LockedTestError`), transformed-space input refused (R-104) — the interval is TECU-denominated **by check**, making the BLK-08 dependence explicit rather than silent |
| 2 | C | One copy of the estimand arithmetic: differences precomputed once through R-108's own step-1 path, replicates reapply steps 2–3 only; the full-data point estimate must equal `paired_loss_differential`'s scalar **exactly** (§13.7) or `BootstrapError`, with the pooled-weighting negative control on the asymmetric fixture |
| 3 | C | Fixed non-overlapping 24-hour partition aligned to the scored range's start — 30 blocks for DEC, 15 at 48 h — N blocks drawn with replacement; indivisible ranges and boundary-crossing blocks **raise**, and R-109 limb 3's 2–31 December assertion is inherited as a precondition and additionally refused here |
| 4 | C | Ragged vector blocks under the now-declared rule: same resampled block indices applied to all three stations simultaneously, per-station rows exactly as masked; a zero-support station in a replicate **raises**; the TA-14 synthetic fixture proves blocks travel together and the independently-resampled Q-27 anti-pattern is **caught** |
| 5 | C | Generator and draw discipline pinned: `default_rng(seed)` (PCG64), block-index draws the only primary-stream consumer, child streams for sensitivity and comparator; `BootstrapResult` records seed key, generator identity, replicate hash; same-seed/different-seed hash controls; a bare call without `seed` is a `TypeError` by signature |
| 6 | C | `block_hours` and `replicates` live in `experiment.yaml` and are passed explicitly; the signature amendment removing both defaults is **proposed at the gate, not applied** — recorded as an amendment owed to `component-methods.md`; the 48-hour sensitivity is a predeclared named run on its own child stream, labelled sensitivity, never merged into the confirmatory interval |
| 7 | B | The **percentile interval** (2.5th/97.5th percentiles of the 10,000 replicate statistics) is **proposed and routed to the gate as a scientific confirmation** — TE §13.6 names no interval-construction method (verified against the source); once confirmed it is recorded in `experiment.yaml` beside the 0.95 level. Proposed here, **not decided here** |
| 8 | C | The widening guard is a runtime raise with an exact comparator: same masked data, same block length, same 10,000 replicates, derived child-stream seed; narrower-or-equal raises `BootstrapError`; comparator numbers recorded as guard evidence on `BootstrapResult` and **never serialized as a reported interval**; the within-station substitution is proven caught on the TA-14 fixture; the doubled CPU cost is measured at fixture time against TE §9.3's envelope, never invented |
| 9 | C | The cross-station paired-error correlation is pairwise Pearson on the paired-difference series d_s(t), all three pairs, carried machine-readably on `BootstrapResult`; the series choice (paired differences, not raw errors) goes to the gate as a stated reading; the planted-correlation recovery assertion lands in the fixture |
| 10 | C | `tests/test_bootstrap.py` is scoped as the eight checks plus every named negative control from Q1–Q9, with test-apparatus constants declared as such, scientific values from config even under test, and WS-17/TA-14 evidence emitted machine-readably by the named module |

### Gate items

- **The percentile-method confirmation (Q7 = B)** — a scientific protocol value TE §13.6
  leaves unnamed; proposed as the percentile interval, frozen by the student/supervisor,
  recorded in `experiment.yaml` beside the 0.95 level once confirmed.
- **The Q6 signature amendment** — remove `block_hours=24` and `replicates=10_000` from
  the approved `vector_block_bootstrap` signature, making both required keywords like
  `seed`; **an amendment owed to `component-methods.md`, proposed not applied**. The
  running total, derived not carried, printed before asserted:
  `external-products` R-55 basis **5 across 3 units** + `features-and-splits` **0** +
  `evaluation-and-comparison` **1** (the BLK-08 package, R-103) = **6 across 4 units** —
  **re-verified 2026-08-28** by reading its `business-rules.md` § Amendments owed, which
  prints exactly that derivation — plus **this unit's 2** = **8 across 5 units**.
  *(Updated 2026-08-28: this unit's own owed count rose from 1 to 2 with the R-120
  raise-contract amendment listed as the sixth gate item below; the basis rows were
  re-verified on disk the same day and are unchanged. Total was 7 across 5 units.)*
- **The Q9 series-choice proposal** — the correlation is computed on the paired-difference
  series d_s(t), the reading confirmed at the gate rather than assumed.
- **`experiment.yaml`'s bootstrap fields** — block hours, replicates, CI level, the
  predeclared 48-hour sensitivity run, the interval method once confirmed, **the block
  scheme once confirmed** — config content the gate confirms under the four-config regime.
  **TE §15.3's reduced replicate count is not among them** *(added 2026-08-28 —
  Recommendation 24)*: it is a **constant of the test apparatus** declared in
  `tests/fixtures/scientific_1month/fixture_manifest.yaml` by `fixtures-and-reproducibility`,
  alongside that execution's scored range and realised block counts.
- **The Q3 block-scheme reading — the fifth entry** *(added 2026-08-28 —
  `GOV-2026-08-28-FD-01` Recommendation 26, board option 1)* — **TE §13.6 names no
  block-resampling scheme** at all: not fixed-partition, not moving/overlapping, not
  circular. The **fixed non-overlapping partition** is the **proposed** reading — the
  plainest reading of §13.6's "24-hour blocks" and the one its divisibility-friendly framing
  implies — with the **moving-block (Künsch) scheme** named as the alternative. The choice is
  not cosmetic, and the numbers are derived and printed so the owner can see the cost: over
  the **DEC** scored range (2–31 December, **720 h**) at a 24-hour block length, the fixed
  partition yields **30 resampling units**, while a moving-block scheme yields
  **720 − 24 + 1 = 697** overlapping candidate blocks. Block-level variance estimated from 30
  units is **coarse**, which makes the 95% percentile interval materially **wider and
  noisier**, and it is also the configuration most exposed to the Q8 widening comparison,
  because a small block count inflates the Monte Carlo variability of the interval's
  endpoints. **Confirmed by the student/supervisor before G-05** (the scheme sits inside the
  evaluation code G-05 freezes), then recorded in `experiment.yaml` beside the block length
  and CI level; `BootstrapResult` records the confirmed **scheme and the realised block
  count** (`domain-entities.md` §§ 2 and 5). **Not settled by this artifact set** — TE §18.2
  bars an artifact filling a scientific-protocol value by its own reading, and this unit
  refused to do exactly that for the interval method one rule later, so settling the scheme
  by assertion would be that inconsistency in the other direction. *Why this entry was
  missing: R-115's own words route the reading to the gate — "Block alignment is **stated at
  the gate as a derivation from the frozen texts** … if the owner reads §13.6 otherwise,
  **the gate is where it surfaces**" — while this list carried four entries and none of them
  was this one, the exact representation-sweep gap `project.md`'s learned rules name and this
  unit's own 2026-08-27 `## Review` finding 1 identified.*
- **The R-120 raise-contract amendment** *(added 2026-08-28 — Recommendation 23)* — the
  widening control's **raise** moves to the TA-14 synthetic fixture TE §13.6 specifies, and
  the real-data comparison becomes a **mandatory disclosure** carrying the measured
  cross-station correlations; the comparator's replicate count is stated as **its primary
  call's** rather than a fixed 10,000. This is a **weakening** of the approved
  `component-methods.md:869-872` raise contract, so it is **an amendment owed, proposed not
  applied** — taking the running total to **8 across 5 units** (5 + 0 + 1 + 2) — and the
  runtime-versus-fixture reading is **routed here rather than asserted**. **The G-06 abort
  policy — what happens if the comparison fails at the locked evaluation — is owed to the
  Supervisor at G-05** and is decided by no artifact in this unit.

### The blockers

- **BLK-03 ↓, BLK-04 ↓, BLK-08 ↓, BLK-09 ↓ (all inherited)** — exit conditions on stage
  3.1, **not closed by anything in this file**; this unit may not complete or exit 3.1
  while any contract is unapproved, and no implementation may proceed while they stand.
  **BLK-08 ↓ bounds the interval's units**: the interval this unit reports is in TECU, and
  until the co-owner adopts its half of the R-103 joint contract, nothing in any design
  returns model output to TECU — Q1's receipt/inverse preconditions make that dependence
  checked rather than silent.
- **G-09 is not signed.** `tests/` holds three modules, none this unit's; `src/` and
  `configs/` are absent. The artifacts specify design only; no answer authorises creating
  `src/evaluation/bootstrap.py` or `tests/test_bootstrap.py`.

### The figures, derived not carried

- **2 owned files** — counted from § 10's `Owns` list: `src/evaluation/bootstrap.py`,
  `tests/test_bootstrap.py`. No stage script: this unit runs inside
  `scripts/07_evaluate_and_report.py`, which `evaluation-and-comparison` owns.
- **1 requirement, 0 untested** — read from the story map's rows, the two upstream
  artifacts agreeing: FR-P1-05-8, whose criterion is eight mechanical checks.
- **Acceptance rows** — **WS-17 and TA-14, both primary** (2 rows), supporting none — the
  story map's one unit with full acceptance coverage, earned in `tests/test_bootstrap.py`
  or hollow.
- **The scored December set** — **2–31 December, 30 days** (FU-7 = A, ruled at
  `features-and-splits`), first 24 h excluded and counted; **inherited here as the `DEC`
  precondition** (Q1, Q3), dividing into exactly 30 whole 24-hour blocks and 15 at 48 h.

### What is NOT decided here

- **No scientific value.** The interval method (Q7), the correlation series (Q9), and the
  `experiment.yaml` fields (Q6) are proposed and routed to the gate; 24 h, 10,000,
  20221201, 95%, and 2–31 December are already frozen and merely encoded.
- **No module creation.** G-09 is not signed; the artifacts specify design only.
- **No blocker closes.** All four inherited exit conditions stand exactly as the register
  rules them.

### Assumptions and open questions, summarized

- **Assumptions carried into the artifacts**: rule numbering opens at R-113 with the
  R-83…R-89 gap inherited as observed; `BootstrapResult` is an intra-package shape and
  this stage's to specify, finalized in `domain-entities.md` after the gate;
  `BootstrapError` is one of the fourteen project exceptions, declared here and importing
  `IntegrityError` from `src/data/config.py`, with `FairnessError` and `LockedTestError`
  imported, not redeclared; `src/evaluation/` is a path grant owned by three units and
  this unit designs `bootstrap.py` only, narrowing nothing of TE §12; the seed 20221201
  reaches this unit as `ConfigSnapshot.seeds`' bootstrap entry through `07`'s call site,
  the key name being `foundation`'s surface.
- **Verification obligations owned here**: the mask/stamp/receipt/TECU boundary
  preconditions (Q1); the point-estimate equality check and pooled-weighting control (Q2);
  the divisibility, misalignment and boundary-crossing raises (Q3); the same-indices
  vector assertion, zero-support raise and declared-rule gap fixture (Q4); the
  same-seed/different-seed hash controls and recorded generator identity (Q5); the
  never-merged sensitivity separation (Q6); the widening guard with its quarantined
  comparator and caught-substitution control (Q8); the planted-correlation recovery
  assertion (Q9); `tests/test_bootstrap.py`'s full negative-control set and evidence
  emission (Q10).
- **Governance dependencies owned outside**: BLK-03's limbs (`models-and-baselines`);
  BLK-04's limbs and BLK-09's `train_start` resolution (`features-and-splits`); BLK-08's
  co-owner adoption of the R-103 joint contract; the Q6 signature amendment (ruled at the
  gate); the Q7 interval-method and Q9 series confirmations (student/supervisor);
  `experiment.yaml`'s bootstrap fields (gate-confirmed, frozen under the four-config
  regime); acceptance-row evidence formats for WS-17/TA-14 (stage 3.2, via Vision §15.2
  if any row text needs amendment); G-05's freeze of the evaluation code this stage
  designs (Supervisor); and the measured-not-invented CPU/memory figures, frozen only at
  fixture time per §15.1.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The receipt is recorded, the three design artifacts are generated on these answers, and the adversarial review follows.

- Request changes
   > **Impact**: Nothing is recorded or generated; state what to change and the summary is re-presented.

> **💡 Recommendation**: **Looks correct** — every figure above is derived from this file's own sources rather than carried (the R-113 opening and the 7-across-5 amendment total were both re-derived against the sibling's artifacts today), every scientific choice is either already frozen or routed to the gate as a proposal, and all four blockers stay open exactly as the register rules them.

[Answer]: Looks correct
