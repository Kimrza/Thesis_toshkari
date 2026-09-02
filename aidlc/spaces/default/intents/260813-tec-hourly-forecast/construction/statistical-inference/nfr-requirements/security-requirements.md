# Security Requirements — `statistical-inference`

**Unit** `statistical-inference` (Bolt 10) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NOTHING HERE IS CLAIMED SATISFIED
>
> **The interval method is UNCONFIRMED.** The percentile method is **proposed and routed to
> the gate**; if implementation is reached with it unconfirmed the posture is **TE §18.3's —
> stop and report rather than choose a default**. The **block-resampling scheme** and the
> **correlation series** are likewise **proposed, not decided**.
>
> **BLK-03, BLK-04, BLK-08 and BLK-09 are inherited exit conditions on this stage, and none is
> closed here.** **WS-17 (primary), TA-13 and TA-26 are undischarged** — TA-13 and TA-26 belong
> to `foundation` and `models-and-baselines`.
>
> **G-09 is signed (D-31) with its own preconditions UNMET**; **stage 3.1 remains FAIL**;
> `configs/` does not exist; **no Python interpreter exists in this environment**, so **no
> bootstrap has ever been run** and every runtime figure in this design is a placeholder.
>
> No scientific value is decided here, and TE §18.2's absolute rule stands.

## Sources

- `../functional-design/business-rules.md` — **R-113** (the bootstrap is a **metric entry point in full**), **R-114** (**one copy of the estimand arithmetic**: precompute once, resample the precomputed), **R-115** (the block grid: fixed non-overlapping partition, and what a boundary violation raises), **R-116** (the **vector property** and the declared rule for missing pairs), **R-117** (**seed sourcing, generator identity, and what "reproduces exactly" pins**), **R-118** (the frozen numbers live in config; the signature amendment is **proposed, not applied**; the sensitivity is a predeclared named run), **R-119** (**the interval method is proposed at the gate**, and the design is **method-parametric**), **R-120** (the **widening guard**: the raise at fixture time, the real-data comparison as a mandatory disclosure, and the comparator **exact and quarantined**), **R-121** (the cross-station paired-error correlation, **emitted by the producing path**), **R-122** (`tests/test_bootstrap.py`: **eight checks**, every named control, and the constants convention).
- `../functional-design/business-logic-model.md` — **W-1** … **W-8**, in particular **W-4** (seed and stream discipline), **W-5** (interval construction, method-parametric, and the 48-hour sensitivity), **W-6** (the widening guard), **W-7** (correlation emission and `BootstrapResult` assembly), and § Requirement coverage — **1 requirement, 0 untested**.
- `../../evaluation-and-comparison/nfr-requirements/security-requirements.md` — § SEC-C-02, whose estimand orientation this unit resamples but does not recompute, and § SEC-C-03's hash-receipt precondition.
- `../../../inception/requirements-analysis/requirements.md` — **FR-P1-05-8** (this unit's requirement), **FR-P1-04-5** (context — `features-and-splits`' fold and embargo requirement, which the block grid is drawn over), **NFR-DET-01**, **NFR-AUD-01**, **NFR-REP-01** (§13.7's **exact-equality classes** — hashes, schemas, partition membership, IDs and deterministic CPU transformations compare **for equality, not tolerance** — which is the provision SEC-S-01's replicate-hash controls actually rest on).
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§13.5** (seeds), **§13.6** (the vector time-block bootstrap; *"report 95% confidence intervals"* and **no method named**), **§13.7** (exact equality), **§15.1** (measured, never invented), **§15.3** (the reduced-replicate fixture bootstrap), **§9.2–9.3**, **§18.2–18.3**, **§16** (WS-17), **§19** (TA-13, TA-26).
- `evidence/DECISIONS.md` — the bootstrap seed **20221201**, separately frozen (TE §13.6, §13.5; **not** part of D-122's item set).
- `governance/reviews/GOV-2026-08-28-FD-01.md` — **Recommendation 23** (the G-06 abort policy for a failed widening comparison, **owed to the Supervisor at G-05**), **Recommendation 24** (the §15.3 reduced-replicate count), **Recommendation 8** (the exception taxonomy).
- `nfr-requirements-questions.md` — Q1 = B, Q2 = A, and the receipted Consolidated Summary Confirmation.

---

## Scope note — and why Performance is a real category here

`produces_kinds` excludes `performance-requirements`, `scalability-requirements` and
`reliability-requirements` for a `library` unit. Assessed anyway — and unlike the other units,
**one of them genuinely bites**:

| Category | Assessment for `statistical-inference` | Where it lives |
|---|---|---|
| **Performance** | **Real, and unmeasured.** This unit runs the project's heaviest computation — **10,000 replicates** over 24-hour blocks carrying **all three stations together**, plus the 48-hour sensitivity and the widening comparator as child streams. **No numeric memory ceiling exists in the authorities**, and **neither fixture has run**, so there is no figure. | § SEC-S-04 |
| **Scalability** | Bounded and fixed by protocol: 10,000 replicates, 3 stations, 30 scored days. The replicate count is a **frozen scientific value**, not a tuning knob — it cannot be reduced to fit a budget. | § SEC-S-04 |
| **Reliability** | **Fail-closed on identity and on inputs**: a call without `seed` is a **`TypeError` by signature**; a block-grid boundary violation **raises**; an unrecognised or unconfirmed interval method **raises `BootstrapError`**. | § SEC-S-01, § SEC-S-02 |
| **Security** | This artifact — **the integrity of the reported uncertainty**. An interval that is too narrow overstates confidence in the thesis's central claim. | — |
| **Observability** | `BootstrapResult` records the **seed key consumed, the generator identity, and the replicate hash** — WS-17's evidence **emitted by the producing path**, an assertable artifact fact rather than a log line. | § SEC-S-01 |

---

## SEC-S-01 — Exact reproduction is pinned by more than a seed

**Requirement (R-117, W-4, Q5 = C, NFR-DET-01).** The seed is **required and passed in** —
`ConfigSnapshot.seeds`' bootstrap entry from `configs/seeds.yaml`, the separately frozen
**20221201** (TE §13.6, §13.5; **not** part of D-122's item set), **never defaulted and never
inlined** (TC-03e).

**Four pins, because a seed alone does not determine a stream.**

1. **`default_rng(seed)` — PCG64** is the generator. A different generator produces different
   draws from the same seed, so "reproduces exactly" is meaningless without it.
2. **Block-index draws are the only consumer of the primary stream.** The 48-hour sensitivity
   (R-118) and the widening comparator (R-120) draw from **deterministically derived child
   streams** (seed-sequence spawn), so **no consumer can perturb another's draws**.
3. **`BootstrapResult` records the seed key consumed, the generator identity, and the replicate
   hash** — WS-17's evidence **emitted by the producing path** (R-110's pattern), an
   **assertable artifact fact rather than a log line**.
4. **A call without `seed` is a `TypeError` by signature** — the never-defaulted rule is
   **unrepresentable rather than checked**.

**These pins are engineering contracts, not scientific constants.** The scientific value —
**20221201** — stays in `seeds.yaml`; the generator name is no more a scientific constant than
the language pin. What they buy: *"reproduces exactly"* stops meaning *"reproduces on the
machine that wrote the hash"*.

**Negative controls (R-117's 13–15).** A **different** seed → a **different** replicate hash,
asserted. A **same-seed rerun** → the **identical** replicate hash, asserted (§13.7 exact
equality). A call **without** `seed` → **`TypeError`**.

**Requirement (NFR-AUD-01).** The replicate hash and the recorded seed key are **append-safe
audit facts**; a re-run does not overwrite a prior `BootstrapResult`, and a failed run stays
visible with its status and reason.

## SEC-S-02 — The estimand arithmetic exists once, and the resampling never redefines it

**Requirement (R-114, W-2).** **One copy of the estimand arithmetic.** The per-pair squared-error
differences are **precomputed once**, and the bootstrap **resamples the precomputed values** —
it does **not** recompute the estimand inside the replicate loop.

**Why this is a security requirement and not an optimisation.** Two copies of the estimand
arithmetic can **disagree**, and the one inside a 10,000-iteration loop is the one nobody reads.
A resampling routine that recomputed `benchmark − model` could silently invert the sign, apply
row-weighting instead of **equal-station weighting**, or drop a station — and the interval would
look entirely normal. **`evaluation-and-comparison` § SEC-C-02 owns the estimand's orientation
and its reversed-sign control; this unit resamples that output and adds no second definition.**

**Requirement (R-113, W-1).** The bootstrap is **a metric entry point in full** — it inherits
**every** precondition a metric entry point carries, including the **inverse-before-metric**
refusal, the **stamp** refusal, and **`evaluation-and-comparison` § SEC-C-03's hash-receipt
precondition**. It is not a downstream helper exempt from the boundary.

**Requirement (R-115, W-3).** The block grid is a **fixed non-overlapping partition** into
24-hour blocks; a **boundary violation raises**. The blocks are drawn over
`features-and-splits`' **exact fixed calendar folds with their 24-hour embargo** (FR-P1-04-5),
and **the first 24 h are excluded and counted**.

**Requirement (R-116).** The **vector property**: a drawn block carries **all three stations
together**, preserving the cross-station error correlation. A **within-station or naive
bootstrap is never substituted** — `project.md` records that it produces **systematically
narrower intervals**, and the within-station 2,000-replicate variant was **rejected at Q-27**.
The declared rule for **missing pairs** is stated rather than left to the implementation.

## SEC-S-03 — The widening guard, and what happens when it does not widen

**Requirement (R-120, W-6).** The widening guard uses the **rejected** within-station method as
a **yardstick**: the vector bootstrap should produce **wider** intervals, because that is the
stated reason the within-station variant is forbidden. **The raise lands at fixture time.** On
**real data** the comparison is a **mandatory disclosure**. The comparator is **exact and
quarantined** — deliberately **not load-bearing**.

> ### Requirement (Q1 = B) — a non-widening outcome on real data is ADJUDICATED, not absorbed
>
> If, on the real December data, the vector bootstrap is **not** wider than the rejected
> method, the result is **disclosed as designed** and the run proceeds — **and the outcome
> becomes a named G-06 item the supervisor must rule on before the interval is reported as
> confirmatory.**
>
> **Why.** A non-widening outcome has exactly two explanations: **the implementation is wrong**,
> or **the assumption behind rejecting within-station does not hold for this dataset**. Both
> bear directly on the reported interval, and disclosure alone leaves a possibly-too-narrow
> interval reaching the thesis with a caveat — **this project has already recorded how much
> less far a caveat travels than the number it qualifies**.
>
> **Why not a block.** The comparator is **exact and quarantined precisely so it is not
> load-bearing**. Making a **rejected** method's output a blocking condition would invert
> that — the yardstick would become the authority.
>
> **This is not a new route.** This unit's own `functional-design` already records that **the
> G-06 abort policy for a failed widening comparison is owed to the Supervisor at G-05**
> (`GOV-2026-08-28-FD-01` **Recommendation 23**) and is **decided by no artifact**. This
> requirement states what that ruling must cover; **it does not pre-empt it.**

**Requirement (R-119, Q7 = B).** Interval construction is **method-parametric**, reading its
method from `experiment.yaml`. **The percentile method is PROPOSED and routed to the gate** —
TE §13.6 says *"report 95% confidence intervals"* and **names no method**, and percentile, basic
and BCa **can differ materially** on 10,000 replicates of a skewed statistic, so the choice is a
**scientific protocol value** §18.2 bars an implementer from filling. **Negative control (18):**
an unrecognised, absent or **unconfirmed** interval-method value → **refused**
(`BootstrapError`, naming the config key).

**Requirement (R-118).** The frozen numbers live **in config**; the signature amendment is
**proposed, not applied**; the 48-hour sensitivity is a **predeclared named run**.

**Requirement (R-121, W-7).** The **cross-station paired-error correlation** is **defined and
emitted by the producing path** — not left for a reader to compute. **The series reading is
routed to the gate.**

## SEC-S-04 — Resource posture: what the authorities actually state, and what they do not

**Requirement (Q2 = A, TE §9.2, TC-01).** The bootstrap **completes on CPU** within the two
governed platforms. **CPU is a complete execution path, not an emergency mode**, and **GPU may
be an optional accelerator only, never a dependency of any result**.

> ### ⛔ NO NUMERIC MEMORY CEILING EXISTS IN THE AUTHORITIES
>
> **TE §9.3 is a storage budget.** `services.md`'s *"peak memory, not cumulative runtime, is
> the binding quantity against TE §9.3's 10.0 GB hard planning envelope"* is a **conflation**,
> quoted here as **upstream text** and **not adopted**. **A change record against
> `services.md` is owed and is not this stage's to write.**
>
> **No memory ceiling is asserted here, and none is borrowed.** Adopting 10.0 GB would make
> this stage the place a **storage** budget quietly became a **memory** ceiling — precisely the
> defect the change record exists to correct.
>
> **The peak-memory figure is to be MEASURED on the fixtures and FROZEN** (TE §15.1: exact
> counts, tolerances and runtimes are **measured from the fixtures and frozen, never
> invented**). **Neither fixture has run**, so **there is no figure**, and an implementer has
> **no memory budget to design against today**. That is a real gap, stated rather than papered
> over with a number the authorities do not supply.

**Requirement.** The **replicate count is a frozen scientific value**, not a tuning knob.
**10,000 replicates cannot be reduced to fit a resource budget** — a smaller count is a
different protocol, and TE §18.2 bars changing a scientific value for convenience. If the
measured peak memory proves intolerable, the response is a **decision routed to the owner**,
not a quiet reduction.

**Carried — TE §15.3's reduced-replicate fixture bootstrap** (Recommendation 24) is a
**separate** apparatus constant in `tests/fixtures/scientific_1month/fixture_manifest.yaml`,
**not** a licence to reduce the confirmatory count. **Its classification is open** — apparatus
constant, or a predeclared `experiment.yaml` named run if the owner rules a replicate count is
protocol wherever it appears.

**Requirement (in-Kaggle obligation).** Any Bolt performing a **governed run** inside a Kaggle
session must first evidence that the required critical tests and applicable fixtures passed
**inside that same session**. **The G-06 interval is computed once**, so this binds at the run
that matters most.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| **FR-P1-05-8** | SEC-S-01, SEC-S-02, SEC-S-03 | **WS-17 (primary)**, TA-13, TA-26 | `Pending` — **the story map names this the one unit with full acceptance coverage; that coverage is earned in `test_bootstrap.py`'s eight checks or it is hollow, and the module does not exist** |
| **FR-P1-04-5** *(context — `features-and-splits`' requirement)* | SEC-S-02 | — | `Pending` — the folds and embargo the block grid is drawn over |
| **NFR-REP-01** | SEC-S-01, SEC-S-02 | **WS-20, TA-17** — rows owned by `fixtures-and-reproducibility` | `Pending` — **the exact-equality classes SEC-S-01's replicate-hash controls rest on** |
| **NFR-DET-01** | SEC-S-01 | WS-17 (supporting), TA-13 | `Pending` |
| **NFR-AUD-01** | SEC-S-01 | TA-10, TA-21 | `Pending` — rows owned by `foundation` |

**Derived and printed**: 4 requirement sections (SEC-S-01…SEC-S-04); **5** coverage rows *(corrected 2026-09-01 on adversarial finding 1, Major; superseded: **4**. **NFR-REP-01** is the provision SEC-S-01's exact-equality controls and TS-S-05's implementation-independence claim both rest on — both artifacts cited **TE §13.7 directly** and never the NFR ID that provision backs. The up-front derivation that produced this artifact's set grepped **this unit's own design files** for IDs; NFR-REP-01 is not named there, so the check passed while the substance was present. **Grepping a unit's design is not set-differencing against `requirements.md`** — the FR families were clean, the NFR family was not.)* — the
**1** requirement the `functional-design` map carries (**FR-P1-05-8**, *0 untested*), plus
**FR-P1-04-5**, **NFR-DET-01** and **NFR-AUD-01**, the three further IDs this unit's design
names and this artifact states obligations against. **The set was derived from `requirements.md`
before this artifact was written**, not reconstructed afterwards. **0** rows claimed satisfied.

## Assumptions & Open Questions

- **[Q1]** The G-06 adjudication requirement **states what Recommendation 23's owed ruling must cover; it does not pre-empt it**. The abort policy remains **the Supervisor's at G-05**.
- **[Q2]** **No numeric memory ceiling exists in the authorities.** None is asserted or borrowed here, and **the peak-memory figure is owed as a fixture measurement**. **Neither fixture has run.**
- **[assumption]** The replicate count and the measured memory are independent enough that a memory problem can be solved without touching the count. **If they are not**, the trade is a **scientific decision routed to the owner**, not an implementation choice — and this artifact does not pre-authorise a reduction.
- **Open, and not this stage's — the interval method is UNCONFIRMED.** Percentile is proposed. **Stage 3.5 must stop and report** if it is reached unconfirmed.
- **Open — the block-resampling scheme (W-3) and the correlation series (W-7) are proposed, not decided.**
- **Open — the §15.3 reduced-replicate count's classification** (Recommendation 24): apparatus constant, or a predeclared named run.
- **Open — the exception taxonomy** (Recommendation 8): `PartitionError` is `foundation` R-01's **fifteenth** by owner ruling, **imported** here and declared by `models-and-baselines`.
- **Carried — BLK-03, BLK-04, BLK-08 and BLK-09 are inherited exit conditions on this stage.** Nothing here closes any of them, and **this unit may not complete or exit 3.1 while they stand.**
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z (system clock rollover mid-review; content facts below were derived before the rollover)
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `security-requirements.md` § Sources / § SEC-S-01; `tech-stack-decisions.md` § Sources / § TS-S-01 / § TS-S-05 | **`NFR-REP-01` is cited by neither artifact, despite its substance being the direct subject of both.** `requirements.md` line 485 defines `NFR-REP-01` as "Clean CPU reproducibility — the §13.2 ordered sequence completes on CPU from a clean environment, **and §13.7's exact-equality classes hold exactly**: hashes, schemas, partition membership, IDs and deterministic CPU transformations compare for equality, not tolerance, and a mismatch must not silently update the expected value." `security-requirements.md` § SEC-S-01 states the identical substance under R-117/NFR-DET-01 — "A **different** seed → a **different** replicate hash... A **same-seed rerun** → the **identical** replicate hash, asserted (§13.7 exact equality)" — and cites `TE §13.7` directly in its Sources list (line 28), but never cites the NFR ID that §13.7 backs. `tech-stack-decisions.md` § TS-S-05 makes the same point again ("the replicate hash is **implementation-independent**... which is precisely what a two-platform project needs") with no `NFR-REP-01` citation either. This is the same defect class the dispatch brief names as having recurred on four consecutive prior units: substance present, requirement ID silently uncited. Verified programmatically: `grep -c NFR-REP-01` against both artifacts returns 0; `requirements.md` line 485 is the sole defining row and it names WS-20/TA-17 as its acceptance rows, neither of which either artifact's coverage table lists as a section-level citation even though WS-17/TA-13/TA-26 are extensively discussed. | Add `NFR-REP-01` to both artifacts' Sources lists and to SEC-S-01/TS-S-01's requirement citation, or state explicitly why the reproducibility requirement two artifacts build their central negative controls on is out of scope for this unit's coverage table. |
| 2 | Minor | `security-requirements.md` § Requirement coverage; `tech-stack-decisions.md` § Requirement coverage | The completeness claim ("derived from `requirements.md` before this artifact was written") is corroborated by `functional-design/business-logic-model.md` line 678 and `business-rules.md` line 748, which independently confirm this unit's `functional-design` map carries exactly **1** requirement (FR-P1-05-8, 0 untested) against the 18 FR-P1-04-* and 22 FR-P1-05-* IDs enumerated in `requirements.md` overall — so the narrow four/two-row coverage tables are not under-scoped with respect to the FR families. This is stated for the record since finding #1 shows the completeness claim is not fully clean; it is confined to the FR families and does not extend to the NFR family. | None — record only. |

### Validation Tool Results

No validation tools were listed for this stage in the dispatch brief; checks were performed by direct `grep`/set-difference against `requirements.md`, `business-rules.md`, and `business-logic-model.md`, with derivations printed above.

### Coverage limits (8-call budget)

This pass read both PRIMARY/SECONDARY artifacts in full, set-differenced the FR-P1-04-*/FR-P1-05-*/NFR-* ID families against `requirements.md`, and cross-checked the functional-design coverage claims. It did **not** independently verify: the D-122/D-31/G-09 claims, the literal non-existence of `configs/` and the Python interpreter, or the `evaluation-and-comparison` sibling file's SEC-C-02/SEC-C-03/TS-C-02 content (spot-check carve-out not exercised — those cross-unit claims are taken as stated per the read-scope bound). The RNG-pin classification (engineering contract vs. scientific constant) was judged on the reasoning given in the artifacts and found internally consistent and adequately caveated (NumPy-version dependency is explicitly stated), not independently re-derived from TE §18.2 beyond that.

### Summary

The two artifacts are unusually disciplined about **not** claiming anything satisfied, and the FR-family completeness claim holds up against an independent set-difference for the first time in five units. But the completeness check is not clean overall: `NFR-REP-01`, whose defining text (§13.7 exact-equality classes, hash/seed reproducibility) is exactly what SEC-S-01 and TS-S-01/TS-S-05 build their reproducibility argument on, is never cited by ID in either artifact — the same silent-substance-uncited-ID pattern flagged on the four preceding units. One Major finding blocks READY under the ≤2-Major rule.

NOT-READY

## Review — iteration 2 (terminal)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:31:16Z
**Iteration:** 2 (terminal — advisory from this point; no further fix-and-re-review cycle)

### Verification of the iteration-1 Major repair

- **`NFR-REP-01` is now cited by ID in both artifacts.** `security-requirements.md` § Sources cites it against §13.7's exact-equality classes and states explicitly it is "the provision SEC-S-01's replicate-hash controls actually rest on"; the Requirement-coverage table carries it as its own row (`SEC-S-01, SEC-S-02` · `WS-20, TA-17`). `tech-stack-decisions.md` carries the same row (`TS-S-01, TS-S-05` · `WS-20, TA-17`, "the RNG pin is what makes §13.7 exact equality reachable"). Grep confirms `NFR-REP-01` present in both files (0 hits before, present now — programmatically checked this pass).
- **Dependent figures are internally consistent, not merely relabelled.** `security-requirements.md`'s coverage table has exactly **5** rows, counted directly off the table: FR-P1-05-8, FR-P1-04-5, NFR-REP-01, NFR-DET-01, NFR-AUD-01 — matches the printed "**5** coverage rows" and the "4 → 5" correction note. `tech-stack-decisions.md`'s table has exactly **3** rows, counted directly: FR-P1-05-8, NFR-DET-01, NFR-REP-01 — matches "**3** coverage rows" and the "2 → 3" correction. The dependent phrase "**two fewer** than `security-requirements.md`'s **five**" checks out arithmetically: 5 − 3 = 2, and both operand counts are independently verified against their own tables (not carried from prose), satisfying `project.md`'s count-derivation rule.
- **Root cause recorded, not just the symptom fixed**: the correction note in `security-requirements.md`'s coverage section states the up-front derivation grepped this unit's own design files rather than set-differencing `requirements.md`, and that the superseded figures are left standing per the project's append-only correction convention. Consistent with `functional-design:fd-2026-08-30-sweep-numerals-and-surfaces`/`sweep-derive-sites` and `never-edit-signed-record`.

### NFR-family completeness re-check (all 11 IDs, set-differenced against `requirements.md`)

`requirements.md` defines exactly 11 NFR IDs (grep-derived, printed): `NFR-AUD-01, NFR-DET-01, NFR-DQ-01, NFR-FAIR-01, NFR-IRI-01, NFR-LEAK-01, NFR-LIC-01, NFR-PHASE-01, NFR-REP-01, NFR-SEC-01, NFR-TDEF-01`. Grepping both artifacts for every one of the 11: only `NFR-AUD-01, NFR-DET-01, NFR-REP-01` appear in either file; `NFR-DQ-01, NFR-FAIR-01, NFR-IRI-01, NFR-LEAK-01, NFR-LIC-01, NFR-PHASE-01, NFR-SEC-01, NFR-TDEF-01` appear in neither. Unlike the `NFR-REP-01` case, none of these eight has its defining substance argued elsewhere in the artifacts under an uncited synonym — this unit's own text repeatedly delegates the adjacent concerns explicitly rather than silently restating them: the estimand orientation and its reversed-sign control are stated as owned by `evaluation-and-comparison` § SEC-C-02 (not restated here — NFR-FAIR-01/comparison-wide-mask territory); IRI, phase-boundary, licensing and target-definition are outside a bootstrap/CI library's surface entirely and are not paraphrased anywhere in either file. This is the same pattern iteration 1 already confirmed clean for the FR families, now extended to the NFR family: **NFR-REP-01 was the only miss** — the completeness gap iteration 1 found is fully closed, and no second miss of the same class was found in this pass.

### Regression check

Sources, both coverage tables, both printed counts, and the dependent "two fewer than five" phrase were all re-read this pass; no new inconsistency was introduced by the repair. No other section of either artifact was touched by the diff between iterations per the correction note's own scope statement, and no drift from that statement was found.

### Standing conclusions (iteration 1, not re-derived)

FR-family completeness (1 requirement, FR-P1-05-8, 0 untested), the RNG-pin engineering-contract classification with its NumPy-version dependency stated, and the no-numeric-memory-ceiling posture (services.md's 10.0 GB quoted as upstream and not adopted, change record owed elsewhere) are taken as verified per iteration 1 and were not re-checked in this pass, per the dispatch brief.

### Findings

None outstanding. No Critical, no Major, no Minor raised this iteration.

### Summary

The sole iteration-1 Major — `NFR-REP-01` uncited despite being the provision two central claims rest on — is repaired in both artifacts, with the dependent row counts and the "two fewer than five" arithmetic independently verified against the tables rather than trusted from prose. A full re-derivation across all 11 project NFR IDs (not only the one named in the dispatch) confirms `NFR-REP-01` was the only miss; the other eight untouched IDs are legitimately out of this unit's surface, each with an explicit delegation elsewhere in the text rather than a silent restatement. This is a terminal advisory pass: the verdict below informs the human at the approval gate and does not itself gate.

READY

## Review — 2026-09-01 confirming pass

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 1 of 2 (fresh budget after human gate rejection; advisory dispatch — this verdict informs the human, it does not itself gate)

### What this pass re-verified, independently

- **The "residual NFR-ID" check, extended.** Re-derived the 11 project NFR IDs from `requirements.md` and grepped both artifacts (already done at iteration 2 above, re-confirmed here): only `NFR-AUD-01`, `NFR-DET-01`, `NFR-REP-01` appear in either file; the other eight are absent and each has substance that either belongs to another unit's surface (IRI, phase-boundary, licensing, target-definition) or is explicitly delegated elsewhere in this unit's own text (estimand orientation to `evaluation-and-comparison` § SEC-C-02). No new uncited-substance instance found.
- **`FR-P1-05-*` and `FR-P1-06-*`, set-differenced against `requirements.md` directly** (not against this unit's own map, per the dispatch instruction). `requirements.md` defines `FR-P1-05-1` through `-22` (23 IDs including the `-16`/`-19`/`-20`/`-21`/`-22` additions) and `FR-P1-06-1` through `-4`. Of the 23 `FR-P1-05-*` rows, only **FR-P1-05-8** (the bootstrap requirement) is this unit's — the other 22 belong to `models-and-baselines`, `evaluation-and-comparison`, and `regimes-diagnostics-reporting` (model set, seeds, grids, ablations, breakdowns, locked-test guard, registry schema, regime-count audit, etc.) and neither artifact paraphrases their substance without citing them — they are simply out of a bootstrap library's surface. `FR-P1-06-1…4` (phase-transition-manifest freeze, seventeen-item protected set, weight-carry prohibition, reuse register) is likewise none of this unit's business and is correctly absent from both files. **No defect found in this range.**
- **`tech-stack-decisions.md`'s three coverage-table rows, checked against the dispatch brief's own characterization.** The brief describes them as "`NFR-AUD-01`, `NFR-DET-01`, `NFR-REP-01`" — that is **not** what the table (§ Requirement coverage, three rows) actually lists: it is **`FR-P1-05-8`, `NFR-DET-01`, `NFR-REP-01`**. `NFR-AUD-01` does not appear anywhere in `tech-stack-decisions.md`; it appears only in `security-requirements.md`'s coverage table (row 5, `SEC-S-01` · `TA-10, TA-21`). This is a factual correction to the dispatch brief, not a finding against the artifact — the artifact's actual three rows are internally correct (an append-safe-registry requirement like `NFR-AUD-01` legitimately raises no technology choice, which is exactly why the artifact's own text at line 167 excludes it and names `FR-P1-04-5`/`NFR-AUD-01` together as the two rows absent from this file relative to `security-requirements.md`'s five). Recorded here per the convention of verifying a fact before building on it, since the brief asked this be checked "by substance."
- **Acceptance-row completeness, re-counted.** `security-requirements.md`'s `NFR-AUD-01` row lists **`TA-10, TA-21`** — both, not truncated to the first. No cited requirement row in either table was found truncated to a single acceptance row where the requirement carries two.
- **Row-count arithmetic, re-derived.** `security-requirements.md`: 5 coverage rows (`FR-P1-05-8, FR-P1-04-5, NFR-REP-01, NFR-DET-01, NFR-AUD-01`), counted directly off the table. `tech-stack-decisions.md`: 3 coverage rows (`FR-P1-05-8, NFR-DET-01, NFR-REP-01`), counted directly. The two tables are **not** disjoint or simply nested — `tech-stack-decisions.md` carries `FR-P1-05-8` and `NFR-DET-01`/`NFR-REP-01`, all three of which also appear in `security-requirements.md`; `security-requirements.md` additionally carries `FR-P1-04-5` and `NFR-AUD-01`, which `tech-stack-decisions.md` omits. `tech-stack-decisions.md`'s table is therefore a **subset** of `security-requirements.md`'s (3 of its 3 rows recur in the 5), so "two fewer" (5 − 3 = 2) is arithmetically sound here — the subset trap the brief warns of (seen on `models-and-baselines`) does **not** reproduce on this pair.
- **Estimand and bootstrap specifics.** Confirmed present and exact in both files: vector time-block bootstrap, 24-hour blocks carrying all three stations together, 10,000 replicates, seed 20221201, 95% CI, cross-station paired-error correlation reported (R-121/W-7); within-station/naive bootstrap explicitly never substituted (R-116, TS-S-02). The paired loss differential (benchmark minus model, equal-station weighting) is correctly treated as owned by `evaluation-and-comparison` § SEC-C-02 and not redefined here (SEC-S-02, TS-S-02) — consistent with the project's single-definition mandate.
- **Q1/Q2 answers.** Q1 (disclosure plus G-06 adjudication) is stated exactly as the non-widening-outcome route in § SEC-S-03/TS-S-03: disclosed as designed, run proceeds, and the outcome becomes a named G-06 item — not silently absorbed. Q2 (CPU-completeness only, measurement owed): both files assert CPU-completeness with **no numeric memory ceiling**, explicitly refuse to adopt `services.md`'s 10.0 GB figure (quoted as upstream, not adopted, change record owed elsewhere), and state the peak-memory figure is owed as a fixture measurement. No ceiling has crept in.
- **Mechanism-vs-convention.** Every "engineering contract, not scientific constant" and "assertable artifact fact rather than a log line" framing in both files states the enforcement mechanism (signature-level `TypeError`, `BootstrapError` on unconfirmed method, `BootstrapResult`'s recorded seed/generator/hash) at the point the guarantee is claimed, not deferred to `## Assumptions` alone.
- **Not-yet-discharged items.** Both files continue to state G-09 signed (D-31) with preconditions UNMET, stage 3.1 FAIL, `configs/` absent, no Python interpreter present, and every coverage-table row `Pending` — nothing is newly claimed discharged in either file relative to iteration 2.

### Findings

None. No Critical, Major, or Minor findings this pass — this is a confirming pass over artifacts unchanged since the terminal iteration-2 READY above; the one substantive check this pass added beyond iteration 2 (the `FR-P1-05-*`/`FR-P1-06-*` set-difference against `requirements.md`, and the correction to the dispatch brief's mischaracterization of `tech-stack-decisions.md`'s three rows) surfaced no new defect.

### Summary

A fresh, independent set-difference of `FR-P1-05-*` and `FR-P1-06-*` against `requirements.md` (rather than this unit's own map) confirms both artifacts cite exactly the one FR-P1-05 requirement that is theirs (`FR-P1-05-8`) and correctly omit the other 22 `FR-P1-05-*` and all 4 `FR-P1-06-*` IDs, which belong to other units. The dispatch brief's description of `tech-stack-decisions.md`'s three coverage rows as `NFR-AUD-01, NFR-DET-01, NFR-REP-01` does not match the artifact — the actual three are `FR-P1-05-8, NFR-DET-01, NFR-REP-01`, and `NFR-AUD-01` correctly appears only in `security-requirements.md`; this is recorded as a correction to the brief, not a defect in the artifact. Acceptance-row completeness (`NFR-AUD-01` → `TA-10, TA-21`, both), the row-count arithmetic ("two fewer than five"), the Q1/Q2 answers, the exact bootstrap/estimand specifics, and the not-yet-discharged gate language all re-verify clean.

READY
