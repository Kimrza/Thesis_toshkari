# Security Design — `target-standardization`

**Unit** `target-standardization` (Bolt 6) · **Kind** `library` · **Stage** `nfr-design`

> **Re-saved 2026-09-04, content unchanged — not a redo and not a revision.** This stage's
> final pass ran on another clone of this repository, rooted at a different absolute path. The
> engine's completion check matches each artifact against the path recorded in its write
> receipt, so those confirmed writes are unreachable from this clone and the stage cannot be
> completed here. The consolidated summary confirmation of `2026-09-04T14:07:50Z` **stands and
> was not re-asked** — its questions-file digest still verifies. This paragraph is the
> native-tool write that re-registers the artifact on this clone. **Everything below is
> byte-identical to the reviewed text apart from this note. In particular the fail-closed
> block below is untouched: FR-P1-03-1 remains BLOCKED and the QC operation list remains
> `TBD — freeze gate`.**

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
> ⚠ *(Stale in turn on this clone, corrected 2026-09-04 on adversarial finding 7, Major:
> `python --version` now resolves to the zero-byte WindowsApps stub — **no interpreter is
> reachable at all**. The sentence above was true when written on 2026-09-03 and is preserved;
> the conclusion survives a second ground-shift — nothing here is governed evidence because
> nothing runs at all. The lesson the reviewer attached: a re-save that asserts "content
> unchanged" re-asserts the artifact's checked-and-printed disk facts, so interpreter
> reachability should be re-run at every re-save, not only at the original write.)*
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
| Banner: *"**No Python interpreter exists** in this environment, so every test is written-but-unexecuted or unwritten"* | **Stale.** `python --version` → **Python 3.14.7**. The suite runs. But **3.14.7 is not the governed pin** — TE §8.1 and TC-03d fix **3.11 exactly** — so nothing it produces is governed evidence. *(⚠ This cell was true on 2026-09-03 and is itself stale in turn on this clone as of 2026-09-04 — `python` now resolves to the WindowsApps stub and **nothing runs at all**; recorded per iteration-2 Minor 8, matching the banner's dated correction. The conclusion survives both ground-shifts.)* | **Neutral.** The conclusion survives on a different ground; the stated reason is false |
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

**The FR-P1-03 family is cited in full; it is NOT carried in full.** *(Corrected 2026-09-04 on
adversarial finding 6, Critical. The superseded paragraph, preserved: "…this unit carries
**all five**. Unlike its siblings there is no complement to explain: nothing in the family
belongs to another unit's design…")* `requirements.md`'s FR-P1-03 space is `{1,2,3,4,5}`, five
IDs, and all five appear in the table above — but `unit-of-work.md` § 5 gives this unit's
"Requirements carried" as **FR-P1-03-1, -3, -4, -5** (four of five), and § 2 assigns
**FR-P1-03-2 — the requirement AND its TA-27 acceptance row — to `governance-guards`**.
FR-P1-03-2's row above is therefore a **cited external obligation**, present because § SD-T-06
states obligations against it (this unit *raises* `PhaseBoundaryError`; it does not define the
boundary), exactly the footing NFR-LEAK-01 and NFR-PHASE-01 already stand on — and the table's
own owner column said so all along, which makes the superseded sentence a contradiction of the
table it summarised. The unqualified "carries all five" was an overclaim **not present in this
unit's own upstream** (`business-logic-model.md`'s map already routes FR-P1-03-2's row to
`governance-guards`); it was introduced at this stage. So: **carried = 4 of 5**; **cited = 5 of
5**; three of the four carried have their acceptance rows owned elsewhere, which is a third
distinct thing and is stated per row.

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
- **Carried, and re-dated — interpreter reachability.** On 2026-09-03 a Python 3.14.7 was reachable, off the governed 3.11 pin; **on 2026-09-04 no interpreter resolves at all** (WindowsApps stub). Under either state, **nothing run here is governed evidence** — the conclusion is ground-independent and that is the point of carrying it.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, authorises writing a module, or claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-04T21:20:32Z
**Iteration:** 2 (fresh receipt floor after redo jump; both "Receipt-floor note" sections treated as claims to verify, not as trusted context)

### Prior finding status

| # | Severity | Finding | Status |
|---|---|---|---|
| 1 | Major | §18.3 cited for a runtime stop it does not require; refuse-to-release option never weighed; block scope overstated | **Still open, unsoftened, routed to the gate** — confirmed present verbatim under the "⚠ THE §18.3 CITATION IS CORRECTED, AND A THIRD OPTION IS ROUTED" box in § SD-T-01 and under the equivalent box in `logical-components.md` § T-1. Both Receipt-floor notes (2026-09-04) correctly state it is unaltered. |
| 2 | Major | Column choice answers detectability, not TS-T-03's survival criterion; enforcing half unbuilt | **Still open, unsoftened, routed to the gate** — confirmed present under the "⚠ WHAT THE COLUMN ACTUALLY BUYS" box in § SD-T-02 and the equivalent box in `logical-components.md` § T-3. Both Receipt-floor notes correctly state it is unaltered. |
| 3 | Minor | DISC-T-2 missing from `logical-components.md` | **Resolved** — now present under `logical-components.md` § Requirement coverage, "DISC-T-2 applies to this table too (added 2026-09-03 …)". |
| 4 | Minor | "0 new dependencies" printed unqualified | **Resolved** — now reads "0 new **package** dependencies", with the cross-unit dependencies named separately in the same sentence. |
| 5 | Minor | Clean-run-assertion author unnamed | **Resolved** — § SD-T-05 and `logical-components.md` § T-1 now name `fixtures-and-reproducibility` as the assertion's author, with `foundation` and this unit named as the other two parties. |

### New findings (this pass)

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 6 | Critical | `security-design.md` § Requirement coverage, "The FR-P1-03 set difference is empty" paragraph; `logical-components.md` § Requirement coverage (same 9-row table) | The claim **"this unit carries all five [FR-P1-03] … nothing in the family belongs to another unit's design"** is false against the authoritative per-unit ownership ledger. `inception/units-generation/unit-of-work.md` § 5 (`target-standardization`) states **"Requirements carried (6). FR-P1-03-1, FR-P1-03-3, FR-P1-03-4, FR-P1-03-5, NFR-TDEF-01, NFR-DQ-01"** — four of the five FR-P1-03 IDs, explicitly omitting **FR-P1-03-2**. `unit-of-work.md` § 2 (`governance-guards`) states **"Requirements carried (10). REQ-ENG-5, FR-P1-02-6, FR-P1-03-2, …, NFR-PHASE-01, NFR-LIC-01"** — `governance-guards` carries FR-P1-03-2, not this unit. This is not merely an acceptance-row split (which the artifact does correctly disclose for FR-P1-03-3/-4/NFR-TDEF-01, all routed to `foundation`'s TA-15): for FR-P1-03-2, `unit-of-work.md` assigns **both** the requirement and its acceptance row (TA-27) to `governance-guards`. The artifact's own § SD-T-06 elsewhere states the substance correctly ("NFR-PHASE-01's row is `governance-guards`'… this unit raises `PhaseBoundaryError` rather than defines it"), which makes the unqualified "carries all five / nothing belongs to another unit's design" sentence in § Requirement coverage a direct, checkable contradiction of its own § SD-T-06 as well as of `unit-of-work.md`. This is the same defect class the dispatch brief names as Critical in two sibling units (a requirement folded into a unit's completeness claim that the authoritative unit-of-work.md assigns elsewhere), and it inflates this unit's printed "9 coverage rows … matching `nfr-requirements`' own corrected 9-row set" into an implicit ownership claim that `unit-of-work.md` does not support for FR-P1-03-2. | Correct the sentence to state that FR-P1-03-2 is carried by `governance-guards` per `unit-of-work.md` §2, not by this unit, and that this unit's own FR-P1-03 carry-set is `{1,3,4,5}` (4 of 5), with FR-P1-03-2 appearing in the coverage table only as a cited external obligation (the `PhaseBoundaryError` raise), exactly as NFR-LEAK-01 and NFR-PHASE-01 are already labelled. Re-derive and re-print the "9 rows" figure with that distinction stated, the way § SD-T-06 already models for the two NFR rows. |
| 7 | Major | `security-design.md` § SD-T-00, banner, and `nfr-design-questions.md` banner | The claim **"A Python interpreter DOES exist — 3.14.7"**, printed as a disk-state fact and carried unchanged through two Receipt-floor re-saves (2026-09-04), does **not** hold on this clone today: `python --version` now resolves to the WindowsApps execution-alias stub (exit code 49, "Python was not found; run without arguments to install from the Microsoft Store"), not a working 3.14.7 interpreter. The artifact's own stated conclusion — "nothing it runs is governed evidence" — is not undermined by this (it holds more strongly: nothing runs at all), but the premise it argues from is now stale, and neither Receipt-floor note re-verified workspace state before re-asserting "content unchanged" and "everything below is byte-identical." | Re-run `python --version` at the next touch of this artifact and either reconfirm 3.14.7 or record the WindowsApps-stub state explicitly, since the artifact already treats interpreter reachability as a checked-and-printed fact rather than an assumption, and that discipline should extend to re-saves, not only to the original write. |

### Checks run (this pass)

| Check | Result | Interpretation |
|---|---|---|
| `unit-of-work.md` § 5 "Requirements carried" for `target-standardization` | `FR-P1-03-1, FR-P1-03-3, FR-P1-03-4, FR-P1-03-5, NFR-TDEF-01, NFR-DQ-01` (6, no FR-P1-03-2) | Finding 6 — the "carries all five" claim is false. |
| `unit-of-work.md` § 2 "Requirements carried" for `governance-guards` | includes `FR-P1-03-2`, and "Acceptance rows (2). TA-27, TA-28" | Confirms FR-P1-03-2 (requirement **and** its TA-27 row) belongs to `governance-guards`, not this unit. |
| `unit-of-work.md` § 1 "Acceptance rows" for `foundation` | `TA-01, TA-02, TA-03, TA-10, TA-15, TA-22, TA-23` | Confirms TA-15's owner is `foundation`, as both artifacts state for FR-P1-03-3/-4/NFR-TDEF-01 — this limb of the ownership claim **holds**. |
| `unit-of-work.md` § 7 "Acceptance rows" for `features-and-splits` | includes `TA-11` | Confirms NFR-LEAK-01 → TA-11 → `features-and-splits` **holds**. |
| `unit-of-work.md` § 4 "Acceptance rows" for `inventory-and-registry` | includes `TA-04` | Confirms FR-P1-03-1 → TA-04 → `inventory-and-registry` **holds**. |
| `requirements.md` lines 360–364, FR-P1-03 family text and per-row `Test` column | FR-P1-03-1→TA-04, -2→TA-27, -3→TA-15, -4→TA-15, -5→`UNTESTED`/WS-05 deferred to G-P3A | Matches both artifacts' per-row citations exactly; the defect is the completeness sentence, not the per-row table. |
| `functional-design/business-logic-model.md` § Requirement-to-workflow map (lines 483–494) | 7 rows including FR-P1-03-2 (`W-1, through the stage entry contract` → TA-27 → `governance-guards`), text reads "6 requirements, 1 without an acceptance row" | Reconfirms DISC-T-2 (7 vs. "6"); also shows the upstream `functional-design` artifact already correctly attributes FR-P1-03-2's row ownership to `governance-guards` — the nfr-design artifacts' new "carries all five" sentence is an overclaim not present in their own upstream source. |
| `src/data/config.py` `__all__`, re-derived | 17 names, `PhaseBoundaryError` present, `StandardizationError` absent | DISC-T-1 reconfirmed accurate. |
| `evidence/DECISIONS.md` — D-1, D-16, D-17, D-19 | all four exist with matching content (D-16 median statistic, D-17 sixteen-field contract, D-19 four thresholds, D-1 half-open floor rule) | All four D-number citations verified accurate. |
| `domain-entities.md` 16-row field table | row 16 = `target_definition_id`, rows 14–16 tagged FR-P1-03-3 | Confirms the sixteen-field claim and the mechanism-vs-entity alignment for T-2. |
| `domain-entities.md` § 8 `TargetLabel` | label + lineage statement emitted by "the target-writing path", `target_definition_id` "already on every row" | Consistent with the column design in § SD-T-02/T-3; no contradiction found. |
| `component-methods.md`, grep for run-manifest / executed-scripts contract | no match | Confirms § SD-T-05's "dependency stated as owed, not assumed" is accurate — no such contract exists yet to cite. |
| Live filesystem: `scripts/`, `src/gnss/`, `configs/` | `scripts/` = `audit_ec1_drivers.py`, `merge_coverage_year.py` (+ `__pycache__`); `src/gnss/` = `__init__.py` only; `configs/` absent | All three disk-state claims **hold** as of this review. |
| Live filesystem: `python --version` | resolves to WindowsApps stub, exit 49, no interpreter | Finding 7 — stale against the artifact's printed "3.14.7" claim. |

### Coverage limits

- **Read-scope bound.** No sibling unit's `construction/<other-unit>/` content was opened; ownership facts for `foundation`, `governance-guards`, `inventory-and-registry` and `features-and-splits` were resolved only through the shared `inception/units-generation/unit-of-work.md` contract, per the dispatch's spot-check carve-out, not by reading any sibling's `construction/` directory.
- The four sibling boundary criteria (Q4's "fifth axis" claim) were again assessed for internal soundness only, not against sibling text.
- `unit-of-work.md` § 5's stale "19" test-module count (against the §12 tree's 21) is carried, not re-derived here; already recorded under `team.md` § Corrections as an owner ruling.
- `business-rules.md` R-64…R-73 content was taken on the citing artifacts' own quotations, consistent with the prior pass's coverage limits; not independently re-read line-by-line this pass given the budget spent on the ownership cross-check that surfaced Finding 6.

### Summary

The two Majors routed to the gate at the prior iteration (§18.3 misused for a runtime rule; the column decision answering detectability rather than TS-T-03's survival criterion) are confirmed **still present, unsoftened, and correctly disclosed as unresolved** by both Receipt-floor notes. All three prior Minors are resolved. This pass's per-ID ownership sweep against `unit-of-work.md` — the authoritative unit-carries-requirement ledger, not merely the acceptance-row crosswalk — found a new Critical: the printed claim that "this unit carries all five" FR-P1-03 requirements with "nothing in the family belonging to another unit's design" is false, since `unit-of-work.md` assigns FR-P1-03-2 (both the requirement and its TA-27 acceptance row) to `governance-guards`, and the artifact's own § SD-T-06 already says as much for the substance of that same requirement without the coverage table reflecting it. A live filesystem check also found the artifact's "Python 3.14.7 exists" disk-state claim stale on this clone (Major) — the interpreter now fails to resolve at all — though the artifact's own governed-evidence conclusion is not disturbed by that. One Critical finding is sufficient on its own to block READY under this project's verdict rule; the verdict is **NOT-READY** pending the ownership-sentence correction (Finding 6) and, ideally, a disk-state refresh (Finding 7) before the next re-save.

---

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-04T21:27:30Z
**Iteration:** 2 (repair verification — final iteration, budget is 2)

### Repair verification

| Prior finding | Repair claimed | Independently verified | Result |
|---|---|---|---|
| 6 (Critical) — "carries all five [FR-P1-03] … nothing in the family belongs to another unit's design" | Rewritten to state **cited = 5 of 5, carried = 4 of 5** (`{1,3,4,5}`), with FR-P1-03-2 stated as a cited external obligation on `governance-guards`, on the same footing as NFR-LEAK-01/NFR-PHASE-01; superseded text preserved as a quotation. Same repair applied to `logical-components.md` § Requirement coverage. | Re-derived independently from `unit-of-work.md` (not from the correction text): § 5 `target-standardization` — `**Requirements carried (6).** FR-P1-03-1, FR-P1-03-3, FR-P1-03-4, FR-P1-03-5, NFR-TDEF-01, NFR-DQ-01` (line 261, no FR-P1-03-2). § 2 `governance-guards` — `**Requirements carried (10).** … FR-P1-03-2 …` and `**Acceptance rows (2).** TA-27, TA-28` (lines 162, 166). This independently confirms carried = `{1,3,4,5}` and cited = 5/5 with FR-P1-03-2's requirement **and** its TA-27 row both belonging to `governance-guards`. The corrected text in both artifacts matches this exactly. | **Confirmed accurate. Resolved.** |
| 7 (Major) — "A Python interpreter DOES exist — 3.14.7" | Dated correction added under the banner (both files), the § Assumptions "Carried" bullet re-dated in both files, and the `logical-components.md` banner line updated — all stating the WindowsApps-stub / no-interpreter state as of 2026-09-04, with the ground-independent conclusion ("nothing run here is governed evidence") preserved. | Ran `python --version` live on this clone: exit code 49, `"Python was not found; run without arguments to install from the Microsoft Store…"` — confirms **no interpreter is reachable**, exactly as the correction states. Checked all five claimed sites: SD banner (lines 35–41) ✅ corrected; SD § Assumptions Carried bullet (line 445) ✅ corrected; LC banner (lines 33–36) ✅ corrected; LC § Assumptions Carried bullet (line 323) ✅ corrected; **SD-T-00's own discrepancy table, row 1 (line 87), was NOT touched** — it still reads *"python --version → Python 3.14.7. The suite runs… Neutral"* with no pointer to the 2026-09-04 re-correction, even though the banner six lines above it in the same file now says otherwise. | **Substance confirmed and independently reproduced. One representation missed — see new Minor finding below.** |

### New findings (this pass)

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 8 | Minor | `security-design.md` § SD-T-00, table row 1 (line 87) | The interpreter-state correction (finding 7) was applied to the banner, both files' § Assumptions "Carried" bullets, and the `logical-components.md` banner, but **not** to § SD-T-00's own discrepancy table, which still asserts unqualified *"python --version → Python 3.14.7. The suite runs"* with a `Neutral` direction — a stale, unqualified disk-state claim sitting a few lines below the corrected banner in the same document. This is the same defect class `project.md`'s sweep-representations corrections warn against (a corrected fact left standing in one of its representations while others are fixed), though here the ground-independent conclusion ("nothing run here is governed evidence") is not disturbed by it. | Add the same dated parenthetical used in the banner/Assumptions bullet to this table row, or add a one-line pointer to the correction, so a reader consulting only § SD-T-00's table is not given the stale claim as current fact. |

### Prior findings re-confirmed unsoftened

- **Finding 1 (Major, §18.3 misused for a runtime-stop rule; refuse-to-release option unweighed)** — still present verbatim under the "⚠ THE §18.3 CITATION IS CORRECTED, AND A THIRD OPTION IS ROUTED" box in § SD-T-01 and the equivalent box in `logical-components.md` § T-1. Correctly disclosed as routed to the gate, not resolved by this unit.
- **Finding 2 (Major, column choice answers detectability not TS-T-03's survival criterion)** — still present verbatim under the "⚠ WHAT THE COLUMN ACTUALLY BUYS" box in § SD-T-02 and the equivalent box in `logical-components.md` § T-3. Correctly disclosed as routed to the gate, not resolved by this unit.
- **DISC-T-1 (`StandardizationError` gate item)** — still open, still routed to the project decision owner for an explicit yes/no, unchanged from the prior pass.
- **Overclaim sweep** — QC operation list still `TBD — freeze gate` (line 21); floating-point diff tolerance still unset; FR-P1-03-1 still `BLOCKED` (line 384); "0 rows claimed satisfied" (line 399) still holds; no scientific value is filled and no gate/acceptance row is claimed discharged anywhere in the artifact.

### Recount and drift check (this pass)

| Item | Recounted value | Source | Drift? |
|---|---|---|---|
| Coverage rows | 9 (FR-P1-03-1…5 + NFR-TDEF-01, NFR-DQ-01, NFR-LEAK-01, NFR-PHASE-01), counted from the table at lines 382–392 | this artifact | None |
| FR-P1-03-1 → TA-04 → owner | `inventory-and-registry` | `unit-of-work.md` § 4, `Acceptance rows (3). WS-01, TA-04, TA-25` (line 233) | None |
| FR-P1-03-2 → TA-27 → owner | `governance-guards` | `unit-of-work.md` § 2, `Acceptance rows (2). TA-27, TA-28` (line 166) | None |
| FR-P1-03-3, -4 → TA-15 → owner | `foundation` | `unit-of-work.md` § 1, `Acceptance rows (7). TA-01, TA-02, TA-03, TA-10, TA-15, TA-22, TA-23` (line 133) | None |
| NFR-DQ-01 → TA-19 → owner | `target-standardization` (production half) | `unit-of-work.md` § 5, `Acceptance rows (1). TA-19` (line 265) | None |
| NFR-LEAK-01 → TA-11 → owner | `features-and-splits` | `unit-of-work.md` § 7, `Acceptance rows (12). WS-10 … TA-11 …` (line 329) | None |
| NFR-PHASE-01 → TA-27 → owner | `governance-guards` | same as FR-P1-03-2's row (line 166) | None |
| "1 row with no acceptance row" (FR-P1-03-5) | Still 1, blank acceptance cell at line 388 | this artifact | None |

No drift found against the iteration-1 verified figures; the finding-6 rewrite did not disturb the "9 rows" figure, the "1 row with no acceptance row" figure, the 4/1/1 section-decomposition split in `logical-components.md`, or the DISC-T-2 seven-vs-six disagreement note (still stated identically in both files, lines 111–117 here and lines 294–299 in `logical-components.md`).

### Verified — did not break

- No live text outside preserved-superseded quotations or `## Review` sections still asserts "carries all five" or an empty FR-P1-03 set difference in either file (grep-swept both files for the phrase and its variants; every hit is inside a quoted correction or the Review discussion).
- The two files' 9-row coverage tables and owner columns still agree with each other (`security-design.md` lines 382–392 vs `logical-components.md` lines 266–276) and with `unit-of-work.md`, cell for cell.
- The rewritten Finding-6 paragraph did not alter any adjacent claim: the "6 design sections" count, the "0 new package dependencies" qualification, and the "5 across three units" amendments-owed figure are all unchanged and internally consistent.
- `logical-components.md`'s own finding-6 paragraph (lines 301–309) is worded consistently with `security-design.md`'s (carried = 4, cited = 5/5), not merely cross-referencing it.

### Coverage limits

- Read-scope bound respected: ownership facts were re-derived only from the shared `inception/units-generation/unit-of-work.md` contract (the file this dispatch names as authoritative), never from any sibling unit's `construction/<other-unit>/` content.
- The live `python --version` check reflects this clone's current state only; the artifact's own dated-correction discipline (re-check at every re-save) is the right posture given interpreter reachability has now changed twice across two saves.
- `business-rules.md` R-64…R-73 and `functional-design`'s DISC-T-2 figures were taken as already-verified from the prior pass and not re-read line-by-line this pass, consistent with that pass's stated coverage limits.

### Summary

Both repairs verified independently and hold: the FR-P1-03 ownership correction (Finding 6, Critical) matches `unit-of-work.md` exactly — carried = `{FR-P1-03-1,3,4,5}`, cited = 5/5, with FR-P1-03-2's requirement and its TA-27 row both on `governance-guards` — and no live text outside preserved quotations still makes the false "carries all five" claim. The interpreter correction (Finding 7, Major) is independently reproduced (`python --version` exits 49, no interpreter reachable) and applied at four of five claimed sites; one representation, § SD-T-00's own table row, was missed and is raised as a new Minor (finding 8) rather than a blocker, since the ground-independent conclusion it supports is unaffected. The two Majors routed to the gate at iteration 1 (§18.3 misused for a runtime rule; column choice answering detectability rather than TS-T-03's survival criterion) stand unsoftened, exactly as intended — they are gate input, not defects owed to this stage. With the Critical resolved and confirmed, and two pre-existing, already-disclosed Majors plus one new Minor remaining, this artifact meets the stated verdict rule (zero Critical, ≤2 Major). **Verdict: READY**, with finding 8 and the two gate-routed Majors carried forward as the human's decision material at approval.

---

## Receipt-floor note — 2026-09-04 (re-saved after the second re-affirmation)

*A second redo jump was taken because the first recovery ran confirm/write/review out of
order. This unit's design is untouched, and its two Majors stay routed to the gate.*

A **redo jump** on `nfr-design` — taken to lift the review-freeze on `features-and-splits` and
`models-and-baselines` so their adversarial findings could be fixed on the project decision
owner's direction — reset this stage's receipt floor and invalidated this unit's
summary-confirmation and review receipts. **This unit's design was untouched by it.**

**No claim above is altered by this note** — including the two Majors routed to the approval
gate (§ SD-T-01's use of a TE §18.3 implementation clause to justify a runtime stop without
weighing the narrower refuse-to-release alternative, and § SD-T-02 answering TS-T-03's
*survival* question with a *detectability* answer while conceding the detecting half is
unbuilt). Both still reach the human. The stored confirmation was re-affirmed on 2026-09-04
(its value was already `Looks correct`), and this artifact is re-saved unchanged so the
engine's write-after-confirmation precondition is satisfied honestly rather than bypassed.

---

## Review — 2026-09-04 confirming pass (fourth floor)

**Reviewer:** aidlc-architecture-reviewer-agent

**Verdict:** READY
**Date:** 2026-09-04T21:34:00Z
**Iteration:** 1 (adversarial confirming pass, fresh receipt floor after a third stage-wide reset)

### Targeted checks (this pass)

| # | Check | Result |
|---|---|---|
| 1 | § SD-T-00 table row 1 (line 87) gained the dated stale-note fix (finding 8, Minor) | **Confirmed.** The row now reads: *"⚠ This cell was true on 2026-09-03 and is itself stale in turn on this clone as of 2026-09-04 — `python` now resolves to the WindowsApps stub and nothing runs at all; recorded per iteration-2 Minor 8, matching the banner's dated correction. The conclusion survives both ground-shifts."* Consistent with the banner (lines 35–41) and the § Assumptions "Carried, and re-dated" bullet (line 445) — all three sites now agree. Live-verified: `python --version` on this clone resolves to the WindowsApps execution-alias stub ("Python was not found; run without arguments to install from the Microsoft Store…"), confirming no interpreter is reachable, exactly as the note states. Finding 8 is resolved. |
| 2 | Critical repair (finding 6) still stands | **Confirmed independently against `unit-of-work.md`.** § 5 (`target-standardization`, line 261): `**Requirements carried (6).** FR-P1-03-1, FR-P1-03-3, FR-P1-03-4, FR-P1-03-5, NFR-TDEF-01, NFR-DQ-01` — no FR-P1-03-2. § 2 (`governance-guards`, lines 162, 166): `**Requirements carried (10).** … FR-P1-03-2 …` and `**Acceptance rows (2).** TA-27, TA-28`. This matches the artifact's stated carried = `{1,3,4,5}` (4/5), cited = 5/5, with FR-P1-03-2's requirement **and** its TA-27 row both on `governance-guards`. The 9-row § Requirement coverage table (lines 382–392) still shows the `FR-P1-03-2 \| SD-T-06 \| TA-27 \| governance-guards \| Pending` row with the correct owner cell. `logical-components.md`'s equivalent table (lines 266–276) and its own finding-6 paragraph (lines 301–309) agree cell-for-cell. |
| 3 | The two gate-routed Majors and `StandardizationError` open item stand unsoftened | **Confirmed.** § SD-T-01's "⚠ THE §18.3 CITATION IS CORRECTED, AND A THIRD OPTION IS ROUTED" box (lines 152–171) and § SD-T-02's "⚠ WHAT THE COLUMN ACTUALLY BUYS" box (lines 206–221) are present verbatim, matched by the equivalent boxes in `logical-components.md` § T-1/T-3 and its Assumptions bullets (lines 314–315). DISC-T-1 (`StandardizationError`, lines 94–109 and Assumptions line 437) is still open and routed to the project decision owner; `logical-components.md` line 316 carries the same. None of the three has been softened, resolved, or silently answered by this or the prior floor. |
| 4 | Regression grep — no live "carries all five" / unqualified interpreter claim outside preserved quotes and `## Review` | **Confirmed clean.** Grepped both files for `carries all five` and `nothing in the family belongs to another`. Every hit in `security-design.md` (lines 420, 469, 476, 482, 500, 515, 548, 561) sits inside the finding-6 discussion, a `## Review` table, or an explicitly labelled "superseded" quotation. `logical-components.md`'s one hit (line 306) is explicitly framed as a quoted superseded clause ("the superseded clause read …"). No live assertion of the false claim survives outside those contexts. |
| 5 | Overclaim sweep | **Confirmed unchanged.** QC operation list still `TBD — freeze gate` (line 21, and § SD-T-01 table row 4, line 130). Floating-point diff tolerance still unset (§ SD-T-03, lines 279–282). FR-P1-03-1 still `⛔ BLOCKED` (line 384). "0 rows claimed satisfied" (line 399) still holds. No scientific value is filled, no `TBD` field is closed, and no gate/acceptance row is claimed discharged anywhere in the artifact. |

### Verified — did not break

- The 9-row coverage tables in both files remain identical in membership and owner columns to each other and to `unit-of-work.md`, cell for cell.
- The "6 design sections" / "3 components, 4+1+1 decomposition" figures are unchanged and internally consistent across both files.
- The interpreter-state correction now agrees at all four prior sites plus the newly fixed § SD-T-00 table row — five of five representations now consistent, closing out finding 8.
- Both Receipt-floor notes (the re-registration note at the top of this file and its `logical-components.md` counterpart, plus the second-redo-jump notes) correctly state that no component, boundary, or status claim is altered by the re-save, and this is accurate against the content below them.

### Coverage limits

- Read-scope bound respected: this unit's own artifacts, its own `nfr-requirements/` and `functional-design/`, and the shared `inception/units-generation/unit-of-work.md` contract only. No sibling `construction/<other-unit>/` content was read; no `memory.md` was read.
- `unit-of-work.md` § 5's stale "19" test-module count (against the §12 tree's 21) is carried as an existing, already-recorded discrepancy and was not re-derived this pass.
- `business-rules.md` R-64…R-73 content was taken on the citing artifacts' own quotations, consistent with prior passes; not independently re-read line-by-line this pass.
- The live `python --version` check reflects this clone's current state at review time only.

### Summary

All five targeted checks pass. The § SD-T-00 discrepancy-table cell (the sole outstanding Minor from iteration 2) now carries the same dated stale-note as the banner and the Assumptions bullet, verified live against `python --version` on this clone. The Critical repair (FR-P1-03 carried=4/cited=5) is independently reconfirmed against `unit-of-work.md` §§ 2 and 5 with no drift. The two gate-routed Majors and the `StandardizationError` open item remain present, unsoftened, and correctly routed to the human rather than resolved unilaterally. No regression of the corrected overclaims was found. **Verdict: READY**, with the two Majors and the `StandardizationError` question carried forward as gate input.

---

## Review — 2026-09-05 re-affirmation (post-gate receipt refresh)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T08:15:17Z

### Prior terminal review quoted

`## Review — 2026-09-04 confirming pass (fourth floor)` — **Verdict: READY**, **Date:** 2026-09-04T21:34:00Z, **Iteration:** 1 (adversarial confirming pass, fresh receipt floor after a third stage-wide reset). Summary: "All five targeted checks pass... **Verdict: READY**, with the two Majors and the `StandardizationError` question carried forward as gate input."

### No edits since that review

The gate-rejection revision cycle touched `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`, and `fixtures-and-reproducibility` only. This unit's `security-design.md` and `logical-components.md` were not part of that revision scope; the file's content ends at the "2026-09-04 confirming pass (fourth floor)" review block with no subsequent edits, confirmed by direct read of the full file (no content follows that review section apart from this re-affirmation).

### Spot-checks performed (verified still holding)

| # | Claim re-verified | Result |
|---|---|---|
| 1 | `unit-of-work.md` § 5 (`target-standardization`), line 261: "Requirements carried (6). FR-P1-03-1, FR-P1-03-3, FR-P1-03-4, FR-P1-03-5, NFR-TDEF-01, NFR-DQ-01" (no FR-P1-03-2) | **Confirmed unchanged** — grep re-run against the live file, matches exactly. |
| 2 | `unit-of-work.md` § 2 (`governance-guards`), line 162: FR-P1-03-2 carried there, not by this unit | **Confirmed unchanged** — grep re-run against the live file, matches exactly. |
| 3 | Interpreter state — no Python interpreter reachable on this clone (WindowsApps stub) | **Confirmed unchanged** — `python --version` re-run live, exit code 49, "Python was not found; run without arguments to install from the Microsoft Store...", matching the artifact's carried claim. |
| 4 | QC operation list still `TBD — freeze gate`; FR-P1-03-1 still `⛔ BLOCKED` | **Confirmed unchanged** — both still read as stated at lines 21 and 384 of the live file. |

### Re-affirmed verdict

No repair was performed and none was needed. The standing verdict from the 2026-09-04 terminal review holds unchanged: the Critical (FR-P1-03 ownership) and prior Minor (interpreter-state table cell) remain resolved and unregressed; the two gate-routed Majors (§18.3 misuse; column-choice detectability-vs-survival) and the `StandardizationError` open item remain correctly routed to the human as unresolved gate input, not defects owed to this stage.

**READY**
