# Security Requirements — `fixtures-and-reproducibility`

**Unit** `fixtures-and-reproducibility` (Bolt 12) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NOTHING HERE IS CLAIMED SATISFIED — AND NEITHER FIXTURE HAS EVER RUN
>
> **No measured value exists.** Every runtime, tolerance, row-count range and storage figure in
> this unit's design is a **placeholder** until fixture time (TE §15.1), and **the two manifest
> freeze acts — promoting measured values from `candidate` to `frozen` — are the project
> owner's under Q-31**. Nothing here performs them.
>
> **THREE requirements have no acceptance row** — **FR-WS-2**, **FR-WS-3** and **FR-P1-03-5**
> *(banner corrected 2026-09-01 as the third representation of the same figure; superseded:
> "FR-WS-2 and FR-WS-3 have no acceptance row". The iteration-1 Critical corrected the table
> cell and the derivation; **this banner states the fact first and was left behind** — the
> sweep-every-representation defect, committed once more by the repair fixing an instance of
> it, and caught only because the write-freeze forced it to the gate.)* FR-WS-2 and FR-WS-3 are
> covered by R-136's controls (13) and (14) meanwhile — **a control is not a row** — and
> `requirements.md` records **FR-P1-03-5 as `UNTESTED`, WS-05 deferred to G-P3A**. With
> **REQ-ENG-10 untested by design**, **4 requirements carry no evidence**. **WS-20, TA-09, TA-17, TA-03 and TA-26 are
> undischarged**, and **WS-01 plus WS-09…WS-20 is a 13-row bounded set, not a discharged one**.
>
> **BLK-08 ↓ is checked here rather than inherited silently.** **G-09 is signed (D-31) with its
> own preconditions UNMET**; **stage 3.1 remains FAIL**; `configs/` does not exist; **no Python
> interpreter exists in this environment**.
>
> No scientific value is decided here, and TE §18.2's absolute rule stands.

## Sources

- `../functional-design/business-rules.md` — **R-133** (one manifest schema, **one validating loader, and the loader is the only read path**), **R-134** (**measure then freeze**: two manifest states, identity by citation, **no silent update**), **R-135** (the plumbing fixture: identity cited, one-station scope enforced, **DATA-07 and the December-representativeness prohibition travelling as freight**), **R-136** (**the plumbing fixture is never evidence**, and December is excluded **on record dates**), **R-137** (fixture partitions are **apparatus constants in a quarantined id space**; the M10 step is named), **R-138** (the clean run executes the **amended §13.2 sequence verbatim** — the seven Phase 1 invocations, **Phase 2 deferred to G-P2** — **on CPU, with no GPU visible**), **R-139** (the comparison ledger: classes declared in the manifest, **exactness where §13.7 demands it**, **no expectation ever updated**), **R-140** (fixture-pass receipts, and an **exported two-receipt check** for any full-year job), **R-141** (the Kaggle **in-session gate is a producing path**, stamped by the platform and bound to the run's own lock), **R-142** (the matrix, the bounded acceptance table and the preflight report are **generated paths that refuse**).
- `../functional-design/business-logic-model.md` — **W-1** … **W-10**, in particular **W-2** (measure then freeze, and the act in between), **W-4** (the smoke quarantine and the record-date December exclusion), **W-6** (`test_clean_run.py`: the amended §13.2 sequence verbatim, and the comparison ledger), **W-7** (the ordering contract as an executable gate), **W-8** (the Kaggle in-session gate), **W-9** (the three evidence artifacts as generated paths that refuse).
- `../../../inception/requirements-analysis/requirements.md` — **FR-WS-1** … **FR-WS-6**, **FR-WS-7** (context — `foundation`'s §18.3 preflight requirement, whose evidence artifact is `aws_ai_dlc_preflight_report`, distinct from this unit's `environment_and_cpu_preflight_report`), **FR-P1-03-5**, **REQ-ENG-4**, **REQ-ENG-5**, **REQ-ENG-10**, **REQ-NFR-A3**, **NFR-REP-01**, **NFR-PHASE-01**.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§9.1–9.2** (the two platforms; **run both fixtures before any full-year job**; CPU a complete execution path), **§13.1** (the eight environment-lock items), **§13.2** (the ordered clean-run sequence), **§13.7** (**the five exact-equality classes**), **§15.1** (**measured from the fixtures and frozen, never invented**), **§15.2** (the fixture manifest's fields), **§15.3** (the reduced-replicate fixture bootstrap), **§16** (WS-01, WS-09…WS-20), **§18.2–18.3**, **§19** (TA-03, TA-09, TA-17, TA-26).
- `evidence/DECISIONS.md` — **D-11** (the plumbing window: **2022-11-01 to 2022-11-07**, seven days, one station, **smoke test only**), **D-14** (the scientific fixture: **March 2022**), **D-18** (the re-merge that hashed differently on identical records — `DATA-17`).
- `nfr-requirements-questions.md` — Q1 = A, Q2 = A, and the receipted Consolidated Summary Confirmation.

---

## Scope note

`produces_kinds` excludes `performance-requirements`, `scalability-requirements` and
`reliability-requirements` for a `library` unit. Assessed anyway:

| Category | Assessment for `fixtures-and-reproducibility` | Where it lives |
|---|---|---|
| **Performance** | **Every figure is a placeholder.** Runtimes and storage are **measured on the fixtures and frozen** (TE §15.1) — **neither fixture has run**, so nothing is asserted. R-141 records the in-session gate's **own measured total runtime**, and **no session or wall-clock ceiling exists in any authority** to check it against. | § SEC-X-04 |
| **Scalability** | Bounded: two fixtures, three cells, one year. No growth projection. | — |
| **Reliability** | **This unit IS the project's reliability evidence.** Its posture is fail-closed throughout: the loader **refuses** an invalid or hash-mismatched manifest, an `exact`-class mismatch **raises** and **never updates the expectation**, a full-year job **without two receipts fails**, and a governed Kaggle run without a valid in-session gate **fails before domain work**. | § SEC-X-01 … § SEC-X-04 |
| **Security** | This artifact — **the integrity of the evidence that everything else rests on**. If the fixture manifest can be edited to match a bad run, every reproducibility claim in the project becomes unfalsifiable. | § SEC-X-01 |
| **Observability** | The two fixture-pass receipts; the in-session gate result with its §13.1 lock items and measured total runtime; the three generated evidence artifacts. | § SEC-X-03, § SEC-X-04 |

---

## SEC-X-01 — The frozen manifest is hash-protected, so an edited expectation cannot load

**Requirement (R-133, W-1).** There is **one manifest schema**, **one validating loader**, and
**the loader is the only read path**. No test body reads a manifest directly.

**Requirement (R-134, W-2).** **Measure then freeze**: two manifest states, `candidate` and
`frozen`, with **identity by citation** and **no silent update**. **The freeze act is the
project owner's under Q-31** — nothing in this unit performs it.

**Requirement (R-139).** Every required output carries its **comparison class in the manifest**,
declared **per output at freeze time**, never in a test body: **`exact`** for §13.7's five
classes — **hashes, schemas, partition membership, IDs, and deterministic CPU transformations**,
compared for **equality, not tolerance** — and **`toleranced`** otherwise against the manifest's
declared floating-point tolerance **with its units**. A mismatch in an `exact`-class artifact
**raises**, naming file and violated expectation, and **never updates the expectation**.

> ### Requirement (Q2 = A) — "no silent update" becomes a MECHANISM
>
> The frozen values carry a **manifest hash recorded outside the manifest**, and **the single
> validating loader refuses a manifest whose hash does not match**. An edited expectation
> **fails to load** rather than silently becoming the new truth.
>
> **Why a rule was not enough.** R-139 and R-134 are **rules**; the failure they describe is a
> person **editing a YAML expectation to match what a run produced**. This project's own
> evidence shows the moment is real: **D-18's re-merge hashed differently from an artifact
> holding the identical record set** because output order followed directory traversal, and
> only a sort on the dedup key made two consecutive runs agree byte for byte (`DATA-17`). That
> is precisely when updating the expectation looks like the reasonable fix.
>
> **Why not procedural detection.** The edit is visible in a diff — but `team.md` records this
> as a **single-author codebase with no pull requests**, so "review" means the author reviewing
> their own edit at the moment they most want it to change.
>
> **The friction is intended.** A legitimate re-freeze becomes a **deliberate two-step act**,
> which is appropriate because **Q-31 already makes the freeze an owner act**. The check costs
> one comparison at the one place — R-133's loader — that every read already passes.
>
> ### ⛔ THE CHOKEPOINT THIS RESTS ON IS NOT ENFORCED — read this with the mechanism
>
> *(Moved into the Requirement body 2026-09-01 on adversarial finding 2, Major. It was stated
> only under `## Assumptions`, leaving this block asserting that the hash check closes "no
> silent update" without the qualification. **Fourth occurrence of that misplacement in this
> stage**, recorded in `project.md` § Corrections.)*
>
> **R-133 states the loader is the only read path. Nothing enforces that today.** A test using
> **`yaml.safe_load` directly** would bypass **both** the schema validation **and** this hash
> check, and nothing would fail.
>
> **So the mechanism is exactly as strong as an unenforced convention.** It closes the case
> where an edited manifest is read through the loader — which is every read the design
> intends — and closes nothing where a reader goes around it. **The check that would catch
> that is R-132's convention, and it is unwritten.** **No artifact may describe "no silent
> update" as enforced.**

**Requirement (R-139).** **No tolerance, class or expectation lives in a test body** — TC-03e's
shape applied to test apparatus.

## SEC-X-02 — The plumbing fixture is never evidence, and December is excluded on record dates

**Requirement (R-135, R-136, W-3, W-4, TC-03f).** The **seven-day single-station plumbing
fixture** (**D-11**: 2022-11-01 to 2022-11-07) is a **smoke test only** and is **never
scientific evidence**. Its **one-station scope is enforced**, not assumed, and its identity is
**cited from D-11** rather than restated.

**Requirement.** The **`smoke_only` stamp** travels with it, asserted by the surfaces that
consume it, with **absence assertions** on the paths that must not accept it.

**Requirement — DATA-07 and the December-representativeness prohibition travel as freight.**
D-11 carries the mandatory limitation that the window **does not reproduce December's
winter-solstice regime or activity distribution and is not representative of the locked month**,
and the **provisional-Dst restriction**: it may characterise **selection only**, and must
**never** become a modelling input, a frozen tolerance, or a G-05 regime count.

**Requirement (R-136).** **No record whose observation date falls in December 2022 enters
either fixture**, asserted on **record dates** — never on the folder a file was filed under.
This is a rule rather than a convention because the year-blind acquisition predicate already
filed locked-month records into `audit_evidence_2022-01/` in fact
(`tests/test_acquisition_window.py`, R-31).

**Requirement (R-137, W-5).** Fixture partitions are **apparatus constants in a quarantined id
space** — they cannot collide with, or be mistaken for, the scientific partition ids — and the
**M10 contract-fixture step is named**.

**Status.** ~~**FR-WS-2 and FR-WS-3 have no acceptance row.**~~ ⛔ **THREE requirements have no
acceptance row — FR-WS-2, FR-WS-3 and FR-P1-03-5**, the last recorded by `requirements.md` as
**`UNTESTED` (WS-05 deferred to G-P3A)**. R-136's controls (13) and (14) cover **FR-WS-2 and
FR-WS-3** meanwhile, and **a control is not a row**; **FR-P1-03-5 has no control standing in for
it either**. With **REQ-ENG-10 untested by design**, **4 requirements carry no evidence**.

> *(Corrected 2026-09-01 — the **fourth** site in this one file to carry this figure, found on
> the re-verification pass after the banner, the table cell and the derivation had each been
> corrected in turn. The first repair fixed the table cell and derivation; the second fixed the
> banner; **this paragraph states the same fact a third way and survived both**. Derived by
> sweeping the file's live region for every phrasing of the claim rather than for the string a
> finding named — which is what `project.md` `fd-2026-08-30-sweep-derive-sites` prescribes and
> what the two preceding repairs did not do.)*

## SEC-X-03 — The clean run compares, and the ordering contract is executable

**Requirement (R-138, W-6, FR-WS-5, NFR-REP-01).** The clean run executes the **amended §13.2
sequence verbatim** — the **seven Phase 1 invocations**, with **Phase 2 deferred to G-P2** — **on
CPU, with no GPU visible**. Phase 2 invocations are **not** run, and a Phase-2-only invocation
**raises `PhaseBoundaryError`** (NFR-PHASE-01).

**Requirement (R-139).** **The clean run compares; it does not merely succeed.** *"A run that
exits zero without comparing artifacts satisfies A's shape and fails WS-20's wording while
appearing green."* Runtime and storage are asserted inside the manifest's **measured** ranges.

**Requirement (R-140, W-7, TE §9.2).** **Both fixtures pass, in order, before any full-year
job** — the plumbing fixture then the scientific fixture. Each emits a **fixture-pass receipt**,
and an **exported two-receipt check** is the executable form of the ordering contract: **a
full-year job without both receipts fails**.

**Requirement (R-142, W-9).** The **matrix, the bounded acceptance table and the preflight
report are generated paths that refuse** — the TA-09 acceptance table is **bounded to 13 rows by
construction** (WS-01 plus WS-09…WS-20), and a **deferral is a raise** rather than a silent
omission. **WS-02–WS-08 are deferred to G-P3A**, which is why the bound is 13 rather than 20.

**Carried — BLK-08 ↓ is checked here rather than inherited silently.** A clean-run tolerance
stated in TECU **cannot be checked** against output no design path returns to TECU.

## SEC-X-04 — The in-session gate, and what makes a gate result stale

**Requirement (R-141, W-8, TC-03g `binding: hard`, TE §9.1–9.2, REQ-NFR-A3).** Before any
governed Kaggle run, the **critical test set and both fixtures execute in-session**, emitting a
machine-readable **in-session gate result** carrying:

- the **resolved platform**, taken from `ConfigSnapshot.platform` — resolved by `foundation`'s
  `resolve_platform_roots` detection, **never asserted by the caller**;
- the **§13.1 environment-lock items in force** — code commit, the four configuration snapshot
  hashes, the `requirements.txt` hash and per-run `pip freeze`, versions, input dataset and
  manifest versions, platform, known nondeterministic operations;
- timestamps, and **per-test and per-fixture results**;
- its **own measured total runtime**, recorded into `environment_and_cpu_preflight_report` at
  **G-07**.

**Why in-session at all.** A Kaggle session carries **no git working tree**, **no commit hook
fires there**, and **a local suite run proves nothing about the environment the governed run
actually executes in**. **REQ-NFR-A3 names the gap NFR-REP-01 leaves**: NFR-REP-01 governs *a*
clean environment, **not *the* platform**.

> ### Requirement (Q1 = A) — staleness is a DERIVED FACT, not a time window
>
> A governed run may **reuse** an in-session gate result **only if its §13.1 lock items are
> identical to those the gate recorded**. **Any difference makes the result stale and the gate
> re-runs.**
>
> **Why the lock and not a clock.** What invalidates a gate is a **changed environment**, not
> elapsed minutes. A config edited one minute after the gate would pass a time window; an
> untouched session would fail one. Binding to the lock makes a config edit or a re-install
> **invalidate the gate automatically**, and permits reuse within one unchanged session — which
> is what makes an expensive precondition tolerable rather than an incentive to skip it.
>
> **Its limit, stated.** It **cannot see a change the §13.1 items do not cover**, so the check
> is **only as good as the lock's completeness**.

**Requirement.** A governed Kaggle run whose evidence record **lacks** a gate result — **or
carries one stamped `local`** — **fails before domain work**, rather than proceeding silently.

> ### ⚠ THIS GATE IS SPECIFIED AND UNRUNNABLE TODAY
>
> *(Stated here 2026-09-01 on adversarial finding 3, Minor: `tech-stack-decisions.md` § TS-X-05
> carried this disclosure and **the artifact that owns the gate as a functional requirement did
> not**.)*
>
> The gate reads **`ConfigSnapshot.platform`, resolved by `foundation`'s
> `resolve_platform_roots`** — **never asserted by the caller** — and **that detection does not
> exist**. **`configs/` does not exist either**, so the **four configuration snapshot hashes**
> Q1's staleness comparison depends on **have nothing to hash**.
>
> The gate's correctness therefore **rests on a sibling's detection being right**, and **no part
> of this section can run today**.

**No ceiling is invented for the measured runtime.** **No session or wall-clock ceiling exists
in any authority** — the only quota is the ~30 Kaggle **GPU** hours per week at Vision §4.4,
which *"are available but not required"* and **does not bind the CPU path**. The figure is
recorded so it is **visible at the gate that would care**, not checked against a limit that does
not exist.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| FR-WS-1 | SEC-X-02, SEC-X-03 | **WS-20, TA-09 (primary)** | `Pending` |
| **FR-WS-2** | SEC-X-02 | ⚠ **NO ROW** — R-136 control (13) meanwhile | not evidence |
| **FR-WS-3** | SEC-X-02 | ⚠ **NO ROW** — R-136 control (14) meanwhile | not evidence |
| FR-WS-4 | SEC-X-03 | **WS-01, WS-09…WS-20 — 13 rows, bounded by construction** | `Pending` |
| FR-WS-5 | SEC-X-03 | **WS-20, TA-17 (primary)** | `Pending` |
| FR-WS-6 | SEC-X-04 | TA-03, TA-26 (supporting) | `Pending` |
| **NFR-REP-01** | SEC-X-01, SEC-X-03 | **WS-20, TA-17 (primary)** | `Pending` |
| **REQ-NFR-A3** | SEC-X-04 | TA-03 (supporting) | `Pending` |
| FR-WS-7 *(context — `foundation`'s)* | SEC-X-04 | TA-23 | `Pending` — **`aws_ai_dlc_preflight_report` does not exist** |
| **FR-P1-03-5** | SEC-X-01 | ⚠ **NO ROW** — `requirements.md` records it **`UNTESTED` (WS-05 deferred to G-P3A)** | not evidence |
| REQ-ENG-4 | SEC-X-03 | TA-09 — bounded scope | `Pending` |
| REQ-ENG-5 | SEC-X-03 | TA-27 — row owned by `governance-guards` | `Pending` |
| REQ-ENG-10 | SEC-X-04 | ⚠ **UNTESTED by design** — no row covers §13.1's capture list | not evidence |
| NFR-PHASE-01 | SEC-X-03 | TA-27 — row owned by `governance-guards` | `Pending` |

**Derived and printed**: 4 requirement sections (SEC-X-01…SEC-X-04); **14** coverage rows — the
**8** the `functional-design` map carries, plus **FR-WS-7**, **FR-P1-03-5**, **REQ-ENG-4**,
**REQ-ENG-5**, **REQ-ENG-10** and **NFR-PHASE-01**, which this unit's design names and this
artifact states obligations against; **3 without any acceptance row** — **FR-WS-2**, **FR-WS-3** and **FR-P1-03-5**, the last recorded by `requirements.md` as **`UNTESTED` (WS-05 deferred to G-P3A)** — **plus REQ-ENG-10 untested by design**, so **4 carry no evidence** *(corrected 2026-09-01 on adversarial finding 1, Critical; superseded: "2 without any acceptance row (FR-WS-2, FR-WS-3), matching the map, plus REQ-ENG-10". **FR-P1-03-5's table cell already read `—`** — the same shape as FR-WS-2 and FR-WS-3 — and the printed derivation counted it in neither total. **Seventh instance of this defect family in twelve units, and the first inside the unit that calls itself the project's reliability evidence.**)*; **0** rows claimed satisfied.

## Assumptions & Open Questions

- **[Q1]** Gate reuse is bound to the §13.1 lock. **It cannot see a change the lock items do not cover** — the check is only as good as the lock's completeness, and **`configs/` does not exist**, so the four configuration snapshot hashes have nothing to hash yet.
- **[Q2]** The manifest hash must be **recorded outside the manifest**. **Where it lives is owed at 3.5** — nothing here designs that surface, and a hash recorded inside the file it protects would protect nothing.
- **[assumption]** The loader is genuinely the only read path. **R-133 states it; nothing enforces it today** — a test that opened a manifest with `yaml.safe_load` directly would bypass both the schema validation and the hash check. **The check that would catch that is R-132's convention**, and it is unwritten.
- **[assumption]** Fixture-pass receipts survive the session that wrote them. **Kaggle's durability semantics are unmeasured** (`foundation` W-6 step 8's carried dependency), and the two-receipt check for a full-year job depends on receipts written in an earlier session still being there.
- **Carried, and the owner's — the two manifest freeze acts under Q-31.** **Neither fixture has run**, so **no measured value exists to freeze**.
- **Carried — BLK-08 ↓** is checked here rather than inherited silently; a TECU-stated tolerance is uncheckable until R-103's joint contract is adopted by both halves.
- **Carried — WS-02–WS-08 are deferred to G-P3A**, which is why FR-WS-4's table is bounded to **13** rows and not 20.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | § Requirement coverage (this file, rows 189–210) | **FR-P1-03-5's coverage row is silently miscounted.** `../../../inception/requirements-analysis/requirements.md` line 912 (`FR-P1-03-1…5` crosswalk row) states verbatim: *"FR-P1-03-5 `UNTESTED` (WS-05 deferred to G-P3A)"* — the upstream authority explicitly flags this requirement as untested-by-design, the same status this artifact confers on REQ-ENG-10. Yet in this file's own coverage table, FR-P1-03-5's **Acceptance row cell is `—`** (literally empty, identical in kind to FR-WS-2/FR-WS-3's no-row state), and its Status cell reads plain `Pending` — not the `⚠ NO ROW` / `not evidence` treatment given to FR-WS-2, FR-WS-3 and REQ-ENG-10. The artifact's own printed derivation then compounds the miss: *"2 without any acceptance row (FR-WS-2, FR-WS-3)... plus REQ-ENG-10 untested by design"* — FR-P1-03-5 is counted in neither set, despite meeting both criteria (no row cited, upstream-flagged UNTESTED). This is the same completeness-check failure family (text/ID reproduced from an upstream source, its untested status not surfaced) that the dispatch brief records as recurring across six consecutive units, now with a seventh instance, and it sits inside this unit's own stated core deliverable — "This unit IS the project's reliability evidence" — where an inaccurate completeness count is a direct defect in the evidence itself, not merely cosmetic. | Add FR-P1-03-5 to the "no acceptance row" enumeration (making it 3, not 2) and/or flag it `⚠ NO ROW — UNTESTED (WS-05 deferred to G-P3A)` to match FR-WS-2/FR-WS-3/REQ-ENG-10 treatment; recompute and reprint the derived-and-printed summary line. |
| 2 | Major | § SEC-X-01 (this file) and `tech-stack-decisions.md` § TS-X-01 | **The chokepoint's unenforced status is confined to Assumptions in both artifacts.** SEC-X-01's Requirement body (R-133) states flatly "the loader is the only read path" as the mechanism the hash-protection rests on; the concession that *nothing enforces this today* — a test calling `yaml.safe_load` directly would bypass both schema validation and the hash check, and "the check that would catch that is R-132's convention, and it is unwritten" — appears only under `## Assumptions & Open Questions` (line 216), never in SEC-X-01's own Requirement text where the mechanism is asserted. `tech-stack-decisions.md` TS-X-01 restates "R-133 already makes the loader the only read path" as settled fact and carries no concession anywhere in its decision body. Per `project.md` § Corrections (`fd-2026-08-30-sweep-numerals-and-surfaces`), a concession landing only in Assumptions while the rule's own body — what an implementer reads first — keeps asserting the closed version has been Major on three prior units; this is the same pattern's fourth occurrence, and it directly weakens Finding 1 in Q4 of the dispatch brief: the hash-protection mechanism SEC-X-01 sells as closing "no silent update" rests on a chokepoint conceded elsewhere to be open. | Move the unenforced-chokepoint concession (or a summary of it) into SEC-X-01's Requirement text and into TS-X-01's decision body, not only Assumptions. |
| 3 | Minor | `tech-stack-decisions.md` § TS-X-05 vs. this file's § SEC-X-04 | **Asymmetric "unrunnable today" disclosure.** `tech-stack-decisions.md` TS-X-05 states the in-session gate is *"specified and unrunnable today"* because it reads `foundation`'s non-existent `resolve_platform_roots`, and repeats this in its own Assumptions. This file's SEC-X-04, which owns the same gate as a functional requirement, states the same dependency ("resolved by `foundation`'s `resolve_platform_roots` detection, never asserted by the caller") but never states the "unrunnable today" consequence anywhere in this PRIMARY artifact — not in the SEC-X-04 body, not in this file's own Assumptions. A reader of the primary artifact alone would not learn the gate cannot run yet. | State "specified and unrunnable today" (or equivalent) in SEC-X-04 or this file's Assumptions, not only in the sibling tech-stack artifact. |

### Validation Tool Results

No stage-declared validation tools were listed for `nfr-requirements`; checks below were performed manually against the artifacts and the upstream `requirements.md` crosswalk.

| Check | Result | Interpretation |
|---|---|---|
| ID set-difference: 11 NFR IDs + `FR-WS-*`/`FR-P1-0*-*`/`REQ-*` against both artifacts' Sources/coverage tables | FR-P1-03-5 cited but its UNTESTED status from `requirements.md`:912 not carried into this file's coverage-derivation counts (Finding 1) | Confirms the completeness-check family defect |
| `security-requirements.md` coverage table: 8 (map) + 6 (named) = 14, and 14 rows counted | 8+6=14 ✓; table has exactly 14 rows (FR-WS-1…7 minus none, FR-P1-03-5, REQ-ENG-4, REQ-ENG-5, REQ-ENG-10, NFR-PHASE-01, NFR-REP-01, REQ-NFR-A3) | Arithmetic and row count both correct |
| `tech-stack-decisions.md`: 14 − 7 = 7, and 7 rows counted | 14−7=7 ✓; table has exactly 7 rows | Arithmetic and row count both correct |
| New-mechanism framing (hash-protected manifest location "owed at 3.5"; "hash inside the file it protects protects nothing") | Present in both artifacts' bodies, not only Assumptions | No defect |
| Lock-bound gate reuse framing ("cannot see a change the §13.1 items do not cover") | Present in this file's SEC-X-04 body (blockquote) | No defect |
| TS-X-02 determinism claim vs. D-18/pyarrow-unverified concession | Decision body states requirement prescriptively ("must not depend on..."); "unverified" concession correctly placed in Assumptions | No defect — this is a forward-looking requirement, not a claim of present compliance |
| No claim of satisfaction/discharge/measurement (dispatch Q6) | Both artifacts consistently state 0 rows satisfied, both fixtures never run, freeze acts are the owner's, `configs/` absent, G-09/stage 3.1 status carried | No defect found |

### Summary

Two of the three findings are structural repeats of failure patterns this stage has already logged as recurring across prior units (a completeness-check miss on an upstream-flagged UNTESTED requirement, and a hash-chokepoint concession confined to Assumptions rather than the rule body it undercuts) — the fact that they recur on the twelfth and final unit, after the pattern was already named in five prior reviews, is itself the strongest evidence this needs a repair pass before READY. The arithmetic claims (14 = 8+6, 7 = 14−7) both check out, and the "nothing is claimed satisfied" framing is honest and consistently applied elsewhere in both artifacts.

NOT-READY

## Review — iteration 2 (terminal)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 2 (terminal)

### Prior findings — resolution check

| # | Severity | Resolution |
|---|---|---|
| 1 | Critical | **Resolved.** Line 231's FR-P1-03-5 row now reads `⚠ NO ROW — requirements.md records it UNTESTED (WS-05 deferred to G-P3A)`, matching the FR-WS-2/FR-WS-3/REQ-ENG-10 treatment. The derivation paragraph (line 240) now reads "3 without any acceptance row — FR-WS-2, FR-WS-3 and FR-P1-03-5 … plus REQ-ENG-10 untested by design, so 4 carry no evidence," with the superseded 2-count preserved in a dated correction box naming this as the "seventh instance of this defect family." Table and prose agree: 3 `⚠ NO ROW` cells + 1 `⚠ UNTESTED by design` cell = 4, exactly as stated. |
| 2 | Major | **Resolved.** `security-requirements.md` § SEC-X-01 body (lines 92–99, a boxed blockquote inside the Requirement text, not Assumptions) now states "R-133 states the loader is the only read path. Nothing enforces that today" and names R-132's unwritten convention as the missing check. `tech-stack-decisions.md` § TS-X-01 body (lines 50–53) carries the matching concession. Both artifacts still repeat the point under Assumptions (redundant, not a defect). |
| 3 | Minor | **Resolved.** `security-requirements.md` § SEC-X-04 body (lines 200–208) now states the gate "rests on a sibling's detection being right" and that "no part of this section can run today," and that `configs/` does not exist so the four configuration hashes "have nothing to hash" — matching `tech-stack-decisions.md` TS-X-05's "specified and unrunnable today" framing in both artifacts' bodies, not only Assumptions. |

### Consistency re-check

| Check | Result |
|---|---|
| `security-requirements.md` coverage table: 14 rows, 8 (map) + 6 (named) | Table (lines 222–235) has exactly 14 data rows; decomposition (line 237–239) names FR-WS-7, FR-P1-03-5, REQ-ENG-4, REQ-ENG-5, REQ-ENG-10, NFR-PHASE-01 as the 6 beyond the map's 8 — matches. |
| "3 without any row … 4 carry no evidence" vs. table's actual `⚠` cells | Table shows exactly 3 `⚠ NO ROW` (FR-WS-2, FR-WS-3, FR-P1-03-5) and 1 `⚠ UNTESTED by design` (REQ-ENG-10) — 3+1=4, matches the prose exactly. |
| `tech-stack-decisions.md`: 7 rows, "seven fewer than fourteen" | Table (lines 149–155) has exactly 7 rows; the named excluded-ID list (FR-WS-2, FR-WS-3, FR-WS-7, FR-P1-03-5, REQ-ENG-4, REQ-ENG-5, REQ-ENG-10 — 7 IDs) reconciles arithmetically against `security-requirements.md`'s 14; 14−7=7 checks out. |
| Completeness set-difference: `FR-WS-*`, `FR-P1-0*-*`, `REQ-*`, 11 NFR IDs against both artifacts' coverage tables | Union of the two tables' Requirement columns: FR-WS-1…7, FR-P1-03-5, REQ-ENG-4, REQ-ENG-5, REQ-ENG-10, NFR-PHASE-01, NFR-REP-01, REQ-NFR-A3 — matches this unit's Sources list (line 26) with no addition or omission found within this unit's own read scope. |
| Regression scan on the three touched sites (one table row, one derivation paragraph, three inserted blocks) | No new contradiction introduced; the correction boxes correctly preserve the superseded figures per `project.md`'s append-only sweep rule rather than silently overwriting them. |

### Not newly discharged (confirmed unchanged)

Neither fixture has run; no measured value exists; the two manifest freeze acts remain the owner's under Q-31; FR-WS-2/FR-WS-3/FR-P1-03-5 carry no acceptance row; REQ-ENG-10 is untested by design; WS-20/TA-09/TA-17/TA-03/TA-26 remain undischarged; `aws_ai_dlc_preflight_report` is confirmed non-existent and distinct from this unit's own artifact; `configs/` does not exist; `resolve_platform_roots` does not exist. None of these are claimed resolved by this pass or by the repairs under review.

### Summary

All three iteration-1 findings are repaired at the locations claimed, in the artifact bodies rather than only in Assumptions, and every dependent count (14, 8+6, 3+1=4, 7, 14−7) is now internally consistent between prose and table on both artifacts. No new defect surfaced on this terminal pass.

## Review — 2026-09-01 iteration 2 (terminal)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T04:57:28Z
**Iteration:** 2 (terminal)

### 1. Status-paragraph repair verified

Line 138's § SEC-X-02 Status paragraph now reads: `~~**FR-WS-2 and FR-WS-3 have no acceptance row.**~~ ⛔ **THREE requirements have no acceptance row — FR-WS-2, FR-WS-3 and FR-P1-03-5**`, with the superseded two-count struck through and dated. It states FR-P1-03-5's `UNTESTED (WS-05 deferred to G-P3A)` status, that R-136's controls (13)/(14) cover FR-WS-2/FR-WS-3 meanwhile but FR-P1-03-5 has no control standing in for it, and closes with `4 requirements carry no evidence` (REQ-ENG-10 folded in). This now agrees with the banner (line 12) and the derivation (lines 256–258).

### 2. Independent site re-derivation (fifth-site check)

Grepped `security-requirements.md` for every phrasing of the claim (numeral and spelled-out forms, "no acceptance row", "NO ROW", "carry no evidence", "untested", the individual IDs) across the full live region, plus a separate grep of `tech-stack-decisions.md` for the same terms. Result: **exactly the four sites already accounted for, all agreeing at 3 NO ROW + 1 UNTESTED = 4** — banner (line 12), the now-repaired Status paragraph (lines 138–142), the coverage-table cells for FR-WS-2/FR-WS-3/FR-P1-03-5/REQ-ENG-10 (lines 241, 242, 249, 252), and the printed derivation (line 256–258). `tech-stack-decisions.md` lines 158–159 name FR-WS-2/FR-WS-3/FR-P1-03-5/REQ-ENG-10 in a *different* count (7 IDs excluded because they raise no technology choice) — not a restatement of the rowless-requirement claim, so not a fifth site of this figure. **No fifth stale site found.**

### 3. No-regression checks

- Arithmetic: 14 = 8+6 (line 293, table row count confirmed), 7 = 14−7 (line 294/367), 3 NO ROW + 1 UNTESTED = 4 (line 368) — all print-derived and consistent, unregressed.
- Loader-chokepoint concession: present in both artifacts' bodies, not confined to Assumptions — `security-requirements.md` lines 92–99 (SEC-X-01 body) and `tech-stack-decisions.md` line 49 (TS-X-01 body), both stating R-133's only-read-path is unenforced, `yaml.safe_load` bypasses schema/hash checks, R-132's convention unwritten.
- § SEC-X-04 "specified and unrunnable today" disclosure: present at `security-requirements.md` lines 200–214 (gate rests on `foundation`'s non-existent `resolve_platform_roots`; `configs/` does not exist so the four hashes have nothing to hash) and matched at `tech-stack-decisions.md` lines 135, 170.
- FR-P1-03-5's table row (line 249) and its correct inclusion in the derivation (lines 256–258): intact.

### Findings

No findings this pass.

### Summary

The fourth stale site (§ SEC-X-02 Status paragraph) is repaired and now agrees with the other three sites; an independent sweep in every phrasing across both artifacts' live regions found no fifth stale representation. Arithmetic, the loader-chokepoint concession, and the SEC-X-04 unrunnable-today disclosure all check out unregressed. Terminal pass closes clean.

READY

READY

## Review — 2026-09-01 re-verification after gate rejection

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 1 of 2 (fresh budget after human gate rejection)

### 1. Banner correction — verified landed and consistent at its own site

Lines 12–21 (the top `⚠` banner) now read **"THREE requirements have no acceptance row — FR-WS-2, FR-WS-3 and FR-P1-03-5"**, with a dated correction box naming the superseded two-count and stating this was "the third representation of the same figure... left behind" by the earlier repair. It correctly totals **4** with REQ-ENG-10 ("4 requirements carry no evidence"). This matches the coverage table (3 `⚠ NO ROW` + 1 `⚠ UNTESTED by design` = 4, lines 230–241) and the printed derivation at line 247. Three sites now agree: banner, table, derivation paragraph.

### 2. Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | `security-requirements.md` line 138, § SEC-X-02 **Status** paragraph | **A fourth, still-stale representation of the corrected figure.** The paragraph reads verbatim: *"**Status.** **FR-WS-2 and FR-WS-3 have no acceptance row.** R-136's controls (13) and (14) cover them **meanwhile**, and **a control is not a row**."* This is not a quoted historical fact (no correction box, no "superseded" marker, no dated annotation) — it is stated as the live status of SEC-X-02, the same requirement section that owns FR-WS-2/FR-WS-3/FR-P1-03-5 in the coverage table two sections below. It omits FR-P1-03-5 entirely and gives no count, silently reproducing exactly the two-count that the banner (line 12), the derivation (line 247), and the iteration-2 review all now treat as superseded. This is the fourth site carrying this figure in this artifact (banner, table cells, derivation paragraph, and now this Status line), and it is the fourth instance of the "sweep every representation" defect this same unit already committed once at the gate. A developer reading SEC-X-02 top-to-bottom hits this Status line before the coverage table and would reasonably conclude only two requirements are affected. | Rewrite line 138 to state the current fact: three requirements (FR-WS-2, FR-WS-3, FR-P1-03-5) have no acceptance row for SEC-X-01/SEC-X-02 combined, or scope the sentence explicitly to "the two SEC-X-02 requirements" if that narrower scope is intended — but if narrower, say so explicitly rather than leaving a bare, unscoped repetition of the superseded system-wide count. |

### 3. Regression check — three earlier repairs still stand

- FR-P1-03-5's row (line 238) and its inclusion in the derivation (line 247): intact, unregressed.
- Loader-chokepoint concession: `security-requirements.md` SEC-X-01 body (lines 92–99 range) and `tech-stack-decisions.md` TS-X-01 body both still state R-133's only-read-path is not enforced today, `yaml.safe_load` bypasses schema validation and the hash check, and R-132's convention is unwritten — confirmed present, unregressed.
- § SEC-X-04 "specified and unrunnable today" disclosure (lines ~200–208): confirmed present, unregressed.

### 4. Arithmetic re-check

- `security-requirements.md` coverage table: 14 rows total, decomposed as 8 (map) + 6 named (FR-WS-7, FR-P1-03-5, REQ-ENG-4, REQ-ENG-5, REQ-ENG-10, NFR-PHASE-01) — 8+6=14, confirmed.
- `tech-stack-decisions.md`: 7 rows; line 158 states "seven fewer than fourteen," naming the 7 excluded IDs (FR-WS-2, FR-WS-3, FR-WS-7, FR-P1-03-5, REQ-ENG-4, REQ-ENG-5, REQ-ENG-10) — 14−7=7, confirmed.
- 3 `⚠ NO ROW` + 1 `⚠ UNTESTED by design` = 4 "carry no evidence" — confirmed at banner, table, and derivation (but contradicted by the stale line 138, Finding 1).

### 5. Completeness set-difference (NFR IDs)

Of the eleven named NFR IDs, only **NFR-PHASE-01** (7 occurrences in `security-requirements.md`, 1 in `tech-stack-decisions.md`) and **NFR-REP-01** (6/1) are reproduced by this unit's text — matching the Sources line (line 33) exactly. The other nine (`NFR-AUD-01, NFR-DET-01, NFR-DQ-01, NFR-FAIR-01, NFR-IRI-01, NFR-LEAK-01, NFR-LIC-01, NFR-SEC-01, NFR-TDEF-01`) do not appear in either artifact and are not claimed or reproduced here — no completeness gap on this axis; they belong to other units' scope.

### Not newly discharged (confirmed unchanged)

Neither fixture has run; no measured value exists; the two manifest freeze acts remain the owner's under Q-31; FR-WS-2, FR-WS-3 and FR-P1-03-5 have no acceptance row; REQ-ENG-10 is untested by design; WS-20, TA-09, TA-17, TA-03, TA-26 remain undischarged; WS-01 plus WS-09…WS-20 is a 13-row bounded set; `aws_ai_dlc_preflight_report` does not exist; BLK-08 remains open; `configs/` does not exist; G-09 is signed (D-31) with preconditions UNMET; stage 3.1 remains FAIL. None of these are claimed resolved by this pass.

### Summary

The banner correction landed correctly and is internally consistent with the table and the derivation paragraph — three sites now agree. But a fourth, unflagged representation of the superseded two-count survives at line 138 (§ SEC-X-02 Status), stated as live fact with no correction marker. This is the exact defect family the dispatch brief warned to hunt for, now found at a fourth site inside the very artifact whose repair history is about sweeping every representation. One Critical finding blocks READY.

NOT-READY
