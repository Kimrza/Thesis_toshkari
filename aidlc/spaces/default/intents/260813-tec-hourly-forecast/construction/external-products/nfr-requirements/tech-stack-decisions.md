# Tech Stack Decisions — `external-products`

**Unit** `external-products` (Bolt 5) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NO NEW DEPENDENCY; TWO PINS THIS STAGE MAY NOT SET
>
> The governed stack is fixed by **TE §8** and transcribed at
> `../../foundation/nfr-requirements/tech-stack-decisions.md`. This unit adds **none**.
>
> **Two values stay `TBD — freeze gate`**: the **`iricore` pin with its switch set, topside
> option and the explicit 2000 km ceiling**, and the **CODE final GIM product version**.
> Both are scientific values under TE §18.2 — the IRI configuration *is* the benchmark, and
> the GIM issue *is* the comparator.
>
> **`src/external`'s contracts are an amendment owed** (R-55). **IRI generation is blocked**
> until R-59's validation passes, and it has not run. **G-09** is signed (D-31) with
> preconditions UNMET; stage 3.1 remains **FAIL**; no Python interpreter exists here.

## Sources

- `../../foundation/nfr-requirements/tech-stack-decisions.md` — the governed stack, its prohibitions and the platform rules. Referenced, not restated.
- `../functional-design/business-rules.md` — **R-55**, **R-56** (transitive allowlist; static check authoritative), **R-57**/**R-57a**, **R-58**, **R-59**, **R-60**, **R-61**, **R-62**, **R-63**.
- `../functional-design/business-logic-model.md` — **W-3** (enforcing the module-path import allowlist), **W-4**, **W-5**, **W-6**, **W-7**, **W-8** (the exit-code gap and its provenance-fields block).
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§5.2**, **§6.2**, **§8.1** (`iricore` required, **benchmark generation only**, with pinned implementation, switches, topside option and explicit 2000 km ceiling; `requests` where provider terms permit; stdlib for retrieval and hashing), **§8.2** (B-01 IRI via `src/external/iri.py`; C-01 CODE GIM via `src/external/gim.py` — both **generated, not trained**), **§8.3** (any IRI-derived ML feature or target **prohibited**), **§10**, **§12**.
- `nfr-requirements-questions.md` — Q1 = A, Q2 = A, and the receipted Consolidated Summary Confirmation.

---

## TS-E-01 — `iricore`, and the configuration that is the benchmark

| Component | TE §8.1 status | Use |
|---|---|---|
| `iricore` | **Required** | IRI-2016 **benchmark** generation only |

**Decision: the pin and its configuration are `TBD — freeze gate`.** TE §8.1 requires a
**pinned implementation, switches, topside option, explicit 2000 km ceiling, forecast-safe
drivers, and 5–10 validated samples**. None is named here.

**Why these are scientific values, not operational ones.** The IRI switch set and topside
option **change the benchmark's numbers**. The 2000 km ceiling is a physical modelling
choice. A comparison against a differently-configured IRI is a comparison against a different
benchmark — so choosing any of them by convenience is exactly what TE §18.2 forbids, and
TC-03e requires them in `configs/`, not in source.

**Decided here, because it is a mechanism and not a value.** On validation failure, IRI
generation is **blocked** and the implementation is **not silently switched** (R-59). A
switch made because the first implementation failed validation is a scientific change wearing
an operational disguise.

**B-01 is generated, not trained** (TE §8.2). IRI is a **benchmark table**, not a model in
the ladder — `iri_baseline.py` as a model module was deleted from v1.0, and IRI-residual RF
and IRI-residual LSTM are **removed**.

## TS-E-02 — CODE final GIM, and why its version is also a freeze-gate value

| Component | Status | Use |
|---|---|---|
| CODE final GIM | evaluation-time comparator (C-01, via `src/external/gim.py`) | **generated, not trained** — comparator table only |

**Decision: the product version/issue is `TBD — freeze gate`.** The GIM issue **is** the
comparator; a different issue is a different comparison. It is not named here.

**Decided here.** The reader for GIM/IONEX inputs uses TE §8.1's already-approved set —
stdlib for retrieval and hashing, `georinex` **conditional** for IONEX parsing or inspection
**cross-check only**. **No new parser is adopted**, and `georinex` is not treated as settled:
TE lists it as conditional.

**Independence is not a stack property.** The network-overlap audit and its
`gim_network_overlap_flag` are a **scientific** obligation (SEC-E-02), not a dependency
choice, and no tooling decision here bears on it.

## TS-E-03 — Enforcing the import allowlist with stdlib

**Decision.** The transitive import allowlist (R-56, W-3) is enforced with stdlib **`ast`**,
the same technique `tests/test_phase_boundary.py` already uses and the same one
`inventory-and-registry` adopts for its audit boundary. **No import-graph package is added.**

**Transitivity is what the check must implement.** A direct import of `src/external/iri.py`
from `src/features/` is easy to see; the failure that matters is a shim under a third package
that re-exports it. The check follows the **graph**, not the file — and R-56 makes the
**static** check authoritative for this unit, unlike `governance-guards` R-24 where run-time
is authoritative. **That difference is deliberate**: an import boundary is a property of the
module graph, which a static check reads directly, whereas a phase boundary is a property of
what actually executes.

**Dynamic imports are in scope.** `importlib.import_module`, `__import__`, and a computed
module path are each a stated evasion the check must catch, on the same list
`governance-guards` R-28 enumerates for the restricted-root literal.

**The limb the static check cannot reach** — the non-import data channel — is closed by
**SEC-E-01 limb 2**, a run-time content assertion at the feature-matrix boundary. That is a
**cross-unit contract**, not a tooling decision, and it adds no dependency either.

## TS-E-04 — Driver handling uses the approved data stack

**Decision.** `pandas` for the driver series and the hourly alignment, `numpy` for the
trailing-mean computation, `pyyaml` for the governed configs, stdlib `hashlib` for product
hashes, `pytest` for the controls. All TE §8.1 **required**; **nothing added**.

**One property the stack must not obscure.** R-57 requires the F10.7 81-day mean to be
**trailing, proven as a property**. `pandas` rolling windows default to a **trailing** window
but accept `center=True`, and a centered mean **uses future days** — TE §10 calls it *"a
defect, not a fallback"*. The requirement is therefore a property test over the computation,
**not** a code review of one call site: a test that shifts the input and asserts the output
shifts with it catches the centered variant regardless of which API produced it.

**Carry-forward is bounded in code, not by convention.** R-57a's ≤ 3 h then exclude has an
**injected four-hour gap** as its control.

## TS-E-05 — Platform posture

Unchanged from `foundation`: **exactly two platforms**; **CPU is a complete execution path**;
artifacts move between platforms **with a SHA-256 manifest** and the transfer is recorded.

**Specific to this unit.** IRI generation over a year of hourly epochs at three cells is the
largest compute this unit performs, and TE §9.2 requires it to complete **on CPU**. It is
**blocked** by R-59 regardless, so no runtime has been measured and none is claimed.

**Retrieval of external products** follows `acquisition`'s posture — provider terms bound the
rate, and **§ SEC-E-05's byte-identical-or-explicitly-divergent contract** governs a re-run.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| FR-P1-04-9 | TS-E-02 | WS-09, TA-12 | `Pending` |
| **FR-P1-04-15** | TS-E-01 | ⚠ **NO ACCEPTANCE ROW** | untested |
| FR-P1-04-17 | TS-E-04 | **TA-36** | ⚠ **`Pending` — not implemented, not executed, not passing** |
| FR-P1-04-3 | TS-E-04 | via R-57a's control | `Pending` |
| NFR-IRI-01 | TS-E-03 | WS-10, TA-07 | `Pending` — **test written, UNEXECUTED** |

**Derived and printed**: 5 decision sections (TS-E-01…TS-E-05); **5** coverage rows — **five fewer**
than `security-requirements.md`'s **ten** *(dependent figure re-derived 2026-09-01 in the same
sweep as that file's coverage correction; superseded: "four fewer than nine")*, because
REQ-ENG-9, FR-P1-04-4, FR-P1-04-18, **FR-P1-04-1** and NFR-LEAK-01 raise **no technology
choice** — FR-P1-04-1's allowlist is enforced by the same `ast` walk TS-E-03 already selects for
NFR-IRI-01, so it adds an obligation, not a technology; **0** rows claimed satisfied; **0** new
dependencies; **2** values left `TBD — freeze gate` (the `iricore` pin with its
configuration, and the CODE final GIM version); **1** component held **conditional**
(`georinex`, cross-check only).

## Assumptions & Open Questions

- **[TS-E-01, TS-E-02]** Both pins are **scientific values** and stay `TBD — freeze gate`. **No IRI benchmark and no GIM comparator can be produced until they are frozen under a D-number**, which is a precondition rather than a blocker this stage may lift.
- **[assumption]** `iricore` exposes the switches, topside option and altitude ceiling TE §8.1 names as configurable. If it does not, the pin question becomes an implementation-selection question and **returns here** rather than being resolved at 3.5.
- **[TS-E-03]** The static check is authoritative **for this unit** while run-time is authoritative for `governance-guards`. **The divergence is deliberate and stated**; anyone reading both units should not read it as an inconsistency.
- **[assumption]** A property test can prove the trailing mean. It proves the **window direction**, not that the underlying series was itself free of reanalysed values — **TE §10's never-backfill rule is a separate obligation** with separate evidence, and the property test does not discharge it.
- **Carried — `src/external`'s contracts are an amendment owed** (R-55).
- **Carried — `foundation`'s TensorFlow pin stays `TBD — freeze gate`.** This unit has no NN dependency.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row, install or test as discharged.
