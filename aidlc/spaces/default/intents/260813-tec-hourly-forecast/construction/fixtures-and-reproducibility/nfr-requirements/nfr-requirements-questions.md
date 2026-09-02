# NFR Requirements — Questions — `fixtures-and-reproducibility`

**Unit** `fixtures-and-reproducibility` (Bolt 12) · **Kind** `library` · **Stage** `nfr-requirements`

Two artifacts only — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit.

**Requirement set derived against `requirements.md` across both families before writing.** The
map carries **8 requirements, 2 without a §16/§19 row** — with rows: **FR-WS-1** (WS-20, TA-09
primary), **FR-WS-4** (WS-01, WS-09…WS-20 — **13 rows**), **FR-WS-5** (WS-20, TA-17 primary),
**FR-WS-6** (TA-03, TA-26 supporting), **NFR-REP-01** (WS-20, TA-17 primary), **REQ-NFR-A3**
(TA-03 supporting); without: **FR-WS-2** and **FR-WS-3**, covered by R-136's controls (13) and
(14) meanwhile. The design additionally names **FR-WS-7** (context — `foundation`'s §18.3
preflight requirement), **FR-P1-03-5**, **REQ-ENG-4**, **REQ-ENG-5**, **REQ-ENG-10** and
**NFR-PHASE-01**; all are cited. *(The NFR family was set-differenced separately against
`requirements.md`'s eleven NFR IDs — on `statistical-inference` a design-file grep came back
clean on both FR families and still missed NFR-REP-01.)*

**Not re-asked, because `functional-design` already decided them.** One manifest schema, **one
validating loader, and the loader as the only read path** (R-133, W-1); **measure then freeze**
with two manifest states, identity by citation and **no silent update** (R-134, W-2); the
plumbing fixture's identity cited, **one-station scope enforced**, with **DATA-07 and the
December-representativeness prohibition travelling as freight** (R-135, W-3); the plumbing
fixture **never evidence**, December excluded **on record dates** (R-136, W-4); fixture
partitions as **apparatus constants in a quarantined id space** (R-137, W-5); the clean run
executing the **amended §13.2 sequence verbatim — seven Phase 1 invocations, Phase 2 deferred to
G-P2 — on CPU with no GPU visible** (R-138, W-6); the **comparison ledger** with `exact` where
§13.7 demands it and **no expectation ever updated** (R-139); **fixture-pass receipts and the
exported two-receipt check** (R-140, W-7); the **Kaggle in-session gate as a producing path**
(R-141, W-8); the three evidence artifacts as **generated paths that refuse** (R-142, W-9).

**Carried, not decided here.** **The two manifest freeze acts — promoting measured values from
`candidate` to `frozen` — are the project owner's under Q-31**, and nothing here performs them.
**Neither fixture has ever run**, so **no measured value exists**.

---

## Question 1

R-141 makes the Kaggle in-session gate a **producing path**: before any governed Kaggle run,
the critical test set and **both fixtures** execute **in-session** and emit a machine-readable
gate result carrying the resolved platform, the §13.1 environment-lock items, timestamps,
per-test and per-fixture results, and its **own measured total runtime**. A governed run whose
evidence record **lacks** one — or carries one stamped `local` — **fails before domain work**.

`functional-design`'s coverage map refers to *"the platform stamp and **the staleness bound**"*.
The platform stamp is fully specified. **The staleness bound is not stated anywhere I can find**:
nothing says whether a gate result produced earlier **in the same session** may be reused by a
later governed run in that session, or under what condition it goes stale.

This matters because R-141 stacks the critical set **and both fixtures** ahead of the governed
work — an expensive precondition that there is an obvious incentive to run once and reuse.

What should `security-requirements.md` require?

A. **Bind the gate result to the run's own environment lock**: a governed run may reuse an in-session gate result **only if** its §13.1 lock items — code commit, the four config snapshot hashes, the `requirements.txt` hash and `pip freeze`, platform — are **identical** to those the gate recorded; **any difference makes it stale and the gate re-runs**
   > **Impact**: Makes staleness a **derived fact** rather than a time window, so a config edit or a re-install between the gate and the run invalidates it automatically. It permits reuse within one unchanged session, which is what makes the expensive precondition tolerable. It cannot detect a change the lock items do not cover.

B. **One gate per governed run, no reuse** — every governed run re-executes the critical set and both fixtures
   > **Impact**: Simplest and strongest: no staleness question can arise. It re-runs both fixtures ahead of every governed run, which on a full-year job means the complete fixture ladder every time, and creates a strong incentive to batch governed work in ways the protocol did not intend.

C. **A time-based bound** — a gate result is valid for a stated number of hours within its session
   > **Impact**: Familiar and easy to implement. Time is a **proxy for change**, and the thing that actually invalidates a gate is a changed environment, not elapsed minutes — a config edited one minute after the gate would pass, and an untouched session would fail after the window.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the gate exists to prove the environment the governed run executes in was tested, so the correct invalidator is **a change to that environment**, which the §13.1 lock already enumerates. Its limit should be stated: it cannot see a change the lock items do not cover, so it is only as good as the lock's completeness. Option C would let a real change pass and a non-change fail.

[Answer]: A

---

## Question 2

R-139 states the rule that makes reproducibility testing meaningful: a mismatch in an
`exact`-class artifact **raises**, naming file and violated expectation, and **never updates the
expectation**. R-134 adds **no silent update** to the manifest, with **identity by citation**.

Both are **rules**. Neither is a **mechanism**. The failure they describe — a frozen expectation
edited to match what the run actually produced — is committed by a person editing a YAML file,
and this project's own evidence shows the shape is real: **D-18's re-merge hashed differently
from an artifact holding the identical record set** because output order followed directory
traversal, and only a sort on the dedup key made two runs agree. That is precisely the moment
someone would be tempted to update the expectation instead.

**The freeze act itself is the project owner's under Q-31**, so this unit cannot own the
decision — but it can own whether an edit is **detectable**.

What should the artifacts require?

A. **Hash-protect the frozen manifest**: the frozen values carry a manifest hash recorded outside the manifest, and the loader **refuses a manifest whose hash does not match** the recorded one — so an edited expectation fails to load rather than silently becoming the new truth
   > **Impact**: Turns "no silent update" from a rule into a mechanism, at the one place — R-133's **single validating loader, the only read path** — where every read already passes. It needs somewhere outside the manifest to record the hash, and a legitimate re-freeze then requires a deliberate two-step act, which is the intended friction.

B. Keep it procedural, and record that detection rests on **git history and review**
   > **Impact**: No new mechanism, and the edit is genuinely visible in a diff to anyone who looks. It depends on someone looking at the right commit, and `team.md` records this project as a single-author codebase with no pull-request review — so "review" here means the author reviewing their own edit.

C. Require the loader to **warn** on a manifest whose hash differs, without refusing
   > **Impact**: Surfaces the change without blocking a legitimate re-freeze. A warning in a test-apparatus load path is the kind of output that is read once and then filtered, and it would fire on every legitimate freeze too — training everyone to ignore it.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — R-133 already establishes **one validating loader as the only read path**, so the check has a natural home and costs one comparison. The friction is the point: a re-freeze should be deliberate, and Q-31 makes it an owner act anyway. Option B's weakness is specific to this project rather than general — a single-author codebase with no PR review means the diff is reviewed by the person who wrote it, at the moment they most want the expectation to change.

[Answer]: A

---

## Consolidated Summary Confirmation

Confirm this reading before the two artifacts are written. Nothing below decides a
scientific value, and nothing claims a gate or acceptance row is discharged.

**Scope.** Two artifacts — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit.

**Requirement set derived against `requirements.md` across both families before writing.** The
map's **8 requirements, 2 without a row** — with rows **FR-WS-1**, **FR-WS-4**, **FR-WS-5**,
**FR-WS-6**, **NFR-REP-01**, **REQ-NFR-A3**; without **FR-WS-2** and **FR-WS-3**, covered by
R-136's controls (13) and (14) meanwhile — plus **FR-WS-7** (context, `foundation`'s),
**FR-P1-03-5**, **REQ-ENG-4**, **REQ-ENG-5**, **REQ-ENG-10** and **NFR-PHASE-01**, all cited.
**Every requirement whose text these artifacts reproduce is covered, whoever owns the row** —
the lesson from six consecutive units on which this check found a defect.

**Q1 = A — a gate result is bound to the run's own environment lock.** A governed Kaggle run
may reuse an in-session gate result **only if** its **§13.1 lock items** — code commit, the four
configuration snapshot hashes, the `requirements.txt` hash and per-run `pip freeze`, versions,
input dataset and manifest versions, platform, known nondeterministic operations — are
**identical** to those the gate recorded. **Any difference makes the result stale and the gate
re-runs.** Staleness becomes a **derived fact**, not a time window: the thing that invalidates a
gate is a **changed environment**, not elapsed minutes.

**Its limit is stated:** it **cannot see a change the lock items do not cover**, so it is only
as good as the lock's completeness. The platform stamp stays as designed — resolved from
`ConfigSnapshot.platform` by `foundation`'s detection, **never asserted by the caller** — and a
governed Kaggle run whose evidence record lacks a gate result, **or carries one stamped
`local`**, still **fails before domain work**.

**Q2 = A — the frozen manifest is hash-protected.** Frozen values carry a **manifest hash
recorded outside the manifest**, and **R-133's single validating loader — already the only read
path — refuses a manifest whose hash does not match**. This turns R-139's *"never updates the
expectation"* and R-134's *"no silent update"* from **rules into a mechanism**, at the one place
every read already passes.

**Why a mechanism and not review.** The failure is a person editing a YAML expectation to match
what a run produced — and **D-18's re-merge hashing differently from an artifact holding the
identical record set**, cured only by a sort on the dedup key, is exactly the moment that
temptation arrives. `team.md` records this as a **single-author codebase with no pull
requests**, so procedural detection means the author reviewing their own edit. **The friction is
intended:** a legitimate re-freeze becomes a deliberate two-step act, and **Q-31 makes the freeze
an owner act anyway**.

**Carried, not re-decided.** R-133's one schema, one validating loader, **loader as the only
read path**; R-134's **measure then freeze** with two states and identity by citation; R-135's
plumbing-fixture lineage with **DATA-07 and the December-representativeness prohibition
travelling as freight**; R-136's **plumbing fixture never evidence** and December excluded **on
record dates**; R-137's fixture partitions as **apparatus constants in a quarantined id space**;
R-138's **amended §13.2 sequence verbatim — seven Phase 1 invocations, Phase 2 deferred to
G-P2 — on CPU with no GPU visible**; R-139's comparison ledger with **`exact` where §13.7
demands it**; R-140's **two-receipt exported check**; R-141's in-session gate as a producing
path; R-142's three evidence artifacts as **generated paths that refuse**.

**Status claims made.** None. **Neither fixture has ever run**, so **no measured value exists**
and every runtime, tolerance and range in this design is a **placeholder**. **The two manifest
freeze acts are the project owner's under Q-31** and nothing here performs them. **FR-WS-2 and
FR-WS-3 have no acceptance row.** **WS-20, TA-09, TA-17, TA-03 and TA-26 are undischarged**;
**WS-01 plus WS-09…WS-20 is a 13-row bounded set**, not a discharged one. **BLK-08 ↓ is checked
here rather than inherited silently.** G-09 is signed (D-31) with preconditions UNMET; stage 3.1
remains FAIL; `configs/` does not exist; no Python interpreter exists here.

Reply `Looks correct` to proceed, or state what to change.

[Answer]: Looks correct
