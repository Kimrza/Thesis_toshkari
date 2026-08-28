# Functional Design Questions — `regimes-diagnostics-reporting`

**Unit** `regimes-diagnostics-reporting` — Regimes, Diagnostics and Reporting: breakdowns,
figures, claims.
**Kind** `library` · **Complexity** L · **Deployment** embedded · **Depends on**
`statistical-inference`.

Unit **11 of 12**. It owns **3 `src/` modules, 4 notebooks and 1 checklist artifact —
derived by counting § 11's `Owns` list**: `src/evaluation/regimes.py`, `diagnostics.py`,
`plots.py`; the four analysis/review notebooks (`01_data_and_target_audit`,
`02_processor_verification`, `03_features_and_splits_review`, `04_results_and_figures`);
and the claims-and-limitations checklist artifact. It owns no stage script: it runs inside
`scripts/07_evaluate_and_report.py`, which `evaluation-and-comparison` owns, and inside the
four review notebooks. `plots.py` is **presentation only and computes no reported
quantity**. Its responsibility is everything between a computed interval and a defensible
statement: the Kp/Hp60 regime strata and the §9.3 storm-event rule, quality strata over
the measured-available fields with the top-1%-removed sensitivity, the required
prediction/residual/target-support/quality plots each carrying its source-data IDs, the
primary results table with its three mandatory difficulty controls, the mandated
disclosures, and the claims-and-limitations checklist.

**Four inherited exit conditions stand on this stage: BLK-03 ↓, BLK-04 ↓, BLK-08 ↓,
BLK-09 ↓.** None is owned here. Every reported number, breakdown, figure and claim in this
unit derives from the confirmatory prediction and the transform-fitted features, so those
inherited contracts bound what may be claimed. **BLK-08 ↓ reaches the claims directly**:
the practical-relevance threshold comparison is stated in TECU, and until the co-owner
adopts its half of `evaluation-and-comparison`'s R-103 joint contract, no design path
returns model output to TECU. **BLK-09 ↓** — the fit those numbers rest on compares against
a training range no field states. All four are **exit conditions on stage 3.1, not entry
conditions** (`GOV-2026-08-22-REM-01` Rec 2, extended to BLK-08/BLK-09 on 2026-08-23):
this unit may enter, **may not complete or exit** 3.1 while any contract is unapproved,
and **no implementation may proceed** while they stand.

**11 requirements, 7 untested — derived by reading the story map's rows, and the two
upstream artifacts agree**: REQ-ENG-12 (TA-16), FR-P1-05-9 (TA-20), FR-P1-05-10 (TA-19),
FR-P1-05-11 (WS-19), and seven with **no current acceptance row** — FR-P1-05-14,
FR-P1-05-15, FR-P1-05-16, FR-P1-05-18, FR-P1-05-19, FR-P1-05-20, REQ-CLAIM-01. Per-unit
coverage summary row: 11 requirements, 7 untested, **primary WS-19, TA-16, TA-20 (3
rows)**, supporting **TA-19** (the target uncertainty budget: `target-standardization`
produces it, this unit reports it adjacent to the primary result). Seven untested of
eleven is a figure this file must convert into designed falsifiers or leave as recorded
gaps — never silently narrow.

**G-09 is not signed.** Workspace inspection 2026-08-27: `tests/` holds three modules
(`test_acquisition_window.py`, `test_phase_boundary.py`, `test_release_hashes.py`) — none
this unit's; `src/` and `configs/` are absent; `notebooks/` holds only
`madrigal_phase1_coverage_audit.ipynb`, the REQ-ENG-8 migration source whose target is this
unit. No answer here authorises creating any module.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 11 — the `Owns` list (3 modules + 4 notebooks + 1 checklist artifact), the boundary (runs inside `07` and the four notebooks; `plots.py` presentation only; a notebook never holds the only copy of parsing, calibration, feature, split, training, evaluation or bootstrap logic), the 11 requirements (7 bolded untested), acceptance rows WS-19/TA-16/TA-20, the six implementation notes (the FR-P1-05-18 advisory NOT-READY landing here; beats-the-LSTM disclosure in table **and** abstract-level conclusion; three controls co-reported in the same primary table; Phase-2-not-independent; the D-8 claim boundary and the NICO 5-minute bar; no practical-relevance threshold change after December opens and post-access changes labelled exploratory); **BLK-03/BLK-04/BLK-08/BLK-09** (all inherited, exit conditions, BLK-08's TECU reach into the claims).
- `../../../inception/units-generation/unit-of-work-story-map.md` — Table 1 rows for the 11 requirements (7 marked **NO CURRENT ACCEPTANCE ROW**); Table 2's WS-19 row (figure set, each carrying its source-data IDs), TA-16 row (notebook header declarations + acquisition-notebook/script diff), TA-19 row (primary `target-standardization`, supporting this unit — budget artifact + its placement in the results section), TA-20 row (primary results table with the three controls alongside the IRI comparison); § Per-unit coverage summary (11 / 7 / WS-19, TA-16, TA-20 / TA-19); § Cross-unit responsibilities (REQ-ENG-8: the coverage notebook migrates **here**; NFR-DQ-01/FR-P1-05-10/TA-19: production there, adjacent reporting here); the open-issues rows (FR-P1-05-18's missing source criterion — a `requirements.md` change).
- `../../../inception/requirements-analysis/requirements.md` — REQ-ENG-12 (the four declarations, no-only-copy, "Run all" stop semantics; the acquisition notebook excluded, governed by REQ-ENG-13 in another unit); FR-P1-05-9 (three controls in the primary table, never an appendix); FR-P1-05-10 (budget **contents, not existence** — the Phase 1-applicable contents plus the asymmetry statement, the four Phase 2 quantities recorded not-applicable per § Known defects row 11; top-1%-absolute-error-removed sensitivity); FR-P1-05-11 (plot manifest with source-data IDs); FR-P1-05-16 (the enumerated breakdowns: per-cell +1 h, equal-station macro headline, pooled row-weighted supplementary, quiet/disturbed/storm split, quality strata from **D-17's measured-available fields only** — `valid_observation_count`, `within_hour_spread_tecu`, `provider_dtec_summary`, no satellite/elevation/zenith stratum — daily error, four LST bins, **Vision §9.5's F1–F4 fold table**, **per-seed three-seed stability with mean and spread**; December regime results **descriptive only** unless at least three independent storm events); FR-P1-05-18 (four clauses: audit report registered pre-G-05 and performance-blind; demotion timestamp precedes the freeze; the three regime thresholds — quiet `Kp<4`, disturbed `Kp>=4`, storm `Kp>=5` — **asserted as configured values, read from configuration rather than recomputed per report**; the −12 h/+24 h event window; the count from **GFZ Kp/Hp60 at a recorded release grade**, D-11 barring any provisional-Dst-derived figure; D-13's three-independent-storm-events threshold with independence at >=24 h of `Kp<4`); FR-P1-05-14 (post-access changes labelled exploratory); FR-P1-05-15 (threshold timestamp precedes G-06; **descriptive-only when the reference is smaller than the budget**); FR-P1-05-19 (plasmaspheric disclosure at the table caption, the abstract-level conclusion, and the limitations section); FR-P1-05-20 (beats-the-LSTM disclosure in table **and** conclusion — `UNTESTED`, candidate TA row via Vision §15.2); REQ-CLAIM-01 (the checklist applied per prohibited class, the enumeration **maintained in § Out of scope C only**, cited not duplicated; `TST-CLAIMS-01` named by Vision §11.2 with no §16/§19 row — **adding a criterion is not adding an acceptance row**); § Cleanup row on `.dst_summary.json` (unmanifested December storm-day characterisation from **provisional** Dst — "the path of least resistance for filling the regime-count requirement with an input D-11 prohibits").
- `../../../inception/application-design/component-methods.md` § `src/evaluation` — the approved boundary call `count_storm_events(kp, *, release_grade: str, source: str)`: both **required arguments, not inferred**, raising `RegimeError` when `source` is not GFZ Kp/Hp60 or `release_grade` is absent — "as far as design can carry the open advisory finding"; § Depth (Q1 = B: full signatures at cross-package boundaries only; intra-package shapes are this stage's to specify, names indicative); § Assumptions (fourteen project exceptions declared where raised until 3.1 places them; **no signature encodes a scientific constant** — every threshold arrives through `ConfigSnapshot`); `src/data/locked_test.py`'s `purpose` enum (`"coverage_audit" | "regime_audit" | "locked_evaluation"`); the `Prediction` stamps `partition_id`/`transform_id` (ADR-11).
- `../../../inception/application-design/services.md` — `07_evaluate_and_report.py`'s row (reads predictions carrying `partition_id`/`transform_id`, benchmark, mask; writes metrics, bootstrap intervals, **breakdowns, figures**); the five notebooks as review and presentation surfaces (TE §7: notebooks do not own production logic); `experiment_registry.csv` derived, regenerated by folding the JSONL.
- `../evaluation-and-comparison/functional-design/` — **READY**: R-108 (`EstimandResult` carries the scalar, per-station components, orientation `benchmark_minus_model`, weighting `equal_station`, and the sign-convention sentence machine-readably; **this unit asserts the field's presence and does not restate the convention**); R-109 (the two-events boundary: the pre-G-05 coverage and regime audit is **`inventory-and-registry`'s** permitted performance-blind read; `07`'s December read arrives only through `open_restricted` purpose `"locked_evaluation"` post-receipt); R-110 (the split stated: completeness refusal upstream — a primary table missing M-02 impossible **upstream** of the table, the three controls computed there over the one frozen mask, **their co-reporting in the primary table is this unit's obligation**; the per-benchmark **`beats_model`** flag as the disclosure trigger; the spatial-representativeness sentence and `gim_network_overlap_flag` **emitted by the comparison-producing path** — this unit asserts presence); R-112 (`src/evaluation/` a path grant owned by three units). Rule IDs there run **R-103…R-112, derived by grepping its `business-rules.md` headings**.
- `../statistical-inference/functional-design/` — rules **R-113…R-122, derived the same way**: R-121 (the cross-station correlation carried machine-readably on `BootstrapResult`; this unit asserts the field's presence and restates nothing); R-120 (the widening-guard comparator's numbers **never serialized as a reported interval** — quarantined from every results artifact, table and notebook); `BootstrapResult`'s proposed fields (interval, level, sensitivity labelled and never merged).
- `../features-and-splits/functional-design/` — **FU-7 = A**: the G-06 locked test scores **2–31 December 2022, 30 days**, first 24 h excluded and counted; BLK-04/BLK-09's home.
- `../inventory-and-registry/functional-design/` — its assumption row: **D-13 owns the December regime-count threshold** — three independent storm events under Vision §9.3, counted from GFZ Kp/Hp60 at a recorded release grade, D-11 barring any provisional-Dst-derived figure; **"This unit measures against it"** — the pre-G-05 December coverage and regime audit is its read, not this unit's; membership from record timestamps, never directory names.
- `../external-products/functional-design/` — R-62 (Dst's three restrictions kept apart; **provisional grade renders the series ineligible** for a modelling input, a frozen tolerance, or a G-05 regime count, **asserted at the point of use**; `dst_provisional_202212.html` exists in the workspace); R-60 (the emit-from-the-producing-path pattern for mandated sentences, adopted by `evaluation-and-comparison` R-110 as well); the driver-alignment rule (Dst aligned to its own hourly averaging interval).
- `../models-and-baselines/functional-design/` — R-100 (RF importance never adds, removes or ranks a feature into the production feature set; the **production-path** negative control lives there; the importance score is saved as a **non-authoritative diagnostic artifact** — the figure rendered from it is this unit's surface); BLK-03's open contract limbs on the confirmatory prediction every reported number consumes.
- `../foundation/functional-design/business-rules.md` R-01 — all fourteen project exceptions derive from `IntegrityError` (base in `src/data/config.py`); **`RegimeError` is one of the fourteen, raised by this unit**, and foundation's OPEN cross-unit obligation requires each raising unit's 3.1 to declare its exception as an `IntegrityError` subclass; R-10 (report honestly even when reporting fails); R-15 (only `foundation` reads `configs/`); R-17 (docstrings).
- `aidlc/spaces/default/memory/project.md` § Mandated/Forbidden and `team.md` — Dst diagnostic/hindcast-only, never a confirmatory ML feature (TC-11); no Kyoto Dst grade mixing within one series (D-10.1); NEVER let December inform model/feature/threshold/hyperparameter selection — **the trigger is December being seen**, the pre-G-05 audit being exactly the channel the rule closes (ML-02); the pre-G-05 audit kept performance-blind and recorded (Vision §8.3, R-13); the three difficulty controls co-reported in the same primary table (PC-03/PC-04); any baseline beating the LSTM disclosed in table and abstract-level conclusion; the spatial-representativeness statement wherever an IRI/GIM comparison is reported (TEC-06); the Phase-2-not-independent disclosure at abstract-level interpretation (VAL-05); claim boundary D-8 and the NICO 5-minute bar (D-7); no practical-relevance threshold change after December opens (PC-09); RF importance never a selection input; stamps `phase_id`/`source_id`/`target_definition_id` on every dataset, prediction, mask and comparison (TEC-05); notebooks own no production logic (§14, §7); no scientific constant in source (TC-03e); the two-tier error posture; the negative-control-per-hard-rule methodology; TE §18.3's stop-and-report posture.
- `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §14 (notebook obligations, both classes); §13.5 (per-seed reporting); §12 (the `tests/` tree — **its seventeen named modules include none for regimes, diagnostics, plots or claims**, derived by scanning the list); §9.3 via Vision (regime thresholds, event definition, analysis window).
- Workspace inspection, 2026-08-27: `tests/` holds three modules, none this unit's; `src/` and `configs/` absent; `notebooks/madrigal_phase1_coverage_audit.ipynb` present; `.dst_summary.json` at the repository root; `evidence/audit_ec1_2026-08-15/kyoto_dst/dst_provisional_202212.html` present.
- Absent by scope design: `stories` (2.4 `SKIP`), `mockups` (1.6 and 2.5 `SKIP`). `kind: library`.

---

## Question 1

**Regime classification: one copy, configured thresholds, and the guarded count.** Vision
§9.3's values are frozen and carried in FR-P1-05-18: quiet `Kp<4`, disturbed `Kp>=4`,
storm `Kp>=5`; an event is a contiguous `Kp>=5` interval with independence at >=24 h of
`Kp<4`; the analysis window is −12 h to +24 h; D-13 freezes the three-independent-events
threshold. Criterion clause 3 requires the thresholds **asserted as configured values —
read from configuration rather than recomputed per report** — and clause 4 fixes the
window span. The one approved boundary call, `count_storm_events(kp, *, release_grade,
source)`, raises `RegimeError` when `source` is not GFZ Kp/Hp60 or the grade is absent.
Unstated: where the hour-classifier lives, whether the pre-G-05 audit
(`inventory-and-registry`'s read) and this unit's regime breakdowns share one copy — H4's
fate and the general storm-claim rule turn on **one measured quantity** by D-13's design —
and which violations are proven caught.

A) Each consumer classifies inline: the audit, the breakdowns and any figure compute their own quiet/disturbed/storm labels from the Kp series with the thresholds as local constants
   > **Impact**: Violates TC-03e (a scientific constant in source) and FR-P1-05-18 clause 3 directly, and splits D-13's one measured quantity into copies that can drift — an audit count and a breakdown count that disagree would be uninterpretable at G-05.

B) One classifier in `src/evaluation/regimes.py`: an hour-classification function reads the three thresholds and the −12 h/+24 h window from `experiment.yaml` via `ConfigSnapshot` (encoding frozen values, deciding nothing); `count_storm_events` is the **only** counting path, implementing D-13's event and independence definitions; every consumer — this unit's regime split and `inventory-and-registry`'s pre-G-05 audit alike — calls these and never reclassifies
   > **Impact**: Clause 3 is satisfied by construction and the storm-event rule has exactly one copy, so the audit count, the H4 demotion decision and the descriptive-only guard all turn on the same computation. Costs the config keys, which are `foundation`'s surface to schema.

C) B, plus the negative controls: an hour at the boundary values misclassified (a `Kp>=4` hour labelled quiet, a `Kp>=5` hour not labelled storm) **fails**; a window of any span other than −12 h/+24 h **fails** (clause 4); a non-GFZ source or an absent release grade **raises `RegimeError`**; a provisional-Dst-derived series offered as the count's input **raises** — with `.dst_summary.json` (the VAL-11 custody item, present in the workspace today) named as exactly the path of least resistance this control closes; and `RegimeError` is declared here as an `IntegrityError` subclass, discharging foundation R-01's cross-unit obligation for this unit
   > **Impact**: FR-P1-05-18's clauses 3–4 and D-11's prohibition get their violation-is-caught proofs — as far as design can carry the advisory NOT-READY, whose missing source criterion remains a `requirements.md` change outside this stage. Costs four fixture cases on synthetic Kp series.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. D-13 deliberately collapsed H4's fate and the storm-claim guard onto one measured quantity; only a single classifier copy preserves that collapse, and the provisional-Dst control is the executable form of the one restriction D-11 states three ways. A is barred by two affirmed rules; B without C leaves the unit's hardest rule without the proof the affirmed methodology demands.

[Answer]: C

---

## Question 2

**The December channel: what lands here versus `inventory-and-registry`, and how regime
reporting avoids becoming the ML-02 channel.** The pre-G-05 December coverage and
regime-count audit is required, performance-blind, and **not this unit's read** — it is
`inventory-and-registry`'s lane (R-13; `evaluation-and-comparison` R-109 states the
two-events boundary; `locked_test.py` carries the distinct purposes `"coverage_audit"` /
`"regime_audit"` / `"locked_evaluation"`). ML-02's rule names the audit as precisely the
channel through which December is legitimately **seen**, and closes it: nothing
December-derived may inform model, feature, threshold or hyperparameter selection. This
unit computes December regime **performance** breakdowns — which exist only after G-06 —
and enforces FR-P1-05-16's storm-claim guard (December regime results descriptive only
unless at least three independent storm events) and FR-P1-05-18 clause 2 (a demotion
recorded after the G-05 freeze is invalid rather than corrected). Unstated: how the
breakdown path is gated, and where the guard's count comes from.

A) Sequencing by process: `07` runs after G-06 in practice, and the notebooks are trusted not to compute December regime performance early
   > **Impact**: The guarantee holds for one caller's call order only — `04_results_and_figures.ipynb` reads serialized artifacts directly, and nothing would stop a pre-G-06 December regime-performance figure, which is the ML-02 channel reopened at exactly the surface the rule was written about.

B) December-blind by signature, post-receipt by construction: the hour-classifier consumes only the Kp driver series and configured thresholds — never a December target or prediction value — so classification itself cannot see December; and every regime **performance** breakdown over a `DEC`-partition result is computed only from `evaluation-and-comparison`'s emitted metrics artifact, which cannot exist before R-109's verified hash receipt — the breakdown functions take the artifact, not raw predictions
   > **Impact**: This unit cannot become the pre-G-05 December performance channel: the only inputs its December-touching paths accept either carry no December information (Kp) or provably post-date the receipt. The audit's regime counts remain `inventory-and-registry`'s performance-blind read, untouched.

C) B, plus the two executable guards: December regime results are labelled **descriptive-only unless** the registered pre-G-05 audit artifact records >=3 independent storm events — the count **read from the registered December regime-count audit report, never recomputed here from December data**, so one measured quantity governs both the guard and H4's fate; and the H4/SRQ-5 demotion record's timestamp is asserted to precede the G-05 freeze, a post-freeze demotion failing rather than being corrected; negative controls for a missing descriptive-only label when the count is below three and for a post-freeze demotion record
   > **Impact**: FR-P1-05-16's storm guard and FR-P1-05-18 clauses 1–2 become checks instead of prose, and the guard consumes the audit's registered artifact rather than duplicating its read — the split R-109 stated survives into this unit's mechanics. Costs one artifact read and two fixture cases.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. The board wrote ML-02 about exactly this seam, and B is the only shape under which this unit's regime reporting is December-blind where it must be and receipt-gated where it may see December at all; C adds the guard that keeps a thin December (fewer than three events) from silently carrying confirmatory storm claims, reading the one registered count instead of minting a second.

[Answer]: C

---

## Question 3

**The primary results table as an executable contract.** FR-P1-05-9/TA-20 require the
three difficulty controls (M-01 persistence, M-02 24-hour seasonal persistence, M-03
fitted climatology) co-reported **in the primary results table**, never an appendix.
`evaluation-and-comparison` R-110 has already done the upstream half and **stated the
split**: its evaluation run refuses to emit a results artifact with any declared member's
metric missing, computes the controls over the one frozen mask, and carries a per-benchmark
`beats_model` flag and R-108's orientation/sign-convention fields — **the co-reporting in
the table is this unit's obligation**. TA-19 places the target uncertainty budget adjacent
to the primary result. BLK-08 reaches the table directly: its numbers are TECU-denominated
only if the inverse path is adopted. Unstated: what builds the table, and what refuses.

A) The table is assembled in `04_results_and_figures.ipynb` from the serialized artifacts, with the co-reporting and adjacency obligations documented in prose
   > **Impact**: A notebook could omit a control or the budget without anything firing, TA-20's evidence has no producing path, and §14 bars a notebook holding the only copy of evaluation logic — the gap class R-110's own limb 3 was written to close.

B) A producing path in `diagnostics.py` builds the table from the emitted metrics artifact: it **refuses to render** when any declared primary member's metric is absent (consuming R-110 limb 1's completeness refusal rather than re-checking membership); all three controls and the IRI comparison land in the **same table by construction**, appendix relegation unrepresentable; R-108's orientation, weighting and sign-convention fields are asserted **present** and printed from the artifact, never restated; the uncertainty budget artifact is read and placed adjacent (TA-19's supporting evidence), with FR-P1-05-10's Phase 1-applicable contents and asymmetry statement asserted non-empty and the four Phase 2 quantities shown as recorded not-applicable
   > **Impact**: TA-20's evidence is the artifact this path emits, and the three failure modes the honesty rules name — a missing control, an appendix table, a sign convention remembered rather than asserted — become impossible or loud. Costs one rendering function and its artifact reads.

C) B, plus the disclosure trigger and the units check: every benchmark row prints its `beats_model` flag, and any true flag enrols that baseline in Question 4's abstract-level check — the field comparison R-110 limb 2 built the flag for; the table's units are asserted from the artifact's units metadata as TECU rather than assumed (BLK-08's bound made checked, not silent); negative controls: a table rendered with a declared member missing **fails**, a control placed outside the primary table **fails** the same-table assertion, a benchmark row without a `beats_model` field **fails**
   > **Impact**: The project's highest-rated reporting risk (R-16) stays a field comparison end to end, and the TECU assertion makes this unit's dependence on BLK-08's resolution explicit at the exact surface the register says it reaches. Costs three assertions and their fixtures.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. R-110 built the upstream mechanics precisely so this unit's table could be a consumer of checked fields rather than a re-deriver of prose; C completes that contract at the table and points the `beats_model` flag at the disclosure obligation it exists to serve, with the BLK-08 units bound surfacing where the register says it lands.

[Answer]: C

---

## Question 4

**The mandated disclosures and the claims-and-limitations checklist: checks where
checkable, recorded obligations where not.** Five disclosure obligations converge on this
unit's prose surfaces: FR-P1-05-20 (any baseline beating the LSTM appears in the primary
table **and** the abstract-level conclusion — `UNTESTED`); FR-P1-05-19 (the plasmaspheric
offset disclosed at three interpretation points: table caption, abstract-level conclusion,
limitations section — `UNTESTED`); VAL-05 (Phase 2 stated as a fixed-protocol replication,
**not** a second statistically independent blind test, at abstract-level interpretation);
the spatial-representativeness sentence at every IRI/GIM comparison report (emitted by
`evaluation-and-comparison`'s producing path per R-110 limb 3 — this unit asserts
presence); and REQ-CLAIM-01 (no claim outside the frozen D-8 boundary; the prohibited-class
enumeration **maintained in § Out of scope C only**, cited not duplicated; the NICO
5-minute bar). `TST-CLAIMS-01` is named by Vision §11.2 but has no §16/§19 row, and adding
one is a Vision §15.2 amendment this stage may not make.

A) All five are documented obligations, verified by human review of the thesis text
   > **Impact**: The strongest honesty rules in the project — including the one the register rates its highest reporting risk — would rest entirely on recall at writing time, when four of the five have machine-checkable halves the design can bind now.

B) The claims-and-limitations checklist is a **machine-readable artifact produced by a path in `diagnostics.py`**: one row per prohibited class, citing § Out of scope C's enumeration by reference and recording each class unasserted across every reported artifact; plus one row per mandated disclosure — each `beats_model = true` baseline found in the conclusion text, FR-P1-05-19's sentence found at each of its three points, VAL-05's sentence found at the abstract-level interpretation, the spatial-representativeness sentence asserted present on every serialized IRI/GIM comparison, the D-8 boundary and NICO statements present — each row recording where the text was found, or failing
   > **Impact**: REQ-CLAIM-01's criterion is implemented as it is written (the checklist applied per prohibited class), and prose obligations become presence checks against named locations. The residue that stays human — whether found text *means* what the rule requires — is recorded as such rather than claimed covered.

C) B, plus the controls and the routing: negative controls that a `beats_model = true` baseline absent from the conclusion **fails**, a caption missing the plasmaspheric sentence **fails**, and a prohibited-class phrase planted in a reported artifact **is caught**; and the acceptance-row gap is routed to the gate as Vision §15.2 **proposals, proposed not applied** — candidate rows for FR-P1-05-20 and FR-P1-05-19 (both named as candidates in `requirements.md`) and for `TST-CLAIMS-01`, with the checklist artifact named as the evidence each row would point at
   > **Impact**: The three most consequential disclosure rules get violation-is-caught proofs, and the seven-untested figure this unit carries starts shrinking through the front door — the owner rules on the rows; nothing is minted here. Costs three fixtures and one gate item.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. Every one of these rules exists because silence at exactly these locations is the failure — a presence check at a named location is the strongest guarantee design can give, and C routes the missing acceptance rows to the only authority that can create them instead of leaving seven untested requirements untested by default.

[Answer]: C

---

## Question 5

**The breakdowns: producing paths, the D-17 strata bound, and stamps.** FR-P1-05-16
enumerates the required breakdowns: per-cell metrics at +1 h; equal-station macro-average
**as the headline**; pooled row-weighted as supplementary; the quiet/disturbed/storm split;
observation-quality strata computed **from D-17's measured-available fields only** —
`valid_observation_count`, `within_hour_spread_tecu`, `provider_dtec_summary`, with no
stratum on satellite count, elevation or zenith angle, none of which exists on the
five-column product; daily error; four LST diagnostic bins; Vision §9.5's F1–F4
validation-fold table; and per-seed three-seed stability reported per seed **with the mean
and the spread**, not the mean alone. FR-P1-05-10 adds the top-1%-absolute-error-removed
sensitivity. Every dataset, prediction, mask and comparison is stamped `phase_id`,
`source_id`, `target_definition_id` (TEC-05), and the two-tier error posture applies. The
requirement is `UNTESTED` — WS-19 reaches plots only.

A) Breakdowns are computed at reporting time in the results notebook, one cell per breakdown
   > **Impact**: §14 and the no-only-copy rule are violated the moment a breakdown exists nowhere else, a missing breakdown is invisible until a reader looks for it, and nothing stops a stratum quietly keyed on a field the product does not carry.

B) Each named breakdown is a producing function in `diagnostics.py` emitting a machine-readable artifact stamped with the three IDs: the quality-strata surface accepts **only** the three D-17 field names (an enumerated set from config, not free strings — a stratum on any other field is unrepresentable by signature); headline/supplementary is a **label carried on the artifact**, equal-station macro being the headline value; per-seed stability emits the three per-seed values, the mean and the spread as separate fields; the top-1% sensitivity is emitted beside its parent figure, labelled sensitivity; completeness shortfalls are machine-readable fields on the artifact, never console text, per the affirmed two-tier posture
   > **Impact**: The breakdown set is a checkable inventory rather than a notebook's table of contents, and the D-17 bound — written because the previous draft invented strata the data cannot support — becomes structural. Costs the enumerated-field config surface.

C) B, plus the negative controls: a stratum requested on a non-D-17 field **fails**; a pooled row-weighted figure labelled headline **fails**; a fold table missing any of F1–F4 **fails**; per-seed stability reported as mean-only **fails**; an artifact missing any of the three stamps **fails**; and the emitted inventory is asserted complete against the configured breakdown list — a missing declared breakdown refuses the results artifact rather than shipping partial
   > **Impact**: FR-P1-05-16 — untested, and the longest single criterion this unit carries — gets a falsifier per named clause, and the refusal mirrors R-110 limb 1's shape one level down. Costs six fixture cases, all synthetic.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. This requirement's history is exactly two rounds of governance adding clauses because breakdowns were collapsed or invented; B makes the enumeration structural and C makes each clause falsifiable, which is the only currency the §16/§19 acceptance vocabulary accepts.

[Answer]: C

---

## Question 6

**Practical relevance and post-access discipline: two untested requirements with
mechanics.** FR-P1-05-15: the threshold record's timestamp precedes G-06, and — Vision
§5.4's first constraint — where the practical-relevance reference is **smaller than the
target uncertainty budget**, practical relevance is **descriptive only** and may not be
claimed as a result. The comparison is stated in TECU, which is BLK-08's direct reach into
this unit's claims. FR-P1-05-14: any test-driven change made after locked-test access is
labelled exploratory in the registry. Both are `UNTESTED`, and no design yet states how
either becomes a check.

A) Both are checklist rows in Question 4's artifact and nothing more
   > **Impact**: The timestamp ordering and the smaller-than-budget comparison are numeric facts a path can assert; leaving them as prose rows spends the checklist's credibility on items that never needed to be prose.

B) The practical-relevance comparison is a producing function: it reads the threshold record with its timestamp and FR-P1-05-10's budget artifact; asserts the threshold timestamp precedes the G-06 receipt's; computes the reference-versus-budget comparison and, when the reference is the smaller, **emits the descriptive-only label on every practical-relevance statement** — a claim without the label is unrepresentable because the producing path is the only source of the statement; and the comparison **refuses** when either input's units metadata is not TECU (BLK-08's bound checked at the exact comparison the register names)
   > **Impact**: PC-09's freeze and §5.4's demotion become mechanical, and the one comparison BLK-08 reaches by name carries its own units guard. Costs two artifact reads and a label field.

C) B, plus FR-P1-05-14's reporting-side assertion and the honest boundary: every run this unit reports whose registry timestamp postdates a recorded `locked_test_accessed = true` event is asserted to carry the exploratory label — **a post-access run reported without the label fails** — while the question of which surface *writes* the label (the registry writer is `foundation`/`inventory-and-registry` territory) is routed to the gate rather than annexed; negative controls for a post-G-06 threshold edit and for the missing exploratory label
   > **Impact**: This unit checks what only it can see — the reporting surface — and does not trespass on the registry writer's design; the seam is put to the owner instead of papered over. Costs one assertion, one gate item, two fixtures.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. Both requirements protect the locked test's meaning after the fact, which is this unit's whole jurisdiction; B mechanises the two numeric halves, and C adds the one assertion this unit can honestly make about the exploratory label while routing the writer question to the gate — the same narrowing-not-relocating shape the project's rules keep demanding.

[Answer]: C

---

## Question 7

**Plots: presentation-only enforced, and the manifest as WS-19's evidence.** The approved
boundary states `plots.py` is **presentation only and computes no reported quantity**;
WS-19/FR-P1-05-11 require the prediction, residual, target-support and quality plots to
exist, **each carrying its source-data IDs**, with a plot manifest listing every required
plot. Unstated: how presentation-only is enforced rather than asserted, what a manifest
entry holds, and where the figure's units label comes from.

A) `plots.py` accepts DataFrames and computes whatever summaries a figure needs at render time
   > **Impact**: "Computes no reported quantity" becomes a comment, not a property — a figure could smuggle a number no producing path owns, unstamped and unverifiable, which is the §14 only-copy failure wearing a figure's clothing.

B) `plots.py` renders **exclusively from serialized, stamped artifacts** emitted by producing paths (the metrics artifact, Question 5's breakdown artifacts, the budget, `BootstrapResult`): its API takes artifact objects, not raw predictions, so presentation-only holds by signature; every figure is written with a manifest entry carrying the plot ID, the source artifact IDs and stamps it rendered, and its axis-units label **taken from the artifact's units metadata** rather than hardcoded; the manifest is WS-19's evidence
   > **Impact**: WS-19's criterion ("each carrying its source-data IDs") is the manifest's schema rather than a caption convention, and a TECU axis label can never disagree with the data behind it. Costs the artifact-object API shape.

C) B, plus the controls and the labelled diagnostics: a manifest entry missing source IDs **fails**; a figure whose units label disagrees with its artifact metadata **fails**; the manifest is asserted complete against the configured required-plot list (a missing required plot refuses, mirroring Question 5's inventory shape); and the RF-importance and Dst-diagnostic figures render only from their labelled artifacts, printing the **non-authoritative** / **diagnostic, hindcast-only** labels those artifacts carry (Question 8's surfaces)
   > **Impact**: WS-19 gets a falsifier instead of an existence glance, and the two figures with mandatory caveats can never render without them because the caveat arrives on the input. Costs three fixture cases.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. The artifact-only API is the cheapest possible enforcement of a sentence the boundary already commits to, and the manifest-as-schema reading is the only one under which WS-19's evidence column can be produced mechanically; C's controls cost three fixtures and buy the unit's one primary WS row.

[Answer]: C

---

## Question 8

**The diagnostics quarantine: Dst hindcast work and the RF-importance figure.** Dst is
diagnostic/hindcast-only, never a confirmatory ML feature (TC-11); grades are never mixed
within one series and the 2022 grade is recorded before use (D-10.1); `external-products`
R-62 makes provisional-grade ineligibility **assertable at the point of use**. RF
importance never adds, removes or ranks a feature into the production set —
`models-and-baselines` R-100 holds the production-path control and saves the score as a
**non-authoritative diagnostic artifact**; the figure rendered from it is this unit's
surface. Unstated: where Dst diagnostics live, what they may consume and emit, and how
the labels reach the figures.

A) Dst diagnostics and the RF figure are notebook material, computed where displayed
   > **Impact**: The only copy of a diagnostic computation would live in a notebook against §14, and the two mandatory caveats — non-authoritative, hindcast-only — would be captions someone remembers rather than fields something asserts.

B) Dst hindcast diagnostics are producing functions in `diagnostics.py`: they consume the Dst series through `external-products`' surface **with its recorded release grade**, assert a single grade per series (mixed grade raises, D-10.1), align per the driver rule, and emit artifacts **labelled diagnostic/hindcast-only** that live only under diagnostic paths — never in the metrics artifact, the primary table, or any feature-bearing artifact; the RF-importance figure renders only from `models-and-baselines`' saved diagnostic artifact, the **non-authoritative** label emitted with it by the producing path (R-60's pattern, third use)
   > **Impact**: The diagnostic lane is structurally separate from the confirmatory lane, and both caveats travel on the artifacts, so Question 7's plots print them without a second copy existing anywhere. Costs the label fields.

C) B, plus the boundary statement and the controls: the Dst-never-a-feature negative control is **stated as `features-and-splits`'/WS-11's lane, not annexed** — this unit's narrower controls are: a mixed-grade Dst series **raises**; a diagnostic-labelled field found in any feature-bearing or metrics artifact **fails**; an RF-importance figure without the non-authoritative label **fails**; and a provisional-grade series reaching any surface R-62 bars **raises at the point of use**
   > **Impact**: Each hard rule this unit actually touches gets its caught-violation pair, and the one control that belongs to a sibling is named as theirs — the same by-lane split R-109 and R-100 both practised. Costs four fixture cases.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. The diagnostic lane exists precisely so forbidden things have a permitted place to live; B builds the lane with the caveats as freight, and C fences it with controls scoped to this unit's actual reach while leaving WS-11's control where the story map puts it.

[Answer]: C

---

## Question 9

**The four analysis notebooks: REQ-ENG-12's obligations as mechanics, and the migrated
coverage notebook's home.** Each of the four notebooks imports from `src/`, reads
versioned artifacts, and **begins with the dataset version, code commit, configuration IDs
and artifact IDs it expects**; none holds the only copy of any logic class; "Run all"
either succeeds from declared inputs or **stops with a clear missing-artifact or
Internet-access message** rather than proceeding on partial state. The acquisition
notebook is expressly excluded (REQ-ENG-13, `acquisition`'s lane). TA-16's evidence:
notebook header declarations plus the acquisition-notebook/script diff. Separately,
REQ-ENG-8 migrates the existing `madrigal_phase1_coverage_audit.ipynb` **into this unit**,
its frozen inline constants moving to config under the already-recorded D-number-first
obligation. Unstated: how the declarations are made checkable, how "Run all" stops, and
where the migrated content lands.

A) Each notebook maintains its own hand-written header markdown; conventions documented
   > **Impact**: Four hand-maintained headers drift independently, nothing makes "Run all" actually stop, and TA-16's evidence is a visual inspection — which the acceptance vocabulary expressly calls insufficient.

B) A shared first-cell pattern: each notebook's first executed cell calls one `src/` helper — declare the expected dataset version, code commit, config IDs and artifact IDs; the helper verifies each against the workspace and **stops with the stated missing-artifact message before any later cell runs**, giving "Run all" its required semantics by construction; all four notebooks call `src/` functions only; and the migrated coverage-audit content is proposed to land in `01_data_and_target_audit` — the §12 tree fixes five notebooks and names no sixth — with the proposal routed to the gate rather than assumed
   > **Impact**: The four declarations become one checkable call instead of four conventions, and the migration question — the only place a sixth notebook could silently appear — is put to the owner. Costs one helper in this unit's `src/` surface.

C) B, plus TA-16's evidence mechanics: the deliberately-missing-declared-input negative control (Run all stops with the stated message, asserted per notebook); grep-style evidence that no logic class is present only in a notebook (the no-only-copy check, machine-producible); and the header-declaration block emitted in a fixed machine-readable form so TA-16's evidence column is a parse, not a screenshot
   > **Impact**: REQ-ENG-12's criterion — all three clauses — gets a falsifier, and the unit's TA-16 primary row is producible mechanically. Costs one fixture per notebook and a fixed header format.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. The declaration helper is the only design under which "begins with the declarations" and "Run all stops" are the same mechanism rather than two hopes, and the migration-target proposal belongs at the gate because a wrong assumption there creates a sixth notebook §12 does not name.

[Answer]: C

---

## Question 10

**Test scope: none of §12's seventeen modules is this unit's — where do its controls
live?** Derived by scanning §12's `tests/` list: no module for regimes, diagnostics,
plots, notebooks or claims exists in the mandated seventeen. This unit carries 7 untested
requirements of 11, plus the named negative controls Questions 1–9 accumulate, and the
affirmed methodology requires every hard rule to have a test proving the violation is
caught. Precedent exists for a project-authored module outside §12's seventeen:
`tests/test_acquisition_window.py` is in the workspace today and appears in no §12 row.

A) Rely on the three primary acceptance rows' evidence (WS-19's figure set, TA-16's headers and diff, TA-20's table) and design-time review for everything else
   > **Impact**: The 7 untested requirements stay untested, the negative controls of Questions 1–9 have no home, and this unit — whose whole job is honesty mechanics — would be the least-tested unit in the pipeline by its own choice.

B) One project-authored module is proposed: `tests/test_regimes_and_reporting.py` (the `test_<subject>.py` convention), hosting the named negative controls from Questions 1–9 — the boundary-value misclassification, the provisional-Dst raise and the window-span check (Q1); the descriptive-only guard and demotion-ordering controls (Q2); the missing-member, appendix-placement and `beats_model`-presence controls (Q3); the disclosure-presence and planted-claim controls (Q4); the strata/headline/fold-table/per-seed/stamp controls (Q5); the timestamp-ordering, units-refusal and exploratory-label controls (Q6); the manifest and units-label controls (Q7); the mixed-grade, quarantine and label controls (Q8); the notebook stop and no-only-copy controls (Q9) — following the `test_acquisition_window.py` precedent, an addition beside §12's set rather than an amendment to it
   > **Impact**: Every hard rule this unit carries gets its violation-is-caught pair in one named module, on synthetic fixtures. Costs the module's design now and its fixtures at 3.5 — no full-year data needed.

C) B, plus the acceptance-row routing: the module's machine-readable evidence is named as what the candidate Vision §15.2 rows would point at — FR-P1-05-20 and FR-P1-05-19 (both named candidates in `requirements.md`), FR-P1-05-16, FR-P1-05-18 and `TST-CLAIMS-01` — with the proposals routed to the gate, **proposed not applied**, and the remaining untested pair (FR-P1-05-14, FR-P1-05-15) covered by the module's controls even while rowless
   > **Impact**: The unit's 7-of-11 untested figure is addressed through the only two legitimate channels at once — designed falsifiers now, acceptance rows by owner amendment — with nothing minted by assertion. Costs one gate item.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A unit whose deliverable is defensible statements cannot itself be the untested one; B gives every control a home under an existing project precedent, and C connects that home to the acceptance vocabulary through the front door. The gate — and where required, the supervisor — rules on the rows; the module design stands either way.

[Answer]: C

---

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence: the siblings close at **R-122**
  (derived 2026-08-27 by grepping both `business-rules.md` heading sets:
  `evaluation-and-comparison` R-103…R-112, `statistical-inference` R-113…R-122, ten
  headings each), so this unit opens at **R-123**. The inherited R-83…R-89 gap remains
  observed, not explained.
- **[assumption]** Depth Q1 = B: `count_storm_events` is this unit's only approved
  cross-package boundary call; the hour-classifier, the breakdown/table/checklist
  producing functions, the plot API and the notebook declaration helper are intra-package
  shapes this stage specifies, names indicative, finalized in the three design artifacts
  after the gate.
- **[assumption]** Exception placement follows `foundation` R-01: **`RegimeError` is one
  of the fourteen**, declared **here** (`src/evaluation/regimes.py`, this unit's raise
  site) as an `IntegrityError` subclass, discharging R-01's OPEN cross-unit obligation for
  this unit; `FairnessError` and `LockedTestError` are imported for consumed
  preconditions, not redeclared; **no fifteenth exception is minted** — reporting refusals
  reuse `FairnessError` and `RegimeError` as placed, and every raise names the file or
  resource and the violated expectation.
- **[assumption]** `src/evaluation/` is a path grant owned by three units
  (`evaluation-and-comparison` R-112); this unit designs `regimes.py`, `diagnostics.py`
  and `plots.py` only and narrows nothing of TE §12.
- **[assumption]** The regime thresholds (quiet `Kp<4`, disturbed `Kp>=4`, storm `Kp>=5`),
  the −12 h/+24 h event window and D-13's three-event threshold arrive via
  `ConfigSnapshot` from `experiment.yaml` — frozen values encoded, not decided; the config
  key names are `foundation`'s surface, and this unit consumes whatever keys its schema
  fixes.
- **[assumption]** The pre-G-05 December coverage and regime-count audit is
  `inventory-and-registry`'s read under its own `open_restricted` purpose; this unit
  performs **no pre-G-05 December read of any kind** and consumes the audit's registered
  artifact only (Q2).
- **Verification obligations owned here:** the single-classifier copy with configured
  thresholds and the source/grade/provisional-Dst raises (Q1); the December-blind
  classification signature, the post-receipt breakdown gating, the descriptive-only storm
  guard and the demotion-ordering assertion (Q2); the primary-table rendering refusals,
  same-table construction, field-presence assertions, budget adjacency and TECU units
  check (Q3); the checklist artifact's presence checks and disclosure controls (Q4); the
  breakdown producing paths, D-17 strata bound, stamps and inventory refusal (Q5); the
  threshold-timestamp, budget-comparison, descriptive-only labelling, TECU refusal and
  exploratory-label assertions (Q6); the artifact-only plot API, manifest schema and units
  labels (Q7); the diagnostic quarantine, grade discipline and caveat labels (Q8); the
  notebook declaration helper, stop semantics and no-only-copy evidence (Q9);
  `tests/test_regimes_and_reporting.py`'s full negative-control set and evidence emission
  (Q10).
- **Governance dependencies owned outside this unit:** BLK-03's contract limbs
  (`models-and-baselines`, 3.1); BLK-04's contract limbs and BLK-09's `train_start`
  resolution (`features-and-splits`, 3.1); BLK-08's co-owner adoption of the R-103 joint
  contract — until adopted, no design path returns model output to TECU, and the primary
  table's numbers, the practical-relevance comparison and every TECU-denominated claim
  inherit that bound (Q3, Q6 make it checked rather than silent); the pre-G-05 audit's
  execution and registration (`inventory-and-registry`); FR-P1-05-18's missing source
  criterion (a `requirements.md` change, not this stage's produces list); the exploratory
  label's **writer** (the registry surface — `foundation`/`inventory-and-registry`; Q6
  routes it to the gate); the migrated coverage notebook's home (Q9, gate); the candidate
  Vision §15.2 acceptance rows (Q4, Q10 — owner/supervisor; proposed, never applied here);
  the D-number-first freeze of the notebook's inline constants (recorded team obligation,
  `acquisition`/`foundation` scaffold territory); G-05's freeze of the evaluation code
  this stage designs (Supervisor).
- **Open — all four inherited blockers are EXIT conditions on this stage.** BLK-03 ↓,
  BLK-04 ↓, BLK-08 ↓, BLK-09 ↓ remain open; nothing in this file closes any of them, this
  unit may not complete or exit 3.1 while any stands, and no implementation may proceed
  while they stand.
- **Open — the advisory NOT-READY carried from 2.3 lands here and stays open.**
  FR-P1-05-18's criterion still does not test the count's source; Q1's design makes the
  source assertable, and writing the criterion remains a `requirements.md` change outside
  this stage.
- **G-09 is not signed.** No answer here authorises creating `src/evaluation/regimes.py`,
  `diagnostics.py`, `plots.py`, any notebook, or `tests/test_regimes_and_reporting.py`;
  TE §18.3's stop-and-report rule binds every affected component while any P0 decision is
  unresolved.
- **None** of the above decides a scientific value. The regime thresholds, event window,
  D-13 count, D-8 boundary and disclosure sentences are already frozen and merely encoded;
  everything underdetermined — the migration target (Q9), the acceptance-row proposals
  (Q4, Q10), the exploratory-label writer (Q6) — is expressly routed to the gate.

---

## Consolidated Summary Confirmation

Questions 1–10 are answered above: **Q1 = C, Q2 = C, Q3 = C, Q4 = C, Q5 = C, Q6 = C,
Q7 = C, Q8 = C, Q9 = C, Q10 = C**. This is the pre-generation summary stop: before the
three design artifacts are generated, this section states the whole of what those answers
commit to, and nothing else is generated from them.

### What will be generated

Three artifacts, in this directory:

- **`business-logic-model.md`** — the workflows: the **single regime classifier** in
  `src/evaluation/regimes.py` — hour classification reading the three thresholds and the
  −12 h/+24 h window from `experiment.yaml` via `ConfigSnapshot`, `count_storm_events`
  the **only** counting path, every consumer (this unit's split and
  `inventory-and-registry`'s pre-G-05 audit alike) calling it and never reclassifying,
  with the boundary-value, window-span, source/grade and provisional-Dst controls —
  `.dst_summary.json` named as the closed path (Q1); the **December/ML-02 guard pair** —
  December-blind classification by signature (Kp and configured thresholds only) and
  post-receipt breakdown gating (the breakdown functions take
  `evaluation-and-comparison`'s emitted metrics artifact, which cannot exist before
  R-109's receipt), plus the descriptive-only storm guard reading the **registered**
  pre-G-05 audit count rather than recomputing it, and the demotion-timestamp-precedes-
  the-freeze assertion (Q2); the **primary-table producing path** in `diagnostics.py` —
  refuses to render on any missing declared member, same-table by construction, R-108's
  orientation/weighting/sign-convention fields asserted present and printed never
  restated, the budget placed adjacent (TA-19), the `beats_model` flag printed per row
  and enrolled in the disclosure check, units asserted TECU from artifact metadata (Q3);
  the **claims-and-limitations checklist** producing path — one row per prohibited class
  citing § Out of scope C by reference, one row per mandated disclosure as a presence
  check at its named locations, the human residue recorded as such (Q4); the **breakdown
  producing functions** — the FR-P1-05-16 enumeration as stamped machine-readable
  artifacts, the D-17 strata bound by signature (three field names, an enumerated set),
  headline/supplementary as a carried label, per-seed values with mean **and** spread,
  the top-1% sensitivity labelled beside its parent, the inventory refusal (Q5); the
  **practical-relevance/post-access pair** — threshold timestamp precedes the G-06
  receipt, reference-versus-budget comparison emitting the descriptive-only label from
  the only producing path, refusal when either input's units metadata is not TECU, and
  the reporting-side exploratory-label assertion on post-access runs (Q6); the **plots
  manifest** — `plots.py` rendering exclusively from serialized stamped artifacts,
  presentation-only by signature, the manifest as WS-19's evidence with per-entry source
  IDs and units labels taken from artifact metadata, completeness asserted against the
  configured plot list (Q7); the **Dst/RF diagnostics quarantine** — Dst consumed through
  `external-products`' surface with its recorded grade, mixed grade raising, artifacts
  labelled diagnostic/hindcast-only and confined to diagnostic paths, the RF-importance
  figure rendering only from `models-and-baselines`' labelled non-authoritative artifact,
  WS-11's control stated as `features-and-splits`' lane (Q8); and the **notebook
  declaration helper** — one `src/` first-cell call declaring dataset version, code
  commit, config IDs and artifact IDs, verifying each and stopping with the stated
  message before any later cell, giving "Run all" its semantics by construction, with
  TA-16's header block emitted machine-readably (Q9).
- **`business-rules.md`** — rules opening at **R-123**, continuing the single sequence:
  the siblings end at **R-122**, re-verified 2026-08-27 by grepping the
  `business-rules.md` heading sets (`evaluation-and-comparison` R-103…R-112 and
  `statistical-inference` R-113…R-122, ten headings each; `models-and-baselines` tops at
  R-102); the R-83…R-89 gap is inherited as observed, not explained.
- **`domain-entities.md`** — the intra-package artifact shapes Depth Q1 = B assigns to
  this stage: the **primary-table artifact** (declared members, controls-in-table by
  construction, printed R-108 fields, `beats_model` per row, TECU units metadata, budget
  adjacency); the **checklist artifact** (one row per prohibited class and per mandated
  disclosure, each recording where the text was found or failing); the **breakdown
  artifacts** (three stamps `phase_id`/`source_id`/`target_definition_id`,
  headline/supplementary label, per-seed fields, machine-readable completeness
  shortfalls per the two-tier posture); the **plot-manifest entry** (plot ID, source
  artifact IDs and stamps, units label); and **`RegimeError`**, declared in
  `src/evaluation/regimes.py` as an `IntegrityError` subclass — one of the fourteen,
  discharging foundation R-01's OPEN cross-unit obligation for this unit; no fifteenth
  exception is minted.

The one test module scoped here is **`tests/test_regimes_and_reporting.py`** (Q10 = C):
a project-authored addition beside §12's seventeen on the `test_acquisition_window.py`
precedent, hosting every named negative control from Questions 1–9 on synthetic
fixtures, its machine-readable evidence named as what the candidate acceptance rows
would point at. Its design is specified; **no module is created** — G-09 is not signed.

### Each answer, one line

| Q | Answer | Design consequence |
|---|---|---|
| 1 | C | One classifier copy in `regimes.py`, thresholds and window read from `experiment.yaml` via `ConfigSnapshot`; `count_storm_events` the only counting path; boundary-misclassification, window-span, non-GFZ/absent-grade and provisional-Dst controls, `.dst_summary.json` named; `RegimeError` declared here as an `IntegrityError` subclass |
| 2 | C | December-blind by signature and post-receipt by construction; the storm guard reads the registered pre-G-05 audit count (never recomputed here), December regime results descriptive-only below three independent events; the H4/SRQ-5 demotion timestamp must precede the G-05 freeze, a post-freeze demotion failing rather than being corrected |
| 3 | C | The primary table is a producing path consuming R-110's checked fields: missing-member refusal, same-table by construction, R-108 fields asserted present and printed, budget adjacent (TA-19), `beats_model` printed and enrolled in the disclosure check, units asserted TECU — BLK-08's bound made checked, not silent |
| 4 | C | The checklist is a machine-readable artifact: presence checks at named locations for all five disclosure obligations, prohibited classes cited from § Out of scope C; negative controls for the missing conclusion mention, missing caption sentence and planted claim; the acceptance-row gap routed as Vision §15.2 proposals, proposed not applied |
| 5 | C | Every FR-P1-05-16 breakdown is a producing function emitting a stamped artifact; D-17's three fields the only representable strata; headline label structural; per-seed with mean and spread; a missing declared breakdown refuses the results artifact; six negative controls |
| 6 | C | Threshold-timestamp-precedes-G-06 and reference-versus-budget become mechanical, the descriptive-only label emitted by the only producing path, non-TECU inputs refused; post-access runs asserted to carry the exploratory label at reporting, the label's **writer** routed to the gate |
| 7 | C | `plots.py` takes artifact objects only — presentation-only by signature; the manifest is WS-19's evidence, entries carrying source IDs and metadata-derived units labels, completeness asserted against the configured plot list; RF and Dst figures print the caveats their input artifacts carry |
| 8 | C | The diagnostic lane is structurally separate: Dst with recorded grade, mixed grade raises, hindcast-only labels travel on the artifacts, provisional grade raises at the point of use (R-62); the RF figure renders only from the labelled non-authoritative artifact; WS-11's Dst-never-a-feature control stated as `features-and-splits`' lane |
| 9 | C | One shared first-cell helper makes the four declarations checkable and gives "Run all" its stop semantics by construction; the migrated coverage content is proposed to land in `01_data_and_target_audit` (no sixth notebook), routed to the gate; TA-16's evidence is a parse, not a screenshot |
| 10 | C | `tests/test_regimes_and_reporting.py` proposed on the `test_acquisition_window.py` precedent, hosting Q1–Q9's negative controls; its evidence named as what the candidate Vision §15.2 rows would point at, the proposals routed to the gate; FR-P1-05-14/15 covered by controls even while rowless |

### Gate items

Routed, not decided:

- **The regime configuration** — quiet `Kp<4`, disturbed `Kp>=4`, storm `Kp>=5`, the
  −12 h/+24 h window and D-13's three-event threshold are **frozen values this unit only
  encodes**, arriving via `ConfigSnapshot` from `experiment.yaml`; the config key names
  are `foundation`'s surface, and the gate confirms the config content under the
  four-config regime.
- **The exploratory-label writer (Q6)** — this unit asserts the label at its reporting
  surface; which surface *writes* it is the registry writer's design
  (`foundation`/`inventory-and-registry`), put to the gate rather than annexed.
- **The migrated coverage notebook's home (Q9)** — proposed to land in
  `01_data_and_target_audit`, because §12's tree fixes five notebooks and names no
  sixth; the D-number-first freeze of its inline constants remains the recorded team
  obligation and is not performed here.
- **The Vision §15.2 acceptance-row proposals (Q4, Q10)** — candidate rows for
  FR-P1-05-20, FR-P1-05-19, FR-P1-05-16, FR-P1-05-18 and `TST-CLAIMS-01`, each naming
  the checklist or test-module evidence it would point at; **proposed, never applied
  here** — the owner and, where required, the supervisor rule on the rows. FR-P1-05-14
  and FR-P1-05-15 remain rowless and are covered by the module's controls meanwhile.

### The blockers and standing authority

- **BLK-03 ↓, BLK-04 ↓, BLK-08 ↓, BLK-09 ↓ (all inherited)** — exit conditions on stage
  3.1, **not closed by anything in this file**; this unit may not complete or exit 3.1
  while any contract is unapproved, and no implementation may proceed while they stand.
  **BLK-08 ↓ reaches the claims directly**: the practical-relevance comparison and the
  primary table's numbers are TECU-denominated only if the co-owner adopts its half of
  the R-103 joint contract — Q3's and Q6's units assertions make that dependence checked
  rather than silent. **BLK-09 ↓** bounds the fit every reported number rests on.
- **The FR-P1-05-18 advisory NOT-READY on `requirements.md` stays open** — its criterion
  still does not test the count's source; Q1's design makes the source assertable, and
  writing the criterion is a `requirements.md` source-criterion change **reported here,
  not fixed here**.
- **G-09 is not signed.** `tests/` holds three modules, none this unit's; `src/` and
  `configs/` are absent. The artifacts specify design only; no answer authorises
  creating `regimes.py`, `diagnostics.py`, `plots.py`, any notebook, or
  `tests/test_regimes_and_reporting.py`.
- **D-11's provisional-Dst bar** — provisional Dst characterised fixture selection only
  and never becomes a modelling input, a frozen tolerance, or a G-05 regime count; Q1's
  control is its executable form, `.dst_summary.json` the named path it closes.
- **The pre-G-05 December coverage and regime audit is `inventory-and-registry`'s read**
  under its own `open_restricted` purpose; this unit performs no pre-G-05 December read
  of any kind and consumes the audit's registered artifact only.

### The figures, derived not carried

- **3 `src/` modules + 4 notebooks + 1 checklist artifact** — counted from § 11's `Owns`
  list: `regimes.py`, `diagnostics.py`, `plots.py`; `01_data_and_target_audit`,
  `02_processor_verification`, `03_features_and_splits_review`,
  `04_results_and_figures`; the claims-and-limitations checklist. No stage script: this
  unit runs inside `scripts/07_evaluate_and_report.py`, which
  `evaluation-and-comparison` owns.
- **11 requirements, 7 untested** — read from the story map's rows, the two upstream
  artifacts agreeing: 4 with rows (REQ-ENG-12/TA-16, FR-P1-05-9/TA-20,
  FR-P1-05-10/TA-19, FR-P1-05-11/WS-19) + 7 without (FR-P1-05-14, FR-P1-05-15,
  FR-P1-05-16, FR-P1-05-18, FR-P1-05-19, FR-P1-05-20, REQ-CLAIM-01) = 11.
- **Acceptance rows** — **WS-19, TA-16, TA-20 primary (3 rows)**, supporting **TA-19**
  (`target-standardization` produces the budget; this unit reports it adjacent to the
  primary result).
- **Amendments owed — derived against the current chain, printed before asserted:
  5 + 0 + 1 + 1 + 0 = 7 across 5 units.** `external-products` R-55 basis **5 across 3**
  + `features-and-splits` **0** + `evaluation-and-comparison` **1** (the BLK-08 package,
  R-103) + `statistical-inference` **1** (the R-118 signature amendment) — re-verified
  2026-08-27 by reading `statistical-inference`'s `business-rules.md` § Amendments owed,
  which prints exactly the 5 + 0 + 1 + 1 = 7-across-5 derivation — **plus this unit's
  0**. This unit adds no amendment: `count_storm_events(kp, *, release_grade, source)`
  is consumed exactly as approved with no signature change, and the Q4/Q10
  acceptance-row proposals are Vision §15.2 amendments owned by the owner/supervisor —
  not boundary-contract amendments to `component-methods.md`, the only class this
  ledger tracks. The total therefore **stands at 7 across 5 units**.

### What is NOT decided here

- **No scientific value.** The regime thresholds, event window, D-13 count, D-8
  boundary and disclosure sentences are already frozen and merely encoded; the
  migration target (Q9), the acceptance-row proposals (Q4, Q10) and the
  exploratory-label writer (Q6) are proposed and routed to the gate.
- **No module creation.** G-09 is not signed; the artifacts specify design only.
- **No blocker closes.** All four inherited exit conditions stand exactly as the
  register rules them, and the FR-P1-05-18 advisory NOT-READY stays open as a
  `requirements.md` change outside this stage.

### Assumptions and open questions, summarized

- **Assumptions carried into the artifacts**: rule numbering opens at R-123 with the
  R-83…R-89 gap inherited as observed; `count_storm_events` is the only approved
  cross-package boundary call, everything else an intra-package shape this stage
  specifies (Depth Q1 = B), finalized in the three artifacts after the gate;
  `RegimeError` is one of the fourteen project exceptions, declared here as an
  `IntegrityError` subclass, with `FairnessError` and `LockedTestError` imported, not
  redeclared, and no fifteenth minted; `src/evaluation/` is a path grant owned by three
  units and this unit designs its three modules only, narrowing nothing of TE §12; the
  regime constants arrive via `ConfigSnapshot` from `experiment.yaml`, the key names
  being `foundation`'s surface.
- **Verification obligations owned here**: the single-classifier copy with configured
  thresholds and the source/grade/provisional-Dst raises (Q1); the December-blind
  signature, post-receipt gating, descriptive-only storm guard and demotion-ordering
  assertion (Q2); the primary-table refusals, same-table construction, field-presence
  assertions, budget adjacency and TECU check (Q3); the checklist's presence checks and
  disclosure controls (Q4); the breakdown producing paths, D-17 bound, stamps and
  inventory refusal (Q5); the threshold-timestamp, budget-comparison, descriptive-only
  labelling, TECU refusal and exploratory-label assertions (Q6); the artifact-only plot
  API, manifest schema and units labels (Q7); the diagnostic quarantine, grade
  discipline and caveat labels (Q8); the notebook declaration helper, stop semantics
  and no-only-copy evidence (Q9); `tests/test_regimes_and_reporting.py`'s full
  negative-control set and evidence emission (Q10).
- **Governance dependencies owned outside**: BLK-03's limbs (`models-and-baselines`);
  BLK-04's limbs and BLK-09's `train_start` resolution (`features-and-splits`);
  BLK-08's co-owner adoption of the R-103 joint contract; the pre-G-05 audit's
  execution and registration (`inventory-and-registry`); FR-P1-05-18's missing source
  criterion (a `requirements.md` change); the exploratory label's writer (registry
  surface, Q6 → gate); the migrated notebook's home (Q9 → gate); the candidate Vision
  §15.2 rows (Q4, Q10 → owner/supervisor, proposed never applied); the D-number-first
  freeze of the notebook's inline constants (`acquisition`/`foundation` scaffold
  territory); G-05's freeze of the evaluation code this stage designs (Supervisor).

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The receipt is recorded, the three design artifacts are generated on these answers, and the adversarial review follows.

- Request changes
   > **Impact**: Nothing is recorded or generated; state what to change and the summary is re-presented.

> **💡 Recommendation**: **Looks correct** — every figure above is derived from this file's own sources rather than carried (the R-123 opening and the 7-across-5 amendment total were both re-derived against the siblings' artifacts today, and this unit adds zero to the amendment ledger), every scientific value is already frozen and merely encoded, everything underdetermined is routed to the gate as a proposal, and all four blockers plus the FR-P1-05-18 advisory stay open exactly as the register rules them.

[Answer]: Looks correct
