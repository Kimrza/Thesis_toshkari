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
| a field outside the §6.2 dictionary entering features | FR-P1-04-12 | `features.build_features` raises | **TA-33** (`Pending`) |
| a carried-forward `vtec_lag_*` value | TE §6.2; FR-P1-04-13 | `features.build_features` raises | **TA-34** (`Pending`) |
| a driver repeated outside its own interval, or **shifted to a neighbouring hour** | D-10.2; FR-P1-04-17 | `features.build_features` raises `AlignmentError` | **TA-36** (`Pending`), `tests/test_feature_leakage_guards.py` |
| a driver **interpolated**, at any stage | D-10.2; FR-P1-04-17 | **static source check, not a runtime raise** — an interpolated value is indistinguishable at runtime from a genuine one | **TA-36** (`Pending`), same module, grep limb |
| **a transform used on a frame built for another partition** | **NFR-LEAK-01; BLK-04** | **`features.build_features` raises `LeakageError`** when `transform.partition_id != spec.partition_id` — an **identity** check, because the training ranges nest and no containment rule can separate them (**ADR-11**). **One enumerated exception:** `REFIT` → `DEC` with `role == "score"`, the G-06 apply | `test_train_only_transforms.py` — enumerates **every** other ordered pair of the six ids; **no WS/TA row covers the identity check itself**, and NFR-LEAK-01's evidence is owed to the Supervisor at G-04/G-05 |
| **a `REFIT` transform against a `DEC` frame with `role == "train"`** | **NFR-LEAK-01; Vision §5.3** | **raises** — the carve-out permits scoring December, never fitting on it | `test_locked_test_guard.py`, `test_train_only_transforms.py` |
| **a window reaching before its frame's `scored_start`** | **FR-P1-04-5; FR-P1-04-13** | **excluded and counted**, never silently dropped — `lead_in_hours` was removed 2026-08-23 rather than let a window cross the Nov/Dec boundary | `test_split_embargo.py`; **1 December is not scored, and the locked test covers 30 days** |
| **a transform fitted on anything but a partition's own training rows** | **NFR-LEAK-01** | **`features.fit_transforms` raises** — it takes the `Partition` alongside the `FeatureBundle`, so it can compare the bundle's scored range against that partition's training range and reject a full-dataset fit at run time; also raises when `role != "train"`, when `partition_id` disagrees, or when the bundle is already transformed. The check is an **executable raise, not a type-level impossibility** — the earlier "no argument to be passed as" claim is withdrawn (ADR-11) | `test_train_only_transforms.py` |
| **an untransformed bundle reaching training or scoring** | **NFR-LEAK-01** | **`06`/`07` raise** on `transform_id is None` — the three-call build sequence leaves one live in-process | `test_train_only_transforms.py` |
| **a bundle scored against the wrong partition's transform, across the `05`→`06` handoff** | **NFR-LEAK-01** | **`07` asserts** `spec.partition_id`, `spec.role == "score"` and `transform_id` off the **`FeatureBundle`** — the stamp travels with the data rather than in a side-car manifest | `test_train_only_transforms.py` |
| a support field used as a model input without G-04 approval | TE §6.2; FR-P1-04-16 | `features.build_features` raises | **TA-35** (`Pending`) |
| a December read without a preceding access-log row | FR-P1-05-12; VAL-2 | `locked_test.open_restricted` writes then reads | `test_locked_test_guard.py` |
| December execution before G-05 | FR-P1-05-12 | `splits.materialise_locked_partition` raises | `test_locked_test_guard.py`, WS-18 |
| `src/models` → `src/evaluation` | dependency direction | none needed — inverted import would be a cycle | — |

**One of these has no §16/§19 row** — the identity check in the transform row, whose
test module is named but which no acceptance row covers. **Corrected 2026-08-23; the
figure read "Five".**

*Check against this table as it now stands — reproducible.* Counting rows of the
table above that carry the phrase *"no WS/TA row"* gives **1**: the transform-identity
row, where the phrase is an embedded clause rather than the whole Test cell. No row
carries the literal `UNTESTED` any more. That is the figure this paragraph states.

*How it got there, counted against the **pre-correction** text and labelled as
history so the numbers below are not mistaken for a check on the current table.*
Before 2026-08-23 the table carried the literal `UNTESTED` in **3** rows —
FR-P1-04-12, FR-P1-04-13 and FR-P1-04-16 — and the phrase *"no WS/TA row"* in **4**,
the fourth being the identity check's clause, which is the one that survives. All
three of the first group gained acceptance rows on **2026-08-22** — **TA-33**,
**TA-34** and **TA-35** respectively — under `CR-2026-08-22-LEAKAGE-TA`, the same
change record that moved the untested-requirement total from 40 to 36 and that added
**TA-36** to FR-P1-04-17, which this table already cited. Correcting those three left
**1**.

*Rewritten 2026-08-23 after the advisory reviewer found the derivation stated in the
present tense inside the corrected file, where its counts no longer reproduce —
`project.md`'s count-derivation rule broken by the sentence written to satisfy it.
The figure was independently verified as correct both times; only the method was
unverifiable.*

**Why the stale rows survived a sweep that reached their sibling.** The 40 → 36
correction was scoped to the file that carried the wrong number. FR-P1-04-17's row
here was right only because it was written after the change record; the other three
predate it and no sweep asked which *other* artifacts asserted the same superseded
status. That is the failure mode `project.md` § Way of Working names — sweeping for
the numeral rather than for the claims it supported — and it is the fourth instance
in this stage.

The remaining gap is real and unchanged in substance: no acceptance row covers the
identity check itself, and NFR-LEAK-01's evidence is owed to the Supervisor at
G-04/G-05. This design makes it a **raise at a named call site**, so a test *can*
assert it; writing that criterion is a `requirements.md` change, not this stage's
work. The three `Pending` rows above are likewise rows that exist, not tests that
have run.

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
- **Open.** **One** forbidden edge has no §16/§19 row — the transform-identity check. *Corrected 2026-08-23 from "Five": FR-P1-04-12, FR-P1-04-13 and FR-P1-04-16 gained TA-33, TA-34 and TA-35 on 2026-08-22, so they are no longer in `requirements.md`'s untested list. Derivation in § Forbidden edges.*
- **Open.** `plumbing_7day`'s fixture manifest is blocked on a supervisor decision.

---

*Finalized 2026-08-23 under the stage's revision-4 completion pass. The NFR-LEAK-01
enforcement row was corrected in this pass: the full-dataset fit is rejected by an
**executable raise** — `fit_transforms` holds the `Partition` and compares ranges —
not by the absence of an argument to pass. That earlier claim is withdrawn; see
`decisions.md` ADR-11 § ⚠ THE "UNREPRESENTABLE" CLAIM IS WITHDRAWN. Also open, and
visible at the gate: `src/evaluation` has no route to `Transform.inverse`, which
`ABL-DIFF` requires — this matrix carries no `features` edge for it and none should
be added without the design naming the lookup.*
