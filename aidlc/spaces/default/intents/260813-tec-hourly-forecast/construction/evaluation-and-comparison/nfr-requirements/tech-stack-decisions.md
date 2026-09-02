# Tech Stack Decisions — `evaluation-and-comparison`

**Unit** `evaluation-and-comparison` (Bolt 9) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NO NEW DEPENDENCY; TWO MECHANISMS THAT CANNOT RUN YET
>
> The governed stack is fixed by **TE §8** and transcribed at
> `../../foundation/nfr-requirements/tech-stack-decisions.md`. This unit adds **none**.
>
> **The mask-ordering refusal is unrunnable** — **BLK-07 is open** and `open_restricted` does
> not exist. **The G-06 hash-receipt refusal is fail-closed but unexercised** — its producing
> half is `models-and-baselines`' and is unbuilt.
>
> **FR-P1-05-7's row is `Pending`** (approved under D-32, never run, NOT passed);
> **FR-P1-05-17 and FR-P1-05-20 have no row** *(corrected 2026-09-01 in the same sweep)*. WS-16 and TA-11 are undischarged. **G-09** is signed (D-31) with
> preconditions UNMET; stage 3.1 remains **FAIL**; `configs/` does not exist; no Python
> interpreter exists here, and **no metric has ever been computed**.

## Sources

- `../../foundation/nfr-requirements/tech-stack-decisions.md` — the governed stack and the platform rules. Referenced, not restated.
- `../functional-design/business-rules.md` — **R-104**, **R-106**, **R-107**, **R-108**, **R-109**, **R-110**, **R-111**, **R-112**.
- `../functional-design/business-logic-model.md` — **W-1** (mask construction and registration), **W-2** (the ordered estimand pipeline), **W-5** (the G-06 path), **W-6** (the honesty mechanics), **W-7** (what `07` orchestrates and what it must not).
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§1.3** (the estimand), **§8.1** (`numpy`, `pandas`, `pyarrow`, `scikit-learn` for metrics, `matplotlib`, `pytest` — all required), **§13.6** (the vector time-block bootstrap, **`statistical-inference`'s**), **§18.2**.
- `evidence/DECISIONS.md` — **D-28** (2–31 December, 30 days), **D-32**.
- `nfr-requirements-questions.md` — Q1 = A, Q2 = C, and the receipted Consolidated Summary Confirmation.

---

## TS-C-01 — Metrics use the approved stack, and one library default is a hazard

**Decision.** Metric computation uses **`numpy`** for the paired differences and
**`scikit-learn`** for standard metrics where they apply (TE §8.1, both required), with
**`pandas`** for the per-station tabulation and **`pyarrow`** for stored results. **No metrics
or statistics package is added.**

**The hazard, named because it is a one-line mistake.** Every common metrics library computes
**model error**, not **benchmark minus model**. The estimand's orientation is a **project
convention layered on top of** whatever a library returns, so the sign is introduced by
**project code** at a single point — which is exactly why § SEC-C-02 requires both a
reversed-sign control on that code and carried orientation fields on its output.

**Equal-station weighting is likewise project logic.** A library aggregate over pooled rows is
**row-weighted**, not station-weighted, and the two differ whenever stations contribute unequal
row counts — which they do: ARUC, BSHM and NICO have different coverage. **Using a default
aggregate would silently substitute a different estimand.**

## TS-C-02 — The bootstrap is not this unit's, and this unit must not reimplement it

**Decision.** The **vector time-block bootstrap** — 24-hour blocks carrying **all three
stations together**, **10,000** replicates, seed **20221201**, 95% CI, with the cross-station
paired-error correlation reported — is **`statistical-inference`'s** (TE §13.6). **This unit
consumes its result and does not reimplement it.**

**Stated because reimplementation is the likely failure.** A metrics module that needs a
confidence interval will reach for `scipy.stats` or a resampling helper, and **a within-station
or naive bootstrap produces systematically narrower intervals** — a `project.md` **NEVER**. The
within-station 2,000-replicate variant was **rejected at Q-27**. **No bootstrap is implemented
here.**

## TS-C-03 — The mask is one stored artifact, and its identity is a hash

**Decision (R-107, W-1).** The comparison-wide mask is **computed once, stored once, and
referenced by a stable ID** — not recomputed per comparison. Storage is **`pyarrow`/Parquet**
with the mask manifest recording the ID and **reported row counts**.

**Why identity is a hash, not a name.** A mask referenced by filename can be replaced with a
different mask under the same name; a mask referenced by content hash cannot. R-107's
once-only registration is what makes the hash meaningful — a second registration **fails**
rather than silently versioning.

**The ordering check reads two timestamps** (§ SEC-C-01). **Where the mask registry's
timestamp is read from, and by what, is owed at 3.5**, and the check is **unrunnable while
BLK-07 is open**.

> **A constraint on that check, stated rather than assumed away.** The registration timestamp
> and the access timestamp are in the **same clock domain only if written by the same host**.
> **On Kaggle they may not be**, and **Kaggle's durability semantics are unmeasured**. An
> ordering comparison across two clocks with no stated skew bound is weaker than it looks —
> **raised here, not resolved**, and it bears directly on whether § SEC-C-01's refusal means
> what it says.

## TS-C-04 — Figures are reproducible, and the caveat is emitted with them

**Decision.** Figures use **`matplotlib`** (TE §8.1, required) with **`seaborn`** preferred for
diagnostics. Figures are **reproducible from stored results** — regenerating a figure re-reads
the stored metric artifact rather than recomputing metrics, so a figure cannot silently differ
from the table it illustrates.

**The caveat is emitted by the producing path** (R-110), not attached by an author. That makes
it a property of the artifact rather than of someone's diligence — the same reasoning
`target-standardization` applies to its lineage caveat, and the reason VAL-05's Phase 2
disclosure being **absent from every stage artifact** when checked is treated as evidence
rather than an anecdote.

**No reporting or templating package is added.** The primary results table is
`regimes-diagnostics-reporting`'s; this unit emits values, the trigger field and the caveat.

## TS-C-05 — Platform posture

Unchanged from `foundation`: **exactly two platforms**; **CPU is a complete execution path**;
artifacts move between platforms **with a SHA-256 manifest** and the transfer is recorded.

**Specific to this unit.** Evaluation is CPU-bound tabular work. **The G-06 evaluation is a
governed run**, so if it executes inside a Kaggle session the **in-Kaggle obligation binds**:
the required critical tests and applicable fixtures must have passed **inside that same
session**, because a Kaggle session carries no git working tree and a local suite run proves
nothing about the environment the one-shot evaluation actually ran in. **G-06 is the run where
that matters most** — it happens once.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| FR-P1-04-7 | TS-C-03 | WS-16, TA-11 | `Pending` |
| **FR-P1-05-7** | TS-C-01, TS-C-02 | ⚠ **`Pending`** — approved under D-32, **never run, NOT passed** | not evidence |
| **FR-P1-05-17** | TS-C-03 | ⚠ **NO ROW** | not evidence |
| NFR-FAIR-01 | TS-C-01, TS-C-03 | WS-16, TA-11 | `Pending` |

**Derived and printed**: 5 decision sections (TS-C-01…TS-C-05); **4** coverage rows — **four**
fewer than `security-requirements.md`'s **eight** *(corrected 2026-09-01 on adversarial finding 2, Major; superseded: "five". This dependent figure was left behind when the source count moved 5 → 7 → 8 — the exact defect `project.md` `delivery-planning:dp-1` records, and one the reviewer had been briefed to check)*, because NFR-IRI-01, FR-P1-05-9, FR-P1-05-12 and FR-P1-05-20 raise **no technology
choice** in this unit; **0** rows claimed satisfied; **0** new dependencies; **0** values left
`TBD — freeze gate` by this unit; **2** mechanisms recorded as **specified and unrunnable
today** (the mask-ordering refusal, blocked by BLK-07; the hash-receipt refusal, whose
producing half is unbuilt).

## Assumptions & Open Questions

- **[TS-C-01]** The estimand's **orientation and equal-station weighting are project logic**, not library defaults. A library aggregate would be **row-weighted** and would silently substitute a different estimand.
- **[TS-C-02]** **No bootstrap is implemented here.** If a metrics path appears to need an interval, that is a signal to consume `statistical-inference`'s result — **not** to reach for `scipy.stats`, which would produce the narrower intervals `project.md` forbids.
- **[TS-C-03 / Q1]** The ordering check compares **two timestamps that may be written by different hosts**. **No skew bound is stated anywhere**, and Kaggle's durability semantics are unmeasured. This **weakens § SEC-C-01's refusal** and is raised rather than resolved.
- **[assumption]** A mask stored as one Parquet artifact is what every comparison actually reads. Nothing prevents a caller **recomputing** an intersection inline and using that; the once-only registration catches a second *registration*, not a second *computation*. **The check that would catch it is `tests/test_common_masks.py`'s**, and it is unwritten.
- **Carried — the prediction-hash receipt** is a two-half contract with `models-and-baselines`; **enforced here, produced there, satisfied by neither alone**.
- **Carried — BLK-08's half A/half B** split with `features-and-splits`, narrowed to `ABL-DIFF`.
- **Carried — `foundation`'s TensorFlow pin stays `TBD — freeze gate`.** This unit trains nothing.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row, install or test as discharged.
