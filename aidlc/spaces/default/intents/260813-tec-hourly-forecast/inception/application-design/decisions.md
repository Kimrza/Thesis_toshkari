# Architecture Decisions — Hourly VTEC Forecasting (TEC_Project Phase 1)

Stage 2.6 (application-design), intent `260813-tec-hourly-forecast`.

## Sources

- Requirements: `../requirements-analysis/requirements.md`.
- Affirmed practices: `../practices-discovery/team-practices.md`.
- Authority: Vision v4.3, Technical Environment v3.3, `evidence/DECISIONS.md`
  D-1…D-19.
- Stage answers: `application-design-questions.md` Q1–Q8 and FU-1–FU-3, confirmed
  at the consolidated summary.

## How to read these ADRs

Ten decisions. Each carries **Context, Decision, Consequences, Alternatives
Rejected** as `phases/inception.md` § Architecture Standards requires, plus a
**Reversibility** line, since a decision that is cheap to revisit deserves less
scrutiny than one that locks the project in.

**None of these ADRs decides a scientific value.** Every threshold, seed, grid and
window length in this pipeline is frozen under D-1…D-19 or Vision §8.6, and
`project.md` § Forbidden bars an agent from filling such a value by convenience.
Where a decision *depends* on an unfrozen value, it names the hole.

---

## ADR-01 — Method-surface depth: signatures at package boundaries only

**Context.** TE §12 fixes the module tree to file level but fixes no function
signature. `component-methods.md` had to choose a depth, and `functional-design`
(3.1) runs later per unit and will specify business rules regardless. Specifying
everything risks rework; specifying nothing leaves `units-generation` (2.7) with
no contract to cut unit boundaries along.

**Decision.** Full signatures with types for **cross-package boundary calls**;
names and one-line purposes for intra-package functions. (Q1 = B.)

**Consequences.** 2.7 gets real contracts at exactly the seams it must not cut
across. Against that: intra-package structure stays unspecified, so 3.1 has real work
per unit and two type names (`Transform`, `BootstrapResult`) are referenced but
undefined.

> **⚠ The leakage half of this consequence was FALSE, and is withdrawn 2026-08-23.**
> It read: *"The leakage and phase-boundary contracts are expressible as shapes —
> `fit_transforms(train, fold)` and `apply_transforms(frame, transform)` are two
> functions precisely so that `fit_transform(all_data)` is unrepresentable."*
>
> `train` was an unconstrained `DataFrame`, so `fit_transforms(all_data, fold=F1)`
> type-checked. **This artifact's own advisory review flagged it at the time**
> (finding 2, § Review) and recommended either narrowing the claim or adding a runtime
> assertion; the claim was left standing. Stage 3.1 inherited it as an exit condition
> (BLK-04) and spent **five adversarial review cycles** failing to close it from below,
> because the gap is not one a downstream stage can close.
>
> **ADR-11 replaces the mechanism**, and it is now true by shape: `fit_transforms`
> takes a `FeatureBundle` whose `FrameSpec` states which partition and role it was
> built for, so a full-dataset fit has no argument to be passed as. The
> **phase-boundary** half of the original consequence is unaffected and stands.

**Alternatives rejected.**
- *Full signatures everywhere.* The largest artifact and the most rework, and it
  would specify `src/gnss` internals against a Phase 2 target contract that D-17
  already showed does not survive contact with the Phase 1 product.
- *Names and purposes only.* 2.7 would draw unit boundaries with nothing to cut
  along, and the IRI-denial contract would stay prose until Construction.
- *Signatures only for hard-rule packages.* Nearly right, but the boundary that
  matters is a *pair* of packages, and `external`/`gnss` sit on one side of two of
  the most important ones.

**Reversibility.** Easy. Adding intra-package signatures later costs nothing;
removing published boundary signatures would invalidate 2.7's unit boundaries.

---

## ADR-02 — Phase 1 import prohibition enforced at run time

**Context.** FR-P1-03-2 requires two independent pass/fail results for the §7.0
prohibition: an import limb and a produced-field limb.
`tests/test_phase_boundary.py` covers both in test. Nothing covered the import
limb *when the pipeline runs*. `project.md` § Mandated requires the critical test
set to run inside the Kaggle session precisely because a Kaggle session has no git
working tree, a commit hook cannot fire, and a local test run proves nothing about
the environment a governed run executes in.

**Decision.** A runtime guard, `phase_contract.assert_phase_boundary`, called at
entry by every phase-aware stage script: under `--phase 1` it asserts no
`src.gnss` module is in `sys.modules` and refuses to proceed. The test suite
becomes the second independent check rather than the only one. (Q3 = B.)

**Consequences.** The prohibition holds in the session where the governed run
actually executes. One guard, called in nine places, and `RAW_MODULES` names all
four `gnss` modules rather than the two the earlier requirement wording listed —
`target.py` and `verification.py` are raw-processing adapters and were added per
finding `IMPL-2`. Cost: nine call sites to keep correct, and a forgotten call
silently loses the runtime half.

**Alternatives rejected.**
- *Test-only.* Satisfies §7.0 as written and adds nothing to the run path, but a
  Phase 1 run in an environment where tests were not run has nothing stopping it —
  which is the exact gap `BENCH-01` identified for the test suite generally.
- *Import-time raise inside the raw modules.* Cannot be bypassed by forgetting a
  call, which is genuinely attractive. Rejected because it inverts the dependency:
  a Phase 2 module becomes conditional on Phase 1 state, and the active phase must
  be discoverable at import time, which means a module-level global. §12 already
  designates `phase_contract.py` for the boundary.
- *Both, plus tests.* Strongest on paper. Rejected as more moving parts than one
  prohibition warrants, given the produced-field limb is separately enforced.

**Reversibility.** Easy. Adding the import-time raise later is additive.

---

## ADR-03 — Two locked-test guards, deliberately separate

**Context.** The December set is opened **once** for the one-shot evaluation,
hash-before-metrics, after G-05 (Vision §5.3, G-06). But Vision §8.3 *requires* a
performance-blind December coverage and regime audit **before** G-05. So December
is legitimately read before it may be executed, and `VAL-2` found that
non-execution reads had no requirement at all — the access log showed two events
where the manifests showed four.

**Decision.** Two guards. A **path guard** (`data.locked_test.open_restricted`)
owns the access log and writes the row **before** the read, for every access
including non-execution reads. A **fold guard**
(`data.splits.materialise_locked_partition`) owns execution and refuses without a
verifying G-05 signature. (Q4 = C.)

**Consequences.** The two obligations the project keeps distinct stay distinct in
code: a permitted read cannot be mistaken for a prohibited execution, and the
required pre-G-05 audit is expressible without weakening the lock. A failed
access-log write **aborts the read** rather than proceeding unlogged. Cost: two
surfaces to keep consistent, in two modules.

**Alternatives rejected.**
- *Path guard only.* One chokepoint, matching what D-15 built. Rejected: it does
  not block *execution*, which is the G-06 obligation.
- *Fold guard only.* Sits where the locked test is conceptually defined, but
  misses the non-execution read — reproducing `VAL-2` exactly.

**Reversibility.** Moderate. Merging them later is easy; splitting them after
Construction has built one would touch every call site.

---

## ADR-04 — Experiment registry: append-only JSONL, derived CSV

**Context.** NFR-AUD-01 requires registry writes to be atomic or append-safe,
failed and aborted runs to stay visible with status and reason, and silent reruns
to be prohibited. TA-10 gates it. §13.4 permits CSV or JSONL. §13.4 and TA-10 also
assume a human reviews the registry at a gate.

**Decision.** An append-only JSONL log of run events is **authoritative**; a CSV
regenerated by folding it is **derived**, marked as such, and hashed. Status
transitions append a new row referencing the run ID rather than mutating the
original. (Q5 = C.)

**Consequences.** Append-safety is structural: removing a failed run's line would
require rewriting a file that nothing rewrites, and two `started` rows against one
`completed` makes a silent rerun visible rather than hidden. Concurrent appends do
not corrupt. The derived CSV keeps the registry reviewable without folding JSONL
by eye, and a corrupted CSV is never data loss. Cost: current state requires
folding the log, and the derived file needs its own hash.

**Alternatives rejected.**
- *Append-only JSONL alone.* Satisfies the NFR. Rejected because it leaves the
  gate reviewer folding a log by hand, which §13.4 and TA-10 assume they do not.
- *CSV with temp-file-plus-rename.* One row per run and trivially readable.
  Rejected: a crash mid-write leaves a temp file, and rename atomicity would have
  to be verified on both platforms — an obligation with no owner.

**Reversibility.** Easy for the CSV. The JSONL choice is effectively permanent
once runs exist, since re-deriving history from a rewritten format would break
`test_release_hashes.py`.

---

## ADR-05 — Determinism centralised, with the bootstrap seed carved out

**Context.** NFR-DET-01 and TC-21 require fixed seeds from `seeds.yaml`, the
three-seed element-wise mean as the confirmatory prediction, and nondeterministic
operations recorded where determinism cannot be guaranteed. §12 assigns this to no
module. Python, NumPy and TensorFlow each need seeding; TensorFlow additionally
needs op determinism configured **before** graph construction. Vision §8.6 freezes
the bootstrap seed `20221201` **independently** of the model seeds.

**Decision.** A shared determinism helper in `data.config` (the module ADR-06
creates), called at every stage entry: seeds applied to Python, NumPy and
TensorFlow; op determinism enabled before any graph construction; and the applied
seeds, framework versions, determinism settings, environment and any
non-guaranteed operations recorded in both the environment lock and the experiment
registry. Three approved model seeds, individual predictions **preserved**, the
confirmatory prediction as their element-wise mean with **sample alignment
explicitly verified** — no best-seed selection, no single-seed substitution.
`evaluation.bootstrap` builds **its own local generator** from `20221201`, read
from `seeds.yaml`, so changing a model seed cannot change a bootstrap draw.
(Q6 = X.)

**Consequences.** REQ-ENG-10's environment lock captures determinism state
automatically rather than as nine separate obligations. `three_seed_mean` **raises**
on misaligned indices and on a seed set that is not exactly the frozen three, so
selecting a best seed is unrepresentable rather than merely forbidden.
`seed_everything` **raises** if TensorFlow is already initialised, because enabling
op determinism afterwards is not equivalent — the claim Q6 explicitly bars.
Bootstrap independence is structural, not a convention. Cost: seeding is coupled
to config loading, and the bootstrap seed is read in a second place.

**Alternatives rejected.**
- *Seed in `models/train.py` only.* Sits where seeds matter most, but misses the
  bootstrap's independent seed and anything stochastic upstream.
- *Per-consumer seeding throughout.* Each consumer owns what it is accountable
  for, and bootstrap independence is explicit. Rejected as the primary scheme
  because REQ-ENG-10 requires every run to capture what it applied, and
  per-consumer seeding makes that capture nine obligations. **Its bootstrap
  carve-out was adopted.**

**Reversibility.** Easy for placement. The three-seed mean and the frozen seed
values are scientific decisions under D-122 and are **not** reversible here.

*Recorded, not resolved:* Vision §14.2 marks D-122 **"Approved — supervisor
sign-off pending"**. The seed set is frozen for implementation and still owes a
signature at G-05. `component-methods.md` carries that status rather than
concealing it.

---

## ADR-06 — A new `src/data/config.py` rather than widening an existing module

**Context.** §13.1 requires every run to snapshot and hash all four configs, and
§18.3 requires an automated assertion that no required field is `TBD` plus — per
`DATA-13` — that every declared source and hash exists. **§12's tree assigns none
of this to any module**, and `team.md` § Code Style states there is no seventh
`utils` package to put it in. TC-03e bars scientific constants from source, so the
loader must read values rather than hold them.

**Decision.** A new `src/data/config.py`, added to §12's tree as a recorded
amendment under Vision §15.2. It becomes the only module that reads `configs/`,
and it hosts the ADR-05 determinism helper and the ADR-08 platform resolver.
(Q2 = B.)

**Consequences.** Single responsibility, and the §12 responsibilities that the
release and phase-boundary tests key on stay intact. One loader means §13.7's
exact-equality requirement rests on one implementation. Cost: a §15.2 change
record and, on this project's own precedent, a supervisor countersignature — see
ADR-10.

**Alternatives rejected.**
- *`data/release.py`.* No new module, and hashing stays in one place. Rejected:
  it mixes "what a run consumed" with "what a run produced" in the module whose
  §12 responsibility the release tests key on.
- *`data/phase_contract.py`.* Keeps every gate-checked hash together. Rejected for
  the same reason — its §12 responsibility is specifically the phase boundary.
- *Each of the nine scripts loads its own.* No amendment, but nine copies, and
  §13.7's exact-equality then depends on nine implementations agreeing.

**Reversibility.** Moderate. Moving the module later is mechanical; withdrawing
the §12 amendment after Construction cites it is not.

---

## ADR-07 — Platform differences resolved at runtime, never in the governed configs

**Context.** TC-03c fixes exactly two platforms. §12 permits exactly four config
files, so a `platform.yaml` is unavailable. Roots differ (`/kaggle/working` versus
a local tree), credentials differ, and `BENCH-09` required the two-platform rule
to be falsifiable rather than asserted.

**Decision.** Credentials come from the environment (§10: platform secret stores
or environment configuration excluded from version control). Platform roots are
resolved at runtime by `config.resolve_platform_roots(env)`, and the **resolved
roots are recorded in the run's environment lock**. Every run records its
`platform` field, and a run whose platform is neither Kaggle nor local **fails**.
(Q7 = C.)

**Consequences.** No machine path enters the four governed configs, so moving a
directory never changes a governed hash and never trips §13.7's exact-equality
check on an event that is not a scientific change. The run record shows where the
data actually came from, which is what makes a cross-platform result
reproducible. The third-platform prohibition is now falsifiable by its own
evidence. Cost: the expected environment variables are documented in `README.md`
rather than enforced by a schema.

**Alternatives rejected.**
- *Environment variables only, no recording.* Nearly right, and correct on
  credentials. Rejected because it leaves no record of the roots a given run
  resolved — the reproducibility gap.
- *A platform block inside `data.yaml`.* One committed place to read the layout
  from. Rejected: it puts machine paths inside a governed config whose hash is
  checked every run, so relocating a directory would fire §13.7.

**Reversibility.** Easy.

---

## ADR-08 — `PYTHONHASHSEED` enforced by re-exec *and* in the documented sequence

**Context.** ADR-05 requires process-level determinism settings to take effect
before the interpreter initialises, and bars claiming a post-startup assignment is
equivalent. But §13.2's clean-run contract is a **literal command sequence**
beginning `python scripts/run_walking_skeleton.py --config configs/ --fixture
plumbing_7day`, and `test_clean_run.py`, WS-20 and TA-17 test that sequence as
written. Code the interpreter is already running cannot set that variable.

**Decision.** Both. Every stage script calls
`config.ensure_process_determinism(argv)` as the **first statement** of `main()`,
re-execing with the variable set when it finds it unset — so the guarantee holds
however the script is invoked. **And** §13.2's documented command sequence is
amended to carry it, so the sequence a reader follows is the whole truth. The
re-exec is recorded in `DeterminismRecord.reexec_performed` and the run log.
(FU-1 = D.)

**Consequences.** The guarantee does not depend on the reader having read the
documentation, and the documentation does not misdescribe what a correct run
looks like. The recorded re-exec flag is what stops a reviewer reading two
process starts as a double run. Cost: two changes to keep in step, and
`test_clean_run.py` must assert the amended command form — so this ADR is
coupled to ADR-10's amendment.

**Alternatives rejected.**
- *Re-exec only.* No authority change, guarantee holds. Rejected because §13.2's
  sequence would then omit a setting a correct run requires.
- *Amend the commands only.* Sequence stays the whole truth. Rejected because a
  directly invoked script — which §13.2's own sequence does nine times after the
  fixtures — would silently lose the guarantee.
- *Platform environment, record only.* Smallest change. Rejected: it weakens
  "enforce" to "record", the failure mode ADR-05's source answer was written to
  prevent.

**Reversibility.** Easy for the re-exec. The §13.2 amendment carries ADR-10's cost.

---

## ADR-09 — Phase 2 gets a governed boundary, not a designed interior

**Context.** Phase 1 is barred from executing `src/gnss/` (§7.0), and
NFR-PHASE-01 plus the phase-transition hash freeze mean Phase 2 must not drift
from a Phase 1 protocol. Those modules exist in §12's tree with stated
responsibilities. There is a live precedent for over-specifying: TE §6.1's
ten-field target row was written for Phase 2's IPP population and proved
**unsatisfiable** on Phase 1's five-column product, which is why D-17 exists.

**Decision.** Design Phase 1 fully. For `src/gnss/`, record module
responsibilities and the externally visible Phase 1 → Phase 2 interface only — no
internal signatures, no unverified scientific assumptions. The transition contract
is built from **evidence-backed Phase 1 artifacts**: observed schema, artifact
identities, SHA-256 and config hashes, approved decisions, provenance, and the
invariants Phase 2 must preserve. The observed Phase 1 schema is held **explicitly
distinct** from any future Phase 2 target schema; the ten-field contract is not
imposed on the five-column product; D-17's resolution is preserved; any later
transformation is Phase 2 work needing its own evidence and approval. The
manifest **names unresolved Phase 2 decisions rather than inventing values**.
(Q8 = B.)

**Consequences.** The frozen surface is small and evidence-backed, so G-P2 checks
manifest integrity, schema compatibility, configuration continuity and locked-test
protections rather than an invented API. `TransitionManifest.unresolved_phase2`
makes the open decisions visible instead of silently defaulted. The Phase 1 →
Phase 2 boundary is recognised as an **artifact and data contract, not a call
surface**, which is why ADR-01's signature rule does not reach `gnss`. Cost:
Phase 2 begins with real design work outstanding.

**Alternatives rejected.**
- *Design all six packages fully.* The transition manifest would have a complete
  interface to freeze. Rejected: it invites exactly the D-17 failure, freezing an
  interface against a contract no measurement has validated.
- *Leave `src/gnss` entirely to a later stage.* Smallest artifact. Rejected: the
  phase-transition freeze would have no recorded interface to compare against,
  which is what NFR-PHASE-01 exists to prevent.

**Reversibility.** Easy now, locked at G-P2 — once the manifest is signed, its
protected hashes are frozen by definition.

---

## ADR-10 — The four-part §12/§13.2 amendment, recorded as an obligation

**Context.** ADR-06, ADR-08, and the FU-2/FU-3 answers each require a change to an
authority document. Assembled, they are **four** changes, not one. This project has
a precedent: `test_acquisition_window.py` was added to §12's tree and
**countersigned 2026-08-16**.

**Decision.** Record the amendment as a single obligation covering all four items,
and **do not apply it in this stage**. `project.md` § Forbidden bars an agent from
filling a supervisor-owned value by convenience, and a tree amendment is that
class of change.

| Change | Where | Effect |
|---|---|---|
| `src/data/config.py` | TE §12 tree | REQ-ENG-1's package enumeration gains a module |
| `src/data/locked_test.py` | TE §12 tree | as above |
| `tests/test_determinism.py` | TE §12 tree | REQ-ENG-4's count rises — see the correction below for the applied figure |
| `PYTHONHASHSEED` in the clean-run commands | TE §13.2 | `test_clean_run.py`, WS-20, TA-17 test the sequence as written |

> ## ⚠ CORRECTED 2026-08-23 — THIS AMENDMENT IS ALREADY APPLIED, AND THE COUNT IS 21
>
> **Superseded, preserved:** the table row read *"**REQ-ENG-4's count goes 18 → 19**"*,
> the Consequences paragraph read *"Until it is signed, three modules and one test
> module in this design have **no authority backing**"*, and the paragraph below it
> claimed the count *"appears in REQ-ENG-4, § Requirements with no testing row,
> `team-practices.md` § Testing Posture, and the §12 enumeration"* with *"all four
> must move together"*.
>
> **All three statements were stale.** `requirements.md` REQ-ENG-4 — dated a day
> earlier, 2026-08-22 — records this amendment as **applied and approved**, and the
> mandated count as **21**, re-derived by enumerating the amended §12 tree's
> `test_*.py` entries rather than carried from prose. The route to 21, as
> `requirements.md` states it: `test_acquisition_window.py` (countersigned
> 2026-08-16, written into §12 on 2026-08-22) and `test_determinism.py` (this ADR)
> together took the tree **17 → 19** under `CR-2026-08-22-TE-AMEND`;
> `test_prepared_target_schema.py` took it to **20** under
> `CR-2026-08-22-TARGET-SCHEMA-TEST`; `test_feature_leakage_guards.py` took it to
> **21** under `CR-2026-08-22-LEAKAGE-TA`. All three 2026-08-22 acts were approved by
> the project owner under the recorded student/supervisor authority equivalence.
> **18 of the 21 are unwritten** — only `test_acquisition_window.py`,
> `test_phase_boundary.py` and `test_release_hashes.py` exist.
>
> **What this ADR should have said, and now says:** `test_determinism.py`'s
> authority backing exists. The `code-generation` prohibition in the superseded
> Consequences no longer applies to it, and repeating "until it is signed" would
> have blocked a module the owner already approved.
>
> **The earlier "four places" claim was also wrong, and its correction is
> independent of this one.** The re-entry advisory pass derived that the count
> appears in **two** places, not four. Both figures were asserted rather than
> derived, which is the `DATA-21` pattern this ADR's own next paragraph warns
> about — made twice inside the warning.
>
> **One gap remains open and is not closed by this correction.** Two of the
> twenty-one modules reached the tree after this design's package inventory was
> written. `test_feature_leakage_guards.py` **is** carried, at
> `component-dependency.md` § Forbidden edges as TA-36's evidence.
> `test_prepared_target_schema.py` (BLK-05) appears **nowhere** in this stage's five
> artifacts outside review text — no module owns the prepared-target schema
> assertion it tests. That is a real coverage gap in this design, it is **not**
> resolved here, and it is carried to the gate.

**Alternatives rejected.**
*These were the alternatives weighed when the amendment was still unsigned; they
are preserved as the reasoning that produced it, and the approval recorded in the
correction box above is what settled it.*

- *Apply the amendment here.* Rejected: not in this stage's produces list, and
  supervisor-owned. (Applied instead on 2026-08-22 under `CR-2026-08-22-TE-AMEND`,
  by the owner, in the stage that owns the change record.)
- *Four separate change records.* Rejected as four approvals for one coherent
  design decision. One record covered all four items, which is how it was approved.
- *Avoid the amendment by widening existing modules.* Rejected in ADR-06 and FU-2
  on the merits, not on cost.

**Reversibility.** *Corrected 2026-08-23: this paragraph read "The record is easy
to withdraw before signature", which was true only while the amendment was
pending.* The amendment is **approved**, so withdrawal is now a governed change of
its own rather than the retraction of an unsigned proposal. Until Construction
builds against it, that change costs a change record and the owner's approval;
after, it also means deleting modules.

---

## Decision summary

| ADR | Decision | Reversibility | Needs a human |
|---|---|---|---|
| 01 | Signatures at package boundaries only | Easy | no |
| 02 | Runtime phase-boundary guard | Easy | no |
| 03 | Two locked-test guards, separate | Moderate | no |
| 04 | Append-only JSONL, derived CSV | Easy / permanent | no |
| 05 | Centralised determinism, bootstrap carved out | Easy placement, **frozen values** | D-122 sign-off pending |
| 06 | New `src/data/config.py` | Moderate | **yes — ADR-10** |
| 07 | Runtime platform resolution | Easy | no |
| 08 | `PYTHONHASHSEED` by re-exec and amendment | Easy / coupled | **yes — ADR-10** |
| 09 | Phase 2 boundary only | Easy now, locked at G-P2 | no |
| 10 | Four-part amendment — **approved 2026-08-22**, `CR-2026-08-22-TE-AMEND` | Governed change to reverse | **granted** |

## ADR-11 — The leakage boundary is an identity check, not a containment rule

**Status.** Accepted 2026-08-23, on a backward jump from stage 3.1 directed by the
owner. Supersedes the leakage half of **ADR-01**'s consequences.

**Context.** ADR-01 claimed the two-function split made a full-dataset fit
*"unrepresentable"*. It did not: `fit_transforms(train: DataFrame, *, fold: FoldSpec)`
types `train` as unconstrained, so `fit_transforms(all_data, fold=F1)` type-checks.
This artifact's own advisory review said so at the time (finding 2) and the claim was
left standing. Stage 3.1 inherited it as **BLK-04**, an exit condition on five units,
and returned `NOT-READY` five consecutive times:

| Cycle | Mechanism | Why it failed |
|---|---|---|
| 1 | *"refuses a transform whose fold does not match the frame's partition"* | A claim, not a check — no such parameter existed |
| 2 | Derive each row's partition from timestamps | The training ranges **nest**; no single-valued label exists. Also blocked G-06 and the refit |
| 3 | Containment in the transform's own scope | The scopes are **strictly nested prefixes**; F4's transform on April passed, and F4's fit saw April |
| 4 | A required `purpose` enum | Closes `evaluate`; leaves **10 nested `train` cells**, each a truthful declaration |
| 5 | `purpose` + a call-site pairing control | Unimplementable — `05` writes features to disk, `06`/`07` read them, so no scoring site calls `apply_transforms` |

**Decision.** Four changes, together (Q9–Q12).

1. **`FoldSpec` → `Partition`**, carrying `kind: PartitionKind` (`fold` | `refit` |
   `locked`) and `validation_month: date | None`. The final refit and December become
   ordinary members of one list, so one *"exactly one role per month"* assertion walks
   one list, and December stays distinguishable from the refit **in the type** — which
   matters because December alone is access-gated.
2. **`build_features` takes a `FrameSpec`** — `partition_id`, `role`
   (`train` | `score`) and the scored range. This is the row selector the interface
   lacked. **`build_features` and `fit_transforms` both take the `Partition`(s)**, so
   the range a spec claims is **verified** rather than asserted — without that, the
   spec's fields are caller assertions and the old defect simply relocates.
3. **The check is identity, with one enumerated exception**: `build_features` raises
   `LeakageError` when `transform.partition_id != spec.partition_id`, **except** the
   single pair `REFIT` → `DEC` with `role == "score"`, which is the G-06 apply.
   Nesting is irrelevant to an id comparison. **`apply_transforms` is removed** — an
   apply that accepts any frame is the hole itself.
4. **`build_features` returns a `FeatureBundle`** carrying `matrix`, `tensor`, its
   `FrameSpec` and `transform_id`. The stamp is the same object as the data, so it
   survives the `05` → `06` handoff and cannot drift from what it describes.

**Consequences.** `fit_transform(all_data)` is **rejected at run time by a check the
argument closure can execute**: `fit_transforms` receives the `Partition`, so
comparing the bundle's scored range against that partition's training range is
computable rather than asserted. FR-P1-04-8's parity strengthens from *asserted* to
*structural*, both representations travelling in one object. The three-call sequence
leaves an untransformed bundle live in-process, closed by `06`/`07` raising on
`transform_id is None`.

> ## ⚠ THE "UNREPRESENTABLE" CLAIM IS WITHDRAWN — 2026-08-23 (C1 residual)
>
> **Superseded, preserved:** *"`fit_transform(all_data)` is now **genuinely
> unrepresentable** — `fit_transforms` takes a `FeatureBundle`, and a bundle exists
> only for a declared partition and role."*
>
> **Why it is withdrawn rather than restated in stronger words.** The `partition`
> argument makes the check **executable**; it does not make the leak
> **unrepresentable in the type**. `FrameSpec.partition_id` remains a
> caller-supplied string, and `FrameSpec(...)` remains constructible with any range —
> what changed is that constructing a wrong one now **raises** instead of passing
> silently. A run-time raise and a type-level impossibility are different guarantees,
> and this ADR's own history is the argument for not conflating them: ADR-01 made
> exactly this claim, stage 3.1 inherited it as **BLK-04**, and five review cycles
> were spent trying to make the claim true from below. The claim was the defect, not
> the mechanism.
>
> **What is now actually guaranteed, stated at its real strength:**
>
> | Guarantee | Strength | Mechanism |
> |---|---|---|
> | A transform fitted on a range other than its partition's training range | **raises** | `fit_transforms` compares `bundle.spec` against `partition`'s training range |
> | A transform applied across partitions | **raises**, except the one enumerated `REFIT` → `DEC` `score` pair | identity comparison, plus the enumerated negative control |
> | An untransformed bundle consumed for training or scoring | **raises** | `06`/`07` on `transform_id is None`; `fit_predict` likewise |
> | A `FrameSpec` naming a partition that does not exist, or a range outside what its role permits | **raises** | `build_features` takes `partitions: Sequence[Partition]` |
> | Writing `fit_transforms(some_bundle, partition=p)` at all | **not prevented** — it is a legal call that fails at run time | — |
>
> The last row is the withdrawal. **NFR-LEAK-01 is enforced by executable checks
> with named raises, and those checks are what `tests/test_train_only_transforms.py`
> asserts** — not by an interface in which the leak cannot be written. Two further
> copies of the superseded claim, in `components.md` § `src/features` and
> `component-dependency.md` § Forbidden edges, are corrected to match.
>
> Raised by the re-entry advisory review as finding 1 and carried as the residual
> limb of the owner's C1 ruling.

**Blast radius, derived by listing the units with 3.1 artifacts on disk rather than
recalled.** **Six** units must be re-checked against the new signatures:
`features-and-splits` (which authors BLK-04's contract), `models-and-baselines`,
`evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`
— the five BLK-04 names — **and `fixtures-and-reproducibility`**, which BLK-04's own
register row names and which the first draft of this ADR omitted. `fit_predict` and
`Prediction` change with them. A sweep of the 3.1 tree finds **152** occurrences of
retired identifiers — `FoldSpec` 85, `apply_transforms` 63, `build_folds` 4 — across
four files, all under `construction/features-and-splits/functional-design/`. Those
artifacts were reset by the backward jump and are rewritten when 3.1 re-runs; the
count is recorded so the rewrite is not mistaken for a light edit.

**Two owner decisions taken 2026-08-23**, after the re-entry advisory review found the
first draft wrong on both:

- **G-06's transform.** A pure identity rule raised on `REFIT` → `DEC`, which **is**
  the locked-test apply; the only alternative it permitted was fitting on December.
  The owner chose the **carve-out**: one enumerated pair, `role == "score"` only, with
  a negative control enumerating all other ordered pairs so a second exception cannot
  be added silently. The invariant is knowingly weaker than a pure identity, and that
  is recorded rather than smoothed over.
- **`lead_in_hours` removed.** It existed to let `vtec_seq_24` cross the
  November/December boundary so **1 December** could be scored — which **reverses**
  FR-P1-04-5's *"No window crosses a boundary … the first 24 h are excluded and
  counted"* and enlarges the locked-test scored set, a supervisor-owned matter under
  Vision §8.2/§8.7 and G-05. The owner chose to honour the approved requirement.
  **Consequence, which must be disclosed wherever December coverage is reported: the
  locked test covers 30 days, not 31.** The same exclusion applies to Apr, Jul, Oct
  and Nov.

**What this does not resolve, carried to the gate.** Vision §8.1's *"exactly one
partition per timestamp"* cannot run over the nesting training ranges; the
evaluation-role reading is adopted so the check can execute, but reading a frozen
Vision rule is not this stage's call.

**Alternatives rejected.**
- *Keep patching in 3.1.* Cycle six would have added the artifact stamp and a period
  selector as amendments **to** this stage's interface — 9+ owed across 4–5 units, all
  against a design that does not fit. Rejected: the amendment set was growing per
  cycle, which is the signal that the interface, not the wording, was wrong.
- *`purpose` enum plus containment* (cycle 4's mechanism, promoted here). Rejected:
  it needs two concepts where `FrameSpec.role` already carries the use, and it leaves
  the 10 nested `train` cells that identity closes for free.
- *A side-car manifest for provenance.* Cheaper than `FeatureBundle`. Rejected: this
  project has already been bitten by a derived artifact drifting from the record
  describing it (`evidence.md` fact 6), and a manifest re-creates that failure mode
  one level up.
- *Separate `RefitSpec` / `LockedSpec` types.* Rejected: every partition-taking
  function would need a union, and the exactly-one assertion would walk three lists —
  the shape that let November go unchecked in the first place.

## Assumptions & Open Questions

- **Closed as to authority, corrected 2026-08-23; one coverage gap left open.** This bullet read: *"**Open, supervisor-owned.** The four-part §12/§13.2 amendment (ADR-10). Three modules and one test module have no authority backing until it is signed."* `requirements.md` REQ-ENG-4 records the amendment as **applied and approved** on 2026-08-22 under `CR-2026-08-22-TE-AMEND`, with REQ-ENG-4's mandated count now **21**. The authority backing exists; the prohibition on `code-generation` creating these modules is lifted. **Still open, and not closed by that correction:** `test_prepared_target_schema.py` (BLK-05, a 2026-08-22 tree member) has no owning module anywhere in this design. See ADR-10 § ⚠ CORRECTED.
- **Open, supervisor-owned.** D-122's sign-off, still pending per Vision §14.2.
- **Open, supervisor-owned.** § Known defects row 12 — the `plumbing_7day` station count — blocks that fixture's manifest, which `run_walking_skeleton.py` reads.
- **Open, carried from 2.3.** The advisory `NOT-READY` finding on FR-P1-05-18: no criterion tests the storm-event count's source. ADR-05's design makes the source an explicit required argument so a test *can* assert it; writing the criterion is a `requirements.md` change.
- **Open, a §12 defect.** The `02` ordinal collision between the Phase 1 and Phase 2 target scripts. `services.md` records the reading adopted; renaming either script would be a further amendment.
> **⚠ CORRECTED 2026-08-23.** This section previously ended: *"**None** of these ADRs
> adopts a reading on a supervisor-owned value, and none decides a scientific
> constant."* The second half still holds — **no ADR here decides a scientific
> constant**, and every constant remains in `data.yaml`, `features.yaml`,
> `experiment.yaml` or `seeds.yaml` (TC-03e). The first half became false when ADR-11
> was written and is replaced by the two bullets below.

- **Readings adopted, and carried to the gate rather than settled here.** (1) Vision §8.1's *"each target timestamp belongs to exactly one partition"* is read as holding over each month's **evaluation role**, not over the training ranges, which nest and make the literal reading unsatisfiable. (2) FR-P1-04-5's *"all five partitions"* is read as F1–F4 plus the final refit, with the locked December partition recorded separately. Both are readings of approved text, and both are put to the owner at the gate.
- **Two owner decisions taken, not agent inferences**: the `REFIT` → `DEC` carve-out and the withdrawal of `lead_in_hours`. Both are recorded in ADR-11 § Two owner decisions with their consequences stated. Under the ruling of 2026-08-23, **any** proposal to use pre-December lead-in data or otherwise enlarge the December scored set is a separate controlled gate decision requiring its scientific rationale, its exact scored-sample impact, a leakage analysis and its comparability consequences — it is not decided in an application-design edit.

### Deferred obligations — tracked open, none closed

Recorded here under the owner's ruling of 2026-08-23. Each carries a destination
artifact, a named owner, a due gate and a future acceptance test. **None of these
is resolved, and none may be marked closed by the stage that inherits it without
satisfying the test named.**

| Item | Destination artifact | Owner | Due gate | Acceptance test |
|---|---|---|---|---|
| **M10** — neither mandated walking-skeleton fixture can exercise the redesigned leakage boundary. Partitions come from the frozen 2022 calendar boundaries; D-11 froze the plumbing window at 2022-11-01 to 2022-11-07, and the one-month scientific window is still open under Q-31 | A **focused contract fixture** — synthetic, tiny, and explicitly **not scientific evidence** (TC-03f) — built over synthetic partition dates, placed in the existing mandated modules `tests/test_train_only_transforms.py` and `tests/test_split_embargo.py`. Deliberately **not** a new `tests/fixtures/` directory, which would require its own §12 tree amendment | Authored by the developer at **code-generation (3.5)**; executed and evidenced by quality at **build-and-test (3.6)**, both for the `features-and-splits` unit. Fixture *window* decisions stay Student-owned under Q-31 and are untouched | **§18.3 preflight gate**, expressed as **TA-23** — *"zero unresolved P0 fields and no failing critical test"*, before any governed run | Four assertions: (a) the identity check raises for **every** ordered pair of partition ids except the one enumerated pair, asserted by enumeration over the six ids rather than by sampling; (b) `REFIT` → `DEC` with `role="score"` passes and with `role="train"` raises; (c) `fit_transforms` raises when the bundle's scored range is not exactly the partition's training range; (d) `06`/`07` and `fit_predict` raise on any bundle with `transform_id is None` |
| **M14** — `construction/inventory-and-registry/functional-design/business-logic-model.md` line 529 cites `build_features`'s signature by **line number** (`component-methods.md` line 389), an anchor this stage's amendments moved | That same 3.1 artifact | Architect, at **functional-design (3.1)** for the `inventory-and-registry` unit | That unit's 3.1 approval gate | The re-verification cites the **section heading** rather than a line number, so the anchor cannot go stale a second time |
| **BLK-04 / BLK-06 register wording** — BLK-04's remedy text still prescribes *"a `LeakageError` when `train`'s index is not a subset of that partition"*, which is the **containment rule ADR-11 explicitly rejects**; the register therefore contradicts the ADR that supersedes it | `unit-of-work-story-map.md`, produced by **units-generation (2.7)** — the next stage | Architect (lead), with delivery support, at units-generation | The units-generation approval gate | The BLK-04 remedy text matches ADR-11's identity-plus-one-enumerated-exception mechanism, and **no containment wording survives** anywhere in the register |

## Review

READY

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `component-methods.md` lines 419–428 (`three_seed_mean`) | The signature `three_seed_mean(predictions: Sequence[Prediction]) -> Prediction` takes no config/seeds parameter, yet its prose claims it `raises SeedError ... when their seeds are not exactly the frozen set`. The frozen set is `{1337, 2024, 7}` (D-122, restated in `requirements.md` FR-P1-05-2), a value that must live in `seeds.yaml` per TC-03e/project.md § Forbidden ("NEVER hide a scientific constant in source code"). With no `ConfigSnapshot`/`seeds` argument, the function can only be implemented one of two ways: (a) hardcode `{1337, 2024, 7}` inside `src/models`, which is exactly the forbidden pattern, or (b) check only "exactly three, pairwise distinct" `Prediction.seed` values, which is weaker than "exactly the frozen set" and would pass a wrong-but-distinct triple undetected. Contrast `vector_block_bootstrap` a few sections later, which correctly takes `seed: int` as a required parameter "read from `seeds.yaml`, never defaulted and never inlined" for the identical reason. `three_seed_mean` is missing the analogous parameter, so ADR-05's claim that "selecting a best seed... is unrepresentable rather than merely forbidden" is not actually true of this signature as written. | Add a frozen-seed-set parameter (e.g. `expected_seeds: frozenset[int]`, sourced from `ConfigSnapshot.seeds` at the call site) to `three_seed_mean`, so the comparison is against the configured value rather than an inlined constant or a weaker distinctness check. |
| 2 | Major | `component-methods.md` lines 386–392 (`fit_transforms`/`apply_transforms`); `decisions.md` ADR-01 lines 40–42 | The two-function split is claimed to make "`fit_transform(all_data)` ... unrepresentable in this interface, which is how NFR-LEAK-01 is enforced by shape rather than by review." That is true only of the specific single-function call shape. The signature `fit_transforms(train: DataFrame, *, fold: FoldSpec) -> Transform` types `train` as an unconstrained `DataFrame` — nothing in the shape stops a caller from writing `fit_transforms(all_data, fold=f)` (fitting on the full dataset, the exact leak NFR-LEAK-01 forbids) followed by `apply_transforms(...)`. The split prevents one convenience call, not the underlying leak; the leak is still fully representable and would require review (or a runtime check inside `fit_transforms` comparing `train`'s index against the fold's training window) to catch, contradicting the "by shape rather than by review" claim. | Either narrow the claim in ADR-01/`component-methods.md` to "prevents the single-call convenience shape" rather than "makes the leak unrepresentable," or add a runtime assertion inside `fit_transforms` that `train`'s index is a subset of `fold`'s training partition (raising `LeakageError` otherwise), which would make the claim true. |
| 3 | Major | `decisions.md` ADR-10 table, lines 372–390 | ADR-10 claims REQ-ENG-4's test-module count "appears in REQ-ENG-4, § Requirements with no testing row, `team-practices.md` § Testing Posture, and the §12 enumeration" and "all four must move together" from 18 to 19 when `test_determinism.py` is added. Two of those four citations are checked and do not carry the count claimed: (a) `requirements.md` § Requirements with no testing row (lines 736–753) is a list of 40 untested *requirement* IDs, not a test-module count — it never states "18" or any test-module total; (b) `practices-discovery/team-practices.md` § Testing Posture (line 184) states "**The mandated test set is 17 modules, not 2**" and enumerates exactly the 17 §12-tree modules, deliberately excluding both `test_acquisition_window.py` (the already-countersigned 18th, mentioned separately in that same file's § Way of Working, line 116) and the not-yet-countersigned `test_determinism.py`. That "17" is not the same count as REQ-ENG-4's current "18" and was never claimed to be — so it is not a place where a count "goes 18 → 19"; updating it to 19 would misstate what that section deliberately scopes. Only REQ-ENG-4 itself (`requirements.md` line 266, correctly stating 18 today) and the external TE §12 tree are genuine loci of this count. | Correct ADR-10's table to name the two real loci (REQ-ENG-4 and the TE §12 tree/§13.2 amendment) and drop or re-scope the other two citations; if `team-practices.md` § Testing Posture is meant to eventually track the full mandated set including amendment-added modules, say so explicitly rather than implying its current "17" is the same count as REQ-ENG-4's "18." |
| 4 | Minor | `services.md` § Known defects cross-reference; `components.md` Assumptions | Both artifacts correctly carry forward the unresolved `plumbing_7day` station-count conflict and the `02` ordinal collision as open items rather than resolving them by convenience — noted here only so the approval gate sees both are still open, not fixed, going into `units-generation`. | None required; confirm these two items are visible to whoever signs the amendment in ADR-10. |

### Validation Tool Results

No validation tooling is listed for this stage beyond the `required-sections` and `upstream-coverage` sensors (frontmatter), which are structural checks the orchestrator runs automatically; no separate CLI validator was invoked for this advisory pass. Cross-references were verified manually against `requirements.md`, `practices-discovery/team-practices.md`, `evidence/DECISIONS.md`, and the Technical Environment/Vision authority documents, with line citations given per finding above.

### Summary

The five artifacts are internally coherent on the large structural questions (module tree, phase boundary, dependency matrix, IRI/GIM allowlist scoping, the fourteen protected-hash count, the D-144 acquisition-notebook exception) and would let `units-generation` draw unit boundaries without inventing a governance decision. The three Major findings are the class of defect this project's governance has repeatedly caught: two are signatures that claim to make a leakage/selection path "unrepresentable" or "checkable" when the shape as written cannot actually perform the check without either an unstated dependency or a hidden scientific constant, and one is an internal count-tracking claim (ADR-10) that names a citation which does not carry the count it claims. None is a blocking architectural flaw at this stage (all three are fixable by adding a parameter or narrowing a claim), so the verdict is READY with these findings routed to the human for triage before Construction inherits them.

---

## Review — 2026-08-23 re-entry pass (ADR-11 scope)

> The 2026-08-22 advisory review above is **preserved unchanged**. This section
> reviews **only** the ADR-11 re-entry changes to `src/features` and
> `src/data/splits.py` (Q9–Q12). Q1–Q8 and FU-1–FU-3 were not reopened and are not
> re-reviewed.

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-23T09:30:07Z
**Iteration:** 2 (re-entry, advisory class, single pass)
**Scope reviewed:** `components.md` § `src/features`; `component-methods.md`
§ `src/data/splits.py`, § The `src/features` leakage boundary, § `src/models`;
`services.md` § The nine stage scripts and the `05`→`06` box;
`component-dependency.md` § Forbidden edges (the four new rows); `decisions.md`
ADR-01 withdrawal box and ADR-11.

### Prior findings — status

| Prior # | Status under ADR-11 |
|---|---|
| 1 (`three_seed_mean` has no frozen-seed parameter, BLK-03) | **Unresolved.** `three_seed_mean(predictions)` is unchanged; `fit_predict` was re-signed immediately beside it and the seed parameter was still not added. Not re-raised as new — it is BLK-03 and outside this re-entry's scope. |
| 2 (`fit_transforms` claim false — BLK-04) | **Not resolved. Reproduced in a new shape.** See finding 1: the unconstrained argument moved from `train: DataFrame` to `FrameSpec`'s scored range, and the check that would close it is again specified in prose the signature cannot execute. |
| 3 (ADR-10 count loci) | Untouched by this re-entry; not re-raised. |
| 4 (open items visible at the gate) | Still open and still visible. |

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | **Critical** | `component-methods.md` § The `src/features` leakage boundary — `fit_transforms(bundle: FeatureBundle) -> Transform` and the `FrameSpec` dataclass; `decisions.md` ADR-11 § Consequences (*"`fit_transform(all_data)` is now genuinely unrepresentable"*) | **The full-dataset fit is still representable, by the same structural error ADR-01 made.** The prose says `fit_transforms` *"raises `LeakageError` … when the bundle's scored range is not its partition's training range."* `fit_transforms` receives **only** a `FeatureBundle`. `FeatureBundle` carries `matrix`, `tensor`, `spec: FrameSpec`, `transform_id`; `FrameSpec` carries `partition_id`, `role`, `scored_start`, `scored_end`, `lead_in_hours`. **No argument in that closure carries any partition's training range** — no `Partition`, no `Sequence[Partition]`, no `ConfigSnapshot`, hence no way to reach `build_partitions(snapshot)`. The check is unimplementable from the arguments given, exactly as prior finding 1 showed for `three_seed_mean`'s frozen seed set. No other raise fills the gap: `build_features`'s enumerated raises (§6.2 dictionary, carried-forward `vtec_lag_*`, incomplete `vtec_seq_24`, support field, target-hour quality field, raw longitude, driver beyond 3 h, plus the identity check) **contain no validation of `spec.scored_start`/`scored_end` against the declared partition**. The leak is three legal calls: `raw = build_features(..., spec=FrameSpec("F1", "train", 2022-01-01, 2022-11-30))` → `T = fit_transforms(raw)` → `build_features(..., spec=FrameSpec("F1","train",…), transform=T)`. Every call type-checks, the identity check passes (both say `F1`), and `T` was fitted on all of January–November. `partition_id` is a **caller-asserted string**, not a constrained value; substituting a string for a `DataFrame` as the unconstrained argument relocates the hole rather than closing it. | Give `fit_transforms` the partition it claims to check against — `fit_transforms(bundle: FeatureBundle, *, partition: Partition) -> Transform` — and specify the raise concretely: `LeakageError` when `bundle.spec.scored_start`/`scored_end` do not equal `partition`'s training range, when `partition.partition_id != bundle.spec.partition_id`, when `role != "train"`, or when `transform_id is not None`. Correspondingly specify a raise in `build_features` validating `spec` against a `Partition` (it already receives `snapshot` and could resolve the list, but the design must say so). Until a named argument carries the training range, ADR-11's "genuinely unrepresentable" claim must be **withdrawn**, not restated — the same withdrawal ADR-01 needed. |
| 2 | **Critical** | `component-methods.md` § The `src/features` leakage boundary (the identity check and the three-call sequence); § `src/data/splits.py` (`Partition.partition_id # "F1".."F4", "REFIT", "DEC"`); `decisions.md` ADR-11 decision 3 | **The identity check forbids the one apply the locked test requires, and the only path it leaves open is the leak.** G-06 scores December with the model refit on January–November (FR-P1-04-14; `project.md` § Mandated, locked-test predictions generated once after G-05). Stage 3.1 established this explicitly and recorded it as resolved: `construction/features-and-splits/functional-design/business-logic-model.md` § Review, iteration-2 remedy — *"December **only** through a frame materialised by `materialise_locked_partition` …, **with the transform being the final refit's**"* — and iteration 3 confirms *"R-74's controls that must not fire now assert that the refit→December apply **passes**."* Under ADR-11 that apply is `build_features(spec=FrameSpec("DEC","score",…), transform=T_REFIT)`, which **raises `LeakageError`**, because `"REFIT" != "DEC"`. The identity check has no exception, no `kind`-aware branch, and no scoring-transform concept. The only representable alternative is a transform whose `partition_id == "DEC"` — obtainable solely by `fit_transforms` on a `FrameSpec("DEC","train",…)` bundle, i.e. **fitting a transform on December**, the leak NFR-LEAK-01 exists to prevent, which no `g05_signature` gate touches. The three-call sequence is written for a generic partition *k* and never states which transform December uses; Q9–Q12 never ask. **The single evaluation this thesis turns on has no lawful path.** | Separate the two identities the check conflates: the partition a frame's **rows** belong to, and the partition whose transform may be applied to it. State it as an explicit closed relation rather than an equality — `Transform.partition_id` must be `spec.partition_id` **or** the partition declared as `spec.partition_id`'s scoring source, with `Partition` carrying that source (`REFIT` for `DEC`, self for a fold). Name the December case in `component-methods.md`, in ADR-11 decision 3, and in the three-call sequence, adding a fourth call showing the locked evaluation end to end. Any resolution permitting a `"DEC"`-stamped transform to be fitted must be rejected outright. |
| 3 | **Critical** | `component-methods.md` § The `src/features` leakage boundary (*"`lead_in_hours` makes the history rows explicit"*); `application-design-questions.md` Q10 impact text; `decisions.md` ADR-11 decision 2 and § Assumptions (*"None of these ADRs adopts a reading on a supervisor-owned value"*) | **`lead_in_hours` reverses an approved requirement criterion and changes the December scored row set, without recording that as a supervisor-owned reading.** `requirements.md` FR-P1-04-5's pass/fail criterion reads, verbatim: *"**No window crosses a boundary**; the split manifest records the excluded count and enumerates all five partitions"*, and its rule text states *"the first 24 h are excluded and counted"*. FR-P1-04-13 states `vtec_seq_24` *"is excluded when incomplete"*. Both are tested (WS-12, TA-11, TA-34). ADR-11 defines `lead_in_hours` precisely so a December score frame **contains late-November rows** — a window crossing the November/December partition boundary — and so 1 December **is scored** rather than excluded. That is not a refinement of the approved criterion; it is its negation, and it enlarges the locked-test evaluation window by roughly 24 hourly rows per cell. The scored set of the locked test is supervisor-owned (Vision §8.2, §8.7; G-05), and `project.md` § Forbidden bars filling such a value by convenience. The artifacts present this as fixing a "silent drop"; FR-P1-04-5 makes that drop **explicit and counted**, which is the opposite of silent. | Do not carry this to Construction as a design decision. Restate it at the approval gate as a **supervisor question**: does the locked-test evaluation score the first 24 h of December on November history, or does FR-P1-04-5's exclusion-and-count stand? If the exclusion stands, `lead_in_hours` is a loading convenience with no effect on the scored set and must say so. If it does not, FR-P1-04-5's criterion, FR-P1-04-13, WS-12 and TA-11 change together under a §15.2 change record — a `requirements.md` change outside this stage's produces list. Remove ADR-11's *"None of these ADRs adopts a reading on a supervisor-owned value"* line, or make it true. |
| 4 | **Critical** | `component-methods.md` § `src/data/splits.py` (`assert_membership_from_timestamps` and its 2026-08-23 "What this does NOT do" box) against § The `src/features` leakage boundary (`lead_in_hours`) | **The two mechanisms added on the same day contradict each other, and the "not scored" half is enforced nowhere.** `assert_membership_from_timestamps` *"**Raises** on any row whose month or year disagrees with its partition"*. `lead_in_hours` **requires** a December score frame to contain November rows and an April score frame to contain March rows. Run the guard over any score frame built as ADR-11 specifies and it raises; scope it away from score frames and it no longer covers the frames where a mis-filed row actually reaches a metric. Neither passage scopes one against the other. Separately, **nothing drops the lead-in rows before scoring**: `fit_predict(model_id, *, bundle, partition, snapshot)` receives the whole bundle, and no function is specified as restricting prediction to `[scored_start, scored_end]`. `Prediction.frame` therefore carries lead-in rows, `build_comparison_mask` intersects over them, and the "present but never scored" contract stated on `FrameSpec` is a claim in prose with no check behind it — the exact pattern that produced BLK-04. | State the interaction explicitly: `assert_membership_from_timestamps` applies to rows within `[scored_start, scored_end]` only, lead-in rows exempt by construction. Then give the "not scored" half a mechanism: specify that `fit_predict` emits predictions **only** for rows inside the bundle's scored range and raises otherwise, or that `FeatureBundle` carries an explicit scored-row mask, and add the corresponding row to `component-dependency.md` § Forbidden edges. |
| 5 | Major | `component-methods.md` § `src/data/splits.py` (`Partition`); `requirements.md` FR-P1-04-5 | **Partition cardinality conflicts with the approved criterion, and the locked partition cannot say which month it evaluates.** `Partition.partition_id` is commented `"F1".."F4", "REFIT", "DEC"` — **six** ids. FR-P1-04-5's pass/fail criterion requires the split manifest to *"enumerate all **five** partitions"*, and its rule text lists `F1`–`F4` plus `Final refit: 1 Jan – 30 Nov`. Six against five is a count a governance board will find, in the same class as `DATA-21`. Compounding it, `validation_month: date | None` is annotated *"None for refit and locked"* — so `Partition("DEC", kind=locked, …)` **cannot record December as its evaluated month**, the one fact that partition exists to carry. Q9=C was chosen expressly so *"December stays distinguishable from the refit in the type"*; the field that would distinguish them is `None` in both, leaving `kind` as the sole discriminator and no evaluated window anywhere in the type. | Reconcile the count in one place: either `DEC` is a sixth `Partition` and FR-P1-04-5's criterion changes under a §15.2 record (outside this stage — raise it at the gate), or `DEC` is not a `Partition` and finding 2's December path must be expressed otherwise. Whichever holds, give the locked partition its evaluated month (`validation_month` is `None` only for `kind == refit`), so `kind` is not carrying the whole distinction alone. |
| 6 | Major | `component-methods.md` § The `src/features` leakage boundary (*"`apply_transforms` is removed"*); `component-dependency.md` § Dependency matrix, row `src/evaluation` | **Removing `apply_transforms` closed a legitimate path with no replacement: the inverse transform.** `project.md` § Mandated requires that *"`ABL-DIFF` inverse-transforms to absolute TECU before any metric"*, and every reported quantity — the paired loss differential, the bootstrap interval, the practical-relevance threshold — is in TECU. If the train-only transform touches the target, model output is in transformed space and something must invert it before `paired_loss_differential`. After ADR-11: `Transform` exposes no inverse (its *"fitted state is intra-package"*), transforms are applied *"only inside `build_features`"*, `Prediction` carries `model_id`, `seed`, `frame`, `target_definition_id`, `phase_id`, `source_id` and **no transform identity or unit**, and the dependency matrix gives `src/evaluation` **no import edge to `src/features`** (that cell is `—`). No module that needs the inverse can obtain it. On the re-entry brief's question: the evaluation-time IRI/GIM join and the bootstrap resampling do **not** need an apply; ABL-DIFF and unit restoration do, and the design no longer expresses them. | State whether the transform touches the target. If it does, add an inverse to the boundary (`invert(transform, frame) -> DataFrame` in `src/features`, plus the `features` import edge for `src/evaluation`, or an `inverse_transform_id` on `Prediction` with a named owner) and add a `component-dependency.md` row for it. If it does not, say so explicitly in `component-methods.md` and in ADR-11's consequences, so ABL-DIFF's obligation is visibly satisfied rather than silently assumed. |
| 7 | Major | `services.md` § The nine stage scripts (the `07_evaluate_and_report.py` row) against its own ⚠ box, `component-dependency.md` (two of the new rows), and `component-methods.md` § The `src/features` leakage boundary | **`07` is claimed to assert on `FeatureBundle`s it is not recorded as reading.** The script table was amended for `05` (writes `FeatureBundle`s) and `06` (reads `FeatureBundle`s, partitions). The `07` row was **not**: it still reads *"predictions, benchmark, mask"*. Three separate passages nonetheless say `07` raises on `transform_id is None` and asserts `spec.partition_id` / `spec.role` off the bundle. Both cannot be true, and the reachable reading is the worse one: since `Prediction` carries no `partition_id` and no `transform_id`, **all bundle provenance dies at `06`**, so `07` has nothing to assert on and the `05`→`06` stamp never reaches the stage that computes the reported numbers. | Pick one and make all four locations agree. The stronger fix propagates rather than re-reads: add `partition_id: str` and `transform_id: str` to `Prediction`, have `fit_predict` copy them off `bundle.spec`, and let `07` assert against the prediction. Then correct the `07` reads column, or add `FeatureBundle`s to it if `07` genuinely reloads them. |
| 8 | Major | `services.md` ⚠ `05`→`06` box (*"persisted and reloaded **as one unit**"*); `decisions.md` ADR-11 decision 4 and its rejected *"side-car manifest"* alternative | **`FeatureBundle` is asserted persistable as one unit with no format named, and the rationale for rejecting a manifest does not survive §13.3.** The bundle is a `DataFrame` + an `NDArray` + a frozen dataclass. No single mainstream format holds all three: Parquet does not carry the tensor, `.npz` does not carry the frame, and `pickle` is not byte-stable across NumPy/pandas versions — colliding directly with NFR-DET-01, TE §13.7's exact-equality hash check, and `test_clean_run.py`/WS-20/TA-17, which compare artifacts by hash across a clean run. Meanwhile TE §13.3 **requires** every release to record a version, source manifest, SHA-256 hashes, schema, row counts, exclusions and fold/mask identifiers, gated by `test_release_hashes.py`/TA-15 — so a manifest describing this artifact **will exist regardless**, and ADR-11's rejection of option B because *"a manifest is a separate file … so the two can drift"* does not remove the failure mode it names. The advantage `FeatureBundle` genuinely buys is in-process type safety; the on-disk claim is unevidenced. | Name the on-disk form and its determinism story: a bundle directory with a fixed layout (`matrix.parquet`, `tensor.npy`, `spec.json`) hashed per file into the §13.3 manifest is the honest version and keeps the in-process guarantee intact. Narrow ADR-11 decision 4 and the ⚠ box to what is true — the stamp is inseparable **in memory**, and on disk it is a §13.3 release like every other artifact. |
| 9 | Major | `component-methods.md` § The `src/features` leakage boundary (the three-call sequence); `services.md` § The nine stage scripts (`05` writes) | **`FrameSpec` is not a unique key, so the `05`→`06` handoff has no unambiguous address.** In the published sequence `raw` and `train` carry **identical** `FrameSpec` values — same `partition_id`, same `role`, same scored range, same lead-in — differing only in `transform_id` (`None` against `T_k`). Two distinct artifacts with the same stamp is precisely the addressing problem `FeatureBundle` was introduced to solve. Nothing forbids `05` from persisting `raw`; `06`'s `transform_id is None` raise catches consumption but not a same-key overwrite, nor a mis-selection between two files whose specs are equal. | Make bundle identity unique: either forbid persisting a bundle with `transform_id is None` (a stated rule in `services.md` and a row in `component-dependency.md` § Forbidden edges), or give `FeatureBundle` a `bundle_id` derived from `(spec, transform_id)` and address the handoff by it. |
| 10 | Major | `component-methods.md` § The `src/features` leakage boundary; `services.md` § Ordering contract; `team-practices.md` § Walking Skeleton (D-11, D-20) | **The redesigned boundary cannot be exercised by either mandated fixture.** Partitions come from `build_partitions(snapshot)` over the frozen 2022 calendar boundaries. D-11 froze the plumbing window at **2022-11-01 to 2022-11-07** (station BSHM under D-20). That window lies **inside the training range of every partition** and is **no partition's validation month**, so no legal `FrameSpec(k, "score", …)` exists over fixture data — and finding 1's remedy, requiring the scored range to equal the partition's training range, would make the fixture's `train` frame illegal too. Yet WS-12 (splits/embargo), WS-13 (matrix/tensor window parity) and WS-20 (clean-CPU reproduction of **both** fixtures) are Phase 1 acceptance rows, and `project.md` § Mandated requires both fixtures to run inside the Kaggle session before any governed run. The design states no fixture-partition derivation. | Specify how partitions are derived for a fixture run: either `build_partitions` accepts the fixture window and emits scaled partitions, or the fixture declares its own partition list in `tests/fixtures/<id>/fixture_manifest.yaml` beside the row counts and tolerances that file already owns. Name it in `component-methods.md` and in `services.md` § Ordering contract, and note the dependency on BLK-02 (that manifest does not yet exist). |
| 11 | Major | `decisions.md` ADR-11 § Consequences (the five named units) | **The blast radius is named inaccurately and understates what is already written.** ADR-11 names five units to re-check: `features-and-splits`, `models-and-baselines`, `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`. The blocker register's own BLK-04 row says the change *"reaches **every** unit downstream of features … **including `fixtures-and-reproducibility`**, whose clean-run tolerance comparison and TA-21 traceability matrix consume those artifacts"* — that unit is **absent** from ADR-11's list, and finding 10 shows the fixture path is materially affected. ADR-11 also names **no already-written 3.1 artifact**, though seven units have `functional-design/` artifacts on disk today and a derived scan finds **152 occurrences of the retired identifiers** (`FoldSpec` ×85, `apply_transforms` ×63, `build_folds` ×4) across **4 files**, all under `construction/features-and-splits/functional-design/`. Separately, BLK-04's remedy text in `unit-of-work-story-map.md` still prescribes *"a `LeakageError` when `train`'s index is not a subset of that partition"* — the **containment rule ADR-11 explicitly rejects** — so the register now contradicts the ADR that supersedes it. | Add `fixtures-and-reproducibility` to ADR-11's consequences. Name the invalidated artifacts by path and derived count rather than by unit alone, so the 3.1 re-entry has a checklist. Flag that BLK-04's and BLK-06's register entries need re-wording — a `unit-of-work-story-map.md` change outside this stage's produces list, and therefore a gate item, not an edit. |
| 12 | Minor | `component-methods.md` § The `src/features` leakage boundary (`FrameSpec.lead_in_hours: int = 24`); § `src/data/splits.py` (`Partition.embargo_hours: int = 24`) | **`lead_in_hours` is caller-supplied, defaulted and unvalidated.** No raise is specified for `lead_in_hours=0` — which silently reinstates the dropped-first-24-h behaviour the field was added to prevent — nor for an arbitrarily large value pulling the whole year into a score frame. Its relation to `embargo_hours` is unstated although both default to 24 and they govern adjacent rows on the same boundary. And it is not said whether the lead-in slices `drivers` as well as `target`: if it does, `f107_81_trailing`'s **81-day** trailing window cannot be satisfied by a 24-hour lead-in, and `assert_lags_safe`'s anchor check (`TEC-13`) has no data to check against. | State that `lead_in_hours` bounds the **target** history only and that driver series arrive complete from `04_build_external_products.py` with `f107_81_trailing` pre-computed; specify the raise when `lead_in_hours` is insufficient for the widest configured target-derived lag (24 h for `vtec_seq_24` / `vtec_lag_24h`), read from `features.yaml` rather than defaulted; and state the invariant relating it to `embargo_hours`. |
| 13 | Minor | `services.md` § Resource envelope | **The three-call sequence's cost is not reflected in the envelope.** ADR-11 replaces one apply with a **full rebuild**: `build_features` is the only place transforms are applied, so producing `raw`, `train` and `score` for one partition is **three complete feature constructions**, with three `matrix`+`tensor` pairs live simultaneously; over six partition ids that is 18 full builds per run. TE §9.3's 10.0 GB is a **hard** planning envelope on a CPU-only path (TC-01, TC-03, TC-03g), and § Resource envelope was not amended in this re-entry — it still names `07` as the heaviest stage. | Add a line to § Resource envelope acknowledging the rebuild multiplier and stating that `raw` is released before `train` is built, or amend the sequence so the untransformed bundle is not held alongside the transformed one. Measure rather than assert once the fixtures exist (BLK-02). |
| 14 | Minor | `construction/inventory-and-registry/functional-design/business-logic-model.md` line 529 | A 3.1 artifact cites `build_features`'s signature by **line number** (`component-methods.md line 389`), which this amendment moved. Noted only so the 3.1 re-entry does not re-verify against a stale anchor. | No action in this stage; fold into finding 11's checklist. |

### Validation tool results

| Check | Result | Interpretation |
|---|---|---|
| Stage-declared validators | none beyond the `required-sections` / `upstream-coverage` / `claim-sources` sensors the orchestrator runs | No CLI validator was available to invoke; every finding below is manual cross-reference with the location named. |
| Derived count — retired identifiers in written 3.1 artifacts | `FoldSpec` 85, `apply_transforms` 63, `build_folds` 4 = **152** occurrences across **4** files, all under `construction/features-and-splits/functional-design/` | Supports finding 11. Derived by scan, not carried from prose. |
| Derived count — units with 3.1 artifacts on disk | **7** (`acquisition`, `external-products`, `features-and-splits`, `foundation`, `governance-guards`, `inventory-and-registry`, `target-standardization`) | Only one of the five units ADR-11 names has 3.1 artifacts written, so the rework burden is narrower than the unit list implies — and wider than ADR-11 states in the fixture direction. |
| Derived count — `Partition` ids against FR-P1-04-5 | 6 (`F1`–`F4`, `REFIT`, `DEC`) against the criterion's *"all five partitions"* | Supports finding 5. |
| Cross-unit spot-check (permitted: the design names this integration point) | `construction/features-and-splits/functional-design/business-logic-model.md` § Review, iterations 2–4 | Confirms the refit→December apply is the resolved required path — the path finding 2 shows the identity check forbids. |

### Summary

ADR-11 fixes three real defects — `FoldSpec` could not express the refit, `build_features`
had no row selector, and nothing stamped the emitted artifacts — and
`Partition` / `FrameSpec` / `FeatureBundle` are the right vocabulary for all three. But the
central claim is false in the same way ADR-01's was: `fit_transforms` is handed a
`FeatureBundle` whose `FrameSpec` range **nothing validates and nothing in its argument
list can validate**, so `fit_transform(all_data)` is still three legal calls away
(finding 1). Worse, the identity check that replaced containment **forbids the
refit→December apply that G-06 requires and that stage 3.1 had already resolved**,
leaving a December-fitted transform as the only representable alternative (finding 2).
And `lead_in_hours` reverses FR-P1-04-5's approved *"no window crosses a boundary …
the first 24 h are excluded and counted"* criterion, enlarging the locked-test scored
set — a supervisor-owned change the ADR records as no supervisor-owned reading at all
(finding 3). Four Critical, seven Major, three Minor. This pass is **advisory**: nothing
here is applied, and the verdict informs the approval gate rather than gating it. The
recommendation to the gate is that findings 1, 2 and 3 be resolved **in this stage**
before 3.1 re-enters, because each is the same class of gap that cost 3.1 five review
cycles — a check stated in prose that the signature cannot execute.

**Verdict:** NOT-READY

---

## Review — 2026-08-23 fix pass

> The 2026-08-22 advisory review and the 2026-08-23 re-entry pass above are both
> **preserved unchanged**. This section reviews the fix-pass edits made under the
> owner's 2026-08-23 rulings (§ Consolidated Summary Confirmation, revision 2, in
> `application-design-questions.md`): the `fit_transforms`/`build_features`
> partition parameter (C1), the `REFIT`→`DEC` carve-out (C2), the withdrawal of
> `lead_in_hours` (C3/C4), `three_seed_mean`'s `expected_seeds` (BLK-03), the
> five-vs-six `Partition` reconciliation (M5), the bundle-address naming rule (M9),
> the resource-envelope statement (M13), the blast-radius correction (M11), the
> restored `Transform.inverse` (M6), the `07` read-column correction (M7), the
> on-disk bundle form (M8), and the three-place withdrawal of the
> "unrepresentable" claim (C1-residual) — against both the artifacts themselves
> and the upstream `requirements.md` / `team-practices.md` contracts.

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-23T14:08:58Z
**Iteration:** 3 (fix pass, advisory class, single pass)
**Scope reviewed:** All five produces artifacts as they now stand
(`components.md`, `component-methods.md`, `services.md`,
`component-dependency.md`, `decisions.md`), cross-referenced against
`../requirements-analysis/requirements.md` and
`../practices-discovery/team-practices.md` (consumes), plus the one permitted
spot-check of `construction/features-and-splits/functional-design/business-logic-model.md`
§ Review. Deferred items M10, M14 and the BLK-04/BLK-06 register wording were
checked only for tracking accuracy, per the dispatch brief, and are not
re-litigated on their merits.

### Prior findings — status

| Prior # (2026-08-23 re-entry pass) | Status under this fix pass |
|---|---|
| 1 (Critical, C1 — `fit_transforms` could not execute its claimed raise) | **Resolved.** `fit_transforms(bundle: FeatureBundle, *, partition: Partition)` now receives the partition; the raise (`role != "train"`, already-transformed, `partition_id` mismatch, scored range not the partition's training range) is executable from the argument closure `component-methods.md` §§ `src/data/splits.py`/leakage boundary now specify. See new finding 4 below for a residual gap in what "the partition's training range" means as a value. |
| 2 (Critical, C2 — identity check forbade the required G-06 apply) | **Resolved.** The single enumerated exception `REFIT`→`DEC`, `role == "score"`, with a negative control over the other five ordered pairs, is specified in `component-methods.md` § ⚠ ONE ENUMERATED EXCEPTION and `decisions.md` ADR-11 decision 3. |
| 3 (Critical, C3/C4 — `lead_in_hours` reversed FR-P1-04-5 and contradicted the timestamp-membership guard) | **Resolved by withdrawal.** `lead_in_hours` is removed from `FrameSpec` everywhere; a scan of all five artifacts finds no live field definition or call site left (only the historical ⚠-boxed record and the Q&A history, both correctly framed as superseded). `assert_membership_from_timestamps` and the scored-range bound no longer conflict because there is no lead-in row to conflict over. |
| 5 (Major, M5 — six `Partition` ids against FR-P1-04-5's "five") | **Resolved, as a disclosed reading rather than a silent fix.** The split manifest is now stated to enumerate exactly F1–F4 and `REFIT` (five), with `DEC` recorded separately as the access-gated locked partition carrying `validation_month = 2022-12-01`. Checked against `requirements.md` FR-P1-04-5's verbatim criterion (`requirements-analysis/requirements.md` line 374): "the split manifest records the excluded count and enumerates all five partitions... The partition list also carries `Final refit: 1 Jan – 30 Nov`" — December is described as "locked," not as one of the enumerated five, so this reading is textually defensible, and `decisions.md` § Assumptions correctly carries it to the gate as a reading rather than presenting it as settled. |
| 6 (Major, M6 — no inverse transform after `apply_transforms`'s removal) | **Not resolved — reproduced in a new shape.** See new finding 1 below. |
| 7 (Major, M7 — `07`'s reads column contradicted its own assertions) | **Resolved.** `services.md` line 54 now reads "predictions (**carrying `partition_id` and `transform_id`**), benchmark, mask," matching `Prediction`'s two added fields in `component-methods.md` § `src/models` and the assertions described in the `05`→`06` box. |
| 8 (Major, M8 — no on-disk form named for `FeatureBundle`) | **Resolved.** `services.md` § ⚠ THE `05`→`06` HANDOFF now names the directory-of-three-files form (`matrix.parquet`, `tensor.npy`, `spec.json`) and ties it to the §13.3 per-file hash manifest. |
| 9 (Major, M9 — `FrameSpec` not a unique key) | **Resolved.** The `<partition_id>__<role>__<transform_id>/` naming rule (with `untransformed` for `None`) gives `raw`, `train`, `score` and the `DEC__score__T-REFIT/` G-06 frame four distinct addresses, checked directly against the table in `services.md` § ⚠ THE BUNDLE ADDRESS IS THE DIRECTORY NAME. |
| 11 (Major, M11 — blast radius omitted `fixtures-and-reproducibility` and named no derived count) | **Resolved.** `decisions.md` ADR-11 § Consequences now names six units including `fixtures-and-reproducibility`, and states the 152-occurrence / 4-file derived count. (This pass could not re-derive that count itself: it requires reading sibling units' `construction/` trees, which is outside this pass's read scope; it is accepted as reported.) |
| 13 (Minor, M13 — resource envelope not updated for the three-construction cost) | **Resolved.** `services.md` § "`05`'s cost changed with ADR-11" states the 18-construction / three-simultaneous-pairs cost against the 10.0 GB envelope. |
| C1-residual (withdrawal of the "unrepresentable" claim in three places) | **Resolved and complete.** A search of all five artifacts for "unrepresentable" finds exactly the three corrected sites (`decisions.md` ADR-11 § Consequences, `components.md` § `src/features` row `transforms.py`, `component-dependency.md` § Forbidden edges) plus the properly-historical ⚠-boxed preservations and the prior review's own quoted findings; no live claim of unrepresentability survives. `decisions.md` § Assumptions & Open Questions' closing bullet is likewise replaced with the two "readings adopted" / "owner decisions" bullets, so it no longer asserts "none of these ADRs adopts a reading on a supervisor-owned value." |
| M10, M14, BLK-04/BLK-06 register wording | **Tracking is accurate.** All three appear in `decisions.md` § Deferred obligations with a destination artifact, owner, due gate and acceptance test, matching the dispatch brief's description exactly. Not evaluated on the merits per instructions. |

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | **Critical** | `component-methods.md` § `src/models`, lines 731–739 (*"`inverse_transform` is required..."*) — `Transform.inverse(frame) -> DataFrame`; `Prediction` dataclass (no `Transform` field, only `transform_id: str`); `component-dependency.md` § Dependency matrix, row `src/evaluation` (cell `features` = `—`) | **The restored inverse cannot be invoked by the package the design says invokes it — the same "prose claims a mechanism the argument closure cannot support" defect as prior findings 1 and 2.** The text states plainly that `src/evaluation` "must be able to do that [inverse-transform to absolute TECU] without importing `src/features`," and that the inverse "travels with the `Prediction`'s `transform_id` and needs no new package edge." But `Transform.inverse` is a **method on the `Transform` class**, defined in `src/features` (§ The `src/features` leakage boundary), whose "fitted state is intra-package" — i.e. it holds the actual scaling parameters an inversion needs. `Prediction.transform_id` is a bare `str` (e.g. `"T-F1"`). A string cannot have `.inverse()` called on it, and nothing in `component-methods.md` or `component-dependency.md` specifies a lookup, registry, or deserialization path by which `src/evaluation` — which the dependency matrix confirms has **no import edge to `src/features`** — could turn that string into the `Transform` object the method requires. The M6 fix-scope confirmation (`application-design-questions.md` § 1) marks this "Approved — already implemented," but inspecting the signature shows the mechanism it approved does not execute. Separately, the fix never answers the conditional the prior review posed ("state whether the transform touches the target") — `FR-P1-04-6`/`NFR-LEAK-01` scope `transforms.py` to "scaling or standardization," which is a feature-space concept, while `ABL-DIFF`'s inverse (`team-practices.md` § Mandated, "`ABL-DIFF` inverse-transforms to absolute TECU before any metric") reads as a **target-representation** inversion (differenced vs. absolute TECU), a distinct concern the design now conflates with the feature scaler by naming both `Transform.inverse`. | Name the concrete path: either (a) give `Prediction` (or `FeatureBundle`) the actual mechanism `src/evaluation` needs — a loader keyed by `transform_id` that resolves to a `Transform` instance without a static import of the class (e.g. a registry module `src/data` can own, since `src/evaluation` already imports `src/data`), or (b) perform the inversion inside `src/models`/`src/features` before `Prediction` is constructed, so `Prediction.frame` is already in absolute TECU and `src/evaluation` needs no inverse call at all. Whichever is chosen, also settle whether `ABL-DIFF`'s target-representation inverse is the same operation as the feature-scaler's inverse or a separate one, and say so explicitly rather than reusing one method name for both. |
| 2 | **Critical** | `decisions.md` ADR-10 (lines 375–417, esp. the table at line 391 and "no authority backing" at line 397); `decisions.md` § Assumptions & Open Questions line 573; against `requirements-analysis/requirements.md` REQ-ENG-4 (line 266) and § Requirements with no testing row (lines 829–844) | **ADR-10 is stale against the upstream contract it names as authoritative, and understates what has already happened.** ADR-10's table states the amendment "goes 18 → 19" when `test_determinism.py` is added, and declares it **"not applied in this stage"** with the three new modules plus the `PYTHONHASHSEED` change having **"no authority backing"** until signed. But `requirements.md` REQ-ENG-4, verbatim: *"The **21** mandated test modules exist under `tests/`... The tree reached twenty-one by **four** amendments of three authorities: `test_acquisition_window.py` was countersigned 2026-08-16... and `test_determinism.py` was added under **ADR-10**... **both applied** under `CR-2026-08-22-TE-AMEND`, taking the tree from 17 to 19; `test_prepared_target_schema.py` was then added under **BLK-05**... taking it to 20; and `test_feature_leakage_guards.py` under `CR-2026-08-22-LEAKAGE-TA`, taking it to 21 — all three 2026-08-22 acts approved by the project owner under the recorded student/supervisor authority equivalence."* This is not a different ADR-10 by coincidence: the amendment content it names (`test_determinism.py`, added "under ADR-10") matches this ADR-10's own fourth item exactly. Two consequences follow, both checkable and both currently wrong in the design: (a) the framing that the amendment is unsigned and blocks `code-generation` from creating these modules is contradicted by requirements.md's own record of approval, one day before this pass; (b) `test_prepared_target_schema.py` and `test_feature_leakage_guards.py` — two modules bearing directly on this stage's own subject matter (target-schema validation and feature-leakage guards) — appear in **none** of the five application-design artifacts' package, test, or dependency inventories, even though requirements.md already treats them as existing, approved tree members. | Reconcile ADR-10 against the current `requirements.md`: either confirm the amendment was in fact signed (in which case ADR-10's "not applied," "no authority backing" language must be corrected, and REQ-ENG-4's current count of 21 — not 19 — is the number to track) or, if requirements.md is itself the stale artifact, say so explicitly and raise it as a cross-stage contradiction at the gate rather than silently building against the older number. Either way, add `test_prepared_target_schema.py` and `test_feature_leakage_guards.py` to `components.md`'s test/package inventory (or state which module owns them) so the five artifacts are not silently missing two mandated modules requirements.md already carries. |
| 3 | Major | `components.md` line 11 (*"94 requirement rows, 40 with no §16/§19 test row"*); against `requirements-analysis/requirements.md` § Requirements with no testing row, lines 829–844 | **The 40-count is stale; derived and counted directly, the current figure is 36.** `requirements.md` line 844 states outright: *"**Four removed 2026-08-22 — 40 → 36.**"* Counting the current enumeration at line 836–841 by hand (`REQ-ENG-7, REQ-ENG-9, REQ-ENG-10, FR-P1-01-11, FR-P1-01-5, FR-P1-01-7, FR-P1-01-8, FR-P1-01-9, FR-P1-02-6, FR-P1-03-5, FR-P1-04-4, FR-P1-04-10, FR-P1-04-14, FR-P1-04-15, FR-P1-04-18, FR-P1-05-3, FR-P1-05-4, FR-P1-05-5, FR-P1-05-6, FR-P1-05-7, FR-P1-05-14, FR-P1-05-15, FR-P1-05-16, FR-P1-05-17, FR-P1-05-18, FR-P1-05-19, FR-P1-05-20, FR-P1-05-21, FR-P1-05-22, FR-WS-2, FR-WS-3, REQ-CLAIM-01, REQ-NFR-A1, REQ-NFR-A2, FR-P1-02-7, FR-P1-02-8`) yields exactly **36**, matching the line's own stated total and confirming `40` is the pre-2026-08-22 figure. The 94-requirement-row count in the same line (`components.md` line 10) was independently re-derived by counting `FR-*`/`REQ-*` rows in `requirements.md` and is correct as 94. This is exactly the count-carried-from-an-earlier-revision defect class `project.md` § Way of Working's own learned rule warns against. | Update `components.md` line 11 to 36, and re-check whether any component-to-requirement mapping in the same file was built against the withdrawn four (`FR-P1-04-12/-13/-16/-17`, which left the untested list because they now have coverage) to confirm none is still marked untested by mistake. |
| 4 | Major | `component-methods.md` § `src/data/splits.py`, `Partition` dataclass (lines 288–297, fields `partition_id`, `kind`, `train_end`, `validation_month`, `embargo_hours` — no `train_start`); § The `src/features` leakage boundary, `fit_transforms`'s raise (line ~605, *"…is not exactly `partition`'s training range"*) and `build_features`'s raise (line ~611, *"the training range for `train`"*) | **"The partition's training range," the exact quantity two named raises compare against, is not a value any argument in scope carries.** `Partition` records only `train_end: date`; there is no `train_start` field, no method, and no referenced config value that fixes the lower bound. The comparison is executable only under an unstated convention — every partition's training window begins 2022-01-01 — which is true by the frozen calendar-year scope (`project.md` § Mandated, "calendar year 2022") but is never written down in `component-methods.md` as a governing invariant of `Partition`, `fit_transforms`, or `build_features`. This is a narrower version of the defect class findings 1 and 2 (this pass) and the prior pass's findings 1–2 were built on: a check specified in prose whose inputs, read literally, underdetermine the value being compared. | State the invariant explicitly wherever `Partition`'s training range is used as a check operand: either add it as a documented constant (e.g. `STUDY_START = date(2022, 1, 1)`, referenced by `fit_transforms`/`build_features`) or give `Partition` an explicit `train_start: date` field (defaulting to the frozen study start) so the range is a value on the object rather than an assumption in the reader's head. |

### Validation tool results

| Check | Result | Interpretation |
|---|---|---|
| Stage-declared validators | none beyond the `required-sections` / `upstream-coverage` / `claim-sources` sensors the orchestrator runs automatically | No CLI validator was invoked; every finding is a manual cross-reference with the location and, where a count is asserted, the derivation shown in the finding text. |
| Derived count — `requirements.md` § Requirements with no testing row, current enumeration | Hand-counted at **36** IDs, matching the line's own stated total ("36 fully untested requirements") and its own "40 → 36" note | Supports finding 3. `components.md`'s carried-forward "40" is stale. |
| Derived count — `FR-*`/`REQ-*` requirement rows in `requirements.md` | `94`, via `grep -oE '^\| (FR-[A-Z0-9-]+|REQ-[A-Z0-9-]+) \|' requirements.md \| sort -u \| wc -l` | Confirms `components.md` line 10's "94 requirement rows" is correct; only the untested-count half of that same sentence is stale. |
| Derived count — `Partition` fields versus what `fit_transforms`'s/`build_features`'s raises require | `Partition` has 5 fields (`partition_id`, `kind`, `train_end`, `validation_month`, `embargo_hours`); the raise needs a training-range **start**, which is not among them | Supports finding 4. |
| Cross-reference — "unrepresentable" occurrences across all five artifacts | 3 live corrected sites, 0 surviving unwithdrawn claims (remainder are historically-preserved ⚠ boxes and the two prior review passes' own quoted findings) | Confirms the C1-residual withdrawal is complete, per the dispatch brief's specific ask. |
| Cross-reference — `lead_in_hours` occurrences across all five artifacts | 0 live field definitions or call sites; remainder are the historical ⚠ boxes, the Q&A ruling record, and the disclosure sentence in `component-dependency.md` describing its removal | Confirms C3/C4's resolution is complete, not partial. |
| Cross-reference — REQ-ENG-4's count, `requirements.md` versus `decisions.md` ADR-10 | `requirements.md` line 266: **21** (already applied, 2026-08-22). `decisions.md` line 391: claims "18 → 19," "not applied" | Supports finding 2 — the two documents disagree about a fact (has the amendment been signed?) that determines whether `code-generation` may build the three new modules at all. |
| Cross-unit spot-check (permitted integration point) | `construction/features-and-splits/functional-design/business-logic-model.md` § Review, iterations 2–4 | Re-confirms the refit→December apply is the resolved required path, consistent with C2's fix; no new information against this pass's findings. |

### Summary

The five substantive edits the owner approved (C1, C2, C3/C4, BLK-03, M5, M9,
M13) are correctly and completely implemented, and the C1-residual withdrawal of
the "unrepresentable" claim is honest and thorough — no overstated copy survives
anywhere in the five artifacts. That resolves every Critical and Major finding
from the 2026-08-23 re-entry pass **except** M6 (the inverse transform), which
reproduces the identical defect class in a new location: `Transform.inverse` is
specified as reachable by `src/evaluation` through nothing more than a string
`transform_id`, with no import edge and no lookup mechanism named, so the
"already implemented" label in the fix-scope confirmation does not survive
inspection of the signatures it approved. Independently of the re-entry review's
scope, this pass found the design has drifted from its own upstream contract:
`requirements.md` already records ADR-10's four-part amendment as signed and the
mandated test-module count at 21 (not the 19 `decisions.md` still targets),
naming two mandated modules — one on target-schema validation, one on feature-
leakage guards — that appear nowhere in this stage's package or test inventory.
A third, smaller drift is a stale untested-requirement count (`components.md`
says 40; `requirements.md`'s own text says 36 as of 2026-08-22) of the exact
class this project's own `project.md` memory records as a recurring defect. One
further Major finding narrows a residual ambiguity in the newly-fixed leakage
check: `Partition` never states its training range's start date, so "the
partition's training range" is executable only under an unwritten convention.
Two Critical, two Major. The recommendation to the gate is that finding 1 (the
inverse transform) and finding 2 (the ADR-10/REQ-ENG-4 staleness) be resolved
before `units-generation` inherits this design, because both are the same
"prose claims what the arguments cannot deliver" and "count carried instead of
derived" defect classes this project's governance has already paid for twice.

**Verdict:** NOT-READY

## Review — 2026-08-23 count corrections

**Verdict:** READY

**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-23T14:51:38Z
**Iteration:** 3 (advisory, single pass)
**Scope reviewed:** Only the four edits made under the human owner's 2026-08-23
gate ruling ("approve, but fix the two counts first") — `components.md` §
Sources' untested-requirement count (40 → 36), and, in `decisions.md`, ADR-10's
table row on REQ-ENG-4's count, the new `## ⚠ CORRECTED 2026-08-23` box, and the
§ Assumptions & Open Questions ADR-10 bullet. The rest of the 2026-08-23
re-entry pass (recorded above) and the carried-forward accepted gate risks
(`Transform.inverse` not callable from `Prediction.transform_id`; `Partition`'s
missing `train_start`) are out of scope and not re-reviewed here.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Minor | `decisions.md` ADR-10, "Alternatives rejected" and "Reversibility" paragraphs (lines 440–446) | These two paragraphs were written on the assumption the four-part amendment was unsigned and were not swept when the `## ⚠ CORRECTED 2026-08-23` box was added three lines above them. "Four separate change records… Rejected as four countersignatures for one coherent design decision" still frames the amendment as awaiting countersignature, and "Reversibility. The record is easy to withdraw **before signature**" still frames it as pre-signature — both contradicted by the box's own claim, three lines up, that the amendment "IS ALREADY APPLIED" and was "approved by the project owner under the recorded student/supervisor authority equivalence" on 2026-08-22. A reader who reaches these two paragraphs without re-reading the box above could conclude the amendment is still pending. | Reword "Alternatives rejected" to drop "four countersignatures" (only `test_acquisition_window.py` was countersigned; the other three items were approved under the authority-equivalence mechanism the box names) and reword "Reversibility" to "before Construction builds against it" or similar, dropping "before signature" now that the box records the amendment as already approved. |

No Critical or Major findings survive against the four edits themselves.

### Validation Tool Results

| Check | Method | Result |
|---|---|---|
| Untested-requirement count (36) | Hand-enumerated the 36 comma-separated IDs at `requirements.md` lines 836–841 (`REQ-ENG-7, REQ-ENG-9, REQ-ENG-10, FR-P1-01-11, FR-P1-01-5, FR-P1-01-7, FR-P1-01-8, FR-P1-01-9, FR-P1-02-6, FR-P1-03-5, FR-P1-04-4, FR-P1-04-10, FR-P1-04-14, FR-P1-04-15, FR-P1-04-18, FR-P1-05-3, FR-P1-05-4, FR-P1-05-5, FR-P1-05-6, FR-P1-05-7, FR-P1-05-14, FR-P1-05-15, FR-P1-05-16, FR-P1-05-17, FR-P1-05-18, FR-P1-05-19, FR-P1-05-20, FR-P1-05-21, FR-P1-05-22, FR-WS-2, FR-WS-3, REQ-CLAIM-01, REQ-NFR-A1, REQ-NFR-A2, FR-P1-02-7, FR-P1-02-8`) by splitting on commas/"and" and de-duplicating in a shell script (`/tmp/ids2.txt`) rather than eyeballing the prose total | **36 unique IDs, 0 duplicates.** Matches `requirements.md`'s own stated total ("36 fully untested requirements", line 842) and `components.md` line 11's corrected figure. **36 is correct.** |
| Test-module count (21) and its 17 → 19 → 20 → 21 route | Read `requirements.md` REQ-ENG-4 (line 266) verbatim and compared its route sentence against `decisions.md` ADR-10's corrected box (lines 403–413) clause by clause | Both state, identically: `test_acquisition_window.py` (countersigned 2026-08-16) + `test_determinism.py` (ADR-10) → 17 to 19 under `CR-2026-08-22-TE-AMEND`; `test_prepared_target_schema.py` → 20 under `CR-2026-08-22-TARGET-SCHEMA-TEST`; `test_feature_leakage_guards.py` → 21 under `CR-2026-08-22-LEAKAGE-TA`. **The route is faithful; 21 is correct**, and matches the three modules requirements.md says exist (`test_acquisition_window.py`, `test_phase_boundary.py`, `test_release_hashes.py`) against 18 unwritten. |
| "Applied and approved" claim, checked for over-reading | Cross-checked the "student/supervisor authority equivalence" mechanism the box invokes against `units-generation/unit-of-work-story-map.md` line 306 and `unit-of-work.md` lines 122, 520, 545, 613, 670, which independently use the identical mechanism to close **BLK-01** on 2026-08-22 under the same change record (`CR-2026-08-22-TE-AMEND`) | The claim is **supported, not an over-read**. A downstream stage already treats this exact amendment as closed on authority grounds while explicitly distinguishing authority-to-name from authority-to-write ("none of the four modules exists, and `code-generation` must not create any of them before G-09") — the same distinction the box preserves ("18 of the 21 are unwritten"). |
| Limb 4 — `test_feature_leakage_guards.py` and `test_prepared_target_schema.py` across the five artifacts | `grep` for each literal filename across `components.md`, `component-dependency.md`, `component-methods.md`, `decisions.md`, `services.md` | `test_feature_leakage_guards.py`: **one hit**, `component-dependency.md` line 59, § Forbidden edges, cited as **TA-36**'s evidence — matches the box's "is carried" claim. `test_prepared_target_schema.py`: **zero hits** in `components.md`, `component-dependency.md`, `component-methods.md`, `services.md`; the only occurrences are inside `decisions.md`'s own review/correction prose. Matches the box's "appears nowhere… outside review text" claim. **Limb 4 is correct in full.** |
| Stray survival of `40` or `18 → 19` | `grep -n` for `\b40\b` and for `18 →`/`goes 18`/`mandated.*18` across all six files in `application-design/` (the five artifacts plus `application-design-questions.md`) | Every `40` outside `decisions.md`'s preserved-supersession/review text is in `components.md` lines 12/16, both correctly framed as the superseded figure. The `decisions.md` ADR-10 table row itself (line 391) no longer states "18 → 19" — it now reads "REQ-ENG-4's count rises — see the correction below". One stale `"REQ-ENG-4's mandated count goes 18 to 19"` line survives at `application-design-questions.md` line 618 — outside the five-artifact scope this pass and the dispatch brief both define, and outside "the four edits" this pass is bounded to; not raised as a finding against this revision, noted here only so it is not mistaken for a swept location. |

### Summary

Both corrected counts are right: 36 untested requirements (hand-enumerated and de-duplicated from `requirements.md`'s own list, matching its stated total) and 21 mandated test modules (the 17 → 19 → 20 → 21 route in ADR-10's box is a verbatim match to REQ-ENG-4's own wording). The "applied and approved" framing is supported by independent, contemporaneous use of the same authority mechanism in `units-generation`'s artifacts, not an over-read in the opposite direction. Limb 4 of the prior Critical 2 finding is correctly split: `test_feature_leakage_guards.py` is carried (as TA-36 evidence in `component-dependency.md`), `test_prepared_target_schema.py` is not carried anywhere in the five artifacts. The one Minor finding — ADR-10's "Alternatives rejected" and "Reversibility" paragraphs still read as if the amendment were unsigned, unswept when the correction box was added — does not affect the correctness of either count and is offered as gate input for a follow-on wording pass, not as a blocker. The human owner's ruling already carries the two accepted-as-risk items (the inverse-transform callability gap and `Partition`'s missing `train_start`) forward to `units-generation` unchanged; this pass adds nothing new against those two.

---

## Review — 2026-08-23 minor sweep

**Verdict:** READY

**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-23T18:57:48Z
**Iteration:** 4 (advisory, single pass)
**Scope reviewed:** Only the four edits made under the human owner's gate ruling
("approve, sweep the Minor first") on the one Minor finding from the
2026-08-23 count-corrections pass — `decisions.md` ADR-10 § Alternatives
rejected (preface note, "four countersignatures" → "four approvals," first
bullet annotated with where/when applied), ADR-10 § Reversibility (rewritten
to state the amendment as approved), `application-design-questions.md`'s
"18 to 19" table row (left in place, annotated with a superseding note
beneath the table), and `decisions.md` § Decision summary's ADR-10 row
(found by the orchestrator's own sweep, reworded to "approved 2026-08-22").
All three prior review sections above are preserved unchanged.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `application-design-questions.md` lines 638–642 (*"REQ-ENG-4's count is the item to watch... Every place it appears — REQ-ENG-4, § Requirements with no testing row, `team-practices.md` § Testing Posture, and the §12 enumeration — has to move together, or the next board finds a count mismatch exactly like `DATA-21`."*) | **This paragraph carries the same superseded "four places" claim the "18 to 19" table row above it carries, and it was not swept when that row was annotated.** `decisions.md` ADR-10's own `## ⚠ CORRECTED 2026-08-23` box, seven lines above the point edit 3 touched, states explicitly: *"The earlier 'four places' claim was also wrong, and its correction is independent of this one. The re-entry advisory pass derived that the count appears in **two** places, not four."* The `application-design-questions.md` paragraph at lines 638–642 restates the pre-correction four-place claim in full — naming `team-practices.md` § Testing Posture and "§ Requirements with no testing row" as loci the count must move through — with no annotation, strikethrough, or pointer to ADR-10's correction. It sits a few lines *below* the box that was inserted for the adjacent "18 to 19" figure (lines 621–628), so a reader who reads past that box, exactly the reader edit 3's annotation is meant to protect, reaches this paragraph next and finds an un-flagged instruction to synchronize four loci that ADR-10 has already found to be two. This is the status-claim-without-a-superseded-numeral failure mode `project.md` § Way of Working names directly ("a stale claim carrying no numeral... four of the six defects found on resume... were of those two kinds"), and it is the same "four places" defect this project's own re-entry review already caught once in `decisions.md`. | Add a superseding annotation to this paragraph (or fold it into the existing ⚠ box above it), pointing to `decisions.md` ADR-10 § ⚠ CORRECTED 2026-08-23's finding that the count appears in two real loci (REQ-ENG-4 and the TE §12/§13.2 amendment), not four. |
| 2 | Minor | `decisions.md` § Decision summary, row 10, "Reversibility" column (*"Governed change to reverse"*) | **The reworded cell breaks the table's own rating convention without contradicting it.** The other nine rows in this column all give a difficulty rating — `Easy`, `Moderate`, `Easy / permanent`, `Easy placement, **frozen values**`, `Easy now, locked at G-P2`, `Easy / coupled` — a reader can scan and compare at a glance. Row 10's new text is a mechanism description, not a rating, and it is not obviously equivalent to any of the other rows' vocabulary: ADR-10's own rewritten Reversibility paragraph (*"that change costs a change record and the owner's approval; after, it also means deleting modules"*) reads closer to `Moderate` than to `Easy`, but the summary cell states neither. This does not contradict ADR-10's prose — both agree the amendment is now a governed act, not a free retraction — but it weakens the table's at-a-glance comparability, the property the summary table exists for. | Either prefix the cell with a rating consistent with ADR-10's paragraph (e.g. `Moderate — governed change to reverse`) or leave it as a deliberate exception and say so once in the table's lead-in sentence, so the format break reads as intentional rather than inconsistent. |

### Validation Tool Results

| Check | Method | Result |
|---|---|---|
| Live survival of "unsigned"/"pending"/"before signature" framing across the two edited artifacts | `grep -n` for `unsigned|not applied|no authority backing|awaiting|pending sign|before signature|not yet signed` in `decisions.md` | Every hit is either inside the preserved `## ⚠ CORRECTED 2026-08-23` box (quoting the superseded text verbatim, correctly framed as historical) or inside the two edited paragraphs themselves, both of which use "unsigned"/"before signature" only in an explicit past-tense contrast ("weighed when the amendment was still unsigned," "rather than the retraction of an unsigned proposal") — no live claim that the amendment is currently unsigned survives. |
| Same sweep, `application-design-questions.md` | `grep -n` for the same pattern set, plus `18.*19` and `has to move together` | One hit for the annotated "18 to 19" table row (correctly boxed by edit 3) and one hit for the unannotated "has to move together" paragraph at lines 638–642 — the latter is finding 1. |
| Edit 1 verification (Alternatives rejected) | Read `decisions.md` lines 437–449 directly | Preface note present (*"weighed when the amendment was still unsigned... the approval recorded in the correction box above is what settled it"*); "four countersignatures" replaced with "four approvals"; first bullet annotated *"(Applied instead on 2026-08-22 under `CR-2026-08-22-TE-AMEND`, by the owner, in the stage that owns the change record.)"* — matches the scope description exactly. |
| Edit 2 verification (Reversibility) | Read `decisions.md` lines 450–455 directly | Rewritten to *"Corrected 2026-08-23: this paragraph read 'The record is easy to withdraw before signature'... The amendment is **approved**, so withdrawal is now a governed change of its own rather than the retraction of an unsigned proposal."* No residual "easy before signature" framing. |
| Edit 4 verification (Decision summary row) | Read `decisions.md` line 472 directly | Reads `| 10 | Four-part amendment — **approved 2026-08-22**, \`CR-2026-08-22-TE-AMEND\` | Governed change to reverse | **granted** |` — matches the description; assessed for internal consistency as finding 2 above. |
| "Four approvals" rewording checked as a rejected-alternative rationale | Compared the reworded bullet against ADR-10's own scope (the single `CR-2026-08-22-TE-AMEND` covering exactly these four items) | Coherent: the rejected alternative is four separate approvals for what the box records as one coherent decision approved under one change record: "one record covered all four items, which is how it was approved." No contradiction found. |
| Cross-check: does the Decision summary row's new rating match ADR-10's own Reversibility paragraph | Compared row 10's cell text against the rewritten paragraph (see edit 2) | No factual contradiction; format inconsistency only (finding 2). |
| Broader stale-claim sweep across the two edited artifacts | `grep -n` for `REQ-ENG-4|test_determinism|CORRECTED|superseded|superseding` in both files, plus manual read of every matched region | No further un-annotated survival of the superseded unsigned/pending framing or of the four-places claim found beyond finding 1. |

### Summary

Three of the four edits are complete and correctly framed: ADR-10's
Alternatives-rejected and Reversibility paragraphs no longer read as though
the amendment were unsigned, and the Decision summary row correctly states
the amendment as approved. The fourth edit (the `application-design-questions.md`
annotation) is sound in its stated reasoning — annotating an answered
question's record rather than rewriting it is the right call, and it
successfully covers the "18 to 19" table row itself — but the sweep it
performed was too narrow: a paragraph a few lines below the annotated table,
restating the now-superseded "four places must move together" claim in
prose, was left with no pointer to ADR-10's own finding that the real count
is two places, not four. That is a Major finding because it reproduces,
unswept, inside this same review cycle, the exact status-claim-without-a-numeral
failure mode this project's memory already names as a recurring defect
class. A second, Minor finding notes that the Decision summary's reworded
row breaks the table's Easy/Moderate rating convention without contradicting
it. Neither finding revisits the substance of the approval itself or the
two count corrections already verified in the prior pass. Recommendation to
the gate: sweep the one remaining paragraph before or shortly after approval;
it is a documentation-hazard fix, not a design change, and does not need to
block the gate on its own.

---

*Finalized 2026-08-23 under the stage's revision-4 completion pass. The Major above
was resolved before this pass — the "four places" paragraph in
`application-design-questions.md` is annotated as superseded, preserving the record
of what was put to the owner on 2026-08-21. The Minor is knowingly accepted: §
Decision summary's row 10 reads "Governed change to reverse" against the other nine
rows' Easy/Moderate scale, because a one-word rating for a governed change would
restate the inaccuracy the row was corrected for. Four items go to the approval gate
unresolved and are recorded above: `Transform.inverse`'s missing lookup (Critical),
`Partition.train_start`'s absence (Major), `test_prepared_target_schema.py`'s missing
owner (ADR-10 § ⚠ CORRECTED), and the three tracked deferrals in § Deferred
obligations.*

---

## Review — 2026-08-23 completion pass

**Verdict:** READY

**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-23T19:11:05Z
**Iteration:** 5 (terminal advisory pass, single pass, class `advisory`)
**Scope reviewed:** The five `produces[]` artifacts as finalized under the
revision-4 completion pass (`components.md`, `component-methods.md`,
`services.md`, `component-dependency.md`, `decisions.md`), with emphasis on the
five new *"Finalized 2026-08-23…"* footers, the surviving copies of the "None of
the above adopts a reading on a supervisor-owned value" sentence in
`components.md` and `services.md`, and every numeral in the five artifacts.
Cross-referenced against `../requirements-analysis/requirements.md` and
`../practices-discovery/team-practices.md` (consumes). Per the dispatch brief,
the four owner-accepted carried risks (`Transform.inverse`'s lookup,
`Partition.train_start`'s absence, `test_prepared_target_schema.py`'s missing
owner, ADR-10's Decision-summary row 10 wording, and the M10/M14/BLK-04/BLK-06
deferrals) are **not re-litigated** below; they are restated only where a
footer's description of them was checked for accuracy.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `component-dependency.md` § Forbidden edges, rows for *"a field outside the §6.2 dictionary entering features"* (FR-P1-04-12) and *"a carried-forward `vtec_lag_*` value"* (FR-P1-04-13) at lines 57–58, and *"a support field used as a model input without G-04 approval"* (FR-P1-04-16) at line 67; the summary line *"**Five of these have no §16/§19 row.**"* at line 72; and the Assumptions bullet *"Five forbidden edges have no §16/§19 row"* at line 164 | **These three rows, and the "Five" count built on them, are stale — contradicted by `components.md`'s own corrected Sources line and by `requirements.md` itself.** All three rows are marked `UNTESTED` — **no WS/TA row**", and the summary/assumptions text asserts they are "in `requirements.md`'s untested list." But `components.md` line 12–14 (corrected in this same completion pass) states in so many words that `FR-P1-04-12`, `FR-P1-04-13`, `FR-P1-04-16` and `FR-P1-04-17` **"left the untested list on gaining acceptance rows TA-33 through TA-36"** — and `requirements.md` confirms it directly: FR-P1-04-12 now carries **TA-33**, FR-P1-04-13 carries **TA-34**, FR-P1-04-16 carries **TA-35** (all `Status: Pending — the row exists, no test module is implemented`, but a §19 row unambiguously exists), and none of the three appears in `requirements.md`'s current 36-ID untested-requirements list (verified by the same hand-enumeration the prior "count corrections" pass used). The fourth ID in that same corrected group, FR-P1-04-17, **was** correctly updated in this file — rows 59–60 already cite `TA-36 (Pending)` — so the sweep that fixed one of the four sibling rows did not reach the other three, and then locked a now-wrong "Five" into both a prose summary and an open item. Re-derived today, the true count of forbidden edges with no §16/§19 row of any status is **one** (the identity-check row at line 61, which explicitly states "no WS/TA row covers the identity check itself"), not five. This is the identical count-carried-instead-of-derived and status-claim-without-a-numeral failure mode `project.md` § Way of Working already names as recurring in this stage, now found in a sibling artifact the prior "40 → 36" sweep did not check (that sweep's own recommendation — decisions.md finding 3, fix pass — scoped the re-check to "the same file," i.e. `components.md`, and so never reached `component-dependency.md`). | Update the three rows (FR-P1-04-12, FR-P1-04-13, FR-P1-04-16) to cite `TA-33`/`TA-34`/`TA-35` `(Pending)` in place of `UNTESTED — no WS/TA row`, matching the FR-P1-04-17 rows' already-correct treatment; recompute and restate the "Five of these have no §16/§19 row" line (true count: one, the identity-check row) at line 72; and update the Assumptions bullet at line 164 to match. |

No Critical findings survive against this pass's scope. No further Major or Minor findings survive beyond the one above; the sentence-level checks in items 2–3 below found the artifacts' remaining live claims true as stated.

### Validation Tool Results

| Check | Method | Result |
|---|---|---|
| Footer claims — `components.md`, `services.md`, `component-methods.md`, `component-dependency.md` | Read each footer against the body content and against the other footers and prior review sections it references | All four footers accurately restate what was fixed in this pass and what is carried unresolved (`Transform.inverse`, `Partition.train_start`, `test_prepared_target_schema.py`'s missing owner, the bundle-address rule, the three-construction resource-envelope statement, the NFR-LEAK-01 executable-raise correction). No footer overstates a fix or misdescribes a carried item. |
| Footer claim — `decisions.md` footer's "Major… resolved before this pass" | Read `application-design-questions.md` lines 644–651 directly | Confirmed present and accurate: the "four places" paragraph carries a `⚠` box stating the real count is **two**, dated 2026-08-23, matching the footer's claim and ADR-10's own § ⚠ CORRECTED box. |
| "None of the above adopts a reading on a supervisor-owned value" — `components.md` § Assumptions & Open Questions | Checked each of the four preceding bullets in that file against the sentence | True of this file's own contents: the `spaceweather.py`-placement assumption, the Q8 `src/gnss`-internals note, and the two "Open, carried from 2.3" items (the `02` ordinal collision, the `plumbing_7day` station count) each either declines to adopt a supervisor-owned reading or points to `services.md` as the place a reading was made. No bullet in this file's own list adopts one. |
| "None of the above adopts a reading on a supervisor-owned value" — `services.md` § Assumptions & Open Questions | Checked each of the five preceding bullets in that file against the sentence | True of this file's own contents: the `run_walking_skeleton.py`-scope assumption, the Q7 env-var-naming note, the `02` ordinal-collision and `plumbing_7day` open items (the latter explicitly named supervisor-owned and explicitly *not* resolved — "this design names the dependency rather than picking a station count"), and the `03_verify_processing.py` scope question. No bullet adopts a reading; `decisions.md`'s own corrected copy of this sentence (§ Assumptions, replaced by the two "readings adopted" bullets after ADR-11) is not contradicted by either surviving copy, since neither `components.md` nor `services.md` states the two readings ADR-11 records. |
| Count — `components.md` line 11, "94 requirement rows, 36 with no §16/§19 test row" | Re-derived independently: `grep -oE '^\| (FR-[A-Z0-9-]+\|REQ-[A-Z0-9-]+) \|' requirements.md \| sort -u \| wc -l` → 94; hand-enumeration of `requirements.md`'s current untested-ID list → 36 | Both confirmed correct and unchanged since the prior "count corrections" pass. |
| Count — `src/data/reuse_registry.py`, "all fifteen fields" (`components.md` line 71) | Counted the field list `team-practices.md` § Mandated gives for the §10.1 register: `reuse_id`, repository URL, immutable commit/tag, upstream file and line/function, retrieval date, licence/SPDX ID, copied-vs-adapted status, destination file, scientific purpose, modifications, tests, original citation, notice location, reviewer, approval date | 15 items — matches "all fifteen fields" exactly. |
| Count — forbidden-edge rows lacking a §16/§19 acceptance row, `component-dependency.md` | Enumerated every row in § Forbidden edges and classified each by its Test column: literal `UNTESTED` (3: FR-P1-04-12, FR-P1-04-13, FR-P1-04-16) plus the identity-check row's "no WS/TA row covers the identity check itself" (1) = 4 by the file's own (stale) classification; cross-checked each of the 3 `UNTESTED` rows against `requirements.md`'s current TA-33/34/35 rows, which exist (Pending) | Supports finding 1. The file's internal count before correction is 4, not the asserted 5, and after accounting for TA-33/34/35 the honest count is 1. |
| Cross-reference — `test_feature_leakage_guards.py` / `test_prepared_target_schema.py` across the five artifacts | Re-ran the same grep the prior "count corrections" pass used | Unchanged: `test_feature_leakage_guards.py` one hit (`component-dependency.md` line 59, TA-36 evidence); `test_prepared_target_schema.py` zero hits outside `decisions.md`'s own review prose. Both facts still hold as this pass's footers and ADR-10's box describe them. |
| Stray survival of the superseded "40" or "18 → 19" figures | `grep -n '\b40\b'` and `18 →|goes 18|mandated.*18` across all five artifacts | Every live "40" is inside `components.md`'s own correctly-framed supersession note (lines 12–16); no bare "18 → 19" survives inside the five artifacts (the one known stray copy in `application-design-questions.md` is outside this stage's produces list and was already noted as out-of-scope by the prior pass). |

### Summary

The five artifacts, as finalized under this completion pass, are gate-ready.
Every footer's claim checked out against the body text it summarizes and
against the sibling artifacts it cross-references; the two surviving copies of
"None of the above adopts a reading on a supervisor-owned value" (in
`components.md` and `services.md`) are each true of their own file's contents,
independently verified rather than assumed to inherit `decisions.md`'s
correction. The `94`/`36` untested-requirement counts and the reuse-registry's
`15`-field count both re-derive correctly. One new Major finding survives this
pass: `component-dependency.md`'s Forbidden-edges table still marks three rows
(FR-P1-04-12, FR-P1-04-13, FR-P1-04-16) as having no WS/TA acceptance row, and
states a "Five" summary count built on that, when `requirements.md` — and this
same completion pass's own correction to `components.md`'s Sources line — record
that these exact three IDs gained acceptance rows (TA-33/34/35, status
`Pending`) on 2026-08-22. This is the same class of defect the "40 → 36" sweep
fixed in `components.md`, in a sibling file that sweep's own recommendation did
not reach; it is a tracking-accuracy gap, not a structural one, since the
underlying `features.build_features` raises these findings describe are
unaffected by which acceptance row backs them. With the four owner-accepted
carried risks (`Transform.inverse`'s missing lookup, `Partition.train_start`'s
absence, `test_prepared_target_schema.py`'s missing owner, and the
M10/M14/BLK-04/BLK-06 deferrals) already recorded and going to the gate as
carried risk rather than as new findings, and with only one new Major finding
that does not touch the design's structural soundness, `units-generation`
(2.7), `delivery-planning` (2.8) and `functional-design` (3.1) for
`features-and-splits` inherit a design whose module boundaries, dependency
matrix, leakage-boundary mechanism (identity check plus the one enumerated
`REFIT`→`DEC` exception), bundle addressing and provenance handoff, and
resource envelope are internally consistent and implementable — with the one
new finding above, and the four already-carried items, both worth a line at
the approval gate before Construction inherits them.

## Review — 2026-08-23 acceptance-row corrections

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-23T19:25:31Z
**Iteration:** 1 (narrow correction pass, following the completion-pass review above)
**Scope reviewed:** `component-dependency.md` only — the sole file this correction
touched — checked against `../requirements-analysis/requirements.md` (upstream,
read-only) and, for stale-copy sweeping, the other four `application-design`
artifacts. The prior four review passes on this stage are preserved unchanged
above and are not re-litigated here.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `component-dependency.md` lines 76–83, § Forbidden edges | The printed derivation is not reproducible against the current artifact. It claims "counting the table rows carrying the literal `UNTESTED` gives **3**" — but the literal string `UNTESTED` does not appear anywhere in the § Forbidden edges table (lines 50–70); the corrected rows now read `TA-33 (Pending)`, `TA-34 (Pending)`, `TA-35 (Pending)`. It also claims "counting rows carrying the phrase *'no WS/TA row'* gives **4**" — but that exact phrase appears exactly **once** in the table (line 61, the identity-check row); a literal grep of the current file finds it nowhere else in the table. Both counts describe a prior revision's wording, recalled and asserted rather than counted from what is on the page today — precisely the failure mode `project.md` § Corrections (learned 2026-08-21, `application-design:application-design:count-derivation`) exists to prevent: "never carry a count from adjacent prose... or from an earlier revision." The final total the paragraph reaches (**1**) is independently correct (see Validation Tool Results below), so no downstream claim is wrong, but a reader who tries to verify "3" or "4" by searching the current table as instructed will fail to reproduce either number. | Rewrite the derivation to count against the table as it stands today, e.g.: "Before 2026-08-22's `CR-2026-08-22-LEAKAGE-TA`, the FR-P1-04-12/-13/-16 rows and the identity-check row's embedded clause all read a status equivalent to 'no acceptance row' (4 rows). The change record gave the first three TA-33/34/35 (`Pending`); only the identity-check row still has none, leaving **1**." Or, if the "3"/"4" figures are meant historically, label them explicitly as "as this table read before 2026-08-22" so a reader is not directed to recount literal strings against the present text and fail. |

### Validation Tool Results

| Check | Method | Result |
|---|---|---|
| TA-33/34/35 ↔ FR-ID mapping correctness | Grepped `requirements.md` for `TA-33\|TA-34\|TA-35\|TA-36\|FR-P1-04-1[2367]`; read lines 590–598 and 844–863 | `requirements.md` states the four rows were "added 2026-08-22 under Vision §15.2 (`CR-2026-08-22-LEAKAGE-TA`) as negative-path controls for FR-P1-04-12, FR-P1-04-13, FR-P1-04-16 and FR-P1-04-17" in that order, mapping 1:1 to TA-33, TA-34, TA-35, TA-36. `component-dependency.md`'s three edited rows cite FR-P1-04-12→TA-33, FR-P1-04-13→TA-34, FR-P1-04-16→TA-35 — all three correct. |
| `(Pending)` status accuracy | Read `requirements.md` line 597–598 | "All four carry status `Pending` — approved as criteria, not implemented, not executed, not passing." `component-dependency.md`'s `(Pending)` tags for TA-33/34/35 match this exactly; they do not imply an implemented or passing test. |
| Re-derivation of the "no §16/§19 row" count, method: enumerate every row of § Forbidden edges (lines 50–70, 19 rows including the non-edge `models→evaluation` row) and classify by whether the row (or the file elsewhere) states outright that no acceptance row exists | Manual enumeration against the table text | Exactly **one** row states this outright — the transform-identity check (line 61: "no WS/TA row covers the identity check itself"). Rows citing only a test-module name without an inline TA/WS number (phase-boundary, IRI-denial, `REFIT`/`DEC`, train-only-transform rows 63–66, locked-test-guard) are *not* additional instances of "no row" — `team.md`'s "Test-bearing WS rows"/"Test-bearing TA rows" lists and `requirements.md` document off-table acceptance rows for each of those test modules (e.g. WS-10/TA-07 for IRI denial, TA-11 for train-only transforms, WS-18/TA-18 for the locked-test guard); the table simply doesn't repeat the number on every rule row. Counting those as "missing" would give a much larger, wrong number under a reading the paragraph itself does not use and should not switch to. **Independently-derived count: 1**, matching the paragraph's stated conclusion despite the derivation-method issue in Finding 1. |
| Literal-string reproducibility check for the derivation's own claimed counts | `grep -n "UNTESTED"` and `grep -n "no WS/TA row"` against `component-dependency.md` | `UNTESTED`: 1 hit total, and it is inside the derivation sentence itself (line 77), not in the table. `no WS/TA row`: 2 hits total — line 61 (the table) and line 78 (the derivation sentence describing the count) — not 4. Confirms Finding 1: the printed method does not reproduce 3 or 4 from the current file. |
| Stale "Five" / untested-status sweep across the other four `application-design` artifacts | Grepped `components.md`, `component-methods.md`, `services.md` for `Five`, `FR-P1-04-12`, `FR-P1-04-13`, `FR-P1-04-16`, `no §16/§19 row`, `no WS/TA row`, `UNTESTED` | No stale copy found. `components.md` line 13 already carries the correct, previously-fixed 40→36 note naming the same four FR IDs and TA-33…36 — consistent with, not contradicted by, this pass's edits. `component-methods.md` line 656 cites FR-P1-04-13 only in an unrelated context (excluded-row count), no status claim. No occurrence of "Five" refers to this topic anywhere outside the two preserved prior-review sections in `decisions.md` (lines ~1012–1013, correctly left untouched as history). |
| § Sources line accuracy (`component-dependency.md` lines 7–9) | Read the line and cross-checked against the table's FR-ID citations | Unchanged by this correction and not contradicted by it: FR-P1-04-16 and FR-P1-04-17 are still accurately named as requirements this file carries. Pre-existing and out of this correction's scope: the same line does not separately name FR-P1-04-12 or FR-P1-04-13, though the table cites both (lines 57, 58, 63) — this omission predates the current pass (it was already the case when the file held TA-33/34's rows under their prior, uncorrected status) and was not part of the owner's fix-the-Major ruling, so it is noted here rather than treated as a new finding against this correction. |
| Internal contradiction check: corrected table vs. rewritten paragraph vs. § Assumptions bullet vs. finalization footer | Read all four locations together | No contradiction. The paragraph (lines 76–83, aside from Finding 1's derivation-method issue) and the § Assumptions bullet (line 186) agree on "1" and on the TA-33/34/35 attribution; the finalization footer (lines 191–198) does not touch this topic and does not conflict with it. |

### Summary

The Major finding from the 2026-08-23 completion pass is fixed on its substance: the three rows now cite the correct TA-33/34/35 against the correct FR IDs, correctly marked `(Pending)` rather than implemented or passing, and the file's own summary count is corrected from "Five" to "One," which this review independently re-derives and confirms as the right number by a method that does not rely on recalling the file's prior wording. One new Major finding survives: the paragraph's *shown* derivation ("literal `UNTESTED` gives 3," "phrase 'no WS/TA row' gives 4") cannot be reproduced by searching the current table, because that literal text no longer appears there — the derivation narrates a prior revision's state rather than counting the artifact as it now reads, which is the exact anti-pattern `project.md`'s count-derivation learning was written to prevent, even though it did not produce a wrong final answer this time. The human should decide at the gate whether to require the derivation sentence be rewritten to count against the present table (or explicitly labeled as historical) before or alongside approval, since the number it supports is correct but the method as written would mislead the next person who tries to check it the way the file itself invites.

## Review — 2026-08-23 derivation rewrite

**Verdict:** READY

**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-23T19:36:28Z
**Iteration:** 1 (narrow correction pass, following the "acceptance-row corrections" pass above; owner ruling: "fix the derivation, then approve")
**Scope reviewed:** `component-dependency.md` § Forbidden edges only — the one paragraph replaced by the correction (the present-tense reproducible check, the pre-correction historical counts, and the rewrite note). No other file changed since the completion pass; the prior six review sections above are preserved unchanged and not re-litigated. Read-only reference to `../requirements-analysis/requirements.md` for the TA-33/34/35 mapping already verified in the prior pass (not re-derived here, since this pass's scope is the derivation paragraph, not that mapping).

### Findings

_None. No finding survives against this correction's scope._

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| — | — | — | — | — |

### Validation Tool Results

| Check | Method (exact command / procedure) | Output / Result |
|---|---|---|
| Does part 1's present-tense check reproduce against the current table? — rows carrying the phrase `no WS/TA row` | `awk '/^## Forbidden edges/,/^## Why the guard/' component-dependency.md \| grep -n "no WS/TA row"` (table-scoped, excluding the derivation prose that follows the table) | 1 hit: line 14 of the extracted range — the transform-identity row ("**no WS/TA row covers the identity check itself**"). Matches the paragraph's stated **1**. |
| Does part 1's check reproduce? — rows carrying the literal `UNTESTED` | Same table-scoped extraction, `grep -n "UNTESTED"` | 0 hits inside the table. Matches the paragraph's claim that "no row carries the literal `UNTESTED` any more." |
| Whole-file scoping sanity check (does a naive whole-file grep diverge from the paragraph's table-scoped claim, and if so is that itself a defect?) | `grep -c "no WS/TA row" component-dependency.md` and `grep -c "UNTESTED" component-dependency.md` over the whole file | `no WS/TA row`: 3 whole-file hits (the table row, plus the two prose sentences of the derivation paragraph itself, which quote the phrase to describe the check). `UNTESTED`: 2 whole-file hits (both inside the derivation paragraph's own historical sentence, quoting the retired literal). Not a defect: the paragraph explicitly scopes its check to "rows of the table above," and a reader following that instruction (as this review did, and as the prior "acceptance-row corrections" pass's own table-scoped re-derivation did) gets the same 1/0 the paragraph states. |
| Is part 2 correctly labelled as historical, and consistent with the file's own preserved supersession record? | Read part 2's lead-in sentence; cross-checked its claimed pre-correction counts (`UNTESTED` × 3: FR-P1-04-12, FR-P1-04-13, FR-P1-04-16; `no WS/TA row` × 4, the fourth being the identity-check clause) against the "completion pass" review section above (its Finding 1 and its "Count — forbidden-edge rows lacking a §16/§19 acceptance row" validation row) and against `git diff` of this file against the baseline commit `b7bcd99`/`a39fd03` | Consistent on both counts. The lead-in reads "*counted against the **pre-correction** text and labelled as history so the numbers below are not mistaken for a check on the current table*" — an explicit, unambiguous historical label. The completion-pass review independently found, before TA-33/34/35 existed, "literal `UNTESTED` (3: FR-P1-04-12, FR-P1-04-13, FR-P1-04-16) plus the identity-check row's clause (1) = 4" — the same 3/4 split this paragraph states. `git diff`'s removed lines confirm the same three FR-IDs plus a fourth pre-TA-36 row once shared the literal cell text `UNTESTED` — `no WS/TA row`, corroborating the 3/4 relationship (every `UNTESTED` cell also carried the `no WS/TA row` phrase, plus the identity-check row carrying only the phrase). |
| Is "1" still the right answer, independently re-counted (not carried from the paragraph's own claim)? | Manual enumeration of every row in the § Forbidden edges table (19 rows) by its Test column, same method the completion-pass and acceptance-row-corrections passes used | Exactly one row states outright that no acceptance row exists — the transform-identity row. Every other row either cites a WS/TA number, a named test module without a "no row" claim (which prior passes already established is not an additional instance, per `team.md`'s off-table WS/TA lists), or is the non-edge `models→evaluation` row. Independently confirms **1**. |
| New contradiction check: paragraph vs. corrected table vs. § Assumptions bullet vs. finalization footer | Read all four locations together: table (lines ~50–70), the rewritten paragraph (lines ~72–90), the § Assumptions bullet ("**Open.** **One** forbidden edge has no §16/§19 row..."), and the finalization footer | No contradiction. All agree on **1** and on the transform-identity row being the sole gap; the footer does not touch this topic. The new "Rewritten 2026-08-23..." note's account of why the paragraph changed matches this review's own prior "acceptance-row corrections" section (Major finding 1, and the owner's "fix the derivation, then approve" ruling stated in this dispatch) — no misdescription of that history. |

### Summary

The correction fixes the exact defect the prior pass raised: part 1 now states a check that reproduces against the current table (1 row carries "no WS/TA row," 0 carry literal `UNTESTED`, independently re-confirmed here by table-scoped grep and by manual enumeration), part 2 states the same 3-`UNTESTED`/4-`no WS/TA row` figures but now explicitly labelled as counted against the pre-correction text rather than the present one, and those historical figures agree with what the completion-pass review and the raw `git diff` both independently show the pre-correction table actually contained. No new contradiction was introduced against the corrected table, the § Assumptions "One" bullet, or the finalization footer. No finding survives; this narrow correction is gate-ready.
