# Functional Design Questions — `external-products`

**Unit** `external-products` — the three externally sourced product families: the driver
series with their availability semantics, the IRI-2016 benchmark with its pre-generation
validation, and the CODE final GIM comparator with its interpolation and network-overlap
audit.
**Kind** `library` · **Complexity** L · **Deployment** standalone · **Depends on**
`inventory-and-registry`.

Unit **5 of 12**, running in the same batch as `target-standardization` (both depend only
on `inventory-and-registry`). It owns `src/external/spaceweather.py`,
`src/external/iri.py`, `src/external/gim.py` and
`scripts/04_build_external_products.py`.

**This unit sits on the IRI/GIM containment boundary.** Nothing it produces from
`iri.py` or `gim.py` may reach training or inference: those products join **only at
evaluation time**, onto the already-frozen comparison-wide mask. `spaceweather.py` is
deliberately outside that restriction — drivers **are** model inputs, subject to the
availability lags.

**7 requirements. The untested count is 4, not 5 — and the two upstream artifacts
disagree.** Derived by reading the rows rather than carried from either:

| Source | Untested here | Acceptance rows owned |
|---|---|---|
| `unit-of-work-story-map.md` Table 1 + § Per-unit coverage summary | **4** — REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18 | **WS-09 and TA-36** |
| `unit-of-work.md` § 6 | **5** — the four above **plus FR-P1-04-17** | **1 — WS-09** |

**The story map is the current one.** `TA-36` was approved **2026-08-22** under Vision
§15.2 (`CR-2026-08-22-LEAKAGE-TA`) as the negative-path row for FR-P1-04-17, and the story
map records the sweep — *"Changed 2026-08-22 by the addition of TA-33…TA-36: untested
40 → 36."* `unit-of-work.md` § 6's bold list and its `Acceptance rows (1)` line were not
swept with it. **Question 2 decides what this stage does about that**; it does not edit an
approved artifact.

**TA-36's own status is `Pending`**: the row exists; it is **not implemented, not
executed, not passing.** A row is not a result.

**G-09 is not signed.** `src/external/` does not exist; neither does `src/` or `configs/`.
What does exist and matters here: `scripts/audit_ec1_drivers.py`, whose **line 184 returns
`0` regardless of missing months** — the exit-code gap REQ-ENG-9 exists to close.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 6 — the `Owns` list, the module-path allowlist, the 7 requirements, and the implementation notes.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2 plus § Per-unit coverage summary. **Derived by reading the rows:** 7 requirements, **4** with no acceptance row; **owns** WS-09 and TA-36; **supports** WS-10, WS-11, TA-08, TA-12.
- `../../../inception/requirements-analysis/requirements.md` — REQ-ENG-9; FR-P1-04-3, -4, -9, -15, -17, -18.
- `../../../inception/application-design/components.md` § `src/external` — the three modules and the importable-only rule.
- `../../../inception/application-design/component-methods.md` — which carries `src/features`, `src/models` and `src/evaluation` boundary-call blocks and **no `src/external` block at all** (Question 1).
- `../../../inception/application-design/services.md` § The nine stage scripts — `04_build_external_products.py`.
- `../inventory-and-registry/functional-design/business-rules.md` — R-44's source inventory and R-45's registry, both consumed here.
- `evidence/DECISIONS.md` — **D-5**, **D-10.1**, **D-10.2**, **D-10.3**, **D-11**, **D-21/22/23**.
- Workspace inspection, 2026-08-23: `scripts/audit_ec1_drivers.py` (including line 184), and the absence of `src/` and `configs/`.
- Absent by scope design: `stories` (2.4 `SKIP`), `mockups` (1.6 and 2.5 `SKIP`). `kind: library`, so `frontend-components.md` is not produced.

---

## Question 1

**`src/external` has no contract block.** `components.md` § `src/external` names the three
modules and states the importable-only rule. `component-methods.md` carries boundary-call
blocks for `src/features`, `src/models` and `src/evaluation` — and **nothing for
`src/external`**: no signature, no dataclass, no raise-contract, for any of
`spaceweather.py`, `iri.py` or `gim.py`.

**This is the third consecutive unit whose design finds a named module with no contract** —
`acquisition`'s named accessors, `inventory-and-registry`'s `inventory.py`, and now an entire
package. The first two are recorded as amendments owed.

> **Corrected 2026-08-23 after two adversarial passes.** Superseded text, preserved:
> *"`governance-guards`' `open_d9_input`…"* — that accessor is **`acquisition`'s** finding
> about `governance-guards`' module; `governance-guards`' own artifacts record **no**
> missing-contract finding. The running total below was likewise wrong; see the Consolidated
> Summary Confirmation.

How is the absence handled?

A) Design all three modules' contracts here as settled by this stage
   > **Impact**: Fastest, and this unit owns them. But `component-methods.md` is an approved stage-2.6 artifact, and treating three new module contracts as settled without a change record is the defect an adversarial reviewer caught two units ago — with the finding still in that unit's Review section.

B) Design them here and record the package as **one** amendment owed to `component-methods.md`
   > **Impact**: Consistent with how the two prior units recorded theirs, so all three read the same way. One amendment covering three modules keeps the change record proportionate to the gap. Costs a fourth entry on a pile that is becoming the story.

C) Design only `spaceweather.py` here; raise `iri.py` and `gim.py` as blocked
   > **Impact**: Draws the line where the containment risk is — the IRI/GIM modules are the ones the import-boundary rule and NFR-IRI-01 exist to constrain. But WS-09, which this unit owns, is precisely the IRI/GIM row, so blocking those two blocks the unit's only currently-passing acceptance path.

D) B, plus this stage recording that **three units in a row have now found a named module with no contract**, and proposing the owed amendments be carried as **one consolidated change record** rather than separately
   > **Impact**: Treats the recurrence as the finding it is, rather than filing another instance of the same defect. A single change record is also easier for a reviewer to judge as a set — whether `component-methods.md` is systematically under-specified — than several arriving one unit at a time. Costs proposing a governance action this stage does not own. **The count, corrected 2026-08-23: FIVE owed amendments across three units**, boundary contracts only — `acquisition` 3, `inventory-and-registry` 1, this unit 1. **Superseded:** *"six owed amendments across three units — `acquisition` 3, `inventory-and-registry` 2, this unit 1."*

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A repeats a caught defect. C blocks WS-09, the one acceptance row this unit can currently satisfy, to avoid a risk the design's own containment rules already address. B is correct and incomplete: filing another instance without naming the pattern is how a systemic gap gets recorded as coincidences. D is B with the recurrence stated — and the consolidated-change-record proposal is offered to the owner, not taken.

[Answer]: D

---

## Question 2

Two approved upstream artifacts disagree about this unit, and both are `consumes` inputs
to this stage:

| Claim | `unit-of-work.md` § 6 | `unit-of-work-story-map.md` |
|---|---|---|
| Untested requirements | **5** (bold list includes FR-P1-04-17) | **4** (§ Per-unit coverage summary: `external-products (4)`) |
| Acceptance rows owned | **1** — WS-09 | **WS-09 and TA-36** |

The story map is the one that moved: **TA-36 was approved 2026-08-22** under Vision §15.2
(`CR-2026-08-22-LEAKAGE-TA`) as FR-P1-04-17's negative-path row, and the story map records
the resulting sweep. `unit-of-work.md` § 6 was not swept with it.

`CHANGE_RECORD_PROCEDURE.md` reserves approved-stage artifacts: a sweep **reports**, it does
not edit, absent owner approval for annotate-in-place.

What does this stage do?

A) Follow `unit-of-work.md` § 6 — it is this unit's own definition
   > **Impact**: Uses the artifact written specifically about this unit. But it would state 5 untested and 1 acceptance row, both superseded by an approved §15.2 amendment — the artifacts would carry a number that was correct in August and is not now.

B) Follow the story map, and note the discrepancy in passing
   > **Impact**: Uses the current figures, which is right. A passing note is cheap. But it leaves a reader who opens `unit-of-work.md` § 6 next month with no way to know which of the two they are looking at.

C) Follow the story map, and **report the discrepancy explicitly at the gate** with both readings, the amendment that caused it, and the exact stale text
   > **Impact**: Matches `CHANGE_RECORD_PROCEDURE.md` — report, do not edit — and gives the owner what they need to decide whether to sweep `unit-of-work.md` § 6. This project has already recorded that a sweep keyed to a superseded numeral is blind to stale *claims* carrying no numeral, and `Acceptance rows (1)` is exactly that shape. Costs a gate item.

D) C, plus this stage's own artifacts stating **TA-36's `Pending` status** wherever they cite it
   > **Impact**: Closes the second, subtler trap: TA-36 exists as an approved row but is **not implemented, not executed, not passing**. Citing it as an acceptance row without its status would let a reader infer FR-P1-04-17 is covered — the exact failure that made FR-P1-02-8 look covered behind a withdrawn `TA-29` for five revisions. Costs repeating a status label.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A adopts superseded figures. B is right and forgetful. C is the procedure this project has written down. D adds the limb that matters most here: a row that exists but has never run is the precise shape of the defect that survived four governance boards on FR-P1-02-8, and the cost of stating `Pending` beside TA-36 is three words.

[Answer]: D

---

## Question 3

The import-boundary rule is stated at **module-path** granularity, quoted from
`unit-of-work.md` § 6: IRI/GIM imports are permitted **only** in
`scripts/04_build_external_products.py` and modules under `src/evaluation/`. An import
from `src/data`, `src/features`, `src/models`, `src/gnss`, a training script or a notebook
violates it **identically**.

The complication: **`src/evaluation/` is owned by three different units** —
`evaluation-and-comparison` (`masks.py`, `metrics.py`), `statistical-inference`
(`bootstrap.py`), and `regimes-diagnostics-reporting` (`regimes.py`, `diagnostics.py`,
`plots.py`). The allowlist grants an authorized **path**, never a whole unit's unrelated
code.

`governance-guards`' **R-23/R-24** already enforce the *data-flow* IRI rule at run time and
keep a static scan as the subordinate limb. This is a distinct, module-graph constraint.

How is the allowlist enforced?

A) A static import scan asserting no module outside the allowed paths imports `iri` or `gim`
   > **Impact**: Directly checks the rule as stated, cheap, and it is the same `ast`-walk shape `tests/test_phase_boundary.py` already uses. But a static scan cannot see a dynamic import assembled at run time, and it says nothing about the *transitive* case — module C importing B which imports `gim`.

B) A, extended to **transitive** reachability rather than direct imports only
   > **Impact**: Closes the realistic evasion: a helper in `src/features` that imports a shim that imports `gim` satisfies a direct-import check and violates the rule. `project.md` § Forbidden states the constraint as *"directly or transitively"*, so a direct-only check does not implement the rule it cites. Costs building the import graph rather than scanning one file at a time.

C) B, plus a run-time assertion inside `iri.py` and `gim.py` that the importing module is on the allowlist
   > **Impact**: Holds inside the Kaggle session, where the bolt-plan's confidence hypothesis says enforcement must hold and where a static scan of a checkout proves nothing. But it makes the two guarded modules aware of their callers — the coupling `governance-guards` R-28 declined for the same reason, and here it would name three sibling units' paths.
   
D) B, with the run-time limb declined **for the stated reason** and the static scan's status declared **authoritative for this rule** rather than subordinate
   > **Impact**: Distinguishes this constraint from the phase-boundary one honestly. The module graph is a property of the *source tree*, not of a running process — unlike a loaded module, which is why `assert_phase_boundary` reads `sys.modules`. A static analysis is the right authority for a static property, and saying so prevents a reader importing R-24's subordinate-scan framing where it does not apply. Costs stating the asymmetry explicitly.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A under-implements the rule its own citation states. B is the necessary mechanism. C's instinct — run-time enforcement — is right for the phase boundary and wrong here: an import allowlist is a claim about the source tree, and checking it at run time both couples the guarded modules to three sibling units' paths and catches the violation later than a scan would. D is B with the asymmetry stated, which matters because the neighbouring unit's design declares its static scan *subordinate* and an unexplained inconsistency between the two reads as an oversight.

[Answer]: D

---

## Question 4

`project.md` § Forbidden, quoted: *"NEVER use a centered rolling/trailing window for
F10.7 — only the trailing 81-day mean ending at the safe-lagged day is permitted; a
centered mean uses future days and is a defect, not a fallback."*

The failure is **invisible in validation**: a centered mean produces a smoother, entirely
plausible series, and every downstream check passes. It surfaces only as unexplained
optimism against a benchmark, or not at all.

How is trailing-ness proven?

A) The implementation uses a trailing window; review confirms it
   > **Impact**: Costs nothing. But this is a leakage rule whose violation is undetectable downstream, and §16/§19 both state that visual inspection alone is insufficient. "We looked at it" is the evidence class this project's methodology rejects.

B) A test asserting the 81-day mean at day *d* equals the mean of the 81 days **ending at** the safe-lagged day
   > **Impact**: Directly asserts the definition, and it fails on a centered window. Cheap and precise. But it tests the value at chosen days; a window that is trailing everywhere except at a boundary — the series start, or across the March F10.7 gap — can pass a spot check.

C) B, plus a **future-independence** assertion: perturbing any day after the safe-lagged day must leave the computed mean **unchanged**
   > **Impact**: A property rather than a spot check — it catches any use of a future day, at any index, including boundary handling and gap fill, without enumerating cases. This is the strongest available statement of what "no future days" means, and it fails loudly on a centered window at every point rather than at sampled ones. Costs one perturbation fixture.

D) C, plus the same future-independence property asserted for **every** driver series, not only F10.7
   > **Impact**: Generalises the guarantee — Kp/ap3, Hp60/ap60 and Dst all carry availability lags, and the same class of error is possible in each. But D-10.2 governs those by an *alignment* contract rather than a window, and FR-P1-04-17 already tests that with two named negative controls; a second, differently-shaped guarantee over the same series risks two rules about one fact.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A is barred by the acceptance standard. B tests the definition at sampled points, which is where a boundary or gap-fill defect hides. C converts the rule into a property that holds at every index — perturb a future day, the mean must not move — and that is exactly what "uses future days" means, stated so a test can fail on it. D's generalisation is attractive but collides with FR-P1-04-17's alignment contract, which already owns the other three series and has its own approved negative-path row.

[Answer]: C

---

## Question 5

**D-10.2's alignment contract**, quoted through FR-P1-04-17: Kp/ap3 is repeated **only
within its own defined 3-hour interval**; Dst is aligned to **its own hourly averaging
interval** and is *"not shifted to a neighbouring hour for convenience"*; F10.7 is daily;
and **no driver is interpolated, at any stage**.

This is **distinct from** FR-P1-04-3's ≤3 h carry-forward, which governs a *missing* value.
Alignment governs how a *present* value maps onto the hourly grid.

**TA-36 is the approved negative-path row** for this — and its status is **`Pending`: the
row exists; not implemented, not executed, not passing.** Its criterion names **two**
negative controls plus a grep-level check.

What does this unit build against TA-36?

A) The two named negative controls — Kp repeated outside its interval fails; Dst shifted to a neighbouring hour fails
   > **Impact**: Exactly what TA-36's criterion states, and no more. Precise and defensible. But TA-36's criterion also names a `grep`-level check that no interpolation call appears on any driver series, and building two of three leaves the row partially satisfied while looking complete.

B) A, plus the grep-level no-interpolation check
   > **Impact**: All three limbs TA-36 names. The interpolation limb matters independently: *"no driver is interpolated, at any stage"* is absolute, and a grep is the only check that reaches a call site no fixture exercises. Costs nothing beyond the two tests already required.

C) B, plus an assertion that the alignment contract and the carry-forward contract are **tested separately**, so neither passes on the other's evidence
   > **Impact**: Closes a confusion the requirement itself flags — FR-P1-04-17 says explicitly that it is *"distinct from FR-P1-04-3's ≤ 3 h carry-forward"*. Two rules governing adjacent behaviour on the same series are exactly where one test gets counted twice. Costs stating the separation and one assertion.
   
D) C, plus this unit's artifacts recording TA-36's `Pending` status wherever they cite it
   > **Impact**: Prevents the row being read as a passing result. A row that exists but has never run is the shape of the FR-P1-02-8 defect that survived four governance boards behind a withdrawn `TA-29`. Costs three words per citation.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A builds two of the three limbs its own acceptance row names. B completes them. C adds the separation the requirement text itself insists on, and this project has already had a requirement counted as covered because a neighbouring row's evidence was accepted for it. D carries TA-36's status, which is the cheapest defence against the single failure mode this document has recorded most often — a citation read as a result.

[Answer]: D

---

## Question 6

FR-P1-04-15: **the IRI-2016 benchmark is validated before generation, and generation is
blocked if validation fails** — *"a validation failure **blocks** benchmark generation
rather than warning."*

The `iri_implementation_validation_report` must record: the pinned package/build with exact
version or commit; all model switches and the topside option; **the altitude ceiling stated
explicitly as 2000 km**; units and output extraction; the coordinate, time, solar and
geomagnetic driver inputs **with confirmation that no driver is future-centered or
unavailable at target time**; and **five to ten samples** spanning sites, day and night,
quiet and disturbed, validated against the **official IRI interface** within a tolerance
**predeclared before the comparison runs**.

**FR-P1-04-15 has no acceptance row.** The blocking behaviour, the report's completeness,
and the predeclared tolerance are all unrowed.

How is "blocks, not warns" built?

A) The generation function checks for a passing report and refuses without one
   > **Impact**: Implements the sentence directly. But "a passing report exists" is satisfiable by a report whose tolerance was chosen after the comparison ran — which is the failure the *predeclared* clause exists to prevent, and which no presence check can see.

B) A, with the tolerance **recorded with a timestamp preceding the comparison**, and generation refusing if the ordering is violated
   > **Impact**: Makes the predeclaration checkable rather than asserted, using the same ordering-evidence shape `inventory-and-registry` adopted for retrospective split redesign — a frozen value plus a timestamp is the only evidence class that distinguishes *declared before* from *fitted after*. Costs recording one timestamp and asserting one ordering.

C) B, plus the report's **required content asserted field by field**, so an incomplete report fails rather than passing on presence
   > **Impact**: FR-P1-04-15 enumerates seven content areas and a 5–10 sample range; a report missing the altitude ceiling or the driver-availability confirmation would otherwise pass a presence check. This is the same list-plus-completeness-test shape used three times already in this design. Costs one enumeration that must stay current.

D) C, plus the benchmark's **own drivers appearing as rows in the same frozen availability matrix used for ML features**
   > **Impact**: FR-P1-04-15's criterion states this explicitly, and it is the limb that makes the benchmark's fairness checkable: a benchmark fed better-timed drivers than the model gets is not a benchmark. Each row carries observation timestamp, publication timestamp, release status and safe lag. Costs extending the availability matrix, which `features-and-splits` owns.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A implements the sentence and not the clause that gives it force. B makes the predeclaration real. C stops an incomplete report passing on presence, which is the same defect class as a short protected-set list passing a membership check. D is stated in the requirement's own criterion and is the limb with scientific consequence: it is what stops the IRI benchmark being quietly advantaged relative to the model it is benchmarking. Note that D's matrix is `features-and-splits`' artifact, so this unit states the obligation and does not own the row.

[Answer]: D

---

## Question 7

FR-P1-04-18 states **four** obligations as one contract, because Vision §6.10 does:

1. Interpolation is **bilinear in space, linear in time, with a longitude-rotation
   correction** — a §18.2 **Student-owned forbidden choice** (Q-15), so **no implementer
   may pick it**.
2. *"One sample interpolation must be hand-checked against the code"*, and **EV-11 places
   that hand-calculation BEFORE comparator generation.**
3. Because Madrigal binned VTEC is the adopted Phase 1 target, §6.10's conditional is
   **live**: the Phase 1 GIM comparison *"is explicitly a map-product-to-map-product
   comparison … cannot validate receiver-level station VTEC or serve as an independent
   target check"* — and that sentence is **stated wherever the comparison is reported**.
4. The comparator is **never tuned and then claimed independent**.

**FR-P1-04-18 has no acceptance row.** Its criterion requires the report to carry the
interpolation rule, the hand-checked sample **with its worked arithmetic**, and the
map-to-map statement, and that *"a comparator generated before the hand-check **fails**
rather than being accepted retrospectively."*

How are the four built?

A) The report carries all four, and generation checks the report exists
   > **Impact**: One artifact, one check. But obligation 2 is an *ordering* claim and obligation 4 is a claim about what was never done — neither is provable by a report's existence, and obligation 1 is a decision this stage may not make at all.

B) A, with the hand-check's **timestamp asserted to precede** comparator generation, generation failing otherwise
   > **Impact**: Implements the criterion's own wording, and it is the same ordering-evidence shape as Question 6's predeclared tolerance and `inventory-and-registry`'s split-redesign hash. Retrospective acceptance becomes a failure rather than a judgement call. Costs one timestamp comparison.

C) B, plus the map-to-map sentence emitted **by the reporting path itself**, not left to a human to remember
   > **Impact**: Obligation 3 says the sentence appears *"wherever the comparison is reported"* — a rule about every future report, including ones nobody has written yet. Emitting it from the code that produces the comparison is the only form that survives a new report being added. Costs coupling the sentence to the output path.
   
D) C, plus obligation 1 recorded as **BLOCKED pending the Student's Q-15 decision**, with generation refusing while the interpolation rule is unset
   > **Impact**: The interpolation rule is a §18.2 forbidden-choice item, and `project.md` § Forbidden bars any implementer filling a `TBD — freeze gate` value by convenience. A design that specifies the mechanism without recording that the *value* is not this stage's to set would invite exactly that. Refusing to generate while it is unset is the zero-TBD preflight's shape. Costs surfacing a blocker.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A cannot carry obligations 2 or 4 and quietly steps past 1. B makes the ordering real. C is what obligation 3 actually asks for — a sentence that must appear in every report, present and future, belongs in the path that writes them. D adds the limb this project's rules make mandatory: the interpolation rule is Student-owned, and stating the mechanism while leaving the value implicitly fillable is precisely what TE §18.2's "no implementer or coding agent may fill such a value by convenience" prohibits. Obligation 4 stays a reporting-discipline rule with no code check, and that is stated rather than papered over.

[Answer]: D

---

## Question 8

**REQ-ENG-9**, and the workspace fact behind it: `scripts/audit_ec1_drivers.py` **line 184
returns `0` regardless of missing months.** The requirement closes that gap — *"a
completeness shortfall is recorded as a machine-readable field in the output manifest, an
integrity violation terminates the run naming the file and the violated expectation."*

**REQ-ENG-9 has no acceptance row.** Its criterion names two injections: a missing month
must yield a non-silent machine-readable record; a hash mismatch must yield a non-zero exit
with a naming message.

The script migrates here, gaining `--config configs/` and its numbered position.

What does the migration do about the gap?

A) Fix the exit code — return non-zero when months are missing
   > **Impact**: The obvious reading, and it makes the failure visible. But it collapses the project's two-tier posture: a missing month is a **completeness shortfall**, which `team.md` § Code Style says is non-fatal and recorded as a machine-readable field, not a termination. This fix would make an ordinary partial retrieval abort the run.

B) Record missing months as a machine-readable manifest field; terminate only on integrity violations
   > **Impact**: Exactly the two-tier posture, and exactly what REQ-ENG-9's text says. The distinction is real here: a month absent from the provider is a fact to record; a hash that does not match is a fact that invalidates everything downstream of it. Costs distinguishing the two in code rather than in prose.

C) B, with **both** injections built as tests — a missing month and a hash mismatch — asserting the two different behaviours
   > **Impact**: REQ-ENG-9's criterion names both, and they prove opposite things: one that the run continues with a record, one that it stops. A single test covers half the requirement and would let the other half regress silently. Costs two small tests.
   
D) C, plus the manifest field carrying **which** months are missing rather than a count
   > **Impact**: A count tells a reader something is wrong; the list tells them what to do. This unit's outputs feed G-P1A's coverage decision, where `inventory-and-registry` must report per-station-month figures and *"never an unattributed number"* — a bare count of missing months is that same shape. Costs a list where a count would fit.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A misreads the gap as an exit-code bug when it is a tier question, and would make a normal partial retrieval fatal. B is the correct behaviour. C builds both halves of a criterion whose two halves assert opposite outcomes — the case where one test genuinely cannot stand for the requirement. D makes the recorded shortfall actionable and consistent with the neighbouring unit's no-unattributed-number rule, at the cost of a list instead of an integer.

[Answer]: D

---

## Question 9

**Dst carries three separate restrictions**, and they are easy to blur:

1. **Diagnostic/hindcast-only** — never a confirmatory ML feature (`project.md`
   § Mandated; TC-11).
2. **Release grades never mixed within one series**, with the grade for calendar 2022
   recorded before use (D-10.1).
3. **Provisional Dst may characterise fixture selection only** — never a modelling input,
   never a frozen tolerance, and **never a G-05 regime count** (D-11).

Restriction 3 is the one with a live trap: `evidence/audit_ec1_2026-08-15/kyoto_dst/dst_provisional_202212.html`
exists in the workspace, D-11 used provisional Dst to characterise the fixture window, and
**D-13 requires the December regime count to come from GFZ Kp/Hp60 at a recorded release
grade** — explicitly barring any provisional-Dst-derived figure.

`governance-guards` **R-26** separately names Dst as the driver class excluded from the
December-hit definition, on the grounds that it is diagnostic-only.

How does this unit keep the three apart?

A) State all three in the design and rely on downstream units to honour them
   > **Impact**: They are stated in three governing documents already, and restating them costs nothing. But restriction 1 is enforced by `features-and-splits`, restriction 3 partly by whoever computes the regime count, and a rule that depends on three units remembering is the shape D-15 warns about for the restricted root.

B) A, plus a **grade field on the series** that a consumer must read, with mixed grades failing at construction
   > **Impact**: Makes restriction 2 enforceable where the series is built, which is here. `inventory-and-registry`'s R-40 already requires a single recorded grade per series; this is its construction-side counterpart. But it leaves restrictions 1 and 3 as prose.

C) B, plus the **provisional grade rendering the series ineligible** as a modelling input, a frozen tolerance, or a regime-count source — asserted at the point of use rather than trusted
   > **Impact**: Turns D-11's restriction into a property of the data rather than a rule about the data: a provisional-graded series cannot be consumed for those three purposes because the consumer checks the grade. It also makes the fixture-characterisation use, which **is** permitted, explicitly distinguishable from the three that are not. Costs the consumers reading a field.
   
D) C, plus a test that a **regime count computed from a provisional-graded series fails**, naming D-13's GFZ Kp/Hp60 requirement
   > **Impact**: The negative control for the specific trap that exists today — a provisional December Dst capture sits in the workspace, and D-13 bars exactly that figure from the G-05 regime count. Without the test, restriction 3 is a sentence in a decision record. Costs one test, and it is the one restriction with a concrete artifact already present to get it wrong with.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A leaves three restrictions to three units' memory. B enforces the one this unit can enforce at construction and stops there. C makes the eligibility a property the consumer must check, which is the only form that survives a consumer nobody has written yet. D adds the negative control for the restriction with a live artifact in the workspace and a named G-05 consequence — and this project's affirmed methodology pairs a negative control with every hard rule rather than with the convenient ones.

[Answer]: D

---

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence — `foundation` R-01…R-17, `governance-guards` R-18…R-29, `acquisition` R-30…R-43, `inventory-and-registry` R-44…R-53 — so this unit opens at **R-54**. If per-unit numbering was intended, say so at the gate and the artifacts restart.
- **[assumption]** The **story map governs** where it and `unit-of-work.md` § 6 disagree, because TA-36's 2026-08-22 approval is what moved it. Question 2 decides how that is recorded; neither artifact is edited by this stage.
- **[assumption]** `TA-36` is `Pending` — the row exists and has never run. Cited with that status throughout.
- **[assumption]** The availability matrix FR-P1-04-15 requires the benchmark's drivers to appear in is **`features-and-splits`' artifact**. This unit states the obligation and does not own the row.
- **[assumption]** `audit_ec1_drivers.py` migrates here with `--config configs/` and its numbered position. This stage designs the target shape, not the migration commit.
- **Open — `src/external` has no contract block in `component-methods.md`**, for any of its three modules. Question 1 addresses it; whatever is designed is an amendment owed.
- **Open — FIVE owed amendments across three units**, boundary contracts only: **`acquisition` 3** (the named accessors `open_d9_input` and the restricted writer; the `AccessRecord.purpose` extension plus a restricted-write function; `write_release`'s `identity_fields` parameter), **`inventory-and-registry` 1** (`Station`'s provenance field — its `inventory.py` contract is **intra-package** and owes nothing), **this unit 1** (boundary blocks for `iri.py`, `gim.py` and `spaceweather.py`). Question 1 proposes carrying them as one consolidated change record; that is the owner's call. **Corrected twice on 2026-08-23.** First: the opening reading said "four across three" and attributed the named accessors to `governance-guards`, which recorded no such finding. Then: **"six across three"** was corrected once `component-methods.md` § Depth was read — it specifies **cross-package boundary calls only** and names **this stage** as where intra-package shapes are specified, which removes `inventory-and-registry`'s `inventory.py` from the count and narrows this unit's from "the `src/external` package" to its three boundary-importable modules.
- **Open — FR-P1-04-18's interpolation rule is a §18.2 Student-owned forbidden choice (Q-15)** and is **not set**. No implementer may fill it by convenience.
- **Open — four requirements with no acceptance row**: REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18. The artifacts state what evidence would close each and draft no §19 criterion.
- **Open — `unit-of-work.md` § 6 carries stale text**, reported not edited: a five-item bold list including FR-P1-04-17, and `Acceptance rows (1). WS-09`. Both were correct before 2026-08-22.
- **Open — BLK-07's authorization limb**, carried forward. Nothing in this unit reads the locked month, but its products join at evaluation time onto the frozen comparison-wide mask.
- **G-09 is not signed.** No answer here authorises creating `src/external/spaceweather.py`, `src/external/iri.py`, `src/external/gim.py` or `scripts/04_build_external_products.py`.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

---

## Consolidated Summary Confirmation

Questions 1–9 are answered above as the recommended option in each case, on the
owner's instruction to apply the recommendations. Consolidated:

| Q | Answer | What it settles |
|---|--------|-----------------|
| 1 | D | `src/external`'s three modules get **boundary contracts** here, recorded as **one amendment owed**; and this stage proposes the **five** owed amendments (`acquisition` 3, `inventory-and-registry` 1, this unit 1) be carried as **one consolidated change record** — offered to you, not taken. **Corrected 2026-08-23**; superseded: *"three consecutive units have now found a named module with no contract… the six owed amendments (… `inventory-and-registry` 2 …)"* |
| 2 | D | The **story map governs** (4 untested; **owns WS-09**); `unit-of-work.md` § 6's stale five-item list and `Acceptance rows (1)` line are **reported at the gate, not edited**; and **TA-36's `Pending` status** is stated wherever it is cited. **On TA-36 the story map contradicts itself**, and § Cross-unit responsibilities is the reconciling statement: **`features-and-splits` holds enforcement and the primary negative-path acceptance test** (`tests/test_feature_leakage_guards.py`); **this unit holds data production and upstream evidence**. This stage does **not** reallocate |
| 3 | D | The import allowlist is enforced by a **transitive** static reachability scan; a run-time caller check is declined with its reason; and the scan is declared **authoritative for this rule** — a module graph is a property of the source tree, unlike the phase boundary's `sys.modules` check |
| 4 | C | F10.7 trailing-ness proven as a **property**: perturbing any day after the safe-lagged day must leave the 81-day mean unchanged. Catches boundary and gap-fill cases a spot check misses. Not generalised to the other drivers, which FR-P1-04-17 already governs |
| 5 | D | All three TA-36 limbs built (Kp outside its interval fails; Dst shifted fails; grep finds no interpolation call), alignment and carry-forward asserted **separately**, and TA-36 cited with its `Pending` status |
| 6 | D | IRI generation **blocked** without a passing report; the tolerance **timestamped before** the comparison; the report's seven content areas asserted field by field; and the benchmark's own drivers appearing in the same frozen availability matrix as ML features — that matrix being `features-and-splits`' artifact, so this unit states the obligation and does not own the row |
| 7 | D | GIM: hand-check timestamp **precedes** comparator generation or generation fails; the map-to-map sentence emitted **by the reporting path** so it survives reports nobody has written yet; and obligation 1's interpolation rule recorded as **BLOCKED pending the Student's Q-15 decision**, with generation refusing while it is unset |
| 8 | D | REQ-ENG-9's gap closed **as a tier question, not an exit-code bug**: missing months recorded as a machine-readable field naming **which** months; integrity violations terminate; both injections tested, asserting opposite outcomes |
| 9 | D | Dst's three restrictions kept apart: a **grade field** failing on mixed grades at construction; **provisional grade rendering the series ineligible** as a modelling input, a frozen tolerance or a regime-count source; and a test that a regime count from a provisional-graded series **fails**, naming D-13's GFZ Kp/Hp60 requirement |

**One answer surfaces a blocker rather than designing past it.** Q7 records
FR-P1-04-18's interpolation rule as **BLOCKED pending the Student's Q-15 decision** — a
§18.2 forbidden-choice item that no implementer may fill by convenience. Comparator
generation refuses while it is unset.

**One answer proposes a governance action this stage does not own.** Q1's consolidated
change record for the **five** owed amendments across **three** units is put to you; the stage
records its own amendment either way. **Corrected 2026-08-23 from "six"** — see the
Assumptions entry.

**Two answers state obligations on other units.** Q6's availability matrix is
`features-and-splits`' artifact; Q3's allowlist covers `src/evaluation/` paths owned by
three different units. Both are stated, not claimed.

Carried to the gate, unchanged by these answers: `unit-of-work.md` § 6's stale untested
list and acceptance-row count, reported not edited; TA-36 `Pending`, never a result; four
requirements with no acceptance row (REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18);
BLK-07's authorization limb; rule numbering assumed to continue at R-54; G-09 unsigned.

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

### Re-confirmation, 2026-08-23 — after a redo jump taken to correct THIS unit

The iteration-2 adversarial pass returned **NOT-READY** on a defect the correction pass
itself introduced: a sweep that fixed the passages the first pass named and **missed other
restatements of the same facts** — the failure `project.md` § Way of Working records.
**Four corrections were applied to this file under the cleared receipt**, all with
superseded text preserved:

- the named accessors re-attributed from `governance-guards` to **`acquisition`**; that unit
  recorded no missing-contract finding of its own;
- the amendment total corrected — and then corrected again. That cycle set it to "six across
  three units" in four places, two of which the reviewer's line list had not named. **A
  later reading of `component-methods.md` § Depth corrected it to FIVE across three**
  (`acquisition` 3, `inventory-and-registry` 1, this unit 1), boundary contracts only — see
  the Assumptions entry;
- the Q2 summary row corrected: this unit **owns WS-09**, and on **TA-36 the story map
  contradicts itself** — § Cross-unit responsibilities reconciles it as
  **`features-and-splits` holding enforcement and the primary negative-path acceptance
  test** (`tests/test_feature_leakage_guards.py`), with this unit holding **data production
  and upstream evidence**. This stage does **not** reallocate;
- `business-logic-model.md`'s own Assumptions footer swept to match its corrected body.

**No question, option or answer letter changed.** Q1–Q9 stand as D, D, D, C, D, D, D, D, D.

### Re-confirmation, 2026-08-23 (second) — after a third stage-wide redo jump, and one applied correction

**No question, option or answer above changed.** One correction was applied to this unit's
artifacts under the cleared receipt, and it narrows a claim this file's Q1 argues.

`component-methods.md` § Depth specifies **cross-package boundary calls only** and names
**`functional-design` (3.1)** as where intra-package shapes are specified. Re-checked
against that policy:

- **`inventory-and-registry`'s `inventory.py` was never an amendment** — same package as
  `release.py`;
- **this unit's `src/external` claim is real but narrower** — `iri.py` and `gim.py` are
  importable from `scripts/` and `src/evaluation/`, and `spaceweather.py` feeds
  `src/features`, so **those are boundary calls**; "an entire package with no contract"
  overstated it.

**Corrected total: five across three units, not six.** The "third consecutive unit finds a
named module with no contract" framing was **partly a misreading of a stated depth policy**,
and the consolidated-change-record proposal now rests on the corrected footing. Q1's answer
(D) stands; the pattern it names is narrower than first argued.

### Re-confirmation, 2026-08-23 (third) — this file swept to match its own artifacts

**No question, option or answer changed.** The three design artifacts had already been
corrected to **five owed amendments across three units**, boundary contracts only, after
`component-methods.md` § Depth was read.

**This file had not been swept with them**, because its receipt was recorded before the
artifact correction was applied. An adversarial pass found **five** live restatements still
asserting "six across three" — Q1's option-D Impact text, the Assumptions entry, the Q1
summary row, the paragraph after the summary table, and one line inside the previous
re-confirmation note. All five are corrected here, with the superseded text preserved.

**The ordering that caused this is changed going forward:** every correction is applied to
the artifacts **and** this file before a confirmation receipt is recorded, so the receipt
seals a consistent set. Four cycles of this stage hit the same defect by the old ordering.

### Re-confirmation, 2026-08-23 (fifth) — after a fifth stage-wide redo jump

A redo jump aimed at correcting four stale cross-references in `target-standardization`'s
question file reset the receipt floor for every unit of this stage. **No question, option,
answer or amendment on this unit changed.** *(Answered `Looks correct`, 2026-08-23; that
receipt belongs to the previous attempt. The live answer tag for this section is the blank
one at its end.)*

### Re-confirmation, 2026-08-24 (sixth) — new stage attempt after the Inception close

**Why this is being re-asked.** Inception closed and Construction opened at
**2026-08-24T11:46:26Z**, starting a fresh `functional-design` attempt and resetting the
receipt floor for every unit.

**What changed upstream, and why it leaves this unit's answers untouched.** Two passes ran
on `foundation`, both in `governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md`:
the **amendment pass** (A **declined**; B and C **approved and executed**) and the **sites
9–11 addendum** (three superseded-status statements annotated in place inside `foundation`'s
own files).

| What the passes touched | Why this unit is unaffected |
|---|---|
| `component-methods.md` — `DeterminismRecord` **6 → 9** fields (B) | **Question 1's premise re-verified directly, not assumed:** `grep -n "src/external" component-methods.md` returns **no hits**. The file still carries `src/features`, `src/models` and `src/evaluation` boundary-call blocks and **no `src/external` block at all** — B added fields to a `foundation` entity and created no block |
| `services.md` **§ Run record and registry** (C) | This unit reads **§ The nine stage scripts**, for `04_build_external_products.py` |
| `unit-of-work.md` **§ 1** `Owns` (C) | This unit reads **§ 6** — the `Owns` list, the module-path allowlist, the 7 requirements |
| The sites 9–11 annotations | Inside `foundation`'s own artifacts; a superseded **status** annotated, no contract changed |
| Amendment **A** — **declined** | **No count moved.** This unit's 7 requirements and **4** with no acceptance row stand; it still owns WS-09 and TA-36 and supports WS-10, WS-11, TA-08, TA-12 |

**Its other upstream, also unchanged.** `inventory-and-registry` **R-44** (source inventory)
and **R-45** (registry), both consumed here, re-confirmed under this attempt with no rule
changed.

**What still stands.** Every answer, and everything carried to the gate: `unit-of-work.md`
**§ 6's stale text** reported and **not edited** (a five-item bold list including
FR-P1-04-17, and `Acceptance rows (1). WS-09`); **FR-P1-04-18 obligation 4 named
uncheckable** rather than given a check that would not test it; **BLK-07's authorization
limb** carried forward, with nothing here reading the locked month — this unit's IRI and GIM
products join **at evaluation time** onto the frozen comparison-wide mask; **G-09 unsigned**,
so nothing here authorises creating `src/external/spaceweather.py`, `src/external/iri.py`,
`src/external/gim.py` or `scripts/04_build_external_products.py`. The § Review verdict of
**READY** belongs to the previous attempt.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The receipt is recorded for `external-products` under this attempt and its three artifacts are re-saved. No answer, contract, count or scientific value changes.

- Request changes
   > **Impact**: No receipt is recorded and nothing is re-saved. Tell me what to change and I re-present first.

> **💡 Recommendation**: **Looks correct** — Question 1's premise was re-verified against the current `component-methods.md` rather than carried from the previous attempt, and every amended section is one this unit does not read.

*(Answered `Looks correct` earlier on 2026-08-24; that receipt was reset by the authorised redo jump below. The live answer tag for this section is the blank one at its end.)*


### Re-confirmation, 2026-08-24 (post-redo) — receipt floor reset by an authorised redo jump

**Why this is being re-asked, and it is not about this unit.** The project decision owner
authorised a **redo jump on `functional-design`** at **2026-08-24T14:57:07Z**, so that three
standing reviewer findings on **`models-and-baselines`** (unit 8) could be fixed and
re-reviewed — its adversarial budget had been exhausted at NOT-READY, and the write-freeze on a
terminal review receipt made a redo the only route to a fix. **A redo resets the receipt floor for
every unit of the stage**, which is the stated cost that was accepted when the redo was chosen.

**Nothing in `external-products` changed.** No question, option, answer, amendment, rule, entity or
workflow of this unit was touched after its earlier confirmation today. The only artifacts edited
after the redo are `models-and-baselines`'s; its three fixes are confined to its own
files and reach no contract this unit consumes.

**The redo bought what it was for.** `models-and-baselines` returned **READY** on the
second pass of the restored budget, after three further Major findings were fixed. Two residuals
ride that READY verdict and are carried to the stage gate rather than applied.

**Everything this unit carried to the gate still stands, unchanged**, as recorded above.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The receipt is recorded for `external-products` under the post-redo floor and its three artifacts are re-saved. No answer, rule, entity, count or scientific value changes.

- Request changes
   > **Impact**: No receipt is recorded and nothing is re-saved. Tell me what to change and I re-present first.

> **💡 Recommendation**: **Looks correct** — this unit is untouched; the reset is a mechanical consequence of a redo taken for a different unit, and that redo achieved what it was authorised for.

[Answer]: Looks correct
