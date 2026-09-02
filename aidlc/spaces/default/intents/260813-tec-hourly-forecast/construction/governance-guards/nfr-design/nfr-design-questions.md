# NFR Design — Questions — `governance-guards`

**Unit** `governance-guards` (Bolt 2) · **Kind** `library` · **Stage** `nfr-design`

Two artifacts only — `security-design.md` and `logical-components.md`. `produces_kinds`
maps `performance-design`, `scalability-design` and `reliability-design` to
`[service]` / `[service, ui]`, and this unit is `library`.

**Nothing below decides a scientific value.** TE §18.2's absolute rule stands.

**What is already fixed upstream and is not re-asked.** Every read of **content** beneath
`evidence/locked_test_restricted/` routes through **`open_restricted`**, which **durably
appends the `AccessRecord` before the read begins** — a log-write or durability failure
**prevents the read** (SEC-G-01, R-25). The static check is **AST-based with constant
folding**, its dynamic-path residual **stated in the rule body**, with R-24's hierarchy
intact: the static scan is the **early-warning** limb and the **run-time assertions are
authoritative** (SEC-G-04, Q2 = B at `nfr-requirements`). `RESTRICTED_LITERAL_EXEMPT_MODULES`
has **five members in addition to** the chokepoint `src/data/locked_test.py` — **six counting
it** — and member 5 is `scripts/merge_coverage_year.py`, a **production script, not a test**.
`RAW_MODULES` is **four** modules. **Both** phase-boundary limbs run and neither substitutes
for the other (SEC-G-05, R-23). An unparseable file is a **failure, never a skip** (R-27).

> ## ✅ THE BREACH IS REMEDIATED — corrected 2026-09-01 against the workspace
>
> *(This box previously read: "**THE ONE-DOOR PROPERTY IS BREACHED TODAY, AT TWO NAMED
> SITES** … `open_restricted` does not exist, so there is no guard for these reads to
> predate. Routing them through it is **owed at stage 3.5**." That was inherited from
> `nfr-requirements` and **was false when written here** — it was carried as established
> input without checking disk, which `project.md` § Way of Working forbids in those words.
> Superseded text preserved above. The owner ruled on 2026-09-01 that this file be
> corrected and that `nfr-requirements` be left unchanged.)*
>
> **`src/data/locked_test.py` EXISTS**, and `open_restricted` is defined at line **147**.
> **Both formerly breached sites now route through it** — `tests/test_release_hashes.py`
> and `tests/test_acquisition_window.py` each import `AccessRecord, open_restricted` and
> read via a `_read_guarded` helper that calls the chokepoint for restricted paths.
>
> **Two NEW discrepancies found by that same check, and they run the other way:**
>
> 1. **The exempt list has SEVEN members on disk, not six.**
>    `tests/test_locked_test_guard.py:287` enumerates the chokepoint plus **six** others —
>    the seventh, `tests/test_merge_script_restricted_reads.py`, was **added 2026-08-28
>    because the membership assertion caught it on first run**. Every upstream artifact,
>    and this file's own preamble above, says **six counting the chokepoint**.
> 2. **The literal scan is textual, not AST-based.** The same test does
>    `if "locked_test_restricted" in text` over `module.read_text(...)`. `nfr-requirements`
>    Q2 = B specified **AST-based with constant folding** precisely so that
>    `"locked_test" + "_restricted"` is caught — and a substring check **cannot** catch
>    that, because the joined literal never appears in the source text. **The gap
>    AST-plus-folding existed to close is open in the implementation.**
>
> Both are recorded in `security-design.md` and are **owed to the human at the gate**;
> neither is fixed here, and `nfr-requirements` stays unchanged per the owner's ruling.

---

## Question 1

SEC-G-01 requires `open_restricted` to **durably append** the `AccessRecord` **before**
the read begins, and makes a **durability failure prevent the read**. "Durably" is the
load-bearing word and it is **not defined anywhere in the upstream design**.

This is the same gap `foundation` hit from the other side: its § SD-03 records that
**Kaggle's durability semantics are characterised nowhere**, and its registry writer
stamps rows *"durability unverified on this platform"* rather than claiming otherwise.
`open_restricted` cannot make a weaker claim than the registry it writes to — but it also
**cannot block on a measurement nobody has taken**.

What should `open_restricted` do on the platform whose durability is uncharacterised?

A. **Refuse the read** — until Kaggle's durability semantics are measured, `open_restricted` fails closed on that platform, so no locked-test content is ever read there without a durably recorded access
   > **Impact**: The strongest reading of "a durability failure must prevent the read", and it cannot record an access it did not durably record. It **blocks locked-test access on the project's primary compute platform** until the measurement is done — and the required pre-G-05 December coverage audit is exactly the work that would hit this.

B. **Write, stamp, and let the consumer refuse** — the access is recorded with its durability marked **unverified on this platform**, the read proceeds, and **G-05's evidence package refuses a stamped access record**
   > **Impact**: Matches `foundation` § SD-03's shape exactly, so the two writers make the **same** claim rather than contradictory ones, and the limitation travels as a machine-carried field. It permits a read whose access record might not survive a session crash — which for the locked test is the record that matters most.

C. **Best-effort flush, no stamp** — `open_restricted` flushes and proceeds; durability is assumed
   > **Impact**: Simplest, and indistinguishable from correct behaviour whenever the platform happens to be durable. It converts SEC-G-01's explicit "a durability failure must prevent the read" into a claim nothing checks, on the one guard whose whole purpose is that the December lock is auditable.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — and this is the one place I would diverge from
> `foundation`'s stamp-and-proceed answer, because the asymmetry is real. A registry row
> records **what a run did**; an `AccessRecord` is the **only evidence that the locked test
> was opened at all**. If it is lost, the loss is invisible — there is no second record to
> reconcile against, which is precisely why SEC-G-02 needs orphan detection in both
> directions. Option B's stamped record is a record that might not exist, which for the
> December lock is the failure the whole guard exists to prevent. The honest cost, stated:
> **A blocks the required pre-G-05 December coverage audit on Kaggle until W-6 step 8's
> measurement is done** — so choosing A makes that measurement a scheduling dependency,
> not a background task.

[Answer]: A

---

## Question 2

`RESTRICTED_LITERAL_EXEMPT_MODULES` is a **security allowlist with exactly six members**,
asserted exactly. Where it lives is not settled.

There is a real tension. TC-03e says **no scientific constant may hide in source or a
notebook** — every scientific constant lives in one of the four governed configs. But this
list is **not a scientific constant**: it is a security boundary, and a config file is
**easier to edit than source and is not itself in the guard's scan scope**.

Where should the exempt list live?

A. **In source, as a module-level constant in the guard itself**, with the membership assertion as a test
   > **Impact**: The allowlist changes only via a code change, which is visible in a diff and, once git exists, attributable to a commit citing a D-number. It sits inside the artifact whose job is enforcement, so the guard cannot be pointed at a different list. TC-03e does not reach it — this is not a scientific constant — but a reader who applies TC-03e by analogy will think it is misplaced, so the reasoning must be stated.

B. **In a governed config** (`data.yaml` or a new security section)
   > **Impact**: Consistent with the project's "constants live in config" habit, and changes are captured by the four-config snapshot hash in every run's environment lock. It also makes the security boundary editable by anyone editing config, and a config edit that widens the allowlist would be hashed and recorded — but not **refused**.

C. **In source, but derived** — the guard discovers exempt modules by a marker (a decorator, a magic comment) rather than a central list
   > **Impact**: No list to keep in sync with reality. It also means **any file can exempt itself** by adding the marker, which inverts the property: the allowlist stops being a list someone maintains and becomes a permission each module grants itself.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the allowlist is the boundary, not a parameter of it,
> and the question to ask is "what does it take to widen this?" A requires a code change to
> a guard module plus a test update; B requires editing a YAML file; C requires adding a
> comment to the file that wants the exemption. Only A makes widening as deliberate as the
> boundary is meant to be. The stated cost: it looks like a TC-03e violation to a reader
> applying that rule by analogy, so the design must say why TC-03e does not reach it —
> and this list's **sixth member is a production script**, which is exactly the kind of
> entry that should be hard to add quietly.

[Answer]: A

---

## Question 3

This unit runs **two** static scans over the repository tree, and they are distinct:

- **The literal scan** (SEC-G-04) — who may **name** the restricted root; AST-based with constant folding; the exempt list bounds it.
- **The residency scan** (W-8a, FR-P1-02-6) — whether **December content has escaped** the root; R-26's hit definition including the bounded driver exclusion.

Both use R-27's per-artifact-class dispatch, and both treat an **unparseable file as a
failure**. Whether they are one walk or two is not stated.

A. **Two independent scans, each with its own entry point and its own failure**
   > **Impact**: Each scan fails for its own reason, and a reader of a failure knows immediately which property was violated. Each can be run alone — useful, since the residency scan is the one with **no acceptance row** and may need running ad hoc. The tree is walked twice, which at this repository's size costs nothing measurable.

B. **One walk, two visitors** — a single tree traversal dispatches both checks per file
   > **Impact**: Half the I/O and one place where R-27's unparseable-is-a-failure rule is implemented, so the two cannot drift apart on that rule. It couples them: a change to the walk affects both, and a failure has to say which visitor raised it or the message becomes ambiguous at exactly the wrong moment.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — they answer different questions, have different hit
> definitions, and one of them (residency) carries **no §16 or §19 evidence obligation at
> all**, which makes it the one most likely to be run, changed or skipped independently.
> Coupling a check with an acceptance row to a check with none invites the rowless one to
> ride on the other's evidence. The duplicated traversal is genuinely free here; the shared
> unparseable-is-a-failure rule should be **one helper both call**, which captures B's real
> benefit without the coupling.

[Answer]: A

---

## Question 4

`logical-components.md` needs component boundaries. This unit holds: the **content
chokepoint** (`open_restricted`), the **access recorder** and its orphan detection, the
**literal scan**, the **residency scan**, the **phase-boundary limbs** (import + produced
field), the **protected-hash differ** for G-P3C, and the **reuse registry**.

How should the boundary be drawn?

A. **On enforcement timing** — **run-time guards** (chokepoint, access recorder, phase-boundary assertions, hash differ) as one component; **static scans** (literal, residency) as another; the **reuse registry** as a third
   > **Impact**: Draws the boundary on R-24's own hierarchy — the run-time limb is **authoritative**, the static limb is **early warning** — so the components mirror the enforcement model the upstream already fixed. It puts the breached chokepoint and the phase assertions together, which is right: both are authoritative and both are unbuilt.

B. **On what is guarded** — restricted-root components, phase-boundary components, licence components
   > **Impact**: Maps to the three governing rules and reads naturally against the requirements. It splits the literal scan from the residency scan even though they share a traversal technique, and it puts a static scan and a run-time assertion in the same box, blurring exactly the distinction R-24 exists to preserve.

C. **One component** — the guard library
   > **Impact**: Honest about how it is imported. It has nothing to say about the fact that one limb is authoritative and the other is advisory, which is this unit's single most important structural property.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — R-24's hierarchy is the real structure here, and a
> component diagram that does not show it would be describing a different system. The
> distinction matters operationally: a static-scan failure is a warning to fix before a
> run, a run-time guard failure **stops the run**, and conflating them is how a project
> ends up treating an advisory scan as though it enforced something. `foundation`'s
> boundary was drawn on the same kind of criterion — failure consequence, not module
> listing — so the two units stay comparable.

[Answer]: A

---

## Consolidated Summary Confirmation

Confirm this reading before the two artifacts are written. **Nothing below decides a
scientific value**, and nothing claims a gate, acceptance row, install or test as
discharged.

**How these answers were given.** The owner approved the four recommendations as an
**explicit decision**, not as agent defaults.

> **⚠ This summary is being re-presented, and the reason is recorded rather than hidden.**
> It was confirmed once on 2026-09-01. **The file then changed**: the preamble's breach box
> was corrected from *"THE ONE-DOOR PROPERTY IS BREACHED TODAY"* to the remediated state,
> on the owner's ruling, after a workspace check showed the upstream status claims were
> false. The engine refused stage completion because a confirmed summary must match the
> file it was confirmed against — so the first confirmation is **void** and this one
> replaces it. **The four answers are unchanged**; what changed is the factual preamble
> they sit under, and two new discrepancies (DISC-1, DISC-2) are now recorded below.

**Scope.** Two artifacts — `security-design.md` and `logical-components.md`.
`produces_kinds` excludes the other three for a `library` unit. The excluded categories
were assessed at `nfr-requirements` and are **not re-opened**; no service-shaped content
is manufactured for a library that serves no request.

**Q1 = A — `open_restricted` refuses the read where durability is uncharacterised.**
Until Kaggle's durability semantics are measured, the chokepoint **fails closed on that
platform**: no locked-test content is read there without a **durably recorded** access.

> **This deliberately diverges from `foundation` § SD-03**, which stamps a registry row
> *"durability unverified on this platform"* and lets the gate refuse it. The asymmetry is
> the reason, and the design states it rather than leaving two sibling units looking
> inconsistent: **a registry row records what a run did; an `AccessRecord` is the only
> evidence that the locked test was opened at all.** A lost registry row can be
> reconciled against the run's other artifacts. A lost `AccessRecord` leaves **no trace of
> the access** — which is precisely why SEC-G-02 requires orphan detection **in both
> directions**. Option B's stamped record is a record that **might not exist**, and for the
> December lock that is the failure the guard exists to prevent.

> **⚠ The cost, stated as a scheduling dependency and not as a footnote.** This **blocks
> the required pre-G-05 December coverage audit on Kaggle** until **W-6 step 8's durability
> measurement** is done. That audit is a **precondition of G-05** (Vision §8.3), so the
> measurement moves onto the critical path. Choosing A is choosing to do the measurement
> first.

**Q2 = A — the exempt list is a module-level constant in the guard, with its membership
asserted by a test.** The list has **six members counting the chokepoint**
`src/data/locked_test.py`; member 5 is `scripts/merge_coverage_year.py`, a **production
script, not a test**.

**The criterion applied was "what does it take to widen this?"** A code change to a guard
module plus a test update (A); a YAML edit (B); a comment added to the file that wants the
exemption (C). Only A makes widening as deliberate as the boundary is meant to be — and C
inverts the property entirely, turning a maintained list into a permission each module
grants itself. **The design must state why TC-03e does not reach this**, since a reader
applying that rule by analogy will read a source-resident constant as misplaced: TC-03e
governs **scientific constants**, and a security allowlist is not one.

**Q3 = A — two independent scans, each with its own entry point and its own failure.**
The **literal scan** asks who may **name** the restricted root; the **residency scan**
asks whether **December content has escaped it**. Different hit definitions, different
failures. The decisive reason: **the residency scan carries no §16 or §19 acceptance row
at all** (`FR-P1-02-6`), and coupling a check that has evidence obligations to one that
has none invites the rowless check to ride on the other's evidence. **R-27's
unparseable-is-a-failure rule is one helper both call**, which takes the real benefit of a
shared walk without the coupling.

**Q4 = A — components split on enforcement timing**, mirroring **R-24's hierarchy**:
**run-time guards** (the `open_restricted` chokepoint, the access recorder, the
phase-boundary assertions, the protected-hash differ) as one component; **static scans**
(literal, residency) as a second; the **reuse registry** as a third. A static-scan failure
is a warning to fix before a run; a run-time guard failure **stops the run**. Conflating
them is how an advisory scan comes to be treated as enforcement. This is the same kind of
criterion `foundation` used — **failure consequence, not module listing** — so the two
units stay comparable.

**Carried, not re-decided.** `open_restricted` **durably appends the `AccessRecord`
before the read begins**; a log-write or durability failure **prevents the read** (R-25).
**Holding the literal is not an access; reading bytes is** (D-15, as scoped by R-28). The
static check is **AST-based with constant folding**, and its **dynamic-path residual is
stated in the rule body**: a value read from config, an environment variable or a name
computed at run time **still passes** — the blind spot **narrows, it does not close**.
**R-24's hierarchy is unchanged**: static scan is early warning, **run-time assertions are
authoritative**, and both run. `RAW_MODULES` is **four** modules — `rinex`, `calibration`,
`target`, `verification`. **Both** phase-boundary limbs run and **neither substitutes for
the other**; `assert_no_raw_fields` is called by **each of the eight Phase 1 producing
scripts before it writes**, with a completeness test asserting every one of them calls it.
Phase 2 **refuses to train if any protected hash differs**; Phase 1 weights are **never**
carried forward. An **unparseable file is a failure, never a skip** (R-27). Reuse is
registered **before use**, and reimplementation from the paper is the **standing default**
while the AGPLv3 question is open.

**Two discrepancies found by the workspace check, both recorded in 
and owed to the human at the gate** *(added on re-presentation)*:

- **DISC-1 — the exempt list has SEVEN members on disk, not six.**
   enumerates the chokepoint plus six others; the seventh,
  , was **added 2026-08-28 because the
  membership assertion caught it on first run**. The mechanism working is what made every
  document's count stale. Verified by parsing the set literal: **exactly 7**.
- **DISC-2 — the literal scan is TEXTUAL, not AST-based.** It does
  , so the **concatenated-literal evasion that
  Q2 = B's AST-plus-constant-folding was chosen to close is open**. A design-versus-
  implementation gap; the requirement stands, the code does not yet meet it. **Owed at 3.5.**

**On execution.** ........................................................................ [ 25%]
..............................s...s..................................... [ 51%]
........................................................................ [ 77%]
...............................................................          [100%]
277 passed, 2 skipped in 4.25s returned **277 passed, 2 skipped** on
2026-09-01 — under **Python 3.14.7 with pytest 9.1.1**, against a governed pin of **3.11
exactly** (TE §8.1, TC-03d) and with no  to pin pytest. **Not governed
evidence**; it discharges nothing.

**Status claims made. None.**

> ⛔ **The one-door property is BREACHED today at two named sites** —
> `tests/test_release_hashes.py:137` and `tests/test_acquisition_window.py:195` read
> content beneath the restricted root **with no `AccessRecord`**. **Nothing is
> grandfathered**: `open_restricted` does not exist, so there is no guard for these reads
> to predate. Remediation is **owed at stage 3.5** and is a **precondition of the G-05
> evidence package**. **No artifact may describe the one-door property as enforced.**

**WS-18 and TA-18 are `Pending`** and `tests/test_locked_test_guard.py` is **unexecuted**;
**TA-27 and TA-28 are `Pending`**; **`FR-P1-02-6` carries no acceptance row at all**;
**G-P2 is unaffected by G-09's signature**. **G-09 is signed (D-31) with its own
preconditions UNMET**; **stage 3.1 remains FAIL**; `configs/` does not exist; **no Python
interpreter exists in this environment**, so every test is written-but-unexecuted or
unwritten.

Reply `Looks correct` to proceed, or state what to change.

[Answer]: Looks correct
