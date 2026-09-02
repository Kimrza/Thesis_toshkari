# NFR Requirements — Questions — `external-products`

**Unit** `external-products` (Bolt 5) · **Kind** `library` · **Stage** `nfr-requirements`

Two artifacts only — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit.

**Not re-asked, because `functional-design` already decided them.** The import allowlist
enforced **transitively**, with the **static check authoritative** (R-56, W-3); the F10.7
mean proven **trailing** as a property (R-57, W-4); the **≤3 h carry-forward then exclude**
rule with its injected-four-hour-gap control (R-57a); driver alignment's three limbs (R-58,
W-5); IRI generation **blocked** without a passing, complete, pre-declared validation (R-59,
W-6); the GIM comparator's four obligations, **one blocked** (R-60, W-7); a missing month
recorded and a hash mismatch terminating (R-61); Dst's three restrictions kept apart, with
eligibility a property of the data (R-62, W-9); driver series **time-indexed only** (R-63);
the story map governing this unit's coverage figures (R-54, R-54a, W-2, W-2a).

**Carried, not decided here.** `src/external`'s contracts are an **amendment owed** (R-55).
**REQ-ENG-9, FR-P1-04-4, FR-P1-04-15 and FR-P1-04-18 carry no acceptance row**; **TA-36
exists but is `Pending` — not implemented, not executed, not passing**.

---

## Question 1

R-56 makes the **static** import check authoritative for this unit — the opposite of
`governance-guards` R-24, where run-time assertions are authoritative and the static scan is
early warning. That difference is defensible: an import boundary is a property of the module
graph, and a static check reads the graph directly.

But `functional-design` discloses a residual the static check **cannot** see: a **non-import
data channel**. An IRI value written to a cached file by
`scripts/04_build_external_products.py` and read back by a feature builder that imports
nothing from `src/external/` passes every import check ever written, and NFR-IRI-01 is
breached with no mechanism firing.

This unit is where such a value would originate.

What should `security-requirements.md` require?

A. Add a **run-time content assertion** at the feature-matrix boundary — before any matrix reaches training or inference, assert no `iri_*` column, no IRI-derived residual and no IRI-computed value is present — as a second, independent limb alongside the authoritative static check
   > **Impact**: Closes the one NFR-IRI-01 path the import boundary structurally cannot reach, and gives WS-10's deliberate-injection test something to fire against on the data as well as the module graph. It puts an assertion at a boundary this unit does not own — the feature matrix is `features-and-splits`' — so it becomes a two-unit contract, and this stage can only state one half.

B. Keep the static check alone, with the non-import channel disclosed as a stated residual
   > **Impact**: No new cross-unit obligation, and the residual is already disclosed rather than hidden. It leaves the project's single most load-bearing scientific rule — that no IRI value reaches training — resting on a check that a file write and a file read walk straight past.

C. Require the run-time assertion inside this unit only, on what it writes rather than on what training reads
   > **Impact**: Stays wholly within this unit's ownership and needs no sibling's agreement. It asserts the wrong end: this unit is *supposed* to produce IRI values, so an assertion on its own outputs cannot distinguish a legitimate benchmark artifact from one about to be read by a feature builder.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — NFR-IRI-01 is the rule the whole comparison depends on, and the artifacts already admit the static check cannot see the channel that would breach it. The cross-unit cost is real and must be stated honestly: this stage can state only this unit's half, and `features-and-splits` owes the other half, in the same two-half pattern the project already uses for BLK-08. Option C asserts at the end that cannot tell violation from normal operation.

[Answer]: A

---

## Question 2

R-61 records a missing month and terminates on a hash mismatch. It does not say what happens
when a provider **revises** a product this unit has already downloaded — a re-issued CODE
final GIM day, or an `iricore` output that changes because a pinned input moved.

`acquisition` faced the same question for provider files and answered it: a re-run is
**byte-identical or explicitly divergent** — recompute the hash, and on any difference record
both identities and both hashes and refuse to overwrite.

What should this unit require for its external products?

A. The same contract as `acquisition` — byte-identical or explicitly divergent, recording both product identities and both hashes, refusing to overwrite
   > **Impact**: One rule across both units that fetch external material, so an implementer meets the same contract twice rather than two shapes. A GIM re-issue stops the run for adjudication, which for a comparator table is arguably more disruptive than for a raw input.

B. Terminate on any difference, with no divergence record beyond the failure
   > **Impact**: Simplest, and consistent with R-61's existing hash-mismatch termination. It discards the side-by-side identity evidence that makes a divergence interpretable later — the exact evidence whose absence for three acquisition months `team.md` records as making disagreement uninterpretable.

C. Treat external comparator products as re-derivable and simply regenerate them
   > **Impact**: Lowest friction, and IRI output genuinely is regenerable from a pinned implementation. It makes the comparator silently non-reproducible across time, and TE requires the IRI implementation, switches, topside option and 2000 km ceiling pinned precisely so the output is fixed.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the two units should not diverge on the same question, and a comparator whose bytes changed without a record is worse than a raw input whose bytes changed, because the comparison is what the thesis reports. The disruption is the intended cost: a re-issued GIM day that silently replaced the old one would change a published number with no trace.

[Answer]: A

---

## Consolidated Summary Confirmation

Confirm this reading before the two artifacts are written. Nothing below decides a
scientific value, and nothing claims a gate or acceptance row is discharged.

**Scope.** Two artifacts — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit. Those categories are still
assessed in the security artifact's scope note.

**Q1 = A — NFR-IRI-01 gains a run-time content assertion alongside the authoritative static
check.** Before any feature matrix reaches training or inference, it is asserted to carry
**no `iri_*` column, no IRI-derived residual and no IRI-computed value**. This closes the
**non-import data channel** the static check structurally cannot see — an IRI value cached
to a file by `scripts/04_build_external_products.py` and read back by a feature builder that
imports nothing from `src/external/`. **The cost is stated, not hidden:** the feature matrix
is **`features-and-splits`'** surface, so this is a **two-half cross-unit contract** on the
BLK-08 pattern, and **this stage states only this unit's half**. R-56's static check remains
**authoritative** for the import boundary; the assertion is a second, independent limb, not
a replacement.

**Q2 = A — a revised external product is byte-identical or explicitly divergent.** A re-run
recomputes the hash and, on any difference, **records both product identities and both
hashes and refuses to overwrite**. This is the **same contract `acquisition` adopted** for
provider files, so the two units that fetch external material do not diverge. A re-issued
CODE final GIM day stops the run for adjudication — the intended cost, because a silently
replaced comparator day would change a published number with no trace.

**Carried, not re-decided.** R-56's transitive import allowlist with the static check
authoritative; R-57's trailing-mean property proof; R-57a's **≤3 h carry-forward then
exclude** with its injected-four-hour-gap control; R-58's three alignment limbs; R-59's
IRI generation **blocked** without a passing, complete, pre-declared validation; R-60's four
GIM obligations with **one blocked**, read as **partial control plus a named residual**;
R-61's missing-month record and hash-mismatch termination; R-62's three Dst restrictions kept
apart; R-63's **time-indexed only** driver series; R-54/R-54a/W-2/W-2a on which upstream
artifact governs coverage figures and TA-36's split ownership.

**Status claims made.** None. **`src/external`'s contracts are an amendment owed** (R-55).
**REQ-ENG-9, FR-P1-04-4, FR-P1-04-15 and FR-P1-04-18 carry no acceptance row.** **TA-36
exists but is `Pending` — not implemented, not executed, not passing.** The
`gim_network_overlap_flag` audit has not run and **no independence claim may precede it**.
G-09 is signed (D-31) with its preconditions UNMET; stage 3.1 remains FAIL; no Python
interpreter exists here, so every test is written-but-unexecuted or unwritten.

Reply `Looks correct` to proceed, or state what to change.

[Answer]: Looks correct
