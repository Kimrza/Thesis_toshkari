# Security Design — `external-products`

**Unit** `external-products` (Bolt 5) · **Kind** `library` · **Stage** `nfr-design`

> **Re-saved 2026-09-02 after the owner-directed redo.** This is the unit the
> `STAGE_JUMPED` redo of `nfr-design` was ordered for. Unlike its four siblings, **this
> artifact did change**: the terminal pass's Critical and Major were repaired, and the two
> Minors with them. See § Remediation of the TERMINAL-pass findings at the foot of this file
> for what moved and why. The consolidated summary was re-confirmed against the corrected
> design before this save.
>
> **Revised again 2026-09-02 under a SECOND owner-directed redo.** The fifth reviewer pass
> found the fourth consecutive Critical of the same family, so the repair changed shape: the
> **candidate-importer set is now defined once by subtraction from the allowlist and is never
> enumerated anywhere**, and an unresolvable intermediate yields `skipped` rather than
> `passed`.
>
> **Revised a THIRD time 2026-09-02** after the sixth reviewer pass found the enumeration
> genuinely gone but the **domain** narrowed twice over in its place. The domain now spans
> **`.py` files and `.ipynb` code cells**; the **walk includes `__init__.py`** while only the
> cardinality **count** subtracts it; **`tests/*` is NOT allowlisted** — the allowlist is TE
> §12's two paths, and the blanket matrix row is routed to the gate; and the
> unresolvable-intermediate rule is **inside** the ordered switch, ranked below a found path.
> See § Remediation of the post-redo TERMINAL pass and § Remediation of the second-redo pass.
>
> **Revised a FOURTH time 2026-09-02** under a third owner-directed redo. The seventh pass
> recorded the design's **control** as buildable and its **domain** as coextensive with the
> rule, and found the remaining defect in its **account of the workspace**: the artifacts
> still called the candidate set empty and the check *"cannot fail today"*. **Derived and
> printed instead: 18 files walked, 12 counted — only the TARGET limb is empty**, so the
> check reports **`skipped` over 18 files it really would inspect**. The `__init__.py` byte
> sizes are corrected, the matrix discrepancy is routed with an owner, and one payload schema
> is stated in both artifacts. See § Remediation of the second-redo TERMINAL pass.

> ## ⚠ NFR-IRI-01'S NEGATIVE CONTROL IS NOT WRITTEN, AND ALL THREE MODULES ARE ABSENT
>
> Written against the **workspace as it is on 2026-09-02**, per the owner's ruling that a
> design is written against current state while `nfr-requirements` stays unchanged.
>
> **`tests/test_iri_denial.py` DOES NOT EXIST.** `nfr-requirements` states in its banner and
> twice in its coverage table that it is *"written but UNEXECUTED"*. It is not written.
> **NFR-IRI-01 — Vision §7.1's *binding architectural rule* — has no negative control at
> all**, and this correction runs **against** this unit, not for it.
>
> **`src/external/iri.py`, `gim.py` and `spaceweather.py` do not exist**;
> `src/external/` holds `__init__.py` only. Neither does
> `scripts/04_build_external_products.py`, nor `configs/`. R-55's amendment — a boundary
> contract for the whole package — is still owed.
>
> **A Python interpreter DOES exist — 3.14.7, off the governed 3.11 pin (TE §8.1).** Anything
> it runs is **not governed evidence**.
>
> **D-25's requested §15.2 amendment is UNGRANTED, and EV-12's F10.7 limb is unmet at G-04**
> (`evidence/DECISIONS.md:1854`, `:1648`). SD-E-04's limb 4 — the limb with scientific
> consequence — leans on that convention.
>
> **Undischarged**: WS-09 (this unit's own), WS-10, WS-11, TA-08, TA-12; **TA-36 is
> `Pending`** — approved, never run. **REQ-ENG-9, FR-P1-04-4, FR-P1-04-15 and FR-P1-04-18
> carry no acceptance row at all.** The **`gim_network_overlap_flag` audit has not run**, and
> **no independence claim may precede it**. **IRI generation is blocked** on R-59's
> validation, which has not happened. **G-09 is signed (D-31) with its own preconditions
> UNMET**; the §18.3 preflight has never run.
>
> **Two values stay `TBD — freeze gate`**: the `iricore` pin with its switch set, topside
> option and explicit 2000 km ceiling, and the CODE final GIM product version. **FR-P1-04-18's
> interpolation rule is UNSET** — a §18.2 Student-owned forbidden choice (Q-15). No scientific
> value is decided here.

## Sources

- `../nfr-requirements/security-requirements.md` — **SEC-E-01** (NFR-IRI-01 on two independent limbs, and the residual that survives both), **SEC-E-02** (the GIM comparator and unproven independence), **SEC-E-03** (IRI generation gated on an unrun validation), **SEC-E-04** (driver integrity: lags, grades, trailing mean, carry-forward, never backfill), **SEC-E-05** (byte-identical or explicitly divergent). **Three status claims superseded — see § SD-E-00.**
- `../nfr-requirements/tech-stack-decisions.md` — **TS-E-01** (`iricore`; the configuration *is* the benchmark), **TS-E-02** (CODE final GIM; the issue *is* the comparator), **TS-E-03** (stdlib `ast`; the static check authoritative; dynamic imports in scope), **TS-E-04** (the approved data stack; the trailing mean as a property test), **TS-E-05** (two platforms; CPU a complete path).
- `../functional-design/business-logic-model.md` — **W-1** … **W-10**, and § Requirement-to-workflow map; in particular W-3's transitive reachability scan and its two disclosed gaps, W-6's four limbs, W-7's four obligations, W-8's two-tier closure and its reanalysed-value block.
- `../functional-design/business-rules.md` — **R-54**/**R-54a**, **R-55** … **R-63**.
- **`performance-requirements.md`, `scalability-requirements.md` and `reliability-requirements.md` are absent by `produces_kinds` design** — `nfr-requirements` maps them to `[service, ui]` / `[service]` / `[service]`, and this unit is `library`. Assessed in § Scope note rather than treated as a gap.
- **The workspace, read 2026-09-02** — `src/` (six packages), `src/data/config.py`, `scripts/audit_ec1_drivers.py`, `tests/` (six modules), `python --version`.
- `../../../inception/application-design/component-dependency.md` — the dependency matrix and its forbidden-edge row for `iri.py` / `gim.py`; `components.md`, `component-methods.md`, `services.md`.
- `../../../inception/requirements-analysis/requirements.md` — **FR-P1-04-1**, **-3**, **-4**, **-9**, **-15**, **-17**, **-18**; **REQ-ENG-9**; **NFR-IRI-01**, **NFR-LEAK-01**, **NFR-REP-01**.
- `nfr-design-questions.md` — **Q1 = A**, **Q2 = A**, **Q3 = A**, **Q4 = A**, and the receipted Consolidated Summary Confirmation.

---

## Scope note

`produces_kinds` yields two artifacts for a `library` unit. The three absent categories are
assessed rather than skipped:

| Category | Assessment for `external-products` | Where it lives |
|---|---|---|
| **Performance** | No latency target. IRI generation over a year of hourly epochs at three cells — W-6's **26,000-call workload** — is the largest compute here, and it is **blocked** by R-59, so the gate binds before throughput does. The runtime is **measured and recorded**, never estimated. | § SD-E-04 |
| **Scalability** | Bounded: three cells, calendar 2022, hourly. No growth projection exists and none is invented. | — |
| **Reliability** | **Two-tier and already fixed by R-61**, and this unit is where the distinction is sharpest: a **missing month is recorded** (non-fatal, machine-readable, naming *which* months), a **hash mismatch terminates** naming the file and the violated expectation. A missing driver hour and a wrong driver hour get opposite handling. | § SD-E-06 |
| **Security** | This artifact — dominated by **containment**, not access control. | — |
| **Observability** | W-8's provenance-fields block on the manifest — `release_status`, `retrieval_date`, the full product identity **including any version suffix**, `sha256` — plus the run record. | § SD-E-06, § SD-E-07 |

---

## SD-E-00 — What is on disk, and the upstream claims it contradicts

Derived by direct inspection on 2026-09-02, printed before it is relied on.

| Upstream claim | State on disk | Direction |
|---|---|---|
| Banner and coverage table: *"`tests/test_iri_denial.py` is **written but UNEXECUTED**"*; FR-P1-04-1 and NFR-IRI-01 marked *"`Pending` — test written, UNEXECUTED"* | **False.** `tests/` holds six modules — `test_acquisition_window.py`, `test_locked_test_guard.py`, `test_merge_script_restricted_reads.py`, `test_phase_boundary.py`, `test_release_contract.py`, `test_release_hashes.py`. **`test_iri_denial.py` is not among them.** | **AGAINST this unit.** The gap is larger than upstream states: the control is **unwritten**, not merely unrun |
| Banner: *"No Python interpreter exists in this environment"* | **Stale.** `python --version` → **Python 3.14.7**, present and **off the governed 3.11 pin**. | **Mixed.** Tests can run; nothing they produce is governed evidence |
| `src/external`'s three modules, and R-55's owed contract | **None exists.** `src/external/` holds `__init__.py` (24 bytes). `src/features/`, `src/models/`, `src/evaluation/`, `src/gnss/` each hold `__init__.py` only. `scripts/` holds two scripts, neither of them `04_build_external_products.py`. | **Neutral** — the scaffolding exists, this unit's own work does not |
| W-8: *"`audit_ec1_drivers.py` **line 184 returns `0` regardless of missing months**"* | **Confirmed open.** `scripts/audit_ec1_drivers.py:184` is an unconditional `return 0` at the end of `main()`; `:181` prints `missing=` to stdout and nothing reads it into an exit code. | **Neutral** — the gap W-8 exists to close is exactly as described |

**One fact runs the other way and is stated here rather than discovered later.**

**DISC-E-1 — the containment rule's TARGETS do not exist, so W-3's check as originally
specified would have returned a vacuous `pass`.** `src/external/iri.py` and `gim.py` are
absent, so a reachability scan finds nothing to reach and — under the pre-design specification
— reports success. That is the discrepancy: a passing critical check on Vision §7.1's *binding
architectural rule* is exactly the kind of reassurance that survives into a gate record
unexamined.

> ## ⚠ THE CANDIDATE-IMPORTER SET IS **NOT** EMPTY, AND SAYING IT WAS WAS A DEFECT
>
> *(Corrected 2026-09-02 on the second-redo terminal pass's finding 1, Critical.)* The
> superseded text said *"**every module that could violate it** … is absent"* and called this
> **two independent causes of vacuity**. **Only one cause is real.** Derived under this
> design's own definition and printed rather than asserted:
>
> | | Today |
> |---|---|
> | **Target limb** | **EMPTY** — neither `src/external/iri.py` nor `gim.py` exists |
> | **Risk-surface limb** | **POPULATED** — **18 files walked, 12 counted** |
>
> The 18: `notebooks/madrigal_phase1_coverage_audit.ipynb`; `scripts/audit_ec1_drivers.py`
> and `scripts/merge_coverage_year.py`; `src/__init__.py`; `src/data/{__init__,config,
> locked_test,release}.py`; `src/{external,features,gnss,models}/__init__.py`; and the six
> `tests/` modules. **`src/evaluation/` is excluded because it is allowlisted, not because it
> is empty.** The count is 18 minus the six `__init__.py` files.
>
> **Consequence, and it is the reason this correction is Critical rather than tidy.** The
> check does **not** report a vacuous `pass` today and it is **not** inert: under the ordered
> switch it reaches **clause 4** and reports **`skipped`, naming the target limb** — over a
> set of 18 files it really would inspect. An implementer told the check is dead has no reason
> to run it; a gate record saying so captures a dead control where a live one exists. **The
> stale claim was an inference the earlier, narrower set supported, carried forward without
> being re-derived when the set widened.**

## SD-E-01 — A check that cannot fail is not a control (Q1 = A)

> **What the check does TODAY, stated before the design that produces it**: it reaches clause
> 4 of the ordered switch and reports **`skipped`, naming the empty target limb**, having
> walked **18 files**. It is live, not inert.

R-56's static check asks whether any module outside `scripts/04_build_external_products.py`
and `src/evaluation/` can reach `src/external/iri.py` or `gim.py`, **directly or
transitively**. Per § DISC-E-1, it returns `pass` while proving nothing.

**Why this is not a curiosity.** TE §18.3's preflight gate criterion is *"zero unresolved P0
fields and **no failing critical test**"*, and **IRI-free denial is one of its ten named
critical items**. A vacuous pass satisfies that criterion in full.

**Design — three parts, and the third is the one that matters.**

1. **The check reports `skipped`, never `passed`, whenever EITHER side of the rule is
   unpopulated.** The vacuity predicate has **two limbs, because DISC-E-1 names two causes**:

   | Limb | Populated when | Skip reason if empty |
   |---|---|---|
   | **Target side** | at least one of `src/external/iri.py`, `src/external/gim.py` exists | *no containment target exists* |
   | **Risk-surface side** | the **candidate-importer set** (defined once below) is **non-empty** | *the candidate-importer set is empty* |

   ### The candidate-importer set — defined ONCE, by complement, and never enumerated

   > **The candidate-importer set is everything that can execute Python in this repository
   > and is not an allowlisted importer.** It is defined by **subtraction from the
   > allowlist**, never by listing directories.

   | | |
   |---|---|
   | **The domain** | every file in the repository that can execute Python: **`.py` files AND the code cells of `.ipynb` notebooks**. A notebook is not a `.py` file, so the walk **extracts its code cells and parses each with `ast`** before matching — without that step the domain silently excludes the one importer class `requirements.md`:370 names by example and `business-rules.md`:318 requires a negative control for |
   | **Allowlisted importers** | `scripts/04_build_external_products.py`; anything under `src/evaluation/`. **Two paths, exactly as TE §12 states them.** |
   | **Candidate-importer set** | **everything else in the domain** |

   **The walked set and the counted set differ in ONE stated way, and the difference is
   deliberate.**

   | | Contents |
   |---|---|
   | **Walked** (clause 1's reachability search) | the candidate-importer set **entire, `__init__.py` files included** |
   | **Counted** (the risk-surface limb's cardinality test) | the candidate-importer set **minus `__init__.py` files** |

   > **⚠ WHY THE TWO ARE NOT THE SAME SET, AND WHY SAYING THEY WERE WAS A DEFECT** *(corrected
   > 2026-09-02 on the second-redo pass's finding 2, Critical)*. The `__init__.py` exclusion is
   > a **cardinality heuristic**: an otherwise-empty package should not count as a populated
   > risk surface. The previous revision declared walked and counted to be one set, which
   > **promoted that heuristic into the walk** — and on today's tree that is decisive:
   > **`src/features/`, `src/models/`, `src/gnss/` and `src/external/` each hold exactly one
   > file, their `__init__.py`** — 24, 22, 20 and 24 bytes by `wc -c` *(sizes corrected and
   > `src/evaluation/` removed from this list 2026-09-02 on the terminal pass's finding 3: the
   > superseded text read "five packages, exactly 24 bytes", which was right for two of five,
   > and `src/evaluation/` is **allowlisted** and therefore not a candidate at all)*. So the
   > only place an `src/features` → `iri` import could be written today is the file the walk
   > had subtracted.
   > **A package `__init__.py` can carry an import like any other module**, and transitivity
   > **through** a package `__init__` is walked like any other edge. The walk is a strict
   > superset of the count; only the count subtracts.

   > **⚠ `tests/*` IS NOT ALLOWLISTED, AND THE PREVIOUS REVISION'S REASON FOR GRANTING IT WAS
   > WRONG** *(corrected 2026-09-02 on the second-redo pass's findings 1 and 5)*. That revision
   > admitted `tests/*` on the ground that *"WS-10 requires the denial test to fail on a
   > deliberately injected `iri_*` field, and `tests/test_iri_denial.py` cannot perform that
   > injection without importing what it is testing."* **That reasoning does not hold.** WS-10
   > injects an **`iri_*` field** — a **data** act on a feature matrix, not an import — and
   > this project's own `tests/test_phase_boundary.py` demonstrates the technique for asserting
   > an import boundary **without importing anything**: parse the source with `ast`. So no test
   > needs the grant, and the grant is withdrawn. **The allowlist is TE §12's two paths.**
   >
   > **The matrix row that appeared to grant it is routed, not followed.**
   > `component-dependency.md`:34's `tests/*` row reads `yes` in **all seven columns** — a
   > blanket convenience row — and is contradicted **four lines below it**, at `:38`, by that
   > same artifact's *"**Exactly two importers** of `iri.py` and `gim.py`, as TE §12 states
   > it… Everything else is forbidden"*, and by `requirements.md`:370's allowlist statement.
   > **This design follows TE §12 and the matrix's own prose, and routes the blanket row to
   > the gate as a discrepancy for the owner to rule on.** If a test is ever found to
   > genuinely require the import, that is a change record against TE §12, not a reading this
   > stage may adopt.

   > **⚠ WHY THIS IS STATED AS A COMPLEMENT AND NOT A DIRECTORY LIST** *(corrected 2026-09-02
   > on the terminal pass's finding 2, Major, and its Critical)*. This is the **fourth** time
   > this section has restated the risk surface, and the first three all failed the same way:
   > `src/features/` + `src/models/` (two trees), then `src/` + `scripts/` (two directories),
   > then `src/` + `scripts/` + `notebooks/` (three). **Each enumeration was narrower than the
   > rule and read as a tightening**, and the third left `tests/` neither walked nor counted
   > while the *walk* stayed narrower than the *limb* at one site. `requirements.md`:370 states
   > an **allowlist**; its four named importer classes — `src/data/`, `src/gnss/`, a training
   > script, a notebook — are **examples of the complement, not its definition**. An
   > enumeration can always omit one more directory; a complement cannot.

   **Precedence, stated because a condition without one is not a control.** The outcome
   switch is ordered, and **a detected violation outranks both limbs**:

   1. **The scan found a reachability path** → **`failed`**, regardless of either limb **and
      regardless of any unresolved edge elsewhere in the graph**.
   2. No path found, but the walk hit **an unresolved edge** → `skipped`, with the edge
      recorded.
   3. No path, no unresolved edge, **both** limbs populated → `passed`.
   4. No path, no unresolved edge, **either** limb empty → `skipped`, naming which.

   > **⚠ CLAUSE 1'S RANK OVER CLAUSE 2 IS THE POINT, AND ITS ABSENCE WAS A DEFECT**
   > *(corrected 2026-09-02 on the second-redo pass's finding 4, Major)*. The
   > unresolvable-intermediate rule was previously stated **outside** the ordered switch, so
   > its rank against clause 1 was unstated and the literal reading let an unresolved edge
   > **skip over a violation the scan had already found** — the same masking shape the
   > terminal pass graded Critical. **A found path is a fact; an unresolved edge is an
   > absence of information, and an absence never outranks a fact.**

   > **⚠ CORRECTED 2026-09-02 on adversarial finding 1 of the terminal pass, which was
   > Critical — the iteration-1 repair reopened the defect in a broader form.** That repair
   > scoped the risk-surface limb to *"`src/features/` or `src/models/` — the two package
   > trees FR-P1-04-1 and TE §12 name as the forbidden importers"*. **`requirements.md`:370
   > says the opposite in terms**: the boundary holds *"**as an allowlist, not a denylist** —
   > TE §12 states it as 'imported only by `scripts/04_build_external_products.py` and
   > `src/evaluation/`', so an import from **`src/data/`, `src/gnss/`, a training script or a
   > notebook violates it exactly as** an import from `src/features/` or `src/models/`
   > does"*. DISC-E-1's own wording already carried the right phrase — *"and any other
   > importer"* — and **the repair dropped it while appearing to add rigour.**
   >
   > Paired with an **unconditional** *"otherwise it skips"*, the effect on today's tree was
   > strictly worse than what it replaced: `src/data/` holds three real modules, so a
   > **detected** violation originating there would have reported `skipped` and satisfied
   > §18.3's *"no failing critical test"*. **Iteration 1's predicate could only skip where a
   > violation was impossible; its repair could skip where one had been found.** The precedence
   > rule above is the second half of the fix and is why a condition alone was not enough.
   >
   > **`IMPL-3` and `IMPL-13` are open against exactly this allowlist-versus-denylist
   > reading**, which is why the wider form is the one that must be written down.
   >
   > **⚠ NOTEBOOKS WERE STILL MISSING FROM THAT WIDENING** *(corrected 2026-09-02 on the
   > post-redo pass's finding 2, Major)*. The complement was scoped *"under `src/` or
   > `scripts/`"*, and `requirements.md`:370 names **a notebook** alongside a training script
   > as violating the boundary identically. `business-rules.md`:318 carries **`Import iri from
   > a notebook → fails`** as a required R-56 negative control, and
   > `notebooks/madrigal_phase1_coverage_audit.ipynb` **exists on disk today**. `notebooks/`
   > is now in the walked set. A widening that stopped one directory short of the rule it was
   > widening to match is the third instance this stage has recorded of a repair narrowing a
   > set while appearing to broaden it.

   **Two mechanics this design fixes so 3.5 does not re-decide them.**

   - **The skip payload and the `passed` payload are the same structure.** Both carry the
     candidate-importer set the scan actually walked — **count and module paths** — plus,
     on a skip, the identifier of the empty limb. Naming one payload and not the other is
     what made the earlier symmetry claim unbuildable.
   - **Clause 1 is decided by name-matching, not by file resolution**, so it is meaningful
     even when the target limb is empty. The walk asks whether any module in the candidate
     set imports the module **path** `src.external.iri` or `src.external.gim`, directly or
     transitively. A file that does not exist can still be **named** in an import statement —
     which is exactly the state a partly-built tree produces — so a violation is detectable
     with no target file present, and clause 1 fires ahead of the skip.
   - **A third-party or stdlib import is NOT an edge in this graph, and is NOT an unresolved
     edge** *(added 2026-09-02 on the third-redo pass's finding 2, Major — the rule said
     nothing about them, and the omission was decisive)*. The graph is **first-party only**:
     an import naming a module outside this repository — `pytest`, `pandas`, `numpy`,
     `pyyaml`, anything in the stdlib — is **not walked and not recorded as unresolved**,
     because it cannot reach `src.external.iri` or `gim` by any path this check governs.
     **Why this had to be said**: all six `tests/` modules import `pytest`, so if a
     third-party import scored as an unresolved edge the scan would land on **clause 2**
     rather than clause 4, and the liveness claim stated throughout both artifacts would be
     wrong — in exactly the clean CPU environment TE §13.2 governs. An **unresolved edge** is
     therefore only a **first-party** import that names a repository module which does not
     exist.
   - **An unresolvable INTERMEDIATE breaks the chain, and that is reported rather than passed
     over** *(added 2026-09-02 on the terminal pass's Minor)*. Name-matching settles the absent
     *target*; it does not settle an absent *intermediate*. If `a.py` imports `b`, `b` does not
     exist, and the chain `a → b → gim` therefore cannot be walked, the scan **records an
     unresolved edge** in its scan-scope payload and the outcome is **`skipped`, not
     `passed`** — the same treatment as an empty limb, for the same reason. A partly-built
     tree is full of unresolvable intermediates, so treating them as clean would restore the
     vacuous pass by a third route. This is the transitive-walk counterpart of R-27's rule
     that an unparseable file is a failure rather than a file importing nothing.

   > **⚠ CORRECTED 2026-09-02 on adversarial finding 1, which was Critical.** The first issue
   > carried the target limb only — *"when neither `src/external/iri.py` nor
   > `src/external/gim.py` exists"* — and so **reproduced the defect it was written to fix**.
   > W-10 explicitly permits *"module structure, interfaces, placeholder CLI definitions"*
   > before G-09, so `iri.py` and `gim.py` may legitimately exist as **stubs** while
   > `src/features/` and `src/models/` still hold only `__init__.py`. In that state the
   > one-limb predicate does not fire, the scan walks `src/data`'s three real modules — which
   > were never going to import IRI — finds nothing, and returns **`passed`**: the vacuous
   > pass, now green instead of skipped, and therefore worse. **DISC-E-1 named both causes and
   > the control covered one.**

2. **The skip reason is machine-readable, not only prose** — a structured value naming the
   empty limb — so the preflight reads it without parsing English. A skip is already this
   project's idiom: the local suite run of this session recorded **277 passed / 2 skipped**,
   so a skip is a legible outcome here rather than a novelty.
3. **A skipped critical check is UNMET at the §18.3 preflight — and that is already the
   approved criterion, not a reading this stage invents.**

   > **⚠ CORRECTED 2026-09-02 on adversarial finding 2, Major.** The first issue called this
   > *"a reading this stage fixes"* and *"the option"*, cited nothing, named no owner, and
   > routed it nowhere — while Q2's and Q3's smaller cross-unit enlargements were each
   > explicitly routed to the gate. **`requirements.md` FR-WS-7 (line 462) already carries
   > it, and more strongly.** FR-WS-7 states the §18.3 gate — *"zero unresolved P0 fields and
   > no failing critical test"* — and **enumerates the ten critical tests rather than leaving
   > them as "the critical set"**, with **IRI-free denial** named among them. A skipped check
   > is not a passing one, so a skip fails FR-WS-7's criterion **by definition**; this stage
   > does not have to legislate the reading, and it does not have the standing to.
   >
   > **The row is another unit's.** `application-design/components.md:63` assigns FR-WS-7 to
   > `config.py` — `foundation`'s module — together with REQ-ENG-2, REQ-ENG-10 and
   > FR-P1-03-5. **Q1's option-A impact line said the cost was "a definition this stage would
   > be fixing"**, which understated what already exists and overstated this unit's standing.
   > The correction is recorded rather than applied to the answered question, and the
   > **dependency is routed to the gate** on the same footing as SD-E-02's and SD-E-03's.

   **What this unit owns and what it does not.** This unit owns the check's **reporting
   contract** — a two-limb vacuity predicate, a `skipped` outcome, and a machine-readable
   reason. It does **not** own the preflight that consumes it. What it depends on is that
   `foundation`'s FR-WS-7 assertion **reads the structured skip reason** rather than counting
   non-failures, and **that dependency is stated as owed, not assumed satisfied.**

**What each rejected option would have cost, recorded so the choice is checkable.**
Failing closed always (option B) would make a vacuous pass impossible with no new gate
semantics, at the price of a suite that is **red today and until the modules are written** on
a state the project's own plan calls correct — and a permanently-red suite trains people to
ignore red. Skipping with no preflight consequence (C) leaves §18.3 able to pass with
NFR-IRI-01 unverified. Passing with a recorded caveat (D) puts `passed` beside the binding
architectural rule when nothing was checked, and this project's own evidence records how a
caveated figure becomes a relied-on figure.

> ### ⚠ THE RISK THIS DESIGN TAKES ON, NAMED RATHER THAN MITIGATED AWAY
>
> **A normalised skip is how a control quietly stops being one.** If a preflight ever counts
> a skip as satisfied, the skip becomes **strictly worse than the vacuous pass it replaced**,
> because it looks like diligence. FR-WS-7's *"no failing critical test"* over an enumerated
> ten is what stops that — **an already-approved criterion this unit depends on, not one it
> supplies**, which is the correction of 2026-09-02 above.
>
> **Two residual risks this design names and does not close.** First, the dependency itself:
> if `foundation`'s FR-WS-7 assertion counts non-failures instead of reading the structured
> skip reason, nothing here detects it. Second, **the risk-surface limb is a cardinality test,
> not a representativeness test.** A candidate-importer set holding one trivial stub satisfies
> it, and the scan then reports `passed` over a surface that is populated but thin.
>
> **The mitigation is symmetry, and it is required rather than suggested** *(strengthened
> 2026-09-02 on terminal finding 4, Minor — the first issue said "a narrower proxy would have
> to know which modules are 'real', which is a judgment no static check makes", which is an
> overstatement that closed off a cheap fix)*. **Every outcome carries ONE payload schema**
> *(field list unified across both artifacts 2026-09-02, terminal Minor — the two had listed
> different subsets and neither was the union)*: the **candidate-importer set actually
> walked, by count and by module path**; **any unresolved edges**; and, on a skip, **the
> identifier of the empty limb**. `failed`, `passed` and `skipped` all carry it, with the
> empty-limb field populated only where it applies. A reader of a `passed` result can then see
> it was reached over 18 modules rather than thirty, **without any check having to judge which
> modules are "real"**. The judgment stays with the reader, and the evidence stops being
> absent.

**What is not reopened.** R-56's mechanism stands as specified: **transitive** reachability
over the import graph, stdlib `ast`, **static check authoritative for this unit** (the
source-tree-versus-running-process asymmetry W-3 argues in its own terms, not a paraphrase of
`governance-guards` R-24), a **grep-class visibility check** for `importlib` / `__import__`
outside the allowlist with any hit a **review item**, and the **uncovered residual** of a
run-time-computed module path. This section changes what the check *reports*, never what it
*checks*.

## SD-E-02 — Where the exceptions live (Q2 = A) — and there are five, not two

**Decision.** `ImportBoundaryError` and `FeatureAvailabilityError` are **declared in
`src/data/config.py`**, derive from `IntegrityError`, are added to `__all__`, and **ride
R-01's *"any future integrity-related exception"* clause** — not claimed as enumeration
entries. This matches the owner's `inventory-and-registry` Q2 = A ruling and this unit's own
upstream, which reaches the same reading independently for `FeatureAvailabilityError`.

**Why `config.py` and not the `src/data/exceptions.py` §12 amendment.** The amendment is the
better end state and is **not taken here**: splitting declarations between two modules would
defeat the stated reason `config.py` was ruled the site — that a package forbidden from
importing a leaf module must still be able to catch what it raises — and this unit is the one
where that reason bites hardest, since the whole point of the allowlist is that
`src/features` and `src/models` **cannot** import `src/external`. The §12 amendment should be
raised on its own merits with **all seventeen existing declarations migrating together**, not
as a side effect of placing two new ones.

**Constructor contract, inherited unchanged.** R-01 requires every raise to name the
**resource** and the **violated expectation**. For `ImportBoundaryError` the resource is the
**offending module path**, and the expectation names the **reachability path** — the chain,
not just the endpoint, because a transitive violation whose message names only `gim` tells an
implementer nothing about which hop to cut.

> ## ⚠ THE SET DIFFERENCE IS FIVE, AND Q2 PUT TWO TO THE OWNER
>
> Derived at this stage by set-differencing the `RAISES` declarations in
> `business-logic-model.md` against `src/data/config.py`'s `__all__`, printed before it is
> asserted. `__all__` holds **17** names. The unit's `RAISES` lines are `business-logic-model.md`
> **:104** (`DriverError, BenchmarkError, ComparatorError, ImportBoundaryError`), **:367**
> (`FeatureAvailabilityError`) and **:478** (`BenchmarkError`). The difference is:
>
> **`{DriverError, BenchmarkError, ComparatorError, ImportBoundaryError, FeatureAvailabilityError}` — five.**
>
> **`AlignmentError` is NOT in that set**: it already exists in `__all__`, documented as *"A
> driver series did not align onto the hourly grid as its contract requires"* — which is this
> unit's own W-5 alignment condition, already covered.
>
> **Three of the five were not in Q2's scope**, and one of those three cannot be dispositioned
> here at all:
>
> - **`BenchmarkError` and `ComparatorError`** sit in the same position as the two the owner
>   ruled on — raised by this unit alone, no cross-unit meaning to reconcile. **Proposed
>   disposition: identical to Q2 = A.** Routed to the gate for an explicit yes or no rather
>   than folded in, because applying an owner's ruling to items they were not shown is a
>   widening this project has already had to correct once.
> - **`DriverError` is different and gets no proposal.** Its **scope is contested upstream**:
>   `business-logic-model.md`'s carried **Finding 9 (Major)** records that `domain-entities.md`
>   § 9's `DriverError` cell was annotated without being changed, so *"the artifact now
>   specifies both readings at once: `DriverError` both is and is not"* the exception for the
>   two alignment conditions that `AlignmentError` in fact owns. **Placing an exception whose
>   raise-conditions are self-contradictory would fix the wrong thing.** The declaration site
>   waits on that reconciliation.
>
> **This is the second consecutive unit where the question set undercounted the missing
> exceptions** — `inventory-and-registry` put two and the derivation found three. The
> derivation is cheap and the question set is not the place it belongs; recorded so the next
> unit derives before it asks.

## SD-E-03 — Narrowing the IRI residual: absent provenance fails (Q3 = A)

SEC-E-01 states the residual that survives **both** containment limbs, and this design does
not claim to close it:

> *"A value numerically derived from IRI, renamed so it carries no `iri_*` name, and stripped
> of its provenance stamp, defeats BOTH limbs… What bounds it is not a mechanism but a
> **person**."*

**The residual is a conjunction of two independent acts** — renaming, and stripping
provenance — and the second is addressable.

**Design — the provenance default is flipped.**

| | Limb 2 as specified upstream | Limb 2 as designed here |
|---|---|---|
| Admits a column when | its provenance does **not say IRI** — so an **absent** provenance is admitted | its provenance is **present and does not say IRI** |
| A stripped stamp | passes | **fails** |
| Producing side | not stated | **every value `04_build_external_products.py` writes carries a provenance stamp** |

**What this closes and what it does not, stated at the same volume.** It closes the
**stripping** act: a laundered value must now **forge** a provenance stamp rather than merely
delete one, which is a materially different and more deliberate act. **It does not close the
residual.**

> **⚠ FORGING IS CHEAP, AND SAYING OTHERWISE WOULD OVERSTATE THIS DESIGN** *(added 2026-09-02
> on adversarial finding 7, Minor)*. **Nothing validates a stamp's truthfulness.** The stamp is
> a field whose value the writer chooses, so "forge" here means *type a different string*, not
> defeat a signature. What the flip actually buys is narrower and worth stating exactly: an
> omission becomes a **commission**. A stripped stamp could be an accident of a copy step; a
> stamp that asserts a false origin is a written claim, attributable and reviewable, and it is
> the kind of thing a reader of the manifest can be asked about. **The barrier this adds is
> evidentiary, not cryptographic**, and no artifact should describe it as the latter.

A value renamed and recomputed from scratch, carrying a fabricated but plausible
provenance, survives. **No artifact may describe NFR-IRI-01 as fully enforced**, and the
honest reach of this design is unchanged in kind: it catches every accidental path and more
than one deliberate one, and it does not catch a determined one.

**Why fail-closed on absence is the right shape here specifically.** It is the same shape the
project already uses for an absent IGRF version and an absent `madrigalWeb_version` — *no
value* and *a value chosen for you* are both refused. Admitting a column because its
provenance is silent is inferring a grade from silence, which W-8's own reanalysed-value
block calls out by name: *"Inferring a grade from silence is not evidence."*

**Option B was declined explicitly, not passed over.** A **numeric fingerprint** —
correlating candidate feature columns against the IRI benchmark table — would reach the
rename-and-recompute case this design cannot. It is declined because VTEC and an IRI VTEC
estimate of the same cell and hour are **supposed to agree**, so the test's threshold would be
a new number invented beside frozen ones, on a quantity that correlates with the benchmark by
construction. It would also require the IRI benchmark to exist, and it is blocked.

> ### ⚠ THIS ADDS TO A CONTRACT THAT IS OWED, NOT AGREED
>
> **The feature matrix is `features-and-splits`' surface, not this unit's.** SEC-E-01 already
> records limb 2 as **one half of a two-half cross-unit contract** whose other half —
> *where the assertion sits, what it raises, and when it runs relative to the split* — **has
> not been stated**. This design **enlarges this unit's half**: every column now needs a
> provenance value, including columns no unit currently stamps.
>
> **This unit does not declare the contract satisfied from one side**, and the enlargement is
> **routed to the gate** alongside the contract it extends. What this unit can own outright is
> the **producing** half — that every value it writes carries a stamp — and that half is
> designed here without waiting.

## SD-E-04 — The IRI benchmark gate, and why three of its four limbs are ordering checks

W-6's four limbs are unchanged; what this section fixes is their **failure semantics** and
their evidence class.

1. **Generation refuses without a passing report** — `BenchmarkError`, naming the report and
   the missing pass.
2. **The tolerance's recorded timestamp precedes the comparison**, and generation refuses
   otherwise. **This is the limb that carries the requirement's weight.** *"A passing report
   exists"* is satisfiable by a report whose tolerance was chosen **after** the comparison
   ran — the exact failure *pre-declared* exists to prevent, and one no presence check can
   see. A frozen value plus an ordering is the only evidence class that separates *declared
   before* from *fitted after*, and it is the same mechanism `inventory-and-registry` adopts
   for retrospective split redesign and `evaluation-and-comparison` for the locked test.
3. **The report's content is asserted field by field**, not by presence of a report:
   the pinned package/build with exact version or commit; all model switches and the topside
   option; the altitude ceiling **stated explicitly as 2000 km**; units and output extraction;
   coordinate, time, solar and geomagnetic driver inputs **with confirmation that no driver is
   future-centered or unavailable at target time**; **5–10 samples** spanning sites, day and
   night, quiet and disturbed, validated against the **official IRI interface**; and the
   predeclared tolerance.
4. **The benchmark's own drivers appear in the same frozen availability matrix used for ML
   features**, each carrying observation timestamp, **publication timestamp OR — where the
   provider supplies none — the approved conservative convention plus the documented absence
   and an unverified-latency statement** (for F10.7 this is **D-25**:
   `availability_ts(median(D))` = **00:00 UTC on day D+1, never same-day** — an explicit
   project assumption, not a measured latency), release status and safe lag. **The matrix is
   `features-and-splits`' artifact; this unit states the obligation and does not own the
   row.**

   > **⚠ D-25 CARRIES ITS OWN UNGRANTED AMENDMENT, AND LIMB 4 LEANS ON IT** *(added 2026-09-02
   > on adversarial finding 4, Major — the first issue cited D-25 as though the convention were
   > settled and stated neither fact)*. `evidence/DECISIONS.md:1854` records D-25 verbatim: it
   > **"Requests, but does not take, a §15.2 amendment to TE §7.0A stage 4 and EV-12; until
   > granted, EV-12's F10.7 limb is unmet at G-04."** The convention limb 4 relies on for the
   > one series with **no provider publication timestamp** is therefore an approved
   > **assumption whose authorising amendment has not been granted**, and **EV-12's F10.7 limb
   > is unmet at G-04**. `DECISIONS.md:1648` lists that requested amendment among the open
   > holes leaving §18.3's first precondition only **partially met**. This also matters because
   > limb 4 **relaxes** `requirements.md` FR-P1-04-15's plain *"publication timestamp"*
   > requirement: the relaxation is the `CR-2026-08-22-EV-12` route, and that route is **not
   > yet closed**. Limb 4 is designed against D-25 as it stands; **nothing here treats the
   > amendment as granted or the limb as satisfiable today.**

**Why limb 4 has scientific consequence and is not bookkeeping.** *A benchmark fed
better-timed drivers than the model gets is not a benchmark.* This is what keeps the IRI
comparison fair, and it is the one limb whose violation would flatter the model rather than
break the run.

**On failure the implementation is NOT silently switched** (R-59). A switch made because the
first implementation failed validation is a scientific change wearing an operational
disguise, and TE §18.2 forbids it whichever costume it wears.

**Status.** Not run. `iricore` is TE §8.1 **required**; the validation gating its use has not
been performed; **no IRI benchmark exists**. **FR-P1-04-15 has no acceptance row** — the
blocking behaviour, the report's completeness and the predeclared tolerance are all unrowed,
and **designing them is not testing them**.

## SD-E-05 — The GIM comparator: one blocked obligation, one partial control, one residual

W-7's four obligations stand as one contract. This section states only what the design fixes.

| # | Obligation | Design | Status |
|---|---|---|---|
| 1 | Interpolation **bilinear in space, linear in time, with a longitude-rotation correction** | **Not specified here.** A §18.2 **Student-owned forbidden choice** (Q-15), **UNSET**. Comparator generation **refuses while it is unset** — the zero-TBD preflight's shape | ⛔ **BLOCKED** |
| 2 | One sample interpolation **hand-checked against the code**, EV-11 placing the hand-calculation **before** generation | The hand-check's **timestamp is asserted to precede** generation; generation **fails** otherwise. Same evidence class as SD-E-04's limb 2 | `Pending` |
| 3 | The comparison is **map-product-to-map-product** and *"cannot validate receiver-level station VTEC or serve as an independent target check"* | **Emitted by the reporting path itself**, not left to a writer. The **spatial-representativeness mismatch** is stated at the same point: part of any measured difference is a geometry and sampling artefact rather than skill | `Pending` |
| 4 | **Never tuned and then claimed independent** | **Partial control plus a named residual** (R-60 is authoritative): a **grep-class check** that no fitting, tuning, optimiser or parameter-search call appears in `gim.py`; and the report **stating no tuning occurred** with the independence claim **citing the overlap audit**. **⛔ The residual** — tuning performed **outside** `gim.py` and pasted in as a constant — is reached by no check and stays a **reporting-discipline obligation** | `Pending`, **residual open** |

**The `gim_network_overlap_flag` result is disclosed once the audit runs, and no independence
claim precedes it.** Disclosure is **mandatory**, not conditional on the result being
favourable. **The audit has not run.**

**Obligation 1's refusal is a mitigation that EXPIRES.** The moment Q-15 is decided, the
refusal stops covering obligation 4's disclosure. W-7 therefore keys the overlap-disclosure
control to **a GIM comparison artifact existing**, not to the refusal standing — and that
keying is preserved here rather than re-derived.

## SD-E-06 — Driver integrity, and the two-tier posture the exit-code gap violates

**The workspace fact, confirmed:** `scripts/audit_ec1_drivers.py:184` returns `0`
unconditionally; `:181` prints `missing=` and nothing reads it.

**REQ-ENG-9's closure is a TIER question, not an exit-code bug:**

| Condition | Tier | Behaviour |
|---|---|---|
| A missing month | **Completeness shortfall** | **Non-fatal.** A machine-readable manifest field naming **which** months are missing |
| A hash mismatch | **Integrity violation** | **Terminates** non-zero, naming the file and the violated expectation |

**Why not simply return non-zero on missing months.** That collapses the two-tier posture
`team.md` § Code Style fixes. A month absent from the provider is a fact to record; a hash
that does not match invalidates everything downstream of it. Making an ordinary partial
retrieval abort the run is how a guard gets worked around.

**Why the field names the months rather than counting them.** A count says something is
wrong; the list says what to do. This unit's outputs feed G-P1A's coverage decision, where
`inventory-and-registry` R-51 forbids *"an unattributed number"* — a bare count is that same
shape.

**Both injections are tested**, because REQ-ENG-9's criterion names both and they assert
**opposite** outcomes. A single test covers half the requirement and lets the other half
regress silently. **REQ-ENG-9 has no acceptance row.**

**The forecast-safety rules are unchanged and are restated only where the design adds
something.** The F10.7 81-day mean is **trailing**, ending at the safe-lagged day, and is
**proven as a property** — a test that shifts the input and asserts the output shifts with it,
which catches a centered variant *regardless of which API produced it*, where a code review of
one `pandas` call site would not. A centered mean **is a defect, not a fallback**. Missing
driver values carry forward **at most 3 hours**, then the row is **excluded**, with an
**injected four-hour gap** as the control. Every predictor is lagged to its **actual
availability timestamp** — Kp/ap3 **≥ 3 h**, Hp60/ap60 **≥ 1 h**, F10.7 at the
**previous-day observed** value. Driver series are **time-indexed only**: one value per epoch,
**identical across all three cells**, and a station performance difference is **never**
attributed to local forcing the dataset does not contain. **Dst's three restrictions stay
apart**: diagnostic and hindcast-only; **grades never mixed** within a series, with the 2022
grade recorded **before use**; and eligibility is a property of **the data**, not of intent.
**Never backfill from future final or definitive archived values** — *invisible in validation,
fatal on discovery* — and **record the release status of every driver, not only its lag**.
**No value is imputed for the F10.7 outage window** until the measured gap is recorded and
governed.

**The reanalysed-value check is BOUNDED, not closed**, and this design does not narrow the
bound. Four fields per series on the manifest — `release_status`, `retrieval_date`, the **full
provider product identity including any version suffix**, `sha256` — with the check asserting
their internal consistency **and** that the declared status matches the **contemporaneous**
grade the feature contract requires. Where a file carries no provenance column, the sanctioned
evidence is **that absence plus an explicit unverified-status statement** (D-25's shape, and
`CR-2026-08-22-EV-12`'s). **Inferring a grade from silence is not evidence.** F10.7 and Dst
remain **declared-status-only**, with substantive detection specified only for the two
**unretrieved** GFZ series. **No artifact may report this as closed.**

**The daily carry-forward composition is a G-04 freeze item and is NOT decided here.** D-21
binds the composition and no rule states what a **3-hour** bound means on a **24-hour** step;
the two readings differ by **20 of 24 scored rows per affected day, in all three cells**.
Until the Student freezes it, `configs/features.yaml`'s `carry_forward_composition` is `TBD`
and availability resolution **raises `FeatureAvailabilityError` and stops**.

## SD-E-07 — A revised external product is byte-identical, or explicitly divergent

**Design (SEC-E-05, Q2 = A upstream).** A re-run recomputes the SHA-256 of every external
product. On any difference it **records both product identities and both hashes and refuses
to overwrite**. This is `acquisition`'s § SEC-A-02 contract **adopted unchanged**, so the two
units that fetch external material do not diverge on the same question.

**Why it matters more here.** A re-issued CODE final GIM day that silently replaced the old
one would **change a published number with no trace** — the comparator is what the thesis
reports. **A stopped run awaiting adjudication is the intended cost**, and it will fire on
legitimate provider re-issues.

**The recorded identity includes the product's version or issue designation** where the
provider gives one, on the same reasoning that makes `acquisition` record provider version
suffixes: a divergence without both identities is uninterpretable, and drift is already
observed in this dataset (`g.002` versus `g.003`).

**NFR-REP-01 obligation, stated and not claimed as coverage.** Product hashes and the report
digests are **exact-equality classes** under §13.7 — they compare for equality, not tolerance,
and a mismatch must not be silently absorbed. NFR-REP-01 is
`fixtures-and-reproducibility`'s row; this artifact states an obligation against it.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Row primary owner | Status |
|---|---|---|---|---|
| **REQ-ENG-9** | SD-E-06 | ⚠ **NO ACCEPTANCE ROW** | — | untested |
| FR-P1-04-3 | SD-E-06 | **WS-11** *(row restored 2026-09-02 on adversarial finding 5, Minor — the first issue wrote R-57a's injected-four-hour-gap control into the acceptance-row cell and so dropped the row the map carries)*; R-57a's control is the mechanism, not the row | `features-and-splits` | `Pending` |
| **FR-P1-04-4** | SD-E-06 | ⚠ **NO ACCEPTANCE ROW** | — | untested |
| FR-P1-04-9 | SD-E-05 | WS-09, TA-12 | **`external-products`** (WS-09); `models-and-baselines` (TA-12) | `Pending` |
| **FR-P1-04-15** | SD-E-04 | ⚠ **NO ACCEPTANCE ROW** | — | untested |
| FR-P1-04-17 | SD-E-06 | **TA-36** | `features-and-splits` | ⚠ **`Pending` — approved, never run** |
| **FR-P1-04-18** | SD-E-05 | ⚠ **NO ACCEPTANCE ROW** | — | untested |
| FR-P1-04-1 | SD-E-01, SD-E-03 | WS-10, TA-07 | — | `Pending` — ⚠ **control NOT WRITTEN** |
| NFR-IRI-01 | SD-E-01, SD-E-03 | WS-10, TA-07 | — | `Pending` — ⚠ **control NOT WRITTEN** |
| NFR-LEAK-01 | SD-E-03, SD-E-06 | TA-11 | `features-and-splits` | `Pending` |

**Derived and printed.** **7** design sections (SD-E-00 … SD-E-07 is eight headings, of which
SD-E-00 is a state record rather than a design section). **10** coverage rows, counted from
the table above — the **7** the `functional-design` map fixes for this unit, plus
FR-P1-04-1, NFR-IRI-01 and NFR-LEAK-01, matching `nfr-requirements`' corrected 10-row set with
**empty set difference in both directions**. **4** rows with no acceptance row (REQ-ENG-9,
FR-P1-04-4, FR-P1-04-15, FR-P1-04-18), re-derived by counting blank acceptance cells above
rather than read off the map. **0** rows claimed satisfied. **2** values left `TBD — freeze
gate` by this unit (the `iricore` configuration; the GIM product version), **plus one UNSET
§18.2 Student choice** (FR-P1-04-18's interpolation rule) and **one `TBD` G-04 freeze item**
(`carry_forward_composition`). **0** new dependencies. **1** amendment owed (R-55: boundary
contracts for `iri.py`, `gim.py`, `spaceweather.py` as one change record).

**Two status cells are corrected downward from `nfr-requirements`, and the correction is
disclosed rather than left to be noticed.** FR-P1-04-1 and NFR-IRI-01 read *"`Pending` — test
written, UNEXECUTED"* upstream; both now read **"control NOT WRITTEN"**, because
`tests/test_iri_denial.py` does not exist (§ SD-E-00). This is the only kind of coverage-cell
change that needs no argument for its direction — it removes a claim rather than adding one —
but it is stated because a cell that changes between stages is exactly what this project has
had to correct before.

**Why the other eleven `FR-P1-04-*` IDs are absent.** `requirements.md`'s FR-P1-04 space is
`{1…18}`, eighteen IDs. This unit carries `{1, 3, 4, 9, 15, 17, 18}` — seven. The set
difference is `{2, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16}`, eleven IDs, and they are the **feature
contract itself** — `features-and-splits`' space, not this unit's. The `functional-design` map
fixed this unit's set and reconciled it upstream; FR-P1-04-1 was added at `nfr-requirements`
because SEC-E-01 reproduces its text on both limbs while citing only NFR-IRI-01.

**Two NFRs are named as obligations and deliberately given no coverage row**: **NFR-REP-01**
(§ SD-E-07 — product hashes and report digests are §13.7 exact-equality classes) and
**NFR-DET-01** is not claimed at all, because nothing this unit produces is seeded. Stating an
obligation against a requirement is not covering it, and the distinction is made here so a
later reader does not read either as a silent omission.

## Assumptions & Open Questions

- **[Q1 / SD-E-01 — OPEN, routed to the gate]** **The §18.3 preflight is another unit's row, and this design depends on it.** `requirements.md` **FR-WS-7** (line 462) already carries the criterion — *"zero unresolved P0 fields and no failing critical test"*, with the **ten critical tests enumerated** and **IRI-free denial** among them — and `components.md:63` assigns FR-WS-7 to `config.py`, `foundation`'s module. A skip is not a pass, so a skipped check fails FR-WS-7 by definition. **What is owed is that `foundation`'s assertion reads the structured skip reason rather than counting non-failures**, and that dependency is stated as owed, not assumed satisfied. *(Corrected 2026-09-02 on adversarial finding 2, Major: the first issue called this "a reading this stage fixes", cited nothing, named no owner and routed it nowhere — while Q2's and Q3's smaller enlargements were each routed. Q1's option-A impact line carried the same overstatement, and the answer was given on it.)*
- **[Q1 / SD-E-01 — the domain, the two sets, and the allowlist]** The candidate-importer set is the **complement of TE §12's two allowlisted paths**, over a domain of **`.py` files and `.ipynb` code cells** — never a directory list. The **walk includes `__init__.py`; only the cardinality count subtracts it**, which matters because five `src/` packages hold nothing else today. **`tests/*` is NOT allowlisted**: the previous revision granted it on a reading of WS-10 that does not hold (WS-10 injects an `iri_*` **field**, a data act, and `test_phase_boundary.py` shows an import boundary can be asserted by parsing rather than importing), and `component-dependency.md`:34's blanket row is contradicted at `:38`. **The blanket row is routed to the gate**, not followed. *(Corrected 2026-09-02 on the second-redo pass's findings 1, 2 and 5.)*
- **[Q1 / SD-E-01 — OPEN, routed to the gate: the `component-dependency.md` blanket row]** `:34`'s `tests/*` row reads `yes` in **all seven columns** and is contradicted **four lines below** at `:38` by that artifact's own *"exactly two importers… Everything else is forbidden"*, and by `requirements.md`:370. **This design follows TE §12's two paths and does NOT allowlist `tests/*`.** **Owner: the project decision owner**, as a discrepancy in an approved application-design artifact — either the row is a blanket convenience that does not govern this column, or it is wrong. If a test is ever found to genuinely require the import, that is a **change record against TE §12**, not a reading this stage may adopt. *(Routed with an owner 2026-09-02 on the terminal pass's finding 4: the previous revision withdrew the grant correctly but tagged and owned the discrepancy nowhere.)*
- **[Q2 / SD-E-02 — OPEN, routed to the gate]** **The missing-exception set is five, and Q2 named two.** `{DriverError, BenchmarkError, ComparatorError, ImportBoundaryError, FeatureAvailabilityError}`, derived against `config.py`'s 17-name `__all__`. **`BenchmarkError` and `ComparatorError`** carry a proposed disposition identical to Q2 = A, for an explicit yes or no. **`DriverError` carries none**: its raise-conditions are self-contradictory upstream (carried **Finding 9**, Major — `domain-entities.md` § 9 annotated without being changed, so it *"both is and is not"* the exception `AlignmentError` in fact owns). **`AlignmentError` already exists** and is not in the set.
- **[Q3 / SD-E-03 — OPEN, routed to the gate]** The flipped provenance default **enlarges this unit's half of a two-half contract whose other half has not been stated**. `features-and-splits` owes where the assertion sits, what it raises, and when it runs relative to the split — now over **every** column, not only `iri_*`-named ones. **This unit does not declare the contract satisfied from one side.**
- **[Q3 — the residual is NOT closed]** A value renamed and recomputed from scratch, carrying a fabricated provenance, survives both limbs and this narrowing. **No artifact may describe NFR-IRI-01 as fully enforced.**
- **[DISC-E-1 — what the check does TODAY, derived not asserted]** The **target limb is empty** (`iri.py`, `gim.py` absent); the **risk-surface limb is POPULATED — 18 files walked, 12 counted**. So the check is **live, not inert**: it reaches **clause 4** and reports **`skipped`, naming the target limb**, over 18 files it really would inspect. *(Corrected 2026-09-02 on the second-redo terminal pass's finding 1, Critical: the superseded bullet said it "cannot fail today" and DISC-E-1 claimed "two independent causes of vacuity" — an inference the earlier, narrower candidate set supported, carried forward without being re-derived when the set widened.)*
- **⚠ [SD-E-00 — the largest open item in this unit]** **`tests/test_iri_denial.py` does not exist.** WS-10 requires the denial test to **fail on a deliberately injected `iri_*` field**, and TE §18.3 names IRI-free denial among its ten critical items. Upstream records it as written; it is not.
- **Carried — `src/external` has no contract block for any of its three modules** (R-55). One amendment owed, part of five across three units.
- **Carried — IRI generation is blocked** on R-59's pre-declared validation, which has not run. **No IRI benchmark exists.**
- **Carried — FR-P1-04-18's interpolation rule is UNSET**, a §18.2 Student-owned forbidden choice (Q-15). Comparator generation refuses while it stands, and **that refusal expires the moment Q-15 is decided** — which is why the overlap-disclosure control keys to a comparison artifact existing, not to the refusal.
- **Carried — the `gim_network_overlap_flag` audit has not run.** No independence claim may precede it, and disclosure is mandatory whatever the result.
- **Carried — obligation 4's residual**: tuning performed outside `gim.py` and pasted in as a constant is reached by no check.
- **Carried — the reanalysed-value check is bounded, not closed** for F10.7 and Dst, both declared-status-only. **No artifact may report it as closed.**
- **Carried — `carry_forward_composition` is a G-04 freeze item**, `TBD`, differing by 20 of 24 scored rows per affected day across all three cells. Availability resolution raises and stops.
- **Carried — TA-36 is `Pending`**: approved, never run, never cited as a result. This unit holds data production and upstream evidence; `features-and-splits` holds enforcement and the primary test.
- **Carried — the Python interpreter present is 3.14.7, off the governed 3.11 pin.** Nothing it runs is governed evidence.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, authorises writing a module, or claims a gate, acceptance row or test as discharged.

---

## Review

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-02T05:08:29Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | `security-design.md` § SD-E-01 part 1; § DISC-E-1; `logical-components.md` E-1 limb 1 | **The skip predicate covers one of the two causes of vacuity the artifact itself names.** DISC-E-1 states the scan is vacuous because *both* "every module the import allowlist protects (`iri.py`, `gim.py`)" **and** "every module that could violate it (`src/features/*`, `src/models/*`, and any other importer)" are absent. SD-E-01 part 1 keys the skip on the first cause only: *"when neither `src/external/iri.py` nor `src/external/gim.py` exists, the check raises a skip"*. § Failure domains records that W-10 **permits before G-09** "module structure, interfaces, placeholder CLI definitions" — so `iri.py`/`gim.py` may legitimately exist as stubs while `src/features/` and `src/models/` still hold only `__init__.py` (verified on disk today). In that state the skip does not fire, the scan returns **`passed`**, and it has verified nothing — the exact vacuous pass § SD-E-01 exists to prevent, now green rather than skipped. The artifact's own guard sentence — *"This section changes what the check reports, never what it checks"* — is why the reporting change cannot reach the second cause. | Key the skip on the vacuity condition, not on target existence: report `skipped` whenever the scan's *candidate importer set* is empty (no module outside the allowlist under `src/` and `scripts/` beyond `__init__.py`) **or** neither protected target exists. State the predicate as a machine-readable condition so the §18.3 consumer reads the same test the check applies. |
| 2 | Major | `security-design.md` § SD-E-01 part 3, § Assumptions [Q1]; `logical-components.md` E-1 DISC-E-1 box, § Assumptions | **The design's declared load-bearing half is unowned and unrouted, and a passed contract already covers it — uncited.** Part 3 asserts *"the §18.3 preflight reads 'no failing critical test' as 'no critical check unmet'"* and calls it *"a reading this stage fixes"* / *"the option"*. **`requirements.md` FR-WS-7 (line 462) already states the stronger acceptance criterion verbatim: "all ten named tests **passing**"** — which a skip fails by definition. FR-WS-7 is owned elsewhere (`application-design/components.md` line 63 assigns it to `config.py`; the story map records `foundation`, row TA-23). Neither artifact cites FR-WS-7, and Q1's option-A impact line frames the cost as *"a definition this stage would be fixing"* without it — the owner chose A on a framing that understated what already exists and overstated this unit's standing. Contrast the artifact's own discipline: Q2's and Q3's cross-unit enlargements are each explicitly **"routed to the gate"**; Q1's — the largest of the three, and the one the design calls load-bearing — is routed nowhere, names no owner, and raises no amendment. | Cite `requirements.md` FR-WS-7 and its "all ten named tests passing" criterion in § SD-E-01, state that the preflight is another unit's row (TA-23), and route part 3 to the gate as an explicit item against that owner — the same treatment SD-E-02 and SD-E-03 already receive. |
| 3 | Major | `logical-components.md` § Failure domains (E-2 row; "Not one of the three announces itself"); contradicted by `logical-components.md` E-2 (W-8 paragraph) and `security-design.md` § Scope note (Reliability row), § SD-E-06 (tier table) | **Self-contradiction on the observation the section calls "the finding".** § Failure domains marks E-2 "Failure announces itself? **No**" and asserts *"The three siblings each had at least one component that raises and stops … **This unit has none.**"* E-2's own body states the opposite three times: *"a **hash mismatch terminating** non-zero and naming the file and the violated expectation"* (E-2), *"a **hash mismatch terminates** naming the file and the violated expectation"* (§ Scope note), *"**Terminates** non-zero, naming the file and the violated expectation"* (§ SD-E-06 tier table). That is precisely the build-time-integrity class the sentence cites as the sibling contrast. The contradiction is load-bearing, not cosmetic: the Q4 rationale rejects the "how the failure surfaces" axis on the ground that *"the latter would have produced one box"* — untrue if E-2 contains a raise-and-stop control the other two lack. | Restate the claim at the resolution the evidence supports: every *silent* failure mode in this unit is silent, and E-2 additionally carries one announcing control (the integrity tier), which the other two components lack. Then re-argue Q4's rejection of the surfacing axis against that corrected fact, or record that it survives for a different reason. |
| 4 | Major | `security-design.md` § SD-E-04 limb 4; `logical-components.md` E-3 limb-4 box | **D-25 is presented as the sanctioned alternative without its own recorded residual.** Limb 4 admits, where a provider supplies no publication timestamp, *"the approved conservative convention plus the documented absence and an unverified-latency statement (for F10.7 this is **D-25**)"*. This relaxes `requirements.md` FR-P1-04-15's acceptance criterion, which requires the benchmark's drivers to carry "publication timestamp" plainly. `evidence/DECISIONS.md` line 1854 records that D-25 **"Requests, but does not take, a §15.2 amendment to TE §7.0A stage 4 and EV-12; until granted, EV-12's F10.7 limb is unmet at G-04."** Neither artifact states that the authorising amendment is ungranted or that EV-12's limb is unmet — on the one limb the artifact itself calls *"the one with scientific consequence"*, and against `project.md`'s standing rule to enumerate every open gate. | Add the ungranted-amendment status and EV-12's unmet F10.7 limb to limb 4 and to the banner's open-item list, at the same volume as the other carried blockers. |
| 5 | Minor | § Requirement coverage, FR-P1-04-3 row (both artifacts) | The acceptance-row cell reads "via R-57a's injected-four-hour-gap control" where the `functional-design` map (`business-logic-model.md` line 744) records the acceptance row as **WS-11**. A control is not an acceptance row, and the substitution is undisclosed while two other cell changes (FR-P1-04-1, NFR-IRI-01) are disclosed at paragraph length. Inherited from `nfr-requirements` (`security-requirements.md` line 210), not introduced here — but this stage re-derived the map's 7 and did not reconcile it. | Restore WS-11 in the acceptance-row cell (keeping R-57a's control as the mechanism), or state the divergence from the map with the same disclosure the other two cells receive. |
| 6 | Minor | `logical-components.md` § "Decomposition of … 7 design sections", SD-E-02 line | The 5/2/2 split maps SD-E-02 as "the exceptions split across all three" and names **four** — `ImportBoundaryError` → E-1, `FeatureAvailabilityError` → E-2, `BenchmarkError` and `ComparatorError` → E-3. **`DriverError`, the fifth member of the set the artifact spends a call-out box deriving, is placed in no component**, and its raise site W-1 has no component either. The arithmetic (5 + 2 = 7) is unaffected; the completeness of the placement is not. | Name `DriverError` in the SD-E-02 line as deliberately unplaced pending Finding 9's reconciliation, so its absence reads as the recorded refusal it is rather than as an omission. |
| 7 | Minor | § SD-E-03 | The flipped default makes a provenance value **required** but nothing in the design gives it a truthfulness property — no check compares a stamp against what produced the column. The artifact says a laundered value must now *"forge a provenance stamp rather than merely delete one, which is a materially different and more deliberate act"*; that is true of intent and false of effort, and the design never states that a stamp is unvalidated. The residual it *does* disclose (rename-and-recompute) is stated well. | Add one sentence: a provenance stamp is asserted present and non-IRI, never verified true; the control raises the deliberateness of the act, not its cost. |

### Checks actually run

| Check | Method | Result |
|---|---|---|
| `produces_kinds` yields exactly two artifacts for `library` | read the stage definition's `produces` / `produces_kinds` frontmatter, lines 14–24 | **Confirmed independently.** `security-design` carries no `produces_kinds` entry → applies to all kinds; `logical-components: [service, ui, library]` → applies; `performance-design: [service, ui]`, `scalability-design: [service]`, `reliability-design: [service]` → excluded. Two artifacts, correct |
| `tests/test_iri_denial.py` absent; `tests/` holds exactly the six named modules | `ls -1 tests/` | **Confirmed.** Exactly `test_acquisition_window.py`, `test_locked_test_guard.py`, `test_merge_script_restricted_reads.py`, `test_phase_boundary.py`, `test_release_contract.py`, `test_release_hashes.py` (plus `__pycache__`). No `test_iri_denial.py`. The "runs **against** this unit" framing is honest, not overstated |
| Python 3.14.7, off the 3.11 pin | `python --version` | **Confirmed.** `Python 3.14.7` |
| `src/external/` holds `__init__.py` only, 24 bytes; `features`/`models`/`evaluation`/`gnss` likewise; `src/` six packages, one populated | `ls -1 src/*/`, `wc -c` | **Confirmed on every limb**, including the 24-byte figure |
| `scripts/04_build_external_products.py` and `configs/` absent | `ls -1 scripts/`, `ls -d configs` | **Confirmed.** `scripts/` holds `audit_ec1_drivers.py` and `merge_coverage_year.py` only; `configs` does not exist |
| `audit_ec1_drivers.py:184` unconditional `return 0`; `:181` prints `missing=` | `sed -n '170,190p'` | **Confirmed exactly.** `:184` is `return 0` closing `main()`; `:181` is the f-string carrying `missing={info.get('missing_days')}`; nothing reads it into an exit code |
| "277 passed / 2 skipped" | `python -m pytest tests/ -q` | **Confirmed exactly**: `277 passed, 2 skipped in 4.29s` |
| §18.3 criterion text and its ten named critical items; "IRI-free denial" among them | `requirements.md` line 462 (FR-WS-7) | **Confirmed.** Criterion quoted correctly; ten items enumerated; IRI-free denial is the third. **Also surfaced the uncited "all ten named tests passing" acceptance clause — finding 2** |
| Five-not-two exception derivation | `grep -n RAISES business-logic-model.md`; `config.py` `__all__` | **Confirmed.** Three `RAISES` lines at **:104**, **:367**, **:478**, union `{DriverError, BenchmarkError, ComparatorError, ImportBoundaryError, FeatureAvailabilityError}` = **5**; `__all__` holds exactly **17** names, none of the five among them |
| `AlignmentError` already covers W-5's alignment condition | `config.py:141-142` docstring; `business-logic-model.md` W-5 (line 405ff) | **Confirmed.** Docstring quoted verbatim and correct. W-5's limbs 1–2 (Kp outside its 3-h interval; Dst shifted to a neighbouring hour) are alignment conditions; limb 3 is a static scan, not a runtime raise, as Finding 9's own annotation states. Excluding `AlignmentError` from the missing set is right |
| Refusing to disposition `DriverError` — justified or evasion? | Finding 9 text, `business-logic-model.md` :1173–1195 | **Justified, not an evasion.** Finding 9 is MAJOR, carried, open; the quoted phrase *"both is and is not"* is accurate; `domain-entities.md` § 9's `Raised when` cell is the column 3.5 implements from and still carries the superseded conditions. Placing the declaration now would fix the wrong thing, as stated |
| Q3's cost stated at the right volume? | § SD-E-03 call-out; § Assumptions (both artifacts) | **Adequate.** The enlargement is in a bordered call-out, explicitly routed to the gate, and repeated in both artifacts' Assumptions. Not buried. (Finding 7 concerns a different omission) |
| 7 design sections | `grep -c "^## SD-E"` | **Confirmed.** 8 `SD-E-*` headings; SD-E-00 is a state record → 7 design sections |
| 10 coverage rows in each artifact, identical membership | ID extraction + `comm -23` / `comm -13` | **Confirmed. Empty in both directions.** 10 rows each: REQ-ENG-9, FR-P1-04-1, -3, -4, -9, -15, -17, -18, NFR-IRI-01, NFR-LEAK-01 |
| 4 rows with no acceptance row | blank-cell count, both tables | **Confirmed.** REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18 — matching `business-logic-model.md` :751 and :866–871 |
| FR-P1-04 set difference `{2,5,6,7,8,10,11,12,13,14,16}` = 11 | ID enumeration over `requirements.md` | **Confirmed.** Space is exactly `{1…18}`, 18 IDs; unit carries 7; difference is the 11 IDs listed, exactly |
| 5/2/2 decomposition | manual re-derivation against § SD-E headings | **Arithmetically confirmed** (5 single-component + 2 shared = 7). See finding 6 for the placement gap |
| 3 components | `grep -n "^### E-"` | **Confirmed.** E-1, E-2, E-3 |
| "7 requirements the `functional-design` map fixes" | `business-logic-model.md` § Requirement-to-workflow map | **Confirmed.** Map carries exactly the 7; :751 states "7 requirements, 4 without an acceptance row"; :864 records the set difference as empty both directions |
| No satisfaction or discharge claim; freeze-gate values unnamed | grep for `iricore` version, GIM product issue, `2000 km` across both artifacts | **Confirmed clean.** No version pin, no switch set, no product issue is named. `2000 km` appears only as a quotation of FR-P1-04-15's own required report field (`requirements.md` :386), never as a decision. FR-P1-04-18's interpolation rule is stated UNSET. `carry_forward_composition` left `TBD`. **0 rows claimed satisfied**; no gate, acceptance row or test claimed passing; nothing authorises a module write |
| Q1 recommendation self-serving or under-argued? | `nfr-design-questions.md` Q1 | **Not self-serving.** Options B/C/D are argued on their merits, B is named as the reviewer's fallback, and A's cost is disclosed in the recommendation itself. **But under-argued on one point** — the framing omits FR-WS-7's existing criterion (finding 2) |

### Validation tool results

| Tool | Result | Interpretation |
|---|---|---|
| — | The stage definition declares **no** validation tools | No tool output to interpret. Every check above was run by hand against the workspace, the passed shared contracts, and the declared upstream |

### Coverage limits — what was NOT checked, and why

- **"One amendment owed (R-55), part of five across three units."** The "five across three units" half rests on sibling units' construction artifacts and is **out of read-scope**. R-55's own limb (no boundary block for `iri.py`, `gim.py`, `spaceweather.py`) was confirmed against `application-design/component-methods.md`; the roll-up figure is **unverified** and stands as this unit's own characterisation.
- **The three sibling `logical-components.md` criterion comparisons** (failure consequence, enforcement timing, how the failure reaches a human), the **`governance-guards` R-23/R-24/R-28** and **`inventory-and-registry` R-51** citations, and the claim that `inventory-and-registry`'s Q2 put two exceptions while the derivation found three: all out of read-scope, all **unverified**. They are this unit's characterisation of other units' work and should be read as such. Note that the artifacts are careful about this in one place (§ SD-E-01's parenthetical that the static/run-time asymmetry is "W-3's own terms, not a paraphrase of `governance-guards` R-24"), which is the right instinct and should be the pattern everywhere such a comparison appears.
- **`domain-entities.md` § 9 line 318** was read only through Finding 9's verbatim quotation inside `business-logic-model.md`, not opened directly.
- **The upstream `nfr-requirements` banner claims that § SD-E-00 supersedes** were checked only where this stage relies on them; `security-requirements.md`'s and `tech-stack-decisions.md`'s own internal consistency was not re-reviewed.

### Summary

The workspace evidence in § SD-E-00 and DISC-E-1 is **accurate on every limb I could test** — the six test modules, the missing `test_iri_denial.py`, Python 3.14.7, the empty `src/` packages, the absent `configs/` and stage script, line 184's unconditional `return 0`, even the 277/2 suite figure — and every printed count re-derives correctly, including the two coverage tables' empty set difference in both directions. Nothing is claimed satisfied, no freeze-gate value is filled, and the artifact volunteers a correction that runs against itself. That is a high standard of evidence.

The verdict turns on the design itself. **SD-E-01's control does not cover the failure condition SD-E-00 diagnosed**: DISC-E-1 names two causes of vacuity and the skip predicate reaches one, so a stub file — which W-10 explicitly permits before G-09 — restores the vacuous pass under a green light (finding 1). And the half the artifact calls *"the option"* is an obligation on FR-WS-7's owning unit, and FR-WS-7 already carries the stronger "all ten named tests passing" criterion yet is cited nowhere, while the two smaller cross-unit enlargements are both properly routed to the gate (finding 2). Add the announce-itself self-contradiction that undercuts Q4's own rationale (finding 3) and D-25's unstated ungranted amendment on the limb the artifact calls scientifically consequential (finding 4), and the design is not yet one a developer could build the containment control from without asking which of two incompatible vacuity conditions it is meant to catch.

---

## Remediation of the iteration-1 findings — 2026-09-02

All seven findings addressed. Each repair was swept for **every representation** of the
corrected fact across both artifacts, not only the site the finding named.

| # | Sev | Repair | Sites changed |
|---|---|---|---|
| 1 | **Critical** | The vacuity predicate now has **two limbs**, matching the two causes DISC-E-1 names: a **target side** (at least one of `iri.py`, `gim.py` exists) and a **risk-surface side** (at least one module beyond `__init__.py` under `src/features/` or `src/models/` — the two trees FR-P1-04-1 and TE §12 name as forbidden importers). The check reports `passed` only when **both** are populated; otherwise it skips, naming **which** limb was empty. The stub scenario W-10 permits is now covered. | `security-design.md` § SD-E-01 part 1 (predicate table + correction box), part 2 (machine-readable reason); `logical-components.md` E-1 DISC-E-1 box, § Assumptions |
| 2 | Major | **The §18.3 reading is not this stage's to fix, and is no longer claimed as such.** `requirements.md` **FR-WS-7** (line 462) already carries the criterion with the **ten critical tests enumerated** and **IRI-free denial** among them; `components.md:63` assigns FR-WS-7 to `config.py`, `foundation`'s module. A skip is not a pass, so it fails FR-WS-7 by definition. What this unit owns is the **reporting contract**; what it depends on — that `foundation`'s assertion **reads the structured skip reason** rather than counting non-failures — is now **routed to the gate**, on the same footing as SD-E-02's and SD-E-03's enlargements. | `security-design.md` § SD-E-01 part 3 (rewritten with correction box), the risk box, § Assumptions `[Q1]`; `logical-components.md` E-1 DISC-E-1 box, § Assumptions |
| 3 | Major | The headline claim is **narrowed, not dropped**: *no component's **characteristic** failure announces itself*. E-2's hash-mismatch tier **is** loud, and it is an integrity check on **inputs** — a fact about a file, not about whether the future leaked into a forecast origin. **Q4's rejection rationale is corrected with it**: *"would have produced one box"* is **too strong and withdrawn** (the axis yields two), and the rejection now stands on the narrower ground that those two boxes would split E-2's hash check from E-2's own leakage rules. | `logical-components.md` § Failure domains (claim + correction box + Q4 rationale), the E-2 failure-domain row |
| 4 | Major | **D-25's ungranted amendment is stated at the volume of the other carried blockers.** `evidence/DECISIONS.md:1854`: D-25 *"Requests, but does not take, a §15.2 amendment to TE §7.0A stage 4 and EV-12; until granted, EV-12's F10.7 limb is unmet at G-04."* `:1648` lists it among the holes leaving §18.3's first precondition **partially met**. Limb 4's relaxation of FR-P1-04-15's plain *"publication timestamp"* rests on a route that is **not closed**. | `security-design.md` banner, § SD-E-04 limb 4 (new box); `logical-components.md` E-3 limb-4 box, § Assumptions |
| 5 | Minor | **FR-P1-04-3's acceptance row restored to `WS-11`** at both coverage tables. The first issue wrote R-57a's injected-four-hour-gap control into the acceptance-row cell, which is the **mechanism**, not the row. | `security-design.md` coverage table; `logical-components.md` coverage table |
| 7 | Minor | **The provenance flip's barrier is restated as evidentiary, not cryptographic.** Nothing validates a stamp's truthfulness, so "forge" means *type a different string*. What the flip buys is that an **omission becomes a commission** — a written, attributable claim rather than a plausible copy-step accident. | `security-design.md` § SD-E-03 (new box) |
| 6 | Minor | **`DriverError`'s absence from the 5/2/2 split is registered as deliberate.** It is assigned to no component because which one it belongs to depends on the reading carried **Finding 9** leaves unresolved; assigning it would encode a reading this stage explicitly refused to take. `AlignmentError`, which already exists, is placed in E-2 and is unaffected. | `logical-components.md` § decomposition (new box), § Assumptions |

**One thing was deliberately NOT changed.** Finding 2 observes that **Q1's option-A impact
line** carried the same overstatement the artifacts did, and that the owner answered on that
framing. **The questions file is a human-signed record** — it carries a receipted Consolidated
Summary Confirmation — and `project.md` forbids editing one to bring it into line with a later
derivation. The correction is recorded in the artifacts this stage owns, and the **ruling is
routed to the approval gate**: the answer stands, and what changes is that the dependency it
implied is now named, owned and routed.

**No count was adjusted to fit.** Every figure the repairs touched — 7 sections, 10 rows per
table, 4 unrowed, 3 components, the 5/2/2 split, the 11-ID FR-P1-04 difference — was
**re-derived from the corrected artifacts** and is unchanged.

*(Rows 6 and 7 above were relabelled 2026-09-02 on the terminal pass's Minor finding 3: the
two Minors were cited under each other's numbers here and in both correction boxes. Iteration-1
finding **6** is the `DriverError` placement gap; finding **7** is the unvalidated provenance
stamp. Corrected at all three sites.)*

---

## Remediation of the TERMINAL-pass findings — 2026-09-02, owner-directed redo

The terminal pass returned **NOT-READY** with 1 Critical, 1 Major and 2 Minors, and its
iteration budget was spent — so under the stage protocol the findings would have reached the
approval gate unfixed. **The project decision owner directed a redo instead**, at the choice
put to them after that pass. The two artifacts were revised, which invalidates the terminal
receipt and returns the unit to review.

| # | Sev | Repair |
|---|---|---|
| 1 | **Critical** | **The iteration-1 repair had reopened the defect in a broader form, and both halves of that are fixed.** (a) The risk-surface limb is widened from *"`src/features/` or `src/models/`"* to **the allowlist complement the scan already walks** — every module beyond `__init__.py` under `src/` or `scripts/` outside `scripts/04_build_external_products.py` and `src/evaluation/`. `requirements.md`:370 states the boundary *"as an allowlist, not a denylist"* and names `src/data/`, `src/gnss/`, a training script and a notebook as violating it identically; DISC-E-1's own *"and any other importer"* had said so too, and the repair had dropped it. (b) A **precedence rule** is added, because a vacuity condition without one is not a control: **a detected reachability path fails regardless of either limb**. Under the superseded text, a violation found in `src/data/` — three real modules today — would have reported `skipped` and satisfied §18.3. |
| 2 | Major | **The narrowed announce-itself claim is swept to where the fact lives**, not only where the previous finding pointed. `logical-components.md`'s § The boundary criterion (`:61`) and its § decomposition here-only list both asserted the withdrawn form; both now carry *every component's **boundary** failure is silent, and E-2 additionally carries one loud input-integrity path*. **The Q4 justification is re-argued against the corrected fact**: the surfacing axis yields **two** boxes here, not zero, so the rejection no longer rests on "barely varies" — it rests on those two boxes splitting E-2's hash check from E-2's own leakage rules. |
| 3 | Minor | Iteration-1 findings **6** and **7** relabelled at all three sites (see the note above). |
| 4 | Minor | **The "no static check can judge which modules are real" claim is withdrawn as an overstatement** that closed off a cheap fix. Replaced with a **required symmetry**: a `passed` outcome carries the same machine-readable scan-scope evidence the skip carries — the candidate-importer set actually walked, by count and by path — so a reader can see a `passed` reached over three modules rather than thirty, with no check having to make that judgment. |

**What this episode is recorded as, because the pattern is the point.** The Critical was not a
missed check; it was a **repair that narrowed a set while appearing to tighten it**. The
two-tree list came from the rule's own example sentence rather than from the rule, and the
artifact being repaired already carried the correct wider phrase three paragraphs earlier. A
sweep for a corrected fact would not have caught it, because the defect was in the **new** text.
The mechanical form that would have: **when a repair narrows a set, print the set it narrowed
from and set-difference it against the rule's own statement of scope before writing.**

---

## Remediation of the POST-REDO pass — 2026-09-02

The post-redo pass returned **NOT-READY** (1 Critical, 1 Major, 3 Minor) on iteration 1 of a
fresh budget, so one review pass remains.

| # | Sev | Repair |
|---|---|---|
| 1 | **Critical** | **The terminal Critical had been repaired in `security-design.md` and left standing in `logical-components.md`** — in E-1's DISC-E-1 box, the exact site the terminal finding had named. That box still specified the superseded **denylist** predicate (`src/features/` or `src/models/`) with no precedence rule, so the set specified **two incompatible predicates**, with the narrow one sitting in the component definition an implementer builds from. The box now carries the **allowlist complement** and the **ordered outcome switch** in full. Two bookkeeping claims that asserted otherwise — this artifact's re-save banner and terminal-remediation row 1 — are true as of this repair rather than before it. **This is the second time in this unit that a repair landed in one artifact and not its sibling.** |
| 2 | Major | **The complement omitted notebooks.** It was scoped *"under `src/` or `scripts/`"*; `requirements.md`:370 — the authority the repair cites — names *"a training script **or a notebook**"* as violating the boundary identically, `business-rules.md`:318 carries **`Import iri from a notebook → fails`** as a required R-56 negative control, and `notebooks/madrigal_phase1_coverage_audit.ipynb` **exists on disk**. `notebooks/` is now in the walked set, at all four sites that state the scope. **A widening that stopped one directory short of the rule it was widening to match** is the third instance this stage has recorded of a repair narrowing a set while appearing to broaden it. |
| 3 | Minor | **The skip payload and the `passed` payload are now specified as the same structure** — the candidate-importer set actually walked, by count and by module path, plus the empty-limb identifier on a skip. The earlier symmetry claim named a payload for one outcome and not the other, which made it unbuildable. |
| 4 | Minor | **Clause 1's behaviour with an empty target limb is determined**: the walk matches **module paths by name**, not by file resolution, so a violation is detectable with no target file present — which is exactly the state a partly-built tree produces — and clause 1 fires ahead of the skip. |
| 5 | Minor | **Two blockquotes that broke mid-sentence are closed.** § SD-E-03's box had severed *"No artifact may describe NFR-IRI-01 as fully enforced"* from its own paragraph; `logical-components.md`'s `DriverError` box had split the printed 5/2/2 derivation across the box boundary. Both were appended-text-on-a-`>`-line accidents from the redo. |

**The recurring failure this unit has now produced three times, named plainly.** Each of the
three Criticals was introduced by the **repair of the previous one**, and each took the same
shape: a set was restated more narrowly than the rule states it, in text that read as a
tightening. The check that catches it is not a sweep — the defect is always in new text — it is
**printing the rule's own statement of scope beside the repair before writing the repair.**

---

## Remediation of the post-redo TERMINAL pass — 2026-09-02, second owner-directed redo

That pass returned **NOT-READY** (1 Critical, 1 Major, 1 Minor) with its budget spent. The
project decision owner directed a second redo, on the explicit basis that the fix would be
**complement-only, with no enumeration left anywhere to get wrong.**

| # | Sev | Repair |
|---|---|---|
| 1 | **Critical** | **The walk scope was left narrow at one of five sites.** `logical-components.md:129` — E-1's limb-1 mechanism cell — still read *"reachability over `src/` and `scripts/`"* after the limb had been widened at four other sites, so the limb **counted** notebook modules as populating the risk surface while the walk never **opened** `notebooks/`: a tree whose only candidate importer is a notebook satisfied the limb, the walk found nothing, and clause 2 returned **`passed`** over an uninspected tree. The remediation row that claimed *"all four sites"* was also wrong — the derived count is **five**. All five now state one set. |
| 2 | Major | **The enumeration is gone entirely, which is the actual fix.** `requirements.md`:370 states an **allowlist**, and its four named importer classes are **examples of the complement, not its definition** — so any directory list is the same defect in a new costume, as three successive lists proved. The candidate-importer set is now **defined once, by subtraction**, in a dedicated block in § SD-E-01, and every other site refers to it rather than restating it. **The walked set and the counted set are declared to be the same set.** |
| 3 | Major (same finding) | **`tests/` is settled explicitly, and the reason it had to be is WS-10.** `component-dependency.md`'s matrix grants `tests/*` a `yes` against the `external.iri` / `external.gim` column, making it an **allowlisted importer** — necessarily, because `tests/test_iri_denial.py` cannot perform WS-10's **deliberate injection** without importing what it tests, and a scan that scored its own negative control as a violation would make WS-10 unwritable. **The grant is a discrepancy against TE §12's "imported only by" two-path wording, recorded for a ruling rather than resolved here.** |
| 4 | Minor | **The absent-INTERMEDIATE transitive case is determined.** Name-matching settled the absent *target*; an unresolvable intermediate now **records an unresolved edge and yields `skipped`, not `passed`** — the same treatment as an empty limb, because a partly-built tree is full of unresolvable intermediates and treating them as clean would restore the vacuous pass by a third route. |

**Why this repair is shaped differently from the four before it.** Every previous attempt
answered *"which directories should the scan cover?"* — a question with an enumeration for an
answer, and an enumeration can always omit one more directory. This one answers *"what is not
an allowlisted importer?"*, which has a complement for an answer and no room to omit. **The
site list was derived and printed before any of the five was touched**, which is the step
missing from all four earlier repairs.

---

## Remediation of the second-redo pass — 2026-09-02

That pass returned **NOT-READY** (3 Critical, 3 Major, 1 Minor) on iteration 1 of the
second-redo budget, so one pass remains. Its headline finding is worth quoting rather than
paraphrasing: **the structural fix worked and the same failure recurred one level down** — no
live sentence enumerates directories any more, but the complement was stated over a **domain**,
and the domain was narrower than the rule twice over. Because that revision had also declared
the walked set to be the counted set, both narrowings sat in the **walk**.

| # | Sev | Repair |
|---|---|---|
| 1 | **Critical** | **The domain word was "Python module", which does not reach a notebook.** A `.ipynb` is not a `.py` file, the mechanism is stdlib `ast` with no cell-extraction step, and the one named exclusion (`__init__.py`) fixed the reading as `*.py`. `requirements.md`:370 names a notebook; `business-rules.md`:318 carries `Import iri from a notebook → fails` as a **required** R-56 negative control; the notebook exists on disk. **The domain is now "everything that can execute Python": `.py` files AND `.ipynb` code cells, with cell extraction named as a step of the walk.** |
| 2 | **Critical** | **`excluding __init__.py` was a counting heuristic promoted into the walk.** Verified on disk: `src/features`, `src/models`, `src/gnss`, `src/evaluation` and `src/external` each hold **exactly one file, `__init__.py`, 24 bytes** — so the only place an `src/features` → `iri` import could be written today was the file the definition subtracted. **The walk now covers the candidate-importer set entire, `__init__.py` included; only the cardinality count subtracts it**, and transitivity **through** a package `__init__` is walked like any other edge. The previous revision's *"walked set and counted set are the same set"* was itself the defect — an over-correction for an earlier divergence. |
| 3 | **Critical** | **The unresolvable-intermediate rule had landed in one artifact only — the third time this same box diverged.** `logical-components.md` contained "intermediate", "unresolvable" and "unresolved edge" **zero times** while presenting a closed three-clause switch. Both artifacts now carry the four-clause switch and the rule. |
| 4 | Major | **The intermediate rule sat outside the ordered switch**, so its rank against clause 1 was unstated and the literal reading let an unresolved edge **skip over a violation already found** — the masking shape the terminal pass graded Critical. It is now **clause 2**, with clause 1 stated to outrank it explicitly: *a found path is a fact, an unresolved edge is an absence, and an absence never outranks a fact.* |
| 5 | Major | **The `tests/*` grant is WITHDRAWN, and the reason it was made was wrong.** The previous revision admitted `tests/*` on the ground that WS-10's injection required the import. **WS-10 injects an `iri_*` field — a data act on a feature matrix, not an import** — and this project's own `tests/test_phase_boundary.py` asserts an import boundary by **parsing** rather than importing. No test needs the grant. **The allowlist is TE §12's two paths.** |
| 6 | Major | **The matrix discrepancy is now routed, having been routed nowhere.** `component-dependency.md`:34's `tests/*` row reads `yes` in **all seven columns** — a blanket convenience row — and is contradicted **four lines below**, at `:38`, by that artifact's own *"exactly two importers… Everything else is forbidden"*, and by `requirements.md`:370. **This design follows TE §12 and the matrix's own prose, and routes the blanket row to the gate.** |

**The pattern, now on its fifth instance and worth stating as a rule rather than an
apology.** Every repair in this section has been a **restatement of a set**, and every one
until this pass restated it more narrowly than the rule — trees, then directories, then a
domain, then a file-type exclusion. The failure is not carelessness about scope; it is that
**a narrower set always reads as a more rigorous one**. The only check that has caught it is an
adversarial reader holding the rule's own words beside the restatement, which is what the last
six passes did. What this stage can carry forward is the shape of the question: **when a design
restates a rule's scope, the restatement is a defect until the rule's own scope sentence is
printed beside it.**

---

## Remediation of the second-redo TERMINAL pass — 2026-09-02

That pass returned **NOT-READY** (1 Critical, 2 Major, 4 Minor) — but it also recorded three
things no earlier pass could: **the sibling-divergence check passed for the first time in
seven passes**, the domain is **coextensive with the rule** (*"a seventh restatement of the
domain would find nothing"*), and the **control itself is buildable** — *"an implementer can
build the scan, switch, limbs, payload and skip semantics from this text without asking a
question; that was untrue at every earlier pass."*

**The remaining Critical was a different animal from the five before it.** Those five narrowed
a **set**. This one was an **inference the old, narrower set supported, carried forward
without being re-derived when the set widened** — the artifacts still said the candidate set
was empty and the check *"cannot fail today"*.

| # | Sev | Repair |
|---|---|---|
| 1 | **Critical** | **The candidate-importer set is NOT empty, and the check is NOT inert.** Derived under this design's own definition and printed at DISC-E-1 in both artifacts: **18 files walked, 12 counted** — the notebook, both `scripts/` modules, `src/__init__.py`, four `src/data/` modules, four package `__init__.py` files, six `tests/` modules; `src/evaluation/` excluded because it is **allowlisted**, not because it is empty. **Only the target limb is empty.** So the check reaches **clause 4** and reports **`skipped`, naming the target limb**, over 18 files it really would inspect. The superseded *"two independent causes of vacuity"* and *"cannot fail today"* are withdrawn from DISC-E-1, both `## Assumptions` lists, the E-1 failure-domain row, and § SD-E-01's opening. **This matters at the gate**: an implementer told the check is dead has no reason to run it, and the gate record would capture a dead control where a live one exists. |
| 2 | Major | **The `__init__.py` evidence was false where the reasoning was sound.** `wc -c`: `src/external` **24**, `src/features` **24**, `src/models` **22**, `src/gnss` **20** — not "five packages, exactly 24 bytes", which was right for two of five. **`src/evaluation/` is removed from the list entirely**: it is allowlisted, so it was never a candidate. The walked/counted split it justifies is unaffected. |
| 3 | Major | **The `component-dependency.md` blanket row is now routed WITH AN OWNER.** The previous revision withdrew the `tests/*` grant correctly but tagged the discrepancy nowhere and named no owner, while four smaller items carried `OPEN, routed to the gate`. Both `## Assumptions` lists now carry it in that form, owned by **the project decision owner**. |
| 4 | Minor | **One payload schema, stated identically in both artifacts.** The two had listed different field subsets and neither was the union. Every outcome — `failed`, `passed`, `skipped` — carries the walked set by count and module path, any unresolved edges, and the empty-limb identifier where it applies. |

**Two residuals the pass named and this repair does not close**, recorded rather than
silently inherited: **`__pycache__` bytecode**, which exists on disk and is not in the domain,
and **notebook cells carrying IPython magics**, which `ast.parse` cannot read — verified as
**0 of the notebook's 14 code cells** today. Both are stated here rather than treated as
covered.

**What this section stops claiming.** Seven passes in, the honest summary is not that the
design is now correct — it is that **the control is buildable and its account of the workspace
is finally derived rather than inherited**. Every present-tense claim about the candidate set
in either artifact is now a printed derivation with its command shown.

---

## Review — 2026-09-02 iteration 2 (terminal)

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-02T05:18:58Z
**Iteration:** 2 of 2 — terminal pass, advisory. No third pass follows; the findings below go
to the human at the approval gate.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | **Critical** | `security-design.md` § SD-E-01 part 1 (predicate table, :107) and the correction box; `logical-components.md` E-1 DISC-E-1 box (:122); both artifacts' § Assumptions ("the predicate is a proxy") | **The Critical repair narrows the rule to a denylist that `requirements.md` FR-P1-04-1 expressly forbids, and the new limb can mask a violation the scan has actually found.** The risk-surface limb is defined as *"at least one module beyond `__init__.py` exists under `src/features/` or `src/models/` — **the two package trees FR-P1-04-1 and TE §12 name as the forbidden importers**"*. FR-P1-04-1 (`requirements.md:370`) says the opposite, in terms: *"the import boundary holds **as an allowlist, not a denylist** — TE §12 states it as 'imported only by `scripts/04_build_external_products.py` and `src/evaluation/`', so an import from **`src/data/`, `src/gnss/`, a training script or a notebook violates it exactly as** an import from `src/features/` or `src/models/` does"*, with `IMPL-3` and `IMPL-13` open against exactly this reading. The artifact's own DISC-E-1 names the risk surface as *"`src/features/*`, `src/models/*`, **and any other importer**"* — the repair dropped the third clause. Two consequences, and the second is the blocker. **(a)** The limb is narrower than the scan's own candidate set, which R-56 and this artifact define as the allowlist complement (*"any module outside `scripts/04_build_external_products.py` and `src/evaluation/`"*). **(b)** The outcome switch is stated unconditionally — *"The check reports `passed` only when both limbs are populated. **Otherwise it skips**, naming which limb was empty"* — with no precedence rule anywhere in either artifact for a scan that finds a violation while a limb is empty. Verified on disk today: `src/data/` holds three real modules (`config.py`, `locked_test.py`, `release.py`) while `src/features/` and `src/models/` hold only `__init__.py`. So a violating edge from `src/data/` — a plausible one, since `src/data` is the only package that writes release manifests (`components.md` § `src/data`) and SD-E-07 puts the byte-identical product contract on exactly that path — is **detected by the scan and reported as `skipped`**, and §18.3's *"no failing critical test"* is satisfied. Iteration 1's one-limb predicate could only skip when no target existed, a state in which no violation is possible; the new limb decouples the skip from the possibility of a violation, so this is a **broader** masking path than the one it repaired, on Vision §7.1's binding architectural rule. **Iteration-1 finding 1 is not closed.** | Two changes, both small. (i) Define the risk-surface limb as the **allowlist complement** the scan already walks — populated when any module beyond `__init__.py` exists under `src/` or `scripts/` outside `scripts/04_build_external_products.py` and `src/evaluation/` — and drop the FR-P1-04-1 citation for the two-tree reading, since FR-P1-04-1 rejects it and `IMPL-3` is open on it. Under that definition the limb is already populated today (`src/data`), which is the correct answer. (ii) State the outcome precedence explicitly: **a detected violation reports `failed` regardless of either limb**; `skipped` is reachable only when the scan found nothing *and* a limb is empty. An implementer cannot infer (ii) from the current text and would have to ask. |
| 2 | Major | `logical-components.md:62` (§ The boundary criterion, Q4 = A) and `:375` (§ decomposition, "2 subjects here-only") | **The finding-3 repair swept § Failure domains and left the Q4 criterion's own justification asserting the withdrawn claim.** § Failure domains now reads *"No component's **CHARACTERISTIC** failure announces itself"* and withdraws *"would have produced one box"*. But `:62` — the paragraph that argues **why the Q4 = A criterion was chosen** — still states the un-narrowed form: *"This unit's material barely varies on any of those three — **every component here fails silently and none of them raises at a human** — and it varies sharply on what is being excluded."* That is false on the corrected fact (E-2's hash-mismatch tier terminates non-zero and names the file) and it is load-bearing: it is the sentence that dismisses `inventory-and-registry`'s *how the failure reaches a human* axis as one this unit "barely varies on", which § Failure domains now concedes yields **two** boxes, not zero. `:375` repeats the same superseded form: *"the § Failure domains observation that **no component in this unit announces its own failure**"*. The remediation table lists the changed sites as *"§ Failure domains (claim + correction box + Q4 rationale), the E-2 failure-domain row"* — the "Q4 rationale" changed is the one **inside** § Failure domains (:302), not the criterion section at :62. This is the exact sweep failure `project.md` records twice (`fd-2026-08-30-sweep-derive-sites`, `fd-2026-08-30-sweep-numerals-and-surfaces`): the correction landed where the finding pointed and not where the fact lives. | Restate `:62` and `:375` in the narrowed form — every component's *boundary* failure is silent; E-2 additionally carries one loud input-integrity path — and re-state the Q4 justification against that, since "barely varies" is no longer the ground the rejection stands on (the ground § Failure domains now gives is that the two boxes would split E-2's hash check from E-2's own leakage rules). |
| 3 | Minor | `security-design.md` § SD-E-03 box (*"on adversarial finding 6"*); `logical-components.md` § decomposition box (*"on adversarial finding 7"*); § Remediation rows 6 and 7 | **The two Minor findings are cited under each other's numbers, in all three places.** Iteration-1 finding **6** is the `DriverError` placement gap; finding **7** is the unvalidated provenance stamp. The provenance box cites "finding 6", the `DriverError` box cites "finding 7", and the remediation table lists them in that swapped order. Every other correction box cites its number correctly (1, 2, 3, 4, 5). In an artifact whose discipline is exact citation, a reader reconciling the repairs against the findings table is sent to the wrong row twice. | Swap the two numbers at all three sites. |
| 4 | Minor | `security-design.md` :522 and the risk box :173–176; `logical-components.md` :395 | **"A narrower proxy would have to decide which modules are 'real', which no static check does" is overstated, and it is the sentence that closes off the alternative.** A static check cannot judge realness, but it can publish its own scope: the number of candidate modules walked, the number of import edges resolved, and whether either target module resolved as an importable name. Emitting those alongside a `passed` outcome — the same machine-readable treatment part 2 already gives the *skip* reason — lets `foundation`'s FR-WS-7 assertion distinguish "passed over 40 modules and 300 edges" from "passed over one stub", which is precisely the distinction the concession says is unavailable. The residual would then be narrow-and-quantified rather than narrow-and-stated. | Either add scan-scope metrics to the `passed` outcome, or narrow the claim to "no static check can decide realness" and record the metrics option as considered and declined with a reason. |

### Checks actually run

| Check | Method | Result |
|---|---|---|
| `requirements.md` FR-WS-7 is at line 462 and says what both artifacts now claim | `grep -n "^| FR-WS-7"`; full row read | **Confirmed.** Line 462 exactly. Criterion quoted correctly; the ten critical tests **are** enumerated; **IRI-free denial is the third**; the acceptance cell reads *"all ten named tests passing"*. The artifacts' *"a skip is not a pass, so it fails FR-WS-7 by definition"* is sound |
| `components.md:63` assigns FR-WS-7 to `config.py` | `grep -n "FR-WS-7" components.md`; surrounding table read | **Confirmed.** Line 63 exactly: `config.py` **NEW**, carrying REQ-ENG-2, REQ-ENG-10, **FR-WS-7**, FR-P1-03-5. Independently corroborated by `evidence/DECISIONS.md:1652`, which states *"`foundation` owns FR-WS-7/TA-23"* |
| `evidence/DECISIONS.md:1854` D-25 quotation | `sed -n '1850,1858p'` | **Confirmed verbatim.** Line 1854 is the D-25 row; *"Requests, but does not take, a §15.2 amendment to TE §7.0A stage 4 and EV-12; until granted, EV-12's F10.7 limb is unmet at G-04"* is exact, including *"An explicit project assumption, not a demonstrated publication latency"* |
| `evidence/DECISIONS.md:1648` lists D-25's request among the §18.3 precondition-1 holes | `sed -n '1644,1652p'` | **Confirmed exactly.** Line 1648 is precondition 1, **"Partially met"**, naming *"D-25's requested §15.2 amendment"* alongside D-17, D-26 and the nine unfrozen values |
| D-25's residual stated at the volume of the other carried blockers | read banner, § SD-E-04 limb-4 box, `logical-components.md` E-3 limb-4 box, both § Assumptions | **Confirmed — banner + section + assumptions, in both artifacts.** Four surfaces, matching the treatment of the other carried blockers. Finding 4 of iteration 1 is genuinely closed |
| `src/data/config.py` `__all__` = 17 | parsed `__all__` programmatically, printed before asserting | **Confirmed. 17**, and `AlignmentError` is present, so its exclusion from the missing set is right |
| The five-name `RAISES` set difference | `grep -n RAISES business-logic-model.md`; set-differenced against `__all__` | **Confirmed.** Exactly three `RAISES` lines — **:104**, **:367**, **:478** — union `{DriverError, BenchmarkError, ComparatorError, ImportBoundaryError, FeatureAvailabilityError}` = **5**, none of the five in `__all__` |
| 7 design sections | `grep -c "^## SD-E"` | **Confirmed.** 8 headings, SD-E-00 a state record → **7** |
| 10 coverage rows in each artifact, identical membership, set-differenced **both** directions | parsed both tables programmatically | **Confirmed. 10 and 10, empty in both directions.** `{REQ-ENG-9, FR-P1-04-1, -3, -4, -9, -15, -17, -18, NFR-IRI-01, NFR-LEAK-01}` |
| 4 unrowed | counted `NO ACCEPTANCE ROW` cells in both tables programmatically | **Confirmed. 4 in each** — REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18 |
| 3 components | `grep -c "^### E-"` | **Confirmed. 3** |
| The 11-ID FR-P1-04 set difference | enumerated the ID space in `requirements.md` | **Confirmed.** Space is exactly `{1…18}`; unit carries 7; difference is the 11 listed |
| 5/2/2 decomposition | re-derived against the SD-E headings | **Confirmed arithmetically** (5 single + 2 shared = 7), and `DriverError`'s non-placement is now registered as deliberate |
| WS-11 restored at **both** coverage tables, and correct against the map | read both tables; `business-logic-model.md:744` | **Confirmed.** Both tables read **WS-11** with R-57a demoted to "the mechanism, not the row"; the map's row for FR-P1-04-3 is **WS-11**, owner `features-and-splits`. Iteration-1 finding 5 genuinely closed |
| The provenance barrier restated as evidentiary | § SD-E-03 new box | **Confirmed and well done.** *"'forge' here means type a different string, not defeat a signature"*, *"The barrier this adds is evidentiary, not cryptographic"*. Iteration-1 finding 7 genuinely closed (though cited under the wrong number — finding 3 above) |
| `DriverError`'s non-placement registered | `logical-components.md` § decomposition box, § Assumptions | **Confirmed.** Registered as a refusal with its reason (carried Finding 9), not an omission. Iteration-1 finding 6 genuinely closed (wrong number — finding 3 above) |
| Workspace state on every limb the artifacts assert | `ls -1 src/`, per-package listing, `ls tests/ scripts/`, `ls -d configs`, `python --version` | **Confirmed on every limb.** `src/external/` = `__init__.py` only; `features`/`models`/`evaluation`/`gnss` likewise; **`src/data/` holds `config.py`, `locked_test.py`, `release.py`** — the three real modules, and the premise of finding 1; `tests/` holds exactly the six named modules with **no `test_iri_denial.py`**; `scripts/` holds two, neither `04_build_external_products.py`; `configs` absent; **Python 3.14.7** |
| Fresh-defect sweep: does any surviving sentence assert the one-limb predicate, "a reading this stage fixes", or "not one of the three announces itself"? | `grep -n` for each phrase and its variants across both artifacts | **The first two: clean.** Every surviving occurrence sits inside a correction box quoting the superseded text, which is the right treatment. **The third: NOT clean** — `logical-components.md:62` and `:375` still assert the withdrawn form. See finding 2 |
| Does the narrowed announce-itself claim contradict the E-1 or E-3 failure-domain rows? | read all three rows against the headline | **No contradiction.** E-1 *"No — nothing raises"*, E-3 *"No"*, E-2 *"Not for its boundary property… its input-integrity tier is loud"*. The headline *"No component's CHARACTERISTIC failure announces itself"* is consistent with all three, as is the closing *"not one of the three boundary properties has one"* |
| Did the Q4 rationale correction hollow out the criterion's justification? | read the corrected rationale at `:300–306` | **Sound on its own terms.** The withdrawal of *"would have produced one box"* is honest, and the replacement ground — that the two boxes would split E-2's hash check from E-2's own leakage rules, i.e. split a component by loudness rather than purpose — is a real argument. **But it now contradicts `:62`**, which is finding 2 |
| Is the refusal to edit the signed questions file correct, or an evasion? | read `nfr-design-questions.md` Q1 in full, its `[Answer]: A`, and the receipted Consolidated Summary Confirmation (`[Answer]: Looks correct`); checked against `project.md` `fd-2026-08-30-never-edit-signed-record` | **Correct, not an evasion, and this is the sanctioned path.** The rule is exactly on point: *"Record the correction in the artifacts you own, state the derived value with its derivation printed, and route ONE explicit ruling to the human."* Both were done. **A further point runs in the builder's favour:** Q1's own preamble already stated **both** causes of vacuity — *"neither target module exists, **and** every package that could import one holds only `__init__.py`"* — so the two-limb reading is within the answered question, not a widening of it. (That preamble clause is itself factually wrong today — `src/data` is a package that could import one and holds three modules — which is the same allowlist/denylist conflation finding 1 identifies, predating the repair. It is a signed record; it is noted, not repaired) |
| No satisfaction or discharge claim | grep for `iricore` version, GIM product issue, `2000 km`, FR-P1-04-18's rule, `test_iri_denial.py`, any `PASS`/satisfied claim | **Confirmed clean.** Both `TBD — freeze gate` values remain unnamed; `2000 km` appears only as a quotation of FR-P1-04-15's own required report field; FR-P1-04-18's interpolation rule is stated **UNSET**; `carry_forward_composition` left `TBD`; `tests/test_iri_denial.py` stated as not existing in both banners, both § Assumptions and the coverage cells; **0 rows claimed satisfied**; no gate, acceptance row or test claimed passing; nothing authorises a module write |

### Iteration-1 findings — closed or not

| It-1 # | Sev | Status |
|---|---|---|
| 1 | Critical | **NOT CLOSED.** The stub scenario is covered; the repair introduced a **broader** masking path in its place — see finding 1 above |
| 2 | Major | **Closed.** FR-WS-7 cited at line 462 with its enumerated ten, ownership assigned to `config.py`/`foundation` via `components.md:63`, the claim of standing withdrawn, the dependency routed to the gate on the same footing as SD-E-02's and SD-E-03's. Both verified against source |
| 3 | Major | **Partially closed.** The narrowing is real and the distinction (input integrity vs. boundary property) **holds** — a hash check genuinely says nothing about whether the future leaked, and the withdrawal of *"one box"* is honest. Two representations were not swept — finding 2 above |
| 4 | Major | **Closed.** Both `DECISIONS.md` quotations verified verbatim at the cited lines; the residual is stated in the banner, the section and § Assumptions, in both artifacts |
| 5 | Minor | **Closed.** WS-11 restored at both tables and correct against the map |
| 6 | Minor | **Closed** (`DriverError` non-placement registered as a refusal), **cited under the wrong number** |
| 7 | Minor | **Closed** (the barrier restated as evidentiary), **cited under the wrong number** |

### Validation tool results

| Tool | Result | Interpretation |
|---|---|---|
| — | The stage definition declares **no** validation tools | No tool output to interpret. Every check above was run by hand against the workspace, the passed shared contracts and the declared upstream, and every count was derived programmatically and printed before being asserted |

### Coverage limits — what was NOT checked, and why

- **The three sibling `logical-components.md` criterion comparisons** (failure consequence, enforcement timing, how the failure reaches a human), the **`governance-guards` R-23/R-24/R-28** and **`inventory-and-registry` R-51/Q2** citations, and the *"five amendments across three units"* roll-up: all out of read-scope, all **unverified**, and they remain this unit's own characterisation of other units' work. Finding 2 turns on `:62`'s claim about **this** unit's components, which is checkable inside scope; it does not turn on whether the sibling characterisations are right.
- **`foundation`'s FR-WS-7 assertion** — whether it will in fact read the structured skip reason rather than count non-failures — is the dependency this stage routes to the gate. It cannot be verified from here, and the artifacts correctly state it as owed rather than satisfied.
- **`domain-entities.md` § 9's `DriverError` cell** was read only through Finding 9's verbatim quotation inside `business-logic-model.md`.
- The upstream `nfr-requirements` artifacts' own internal consistency was not re-reviewed; only the claims § SD-E-00 supersedes were checked.

### Summary

The repairs to findings 2, 4, 5, 6 and 7 are real, complete and verified at source — FR-WS-7
at line 462, `components.md:63`, both `DECISIONS.md` quotations, WS-11 against the map. Every
printed count re-derives from the current files, including the two coverage tables' empty set
difference in both directions. Nothing is claimed satisfied, no freeze-gate value is filled,
and the refusal to edit the signed questions file is the sanctioned path under `project.md`,
not an evasion — Q1's own preamble already put both causes of vacuity to the owner.

**The Critical is not closed, and the repair is what reopened it.** The risk-surface limb was
written as a denylist over `src/features/` and `src/models/` and cited to FR-P1-04-1, which
says in terms that the boundary is *"an allowlist, not a denylist"* and that an import from
`src/data/` or `src/gnss/` *"violates it exactly as"* one from those two trees does — the
artifact's own DISC-E-1 says the same thing in the words *"and any other importer"*, which the
repair dropped. Paired with an outcome switch stated as *"otherwise it skips"* and no
precedence rule for a scan that finds something, the effect on today's tree — three real
modules in `src/data/`, `src/features/` and `src/models/` empty — is that a **detected**
violation of Vision §7.1's binding architectural rule reports `skipped` and passes §18.3.
Iteration 1's predicate could only skip where a violation was impossible; this one can skip
where a violation has been found. Both changes needed are small and local (widen the limb to
the allowlist complement the scan already walks; state that a detected violation fails
regardless), but as written a developer cannot build the control without asking which of two
incompatible readings of the boundary rule it implements.

**For the human at the gate.** Finding 1 is a blocker in substance: it should not go to
implementation as written, and it is cheap to fix. Finding 2 is a completeness defect in a
correction, of the kind this project has recorded twice as a standing pattern — worth
weighing, not a blocker. Findings 3 and 4 are housekeeping and judgement respectively and
neither should hold the gate.

---

## Review — 2026-09-02 post-redo pass

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-02T19:06:48Z
**Iteration:** 1 of 2 (fresh budget after the owner-directed redo jump; the third revision of these artifacts)

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | **Critical** | `logical-components.md:137–142` (§ E-1, DISC-E-1 box); contradicted by `security-design.md:114` and `logical-components.md:414–415`; falsely described by `logical-components.md:5–8` (re-save banner) and `security-design.md:689` (terminal-remediation row 1) | **The terminal Critical is repaired in one artifact and left standing in the other, at the exact site the terminal finding named.** The terminal pass located finding 1 at *"`logical-components.md` E-1 DISC-E-1 box (:122)"*. That box today still states the design as: *"a **two-limb vacuity predicate**: the **target side** (at least one of `iri.py`, `gim.py` exists) and the **risk-surface side** (at least one module beyond `__init__.py` under `src/features/` or `src/models/`). It passes only when **both** are populated"* — the superseded denylist form, asserted as current design in the component section that OWNS the check, not quoted inside a correction box as superseded. It carries **no precedence rule**: `grep -n -i "precedence\|complement\|regardless of either limb" logical-components.md` returns only `:6` (banner), `:414` and `:415` (§ Assumptions) — nothing in E-1. So the two artifacts now specify **two incompatible predicates**, and the narrow one sits in the component definition an implementer builds from. Every consequence the terminal pass proved still follows from it verbatim: `src/data/` holds three real modules (`config.py`, `locked_test.py`, `release.py`) while `src/features/` and `src/models/` hold `__init__.py` only (verified on disk today), so a **detected** violating edge out of `src/data/` reports `skipped` under E-1's predicate and satisfies TE §18.3's *"no failing critical test"* on Vision §7.1's binding architectural rule. **Two claims about this box are false as written**: the re-save banner states *"E-1's DISC-E-1 box **now carries** the two-limb vacuity predicate over the **allowlist complement** and the precedence rule"*, and terminal-remediation row 1 claims the widening and the precedence rule as done. Neither is true of that box. This is the third consecutive revision in which the repair of this one finding left a defect behind. | Replace the risk-surface limb inside the DISC-E-1 box with the allowlist-complement wording already at `security-design.md:114`, and state the precedence rule (clause 1 → `failed` regardless of either limb) inside E-1, where the check is defined. Then re-verify the banner's and the remediation row's claims against the box rather than against `security-design.md`. |
| 2 | Major | `security-design.md:114` (risk-surface limb) and `logical-components.md` § E-1 limb 1 (*"reachability over `src/` and `scripts/`"*); against `requirements.md:370` and `business-rules.md:318` | **The widened complement still does not reach a notebook — the one importer class its cited authority names that exists on disk today.** The complement is scoped to *"anywhere under `src/` or `scripts/`"*. `requirements.md:370`, quoted by the repair as its authority, states the boundary *"as an allowlist, not a denylist… so an import from `src/data/`, `src/gnss/`, **a training script or a notebook** violates it exactly as an import from `src/features/` or `src/models/` does"*, and upstream `business-rules.md:318` carries *"Import `iri` from a notebook → **fails**"* as a **required negative control** of R-56. `ls notebooks/` returns `madrigal_phase1_coverage_audit.ipynb` — the notebook exists, and `team.md` § Code Style records it as still holding logic owed a migration. A notebook import of `iri.py` therefore falls outside both the limb and the scan scope, and is **undisclosed**: § SD-E-01's *"What is not reopened"* paragraph discloses only the dynamic-import residual and the run-time-computed module path. The repair's own standard — set-difference the narrowed set against the rule's statement of scope — was not applied to the wider form it wrote. | Either extend the scan scope and the complement to `notebooks/` (which makes R-56's own negative control executable), or disclose the notebook exclusion in § SD-E-01 beside the dynamic-import residual and route it as a gap against R-56's negative-control list. Do not leave the citation to `requirements.md:370` standing over a complement that omits one of the four importer classes that line names. |
| 3 | Minor | `security-design.md` § SD-E-01 part 2 (`:152–155`) against the symmetry requirement at `:210–215`; `logical-components.md:414` | **The required symmetry names an evidence payload that the skip is not specified to carry.** Part 2 specifies the skip's machine-readable payload as *"a structured value **naming the empty limb**"* — a reason code. The symmetry then requires that *"a `passed` outcome carries **the same** machine-readable scan-scope evidence the skip carries — the candidate-importer set the scan actually walked, by count and by module path."* Those are different payloads: a limb name is not a scan-scope set. The `passed` side is buildable as written (count + paths), but an implementer cannot tell whether the skip must now also emit the scope set, and `foundation`'s FR-WS-7 consumer — the dependency this design declares load-bearing — reads whichever one is actually emitted. | State one payload schema used by both outcomes: outcome, empty-limb reason (skip only), candidate-importer count, and the module paths walked. Then the symmetry claim is literally true and the consumer contract is single. |
| 4 | Minor | `security-design.md:118–121` (precedence clause 1) | **Clause 1's reachability under an empty target limb is undetermined, so the ordering cannot be evaluated where it matters most.** The ordering itself is sound — `passed` is reachable only with both limbs populated and no violation, and the cardinality-vs-representativeness residual is disclosed and mitigated. But whether clause 1 can fire at all when neither `iri.py` nor `gim.py` exists depends on an unstated implementation choice: an `ast` walk that matches import **statements by name** detects `import src.external.iri` against a nonexistent file, while one that resolves imports against the **file tree** cannot. Today's tree is exactly that state. Neither artifact says which. | State that the scan matches import statements by module path textually and does not require the target file to exist, so clause 1 is live in the pre-build state — or, if the opposite is intended, say so and record that clause 1 is inert while the target limb is empty. |
| 5 | Minor | `security-design.md:316–317`; `logical-components.md:391–392` | **Two blockquotes introduced by this redo break mid-sentence, severing load-bearing text from its box.** At `security-design.md:316` the § SD-E-03 box ends inside the sentence *"A value renamed and recomputed from scratch, carrying a fabricated but plausible / provenance, survives"*, so that sentence and the following **"No artifact may describe NFR-IRI-01 as fully enforced"** render half inside the warning box and half as body text. At `logical-components.md:391` the `DriverError` box ends inside *"…is unaffected. **2** subjects are here-only with no `security-design.md` / counterpart"*, splitting a printed derivation across the box boundary. Both are the result of appended text on an existing `>` line. | Close each blockquote with a blank `>` line and start the following sentence as body text. |

### Checks actually run

| Check | Method | Result |
|---|---|---|
| Does `logical-components.md`'s DISC-E-1 box carry the widened limb and the precedence rule? | `grep -n "beyond \`__init__.py\`" logical-components.md security-design.md`; `grep -n -i "precedence\|complement\|regardless of either limb" logical-components.md`; box read in full | **NO on both.** `logical-components.md:139–140` still reads *"under `src/features/` or `src/models/`"*; precedence appears only at `:6`, `:414`, `:415`. `security-design.md:114` carries the wide form. **Finding 1.** |
| Are the banner's and the remediation row's claims about that box true? | read `logical-components.md:5–8` and `security-design.md:689` against the box | **False.** Both assert the box now carries the allowlist complement and the precedence rule. **Finding 1.** |
| Does the complement reach the importer classes `requirements.md`:370 names? | `sed -n '368,372p' requirements.md`; `ls notebooks`; `grep -n notebook business-rules.md business-logic-model.md` | `src/data/`, `src/gnss/`, a training script: reached. **A notebook: NOT reached**, and `notebooks/madrigal_phase1_coverage_audit.ipynb` exists. R-56 (`business-rules.md:318`) requires *"Import `iri` from a notebook → fails"*. **Finding 2.** |
| Is the precedence ordering sound; is `passed` reachable while the check is meaningless? | traced all three clauses against today's tree | Ordering sound: `passed` requires both limbs populated **and** no violation, so no violation can be masked. `passed` over a thin surface remains reachable — disclosed by the artifact as a cardinality-not-representativeness test and mitigated by the required symmetry. Clause 1's behaviour with an empty target limb is unstated. **Finding 4.** |
| Terminal Major: is § The boundary criterion (`:61`) swept? | read `:70–79` | **Closed.** Now *"every component's **BOUNDARY** failure is silent, and **E-2 additionally carries one loud path**"*, with the withdrawal dated and attributed. |
| Terminal Major: is the § decomposition here-only list swept? | read `:391–395` | **Closed.** Now *"no component's CHARACTERISTIC failure announces itself — every boundary failure here is silent, while E-2 alone carries one loud input-integrity path"*. |
| Is there a THIRD site still asserting the un-narrowed claim? | `grep -n -i "announce\|silent\|loud"` across both artifacts, every hit read | **None.** `:301`, `:310–312`, `:323`, `:393` all carry the narrowed form; `:304` and `security-design.md:592/654/717` quote the superseded text inside review or correction context. |
| Is the re-argued Q4 rejection sound? | read `logical-components.md:318–330` | **Sound.** *"Would have produced one box"* is withdrawn as too strong; the axis is conceded to yield **two**; the rejection now rests on those two boxes splitting E-2's hash check from E-2's own leakage rules — grouping by loudness rather than purpose. That is an argument, not a restatement, and it is consistent with the E-1/E-2/E-3 failure-domain rows. |
| Terminal Minor 3: are it-1 findings 6 and 7 relabelled at all three sites? | read § SD-E-03 box, § decomposition box, § Remediation rows | **Closed.** Provenance box → *"finding 7"*; `DriverError` box → *"finding 6"*; remediation table footnoted. (Remediation rows print in order 5, 7, 6 — cosmetic only.) |
| Terminal Minor 4: is the symmetry buildable? | read `:210–215` against part 2's skip payload | **Buildable on the `passed` side** (count + module paths, machine-readable) — not a gesture. **But not "the same evidence the skip carries".** **Finding 3.** |
| 7 design sections | `grep -c "^## SD-E" security-design.md` | **Confirmed. 8 headings, SD-E-00 a state record → 7.** |
| 3 components | `grep -c "^### E-" logical-components.md` | **Confirmed. 3.** |
| 10 coverage rows in each, identical membership, set-differenced BOTH directions | both tables parsed programmatically, ID sets printed before comparison | **Confirmed. 10 and 10; A−B = ∅ and B−A = ∅.** `{REQ-ENG-9, FR-P1-04-1, -3, -4, -9, -15, -17, -18, NFR-IRI-01, NFR-LEAK-01}`. |
| 4 unrowed | blank acceptance cells counted in both tables | **Confirmed. 4 in each** — REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18. |
| `config.py` `__all__` = 17, and the five-name RAISES difference | `__all__` parsed with `ast` and printed; `grep -n RAISES business-logic-model.md`; set-differenced | **Confirmed. 17 names**, `AlignmentError` among them (so its exclusion is right). Exactly three `RAISES` lines — `:104`, `:367`, `:478` — union `{DriverError, BenchmarkError, ComparatorError, ImportBoundaryError, FeatureAvailabilityError}` = **5**, none present in `__all__`. |
| The 11-ID FR-P1-04 set difference | ID space enumerated from `requirements.md` and printed | **Confirmed.** Space is exactly `{1…18}`; unit carries `{1,3,4,9,15,17,18}` = 7; difference = 11. |
| 5/2/2 decomposition | re-derived against the SD-E headings | **Confirmed.** 5 single-component + 2 shared = 7; `DriverError`'s non-placement registered as a refusal with its reason. |
| WS-11 restored at both coverage tables | read both tables against `business-logic-model.md:744` | **Confirmed.** Both read **WS-11**, owner `features-and-splits`, with R-57a demoted to "the mechanism, not the row". |
| No satisfaction or discharge claim | grep for `iricore` version, GIM product issue, `2000 km`, FR-P1-04-18's rule, `test_iri_denial.py`, `TBD`, any pass/satisfied claim | **Confirmed clean.** Both freeze-gate values unnamed; `2000 km` appears only as a required report field; FR-P1-04-18's interpolation rule stated **UNSET**; `carry_forward_composition` `TBD`; `tests/test_iri_denial.py` stated as not existing; D-25's amendment stated ungranted with EV-12's F10.7 limb unmet at G-04; no gate, acceptance row or test claimed passing; nothing authorises a module write. |
| Fresh-defect sweep: two-tree risk surface, unconditional *"otherwise it skips"*, *"a reading this stage fixes"*, un-narrowed announce-itself | `grep -n` for each phrase and variants across both artifacts, every hit read | **Three clean, one not.** *"otherwise it skips"* and *"a reading this stage fixes"* survive only inside correction boxes and review history; the announce-itself claim is narrowed everywhere. **The two-tree risk surface survives as live design text at `logical-components.md:139–140` — finding 1.** |
| Do the two remediation sections contradict the body? | read both against §§ SD-E-01, SD-E-03, the coverage table and `logical-components.md` | **One contradiction.** Terminal row 1's claim (a)+(b) is true of `security-design.md` and false of `logical-components.md` — finding 1. Iteration-1 row 1 restates the superseded narrow limb as "the repair"; that is an accurate historical record and the terminal section immediately corrects it, so it is not counted as a defect. |
| Are the correction boxes' claims about the superseded text accurate? | each box's quotation checked against the terminal review's own findings table | **Accurate.** The SD-E-01 box's quotation of the two-tree scoping, the *"otherwise it skips"* pairing, and the `src/data/` masking path all match terminal finding 1 verbatim; the Q4 box's *"would have produced one box"* matches terminal finding 2. |
| Workspace state on every limb asserted | `ls -d notebooks src scripts tests configs`; per-package listing; `python --version` | **Confirmed.** `src/data/` = `config.py`, `locked_test.py`, `release.py`; `src/external|features|models|evaluation|gnss` = `__init__.py` only; `tests/` = six modules, **no `test_iri_denial.py`**; **no `configs/`**; `notebooks/` holds one notebook; interpreter 3.14.7, off the 3.11 pin. |

### Terminal-pass findings — closed or not

| Terminal # | Sev | Status |
|---|---|---|
| 1 | **Critical** | **NOT CLOSED.** Repaired in `security-design.md` (`:114` complement + `:118–121` precedence) and **left standing in `logical-components.md`'s DISC-E-1 box**, the site the finding named. Two artifacts, two incompatible predicates. Additionally, the widened complement omits notebooks — finding 2. |
| 2 | Major | **Closed.** Both named sites swept to the narrowed form; no third site survives; the re-argued Q4 rejection is sound on the ground given. |
| 3 | Minor | **Closed.** Findings 6 and 7 relabelled at all three sites, with a dated footnote. |
| 4 | Minor | **Closed in substance.** The overstatement is withdrawn and replaced by a required, buildable symmetry — though its payload does not match the skip's as claimed (finding 3). |

### Validation tool results

| Tool | Result | Interpretation |
|---|---|---|
| — | The stage definition declares **no** validation tools | Nothing to interpret. Every check above was run by hand against the workspace, the declared upstream and the passed shared contracts; every count was derived programmatically and printed before being asserted. |

### Coverage limits — what was NOT checked, and why

- **All sibling-unit criterion comparisons** (`foundation`'s failure-consequence axis, `governance-guards`' enforcement-timing axis, `inventory-and-registry`'s how-it-reaches-a-human axis), the `governance-guards` R-23/R-24 and `inventory-and-registry` R-51/Q2 citations, and the *"five amendments across three units"* roll-up: **out of read-scope, unverified**, and treated as this unit's own characterisation. Finding 1 does not depend on any of them.
- **`foundation`'s FR-WS-7 assertion** — whether it will read the structured skip reason rather than count non-failures — is unverifiable from here. The artifacts correctly state it as owed.
- **`domain-entities.md` § 9's `DriverError` cell** was read only through carried Finding 9's verbatim quotation inside `business-logic-model.md`.
- The upstream `nfr-requirements` artifacts' internal consistency was not re-reviewed; only the claims § SD-E-00 supersedes were checked.
- Whether `notebooks/madrigal_phase1_coverage_audit.ipynb` currently imports anything from `src/external/` was **not** tested — it cannot, since those modules do not exist. Finding 2 is about the control's specified reach, not about a present violation.

### Summary

Four of the five things the redo set out to fix are genuinely fixed and verified at source: the boundary criterion and the decomposition list both carry the narrowed announce-itself claim with no third site surviving, the Q4 rejection is re-argued on real ground, the two Minors are relabelled everywhere, and the "no static check judges realness" overstatement is replaced by a buildable symmetry. Every printed count re-derives from the current files — 7 sections, 3 components, 10/10 coverage rows with an empty set difference in both directions, 4 unrowed, `__all__` = 17, the five-name RAISES difference, the 11-ID FR-P1-04 difference, 5 + 2 = 7. Nothing is claimed satisfied, both freeze-gate values stay unnamed, and D-25's ungranted amendment and the unwritten `tests/test_iri_denial.py` are stated against the unit rather than for it.

**The Critical is still open, and this time it is open by omission rather than by over-narrowing.** `security-design.md` carries the correct predicate — allowlist complement plus a precedence rule under which a detected path fails regardless of either limb. `logical-components.md`'s E-1 DISC-E-1 box, the site the terminal finding explicitly named, still specifies the `src/features/`-or-`src/models/` denylist with no precedence rule at all, and both the re-save banner and terminal-remediation row 1 assert that it was changed. An implementer builds a check from the component that defines it, and that component still describes the predicate under which a violation detected in `src/data/` — three real modules today — reports `skipped` and satisfies §18.3 on Vision §7.1's binding architectural rule. The repair is a copy-edit away; what makes it Critical is that the artifact set now states two incompatible controls and its own bookkeeping says the disagreement was resolved. This is the pattern the redo's own closing note names — *"when a repair narrows a set, print the set it narrowed from"* — applied to one artifact and not the other.

Finding 2 is a second, independent gap in the widened complement: it reaches `src/data/`, `src/gnss/` and training scripts but not a notebook, though the line it cites names a notebook and R-56 carries *"Import `iri` from a notebook → fails"* as a required negative control, and the notebook exists on disk. Findings 3–5 are specification and presentation defects that should be fixed but should not hold the gate.

**For the human at the gate.** Findings 1 and 2 are both cheap and both should be fixed before implementation: copy the corrected predicate and the precedence rule into `logical-components.md`'s E-1 box, correct the two claims that say it was already done, and either extend the complement to `notebooks/` or disclose the exclusion. The design's substance — a two-limb vacuity predicate with a precedence rule, a machine-readable skip reason, a flipped provenance default, ordering-not-presence gates, and a two-tier reliability posture — is sound and reviewable; what is not yet safe is that the two artifacts disagree about the single control that TE §18.3 counts as critical.

---

## Review — 2026-09-02 post-redo iteration 2 (terminal)

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-02T19:18:18Z
**Iteration:** 2 of 2 on the post-redo budget — terminal. Advisory: no third pass follows, and
the findings below go to the human at the approval gate rather than back into a repair loop.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | **Critical** | `logical-components.md:129` (§ E-1, limb-1 table, "Mechanism" cell); against `logical-components.md:143`, `:436`, `security-design.md:114`, `:585`; falsely described by `security-design.md:737` (post-redo remediation row 2) | **The notebooks repair landed in the risk-surface LIMB at four sites and not in the SCAN SCOPE, which is the fifth — and the fifth is the site the post-redo finding's own Location field named.** E-1's limb-1 mechanism cell still reads *"stdlib `ast` reachability **over `src/` and `scripts/`**"*. The post-redo finding 2's Location was *"`security-design.md:114` (risk-surface limb) **and `logical-components.md` § E-1 limb 1 ("reachability over `src/` and `scripts/`")**"*, and its recommendation was to *"extend **the scan scope** and the complement to `notebooks/`"*. The complement was extended; the scan scope was not. Two consequences, and the second is new damage rather than a survival. **(a)** Under E-1's stated mechanism the walk never opens a notebook, so R-56's **required** negative control — `business-rules.md:318`, *"Import `iri` from a notebook → **fails**"* — is not executable by the check as specified, and `notebooks/madrigal_phase1_coverage_audit.ipynb` exists on disk today. **(b) The half-repair creates a masking path the pre-repair text did not have.** The candidate-importer limb (`:143`) now counts notebook modules as populating the risk surface, while the walk (`:129`) does not cover `notebooks/`. A tree whose only non-`__init__.py` module outside the allowlist is a notebook therefore satisfies the limb, the walk finds nothing because it never looked there, and clause 2 returns **`passed`** — a vacuous pass, green, over a surface the scan does not inspect. That is the exact defect § SD-E-01 exists to prevent. **The two artifacts again specify incompatible scopes**, with the narrow one in the component definition an implementer builds from. **And the bookkeeping claim is false**: remediation row 2 states *"`notebooks/` is now in the walked set, **at all four sites that state the scope**"* — the derived site count is **five** (`sd:114`, `sd:585`, `lc:143`, `lc:436`, `lc:129`), four changed, one left. **Fourth consecutive revision in which the repair of this one finding left the same defect behind, and third in which it landed in one artifact and not its sibling.** | Replace `logical-components.md:129`'s mechanism cell with the walked set as `security-design.md:114` defines it — every module beyond `__init__.py` outside `scripts/04_build_external_products.py` and `src/evaluation/`, across `src/`, `scripts/` and `notebooks/` — so the limb and the walk range over one set. Then re-derive the site count from the artifacts rather than from the repair's own list, and correct remediation row 2's "all four sites". |
| 2 | Major | `security-design.md:114`, `:585`; `logical-components.md:143`, `:436`; against `requirements.md:370` and `business-rules.md:318` | **Enumerating three directories is the narrowing defect in a new costume: the rule is an allowlist, and an allowlist's complement is everything else.** `requirements.md:370` fixes the boundary as *"imported only by `scripts/04_build_external_products.py` and `src/evaluation/`"*, **as an allowlist, not a denylist**; its four named importer classes (`src/data/`, `src/gnss/`, a training script, a notebook) are **examples of the complement, not its definition** — the same misreading that produced the two-tree Critical, one level up. `tests/` holds **six real modules today** (`test_acquisition_window.py`, `test_locked_test_guard.py`, `test_merge_script_restricted_reads.py`, `test_phase_boundary.py`, `test_release_contract.py`, `test_release_hashes.py`), sits outside both allowlisted paths, and is in TE §12's mandated tree — a test module importing `src.external.iri` violates FR-P1-04-1 exactly as `src/data/` does, and is neither walked nor counted. The repository root and `artifacts/` are outside the enumeration too. The exclusion is **undisclosed**: § SD-E-01's *"What is not reopened"* residual paragraph names only the dynamic-import and run-time-computed-path residuals. A second implementer question falls out of the same gap and is unanswered anywhere in either artifact: **whether `tests/test_iri_denial.py`'s own deliberate `iri_*` injection would be scored a violation** — the control WS-10 requires cannot be written until that is settled. | State the walked set as the allowlist complement itself — every Python module and notebook in the repository outside `scripts/04_build_external_products.py` and `src/evaluation/` — and name any carve-out explicitly (the denial test's own fixture being the obvious one), rather than enumerating trees. If an enumeration is kept for implementability, disclose the excluded trees beside the dynamic-import residual and route the omission as a gap against R-56's negative-control list. |
| 3 | Minor | `security-design.md:159–166` (part 1, clause-1 mechanics) | **Name-matching settles clause 1 for an absent TARGET and leaves it undetermined for an absent INTERMEDIATE, which is the other half of the same partly-built tree.** The text establishes that the walk matches the module **path** `src.external.iri` / `src.external.gim` textually, so a violation is detectable with no target file present. It says nothing about a **transitive** chain whose intermediate hop is absent — A imports B, B is planned to import `iri` but is not yet on disk — where the walk has no AST to expand. The design's own transitivity claim (*"directly or transitively"*) therefore holds only over modules present in the candidate set, and an implementer cannot tell whether that is the intent or an omission. | Add one sentence: transitivity is resolved over modules present in the candidate set, so a chain through a module not yet on disk is not detectable, and record that as a third named residual beside the dynamic-import ones. |

### Checks actually run

| Check | Command / method | Result |
|---|---|---|
| The same-artifact-pair check on the predicate | `lc:137–152` and `sd:107–121` read side by side, phrase by phrase | **Predicate, limbs, precedence order and payload AGREE.** Target side identical; risk-surface side identical including `notebooks/`; the ordered switch (violation → `failed` regardless of either limb; both populated → `passed`; either empty → `skipped` naming which) identical in both; payload identical (candidate-importer set actually walked, by count and by path, plus the empty-limb identifier on a skip). **The post-redo Critical is closed at the predicate.** |
| Every OTHER site stating scan scope, outcome switch or payload | `grep -n "notebook\|reachability over\|walked\|candidate-importer\|regardless of either limb\|otherwise it skips"` across both files, every hit read | **Four of five scope sites agree; `lc:129` does not** — *"reachability over `src/` and `scripts/`"*. Outcome-switch and payload sites: **all agree.** **Finding 1.** |
| Is the complement complete against the rule? | `sed -n '368,372p' requirements.md`; `sed -n '314,322p' business-rules.md`; `ls tests src/* scripts notebooks` | `src/data/`, `src/gnss/`, training scripts, notebooks: reached by the limb. **`tests/` (six modules) and the repository root: NOT reached, and not disclosed.** **Finding 2.** |
| Skip and `passed` payloads buildable as one structure? | `sd:155–158` against part 2 (`:178–181`) | **Buildable.** One structure: outcome, candidate-importer count, module paths walked, plus empty-limb identifier on a skip. Part 2's *"structured value naming the empty limb"* is a field of it, not a rival payload. **Post-redo Minor 3 closed.** |
| Clause 1 under an empty target limb | `sd:159–166` read against the transitive claim | **Direct case determined** (name-matching; the target file need not exist). **Transitive-through-absent-intermediate case undetermined. Finding 3** — post-redo Minor 4 is closed only for the case it named. |
| Broken blockquotes | script over both files: every `>`-block terminal line tested for sentence-final punctuation, and every post-blockquote line tested for lowercase continuation | **One hit, `sd:314`, which is a correctly closed quotation.** No broken blockquotes remain and the redo introduced none elsewhere. **Post-redo Minor 5 closed.** |
| Fresh-defect sweep: two-tree risk surface, unconditional *"otherwise it skips"*, un-narrowed announce-itself, scope omitting notebooks | `grep -n` for each phrase and its variants across both artifacts, every hit read | **Three clean** — the two-tree form, *"otherwise it skips"* and the withdrawn *"this unit has none"* survive only inside correction boxes and review history, which is the right treatment; `lc:61–62` and `lc:415` carry the narrowed form. **The fourth is not clean — `lc:129`. Finding 1.** |
| Do the three remediation sections contradict the body or each other? | all three read against §§ SD-E-01…SD-E-07 and `logical-components.md` | **No contradiction, one false completeness claim.** Post-redo row 2's *"at all four sites that state the scope"* is wrong on the derived count of five. Their characterisations of the superseded text (the denylist predicate, the *"otherwise it skips"* pairing, the `src/data/` masking path, *"would have produced one box"*) were checked against the earlier findings tables and are **accurate**. |
| Counts, all re-derived | enumeration and set-difference, printed before assertion | **7** design sections (SD-E-01…SD-E-07; SD-E-00 is a state record) ✓. **10** coverage rows in each artifact; membership `{REQ-ENG-9, FR-P1-04-3, -4, -9, -15, -17, -18, FR-P1-04-1, NFR-IRI-01, NFR-LEAK-01}`; **set difference empty in both directions** ✓. **4** unrowed (REQ-ENG-9, FR-P1-04-4, -15, -18) ✓. **3** components ✓. **5 / 2 / 2** split verified item by item, 5 + 2 = 7 ✓. FR-P1-04 difference `{2,5,6,7,8,10,11,12,13,14,16}` = **11** ✓. |
| `config.py` `__all__` and the five-name difference | parsed `src/data/config.py`'s `__all__`; `grep -n RAISES business-logic-model.md` | `__all__` = **17** names ✓. `RAISES` at **:104, :367, :478** exactly as cited ✓. Difference = `{DriverError, BenchmarkError, ComparatorError, ImportBoundaryError, FeatureAvailabilityError}` — **five**, none present in `__all__` ✓; **`AlignmentError` present in `__all__`** and correctly excluded ✓. |
| Workspace state on every limb asserted | `ls` per package; `ls tests scripts notebooks`; `ls -d configs` | **Confirmed.** `src/external|features|models|evaluation|gnss` = `__init__.py` only; `src/data/` = `config.py`, `locked_test.py`, `release.py`; `tests/` = six modules, **no `test_iri_denial.py`**; `scripts/` = two scripts, **no `04_build_external_products.py`**; **no `configs/`**; `notebooks/` = one notebook. |
| No satisfaction or discharge claim | § Assumptions and banners of both artifacts read in full | **Clean.** Both `TBD — freeze gate` values left unnamed; FR-P1-04-18 UNSET; `carry_forward_composition` `TBD`; `test_iri_denial.py` stated absent and the two coverage cells corrected **downward**; D-25's amendment stated ungranted; the interpreter recorded as off-pin and its output as non-evidence; the closing bullet refuses to authorise a module write. |
| Cited upstream lines | `evidence/DECISIONS.md` D-25 row and the §18.3 "Partially met" row; `components.md:63`; `requirements.md:462`; `requirements.md:370`; `business-rules.md:318` | **All verify verbatim**, including FR-WS-7's assignment to `config.py` and D-25's *"Requests, but does not take, a §15.2 amendment… until granted, EV-12's F10.7 limb is unmet at G-04."* |

### Post-redo findings — closed or not

| # | Sev | Status |
|---|---|---|
| 1 | **Critical** | **CLOSED at the predicate.** `logical-components.md`'s DISC-E-1 box now carries the allowlist complement and the full ordered switch, matching `security-design.md:114–121` exactly. The banner's and the remediation rows' claims about that box are now true of it. |
| 2 | Major | **NOT CLOSED.** The complement reached `notebooks/`; the **scan scope did not** (`lc:129`), and that site was named in the finding's own Location. Re-raised as **Finding 1** and escalated to Critical, because the half-repair opens a `passed`-over-an-unwalked-tree path the pre-repair text did not have. |
| 3 | Minor | **CLOSED.** One payload schema now serves both outcomes. |
| 4 | Minor | **CLOSED for the case it named** (absent target); the absent-intermediate case is newly stated as **Finding 3**, Minor. |
| 5 | Minor | **CLOSED.** Both blockquotes repaired; the sweep found no others. |

### Validation tool results

| Tool | Result | Interpretation |
|---|---|---|
| Stage-declared validation tools | **None declared** by the `nfr-design` stage definition | No tool output to interpret; every check above is manual and each names its command or method. |
| Workspace inspection (`ls`, `sed`, `grep`, Python `__all__` parse) | Ran clean | Used as the fact base for the counts and the disk-state claims. The interpreter present is **3.14.7, off the governed 3.11 pin** — the `__all__` parse is a text read, not governed evidence. |

### Coverage limits — what was NOT checked, and why

- **No sibling unit's `construction/<other-unit>/` content was opened, grepped or globbed**, per the read-scope bound. Cross-unit claims were checked only against the shared inception contracts (`requirements.md`, `components.md`) and `evidence/DECISIONS.md`.
- **`foundation`'s FR-WS-7 assertion was not inspected.** Whether it reads a structured skip reason is the routed dependency itself; this pass confirms the dependency is routed and owed, not that it is satisfied.
- **The scan was not executed** — it does not exist, and nothing in this unit does. Findings 1 and 2 are about the control's **specified reach**, not about a present violation; `notebooks/madrigal_phase1_coverage_audit.ipynb` cannot import `src/external/` today because those modules are absent.
- **No scientific value, gate status or acceptance row was assessed as discharged**, and nothing in this review authorises a module write, fills a `TBD — freeze gate` field, or takes a position on G-09/D-31.

### Summary

The post-redo Critical is genuinely closed: the two artifacts now state one predicate, one set of limbs, one precedence order and one payload, and the arithmetic, the `__all__` derivation, the `RAISES` set difference and the coverage-table set difference all verify. What recurred is the pattern this stage has now recorded four times — the notebooks repair widened the *limb* at four sites and left the *walk* narrow at the fifth, `logical-components.md:129`, the site the previous finding's Location named — and this instance is worse than a survival, because a notebook can now populate the limb over a tree the scan never opens and turn a vacuous result green. Finding 2 answers the question put to this pass directly and answers it yes: enumerating three directories is the same narrowing in a new costume, since the rule is an allowlist and `tests/` sits in its complement with six modules on disk, undisclosed.

**For the human at the gate.** **Finding 1 is a blocker** and is one line of text: make `lc:129`'s mechanism cell range over the same set `sd:114` defines, then re-derive the site count instead of trusting the repair's own list. **Finding 2 is a matter for you to weigh** — a real under-specification against `requirements.md:370` with a named consequence (a `tests/` importer is unwalked, and the denial test's own injection is unadjudicated), but a widening of an already-sound control rather than a contradiction inside it, dischargeable by disclosure as well as by extension. **Finding 3 is not a blocker.** The design's substance — the two-limb vacuity predicate with its precedence rule, the machine-readable skip, the flipped provenance default, the ordering-not-presence gates, the two-tier reliability posture, and the refusal to close the residual — remains sound, honestly bounded and reviewable; what is not yet safe to build from is that the component section an implementer opens first still tells them to walk a smaller tree than the check is specified to cover.

---

## Review — 2026-09-02 second-redo pass

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-02T19:43:03Z
**Iteration:** 1 of 2 — fresh budget after the second owner-directed redo.

The enumeration is genuinely gone, and the five-site walk/limb split that produced the last
Critical is genuinely closed. **The same failure recurred one level down.** The complement is
now stated over a **domain** — *"every Python module in the repository"*, **minus
`__init__.py`** — and that domain is narrower than the rule in two respects, both of which
land in the **walk** rather than only in the limb, because this revision declares the walked
set and the counted set to be the same set.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | **Critical** | `security-design.md:126`, `:135` (the definition block); `logical-components.md:135`, `:149`; against `requirements.md:370` and `business-rules.md:318` | **The complement's domain is "Python module", which does not reach a notebook — and "and notebook" is the exact phrase the previous pass's recommendation used and this repair dropped.** The post-redo terminal finding 2 recommended, verbatim, *"State the walked set as the allowlist complement itself — **every Python module and notebook in the repository** outside `scripts/04_build_external_products.py` and `src/evaluation/`"*. The block as written says *"every **Python module** in the repository that is not an allowlisted importer"* and *"**everything else**, repository-wide, excluding `__init__.py` files"*. A `.ipynb` is not a Python module and not a `.py` file; the stated mechanism is **stdlib `ast`**, which cannot parse a notebook without a cell-extraction step this design never specifies; and `__init__.py`, the one file type the definition names, is a `.py` filename, which fixes the domain's natural reading as `*.py`. `requirements.md:370` — the authority cited three times in this section — names *"a training script **or a notebook**"*; `business-rules.md:318` carries **`Import iri from a notebook → fails`** as a **required** R-56 negative control; `notebooks/madrigal_phase1_coverage_audit.ipynb` exists on disk. The only text in either artifact that puts notebooks in the walked set is the **historical correction box** at `:187–193`, which describes a superseded three-directory enumeration; the live definition supersedes it and does not carry it forward. So the artifact now states both readings and settles neither, and under the literal one R-56's required negative control is **not executable by the check as specified**. This is the fifth consecutive revision in which the repair restated a set more narrowly than the rule states it. | State the domain explicitly and by file kind, not by the word "module": *every Python source file **and every notebook** in the repository*, with one sentence saying a notebook is walked by extracting its code cells before the `ast` pass. Then set-difference the stated domain against the four importer classes `requirements.md:370` names and print the result, rather than against the previous wording. |
| 2 | **Critical** | `security-design.md:135` (`excluding __init__.py files`) read against `:128` (*"the walked set and the counted set are the same set"*); `logical-components.md:149` | **Subtracting `__init__.py` was a counting heuristic; unifying the walked and counted sets has just promoted it into the walk, and it removes the only file in which an `src/features` violation can be written today.** In every earlier revision the phrase *"beyond `__init__.py`"* qualified the **limb** — a defensible rule for deciding whether a risk surface is *populated*, since an empty package should not count as one. This revision declares the two sets identical, so the exclusion now governs what the scan **opens**. `src/features/`, `src/models/`, `src/gnss/`, `src/evaluation/` and `src/external/` each hold **exactly one file, `__init__.py` (24 bytes)** — verified on disk today. A single line `from src.external.iri import ...` placed in `src/features/__init__.py` is a violation of NFR-IRI-01 and of `component-dependency.md`'s `X` cell, it executes on any import of the package, and it is **by definition never walked**. The transitive case is worse and equally unstated: a chain `src/models/train.py` → the `src.features` package `__init__` → `iri` passes through a hop the walked set excludes, so a design that claims reachability *"directly or transitively"* has an unspecified answer for whether the walk follows an edge into a non-candidate module. | Separate the two sets again on this one point, and say so: `__init__.py` files are **walked** (they are executable import sites) but do not **count** toward the risk-surface limb's cardinality. Add one sentence stating that transitive expansion follows an edge into any module on disk, candidate or allowlisted, and that only the *origin* of a chain must be a candidate. |
| 3 | **Critical** | `security-design.md:209–216` (the unresolvable-INTERMEDIATE rule) against `logical-components.md:145–158` (E-1's DISC-E-1 box: the outcome switch and the payload sentence) | **The Minor repair landed in one artifact and not its sibling — the third time in this unit, and in the same box.** `security-design.md` adds a fourth outcome behaviour: an unresolvable intermediate **records an unresolved edge in the scan-scope payload** and the outcome is **`skipped`, not `passed`**. `logical-components.md` contains the strings "intermediate", "unresolvable" and "unresolved edge" **zero times** (grep, whole file). Its DISC-E-1 box presents the outcome switch as complete and closed — three clauses, `failed` / `passed` / `skipped` — and its payload sentence names only *"the candidate-importer set actually walked, by count and by path"*, omitting the unresolved-edge record. An implementer building E-1 from the component definition returns **`passed`** in precisely the state `security-design.md` requires `skipped`, on a partly-built tree, which is the state the repository is in. The re-save banner of `logical-components.md` lists what this revision changed and does not mention it. | Copy both halves into `logical-components.md`'s DISC-E-1 box — a fourth clause in the ordered switch and the unresolved-edge field in the payload — and correct the banner. Then re-derive the list of sites that state the outcome switch or the payload in either artifact and print it, rather than working from the repair's own list of what it touched. |
| 4 | Major | `security-design.md:196–200` (the ordered switch) vs `:209–216` (the intermediate rule) | **The new outcome sits outside the ordered switch, so its rank against clause 1 is unstated — and the natural reading masks a real violation.** The switch is presented as *the* precedence rule (*"a condition without one is not a control"*), and it has three clauses, none of which mentions an unresolved edge. The intermediate rule is stated two bullets later as *"the outcome is `skipped`, not `passed`"*, flatly, with no qualifier. On a partly-built tree — the state this design is written against — unresolvable intermediates will be **common**, so an implementer who applies the sentence as written skips whenever any edge anywhere in the graph fails to resolve, **including runs in which clause 1 has already found a reachability path elsewhere**. That is the same masking shape the terminal pass graded Critical (*"its repair could skip where one had been found"*), reintroduced by the fix for a Minor. The parenthetical *"the same treatment as an empty limb"* implies clause-3 rank and is the only thing pointing the other way; an implementer should not have to infer a precedence from an analogy. | Fold it into the switch as an explicit clause: **1** violation found → `failed`, regardless of unresolved edges or either limb; **2** no violation, both limbs populated, no unresolved edge → `passed`; **3** no violation, and either a limb empty or any unresolved edge → `skipped`, naming which. |
| 5 | Major | `security-design.md:134`, `:137–147` (the `tests/*` grant and its WS-10 justification); `security-design.md:812` (remediation row 3); against `component-dependency.md:34`, `:38–41` and `requirements.md:370` | **The grant's stated reason is an assumption that does not hold, and its evidence base is a blanket matrix row contradicted by prose in the same file.** (a) *"`tests/test_iri_denial.py` cannot perform WS-10's deliberate injection without importing what it is testing"* — WS-10's injection is of an **`iri_*` field**, a column name in a feature matrix. That is a data act; it requires no import of `src/external/iri.py`. `requirements.md:370`'s criterion states the two limbs separately: *"`tests/test_iri_denial.py` **fails** on deliberate `iri_*` injection; **the import-boundary check** passes and rejects an importer outside the two permitted ones"*. A test *of the import scan* would plausibly need a fixture that names the module — a real reason for a carve-out, and a much narrower one than `tests/*` — but the artifact does not give it. (b) I verified the matrix row: `component-dependency.md:34` does read `yes` in the `external.iri` / `external.gim` column. It also reads `yes` in **every other column of that row**, including `gnss`, which Phase 1 is barred from touching — it is a blanket "tests may import anything" row, not a considered grant. Four lines below it, the same file states: *"**Exactly two importers of `iri.py` and `gim.py`**, as TE §12 states it… **Everything else is forbidden**"*, and `requirements.md:370`'s criterion says the check *"rejects an importer outside **the two permitted ones**"*. The artifact records the discrepancy against **TE §12's wording only** and does not state that the matrix row contradicts the matrix's own prose and the passed requirement's pass/fail criterion — which is what a ruling would actually turn on. The consequence is not cosmetic: `tests/*` is now neither walked nor counted, so a path introduced through a test helper is invisible to the control. | Restate the justification as the import-scan fixture case rather than the field-injection case; narrow the carve-out to what that reason supports (the denial test's own fixture, named, rather than `tests/*` wholesale); and state all three sides of the discrepancy — TE §12, `component-dependency.md`'s own "exactly two" prose, and `requirements.md:370`'s "the two permitted ones" — when routing it. |
| 6 | Major | `security-design.md:634–655` and `logical-components.md:436–457` (both `## Assumptions & Open Questions`) | **The `tests/*` discrepancy is "recorded for a ruling" in a call-out box and is routed to nobody.** The box says it is *"Recorded as a discrepancy to be ruled on, not resolved here"*, but the string `tests/*` does not appear in either artifact's `## Assumptions & Open Questions` (grep, both files), it names no owner, and it raises no amendment — while Q1's preflight dependency, Q3's contract enlargement, the five-exception set and D-25 are each carried there and explicitly **"routed to the gate"**. This is the identical defect the terminal pass graded Major for Q1 (*"routed nowhere, names no owner, and raises no amendment"*), which this unit accepted and repaired for that item; it has reappeared for the item this revision introduced. A discrepancy that shrinks the allowlist's complement — the one set the last four Criticals were about — is not a smaller item than the two that are routed. | Add a bullet to both `## Assumptions & Open Questions` lists: the `tests/*` grant, the three-way conflict in finding 5, the owner (`component-dependency.md` is `application-design`'s artifact; TE §12 is the normative core), and an explicit **routed to the gate** for a yes or no. |
| 7 | Minor | `security-design.md:14`, `:124`, `:128`, and remediation row 2 of § Remediation of the post-redo TERMINAL pass; `logical-components.md:149` | **"Defined once … and never enumerated anywhere" is not true of the artifacts as saved, and one of the two bookkeeping claims about this repair is inaccurate.** `logical-components.md:149` restates the definition **in full** — allowlist members and the `__init__.py` exclusion — rather than referring to it, so the set is defined twice, in two files, which is exactly the configuration that produced the post-redo Critical. Remediation row 2's *"every other site refers to it rather than restating it"* is therefore wrong at that site. Row 2 also states *"The site list was derived and printed before any of the five was touched"*; no such list is printed in either artifact, and `project.md` § Way of Working requires a derived count to be printed where it is asserted, not asserted to have been printed. | Reduce `logical-components.md:149` to a reference plus the one fact E-1 needs (that `tests/*` is allowlisted by the matrix), or print the site list in the remediation row and drop the claim that every other site is a reference. |

### Checks actually run

| Check | Method | Result |
|---|---|---|
| Is *"everything else, repository-wide"* unambiguous for a static scan? | read `:126`, `:135`, `:128` together with the stated mechanism (stdlib `ast`) and the `__init__.py` exclusion | **No.** The domain word is "Python module" and the one named exclusion is a `.py` filename; `.ipynb` is neither. **Finding 1** |
| Does the previous pass's recommendation contain the dropped phrase? | read the post-redo terminal finding 2 recommendation in this file | **Confirmed verbatim**: *"every Python module **and notebook** in the repository"*. The repair kept the first half |
| Is a notebook still asserted to be in the walked set anywhere live? | `grep -n -i "notebook\|ipynb"` across both files, every hit read | **Only inside the historical correction box** (`:187–193`) describing the superseded three-directory form, and inside review history. **No live definitional site names a notebook.** `logical-components.md` names one only inside a quotation of `requirements.md:370` |
| `notebooks/madrigal_phase1_coverage_audit.ipynb` on disk | `ls -la notebooks/` | **Confirmed.** One notebook, 36,174 bytes |
| R-56's negative-control list | read `business-rules.md:316–321` | **Confirmed.** *"Import `iri` from a notebook → fails"* is one of five required controls |
| Does the `__init__.py` exclusion create a hole? | `:135` read against `:128`; `ls -la src/*/` | **Yes, and a current one.** `src/features`, `src/models`, `src/gnss`, `src/evaluation`, `src/external` each hold **exactly one file, `__init__.py`, 24 bytes**. The only writable violation site in `src/features` today is the file the definition subtracts. **Finding 2** |
| Any residual directory enumeration in a live scope-bearing sentence? | `grep -n "walked\|repository-wide\|candidate-importer\|reachability over"` across both files, every non-history hit read | **None.** The three-directory form survives only in correction boxes and review history — **the enumeration defect itself is closed**. The narrowing moved into the domain and the exclusion instead |
| `component-dependency.md`'s `tests/*` row against the `external.iri`/`external.gim` column | read the matrix, lines 22–36, and the prose at 38–41 | **`yes` — the artifact's claim is accurate.** Also `yes` in all seven columns of that row, and contradicted four lines below by *"Exactly two importers… Everything else is forbidden"*. **Finding 5** |
| TE §12 discrepancy stated honestly, and routed? | read the grant box; grep both `## Assumptions` sections for the literal | **Stated honestly; routed nowhere.** Zero hits in either Assumptions list. **Finding 6** |
| Is the WS-10 justification sound or assumed? | `requirements.md:370` pass/fail criterion read against the grant box | **Assumed, and it does not hold as stated.** The injection is of an `iri_*` **field**, not of the module. **Finding 5** |
| Same-artifact-pair check: set, limbs, precedence, payload | `sd:122–216` and `lc:135–158` read side by side, phrase by phrase | **Set: identical wording** (including both defects in findings 1 and 2). **Limbs: identical. Precedence: identical, three clauses. Payload: NOT identical** — `logical-components.md` omits the unresolved-edge record. **Finding 3** |
| Every other site stating scope, outcome or payload | `grep -n` for `walked`, `candidate-importer`, `regardless of either limb`, `skipped`, `unresolved`, `intermediate` across both files, every live hit read | **Scope sites: all agree. Outcome/payload sites: one divergence** — `logical-components.md` carries zero occurrences of the intermediate rule. **Finding 3** |
| Does the intermediate rule interact correctly with precedence? | `:196–200` read against `:209–216` | **Its rank is unstated and the literal reading masks a found violation. Finding 4** |
| Do the four remediation sections contradict each other or the body? | all four read end to end against § SD-E-01 as saved | **One inaccuracy** (row 2's "every other site refers to it", and an unprinted "site list was derived and printed"). Their accounts of superseded text are otherwise accurate — each superseded phrase quoted in a correction box was re-read and is quoted correctly. **Finding 7** |
| Broken blockquotes from this round | scanned every `>`-block in both files for a severed sentence or a table split across a box boundary | **None found.** The two the post-redo pass fixed are intact |
| 7 design sections | `grep -c "^## SD-E"` | **Confirmed.** 8 headings, SD-E-00 a state record → 7 |
| 10 coverage rows each, identical membership | ID extraction from both tables, set-difference both directions | **Confirmed, empty both ways.** REQ-ENG-9, FR-P1-04-1, -3, -4, -9, -15, -17, -18, NFR-IRI-01, NFR-LEAK-01 |
| 4 unrowed | blank acceptance cells, both tables | **Confirmed.** REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18 |
| `config.py` `__all__` = 17; the five-name `RAISES` difference | parsed `__all__` programmatically and printed it; `grep -n RAISES business-logic-model.md` | **Confirmed both.** `__all__` = 17 names; `RAISES` at **:104**, **:367**, **:478**, union = `{DriverError, BenchmarkError, ComparatorError, ImportBoundaryError, FeatureAvailabilityError}` = **5**, none of them in `__all__`; `AlignmentError` **is** in `__all__`, correctly excluded from the set |
| 11-ID FR-P1-04 difference | enumerated every `FR-P1-04-*` ID over `requirements.md` | **Confirmed.** Space = `{1…18}`; unit carries 7; difference = `{2,5,6,7,8,10,11,12,13,14,16}` = 11 |
| 5/2/2 and 3 components | re-derived against the `SD-E` headings; `grep -n "^### E-"` | **Confirmed.** 5 + 2 = 7; E-1, E-2, E-3 |
| "277 passed / 2 skipped" | `python -m pytest tests/ -q` | **Confirmed exactly**: `277 passed, 2 skipped in 4.29s` |
| Workspace state on every asserted limb | `ls` per package; `ls tests scripts notebooks`; `python --version` | **Confirmed.** `tests/` = six modules, **no `test_iri_denial.py`**; `scripts/` = two scripts, **no `04_build_external_products.py`**; **no `configs/`**; `src/data/` = `config.py`, `locked_test.py`, `release.py`; five other packages `__init__.py` only; interpreter **3.14.7**, off the 3.11 pin |
| No satisfaction or discharge claim | grep for `iricore` version, GIM product issue, `2000 km`, "satisfied", "discharged" across both files | **Clean.** Both freeze-gate values unnamed; FR-P1-04-18 stated UNSET; `tests/test_iri_denial.py` stated absent; D-25's amendment stated ungranted; `carry_forward_composition` left `TBD`; 0 rows claimed satisfied; nothing authorises a module write |

### Post-redo TERMINAL findings — closed or not

| # | Sev | Status |
|---|---|---|
| 1 | Critical (`lc:129` walk narrow at the fifth site) | **CLOSED.** `logical-components.md:135` now defines the mechanism by reference to the shared set and states *"the walked set is the counted set"*. The five sites state one set |
| 2 | Major (enumeration is the defect; state the complement) | **PARTLY CLOSED.** The enumeration is genuinely gone and no live sentence lists directories — that half is done. The complement's **domain** is narrower than the rule in two places, both now inside the walk: notebooks (**Finding 1**) and `__init__.py` (**Finding 2**). The recommendation's own phrase *"and notebook"* was dropped |
| 3 | Major (settle `tests/`) | **CLOSED as a statement, NOT as a justification or a routing.** `tests/*` is settled and the TE §12 discrepancy is recorded; the reason given is unsound and the discrepancy reaches no Assumptions list. **Findings 5, 6** |
| 4 | Minor (absent intermediate) | **CLOSED in `security-design.md` only.** Absent from `logical-components.md` entirely, and its precedence rank is unstated. **Findings 3, 4** |

### Validation tool results

| Tool | Result | Interpretation |
|---|---|---|
| — | The stage definition declares **no** validation tools | No tool output to interpret. Every check above was run by hand against the workspace, the passed shared contracts (`requirements.md`, `component-dependency.md`), and the declared upstream |

### Coverage limits — what was NOT checked, and why

- **The scan does not exist and was not executed.** Findings 1, 2 and 4 are about the control's **specified reach and outcome**, not about a present violation: `src/features/__init__.py` and the notebook cannot import `src/external/iri.py` today because that module is absent.
- **All sibling-unit characterisations remain unverified** and out of read-scope: the three `logical-components.md` criterion comparisons, the `governance-guards` R-23/R-24/R-28 and `inventory-and-registry` R-51/Q2 citations, and *"one amendment owed, part of five across three units"*. R-55's own limb was checked against `application-design/component-methods.md`; the roll-up is this unit's characterisation.
- **`domain-entities.md` § 9** was again read only through Finding 9's verbatim quotation inside `business-logic-model.md`.
- **`evidence/DECISIONS.md`:1854 and :1648** were relied on as quoted by the artifact and by the terminal pass, not re-opened this round.
- **`nfr-requirements`' own internal consistency** was not re-reviewed; only the claims § SD-E-00 supersedes were checked.

### Summary

The structural change is real and the previous Critical is genuinely closed: no live sentence in either artifact enumerates directories, and the five scope sites now state one set. **But the narrowing moved rather than stopped.** Defining the complement over *"every Python module … excluding `__init__.py`"* narrows it twice against a rule whose own authority names a notebook, and this revision's other headline decision — that the walked set **is** the counted set — is what turns both narrowings from counting heuristics into holes in the walk. The concrete state on disk makes them current rather than theoretical: the only notebook in the repository exists, and the only file in `src/features/` is the `__init__.py` the definition subtracts. Separately, the Minor repair reproduced the unit's other recurring pattern exactly — the unresolvable-intermediate rule is in `security-design.md` and nowhere in `logical-components.md`, whose E-1 box presents a complete three-clause switch and a payload that omits it, so the two artifacts once again specify different outcomes for the same tree, with the permissive one in the component definition an implementer builds from.

**For the human at the gate.** Findings 1, 2 and 3 are each a one-to-three-sentence edit and none requires a design change: name the file kinds instead of the word "module"; walk `__init__.py` while not counting it; copy the intermediate clause and its payload field into `logical-components.md`. Finding 4 is one clause added to the switch. Findings 5 and 6 concern the `tests/*` grant, which may well be the right answer — the grant is not challenged here, only the reason given for it and the fact that a discrepancy against TE §12, against `component-dependency.md`'s own prose and against `requirements.md`'s pass/fail criterion sits in a call-out box and reaches no Assumptions list while four smaller items are routed. The evidence discipline in the rest of the artifact remains high: every printed count re-derives, both coverage tables set-difference empty in both directions, the suite figure and every workspace limb verify exactly, and nothing is claimed satisfied or discharged.

---

## Review — 2026-09-02 second-redo iteration 2 (terminal)

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-02T20:05:23Z
**Iteration:** 2 of 2 on the second-redo budget — terminal. Advisory: no third pass follows,
and the findings below go to the human at the approval gate rather than back into a repair
loop.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | **Critical** | `security-design.md:103–105` (DISC-E-1), `:123` ("two causes"), `:686` (§ Assumptions); `logical-components.md:145–146` (DISC-E-1 box), `:349` (failure-domain table), `:466` (§ Assumptions) — against the definition block at `security-design.md:130–148` and clause 1's mechanic at `:247–252` | **The enumeration is gone from the definition and survives in the CONCLUSION drawn from it: DISC-E-1's premise is false under the design's own new definition, and the "cannot fail today" claim contradicts clause 1's own mechanic.** DISC-E-1 asserts as present fact that *"every module that could violate it (`src/features/*`, `src/models/*`, and any other importer) is **absent**"*, `logical-components.md:145–146` asserts *"every module that could violate it is **absent** — **two independent causes of vacuity**"*, and both § Assumptions state the check *"cannot fail today"*. **Derived and printed against the design's own definition** — `.py` files and `.ipynb` code cells, minus `scripts/04_build_external_products.py` and `src/evaluation/`, walk including `__init__.py` — the candidate-importer set today is **18 files walked, 12 counted**: the notebook, both `scripts/` modules, `src/data/config.py`, `locked_test.py`, `release.py`, all six `tests/` modules, and six `__init__.py` files. **The risk-surface limb is POPULATED today, not empty.** Only ONE of the two causes holds (the target side), so the correct outcome today is `skipped` naming the **target** limb — not the two-empty-limbs state both artifacts describe. Worse, *"cannot fail today"* is refuted by the design's own post-redo Minor-4 repair at `:247–252`: *"Clause 1 is decided by name-matching, not by file resolution… a violation is detectable with no target file present."* A line `from src.external.iri import x` written today into any of those 18 files is found by clause 1 and reports **`failed`**. The artifacts therefore assert both "clause 1 fires with no target present" and "the check cannot fail today", and those cannot both be true. **This is the recurring failure in its seventh costume**: the definition block was widened correctly, and the conclusion the OLD two-tree enumeration supported — *features and models are empty, therefore the risk surface is absent* — was never re-derived. The previous pass's own recommendation stated the answer verbatim (*"the limb is already populated today (`src/data`), which is the correct answer"*) and it is recorded nowhere in the design: `grep -n "populated today\|non-empty today"` returns only that review line. | Re-derive DISC-E-1 against the definition block and print the result: state that the **target** limb is empty and the **risk-surface** limb is **populated (18 walked / 12 counted today)**, so today's correct outcome is `skipped` on the target limb alone. Delete or restate *"cannot fail today"* at `security-design.md:686`, `logical-components.md:349` and `:466` — under clause 1's name-matching the check **can** fail today. Then re-check every sentence that depends on the two-empty-limbs premise, including `logical-components.md:141`'s *"per DISC-E-1 it cannot fail today"*. |
| 2 | Major | `security-design.md:156` (the `__init__.py` box), `:881` (second-redo remediation row 2, *"Verified on disk"*), `:727`; `logical-components.md:178` | **A figure asserted as verified on disk is wrong for three of the five files it names, and one of the five is not in the candidate set at all.** Both live boxes state that `src/features/`, `src/models/`, `src/gnss/`, `src/evaluation/` and `src/external/` *"each hold **exactly one file, `__init__.py`, 24 bytes**"*, and remediation row 2 prefixes it *"Verified on disk"*. `wc -c` today: `src/external` **24**, `src/features` **24**, `src/models` **22**, `src/gnss` **20**, `src/evaluation` **26**. Two of five, not five. Separately, **`src/evaluation/` is an allowlisted path**, so its `__init__.py` is by construction *not* in the candidate-importer set and does not belong in a list whose stated point is *"the one file an `src/features` → `iri` import could be written in is the file the count subtracts"*. The design conclusion (walk `__init__.py`, count without it) is unaffected and correct; what fails is the evidence, in the box that repairs the previous Critical, against `project.md`'s standing rule *"ALWAYS derive a count programmatically from the artifact and print it before asserting it"*. | Replace the "24 bytes" figure with the per-file byte counts actually measured, or drop the byte figure and say each package holds only an `__init__.py`. Remove `src/evaluation/` from that list or mark it as allowlisted-and-therefore-not-a-candidate. Correct remediation row 2's "Verified on disk" claim. |
| 3 | Major | `security-design.md:229` (*"`IMPL-3` and `IMPL-13` are open against exactly this allowlist-versus-denylist reading"*); absent from both artifacts' § Assumptions | **`IMPL-13` is misattributed, and the gap it actually records — that this check has no owning module — is carried nowhere.** `requirements.md:1020` defines it: *"`IMPL-13` \| Open \| Recorded inside FR-P1-04-1 as an authority-level silence, **no owning §12 module existing**"*, and FR-P1-04-1 itself says *"**No §12 module owns this check today** — an authority-level silence recorded here rather than left to be read as covered (`IMPL-13`)"*. That is not the allowlist-versus-denylist reading (`IMPL-3`); it is the absence of a home for the check. The consequence is a buildability gap in the artifact whose entire subject is this check: the design fixes the domain, the allowlist, the walked/counted split, the four-clause switch, the payload and the consumer — and never says which file implements it, while TE §12's mandated tree has no slot for it and the requirement records that silence as **Open**. § SD-E-01 enumerates what this unit owns (*"the check's reporting contract"*) and what it does not (*"the preflight that consumes it"*), and the producer's placement falls between the two, unclaimed and unrouted. Both § Assumptions lists route the §18.3 consumer, the exception sites, the provenance contract and the matrix row — not this. | Correct `:229` to cite `IMPL-3` for the allowlist reading and `IMPL-13` for the ownership silence separately. Add an `## Assumptions & Open Questions` item, on the same footing as the Q1/Q2/Q3 entries: **no §12 module owns the import-boundary check (`IMPL-13`, Open)** — state whether this unit proposes a home (`src/data/` is the only populated package and already holds `release.py`'s integrity logic) or routes the placement to the gate. |
| 4 | Minor | `security-design.md:243–246` against `:330–334`; `logical-components.md:182–184` | **The single payload schema the post-redo Minor 3 asked for is still not stated once, and the two artifacts now list different fields.** `security-design.md` says both payloads carry *"the candidate-importer set the scan actually walked — **count and module paths** — plus, on a skip, the identifier of the empty limb"*. `logical-components.md:182–184` says both carry *"the candidate-importer set actually walked, by count and by path, **plus any unresolved edges**"*. Neither is the union: SD omits unresolved edges from the payload sentence (it appears only in the intermediate-rule paragraph), LC omits the empty-limb identifier (it appears only in clause 4). The union is recoverable from each artifact by reading two places, so this is not a contradiction — but `foundation`'s FR-WS-7 consumer, which the design declares load-bearing, reads whichever schema is actually emitted, and no single sentence states it. | State one schema once, in the definition block, and refer to it from `logical-components.md`: `{outcome, candidate_count, walked_module_paths, unresolved_edges, empty_limb}` with `empty_limb` populated on a skip only. |
| 5 | Minor | `logical-components.md:20–22` (re-save banner) against `security-design.md:884` (second-redo review finding 3) | **A bookkeeping claim in the re-save banner undercounts the divergence history it exists to record.** The banner states this box carries all four corrections *"having diverged from its sibling **twice** before"*. The second-redo pass's own finding 3 states *"the **third** time this same box diverged"*, and the dispatch history records three. `security-design.md`'s banner makes no such count, so the two banners also disagree by omission. | Either state three, or state which two divergences the count covers and why the third is excluded. |
| 6 | Minor | `security-design.md:682` and `logical-components.md:468` (§ Assumptions) | **The `tests/*` matrix discrepancy is routed in prose but carries neither the artifact's own routing marker nor a named owner.** Both bullets say *"the blanket row is routed to the gate"*, and the substance is right — `component-dependency.md:34` reads `yes` in all seven columns and `:38` says *"Exactly two importers… Everything else is forbidden, including `src/data`, `src/gnss`, a training script and a notebook"* (**both citations verified exactly, at those line numbers**). But the three other routed items are tagged `— OPEN, routed to the gate` in their bullet headers and each names an owner (`foundation`, `features-and-splits`); this one is tagged `— the domain, the two sets, and the allowlist` and names none. It is also the only place this design overrides a literal cell of a passed shared contract, so it is the item a gate reader most needs to find. | Retag the bullet `— OPEN, routed to the gate` and name the ruling owner for a change against `component-dependency.md:34` / TE §12. |
| 7 | Minor | `security-design.md:132–136` (the domain), § SD-E-01 *"What is not reopened"* | **The domain's general clause is broader than its own enumeration, and the two residuals in the gap are undisclosed.** The domain reads *"everything that can execute Python in this repository"* and then enumerates *"`.py` files AND the code cells of `.ipynb` notebooks"*. Two things sit between them. (a) **Compiled bytecode**: `src/__pycache__/`, `scripts/__pycache__/` and `tests/__pycache__/` exist on disk and a `.pyc` executes Python and carries imports; it is in the general clause and outside the enumeration. (b) **Unparseable cells**: the mechanism is `ast` over extracted cells, and a cell containing an IPython magic (`%run`, `!python -c`) is not valid Python — `ast.parse` raises, and the design's cited R-27 rule says an unparseable file is a **failure**, not a file importing nothing, which would make such a notebook report `failed` spuriously. **Checked: today's `notebooks/madrigal_phase1_coverage_audit.ipynb` has 19 cells, 14 code, and 0 of 14 fail `ast.parse`** — so this is a residual, not a present defect. The *"What is not reopened"* paragraph discloses only the dynamic-import and run-time-computed-path residuals. | Add both to the disclosed-residual list beside the dynamic import, and state the intended behaviour for a cell that fails to parse (fail, or record an unresolved edge and skip — the switch already has a clause for the latter). |

### Checks actually run

| Check | Method | Result |
|---|---|---|
| **Sibling-divergence check — domain, allowlist membership, walked/counted split, four-clause switch, payload** | `security-design.md:130–160` and `logical-components.md:143–184` read side by side, clause by clause | **AGREE on four of five, and this is the first pass at which they do.** Domain: both *"everything in the repository that can execute Python — `.py` files and the code cells of `.ipynb` notebooks"*. Allowlist: both *"`scripts/04_build_external_products.py`; anything under `src/evaluation/`"* — **two paths, both artifacts**. Walked/counted: both *"walk entire, `__init__.py` included; only the cardinality count subtracts"*, both with the strict-superset sentence. Switch: **both carry all four clauses in the same order with identical conditions**, and both state clause 1 outranks clause 2 with the same *fact-versus-absence* reasoning. **Payload diverges — finding 4** |
| Term-by-term sweep: `intermediate`, `unresolved`, `__init__.py`, `ipynb`, `notebook`, `tests/*` | `grep -n -i` across both artifacts, every hit in live design text read | **Every live-design occurrence agrees.** `logical-components.md` now contains "intermediate" 4×, "unresolved" 9×, "ipynb" 4× (it contained the first two **zero** times last pass). No live sentence in either artifact enumerates directories or scopes the walk to `src/`+`scripts/`: `grep -n "over \`src/\`\|\`src/\` or \`scripts/\`"` returns **only review-history and remediation rows** |
| **Is the domain finally coextensive with the rule?** | enumerated every file kind in `src/`, `scripts/`, `tests/`, `notebooks/`; parsed the notebook's cells; checked `__pycache__` | **Coextensive for every artifact that exists or is planned in this repository — with two named residuals.** `.py` and `.ipynb` cover every importer class `requirements.md:370` names and every one `business-rules.md:316–321` requires a control for. The residuals are bytecode and unparseable cells — **finding 7**, neither of which is a present violation. **My answer to "would a seventh restatement find another gap": not in the domain. It found one in the CONCLUSION drawn from the old domain — finding 1** |
| **The `__init__.py` walked/counted split — on-disk claim** | `wc -c src/*/__init__.py` | **FALSE as stated. 24 / 24 / 22 / 20 / 26** for external / features / models / gnss / evaluation. Two of five, not five — **finding 2** |
| **Can the count be zero while the walk finds a violation, and does the switch handle it?** | traced the switch against a tree whose only candidate file is `src/features/__init__.py` carrying `import src.external.iri` | **Yes, and it is handled correctly.** Count = 0 (subtracted), walk finds the path, **clause 1 fires first and says "regardless of either limb"** → `failed`. The split creates no new inconsistency; ranking clause 1 above the limbs is exactly what makes it safe |
| **Candidate-importer set on today's tree, derived under the design's own definition** | walked `src/`, `scripts/`, `tests/`, `notebooks/`, subtracted the two allowlisted paths, printed the set before asserting | **18 walked / 12 counted.** The risk-surface limb is **populated**, contradicting DISC-E-1 in both artifacts — **finding 1** |
| **The withdrawn `tests/*` grant — is withdrawing it correct?** | `component-dependency.md` lines 23 (header), **34** (`tests/*` row), **38** (prose); `requirements.md:370`; R-56's controls at `business-rules.md:316–321` | **Correct, and the citations are exact.** `:34` reads `yes` in all seven columns; `:38` reads *"**Exactly two importers of `iri.py` and `gim.py`**, as TE §12 states it… Everything else is forbidden, including `src/data`, `src/gnss`, a training script and a notebook — which is the correction `IMPL-3` required"*. **`external.iri` and `external.gim` are one column**, and `src/evaluation` is `allowed` there while `X` against `gnss` — so the design's two-path allowlist matches the matrix's own prose. **WS-10 injects a field, not an import**: FR-P1-04-1's criterion is *"`tests/test_iri_denial.py` **fails** on deliberate `iri_*` injection"*. The withdrawal reasoning holds. Routing form — **finding 6** |
| **The four-clause switch — same order, same conditions, no contradicting sentence** | both switches diffed clause by clause; `grep -n "otherwise it skips\|regardless of either limb\|skipped, naming"` across both | **Identical, and no live sentence contradicts the ordering.** The superseded unconditional *"otherwise it skips"* survives only inside correction boxes and review history |
| Blockquote integrity — any severed sentence from this round? | programmatic scan for `>`-blocks ending mid-sentence or immediately followed by continuation prose, both files | **Clean. Zero.** Every blockquote is followed by a blank line; the two breaks the post-redo pass found are closed and none was introduced |
| Five remediation sections — mutual contradiction, and accuracy about superseded text | all five read against the body and against each other | **No contradiction between them; each correctly scopes itself to the pass it answers.** Superseded-text quotations spot-checked against the review findings they cite and **accurate**. **One false claim inside one: row 2's "Verified on disk… 24 bytes" — finding 2** |
| Re-save banners — false claims? | `security-design.md:5–24` and `logical-components.md:5–22` checked clause by clause against the body | **`security-design.md`'s banner: every clause true.** Domain, walk-includes-`__init__.py`, `tests/*` not allowlisted, intermediate rule inside the switch ranked below a found path — all four verified in the body. **`logical-components.md`'s banner: three clauses true, one undercounts — finding 5** |
| 7 design sections | `grep -c "^## SD-E"` | **Confirmed. 8 headings; SD-E-00 is a state record → 7** |
| 10 coverage rows in each artifact, identical membership, set-differenced **both** directions | both tables parsed programmatically, ID sets printed before comparison | **Confirmed. 10 and 10; A−B = ∅, B−A = ∅.** `{REQ-ENG-9, FR-P1-04-1, -3, -4, -9, -15, -17, -18, NFR-IRI-01, NFR-LEAK-01}` |
| 4 unrowed, in each table | `NO ACCEPTANCE ROW` cells counted programmatically in both | **Confirmed. 4 and 4** — REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18 |
| `config.py` `__all__` = 17, and the five-name `RAISES` difference | `__all__` parsed with `ast` and printed; `grep -n RAISES business-logic-model.md`; set-differenced | **Confirmed. 17 names**, `AlignmentError` present (so its exclusion from the missing set is right). Exactly three `RAISES` declaration lines — **:104**, **:367**, **:478** — union `{DriverError, BenchmarkError, ComparatorError, ImportBoundaryError, FeatureAvailabilityError}` = **5**, none in `__all__` |
| The 11-ID FR-P1-04 difference | ID space extracted from `requirements.md` by regex and printed | **Confirmed.** Space is exactly `{1…18}`; unit carries `{1,3,4,9,15,17,18}` = 7; difference = `{2,5,6,7,8,10,11,12,13,14,16}` = **11** |
| 5/2/2 decomposition; 3 components | re-derived against the SD-E headings; `grep -c "^### E-"` | **Confirmed.** 5 single-component + 2 shared = 7; **3** components; `DriverError`'s non-placement registered as a refusal with its reason |
| **No satisfaction or discharge claim** | grep for an `iricore` version/switch set, a GIM product issue, `2000 km`, FR-P1-04-18's rule, `test_iri_denial.py`, D-25, any pass/satisfied claim, any module-write authorisation | **Confirmed clean, on every limb the brief names.** Both `TBD — freeze gate` values remain **unnamed**; `2000 km` appears only as a quotation of FR-P1-04-15's own required report field; **FR-P1-04-18's interpolation rule is stated UNSET**; `carry_forward_composition` left `TBD`; **`tests/test_iri_denial.py` stated absent** in both banners, both § Assumptions and both coverage tables; **D-25's §15.2 amendment stated ungranted** with EV-12's F10.7 limb unmet at G-04; **0 rows claimed satisfied**; no gate, acceptance row or test claimed passing; nothing authorises a module write |
| Workspace state on every limb the artifacts assert | `ls` of `src/`, each `src/` package, `scripts/`, `tests/`, `notebooks/`; `wc -c` on every `__init__.py`; `python --version` | **Confirmed except the byte figure.** `src/data/` = `config.py`, `locked_test.py`, `release.py`; the other five `src/` packages hold only `__init__.py`; `tests/` = the six named modules, **no `test_iri_denial.py`**; `scripts/` = two, neither `04_build_external_products.py`; **no `configs/`**; `notebooks/` = one notebook; interpreter **3.14.7**, off the 3.11 pin |

### Second-redo findings — closed or not

| 2nd-redo # | Sev | Status |
|---|---|---|
| 1 | **Critical** (domain = "Python module") | **Closed in the definition, NOT in the conclusion.** The domain now reaches notebooks at every live site in both artifacts and cell extraction is named as a walk step. But DISC-E-1's *"every module that could violate it is absent"* was never re-derived against the widened domain, and it is false today — **finding 1**. The set was fixed; the inference the old set supported was not |
| 2 | **Critical** (`__init__.py` promoted into the walk) | **Closed in substance, with a false evidence figure.** Walk includes `__init__.py`, only the count subtracts, transitivity through a package `__init__` is walked, and the strict-superset sentence appears in both artifacts. The supporting "five packages, 24 bytes" claim is wrong for three of five — **finding 2** |
| 3 | **Critical** (intermediate rule in one artifact only) | **Closed.** `logical-components.md` now carries "intermediate" 4× and "unresolved" 9×, the four-clause switch in full, and the unresolvable-intermediate paragraph. **This is the first pass at which the DISC-E-1 box does not diverge from its sibling on the predicate** |
| 4 | Major (intermediate rule outside the switch) | **Closed.** It is clause 2 in both artifacts, with clause 1 stated to outrank it in identical words in both |
| 5 | Major (`tests/*` grant wrongly reasoned) | **Closed.** The grant is withdrawn, the WS-10 reasoning is corrected (a field injection, not an import), `test_phase_boundary.py`'s parse-don't-import technique is cited, and **the allowlist is TE §12's two paths in both artifacts** |
| 6 | Major (matrix discrepancy unrouted) | **Closed in substance, incomplete in form.** Both artifacts route it with exact line citations, both of which I verified. Missing the routing marker and an owner — **finding 6** |
| 7 | Minor (payload) | **Partially closed.** Both outcomes carry scan-scope evidence; the single schema is still not stated once and the two artifacts list different fields — **finding 4** |

### Validation tool results

| Tool | Result | Interpretation |
|---|---|---|
| — | The stage definition (`.claude/aidlc-common/stages/construction/nfr-design.md`) declares **no** validation tools | Nothing to interpret. Every check above was run by hand against the workspace, the declared upstream and the passed shared contracts. Every count was derived programmatically and **printed before being asserted**, per `project.md` § Way of Working |

### Coverage limits — what was NOT checked, and why

- **All sibling-unit criterion comparisons** (`foundation`'s failure-consequence axis, `governance-guards`' enforcement-timing axis, `inventory-and-registry`'s how-it-reaches-a-human axis), the `governance-guards` R-23/R-24/R-28 and `inventory-and-registry` R-51/Q2 citations, and the *"five amendments across three units"* roll-up: **out of read-scope, unverified**, and they remain this unit's own characterisation of other units' work. **No finding above depends on any of them.**
- **`foundation`'s FR-WS-7 assertion** — whether it will read the structured skip reason rather than count non-failures — is unverifiable from here. The artifacts correctly state it as owed, not satisfied.
- **`domain-entities.md` § 9's `DriverError` cell** was read only through carried Finding 9's verbatim quotation inside `business-logic-model.md`.
- The upstream `nfr-requirements` artifacts' own internal consistency was not re-reviewed; only the claims § SD-E-00 supersedes were checked.
- **Whether the notebook or any `tests/` module currently imports `src/external/*`** was not tested as a live violation — those modules do not exist, so no import of them can resolve. Finding 1 is about the artifacts' claim that the candidate set is empty, which is checkable and false, not about a present violation.
- **The `.pyc` residual in finding 7 was not exploited**, only observed: `__pycache__` directories exist and hold `.cpython-314.pyc` files. Whether the scan should walk bytecode is a design question, not a defect I demonstrated.

### Summary

**The sibling-divergence check passes for the first time in seven passes.** Read side by side, clause by clause, the two artifacts state the same domain, the same two-path allowlist, the same walked/counted split with the same strict-superset sentence, and the same four-clause switch in the same order with clause 1's rank stated identically. `logical-components.md` carries the unresolvable-intermediate rule it contained zero times last pass. `tests/*` is withdrawn from the allowlist in both, on reasoning I verified at source — WS-10 injects a field, and `component-dependency.md:34`'s blanket row is contradicted at `:38` by that artifact's own *"exactly two importers"*, both citations exact at those line numbers. The domain is now, in my judgement, **coextensive with the rule** for every artifact that exists or is planned here; the two residuals I found (bytecode, unparseable cells) are undisclosed rather than wrong. Every printed count re-derives: 7 sections, 3 components, 10/10 coverage rows with an empty set difference in both directions, 4 unrowed in each, `__all__` = 17, the five-name `RAISES` difference, the 11-ID FR-P1-04 difference, 5 + 2 = 7. Nothing is claimed satisfied, both freeze-gate values stay unnamed, FR-P1-04-18 is UNSET, `tests/test_iri_denial.py` is stated absent, D-25's amendment is stated ungranted, and nothing authorises a module write. No blockquote is broken.

**And the same failure recurred, one level up from the last one.** The five previous instances were narrowings of the *set*. This one is a narrowing that survives in the *inference drawn from the old set*. DISC-E-1 — the premise the entire E-1 component rests on, in both artifacts — still says *"every module that could violate it is **absent**"* and *"two independent causes of vacuity"*, and both § Assumptions still say the check *"cannot fail today"*. Derived under the design's own definition and printed before asserting: the candidate-importer set today is **18 files walked, 12 counted**, including three real `src/data` modules, both `scripts/` modules, all six test modules and the notebook. The risk-surface limb is populated; only the target limb is empty. And *"cannot fail today"* is refuted by the design's own clause-1 mechanic — name-matching, added specifically so a violation is detectable with no target file present — so the artifacts assert two things that cannot both be true. The previous pass's recommendation had already stated the correct answer in terms (*"the limb is already populated today"*); a grep shows it was never recorded anywhere in the design.

**Is this design now buildable?** Everything about the *control* is: an implementer can build the scan, the switch, the two limbs, the payload and the skip semantics from this text without asking a question, which was not true at any earlier pass. What is not buildable is the *state assessment* an implementer and a gate reader would act on. Told the check cannot fail today, an implementer has no reason to run it against the 18 files it would actually inspect, and a gate reader records an inert control where a live one exists. That is a one-paragraph fix — re-derive DISC-E-1 and delete three sentences — and it is the last one I can find.

**For the human at the gate.** **Finding 1 is a blocker in substance**: the artifacts assert a factual premise about today's workspace that is false under their own definition, and a claim (*"cannot fail today"*) that contradicts their own clause 1. It should not go to implementation as written, and the repair is smaller than any of the six before it. **Finding 3 is the one I would weigh most heavily after it, and it is not a repair of a repair**: `IMPL-13` records that no §12 module owns this check, that silence is misattributed at `:229`, and it reaches neither § Assumptions — so the most-specified control in this unit still has no home, and no gate item asks for one. **Finding 2** is a false "verified on disk" figure inside the box that repaired the previous Critical; the design conclusion survives it, but this project's own count-derivation rule exists for exactly this. **Findings 4–7 are matters to weigh, not blockers**: a payload schema stated in two halves, a banner that undercounts its own divergence history, a routed item missing its marker and owner, and two undisclosed domain residuals.

**On six passes.** Five of the six Criticals were introduced by the repair of the previous one, and this seventh is the same family — but it is materially different in kind, and worth saying so plainly rather than filing it as more of the same. The structural fix has held: the set is defined once, by complement, and no live sentence in either artifact enumerates a directory or a file type more narrowly than the rule. What remains is prose written under the superseded definition that was never re-derived against the new one. That is a bounded, enumerable class — the sentences that state what is true of the workspace *today* — and I would put to the owner that the fix be scoped exactly that way: re-derive every present-tense claim about the candidate set and the check's liveness against the definition block, print the derivation, and stop. A seventh repair aimed at the *set* would find nothing left to fix.

---

## Review — 2026-09-02 third-redo pass

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-03T09:43:15Z
**Iteration:** 1 (of 2; fresh budget after the third owner-directed redo)

The prior pass advised scoping any further repair strictly to **present-tense claims about the
candidate set and the check's liveness**. That advice was followed in `security-design.md`, and
the derived set it produced is **correct** — re-derived independently below, not checked
arithmetically. It was **not** carried into `logical-components.md` at two sites, one of which
is the sibling-divergence check that had passed for the first time on the seventh pass and now
fails again.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | **Critical** | `logical-components.md:150` (E-1, limb-1 row, "Built?" cell) and `logical-components.md:490` (`## Assumptions & Open Questions`) | **The superseded liveness claim survives in the sibling artifact at two sites, in present tense and outside any correction box — the exact Critical the seventh pass raised, repaired in the PRIMARY only.** (a) `:150` — the limb-1 mechanism table's "Built?" cell reads *"**No.** And per DISC-E-1 it **cannot fail today** — see below"*. This is the first statement about E-1's limb 1 an implementer meets, and it is contradicted three lines later by the correction box at `:153–167` (*"So the check is live, not inert… it reaches **clause 4**… over 18 files it really would inspect"*). (b) `:490` — an Assumptions bullet reads *"Limb 1 **cannot fail today**, because **neither its targets nor any potential violator exists — two independent causes**"*, sitting **immediately below** `:489`, the corrected bullet asserting the opposite. Its parenthetical cites an **older** correction (iteration-1 finding 1) and nowhere marks the bullet superseded, so the reader has no basis to prefer one over the other. **Sibling divergence:** `security-design.md` § SD-E-01 carries only the corrected form (`:137–139`, `:146–148`); it has no stale twin at either site. The divergence is therefore introduced by this round, against a check that passed on the seventh pass. This is the failure `project.md` § Corrections `fd-2026-08-30-sweep-derive-sites` and `fd-2026-08-30-sweep-numerals-and-surfaces` both describe: the correction landed in prose and in `## Assumptions` while a component's own mechanism table — what an implementer reads first — kept asserting the superseded version. | Two edits, both local, neither touching the design. At `:150` replace the "Built?" cell with the derived state: *"**No** — unbuilt. Live, not vacuous: reaches clause 4 and reports `skipped` naming the empty target limb, over 18 files walked, 12 counted."* At `:490` delete the superseded bullet outright (its content is fully carried by `:489`), or move it verbatim into a correction box explicitly labelled superseded. Do not leave two contradictory present-tense bullets adjacent. |
| 2 | Major | `security-design.md:240` (clause 2) and `:296–301`; `logical-components.md:181` | **The unresolved-edge rule never classifies a third-party or stdlib import, and the artifacts' central liveness claim depends on that classification.** The design defines an unresolvable intermediate only by example — *"if `a.py` imports `b`, `b` does not exist, and the chain `a → b → gim` therefore cannot be walked"* — and gives no rule for an import that resolves outside the repository. On today's tree that is decisive rather than academic: **all six `tests/` modules import `pytest`**, and every walked file imports stdlib. If a non-repository import is scored an unresolved edge, the check lands on **clause 2** (`skipped`, edge recorded), not **clause 4** (`skipped`, naming the target limb) — and the claim repeated at seven sites across both artifacts, that the check *"reaches clause 4"*, is wrong in exactly the clean CPU environment TE §13.2 governs, where `pytest` may not be installed. The outcome label a `foundation` FR-WS-7 consumer reads differs between the two clauses. An implementer cannot settle this from the text and must ask. | State the rule in the domain block beside the allowlist: an import that resolves to the standard library or to an installed third-party distribution is **not** an unresolved edge and terminates the chain as resolved; only an unresolvable **first-party** module path records one. Then re-derive the clause the check lands on today and confirm it is still clause 4. |

### Checks run, and their results

| Check | Method | Result |
|---|---|---|
| **The derived set, re-derived independently** (brief item 1) | `find src scripts tests notebooks -type f`, `__pycache__` discarded; walk = everything executing Python outside `scripts/04_build_external_products.py` and `src/evaluation/`; count = walk minus `__init__.py` | **18 / 12 HOLDS, exactly.** 18 `.py` on disk; minus `src/evaluation/__init__.py` (allowlisted) = 17; plus `notebooks/madrigal_phase1_coverage_audit.ipynb` = **18 walked**. Six `__init__.py` remain in the walk (`src/`, `src/data/`, `src/external/`, `src/features/`, `src/gnss/`, `src/models/`); 18 − 6 = **12 counted**. The enumeration at `sd:130–134` and `lc:161–165` matches the disk file-for-file. `src/evaluation/` is correctly excluded **as allowlisted, not as empty** — and it is in fact non-empty (26 bytes), so the distinction is load-bearing and correctly drawn |
| **`scripts/04_build_external_products.py` exists?** | `find scripts` | **Absent** — so the first allowlist path subtracts nothing today, correctly stated in the banner |
| **The liveness claim, PRIMARY** (item 2) | `grep -n "cannot fail\|two independent causes\|vacuous\|inert\|18 files\|clause 4\|skipped"` over `security-design.md`, every hit read | **Clean.** Every surviving *"cannot fail"* is either the § SD-E-01 section title (a general principle, not a workspace claim) or confined to a correction box quoting superseded text. `:112` *"vacuous"* is scoped to the **pre-design specification**, correctly. No present-tense "cannot fail today" survives |
| **The liveness claim, sibling** (item 2) | same grep over `logical-components.md`, every hit read | **FAILS at two sites — Finding 1.** `:150` and `:490` |
| **Clause 4 is the clause it lands on** (item 2) | Traced the four-clause switch against disk: target limb empty; risk-surface limb populated at 12; extracted every `import`/`from` statement in all 17 walked `.py` files | **Correct, subject to Finding 2.** No file names `src.external.iri` or `src.external.gim`, so clause 1 does not fire. Every first-party import resolves (`src.data.config`, `src.data.locked_test`, `src.data.release` all exist), so no first-party unresolved edge exists and clause 2 does not fire on that ground. Clause 3 fails on the empty target limb. **Clause 4 fires, naming the target limb** — as claimed. The residual doubt is third-party classification only (Finding 2) |
| **Sibling-divergence check** (item 3) | § SD-E-01 read against `logical-components.md` E-1 side by side | **FAILS.** Predicate, four-clause switch, precedence, allowlist, domain and payload all **agree**; the divergence is confined to the two liveness sites of Finding 1. It is narrower than the divergences of the third, fourth and fifth passes, but it is on the same fact and in the same direction |
| **`__init__.py` byte sizes** (item 4) | `wc -c` on all seven | **Correct.** external **24**, features **24**, models **22**, gnss **20** — all four verify. `src/evaluation/` is removed from the list and re-labelled allowlisted, as claimed. *(`src/` 19 and `src/data/` 20 are not asserted by the artifacts and are not defects.)* **Prior Minor closed** |
| **The routed discrepancy** (item 5) | Read both `## Assumptions` lists | **Present in both**, tagged `OPEN, routed to the gate`, owner named as **the project decision owner** — `sd:728`, `lc:493`. Citations `component-dependency.md:34`, `:38` and `requirements.md:370` all carried at both sites |
| **The unified payload schema** (item 6) | `sd:286–288` and `sd:373` against `lc:200–208` | **One schema, field for field**: the candidate-importer set actually walked, **by count and by module path**; **any unresolved edges**; and, on a skip, the **empty-limb identifier**. `failed`, `passed` and `skipped` all carry it. **Prior Minor closed** |
| **Printed counts** (item 8, partial) | Read the derived-count blocks | **3** components; **10** coverage rows *set-differenced in both directions, empty both ways*; **4** unrowed; **7** design sections decomposing as **5 + 2**. Arithmetic and set-difference method both correct as printed |
| **No satisfaction or discharge claim** (item 9) | Read the self-audit row at `sd:789` and the banner | **Confirmed clean.** Both freeze-gate values unnamed (no `iricore` pin, no GIM product issue); `2000 km` appears only as a quotation of FR-P1-04-15's own required report field; FR-P1-04-18 stated **UNSET**; `tests/test_iri_denial.py` stated **absent** (verified: it is not among the six `tests/` modules); D-25's amendment stated **UNGRANTED**; **0 rows claimed satisfied**; nothing authorises a module write |

### Are the prior pass's findings closed?

| Prior finding | Status |
|---|---|
| **Critical — stale inference about the workspace** ("candidate set empty", "cannot fail today", "two independent causes") | **PARTIALLY closed.** Fully repaired in `security-design.md`, and the replacement derivation is correct and independently reproducible. **Not** carried into `logical-components.md` at `:150` and `:490` — **Finding 1**. The repair was scoped to the PRIMARY, which is precisely the sweep failure the prior pass and two standing `project.md` corrections warn against |
| **Major — `__init__.py` byte sizes wrong; `src/evaluation/` listed as a candidate** | **CLOSED.** All four asserted sizes verify by `wc -c`; `src/evaluation/` removed and re-labelled allowlisted |
| **Major — matrix discrepancy routed nowhere, no owner** | **CLOSED.** Tagged `OPEN, routed to the gate` with an owner in both artifacts |
| **Minor — two different payload field lists, neither the union** | **CLOSED.** One schema, stated identically in both |
| **Did the repair introduce anything new?** | **Yes, one item.** Finding 1(b) — the corrected Assumptions bullet was **added** at `:489` without deleting the superseded bullet at `:490`, producing two adjacent contradictory bullets where previously there was one wrong one. This is a fresh defect of this round, and it makes five of eight repairs in this unit's history that introduced something |

### Validation tool results

| Tool | Result | Interpretation |
|---|---|---|
| — | **None run** | I did not reach the stage definition's validation-tool list before the interruptions. Recorded as a coverage limit, not as a pass |

### Coverage limits — what I did not reach

Two transport interruptions cut this pass. Per the coordinator's instruction I prioritised brief
items 1–3 and stopped verification at the point the second interruption reached me. **Not
checked, and not to be read as passing:**

- **Item 7 (fresh-defect hunt) — only partially done.** I read the four re-save banner
  paragraphs and found them mutually consistent, but I did **not** read the six remediation
  sections end to end against each other or against the body, and I did **not** sweep for
  broken blockquotes or severed sentences from this round. Finding 1 was reached through the
  liveness grep, not through this hunt; a systematic hunt could surface more.
- **Item 8 — three counts unverified**: `config.py`'s `__all__` = **17** and the five-name
  RAISES difference; the **11-ID** FR-P1-04 difference; and the **5 / 2 / 2** decomposition
  beyond confirming its printed arithmetic. I verified the counts' *method* (set-difference,
  printed derivation) but not these three values against their sources.
- **The stage definition and the Q&A file** were not opened. Q1–Q4 = A is taken from the
  dispatch brief, not verified against the receipted file.

### Summary

**No — not yet complete enough to build from, but the gap is narrow and precisely located.**

On the two questions the brief asks me to answer explicitly: the design is now **accurate about
its own workspace in the PRIMARY artifact** — I re-derived 18 walked / 12 counted from disk
independently and it holds exactly, the enumeration matches file-for-file, `src/evaluation/` is
excluded for the right reason, the byte sizes verify, and the claim that the check reaches
clause 4 and reports `skipped` over a live 18-file set is **true**. The seventh pass's judgement
that the **control is buildable** and the **domain is coextensive with the rule** survives this
pass unchallenged; I found nothing to add to either, and the prior advice that a repair aimed at
the *set* would find nothing left to fix is confirmed.

What defeats READY is not the design and not the derivation — it is that **the derivation was
carried into one artifact of two**. `logical-components.md` still tells an implementer, in E-1's
own mechanism table and again in its Assumptions list, that limb 1 *"cannot fail today"* because
of *"two independent causes"* — the precise sentence this revision exists to retire, in the
precise place `project.md`'s own standing corrections predict it will be missed. An implementer
reading the sibling first is told the control is dead; one reading the PRIMARY is told it is
live over 18 files. That contradiction, on Vision §7.1's binding architectural rule and on a
§18.3 critical item, is a **blocker, not a matter for the human to weigh** — a gate record
resting on the sibling's text captures a dead control where a live one exists, which is the
exact harm the seventh pass graded Critical.

It is, however, a **two-edit blocker**: one table cell and one deleted bullet, neither touching
the predicate, the switch, the allowlist, the domain or the payload — all of which I verified
agree across both artifacts. Finding 2 (third-party import classification) is a genuine
implementer question that should be settled in the same pass, since the liveness claim's own
clause depends on it, but it would not on its own have blocked. With those two edits and that one
sentence, I would expect the next pass to reach READY on this unit.

---

## Remediation of the third-redo pass — 2026-09-02

Two edits and one addition. **None touches the predicate, the ordered switch, the allowlist,
the domain or the payload** — the pass confirmed all five agree across both artifacts, and
none was reopened.

| # | Sev | Repair |
|---|---|---|
| 1 | **Critical** | **The seventh pass's Critical was repaired in the PRIMARY only, and `logical-components.md` went on asserting the superseded claim in present tense at two sites.** `:150`, E-1's limb-1 "Built?" cell — the first thing an implementer reads about limb 1 — said *"per DISC-E-1 it **cannot fail today**"* while the correction box three lines below said the opposite. And a **stale duplicate Assumptions bullet** survived immediately beneath its own replacement, so two adjacent present-tense bullets contradicted each other; it was a fresh defect of that round, created by adding the corrected bullet without deleting the old one. **The cell now states the derived truth (live, clause 4, `skipped` over 18 files) and the duplicate is deleted.** |
| 2 | Major | **A third-party or stdlib import is now stated to be no edge at all — neither walked nor recorded as unresolved.** The rule said nothing about them. **All six `tests/` modules import `pytest`**, so if that scored as an unresolved edge the scan would land on **clause 2** rather than clause 4, and the liveness claim repeated across both artifacts would be wrong **in exactly the clean CPU environment TE §13.2 governs**. An unresolved edge is now defined as a **first-party** import naming a repository module that does not exist. Stated in both artifacts. |

**What the pass confirmed, and it is worth recording because eight passes bought it.** The
candidate set was **re-derived independently rather than checked**: 18 `.py` on disk, minus
`src/evaluation/__init__.py` as **allowlisted** (and genuinely non-empty at 26 bytes, so the
distinction is drawn for the right reason), plus the notebook = **18 walked**; minus six
`__init__.py` = **12 counted**. Exact, and the enumeration matches disk file for file. Byte
sizes verify. **Clause 4 is the right clause** — no file names `src.external.iri` or `gim`,
and every first-party import resolves. The payload schema, the routed discrepancy with its
owner, and every printed count check out. Three prior findings genuinely closed.

**The pattern, at its eighth instance and unchanged in shape.** Six of the eight Criticals in
this unit's history were introduced by the repair of the previous one, and this one was the
same class as the fifth: **a correction applied to one artifact and not its sibling.** That
check has now failed four times and passed twice. The one thing that has caught it every time
is an adversarial reader holding the two artifacts side by side — which is the argument for
the reviewer step, not against it.

*(Section authored with the file-writing tools, per `project.md`'s rule that every
`produces[]` artifact carries a native write event.)*

---

## Review — 2026-09-02 third-redo iteration 2 (terminal)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-03T10:01:55Z
**Iteration:** 2 (terminal — no further pass follows)

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| — | — | — | **None.** Both iteration-1 findings are closed, and the repairs introduced no fresh defect within the reviewed scope. | — |

### Check 1 — the two stale sites in `logical-components.md` (was Critical) — **CLOSED**

| Site | Iteration-1 state | State now | Result |
|---|---|---|---|
| `logical-components.md` E-1 limb-1 "Built?" cell (was `:150`) | *"**No.** And per DISC-E-1 it **cannot fail today**"* — present tense, contradicted three lines below | *"**Unbuilt.** When built it is **live today**, not inert: the target limb is empty and the risk-surface limb is populated, so it reaches **clause 4** and reports **`skipped` over the 18 files it walks**. See DISC-E-1 below"* | **Repaired.** States the derived truth, and the first sentence an implementer meets about limb 1 now agrees with the correction box beneath it |
| The stale duplicate `## Assumptions` bullet (was `:490`) | A second, contradictory present-tense bullet — *"**cannot fail today** … **two independent causes**"* — sitting immediately below its own corrected replacement | **Gone.** `## Assumptions & Open Questions` now carries exactly **one** `[E-1 / DISC-E-1]` liveness bullet (`:497`), asserting target limb empty / risk-surface limb populated at 18 walked, 12 counted, clause 4, `skipped` | **Repaired.** No adjacent contradiction survives |

**Sweep of both artifacts** — `grep -n "cannot fail\|two independent causes\|inert\|vacuous pass today"` across `security-design.md` and `logical-components.md`, every hit read:

| Hit class | Sites | Disposition |
|---|---|---|
| § SD-E-01's section title, *"A check that cannot fail is not a control"* | `security-design.md:144` | **Legitimate.** A design principle, not a workspace claim — as the dispatch anticipated |
| Corrected statements (*"live, not inert"*, *"not inert"*, *"the check is live"*) | `security-design.md:137`, `:148`, `:744`; `logical-components.md:150`, `:165`, `:497` | **Legitimate.** Every one asserts the derived truth |
| Correction boxes quoting superseded text | `security-design.md:29`, `:122`; `logical-components.md:27`, `:160` | **Legitimate.** Each is explicitly framed as the superseded claim being withdrawn |
| Review sections (iterations 1 and earlier) and the remediation table | `security-design.md:938`–`:1523` | **Legitimate.** Historical record |
| *"vacuous"* scoped to the **pre-design specification** | `security-design.md:112` | **Legitimate.** Correctly scoped; not a claim about this design's check |

**No present-tense assertion that the check cannot fail, is inert, or passes vacuously survives anywhere in either artifact.**

### Check 2 — third-party and stdlib imports (was Major) — **CLOSED**

Present in **both** artifacts, in substantively matching terms:

| Artifact | Location | Content |
|---|---|---|
| `security-design.md` | `:296–301`, inside the clause-mechanics block | *"A third-party or stdlib import is **NOT an edge in this graph, and is NOT an unresolved edge**"*; the graph is **first-party only**; `pytest`, `pandas`, `numpy`, `pyyaml` and the stdlib named; *"an **unresolved edge** is therefore only a **first-party** import that names a repository module which does not exist"*; the `pytest` → clause-2 consequence stated with the TE §13.2 clean-CPU framing |
| `logical-components.md` | `:185–191`, inside the DISC-E-1 box, directly beneath the four-clause switch | The same rule, the same first-party-only framing, the same named exclusions, the same `pytest` → clause-2 consequence, and the same first-party definition of an unresolved edge |

**Consistency with the surrounding design — three checks, all clean:**

1. **Against the unresolvable-intermediate rule** (`security-design.md:308` onward; `logical-components.md:193` onward). No contradiction. That rule's own worked example is first-party by construction — *"`a.py` imports `b`, `b` does not exist"* names a repository module — and the new rule scopes an unresolved edge to exactly that case. The two rules partition the import space cleanly: outside the repository → not an edge at all; inside the repository and missing → unresolved edge, clause 2.
2. **Against the four-clause switch.** No clause is altered, reordered, or made unreachable. Clause 2 narrows its trigger; clauses 1, 3 and 4 are untouched. Clause 1's rank over clause 2 still holds and is still stated in both artifacts.
3. **Against the liveness claim.** The clause-4 landing is re-derived rather than merely re-asserted: with third-party imports excluded from the graph, the six `tests/` modules' `pytest` imports no longer create unresolved edges, no first-party import is unresolvable, clause 1 does not fire, and clause 3 fails on the empty target limb — leaving **clause 4, `skipped` naming the target limb**, as claimed. The claim now survives the clean CPU environment TE §13.2 governs.

### Check 3 — sibling divergence, scoped to the two repairs

**None introduced.** Repair 1 is by construction a divergence *closure*: the corrected form already stood alone in `security-design.md` § SD-E-01 (`:137–139`, `:146–148`) and now stands alone in `logical-components.md` too. Repair 2 landed in both artifacts in the same round, at the same structural position relative to the clause list, with the same rule, the same named exclusions, the same consequence and the same definition of an unresolved edge. § SD-E-01 and `logical-components.md` E-1 state one design.

### Check 4 — fresh defects in the repairs only

| Question | Result |
|---|---|
| Did deleting the duplicate Assumptions bullet sever anything? | **No.** Its content is fully carried by the surviving `:497` bullet, which is the one the earlier correction added. Nothing in either artifact cross-references the deleted bullet, and the `[E-1 …]` bullet series remains contiguous and well-formed |
| Does `## Remediation of the third-redo pass — 2026-09-02` contradict the body? | **No.** Its two rows describe exactly the two repairs verified above, and describe them accurately — the "Built?" cell, the deleted duplicate, the first-party-only rule, the `pytest` → clause-2 consequence, and *"Stated in both artifacts"* (verified true). No count or superlative in it was checkable-and-wrong |
| Does it contradict the earlier remediation sections? | **No.** It is additive: it repairs the seventh pass's Critical *in the sibling* and adds a rule that was previously absent, rather than restating one. No earlier remediation row is falsified by it |
| Broken blockquote from this round? | **No.** The `logical-components.md` DISC-E-1 box reads as one continuous `>` block from the limb table through the clause list, the new third-party paragraph, and the clause-1-outranks-clause-2 paragraph. The `security-design.md` insertion sits inside an existing numbered list at the same indent as its siblings |

### Are both prior findings genuinely closed?

**Yes, both.** Finding 1 (Critical) is closed at both named sites and confirmed by a four-term sweep over both artifacts, with every surviving hit accounted for. Finding 2 (Major) is closed in both artifacts, and — the part that matters — the rule was not merely inserted but reconciled: the clause the check lands on today was re-derived under it and is still clause 4.

### Coverage limits of this pass

This is a **bounded terminal pass**, scoped by dispatch to the four checks above. Everything else in these two artifacts was verified in **iteration 1** of this third-redo cycle and was **not re-checked here**: the 18-walked / 12-counted candidate set (re-derived independently there and found exact, its enumeration matching disk file for file), `src/evaluation/__init__.py`'s byte size and its allowlisted-not-empty status, the clause-4 landing traced against every import statement on disk, the payload schema, the routed `component-dependency.md:34` discrepancy with its named owner, and every printed count. Also unre-checked, and unchanged by this round: the items routed to the gate (D-25/EV-12, the `tests/*` allowlist discrepancy, `IMPL-13`'s unowned check, the `features-and-splits` two-half contract, `DriverError`'s placement). Those remain gate input, not review findings.

### Summary

**This design is now complete enough to build from, and accurate about its own workspace.** The last two defects were both defects of *statement* rather than of design — a component table asserting a superseded liveness claim, and a classification rule that was never written down — and both are repaired at every site within the reviewed scope, in both artifacts, without introducing a new contradiction. The control itself has been buildable for two passes: an implementer can construct the `ast` scan, the two-limb vacuity predicate, the ordered four-clause switch, the skip payload and the first-party edge rule from this text without asking an architectural question. What was missing until now was that the design also told the truth about what the check does on today's tree — it reaches clause 4 and reports `skipped` over 18 real files, rather than being the dead control seven earlier revisions described. It now does. The eight-pass pattern in this unit — a repair landing in one artifact and not its sibling — did **not** recur this round: the sibling check is the one I ran hardest, and both repairs are present in both files.

---

## Re-save note — 2026-09-04

A **fourth** owner-directed redo of `nfr-design` cleared every unit's checkpoint and review
receipts again. It was ordered to repair two Majors in **`target-standardization`**, not here.
**This unit was untouched by it**; the summary was re-confirmed and the artifact re-saved so
the receipts exist. **No claim in this document is altered by this note** — the complement
definition, the four-clause switch, the 18-walked / 12-counted derivation, the withdrawn
`tests/*` grant and every routed open item stand exactly as recorded above, on the ninth
reviewer pass's READY verdict.
