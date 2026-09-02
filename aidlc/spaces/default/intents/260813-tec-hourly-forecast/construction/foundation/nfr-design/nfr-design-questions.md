# NFR Design — Questions — `foundation`

**Unit** `foundation` (Bolt 1) · **Kind** `library` · **Stage** `nfr-design`

Two artifacts only — `security-design.md` and `logical-components.md`. `produces_kinds`
maps `performance-design`, `scalability-design` and `reliability-design` to
`[service]` / `[service, ui]`, and this unit is `library`.

**Nothing below decides a scientific value.** TE §18.2's absolute rule stands, and
§18.3's stop-and-report obligation is the reason Question 2 exists as a question rather
than as a design decision I made.

**What is already fixed upstream and is not re-asked.** The secret-scan **scope** is
TE §10's full width — history, configurations, logs, artifacts (SEC-F-01, Q1 = A at
`nfr-requirements`). Credentials come from a **platform secret store or environment
configuration excluded from version control**, resolved through **one interface** that
never branches on platform (SEC-F-03). The registry is **append-safe and atomic** with a
**closed status vocabulary** validated at write time, `exploratory` derived in the writer
and never passed by a caller, and writes that **never read the run history** (SEC-F-05).
Release identity is the **content hash**; `dataset_version` is its first 12 hex
characters with a verify-on-write uniqueness check (**D-29**). The restricted root is
**unreachable from this unit** (SEC-F-04).

---

## Question 1

SEC-F-01 states TA-22's acceptance as a **history-inclusive** secret scan over history,
configurations, logs and artifacts, with the tooling *"to be selected — `gitleaks`,
`trufflehog` or equivalent, pinned"*. **The tool is not selected, and neither is where it
runs.** `team.md` records that this project uses **no CI service**: the affirmed practice
is a git pre-commit/pre-push hook for the critical test set, plus a full local run before
every governed run and freeze gate.

That matters here because a history scan is not like a test. It is slow, it grows with
the repository, and its result is a property of a **commit range**, not of a working tree.

Where should the history-inclusive scan run?

A. **At the freeze gates only** — the scan runs before each governed run and each freeze gate (G-05, G-06, phase transitions), over the **full history to that commit**, and its report plus tool version and commit range is captured in that run's evidence record
   > **Impact**: Matches `team.md`'s existing gate-test practice exactly, and puts the evidence where TA-22 needs it — attached to a gate, with a commit range. A credential committed between gates stays in history undetected until the next gate, which for a single-author thesis codebase may be days. The scan cost is paid rarely, so full-history depth stays affordable.

B. **On every commit, via the existing pre-commit hook** — the scan runs incrementally on the staged diff, with a full-history scan still required at each freeze gate
   > **Impact**: Catches a credential **before** it enters history, which is the only point at which the fix is cheap rather than a history rewrite. Two scan modes to configure and keep consistent. The incremental scan proves nothing about history, so it supplements the gate scan rather than replacing it — B is A plus a cheap early net.

C. **Manually, when someone remembers** — no hook, no gate wiring; the scan is run and recorded before G-05
   > **Impact**: Nothing to build now. It makes TA-22 depend on a person remembering at exactly the moment they are busiest, and `team.md` already records that this is a single-author codebase with no reviewer to catch the omission. The obligation would be satisfiable in principle and unmet in practice.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B — the two modes answer two different questions, and only the cheap one is capable of preventing the expensive failure. A credential that reaches history requires a history rewrite to remove, which for a thesis repository with tagged freeze gates means rewriting tagged commits; catching it at `git commit` costs a second. The gate scan still carries TA-22's evidence, so B does not weaken A, it adds to it. The honest cost: two configurations to keep in step, and the pre-commit scan will occasionally fire on a false positive in a test fixture, which is the standard friction of this class of tool.

[Answer]: B

---

## Question 2

**This one is a TE §18.3 stop-and-report point, routed to you rather than decided.**

D-29 fixes `dataset_version` as the first 12 hex characters of the release's
`content_hash`, with a **verify-on-write uniqueness check**. That check must read back the
**existing release population** — and SEC-F-06 records that **where that population lives
and how it is enumerated is not settled**. The release-history ledger that would have
answered it was **declined as drafted at Amendment C**, and `ReleaseLedgerEntry` was
withdrawn with it. So `write_release` cannot perform D-29's check today: the mechanism is
specified and not implementable.

`functional-design` § Assumptions names three candidate surfaces and chooses none. An
agent may not pick one by convenience — but you may decide.

A. **A release-root directory scan** — enumerate the release directories under the release root and read each one's recorded `content_hash`
   > **Impact**: No new artifact and no schema change; the releases themselves are the register, so the check cannot disagree with reality. It requires the release root to be reachable and complete wherever `write_release` runs — which across **two platforms** with different filesystem semantics is exactly the assumption that has bitten this project before. It also gets slower as releases accumulate, though at thesis scale that is negligible.

B. **The experiment registry's release columns** — enumerate from the registry rows that already carry `dataset_version` and `artifact_manifest_path`
   > **Impact**: Reuses a structure that is already append-safe, atomic and schema-asserted, and that already exists in the design. But it makes release uniqueness depend on the **registry** being complete — and a release written by a path that failed to register, or written before the registry existed, would be invisible to the check. It also couples two subsystems that SEC-F-04's one-way boundaries otherwise keep apart.

C. **A narrower re-proposal of the declined ledger** — a minimal append-only file recording only `content_hash` and `dataset_version` per release
   > **Impact**: Purpose-built, cheap to read, and answers exactly the question D-29 asks. It reopens something the owner **already declined**, and `project.md` records that reopening a recorded refusal needs a new argument or an explicit decision — this would be the explicit decision, but it should be made deliberately rather than by inheriting the old draft's shape. It also adds a third thing that can disagree with the other two.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A, with a stated limit — the releases are the only surface that cannot disagree with itself, because it *is* the population. B's failure mode is the dangerous one: a missing registry row silently turns a collision check into a no-op, and D-29's whole purpose is injectivity. C is defensible but should not be chosen merely because it is convenient now, given the refusal on record. **The limit A must carry:** the check is only as complete as the release root the writing process can see, so a cross-platform release population needs its enumeration to be over a single authoritative root, not whichever root the current session resolved. If you would rather not settle this at design time, say so and I will record it as an owner decision still open and have the design refuse rather than assume.

[Answer]: A

---

## Question 3

SEC-F-05 carries a **measurement obligation this stage cannot discharge**: W-6 step 8's
durability confirmation reuses `governance-guards` R-25's pattern, but **Kaggle's
durability semantics are characterised nowhere in this design**, and rows written inside
a Kaggle session need measured evidence before they are relied on at a freeze gate.

The design has to say what the registry writer **does today**, while that measurement
does not exist.

A. **Fail-closed on the unmeasured platform** — a registry write inside a Kaggle session refuses to report success until the durability confirmation it performs has been characterised, so a governed Kaggle run cannot silently rely on an unproven write
   > **Impact**: Nothing false is ever recorded as durable, and the gap becomes visible the first time someone runs a governed job on Kaggle rather than at the gate where it matters. It **blocks governed Kaggle runs until the measurement is done** — and Kaggle is the project's primary compute, so this is a real schedule cost, not a theoretical one.

B. **Write, and stamp the row with the durability status** — the write proceeds; the row records that its durability is **unverified on this platform**, and the freeze gate refuses to accept a row so stamped as evidence
   > **Impact**: Keeps work moving while making the unmeasured claim travel **with the data** rather than living in a design document nobody reads at 2am. The refusal lands at the gate, where the consequence belongs. The risk: a stamped row is easy to accumulate and easy to normalise, and the gate refusal has to actually exist for the stamp to mean anything.

C. **Proceed and record the obligation in the design only** — the writer behaves identically on both platforms; the measurement is tracked as an open item
   > **Impact**: Simplest, and matches what the code would do anyway today. It also means nothing in the running system knows the difference, so the obligation is discharged by memory alone — and this stage has already recorded that an obligation with no mechanism is one a reviewer finds later, not one the pipeline enforces.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B — it is the same shape this project already chose for `inventory-and-registry`'s audit blindness and for the two-half cross-unit contracts: make the limitation a **machine-carried field** rather than prose, and put the refusal at the gate that consumes it. A is more rigorous but stops the primary compute platform to buy rigour the project can obtain by measurement instead; C leaves nothing enforcing anything. B's honest weakness is that it depends on the gate-side refusal being built, which makes that refusal part of this design rather than an assumption about someone else's.

[Answer]: B

---

## Question 4

`logical-components.md` asks for component boundaries, failure domains and blast radius.
`foundation` currently holds six responsibilities: **config loading and hashing**,
**platform and root resolution**, **credential resolution**, **seeding and the environment
lock**, **the experiment registry writer**, and **release writing**.

Two of those are unlike the rest. The **registry writer** and the **release writer** both
perform integrity-critical, append-only writes whose failure modes are exactly what
SEC-F-05 and SEC-F-06 govern; the other four are read-and-resolve.

How should the component boundary be drawn?

A. **Split on write-integrity** — group the four read-and-resolve responsibilities as one component, and give the registry writer and the release writer their own boundaries, each with its own failure domain
   > **Impact**: Puts a boundary exactly where the blast radius differs: a bad config read fails a run, a bad registry or release write corrupts the permanent record. It makes the two integrity-critical paths separately testable and separately reviewable, which is what TA-10, TA-21 and TA-15 will each need. Three components in a unit that a reader might expect to be one.

B. **One component per responsibility** — six boundaries, one each
   > **Impact**: Maximum isolation and the clearest mapping to the six `src/` modules TE §12 mandates. It also implies six sets of boundary contracts for a unit whose whole job is to be the shared foundation the other eleven units import, and over-decomposition here would push coupling into the callers rather than removing it.

C. **One component** — `foundation` is a single logical component with internal structure
   > **Impact**: Matches how callers actually experience it: one library they import. It makes the blast-radius section nearly contentless, which for the unit that owns the permanent record is the wrong place to have nothing to say.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the boundary that matters is the one between "this run fails" and "the permanent record is wrong", and that boundary runs between the resolve responsibilities and the two writers, not between the six modules. B's six boundaries are a file listing rather than a failure analysis; C has nothing to say about the failure that actually matters. A also lines up with the three separate acceptance rows already pointed at these paths.

[Answer]: A

---

## Consolidated Summary Confirmation

Confirm this reading before the two artifacts are written. **Nothing below decides a
scientific value**, and nothing claims a gate, acceptance row, install or test as
discharged.

**How these answers were given.** The owner directed *"Apply your recommendations"* —
so all four are the recommended options, adopted as an **explicit owner decision**, not
as agent defaults. That distinction matters most for **Q2**, which is a TE §18.3
stop-and-report point: an agent may not pick an unresolved mechanism by convenience, and
the owner may decide. This is recorded as the owner deciding.

**Scope.** Two artifacts — `security-design.md` and `logical-components.md`.
`produces_kinds` excludes `performance-design`, `scalability-design` and
`reliability-design` for a `library` unit. Those three categories were **assessed** at
`nfr-requirements` and found to have no latency target, no load projection, and exactly
two execution environments with one user; the design does not manufacture service-shaped
content to fill them.

**Q1 = B — the secret scan runs in two modes.** An **incremental scan on the staged diff
at every commit**, via the pre-commit hook `team.md` already establishes, **plus** a
**full-history scan** over history, configurations, logs and artifacts before each
governed run and each freeze gate, whose report, **tool version and commit range** are
captured in that run's evidence record. The two answer different questions and neither
replaces the other: the incremental scan **proves nothing about history**, and the gate
scan is what carries TA-22's evidence. Rationale for the pair: a credential that reaches
history requires a history rewrite to remove, and this repository **tags its freeze
gates**, so that rewrite would rewrite tagged commits. Accepted cost, stated: two
configurations to keep in step, and periodic false positives on test fixtures.
**The tool is still not selected** — `gitleaks`, `trufflehog` or equivalent, **pinned** —
and selecting it is not this stage's act.

**Q2 = A — the release population is enumerated by scanning the release root.**
`write_release` reads back each release directory's recorded `content_hash` to perform
**D-29**'s verify-on-write uniqueness check. Chosen because the releases **are** the
population, so the check cannot disagree with reality. **B was rejected on its failure
mode**: a release written by a path that failed to register would be invisible, silently
turning a collision check into a no-op, which defeats D-29's purpose. **C was rejected
because it reopens a refusal already on record** (the ledger declined as drafted at
Amendment C).

> **The limit this choice must carry, stated in the design and not only here.** The check
> is only as complete as the release root the writing process can see. Across **two
> platforms** with different filesystem semantics, enumeration must be over a **single
> authoritative root**, never whichever root the current session happened to resolve. A
> `write_release` that cannot reach that root **refuses** rather than treating an
> unreachable population as an empty one — an empty population makes every hash unique.

> **Owed, and not performed here: this decision should carry a D-number.** It settles a
> mechanism that a governing document left open at a stop-and-report point, and
> `team.md`'s linking rule makes `evidence/DECISIONS.md` authoritative for exactly this
> class of decision. Recording it there is the student's act; this stage records that it
> is owed.

**Q3 = B — the registry write proceeds and stamps its durability status.** A row written
where durability semantics are uncharacterised records that its durability is
**unverified on this platform**, and **the freeze gate refuses to accept a so-stamped row
as evidence**. The limitation travels as a **machine-carried field** rather than as prose,
matching the shape this project already uses for `inventory-and-registry`'s audit
blindness and for its two-half cross-unit contracts. **The gate-side refusal is part of
this design**, not an assumption about someone else's — a stamp with no refusal behind it
is decoration. **Kaggle's durability is still unmeasured**; W-6 step 8 needs its own
measured evidence, and this design does not supply it.

**Q4 = A — the component boundary is drawn on write-integrity.** Three components: the
four **read-and-resolve** responsibilities (config loading and hashing, platform and root
resolution, credential resolution, seeding and the environment lock) as one; the
**experiment registry writer** as its own; the **release writer** as its own. The boundary
sits where blast radius differs — a bad config read **fails a run**, a bad registry or
release write **corrupts the permanent record** — and it lines up with **TA-10**, **TA-21**
and **TA-15** as three separate acceptance rows.

**Carried from upstream, not re-decided.** The secret-scan **scope** is TE §10's full
width (SEC-F-01). Credentials come from a platform secret store or environment
configuration excluded from version control, through **one interface that never branches
on platform**, which reads, returns, logs, serializes, interpolates and persists **no
credential value** (SEC-F-03, R-14). The registry is append-safe and atomic, its status
vocabulary closed and validated at write time, `exploratory` **derived in the writer and
never passed by a caller**, writes **never reading the run history** (SEC-F-05).
`AccessRecord`/`RegistryEvent` orphan detection runs **both ways**, and the known
pre-guard orphans are **never back-filled away**. Release directories are **never
overwritten**; identity is the content hash and the label is not authoritative
(SEC-F-06). The restricted root is **unreachable from this unit** (SEC-F-04).

**Status claims made. None.** **TA-22 remains `Pending` and NFR-SEC-01 unclaimed** —
the history, configuration, log and artifact limbs have **not been scanned**, and
SEC-F-02's acquisition identity-block exception is **unresolved**. **TA-15 is NOT
covered**: `tests/test_release_hashes.py` exercises none of §13.3's manifest fields and
does not exercise R-13's overwrite refusal. **TA-10 and TA-21 are `Pending`**; the
registry tests are unwritten. `src/data/config.py`, `src/data/release.py`,
`src/data/reuse_registry.py` and `tests/test_determinism.py` **do not exist** — BLK-01
granted authority to name a module, which is not authority to have written one. **WS-18
and TA-18 are not discharged.** **G-09 is signed (D-31) with its own preconditions
UNMET**; **stage 3.1 remains FAIL**; `configs/` does not exist; **no Python interpreter
exists in this environment**, so every test is written-but-unexecuted or unwritten.
`foundation`'s **TensorFlow pin stays `TBD — freeze gate`**.

Reply `Looks correct` to proceed, or state what to change.

[Answer]: Looks correct
