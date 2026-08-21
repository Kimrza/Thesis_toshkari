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
across. The leakage and phase-boundary contracts are expressible as *shapes* —
`fit_transforms(train, fold)` and `apply_transforms(frame, transform)` are two
functions precisely so that `fit_transform(all_data)` is unrepresentable. Against
that: intra-package structure stays unspecified, so 3.1 has real work per unit and
two type names (`Transform`, `BootstrapResult`) are referenced but undefined.

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
| `tests/test_determinism.py` | TE §12 tree | **REQ-ENG-4's count goes 18 → 19** |
| `PYTHONHASHSEED` in the clean-run commands | TE §13.2 | `test_clean_run.py`, WS-20, TA-17 test the sequence as written |

**Consequences.** One change record and one countersignature cover all four, which
is why FU-2 and FU-3 were folded into ADR-06's amendment rather than raised
separately. Until it is signed, three modules and one test module in this design
have **no authority backing**, and `code-generation` must not create them on the
strength of this ADR alone.

**REQ-ENG-4's count is the item to watch.** Stage 2.3 corrected that number twice
under governance findings — most recently `DATA-21`, a count carried from a
finding's text without being checked against the source table. It appears in
REQ-ENG-4, § Requirements with no testing row, `team-practices.md` § Testing
Posture, and the §12 enumeration. All four must move together or the next board
finds the same class of mismatch again.

**Alternatives rejected.**
- *Apply the amendment here.* Rejected: not in this stage's produces list, and
  supervisor-owned.
- *Four separate change records.* Rejected as four countersignatures for one
  coherent design decision.
- *Avoid the amendment by widening existing modules.* Rejected in ADR-06 and FU-2
  on the merits, not on cost.

**Reversibility.** The record is easy to withdraw before signature. After
Construction builds against it, withdrawal means deleting modules.

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
| 10 | Four-part amendment as an obligation | Easy before signature | **yes** |

## Assumptions & Open Questions

- **Open, supervisor-owned.** The four-part §12/§13.2 amendment (ADR-10). Three modules and one test module have no authority backing until it is signed.
- **Open, supervisor-owned.** D-122's sign-off, still pending per Vision §14.2.
- **Open, supervisor-owned.** § Known defects row 12 — the `plumbing_7day` station count — blocks that fixture's manifest, which `run_walking_skeleton.py` reads.
- **Open, carried from 2.3.** The advisory `NOT-READY` finding on FR-P1-05-18: no criterion tests the storm-event count's source. ADR-05's design makes the source an explicit required argument so a test *can* assert it; writing the criterion is a `requirements.md` change.
- **Open, a §12 defect.** The `02` ordinal collision between the Phase 1 and Phase 2 target scripts. `services.md` records the reading adopted; renaming either script would be a further amendment.
- **None** of these ADRs adopts a reading on a supervisor-owned value, and none decides a scientific constant.

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
