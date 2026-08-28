# Business Rules — `statistical-inference`

**Unit** `statistical-inference` · **Kind** `library` · **Complexity** M ·
**Deployment** embedded · **Depends on** `evaluation-and-comparison`

The prohibitions this unit enforces, each with what it rejects, what it raises, and the
negative control that proves the rejection happens.

**This project's affirmed methodology is a negative control paired with every hard rule** —
a test that proves the violation is *caught*, not only that the happy path works.

**Every rule here guards the thesis's uncertainty statement on its single most protected
number.** A violation does not crash a pipeline; it prints a systematically narrower
interval around the confirmatory estimand with a plausible width — TC-19's named failure,
the exact substitution Q-27 rejected.

**Rule IDs continue the single sequence.** `foundation` R-01…R-17, `governance-guards`
R-18…R-29, `acquisition` R-30…R-43, `inventory-and-registry` R-44…R-53, `external-products`
R-54…R-63 (plus R-54a), `target-standardization` R-64…R-73, `features-and-splits` R-74…R-82
(plus R-76a), `models-and-baselines` R-90…R-102, `evaluation-and-comparison` R-103…R-112 —
so this unit opens at **R-113**. The sibling's closing ID was **re-derived 2026-08-27 by
grepping its `business-rules.md` headings (R-103…R-112, ten headings)**, not carried. **The
R-83…R-89 gap between `features-and-splits` and `models-and-baselines` is inherited as
observed, not explained**: if it was a reservation, or per-unit numbering was intended, say
so at the gate and these artifacts renumber.

**Four inherited exit conditions stand on this stage: BLK-03 ↓, BLK-04 ↓, BLK-08 ↓,
BLK-09 ↓.** None is owned here; none closes here. **BLK-08 ↓ bounds the interval's units
for `ABL-DIFF` only** — **D-27** (2026-08-24, `evidence/DECISIONS.md`) froze that the
primary configuration's train-only transform touches target-**derived inputs**, not the
target, which stays **raw TECU**, so **the primary path needs no inverse transform** and
the bootstrap interval is computed on the quantity the model emits. The primary interval's
**TECU status is therefore a recorded fact, not an open dependency**; the residual under
BLK-08 ↓ is **`ABL-DIFF` alone**, whose inverse obligation TE §7.2 keeps in full. R-113's
precondition 4 stays as the check that proves it rather than assumes it. This unit **may
enter** 3.1, **may not complete or exit** it while any contract is unapproved, and **no
implementation may proceed while they stand** (`GOV-2026-08-22-REM-01` Rec 2, extended to
BLK-08/BLK-09 on 2026-08-23). **G-09 is not signed**: no module named here may be created.

> **Remediation, 2026-08-28 — `GOV-2026-08-28-FD-01`, verdict FAIL.** Six owner-ruled
> items were applied to this artifact set. Each carries its own dated note at the site it
> changed: **Recommendation 23** (R-120 — the widening guard's raise is restored to
> "narrower", relocated to fixture time, and paired with a mandatory real-data disclosure;
> the runtime-versus-fixture reading is routed to the gate); **Recommendation 24** (R-115,
> R-118, R-120, R-122 — TE §15.3's reduced-replicate fixture bootstrap made representable:
> the comparator tracks its primary's replicate count, control (17) is scoped to
> confirmatory runs, and the divisibility claim is corrected with the ranges it was derived
> over); **Recommendation 26** (§ Gate items in `functional-design-questions.md` gains the
> Q3 block-scheme reading as a fifth entry; the scheme and realised block count are
> recorded on `BootstrapResult`); **Recommendation 7 as narrowed** (D-27 cited; the primary
> interval's TECU status is a recorded fact and the residual is `ABL-DIFF` only);
> **Recommendation 8** (`PartitionError` promoted to `foundation` R-01's fifteenth; R-105's
> `partition_id`-mismatch limb corrected); **Recommendation 40** (TE §9.3 is a **storage**
> budget, not a memory ceiling; a change record against `services.md` and `unit-of-work.md`
> is owed). **No blocker closes and no scientific value is decided by any of them.** The
> `## Review` box in `business-logic-model.md` is a dated record of the 2026-08-27 pass and
> is preserved byte-for-byte, so its re-derived control count (**23**) predates the
> twenty-fourth control this remediation adds at R-120.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 10 — the `Owns` list (2 files), the boundary, the 1 requirement, the acceptance rows, the three implementation notes (Q-27 rejection; heaviest CPU cost inside TE §9.3's envelope; the ADR-05 seed carve-out); the four inherited blockers with the exit-condition ruling.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Table 1's FR-P1-05-8 row, Table 2's WS-17 and TA-14 rows (both primary), § Per-unit coverage summary (1 / 0 / WS-17, TA-14 / —).
- `../../../inception/requirements-analysis/requirements.md` FR-P1-05-8 — the eight enumerated mechanical checks and the 48-hour sensitivity.
- `../../../inception/application-design/component-methods.md` — the approved `vector_block_bootstrap` signature and raise contract at `:869-872` (quoted verbatim in `business-logic-model.md` W-1, where the R-120 amendment sits beside it rather than replacing it); § Open (`BootstrapResult` unspecified, intra-package under § Depth); § Assumptions (**as written**: fourteen exceptions declared where raised until 3.1 places them — the figure Recommendation 8's ruling amends to fifteen; cited as that artifact's own text, not as the live enumeration).
- `../evaluation-and-comparison/functional-design/business-rules.md` — R-104 (transformed-space refusal at every metric entry point), **R-105 as corrected 2026-08-28 under `GOV-2026-08-28-FD-01` Rec 8**: a `partition_id` mismatch raises **`PartitionError`** (matching `models-and-baselines` R-92), while an absent stamp or a `transform_id` mismatch raises `LeakageError`, and a wrong-partition mask raises `FairnessError` — R-107 (registered-mask check), R-108 (the estimand's ordered contract and step-1 path), R-109 (DEC hash receipt; scored range exactly 2–31 December), R-110 (emit-from-the-producing-path), R-112 (`vector_block_bootstrap` recorded as belonging to this unit); § Amendments owed (**5 + 0 + 1 = 6 across 4 units**, the basis this unit extends); `domain-entities.md` § 8 (exception placement); its narrowing of the BLK-08 resolver to **`load_inverse(transform_id) -> Inverse`**, in parallel under Rec 7.
- `evidence/DECISIONS.md` — **D-27** (2026-08-24, reading): the primary configuration's train-only transform touches target-**derived inputs**, not the target, which stays **raw TECU**; the primary path needs no inverse transform and the bootstrap interval is computed on the quantity the model emits; `ABL-DIFF` retains its inverse obligation in full (TE §7.2). **D-28** (2026-08-28, freeze): the G-06 locked-test scored set is **2–31 December 2022, 30 days**, first 24 h excluded and counted — the record behind FU-7 = A, with the Vision §8.2 / TE §7.1 authority conflict disclosed. **D-14** (freeze): the one-month all-station scientific fixture is **March 2022, 2022-03-01 to 2022-03-31 inclusive** — the window whose divisibility R-115 now states. **D-11** (freeze): the seven-day plumbing window, 2022-11-01 to 2022-11-07.
- `governance/reviews/GOV-2026-08-28-FD-01.md` — Recommendations 7 (as narrowed to `ABL-DIFF` on D-27's strength), 8 (`PartitionError` promoted to R-01's fifteenth), 23, 24, 26 and 40, with the owner rulings recorded at the top of this file.
- `../features-and-splits/functional-design/` — **FU-7 = A** (2–31 December, 30 days, first 24 h excluded and counted).
- `../models-and-baselines/functional-design/business-rules.md` — R-91 (the `expected_seeds`-from-`ConfigSnapshot` shape, this unit's seed parameter cited there as precedent), R-92 (the (`station`, `interval_start_utc`) alignment key).
- `../foundation/functional-design/business-rules.md` — R-01 **as amended 2026-08-28 under `GOV-2026-08-28-FD-01` Rec 8**: the enumeration grows from fourteen to **fifteen** with **`PartitionError`** promoted into it, all deriving from `IntegrityError` (base in `src/data/config.py`); **`BootstrapError` is named among those raised by other units** — one of the enumerated set, not a unit-local addition; each raising unit declares its own as subclasses; every raise names the file or resource and the violated expectation — plus R-10 and § Stage entry contract. **Disk state, checked 2026-08-28:** `foundation`'s file still reads "all fourteen" and does not yet list `PartitionError`; the amendment is the owner's ruling being applied in parallel, so this unit cites the amended enumeration and records the dependency rather than asserting the sibling's text is already on disk. ⚠ **SWEPT 2026-08-28 on the resume pass — this disk-state claim is SUPERSEDED.** `foundation` R-01 **has been amended** and now reads **fifteen**, with `PartitionError` promoted into the enumeration, the count restated as **derived and printed** rather than carried in prose, and `InverseTransformError` **explicitly disposed** — not a sixteenth, riding R-01's *"any future integrity-related exception"* clause, on the stated ground that the two units raising it agree on its condition and meaning, so nothing needs reconciling. Verified at `foundation/functional-design/business-rules.md` R-01 (the amendment row, the superseded-wording box, and the `InverseTransformError` box). **The dependency this sentence recorded is discharged; any open item stated alongside it is NOT** — see the sentence it accompanies.
- `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` **§15.3** (line 913, verbatim): *"Fixture 2 must run the complete ladder across all three stations with pooled comparison-wide masks, the full benchmark join at evaluation time, and **one bootstrap execution at reduced replicate count for timing**."* — the requirement R-118 and R-122 now carry.
- `aidlc/spaces/default/memory/project.md` § Mandated/Forbidden and `team.md` — the vector time-block bootstrap rule (TE §13.6; TC-19 `binding: hard`), NEVER substitute a within-station or naive bootstrap, seeds from `seeds.yaml` (NFR-DET-01, TC-21), TC-03e, the negative-control methodology, TC-01, TE §18.3's stop-and-report posture.
- `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §13.6 (including its final sentence, quoted verbatim in R-120), §13.7, **TE §9.3 — read at line 532, titled "Storage budget" and self-described as "A capacity plan, not a scientific freeze gate"; always written "TE §9.3" here because **Vision §9.3** is a different section (Geomagnetic Regimes and Storm Events, Vision line 896)**, §9.2 (records "peak memory" with **no numeric value**), §7.2, §15.1/§15.2, **§15.3**, §18.2/§18.3.
- Workspace inspection, 2026-08-27: `tests/` holds three modules, none this unit's; `src/` and `configs/` absent.
- `functional-design-questions.md` (**Q1 through Q10**, answered; summary receipted), `business-logic-model.md`, `domain-entities.md`.

---

## R-113 — The bootstrap is a metric entry point in full

**Rule (Q1 = C).** `vector_block_bootstrap` **asserts its own preconditions rather than
trusting any caller's call order** — TE §14 expressly reads bootstrap artifacts into
`04_results_and_figures.ipynb`, so the one-specific-caller gap R-104 was written to close
applies here verbatim. Before any draw:

1. `mask` is a **registered frozen mask for the members' declared comparison set** —
   R-107's check, imported intra-package from `evaluation-and-comparison` — or
   **`FairnessError`**.
2. Both `Prediction`s carry **non-`None`, mutually agreeing** `partition_id`/`transform_id`
   stamps (**R-105 as corrected**): a **`partition_id` mismatch raises `PartitionError`**,
   matching `models-and-baselines` R-92 exactly; an **absent (`None`) stamp of either kind,
   or a `transform_id` mismatch, raises `LeakageError`**; a mask whose recorded
   `partition_id` differs from the members' **raises `FairnessError`**.

   > **Applied 2026-08-28 — `GOV-2026-08-28-FD-01` Recommendation 8.** The earlier text
   > imported R-105 *"as written"* and thereby inherited the taxonomy disagreement the
   > sibling's own reviewer had logged as an open Major finding: R-105 raised
   > `LeakageError` for a `partition_id` mismatch while R-92 raised `PartitionError` for
   > the identical condition, so a test asserting `pytest.raises(PartitionError)` passed at
   > `06` and failed at `07`. The owner ruled Rec 8's option (1): **`PartitionError` is
   > promoted into `foundation` R-01's enumeration as its fifteenth**, and R-105's
   > `partition_id`-mismatch limb is corrected to raise it. This rule now cites the
   > **corrected** R-105 and the **amended** R-01 rather than importing the disagreement.
   > `PartitionError` is **imported here, not declared** — its declaring unit is
   > `models-and-baselines`, its raise site at this boundary is the stamp check.
   > **Dependency, stated rather than assumed:** `foundation`'s file on disk still reads
   > "all fourteen" and omits `PartitionError`, and `evaluation-and-comparison`'s R-105
   > still raises `LeakageError` for the mismatch; both are being corrected in parallel
   > under the same ruling. If either lands differently, this precondition follows the
   > amended R-01 and the corrected R-105, not this paragraph.
3. Evaluating the **`DEC`** partition requires the recorded **prediction-hash receipt
   re-verified before any draw** (R-109 limb 1): absence, hash mismatch, or a receipt
   timestamp not preceding the call **raises `LockedTestError`**. The DEC mask's assertion
   that the scored range is exactly 2–31 December (R-109 limb 3; FU-7 = A) is inherited as
   a precondition.
4. **Transformed-space input is refused** (R-104): **`InverseTransformError`** unless the
   resolved transform is declared non-target-touching or the inversion lineage shows the
   inverse applied — so the interval is **TECU-denominated by check, not by assumption**.

   > **Applied 2026-08-28 — `GOV-2026-08-28-FD-01` Recommendation 7, as narrowed by the
   > owner to `ABL-DIFF` on D-27's strength.** **D-27** (2026-08-24, `evidence/DECISIONS.md`
   > — a reading of frozen text, no scientific value set) froze that the primary
   > configuration's train-only transform acts on target-**derived input features** —
   > `vtec_lag_1h/2h/3h/24h` and `vtec_seq_24`, per the TE §6.2 **feature** dictionary —
   > while the target itself remains **raw TECU**; TE §7.2's `ABL-DIFF` row reads "Primary
   > remains: Raw TECU". Two consequences land here. **(a) The primary path needs no inverse
   > transform**, so this precondition **passes by the non-target-touching branch** and the
   > bootstrap interval is computed on the quantity the model emits: **the primary
   > interval's TECU status is a recorded fact, not an open dependency.** **(b) The residual
   > under BLK-08 ↓ is `ABL-DIFF` alone** — the sole configuration that transforms the
   > target, which TE §7.2 requires to inverse-transform to absolute TECU before any metric
   > with its error propagation recorded. Precondition 4 is therefore **discharged for the
   > primary path and open only for `ABL-DIFF`**, where it is the check that fires if an
   > un-inverted first-difference prediction reaches the bootstrap.
   >
   > The precondition is **kept, not deleted**: D-27 is a reading taken before any code
   > exists, and its own § Limitation states that a model path found to scale the target
   > contrary to it is *"a contradiction to surface"*, not a licence to adjust the target
   > contract. This check is what surfaces it. `evaluation-and-comparison` is narrowing its
   > resolver to **`load_inverse(transform_id) -> Inverse`** in parallel under the same
   > Recommendation, exposing only `inverse(frame)` so ADR-11's removal of a cross-package
   > `apply` surface stays structural; this unit consumes the inversion **lineage**, never a
   > transform object, and gains no import edge either way.

The interval and the scalar it brackets thereby provably describe the same data in the same
units, whatever the caller — script, notebook or test. Costs two imported precondition
checks; all four are intra-`src/evaluation` calls under the path grant (R-112), no new
dependency edge.

**Negative controls.** (1) An unregistered or ad-hoc mask → **`FairnessError`**. (2) A
stamp defect on either `Prediction`, asserted **by discriminated type**: a `partition_id`
mismatch → **`PartitionError`**; an absent (`None`) stamp of either kind or a
`transform_id` mismatch → **`LeakageError`** — one control, two asserted types, so the
R-105/R-92 agreement is proven at this boundary rather than claimed. (3) A `DEC` call with
the receipt absent, the file hash mismatching, or the timestamp not preceding the call →
**`LockedTestError`**. (4) An un-inverted target-touching (transformed-space) `Prediction`
at the bootstrap boundary → **`InverseTransformError`** — reachable only through
`ABL-DIFF` after D-27, and asserted on a synthetic first-difference `Prediction` rather
than on the primary path, which D-27 records as raw TECU.

**Control that must *not* fire:** the G-06 path — members stamped `(DEC, ...)`, the
registered DEC mask, a verified receipt → **passes**.

**Acceptance.** Contributes to WS-17/TA-14 via `tests/test_bootstrap.py` (R-122); the
precondition machinery consumes the sibling's rows (WS-16, TA-11, TA-18) without claiming
them.

## R-114 — One copy of the estimand arithmetic: precompute once, resample the precomputed

**Rule (Q2 = C).** The per-(station, hour) paired squared-error differences are computed
**once**, on masked rows only, **through the same step-1 code path R-108's
`paired_loss_differential` uses** — pairing per station-hour on the
(`station`, `interval_start_utc`) alignment key (R-92) before differencing (check 1).
Replicates resample **blocks of those precomputed differences** and reapply **only steps
2–3** of R-108 (per-station mean, **benchmark minus model** orientation preserved;
unweighted three-station mean — check 5's equal-station weighting). No differencing
arithmetic is reimplemented in `bootstrap.py`: the replicate statistic is the estimand **by
construction**, and differencing runs once, not 10,000 times.

**The equality control.** The bootstrap's own full-data point estimate must equal
`paired_loss_differential`'s scalar on the same mask **exactly** — a deterministic CPU
transformation under §13.7's exact-equality rule — or **`BootstrapError`** is raised. The
one-copy claim is a checked invariant, not an architecture diagram.

**Negative controls.** (5) A full-data point estimate differing from
`paired_loss_differential`'s scalar by any amount → **`BootstrapError`**. (6) A pooled
row-weighted replicate statistic → **fails** on the fixture with asymmetric per-station row
counts — the same fixture R-108's control (16) uses, applied to the replicate path.

**Acceptance.** TA-14 (the reproducible output presupposes the bracketed statistic is the
estimand); checks 1 and 5 of FR-P1-05-8.

## R-115 — The block grid: fixed non-overlapping partition, and what a boundary violation raises

**Rule (Q3 = C).** The scored range is partitioned into **contiguous, non-overlapping
`block_hours`-hour blocks aligned to its start** — for DEC: 00:00 UTC boundaries,
**exactly 30 whole blocks** over the 2–31 December scored set (FU-7 = A, recorded as
**D-28**), **exactly 15** at the 48-hour sensitivity. A replicate draws **exactly N blocks
with replacement**, N being the number of whole blocks in the range. `BootstrapResult`
records **the scheme and the realised block count**, so the partition actually used is an
auditable fact rather than an inference from `block_hours`. Two structural raises:

1. A scored range **not evenly divisible** by the block length **raises `BootstrapError`**
   rather than silently truncating or padding a partial block. It exists so a changed range
   surfaces as an error, not a quiet reweighting.

   > **Corrected 2026-08-28 — `GOV-2026-08-28-FD-01` Recommendation 24.** The earlier text
   > claimed "for the frozen ranges it never fires (30/1 and 30/2 both divide)". That claim
   > was **derived over the DEC scored range only** and is false as a general statement: the
   > 48-hour sensitivity is **indivisible** over three other ranges in play. Derived
   > programmatically, printed before asserted:
   >
   > | Range | Hours | 24 h | 48 h |
   > |---|---|---|---|
   > | **DEC** scored, 2–31 Dec (D-28, 30 d) | 720 | **30 blocks** | **15 blocks** |
   > | **Fixture 2** raw window, 1–31 March 2022 (D-14, 31 d) | 744 | 31 blocks | **INDIVISIBLE** (15.5) |
   > | Fixture 2 after a 24-h exclusion (30 d) | 720 | 30 blocks | 15 blocks |
   > | **F1 validation, April** after the 24-h exclusion | 696 | 29 blocks | **INDIVISIBLE** (14.5) |
   > | **F4 validation, November** after the 24-h exclusion | 696 | 29 blocks | **INDIVISIBLE** (14.5) |
   > | F2 validation, July after the 24-h exclusion | 720 | 30 blocks | 15 blocks |
   > | F3 validation, October after the 24-h exclusion | 720 | 30 blocks | 15 blocks |
   > | **Plumbing fixture** raw window, 7 days (D-11) | 168 | 7 blocks | **INDIVISIBLE** (3.5) |
   >
   > The corrected claim: **limb 1 never fires on the DEC range at either block length**,
   > which is the range the confirmatory interval and its 48-hour sensitivity are computed
   > over — and it **does** fire, by design, on the raw March fixture window, on the April
   > and November validation months after their 24-h exclusion, and on the raw 7-day
   > plumbing window, at 48 h. That is the raise doing its job, not a defect: any of those
   > ranges reaching a 48-hour bootstrap is a range change that must surface.
   >
   > **The consequence for TE §15.3's fixture bootstrap** (see R-118): its **scored range
   > must be declared**, because 744 h and 720 h differ at 48 h. §15.3 asks for **one**
   > bootstrap execution for timing and names no block length, so the declared fixture run
   > is a **24-hour** execution, where every range above divides. Should a 48-hour fixture
   > execution ever be declared, the fixture's scored range must be the post-exclusion 720 h
   > or limb 1 raises — stated here so the choice is visible rather than discovered at
   > `build-and-test`.
2. Any block extending **outside the mask's scored range** **raises `BootstrapError`**. A
   31-block December containing 1 December is unrepresentable upstream (R-109 limb 3's
   mask assertion) **and additionally refused here** — redundancy at the locked boundary is
   by design.

Block alignment is **stated at the gate as a derivation from the frozen texts** (TE §13.6's
fixed-block wording read plainly), not decided silently; if the owner reads §13.6
otherwise, the gate is where it surfaces.

> **Applied 2026-08-28 — `GOV-2026-08-28-FD-01` Recommendation 26 (board option 1).** The
> sentence above routed the reading to the gate while `functional-design-questions.md`
> § Gate items listed only four entries — the Q7 percentile-method confirmation, the Q6
> signature amendment, the Q9 correlation-series proposal and `experiment.yaml`'s bootstrap
> fields — so **Q3's block-scheme reading reached no punch-list entry** while three lesser
> readings did. That is the representation-sweep failure `project.md` names: a claim
> asserted in a rule body but absent from the itemized list the owner actually works from.
> **The Q3 block-scheme reading is now § Gate items' fifth entry.**
>
> The choice is not cosmetic, and the numbers are stated so the owner can see the cost.
> Over the DEC scored range (720 h) at a 24-hour block length: a **fixed non-overlapping
> partition yields 30 resampling units**; a **moving-block (Künsch) scheme yields
> 720 − 24 + 1 = 697 overlapping candidate blocks** (both derived, printed before
> asserted). Block-level variance estimated from 30 units is coarse, which makes the 95%
> percentile interval materially wider and noisier, and it is also the configuration most
> exposed to R-120's widening comparison, because a small block count inflates the Monte
> Carlo variability of the interval's endpoints. The fixed non-overlapping partition
> **remains the proposed reading** — the plainest reading of §13.6's "24-hour blocks" and
> the one its divisibility-friendly framing implies — with the moving-block scheme named as
> the alternative. **It is not settled here.** TE §18.2 bars an artifact settling a
> scientific-protocol value by its own reading, and this unit refused to do exactly that
> for the interval method one rule later (R-119); settling the scheme by assertion would be
> the same inconsistency in the other direction.

**Negative controls.** (7) A scored range not evenly divisible by `block_hours` →
**`BootstrapError`**. (8) A misaligned or boundary-crossing block → **`BootstrapError`**.
(9) A DEC scored set containing a 1 December row → refused — upstream by the mask's R-109
limb 3 assertion (**`LockedTestError`**) and additionally here as a grid-alignment
violation.

**Acceptance.** TA-14 (reproducible 24-hour output); check 3 of FR-P1-05-8.

## R-116 — The vector property and the declared rule for missing pairs

**Rule (Q4 = C).** The resampling unit is a **vector block carrying all three stations at
the same timestamps** (check 2), enforced as: **the same resampled block indices applied to
all three stations simultaneously** — the property that preserves cross-station dependence
and the thing a within-station resampler breaks. Because the comparison-wide mask is an
intersection per (station, hour) and a station can be absent at hours where another is
present (NICO holds 96.4% of hourly bins), a 24-hour window generally holds a **ragged**
three-station vector; the **declared rule** (check 7, declared here at last):

1. a block carries, **per station, exactly the masked rows falling inside its window** —
   arithmetic on what the frozen mask already says, never a new exclusion policy and never
   a narrowing of the scored population (the interval and the point estimate describe the
   same frozen mask);
2. per-replicate per-station means use whatever masked rows the drawn blocks contain;
3. a replicate in which any station ends with **zero** masked rows **raises
   `BootstrapError`** — the equal-station mean is undefined — a structural guard December's
   measured coverage makes practically unreachable, naming the station and window per
   R-01's constructor contract.

**Negative controls.** (10) A zero-support station in a replicate → **`BootstrapError`**,
naming the station and window. (11) **Independently resampled per-station block indices —
the Q-27 anti-pattern, named** — → **caught**: directly by a same-indices assertion in
`tests/test_bootstrap.py`, and behaviourally by R-120's widening guard firing on the
narrower interval it produces. (12) Gap handling departing from the declared rule on the
TA-14 gapped fixture (known cross-station and temporal correlation, gaps injected in one
station's series) → **fails**.

**Control that must *not* fire:** a real DEC-shaped fixture with ragged per-station
coverage but nonzero support in every replicate → **passes** — the raise must not make
December's measured coverage unrunnable.

**Acceptance.** TA-14 (verified on synthetic correlated data); checks 2 and 7 of
FR-P1-05-8.

## R-117 — Seed sourcing, generator identity, and what "reproduces exactly" pins

**Rule (Q5 = C).** The seed is **required and passed in** — `ConfigSnapshot.seeds`'
bootstrap entry from `configs/seeds.yaml`, the separately frozen **20221201** (TE §13.6,
§13.5; not part of D-122's item set), **never defaulted and never inlined** (TC-03e) — and
the function builds **its own local generator** (the ADR-05 carve-out, a design decision).
The contract pins what a seed alone cannot:

1. **NumPy `default_rng(seed)` (PCG64)** is the generator;
2. **block-index draws are the only consumer of the primary stream**; the 48-hour
   sensitivity (R-118) and the widening comparator (R-120) draw from **deterministically
   derived child streams** (seed-sequence spawn), so no consumer can perturb another's
   draws;
3. `BootstrapResult` records the **seed key consumed, the generator identity, and the
   replicate hash** — WS-17's evidence emitted by the producing path (R-110's pattern), an
   assertable artifact fact rather than a log line;
4. a call without `seed` is a **`TypeError` by signature** — the never-defaulted rule is
   unrepresentable rather than checked.

These pins are engineering contracts, not scientific constants: the scientific value
(20221201) stays in `seeds.yaml`; the generator name is no more a scientific constant than
the language pin. Exact reproduction becomes implementation-independent and
refactor-stable — "reproduces exactly" no longer means "reproduces on the machine that
wrote the hash".

**Negative controls.** (13) A different seed → a **different** replicate hash, asserted.
(14) A same-seed rerun → the **identical** replicate hash, asserted (§13.7 exact
equality). (15) A call without `seed` → **`TypeError`** by signature.

**Acceptance.** **WS-17 (primary)** — "reproduces exactly from seed 20221201", evidence:
the replicate hash from seed 20221201 emitted by the producing path; TA-13/TA-26 belong to
`foundation` and `models-and-baselines` (NFR-DET-01) — the carved-out bootstrap seed is
context there, not a row here.

## R-118 — The frozen numbers live in config; the signature amendment is proposed, not applied; the sensitivity is a predeclared named run

**Rule (Q6 = C).** `block_hours` and `replicates` are frozen scientific protocol values (TE
§13.6) and therefore **declared in `experiment.yaml` and passed explicitly from
`ConfigSnapshot` at every call** (TC-03e) — the signature's two defaults are never
exercised. The approved contract's defaults are an inconsistency the project already ruled
on once in the same signature (the seed); the amendment finishing that thought — **remove
`block_hours=24` and `replicates=10_000`, making both required keywords like `seed`** — is
**RAISED AT THE GATE as an amendment owed to `component-methods.md`, proposed not applied**
(changing an approved contract by assertion is refused practice; § Amendments owed derives
the total).

**The 48-hour sensitivity** (TE §13.6; TA-14) is a **predeclared named run in
`experiment.yaml`** — the TE §7.2 ablation-registration discipline applied to a required
sensitivity: same seed 20221201 on its **own derived child stream** (R-117), `block_hours
= 48` (15 blocks on DEC), its result **labelled sensitivity and never merged into or
substituted for** the 24-hour confirmatory interval.

**TE §15.3's reduced-replicate fixture bootstrap.** §15.3 requires, verbatim, that fixture
2 run *"one bootstrap execution at **reduced replicate count** for timing"*. That execution
is **not** a confirmatory run and **not** a scientific value: it exists solely to time a
smoke path and is never reported. Its replicate count is therefore declared **as a constant
of the test apparatus in `tests/fixtures/scientific_1month/fixture_manifest.yaml`** — on
R-122's authority, the same route R-122 already uses for the planted correlation, the gap
pattern and the per-station row counts, and explicitly **not** a fifth `experiment.yaml`
field. `fixtures-and-reproducibility` owns that declaration; this unit's side is the three
statements below.

> **Applied 2026-08-28 — `GOV-2026-08-28-FD-01` Recommendation 24 (board option 2).**
> Derived: `reduced-replicate`/`reduced replicate` appears **once** across all twelve units
> — a Sources citation of §15.3 in `fixtures-and-reproducibility/business-rules.md:67` —
> and **zero** times in this unit, which owns `vector_block_bootstrap`. Two of this unit's
> own rules made the mandated execution unrepresentable, and both are fixed:
>
> **(a) R-120's comparator tracks its primary's replicate count, not the literal 10,000.**
> Applied at R-120 limb 1. A reduced-replicate primary compared against a full-replicate
> comparator is not like-for-like and **biases the comparison toward firing**, because a
> 2.5/97.5 percentile interval is unstable at low replicate counts — the reduced primary's
> endpoints move more than the full comparator's, which is an artefact of the replicate
> count rather than a property of the resampling scheme.
>
> **(b) Control (17) is scoped to the confirmatory run.** It fires on a **confirmatory**
> interval whose recorded `block_hours` or `replicates` differs from the config-declared
> values, and **does not fire** on the declared fixture run, whose reduced count comes from
> the fixture manifest by design and is labelled as a timing execution rather than a
> confirmatory interval. Without that scope the fixture run would fail the very control
> written to catch dead-default drift — a control firing on the one case it was never
> about.
>
> **(c) The fixture bootstrap's scored range is stated** so R-115 limb 1's divisibility is
> checkable: R-115's dated note prints the arithmetic for the raw March window (744 h) and
> its post-exclusion form (720 h), and records that the declared fixture execution is at a
> **24-hour** block length, where both divide. R-115's "never fires" claim is corrected
> there to name the ranges it was derived over.
>
> Rejected readings, recorded: declaring the reduced count as a second `experiment.yaml`
> field (Rec 24 option 1) would make a timing smoke-test look like a scientific run in the
> registry unless the label were explicit, and adds a gate-confirmed field for a value that
> is never reported; reading §15.3 as satisfied by the full 10,000-replicate run at fixture
> data scale (option 3) defeats §15.3's stated purpose, which is timing.

**Negative controls.** (16) A sensitivity result merged into or substituted for the
confirmatory interval → **fails** the labelling assertion (the confirmatory interval's
recorded `block_hours` must equal the config-declared 24; the sensitivity's, 48; distinct
labelled fields, never one field). (17) **On a confirmatory run**, a recorded `block_hours`
or `replicates` differing from the config-declared values → **fails** — the dead-default
drift channel made visible. Scoped to confirmatory runs, so the declared reduced-replicate
fixture execution (§15.3) does not trip it; the paired assertion is that the fixture run's
recorded count equals the **fixture manifest's** declared value.

**Acceptance.** TA-14 (the 48-hour sensitivity is named in its row); check 4 of
FR-P1-05-8. The fixture execution contributes to **WS-20 / TA-17** through
`test_clean_run.py`, which `fixtures-and-reproducibility` owns — named here as the
consuming row, not claimed.

## R-119 — The interval method is proposed at the gate, and the design is method-parametric

**Rule (Q7 = B).** TE §13.6 says *"report 95% confidence intervals"* and stops — verified
against the source: **no interval-construction method is named**. Percentile, basic and BCa
intervals can differ materially on 10,000 replicates of a skewed statistic, so the choice
is a scientific protocol value: §18.2 bars an implementer filling it by convenience. The
**percentile interval** — the 2.5th and 97.5th percentiles of the 10,000 replicate
statistics — is **PROPOSED and routed to the gate as an explicit scientific
confirmation**, to be recorded in `experiment.yaml` beside the 0.95 level **once
confirmed**. It is exactly reproducible from the replicate set alone, which keeps WS-17's
replicate-hash evidence sufficient to re-derive the interval. **Proposed here, not decided
here** — the confirmation is the student/supervisor's.

**The design is method-parametric**: interval construction is a named component reading its
method from `experiment.yaml`, so a BCa ruling at the gate changes **that component, not
the whole unit**. If implementation is reached with the method unconfirmed, the posture is
TE §18.3's — **stop and report rather than choose a default**.

**Negative control.** (18) An unrecognized, absent or unconfirmed interval-method value at
the interval-construction component → **refused** (`BootstrapError`, naming the config
field and the violated expectation) — the stop-and-report posture made executable rather
than procedural. (The four-config zero-`TBD` preflight at stage entry is `foundation`'s
step 3 and is consumed, not duplicated.)

**Acceptance.** ⚠ No row of its own — the method confirmation is a gate item; once
confirmed and recorded in `experiment.yaml`, a later change is a visible protocol change,
not an edit.

## R-120 — The widening guard: the raise lands at fixture time, the real-data comparison is a mandatory disclosure, and the comparator stays exact and quarantined

**Rule (Q8 = C, amended 2026-08-28).** The comparison itself runs **everywhere the
bootstrap runs** — it is computed on every call and its evidence is always emitted. What
differs is what a failure **does**:

- **At fixture time, a failure raises.** On the TA-14 synthetic fixture — a dataset with
  **known** cross-station and temporal correlation, where widening holds **by
  construction** — an interval **narrower** than the naive within-station comparator's
  **raises `BootstrapError`**. This is the assertion TE §13.6 actually specifies, and it is
  where a within-station substitution is detectable **with certainty**.
- **On real data, a failure is a mandatory disclosure, not a raise.** The comparison is
  computed and recorded; if the vector interval is **not** wider than the comparator's, the
  run emits a **mandatory disclosure** alongside the interval. The disclosure is not
  optional, not a log line, and not suppressible: an absent disclosure on a failed real-data
  comparison **fails** control (22).

The comparator is, by construction, the method Q-27 rejected — it exists in the code
**solely to be beaten**:

1. **Exact parameters**: same masked data, same block length, and **the same replicate
   count as its primary call** — whatever that call was given, so the comparison is
   like-for-like at 10,000 for the confirmatory run and at the reduced count for TE §15.3's
   fixture timing execution (R-118). The rejected variant's 2,000-replicate parameter is
   never resurrected as a *fixed* comparator count, so there is no small-sample excuse for a
   narrow comparator; the seed is drawn from a deterministically derived child stream of the
   primary seed (R-117).
2. **The comparison**: interval width at the same confidence level; **narrower** fails —
   the fixture path raises, the real-data path discloses.
3. **Quarantine**: the comparator's numbers are **never serialized as a reported
   interval** — the Q-27 variant may not re-enter any results artifact, table or notebook.
   What `BootstrapResult` carries is **guard evidence**: the comparator's width, its
   replicate count and derived seed, the outcome, and — when the comparison fails on real
   data — the disclosure, machine-readable (R-110's pattern), expressly *evidence of the
   check, not a reported interval*.
4. **The cost is measured and recorded, never invented**: the doubled CPU cost is
   **measured at fixture time and frozen into the fixture manifest** per §15.2.
   **Storage** is bounded by **TE §9.3**'s 10.0 GB plan, and **no numeric memory ceiling is
   currently frozen** anywhere in the authorities.

**The disclosure's content** — this is where Rec 23's second option is folded in. When the
real-data comparison fails, the disclosure states: the vector interval's width, the
comparator's width, the comparator's replicate count and derived seed, the block length and
realised block count, and **the measured cross-station paired-error correlations R-121
already computes** (all three pairs). That last item is the point: the equal-station mean's
variance under the vector construction is (1/9)ΣΣCov(d̄_s,d̄_t), and under within-station
resampling the s≠t terms vanish, so **widening follows only where cross-station paired-error
covariance is positive**. A failure paired with near-zero measured correlation is the
expected convergence of two estimators, not evidence of a substitution; a failure paired
with clearly positive measured correlation is the case genuinely worth stopping for. The
disclosure puts the discriminating quantity beside the failure instead of leaving a reader
to infer it.

**Where TC-19's substitution prohibition stays caught.** TC-19 (`binding: hard`; `project.md`
§ Forbidden, "NEVER substitute a within-station or naive bootstrap for the vector time-block
construction") is caught in **three** places, none of which this amendment weakens:

1. **Structurally**, by `VectorBlockDraw`'s shape (R-116, `domain-entities.md` § 3): one
   `block_indices` sequence per replicate applied to all three stations, so a per-station
   index sequence is **unrepresentable**, not merely rejected.
2. **Directly**, by control (11)'s same-indices assertion in `tests/test_bootstrap.py` —
   the Q-27 anti-pattern named and asserted caught.
3. **Behaviourally and with certainty**, by control (19)'s **fixture-time raise** on the
   TA-14 synthetic fixture, where the planted correlation makes widening hold by
   construction and a within-station resampler therefore **must** produce the narrower
   interval.

The real-data comparison was never the mechanism that caught TC-19 — it cannot be, because
its premise is unmeasured until it runs. It is diagnostic, and it is now labelled as such.

> **Applied 2026-08-28 — `GOV-2026-08-28-FD-01` Recommendation 23 (board option 1, with
> option 2's condition folded into the disclosure's content).** Three defects were fixed.
>
> **(1) "narrower or equal" is restored to "narrower".** TE §13.6's final sentence reads,
> verbatim: *"**A synthetic dataset with known cross-station and temporal correlation** must
> confirm that blocks carry all stations together and that intervals widen relative to a
> naive within-station bootstrap."* `requirements.md` FR-P1-05-8 lists it among eight
> mechanical **checks** with acceptance rows WS-17 and TA-14.
> `component-methods.md:869-872` converted it to a runtime raise on "narrower than", and
> this rule **propagated that and strengthened it to "narrower than or equal in width to"**.
> The strengthening was applied **by assertion** — in the same artifact that correctly
> **refused** to apply its own R-118 signature change by assertion, so two contract changes
> were treated inconsistently. The board found this and the owner ruled it: the equality
> limb is removed.
>
> **(2) The raise moves to where its premise holds.** The statistical premise is
> **conditional, not universal** — widening follows only where cross-station paired-error
> covariance is positive, and **no frozen document asserts that sign for ARUC/BSHM/NICO**,
> while R-121 requires the correlation merely *reported*, never conditioning the guard on
> it. The guard's firing point is the **DEC** partition, the one-shot locked evaluation: on
> real data with near-zero cross-station dependence the two intervals converge, and
> "narrower **or equal**" made the raise approximately a coin flip in exactly that regime. A
> false raise at DEC **aborts G-06 after the lock has been opened and the access logged**,
> and Vision §8.3 then labels whatever follows **exploratory** — converting the confirmatory
> result into an exploratory one. §13.6 puts the confirmation on the synthetic fixture, so
> that is where the raise now lives.
>
> **(3) The reading is routed to the gate, not asserted.** Whether check 8 is a runtime
> raise or the fixture-time assertion §13.6 specifies is **the owner's reading to confirm**,
> and it is recorded as such rather than settled here — this rule states the fixture-time
> reading as its **proposal**, on §13.6's words. The change is **weaker than the approved
> `component-methods.md` raise contract**, so it needs the owner's ruling and is listed at
> the gate; the approved contract's own sentence is preserved verbatim in
> `business-logic-model.md` W-1 beside the amendment. **The G-06 abort policy — what happens
> if the comparison fails at the locked evaluation — is owed to the Supervisor at G-05**,
> and no artifact here decides it.

**Negative controls.** (19) A deliberately within-station-resampled primary → **raises** on
the TA-14 synthetic fixture — the fixture-time raise proven to catch the substitution TC-19
names, on the one dataset where widening holds by construction. (20) Comparator numbers
appearing in any serialized results artifact → **fails** the quarantine presence test.
(21) Guard-evidence fields absent from `BootstrapResult` → **fails** the presence test.
(22) A **failed real-data comparison that emits no disclosure**, or a disclosure omitting
the measured cross-station correlations → **fails** — the mandatory disclosure proven
mandatory, so relocating the raise does not silently downgrade the check to a suppressible
warning.

**Acceptance.** TA-14; check 8 of FR-P1-05-8 — the check *"which is what makes the other
checks sufficient"*, read as §13.6 states it: confirmed on the synthetic fixture, disclosed
on real data.

## R-121 — The cross-station paired-error correlation: defined, emitted by the producing path, and the series reading routed to the gate

**Rule (Q9 = C).** The mandated disclosure (TE §13.6: *"report the cross-station
paired-error correlation"*) is computed as **pairwise Pearson correlation of the
per-station paired-error difference series d_s(t)** — the estimand's own series, whose
cross-station correlation is precisely the quantity that justifies the vector construction
(correlated d_s(t) is why within-station resampling narrows intervals) — over **common
masked timestamps of each pair**, **all three pairs reported** (ARUC–BSHM, ARUC–NICO,
BSHM–NICO), carried machine-readably on `BootstrapResult`. `regimes-diagnostics-reporting`
asserts the field's presence and restates nothing (R-110's pattern); §14 forbids a notebook
holding the only copy of bootstrap logic, so the notebook reads the field, never computes
it.

**The series choice (paired differences, not raw errors) is stated at the gate as a
proposal** — the governing sentence names "paired-error correlation" without fixing the
series, so the reading is confirmed, not assumed.

**Negative controls.** (23) The TA-14 synthetic fixture's planted cross-station correlation
not recovered within the declared tolerance (§13.7's fixture-derived-tolerance discipline;
the tolerance lives in the fixture manifest, not here) → **fails**. (24) Correlation fields
absent from `BootstrapResult` → **fails** the presence test.

> **Renumbered 2026-08-28 — `GOV-2026-08-28-FD-01` Recommendation 23.** These two controls
> were (22) and (23); R-120 gained a fourth control at (22) for the mandatory real-data
> disclosure, so they shift by one. The set stays contiguous at **1–24** with no gap or
> duplicate — re-derived programmatically in § Negative-control count. **These correlations
> are now load-bearing twice**: as TE §13.6's mandated disclosure (unchanged), and as the
> content of R-120's real-data disclosure, which is what makes a failed widening comparison
> interpretable. R-121 still does **not** condition the guard on them — the correlation is
> reported and disclosed, never a gate on the raise.

**Acceptance.** TA-14 ("cross-station correlation, verified on synthetic correlated
data").

## R-122 — `tests/test_bootstrap.py`: eight checks, every named control, and the constants convention

**Rule (Q10 = C).** This unit's one test module is scoped as: **the eight FR-P1-05-8
checks plus every named negative control from Questions 1–9** — controls (1)–(24) above,
each asserted to raise or fail — with:

- **fixture parameters declared constants of the test apparatus** (planted correlation,
  gap pattern, per-station row counts, **and TE §15.3's reduced replicate count**), stated
  as such — explicitly **not scientific values**;
- **the scientific values (seed, block length, replicate count, CI level) arriving from
  config even under test**, so the suite itself proves the no-inlined-constant rule
  (TC-03e);
- **WS-17's replicate hash and TA-14's synthetic-case results emitted as machine-readable
  evidence** suitable for the acceptance rows' evidence columns;
- fixture assertion data in `tests/fixtures/<fixture_id>/fixture_manifest.yaml` (§15.2),
  never hardcoded in test bodies.

**What `tests/fixtures/scientific_1month/fixture_manifest.yaml` must carry for the §15.3
bootstrap execution** (owned by `fixtures-and-reproducibility`; named here so the
obligation is not split silently, added 2026-08-28 per Recommendation 24): the **reduced
replicate count** as a declared apparatus constant; the execution's **scored range**, so
R-115 limb 1's divisibility is checkable rather than assumed; and the **realised block
counts at 24 h and, if ever declared, 48 h** — the arithmetic R-115's dated note prints
(744 h raw / 720 h post-exclusion for the March fixture window, D-14). The **measured**
runtime range for this execution is the §15.2 figure §15.3 exists to obtain, and it is
measured there, never invented here (§15.1).

The module's scope is derived from this artifact set's own rules rather than invented at
3.5. The story map names this the one unit with **full acceptance coverage** — that claim
is earned in this module or hollow, and every one of the eight checks lands in a designed
behaviour (§ Eight checks, below).

**G-09 is not signed: the module's design is specified; no module is created.**

**Negative controls.** None new — this rule hosts the set; every control is counted once at
its owning rule.

**Acceptance.** WS-17 (primary), TA-14 (primary) — both earned here.

---

## Negative-control count, derived not carried

Controls are numbered (1)–(24) in the rules above, each counted once at its owning rule.
Derivation by rule: R-113 4, R-114 2, R-115 3, R-116 3, R-117 3, R-118 2, R-119 1,
R-120 **4**, R-121 2, R-122 0 → 4+2+3+3+3+2+1+4+2+0 = **24 distinct negative controls**,
contiguous 1–24 with no gap and no duplicate. Two controls that must **not** fire are listed
separately (R-113's G-06 pass path, R-116's ragged-but-supported December fixture) and are
not in this count.

> **Re-derived 2026-08-28, printed before asserted.** The count was **23** before this
> remediation and is **24** after it: R-120 gained control (22), the mandatory-disclosure
> falsifier Recommendation 23's fix requires, and R-121's two controls shifted from
> (22)–(23) to (23)–(24). Derivation was run programmatically over this file's
> `**Negative controls.**` blocks — per-rule counts `4+2+3+3+3+2+1+4+2+0 = 24`, distinct
> numbers 1…24, gaps none, duplicates none — rather than carried from the prior revision or
> from any finding's prose. **The `## Review` box in `business-logic-model.md` records 23**;
> that box is the dated 2026-08-27 reviewer pass, preserved byte-for-byte, and its figure is
> correct **for the artifact it reviewed**. It is not a live count and must not be swept to
> 24.

## Eight checks, mapped — full coverage earned, not nominal

FR-P1-05-8's criterion is **eight mechanical checks, not two**; each lands in a designed
behaviour:

| Check | Rule | Where it bites |
|---|---|---|
| (1) pairing per station-hour before differencing | R-114 | R-108's step-1 path, (`station`, `interval_start_utc`) key |
| (2) vector block, all three stations, never independent resampling | R-116 | same-indices enforcement; controls (11) |
| (3) block length 24 h | R-115, R-118 | fixed partition (**proposed reading, gate item 5**); config-declared value; scheme and realised block count recorded on `BootstrapResult` |
| (4) 10,000 replicates | R-118 | config-declared, passed explicitly; control (17) scoped to confirmatory runs so TE §15.3's reduced-replicate fixture execution is representable |
| (5) equal-station weighting matching the estimand | R-114 | steps 2–3 reapplied; control (6) |
| (6) exact reproduction from seed 20221201 on synthetic correlated data | R-117 | pinned generator; controls (13)–(14); WS-17 |
| (7) missing paired prediction handled by the declared rule | R-116 | the ragged-block rule; controls (10), (12) |
| (8) interval wider than a naive within-station bootstrap | R-120 | the **fixture-time raise** plus the **mandatory real-data disclosure**; controls (19)–(22) |

The 48-hour sensitivity (also required by the criterion's closing sentence) is R-118's;
the correlation disclosure is R-121's; TE §15.3's reduced-replicate fixture execution is
R-118's and R-122's, with its manifest declaration owned by
`fixtures-and-reproducibility`.

## Amendments owed

**Derived against the sibling's re-derived basis, and printed before asserted:
5 + 0 + 1 + 2 = 8 across 5 units.** *(Was 7 across 5 units; this unit's own owed count rose
from 1 to 2 on 2026-08-28 with Recommendation 23's raise-contract amendment. The basis rows
were re-verified on disk the same day and are unchanged.)*

| Source | Owed | Basis |
|---|---|---|
| `external-products` **R-55** | **5**, across **3** units | Derived there (`acquisition` 3, `inventory-and-registry` 1, `external-products` 1), boundary contracts only. Not restated here; a restated count drifts. **Re-verified 2026-08-28** by reading its § Amendments owed total row. |
| `features-and-splits` | **0** | Re-derived 2026-08-26 in its § Amendments owed: its three dissolved into ADR-11. |
| `evaluation-and-comparison` | **1** | The BLK-08 resolution package (its R-103), one consolidated amendment — **re-verified 2026-08-28** by reading its `business-rules.md` § Amendments owed, which prints exactly the 5 + 0 + 1 = 6-across-4 derivation this row extends. **Open dependency:** that unit is narrowing its resolver to `load_inverse(transform_id) -> Inverse` in parallel under Recommendation 7; if that changes its owed count, this row follows **its** re-derived figure, not a restatement made here. |
| **This unit** | **2** | **(i) The R-118 signature amendment**: remove `block_hours=24` and `replicates=10_000` from the approved `vector_block_bootstrap` signature, making both required keywords like `seed` — the same rule (TC-03e) that reshaped `seed`, finished. **(ii) The R-120 raise-contract amendment** *(new 2026-08-28, Recommendation 23)*: the approved contract at `component-methods.md:869-872` raises `BootstrapError` *"when the resulting interval is narrower than a naive within-station bootstrap on the same data"* as a **runtime** raise; the amendment relocates the **raise** to the TA-14 synthetic fixture §13.6 specifies and makes the real-data comparison a **mandatory disclosure**, and additionally states the comparator's replicate count as **its primary call's** rather than a fixed 10,000 (Recommendation 24). This is a **weakening** of an approved contract, so it is treated exactly as (i) was — **proposed at the gate, not applied**, never asserted into the contract. |
| | **8 across 5 units** | 5 + 0 + 1 + 2 |

**Why Q7, Q9 and Q3 add no rows.** The interval-method confirmation (R-119), the
correlation-series reading (R-121) and — added 2026-08-28 per Recommendation 26 — the
**block-scheme reading** (R-115) are **scientific confirmations routed to the gate**
(TE §18.3), configuration content under the four-config regime, not boundary contracts:
each is a value the owner freezes into `experiment.yaml`, not a signature or a raise
contract in `component-methods.md`. `experiment.yaml`'s bootstrap fields (block hours,
replicates, CI level, the predeclared 48-hour sensitivity run, the method once confirmed,
the scheme once confirmed) are gate-confirmed config, the same class as the sibling's R-106
membership. **TE §15.3's reduced replicate count adds no row either**, and for a different
reason: it is an **apparatus constant** in
`tests/fixtures/scientific_1month/fixture_manifest.yaml` (R-118, R-122), not config and not
a contract — `fixtures-and-reproducibility` declares it there.

## Requirement coverage

| Requirement | Rules | Acceptance |
|---|---|---|
| FR-P1-05-8 | R-113…R-122 (the eight-check map above) | WS-17 (primary), TA-14 (primary) |

**1 requirement, 0 untested — derived from the story map's rows, the two upstream
artifacts agreeing.** No supporting rows; the determinism rows TA-13/TA-26 belong to
`foundation` and `models-and-baselines`, with this unit's carved-out seed named there as
context, not claimed here.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence: the sibling closes at **R-112** (re-derived 2026-08-27 by grepping its headings), so this unit opens at **R-113** and closes at **R-122** — **10 rules, derived by numbering this file's headings**. The R-83…R-89 gap is inherited as observed, not explained.
- **[assumption]** **`BootstrapError` is one of `foundation` R-01's enumerated project exceptions** (R-01 names it among those raised by other units), **declared here** — `src/evaluation/bootstrap.py`, this unit's raise site — importing `IntegrityError` from `src/data/config.py`; `FairnessError` (declared by `evaluation-and-comparison` in `src/evaluation`), `LeakageError` (`features-and-splits`), `LockedTestError` (`governance-guards`), **`PartitionError`** (`models-and-baselines`) and `InverseTransformError` (the sibling's, its placement being settled by `foundation`) are **imported for R-113's preconditions, not redeclared**. Every raise names the file or resource and the violated expectation. **Updated 2026-08-28 per Recommendation 8:** the enumeration is cited as **fifteen** — `PartitionError` promoted into it by owner ruling — and no longer as "the fourteen"; this unit **imports** the fifteenth and declares none of it. `InverseTransformError`'s status is `foundation`'s to settle (it was labelled here as the sibling's unit-local under R-01's any-future clause); **this unit cites whatever `foundation` settles and does not decide it**, and the dependency is recorded rather than resolved because `foundation`'s file on disk still asserts "all fourteen" and lists neither name. ⚠ **SWEPT 2026-08-28 on the resume pass — this disk-state claim is SUPERSEDED.** `foundation` R-01 **has been amended** and now reads **fifteen**, with `PartitionError` promoted into the enumeration, the count restated as **derived and printed** rather than carried in prose, and `InverseTransformError` **explicitly disposed** — not a sixteenth, riding R-01's *"any future integrity-related exception"* clause, on the stated ground that the two units raising it agree on its condition and meaning, so nothing needs reconciling. Verified at `foundation/functional-design/business-rules.md` R-01 (the amendment row, the superseded-wording box, and the `InverseTransformError` box). **The dependency this sentence recorded is discharged; any open item stated alongside it is NOT** — see the sentence it accompanies. See R-113 precondition 2 for the discriminated-type contract this affects.
- **[assumption]** `vector_block_bootstrap` lives in `src/evaluation/` under the TE §12 allowlist as a **path grant owned by three units** (sibling R-112 records it as belonging to this unit); this unit designs `bootstrap.py` only and asserts no narrowing of TE §12.
- **[assumption]** The seed 20221201 reaches this unit as `ConfigSnapshot.seeds`' bootstrap entry through `07`'s call site; the `seeds.yaml` key name is `foundation`'s surface.
- **Verification obligations owned here:** controls (1)–(24), enumerated per rule and counted in § Negative-control count; the two must-not-fire controls; R-122's evidence emission.
- **Governance dependencies owned outside this unit:** BLK-03's contract limbs (`models-and-baselines`); BLK-04's limbs and BLK-09's `train_start` resolution (`features-and-splits`); **BLK-08 ↓ — narrowed 2026-08-28 to `ABL-DIFF` alone on D-27's strength**: the primary interval's TECU status is a **recorded fact** (D-27, 2026-08-24), so the residual dependency is the `ABL-DIFF` inverse mechanism and its error-propagation record, jointly owned by `features-and-splits` and `evaluation-and-comparison` (the latter narrowing its resolver to `load_inverse(transform_id) -> Inverse` under Recommendation 7); the **R-118 signature amendment and the R-120 raise-contract amendment** (both ruled at the gate); the R-119 interval-method, the R-121 series and — **new 2026-08-28 per Recommendation 26** — the **R-115 block-scheme** confirmations (student/supervisor); `experiment.yaml`'s bootstrap fields (gate-confirmed, frozen under the four-config regime); **TE §15.3's reduced replicate count in `tests/fixtures/scientific_1month/fixture_manifest.yaml`** (`fixtures-and-reproducibility`); **`foundation` R-01's amended fifteen-exception enumeration and `evaluation-and-comparison`'s corrected R-105** (Recommendation 8); **the G-06 abort policy for a failed widening comparison at the locked evaluation — owed to the Supervisor at G-05** (Recommendation 23); **a change record against `services.md` and `unit-of-work.md`** for the TE §9.3 storage-versus-memory conflation (Recommendation 40; those two artifacts are approved upstream and are **not** edited from here); acceptance-row evidence formats for WS-17/TA-14 (stage 3.2 via Vision §15.2 if any row text needs amendment); G-05's freeze of the evaluation code this stage designs (Supervisor).
- **Open — all four inherited blockers are EXIT conditions on this stage.** BLK-03 ↓, BLK-04 ↓, BLK-08 ↓, BLK-09 ↓ remain open; nothing in this file closes any of them; this unit may not complete or exit 3.1 while any stands, and no implementation may proceed while they stand.
- **Open — the CPU and memory figures are measured and recorded, not asserted** (§15.1): the doubled comparator cost and the 10,000-replicate primary run are **measured and recorded; storage is bounded by TE §9.3's 10.0 GB plan, and no numeric memory ceiling is currently frozen**; every runtime and tolerance is a placeholder until fixture time.

  > **Corrected 2026-08-28 — `GOV-2026-08-28-FD-01` Recommendation 40.** **TE §9.3** (line 532) is titled **"Storage budget"** and self-describes as *"A capacity plan, not a scientific freeze gate"*, totalling 10.0 GB across **eight disk categories**. **TE §9.2** records *"peak memory where available"* and names **no numeric value**, and a sweep of `PreFlight/` finds **no memory ceiling anywhere in the authorities**. R-120 limb 4 and `business-logic-model.md` therefore no longer measure a CPU/memory cost "against TE §9.3's 10.0 GB envelope"; they say **"measured and recorded; storage is bounded by TE §9.3's 10.0 GB plan, and no numeric memory ceiling is currently frozen"**. **The conflation is upstream, not introduced here:** `services.md:258-259` and `:264` state *"peak memory, not cumulative runtime, is the binding quantity against TE §9.3's 10.0 GB hard planning envelope"* and `unit-of-work.md:453` repeats it — both **approved upstream artifacts** this stage cited faithfully, which this unit's own `## Review` (finding 2) identified and traced correctly before the board did. **A change record against `services.md` and `unit-of-work.md` is owed** (Recommendation 40 option 1, owner: those artifacts' owners, due before G-07); **neither file is edited from here.** **Disambiguation hazard, recorded:** **two different §9.3s exist** — **TE §9.3** = Storage budget; **Vision §9.3** = Geomagnetic Regimes and Storm Events (Vision line 896) — and TE line 188 itself cross-cites "per Vision §9.3" while `unit-of-work.md:462` says "the §9.3 storm-event rule" unqualified, so this artifact set always writes **"TE §9.3"** or **"Vision §9.3"** explicitly. **A real memory envelope could be frozen from measurement after the fixtures run**, which §15.1 permits — inventing one now, which is what a 10.0 GB memory ceiling would be, it forbids.
- **G-09 is not signed.** No rule here authorises creating `src/evaluation/bootstrap.py` or `tests/test_bootstrap.py`; TE §18.3's stop-and-report rule binds every affected component while any P0 decision is unresolved.
- **None** of the above decides a scientific value: 24 h, 10,000, 20221201, 95% and 2–31 December (now recorded as **D-28**) are already frozen and merely encoded; the interval method (R-119), the correlation series (R-121), the **block scheme** (R-115) and the `experiment.yaml` fields (R-118) are expressly routed to the gate as proposals, and TE §15.3's reduced replicate count is an apparatus constant rather than a scientific value. **Nor does the 2026-08-28 remediation decide one**: D-27 and D-28 are cited as already-recorded decisions, Recommendation 8's taxonomy is the owner's ruling being cited, Recommendation 23's raise relocation is **proposed at the gate** as an amendment owed, Recommendation 26 **adds a gate item rather than settling it**, and Recommendation 40 removes an unfounded ceiling instead of inventing a founded one.
