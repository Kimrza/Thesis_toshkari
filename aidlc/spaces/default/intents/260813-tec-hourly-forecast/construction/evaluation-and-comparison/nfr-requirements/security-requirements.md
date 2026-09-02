# Security Requirements — `evaluation-and-comparison`

**Unit** `evaluation-and-comparison` (Bolt 9) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NOTHING HERE IS CLAIMED SATISFIED
>
> **FR-P1-05-7's row is `Pending`** — **APPROVED under D-32 (2026-08-28), never run, NOT
> passed.** **TWO requirements have no acceptance row at all and are `UNTESTED` — FR-P1-05-17
> and FR-P1-05-20** *(banner corrected 2026-09-01; superseded: "FR-P1-05-17 has no acceptance
> row at all". FR-P1-05-20 was added to the coverage table on the iteration-1 Major and this
> banner, which states the fact first, was left behind)*. So **3 of this artifact's 8 coverage
> rows carry no result** — one approved-but-unrun, two with no row. An approved-but-unrun row
> and an absent row are **both `Pending`, and neither is evidence**.
>
> **WS-16 and TA-11 are undischarged.** **BLK-07 is open**, so the mask-ordering refusal this
> artifact requires is **specified and unrunnable today**. **G-09 is signed (D-31) with its own
> preconditions UNMET**; **stage 3.1 remains FAIL**; `configs/` does not exist; **no Python
> interpreter exists in this environment**, so every test is **written-but-unexecuted** or
> unwritten and **no metric has ever been computed**.
>
> No scientific value is decided here, and TE §18.2's absolute rule stands.

## Sources

- `../functional-design/business-rules.md` — **R-103** (the BLK-08 joint transform-resolution contract, **narrowed to `ABL-DIFF`** — one statement, two halves), **R-104** (**inverse-before-metric enforced at the boundary every caller crosses**), **R-105** (`07`'s half of the eighth amendment: the stamp refusal at this unit's boundary), **R-106** (comparison-set membership is **declared configuration, checked exactly**), **R-107** (**mask identity, once-only registration, and the G-05 freeze**), **R-108** (the estimand is an **ordered executable contract**, and its result carries its own interpretation), **R-109** (the G-06 evaluation: **hash-receipt before metrics, one chokepoint, and exactly 2–31 December**), **R-110** (honesty mechanics: completeness upstream, the **disclosure trigger as a field**, the **caveat emitted by the path**), **R-111** (`tests/test_common_masks.py`: masks plus the matched-window assertion, and the WS-13 proposal), **R-112** (IRI and GIM join at evaluation time onto the frozen mask, and **this unit narrows nothing**).
- `../functional-design/business-logic-model.md` — **W-1** (comparison-mask construction and once-only registration), **W-2** (the estimand pipeline in its ordered form), **W-3** (the narrowed BLK-08 resolver and the boundary refusal), **W-4** (`07`'s stamp refusal), **W-5** (the G-06 locked-test evaluation path), **W-6** (the honesty mechanics), **W-7** (what `scripts/07_evaluate_and_report.py` orchestrates and what it must not), **W-8** (the `test_common_masks.py` verification plan).
- `../../governance-guards/functional-design/business-rules.md` — **R-25**'s durable access log and the `open_restricted` chokepoint, which § SEC-C-01's ordering refusal must attach to.
- `../../models-and-baselines/nfr-requirements/security-requirements.md` — § SEC-M-04, the prediction-hash receipt whose producing half is that unit's and whose refusal this unit enforces.
- `../../../inception/requirements-analysis/requirements.md` — **FR-P1-04-7**, **FR-P1-05-7**, **FR-P1-05-9**, **FR-P1-05-12**, **FR-P1-05-17**, **FR-P1-05-20**, **NFR-FAIR-01**, **NFR-IRI-01**.
- `../../../../../../../../PreFlight/vision_document(3)(2)(2).md` — **§2.3** (the paired loss differential as the confirmatory estimand), **§2.4** (the **binding honesty rule**), **§5.3** and the **G-06** gate row, **§5.4** (practical-relevance thresholds), **§6.6** (the spatial-representativeness mismatch), **§8.3** (the required performance-blind pre-G-05 audit, distinct from G-06).
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§1.3** (the estimand), **§1.4**, **§5**, **§5.2** (`gim_network_overlap_flag`), **§13.6** (the vector time-block bootstrap), **§18.2–18.3**, **§19** (TA-11), **§16** (WS-16).
- `evidence/DECISIONS.md` — **D-28** (the G-06 scored set: **2–31 December 2022, 30 days**, first 24 h excluded and counted), **D-32** (the eight approved §15.2 rows).
- `nfr-requirements-questions.md` — Q1 = A, Q2 = C, and the receipted Consolidated Summary Confirmation.

---

## Scope note

`produces_kinds` excludes `performance-requirements`, `scalability-requirements` and
`reliability-requirements` for a `library` unit. Assessed anyway:

| Category | Assessment for `evaluation-and-comparison` | Where it lives |
|---|---|---|
| **Performance** | No latency target. The heaviest operation is the bootstrap, and its cost is `statistical-inference`'s. Nothing here is optimised for speed; § SEC-C-01's ordering check runs once per access. | — |
| **Scalability** | Bounded: three cells, one locked month, a fixed comparison set. No growth projection. | — |
| **Reliability** | **Fail-closed at the boundary**: `07` **refuses** a frame with an absent or mismatched stamp, **refuses** a metric before the hash receipt, and **refuses** a transformed-space value at every metric entry point. This unit would rather compute nothing than compute a comparison that is not the declared one. | § SEC-C-02, § SEC-C-03 |
| **Security** | This artifact — **fairness and the integrity of the reported result**. The asset is the honesty of the comparison. | — |
| **Observability** | The mask manifest with stable IDs and reported row counts; the G-06 hash receipt; the disclosure trigger field; the emitted caveat. | § SEC-C-01, § SEC-C-03, § SEC-C-04 |

---

## SEC-C-01 — One mask, registered once, frozen before the test is opened

**Requirement (NFR-FAIR-01, TC-16, R-107, W-1).** A **single comparison-wide intersection
mask** is computed **once per comparison set** and used for **every** model-versus-baseline
comparison. **No pairwise or model-specific mask is produced.** Masks carry **stable IDs and
reported row counts**, and registration is **once-only** — a second registration of the same
comparison set **fails**.

**Requirement (R-106).** Comparison-set membership is **declared configuration, checked
exactly**. A set that differs from its declaration **fails**; it does not proceed on the
membership it found.

> ### Requirement (Q1 = A) — the freeze-precedes-access ordering is MACHINE-ENFORCED
>
> **FR-P1-05-17 is `UNTESTED` and has no acceptance row.** What it governs is an **ordering**:
> the comparison-wide mask must be **frozen before** the locked test is accessed.
>
> **The locked-test access path REFUSES** unless a registered, frozen mask bundle exists whose
> **registration timestamp precedes the access**. A **hard failure**, not a warning, not a
> recorded note.
>
> **Why an after-the-fact record is not enough.** A mask frozen **after** December was opened
> could have been shaped by what December contained, and **no downstream check can detect
> it** — the mask is what every comparison is measured *through*, so a comparison computed on
> a compromised mask looks entirely normal. Worse: **the run that would violate the ordering
> is the run that writes the record proving it.**
>
> **Two costs, stated rather than discovered.** (1) This is a **cross-unit half-contract**
> with `governance-guards`' access path; **this artifact states only this unit's half** — that
> a frozen, registered bundle with a preceding timestamp is a **precondition of access** — and
> **does not declare the contract satisfied**. (2) It is **unrunnable today**: **BLK-07 is
> open** and `open_restricted` does not exist, so there is no access path to attach the
> refusal to. The same posture `models-and-baselines` takes for its December-window block.

**Requirement (R-111, W-8).** `tests/test_common_masks.py` asserts **the masks and the
matched-window** property together. WS-13's evidence question — what proves two representations
encode the same window — **stays open**, and R-111 carries the proposal rather than the answer.

## SEC-C-02 — The estimand is an ordered contract, and its sign is protected twice

**Requirement (R-108, Vision §2.3, TE §1.3).** The confirmatory estimand is the **mean
within-station difference of squared errors**, **benchmark minus model**, with **equal-station
weighting**. **A positive value favours the model.** It is an **ordered executable contract**,
and its result **carries its own interpretation**.

> ### Requirement (Q2 = C) — two mechanisms, because they protect against different failures
>
> **1 — A reversed-sign negative control**, on the precedent TA-07/WS-04 sets for DCB: a
> **deliberately inverted computation must FAIL** the test. This proves the **producer**
> computes `benchmark − model` rather than merely claiming to.
>
> **2 — The convention travels as data.** Every emitted estimand value carries fields naming
> its **orientation** (`benchmark_minus_model`) and its **weighting** (`equal_station`), and a
> **consumer that reports the value without them fails**. This prevents a **correct** value
> being read under the **wrong** convention downstream.
>
> **Neither substitutes for the other**, which is why this project's usual objection to
> duplicating an obligation does not attach: the control verifies the producer, the fields
> protect the consumer, and a failure in either place is invisible to the other. The same
> reasoning `governance-guards` R-23 uses to keep both phase-boundary limbs.
>
> **Why the sign is worth two mechanisms.** Reversing it turns *"the LSTM beats IRI"* into
> *"IRI beats the LSTM"* — **the entire thesis conclusion** — and **the number looks identical
> either way**. There is no plausibility check that catches it.
>
> **Who owes the consumer half** *(named 2026-09-01 on adversarial finding 2, Minor — the Q2 block stated the obligation without saying whose it is)*: **`regimes-diagnostics-reporting`**, which owns the **primary results table** and is therefore the consumer that would report an estimand value. **This unit states only the producer half** — that the fields are emitted and what they carry — and **does not declare the consumer half met**. `regimes-diagnostics-reporting` has not stated it.
>
> **The cost:** extra fields on every emitted result, and one more test.

**Requirement (R-104, W-3).** **Inverse-before-metric is enforced at the boundary every caller
crosses** — a transformed-space value reaching any metric entry point **raises**. **`ABL-DIFF`
inverse-transforms to absolute TECU before any metric.**

**Requirement (R-103).** BLK-08's joint transform-resolution contract is **narrowed to
`ABL-DIFF`**, stated **once in two halves**. `features-and-splits` holds half B; **this unit
does not declare the joint contract satisfied from one side.**

**Requirement (R-105, W-4).** `07` **refuses** a frame whose stamps are **absent or
mismatched**: a `partition_id` mismatch raises **`PartitionError`**, an absent stamp or a
`transform_id` mismatch raises **`LeakageError`**, and a **wrong-partition mask** raises
**`FairnessError`**. Three distinguishable failures, not one generic refusal.

## SEC-C-03 — The locked test opens once, and the receipt precedes every metric

**Requirement (R-109, W-5, Vision §5.3).** The G-06 evaluation is a **one-shot,
hash-before-metrics** event, through **one chokepoint**, scoring **exactly 2–31 December
2022 — 30 days**, with the **first 24 hours excluded and counted** (D-28).

**Requirement.** The **prediction hash receipt precedes any metric computation**. Every `DEC`
metric entry point **refuses without a verified receipt** — the design is **fail-closed** while
the producing half is unbuilt. The receipt's **producer** is `models-and-baselines`
(`scripts/06_train_and_predict.py`) and its **destination** is `foundation`'s registry row,
which **refuses a hash presented by the metric-computing process**. **This unit enforces the
refusal; it does not produce the receipt**, and does not declare that two-half contract
satisfied.

**Requirement — the pre-G-05 audit is a different event and must not be blocked.** The
**required, performance-blind December coverage and regime audit** (Vision §8.3) is
**distinct** from the G-06 evaluation. Nothing in this unit's refusals may block it; a guard
that did would breach Vision §8.3 as surely as one that let a model see December.

**Requirement (Vision §5.4, PC-09).** **No practical-relevance threshold is introduced,
changed or reinterpreted after the December locked test is opened.**

**Requirement (Vision §8.3).** Any **test-driven change** made to the pipeline **after**
locked-test access is **labelled exploratory**. Every access records
**`locked_test_accessed = true`**.

## SEC-C-04 — The honesty mechanics are emitted, not remembered

**Requirement (R-110, W-6, Vision §2.4).** The honesty rule is **mechanised in three parts**:
**completeness is checked upstream**, the **disclosure trigger is a field** rather than a
judgement, and the **caveat is emitted by the path that produces the result** rather than added
by an author.

**Requirement.** The **three mandatory difficulty controls** — persistence, 24-hour seasonal
persistence, and fitted station×month×hour climatology (trained on training partitions only) —
are **co-reported in the same primary results table** as the LSTM-vs-IRI comparison, and
**never relegated to an appendix**.

**Requirement.** **Any baseline that beats the LSTM on the locked test is disclosed** in the
primary results table **and** in the abstract-level conclusion. A favourable LSTM-vs-IRI result
**never licenses silence** about an unfavourable LSTM-vs-persistence or LSTM-vs-climatology
result.

**Requirement (R-112, Vision §6.10, TE §5.2).** IRI and GIM **join at evaluation time onto the
frozen mask**, and **this unit narrows nothing** — it does not re-scope, re-mask or re-weight
what it was handed. CODE final GIM is **never presumed independent before the network-overlap
audit**, and the **`gim_network_overlap_flag` result is disclosed once that audit runs**.

**Requirement (Vision §6.6).** The **spatial-representativeness mismatch** is stated **wherever
an IRI or GIM comparison is reported** — part of any measured difference is a **geometry and
sampling artefact rather than skill**.

**Requirement (Vision §2.2, §7.0B).** The abstract-level interpretation states that **Phase 2
is a fixed-protocol replication on a new target lineage, not a second statistically independent
blind test**, because it reuses the December timestamps after Phase 1 has reported them.

**The table itself is `regimes-diagnostics-reporting`'s.** This unit produces the values and
the trigger field and emits the caveat; **it does not own the primary results table**, and
states these obligations rather than discharging them.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| FR-P1-04-7 | SEC-C-01 | WS-16 (primary), TA-11 (supporting) | `Pending` |
| **FR-P1-05-7** | SEC-C-02 | ⚠ **`Pending`** — row **APPROVED under D-32**, **never run, NOT passed** | not evidence |
| **FR-P1-05-17** | SEC-C-01 | ⚠ **NO ROW AT ALL** — `UNTESTED` | not evidence |
| NFR-FAIR-01 | SEC-C-01, SEC-C-02 | WS-16, TA-11 | `Pending` |
| **FR-P1-05-12** | SEC-C-03 | **WS-18, TA-18** — rows owned by `features-and-splits` and `governance-guards` | `Pending` — **the write-once and hash-before-metric criterion this unit enforces** |
| **FR-P1-05-9** | SEC-C-04 | **TA-20** — row owned by `regimes-diagnostics-reporting` | `Pending` — **obligation stated here, discharged there** |
| **FR-P1-05-20** | SEC-C-04 | ⚠ **NO ROW** — `UNTESTED` | not evidence |
| NFR-IRI-01 | SEC-C-04 | WS-10, TA-07 | `Pending` — **test written, UNEXECUTED** |

**Derived and printed**: 4 requirement sections (SEC-C-01…SEC-C-04); **8** coverage rows *(corrected twice on 2026-09-01. Iteration 1, Major: **FR-P1-05-9** and **FR-P1-05-20** were restated almost verbatim in § SEC-C-04 and cited nowhere. Iteration 2, **Critical**: **FR-P1-05-12** — the locked-test write-once and hash-before-metric criterion — is the mechanism § SEC-C-03 enforces, and it too was uncited, **in the same family the iteration-1 repair was meant to sweep**. Superseded figures preserved: **5**, then **7**. The lesson is recorded rather than the number alone: a repair scoped to the IDs a finding named is not a sweep, which is `project.md` `fd-2026-08-30-sweep-derive-sites` in a third form.; superseded figure preserved: **5**. **FR-P1-05-9** and **FR-P1-05-20** are restated almost verbatim by § SEC-C-04 — the three difficulty controls co-reported in the primary results table, and any baseline beating the LSTM disclosed there and at abstract level — and this unit's own `business-rules.md` names both by ID at `:697` and `:761`. Neither appeared in Sources or in either coverage table. The artifact's own inclusion criterion — a requirement "which this artifact states an obligation against", used to justify NFR-IRI-01 — is met at least as strongly by these two.)* — the 4 requirements the `functional-design` map carries, plus NFR-IRI-01, FR-P1-05-9 and FR-P1-05-20 which this artifact states obligations against; **3 carrying no result** *(leading numeral corrected 2026-09-01; superseded: "**2 carrying no result**, in **two different states**". The sentence went on to state "so **3 carry no result**, not 2" — so the repair contradicted itself inside one sentence, which is the sweep defect at its smallest scale)*, in **three different states** — one
approved-but-unrun (**FR-P1-05-7**) and **two** with no row (**FR-P1-05-17**, **FR-P1-05-20**) — so **3 carry no result**, not 2 *(decomposition corrected 2026-09-01 in the same sweep that corrected the banner; superseded: "one approved-but-unrun (FR-P1-05-7), one with no row (FR-P1-05-17) — matching the map's own corrected wording". The map's wording described the state before FR-P1-05-20 was added to this table on the iteration-1 Major; **the headline moved 5 → 7 → 8 and this decomposition tracked neither addition**)*; **0** rows claimed satisfied.

## Assumptions & Open Questions

- **[Q1]** The ordering refusal is **new at this stage** — `functional-design` records the ordering as a G-05 record property. It is a **half-contract**, and it is **unrunnable while BLK-07 is open**. Where the mask registry's timestamp is read from, and by what, is **owed at 3.5**.
- **[assumption]** A registration timestamp is trustworthy enough to order against an access timestamp. Both come from the same clock domain **only if** the mask registry and the access log are written by the same host. **On Kaggle they may not be**, and Kaggle's durability semantics are unmeasured — so the comparison could be made across two clocks with no stated skew bound. **Raised, not resolved.**
- **[Q2]** Both sign mechanisms are required. **Neither alone is sufficient**, and the artifact does not claim either is implemented.
- **Carried — the prediction-hash receipt is a two-half contract**; this unit **enforces** the refusal and `models-and-baselines` **produces** the receipt. **Not satisfied from one side.**
- **Carried — BLK-08's half A/half B split** with `features-and-splits`, narrowed to `ABL-DIFF`. **Not satisfied from one side.**
- **Carried — the primary results table is `regimes-diagnostics-reporting`'s.** This unit states the honesty obligations; it does not discharge them.
- **Carried — WS-13's evidence question stays open** (R-111).
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:07:53Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `security-requirements.md` § SEC-C-04, § Sources, Requirement coverage; `tech-stack-decisions.md` (same gap, no SEC-C-04 analogue) | **FR-P1-05-9 and FR-P1-05-20 are substantively restated near-verbatim in SEC-C-04 but neither ID is cited anywhere in either artifact's Sources or Requirement coverage table.** SEC-C-04's "the three mandatory difficulty controls … are co-reported in the same primary results table … and never relegated to an appendix" is FR-P1-05-9's requirement text verbatim (`requirements.md:402`, acceptance row **TA-20**). SEC-C-04's "Any baseline that beats the LSTM on the locked test is disclosed in the primary results table and in the abstract-level conclusion" restates FR-P1-05-20 (the BENCH-06 disclosure limb, `requirements.md:1009`, `UNTESTED`). Crucially, **this same unit's own upstream `functional-design/business-rules.md:96` already names both IDs by ID** ("consulted for context: … FR-P1-05-9 … FR-P1-05-20") and even carries TA-20/`UNTESTED` acceptance detail for them (`business-rules.md:697,761`) — so the omission is not that the IDs are unknown to this unit, only that `nfr-requirements` dropped them. The stated criterion this artifact itself used to justify listing a fifth requirement, NFR-IRI-01, is "which this artifact states an obligation against" (§ Requirement coverage note, line 200-204) — FR-P1-05-9 and FR-P1-05-20 meet that criterion at least as strongly, since SEC-C-04 states their obligations in the artifact's own prose. This is the same defect class that produced a Major on the two immediately preceding units (approved acceptance rows TA-34/TA-35 uncited). | Add FR-P1-05-9 (→ SEC-C-04, TA-20) and FR-P1-05-20 (→ SEC-C-04, TA-20/`UNTESTED`) to Sources and to both artifacts' Requirement coverage tables, with status `Pending`/`UNTESTED` as appropriate, and update the "Derived and printed" counts (4→6 rows in `security-requirements.md`) to match. |
| 2 | Minor | `security-requirements.md` § SEC-C-02, Q2 block (lines 99-107) | The Q2 sign-convention mechanism 2 ("the convention travels as data … a consumer that reports the value without them fails") never names which unit *owes* that consumer-side obligation — the dispatch brief specifically asked this be checked, and the text states the mechanism binds "a consumer" without naming one. `regimes-diagnostics-reporting` is named elsewhere as the owner of the primary results table (§ SEC-C-04), which is the most plausible consumer, but SEC-C-02 itself is silent on this, so a reader of SEC-C-02 alone cannot tell who is bound. | Name the consumer unit(s) explicitly in SEC-C-02, or cross-reference § SEC-C-04's ownership statement, so the obligation is traceable to an owner rather than left implicit. |

### Validation Tool Results

No stage-listed validation tool was named in the dispatch brief or the stage definition path provided; none was run. Findings above are derived by direct cross-reference of the two PRIMARY/companion artifacts against `requirements.md` and this unit's own `functional-design/business-rules.md` (both within read scope), with line numbers printed.

### Coverage limits

Within an 8-tool-call budget: read both nfr-requirements artifacts in full; grep-derived the full FR-P1-04-*/FR-P1-05-*/NFR-FAIR-01/NFR-IRI-01/NFR-LEAK-01 ID list from `requirements.md`; grep-checked FR-P1-05-9/FR-P1-05-20 against this unit's `business-rules.md`. Did not re-open `domain-entities.md`/`business-logic-model.md` or the cited `governance-guards`/`models-and-baselines` sibling files (single spot-check permitted, not exercised — the claims about those units' owned halves, e.g. SEC-M-04's producing half, are stated as unenforced/uncompleted throughout and were taken at face value rather than independently verified against the sibling artifact). Did not independently verify NFR-LEAK-01's applicability beyond confirming it is not cited here and its acceptance rows (WS-11/TA-08/TA-11) look like `features-and-splits`/upstream territory rather than this unit's.

### Summary

The two "unrunnable" claims, the D-28 scored-set figure, the clock-skew objection placement, the sign-convention pair's producer/consumer split, and all printed counts check out against the text. The blocking issue is a requirement-coverage gap of the exact kind that has now recurred across three units running: two requirements (FR-P1-05-9, FR-P1-05-20) whose substance this artifact states almost verbatim, and whose IDs this unit's own functional-design artifact already carries with acceptance-row detail, are absent from both nfr-requirements artifacts' Sources and coverage tables.

NOT-READY

## Review — iteration 2 (terminal)

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z (see printed `date -u` output for exact timestamp)
**Iteration:** 2 (terminal — adversarial)

### Iteration 1 findings — verified

- **Major (FR-P1-05-9 / FR-P1-05-20 uncited):** RESOLVED. Both now appear in the Sources
  list (line 25) and the coverage table (lines 200–201) — FR-P1-05-9 against TA-20
  (row owned by `regimes-diagnostics-reporting`), FR-P1-05-20 correctly marked `NO ROW —
  UNTESTED`.
- **Minor (unnamed consumer half):** RESOLVED. § SEC-C-02 (line 113) now names
  `regimes-diagnostics-reporting` as the owner of the consumer half and states this unit
  declares only the producer half.
- **Count correction 5 → 7:** verified consistent inside `security-requirements.md` — the
  Sources line cites exactly 7 requirement/NFR IDs.

### New findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | `security-requirements.md` Sources / coverage table | **FR-P1-05-12 is substantively implemented here but remains uncited — the identical defect class that failed iteration 1.** `business-rules.md` lines 619–623 and 667 implement FR-P1-05-12's write-once/hash-receipt criterion as this unit's own mechanism ("Hash-receipt precondition… re-verifies the prediction file against it before computing (write-once detection, FR-P1-05-12)… detected by the re-verification, per FR-P1-05-12's write-once criterion → raises"), and `security-requirements.md` itself describes this exact mechanism under SEC-C-02/SEC-C-03 ("refuses a metric before the hash receipt"). `business-rules.md`'s own Sources line (line 96) labels FR-P1-05-12 "consulted for context" — the same label it gave FR-P1-05-9 and FR-P1-05-20 before iteration 1 found both to be substantively implemented and required as Sources. The dispatch's mandated completeness re-check (set-difference the FR-P1-05-* family against what is cited) did not catch this, meaning the repair's own verification step is unsound. | Add FR-P1-05-12 to Sources and the coverage table against SEC-C-02/SEC-C-03, with an honest acceptance-row status (no dedicated WS/TA row is named for it in the artifacts reviewed — mark `UNTESTED` unless one is found). Re-run the FR-P1-05-* / FR-P1-04-* set-difference against `business-rules.md`'s full reference list (9 IDs: FR-P1-04-5, FR-P1-04-7, FR-P1-04-9, FR-P1-05-6, FR-P1-05-7, FR-P1-05-9, FR-P1-05-12, FR-P1-05-17, FR-P1-05-20), not only against `requirements.md`'s full FR-P1-04/05 family, which is too broad (most of that family belongs to other units). |
| 2 | Major | `tech-stack-decisions.md`, "Derived and printed" paragraph (~line 121) | The count-correction sweep from iteration 1 was not propagated: `tech-stack-decisions.md` still reads "**4** coverage rows — one fewer than `security-requirements.md`'s **five**", but `security-requirements.md`'s Sources count is now corrected to **seven** (7 IDs, not 5). The dependent sentence is now doubly wrong — it neither matches the new count arithmetically (4 is not "one fewer than 7") nor states the current figure. This is the exact pattern `project.md` already names as this project's most-repeated defect (`delivery-planning:dp-1`, "extend a correction sweep into the downstream artifacts that consumed the corrected fact"). | Recompute and restate: either name the actual current relationship (e.g., "4 of the 7 security-requirements.md IDs raise a technology choice; NFR-IRI-01 and the three FR-P1-05-* honesty-mechanics IDs do not"), or drop the comparative sentence and state `tech-stack-decisions.md`'s own count independently, since a cross-file comparative count is exactly the kind of dependent figure this project has repeatedly let go stale. |

### Confirmed no regression

Diff-adjacent spot-check found no unrelated drift: the Sources list, coverage table, count
paragraph, and § SEC-C-02 blockquote are the only sections that changed shape from
iteration 1; § SEC-C-01, § SEC-C-03, and the standing "unrunnable" / D-28 / sign-convention
conclusions named in the dispatch brief as already-verified were not touched and were not
re-derived here (per instruction).

### Do-not-report-as-discharged list

Confirmed still true and not contradicted anywhere in the reviewed diff: FR-P1-05-7
`Pending` (D-32, never run); FR-P1-05-17 / FR-P1-05-20 no row; WS-16, TA-11, WS-10, TA-07,
TA-20 and the §18.3 preflight undischarged; no metric ever computed; G-09 signed with
preconditions unmet; stage 3.1 FAIL; `configs/` absent; BLK-07 open.

## Review — 2026-09-01 re-verification after gate rejection

**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 1 (fresh budget after human gate rejection; prior attempt's analysis lost to a scope-record overwrite, nothing persisted)

### Verification performed

1. **Minor repair (self-contradictory lead-in) — verified fixed.** Line 209 now reads "**3 carrying no result** ... in **three different states**" and line 210's decomposition sums to 3 (one approved-but-unrun FR-P1-05-7, two no-row FR-P1-05-17/FR-P1-05-20). The prior self-contradiction ("2 carrying no result ... so 3 carry no result, not 2") is gone; the superseded text is preserved in the inline correction box per this project's non-destructive-correction convention. No fresh inconsistency introduced by the repair.
2. **Independent re-derivation of the coverage table figure, both files, counted directly from the tables:**
   - `security-requirements.md` requirement-coverage table (lines 199–206): **8 rows** — FR-P1-04-7, FR-P1-05-7, FR-P1-05-17, NFR-FAIR-01, FR-P1-05-12, FR-P1-05-9, FR-P1-05-20, NFR-IRI-01. Matches the artifact's own "**8** coverage rows" claim.
   - `tech-stack-decisions.md` requirement-coverage table (lines 116–119): **4 rows** — FR-P1-04-7, FR-P1-05-7, FR-P1-05-17, NFR-FAIR-01. Matches "**4** coverage rows".
   - Dependent phrase: "four fewer than ... eight" = 8 − 4 = 4. Correct.
   - No fifth site carrying a stale figure was found across banner (line 12 — "one approved-but-unrun, two with no row" = 3, consistent), section bodies, both coverage tables, the printed derivation, and the `tech-stack-decisions.md` dependent phrase. All sites now agree at 8 / 4 / 3.
3. **Spot-checks of the two named repairs**, both confirmed: FR-P1-05-12 appears in Sources (line 29) and in both files' coverage tables (line 204 security; referenced via the dependent-count exclusion list in tech-stack); "four fewer than eight" arithmetic confirmed above.
4. **Regression checks, all confirmed present and unchanged in substance:**
   - Both "unrunnable today" claims: mask-ordering blocked by BLK-07 (security-requirements.md lines 15, 82, 214, 290; tech-stack-decisions.md lines 10, 74, 126) and the G-06 hash-receipt producer unbuilt (tech-stack-decisions.md lines 10–11, 104–108).
   - Clock-skew objection in TS-C-03's body: tech-stack-decisions.md lines 79 and 133 — "two timestamps that may be written by different hosts... No skew bound is stated anywhere."
   - Sign-convention pair (SEC-C-02, Q2 block) and its named-owner gap: security-requirements.md line 117 explicitly names `regimes-diagnostics-reporting` as owing the consumer half, and line 235 records this as an already-tracked Minor (finding 2) rather than a regression.
   - `regimes-diagnostics-reporting` named as owning the consumer half / primary results table: security-requirements.md lines 117, 190, 205, 219, 262, 265 — consistent throughout.
   - D-28's scored set: "2–31 December 2022, 30 days, first 24 h excluded and counted" appears identically in security-requirements.md (lines 32, 138) and tech-stack-decisions.md (line 25, abbreviated but consistent: "2–31 December, 30 days"). No other range asserted anywhere in either file.

### Findings

No new findings. The Minor from the prior (lost) attempt is confirmed repaired without regression. No fifth stale-figure site was found on independent re-derivation.

### Not newly discharged (confirmed still open, per dispatch guardrail)

FR-P1-05-7 remains `Pending`/approved-but-unrun, not passed (line 201). FR-P1-05-17 and FR-P1-05-20 remain no-row/`UNTESTED` (lines 202, 206). WS-16, TA-11, WS-10, TA-07, TA-18, WS-18, TA-20 and the §18.3 preflight remain undischarged throughout. BLK-07 remains open. No claim of any metric having been computed appears anywhere in either artifact.

### Summary

Both named repairs (Critical FR-P1-05-12 citation gap; Major dependent-count drift) verified sound, and the newly-surfaced Minor (self-contradictory lead-in) is now repaired cleanly, with the superseded text preserved rather than erased. Independent recount of both coverage tables and every site carrying the 8/4/3 figures found full agreement — no fifth uncorrected site. No regression in the unrunnable claims, clock-skew objection, sign-convention ownership, `regimes-diagnostics-reporting` attribution, or D-28's scored-set figure. Zero Critical, zero Major, zero Minor outstanding.

READY

### Summary

Both iteration-1 defects are genuinely fixed, but the same completeness-check class of
defect recurs once more (FR-P1-05-12, substantively implemented, uncited) and the
count-correction from iteration 1 was not swept into the sibling artifact
(`tech-stack-decisions.md`), leaving a now-inconsistent cross-file figure. Terminal pass:
findings are handed to the human gate rather than looped back for a third repair.

NOT-READY
