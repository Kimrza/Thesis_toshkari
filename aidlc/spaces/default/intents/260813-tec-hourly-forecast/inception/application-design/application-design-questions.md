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

## Consolidated Summary Confirmation

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

