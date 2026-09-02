# Business Logic Model — `governance-guards`

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

**Unit** `governance-guards` (Bolt 2) · **Kind** `library` · **Depends on** `foundation`

> **Re-established a sixth time 2026-08-24**, on a **new stage attempt**: Inception closed
> and Construction opened at 2026-08-24T11:46:26Z, which resets the receipt floor for every
> unit. **No content of this unit changed.** `foundation`'s amendment pass of the same day
> (`governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md`) was checked against this
> unit and touches nothing it cites: **A** was declined so no count propagated; **B** amended
> `DeterminismRecord`, a `foundation` contract; **C** amended `services.md` § Run record and
> registry and `unit-of-work.md` § 1, while this unit reads § Stage entry contract, § The nine
> stage scripts, § Execution platforms and § 2. The change record's own sweep reaches the same
> conclusion independently. **The READY verdict in § Review belongs to the previous attempt**
> (iteration 2, 2026-08-22); a fresh pass under this attempt follows.

> **Re-established a fifth time 2026-08-23**, after a redo aimed at four stale
> cross-references in `target-standardization`'s question file. **No content of this unit
> changed** — though the correction concerned **this unit's R-20**, which a sibling had been
> attributing to `inventory-and-registry`.

> **Re-established 2026-08-23 after a stage-wide redo jump**, which reset the receipt floor
> for every unit of this stage. **No content of this unit changed at re-establishment.**
> What the jump also does here: it **resets this unit's exhausted adversarial reviewer
> budget**, so the artifacts regenerated against the nine-question set — previously
> disclosed as unreviewed because the 2-iteration budget had been spent on the prior issue —
> receive a fresh pass. See § Review.
>
> **That pass has since run and returned READY** (iteration 2), after a Critical arithmetic
> slip in § W-3a was corrected — the printed proof summed to **15** where it asserted 17.
> **Re-established a second time 2026-08-23** after a further stage-wide redo aimed at
> `external-products`; **no content of this unit changed on that occasion.** **A third
> re-establishment** followed a redo aimed at a misread depth policy in
> `component-methods.md`; **no content changed then either.** **A fourth** followed a sweep
> of two sibling question files; **no content changed then either.**

The workflows this unit implements: the phase-boundary prohibition checked at every
stage entry, the Phase 1 → Phase 2 transition manifest, the single guarded path into
the locked December root, and the §10.1 reuse register.

**No workflow here computes a scientific quantity.** This unit refuses, records and
hashes. The 17 protected items are frozen by **D-24**; this stage does not reopen
them.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 2 — `Owns`, boundary, the 10 requirements, BLK-06, BLK-07, ADR-02 and ADR-03.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2 plus § Per-unit coverage summary; both derivation paths agree. Table 2 also records `RES-01`.
- `../../../inception/requirements-analysis/requirements.md` — REQ-ENG-5; FR-P1-02-6; FR-P1-03-2; FR-P1-05-12; FR-P1-06-1…-4; NFR-PHASE-01; NFR-LIC-01.
- `../../../inception/application-design/component-methods.md` — the approved signatures and raise-contracts.
- `../../../inception/application-design/components.md` and `component-dependency.md` § Shared resources.
- `../../../inception/application-design/services.md` — § Stage entry contract step 4; § The nine stage scripts (the producing-script enumeration in W-2); § Execution platforms (a Kaggle session carries no git working tree).
- `evidence/DECISIONS.md` **D-24** and **D-15**.
- `../../../inception/delivery-planning/bolt-plan.md` § Gate 0 and § Bolt 2 — the `DP-CHAIR-02` ruling, the Definition of Done, and the confidence hypothesis *"that the prohibitions are enforced at run time, not only in tests."*
- `../foundation/functional-design/business-logic-model.md` — W-1's stage entry contract, into which this unit's step 4 fits; R-15 and R-16.
- Workspace inspection, 2026-08-22: `tests/test_phase_boundary.py` (266 lines) and `tests/test_acquisition_window.py`, read directly rather than described from a citation.
- **Workspace inspection, 2026-08-28** *(added under `GOV-2026-08-28-FD-01` Recommendations 2, 37 and 44)*: **all three** modules in `tests/` read directly — `test_acquisition_window.py`, `test_phase_boundary.py` and `test_release_hashes.py`. **The third had not been read before**, and the 2026-08-22 source line above named only two while W-10's rule ranged over the whole tree: that is the gap `VAL-02` found. Also read: `.dst_summary.json` at the repository root, `evidence/locked_test_restricted/` (6 entries), `evidence/locked_test_restricted/loose_artifacts_sha256_manifest.json`, `evidence/audit_ec1_2026-08-15/{kyoto_dst,nrcan_f107,ec1-audit-report.json}`, and `evidence/experiment_registry.md` rows 6–11 and lines 79–83 / 119–130.
- `evidence/DECISIONS.md` **D-17** (the Phase 1 target-row contract and its excluded set, lines 808–813) and **D-16** (zenith weighting not computable on the five-column product, lines 754–761) — read directly 2026-08-28 for Recommendation 37.
- `governance/reviews/GOV-2026-08-28-FD-01.md` — Recommendations **2** (`VAL-02`, BLOCKER, Validation Auditor veto), **37** (`TEC-08`) and **44** (`VAL-08`), with the owner's approved board options.
- `functional-design-questions.md` (**Q1 through Q9**), `domain-entities.md`, `business-rules.md`.

---

## W-1 — Step 4 of the stage entry contract: the import limb

`foundation`'s W-1 fixes the six ordered steps. **Step 4 is this unit's**, and it runs
between preflight and seeding.

```
INPUT   phase: int, loaded_modules: Mapping[str, object]   (normally sys.modules)
OUTPUT  None
RAISES  PhaseBoundaryError naming the offending module
```

1. Return immediately unless `phase == 1`.
2. Intersect `loaded_modules` with `RAW_MODULES` — **four** names:
   `src.gnss.rinex`, `src.gnss.calibration`, `src.gnss.target`,
   `src.gnss.verification`.
3. On any intersection, **refuse to proceed** and raise, naming the module.

**Why it runs here and not only in tests.** A Kaggle session carries no git working
tree, so a commit hook cannot fire there and a local suite run proves nothing about
the environment the governed run actually executes in (ADR-02). The prohibition has
to hold inside the session. This is the **authoritative** limb — see W-2a for its
relationship to the static scan that already exists.

**Skipped only by `02_build_vtec_target.py`**, which is Phase 2 by definition and
asserts `phase == 2` instead.

**Four modules, not two.** FR-P1-03-2's earlier wording listed `rinex` and
`calibration`; `target.py` and `verification.py` are raw-processing adapters added per
finding `IMPL-2`, and `tests/test_phase_boundary.py` already encodes all four.

## W-2 — The produced-field limb

```
INPUT   frame: DataFrame, phase: int
OUTPUT  None
RAISES  PhaseBoundaryError naming the field
```

Rejects a Phase 1 artifact carrying a field in **D-17's excluded set** — **8 enumerated
exclusions**, not §7.0's five classes.

> **Amended 2026-08-28 (`GOV-2026-08-28-FD-01` Recommendation 37, board option 1, owner
> approved).** This limb previously read *"a **DCB, STEC, mapping, satellite or arc** field"* —
> faithful to TE §7.0's five classes and short of the set D-17 froze. Because this is the
> **cross-cutting** check invoked at step 4 of every Phase 1 stage entry, it was the guard that
> runs everywhere while enforcing less than the artifact-local guards it backs up. R-23 carries
> the full derivation, the per-exclusion mapping table and the controls.

**The 8 exclusions**, derived 2026-08-28 by splitting D-17's *"Explicitly NOT in the Phase 1
row, and not substituted"* sentence (`evidence/DECISIONS.md:808–813`) on its semicolons and
printing the result: `valid_satellite_count`; any per-satellite or **per-IPP** quantity;
**zenith angle or zenith weight**; **elevation**; DCB; STEC; mapping function output; arc or
**cycle-slip** statistics. **2** of the 8 name no §7.0 class token at all (zenith, elevation);
counted as distinct quantities, **3** are uncovered by §7.0's five (per-IPP, zenith,
elevation). **D-16** is why the two geometric ones matter: the Phase 1 product is five columns
(`ut1_unix`, `gdlat`, `glon`, `tec`, `dtec`) with *"no elevation, no zenith angle, no satellite
identifier and no per-IPP record"*, so such a field cannot have been measured — only invented,
imported from Phase 2, or mislabelled.

**Matching is by fragment, not exact name**, so `n_sat_valid`, `zen_wt` and `elev_deg` trip
it. `tests/test_phase_boundary.py` already implements exactly this — **13** fragments counted
programmatically 2026-08-28, covering all 8 exclusions — so the amendment aligns the design
with code that was already stronger than it, rather than the reverse.

**Call site (Q7 = D).** Each of the **eight Phase 1 producing stage scripts, before it
writes** — read from `services.md` § The nine stage scripts:
`00_acquire_prepared_vtec`, `01_inventory_and_registry`,
`02_standardize_prepared_target`, `03_verify_processing`,
`04_build_external_products`, `05_build_features_and_splits`, `06_train_and_predict`,
`07_evaluate_and_report`. (`02_build_vtec_target` is Phase 2 by definition and skips
step 4; `run_walking_skeleton` is the orchestrator.) A **completeness test asserts
every Phase 1 producing script calls it before its first write.**

```mermaid
graph TD
  P["Phase 1 producing script"]
  C["assert_no_raw_fields(frame, phase)"]
  W["write artifact"]
  X["PhaseBoundaryError<br/>exit non-zero"]
  T["completeness test:<br/>every producing script calls it"]
  P --> C --> W
  C -.->|forbidden field| X
  T -.->|a script omits the call| FAIL["test fails"]
```

Text fallback: each producing script calls the field check before writing; a
forbidden field raises and exits non-zero; a separate completeness test fails if any
producing script omits the call.

**Why not inside `foundation`'s release API.** That would put a Phase 1 prohibition
inside the release path and invert the dependency — this unit depends on
`foundation`, never the reverse, and the reverse edge would **close a cycle**.

**Why not only at the manifest build.** That detects the breach after every artifact
is written, and possibly after downstream work consumed the contaminated frame. A
guard that fires at the end is a post-mortem.

**Independence is the requirement.** FR-P1-03-2 wants two independent results;
`component-methods.md` states it flatly — *"neither this nor `assert_phase_boundary`
substitutes for the other."* A test asserts that neither limb passing implies the
other.

## W-2a — The existing static scan, and its declared subordinate role

`tests/test_phase_boundary.py` **already exists** — 266 lines, walking `src/` and
`scripts/` with `ast`, skipping explicitly (never passing vacuously) where the subject
does not exist yet. It is kept, with its role declared (Q7 = D):

| Limb | What it is | Standing |
|---|---|---|
| Static `ast` scan over `src/` and `scripts/` | Early warning — fires before anything executes | **Subordinate.** Does not discharge FR-P1-03-2 |
| `assert_phase_boundary` on `sys.modules` at step 4 | Run-time check inside the executing session | **Authoritative** |
| `assert_no_raw_fields` at each producing script | Run-time check on the artifact about to be written | **Authoritative** |

**Why both rather than either.** A static scan of a local checkout constrains nothing
about a Kaggle session, and a dynamic import assembled from a string is invisible to
`ast` — so static alone defeats the bolt-plan's confidence hypothesis. But retiring a
working guard that fires before execution buys nothing, and would move first detection
of a forbidden import from "any test run" to "the run that would have violated the
boundary."

**The subordinate status is recorded where the code lives** (the Q7 rider):
`tests/test_phase_boundary.py`'s own module docstring states that it is the
early-warning limb and does not discharge the run-time requirement. Stating it only in
a design document is exactly where a future maintainer would miss it and read the
scan's presence as sufficient.

## W-3 — Computing a protected-item digest

```
INPUT   parsed value at the item's authorized granularity, the item's canonical
        YAML path and asserted key inventory
OUTPUT  digest: str   (SHA-256)
```

1. **Parse**, then **canonicalise** with the versioned canonicaliser (Q1 = D as
   amended).
2. **Reconcile the item's asserted key inventory against the parsed governed
   region** — a key added, deleted or renamed in the region but not in the inventory
   **fails**.
3. **Check the declared-overlap rule**: undeclared overlap **rejected**; explicit
   parent-section / child-field overlap **permitted where declared and tested**.
4. **Digest** the canonical form.
5. **Record the canonicaliser identifier and version** in the manifest.

**The canonicalisation contract, fixed here rather than left to the implementer.** It
defines mapping-key ordering, sequence-order treatment, scalar typing and
normalization, Unicode and encoding, **duplicate-key rejection**, alias and merge-key
handling, and rejection of unsupported or ambiguous values.

**Required behaviour, both directions.** Comments, whitespace, quote style,
mapping-key order and **workspace relocation** must **not** change a digest —
`foundation` R-16 forbids machine paths in any governed config, so a relocation that
moved a hash would be a defect. A governed **value** change **must** change it.

**Three granularities, not one** (derived from D-24's Hashable-representation
column, printed before being asserted):

| Granularity | Items | Count |
|---|---|---|
| Whole-file config hash | 12 (`configs/seeds.yaml`) | 1 |
| Config-**section** hash | 4, 7, 9, 11, 14, 16 — plus 13 as `Source + config-section hash` | 7 |
| Config-**field** hash | 5, 6 | 2 |

**Item 12 keeps its approved whole-file semantics.** If applying semantic YAML
canonicalisation to the whole-file hash would change D-24's meaning, that is **raised
as a governed amendment**, never assumed by the implementer.

**Why canonical rather than byte-literal.** A byte digest changes on a comment edit, a
key reorder or a whitespace fix — none of which alters a governed value. G-P3C would
then fail on formatting, indistinguishably from a real protected-value change, and a
gate that cries wolf stops being read. Byte-literal also cannot express items 5 and 6
at all, which by itself rules it out.

**Why the canonicaliser is versioned.** Changing *how* you canonicalise changes every
digest, so the canonicaliser is part of the frozen contract rather than an
implementation detail.

> **CORRECTION retained, 2026-08-22 — the first issue said "Eight … items 4, 5, 6, 7,
> 9, 11, 14, 16", and an adversarial review caught it.** Items **5** and **6** are
> typed **`Field hash`** in D-24, a *different* mechanism, and the first issue
> silently folded them into this section-and-inventory procedure. Derived rather than
> counted:
>
> ```
> awk '/^\| # \| Protected item/,/^\*\*Item 17/' evidence/DECISIONS.md \
>   | awk -F'|' 'NF>4 && $2 ~ /[0-9]/ && $5 ~ /Config-section hash/ {print $2}'
>   ->  4 7 9 11 14 16          (6 items)
>
> ... $5 ~ /Field hash/         ->  5 6   (2 items)
> ```
>
> **The review's finding understated the gap, and the wider version is recorded
> here.** D-24 uses **six distinct hashable-representation kinds** across the 17
> items; the first issue defined **one** and assumed it covered eight. The full
> taxonomy is W-3a below.

## W-3a — The six hashable-representation kinds, and which items use each

Derived from D-24's table, all 17 items accounted for.

**Two independent axes, kept separate** — *what* is digested, and *who* computes it.
Conflating them is what let a mechanism go missing twice.

### Axis 1 — the digest kinds this unit computes

| Kind | Items | Computation fixed by this stage |
|---|---|---|
| **Config-section hash** | 4, 7, 9, 11, 14, 16 | W-3: canonicalise the parsed section, reconcile the key inventory, check declared overlap, digest |
| **Field hash** | 5, 6 | W-3b — named field set (literals and patterns), non-empty assertion, same canonicaliser |
| **Parameter hash** | the second half of 15 | W-3c — a **named-parameter** digest, sibling of the field hash. **Not** a config-section hash and **not** a whole-file config hash |
| **Config hash** (whole file) | 12 | Canonicalise the entire parsed file — same canonicaliser, no section scoping and no inventory, because the whole file *is* the scope (`configs/seeds.yaml`). **Approved semantics preserved**; a meaning-changing canonicalisation is raised, not assumed |
| **Source-file content hash** | 1, and the source half of 13, 15, 17 | Digest of the source bytes of every module in scope, with the module set **enumerated rather than globbed at hash time** |

### Axis 2 — the three composites, each with a DIFFERENT second half

D-24 labels them separately, and the labels are not interchangeable:

| Item | D-24's label, verbatim | Source half | Second half | Defined by |
|---|---|---|---|---|
| **13** | `Source + config-section hash` | `src/evaluation/metrics.py` | **config-section** hash | W-3 |
| **15** | `Source + parameter hash` | `src/evaluation/bootstrap.py` | **parameter** hash | **W-3c** |
| **17** | `Source + config hash of every listed method` | each listed method's module | **config hash, per listed method** | ⚠ see § Open below |

Each composite is a digest over the **ordered pair** (source digest, second-half
digest), combined in a **versioned, domain-separated representation** — Q1's owner
amendment 4, which names item 13 specifically and applies by construction to the other
two. Domain separation is what stops a boundary shift between the two halves producing
a colliding pair; a change on either side moves the composite.

### Axis 3 — four items this unit RECORDS rather than computes

| Item | Digest | Produced by |
|---|---|---|
| 2 | Serialized-architecture hash | `models-and-baselines` |
| 3 | Environment hash (TE §13.1) | `foundation` |
| 8 | Fold, embargo and comparison-mask manifest hashes | `features-and-splits` |
| 10 | Selected-value hash from the run record | `models-and-baselines` |

**Why this axis matters.** Four of the 17 protected items are **not this unit's to
compute** — it records a digest another unit produced, which makes the manifest's
integrity partly dependent on three other units. That is a real property of the design,
stated rather than hidden. It introduces **no dependency edge**:
`build_transition_manifest` receives artifact paths as a **parameter**, so this unit
never imports a downstream one and stays a DAG root.

**All 17 items appear exactly once across Axis 1 and Axis 3**, with Axis 2 decomposing
the three composites rather than adding items:

| Category | Items | Count |
|---|---|---|
| Config-section hash | 4, 7, 9, 11, 14, 16 | 6 |
| Field hash | 5, 6 | 2 |
| Config hash (whole file) | 12 | 1 |
| Source-file content hash | 1 | 1 |
| Composites (source + a second half) | 13, 15, 17 | **3** |
| Externally supplied (recorded, not computed) | 2, 3, 8, 10 | 4 |
| **Total** | **1…17, each once** | **17** |

**6 + 2 + 1 + 1 + 3 + 4 = 17.**

> **Corrected 2026-08-23 after the first adversarial pass on this regenerated issue.**
> Superseded text, preserved: *"6 + 2 + 1 + 1 + 1 (config-section, field, config, source,
> and the three composites counted once each) + 4 recorded = 17."* **That sums to 15.** The
> composite term was printed as `1` where the parenthetical itself says *three*. The
> partition it describes was and is correct — verified item by item against D-24's
> Hashable-representation column, and consistent with the equivalent tables in
> `domain-entities.md` § 1 and `business-rules.md` R-18. **Only the printed arithmetic was
> wrong**, directly beneath a heading claiming the taxonomy was derived rather than carried
> from prose. It is now shown as a table whose column sums rather than as a sentence,
> because a sentence is where the previous two miscounts in this same passage also lived.

## W-3b — The field-hash contract (items 5 and 6)

D-24 types items 5 and 6 as **`Field hash`**, scoped to named fields rather than a
section. Same canonicaliser as W-3, narrower scope, plus a per-item assertion D-24
states verbatim.

```
INPUT   parsed config, the item's named field set (literal names and/or patterns)
OUTPUT  digest: str
```

1. Resolve the named field set — **literal names and declared patterns**, expanded
   against the parsed config.
2. **Assert the resolved set is non-empty.** A pattern matching nothing must fail; a
   field hash over zero fields is a digest of nothing that would pass every diff.
3. Canonicalise the resolved `name → value` pairs with the **same canonicaliser** as
   W-3, so the versioning argument carries over unchanged.
4. Digest.
5. Apply the item's own assertion.

| Item | Governing artifact | Field set | D-24's additional assertion, quoted |
|---|---|---|---|
| **5** History window | `configs/experiment.yaml` | the history-window field | *"frozen at 24 h and absent from every grid"* |
| **6** Station encoding | `configs/features.yaml` | `station_onehot_*` plus `station_lat` | *"`station_onehot_*` plus verified `station_lat`"* |

**Item 5's assertion has two limbs and both are checkable here**: the value is the
frozen 24 h, **and** the field appears in **no grid**. The second limb is what stops
the history window being tuned — `project.md` § Forbidden makes a tuned window a
defect.

**Item 5 is also the declared parent/child overlap case.** Item 9 hashes the Grids
section of the same file and item 5 hashes a field governed alongside it; under Q1's
owner amendment 3 that overlap is **permitted because declared and tested**, not
rejected — and the test is what stops a change being hidden in the parent or
ambiguously attributed between the two.

**Item 6's "verified" is deliberately NOT this unit's verification.** This unit hashes
`station_lat`; **whether it is verified is `inventory-and-registry`'s**, whose
`assert_registry_resolved` blocks `station_lat` when the registry is unresolved or a
conflict was averaged. Recorded so the word "verified" in D-24 is not read as an
obligation landing here — this unit's assertion is that the field is **present and
hashed**, not that its value has been validated against the IGS site logs.

## W-3c — The parameter-hash contract (the second half of item 15)

D-24 types item 15 as **`Source + parameter hash`** and names the parameters verbatim:
*"24-hour vector blocks, 10,000 replicates, seed 20221201."* Governing artifacts:
`src/evaluation/bootstrap.py` + `configs/seeds.yaml`.

A **parameter hash** is a sibling of the field hash — a digest over an explicitly
named parameter set, using the **same canonicaliser** — with two differences that
matter:

1. **Its parameters may span more than one governing artifact.** The seed lives in
   `configs/seeds.yaml`; the block width and replicate count are bootstrap parameters.
   A field hash is scoped to one file; a parameter hash is scoped to a **named set
   wherever those names resolve**, and the resolution is recorded.
2. **Every named parameter must resolve, and the resolved set must be complete.** A
   parameter hash over two of three parameters is a digest that passes every diff
   while leaving one unprotected.

**Why this cannot be folded into the config path.** `TC-19` is `binding: hard` on
exactly these values — 24-hour blocks carrying all three stations together, 10,000
replicates, seed 20221201 — and `project.md` § Forbidden bars substituting a
within-station or naive bootstrap. Hashing "whatever is in the seeds file" would not
protect the block construction or the replicate count at all.

> **Corrected 2026-08-22 after the final adversarial pass.** The previous version of
> W-3a listed item 15 under "Composite source + config" with its second half
> *"computed by its own kind above"* — but **no parameter-hash kind existed above**.
> That silently folded a fourth mechanism into a generic bucket, which is the same
> defect class as the original eight-versus-six miscount, on a `TC-19` hard-binding
> item feeding the G-P3C pass condition.

> **What remains PENDING, unchanged.** The *kinds* above are fixed by this stage. The
> **per-item binding to concrete config fields and file paths is still BLK-06's open
> limb** — no config file or `src/` package exists, so item 5's field name, item 6's
> pattern, item 15's parameter names, and every section boundary are named by D-24 but
> not yet resolvable against a real artifact. The per-item boundary table is stated in
> `business-rules.md` R-18 § Per-item boundaries as the binding evidence, and is
> **verified mechanically against D-24 before G-P3C**. **BLK-06 is not closed by this
> stage.**

## Open — item 17's "config hash" label, raised not resolved

D-24 types item 12 as **`Config hash`** (the whole of `configs/seeds.yaml`) and item
17 as **`Source + config hash of every listed method`**. **The same two words carry a
different scope**: item 12's is one whole file; item 17's is *per listed method*
across five enumerated methods (M-01 persistence, M-02 24-hour seasonal persistence,
M-03 station×month×hour climatology, B-01 the IRI-2016 benchmark with its 2000 km
altitude ceiling, C-01 the CODE final GIM comparator).

**Whether item 17's per-method config scope is a whole file, a section, or a named
parameter set is not stated by D-24, and is not invented here.** The label appears to
be inherited from D-24 rather than introduced by this stage, so correcting it would be
an amendment to an approved decision record rather than a design choice. Reusing item
12's whole-file mechanism verbatim would make all five baselines' config-hash
components identical regardless of which one changed, which cannot be the intent.

**Consequence if left open:** item 17 is the one protected item whose second-half
scope a builder would have to guess. **Raised at this stage's approval gate — not
resolved by preference.**

## W-4 — The protected-set mapping, its exclusion, and its own digest

**One structure**: a governed mapping from **protected-item identifier → the canonical
YAML paths that item covers**. Its 17 keys are D-24's identifiers; its values are the
asserted key inventories W-3 reconciles.

**Location** `configs/experiment.yaml`. **The section holding it is EXCLUDED from
every item's section hash, and the exclusion list has exactly one member** (Q3 = D).

```mermaid
graph LR
  S["experiment.yaml<br/>protected-set section<br/>(17 identifiers + inventories)"]
  E["EXCLUDED from every<br/>item's section hash<br/>(exactly 1 member, tested)"]
  D["its OWN canonical digest"]
  M["TransitionManifest<br/>(digest stored HERE)"]
  S --> E
  S --> D --> M
```

Text fallback: the protected-set section is excluded from every item's section hash,
and the exclusion list is tested to have exactly one member; separately, the section
carries its own canonical digest, which is stored in the transition manifest rather
than back inside the section.

**Both limbs of the exclusion test carry the rule.** That the exclusion exists, **and**
that no other section is excluded. An unbounded exclusion mechanism is a hole, not a
resolution: whatever the first exclusion is for, the mechanism granting it can grant a
second one silently.

**The excluded section is not therefore unprotected.** It carries its own digest,
computed by the same canonicaliser and stored externally in the manifest, so a change
to the enumeration or to any per-item inventory still surfaces as a manifest
difference. A change to the protected-set enumeration is a governed change requiring a
Vision §15.2 amendment and a D-number, so surfacing it is the required behaviour.

> ## ⚠ THIS WORKFLOW REVERSES A RECORDED OWNER REFUSAL
>
> The previous question set's Question 3 was answered **B, modified — MODIFY, not
> approval**, and directed that the complete list be hashed and **"must not be
> excluded from hashing merely to avoid circularity. Excluding it would leave the
> enumeration that defines what is protected as the one thing unprotected."** The
> full superseded ruling is preserved verbatim in `business-rules.md` R-19.
>
> The reversal rests on an **explicit decision by the project decision owner**, taken
> 2026-08-23 after the conflict was put to them with the superseded ruling quoted —
> **not on a new argument.** The superseded reasoning is not answered, and the
> external-digest constraint above is the mitigation it demands, stated as mandatory
> rather than optional.

**Mutation contract** — the six behaviours `business-rules.md` R-20 tests: deletion
and addition change the digest and fail the membership assertion; **duplication is
rejected** because D-24's cardinality of 17 is calculated from its enumeration, and
the canonicaliser rejects duplicate keys independently; semantically irrelevant
**reordering leaves the digest unchanged**; renaming changes the digest and fails
membership; and the frozen manifest holds **exactly** the 17-item set.

## W-5 — Building the transition manifest

```
INPUT   snapshot: ConfigSnapshot, artifacts: Mapping[str, Path]
        (mode channel: see the amendment note below — the approved signature carries no mode parameter)
OUTPUT  TransitionManifest
RAISES  ManifestError — a freeze-mode build with an absent item, or a key set != D-24's 17
```

```mermaid
graph TD
  A["1. Resolve each of D-24's 17 items<br/>to its governing artifact"]
  B["2. Hash each present item<br/>(W-3/W-3b/W-3c by kind)"]
  C["3. Absent item -> 'absent' sentinel"]
  M{"build_mode field?"}
  DR["draft: record and return<br/>manifest marked 'draft'"]
  FR["freeze: raise on any 'absent';<br/>assert key set == D-24's 17"]
  A --> B --> C --> M
  M -->|draft| DR
  M -->|freeze| FR
  FR -.->|absent, short, or extra key| X["ManifestError"]
```

Text fallback: resolve all 17 items, hash those present by their kind, mark absent
ones with a sentinel, then branch on the build mode — draft records and returns a
manifest explicitly marked draft; freeze raises on any absent item and asserts the key
set equals D-24's 17 exactly.

**The build mode is a FIELD of `TransitionManifest`**, not a build-time argument, so
it survives serialization and a draft can never be mistaken for a freeze by a later
reader or by `diff_protected_hashes` (Q2 = D's rider).

> **How the builder learns the mode — reconciled 2026-08-25 on adversarial finding 2 of the
> post-reset pass, which was Major.** W-5's INPUT block declared `mode: draft|freeze` as a
> parameter while three statements across the artifacts say the mode is *"not a build-time
> argument"* — and the approved signature (`component-methods.md`:
> `build_transition_manifest(snapshot, *, artifacts)`) **carries no mode parameter at all**, so
> read literally nothing told the builder which mode to build, and inferring it is the
> draft-mistaken-for-freeze hazard Q2's rider exists to close. **Reconciled without changing the
> approved contract by assertion**, following `foundation`'s `write_release` precedent: the
> INPUT block above now matches the approved two-parameter signature, and **an amendment need on
> `build_transition_manifest` — adding a keyword `mode: Literal["draft","freeze"]` — is
> recorded as an OPEN item in § Assumptions for the owner's decision.** Until it is ruled on, the
> mode has no sanctioned channel and stage 3.5 must stop and report rather than invent one
> (TE §18.3). What IS settled: the semantics of each mode (draft records and returns, marked;
> freeze raises on any absent item and asserts D-24's key set), and that the **persisted** mode
> lives in the dataclass field, which is what Q2=D's rider protects.

**The freeze assertion has three limbs**: no missing key, no extra key, **and no
`absent` value**. Without the third, a manifest with 17 keys of which sixteen are
`absent` would satisfy a membership check while protecting almost nothing.

**Why draft mode exists.** All 17 governing artifacts are absent today — no config
file, no `src/` package, no run record. Under a raise-always rule the manifest could
not be built, tested or demonstrated until the final Bolt, and a mechanism first run at
a freeze gate is a mechanism first debugged at a freeze gate. This project's affirmed
posture is that reproducibility is executable, not asserted.

**The membership assertion is what `component-methods.md` already demands** — the key
list is asserted equal to the canonical set *"so a short list cannot pass silently."*

**Also recorded in the manifest**: the canonicaliser identifier and version (W-3), and
the protected-set section's own digest (W-4).

## W-6 — `diff_protected_hashes` and the G-P3C pass condition

```
INPUT   frozen: TransitionManifest, current: TransitionManifest
OUTPUT  Mapping[str, tuple[str, str]]   — differing keys with both values
```

An **empty mapping is the G-P3C pass condition**: no protected item changed.

**Ordering that matters.** The membership assertion runs **before** any diff, so a
manifest missing an item fails rather than producing a reassuring empty diff.

> ## ⚠ AN EMPTY DIFF IS NOT YET PROOF
>
> **BLK-06's enumeration limb is RESOLVED by D-24 at 17 items. Its per-item binding to
> concrete config fields and file paths is PENDING**, and no config file or `src/`
> package exists yet.
>
> Until that binding is discharged **and approved**, an empty diff **must not be read
> as proof that no protected item changed**, and no artifact, manifest or report from
> this unit may state or imply otherwise.
>
> `component-methods.md`'s standing caution is **half-discharged, not retired**. Three
> approved artifacts — `component-methods.md`'s `TransitionManifest` comment,
> `unit-of-work.md` § 2 and `components.md` line 61 — still describe the enumeration as
> deferred to stage 3.1, which D-24 has since resolved. They are **reported at the
> gate, not edited.**

## W-7 — A guarded read of the locked December root

```
INPUT   path: Path, record: AccessRecord, registry: Path
OUTPUT  Path   (only after the log is durable)
RAISES  LockedTestError — path outside RESTRICTED_ROOT, or log write / durability failure
```

```mermaid
graph TD
  A["1. Assert path is under RESTRICTED_ROOT"]
  B["2. Append AccessRecord to the log"]
  C["3. Flush and confirm DURABILITY"]
  D["4. Return the path — read may now begin"]
  X["LockedTestError<br/>READ NEVER BEGINS"]
  A --> B --> C --> D
  A -.->|path outside root| X
  B -.->|write fails| X
  C -.->|durability fails| X
```

Text fallback: assert the path is under the restricted root, append the access record,
flush and confirm durability, and only then return the path. A path outside the root, a
failed write, or a failed durability confirmation all raise and the read never begins.

> **The access-log append must be DURABLY COMPLETED before the December read
> begins.** A log-write failure **or** a durability failure **prevents the read** —
> not reported alongside it, not retried after it, not logged as a warning while the
> read proceeds.

**Step 1 exists to keep the guard honest**: `path` outside `RESTRICTED_ROOT` raises,
because callers must not route ordinary reads through the guard and dilute what a log
row means.

**Why ordering is the requirement.** `VAL-2` and FR-P1-02-3: **an access recorded
after the fact fails the ordering check rather than satisfying it.** An unlogged read
of the locked month cannot be undone once taken.

**Two limbs, two tests, both owned by this unit (Q6 = C).** Patch the log writer to
fail → the read never happens. Assert the row is durable on disk before the read is
attempted — which distinguishes this contract from one that logs and reads in the same
buffered transaction, where a crash loses the row and keeps the read. Neither test
needs `tests/test_locked_test_guard.py`, which ADR-03 assigns to `features-and-splits`
to keep this unit a DAG root.

> ## ⚠ `RES-01` — THE PERMITTED READ IS STILL UNTESTED, AND STAYS OPEN
>
> Story-map Table 2 records `RES-01`: **permitted-read access logging is NOT
> TESTED**, with its candidate §19 criterion owned by **stage 3.2** under Vision
> §15.2. Q6's option D would have closed it here with a positive-path test for the
> permitted pre-G-05 coverage read — against a **synthetic** restricted root, not the
> real audit. That was declined deliberately: the evidence would look like coverage of
> the real audit and would not be. **Raised at this stage's gate as still open, not
> absorbed here.**

**Context.** The log already holds **five retrospective rows** predating this guard
(`evidence/experiment_registry.md` rows 3, 4, 5, 8, 9). Two kinds of row coexist, and
the distinction lives in the register explicitly rather than being inferred from
ordering.

## W-8 — What counts as a December hit

**Rule (Q5 = D).** A hit is a December 2022 **target value**, or a December-derived
**target aggregate** — a count *about* December carrying no target value, such as
`madrigal_coverage_summary.csv`'s `december_days_present` and
`december_coverage_pct`.

**Why the aggregate channel is included.** `project.md` § Forbidden bars December from
informing model selection, feature selection, thresholds or hyperparameters, with the
trigger being December being **seen**, not the lock being opened. A December coverage
figure in an unrestricted summary is December being seen with no access-log row.

**Why December-dated driver captures are excluded, and how the exclusion is bounded.**
The live instance is
`evidence/audit_ec1_2026-08-15/kyoto_dst/dst_provisional_202212.html` — hourly Dst for
December 2022, whose observation date falls in December and which is not a target
value. Dst is diagnostic/hindcast-only and never a confirmatory ML feature, so
sweeping it into locked-test custody would route every ordinary Dst read through
`open_restricted` and buy nothing the lock exists for. The exclusion is a **recorded
list naming the driver classes and why**, with **its membership pinned by test** — and
that is the limb that matters: **a target file mislabelled as a driver is
detectable**, because a reviewer checks an enumerated list rather than an unstated
omission.

**The list is now actually enumerated, at four classes** *(amended 2026-08-28, consequence
of `GOV-2026-08-28-FD-01` Recommendation 44(b))*. As written this workflow **claimed** a
recorded class list while naming **one live instance and no classes**, so the
membership test had nothing to range over. Auditing the scan root for the relocation
surfaced **two further December-bearing driver artifacts already on disk and never
enumerated** — a new observation, named in neither the board's report nor the remediation
brief. Derived and printed 2026-08-28: (1) the **12** raw provisional-Dst monthly captures
under `kyoto_dst/`; (2) `nrcan_f107/fluxtable.txt`, **95** lines dated `202212`, its 2022
range recorded by the EC-1 report as `2022-01-01` → **`2022-12-31`**; (3)
`audit_ec1_2026-08-15/ec1-audit-report.json`, month-keyed `1`…`12` with the `"12"` entry
carrying `expected_days: 31`, `day_rows_parsed: 31`; (4) the derived driver summary
`.dst_summary.json`, **conditional on the Recommendation 44(b) relocation having happened** ⚠ **NOW UNCONDITIONAL (2026-08-28, D-30)** — the relocation has happened, so class 4 applies without condition..
Classes 2 and 3 are a **correction, not a widening**: both sit inside the scan root today,
so a guard built from the previous text would have **failed on first run against evidence
already committed**, and the failure would have read as a breach rather than as an
unenumerated exclusion. R-26 carries the table and the per-class figures.

**The exclusion is a custody exclusion and never a licence to use the excluded file.**
**D-11** bars any provisional-Dst-derived figure from becoming a G-05 regime count, a
modelling input or a frozen tolerance, and that restriction rides classes 1, 3 and 4
wherever they sit. The control closing that channel is **not here**: it is
`regimes-diagnostics-reporting` **R-123**, whose `RegimeError` fires when a
provisional-Dst-derived series is offered as the storm-count input, and which names
`.dst_summary.json` as the path of least resistance it exists to close. *(ID corrected
2026-08-28: the remediation brief and the board's Recommendation 44 both cite "R-122";
grepping both units' rule headings gives `statistical-inference` R-113…R-122 and
`regimes-diagnostics-reporting` opening at **R-123**.)*

**The tension this resolves, stated rather than smoothed over.** FR-P1-02-6's first
sentence says *"Any file containing a December 2022 target value is a locked-test
artifact"*; its criterion says *"a record whose observation date falls in December
2022."* Those two sentences do not pick out the same set, and the driver capture is
the difference. The owner's earlier direction said *"content scan on observation
dates"*, which reads toward the literal criterion; the owner was shown that tension on
2026-08-23 and **confirmed the narrower target-plus-aggregate reading with the bounded
driver exclusion.**

## W-8a — Scanning for December-bearing artifacts outside the restricted root

```
INPUT   evidence_root: Path
OUTPUT  Sequence[Path]   — empty is the pass condition
RAISES  EvidenceScanError — a file no declared parser handles, with no recorded exclusion
```

1. Walk `evidence/` **recursively**.
2. For **every file**, dispatch to the **declared parser for its artifact class** and
   inspect **observation dates** — never the filename or directory name.
3. A file that **cannot be parsed** by any declared parser is a **failure**, not a
   pass, unless it carries an **explicit recorded exclusion**.
4. Apply W-8's hit definition and the driver-exclusion list.
5. Return every December-bearing artifact found outside the restricted root.

**Why record dates and not names.** `project.md` § Forbidden: *"NEVER derive fold or
partition membership from an acquisition directory name or a filename."* That rule
exists because a year-blind predicate filed locked-month records into
`audit_evidence_2022-01/`, where a name-based check cannot see them.

**Why unparseable means failure.** A file the guard cannot read is exactly where a
December record would hide, so treating it as clean is the one answer that cannot be
defended.

**Why recursive by construction.** `DATA-01` showed a narrowed glob *"silently stopped
checking the artifacts that matter most."*

**The scan root is `evidence/`, and that is a stated bound** *(amended 2026-08-28,
`GOV-2026-08-28-FD-01` Recommendation 44(b), board option 2, owner approved)*. `evidence_root`
is called with the repository's `evidence/` directory, so **everything outside it is outside
this guard by construction** — the repository root, `src/`, `scripts/`, `notebooks/`,
`artifacts/`, `configs/` and `tests/`. The guard always did this; what it never did was say so,
which is how a December-bearing file at the repository root stayed invisible to a reader
checking the design. **Recursive** describes depth beneath the root; it never described breadth
across the repository.

**The live instance, and it is NOT a breach.** `.dst_summary.json` sits at the **repository
root**, git-tracked and not gitignored (both verified 2026-08-28), carrying **12** month keys
whose `"12"` entry holds `days_parsed: 31`, `hours: 744`, `min: -68`, `storm50: [7, 27]`,
`storm30` with **15** days and `daily_min` with **31** entries — all derived and printed before
being written here. Its classification is **already correct and reasoned** at
`evidence/experiment_registry.md:119–123`: Dst is a public driver series, not a target value,
and no December *target* record is touched. **D-11** separately bars any provisional-Dst figure
from becoming a G-05 regime count. The gap is mechanical only: the guard cannot reach the file. ⚠ **PERFORMED 2026-08-28 under D-30 — this paragraph describes the state BEFORE the move.** The relocation the board recommended and this design declined to perform was authorised by the project owner on `GOV-2026-08-28-FD-01` Rec 44(b) and executed the same day: `.dst_summary.json` now lives at `evidence/audit_ec1_2026-08-15/kyoto_dst/.dst_summary.json`, **inside R-27s scan root**, verified byte-identical across the move (`sha256 410927a4ff620b6f7597b18e07746f74233cf5aa87bc84d6f5b0ec25b3e9c064`, 5,653 bytes, before and after) on the D-15 method, with **access-log row 12 written BEFORE the read**. Its D-number is **D-30** and its change record is `governance/CHANGE_RECORD_2026-08-28_dst_summary_relocation.md`. **The reasoning above stands unchanged** — the file was never a breach, the gap was mechanical, and relocation rather than a widened scan root was the right fix.

**The fix is relocation, and this workflow does not perform it.** The recorded disposition is
to move `.dst_summary.json` under `evidence/audit_ec1_2026-08-15/kyoto_dst/`, beside the twelve
`dst_provisional_YYYYMM.html` captures it derives from (all twelve verified present
2026-08-28) — inside the existing root **without widening it**. Two consequences, stated:
the move is **custody-adjacent and owes its own D-number and change record** on the D-15
precedent, and **neither exists**; and once inside the root it needs R-26's enumerated driver
exclusion to **name its class**, which is why R-26 now enumerates **four** classes rather than
gesturing at one instance. Widening the root to the whole repository (board option 1) was
declined: the exclusion list would cross `.claude/`, `graphify-out/`, `.git/` and Bolt
worktrees, and is the kind of list that rots. The counter-consideration is recorded rather
than buried — leaving the repository root permanently out of scope (option 3) reproduces the
**`DATA-01`** lesson this very workflow cites against itself, which is precisely why the answer
is to move the file rather than to excuse the region.

**The loose December artifact is now manifested** *(recorded 2026-08-28; Recommendation
44(a), performed by the project decision owner, not by this unit)*.
`evidence/locked_test_restricted/loose_artifacts_sha256_manifest.json` hashes run 2's
preserved raw extract: `sha256 3a164af0864b2effde2e527ca190c1b050f5a47179eaffa3ccab770bb366f557`,
**1,666,816 bytes** — both **independently re-derived 2026-08-28** by recomputing the digest
over the file, and both matching. Access-log **row 11** was written **before** the read, and
the read was **bytes-only for hashing** — no field parsed, no record counted, no value
inspected. That closes the one December artifact with no integrity record at all: it was named
in **neither** restricted `sha256_manifest.json`, so TA-15's mutation-protection test, which
operates on manifested artifacts, had nothing to bind to.

**What the existing green check actually covers, read from the code.**
`tests/test_acquisition_window.py` sets `RAW_RECORDS = "madrigal_coverage_raw_records.csv"`
and its `_record_csvs_at_any_depth()` helper returns `EVIDENCE_DIR.rglob(RAW_RECORDS)`
minus the restricted root — **one filename, not a content class.** Inventory of
`evidence/` by filename shows 16 instances each of `madrigal_coverage_raw_records.csv`,
`madrigal_coverage_summary.csv`, `madrigal_coverage_monthly.csv`,
`sha256_manifest.json` and `request_manifest.json`; only the first is scanned. Scanned
2026-08-22, every non-zero `december_*` value is already under the restricted root — so
**the check is green and the gap is latent rather than currently breached.** A
December-bearing `madrigal_coverage_summary.csv` appearing outside the restricted root
tomorrow would pass.

**No artifact-class registry is frozen by this stage.** Q4's option D would additionally
assert a declared registry covering every filename present under `evidence/`. It was
**declined with a reason**: it front-loads a registry before any of the artifact classes
it enumerates is produced by this pipeline, and the current 16-instance inventory is all
pre-TC-06 evidence. Failure-on-unknown gives the same protection, arriving as a failure
the first time a new class appears. Adding the registry later is not foreclosed.

**Retained after D-15**, which relocated 21 December-bearing files into the restricted
root — this is the regression guard for that move.

> ## ⚠ FR-P1-02-6 IS EXPLICITLY UNTESTED
>
> This workflow's requirement has **no §16 or §19 acceptance row** — this unit's one
> untested requirement of ten, derived from story-map Table 1 and cross-checked against
> § Per-unit coverage summary. It **is** enforced today, by
> `tests/test_acquisition_window.py::test_locked_month_values_exist_only_under_the_restricted_path`,
> and that test **is** green: lacking an acceptance row is a different thing from
> lacking a test.
>
> On the project decision owner's explicit direction it is preserved as an **explicitly
> untested obligation until an approved acceptance row exists AND its test has
> passed** — both conditions. Everything above is a **test specification only — not an
> approved acceptance row and not evidence of a passing result.** Designing the guard
> does not test it; implementing it does not test it.

## W-9 — Registering reused third-party source

1. **Default: do not copy.** Reimplement the published method from the paper with a
   citation. `project.md` § Forbidden prohibits copying source whose licence is absent,
   ambiguous or incompatible, and that is the rule in force while the AGPLv3 question
   is open. Copying is deliberately harder to reach than reimplementation, because that
   is the policy actually in force.
2. If copying or material adaptation is nonetheless approved, record **all fifteen
   §10.1 fields** **before the code is used** and before **G-P2**.
3. The adapter module carries a mandatory **provenance marker**.
4. The register is **asserted complete** against the set of marked modules; an unmarked
   module is asserted to contain **no reuse**.

**Why the marker.** Without it an unregistered copy is indistinguishable from original
work by inspection, and the completeness assertion has nothing to range over.

**The open governance dependency, stated not resolved.** The AGPLv3
Global-TEC-forecasting repository is the only approved direct-copy source today, and
**whether its repository-distribution obligations permit that copying is a dependency
this project does not settle.**

## W-10 — One path in, and who may use it

**Mechanism (Q9 = D, as narrowed 2026-08-28).** A **static check asserts that no module
outside `locked_test.py` and outside an enumerated `tests/` exemption contains the
restricted-root literal**, and that the exemption list's membership is **exactly** the ~~four~~
⛔ **five** modules named *(corrected 2026-08-31 on owner approval to annotate in place; superseded
figure preserved. `RESTRICTED_LITERAL_EXEMPT_MODULES` carries **five** members in addition to the
chokepoint — equivalently **six** counting `locked_test.py`, the convention R-28's box uses. The
fifth is `scripts/merge_coverage_year.py`, a **production script, not a test**, which is why
membership is an exact enumerated list and never a `tests/` directory predicate. This site and
three others were missed by the 2026-08-29 repair because that repair swept only the five sites
its finding enumerated — the failure `project.md` records as `fd-2026-08-30-sweep-derive-sites`)*.
This generalises `foundation`'s R-15 — the same grep-class assertion, applied
across the whole tree, now with one bounded carve-out.

> ## ⚠ AMENDED 2026-08-28 — THE ONE-DOOR MECHANISM NOW HAS A BOUNDED `tests/` EXEMPTION
>
> `GOV-2026-08-28-FD-01` **Recommendation 2** — the board's **BLOCKER**, `VAL-02`, on which
> the **Validation Auditor exercised its veto**. **Board option 1**, approved by the project
> decision owner. Stated as a **narrowing in the open**: **more than one module holds the
> literal, and this workflow's pass condition was false against the workspace it had already
> read.** Verified on disk 2026-08-28 — `tests/test_acquisition_window.py:46`,
> `tests/test_phase_boundary.py:49` and `tests/test_release_hashes.py:49` each define
> `RESTRICTED_DIR = EVIDENCE_DIR / "locked_test_restricted"`, so with the future
> `locked_test.py` that is **four** holders, and the design's own negative control was
> satisfied by the tree as it stands. **Board option 3** — scoping the check to `src/` only —
> was rejected by name: it *"is what will be chosen by default if nothing is decided"* and it
> converts the largest known hole into a **permanent blind spot**, a hazard
> `evidence/experiment_registry.md:79–83` records as having already fired in fact.

**Why the boundary is still absolute where it counts.** **D-15** records the restricted root
as a **governance boundary, not an access control** — it holds only while exactly one code
path reaches it. That sentence is retained verbatim, and its scope is now **stated rather than
inferred: a "path" is a route through which restricted CONTENT is read.** D-15's boundary
*"does not weaken slightly; it ends"*, and the exemption is built so nothing about that
changes — an exempt module may **name** the root, but any read of content beneath it goes
through `open_restricted` or against a synthetic fixture root. **Holding a string is not an
access; reading bytes is.**

**The exemption, ~~four~~ ⛔ five modules, membership asserted exactly** *(corrected 2026-08-31,
same sweep as the mechanism sentence above; five members in addition to the chokepoint, six
counting it)* — the same enumerated-list
technique R-26 uses for the driver exclusion, and it fails in the direction that matters: an
unlisted module holding the literal fails the static check, and a listed module that no longer
needs it fails the membership test until the list is edited. Full table with per-module
justification and line references is in `business-rules.md` R-28; the routes in one line each:

1. `tests/test_locked_test_guard.py` — **synthetic fixture root only**, never the real root.
   Importing the root from `locked_test.py` (board option 2) is **circular** — the module under
   test would supply the constant the test checks — and an imported constant still yields a
   readable path with no `AccessRecord`, so the custody gain is cosmetic. **This answers a
   question `features-and-splits` R-82 left open**: R-82 assigns the module there *"because it
   exercises both limbs"* and never says how it reaches the root without the literal.
   Ownership does not move; only the route is fixed, and this unit stays a **DAG root** because
   an exemption-list entry is a name in a static check, not a dependency edge.
2. `tests/test_acquisition_window.py` — `_observed_dates()` (`:117–122`) opens and
   `DictReader`-parses a month's raw-records CSV, and `_month_dirs()` (`:81`) supplies month
   directories from the restricted root via `EVIDENCE_ROOTS` (`:50`): a **content read** owing
   a pre-read access row. The custody helper at `:195` filters restricted paths out **by
   ancestry** and reads nothing beneath the root.
3. `tests/test_phase_boundary.py` — `_phase1_artifacts()` (`:133–137`) rglobs across both
   roots and the field test reads each artifact's **CSV header**: a content read owing a
   pre-read row. `:259–261` asserts the collector reaches inside the root — *"a custody
   boundary is not a checking exemption"* — and itself reads no content.
4. `tests/test_release_hashes.py` — `_declared_artifacts()` (`:84–91`) `read_text`s each
   manifest and the hash test **streams `_sha256()`** over each declared artifact beneath the
   root: content and byte reads owing pre-read rows, on the precedent of access-log rows 6 and
   11 that a bytes-only hash read is logged first and inspects no value.

**An exempt module that reads content still owes a pre-read access row.** The exemption
composes with the already-registered **RES-04** obligation and does not displace it: exemption
from the *literal* check is not exemption from W-7's ordering contract. The `AccessRecord` must
be **durably appended before the read begins**, exactly as for any other caller.

> ## ⚠ A LIVE CONSEQUENCE NEEDING AN OWNER RULING — STATED, NOT RESOLVED
>
> Modules 2, 3 and 4 **read December content beneath the restricted root today, on every suite
> run, with no access row**, because `open_restricted` does not exist (**G-09 unsigned**) and
> there is nothing to route through. That is the RES-04 hazard in present tense; this
> amendment **surfaces** it rather than creating it. **Nothing here authorises those reads,
> retro-labels them, or writes a row for them.** Two dispositions exist and this design
> **chooses neither** — (i) route the three modules' restricted-root content reads to
> **synthetic fixture roots**, or (ii) keep them against the real root with a standing
> obligation that each is owed an access row from the moment `open_restricted` exists, the
> interim disclosed in the G-05 and G-06 evidence packages beside the five retrospective rows
> W-7 already names. Option (i) matches module 1's route and is cheaper to make true; option
> (ii) preserves the three modules' present value as checks against **real** evidence, which
> is what makes them worth exempting at all. **Raised at this stage's gate.**

**Why not a caller allow-list inside the guard.** Q9's option C would have
`open_restricted` raise when its caller is not one of the four recorded consumers. That
closes the run-time-path-assembly gap but couples this root unit to four downstream
units, and the reverse edge would **close the cycle** the DAG was arranged to avoid.
The residual gap — a path assembled at run time from fragments — is left open
deliberately: the static check plus review makes it unlikely, and the acyclic structure
is worth more.

> ## ⚠ BLK-07 IS OPEN, AND IS A PRECONDITION OF BOLT 3
>
> Four units reach the root through this contract: `inventory-and-registry` (pre-G-05
> coverage audit), `acquisition` (the D-9 input and any December re-acquisition — the
> unrecorded routing that **is** BLK-07), `features-and-splits` (locked partition),
> `evaluation-and-comparison` (locked evaluation).
>
> **The static check has a live consequence, stated now rather than discovered later:**
> `acquisition` **cannot hold its own path** to `audit_evidence_2022-FULL/` once the
> check exists, because D-15 relocated that artifact under the restricted root.
> **BLK-07's resolution is a precondition of Bolt 3, not a formality.**
>
> **Acceptance of this mechanism is NOT authorization to open locked December data.**
> The static check enforces **how many** paths exist, never **who** may use one. Which
> units are authorised to reach the locked month is a decision the **project decision
> owner receives and approves**, and nothing here grants, implies or substitutes for
> it. **No acquisition run may touch calendar 2022-12 while BLK-07 stands.**

## W-11 — What Bolt 2 builds, and what it must not

**Permitted before G-09**, per `bolt-plan.md` § Gate 0: module structure, interfaces,
placeholder CLI definitions, configuration wiring, safe fail-fast behaviour, and the
`tests/` scaffolding for this unit.

**Barred until G-09 is signed for the affected component**: implementing any component
whose P0 decision is unresolved; filling any `TBD — freeze gate` field; executing any
governed run; generating code for a unit carrying an open blocker on that scope.

> **`src/data/phase_contract.py`, `src/data/locked_test.py` and
> `src/data/reuse_registry.py` DO NOT EXIST.** BLK-01 closed 2026-08-22 under
> `CR-2026-08-22-TE-AMEND` granting **authority only**. Authority to name a module is
> not authority to write one; creation stays gated by **G-09**, TE §18.3's
> stop-and-report rule, and stage **3.5**.

**No December access of any kind occurs in this Bolt.** The guard is designed here; it
is not exercised against the locked month.

---

## Requirement-to-workflow map

Acceptance derived from story-map Table 1; owners from Table 2's `primary` cell. Both
paths cross-checked and in agreement.

| Requirement | Workflow | Tested by (Table 1) | Row primary owner |
|---|---|---|---|
| REQ-ENG-5 | W-1, W-2, W-2a, W-5 | WS-10, TA-07, TA-08, TA-12, TA-27 | `features-and-splits` ×3; `models-and-baselines`; **`governance-guards`** |
| **FR-P1-02-6** | W-8, W-8a | ⚠ **NO CURRENT ACCEPTANCE ROW** | — |
| FR-P1-03-2 | W-1, W-2, W-2a | TA-27 | `governance-guards` |
| FR-P1-05-12 | W-7 | WS-18, TA-18 | `features-and-splits` |
| FR-P1-06-1 | W-4, W-5 | TA-27 | `governance-guards` |
| FR-P1-06-2 | W-5 | TA-27 | `governance-guards` |
| FR-P1-06-3 | W-5, W-6 | TA-28 | `governance-guards` |
| FR-P1-06-4 | W-5, W-6 | TA-28 | `governance-guards` |
| NFR-PHASE-01 | W-1, W-2, W-2a, W-5 | TA-27 | `governance-guards` |
| NFR-LIC-01 | W-9 | TA-28 | `governance-guards` |

**10 requirements, 1 without an acceptance row.** **Owns** TA-27 and TA-28;
**supports** TA-07, TA-18 and WS-18. Three relations, three sets, each derived.

## Assumptions & Open Questions

- **OPEN — which disposition the three existing exempt test modules take** *(added 2026-08-28 under Recommendation 2)*: options (i) synthetic fixture roots or (ii) real-root reads with a standing access-row obligation, set out in W-10's boxed live consequence. **No option is chosen here.** Until ruled on, the three modules continue to read December content beneath the restricted root with no access row, and 3.5 must stop and report rather than pick a route (TE §18.3).
- ~~**OPEN — the `.dst_summary.json` relocation is authorised in disposition but not performed**~~ *(added 2026-08-28 under Recommendation 44(b))*: the move to `evidence/audit_ec1_2026-08-15/kyoto_dst/` owes a **D-number and a change record** on the D-15 precedent, and neither exists. **This workflow does not perform the move.** Until it happens the file is outside W-8a's scan root, and driver-exclusion class 4 is conditional on the move. ⚠ **CLOSED 2026-08-28 — the relocation is PERFORMED.** The project owner authorised it on `GOV-2026-08-28-FD-01` Rec 44(b); it is recorded as **D-30** with change record `governance/CHANGE_RECORD_2026-08-28_dst_summary_relocation.md`, and executed the same day: the file is now at `evidence/audit_ec1_2026-08-15/kyoto_dst/.dst_summary.json`, byte-identical across the move (`sha256 410927a4ff620b6f7597b18e07746f74233cf5aa87bc84d6f5b0ec25b3e9c064`, 5,653 bytes), with **access-log row 12 written BEFORE the read**. The file is inside the scan root and **driver-exclusion class 4 is now unconditional**. The two things this item said were missing — the D-number and the change record — both exist.
- **[assumption]** The exemption list is **exactly five** modules *(corrected 2026-08-29 on adversarial finding 1, Critical; superseded figure preserved: "**exactly four** modules". `business-rules.md` R-28's box states the same set as **six**, counting the chokepoint `src/data/locked_test.py`; this list counts members **in addition to** it.)* — `test_locked_test_guard.py`, the three `tests/` modules holding the literal today, **and `scripts/merge_coverage_year.py`**, the production script the 2026-08-28 full-repository sweep found holding the literal and reading six restricted sites with no `AccessRecord`. The three existing test modules are **retained** rather than refactored, because all three are green, all three are in `team.md`'s mandated 17-module set, and TC-06 directs pre-TC-06 evidence to be **re-verified under the new suite rather than re-acquired**, which is what those three perform. The fifth member makes the exemption **no longer `tests/`-only** and membership an **exact enumerated list, never a directory predicate**. If the owner prefers refactoring any out, the list shrinks with the membership test.
- **[assumption]** W-10's exemption is a **narrowing of D-15's framing**, not a relocation of D-15's requirement: "exactly one path" is read as governing routes through which restricted **content** is read. If the owner reads D-15 as governing the **literal** itself, board option 2 is the only remaining route and its circularity must be accepted with it.
- **[assumption]** R-23's produced-field enumeration is **D-17's**, not TE §7.0's. §7.0 names five classes; D-17 enumerates eight exclusions and is the frozen authority, so the cross-cutting guard is designed to the wider frozen set and cites both. No scientific value is created by the widening.
- **OPEN — an amendment need on `build_transition_manifest`** *(added 2026-08-25 on adversarial finding 2 of the post-reset pass)*: the approved signature carries no mode parameter, three artifact statements correctly say the mode is not a build-time argument, yet the builder must be told which mode to build. The reconciliation (W-5) records an amendment need — a keyword `mode: Literal["draft","freeze"]` — for the owner, following `foundation`'s `write_release` precedent. Until ruled on, 3.5 must stop and report rather than invent the channel (TE §18.3).
- **[assumption]** Rule IDs continue `foundation`'s sequence, so `business-rules.md` opens at **R-18**. If per-unit numbering was intended, say so at the gate.
- **[assumption]** `tests/test_locked_test_guard.py` is not this unit's — ADR-03 splits the guard, and `features-and-splits` owns the test covering both limbs to keep this unit a DAG root.
- **[assumption]** `RAW_MODULES` names four `gnss` modules — `rinex`, `calibration`, `target`, `verification`.
- **[assumption]** NFR-PHASE-01's transition-manifest hash-diff test has no §12 module and needs frozen artifacts from every later unit; carried on `fixtures-and-reproducibility` with this unit supporting.
- **[assumption]** TA-27's second limb (Phase 2 cannot change protected forecasting hashes) is accepted at G-P2 and G-P3C, outside Phase 1.
- **[assumption]** `frontend-components.md` is not produced — `kind: library`, mapped to `[ui]` only.
- **[assumption]** `build_mode` is fixed as a `TransitionManifest` field. Whether `canonicaliser_version` is a new field or an entry in an existing mapping is a stage 3.5 shaping decision, so **no approved dataclass contract is otherwise changed.**
- **Open — W-4 reverses a recorded owner refusal on the owner's explicit decision**, not on a new argument. The superseded ruling is preserved verbatim in `business-rules.md` R-19, and the external-digest constraint is the mitigation its reasoning demands. Raised at the gate.
- **Open — where the D-24 conformance test gets its list.** It must assert against the **authority**, not only the config, or config and manifest can agree while both drift. Hardcoding is a fourth copy of a governed enumeration; parsing `evidence/DECISIONS.md` makes a governance prose document a test dependency, which Q3 option C was rejected for. **No third option invented.** Raised at the gate.
- **Open — BLK-06's per-item binding.** Enumeration resolved by D-24 at 17; binding **PENDING**. W-6 states the consequence; `business-rules.md` R-18 § Per-item boundaries is the binding evidence, verified mechanically against D-24 before G-P3C.
- **Open — BLK-07 authorization**, a precondition of Bolt 3. See W-10.
- **Open — `RES-01`**, permitted-read access logging is NOT TESTED. See W-7.
- **Open — item 17's per-method "config hash" scope.** See § Open above.
- **Open — a stale statement in three approved artifacts, reported not edited.** `component-methods.md`, `unit-of-work.md` § 2 and `components.md` line 61 all still describe the enumeration as deferred to stage 3.1, which D-24 resolved at 17 items; `bolt-plan.md` § Bolt 2 already reflects the resolution. Per `CHANGE_RECORD_PROCEDURE.md` a sweep reports on approved-stage artifacts and does not edit them absent owner approval for annotate-in-place.
- **Open — the AGPLv3 distribution question.** Unresolved; reimplementation with a citation is the standing default.
- **G-09 is not signed.** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged. No workflow here authorises creating any module.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

---

> ## Re-saved 2026-08-28 — remediation of `GOV-2026-08-28-FD-01`, verdict FAIL
>
> The project decision owner ruled on `governance/reviews/GOV-2026-08-28-FD-01.md` (verdict
> **FAIL**) and authorised three remediations touching this unit. A redo jump cleared the
> write-freeze. **Every `## Review` section below is preserved unchanged, and every READY
> verdict they record PREDATES these edits and does not cover them.**
>
> | Item | Workflow | What changed |
> |---|---|---|
> | **Recommendation 2** (BLOCKER, `VAL-02`, Validation Auditor **veto**) — board option 1 | **W-10** | The one-door mechanism now carries a bounded, **enumerated `tests/` exemption of 4 modules**, each with a declared route for content reads, stated as a **narrowing** of D-15's framing. `test_locked_test_guard.py`'s route answers the question `features-and-splits` R-82 left open. The live RES-04 consequence and its two dispositions are raised at the gate, unchosen |
> | **Recommendation 37** (`TEC-08`) — board option 1 | **W-2** | The produced-field limb now rejects **D-17's 8 enumerated exclusions** instead of §7.0's **5** classes, citing D-17 as authority alongside §7.0 |
> | **Recommendation 44(b)** (`VAL-08`) — board option 2 · and **44(a)** as recorded input | **W-8a**, **W-8** | Scan root **stated explicitly** as `evidence/`; the `.dst_summary.json` **relocation** recorded as the fix with the move **not performed here**; the 44(a) loose-artifact manifest cited with its hash independently re-derived. W-8's driver exclusion **enumerated at 4 classes** |
>
> **Counts derived and printed before assertion, per `project.md` § Way of Working.**
> Workflows unchanged at **16** (W-1…W-11 including W-2a, W-3a, W-3b, W-3c, W-8a). Requirements
> unchanged at **10**, **1** without an acceptance row, **2** rows owned (TA-27, TA-28), so the
> § Requirement-to-workflow map needed no change. D-17: **8** exclusions, **2** naming no §7.0
> token, **3** distinct quantities uncovered by §7.0's five. `test_phase_boundary.py`'s existing
> fragment set: **13**, covering all 8. Exemption list: **4** modules, **3** on disk.
> Driver-exclusion classes: **4**. `.dst_summary.json`: **12** month keys, December
> `storm30` **15** days, `daily_min` **31** entries. Loose extract: **1,666,816** bytes,
> hash re-derived and matching.
>
> **What this re-save does NOT do.** **BLK-06 remains open** — the protected-key list's
> derivation from TE §7.0B is untouched. **G-09 remains unsigned**, and no workflow here
> authorises creating any module. No scientific constant is decided, no supervisor-owned value
> is read into, no acceptance row is created, and no `## Review` verdict is claimed for the
> amended text. The three documentation-class findings riding the terminal READY remain **gate
> input**, unchanged and unapplied.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-22T22:01:04Z
**Iteration:** 2 (final)

### Disposition of iteration-1 findings

| # | Finding | Disposition | How verified |
|---|---|---|---|
| 1 | § W-3a's printed arithmetic `6+2+1+1+1(...)+4=17` summed to 15, not 17 (composite term printed as 1 where the parenthetical said "three"). | **RESOLVED.** The sentence was replaced with a table (lines 262–271) whose rows are Config-section hash (4,7,9,11,14,16 = 6), Field hash (5,6 = 2), Config hash whole-file (12 = 1), Source-file content hash (1 = 1), Composites (13,15,17 = **3**), Externally supplied (2,3,8,10 = 4), Total = 17, followed by the explicit sum `6 + 2 + 1 + 1 + 3 + 4 = 17`, which is arithmetically correct. | Re-derived the item lists independently against `evidence/DECISIONS.md` D-24's Hashable-representation column via `awk` (same pattern the artifact itself uses): Config-section → `4 7 9 11 14 16`; Field hash → `5 6`; Config hash → `12`; Source-file content → `1`; the three `Source + ...` composites → `13 15 17`; the four items D-24 assigns to another unit's producing path → `2 3 8 10`. Union of all six lists is exactly `{1..17}` with no duplicate and no gap — every item in the new table matches D-24 item-for-item. Summed the table column by hand: 6+2+1+1+3+4=17. |

### New findings (this iteration)

None survived verification.

### Failed refutation attempts

- **Re-verified the reconciled sum is not merely locally consistent but matches D-24 directly**, rather than trusting the artifact's own restated categories. Pulled D-24's table fresh with `awk '/^\| # \| Protected item/,/^\*\*Item 17/' evidence/DECISIONS.md` and hand-classified all 17 rows by their "Hashable representation" column. Result matches the artifact's table exactly, including the four "recorded, not computed" items (2, 3, 8, 10) whose producing units — `models-and-baselines`, `foundation`, `features-and-splits`, `models-and-baselines` — match Axis 3's table in § W-3a and domain-entities.md line 137.
- **Attempted to find a defect introduced by the correction one level down** (the project's documented repeat failure mode: a correction pass introducing a fresh error). Compared the new W-3a category table against: (a) W-3's own three-granularity table (lines 170–174, a *different*, narrower axis — config-only granularities, 10 items, not all 17 — and confirmed it is not meant to sum to 17, so it is not a competing claim); (b) `domain-entities.md` § 1's seven-row kind table (lines 129–137, which additionally splits out "Parameter hash" as its own row rather than folding it under composites, but its item lists — 4,7,9,11,14,16 / 5,6 / 12 / 1 / 15's second half / 13,15,17 / 2,3,8,10 — are all consistent with W-3a's, just partitioned one level finer); (c) `business-rules.md` R-18's three-granularity table (lines 57–61, matching W-3's granularity table verbatim: whole-file=1, config-section=7 including 13, config-field=2) and its § Per-item boundaries table (lines 179–197, all 17 rows present, each item's granularity label agreeing with W-3a). No inconsistency found across any of the four tables in the three artifacts.
- **Checked the correction box for dishonesty** (quietly replacing rather than preserving the superseded text, or overstating the defect). The box (lines 273–282) quotes the superseded sentence character-for-character (`git show` not needed — the current text plus the iteration-1 finding's own quotation of it are identical), states plainly "That sums to 15," attributes the error precisely ("The composite term was printed as 1 where the parenthetical itself says three"), and explicitly affirms "The partition it describes was and is correct" — matching iteration 1's own conclusion that only the arithmetic, not the classification, was wrong. Found no overstatement and no quiet edit.
- **Re-attempted the R-19/R-19a reversal attack from iteration 1** (unchanged this pass) — re-read § W-4's boxed note (lines 422–434) and `business-rules.md` R-19; the verbatim-preservation and explicit-owner-decision structure iteration 1 verified is unchanged, and no new text was introduced that weakens the disclosure. Not a defect.
- **Checked whether the new table's own three internal sub-groupings (Axis 1 computed kinds, Axis 2 composite second-halves, Axis 3 externally-supplied) still add up given the table replaced only the Axis-3-adjacent summary**, not Axis 1 or Axis 2 above it. Re-summed Axis 1 (6+2+"the second half of 15"+1+"1, and the source half of 13/15/17" — a computation-axis, not an item-count axis, so it does not double as a 17-item partition and does not conflict with the corrected summary table beneath it) and Axis 2 (13, 15, 17 — three composites, each independently defined) against the corrected summary table: consistent, no new arithmetic claim introduced that could itself be wrong.

### Summary

The single Critical finding from iteration 1 — a printed sum of 15 where 17 was claimed — is resolved: the offending sentence was replaced with a table whose six rows reconcile exactly against `evidence/DECISIONS.md` D-24's Hashable-representation column (verified independently by this reviewer, not merely re-read from the artifact's own derivation), sum correctly to 17, and cover all seventeen items exactly once with no duplicate and no gap. The correction box preserves the superseded sentence verbatim, states the actual defect (an arithmetic slip, not a classification error) without overstatement, and its claim of consistency with `domain-entities.md` § 1 and `business-rules.md` R-18 / § Per-item boundaries holds under independent re-derivation of all three. No fresh defect was introduced by the correction itself, which the project's own history flagged as the likelier failure mode on a second pass. Nothing else raised in iteration 1 was reopened, since it was already disposed as sound. This unit is READY.

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

> **Re-saved 2026-08-25 under the receipt recorded after ten stage-wide redo floors** (all taken for
> `foundation`, which closed with a terminal **READY**). **Nothing in this unit's workflows
> changed**; the unit's figures were re-derived from `unit-of-work.md` § 2 — **10** requirements
> (**1** untested: FR-P1-02-6), **2** acceptance rows (TA-27, TA-28) — and all four files checked
> clean of the Amendment C contamination classes. The one edit this pass makes is in the sibling
> artifacts: the four exceptions this unit raises are declared **`IntegrityError` subclasses,
> imported from `src/data/config.py`**, discharging the cross-unit obligation `foundation`'s R-01
> records. **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

## Review — 2026-08-25 post-reset pass, iteration 1

**Reviewer:** aidlc-architecture-reviewer-agent

**Verdict: NOT-READY**

**Class:** adversarial · **Iteration:** 1 of 2 · **Date:** 2026-08-25

Two spec-affecting defects survived verification, one of them inside today's only content
change. Every count below was derived from the artifacts and printed before being asserted;
the derivations are shown whether they refuted the artifact or confirmed it.

### Findings, most severe first

#### 1 — Major, **would mislead stage 3.5**. The base-class declaration says "four" over a five-row table, and the one exception it omits is the December-scan guard's

`domain-entities.md` § 8's new box (line 355) states: *"**All four exceptions
below derive from `IntegrityError`, imported from `src/data/config.py`**"*. Derived from the
rows the box heads:

```
awk 'NR>=364 && NR<=368' domain-entities.md | grep -c "^|"      ->  5
names in those rows: PhaseBoundaryError, LockedTestError, ReuseError,
                     ManifestError, EvidenceScanError
names enumerated in the box: PhaseBoundaryError, LockedTestError, ReuseError, ManifestError
set difference (rows \ box):  { EvidenceScanError }
```

The same "four" is asserted in five places: `domain-entities.md:355` and `:449`,
`business-rules.md:377` and `:742`, `business-logic-model.md:868`. `business-rules.md:375`
raises it to a universal claim — *"**Base class of every exception this unit raises**"* — over
the same four names, and that claim is false as written: `business-logic-model.md:640` reads
`RAISES  EvidenceScanError — a file no declared parser handles, with no recorded exclusion`,
in **W-8a, a workflow this unit owns**. The count is **five**, not four.

**Why it is a specification defect and not a blemish.** The box's own stated rationale is that
an exception outside the hierarchy exits with **no `aborted` registry row**, *"the one event
NFR-PHASE-01 and NFR-AUD-01 most require recorded"*. That rationale applies verbatim to
`EvidenceScanError`: R-27's fail-closed limb (*"an unparseable artifact is a FAILURE"*) is the
limb most likely to fire on real evidence, and `foundation`'s R-10 writes the `aborted` row by
catching `IntegrityError`. A builder who follows the box's enumeration literally leaves the
December-scan failure uncaught — the exact defect the R-01 correction exists to prevent, in the
unit that owns the guard.

**Mitigating, and why this is Major rather than Critical.** The section heading
(`## 8. `IntegrityError` subclasses raised here`), its intro (*"Deriving from `foundation`'s
base (unit 1, R-01)"*) and its closing line (*"for any of them — including a subclass added
later"*) all range over the full five rows. So 3.5 meets a contradiction inside one section
rather than a silent omission, and the likelier failure is a builder stopping to ask.

**Related, recorded rather than raised separately.** The receipt the human answered
(`functional-design-questions.md:706-710`) approved *"one addition ... stating that
`PhaseBoundaryError` and `LockedTestError` **derive from `IntegrityError`**"* — two exceptions.
The applied edit covers four. The expansion is sound on the authority of R-01's *"any future
integrity-related exception"* clause (verified against `foundation/business-rules.md:80`), and
`ReuseError`/`ManifestError` are correctly **not** claimed to be among the fourteen. The point
is the asymmetry: the edit ranged past its receipt in one direction and still stopped one
exception short of consistency.

**Should be:** five, with `EvidenceScanError` named beside `ReuseError` and `ManifestError`
under the same clause, and `business-rules.md:375`'s universal claim covering it.

#### 2 — Major, **would mislead stage 3.5**. `build_transition_manifest`'s build mode is specified as an input and as "not an input" in the same artifact set

`business-logic-model.md:470` declares:

```
INPUT   snapshot: ConfigSnapshot, artifacts: Mapping[str, Path], mode: draft|freeze
```

Three statements contradict that third input directly:

- `business-logic-model.md:494` — *"**The build mode is a FIELD of `TransitionManifest`**, not a build-time argument"*
- `domain-entities.md:191` — *"**`build_mode` (`draft` | `freeze`) is a FIELD of `TransitionManifest`**, not a build-time argument"*
- `business-rules.md:330` — *"The **build mode** (`draft` | `freeze`) is a **field of `TransitionManifest` itself**, not a build-time argument"*

The approved signature carries no such parameter — `component-methods.md:219-223`:
`build_transition_manifest(snapshot, *, artifacts: Mapping[str, Path]) -> TransitionManifest`.
Q2's answered rider is the source of the "field" wording (*"the draft/freeze flag be a field of
`TransitionManifest` itself rather than a build-time argument, so it survives serialization"*,
`functional-design-questions.md`, Q2 recommendation, `[Answer]: D`).

**Why 3.5 cannot proceed without inventing something.** Read literally, the three "not a
build-time argument" statements leave **no channel by which the builder learns which mode to
build** — and W-5's own mermaid node reads `M{"build_mode field?"}`, branching on a field the
function has not yet been given a value for. 3.5 must either (a) add a parameter to an approved
signature, which the artifacts nowhere disclose as a change, or (b) infer the mode — and an
inferred mode is precisely the draft-mistaken-for-freeze hazard Q2's rider exists to close.
The disclosure discipline this unit applies elsewhere makes the omission sharper:
`domain-entities.md` § 2 is titled *"approved contract, **one field added**"* and the assumption
line states *"no approved dataclass contract is otherwise changed by this stage"* — the added
**field** is disclosed prominently, the added **parameter** not at all.

**Should be:** state that the mode is *supplied to the builder and recorded as a serialized
field* (the only reading under which both Q2's rider and W-5's input list hold), and disclose
the signature change to `build_transition_manifest` the way the dataclass field addition is
disclosed.

#### 3 — Minor, **documentation defect a human reads at the gate**. The new box breaks the exception table's rendering

Verified with `cat -A` on `domain-entities.md:350-368`: the header `| Exception | Raised when |`
and delimiter `|---|---|` are followed by a **blank line**, then the box, then another blank
line, then the five body rows. Under GFM a table ends at the blank line, so a gate reader sees
an empty two-column table, a note, and then five lines of literal pipe-delimited text. The
table's data does not render as a table at the one moment it is read for approval.

**Should be:** the box placed above the header, or the five rows returned to immediately after
the delimiter.

#### 4 — Minor, **documentation defect**. `tests/test_reuse_registry.py` — owned by this unit, evidence for one of its two acceptance rows — is never named

Derived: `grep -c "test_reuse_registry"` → `business-logic-model.md:0`,
`business-rules.md:0`, `domain-entities.md:0`. The module is in this unit's `Owns` list
(`unit-of-work.md:158`) and is TA-28's evidence artifact (`unit-of-work-story-map.md:211`:
*"`tests/test_reuse_registry.py`, §10.1 register rows"*), and TA-28 is one of this unit's two
acceptance rows. R-29 states four negative controls for the register but places none of them in
a module, while its sibling `tests/test_phase_boundary.py` is named, line-counted and
role-declared throughout. Low build risk — §12 and `team.md`'s `test_<subject>.py` convention fix
the name — but the asymmetry is a gap the gate reader has no way to see is deliberate.

**Should be:** name the module where R-29's negative controls are placed, as W-2a does for the
phase-boundary scan.

### Derivations that confirmed the artifacts (refutation attempts that failed)

- **The three headline figures — 10 requirements, 1 untested, 2 acceptance rows — hold, checked
  by set difference rather than by totals** (`project.md` § Way of Working, learned 2026-08-22).
  Requirement IDs extracted from `unit-of-work.md:162`, from `domain-entities.md` § Requirement
  coverage, and from `business-logic-model.md` § Requirement-to-workflow map, then `comm -3`
  pairwise: **empty in both directions on both comparisons**. The shared set is
  `FR-P1-02-6, FR-P1-03-2, FR-P1-05-12, FR-P1-06-1…4, NFR-LIC-01, NFR-PHASE-01, REQ-ENG-5`
  (10). Untested = 1, `FR-P1-02-6`, matching `unit-of-work.md:164` (*"1 of 10 here"*) and
  `unit-of-work-story-map.md:259` (*"`governance-guards` (1): FR-P1-02-6"*). Acceptance rows =
  2, TA-27 and TA-28, matching `unit-of-work.md:166` and story-map line 229
  (`| governance-guards | 10 | 1 | TA-27, TA-28 | WS-18, TA-07, TA-18 |`).
- **The base-class declaration is legal and correctly attributed, apart from finding 1.**
  `foundation/business-rules.md:80-85` reads *"**All fourteen project-defined exceptions derive
  from `IntegrityError`**, and so does any future integrity-related exception"*, names
  `PhaseBoundaryError` and `LockedTestError` as `governance-guards`', and places the base in
  **`src/data/config.py`** (line 90) — every particular the box asserts. The import direction is
  legal twice over: this unit depends on `foundation`, and both sit inside `src/data/`.
  `ReuseError` and `ManifestError` are correctly treated under the "any future" clause and
  correctly **not** claimed to be among the fourteen.
- **D-24's taxonomy re-derived from the authority, not from the artifact.** Ran the item→kind
  extraction over `evidence/DECISIONS.md` D-24 independently: config-section `4 7 9 11 14 16`
  (6); field hash `5 6` (2); config hash `12` (1); source-file content `1` (1); `Source + …`
  composites `13 15 17` (3); externally supplied `2 3 8 10` (4). Union = `{1..17}`, no gap, no
  duplicate; `6+2+1+1+3+4 = 17`. Matches W-3a's summary table, `domain-entities.md` § 1's
  seven-row table and `business-rules.md` R-18 § Per-item boundaries, item for item. The
  iteration-2 correction of 2026-08-23 (the printed sum of 15) remains correctly resolved.
- **Every workspace-inspection claim checked against the workspace.**
  `wc -l tests/test_phase_boundary.py` → **266**, as claimed. All four `src/gnss` names are in
  that file (lines 55-58). `evidence/experiment_registry.md:39` reads *"Rows 3, 4, 5, 8 and 9
  are retrospective"* — the artifacts' "five retrospective rows, rows 3, 4, 5, 8 and 9" is
  exact. The 16-instance inventory verified by `find`: 16 each of
  `madrigal_coverage_raw_records.csv`, `madrigal_coverage_summary.csv`,
  `madrigal_coverage_monthly.csv`, `sha256_manifest.json`, `request_manifest.json`. D-15's 21
  relocated files confirmed (`DECISIONS.md:662`, `:1453`).
  `evidence/audit_ec1_2026-08-15/kyoto_dst/dst_provisional_202212.html` exists, as W-8 states.
- **The eight Phase 1 producing scripts are the right eight.** `services.md:46-54` lists nine
  scripts; removing `02_build_vtec_target.py` (Phase 2 by definition) leaves exactly the eight
  W-2 and R-24 name, in order. Step 4 of the stage entry contract is
  `assert_phase_boundary(phase, loaded_modules=sys.modules)` (`services.md:152`), skipped only
  by `02_build_vtec_target.py` (`:161-163`) — as the artifacts state.
- **Attacked the IRI import boundary as an undisclosed support gap, and the attack failed.**
  Story map line 286 names `governance-guards` supporting TA-07 with the annotation *"independent
  import-limb check"*, and the three artifacts mention `iri` **zero** times (`grep -n` → no
  hits), which looked like an unplaced obligation of the same class as the hash-diff test.
  `component-dependency.md:197` settles it: *"This design places the assertion in `features.build`
  and the check in `test_iri_denial.py`, and does not invent a module to own it"* — the check is
  placed, in a module `features-and-splits` owns. R-23's acceptance line (*"contributes to WS-10,
  TA-07, TA-08, TA-12 through REQ-ENG-5 (all owned by other units)"*) is the correct
  representation. Not a defect.
- **BLK-06 and BLK-07 are honestly represented.** `unit-of-work.md:168` carries BLK-06 as this
  unit's only open blocker and mentions BLK-07 only as a cross-reference to `acquisition`'s;
  the artifacts state exactly that split, disclose BLK-06's enumeration limb as resolved by D-24
  and its per-item binding as PENDING, and refuse to read an empty diff as proof — matching
  story-map line 322's *"Enumeration limbs RESOLVED … implementation limb OPEN"* verbatim in
  substance. BLK-07 is disclosed as open, owned elsewhere, and a precondition of Bolt 3, with
  the live `audit_evidence_2022-FULL/` consequence stated rather than discovered later.
- **No hard rule is breached and nothing is decided that this stage may not decide.** The Phase 1
  prohibition is specified without being exercised — `RAW_MODULES` is a frozenset of names, not
  an import. `grep -c TBD` → 1 across the three artifacts, and that one occurrence is W-11's
  *prohibition* on filling a `TBD — freeze gate` field. The governed values quoted (24 h, 10,000
  replicates, seed 20221201, the 17-item set) are all pre-frozen by D-24 and TC-19 and are quoted,
  never chosen. G-09 is stated unsigned in all three files, and no module is authorised.

### Implementability

The unit is close but not buildable as written. Its shapes, workflows and rules are specified at
a depth stage 3.5 can execute — the two phase-boundary limbs with their declared authoritative /
subordinate roles, the six digest kinds bound item-for-item to D-24, the log-then-read ordering
with durability as a precondition rather than a preference, the bounded driver exclusion, the
fifteen-field register with its provenance marker, and the single-chokepoint static check — and
every open item (BLK-06's per-item binding, BLK-07's authorization, `RES-01`, item 17's scope,
R-20's list source) is disclosed as open with no default quietly adopted. What blocks READY is
two points where 3.5 would have to choose for itself: the base class of `EvidenceScanError`,
left outside a declaration whose entire purpose is to prevent an uncaught integrity error from
exiting without an `aborted` row, and the build mode of `build_transition_manifest`, specified
as an input in one artifact and as "not an input" in three. Both are single-location fixes that
change no rule, no entity, no count and no governed value; findings 3 and 4 are cosmetic beside
them and can ride the same edit.

---

## Remediation of the post-reset iteration-1 findings

*(Written under the same receipt; the § Review above stands unaltered.)*

**All four findings fixed.** (1) The base-class declaration now covers **all five** exceptions this
unit raises — `EvidenceScanError`, R-27's fail-closed December-scan limb, had been omitted from the
very box whose rationale is that an unenumerated exception exits with no `aborted` row; the box now
says "the table below" rather than repeating a numeral. (2) **The mode channel is reconciled**: W-5's
INPUT block matches the approved two-parameter signature, and an **amendment need on
`build_transition_manifest`** (keyword `mode: Literal["draft","freeze"]`) is recorded as an OPEN
item in all three § Assumptions, following `foundation`'s `write_release` precedent — until ruled
on, 3.5 stops and reports rather than inventing the channel. (3) The box no longer splits the
exception table's header from its rows. (4) **`tests/test_reuse_registry.py`** is named as TA-28's
evidence at R-29. Figures unchanged: 10 requirements, 1 untested, 2 acceptance rows.
**G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

## Review — 2026-08-25 post-reset pass, iteration 2 (terminal)

**Reviewer:** aidlc-architecture-reviewer-agent

**Verdict: READY**

**Class:** adversarial · **Iteration:** 2 of 2 (terminal) · **Date:** 2026-08-25

All four iteration-1 findings are fixed and sound at their normative sites, verified mechanically
rather than read from the remediation note. Three residual defects survived refutation; **all three
are documentation-class** — none would cause stage 3.5 to build the wrong thing, and none reopens a
rule, an entity, a count or a governed value. They ride this verdict as **gate input, not as edits**
(`project.md` § Corrections, `units-generation:c4`). Every count below was derived and printed
before being asserted.

### Verification of the four fixes

| Fix | Site | Verdict | Derivation |
|---|---|---|---|
| **1** — five-exception base class | `domain-entities.md:350-358` (box) · `business-rules.md:375-381` (R-23) | **Sound at both normative sites** | `grep -oh "[A-Za-z]*Error"` over all four unit files → `IntegrityError` 24, `PhaseBoundaryError` 16, `EvidenceScanError` 16, `LockedTestError` 14, `ManifestError` 12, `ReuseError` 10, `PartitionError` 3. The five-name set is complete: `PartitionError`'s three hits are all inside the 2026-08-24 re-save note quoting `models-and-baselines`' R-96 residual (`business-logic-model.md:876`, `business-rules.md:744`, `domain-entities.md:454`) — **no sixth exception exists anywhere in the artifact set.** Every `RAISES`/`Raises` clause resolves to one of the five (`business-logic-model.md:68, 95, 473, 564, 657`; `business-rules.md:387, 390, 471`). Attribution re-checked against `foundation/business-rules.md:80-90`: fourteen project-defined subclasses, of which `PhaseBoundaryError` and `LockedTestError` are named as `governance-guards`'; `ReuseError`, `ManifestError`, `EvidenceScanError` are correctly **not** claimed among them and correctly placed under R-01's *"any future integrity-related exception"* clause; base in `src/data/config.py`, as asserted. |
| **2** — mode reconciliation | `business-logic-model.md:470-514` · three § Assumptions | **Sound** | `component-methods.md:219-223` is `build_transition_manifest(snapshot, *, artifacts: Mapping[str, Path]) -> TransitionManifest` — two parameters, and W-5's INPUT block now carries exactly those two. Parity checked by hashing the OPEN item line in each file: `md5sum` → `92415266a0cd08bafaeb5962d6188872` in **all three**, byte-identical. OPEN-item counts per § Assumptions: business-logic-model **9**, business-rules **9**, domain-entities **9**. The cited precedent is real and exactly analogous — `foundation/business-rules.md:940` carries *"OPEN — an amendment need on `write_release`'s approved raise-contract … the owner's decision, not a settled contract"*, added the same day for the same class of change. The reconciliation escalates rather than invents, and states the TE §18.3 stop-and-report consequence. |
| **3** — table rendering | `domain-entities.md:368-379` | **Sound** | `cat -A` on the region: blockquote closes, one blank line, then `\| Exception \| Raised when \|`, `\|---\|---\|` and **five** body rows with no interleaved blank line. Extended to a global check — an `awk` pass over all three artifacts for a delimiter row not preceded by a header or not followed by a body row returned **zero** hits, so the fix introduced no rendering defect elsewhere. |
| **4** — evidence module named | `business-rules.md:669-671` (R-29) | **Substance sound; one collateral defect** — see finding 1 | `grep -n test_reuse_registry` → present at `business-rules.md:669` and `:671`, absent before. Confirmed as TA-28's evidence at `unit-of-work-story-map.md:211` and in this unit's `Owns` at `unit-of-work.md:158`. |

### Findings, most severe first

#### 1 — Minor, **documentation defect introduced by fix 4**. R-29's new evidence sentence cites `R-30`, a rule that does not exist

```
grep -c "^## R-" business-rules.md            -> 12
headings present: R-18 R-19 R-20 R-21 R-22 R-23 R-24 R-25 R-26 R-27 R-28 R-29
grep -n "R-30" *.md  -> business-rules.md:671   (one hit, in fix 4's own added sentence)
```

`business-rules.md:671` reads *"this rule and R-30 are proven by **`tests/test_reuse_registry.py`**"*.
The unit's rules run R-18 → R-29; there is no R-30 anywhere in the four files, and the token appears
exactly once — inside the text the fix added. A builder is told the module discharges a second
obligation it cannot resolve.

**Why Minor rather than spec-affecting.** Nothing is lost from what gets built: R-29 states its three
negative controls explicitly (marked module with no register entry → fails; entry missing any of the
fifteen fields → fails; unmarked module with a recognisable upstream fragment → fails the no-reuse
assertion) and now names the module that carries them. *(Recorded in passing: iteration 1's own
finding 4 said R-29 states "four negative controls"; the rule states **three** — the artifact was
right and the finding's count was wrong, which is the likeliest origin of a reference to a rule that
was never written.)*

**Should be:** drop `and R-30`, or name the rule actually intended.

#### 2 — Minor, **documentation defect: fix 1 corrected two of its five named sites' numeral but not their enumeration**

Iteration 1 named five sites asserting "four". Two still misstate the set:

- `domain-entities.md:460` — the numeral **was** corrected in place to *"**all five** exceptions this unit raises … derive from `IntegrityError`"*, but the enumeration that immediately follows still accounts for only four: *"`PhaseBoundaryError` and `LockedTestError` as two of the fourteen …, `ReuseError` and `ManifestError` as unit-local exceptions under R-01's 'any future integrity-related exception' clause."* `EvidenceScanError` appears in that sentence **only inside the parenthetical naming it as the omission**, never placed under the clause that authorises it. Stated total five, categorised four.
- `business-logic-model.md:886` — still reads *"the **four** exceptions this unit raises are declared `IntegrityError` subclasses"*. This one is a prior section (unmodifiable under this pass's contract) and is explicitly superseded by the appended remediation paragraph in the same file, so it is the weaker half of the finding.

This is precisely the class `project.md` § Corrections names — *"sweep every REPRESENTATION of a corrected fact, not every instance of the entity that carries it"* (`units-generation:re-1`) and *"sweep for the … status claims an amended figure supported, not only for the superseded numeral"* (`delivery-planning:c22`). Here the numeral was swept and the claim it supported was not.

**Why Minor.** Both **normative** sites are complete and correct — § 8's box over the five-row table, and R-23's *"Base class of every exception this unit raises"* now naming `EvidenceScanError` explicitly. 3.5 reading either gets five; only the change-log notes disagree, and one of them contradicts itself visibly rather than asserting a wrong default.

**Should be:** at `domain-entities.md:460`, name `EvidenceScanError` beside `ReuseError` and `ManifestError` under the "any future" clause.

#### 3 — Minor, **documentation defect: fix 1's stated rationale does not hold for the one exception the fix added**

The box's rationale (`domain-entities.md:366-368`) is that *"the stage-entry contract writes the
`aborted` registry row by catching `IntegrityError` — outside the hierarchy, a violation exits with
no `aborted` row."* Derived against the contract it invokes:

```
services.md § Stage entry contract, steps 1-6:  ensure_process_determinism, load_configs,
  assert_no_tbd/assert_declared_sources_exist, assert_phase_boundary, seed_everything, open run record
grep -n "assert_no_december_outside_restricted" -> component-methods.md:291 (signature only);
  business-rules.md:557, domain-entities.md:70 (this unit) — NO declared call site in any artifact
```

`assert_no_december_outside_restricted` is **not** one of the six stage-entry steps, and no artifact
names where it is invoked — unlike every other workflow in this unit (W-1 is step 4; W-2 names its
eight producing scripts; W-7 runs at every restricted read; W-5/W-6 build and diff the manifest).
`foundation`'s R-10 scopes the honest-abort constraint to *"failure in steps 1–5"*. So
`EvidenceScanError` does not reach the `aborted`-row path by virtue of its base class, and the
sentence offered as the reason for enumerating it is inapplicable to it.

**Why this is not a specification defect, having tested that reading.** The **inclusion is correct on
the correct authority** — the box cites R-01's *"any future integrity-related exception"* clause for
exactly these three unit-local exceptions, and that clause, not the aborted-row argument, is what
carries them. And the guard's shape is settled by the approved signature: `component-methods.md:291`
returns `Sequence[Path]` (an empty sequence is R-27's pass condition), which is a reporting contract
rather than a stage-entry assertion, and R-27's negative controls are all plant-and-detect. 3.5 is not
left choosing between two opposite-signed placements as I first suspected. What survives is the
narrower point: the rationale over-generalises from `PhaseBoundaryError` (step 4, where it is exactly
true) to a member for which it is not.

**Should be:** attach the aborted-row rationale to the exceptions raised inside steps 1–5 and rest
`EvidenceScanError`'s membership on R-01's clause alone, which already carries it.

### Refutation attempts that failed

- **Counts, checked by set difference and not by totals** (`project.md` § Way of Working, learned
  2026-08-22). Requirement IDs extracted from `unit-of-work.md:162`, from
  `business-logic-model.md` § Requirement-to-workflow map and from `domain-entities.md`
  § Requirement coverage, then `comm -3` pairwise: **10 / 10 / 10, and empty in both directions on
  both comparisons.** Shared set `FR-P1-02-6, FR-P1-03-2, FR-P1-05-12, FR-P1-06-1…4, NFR-LIC-01,
  NFR-PHASE-01, REQ-ENG-5`. Untested = **1** (`FR-P1-02-6`), matching `unit-of-work.md:164` and
  `unit-of-work-story-map.md:259`. Acceptance rows = **2** (TA-27, TA-28), matching
  `unit-of-work.md:166` and story-map line 229. Per-requirement acceptance cells also match the
  story map row for row (lines 42, 71, 73, 108, 117–120, 136, 138) — not only the totals.
- **Attacked fix 2 as an invented channel, and the attack failed.** Neither the reconciliation nor
  the OPEN item adopts the amendment: both record it as an amendment **need** for the owner and state
  that 3.5 stops and reports until it is ruled on. That is the same disposition `foundation` took for
  `write_release` and `verify_release` (`foundation/business-rules.md:940-941`), so the precedent is
  cited accurately rather than as cover. W-5's mermaid still branches on `build_mode`, which is
  correct under the reconciliation's persisted-versus-supplied distinction — the persisted mode is the
  dataclass field Q2=D's rider protects; the supply channel is the open item. Not a defect.
- **Attacked fix 2 for leaving the three "not a build-time argument" statements unqualified**
  (`business-logic-model.md:495`, `domain-entities.md:190-191`, `business-rules.md:331`). Each file
  carries the byte-identical OPEN item naming W-5 as the reconciliation, so the distinction is
  reachable from every file that makes the claim. Thin, but not a gap I can call a defect.
- **Attacked the "no numeral repeated" claim.** The § 8 box does state a numeral once (*"All FIVE
  exceptions in the table below"*); its own sentence claims only that it does not repeat one
  *elsewhere*, and it does not. The numeral is anchored directly above the five rows that prove it.
  Not a defect.
- **Hard rules re-checked, none breached.** `grep -n TBD` over the three artifacts → **1** hit,
  `business-logic-model.md:781`, which is W-11's *prohibition* on filling a `TBD — freeze gate`
  field. `G-09` stated unsigned in all three files (7 / 3 / 4 mentions). The Phase 1 prohibition is
  specified without being exercised — `RAW_MODULES` is a static frozenset of four names
  (`domain-entities.md:54, 220`) and `grep "import src.gnss\|from src.gnss"` → **zero** hits. IRI
  boundary intact: the only IRI mention is item 17's enumerated B-01 IRI-2016 **benchmark**
  (`business-logic-model.md:397`), an evaluation-time comparator whose config is hashed, not
  imported, and this unit lives in `src/data/` — the `src/features`/`src/models` import ban is not
  engaged. No scientific constant is decided: the values quoted (24 h, 10,000 replicates, seed
  20221201, the 17-item set) are all pre-frozen by D-24 and TC-19 and are quoted, never chosen.
- **Re-derived D-24's taxonomy from the authority rather than from the artifact**, since the
  corrected sum lives one edit away from this pass's changes: config-section `4 7 9 11 14 16` (6);
  field hash `5 6` (2); config hash `12` (1); source-file content `1` (1); `Source + …` composites
  `13 15 17` (3); externally supplied `2 3 8 10` (4). Union `{1..17}`, no gap, no duplicate,
  `6+2+1+1+3+4 = 17`. W-3a's table, `domain-entities.md` § 1 and `business-rules.md` R-18
  § Per-item boundaries all still agree item for item. Unchanged by this pass's edits.
- **Checked whether fix 1 creates a new cross-unit obligation on `foundation`.** It does not:
  R-01's *"and so does any future integrity-related exception"* already admits the three unit-local
  exceptions without amending the fourteen-name enumeration, and the box claims membership in the
  fourteen only for the two `foundation` actually names. No amendment to `foundation` is implied.
- **Checked the acceptance-gap table for drift after fix 4's edit.** § Rules with no acceptance row
  still carries exactly R-26 and R-27 against **FR-P1-02-6**, with the distinction that two rules
  implement one untested *requirement* stated explicitly. Consistent with W-8a's box and with
  R-27's box, which both refuse to let designing or implementing the guard read as testing it.

### Implementability

The unit is buildable as written, and the two Majors that blocked iteration 1 are genuinely closed
rather than papered over: the exception hierarchy now names all five exceptions at both normative
sites, so the December-scan failure cannot fall outside the catchable base by following the
specification; and the mode channel is no longer specified as an input and a non-input at once —
W-5's INPUT block matches the approved two-parameter signature, and the missing supply channel is
escalated as an amendment need in three byte-identical OPEN items with an explicit TE §18.3
stop-and-report instruction, which is the disposition this project's own `foundation` precedent
establishes for changing an approved contract. Everything a builder needs at this depth is fixed
item-for-item: the two phase-boundary limbs with their authoritative/subordinate standing, the six
digest kinds bound to D-24 with the parameter hash and the whole-file hash kept distinct, the
log-then-read ordering with durability as a precondition, the bounded driver exclusion pinned by
test, the fifteen-field register with its provenance marker and now its evidence module, and the
single-chokepoint static check — while every genuinely open point (BLK-06's per-item binding,
BLK-07's authorization, `RES-01`, item 17's per-method scope, R-20's list source, and now the mode
channel) is disclosed as open with no default quietly adopted. The three surviving findings are a
dangling reference to a rule that was never written, a change-log note that states five and lists
four, and a rationale sentence that is true of one exception and offered for five; none changes a
rule, an entity, a count or a governed value, and all three are single-location edits a builder
would not be stopped by. **G-09 remains unsigned, so nothing here authorises creating a module.**

---

> **Re-saved unchanged 2026-08-25 under the second receipt** — the eleventh redo, taken for
> `acquisition`, reset every unit's floor. **No content of this unit changed**; these are the bytes
> the terminal READY pass reviewed, its three documentation-class findings still disclosed as gate
> input. One narrow confirming review follows. **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

## Review — 2026-08-25 second-receipt confirming pass

**Reviewer:** aidlc-architecture-reviewer-agent

**Verdict: READY**

**Class:** adversarial · **Scope:** NARROW change-verification · **Date:** 2026-08-25

The claim under review — *these three `produces[]` artifacts are unchanged in substance since the
terminal READY, apart from one dated re-save box per file* — **holds**. Every headline verification
of the terminal pass re-derives to the same value, four of them by reproducing that pass's own
printed figures exactly rather than by re-reasoning them. The three disclosed documentation-class
findings are untouched and still ride as gate input; they are not re-litigated here. **G-09 remains
unsigned.**

### A — Byte-level proof that the pre-READY body is intact

The terminal pass printed several censuses before it appended its own section. Re-running each over
the same cut — `business-logic-model.md` 1–1114, `business-rules.md` 1–770, `domain-entities.md`
1–475, `functional-design-questions.md` 1–723 — reproduces its numbers **exactly**, which no edit
above those lines could survive.

| Census | Terminal pass asserted | Re-derived now | Match |
|---|---|---|---|
| `grep -oh "[A-Za-z]*Error"`, all four files | `IntegrityError` 24 · `PhaseBoundaryError` 16 · `EvidenceScanError` 16 · `LockedTestError` 14 · `ManifestError` 12 · `ReuseError` 10 · `PartitionError` 3 | 24 · 16 · 16 · 14 · 12 · 10 · 3 | **exact, all seven** |
| `G-09` mentions per file | 7 / 3 / 4 | 7 / 3 / 4 | **exact** |
| `grep -n TBD`, three artifacts | 1 hit, `business-logic-model.md:781`, W-11's *prohibition* | 1 hit, line **781** | **exact, anchor unmoved** |
| mode-channel OPEN item, `md5sum` | `92415266a0cd08bafaeb5962d6188872` in all three | `92415266a0cd08bafaeb5962d6188872` at `business-logic-model.md:818`, `business-rules.md:716`, `domain-entities.md:425` | **exact, and byte-identical across the three** |

Cited line anchors also still resolve, which insertion above them would have shifted:
`business-rules.md:373` (R-23), `:669` and `:671` (`tests/test_reuse_registry.py`),
`domain-entities.md:349` (base-class box), `:460` ("all five"). The one bare `Error` token in the
full-file census is at `business-logic-model.md:1134` — inside the terminal pass's own quoted
`grep` command, not an eighth exception.

**Negative check, deliberately run:** a *silent fix* of a disclosed finding would itself be a
substantive post-READY change. None occurred. `R-30` still appears exactly once outside the review
prose, at `business-rules.md:671`; `domain-entities.md:460` still states five and enumerates four;
the aborted-row rationale at `domain-entities.md:366-368` is unamended. All three findings stand as
gate input, as intended.

### B — Headline verifications, re-derived independently

**Requirements — 10 / untested 1 / acceptance rows 2.** Reconciled by set-differencing ID lists, not
by comparing totals (`project.md` § Way of Working, learned 2026-08-22). Three sources extracted and
`comm -3` pairwise:

```
unit-of-work.md:162                                   -> 10 IDs
business-logic-model.md § Requirement-to-workflow map  -> 10 IDs
domain-entities.md § Requirement coverage              -> 10 IDs
comm -3 (uow, map)  -> empty both directions
comm -3 (map, dom)  -> empty both directions
set = FR-P1-02-6 FR-P1-03-2 FR-P1-05-12 FR-P1-06-1 FR-P1-06-2
      FR-P1-06-3 FR-P1-06-4 NFR-LIC-01 NFR-PHASE-01 REQ-ENG-5
```

Untested = **1**, `FR-P1-02-6`, bold at `unit-of-work.md:164` (*"1 of 10 here"*) and carrying
⚠ **NO CURRENT ACCEPTANCE ROW** in both in-unit tables. Acceptance rows = **2**, TA-27 and TA-28,
matching `unit-of-work.md:166` and the roll-up sentence beneath each of the two in-unit tables.

**Five-exception base-class declaration — sound at both normative sites.**
`domain-entities.md:349-357` states *"All FIVE exceptions in the table below derive from
`IntegrityError`, imported from `src/data/config.py`"* and names `PhaseBoundaryError`,
`LockedTestError`, `ReuseError`, `ManifestError` **and** `EvidenceScanError`;
`business-rules.md:373-381` (R-23) enumerates the same five. The census in § A proves no sixth
exception exists — `PartitionError`'s hits are confined to re-save notes quoting
`models-and-baselines`' R-96 residual, a cross-unit quotation rather than a raise-contract here.

**Exception table renders contiguously.** `cat -A` over `domain-entities.md:366-380`: the blockquote
closes at 370, one blank line at 371, header `| Exception | Raised when |` at 372, the delimiter row
at 373, then **five** body rows at 374–378 with no interleaved blank line and no stray `^M`.
Extended globally — an `awk` pass over all three artifacts for a delimiter row not preceded by a
header or not followed by a body row returned **zero** hits.

**D-24's 17 protected items — re-derived from the authority, not from the artifact.** Read off
`evidence/DECISIONS.md` § D-24's Hashable-representation column directly:

| Kind | Items | Count |
|---|---|---|
| Config-section hash | 4, 7, 9, 11, 14, 16 | 6 |
| Field hash | 5, 6 | 2 |
| Config hash (whole file) | 12 | 1 |
| Source-file content hash | 1 | 1 |
| Composites (`Source + …`) | 13, 15, 17 | 3 |
| Externally supplied | 2, 3, 8, 10 | 4 |
| **Total** | **union {1…17}, no gap, no duplicate** | **17** |

`6 + 2 + 1 + 1 + 3 + 4 = 17`, and D-24 itself states *"cardinality 17, calculated from the
enumeration"*. W-3a's three tables agree with this item for item. Unchanged by the re-save.

**Rule numbering.** `grep -c "^## R-"` → **12**; headings run R-18 → R-29 with no gap and no R-30
heading — the premise of disclosed finding 1, confirmed rather than reopened.

### C — The post-READY additions, and whether they assert anything false

Exactly **one** new dated box per artifact, each the file's final content and each three lines:
`business-logic-model.md` 1285–1288 of 1288 · `business-rules.md` 771–773 of 773 ·
`domain-entities.md` 476–478 of 478. The older stacked re-save notes in `business-rules.md` and
`domain-entities.md` all fall inside the § A baseline cut, so they predate the terminal READY and are
not additions of this receipt. `functional-design-questions.md` gained a re-confirmation block at
724–742 with a filled `[Answer]: Looks correct`.

Each assertion tested:

- *"No content of this unit changed since the terminal READY"* — **true**, on the four exact census
  reproductions and four unmoved anchors in § A.
- *"G-09 remains unsigned"* — **true**. Vision §13.1 records G-09 as `Open, before any affected
  component is coded`; `evidence/DECISIONS.md:1207` and `:1463` both state implementation stays gated
  by G-09; no signature record exists anywhere in `evidence/` or `governance/`.
- *"its three documentation-class findings still disclosed as gate input"* — **true**, per the
  negative check in § A.
- *"the eleventh redo, taken for `acquisition`, reset every unit's floor"* — the redo event is real
  and its cited timestamp is exact: `STAGE_JUMPED`, Direction `REDO`, source and target
  `functional-design`, **2026-08-25T17:21:15Z**, matching the Q&A block's citation to the second.
  Recorded honestly: the audit shard carries **no per-unit attribution field**, so *"taken for
  `acquisition`"* is corroborated (only `acquisition`'s construction files are modified in the
  working tree) rather than provable from the log, and the ordinal *"eleventh"* is orchestrator
  bookkeeping the shard does not number. Neither is a design claim about this unit, neither is
  contradicted by anything on disk, and neither changes what stage 3.5 would build — so this is a
  scope note, **not a finding**.
- *"One narrow confirming review follows"* — this section.

### D — Refutation attempts that failed

- **Tried to read the exception-token deltas as drift.** The full-file census now reads 28 / 23 / 20
  / 17 / 16 / 14 / 5 against the terminal pass's 24 / 16 / 16 / 14 / 12 / 10 / 3. Every unit of the
  difference is accounted for by text appended *after* that pass counted — its own findings prose and
  the three new boxes — and cutting the files at the pre-READY boundary returns the original seven
  figures exactly. Not drift.
- **Tried to make the stacked re-save boxes a violation of "one box per file."** They are not new:
  `domain-entities.md`'s post-ten-redo and iteration-1-remediation boxes and `business-rules.md`'s
  iteration-1 box all sit inside the baseline cut whose censuses reproduce, so they were present when
  the terminal READY was issued. Exactly one box per file is new.
- **Tried to find a substantive edit disguised as a box.** Each new box is three lines of dated
  provenance prose. None states a rule, an entity, a count, a signature, a governed value or a
  scientific constant; none supersedes a prior statement; none adopts a default for any open item.
  The six disclosed open points (BLK-06's per-item binding, BLK-07's authorization, `RES-01`, item
  17's per-method scope, R-20's list source, the mode channel) remain open with no default quietly
  taken.
- **Re-checked the hard rules the re-save could have disturbed.** The single `TBD` hit is W-11's own
  prohibition; `RAW_MODULES` remains a static frozenset of four names with zero
  `import src.gnss` / `from src.gnss` hits; the only IRI mention stays item 17's enumerated B-01
  evaluation-time benchmark, whose configuration is hashed and never imported, in a unit living under
  `src/data/` where the `src/features` / `src/models` import ban is not engaged. No breach.

### E — Disposition

The artifacts are the bytes the terminal READY pass reviewed. Nothing of substance changed, no count
fails, and no post-READY addition asserts anything false. The unit stays buildable exactly as it was
approved, with its three documentation-class findings carried to the stage gate as input rather than
applied. **G-09 remains unsigned, so nothing here authorises creating a module.**

---

> **Re-saved unchanged 2026-08-26 under the third receipt** (twelfth redo, taken for
> `inventory-and-registry`; floor reset mechanical). **No content of this unit changed.**
> **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

## Review — 2026-08-26 third-receipt confirming pass

**Reviewer:** aidlc-architecture-reviewer-agent

**Verdict: READY**

**Class:** adversarial · **Scope:** NARROW change-verification · **Date:** 2026-08-26

The claim under review — *these three `produces[]` artifacts are unchanged in substance since the
2026-08-25 second-receipt confirming pass, apart from one dated re-save box per file* — **holds**.
Every census that pass printed re-derives to the same value, and two further counts are re-derived
independently. The three disclosed documentation-class findings are untouched and still ride as gate
input; they are not re-litigated here. **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

### A — Byte-level proof that the reviewed body is intact

Two cuts were measured. The first is the second-receipt pass's own § A baseline —
`business-logic-model.md` 1–1114, `business-rules.md` 1–770, `domain-entities.md` 1–475,
`functional-design-questions.md` 1–723 — the pre-READY body. The second is the state of the files
*at the moment that pass measured them*, before it appended its own section:
`business-logic-model.md` 1–1288, `business-rules.md` 1–773, `domain-entities.md` 1–478,
`functional-design-questions.md` 1–741. Reproducing both pins every byte through that pass's own
measurement point, not merely through the terminal READY.

| Census | Second-receipt pass asserted | Re-derived now | Match |
|---|---|---|---|
| `grep -oh "[A-Za-z]*Error"`, pre-READY cut | `IntegrityError` 24 · `PhaseBoundaryError` 16 · `EvidenceScanError` 16 · `LockedTestError` 14 · `ManifestError` 12 · `ReuseError` 10 · `PartitionError` 3 | 24 · 16 · 16 · 14 · 12 · 10 · 3 | **exact, all seven** |
| same census, that pass's own measurement cut | 28 · 23 · 20 · 17 · 16 · 14 · 5, plus **1** bare `Error` | 28 · 23 · 20 · 17 · 16 · 14 · 5, plus **1** bare `Error` | **exact, all eight** |
| `G-09` mentions per file, pre-READY cut | 7 / 3 / 4 | 7 / 3 / 4 | **exact** |
| `grep -n TBD`, three artifacts | 1 substantive hit, `business-logic-model.md:781`, W-11's *prohibition* | 1 hit, line **781** | **exact, anchor unmoved** |
| mode-channel OPEN item, `md5sum` | `92415266a0cd08bafaeb5962d6188872` at three sites | `92415266a0cd08bafaeb5962d6188872` at `business-logic-model.md:818`, `business-rules.md:716`, `domain-entities.md:425` | **exact, and still byte-identical across the three** |

The second row is the decisive one: an edit anywhere in `business-logic-model.md` 1–1288 — including
inside the second-receipt section's own § A–§ E — would have to leave all eight token counts
untouched to survive it.

Cited line anchors still resolve, which insertion above them would have shifted:
`business-rules.md:373` reads `## R-23 — Both phase-boundary limbs run, and neither substitutes for
the other`; `:669` and `:671` still carry `tests/test_reuse_registry.py`; `domain-entities.md:349` is
the base-class box; `:460` still reads *"all five"*; the aborted-row rationale still sits at
`:366-368`.

**Exception table still renders contiguously.** `cat -A` over `domain-entities.md:371-379`: blank at
371, header `| Exception | Raised when |` at 372, delimiter at 373, **five** body rows at 374–378
(`PhaseBoundaryError`, `LockedTestError`, `ReuseError`, `ManifestError`, `EvidenceScanError`), blank
at 379. No interleaved blank line, no stray `^M`.

**Negative check, deliberately run.** A *silent fix* of a disclosed finding would itself be a
substantive change. None occurred: `R-30` still appears exactly once outside review prose, at
`business-rules.md:671`; `domain-entities.md:460` still states five and enumerates four; the
aborted-row rationale is unamended. All three findings stand as gate input, as intended.

### B — Spot re-derivations, chosen independently

**Rule numbering — 12 headings, R-18 → R-29.** `grep -c "^## R-" business-rules.md` → **12**; the
extracted heading list, sorted with `sort -V`, is `R-18 R-19 R-20 R-21 R-22 R-23 R-24 R-25 R-26 R-27
R-28 R-29`: no gap, no duplicate, and **no `R-30` heading**. That is the premise of disclosed finding
1, confirmed rather than reopened.

**Second, re-derived from the authority rather than from the artifact — D-24's 17 protected items.**
Read straight off `evidence/DECISIONS.md` § D-24's Hashable-representation column, rows extracted
programmatically rather than carried from adjacent prose:

| Kind | Items | Count |
|---|---|---|
| Config-section hash | 4, 7, 9, 11, 14, 16 | 6 |
| Field hash | 5, 6 | 2 |
| Config hash (whole file) | 12 | 1 |
| Source-file content hash | 1 | 1 |
| Composites (`Source + …`) | 13, 15, 17 | 3 |
| Externally supplied | 2, 3, 8, 10 | 4 |
| **Total** | **union {1…17}, no gap, no duplicate** | **17** |

`6 + 2 + 1 + 1 + 3 + 4 = 17`, and `evidence/DECISIONS.md:1463` independently states *"cardinality 17,
calculated from the enumeration"*. W-3a's three tables agree item for item. Unchanged by the re-save.

### C — The post-READY additions, and whether they assert anything false

Exactly **one** new dated box per artifact, each three lines and each the file's final content before
this section: `business-logic-model.md` 1447–1449 · `business-rules.md` 777–779 ·
`domain-entities.md` 482–484. Every older stacked box falls inside the § A measurement cuts whose
censuses reproduce, so none is an addition of this receipt.
`functional-design-questions.md` gained a re-confirmation block at 742–758.

Each assertion tested:

- *"No content of this unit changed"* — **true**, on the eight exact census reproductions across two
  cuts and the unmoved anchors in § A.
- *"G-09 remains unsigned"* — **true**. Vision §13.1 records G-09 as `Open, before any affected
  component is coded` (quoted at `governance/reviews/GOV-2026-08-21-RA-01.md:135`);
  `evidence/DECISIONS.md:1207` and `:1463` both state implementation stays gated by G-09; a search of
  `evidence/` and `governance/` for a G-09 sign, approve or close record returns no signature.
- *"twelfth redo, taken for `inventory-and-registry`; floor reset mechanical"* — the redo event is
  real and its cited timestamp is exact to the second: `STAGE_JUMPED`, **Direction** `REDO`,
  **Source** and **Target** `functional-design`, **2026-08-26T05:43:39Z**, matching the citation in
  `functional-design-questions.md`. Recorded honestly, exactly as the second-receipt pass recorded
  the equivalent claim: the audit shard carries **no per-unit attribution field**, so *"taken for
  `inventory-and-registry`"* is **corroborated** — that unit's `functional-design/` files were written
  10:04–10:14 today against this unit's 09:48–09:50, and its construction files are modified in the
  working tree — rather than provable from the log. The ordinal *"twelfth"* is orchestrator
  bookkeeping the shard does not number: the shard records **17** `functional-design` →
  `functional-design` `REDO` jumps and numbers none of them. Neither point is a design claim about
  this unit, neither is contradicted by anything on disk, and neither changes what stage 3.5 would
  build — so this is a **scope note, not a finding**.

### D — Refutation attempts that failed

- **Tried to read the exception-token deltas as drift.** The full-file census now reads
  30 / 25 / 22 / 19 / 18 / 16 / 7 against the pre-READY 24 / 16 / 16 / 14 / 12 / 10 / 3. Every unit of
  the difference is text appended *after* each measurement — the second-receipt section's own prose
  and the three new boxes — and cutting at either § A boundary returns that boundary's figures
  exactly. Not drift.
- **Tried to make `grep "import src.gnss\|from src.gnss"` fail.** The full file now returns **2**
  hits in `business-logic-model.md`, at `:1240` and `:1434` — both inside review prose *quoting the
  grep pattern*, the same self-reference artefact as the single bare `Error` token at `:1134`. Over
  the pre-READY cut the count is **0**, and `business-rules.md` and `domain-entities.md` return zero
  over the whole file. The import ban is intact.
- **Tried to find a substantive edit disguised as a box.** Each new box is three lines of dated
  provenance prose. None states a rule, an entity, a count, a signature, a governed value or a
  scientific constant; none supersedes a prior statement; none adopts a default for any open item.
  The six disclosed open points (BLK-06's per-item binding, BLK-07's authorization, `RES-01`, item
  17's per-method scope, R-20's list source, the mode channel) remain open, and the mode-channel item
  is byte-identical at all three sites per § A.
- **Re-checked the hard rules the re-save could have disturbed.** The single substantive `TBD` hit is
  W-11's own prohibition at `:781`; `RAW_MODULES` remains a static frozenset of four names —
  `rinex`, `calibration`, `target`, `verification` (`business-logic-model.md:72`, `:821`;
  `business-rules.md:396`); the only IRI mention of consequence stays item 17's enumerated B-01
  evaluation-time benchmark, whose configuration is hashed and never imported, in a unit living under
  `src/data/` where the `src/features` / `src/models` import ban is not engaged. No breach.

### E — Disposition

The artifacts are the bytes the second-receipt confirming pass reviewed, which were in turn the bytes
the terminal READY pass reviewed. Nothing of substance changed, no count fails, and no post-READY
addition asserts anything false. The unit stays buildable exactly as it was approved, with its three
documentation-class findings carried to the stage gate as input rather than applied. **G-09 remains
unsigned, so nothing here authorises creating a module.**

---

> **Re-saved unchanged 2026-08-26 under the fourteenth-redo re-confirmation receipt** (redo taken
> for `external-products`; floor reset mechanical). **No content of this unit changed.**
> **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

## Review — 2026-08-26 fourteenth-receipt confirming pass

**Reviewer:** aidlc-architecture-reviewer-agent

**Class:** advisory-narrow · **Scope:** confirming pass over the fourteenth-redo re-confirmation
receipt (2026-08-26T08:18:34Z, taken for `external-products`; floor reset mechanical for this unit).

### Findings

1. `business-logic-model.md` — verified the only bytes added after the third-receipt confirming-pass
   review section (line 1453) are the disclosed fourteenth-redo provenance blockquote (three lines,
   ending the file). No other content added or removed.
2. `business-rules.md` and `domain-entities.md` — each carries the pre-existing twelfth-redo
   ("third receipt") blockquote followed by the new fourteenth-redo blockquote as the last content in
   the file; no other change intervenes.
3. `functional-design-questions.md` — the new "Re-confirmation, 2026-08-26 — under the
   fourteenth-redo floor" section is well-formed: an Impact line under each option, exactly one
   `> **💡 Recommendation**:` line placed after the options and before `[Answer]:`, and the tag is
   filled `Looks correct`.
4. Scripted scan (`bun -e`) of all four in-scope files for mojibake (`Ã`/`Â` runs) and C1 controls
   (U+0080–U+009F) found zero hits in every file.

No regression found. This is a narrow confirming pass only — the underlying content was not
re-litigated, and G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.

---

> **Re-confirmation receipt, 2026-08-29.** The 2026-08-27T21:49:36Z REDO jump reset every
> unit's receipt floor. This unit's content had already changed after that floor under the
> G-09 pass (D-29 through D-32; G-09 signed under D-31 with its §18.3 preconditions disclosed
> unmet), so the owner re-confirmed the unchanged post-G-09-pass content via the Consolidated
> Summary Confirmation at the foot of `functional-design-questions.md`, receipted `2026-08-29`.
> No line above this marker was touched by this pass.

READY

---

## Review — 2026-08-29 re-confirmation pass, iteration 1

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-29T00:00:00Z
**Iteration:** 1 of 2 (adversarial)

The trailing `READY` immediately above this section belongs to the 2026-08-22 iteration-2
pass and predates every G-09-pass edit (D-29 through D-31) and today's re-confirmation. This
pass reviews the unit as it stands after that pass, per the dispatch brief.

### Finding 1 — Critical. `RESTRICTED_LITERAL_EXEMPT_MODULES` is stated as **four** members in every representation except the one that records the correction to **five/six**

**Claim under test.** Under D-31 (2026-08-28, the G-09 pass), `business-rules.md` R-28 records
a **sixth holder** of the restricted-root literal, found by a full-repository sweep:
`scripts/merge_coverage_year.py`, a **production script**, outside the `tests/` exemption
entirely. R-28's own text states the consequence explicitly: *"The exemption is therefore no
longer `tests/`-only... bringing the list to **six**: the chokepoint itself, four `tests/`
modules, and this one production script"* and *"R-28's rule text above is narrowed
accordingly: membership is an **exact enumerated list**, not a directory predicate."*
(`business-rules.md` lines 907–920). This correction is dated the same day as, and is part
of, the D-31 G-09 pass this unit's own re-confirmation receipt (line 1856 above) says the
2026-08-29 re-confirmation covers.

**Derivation — every representation of the exemption count, grepped and printed:**

```
grep -rn "exactly four\|four modules hold the literal\|Four members\|four members" \
  business-logic-model.md business-rules.md domain-entities.md
```

Result (5 hits, 1 heading not matched by the pattern but asserting the same number):

- `business-logic-model.md:1015` — `§ Assumptions`: *"The exemption list is **exactly four**
  modules"* — **stale**.
- `business-rules.md:1148` — `§ Assumptions & Open Questions`: *"The exemption list is
  **exactly four** modules"* — **stale, and this is inside the SAME FILE as R-28's own
  six-member correction**, roughly 250 lines below it.
- `domain-entities.md:397` — § 7 `RESTRICTED_ROOT` body: *"the exemption's membership is
  **exactly** its four members"* — **stale**.
- `domain-entities.md:522` — the § 10 **heading itself**: *"`RESTRICTED_LITERAL_EXEMPT_MODULES`
  — new, bounded, **four members**, membership asserted exactly"* — **stale**.
- `domain-entities.md:546` — § 10 body: *"**Four members**, derived and printed 2026-08-28;
  3 of the 4 exist on disk today"* — **stale**, and the table immediately beneath it
  (lines 551–554) lists only the original four `tests/`-exemption rows; `scripts/
  merge_coverage_year.py` has no row.
- `domain-entities.md:591` — § 10 close: *"four modules hold the literal and no check exists
  to notice"* — **stale**.

**Why this is Critical, not Minor.** `RESTRICTED_LITERAL_EXEMPT_MODULES` is not incidental
prose — it is the entity whose exact membership *is* the one-door locked-test guard this unit
exists to build (W-10 / R-28's stated purpose: "membership is asserted exactly... an unlisted
module holding the literal fails the static check"). `domain-entities.md` is this unit's own
entity-shape artifact — the file a builder reads to know what constant to write and what the
membership test asserts against. As it stands, `domain-entities.md` § 10's heading, body, and
field table all specify a 4-member allow-list that omits `scripts/merge_coverage_year.py`. A
static check for "no module outside the enumerated exemption holds the restricted-root
literal," built against this specification, would **fail against the workspace on first run**
(`scripts/merge_coverage_year.py` does hold the literal, per R-28's own finding) — reproducing
exactly the failure mode `business-rules.md` R-28's own box says the sixth-holder discovery was
raised to prevent: *"The one-door property was broken by a production path, not only by test
scaffolding."* This is the sweep-completeness defect class the dispatch brief named by name:
a corrected fact updated in one representation (R-28's narrative box in `business-rules.md`)
and left standing in its pre-correction form in the entity's own field table, its own heading,
and — separately — in `business-logic-model.md`'s workflow narrative and both files' own
`§ Assumptions` sections, which exist specifically to carry forward the current open state.

**Not resolved by the day's later boxes.** The `⚠ THE READING IS RULED` box
(`business-rules.md` lines 928–934) and the re-confirmation receipts at the foot of all three
files post-date the sixth-holder finding and reference nothing about it; none narrows or
retracts R-28's "six" statement. The 2026-08-29 re-confirmation receipt on this file (line
1856) asserts the unit's content "had already changed after that floor under the G-09 pass
(D-29 through D-32...)" — i.e., claims to already carry the D-31 pass's content — while
`domain-entities.md` § 10, part of that same pass's edited surface, was not brought into
agreement with `business-rules.md`'s own correction from the same pass.

**Consequence for review class.** This is a within-unit cross-artifact inconsistency on a
governance-critical enumeration (the exact scope of the only sanctioned exception to the
locked-test one-door rule), verified by direct grep against the three PRIMARY produces[]
artifacts of this unit — not a sibling-unit or upstream-contract question, so it sits squarely
inside this review's bound.

### Finding 2 — Minor / documentation-debt, disclosed but worth flagging alongside Finding 1

R-28's own in-file arithmetic is ambiguous about whether the corrected figure is **five** or
**six**: the sixth-holder box counts *"the chokepoint itself, four `tests/` modules, and this
one production script"* as six, while `domain-entities.md` § 10's own framing ("members ...
in addition to `locked_test.py`") would put the corrected `RESTRICTED_LITERAL_EXEMPT_MODULES`
entity at **five** (four `tests/` modules + the one script), with the chokepoint counted
separately as before. Neither business-rules.md nor domain-entities.md states the corrected
entity-level count explicitly under either convention — the fix for Finding 1 needs to settle
this, not just add a sixth row under the ambiguous "six" label. Not blocking on its own, but
noted so the fix for Finding 1 doesn't introduce a second inconsistency between "five" and
"six" while resolving the first.

### What was checked and held

- The G-09-signed banner and its "preconditions UNMET" disclosure is consistent, verbatim or
  near-verbatim, across all three artifacts and every dated re-save box — no discharge is
  falsely claimed for TA-27, TA-28, WS-18, TA-18, the §18.3 preflight, or
  `aws_ai_dlc_preflight_report`.
- R-26's driver-exclusion class 4 (`.dst_summary.json`) "now unconditional" (D-30) is
  consistently represented across `business-logic-model.md` W-8, `business-rules.md` R-26, and
  `domain-entities.md` § 5 — all three read the same corrected figures (12 month keys, `storm30`
  15 days, `daily_min` 31 entries) and all three mark the relocation performed. No stale
  "conditional" language survives on this fact.
- R-28's "exact enumerated list, not a directory predicate" reading is internally coherent
  within `business-rules.md` itself (the ruling box, the narrowing box, and the per-member
  route table agree with each other), and nothing in the design still relies on the superseded
  substring/prefix reading — the defect is the stale headline number, not the mechanism.
- The pre-G-05 December coverage-and-regime audit is correctly modelled as permitted and
  performance-blind (W-7/R-25's box distinguishes it from the one-shot post-G-05 read), and
  W-8/R-26's December-hit definition correctly includes target aggregates, not only target
  values — no path was found by which a December record could reach a model while looking like
  a driver read.

### Summary

One Critical finding: the exemption entity that defines the locked-test guard's one-door
boundary is stated as four members in five of its six textual representations across this
unit's three PRIMARY artifacts, while the sixth representation (`business-rules.md` R-28's own
narrative) records the corrected count of five or six following the same-day discovery that a
production script, not only test modules, held the restricted-root literal. This is a
governance-critical, machine-checkable inconsistency inside the unit under review, not a
matter of taste, and it would misdirect an implementer building the entity from
`domain-entities.md` as written. NOT-READY.

## Review

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-29T08:06:00Z
**Iteration:** 2 (final)

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | `domain-entities.md:88` | The § "Entity map" Mermaid diagram still labels the `RESTRICTED_LITERAL_EXEMPT_MODULES` node `(4 members, asserted exactly)`. This is an eighth representation of the exemption count, not named in iteration 1's dispatch site list and not touched by the 2026-08-29 repair (verified: `grep -n "4 members\|four members" domain-entities.md` returns only this line and the intentionally-preserved historical box at `:577`/`:753`). It reproduces the exact defect class iteration 1 found Critical: a corrected fact (five members counting from the chokepoint, six counting the chokepoint, per R-28's reconciled convention) left standing in its pre-correction form in a representation a reader encounters. It is materially worse than a stray prose mention because the entity map sits at the top of `domain-entities.md`, ahead of § 10's corrected heading/body/table/box (line 522+) and ahead of the ⛔ correction box's own instruction "read this before any figure below" (line 524) — a reader who stops at the diagram, or who reads top-to-bottom, sees the stale "4" first and with no forward pointer to the correction. The immediately adjacent text fallback (lines 104–117) does not restate the number, so it does not contradict the diagram, but it also does not correct it. | Update the node label to `(5 members, asserted exactly)` (or state both conventions as § 10 now does) and, ideally, add a one-line note under the diagram or in the text fallback pointing to § 10's corrected count, so the entity map does not read the two counting conventions as a third, wrong one. |
| 2 | Minor | `domain-entities.md:753` | The dated 2026-08-28 remediation-log box ("Recommendation 2 … carries the **4 members**") still states the pre-correction figure. This is judged non-blocking: unlike Finding 1, it is explicitly a dated, preserved historical change-log entry describing what changed *on that day* (consistent with this artifact's own "superseded figures are preserved in place, never deleted" convention used throughout the 2026-08-29 correction boxes), not a live current-state claim, and it sits inside a box already marked "every earlier dated box above is preserved unchanged" (line 748). Flagged only so the human confirms this reading is intended rather than another missed site. | No change required if the historical-record reading is confirmed; otherwise append a forward-pointer to the 2026-08-29 correction the way the other dated boxes in this file do. |

### Verification of the iteration-1 repair (Critical + Minor)

- **Critical (iteration 1) — sweep completeness.** Re-grepped all three PRIMARY artifacts for every numeral/word form of the exemption count. All six originally-named sites (`business-rules.md:1148`, `business-logic-model.md:1015`, `domain-entities.md:397`, `:522` heading, `:546`→now `:576` body, § 10 field table) are corrected, each preserving the superseded "four" figure inline per this project's own learned correction-sweep convention, and the new field-table row 5 for `scripts/merge_coverage_year.py` accurately reflects R-28's box: six restricted content sites, all routed under D-31 through `open_restricted`, `On disk: Yes`. One site was missed — see Finding 1 above — because it uses the numeral `4` rather than the word `four`/`Four`, which is exactly the pattern iteration 1's own grep (`"exactly four\|four modules hold the literal\|Four members\|four members"`) would not have caught either; the repair inherited the same blind spot rather than introducing a new one.
- **Minor (iteration 1) — dual counting convention.** Resolved cleanly. Every corrected site now states both conventions explicitly and consistently: "this entity counts members **in addition to** the chokepoint" → five; "R-28's box counts the chokepoint as well" → six; "six = the chokepoint + these five." Checked for a *new* 5-vs-6 contradiction by grepping every remaining `\bsix\b`/`\bfive\b` occurrence across all three files — no other site conflates the two conventions or states an unreconciled figure for this specific entity.
- **Adjacent breakage.** No adjacent breakage found. The § 10 table's five rows are internally consistent (four `tests/` modules + the one production script), the "4 of the 5 exist on disk today" body sentence agrees with the table's per-row "On disk" column, and § Assumptions in both `domain-entities.md` and `business-rules.md` restate the same reconciled five/six pair without drift.

### Summary

The repair correctly reached and fixed all six sites named in iteration 1's finding, and cleanly resolved the counting-convention ambiguity flagged as Minor. It missed one further, genuine, live representation — the Mermaid entity-map diagram at `domain-entities.md:88` — which was never named in iteration 1's own grep-derived site list because that grep matched only word-form "four," not the numeral "4" the diagram uses. Given this is the same governance-critical entity, in the same document, under the same repair pass, and the diagram precedes the correction box that would otherwise warn a reader, this is graded Critical rather than accepted as a residual documentation nit. This is the final review iteration; the remaining gap and the one Minor historical-box question go to the human at the approval gate rather than a further automated repair cycle.

NOT-READY

## Review — 2026-08-30 fresh pass, iteration 1 (post-gate-rejection)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-30T11:35:06Z
**Iteration:** 1

### Scope and method

Re-derived the site list from scratch rather than trusting either prior review's enumeration, per this project's own learned rule (`fd-2026-08-30-sweep-derive-sites`). Grepped all three PRIMARY artifacts (`business-logic-model.md`, `business-rules.md`, `domain-entities.md`) for **both** numeral and word forms in both directions — `4 members|four members|Four members|exactly four` and, separately, `RESTRICTED_LITERAL_EXEMPT_MODULES|four member|4 members|five member|5 members|six member|6 members|merge_coverage_year` — across headings, entity field tables, Mermaid node labels, rule bodies, § Assumptions, change-log/correction boxes, and Sources. Cross-checked `WS-18`/`TA-18`/`G-09`/`UNEXECUTED`/`discharged` occurrences in `domain-entities.md` against the dispatch's non-discharge caveats. Budget-bound: did not re-read every artifact line end-to-end; coverage is targeted at the defect class named in the dispatch plus a bounded adversarial hunt for two named failure modes (guard bypass, audit blockage).

### Findings

No Critical or Major findings survive verification.

**Verification of the 2026-08-30 repair (the specific defect two prior iterations found):**

- **The stale Mermaid node is fixed.** `domain-entities.md:88` now reads `(5 members, asserted exactly)`. Line 116 adds a forward/backward pointer (`⛔ the diagram node above read (4 members …) until 2026-08-30 and is corrected; see § 10's...`), which is exactly the "note under the diagram" iteration 2's Finding 1 recommended. The text fallback carries the corrected count.
- **No live "four" survives elsewhere.** Every remaining `four`/`Four`/`4 members` hit resolves to one of two accepted categories: (a) inside a prior appended `## Review` section in this same file (lines 1867–2019) — per the dispatch contract, prior `## Review` sections are reviewer output, not content under review, so a reviewer quoting the old "four" while describing the historical defect is expected, not a live claim; (b) inside an explicitly dated, preserved historical box (`domain-entities.md:582`, `:753`) that this artifact's own convention marks as superseded-and-kept, each carrying a `(corrected 2026-08-29…, superseded figure preserved: "four…")` annotation immediately adjacent. Neither category is a live stale assertion a reader would take as current.
- **No new 5-vs-6 contradiction.** Every site stating a count states it as one of the two reconciled conventions ("this entity: five, in addition to the chokepoint" / "R-28's box: six, chokepoint included"), consistently, including `business-rules.md`'s sixth-holder box (lines 888–914, "bringing the list to six: the chokepoint itself, four `tests/` modules, and this one production script") and `domain-entities.md`'s § 10 body/table/assumptions (lines 527, 629, 402, 643).
- **Row 5 (`scripts/merge_coverage_year.py`) is described accurately** and consistently between `business-rules.md`'s box and `domain-entities.md` § 10: a production script (not a test), holding the restricted-root literal, that read six restricted sites with no `AccessRecord`, now routed through `src.data.locked_test.open_restricted` under D-31, with `On disk: Yes`.

**Adversarial hunt beyond the defect class (dispatch-directed):**

- **WS-18/TA-18 discharge:** not found implied-discharged anywhere checked. `domain-entities.md:557` states outright, in bold, "**WS-18 and TA-18 are NOT discharged**," and line 616 additionally notes `open_restricted` "does not exist (G-09 unsigned)" as of the point that sentence describes — reconciled at lines 772–783 with the later, separate fact that G-09 was subsequently signed under D-31 with its §18.3 preconditions explicitly disclosed as **unmet**. No site claims the guard test executed or that access was logged by a running system.
- **December-record-reaches-model / audit-blockage paths:** found no constructed path. `domain-entities.md:303` explicitly keeps `RES-01` (permitted-read logging) open as **NOT [resolved]**, rather than overclaiming it closed, and the pre-G-05 coverage-audit references (lines 303, 418) describe it as a permitted, distinct read path rather than one the locked-test guard would block. This is consistent with — not merely silent on — the mandated rule that the pre-G-05 audit must remain unblocked.
- **G-09/D-31 status:** correctly stated as signed-with-unmet-preconditions throughout the sites checked (lines 3–8, 782–783), not as a general discharge of stage 3.1 or of TA-15/`aws_ai_dlc_preflight_report`/`configs/`/the §18.3 zero-TBD preflight — none of those was found asserted as discharged anywhere in this pass.

### Coverage limits

This pass targeted the named defect class and the two named adversarial paths; it did not re-verify every cross-reference, entity cardinality, or business rule in the three PRIMARY artifacts end-to-end, and did not re-open sibling-unit content (none was read, per read-scope). Any defect outside that targeted scope would not have been caught here.

### Summary

The 2026-08-30 repair closes the specific gap that produced two consecutive NOT-READY verdicts: the Mermaid entity-map node is corrected, carries a forward pointer, and no other live site in the three artifacts still asserts the superseded "four" figure — the remaining occurrences are prior-review quotations or explicitly preserved, dated historical boxes, both outside the defect's scope. The 5-vs-6 dual convention remains internally consistent, row 5 is described accurately, and the targeted adversarial checks (WS-18/TA-18 discharge, guard-blocks-required-audit) found no new defect. No Critical or Major finding is raised.

READY

## Review — 2026-08-30 re-confirmation pass, iteration 1 (gate-rejection reset, prior attempt lost to rate limit)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-30T00:00:00Z
**Iteration:** 1 of 2 (adversarial)

### Scope and method

Content under review is unchanged since the standing 2026-08-30T11:35:06Z READY verdict immediately above (a human gate rejection reset the review floor; nothing in this unit's three PRIMARY artifacts was edited in between). Per the dispatch's own framing this is a confirming pass, not a rubber-stamp: independently re-derived the site list rather than trusting the prior verdict, then compared results.

Ran, fresh, against all three PRIMARY artifacts:
```
grep -n "four member|Four member|4 members|exactly four" business-logic-model.md business-rules.md domain-entities.md
```
Every hit resolves to one of two non-live categories: (a) inside an already-appended `## Review` section of this same file (out of scope per the dispatch — prior `## Review` sections are reviewer output, not content under review), or (b) inside an explicitly dated, annotated superseded-and-preserved box (`domain-entities.md:582`, `:758`) that states its own supersession inline. No live assertion of "four" survives anywhere in `business-logic-model.md`, `business-rules.md`, or `domain-entities.md`.

Every live count site — `business-logic-model.md:1015`, `business-rules.md:1148`, `domain-entities.md:677` (§ Assumptions), `domain-entities.md` § 10 heading/body/table, and the Mermaid node + forward-pointer at `domain-entities.md:88`/`:116` — states **exactly five** (equivalently six counting the chokepoint `src/data/locked_test.py`), with both conventions reconciled consistently and `scripts/merge_coverage_year.py` present as the fifth/production member in every table and assumption. No 5-vs-6 contradiction found.

### Findings

No Critical, Major, or new Minor findings.

- **RESTRICTED_LITERAL_EXEMPT_MODULES count (Focus 1):** confirmed correct at every live site checked, independently re-derived, not merely re-read from the prior review's own claim.
- **No overclaim (Focus 2):** `domain-entities.md` still states outright that WS-18 and TA-18 are **not** discharged, and the G-09-signed / preconditions-unmet disclosure (§18.3 preflight never ran, critical tests UNEXECUTED, `aws_ai_dlc_preflight_report` absent) is present and undisturbed since the last pass — nothing in the unchanged content implies the guard test executed.
- **Adversarial hunt (Focus 3):** no path found by which a December record reaches a model undetected, and the pre-G-05 coverage/regime audit is still modelled as a permitted, performance-blind read distinct from the guard's blocked path — consistent with the standing review's own finding here, re-checked rather than assumed.

### Coverage limits

This is a confirming pass on unedited content, budget-bound to the named focus areas (the exemption-count sweep and the two named adversarial paths) plus a spot recheck of the discharge-caveat language; it did not re-derive entity cardinalities, business-rule completeness, or cross-references end to end. Any defect outside that targeted scope would not have been caught here, consistent with the coverage limits the standing 2026-08-30T11:35:06Z review already disclosed.

### Summary

No regression from the standing READY verdict: the exemption-count sweep is independently re-verified clean, no discharge is overclaimed, and no new guard-bypass or audit-blockage path was found. Confirming this unit's functional-design artifacts remain READY.

READY

## Review — 2026-08-30 confirming pass

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-30T18:31:36Z
**Iteration:** 1 of 2 (fresh budget after human gate rejection; this unit's artifacts are unchanged since the prior READY)

### Independent re-derivation (this pass, not carried from prior reviews)

`RESTRICTED_LITERAL_EXEMPT_MODULES` (Focus 1): grepped `business-rules.md`, `business-logic-model.md`, and `domain-entities.md` for the count in both numeral and word form (`four`, `Four`, `4 members`, `five`, `5 members`, `six`, `6 members`, `merge_coverage_year`). Every live current-state site states **five** members in addition to the chokepoint `src/data/locked_test.py`, equivalently **six** counting it — `business-rules.md:1148`, `business-logic-model.md:1015`, `domain-entities.md` entity-map Mermaid node (`domain-entities.md:88`, now `(5 members, asserted exactly)`) with its forward-pointer at `:116`, and § 10's heading/body/table/assumptions (`:402`, `:527`, `:541-545`). `scripts/merge_coverage_year.py` — a production script, not a test — is present as the fifth/production member at every one of those sites, consistent with R-28's own convention that membership is an exact enumerated list, never a `tests/`-directory predicate. Every remaining occurrence of the superseded "four" is either (a) a quotation inside a prior `## Review` section — not live content under this dispatch's rule — or (b) an explicitly dated, preserved historical box (`domain-entities.md:582`, `:753`) carrying its own superseded-figure annotation. No live site asserts four. No new 5-vs-6 conflation found.

No overclaim (Focus 2): `domain-entities.md:557` states outright "**WS-18 and TA-18 are NOT discharged**"; `domain-entities.md:696` and its restated copies carry D-31's full disclosure alongside the G-09 signature — §18.3 preflight never ran, critical tests **UNEXECUTED** in this environment, `aws_ai_dlc_preflight_report` does not exist, no scientific value becomes fillable. Nothing in the artifacts implies the guard test executed or that access was logged by a running system.

Adversarial hunt (Focus 3): checked `business-rules.md` for the record-date-vs-directory/filename fold-membership rule — `business-rules.md:804-806` states identification is "by record date, never by filename or directory name," citing the `audit_evidence_2022-01/` incident directly, closing the path a December record could enter under a non-December directory label. The pre-G-05 December coverage/regime audit is modelled as a distinct, permitted, performance-blind read, separate from the guard's blocked path (no site found that would block it). No path found for a locked-test access without an `AccessRecord`/`locked_test_accessed` write, or for a Phase 2 run proceeding on a differing protected hash, within the scope of these three artifacts.

### Findings

No Critical, Major, or Minor findings from this pass.

### Coverage limits

Confirming pass on unchanged content, bounded to the dispatch's three focus areas plus the named adversarial paths; did not re-derive entity cardinalities, business-rule completeness, or cross-references end to end beyond what the exemption-count and discharge checks required.

### Summary

Independently re-verified: the exemption-count sweep resolves clean at every live site, no WS-18/TA-18/G-09-preflight discharge is overclaimed, and the record-date-vs-directory-name and audit-blockage adversarial paths are both closed by the artifacts as written. No regression from the standing READY verdict.

READY
