# NFR Design Questions — `statistical-inference`

**Unit** `statistical-inference` (Bolt 10) · **Kind** `library` · **Stage** `nfr-design`

Construction-stage questions are exceptional. The scientific opens (interval method,
block-resampling scheme, correlation series, §15.3 replicate-count classification) are
already **proposed and routed to gates** — §18.2 bars this stage from touching them, and
no question below re-asks one. Two genuine engineering-design gaps remain. Per
`produces_kinds`, this `library` unit gets `security-design.md` and `logical-components.md`.

## Question 1

WS-17's evidence is the **replicate hash**: a same-seed rerun must produce the identical
hash (§13.7 exact equality), on either governed platform. `nfr-requirements` pins the
generator (PCG64) and records seed key, generator identity and hash in `BootstrapResult` —
but never says **what bytes the hash covers**. A hash over floats is only
platform-independent if the serialisation is canonical. What does the replicate hash hash?

A) The replicate vector's raw IEEE-754 bytes, with the canonical form pinned: dtype
   `float64`, little-endian, C-order, replicate order = draw order — and those four facts
   recorded in `BootstrapResult` beside the hash, like the generator identity.
   > **Impact**: Exact, cheap (one `tobytes()` pass), and deterministic on every CPU platform the project allows — §13.7's exact-equality class for deterministic CPU transforms is satisfiable byte-for-byte. The pinned facts travel with the evidence, so a future dtype drift is detectable rather than silent. Engineering contract, no scientific value touched.

B) A canonical decimal serialisation (e.g. repr at fixed precision, newline-joined) hashed
   as text.
   > **Impact**: Human-inspectable but slower, and it introduces a precision constant (how many digits) that is a new invented number — the exact thing this unit's posture avoids. Round-trip at any finite precision can collide distinct replicate sets.

C) Defer the hash's byte definition to code-generation (3.5).
   > **Impact**: WS-17's central evidence artifact would get its definition chosen by an implementer without a design stage behind it; two platforms could plausibly write different canonical forms before anyone notices, which is precisely the reproducibility failure the pin exists to prevent.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it is the only form that is simultaneously exact (§13.7), constant-free, and self-describing (the four pinned facts ride in `BootstrapResult`). B invents a precision constant; C defers the one definition WS-17's evidence cannot do without.

[Answer]: A

## Question 2

W-1 re-asserts every metric-entry-point precondition inside `vector_block_bootstrap`
(registered mask, stamps, DEC receipt, target space) rather than trusting `07`'s call
order. `evaluation-and-comparison`'s NFR design just placed all five refusal checks in
**one guard module** in `src/evaluation` (its SD-C-01, Q2 = C there), with per-entry
negative controls. This unit's bootstrap lives in the same `src/evaluation` package
(R-112 path grant). Where do this unit's precondition checks come from?

A) Import the shared guard module — `vector_block_bootstrap` calls the same
   `src/evaluation` guards `evaluation-and-comparison` designed (one copy of each check),
   and only the bootstrap-specific refusals (block-grid violation, missing-pair rule,
   unconfirmed interval method → `BootstrapError`) stay local to this unit. This unit's
   entry point joins the sibling's per-entry negative-control set: one control pushes each
   violating input through `vector_block_bootstrap` and asserts the raise.
   > **Impact**: One copy of each cross-cutting check — the R-105-vs-R-92 drift class has nothing to drift. Intra-package import, no new boundary crossed, consistent with R-114's single-copy principle (stated for the estimand, same reasoning). Cost: a cross-unit dependency on the sibling's guard module — a half-contract to state in both directions, and both units already share the package.
B) Local re-implementation — this unit writes its own precondition checks inside its two
   files, mirroring the sibling's semantics.
   > **Impact**: No cross-unit dependency, but a second copy of four checks whose taxonomy has already drifted once between units (LeakageError vs PartitionError, caught by the governance board). Two copies must now be corrected twice, forever.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — single-copy is this unit's own stated principle for the estimand (R-114: the copy inside the loop is the one nobody reads); the same argument covers guards. The dependency cost is small because both units already co-own the `src/evaluation` package by the approved path grant.

[Answer]: A

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
