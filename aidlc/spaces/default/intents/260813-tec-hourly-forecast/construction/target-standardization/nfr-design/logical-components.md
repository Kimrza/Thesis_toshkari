# Logical Components — `target-standardization`

**Unit** `target-standardization` (Bolt 6) · **Kind** `library` · **Stage** `nfr-design`

> ## ⚠ NONE OF THESE COMPONENTS EXISTS, AND ONE OF THEM CANNOT RUN AT ALL
>
> `src/data/prepared.py`, `scripts/02_standardize_prepared_target.py`,
> `tests/test_prepared_target_schema.py` and `configs/` are all absent. `scripts/` holds
> `audit_ec1_drivers.py` and `merge_coverage_year.py` only.
>
> **T-1 is blocked by design, not by absence.** Under Q2 = A, while `configs/data.yaml`'s
> **QC operation list is `TBD — freeze gate`**, standardization **raises and stops** — **no
> target is produced**. That is this unit's stated posture made operative: it would rather
> produce nothing than produce a target whose definition is uncertain. **Production of a target waits
> on a supervisor freeze.**
>
> **This is a logical decomposition, not an infrastructure deployment.** No services, no
> processes, no network boundaries. `target-standardization` is a **library plus one stage
> script plus its tests**, and its "failure domains" are the blast radii of function calls in
> one process.
>
> **`FR-P1-03-5` carries no acceptance row** — WS-05 is deferred to G-P3A. **BLK-05's
> implementation and execution limbs are open.** The **`02` ordinal collision** is a recorded
> §12 defect; **no `02a`/`02b` convention** is invented. **G-09 is signed (D-31) with
> preconditions UNMET**; stage 3.1 remains **FAIL**; the Python interpreter present is
> **3.14.7, off the governed 3.11 pin**.

## Sources

- `security-design.md` — **SD-T-00** … **SD-T-06**, this stage's sibling artifact. The boundaries below are where those decisions land, and § SD-T-00 carries the workspace evidence and both discrepancies.
- `../nfr-requirements/security-requirements.md` — **SEC-T-01** … **SEC-T-04** as the requirement set; **one status claim superseded**, per § SD-T-00.
- `../nfr-requirements/tech-stack-decisions.md` — **TS-T-01** … **TS-T-05**.
- `../functional-design/business-logic-model.md` — **W-1** … **W-9**; `../functional-design/business-rules.md` — **R-64** … **R-73**.
- **`performance-requirements.md`, `scalability-requirements.md` and `reliability-requirements.md` are absent by `produces_kinds` design** for a `library` unit; assessed in `security-design.md` § Scope note.
- `../../foundation/nfr-design/logical-components.md`, `../../governance-guards/nfr-design/logical-components.md`, `../../inventory-and-registry/nfr-design/logical-components.md`, `../../external-products/nfr-design/logical-components.md` — the four sibling decompositions and their stated criteria.
- **The workspace, read 2026-09-03** — `scripts/` (two scripts), `src/data/config.py`, `tests/` (six modules).
- `../../../inception/application-design/components.md`, `component-methods.md`, `services.md`.
- `../../../inception/requirements-analysis/requirements.md` — **FR-P1-03-1** … **-5**; **NFR-TDEF-01**, **NFR-DQ-01**, **NFR-LEAK-01**, **NFR-PHASE-01**.
- `nfr-design-questions.md` — **Q4 = A**, and the receipted Consolidated Summary Confirmation.

---

## The boundary criterion (Q4 = A)

**The boundary is drawn on what each component makes true about the target.**

> **This unit is not a guard and keeps nothing out. Everything it does establishes some claim
> about the target — what its values ARE, what shape each row HAS, and what the number MEANS
> when someone reports it.**

- **T-1** establishes the target's **values**.
- **T-2** establishes each row's **shape**.
- **T-3** establishes what the number **means**.

**The three fail in three different directions, and that is the point.** A wrong **value** is
wrong science. A wrong **shape** breaks a consumer loudly, at the first read. A wrong
**meaning** is a **correct number reported as something it is not** — it passes every value
check and every schema check, and it is wrong only in the sentence a person writes about it.
**T-3 is the only one of the three whose failure is silent all the way to the thesis**, which
is precisely why Vision §6.6 makes its disclosure mandatory and why SD-T-02 carries it as
data rather than documentation.

**Consistency with the four siblings, without copying any of them.** `foundation` drew on
**failure consequence**; `governance-guards` on **enforcement timing**;
`inventory-and-registry` on **how the failure reaches a human**; `external-products` on **what
the component keeps out**. Each picked the axis its own material varies on. **This unit has no
guard to time and keeps nothing out** — it varies on what it *establishes*, so that is the
axis. Same discipline, a fifth axis.

**Why not "by workflow grouping"** (W-1/W-2 | W-3/W-5 | W-6/W-7). Traceable straight back to
`functional-design` and easy to verify. It separates **W-5's labelling** from **W-3's field
contract** despite both being properties of the same row, and pairs **W-6** (a script-ordinal
defect) with **W-7** (the uncertainty budget) on adjacency alone.

**Why not "by artifact produced"** (the standardized target / the data-quality block / the
uncertainty budget). It maps onto what a reader can open. It puts the label and the caveat
inside "the standardized target" with **nothing marking that they are the one part whose
failure is silent**, and W-7 already records that the uncertainty budget is **not wholly this
unit's**.

**Why not "by requirement"** (FR-P1-03-1 … -5). Direct traceability, and the coverage table
writes itself. It splits nothing by behaviour: **FR-P1-03-3 and -4 both land on the same
row-level contract** yet sit in separate boxes, while -1's diff and -5's field contract share
a box only through ID adjacency.

**Two things cross all three components and are placed explicitly rather than left implicit:**

- **W-6's `02` ordinal collision and its one-per-run assertion** is a property of **the run**,
  not of any one component. Stated once in **T-1**, whose stage script hosts it, and **named
  as crossing** in T-2 and T-3 rather than duplicated.
- **W-9's build boundary** — what Bolt 6 may build before G-09 — binds all three identically
  and is stated once in § Failure domains.

---

## Component inventory

| # | Component | Contents | What it establishes | How its failure surfaces | State on disk |
|---|---|---|---|---|---|
| **T-1** | **Values** | the four transformations — UTC normalization, D-1's half-open floor cell rule, D-16's median aggregation, and the `TBD` QC list; the **value-level** closed-set diff (W-1, W-2) | what the target's numbers **are** | **Wrong science.** A number that is simply not what the provider bytes plus the documented transformations produce | **Unbuilt, and blocked** |
| **T-2** | **Shape** | D-17's sixteen fields and the schema test; the three definition IDs; the asserted excluded set; D-19's thresholds with their basis (W-3) | what each row **has** | **Loudly.** A consumer breaks at the first read — a missing field, an unstamped ID | **Unbuilt** |
| **T-3** | **Meaning** | the label; the lineage caveat as a **column**; the spatial-representativeness mismatch; the no-equivalence rule (W-5) | what the number **means** when reported | **Silently, all the way to the thesis.** A correct number reported as something it is not | **Unbuilt** |

### T-1 — Values (establishes what the numbers are)

**Blast radius: every scientific claim built on the target.** T-1 is the only component that
changes numbers. Its defects are not detectable by any downstream schema or contract check —
a wrongly aggregated hour is a well-formed row.

> **⚠ T-1 CANNOT RUN TODAY, AND THAT IS THE DESIGN RATHER THAN AN ACCIDENT.** The closed set
> has four members and the fourth — **"documented QC"** — is `TBD — freeze gate`. Under
> Q2 = A, standardization **raises and stops** while it is unset, naming
> `configs/data.yaml`'s `qc_operations` field and the expectation that it be **frozen under a
> D-number** — not merely non-empty, since a list filled by convenience would satisfy that and
> is exactly what §18.2 forbids. **No target is produced.**
>
> **The rule's SCOPE is narrower than "the whole unit waits"** *(corrected 2026-09-03 on the
> reviewer's finding 1, Major)*. It binds **the run that produces a standardized target**. It
> does **not** bind T-2's schema contract, T-3's caveat column, or any fixture exercise of
> either — all three are properties of the writer, testable with no QC list at all. **The QC
> list bears on which value transformations are permitted, and on nothing else.** A
> fail-closed rule that halted work it has no bearing on would be a scheduling accident
> wearing a governance costume.
>
> **And §18.3 does not supply the rule.** As `team.md` quotes it, §18.3 governs
> **implementation** — *"must not implement an affected component while its P0 decision is
> unresolved"* — not the runtime behaviour of a written module. **A third option was never
> weighed and is routed to the gate**: refuse to **RELEASE** rather than to **RUN** — produce
> the artifact, refuse to hash, register or promote it, mark it non-governed.
>
> **Why fail-closed here when `external-products` chose skip-not-pass**, stated because the
> two look inconsistent and are not: that unit's unverified check guards **a module that does
> not exist**, so nothing can be wrongly consumed meanwhile. T-1's would guard **an artifact
> that exists on disk and gets read**. A skipped check is a fact about a run; a target file is
> a fact about the project, and **a gate report does not travel with a file**.

**The diff is value-level, not schema-level.** FR-P1-03-1's criterion is about **what changed
between the provider bytes and the standardized product**. A check comparing column names and
dtypes does not meet it — and it is the cheaper check, so it looks like progress.

**The floating-point tolerance is a declared value and is not set here**; it belongs with the
fixture manifest's permitted tolerances (TE §15.2). A tolerance taken from a library default
is a scientific value filled by convenience.

**W-6's one-`02`-per-run assertion lives here**, because this component's stage script is the
`02` in question: the clean-run contract asserts **exactly one recorded entry whose basename
matches `02_*`** in the run manifest. It is a property of **the run**, and it is **named as
crossing** T-2 and T-3 rather than restated there. **Three parties, named rather than left
implicit** *(assigned 2026-09-03 on the reviewer's Minor 3)*: `foundation` supplies the
manifest field, **`fixtures-and-reproducibility` authors the assertion** in
`tests/test_clean_run.py` — TE §13.2 makes the ordered clean-run sequence that unit's
artifact, and R-73 places the assertion there in terms — and **this unit specifies what it
must assert without authoring it.**

### T-2 — Shape (establishes what each row has)

**Blast radius: the first consumer, and no further.** T-2's failures are the ones this unit
can afford — a missing field or an unstamped ID **breaks a read**, immediately and visibly. It
is the only component of the three whose defects announce themselves.

**Exactly sixteen fields** (D-17), **not fifteen, not seventeen**, checked by a **schema test
against the contract** rather than by review. **Three definition IDs** — `phase_id`,
`source_id`, `target_definition_id` — on every dataset, prediction, mask and comparison. **The
excluded set is asserted, never substituted**: a run that finds a different excluded set than
the one declared **fails** rather than proceeding on what it found — the same shape as
`inventory-and-registry`'s declared-versus-required scope check, and for the same reason.
**D-19's thresholds carry their basis**, frozen from **January–November** distributions with
**December excluded by construction**; the trigger is December being **seen**, not the lock
being opened.

> **⚠ Where the conformance check reads the frozen field set from is OPEN.** W-3 asserts
> config-equals-D-17, which raises `governance-guards` **R-20**'s question verbatim: *"it must
> assert against the **authority**, not merely against the config — otherwise config and
> manifest can agree with each other while both drift."* **No third option is invented**;
> carried to the gate.

**No schema library is added.** Sixteen fields against a contract already written down do not
justify a new dependency, a §10.1 register entry and a version pinned on two platforms. If 3.5
finds otherwise, **that returns to `nfr-requirements`** rather than being settled there.

### T-3 — Meaning (establishes what the number means when reported)

**Blast radius: the thesis.** T-3 is the component whose failure nobody catches. A target
labelled as something it is not produces a **correct number**, passes **every** value check
T-1 makes and **every** schema check T-2 makes, and is wrong only in the sentence a person
writes about it. That asymmetry is the whole reason for this decomposition.

**The caveat is a COLUMN, not Parquet metadata** (Q1 = A) — **and what that buys is
detectability, not survival** *(corrected 2026-09-03 on the reviewer's finding 2, Major; the
superseded text argued as though the column survived operations metadata does not)*.
TS-T-03's criterion is that the carrier *"survive the pipeline's actual operations, not merely
a direct read-back."* **A column is dropped by a column-subset or `groupby` rebuild exactly as
metadata is; neither survives by itself.** What the column buys is that **its loss is visible
to a schema check**, where lost key-value metadata leaves nothing in the frame recording it
was ever there.

**So the design adds a preservation obligation on this unit's own write path** — the only
part of survival within this unit's power: every artifact it writes carries the column, on
**every** write and not the first only; a **round-trip test against a fixture** asserts the
column survives the operations **this unit** performs; and **beyond this unit's write path
survival is neither guaranteed nor claimed**. **Cost: one repeated identical string per row**,
near-free on disk under dictionary encoding, genuinely redundant in memory. **If a metadata
mirror is ever added, the column wins by rule.**

**What it carries.** That the Phase 1 target is **location-sampled gridded VTEC** (Madrigal
cell), **never** receiver-specific station-observed VTEC, with its own distinct
`target_definition_id`; and that part of any measured IRI or GIM difference is a **geometry
and sampling artefact rather than skill**. **No claim of numerical equivalence** between the
Phase 1 and Phase 2 targets is permitted, and Phase 2 must be stated at abstract level as a
**fixed-protocol replication on a new target lineage, not a second statistically independent
blind test**.

> **⚠ THIS COMPONENT IS ONE HALF OF A CROSS-UNIT CONTRACT.** T-3 can make the caveat **exist
> and travel**. It **cannot** make a consumer **fail** for omitting it — that check lives in
> the consuming unit's reporting path. Choosing a column makes the other half *buildable*; it
> does not build it. **The contract is not declared satisfied from one side.**

---

## Failure domains and blast radius

| Component | Does its failure announce itself? | Blast radius | Contained by |
|---|---|---|---|
| **T-1** | **No** — a wrongly aggregated hour is a well-formed row | **Every scientific claim built on the target** | The value-level closed-set diff — **which cannot run while the QC list is `TBD`**, and the fail-closed rule that stops the unit rather than shipping past it |
| **T-2** | **Yes** — a missing field or unstamped ID breaks the first read | **The first consumer**, and no further | The D-17 schema test; the asserted excluded set; **the open authority question about where the frozen field set is read from** |
| **T-3** | **No, and least of the three** — a correct number, reported wrongly | **The thesis** | The caveat as a **column**, plus a consuming-unit check **that is not yet stated** |

**Two of the three fail silently, and they are the two that matter most.** T-2 — the loud
one — has the smallest blast radius. This is the inverse of the arrangement anyone would
choose, and it is a property of the material rather than of the design: **definitional
failures are quiet by nature**, because a definition that is wrong still produces
well-formed output.

**W-9's build boundary binds all three identically.** Permitted before G-09: module structure,
interfaces, placeholder CLI definitions, configuration wiring, safe fail-fast behaviour, and
this unit's `tests/` scaffolding. Barred until G-09 is signed for the affected component:
implementing any component whose P0 decision is unresolved; **filling any `TBD — freeze gate`
field**; executing any governed run; generating code for a unit carrying an open blocker on
that scope.

## Shared resources

| Resource | Owner | Used by | Note |
|---|---|---|---|
| `src/data/config.py` — `IntegrityError` and the hierarchy | `foundation` (R-01) | T-1, T-2 | **`StandardizationError` does not exist.** Set-differenced against `__all__`'s 17 names, the difference is exactly `{StandardizationError}`; `PhaseBoundaryError` is present. **No question in this unit's set asked about it** — routed to the gate (§ DISC-T-1) |
| The **run manifest**'s record of executed stage scripts | `foundation` | T-1 (the one-`02`-per-run assertion) | **Dependency owed, not assumed.** If the manifest does not record executed scripts, the assertion has nothing to read |
| `configs/data.yaml` — the QC operation list, D-17's field set, D-19's thresholds | this unit writes into it; `foundation` owns the config contract | T-1, T-2 | **`configs/` does not exist**, and the **QC list is `TBD — freeze gate`**, which is what blocks T-1 |
| The **stage entry contract** and `PhaseBoundaryError` | `governance-guards` | T-1 | Raised by this unit, **defined** by that one. NFR-PHASE-01's row (TA-27) is `governance-guards`' and **no coverage of it is claimed** |
| The **consuming units' reporting paths** | `evaluation-and-comparison`, `regimes-diagnostics-reporting` | T-3 | **The other half of the caveat contract**, and it is **not stated by them yet** |
| The **uncertainty budget** | split — production half here, placement `regimes-diagnostics-reporting`'s | T-2 | W-7 records the split; nothing here claims the budget complete |

---

## Requirement coverage

| Requirement | Component | Acceptance row | Row primary owner | Status |
|---|---|---|---|---|
| FR-P1-03-1 | T-1 | TA-04 | `inventory-and-registry` | ⛔ **BLOCKED** — closed set unavailable until the QC list is frozen |
| FR-P1-03-2 | T-1 (stage entry contract) | TA-27 | `governance-guards` | `Pending` |
| FR-P1-03-3 | T-2 | TA-15 | `foundation` | `Pending` |
| FR-P1-03-4 | T-3 | TA-15 | `foundation` | `Pending` |
| **FR-P1-03-5** | T-2 | ⚠ **NO ACCEPTANCE ROW** — WS-05 deferred to G-P3A | — | untested |
| NFR-TDEF-01 | T-2, T-3 | TA-15 | `foundation` | `Pending` |
| NFR-DQ-01 | T-2 | TA-19 | **`target-standardization`** — production half only | `Pending` |
| NFR-LEAK-01 | — *(binds elsewhere; see `security-design.md` § SD-T-06)* | TA-11 | `features-and-splits` | `Pending` — not claimed here |
| NFR-PHASE-01 | T-1 (as a raiser, not a definer) | TA-27 | `governance-guards` | `Pending` |

**Derived and printed.** **3** components (T-1, T-2, T-3). **9** coverage rows, identical in
membership to `security-design.md`'s table — set-differenced in both directions, **empty both
ways**. **1** row with no acceptance row, counted from the blank acceptance cell. **1**
requirement **BLOCKED**. **0** rows claimed satisfied. **0** of the three components exist on
disk, and **T-1 cannot run even once they do**, until the QC list is frozen.

**Decomposition of `security-design.md`'s 6 design sections across the three components**,
derived rather than asserted: **4** land in exactly one component — SD-T-01 → T-1,
SD-T-02 → T-3, SD-T-03 → T-1, SD-T-05 → T-1 — **1** is shared, **SD-T-04** (the row contract
across T-2, with its label limb touching T-3 through NFR-TDEF-01) — and **1**, **SD-T-06**,
belongs to **no component by construction**: it states what this unit does **not** own.
4 + 1 + 1 = 6, matching the sibling artifact's section count. **2** subjects are here-only
with no `security-design.md` counterpart: the § Failure domains observation that **the loud
component has the smallest blast radius**, and the explicit placement of the two cross-cutting
concerns W-6 and W-9.

**DISC-T-2 applies to this table too** *(added 2026-09-03 on the reviewer's Minor 1, which
found it stated in `security-design.md` and missing here)*. The `functional-design` map's
§ Requirement-to-workflow table carries **seven** rows against a printed *"6 requirements"*.
**This table uses 9**, matching `nfr-requirements`' corrected set and its sibling artifact,
and the disagreement is recorded rather than silently arbitrated. Its *"1 without an
acceptance row"* limb is correct and is what this table also prints.

**A decomposition that verifies is not evidence the decomposed set is complete.** The 4/1/1
split is arithmetically sound against `security-design.md` as written; it says nothing about
whether that artifact covers everything it should. The completeness check is the FR-P1-03 set
difference recorded in `security-design.md` § Requirement coverage — **empty, because this
unit carries all five** — and the two answer different questions.

## Assumptions & Open Questions

- **[Q4]** The criterion is **what each component makes true about the target**. It required placing W-6's one-`02`-per-run assertion and W-9's build boundary explicitly, since both cross all three; both are placed rather than left implicit.
- **[T-1 — blocked by design, and the scope of the block]** While the QC list is `TBD`, **standardization raises and stops and no target is produced**. The rule binds **the run that produces a target**, NOT T-2's schema contract, T-3's caveat column or any fixture exercise. **Production of a target waits on a supervisor freeze**, and that is on the critical path rather than a runtime surprise. **§18.3 does not supply this rule** — it governs implementation — and a third option, **refuse to RELEASE rather than to RUN**, was never weighed and is **routed to the gate** *(all three corrected 2026-09-03, reviewer finding 1, Major)*.
- **[T-3 — OPEN, the other half is not stated]** T-3 makes the caveat exist and travel; **a consumer failing for omitting it is the consuming unit's code**. **Not declared satisfied from one side.**
- **[Shared resources — OPEN, routed to the gate]** **`StandardizationError` does not exist**, and **no question in this unit's set asked about it**. Two sibling units have now had the same question put on a scope that undercounted it; this one did not ask at all. Proposed disposition follows the owner's two prior rulings, offered for an explicit yes or no. **Owner: the project decision owner.**
- **[Shared resources — dependency owed]** The one-`02`-per-run assertion needs `foundation`'s run manifest to **record executed stage scripts**.
- **[T-2 — OPEN, the authority question]** Where the D-17 conformance check reads the frozen field set from is `governance-guards` **R-20**'s question verbatim. **No third option is invented.**
- **Carried — the `02` ordinal collision** is a recorded §12 defect; **no `02a`/`02b` convention**; reachability is `governance-guards` R-23's and is **not guarded twice**.
- **Carried — BLK-05's implementation and execution limbs are open**; approving this stage discharges neither.
- **Carried — the floating-point diff tolerance is unset**, belonging with the fixture manifest's permitted tolerances.
- **Carried — `unit-of-work.md` § 5's stale "19"** against the §12 tree's **21** test modules; reported, not edited.
- **Carried — the Python interpreter present is 3.14.7, off the governed 3.11 pin.** Nothing it runs is governed evidence.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, authorises writing a module, or claims a gate, acceptance row or test as discharged.
