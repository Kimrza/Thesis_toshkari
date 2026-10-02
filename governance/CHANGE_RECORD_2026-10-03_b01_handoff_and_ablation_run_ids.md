# Change record CR-2026-10-03-B01-HANDOFF-AND-ABLATION-IDS

**Status: PROPOSED. Nothing in this record is adopted.** It drafts two register acts for the
Student: proposed D-91 and proposed D-92. The code that the drafts depend on is committed. It
is built so that nothing it enables runs until the matching D-number exists in
`evidence/DECISIONS.md`:

- the cross-environment receipt path refuses on the register;
- the ablation runs refuse on `TBD` in `configs/experiment.yaml`.

The agent writes neither `evidence/DECISIONS.md` nor the `run_id` / `registered_at` fields
(project.md `code-generation:c31`, `c5`; `configs/experiment.yaml` lines 314-318).

## Part 1: the B-01 IRI environment blocker

### Root cause (measured from the code, not inferred)

- D-83 revision 8 item 1 confines B-01 generation and `verify_runtime` to (b) `b01_iri`. Every
  stage script, the confirmatory set and the evaluation-time IRI join run in (a) `tec-thesis-311`.
- `scripts/04_build_external_products.py` treats `--generate-benchmark` as a full-year job: it
  is outside the `full_year_job=not (...)` exemptions in `main()`. It therefore calls
  `require_receipts_for_snapshot` (TE 9.2: both fixtures pass before any full-year job).
- `src/data/fixture_gate.verify_receipt` accepts a receipt only when
  `environment_identity(recorded_lock) == environment_identity(caller_lock)`. That identity
  covers the requirements hash, pip freeze, runtime versions, code commit, config hashes,
  platform and nondeterministic ops (SD-X-02).
- Fixture receipts exist in (a) and (c) only. D-83 permits (b) nothing but B-01 work, so the
  fixtures cannot be run in (b) without amending D-83.

So a governed January-November generation in (b) refuses by construction. This is a conflict
between two governed rules: D-83's environment confinement and SD-X-02's receipt binding.

### Answer to "A or B"

- **Not A.** No rule requires the IRI calculation to run in the receipt-producing
  environment. D-83 requires the opposite, that it runs in (b), and (a) consumes it.
- **B, with one governed residue.** The architecture already moves the artifact across. D-83
  revision 7 §A7 transfers B-01 receipts from (b) to (a) through `/mnt/c`, re-verifies them,
  and binds assembly to the admitted receipt. That machinery covered December only.
  - What B does NOT dissolve is TE 9.2's gate on the generation run itself.
  - Moving the gate to the consumption point in (a) would weaken "before any full-year job"
    for the expensive 24,048-call generation. The agent therefore did not do it.
  - Accepting (a)'s receipts in (b) changes what a receipt binds to. That is a register act,
    hence proposed D-91.

### What was implemented (`src/data/b01_handoff.py`; script 04; tests)

1. **Admission in (a): ungated, strictly additive.** It runs as
   `04_build_external_products.py --admit-b01-receipt <provenance>`, in (a), where the normal
   TE 9.2 receipt gate applies. It re-verifies:
   - the transfer hashes (rows, provenance, SHA-256 manifest);
   - that the generating environment is `b01_iri`, in a recorded lock that hashes to the
     provenance's own `environment_lock_hash`;
   - the code commit and config hashes, with data.yaml allowed to differ only under `gates`,
     as D-83 rev 8 item 4 already allows;
   - the phase_id and that the months are exactly 1-11;
   - exact grid coverage against `iri.build_target_grid` (no missing point, no extra point);
   - that there are no duplicate `(station_id, target_time_utc)` pairs;
   - that every `ok` value is a finite, non-negative TECU number.

   Error rows are counted and recorded as a completeness shortfall, never refused and never
   imputed. It writes `evidence/b01_admission/jan_nov_admission_<phase_id>.json` once. The
   marker names `generating_environment_id` and `admitting_environment_id` separately.
2. **Assembly now requires that admission.** `_assemble_benchmark` refuses unless the
   January-November half is the receipt (a) admitted, byte for byte. This strengthens an
   existing path; the existing W-1/W-2 and PV-09 tests were updated to admit the half first.
3. **Provenance now records the generating lock.** `_generate_benchmark` writes
   `environment_lock` (the eight items), `environment_id` and a summary of `receipts_gate`
   into `b01_provenance_*.json`, so that (a) can check identity rather than trust a hash.
4. **The cross-binding in (b) is gated.** `--receipts-environment tec-thesis-311` together
   with `--generate-benchmark` calls `require_cross_environment_receipts`. It refuses unless a
   `## D-<n>` section of `evidence/DECISIONS.md` carries the literal
   `cross_environment_receipt_binding: b01_iri <- tec-thesis-311`. When it is authorized:
   - every `verify_receipt` integrity check still runs against the receipt's own lock: the
     manifest frozen and in force, PASS, the self-hash, the append-only registry row, and the
     manifest bound into the lock;
   - the caller must be `b01_iri`, and the receipts must have been written in
     `tec-thesis-311`;
   - the code commit, config hashes and platform must be equal;
   - only the requirements hash, pip freeze and runtime versions may differ, because they
     differ by design (D-49).

   Without the flag, (b) behaves exactly as before.

### Tests (run in this session; the venv is Python 3.11.15 with pyyaml, numpy, pandas, pyarrow and pytest, not the governed lock)

- `tests/test_b01_handoff.py`: **42 passed.** Coverage:
  - the cross-binding refuses with no decision, with a missing register, from a caller
    outside (b), for a receipt written outside (a), for a wrong commit, config or platform,
    for missing receipts, and for an edited receipt; it passes under a decision;
  - admission refuses a missing provenance, missing rows, a missing manifest, corrupt rows,
    corrupt provenance, the wrong generating or admitting environment, an edited lock, a
    wrong commit, a non-data config difference, and a non-`gates` data.yaml difference;
  - admission refuses incomplete coverage, unexpected rows, duplicate timestamps, NaN, inf,
    negative, string, null and boolean values, an unknown status, a valued error row, an
    error-count mismatch, the wrong months or phase, a row from another phase, a second
    admission, and a substituted half;
  - error rows are recorded and not refused;
  - identical rows hash identically.
- `tests/test_external_drivers.py`: **97 passed**, including the updated W-1/W-2 and PV-09
  assembly tests.
- `ruff check` is clean on the new files. Script 04 keeps its 3 pre-existing B905 findings,
  the same count as before this change.

**Owed in the governed environment:** the full suite in (a) and in (b) at the commit carrying
this change. A code change invalidates both fixture receipts (SD-X-02), so the plumbing and
scientific verification runs must be repeated at the new commit before any full-year job.
That cost applies to any code change, this one included.

### Proposed D-91 text (for the Student to append verbatim)

```markdown
## D-91 — B-01 generation in `b01_iri` accepts the `tec-thesis-311` fixture receipts

**Decision date:** <date>. **Decided by:** the Student (D-83's environment owner).

**Problem.** D-83 rev 8 item 1 confines B-01 generation to (b) `b01_iri`; TE 9.2 gates every
full-year job, `--generate-benchmark` included, on both fixture receipts; and SD-X-02 binds a
receipt to the caller's whole environment identity. Receipts exist in (a) and (c) only, so the
January-November B-01 cannot be generated (CR-2026-10-03-B01-HANDOFF-AND-ABLATION-IDS).

**Decision.** A `--generate-benchmark` run in `b01_iri` accepts the two fixture receipts
written in `tec-thesis-311` when, and only when:
- every `verify_receipt` integrity check passes against the receipt's own lock;
- the caller's `environment_id` is `b01_iri` and the receipts' is `tec-thesis-311`;
- `code_commit`, `config_hashes` and `platform` are equal.

The requirements hash, pip freeze and runtime versions may differ, because (b) is a different
environment by design (D-49). No other job, and no other environment pair, is affected.

cross_environment_receipt_binding: b01_iri <- tec-thesis-311

**Consumption.** The January-November half is admitted in (a) by `--admit-b01-receipt`, under
(a)'s own TE 9.2 gate, before assembly or any evaluation join consumes it. Generating and
admitting environments are recorded separately.

**Effect on leakage / uncertainty / comparability / claim.**
- Leakage: none; B-01 is evaluation-time only (NFR-IRI-01).
- Uncertainty: none.
- Comparability: none.
- Claim: none.
```

## Part 2: ablation run IDs (TE 7.2)

### Inventory (from `configs/experiment.yaml` lines 320-362 and `src/models/train.py`)

| Ablation | Change | Phase 1 | Constraint |
|---|---|---|---|
| ABL-NODOY | drop doy_sin, doy_cos | yes | |
| ABL-DIFF | first-difference target, inverse to TECU before metrics | yes | refuses while no inverse exists (D-27) |
| ABL-NOSW | drop the six forecast-safe space-weather features | yes | |
| ABL-HIST48 | 48 h window / 48-step sequence | yes | only after the primary freeze |
| ABL-ZENITH | zenith-weighted aggregate | **no**, Phase 2 | refused in Phase 1 |

Five are named and four are reachable in Phase 1. Folds are F1-F4, January-November only.
The seeds are the confirmatory seeds in `seeds.yaml` (1337, 2024, 7). The environment is (a)
`tec-thesis-311`.

### Convention and proposed IDs

The existing registry IDs are minted at execution as `<stage>-<UTC>-<uuid8>`, so they cannot
be predeclared. The proposed registered ID is therefore a function of the ablation identity
only: `ablation-<ablation id, lower case>`. Each execution is a child run
`<run_id>/<fold_id>/seed-<seed>`. No result, score or timestamp enters the ID.

| Ablation | Proposed `run_id` |
|---|---|
| ABL-NODOY | `ablation-abl-nodoy` |
| ABL-DIFF | `ablation-abl-diff` |
| ABL-NOSW | `ablation-abl-nosw` |
| ABL-HIST48 | `ablation-abl-hist48` |
| ABL-ZENITH | `ablation-abl-zenith` |

**Collision check.** The committed `artifacts/registry/experiment_registry.jsonl` has **0**
run IDs beginning `ablation-`. The laptop's working-tree registry has uncommitted rows, and
the same check must be re-run there before adoption; `assert_registration` does it.

`registered_at` must be the UTC instant of the Student's adoption, strictly before the primary
freeze (`assert_ablation_runnable`). The agent does not choose it.

### Implemented (`src/models/ablation_registry.py`; `tests/test_ablation_registry.py`, 17 passed)

`canonical_run_id`, `child_run_id` and `assert_registration`. The last refuses:
- a TBD `run_id` or `registered_at`;
- a missing or duplicated ablation;
- a duplicate, swapped or mismatched run ID;
- a collision with an existing registry run or child run;
- a non-UTC or non-ISO `registered_at`.

One test asserts that the live config is still `TBD` and therefore refuses. That test flips to
asserting a pass once the act is adopted.

### Proposed D-92 text and config edit

```markdown
## D-92 — TE 7.2 ablation run-ID registration

**Decision date:** <date>. **Decided by:** the Student. Registers the five TE 7.2 ablations
with run IDs derived from identity only (`ablation-<id lower case>`), before the primary
freeze and before any ablation result exists:

- ABL-NODOY `ablation-abl-nodoy`;
- ABL-DIFF `ablation-abl-diff`;
- ABL-NOSW `ablation-abl-nosw`;
- ABL-HIST48 `ablation-abl-hist48`;
- ABL-ZENITH `ablation-abl-zenith` (Phase 2 only).

`registered_at`: <UTC instant>. Executions are child runs `<run_id>/<fold>/seed-<seed>` on
F1-F4 with the seeds.yaml confirmatory seeds, in `tec-thesis-311`. ABL-DIFF stays refused
until the D-27 inverse exists; ABL-HIST48 runs only after the primary freeze. Collision check:
`src.models.ablation_registry.assert_registration` against the registry at adoption.

**Effect:** none on leakage, uncertainty or claim; comparability is unchanged (identical folds,
masks and tuning budget, TE 7.2).
```

The config edit is in `configs/experiment.yaml`. For each of the five entries, replace
`run_id: "TBD — freeze gate"` with the ID above and `registered_at: "TBD — freeze gate"` with
the same UTC instant, ending in `+00:00`. The commit message cites D-92 (team.md § Way of
Working).
