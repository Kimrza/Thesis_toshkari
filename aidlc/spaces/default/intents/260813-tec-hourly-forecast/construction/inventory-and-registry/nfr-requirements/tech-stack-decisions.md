# Tech Stack Decisions — `inventory-and-registry`

**Unit** `inventory-and-registry` (Bolt 4) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NO NEW DEPENDENCY, AND NOTHING CLAIMED INSTALLED OR RUN
>
> The governed stack is fixed by **TE §8** and transcribed at
> `../../foundation/nfr-requirements/tech-stack-decisions.md`. This unit adds **none**.
>
> **One component is unfrozen and stays unfrozen**: the **IGRF version**, which R-45
> requires to be **pinned and never defaulted**. It is a scientific value, so **TE §18.2
> forbids this stage from choosing it**.
>
> **BLK-07 is open**, so the December audit cannot run. **WS-01, WS-18, TA-04, TA-18, TA-25,
> TA-32** and the §18.3 preflight are undischarged; **G-09** is signed (D-31) with
> preconditions UNMET; stage 3.1 remains **FAIL**; no Python interpreter exists here.

## Sources

- `../../foundation/nfr-requirements/tech-stack-decisions.md` — the governed stack, the platform rules, and the `TBD — freeze gate` TensorFlow pin. Referenced, not restated.
- `../functional-design/business-rules.md` — **R-44**, **R-45** (the pinned IGRF version), **R-47**, **R-48**, **R-49** (a governed schema; a self-contained report), **R-50**, **R-53**.
- `../functional-design/business-logic-model.md` — **W-1** … **W-9**, in particular **W-3** (why averaging becomes detectable), **W-4** (migrating the frozen literals), **W-5** (schema validation), **W-6** (the December audit).
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§5.1**, **§6.2**, **§8.1**, **§12** (the import-boundary rule; `pyyaml` for the four configs; `pandas` for manifests and registry), **§18.2**.
- `nfr-requirements-questions.md` — Q1 = A, Q2 = A, and the receipted Consolidated Summary Confirmation.

---

## TS-I-01 — The IGRF version is pinned, and this stage does not pin it

**R-45 requires the IGRF version to be pinned and never defaulted.** Geomagnetic
coordinates for ARUC, BSHM and NICO are computed with it, so the version **changes a
scientific quantity**.

**Decision: `TBD — freeze gate`.** TE §18.2 forbids an implementer or coding agent from
filling such a value by convenience, and TC-03e requires it to live in a governed config
(`configs/data.yaml`) rather than in source. **No version is named here**, and the sentinel
stays visible to the §18.3 zero-TBD preflight.

**What is decided is the failure mode, which is not a scientific value.** An **absent** IGRF
version **fails**; it does not fall back to a library default. This is the same shape as
R-35's rule that an absent `madrigalWeb_version` fails exactly as `"unknown"` fails — the
distinction that matters is between *no value* and *a value chosen for you*, and both are
refused.

**Consequence.** The station registry cannot be built until the version is frozen under a
D-number. That is a precondition, stated, not a blocker this stage may lift.

## TS-I-02 — The audit's import boundary is a placement constraint, not a package

**Decision (Q1 = A).** The December-audit code path may not import, directly or
transitively, any module under `src/models/` or `src/evaluation/`. **The mechanism is the
project's existing one** — TE §12's import-boundary rule, asserted the way **TA-07** asserts
the IRI boundary — implemented with stdlib **`ast`**, the same technique
`tests/test_phase_boundary.py` already runs across `src/` and `scripts/`.

**No dependency is added.** A third-party import-graph analyser would be a new package, a
§10.1 reuse-register entry, and a version to pin on two platforms, to check a property the
project already checks with stdlib elsewhere.

**Where the audit code lives becomes a decision.** The constraint binds a **code path**, so
that path needs a home that does not reach into `src/evaluation/`. TE §12's six `src/`
packages are `data`, `gnss`, `external`, `features`, `models`, `evaluation` — this unit's
work sits in `src/data/`, which crosses no boundary. **Naming the module is stage 3.5's**;
this artifact fixes only that it must not import across the two named packages.

**Transitive is the load-bearing word.** A direct import is easy to see; the failure that
matters is `src/data/audit.py` importing a helper that imports `src/evaluation/metrics.py`.
The check must follow the graph, not the file.

## TS-I-03 — Schema validation runs against a governed schema

**Requirement (R-49).** Validation runs against a **governed schema** — a versioned,
hash-recorded artifact — and the report is **self-contained**, readable without re-deriving
the schema it validated against.

**Stack.** `pyyaml` for the schema and the four governed configs; `pandas` for the tabular
comparison; stdlib `hashlib` for the schema hash; `pytest` for the checks. All TE §8.1
required components; **nothing added**.

**Not decided here.** *Which* schema language or shape the governed schema takes — a YAML
schema document, a `pandas` dtype contract, or a JSON Schema — is **owed at stage 3.5**. TE
§8.1 names no schema library, and adopting one (`jsonschema`, `pandera`) would be a **new
dependency** and returns here rather than being settled at 3.5.

## TS-I-04 — Registry and manifest formats

**Decision, transcribed.** `pandas` for the registry and manifests, `pyarrow` for Parquet
artifacts, `pyyaml` for the configs — TE §8.1, all required. The **experiment registry's
twenty-column §13.4 schema** and its append-safe write mechanism are **`foundation`'s**
(R-08, R-18), not this unit's; this unit's registry is the **station registry** (§6.2), a
different artifact with a different schema.

**Stated because the two are easy to conflate.** "Registry" in this unit's name means the
station registry. NFR-AUD-01's append-safety and no-silent-rerun rules bind the **experiment
registry**, which `foundation` owns — this unit's obligation under NFR-AUD-01 is the access
log its audit writes (SEC-I-02, SEC-I-03), not the experiment registry's write path.

## TS-I-05 — Platform posture

Unchanged from `foundation`: **exactly two platforms**; **CPU is a complete execution path**;
artifacts moving between platforms move **with a SHA-256 manifest** and the transfer is
recorded.

**Specific to this unit.** The December audit's access rows must be **durable before each
read**, and **Kaggle's durability semantics are unmeasured** (`foundation` W-6 step 8's
carried dependency). An audit run inside a Kaggle session therefore rests on an unmeasured
property for the guarantee that makes it auditable at all. That measurement is owed on
Bolt 1's in-Kaggle work, and it bears directly on whether this unit's audit can be evidenced
from a Kaggle session.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| FR-P1-02-1 | TS-I-01, TS-I-04 | WS-01, TA-04 | `Pending` |
| FR-P1-02-2 | TS-I-03 | TA-04 | `Pending` |
| FR-P1-02-3 | TS-I-02, TS-I-05 | WS-18, TA-25 | `Pending` — **cannot run, BLK-07** |
| **FR-P1-02-7** | TS-I-01 | ⚠ **NO ACCEPTANCE ROW** | untested |

**Derived and printed**: 5 decision sections (TS-I-01…TS-I-05); **4** coverage rows — five
fewer than `security-requirements.md`'s nine, because FR-P1-02-4, FR-P1-02-5, FR-P1-02-8,
NFR-AUD-01 and NFR-DQ-01 raise **no technology choice**; **0** rows claimed satisfied;
**0** new dependencies; **1** value left `TBD — freeze gate` by this unit (the IGRF
version); **1** choice explicitly deferred to 3.5 with a return condition (the governed
schema's form, which returns here if it needs a package).

## Assumptions & Open Questions

- **[TS-I-01]** The **IGRF version is a scientific value** and stays `TBD — freeze gate`. The station registry cannot be built until it is frozen under a D-number.
- **[Q1 / TS-I-02]** The import boundary is **new at this stage** and its exact expression is owed at 3.5. **The audit's module placement is constrained by it**, and if the audit needs something from `src/evaluation/`, that dependency must move or be duplicated.
- **[TS-I-03]** A schema **library** would be a new dependency and is **not adopted**. If 3.5 finds the governed schema needs one, that returns here rather than being settled there.
- **Carried — Kaggle's durability semantics are unmeasured**, and the audit's before-the-read log durability depends on them.
- **Carried — `foundation`'s TensorFlow pin stays `TBD — freeze gate`.** This unit has no NN dependency of its own.
- **Carried, and blocking — BLK-07 is open.**
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row, install or test as discharged.
