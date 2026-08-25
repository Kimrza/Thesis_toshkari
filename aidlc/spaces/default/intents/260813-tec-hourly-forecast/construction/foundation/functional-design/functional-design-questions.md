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

> ## 🔄 RE-ANSWERED 2026-08-25 — **D′: D minus monotonicity**
>
> **The answer above is superseded and preserved verbatim.** It is the record of what was
> answered and of the design that was built on it through 2026-08-24.
>
> **Why it was re-asked.** The project decision owner **declined Amendment C as drafted** on
> 2026-08-25, removing the durable, append-only release history. Monotonicity is information
> about *sequence*; a label that is a function of content alone cannot carry it, and no test
> recovers it. So D as answered had become unsatisfiable rather than merely unimplemented. The
> owner directed that Q6 be re-answered to drop the monotonicity requirement, and the question
> was re-presented for an explicit re-answer rather than amended silently.
>
> **[Re-answer]: D′** — Keep the **content hash as the authoritative release identity**
> (R-11, unchanged). Keep `dataset_version` as a **distinct, non-authoritative,
> human-readable field** on `ReleaseManifest` for citation at a human-reviewed gate — but
> **derive** it from the release `content_hash` rather than allocating it from a durable
> history. **Drop "monotonic."** **Drop the append-only release history**, the
> `ReleaseLedgerEntry` entity and `artifacts/registry/release_history.jsonl`. **Keep
> "never reused"** — now satisfied by determinism rather than by bookkeeping: a pure derivation
> allocates nothing and consults nothing, so the delete-and-rebuild failure that motivated the
> ledger cannot arise, and a label bound to two genuinely different contents reduces to a
> SHA-256 collision. **Keep label/hash mismatch as an integrity violation.** **Do not invent
> the hash-to-label encoding** — no approved artifact specifies one, and per TE §18.3 stage 3.5
> must stop and report rather than pick a default.
>
> **What is deliberately given up, recorded rather than absorbed.** Release labels can no
> longer be **ordered**. A reviewer citing two labels at a gate cannot tell from the labels
> alone which release came first; that must be read from the run record or the registry
> instead. This was accepted knowingly: the owner was shown that option C's derived label was
> the mechanism this question had originally declined, and on exactly the monotonicity
> reasoning above.
>
> **What is unchanged by the re-answer.** TE §13.3 and TA-15 still hold —
> `write_release` rejects an output directory that already holds a release and never
> overwrites release content, and repeated writes are not silently treated as successful. The
> canonicalization rule is unchanged: the authoritative hash is derived from a canonical
> representation that excludes the human-readable label, volatile metadata and any
> self-referential hash field. **No scientific value is decided, and G-09 remains unsigned.**
>
> **Where this lands in the design:** `business-rules.md` **R-12** (rewritten, with three
> negative controls — correspondence, derivation determinism, and injectivity against a
> degenerate encoding), `business-logic-model.md` **W-7** (step 7 removed, step 5 changed to
> derivation), and `domain-entities.md` **§ 8** (entity withdrawn; eight live entities).

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

> ## 🔄 SUPERSEDED 2026-08-25 — the follow-up is moot; its parent answer changed
>
> **The answer above is superseded and preserved verbatim.** FU-2 exists only to locate the
> ledger that **Q6=D** required. **Q6 was re-answered on 2026-08-25 as D′**, dropping the
> monotonicity requirement and the durable append-only history with it, after the project
> decision owner **declined Amendment C as drafted**. With no ledger to place, FU-2 has no
> subject: there is no release-history file, no owner for one, no schema, no append-only
> behaviour and no label-allocation rule, because `dataset_version` is **derived** from the
> release `content_hash` instead of allocated.
>
> **Its integrity obligation is discharged rather than dropped.** FU-2=D required *"an
> independent integrity test that rejects duplicate or reused labels and inconsistent
> label/hash mappings."* The inconsistent-mapping half is carried by R-12's
> derivation-correspondence control, joined by two more that the ledger design never had —
> derivation determinism, and injectivity against a degenerate or truncating encoding. The
> duplicate-and-reused-label half becomes **vacuous**: with no rows there is nothing to
> duplicate, and with the label a function of the hash, reuse across different content reduces
> to a SHA-256 collision.
>
> **Its final clause was honoured, not bypassed.** FU-2=D closed: *"If introducing this ledger
> changes an approved ownership list, artifact inventory, or governed design, raise the
> required change request rather than modifying approved artifacts silently."* **Removing** it
> changed two approved artifacts the same way, and the same discipline was applied in reverse:
> `functional-design` **reported** both sites rather than editing them, because its scope
> control forbade touching an approved Inception artifact; the owner then authorised the edits
> explicitly on 2026-08-25. `unit-of-work.md` § 1 `foundation` → `Owns` no longer names
> the ledger and `services.md` § Run record and registry now reads *"Two artifacts, one
> authoritative"*, both with their superseded wording preserved in place. A search across
> `construction/` confirmed **no other unit referenced the ledger**, so nothing further was
> orphaned.

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

> **❌ RAISED AND DECLINED 2026-08-24** by the project decision owner
> (`CR-2026-08-24-FOUNDATION-AMENDMENTS`). The request as raised is preserved below.
>
> **Why it was declined.** No project rule requires universal §19 coverage — the
> requirements, all memory layers and both authority documents were searched and no
> such rule exists. The approved position is the opposite: `unit-of-work-story-map.md`
> dispositions uncovered requirements as *"Open by design"*. This unit already designs
> both requirements as enforceable obligations without the rows, and **TA-37 would have
> passed vacuously** — its subject is tags on G-05, G-06 and the phase transitions,
> none of which has occurred.
>
> **This resolves Q7=X rather than contradicting it.** Q7=X directed that the request
> be *raised*; it was, and the owner declined it. Raising a request never obliged its
> approval.
>
> **Consequence:** REQ-ENG-7 and REQ-ENG-10 remain untested **by design, permanently
> rather than pending**. The negative-path test specifications in `business-rules.md`
> keep their *"Test specification only — not an approved acceptance row"* label as a
> settled state. No count propagated: untested stays **36**, this unit's stays **2 of
> 16**, its acceptance rows stay **7**, and §19 stays at **36** rows.

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

> **✅ APPLIED 2026-08-24.** The paragraph above records the state when this request
> was raised and is preserved as that record. Amendment B was **approved** by the
> project decision owner and executed under
> `CR-2026-08-24-FOUNDATION-AMENDMENTS`: `component-methods.md` now defines **nine**
> fields (derived: `awk … | grep -cE "^ +[a-z_]+: "` → `9`), and the three artifacts
> have been updated so the specification and the contract now agree. **R-06 is
> unchanged** — an empty `nondeterministic_ops` is still never proof of determinism.

## Amendment C — the release-history ledger (approved 2.6 and 2.7 artifacts)

> **✅ APPROVED AND APPLIED 2026-08-24** under
> `CR-2026-08-24-FOUNDATION-AMENDMENTS`. `unit-of-work.md` § 1 `foundation` → `Owns`
> now names the ledger, and `services.md` § Run record and registry reads **three
> artifacts, one authoritative**. The request as raised is preserved below.
>
> **Its authority was re-examined before approval and corrected.** A draft of the
> change record proposed *rejecting* C on the grounds that no requirement mandates a
> ledger — true of `requirements.md` and the eight upstream artifacts, but the search
> had not covered this stage's own answers, where **Q6=D** and **FU-2=D** mandate it.
> The proposed replacement, deriving the label from the content hash, is **Q6 option
> C** — read and declined by the owner — and cannot produce the *monotonic* label
> Q6=D requires, since monotonicity needs durable state. The rejection was withdrawn.

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

## Consolidated Summary Confirmation (2026-08-23 pass, answered and superseded by the re-entry below)

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes


### Re-confirmation, 2026-08-22 — after a redo jump for a fresh reviewer pass

The first confirmation was recorded at this checkpoint and the three artifacts were
generated and reviewed. The adversarial reviewer returned **NOT-READY twice**, and
both verdicts were confirmed correct:

- **Iteration 1** — the requirement-to-acceptance-row mapping was wrong in **8 of
  14** cited rows and incomplete in **2** more; only 4 were right. It had been
  reasoned from acceptance-row text rather than derived from story-map Table 1.
- **Iteration 2** — the `Row owner` column added to *fix* iteration 1 was wrong in
  **3 of its 4** multi-row entries (supporting units named as owners, and one unit
  absent from the row entirely), and the explaining sentence carried an underived
  count (13, actually 14).

Both were corrected, every superseded value preserved in place. **Those corrections
landed after the final reviewer pass, so they were unreviewed.** The project
decision owner directed a **re-review of `foundation` before any further unit**,
which required a redo jump to reset the exhausted 2-iteration budget. The jump also
moved the receipt floor past the original confirmation, so the summary is
re-presented here.

**No question, option, answer or amendment status changed under either correction.**
The eight base answers, the three follow-ups, the TA-03 verification and the three
PENDING amendments all stand exactly as recorded above. What changed is confined to
traceability citations in `business-logic-model.md` and `domain-entities.md`, and
the per-rule acceptance lines in `business-rules.md`.

### Re-confirmation, 2026-08-23 — after a stage-wide redo jump

A redo jump on `functional-design` (executed 2026-08-22T21:43Z) reset the receipt floor for
**every** unit of this stage, not only the unit it was aimed at. No question, option,
answer or amendment on this unit changed; the summary is re-presented because the prior
confirmation receipt no longer stands.

### Re-confirmation, 2026-08-23 (second) — after a second stage-wide redo jump

A redo jump aimed at correcting `external-products` reset the receipt floor for every unit
of this stage again. **No question, option, answer or amendment on this unit changed.**

### Re-confirmation, 2026-08-23 (third) — after a third stage-wide redo jump

A redo jump aimed at correcting a **misreading of `component-methods.md` § Depth** reset the
receipt floor for every unit of this stage. **No question, option, answer or amendment on
this unit changed.**

### Re-confirmation, 2026-08-23 (fourth) — after a fourth stage-wide redo jump

A redo jump aimed at sweeping two **question files** that had fallen stale against their
own corrected artifacts reset the receipt floor for every unit of this stage. **No
question, option, answer or amendment on this unit changed.**

### Re-confirmation, 2026-08-23 (fifth) — after a fifth stage-wide redo jump

A redo jump aimed at correcting four stale cross-references in `target-standardization`'s
question file reset the receipt floor for every unit of this stage. **No question, option,
answer or amendment on this unit changed.**

[Answer]: Looks correct

---

## Consolidated Summary Confirmation (2026-08-24 re-entry — superseded by the amendment pass below)

*(after the Inception re-run and a change assessment. **Superseded**: this section
states that Amendments A, B and C all stay pending. That was true when written and is
false now — A was declined and B and C were approved and executed on 2026-08-24 under
`CR-2026-08-24-FOUNDATION-AMENDMENTS`. Preserved as the record of what was presented.)*

**Why this confirmation is being retaken.** The backward jump from this stage on
2026-08-23 cleared every receipt while leaving the artifacts on disk. Three Inception
stages were then re-run — `application-design` produced **ADR-11**, `units-generation`
registered **BLK-08** and **BLK-09**, `delivery-planning` reconciled the Bolt plan and
recorded **D-27**. This unit's design was written before all of that, so it was
assessed against it before any receipt was sought.

**The assessment found nothing to change.** Six checks against everything that moved:

| Check | Result |
|---|---|
| Retired ADR-11 identifiers (`FoldSpec`, `apply_transforms`, `build_folds`) | **0** across all four files |
| References to `features-and-splits` or `evaluation-and-comparison` | **0** |
| Stale blocker spans, "six open", or a stale `40` | **none** |
| Blocker references | only **BLK-01** (correctly noted closed) and **BLK-07** as acquisition context |
| Its own figures — 16 requirements, 2 untested, 7 acceptance rows | match the current unit table; TA-33…TA-36 touched `external-products` and `features-and-splits` only |
| Stale ADR-10 authority claims (*"unsigned"*, *"no authority backing"*) | **none** |

The reason is structural rather than luck: `foundation` sits upstream of everything
ADR-11 changed. It owns config loading, determinism, run records, the registry and
releases — none of which touches the leakage boundary. BLK-08 and BLK-09 land on
Bolts 7 and 9; RES-05 is `inventory-and-registry`'s; the M10 fixture is Bolts 7 and
12; D-27 concerns the target transform. **None reaches this unit.**

### What this unit's functional design commits to

**Nine entities.** `ConfigSnapshot` (frozen per run — config hashes to the run record,
seeds to determinism); `DeterminismRecord`; `RunRecord`; `RegistryEvent`
(append-only); `ReleaseManifest` (immutable, content-addressed); `ReleaseLedgerEntry`;
two static maps — `RequiredFieldsMap` keyed by `(stage, phase)` and
`CredentialNameMap`, which `ConfigSnapshot` **declares and never consumes**; and
`IntegrityError` as an entity in its own right, the single catchable base.

**Ten workflows** (W-1…W-10): the stage entry contract; `load_configs`
read/snapshot/hash/resolve; preflight `assert_no_tbd` and
`assert_declared_sources_exist`; `seed_everything` plus the determinism probe;
opening the run record; registry append; `write_release` and label allocation;
`resolve_platform_roots` with its credential precondition; what Bolt 1 builds and must
not; and fixture-scale-only with the in-Kaggle obligation.

**Business rules worth naming.** Preflight rejects a *missing* field and a `TBD` field
alike (R-02); an authorized `TBD` in Bolt 1 is expected evidence, not a failure
(R-04); determinism applies before graph construction, re-exec first (R-05); an empty
`nondeterministic_ops` is **never proof** of determinism (R-06); registry writes never
read run history (R-08); the **content hash is authoritative** and the release label is
explicitly not (R-11); and on integrity failure, report honestly even when reporting
itself fails (R-10).

### The three amendments stay PENDING and unapproved *(as written 2026-08-24, before the rulings — SUPERSEDED: A declined, B and C approved and executed the same day)*

The assessment confirmed each is correctly classified into its own authority class —
conflating them would overstate two of the three:

| Amendment | Authority class | Why it stays open |
|---|---|---|
| **A** — §19 rows for REQ-ENG-7 and REQ-ENG-10 | **Vision §15.2** — an authority-document change | `requirements.md` marks both `UNTESTED`; TA-03 covers neither fully (two partials, both install-time rather than per-run). Yours to approve or decline |
| **B** — three `DeterminismRecord` fields | **Approved-artifact annotation** (`GOV-2026-08-22-INC-01` Rec 7 precedent) | Your own **Q3=C** answer mandates recording probe scope, detected mismatches and a `partial` / `not-yet-measured` classification. `component-methods.md` defines six fields. **No requirement fixes the field set** — so this is not a §15.2 change |
| **C** — the release ledger | **Approved-artifact annotation**; **no §12 amendment needed**, derived | *"ledger"* appears **0 times** in `requirements.md` and all eight approved upstream artifacts. TE §13.3 requires `dataset_version` as a *"Stable release ID"* but mandates no ledger, and R-11 makes the label non-authoritative. The weakest of the three |

**Nothing here claims what is not approved.** No acceptance coverage is claimed for
REQ-ENG-7 or REQ-ENG-10; no output states or implies determinism has been measured
(W-4: *"Silence is the correct output"*); the ledger appears in no approved `Owns`
list, and `component-methods.md`, `services.md` and `unit-of-work.md` are unedited.
That is what your **Q7=X** answer directed.

**G-09 is not signed.** Nothing in this design authorises creating a module.

### Limits on what this confirms

I verified these artifacts against everything that changed upstream and against the
six questions in the assessment. I did **not** independently re-derive all ten
workflows and thirteen business rules against their cited sources *(the count is wrong and was wrong when written: seventeen, R-01–R-17, derived 2026-08-25 on reviewer finding M-1)* — that was the
original review's work, and it returned **READY**.

Does this all look correct before the stage proceeds?

- Looks correct
   > **Impact**: The confirmation receipt is recorded for `foundation`, and the workflow moves to the next unit in functional design. Amendments A, B and C stay pending and unapproved; nothing is marked resolved and no module is authorised.

- Request changes
   > **Impact**: No receipt is recorded. Tell me what to change — including deciding any of A, B or C, or reopening the stage body for this unit — and I re-present first.

> **💡 Recommendation**: **Looks correct** — the assessment's minimal edit set was empty, and the design already handles all three open items the way this project's rules require: specify the target, claim nothing unapproved.

[Answer]: Superseded — not answered. The owner ruled on Amendments A, B and C
instead, which changed the facts this summary asserted. See the amendment pass below.

---

## Consolidated Summary Confirmation

*(2026-08-24 — the amendment pass)*

**What changed since the last summary.** That summary said Amendments A, B and C all
stay pending. The owner then ruled on all three, an independent challenge of each
against the approved artifacts followed, and one of the three rulings was reversed on
evidence. All of it is executed and recorded in
`governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md`.

### The three rulings

| | Decision | Authority | What it means for this unit |
|---|---|---|---|
| **A** — §19 rows for REQ-ENG-7 and REQ-ENG-10 | **DECLINED** | Owner, on the evidence that **no rule requires universal §19 coverage** and that the approved position dispositions uncovered requirements as *"Open by design"* | Both stay untested **by design, permanently**. Their negative-path test specifications keep the *"Test specification only"* label as a settled state, not a provisional one. **No count moved** — untested stays 36, this unit's 2 of 16, its acceptance rows 7, §19 at 36 rows |
| **B** — three `DeterminismRecord` fields | **APPROVED** | Owner, under the Rec 7 annotate-in-place precedent. Required by your own **Q3=C** answer, which the six-field contract could not record | `component-methods.md` now defines **nine** fields. W-4 steps 5–7 are fully recordable and **the prohibition on stating that determinism was measured is lifted** — replaced by a narrower rule: a measured claim requires `probe_scope` recorded and `measurement_status` = `complete`. **R-06 unchanged** |
| **C** — the release-history ledger | **APPROVED** | Owner, on the authority of **Q6=D** and **FU-2=D** | `services.md` reads **three artifacts, one authoritative**; `unit-of-work.md` § 1 `Owns` names the ledger. **R-11 unchanged** — the content hash stays authoritative and the label is a citation device |

### One reversal, recorded rather than buried

A draft of the change record proposed **rejecting C**, on the finding that *"ledger"*
appears **0 times** in `requirements.md` and the eight approved upstream artifacts —
true, but the search had never covered **this stage's own answered questions**. **Q6=D**
requires a *monotonic, human-readable* label alongside the hash, and **FU-2=D** names
the durable append-only ledger, its ownership and its append behaviour.

The replacement that draft proposed — deriving `dataset_version` from `content_hash` —
is **Q6 option C**, which you read and declined in favour of D. It also cannot produce
a *monotonic* label, because monotonicity requires durable state. The rejection was
withdrawn and C reinstated on the same logic that makes B required: an approved stage
answer mandates something the upstream artifacts do not express.

### What was executed

Six planned sites, plus two the sweep found in this file's own Amendment sections.
Two superseded literals swept and both re-derived rather than decremented:
`DeterminismRecord` **6 → 9** fields, and `services.md` **two → three** artifacts. The
sweep also caught a box **heading** in `domain-entities.md` still asserting the
superseded claim while its body said otherwise, and a duplicate bullet introduced
during execution — both corrected.

**Confirmed untouched**, because A was declined: the Technical Environment §19 table,
`requirements.md`, and every untested and acceptance figure across
`components.md`, `unit-of-work.md`, `unit-of-work-story-map.md`, `bolt-plan.md`,
`risk-and-sequencing-rationale.md` and `phase-check-inception.md`.

### What still stands unchanged

The design itself — nine entities, ten workflows W-1…W-10, thirteen business rules *(count wrong when written; seventeen, R-01–R-17, derived 2026-08-25 on reviewer finding M-1)*.
**G-09 is not signed**, so nothing here authorises creating a module. No scientific
value was decided. ADR-11, D-27 and BLK-02…BLK-09 are untouched. The concrete
`RequiredFieldsMap` and `CredentialNameMap` contents still await the four configs
existing — this stage fixes the mechanism only.

Does this all look correct before the stage proceeds?

- Looks correct
   > **Impact**: The confirmation receipt is recorded for `foundation` and the workflow moves to the next unit in functional design. The three amendments are settled — A declined permanently, B and C approved and executed.

- Request changes
   > **Impact**: No receipt is recorded. Tell me what to change — including revisiting any of the three rulings or the change record — and I re-present first.

> **💡 Recommendation**: **Looks correct** — the three amendments are resolved, the two superseded literals are swept and re-derived, and the artifacts now agree with the contracts they cite.

*(Answered `Looks correct`, 2026-08-24T12:36:34Z. That receipt is superseded by the
addendum re-confirmation below, which was required because this file changed after it.
The live answer tag for this section is the blank one at its end.)*

### Re-confirmation — the three sites the amendment sweep missed

**Why this is being re-asked.** Three sites asserting a **superseded amendment status**
were found while verifying two execution defects raised at `governance-guards`'s sixth
summary confirmation. You approved the annotate-in-place exception on 2026-08-24. One of
the three corrections lands in **this file**, which changes it after the receipt above and
so requires a fresh response. They are recorded as sites **9, 10 and 11** in
`governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md` § Addendum.

| # | Site | What was stale | Applied |
|---|---|---|---|
| 9 | `business-logic-model.md` § Review (dated 2026-08-22) | Three statements: § Regression checks' *"Amendments A/B/C nowhere treated as approved"* and *"No determinism claimed as measured … while Amendment B is pending"*, and § Implementability's *"`DeterminismRecord`'s three pending fields and the release ledger await Amendments B and C"* | One dated annotation box at the head of § Review. **The READY verdict is untouched, no finding withdrawn, no reviewer sentence rewritten** — the box names the three statements and their current state; the reviewer's text stands as the dated record of what that reviewer saw |
| 10 | `domain-entities.md` § 5, REQ-ENG-10 acceptance-status box | *"A row is **sought** under Amendment A (Vision §15.2), not approved"* — reads the gap as provisional when **A was declined**, i.e. permanent. §§ 9, Coverage and Assumptions in the same file already read correctly, so this was a missed site rather than a disagreement | Rewritten to *"No row is sought … untested by design, permanently rather than pending"*, superseded wording preserved |
| 11 | **this file**, the § heading above at line 736 | *"### The three amendments stay PENDING and unapproved"* — its body sits inside a section already marked superseded, but the **heading** asserted the false claim unqualified | Heading qualified in place. Same *"heading still asserting the superseded claim while its body said otherwise"* class the change record's § Sweep result already reported once |

**Why the original sweep missed all three.** It was keyed to two literals —
`DeterminismRecord` *"six fields"* and `services.md` *"two artifacts"*. None of the three
contains either: 9 and 11 assert **amendment status** rather than a count, and 10 turns on
the single word *"sought"*. This is the failure mode `project.md` § Way of Working already
names — sweep the **status claims** an amended figure supported, not only the superseded
numeral.

**What did not change.** **No count moved** — untested stays 36, this unit's stays 2 of 16,
its acceptance rows stay 7, TE §19 stays at 36 rows. No rule, entity, workflow or contract
was edited. No scientific value was touched. The three rulings themselves are unchanged: A
declined permanently, B and C approved and executed. **G-09 remains unsigned.**

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: A fresh confirmation receipt is recorded for `foundation` and the stage continues to the next unit. Sites 9, 10 and 11 stand as applied, with every superseded wording preserved in place.

- Request changes
   > **Impact**: No receipt is recorded. Tell me what to change — including reverting any of the three annotations — and I re-present before touching anything.

> **💡 Recommendation**: **Looks correct** — all three corrections execute rulings you had already approved, none decides anything new, no count or scientific value moved, and each preserves its superseded wording rather than erasing it.

*(Answered `Looks correct` earlier on 2026-08-24; that receipt was reset by the authorised redo jump below. The live answer tag for this section is the blank one at its end.)*


### Re-confirmation, 2026-08-24 (post-redo) — receipt floor reset by an authorised redo jump

**Why this is being re-asked, and it is not about this unit.** The project decision owner
authorised a **redo jump on `functional-design`** at **2026-08-24T14:57:07Z**, so that three
standing reviewer findings on **`models-and-baselines`** (unit 8) could be fixed and
re-reviewed — its adversarial budget had been exhausted at NOT-READY, and the write-freeze on a
terminal review receipt made a redo the only route to a fix. **A redo resets the receipt floor for
every unit of the stage**, which is the stated cost that was accepted when the redo was chosen.

**Nothing in `foundation` changed.** No question, option, answer, amendment, rule, entity or
workflow of this unit was touched after its earlier confirmation today. The only artifacts edited
after the redo are `models-and-baselines`'s; its three fixes are confined to its own
files and reach no contract this unit consumes.

**The redo bought what it was for.** `models-and-baselines` returned **READY** on the
second pass of the restored budget, after three further Major findings were fixed. Two residuals
ride that READY verdict and are carried to the stage gate rather than applied.

**Everything this unit carried to the gate still stands, unchanged**, as recorded above.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The receipt is recorded for `foundation` under the post-redo floor and its three artifacts are re-saved. No answer, rule, entity, count or scientific value changes.

- Request changes
   > **Impact**: No receipt is recorded and nothing is re-saved. Tell me what to change and I re-present first.

> **💡 Recommendation**: **Looks correct** — this unit is untouched; the reset is a mechanical consequence of a redo taken for a different unit, and that redo achieved what it was authorised for.

*(Answered `Looks correct`, 2026-08-24T15:26:16Z. That receipt was reset by the sixth stage-wide redo jump, 2026-08-25T06:30:05Z. The live answer tag for this section is the blank one at its end.)*


### Re-confirmation, 2026-08-25 (post-redo) — sixth stage-wide receipt-floor reset

**Why this is being re-asked, and again it is not about this unit.** The stage wedged on
`models-and-baselines`. Its post-redo sequence ran out of order: the three artifacts were
written (2026-08-24T14:57:33Z, 15:16:20Z) and the adversarial reviewer returned **READY** on
iteration 2 of 2 (15:16:47Z), and only then was its summary confirmation recorded
(15:32:45Z). The engine requires a produces-artifact write *after* the confirmation receipt;
the attempted re-save at 15:32:59Z was refused by the write-freeze hook because a fresh
READY receipt covered the unit, and the adversarial budget of 2 was spent, so no further
reviewer pass could be requested. That is a genuine deadlock whose only sanctioned exit is a
redo jump, which the project decision owner authorised at **2026-08-25T06:30:05Z**. **A redo
resets the receipt floor for every unit of the stage** — the stated and accepted cost.

**Nothing in `foundation` changed.** No question, option, answer, amendment, rule, entity,
workflow or count of this unit was touched since its 2026-08-24T15:26:16Z confirmation. No
file this unit consumes changed after its artifacts were written: `component-methods.md`,
`services.md` and `unit-of-work.md` were last modified at **12:26 UTC**, three hours before
the 15:27 UTC artifact writes. *(Corrected 2026-08-25 on reviewer finding m-5: the clause that followed — "and their content is committed at `9c7afd9` unchanged" — was overstated when generalised to all six consumed files. Per-file derivation: `unit-of-work.md`, `component-methods.md` and `services.md` are at `9c7afd9`; `unit-of-work-story-map.md` and `components.md` are at `45796f5`; `requirements.md` is at `89674b6`. Every one is older than this unit's artifacts, so the substance holds, but the derivation had never enumerated its scope.)*

**Independent re-derivation, run before seeking this receipt** — because a count carried from
prose rather than derived from the artifact is this project's recorded repeat defect
(`project.md` § Way of Working). Every figure was re-derived programmatically from the
current `unit-of-work.md` § 1 rather than read from adjacent text:

| Figure | Declared upstream | Derived from the ID list | Asserted in this unit's artifacts |
|---|---|---|---|
| Requirements carried | 16 | **16** (REQ-ENG-1, -2, -3, -4, -6, -7, -8, -10, -11, FR-P1-01-10, FR-P1-04-11, FR-P1-05-13, FR-WS-7, NFR-AUD-01, NFR-SEC-01, NFR-DET-01) | *"16 requirements"*, *"2 of 16"* — agrees |
| Untested (no §16/§19 row) | 2 of 16 | **2** (REQ-ENG-7, REQ-ENG-10 — the bolded pair) | agrees |
| Acceptance rows | 7 | **7** (TA-01, TA-02, TA-03, TA-10, TA-15, TA-22, TA-23) | all seven cited; agrees |

**No defect was found, so nothing was revised.** The owner's direction for this recovery was
evidence-driven revision rather than a blanket re-derive: keep the adversarially-verified text
as the baseline and edit only where a real defect is found. None was, so the three artifacts
are re-saved unchanged and go back to the reviewer for a fresh verdict under the restored
2-iteration budget.

**Everything this unit carried to the gate still stands, unchanged.** Nine entities, ten
workflows W-1…W-10, and **seventeen** business rules R-01–R-17. *(Corrected 2026-08-25 on reviewer finding M-1, which was Major: this line read "thirteen business rules", carried from the prose of an earlier section rather than derived. `grep -cE "^## R-[0-9]+" business-rules.md` returns **17**; `business-logic-model.md` § Implementability already read "the seventeen rules (R-01–R-17)" correctly, so the two disagreed. Superseded wording preserved here.)* Amendment A declined permanently, B and C
approved and executed. Sites 9, 10 and 11 stand as applied. **G-09 remains unsigned**, so
nothing here authorises creating a module. No scientific value was decided.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The receipt is recorded for `foundation` under the sixth post-redo floor and its three artifacts are re-saved, then re-reviewed. No answer, rule, entity, count or scientific value changes.

- Request changes
   > **Impact**: No receipt is recorded and nothing is re-saved. Tell me what to change — including revisiting the evidence-driven revision scope — and I re-present before touching anything.

> **💡 Recommendation**: **Looks correct** — this unit is untouched, the reset is a mechanical consequence of a redo taken for `models-and-baselines`, and every figure was re-derived from the current upstream artifact rather than carried from prose.

*(Answered `Looks correct`, 2026-08-25T06:58:26Z. That receipt no longer stands: this file changed after it, to correct two errors the adversarial reviewer found in the section above — see the re-confirmation below. The live answer tag is the blank one at its end.)*


### Re-confirmation, 2026-08-25 (second) — the adversarial reviewer refuted the section above

**Why this is being re-asked, and this time it IS about this unit.** The confirmation above
was recorded, the three artifacts were re-saved, and the adversarial reviewer was dispatched
for iteration 1 of the restored 2-iteration budget. It returned **NOT-READY** with seven
findings, all seven verified at their named locations before anything was touched. **Two of
them are defects in the re-save annotations written during this recovery**, and one of those
two is in the confirmation section above — which is why that receipt could not stand and this
question is being put again rather than the fix being applied quietly.

**The verdict is accepted in full. Every finding is real.**

#### The two defects this recovery introduced

| # | Severity | Where | What was wrong | Corrected |
|---|---|---|---|---|
| **M-1** | **Major** | `business-rules.md` line 586, and the section above | *"The thirteen rules, their IDs and their acceptance citations are unchanged"* — the rule count. `grep -cE "^## R-[0-9]+" business-rules.md` returns **17** (R-01…R-17). `business-logic-model.md` § Implementability already read *"the seventeen rules (R-01–R-17)"* correctly, so the two artifacts contradicted each other | Corrected to **seventeen, R-01–R-17**, derived rather than read. Two further sites carrying the same wrong figure in already-superseded sections of this file (lines 759, 825) are annotated in place, superseded wording preserved |
| **m-5** | Minor | all four files of this unit | *"Every consumed upstream file … committed unchanged at `9c7afd9`"* — true for three of six. Per-file: `unit-of-work.md`, `component-methods.md`, `services.md` at `9c7afd9`; `unit-of-work-story-map.md`, `components.md` at `45796f5`; `requirements.md` at `89674b6` | Corrected to enumerate all six. **The substance is unharmed** — every one is older than this unit's artifacts, so the no-drift conclusion stands; what was wrong is that the derivation never enumerated its scope |

**M-1 is the exact defect the section above claimed to be guarding against.** That section
opens by naming this project's recorded repeat failure — a count carried from prose rather
than derived from the artifact — derives three figures correctly, and then closes by carrying
a fourth from the prose of an earlier section. It is recorded here rather than quietly fixed
because it bears on how much weight a derived-count assurance in this file should carry.

#### Five pre-existing stale sites the earlier sweep missed, all in `business-rules.md`

Every one asserts a **superseded amendment status**. All five are in the same file, and none
carries a numeral — which is why a sweep keyed to `DeterminismRecord` *"six fields"* and
`services.md` *"two artifacts"* could not see them. This is the failure mode
`project.md` § Way of Working already names, recurring in the one file the addendum sweep
had certified as clean.

| # | Severity | Line | What it asserts | Fix |
|---|---|---|---|---|
| **M-2** | **Major** | 515 | *"Open — Amendments A, B and C. All three **PENDING and NOT approved**"* — refuted in the passed contracts: the ledger is in `unit-of-work.md` § 1 `Owns`, `services.md` reads *"Three artifacts, one authoritative"*, `DeterminismRecord` carries nine fields. Both sibling artifacts swept this same bullet; this file's § Assumptions was not | Rewrite to the settled state — A declined permanently, B and C approved and executed — superseded wording preserved |
| **M-3** | **Major** | 5–11 | The addendum box asserts *"**None of them is in this file** … already read correctly"*. Refuted by M-2, M-4, m-1 and m-2 — four stale sites in this file. This self-certification is why the file was never swept | Correct the box: the claim was false when written, and name the four |
| **M-4** | **Major** | 224–225 | *"No row accepts the scope or status fields, **because they are not yet in the contract**"* — they are, per Amendment B, as the box thirty lines above says. **The conclusion survives; the stated reason is refuted.** Carries no numeral — the precise blind spot | Keep the conclusion, replace the reason, preserve the superseded clause |
| **m-1** | Minor | 507–509 | *"not claimed **until the amendment is approved**"* — Amendment A was **declined**, so the condition can never be met and the sentence contradicts the acceptance box above it | Restate as permanent-by-design |
| **m-2** | Minor | 192 | Heading *"⚠ THIS RULE IS NOT FULLY ENFORCEABLE UNDER THE APPROVED CONTRACT"* directly above its own first line *"✅ Amendment B APPROVED 2026-08-24"*. Both siblings rewrote the equivalent heading; this one was missed — the same heading-versus-body class the change record already reported once | Qualify the heading in place |

#### Two design findings, and what I propose to do with them

| # | Severity | Finding | Proposed |
|---|---|---|---|
| **m-3** | Minor | **`reexec_performed` has no carrier.** `ensure_process_determinism(argv) -> None` re-execs the interpreter, but the child process cannot distinguish a re-exec from an externally exported `PYTHONHASHSEED`. W-4 step 4 captures the field and R-05's negative control asserts it `True`. No marker is named anywhere, so stage 3.5 would have to invent one | Name the carrier explicitly in W-4 and R-05: a sentinel environment variable set immediately before `os.execv` and read by the child. This is an **engineering** decision with no scientific content and no governed value, so it is inside this stage's remit — but it is a decision, not a derivation, so it is put to you here rather than assumed |
| **m-4** | Minor | **W-1 step 4 calls `assert_phase_boundary`**, which `component-methods.md` places in `src/data/phase_contract.py`, owned by `governance-guards` — while this unit is declared to *"import nothing from any other unit — this is the DAG's first root"*. Undisclaimed contradiction | Disclaim it: the stage-entry contract **sequences** the call, and the boundary statement is about `foundation`'s own module imports. If instead this is a real import, it breaks the DAG root claim and belongs upstream in `units-generation` — I would raise it rather than paper over it |

#### What is NOT being changed

- **No finding is being applied to any `## Review` section.** Prior review sections are the
  dated record of what each reviewer saw. The reviewer's own residual notes point at
  `business-logic-model.md` lines 514 and 520 (a review-history row marking a completed pass
  *"pending"*, and an unannotated *"`DeterminismRecord` fields = 6"*), both inside § Review —
  they are named at the gate, not rewritten.
- **No count moved.** Requirements stay 16, untested stays 2 of 16, acceptance rows stay 7,
  §19 stays at 36 rows, untested total stays 36. The rule count was never 13; it is 17 and
  always was — the figure was misreported, not changed.
- **No scientific value was decided, and G-09 remains unsigned.** Nothing here authorises
  creating a module.
- **The reviewer confirmed the design itself.** Quoting its close: *"The design is sound —
  every defect is in the status-and-count layer a human reads at the gate."* It independently
  reproduced 16 requirements, 2 untested by two paths, 7 acceptance rows, 9
  `DeterminismRecord` fields, `services.md`'s three artifacts, 9 entities, 10 workflows, and
  the full Table 1 and Table 2 traceability cell for cell, and verified G-09, the Phase 1
  prohibition, the IRI allowlist and the locked-test carve-out are all honoured.

**One iteration of the budget remains.** Fixes are applied after this confirmation, then the
reviewer runs iteration 2. If that returns NOT-READY, the budget is spent and the remaining
findings go to the stage approval gate for your decision rather than into another repair loop.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: A fresh receipt is recorded, then the eight fixes above are applied — M-1 through M-4, m-1, m-2, m-5, plus m-3's named sentinel and m-4's disclaimer — every superseded wording preserved in place. The reviewer then runs iteration 2, the last of the budget.

- Request changes
   > **Impact**: No receipt is recorded and no fix is applied. Tell me what to change — including ruling differently on m-3 or m-4, or declining any fix and sending it to the gate as a residual instead — and I re-present before touching anything.

> **💡 Recommendation**: **Looks correct** — the verdict is correct on all seven findings and I verified each at its named location. The two design findings (m-3, m-4) are the only ones carrying a judgement, and both are flagged rather than assumed; everything else is a factual correction with its superseded wording preserved.

*(Not answered. The 2026-08-25 second re-confirmation was superseded before a response was recorded: the owner ruled on the seven findings and reversed Amendment C, so the remediation summary below replaces it. The live answer tag is the blank one at the end of this file.)*


### Re-confirmation, 2026-08-25 (third) — remediation executed, and Amendment C reversed

**What you ruled, and what was done.** You directed careful remediation of the seven
iteration-1 findings with no redesign, gave three explicit rulings, and told me to stop rather
than silently decide the two design findings. All seven findings are remediated. Both design
findings were investigated, put to you with their evidence, and applied only after your ruling.
**And one settled decision was deliberately reversed on your instruction: Amendment C is
declined as drafted.** That reversal is the largest change in this pass and is recorded in full
rather than absorbed.

#### The seven findings

| Finding | Sev | Fixed | Where | Verification |
|---|---|---|---|---|
| **M-1** | Major | ✅ | `business-rules.md` re-save box; three sites in this file (955 rewritten, 759 and 825 annotated in place) | `grep -cE "^## R-[0-9]+" business-rules.md` → **17**. Prose now reads *"seventeen rules R-01–R-17"*, agreeing with `business-logic-model.md` § Implementability. **Correction to your Part 1:** the rules live in `business-rules.md`; `business-logic-model.md` has **zero** `## R-` headings, so the verify command named the wrong file |
| **m-5** | Minor | ✅ | all three artifacts + this file — a per-file provenance table replaces the generalised claim | 6/6 enumerated: `unit-of-work.md`, `component-methods.md`, `services.md` → `9c7afd9`; `unit-of-work-story-map.md`, `components.md` → `45796f5`; `requirements.md` → `89674b6`. **No-drift conclusion unchanged** — all six predate this unit's artifacts |
| **M-2** | Major | ✅ | `business-rules.md` § Assumptions | The all-three-pending bullet now states A declined, B approved, C declined as drafted. Superseded wording preserved. Live occurrences of *"All three **PENDING**"*: **0** — the one remaining match is inside the preserved quotation |
| **M-3** | Major | ✅ | `business-rules.md` lines 5–11 addendum box | The *"none of them is in this file"* self-certification is corrected and the four sites it missed are named (M-2, M-4, m-1, m-2), with the superseded wording preserved verbatim |
| **M-4** | Major | ✅ | `business-rules.md` R-06 § Acceptance | Conclusion preserved and re-evidenced: `probe_scope` and `measurement_status` appear in **no** acceptance table anywhere in this workspace — only `component-methods.md` and the change record. New reason: no §16/§19 row was added or amended, Amendment A declined, §19 held at 36 |
| **m-1** | Minor | ✅ | `business-rules.md`, acceptance-coverage note | The unsatisfiable *"until the amendment is approved"* is replaced by permanent-by-design. No new dependency on Amendment A; A is not reopened |
| **m-2** | Minor | ✅ | `business-rules.md` R-06 heading | Now *"✅ THIS RULE IS ENFORCEABLE UNDER THE APPROVED CONTRACT"*; the old heading appears **0** times as a heading. The enforceability conclusion is the one the body already evidences — not adjusted to make the heading fit |

#### The two design findings — investigated, then ruled

**m-3 — a carrier IS required, and you chose the sentinel environment variable.** Evidence:
`ensure_process_determinism(argv) -> None` returns nothing, so nothing crosses the `exec`
boundary in its return value; the child's environment looks identical whether it is a re-exec
child or a process with an externally exported `PYTHONHASHSEED`. `reexec_performed` is an
**approved** `bool` field, W-4 step 4 captures it, and R-05's negative control asserts it
`True` — a test that cannot discriminate without a carrier. Minimum information crossing: **one
bit**. Applied: a sentinel set immediately before `os.execv`, read once by the child, recorded
in W-4 and as a new constraint on R-05. The variable's **name is deliberately not fixed** — it
is an implementation identifier with no scientific content, so it is not a TC-03e constant. The
approved stage-2.6 `-> None` signature is **unchanged**; the alternative that returns `bool`
would have required amending an approved contract.

**m-4 — a sequencing reference, not an import; you chose to document the distinction.**
Evidence: `component-methods.md` states `assert_phase_boundary` is *"Called at entry by every
phase-aware stage script"*, and W-1 is described here as *"identical in all nine scripts"* — so
the **caller is the script**, which may import from both units, and `src/data/config.py` does
not import `phase_contract.py`. `unit-of-work.md` § 2 gives `phase_contract.py` to
`governance-guards` and records `Q5=A` confirming it. Decisive independent check:
`unit-of-work-dependency.md` has `foundation depends_on: []` and
`governance-guards depends_on: [foundation]` — a real import would make the unit graph
**cyclic**, and `units-generation` validated it acyclic, so a genuine import would have failed
upstream validation rather than merely reading oddly. Applied as a note in W-1. **No design
change, no upstream decision required.**

#### Amendment C — reversed on your ruling, with its cost stated

You were shown the conflict before executing: `ReleaseLedgerEntry` **predated** Amendment C (C
propagated it upstream rather than creating it); its authority was **your own Q6=D and FU-2=D
answers**; deriving `dataset_version` from `content_hash` is **Q6 option C, which you read and
declined** on the reasoning that it cannot yield a *monotonic* label; and executing the reversal
necessarily deletes an entity and amends a workflow. You chose the full reversal with those
consequences stated. It is recorded throughout as a **deliberate override, not an oversight**.

What was applied, in this unit's three artifacts only:

| Site | Change |
|---|---|
| `domain-entities.md` § 8 | `ReleaseLedgerEntry` **withdrawn**, definition preserved verbatim beneath a withdrawal box. Section **not renumbered** — every cross-reference in this unit cites entities by number, so § 8 stays as the withdrawal record: **nine numbered sections, eight live entities** |
| `domain-entities.md` entity diagram + text fallback | Ledger node and its two edges removed; fallback rewritten; superseded sentences preserved |
| `domain-entities.md` REQ-ENG-7 row | `RegistryEvent, ReleaseLedgerEntry` → `RegistryEvent`, superseded value preserved |
| `business-logic-model.md` W-7 | **Step 7 removed**; step 5 changed from ledger allocation to derivation from `content_hash`; heading *"label allocation"* → *"label derivation"*. Superseded steps preserved verbatim |
| `business-logic-model.md` § Label allocation | Rewritten as § Label derivation, encoding explicitly **not** specified |
| `business-rules.md` **R-12** | Rewritten. **Amended, not deleted — the rule count stays 17** |
| All three, Amendment C status boxes | Approval boxes retained as dated records, each now headed by a declined-as-drafted box |

**What the reversal costs, stated rather than hidden.** Two obligations of **Q6=D** now have
**no mechanism**: the label is no longer **monotonic**, and **reuse is no longer detectable**
across a deleted and rebuilt release directory. The superseded R-12 text names that exact
failure as its reason for rejecting a derived index — the mechanism now mandated — so the
failure is **accepted, not solved**, and R-12's original negative control cannot pass and has
been replaced by a weaker label/hash correspondence check. Separately, the independent
ledger-integrity test **FU-2=D** required no longer exists and **is not replaced**.

**Two upstream artifacts now contradict this design and were NOT edited**, per your Part 5
scope control: `inception/units-generation/unit-of-work.md` § 1 `foundation` → `Owns` names
`artifacts/registry/release_history.jsonl`, and `inception/application-design/services.md`
§ Run record and registry reads *"Three artifacts, one authoritative"* where two is now
correct. Both need an upstream correction this stage will not make.

#### Counts — every figure you fixed is intact, derived not carried

| Figure | Value | Derivation |
|---|---|---|
| Requirements carried | **16** | ID list in `unit-of-work.md` § 1 |
| Untested | **2 of 16** | bolded pair REQ-ENG-7, REQ-ENG-10 |
| Acceptance rows | **7** | TA-01, TA-02, TA-03, TA-10, TA-15, TA-22, TA-23 |
| §19 rows | **36** | held; **no TA-37 or TA-38 added** — the only three mentions are prohibitions |
| Rules | **17** | `grep -cE "^## R-[0-9]+" business-rules.md` → 17 |
| Workflows | **10** | `grep -cE "^## W-[0-9]+" business-logic-model.md` → 10 (W-7 lost a step, not its existence) |
| Entities | **8 live** *(was 9)* | 9 numbered sections − 1 withdrawn. **This is the one count the reversal moves, and it moves because you authorised it** |

#### Governance state

A **declined** · B **approved** (three fields, nine total) · C **declined as drafted**, its
approval reversed · **G-09 unsigned** — nothing here authorises creating a module · no release
ledger created · no `release_history.jsonl` created · no scientific value decided · no `## Review`
section edited, on any artifact.

#### What remains open, and goes to the stage approval gate

1. **Q6=D has no mechanism for monotonicity or reuse detection.** Whether Q6=D should be
   re-answered is yours to decide, not this stage's.
2. **FU-2=D's independent ledger-integrity test is gone and unreplaced** — a coverage loss.
3. **`unit-of-work.md` and `services.md` need an upstream correction.**
4. The reviewer's own residual notes on `business-logic-model.md` § Review (a review-history row
   marking a completed pass *"pending"*; an unannotated *"`DeterminismRecord` fields = 6"*) —
   **named, not rewritten**, because prior review sections are the dated record of what each
   reviewer saw.

**One reviewer iteration remains.** After this confirmation the three artifacts are re-saved and
the reviewer runs **iteration 2, the last of the budget**. If it returns NOT-READY, the
remaining findings go to the stage approval gate for your decision rather than into another
repair loop.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: A fresh receipt is recorded, the three artifacts are re-saved, and the reviewer runs iteration 2. The Amendment C reversal stands as executed, with its costs and the two upstream contradictions carried to the stage gate.

- Request changes
   > **Impact**: No receipt is recorded and nothing is re-saved. Tell me what to change — including reinstating Amendment C, re-answering Q6, or reverting any individual remediation — and I re-present before touching anything.

> **💡 Recommendation**: **Looks correct** — every one of the seven findings is remediated with its superseded wording preserved, both design findings were ruled by you rather than assumed, and the Amendment C reversal is executed exactly as you directed with its costs named rather than smoothed over. The one figure that moved, entities nine → eight, moved because you authorised it.

*(Not answered. Superseded before a response was recorded: the owner directed that all defects be resolved rather than carried to the gate, then ruled on the two items this stage could not close itself — re-answer Q6 dropping monotonicity, and authorise the upstream edits. The remediation summary below replaces this section. The live answer tag is the blank one at the end of this file.)*


### Re-confirmation, 2026-08-25 (fourth) — all defects resolved, Q6 re-answered as D′

**What you directed after the third presentation:** *"resolve all the defects"* — rather than
carrying any of them to the stage gate. Then two rulings on the items I could not close myself:
**re-answer Q6 to drop monotonicity**, and **authorise the upstream edits**. All of it is done.
Nothing from the Amendment C reversal is left open.

#### The seven reviewer findings — unchanged from the third presentation, all remediated

M-1 (rule count 13 → **17**, derived), m-5 (per-file commit provenance, 6 of 6 enumerated),
M-2 (all-three-pending bullet), M-3 (the false *"none of them is in this file"*
self-certification), M-4 (a refuted reason replaced, conclusion preserved and re-evidenced),
m-1 (an unsatisfiable *"until the amendment is approved"* condition), m-2 (heading contradicting
its own body). Every superseded wording preserved in place. **Correction to the directive's
Part 1, restated because it matters for the verification command:** the rules live in
`business-rules.md`, which carries 17 `## R-` headings; `business-logic-model.md` carries
**zero**.

#### Three things that first read as open, and how each was actually closed

| | First read as | Closed by | Not by |
|---|---|---|---|
| **Never-reuse** | lost with the ledger | **Analysis.** The superseded R-12 objects to *allocation from an index*, and that objection does not transfer to a pure derivation: it allocates nothing and consults nothing, so there is no index to forget. Identical content yields an identical label **by construction**, and a label bound to two genuinely different contents reduces to a **SHA-256 collision** | a new mechanism, and not a decision |
| **FU-2's integrity test** | removed, unreplaced | **Analysis.** Its inconsistent-mapping half is carried by R-12's derivation-correspondence control, now joined by two the ledger design never had — derivation **determinism** and **injectivity** against a degenerate or truncating encoding. Its duplicate-and-reused-label half is **vacuous**: no rows to duplicate, and reuse across different content is a hash collision | a decision |
| **Monotonicity** | irreducibly unmet | **Your ruling.** Ordering is information about *sequence*, which a function of content alone cannot carry — no test or implementation choice reaches it. So the **requirement changed rather than the mechanism**: Q6 re-answered as **D′** | analysis, which could not reach it |

#### Q6 = D′, re-presented rather than amended silently

The original **Q6 = D** answer is preserved verbatim; the re-answer sits beneath it. **D′**
keeps the content hash authoritative (R-11), keeps `dataset_version` as a distinct,
non-authoritative citable field on `ReleaseManifest`, but **derives** it from `content_hash`
instead of allocating it. It **drops "monotonic"** and drops the append-only history,
`ReleaseLedgerEntry` and `release_history.jsonl`. It **keeps "never reused"** — now satisfied by
determinism — and keeps label/hash mismatch as an integrity violation. It does **not** invent
the hash-to-label encoding: no approved artifact specifies one, and per TE §18.3 stage 3.5 must
stop and report rather than pick a default.

**FU-2 is moot** and marked so: it existed only to locate the ledger Q6=D required. Its closing
clause — *"raise the required change request rather than modifying approved artifacts
silently"* — was honoured in reverse when the ledger was **removed**: this stage reported both
upstream sites rather than editing them, and edited only after you authorised it explicitly.

**What D′ gives up, stated as a capability rather than a gap.** Release labels can no longer be
**ordered**. A reviewer citing two labels at a human-reviewed gate cannot tell from the labels
alone which release came first; sequence is read from the run record or the experiment registry,
both of which carry timestamps and `run_id`. Nothing else in this design depended on label
ordering. Because the requirement itself changed, R-12 is **fully compliant with Q6=D′** — this
is no longer non-compliance against an answered question.

#### The two upstream artifacts — corrected, on your explicit authorisation

| Artifact | Correction | Preserved |
|---|---|---|
| `inception/units-generation/unit-of-work.md` § 1 `foundation` → `Owns` | `artifacts/registry/release_history.jsonl` struck, with the withdrawal reason and authority stated | full superseded entry, verbatim |
| `inception/application-design/services.md` § Run record and registry | *"Three artifacts, one authoritative"* → **"Two"**; ledger row removed | superseded row and opening line, verbatim |

**Containment verified rather than assumed:** a search across `construction/` found **no other
unit** referencing the ledger, `ReleaseLedgerEntry`, or *"Three artifacts, one authoritative"*,
so nothing further was orphaned by the removal. The 2026-08-24 note recording the ledger's
addition is left in place beneath the new one, as the dated record of that decision.

#### Counts — derived after every edit, not carried

| Figure | Value | Derivation |
|---|---|---|
| Requirements carried | **16** | ID list, `unit-of-work.md` § 1 |
| Untested | **2 of 16** | REQ-ENG-7, REQ-ENG-10 |
| Acceptance rows | **7** | TA-01, TA-02, TA-03, TA-10, TA-15, TA-22, TA-23 |
| §19 rows | **36** | held; **no TA-37/TA-38 added** — all three mentions are prohibitions |
| Rules | **17** | `grep -cE "^## R-[0-9]+" business-rules.md` |
| Workflows | **10** | `grep -cE "^## W-[0-9]+" business-logic-model.md` — W-7 lost a step, not its existence |
| Entities | **8 live** | 9 numbered sections − 1 withdrawn; § 8 kept in place so every by-number cross-reference still resolves |

The entity count is the **only** figure that moved, and it moved because you authorised the
reversal that moved it.

#### Staleness sweep — every representation, not every instance

Swept for the *claims* the reversal invalidated, not only for the strings it changed, because a
sweep keyed to a literal is what missed five sites on 2026-08-24. Live occurrences now **zero**
across all three artifacts for: *"not edited here"*, *"still name the ledger"*, *"irreducibly
unmet"*, *"Monotonicity — OPEN"*, *"uncovered, and not replaced"*, *"unresolved Q6=D
monotonicity"*, and *"all resolved 2026-08-24"* in the § Sources amendment summaries. Every
remaining match of those phrases sits inside a **preserved superseded quotation**, verified by
reading each one rather than trusting the count. Code fences balance in all three files.

#### Governance state

A **declined** · B **approved** (three fields, nine total) · C **declined as drafted**, its
2026-08-24 approval reversed · **Q6 = D′**, FU-2 moot · **G-09 unsigned** — nothing here
authorises creating a module · no release ledger and no `release_history.jsonl` created · no
scientific value decided · **no `## Review` section rewritten**, on any artifact: the two
residual defects inside `business-logic-model.md` § Review history were corrected by a dated
annotation box on the `GOV-2026-08-22-INC-01` Rec 7 precedent, with the reviewer's own sentences
and verdicts untouched.

#### Nothing carried to the stage gate as an open item

The third presentation listed four. All four are closed: monotonicity (by the Q6 re-answer),
FU-2's integrity test (discharged by three controls), the upstream contradiction (corrected),
and the two § Review residuals (annotated). **One reviewer iteration remains.** After this
confirmation the three artifacts are re-saved and the reviewer runs **iteration 2, the last of
the budget** — and it will be reviewing a design whose release-labelling mechanism, Q6 answer
and entity count all changed since iteration 1, not a lightly-edited version of what it saw.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: A fresh receipt is recorded, the three artifacts are re-saved, and the reviewer runs iteration 2. Q6 = D′ and the Amendment C reversal stand as executed, with the upstream corrections applied and no item carried forward.

- Request changes
   > **Impact**: No receipt is recorded and nothing is re-saved. Tell me what to change — including reinstating Amendment C, restoring Q6 = D, reverting either upstream edit, or any individual remediation — and I re-present before touching anything.

> **💡 Recommendation**: **Looks correct** — every defect is resolved rather than deferred, the two items needing your authority were put to you before being applied, the one capability the design gives up is disclosed rather than absorbed, and every count was derived after the edits instead of carried across them.

[Answer]: Looks correct
