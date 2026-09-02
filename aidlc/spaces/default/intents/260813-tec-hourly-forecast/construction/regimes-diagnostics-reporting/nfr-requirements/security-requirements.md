# Security Requirements — `regimes-diagnostics-reporting`

**Unit** `regimes-diagnostics-reporting` (Bolt 11) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NOTHING HERE IS CLAIMED SATISFIED — AND THIS UNIT IS WHERE THE HONESTY RULES LAND
>
> **This artifact covers 19 requirements, 9 of them carrying no result** *(banner corrected
> 2026-09-01; superseded: "11 requirements, 7 without a §16/§19 row". That is the
> `functional-design` map's figure and it is still true **of the map** — but this artifact's
> coverage table was extended to **19** on the iteration-1 Majors, adding **FR-P1-05-3** and
> **FR-P1-05-21**, and **both are themselves rowless**. The banner states the fact first and
> was left describing the map rather than the artifact.)*
>
> The map's **11 requirements, 7 without a §16/§19 row** break down as: **five hold
> D-32-approved rows that are `Pending` — never run, NOT passed** (FR-P1-05-16, FR-P1-05-18,
> FR-P1-05-19, FR-P1-05-20, `REQ-CLAIM-01`/`TST-CLAIMS-01`), and **two are genuinely rowless** —
> **FR-P1-05-14** and **FR-P1-05-15**, covered by R-128's controls meanwhile. **The two added
> requirements — FR-P1-05-3 and FR-P1-05-21 — have no row either**, their rows being
> `models-and-baselines`' to propose. **An approved-but-unrun row and an absent row are both
> `Pending`, and neither is evidence.**
>
> **TA-16, TA-19, TA-20 and WS-19 are undischarged.** **G-09 is signed (D-31) with its own
> preconditions UNMET**; **stage 3.1 remains FAIL**; `configs/` does not exist; **no Python
> interpreter exists in this environment**, so **no results table has ever been produced**.
>
> No scientific value is decided here, and TE §18.2's absolute rule stands.

## Sources

- `../functional-design/business-rules.md` — **R-123** (one regime classifier, configured thresholds, **one counting path**), **R-124** (**December-blind by signature, post-receipt by construction**, and the two guards), **R-125** (the primary results table **refuses, co-reports, prints, and checks its units**), **R-126** (the claims-and-limitations checklist: **presence checks at named locations**, and the §15.2 routing), **R-127** (the breakdown family: **stamped producing functions**, the D-17 bound, the inventory refusal), **R-128** (**practical relevance frozen and demoted honestly**; post-access runs **labelled**), **R-129** (`plots.py` is **presentation-only by signature**; the manifest is WS-19's evidence), **R-130** (the **diagnostics quarantine**: grade discipline, labelled artifacts, and the lane boundary), **R-131** (the notebooks: one declaration helper, stop semantics, **no only-copy**), **R-132** (`tests/test_regimes_and_reporting.py`: **one home for every named control**).
- `../functional-design/business-logic-model.md` — **W-1** … **W-10**, in particular **W-2** (the December channel), **W-3** (the primary results table as a producing path consuming **checked** fields), **W-4** (the claims checklist's presence checks), **W-6** (**two untested requirements made mechanical**), **W-8** (the diagnostics quarantine).
- `../../evaluation-and-comparison/nfr-requirements/security-requirements.md` — **§ SEC-C-02**, whose **consumer half** this unit's § SEC-R-02 completes.
- `../../target-standardization/nfr-requirements/security-requirements.md` — **§ SEC-T-02**, whose **consumer half** this unit's § SEC-R-02 also completes.
- `../../../inception/requirements-analysis/requirements.md` — **REQ-ENG-4**, **REQ-ENG-8**, **REQ-ENG-12**, **REQ-ENG-13**, **FR-P1-03-4**, **FR-P1-05-9**, **FR-P1-05-10**, **FR-P1-05-11**, **FR-P1-05-14**, **FR-P1-05-15**, **FR-P1-05-16**, **FR-P1-05-18**, **FR-P1-05-19**, **FR-P1-05-20**, **FR-P1-05-3**, **FR-P1-05-21**, **REQ-CLAIM-01**, **NFR-DQ-01**, **NFR-TDEF-01**. *(The NFR family was set-differenced separately against `requirements.md`'s eleven NFR IDs, because on `statistical-inference` a design-file grep came back clean on both FR families and still missed NFR-REP-01.)*
- `../../../../../../../../PreFlight/vision_document(3)(2)(2).md` — **§2.4** (the **binding honesty rule**), **§2.5** (the claim boundary), **§5.4** (practical-relevance thresholds), **§6.4** (RF importance non-authoritative), **§6.6**, **§8.3**, **§11** (the December regime-count audit as a required G-05 input).
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§6.2** (Dst diagnostic/hindcast-only), **§7.2**, **§14** (notebook obligations), **§15.2**, **§18.2–18.3**, **§19** (TA-16, TA-19, TA-20), **§16** (WS-19).
- `evidence/DECISIONS.md` — **D-17** (the sixteen target fields, which bounds the breakdown family), **D-32** (the eight approved §15.2 rows).
- `nfr-requirements-questions.md` — Q1 = A, Q2 = A, and the receipted Consolidated Summary Confirmation.

---

## Scope note

`produces_kinds` excludes `performance-requirements`, `scalability-requirements` and
`reliability-requirements` for a `library` unit. Assessed anyway:

| Category | Assessment for `regimes-diagnostics-reporting` | Where it lives |
|---|---|---|
| **Performance** | No latency target. Rendering a results table and a figure set over three cells and one scored month is bounded. | — |
| **Scalability** | Bounded and known. No growth projection. | — |
| **Reliability** | **Fail-closed on rendering**: the table **refuses** to render an estimand value without its orientation and weighting, **refuses** an IRI or GIM comparison without the lineage caveat, and **refuses** a breakdown outside the D-17 bound. This unit would rather report nothing than report a number whose meaning it cannot establish. | § SEC-R-01, § SEC-R-02 |
| **Security** | This artifact — **the honesty of what is reported**. This unit is the **last surface before the thesis**, and every containment rule upstream is defeated if a quarantined or unqualified value is rendered here as a finding. | — |
| **Observability** | The `beats_model` trigger field printed by W-3; the claims-checklist presence results; the `plots.py` manifest as WS-19's evidence. | § SEC-R-01, § SEC-R-03 |

---

## SEC-R-01 — The primary results table, and the honesty rule it enforces

**Requirement (R-125, W-3, FR-P1-05-9, Vision §2.4).** The **three mandatory difficulty
controls** — persistence, 24-hour seasonal persistence, and fitted station×month×hour
climatology (trained on training partitions only) — are **co-reported in the same primary
results table** as the LSTM-vs-IRI comparison, and **never relegated to an appendix**.

**Requirement (FR-P1-05-20, Vision §2.4).** **Any baseline that beats the LSTM on the locked
test appears in the primary results table AND in the abstract-level conclusion.** A favourable
LSTM-vs-IRI result **never licenses silence** about an unfavourable LSTM-vs-persistence or
LSTM-vs-climatology result.

**The trigger is a field, not a judgement.** W-3 prints **`beats_model`**, so the disclosure
obligation fires on a **computed value** rather than on an author noticing. R-110's pattern:
the **caveat is emitted by the producing path**.

**Requirement (R-125).** The table **checks its units**. A number rendered in the wrong units
is a wrong number that looks right.

**Requirement (FR-P1-05-11, W-7, R-129).** `plots.py` is **presentation-only by signature** —
it cannot compute a reported quantity — and its **manifest is WS-19's evidence**.

**Requirement (Vision §2.5).** Every claim is bounded to the frozen scope: hourly VTEC at
**ARUC 40/44, BSHM 32/35, NICO 35/33**, **calendar year 2022**, **tested on December 2022
only** — no generalisation beyond these cells, this year, or this test month.

**Requirement (Vision §2.2, §7.0B).** The abstract-level interpretation states that **Phase 2
is a fixed-protocol replication on a new target lineage, not a second statistically independent
blind test**.

## SEC-R-02 — The two consumer halves this unit owes, stated as refusals

> ### Requirement (Q1 = A) — both half-contracts are completed HERE, at the consumer
>
> Two sibling units built a refusal on their side and named **this unit** as the counterparty,
> because this unit owns the **primary results table**. Neither half had been stated. Both are
> stated now, as **hard failures**:
>
> **1 — The estimand's sign and weighting** (completing `evaluation-and-comparison`
> § SEC-C-02). The table **refuses to render** an estimand value that does not carry its
> **orientation** (`benchmark_minus_model`) and **weighting** (`equal_station`). A correct
> value read under the wrong convention **inverts the thesis conclusion**, and the number looks
> identical either way.
>
> **2 — The lineage caveat** (completing `target-standardization` § SEC-T-02). The table
> **refuses to render** any **IRI or GIM comparison** that does not carry the **lineage
> caveat** — that the Phase 1 target is **location-sampled gridded VTEC**, never
> receiver-specific station-observed VTEC, and that part of any measured difference is a
> **geometry and sampling artefact rather than skill** (Vision §6.6).
>
> **The cost, written down rather than discovered.** **Both refusals will fail on every input
> until the producing halves land.** That is correct fail-closed behaviour, and it will look
> like breakage. It is stated here so the first failure is recognised as the mechanism working.
>
> **Why refusals and not acknowledgements.** Both siblings enforce on their side. An
> acknowledgement here would leave each pair **asymmetric** — producer enforcing, consumer
> merely intending — and **a half-contract stated on one side only is not a contract**.

## SEC-R-03 — The diagnostics quarantine, extended from production to citation

**Requirement (R-130, W-8).** The diagnostics lane is **quarantined**: **Dst is diagnostic and
hindcast-only, never a confirmatory ML feature** (TE §6.2), and the **Random Forest importance
figure is non-authoritative** — it may be **saved as a diagnostic figure**, and may **never**
add, remove or rank a feature into the production set (Vision §6.4). Grade discipline, labelled
artifacts, and a lane boundary.

> ### Requirement (Q2 = A) — the claims checklist extends to CITATION
>
> **R-130 governs production. Nothing governed citation.** A correctly quarantined, correctly
> labelled figure can still be **cited in thesis text as if it were evidence**, because **the
> label travels with the artifact, not with the sentence that references it**.
>
> **Any thesis-level location citing a quarantined diagnostic must carry its non-authoritative
> label alongside the citation**, checked at the **same named locations R-126's checklist
> already inspects**. This extends a mechanism this unit already owns rather than adding one.
>
> **Its weakness, stated plainly.** A **prose check is weaker than a field check**. An
> **indirectly phrased citation evades it** — a sentence that describes the figure's content
> without naming it will pass. **This narrows the gap; it does not close it**, and **no artifact
> may describe the diagnostics quarantine as fully enforced.**
>
> **Why not forbid citation outright.** Vision **requires** the RF-importance figure to be
> *saved* as a diagnostic. A diagnostic that may never be discussed is of no use to anyone, so
> a blanket prohibition would forbid the use the authority mandates.

**Requirement (R-126, W-4).** The claims-and-limitations checklist performs **presence checks at
named locations**, with **one row per prohibited class**, cited from § Out of scope C.

## SEC-R-04 — December stays out of the reporting path, and post-access work is labelled

**Requirement (R-124, W-2).** The December channel is **blind by signature** and **post-receipt
by construction**, with **two guards**. The regime count reaching a report comes from the
**required, performance-blind pre-G-05 coverage and regime audit** (Vision §8.3, §11) — which is
a **required G-05 input**, not a violation of the lock — and is **guarded by the registered
count**.

**Requirement (R-123, W-1).** **One regime classifier, configured thresholds, one counting
path.** Two counting paths can disagree, and the one used in the report is the one nobody
re-derives.

**Requirement (R-128, W-6, FR-P1-05-14, FR-P1-05-15).** **Practical relevance is frozen and
demoted honestly**: **no practical-relevance threshold is introduced, changed or reinterpreted
after the December locked test is opened** (Vision §5.4), and where a result fails to meet a
frozen threshold it is **demoted honestly** rather than re-described. **Every post-access run is
labelled exploratory** (Vision §8.3).

**These are the two rowless requirements *the `functional-design` map carries*.** FR-P1-05-14 and
FR-P1-05-15 have **no acceptance row at all** and are **covered by R-128's controls meanwhile** —
W-6's own framing is *"two untested requirements made mechanical"*. **A mechanism is not an
acceptance row**, and this artifact does not treat it as one.

*(Scoped 2026-09-01 in the same sweep; superseded: "These are the two genuinely rowless
requirements." **Four are rowless in this artifact's coverage** — these two, plus **FR-P1-05-3**
and **FR-P1-05-21**, added on the iteration-1 Majors and rowless as well, their rows being
`models-and-baselines`' to propose. The sentence was true of the map and read as a claim about
the total.)*

**Requirement (R-127, W-5).** The breakdown family uses **stamped producing functions**, is
**bounded by D-17**, and carries an **inventory refusal** — a breakdown outside the bound
**fails** rather than rendering.

**Requirement (R-131, W-9, REQ-ENG-12, TE §14).** The four analysis notebooks each **import from
`src/`**, **read versioned artifacts**, and **begin with the dataset version, code commit,
configuration IDs and artifact IDs they expect**. **None holds the only copy** of parsing,
calibration, feature, split, training, evaluation or bootstrap logic. *"Run all"* either
**succeeds from declared inputs or stops with a clear missing-artifact or Internet-access
message** — it never proceeds on partial state.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| REQ-ENG-12 | SEC-R-04 | **TA-16 (primary)** | `Pending` |
| FR-P1-05-9 | SEC-R-01 | **TA-20 (primary)** | `Pending` |
| FR-P1-05-10 | SEC-R-01, SEC-R-04 | TA-19 (supporting; `target-standardization` primary) | `Pending` |
| FR-P1-05-11 | SEC-R-01 | **WS-19 (primary)** | `Pending` |
| **FR-P1-05-14** | SEC-R-04 | ⚠ **NO ROW AT ALL** — R-128's controls meanwhile | not evidence |
| **FR-P1-05-15** | SEC-R-04 | ⚠ **NO ROW AT ALL** — R-128's controls meanwhile | not evidence |
| **FR-P1-05-16** | SEC-R-04 | ⚠ **`Pending`** — approved under **D-32**, never run, NOT passed | not evidence |
| **FR-P1-05-18** | SEC-R-04 | ⚠ **`Pending`** — approved under **D-32**, never run, NOT passed | not evidence |
| **FR-P1-05-19** | SEC-R-03 | ⚠ **`Pending`** — approved under **D-32**, never run, NOT passed | not evidence |
| **FR-P1-05-20** | SEC-R-01, SEC-R-02 | ⚠ **`Pending`** — approved under **D-32**, never run, NOT passed | not evidence |
| **REQ-CLAIM-01** | SEC-R-03 | ⚠ **`Pending`** — `TST-CLAIMS-01` approved under **D-32**, never run, NOT passed | not evidence |
| FR-P1-03-4 | SEC-R-02 | TA-15 — row owned elsewhere | `Pending` |
| REQ-ENG-4 | SEC-R-04 | TA-09 — bounded scope | `Pending` |
| REQ-ENG-8 | SEC-R-04 | TA-16 | `Pending` |
| REQ-ENG-13 | SEC-R-04 | TA-16 | `Pending` |
| **FR-P1-05-3** | SEC-R-03 | ⚠ **NO ROW** — row owned by `models-and-baselines`, which proposes it | `Pending` — **the RF-importance non-authoritative rule SEC-R-03 quarantines** |
| **FR-P1-05-21** | SEC-R-01 | ⚠ **NO ROW** — row owned by `models-and-baselines`, which proposes it | `Pending` — **M-03 fitted on training partitions only, the control SEC-R-01 co-reports** |
| NFR-DQ-01 | SEC-R-04 | — | `Pending` |
| NFR-TDEF-01 | SEC-R-02 | — | `Pending` |

**Derived and printed**: 4 requirement sections (SEC-R-01…SEC-R-04); **19** coverage rows *(corrected 2026-09-01 on adversarial findings 1 and 2, both Major; superseded: **17**. **FR-P1-05-3** — RF importance never adds, removes or ranks a feature — is the rule § SEC-R-03 quarantines, and **FR-P1-05-21** — M-03 fitted on training partitions only — is stated verbatim inside § SEC-R-01's difficulty-controls text. Both were restated in substance and cited by neither ID. **This is the sixth consecutive unit on which this check found a defect**, and the third distinct cause: the map, then the NFR family, now requirements another unit owns whose substance this unit restates. The lesson recorded: **a unit's coverage table must cover every requirement whose text its artifacts reproduce, whoever owns the row.**)* — the
**11** the `functional-design` map carries, plus **FR-P1-03-4**, **REQ-ENG-4**, **REQ-ENG-8**,
**REQ-ENG-13**, **NFR-DQ-01** and **NFR-TDEF-01** (six), plus **FR-P1-05-3** and
**FR-P1-05-21** (two, added on the iteration-1 findings) — **11 + 6 + 2 = 19**; **9** carrying
no result — **5** approved-but-unrun under D-32, **2** genuinely rowless, and **the 2 newly
added, which are themselves no-result entries** *(decomposition and the no-result sub-count both
corrected 2026-09-01 on adversarial finding 4, Major; superseded: "11 the map carries, plus six
… 7 carrying no result". **The headline was bumped 17 → 19 and its own decomposition directly
below it was left reading 11 + 6 = 17** — the sweep-every-representation defect `project.md`
records twice, **committed by the repair that was fixing an instance of it**)*; **0** rows claimed satisfied.

## Assumptions & Open Questions

- **[Q1]** Both consumer refusals are **new at this stage**. **They will fail on every input until the producing halves land**, and neither producing half exists — `evaluation-and-comparison`'s field emission and `target-standardization`'s caveat field are both unbuilt.
- **[assumption]** A rendering path exists to attach the refusals to. **It does not** — no results table has ever been produced, and where the refusal sits in the rendering path is **owed at 3.5**.
- **[Q2]** The citation check is a **prose check** and is **weaker than a field check**. **An indirectly phrased citation evades it.** It **narrows** the quarantine gap and does not close it.
- **[assumption]** "Thesis-level locations" can be enumerated for the checklist to inspect. R-126 already inspects **named locations**, so the mechanism exists — but **which locations count as thesis-level is not fixed anywhere**, and a location added later is not automatically inspected. **Raised, not resolved.**
- **Carried — FR-P1-05-14 and FR-P1-05-15 have no acceptance row.** R-128's controls make them **mechanical**, which is **not the same as tested**. Whether to propose rows for them is a §15.2 act this artifact does not take, because the two sit differently from the five D-32 approved: the owner has already ruled once on this unit's row set.
- **Carried — five rows are approved but unrun.** D-32 approved them on **2026-08-28**; **none has been executed** and **approval is not evidence**.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `security-requirements.md` § SEC-R-03 / Sources / Requirement coverage table | **FR-P1-05-3 is uncited anywhere in either artifact, but its substance is stated verbatim in SEC-R-03.** `requirements.md` line 396: *"No Random Forest importance score adds, removes or ranks a feature into the production feature set; RF importance is saved only as a non-authoritative diagnostic figure [Vision §6.4] [TE §6.4]."* SEC-R-03's opening sentence: *"the Random Forest importance figure is non-authoritative — it may be saved as a diagnostic figure, and may never add, remove or rank a feature into the production set (Vision §6.4)"* — same rule, same authority citation (Vision §6.4), same substance, and this unit is the reporting/diagnostics unit where an RF-importance figure would actually be rendered and cited. Neither the Sources list (line 25) nor the 17-row coverage table names `FR-P1-05-3`. This is the sixth consecutive unit's completeness miss, and it is exactly the pattern the dispatch brief warned of: substance present, ID uncited. | Add `FR-P1-05-3` to Sources and as an eighteenth coverage row (status `Pending`/`UNTESTED`, matching `requirements.md`'s own `UNTESTED` status for it), tracing to SEC-R-03. |
| 2 | Major | `security-requirements.md` § SEC-R-01 / Sources / Requirement coverage table | **FR-P1-05-21 is uncited anywhere in either artifact, but its substance is stated verbatim in SEC-R-01.** `requirements.md` line 414: *"M-03's fitting partition. The station×month×hour climatology is fitted on training partitions only and is never fitted using validation or December data."* SEC-R-01's first requirement: the three difficulty controls include *"fitted station×month×hour climatology (trained on training partitions only)"* — the identical constraint (M-03's train-only fitting), stated as part of what SEC-R-01 requires the primary results table to co-report, yet FR-P1-05-21 appears in neither the Sources list nor the coverage table of either artifact. | Add `FR-P1-05-21` to Sources and as a coverage row against SEC-R-01, tracing the "trained on training partitions only" clause to it. |
| 3 | Major | `tech-stack-decisions.md` § TS-R-02 body vs. § Assumptions & Open Questions | **TS-R-02's rule body overstates the guarantee its own Assumptions concede is partial.** The body states flatly: *"presentation-only by signature"*, *"Constraining the signature makes the second computation unrepresentable rather than discouraged"*, and *"No plotting-adjacent statistics"* as an unqualified declarative — read on its own, this claims the signature constraint alone rules out `seaborn` computing a plotting-adjacent statistic. The Assumptions section then concedes: *"A signature constrains inputs, not which library calls a module makes — so this rests partly on review rather than wholly on mechanism, and that is a weaker guarantee than TS-R-02's framing might suggest."* This is the same rule-body-vs-Assumptions misplacement `project.md`'s learnings log has flagged as a recurring Major on this exact stage (`fd-2026-08-30-sweep-numerals-and-surfaces`: "a rule's own Rule statement... kept asserting the superseded/overstated version" while the caveat sat only in Assumptions). A reader of TS-R-02's Decision text alone would not learn that `seaborn`'s statistical drawing functions are kept out only "partly" by mechanism and partly by review discipline. | Move the concession ("rests partly on review, not wholly on mechanism") into TS-R-02's own Decision/body text, not only the Assumptions bullet — the same fix already correctly applied to SEC-R-03/TS-R-04's citation-check weakness, which states its "narrows, does not close" admission in the rule body itself. |

### Validation Tool Results

No stage-listed validation tool was run (none is named for `nfr-requirements` in the stage definition available to this pass); findings above were derived by direct ID set-differencing between `requirements.md`'s enumerated `FR-P1-05-*` family (21 IDs, printed via grep) and the IDs cited in this unit's two artifacts' Sources sections and coverage tables (9 FR-P1-05-* IDs cited: -9, -10, -11, -14, -15, -16, -18, -19, -20). The arithmetic claim "nine fewer than seventeen" in `tech-stack-decisions.md` was re-derived: `security-requirements.md`'s table has 17 rows (counted), `tech-stack-decisions.md`'s has 8 (counted), 17 − 8 = 9 — confirmed correct. `security-requirements.md`'s own printed derivation (4 sections, 17 rows, 7 no-result: 5 D-32-pending + 2 rowless) was recounted directly from its table and confirmed correct.

### Coverage limits

Budget did not permit reading this unit's own `functional-design/` map to cross-check the "11 the functional-design map carries" claim, the eleven-NFR-ID set-difference in full (spot-checked only NFR-REP-01, whose subject — clean-CPU exact-equality reproducibility — is plausibly out of this unit's domain and not flagged), or the remaining FR-P1-05-1/2/4–8/12/13/17/22 IDs against this unit's narrower domain boundary. The two FR-P1-05 misses above were confirmed by direct textual match against this unit's own rule bodies, not by exhaustive domain analysis of every uncited ID.

### Summary

Two more substance-present/ID-uncited completeness gaps continue the streak the dispatch brief flagged across five prior units, now landing on the NFR family's home unit itself (FR-P1-05-3's RF-importance rule and FR-P1-05-21's train-only climatology-fitting rule are both stated verbatim in this unit's own SEC-R rules but never cited). A third Major repeats a previously-flagged defect pattern: TS-R-02's rule body claims a stronger guarantee ("presentation-only by signature," unqualified) than its own Assumptions section admits the mechanism actually provides. The two refusal mechanisms, the honesty-rule framing, the counts, and the arithmetic cross-check all held up under adversarial testing — the failures are confined to citation completeness and one rule-body/Assumptions mismatch, not to the substantive design.

NOT-READY

## Review — iteration 2 (terminal)

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:45:43Z
**Iteration:** 2 (terminal — advisory to the human gate, no further repair cycle behind this pass)

### Findings 1 & 2 (iteration 1) — CONFIRMED RESOLVED

`FR-P1-05-3` and `FR-P1-05-21` are now both present in the Sources line (line 25, alongside the rest of the `FR-P1-05-*` family) and as explicit coverage-table rows (lines 191–192), each carrying the quarantined-rule substance and the `models-and-baselines` ownership note. Verified by direct grep against the artifact — landed as claimed.

### New finding — the row-count repair is internally inconsistent (Major)

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 4 | Major | `security-requirements.md` § "Derived and printed" paragraph, immediately below the coverage table | **The headline total was corrected (17 → 19) but the sentence's own decomposition was not, and it no longer sums to the total it introduces.** The paragraph reads "**19** coverage rows ... — the **11** the `functional-design` map carries, plus **FR-P1-03-4**, **REQ-ENG-4**, **REQ-ENG-8**, **REQ-ENG-13**, **NFR-DQ-01** and **NFR-TDEF-01** ... ; **7** carrying no result ... ; **0** rows claimed satisfied." 11 + 6 = **17**, not 19 — the decomposition still describes the pre-repair table and never mentions `FR-P1-05-3` or `FR-P1-05-21` as part of what makes up the 19. The "**7** carrying no result — 5 D-32-pending, 2 rowless" count is stale in the same way: both new rows are themselves no-result entries (`Pending`, "NO ROW — owned by `models-and-baselines`"), so the true no-result count is now 9, not 7, and "matching the map exactly" is no longer a checkable claim against the printed breakdown. This is exactly the defect pattern `project.md`'s own learnings log names twice over — `fd-2026-08-30-sweep-derive-sites` (repair scoped to a finding's enumerated sites leaves other representations of the same fact standing) and the `count-derivation` rule (derive and print a count from the artifact, never carry it from an earlier revision) — reproduced by the repair itself: the two Major citation fixes were applied to the table and the headline number, but not propagated into the sentence that explains the number. | Recompute and reprint the decomposition: state which 13 items make up the "map-plus-named" component (11 map + FR-P1-05-3 + FR-P1-05-21, or reclassify however the two new rows actually fit), and correct "7 carrying no result" to 9 (5 D-32-pending + 2 rowless + 2 owned-elsewhere-pending). Do this by re-deriving from the table directly, not by incrementing the old numbers. |

### Finding 3 (iteration 1, TS-R-02) — NOT VERIFIED THIS PASS (flag, not a clearance)

This pass's tool-call budget was exhausted confirming Findings 1/2 and the row-count arithmetic above before the TS-R-02 body in `tech-stack-decisions.md` could be re-read directly (an early grep aimed at "TS-R-02" was mistakenly run against `security-requirements.md`, which only surfaced iteration 1's own `## Review` text quoting TS-R-02 — not the live rule body in the other file). The dispatch brief's description of the fix (a boxed split-guarantee caveat now in the decision body) is **not independently confirmed by this pass**. Per `project.md`'s "do not report as newly discharged" convention and the standing rule against treating a described repair as landed without verification, this finding is carried forward **open** rather than cleared.

### Dependent arithmetic check (`tech-stack-decisions.md`)

Confirmed by direct count: `tech-stack-decisions.md`'s coverage table has exactly **8** rows (`REQ-ENG-12`, `FR-P1-05-9`, `FR-P1-05-11`, `FR-P1-05-19`, `FR-P1-05-20`, `REQ-CLAIM-01`, `REQ-ENG-13`, `NFR-TDEF-01`). `security-requirements.md`'s printed total is **19**. 19 − 8 = 11, matching the corrected "**eleven fewer** than ... **nineteen** (superseded: 'nine fewer than seventeen')" phrase at `tech-stack-decisions.md` line 171. This dependent figure is correct even though the source paragraph it depends on (Finding 4 above) is internally inconsistent.

### Eleven-NFR-ID set-difference (owed from iteration 1's coverage limits)

`requirements.md`'s eleven NFR IDs: `NFR-AUD-01, NFR-DET-01, NFR-DQ-01, NFR-FAIR-01, NFR-IRI-01, NFR-LEAK-01, NFR-LIC-01, NFR-PHASE-01, NFR-REP-01, NFR-SEC-01, NFR-TDEF-01`. Cited across this unit's two artifacts: `NFR-DQ-01, NFR-REP-01, NFR-TDEF-01` only. The other eight are uncited in both artifacts. No textual match was found for their substance inside this unit's SEC-R/TS-R rule bodies on inspection of the rules already read in this and the prior pass (e.g. `NFR-IRI-01`, `NFR-LEAK-01`, `NFR-PHASE-01` govern raw-processing/training-time concerns outside a reporting/diagnostics unit's domain; `NFR-AUD-01`/`NFR-SEC-01`/`NFR-LIC-01`/`NFR-FAIR-01` are plausibly other units' concerns). This is consistent with — not a contradiction of — the artifact's own domain-boundary framing, so it is **not raised as a new finding**, but it was not exhaustively re-verified against full rule-body text in this budget-constrained pass and should not be read as a clean bill of health beyond the spot-check basis stated here.

### Summary

Two of the three iteration-1 Majors are confirmed resolved by direct evidence. The third (TS-R-02) could not be independently re-verified this pass and is carried forward open rather than credited. Separately, the repair to Majors 1–2 introduced a fresh, evidence-backed Major: the coverage table's own explanatory arithmetic ("11 + 6 = 19"; "7 carrying no result") was not recomputed after the two new rows were added, so the artifact's printed self-check no longer matches its own table — the same "propagate the fix into every representation, not just the enumerated site" failure this stage's memory already names twice. With one carried-open Major, one new Major, and this being the terminal pass with no further repair cycle behind it, the verdict is NOT-READY; both should go to the human as gate input.

NOT-READY

## Review — 2026-09-01 re-verification after gate rejection

**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 2 (fresh budget after human gate rejection of terminal iteration-2 NOT-READY)

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | — (verification, no defect) | `security-requirements.md` "Derived and printed" paragraph | The original Major is repaired and independently re-verified: counted the coverage table directly (19 rows) and re-derived the decomposition myself — 11 (map) + 6 (FR-P1-03-4, REQ-ENG-4, REQ-ENG-8, REQ-ENG-13, NFR-DQ-01, NFR-TDEF-01) + 2 (FR-P1-05-3, FR-P1-05-21) = **19**, matches. No-result sub-count re-derived from the table's `Pending`/no-row markings: 5 D-32-approved-unrun (FR-P1-05-16, -18, -19, -20, REQ-CLAIM-01) + 2 genuinely rowless (FR-P1-05-14, -15) + 2 newly added rowless (FR-P1-05-3, -21) = **9**, matches the stated figure. No new counting defect found here. | None — verified correct. |
| 2 | — (verification) | `security-requirements.md` banner (lines 7–19); `tech-stack-decisions.md` banner | Both banners independently re-derived and confirmed: `security-requirements.md` states 19 covered / 9 no-result and separately preserves the map's 11/7 as a labelled sub-breakdown, naming FR-P1-05-3 and FR-P1-05-21 as additionally rowless. `tech-stack-decisions.md`'s banner states four rowless (FR-P1-05-14, -15, -3, -21), consistent with the primary artifact. No fifth stale representation found at either banner. | None. |
| 3 | — (verification) | `tech-stack-decisions.md` "eleven fewer than nineteen" phrase | Counted both tables directly: `security-requirements.md` = 19 rows, `tech-stack-decisions.md` = 8 rows (REQ-ENG-12, FR-P1-05-9, FR-P1-05-11, FR-P1-05-19, FR-P1-05-20, REQ-CLAIM-01, REQ-ENG-13, NFR-TDEF-01). 19 − 8 = 11, matching the stated "eleven fewer". Confirmed correct. | None. |
| 4 | Minor | `security-requirements.md`, prior review's own "Budget did not permit" note | The prior iteration's limitation note (FR-P1-05-1/2/4–8/12/13/17/22 not exhaustively checked against this unit's domain boundary, and the full 11-NFR-ID set-difference not completed) is still true of this pass too: this pass's budget did not permit an exhaustive domain-boundary check of the ten uncited `FR-P1-05-*` IDs or the eleven-NFR-ID sweep named in the dispatch beyond the spot-check already recorded. This is carried forward as a disclosed limitation, not a discovered defect — no textual match was found showing this unit's rule bodies restate the substance of any of the ten uncited IDs. | A future pass with budget for the full `functional-design/business-logic-model.md` cross-check and the complete 11-NFR-ID set-difference should close this out explicitly rather than carry it indefinitely. |

### Standing content — no regression found

- § SEC-R-02: both consumer refusals (estimand orientation/weighting; lineage caveat) still stated as hard failures that fail on every input until the producing halves land ("`evaluation-and-comparison`'s field emission and `target-standardization`'s caveat field are both unbuilt"); neither declared satisfied. Confirmed present, unchanged in substance.
- § SEC-R-03: the citation-check prose-check weakness ("A prose check is weaker than a field check... An indirectly phrased citation evades it") is stated in the **rule body itself**, not only in `## Assumptions & Open Questions`. Confirmed.
- `tech-stack-decisions.md` § TS-R-02: the boxed caveat — a signature constrains what a function is GIVEN, not what it DOES, so the no-derived-statistics half rests on review — confirmed present and unchanged.
- No-results-table status, D-32 Pending rows, TA-16/TA-19/TA-20/WS-19 undischarged, G-09/D-31 preconditions unmet, stage 3.1 FAIL, `configs/` absent — all still stated as such; nothing newly claimed discharged.

### Validation Tool Results

| Tool | Result | Interpretation |
|---|---|---|
| (none stage-listed) | N/A | No validation tool is named for `nfr-requirements` in the stage definition available to this pass; findings above were derived by direct table counts and ID grep against `inception/requirements-analysis/requirements.md`'s full `FR-P1-05-*` family (22 IDs, printed), not by an automated tool. |

### Summary

The Major that made iteration 2 terminal NOT-READY — the stale "11 + 6 = 17" decomposition and stale "7 carrying no result" sub-count sitting below a headline already corrected to 19 — is repaired and this pass independently re-derived every number involved (table row counts, decomposition, no-result sub-count, both banners, and the dependent "eleven fewer than nineteen" arithmetic) rather than trusting the repaired text. No sixth stale representation was found. One Minor carries forward: the domain-boundary check against the ten uncited `FR-P1-05-*` IDs and the full 11-NFR-ID set-difference remain budget-limited rather than exhaustively closed, as already disclosed in the artifact itself. Zero Critical, zero Major.

READY
