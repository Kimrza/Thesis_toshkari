# Tech Stack Decisions — `target-standardization`

**Unit** `target-standardization` (Bolt 6) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NO NEW DEPENDENCY; ONE FREEZE-GATE VALUE THIS STAGE MAY NOT SET
>
> The governed stack is fixed by **TE §8** and transcribed at
> `../../foundation/nfr-requirements/tech-stack-decisions.md`. This unit adds **none**.
>
> **The QC operation list stays `TBD — freeze gate`** — a scientific constant owed a
> **D-number**, and the reason FR-P1-03-1's closed-set criterion is **blocked**
> (§ SEC-T-01).
>
> **The `02` ordinal collision is a recorded §12 defect, not a resolved one**, and
> `code-generation` **must not invent a `02a`/`02b` convention**. `configs/` does not exist;
> no Python interpreter exists here; **G-09** is signed (D-31) with preconditions UNMET;
> stage 3.1 remains **FAIL**.

## Sources

- `../../foundation/nfr-requirements/tech-stack-decisions.md` — the governed stack, the platform rules, and the `TBD — freeze gate` TensorFlow pin. Referenced, not restated.
- `../functional-design/business-rules.md` — **R-64**, **R-65**, **R-66**, **R-69**, **R-70**, **R-73**.
- `../functional-design/business-logic-model.md` — **W-2** (the value-level diff and the "documented QC" gap), **W-3** (the D-17 field contract and its schema test), **W-6** (the `02` ordinal collision), **W-8** (the §12 module count, and a file that contradicts itself).
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§8.1** (`pandas`, `numpy`, `pyarrow`, `pyyaml`, `pytest` required), **§12** (the repository tree; the `NN_verb_noun.py` convention; `--config configs/` and `--phase 1|2`), **§13**, **§18.2–18.3**.
- `evidence/DECISIONS.md` — **D-1**, **D-16**, **D-17**, **D-19**.
- `nfr-requirements-questions.md` — Q1 = A, Q2 = A, and the receipted Consolidated Summary Confirmation.

---

## TS-T-01 — The QC list is config, and this stage does not fill it

**Decision (Q1 = A).** The QC operations are a **named list in `configs/data.yaml`**, per
TC-03e — no scientific constant lives in source or a notebook. **The list's contents stay
`TBD — freeze gate`.**

**Why the contents are a scientific value.** A QC operation **changes target values**. Which
operations are permitted is therefore a choice TE §18.2 places with the student and
supervisor, not with an implementer — *"No implementer or coding agent may fill such a value
by convenience."*

**What this stage decides, because it is structure and not value:**

- the list is **enumerated**, not an open category;
- an operation **outside** the list **fails** exactly as a fifth transformation would;
- the list is **read from config**, never inlined, so the §18.3 zero-TBD preflight can see
  the sentinel and the freeze is forced rather than forgotten.

**What it does not decide.** Which operations are on it, and with what parameters. **Stage
3.5 must stop and report** rather than choose.

## TS-T-02 — The diff and the schema check use the approved stack

**Decision.** The value-level diff (W-2) and the D-17 field-contract check (W-3) are built
from TE §8.1's required set — **`pandas`** for the tabular comparison, **`numpy`** for
numeric tolerance, **`pyyaml`** for the governed configs, **`pyarrow`** for Parquet
artifacts, **`pytest`** for the checks. **No diff, schema or data-validation package is
added.**

**Why no schema library.** `pandera`, `jsonschema` or an equivalent would be a **new
dependency**, a §10.1 reuse-register entry, and a version to pin on two platforms — to check
a **fixed set of sixteen fields** against a contract that is already written down. If 3.5
finds the field contract genuinely needs one, that is a **new dependency question and returns
here** rather than being settled there.

**The diff must be value-level, not schema-level.** FR-P1-03-1's criterion is about
**values** — what changed between the provider bytes and the standardized product — so a
check that only compares column names and dtypes does not meet it. Stated because the two are
easy to conflate and the cheaper one looks like progress.

**Floating-point tolerance is a declared value, not an implementation default.** A diff over
aggregated values needs a tolerance, and a tolerance chosen by whatever `numpy.isclose`
defaults to is a scientific value filled by convenience. It belongs with the fixture
manifest's *"permitted floating-point tolerances"* (TE §15.2) and is **not set here**.

## TS-T-03 — The caveat field travels in the artifact format

**Decision (Q2 = A).** The label and lineage caveat are carried **in the artifact itself**,
alongside `target_definition_id` — in the Parquet schema's metadata or as a column, whichever
survives the round-trip that `pyarrow` performs.

**A real constraint, stated rather than assumed.** Parquet key-value metadata survives a
`pyarrow` round-trip but is **easy to drop** through an intermediate `pandas` operation that
rebuilds the frame. If the caveat is metadata rather than a column, the requirement in
§ SEC-T-02 — that a consumer reporting a comparison without it **fails** — is doing more work
than the format guarantees. **Whether it is a column or metadata is owed at 3.5**, with the
constraint that whichever is chosen must **survive the pipeline's actual operations**, not
merely a direct read-back.

**No serialization format is added.** `pyarrow`/Parquet is TE §8.1's required artifact format.

## TS-T-04 — Script identity, and a §12 defect this stage does not paper over

**Decision, transcribed from §12 and R-73.** This unit's script is
`scripts/02_standardize_prepared_target.py`, taking `--config configs/` and `--phase 1|2`.

**The collision is recorded, not fixed.** `scripts/02_build_vtec_target.py` (Phase 2) shares
the ordinal. The adopted reading is `unit-of-work.md` § 5's — *"the ordinal denotes the
pipeline position and `--phase` selects exactly one, so a clean run contains one `02` per
phase"* — and the clean-run contract **asserts exactly one `02` script per run**, which makes
that reading **falsifiable**.

**`code-generation` must not invent a `02a`/`02b` convention.** The ambiguity such a
convention would resolve is **already resolved by `--phase`**, and inventing one would be a
§12 amendment made by assertion.

**W-8's related finding stands.** The §12 module count and a file that contradicts itself are
recorded there; **nothing here resolves either**.

## TS-T-05 — Platform posture

Unchanged from `foundation`: **exactly two platforms**; **CPU is a complete execution path**;
artifacts move between platforms **with a SHA-256 manifest** and the transfer is recorded.

**Specific to this unit.** Standardization is CPU-bound tabular work with no accelerator
path, so the CPU-complete requirement costs nothing here. **The in-Kaggle obligation binds any
Bolt performing a governed run inside a Kaggle session** — a condition on the session, not a
Bolt number.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| FR-P1-03-1 | TS-T-01, TS-T-02 | — | ⛔ **BLOCKED** — QC list unfrozen |
| FR-P1-03-5 | TS-T-02 | — | `Pending` |
| NFR-TDEF-01 | TS-T-03 | — | `Pending` |
| FR-P1-03-2 | TS-T-04 | TA-27 | `Pending` — row owned by `governance-guards` |
| **FR-P1-03-3** | TS-T-03 | TA-15 | `Pending` — row owned elsewhere |
| **FR-P1-03-4** | TS-T-03 | TA-15 | `Pending` — row owned elsewhere |

**Derived and printed**: 5 decision sections (TS-T-01…TS-T-05); **6** coverage rows *(corrected 2026-08-31, same finding; superseded figure preserved: **4**)* — three
fewer than `security-requirements.md`'s nine, because NFR-DQ-01, NFR-LEAK-01 and
NFR-PHASE-01 raise **no technology choice**; **0** rows claimed satisfied; **0** new
dependencies; **2** values left unset by this stage (the **QC operation list**, a scientific
constant owed a D-number; and the **floating-point diff tolerance**, owed with the fixture
manifest); **1** choice deferred to 3.5 with a return condition (a schema library, which
returns here if the field contract needs one).

## Assumptions & Open Questions

- **[Q1 / TS-T-01]** The **QC list is a scientific constant** and is not filled here. FR-P1-03-1 is **blocked** until it is frozen under a D-number.
- **[TS-T-02]** The **floating-point diff tolerance** is a declared value, not a library default. It is **not set here** and belongs with the fixture manifest's permitted tolerances.
- **[Q2 / TS-T-03]** Whether the caveat is a **column or Parquet metadata** is owed at 3.5. **Metadata is easy to drop through an intermediate `pandas` rebuild**, so the format choice bears directly on whether § SEC-T-02's enforcement is real — this is a genuine risk to the requirement, not a formatting preference.
- **[assumption]** Sixteen fields can be contract-checked without a schema library. If 3.5 finds otherwise, the dependency question **returns here**.
- **Carried, not resolved — the `02` ordinal collision** and W-8's §12 module-count finding.
- **Carried — `foundation`'s TensorFlow pin stays `TBD — freeze gate`.** This unit has no NN dependency.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row, install or test as discharged.
