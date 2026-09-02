# Logical Components — `inventory-and-registry`

**Unit** `inventory-and-registry` (Bolt 4) · **Kind** `library` · **Stage** `nfr-design`

> ## ⚠ NONE OF THESE COMPONENTS EXISTS
>
> Unlike `governance-guards`, whose decomposition described a mixed state, **every component
> below is unbuilt**. `src/data/inventory.py`, `src/data/registry.py`,
> `scripts/01_inventory_and_registry.py` and `tests/test_station_registry.py` do not exist,
> and neither does `configs/`. What **does** exist is the shared machinery two of these
> components depend on — `src/data/config.py`, `src/data/locked_test.py`,
> `src/data/release.py` — and § Shared resources says exactly which parts.
>
> **This is a logical decomposition, not an infrastructure deployment.** No services, no
> processes, no network boundaries. `inventory-and-registry` is a **library plus one stage
> script plus its tests**, and its "failure domains" are the blast radii of function calls in
> one process.
>
> **No December access occurs in this Bolt.** `evidence/merge_run_access_log.jsonl` does not
> exist; the only access log present is `evidence/test_run_access_log.jsonl` (158 rows, all
> `purpose: coverage_audit`). **BLK-07's authorization limb is open**; **G-09 is signed
> (D-31) with preconditions UNMET**; the §18.3 preflight has never run.

## Sources

- `security-design.md` — **SD-I-00** … **SD-I-08**, this stage's sibling artifact. The boundaries below are where those decisions land, and § SD-I-00 carries the workspace evidence and the two discrepancies.
- `../nfr-requirements/security-requirements.md` — **SEC-I-01** … **SEC-I-05** as the requirement set; **three status claims superseded**, per § SD-I-00.
- `../nfr-requirements/tech-stack-decisions.md` — **TS-I-01** … **TS-I-05**.
- `../functional-design/business-logic-model.md` — **W-1** … **W-9**; `../functional-design/business-rules.md` — **R-44** … **R-53**.
- **`performance-requirements.md`, `scalability-requirements.md` and `reliability-requirements.md` are absent by `produces_kinds` design** for a `library` unit; assessed in `security-design.md` § Scope note.
- `../../foundation/nfr-design/logical-components.md` and `../../governance-guards/nfr-design/logical-components.md` — the two sibling decompositions and their stated criteria.
- **The workspace, read 2026-09-01** — `src/data/config.py`, `src/data/locked_test.py`, `src/data/release.py`, `scripts/merge_coverage_year.py`, `tests/` (six modules).
- `../../../inception/application-design/services.md`, `components.md`, `component-methods.md`, `component-dependency.md`.
- `../../../inception/requirements-analysis/requirements.md` — **FR-P1-02-1** … **-5**, **-7**, **-8**; **NFR-AUD-01**, **NFR-DQ-01**, **NFR-SEC-01**.
- `nfr-design-questions.md` — **Q4 = A**, and the receipted Consolidated Summary Confirmation.

---

## The boundary criterion (Q4 = A)

**The boundary is drawn on how a failure reaches a human.**

> **Some defects here raise and stop. One fails silently into a number a supervisor signs.
> One is a signature over results this unit did not compute.**

W-6 states the middle case in its own words: *"a silently skipped month produces a wrong
figure that looks right."* That figure is what a **supervisor** accepts at G-P1A. Nothing
else in this unit behaves that way — W-1 through W-5 raise, and W-7/W-8 compute nothing.
A decomposition that did not isolate it would put the unit's only silent-failure workflow in
the same box as its fail-fast ones, and the entire reason W-6 carries **three independent
scope checks instead of one** is that its defect mode is a plausible answer rather than an
exception.

**Consistency with the siblings, without being forced into their shape.** `foundation` drew
on **failure consequence** (a bad read fails a run, a bad write corrupts the record);
`governance-guards` on **enforcement timing** (a warning to fix versus a stop). This unit
uses the same *family* of criterion — what the failure does — applied to the property its own
material actually varies on. The three stay comparable; none is a copy.

**Why not "by artifact owned"** (inventory / registry / audit / gate record). It maps 1:1
onto `unit-of-work.md`'s `Owns` list and reads well, and it is silent on failure behaviour:
it would seat the **schema validator** (fail-fast) beside the **audit** (silently wrong)
with nothing marking the difference — the same flattening `governance-guards` rejected when
it declined to group a static scan with a run-time assertion.

**Why not "by module".** True to how the code is imported, silent on the property that
matters, and a module listing rather than a decomposition. Both siblings rejected it for that
reason.

**Why not "by requirement".** Traceability is direct, but FR-P1-02-4/-5/-8 group with the
registry work only because their IDs are adjacent, and FR-P1-02-3 alone would carry the one
component whose isolation is the point.

**One split this criterion forces, justified rather than absorbed.** W-5 (schema validation)
and W-6 (the audit) both read prepared artifacts and both emit a report, so an artifact- or
module-shaped decomposition would keep them together. They are separated here because **W-5
raises `SchemaError` and stops, while W-6 emits a number** — and a schema report that is
wrong is a schema report that failed to be produced, whereas a coverage report that is wrong
is a coverage report that was produced and signed.

---

## Component inventory

| # | Component | Contents | How its failure reaches a human | State on disk |
|---|---|---|---|---|
| **I-1** | **Build-time integrity** | source inventory (W-1); station registry and per-field provenance (W-2, W-2a); conflict resolution against the **named** source (W-3); the frozen-literal migration and its diff (W-4); schema validation of the prepared product (W-5) | **Raises and stops** — `InventoryError`, `RegistryError`, `SchemaError`. Nothing downstream runs. | **Unbuilt** |
| **I-2** | **The December audit** | scope declaration and the declared-versus-required check; the two typed logged reads; the counts; the reconciliation; the import boundary that keeps it performance-blind (W-6) | **Fails silently into a number** a supervisor accepts at G-P1A — unless one of three independent checks fires first | **Unbuilt**; its chokepoint dependency is built |
| **I-3** | **The G-P1A gate record** | the two-threshold decision record with every figure attributed (W-7); the assertion that all four prohibition results are present and passing (W-8) | **A signature over results this unit did not compute.** Its failure is a missing or unattributed result nobody noticed | **Unbuilt** |

### I-1 — Build-time integrity (raises and stops)

**Blast radius: the run attempting it, and nothing beyond.** Every member raises before its
output reaches a consumer. `assert_registry_resolved` raising **blocks `station_lat` and
excludes `lst_sin` / `lst_cos`**, so `features.build` calls it before constructing either —
the failure is contained by the call order, not by a downstream check.

**Why these five belong together.** They share a failure consequence *and* a failure
**visibility**: an implementer sees a traceback, and R-01's constructor contract guarantees
that traceback names the **resource** and the **violated expectation**. None of them can
produce a wrong-but-plausible artifact, because none of them produces an artifact when it
fails.

**The two design decisions that land here.**

- **§ SD-I-03 — the `RegistryError` collision.** W-2's approved `RAISES RegistryError` is the
  same class `foundation` uses for a lost **experiment-registry write**. Inside this
  component the discriminator is the **resource**: every station-registry raise names the
  registry artifact or the `station_id` whose field failed. The residual stands — a caller
  catching **by type** cannot separate the two.
- **§ SD-I-06 — the inventory's `licence and access notes` field is a secret-egress
  surface.** TE §5.1 requires it, W-1 fails an entry without it, and the inventory is a
  **committed** artifact in scope for NFR-SEC-01's scan. This component is a **caller** of
  `acquisition`'s redaction serializer, which **does not exist** — grep across `src/`,
  `scripts/` and `tests/` returns no `CredentialEgressError` and no redaction helper of any
  name.

> **⚠ The provenance limb is what makes this component more than presence-checking.** R-46's
> *"presence is not provenance"* means the raise is conditioned on **provenance**, not only
> on a field being populated. **What provenance is sufficient is not decided** — station
> coordinates are a §18.2 **Student** forbidden choice, the coordinate-to-cell rule a
> **Student + Supervisor** one, and **D-1's site-log validation limitation is still open.**
> A component that only checked presence would run clean today on values D-1 itself records
> as not yet validated against the higher-ranked evidence source.

> **⚠ W-3's residual belongs to this component and is not closed by it.** When an averaged
> value **coincides exactly** with the named source's value, the stored value *is* that
> source's value bit for bit, and **no check on the value can distinguish it from a
> legitimate resolution**. What reaches that case is the rationale, read by a human at
> G-P1A. The negative control must exercise the coincidence case so the limit is pinned
> rather than discovered.

### I-2 — The December audit (fails silently into a number)

**Blast radius: a supervisor's signature at G-P1A, and every claim built on the coverage
figures afterwards.** This is the largest blast radius in the unit and the only one that
does not announce itself. It is a component of its own for exactly that reason.

**Four independent guards, none substituting for another.** Three are W-6's and one is
§ SD-I-01's.

> **⚠ CORRECTED 2026-09-01 — the second and third guards were overstated.** The first issue
> of this table marked the logged read **Built: Yes** while § Shared resources on this same
> page recorded the accessor routing layer as **proposed**; the two rows contradicted each
> other. It also described the second guard as covering *"each read"*, which
> § SD-I-04's own correction shows is unbuildable: **eleven of the twelve declared months sit
> outside `evidence/locked_test_restricted/`**, and `open_restricted` refuses exactly those
> paths by contract. Both rows are restated below. Found by an adversarial pass, on the
> component this decomposition exists to isolate.

| Guard | What it proves | Built? |
|---|---|---|
| Declared **versus required**, against a governed reference set derived from the release inventory | The audit **declared everything required** — the only check that proves completeness | **No.** Entirely this unit's to build |
| A durable access row **before** each read of a **December-bearing** artifact, through `acquisition`'s named accessor | **Every read of a locked-month artifact was logged**, in an order a later artifact can be compared against | **Half.** The **chokepoint** is built — `open_restricted`, `_append_and_flush`, `os.fsync`, guard-stamped `logged_at_utc`. The **R-32 accessor routing layer is not**: it is absent from `component-methods.md`'s approved block and is amendment (1) of `acquisition`'s three |
| Rows reconciled against the **December portion** of the declared scope, **per `run_id`**; the other eleven months reconciled against the **coverage report's own per-month output** | The audit **read what it declared**, and an honest re-run is legible as one | **No.** `run_id` exists as a required field, but the **uniqueness convention** does not, and neither reconciler exists |
| The **import boundary** — Limb A's forbidden edge and Limb B's reachability closure | The audit **could not have seen a performance figure**, rather than merely declaring it did not | **No.** `_imported_modules` is the primitive; the closure does not exist |

**Why the fourth guard is in this component and not a cross-cutting concern.** The
`performance_inspected=false` flag is **a value the caller sets**. Limb A and Limb B are what
make December-blindness *structural*, and they constrain **this component's code path** —
including, under Limb A, `scripts/01_inventory_and_registry.py`, because
`component-dependency.md` grants the `scripts/*` row `yes` against both `models` and
`evaluation`. A boundary that bound the module but not the script that calls it would not be
a boundary.

> **⚠ DISC-I-1 lands squarely on this component.** **No approved application-design row owns
> this component's two output artifacts.** `services.md` gives `01_inventory_and_registry.py`
> the outputs *"source inventory (§5.1 nine fields), station registry"* and names neither the
> coverage report nor the regime-count report; grep across `services.md`, `components.md`
> and `component-methods.md` for those five spellings returns **zero matches in all three**.
> Limb A's constrained set assumes this component lives in
> `scripts/01_inventory_and_registry.py`; **if 3.5 places it elsewhere, the constrained set
> must move with it**, and that is a boundary defect, not a relocation.

> **⚠ The two limbs are two typed reads, and `locked_evaluation` is refused.**
> `purpose="coverage_audit"` and `purpose="regime_audit"`, each `performance_inspected=False`,
> `locked_test_accessed=True`, `authorization` referencing **Vision §8.3**. A read attempted
> under `purpose="locked_evaluation"` is refused: that literal is G-06's, and an audit
> carrying it would trip `evaluation-and-comparison` R-109's must-not-fire control and block
> the read §8.3 **requires** — the *"opened exactly once"* misreading `team.md` records this
> project having already corrected once.

**Every coverage figure leaves this component carrying `data07_caveat`**, sourced from that
month's `provenance_class` (`acquisition` R-36) rather than restated. **A figure emitted for a
`derived_only` month with no caveat field fails.** The source field **reaches no other unit
today**; if it is absent at implementation, R-50 requires a **stop-and-report under TE §18.3**
rather than an uncaveated figure.

**What this component must not do, restated because the constraint is easy to invert.** It
adds a constraint on **what the audit may import**, never on **whether it may run**. Vision
§8.3 makes the performance-blind coverage and regime audit a **precondition of G-05**; a guard
that blocked it would breach §8.3 as surely as one that let a model see December.

### I-3 — The G-P1A gate record (a signature over others' results)

**Blast radius: a gate decision, and it is the only component whose failure mode is an
absence.** I-3 computes nothing and raises nothing on its own behalf. It **assembles**: two
thresholds with every figure attributed to the D-number it is judged against (W-7), and an
assertion that **four separately named results** are present and passing (W-8).

**Two of the four results are not this unit's.** Prohibition 3 (retrospective split redesign
after performance is viewed) is `features-and-splits`' **frozen-hash ordering artifact** —
which cannot be an injection test, because the prohibited act is *a person changing a design
after seeing a result*, and no injected value proves that did not happen. Prohibition 4
(labelling a map value as station-observed VTEC) is `target-standardization`'s. **I-3's
obligation is to assert all four are present and passing**, not to own three of the four
tests.

> **⚠ This component is where the FR-P1-02-8 failure actually happened, and the fix is
> structural.** One citation — **`TA-29`, a row `requirements.md` lists under "Not applicable
> in Phase 1 — Phase 2 by definition"** — stood for **four** obligations, made the row appear
> covered, and kept it out of the untested list stage 3.2 reads to size the G-05 freeze
> manifest. **Four governance boards passed over it.** Naming the four results individually
> in the G-P1A evidence set is what makes a missing one structural rather than something a
> fifth reviewer has to notice. **The row remains UNTESTED**: naming four results is a
> mechanism, not an acceptance row.

**D-2's own disclosure travels onto this record**, and this is a component-level obligation
rather than a formatting note: five of twelve months had already been audited at 100% day
coverage when the threshold was chosen, *"not set blind… stated here so a reviewer can
discount it accordingly."* A record that omits it presents a partly post-hoc threshold as
blind — which is a defect in the **signature**, this component's whole output.

**No soft margin band.** Flagging station-months near a threshold is genuinely useful at
NICO's 93.2%, and *"near"* would be a new number invented beside a **supervisor-frozen** hard
threshold.

---

## Failure domains and blast radius

| Component | Failure announces itself? | Blast radius | Contained by |
|---|---|---|---|
| **I-1** | **Yes** — a raise naming resource and expectation | The run attempting it | Call ordering (`assert_registry_resolved` before `features.build`) and R-01's constructor contract |
| **I-2** | **No** — a plausible number | G-P1A's signature, and every claim built on FULL's coverage figures | Four independent guards, of which **three are unbuilt and the fourth is only half-built** *(recounted 2026-09-01 from the corrected guard table above; the first issue said "two are unbuilt and one is half-built", against a table that then over-claimed the logged read as Built)* |
| **I-3** | **No** — an absence | The gate decision | Four separately named results, and every figure attributed to its D-number |

**The asymmetry is the finding, not an artefact of the table.** I-1 is fully contained by
mechanisms that either exist or are ordinary code. **I-2's containment rests on four things
that do not exist yet** *(recounted 2026-09-01 from the corrected guard table; the first
issue said three, and the fourth — the accessor routing layer — was the row that had been
over-claimed as Built)* — the declared-versus-required check, **`acquisition`'s R-32 accessor
routing layer**, the `run_id` uniqueness
convention, and both limbs of the import boundary — and it is the component whose failure a
human cannot see. That is where this unit's build risk concentrates.

## Shared resources

| Resource | Owner | Used by | Note |
|---|---|---|---|
| `src/data/config.py` — `IntegrityError` and the exception hierarchy | `foundation` (R-01); declaration site ruled 2026-08-28 | I-1, I-2 | **Three exceptions this unit needs are absent**: `InventoryError`, `AuditScopeError`, `SchemaError`. Set-differenced against `__all__`'s 17 names; `SchemaError` was **not** in Q2's scope and is routed to the gate |
| `RegistryError` | `foundation` (experiment registry) | I-1 (station registry) | **A shared name for two unrelated failures.** Discriminated by `resource`; the type-level residual stands (§ SD-I-03) |
| `open_restricted`, `AccessRecord`, `PURPOSES`, the access log | `governance-guards` module; `acquisition`'s named accessors route through it | I-2 | **Built.** The accessor layer R-32 names is still absent from `component-methods.md`'s approved block and is amendment (1) of `acquisition`'s three — **this unit inherits that proposed status** |
| `acquisition`'s redaction serializer | `acquisition` (SEC-A-03 limb 1) | I-1 | **Does not exist.** A hard dependency of the inventory, not a preference |
| `configs/data.yaml` — the governed schema, the station registry values, the IGRF pin | this unit writes into it; `foundation` owns the config contract | I-1, I-2 | **`configs/` does not exist.** The **IGRF version stays `TBD — freeze gate`** and the registry cannot be built until it is frozen under a D-number |
| `provenance_class` on a month | `acquisition` (R-36) | I-2, I-3 | **Reaches no other unit today.** Absent at implementation ⇒ stop-and-report under §18.3, never an uncaveated figure |
| `tests/test_phase_boundary.py`'s `_imported_modules` | `governance-guards` | I-2 (Limb B) | Reused as a **primitive**; its existing `PHASE1_PERMITTED_PACKAGES` behaviour must not change. **NFR-PHASE-01 is not weakened and no coverage of it is claimed** |

---

## Requirement coverage

| Requirement | Component | Acceptance row | Row primary owner | Status |
|---|---|---|---|---|
| FR-P1-02-1 | I-1 | WS-01, TA-04 | **`inventory-and-registry`** (both) | `Pending` |
| **FR-P1-02-7** | I-1 | ⚠ **NO ACCEPTANCE ROW** — WS-01 reaches the registry's existence and the header cross-check only | — | untested |
| FR-P1-02-2 | I-1 | TA-04 | **`inventory-and-registry`** | `Pending` |
| FR-P1-02-3 | I-2 | WS-18, TA-25 | `features-and-splits` (WS-18); **this unit** (TA-25) | `Pending` — **authorization limb of BLK-07 open** |
| FR-P1-02-4 | I-3 | TA-25 | **`inventory-and-registry`** | `Pending` |
| FR-P1-02-5 | I-3 | TA-25 | **`inventory-and-registry`** | `Pending` |
| **FR-P1-02-8** | I-3 | ⚠ **NO ACCEPTANCE ROW** — `TA-29` **withdrawn** | — | untested |
| NFR-AUD-01 | I-2 | TA-10, TA-21 | `foundation` | `Pending` |
| NFR-DQ-01 | I-1 | **TA-19** *(row filled in at this stage from `requirements.md:487`; `—` upstream — disclosed in `security-design.md` § Requirement coverage)* | — | `Pending` |
| **NFR-SEC-01** *(added at this stage)* | I-1 | TA-22 | — | `Pending` |

**Derived and printed.** **3** components (I-1, I-2, I-3). **10** coverage rows, identical in
membership to `security-design.md`'s table — set-differenced against it in both directions,
**empty both ways**. **2** rows with no acceptance row, counted from the blank acceptance
cells above. **0** rows claimed satisfied. **0** of the three components exist on disk.

**Decomposition of `security-design.md`'s 8 design sections across the three components**,
derived rather than asserted: **7** land in exactly one component — SD-I-01 → I-2,
SD-I-03 → I-1, SD-I-04 → I-2, SD-I-05 → I-2, SD-I-06 → I-1, SD-I-07 → I-1, SD-I-08 → I-3 —
and **1** is shared, SD-I-02, whose three exceptions split across I-1 (`InventoryError`,
`SchemaError`) and I-2 (`AuditScopeError`). 7 + 1 = 8, matching the sibling's section count.
**2** subjects are here-only with no `security-design.md` counterpart: the § Failure domains
asymmetry, and DISC-I-1's consequence for Limb A's constrained set.

**A decomposition that verifies is not evidence the decomposed set is complete.** The 7 / 1 / 2
split above is arithmetically sound against `security-design.md` as written; it says nothing
about whether that artifact covers everything it should. The completeness check is the
FR-P1-02 set difference recorded in `security-design.md` § Requirement coverage, and the two
answer different questions.

**Why `FR-P1-02-6` is absent.** It is the **residency** rule, and this unit does not state
it — W-6 *depends* on restricted-root custody through `acquisition`'s named accessor, and
depending on a rule is not reproducing its text. Set-differenced at this stage against
`requirements.md`'s FR-P1-02 space `{1,2,3,4,5,6,7,8}`: the difference is exactly `{6}`.
Its coverage belongs to `governance-guards`; `requirements.md` records that it **now passes**,
enforced by `tests/test_acquisition_window.py` and `assert_no_december_outside_restricted`.

## Assumptions & Open Questions

- **[Q4]** The criterion is **how a failure reaches a human**. It forces the W-5 / W-6 split, which an artifact- or module-shaped decomposition would not; the justification is stated in § The boundary criterion rather than left implicit.
- **[DISC-I-1 — open]** **No approved component row owns I-2's two output artifacts.** Limb A's constrained set assumes I-2 lives in `scripts/01_inventory_and_registry.py`. If 3.5 places it elsewhere, **the constrained set must move with it.**
- **[Q2 / SD-I-02 — open, routed to the gate]** **`SchemaError` is a third missing exception and was not in Q2's scope.** The set difference of W-1 … W-6's `RAISES` lines against `config.py`'s 17-name `__all__` is `{InventoryError, AuditScopeError, SchemaError}`. The same disposition applies on its face; applying an owner's ruling to an item they were not shown would be a widening, so it goes to the gate.
- **[Q3 / SD-I-03 — residual]** A caller catching `RegistryError` **by type** still cannot separate I-1's provenance failure from `foundation`'s lost write. `StationRegistryError` remains available as a change record against `functional-design` and is **not** proposed here.
- **[SD-I-01 — owed]** **One change record carrying three edits**: two `component-dependency.md` cells promoted `—` → `X`, **plus a named carve-out withdrawing the `scripts/*` row's affirmative `yes` grant for `01_inventory_and_registry.py`**. The carve-out is the larger deviation — it withdraws a permission the matrix explicitly gives, where the other two record an obligation it did not have. *(Scope corrected 2026-09-01 on adversarial finding 3, Major; the first issue said "two cells".)*
- **[DISC-I-3]** `components.md:64` puts two **`acquisition`-owned** requirements — **FR-P1-01-6** and **FR-P1-01-2** — into `inventory.py`, which is I-1's module. FR-P1-01-2's suffix-mismatch half is **⚠ PROPOSED**: `acquisition` R-34 holds the release-manifest carriage of `suffix_mismatch` **Open for stage 3.2**. Neither appears in this unit's coverage table, correctly; the seam is the module, not the requirement.
- **[I-2 — OPEN, routed to the gate]** **W-6's approved mechanism carries the routing defect too** — *"for each artifact: `acquisition`'s named accessor"*, with no restricted/ordinary distinction. Corrected in this stage's artifacts and **not applied upstream**; the ruling owed at the gate is whether W-6 is amended by change record or whether the narrowing stands in the gate record alone.
- **[I-2 — the routing correction's own dependency]** The two-class routing in `security-design.md` § SD-I-04 rests on **`assert_no_december_outside_restricted` continuing to pass**: it is what keeps "December-bearing" and "under the restricted root" the same set after D-15's relocation of 21 files. **If that guard fails, the routing is wrong before the audit is** — an unrelocated December artifact would be read as an ordinary path and never logged.
- **[SD-I-05 — owed]** The **`run_id` uniqueness convention**; the field exists, nothing today makes two attempts carry different values. Format is 3.5's.
- **[SD-I-06 — hard dependency]** **`acquisition`'s redaction serializer does not exist**, and I-1's inventory entries depend on it.
- **[DISC-I-2]** `merge_coverage_year.py`'s `retrieved_at_utc` placeholder migrates into I-2's stage script unless replaced. **A migration obligation.**
- **Carried — the IGRF version stays `TBD — freeze gate`**; I-1 cannot be built until it is frozen under a D-number.
- **Carried — D-1's site-log validation limitation** is open, and I-1's provenance limb turns on it.
- **Carried — BLK-07's authorization limb is open.** No run may touch calendar 2022-12 while it stands.
- **Carried — `RES-01`**: permitted-read access logging is NOT TESTED, owned by stage 3.2, and I-2 performs the permitted read it is about.
- **Carried — Kaggle's durability semantics are unmeasured**, and I-2's before-the-read guarantee depends on them.
- **Carried — FR-P1-02-8's replacement acceptance row** after `TA-29`'s withdrawal.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, authorises writing a module, or claims a gate, acceptance row or test as discharged.
