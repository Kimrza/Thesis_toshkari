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

[Answer]: B — Define one centralized, declarative stage-to-required-fields map in config.py. Validate the map against the configuration schema or parsed configuration structure, and add tests that fail when a governed required field is omitted. Preflight must reject both missing required fields and fields containing the "TBD — freeze gate" sentinel. Do not introduce a fifth governed configuration file.

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

[Answer]: B — Test assert_no_tbd against both synthetic fixtures and the real governed configuration files. Synthetic fixtures must cover both failure on TBD or missing required fields and successful execution when all required fields are present and finalized. For the real configurations, assert that the function raises and that its error identifies exactly the required fields still containing the "TBD — freeze gate" sentinel. Keep the expected unresolved fields explicit and update them as the corresponding freeze gates close. The presence of authorized TBD values in Bolt 1 must be treated as expected test evidence, not as a foundation-stage failure.

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

[Answer]: C — Populate nondeterministic_ops from runtime observations and compare the observed results with any expected operations declared in the configuration. Record the framework version, determinism settings, probe scope, and any detected mismatches. If the framework cannot provide a complete assessment, explicitly mark the result as "partial"; if the relevant operations have not yet been executed, mark them as "not-yet-measured" rather than treating an empty list as proof of determinism.

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

[Answer]: D — Enforce a closed status vocabulary at write time: started, completed, aborted, and failed. Require a non-empty reason for aborted and failed records. Keep registry writes append-only without requiring a prior read of the run history.

Validate status transitions through a separate registry-integrity test. For each run ID, permit started → completed, started → aborted, or started → failed; reject duplicate started records, repeated terminal statuses, transitions from terminal statuses, and unknown or malformed records.

Run the integrity test before TA-10/G-09 acceptance and before relying on registry contents as audit evidence. Treat aborted as an intentional or preflight-triggered stop and failed as an execution failure.

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

[Answer]: B — Define IntegrityError as the common base class for ConfigError, PreflightError, PlatformError, DeterminismError, ReleaseError, RegistryError, and any future integrity-related exceptions.

Require every IntegrityError to carry the affected file or resource and the violated expectation, and produce a consistent diagnostic message from those fields.

The stage entry contract must catch IntegrityError, attempt to append an aborted registry record containing the failure reason, and exit non-zero. If registry writing itself fails, preserve the original exception, report both the original failure and the registry-write failure to stderr, and exit non-zero without claiming that an aborted record was successfully written.

Represent non-fatal completeness shortfalls as explicit manifest or return-value data rather than introducing a separate exception hierarchy unless propagation requirements later justify one.

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

[Answer]: D — Use a content-derived SHA-256 hash as the authoritative release identity and assign a separate monotonic, human-readable release label for review and citation.

Derive the authoritative hash from a canonical manifest or content representation that excludes the human-readable label, volatile metadata, and any self-referential hash field. Persist the mapping between the label and content hash in an auditable release record.

Allocate human-readable labels from a durable, append-only release history rather than solely by scanning existing directories, and never reuse a previously assigned label. Detect label/hash mismatches as integrity violations.

Preserve TE §13.3 and TA-15: write_release must reject an output directory that already contains a release and must never overwrite existing release content. Do not silently treat repeated writes as successful unless that behavior is explicitly authorized through the project's change-control process.

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

[Answer]: X — Combine options B and C.

Design both REQ-ENG-7 and REQ-ENG-10 as enforceable obligations and specify explicit negative-path tests, clearly labeled: "Test specification only — not an approved acceptance row and not evidence of a passing result."

For REQ-ENG-7, specify tests that reject changes to governed scientific constants or governed configuration files when the required decision identifier is missing or invalid, and verify the applicable freeze-gate tagging requirements.

For REQ-ENG-10, derive the required environment-lock fields directly from TE §13.1 and specify tests that fail when any required item is missing, malformed, or not captured for the applicable run.

Before creating a new acceptance row for REQ-ENG-10, inspect the actual TA-03 text and map it against all eight TE §13.1 items. Treat TA-03 as sufficient only if complete coverage is demonstrated explicitly; otherwise, identify the uncovered obligations.

Raise a Vision §15.2 change request for a formal acceptance row covering REQ-ENG-7 and for any REQ-ENG-10 obligations not already covered by verified acceptance criteria. Present the proposed amendment for my approval as project owner.

Allow design and implementation planning to proceed while the amendment is pending where permitted, but do not claim formal acceptance coverage or gate satisfaction until the applicable change is approved and the required tests are executed successfully.

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

[Answer]: D — Define credential availability as an explicit, stage-specific precondition while preserving the foundation unit's strict no-secret-value boundary.

Maintain required credential environment-variable names in one centrally reviewed stage/provider mapping rather than duplicating per-script lists. For stages that actually require authenticated provider access, check only whether the required environment-variable names are present and fail early with a message identifying missing names.

Do not require credentials for unrelated stages, public providers, or foundation initialization itself. Do not read, return, log, serialize, interpolate, or persist credential values in resolve_platform_roots or other foundation-layer diagnostics.

Document that checking the presence of an environment-variable name does not prove its value is non-empty, valid, or authorized. The actual provider client must perform any necessary value validation without exposing the secret.

Back these rules with negative-path tests using synthetic canary secrets and with the TA-22 secret-scan requirements for the repository tree, history, configurations, logs, and artifacts. Ensure the required .gitignore deny-list exists before the first relevant commit, and do not claim NFR-SEC-01 or TA-22 compliance until the required checks have actually passed.

---

---

# Follow-up questions

Raised 2026-08-22 from the Step 4 ambiguity analysis over the eight answers
above. **No answer above is vague and none contradicts another** — all three
follow-ups are *missing details* that artifact generation needs and that no
answer supplies. Each names the answer it descends from.

## TA-03 verification — the result, before FU-1

Q7 directed: *"inspect the actual TA-03 text and map it against all eight TE
§13.1 items."* Done, and it changes the instruction's own premise twice.

**First: TE §13.1 carries seven bullets, not eight.** Derived, printed before
assertion:

```
awk 'NR>=749 && NR<=760 && /^- /' <TE> | wc -l   ->  7
```

1. `requirements.txt` hash and a per-run `pip freeze`
2. Python, operating system, CPU (and GPU if used), and key library versions
3. code commit
4. configuration snapshot hashes for all four config files
5. input dataset and manifest versions
6. platform (`local` or `kaggle`)
7. known nondeterministic operations

"Eight" is **defensible at field granularity and not at bullet granularity**:
bullet 1 names two distinct captures, so a registry row carrying them as
`requirements_hash` and `pip_freeze` has eight fields over seven bullets.
REQ-ENG-10's own criterion says *"A registry row exists carrying all eight
fields"*, so the field reading is the operative one for the test. Nothing in the
governed tree reconciles the two granularities, which is why the figure reads
inconsistently between `services.md` § Stage entry contract step 6, `unit-of-work.md`
§ 1, and REQ-ENG-10. **The design below uses eight named fields and states the
seven-bullet provenance**, so neither count has to be trusted on its own.

**Second: TA-03 does not cover REQ-ENG-10.** TA-03 verbatim: *"Python 3.11 and
exact pins install successfully on both Kaggle and local"*, evidence *"Lock file,
install log, environment hash"*.

| §13.1 field | Covered by TA-03? | Where it actually sits |
|---|---|---|
| `requirements.txt` hash + per-run `pip freeze` | **No** | TA-03's lock file and environment hash are install-time artifacts with no per-run dimension |
| Python / OS / CPU / GPU / library versions | **Partial** | "Python 3.11" only; OS, CPU, GPU and library versions unnamed |
| code commit | **No** | TA-01's evidence column ("Repository tree and code commit") |
| configuration snapshot hashes ×4 | **No** | TA-02 covers config existence and `TBD` marking, not per-run snapshot hashes |
| input dataset and manifest versions | **No** | TA-15 covers release manifests, not the per-run lock |
| platform | **Partial** | "on both Kaggle and local" is install-test coverage, not per-run platform capture |
| known nondeterministic operations | **No** | nothing in this unit's seven rows |

**Zero of seven fully covered; two partial, and both partials are install-time
rather than per-run — which is the whole substance of the requirement.**
Independently confirmed by the artifact itself: REQ-ENG-10's test-row column
already reads *"`UNTESTED` — no WS/TA row covers the §13.1 capture list; candidate
new TA row via Vision…"*, so `requirements.md` had recorded this answer before the
question was asked.

**Consequence for Q7:** the §15.2 change request covers **REQ-ENG-7 in full and
REQ-ENG-10 in full**. There is no partial-coverage carve-out to subtract, and the
Q7 option-D framing that floated TA-03 as a candidate was wrong.

## FU-1 — Is the required-fields map keyed by stage, or by stage × phase?

Descends from **Q1=B** (one centralized declarative stage-to-required-fields map)
and touches **Q2=B**.

`load_configs(config_dir, *, phase: int)` takes a phase; seven of the nine stage
scripts are phase-aware; and TE §7.0's Phase 1 hard prohibition means some fields
are *legitimately* `TBD` under `--phase 1` — a Phase 2 DCB or RINEX field is not a
Phase 1 omission. A stage-only key therefore has to resolve one way or the other,
and both ways are lossy.

A) Key by stage only, with the map listing the union of both phases' fields
   > **Impact**: Simplest structure. But a Phase 1 run then fails preflight on Phase 2 fields that are correctly unset, so either Phase 1 cannot pass its own gate or the sentinels get filled early — and filling a `TBD — freeze gate` field early is exactly what `project.md` § Forbidden prohibits.

B) Key by stage only, with the map listing the intersection (fields required in both phases)
   > **Impact**: Phase 1 passes cleanly. But the check silently stops covering every Phase-2-only field, so REQ-ENG-2's guarantee quietly weakens at the phase boundary — the failure is invisible, which is the property this project treats as worst.

C) Key by `(stage, phase)`, so each stage-phase pair declares its own required set
   > **Impact**: Each run is checked against exactly what it should have. Costs a two-dimensional map and a completeness assertion that covers both phases, and it makes the phase boundary visible in the map — arguably a benefit, since NFR-PHASE-01 wants that boundary explicit everywhere.

D) Key by stage, with each field annotated `required-in: [1] | [2] | [1,2]`
   > **Impact**: Same coverage as C with a flatter shape that reads as one list per stage. The phase logic moves into the field annotation rather than the key, which is easier to scan and slightly easier to get wrong.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. Q1's whole purpose was to make an omission a test failure rather than a silent pass, and B reintroduces exactly the silent pass at the phase boundary while A forces a prohibited early fill. C keeps the guarantee intact in both phases and makes the boundary legible in the structure the preflight reads. D is equivalent in coverage and I would accept it without argument; C is preferred only because a `(stage, phase)` key cannot be *forgotten* the way a per-field annotation can be omitted.

[Answer]: C — Key the required configuration-fields map by (stage, phase). Validate completeness against the applicable configuration schema and phase-specific obligations. Fields that legitimately remain TBD in Phase 1 must not block Phase 1, while Phase-2-required fields must be enforced in Phase 2.

## FU-2 — Where does the append-only release-label history live, and who owns it?

Descends from **Q6=D**: *"Allocate human-readable labels from a durable,
append-only release history rather than solely by scanning existing directories,
and never reuse a previously assigned label."*

That requires a persistent record that does not exist in any artifact today.
`foundation`'s `Owns` list names `experiment_registry.jsonl` and `artifacts/` and
no release ledger, so this is a new owned thing and the design has to say which.

A) A new `foundation`-owned append-only file, e.g. `artifacts/release_history.jsonl`
   > **Impact**: Single purpose, easy to reason about, and the never-reuse rule is enforced by scanning one small file. Adds a third append-only artifact to the unit alongside the registry and the releases themselves.

B) Folded into `experiment_registry.jsonl` as release-event rows
   > **Impact**: No new artifact, and release allocation inherits the append-only guarantees and integrity test already designed for the registry under Q4. But it mixes two vocabularies in one log — run status transitions and release labels — and Q4's transition graph would need to ignore rows that are not run events.

C) A manifest index under `artifacts/`, derived and rebuildable from the release manifests themselves
   > **Impact**: Nothing authoritative to corrupt, since it can be regenerated. But a *derived* index cannot guarantee never-reuse: if a release directory is deleted, the rebuilt index forgets the label and the next allocation reuses it — the exact failure Q6 rejected when it ruled out scanning directories.

D) A new `foundation`-owned file as in A, with the label allocation covered by the same registry-integrity test pattern Q4 established
   > **Impact**: A's clarity plus an explicit home for the never-reuse assertion, reusing a test shape already agreed rather than inventing one. Costs the third artifact and one more test module's worth of scope in Bolt 1.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. C is ruled out by Q6's own reasoning — a derived index reintroduces label reuse after a directory is removed. B is genuinely tempting for reusing the registry's guarantees, but a log whose readers must filter by row kind before applying an integrity rule is where a rule quietly stops applying to the rows it was written for. A separate file with the same test pattern keeps both logs single-vocabulary.

[Answer]: D — Define a separate, foundation-owned, durable, append-only release-history ledger for human-readable release labels and their authoritative content hashes. Keep it separate from experiment_registry.jsonl. Specify its approved location, ownership, schema, append-only behavior, label-allocation rules, and an independent integrity test that rejects duplicate or reused labels and inconsistent label/hash mappings. If introducing this ledger changes an approved ownership list, artifact inventory, or governed design, raise the required change request rather than modifying approved artifacts silently.

> **Amendment scope, determined 2026-08-22 rather than assumed.** Three checks were
> run against the authority and the approved artifacts before deciding what this
> ledger requires:
>
> **No TE §12 tree amendment is needed.** `artifacts/registry/` is already an
> enumerated directory in the §12 tree, and the tree carries **zero file-level
> entries inside any `artifacts/` subdirectory** — derived:
> `sed -n '709,721p' <TE> | grep -cE '\.(jsonl|json|csv)'` → `0`. Confirming the
> pattern from the other direction, `experiment_registry.jsonl` is **not named
> anywhere in the Technical Environment**; it originates in stage 2.6's
> `services.md` § Run record and registry. A new file under an already-enumerated
> `artifacts/` subdirectory therefore sits inside the tree as approved.
>
> **Two approved AI-DLC stage artifacts do need annotation.** `unit-of-work.md`
> § 1 `foundation` → `Owns` enumerates owned artifacts and names "the run record
> and `experiment_registry.jsonl` append-only writer" with no release ledger; and
> `services.md` § Run record and registry states "Two artifacts, one
> authoritative" in a table that would become three rows. Both are approved-stage
> artifacts, so neither is edited here.
>
> **This is not a Vision §15.2 amendment.** §15.2 governs the authority documents
> (Vision, Technical Environment). Annotating an approved AI-DLC stage artifact is
> the annotate-in-place question the owner already settled at
> `GOV-2026-08-22-INC-01` Rec 7. The request raised for this item is therefore the
> cheaper class, and is presented at this stage's approval gate rather than through
> §15.2 change control.

## FU-3 — One central mapping or two?

Descends from **Q1=B** (a centralized stage-to-required-fields map in `config.py`)
and **Q8=D** (*"one centrally reviewed stage/provider mapping"* of required
credential environment-variable names).

Both answers centralize a per-stage list, and both lists are keyed by stage.
Nothing says whether they are one structure or two — and Q8 adds a wrinkle worth
settling explicitly: it says credentials are **not** required for *"foundation
initialization itself"*, while Q1 puts the map inside `config.py`, which
`foundation` owns. So `foundation` would host a credential map it never consumes.
That is coherent, but if it is not stated it reads like a boundary violation.

A) Two separate structures, both in `config.py`
   > **Impact**: Each has one job and neither's schema constrains the other. `foundation` hosts both and consumes only the config-fields one — which needs saying out loud, once, or a reviewer will read the credential map as `foundation` reaching for secrets.

B) One structure per stage with two fields — `required_config_fields` and `required_credential_names`
   > **Impact**: One place to look and one completeness test covering both. But it couples two unrelated review cadences: a credential-name change and a config-schema change would touch the same entry, and the credential half has a different reviewer concern (§10, NFR-SEC-01) than the config half.

C) Two structures, with the credential map outside `config.py` — e.g. `src/data/credentials.py`
   > **Impact**: Puts the strongest possible distance between the credential surface and the module that resolves platform roots, which is where Q8's no-secret-value boundary matters most. Costs a seventh module in a unit whose `Owns` list is already long, and `src/` has exactly six mandated packages with no room for a stray file.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A, with the hosting statement made explicit in
`business-rules.md`: `foundation` **declares** the credential-name map and
**never reads a credential value**, and no `foundation` code path consumes the map
except to hand the names to a stage that asked. C's instinct is right but there is
no legal home for a seventh module — TE §12 fixes six `src/` packages — and B's
single entry merges a security review with a schema review, which is the kind of
coupling that gets one of them skipped.

[Answer]: A — Maintain two separate centralized declarative mappings in config.py: one for required configuration fields keyed by (stage, phase), and one for required credential environment-variable names keyed by the applicable stage/provider and, where necessary, phase. State explicitly that foundation owns or hosts the credential-name mapping but does not read, return, log, or consume credential values during initialization. Only stages requiring authenticated access should apply the credential-presence precondition.

---

---

# Pending governed amendments — presented, NOT applied

Three items below need a change the owner has not yet approved. **None is applied
in this stage's artifacts.** Each is presented for an explicit decision, and each
names its authority class, because the three are not the same kind of change and
conflating them would overstate two of them.

| Class | What governs it | Items here |
|---|---|---|
| **Vision §15.2 amendment** | The authority documents (Vision, Technical Environment). Owner or supervisor decision, with lead time | **A** — new §19 TA rows for REQ-ENG-7 and REQ-ENG-10 |
| **Approved AI-DLC artifact annotation** | The `GOV-2026-08-22-INC-01` Rec 7 precedent, where the owner settled that a completed stage's artifact may be annotated in place on explicit approval | **B** — `DeterminismRecord` fields in `component-methods.md`; **C** — the release ledger in `services.md` and `unit-of-work.md` |
| **No amendment needed** | — | The TE §12 tree, for the release ledger. `artifacts/registry/` is already enumerated and the tree carries zero file-level entries inside `artifacts/` |

## Amendment A — §19 acceptance rows for REQ-ENG-7 and REQ-ENG-10 (Vision §15.2)

Directed by **Q7=X**. The TA-03 verification above establishes there is **no
partial coverage to subtract**: both requirements need a row in full.

- **REQ-ENG-7** — freeze-gate tagging, and a D-number cited on any commit that
  changes a scientific constant or a governed config. Proposed criterion: the tag
  list covers every signed gate, and a commit-message audit shows a D-number on
  every governed change; a governed change with a missing or malformed D-number
  **fails**.
- **REQ-ENG-10** — the per-run environment lock. Proposed criterion: a registry
  row carries **all eight fields populated** — not `unavailable` — and a run that
  captures none of them **fails** rather than completing silently. The eight
  fields, and their seven-bullet provenance, are enumerated in § TA-03
  verification above so the row does not have to restate a count.

**Nothing is claimed as covered until such a row exists, is approved, and its test
has actually executed and passed.** Per Q7's own instruction, design and planning
proceed meanwhile; acceptance coverage does not.

## Amendment B — `DeterminismRecord` fields (approved 2.6 artifact)

**The current contract, derived from `component-methods.md` rather than recalled** —
six fields:

```
awk '/class DeterminismRecord/,/^$/' component-methods.md | grep -cE "^ +[a-z_]+: "   ->  6
```

`seeds_applied` · `pythonhashseed` · `reexec_performed` · `framework_versions` ·
`tf_op_determinism` · `nondeterministic_ops`

**Q3=C requires recording five things. Two are already covered:**

| Q3 requirement | Existing field | Status |
|---|---|---|
| framework version | `framework_versions` | **covered** |
| determinism settings | `tf_op_determinism`, `pythonhashseed` | **covered** |
| probe scope | — | **missing** |
| detected mismatches | — | **missing** |
| `partial` / `not-yet-measured` status | — | **missing** |

**Three fields proposed, taking the contract from six to nine:**

| Proposed field | Type | Why it cannot be omitted |
|---|---|---|
| `probe_scope` | `Sequence[str]` | Without it, `nondeterministic_ops: []` is ambiguous between *"probed and found none"* and *"probed nothing"*. Q3 chose C precisely so the record is a measurement; an unrecorded scope makes the measurement unreadable |
| `measurement_status` | `str` — one of `complete` \| `partial` \| `not-yet-measured` | The field Q3 explicitly asks for. It is what stops an empty `nondeterministic_ops` reading as proof of determinism, which the answer names as the failure to avoid |
| `declared_vs_observed_mismatches` | `Sequence[str]` | The result of Q3's config cross-check. Empty means the declared and observed sets agree; a non-empty value is an integrity finding under Q5's `IntegrityError` base. Without the field the cross-check happens and is not recorded |

**Deliberately not proposed:** a field carrying the config-declared expected set
itself. It is recoverable from the configuration snapshot hash already in
`ConfigSnapshot`, and adding it would duplicate governed data into a second place
— the drift pattern this project has spent the session correcting.

**Not applied.** The dataclass stays at six fields in the approved artifact. The
three artifacts this stage produces specify the *semantics* of all nine and mark
the three proposed fields as **not present in the approved component design**, so
a reader cannot mistake the specification for the contract. **No determinism is
claimed as measured anywhere on the strength of a field that does not exist.**

## Amendment C — the release-history ledger (approved 2.6 and 2.7 artifacts)

Directed by **FU-2=D**, which instructs raising the request rather than editing
silently. Scope determined above, not assumed:

- `unit-of-work.md` § 1 `foundation` → `Owns` gains the ledger. It currently names
  "the run record and `experiment_registry.jsonl` append-only writer" and no
  release ledger.
- `services.md` § Run record and registry becomes three rows. It currently opens
  "Two artifacts, one authoritative".
- **Proposed location** `artifacts/registry/release_history.jsonl` — inside the
  already-enumerated `artifacts/registry/`, so **no TE §12 amendment**.
- **Proposed schema**, one line per label allocation: the human-readable label; the
  authoritative content hash; the release path; the allocating run ID; a UTC
  timestamp. Append-only, never rewritten.
- **Proposed integrity test**, following the pattern Q4 established: rejects a
  duplicate or reused label, rejects a label bound to two different content hashes,
  rejects a content hash bound to two labels, and rejects a malformed row.

**Not applied.** Both approved artifacts are unedited.

## Assumptions & Open Questions

- **[assumption]** `frontend-components.md` is not produced for this unit. `foundation` is `kind: library` with no user-facing surface, and the stage's `produces_kinds` maps `frontend-components` to `[ui]` only. The engine's resolved `produces` list for this unit confirms three artifacts, not four.
- **[assumption]** `src/data/registry.py` is **not** part of this unit. It appears in `component-methods.md` between two `foundation` modules, but `unit-of-work.md` § 1 does not list it under `Owns`, and the station registry belongs to `inventory-and-registry`. Design questions about `Station` and `load_registry` are therefore out of scope here.
- **[assumption]** `src/data/locked_test.py` is not this unit's either, notwithstanding that `foundation` owns the boundary rule that names it. § Shared resources fixes the carve-out that only that module may construct a path into `evidence/locked_test_restricted/`; the module itself belongs to `governance-guards` (BLK-07).
- **Open** — whether TA-03 covers all eight items of TE §13.1's environment lock or only the platform evidence. Question 7 option D depends on it and the claim is **unverified**; it will be checked against the row text before any artifact relies on it, per `project.md` § Way of Working on verifying a fact before handing it on as established.
- **Open** — the `required` field list from Question 1 cannot be fully enumerated until the four configs exist with their field names. Whatever mechanism is chosen, this stage specifies the *mechanism*; the concrete list is a Bolt 1 work product.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
