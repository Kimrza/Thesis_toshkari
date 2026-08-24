# Unit of Work Dependencies — Hourly VTEC Forecasting (TEC_Project Phase 1)

Stage 2.7 (units-generation), intent `260813-tec-hourly-forecast`.

## Sources

- Design: `../application-design/component-dependency.md` (the dependency matrix, the forbidden edges and what proves each, the data flow, the shared-resource table), `../application-design/components.md` (package boundaries), `../application-design/component-methods.md` (the boundary signatures each edge crosses), `../application-design/services.md` (the stage entry contract and the ordering contract), `../application-design/decisions.md` (ADR-02, ADR-03, ADR-05, ADR-09, ADR-10).
- Requirements: `../requirements-analysis/requirements.md` — FR-P1-03-2 (both prohibition limbs), FR-P1-04-1 (the IRI allowlist), FR-WS-1 (fixture ordering), REQ-ENG-1 (the §12 tree).
- `stories` (`../user-stories/stories.md`) is absent by scope design — stage 2.4 is `SKIP`.
- Companion: `unit-of-work.md` (unit definitions), `unit-of-work-story-map.md` (requirement and acceptance traceability).

## Topology only

This artifact records **which unit can depend on which**. It does not name a
recommended build order and does not identify a critical path: multiple
topological orderings are legal, and choosing among them is stage 2.8's economic
decision.

## The DAG

Two dependency roots, then a spine with one fork, closed by the fixture and
clean-run unit.

```
foundation
    │
    └─► governance-guards
              │
              └─► acquisition
                       │
                       └─► inventory-and-registry
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
        target-standardization           external-products
                    │                           │
                    └─────────────┬─────────────┘
                                  ▼
                        features-and-splits ◄── governance-guards
                                  │
                                  ▼
                        models-and-baselines
                                  │
                                  ▼
                   evaluation-and-comparison ◄── external-products
                                  │
                                  ▼
                        statistical-inference
                                  │
                                  ▼
                   regimes-diagnostics-reporting
                                  │
                                  ▼
                   fixtures-and-reproducibility
                   (direct edges to nine units — the seven that own an
                    invoked stage script, plus statistical-inference and
                    regimes-diagnostics-reporting for their artifacts)
```

**Text fallback.** `foundation` is the first root and depends on nothing.
`governance-guards` depends on `foundation` alone and is the second root.
`acquisition` depends on both roots. `inventory-and-registry` depends on
`acquisition`. The graph then forks: `target-standardization` and
`external-products` both depend on `inventory-and-registry` and on nothing else
in the fork. `features-and-splits` depends on both fork branches plus
`governance-guards`. From there the spine is linear:
`models-and-baselines` → `evaluation-and-comparison` (which also takes an edge
from `external-products`) → `statistical-inference` →
`regimes-diagnostics-reporting`. `fixtures-and-reproducibility` depends directly
on nine units. Seven of them own a stage script the clean-run sequence invokes:
`acquisition`, `inventory-and-registry`, `target-standardization`,
`external-products`, `features-and-splits`, `models-and-baselines` and
`evaluation-and-comparison`. The other two — `statistical-inference` and
`regimes-diagnostics-reporting` — own **no** stage script; their logic runs inside
`07_evaluate_and_report.py`, which `evaluation-and-comparison` owns, so their
edges exist because the clean run and its evidence package consume their released
artifacts, not because a script of theirs is invoked.

## Edge table

| Unit | Depends on | Why this edge exists |
|---|---|---|
| `foundation` | — | Dependency root. Owns the §12 tree, the pins, the four configs and the config/determinism/release services every other unit calls. |
| `governance-guards` | `foundation` | The transition manifest hashes the configuration snapshot, and both guards are constructed from the loaded config. |
| `acquisition` | `foundation`, `governance-guards` | Its stage script runs the six-step stage entry contract, which calls `ensure_process_determinism`, `load_configs`, `assert_no_tbd` and `assert_phase_boundary` before any domain work. |
| `inventory-and-registry` | `acquisition` | Inventories and validates the artifacts acquisition released, by release ID and hash. |
| `target-standardization` | `inventory-and-registry` | Standardizes only files that passed schema validation, using the registry's cell rule. |
| `external-products` | `inventory-and-registry` | IRI and GIM products are generated at the registry's pinned coordinates and cells. Drivers are time-indexed and need no cell join, so this edge is carried by the benchmark and comparator, not by `spaceweather.py`. |
| `features-and-splits` | `target-standardization`, `external-products`, `governance-guards` | Features join the target rows with the driver series; the locked-partition execution guard consumes `locked_test.py`'s contract. |
| `models-and-baselines` | `features-and-splits` | Trains on the **`FeatureBundle`s** — matrix and sequence tensor travelling as one stamped object — over the six-member `Partition` list. *(Corrected 2026-08-23 from "the feature matrix and sequence tensor over the F1–F4 folds": ADR-11 replaced both nouns, and `FoldSpec`'s four folds became `Partition`'s six members, `REFIT` and `DEC` having been unrepresentable before. Same correction as § Integration points, which this row restates.)* |
| `evaluation-and-comparison` | `models-and-baselines`, `external-products` | Masks and metrics read predictions on one side and the IRI benchmark / GIM comparator on the other, joined at evaluation time. |
| `statistical-inference` | `evaluation-and-comparison` | Bootstraps the paired loss differential the metrics module computes, on the frozen mask. |
| `regimes-diagnostics-reporting` | `statistical-inference` | Reported breakdowns and figures carry the intervals the bootstrap produces. |
| `fixtures-and-reproducibility` | nine units — see the two rows below | Split by reason, because the two reasons are not the same. |
| ↳ `acquisition`, `inventory-and-registry`, `target-standardization`, `external-products`, `features-and-splits`, `models-and-baselines`, `evaluation-and-comparison` (7) | — | Each owns a stage script TE §13.2's clean-run sequence invokes directly. The edges are direct, not transitive. |
| ↳ `statistical-inference`, `regimes-diagnostics-reporting` (2) | — | Neither owns a stage script — both run inside `07_evaluate_and_report.py`. The edge is on their released artifacts (bootstrap intervals, breakdowns, figures, the claims checklist), which the clean-run tolerance comparison and the traceability matrix consume. |

## Edge block

```yaml
units:
  - name: foundation
    kind: library
    depends_on: []
  - name: governance-guards
    kind: library
    depends_on: [foundation]
  - name: acquisition
    kind: library
    depends_on: [foundation, governance-guards]
  - name: inventory-and-registry
    kind: library
    depends_on: [acquisition]
  - name: target-standardization
    kind: library
    depends_on: [inventory-and-registry]
  - name: external-products
    kind: library
    depends_on: [inventory-and-registry]
  - name: features-and-splits
    kind: library
    depends_on: [target-standardization, external-products, governance-guards]
  - name: models-and-baselines
    kind: library
    depends_on: [features-and-splits]
  - name: evaluation-and-comparison
    kind: library
    depends_on: [models-and-baselines, external-products]
  - name: statistical-inference
    kind: library
    depends_on: [evaluation-and-comparison]
  - name: regimes-diagnostics-reporting
    kind: library
    depends_on: [statistical-inference]
  - name: fixtures-and-reproducibility
    kind: library
    depends_on: [acquisition, inventory-and-registry, target-standardization, external-products, features-and-splits, models-and-baselines, evaluation-and-comparison, statistical-inference, regimes-diagnostics-reporting]
```

Derived and checked when this artifact was written: **12** units, each named
exactly once; **23** edges; every name in every `depends_on` list is a
declared unit; no unit depends on itself; the graph is acyclic.

## Integration points

Units communicate through **hashed released artifacts identified by release ID**,
verified by hash — never by path convention, so a unit cannot silently consume a
stale artifact from a previous run. There is no database, no lock file, no
message queue and no shared mutable state between units.

| Contract | Producer | Consumers | Form |
|---|---|---|---|
| `ConfigSnapshot` + config hash | `foundation` | every unit, at stage entry | in-memory object, hashed into the run record |
| seeded-run contract (`seed_everything`, `ensure_process_determinism`) | `foundation` | every unit | call at stage entry; `statistical-inference` carries its own carved-out seed |
| release manifest + SHA-256 (TE §13.3, ten rows over fourteen fields) | `foundation` | every unit that releases an artifact | manifest file, write-protected or new version |
| `experiment_registry.jsonl` | `foundation` writer, appended by every stage script | human review, `fixtures-and-reproducibility` | append-only JSONL; a derived, hashed CSV is regenerated, never merged |
| `assert_phase_boundary`, `assert_no_raw_fields` | `governance-guards` | every stage script | call at stage entry, step 4 of six |
| `open_restricted` (access-log row written before the read) | `governance-guards` | `acquisition` (the D-9 input `audit_evidence_2022-FULL/` and any December re-acquisition — routing contract **not yet authored**, see `unit-of-work.md` **BLK-07**), `inventory-and-registry` (coverage audit), `features-and-splits` (locked partition), `evaluation-and-comparison` (locked evaluation) | single chokepoint into `evidence/locked_test_restricted/`. `component-dependency.md` § Shared resources states the rule without qualification — "nothing else may construct a path into it" — and **no unit may construct such a path directly**, `foundation` and `acquisition` included, notwithstanding their general permission to construct paths into `evidence/` |
| `phase_transition_manifest` over the canonical protected set derived from TE §2.2 ∪ TE §7.0B; **final enumeration and cardinality deferred to stage 3.1**, and this artifact states neither — see `unit-of-work.md` **BLK-06** | `governance-guards` | G-P2 / G-P3C | manifest file; a data contract, not a call surface |
| §10.1 reuse register rows | `governance-guards` | G-P2 | register file, written before the code is used |
| provider files, `request_manifest.json`, `sha256_manifest.json` | `acquisition` | `inventory-and-registry` | released artifacts by release ID |
| source inventory (TE §5.1, nine fields) + station registry | `inventory-and-registry` | `target-standardization`, `external-products` | released artifacts |
| Phase 1 target rows under D-17's contract, stamped `phase_id` / `source_id` / `target_definition_id` | `target-standardization` | `features-and-splits` | released artifact |
| driver series with availability semantics | `external-products` | `features-and-splits` | released artifact; time-indexed only |
| IRI-2016 benchmark (B-01), CODE final GIM comparator (C-01) | `external-products` | `evaluation-and-comparison` **only** | released artifacts, joined at evaluation time onto the frozen mask |
| **`FeatureBundle`s** — matrix + tensor + `FrameSpec` + `transform_id`, from one window definition — the six-member `Partition` list (`F1`–`F4`, `REFIT`, `DEC`), and the 24-hour embargo | `features-and-splits` | `models-and-baselines` | released artifacts, one directory per bundle addressed `<partition_id>__<role>__<transform_id>/`, sharing one feature-set ID |
| per-seed predictions + three-seed element-wise mean, checkpoints | `models-and-baselines` | `evaluation-and-comparison` | released artifacts |
| comparison-wide intersection mask (stable ID, row counts), paired loss differential | `evaluation-and-comparison` | `statistical-inference`, `regimes-diagnostics-reporting` | one mask per comparison set, never pairwise |
| bootstrap intervals, 48 h sensitivity, cross-station correlation | `statistical-inference` | `regimes-diagnostics-reporting` | released artifact |
| fixture manifests, clean-run log, `environment_and_cpu_preflight_report`, traceability matrix | `fixtures-and-reproducibility` | G-07, G-09 | released artifacts |
| **M10 contract fixture** — synthetic partition dates plus its four assertions on ADR-11's leakage boundary, carried in `test_train_only_transforms.py` and `test_split_embargo.py` | `features-and-splits` (**authors**) | `fixtures-and-reproducibility` (**runs it in the clean-run sequence**) | test modules invoked by the clean run; a **negative control**, never scientific evidence, and **not** a third mandated walking-skeleton fixture |

> **⚠ The `features-and-splits` → `models-and-baselines` row was corrected 2026-08-23.**
> It read *"feature matrix + sequence tensor (one window definition), F1–F4 folds,
> embargo … released artifacts sharing one feature-set ID"*. **ADR-11 replaced both
> nouns**: the two representations now travel in one `FeatureBundle` carrying its own
> `FrameSpec` and `transform_id`, and `FoldSpec` became `Partition` with six members
> rather than four — `REFIT` and `DEC` were unrepresentable under the old type, which
> is what stalled stage 3.1 for five review cycles. The row described a contract that
> no longer existed. Corrected under the owner's ruling of 2026-08-23 at the approval
> gate, in the same sweep that reached the per-unit blocker paragraphs.

**Added 2026-08-23 under the owner's ruling Q12 = C.** This handoff **adds no edge**:
`fixtures-and-reproducibility` already depends on `features-and-splits` in the fenced
block below, so the fenced `yaml` is unchanged. Recording it as an integration point
on an existing edge rather than as a new edge is deliberate — topology is what the
graph states, and this contract rides an edge the graph already carries.

## Forbidden edges — absent by rule, not by accident

Carried from `component-dependency.md`, restated at unit granularity because a
forbidden edge needs a test and an absent one does not.

| Forbidden edge (unit level) | Rule | Enforced at run time by | Test | Owning unit |
|---|---|---|---|---|
| any Phase 1 unit → `src/gnss/*` | TE §7.0 hard prohibition; NFR-PHASE-01 | `assert_phase_boundary` at every stage entry | `test_phase_boundary.py` | `governance-guards` |
| a Phase 1 artifact carrying a DCB/STEC/mapping/satellite/arc field | TE §7.0, produced-field limb | `assert_no_raw_fields` | `test_phase_boundary.py`, second independent result | `governance-guards` |
| `features-and-splits` or `models-and-baselines` → `iri.py`/`gim.py` | NFR-IRI-01; TE §12 | import-boundary check | `test_iri_denial.py` | `features-and-splits` |
| any path outside the authorized two → `iri.py`/`gim.py` | TE §12 allowlist, stated at **module-path** granularity: permitted only in `scripts/04_build_external_products.py` and modules under `src/evaluation/`, subject to all applicable evaluation-stage, frozen-mask and locked-test restrictions. Modules under `src/evaluation/` are owned by three units — `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting` — so the grant is on the path, never on a whole unit's unrelated code, and directory membership never overrides a separate gate, access-logging, frozen-mask or locked-test restriction | same check, allowlist form | `test_iri_denial.py` | `features-and-splits` |
| an `iri_*` field or IRI-derived residual reaching training or inference | Vision §7.1 | `features.build_features` raises | `test_iri_denial.py` — **must fail on deliberate injection** | `features-and-splits` |
| a field outside the TE §6.2 dictionary entering features | FR-P1-04-12 | `features.build_features` raises | **no §16/§19 row** | `features-and-splits` |
| a carried-forward `vtec_lag_*` value | FR-P1-04-13 | `features.build_features` raises | **no §16/§19 row** | `features-and-splits` |
| a driver repeated outside its own interval, or interpolated | FR-P1-04-17 | `features.build_features` raises | **TA-36** (added 2026-08-22, `CR-2026-08-22-LEAKAGE-TA`); primary rejection test at the feature-building enforcement boundary, in `tests/test_feature_leakage_guards.py` | **Enforcement + acceptance test:** `features-and-splits`. **Data production:** `external-products` — see the reconciliation below |
| a support field used as a model input without G-04 approval | FR-P1-04-16 | `features.build_features` raises | **no §16/§19 row** | `features-and-splits` |
| a December read without a preceding access-log row | FR-P1-05-12 | `locked_test.open_restricted` writes then reads | `test_locked_test_guard.py` | `governance-guards` (module) / `features-and-splits` (test) |
| December execution before G-05 | FR-P1-05-12 | `splits.materialise_locked_partition` raises | `test_locked_test_guard.py`, WS-18 | `features-and-splits` |
| `models-and-baselines` → `evaluation-and-comparison` | dependency direction | none needed — the inverted import would be a cycle | — | — |

**Four of the five gained acceptance rows on 2026-08-22.** TA-33, TA-34, TA-35 and
TA-36 were approved under Vision §15.2 (`CR-2026-08-22-LEAKAGE-TA`) for
FR-P1-04-12, FR-P1-04-13, FR-P1-04-16 and FR-P1-04-17 — the leakage paths a
governance board flagged as "criterion states it, nothing tests it". **One
remains without a row: FR-P1-04-10**, carried to stage 3.2. All four new rows
carry status `Pending`: the criteria exist, the module `tests/test_feature_leakage_guards.py`
is named and documented but **not written, not executed and not passing**.

### FR-P1-04-17 — ownership reconciliation, recorded 2026-08-22

The story map assigned FR-P1-04-17 to `external-products`; this table's
enforcement column put the raise in `features.build_features`, owned by
`features-and-splits`. Both were right about different things, and the
inconsistency was carried silently until governance review surfaced it. It is
resolved here by distinguishing four ownerships rather than picking one unit:

| Ownership | Unit / Bolt | What it covers |
|---|---|---|
| **Upstream data production** | `external-products` / Bolt 5 | Building the driver series so each value carries its own interval semantics — Kp/ap3 on its 3-hour interval, Dst on its hourly averaging interval, F10.7 daily — and performing no interpolation at any stage |
| **Enforcement** | `features-and-splits` / Bolt 7 | The raise at `features.build_features` when a driver value is repeated outside its own interval or shifted to a neighbouring hour |
| **Primary negative-path acceptance test** | `features-and-splits` / Bolt 7 | TA-36, sited at the feature-building enforcement boundary, in `tests/test_feature_leakage_guards.py` |
| **Upstream evidence and data-contract responsibility** | `external-products` / Bolt 5 | Driver manifests recording per-series interval semantics and release grade; any upstream contract test is **documented separately and does not replace** the primary rejection test |

**This allocation is the default and stands unless functional design produces
verified evidence for a better one.** Functional design owns the confirmation; if
it reallocates, it records the reason and updates both artifacts rather than one.
The story map's Table 1 keeps `external-products` as the requirement's primary
unit (data production is where the obligation originates) with
`features-and-splits` named as supporting on TA-36 — so the two artifacts now
agree.

## Independent unit sets

Q7 = A: independence is recorded as a property of the graph, for stage 2.8's
sequencing, for alternative legal orders, and for recovery when a unit is
blocked. It is **not** a statement about staffing. This is a single-author thesis
codebase, and independent units will normally be implemented sequentially.

Derived from the edge block — every pair with no directed path in either
direction:

- `target-standardization` ∥ `external-products`

**1** independent pair in a graph of 12 units. The graph is
deliberately near-linear: the pipeline's own data flow, TC-06's precondition and
TE §9.2's fixture ordering leave little genuine independence, and Q7 forbids
manufacturing more by dropping real edges.

**Independence does not mean ready.** Neither member of an independent pair may
be described as free to begin while it carries a governance restriction — an
unsigned amendment, an unresolved locked-test authorization, or a Phase 1
boundary it would breach. `unit-of-work.md` § Blocker register carries BLK-01
through **BLK-09**, each naming its affected artifacts, owning unit, downstream
units, required resolution, approval authority and status. *(Corrected 2026-08-23
from **BLK-07**: BLK-08 and BLK-09 were registered on 2026-08-23 and this span
sentence was not extended with them. Count derived from the register's `### BLK-0…`
headings — nine — rather than carried.)* **Nine of the twelve units
carry an open blocker row, owned or inherited** — `foundation`,
`inventory-and-registry` and `external-products` carry none. That is the sense in which
"nine" is meant; BLK-01's `config.py` row named *every* unit as a downstream, so
counting downstream mentions of a closed row would give twelve (the downstream-versus-
carried distinction was clarified 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 10).
Structural presence in this graph is not readiness.

> **⚠ "Ten" corrected to nine, 2026-08-23.** The figure was true while BLK-01 was open,
> because `foundation` carried it. **BLK-01 closed on 2026-08-22** and this derived
> count was not re-derived — a closure invalidating a claim that names no blocker ID,
> so no sweep keyed to an ID would ever reach it. Found by a mechanical audit of every
> fact stated in more than one place, after five consecutive review passes each found
> one more instance of this class by reading. Derived from `unit-of-work.md`'s summary
> table, Blocker column matched against `BLK-0[2-9]`: nine of twelve.

BLK-06, added 2026-08-22, named no unit that was not already listed; **BLK-07**,
added 2026-08-22, added `acquisition`, which is why the figure rose to ten while
BLK-01 was open. **BLK-01 is closed** (2026-08-22, `CR-2026-08-22-TE-AMEND`) and its row
is retained in the register as a closed row rather than deleted; BLK-02 through
**BLK-09** are open — **eight** entries. *(Corrected 2026-08-23 from "BLK-02 through
BLK-07": BLK-08 and BLK-09 were registered on 2026-08-23, and this sentence sat four
lines below the "BLK-01 through BLK-09" span corrected in the same paragraph on the
same day. Count derived from the register's `| Status |` rows — eight, every one
beginning `Open` — rather than carried.)*

TE §9.2's fixture ordering is worth separating from TC-06 for the same reason:
TC-06 is an inter-unit edge in the block above, while §9.2 is an intra-unit
ordering contract enforced inside `fixtures-and-reproducibility`'s own
`run_walking_skeleton.py`. Both constrain what may run when; only one is an edge.

## Assumptions & Open Questions

- **[assumption]** `external-products` takes its edge from `inventory-and-registry` rather than from `target-standardization`: the benchmark and comparator need the registry's pinned coordinates and cells, and the driver series are time-indexed with no cell join at all. If `functional-design` finds that IRI generation needs the standardized target's timestamp set rather than the registry's, this edge moves and the one independent pair disappears.
- **[assumption]** `fixtures-and-reproducibility` carries direct edges to nine units for two different reasons, recorded separately in the edge table: seven own a stage script the clean-run sequence invokes, and two (`statistical-inference`, `regimes-diagnostics-reporting`) own none but produce artifacts the clean-run comparison and the traceability matrix consume. Listing only terminal units would have been sparser but wrong, and describing all nine as script-owning — as the first attempt did — was wrong in the other direction.
- **Open.** NFR-PHASE-01's transition-manifest hash-diff test has no module in the §12 tree. It is carried as an acceptance row on `fixtures-and-reproducibility` with `governance-guards` supporting, rather than by inventing a module or a Phase 2 unit.
- **Open, a §12 defect.** The `02` ordinal collision, carried unresolved from `services.md`.
- **None** of the above adopts a reading on a supervisor-owned value.
