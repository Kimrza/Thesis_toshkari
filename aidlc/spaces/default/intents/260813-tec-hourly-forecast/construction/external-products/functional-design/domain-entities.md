# Domain Entities — `external-products`

**Unit** `external-products` (Bolt 5) · **Kind** `library` · **Depends on**
`inventory-and-registry`

> **Re-established a sixth time 2026-08-24**, on a **new stage attempt** (Construction opened
> 2026-08-24T11:46:26Z, resetting every unit's receipt floor). **No content of this unit
> changed.** Both `foundation` passes of that day touch nothing this unit reads, and the
> absence of an `src/external` block in `component-methods.md` was re-verified directly.
> Amendment A was declined, so **no count moved**. **The READY verdict in § Review belongs
> to the previous attempt.**

> **Re-established a fifth time 2026-08-23**, after a redo aimed at a sibling unit's stale
> cross-references. **No content of this unit changed.**

The data shapes this unit owns: the three driver series with their grades and alignment
semantics, the IRI benchmark with its validation report, the GIM comparator with its
interpolation and overlap-audit records, and the import-allowlist declaration that keeps
the first two apart from the model path.

**Nothing here is a scientific value.** These shapes *carry* governed values — D-10.2's
alignment intervals, D-10.3's lags, D-21/22/23's F10.7 selection choices, the 2000 km IRI
ceiling — and record their grade, provenance and availability.

> **Corrected and re-established 2026-08-23**, after two adversarial passes and a redo jump.
> The two Criticals — TA-36's ownership and the amendment count — are fixed here and in the
> sibling artifacts, with every superseded reading preserved in place. **No answer to any
> question changed.**
>
> **A third redo followed**, aimed at a misread of `component-methods.md` § Depth, which
> specifies **cross-package boundary calls only** and names **this stage** as where
> intra-package shapes are specified. **Corrected total: five owed amendments across three
> units**, boundary contracts only.
>
> **A fourth redo** then swept this unit's **question file**, which still asserted "six
> across three" in five live places. **No content of this artifact changed.**

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 6 — the `Owns` list, the module-path allowlist, the 7 requirements, the implementation notes.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2 plus § Per-unit coverage summary. **Derived by reading the rows:** 7 requirements, **4** with no acceptance row; **owns** WS-09; on **TA-36** this artifact contradicts itself and § Cross-unit responsibilities is the reconciling statement — see W-2a / § TA-36. **Supports** WS-10, WS-11, TA-08, TA-12.
- `../../../inception/requirements-analysis/requirements.md` — REQ-ENG-9; FR-P1-04-3, -4, -9, -15, -17, -18.
- `../../../inception/application-design/components.md` § `src/external`.
- `../../../inception/application-design/component-methods.md` — **which carries no `src/external` block**.
- `../../../inception/application-design/services.md` § The nine stage scripts.
- `../inventory-and-registry/functional-design/domain-entities.md` — `SourceInventoryEntry`, `Station`, `DriverSeriesInventory`'s upstream.
- `evidence/DECISIONS.md` — **D-5**, **D-10.1**, **D-10.2**, **D-10.3**, **D-11**, **D-13**, **D-21/22/23**.
- Workspace inspection, 2026-08-23: `scripts/audit_ec1_drivers.py` line 184; `evidence/audit_ec1_2026-08-15/kyoto_dst/dst_provisional_202212.html`; the absence of `src/` and `configs/`.
- `functional-design-questions.md` (**Q1 through Q9**), `business-logic-model.md`, `business-rules.md`.

---

## Entity map

```mermaid
graph TD
  DS["DriverSeries<br/>(grade + alignment + lag)"]
  GA["GradeEligibility<br/>(provisional = restricted use)"]
  AM["AvailabilityRow<br/>(obs; publication OR D-25 convention;<br/>grade; safe lag)"]
  BM["IRIBenchmark<br/>(B-01, generated not trained)"]
  VR["IRIValidationReport<br/>(7 areas + predeclared tolerance)"]
  GC["GIMComparator<br/>(C-01, generated not trained)"]
  IR["GIMInterpolationRecord<br/>(rule UNSET - blocked)"]
  OF["gim_network_overlap_flag"]
  AL["ImportAllowlist<br/>(module paths)"]
  MF["DriverManifest<br/>(missing months NAMED)"]

  GA --> DS
  DS --> AM
  DS --> MF
  AM --> BM
  VR -->|"must pass BEFORE"| BM
  IR -->|"hand-check BEFORE"| GC
  GC --> OF
  AL -.->|"transitive reachability"| BM
  AL -.->|"transitive reachability"| GC
  GA -.->|"provisional blocks"| RC["regime count<br/>(D-13: GFZ Kp/Hp60 only)"]
```

Text fallback: grade eligibility gates each driver series, which produces availability rows
and a manifest naming any missing months. The IRI benchmark cannot be generated until its
validation report passes, and consumes the same availability rows the ML features use. The
GIM comparator cannot be generated until the interpolation hand-check is recorded — and its
interpolation rule is currently unset and blocked. The import allowlist constrains, by
transitive reachability, which modules may reach the benchmark and comparator modules. A
provisional grade blocks the regime count, which D-13 requires from GFZ Kp/Hp60.

---

## 1. `DriverSeries` — grade, alignment, lag

Four series, frozen by contract: **Kp/ap3** and **Hp60/ap60** from GFZ, **hourly Dst** from
Kyoto WDC, **observed (not 1-AU-adjusted) F10.7** from Canada's Solar Radio Monitoring
Program. **SSN is absent**, confirmed by `grep`.

| Attribute | Meaning |
|---|---|
| `series_id` | Which series |
| `grade` | Release status — real-time / provisional / final. **One recorded grade per series for calendar 2022; never mixed** (D-10.1) |
| `alignment` | How a **present** value maps onto the hourly grid (§ 2) |
| `safe_lag` | The availability lag applied before a forecast origin (D-10.3) |
| `values` | Time-indexed only — **one value per epoch, identical across all three cells** |
| `carry_forward_h` / excluded rows | A missing value carries forward **at most 3 hours** (bound read from `configs/features.yaml`); beyond it the row is **excluded**, recorded machine-readably — R-57a, FR-P1-04-3, TC-09 *(field added 2026-08-26, finding 10)* |

**Time-indexed only, and the consequence is stated** (FR-P1-04-4, TC-12): a join must never
imply a per-cell measurement, and **a station performance difference must never be
attributed to local forcing the dataset does not contain.**

**Lags, applied here and decided elsewhere** (D-10.3): Kp/ap3 **≥ 3 h**; Hp60/ap60 **≥ 1 h**;
F10.7 at the **previous-day observed** value with a **trailing** 81-day mean ending at the
safe-lagged day.

**F10.7's three frozen selection choices** — D-21 (daily **median**), D-22 (duplicate UT
records take the **mean**, with a QC flag and provider-defined correction semantics taking
precedence), D-23 (the four high-spread days flagged and retained with the median as
representative).

**No backfill from future final or definitive archived values** — NFR-LEAK-01 governs
*timing* only, and a series can satisfy its declared lag while being built from reanalysed
values, invisible to every existing check.

## 2. Alignment — how a present value maps onto the grid

| Series | Rule (D-10.2) |
|---|---|
| Kp / ap3 | Repeated **only within its own defined 3-hour interval** |
| Dst | Aligned to **its own hourly averaging interval** — *"not shifted to a neighbouring hour for convenience"* |
| F10.7 | Daily |
| **All** | **No driver is interpolated, at any stage** |

**Distinct from carry-forward, and the requirement says so.** FR-P1-04-3's ≤3 h
carry-forward (then exclude the row) governs a **missing** value; alignment governs a
**present** one. **The two are tested separately**, so neither passes on the other's
evidence.

**TA-36 is this contract's approved negative-path row** — status **`Pending`: the row exists,
and it is not implemented, not executed, not passing.** Its three limbs: Kp repeated outside
its interval fails; Dst shifted to a neighbouring hour fails; a grep-level check finds no
interpolation call.

> **The PRIMARY test is not this unit's.** The story map's § Cross-unit responsibilities
> reconciliation sites TA-36's primary negative-path test at the feature-building enforcement
> boundary, in **`tests/test_feature_leakage_guards.py`**, owned by **`features-and-splits`**.
> This unit holds **data production** and **upstream evidence**, and its own contract test is
> *"documented separately and **not** replacing the primary rejection test."* See
> `business-logic-model.md` § W-2a.

## 3. `GradeEligibility` — new, and the entity that keeps Dst's three restrictions apart

The grade a series carries, and what that grade makes it **eligible for**.

| Grade | Fixture characterisation | Modelling input | Frozen tolerance | G-05 regime count |
|---|---|---|---|---|
| Final | ✅ | per restriction 1 | ✅ | ✅ |
| Provisional | ✅ **permitted** (D-11) | ❌ | ❌ | ❌ **(D-13)** |
| Mixed within a series | ❌ **fails at construction** (D-10.1) | ❌ | ❌ | ❌ |

**Why eligibility is a property of the data rather than a rule about it.** A rule that
depends on three units remembering is the shape D-15 warns about for the restricted root.
Making the consumer read the grade is the only form that survives a consumer nobody has
written yet — and it makes the **permitted** fixture-characterisation use explicitly
distinguishable from the three that are not.

**The live trap.** `evidence/audit_ec1_2026-08-15/kyoto_dst/dst_provisional_202212.html`
exists in the workspace today; **D-11** used provisional Dst to characterise the fixture
window, which is permitted; and **D-13** requires the December regime count to come from
**GFZ Kp/Hp60 at a recorded release grade**, explicitly barring any provisional-Dst-derived
figure.

**Dst is diagnostic/hindcast-only** and never a confirmatory ML feature (TC-11) — enforced
downstream by `features-and-splits`, stated here. `governance-guards` **R-26** separately
names Dst as the driver class excluded from the December-hit definition, a fourth
consequence of the same fact and not restated as a rule here.

## 4. `AvailabilityRow` — the same matrix the benchmark must appear in

Per driver, per epoch: **observation timestamp, publication timestamp OR — where the provider
supplies none — the approved conservative convention (for F10.7: D-25's 00:00 UTC on day D+1,
never same-day) plus the documented absence and an unverified-latency statement**
(`CR-2026-08-22-EV-12`; field corrected 2026-08-26, finding 2)**, release status,
safe lag.**

**FR-P1-04-15 requires the IRI benchmark's OWN drivers to appear as rows in this same
frozen matrix** — the one used for ML features. *A benchmark fed better-timed drivers than
the model gets is not a benchmark*, and this is the limb that makes the comparison's fairness
checkable rather than asserted.

> **The matrix is `features-and-splits`' artifact.** This unit states the obligation and
> **does not own the row**.

## 5. `IRIBenchmark` and `IRIValidationReport`

**`IRIBenchmark`** is **B-01**, represented in the model/config inventory and labelled
**generated, not trained** — never fitted.

**`IRIValidationReport` must pass before generation**, and FR-P1-04-15 enumerates its
content:

| # | Content area |
|---|---|
| 1 | The pinned package/build with its **exact version or commit** |
| 2 | All model switches and the topside option |
| 3 | **The altitude ceiling stated explicitly as 2000 km** |
| 4 | Units and output extraction |
| 5 | The coordinate, time, solar and geomagnetic driver inputs, **with confirmation that no driver is future-centered or unavailable at target time** |
| 6 | **Five to ten samples** spanning sites, day and night, quiet and disturbed, validated against the **official IRI interface** |
| 7 | The tolerance, **predeclared before the comparison runs** |

**Each area is asserted field by field**, so an incomplete report **fails rather than
passing on presence** — the same defect class as a short protected-set list passing a
membership check.

**Area 7 carries a timestamp preceding the comparison**, and generation refuses if the
ordering is violated. *"A passing report exists"* is satisfiable by a report whose tolerance
was chosen **after** the comparison ran, which is the failure the predeclared clause exists
to prevent and which no presence check can see.

**Also recorded:** the **26,000-call workload is timed** and its measured runtime recorded;
the `iri2016` Fortran build **re-establishes from pins on a cold session** (TC-04).

> **FR-P1-04-15 has NO acceptance row.** Designing this is not testing it.

## 6. `GIMComparator`, `GIMInterpolationRecord`, `gim_network_overlap_flag`

**`GIMComparator`** is **C-01**, in the model/config inventory and labelled **generated, not
trained**.

**`GIMInterpolationRecord`** carries the interpolation rule, the hand-checked sample **with
its worked arithmetic**, and the map-to-map statement.

> ## ⚠ THE INTERPOLATION RULE IS UNSET, AND GENERATION REFUSES WHILE IT IS
>
> **Bilinear in space, linear in time, with a longitude-rotation correction** is a §18.2
> **Student-owned forbidden choice** (**Q-15**). TE §18.2: *"No implementer or coding agent
> may fill such a value by convenience."*
>
> Specifying the mechanism while leaving the **value** implicitly fillable is exactly what
> that prohibits. **Comparator generation refuses while the rule is unset** — the zero-TBD
> preflight's shape.

**Ordering, enforced not asserted:** *"One sample interpolation must be hand-checked against
the code"*, and **EV-11 places that hand-calculation BEFORE comparator generation.** The
hand-check's timestamp is asserted to precede generation; **a comparator generated before
the hand-check fails rather than being accepted retrospectively.**

**The map-to-map statement is emitted by the reporting path itself**, because §6.10 requires
it *"wherever the comparison is reported"* — a rule about **every** report, including ones
nobody has written yet. Its text: the Phase 1 GIM comparison *"is explicitly a
map-product-to-map-product comparison … cannot validate receiver-level station VTEC or serve
as an independent target check."*

**`gim_network_overlap_flag`** — the audit **is present and its result disclosed**, **no
independence claim precedes the audit**, and the **flag value appears wherever GIM is
compared** (FR-P1-04-9, TC-08).

**The comparator is never tuned and then claimed independent** — carried as a
reporting-discipline rule with **no code check**, and named uncheckable rather than given a
check that would not test it. No injected value proves a negation of that kind.

> **FR-P1-04-18 has NO acceptance row**, and its interpolation limb is blocked on Q-15.

## 7. `ImportAllowlist` — module paths, checked transitively

The permitted importers of `iri` and `gim`: **`scripts/04_build_external_products.py`** and
**modules under `src/evaluation/`**. An import from `src/data`, `src/features`, `src/models`,
`src/gnss`, a training script or a notebook violates it **identically**.

**`src/evaluation/` is owned by three units** — `evaluation-and-comparison` (`masks.py`,
`metrics.py`), `statistical-inference` (`bootstrap.py`), `regimes-diagnostics-reporting`
(`regimes.py`, `diagnostics.py`, `plots.py`). The allowlist grants an authorized **path**,
never a whole unit's unrelated code.

**Checked by transitive reachability, not direct imports.** `project.md` § Forbidden states
the constraint as *"directly or transitively"*; a direct-import check does not implement the
rule its own citation states, because a helper importing a shim that imports `gim` satisfies
it and violates the rule.

**The static check is AUTHORITATIVE for this rule**, unlike `governance-guards` R-24's
subordinate scan — a module graph is a property of the **source tree**, where a loaded module
is a property of a **running process**. The asymmetry is stated so it does not read as an
oversight.

**`spaceweather.py` is deliberately outside the restriction:** drivers **are** model inputs,
subject to the availability lags.

## 8. `DriverManifest` — completeness recorded, integrity terminal

| Field | Tier | Behaviour |
|---|---|---|
| `missing_months` | **Completeness shortfall** | **Names which months**, machine-readable, **non-fatal** |
| hash mismatch | **Integrity violation** | **Terminates** the run, naming the file and the violated expectation |

**The workspace fact this closes:** `scripts/audit_ec1_drivers.py` **line 184 returns `0`
regardless of missing months** (REQ-ENG-9).

**Why not simply return non-zero on missing months.** That collapses the two-tier posture: a
month absent from the provider is a fact to record; a hash that does not match invalidates
everything downstream. Making an ordinary partial retrieval abort the run is how a guard
gets worked around.

**Why the field names the months rather than counting them.** A count says something is
wrong; the list says what to do — and `inventory-and-registry` R-51 already forbids *"an
unattributed number"* in the G-P1A decision this feeds.

> **REQ-ENG-9 has NO acceptance row.** Both injections must be tested, because they assert
> **opposite** outcomes.

## 9. `IntegrityError` subclasses raised here

Deriving from `foundation`'s base — **`IntegrityError`, imported from `src/data/config.py`**,
under R-01's *"any future integrity-related exception"* clause for the unit-local names — each
naming the affected resource and the violated expectation. *(Base named explicitly 2026-08-26,
matching every prior unit; the **declaration site** for the unit-local exceptions is the same
OPEN item recorded at `foundation`: a cross-unit agreement into `config.py`, or the
`src/data/exceptions.py` §12 amendment.)*

| Exception | Raised when |
|---|---|
| `DriverError` *(scope corrected 2026-08-26, finding 3: the two alignment conditions previously claimed here are raised as **`AlignmentError`** — one of the fourteen in the shared base — by the approved `build_features` contract at `component-methods.md`, not by this unit; and "an interpolation call is found" is a **static grep check** per this unit's own R-58/W-5 limb 3, not a runtime raise)* | A series mixes release grades; a grade renders the series ineligible for the requested use; a hash mismatch is detected. *(Three conditions removed from THIS cell 2026-08-26, finding 9 — the 2026-08-26 note beside it had retracted them while the cell 3.5 implements from still listed them: Kp repeated outside its interval and Dst shifted to a neighbouring hour raise the approved **`AlignmentError`** at `build_features`, not here; "an interpolation call is found" is a **static grep check**, not a runtime raise.)* |
| `BenchmarkError` | Generation is attempted without a passing validation report; the report is missing any of its seven content areas; the tolerance timestamp does not precede the comparison |
| `ComparatorError` | Generation is attempted while the interpolation rule is **unset**; the hand-check timestamp does not precede generation; the overlap audit is absent where an independence claim is made |
| `ImportBoundaryError` | A module outside the allowlist can reach `iri` or `gim`, directly or transitively |

Catching `foundation`'s base is what lets the stage entry contract write the `aborted`
registry row for any of them.

---

## Requirement coverage

Acceptance derived from story-map Table 1; owners from Table 2's `primary` cell. **Where
`unit-of-work.md` § 6 disagrees, the story map governs** — see `business-logic-model.md`
§ W-2.

| Requirement | Entities | Tested by (Table 1) | Row primary owner |
|---|---|---|---|
| **REQ-ENG-9** | `DriverManifest` | ⚠ **NO ROW** | — |
| FR-P1-04-3 | `DriverSeries` (carry-forward, tested separately) | WS-11 | `features-and-splits` |
| **FR-P1-04-4** | `DriverSeries` | ⚠ **NO ROW** | — |
| FR-P1-04-9 | `GIMComparator`, `gim_network_overlap_flag`, `IRIBenchmark` | WS-09, TA-12 | **`external-products`** (WS-09); `models-and-baselines` (TA-12) |
| **FR-P1-04-15** | `IRIValidationReport`, `AvailabilityRow` | ⚠ **NO ROW** | — |
| FR-P1-04-17 | § 2 Alignment | **TA-36** — ⚠ **`Pending`**: row exists, **not implemented, not executed, not passing** | **`features-and-splits`** (primary test); **`external-products`** (data production, upstream evidence) — W-2a |
| **FR-P1-04-18** | `GIMInterpolationRecord` | ⚠ **NO ROW**, and its interpolation limb is **blocked on Q-15** | — |

**7 requirements, 4 without an acceptance row.** **Owns WS-09.** On **TA-36** this unit holds
**data production** and **upstream evidence**; `features-and-splits` holds **enforcement** and
the **primary acceptance test** (`tests/test_feature_leakage_guards.py`) — see
`business-logic-model.md` § W-2a. **Supports** WS-10, WS-11, TA-08, TA-12.

> ## THE TWO UPSTREAM ARTIFACTS DISAGREED — RESOLVED; § 6 WAS SWEPT 2026-08-24
>
> *(Heading and standing corrected 2026-08-26 on adversarial finding 8, Critical: this box still
> asserted the disagreement as live. `unit-of-work.md` § 6 now reads **4** untested and
> `Acceptance rows (2). WS-09, TA-36 (Pending …)`, present since commit `45796f5`. The text below
> is the dated record of the conflict as it stood; **nothing is currently reported to the gate
> from this box**.)*
>
> `unit-of-work.md` § 6 says **5 untested** (its bold list includes FR-P1-04-17) and
> **`Acceptance rows (1). WS-09`**. The story map says **4 untested** and **WS-09 and
> TA-36**.
>
> **The story map governs**: TA-36 was approved **2026-08-22** under Vision §15.2
> (`CR-2026-08-22-LEAKAGE-TA`), and the story map records the sweep — *"untested 40 → 36."*
> § 6 was not swept with it.
>
> **Both stale statements are reported at the gate, not edited**, per
> `CHANGE_RECORD_PROCEDURE.md`. The `Acceptance rows (1)` line **carries no numeral tied to
> the change**, which is exactly the stale-claim shape `project.md` § Way of Working records
> a numeral-keyed sweep as being blind to.
>
> **TA-36 is `Pending` and is never cited as a result.** A row that exists but has never run
> is the shape of the defect that let FR-P1-02-8 look covered behind a withdrawn `TA-29` for
> five revisions, past four governance boards.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence, so `business-rules.md` opens at **R-54**. If per-unit numbering was intended, say so at the gate.
- **[assumption]** The **story map governs** where it and `unit-of-work.md` § 6 disagree. Neither is edited by this stage.
- **[assumption]** The availability matrix in § 4 is **`features-and-splits`' artifact**; the obligation is stated, the row not owned.
- **[assumption]** `audit_ec1_drivers.py` migrates here; target shape designed, migration commit not made.
- **[assumption]** `frontend-components.md` is not produced — `kind: library`.
- **Open — `src/external` has no contract block** for any of its three modules; § 1–§ 8's shapes are **one amendment owed**, not approved.
- **Open — FIVE owed amendments across three units** (`acquisition` 3, `inventory-and-registry` 1, this unit 1), **boundary contracts only**. `business-logic-model.md` § W-1 **proposes** one consolidated change record. **Corrected twice on 2026-08-23**: from "four across four" with `open_d9_input` misattributed; then from "six across three", after `component-methods.md` § Depth was found to specify **cross-package boundary calls only** and to name **this stage** as where intra-package shapes are specified.
- **Open — FR-P1-04-18's interpolation rule is UNSET** (§ 6), a §18.2 Student-owned forbidden choice. Comparator generation refuses while it stands.
- **Open — four requirements with no acceptance row**: REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18.
- **Open — TA-36 is `Pending`**: approved, never run.
- **Closed 2026-08-26 (finding 8): the § 6 conflict no longer exists — the file was swept 2026-08-24; kept as the dated record.** *(Superseded bullet:)*  — `unit-of-work.md` § 6 carries stale text**, reported not edited.
- **Open — FR-P1-04-18 obligation 4 has no code check**, and is named uncheckable rather than given one that would not test it.
- **G-09 is not signed.** No entity here authorises creating `src/external/spaceweather.py`, `src/external/iri.py`, `src/external/gim.py` or `scripts/04_build_external_products.py`.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

---

> **Re-saved 2026-08-24 under the post-redo receipt floor.** The project decision owner
> authorised a redo jump on `functional-design` at 2026-08-24T14:57:07Z so that three
> standing reviewer findings on `models-and-baselines` could be fixed and re-reviewed;
> a redo resets the receipt floor for **every** unit of the stage. **No content of this unit
> changed** — not a question, answer, amendment, rule, entity, workflow, count or scientific
> value. The only artifacts edited after the redo were `models-and-baselines`'s, whose
> three fixes are confined to its own files. That unit returned **READY** on the second pass of
> the restored budget, which is what the redo was authorised for. The two residuals riding that
> verdict — R-96's `PartitionError` mechanism and R-95's field label — are carried to the stage
> gate rather than applied, per the rule that a suggestion riding a READY verdict is gate input.

---

> **Re-saved 2026-08-26 under the thirteenth-redo receipt, after the terminal-pass remediation.**
> In this file: the upstream-disagreement box re-headed **RESOLVED** (the § 6 conflict no longer
> exists); the `DriverError` **Raised-when cell purged** of the three retracted conditions —
> Kp/Dst misalignment raise the approved **`AlignmentError`**, interpolation is a static grep;
> `DriverSeries` gained the **carry-forward/exclusion field** (R-57a); the availability-row
> field and mermaid node carry the D-25 branch. Figures unchanged (7/4/2).
> **G-09 remains unsigned.**

---

> **Re-saved unchanged 2026-08-26 under the fourteenth-redo receipt** (the redo finished the
> gate-record sweep in the sibling files; no entity here changed). **G-09 remains unsigned.**

---

> **Re-saved unchanged 2026-08-26 under the fourteenth-redo re-confirmation receipt** (finding 17's
> mojibake repair touched the question file only; no entity here changed). **G-09 remains unsigned.**
