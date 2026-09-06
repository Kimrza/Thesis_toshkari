# Security Design — `evaluation-and-comparison`

**Unit** `evaluation-and-comparison` (Bolt 9) · **Kind** `library` · **Stage** `nfr-design`

> ## ⚠ NOTHING HERE IS CLAIMED SATISFIED
>
> This is a design. **No module is created, no test is executed, no metric has ever been
> computed.** The environment carries **no Python interpreter**; `configs/` and
> `src/evaluation/` do not exist. **BLK-07 is open**, so the ordering refusal designed in
> § SD-C-02 is **specified and unrunnable today**, exactly as `nfr-requirements` recorded.
> **G-09 is signed (D-31) with its own TE §18.3 preconditions UNMET** — module creation is
> authorised, evidence of passing tests is not implied. G-05 and G-06 remain `Blocked`.
> FR-P1-05-7 stays `Pending` (approved under D-32, never run); FR-P1-05-17 and FR-P1-05-20
> stay `UNTESTED`. TE §18.2's absolute rule stands: **no scientific value is decided here.**

## Sources

- `../nfr-requirements/security-requirements.md` — **SEC-C-01** (one mask, registered once, frozen before access; the machine-enforced ordering, Q1 = A there), **SEC-C-02** (the ordered estimand contract, the two sign mechanisms, the boundary refusals R-104/R-105), **SEC-C-03** (G-06 one-shot, hash-receipt before metrics, the pre-G-05 audit that must not be blocked), **SEC-C-04** (the honesty mechanics as emitted fields and caveats). This design gives each a mechanism; it re-decides none.
- `../nfr-requirements/tech-stack-decisions.md` — **TS-C-01** (sign and weighting are project logic), **TS-C-02** (no bootstrap here), **TS-C-03** (mask identity is a content hash; **the two-clock-domain problem this design resolves at § SD-C-02**), **TS-C-04** (caveat emitted by the producing path), **TS-C-05** (platform posture, the in-Kaggle obligation for G-06).
- `../functional-design/business-logic-model.md` — **W-1**…**W-8**, consumed as the behavioural contract the guards enforce; especially W-1 step 1 (stamp check first), W-2's preconditions, W-5's G-06 graph, W-6's three limbs.
- `../functional-design/business-rules.md` — R-103…R-112.
- `../../governance-guards/functional-design/business-rules.md` — **R-25** (log-then-read access record), **R-28** (one door into the restricted root) — the co-owner surfaces § SD-C-02's half-contract attaches to.
- `nfr-design-questions.md` — **Q1 = A** (causal containment), **Q2 = C** (guard module + negative controls), and the receipted Consolidated Summary Confirmation.
- Absent by scope design (`library` kind): `performance-requirements.md`, `scalability-requirements.md`, `reliability-requirements.md` were not produced at `nfr-requirements`; their assessments live in that stage's Scope note and are not reinvented here.

---

## Scope note

A `library` unit gets `security-design.md` and `logical-components.md` only. "Security" here
is what `nfr-requirements` defined it to be: **fairness and the integrity of the reported
result**. There is no authentication, no user, no network surface, no secret handled by this
unit — credentials stay governed by TE §10 and NFR-SEC-01 at the platform layer, and nothing
in this unit reads or stores one. Reliability's fail-closed posture (refuse rather than
compute the wrong comparison) is realised by the same mechanisms below, as the
`nfr-requirements` Scope note anticipated.

## SD-C-01 — The guard module: six refusals, one failure domain (Q2 = C; sixth added at the gate)

**Design.** All refusal checks (six after the gate's Recommendation-1 addition) live in **one guard module** inside `src/evaluation`
(proposed name `src/evaluation/guards.py`, final naming owed to 3.5):

| Guard | Raises | Enforces | Contract |
|---|---|---|---|
| `require_stamps` | `LeakageError` | non-`None` `partition_id`/`transform_id` on every `Prediction`; `transform_id` agreement | R-105, W-1 step 1 |
| `require_partition_agreement` | `PartitionError` | members agree on `partition_id` | R-92-matched, W-4 |
| `require_registered_mask` | `FairnessError` | mask is registered, frozen, and matches the members' declared set; membership exact (R-106); never pairwise | R-106, R-107, W-1 |
| `require_target_space` | `InverseTransformError` | no transformed-space value at any metric entry point; `ABL-DIFF` inverse-before-metric | R-104, W-3 |
| `require_locked_receipt` | `LockedTestError` | on `DEC` only: hash receipt present, file re-hashes to it, ordering per § SD-C-02 | R-109, W-5 |
| `require_mask_member_alignment` | `FairnessError` | the mask's **recorded** `partition_id` matches every member's — a self-consistent member set scored against a mask built for a different partition **refuses** | W-4's third failure ("wrong mask: member-versus-mask partition disagreement"), W-2 step 1 |

*(Sixth guard added 2026-09-05 at the stage gate on governance Recommendation 1 (= the
architecture review's open Major): W-4 names three distinguishable failures and the five-guard
table implemented two — members-vs-members agreement and set membership — leaving the
mask-vs-member alignment check homeless. Its negative control joins the per-entry set: an
agreeing-but-mask-mismatched `partition_id` member set pushed through each entry point must
raise. The gate's Request Changes lifted the terminal receipt, per the recorded
cheap-release lesson.)*

**Entry points call guards; controls prove they do.** Every public entry point — mask
construction (W-1), the estimand pipeline (W-2), the G-06 path (W-5), the honesty emission
(W-6) — calls the guard module before touching a row. The **negative-control set** (Q2 = C's
addition) closes the fail-open gap a guard module alone leaves: for **each public entry
point**, one control pushes a violating input through that entry point and asserts the raise —
a stamp-less `Prediction` into W-1, a mismatched-partition pair into W-2, an un-inverted
`ABL-DIFF` frame into any metric, a receipt-less `DEC` call into W-5. The guard being correct
is proven once; the guard being **invoked** is proven per entry point. This is WS-10's
methodology applied to this unit's own boundary, and it is the design answer to the drift
failure `GOV-2026-08-28-FD-01` Recommendation 8 caught (R-105 raising the wrong exception
while claiming to mirror R-92): one copy of the logic, so there is nothing to drift.

**Distinguishability is part of the design.** The guards' exceptions are distinct
diagnoses; a generic refusal would hide which contract failed. All are (or are proposed
to `foundation` as) members of R-01's `IntegrityError` hierarchy — `PartitionError` is already
its fifteenth member; this design adds **no new exception type** (the sixth guard reuses
`FairnessError`, exactly as W-4 assigns it).

## SD-C-02 — The ordering check is causal containment, not clock comparison (Q1 = A)

**The problem, as raised.** SEC-C-01 requires the comparison-wide mask to be **frozen before**
the locked test is accessed, machine-enforced. `nfr-requirements` designed that as a
timestamp comparison and then recorded its own weakness: the mask registry and the access log
may be written by **different hosts** (on Kaggle: unmeasured durability, no stated skew
bound), so "registration timestamp precedes access timestamp" compares two clocks with no
bound relating them.

**Design (Q1 = A): the access record contains the registration evidence.** At locked-test
access time, the access path reads the mask registry and writes into the access record:

- `mask_bundle_ids` — the `mask_id`s of the frozen bundle found at access time, and
- `mask_registry_hash` — the SHA-256 content hash of the **frozen bundle's manifest** (the
  write-once artifact enumerating the bundle's `mask_id`s and content hashes) at that moment.
  *(Hash target narrowed 2026-09-05 at the stage gate, governance Recommendation 8;
  superseded: "the registry artifact's SHA-256 content hash" — the registry legitimately
  grows (three declared sets; later registrations), so a whole-registry hash would make a
  correct access record fail post-hoc re-verification after any append: a false-refusal
  channel at the one unrepeatable event. The bundle manifest is write-once per freeze, so
  its hash is append-immune; this also resolves the [Q1] registry-split note below in the
  same direction.)*

Ordering is then proven by **containment**: the access record *contains* evidence derived
from the completed registration, so registration necessarily preceded the access — on any
clocks, across any hosts. A mask registered *after* the access cannot appear in the access
record, and a record without the two fields **refuses** (the access path fails closed, not
the audit after the fact). Verification is possible post hoc from the two artifacts alone:
re-hash the frozen bundle's manifest, compare with the recorded hash, check the scored
mask's `mask_id` is in `mask_bundle_ids`.

**What this dissolves and what it costs.** No skew bound is invented (the C option's
convenience constant), no same-host operational constraint is added (the B option's spurious
failure mode). The cost: the access path gains one registry read, and the access record gains
two fields. The **false-refusal risk at G-06 drops to zero from clock behaviour** — the one
event that can never be re-run no longer depends on two clocks agreeing.

**The half-contract, stated in both directions.** The access record is
**`governance-guards`'** (R-25 log-then-read; R-28's one door). **This unit's half:**
`require_locked_receipt` refuses a `DEC` metric unless the access record carries the two
fields and the scored mask's `mask_id` ∈ `mask_bundle_ids` with a verifying registry hash.
**The co-owner's half (stated, not declared satisfied):** `open_restricted` populates the two
fields at access time. Same pattern as the prediction-hash receipt (produced by
`models-and-baselines`, enforced here) — **satisfied by neither side alone**. It remains
**unrunnable while BLK-07 is open**: `open_restricted` does not exist, and this design
attaches the refusal to a surface that is still a specification.

**What it does not touch.** The pre-G-05 **coverage audit** (purpose `"coverage_audit"`,
`inventory-and-registry`'s, performance-blind, Vision §8.3) is a different event; nothing in
this check applies to it, and a design that blocked it would breach Vision §8.3. The
timestamp fields themselves stay in both artifacts — containment supersedes the *comparison*,
not the recording.

## SD-C-03 — The G-06 chokepoint, receipt-before-metric, and the one-shot posture

**Design.** `require_locked_receipt` composes three checks at every `DEC` metric entry point,
in order: (1) the prediction-hash receipt exists in `foundation`'s registry row and the
prediction file re-hashes to it (write-once detection, FR-P1-05-12's criterion); (2) the
§ SD-C-02 containment check passes; (3) the scored range is exactly the D-28 window —
2–31 December 2022, 30 days, first 24 h excluded and counted — asserted via the mask's
scored-window statement, so a 1 December row raises. Failure of any limb is `LockedTestError`
naming the limb. Every access sets `locked_test_accessed = true` in the registry (Vision
§8.3); any post-access test-driven pipeline change is labelled exploratory. No
practical-relevance threshold is introduced or reinterpreted after opening (PC-09) — this
unit computes the estimand and emits fields; thresholds are not its to state.

## SD-C-04 — Honesty mechanics: emitted, not remembered

**Design.** W-6's three limbs become properties of the producing path: the completeness
refusal (a results artifact missing any declared member's metric is not emitted —
`FairnessError`), the **`beats_model` trigger field** per benchmark (FR-P1-05-20's
abstract-level disclosure downstream becomes a field comparison), and the **emitted caveats**
— the spatial-representativeness sentence on every serialized IRI/GIM comparison (Vision
§6.6), the GIM overlap disclosure, and the Phase 2 not-independent-blind-test statement
carried as an artifact field for the abstract-level interpretation.

**The GIM overlap disclosure, fail-closed and clock-free** *(amended 2026-09-05 at the stage
gate on governance Recommendation 3; superseded: "keyed to a GIM comparison existing with a
registered audit result whose timestamp precedes comparator generation" — a cross-host
timestamp comparison of exactly the class § SD-C-02 rejects, with the no-audit case unstated)*:
a GIM comparison whose comparator generation finds **no registered overlap-audit result**
**refuses** (`FairnessError`) — the disclosure cannot be silently skipped; and ordering is
proven by **containment**, not clocks — the comparator artifact records the audit result's
ID and content hash found at generation time, so the audit necessarily preceded the
comparator on any clocks, the same idiom as § SD-C-02. Negative control: a GIM comparison
emitted with an absent audit result must raise. The sign convention travels as data (`benchmark_minus_model`,
`equal_station` on every `EstimandResult`); the reversed-sign negative control on the
producer stays in the test plan (W-2's controls). **The primary results table is
`regimes-diagnostics-reporting`'s**; this unit emits values, trigger fields, and caveats, and
discharges nothing that table owes.

---

## Requirement coverage

| Requirement | Design section | Acceptance row | Status |
|---|---|---|---|
| FR-P1-04-7 | SD-C-01 (`require_registered_mask`), SD-C-03 | WS-16, TA-11 | `Pending` |
| FR-P1-05-7 | SD-C-01, SD-C-04 (sign mechanisms) | `Pending` — approved under D-32, never run | not evidence |
| FR-P1-05-17 | SD-C-02 | **NO ROW — `UNTESTED`**; the containment mechanism is this design's answer to how it will be enforceable | not evidence |
| FR-P1-05-12 | SD-C-03 limb 1 | **WS-18, TA-18** — rows owned by `features-and-splits` and `governance-guards` | `Pending` — the write-once and hash-before-metric criterion this unit enforces *(cells restored to upstream verbatim 2026-09-05, governance Recommendation 4; superseded: Acceptance `UNTESTED`, Status `not evidence` — a substitution that severed the trace to two existing acceptance rows)* |
| FR-P1-05-9 | SD-C-04 (completeness limb) | TA-20 — row owned by `regimes-diagnostics-reporting` | `Pending` |
| FR-P1-05-20 | SD-C-04 (`beats_model` field) | **NO ROW — `UNTESTED`** | not evidence |
| NFR-FAIR-01 | SD-C-01, SD-C-02 | WS-16, TA-11 | `Pending` |
| NFR-IRI-01 | SD-C-04 (evaluation-time join, caveats) | WS-10, TA-07 | `Pending` — test written upstream, unexecuted |

**Derived and printed**: 4 design sections (SD-C-01…SD-C-04); **8** coverage rows, matching
`security-requirements.md`'s 8 exactly (same ID set, set-differenced: +0 / −0); **0** rows
claimed satisfied; **0** new exception types; **0** scientific values decided.

## Assumptions & Open Questions

- **[Q1]** The containment design adds **two fields to `governance-guards`' access record**
  (`mask_bundle_ids`, `mask_registry_hash`). That is a **half-contract**: stated here,
  populated there, **satisfied by neither side alone**, and owed to `governance-guards`'
  attention at its next touch. Unrunnable while **BLK-07** is open.
- **[Q1]** The hash target is the **frozen bundle's write-once manifest** (Recommendation 8's
  amendment above), so a registry split or later append no longer threatens the check; owed
  to 3.5: the manifest is write-once per freeze, and the registration path that writes it.
- **[Q2]** Guard-module naming (`guards.py`) and the exact public-entry-point enumeration are
  **proposed, owed to 3.5**. The design fixes the shape (one module, per-entry negative
  controls), not the file layout.
- **Carried** — the prediction-hash receipt two-half contract (`models-and-baselines`
  produces, this unit enforces); BLK-08's half A/half B with `features-and-splits`; the
  primary results table is `regimes-diagnostics-reporting`'s; WS-13's evidence question stays
  open (R-111).
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or
  claims a gate, acceptance row, or test as discharged.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-04T22:47:43Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `security-design.md` § SD-C-01 table (lines 43-49); `logical-components.md` C1 row (line 32) | **One of R-105/W-4's three distinguishable `FairnessError`-class failures has no guard.** `business-logic-model.md` W-4's `RAISES` block names three distinct triggers: `LeakageError` (absent stamp/`transform_id` disagreement), `PartitionError` (`partition_id` mismatch between members), and `FairnessError` for **"wrong mask: member-versus-mask partition disagreement"** — i.e. a `Prediction`'s `partition_id` failing to match the *mask's own recorded* `partition_id` (this is also W-2 step 1's stated precondition: "both predictions pass R-105's stamp check **against the mask's recorded stamps**"). SD-C-01's five guards do not cover this case: `require_stamps` and `require_partition_agreement` only compare `Prediction`s to each other (contracts R-105/W-1 step 1 and "R-92-matched"/W-4), and `require_registered_mask`'s stated contract is R-106/R-107 — comparison-**set membership** ("matches the members' declared set; membership exact") — a different check from partition-stamp alignment between a mask and the predictions scored against it. A run where every member shares one (wrong) `partition_id` that disagrees with the mask's recorded `partition_id` would pass `require_partition_agreement` (members agree with each other) and `require_registered_mask` (set membership is exact) and reach the metric — exactly the "compute the wrong comparison instead of nothing" failure this unit's whole design exists to close (§ "unit-level posture" in `logical-components.md`, line 100-102). | Add the mask-vs-member partition-stamp check to `require_registered_mask` (or a sixth guard) explicitly, citing W-2 step 1 and W-4's `FairnessError` trigger by name, and add the corresponding negative control (a `Prediction` set sharing an agreeing but mask-mismatched `partition_id`) to the Q2=C negative-control set. |
| 2 | Minor | `security-design.md` § SD-C-01 (line 57-58) | Present-tense over-claim: "The guard being correct is proven once; the guard being invoked is proven per entry point" states an accomplished fact, but `logical-components.md` line 40 records the test module as "specified (unwritten)" and this artifact's own banner states no test is executed and no interpreter exists. Nothing is "proven" yet — the sentence describes an intended design property. | Reword to "...is designed to be proven once..." / "...would be proven per entry point once the negative-control set exists," consistent with the artifact's own status-honesty banner. |
| 3 | Minor | `security-design.md` § SD-C-02 (lines 77-89) | The containment mechanism specifies a read-then-write sequence (access path reads the mask registry, then writes the two fields into the access record) with no stated atomicity/locking guarantee. A registration landing concurrently between the read and the access record's write, or a read racing a partially-committed registry write, is not addressed — unlike the design's other acknowledged gaps (e.g. the registry-hash target if the registry ever splits, explicitly flagged as "a note for 3.5" at line 168-169), this race is not flagged as owed to 3.5 anywhere in either artifact. | Either state that mask registration and locked-test access are mutually exclusive by construction (e.g. serialized through a single process/lock), or add this as an explicit open item owed to 3.5/`governance-guards`, matching the treatment given the registry-split case. |

### What was verified

- **Q1 = A causal containment (SD-C-02) is sound and does not smuggle a clock comparison back in.** The two fields (`mask_bundle_ids`, `mask_registry_hash`) are read by the access path itself as an in-process step before the access record is written, converting a cross-host clock comparison into a same-process happens-before relation; no timestamp comparison appears anywhere in § SD-C-02 or SD-C-03, and § SD-C-02 explicitly states "the timestamp fields themselves stay in both artifacts — containment supersedes the comparison, not the recording," consistent with TS-C-03's requirement. A mask registered after the access genuinely cannot appear in a record written from an earlier registry read.
- **The half-contract with `governance-guards` is stated in both directions and not declared satisfied**, in both `security-design.md` (lines 97-105, 163-166) and `logical-components.md` (lines 109, 128-130) — consistently worded, consistently unrunnable-while-BLK-07-is-open.
- **Requirement-coverage completeness (task #3): set-difference is empty.** Printed IDs in `security-design.md`'s coverage table (lines 148-155): FR-P1-04-7, FR-P1-05-7, FR-P1-05-17, FR-P1-05-12, FR-P1-05-9, FR-P1-05-20, NFR-FAIR-01, NFR-IRI-01 — **8 IDs**. `security-requirements.md`'s 8-row set (lines 200-207): the identical 8 IDs. Set difference: **+0 / −0**, matching the artifact's own printed claim (line 157-159).
- **Status honesty (task #4), except finding #2 above**: no claim of a satisfied gate, a run metric, a discharged test, or a resolved BLK item was found. BLK-07 open (lines 9, 104, 166), BLK-08 open (`logical-components.md` line 134-135), G-09 signed with TE §18.3 preconditions unmet (line 11), D-28's 30-day window (line 118-119) all stated consistently with the upstream artifacts.
- **Field-name consistency (task #5)**: `mask_bundle_ids` and `mask_registry_hash` are named identically in both artifacts (`security-design.md` lines 80-81, 163-164; `logical-components.md` line 109, 128).
- **Two of the three requirement-guard/exception mappings in SD-C-01 are correct**: `require_stamps` → `LeakageError` and `require_partition_agreement` → `PartitionError` both match W-4's `RAISES` table exactly.
- **Sensors**: both artifacts carry well more than 2 H2 headings, reference all three consumed artifacts by name in their Sources sections, and both explicitly state the absence of `performance-requirements.md`/`scalability-requirements.md`/`reliability-requirements.md` (`security-design.md` line 24, `logical-components.md` line 17).

### Coverage limits

- The instructed spot-check of `governance-guards/functional-design/business-rules.md` (R-25/R-28) was attempted via Read and Grep and was **blocked by the `aidlc-reviewer-scope.ts` hook**, which refused the cross-unit path outright despite the dispatch brief naming it as a permitted exception. R-25/R-28's content is therefore taken on the strength of this unit's own citations (`security-design.md` lines 22, 98; `security-requirements.md` line 27) and was not independently re-verified against the governance-guards artifact itself.
- Did not re-open `models-and-baselines`, `features-and-splits`, or `statistical-inference` artifacts — all claims about those units' owned halves (the prediction-hash receipt, `load_inverse`, the bootstrap) are taken at face value as stated, unrunnable-and-unsatisfied obligations, consistent with how the artifacts themselves describe them.
- Did not independently verify R-92's exact wording (cited as "R-92-matched" in the guard table) beyond what `business-logic-model.md` W-4 already quotes within this unit's own consumed artifact; R-92 itself lives in `models-and-baselines` and was not opened.
- `nfr-design-questions.md` Q1/Q2 answers and the Consolidated Summary Confirmation were read and match the design's stated rationale for both decisions.

### Summary

The design's central architectural move — replacing a cross-host clock comparison with causal containment at SD-C-02 — is sound, its half-contract with `governance-guards` is honestly stated in both directions, and requirement coverage is complete against the upstream 8-row set with a correctly printed set-difference. One Major gap survives adversarial scrutiny: the guard-module design does not assign an explicit check to the mask-versus-member partition-stamp mismatch that W-4's own `RAISES` table names as a distinct `FairnessError` trigger, leaving one of the unit's three documented `FairnessError` causes without a corresponding guard in SD-C-01's table. At 1 Major and 2 Minor findings, this does not cross the ≤2-Major READY threshold, but the Major should be closed before 3.5 builds from this design, since it is exactly the class of gap (a named failure mode with no assigned enforcement point) that could let a wrong comparison compute silently rather than refuse.

READY

## Review — 2026-09-05 post-gate repair verification

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T07:46:46Z
**Iteration:** 1 (fresh budget after gate rejection)

### Per-recommendation verification

**Recommendation 1 (sixth guard, `require_mask_member_alignment`) — VERIFIED, landed correctly.**
The guard appears as the sixth row of SD-C-01's table (`security-design.md` line 50), raising
`FairnessError`, enforcing "the mask's recorded `partition_id` matches every member's," cited
against **W-4's third failure** ("wrong mask: member-versus-mask partition disagreement") and
**W-2 step 1**. Both citations check out against the actual upstream text: `business-logic-model.md`
W-4's `RAISES` block (line 281) names exactly `FairnessError (wrong mask: member-versus-mask
partition disagreement)`, and W-2's ordered contract step 1 (line 166-167) states "both
predictions pass R-105's stamp check **against the mask's recorded stamps**" — the precondition
the new guard now enforces. This closes the exact gap the prior iteration's Major found: a
self-consistent member set sharing one wrong `partition_id` that disagrees with the mask's
recorded `partition_id` previously passed both `require_partition_agreement` (members agree with
each other) and `require_registered_mask` (set membership exact) and would have reached the
metric unguarded. It no longer can. Section heading and count representations were swept
correctly in both numeral and spelled-out form: `security-design.md` reads "six refusals" (line
38 heading), "six after the gate's Recommendation-1 addition" (line 40), "Sixth guard added"
(line 52), "the sixth guard reuses `FairnessError`" (line 75); `logical-components.md` C1's row
(line 32) and its "six mandated §12 packages" phrase (line 26, unrelated count, not a regression)
both read six. The one surviving "five" (`security-design.md` line 53, "the five-guard table
implemented two") is inside the dated amendment box narrating what the *prior* table looked like
before the gate — a legitimate historical reference, not a stale current-state claim, consistent
with this project's non-destructive-correction convention. `logical-components.md` line 108's
"five exposed values" is an unrelated count (mask-registry values exposed to
`regimes-diagnostics-reporting`), not the guard count — not a regression. The new guard reuses
`FairnessError` rather than adding a type, correctly matching W-4's assignment and the "0 new
exception types" claim in the coverage-count paragraph (line 186). Negative control for the new
guard is named ("an agreeing-but-mask-mismatched `partition_id` member set pushed through each
entry point must raise," line 55-58).

**Recommendation 3 (GIM overlap disclosure, fail-closed) — VERIFIED, landed correctly.**
SD-C-04's amended paragraph (line 154-167) replaces the prior timestamp-comparison design with a
fail-closed refusal: "a GIM comparison whose comparator generation finds **no registered
overlap-audit result** **refuses** (`FairnessError`)," and orders by containment — "the comparator
artifact records the audit result's ID and content hash found at generation time, so the audit
necessarily preceded the comparator on any clocks, the same idiom as § SD-C-02." This is the
correct application of the same containment idiom SD-C-02 already established, closing the
absent-audit-case gap the superseded text left open. The superseded text is preserved verbatim in
the italicized amendment box ("keyed to a GIM comparison existing with a registered audit result
whose timestamp precedes comparator generation... with the no-audit case unstated"). A negative
control is stated ("a GIM comparison emitted with an absent audit result must raise").

**Recommendation 4 (FR-P1-05-12 coverage row restored) — VERIFIED, landed correctly.**
The coverage-table row (`security-design.md` line 178) now reads Acceptance
"**WS-18, TA-18** — rows owned by `features-and-splits` and `governance-guards`" and Status
"`Pending` — the write-once and hash-before-metric criterion this unit enforces" — checked
character-for-character against `../nfr-requirements/security-requirements.md` line 204 and found
to match verbatim in both cells. The dated amendment box correctly names the prior substitution
("Acceptance `UNTESTED`, Status `not evidence`") as superseded and preserves it. The other seven
rows (FR-P1-04-7, FR-P1-05-7, FR-P1-05-17, FR-P1-05-9, FR-P1-05-20, NFR-FAIR-01, NFR-IRI-01) were
diffed cell-by-cell against the same upstream table and found unregressed — identical Acceptance
and Status text in both artifacts. The coverage-count paragraph's claim of "8 coverage rows,
matching `security-requirements.md`'s 8 exactly (same ID set, set-differenced: +0/−0)" was
independently re-derived by listing both ID sets and remains correct.

**Recommendation 8 (mask_registry_hash target narrowed to the frozen bundle's manifest) —
VERIFIED, landed correctly.** SD-C-02's bullet (line 90-99) now targets "the SHA-256 content hash
of the **frozen bundle's manifest** (the write-once artifact enumerating the bundle's `mask_id`s
and content hashes)," with the superseded whole-registry-hash text preserved in the dated
amendment box along with its stated rationale (append-immunity vs. the registry's legitimate
growth). The post-hoc verification sentence (line 105-107 — "re-hash the frozen bundle's
manifest, compare with the recorded hash, check the scored mask's `mask_id` is in
`mask_bundle_ids`") is consistent with the narrowed target, not left describing the old
whole-registry scheme. The `[Q1]` assumption block (line 194-196) was updated in the same
direction, stating the narrowing resolves the registry-split note "in the same direction." Field
names are unchanged in both artifacts: `mask_bundle_ids` and `mask_registry_hash` appear
identically in `security-design.md` (lines 90-91, 115-118, 163-164, 190-193) and
`logical-components.md` (lines 109, 128-130) — sibling references (e.g. `governance-guards`'
owed half, `foundation`'s registry rows) stay valid because nothing that names these fields by
name needed to change.

### Regression check

- Count/status representations agree across banner, tables, and derivations in both files: banner
  states BLK-07 open, G-09 signed with §18.3 preconditions unmet, FR-P1-05-7/17/20 status
  (unchanged from before the repair, correctly untouched by Recommendations 1/3/4/8 since none of
  them concern those three IDs).
- No newly claimed satisfaction: "0 rows claimed satisfied; 0 new exception types; 0 scientific
  values decided" (line 186) still holds on inspection — none of the four repairs introduces a
  claim of a passing test, a computed metric, or a discharged gate.
- BLK-07 (line 9, 122, 193, 201) and BLK-08 (`logical-components.md` line 134-135, referenced via
  C4/BLK-08 in `security-design.md`) remain open in both artifacts.
- The pre-G-05 coverage-audit carve-out (SD-C-02, "What it does not touch," lines 125-129) is
  untouched by the Recommendation-3 and Recommendation-8 edits, which are in different sections
  (SD-C-04 and SD-C-02's hash-target bullet respectively) and do not overlap it.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Minor | `security-design.md` § SD-C-01 (lines 63-67) | The illustrative negative-control-example sentence ("a stamp-less `Prediction` into W-1, a mismatched-partition pair into W-2, an un-inverted `ABL-DIFF` frame into any metric, a receipt-less `DEC` call into W-5") was not extended to include an example for the new sixth guard, even though the sixth guard's own negative control is correctly stated two paragraphs earlier (line 55-58). This list was already non-exhaustive before the repair (it never listed all five original guards' controls either), so this is pre-existing illustrative style rather than a repair-introduced gap, but a reader skimming only this sentence could miss that a sixth control now exists. | Add the sixth guard's negative-control example to this sentence for a complete at-a-glance list, or add a forward pointer to line 55-58. |

Two pre-existing Minor findings from the prior iteration (the "proven" present-tense over-claim at
line 60ish, and the SD-C-02 read-then-write race condition with no stated atomicity guarantee)
were not in the scope of Recommendations 1/3/4/8 and remain open, unaddressed and unregressed —
correctly out of scope for this pass.

### Summary

All four gate-directed recommendations (1, 3, 4, 8) verified as correctly and completely landed
against their respective upstream sources (W-4/W-2 for the sixth guard, the containment idiom's
own prior art for the GIM fix, `security-requirements.md`'s verbatim cells for FR-P1-05-12, and
internal consistency for the narrowed hash target), with superseded text preserved in every case
per this project's non-destructive-correction convention and no repair-introduced regression found
in status claims, BLK item states, field names, or the pre-G-05 audit carve-out. One new Minor
(non-blocking, pre-existing illustrative-list style) is the only finding.

READY
