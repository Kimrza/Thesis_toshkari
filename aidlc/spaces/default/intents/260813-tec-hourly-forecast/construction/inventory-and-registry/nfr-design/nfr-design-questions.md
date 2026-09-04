# NFR Design — Questions — `inventory-and-registry`

**Unit** `inventory-and-registry` (Bolt 4) · **Kind** `library` · **Stage** `nfr-design`

Two artifacts only — `security-design.md` and `logical-components.md`. `produces_kinds`
maps the other three to `[service]` / `[service, ui]`, and this unit is `library`.

**Nothing below decides a scientific value.** TE §18.2's absolute rule stands. The IGRF
version stays `TBD — freeze gate` (TS-I-01); no question here fills it.

> ## ⚠ UPSTREAM STATUS CLAIMS CHECKED AGAINST THE WORKSPACE, 2026-09-01
>
> `nfr-requirements` for this unit was written on 2026-08-31 / 2026-09-01, and parts of it
> are already stale. Verified before drafting these questions, per the owner's 2026-09-01
> ruling that designs are written against **current state** while `nfr-requirements` itself
> stays unchanged:
>
> | Upstream claim | Actual state |
> |---|---|
> | SEC-I-02 § Status: *"Cannot run. **BLK-07 is open** and `acquisition`'s accessor does not exist."* | **Half stale.** The **read** chokepoint exists — `open_restricted` at `src/data/locked_test.py:147`, with `AccessRecord`, `PURPOSES` and the durable `_append_and_flush`. The **write** contract (R-33) still does **not** exist. BLK-07's authorization limb is untouched by either fact. |
> | SEC-I-01 limb 1: the declared flag | **Built.** `AccessRecord.performance_inspected` is a required field, and `PURPOSES` is a validated `frozenset({"coverage_audit", "regime_audit", "locked_evaluation"})` — W-6's two typed rows are already expressible. |
> | SEC-I-03 `[Q2]`: *"a re-run produces a second full set of access rows… the mechanism to distinguish attempts is named as owed"* | **Partly answered.** `AccessRecord.run_id` exists and is required non-empty, and the guard stamps its own `logged_at_utc`. What is still owed is the **convention** that gives each audit attempt a distinct `run_id`. |
> | `business-logic-model.md` W-9: *"`src/` … DO NOT EXIST"*, *"`tests/` holds three modules"* | **Stale.** `src/` exists with all six §12 packages and three modules under `src/data/` (`config.py`, `locked_test.py`, `release.py`). `tests/` holds **six** modules. `configs/`, `src/data/inventory.py`, `src/data/registry.py`, `scripts/01_inventory_and_registry.py` and `tests/test_station_registry.py` still do **not** exist. |
> | W-9: *"No December access of any kind occurs in this Bolt."* | **Holds.** `evidence/merge_run_access_log.jsonl` does not exist; `merge_coverage_year.py` has been routed through the guard but not re-run. The only access log present is `evidence/test_run_access_log.jsonl` (158 rows, all `purpose: coverage_audit`, from `test_release_hashes` and `test_acquisition_window`). |
>
> **The live gap in this unit is that its two modules do not exist at all.** Nothing here
> claims otherwise, and no question below authorises writing them.

**What is already fixed upstream and is not re-asked.** The audit's scope check is
**declared-versus-required against a governed reference set derived from the release
inventory** (W-6, Q4 = C), failing with `AuditScopeError` **before any read**. Every read
routes through `acquisition`'s named accessor, logged durably **before** the read. An
interrupted audit yields **no report** and re-runs from the start, while its rows stand
permanently (SEC-I-03, Q2 = A). Membership is derived from **record timestamps**, never a
directory name. Coverage figures carry the **`data07_caveat`**, sourced from that month's
`provenance_class`. A conflict resolved by **averaging** fails against the **named** source
(W-3). None of that is reopened here.

---

## Question 1

SEC-I-01 limb 2 requires the December-audit code path to import **no** module under
`src/models/` or `src/evaluation/`, *"directly or transitively"*, asserted by a test —
and TS-I-02 makes **transitive** the load-bearing word: *"the failure that matters is
`src/data/audit.py` importing a helper that imports `src/evaluation/metrics.py`."*

Two workspace facts decide how this can actually be built:

1. `component-dependency.md`'s matrix marks `src/data` → `models` and `src/data` →
   `evaluation` as **`—` (absent)**, not **`X` (forbidden)**. The matrix states the
   difference itself: *"a forbidden edge needs a test and an absent one does not."*
2. The same matrix gives `scripts/*` (all others) a **`yes`** against both `models` and
   `evaluation`. The audit's own stage script, `scripts/01_inventory_and_registry.py`, is
   in that row — so a boundary stated over `src/` alone leaves the script free to import
   what the module it calls may not.
3. `tests/test_phase_boundary.py`'s `_imported_modules` helper parses **one file's direct
   imports** with stdlib `ast`. There is no transitive closure anywhere in the repository
   today.

How should the boundary be expressed and enforced?

A. **Package-wide, promoted to a forbidden edge** — state it as `src/data/*` and
   `scripts/01_inventory_and_registry.py` may not import `src/models/*` or
   `src/evaluation/*`, promote both matrix cells from `—` to `X`, and enforce with the
   existing per-file direct-import check applied to every file in the constrained set
   > **Impact**: No transitive walker is needed and none is written: if every file in the constrained set is checked directly, a chain through the set is caught at its first hop. It reuses `_imported_modules` unchanged. It is **broader than the requirement** — it binds `release.py`, `config.py` and every future `src/data` module, not only the audit — and it **amends an approved application-design artifact**, so a change record is owed. Its real gap is stated rather than hidden: a chain leaving the constrained set (audit → `src/external/spaceweather` → `src/evaluation`) is not caught, because `src/external` is not in the set.

B. **Entry-point reachability, with a real transitive walk** — state the boundary over the
   audit entry point only, build the module graph across `src/` and `scripts/` from
   `_imported_modules`, close it transitively from that entry point, and fail if the
   closure contains `src/models/*` or `src/evaluation/*`
   > **Impact**: This is what the requirement literally asks for, and it is the only option that catches a chain through **any** package, including `src/external`. It leaves `component-dependency.md` untouched, so no amendment is owed. It costs a new graph-closure helper — cycle handling, unresolvable dynamic imports, and a decision about what an unparseable file means (`governance-guards` R-27 already fixes that: unparseable is a failure). It also binds nothing until the audit module exists, so the test is written against a module that is absent today.

C. **Both limbs** — the package-wide forbidden edge from A **and** the entry-point
   reachability closure from B, as two separately named results
   > **Impact**: Closes A's escape route and B's breadth gap together, and matches this project's own repeated pattern of two independent checks over one rule (W-6's three scope checks; R-23's two limbs; G-2's two scans). It is the most work of the three and produces two tests to maintain, and it still owes the same change record A does.

D. **Defer the mechanism to 3.5**, stating only that the constraint binds a code path
   > **Impact**: Nothing is designed against a module that does not exist. It also leaves this stage's one genuinely new security requirement with no design, and TS-I-02 has already deferred the *expression* to 3.5 once — deferring it twice is how a requirement arrives at code-generation with nothing to build.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C — the decisive fact is #2. A boundary that binds
> `src/data/audit.py` but not `scripts/01_inventory_and_registry.py`, the script that
> **calls** it, is not a boundary; and the matrix currently grants that script `yes`
> against both packages. A alone fixes that but cannot see through `src/external`; B alone
> sees through everything but leaves the matrix saying the edge is merely absent, which the
> matrix itself says means no test is owed. Together they are the same two-independent-checks
> shape this unit already uses for its scope validation, and the amendment C owes is one
> change record promoting two cells, not a new mechanism. The cost is honest: two tests, and
> a graph-closure helper this repository does not have yet.

[Answer]: C

---

## Question 2

W-1 declares `RAISES InventoryError` and W-6 declares `RAISES AuditScopeError`. **Neither
exception exists.** `foundation` R-01 fixes that every project-defined exception derives
from `IntegrityError`, declared in `src/data/config.py`, whose constructor requires a
**resource** and a **violated expectation**.

R-01's own history is the relevant precedent, and it cuts both ways. `PartitionError` was
**promoted into R-01's enumeration** as its fifteenth entry under `GOV-2026-08-28-FD-01`
Recommendation 8, with the declaration site ruled to be `config.py` and the semantic owner
left as `models-and-baselines`. `InverseTransformError` was **not** enumerated — it rides
R-01's *"any future integrity-related exception"* clause, on the stated ground that the two
units raising it agree on its condition and meaning, so nothing needed reconciling. R-01
*"deliberately stopped asserting a count after its enumeration went stale twice."*

Where do these two exceptions live, and what status do they carry?

A. **Declared in `src/data/config.py`, riding R-01's any-future clause** — both derive from
   `IntegrityError`, both are added to `__all__`, neither is claimed as an enumeration entry
   > **Impact**: Follows the `InverseTransformError` precedent exactly and needs no change record. Both are raised by one unit only, so there is no cross-unit meaning to reconcile — the discriminator that promoted `PartitionError` does not apply. Every package can import them, which matters because a future consumer of the coverage report may want to catch `AuditScopeError`. It grows `config.py`'s `__all__` by two without growing R-01's enumeration, which a reader may misread as an oversight unless the module says why.

B. **Declared in `config.py` and formally promoted into R-01's enumeration** — the
   `PartitionError` path, with a change record
   > **Impact**: The enumeration stays a complete list, which is easier to read than a list plus an unwritten clause. It reopens a count R-01 deliberately stopped asserting after two stale enumerations, and it spends a change record on a status question with no behavioural consequence — the class derives from `IntegrityError` either way.

C. **Declared in the unit's own modules** — `InventoryError` in `src/data/inventory.py`,
   `AuditScopeError` in `src/data/registry.py`
   > **Impact**: Ownership sits with the code that raises. It contradicts R-01's declaration-site rule and the 2026-08-28 owner ruling that moved `PartitionError`'s declaration site *into* `config.py` for exactly this reason: an exception declared in a leaf module cannot be caught by a package that must not import that module.

D. **Reuse existing classes** — `ConfigError` for the inventory, `LockedTestError` for the
   audit scope
   > **Impact**: No new classes at all. It makes a short **scope declaration** indistinguishable from a **chokepoint breach**: `LockedTestError` today means a restricted read was attempted outside `open_restricted`, or its log write failed. A caller that catches it to report a containment failure would report one for an audit that never touched the restricted root.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the precedent that fits is `InverseTransformError`, not
> `PartitionError`. Both new exceptions are raised by this unit alone, so there is no
> cross-unit disagreement to reconcile, which is the stated discriminator for promotion.
> D's cost is concrete and worth naming: `AuditScopeError` fires when the audit's *own
> declaration* is short, before any restricted path is opened, and collapsing that into
> `LockedTestError` would make the log say a containment guard fired when none did. What A
> owes is one sentence in `config.py` recording that these two ride the clause and why —
> the same sentence `InverseTransformError` already carries.

[Answer]: A

---

## Question 3

`src/data/config.py` declares `RegistryError` with this docstring: *"An experiment-registry
write would be lost, silently overwritten, or reordered."* That is `foundation`'s
experiment registry (R-08, R-18, TE §13.4's twenty-column schema).

W-2 declares the **station registry** build `RAISES RegistryError` — the same class — for
an entirely different failure: a missing §6.2 field, an `igrf_version` that is a **default
rather than a pin**, or a conflict resolved by **averaging**. TS-I-04 already flagged the
collision in prose: *"'Registry' in this unit's name means the station registry… stated
because the two are easy to conflate."*

The concrete failure this creates: a caller catching `RegistryError` to retry or report a
lost registry **write** would swallow a station-registry **provenance** failure — the exact
class of defect W-3's whole mechanism exists to make loud.

W-2's `RAISES RegistryError` is an **approved `functional-design` contract**. How should
this stage handle the collision?

A. **Keep `RegistryError` as W-2 names it, and make the two distinguishable by the
   `resource` argument R-01's constructor already requires** — widen `config.py`'s
   docstring to name both registries, and require every station-registry raise to name the
   registry artifact as its resource
   > **Impact**: The upstream contract is preserved exactly and no change record is owed. R-01's constructor already forces a non-empty resource, so the discriminator exists today and costs nothing to use. The residual is real and would be recorded rather than designed away: a caller catching `RegistryError` **by type** still cannot distinguish the two, and only a caller that reads `.resource` can.

B. **Split into a distinct `StationRegistryError`** — a new class beside `RegistryError`,
   with a change record against W-2's approved `RAISES` line
   > **Impact**: Type-level separation, so `except RegistryError` cannot swallow a provenance failure. It changes an approved `functional-design` contract from a downstream stage, which `project.md` warns against: *"a stage answer cannot move a requirement out of the layer the authority document places it in."* The change record is owed to `functional-design`, not resolvable here.

C. **Rename `RegistryError` to `ExperimentRegistryError` and give the station registry the
   plain name**
   > **Impact**: The clearest end state, and the most disruptive: `RegistryError` is `foundation`'s, declared and documented, and renaming it touches a sibling unit's approved contract plus every future caller. It trades one collision for a rename this stage has no authority to make.

D. **Record the collision as a limitation and change nothing** — no docstring edit, no new
   class
   > **Impact**: Zero footprint. It leaves `config.py`'s docstring stating, as fact, that the class means an experiment-registry write failure — while this unit raises it for something else. An implementer reading the declaration site would be misled by the artifact that is supposed to be authoritative.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — B and C are both better designs in isolation and both
> require this stage to overrule an approved upstream contract, which is precisely the move
> `project.md` records as a repeat failure. A keeps W-2's contract, uses a discriminator
> R-01 already mandates, and states the residual honestly instead of claiming the collision
> is resolved. If the owner wants type-level separation, B is the right shape — but it
> should be routed as a change record against `functional-design`, not decided here.

[Answer]: A

---

## Question 4

`logical-components.md` needs a boundary criterion. The two sibling units chose different
ones and both stated why: `foundation` drew on **failure consequence** (a bad read fails a
run, a bad write corrupts the record); `governance-guards` drew on **enforcement timing**
(a static-scan failure is a warning, a run-time guard failure stops the run), mirroring
R-24's own hierarchy.

This unit's material has a distinctive property neither sibling shares. W-6 states it
directly: *"a silently skipped month produces a wrong figure that looks right"* — and that
figure is what a **supervisor** accepts at G-P1A. W-2/W-3/W-4, by contrast, raise and stop.
W-7/W-8 neither compute nor raise: they **aggregate results other units own** and put a
signature behind them.

What criterion should the decomposition use?

A. **How the failure reaches a human** — three components: (I-1) build-time integrity, which
   **raises and stops** before anything downstream runs; (I-2) the December audit, which
   **fails silently into a number** a supervisor signs; (I-3) the G-P1A gate record, which
   **asserts others' results** and whose blast radius is a signature
   > **Impact**: It makes the one property that distinguishes this unit from its siblings the axis of the diagram, and it puts W-6 in a box of its own — which is right, because it is the only workflow here whose defect mode is a plausible wrong answer rather than an exception. It is the same *kind* of criterion as `foundation`'s, applied to this unit's material, so the two stay comparable. It splits W-5 (schema validation) from W-6 (the audit) even though both read prepared artifacts, which needs a sentence of justification.

B. **By artifact owned** — the source inventory, the station registry, the audit, the gate
   record: four components matching the four things this unit produces
   > **Impact**: Immediately legible and maps 1:1 onto the `Owns` list in `unit-of-work.md`. It is silent on failure behaviour, so it puts a fail-fast build and a silently-wrong audit in adjacent boxes with nothing marking the difference — the same flattening `governance-guards` rejected when it declined to group a static scan with a run-time assertion.

C. **By module** — `src/data/inventory.py`, `src/data/registry.py`, and the stage script
   > **Impact**: True to how the code is imported, and the easiest to verify against the workspace. It is a module listing rather than a decomposition, and both siblings explicitly rejected this shape for that reason.

D. **By requirement** — grouped by FR-P1-02-1/-2/-7, -3, and -4/-5/-8
   > **Impact**: Traceability is direct and the coverage table writes itself. It splits nothing by behaviour and merges W-7 and W-8 with W-2's registry work only because their requirement IDs are adjacent.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the criterion should isolate the property that actually
> governs risk here, and in this unit that is **whether a defect announces itself**. I-1
> cannot reach a supervisor undetected because it raises; I-2 can, and that is the whole
> reason W-6 carries three independent scope checks rather than one; I-3 carries no
> computation at all, so its failure mode is a missing result nobody noticed. B's weakness
> is specific: it would place the audit beside the schema validator, and the schema
> validator is a fail-fast check while the audit is not.

[Answer]: A

---

## Consolidated Summary Confirmation

**Q1 — the audit's import boundary**: **C. Both limbs.** A package-wide forbidden edge over
`src/data/*` **and** `scripts/01_inventory_and_registry.py` against `src/models/*` and
`src/evaluation/*`, promoting two `component-dependency.md` cells from `—` to `X` (change
record owed), **plus** an entry-point reachability closure built from
`_imported_modules` that catches a chain leaving the constrained set. Two separately named
results, on this unit's own two-independent-checks pattern.

**Q2 — the two new exceptions**: **A. Declared in `src/data/config.py`, riding R-01's
any-future clause.** `InventoryError` and `AuditScopeError` derive from `IntegrityError`
and are added to `__all__`; neither is claimed as an R-01 enumeration entry, on the
`InverseTransformError` precedent. `config.py` records why in one sentence. No change
record.

**Q3 — the `RegistryError` collision**: **A. Keep the class, discriminate on `resource`.**
W-2's approved `RAISES RegistryError` stands; `config.py`'s docstring is widened to name
both the experiment registry and the station registry; every station-registry raise names
its registry artifact as the resource R-01's constructor already requires. The residual is
recorded, not designed away: a caller catching `RegistryError` **by type** still cannot
separate the two. Type-level separation stays available as a change record against
`functional-design`.

**Q4 — the component boundary criterion**: **A. How the failure reaches a human.** Three
components — build-time integrity that **raises and stops**; the December audit that
**fails silently into a number** a supervisor signs at G-P1A; the G-P1A gate record that
**asserts results other units own**, whose blast radius is a signature.

**Unchanged by these answers.** No scientific value is decided. The IGRF version stays
`TBD — freeze gate`. BLK-07's authorization limb stays open and no December access occurs.
No module is written by this stage.

- Looks correct
- Request changes

[Answer]: Looks correct

---

## Requested Changes Feedback

What should change?

[Answer]: Fix all findings until all are clean. (Owner instruction, 2026-09-02.) This unit's two
open Majors from the 2026-09-01 terminal pass are in scope: the split reconciliation leaving
December in neither limb, and `assert_no_december_outside_restricted` scanning `*.json` only
while the routing depends on it. `SchemaError`'s declaration site stays **routed to the gate**
— a blanket instruction to fix findings is not a ruling on a decision explicitly reserved to
the owner, and Q2 was answered on a two-item scope.
