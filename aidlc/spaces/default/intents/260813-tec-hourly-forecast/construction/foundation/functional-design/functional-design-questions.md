# Functional Design Questions — `foundation`

**Unit** `foundation` — Foundation: scaffold, configuration, determinism, releases.
**Kind** `library` · **Complexity** M · **Deployment** shared · **Depends on** — (dependency root).

This is the first pass of **Functional Design** — the step that fixes the
behaviour of a unit's logic, its rules and its data shapes before any code is
written. It covers one **Bolt**'s worth of design work (a Bolt being one build
pass over one piece of the work, ending in something that runs). `foundation` is
Bolt 1.

**Nothing here decides a scientific value.** Every question below is about
*mechanism* — how a rule is enforced, where a value is looked up, what shape a
record takes. Scientific constants live in the four governed configs and are
frozen by D-number; a question that would set one is out of scope for this stage
by `project.md` § Forbidden, and none is asked.

**G-09 is not signed.** This stage produces design, not code. Nothing answered
here authorises writing `src/data/config.py`, `src/data/release.py` or
`tests/test_determinism.py` — creation stays gated by G-09, TE §18.3's
stop-and-report rule, and stage 3.5.

## Sources

- `../../../inception/units-generation/unit-of-work.md` — § 1 `foundation`: responsibility, the 16 requirements carried, the 7 acceptance rows, the boundary, and the implementation notes (BLK-01 closed 2026-08-22, authority-only).
- `../../../inception/units-generation/unit-of-work-story-map.md` — this unit's requirement-to-acceptance mapping; **2 of its 16 requirements carry no §16/§19 test row** (REQ-ENG-7, REQ-ENG-10).
- `../../../inception/requirements-analysis/requirements.md` — REQ-ENG-1, -2, -3, -4, -6, -7, -8, -10, -11; FR-P1-01-10; FR-P1-04-11; FR-P1-05-13; FR-WS-7; NFR-AUD-01; NFR-SEC-01; NFR-DET-01.
- `../../../inception/application-design/component-methods.md` — the signatures and raise-contracts for `src/data/config.py` and `src/data/release.py`, and the `ConfigSnapshot` / `DeterminismRecord` shapes.
- `../../../inception/application-design/components.md` and `component-dependency.md` — the layering rule, the import boundaries, and § Shared resources' unqualified carve-out on `evidence/locked_test_restricted/`.
- `../../../inception/application-design/services.md` — § Stage entry contract (the six ordered steps), § Run record and registry (Q5 = C, JSONL authoritative / CSV derived).
- `../../../inception/delivery-planning/bolt-plan.md` — Bolt 1's Definition of Done, and § Gate 0's permitted/barred boundary before G-09.
- `../../../inception/practices-discovery/team-practices.md` — § Code Style (ruff, `NN_verb_noun.py`, docstring rule, two-tier error posture), § Testing Posture (§18.3 as the real gate).
- Absent by scope design, named so the gap is visible rather than silent: `stories` — stage 2.4 is `SKIP`; `mockups` — stages 1.6 and 2.5 are `SKIP`. `foundation` is `kind: library` with no user-facing surface, so `frontend-components.md` is not produced and no mockup input is missing in substance.

---

## Question 1

`assert_no_tbd(snapshot, *, required: Sequence[str])` takes the list of fields it must check as an argument. Nothing in the design says where that list comes from — and a field missing from it passes preflight silently, which is the exact failure §18.3 exists to prevent.

Where should the `required` field list live?

A) Each stage script passes its own literal list
   > **Impact**: Simplest to write and each script states its own needs. But nine independently-maintained lists drift, and a field omitted from one script's list is invisible — the preflight passes and reports nothing. This is the failure mode `DP-DATA-01` already caught once in this project, where an obligation written as a hand-maintained list silently exempted whatever was not anticipated.

B) One declarative map in `config.py`, keyed by stage, checked for completeness against the config schema
   > **Impact**: Single place to read and review, and the completeness check makes an omission a test failure rather than a silent pass. Costs a schema-versus-map consistency test that must itself be maintained. Keeps the rule and its trigger together, matching the correction this project already made when it replaced a Bolt-number list with the rule's own condition.

C) Derive it entirely from the config files — every field whose value is the `TBD — freeze gate` sentinel is required
   > **Impact**: No list to maintain and no drift by construction. But it inverts the check into a tautology: it can only ever find fields already marked `TBD`, so a required field that is simply **absent** from the config passes. REQ-ENG-2 wants both conditions caught.

D) Derive from a schema file that marks each field required-or-optional per phase
   > **Impact**: Strongest coverage — catches absent fields, `TBD` fields and phase-inappropriate fields. Adds a fifth governed file in spirit, which cuts against TE §12's "exactly four" and would need an amendment or an explicit statement that the schema carries no scientific constant.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B — with the explicit rule that the map's completeness against the parsed config structure is asserted by a test, so an omission fails loudly. It puts the rule in one reviewable place without adding a fifth file, and it directly applies the lesson this project recorded at `DP-DATA-01`: a list is not a rule, so the list needs a mechanism that proves it is complete. C is tempting for its zero maintenance but cannot see an absent field, which is half of what REQ-ENG-2 asks for.

[Answer]:

---

## Question 2

Bolt 1 creates the four governed configs carrying visible `TBD — freeze gate` sentinels — REQ-ENG-2 requires exactly that, and Gate 0's boundary list permits it before G-09. Bolt 1 also builds `assert_no_tbd`, whose whole job is to fail on `TBD`.

So what does `foundation`'s own test suite assert about a config that is *supposed* to contain `TBD` at this point?

A) `assert_no_tbd` is tested only against synthetic fixtures; the real `configs/` are never passed to it in Bolt 1
   > **Impact**: Clean separation and no false failure. The mechanism is proven on fixtures that contain both a `TBD` field and a clean field. Risk: the test never exercises the real config structure, so a parser mismatch between fixture shape and real shape stays hidden until a later Bolt.

B) Tested against synthetic fixtures **and** against the real `configs/`, with the real-config test asserting that it *raises* and that the raised message names every `TBD` field
   > **Impact**: Proves the mechanism and the real structure together, and turns the sentinels into positive evidence: the test asserts the freeze gates that are still open are exactly the ones expected. Costs a test that must be updated as each freeze gate closes — which is arguably a feature, since it makes closing a gate a visible event.

C) `assert_no_tbd` is not tested in Bolt 1 at all; it is tested when the first real caller exists
   > **Impact**: Least work now. But `assert_no_tbd` is one of §18.3's named critical checks and TA-23 gates on it, so deferring its test leaves a critical-set item untested through several Bolts — and TC-06 orders the test suite ahead of acquisition precisely to avoid that.
D) Tested against the real `configs/` only
   > **Impact**: Exercises the true structure with no fixture maintenance. But it cannot test the *passing* path at all until every freeze gate is closed, so the "no `TBD` present, returns cleanly" branch stays unexercised for most of the project.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B. It is the only option that exercises both branches and the real structure, and it converts a slightly awkward situation — a project whose configs are meant to contain `TBD` — into the clearest available evidence about which freeze gates remain open. It also matches this project's affirmed methodology of pairing every hard rule with a negative control rather than testing the happy path alone.

[Answer]:

---

## Question 3

`NFR-DET-01` requires recording nondeterministic operations where determinism cannot be guaranteed, and `DeterminismRecord.nondeterministic_ops` is the field that carries them. How is that field populated?

A) A hardcoded list in `config.py`, maintained by hand
   > **Impact**: Immediate and readable. But it goes stale silently against a TensorFlow version bump, and the record would then claim determinism the environment does not provide — an assertion presented as a measurement, which is what `project.md` § Way of Working warns against.

B) Declared in `configs/experiment.yaml`, read into the record
   > **Impact**: Reviewable and versioned with the run, and it changes with a D-number rather than a code edit. But it is a **claim about the environment kept in a config file**, so it can disagree with the installed TensorFlow and nothing would catch the disagreement.

C) Probed from the framework at run time, with the probe result recorded and the config-declared list used only as an expected-set cross-check
   > **Impact**: The record becomes a measurement rather than a claim, and a mismatch between expected and probed is surfaced as an integrity finding. Costs a probe that must be written against TensorFlow's determinism surface, which is version-sensitive and may not enumerate everything.
D) Left empty in Phase 1 and populated when model training starts
   > **Impact**: Honest about Phase 1's scope — the heaviest nondeterminism risk is in training, which is a later Bolt. But `NFR-DET-01` is not phase-scoped, and an empty field reads as "none known" rather than "not yet measured" unless it is explicitly marked.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. This project has an explicit, repeatedly-affirmed preference for executable evidence over asserted evidence — reproducibility is tested, determinism is tested, the locked-test guard is a test rather than a signature. A probed value with a config cross-check is the same discipline applied here. If the probe surface turns out to be too thin to be worth it, D with an explicit `not-yet-measured` marker is the honest fallback, and it should be marked rather than left empty.

[Answer]:

---

## Question 4

The experiment registry is append-only, and status transitions append a new row referencing the run ID rather than mutating the original (`services.md` § Run record and registry). What are the legal statuses, and is the transition set enforced?

A) `started` / `completed` / `aborted`, unenforced — the writer accepts any status string
   > **Impact**: Minimal and flexible. But NFR-AUD-01's guarantee is that a failed run stays visible **with its status and reason**; an unenforced vocabulary lets a typo produce a row that no reader groups correctly, and the corruption is permanent in an append-only file.

B) A closed enum `started` / `completed` / `aborted` / `failed`, enforced at write time, with `aborted` and `failed` requiring a non-empty reason
   > **Impact**: The vocabulary cannot drift and the reason cannot be omitted where it matters most. Distinguishes a run that stopped itself (`aborted`, e.g. a preflight raise) from one that died (`failed`), which are different diagnostic stories. Costs one enum to agree on now.

C) Closed enum plus an enforced transition graph — a run ID cannot go `completed` → `started`, and cannot be `completed` twice
   > **Impact**: Strongest integrity, and it makes the silent-rerun prohibition machine-checkable rather than merely visible. But enforcing a transition graph requires reading prior rows for that run ID before appending, which means the append is no longer a pure append and needs a defined behaviour when the file is large or partially written.

D) Closed enum, with the transition graph asserted by a **separate registry-integrity test** rather than at write time
   > **Impact**: Keeps the write path a pure append — the property that makes append-only trustworthy — while still making illegal sequences a detectable failure. A violation is caught at the next test run rather than at write time, so a bad sequence can exist briefly.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. It gets C's integrity guarantee without compromising the one property that makes an append-only log worth having: that writing never depends on reading. TA-10 gates on registry integrity and is satisfied by a test, so the check has a home. The distinction between `aborted` and `failed` from B should be kept in either case — the stage entry contract already writes `aborted` explicitly on a steps 1–5 raise.

[Answer]:

---

## Question 5

The design names six error types across this unit and its neighbours — `ConfigError`, `PreflightError`, `PlatformError`, `DeterminismError`, `ReleaseError`, `RegistryError` — and the affirmed two-tier posture says an integrity violation exits non-zero naming the file and the violated expectation. How are these organised?

A) Six independent exception classes, each raised and handled where it occurs
   > **Impact**: Explicit and easy to trace. But the stage entry contract needs to catch *any* of them uniformly to write the `aborted` registry row with its reason, and a bare list of six means a seventh added later is silently not caught — the same list-versus-rule failure as Question 1.

B) One `IntegrityError` base with the six as subclasses; the stage entry contract catches the base
   > **Impact**: A new error type is caught automatically by virtue of its base, so the registry row is never missed. The base carries the two fields the posture requires — the file and the violated expectation — so the message format is uniform by construction rather than by convention.

C) Base class as in B, plus a second base `CompletenessShortfall` for the non-fatal tier
   > **Impact**: Makes the two-tier posture structural rather than remembered: a shortfall cannot accidentally be raised as fatal, because it is not in that hierarchy. Costs a second hierarchy for a tier that is recorded in a manifest rather than raised, so it may be a type where a return value would do.
D) No project exception types — raise built-ins with formatted messages
   > **Impact**: Least machinery. But nothing can catch a category, the message format becomes convention rather than contract, and the two tiers become indistinguishable to a caller.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B, with the file and the violated-expectation fields required on the base so the posture is enforced by the constructor rather than by discipline. C's second hierarchy is worth considering only if a completeness shortfall ever needs to propagate; as designed it is recorded as a manifest field and returned, not raised, so a type for it would be unused machinery today.

[Answer]:

---

## Question 6

`write_release` raises when `out_dir` already holds a release — a release is write-protected or stored under a new version, never overwritten (TE §13.3, TA-15). Where does the new version identifier come from?

A) A caller-supplied version string
   > **Impact**: Fully explicit. But nothing prevents a caller reusing a version, and the release's identity then depends on caller discipline rather than on the release API — which is what the mutation-protection test is meant to remove.

B) Monotonic integer assigned by `release.py` by scanning the parent directory
   > **Impact**: Cannot collide and needs no caller input. But the version becomes a function of directory state, so the same content released into a different tree gets a different version, and a deleted directory silently reuses a number.

C) Content-addressed — the version is derived from the manifest hash, so identical content is the same release and different content is necessarily a new one
   > **Impact**: Version identity and content identity become the same fact, which makes "was this released before?" answerable by hashing rather than by bookkeeping. Re-releasing identical content is a no-op rather than an error, which is arguably the correct behaviour for an idempotent pipeline. Costs human readability: a hash is not a version number a person can order.
D) Content hash for identity plus a monotonic human-readable label recorded alongside it
   > **Impact**: Both properties — collision-free identity and a label a reviewer can cite at a gate. Costs carrying two identifiers and defining which one is authoritative when they disagree.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D, with the **content hash authoritative** and the label explicitly derived and non-authoritative. This project's gates are human-reviewed and its records are cited by name, so a reviewer needs something citable; but every integrity guarantee here is hash-based, and making the label authoritative would put the weaker identifier in charge. Stating which one wins is the part that must not be left implicit.

[Answer]:

---

## Question 7

Two of this unit's sixteen requirements carry **no §16 or §19 acceptance row**: **REQ-ENG-7** (freeze-gate tags, and any commit changing a scientific constant or governed config citing its D-number) and **REQ-ENG-10** (the per-run environment lock capturing TE §13.1's eight items). Both are real obligations with a pass/fail criterion and no row behind them.

How should this unit's design treat them?

A) Design to the requirement and note the absent row; propose nothing
   > **Impact**: Honest and within this stage's authority — creating an acceptance row is a Vision §15.2 amendment this stage cannot grant. But it leaves both obligations enforced only by attention, and REQ-ENG-10 feeds the environment lock that G-07 accepts.

B) Design to the requirement, and specify a negative-path test for each **as a specification**, explicitly marked as not an acceptance row
   > **Impact**: Gives 3.5 and 3.6 something concrete to build and keeps the §15.2 boundary intact. Matches exactly how this project handled the four leakage prohibitions before their rows existed — a written specification, explicitly labelled as neither a row nor a result. Risk: a reader mistakes a specification for coverage, which is why the labelling has to be blunt.

C) Design to the requirement and raise a change request now, seeking §19 rows for both
   > **Impact**: Closes the gap properly and permanently. But it is a §15.2 amendment with owner lead time in front of it, and it would be the second such request opened from a design stage; TA-33–TA-36 set the precedent that this is possible, so the path is proven.
D) Treat REQ-ENG-10 as covered by TA-03 and design only REQ-ENG-7 as uncovered
   > **Impact**: Reduces the gap to one item if TA-03 genuinely covers the eight-item environment lock. **This needs verification, not assertion** — the story map lists TA-03 among this unit's rows, and whether it covers all eight §13.1 items or only the platform evidence is a claim to check against the row text before relying on it.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B, with the labelling made unmissable. It is the precedent this project already set and then confirmed at the owner's ruling on `DP-ML-01`, and it keeps the §15.2 line where the authority documents put it. If you would rather close the gap for good, C is the stronger answer and the TA-33–TA-36 route shows it works — say so and I will draft the request rather than the specification. D should not be chosen without first checking TA-03's actual text; I have not verified that claim and will not assert it.

[Answer]:

---

## Question 8

`resolve_platform_roots` must return no credential and log none (§10, NFR-SEC-01), and TA-22 accepts a secret scan over the tree, history, configs, logs and artifacts. But `foundation` is also the unit that resolves the environment a credential arrives through, and Bolt 3 is the consumer that reaches a provider client.

What does `foundation`'s design specify about the *absence* of a credential?

A) Nothing — a missing credential is Bolt 3's problem, surfaced when the provider client fails
   > **Impact**: Keeps the boundary clean: `foundation` never touches credentials at all, which is the strongest reading of §10. But the failure then arrives deep in an acquisition run, after a platform resolution that reported success, and the message names a provider error rather than a missing environment variable.

B) `resolve_platform_roots` checks that the **names** it expects are present in the environment, without reading or returning the values
   > **Impact**: Fails early with a message naming the missing variable, and still never touches a value — presence of a name is not a secret. Costs `foundation` knowing which names exist, which is a small coupling to the providers.

C) A separate `assert_credentials_available(names)` in `config.py`, called by the stage scripts that need it
   > **Impact**: Keeps `resolve_platform_roots` single-purpose and makes the credential precondition explicit at each call site that has one. Same early failure as B with a clearer boundary. Costs one more function and a per-script list — which is the Question 1 problem again in miniature.
D) B, plus an explicit design statement that no code path returns, logs, or interpolates a credential value, backed by the secret-scan test
   > **Impact**: Pairs the mechanism with the negative control that proves it, which is this project's affirmed methodology. The scan is required for TA-22 anyway, so this adds a design statement rather than new machinery.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. Early failure on a missing name costs little and turns a deep provider error into a clear precondition failure, while the explicit never-return-never-log statement plus the scan is what makes NFR-SEC-01 checkable rather than intended. Note that `evidence.md` records NFR-SEC-01 as **not yet satisfied in this workspace today**, so this is a rule being built rather than one being ratified — the `.gitignore` deny-list precondition from `team.md` § Way of Working has to exist before the first commit regardless of which option you pick.

[Answer]:

---

## Assumptions & Open Questions

- **[assumption]** `frontend-components.md` is not produced for this unit. `foundation` is `kind: library` with no user-facing surface, and the stage's `produces_kinds` maps `frontend-components` to `[ui]` only. The engine's resolved `produces` list for this unit confirms three artifacts, not four.
- **[assumption]** `src/data/registry.py` is **not** part of this unit. It appears in `component-methods.md` between two `foundation` modules, but `unit-of-work.md` § 1 does not list it under `Owns`, and the station registry belongs to `inventory-and-registry`. Design questions about `Station` and `load_registry` are therefore out of scope here.
- **[assumption]** `src/data/locked_test.py` is not this unit's either, notwithstanding that `foundation` owns the boundary rule that names it. § Shared resources fixes the carve-out that only that module may construct a path into `evidence/locked_test_restricted/`; the module itself belongs to `governance-guards` (BLK-07).
- **Open** — whether TA-03 covers all eight items of TE §13.1's environment lock or only the platform evidence. Question 7 option D depends on it and the claim is **unverified**; it will be checked against the row text before any artifact relies on it, per `project.md` § Way of Working on verifying a fact before handing it on as established.
- **Open** — the `required` field list from Question 1 cannot be fully enumerated until the four configs exist with their field names. Whatever mechanism is chosen, this stage specifies the *mechanism*; the concrete list is a Bolt 1 work product.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.
