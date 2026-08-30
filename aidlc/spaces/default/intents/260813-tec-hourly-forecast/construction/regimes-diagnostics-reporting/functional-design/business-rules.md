# Business Rules — `regimes-diagnostics-reporting`

> ## ✳ G-09 IS SIGNED — 2026-08-28, **D-31** (read this before any G-09 statement below)
>
> The project decision owner **signed and approved G-09 (Agent preflight)** on 2026-08-28,
> recorded as **D-31** in `evidence/DECISIONS.md` with change record
> `governance/CHANGE_RECORD_2026-08-28_G09_signed.md`. **Every statement below of the form
> "G-09 is not signed" / "G-09 stays unsigned" is superseded as to the gate's status**, and
> is left standing as the accurate record of the constraint that applied when it was
> written.
>
> ⚠ **D-31 records the gate's own TE §18.3 preconditions as UNMET, and that disclosure
> travels with the signature.** `configs/`, and until 2026-08-28 `src/`, did not exist, so
> the mandated automated zero-TBD preflight **could not run**; the ten named critical tests
> **cannot be executed in this environment** (no Python interpreter is installed — a
> zero-byte Windows Store stub, no registry entry, no interpreter on disk); and the evidence
> artifact `aws_ai_dlc_preflight_report` **does not exist**. "No failing critical test" is
> therefore **unproven, not proven** — an absence of executions, not an absence of failures.
> This is the owner **opening the gate by authority**, not a record that its evidentiary
> conditions were satisfied, and no reader may infer the second from the first.
>
> **What the signature changes here:** module creation is authorised, and any defect this
> unit deferred *solely* because G-09 barred editing a file is now correctable.
> **What it does NOT change:** G-05 and G-06 remain `Blocked`; G-P1A, G-P2, G-P3A, G-P3C
> and G-07 are unaffected; **TE §18.2's absolute rule stands** — every scientific value this
> unit routed to G-04/G-05 **stays routed**, and no agent may fill a freeze-gate value by
> convenience; and **§18.3's stop-and-report obligation survives its own gate**, being a
> standing rule on implementation rather than a one-time gate condition.

**Unit** `regimes-diagnostics-reporting` · **Kind** `library` · **Complexity** L ·
**Deployment** embedded · **Depends on** `statistical-inference`

The prohibitions this unit enforces, each with what it rejects, what it raises or fails,
and the negative control that proves the rejection happens.

**This project's affirmed methodology is a negative control paired with every hard rule** —
a test that proves the violation is *caught*, not only that the happy path works.

**Every rule here guards the step from a computed number to a defensible statement.** A
violation does not crash a pipeline; it prints a plausible table with a missing control, a
regime count from a prohibited source, a claim outside the frozen boundary, or a silence
where a mandated disclosure belongs — failures a reader cannot detect from the artifact
alone, which is why each one is made structural or loud here.

**Rule IDs continue the single sequence.** `foundation` R-01…R-17, `governance-guards`
R-18…R-29, `acquisition` R-30…R-43, `inventory-and-registry` R-44…R-53, `external-products`
R-54…R-63 (plus R-54a), `target-standardization` R-64…R-73, `features-and-splits` R-74…R-82
(plus R-76a), `models-and-baselines` R-90…R-102, `evaluation-and-comparison` R-103…R-112,
`statistical-inference` R-113…R-122 — so this unit opens at **R-123**. The two siblings'
closing IDs were **re-derived 2026-08-27 by grepping their `business-rules.md` headings
(R-103…R-112 and R-113…R-122, ten headings each)**, not carried. **The R-83…R-89 gap
between `features-and-splits` and `models-and-baselines` is inherited as observed, not
explained**: if it was a reservation, or per-unit numbering was intended, say so at the
gate and these artifacts renumber.

**Four inherited exit conditions stand on this stage: BLK-03 ↓, BLK-04 ↓, BLK-08 ↓,
BLK-09 ↓.** None is owned here; none closes here. **BLK-08 ↓ reaches the claims
directly** — the practical-relevance comparison is stated in TECU and the primary table's
numbers are TECU-denominated only if the co-owner adopts its half of the R-103 joint
contract; R-125's and R-128's units assertions make that dependence checked rather than
silent. **BLK-09 ↓** bounds the fit every reported number rests on. This unit **may
enter** 3.1, **may not complete or exit** it while any contract is unapproved, and **no
implementation may proceed while they stand** (`GOV-2026-08-22-REM-01` Rec 2, extended to
BLK-08/BLK-09 on 2026-08-23). **G-09 is not signed** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.: no module named here may be created.

> **Remediation, 2026-08-28 — `GOV-2026-08-28-FD-01` (verdict FAIL), owner-ruled items.**
> Seven changes, each dated at its site and citing its Recommendation number:
> **Rec 16** — R-125 gains limb 7's provenance block (`mask_id`, `feature_set_id`,
> per-station surviving row counts, exclusion counts, the D-28 scored-window statement),
> printed from the producing objects and carried onto every breakdown, with R-126 gaining a
> D-28 `disclosure` row; **Rec 20** — R-127's configured list gains RMSE per member, the
> `derived: true`-labelled percentage reduction and §5.5's six supporting metrics, and
> R-128 gains the measured improvement so Vision §5.3's **first** conjunct can be evaluated
> at all; **Rec 21** — the conclusion / limitations / abstract-level surfaces become a
> named, registered, hash-listed artifact (`domain-entities.md` § 6) and R-126's text rows
> **fail closed** without it; **Rec 17** — TC-12's interpretive half becomes both a
> `prohibited_class` row (R-126) and a caveat emitted from the per-station producing path
> (R-127); **Rec 27** — §12's module count is corrected from "seventeen" to the derived
> **21**, the derivation printed at R-132, and the `test_acquisition_window.py` precedent
> sentence corrected (that module is **inside** §12 by amendment, which changes the
> conclusion); **Rec 43** — VAL-05 gains the named falsifier its two neighbours already
> had; **Rec 15** — R-124 **asserts** its December day range instead of inheriting it and
> excludes wholly-outside events from D-13's threshold, with the range's **value** routed to
> the gate as a Student + Supervisor item. **Rec 6's D-28** and **Rec 19's third comparison
> set** are carried as owner rulings. Negative controls: **31 → 40**, re-derived and
> printed. Entities: **5 → 6**. **BLK-03 ↓, BLK-04 ↓, BLK-08 ↓, BLK-09 ↓ stay open; G-09
> stays unsigned; no scientific value is decided.** The two `## Review` sections in
> `business-logic-model.md` are the 2026-08-27 historical record and are preserved
> byte-for-byte; the counts they verified (30/31 controls, 5 entities) were correct then.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 11 — the `Owns` list (3 modules + 4 notebooks + 1 checklist artifact), the boundary, the 11 requirements (7 bolded untested), acceptance rows WS-19/TA-16/TA-20, the six implementation notes, the four inherited blockers with the exit-condition ruling.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Table 1's rows for the 11 requirements (7 marked **NO CURRENT ACCEPTANCE ROW**); Table 2's WS-19/TA-16/TA-19/TA-20 rows; § Per-unit coverage summary (11 / 7 / WS-19, TA-16, TA-20 / TA-19); § Cross-unit responsibilities; the open-issues row on FR-P1-05-18's missing source criterion.
- `../../../inception/requirements-analysis/requirements.md` — the eleven requirement rows this file's § Requirement coverage enumerates, including FR-P1-05-18's four clauses and its advisory NOT-READY, FR-P1-05-16's enumerated breakdowns and D-17 strata bound, REQ-CLAIM-01's § Out of scope C citation rule, and FR-P1-05-19/FR-P1-05-20's named-candidate status.
- `../../../inception/application-design/component-methods.md` — the approved `count_storm_events(kp, *, release_grade, source)` boundary call and `RegimeError` raise contract (quoted in `business-logic-model.md` W-1); § Depth (Q1 = B); § Assumptions (the fourteen exceptions declared where raised until 3.1 places them; no signature encodes a scientific constant).
- `../evaluation-and-comparison/functional-design/business-rules.md` — R-108 (the estimand's machine-readable orientation/weighting/sign-convention fields), R-109 (the two-events boundary; DEC post-receipt), R-110 (completeness refusal upstream, `beats_model` per benchmark, the spatial-representativeness sentence emitted by the producing path, the co-reporting obligation stated as this unit's), R-112 (the `src/evaluation/` path grant); § Amendments owed (the 5 + 0 + 1 = 6-across-4 derivation the chain extends).
- `../statistical-inference/functional-design/business-rules.md` — R-113…R-122 (grepped, ten headings), R-120 (comparator quarantine), R-121 (correlation field presence asserted downstream, restated nowhere); § Amendments owed (**5 + 0 + 1 + 1 = 7 across 5 units**, the basis this unit extends with zero).
- `../features-and-splits/functional-design/` — **FU-7 = A** (2–31 December, 30 days); WS-11's Dst-never-a-feature control is its lane.
- `../inventory-and-registry/functional-design/business-rules.md` — the D-13 assumption row: the December regime-count threshold is D-13's, counted from GFZ Kp/Hp60 at a recorded release grade, D-11 barring any provisional-Dst-derived figure; the pre-G-05 audit is its read.
- `../external-products/functional-design/business-rules.md` — R-62 (grade discipline; provisional-grade ineligibility asserted at the point of use), R-60 (emit-from-the-producing-path).
- `../models-and-baselines/functional-design/business-rules.md` — R-100 (RF importance diagnostic-only; `authoritative = false` in the artifact's own metadata; the production-path control lives there).
- `../foundation/functional-design/business-rules.md` — R-01 (the fourteen-exception `IntegrityError` hierarchy; **`RegimeError` named among the eight raised by other units**, verified 2026-08-27), R-10, R-15, R-17, § Stage entry contract.
- `aidlc/spaces/default/memory/project.md` § Mandated/Forbidden and `team.md` — TC-11, D-10.1, ML-02, Vision §8.3/R-13, PC-03/PC-04, TEC-06, VAL-05, D-8/TC-17, D-7, **TC-12** (`binding: hard`; cited 2026-08-28 per `GOV-2026-08-28-FD-01` Rec 17 — the data-shape half is `external-products` R-63's, the interpretive half *"a station performance difference must never be attributed to local forcing the dataset does not contain"* reaches R-126 and R-127 here), PC-09, the RF rule, TEC-05's stamps, §14/§7, TC-03e, the two-tier error posture, the negative-control methodology, TE §18.3.
- `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §14, §13.5, §12 (the `tests/` tree — **21** `test_*.py` modules as amended, derived and printed in R-132; §12's mandated set as amended, see `requirements.md` REQ-ENG-4 for the current count — none of the 21 is this unit's), **§15.4** (the required-output tree; every output hash-listed in `artifact_manifest.json` — the home of `domain-entities.md` § 6), §9.3 via Vision. *(Corrected 2026-08-28 per Rec 27: this line previously read "seventeen test modules … derived by scanning the list"; the derived figure is 21.)*
- `PreFlight/vision_document(3)(2)(2).md` — **§8.9** (*"exclusions and row counts are reported"*; *"the comparison records a stable mask ID and feature-set ID"* — R-125 limb 7); **§5.5** (RMSE as the primary reported error metric; the derived relative summary `1 - RMSE_model/RMSE_reference`; the six supporting metrics); **§9.5** required result 2 (*"Derived percentage RMSE reduction, clearly labeled as derived"*); **§5.3** (the practical-relevance layer's two conjuncts) and **§5.4** (the ten-percent RMSE-reduction reference magnitude) — R-127 and R-128; **§2.4** (the binding honesty rule; tier 3's learned-model comparison).
- `evidence/DECISIONS.md` **D-28** (2026-08-28) — the G-06 locked-test scored set is **2–31 December 2022, 30 days**, first 24 h excluded and counted, with its stated consequence that the scored set *"must be disclosed as 30 days"* on the primary table, the breakdown artifacts and the claims-and-limitations checklist; the disclosed Vision §8.2 / TE §7.1 authority conflict, carried to G-05 unresolved; the owed revised split manifest; **no supervisor signature exists or is claimed**. Also **D-13**, **D-11**, **D-17**, **D-7**, **D-8**.
- `governance/reviews/GOV-2026-08-28-FD-01.md` — Recommendations **16**, **17**, **18** (limb (3) — the `NFR-TDEF-01` and `FR-P1-03-4` checklist rows, added on the 2026-08-28 resume pass), **19** (the owner's third declared comparison set `{M-04, M-05, M-06}`), **20**, **21**, **27**, **43**, and **15**'s mechanism-plus-route-the-value half.
- Workspace inspection, 2026-08-27: `tests/` holds three modules, none this unit's; `src/` and `configs/` absent; `.dst_summary.json` at the repository root; `dst_provisional_202212.html` under `evidence/audit_ec1_2026-08-15/kyoto_dst/`.
- `functional-design-questions.md` (**Q1 through Q10**, all answered **C**; summary receipted), `business-logic-model.md`, `domain-entities.md`.

---

## R-123 — One regime classifier, configured thresholds, one counting path

**Rule (Q1 = C).** Exactly one hour-classification function, in
`src/evaluation/regimes.py`, labels hours quiet/disturbed/storm; it reads the three
thresholds (quiet `Kp<4`, disturbed `Kp>=4`, storm `Kp>=5`) and the −12 h/+24 h event
window from `experiment.yaml` via `ConfigSnapshot` — **encoding frozen values, deciding
nothing** (TC-03e; FR-P1-05-18 clause 3 satisfied by construction: no threshold literal in
source). **`count_storm_events` is the only counting path**, implementing D-13's event
definition (a contiguous `Kp>=5` interval) and independence rule (>=24 h of `Kp<4`);
`source` and `release_grade` are required arguments, and a `source` that is not GFZ
Kp/Hp60 or an absent grade **raises `RegimeError`** (the approved contract, consumed
as-is). Every consumer **in this unit** calls these and never reclassifies — every regime
label or storm-event count this unit's workflows and artifacts use comes from the one
classifier and the one counting path; no inline reclassification exists here.
`inventory-and-registry`'s pre-G-05 audit is **not** a consumer: it computes its count by
its own means in its own lane (`external-products` R-56's allowlist bars it from
`src/evaluation/`, and the unit DAG carries no edge from it to this unit), and this unit
**reads** its registered artifact (R-124), never expecting the audit to call this unit's
code. D-13 collapsed H4's fate and the general storm-claim guard onto **one measured
quantity** — the registered audit count — and R-124's audit-count consistency control
(31) is what preserves the collapse across the unit boundary: a divergence **raises**
rather than being silently resolved, and is adjudicated at the gate, not here.
*(Corrected 2026-08-27, iteration-1 Critical: the earlier text named the pre-G-05 audit
as a caller of this unit's classifier — a call R-56 bars and neither the audit's own
design nor the unit DAG carries.)* A **provisional-Dst-derived series** offered as the count's input
**raises `RegimeError`** (D-11; R-62 restriction 3) — `.dst_summary.json`, the VAL-11
custody item present in the workspace today, is named as exactly the path of least
resistance this control closes.

**`RegimeError` is declared here** as an `IntegrityError` subclass (`domain-entities.md`
§ 5), discharging `foundation` R-01's OPEN cross-unit obligation for this unit.

**The advisory NOT-READY is reported, not fixed**: FR-P1-05-18's criterion still does not
test the count's source; this rule makes the source assertable, and writing the criterion
remains a `requirements.md` change outside this stage's produces list.

**Negative controls.** (1) An hour at the boundary values misclassified — a `Kp>=4` hour
labelled quiet, or a `Kp>=5` hour not labelled storm — → **fails** on a synthetic Kp
fixture. (2) An event window of any span other than −12 h/+24 h → **fails** (clause 4).
(3) A non-GFZ `source` or an absent `release_grade` → **`RegimeError`**. (4) A
provisional-Dst-derived series offered as the count's input → **`RegimeError`**, the
`.dst_summary.json` path named in the fixture.

**Control that must *not* fire:** a GFZ Kp/Hp60 series with a recorded release grade →
the count is computed and returned with its event intervals.

**Acceptance.** ⚠ No row — FR-P1-05-18 is `UNTESTED`; a candidate Vision §15.2 row is
proposed at the gate (R-126, R-132), pointing at `tests/test_regimes_and_reporting.py`'s
evidence.

## R-124 — December-blind by signature, post-receipt by construction, and the two guards

**Rule (Q2 = C).** The classifier consumes **only the Kp driver series and configured
thresholds** — never a December target or prediction value — so classification cannot see
December by signature. Every regime **performance** breakdown over a `DEC`-partition
result is computed **only from `evaluation-and-comparison`'s emitted metrics artifact**,
which cannot exist before R-109's verified hash receipt — the breakdown functions take
the artifact, not raw predictions, so the post-receipt property holds by construction and
this unit cannot become the pre-G-05 December performance channel ML-02 closes. Two
executable guards:

1. **The descriptive-only storm guard** (FR-P1-05-16): December regime results are
   labelled **descriptive-only unless** the **registered** pre-G-05 audit artifact
   records **>=3 independent storm events** — the count **read from the registered
   December regime-count audit report, never recomputed here as the guard's input**, so
   one measured quantity governs both the guard and H4's fate (the split R-109 stated,
   surviving into this unit's mechanics).
2. **The demotion-ordering assertion** (FR-P1-05-18 clause 2): the H4/SRQ-5 demotion
   record's timestamp is asserted to **precede the G-05 freeze**; a post-freeze demotion
   **fails rather than being corrected** (**`RegimeError`**, naming the record and the
   violated ordering).

**The audit-count consistency control** *(added 2026-08-27, iteration-1 Critical)*: no
shared call path exists between this unit's classifier and the pre-G-05 audit —
`inventory-and-registry` computes its count by its own means in its own lane
(`external-products` R-56's allowlist gives it no path into `src/evaluation/`) — so where
D-13's single-measured-quantity collapse matters, this unit checks **divergence** instead
of assuming a shared mechanism: when the DEC regime breakdown is produced (post-receipt
by construction), the breakdown path also runs `count_storm_events` over the same Kp
series and over the **asserted** December day range (see the window clause below) and
compares the result against the
registered count; a disagreement **raises `RegimeError`** — naming both counts, the audit
artifact and the violated D-13 single-measured-quantity expectation — rather than
silently preferring either. This unit does not adjudicate; the disagreement surfaces at
the gate.

**The count window: asserted, not inherited** *(added 2026-08-28 per
`GOV-2026-08-28-FD-01` Rec 15, owner ruling **mechanism written, value routed**)*. This
rule previously ran `count_storm_events` over *"the window the registered audit covers"*,
deferring the window entirely to `inventory-and-registry`'s audit, whose declared scope is
**month granularity only** — twelve 2022 months, all three cells, the named artifact
classes — with no day range. D-13 makes H4/SRQ-5's confirmatory status turn on December
containing **>=3 independent storm events**, and the scored set is now **30 days** (D-28),
so under the old wording a `Kp>=5` interval confined to **1 December** could promote H4 and
lift the descriptive-only label while contributing **zero** scored rows; the −12 h
pre-event window of an event beginning early on 2 December has the same shape in reverse.
Two mechanism changes, neither deciding a scientific value:

- **The range is asserted here.** The comparison count is taken over an **explicitly
  configured December day range** read from `experiment.yaml` via `ConfigSnapshot` and
  **asserted** at the call site, rather than inherited from the audit's month-granular
  scope. The design fixes *that a range is asserted*; it does not fix *which range*.
- **An event wholly outside the scored set is reported separately and does not count.**
  Any storm event falling **wholly outside** the scored set (2–31 December 2022 per D-28)
  is **reported separately** on the DEC regime rows and is **excluded from D-13's >=3
  threshold**; counting one toward the threshold **fails** (control (40)). This control is
  executable whichever day range is frozen, because it tests the exclusion rule and not the
  range value.

**Routed, not decided:** *which* December day range governs D-13's count is a **Student +
Supervisor** gate item — D-13 is a supervisor-countersigned demotion threshold, D-11 bars
any provisional-Dst figure from a G-05 regime count, and TE §18.3 forbids this stage
filling it by convenience. `inventory-and-registry` is being amended in parallel to fix the
audit's day range and to report any wholly-outside event separately; where the two units'
ranges disagree, control (31) already makes the divergence raise rather than resolve. **Scoping — no new ML-02 channel**: the check runs only inside the post-receipt
DEC breakdown path; pre-receipt, this unit reads only the audit's own already-registered
numbers and opens no December path of any kind. The registered count remains the storm
guard's sole governing input — the comparison count exists for divergence detection only,
never as a substitute.

The pre-G-05 audit's regime counts remain `inventory-and-registry`'s performance-blind
read, untouched (Vision §8.3; R-13); its execution and registration are owned there.

**Negative controls.** (5) A December regime breakdown missing the descriptive-only label
when the registered count is below three → **fails**. (6) A demotion record whose
timestamp postdates the G-05 freeze → **fails** (**`RegimeError`**). (31) A registered
pre-G-05 audit count and this unit's post-receipt comparison count over the same Kp
series and asserted day range that disagree → **raises** (**`RegimeError`**, naming both
counts and
the audit artifact). Control (31) is appended out of positional order (2026-08-27,
iteration-1 Critical) so controls (7)–(30) keep their existing numbers. **(40)** A storm
event falling **wholly outside the scored set** counted toward D-13's >=3 threshold →
**fails** (**`RegimeError`**, naming the event interval, the scored range and the violated
D-13 threshold) — appended 2026-08-28 per Rec 15, again out of positional order so
(1)–(39) keep their numbers.

**Controls that must *not* fire:** `inventory-and-registry`'s pre-G-05 coverage and
regime audit read — legitimate, earlier, performance-blind, someone else's; and a
post-receipt DEC breakdown with the registered count at three or more → renders
confirmatory regime rows without demotion.

**Acceptance.** ⚠ No row — FR-P1-05-16 and FR-P1-05-18 are `UNTESTED`; candidate rows
proposed at the gate.

## R-125 — The primary results table refuses, co-reports, prints, and checks its units

**Rule (Q3 = C).** The primary table is built by a **producing path in `diagnostics.py`**
from the emitted metrics artifact — never assembled in a notebook (§14). It:

1. **refuses to render** when any declared primary member's metric is absent, consuming
   R-110 limb 1's completeness refusal rather than re-checking membership
   (**`FairnessError`**, the imported class of the consumed precondition);
2. lands all three difficulty controls (M-01, M-02, M-03) and the IRI comparison in the
   **same table by construction** — appendix relegation unrepresentable (FR-P1-05-9;
   PC-03/PC-04; TA-20);
3. asserts R-108's orientation (`benchmark_minus_model`), weighting (`equal_station`) and
   sign-convention fields **present** and prints them **from the artifact, never
   restated**;
4. reads the target uncertainty budget artifact and places it **adjacent to the primary
   result** (TA-19, supporting), asserting FR-P1-05-10's Phase 1-applicable contents and
   asymmetry statement **non-empty** and the four Phase 2 quantities shown as **recorded
   not-applicable**;
5. prints every benchmark row's **`beats_model`** flag, any **true** flag enrolling that
   baseline in R-126's abstract-level conclusion check (R-16, the project's highest-rated
   reporting risk, stays a field comparison end to end);
6. asserts the table's units are **TECU, from the artifact's units metadata**, never
   assumed — **BLK-08 ↓'s bound made checked, not silent**: until the co-owner adopts its
   half of the R-103 joint contract, no design path returns model output to TECU, and
   this assertion fires instead of a wrong number shipping;
7. **carries the provenance block and the §5.5 metric fields** — *added 2026-08-28 per
   `GOV-2026-08-28-FD-01` Rec 16 and Rec 20, board option 1 in both cases* — described in
   full at `domain-entities.md` § 1 and summarised here as the assertions this rule makes:
   `mask_id`, `feature_set_id`, per-station `surviving_row_counts`, `exclusion_counts` and
   the `scored_window_statement` are **asserted present** and **printed from the producing
   objects, never restated** (limb 3's pattern), and `rmse`, the `derived: true`-labelled
   relative summary and §5.5's six supporting metrics are asserted present per member.

> **Why limb 7 exists** *(2026-08-28, Rec 16)*. Vision §8.9 requires that *"exclusions and
> row counts are reported"* and that the comparison *"records a stable mask ID and
> feature-set ID"*. `evaluation-and-comparison` R-107 limbs 1–2 record `mask_id` and
> per-station row counts **on the mask**, and `features-and-splits`' partition record
> carries the excluded count — and nothing carried any of them onto the surface a human
> reads. Derived across this unit's four artifacts before the fix: `mask_id` **0**, "row
> count" **0**, "exclusion" **0**, `feature_set_id` **0**. The scored-window statement is
> the fixed sentence **"2–31 December 2022, 30 days, first 24 h excluded and counted"**
> citing **D-28**, and it is **asserted equal to the DEC mask's own asserted scored range**
> (R-109 limb 3) rather than authored independently — one denominator, one place.
> `feature_set_id` is not among R-107's enumerated mask fields today; supplying it is
> `evaluation-and-comparison`'s half of Rec 16, **named not annexed**, and until it lands
> the presence assertion is what fires. `REQ-CLAIM-01`'s own *"tested on December 2022
> only"* text is a **completed-stage artifact and is not edited here** — it is owed an
> owner-approved annotate-in-place or a Vision §15.2 amendment (Rec 16's follow-on), and
> R-126's D-28 disclosure row carries the scope meanwhile.

> **Why the metric fields exist** *(2026-08-28, Rec 20)*. Derived across all 48 stage
> artifacts before the fix: "RMSE reduction", "percentage reduction", "relative summary",
> "1−RMSE" = **0**; `MAE`, `R²`, "median absolute", "90th–95th percentile" = **0**; `RMSE`
> occurred in **one** unit only (`models-and-baselines`, the tuning owner — 13 hits) and
> **0 times** here, in the unit that owns the primary results table. Vision §5.5 makes RMSE
> the primary reported error metric with the derived relative summary
> `1 - RMSE_model/RMSE_reference` and six supporting metrics; Vision §9.5 required result 2
> demands the derived percentage reduction *"clearly labeled as derived"*. The paired loss
> differential remains the confirmatory estimand (Vision §2.3) — RMSE and its reduction are
> the reported error surface and decide nothing. **Upstream origin, recorded honestly:**
> `requirements.md` FR-P1-05-16 cites `[Vision §5.5]` but enumerates only breakdowns and
> never the metric set, and audit finding **`TEC-14`** (`requirements.md:1006`) is already
> **Open** for exactly that re-citation — **a Vision §15.2 amendment to FR-P1-05-16 is owed
> upstream and is not made here**; what this stage specifies is the reported surface, which
> is this stage's to specify.

**Negative controls.** (7) A table rendered with a declared member missing → **fails**
(the render refuses; `FairnessError`). (8) A difficulty control placed outside the
primary table → **fails** the same-table assertion. (9) A benchmark row without a
`beats_model` field → **fails** the presence test. **(32)** A rendered primary table or
breakdown artifact missing **any** of the five provenance fields → **fails** the presence
test *(2026-08-28, Rec 16)*. **(33)** A `scored_window_statement` that does not equal the
DEC mask's asserted scored range → **raises** (**`RegimeError`**, naming both strings and
the mask) *(2026-08-28, Rec 16)*.

**Named, not annexed** *(2026-08-28)*: the cross-module assertion that the table's
`mask_id` names a **registered** frozen mask is hosted by §12's `test_common_masks.py`
(`evaluation-and-comparison`'s lane, Rec 16's closure evidence); this rule asserts presence
and identity at the render and creates no second mask registry.

**Acceptance.** **TA-20 (primary)** — the primary results table with the three controls
alongside the IRI comparison; evidence: the table artifact this path emits. TA-19
(supporting) via limb 4.

## R-126 — The claims-and-limitations checklist: presence checks at named locations, and the §15.2 routing

**Rule (Q4 = C).** The checklist is a **machine-readable artifact produced by a path in
`diagnostics.py`** (`domain-entities.md` § 2): **one row per prohibited class** — the
enumeration maintained in **§ Out of scope C only, cited by reference, never
duplicated** — recording each class **unasserted across every reported artifact**
(REQ-CLAIM-01, implemented as written; the D-8 claim boundary and the D-7 NICO
5-minute bar are rows); and **one row per mandated disclosure**, each recording **where
the text was found, or failing**: every `beats_model = true` baseline in the primary
table **and** the abstract-level conclusion (FR-P1-05-20); FR-P1-05-19's plasmaspheric
sentence at its three points (table caption, abstract-level conclusion, limitations
section); VAL-05's Phase-2-not-independent sentence at the abstract-level interpretation;
the spatial-representativeness sentence **present on every serialized IRI/GIM comparison
artifact** (emitted upstream by R-110 limb 3 — presence asserted here, nothing emitted
here); and the `gim_network_overlap_flag` value wherever GIM is compared once the audit
has run. **The residue that stays human** — whether found text *means* what the rule
requires — is recorded as such on the row, not claimed covered.

**Four additions of 2026-08-28**, each from `GOV-2026-08-28-FD-01` *(the fourth added on the
resume pass, which found it recorded as owed and never written)*:

1. **The TC-12 `prohibited_class` row (Rec 17, board option 3 — both mechanisms).**
   TC-12's interpretive half — *"a station performance difference must never be attributed
   to local forcing the dataset does not contain"* — becomes a `prohibited_class` row with
   **planted-phrase detection**, mirroring the existing D-8 and D-7 rows (control (37)).
   Derived before the fix: `TC-12` = **7** hits in **one** unit (`external-products`) and
   `local forcing` = **2** hits in **one** unit — this unit carried **zero** of either, and
   TC-12 was absent from § 2's `reference` enumeration, while R-127 produces the per-cell
   metrics, the pooled/equal-station split, the quiet/disturbed/storm split, four LST bins,
   daily error and the fold table. Its companion is the **standing caveat R-127 emits from
   the per-station breakdown producing path itself** — the R-110 limb 3 pattern, presence
   asserted here (control (38) at its owning rule), which is the identical
   emitted-there/asserted-here treatment the design already gives TEC-06, so **no new
   mechanism is introduced**. A phrase check catches the obvious wording and not a
   paraphrase; that residue is already recorded under `human_residue`.
2. **The D-28 scored-set `disclosure` row (Rec 16).** `reference` = **D-28**, text =
   **"2–31 December 2022, 30 days, first 24 h excluded and counted"**,
   `required_location` = **the primary-table caption and the limitations section**, and the
   text asserted equal to R-125 limb 7's `scored_window_statement`. Derived before the fix:
   § 2's `reference` enumeration (FR-P1-05-19, FR-P1-05-20, VAL-05, TEC-06, D-8, D-7) had
   **no row** recording that the test scored **30 of 31** December days, while
   `REQ-CLAIM-01` still reads *"tested on December 2022 only"*. A claim-boundary
   overstatement produced by **omission** is invisible to a prohibited-class check, which
   searches for phrases that are *present* — which is why this is a `disclosure` row and
   not a prohibited-class one.
3. **The check's declared subject, and fail-closed (Rec 21, board option 1).** Every row
   whose `required_location` names a text surface resolves `found_at` against the
   **registered, hash-listed `ConclusionSurfaceArtifact`** (`domain-entities.md` § 6) — a
   **registered artifact ID plus a surface plus a location within it**, never an
   implementation-time path — and a row whose surface artifact is **absent, unmanifested or
   unregistered** **fails closed** (control (36)). Derived before the fix: "abstract
   artifact" = **0** across all 48 artifacts; `.tex`/`.docx`/"manuscript" = **0**;
   "conclusion artifact/file/text/document/path/source" = **1**, and that one hit is a
   question-option restatement — **no unit declared the conclusion or limitations surfaces
   as artifacts with an owner, a path, a schema or a producer**, so FR-P1-05-20's criterion
   (*"a disclosure present in the table and absent from the conclusion fails"*) ran against
   an undeclared input. This is the control over **R-16**, the project's highest-rated
   reporting risk. The `beats_model` field itself is well built and **is not disturbed** —
   the defect was entirely on the text side of a field-versus-text comparison. **Which
   surface is authoritative for the thesis text is a Student confirmation**, routed to the
   gate; this rule fixes only that the check has a registered subject and cannot be
   satisfied by pointing at a stub, nor skipped for want of an input.
4. **The NFR-TDEF-01 and FR-P1-03-4 `disclosure` rows (Rec 18, board recommendation
   "(1) plus (3)'s checklist rows" — limb (3)).** *(Added on the resume pass. Limb (1),
   moving NFR-TDEF-01's statement onto the target-writing path, was applied by
   `target-standardization` on 2026-08-28; limb (3) was recorded there as owed by this unit
   and was **not written**, so the routing had no destination.)* Derived before this fix
   across this unit's four artifacts: `NFR-TDEF-01` = **0**, `FR-P1-03-4` = **0** — while
   `target-standardization` `business-logic-model.md:494` states the routing *"currently has
   **no destination**"* in exactly those terms.
   - **`NFR-TDEF-01`** — the **cross-phase target-lineage** mismatch (grid-cell population
     versus IPP population). It is **not** TEC-06's comparison-geometry mismatch and is not
     discharged by TEC-06's row; keeping the two distinct is Rec 18's substance, and
     collapsing them re-creates the defect. `required_location` = **every reported artifact
     describing the Phase 1 target** — primary-table caption, limitations section, and every
     registered target, coverage and release surface — **not only serialized IRI/GIM
     comparisons**. That widening is the fix: a Phase 1 release carrying no comparison
     disclosed the lineage mismatch through no mechanism at all, and Phase 2 compares against
     Phase 1's reported December timestamps, so the mismatch matters most exactly where no
     comparison report is in scope. Emitted upstream on the target-writing path
     (`target-standardization`, Rec 18 limb (1)); **presence asserted here, nothing emitted
     here** — the R-110 limb 3 pattern this rule already uses for TEC-06.
   - **`FR-P1-03-4`** — the notebook-caption case `target-standardization` R-69 routes to
     "FR-P1-03-4's claims-checklist review", which is this checklist and had no such row.
     `required_location` = **every notebook figure caption describing the Phase 1 target**.
     `human_residue` applies and is recorded: whether a caption *means* what the rule
     requires is a human check. This row makes the review reach a surface; it does not make
     a caption machine-verifiable, and no claim to the contrary is made.
   Both rows **fail closed** under addition 3: an absent, unmanifested or unregistered
   surface **fails** rather than being skipped. **Bound stated**: these rows assert presence,
   not authorship — if the upstream emitting path does not write the lineage sentence, the
   row fails, and this unit does not write a second version of it (§ Assumptions carries the
   dependency).

**The acceptance-row routing.** `TST-CLAIMS-01` is named by Vision §11.2 with no §16/§19
row; **adding a criterion is not adding an acceptance row**, and adding a row is a Vision
§15.2 amendment this stage may not make. Candidate rows for **FR-P1-05-20, FR-P1-05-19**
(both named candidates in `requirements.md`), **FR-P1-05-16, FR-P1-05-18 and
`TST-CLAIMS-01`** are **proposed at the gate, never applied here**, each naming the
checklist or test-module evidence it would point at — the owner and, where required, the
supervisor rule on the rows.

**Negative controls.** (10) A `beats_model = true` baseline absent from the
abstract-level conclusion **of the registered `ConclusionSurfaceArtifact`** → **fails**
*(control unchanged in kind; its subject named 2026-08-28 per Rec 21 — a planted
`beats_model = true` baseline present in the primary table and omitted from the registered
conclusion is exactly what this control now falsifies)*. (11) A table caption missing the
plasmaspheric sentence → **fails**. (12) A prohibited-class phrase planted in a reported
artifact → **caught**. **(36)** A checklist run whose `ConclusionSurfaceArtifact` is
absent, unmanifested or unregistered → **fails closed** (**`RegimeError`**, naming the
missing artifact and the rows it would have carried) — never skipped *(2026-08-28,
Rec 21)*. **(37)** A phrase planted in a reported artifact attributing a station
performance difference to local forcing → **caught** *(2026-08-28, Rec 17 — TC-12's
interpretive half)*. **(39)** An abstract-level interpretation missing **VAL-05's
Phase-2-not-independent sentence** → **fails** *(2026-08-28, Rec 43)*.

> **On control (39)** *(2026-08-28, Rec 43)*. VAL-05's disclosure was already **present and
> correct** — `VAL-05` appears **11 times in this unit and 0 times in the other eleven**,
> so the prior board pass's "absent from every stage artifact" finding is **closed and is
> not disturbed**. What was missing was the **named falsifier** the affirmed methodology
> requires: this rule's enumerated controls were (10) a `beats_model = true` baseline
> absent from the conclusion, (11) a caption missing the plasmaspheric sentence, and (12) a
> planted prohibited-class phrase — VAL-05's two neighbours in the same rule each had one
> and VAL-05 did not, which is precisely why its absence was hard to see. Adding (39) makes
> the three disclosures symmetrical; the negative-control count is re-derived and reprinted
> in § Negative-control count below.

**Acceptance.** ⚠ No row today — the five candidate rows above are gate items;
FR-P1-05-14/FR-P1-05-15 remain rowless and covered by R-128's controls meanwhile.

## R-127 — The breakdown family: stamped producing functions, the D-17 bound, the inventory refusal

**Rule (Q5 = C).** Each breakdown FR-P1-05-16 enumerates is a **producing function in
`diagnostics.py`** emitting a machine-readable artifact stamped
`phase_id`/`source_id`/`target_definition_id` (TEC-05): per-cell metrics at +1 h; the
**equal-station macro-average as the headline** and the pooled row-weighted figure as
supplementary — **headline/supplementary a label carried on the artifact**; the
quiet/disturbed/storm split (consuming R-123's labels only); **quality strata from D-17's
measured-available fields only** — `valid_observation_count`, `within_hour_spread_tecu`,
`provider_dtec_summary`, an **enumerated set from config, not free strings**, so a
stratum on satellite count, elevation or zenith angle (absent from the five-column
product) is **unrepresentable by signature**; daily error; four LST diagnostic bins;
**Vision §9.5's F1–F4 validation-fold table**; and **per-seed three-seed stability with
the three per-seed values, the mean and the spread as separate fields** (TE §13.5). The
**top-1%-absolute-error-removed sensitivity** (FR-P1-05-10) is emitted beside its parent
figure, **labelled sensitivity, never merged**. Completeness shortfalls are
**machine-readable fields on the artifact, never console text** (the two-tier posture),
the artifact marked derived and/or partial. The emitted inventory is asserted **complete
against the configured breakdown list** — a missing declared breakdown **refuses the
results artifact** rather than shipping partial (R-110 limb 1's shape, one level down).

**Three additions of 2026-08-28**, each from `GOV-2026-08-28-FD-01`:

1. **The §5.5 metric set enters the configured breakdown list (Rec 20, board option 1).**
   Added as configured rows so R-127's completeness refusal reaches them: **RMSE per
   member**; the **derived percentage reduction** `1 - RMSE_model/RMSE_reference` carrying
   an explicit **`derived: true`** label (Vision §9.5 required result 2, *"clearly labeled
   as derived"* — an unlabelled derived field **fails**, control (34)); and §5.5's **six
   supporting metrics** — MAE, median absolute error, mean error/bias, R-squared,
   correlation, and 90th/95th percentile absolute error. The mechanism is the one already
   built: a config-driven list with a completeness refusal, so a missing metric row
   **refuses** the results artifact under control (18) rather than shipping a table a reader
   cannot connect to Vision §5.4's ten-percent reference magnitude. **The upstream
   re-citation is owed, not made**: `requirements.md` FR-P1-05-16 cites `[Vision §5.5]` and
   enumerates only breakdowns, and audit finding **`TEC-14`** (`requirements.md:1006`) is
   already **Open** for it — a Vision §15.2 amendment to FR-P1-05-16 is owed upstream, and
   this rule specifies the reported surface only.
2. **The standing driver-identity caveat, emitted from the producing path (Rec 17, board
   option 3).** Every **per-station / per-cell** breakdown artifact is emitted carrying a
   fixed caveat field stating that **every external driver value is identical across all
   three cells by construction** and that **no station performance difference may be
   attributed to local forcing the dataset does not contain** (TC-12, `binding: hard`). The
   caveat is emitted by the producing path — R-110 limb 3's pattern, third use in this unit
   — so it **cannot be omitted from a breakdown nobody has written yet**; a per-station
   breakdown emitted without it **fails** (control (38)), and R-126 presence-asserts it.
   The need is measured, not hypothetical: D-11 records ARUC 163/168, BSHM 168/168, NICO
   155/168; D-7 records NICO holding 53.8% of its native 5-minute slots against BSHM's
   89.9%; and the three cells span 32–40°N across roughly 11° of longitude. Per-station
   results **will** differ for reasons the dataset cannot resolve, and the natural,
   physically plausible-sounding explanation — local forcing — is the one explanation this
   dataset structurally cannot support.
3. **The tier-3 breakdown row (the owner's ruling on Rec 19).** The owner ruled that a
   **third declared comparison set `{M-04, M-05, M-06}`** is added, giving Vision §2.4
   tier 3 (LSTM versus direct Random Forest and versus ridge regression) a declared set.
   This rule's contribution is the reported surface Rec 19's closure evidence names: a
   **tier-3 row in the configured breakdown list**, so the completeness refusal reaches it.
   Set **membership**, the third mask's registration and freezing, and §8.9's matched-window
   assertion all remain `evaluation-and-comparison`'s (R-106, R-107, R-108); the **primary**
   set is unchanged, which is the whole point of a third set rather than a widened first
   one. This unit declares no membership and decides no scientific value.

**Negative controls.** (13) A stratum requested on a non-D-17 field → **fails** (the
enumerated-set signature makes it unrepresentable; the control proves a bypass attempt is
caught). (14) A pooled row-weighted figure labelled headline → **fails**. (15) A fold
table missing any of F1–F4 → **fails**. (16) Per-seed stability reported as mean-only →
**fails**. (17) An artifact missing any of the three stamps → **fails**. (18) A declared
breakdown missing from the inventory → **refuses** the results artifact. **(34)** A derived
percentage-reduction field emitted without its explicit `derived: true` label → **fails**
*(2026-08-28, Rec 20)*. **(38)** A per-station breakdown artifact emitted without the
standing driver-identity / no-local-forcing caveat → **fails** *(2026-08-28, Rec 17)*.

**Acceptance.** ⚠ No row — FR-P1-05-16 is `UNTESTED`; the candidate §15.2 row (R-126) is
a gate item, pointing at these controls' evidence.

## R-128 — Practical relevance frozen and demoted honestly; post-access runs labelled

**Rule (Q6 = C).** The practical-relevance comparison is a **producing function** — the
**only** source of any practical-relevance statement:

1. it reads the threshold record with its timestamp, FR-P1-05-10's budget artifact, and —
   *added 2026-08-28 per `GOV-2026-08-28-FD-01` Rec 20* — the **measured improvement**
   (R-127's derived percentage RMSE reduction, with its `derived: true` label intact), and
   **asserts the threshold timestamp precedes the G-06 receipt's** (PC-09: no
   practical-relevance threshold is introduced, changed or reinterpreted after the
   December locked test is opened);
2. it evaluates **both** conjuncts of Vision §5.3's practical-relevance layer, not one:
   - **first conjunct — does the measured improvement reach the reference magnitude?**
     The measured improvement is compared against §5.4's named reference magnitude (*"Ten
     percent RMSE reduction"*, expressly *"a named reference magnitude, not a pass/fail
     rule"*), and the result is reported as such. *Added 2026-08-28 (Rec 20): before this,
     the `INPUT` named the threshold record, the budget artifact, the G-06 receipt
     timestamp and the registry flags but **not the measured improvement**, so this
     conjunct had no input and the practical-relevance function could only ever **demote**
     a claim, never **determine** one — §5.3's success layer 3 was unreportable.* A
     practical-relevance statement produced without the measured improvement present
     **refuses** (control (35)), so the first conjunct cannot be silently skipped;
   - **second conjunct — reference versus budget.** Where the reference is **smaller than
     the target uncertainty budget**, it **emits the descriptive-only label
     on every practical-relevance statement** (Vision §5.4's first constraint) — a claim
     without the label is unrepresentable because no other path produces the statement;
3. it **refuses when either input's units metadata is not TECU** (**`RegimeError`**,
   naming the artifact and the violated expectation) — BLK-08 ↓'s bound checked at the
   exact comparison the register names.

**No threshold is set here.** §5.4's ten-percent figure is a **reference magnitude** the
Vision already fixes, and whether a supervisor-approved *threshold* exists at all remains
the supervisor's (Vision §5.4: *"Practical relevance is reported descriptively unless the
supervisor explicitly approves a threshold"*). This rule reads the frozen record and
compares; it invents no number and reinterprets none (PC-09).

**The reporting-side post-access assertion** (FR-P1-05-14): every run this unit reports
whose registry timestamp postdates a recorded `locked_test_accessed = true` event is
asserted to carry the **exploratory** label — a post-access run reported without it
**fails**. Which surface **writes** the label is the registry writer's design
(`foundation`/`inventory-and-registry`) and is **routed to the gate rather than
annexed** — this unit checks the only surface it can see.

**Negative controls.** (19) A threshold record whose timestamp does not precede the G-06
receipt's → **fails** (a post-G-06 threshold edit caught). (20) A comparison input whose
units metadata is not TECU → **refused** (**`RegimeError`**). (21) A post-access run
reported without the exploratory label → **fails**. **(35)** A practical-relevance
statement produced without the measured improvement present, so Vision §5.3's first
conjunct is unevaluated → **refused** (**`RegimeError`**, naming the missing input and the
unevaluated conjunct) *(2026-08-28, Rec 20)*.

**Acceptance.** ⚠ No row — FR-P1-05-14 and FR-P1-05-15 are `UNTESTED` and remain rowless;
covered by controls (19)–(21) meanwhile, recorded as designed falsifiers, not acceptance
coverage.

## R-129 — `plots.py` is presentation-only by signature, and the manifest is WS-19's evidence

**Rule (Q7 = C).** `plots.py` renders **exclusively from serialized, stamped artifacts**
emitted by producing paths — the metrics artifact, R-127's breakdown artifacts, the
budget artifact, `BootstrapResult`, R-130's labelled diagnostic artifacts. Its API takes
**artifact objects, not raw predictions**, so *"presentation only and computes no
reported quantity"* holds **by signature**, not by comment. Every figure is written with
a **manifest entry** carrying the plot ID, the source artifact IDs and stamps it
rendered, and its axis-units label **taken from the artifact's units metadata** — never
hardcoded, so a TECU axis label can never disagree with the data behind it. The manifest
is asserted **complete against the configured required-plot list** (the prediction,
residual, target-support and quality plots at minimum) — a missing required plot
**refuses** (R-127's inventory shape). The RF-importance and Dst-diagnostic figures
render only from their labelled artifacts, printing the **non-authoritative** /
**diagnostic, hindcast-only** labels those artifacts carry (R-130). The widening-guard
comparator's quarantine (`statistical-inference` R-120) is inherited by construction: no
plot input carries the comparator's numbers, so no figure can render them.

**Negative controls.** (22) A manifest entry missing source IDs → **fails**. (23) A
figure whose units label disagrees with its artifact's metadata → **fails**. (24) A
required plot missing from the manifest → **refused** by the completeness assertion.

**Acceptance.** **WS-19 (primary)** — the required plots exist, each carrying its
source-data IDs; evidence: the plot manifest this path emits.

## R-130 — The diagnostics quarantine: grade discipline, labelled artifacts, and the lane boundary

**Rule (Q8 = C).** Dst hindcast diagnostics are **producing functions in
`diagnostics.py`**: they consume the Dst series **through `external-products`' surface
with its recorded release grade**, assert a **single grade per series** (D-10.1 — mixed
grade **raises**), align per the driver rule (Dst aligned to its own hourly averaging
interval), and emit artifacts **labelled diagnostic/hindcast-only** that live only under
diagnostic paths — never in the metrics artifact, the primary table, or any
feature-bearing artifact (TC-11). A **provisional-grade** series reaching any surface
R-62 bars — a modelling input, a frozen tolerance, a G-05 regime count — **raises at the
point of use** (eligibility is a property of the data, read from the grade field). The
**RF-importance figure renders only from `models-and-baselines`' saved diagnostic
artifact** (`authoritative = false` in its own metadata, R-100), the **non-authoritative**
label emitted with it by the producing path (R-60's pattern, third use) — RF importance
never adds, removes or ranks a feature into the production set, and the production-path
control lives in `models-and-baselines`, not here.

**The boundary stated, not annexed:** the Dst-never-a-feature negative control is
**`features-and-splits`'/WS-11's lane**; this unit's controls are scoped to the surfaces
it actually touches — the same by-lane split R-109 and R-100 both practised.

**Negative controls.** (25) Two Dst release grades mixed in one series → **raises**
(**`RegimeError`** at this unit's point of use; construction-time failure is
`external-products`'). (26) A diagnostic-labelled field found in any feature-bearing or
metrics artifact → **fails** the quarantine presence test. (27) An RF-importance figure
without the non-authoritative label → **fails**. (28) A provisional-grade series reaching
an R-62-barred surface → **raises at the point of use**.

**Acceptance.** ⚠ No row of its own — these controls guard affirmed hard rules (TC-11,
D-10.1, D-11, the RF rule); their evidence is hosted by R-132's module.

## R-131 — The notebooks: one declaration helper, stop semantics, no only-copy

**Rule (Q9 = C).** Each of the four analysis notebooks (`01_data_and_target_audit`,
`02_processor_verification`, `03_features_and_splits_review`, `04_results_and_figures`)
**begins with one `src/` helper call** declaring the expected **dataset version, code
commit, configuration IDs and artifact IDs**; the helper **verifies each against the
workspace and stops with the stated missing-artifact or Internet-access message before
any later cell runs** — REQ-ENG-12's "Run all" semantics **by construction**, never
proceeding on partial state. All four notebooks call `src/` functions only; **none holds
the only copy of any logic class** (§14, §7), and the no-only-copy check is
machine-producible grep evidence. The **header-declaration block is emitted in a fixed
machine-readable form**, so TA-16's evidence column is **a parse, not a screenshot**. The
acquisition notebook is expressly excluded (REQ-ENG-13, `acquisition`'s lane) — the
acquisition-notebook/script diff half of TA-16's evidence attaches there, named not
annexed. **The migrated coverage notebook's home is proposed, not assumed**: REQ-ENG-8's
content is proposed to land in `01_data_and_target_audit` — §12's tree fixes five
notebooks and names no sixth — **routed to the gate**; the D-number-first freeze of its
inline constants remains the recorded team obligation and is not performed here.

**Negative controls.** (29) A deliberately missing declared input → **Run all stops with
the stated message before any later cell**, asserted **per notebook**. (30) A logic class
present only in a notebook → the no-only-copy grep evidence **fails**.

**Acceptance.** **TA-16 (primary)** — notebook header declarations, machine-parsed;
evidence: the fixed-form header block plus control (29)'s per-notebook stop assertion.

## R-132 — `tests/test_regimes_and_reporting.py`: one home for every named control, and the routing

**Rule (Q10 = C).** §12's `tests/` tree — enumeration re-derived 2026-08-28 and printed
below — names **21** modules (**§12's mandated set as amended; see `requirements.md`
REQ-ENG-4 for the current count**) and **none** for regimes, diagnostics, plots, notebooks
or claims. One project-authored module is
**proposed**: `tests/test_regimes_and_reporting.py` (the `test_<subject>.py` convention),
**a twenty-second module beside §12's 21, and — unlike `test_acquisition_window.py` — one
whose addition into §12 would itself require a §12 amendment** (see the corrected
precedent below), hosting **every named negative control
from R-123…R-131** — controls (1)–(40); (31) appended 2026-08-27, (32)–(40) appended
2026-08-28 — on synthetic fixtures (Kp series, artifact
fixtures, planted-text fixtures), no full-year data needed, with:

- fixture parameters declared **constants of the test apparatus**, not scientific values;
- the scientific values (thresholds, window, D-13 count) arriving **from config even
  under test** (TC-03e);
- fixture assertion data in `tests/fixtures/<fixture_id>/fixture_manifest.yaml` (§15.2),
  never hardcoded in test bodies;
- **machine-readable evidence emitted**, named as what the candidate Vision §15.2 rows
  would point at — FR-P1-05-20, FR-P1-05-19, FR-P1-05-16, FR-P1-05-18, `TST-CLAIMS-01` —
  the proposals **routed to the gate, proposed not applied**; FR-P1-05-14 and
  FR-P1-05-15 remain rowless and are covered by the module's controls meanwhile.

### §12's `tests/` enumeration, derived and printed (2026-08-28, `GOV-2026-08-28-FD-01` Rec 27)

Derived by listing every `test_*.py` entry in TE §12's `tests/` block (**TE:673-702**) and
counting them, per `project.md` § Way of Working (*"derive a count programmatically from the
artifact and print it before asserting it"*). **The count is 21**, in tree order:

`test_station_registry.py`, `test_acquisition_window.py`, `test_determinism.py`,
`test_rinex_schema.py`, `test_dcb_sign.py`, `test_hourly_target.py`, `test_iri_denial.py`,
`test_phase_boundary.py`, `test_reuse_registry.py`, `test_feature_availability.py`,
`test_split_embargo.py`, `test_train_only_transforms.py`, `test_common_masks.py`,
`test_models_smoke.py`, `test_checkpoint_restore.py`, `test_bootstrap.py`,
`test_locked_test_guard.py`, `test_release_hashes.py`, `test_prepared_target_schema.py`,
`test_feature_leakage_guards.py`, `test_clean_run.py` — plus the two fixture directories
`tests/fixtures/plumbing_7day/` and `tests/fixtures/scientific_1month/`.

**Set-differenced against `team.md`'s affirmed 17: +4, −0** —
`test_acquisition_window.py`, `test_determinism.py`, `test_prepared_target_schema.py`,
`test_feature_leakage_guards.py`.

**The correction, stated plainly.** This rule, `business-logic-model.md` and this file's
§ Sources previously asserted **"seventeen"** — and two of those sites claimed to be
**derived by scanning the list**, which is the worse half of the defect. The figure traces
to `team.md` § Testing Posture, affirmed **2026-08-16**, before all four §12 amendments
(`CR-2026-08-22-TE-AMEND` took the tree 17 → 19, `CR-2026-08-22-TARGET-SCHEMA-TEST` 19 → 20,
`CR-2026-08-22-LEAKAGE-TA` 20 → 21). `requirements.md:266` (**REQ-ENG-4**, an approved
upstream this unit consumes) already states **21** with the full change-record chain and
preserves the superseded 17/19/20 figures. **The substantive conclusion is unchanged and was
independently verified correct: none of the 21 covers regimes, diagnostics, plots, notebooks
or claims.** Sites corrected in the three design artifacts: `business-logic-model.md:54` and
its W-10 precedent sentence, and this file's § Sources plus this rule's two sites.
**Residual, recorded not fixed:** `functional-design-questions.md` retains **five** stale
`seventeen` sites (lines 65, 357, 359, 362, 530) inside a receipted record this remediation
may not edit, and `team.md` § Testing Posture still carries the superseded 17 — a residual
obligation on the practices gate, not a sweep this stage may perform. *(Derived total across
the unit's four artifacts before the fix: **10** `seventeen` occurrences — 2 in
`business-logic-model.md`, 3 here, 0 in `domain-entities.md`, 5 in
`functional-design-questions.md`. The governance report's "five live sites" undercounts the
editable design-artifact sites by one — there are **5** in the three design artifacts and
**5** in the question file.)*

**The precedent sentence, corrected — and it changes the conclusion.** This rule and W-10
previously cited `test_acquisition_window.py` as the precedent for *"an addition beside
§12's set rather than an amendment to it"*. Under the correct enumeration that module **is
in §12's tree** — written into it on **2026-08-22** under `CR-2026-08-22-TE-AMEND`, on a
**countersignature of 2026-08-16**. So the named precedent is a module that ended up
**inside** §12 by amendment, which undercuts rather than supports the original argument.
The honest consequence: `tests/test_regimes_and_reporting.py` may be **proposed** and
designed here, but **placing it inside §12's tree is a §12 amendment** requiring the same
authority `test_acquisition_window.py` needed — **routed to the gate as an owner/supervisor
item**, not asserted here as an addition needing none. Nothing in this stage creates the
module (G-09 is unsigned), so the routing costs nothing now and prevents creating a test
module without the amendment authority this unit's own reasoning would require.

**G-09 is not signed: the module's design is specified; no module is created.**

**Negative controls.** None new — this rule hosts the set; every control is counted once
at its owning rule.

**Acceptance.** Hosts the evidence for WS-19/TA-16/TA-20's rows and for every candidate
row above; the rows themselves are the owner's/supervisor's to rule on.

---

## Negative-control count, derived not carried

**Re-derived and reprinted 2026-08-28** after the `GOV-2026-08-28-FD-01` remediation added
nine controls. Controls are numbered (1)–(30) in the rules above, plus **(31)**, appended at
R-124 on 2026-08-27 (the iteration-1 Critical fix), plus **(32)–(40)**, appended
2026-08-28 — every append **out of positional order** so no earlier control's number
shifts. Each is counted once at its owning rule.

| Rule | Controls | Count |
|---|---|---|
| R-123 | (1), (2), (3), (4) | 4 |
| R-124 | (5), (6), (31), **(40)** | 4 |
| R-125 | (7), (8), (9), **(32)**, **(33)** | 5 |
| R-126 | (10), (11), (12), **(36)**, **(37)**, **(39)** | 6 |
| R-127 | (13), (14), (15), (16), (17), (18), **(34)**, **(38)** | 8 |
| R-128 | (19), (20), (21), **(35)** | 4 |
| R-129 | (22), (23), (24) | 3 |
| R-130 | (25), (26), (27), (28) | 4 |
| R-131 | (29), (30) | 2 |
| R-132 | none — hosts the set | 0 |

Derivation: 4+4+5+6+8+4+3+4+2+0 = **40 distinct negative controls**, numbered (1) through
(40) with **no gaps and no duplicates** (the assigned numbers, sorted, are exactly 1…40).
**Was 31 before 2026-08-28**; the nine added are (32) provenance-field presence and (33)
scored-window/mask agreement at R-125 (Rec 16); (34) the unlabelled derived reduction and
(38) the missing driver-identity caveat at R-127 (Rec 20, Rec 17); (35) the absent measured
improvement at R-128 (Rec 20); (36) the absent/unregistered conclusion surface, (37) the
planted local-forcing attribution and (39) the missing VAL-05 sentence at R-126 (Rec 21,
Rec 17, Rec 43); (40) the outside-scored-set storm event at R-124 (Rec 15). The two
`## Review` sections in `business-logic-model.md` record 30 and 31 as the counts they
verified on 2026-08-27 and are preserved as the historical record; the live count is **40**.

Three controls that must **not** fire are listed separately (R-123's recorded-grade GFZ
pass path; R-124's legitimate audit read and its confirmatory post-receipt breakdown at a
registered count of three or more) and are not in this count.

## Amendments owed

**Derived against the sibling's re-derived basis, and printed before asserted:
5 + 0 + 1 + 1 + 0 = 7 across 5 units.**

| Source | Owed | Basis |
|---|---|---|
| `external-products` **R-55** | **5**, across **3** units | Derived there (`acquisition` 3, `inventory-and-registry` 1, `external-products` 1), boundary contracts only. Not restated here; a restated count drifts. |
| `features-and-splits` | **0** | Re-derived 2026-08-26 in its § Amendments owed: its three dissolved into ADR-11. |
| `evaluation-and-comparison` | **1** | The BLK-08 resolution package (its R-103), one consolidated amendment. |
| `statistical-inference` | **1** | The R-118 signature amendment — re-verified 2026-08-27 by reading its `business-rules.md` § Amendments owed, which prints exactly the 5 + 0 + 1 + 1 = 7-across-5 derivation this row carries forward. |
| **This unit** | **0** | **No amendment.** `count_storm_events(kp, *, release_grade, source)` is consumed exactly as approved with no signature change; the Q4/Q10 acceptance-row proposals are **Vision §15.2 amendments owned by the owner/supervisor — not boundary-contract amendments to `component-methods.md`, the only class this ledger tracks**. |
| | **7 across 5 units** | 5 + 0 + 1 + 1 + 0 — the total stands unchanged |

**Why the gate items add no rows.** The regime config content (thresholds, window, D-13
threshold under the four-config regime), the migrated notebook's home, the
exploratory-label writer, and the §15.2 acceptance-row candidates are gate confirmations
or owner amendments — configuration content and acceptance vocabulary, not boundary
contracts.

**The 2026-08-28 additions likewise add no boundary-contract amendment** — re-checked
against this ledger's stated scope (*"boundary-contract amendments to `component-methods.md`,
the only class this ledger tracks"*). R-125 limb 7's provenance block and R-127's metric,
caveat and tier-3 rows are **configured list content plus assertions on already-approved
consumed objects**; `domain-entities.md` § 6's `ConclusionSurfaceArtifact` is an
**intra-package shape this stage is assigned to specify** (§ Depth Q1 = B), owned by this
unit, not a cross-package call; R-124's asserted day range reads `experiment.yaml` through
the existing `ConfigSnapshot` surface. `count_storm_events` is still consumed exactly as
approved, with **no signature change**. The obligations the additions create on **other**
parties are gate items, not entries in this ledger: `feature_set_id`'s supply onto the
comparison object (`evaluation-and-comparison`); the §15.2 amendment to FR-P1-05-16 re-citing
Vision §5.5 (`TEC-14`, Open); `REQ-CLAIM-01`'s boundary text (annotate-in-place or §15.2);
placing `tests/test_regimes_and_reporting.py` inside §12 (a §12 amendment, per R-132's
corrected precedent); the authoritative thesis text surface (Student); and D-13's December
day range (Student + Supervisor).

## Requirement coverage

| Requirement | Rules | Acceptance |
|---|---|---|
| REQ-ENG-12 | R-131 | TA-16 (primary) |
| FR-P1-05-9 | R-125 | TA-20 (primary) |
| FR-P1-05-10 | R-125 (budget adjacency, contents), R-127 (top-1% sensitivity) | TA-19 (supporting; `target-standardization` primary) |
| FR-P1-05-11 | R-129 | WS-19 (primary) |
| FR-P1-05-14 | R-128 (control 21) | ⚠ no row — rowless; contract-level control lands in R-128, hosted by R-132's module |
| FR-P1-05-15 | R-128 (controls 19–20, **35**) | ⚠ no row — rowless; contract-level control lands in R-128, hosted by R-132's module |
| FR-P1-05-16 | R-127 (including the §5.5 metric set, the driver-identity caveat and the tier-3 row); R-124 (the storm guard, the asserted day range) | ⚠ no row — contract-level controls land in R-127/R-124; candidate §15.2 row a gate item; **the §5.5 metric-set re-citation is owed upstream (`TEC-14`, Open)** |
| FR-P1-05-18 | R-123 (clauses 3–4, the count); R-124 (clauses 1–2, controls **31**/**40**) | ⚠ no row — contract-level controls land in R-123/R-124; candidate §15.2 row a gate item; the advisory NOT-READY on the source criterion **reported, not fixed** |
| FR-P1-05-19 | R-126 (control 11, the three-location check, resolved against § 6's registered surface) | ⚠ no row — contract-level control lands in R-126; named candidate in `requirements.md`, §15.2 row a gate item |
| FR-P1-05-20 | R-125 (control 9, `beats_model` printed); R-126 (controls 10, **36**) | ⚠ no row — contract-level controls land in R-125/R-126; named candidate in `requirements.md`, §15.2 row a gate item |
| REQ-CLAIM-01 | R-126 (controls 10–12, **36**, **37**, **39**, one row per prohibited class, plus the D-28 scored-set disclosure row) | ⚠ no row — contract-level control lands in R-126; `TST-CLAIMS-01` named by Vision §11.2 with no §16/§19 row; §15.2 row a gate item. **`REQ-CLAIM-01`'s own "tested on December 2022 only" text is a completed-stage artifact, not edited here** — owed an owner-approved annotate-in-place or a §15.2 amendment |

**11 requirements, 7 untested — derived from the story map's rows, the two upstream
artifacts agreeing** (the table above has exactly **11** rows, one per requirement ID; the
2026-08-28 remediation added no requirement and removed none). The 7 without acceptance
rows, by ID: **FR-P1-05-14, FR-P1-05-15,
FR-P1-05-16, FR-P1-05-18, FR-P1-05-19, FR-P1-05-20, REQ-CLAIM-01.** Each one's
contract-level control lands in the rule the table names; **every §15.2 acceptance-row
proposal is a gate item — proposed, never applied here**. The seven-untested figure is
never silently narrowed: designed falsifiers now, acceptance rows by owner amendment.

**Non-requirement obligations newly guarded here (2026-08-28), listed separately so they
never disturb the 11 / 7 count above:**

| Obligation | Rules | Acceptance |
|---|---|---|
| **TC-12**'s interpretive half (`project.md` § Mandated, `binding: hard`) | R-126 (control **37**, the `prohibited_class` row); R-127 (control **38**, the caveat emitted from the producing path) | no §16/§19 row exists or is claimed — guarded by designed falsifiers per Rec 17 |
| **Vision §8.9**'s reported provenance | R-125 limb 7 (controls **32**, **33**); R-127 (the same block on every breakdown) | no §16/§19 row of its own; the `mask_id`-is-registered assertion is hosted by §12's `test_common_masks.py`, `evaluation-and-comparison`'s lane |
| **Vision §5.5 / §9.5 / §5.3** — the reported metric surface and the practical-relevance first conjunct | R-127 (the metric rows, control **34**); R-128 (control **35**) | no §16/§19 row; the §15.2 re-citation of FR-P1-05-16 is owed upstream (`TEC-14`, Open) |
| **D-28**'s 30-day scored-set disclosure | R-125 limb 7 (control **33**); R-126 (the disclosure row) | no §16/§19 row; D-28 itself states the disclosure obligation |
| **VAL-05**'s Phase-2-not-independent sentence | R-126 (control **39**) | no §16/§19 row; the disclosure was already present, the falsifier was not (Rec 43) |

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence: the siblings close at **R-122** (re-derived 2026-08-27 by grepping both heading sets), so this unit opens at **R-123** and closes at **R-132** — **10 rules, derived by numbering this file's headings**. The R-83…R-89 gap is inherited as observed, not explained.
- **[assumption]** **`RegimeError` is one of the fourteen** project exceptions (`foundation` R-01 names it among the eight raised by other units — verified 2026-08-27 against R-01's enumeration), **declared here** — `src/evaluation/regimes.py`, this unit's raise site — importing `IntegrityError` from `src/data/config.py`; `FairnessError` (declared by `evaluation-and-comparison` in `src/evaluation`) and `LockedTestError` (`governance-guards`) are **imported for consumed preconditions, not redeclared**; **no fifteenth exception is minted** — reporting refusals reuse `FairnessError` and `RegimeError` as placed. Every raise names the file or resource and the violated expectation.
- **[assumption]** `src/evaluation/` is a path grant owned by three units (`evaluation-and-comparison` R-112); this unit designs `regimes.py`, `diagnostics.py` and `plots.py` only and narrows nothing of TE §12.
- **[assumption]** The regime thresholds, the −12 h/+24 h window and D-13's three-event threshold arrive via `ConfigSnapshot` from `experiment.yaml`; the key names are `foundation`'s surface.
- **[assumption]** *(added 2026-08-28)* The five provenance values R-125 limb 7 prints are **owned by their producing units** and merely asserted and printed here: `mask_id` and per-station surviving row counts from the registered frozen mask (`evaluation-and-comparison` R-107 limbs 1–2); the DEC scored range from R-109 limb 3; the excluded count from `features-and-splits`' partition record; `feature_set_id` from the feature-set identity `features-and-splits` freezes and `foundation`'s §13.3 `feature_set_ids` manifest field. **`feature_set_id` is not among R-107's enumerated mask fields today** — supplying it is `evaluation-and-comparison`'s half of Rec 16, named not annexed, and until it lands control (32)'s presence assertion is what fires.
- **[assumption]** *(added 2026-08-28)* **D-28 is carried with its own disclosed limits.** D-28 records that Vision §8.2 and TE §7.1 both carry `—` in the Locked-test Embargo column, that a level-4 `requirements.md` paraphrase is the sole textual basis, that the conflict is **disclosed rather than resolved** and carried to G-05, that a revised split manifest is owed at G-05, and that **no supervisor signature exists or is claimed**. This unit encodes the 30-day value and reports those limits; it resolves no conflict and represents the owner ratification as nothing more than what D-28 says it is.
- **[assumption]** *(added 2026-08-28)* The third declared comparison set `{M-04, M-05, M-06}` is the **owner's ruling** on `GOV-2026-08-28-FD-01` Rec 19. This unit adds only the tier-3 reported surface; membership, mask registration and the §8.9 matched-window assertion stay `evaluation-and-comparison`'s, and the **primary** comparison set is unchanged.
- **Verification obligations owned here:** controls (1)–(40) — (31) appended 2026-08-27, (32)–(40) appended 2026-08-28, every append out of positional order — enumerated per rule and counted in § Negative-control count; the three must-not-fire controls; R-132's evidence emission.
- **Governance dependencies owned outside this unit:** BLK-03's contract limbs (`models-and-baselines`); BLK-04's limbs and BLK-09's `train_start` resolution (`features-and-splits`); BLK-08's co-owner adoption of the R-103 joint contract — until then no design path returns model output to TECU, and the primary table, the practical-relevance comparison and every TECU-denominated claim inherit that bound (R-125/R-128 make it checked); the pre-G-05 audit's execution and registration (`inventory-and-registry`); FR-P1-05-18's missing source criterion (a `requirements.md` change); the exploratory label's writer (registry surface — `foundation`/`inventory-and-registry`; gate); the migrated coverage notebook's home (gate); the candidate Vision §15.2 rows (owner/supervisor; proposed, never applied here); the D-number-first freeze of the notebook's inline constants (`acquisition`/`foundation` scaffold territory); G-05's freeze of the evaluation code this stage designs (Supervisor). **Added 2026-08-28:** the pre-G-05 audit's **December day range** (`inventory-and-registry`, amended in parallel per Rec 15) and the range's value (**Student + Supervisor**, D-13 being a supervisor-countersigned demotion threshold); `feature_set_id`'s supply onto the comparison object (`evaluation-and-comparison`, Rec 16); the **Vision §15.2 amendment to FR-P1-05-16** re-citing §5.5's metric set (`TEC-14`, Open — owner/supervisor); **`REQ-CLAIM-01`'s boundary text**, owed an owner-approved annotate-in-place or a §15.2 amendment (Rec 16 follow-on); **which text surface is authoritative for the thesis** (Student, `domain-entities.md` § 6); and **placing `tests/test_regimes_and_reporting.py` inside §12's tree**, which R-132's corrected precedent shows is a §12 amendment (owner/supervisor). **Added on the 2026-08-28 resume pass (Rec 18 limb (3)):** the **emission** of NFR-TDEF-01's cross-phase target-lineage sentence on the target-writing path (`target-standardization`, Rec 18 limb (1), applied there 2026-08-28) — this unit's two new checklist rows assert that sentence's **presence** and never author it, so if the upstream path does not write it the row **fails** rather than this unit emitting a second version; and the **FR-P1-03-4 notebook-caption text** itself, which `target-standardization` R-69 routes here for review and whose `human_residue` stays a human check.
- **Open — all four inherited blockers are EXIT conditions on this stage.** BLK-03 ↓, BLK-04 ↓, BLK-08 ↓, BLK-09 ↓ remain open; nothing in this file closes any of them; this unit may not complete or exit 3.1 while any stands, and no implementation may proceed while they stand.
- **Open — the FR-P1-05-18 advisory NOT-READY stays open**: its criterion still does not test the count's source; R-123 makes the source assertable, and writing the criterion is a `requirements.md` source-criterion change **reported here, not fixed here**.
- **G-09 is not signed.** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged. No rule here authorises creating `src/evaluation/regimes.py`, `diagnostics.py`, `plots.py`, any notebook, or `tests/test_regimes_and_reporting.py`; TE §18.3's stop-and-report rule binds every affected component while any P0 decision is unresolved.
- **Open — the 2026-08-28 remediation's residual obligations, recorded not fixed:** `functional-design-questions.md` retains **five** stale `seventeen` sites (lines 65, 357, 359, 362, 530) inside a receipted record this remediation may not edit; `team.md` § Testing Posture still states the superseded 17-module figure, affirmed 2026-08-16 before all four §12 amendments, which a sweep may not edit — a residual obligation on the practices gate; FR-P1-05-18's advisory NOT-READY on its source criterion remains a `requirements.md` change reported, not fixed.
- **None** of the above decides a scientific value: the thresholds, window, D-13 count, D-8 boundary, D-28's 30-day scored window, §5.5's metric set, the third comparison set's membership and the disclosure sentences are already frozen, ruled by the owner, or routed; everything underdetermined is expressly routed to the gate. In particular, **no regime threshold, no December day range and no storm-count criterion is decided here**, and D-11's bar on any provisional-Dst figure entering a G-05 regime count stands unchanged.

---

> **Re-confirmation receipt, 2026-08-29 — `regimes-diagnostics-reporting`.** The 2026-08-27T21:49:36Z REDO jump reset every unit's
> receipt floor, and this unit's content had already changed after that floor under the 2026-08-28
> post-execution pass (D-29 through D-32; **G-09 signed under D-31 with its TE §18.3 preconditions
> disclosed unmet**). The owner re-confirmed that post-execution content via the Consolidated
> Summary Confirmation at the foot of `functional-design-questions.md`, receipted `2026-08-29`.
> **No line above this marker was touched by this pass**, no count was re-derived, and nothing here
> discharges TA-15, WS-18 or TA-18, creates `aws_ai_dlc_preflight_report`, or alters the fact that
> stage 3.1 remains **FAIL** with no board having passed it.
