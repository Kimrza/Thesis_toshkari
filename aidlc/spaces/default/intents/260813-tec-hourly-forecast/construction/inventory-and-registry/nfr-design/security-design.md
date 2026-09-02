# Security Design — `inventory-and-registry`

**Unit** `inventory-and-registry` (Bolt 4) · **Kind** `library` · **Stage** `nfr-design`

> ## ⚠ THIS UNIT'S TWO MODULES DO NOT EXIST, AND NOTHING BELOW IS CLAIMED BUILT
>
> Written against the **workspace as it is on 2026-09-01**, per the owner's ruling that a
> design is written against current state while `nfr-requirements` itself stays unchanged.
> `nfr-requirements` for this unit was written on 2026-08-31 / 2026-09-01 and parts of it
> are already stale — the three claims are set out in § SD-I-00, and **two of the three run
> in this unit's favour**, which is why they are corrected rather than quietly inherited.
>
> **`src/data/inventory.py`, `src/data/registry.py`, `scripts/01_inventory_and_registry.py`
> and `tests/test_station_registry.py` do not exist.** Neither does `configs/`. Every
> design below describes what must be built, not what is.
>
> **Every acceptance row this unit touches is undischarged**: **WS-01, TA-04, TA-25**, which
> it owns, and **WS-18, TA-18, TA-32**, which it supports. **`FR-P1-02-7` and `FR-P1-02-8`
> carry no acceptance row at all**; `TA-29` was cited for the latter and is **withdrawn**.
> **G-09 is signed (D-31) with its own preconditions UNMET**; the TE §18.3 zero-TBD preflight
> has never run; `aws_ai_dlc_preflight_report` does not exist.
>
> **BLK-07's authorization limb is open.** No run may touch calendar 2022-12 while it stands,
> and **no December access occurs in this Bolt** — verified: `evidence/merge_run_access_log.jsonl`
> does not exist, and the only access log present is `evidence/test_run_access_log.jsonl`
> (158 rows, every one `purpose: coverage_audit`, from `test_release_hashes` and
> `test_acquisition_window`).
>
> **The IGRF version stays `TBD — freeze gate`.** No scientific value is decided here, and
> TE §18.2's absolute rule stands.

## Sources

- `../nfr-requirements/security-requirements.md` — **SEC-I-01** (the declared flag plus the structural import boundary), **SEC-I-02** (scoped, logged-before, reconciled), **SEC-I-03** (append-only record, all-or-nothing evidence), **SEC-I-04** (provenance and resolution integrity), **SEC-I-05** (the G-P1A record and the four prohibitions). **Three status claims superseded — see § SD-I-00.**
- `../nfr-requirements/tech-stack-decisions.md` — **TS-I-01** (the IGRF version is not pinned here), **TS-I-02** (stdlib `ast`, no new dependency, *"transitive is the load-bearing word"*), **TS-I-03** (a governed schema, self-contained report), **TS-I-04** (the station registry is not the experiment registry), **TS-I-05** (two platforms; Kaggle durability unmeasured).
- `../functional-design/business-logic-model.md` — **W-1** … **W-9**, and § Requirement-to-workflow map.
- `../functional-design/business-rules.md` — **R-44** … **R-53**.
- **`performance-requirements.md`, `scalability-requirements.md` and `reliability-requirements.md` are absent by `produces_kinds` design** — `nfr-requirements` maps them to `[service, ui]` / `[service]` / `[service]`, and this unit is `library`. They are assessed in § Scope note rather than treated as a gap.
- **The workspace, read 2026-09-01** — `src/data/config.py`, `src/data/locked_test.py`, `src/data/release.py`, `scripts/merge_coverage_year.py`, `tests/` (six modules), `evidence/test_run_access_log.jsonl`.
- `../../../inception/application-design/component-dependency.md` — the dependency matrix, its `—` versus `X` distinction, and the `scripts/*` row.
- `../../../inception/application-design/component-methods.md` — `Station`, `load_registry`, `assert_registry_resolved`, `write_release`, `AccessRecord`, `open_restricted`.
- `../../../inception/application-design/services.md` § The nine stage scripts — `01_inventory_and_registry.py`, P1-02, Phase 1 and 2.
- `../../../inception/requirements-analysis/requirements.md` — **FR-P1-02-1** … **-5**, **-7**, **-8**; **NFR-AUD-01**, **NFR-DQ-01**, **NFR-SEC-01**, **NFR-REP-01**, **NFR-PHASE-01**.
- `nfr-design-questions.md` — **Q1 = C**, **Q2 = A**, **Q3 = A**, **Q4 = A**, and the receipted Consolidated Summary Confirmation.

---

## Scope note

`produces_kinds` yields two artifacts for a `library` unit — this one and
`logical-components.md`. The three absent categories are assessed rather than skipped:

| Category | Assessment for `inventory-and-registry` | Where it lives |
|---|---|---|
| **Performance** | No latency target. The audit's cost is bounded by its declared scope and is deliberately **not** optimised: R-25 forces a durable log write **before** each read of a **December-bearing** artifact, a per-artifact synchronous `os.fsync` accepted on purpose. `src/data/locked_test.py` already implements exactly that. | § SD-I-04 |
| **Scalability** | Bounded and known — twelve months, three cells, named artifact classes. No growth projection exists and none is invented. | — |
| **Reliability** | **Fail-closed at three separate points**: a short scope declaration fails before the first artifact is opened; a log-write failure aborts the read; a reconciliation mismatch fails after the counts. An interrupted audit yields **no report**. | § SD-I-04, § SD-I-05 |
| **Security** | This artifact. | — |
| **Observability** | One access row per **December-bearing** artifact read, carrying `run_id`, `purpose`, `performance_inspected` and a guard-stamped `logged_at_utc`. The other eleven months are ordinary paths and produce no access row; they are reconciled against the coverage report's own per-month output instead. | § SD-I-04, § SD-I-05 |

---

## SD-I-00 — What is on disk, and the three upstream claims it contradicts

Derived by direct inspection on 2026-09-01, printed before it is relied on.

| Upstream claim | State on disk | Direction |
|---|---|---|
| SEC-I-02 § Status: *"Cannot run. BLK-07 is open and `acquisition`'s accessor does not exist."* | **Half stale.** The **read** chokepoint exists: `open_restricted` (`src/data/locked_test.py:147`), `AccessRecord`, the validated `PURPOSES` frozenset, and `_append_and_flush` with `os.fsync`. The **write** contract (R-33) does **not** exist. | **In this unit's favour** — the mechanism W-6 routes through is real, not proposed. |
| SEC-I-01 limb 1: *"Every access row the audit writes carries `performance_inspected=false`"* | **Built and enforced.** `AccessRecord.performance_inspected` is a required field; `purpose` is validated against `frozenset({"coverage_audit", "regime_audit", "locked_evaluation"})`; `locked_test_accessed` must be `True`. W-6's **two typed rows** are already expressible today. | **In this unit's favour.** |
| `business-logic-model.md` W-9: *"`src/data/inventory.py`, `src/data/registry.py`, `scripts/01_inventory_and_registry.py` and `tests/test_station_registry.py` DO NOT EXIST, and neither does `src/` or `configs/`. `tests/` holds three modules."* | **Partly stale, and the stale part does not help.** `src/` exists with all six §12 packages; `src/data/` holds `config.py`, `locked_test.py`, `release.py`; `tests/` holds **six** modules. **`configs/` and all four of this unit's named files still do not exist.** | **Neutral** — the scaffolding moved, this unit's own work did not. |

**Three facts run the other way and are stated here rather than discovered later.**
*(Two at first issue; DISC-I-3 registered 2026-09-01 on adversarial finding 5.)*

**DISC-I-1 — no approved component owns the audit's outputs.** `services.md` gives
`01_inventory_and_registry.py` the outputs *"source inventory (§5.1 nine fields), station
registry"*. It does **not** name the coverage report or the regime-count report. Grepped
across `services.md`, `components.md` and `component-methods.md` for `coverage report`,
`coverage_report`, `regime count`, `regime-count` and `regime_count`: **zero matches in all
three**. W-6 designs the audit and `unit-of-work.md` assigns it here, but **no approved
application-design row says which script produces its two artifacts.** This bears directly
on § SD-I-01, because a boundary must bind the script that hosts the audit, and that script
is not yet named. Recorded as an open seam, not resolved here.

**DISC-I-2 — the `retrieved_at_utc` placeholder is still in the migrating script.**
`scripts/merge_coverage_year.py:87-95` builds its `AccessRecord`, and **`:89`** sets
`retrieved_at_utc='recorded-at-call-time-by-the-runner'` — a literal placeholder, for every
row. `locked_test.py`'s own docstring records this defect being found by execution on
2026-08-28 and names `logged_at_utc` as its fix. The fix is real and the placeholder is
still there: the guard-stamped field carries the ordering evidence, and the caller-supplied
field says nothing. When `merge_coverage_year.py` migrates into
`01_inventory_and_registry.py` (W-9), that placeholder migrates with it unless it is
replaced. **Named as a migration obligation, not fixed here** — this stage writes no code.

**DISC-I-3 — two `acquisition`-owned requirements land in this unit's module and appear in
no coverage table** *(registered 2026-09-01 on adversarial finding 5, Minor — the seam was
discussed in `business-logic-model.md` W-1's box but was never given a discrepancy ID, while
DISC-I-1's analogous seam was)*. `components.md:64` assigns `inventory.py` the requirements
**`FR-P1-01-6`** (the frozen driver-acquisition contract, whose provider acknowledgment text
must be reproduced verbatim) and **`FR-P1-01-2`** (the full provider filename including its
version suffix, with a suffix mismatch surfaced rather than silently accepted). Both are
`FR-P1-01-*` — **`acquisition`'s** requirement space, not this unit's — and neither appears
in this unit's coverage table, correctly, because `functional-design` fixed this unit's set
as `{FR-P1-02-1,-2,-3,-4,-5,-7,-8}`.

**The seam is that the module is this unit's while the requirements are not.** § SD-I-06
states the design consequence — the verbatim acknowledgment notice is kept as a **distinct
field** from the operational access notes, so a redaction rule cannot mangle text that must
not change. The **suffix-mismatch surfacing** half is weaker still: W-1's box already marks
it **⚠ PROPOSED, not settled**, because `acquisition` R-34 holds the release-manifest
carriage of `suffix_mismatch` **Open for stage 3.2**. Registered here so it is tracked
rather than resting in one upstream box. **No acceptance row is asserted for either**:
`components.md:169`'s `TA-08`/`TA-12` reference is the grep for absent SSN, residual and GRU
modules and has nothing to do with `inventory.py`.

## SD-I-01 — The audit's import boundary: two limbs, neither substituting for the other (Q1 = C)

SEC-I-01 limb 2 requires the December-audit code path to import **no** module under
`src/models/` or `src/evaluation/`, *"directly or transitively"*. Three workspace facts
decide what that can mean in practice, and all three were checked:

1. **`component-dependency.md` marks the relevant edges `—`, not `X`.** Its `src/data` row
   reads `models: —` and `evaluation: —`. The matrix states the consequence in its own
   words: *"`X` marks a forbidden edge, not an absent one: the difference matters, because
   a forbidden edge needs a test and an absent one does not."* **Today no test is owed on
   either edge**, which is precisely why SEC-I-01 limb 2 has nothing to attach to.
2. **The stage script is explicitly permitted to import both.** The matrix's
   `scripts/*` (all others) row reads `models: yes`, `evaluation: yes`.
   `01_inventory_and_registry.py` sits in that row. A boundary stated over `src/` alone
   would leave the script that **calls** the audit free to import what the audit may not.
3. **No transitive closure exists anywhere in the repository.**
   `tests/test_phase_boundary.py`'s `_imported_modules` parses **one file's direct
   imports** with stdlib `ast`. It is the right primitive and it is not the check.

**Design — two limbs, each a separately named result.**

**Limb A — a package-wide forbidden edge.** `src/data/*` and
`scripts/01_inventory_and_registry.py` may not import `src/models/*` or `src/evaluation/*`.
Enforced by applying `_imported_modules` to **every file in the constrained set**: if each
member is checked directly, a chain that stays inside the set is caught at its first hop.
**The change record this owes is three edits, not two** *(corrected 2026-09-01 on
adversarial finding 3, which was Major — the first issue scoped it to "two matrix cells" and
so under-described the larger of the two deviations)*:

| # | Edit to `component-dependency.md` | Deviation class |
|---|---|---|
| 1 | `src/data` → `models`: **`—` → `X`** | Promotes an **absent** edge to a **forbidden** one. The matrix itself says the difference is that a forbidden edge owes a test |
| 2 | `src/data` → `evaluation`: **`—` → `X`** | Same class as 1 |
| 3 | `scripts/*` (all others) row: a **named carve-out** for `01_inventory_and_registry.py` against `models` and `evaluation` | **Contradicts an affirmative `yes` grant.** Larger than 1 and 2: promoting `—` to `X` records an obligation the matrix did not have, while this **withdraws a permission the matrix explicitly gives** |

Edit 3 is the one a reviewer of the change record should look at hardest, and it is named
first in the record for that reason. **The change record is owed, not written here.**

**Limb B — an entry-point reachability closure.** Build the module graph across `src/` and
`scripts/` from the same `_imported_modules` primitive, close it transitively from the audit
entry point, and fail if the closure contains any module under `src/models/` or
`src/evaluation/`. This is the limb that catches a chain **leaving** the constrained set —
audit → `src/external/spaceweather` → `src/evaluation` — which Limb A structurally cannot
see, because `src/external` is not in its set.

**Why both, stated as the reason and not as a preference.** Limb A cannot see through an
unconstrained package. Limb B leaves the matrix saying the edge is merely absent, and the
matrix itself says an absent edge owes no test — so a future reader of the matrix would find
no obligation recorded where one now exists. Neither is a superset of the other, which is
the same shape this unit already uses for its scope validation (W-6's three checks, where
*"only the declared-versus-required check proves it declared everything required"*) and that
`governance-guards` uses for R-23's two limbs.

**Three implementation constraints this design fixes, so 3.5 does not re-decide them.**

- **Unparseable is a failure, not a skip — and the existing helper already gets this
  right.** *(Corrected 2026-09-01: the first issue asserted that `_imported_modules` "today
  swallows a parse error". **That is false.** `tests/test_phase_boundary.py:112-115` reads
  `except SyntaxError as exc:  # a file that will not parse cannot be cleared` →
  `pytest.fail(...)`, and it is the only `ast.parse` call in `src/`, `scripts/` or `tests/`.
  The constraint below stands; its justification was a fabricated present-day defect and is
  withdrawn.)* The requirement on the closure is therefore **preservation, not repair**: it
  must not introduce a swallow that the direct-import primitive does not have, which is a
  live risk because a graph walk visits far more files than a single check and a
  `try: ... except Exception: continue` is the natural way to keep it running.
  `governance-guards` R-27 fixes the rule; `_imported_modules` already implements it.
- **Cycles terminate the walk, they do not fail it.** A revisited module is skipped; a cycle
  is not itself a violation.
- **A dynamic or computed import the walker cannot resolve is reported, never assumed
  clean.** An unresolved edge is the one case where a static walker can be silently wrong,
  and silence is the failure mode this whole boundary exists to prevent.

**The negative control is what proves it**, following WS-10's pattern for the IRI denial
test: **each limb must fail on a deliberately introduced import** — a direct one for Limb A,
a two-hop one through an unconstrained package for Limb B. Two injections, two separately
named results. `team.md` § Testing Posture makes this mandatory for every hard rule, not
optional.

**What this does NOT constrain.** The audit's **right to run**. SEC-I-01 states it and it is
restated here because the distinction is the load-bearing one: Vision §8.3 makes the
performance-blind coverage and regime audit a **precondition of G-05**, and a guard that
blocked it would breach §8.3 as surely as one that let a model see December. This design
constrains **what the audit may import**, never **whether it may run**.

**NFR-PHASE-01 is not weakened, and no coverage of it is claimed.** Limb B reuses
`test_phase_boundary.py`'s `_imported_modules` primitive; it must not modify that module's
existing `PHASE1_PERMITTED_PACKAGES` behaviour, which permits `models` and `evaluation` for
the phase check and forbids `gnss`. The two boundaries answer different questions over the
same primitive. NFR-PHASE-01 is `governance-guards`', and this artifact states an obligation
against it rather than covering it.

## SD-I-02 — Where `InventoryError` and `AuditScopeError` live (Q2 = A)

W-1 declares `RAISES InventoryError`; W-6 declares `RAISES AuditScopeError`. **Neither
exists.** Both are **declared in `src/data/config.py`, derive from `IntegrityError`, and are
added to `__all__`.**

**Neither is claimed as an R-01 enumeration entry.** They ride R-01's *"any future
integrity-related exception"* clause, on the `InverseTransformError` precedent. The
discriminator that promoted `PartitionError` into the enumeration was a **cross-unit
disagreement to reconcile** — two units raising one exception for conditions that had to be
made to agree. **Both of these are raised by this unit alone**, so there is nothing to
reconcile, and R-01 *"deliberately stopped asserting a count after its enumeration went
stale twice."* **`config.py` records that sentence**; without it, two names in `__all__`
absent from the enumeration read as an oversight.

**Why `config.py` and not this unit's own modules.** The 2026-08-28 owner ruling moved
`PartitionError`'s **declaration site into `config.py`** while leaving its semantic owner
elsewhere, for the stated reason that an exception declared in a leaf module cannot be
caught by a package forbidden from importing that module. § SD-I-01 makes that concrete
here: under Limb A, `src/data/*` is forbidden from importing `src/evaluation/*`, so an
exception the evaluation layer might one day catch must not live behind that edge.

**Constructor contract, inherited unchanged.** R-01 requires every raise to name the
**resource** and the **violated expectation**. For `AuditScopeError` the resource is the
**declared scope**, never a file path — the raise happens **before any artifact is opened**,
and naming a file would imply a read that did not occur.

> ## ⚠ THERE IS A THIRD MISSING EXCEPTION, AND Q2 NAMED ONLY TWO
>
> Derived at this stage by set-differencing the `RAISES` lines in
> `business-logic-model.md` W-1 … W-6 against `src/data/config.py`'s `__all__`, printed
> before it is asserted. `__all__` holds 17 names; W-5 declares **`RAISES SchemaError`**,
> and **`SchemaError` is not among them**. The set difference is
> `{InventoryError, AuditScopeError, SchemaError}` — **three**, not the two Q2 put to the
> owner.
>
> **This is raised, not decided.** Q2's ruling was given on a two-item scope, and
> `project.md` records that a ruling given on a scope that misdescribes the work must have
> the correction stated before the ruling is acted on. The same reasoning applies to
> `SchemaError` on its face — one unit raises it, there is no cross-unit meaning to
> reconcile, and it therefore rides R-01's any-future clause exactly as the other two do —
> but **applying an owner's answer to an item the owner was not shown is the widening this
> project has already had to correct once.**
>
> **Proposed disposition, for the gate:** treat `SchemaError` identically to the other two —
> declared in `src/data/config.py`, deriving from `IntegrityError`, added to `__all__`, not
> claimed as an enumeration entry. **Flagged at the approval gate as an extension of Q2, for
> an explicit yes or no.** Nothing is written to `config.py` by this stage either way.

## SD-I-03 — The `RegistryError` collision (Q3 = A)

`src/data/config.py` declares `RegistryError` as *"An experiment-registry write would be
lost, silently overwritten, or reordered"* — `foundation`'s experiment registry (R-08, R-18,
TE §13.4). **W-2 declares the station registry build `RAISES RegistryError`** — the same
class, for a missing §6.2 field, a **defaulted rather than pinned** `igrf_version`, or a
conflict **resolved by averaging**.

**The failure this creates, stated concretely.** A caller writing
`except RegistryError:` to retry or report a lost registry **write** would swallow a
station-registry **provenance** failure — the exact defect class W-3's entire mechanism
exists to make loud.

**Design: the class stays, and the two are discriminated by `resource`.**

1. **W-2's `RAISES RegistryError` is an approved `functional-design` contract and is not
   changed here.** `project.md` records the rule this obeys: a stage answer cannot move a
   requirement out of the layer the authority document places it in.
2. **`config.py`'s docstring is widened** to name both registries and to state that the two
   are told apart by the resource, not by the type.
3. **Every station-registry raise names its registry artifact as the resource** — the
   registry file or the `station_id` whose field failed. R-01's constructor already refuses
   an empty resource, so the discriminator exists today and costs nothing to adopt.

**The residual is recorded, not designed away.** A caller catching `RegistryError` **by
type** still cannot separate a lost experiment-registry write from a station-registry
provenance failure. Only a caller that reads `.resource` can. **Type-level separation
remains available** as a change record against `functional-design` — proposing
`StationRegistryError` beside `RegistryError` — and that route is named here rather than
taken, because taking it from this stage would be the overreach `project.md` warns against.

## SD-I-04 — The audit, designed against the guard that now exists

SEC-I-02's three checks are unchanged. What changes is that **two of the three now attach to
real code**, and this section says exactly where.

**Check 1 — declared versus required, before any read.** The audit declares its scope up
front. That declaration is compared against a **governed reference set derived from the
release inventory** — twelve 2022 months, **December as the full calendar month, 1–31**, all
three cells, the named artifact classes — never against the declaration itself. A short
declaration raises **`AuditScopeError` before the first artifact is opened**. This check has
**no existing code to attach to** and is entirely this unit's to build. It is the only one of
the three that proves **completeness**; W-6 records that an audit declaring eleven months and
executing eleven reconciles cleanly and raises nothing.

**Check 2 — every read of a December-bearing artifact logged, durably, before it happens.**

> ## ⚠ CORRECTED 2026-09-01 — THE FIRST ISSUE OF THIS SECTION WAS UNBUILDABLE
>
> It said *"every read"* of the twelve-month declared scope routes through
> `open_restricted`. **That design cannot be built**, and the same paragraph quoted the
> reason approvingly two sentences later. Verified by direct inspection: `evidence/` holds
> `audit_evidence_2022-01` … `audit_evidence_2022-11` **outside**
> `evidence/locked_test_restricted/`, which contains only `audit_evidence_2022-12`,
> `audit_evidence_2022-FULL`, two `superseded_*` directories and two loose artifacts.
> `src/data/locked_test.py:173` raises `LockedTestError` for **any path not under the
> restricted root** — deliberately, because *"a guard that accepts anything stops being
> evidence."* A developer following the superseded text would crash on **eleven of twelve
> months**. The unqualified claim is withdrawn.
>
> This landed on **I-2, the unit's largest blast radius**, and it was found by an
> adversarial pass rather than by the derivation that produced the section — which is worth
> recording, because the section's own three-guard structure was sound and its **routing**
> was not.
>
> ## ⚠ THE DEFECT IS UPSTREAM TOO, AND THIS STAGE DOES NOT SILENTLY NARROW IT
>
> `business-logic-model.md` W-6's approved mechanism reads *"for each artifact:
> `acquisition`'s named accessor"*, with no restricted/ordinary distinction. **That approved
> wording carries the same defect**, and correcting it here would be a downstream stage
> quietly narrowing an approved `functional-design` contract — the move `project.md` records
> as a repeat failure. **Routed to the approval gate as an explicit ruling**, not applied
> upstream: either W-6's wording is amended by change record to carry the two-class routing,
> or this section's correction stands alone as a design-level narrowing the gate record
> notes. **The design below is written either way**; what is at stake is where the
> correction is recorded, not what it says.

**Design, corrected.** The audit reads two classes of artifact and routes them differently,
which is exactly what `scripts/merge_coverage_year.py`'s `guarded()` helper already does:
*"Route a restricted path through the chokepoint; pass an ordinary path through.
`open_restricted` REFUSES ordinary paths by contract, so routing every path through it would
raise rather than protect."*

| Artifact class | Route | Logged? |
|---|---|---|
| **December-bearing** — anything under `evidence/locked_test_restricted/`, which after D-15's relocation of 21 files is where every December-bearing artifact lives | `acquisition`'s named accessor → `open_restricted` | **Yes** — one durable row per artifact, before the read |
| **The other eleven months** — `audit_evidence_2022-01` … `-11`, ordinary paths | Read directly. `open_restricted` **refuses** them by contract | **No access row.** FR-P1-02-3's obligation is scoped to *"any operation that reads a **December 2022 record**"* |

**The chokepoint half is built.** `_append_and_flush` writes the row, stamps `logged_at_utc`
itself, flushes, and `os.fsync`s before `open_restricted` returns the path the caller then
reads; an `OSError` on that write raises `LockedTestError` and **aborts the read**.
`open_restricted` derives the restricted root from its own module location, so a caller
cannot relocate the boundary by passing a different one. **The routing half is not built** —
`acquisition` R-32's named accessors are still absent from `component-methods.md`'s approved
`src/data/locked_test.py` block and are amendment (1) of that unit's three, so this unit
inherits their **proposed** status.

**The class test is by record date, not by path.** A December-bearing artifact is one
containing a December 2022 record (FR-P1-02-6's own definition), and the year-blind
predicate already filed locked-month records under `audit_evidence_2022-01/` in fact —
`evidence/locked_test_restricted/superseded_2026-08-16_from_2022-01/` is where they went.
`assert_no_december_outside_restricted` is the standing regression guard that the class and
the location still agree; **if it ever fails, the routing table above is wrong before the
audit is**, because an unrelocated December artifact would be read as an ordinary path.

**Check 3 — reconcile the rows actually written against the December portion of the declared
scope, per `run_id`.** A mismatch fails. This is narrower than the first issue implied, and
the narrowing is forced by Check 2's correction: **access rows exist only for the
December-bearing class**, so they can only reconcile that class. **The other eleven months
are reconciled against the coverage report's own per-month output** — each declared month
must appear in the report with a count, and a declared month absent from the report fails.
Two reconciliations, over two artifact classes, because there is only one class the access
log can speak for. The reconciler is this unit's and does not exist.

**The two limbs are two typed reads.** The coverage limb binds
`purpose="coverage_audit"`, the regime limb `purpose="regime_audit"`; both carry
`performance_inspected=False`, `locked_test_accessed=True`, and an `authorization`
referencing **Vision §8.3**. `PURPOSES` already validates the literal, and
`AccessRecord.__post_init__` already refuses `locked_test_accessed=False` for a restricted
read. **A read attempted under `purpose="locked_evaluation"` is refused** — that literal is
G-06's.

**Membership is derived from record timestamps, never a directory name or a filename.** Every
coverage and regime count attributes a record by its **observation timestamp**; out-of-month
and out-of-year records are excluded from every per-month statistic. This is a rule and not a
convention because the year-blind predicate already filed locked-month records under
`audit_evidence_2022-01/` in fact.

**Every coverage figure carries `data07_caveat`, sourced from that month's
`provenance_class`.** A figure emitted for a `derived_only` month with **no** caveat field
**fails**. The source field is `acquisition`'s (R-36) and **reaches no other unit today**, so
R-50's seam stands: if the field is absent at implementation, the correct response is a
**stop-and-report under TE §18.3**, never an uncaveated figure.

## SD-I-05 — Attempt identity: what SEC-I-03 left owed, and what the workspace already supplies

SEC-I-03 `[Q2]` named the mechanism for distinguishing audit attempts as **owed**. Part of it
is already on disk and part is not, and the two must not be blurred.

**Supplied.** `AccessRecord.run_id` exists, is required non-empty, and is refused if blank.
`logged_at_utc` is stamped **by the guard**, so an ordering comparison against any later
artifact is a real check rather than a restatement of the caller's intent.

**Owed — the convention, not the field.** Nothing today makes two attempts carry **different**
`run_id` values. `scripts/merge_coverage_year.py` hard-codes `run_id='merge_coverage_year'`
for every row of every run; `tests/test_release_hashes.py` and `test_acquisition_window.py`
account for all 158 rows of `evidence/test_run_access_log.jsonl` under two constant ids. A
second attempt under a constant id is **indistinguishable in the log from the first**.

**Design.** Each audit attempt binds a **distinct** `run_id`, and R-50's reconciliation is
performed **per `run_id`**, not over the whole log. The convention is stated at the level the
requirement needs and no further: the id must be unique per attempt and must join to that
attempt's environment lock (TE §13.1). **The exact id format is 3.5's**, on the same footing
as TS-I-02's deferral of the boundary's expression.

**Why this matters at G-05 rather than only in code.** SEC-I-03 requires an interrupted audit
to produce **no report** and to **re-run from the start**, while its rows **stand
permanently** (NFR-AUD-01). The log will therefore legitimately show **December opened more
times than the audit ran**. Per-`run_id` reconciliation is what makes that legible; without
it, an honest re-run is indistinguishable from an undisclosed extra access — the one reading
that would be worst in front of a supervisor.

## SD-I-06 — The inventory's `licence and access notes` field is a secret-egress surface (NFR-SEC-01)

TE §5.1's nine fields include **licence and access notes**, and W-1 requires all nine or the
entry fails. Provider access notes are where an endpoint, a request pattern, or a credential
hint is most likely to be transcribed — and the source inventory is a **committed** artifact.

**NFR-SEC-01's criterion is a clean secret scan over tree, history, configs, logs and
artifacts** (TA-22). The inventory is in scope for that scan by construction.

**Design.**

1. **Every value the inventory writes routes through `acquisition`'s declared redaction
   serializer** (SEC-A-03 limb 1), which refuses unredacted credential-shaped values with
   `CredentialEgressError`. **That serializer does not exist** — grep across `src/`,
   `scripts/` and `tests/` returns no `CredentialEgressError` and no redaction helper of any
   name. This unit is a **caller** of it, not its owner, and this is a **hard dependency**:
   the inventory cannot be written safely before it exists.
2. **The access-notes field carries the provider's terms and the retrieval interface, never
   a credential, token, signed URL or endpoint carrying one.** Credentials resolve from the
   environment through `foundation`'s resolution, and never reach an inventory entry.
3. **FR-P1-01-6's verbatim acknowledgment notice is a distinct field from access notes.**
   `components.md` assigns the verbatim Kyoto / CEDAR notice to `inventory.py`. Provider
   acknowledgment text is published and must be reproduced **verbatim**; access notes are
   operational. Keeping them separate stops a redaction rule from mangling a notice that
   must not change, and stops a notice field from becoming a place operational detail is
   parked.

**No coverage of NFR-SEC-01 is claimed as discharged.** TA-22 is not this unit's row and the
scan has not run.

## SD-I-07 — Provenance and resolution integrity, as design

SEC-I-04's requirements are unchanged; this section fixes only what a builder would
otherwise have to guess.

**R-44 — nine fields or it fails.** The failure is per **entry** and names the entry and the
missing field, not the file alone. An entry-level raise is what makes a partial inventory
actionable; a file-level one is not.

**R-45 / TS-I-01 — the IGRF version is pinned, and is not pinned here.** An **absent**
version **fails**; it does **not** fall back to a library default. This is the same shape as
R-35's rule that an absent `madrigalWeb_version` fails exactly as `"unknown"` fails: the
distinction that matters is between *no value* and *a value chosen for you*, and both are
refused. **The version stays `TBD — freeze gate`** and the station registry cannot be built
until it is frozen under a D-number.

**R-46 / W-2a — presence is not provenance.** `Station` carries a **per-field provenance**
value and the raise is conditioned on provenance, not only presence. **What provenance is
sufficient is not decided here**: station coordinates are a §18.2 **Student** forbidden
choice and the coordinate-to-cell rule a **Student + Supervisor** one. D-1's own limitation
is still open — coordinates were taken from IGS network pages, **not** the official site-log
PDFs, which rank higher in the §6.2 evidence hierarchy.

**R-47 / W-3 — equality against the NAMED source.** The registry value must equal the value
of the source it **names**, not merely some recorded source value: with three or more
sources, an existence check passes an average (0, 3 and 6 average to 3). The **residual
stands unchanged**: when a mean coincides exactly with the named source's value, **no check
on the value can distinguish it from a legitimate resolution**, and the negative control must
exercise that coincidence case so the limit is pinned rather than discovered.

**R-48 / W-4 — the migration emits a diff and asserts no value changed.** The freeze prevents
an *intentional* change; the diff catches the *accidental* one — a transposed digit in a hand
migration of three coordinate pairs.

**R-49 / W-5 / TS-I-03 — a governed schema, a self-contained report.** The report records
**both** the expected schema's digest and the observed values, so it is interpretable a year
later without reconstructing the config state it ran against. **D-24's 17-item protected set
is not reopened.** *Which* schema form the governed schema takes is **owed at 3.5**, and if it
needs a package, that returns to `nfr-requirements` rather than being settled at 3.5.

**NFR-REP-01 obligation, stated and not claimed as coverage.** The schema digest, the source
hashes, and the integer coverage and regime counts are **exact-equality classes** under
§13.7: they compare for equality, not tolerance, and a mismatch must not be silently
absorbed. NFR-REP-01 is `fixtures-and-reproducibility`'s row; this artifact states the
obligation against it.

## SD-I-08 — The G-P1A record and the four prohibitions, as design

**R-51 — two thresholds, every number attributed.** A verdict per station-month against
**both** D-12 (≥90% usable hourly coverage per station per month, hard gate) and **D-2**
(≥95% of calendar days per month; 100% of December days, 31/31), **plus the measured figure
for each, attributed to the D-number it is judged against.** A bare `PASS` makes ARUC's
100.0% and NICO's 93.2% look identical, and the criterion forbids an unattributed number.
**No soft margin band**: *"near"* would be a new number invented beside a supervisor-frozen
hard threshold.

**D-2's own disclosure travels onto the record** — five of twelve months had already been
audited at 100% day coverage when the threshold was chosen, *"not set blind… stated here so a
reviewer can discount it accordingly."* A record that omits it presents a partly post-hoc
threshold as blind.

**The `data07_caveat` travels onto this record with the figures.** The nine cached
non-December months are pre-TC-06 and classed `derived_only`; **2022-04, 2022-07 and 2022-12**
hold no `raw_isprint_cache/`; the 2026-08-16 corrected extracts were produced under Python
3.14, outside the governed **3.11** pin. `team.md`'s limit stands: **FULL must not be relied
on at a freeze gate while its provenance chain points at superseded per-month hashes.** A
`derived_only` figure reaching this record with no caveat field **fails**.

**R-52 — four separately named results.** Each of the four prohibitions produces its own
named result; a single aggregate pass/fail would let one failure hide inside another's pass.
Two are this unit's (silent imputation, source mixing), one is `features-and-splits`'
frozen-hash ordering artifact, one is `target-standardization`'s mislabel injection. **This
unit's obligation is to assert all four results are present and passing before G-P1A
accepts** — it does not own three of the four tests.

**`FR-P1-02-8` has no acceptance row.** `TA-29` was cited and is **withdrawn** — it is a row
`requirements.md` lists under *"Not applicable in Phase 1 — Phase 2 by definition"*. Naming
four results is a **mechanism, not an acceptance row**; the replacement row is stage 3.2's
and change control's. Recorded because a requirement with a withdrawn row is easier to
misread as covered than one that never had a row.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Row primary owner | Status |
|---|---|---|---|---|
| FR-P1-02-1 | SD-I-03, SD-I-07 | WS-01, TA-04 | **`inventory-and-registry`** (both) | `Pending` |
| **FR-P1-02-7** | SD-I-07 | ⚠ **NO ACCEPTANCE ROW** — WS-01 reaches the registry's existence and the header cross-check only | — | untested |
| FR-P1-02-2 | SD-I-07 | TA-04 | **`inventory-and-registry`** | `Pending` |
| FR-P1-02-3 | SD-I-01, SD-I-04, SD-I-05 | WS-18, TA-25 | `features-and-splits` (WS-18); **this unit** (TA-25) | `Pending` — **authorization limb of BLK-07 open** |
| FR-P1-02-4 | SD-I-08 | TA-25 | **`inventory-and-registry`** | `Pending` |
| FR-P1-02-5 | SD-I-08 | TA-25 | **`inventory-and-registry`** | `Pending` |
| **FR-P1-02-8** | SD-I-08 | ⚠ **NO ACCEPTANCE ROW** — `TA-29` **withdrawn** | — | untested |
| NFR-AUD-01 | SD-I-04, SD-I-05 | TA-10, TA-21 | `foundation` | `Pending` |
| NFR-DQ-01 | SD-I-07 | **TA-19** *(row filled in at this stage — see note below)* | — | `Pending` |
| **NFR-SEC-01** *(added at this stage)* | SD-I-06 | TA-22 | — | `Pending` |

**Derived and printed.** **8** design sections (SD-I-00 … SD-I-08 is nine headings, of which
SD-I-00 is a state record rather than a design section, so **8** carry design). **10**
coverage rows, counted from the table above: the **7** requirements the `functional-design`
map fixes for this unit, plus NFR-AUD-01, NFR-DQ-01 and NFR-SEC-01. **2** rows with no
acceptance row (FR-P1-02-7, FR-P1-02-8), re-derived by counting the blank acceptance cells in
the table above rather than read off the map. **0** rows claimed satisfied. **1** value left
`TBD — freeze gate` by this unit (the IGRF version). **0** new dependencies. **1** change
record owed, carrying **3** edits
(§ SD-I-01 Limb A: two `src/data` cells promoted `—`→`X`, plus a named carve-out withdrawing
the `scripts/*` row's affirmative grant for `01_inventory_and_registry.py`).

**Two cells differ from `nfr-requirements`' table besides the added row, and both are
disclosed rather than left to be noticed** *(added 2026-09-01 on adversarial finding 6,
Minor)*. **NFR-DQ-01's acceptance row reads `TA-19` here and `—` upstream.** The value is
right — `requirements.md:487` gives NFR-DQ-01 the test `TA-19` — but a coverage cell that
changes from empty to populated between two stages is exactly the kind of quiet edit this
project has had to correct before, so it is stated: **the row was filled in from
`requirements.md`, not derived here, and TA-19 is not this unit's row and is not claimed as
discharged.** The second differing cell is the added NFR-SEC-01 row, below.

**Why the count is 10 and not `nfr-requirements`' 9.** One row is added: **NFR-SEC-01**.
`security-requirements.md` cites it in `## Sources` and carries no coverage row for it. This
is a **security design** artifact, and § SD-I-06 identifies a concrete egress surface in this
unit's own output — TE §5.1's *licence and access notes* field on a committed artifact. The
addition is stated rather than silent, and it claims an obligation, not a discharge.

**Why `FR-P1-02-6` is absent.** FR-P1-02-6 is the **residency** rule — locked-test artifacts
live only under the restricted path until G-05 is complete. **This unit does not state that
rule.** W-6 *depends* on restricted-root custody and reaches it through `acquisition`'s named
accessor; depending on a rule is not reproducing its text. The exclusion is also **not this
stage's call**: `functional-design` fixed this unit's set as
`{FR-P1-02-1,-2,-3,-4,-5,-7,-8}` and reconciled it by set difference against
`unit-of-work.md` and the story map, **empty both ways**. Set-differenced again at this stage
against `requirements.md`'s FR-P1-02 space `{1,2,3,4,5,6,7,8}`: the difference is exactly
`{6}`, and nothing else. Its coverage belongs to `governance-guards`, and `requirements.md`
records that it **now passes**, enforced by `tests/test_acquisition_window.py` and by
`assert_no_december_outside_restricted` in `src/data/locked_test.py`.

**Two NFRs are named as obligations and deliberately given no coverage row**: **NFR-PHASE-01**
(§ SD-I-01 — Limb B must not weaken `test_phase_boundary.py`'s existing behaviour) and
**NFR-REP-01** (§ SD-I-07 — the schema digest and the counts are §13.7 exact-equality
classes). Both belong to other units; stating an obligation against a requirement is not
covering it, and the distinction is made here so a later reader does not read either as a
silent omission.

## Assumptions & Open Questions

- **[Q1 / SD-I-01]** The **change record is owed, not written**, and it carries **three** edits — two `src/data` cells promoted `—`→`X`, **plus a named carve-out withdrawing the `scripts/*` row's affirmative `yes` grant for `01_inventory_and_registry.py`**. The third is the larger deviation: promoting an absence records an obligation the matrix did not have, while the carve-out **withdraws a permission the matrix explicitly gives**. Until the record clears, Limb A enforces a rule the approved matrix contradicts in one place and is silent on in two. *(Scope corrected 2026-09-01 on adversarial finding 3, Major; the first issue said "two cells".)*
- **[Q1 / DISC-I-1]** **No approved component row owns the audit's two output artifacts.** `services.md` gives `01_inventory_and_registry.py` the inventory and the registry only; grep across `services.md`, `components.md` and `component-methods.md` returns zero matches for the coverage or regime-count reports. Limb A binds `scripts/01_inventory_and_registry.py` **on the assumption that this is where the audit lives**; if 3.5 places it elsewhere, Limb A's constrained set must move with it.
- **[Q1]** **Unresolved dynamic imports are reported, never assumed clean.** This is the one case where a static walker can be silently wrong, and it is named rather than left to the implementation.
- **[Q2 / SD-I-02]** `InventoryError` and `AuditScopeError` ride R-01's any-future clause. If a second unit later raises either for a different condition, the `PartitionError` discriminator applies and promotion into the enumeration becomes the right move.
- **[Q2 / SD-I-02 — OPEN, routed to the gate]** **A third exception is missing and Q2 named only two.** Set-differencing W-1 … W-6's `RAISES` lines against `config.py`'s 17-name `__all__` yields `{InventoryError, AuditScopeError, SchemaError}`; W-5's **`SchemaError`** was not in the question the owner answered. The same disposition applies on its face, but applying an owner's ruling to an item the owner was not shown is a widening, so it is **raised at the gate for an explicit decision** rather than folded in.
- **[Q3 / SD-I-03]** **The `RegistryError` residual is unresolved by design.** A type-level catch still cannot separate the two registries. `StationRegistryError` remains available as a change record against `functional-design` and is **not** proposed here.
- **[SD-I-05]** The **`run_id` uniqueness convention** is fixed in requirement; its **format** is owed at 3.5. Nothing on disk today makes two attempts distinguishable.
- **[SD-I-06]** **`acquisition`'s redaction serializer does not exist**, and the inventory's nine-field entries depend on it. This is a hard cross-unit dependency, not a preference.
- **[DISC-I-2]** `merge_coverage_year.py`'s `retrieved_at_utc` placeholder migrates into this unit's stage script unless replaced. **A migration obligation, not fixed here.**
- **[DISC-I-3]** `components.md:64` puts two **`acquisition`-owned** requirements — **FR-P1-01-6** and **FR-P1-01-2** — into `inventory.py`, this unit's module. FR-P1-01-2's suffix-mismatch half is **⚠ PROPOSED**, because `acquisition` R-34 holds the release-manifest carriage of `suffix_mismatch` **Open for stage 3.2**. Neither appears in this unit's coverage table, correctly; the seam is the module, not the requirement.
- **[SD-I-04 — OPEN, routed to the gate]** **W-6's approved mechanism carries the same defect this section corrects.** Its text reads *"for each artifact: `acquisition`'s named accessor"*, with no restricted/ordinary distinction, and eleven of the twelve declared months are ordinary paths `open_restricted` refuses. **The correction is stated here and NOT applied upstream**; the ruling owed at the gate is whether W-6's wording is amended by change record or whether this stage's narrowing stands recorded in the gate record alone.
- **[SD-I-04 — the routing correction's own dependency]** The two-class routing table rests on **`assert_no_december_outside_restricted` continuing to pass**: it is what keeps "December-bearing" and "under the restricted root" the same set after D-15's relocation of 21 files. **If that guard ever fails, the routing table is wrong before the audit is**, because an unrelocated December artifact would be read as an ordinary path and never logged.
- **[TS-I-01]** The **IGRF version stays `TBD — freeze gate`.** The station registry cannot be built until it is frozen under a D-number.
- **Carried — D-1's site-log validation limitation** is open; W-2a and SD-I-07 both turn on it and neither closes it.
- **Carried — BLK-07's authorization limb is open.** No run may touch calendar 2022-12 while it stands.
- **Carried — `RES-01`**: permitted-read access logging is NOT TESTED, owned by stage 3.2, and this unit performs the permitted read it is about.
- **Carried — the `data07_caveat`** travels with every coverage figure; nothing here discharges it, and `provenance_class` reaches no other unit today.
- **Carried — Kaggle's durability semantics are unmeasured**, and Check 2's before-the-read guarantee depends on them.
- **Carried — FR-P1-02-8's replacement acceptance row** after `TA-29`'s withdrawal.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, authorises writing a module, or claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T20:13:12Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | **Critical** | `security-design.md` § SD-I-04 Check 2 (and `logical-components.md` I-2 guard 2) | **Check 2 as written is not implementable for eleven of the twelve months.** It states *"every read logged, durably, before it happens — routed through `acquisition`'s named accessor, which delegates to `open_restricted`"*, over the twelve-month scope Check 1 declares. But `evidence/` holds `audit_evidence_2022-01` … `2022-11` **outside** `evidence/locked_test_restricted/` (only `2022-12` and `2022-FULL` are inside), and `src/data/locked_test.py:173-179` raises `LockedTestError` for any path not `is_relative_to` the restricted root — the same refusal this section quotes approvingly two sentences later. `AccessRecord.__post_init__:104` additionally requires `locked_test_accessed=True`. A developer following the text crashes on 11/12 months; the only alternative — log December only — leaves **Check 3's reconciliation "rows written against the declared scope"** with no row source for eleven of the twelve months it reconciles. Neither branch is resolvable from the document, and this lands on I-2, the unit's largest blast radius. | State explicitly which reads produce access rows through `open_restricted` (December/restricted only) and what logs the unrestricted eleven, then restate Check 3's reconciliation **domain** to match. `functional-design` W-6's *"for each artifact: acquisition's named accessor"* inherits the same defect and should be raised at the gate rather than silently narrowed here. |
| 2 | Major | `security-design.md` § SD-I-01, third implementation constraint | **"`_imported_modules` today swallows a parse error" is false.** `tests/test_phase_boundary.py:112-115` reads `except SyntaxError as exc:  # a file that will not parse cannot be cleared` → `pytest.fail(...)`. Verified as the only `_imported_modules` and the only `ast.parse` in `src/`, `scripts/` and `tests/`. The constraint itself is correct; its stated justification is a present-day defect that does not exist — in an artifact whose § SD-I-00 method is precisely to correct stale claims before relying on them. | Restate as *"the primitive already fails on an unparseable file (`pytest.fail`); the closure must preserve that behaviour rather than reintroduce a skip."* Drop the `governance-guards` R-27 framing as a fix for a defect here. |
| 3 | Major | `security-design.md` § SD-I-01 Limb A + § Requirement coverage ("**1** change record owed … Limb A's two matrix cells"); repeated in `logical-components.md` § Assumptions | **The change record is under-scoped.** Limb A binds `scripts/01_inventory_and_registry.py`, and the artifact's own point 2 states that `component-dependency.md`'s `scripts/*` (all others) row grants that script `models: yes`, `evaluation: yes` — verified at `component-dependency.md:33`. Forbidding those edges contradicts an **affirmative grant**, a strictly larger deviation than the `—`→`X` promotion on the `src/data` row (`:25`) that the owed change record does cover. By the artifact's own reasoning (an absent edge owes no test, a granted edge is a positive permission), that change needs recording too — as two further cells or a carved-out row. Both artifacts repeat the two-cell scope. | Widen the owed change record to cover the `scripts/*` row's treatment of `01_inventory_and_registry.py`, or state why narrowing a permission needs no record while promoting an absence does. |
| 4 | Major | `logical-components.md` § I-2 guard table row 2 vs § Shared resources row 3; `security-design.md` § SD-I-04 Check 2 ("**This is built.**") | **Internal contradiction on the one guard claimed complete.** The guard is defined as *"a durable access row before each read, **through `acquisition`'s named accessor**"* and marked **Built? Yes**; § Shared resources says that same accessor layer *"is still absent from `component-methods.md`'s approved block and is amendment (1) of `acquisition`'s three — this unit inherits that proposed status."* The **chokepoint** is built (verified: `open_restricted:147`, `_append_and_flush:116`, `os.fsync:143`, guard-stamped `logged_at_utc:138`); the **routing layer the guard is defined over** is proposed. An implementer reading either point of use concludes no work is owed. | Split the guard row into *chokepoint (built)* and *accessor routing (proposed, `acquisition`'s amendment 1)*, and qualify "This is built" at its point of use in § SD-I-04. |
| 5 | Minor | `security-design.md` § SD-I-06, § SD-I-07 (R-44), § Requirement coverage | **W-1's requirement anchor is unregistered.** `business-logic-model.md`'s requirement-to-workflow map covers W-2…W-8 only — **no FR-P1-02 requirement maps to W-1**. `components.md:64` maps `inventory.py` to **FR-P1-01-6**, whose acceptance row is **TA-08** and whose family is `acquisition`'s. SD-I-06 and R-44 design against W-1's nine fields, yet the completeness argument is bounded to the FR-P1-02 space (*"the difference is exactly `{6}`"*), so a builder cannot tell which acceptance row a nine-field failure is judged against, or that it belongs to another unit's family. This is the same class of seam as DISC-I-1, which **is** registered. | Register the W-1 / FR-P1-01-6 / TA-08 seam alongside DISC-I-1, and state that the FR-P1-02 set difference bounds completeness over that space only. |
| 6 | Minor | § Requirement coverage, NFR-DQ-01 row | **A second, unflagged table change.** `../nfr-requirements/security-requirements.md:201` carries NFR-DQ-01 with acceptance row `—`; this stage's tables give it `TA-19`. The value is **correct** (`requirements.md:487`), so nothing downstream breaks — but the artifact flags its NFR-SEC-01 addition explicitly and in a dedicated paragraph, and says nothing about this one. Upstream's own "2 requirements with no acceptance row" line is what the correction quietly repairs. | Add one sentence naming the NFR-DQ-01 correction beside the NFR-SEC-01 paragraph. |
| 7 | Minor | § DISC-I-2 | Line citation off by one: `merge_coverage_year.py:88` is `run_id='merge_coverage_year'`; the `retrieved_at_utc='recorded-at-call-time-by-the-runner'` placeholder is at **:89** (the `AccessRecord(` call opens at :87). Substance verified and correct. | Cite `:87-95` or `:89`. |

**Suggestion (not a finding).** § SD-I-01's *"Why both"* rests Limb A's non-redundancy on a **documentary** argument (the matrix would record no obligation). The stronger detection argument goes unstated: Limb B closes from the audit **entry point**, so it never visits a `src/data/*` module unreachable from that entry point, while Limb A checks every member of the set regardless of reachability. That is the fact that makes "neither is a superset of the other" true in the detection sense, and it is worth stating.

### Checks performed

| # | Check | Method | Result |
|---|---|---|---|
| 1 | `produces_kinds` yields exactly two artifacts for a `library` unit | Read stage frontmatter `:20-24` | **Confirmed.** `performance-design: [service, ui]`, `scalability-design: [service]`, `reliability-design: [service]`, `logical-components: [service, ui, library]`; `security-design` carries **no** `produces_kinds` entry and so applies to all kinds. Two artifacts is right, and the absent three are absent by design |
| 2 | Q1 claim (a): `src/data` row marks `models`/`evaluation` `—` not `X` | `component-dependency.md:25` | **Confirmed.** `\| \`src/data\` \| — \| **X** \| **X** \| — \| — \| — \| — \|` |
| 3 | Q1 claim (b): `scripts/*` (all others) grants `yes`/`yes`; `01_…` sits in it | `component-dependency.md:33`; only `04_build_external_products.py` and `notebooks/00_…` are broken out | **Confirmed** — and it is the basis of finding #3 |
| 4 | The `X` vs `—` quotation | `component-dependency.md:20-21` | **Confirmed verbatim** |
| 5 | Q1 claim (c): direct imports only; no transitive closure anywhere | `grep -rn "_imported_modules\|ast.parse\|transitive\|closure"` over `src/`, `scripts/`, `tests/` | **Half confirmed.** One `_imported_modules`, direct-only, no closure anywhere ✓. **"Swallows a parse error" refuted** → finding #2 |
| 6 | Limb A's stated blind spot (a chain leaving the constrained set) | Matrix rows for `src/external.spaceweather` (`models: —`, `evaluation: —`) | **Sound.** The `audit → external.spaceweather → evaluation` chain is permitted by the matrix and invisible to a set-local direct check |
| 7 | `config.py`'s `__all__` holds 17 names; `SchemaError` absent | `src/data/config.py:42-60`, enumerated | **Confirmed.** 17 names; no `SchemaError` |
| 8 | Set difference of W-1…W-6 `RAISES` against `__all__` | `RAISES` at `business-logic-model.md:108,175,323,351` → {InventoryError, RegistryError, SchemaError, LockedTestError, AuditScopeError}; minus `__all__` | **Confirmed exactly `{InventoryError, AuditScopeError, SchemaError}`** — three, not two |
| 9 | Q2 put only two exceptions to the owner | `nfr-design-questions.md:101,118,124` | **Confirmed.** `SchemaError` appears nowhere in Q2. Routing it to the gate is **correct, not ceremony** |
| 10 | `RegistryError` collision | `config.py:119-120` docstring quoted **verbatim**; `business-logic-model.md:175` declares `RAISES RegistryError` | **Confirmed.** The residual is stated plainly, not waved away; deferring `StationRegistryError` names the route and preserves it |
| 11 | Printed counts — 8 design sections | `## SD-I-00 … SD-I-08` = 9 headings, minus the state record | **Confirmed: 8** |
| 12 | Printed counts — 10 coverage rows in each artifact, identical membership | Enumerated both tables and set-differenced **in both directions** | **Confirmed.** Both = {FR-P1-02-1,-7,-2,-3,-4,-5,-8, NFR-AUD-01, NFR-DQ-01, NFR-SEC-01}; **empty both ways** |
| 13 | 2 rows with no acceptance row; 7 FRs from the map | Blank acceptance cells = FR-P1-02-7, -8; `business-logic-model.md:598-605` states 7 | **Confirmed both** |
| 14 | `{6}` set difference against `requirements.md`'s FR-P1-02 space | `grep -o "FR-P1-02-[0-9]+"`, unique = {1..8} exactly, no -9+ | **Confirmed: `{6}` and nothing else** |
| 15 | 7 / 1 / 2 decomposition across I-1/I-2/I-3 | Re-derived from `logical-components.md:271-275` against the component contents table | **Confirmed.** 7 singly-assigned + SD-I-02 shared = 8, matching the section count; every coverage row's component is consistent with its section mapping in `security-design.md` |
| 16 | `open_restricted` / `AccessRecord` / `PURPOSES` / `performance_inspected` exist as described | `locked_test.py:68-74,81-107,116-144,147,170-186` | **Confirmed exactly**, including line 147, `__file__`-derived root, `logged_at_utc` guard-stamped before `os.fsync`, and `OSError` → `LockedTestError` aborting the read |
| 17 | `configs/` and the four named files do not exist | `ls` of `configs`, `src/data`, `scripts`, `tests` | **Confirmed.** No `configs/`; no `inventory.py`, `registry.py`, `01_inventory_and_registry.py`, `test_station_registry.py` |
| 18 | `tests/` holds six modules; `src/` holds six §12 packages | Directory listing | **Confirmed** (6 test modules; `data, evaluation, external, features, gnss, models`), so W-9's *"three modules"* is stale exactly as § SD-I-00 says |
| 19 | Access-log claims | `evidence/` listing; `wc -l`; `grep -o` on purpose and run_id | **Confirmed.** No `merge_run_access_log.jsonl`; `test_run_access_log.jsonl` = **158** rows, **158/158** `coverage_audit`, run_ids `test_release_hashes` (150) + `test_acquisition_window` (8) = 158 — the constant-id problem SD-I-05 describes is real |
| 20 | DISC-I-1's five spellings return zero matches in three files | `grep -inE "coverage report\|coverage_report\|regime count\|regime-count\|regime_count"` in `services.md`, `components.md`, `component-methods.md` | **Confirmed: zero in all three.** `services.md:47`'s outputs cell is quoted verbatim |
| 21 | DISC-I-2's placeholder | `merge_coverage_year.py:87-89` | **Confirmed in substance** (line cite off by one → finding #7); `locked_test.py:116-135`'s docstring records the 2026-08-28 discovery and names `logged_at_utc` as the fix, as claimed |
| 22 | No `CredentialEgressError`, no redaction helper | `grep -rniE "credentialegress\|redact\|sanitiz"` over `src/`, `scripts/`, `tests/` | **Confirmed absent.** SD-I-06's hard dependency is real |
| 23 | No IGRF version named; no scientific value decided | `grep -nEi "IGRF-?1[0-9]\|IGRF[0-9]\|igrf"` over both artifacts | **Confirmed.** Every occurrence is `TBD — freeze gate` or a citation. No gate, acceptance row or test claimed passing; BLK-07's authorization limb stated open in both; nothing authorises a module write |
| 24 | `TA-29`'s withdrawal is well-founded | `requirements.md:602-603` lists TA-29 under *"Phase 2 by definition"*; the FR-P1-02-8 row itself records the withdrawal | **Confirmed.** Acceptance rows WS-01/TA-04/TA-25/WS-18 all match `requirements.md:346-352` |
| 25 | The NFR-SEC-01 addition (adversarial item 8) | `security-requirements.md:189-209` (9 rows, no NFR-SEC-01) and **its own line 299**, which records NFR-SEC-01 as *"this unit's genuine scope"* | **Legitimate, not widening.** It is cited upstream, upstream's own review classes it in scope, § SD-I-06 identifies a concrete egress surface in **this unit's** committed output, and the row claims an obligation rather than a discharge. This artifact is the security design; carrying the row is scope-correct |
| 26 | Cross-artifact consistency | Component ↔ section ↔ requirement mapping; shared-resources table against SD-I-02/03/06; "obligations, not coverage" for NFR-PHASE-01 and NFR-REP-01 | **Consistent throughout except finding #4.** NFR-PHASE-01 and NFR-REP-01 are held as obligations with no coverage row in both files, and `test_phase_boundary.py:63`'s `PHASE1_PERMITTED_PACKAGES` does permit `models`/`evaluation` and forbid `gnss` as § SD-I-01 states |

### Validation tool results

No stage-specific validator exists for `nfr-design`; the four declared sensors were exercised by proxy.

| Sensor | Method | Result | Interpretation |
|---|---|---|---|
| `required-sections` | `grep -c "^## "` | 13 H2 (`security-design.md`), 7 H2 (`logical-components.md`) | **PASS** — registry default is ≥2 |
| `upstream-coverage` | grep for each of the six `consumes` artefact names in both files | All six present in both (the three absent-by-design categories are named in § Sources / § Scope note) | **PASS** |
| `linter` / `type-check` | `**/*.{ts,js,tsx}` snippets | None — the only fenced block is Mermaid, in the upstream `business-logic-model.md`, not here | **N/A** |

### Coverage limits — what I did not check, and why

- **Sibling units' Construction records were not opened** (read-scope bound). Every cross-unit claim is therefore this unit's own characterization, unverified: `foundation`'s *failure-consequence* criterion and `governance-guards`' *enforcement-timing* criterion and their R-23 two-limb precedent; R-01's any-future clause and the 2026-08-28 `PartitionError` declaration-site ruling; R-25, R-27, R-32, R-33, R-36, R-50, R-109; `acquisition`'s SEC-A-03 limb 1 and its "three amendments"; `features-and-splits`' frozen-hash ordering artifact and `target-standardization`'s mislabel injection. Finding #4 turns on one of these (the accessor's proposed status) **as this unit states it** — I verified the contradiction between the artifact's own two statements, not the upstream fact.
- **`evidence/DECISIONS.md` was not read.** D-1, D-2, D-11, D-12, D-15, D-24, D-28, D-31 and the G-09 signature are taken as stated; D-2's ≥95%/100%-of-December rule and D-12's ≥90% were cross-checked only against `requirements.md:349-350`, where they match. The BLK-07 register entry itself was not opened.
- **No test was executed.** `pytest` was not run; `_imported_modules`' behaviour was established by reading the source, not by running it.
- **The 2026-08-28 `GOV-2026-08-28-FD-01` recommendations** cited by `business-logic-model.md` W-6 were not opened.
- **Prose quality, `nfr-requirements`' own correctness, and the upstream `security-requirements.md` count of "2 rows with no acceptance row"** (which its own table shows as three blank cells, including NFR-DQ-01) are out of this stage's scope; finding #6 records only what **this** stage changed.

### Summary

The workspace-evidence discipline in this pair is unusually strong: **25 of the 26 checks above reproduced the artifacts' claims exactly**, including every printed count, both coverage tables' membership (empty set difference in both directions), the `{InventoryError, AuditScopeError, SchemaError}` derivation, DISC-I-1's zero-match grep across three approved artifacts, and the whole `open_restricted` mechanism down to the line number. Routing `SchemaError` to the gate rather than folding it into Q2 is right, and the NFR-SEC-01 addition is scope-correct rather than a downstream widening.

The blocking concern is that § SD-I-04's Check 2 and Check 3 cannot both be built as written: eleven of the twelve months the audit declares live outside `evidence/locked_test_restricted/`, and the very chokepoint the section leans on refuses exactly those paths — a contradiction the section contains within one paragraph, on the unit's only silent-failure component. Two further Majors are of the same family the artifacts elsewhere police well: one factual claim about existing code that the code refutes, and one owed change record scoped to the smaller of the two matrix deviations Limb A actually creates. **NOT-READY** on 1 Critical and 3 Major.

---

## Remediation of the iteration-1 findings — 2026-09-01

All seven findings addressed. Each repair was swept for **every representation** of the
corrected fact across both artifacts, not only the site the finding named.

| # | Sev | Repair | Sites changed |
|---|---|---|---|
| 1 | **Critical** | § SD-I-04 Check 2 rewritten with a **two-class routing table**: December-bearing artifacts (under `evidence/locked_test_restricted/` after D-15's relocation) route through `open_restricted` and produce one durable row each; the other eleven months are ordinary paths, read directly, refused by the chokepoint by contract, and produce **no** access row — which is what FR-P1-02-3's own scope (*"any operation that reads a December 2022 record"*) actually requires. **Check 3 split into two reconciliations** over the two classes, because only one class has an access log to speak for it. The class test is by **record date**, with `assert_no_december_outside_restricted` named as the standing guard that class and location still agree. **W-6's approved wording carries the same defect and is NOT silently narrowed** — routed to the gate as an explicit ruling. | `security-design.md` § SD-I-04 (correction box + routing table + Check 3), § Scope note Performance and Observability rows, § Assumptions (2 new bullets); `logical-components.md` § I-2 correction box, guard-table rows 2 and 3, § Failure domains row I-2, § The asymmetry paragraph, § Assumptions (3 new bullets) |
| 2 | Major | The claim *"`_imported_modules` today swallows a parse error"* is **false and withdrawn**. `tests/test_phase_boundary.py:112-115` `pytest.fail`s on `SyntaxError`, and it is the only `ast.parse` in `src/`, `scripts/` or `tests/`. The constraint is restated as **preservation, not repair**, with the live risk named: a graph walk visits far more files, and a blanket `except` is the natural way to keep it running. | `security-design.md` § SD-I-01 constraint 1 |
| 3 | Major | The owed change record is **three edits, not two**, and the third is named first because it is the larger deviation: two `src/data` cells promoted `—`→`X`, **plus a carve-out withdrawing the `scripts/*` row's affirmative `yes` grant** for `01_inventory_and_registry.py`. Promoting an absence records an obligation the matrix lacked; the carve-out **withdraws a permission the matrix gives**. | `security-design.md` § SD-I-01 (new table), § Requirement coverage derived line, § Assumptions; `logical-components.md` § Assumptions |
| 4 | Major | The logged-read guard is **Half**, not Built: the **chokepoint** is built, the **R-32 accessor routing layer** is proposed (`acquisition`'s amendment 1). The guard table and § Shared resources no longer contradict each other, and the dependent counts were **recounted, not adjusted**: I-2's guards are now **three unbuilt + one half-built** (was "two unbuilt, one half-built"), and its containment rests on **four** things that do not exist (was three). | `logical-components.md` guard-table row 2, § Failure domains, § The asymmetry paragraph; `security-design.md` § SD-I-04 ("the chokepoint half is built / the routing half is not") |
| 5 | Minor | **DISC-I-3 registered**: `components.md:64` puts `FR-P1-01-6` and `FR-P1-01-2` — **`acquisition`-owned** requirements — into `inventory.py`, this unit's module, and FR-P1-01-2's suffix-mismatch half is **⚠ PROPOSED** under `acquisition` R-34, Open for 3.2. Neither belongs in this unit's coverage table; the seam is the module. The finding's `TA-08` attribution is **not** carried forward: `components.md:169`'s TA-08/TA-12 reference is the grep for absent SSN, residual and GRU modules, unrelated to `inventory.py`. | `security-design.md` § SD-I-00 (new DISC-I-3 + lead-in recount two→three), § Assumptions; `logical-components.md` § Assumptions |
| 6 | Minor | NFR-DQ-01's acceptance row change from `—` to **TA-19** is now **disclosed at both tables**, with the value's source cited (`requirements.md:487`) and an explicit statement that TA-19 is not this unit's row and is not claimed as discharged. | `security-design.md` coverage table + new disclosure paragraph; `logical-components.md` coverage table |
| 7 | Minor | Line citation corrected: `merge_coverage_year.py:87-95` builds the `AccessRecord`, **`:89`** sets the placeholder. | `security-design.md` § DISC-I-2 |

**Two findings were accepted in substance but not in full.** Finding 3's recommendation
offered *"or state why narrowing a permission needs no record"* — that alternative is
declined, because narrowing a permission is the larger deviation and the record is the right
place for it. Finding 5's `TA-08` attribution is corrected rather than adopted, for the
reason given in the table.

**No count was adjusted to fit.** Every figure touched above was **re-derived from the
corrected artifact** and printed with its old value beside it.

---

## Review — 2026-09-01 iteration 2 (terminal)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T20:23:10Z
**Iteration:** 2 of 2 — **terminal pass.** No further reviewer iteration remains; the two
Major findings below are **not blockers under the verdict rule** and go to the human as
matters to weigh at the approval gate.

### Status of the seven iteration-1 findings

Each was re-verified against the files on disk, not against the remediation table.

| # | Sev (it. 1) | Closed? | Evidence |
|---|---|---|---|
| 1 | **Critical** | **Closed in substance** — but the repair raises findings 8 and 9 below | Two-class routing is buildable; the FR-P1-02-3 scoping quotation is verbatim-correct (see check 1); `evidence/` layout re-listed and matches the artifact's description exactly, including *"two `superseded_*` directories and two loose artifacts"*; the `guarded()` quotation is verbatim (`merge_coverage_year.py:99-102`) |
| 2 | Major | **Closed** | `tests/test_phase_boundary.py:112-115` is `try: ast.parse(...)` / `except SyntaxError as exc:` / `pytest.fail(...)`. The false claim is withdrawn and the constraint restated as preservation. The `:112-115` citation is exact, and `ast.parse` occurs **once** in `src/`+`scripts/`+`tests/` (the only other hit is a `__pycache__` binary) |
| 3 | Major | **Closed** | `component-dependency.md:25` `src/data` row = `models: —`, `evaluation: —`; `:33` `scripts/*` (all others) = `models: yes`, `evaluation: yes`. Edit 3 **is** a withdrawal of an affirmative grant, correctly characterized and correctly named as the larger deviation. Three edits is internally consistent (one carve-out row, not two cells) and printed identically in `security-design.md` § SD-I-01, § Requirement coverage and § Assumptions, and in `logical-components.md` § Assumptions |
| 4 | Major | **Closed** | Guard-table row 2 now reads **Half**; § Shared resources row 3 no longer contradicts it. **Recounts re-derived from the corrected table, not accepted:** Built? column = No / Half / No / No ⇒ **three unbuilt + one half-built** ✓; § Failure domains I-2 row and § The asymmetry paragraph both carry the recount ✓; "four things that do not exist" enumerates four named items, one per guard ✓ (but see finding 10) |
| 5 | Minor | **Closed** | `components.md:64` is the `inventory.py` row carrying `FR-P1-01-6, FR-P1-01-2` — exact line, exact IDs. `components.md:169` is *"…design**, and TA-08/TA-12 grep for their absence."* inside the `src/models` **Boundary** paragraph about absent SSN/residual/GRU modules — **the builder's refusal to carry my TA-08 attribution forward is correct and my iteration-1 finding was wrong on that limb** |
| 6 | Minor | **Closed at both tables** | `security-requirements.md:201` carries NFR-DQ-01 with `—`; `requirements.md:487` gives it `TA-19`. `security-design.md` has the dedicated disclosure paragraph; `logical-components.md` carries the disclosure **inline in the NFR-DQ-01 row itself** |
| 7 | Minor | **Closed** | `merge_coverage_year.py:87` opens `return AccessRecord(`, **`:89`** is `retrieved_at_utc='recorded-at-call-time-by-the-runner'` |

### Findings — iteration 2

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 8 | Major | `security-design.md` § SD-I-04 Check 3; § Scope note Observability row; `logical-components.md` § I-2 guard table row 3 | **The split reconciliation leaves December without the report-presence check it just gave the other eleven months.** Limb 1 reconciles *"the rows actually written against the **December portion of the declared scope**, per `run_id`"* — rows against **scope**, never against the report. Limb 2 is scoped to *"the other eleven months … each declared month must appear in the report with a count."* December is therefore in neither: a December read that logs correctly but whose count is **dropped from the coverage report** passes limb 1 (rows match the declared scope) and is out of limb 2's domain. That is exactly I-2's stated failure mode — *"a silently skipped month produces a wrong figure that looks right"* — on the one month it matters most, and it defeats FR-P1-02-3's own acceptance criterion, which reads verbatim *"The coverage report covers all twelve months"* (`requirements.md:349`). The gap did not exist in the first issue (Check 3 then spanned all twelve); it was **introduced by the repair**, and it is represented consistently in all three sites, so it is a design gap rather than a contradiction. | Restate limb 2's domain as **all twelve declared months** (report-presence is orthogonal to how the read was routed), leaving limb 1 as the December-only access-row reconciliation. One sentence in each of the three sites. |
| 9 | Major | `security-design.md` § SD-I-04 (routing table class cell + *"The class test is by record date, not by path"* + the Assumptions bullet naming the guard); `logical-components.md` § Assumptions `[I-2 — the routing correction's own dependency]` | **The routing correction's load-bearing guard cannot see 37 of the 61 files it is claimed to police.** The design carries two definitions of "December-bearing": the routing **table** says *"anything under `evidence/locked_test_restricted/`"* (a **path** test), while the prose two paragraphs later says *"A December-bearing artifact is one containing a December 2022 record"* (a **record-date** test), with `assert_no_december_outside_restricted` named as what keeps the two the same set — *"if it ever fails, the routing table above is wrong before the audit is."* **That guard scans `*.json` only**: `src/data/locked_test.py:213` is `for candidate in sorted(root.rglob("*.json"))`, while its own docstring claims it *"walks `evidence/` recursively and returns every December-bearing artifact."* Outside the restricted root `evidence/` holds **33 `.csv`, 23 `.json`, 1 `.jsonl`, 4 `.md`** (derived by `find … ! -path "*locked_test_restricted*"`), and the coverage artifacts are predominantly CSV. A December-bearing CSV filed under `audit_evidence_2022-01/` — **the exact historical failure TEC-09 records** — would be classed ordinary by the table, read **unlogged**, and reported clean by the guard. This is a residual unlogged-December-read path in a design whose whole purpose is to close them, and the artifact asserts the guard's assurance without stating its scan bound. Also brushes `project.md` § Forbidden (*"NEVER derive fold or partition membership from an acquisition directory name"*), which the table's path test does and the prose test does not. | Make the routing table's class cell state the **record-date** test as the operative one, with the restricted root as its post-D-15 location rather than its definition; and state the guard's `*.json` scan bound where the guard is relied on, as an obligation on `governance-guards` (or on this unit's own pre-read classification) rather than as assurance already in hand. |
| 10 | Minor | `logical-components.md` § The asymmetry paragraph | **The "four things that do not exist" enumeration under-describes guard 3, in the same shape iteration-1 finding 3 was raised for.** The guard table's own Built? cell for row 3 reads *"`run_id` exists as a required field, but the **uniqueness convention** does not, and **neither reconciler exists**"* — three absent items. The asymmetry list carries only *"the `run_id` uniqueness convention"* and drops both reconcilers, which are the parts that actually do the containing. The count of **four** is defensible (one item per guard) and is not disputed; the enumeration beneath it is not the table's. | Add *"and neither reconciler"* to the third item, or re-derive the list per-item rather than per-guard and reprint the count. |
| 11 | Minor | `security-design.md` § SD-I-04, second correction box; `logical-components.md` § Assumptions `[I-2 — OPEN, routed to the gate]` | **The upstream-narrowing route is the correct call and is verified — but option 2 leaves a live contradiction the gate should be told is live.** W-6's wording is confirmed verbatim: `business-logic-model.md:379` (Mermaid node `A["for each artifact:<br/>acquisition's named accessor"]`) and `:396` (text fallback *"opens each artifact through `acquisition`'s named accessor"*), with no restricted/ordinary distinction. Routing rather than narrowing matches `project.md` § Corrections (*"NEVER edit a human-signed record … route ONE explicit ruling"*) exactly and is **not** an evasion. The residual: if the gate picks *"the narrowing stands in the gate record alone,"* an implementer at 3.5 reading only the approved `business-logic-model.md` still gets the unbuildable instruction — the artifact says the design *"is written either way,"* which is true of this artifact and not of W-6. | State, in the same box, that option 2 leaves W-6's text unbuildable-as-read for a builder who does not also read this stage, so the human chooses between two known costs rather than one. |

**Suggestion (not a finding), carried unaddressed from iteration 1.** § SD-I-01's *"Why both"*
still rests Limb A's non-redundancy on the **documentary** argument alone. The detection
argument — Limb B closes from an entry point and never visits a `src/data/*` module
unreachable from it, while Limb A checks every member regardless of reachability — is what
makes *"neither is a superset of the other"* true in the detection sense. Not re-raised as a
finding.

### Checks actually run this pass, with results

Every claim below was re-derived from the files on disk this iteration; nothing was carried
from iteration 1.

| # | Check | Method | Result |
|---|---|---|---|
| 1 | **FR-P1-02-3's scoping claim is supported by `requirements.md`** | `requirements.md:349`, read in full | **Confirmed verbatim.** *"An access-log row with `locked_test_accessed = true` is written BEFORE any operation that reads a **December 2022 record**"*; the *"scope is access, unqualified"* clause qualifies the **kind of operation** (merges, re-derivations, recounts, schema validations), **not the month**. The two-class routing is correctly grounded, and the artifact's quotation is exact |
| 2 | Workspace layout the routing table rests on | `ls evidence/`, `ls evidence/locked_test_restricted/` | **Confirmed exactly.** Eleven ordinary `audit_evidence_2022-01…-11`; restricted holds `2022-12`, `2022-FULL`, **two** `superseded_*` dirs and **two** loose artifacts (`bbox_…hdf5.txt`, `loose_artifacts_sha256_manifest.json`) |
| 3 | `open_restricted` refuses ordinary paths; log-write failure aborts the read | `locked_test.py:147,173-186`; `AccessRecord.__post_init__:104` | **Confirmed.** `is_relative_to` check at `:173`; `OSError` → `LockedTestError` aborting the read; `__file__`-derived root; `logged_at_utc` stamped at `:138` before `os.fsync` at `:143` |
| 4 | The `guarded()` quotation | `merge_coverage_year.py:98-108` | **Confirmed verbatim**, including *"open_restricted REFUSES ordinary paths by contract"* |
| 5 | **The class test by record date, given `superseded_2026-08-16_from_2022-01/`** | Directory listing + `locked_test.py:193-222` | **Half confirmed.** The superseded directory **is** inside the restricted root, so that specific historical case is contained ✓. **The guard that keeps class and location aligned scans `*.json` only** (`:213`) against 33 CSV / 4 MD non-JSON files outside the root → **finding 9** |
| 6 | **Any remaining unlogged December-read path / any ordinary-path crash** | Traced both classes through the routing table | **Ordinary-path crash: none** — direct reads never touch the chokepoint ✓. **Unlogged path: one residual**, per finding 9 |
| 7 | **Does the split reconciliation cover twelve months without a gap?** | Read Check 3 and both mirror sites | **No — one gap.** December is outside limb 2's stated domain → **finding 8** |
| 8 | W-6's wording, and whether routing beats narrowing | `business-logic-model.md:379, 396, 459-469` | **Confirmed verbatim; routing is the correct call.** W-6 itself already flags the R-32 routing as ⚠ PROPOSED at `:464`, so this unit's inherited-status claim is upstream-supported. Residual → finding 11 |
| 9 | Repair 2 — the `_imported_modules` parse-error claim | `tests/test_phase_boundary.py:110-123`; `grep -rn "ast.parse\|_imported_modules"` over `src/`, `scripts/`, `tests/` | **Confirmed accurate.** `pytest.fail` on `SyntaxError`; one `ast.parse` in the tree |
| 10 | Repair 3 — three-edit scope and edit 3's characterization | `component-dependency.md:19-21, 25, 33` | **Confirmed.** `X` vs `—` quotation verbatim; `src/data` = `—`/`—`; `scripts/*` (all others) = `yes`/`yes`; `01_inventory_and_registry.py` falls in that row (only `04_build_external_products.py` and `notebooks/00_…` are broken out) |
| 11 | Repair 4 — four-way agreement of guard table / § Shared resources / § Failure domains / asymmetry paragraph, **and** with § SD-I-04 | Read all five sites; recounted the Built? column | **Agree.** 3 No + 1 Half; § SD-I-04's *"the chokepoint half is built / the routing half is not"* matches guard row 2 exactly. One under-description → finding 10 |
| 12 | Minor 5 — `components.md:64` and `:169` | Exact-line reads | **Both exact.** `:64` = `inventory.py` / `FR-P1-01-6, FR-P1-01-2`; `:169` = the SSN/residual/GRU absence grep |
| 13 | Minor 6 — TA-19 disclosed at BOTH tables | `security-requirements.md:201` (`—`); `requirements.md:487` (`TA-19`); both coverage tables | **Confirmed at both**, one as a paragraph, one inline in the row |
| 14 | Minor 7 — the `:89` citation | `merge_coverage_year.py:85-96` | **Confirmed** |
| 15 | **Fresh-defect sweep — "every read" / "each artifact" / "each read"** | `grep -in "every read\|each read\|each artifact\|every artifact\|all twelve\|twelve month"` over both files | **Clean.** Every survivor is either qualified *"of a **December-bearing** artifact"* (Scope note Performance row `:55`; Check 2 heading `:302`; guard row 2) or an explicit quotation of the withdrawn text inside a correction box. No unqualified chokepoint claim survives |
| 16 | **Scope note Performance and Observability rows vs the corrected § SD-I-04** | Lines `:55` and `:59` read against Check 2 and Check 3 | **Agree**, including the Observability row's *"The other eleven months … produce no access row; they are reconciled against the coverage report's own per-month output"* — which is also where finding 8's gap is faithfully reproduced |
| 17 | **DISC-I-3's addition vs the "Two facts run the other way" lead-in** | Read the lead-in and the three DISC blocks | **Not broken.** The lead-in reads *"**Three** facts run the other way"* with the parenthetical *"(Two at first issue; DISC-I-3 registered 2026-09-01 on adversarial finding 5.)"*, and exactly three DISC blocks follow |
| 18 | Printed count — **8** design sections | `grep "^## SD-I-"` on the pre-`## Review` body | **Confirmed.** Nine headings `SD-I-00 … SD-I-08`, minus the state record = **8** |
| 19 | Printed count — **10** coverage rows in each, **identical membership** | Parsed both tables programmatically and set-differenced **in both directions** | **Confirmed.** Both = `{FR-P1-02-1,-7,-2,-3,-4,-5,-8, NFR-AUD-01, NFR-DQ-01, NFR-SEC-01}`; **A−B = ∅, B−A = ∅** |
| 20 | Printed count — **2** rows with no acceptance row | Counted `NO ACCEPTANCE ROW` cells in both tables | **Confirmed: 2 in each** (FR-P1-02-7, FR-P1-02-8) |
| 21 | `config.py`'s `__all__` = **17**, `SchemaError` absent | Parsed `__all__` and printed the list | **Confirmed: 17 names**; `SchemaError` absent from `__all__` **and from the whole file** |
| 22 | The `{InventoryError, AuditScopeError, SchemaError}` derivation | `RAISES` at `business-logic-model.md:108, 175, 323, 351` → `{InventoryError, RegistryError, SchemaError, LockedTestError, AuditScopeError}`, minus `__all__` | **Confirmed exactly three.** Routing `SchemaError` to the gate rather than folding it into Q2 remains correct |
| 23 | The **7 / 1 / 2** decomposition | Re-derived: SD-I-01→I-2, -03→I-1, -04→I-2, -05→I-2, -06→I-1, -07→I-1, -08→I-3 = **7**; SD-I-02 shared = **1**; here-only subjects = **2** | **Confirmed; 7 + 1 = 8** matches the section count |
| 24 | The `{6}` FR-P1-02 set difference | `grep -oE "FR-P1-02-[0-9]+" requirements.md \| sort -u` | **Confirmed `{1..8}` exactly** ⇒ difference is **`{6}`** and nothing else |
| 25 | The change record's **3** edits, stated identically at every site | Four sites across both artifacts | **Confirmed consistent** |
| 26 | DISC-I-1's five spellings, zero matches in three files | `grep -cinE` on `services.md`, `components.md`, `component-methods.md` | **Confirmed: 0 / 0 / 0** |
| 27 | **No satisfaction or discharge claim** | `grep -niE "igrf-?1[0-9]\|igrf[0-9]"` (**zero hits**) and `grep -ni igrf` (every hit is `TBD — freeze gate` or a citation); read every `Status` cell | **Confirmed.** No IGRF version named; **0** rows claimed satisfied; no gate, acceptance row or test claimed passing; BLK-07's authorization limb stated open in both; no module write authorised; no scientific value decided |
| 28 | Workspace state claims | `ls` of `configs`, `src/data`, `tests`, `evidence` | **Confirmed.** No `configs/`; none of the four named files; `src/data` = `config.py`, `locked_test.py`, `release.py`; `tests/` = **6** modules; `evidence/merge_run_access_log.jsonl` absent |
| 29 | Access-log claims | `wc -l`; `grep -o` on `purpose` and `run_id` | **Confirmed.** **158** rows, **158/158** `coverage_audit`, `test_release_hashes` (150) + `test_acquisition_window` (8) = 158 — the constant-`run_id` problem SD-I-05 describes is real and unchanged |
| 30 | `produces_kinds` yields exactly two artifacts for `library` | Stage frontmatter `:14-24` | **Confirmed.** `logical-components: [service, ui, library]`; `security-design` carries no `produces_kinds` entry; the other three are `[service]`/`[service, ui]` and absent by design |

### Validation tool results

The stage declares four sensors and no stage-specific validator; all four were exercised by proxy.

| Sensor | Method | Result | Interpretation |
|---|---|---|---|
| `required-sections` | `grep -c "^## "` | **15** H2 in `security-design.md`, **7** in `logical-components.md` | **PASS.** No team template exists under `memory/templates/`, so the registry default (≥2) applies |
| `upstream-coverage` | Counted references to each of the six `consumes` artefact names in both files | All six named in **both** files (`security-requirements` 5/1, `tech-stack-decisions` 1/1, `business-logic-model` 11/1, and the three absent-by-design categories 1/1 each) | **PASS** |
| `linter` | Fenced-block scan | **0** fenced blocks in either artifact | **N/A** |
| `type-check` | Same | **0** | **N/A** |

### Coverage limits — what I did not check, and why

- **Sibling units' Construction records were not opened** (read-scope bound, enforced by the harness hook this pass). Every cross-unit claim remains this unit's own characterization, unverified: `acquisition`'s R-32 named accessors, R-33, R-34, R-36, SEC-A-03 limb 1 and its *"three amendments"*; `foundation`'s R-01 any-future clause and the 2026-08-28 `PartitionError` declaration-site ruling; `governance-guards`' R-23, R-25, R-27, R-28 and R-50; `evaluation-and-comparison` R-109; `features-and-splits`' frozen-hash ordering artifact; `target-standardization`'s mislabel injection. `logical-components.md` § Sources also cites `../../foundation/nfr-design/logical-components.md` and `../../governance-guards/nfr-design/logical-components.md`; **neither was opened**, so the sibling-criterion comparison in § The boundary criterion is unverified.
- **Finding 9 was verified against `src/data/locked_test.py`, an ordinary workspace path**, not against `governance-guards`' design prose. What I establish is the guard's **scan bound in code** and the file inventory it faces; whether `governance-guards` intends a wider scan is out of scope here.
- **`evidence/DECISIONS.md` was not read.** D-1, D-2, D-9, D-11, D-12, D-15, D-18, D-24, D-31 and the G-09 signature are taken as stated. D-2 and D-12's thresholds were cross-checked only against `requirements.md:349-350`.
- **No test was executed.** `pytest` was not run; `_imported_modules` and `assert_no_december_outside_restricted` were established by reading source.
- **`nfr-requirements`' own internal correctness** is out of this stage's scope; only what this stage changed relative to it was checked.

### Summary

The Critical repair is real. FR-P1-02-3's scoping is supported **verbatim** at
`requirements.md:349`, the two-class routing is buildable against the workspace as it
actually is, no ordinary-path read can crash, and every surviving *"every read" / "each
artifact"* in either artifact is either month-qualified or an explicit quotation of the
withdrawn text. Repairs 2, 3, 4, 5, 6 and 7 were each verified independently of the
remediation table and each holds; the two recounts (three unbuilt + one half-built; four
absent things) were re-derived from the corrected guard table rather than accepted, and both
are right. **All 30 checks above reproduced the artifacts' claims except the two that became
findings 8 and 9**, including every printed count, both coverage tables' membership with an
empty set difference in both directions, the `{InventoryError, AuditScopeError, SchemaError}`
derivation, the 7/1/2 decomposition, the `{6}` difference, and the `components.md:64` / `:169`
line citations — one of which shows my own iteration-1 finding 5 was wrong on its TA-08 limb,
correctly refused rather than adopted.

Both remaining Majors are **artefacts of the repair itself**, which is the pattern this
project has recorded twice before. Finding 8 is a one-sentence domain widening: the repair
gave the eleven ordinary months a report-presence reconciliation and did not extend it to
December, leaving FR-P1-02-3's own criterion — *"the coverage report covers all twelve
months"* — unenforced on the locked month. Finding 9 is the more consequential to weigh at the
gate: the routing table classifies by **path** while the prose classifies by **record date**,
and the guard the artifact names as reconciling the two scans `*.json` only against 33 CSV and
4 MD files sitting outside the restricted root — so a December-bearing CSV filed under
`audit_evidence_2022-01/`, the exact TEC-09 failure, would be read as an ordinary path and
never logged. Neither is a blocker: nothing is unbuildable, no count is wrong, no gate or
acceptance row is claimed, the IGRF version stays `TBD — freeze gate`, BLK-07's authorization
limb is stated open in both artifacts, and no run may touch calendar 2022-12 while it stands.
**READY** on 0 Critical and 2 Major — with findings 8 and 9 put to the human at the approval
gate as corrections owed before 3.5 implements § SD-I-04.
