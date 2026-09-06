# Security Design — `statistical-inference`

**Unit** `statistical-inference` (Bolt 10) · **Kind** `library` · **Stage** `nfr-design`

> ## ⚠ NOTHING HERE IS CLAIMED SATISFIED
>
> This is a design. **No module is created, no bootstrap has ever executed, no test has
> run.** No Python interpreter exists in this environment; `configs/` and `src/evaluation/`
> do not exist. **The interval method is UNCONFIRMED** (percentile proposed, routed to the
> gate; 3.5 stops and reports if reached unconfirmed). **The block-resampling scheme and the
> correlation series are proposed, not decided.** **BLK-03, BLK-04, BLK-08 and BLK-09 are
> inherited open exit conditions.** WS-17 (primary), TA-13 and TA-26 are undischarged.
> **G-09 is signed (D-31) with preconditions UNMET**; G-05 and G-06 remain `Blocked`.
> TE §18.2's absolute rule stands: **no scientific value is decided here.**

## Sources

- `../nfr-requirements/security-requirements.md` — **SEC-S-01** (four pins: PCG64, child streams, recorded evidence, `TypeError` by signature), **SEC-S-02** (one estimand copy; the bootstrap is a metric entry point in full; the block grid; the vector property), **SEC-S-03** (the widening guard, the Q1 = B adjudication route, the method-parametric interval), **SEC-S-04** (no memory ceiling; the frozen replicate count). This design gives each a mechanism; it re-decides none.
- `../nfr-requirements/tech-stack-decisions.md` — **TS-S-01…TS-S-05**, especially TS-S-01 (the RNG pin and seed-sequence spawn) and TS-S-04's named design consequence (how replicates are held is the one open implementation dimension).
- `../functional-design/business-logic-model.md` — **W-1** (the boundary and its re-asserted preconditions, Q1 = C there), **W-2** (precompute once), **W-3** (block grid), **W-4** (seed/stream discipline), **W-5** (interval, method-parametric), **W-6** (widening guard), **W-7** (correlation emission), **W-8** (`tests/test_bootstrap.py`, eight checks).
- `../functional-design/business-rules.md` — R-113…R-122.
- `../../evaluation-and-comparison/nfr-design/security-design.md` — **SD-C-01** (the shared guard module this unit's Q2 = A imports) and **SD-C-02** (the containment ordering check the DEC path inherits at the access-record level). Cross-unit design contract, stated as such.
- `../../../inception/requirements-analysis/requirements.md` — FR-P1-05-8, FR-P1-04-5 (context), NFR-DET-01, NFR-REP-01, NFR-AUD-01.
- `nfr-design-questions.md` — **Q1 = A** (raw-byte replicate hash, four pinned facts), **Q2 = A** (shared guard module), and the receipted Consolidated Summary Confirmation.
- Absent by scope design (`library` kind): `performance-requirements.md`, `scalability-requirements.md`, `reliability-requirements.md` were not produced at `nfr-requirements`; that stage's Scope note carries the assessments (performance is real and unmeasured — § SD-S-04 below inherits it).

---

## Scope note

"Security" here is what `nfr-requirements` fixed: **the integrity of the reported
uncertainty** — an interval too narrow overstates confidence in the thesis's central claim.
No credential, user, or network surface exists in this unit. Reliability's fail-closed
posture and performance's measured-not-invented posture are realised by the mechanisms
below.

## SD-S-01 — The replicate hash is defined down to the byte (Q1 = A)

**The gap.** SEC-S-01 requires the replicate hash as WS-17's emitted evidence and §13.7
requires exact equality — but no artifact said **what bytes are hashed**. A hash over floats
is platform-independent only if the serialisation is canonical; leaving it to 3.5 could give
two governed platforms two canonical forms.

**Design.** The replicate hash is **SHA-256 over the replicate vector's raw IEEE-754
bytes**, canonical form pinned by four facts:

1. dtype **`float64`**,
2. **little-endian** byte order,
3. **C-order** (contiguous) layout,
4. **replicate order = draw order** (never sorted before hashing).

All four are **recorded in `BootstrapResult` beside the hash**, exactly as the generator
identity already is — the evidence describes itself, so a future dtype or layout drift is
**detectable** rather than silent. One `tobytes()` pass; no precision constant is invented
(the rejected decimal-text option's cost); no scientific value is touched — this is an
engineering contract in the same class as the PCG64 pin, and it is what makes §13.7's
exact-equality assertion *executable*: same seed → same draws (PCG64 pin) → same vector →
same bytes (this pin) → same hash.

**Negative controls (inherited from R-117's 13–15, now byte-grounded):** different seed →
different hash; same-seed rerun → identical hash, compared for **equality, not tolerance**
(NFR-REP-01); a `BootstrapResult` missing any of the four canonical-form facts, or the
generator identity, or the seed key, **fails** the evidence check in `test_bootstrap.py`.

**Append-safe (NFR-AUD-01):** a rerun writes a new `BootstrapResult`; it never overwrites a
prior one, and a failed run stays visible with status and reason — `foundation`'s registry
rows own that surface; this unit emits, it does not manage rows.

## SD-S-02 — Preconditions come from the shared guard module (Q2 = A)

**Design.** `vector_block_bootstrap` re-asserts its metric-entry-point preconditions (W-1's
four: registered mask, stamps, DEC hash receipt, target space) by **calling the shared
`src/evaluation` guard module** designed at `evaluation-and-comparison` SD-C-01 — one copy
of each cross-cutting check, intra-package import, no new boundary crossed (R-112's path
grant already co-locates both units in `src/evaluation`).

**What stays local.** The **bootstrap-specific** refusals are this unit's own and raise
**`BootstrapError`**: a block-grid boundary violation (R-115), a missing pair no declared
rule handles (R-116), an unrecognised/absent/**unconfirmed** interval method naming the
config key (R-119), and the fixture-time widening raise (R-120). A call without `seed`
stays a **`TypeError` by signature** — unrepresentable, not checked.

**Why single-copy is this unit's own principle.** R-114 already states it for the estimand:
the copy inside a 10,000-iteration loop is the one nobody reads. The same argument covers
guards, and the drift class is not hypothetical — R-105 raised `LeakageError` where R-92
raised `PartitionError` for the identical condition until the governance board caught it
(GOV-2026-08-28-FD-01 Rec 8). One copy leaves nothing to drift.

**The half-contract, both directions.** This unit **consumes** the guard module's checks;
`evaluation-and-comparison` **owns** them. `vector_block_bootstrap` joins the sibling's
per-entry negative-control set: one control per violating input class through this entry
point, asserting the raise (stamp-less prediction, unregistered mask, mask-mismatched
`partition_id` set, receipt-less `DEC` call, transformed-space `ABL-DIFF` frame). **This
unit's half is stated here; the sibling's half — naming `vector_block_bootstrap` among its
guarded entry points — is OWED at the sibling's next touch, not yet stated there, and the
contract is satisfied by neither side alone.** *(Corrected 2026-09-05 at the stage gate,
governance Recommendation 5; superseded: "Stated on both sides … the sibling's SD-C-01
already names W-5's path among its guarded entry points" — the sibling's artifacts named no
such entry point, its per-entry set being C2/C3/C5/C6, and its own "W-5" is the G-06 path,
not this unit's interval workflow.)*

**DEC inheritance.** On `DEC`, the receipt check the guard module runs includes the
sibling's SD-C-02 **containment** ordering (access record carries `mask_bundle_ids` +
`mask_registry_hash`); this unit inherits it by calling the same guard and adds nothing to
it — unrunnable while BLK-07 is open, as recorded upstream. *(The guard set this delegation
relies on now includes the mask-vs-member alignment check — the sibling's formerly open
Major, closed 2026-09-05 at the stage gate as its sixth guard, governance Recommendation 1 —
so "adds nothing to it" no longer leaves that check homeless.)*

## SD-S-03 — Stream isolation and the widening guard, as designed mechanisms

**Stream isolation (R-117, TS-S-01).** The primary stream (block-index draws) and the two
child streams (48-hour sensitivity; widening comparator) are **seed-sequence spawns** —
adding or removing a consumer cannot perturb another's draws, so the confirmatory replicate
hash cannot change for a reason unrelated to the confirmatory computation. The spawn tree
(which child index feeds which consumer) is fixed at design: child 0 = sensitivity,
child 1 = widening comparator; the assignment is recorded in `BootstrapResult` so the
evidence names its streams.

**The widening guard (R-120, SEC-S-03).** The comparator (the rejected Q-27 within-station
method) is **exact and quarantined** — computed from child stream 1, never load-bearing,
present solely to be beaten. The raise lands at **fixture time**; on real data the
comparison is a **mandatory disclosure**, and a non-widening outcome on December is a
**named G-06 item for the supervisor** (Q1 = B upstream; the abort policy stays owed to the
Supervisor at G-05 per Rec 23 — this design pre-empts nothing).

## SD-S-04 — Resource posture: the one open dimension, bounded by design

**No memory ceiling exists in the authorities and none is adopted** (SEC-S-04's ⛔ box,
inherited whole). The replicate count 10,000 is frozen and untouchable. The one dimension
left to an implementer — **how replicates are held** (TS-S-04) — is bounded here without a
number: the replicate **vector** (one `float64` estimand scalar per replicate) is
**materialised in full**, because (a) the percentile proposal — if confirmed — re-derives
the interval from the replicate set alone, (b) Q1 = A's hash is over that vector's bytes,
and (c) 10,000 × 8 bytes is four orders of magnitude below any plausible constraint —
printed: 80,000 bytes. What remains genuinely measurement-bound is the **precomputed
per-pair array and the resampling workspace**, whose peak is **measured on the fixtures and
frozen, never invented** (§15.1); neither fixture has run, so no figure exists and none is
stated. CPU remains a complete execution path; the in-Kaggle obligation binds the G-06 run
as recorded at TS-S-05.

---

## Requirement coverage

| Requirement | Design section | Acceptance row | Status |
|---|---|---|---|
| FR-P1-05-8 | SD-S-01, SD-S-02, SD-S-03, SD-S-04 | WS-17 (primary), TA-13, TA-26 | `Pending` — no bootstrap has ever run |
| FR-P1-04-5 *(context — `features-and-splits`')* | SD-S-02 (block grid over its folds/embargo, via W-1) | — | `Pending` |
| NFR-DET-01 | SD-S-01, SD-S-03 | WS-17 (supporting), TA-13 | `Pending` |
| NFR-REP-01 | SD-S-01 (the byte-exact equality this design makes executable) | WS-20, TA-17 — rows owned by `fixtures-and-reproducibility` | `Pending` |
| NFR-AUD-01 | SD-S-01 (append-safe emission) | TA-10, TA-21 | `Pending` — rows owned elsewhere; TA-21's owner is disputed at the gate (see Assumptions) |

**Derived and printed**: 4 design sections (SD-S-01…SD-S-04); **5** coverage rows, matching
`security-requirements.md`'s 5 exactly (same ID set, set-differenced: +0 / −0); **0** rows
claimed satisfied; **1** figure derived and printed (80,000 bytes); **0** scientific values
decided.

## Assumptions & Open Questions

- **[Q1]** The four canonical-form facts are engineering contracts like the PCG64 pin. If a
  future NumPy changes `float64` semantics or PCG64's stream, the recorded facts make the
  break **diagnosable**; they do not prevent it — the environment pin owns prevention.
- **[Q2]** The shared-guard import is a **design-level dependency on
  `evaluation-and-comparison`'s SD-C-01 module**, which does not exist yet (G-09 authorises
  creation; nothing is built). If 3.5 reshapes that module, this unit's checks move with it —
  the contract is the check semantics, not the file name.
- **Carried — the interval method, block-resampling scheme, correlation series and §15.3
  replicate-count classification stay proposed and routed to their gates.** This design is
  method-parametric around the first and touches none of them.
- **Carried — TA-21's ownership is disputed**: this project's diary records
  `unit-of-work.md` assigning TA-21 to `fixtures-and-reproducibility` while two units'
  artifacts attribute it elsewhere; a gate ruling covering all representations is pending.
  The row is cited here as `nfr-requirements` carries it, not re-adjudicated.
- **Carried — BLK-03, BLK-04, BLK-08, BLK-09 open; the peak-memory figure owed as a fixture
  measurement; the in-Kaggle obligation at G-06.**
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or
  claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T06:08:53Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `security-design.md` § SD-S-02 (lines 71-75, 89-94, 96-99); cross-checked against `../../../functional-design/business-logic-model.md` W-1 precondition 2 and `../../evaluation-and-comparison/nfr-design/security-design.md` § SD-C-01 (table, lines 43-49) | **SD-S-02 claims full delegation of a precondition the shared guard does not actually implement.** This unit's own `business-logic-model.md` W-1 precondition 2 states three distinguishable raises for the stamp check, verbatim: a `partition_id` mismatch **between members** raises `PartitionError`; an absent stamp or `transform_id` mismatch raises `LeakageError`; and **"a mask whose recorded `partition_id` differs from the members' raises `FairnessError`"** — a *mask-versus-member* mismatch, distinct from the member-versus-member checks. SD-S-02 asserts `vector_block_bootstrap` "re-asserts its metric-entry-point preconditions (W-1's four: registered mask, stamps, DEC hash receipt, target space) by calling the shared `src/evaluation` guard module," and later "This unit inherits it by calling the same guard and adds nothing to it." But the sibling's own SD-C-01 guard table — the one file this brief's spot-check carve-out permits reading — has no guard implementing the mask-vs-member check: `require_stamps` (→`LeakageError`) and `require_partition_agreement` (→`PartitionError`) only compare `Prediction`s to each other, and `require_registered_mask` (→`FairnessError`) is scoped to comparison-**set membership** (R-106/R-107), not partition-stamp alignment between the mask and the predictions scored against it. This is exactly the gap `evaluation-and-comparison/nfr-design/security-design.md`'s own `## Review` (finding 1, Major, still unresolved as of the single iteration on that file) already identifies against its own artifact. SD-S-02 therefore states a completeness claim over this unit's own W-1 precondition 2 that the artifact it delegates to does not support — the check is homeless: nobody's guard module implements it, yet both units' designs write as if the shared import covers it. | Either state this gap explicitly as a carried dependency on the sibling's open finding (do not claim "adds nothing to it" without qualification), or add the mask-vs-member `FairnessError` check to this unit's own local refusals (alongside the block-grid/missing-pair/method refusals already kept local) until the sibling's guard covers it. |
| 2 | Minor | `security-design.md` § SD-S-02, line 94 | **Ambiguous cross-unit label collision on "W-5."** The sentence "the sibling's SD-C-01 already names W-5's path among its guarded entry points" reads, in context, as referring to *this unit's* W-5 — this artifact's own § Sources defines "W-5" as "interval, method-parametric." But `evaluation-and-comparison/nfr-design/security-design.md` § SD-C-01's Sources independently define its own "W-5" as "the G-06 graph" (its locked-test path), an entirely different workflow under an entirely different unit's own W-numbering. The two units number their workflows W-1…W-8 independently, so "W-5" is not a stable cross-unit identifier; the sentence likely intends the sibling's locked-test/receipt guard (consistent with the DEC-receipt context immediately preceding it), but says so ambiguously enough that a reader could take it as a (false) claim that the sibling's guard already covers this unit's own W-5 (interval construction), which it does not address at all. | Reword to name the sibling's guard explicitly (e.g. "the sibling's `require_locked_receipt` guard, tagged R-109/W-5 in its own numbering") rather than the bare cross-unit label "W-5," to avoid conflating two independently-numbered workflows. |

### What was verified

- **Requirement-coverage completeness (task #4).** `security-requirements.md`'s 5-row set (lines 200-208): `FR-P1-05-8, FR-P1-04-5, NFR-REP-01, NFR-DET-01, NFR-AUD-01`. `security-design.md`'s coverage table (lines 137-143): `FR-P1-05-8, FR-P1-04-5, NFR-DET-01, NFR-REP-01, NFR-AUD-01` — same 5-ID set. Set difference: **+0 / −0**, matching the artifact's own printed claim ("5 coverage rows, matching `security-requirements.md`'s 5 exactly... +0/−0").
- **Byte-count arithmetic (task #1).** 10,000 replicates × 8 bytes (`float64`) = **80,000 bytes**, matching SD-S-04's printed figure exactly.
- **Q1 = A canonical form (task #1).** The four pinned facts (dtype `float64`, little-endian, C-order, draw order) are sufficient for a deterministic, platform-independent byte serialisation given the project's CPU-only, two-platform constraint (TC-01); no invented precision constant is introduced (unlike rejected option B), and the facts are recorded beside the hash for diagnosability, consistent with `nfr-design-questions.md` Q1's answer and impact analysis.
- **Q2 = A half-contract, structurally (task #2).** Bootstrap-specific refusals (block-grid violation R-115, missing-pair rule R-116, unconfirmed-method R-119, fixture-time widening raise R-120) are kept local and raise `BootstrapError`, matching W-1's `RAISES` contract; the shared-guard delegation is stated on both sides (this file's SD-S-02 and the sibling's SD-C-01) without either side declaring it satisfied — except for the gap in finding #1 above, no check was found double-owned.
- **Scientific-value discipline (task #3).** Interval method, block-resampling scheme, correlation series and the §15.3 replicate-count classification are all carried as open/proposed in § Assumptions, never decided. Replicate count 10,000, seed 20221201 and the 24-hour block length are encoded as frozen values, never re-derived or altered. No memory ceiling is asserted or borrowed (SD-S-04) — consistent with `security-requirements.md` § SEC-S-04 and `tech-stack-decisions.md` § TS-S-04's identical "no ceiling exists in the authorities" posture.
- **Status honesty (task #5).** No gate, test, or acceptance row is claimed satisfied or run; every coverage-table row reads `Pending`. BLK-03/04/08/09 carried as open. G-09 stated signed (D-31) with TE §18.3 preconditions unmet, consistent with `business-logic-model.md`'s header. The widening comparator is stated exact-and-quarantined, never load-bearing, in both SD-S-03 and `logical-components.md`'s B5 row and failure-domain table.
- **Cross-artifact consistency (task #6).** Component names B1–B7, stream assignments (primary = block-index draws; child 0 = sensitivity; child 1 = widening comparator) and field names (`BootstrapResult`, `mask_bundle_ids`, `mask_registry_hash` inherited via the guard) are consistent between `security-design.md` and `logical-components.md`. Both files carry well over 2 H2 headings, reference every consumed upstream artifact by name in § Sources, and both explicitly state the absence of `performance-requirements.md`/`scalability-requirements.md`/`reliability-requirements.md` for this `library`-kind unit.

### Coverage limits

- The spot-check carve-out was exercised only against `evaluation-and-comparison/nfr-design/security-design.md` (the one file the brief names); `evaluation-and-comparison/nfr-design/logical-components.md` was **not** opened, so the C1/C7 citations in this unit's `logical-components.md` § Sources (naming the sibling's C1 as the guard module and C7 as the host process) are taken at face value and not independently verified against that file.
- Did not independently re-derive `R-113`…`R-122` or `W-1`…`W-8`'s full text beyond what was needed to check the specific claims above (the mask-vs-member precondition, the byte figure, the coverage table); `business-logic-model.md` was read only through line 507 of 805 (page 1) plus the Q&A file — W-7/W-8 and the remainder of the document were not read in full, so any defect confined to unread lines (roughly W-7 onward) would not surface in this pass.
- `unit-of-work.md`'s TA-21-ownership dispute, cited in this artifact's Assumptions, was not independently verified (out of this pass's read scope); recorded as stated.
- No validation tooling was listed for this stage in the dispatch brief; all checks above were performed by direct reading and manual set-difference/arithmetic, printed above.

### Summary

The two artifacts are disciplined about status honesty and hold up on the requirement-coverage set-difference (+0/−0 against the upstream 5-row set), the byte-count derivation, and the scientific-value-discipline check (nothing decided, nothing re-derived). One Major finding survives: SD-S-02's claim that this unit's mask-vs-member `FairnessError` precondition (stated in this unit's own W-1) is fully covered by the shared guard module does not hold, because the sibling's own guard table has a confirmed, unresolved gap for exactly that check — the check is effectively homeless across both units' designs. One Minor finding (an ambiguous cross-unit "W-5" label collision) is also raised. At 1 Major and 1 Minor, this does not cross the >2-Major NOT-READY threshold, but the Major should be closed — by an explicit carried-dependency statement or a local fallback check — before 3.5 builds from this design, since it is the same class of gap (a named failure mode with no assigned enforcement point) the sibling's own reviewer already flagged as unresolved.

READY

## Review — 2026-09-05 post-gate repair verification

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T07:50:08Z
**Iteration:** 1 (fresh budget after gate rejection)

### Recommendation 5 — verified item by item

Target: SD-S-02 (`security-design.md` lines 89–108).

1. **"Stated on both sides" claim removed.** Confirmed. The live claim now reads: "This unit's half is stated here; the sibling's half — naming `vector_block_bootstrap` among its guarded entry points — is OWED at the sibling's next touch, not yet stated there, and the contract is satisfied by neither side alone" (lines 94–96). Spot-checked against the sibling: `evaluation-and-comparison/nfr-design/security-design.md` has no occurrence of `vector_block_bootstrap` anywhere — the "OWED, not yet stated there" claim is accurate, not merely asserted.
2. **Sibling's half now stated as OWED at its next touch.** Confirmed, same sentence as above.
3. **Ambiguous "W-5" cross-unit label gone from the live claim.** Confirmed. The two remaining "W-5" occurrences in the file are (a) line 20, this unit's own Sources definition of its own W-5 ("interval, method-parametric") — unambiguous, internal — and (b) lines 98–99, inside the verbatim superseded quotation the correction box preserves ("...already names W-5's path among its guarded entry points"), explicitly labeled superseded and immediately glossed as wrong ("the sibling's artifacts named no such entry point... its own 'W-5' is the G-06 path, not this unit's interval workflow"). No live, unqualified use of the bare cross-unit "W-5" label survives — the Minor finding is resolved.
4. **Superseded text preserved in a dated box.** Confirmed at lines 96–100: `*(Corrected 2026-09-05 at the stage gate, governance Recommendation 5; superseded: "Stated on both sides … the sibling's SD-C-01 already names W-5's path among its guarded entry points" — the sibling's artifacts named no such entry point, its per-entry set being C2/C3/C5/C6, and its own "W-5" is the G-06 path, not this unit's interval workflow.)*`
5. **Negative-control input list includes a mask-mismatched `partition_id` set.** Confirmed at lines 92–93: "...one control per violating input class through this entry point, asserting the raise (stamp-less prediction, unregistered mask, **mask-mismatched `partition_id` set**, receipt-less `DEC` call, transformed-space `ABL-DIFF` frame)."
6. **"Adds nothing to it" delegation sentence now references the sibling's sixth guard.** Confirmed at lines 104–108: the DEC-inheritance sentence is followed by "*(The guard set this delegation relies on now includes the mask-vs-member alignment check — the sibling's formerly open Major, closed 2026-09-05 at the stage gate as its sixth guard, governance Recommendation 1 — so "adds nothing to it" no longer leaves that check homeless.)*" The description ("mask-vs-member alignment check", "sixth guard") is accurate but does not spell the guard's function name (`require_mask_member_alignment`) verbatim — a cosmetic gap only, not a Major: the reference is unambiguous once cross-checked against the sibling.
7. **Sibling cross-check: does SD-C-01's table actually have the sixth guard?** Confirmed. `evaluation-and-comparison/nfr-design/security-design.md` line 50: `` `require_mask_member_alignment` | `FairnessError` | the mask's **recorded** `partition_id` matches every member's — a self-consistent member set scored against a mask built for a different partition **refuses** | W-4's third failure ("wrong mask: member-versus-mask partition disagreement"), W-2 step 1 ``, with its own dated box at lines 52–55 ("Sixth guard added 2026-09-05 at the stage gate on governance Recommendation 1... mask-vs-member alignment check homeless [no longer]"). The sibling's own artifact independently confirms this closes the gap the original Major finding identified. Rec 5 is fully landed.

### Recommendation 6 — verified

Target: `logical-components.md` B2 row.

- B2's row (line 34) now reads: "fixed non-overlapping 24-hour partition over `features-and-splits`' folds/embargo **(PROPOSED reading — the block-resampling scheme is a gate item, Rec 26; §18.3 stop-and-report stands at 3.5)**; boundary-violation raise" — the exact annotation specified.
- Cross-checked against the header banner (line 9: "The block-resampling scheme and the correlation series are proposed to gates, not decided") and the Cross-cutting notes section (line 119: "block-resampling scheme undecided"). All three representations agree — proposed/undecided/PROPOSED reading are the same posture stated three ways, no contradiction. Rec 6 is fully landed.

### Regression check

| Area | Result |
|---|---|
| SD-S-01 byte-pinned hash design (lines 37–67) | Untouched — identical to the prior review's verified text; four canonical-form facts, negative controls, append-safe framing all unchanged. |
| Requirement-coverage table (5 rows, lines 146–152) | Unchanged; all statuses remain verbatim `Pending`; the printed derivation line (154–157) still reads +0/−0 against `security-requirements.md`. |
| Stream assignments | Consistent across both files: primary = block-index draws, child 0 = sensitivity, child 1 = widening comparator (`security-design.md` SD-S-03; `logical-components.md` B1/B3/B5 rows and mermaid diagram). |
| New "satisfied" claims | None found — both repaired passages add qualification and cross-reference, not completion claims; every `Pending`/carried/open marker from the prior iteration is still present verbatim. |
| New contradictions introduced by the repair | None found. The "OWED, not yet stated there" claim was independently verified against the sibling file (no `vector_block_bootstrap` match) rather than taken on faith. |

### Coverage limits

- Sibling spot-check was limited to `evaluation-and-comparison/nfr-design/security-design.md`, the one file this brief permits; its `logical-components.md` (which likely carries the C2/C3/C5/C6 entry-point IDs referenced inside the preserved superseded quotation) was not opened — that reference sits inside a quoted-and-labeled-wrong block, so it did not need independent verification for this pass.
- Did not re-read `business-logic-model.md` or `business-rules.md` in full; verification was scoped to the two named recommendations and the regression items the brief specified.

### Summary

Both governance recommendations (5 and 6) verified as landed, item by item, with the sibling cross-check independently confirming the sixth guard (`require_mask_member_alignment`) exists and the `vector_block_bootstrap` OWED claim is accurate rather than merely asserted. No repair-introduced regression found in the hash design, coverage table, or stream assignments, and no new "satisfied" claim was smuggled in. One cosmetic-only gap remains (the delegation sentence describes rather than names the sixth guard by function name) — Minor, not blocking.

READY
