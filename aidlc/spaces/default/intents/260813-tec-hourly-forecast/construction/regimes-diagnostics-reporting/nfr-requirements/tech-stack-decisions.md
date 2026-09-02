# Tech Stack Decisions — `regimes-diagnostics-reporting`

**Unit** `regimes-diagnostics-reporting` (Bolt 11) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NO NEW DEPENDENCY, AND TWO REFUSALS WITH NOTHING TO REFUSE YET
>
> The governed stack is fixed by **TE §8** and transcribed at
> `../../foundation/nfr-requirements/tech-stack-decisions.md`. This unit adds **none**.
>
> **§ SEC-R-02's two consumer refusals have no producing half.** Neither
> `evaluation-and-comparison`'s orientation/weighting fields nor `target-standardization`'s
> caveat field exists, so **both refusals will fail on every input until those land** — correct
> fail-closed behaviour that will look like breakage.
>
> **Five acceptance rows are `Pending`** (approved under **D-32**, never run, NOT passed) and
> **four requirements are rowless** — the map's **FR-P1-05-14** and **FR-P1-05-15**, plus
> **FR-P1-05-3** and **FR-P1-05-21** added to the coverage tables on the iteration-1 Majors
> *(corrected 2026-09-01 in the same sweep; superseded: "two requirements are genuinely
> rowless")*. TA-16, TA-19, TA-20 and WS-19 are undischarged.
> **G-09** is signed (D-31) with preconditions UNMET; stage 3.1 remains **FAIL**; `configs/`
> does not exist; no Python interpreter exists here, and **no results table has ever been
> produced**.

## Sources

- `../../foundation/nfr-requirements/tech-stack-decisions.md` — the governed stack and the platform rules. Referenced, not restated.
- `../functional-design/business-rules.md` — **R-123**, **R-125**, **R-126**, **R-127**, **R-129**, **R-130**, **R-131**, **R-132**.
- `../functional-design/business-logic-model.md` — **W-1** (the classifier), **W-3** (the results table as a producing path), **W-4** (the checklist's presence checks), **W-5** (the breakdown family), **W-7** (`plots.py`), **W-9** (the four notebooks).
- `../../evaluation-and-comparison/nfr-requirements/security-requirements.md` § SEC-C-02 and `../../target-standardization/nfr-requirements/security-requirements.md` § SEC-T-02 — the two producing halves § SEC-R-02 consumes.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§8.1** (`matplotlib` required, `seaborn` preferred; `pandas`, `pyarrow`, `pyyaml`, `pytest` required), **§12** (the five notebooks; `NN_topic.ipynb`), **§14** (notebook obligations), **§15.2**, **§18.2**.
- `../../../../../../../../PreFlight/vision_document(3)(2)(2).md` — **§2.4**, **§6.4**, **§6.6**.
- `nfr-requirements-questions.md` — Q1 = A, Q2 = A, and the receipted Consolidated Summary Confirmation.

---

## TS-R-01 — The results table is code, not a document

**Decision (R-125, W-3).** The primary results table is produced by a **function** —
`pandas` assembling checked fields, `pyarrow` storing the result — **not** hand-assembled in a
notebook or a document. **No reporting, templating or table-formatting package is added.**

**Why this is a security decision and not a style one.** § SEC-R-02's two refusals and
§ SEC-R-01's `beats_model` disclosure **only exist if the table is a code path**. A table
transcribed by hand into a document has **no place to put a refusal** — the disclosure would
depend on the person transcribing, which is exactly the failure mode Vision §2.4's binding
honesty rule is written against.

**The refusals belong at the rendering boundary**, so that a value lacking its orientation,
weighting or lineage caveat **cannot be rendered at all** rather than being rendered and
flagged. **Where that boundary sits in the rendering path is owed at 3.5** — no rendering path
exists.

**Consequence stated:** because both producing halves are unbuilt, **the refusals will fail on
every input**. That is the mechanism working, not a defect, and it is recorded here so the first
failure is read correctly.

## TS-R-02 — Figures are presentation-only, and that is enforced by signature

**Decision (R-129, W-7).** `plots.py` uses **`matplotlib`** (TE §8.1, required) with
**`seaborn`** preferred for diagnostics, and is **presentation-only by signature** — it
**cannot compute a reported quantity**. Its **manifest is WS-19's evidence**.

**Why signature rather than convention.** A plotting module that accepts raw inputs will
eventually compute a mean, a rate or a difference "just for the figure", and that number then
differs from the table's. **Constraining the signature makes the second computation
unrepresentable** rather than discouraged.

**Figures regenerate from stored results**, never by recomputation — so a figure **cannot
silently differ from the table it illustrates**.

**No plotting-adjacent statistics.** `seaborn` will fit and draw a regression or a confidence
band from raw data as a side effect of plotting. **Those are computed quantities**, and any that
reached a figure would bypass every check § SEC-R-01 places on the table.

> ### ⚠ WHAT "BY SIGNATURE" ACTUALLY GUARANTEES — read this with the decision, not after it
>
> *(Moved into the decision body 2026-09-01 on adversarial finding 3, Major. It was stated only
> in `## Assumptions` while this section asserted "unrepresentable rather than discouraged" and
> "no plotting-adjacent statistics" as flat fact — the rule-body-versus-Assumptions misplacement
> `project.md` records as recurring, and which this stage has now committed three times.)*
>
> **A signature constrains what a function is GIVEN. It does not constrain what the function
> DOES with it.** `plots.py` receiving only stored results cannot recompute a reported
> quantity from raw data — that much the signature genuinely makes unrepresentable. But
> nothing in a signature stops the module **calling `seaborn.regplot` on the values it was
> handed** and drawing a fitted line that is itself a computed quantity.
>
> **So the guarantee is split, and only half is mechanical:** the *input* restriction is
> enforced by signature; the *no-derived-statistics* rule **rests on review**. That is a
> weaker guarantee than "unrepresentable" suggests, and it is stated here rather than left to
> a reader to discover in the Assumptions.

## TS-R-03 — One classifier, one counting path, thresholds from config

**Decision (R-123, W-1).** The regime classifier is **one implementation** reading **configured
thresholds** from `configs/`, with **one counting path**. **`pandas`** performs the counting;
**no classification or binning package is added.**

**Thresholds are scientific values.** They live in config per TC-03e, **not in source**, and
**none is named here**. A regime boundary changes which hours count as storm-time, which changes
a reported regime count.

**Why one counting path is a stack decision.** Two counting implementations — one for the
audit, one for the report — can disagree, and **the one used in the report is the one nobody
re-derives**. A single path makes the December-blind guard in § SEC-R-04 meaningful: guarding
two paths requires guarding both.

## TS-R-04 — The claims checklist inspects locations, and the citation check extends it

**Decision (R-126, W-4).** The claims-and-limitations checklist performs **presence checks at
named locations**, implemented with stdlib text handling — **no document-parsing or NLP package
is added**.

**Decision (Q2 = A).** The check **extends to citation**: a thesis-level location citing a
**quarantined diagnostic** must carry its **non-authoritative label alongside the citation**.

**What the tooling can and cannot do, stated at the decision.** A stdlib text check can verify
that a **named artifact and its label co-occur** at an inspected location. It **cannot**
determine that a sentence is *about* a figure it does not name. **An indirectly phrased citation
evades it**, and **no available tooling would close that** — an NLP dependency would trade a
checkable mechanism for a probabilistic one and would still be evadable. **The gap is narrowed,
not closed**, and adding a package here would only make it look closed.

**Which locations count as thesis-level is not fixed anywhere.** R-126 inspects *named*
locations, so a location added later is **not automatically inspected**. **Raised, not
resolved.**

## TS-R-05 — Notebooks import from `src/`, and hold no only-copy

**Decision (R-131, W-9, REQ-ENG-12, TE §12/§14).** The four analysis notebooks —
`01_data_and_target_audit`, `02_processor_verification`, `03_features_and_splits_review`,
`04_results_and_figures` — follow `NN_topic.ipynb`, **import from `src/`**, **read versioned
artifacts**, and **begin with the dataset version, code commit, configuration IDs and artifact
IDs they expect** through **one declaration helper**.

**None holds the only copy** of parsing, calibration, feature, split, training, evaluation or
bootstrap logic (TE §14). **Stop semantics:** *"Run all"* either **succeeds from declared
inputs or stops with a clear missing-artifact or Internet-access message** — never proceeding on
partial state.

**The acquisition notebook is deliberately excluded** from the import-from-`src/` and
no-only-copy rules and is governed by **REQ-ENG-13** instead. Stated because the two notebook
regimes are easy to conflate, and this unit touches both.

**No notebook-execution or parameterisation package is added.** The declaration helper is
project code in `src/`, which is what keeps the notebooks from holding logic.

## TS-R-06 — Platform posture

Unchanged from `foundation`: **exactly two platforms**; **CPU is a complete execution path**;
artifacts move between platforms **with a SHA-256 manifest** and the transfer is recorded.

**Specific to this unit.** Reporting is CPU-bound and light. **The output of this unit is what
reaches the thesis**, so an artifact produced on one platform and reported from another must
**carry its manifest** — a figure or table whose provenance is lost between platforms is a
reported number with no chain back to the run that produced it.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| REQ-ENG-12 | TS-R-05 | **TA-16 (primary)** | `Pending` |
| FR-P1-05-9 | TS-R-01 | **TA-20 (primary)** | `Pending` |
| FR-P1-05-11 | TS-R-02 | **WS-19 (primary)** | `Pending` |
| **FR-P1-05-19** | TS-R-04 | ⚠ **`Pending`** — approved under D-32, never run, NOT passed | not evidence |
| **FR-P1-05-20** | TS-R-01 | ⚠ **`Pending`** — approved under D-32, never run, NOT passed | not evidence |
| **REQ-CLAIM-01** | TS-R-04 | ⚠ **`Pending`** — `TST-CLAIMS-01` approved under D-32, never run | not evidence |
| REQ-ENG-13 | TS-R-05 | TA-16 | `Pending` |
| NFR-TDEF-01 | TS-R-01 | — | `Pending` |

**Derived and printed**: 6 decision sections (TS-R-01…TS-R-06); **8** coverage rows — **eleven
fewer** than `security-requirements.md`'s **nineteen** *(dependent figure corrected 2026-09-01 in the same sweep; superseded: "nine fewer than seventeen")*, because FR-P1-05-10, FR-P1-05-14,
FR-P1-05-15, FR-P1-05-16, FR-P1-05-18, FR-P1-03-4, REQ-ENG-4, REQ-ENG-8 and NFR-DQ-01 raise
**no technology choice** in this unit; **0** rows claimed satisfied; **0** new dependencies;
**0** values left `TBD — freeze gate` by this unit (the regime thresholds are config-resident
scientific values owned upstream, and **none is named here**).

## Assumptions & Open Questions

- **[Q1 / TS-R-01]** The two consumer refusals **have no producing half**. Both **fail on every input until those land**, and **where the refusal sits in the rendering path is owed at 3.5** — no rendering path exists.
- **[Q2 / TS-R-04]** The citation check is a **stdlib text check**. It can verify a named artifact and its label **co-occur**; it **cannot** tell that a sentence is about a figure it does not name. **No package would close that**, and adding one would make the gap look closed rather than make it smaller.
- **[TS-R-04]** **Which locations count as thesis-level is not fixed anywhere.** A location added later is not automatically inspected. **Raised, not resolved.**
- **[assumption]** `seaborn`'s statistical drawing functions can be kept out of the figure path by convention plus signature. **A signature constrains inputs, not which library calls a module makes** — so this rests partly on review rather than wholly on mechanism, and that is a weaker guarantee than TS-R-02's framing might suggest.
- **[TS-R-03]** The regime thresholds are **scientific values in config**, owned upstream. **None is named here.**
- **Carried — `foundation`'s TensorFlow pin stays `TBD — freeze gate`.** This unit trains nothing.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row, install or test as discharged.
