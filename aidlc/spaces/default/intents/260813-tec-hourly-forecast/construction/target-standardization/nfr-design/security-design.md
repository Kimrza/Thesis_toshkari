# Security Design — `target-standardization`

**Unit** `target-standardization` (Bolt 6) · **Kind** `library` · **Stage** `nfr-design`

> ## ⚠ FR-P1-03-1 IS BLOCKED, AND THIS DESIGN MAKES THAT BLOCK OPERATIVE
>
> Written against the **workspace as it is on 2026-09-03**, per the owner's ruling that a
> design is written against current state while `nfr-requirements` stays unchanged.
>
> **The QC operation list is `TBD — freeze gate`**, so the closed set of exactly four
> transformations **cannot be closed**, and FR-P1-03-1's criterion **cannot be checked**.
> Under Q2 = A this design makes that a **fail-closed condition**: while the list is unset,
> **standardization refuses to run and no target is produced.** The schedule cost is stated
> rather than discovered — this unit is blocked until a supervisor freeze lands.
>
> **Nothing this unit designs exists.** `scripts/02_standardize_prepared_target.py`,
> `src/data/prepared.py`, `tests/test_prepared_target_schema.py` and `configs/` are all
> absent; `scripts/` holds only `audit_ec1_drivers.py` and `merge_coverage_year.py`.
>
> **A Python interpreter DOES exist — 3.14.7, off the governed 3.11 pin** (TE §8.1, TC-03d).
> `nfr-requirements` says none exists; that is stale, and the conclusion it supported —
> nothing here is governed evidence — survives on the pin instead.
>
> **`FR-P1-03-5` carries no acceptance row.** WS-05, the only field-contract row, is deferred
> to **G-P3A**. **BLK-05's implementation and execution limbs are open**; **the `02` ordinal
> collision is a recorded §12 defect**, and no `02a`/`02b` convention is invented. **G-09 is
> signed (D-31) with preconditions UNMET**; **stage 3.1 remains FAIL**.
>
> **Two values stay unset by this stage**: the **QC operation list** and the **floating-point
> diff tolerance**. No scientific value is decided here; TE §18.2's absolute rule stands.

## Sources

- `../nfr-requirements/security-requirements.md` — **SEC-T-01** (the closed set, and why it cannot close), **SEC-T-02** (the label and lineage caveat as data), **SEC-T-03** (D-17's sixteen fields, three IDs, the asserted excluded set, D-19's thresholds), **SEC-T-04** (leakage, the phase boundary, and what this unit does not own). **One status claim superseded — see § SD-T-00.**
- `../nfr-requirements/tech-stack-decisions.md` — **TS-T-01** (the QC list is config and this stage does not fill it), **TS-T-02** (the diff and schema check on the approved stack; value-level not schema-level; the tolerance unset), **TS-T-03** (the caveat's carrier, **owed at 3.5** — answered here at § SD-T-02), **TS-T-04** (script identity and the `02` collision), **TS-T-05** (platform posture).
- `../functional-design/business-logic-model.md` — **W-1** … **W-9**, and § Requirement-to-workflow map.
- `../functional-design/business-rules.md` — **R-64** … **R-73**.
- **`performance-requirements.md`, `scalability-requirements.md` and `reliability-requirements.md` are absent by `produces_kinds` design** for a `library` unit; assessed in § Scope note.
- **The workspace, read 2026-09-03** — `scripts/` (two scripts), `src/` (six packages), `src/data/config.py`, `tests/` (six modules), `python --version`.
- `../../../inception/requirements-analysis/requirements.md` — **FR-P1-03-1** … **-5**; **NFR-TDEF-01**, **NFR-DQ-01**, **NFR-LEAK-01**, **NFR-PHASE-01**.
- `../../../inception/application-design/components.md`, `component-methods.md`, `services.md`.
- `evidence/DECISIONS.md` — **D-1** (the half-open floor cell rule), **D-16** (the aggregation statistic), **D-17** (the sixteen target fields), **D-19** (the support thresholds).
- `nfr-design-questions.md` — **Q1 = A**, **Q2 = A**, **Q3 = A**, **Q4 = A**, and the receipted Consolidated Summary Confirmation.

---

## Scope note

`produces_kinds` yields two artifacts for a `library` unit. The three absent categories are
assessed rather than skipped:

| Category | Assessment for `target-standardization` | Where it lives |
|---|---|---|
| **Performance** | No latency target. A bounded product — three cells, calendar 2022, hourly — and CPU-bound tabular work with no accelerator path. | — |
| **Scalability** | Bounded and known. No growth projection exists and none is invented. | — |
| **Reliability** | **Fail-closed on definition, not on availability**, and § SD-T-01 makes that operative rather than aspirational: a fifth transformation **fails**; an aggregation statistic that does not resolve to D-16 **fails**; a missing D-17 field **fails**; an unset QC list **stops the run**. The unit would rather produce nothing than produce a target whose definition is uncertain. | § SD-T-01, § SD-T-04 |
| **Security** | This artifact — **definitional integrity**, not access control. This unit holds no credential and reaches no restricted root. | — |
| **Observability** | The three definition IDs on every artifact; the caveat as a column; the data-quality block's four contents; the uncertainty budget's stated bounds. | § SD-T-02, § SD-T-04 |

---

## SD-T-00 — What is on disk, and the one upstream claim it contradicts

Derived by direct inspection on 2026-09-03, printed before it is relied on.

| Upstream claim | State on disk | Direction |
|---|---|---|
| Banner: *"**No Python interpreter exists** in this environment, so every test is written-but-unexecuted or unwritten"* | **Stale.** `python --version` → **Python 3.14.7**. The suite runs. But **3.14.7 is not the governed pin** — TE §8.1 and TC-03d fix **3.11 exactly** — so nothing it produces is governed evidence. | **Neutral.** The conclusion survives on a different ground; the stated reason is false |
| `configs/` absent | **Holds.** | — |
| The `02` ordinal collision | **Holds, and is still only on paper**: neither `02_standardize_prepared_target.py` nor `02_build_vtec_target.py` exists. `scripts/` holds `audit_ec1_drivers.py` and `merge_coverage_year.py`. | — |
| This unit's modules | **None exists** — `src/data/prepared.py`, `tests/test_prepared_target_schema.py`, the stage script. | — |

**Two facts run the other way and are stated here rather than discovered later.**

**DISC-T-1 — `StandardizationError` does not exist, and no question asked about it.** W-1
declares `RAISES StandardizationError; PhaseBoundaryError`. Set-differenced against
`src/data/config.py`'s `__all__` (17 names, grep-derived): **`PhaseBoundaryError` is
present; `StandardizationError` is absent.** The difference is exactly
**`{StandardizationError}`** — one name, and it is the **only** `RAISES` declaration in this
unit's `business-logic-model.md`.

> **This is routed to the gate, not decided here.** Two sibling units have now had the same
> question put to the owner on a scope that undercounted it — `inventory-and-registry` asked
> about two exceptions and the derivation found three; `external-products` asked about two
> and found five. **This unit's question set did not ask at all.** The disposition that
> follows from the owner's two prior rulings is plain — declared in `src/data/config.py`,
> deriving from `IntegrityError`, riding R-01's *"any future integrity-related exception"*
> clause, not claimed as an enumeration entry, since it is raised by this unit alone — and
> **applying a ruling to an item the owner was not shown is the widening this project has
> already had to correct.** Proposed for an explicit yes or no.

**DISC-T-2 — the `functional-design` map's row count and its printed total disagree.** Its
§ Requirement-to-workflow map table carries **seven** rows — FR-P1-03-1 … -5, NFR-TDEF-01,
NFR-DQ-01 — and the sentence beneath it reads *"**6 requirements**, 1 without an acceptance
row."* Counted from the table above the sentence, not from the sentence. **The "1 without an
acceptance row" figure is correct** (FR-P1-03-5). This artifact uses **9** coverage rows,
matching `nfr-requirements`' own corrected count rather than either figure in the map, and
records the disagreement rather than silently picking a side.

## SD-T-01 — While the QC list is unset, standardization does not run (Q2 = A)

SEC-T-01 records FR-P1-03-1's closed-set criterion as **BLOCKED**: the diff must show *"only
the documented transformations"*, the set has exactly four members, and the fourth —
**"documented QC"** — is defined nowhere.

| # | Transformation | Specified? |
|---|---|---|
| 1 | UTC normalization | **Yes** |
| 2 | Cell selection — D-1's floor rule, half-open | **Yes** |
| 3 | Hourly aggregation — D-16's median | **Yes** |
| 4 | **"documented QC"** | ⛔ **`TBD — freeze gate`** |

**Design.** `configs/data.yaml` carries a named `qc_operations` list. **While it is `TBD`,
standardization raises and stops**, naming the unset field, and **no standardized target is
produced.** An operation outside the list, once frozen, **fails as a fifth transformation
would**.

**Why fail-closed rather than skip-and-report, stated because a sibling unit answered the
same shape of question the other way.** `external-products` § SD-E-01 has its containment
check report **`skipped`, never `passed`**, with the §18.3 preflight reading the skip as
unmet. **That is right there and wrong here**, and the difference is what the check guards:

| | `external-products` | This unit |
|---|---|---|
| What the unverified check guards | a **module that does not exist** | a **scientific artifact that would exist on disk** |
| What can be wrongly consumed meanwhile | nothing — there is no code to violate the boundary | **the target**, by anything that reads the file |
| Where the "unmet" signal lives | a gate report | a gate report — **which does not travel with the file** |

A skipped check is a fact about a run. **A target on disk is a fact about the project**, and
it gets read by whoever needs a target. This unit's own stated posture — *"it would rather
produce nothing than produce a target whose definition is uncertain"* — resolves the case.

> ### ⚠ THE §18.3 CITATION IS CORRECTED, AND A THIRD OPTION IS ROUTED
> *(2026-09-03, on the reviewer's finding 1, Major)*
>
> **The superseded text read *"and TE §18.3's stop-and-report rule requires the same."* That
> over-reaches.** §18.3, as `team.md` quotes it, governs **implementation**: *"must not
> implement an affected component while its P0 decision is unresolved, and must stop and
> report rather than choose a default."* It says nothing about the **runtime behaviour of an
> already-written module**, so it cannot require this rule. What it does require is narrower
> and still bites: **the affected component must not be implemented** while the QC decision is
> unresolved. The fail-closed rule rests on this unit's own reliability posture and on the
> artifact-on-disk argument above — **not** on §18.3.
>
> **A third option was never weighed, and Q2's option set was this stage's own.** **Refuse to
> RELEASE rather than to RUN**: produce the artifact, refuse to hash, register or promote it,
> and mark it non-governed. That keeps fixture exercise and downstream development moving
> while denying the target any governed standing. Its risk is the one the artifact-on-disk
> argument names — a non-governed file is still a file, and this project's own evidence
> records how a caveated artifact becomes a relied-on one. **Which of the two the owner wants
> is routed to the gate**, because Q2 was answered on an option set that omitted it.

**The rule's SCOPE is narrower than the superseded text implied** *(same finding)*.
"Standardization refuses to run" binds **the run that produces a standardized target**. It does
**not** bind:

- **T-2's schema contract** — D-17's sixteen fields, the three IDs, the asserted excluded
  set — which is a property of the writer and is testable against fixtures with no QC list at
  all;
- **T-3's caveat column**, likewise;
- **any fixture exercise** of either.

The QC list bears on **which value transformations are permitted**, and on nothing else. A
fail-closed rule that halted work it has no bearing on would be a scheduling accident wearing
a governance costume.

**The cost, stated rather than discovered at 3.5.** This blocks **production of a standardized
target** until the QC list is frozen under a D-number. Every downstream consumer of that
target waits on a supervisor decision. That is the intended consequence of a
`TBD — freeze gate` value on a definitional input, and it should be visible on the critical
path rather than found when a run refuses.

**What the raise must name.** R-01's constructor contract: the **resource** is
`configs/data.yaml`'s `qc_operations` field, and the **expectation** is that it be frozen
under a D-number — not merely non-empty. A list filled by convenience satisfies "non-empty"
and is exactly what §18.2 forbids.

## SD-T-02 — The lineage caveat is a COLUMN (Q1 = A)

TS-T-03 left the carrier **owed at 3.5** — *"in the Parquet schema's metadata or as a column,
whichever survives the round-trip that `pyarrow` performs"* — and named the risk itself:
metadata *"is **easy to drop** through an intermediate `pandas` operation that rebuilds the
frame."*

**Design: a column on every row, alongside `target_definition_id`.**

> ### ⚠ WHAT THE COLUMN ACTUALLY BUYS — CORRECTED, BECAUSE THE FIRST ARGUMENT ANSWERED A
> ### DIFFERENT QUESTION THAN TS-T-03 ASKED
> *(2026-09-03, on the reviewer's finding 2, Major)*
>
> **TS-T-03's criterion is SURVIVAL**: the carrier must *"survive the pipeline's actual
> operations, not merely a direct read-back."* **The superseded argument answered
> DETECTABILITY** — which carrier's loss can be caught — and presented that as though it
> settled the survival question. It does not.
>
> **A column is dropped exactly as metadata is**, by a column-subset selection or a `groupby`
> that rebuilds the frame. On the criterion TS-T-03 actually set, **neither carrier survives
> by itself**, and claiming otherwise for the column was the defect.
>
> **What the column does buy is real and lesser, and is now stated as what it is**: when a
> column is lost, the loss is **visible to a schema check**; when key-value metadata is lost,
> nothing in the frame records that it was ever there. **Detectability, not survival.**

**Design: a column on every row, alongside `target_definition_id` — plus a preservation
obligation on this unit's own write path**, which the superseded text omitted entirely and
which is the only part of the survival question within this unit's power:

1. **Every artifact this unit writes carries the column.** Not the first write only — every
   write, including any re-write after an internal transformation.
2. **This unit's own round-trip test asserts the column survives the operations this unit
   performs**, exercised against a fixture rather than asserted in prose.
3. **Beyond this unit's write path, survival is not guaranteed and is not claimed.** A
   consuming unit that subsets columns loses it, and only that unit's own check can catch it.

**SEC-T-02's obligation is delivered by neither half alone, and the artifact now says so.**
The requirement is that **a consumer reporting a comparison without the caveat FAILS**. This
unit can make the caveat exist, travel out of its own write path, and be **detectably** absent.
The **failing** is the consuming unit's code, and that half **is not stated**. Choosing a
column makes the other half buildable — a schema check is something a consumer can actually
assert — and **does not build it**.

**The cost, stated plainly.** One repeated identical string per row. Parquet's dictionary
encoding makes that near-free on disk; in memory it is genuinely redundant. Accepted.

**If a metadata mirror is ever added** (question 1's option C), **the column wins by rule** —
otherwise the pair adds a disagreement rather than a safeguard.

**What the column carries** — the two disclosures, unchanged:

1. The Phase 1 target is **location-sampled gridded VTEC** (Madrigal cell), **never** labelled
   receiver-specific station-observed VTEC, and it carries its **own distinct**
   `target_definition_id`.
2. Part of any measured IRI or GIM difference is a **geometry and sampling artefact rather
   than skill** — Phase 1 compares a grid cell against a station-coordinate evaluation,
   Phase 2 an IPP cloud against a zenith estimate (Vision §6.6).

**No claim of numerical equivalence** between the Phase 1 and Phase 2 targets is permitted.
Phase 2 is a **fixed-protocol replication on a new target lineage, not a second statistically
independent blind test**, and that must be stated at abstract level.

> ### ⚠ THIS IS ONE HALF OF A CROSS-UNIT CONTRACT, AND THE OTHER HALF IS NOT STATED
>
> This unit can make the caveat **exist and travel**. It cannot make a consumer **fail** for
> omitting it — that check lives in the **consuming unit's reporting path**. **This artifact
> states only this unit's half**, and **does not declare the contract satisfied from one
> side.** Choosing a column rather than metadata makes the other half *buildable* — a schema
> check is something a consumer can actually assert — but it does not build it.

## SD-T-03 — The closed-set diff, and why it is value-level

**Design (R-64, W-2, TS-T-02).** A **value-level** diff against the provider bytes, showing
**only the documented transformations**, with the set enumerated as **exactly four** and a
**fifth a failure** rather than something a reviewer must notice.

**Value-level, not schema-level, and the distinction is not pedantry.** FR-P1-03-1's criterion
is about **what changed between the provider bytes and the standardized product**. A check
comparing column names and dtypes does not meet it — and it is the cheaper check, so it looks
like progress. Stated because the two are easy to conflate.

**The tolerance is a declared value and is NOT set here.** A diff over aggregated values needs
a floating-point tolerance, and one taken from whatever `numpy.isclose` defaults to is a
scientific value filled by convenience. It belongs with the fixture manifest's *"permitted
floating-point tolerances"* (TE §15.2).

**No diff, schema or data-validation package is added** — `pandas`, `numpy`, `pyyaml`,
`pyarrow`, `pytest`, all TE §8.1 required. A schema library would be a new dependency, a §10.1
register entry and a version to pin on two platforms, to check **sixteen fields** against a
contract already written down. If 3.5 finds the field contract genuinely needs one, **that
returns to `nfr-requirements` as a dependency question** rather than being settled at 3.5.

## SD-T-04 — The row contract: sixteen fields, three IDs, an asserted excluded set

**Exactly D-17's sixteen fields** — not fifteen, not seventeen — checked by a **schema test
against the contract**, not by review (R-66, W-3).

**Three definition IDs** — `phase_id`, `source_id`, `target_definition_id` — stamped on
**every** dataset, prediction, mask and comparison (R-70, NFR-TDEF-01).

**The excluded set is asserted, never substituted** (R-67). A run that finds a different
excluded set than the one declared **fails**; it does not proceed on the set it found. This is
the same shape as `inventory-and-registry`'s declared-versus-required scope check, and for the
same reason: a run that silently adopts what it found produces a defensible-looking artifact
whose scope nobody chose.

**The support thresholds are D-19's, and they carry their basis** (R-68) — frozen from
measured **January–November** distributions with **December excluded by construction**.
December must not inform a threshold, and **the trigger is December being seen, not the lock
being opened**.

**The data-quality block carries four contents, and "unexplained" is doing the work** (R-71,
NFR-DQ-01): an unexplained discrepancy is recorded **as unexplained**, never attributed to the
nearest plausible cause. **The uncertainty budget states its bounds rather than truncating**
(R-72) — a budget that silently clips under-reports.

> **⚠ Where the conformance check reads the frozen field set from is OPEN, and it is the same
> authority question `governance-guards` R-20 already carries for D-24.** W-3 asserts
> config-equals-D-17; R-20's words apply unchanged: *"it must assert against the **authority**,
> not merely against the config — otherwise config and manifest can agree with each other
> while both drift."* **No third option is invented here**; carried to the gate.

## SD-T-05 — Exactly one `02` script per run, asserted from the run manifest (Q3 = A)

R-73 and TS-T-04 fix that a run contains **exactly one `02` script**, selected by `--phase`,
and that the clean-run contract **asserts** it — which is what makes the adopted reading of
the ordinal collision **falsifiable** rather than merely stated.

**Design.** Every run records the stage scripts it executed in its run manifest, and the
clean-run contract asserts **exactly one recorded entry whose basename matches `02_*`**.

**Why the manifest and not the tree.** R-73 constrains **the run**. A static check that
`scripts/` holds exactly two `02_*` files constrains the **repository** — two `02` scripts
executing in one process would pass it, which is precisely the failure the assertion exists to
detect. **A run-time guard inside each script**, asserting via `sys.modules` that the other is
not loaded, was **declined**: it makes each script aware of its sibling's module path — the
coupling `governance-guards` R-28 declined elsewhere for the same reason — and it duplicates a
concern W-6 assigns to `governance-guards` R-23, against its own warning that *"two rules about
one fact is how they drift apart."*

> **Dependency stated as owed, not assumed.** This assertion requires the run manifest to
> **record executed stage scripts**. That is `foundation`'s run-record contract, and this unit
> is its consumer. **If the manifest does not carry executed scripts, this assertion has
> nothing to read** — routed to the gate rather than presumed.
>
> **Who writes the assertion** *(assigned 2026-09-03 on the reviewer's Minor 3, which found it
> unowned)*: **the clean-run contract**, `tests/test_clean_run.py`, owned by
> **`fixtures-and-reproducibility`** — TE §13.2 makes the ordered clean-run sequence that
> unit's artifact, and R-73 places the assertion there in terms (*"the clean-run contract
> asserts exactly one `02` script per run"*). **This unit specifies the assertion and does not
> author it.** Three parties, named rather than left implicit: `foundation` supplies the
> manifest field, `fixtures-and-reproducibility` writes the assertion, this unit states what
> it must assert.

**The collision itself is recorded, not fixed.** `scripts/02_build_vtec_target.py` (Phase 2)
shares the ordinal. **`code-generation` must not invent a `02a`/`02b` convention** — the
ambiguity it would resolve is already resolved by `--phase`, and inventing one would be a §12
amendment made by assertion. The **reachability** question — that the Phase 2 script is
unreachable under `--phase 1` — belongs to `governance-guards` **R-23** and is **not guarded
twice**.

## SD-T-06 — What this unit does not own, stated so it is not assumed

**NFR-LEAK-01 binds elsewhere.** Any train-only transformation is fitted on **training
partitions only, per fold, never on the full dataset**. This unit **defines** the target and
its thresholds; it **does not fit a scaling transform**. The obligation belongs to the feature
and model units, and **this artifact does not claim to satisfy it**.

**NFR-PHASE-01's row is `governance-guards`'** (TA-27). Phase 1 code paths must not import or
execute raw-processing modules, nor produce DCB/STEC/mapping/satellite/arc fields — enforced
through the stage entry contract, whose `PhaseBoundaryError` this unit raises rather than
defines.

**The uncertainty budget is not wholly this unit's.** W-7 records the split; **NFR-DQ-01's
production half is this unit's and its placement is `regimes-diagnostics-reporting`'s**.
Nothing here claims the budget complete.

**TA-15's row is `foundation`'s**, and TA-04's is `inventory-and-registry`'s. This unit
**owns TA-19** and **supports TA-15**.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Row primary owner | Status |
|---|---|---|---|---|
| FR-P1-03-1 | SD-T-01, SD-T-03 | TA-04 | `inventory-and-registry` | ⛔ **BLOCKED** — closed set unavailable until the QC list is frozen |
| FR-P1-03-2 | SD-T-06 | TA-27 | `governance-guards` | `Pending` |
| FR-P1-03-3 | SD-T-04 | TA-15 | `foundation` | `Pending` |
| FR-P1-03-4 | SD-T-02 | TA-15 | `foundation` | `Pending` |
| **FR-P1-03-5** | SD-T-04 | ⚠ **NO ACCEPTANCE ROW** — WS-05 deferred to G-P3A | — | untested |
| NFR-TDEF-01 | SD-T-02, SD-T-04 | TA-15 | `foundation` | `Pending` |
| NFR-DQ-01 | SD-T-04, SD-T-06 | TA-19 | **`target-standardization`** — production half only | `Pending` |
| NFR-LEAK-01 | SD-T-06 | TA-11 | `features-and-splits` | `Pending` — **binds elsewhere**, not claimed here |
| NFR-PHASE-01 | SD-T-06 | TA-27 | `governance-guards` | `Pending` |

**Derived and printed.** **6** design sections (SD-T-00 … SD-T-06 is seven headings, of which
SD-T-00 is a state record rather than a design section). **9** coverage rows, counted from the
table above — the **5** FR-P1-03 requirements plus NFR-TDEF-01, NFR-DQ-01, NFR-LEAK-01 and
NFR-PHASE-01 — matching `nfr-requirements`' own corrected 9-row set with **empty set
difference in both directions**. **1** row with no acceptance row (FR-P1-03-5), counted from
the blank acceptance cell. **1** requirement recorded as **BLOCKED**. **0** rows claimed
satisfied. **2** values left unset by this stage (the QC operation list; the floating-point
diff tolerance). **0** new **package** dependencies — *(qualified 2026-09-03 on the reviewer's
Minor 2: the unqualified "0 new dependencies" sat beside two owed **cross-unit** dependencies,
`foundation`'s run-manifest record of executed scripts and the consuming units' caveat check,
both of which are dependencies in every sense but the packaging one)*. **0** amendments owed —
`src/data/prepared.py` is
intra-package and its shape is this stage's to specify, so the running total stays **five
across three units**.

**The FR-P1-03 set difference is empty.** `requirements.md`'s FR-P1-03 space is `{1,2,3,4,5}`,
five IDs, and this unit carries **all five**. Unlike its siblings there is no complement to
explain: nothing in the family belongs to another unit's design, though three of the five have
their **acceptance rows** owned elsewhere, which is a different thing and is stated per row.

**Where this table differs from the `functional-design` map, and why.** That map's table
carries **seven** rows while the sentence beneath it reads *"6 requirements"* (§ DISC-T-2).
This artifact uses **9**, matching `nfr-requirements`, and adds NFR-LEAK-01 and NFR-PHASE-01
as rows precisely because § SD-T-06 states obligations against them — **as obligations, not as
coverage claims**, which is why both carry an explicit *binds elsewhere* / *row owned* note.

## Assumptions & Open Questions

- **[Q2 / SD-T-01 — the schedule cost is the design]** Fail-closed **blocks the entire unit** until the QC list is frozen under a D-number. Every downstream consumer of the standardized target waits on that supervisor decision. Stated so it appears on the critical path rather than being found when a run refuses.
- **[Q2 / SD-T-01 — and it is not "non-empty"]** The raise fires while the field is `TBD`. A list **filled by convenience** would satisfy a non-emptiness check and is exactly what §18.2 forbids, so the expectation named in the raise is *frozen under a D-number*, not *present*.
- **[Q1 / SD-T-02 — OPEN, the other half is not stated]** This unit makes the caveat exist and travel; **a consumer failing for omitting it is the consuming unit's code**. Choosing a column makes that half buildable and does not build it. **Not declared satisfied from one side.**
- **[DISC-T-1 — OPEN, routed to the gate]** **`StandardizationError` does not exist** and **no question in this unit's set asked about it**. Set-differenced against `config.py`'s 17-name `__all__`: the difference is exactly `{StandardizationError}` (`PhaseBoundaryError` is present). The disposition following the owner's two prior rulings is plain — `config.py`, deriving from `IntegrityError`, riding R-01's any-future clause — but **applying a ruling to an item the owner was not shown is a widening**, so it is proposed for an explicit yes or no. **Owner: the project decision owner.**
- **[DISC-T-2]** The `functional-design` map's table has **seven** rows against a printed *"6 requirements"*. Recorded rather than resolved; this artifact's 9 rows match `nfr-requirements` and the disagreement is not silently arbitrated.
- **[SD-T-04 — OPEN, the authority question]** Where the D-17 conformance check reads the frozen field set from is unresolved, and it is `governance-guards` **R-20**'s question verbatim: *"assert against the **authority**, not merely against the config."* **No third option is invented.**
- **[SD-T-05 — dependency owed]** The one-`02`-per-run assertion needs the run manifest to **record executed stage scripts** — `foundation`'s contract. Stated as owed, not assumed satisfied.
- **Carried — the `02` ordinal collision** is a recorded §12 defect. **No `02a`/`02b` convention.** Reachability is `governance-guards` R-23's and is not guarded twice.
- **Carried — BLK-05's implementation and execution limbs are open.** The module does not exist and has never been run; **approving this stage discharges neither**.
- **Carried — `unit-of-work.md` § 5's stale "19"** against the §12 tree's **21** test modules, reported for an annotate-in-place decision, not edited.
- **Carried — the floating-point diff tolerance is unset** and belongs with the fixture manifest's permitted tolerances (TE §15.2).
- **Carried — the Python interpreter present is 3.14.7, off the governed 3.11 pin.** Nothing it runs is governed evidence.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, authorises writing a module, or claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-04T13:58:38Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `security-design.md` § SD-T-01; `logical-components.md` § T-1 | The fail-closed rule is justified by TE §18.3, but §18.3's quoted text governs **implementation** ("must not implement an affected component while its P0 decision is unresolved, and must stop and report rather than choose a default"), not the **runtime** behaviour of an already-written module. It cannot be cited as requiring that a written module raise at run time. Separately, only two options were weighed — fail-closed run vs. `external-products`' skip-not-pass — and the narrower failure point of **refusing to release rather than refusing to run** (produce the artifact, refuse to hash/register/promote it, mark it non-governed) was never considered. As written the blockage extends to work the QC list has no bearing on: T-2's sixteen-field schema contract, T-3's caveat column, and any exercise of the two TE §9.2 fixtures through this stage. | Re-state the fail-closed rule on its own merits — the artifact's own "a target on disk is a fact about the project" argument is sufficient and is not §18.3 — and explicitly weigh and dispose of refuse-to-release as the narrower alternative, including whether the plumbing fixture may run under it. |
| 2 | Major | `security-design.md` § SD-T-02; `logical-components.md` § T-3 | TS-T-03's stated constraint is that the chosen carrier must **"survive the pipeline's actual operations, not merely a direct read-back"** (verified, `tech-stack-decisions.md` lines 85–87). SD-T-02 answers a different question — which carrier's *loss is detectable* — and never addresses survival. A column is dropped by an ordinary column-subset or groupby rebuild exactly as metadata is; its only advantage is that a **schema check** would catch the loss, and the artifact concedes that check is the consuming unit's code and is not stated. Neither half then delivers SEC-T-02's "a consumer that reports a comparison without it **fails**", and this unit places no preservation obligation on its own write path either. | Either state the preservation obligation this unit does own (which of its own operations must carry the column forward, asserted in `tests/test_prepared_target_schema.py`), or record explicitly that TS-T-03's survival criterion is **not** met by the column and is being converted into a detectability criterion — as a stated substitution, not a silent one. |
| 3 | Minor | `logical-components.md` § Requirement coverage | DISC-T-2 (the `functional-design` map's seven rows against its printed *"6 requirements"*) is stated twice in `security-design.md` but appears nowhere in `logical-components.md`, whose own 9-row table is where a reader meets the disagreement; it is deferred only by a § Sources pointer. | Restate DISC-T-2 in one line under `logical-components.md` § Requirement coverage, as the sibling artifact does. |
| 4 | Minor | `security-design.md` § Requirement coverage ("Derived and printed") | **"0 new dependencies"** is printed unqualified in the same artifact that states an owed cross-unit dependency on `foundation`'s run manifest (§ SD-T-05) and an unresolved authority dependency (§ SD-T-04). The intended sense is package dependencies; the word is used in the cross-unit sense a few lines away. | Qualify as "0 new **package** dependencies", and note the one cross-unit dependency owed. |
| 5 | Minor | `security-design.md` § SD-T-05 | The one-`02`-per-run assertion is placed in "the clean-run contract" (`test_clean_run.py`) without naming which unit writes it. The manifest dependency is routed as owed; the assertion's author is not. | Name the owner of the assertion alongside the manifest dependency, or state it as a second owed item. |

### Checks run

| Check | Result | Interpretation |
|---|---|---|
| `__all__` in `src/data/config.py`, regex-derived and printed | **17 names**; `PhaseBoundaryError` present, `StandardizationError` absent | **DISC-T-1 CONFIRMED.** The `__all__` = 17 figure is exact. |
| `RAISES` grep across `functional-design/business-logic-model.md` | one line (88): `StandardizationError; PhaseBoundaryError` | Confirms it is the unit's **only** `RAISES` declaration; the set difference against `__all__` is exactly `{StandardizationError}`. |
| Row count of `business-logic-model.md` § Requirement-to-workflow map (lines 485–491) vs. its printed total (line 493) | table **7 rows**; sentence **"6 requirements, 1 without an acceptance row"** | **DISC-T-2 CONFIRMED**, including that the "1 without an acceptance row" limb (FR-P1-03-5) is correct. |
| Coverage-row membership, both artifacts, set-differenced both directions | 9 rows each: FR-P1-03-1…-5, NFR-TDEF-01, NFR-DQ-01, NFR-LEAK-01, NFR-PHASE-01 — **empty both ways** | The printed "9 … identical in membership" claim holds. |
| Against `nfr-requirements/security-requirements.md` § Requirement coverage | same 9 IDs | The "matching `nfr-requirements`' own corrected 9-row set" claim holds. |
| FR-P1-03 ID space in `inception/requirements-analysis/requirements.md` | `{1,2,3,4,5}` | The "set difference is empty; this unit carries all five" claim holds. |
| Rows with a blank acceptance cell | **1** (FR-P1-03-5) | Holds in both artifacts. |
| Design-section count | headings SD-T-00…SD-T-06 = 7; minus SD-T-00 (a state record) = **6** | Holds, with the qualifier stated. |
| 4/1/1 decomposition of those 6 sections | SD-T-01, -03, -05 → T-1 and SD-T-02 → T-3 (**4** single-component); SD-T-04 shared (**1**); SD-T-06 no component (**1**); 4+1+1=6 | Arithmetically sound. |
| Component count | T-1, T-2, T-3 = **3** | Holds. |
| Workspace state: `scripts/`, `tests/`, `configs/`, `python --version` | `scripts/` = `audit_ec1_drivers.py`, `merge_coverage_year.py`; `tests/` = 6 modules; `configs/` **absent**; **Python 3.14.7** | All four § SD-T-00 disk claims hold, including the 3.14.7-off-the-3.11-pin correction. |
| TS-T-03 quotation | lines 81–87 verified: *"easy to drop through an intermediate `pandas` operation that rebuilds the frame"*, *"owed at 3.5"*, and the **survival** constraint | Quotes accurate; the survival clause is the one SD-T-02 does not answer — finding 2. |
| SEC-T-02 strength claim | line 89: *"a consumer that reports a comparison without it fails"* | Quoted accurately; the "does not ask that the caveat be *present*" reading is fair. |
| Cross-artifact consistency: fail-closed rule, column decision, DISC-T-1, DISC-T-2 | fail-closed ✓ both; column ✓ both; DISC-T-1 ✓ both; **DISC-T-2 in `security-design.md` only** | Finding 3. |
| Satisfaction / discharge claims | both artifacts print "0 rows claimed satisfied" and close with the "None of the above decides a scientific value, fills a `TBD — freeze gate` field, authorises writing a module, or claims a gate, acceptance row or test as discharged" bullet; QC list and diff tolerance both recorded unset; FR-P1-03-5 marked untested; BLK-05 carried open; no `02a`/`02b` invented | **No improper claim found.** |

### Coverage limits

- **Read-scope bound.** No sibling unit's `construction/<other-unit>/` content was opened. The characterizations of `external-products` § SD-E-01's skip-not-pass, `governance-guards` R-20/R-23/R-28, `foundation`'s run-record contract and TA-15 ownership, `inventory-and-registry`'s scope check, and the four sibling boundary criteria are therefore **unverified** and treated as this unit's own claims. Finding 1 attacks the *argument* the `external-products` comparison carries, not the sibling's actual text.
- **`unit-of-work.md` § 5's stale "19" against 21** is carried, not re-derived here; it is already recorded as an owner ruling under `team.md` § Corrections.
- Q4's boundary criterion was assessed for internal soundness only — the three-axis split and its 4/1/1 decomposition verify — not against the sibling criteria it claims a fifth axis distinct from.

### Summary

Every machine-checkable claim in both artifacts was re-derived and **all of them hold**: `__all__` = 17 with the set difference exactly `{StandardizationError}`, the seven-rows-against-"6 requirements" map defect, the 9-row identical membership across both artifacts and against `nfr-requirements`, the empty FR-P1-03 set difference, the 6 / 3 / 4-1-1 counts, and the four disk-state facts — and nothing is claimed satisfied or discharged. The two Majors are argumentative rather than arithmetic: § SD-T-01 leans on a TE §18.3 clause that governs implementation to justify a **runtime** stop and never weighs the narrower refuse-to-release alternative, even though its own rule blocks the schema and label work the QC list has no bearing on; and § SD-T-02 answers TS-T-03's *survival* question with a *detectability* answer while conceding the detecting half is not built. Neither blocks a developer once the QC list is frozen, so the verdict is READY with both Majors routed to the approval gate.
