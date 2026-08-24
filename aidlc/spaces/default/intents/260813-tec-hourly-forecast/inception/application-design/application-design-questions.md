# Application Design — Questions

Stage 2.6 (application-design), intent `260813-tec-hourly-forecast`.
Depth: Comprehensive. Scope: `research-pipeline-governed`.

**What is already fixed, and therefore not asked.** Technical Environment §12
fixes the repository layout down to individual files: six `src/` packages
(`data`, `gnss`, `external`, `features`, `models`, `evaluation`), every module
named, most with a stated responsibility; nine phase-aware stage scripts; exactly
four configs; five notebooks. §8.3 fixes Python-only with TensorFlow/Keras as the
sole NN stack. TC-03c fixes two platforms. TC-03e bars scientific constants from
source. The affirmed team practices fix `ruff`, the `NN_verb_noun.py` convention,
and the `--config configs/` CLI. None of that is re-opened here.

**What is not asked because it does not exist.** This is a single-process,
CPU-only, offline batch pipeline. There is no network surface, no deployable
service, no database and no user interface, so the stage's default questions on
sync-versus-async communication, REST/gRPC/events, service scaling, cross-service
data ownership and UI component structure have nothing to attach to. `services.md`
will describe the nine stage scripts as pipeline stages; the UX perspective is
recorded `N/A` with that reason.

What follows targets the three things §12 genuinely leaves open: **the method
surface** (§12 fixes no signature), **the enforcement mechanism for each hard
boundary** (§12 names the tests but not the runtime guard), and **the
responsibilities §12's tree assigns to no module at all**.

Answer each by filling the `[Answer]:` tag with the option letter.

---

## Q1 — How deep should the method surface go?

§12 gives each module a name and mostly a one-line responsibility. It fixes no
signature. `component-methods.md` has to choose a depth, and `functional-design`
(3.1) runs later per unit and will specify business rules regardless.

- A. **Full signatures with types for every public function in all six packages** — names, parameter types, return types, raised exceptions.
  *Impact:* the largest artifact and the most rework if a signature proves wrong at 3.1; strongest input to `units-generation` (2.7) for drawing unit boundaries.
- B. **Full signatures only for cross-package boundary calls; names and one-line purposes for intra-package functions.**
  *Impact:* pins exactly the contracts that a leakage or phase-boundary defect would travel across, and leaves internal shapes to 3.1. Smaller artifact, and the parts most expensive to get wrong are still fixed.
- C. **Names and purposes only, no signatures anywhere** — defer all typing to 3.1.
  *Impact:* least rework, but 2.7 draws unit boundaries with no contract to cut along, and the IRI-denial and phase-boundary contracts stay unspecified until Construction.
- D. **Full signatures for the packages that carry a hard rule (`features`, `models`, `evaluation`, `data`), names only for `gnss` and `external`.**
  *Impact:* `gnss` is Phase 2 and barred from Phase 1 execution, so its interface is the least urgent; `external` is small. Concentrates precision where NFR-LEAK-01, NFR-IRI-01 and NFR-PHASE-01 apply.
- X. Other (please specify)

**Recommendation: B.** Every defect this project's governance has actually caught
travelled across a package boundary — IRI reaching features, a raw module reaching
Phase 1, a carried-forward lag reaching the model. Those are the contracts worth
fixing now. Intra-package shapes are cheap to change at 3.1 and expensive to guess
today.

[Answer]: B

---

## Q2 — Where does config loading, snapshotting and hashing live?

§13.1 requires every run to snapshot and hash all four configs. §12's tree
assigns this to **no module**, and `team.md` § Code Style states there is no
seventh `utils` package to put it in. TC-03e bars scientific constants from
source, so wherever the loader lives it must read values rather than hold them.

- A. **`src/data/release.py`** — it already owns SHA-256 hashing and release manifests, so the config snapshot becomes one more hashed artifact.
  *Impact:* no new module, and hashing logic stays in one place (the team practice already consolidates the triplicated SHA-256 helper here). Mixes "what a run consumed" with "what a run produced" in one module.
- B. **A new `src/data/config.py`**, added to §12's tree as a recorded amendment under Vision §15.2 change control.
  *Impact:* clean single responsibility, and the amendment precedent already exists (`test_acquisition_window.py` was added to §12's tree and countersigned 2026-08-16). Costs a change record and, on that precedent, a countersignature.
- C. **Each of the nine stage scripts loads and hashes its own configs.**
  *Impact:* no shared module and no amendment, but nine copies of the snapshot-and-hash logic, and §13.7's exact-equality requirement then depends on nine implementations agreeing.
- D. **`src/data/phase_contract.py`** — it already owns boundary and transition-manifest hashes, so config hashes join the other governed hashes.
  *Impact:* keeps every hash that a freeze gate checks in one module. Widens a module whose §12 responsibility is specifically the phase boundary.
- X. Other (please specify)

**Recommendation: B.** A and D both work by widening a module past its stated
responsibility, and §12's responsibilities are what the phase-boundary and
release tests key on. The amendment path has a precedent in this project and
leaves an auditable record of the tree changing, which is exactly what a reviewer
reconstructing the structure later will need.

[Answer]: B

---

## Q3 — How is the Phase 1 import prohibition enforced at runtime?

FR-P1-03-2 requires **two independent pass/fail results**: an import limb (no
raw-processing module is reachable from a Phase 1 command) and a produced-field
limb. `tests/test_phase_boundary.py` covers both in test. The question is what,
if anything, enforces the import limb when the pipeline actually runs.

- A. **Test-only.** `test_phase_boundary.py` fails if an import is introduced; no runtime guard.
  *Impact:* satisfies §7.0 as written and adds no code to the run path. A Phase 1 run in an environment where tests were not run has nothing stopping it.
- B. **A runtime guard in `src/data/phase_contract.py`**, called by every phase-aware stage script at entry: given `--phase 1`, it asserts the raw modules are absent from `sys.modules` and refuses to proceed.
  *Impact:* the prohibition holds in the Kaggle session too, where `team.md` records that a commit hook cannot fire. One guard, called in nine places.
- C. **Import-time guard inside the raw modules themselves** — `src/gnss/rinex.py` and `calibration.py` raise on import when the active phase is 1.
  *Impact:* impossible to bypass by forgetting a call, since the failure is at the import itself. Puts phase logic inside Phase 2 modules and needs the active phase discoverable at import time.
- D. **B and C together**, with the test suite as the third check.
  *Impact:* strongest, and matches the project's stated methodology of pairing every hard rule with a negative control. Most moving parts for one prohibition.
- X. Other (please specify)

**Recommendation: B.** `project.md` § Mandated requires the critical test set to
run **inside the Kaggle session** precisely because a local test run proves
nothing about the environment a governed run executes in — the same reasoning
says the prohibition should hold at run time, not only at test time. C is
tempting but inverts the dependency, making a Phase 2 module conditional on phase
state; B keeps that knowledge in the module §12 already designates for the
boundary.

[Answer]: B

---

## Q4 — What guards the locked December test set at run time?

`tests/test_locked_test_guard.py` is mandated, WS-18 and TA-18 evidence it, and
D-15 relocated every December-bearing artifact under
`evidence/locked_test_restricted/`. FR-P1-05-12 requires the guard to block
pre-G-05 December execution, record every access **before** the read, and set
`locked_test_accessed`.

- A. **A path-level guard**: any read under `evidence/locked_test_restricted/` goes through one function that checks the G-05 signature, writes the access-log row, then opens the file.
  *Impact:* one chokepoint, and it matches what D-15 actually built — a declared location with a machine-checkable invariant. A read that bypasses the helper bypasses the guard.
- B. **A fold-level guard in `src/data/splits.py`**: the December partition is only materialised when a G-05 token is present.
  *Impact:* sits where the locked test is conceptually defined, and covers the modelling path. Does not cover a non-execution read, which VAL-2 established is exactly the case the access log was missing.
- C. **Both**, with the path guard owning the access log and the fold guard owning execution.
  *Impact:* separates the two obligations the artifact already keeps distinct — the required pre-G-05 coverage audit (a read) versus the one-shot evaluation (an execution). More surface to keep consistent.
- X. Other (please specify)

**Recommendation: C.** The project's own history argues for it: the access log
was found incomplete because non-execution reads had no requirement (VAL-2), and
the coverage audit is *required* before G-05 while the metrics run is barred until
after it. One guard cannot express both without conflating a permitted read with a
prohibited execution.

[Answer]: C

---

## Q5 — How does the experiment registry achieve atomic or append-safe writes?

NFR-AUD-01 requires registry writes to be atomic or append-safe, failed and
aborted runs to stay visible with status and reason, and silent reruns to be
prohibited. TA-10 gates it. §13.4 allows CSV or JSONL.

- A. **Append-only JSONL**: one line per run, opened in append mode, never rewritten; status transitions append a new row referencing the run ID.
  *Impact:* append-safe by construction and crash-tolerant; a failed run's row cannot be silently removed. Reading current state means folding the rows.
- B. **CSV rewritten via temp-file-plus-rename** on every update.
  *Impact:* one row per run and trivially readable. A crash mid-write leaves the temp file, and the rename must be verified atomic on both platforms.
- C. **JSONL append for run events plus a derived CSV** regenerated from it for human reading.
  *Impact:* the append-only log is authoritative and the CSV is disposable, so a corrupted CSV is never a data loss. Two artifacts to keep in step, and the derived file needs its own hash.
- X. Other (please specify)

**Recommendation: C.** A alone satisfies the NFR; the derived CSV is what makes
the registry reviewable at a gate, which §13.4 and TA-10 both assume a human does.
Marking the CSV derived also keeps it inside the two-tier error posture the team
affirmed — a completeness shortfall in a derived artifact is recorded, not fatal.

[Answer]: C

---

## Q6 — Where is determinism plumbed?

NFR-DET-01 and TC-21 require fixed seeds from `seeds.yaml`, the three-seed
element-wise mean as the confirmatory prediction, and nondeterministic operations
recorded where determinism cannot be guaranteed. §12 assigns this to no module.
Python, NumPy and TensorFlow each need seeding, and TensorFlow additionally needs
op-level determinism configured before graph construction.

- A. **One `seed_everything(config)` in `src/models/train.py`**, called at training entry.
  *Impact:* sits where the seeds matter most. Misses `src/evaluation/bootstrap.py`, which needs seed 20221201 independently, and anything stochastic in feature construction.
- B. **A seeding helper wherever Q2 puts config loading**, called by every stage script at entry, with the applied seeds echoed into the run's environment lock.
  *Impact:* one call site per script and the seeds land in the §13.1 lock automatically, which REQ-ENG-10 requires. Couples seeding to config loading.
- C. **Per-consumer seeding**: `train.py` seeds the frameworks, `bootstrap.py` seeds its own generator from the frozen 20221201, and each records what it applied.
  *Impact:* each consumer owns the seed it is accountable for, and the bootstrap's independence from the training seeds is explicit — which matters, because that seed must not drift with a model reseed. No single chokepoint.
- X. Other (please specify)

**Recommendation: B plus C's bootstrap carve-out.** The environment lock is the
reason to centralise: REQ-ENG-10 requires every run to capture what it applied,
and a per-consumer scheme makes that capture nine separate obligations. The
bootstrap seed stays separately owned because Vision §8.6 freezes it independently
and a model reseed must not touch it.

[Answer]: X — Use centralized stage-level deterministic configuration, with an
independent bootstrap-seed carve-out.

Implement a shared determinism helper alongside the configuration
loading infrastructure selected in Q2. At the start of every relevant
stage, load the approved seed values from seeds.yaml and configure
Python, NumPy, and TensorFlow as applicable.

Enable TensorFlow operation determinism before model or graph
construction, and apply any required process-level settings early
enough to be effective. Record the applied seeds, framework versions,
determinism settings, execution environment, and any operations for
which deterministic behavior cannot be guaranteed in the run’s
environment lock and experiment registry.

Train the model using the three approved model seeds. Preserve the
individual predictions and construct the confirmatory prediction as
their element-wise mean, with sample alignment explicitly verified.
Do not select the best seed or substitute a single-seed prediction.

Keep bootstrap randomness independent from model-training randomness.
src/evaluation/bootstrap.py must create its own local random-number
generator using the separately frozen bootstrap seed, 20221201,
obtained from the approved configuration or recorded governance
decision rather than hard-coded as an undocumented scientific
constant. Changing model seeds must never change bootstrap draws.

Where PYTHONHASHSEED or another setting must be established before the
Python interpreter or a framework initializes, enforce that setting in
the stage launcher or process environment and record it; do not claim
that setting it after startup provides equivalent determinism.

Add tests for seed loading, stage-level seed recording, bootstrap
independence, three-seed prediction alignment and averaging,
premature TensorFlow initialization, and explicit reporting of
nondeterministic operations.

---

## Q7 — How do the two platforms differ in the design, given only four configs?

TC-03c fixes exactly two platforms, Kaggle and local. §12 permits exactly four
config files, so a `platform.yaml` is not available. Paths differ
(`/kaggle/working` versus a local tree), credentials differ, and REQ-ENG-3 now
requires every run to record its `platform` field and a manifest for any transfer
between them.

- A. **Environment variables only.** Roots and credentials come from the environment; the four configs stay platform-neutral.
  *Impact:* keeps scientific configuration free of machine detail, which is what TC-03e is protecting, and matches §10's rule that credentials come from platform secret stores or environment configuration excluded from version control. Nothing in the repository documents the expected variables unless `README.md` does.
- B. **A platform block inside `data.yaml`** with a key per platform.
  *Impact:* one committed place to read the layout from. Puts machine-specific paths inside a governed scientific config whose hash is checked every run, so moving a directory changes a governed hash.
- C. **Environment variables for credentials, a small resolved-at-runtime path helper for roots**, with the resolved roots recorded in the run's environment lock.
  *Impact:* credentials stay out of the repository per §10, paths stay out of the governed configs per TC-03e, and the run record still shows where the data actually came from — which is what a reviewer reconstructing a run needs.
- X. Other (please specify)

**Recommendation: C.** B changes a governed config hash when a directory moves,
which makes §13.7's exact-equality check fire on an event that is not a scientific
change. A is nearly right but leaves no record of the roots a given run resolved,
and that record is what makes a cross-platform result reproducible.

[Answer]: C

---

## Q8 — How much of Phase 2's interface do we design now?

Phase 1 is barred from executing `src/gnss/` (§7.0), and NFR-PHASE-01 plus the
phase-transition hash freeze mean Phase 2 must not drift from a Phase 1 protocol.
Those modules are in §12's tree with stated responsibilities.

- A. **Design all six packages fully now, Phase 2 included.**
  *Impact:* the phase-transition manifest has a complete interface to freeze against, and Phase 2 cannot quietly redesign its way around a Phase 1 decision. Specifies modules nobody will run for months, against a target contract (`gnss/target.py`'s ten-field row) whose Phase 1 counterpart D-17 already had to redefine on measured evidence.
- B. **Design Phase 1 fully; for `src/gnss/`, record only the boundary — what Phase 2 must not change, and the interface Phase 1 artifacts present to it.**
  *Impact:* keeps the frozen surface small and honest, and matches D-17's lesson that a Phase 2-shaped contract did not survive contact with the actual Phase 1 product. G-P2 then has less to check.
- C. **Design Phase 1 only; leave `src/gnss/` entirely to a later stage.**
  *Impact:* smallest artifact now. The phase-transition freeze has no recorded interface to compare against, which is what NFR-PHASE-01 exists to prevent.
- X. Other (please specify)

**Recommendation: B.** A invites the exact failure this project already hit once:
TE §6.1's ten-field target row was written for Phase 2's IPP population and proved
unsatisfiable on Phase 1's five-column product, which is why D-17 exists. Freeze
the boundary, not the internals of work no measurement has touched yet.

[Answer]: B — Design the Phase 1 architecture and approved cross-package
interfaces now, while defining only the governed transition boundary
for Phase 2.

For src/gnss/, document module responsibilities and the externally
visible Phase 1-to-Phase 2 interface without prematurely fixing
internal function signatures, implementation details, or unverified
scientific assumptions.

Define the transition contract using actual, evidence-backed Phase 1
artifacts, including their observed schema, artifact identities,
SHA-256 hashes, configuration hashes, approved decisions, provenance,
and any invariants Phase 2 must preserve.

Explicitly distinguish the observed Phase 1 product schema from any
future Phase 2 target schema. Do not impose the Phase 2 ten-field
contract on the Phase 1 five-column product; preserve the D-17
resolution and identify any later schema transformation as Phase 2
work requiring its own evidence and approval.

Require a phase-transition manifest that freezes the approved Phase 1
handoff surface and identifies unresolved Phase 2 design decisions
without silently inventing or freezing unsupported values.

Maintain the Phase 1 prohibition against importing or executing
src/gnss/ modules. Define G-P2 checks around transition-manifest
integrity, schema compatibility, approved configuration continuity,
and preservation of locked-test protections.

Consistent with Q1, specify full signatures for relevant cross-package
boundary calls while leaving intra-package implementation details to
the appropriate functional-design stage.

---

# Follow-up questions

Raised by the Step 4 ambiguity scan. None contradicts an answer above; each is a
consequence of one that collides with something already frozen, and `project.md`
§ Way of Working requires a targeted follow-up rather than a silent
reinterpretation.

---

## FU-1 — `PYTHONHASHSEED` versus §13.2's literal clean-run sequence

Q6 requires process-level settings to be enforced **before** the interpreter
initializes, and explicitly bars claiming that a post-startup assignment is
equivalent. But §13.2's clean-run contract is a **literal command sequence**
beginning `python scripts/run_walking_skeleton.py --config configs/ --fixture
plumbing_7day`, and `test_clean_run.py`, WS-20 and TA-17 all test that sequence
as written. A variable that must precede interpreter start cannot be set by code
the interpreter is already running.

- A. **Amend §13.2's commands** to carry the variable (`PYTHONHASHSEED=0 python scripts/…`) under a Vision §15.2 change record.
  *Impact:* the documented sequence stays the whole truth and the setting is genuinely enforced. Edits an authority document's frozen command list, and `test_clean_run.py` must assert the new form.
- B. **Each stage script re-execs itself** with the variable set when it finds it unset, leaving §13.2's commands verbatim.
  *Impact:* no authority change and the guarantee holds however the script is invoked, including a bare `python scripts/06_train_and_predict.py`. A re-exec is a surprising control flow to a reader and must be recorded in the run log so it is not mistaken for a double run.
- C. **Set it in the platform environment** (Kaggle session setup, local shell) and only *record* it per run; the repository does not enforce it.
  *Impact:* smallest change. Weakens Q6's "enforce" to "record", and a run started in a shell without it produces different hash ordering with nothing objecting — the failure mode Q6's last paragraph was written to prevent.
- D. **B for the nine stage scripts, plus A's amendment** so the documented sequence and the enforcement agree.
  *Impact:* belt and braces; the sequence reads correctly and the guarantee does not depend on the reader having read it. Two changes to keep in step.
- X. Other (please specify)

**Recommendation: B.** It satisfies Q6's "enforce, do not merely claim" without
touching a frozen command sequence that three acceptance rows test verbatim, and
it holds for a script invoked directly — which §13.2's own sequence does nine
times after the fixtures. The re-exec must appear in the run record; that is a
requirement, not a caveat.

[Answer]: D

---

## FU-2 — Which module owns the locked-test path guard?

Q4=C puts the access-log obligation on a **path guard** and execution on a fold
guard. §12 assigns fold logic to `src/data/splits.py`. It assigns the path guard
to **no module**. Q2=B set the governing principle for exactly this situation:
do not widen a §12 module past its stated responsibility — amend the tree with a
record instead.

- A. **A second new module, `src/data/locked_test.py`**, added under the *same* §15.2 amendment as `config.py`.
  *Impact:* single responsibility, and one change record and countersignature covers both new modules rather than two. Two additions to §12's tree in one stage.
- B. **`src/data/release.py`** — it already owns SHA-256 hashing and manifest writing, and every access-log row is a hashed record.
  *Impact:* no new module. Widens release.py from "what a run produced" to "what a run was permitted to read", which is the widening Q2=B rejected.
- C. **`src/data/prepared.py`** — §12 gives it Phase 1 provider-file validation, and the December artifacts are provider files.
  *Impact:* no new module and the file-reading responsibility is adjacent. `prepared.py` is Phase 1-scoped while the guard must also hold at G-06, which is Phase 1's exit.
- D. **`src/data/splits.py` owns both limbs**, with the path guard as a separate function in the same module.
  *Impact:* one module owns everything locked-test, which is easy to review. Collapses the read/execute distinction Q4=C deliberately separated into one file, though not into one function.
- X. Other (please specify)

**Recommendation: A.** It is the only option consistent with the principle Q2=B
established, and folding it into the same amendment makes the marginal cost close
to zero. B and C both reproduce, in a different module, the boundary-widening that
Q2 rejected on the config loader.

[Answer]: A

---

## FU-3 — Q6 names six tests; two have no home in the mandated eighteen

Q6 requires tests for seed loading, stage-level seed recording, bootstrap
independence, three-seed prediction alignment and averaging, premature TensorFlow
initialization, and explicit reporting of nondeterministic operations.
REQ-ENG-4's set is **18 modules** — the 17 in §12 plus the countersigned
`test_acquisition_window.py`. Bootstrap independence and seed reproducibility fit
`test_bootstrap.py`; three-seed averaging fits `test_models_smoke.py` or
`test_checkpoint_restore.py`. **Premature TensorFlow initialization** and
**nondeterministic-operation reporting** fit none of the eighteen by subject.

- A. **New test cases inside existing modules only** — place the two homeless checks in `test_clean_run.py`, whose subject is the reproducibility contract.
  *Impact:* REQ-ENG-4's count stays 18 and no amendment is needed. A reader looking for determinism coverage has to know to look inside the clean-run module.
- B. **One new module, `tests/test_determinism.py`**, under the same §15.2 amendment as FU-2 and Q2.
  *Impact:* determinism coverage is findable by name, and NFR-DET-01 gains a module that maps to it one-to-one. REQ-ENG-4's count becomes 19 — a number stage 2.3 has already had to correct twice, so it must be updated everywhere it appears.
- C. **Extend `test_bootstrap.py`** to cover all six, since it already owns seeded reproducibility.
  *Impact:* no amendment and one place for seed behaviour. Puts a TensorFlow-initialization check inside a module named for the bootstrap, which is where it will be lost.
- X. Other (please specify)

**Recommendation: B.** The count is a bookkeeping cost, and this stage is already
paying for one amendment — whereas A and C both hide a determinism check under an
unrelated module name, and NFR-DET-01 is one of the ten items §18.3's preflight
gate enumerates. Findability matters more than the count.

[Answer]: B

---

# RE-ENTRY — 2026-08-23: the `src/features` leakage boundary

**Why this stage is open again.** A backward jump from stage 3.1, on the owner's
decision, after **five** adversarial review cycles on unit `features-and-splits`
every one of which returned `NOT-READY` on BLK-04's element 4. The failures were not
wording. The interface designed here **cannot express** the check BLK-04 requires, and
each attempt to patch it from 3.1 grew the amendment set — seven across four units by
the fifth cycle, with two more implied.

**The five cycles, and what each proved.** Preserved so this redesign does not
re-derive them:

| Cycle | Mechanism tried | Why it failed |
|---|---|---|
| 1 | *"`apply_transforms` refuses a transform whose fold does not match the frame's partition"* | A **claim, not a check** — the signature carries no fold or partition parameter, and `frame` carries no partition tag |
| 2 | Derive each row's partition from its record timestamps | The training ranges **nest**, so no single-valued label exists; also blocked **G-06** and the final refit outright |
| 3 | Containment in the transform's own named scope | The five scopes are **strictly nested prefixes** (F1 → 30 Apr ⊂ F2 → 31 Jul ⊂ F3 → 31 Oct ⊂ F4 → 30 Nov ⊂ refit → 31 Dec), so containment reduced to *"not later than this transform's validation month"*. **F4's transform on April passed, and F4's fit saw April** |
| 4 | A required `purpose: ApplyPurpose` | Closes the `evaluate` direction — verified over the full 5 × 12 space — but `purpose=train` still admits **10 nested cells**, every one a truthful declaration |
| 5 | `purpose` plus a pairing control over the nine stage scripts | The control is **unimplementable here**: `services.md` has `05` **write** the features and `06`/`07` **read** them, so **no evaluation site calls `apply_transforms` at all** |

**The three defects in this stage's own artifacts**, each verified directly rather
than inferred:

1. **`build_features` has no row selector.** `component-methods.md:385-393` takes
   `target, drivers, registry, matrix, fold, snapshot` — no period. A caller cannot
   ask for "F1's training rows" as distinct from "F1's validation month".
2. **Nothing stamps the emitted artifacts.** `services.md` § The nine stage scripts:
   `05` writes the feature matrix and sequence tensor; `06` and `07` read them. No
   fold, no purpose, no transform identity travels with the file, so provenance
   cannot be checked on the far side of the handoff.
3. **`FoldSpec` cannot represent the final refit.** It carries `validation_month:
   int`; the refit has none. So `fit_transforms(train, *, fold: FoldSpec)` and
   `build_features(..., fold: FoldSpec)` have **no refit path at all**, and December
   inherits that gap. FR-P1-04-14 requires the refit; **G-06 depends on it**.

**Also unresolved and inherited:** `vtec_seq_24` and `vtec_lag_24h` need **24 h of
history preceding** any scored row, so a frame for a validation month must contain
rows that are **present but never scored**. No current type distinguishes them, which
is why cycle 5 forced a choice between raising on every evaluation and silently
dropping the first ~24 h of each validation month — **1 December included**.

**Scope of this re-entry.** The `src/features` and `src/data/splits.py` boundary
calls, and the artifact stamps in `services.md`. Q1's depth answer, Q2–Q8, and
FU-1–FU-3 are **not reopened**; nothing below contradicts them.

---

## Q9 — How is the partition list represented, so the final refit and December are expressible?

`FoldSpec` carries `validation_month: int` and `fold_id: "F1".."F4"`. The refit has
no validation month and no fold id, so it is representable nowhere, and both
functions that take a `FoldSpec` are closed to it.

A) Keep `FoldSpec` and add separate `RefitSpec` / `LockedSpec` types
   > **Impact**: No change to the four folds' path, and each shape says exactly what it is. But every function taking a partition now needs a union type or an overload, and the *"exactly one partition per timestamp"* assertion has three lists to walk instead of one — the shape that let November go unchecked in the first place.

B) Generalise to one `Partition` with `validation_month: date | None`
   > **Impact**: One type, one list, one assertion. The refit and December are ordinary members with `validation_month = None`. Costs a nullable field, and every reader must handle `None` rather than being told by the type which case it has.

C) One `Partition` carrying an explicit `kind: PartitionKind` (`fold` | `refit` | `locked`) alongside `validation_month: date | None`
   > **Impact**: One type and one list as in B, but the case is **named** rather than inferred from a null. A reader branches on `kind`, not on whether a field happens to be `None`, and the locked partition is distinguishable from the refit — which matters, because December is the one partition whose access is gated. Costs one more field than B.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. B and C both fix the blocking defect; C additionally makes December distinguishable from the refit **in the type**, and this project gates December differently from every other partition (`materialise_locked_partition`, `g05_signature`, WS-18). Inferring "locked" from `validation_month is None` would make the refit and the locked month indistinguishable at exactly the boundary where they must not be — the error `project.md` § Way of Working warns about when a gating condition's inputs are left implicit.

[Answer]: C

---

## Q10 — How does `build_features` learn which rows to build?

It currently cannot be asked. The absence is why cycle 5's *"one `train` call and one
`evaluate` call"* was inexpressible.

A) Leave the signature alone; callers slice the frame before and after
   > **Impact**: No amendment. But it is the status quo that five cycles defeated: the slicing lives in nine stage scripts with no check, which is enforcement by review for the project's central leakage rule — precisely what BLK-04 exists to replace.

B) Add `period: tuple[datetime, datetime]`
   > **Impact**: Minimal and expressible. But a bare date range says nothing about *which partition* it belongs to or *what the rows are for*, so the leak check still has to infer both — and the nesting proof above shows a date range cannot carry that information.

C) Add a `FrameSpec` carrying `partition_id`, `role` (`train` | `score`), the scored range, and `lead_in_hours`
   > **Impact**: One parameter that answers all three questions the check needs: which partition, what for, and which rows are history rather than scored. `lead_in_hours` makes the `vtec_seq_24` requirement **explicit**, so the first 24 h of a validation month are present-but-not-scored by contract instead of silently dropped. Costs a new type on the boundary.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. It is the only one that also fixes the lead-in defect, and the lead-in is not a detail: under B, a scored range of *exactly* December forces either a raise on every evaluation or the silent loss of **1 December** — the first day of the locked test month, in the one evaluation this thesis turns on.

[Answer]: C

---

## Q11 — How is the leakage check itself expressed?

A) Date containment — the frame's rows must fall inside the transform's scope
   > **Impact**: What cycle 3 built. **Defeated**: the scopes are nested prefixes, so F4's transform on April passes and F4's fit saw April.

B) `purpose` plus containment
   > **Impact**: What cycle 4 built. Closes `evaluate` but leaves the **10 nested `train` cells**, each a truthful declaration that no signature can reject.

C) **Identity** — `transform.partition_id` must equal `spec.partition_id`
   > **Impact**: The nesting problem **disappears**, because ids are compared rather than date ranges: F4's transform can never be used on a frame whose spec says `F1`, regardless of which months overlap. It is a single equality, checkable inside `build_features`, and it needs no `purpose` parameter at all — `FrameSpec.role` already carries the use, because row selection needed it anyway. Costs nothing beyond Q10's `FrameSpec`.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C, and it is strictly simpler than what cycle 4 reached. Five cycles were spent trying to reconstruct *which partition a row belongs to*; the check never needed that. It needed to know which partition the **frame was built for**, which is a fact the caller states once and the type carries. Identity also removes the separate `ApplyPurpose` parameter, so the amendment shrinks rather than grows.

[Answer]: C

---

## Q12 — How does provenance survive the `05` → `06` disk handoff?

`05` writes; `06` and `07` read. Any pairing rule written inside `05` is invisible to
the scripts that actually score.

A) Nothing — the stage scripts are careful
   > **Impact**: The gap as it stands. It is what made cycle 5's pairing control unimplementable, and it is invisible: a wrong-fold frame produces better numbers and raises nothing.

B) A manifest field beside each artifact
   > **Impact**: Provenance becomes checkable, and the project already hashes and manifests its artifacts. But a manifest is a **separate file** from the array it describes, so the two can drift, and nothing in the type system ties them.

C) A `FeatureBundle` return type carrying `matrix`, `tensor`, its `FrameSpec` and the `transform_id`, persisted and reloaded as one unit
   > **Impact**: The stamp cannot be separated from the data, because it is the same object — and both representations travel together, which is what FR-P1-04-8's parity wanted structurally. `06`/`07` can then assert that a frame scored for partition *k* carries `spec.partition_id == k`, `spec.role == "score"` and the matching `transform_id`. Costs a return-type change on `build_features` and a defined on-disk form.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. B is genuinely workable and cheaper, but this project has already been bitten by a derived artifact drifting from the record that describes it — `evidence.md` fact 6, where `sha256_manifest.json` hashes four derived files and not the retrieval it was read as covering. Making the stamp inseparable from the data removes that failure mode rather than re-creating it one level up.

[Answer]: C

---

## Q13 — Which transform scores December? *(raised by the re-entry advisory review)*

Q11's identity check raises on `transform.partition_id == "REFIT"` against
`spec.partition_id == "DEC"` — **which is exactly the G-06 apply**. Q9–Q12 never asked
which transform scores the locked test, and the only alternative a pure identity
permits is a `DEC`-stamped transform, i.e. **fitting on December**.

A) The refit's transform, with one enumerated carve-out in the identity rule
   > **Impact**: What stage 3.1 already assumed, and scientifically right — the transform is fitted Jan–Nov and December is never fitted on. Costs the invariant: it becomes "ids match, **or** are the one enumerated pair", which is strictly weaker than a pure identity and needs a negative control enumerating every other ordered pair so a second exception cannot be added silently.

B) Fold December into the refit partition, distinguished only by `FrameSpec.role`
   > **Impact**: The identity check stays pure — no exception, no enumeration control. But December loses its own `partition_id`, and both the locked-test guard and the exactly-one-role assertion key on it. `PartitionKind.locked` was added in Q9 precisely so December stays distinguishable at the one boundary that is access-gated.

C) Route it to the supervisor as a G-05-adjacent question
   > **Impact**: The locked-test protocol is supervisor-owned (Vision §5.3, gate row G-06), so this is defensible. Costs: ADR-11 cannot complete, and BLK-04 stays open across five units, until it is answered.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A. B looks cleaner but trades away the distinction the design just spent Q9 establishing, at the exact boundary where December must remain identifiable. A's cost is real and is paid in evidence: the carve-out is one row in a table, and the enumeration control makes any second row a test failure.

[Answer]: A

---

## Q14 — Does a window cross into December so 1 December is scorable? *(raised by the re-entry advisory review)*

Q10's `lead_in_hours` existed so `vtec_seq_24` and `vtec_lag_24h` could reach 24 h
**before** a scored row. **FR-P1-04-5's criterion says the opposite**, verbatim: *"No
window crosses a boundary … the first 24 h are excluded and counted."*

A) Route to the supervisor
   > **Impact**: Whether a window may cross into the locked month, and whether 1 December is scored, changes the **locked-test scored set** — supervisor-owned under Vision §8.2/§8.7 and G-05, and ADR-11 states no ADR here adopts a reading on a supervisor-owned value. Costs: ADR-11 stays conditional until answered.

B) Drop `lead_in_hours` and honour FR-P1-04-5
   > **Impact**: No approved requirement is reversed and nothing supervisor-owned is touched. Costs: **1 December is not scored**, the locked test covers **30 days, not 31**, and the same exclusion applies to Apr, Jul, Oct and Nov — all of which must be disclosed wherever coverage is reported, since a December figure reading as 31 days would be wrong.

C) Keep it, flag the conflict at the gate
   > **Impact**: 1 December stays scorable. But the artifact would ship stating a rule that contradicts an approved requirement, which is the condition `phases/inception.md` § Requirements Quality forbids carrying forward silently.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A or B, not C. Between them: B if the 30-day locked test is acceptable, A if scoring 1 December matters scientifically. B is the conservative reading and needs no one's signature; A is correct if the supervisor would rather widen the test than lose a day.

[Answer]: B

> **Owner decision, 2026-08-23.** Q13 = A, Q14 = B. Both were put to the owner with
> their costs stated, after the re-entry advisory review found the first draft of
> ADR-11 wrong on both points. The consequences are recorded in `ADR-11`
> § "Two owner decisions", in `component-methods.md`'s two `⚠` boxes, and in
> `component-dependency.md`'s enforcement table.

---

## Consolidated Summary Confirmation (2026-08-21 pass, answered and superseded)

Answers as recorded:

- **Q1 = B** — `component-methods.md` gives **full signatures with types for cross-package boundary calls**, and names plus one-line purposes for intra-package functions. Every defect this project's governance has caught travelled across a package boundary, so those contracts are pinned now; internal shapes stay with `functional-design` (3.1).
- **Q2 = B** — config loading, the per-run four-config snapshot and its hash go in a **new `src/data/config.py`**, added to §12's tree as a recorded amendment under Vision §15.2. Rejected widening `release.py` or `phase_contract.py`, since §12's stated responsibilities are what the release and phase-boundary tests key on.
- **Q3 = B** — the Phase 1 import prohibition gets a **runtime guard in `src/data/phase_contract.py`**, called by every phase-aware stage script at entry: given `--phase 1` it asserts the raw modules are absent from `sys.modules` and refuses to proceed. The prohibition therefore holds inside the Kaggle session, where a commit hook cannot fire.
- **Q4 = C** — **both** locked-test guards: a path guard owning the access log (every December read logged *before* the read), and a fold guard owning execution. The two obligations stay separate because the pre-G-05 coverage audit is a *required read* while the metrics run is *barred* until after G-05 — one guard cannot express both without conflating them.
- **Q5 = C** — the experiment registry is an **append-only JSONL log** of run events, authoritative, with a **derived CSV** regenerated from it for review at a gate. The CSV is marked derived and hashed, so a corrupted CSV is never data loss.
- **Q6 = X** (verbatim in the question above) — a **shared determinism helper alongside the Q2 config module**, called at every relevant stage entry: seeds from `seeds.yaml` applied to Python, NumPy and TensorFlow; TensorFlow op determinism enabled **before** graph construction; applied seeds, framework versions, determinism settings, environment and any non-guaranteed operations recorded in the run's environment lock **and** the experiment registry. Three approved model seeds, individual predictions preserved, confirmatory prediction as their element-wise mean with **sample alignment explicitly verified**; no best-seed selection and no single-seed substitution. **Bootstrap randomness is independent**: `src/evaluation/bootstrap.py` builds its own local generator from the separately frozen `20221201`, and changing a model seed must never change a bootstrap draw. Process-level settings are enforced where they take effect, never claimed after startup. Six named tests required.
  - *Reading adopted, stated rather than assumed:* "the approved configuration or recorded governance decision" resolves to **`configs/seeds.yaml`** as the mechanism (TE §13.5 stores all four seeds there) with **Vision §8.6 / D-122** as the authority. The value is read from config and never inlined, satisfying TC-03e.
- **Q7 = C** — **environment variables for credentials** (§10: platform secret stores or environment configuration excluded from version control), a **runtime path helper for platform roots**, and the **resolved roots recorded in the run's environment lock**. Machine paths stay out of the four governed configs, so moving a directory never changes a governed hash and never trips §13.7's exact-equality check.
- **Q8 = B** (verbatim in the question above) — Phase 1 designed fully; for `src/gnss/`, **module responsibilities and the externally visible Phase 1 to Phase 2 interface only**, with no premature internal signatures or unverified scientific assumptions. The transition contract is built from **evidence-backed Phase 1 artifacts** — observed schema, artifact identities, SHA-256 and config hashes, approved decisions, provenance, invariants Phase 2 must preserve. The observed Phase 1 product schema is held **explicitly distinct** from any future Phase 2 target schema: the ten-field contract is **not** imposed on the five-column product, D-17's resolution is preserved, and any later transformation is Phase 2 work needing its own evidence. A phase-transition manifest freezes the handoff surface and **names unresolved Phase 2 decisions rather than inventing values**. The Phase 1 import prohibition stands, and G-P2 checks cover manifest integrity, schema compatibility, config continuity and locked-test protections.
  - *Reading adopted:* the Phase 1 to Phase 2 handoff is an **artifact and data contract**, not a function-call API, so Q1's "full signatures for cross-package boundary calls" applies to the Phase 1 packages and not to a `gnss` call surface that no Phase 1 code may reach.
- **FU-1 = D** — **both**: every stage script re-execs itself with `PYTHONHASHSEED` set when it finds it unset, so the guarantee holds for a directly invoked script, **and** §13.2's documented command sequence is amended to carry it under a §15.2 change record, so the sequence a reader follows is the whole truth. The re-exec is recorded in the run log and is never mistaken for a double run.
- **FU-2 = A** — the locked-test path guard is a **new `src/data/locked_test.py`**, folded into the *same* §15.2 amendment as `config.py`. Consistent with Q2=B's principle rather than reproducing the boundary-widening it rejected.
- **FU-3 = B** — the two determinism checks with no home get a **new `tests/test_determinism.py`**, in the same amendment. NFR-DET-01 gains a module mapping to it one-to-one.

---

### One consequence the individual answers do not show

Q2, FU-1, FU-2 and FU-3 together amend the authority documents in **four**
places, not one:

| Change | Where | Effect |
|---|---|---|
| `src/data/config.py` | TE §12 tree | REQ-ENG-1's six-package enumeration gains a module |
| `src/data/locked_test.py` | TE §12 tree | as above |
| `tests/test_determinism.py` | TE §12 tree | **REQ-ENG-4's mandated count goes 18 to 19** |
| `PYTHONHASHSEED` in the clean-run commands | TE §13.2 | `test_clean_run.py`, WS-20 and TA-17 all test the sequence as written and must be updated with it |

> **⚠ The "18 to 19" figure above is superseded, and the table is left as it was
> presented.** This section records what was put to the owner on 2026-08-21 and what
> they agreed to; rewriting an answered question would falsify that record. The
> current figure is **21**, and the amendment was **applied and approved** on
> 2026-08-22 under `CR-2026-08-22-TE-AMEND` — see `decisions.md` ADR-10 § ⚠ CORRECTED
> 2026-08-23 for the 17 → 19 → 20 → 21 route and its authorities. Annotated
> 2026-08-23 after the advisory reviewer found this copy still carrying the old
> number.

On the precedent this project already set — `test_acquisition_window.py` was
added to §12's tree and **countersigned 2026-08-16** — these carry a §15.2 change
record and a supervisor countersignature. You hold that authority under the
recorded student/supervisor equivalence, so it is grantable here, but it has to be
*recorded* rather than assumed: `project.md` § Forbidden bars an agent from
filling a supervisor-owned value by convenience, and a tree amendment is that
class of change.

**REQ-ENG-4's count is the item to watch.** Stage 2.3 corrected that number twice
under governance findings, and this stage moves it again. Every place it appears —
REQ-ENG-4, § Requirements with no testing row, `team-practices.md` § Testing
Posture, and the §12 enumeration — has to move together, or the next board finds a
count mismatch exactly like `DATA-21`.

> **⚠ The "four places" claim above is superseded too, annotated 2026-08-23.** The
> paragraph is left as it was put to the owner on 2026-08-21, for the same reason as
> the table above it. The count appears in **two** places, not four — derived by the
> advisory reviewer, and recorded in `decisions.md` ADR-10 § ⚠ CORRECTED 2026-08-23,
> which also notes that this "four" was itself asserted rather than derived: the
> `DATA-21` pattern the sentence warns about, committed inside the warning. Caught on
> a sweep of the paragraphs *around* the superseded numeral rather than of the numeral
> alone — the blind spot `project.md` § Way of Working names.

**What I will not do without a further decision from you.** I will design against
these answers and record the amendment as a stated obligation, with its four items,
inside `decisions.md` as an ADR. I will **not** write the change record, edit
`requirements.md`'s counts, or touch the authority documents as part of this
stage — those are separate governed changes, and stage 2.6's produces list does
not include them.

Does this all look correct before I generate the design artifacts?

- Looks correct
- Request changes

[Answer]: Looks correct

---

## Consolidated Summary Confirmation (2026-08-23 fix pass, answered `Request changes` and superseded)

**Why this section exists.** The 2026-08-23 re-entry review returned
**NOT-READY** (4 Critical, 7 Major, 3 Minor). Because it is an *advisory* pass,
nothing in it was applied — the findings were held as gate input. The artifacts
were then edited after that review's receipt was recorded, which invalidated the
receipt, and an advisory stage carries a budget of one review, so no second pass
was available to re-validate the edited text. The stage was therefore re-entered
by a redo jump, which clears the receipt floor and the spent budget. Under this
re-entry the findings become builder input: they are applied first, then one
fresh advisory review runs over the corrected artifacts, then the gate.

**Q1–Q14 and FU-1–FU-3 are not reopened.** Every answer recorded above stands
exactly as given. This pass changes only what the review named.

### What I will fix in this stage

| # | Severity | Finding, in short | Fix |
|---|---|---|---|
| C1 | Critical | `fit_transforms(bundle: FeatureBundle)` claims a check its arguments cannot execute — no argument carries any partition's training range | Re-sign as `fit_transforms(bundle: FeatureBundle, *, partition: Partition) -> Transform` and enumerate the raises concretely (scored range ≠ the partition's training range, `partition_id` mismatch, `role != "train"`, `transform_id is not None`). Specify the matching `spec`-versus-`Partition` validation in `build_features`. **Withdraw** ADR-11's *"genuinely unrepresentable"* claim rather than restating it — the same withdrawal ADR-01 needed |
| C2 | Critical | The identity check forbids the refit→December apply that G-06 requires, leaving a December-fitted transform as the only representable path | Replace the equality with a closed relation: a transform is appliable when its `partition_id` is the frame's own **or** the partition declared as that frame's scoring source. `Partition` gains that source (`REFIT` for `DEC`, self for a fold). Add a fourth call showing the locked evaluation end to end. Any resolution that would permit a `"DEC"`-stamped transform to be fitted is rejected outright |
| C4 | Critical | `assert_membership_from_timestamps` and `lead_in_hours` contradict each other, and the "not scored" half is enforced nowhere | Name the single mechanism that enforces it and give it a concrete raise, so one rule owns the boundary instead of two half-rules |
| BLK-03 | Major, carried | `three_seed_mean(predictions)` cannot verify the seeds are the frozen set without inlining `{1337, 2024, 7}`, which TC-03e forbids | Add `expected_seeds: frozenset[int]`, sourced from `ConfigSnapshot.seeds` at the call site — the shape `vector_block_bootstrap(seed: int)` already gets right |
| M5 | Major | `Partition` carries six ids against FR-P1-04-5's *"all five partitions"*, and the locked partition cannot say which month it evaluates | Reconcile the enumeration against the approved criterion and give the locked partition an explicit evaluated-month field |
| M6 | Major | Removing `apply_transforms` left no inverse, yet `ABL-DIFF` must inverse-transform to absolute TECU before any metric | State whether the transform touches the target. If it does, add the inverse to the boundary plus the `src/evaluation` → `src/features` edge in `component-dependency.md`; if it does not, say so explicitly in both places so the obligation is visibly satisfied |
| M7 | Major | `07_evaluate_and_report.py` is claimed to assert on `FeatureBundle`s it is not recorded as reading | Make the script table and the assertion agree |
| M8 | Major | `FeatureBundle` is asserted persistable "as one unit" with no format named, and no single format holds a `DataFrame` + an `NDArray` + a dataclass | Name the concrete on-disk representation and re-open ADR-11's rejected side-car alternative honestly, since §13.3 requires the release to record hashes per file |
| M9 | Major | `FrameSpec` is not a unique key — `raw` and `train` carry identical values, so the `05`→`06` handoff has no unambiguous address | Add the discriminator that makes the address unique |
| M11 | Major | ADR-11's blast radius omits `fixtures-and-reproducibility` and names no already-written 3.1 artifact | Add the missing unit; name the invalidated artifacts by path and derived count so the 3.1 re-entry has a checklist |
| M12 | Minor | `lead_in_hours` is caller-supplied, defaulted and unvalidated — `0` silently reinstates the behaviour it was added to prevent | Specify the raises (follows whatever C3 resolves to) |
| M13 | Minor | The three-call sequence's cost — three full feature constructions per partition — is not in the resource envelope | Correct the envelope |

### The one that needs your ruling first — C3

`lead_in_hours` reverses FR-P1-04-5's **approved** criterion (*"no window crosses
a boundary … the first 24 h are excluded and counted"*) and thereby **enlarges
the December scored set**. That is a supervisor-owned scientific change, and
`project.md` § Forbidden bars me from filling one by convenience.

**My default, unless you rule otherwise:** withdraw `lead_in_hours`, restore the
approved criterion as written, and carry the enlargement to you as a gate item.
Reverting is the option that changes no frozen scientific value; adopting it
would change what December scores, which needs a recorded decision with a
D-number, not a design edit.

### What I will not touch, and why

These are real and stay visible at the gate rather than being quietly fixed:

- **M10** — neither mandated fixture can exercise the redesigned boundary: partitions come from the frozen 2022 calendar boundaries, while D-11 froze the plumbing window at 2022-11-01 to 2022-11-07. The fixture windows are frozen student decisions; changing one here would be exactly the convenience-fill the rules forbid.
- **M14** and **BLK-04/BLK-06 register wording** — both live in files outside this stage's produces list (`construction/.../business-logic-model.md`, `unit-of-work-story-map.md`). Governed changes in their own right.

Does this fix scope look correct before I edit the design artifacts?

- Looks correct
   > **Impact**: I apply the twelve fixes above, revert `lead_in_hours` to the approved criterion, then run one fresh advisory review over the corrected artifacts and bring you its verdict plus the four gate items at the approval gate. The three deferred items stay open and visible.

- Request changes
   > **Impact**: Nothing is edited. You tell me what to add, drop, or decide differently — including a different ruling on C3 — and I re-present this scope before touching anything.

> **💡 Recommendation**: **Looks correct** — the review's own recommendation is that findings 1, 2 and 3 be resolved *in this stage* before 3.1 re-enters, because each is the same class of gap (a check stated in prose the signature cannot execute) that already cost stage 3.1 five review cycles. Reverting `lead_in_hours` rather than adopting it is the conservative half of that: it keeps a supervisor-owned value where you can rule on it instead of letting a design edit decide it.

[Answer]: Request changes

---

## Consolidated Summary Confirmation (2026-08-23 fix pass, revision 2 — answered `Looks correct` and superseded by the sweep below)

*(re-presented under the owner's rulings)*

### Correction to the scope you were shown

The scope you ruled on listed **twelve fixes as work still to do**. Checking each
against the artifacts before editing anything shows that **seven of them are
already implemented on disk**. They were written between 09:40 and 09:42 on
2026-08-23 — the same post-review edits that invalidated the review receipt and
forced this re-entry. They were never re-reviewed, which is what the fresh
advisory pass at the end of this stage is for; they are not, however, work
outstanding.

The rulings you gave stand unchanged. What changes is the size of the edit: **five
substantive changes plus the deferral tracking**, not twelve.

---

### 1. Approved fixes — already implemented, verified, no further edit

Each was checked at the location named. No edit is proposed for any of them; they
are listed so the fresh review sees the same set you approved.

| # | Ruling | State on disk, verified | Where |
|---|---|---|---|
| C1 | Approved | `fit_transforms(bundle: FeatureBundle, *, partition: Partition)` — the `partition` argument is present, and the raises are enumerated concretely (`role != "train"`; already-transformed bundle; `partition_id` mismatch; scored range not exactly the partition's training range) | `component-methods.md` § The `src/features` leakage boundary |
| C2 | Approved | The identity check carries exactly one enumerated exception, `REFIT` → `DEC` with `role == "score"`, with a negative control enumerating every other ordered pair, and `REFIT` → `DEC` with `role="train"` raising | `component-methods.md` § ⚠ ONE ENUMERATED EXCEPTION; `decisions.md` ADR-11 decision 3 |
| C4 | Approved | **Dissolved by the C3 removal rather than fixed separately.** The contradiction was between `lead_in_hours` and `assert_membership_from_timestamps`; with the field withdrawn, `scored_start`/`scored_end` bound exactly what is scored, nothing precedes them, and out-of-range windows are excluded and counted. No residual wording found | `component-methods.md` §§ `src/data/splits.py`, The `src/features` leakage boundary |
| M6 | Approved | The inverse is restored as `Transform.inverse(frame) -> DataFrame`, travelling with `Prediction.transform_id`, deliberately **without** a new `src/evaluation` → `src/features` package edge | `component-methods.md` § `src/models` |
| M7 | Approved | The script table now records `07` as reading predictions carrying `partition_id` and `transform_id`, not `FeatureBundle`s, and the ⚠ box states it | `services.md` § The nine stage scripts |
| M8 | Approved | The on-disk form is named: one directory per bundle holding `matrix.parquet`, `tensor.npy`, `spec.json`, all three hashed by §13.3's manifest, loaded together or raising | `services.md` § ⚠ THE `05` → `06` HANDOFF |
| M11 | Approved | The blast radius names **six** units including `fixtures-and-reproducibility`, with the derived counts (`FoldSpec` 85, `apply_transforms` 63, `build_folds` 4 = 152 across 4 files) | `decisions.md` ADR-11 § Blast radius |
| M12 | Approved | **Moot.** The finding was that `lead_in_hours` was defaulted and unvalidated; the field no longer exists | — |

### 2. Approved fixes — the five edits I will actually make

| # | Ruling | Change | Artifact |
|---|---|---|---|
| BLK-03 | Approved | `three_seed_mean(predictions: Sequence[Prediction], *, expected_seeds: frozenset[int]) -> Prediction`, sourced from `ConfigSnapshot.seeds` at the call site. The prose keeps its `SeedError` raise but the comparison is now against a configured value instead of an inlined `{1337, 2024, 7}` (TC-03e) or a weaker distinctness check. Matches the shape `vector_block_bootstrap(seed: int)` already uses | `component-methods.md` § `src/models` |
| M5 | Approved | `Partition` gains an evaluated month for the locked partition (`validation_month` set to December rather than `None`, leaving `None` for the refit alone), and the text states explicitly that the **split manifest enumerates the five partitions FR-P1-04-5 names — F1–F4 and the final refit** — with the locked December partition recorded separately as the access-gated evaluation partition. Six `Partition` objects, five manifest rows, one locked partition that can say which month it evaluates | `component-methods.md` § `src/data/splits.py` |
| M9 | Approved | A naming rule for the bundle directory that makes the address unique: `raw` and `train` currently carry **identical** `FrameSpec` values and differ only by `transform_id`, so the `05`→`06` handoff has no unambiguous address. The directory name carries partition, role and transform identity (untransformed bundles distinguished explicitly), and `06`/`07` resolve a bundle by that address | `services.md` § ⚠ THE `05` → `06` HANDOFF |
| M13 | Approved | The envelope records that ADR-11's three-call sequence performs **three complete feature constructions** per partition, with three `matrix`+`tensor` pairs live at once, and states that against TE §9.3's 10.0 GB hard planning envelope | `services.md` § Resource envelope |
| C1-residual | Approved (part of C1) | The withdrawal C1 required but that the on-disk fix did not carry through: three places still assert the leak is *unrepresentable*. See § 4 below | `decisions.md`, `components.md`, `component-dependency.md` |

### 3. The C3 ruling, recorded as given

`lead_in_hours` is **withdrawn**; FR-P1-04-5's approved criterion is restored
**exactly** — *"No window crosses a boundary … the first 24 h are excluded and
counted"*; the December scored set is **not** enlarged through an
application-design edit. This is already the state on disk and no edit changes it.

Recorded with it, in `decisions.md` ADR-11 § Two owner decisions, as the ruling
directs: the frozen protocol requires a 24-hour causal history, prohibits input
windows from crossing partition boundaries, and reserves December 2022 as the
locked test. **Any** proposal to use pre-December lead-in data or to enlarge the
December scored set is therefore a **separate controlled gate decision**, and must
carry its scientific rationale, its exact scored-sample impact, a leakage
analysis, and its comparability consequences. It is not decided implicitly in this
design revision.

The disclosed consequence stands and is not softened: **the locked test covers 30
days, not 31**, and the first 24 h of every validation month (Apr, Jul, Oct, Nov)
are likewise excluded and counted.

### 4. Normative wording withdrawn or replaced

Nothing here changes a requirement. Each item is a **design claim about a
requirement** that the artifacts overstate, and each is corrected in place with the
superseded text preserved, per this project's amendment practice.

| Location | Withdrawn wording | Replaced with |
|---|---|---|
| `decisions.md` ADR-11 § Consequences | *"`fit_transform(all_data)` is now **genuinely unrepresentable** — `fit_transforms` takes a `FeatureBundle`, and a bundle exists only for a declared partition and role."* | The leak is **rejected at run time by a check the argument closure can execute** — `fit_transforms` receives the `Partition`, so the scored-range-equals-training-range comparison is computable rather than asserted. It is not unrepresentable **in the type**: `FrameSpec.partition_id` remains a caller-supplied string. This is the same withdrawal ADR-01 needed, and it is recorded as a withdrawal rather than restated in stronger words |
| `components.md` § `src/features` row `transforms.py` | *"a full-dataset fit has **no argument to be passed as** — genuinely unrepresentable rather than merely discouraged"* | The full-dataset fit **raises**, because `fit_transforms` holds the `Partition` and compares the bundle's scored range against its training range |
| `component-dependency.md` § enforcement row, NFR-LEAK-01 | *"it takes a `FeatureBundle`, so a full-dataset fit has no argument to be passed as"* | Same correction, plus the `partition` argument named as what makes the raise executable |
| `decisions.md` § Assumptions & Open Questions, last bullet | *"**None** of these ADRs adopts a reading on a supervisor-owned value, and none decides a scientific constant."* | **No longer true and replaced.** ADR-11 records two owner decisions and adopts the §8.1 evaluation-role reading. The replacement states which readings are adopted, that they are carried to the gate, and that no scientific constant is decided |

**Why this matters beyond wording.** An overstated safety claim is the exact defect
that cost stage 3.1 five review cycles: BLK-04 was inherited *as a claim*, and each
cycle tried to make the claim true from below. Leaving three copies of a
weaker-than-stated invariant on disk re-seeds that.

### 5. Deferred obligations — tracked open, none closed

Recorded in `decisions.md` § Assumptions & Open Questions. **None is marked
resolved or closed.**

| Item | Destination artifact | Owner | Due gate | Acceptance test |
|---|---|---|---|---|
| **M10** — neither mandated fixture can exercise the redesigned boundary. Partitions come from the frozen 2022 calendar boundaries; D-11 froze the plumbing window at 2022-11-01 to 2022-11-07, and the scientific one-month window is still open under Q-31 | A **focused contract fixture**, synthetic and explicitly **not scientific evidence**, built over synthetic partition dates. Placed in the existing mandated modules `tests/test_train_only_transforms.py` and `tests/test_split_embargo.py` — deliberately **not** a new `tests/fixtures/` directory, which would require a §12 tree amendment | Authored by the developer at **code-generation (3.5)**; executed and evidenced by quality at **build-and-test (3.6)**, both for the `features-and-splits` unit. Fixture *window* decisions remain Student-owned (Q-31) and are untouched | **§18.3 preflight gate (TA-23)** — "no failing critical test", before any governed run | Four assertions: (a) the identity check raises for every ordered pair of partition ids except the enumerated one, by enumeration not sampling; (b) `REFIT` → `DEC` with `role="score"` passes and with `role="train"` raises; (c) `fit_transforms` raises when the bundle's scored range is not exactly the partition's training range; (d) `06`/`07` raise on any bundle with `transform_id is None` |
| **M14** — a 3.1 artifact cites `component-methods.md` **line 389** for `build_features`'s signature, an anchor this amendment moved | `construction/inventory-and-registry/functional-design/business-logic-model.md` line 529 | Architect, at **functional-design (3.1)** for the `inventory-and-registry` unit | That unit's 3.1 approval gate | The re-verification cites the section heading rather than a line number, so the anchor cannot go stale again |
| **BLK-04 / BLK-06 register wording** — BLK-04's remedy still prescribes *"a `LeakageError` when `train`'s index is not a subset of that partition"*, the containment rule ADR-11 explicitly rejects, so the register now contradicts the ADR that supersedes it | `unit-of-work-story-map.md` — produced by **units-generation (2.7)**, the next stage | Architect (lead) with delivery support, at units-generation | The units-generation approval gate | The register's BLK-04 remedy text matches ADR-11's identity-plus-enumerated-exception mechanism, and no containment wording survives |

### 6. Requirement-to-change traceability

| Requirement / rule | Authority | Change it drives | Artifact | Test row |
|---|---|---|---|---|
| **FR-P1-04-5** — fixed calendar folds, 24-h embargo, *"No window crosses a boundary; the split manifest … enumerates all five partitions"*, first 24 h excluded and counted | TE §7.1; Vision §8.2, §8.1 | **C3 ruling** (no enlargement, `lead_in_hours` stays withdrawn) and **M5** (manifest enumerates the five; locked partition names its evaluated month) | `component-methods.md` § `src/data/splits.py` | WS-12, TA-11 |
| **FR-P1-04-6** — scaling fitted on training partitions only, per fold, never the full dataset | Vision §6.4; **NFR-LEAK-01** | **C1-residual** — the three overstated *"unrepresentable"* claims withdrawn and replaced by the executable-raise statement | `decisions.md`, `components.md`, `component-dependency.md` | TA-11 |
| **FR-P1-04-14** — selection then refit on Jan–Nov without changing a hyperparameter | Vision §8.7 | **M5** — `REFIT` is a first-class partition with `validation_month = None`, so the refit stays expressible after the locked partition gains its month | `component-methods.md` § `src/data/splits.py` | `UNTESTED` (candidate TA row via §15.2) |
| **FR-P1-05-2 / NFR-DET-01 / TC-21** — fixed seeds from `seeds.yaml`; the three-seed element-wise mean is the confirmatory prediction | Vision §8.6; TE §13.5; D-122 | **BLK-03** — `expected_seeds: frozenset[int]` from `ConfigSnapshot.seeds`, so the frozen set is never inlined | `component-methods.md` § `src/models` | WS-17, TA-13, TA-26 |
| **TC-03e** — no scientific constant in source or a notebook | TE §12; `project.md` § Forbidden | **BLK-03**, same change — the alternative implementations were an inlined constant or a weaker check | `component-methods.md` § `src/models` | — |
| **FR-P1-04-11** — the release manifest's fourteen fields; releases write-protected or re-versioned | TE §13.3 | **M9** — a unique bundle address, so a hashed manifest row identifies exactly one bundle and `raw` cannot be mistaken for `train` | `services.md` § ⚠ `05` → `06` | TA-15 |
| **REQ-ENG-11 / TC-01 / TC-03** — every run records runtime and peak memory; CPU is a complete execution path within TE §9.3's 10.0 GB envelope | TE §9.2, §9.3 | **M13** — the three-construction cost stated against the envelope | `services.md` § Resource envelope | TA-03, TA-26 |
| **Vision §8.1** — each target timestamp belongs to exactly one partition | Vision §8.1 | No change. The evaluation-role reading stays adopted **and stays carried to the gate** as a reading of a frozen rule | `component-methods.md`, `decisions.md` | — |

### 7. What I will not do

No unrelated edits. No change to any requirement, acceptance criterion, D-number,
config value or `requirements.md` count. No new ADR beyond the corrections above.
No deferred item closed. Nothing outside the five artifacts in this stage's
produces list.

After the edits: one fresh advisory review over the corrected artifacts, then the
learnings ritual, then the approval gate, where the review's verdict and the three
open obligations are put to you.

Does this revised scope look correct before I edit the design artifacts?

- Looks correct
   > **Impact**: I make the five substantive edits plus the wording withdrawals and the deferral tracking, touching all five produces artifacts. The seven already-implemented fixes are left exactly as they are. Then one fresh advisory review runs over the result and its verdict comes to you at the gate.

- Request changes
   > **Impact**: Nothing is edited. You adjust the scope again — including telling me to treat any of the seven already-implemented fixes as insufficient — and I re-present before touching anything.

> **💡 Recommendation**: **Looks correct** — the correction in § 1 narrows the work rather than widening it, every ruling you gave is carried through unchanged, and the five remaining edits are the ones the re-entry review's own findings leave outstanding. The one item worth your eye is § 4's last row: the *"None of these ADRs adopts a reading on a supervisor-owned value"* line is now false on disk, and leaving it would understate what ADR-11 actually decided.

[Answer]: Looks correct

**Owner's words, verbatim:** "approved but resolve these firstFive edits remain:
BLK-03 (three_seed_mean gains expected_seeds: frozenset[int] from
ConfigSnapshot.seeds), M5 (locked partition names its evaluated month; manifest
enumerates FR-P1-04-5's five), M9 (unique bundle address — raw and train currently
carry identical FrameSpecs), M13 (three-construction cost against TE §9.3's 10.0 GB
envelope), and C1's residual withdrawal."

Read as approval of § 2's edit set with the instruction that those five are
resolved before the stage proceeds to review and gate.

---

## Consolidated Summary Confirmation (2026-08-23 minor sweep — revision 3, answered `Looks correct`, superseded on re-entry)

*(content unchanged; retaken below because the stage was re-entered)*

**Why a third confirmation.** The two count corrections you ordered at the first
gate were made and reviewed **READY**, with one Minor left: ADR-10's tail still read
as though the four-part amendment were unsigned. You then ruled *approve, sweep the
Minor first*. Sweeping it required editing this questions file, and the summary
receipt binds to this file's hash — so the engine refused to complete the stage
until the confirmation is retaken. Nothing about the design has changed since your
last approval; this confirms the sweep only.

### The sweep, and everything it touched

| # | What was stale | Change | Where |
|---|---|---|---|
| 1 | *"four countersignatures for one coherent design decision"* — reasoning written while the amendment was pending | Prefaced as the alternatives weighed **while pending**, "countersignatures" → "approvals", and the first bullet annotated with where the amendment was in fact applied (`CR-2026-08-22-TE-AMEND`, 2026-08-22) | `decisions.md` ADR-10 § Alternatives rejected |
| 2 | *"The record is easy to withdraw before signature"* | Rewritten: the amendment is approved, so withdrawal is now a governed change of its own — a change record plus the owner's approval before Construction builds against it, and deleting modules after | `decisions.md` ADR-10 § Reversibility |
| 3 | `\| 10 \| Four-part amendment as an obligation \| Easy before signature \| **yes** \|` | `\| 10 \| Four-part amendment — **approved 2026-08-22**, CR-2026-08-22-TE-AMEND \| Governed change to reverse \| **granted** \|`. **Found by my own sweep, not named in the Minor** | `decisions.md` § Decision summary |
| 4 | The *"18 to 19"* table row in this file | **Left in place, annotated.** This section records what was put to you on 2026-08-21 and what you agreed to; rewriting an answered question would falsify that record. The note beneath gives the current figure (21) and points at ADR-10's correction box | this file, § Consolidated Summary Confirmation (2026-08-21 pass) |
| 5 | The *"four places … has to move together"* paragraph in this file | Same treatment — left in place, annotated. The count appears in **two** places, not four. **Found by the reviewer as a Major after edit 4's sweep proved too narrow** | this file, same section |

### What the reviewer found on the sweep — verdict **READY**, 0 Critical, 1 Major, 1 Minor

- **Major, now fixed as item 5 above.** Edit 4's reasoning was sound but its sweep was too narrow: the paragraph three lines below the annotated table still asserted the superseded "four places" claim, which ADR-10's own correction box had already found wrong. This is the third time in this stage that a stale *claim* survived a sweep aimed at a stale *number* — the exact pattern `project.md` § Way of Working records.
- **Minor, not fixed, and I recommend leaving it.** The Decision summary's reworded row 10 now reads *"Governed change to reverse"* where the other nine rows use an Easy/Moderate scale, which costs comparability. Restoring a one-word rating would mean rating a governed change as *"Easy"* or *"Moderate"*, which is what made the row wrong in the first place. Accuracy over table symmetry.

### Unchanged from your last approval

The design itself is untouched by this sweep. Still carried forward, unfixed and
visible: **Critical 1** (`Transform.inverse` is specified as callable from
`Prediction.transform_id`, a `str`, with no lookup named — `ABL-DIFF`'s
inverse-to-TECU obligation has no executable path); **Major 2** (`Partition` has no
`train_start`, so *"the partition's training range"* rests on an unwritten Jan-1
convention); the three tracked deferrals **M10**, **M14**, **BLK-04/BLK-06**; and
the **`test_prepared_target_schema.py`** gap — a mandated tree member with no owning
module in this design.

Does this sweep look correct?

- Looks correct
   > **Impact**: The confirmation is retaken, the stage completes, and the approval gate comes back to you with the READY verdict and the carried findings.

- Request changes
   > **Impact**: Nothing further is edited. Tell me what to change — including reverting any of the five sweep items, or fixing the Minor after all — and I re-present.

> **💡 Recommendation**: **Looks correct** — items 1–3 remove live false claims, items 4 and 5 preserve the record of what you actually agreed to while killing the stale assertions beneath it, and the one open Minor is a formatting cost knowingly accepted to keep the row accurate.

[Answer]: Looks correct

---

## Consolidated Summary Confirmation

*(2026-08-23 — revision 4, the completion pass)*

**Nothing about the design or the sweep has changed since you approved revision 3.**
This confirmation exists only because the stage's completion check enforces an
ordering I was not working to, and the fix required re-entering the stage.

**What happened, stated plainly.** The engine requires, in this order: the human's
summary confirmation → a write to every `produces[]` artifact → the reviewer's
terminal receipt → the gate. Sweeping the Minor you ordered meant editing *this*
file, and the confirmation receipt binds to this file's hash, so the confirmation
had to be retaken — which put it **newer** than all five artifacts. Re-saving them
to satisfy the ordering would have invalidated the READY review receipt, and an
advisory stage carries a budget of one review, so no second pass was available.
A redo jump clears the receipt floor and the spent budget; that is what the
re-entry is for. It is bookkeeping, not a design change.

**The cost, so it is visible rather than absorbed:** the same trap has now fired
three times in this stage — once on the original post-review edits, once on the
count corrections, once here. Each time the trigger was an edit made after a
terminal receipt. The rule underneath it is that any edit after the reviewer's
receipt costs a full re-entry, and that includes editing this file.

### What is being confirmed

Everything already approved, unchanged and re-stated so this confirmation is
self-contained:

- **The five design edits** of revision 2: BLK-03's `expected_seeds`, M5's locked-partition month and five-manifest-rows rule, M9's bundle directory naming, M13's three-construction envelope statement, and C1's residual withdrawal of the *"unrepresentable"* claim in three places.
- **The C3 ruling** as you gave it: `lead_in_hours` withdrawn, FR-P1-04-5 restored exactly, the December scored set not enlarged by a design edit, and any future proposal routed to a separate controlled gate decision carrying rationale, scored-sample impact, leakage analysis and comparability consequences. The locked test covers **30 days, not 31**.
- **The two count corrections** of the first gate: 40 → **36** untested requirements, and ADR-10 reconciled against REQ-ENG-4's applied-and-approved **21**.
- **The five sweep items** of revision 3, including the two annotations that preserve what you were asked on 2026-08-21 rather than rewriting an answered question.
- **The three tracked deferrals** — M10, M14, BLK-04/BLK-06 — each with destination artifact, owner, due gate and acceptance test. None closed.

### Still carried forward, unfixed and visible at the gate

- **Critical 1** — `Transform.inverse` is specified as callable from `Prediction.transform_id`, which is a `str`, with no lookup or registry named and no import edge to `src/features`. `ABL-DIFF`'s inverse-to-TECU obligation has no executable path.
- **Major 2** — `Partition` carries no `train_start`, so *"the partition's training range"*, which two of the newly-fixed raises compare against, rests on an unwritten January-1 convention.
- **`test_prepared_target_schema.py`** — a mandated §12 tree member since 2026-08-22 with no owning module anywhere in this design.
- **Minor, knowingly accepted** — the Decision summary's row 10 reads *"Governed change to reverse"* against the other nine rows' Easy/Moderate scale.

Does this look correct?

- Looks correct
   > **Impact**: The five artifacts are re-saved unchanged to satisfy the write ordering, one fresh advisory review runs over them, and the approval gate comes back to you.

- Request changes
   > **Impact**: Nothing further is edited. Tell me what to change and I re-present.

> **💡 Recommendation**: **Looks correct** — no design content is in question here; this confirms bookkeeping you have already approved twice.

[Answer]: Looks correct

