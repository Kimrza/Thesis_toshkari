# Component Dependencies — Hourly VTEC Forecasting (TEC_Project Phase 1)

Stage 2.6 (application-design), intent `260813-tec-hourly-forecast`.

## Sources

- Requirements: `../requirements-analysis/requirements.md` — FR-P1-04-1
  (the IRI import allowlist), FR-P1-03-2 (the phase boundary, both limbs),
  FR-P1-04-16, FR-P1-04-17.
- Affirmed practices: `../practices-discovery/team-practices.md` — the §12
  import-boundary rule carried as its own project rule, distinct from the IRI
  data-flow rule.
- Authority: TE v3.3 §12 (the allowlist, stated as an allowlist), §7.0 (the Phase
  1 hard prohibition), §6.2 (the closed input space); Vision v4.3 §7.1.
- Stage answers: Q3, Q8.

## Dependency matrix

Rows import columns. `—` means no import in either direction.
**`X` marks a forbidden edge**, not an absent one: the difference matters,
because a forbidden edge needs a test and an absent one does not.

| ↓ imports → | `data` | `gnss` | `external.iri` `external.gim` | `external.spaceweather` | `features` | `models` | `evaluation` |
|---|---|---|---|---|---|---|---|
| `src/data` | — | **X** | **X** | — | — | — | — |
| `src/gnss` | yes | — | **X** | — | — | — | — |
| `src/external.iri` / `.gim` | yes | — | — | — | — | — | — |
| `src/external.spaceweather` | yes | — | — | — | — | — | — |
| `src/features` | yes | **X** | **X** | yes | — | — | — |
| `src/models` | yes | **X** | **X** | — | yes | — | **X** |
| `src/evaluation` | yes | **X** | **allowed** | — | — | yes | — |
| `scripts/04_build_external_products.py` | yes | — | **allowed** | yes | — | — | — |
| `scripts/*` (all others) | yes | phase-gated | **X** | yes | yes | yes | yes |
| `tests/*` | yes | yes | yes | yes | yes | yes | yes |
| `notebooks/01–04` | yes | — | — | yes | yes | yes | yes |
| `notebooks/00_acquire_phase1_vtec` | — | — | — | — | — | — | — |

**Exactly two importers of `iri.py` and `gim.py`**, as TE §12 states it:
`scripts/04_build_external_products.py` and `src/evaluation/`. Everything else is
forbidden, including `src/data`, `src/gnss`, a training script and a notebook —
which is the correction `IMPL-3` required, because the earlier denylist form
covered only `features` and `models` and left every other module free.

**`notebooks/00_acquire_phase1_vtec` imports nothing from `src/`** — it is the
narrowly approved self-contained acquisition interface under D-144. That row is
deliberately empty rather than absent.

## Forbidden edges, and what proves each one

| Edge | Rule | Enforced at run time by | Test |
|---|---|---|---|
| any Phase 1 code → `src/gnss/*` | §7.0 hard prohibition; NFR-PHASE-01 | `phase_contract.assert_phase_boundary` at every stage entry (Q3 = B) | `test_phase_boundary.py` |
| Phase 1 artifact carrying a DCB/STEC/mapping/satellite/arc field | §7.0, produced-field limb | `phase_contract.assert_no_raw_fields` | `test_phase_boundary.py`, second independent result |
| `src/features/*` or `src/models/*` → `iri.py`/`gim.py` | NFR-IRI-01; §12 | import-boundary check | `test_iri_denial.py` |
| any module outside the two permitted → `iri.py`/`gim.py` | §12 allowlist | same check, allowlist form | `test_iri_denial.py` |
| an `iri_*` field or IRI-derived residual reaching training or inference | Vision §7.1 | `features.build_features` raises | `test_iri_denial.py`, **must fail on deliberate injection** |
| a field outside the §6.2 dictionary entering features | FR-P1-04-12 | `features.build_features` raises | `UNTESTED` — no WS/TA row |
| a carried-forward `vtec_lag_*` value | TE §6.2; FR-P1-04-13 | `features.build_features` raises | `UNTESTED` — no WS/TA row |
| a driver repeated outside its own interval, or interpolated | D-10.2; FR-P1-04-17 | `features.build_features` raises | `UNTESTED` — no WS/TA row |
| a support field used as a model input without G-04 approval | TE §6.2; FR-P1-04-16 | `features.build_features` raises | `UNTESTED` — no WS/TA row |
| a December read without a preceding access-log row | FR-P1-05-12; VAL-2 | `locked_test.open_restricted` writes then reads | `test_locked_test_guard.py` |
| December execution before G-05 | FR-P1-05-12 | `splits.materialise_locked_partition` raises | `test_locked_test_guard.py`, WS-18 |
| `src/models` → `src/evaluation` | dependency direction | none needed — inverted import would be a cycle | — |

**Five of these have no §16/§19 row.** They are in `requirements.md`'s untested
list, and they are exactly the leakage paths a governance board flagged as
"criterion states it, nothing tests it". This design makes each one a **raise at a
named call site**, so a test *can* assert it; writing those criteria is a
`requirements.md` change, not this stage's work.

## Why the guard is at run time and not only in tests

Q3 = B. `project.md` § Mandated requires the critical test set to run **inside the
Kaggle session** before any governed run executed there, precisely because a
Kaggle session carries no git working tree, a commit hook cannot fire, and a local
suite run proves nothing about the environment the governed run executes in.

The same reasoning applies to the prohibition itself. A test that would have
failed is worth nothing in a session where tests were not run. So
`assert_phase_boundary` sits in the run path, called once per stage entry, and
the test suite becomes the **second** independent check rather than the only one.

The rejected alternative — an import-time raise inside `src/gnss/rinex.py` itself
— is recorded in ADR-02: it cannot be bypassed by forgetting a call, but it
inverts the dependency by making a Phase 2 module conditional on Phase 1 state,
and it requires the active phase to be discoverable at import time, which means a
global. `phase_contract.py` is the module §12 already designates for the boundary.

## Data flow

```
configs/ ──► data.config ──► every stage (snapshot + hashes + seeds)
                 │
provider files ──┴──► data.prepared ──► Phase 1 target rows (D-17 contract)
                                              │
GFZ / Kyoto / Canada ──► external.spaceweather┤
                                              ▼
                          features.availability ──► features.build
                                              │        (matrix + tensor,
                                              │         one window definition)
                                              ▼
                                      data.splits (F1–F4, embargo)
                                              │
                                              ▼
                                        models.train ──► per-seed predictions
                                              │              │
                                              │              ▼
                                              │      models.three_seed_mean
                                              │              │
IRI / GIM ──► external.iri/.gim ──────────────┼──────────────┤
   (evaluation time only, onto the frozen mask)              ▼
                                              └──► evaluation.masks
                                                          │
                                        ┌─────────────────┼─────────────────┐
                                        ▼                 ▼                 ▼
                                evaluation.metrics  .bootstrap        .regimes
                                        │                 │                 │
                                        └────────► reports, figures ◄───────┘
```

**Text fallback.** Configs flow through one loader into every stage. Provider
files become Phase 1 target rows under D-17's contract. Drivers arrive from GFZ,
Kyoto and the Canadian archive, pass the availability matrix, and join the target
in feature construction, which emits one matrix and one tensor from a single
window definition. Splits partition into F1–F4 with the embargo. Models train and
produce per-seed predictions, then their element-wise mean. **IRI and GIM enter
only here, at evaluation time, onto the already-frozen comparison-wide mask** —
never upstream. Metrics, bootstrap and regimes read the masked predictions and
feed the reports.

The single most important property of that diagram: **there is no arrow from
`external.iri` or `external.gim` into anything left of `evaluation.masks`.** That
absence is NFR-IRI-01, and `test_iri_denial.py` must fail when an arrow is drawn.

## Shared resources

| Resource | Owner | Shared with | Contention |
|---|---|---|---|
| `configs/` (four files) | `data.config` | read-only by all | none — one loader, snapshot per run |
| `experiment_registry.jsonl` | every stage script | all | **append-only**, so concurrent appends do not corrupt; this is why Q5 = C chose it |
| `experiment_registry.csv` | `07_evaluate_and_report.py` | human readers | derived; regenerated, never merged |
| `evidence/locked_test_restricted/` | `data.locked_test` | nothing else may construct a path into it | serialised through one chokepoint |
| release directories | `data.release` | read-only by later stages | write-protected or new version; never overwritten |
| the fixture manifests | `run_walking_skeleton.py` | tests | read-only; **currently blocked** for `plumbing_7day` |
| `PYTHONHASHSEED` | the process environment | all | set before interpreter start (FU-1 = D) |

**No database, no lock file, no message queue, no shared mutable state between
stages.** Stages communicate through hashed, released artifacts. That is what
makes the clean-run contract testable: a stage's inputs are identified by release
ID and verified by hash, so a stage cannot silently consume a stale artifact from
a previous run.

## Assumptions & Open Questions

- **[assumption]** The import-boundary check has **no owning §12 module**. `IMPL-13` recorded that authority-level silence, and FR-P1-04-1 carries it as a note. This design places the *assertion* in `features.build` and the *check* in `test_iri_denial.py`, and does not invent a module to own it.
- **[Q8]** `src/gnss` rows appear in the matrix so the forbidden edges are explicit, not because this stage designs those modules. Their internals are Phase 2 work.
- **Open.** Five forbidden edges have no §16/§19 row. Listed above and in `requirements.md`'s untested list.
- **Open.** `plumbing_7day`'s fixture manifest is blocked on a supervisor decision.
