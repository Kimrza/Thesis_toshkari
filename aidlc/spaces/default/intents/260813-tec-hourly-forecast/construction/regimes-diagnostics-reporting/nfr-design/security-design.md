# Security Design — `regimes-diagnostics-reporting`

**Unit** `regimes-diagnostics-reporting` (Bolt 11) · **Kind** `library` · **Stage** `nfr-design`

> ## ⚠ NOTHING HERE IS CLAIMED SATISFIED — AND THIS UNIT IS THE LAST SURFACE BEFORE THE THESIS
>
> This is a design. **No module exists, no results table has ever been produced, no test has
> run.** No Python interpreter exists in this environment; `configs/` does not exist.
> **§ SEC-R-02's two consumer refusals still have no producing half** — both will fail on
> every input until `evaluation-and-comparison`'s field emission and `target-standardization`'s
> caveat field land; that is the mechanism working. **Five acceptance rows are `Pending`
> (D-32, never run) and four requirements are rowless** (FR-P1-05-14, -15, -3, -21). TA-16,
> TA-19, TA-20 and WS-19 are undischarged. **G-09 is signed (D-31) with preconditions
> UNMET**; G-05/G-06 remain `Blocked`; BLK-03/04/08/09 stay open exit conditions.
> TE §18.2's absolute rule stands: **no scientific value is decided here.**

## Sources

- `../nfr-requirements/security-requirements.md` — **SEC-R-01** (the primary table's honesty refusals and `beats_model`), **SEC-R-02** (the two consumer half-contracts completed as refusals), **SEC-R-03** (the diagnostics quarantine extended to citation), **SEC-R-04** (December-blind reporting, one counting path, honest demotion, notebooks). This design gives each a mechanism; it re-decides none.
- `../nfr-requirements/tech-stack-decisions.md` — **TS-R-01** (the table is code), **TS-R-02** (presentation-only by signature, with the split-guarantee caveat in the body), **TS-R-03** (one classifier, thresholds from config), **TS-R-04** (the checklist's stdlib presence checks and their stated limits), TS-R-05 as carried.
- `../functional-design/business-logic-model.md` — **W-1**…**W-10**, especially W-2 (the December channel), W-3 (the table path and its provenance block), W-4 (the registered `ConclusionSurfaceArtifact`, fail-closed when absent), W-5 (the breakdown family), W-7 (`plots.py`), W-8 (the quarantine).
- `../functional-design/business-rules.md` — R-123…R-132.
- `../../evaluation-and-comparison/nfr-design/security-design.md` — **SD-C-01** (the shared metric-entry guard module — the boundary split in § SD-R-01 is defined against it). Cross-unit design contract, stated as such. *(Citation corrected 2026-09-05 on adversarial finding 3, Minor; superseded: "§ SD-R-02".)*
- `../../../inception/requirements-analysis/requirements.md` — the 19 IDs the upstream coverage table carries (see § Requirement coverage).
- `nfr-design-questions.md` — **Q1 = A** (the registered conclusion surface owns the location enumeration), **Q2 = A** (one render-guard set), and the receipted Consolidated Summary Confirmation.
- Absent by scope design (`library` kind): `performance-requirements.md`, `scalability-requirements.md`, `reliability-requirements.md` were not produced at `nfr-requirements`; that stage's Scope note carries the assessments and this design does not reinvent them.

---

## Scope note

"Security" here is what `nfr-requirements` fixed: **the honesty of what is reported**. This
unit is the last surface before the thesis; every upstream containment rule is defeated if a
quarantined or unqualified value renders here as a finding. No credential, user, or network
surface exists. Reliability's refuse-rather-than-mislead posture is realised by the
render-guard set below.

## SD-R-01 — The render-guard set: one home for every rendering refusal (Q2 = A)

**Design.** All rendering refusals live in **one local guard component** in this unit's
reporting module (proposed name `src/evaluation/report_guards.py`, final naming owed to
3.5). Every producing path calls it **before emitting**:

| Guard | Refuses | Enforces | Called by |
|---|---|---|---|
| `require_estimand_fields` | an estimand value without `benchmark_minus_model` orientation + `equal_station` weighting | SEC-R-02 half 1 (completing `evaluation-and-comparison` § SEC-C-02) | W-3 table, W-5 breakdowns |
| `require_lineage_caveat` | any IRI/GIM comparison without the lineage caveat (location-sampled gridded VTEC; geometry/sampling artefact statement, Vision §6.6) — for a figure, "present" means the caveat field rendered into the caption or figure metadata | SEC-R-02 half 2 (completing `target-standardization` § SEC-T-02); TEC-06's "wherever reported" | W-3, W-5, **W-7** |
| `require_units` | a value whose units assertion is absent or non-TECU where TECU is required | R-125's units check; BLK-08's reach made checked not silent | W-3, W-5, W-6 |
| `require_complete_members` | a table missing any declared comparison-set member's metric | SEC-R-01 co-reporting; FR-P1-05-9 | W-3 |
| `require_d17_bound` | a breakdown outside the D-17 sixteen-field bound | R-127's inventory refusal | W-5 |
| `require_registered_surface` | emission of a conclusion-bearing artifact not registered in the `ConclusionSurfaceArtifact` | Q1 = A (§ SD-R-03) | W-3, W-5, W-7, W-4 |
| `require_beats_model` | a table row missing its per-benchmark `beats_model` field | R-125 control (9); FR-P1-05-20's trigger printed, never judged | W-3 |
| `require_provenance_block` | a table **or breakdown artifact** missing any of the five provenance values (`mask_id`, `feature_set_id`, per-station surviving row counts, exclusion counts, D-28 scored-window statement), or a scored-window statement disagreeing with the registered mask's | R-125 controls (32) and (33) — control (32)'s own wording is "table **or breakdown artifact**"; R-127 ("the same block on every breakdown", `business-rules.md:908`); Vision §8.9; D-28 | W-3, **W-5** |
| `require_derived_label` | a derived quantity (the §5.5 percentage RMSE reduction) rendered without its `derived: true` label | R-127 control (34); Vision §9.5 required result 2 | W-5 |
| `require_driver_caveat` | a per-station breakdown emitted without the standing TC-12 driver-identity caveat | R-127 control (38); the caveat emitted by the producing path | W-5 |

*(Four guards added 2026-09-05 on adversarial finding 1, Critical; superseded: a 6-row
table. The five render-time negative controls R-125/(9), (32), (33) and R-127/(34), (38)
mandate had no assigned guard while the section title claimed "one home for every rendering
refusal" — the same gap class the sibling's then-open Major named, reproduced at wider scope.
Controls (32) and (33) share `require_provenance_block`: one guard, two assertions —
presence, then agreement. **Swept again 2026-09-05 at the stage gate, governance
Recommendations 2 and 9:** `require_provenance_block` widened to W-5 per control (32)'s own
"table or breakdown artifact" wording — the terminal review's finding 4, now applied on the
gate's Request-Changes ruling — with a W-5 negative control (breakdown missing a provenance
field; breakdown scored-window statement disagreeing with the mask's) joining the per-entry
set; and `require_lineage_caveat` widened to W-7 with "present" defined for figures.)*

**The boundary split, stated so no check is homeless or double-owned.** **Metric-entry
checks** (stamps, registered mask, DEC hash receipt, target space) are the **sibling's
shared guard module** (`evaluation-and-comparison` SD-C-01) and run where metrics are
computed — this unit consumes already-checked fields and does not re-run them. **Rendering
checks** (the table above) are **this unit's render-guard set** and run where values become
reader-visible text, tables and figures — a boundary the shared module does not own. One
copy each side; nothing checked twice, nothing checked nowhere. The one known gap on the
sibling's side — its formerly open Major, no guard checking mask-vs-member partition
alignment — **was closed at the stage gate on 2026-09-05** (governance Recommendation 1: the
sibling's sixth guard, `require_mask_member_alignment`); this unit correctly never papered
over it with a rendering check, because a rendering check runs too late to catch it.

**Per-entry negative controls (Q2 = A).** For each producing path (W-3 table, W-5
breakdowns, W-7 plots manifest, W-4 checklist emission), one control pushes a violating
input through that path and asserts the raise — a field-less estimand into W-3, a
caveat-less GIM comparison into W-5, an unregistered artifact through W-7, an out-of-bound
breakdown into W-5. The guard being correct is proven once; the guard being **invoked** is
proven per path. Same WS-10 methodology as the siblings; controls live in
`tests/test_regimes_and_reporting.py` (R-132's one home).

**Fail-closed cost, restated.** Both SEC-R-02 refusals fail on **every** input today — the
producing halves are unbuilt. First failure is the mechanism working; recorded upstream and
carried here unchanged.

## SD-R-02 — The consumer refusals, as mechanisms with named fields

**Design.** The two half-contracts complete at the render guard, on **fields, not
judgement**: `require_estimand_fields` reads the `EstimandResult`'s recorded orientation and
weighting (emitted by `evaluation-and-comparison` W-2 step 5 — producer half, stated there);
`require_lineage_caveat` reads the caveat field the comparison-producing path emits (R-110's
pattern; `target-standardization`'s caveat field is its half). The `beats_model` disclosure
prints from the computed field, never from an author noticing (SEC-R-01). **Neither
half-contract is declared satisfied**: this design names the fields it refuses without, and
the producing units own emitting them.

**December discipline (SEC-R-04, W-2).** The classifier is December-blind by signature;
regime **performance** breakdowns are post-receipt by construction; the storm count reaching
any report is **read from the registered pre-G-05 audit artifact** (`inventory-and-registry`'s
performance-blind read) — never recomputed here (one counting path, R-123). Post-access runs
are labelled exploratory; practical relevance stays frozen and demoted honestly (R-128).

## SD-R-03 — The conclusion surface owns the location enumeration (Q1 = A)

**The gap, as raised.** "Which locations count as thesis-level is not fixed anywhere, and a
location added later is not automatically inspected."

**Design.** A location is thesis-level **iff registered in the `ConclusionSurfaceArtifact`**
(W-4's registered checked-text subject, already fail-closed when absent). Three consequences:

1. **The checklist inspects exactly the registered set** — its enumeration can no longer go
   stale independently of the surface it checks, because they are the same artifact.
2. **Registration is enforced at the producing path**: emitting a conclusion-bearing
   artifact (table, breakdown, figure set, notebook conclusion cell) without registering it
   is a `require_registered_surface` refusal — the same emit-from-the-producing-path pattern
   R-110/R-60 use, so the registry grows with the surface automatically.
3. **The citation check (SEC-R-03, Q2 = A upstream) inspects the same registered set** — the
   quarantined-diagnostic label co-occurrence check runs at every registered location.

**The residual, stated rather than absorbed.** Hand-authored thesis prose written outside
the pipeline never passes a producing path, so it cannot be forced to register — the
registry bounds what the pipeline produces, not what a human types elsewhere. This is the
same residual SEC-R-03 already states for indirectly phrased citations: **narrowed, not
closed**, and no artifact may describe the checklist as fully enforced. The gate and the
supervisor remain the check on unregistered prose.

## SD-R-04 — Quarantine and notebooks, as designed mechanisms

**Diagnostics quarantine (SEC-R-03, R-130).** Dst artifacts carry grade labels and never
cross the lane into features, tolerances, or G-05 regime counts; the RF-importance figure
renders only from metadata carrying `authoritative = false` (produced by
`models-and-baselines` R-100), and the render guard refuses an RF figure whose metadata
lacks the flag — the citation check then verifies the label co-occurs at every registered
location that cites it. The widening comparator's numbers are never serialized as a reported
interval (R-120's quarantine, enforced at `require_registered_surface`: the comparator has
no registered surface to render to).

**Notebooks (R-131, TE §14).** Each of the four analysis notebooks opens with the
declaration helper (dataset version, code commit, config IDs, artifact IDs), imports from
`src/`, reads versioned artifacts, holds no only-copy of governed logic, and stops with a
clear message on missing inputs. Notebook conclusion cells are registered surfaces (Q1 = A),
so the checklist inspects them like any other location.

---

## Requirement coverage

The upstream table's 19 IDs, mapped to this design's sections. Statuses are the upstream
artifact's; nothing is upgraded here.

| Requirement | Design section | Status (upstream) |
|---|---|---|
| REQ-ENG-12 | SD-R-04 (notebooks) | `Pending` |
| FR-P1-05-9 | SD-R-01 (`require_complete_members`), SD-R-02 | `Pending` |
| FR-P1-05-10 | SD-R-02 (December discipline) | `Pending` |
| FR-P1-05-11 | SD-R-01 (W-7 path), SD-R-04 | `Pending` |
| FR-P1-05-14 | SD-R-02 (frozen relevance, honest demotion) | no row — not evidence |
| FR-P1-05-15 | SD-R-02 (post-access labelling) | no row — not evidence |
| FR-P1-05-16 | SD-R-01 (`require_d17_bound`, `require_derived_label`, `require_driver_caveat`, `require_provenance_block` on W-5), SD-R-02 | not evidence — row approved under D-32, never run |
| FR-P1-05-18 | SD-R-02 (registered audit count) | not evidence — row approved under D-32, never run |
| FR-P1-05-19 | SD-R-04 (quarantine) | not evidence — row approved under D-32, never run |
| FR-P1-05-20 | SD-R-01 (`require_beats_model`), SD-R-02 | not evidence — row approved under D-32, never run |
| REQ-CLAIM-01 | SD-R-03 (checklist over the registered set) | not evidence — `TST-CLAIMS-01` approved under D-32, never run |
| FR-P1-03-4 | SD-R-02 (fields consumed, not restated) | `Pending` |
| REQ-ENG-4 | SD-R-04 | `Pending` |
| REQ-ENG-8 | SD-R-04 (coverage notebook, home routed to gate) | `Pending` |
| REQ-ENG-13 | SD-R-04 | `Pending` |
| FR-P1-05-3 | SD-R-04 (RF `authoritative = false` render refusal) | no row — `Pending` |
| FR-P1-05-21 | SD-R-01 (`require_complete_members` co-reports M-03) | no row — `Pending` |
| NFR-DQ-01 | SD-R-02 (grade discipline via R-130/R-62) | `Pending` |
| NFR-TDEF-01 | SD-R-01 (`require_lineage_caveat`) | `Pending` |

**Derived and printed**: 4 design sections (SD-R-01…SD-R-04); **19** coverage rows, matching
the upstream `security-requirements.md`'s 19 exactly (same ID set, set-differenced:
+0 / −0); **10** render guards in SD-R-01's table, counted off the table *(corrected
2026-09-05 on adversarial finding 1; superseded: **6**. Four guards added for the five
unassigned render-time controls — R-125 (9)/(32)/(33), R-127 (34)/(38); (32) and (33) share
one guard)*; **5** status cells restated verbatim from the upstream Status column
*(corrected 2026-09-05 on adversarial finding 2, Major; superseded: `Pending (D-32, unrun)`
standing alone, which dropped the upstream column's operative words "not evidence")*;
**0** rows claimed satisfied; **0** scientific values decided.

## Assumptions & Open Questions

- **[Q1]** The registered-surface rule binds **pipeline-produced** artifacts only.
  Hand-authored prose outside the pipeline escapes it — narrowed, not closed, exactly as
  SEC-R-03 already states for indirect citation. No artifact may describe the checklist as
  fully enforced.
- **[Q2]** The metric-entry/rendering split assumes the sibling's shared guard module lands
  as designed (its SD-C-01). Its formerly open Major (mask-vs-member partition alignment)
  **was closed at the stage gate on 2026-09-05** as the sibling's sixth guard; this unit's
  rendering guards correctly never absorbed it.
- **[assumption]** `ConclusionSurfaceArtifact` registration and the render-guard calls can
  share one transaction boundary at 3.5, so an artifact cannot be emitted registered but
  unguarded or guarded but unregistered. Owed at 3.5 as a note, not a new decision.
- **Carried — both SEC-R-02 producing halves unbuilt; the refusals fail on every input until
  they land.** Carried — the exploratory label's writer, the coverage notebook's home, and
  the §15.2 row proposals stay routed to their gates. Carried — BLK-03/04/08/09 open;
  BLK-08's TECU reach checked by `require_units`, not resolved by it.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or
  claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T06:42:22Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | `security-design.md` § SD-R-01 guard table (lines 44-51); `logical-components.md` R2 row (line 32) | **SD-R-01's title claims "one home for every rendering refusal," but at least five negative controls named in `business-rules.md` R-125/R-127 have no guard assigned in the 6-row table.** (a) R-125 control (9): "A benchmark row without a `beats_model` field → fails the presence test" — none of the 6 guards' stated scopes cover a missing `beats_model` field on an otherwise-present member (`require_complete_members`'s stated scope is member presence — "a table missing any declared comparison-set member's metric" — not a missing sub-field on a present member). (b) Control (32): "A rendered primary table or breakdown artifact missing any of the five provenance fields [`mask_id`, `feature_set_id`, `surviving_row_counts`, `exclusion_counts`, `scored_window_statement`] → fails." (c) Control (33): "A `scored_window_statement` that does not equal the DEC mask's asserted scored range → raises." (d) R-127 control (34): "A derived percentage-reduction field emitted without its explicit `derived: true` label → fails." (e) R-127 control (38): "A per-station breakdown artifact emitted without the standing driver-identity / no-local-forcing caveat → fails." None of these five is the stated scope of `require_estimand_fields` (orientation/weighting only), `require_lineage_caveat` (IRI/GIM lineage only), `require_units` (TECU only), `require_complete_members` (member presence only), or `require_d17_bound` (D-17 strata bound only) — and all five are render-time/producing-path checks inside this unit's own boundary (not the sibling's metric-entry guards, per the artifact's own boundary-split rule at lines 53-62), so per the design's own architecture they belong at R2. This is the identical failure class the sibling's own reviewer flagged as Major on `evaluation-and-comparison/nfr-design/security-design.md` (a named `FairnessError`/business-rule control with no assigned guard) — reproduced here at greater scope (five controls, not one) and against a stronger claim ("one home for **every** rendering refusal," not a hedged claim). | Add explicit guard entries (or extend named guards' stated scope with citations) for controls (9), (32), (33), (34) and (38), naming each in SD-R-01's table exactly as `require_estimand_fields`/`require_lineage_caveat`/etc. are named, so the "one home for every rendering refusal" claim is checkable against the table rather than against prose scattered across R-125/R-127. |
| 2 | Major | `security-design.md` § Requirement coverage table (lines 143, 149-153); Sources (line 19); banner (line 12) | **The design table's Status column substitutes the upstream Acceptance-row narrative for the upstream Status field on 5 of 19 rows, contradicting the artifact's own claim that "Statuses are the upstream artifact's; nothing is upgraded here."** Direct comparison against `security-requirements.md`'s coverage table (its actual 4th "Status" column, not its 3rd "Acceptance row" column): FR-P1-05-16, FR-P1-05-18, FR-P1-05-19, FR-P1-05-20 and REQ-CLAIM-01 all carry upstream **Status = `not evidence`** (verified directly: `security-requirements.md` lines 197-201). This design's table instead prints `Pending (D-32, unrun)` for all five — the *Acceptance-row* column's content, not the Status column's. By contrast, FR-P1-05-14/-15 correctly carry `not evidence` (matching upstream Status) and FR-P1-05-3/-21 correctly carry `Pending` (matching upstream Status for those two, which genuinely is `Pending` there). The inconsistency is internal to this design's own table: two rowless items keep the upstream Status verbatim while five D-32-approved items silently drop it. This is exactly the representation-fidelity failure this project's `project.md` learnings log names repeatedly (sweep every representation of a fact, not the enumerated site) — here, the fact being dropped is the specific word ("not evidence") the upstream artifact's own banner and Acceptance-row prose exist to hammer home against exactly this kind of D-32-approval-read-as-progress confusion. | Restore the literal upstream Status value (`not evidence`) for FR-P1-05-16, -18, -19, -20 and REQ-CLAIM-01 in the design's Status column, keeping the `(D-32, unrun)` detail as supplementary annotation rather than a substitute for the Status value itself. |
| 3 | Minor | `security-design.md` Sources (line 23) | **Section cross-reference error: the boundary-split prose is in § SD-R-01, not § SD-R-02.** Line 23 states "the boundary split in § SD-R-02 is defined against it," but the actual boundary-split paragraph ("The boundary split, stated so no check is homeless or double-owned...") appears at lines 53-62, inside § SD-R-01 (which opens at line 38); § SD-R-02 does not open until line 76 and contains no boundary-split discussion. | Correct the Sources citation to "§ SD-R-01" (or move the boundary-split paragraph into § SD-R-02 if that was the intended location, though the paragraph's placement immediately after the guard table under SD-R-01 reads as intentional). |

### What was verified

- **Coverage completeness (task 4).** Printed the 19 IDs in this artifact's table and set-differenced against the 19 IDs in the dispatch brief's upstream list and against `security-requirements.md`'s own 19-row table (independently counted: 19 rows, same IDs) — **+0/−0** both ways. The claimed "19 coverage rows... matching the upstream... exactly" and "6 render guards... counted off the table" are both correct as printed.
- **Q1 = A coherence.** W-4's `ConclusionSurfaceArtifact` (fail-closed when absent) is confirmed present in `business-logic-model.md` W-4's `RAISES` block ("an absent, unmanifested or unregistered conclusion surface FAILS CLOSED rather than skipping") and in `business-rules.md` R-126 addition 3 (control (36)). § SD-R-03's residual ("Hand-authored thesis prose written outside the pipeline... narrowed, not closed") is stated in the **rule body itself** (§ SD-R-03, not only `## Assumptions`), correctly avoiding this stage's own previously-flagged rule-body-vs-Assumptions defect pattern (`tech-stack-decisions.md` TS-R-02, `project.md` `fd-2026-08-30-sweep-numerals-and-surfaces`).
- **Q2 = A / boundary split (task 2, partial).** All 6 named guards do map to a stated upstream refusal: `require_estimand_fields`→SEC-R-02 half 1; `require_lineage_caveat`→SEC-R-02 half 2; `require_units`→R-125 point 6; `require_complete_members`→R-125 point 2/FR-P1-05-9; `require_d17_bound`→R-127's D-17 bound; `require_registered_surface`→Q1=A/SD-R-03. The metric-entry/rendering split's guard names (`require_estimand_fields` etc.) do not collide with the sibling's `SD-C-01` guard names (`require_stamps`, `require_partition_agreement`, `require_registered_mask`, `require_target_space`, `require_locked_receipt`), confirmed by reading the sibling's `security-design.md` directly (the one permitted spot-check) — no check is double-named across the boundary. The artifact correctly declines to absorb the sibling's own open Major (mask-vs-member partition alignment, confirmed present and unresolved in the sibling's `security-design.md` § Review) rather than papering over it.
- **Scientific-value discipline (task 3).** Regime thresholds, event window, D-13, D-28 window are stated as encoded/frozen, never re-decided, consistent with `business-rules.md` R-123/R-124. The gate-routed items (exploratory label's writer, coverage notebook's home, §15.2 row proposals) are carried in `## Assumptions & Open Questions` as still routed. No upstream `Pending`/no-row status is upgraded to satisfied anywhere in the prose (the Status-column table defect above is a fidelity error, not an upgrade to a passing claim).
- **Status honesty (task 5, partial).** Both SEC-R-02 halves stated unbuilt and failing on every input today ("that is the mechanism working"), consistently in the banner, § SD-R-01 and § SD-R-02. G-09/D-31 disclosure present in the banner (line 13). BLK-03/04/08/09 open, stated in both artifacts.
- **Sensors.** Both files carry well over 2 H2 headings and reference all three consumed artifact categories, including the explicit statement of the absent `performance-requirements.md`/`scalability-requirements.md`/`reliability-requirements.md` (line 26 here; line 16 in `logical-components.md`).

### Coverage limits

- `../../../inception/application-design/component-methods.md` (cited in `logical-components.md` Sources for the `count_storm_events` boundary and § Depth) was not opened — outside the stated read scope for this pass; the signature it is said to fix is independently corroborated by `business-logic-model.md` W-1, which quotes it verbatim and was already in scope, so this is not treated as an unverified claim, only an unexpanded one.
- `evaluation-and-comparison/nfr-design/logical-components.md` (cited by this unit's `logical-components.md` for components C1/C7) was not read — the permitted spot-check named only the sibling's `security-design.md`, and a second sibling file falls outside the granted carve-out; C1/C7's existence is taken on this unit's own citation, not independently confirmed.
- Did not verify `component-methods.md` § Depth's claim that intra-package shapes are this stage's to specify, or the fourteen-project-exceptions enumeration referenced in `business-logic-model.md` Sources, both out of the granted read scope.

### Summary

One Critical finding: SD-R-01's guard table, despite its own title claiming to be "one home for every rendering refusal," leaves at least five business-rules-mandated render-time controls (R-125's `beats_model` presence, the five-field provenance block, the scored-window-statement agreement check, and R-127's `derived: true` label and driver-identity caveat) with no assigned guard — the same failure class the sibling unit's reviewer already flagged as a Major elsewhere in this same intent, reproduced here at wider scope and against a stronger claim. One Major finding: the coverage table silently substitutes the upstream Acceptance-row narrative for the upstream Status field on five of nineteen rows, dropping the specific `not evidence` status word this project's governance apparatus exists to protect, while inconsistently keeping it verbatim on the other rowless rows. One Minor: a section cross-reference names § SD-R-02 for content that is actually in § SD-R-01. The coverage-count arithmetic, the Q1/Q2 rationale, the metric-entry/rendering boundary split's non-collision with the sibling's guard names, and the scientific-value/status-honesty discipline all held up under adversarial testing. With one Critical finding, the verdict is NOT-READY.

NOT-READY

## Review — iteration 2 (terminal)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T06:48:47Z
**Iteration:** 2 (terminal — advisory to the human gate, no further repair cycle behind this pass)

### Verification of iteration-1 findings

**Finding 1 (Critical, guard-table gap) — CONFIRMED REPAIRED.** Recounted SD-R-01's table directly: 10 rows (`require_estimand_fields`, `require_lineage_caveat`, `require_units`, `require_complete_members`, `require_d17_bound`, `require_registered_surface`, `require_beats_model`, `require_provenance_block`, `require_derived_label`, `require_driver_caveat`), matching the "10" printed at line 176 and `logical-components.md` R2's "the ten rendering refusals... counted: 10" (line 32). Verified each of the five previously-unguarded controls directly against `business-rules.md`:
- Control (9) (`business-rules.md:336`, "A benchmark row without a `beats_model` field → fails the presence test") → `require_beats_model`, Enforces citing "R-125 control (9)". Match.
- Control (32) (`business-rules.md:337-339`, provenance-field presence) and control (33) (`business-rules.md:339-341`, scored-window agreement) → `require_provenance_block`, Enforces citing both. Match (see new finding below on this guard's call-site scope).
- Control (34) (`business-rules.md:560-561`, unlabelled `derived:true` field) → `require_derived_label`, Enforces citing "R-127 control (34)". Match.
- Control (38) (`business-rules.md:562-563`, missing driver-identity caveat) → `require_driver_caveat`, Enforces citing "R-127 control (38)". Match.
The independent counting table at `business-rules.md:811-813` (R-125: (7),(8),(9),(32),(33) = 5; R-127: (13)…(18),(34),(38) = 8) confirms these control numbers exist and are correctly attributed. No guard is double-counted or misattributed. Repaired as claimed, and the repair holds under direct re-derivation rather than trust in the described fix.

**Finding 2 (Major, status-cell substitution) — CONFIRMED REPAIRED.** Cross-checked all 19 rows of this design's coverage table (lines 154-172) against `security-requirements.md`'s own Status column (lines 191-209, verified directly). The five previously-affected rows (FR-P1-05-16, -18, -19, -20, REQ-CLAIM-01) now lead with `not evidence` — matching upstream verbatim — with the `(D-32, unrun)` / "row approved... never run" detail carried as supplementary annotation rather than substituted for it. The two genuinely rowless rows (FR-P1-05-14, -15) correctly keep `not evidence`. The two rows added on the sibling stage's iteration-1 findings (FR-P1-05-3, -21) correctly keep `Pending`, matching upstream's actual (non-`not evidence`) status for those two — the repair did not overcorrect by blanket-replacing every cell with `not evidence`. Repaired as claimed.

**Finding 3 (Minor, § SD-R-02→SD-R-01 citation) — CONFIRMED REPAIRED.** Line 23 now reads "the boundary split in § SD-R-01 is defined against it," matching the actual location of the boundary-split paragraph (lines 64-73, inside § SD-R-01). Repaired as claimed.

### New finding — repair-introduced regression

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 4 | Major | `security-design.md` § SD-R-01 guard table, `require_provenance_block` row (line 53); § Requirement coverage, FR-P1-05-16 row (line 160); `logical-components.md` R4 row (line 34) | **The repair that added `require_provenance_block` for controls (32)/(33) scoped its call site to the table only, but the underlying rule the repair itself cites requires the identical check on breakdown artifacts too — a call site this design nowhere assigns it to.** Control (32)'s own text (`business-rules.md:337-339`) reads "A rendered primary table **or breakdown artifact** missing any of the five provenance fields → fails" — explicitly covering both W-3 (table) and W-5 (breakdowns). `business-rules.md`'s own cross-reference ledger states this directly at line 908: "Vision §8.9's reported provenance \| R-125 limb 7 (controls 32, 33); **R-127 (the same block on every breakdown)**" — i.e. the five-field provenance block is required on every R-127 breakdown artifact, not only the R-125 table. Yet: (a) `require_provenance_block`'s own "Refuses" text narrows this to "**a table** missing any of the five provenance values" (singular "table," dropping "or breakdown artifact" from the very control it Enforces-cites); (b) its "Called by" column lists only `W-3`, omitting `W-5`; (c) the Requirement coverage row for FR-P1-05-16 — the requirement that traces to R-127's breakdown family (`business-rules.md:881`) — cites `require_d17_bound`, `require_derived_label` and `require_driver_caveat` but not `require_provenance_block`; (d) `logical-components.md` R4 ("breakdown family") lists "D-17 strata bound; §5.5 metric set; tier-3 row; driver-identity caveat emitted" with no provenance-block mention. All four representations agree with each other and disagree with `business-rules.md:908` — this is not an isolated typo but a consistently under-scoped guard, the same class of defect ("a repair that fixes the named site and leaves a stale/incomplete representation elsewhere") this project's own `project.md` learnings log names repeatedly, reproduced here by the very repair meant to close the Critical finding. Practical consequence: as designed, a breakdown artifact (W-5) could render missing `mask_id`, `feature_set_id`, row/exclusion counts, or an unverified scored-window statement with no assigned refusal — in the unit whose own scope note calls itself "the last surface before the thesis." This also weakens § SD-R-01's boundary-split claim ("nothing checked twice, nothing checked nowhere"), which is contradicted by this specific gap. | Extend `require_provenance_block`'s "Refuses" text and "Called by" column to include W-5 (breakdown artifacts), matching control (32)'s own "table or breakdown artifact" wording and `business-rules.md:908`'s "the same block on every breakdown." Add `require_provenance_block` to FR-P1-05-16's coverage row and to `logical-components.md` R4's owned-checks list. |

### Regression sweep — no other new inconsistency found

- Guard count ("10") is consistent in numeral form across `security-design.md` (guard table row count, line 176's derivation) and `logical-components.md` (R2 row, line 32, and its mermaid node label "R2 render-guard set (10 refusals)" at line 48) — no stray "6" or "six" found outside the historical iteration-1 `## Review` text (which correctly quotes the pre-repair state as part of the finding record, not a live claim).
- The four newly-added guards' Enforces citations (`require_beats_model`→(9), `require_derived_label`→(34), `require_driver_caveat`→(38)) were independently verified word-for-word against `business-rules.md` and found correctly scoped and correctly cited; only `require_provenance_block` (finding 4 above) has a scope/call-site mismatch.
- Exception-class attributions (`FairnessError`, `RegimeError`, `IntegrityError` in `logical-components.md` R1/R2/R5) remain generic enough not to contradict the specific classes `business-rules.md` names per control (`RegimeError` for (33); unnamed/presence-style for (9), (32), (34), (38)) — no new mismatch introduced.
- No status cell newly claims a satisfied/passing state; the five repaired cells and the two rowless cells all still read `not evidence`, and the artifact's own derivation line ("**0** rows claimed satisfied") is unchanged and still true on inspection.
- No scientific value is decided in the repair; the banner, Assumptions, and BLK-03/04/08/09 open-item carries are unchanged from iteration 1.

### Coverage limits

- Carried from iteration 1: `evaluation-and-comparison/nfr-design/logical-components.md` (C1/C7) and `component-methods.md`'s full § Depth / fourteen-exceptions enumeration were not independently opened this pass either — outside the granted read scope (one sibling `security-design.md` spot-check only); this unit's own citations to them are taken as given, not independently re-confirmed a second time.
- This pass did not re-derive `logical-components.md`'s failure-domain table or shared-resources table line-by-line beyond what was needed to check R2/R4 for the provenance-block gap; no defect is asserted there beyond what is stated above.

### Summary

All three iteration-1 findings (one Critical guard-table gap, one Major status-cell substitution, one Minor citation) are independently re-verified as correctly repaired by direct comparison against `business-rules.md` and `security-requirements.md` rather than by trusting the described fix. The repair itself introduces one new, evidence-backed Major: `require_provenance_block` — one of the four guards added to close the Critical finding — is scoped only to the primary table (W-3), while the control it Enforces (business-rules control (32)) and the project's own cross-reference ledger (`business-rules.md:908`) both state the identical five-field check applies to breakdown artifacts (W-5) too; this gap is consistent across the guard's own wording, its Called-by column, the FR-P1-05-16 coverage row, and `logical-components.md`'s R4 row, so it is a real design gap rather than a single stray line. With zero Critical and one Major finding, the verdict is READY per this project's stated verdict rule (READY if zero Critical, ≤2 Major); finding 4 should nonetheless be weighed explicitly at the human gate, since it reproduces — at narrower scope — the exact failure class iteration 1 rated Critical, in the unit that is the last surface before the thesis.

READY

## Review — 2026-09-05 post-gate repair verification

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T07:55:11Z
**Iteration:** 1 (fresh budget after gate rejection)

### Per-recommendation verification

**Recommendation 2 (`require_provenance_block` widened to breakdown artifacts) — VERIFIED, landed correctly and accurately cited.**
- The guard row (line 53) now reads "a table **or breakdown artifact** missing any of the five provenance values... or a scored-window statement disagreeing with the registered mask's," Called-by `W-3, **W-5**`.
- Cross-checked against `business-rules.md:337-339` directly: control (32)'s own text is "A rendered primary table **or breakdown artifact** missing **any** of the five provenance fields → **fails** the presence test" — the citation is verbatim-accurate, not a paraphrase dressed as a quote.
- Cross-checked `business-rules.md:908` directly: the cross-reference ledger states "Vision §8.9's reported provenance | R-125 limb 7 (controls 32, 33); **R-127 (the same block on every breakdown)**" — confirms the obligation is R-127-owned for breakdowns, independent of R-125's table-scoped limb.
- The SD-R-01 correction box (lines 62-67) documents the widening and cites the correct source (control (32)'s own wording, the gate's Request-Changes ruling).
- `FR-P1-05-16`'s coverage row (line 166) now lists `require_provenance_block` on W-5 alongside `require_d17_bound`, `require_derived_label`, `require_driver_caveat`. Verified against `business-rules.md:881`: FR-P1-05-16 traces to R-127 (which owns the breakdown-family provenance obligation per line 908), so the addition is correctly scoped, not merely bolted on.
- `logical-components.md` R4 row (line 34) carries "**five-field provenance block on every breakdown (`require_provenance_block`, widened to W-5 at the stage gate, governance Recommendation 2)**" — consistent with the other three representations.
- **Sweep for remaining table-only scoping**: none found. All four representations (guard row, correction box, FR-P1-05-16 row, R4 row) now agree; no stray site still narrows this guard to "a table" alone.

**Recommendation 9 (`require_lineage_caveat` widened to W-7, "present" defined for figures) — VERIFIED, landed correctly, with one Minor citation-fidelity gap.**
- The guard row (line 47) now reads Called-by `W-3, W-5, **W-7**`, with "for a figure, 'present' means the caveat field rendered into the caption or figure metadata" added to the Refuses text.
- Confirmed `W-7` (`business-logic-model.md` lines 724-756) is a plausible call site: its INPUT includes "the metrics artifact, W-5's breakdown artifacts... BootstrapResult" — artifacts that can carry IRI/GIM comparison content — and its manifest already asserts axis-units from artifact metadata (point 2), so requiring the lineage-caveat field to ride the same artifact-metadata channel into the caption is architecturally consistent with W-7's existing "presentation-only by signature" design, not a bolt-on.
- **Citation-fidelity gap (Minor, new).** The guard row cites "TEC-06's 'wherever reported'" in quotation marks as if verbatim. This project's own `project.md` § Mandated TEC-06 rule (part of this stage's rule bundle) reads: "state the documented spatial-representativeness mismatch **at the point where any IRI or GIM comparison is reported**" — substantively supports the widening (the caveat is required at every reporting point, not the table alone), but the quoted fragment "wherever reported" does not appear verbatim anywhere in `project.md`, `security-requirements.md`, or this unit's `business-rules.md` (confirmed by direct read/grep of all three). This is a paraphrase dressed as a quotation, not a substantive defect in the widening itself — the underlying justification is sound, only the quotation-mark citation format is inaccurate.
- **No other row contradicts.** `SD-R-02` (lines 93-102, generic field-based mechanism description), the `NFR-TDEF-01` coverage row (line 178), and `logical-components.md` R7's row (line 37, "via R2" — generic) do not restate a table-only scope anywhere; none conflicts with the W-7 widening.

**Sibling-Major references (three sites) — VERIFIED, sibling's sixth guard confirmed landed.**
- All three sites in this unit (`security-design.md` SD-R-01 boundary-split paragraph lines 76-79, `## Assumptions & Open Questions` [Q2] line 198; `logical-components.md` boundary bullet lines 79-80 and `## Assumptions & Open Questions` [Q2] lines 132-134) state the sibling's Major was closed 2026-09-05 as its sixth guard.
- Spot-checked the sibling's `evaluation-and-comparison/nfr-design/security-design.md` directly (the permitted spot-check): `require_mask_member_alignment` is present as SD-C-01's sixth guard row (line 50: "the mask's **recorded** `partition_id` matches every member's... **refuses**"), and the sibling's own terminal review independently verifies it "VERIFIED, landed correctly" (lines 254-269 there). No site in either of this unit's two files still calls it open.

### Regression sweep

- **Guard count still 10.** Counted the SD-R-01 table directly: `require_estimand_fields`, `require_lineage_caveat`, `require_units`, `require_complete_members`, `require_d17_bound`, `require_registered_surface`, `require_beats_model`, `require_provenance_block`, `require_derived_label`, `require_driver_caveat` = 10 rows. Matches the "10" printed at line 182 and `logical-components.md`'s "the ten rendering refusals... counted: 10" (line 32) and mermaid label (line 48). The two widenings (Rec 2, Rec 9) extended existing rows' Called-by/Refuses columns; they added no new rows. No stray "6"/"six" found outside the historical iteration-1 `## Review` text, which correctly records the pre-repair state as part of the finding record.
- **19-row coverage set unchanged.** Recounted the coverage table: 19 rows, same ID set as `security-requirements.md`'s 19-row table (+0/−0). Statuses otherwise verbatim from the prior repaired state (iteration-2's Finding-2 repair): the five D-32-approved rows still read `not evidence`, the two rowless rows still read `no row — not evidence`, and FR-P1-05-3/-21 still read `Pending`, matching upstream.
- **Per-entry negative-control paragraph (lines 81-87)** is unchanged prose and remains consistent with the widened call-sites in substance (it names one representative violating input per producing path, not an exhaustive per-guard enumeration) — it does not assert anything the widened Called-by columns now contradict.
- **Nothing newly claimed satisfied.** The derivation line's "**0** rows claimed satisfied; **0** scientific values decided" (line 188) is unchanged and still true on inspection; the banner (lines 5-15) is untouched.

### Summary

Both Recommendation 2 and Recommendation 9 landed as directed, each independently verified against `business-rules.md`'s own control text and cross-reference ledger rather than trusted from the artifact's description of its own fix, and each is consistent across every representation this unit carries (guard row, correction box, coverage row, `logical-components.md` row). The sibling's sixth guard (Recommendation 1) is independently confirmed present and verified in the sibling's own terminal review. One new Minor finding: the `require_lineage_caveat` widening cites "TEC-06's 'wherever reported'" as a quoted fragment that does not appear verbatim in any governing document, though the substantive justification for the widening (TEC-06's actual text, "at the point where any IRI or GIM comparison is reported") independently supports it. Guard count (10), coverage-row count (19), and status-cell fidelity are unchanged from the last-verified repaired state. With zero Critical and zero Major findings, the verdict is READY.

READY
