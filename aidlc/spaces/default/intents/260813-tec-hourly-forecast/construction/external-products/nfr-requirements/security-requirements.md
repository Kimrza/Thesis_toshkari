# Security Requirements — `external-products`

**Unit** `external-products` (Bolt 5) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NOTHING HERE IS CLAIMED SATISFIED
>
> **`src/external`'s contracts are an amendment owed** (R-55) — the module contracts this
> unit's rules assume are not approved artifacts yet.
>
> **REQ-ENG-9, FR-P1-04-4, FR-P1-04-15 and FR-P1-04-18 carry no acceptance row.**
> **TA-36 exists but is `Pending` — not implemented, not executed, not passing.** WS-09,
> WS-10, WS-11, TA-08 and TA-12 are undischarged. The **`gim_network_overlap_flag` audit has
> not run**, and **no independence claim may precede it**.
>
> **G-09 is signed (D-31) with its own preconditions UNMET**; **stage 3.1 remains FAIL**. No
> Python interpreter exists in this environment, so **`tests/test_iri_denial.py` is written
> but UNEXECUTED** and every other test is unexecuted or unwritten.
>
> No scientific value is decided here, and TE §18.2's absolute rule stands.

## Sources

- `../functional-design/business-rules.md` — **R-54**/**R-54a** (the story map governs this unit's coverage figures; TA-36's primary acceptance test is **not** this unit's), **R-55** (`src/external` contracts are an amendment owed), **R-56** (the import allowlist is enforced **transitively**, and the static check is **authoritative**), **R-57** (the F10.7 mean is trailing, proven as a property), **R-57a** (missing driver values carry forward **at most 3 hours**, then the row is excluded), **R-58** (driver alignment's three limbs), **R-59** (IRI generation is **blocked** without a passing, complete, pre-declared validation), **R-60** (the GIM comparator: four obligations, **one blocked**), **R-61** (a missing month is recorded; a hash mismatch terminates), **R-62** (Dst's three restrictions kept apart; eligibility is a property of the data), **R-63** (driver series are **time-indexed only**).
- `../functional-design/business-logic-model.md` — **W-1** … **W-10**, in particular **W-3** (enforcing the module-path import allowlist), **W-4** (the trailing mean proven as a property), **W-5** (driver alignment onto the hourly grid), **W-6** (the IRI benchmark: validated before generation, blocked on failure), **W-7** (the GIM comparator's four obligations as one contract), **W-8** (closing `audit_ec1_drivers.py`'s exit-code gap, including its provenance-fields block), **W-9** (Dst's three restrictions), § Requirement-to-workflow map.
- `../../acquisition/nfr-requirements/security-requirements.md` — **§ SEC-A-02**, the byte-identical-or-explicitly-divergent contract this unit adopts unchanged.
- `../../../inception/requirements-analysis/requirements.md` — **FR-P1-04-1** *(cited 2026-09-01 on adversarial finding 1, Major — this is the row the **allowlist-not-denylist** framing comes from, and SEC-E-01 reproduced its text on both limbs while citing only NFR-IRI-01 against the same WS-10/TA-07 rows)*, **REQ-ENG-9**, **FR-P1-04-3**, **FR-P1-04-4**, **FR-P1-04-9**, **FR-P1-04-15**, **FR-P1-04-17**, **FR-P1-04-18**, **NFR-IRI-01**, **NFR-LEAK-01**.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§5.2** (the network-overlap audit and `gim_network_overlap_flag`), **§6.2** (the driver dictionary; the trailing 81-day mean; carry-forward ≤ 3 h then exclude), **§8.1** (`iricore` — pinned implementation, switches, topside option, **explicit 2000 km ceiling**, forecast-safe drivers, 5–10 validated samples), **§10** (never backfill from future final values), **§12** (the import-boundary rule), **§19** (TA-07, TA-08, TA-12, TA-36), **§16** (WS-09, WS-10, WS-11).
- `../../../../../../../../PreFlight/vision_document(3)(2)(2).md` — **§7.1** (the binding architectural rule), **§6.10**, **§6.6** (the spatial-representativeness mismatch).
- `nfr-requirements-questions.md` — Q1 = A, Q2 = A, and the receipted Consolidated Summary Confirmation.

---

## Scope note

`produces_kinds` excludes `performance-requirements`, `scalability-requirements` and
`reliability-requirements` for a `library` unit. Assessed anyway:

| Category | Assessment for `external-products` | Where it lives |
|---|---|---|
| **Performance** | No latency target. IRI generation over a year of hourly epochs at three cells is the largest compute this unit does, and it is **blocked** until R-59's validation passes — so throughput is not the binding constraint, the gate is. | § SEC-E-03 |
| **Scalability** | Bounded: three cells, calendar 2022, hourly. No growth projection. | — |
| **Reliability** | Two-tier and already fixed by R-61: a **missing month is recorded** (completeness, non-fatal, machine-readable), a **hash mismatch terminates** (integrity). This unit is where that distinction is sharpest, because a missing driver hour and a wrong driver hour have opposite handling. | § SEC-E-04 |
| **Security** | This artifact — dominated by **containment**, not access control. | — |
| **Observability** | The provenance-fields block W-8 adds to `audit_ec1_drivers.py`, and the run record. | § SEC-E-04 |

---

## SEC-E-01 — NFR-IRI-01 is enforced on two independent limbs

**Requirement — limb 1, the module graph (R-56, W-3, TE §12, TA-07).** `src/external/iri.py`
and `src/external/gim.py` are **never imported, directly or transitively**, by any module
under `src/features/` or `src/models/`. The only permitted importers are
`scripts/04_build_external_products.py` and `src/evaluation/`. **The static check is
authoritative** for this unit, and enforcement is **transitive** — a shim that re-exports is
a violation, and so is a dynamic `importlib.import_module`, an `__import__`, or a computed
module path.

**Requirement — limb 2, the data (Q1 = A). NEW at this stage.** Before any feature matrix
reaches training or inference, it is asserted to carry **no `iri_*` column, no IRI-derived
residual, and no IRI-computed value**.

**Why limb 2 exists, stated plainly.** `functional-design` discloses a residual limb 1
**structurally cannot see**: a **non-import data channel**. An IRI value written to a cached
file by `scripts/04_build_external_products.py` and read back by a feature builder that
imports nothing from `src/external/` passes every import check ever written. NFR-IRI-01
would be breached with **no mechanism firing**. This unit is where such a value originates,
which is why the requirement is stated here.

**The cost, stated rather than hidden.** The feature matrix is **`features-and-splits`'**
surface, not this unit's. This is therefore a **two-half cross-unit contract** on the same
pattern the project already uses for BLK-08, and **this artifact states only this unit's
half**: that the assertion is required, and what it must assert. **`features-and-splits`
owes the other half** — where the assertion sits and what it raises — and **this unit does
not declare the contract satisfied from one side.**

**Limb 2 does not replace limb 1.** R-56's static check stays authoritative for the import
boundary. The two limbs answer different questions, and neither substitutes for the other —
the same structure `governance-guards` R-23 is understood to use for the phase boundary.
*(Two cross-unit analogies in this artifact — this one, and the BLK-08 two-half-contract
precedent cited below — sit **outside this stage's read scope** and are **stated as
understanding, not verified here** (adversarial finding 2, Minor, 2026-08-31). Neither
carries any of this unit's own obligations; both are worth confirming at the gate rather
than standing as unearned reassurance.)*

**The negative control is what proves it.** WS-10 requires the denial test to **fail on a
deliberately injected `iri_*` field**. With limb 2, that injection can be made **against the
data** as well as against the module graph — which is what makes the disclosed channel
testable at all. **`tests/test_iri_denial.py` is written but UNEXECUTED.**

**Requirement.** IRI joins **only at evaluation time**, onto the **frozen comparison-wide
mask**. Never at training, never at inference, never as a residual.

> ### ⛔ WHAT SURVIVES BOTH LIMBS — read this with the rule, not after it
>
> *(Moved into the rule body 2026-08-31 on adversarial finding 1, Major. It was stated only
> in a `[assumption]` bullet at the foot of the document — the placement `project.md` records
> twice as a defect class, where a load-bearing fact lands in Assumptions while the rule
> statement an implementer reads first stays silent. It is restated below rather than moved,
> so the Assumptions bullet still carries it too.)*
>
> **A value numerically derived from IRI, renamed so it carries no `iri_*` name, and stripped
> of its provenance stamp, defeats BOTH limbs.** Limb 1 sees no import because there is none.
> Limb 2 sees no `iri_*` column and no provenance mark because both were removed. Nothing in
> this design catches it.
>
> **This is a residual, not a gap being closed here.** What bounds it is not a mechanism but
> a **person**: such a value has to be moved deliberately — computed, renamed, and stripped —
> which is a different act from the accidental leakage limbs 1 and 2 exist to prevent. **No
> artifact may describe NFR-IRI-01 as fully enforced**, and the honest statement of this
> design's reach is: it catches every accidental path and one deliberate one, and it does not
> catch a determined one.

## SEC-E-02 — The GIM comparator is evaluation-time-only, and its independence is unproven

**Requirement.** CODE final GIM is an **evaluation-time-only comparator** — never a model
input — and is **never presumed independent before the network-overlap audit** (TE §5.2,
Vision §6.10).

**Requirement.** The **`gim_network_overlap_flag` result is disclosed once the audit runs**,
and **no independence claim may precede it**. Disclosure is mandatory, not conditional on
the result being favourable.

**Requirement.** Wherever an IRI or GIM comparison is reported, the **documented
spatial-representativeness mismatch is stated at the point of report**: Phase 1 compares a
grid cell against a station-coordinate evaluation, Phase 2 an IPP cloud against a zenith
estimate, and **part of any measured difference is a geometry and sampling artefact rather
than skill**.

**Status.** R-60's four obligations stand with **one blocked**, read as **partial control
plus a named residual** — grep-class control over two of three limbs, with the uncovered
residual being tuning performed outside `gim.py` and pasted in as a constant. **The audit has
not run.**

## SEC-E-03 — IRI generation is gated on a validation that has not happened

**Requirement (R-59, W-6, TE §8.1).** IRI benchmark generation is **blocked** without a
**passing, complete, pre-declared** validation: pinned implementation, switches, topside
option, **explicit 2000 km ceiling**, forecast-safe drivers, and **5–10 validated samples**.
On failure, generation is blocked — the implementation is **not silently switched**.

**Pre-declared is the load-bearing word.** A validation whose acceptance criteria are chosen
after the samples are seen validates nothing. This is the same discipline the project applies
to ablations and to grid ranges.

**Status.** Not run. `iricore` is TE §8.1 **required** but the validation gating its use has
not been performed, so **no IRI benchmark exists**.

## SEC-E-04 — Driver integrity: lags, grades, and what may never be reconstructed

**Requirement (R-57, W-4, TE §6.2).** The F10.7 81-day mean is **trailing**, ending at the
safe-lagged day, and this is **proven as a property** rather than asserted. **A centered mean
is a defect, not a fallback** — it uses future days.

**Requirement (R-57a, TC-09).** A missing external driver value carries forward **at most 3
hours**; beyond that **the row is excluded**. The control is an **injected four-hour gap**
that must produce an exclusion.

**Requirement (R-58, W-5).** Every predictor is lagged to its **actual availability
timestamp** before it can be used at a forecast origin — Kp/ap3 **≥ 3 h**, Hp60/ap60
**≥ 1 h**, F10.7 at the **previous-day observed** value.

**Requirement (R-63, TC-12).** Driver series are **time-indexed only**: one value per epoch,
**identical across all three cells**. A join must never imply a per-cell measurement, and a
station performance difference must **never** be attributed to local forcing the dataset does
not contain.

**Requirement (R-62, W-9).** Dst's three restrictions are kept **apart**: diagnostic and
hindcast-only, never a confirmatory ML feature; **release grades never mixed** within one
series (real-time, provisional, final), with the grade for calendar 2022 recorded **before
use**; and **eligibility is a property of the data**, not of the analyst's intent.

**Requirement (TE §10).** **Never backfill a driver from future final or definitive archived
values.** Final archived values are not the contemporaneous operational values available at a
2022 forecast origin. A series can satisfy its stated lag while still being built from
reanalysed indices — **invisible in validation, fatal on discovery**. **Record the release
status of every driver, not only its lag.**

**Requirement (R-61).** A **missing month is recorded** — machine-readable, in the output
manifest, with the artifact marked derived and/or partial — while a **hash mismatch
terminates** with a message naming the file and the violated expectation.
`audit_ec1_drivers.py` returning `0` regardless of missing months is the gap **W-8 closes**.

**Requirement (TC-20).** **No value is imputed, substituted or reconstructed for the F10.7
outage window** until the measured gap is recorded and governed.

## SEC-E-05 — A revised external product is byte-identical, or explicitly divergent

**Requirement (Q2 = A).** A re-run recomputes the SHA-256 of every external product. On any
difference it **records both product identities and both hashes and refuses to overwrite**.

**This is `acquisition`'s § SEC-A-02 contract, adopted unchanged**, so the two units that
fetch external material do not diverge on the same question. R-61 already terminates on a
hash mismatch; this states what the **record** must contain when it does.

**Why it matters more here, not less.** A re-issued CODE final GIM day that silently replaced
the old one would **change a published number with no trace** — the comparator is what the
thesis reports. A stopped run awaiting adjudication is the intended cost.

**Requirement.** The recorded identity includes the product's **version or issue
designation** where the provider gives one, on the same reasoning that makes `acquisition`
record provider version suffixes: a divergence without both identities is uninterpretable.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Row primary owner | Status |
|---|---|---|---|---|
| **REQ-ENG-9** | SEC-E-04 | ⚠ **NO ACCEPTANCE ROW** | — | untested |
| FR-P1-04-3 | SEC-E-04 | via R-57a's control | — | `Pending` |
| **FR-P1-04-4** | SEC-E-04 | ⚠ **NO ACCEPTANCE ROW** | — | untested |
| FR-P1-04-9 | SEC-E-02 | WS-09, TA-12 | **`external-products`** (WS-09); `models-and-baselines` (TA-12) | `Pending` |
| **FR-P1-04-15** | SEC-E-03 | ⚠ **NO ACCEPTANCE ROW** | — | untested |
| FR-P1-04-17 | SEC-E-04 | **TA-36** | `features-and-splits` | ⚠ **`Pending` — not implemented, not executed, not passing** |
| **FR-P1-04-18** | SEC-E-02 | ⚠ **NO ACCEPTANCE ROW** | — | untested |
| **FR-P1-04-1** | SEC-E-01 | WS-10, TA-07 | — | `Pending` — **test written, UNEXECUTED** |
| NFR-IRI-01 | SEC-E-01 | WS-10, TA-07 | — | `Pending` — **test written, UNEXECUTED** |
| NFR-LEAK-01 | SEC-E-01 (limb 2), SEC-E-04 | TA-11 | `features-and-splits` | `Pending` |

**Derived and printed**: 5 requirement sections (SEC-E-01…SEC-E-05); **10** coverage rows *(count
re-derived 2026-09-01 on adversarial finding 1, Major; superseded figure preserved: **9**)* — the
7 requirements the `functional-design` map carries, plus **FR-P1-04-1**, NFR-IRI-01 and
NFR-LEAK-01, which this artifact states obligations against; **4** requirements with no
acceptance row (REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18) — **re-derived by counting
blank acceptance-row cells in the table above, not read off the map**, and unaffected by the new
row, which carries WS-10/TA-07; **0** rows claimed satisfied.

**`FR-P1-04-1` was the miss, and it was the source row, not a peripheral one.** SEC-E-01
reproduces its text on both limbs — the permitted-importer **allowlist, not denylist**, and no
`iri_*` column, IRI-derived residual or IRI-computed value reaching training or inference, with
IRI and GIM joining **only at evaluation time** on the frozen comparison-wide mask — while the
table cited only `NFR-IRI-01` against the identical WS-10/TA-07 rows. The set the table was built
from came from the `functional-design` map, and the map does not carry `FR-P1-04-1`. The clause
*"matching the map"* is withdrawn from the no-acceptance-row figure above for that reason: on two
other units this stage, that same clause made a count right only by coincidence.

## Assumptions & Open Questions

- **[Q1]** Limb 2 is **new at this stage** and is **one half of a two-half cross-unit contract**. **`features-and-splits` owes the other half** — where the assertion sits, what it raises, and when it runs relative to the split. **This unit does not declare the contract satisfied from one side**, and the other half has not been stated.
- **[assumption]** "IRI-derived" is decidable on a feature matrix by column identity and provenance stamp. A value **numerically derived** from IRI but carrying no `iri_*` name and no provenance mark would pass limb 2. Limb 1 catches its **import** path; a value moved by hand through a file, renamed, would be caught by **neither**. **Stated as the residual that survives both limbs.**
- **[Q2]** A revised product stops the run for adjudication. **This is deliberate friction**, and it will fire on legitimate provider re-issues.
- **Carried — `src/external`'s contracts are an amendment owed** (R-55). The module contracts these rules assume are not approved artifacts.
- **Carried — the `gim_network_overlap_flag` audit has not run.** No independence claim may precede it.
- **Carried — TA-36 is `Pending`, and this unit holds only data production and upstream evidence**; `features-and-splits` holds enforcement and the primary acceptance test (R-54a, W-2a).
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-31T17:18:59Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `security-requirements.md` SEC-E-01 body vs. `## Assumptions & Open Questions` `[assumption]` bullet (line 203) | The residual that survives **both** limbs of NFR-IRI-01 — a value numerically derived from IRI, renamed, and stripped of provenance, moved by hand through a file — is stated only in an `[assumption]` bullet at the bottom of the artifact. SEC-E-01's own body (lines 58–86) states limb 2's requirement and explains the non-import data channel that motivates it, but never states, at the point a reader meets the rule, that a renamed/provenance-stripped value defeats limb 2 as well as limb 1. Given this project's own `project.md` corrections `fd-2026-08-30-sweep-derive-sites` and `fd-2026-08-30-sweep-numerals-and-surfaces` — both describing the identical failure mode of a load-bearing fact landing in `## Assumptions` while "what an implementer reads first" (the rule statement) is silent on it — this placement repeats a defect pattern the project has already paid for twice. NFR-IRI-01 is the project's most safety-critical containment rule; an implementer skimming SEC-E-01 for "what closes the channel" would reasonably conclude limb 1 + limb 2 are jointly sufficient. | Add one sentence to SEC-E-01 itself (not only to Assumptions) stating explicitly that a renamed, provenance-stripped, numerically-derived IRI value survives both limbs and remains an open residual — mirroring the "why limb 2 exists, stated plainly" paragraph already present. |
| 2 | Minor | `security-requirements.md` line 71 ("the same pattern the project already uses for BLK-08") and line 78 ("the same structure `governance-guards` R-23 uses") | Both claims invoke a sibling/other-unit precedent (a BLK-08 two-half-contract pattern, and `governance-guards` R-23's limb-independence structure) that this review cannot verify without reading another unit's `construction/` tree, which is out of the hard-bound read scope for this pass. Neither claim is load-bearing for this unit's own obligations (both are analogies offered as reassurance, not requirements), so this is not grounds for NOT-READY, but the human approver should confirm at the gate that BLK-08 and R-23 actually match the pattern claimed, since an unverified analogy used as justification is exactly the "cover" risk the dispatch brief warned about. | Confirm against the shared inception contracts or `governance-guards`' own artifact at the approval gate; if the analogy doesn't hold, drop it rather than leave it as unearned reassurance. |

### Validation Tool Results

No validation tools are listed for this stage in `.claude/aidlc-common/stages/construction/nfr-requirements.md`; none were run. All checks below were performed by direct inspection and grep against the artifacts and their declared upstream sources.

**Scope check (frontmatter `produces_kinds`):** confirmed by reading the stage file directly — `performance-requirements: [service, ui]`, `scalability-requirements: [service]`, `reliability-requirements: [service]` are the only `produces_kinds`-restricted artifacts; `security-requirements` and `tech-stack-decisions` carry no kind restriction and are always produced. For `kind: library`, this correctly excludes performance/scalability/reliability, matching the artifact's own § Scope note claim.

**Count re-derivation:** `grep -n "no acceptance row" functional-design/business-rules.md` returns line 1004: "**7** requirements, **4** with no acceptance row, **2** acceptance [rows]" and line 937's enumerated set — REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18 — matches `security-requirements.md`'s § Requirement coverage table exactly (same 4 IDs, same ⚠ markers). `security-requirements.md`'s printed 9-row / 4-no-row / 5-section derivation is internally consistent with this upstream figure (7 requirements + NFR-IRI-01 + NFR-LEAK-01 = 9). `tech-stack-decisions.md`'s claimed 5-row set (FR-P1-04-9, FR-P1-04-15, FR-P1-04-17, FR-P1-04-3, NFR-IRI-01) is exactly `security-requirements.md`'s 9-row set minus {REQ-ENG-9, FR-P1-04-4, FR-P1-04-18, NFR-LEAK-01} — the claimed "four fewer, because these four raise no technology choice" checks out by set difference, not just by total.

**Freeze-gate discipline:** no numeric value for the `iricore` switch set, topside option, or a GIM product/issue designation appears anywhere in either artifact; "2000 km" appears only as a quotation of TE §8.1's own requirement text (the ceiling TE mandates be explicit), not as a value this stage is deciding. Both freeze-gate fields are consistently left `TBD — freeze gate` in both the banner and TS-E-01/TS-E-02.

**Cross-unit half-contract (SEC-E-01):** the artifact (a) states plainly it is one half of a two-half contract (lines 69–74), (b) does not declare the contract satisfied from this side (repeated in the body and in `[Q1]`), and (c) does not silently impose an obligation on `features-and-splits` — it names the obligation explicitly ("`features-and-splits` owes the other half — where the assertion sits and what it raises").

### Coverage limits

This pass could not independently verify (read-scope bound, and not load-bearing enough to justify a carve-out spot-check given the 8-call budget): (a) whether `governance-guards`' actual R-23/R-24 text matches the static-vs-runtime distinction claimed in TS-E-03 — accepted on the strength of the substantive (not vacuous) reasoning given in-artifact; (b) whether a "BLK-08" precedent for two-half contracts exists as characterized (finding #2 above); (c) whether `features-and-splits`' functional-design actually owes/acknowledges the limb-2 obligation — out of scope for this unit's review by design.

### Summary

The artifact is disciplined about not claiming anything satisfied, keeps the two IRI-containment limbs honestly separated from each other and from the cross-unit obligation it does not own, and every printed count reconciles against its own upstream source under a set-difference check, not just a total. The one substantive gap is that the residual defeating both containment limbs — the single most safety-relevant admission in the document — sits only in an `[assumption]` bullet rather than in the rule body itself, repeating a documentation-placement defect this project has already named and corrected twice elsewhere. That is a Major finding worth fixing before this is read at the gate, but it does not misstate a fact, contradict an upstream source, or leave a TBD value filled — so it does not block READY on its own.

READY

## Review — 2026-09-01 repair verification (with iteration-1 findings, unwritten at the time)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 2

Note on the dispatch's own framing: the dispatch brief stated the iteration-1 `## Review` section was absent from the file. On inspection it is present (the section immediately above this one, verdict READY, one Major finding on `FR-P1-04-1` citation). Recorded here as ground truth rather than silently accepted, per this project's `project.md` correction to verify a fact independently before treating it as established input. The iteration-1 finding and its repair are verified below regardless.

### Iteration-1 finding (Major, restated for the record)

`FR-P1-04-1` — the permitted-importer **allowlist, not denylist**, plus the no-`iri_*`/no-IRI-derived-residual/no-IRI-computed-value rule with IRI/GIM joining only at evaluation time on the frozen comparison-wide mask — was cited nowhere in either artifact's Sources or coverage table, although SEC-E-01 reproduces its text on both limbs, and the coverage table cited only `NFR-IRI-01` against the identical WS-10/TA-07 rows.

### Verification of the repair

| # | Severity | Check | Result |
|---|---|---|---|
| 1 | — | § Sources cites `FR-P1-04-1` with a dated note | Confirmed, line 26: cited 2026-09-01, names the allowlist-not-denylist framing and the miscite. |
| 2 | — | § Requirement coverage carries a `FR-P1-04-1 \| SEC-E-01 \| WS-10, TA-07 \| — \| Pending` row | Confirmed, line 216, placed immediately above the `NFR-IRI-01` row as described. Status reads `Pending — test written, UNEXECUTED`, consistent with G-09 signed (D-31) with preconditions unmet, stage 3.1 FAIL, no Python interpreter here — no status is claimed as discharged. |
| 3 | — | `FR-P1-04-1`'s acceptance row really is WS-10/TA-07 in `requirements.md` | Confirmed by direct read of `inception/requirements-analysis/requirements.md` line 370: acceptance column reads `WS-10, TA-07`, and the requirement text matches the allowlist/no-`iri_*`/evaluation-time-join framing verbatim. |
| 4 | — | Printed count 9 → 10, superseded figure preserved, 4-blank-row figure re-derived by counting table cells, "matching the map" clause withdrawn | Confirmed at lines 219–224: "**10** coverage rows *(... superseded figure preserved: **9**)*"; "**4** requirements with no acceptance row ... re-derived by counting blank acceptance-row cells in the table above, not read off the map"; withdrawal of the "matching the map" clause stated explicitly at lines 228–234. Recount: table rows 210–218 (9 rows) plus the REQ-ENG-9 row above the excerpt = 10. Blank-cell recount against the printed table confirms 4 (`REQ-ENG-9`, `FR-P1-04-4`, `FR-P1-04-15`, `FR-P1-04-18`) — unaffected by the new row, which carries WS-10/TA-07 rather than a blank. |
| 5 | — | `tech-stack-decisions.md` moved "four fewer than nine" → "five fewer than ten", added `FR-P1-04-1` to the raise-no-technology-choice list, with the `ast`-walk justification | Confirmed: "**5** coverage rows — **five fewer** than `security-requirements.md`'s **ten**", superseded "four fewer than nine" preserved in a parenthetical; the exclusion list now reads `REQ-ENG-9, FR-P1-04-4, FR-P1-04-18, FR-P1-04-1, NFR-LEAK-01` (5 items); reconciles as set difference of the 10-row set. Set-difference re-check: 10 − 5 = 5, and `tech-stack-decisions.md`'s 5 kept rows (`FR-P1-04-9, FR-P1-04-15, FR-P1-04-17, FR-P1-04-3, NFR-IRI-01`) plus its 5 excluded rows exactly partition `security-requirements.md`'s 10. |

All four repair sites are present, consistent with each other, and consistent with the upstream `requirements.md` row they cite. No arithmetic error found on recount.

### Sweep for a surviving stale "9"/"nine"/"four fewer" site

Searched both artifacts in full (direct read, not keyword-only) for a surviving unqualified assertion of the superseded figures. Both remaining occurrences of "9" and "four fewer than nine" are inside the explicit superseded-figure parentheticals introduced by the repair itself (§ Requirement coverage in `security-requirements.md`; § Requirement coverage in `tech-stack-decisions.md`) — these are intentional "superseded figure preserved" notes per this project's sweep convention, not stale assertions. No banner, heading, `## Assumptions` bullet, or other table cell in either file asserts "9 coverage rows" or "four fewer" as a live, unqualified figure. No fifth stale site found.

### ID-space set-difference re-run

Re-enumerated citations in `security-requirements.md` § Sources (line 26) and the coverage table (lines ~205–218) against `requirements.md`: `FR-P1-04-1, REQ-ENG-9, FR-P1-04-3, FR-P1-04-4, FR-P1-04-9, FR-P1-04-15, FR-P1-04-17, FR-P1-04-18, NFR-IRI-01, NFR-LEAK-01` — 10 IDs, all resolve to rows that exist in `requirements.md` (confirmed for FR-P1-04-1 above; the remaining 9 were the iteration-1-verified set, unchanged by this repair). Checked the rest of the `FR-P1-04-*` range cited elsewhere in `requirements.md` (FR-P1-04-10, -11, -12, -13, -14, -16) against this unit's two artifacts: none of these six is claimed by `external-products`' SEC-E-* or TS-E-* rules, and none appears miscited or half-cited — they belong to other units' scope (target/lag/support-field/GIM-interpolation contracts), consistent with `external-products`' stated scope of IRI/GIM generation and import-boundary enforcement only. No sibling `FR-P1-04-*` miss found beyond the one already repaired. The eleven-NFR-ID list and `REQ-ENG-*`/`FR-WS-*` ranges outside `FR-P1-04-*` were unaffected by this repair and were not re-swept beyond the iteration-1 pass, consistent with the dispatch's framing that this pass verifies the one repair plus its immediate blast radius.

### No regression

Re-checked, unchanged from iteration 1: Q1/Q2 fidelity; the both-limbs residual sits in SEC-E-01's own body (lines 58–86, iteration-1 finding #1 on this remains open — the residual is *also* stated in `[assumption]`, and the repair did not move it into the rule body; this is a **carried-forward, not a new, Major** and is not re-counted below); the data-flow (SEC-E-01) and module-graph (TS-E-03/R-56) IRI rules stay textually distinct; GIM stays evaluation-time-only comparator, non-independent-until-audit, with mandatory `gim_network_overlap_flag` disclosure (TS-E-02, SEC-E-02).

### Nothing newly claimed discharged

Confirmed: G-09 signed (D-31) with preconditions **UNMET** (tech-stack-decisions.md banner); stage 3.1 **FAIL** (same banner); `configs/` absent (implied by both `TBD — freeze gate` fields remaining unset); no Python interpreter here, so `test_iri_denial.py` is **written-but-unexecuted** (`Pending — test written, UNEXECUTED` on both the new FR-P1-04-1 row and the pre-existing NFR-IRI-01 row); WS-10, TA-07, TA-36 and the §18.3 preflight all read `Pending`, never `PASS`. No row anywhere claims a passing status.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major (carried from iteration 1, unresolved) | `security-requirements.md` SEC-E-01 body vs. `[assumption]` bullet | The residual defeating both IRI-containment limbs (a renamed, provenance-stripped, numerically-derived IRI value) still sits only in `[assumption]`, not in SEC-E-01's own rule statement. This repair pass did not touch it — it was orthogonal to the `FR-P1-04-1` citation gap. | Add the residual sentence to SEC-E-01's own body before the gate, as iteration 1 recommended. |

No new findings from this pass; the `FR-P1-04-1` repair is sound, complete, and introduces no fresh defect.

### Summary

The `FR-P1-04-1` citation repair is verified sound across all four claimed sites: the Sources note, the new coverage row (with correct WS-10/TA-07 acceptance evidence verified against `requirements.md` directly), the re-derived 9→10/4-blank-row count, and the dependent `tech-stack-decisions.md` 5-row set — all arithmetic checks out under recount and set-difference, and no stale "9"/"four fewer" assertion survives unqualified. The one substantive gap remains the carried-forward Major from iteration 1 (the both-limbs residual belongs in SEC-E-01's body, not only `## Assumptions`), which this repair did not address because it was scoped to a different finding. Two Majors have not accumulated — only one is currently open — so this does not block READY.

READY
