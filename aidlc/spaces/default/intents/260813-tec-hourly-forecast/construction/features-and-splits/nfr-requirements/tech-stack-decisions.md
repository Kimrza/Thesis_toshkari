# Tech Stack Decisions — `features-and-splits`

**Unit** `features-and-splits` (Bolt 7) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NO NEW DEPENDENCY; ONE MECHANISM OWED BEFORE ITS CHECK CAN RUN
>
> The governed stack is fixed by **TE §8** and transcribed at
> `../../foundation/nfr-requirements/tech-stack-decisions.md`. This unit adds **none**.
>
> **The permitted-producer list per §6.2 dictionary row does not exist**, and § SEC-F-01's
> provenance check cannot run without it. That is a **named dependency**, not a claim.
>
> **TA-33 and TA-36 are `Pending`** — no test module implemented, none executed, none passed.
> **FR-P1-04-10's longitude limb has no acceptance row.** `configs/` does not exist; no
> Python interpreter exists here; **G-09** is signed (D-31) with preconditions UNMET; stage
> 3.1 remains **FAIL**.

## Sources

- `../../foundation/nfr-requirements/tech-stack-decisions.md` — the governed stack, the platform rules, and the `TBD — freeze gate` TensorFlow pin. Referenced, not restated.
- `../functional-design/business-rules.md` — **R-74**, **R-75**, **R-76**, **R-76a**, **R-77**, **R-79**, **R-80**, **R-81**, **R-83**.
- `../functional-design/business-logic-model.md` — **W-1** (the availability matrix), **W-2** (feature construction over a closed dictionary), **W-3** (the train-only fitting contract), **W-4** (one window definition, two representations), **W-5** (folds and embargo), **W-7** (IRI denial's two owners).
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§6.2**, **§7.1**, **§8.1** (`pandas`, `numpy`, `pyarrow`, `pyyaml`, `scikit-learn`, `pytest` required), **§12**, **§18.2–18.3**.
- `nfr-requirements-questions.md` — Q1 = A, Q2 = B, and the receipted Consolidated Summary Confirmation.

---

## TS-F-01 — Provenance stamps use the artifact format, not a new one

**Decision (Q1 = A).** Per-column provenance is carried **in the feature matrix's own
format** — Parquet field metadata or a companion manifest keyed by column, whichever survives
the pipeline's actual operations. **`pyarrow`/Parquet is TE §8.1's required artifact format**
and **no serialization or lineage package is added.**

**A real constraint, stated where the decision is made.** Parquet **field-level** metadata
survives a `pyarrow` round-trip but is **easy to drop** through an intermediate `pandas`
operation that rebuilds the frame — the same hazard `target-standardization` § TS-T-03
records for its caveat field. A provenance stamp that vanishes on a `DataFrame` rebuild
produces a matrix that **fails the check for the wrong reason**, or worse, one whose stamps
were silently regenerated as blank. **Whether stamps live in field metadata or a companion
manifest is owed at 3.5**, with the constraint that the choice must survive the operations
the pipeline actually performs, not merely a direct read-back.

**The permitted-producer list is a new artifact.** It maps each §6.2 dictionary row to the
producing artifact(s) permitted to supply it. It **does not exist**, it is **not created
here**, and § SEC-F-01's check cannot run until it does. **Whether it is a governed config
(`configs/features.yaml`) or a code constant is a TC-03e question** — if any entry encodes a
scientific choice it belongs in config; if it is purely a build-graph fact it need not be.
**Not decided here.**

## TS-F-02 — Train-only fitting is a check, and `scikit-learn` is where it would leak

**Decision.** Transform fitting uses **`scikit-learn`** (TE §8.1, required) for scaling and
preprocessing, with the **fit confined to the training partitions of the fold in question**.

**Why R-74 says "enforced by check rather than by shape".** The most natural
`scikit-learn` idiom — fit a scaler once, transform everything — **is** the leak. Nothing in
the API distinguishes a fold-correct fit from a full-dataset one; both are one line and the
wrong one is shorter. So the control cannot be "use the library correctly": it is a **check
that fails**, comparing what the transform was fitted on against the fold's declared training
bounds, which `Partition` states **on both sides** (R-83, BLK-09).

**The negative control that proves it.** Fit a transform on the full dataset and the check
must **raise**. A test that only confirms a correct fit passes proves nothing about the
mechanism.

## TS-F-03 — The window's two representations, built from one definition

**Decision (R-81, W-4).** The matrix and tensor representations are built from **one window
definition**, using `numpy` for the tensor construction and `pandas` for the matrix. **No
windowing or time-series package is added** — the window is 24 hours, a frozen constant, and
a library that offers configurable windowing invites the constant to become a parameter.

**The constant must not become a parameter.** `experiment.yaml`'s window length **equals 24
and appears in no grid** (R-76, Vision §8.1). Placing it in a grid **fails**. Stated here
because a dependency choice is exactly how such a constant would quietly become tunable.

**WS-13's evidence question stays open.** What evidence proves the two representations encode
the same window is **not settled**, and no tooling choice here settles it.

## TS-F-04 — Splits are computed, not stored, and the mask is one artifact

**Decision.** Fold boundaries and the 24-hour embargo are **computed from record timestamps**
with `pandas` datetime handling — never derived from a directory name or filename, and never
from a random splitter. **`scikit-learn`'s cross-validation splitters are not used**: they
default to shuffling, and TE §7.1 requires exact fixed calendar boundaries. Using one and
disabling the shuffle would leave the correct behaviour depending on a keyword argument.

**The comparison-wide mask is a single artifact.** Computed **once per comparison set** and
stored, not recomputed per comparison — NFR-FAIR-01/TC-16 require one mask, and a recomputed
mask is a mask that can differ.

## TS-F-05 — Platform posture

Unchanged from `foundation`: **exactly two platforms**; **CPU is a complete execution path**;
artifacts move between platforms **with a SHA-256 manifest** and the transfer is recorded.

**Specific to this unit.** Feature construction and split materialisation are CPU-bound
tabular work; no accelerator path exists, so CPU-completeness costs nothing here. **Per-column
provenance adds a resolution step per column per build** — the accepted cost of § SEC-F-01,
noted so it is not later mistaken for an unexplained slowdown.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| FR-P1-04-12 | TS-F-01, TS-F-03 | **TA-33** | ⚠ **`Pending` — nothing implemented or executed** |
| FR-P1-04-1 | TS-F-01 | WS-10, TA-07 | `Pending` |
| NFR-LEAK-01 | TS-F-02 | TA-11 | `Pending` |
| NFR-FAIR-01 | TS-F-04 | WS-16, TC-16 | `Pending` |
| **FR-P1-04-10** | TS-F-03 | ⚠ **NO ACCEPTANCE ROW** — proposed to the gate | untested |

**Derived and printed**: 5 decision sections (TS-F-01…TS-F-05); **5** coverage rows — **eight fewer**
than `security-requirements.md`'s **thirteen** *(dependent figure re-derived 2026-09-01;
superseded: "two fewer than seven". This phrase had been left stale through an **earlier**
correction that moved that file from 7 rows to 11 — it still read "seven" while the other file
read eleven, which is exactly the stale-dependent-figure defect this stage keeps producing, and
it survived a reviewer pass that reported no finding against it)*, because FR-P1-04-6,
FR-P1-04-7, FR-P1-04-13, FR-P1-04-16, FR-P1-04-17, NFR-IRI-01, **NFR-TDEF-01** and
**FR-P1-03-3** raise **no technology choice** beyond what TS-F-01 already states — the identity
stamps ride on the same `pyarrow` schema TS-F-01 selects, so they add an obligation, not a
technology; **0** rows claimed satisfied; **0**
new dependencies; **1** artifact named as **owed and non-existent** (the permitted-producer
list); **2** choices deferred to 3.5 with stated constraints (where provenance stamps live;
whether the producer list is config or code).

## Assumptions & Open Questions

- **[Q1 / TS-F-01]** The **permitted-producer list does not exist**. § SEC-F-01's provenance check **cannot run until it does**, and this stage does not create it.
- **[TS-F-01]** Whether the producer list is a **governed config or a code constant** is a **TC-03e question** turning on whether any entry encodes a scientific choice. **Not decided here.**
- **[TS-F-01]** Whether stamps live in **Parquet field metadata or a companion manifest** is owed at 3.5. **Field metadata is easy to drop through a `pandas` rebuild**, which would make § SEC-F-01's check fail for the wrong reason or pass on regenerated blanks — a genuine risk to the requirement, not a formatting preference.
- **[assumption]** `scikit-learn`'s transforms can be fitted per fold without a wrapper. If a wrapper turns out to be needed, it is **project code**, not a new dependency, and R-74's check-not-shape rule still governs it.
- **Open — WS-13's evidence question** (R-81, TS-F-03). No tooling choice settles it.
- **Carried — `foundation`'s TensorFlow pin stays `TBD — freeze gate`.** This unit builds inputs for the model; it does not construct one.
- **Carried, and owned elsewhere — what provenance is sufficient for the station registry.** Until decided, `station_lat` is blocked and `lst_sin`/`lst_cos` are excluded.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row, install or test as discharged.
