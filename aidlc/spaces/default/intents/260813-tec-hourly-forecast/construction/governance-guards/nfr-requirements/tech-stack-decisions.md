# Tech Stack Decisions — `governance-guards`

**Unit** `governance-guards` (Bolt 2) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ THIS UNIT ADDS NO DEPENDENCY, AND CLAIMS NOTHING INSTALLED
>
> The governed stack is fixed by **TE §8**, transcribed in full at
> `../../foundation/nfr-requirements/tech-stack-decisions.md`. **This unit adds nothing to
> it.** Every mechanism it needs — AST walking, hashing, file traversal — is Python
> standard library.
>
> **Nothing is claimed installed or executed.** No Python interpreter exists in this
> environment; `src/data/locked_test.py` and `open_restricted` **do not exist**; **WS-18
> and TA-18 are undischarged**; TA-27 and TA-28 are `Pending`; **G-09 is signed (D-31) with
> its §18.3 preconditions UNMET**; stage 3.1 remains **FAIL**; **BLK-07 is open**.

## Sources

- `../../foundation/nfr-requirements/tech-stack-decisions.md` — the governed stack, its prohibitions, the platform rules, and the `TBD — freeze gate` TensorFlow pin. **Not restated here; referenced.**
- `../functional-design/business-rules.md` — **R-24** (Q7 = D: the `ast` scan is the early-warning limb, run-time assertions authoritative, both run), **R-25**, **R-27** (per-class walk; unparseable file is a failure), **R-28**, **R-29**.
- `../functional-design/business-logic-model.md` — **W-2a** (the existing static scan and its declared subordinate role), **W-3**…**W-3c** (protected-item digests; the six hashable-representation kinds; field- and parameter-hash contracts), **W-5**, **W-6**, **W-10**, **W-11**.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§8** (approved stack), **§7.0**/**§7.0B**, **§10.1**, **§12**, **§13**.
- `nfr-requirements-questions.md` — Q2 = B and the receipted Consolidated Summary Confirmation.

---

## TS-G-01 — No new dependency, and that is a decision

**Decision.** This unit introduces **no package** beyond TE §8.1's approved set. Its three
mechanisms are all standard library:

| Mechanism | Implementation | Why not a package |
|---|---|---|
| Static source analysis | **`ast`** (stdlib) | `tests/test_phase_boundary.py` already walks `src/` and `scripts/` with `ast` across 266 lines. A linter plugin or a third-party AST tool would add a dependency to the **one unit whose job is to constrain what the codebase contains** — and would itself need a §10.1 reuse-register entry. |
| Digests | **`hashlib`** (stdlib) | TE §8.1 lists `hashlib` as required for acquisition/audit code; the protected-item digests are the same primitive. |
| Tree traversal, file reads | **`pathlib`**, stdlib IO | `pathlib` is `team.md`'s affirmed path convention. |
| Test harness | **`pytest`** | Already required by TE §8.1. |

**Why this is worth stating rather than assuming.** A guard that depends on a third-party
scanner inherits that scanner's supply chain, its version drift across the two platforms,
and a §10.1 register obligation — **inside the unit that exists to make the boundary
checkable**. Keeping it stdlib keeps the guard auditable by reading it.

## TS-G-02 — The static check is AST-based with constant folding

**Decision (Q2 = B).** The restricted-root check is implemented over the **`ast`** parse
tree, folding **constant** string expressions, so a literal split across a concatenation or
an `os.path.join` of literal parts is caught.

**Scope of what folding buys, stated exactly.** Caught: `"locked_test" + "_restricted"`,
`os.path.join("evidence", "locked_test_restricted")`, an f-string of literal parts.
**Not caught:** a value read from `configs/`, an environment variable, a name computed from
a run-time expression. **The residual is real and is not claimed closed.**

**The hierarchy is unchanged (R-24, Q7 = D).** The static scan is the **early-warning**
limb; the **run-time assertions are authoritative**; **both run**. A static scan of a local
checkout constrains nothing about a Kaggle session, which is why it cannot be the only limb.

**Fail-closed (R-27).** The guard walks **every** file, dispatched per artifact class, and
an **unparseable file is a failure**, never a skip.

**The check is code and needs its own test.** Adopting an AST check adds a component that
can itself be wrong — a folding bug produces a false clean. Its negative controls are the
project's standard pattern: a module holding the literal must **fail** the check, and a
module holding it via each folded form must **also** fail.

## TS-G-03 — Digest technique for protected items

**Decision, transcribed from `functional-design`, not taken here.** Protected-item digests
are **canonical, not byte-literal** (R-18) — a re-serialisation that changes whitespace or
key order must not change a hash, or the G-P3C comparison reports drift that did not
happen. The **six hashable-representation kinds** and which items use each are fixed at
W-3a; the field-hash and parameter-hash contracts at W-3b and W-3c.

**The protected-set list is excluded from every item's section hash, and that exclusion is
bounded to exactly one member** (R-19 of this unit) — a self-referential list would
otherwise change every hash whenever the list changed.

**An empty diff is not yet proof** (R-22). `diff_protected_hashes` returning nothing is
evidence only if the manifest it compared against was itself complete — **a freeze-mode
manifest raises on any absent item; a draft records it** (R-21).

**Status.** All `Pending`; TA-28 covers `diff_protected_hashes` and the G-P3C pass
condition, and is unexecuted.

## TS-G-04 — Platform posture

Unchanged from `foundation`: **exactly two platforms**, Kaggle and local; **CPU is a
complete execution path**; **the in-Kaggle obligation is a condition on the session, not a
Bolt number** — any Bolt performing a governed run inside a Kaggle session must first
evidence that the required critical tests and applicable fixtures passed **inside that same
session**.

**Consequence specific to this unit.** The static limb runs wherever the checkout is; **the
run-time limb is the only one that says anything about a Kaggle session**, which is R-24's
stated reason for making it the authoritative one. A guard evidenced only locally has not
been evidenced for the platform that performs the governed runs.

**What Bolt 2 builds, and what it must not** (W-11) is unchanged by G-09's signature in
substance: no scientific value becomes fillable, and TE §18.3's stop-and-report obligation
survives its own gate.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| REQ-ENG-5 | TS-G-02 | WS-10, TA-07, TA-08, TA-12, TA-27 | `Pending` |
| FR-P1-03-2 | TS-G-02, TS-G-04 | TA-27 | `Pending` |
| FR-P1-06-1 | TS-G-03 | TA-27 | `Pending` |
| FR-P1-06-2 | TS-G-03 | TA-27 | `Pending` |
| FR-P1-06-3 | TS-G-03 | TA-28 | `Pending` |
| FR-P1-06-4 | TS-G-03 | TA-28 | `Pending` |
| NFR-PHASE-01 | TS-G-02, TS-G-04 | TA-27 | `Pending` |
| NFR-LIC-01 | TS-G-01 (no dependency to register), SEC-G-06 | TA-28 | `Pending` |

**Derived and printed**: 4 decision sections (TS-G-01…TS-G-04); 8 coverage rows — **three fewer**
than `security-requirements.md`'s **eleven** *(dependent figure re-derived 2026-09-01 in the same
sweep as that file's coverage correction; superseded: "two fewer than ten")*, because
**FR-P1-02-6**, **FR-P1-05-12** and **NFR-AUD-01** raise no technology choice — NFR-AUD-01's
append-safe registry write is `foundation`'s stack decision, not one taken here; **0** rows claimed satisfied; **0** new dependencies; **0** values left
`TBD — freeze gate` by this unit (the one open pin is `foundation`'s TensorFlow row).

## Assumptions & Open Questions

- **[Q2]** Constant folding is required; the **dynamic-path residual is not closed**.
- **[assumption]** `ast` on the pinned Python 3.11 is sufficient for the folding described. Python's `ast` exposes constant folding only for literal expressions, so a `join` whose arguments are literals is foldable while one taking a variable is not. If a needed form turns out not to be foldable with stdlib alone, that is a **new dependency question** and returns here rather than being solved by adding a package at 3.5.
- **[assumption]** The static check covers **Python source**. Whether it must also cover notebooks, YAML configs or Markdown is raised at `security-requirements.md` § Assumptions and **not resolved**.
- **Carried, not decided here.** `foundation`'s **TensorFlow pin** stays `TBD — freeze gate`; the **`IntegrityError` module home** is the owner's; **BLK-07 is open**.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row, install or test as discharged.
