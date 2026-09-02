# Security Requirements — `models-and-baselines`

**Unit** `models-and-baselines` (Bolt 8) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NOTHING HERE IS CLAIMED SATISFIED — AND THIS UNIT HAS THE PROJECT'S LARGEST EVIDENCE GAP
>
> **9 requirements, 7 with no §16 or §19 acceptance row** — derived and printed by this unit's
> own `functional-design`, not carried from prose. That is the **largest untested share of any
> unit in this project**, and several of the seven are rules `project.md` lists under
> `## Forbidden` or `## Mandated`.
>
> **WS-14, WS-15, TA-12, TA-13 and TA-26 are owned and undischarged**; TA-20 is supported.
> **G-09 is signed (D-31) with its own preconditions UNMET**; **stage 3.1 remains FAIL**;
> `configs/` does not exist; **no Python interpreter exists in this environment**, so every
> test is **written-but-unexecuted** or unwritten and **no model has ever been trained**.
>
> No scientific value is decided here, and TE §18.2's absolute rule stands.

## Sources

- `../functional-design/business-rules.md` — **R-90** (a frame whose spec is not `(partition k, role "score")` never reaches partition *k*'s scoring), **R-91** (the confirmatory prediction is the three-seed mean, and nothing may be substituted), **R-92** (a confirmatory mean whose inputs disagree on provenance **fails**), **R-93** (the seed is never selected, and never on December), **R-94** (M-06 restores its **lowest-validation-RMSE** checkpoint, not its last epoch), **R-95** (tuning reads **January–November only**, and the residual is named), **R-96** (grid **content** is asserted, not only immutability), **R-97** (ablations are predeclared — **five named, four reachable in Phase 1**), **R-98** (M-03 is fitted on **training partitions only**), **R-99** (the +24 h horizon needs no code change), **R-100** (**Random Forest importance is diagnostic, and never a selection input**), **R-101** (selection is on mean per-fold skill score; the refit changes no hyperparameter), **R-102** (the model set is **closed**, and **two absences are evidence**), **R-102a** (`06` writes the prediction-hash receipt and refuses to exit without it).
- `../functional-design/business-logic-model.md` — **W-1** … **W-12**, in particular **W-3** (the confirmatory prediction and BLK-03's four limbs), **W-5** (**tuning, and the channel that stays open**), **W-6** (the grid freeze as content and immutability in one mechanism), **W-10** (two evidence obligations belonging to siblings), **W-12** (the one-shot `DEC` write and the receipt that must precede any metric).
- `../../governance-guards/functional-design/business-rules.md` — **R-25**'s durable access log, which R-95 mechanism 3 reads, and whose `AccessRecord` supplies `retrieved_at_utc` and `purpose`.
- `../../features-and-splits/nfr-requirements/security-requirements.md` — § SEC-F-02, whose answer to a missing acceptance row this unit applies at scale.
- `../../../inception/requirements-analysis/requirements.md` — **FR-P1-04-14**, **FR-P1-05-1** … **FR-P1-05-6**, **FR-P1-05-21**, **FR-P1-05-22**, **NFR-DET-01**, **NFR-LEAK-01**, **NFR-IRI-01**, **NFR-AUD-01** *(cited 2026-09-01 on adversarial finding 1, Major — § SEC-M-04 rests on this requirement's substance throughout: the durably flushed receipt, the refusal to exit holding a `DEC` prediction without one, the `locked_test_accessed = true` record, and the exploratory labelling of any post-access change. Acceptance rows **TA-10, TA-21**, owned elsewhere.)*.
- `../../../../../../../../PreFlight/vision_document(3)(2)(2).md` — **§8.3** (December must not inform selection; the trigger is December being **seen**), **§8.6** (seeds), **§2.4** (the binding honesty rule).
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§7.1** (grids exact and committed before G-05), **§7.2** (predeclared ablations), **§8.2** (model implementation ownership), **§8.3** (GRU removed; PyTorch prohibited), **§13.5** (seeds), **§18.2–18.3**, **§19**.
- `evidence/DECISIONS.md` — **D-121** (grid sizes), **D-122** (the seed set, *"Approved — supervisor sign-off pending"*).
- `nfr-requirements-questions.md` — Q1 = A, Q2 = B, and the receipted Consolidated Summary Confirmation.

---

## Scope note

`produces_kinds` excludes `performance-requirements`, `scalability-requirements` and
`reliability-requirements` for a `library` unit. Assessed anyway:

| Category | Assessment for `models-and-baselines` | Where it lives |
|---|---|---|
| **Performance** | The one genuine constraint is **CPU completeness**, not speed: TE §9.2 requires the whole workflow to run on CPU as a complete execution path, and M-06 is the largest compute in the project. **No runtime has been measured** — nothing has been trained. | § SEC-M-05 |
| **Scalability** | Bounded: three cells, calendar 2022, hourly, six model families, three seeds. No growth projection. | — |
| **Reliability** | **Fail-closed on identity**: a frame whose spec is not `(partition k, role "score")` **never reaches** partition *k*'s scoring; a confirmatory mean whose inputs disagree on provenance **fails**; `06` **refuses to exit** holding a `DEC` prediction with no receipt. | § SEC-M-01, § SEC-M-04 |
| **Security** | This artifact — **selection integrity**. The asset being protected is the honesty of the comparison, not a credential. | — |
| **Observability** | `TuningRecord`, the grid hash committed before G-05, the prediction-hash receipt, and the three-seed provenance record. | § SEC-M-02, § SEC-M-04 |

---

## SEC-M-01 — December cannot inform selection, and one channel stays open

**Requirement (R-95, W-5, Vision §8.3).** Model selection, feature selection, thresholds and
hyperparameters are **never** informed by December. **The trigger is December being *seen*,
not the locked test being opened** — the required pre-G-05 coverage audit means December is
legitimately seen earlier, and that is precisely the channel this closes.

**Three mechanisms.**

1. **`TuningRecord.partitions_read` excludes December.** Catches a December partition being
   read.
2. **`criterion_hash` equals `criterion_used_hash`** — the criterion declared **before**
   tuning equals the one used. Catches a criterion changed after December was seen, which the
   partition record cannot see.
3. **`audit_access_since_declaration`**, read from `governance-guards` R-25's durable log. The
   join is stated rather than left as an outcome:
   `AccessRecord.retrieved_at_utc > TuningRecord.criterion_declared_at` **and**
   `AccessRecord.retrieved_at_utc < TuningRecord.run_at`, restricted to `purpose` in
   **`"coverage_audit"`** or **`"regime_audit"`** — the two performance-blind December
   literals. **`"locked_evaluation"` is included rather than filtered**: it is the G-06 event
   and cannot legitimately precede a tuning run at all, so an access carrying it inside the
   window **is itself a finding**.

> ### Requirement (Q2 = B) — the window BLOCKS, it does not merely flag
>
> A tuning run falling inside that window **does not proceed** until a human **attests, on
> the record**, that no December figure informed the criterion. The attestation is dated and
> names the person.
>
> **What this is worth, stated without inflation.** A self-attestation about one's own
> knowledge **proves nothing on its own**. What it buys is a **dated, named record that a
> specific person considered the question at the time** — worth more than a flag read weeks
> later at G-05, because the person still remembers what they knew.
>
> **The residual no mechanism closes.** *"A choice informed by a December figure a human
> carries in their head leaves no trace in any of the three."* Mechanism 3 makes the overlap
> **visible**; it does not eliminate it, **and no mechanism can**. **No artifact may describe
> December-blindness in tuning as fully enforced.**
>
> **The sequence is not forbidden.** The pre-G-05 December coverage and regime audit is
> **required** and its timing is **not this unit's to control**. Forbidding a tuning run from
> post-dating an audit access would set one mandatory obligation against another with no rule
> to resolve them.

**Requirement (R-93, Vision §8.6, TE §13.5).** The seed is **never selected** — not on
validation, not after seeing December. Seeds are fixed in `seeds.yaml`: development **42**,
final **{1337, 2024, 7}**, bootstrap **20221201**. **D-122's own status travels with them** —
Vision §14.2 marks it *"Approved — supervisor sign-off pending"*, so the set is frozen for
implementation and **still owes a signature at G-05**.

**Requirement (R-96, W-6, TE §7.1).** Grid **content** is asserted, not only immutability:
**ridge 6, RF 18, LSTM 16** (D-121), and the **seven** fixed LSTM settings. The grid lives
**once**, in `experiment.yaml`; its **hash is committed before G-05**. A grid that is immutable
but wrong is immutably wrong, which is why content is asserted separately.

**Requirement (R-100, Vision §6.4).** **Random Forest importance is diagnostic and never a
selection input.** It may be saved as a non-authoritative figure; it may never add, remove or
rank a feature into the production set.

## SEC-M-02 — The confirmatory prediction, and what may not stand in for it

**Requirement (R-91, W-3, NFR-DET-01).** The confirmatory prediction is the **three-seed
element-wise mean**, and **nothing may be substituted for it** — not a single seed, not a
best-of-three, not a median.

**Requirement (R-92).** A confirmatory mean **whose inputs disagree on provenance fails**. A
mean over three predictions from different feature sets, partitions or transform IDs is not
the confirmatory prediction; it is a number that looks like one.

**Requirement (R-94, W-4).** M-06 restores its **lowest-validation-RMSE checkpoint**, not its
last epoch. Last-epoch restore silently substitutes a different model for the selected one.

**Requirement (R-101).** Selection is on **mean per-fold skill score**, and **the refit changes
no hyperparameter**. A refit that re-tunes is a second selection with no record.

**Requirement (R-90, W-1).** A frame whose spec is not `(partition k, role "score")`
**never reaches** partition *k*'s scoring path. The stamp match runs **before every** scoring
path, not once at entry.

## SEC-M-03 — The model set is closed, and two absences are evidence

**Requirement (R-102, TE §8.2, §8.3).** The model set is **closed**: M-01 persistence, M-02
24-hour seasonal persistence, M-03 fitted station×month×hour climatology, M-04 Ridge, M-05
Random Forest, M-06 compact LSTM. **B-01 (IRI) and C-01 (CODE GIM) are generated, not
trained** — a benchmark table and a comparator table, never models in the ladder.

**Requirement — two absences are evidence, not omissions.** **GRU** is removed with the gate
closed, and **residual modules** (IRI-residual RF, IRI-residual LSTM) are removed. TA-08 and
TA-12 require **grep evidence that they are absent from the codebase** — an absence that is
tested rather than assumed. **SSN** is likewise absent as a feature.

**Requirement.** **PyTorch is prohibited** in the governed pipeline; TensorFlow/Keras is the
one forecasting stack for both phases.

**Requirement (R-98, W-9, NFR-LEAK-01).** M-03's climatology is fitted on **training
partitions only**. A climatology fitted on everything is a leak wearing the clothes of a
baseline.

**Requirement (Vision §2.4).** The three mandatory difficulty controls — persistence, 24-hour
seasonal persistence, fitted climatology — are **co-reported in the same primary results table**
as the LSTM-vs-IRI comparison, **never relegated to an appendix**; and **any baseline that
beats the LSTM on the locked test is disclosed** in that table and in the abstract-level
conclusion. **This unit produces those controls; `regimes-diagnostics-reporting` owns the
table**, and this artifact states the obligation rather than claiming to discharge it.

## SEC-M-04 — The locked-test write happens once, and the receipt precedes any metric

**Requirement (R-102a, W-12, NFR-AUD-01).** *(NFR-AUD-01 cited 2026-09-01 — every requirement in
this section is an instance of it, and the section named only this unit's own rules. Its
governing form: **registry writes are atomic or append-safe; a failed or aborted run stays
visible with its status and reason; a silent re-run is prohibited; no entry is deleted or
overwritten.** Acceptance rows **TA-10, TA-21** — both, and both owned elsewhere; nothing here
discharges either.)* `scripts/06_train_and_predict.py` **writes the prediction-hash
receipt** — `prediction_path`, `sha256`, `recorded_at_utc`, `run_id`, `partition_id`, durably
flushed — and **refuses to exit holding a `DEC` prediction with no receipt**.

**Requirement.** Locked-test predictions are generated and written **exactly once**, after
**G-05 is signed**, and **hashed before any metric is computed**. Every `DEC` metric entry
point **refuses without a verified receipt** — the design is **fail-closed** while the
producing half is unbuilt.

**Requirement.** Every locked-test access records **`locked_test_accessed = true`**. Any
test-driven change made to the pipeline **after** locked-test access is labelled
**exploratory**.

**Carried — the receipt's destination is `foundation`'s.** W-6 step 4 of `foundation` designs
the registry row as the receipt's destination and **refuses a hash presented by the
metric-computing process**. This is the **two-half contract** registered as a BLK-08-pattern
exit condition for both owners, and **this unit does not declare it satisfied from one side**.

## SEC-M-05 — Determinism, CPU, and the ablations that are predeclared

**Requirement (NFR-DET-01, TE §9.3/§13.5).** Python, NumPy, scikit-learn and TensorFlow seeds
are set through **one tested utility** using `tf.keras.utils.set_random_seed`, with
`tf.config.experimental.enable_op_determinism()` enabled where supported. **Nondeterministic
operations are recorded** where determinism cannot be guaranteed, and **an empty
`nondeterministic_ops` is never proof of determinism**.

**Requirement (TE §9.2, TC-01).** The full workflow runs on **CPU as a complete execution
path**. **GPU may be an optional accelerator only, never a dependency of any result.** M-06 is
the largest compute in the project and **no runtime has been measured** — nothing has been
trained.

**Requirement (R-97, W-7, TE §7.2).** Ablations are **predeclared as named runs in
`experiment.yaml` with run IDs**, executed on the **frozen January–November folds** with
identical folds, masks and tuning budget. **Five are named; four are reachable in Phase 1.**
**`ABL-DIFF` inverse-transforms to absolute TECU before any metric**, and **`ABL-HIST48` runs
only after the primary configuration is frozen**. **No ablation is invented after results are
seen.**

**Requirement (R-99, W-8).** The **+24 h horizon needs no code change** — it is
structurally config-only, so producing it cannot become an occasion to alter the model.

---

## SEC-M-06 — Seven requirements have no acceptance row, and all seven get controls

**Requirement (Q1 = A).** Each of the **seven** requirements carrying no §16 or §19 row gets a
**negative control proving the violation is caught**, required by the affirmed
every-hard-rule-gets-a-test practice **independently of §19**:

| Requirement | Rule | Negative control |
|---|---|---|
| **FR-P1-04-14** | R-101 — selection on mean per-fold skill; refit preserves hyperparameters | A refit that changes a hyperparameter **fails** |
| **FR-P1-05-3** | R-100 — RF importance never a selection input | An importance score used to add or drop a feature **fails** |
| **FR-P1-05-4** | R-95 — tuning reads Jan–Nov only | A December partition in `partitions_read` **fails**; a criterion hash mismatch **fails**; an audit access inside the window **blocks** — ⚠ **this third clause is UNRUNNABLE today**: it reads `governance-guards` R-25's durable log, and **BLK-07 is open** so that log does not exist |
| **FR-P1-05-5** | R-96 — grid content and immutability | A grid whose content differs from D-121's counts **fails**; a changed grid hash **fails** |
| **FR-P1-05-6** | R-97 — ablations predeclared | An ablation absent from `experiment.yaml` **fails**; `ABL-HIST48` before the primary freeze **fails** |
| **FR-P1-05-21** | R-98 — M-03 fitted on training partitions only | A climatology fitted on the full dataset **fails** |
| **FR-P1-05-22** | R-99 — +24 h horizon config-only | A horizon change requiring a code edit **fails** |

**Requirement.** **All seven missing acceptance rows are proposed to the gate as one Vision
§15.2 request**, because they are **one gap rather than seven**. **This stage proposes; it does
not approve.** D-32's approval of eight rows in a single decision is cited as precedent for the
**route**, not as approval of these.

**Why this stage does not simply record the gap.** Several of the seven are rules `project.md`
lists under `## Forbidden` or `## Mandated`. Leaving them with neither a test nor a route to a
row is the posture `GOV-2026-08-15-FE-01` finding `GOV-F-06` warned against, and the same
question one unit earlier was answered by requiring the control and proposing the row —
answering it differently here because the number is larger would make the rule depend on how
expensive it is to follow.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| **FR-P1-04-14** | SEC-M-02, SEC-M-06 | ⚠ **NO ROW** — proposed | control required |
| FR-P1-05-1 | SEC-M-03 | WS-14, TA-12, TA-26 | `Pending` |
| FR-P1-05-2 | SEC-M-02 | WS-15, TA-13 | `Pending` |
| **FR-P1-05-3** | SEC-M-01, SEC-M-06 | ⚠ **NO ROW** — proposed | control required |
| **FR-P1-05-4** | SEC-M-01, SEC-M-06 | ⚠ **NO ROW** — proposed; `requirements.md` records that **no existing row tests its actual trigger** | control required |
| **FR-P1-05-5** | SEC-M-01, SEC-M-06 | ⚠ **NO ROW** — proposed | control required |
| **FR-P1-05-6** | SEC-M-05, SEC-M-06 | ⚠ **NO ROW** — proposed | control required |
| **FR-P1-05-21** | SEC-M-03, SEC-M-06 | ⚠ **NO ROW** — proposed | control required |
| **FR-P1-05-22** | SEC-M-05, SEC-M-06 | ⚠ **NO ROW** — proposed | control required |
| NFR-DET-01 | SEC-M-02, SEC-M-05 | WS-17 (supporting), TA-13 | `Pending` |
| NFR-LEAK-01 | SEC-M-03 | TA-11 | `Pending` |
| NFR-IRI-01 | SEC-M-03 | WS-10, TA-07 | `Pending` — **test written, UNEXECUTED** |
| **NFR-AUD-01** | SEC-M-04 | **TA-10, TA-21** — both rows, owned elsewhere | `Pending` |

**Derived and printed**: 6 requirement sections (SEC-M-01…SEC-M-06); **13** coverage rows *(count
re-derived 2026-09-01 on adversarial finding 1, Major; superseded figure preserved: **12**)* — the
9 requirements the `functional-design` map carries, plus NFR-DET-01, NFR-LEAK-01, NFR-IRI-01 and
**NFR-AUD-01**, which this artifact states obligations against; **7** with **no acceptance row**
— **re-derived by counting `⚠ NO ROW` cells in the table above, not read off the map** (the
clause *"matching the map exactly"* is withdrawn: on two other units this stage that same clause
made a count right only by coincidence); **0** rows claimed satisfied.

**The seven NFR IDs this unit does not cite, stated rather than left as a silent gap** *(added
2026-09-01 on the same finding — the reviewer's point was not only that NFR-AUD-01 was missing
but that no exclusion rationale existed for the set)*. Of `requirements.md`'s eleven NFR IDs,
four are cited here and `NFR-PHASE-01` in `tech-stack-decisions.md`. The remaining six are
**out of this unit's scope by substance, not by oversight**: `NFR-DQ-01` (target quality and
missingness — `target-standardization`'s), `NFR-FAIR-01` (the comparison-wide mask —
`evaluation-and-comparison`'s; this unit trains, it does not compare), `NFR-REP-01`
(reproducibility of the clean run — `fixtures-and-reproducibility`'s; **NFR-DET-01 is this
unit's determinism obligation and is cited**), `NFR-SEC-01` (credentials — this unit reads no
credential), `NFR-TDEF-01` (identity stamps on datasets and masks — this unit consumes them and
produces neither), and `NFR-LIC-01` (third-party reuse — **no model or baseline here is copied
or materially adapted from a third-party source**; if one ever is, the §10.1 register entry is
required **before the code is used**, and this row would move into scope).

## Assumptions & Open Questions

- **[Q1]** Seven negative controls are **required**; seven acceptance rows are **proposed, not approved**. The proposal is **one §15.2 request**, and this stage has **no authority to approve it**.
- **[Q2]** The December-window **block** is new at this stage; `functional-design` states a flag. **The attestation proves nothing on its own** — it is a dated record that someone considered the question, and **the residual it addresses cannot be closed by any mechanism**.
- **[assumption]** `governance-guards` R-25's log will be readable by a tuning run at the moment it needs to block. **Mechanism 3 is a cross-unit read**, and R-25's log does not exist — **BLK-07 is open** and `open_restricted` is unbuilt. The block is therefore **specified and unrunnable today**, exactly as R-95's three mechanisms already are.
- **[assumption]** An attestation can be captured in `TuningRecord`. Where it lives and what form it takes is **owed at 3.5**; nothing here designs the field.
- **Carried — the prediction-hash receipt is a two-half contract** with `foundation`, and **this unit does not declare it satisfied from one side**.
- **Carried — the primary results table is `regimes-diagnostics-reporting`'s.** This unit produces the three difficulty controls and states the co-reporting and disclosure obligations; it does not discharge them.
- **Carried — `PartitionError` is declared in `src/data/config.py`**, not `src/models/`. This unit is the **semantic owner but not the declaration site**.
- **Carried — D-122's seed set owes a supervisor signature at G-05.**
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-31T23:55:46Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Minor | § SEC-M-06 table, row FR-P1-05-4 | The table's third clause ("an audit access inside the window **blocks**") is presented alongside two implementable checks with no inline caveat, even though `## Assumptions & Open Questions` (same file) and `tech-stack-decisions.md`'s `[Q2 / cross-unit]` entry both state this mechanism reads `governance-guards` R-25's log, which does not exist (BLK-07 open), so it is unrunnable today. A reader who stops at the table sees three equally-actionable checks. | Add a one-clause parenthetical to that table cell ("blocked by BLK-07 until R-25's log exists") so the caveat travels with the claim, not only with the assumptions list. |
| 2 | Minor | § SEC-M-01 mechanism 3 / Assumptions | The cross-unit read dependency on `governance-guards` R-25 (BLK-07) could not be independently verified — `governance-guards` construction artifacts are outside this unit's read-scope pass-list, and no shared inception contract in the exempt set pins R-25's existence or shape. The claim is internally consistent across both primary artifacts and `functional-design/business-rules.md` (spot-checked), so this is a coverage limit on this review, not a contradiction found. | None — flag for the gate that BLK-07's resolution is the one external precondition this unit's Q2=B block depends on. |

### Validation Tool Results

No validation tooling is declared for `nfr-requirements` in `.claude/aidlc-common/stages/construction/nfr-requirements.md`. Verification below is manual, derivation-based per the dispatch brief's Focus items.

**Requirement-coverage completeness (Focus 1).** Read `inception/requirements-analysis/requirements.md` for the nine cited IDs and derived their acceptance-row status directly from the table rows (offsets 383–415):

| ID | requirements.md row | Row present? |
|---|---|---|
| FR-P1-04-14 | `UNTESTED` — no WS/TA row | NO ROW |
| FR-P1-05-1 | WS-14, TA-12, TA-26 | has row |
| FR-P1-05-2 | WS-15, TA-13 | has row |
| FR-P1-05-3 | `UNTESTED` | NO ROW |
| FR-P1-05-4 | `UNTESTED` — WS-18 tests the wrong trigger | NO ROW |
| FR-P1-05-5 | `UNTESTED` | NO ROW |
| FR-P1-05-6 | `UNTESTED` | NO ROW |
| FR-P1-05-21 | `UNTESTED` | NO ROW |
| FR-P1-05-22 | `UNTESTED` | NO ROW |

9 requirements, 7 with no row — matches `functional-design`'s printed derivation and this artifact's own claim, ID for ID. NFR-DET-01 (WS-17, TA-13), NFR-LEAK-01 (WS-11, TA-08, TA-11) and NFR-IRI-01 (WS-10, TA-07) all carry rows in `requirements.md` (offsets 482, 483, 486) and are correctly marked `Pending` rather than `NO ROW` in this artifact's coverage table. 9 + 3 = 12 rows, matching the printed "12 coverage rows." `tech-stack-decisions.md`'s 6 rows are exactly the subset that raises a technology choice (FR-P1-05-1, -2, -5, -6, -22, NFR-DET-01) — set-differenced against the 12 by hand, no discrepancy.

**Block vs. flag (Focus 2).** § SEC-M-01's blockquote states "the window BLOCKS, it does not merely flag" and `## Assumptions & Open Questions` [Q2] states the block is new at this stage against `functional-design`'s flag — plainly stated, not presented as pre-existing. The admission "a self-attestation... proves nothing on its own" sits in the **rule body** (the Q2=B blockquote inside § SEC-M-01), not only in Assumptions — confirmed by direct reading. The BLK-07/R-25 dependency is stated as an open assumption in both primary artifacts (see Finding 2) — nothing elsewhere in the read set implies the mechanism works today.

**Seven controls (Focus 3).** All seven rows in § SEC-M-06 test a mechanically checkable condition (a hash mismatch, a set-membership check, a partition-fit assertion, a config-vs-code check) rather than a vacuous always-pass condition. None invents a dependency that cannot exist even in principle; the one control resting on an unbuilt cross-unit artifact (FR-P1-05-4's third clause) is flagged only at Finding 1's granularity, not a structural impossibility.

**Unfrozen pin (Focus 4).** Re-read `tech-stack-decisions.md` in full: no TensorFlow version, switch value, or grid number beyond D-121's ridge 6 / RF 18 / LSTM 16 is asserted as a decision — 2.21.0 appears once, explicitly attributed to "TE §8.1's candidate," not adopted. D-122's seeds (42; 1337, 2024, 7; 20221201) are stated with the carried status "Approved — supervisor sign-off pending" in both files (security-requirements.md line 95, tech-stack-decisions.md via requirements.md cross-reference) — correctly not claimed as fully signed.

**No claims of discharge (Focus 5).** Scanned both files for "trained," "passes," "satisfied," "discharged" — every occurrence is negated or hedged (e.g., "no model has ever been trained," "0 rows claimed satisfied," "this unit does not declare it satisfied from one side"). `PartitionError`'s ownership split (semantic owner in `src/models`, declared in `src/data/config.py`) is stated as a carried assumption, consistent with the dispatch brief.

**Counts (Focus 6).** `security-requirements.md`: 6 sections (SEC-M-01…SEC-M-06), 12 coverage rows, 7 with no row — all verified above. `tech-stack-decisions.md`: 6 sections (TS-M-01…TS-M-06), 6 coverage rows — verified above; "0 new dependencies" holds (only the already-governed `tensorflow`/`scikit-learn`/`numpy`/`pandas`/`pyarrow` stack is used); "1 TBD" (the TensorFlow pin) is the only `TBD — freeze gate` value named.

### Summary

Both artifacts hold up under an adversarial pass: the nine-requirement/seven-no-row derivation matches `requirements.md` ID for ID, the December-window block is plainly marked new (not pre-existing) with its own limits stated in the rule body rather than buried in Assumptions, no scientific value or unfrozen pin is filled by convenience, and no claim of satisfaction, discharge, or training appears anywhere. The two Minor findings are a documentation-placement gap (the BLK-07 caveat should travel with its specific table cell) and an acknowledged coverage limit of this review (the R-25/BLK-07 claim itself is outside this unit's read-scope and taken as consistently stated rather than independently confirmed). Neither blocks readiness.

READY

## Review — 2026-09-01 confirming pass

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 1 (fresh budget after human gate rejection)

### Verification of the four-site NFR-PHASE-01 repair

All four sites confirmed directly in `tech-stack-decisions.md`:

1. **§ Sources** — `NFR-PHASE-01` present with the dated note ("cited 2026-09-01 on a pre-dispatch self-sweep...").
2. **§ TS-M-04 rule body** — the "Serialization is a phase-transition asset" paragraph leads `(NFR-PHASE-01, TE §7.0B, TA-27)` and states both halves: no Phase 1 fitted weights carried forward, and no Phase 1 result may motivate a Phase 2 model/evaluation change.
3. **§ Requirement coverage** — row `NFR-PHASE-01 | TS-M-04 | TA-27 — row owned by governance-guards | Pending` present.
4. **Printed count** — `security-requirements.md` recounted directly: 9 FR rows (FR-P1-04-14; FR-P1-05-1,2,3,4,5,6,21,22) + 3 NFR rows (NFR-DET-01, NFR-LEAK-01, NFR-IRI-01) = **12**, matches. `tech-stack-decisions.md` recounted: FR-P1-05-1,2,5,6,22 + NFR-DET-01 + NFR-PHASE-01 = **7**, matches. 12 − 7 = **5**, and the text correctly reads "five fewer" with "six fewer" preserved as a parenthetical superseded figure — no stale bare "6"/"six fewer" found outside that one parenthetical.

`requirements.md` line 490 confirms `NFR-PHASE-01 | Phase-boundary integrity | test_phase_boundary.py plus the transition-manifest hash-diff test both pass | TA-27` — TA-27 is genuinely NFR-PHASE-01's row, cited correctly as owned by `governance-guards`.

### Full-ID-space sweep (the check that has found a defect on all twelve units)

`requirements.md` carries exactly eleven NFR IDs (grep-derived, printed): `NFR-AUD-01, NFR-DET-01, NFR-DQ-01, NFR-FAIR-01, NFR-IRI-01, NFR-LEAK-01, NFR-LIC-01, NFR-PHASE-01, NFR-REP-01, NFR-SEC-01, NFR-TDEF-01`. Across both artifacts combined, only **four** are cited: `NFR-DET-01`, `NFR-IRI-01`, `NFR-LEAK-01` (security-requirements.md), `NFR-PHASE-01` (tech-stack-decisions.md, post-repair). The remaining seven — `NFR-AUD-01, NFR-DQ-01, NFR-FAIR-01, NFR-LIC-01, NFR-REP-01, NFR-SEC-01, NFR-TDEF-01` — appear nowhere in either artifact, and neither artifact states a deliberate-exclusion rationale for the gap as a set (each cited NFR is individually justified; the uncited six/seven are not addressed at all).

Of these, `NFR-AUD-01` is the one whose **substance** the artifacts rest on without citing: § SEC-M-04 requires the prediction-hash receipt to be "durably flushed," requires `06_train_and_predict.py` to "refuse to exit holding a `DEC` prediction with no receipt," and states "every locked-test access records `locked_test_accessed = true`" and "any test-driven change made after locked-test access is labelled exploratory" — this is exactly NFR-AUD-01's substance (atomic/append-safe registry writes; failed/aborted runs stay visible; no silent reruns), yet NFR-AUD-01 is cited nowhere in either file. `NFR-DQ-01`, `NFR-FAIR-01`, `NFR-LIC-01`, `NFR-REP-01`, `NFR-SEC-01` and `NFR-TDEF-01` were checked against both artifacts' text and, unlike NFR-AUD-01, none has a clear resting-substance without citation on this pass — the FR-P1-05-* range (all 22 IDs enumerated via `requirements.md`) is fully covered by the two artifacts' citations against the nine already claimed.

### Other checks

- **Q1/Q2 answers**: confirmed A and B respectively in `nfr-requirements-questions.md`, consistent with both artifacts' § Sources citation.
- **Seven ⚠ NO ROW entries**: confirmed genuinely `UNTESTED` in `requirements.md` for all seven (FR-P1-04-14, FR-P1-05-3, -4, -5, -6, -21, -22), each carrying "candidate new TA row via Vision §15.2" or equivalent proposed (not assumed) language — matches SEC-M-06's table exactly.
- **Determinism, December-blindness, ablations, no-discharge claims**: re-checked against the artifact text; consistent with the prior 2026-08-31 pass's findings, no regression introduced by the repair.
- Previous pass's two Minor findings (BLK-07 caveat placement; R-25 cross-unit coverage limit) remain unaddressed by this repair (out of its scope) and still stand as Minor, non-blocking.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | Both artifacts, § Sources / no equivalent section | `NFR-AUD-01`'s substance (durable receipt flush, refuse-to-exit-without-receipt, `locked_test_accessed` flag, exploratory-labelling after access) is rested on in § SEC-M-04 without citing `NFR-AUD-01` anywhere in either artifact, and none of the seven uncited NFR IDs (`NFR-AUD-01, NFR-DQ-01, NFR-FAIR-01, NFR-LIC-01, NFR-REP-01, NFR-SEC-01, NFR-TDEF-01`) carries a stated deliberate-exclusion rationale as a set. | Cite `NFR-AUD-01` at § SEC-M-04 alongside R-102a/W-12, and add one line noting the other six NFRs are out of this unit's scope (or citing them where their substance is in fact rested on), so the gap in the eleven-ID space is stated rather than silent. |
| 2 (carried) | Minor | § SEC-M-06 table, row FR-P1-05-4 | Unresolved from the 2026-08-31 pass — the BLK-07 caveat on the third clause is stated only in Assumptions, not inline in the table cell. |
| 3 (carried) | Minor | § SEC-M-01 / Assumptions | Unresolved from the 2026-08-31 pass — the R-25/BLK-07 cross-unit dependency remains outside this unit's read-scope and unverifiable independently; coverage limit, not a contradiction. |

### Verdict rationale

One Major and two carried Minor findings — at the ≤2-Major / no-Critical threshold, this does not cross into NOT-READY. The repair itself is verified accurate at all four claimed sites, the printed counts recount correctly, and TA-27 is confirmed as NFR-PHASE-01's row. The Major finding is new evidence from this pass's full-ID-space sweep (not part of the repair under verification) and should be closed at the next revision rather than block this gate.

READY
