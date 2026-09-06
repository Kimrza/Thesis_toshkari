# Security Design — `governance-guards`

**Unit** `governance-guards` (Bolt 2) · **Kind** `library` · **Stage** `nfr-design`

> **Re-saved 2026-09-02, content unchanged.** A `STAGE_JUMPED` redo of `nfr-design` — ordered
> by the project decision owner to repair a Critical finding in the sibling unit
> `external-products` — cleared this stage's per-unit checkpoint and review receipts for every
> unit. This unit's answers, artifacts and prior reviewer verdict were **not** revised; the
> summary was re-confirmed and the artifact re-saved so the required receipts exist again.
> **DISC-1 and DISC-2 stand exactly as recorded, and no status claim is altered by this
> note.**
>
> **Repeated once more the same day**, after a second owner-directed redo of the same stage.
> This unit was untouched by both. One item worth flagging to a reader of DISC-2:
> `inventory-and-registry` has now recorded that **`assert_no_december_outside_restricted`
> scans `*.json` only** while its docstring claims it walks every December-bearing artifact —
> a **second** narrowing in this unit's G-2 scans, alongside DISC-2's textual literal scan.
> Widening it is this unit's change to make; it is not made here.
>
> **Repeated a third time**, after the seventh reviewer pass on `external-products`. **This
> unit was untouched by all three redos.**
>
> **And a fourth redo 2026-09-04**, to repair two Majors in `target-standardization`. **This unit was untouched by all four.**
>
> **And a fifth re-save 2026-09-04 — not a redo.** This stage's final pass ran on another clone
> of this repository, rooted at a different absolute path; the engine's completion check matches
> each artifact against the path recorded in its write receipt, so those confirmed writes are
> unreachable from this clone. The consolidated summary confirmation of `2026-09-04T14:07:47Z`
> **stands and was not re-asked** — its questions-file digest still verifies. This paragraph is
> the native-tool write that re-registers the artifact here. **DISC-1 and DISC-2 stand exactly
> as recorded, and no status claim is altered by this note.**

> ## ⚠ WRITTEN AGAINST THE WORKSPACE AS IT IS ON 2026-09-01, NOT AGAINST UPSTREAM'S STATUS CLAIMS
>
> The owner ruled on 2026-09-01 that this design be written against **current workspace
> state**, that this unit's questions file be corrected, and that **`nfr-requirements` be
> left unchanged**. So the upstream artifacts still carry status claims this document
> contradicts, **by instruction, not by oversight** — the divergences are enumerated in
> § SD-G-00 below.
>
> **What is built:** `src/data/locked_test.py` (`open_restricted` at line 147,
> `assert_no_december_outside_restricted`), `src/data/config.py`, `src/data/release.py`,
> and **six test modules** — `test_acquisition_window.py`, `test_locked_test_guard.py`,
> `test_merge_script_restricted_reads.py`, `test_phase_boundary.py`,
> `test_release_contract.py`, `test_release_hashes.py`.
>
> **What is not:** `src/data/registry.py`, `src/data/reuse_registry.py`, `configs/`,
> `pyproject.toml`, `requirements.txt`. **TC-06's scaffold precondition remains unmet.**
>
> **On the test run — read the caveat with the number.** `python -m pytest tests/ -q`
> returned **277 passed, 2 skipped in 4.39s** on 2026-09-01. It ran under **Python 3.14.7
> with pytest 9.1.1**. **TE §8.1 and TC-03d pin Python 3.11 exactly**, and no
> `requirements.txt` exists to pin pytest against. **This is not governed evidence** — it
> establishes that the modules are executable and internally consistent, and **nothing
> about TA-03, the §13.1 environment lock, WS-18, TA-18, TA-27 or TA-28**.
>
> **The test run appended 121 rows to `evidence/test_run_access_log.jsonl`, and that is
> recorded here rather than left to a `git status`.** The routed suites read restricted
> content, so the chokepoint logged every access — each row carrying
> `locked_test_accessed: true`, `purpose: coverage_audit`, `performance_inspected: false`,
> and a guard-stamped `logged_at_utc`. **This is § SD-G-01's mechanism working**, and the
> log is append-only, so NFR-AUD-01 is satisfied in form.
>
> Two things follow. The rows came from an **off-pin** run and are **not governed
> evidence**. And they were **not deleted to tidy up after the run**: deleting access
> records is precisely what this guard exists to prevent, and `project.md` forbids
> back-filling a registry to clear entries. The owner was told and left them standing.
>
> **The row count is derived, not asserted.** `evidence/test_run_access_log.jsonl` went
> from **37 rows at HEAD to 158** in the working tree; `git diff --stat` reports
> **`121 insertions(+), 0 deletions`**. The append-only claim is that diff, not an
> intention — and an independent reviewer re-derived both figures on 2026-09-01 rather than
> taking them from this banner.
>
> **G-09 is signed (D-31) with its own preconditions UNMET**; **stage 3.1 remains FAIL**.
> **What the 121 rows do and do not evidence.** They show the chokepoint **fired on every
> restricted read the suite performed**, logged before the read, with a guard-stamped
> timestamp. That is the first execution evidence for § SD-G-01's ordering rule. They
> evidence **nothing about WS-18 or TA-18**, which require the guard test **and** an
> access-log sample **under the governed environment** — and this run was off-pin.
>
> **No scientific value is decided here.** TE §18.2's absolute rule stands.

## Sources

- `nfr-requirements/security-requirements.md` — **SEC-G-01** … **SEC-G-06**. Consumed as the requirement set; its **status claims** are superseded by § SD-G-00.
- `nfr-requirements/tech-stack-decisions.md` — **TS-G-01** (no new dependency), **TS-G-02** (AST with constant folding), **TS-G-03** (digest technique), **TS-G-04** (platform posture).
- `functional-design/business-logic-model.md` — **W-8**/**W-8a** (December-hit definition; scanning outside the restricted root), **W-10** (one path in, and who may use it), **W-11**.
- **The workspace itself, read on 2026-09-01** — `src/data/locked_test.py`, `tests/test_locked_test_guard.py`, `tests/test_release_hashes.py`, `tests/test_acquisition_window.py`, and the pytest run recorded above. Primary evidence for every status claim in this document.
- `../../foundation/nfr-design/security-design.md` — **§ SD-03**, whose durability posture this design deliberately diverges from at § SD-G-01.
- `../../../inception/requirements-analysis/requirements.md` — **FR-P1-05-12** *(added 2026-09-04 on adversarial finding 1, Critical: this is SD-G-01's actual requirement, carrying `WS-18, TA-18`, and it was absent from this artifact entirely)*, **FR-P1-02-3** *(rows corrected to `WS-18, TA-25`)*, **FR-P1-02-6**, **FR-P1-03-2**, **FR-P1-06-1** … **FR-P1-06-4**, **REQ-ENG-5**, **NFR-AUD-01**, **NFR-PHASE-01**, **NFR-LIC-01**.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§7.0** (the Phase 1 hard prohibition), **§7.0B** (the phase transition), **§10.1** (the code-reuse register), **§12**, **§18.2–18.3**, **§19** (TA-18, TA-27, TA-28), **§16** (WS-18).
- `evidence/DECISIONS.md` — **D-15** (the restricted relocation), **D-18**, **D-31**.
- `nfr-design-questions.md` — Q1 = A, Q2 = A, Q3 = A, Q4 = A, and the receipted Consolidated Summary Confirmation.

---

## SD-G-00 — Where this design contradicts its own upstream, and why

Three upstream status claims are **false as of 2026-09-01**. They are listed here rather
than corrected upstream, because `project.md` forbids editing a completed stage's artifact
to match a later finding and the owner ruled the same way.

| Upstream claim | Actual state | Consequence for this design |
|---|---|---|
| *"the one-door property is **BREACHED** at two named sites"* | **Remediated.** Both sites import `AccessRecord, open_restricted` and read through a `_read_guarded` helper. | § SD-G-01 designs a **built** chokepoint, not an owed one. |
| *"`open_restricted` does not exist"* | **Exists**, `src/data/locked_test.py:147`. | Its actual contract is designed against, below. |
| *"no Python interpreter exists"* | **Python 3.14.7** present; pytest installed 2026-09-01. | The suite is **executable but off-pin** — see the banner. |

**Two discrepancies run the other way — the implementation is weaker or wider than the
design, and both were found by reading the code rather than by any review.**

> ### ⛔ DISC-1 — The exempt list has SEVEN members on disk, not six
>
> `tests/test_locked_test_guard.py:287` enumerates: `src/data/locked_test.py` (the
> chokepoint), `scripts/merge_coverage_year.py`, `tests/test_acquisition_window.py`,
> `tests/test_phase_boundary.py`, `tests/test_release_hashes.py`,
> `tests/test_locked_test_guard.py`, and **`tests/test_merge_script_restricted_reads.py`**.
>
> Every upstream artifact says **six counting the chokepoint**. The seventh was added
> **2026-08-28**, and the code comment records why: *"THIS ASSERTION CAUGHT IT on first
> run, which is the behaviour R-28 specifies: a new holder fails rather than being
> silently admitted."*
>
> **This is the mechanism working, and the count being stale is the cost of it working.**
> The number in the design documents was correct when written and is now one behind the
> boundary it describes. **Owed to the human at the gate**; `nfr-requirements` is not
> edited.

> ### ⛔ DISC-2 — The literal scan is textual, not AST-based, so the gap Q2 = B closed is open
>
> `nfr-requirements` Q2 = B fixed the check as **AST-based with constant folding**,
> specifically so a path assembled from joined literals —
> `EVIDENCE_DIR / ("locked_test" + "_restricted")` — is caught.
>
> The implementation at `tests/test_locked_test_guard.py:307` is
> `if "locked_test_restricted" in text` over `module.read_text(...)`. **A substring check
> cannot catch a concatenated literal**, because the joined string never appears in the
> source text. The exact evasion AST-plus-constant-folding was chosen to close **is open**.
>
> **This is a design-versus-implementation gap, not a design change.** The requirement
> stands as written; the code does not yet meet it. Recorded here, **owed at 3.5**, and
> **no artifact may describe the literal scan as AST-based** until it is.

---

## SD-G-01 — The chokepoint is built, and its durability is `fsync`, not intention

**As built** (`src/data/locked_test.py:147`). `open_restricted(path, *, record, registry)`
appends the `AccessRecord`, **`os.fsync`s it**, and only then returns the resolved path
for the caller to read. Three properties are already enforced in code:

1. **It refuses ordinary paths.** A path not under `RESTRICTED_ROOT` raises
   `LockedTestError`. The module's own reasoning: *"a guard that accepts anything stops
   being evidence that restricted reads went through it."*
2. **The boundary is derived from the module's own location**, not from the caller —
   *"so a caller cannot relocate the boundary by passing a different root."*
3. **A failed log write aborts the read.** The `OSError` branch raises rather than
   proceeding unlogged: *"the read is aborted rather than performed unlogged."*

**Durability is `os.fsync`** — the module states why: *"A row sitting in the OS page cache
when the process dies is a read that happened with no record of it."*

**`logged_at_utc` is stamped by the guard, never by the caller**, immediately before the
fsync. The code records the defect that produced this field: on 2026-08-28 the first
routed run produced **37 rows** whose `retrieved_at_utc` was the same caller-supplied
placeholder, *"leaving FR-P1-02-3's ordering requirement unverifiable from the log it is
recorded in."* A field the caller controls cannot evidence that the log preceded the read.

### The design decision (Q1 = A) — refuse where the platform's durability is uncharacterised

**`open_restricted` fails closed on a platform whose durability semantics are
uncharacterised.** `fsync` is a syscall whose guarantee is a property of the filesystem
beneath it, and **Kaggle's is characterised nowhere in this project**.

> **This diverges deliberately from `foundation` § SD-03**, which stamps a registry row
> *"durability unverified on this platform"* and lets the gate refuse it. The asymmetry is
> the reason, stated so the two sibling units do not read as inconsistent:
>
> **A registry row records what a run did; an `AccessRecord` is the only evidence that the
> locked test was opened at all.** A lost registry row can be reconciled against the run's
> other artifacts. A lost `AccessRecord` leaves **no trace of the access** — which is
> exactly why SEC-G-02 requires orphan detection **in both directions**. A stamped record
> is a record that **might not exist**, and for the December lock that is the failure the
> guard exists to prevent.

> **⚠ The cost is a scheduling dependency, not a footnote.** This **blocks the required
> pre-G-05 December coverage audit on Kaggle** until **W-6 step 8's durability
> measurement** is done. That audit is a **precondition of G-05** (Vision §8.3), so the
> measurement is on the critical path. **Choosing this is choosing to measure first.**

> **⚠ What is NOT discharged.** `tests/test_locked_test_guard.py` (16 tests) passes
> **off-pin**, under Python 3.14.7. **WS-18 and TA-18 remain `Pending`** — they require the
> guard test **and an access-log sample** under the **governed** environment.

## SD-G-02 — The access record joins the registry, and the registry does not exist

**Requirement (SEC-G-02, NFR-AUD-01 — rows TA-10 and TA-21, both).** `AccessRecord` and
`RegistryEvent` join on `run_id` with **orphan detection in both directions**. The five
retrospectively logged December accesses, and the **one possible unauthorized access
`GOV-2026-08-28-FD-01` Recommendation 31 records as expressly unresolved**, are **known
pre-guard orphans**. **No registry row is ever back-filled to clear them.**

> **⚠ Half of this join has no implementation.** `AccessRecord` exists and is written.
> **`src/data/registry.py` does not exist**, so `RegistryEvent` has no producer and the
> **orphan detection cannot run in either direction today**. The half that is built writes
> records nothing yet reconciles. **This is a two-half contract with one half missing**,
> and this design does not describe it as satisfied from the built side.

## SD-G-03 — The exempt list is a source constant, and TC-03e does not reach it

**Design (Q2 = A).** The exempt list is a **module-level constant in the guard**, with
membership **asserted exactly** by a test — which is how it is already implemented.

**Why not a governed config.** The criterion applied was **"what does it take to widen
this?"** A source constant requires a code change plus a test update; a config entry
requires editing a YAML file; a self-marking scheme (a decorator or magic comment) requires
only a comment in the file that wants the exemption — which **inverts the property**,
turning a maintained list into a permission each module grants itself.

**Why TC-03e does not reach it, stated because a reader will assume it does.** TC-03e
governs **scientific constants** — values that change a computed result. A security
allowlist changes **who may name a boundary**, not what any number comes out as. Putting it
in `configs/` would also place it **outside the guard's own scan scope** and make it
editable by anyone editing configuration.

**The list's discipline is proven, not asserted.** DISC-1 above is the evidence: a seventh
holder appeared, and **the membership assertion failed on first run rather than silently
admitting it**. The code comment states the principle exactly — *"an exemption a reader
cannot see is not an exemption, it is a hole."*

> **⚠ Member 5 is `scripts/merge_coverage_year.py` — a production script, not a test.**
> It is the one production path that legitimately merges the locked month (D-18), and
> `tests/test_merge_script_restricted_reads.py` (6 tests) pins its routing through the
> chokepoint. A production entry in a test-shaped allowlist is exactly the kind of member
> that should be hard to add quietly, which is the argument for Q2 = A in one line.

## SD-G-04 — Two scans, two failures, one shared fail-closed rule

**Design (Q3 = A).** The **literal scan** and the **residency scan** are **independent**,
each with its own entry point and its own failure.

| Scan | Question it asks | Implemented as |
|---|---|---|
| **Literal** | Who may **name** the restricted root | `test_locked_test_guard.py:277` — **textual today; see DISC-2** |
| **Residency** | Has **December content escaped** the root | `assert_no_december_outside_restricted` in `src/data/locked_test.py` |

**Why independent.** They have different hit definitions and different failures. The
decisive reason: **`FR-P1-02-6` carries no §16 or §19 acceptance row at all**, so the
residency scan has **no evidence obligation attached to it** — and coupling a check that
has one to a check that has none invites the rowless check to ride on the other's evidence.

**R-27's unparseable-is-a-failure rule is one helper both call.** That captures the real
benefit of a shared traversal — a single place where the rule lives, so the two cannot
drift apart on it — without coupling the scans themselves.

**The residency scan is recursive by construction, and the code says why.** *"`DATA-01`
showed a non-recursive glob silently stopped checking the artifacts that matter most, and
D-15 relocated 21 files."* A guard whose traversal is shallower than the thing it guards
reports a cleanliness it never checked.

## SD-G-05 — The phase boundary runs on two limbs, and one of them is unbuilt

**Requirement (SEC-G-05, NFR-PHASE-01, TE §7.0).** `RAW_MODULES` is **four** modules —
`rinex`, `calibration`, `target`, `verification` — corrected under finding `IMPL-2` from
FR-P1-03-2's earlier two-module wording.

**Both limbs run and neither substitutes for the other** (R-23): the **import** limb and
the **produced-field** limb. `assert_no_raw_fields` is called by **each of the eight Phase 1
producing scripts before it writes**, with a **completeness test asserting every one of
them calls it**.

**Requirement (TE §7.0B, gate G-P3C).** Phase 2 **refuses to train if any protected hash
differs**. Phase 1 fitted weights are **never** carried into Phase 2, and **no Phase 1
result may motivate a Phase 2 model or evaluation change**, absent a separately approved,
exploratory-labelled transfer-learning experiment.

> **⚠ Only the import limb exists.** `tests/test_phase_boundary.py` (53 tests) walks `src/`
> and `scripts/` with `ast`. **`assert_no_raw_fields` appears nowhere in the workspace** —
> a grep across `src/` and `tests/` returns nothing — and **none of the eight producing
> scripts exists**, so the completeness test has nothing to assert over. **The
> produced-field limb is specified and unbuilt**, and R-23's "neither substitutes for the
> other" means the built limb **does not** cover for it.
>
> **TA-27 and TA-28 are `Pending`.** TA-27 needs the phase-boundary test **and** a
> transition-manifest hash-diff test; **`diff_protected_hashes` does not exist**.

## SD-G-06 — Reuse is registered before use, and the register is unbuilt

**Requirement (SEC-G-06, TE §10.1, NFR-LIC-01, gate G-P2).** Any reused or materially
adapted third-party source is recorded in the §10.1 register **before the code is used**,
with the full field set — `reuse_id`, repository URL, immutable commit or tag, upstream
file and line or function, retrieval date, licence and SPDX ID, copied-versus-adapted
status, destination file, scientific purpose, modifications, tests, original citation,
notice location, reviewer, approval date.

**Reimplementation is the standing default**, not a fallback: third-party source whose
licence is **absent, ambiguous or incompatible** is not copied or materially adapted —
reimplement from the paper with a citation. The AGPLv3 Global-TEC-forecasting repository is
the one approved direct-copy source today, and **whether its repository-distribution
obligations permit that copying is a governance dependency this project does not resolve on
its own**.

> **⚠ `src/data/reuse_registry.py` and `tests/test_reuse_registry.py` do not exist.**
> **G-P2 is unaffected by G-09's signature.**

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| **FR-P1-05-12** | SD-G-01 | **WS-18, TA-18** | `Pending` — guard built, passes **off-pin only**; **row owned by `features-and-splits`, this unit supporting** |
| **FR-P1-02-3** | SD-G-01 | **WS-18, TA-25** — **row owned by `inventory-and-registry`** (`unit-of-work-story-map.md`; TA-25 is that unit's), WS-18 `features-and-splits`'; **this unit supporting via `open_restricted`** | `Pending` — SD-G-01's log-then-read ordering is what makes this requirement's ordering **verifiable**; the guard is built and passes **off-pin only** *(owner label added 2026-09-04 on iteration-2 Major: the corrected row had stated no cross-unit ownership while its sibling rows did, though the story map gives it the identical split shape)* |
| **FR-P1-02-6** | SD-G-04 | ⚠ **NO ACCEPTANCE ROW** | untested by any §16/§19 row |
| FR-P1-03-2 | SD-G-05 | TA-27 | `Pending` — **import limb only** |
| REQ-ENG-5 | SD-G-05 | WS-10, TA-07, TA-08, TA-12, TA-27 | `Pending` |
| FR-P1-06-1 | SD-G-05 | TA-27 | `Pending` |
| FR-P1-06-2 | SD-G-05 | TA-27 | `Pending` |
| FR-P1-06-3 | SD-G-06 | TA-28 | `Pending` |
| FR-P1-06-4 | SD-G-06 | TA-28 | `Pending` |
| **NFR-PHASE-01** | SD-G-05 | TA-27 | `Pending` |
| **NFR-LIC-01** | SD-G-06 | TA-28 | `Pending` |
| **NFR-AUD-01** | SD-G-02 | **TA-10, TA-21** — both rows, owned by `foundation`/`inventory-and-registry` | `Pending` — **one half unbuilt** |

**Derived and printed**: 7 design sections (SD-G-00…SD-G-06); **12** coverage rows —
counted directly from the table above, **not** read off `nfr-requirements`' table or this
unit's `functional-design` map. **0** rows claimed satisfied; **0** acceptance rows
discharged; **1** requirement with **no acceptance row at all** (FR-P1-02-6).

> ### ⚠ CORRECTED 2026-09-04 on adversarial finding 1, **Critical** — 11 → 12 rows
>
> **SD-G-01's requirement was mis-cited, on the design's own centerpiece section.** The
> superseded row read `| **FR-P1-02-3** | SD-G-01 | **WS-18, TA-18** |`, and **both halves were
> wrong**:
>
> - `requirements.md` gives **`FR-P1-02-3`** the rows **`WS-18, TA-25`**. `TA-18` never appears
>   against it.
> - **`TA-18` belongs to `FR-P1-05-12`** — *"the locked-test guard blocks December performance
>   execution before G-05 is signed, records every access… predictions hashed before any
>   metric"* — which is SD-G-01's subject matter word for word, and which was **absent from
>   both coverage tables entirely** (zero grep hits).
>
> **This unit's own upstream already had it right**, which is what makes this a carry-forward
> failure rather than a fresh error: `domain-entities.md` traces `AccessRecord` /
> `RESTRICTED_LITERAL_EXEMPT_MODULES` to `FR-P1-05-12` (`WS-18, TA-18`, owner
> `features-and-splits`, this unit *supporting*), and `nfr-requirements`'
> `security-requirements.md` independently states the same mapping. This stage failed to carry
> it forward.
>
> **Both rows are kept rather than one dropped.** `FR-P1-05-12` is the row SD-G-01 actually
> serves, and **`FR-P1-02-3` genuinely depends on the same mechanism** — SD-G-01's
> durable-log-before-read ordering is what makes FR-P1-02-3's ordering requirement verifiable
> from the log at all, which this document already stated in § SD-G-01. Dropping it would
> lose a real dependency; leaving it mis-rowed would keep a false citation. So it stays with
> its **correct** rows, `WS-18, TA-25`.
>
> **`FR-P1-05-12` is not claimed as discharged from this side** — the row is
> `features-and-splits`', and this unit supports it.
>
> **What five prior passes missed, stated so the check can be fixed rather than repeated.**
> Every earlier re-derivation verified the coverage table's **ID-set completeness** — does the
> union of cited IDs cover `requirements.md`'s relevant ID space — and **never checked that
> each ID's cited acceptance row matches that ID's own row in `requirements.md`**. A set-union
> check cannot see a correctly-listed ID carrying another requirement's row. The passages in
> the prior `## Review` sections that report this pairing as independently re-verified are left
> standing as the reviewers' own record; they were true about the check they ran.

**The ID set was set-differenced against `requirements.md` before this table was written**,
not after — the omission of that step is what produced a Critical on `foundation`'s
first pass at this stage.

## Assumptions & Open Questions

- **[DISC-1 — owed at the gate]** The exempt list has **seven** members on disk against **six** in every upstream artifact. The mechanism worked; the documented count is one behind. **`nfr-requirements` is not edited**, per the owner's ruling.
- **[DISC-2 — owed at 3.5]** The literal scan is **textual**, so the **concatenated-literal evasion AST-plus-constant-folding was chosen to close is open**. **No artifact may describe the scan as AST-based** until it is.
- **[Q1 / SD-G-01]** **Kaggle's `fsync` semantics are uncharacterised**, and refusing there **blocks the pre-G-05 December coverage audit on Kaggle** until W-6 step 8's measurement is done. This is a **scheduling dependency on the critical path**.
- **[SD-G-02]** **`RegistryEvent` has no producer.** The orphan detection SEC-G-02 requires **cannot run in either direction today**, and this design does not claim the built half satisfies the contract.
- **[SD-G-05]** **`assert_no_raw_fields` does not exist**, and **none of the eight Phase 1 producing scripts exists**. The **produced-field limb is unbuilt**, and the import limb does **not** substitute for it.
- **[SD-G-05]** **`diff_protected_hashes` does not exist**, so TA-27's transition-manifest hash-diff half has no implementation.
- **[banner]** **277 passed / 2 skipped is off-pin** — Python **3.14.7**, not the governed **3.11**; no `requirements.txt` exists to pin pytest. **It is not governed evidence.** The two skips are legitimate: no hourly-target artifact exists yet, and `dataset_version` derivation is covered by the D-29 tests.
- **[carried]** **`configs/`, `pyproject.toml` and `requirements.txt` are all absent**, so **TC-06's scaffold precondition is unmet** and the §18.3 zero-TBD preflight cannot run.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row, install or test as discharged.

## Review — 2026-09-01

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Minor | SD-G-00 DISC-1 / logical-components DISC-1 | The seven-member exempt-list claim was spot-checked against `tests/test_locked_test_guard.py` (the `test_restricted_literal_holders_are_exactly_the_enumerated_exemption` function, the `exempt = {...}` literal, and the code comment quoted verbatim in the artifact — *"THIS ASSERTION CAUGHT IT on first run"*) but the full seven-item enumeration was not re-derived line-by-line under this review's tool budget; only the tail entry (`tests/test_merge_script_restricted_reads.py`) and the surrounding mechanism were directly observed. | No action required to reach READY; a future pass with more budget should re-print the full `exempt` set to close this out completely. |
| 2 | Minor | SD-G-00 (upstream row) / logical-components diagram | Claim 5 ("both formerly breached sites now route through the chokepoint via a `_read_guarded` helper") could not be directly confirmed: `_read_guarded` does not appear in `src/data/locked_test.py` or `tests/test_locked_test_guard.py` (the only files this review had scope to grep), which is consistent with the helper living in the caller sites (e.g. `scripts/merge_coverage_year.py`) rather than in the chokepoint module itself — outside this review's named read scope. Not a defect finding; a scope limitation of this pass. | State explicitly in the artifact (or at the gate) which file(s) define `_read_guarded`, so a future reviewer with the same scope bound can confirm it without needing extra access. |

### Claims verified against code (this review's primary check)

1. **`open_restricted` contract** — confirmed at `src/data/locked_test.py:147`. Docstring and body confirm: raises `LockedTestError` for a path not under `RESTRICTED_ROOT`; `RESTRICTED_ROOT` is derived from `repo_root` inside the module (not caller-supplied); the registry-write branch is documented as aborting the read on failure; `os.fsync(handle.fileno())` is called (line 143); `row["logged_at_utc"]` is stamped by the guard (line 138), before the fsync, never by the caller. **Matches the artifact's claim exactly.**
2. **DISC-1 (seven exempt members)** — corroborated by the named test function, the `exempt = {...}` set, and the code comment quoted verbatim in the artifact. Full recount not completed under this pass's budget (see Minor #1).
3. **DISC-2 (textual, not AST-based scan)** — confirmed: `tests/test_locked_test_guard.py` contains `if "locked_test_restricted" in text` inside the literal-holder scan, over `module.read_text(...)`. This is a substring check, not an AST/constant-folding check, matching the artifact's claim that a concatenated literal (`"locked_test" + "_restricted"`) would not be caught since the joined string never appears in source text.
4. **`assert_no_raw_fields` / `diff_protected_hashes` absent** — grep across the five named files (`src/data/locked_test.py`, `tests/test_locked_test_guard.py`, `tests/test_release_hashes.py`, `tests/test_acquisition_window.py`, `tests/test_phase_boundary.py`) returned zero matches for either symbol, confirming both do not exist in the built code this review could inspect. Consistent with the artifact's claim that R-23's produced-field limb is unbuilt.
5. **Chokepoint routing at both formerly-breached sites** — not independently confirmed (see Minor #2); the artifact's claim is plausible and internally consistent but rests on files outside this review's read scope.

### Also verified

- **Q1 = A divergence from `foundation` § SD-03** is stated explicitly in SD-G-01 with the asymmetry reasoning (reconcilable registry row vs. irrecoverable `AccessRecord`) and the scheduling-dependency cost (blocks the pre-G-05 December coverage audit on Kaggle until W-6 step 8) — present as required.
- **Q2 = A** — exempt list as a module-level source constant, with an explicit "why TC-03e does not reach it" argument (TC-03e governs scientific constants, not security allowlists) — present in SD-G-03 and the shared-resources section of `logical-components.md`.
- **Q3 = A** — two independent scans (literal vs. residency), R-27's unparseable-is-a-failure rule named as the one shared helper, and the decisive reason (`FR-P1-02-6` has no acceptance row) — present in SD-G-04 and G-2.
- **Q4 = A** — component boundary drawn on enforcement timing (R-24: static = early warning, run-time = authoritative), explicitly argued against a "what is guarded" alternative, and R-23's "neither limb substitutes for the other" is stated as visible in the G-1/G-2 boundary itself rather than hidden by it.
- **Off-pin caveat** travels with every test-run claim in both artifacts' banners and `## Assumptions & Open Questions` sections (Python 3.14.7 vs. governed 3.11, no `requirements.txt`, "not governed evidence").
- **Mermaid diagram** in `logical-components.md` parses correctly (valid `graph TD` syntax) and its text fallback matches, including the dotted `G2 -.-> ROOT` edge labelled "names only, never reads content," which correctly encodes D-15/R-28's distinction that holding the literal is not itself an access.
- **Requirement coverage set-difference**: both artifacts cite the identical 11-ID set (`FR-P1-02-3`, `FR-P1-02-6`, `FR-P1-03-2`, `FR-P1-06-1..4`, `NFR-AUD-01`, `NFR-LIC-01`, `NFR-PHASE-01`, `REQ-ENG-5`). Cross-checked against the full ID space in `requirements.md` (grep-derived, printed above) — no `NFR-*`, `FR-P1-*`, `FR-WS-*`, or `REQ-ENG-*` ID relevant to a locked-test/phase-boundary/reuse-register security scope was found missing from the cited set. `NFR-AUD-01` carries both `TA-10` and `TA-21` in both artifacts, not a truncated single row. The 6-shared/5-security-only/0-here-only decomposition was independently re-derived from the printed ID lists (not accepted on arithmetic alone) and it holds: 6 + 5 = 11, matching the printed total in both documents.
- **Not reported as newly discharged**: `configs/`, `pyproject.toml`, `requirements.txt` absence; `src/data/registry.py` and `src/data/reuse_registry.py` absence; WS-18/TA-18/TA-27/TA-28 `Pending`; `FR-P1-02-6` with no acceptance row; G-P2 unaffected by G-09; G-09 signed with preconditions unmet; stage 3.1 FAIL — all correctly carried as open/unresolved in both artifacts, matching this brief's do-not-report-as-discharged list.

### Summary

Both artifacts are unusually self-auditing: every "what is built vs. not" claim checked against the five named source/test files matched the code exactly, including the two discrepancies the design flags as running the other way from upstream (DISC-1's seven-member exempt list, DISC-2's textual-not-AST literal scan). The requirement-coverage decomposition was independently re-derived rather than trusted on its printed arithmetic, and it is sound. No circular dependency, no broken cross-reference, and no requirement silently dropped from the cited ID set was found. The two Minor findings are scope-of-verification notes (the exempt-list recount and the `_read_guarded` site), not defects in the artifacts themselves, and do not block READY.

READY

## Review — 2026-09-01 post-correction

**Scope:** confirming pass over the one paragraph added to this file's banner (lines ~29–34), recording the test-run's write of 121 rows to `evidence/test_run_access_log.jsonl`, plus a re-check of the two Minor items left open by the prior pass. Everything else in the artifact is unchanged from the 2026-08-30 READY pass above and is not re-litigated here.

### The added paragraph, verified against the workspace

1. **Rows exist with the claimed fields.** `evidence/test_run_access_log.jsonl` currently holds 158 lines; every line parses as JSON and every line carries `locked_test_accessed`, `purpose`, `performance_inspected`, and `logged_at_utc`. Sampled rows show `locked_test_accessed: true`, `purpose: "coverage_audit"`, `performance_inspected: false`, and a guard-stamped `logged_at_utc` timestamp — matches the banner's claim.
2. **121 is the right added count, and it is derivable, not asserted.** `git show HEAD:evidence/test_run_access_log.jsonl | wc -l` = 37 (the pre-run baseline); the working tree has 158; `git diff --stat` on the file independently reports `121 insertions(+)`, `0 deletions`. 158 − 37 = 121, and the diff stat corroborates it from a second, independent method. The banner's figure is confirmed by derivation, not accepted on its own say-so, per `project.md`'s count-derivation rule.
3. **Append-only claim is consistent with the diff.** `git diff --stat` shows insertions only (0 deletions, 0 modifications) — no existing row was rewritten or removed by the run. This is exactly what "append-only, so NFR-AUD-01 is satisfied in form" requires and the git evidence supports it.
4. **"Not deleted" is the right call.** The 121 rows are off-pin test-suite exhaust (Python 3.14.7, not the governed 3.11 pin) rather than governed evidence, but they are still `AccessRecord`-shaped log entries asserting `locked_test_accessed: true`. Deleting or truncating them to tidy the log would itself be the exact failure mode SEC-G-01/NFR-AUD-01 exist to catch (a silently vanished access record), and `project.md`'s Forbidden section bars exactly this class of registry back-filling. Leaving them in place, labelled off-pin and non-governed in the banner text, is the correct governance call — the alternative (deleting them) would be a worse violation than the noise it removes.

### Re-checked Minor items from the prior pass

- **DISC-1 (exempt-list count).** `tests/test_locked_test_guard.py` line 287's `exempt = {...}` literal was counted directly: `locked_test.py`, `merge_coverage_year.py`, `test_acquisition_window.py`, `test_phase_boundary.py`, `test_release_hashes.py`, `test_locked_test_guard.py`, `test_merge_script_restricted_reads.py` — **seven entries**, confirmed, including the 2026-08-28 addition with its own inline rationale comment. This closes the prior pass's Minor #1 as confirmed, not merely corroborated.
- **Claim 5 (`_read_guarded` at both formerly-breached sites).** Confirmed present: `tests/test_release_hashes.py:96` and `tests/test_acquisition_window.py:88`, one function definition per file, each used by that file's guarded read calls (`test_release_hashes.py:140,284,312`; `test_acquisition_window.py:163`). This closes the prior pass's Minor #2 as confirmed — no Critical arises, since § SD-G-00's remediation claim is substantiated.

### Coverage completeness — unaffected

The access-log write discharges nothing and no coverage row's status drifted: `NFR-AUD-01` still shows `Pending — one half unbuilt` (line 283, `TA-10, TA-21` both), and the 11-ID set-difference (`FR-P1-02-3`, `FR-P1-02-6`, `FR-P1-03-2`, `FR-P1-06-1..4`, `NFR-AUD-01`, `NFR-LIC-01`, `NFR-PHASE-01`, `REQ-ENG-5`) against `requirements.md`'s full ID space stands unchanged from the prior pass. Not-newly-discharged list (WS-18/TA-18/TA-27/TA-28 `Pending`, `FR-P1-02-6` no acceptance row, G-P2 unaffected by G-09, G-09 preconditions unmet, stage 3.1 FAIL) is unchanged and correctly still carried as open.

### Findings

No new findings. Both items the prior pass flagged as Minor (budget-limited, not defects) are now independently confirmed rather than merely corroborated, and the added paragraph's every factual claim (row count, field shape, append-only-ness, the deliberate non-deletion) checks out against the evidence file and git history.

### Summary

The added banner paragraph is accurate on every checkable point: 121 is the correct, independently-derivable added-row count; the log's append-only claim matches what git shows; the fields match what the code stamps; and declining to delete the off-pin rows is the governance-correct call, not an oversight. The two previously-open Minor items are now confirmed rather than open. No Critical or Major findings. READY stands.

READY

## Review — 2026-09-01 final confirming pass

**Scope:** confirming pass over the redo-jump re-recorded confirmation and the one added paragraph in each of `security-design.md` (banner, lines ~29–34/48–54) and `logical-components.md` (banner, lines ~13–17). Everything else is unchanged from the 2026-08-30/09-01 READY passes above and is not re-litigated.

### The two added paragraphs — verified against code and evidence

1. **`security-design.md`'s scope-bound paragraph.** Confirmed: `open_restricted` (`src/data/locked_test.py:147`) writes `row["logged_at_utc"]` immediately before `os.fsync(handle.fileno())` (guard-stamped, never caller-supplied — code and docstring both confirm this at the lines read above), so the 121 rows are first execution evidence of § SD-G-01's ordering rule firing on every restricted read. The paragraph's negative claim — the rows evidence **nothing about WS-18 or TA-18** because those rows require the guard test **and** an access-log sample **under the governed environment**, and this run is off-pin — is consistent with the banner's own Python 3.14.7-vs-3.11 disclosure and is not contradicted by anything in the coverage table (both rows still `Pending`). The derived-count sub-claim (37 → 158, `git diff --stat`: 121 insertions(+), 0 deletions) is independently re-derived below and holds exactly.
2. **`logical-components.md`'s G-1/G-2/G-3 attribution paragraph.** Confirmed: the execution evidence is scoped to **G-1 only**. Nothing in the 121 rows touches G-2's scans (whose specified weakness remains DISC-2, confirmed live below) or G-3, which — confirmed by grep — has no `src/data/reuse_registry.py` or `tests/test_reuse_registry.py` on disk. The paragraph's claim that this attribution is exactly what an enforcement-timing boundary makes legible is consistent with G-4's stated boundary criterion (Q4 = A) elsewhere in the same artifact.

### Standing checks re-verified against code (this pass, independently)

- **DISC-1 — seven entries, not six.** `tests/test_locked_test_guard.py`'s `exempt = {...}` literal was read directly this pass: `src/data/locked_test.py`, `scripts/merge_coverage_year.py`, `tests/test_acquisition_window.py`, `tests/test_phase_boundary.py`, `tests/test_release_hashes.py`, `tests/test_locked_test_guard.py`, `tests/test_merge_script_restricted_reads.py` — **seven**, matching the artifact exactly, including the inline 2026-08-28 rationale comment quoted verbatim in both artifacts.
- **DISC-2 — textual, not AST-based.** `tests/test_locked_test_guard.py:308` reads `if "locked_test_restricted" in text:` — a substring check over `text`, not an AST/constant-folding check. A concatenated literal (`"locked_test" + "_restricted"`) would not appear in `text` and would not be caught. Matches both artifacts' claim exactly.
- **`open_restricted` contract.** Confirmed at `src/data/locked_test.py:147`: refuses paths not under `RESTRICTED_ROOT`; the boundary is derived from the module's own location; a failed registry write aborts the read (raise, not silent-continue); durability is `os.fsync`; `logged_at_utc` is guard-stamped before the fsync, never caller-supplied. All five properties match both artifacts' claims verbatim.
- **`assert_no_raw_fields` / `diff_protected_hashes` absent.** `grep -rn` across `src/`, `tests/`, and `scripts/` returns zero matches for either symbol. Confirms R-23's produced-field limb remains unbuilt, as both artifacts state.
- **`_read_guarded` at both formerly-breached sites.** Confirmed present and used: `tests/test_acquisition_window.py:88` (used at line 163) and `tests/test_release_hashes.py:96` (used at lines 140, 284, 312). Substantiates § SD-G-00's remediation claim.
- **Evidence-log derivation, re-run independently.** `git show HEAD:evidence/test_run_access_log.jsonl | wc -l` = **37**; current working-tree `wc -l evidence/test_run_access_log.jsonl` = **158**; `git diff --stat -- evidence/test_run_access_log.jsonl` reports **121 insertions(+), 0 deletions** as its own line, with no modified/deleted lines. 158 − 37 = 121, corroborated by the independent diff-stat method. The 37 → 158 / 121-insertions figures **hold exactly** — not a Major finding.

### Coverage completeness — unaffected, re-checked

No row's status has drifted. `NFR-AUD-01` in `security-design.md`'s table still reads `Pending — one half unbuilt` (`TA-10, TA-21`, both rows); the mirrored row in `logical-components.md` is identical. The 11-row (security-design) / 6-row (logical-components) decomposition — 6 shared + 5 security-only + 0 here-only — was re-derived by reading both tables' ID columns directly rather than accepted on the printed arithmetic, and it holds: `FR-P1-02-3, FR-P1-02-6, FR-P1-03-2, NFR-PHASE-01, NFR-AUD-01, NFR-LIC-01` are the six shared rows in both tables; `REQ-ENG-5, FR-P1-06-1, FR-P1-06-2, FR-P1-06-3, FR-P1-06-4` are security-design-only. `FR-P1-02-6` still carries no acceptance row in either artifact.

### Not reported as newly discharged (per the brief's list — confirmed still true)

`configs/`, `pyproject.toml`, `requirements.txt` absent (confirmed by the earlier "what is not built" banner and unchanged by this pass's checks); `src/data/registry.py`, `src/data/reuse_registry.py` absent (confirmed by grep — G-3 unbuilt). WS-18, TA-18, TA-27, TA-28 remain `Pending` in both tables. `FR-P1-02-6` has no acceptance row. G-P2 is stated as unaffected by G-09's signature. G-09 is signed (D-31) with its own preconditions UNMET, and stage 3.1 remains FAIL — all carried forward unchanged in both artifacts.

### Findings

No new findings. The redo-jump's re-recorded confirmation and the two added paragraphs introduce no claim that fails verification against the code or the evidence file; both paragraphs' figures and attributions check out exactly under independent re-derivation. No Critical, no Major, no new Minor.

### Summary

This confirming pass independently re-derived every figure and re-read every code location the added paragraphs and the standing checks depend on (the seven-entry exempt set, the textual DISC-2 scan, `open_restricted`'s five enforced properties, the two absent symbols, `_read_guarded` at both sites, and the 37→158/121-insertion evidence-log arithmetic via two independent methods) rather than trusting the prior passes' record of them, per this project's count-derivation and independent-verification practices. Every check matches the artifacts exactly. The scope-bound and component-attribution paragraphs added for this redo are both accurate and add no unverified claim. No Critical or Major findings; READY stands.

READY

---

## Review — 2026-09-02 post-redo confirming pass

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-03T10:10:37Z
**Iteration:** 1 (of 2) — confirming pass after the third `STAGE_JUMPED` redo of `nfr-design`
**Prior verdict:** holds. Zero Critical, one Major (a stale re-derivation *instruction*, not a wrong design claim), two Minor.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `security-design.md` banner (~lines 58–62) and `logical-components.md` banner (~lines 42–45) | The access-log figures are stated as a **live git derivation** — "`git show HEAD:evidence/test_run_access_log.jsonl` = 37 … working tree 158 … `git diff --stat` reports 121 insertions(+), 0 deletions" — and that derivation **no longer reproduces**. On disk today: `wc -l evidence/test_run_access_log.jsonl` = **232**; `git show HEAD:…` = **158**; `git diff --stat` = **74 insertions(+), 0 deletions**. The 37→158/121 transition has since been **committed** (`fb080ed`, `34e8136` both touch this file), and a **further, undocumented run appended 74 more rows** — the last row is stamped `logged_at_utc: 2026-09-02T19:47:27…`, `run_id: test_release_hashes`. The historical event the banner describes did happen; what is stale is the check a reader is told to re-run to confirm it, and the implication that 121 is the total off-pin exhaust now in the log. | Restate the figures as an event fixed to a commit ("the 2026-09-01 run appended 121 rows, now committed; the log has since grown to 232 rows from a later 2026-09-02 run") rather than as a working-tree diff. The append-only property still holds under the new numbers (0 deletions), so the governance conclusion is unchanged — only the arithmetic and its method need restating. |
| 2 | Minor | `security-design.md` § SD-G-04 table; `logical-components.md` ~line 129 | The literal scan is cited as `tests/test_locked_test_guard.py:277`. Line 275 is `def test_restricted_literal_holders_are_exactly_the_enumerated_exemption`, 277 its docstring; the `exempt = {…}` set is at **287** and the substring check `if "locked_test_restricted" in text:` at **308**. The citation points at the function, not at the mechanism DISC-2 is about. | Cite `:308` for the textual check and `:287` for the exempt set, or drop the line number and name the function. |
| 3 | Minor | `security-design.md` banner (~line 41) | "277 passed, 2 skipped in 4.39s on 2026-09-01" was **not re-verified** this pass (no suite run, per the tool budget), and the 74 new log rows are evidence the suite has been run at least once since. The count may have drifted. | Acceptable as a dated historical record; if any later text leans on it as current, re-run and restamp. |

### Checks run

| Check | Method | Result |
|---|---|---|
| `open_restricted` at line 147 | `grep -n` on `src/data/locked_test.py` | **CONFIRMED** — `def open_restricted(...)` at **147** exactly. |
| `os.fsync` durability, guard-stamped `logged_at_utc` | same grep | **CONFIRMED** — `row["logged_at_utc"] = …now(utc)…` at **138**, `os.fsync(handle.fileno())` at **143**; the stamp precedes the fsync and the caller supplies neither. Docstring lines 119–127 state the ordering rule as the artifact quotes it. |
| `assert_no_december_outside_restricted` exists | same grep | **CONFIRMED** — defined at **193**. |
| DISC-1 — exempt list has **seven** members | `sed -n '285,300p' tests/test_locked_test_guard.py`, enumerated and printed | **CONFIRMED, unchanged, not softened.** Seven entries: `src/data/locked_test.py`, `scripts/merge_coverage_year.py`, `tests/test_acquisition_window.py`, `tests/test_phase_boundary.py`, `tests/test_release_hashes.py`, `tests/test_locked_test_guard.py`, `tests/test_merge_script_restricted_reads.py` — the seventh still carrying its 2026-08-28 inline rationale and the "an exemption a reader cannot see is not an exemption, it is a hole" comment quoted in both artifacts. Upstream's six stands contradicted, exactly as recorded. |
| DISC-2 — scan is **textual**, not AST | `grep -n` on `tests/test_locked_test_guard.py` | **CONFIRMED, unchanged, not softened.** Line **308**: `if "locked_test_restricted" in text:` — a substring test over source text. A concatenated literal is still not caught; no AST/constant-folding code has been introduced. |
| Third narrowing (`rglob("*.json")` vs docstring) | `sed -n '193,215p' src/data/locked_test.py` | **CONFIRMED and accurately stated — neither overstated nor understated.** Line **213** iterates `sorted(root.rglob("*.json"))`, while the docstring (194–197) claims it "Walks `evidence/` **recursively** and returns **every** December-bearing artifact found outside the restricted root." The banner's wording — `*.json` only, docstring claims every artifact, a **second** narrowing beside DISC-2, **this unit's G-2 change to make and not made here** — matches the code. The docstring's own "recursive by construction / DATA-01" rationale is about depth, not extension, so the extension gap is genuinely unclosed and correctly owned. |
| `assert_no_raw_fields` / `diff_protected_hashes` absent | `grep -rn` across `src/`, `tests/`, `scripts/` | **CONFIRMED** — zero matches for either symbol. R-23's produced-field limb and TA-27's hash-diff half remain unbuilt, as both artifacts state. |
| Access-log row counts | `wc -l`, `git show HEAD:…`, `git diff --stat` | **STALE** — see Finding 1. 232 / 158 / 74 today against the artifacts' 158 / 37 / 121. The append-only property (0 deletions) still holds. |
| Q4 = A boundary criterion (enforcement timing, mirroring R-24) | read of the boundary section and the G-1/G-2/G-3 attribution paragraphs in both artifacts | **CONSISTENT; the run-time/static distinction is preserved, not blurred.** The 121-row evidence is attributed to **G-1's run-time chokepoint only**; G-2's static scans (DISC-2, plus the `*.json` narrowing) and G-3 (no `src/data/reuse_registry.py`, no `tests/test_reuse_registry.py` — confirmed absent from `tests/`, which holds six modules) are explicitly excluded from it. Nowhere is a run-time result read as discharging a static check, or the reverse. |
| No satisfaction / discharge claim | scan of both `## Assumptions & Open Questions` sections and the coverage table | **CONFIRMED.** The 121 rows are labelled off-pin and "not governed evidence" at every site that cites them. WS-18, TA-18, TA-27, TA-28 remain `Pending`; `NFR-AUD-01` remains `Pending — one half unbuilt`; G-09-signed-with-preconditions-unmet and stage 3.1 `FAIL` are still carried as open. Nothing authorises a module write beyond G-09/D-31. |
| Cross-artifact consistency | targeted grep of `logical-components.md` for every figure and discrepancy claim | **NO ASYMMETRY.** Both banners carry the same 37/158/121 figures (both equally stale, so Finding 1 splits neither way), the same seven-member DISC-1, the same textual DISC-2, the same `*.json` third narrowing, the same off-pin 3.14.7 caveat. The recurring one-artifact-repaired defect did **not** recur here. |
| Python pin | banner claim vs governed 3.11 | Off-pin disclosure present and unaltered; no `requirements.txt` exists to pin pytest. |

### Coverage limits

- The suite was **not re-run** (Finding 3); `277 passed / 2 skipped` is taken as a dated historical record, not re-derived.
- Of the 74 new log rows, only the tail row was sampled; the producing run is inferred from that row's `run_id: test_release_hashes` and `logged_at_utc: 2026-09-02T19:47:27`.
- Read-scope bound honoured: no `construction/<other-unit>/` file was opened, grepped or globbed. The `inventory-and-registry` recording of the `*.json` narrowing was verified **against the code itself**, never against that unit's artifact.
- No governance gate, acceptance row, or supervisor signature was evaluated; those are the human's at the approval gate.

### Summary

The prior READY verdict holds. Every design-bearing claim this unit makes about built code was re-verified against disk and matches exactly — `open_restricted` at line 147, the stamp-then-fsync ordering, the two absent symbols, and both self-reported discrepancies, neither of which has been quietly softened. The third narrowing (`rglob("*.json")` against a docstring promising every artifact) is stated accurately and correctly owned as G-2's unmade change. The single Major is staleness of a **verification instruction**, not of a design decision: the access log has been committed and appended to since these artifacts were written, so the 37/158/121 derivation a reader is told to re-run now yields 158/232/74. The append-only conclusion drawn from it survives intact under the new numbers; the sentence stating it does not.

READY

---

## Receipt-floor note — 2026-09-04 (re-saved after the second re-affirmation)

*A second redo jump was taken because the first recovery ran confirm/write/review out of
order. This unit's design is untouched, and its two self-reported discrepancies stay open.*

A **redo jump** on `nfr-design` reset this stage's receipt floor, invalidating this unit's
summary-confirmation and review receipts. The jump was taken to lift the review-freeze on two
*other* units whose adversarial findings the project decision owner directed be fixed; the
reset is stage-wide, so it reached this unit too.

**No design content changed and no claim above is altered by this note** — including this
unit's two self-reported discrepancies (the exempt list's **seven** members on disk against the
**six** every upstream artifact states, and the literal scan being **textual rather than
AST-based**, so `"locked_test" + "_restricted"` is not caught). Both remain open and both still
reach the human at the gate. The stored confirmation was re-affirmed by the owner on 2026-09-04
(its value was already `Looks correct`), and this artifact is re-saved unchanged so the
engine's write-after-confirmation precondition is satisfied honestly rather than bypassed.

## Review — 2026-09-04 adversarial pass (fresh receipt floor)

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-04T00:00:00Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | `security-design.md` § Requirement coverage (line 313), § Sources (line 91), § SD-G-01 (line 167); mirrored in `logical-components.md` line 221, 72, 236 | **SD-G-01's requirement is mis-cited.** SD-G-01 designs `open_restricted`/`AccessRecord` — the "one door, records every access, blocks pre-G-05 execution" mechanism. The coverage table attributes this to **`FR-P1-02-3`** with acceptance rows **`WS-18, TA-18`**. Both are wrong. (a) `requirements.md` line 349's own row for `FR-P1-02-3` gives acceptance rows **`WS-18, TA-25`**, not `TA-18` — `TA-18` never appears against `FR-P1-02-3` anywhere in `requirements.md`. (b) `TA-18` is the acceptance row `requirements.md` line 407 assigns to **`FR-P1-05-12`** ("The locked-test guard blocks December performance execution before G-05 is signed, records every access... predictions... hashed before any metric") — the requirement that actually matches SD-G-01's subject matter, word for word. This unit's own upstream artifacts get it right: `domain-entities.md` line 643 traces `AccessRecord`/`RESTRICTED_LITERAL_EXEMPT_MODULES` to `FR-P1-05-12` (`WS-18, TA-18`, owner `features-and-splits`, this unit "supporting"), and `nfr-requirements/security-requirements.md` line 232 independently confirms the same mapping (`FR-P1-05-12 → SEC-G-01, SEC-G-02, SEC-G-03 → WS-18, TA-18 → features-and-splits`). `FR-P1-02-3` is a *different* requirement (the pre-G-05 December coverage-audit ordering rule) that SD-G-01 never actually addresses. **`FR-P1-05-12` is entirely absent from both nfr-design coverage tables** — confirmed by grep, zero hits in either file. This is the exact "sibling cited TA-29 where requirements.md fixes TA-28" defect class the dispatch brief names, and it lands on the design's own centerpiece section. | Re-point the coverage-table row to `FR-P1-05-12` with acceptance rows `WS-18, TA-18` and owner `features-and-splits` (this unit supporting, matching `domain-entities.md` and `security-requirements.md`); either drop `FR-P1-02-3` from this unit's cited-and-covered set or add it as its own row with its own correct acceptance rows (`WS-18, TA-25`) and state which section, if any, actually addresses it — SD-G-01 does not. Sweep both artifacts' banners, Assumptions, and every prior "Review" pass's re-derivation claims that repeat `FR-P1-02-3`/`WS-18, TA-18` as confirmed (both files' § Requirement coverage set-difference passages treat this pairing as independently re-verified when it was checked only against the union of the ID space, never against `requirements.md`'s per-ID rows). |

### Verified — did not break

- **Every line-number citation into built code, re-checked against disk**: `open_restricted` at `src/data/locked_test.py:147` — exact; `logged_at_utc` stamp at `:138`; `os.fsync` at `:143`; `assert_no_december_outside_restricted` at `:193`; `root.rglob("*.json")` at `:213`. All five match exactly.
- **DISC-1 (exempt list has seven members, not six)** — re-enumerated directly from `tests/test_locked_test_guard.py:287`'s `exempt = {...}` literal: `src/data/locked_test.py`, `scripts/merge_coverage_year.py`, `tests/test_acquisition_window.py`, `tests/test_phase_boundary.py`, `tests/test_release_hashes.py`, `tests/test_locked_test_guard.py`, `tests/test_merge_script_restricted_reads.py` — seven, confirmed, matching both artifacts exactly. Still open, still owed at the gate, not softened.
- **DISC-2 (literal scan is textual, not AST-based)** — `tests/test_locked_test_guard.py:308` reads `if "locked_test_restricted" in text:`, confirmed a substring check, not AST/constant-folding. Matches the artifact's claim exactly. Still open, still owed at 3.5, not softened.
- **`_read_guarded` at both formerly-breached sites** — confirmed present and used at `tests/test_release_hashes.py:96` (used at 140, 284, 312) and `tests/test_acquisition_window.py:88` (used at 163).
- **`assert_no_raw_fields` / `diff_protected_hashes` absence** — `grep -rn` across `src/`, `tests/`, `scripts/` returns zero matches for either symbol; matches the artifact's claim that R-23's produced-field limb is unbuilt.
- **Every other cited acceptance row against `requirements.md`'s individual rows** — `REQ-ENG-5` → `WS-10, TA-07, TA-08, TA-12, TA-27` (matches); `FR-P1-03-2` → `TA-27` (matches); `FR-P1-06-1` → `TA-27` (matches); `FR-P1-06-2` → `TA-27` (matches); `FR-P1-06-3` → `TA-28` (matches); `FR-P1-06-4` → `TA-28` (matches); `NFR-PHASE-01` → `TA-27` (matches); `NFR-LIC-01` → `TA-28` (matches); `NFR-AUD-01` → `TA-10, TA-21` (matches, both rows carried); `FR-P1-02-6` → no acceptance row in `requirements.md` (matches "NO ACCEPTANCE ROW" claim exactly). Finding #1 is isolated to the single `FR-P1-02-3`/`TA-18` pairing, not a wider pattern.
- **D-15, D-18, D-31 citations** — all three exist in `evidence/DECISIONS.md` with the substance the artifact attributes to them (D-15 custody relocation, D-18 merge determinism, D-31 G-09 signed with preconditions unmet).
- **Business rules R-23 through R-28** — all six exist in `functional-design/business-rules.md` under exactly the headings cited.
- **Test-module inventory** — the six modules named in the "What is built" banner (`test_acquisition_window.py`, `test_locked_test_guard.py`, `test_merge_script_restricted_reads.py`, `test_phase_boundary.py`, `test_release_contract.py`, `test_release_hashes.py`) match `ls tests/` exactly (six files, excluding `__pycache__`).
- **Ownership boundary** — `unit-of-work.md` § `governance-guards` Owns lists `src/data/phase_contract.py`, `src/data/locked_test.py`, `src/data/reuse_registry.py`, `tests/test_phase_boundary.py`, `tests/test_reuse_registry.py`. The design correctly attributes `tests/test_locked_test_guard.py` to `features-and-splits` (never claimed as this unit's own), and cites other units' test files only as workspace evidence for the cross-cutting `RESTRICTED_LITERAL_EXEMPT_MODULES` list, never as owned components. No mechanism-vs-approved-interface defect of the class found on sibling units this sweep.
- **No overclaim** — no coverage row is marked satisfied, no acceptance row discharged, no scientific value decided, no `TBD — freeze gate` field filled. The banner's "0 rows claimed satisfied" / "0 acceptance rows discharged" holds on recount of the table (11 rows, all `Pending` or `untested`/no-row).
- **Cross-artifact consistency** — `security-design.md` and `logical-components.md` carry the identical (and identically wrong) `FR-P1-02-3`/`WS-18, TA-18` pairing; the defect is symmetric, not a one-file-repaired-the-other-didn't case.
- **Mermaid** in `logical-components.md` — valid `graph TD` syntax, all six referenced nodes declared, text fallback matches the edges including the dotted "names only, never reads content" edge.

### Coverage limits

- This pass is bounded to `governance-guards`' own `nfr-design`, `nfr-requirements` and `functional-design` artifacts plus the shared inception contracts named in the dispatch; no sibling unit's `construction/<other-unit>/` content was read. `foundation/nfr-design/security-design.md` § SD-03 was not opened — Q1's cited divergence is taken on this artifact's own paraphrase, since no entity ID or method signature in `foundation` needed resolution to check the finding above.
- The 232/158/74 access-log arithmetic reported in the prior 2026-09-02 review pass was not independently re-run this pass (the working tree may have moved again since); this pass takes no position on it as it does not bear on the Critical finding above.
- The full pytest suite was not re-executed this pass; "277 passed, 2 skipped" is treated as a dated historical record per the artifact's own caveat, unchanged from prior passes.

### Summary

The artifact is meticulous about line-number citations into built code and about not overclaiming discharge — five prior review passes correctly re-verified `open_restricted`'s contract, the two self-reported discrepancies, and the absent symbols, and none of that verification was wrong. But every one of those passes verified the requirement-coverage table's **ID set** (is every relevant ID present, does 6+5 add to 11) without ever checking that each ID's **cited acceptance row matches that ID's own row in `requirements.md`**. That gap let a substituted requirement — `FR-P1-02-3` standing in for `FR-P1-05-12` — survive five confirming passes and both artifacts, on the design's own centerpiece mechanism (SD-G-01/G-1, the chokepoint). `FR-P1-05-12` is the requirement this section actually satisfies, per this unit's own `domain-entities.md` and per `nfr-requirements/security-requirements.md`'s independent mapping; it does not appear anywhere in either nfr-design coverage table. One Critical finding blocks READY under this review's own severity rule; everything else checked holds.

NOT-READY

---

## Review — 2026-09-04 repair verification (iteration 2, final)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-04T17:56:46Z
**Iteration:** 2 (of 2)

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `security-design.md` § Requirement coverage, `FR-P1-02-3` row (line 314); mirrored `logical-components.md` § Requirement coverage, `FR-P1-02-3` row (line 222) | The repaired `FR-P1-02-3` row states no cross-unit ownership, unlike its two siblings in the same table. `FR-P1-05-12`'s row (added by this repair) reads "row owned by `features-and-splits`, this unit supporting," and `NFR-AUD-01`'s pre-existing row reads "owned by `foundation`/`inventory-and-registry`." `FR-P1-02-3`'s row carries neither. Per the shared contract `inception/units-generation/unit-of-work-story-map.md` line 285, `FR-P1-02-3`'s split is exactly the same shape as `FR-P1-05-12`'s: primary owner `inventory-and-registry` ("performs the audit"), with `governance-guards` named as a **supporting** unit ("`open_restricted`, which writes the access-log row") — a role, not ownership. `unit-of-work.md` line 229 confirms `FR-P1-02-3` sits in `inventory-and-registry`'s own "Requirements carried (7)" list, not in `governance-guards`' 10-item carried list (`unit-of-work.md` line 162). Left as written, a reader of this table alone — which is exactly what stage 3.2 reads to size the G-05 freeze manifest — has no way to tell `FR-P1-02-3`'s evidence is `inventory-and-registry`'s to produce, the same distinction the table already draws correctly for the row two lines above it. The correction box (lines 351–359) explains *why* `FR-P1-02-3` is kept, but not *whose* row it is. | Add the same attribution pattern to both files' `FR-P1-02-3` row: e.g. "row owned by `inventory-and-registry`, this unit supporting via `open_restricted`" — mirroring the language already used for `FR-P1-05-12` and `NFR-AUD-01` in the same tables. |
| 2 | Minor | `logical-components.md` § Sources (line 72) | `FR-P1-05-12` was added to `security-design.md`'s § Sources with a dated addition note (line 91: *"added 2026-09-04 on adversarial finding 1, Critical"*), but the parallel bullet in `logical-components.md` (line 72) was not updated — it still lists only `FR-P1-02-3`, `FR-P1-02-6`, `FR-P1-03-2`, `FR-P1-06-1…4`, `REQ-ENG-5`, `NFR-AUD-01`, `NFR-PHASE-01`, `NFR-LIC-01`, omitting `FR-P1-05-12` even though it is now the first row of this same file's own coverage table (line 221) and the subject of the correction box at lines 232–241. An asymmetric one-file-fixed/one-file-not repair, the same defect class `project.md`'s `fd-2026-08-30-sweep-numerals-and-surfaces` learning names. | Add `FR-P1-05-12` to `logical-components.md`'s § Sources requirements.md bullet. |

### Verified — did not break

- **`FR-P1-02-3`'s corrected acceptance row is right.** `requirements.md` line 349 gives `FR-P1-02-3` exactly `WS-18, TA-25` — re-derived directly from the requirements table, not accepted from the correction box's own account. `TA-18` does not appear against it anywhere in `requirements.md`.
- **`FR-P1-05-12`'s row and rows are right.** `requirements.md` line 407 gives `FR-P1-05-12` exactly `WS-18, TA-18`. Both artifacts now cite this correctly, in both the coverage table and § Sources of `security-design.md`.
- **Ownership of `FR-P1-05-12` re-derived independently, not accepted from the correction box.** Three independent sources agree, cross-checked without relying on each other: (1) this unit's own `functional-design/domain-entities.md` line 643 ("`FR-P1-05-12` | ... | WS-18, TA-18 | `features-and-splits`") and its line 682 prose ("Table 2 confirms `features-and-splits` owns WS-18 and TA-18 with this unit supporting"); (2) `nfr-requirements/security-requirements.md` line 232 ("`FR-P1-05-12` | SEC-G-01, SEC-G-02, SEC-G-03 | WS-18, TA-18 | `features-and-splits`"); (3) the shared contract `inception/units-generation/unit-of-work-story-map.md` line 284, which states the ADR-03 split explicitly: test+execution limb to `features-and-splits`, access-log limb (`locked_test.py`) to `governance-guards`. All three agree with the repair's "row owned by `features-and-splits`, this unit supporting" language verbatim.
- **Recount of both coverage tables, by direct enumeration of the ID column, not by trusting the printed arithmetic.** `security-design.md`'s table (lines 313–324) has exactly **12** rows: `FR-P1-05-12`, `FR-P1-02-3`, `FR-P1-02-6`, `FR-P1-03-2`, `REQ-ENG-5`, `FR-P1-06-1`, `FR-P1-06-2`, `FR-P1-06-3`, `FR-P1-06-4`, `NFR-PHASE-01`, `NFR-LIC-01`, `NFR-AUD-01`. `logical-components.md`'s table (lines 221–227) has exactly **7** rows: `FR-P1-05-12`, `FR-P1-02-3`, `FR-P1-02-6`, `FR-P1-03-2`, `NFR-PHASE-01`, `NFR-AUD-01`, `NFR-LIC-01`. Set-differencing the two ID lists directly (not comparing totals) confirms: all 7 of `logical-components.md`'s rows appear in `security-design.md`'s 12; the 5 remaining in `security-design.md` only are `REQ-ENG-5`, `FR-P1-06-1..4`; 0 rows are unique to `logical-components.md`. `7 + 5 = 12` holds by direct enumeration, matching both files' printed decomposition (`logical-components.md` lines 248–251) exactly.
- **"1 requirement with no acceptance row" (`FR-P1-02-6`) still holds** — unaffected by the split, confirmed present with `⚠ NO ACCEPTANCE ROW` in both tables, and `requirements.md` carries no acceptance-row citation for `FR-P1-02-6` either.
- **No surviving `FR-P1-02-3`/`TA-18` pairing anywhere.** Grepped this unit's full artifact set (`nfr-design`, `nfr-requirements`, `functional-design`) for `FR-P1-02-3` and `FR-P1-05-12`; the only remaining `WS-18, TA-18` citations against `FR-P1-02-3` are inside the two preserved prior `## Review` sections above (2026-09-04 iteration 1, quoting the pre-repair defect for the record) — correctly left standing, not live claims.
- **No stale "11"/"6" current-fact claim survives outside a preserved context.** The one remaining "11 rows" occurrence in `security-design.md` (line 583) sits inside the iteration-1 `## Review` section itself — a prior reviewer's own dated record of the pre-repair state, correctly left standing per this contract, not a live claim in the artifact body. `logical-components.md` carries no live "11" or "6-shared" claim; its one superseded-figure quotation (lines 253–259) is explicitly boxed as a correction with the old figure quoted and dated, not asserted as current.
- **The keep-both-rows decision is defensible on the text, not a rationalisation.** `requirements.md` line 349's own criterion text for `FR-P1-02-3` requires *"An access-log row with `locked_test_accessed = true` is written BEFORE any operation that reads a December 2022 record"* — the identical log-then-read ordering `SD-G-01`/`open_restricted` implements (lines 149–168). `FR-P1-02-3`'s own acceptance set already includes `WS-18` (shared with `FR-P1-05-12`), independently corroborating that `SD-G-01`'s mechanism is genuinely relevant to both requirements rather than merely re-cited for convenience. The shared contract (`unit-of-work-story-map.md` line 285) independently names `governance-guards` (`open_restricted`, "which writes the access-log row") as a support unit for `FR-P1-02-3`, confirming the dependency the correction box claims is real and not invented to justify keeping a stale citation.
- **DISC-1 (seven-member exempt list, against upstream's six) stands unsoftened** in both artifacts' current (non-Review) text — `security-design.md` lines 113–128, 375; `logical-components.md` lines 208–213, 268. Still flagged "owed to the human at the gate," `nfr-requirements` still explicitly not edited.
- **DISC-2 (textual, not AST-based, literal scan) stands unsoftened** in both artifacts' current text — `security-design.md` lines 130–143, 376; `logical-components.md` lines 155–161, 269. Still flagged "owed at 3.5," still states no artifact may describe the scan as AST-based until it is.
- **Upstream functional-design artifacts were never wrong and needed no sweep.** `functional-design/business-logic-model.md` line 1009 and `functional-design/business-rules.md` line 616 already correctly state `FR-P1-05-12 → WS-18, TA-18 → features-and-splits` — confirming the Critical was isolated to the two `nfr-design` files, exactly as finding #1's original text claimed, and that no further correction was owed outside `nfr-design`.
- **`NFR-AUD-01`'s row is unaffected and unchanged** by the split — `TA-10, TA-21`, "owned by `foundation`/`inventory-and-registry`," `Pending — one half unbuilt` in both files, matching the pre-repair state exactly.

### Coverage limits

- This pass re-derived `FR-P1-02-3` and `FR-P1-05-12`'s acceptance rows directly from `inception/requirements-analysis/requirements.md` (not accepted from the correction boxes), and re-derived ownership from three independent sources including the shared `inception/units-generation/unit-of-work-story-map.md` and `unit-of-work.md` contracts — the one sanctioned spot-check into a resolvable cross-unit reference, not a sweep of any sibling unit's `construction/<other-unit>/` content. No sibling unit directory was opened, globbed, or grepped.
- The recount of both coverage tables was by direct enumeration of each table's ID column, not by trusting the printed "12"/"7"/"7+5=12" arithmetic.
- This pass did not re-verify the code-level claims already confirmed by five prior passes (`open_restricted`'s five properties, DISC-1's seven-member enumeration, DISC-2's textual scan, the two absent symbols, `_read_guarded` at both sites) — those hold unchanged since the repair touched only the coverage tables, § Sources, and the correction boxes, and iteration-1's "Verified — did not break" list already covers them.
- The full pytest suite was not re-executed this pass; the 277/2-skip figure and the 232/158/74 access-log arithmetic are unchanged by this repair and were not re-derived here.
- One new gap was found by extending the sweep past what the repair itself touched: `logical-components.md` § Sources' incompleteness (finding #2) and the `FR-P1-02-3` ownership-attribution asymmetry (finding #1) were found by comparing the repaired rows against their siblings in the same tables, not named in the repair's own account of itself.

### Summary

The repair correctly re-derives both acceptance rows from `requirements.md` (`FR-P1-02-3` → `WS-18, TA-25`; `FR-P1-05-12` → `WS-18, TA-18`), correctly re-derives `FR-P1-05-12`'s ownership as `features-and-splits`-owned/this-unit-supporting against three independent sources including the shared units-generation contract, and correctly recounts both tables to 12 and 7 rows with a set-difference-verified 7-shared/5-security-only/0-here-only decomposition. The keep-both-rows decision is grounded in `FR-P1-02-3`'s own requirement text and in the shared contract's explicit support-role assignment, not a rationalisation. Both open items (DISC-1's seven-vs-six, DISC-2's textual scan) stand exactly as before, unsoftened. Two gaps survive the repair: `FR-P1-02-3`'s row states no cross-unit ownership where its two sibling rows in the same tables do (Major), and `logical-components.md`'s § Sources was not updated to add `FR-P1-05-12` the way `security-design.md`'s was (Minor). Zero Critical, one Major, one Minor — within this review's own READY threshold (≤2 Major).

READY

---

## Review — 2026-09-04 confirming pass (fourth floor)

**Reviewer:** aidlc-architecture-reviewer-agent

**Verdict:** READY
**Date:** 2026-09-04T22:03:51Z
**Iteration:** 1 (adversarial confirming pass over the two fixes applied for iteration-2's residual gaps)

### Findings

None.

### Verified — did not break

- **Fix 1 (FR-P1-02-3 ownership label) is correct, re-derived from the shared contracts, not accepted from the correction box.** `inception/units-generation/unit-of-work.md` line 229 lists `FR-P1-02-3` in `inventory-and-registry`'s own "Requirements carried (7)" list, and line 233 confirms `TA-25` in that unit's own "Acceptance rows (3)" — `WS-01, TA-04, TA-25`. `governance-guards`' own carried list at line 162 (`REQ-ENG-5, FR-P1-02-6, FR-P1-03-2, FR-P1-05-12, FR-P1-06-1..4, NFR-PHASE-01, NFR-LIC-01`) does **not** carry `FR-P1-02-3`, confirming this unit never owned it. `unit-of-work-story-map.md` line 67 independently agrees (`FR-P1-02-3 | inventory-and-registry | WS-18, TA-25`). Both `security-design.md` line 314 and `logical-components.md` line 222 now read "row owned by `inventory-and-registry`" — present, worded consistently, and matching in both tables.
- **A residual inconsistency was found in the shared contract itself, outside this unit's fix scope.** `unit-of-work-story-map.md` line 285's cross-unit item header reads *"FR-P1-02-3, WS-18, TA-18 (the permitted G-05 December coverage audit)"* — the header's own acceptance-row citation says `TA-18`, contradicting that same file's line 67 (`WS-18, TA-25`) and `requirements.md` line 349 (`WS-18, TA-25`). This is a labelling defect internal to `unit-of-work-story-map.md`, not something either fix here needed to match: the fix cites `requirements.md` (the authoritative source) and `unit-of-work.md`'s per-unit carried/acceptance lists (the more granular contract), both of which agree with each other and with the repair, and the ownership claim itself — `inventory-and-registry` performs the audit, `governance-guards` supports via `open_restricted` — is what line 285's own body text states regardless of its header's stale acceptance-row label. Not a defect in this artifact; owed to `units-generation`, not to this unit, and outside this stage's read-write authority to correct.
- **Fix 2 (`logical-components.md` § Sources gained `FR-P1-05-12`) is present and accurately dated.** Line 72 now reads `**FR-P1-05-12** *(added 2026-09-04 on iteration-2 Minor: `security-design.md`'s § Sources gained it at the Critical repair and this file's did not — an asymmetric repair)*`, immediately followed by the rest of the pre-existing ID list. Matches `security-design.md`'s own Sources note (line 91) in substance and dating.
- **The Critical repair (iteration 1) still stands, re-verified against `requirements.md` directly.** Line 349: `FR-P1-02-3 | ... | WS-18, TA-25`. Line 407: `FR-P1-05-12 | ... | WS-18, TA-18`. Both artifacts' coverage tables cite these exactly (`security-design.md` lines 313–314; `logical-components.md` lines 221–222).
- **Counts re-derived by direct enumeration, not trusted on printed arithmetic.** `security-design.md`'s table (lines 313–324): 12 rows — `FR-P1-05-12, FR-P1-02-3, FR-P1-02-6, FR-P1-03-2, REQ-ENG-5, FR-P1-06-1..4, NFR-PHASE-01, NFR-LIC-01, NFR-AUD-01`. `logical-components.md`'s table (lines 221–227): 7 rows — `FR-P1-05-12, FR-P1-02-3, FR-P1-02-6, FR-P1-03-2, NFR-PHASE-01, NFR-AUD-01, NFR-LIC-01`. Set-differencing (not comparing totals): all 7 of the smaller table appear in the 12-row table; the 5 remaining (`REQ-ENG-5, FR-P1-06-1..4`) are `security-design.md`-only; 0 rows unique to `logical-components.md`. 7 + 5 = 12, matching both files' printed decomposition.
- **The two self-reported open items stand unsoftened.** DISC-1 (exempt list has seven members on disk against six upstream) — present verbatim at `security-design.md` lines 113–128, 375 and `logical-components.md` lines 208–213, 268, still "owed to the human at the gate," `nfr-requirements` still explicitly not edited. DISC-2 (literal scan is textual, not AST-based) — present verbatim at `security-design.md` lines 130–143, 376 and `logical-components.md` lines 155–161, 269, still "owed at 3.5," still bars any artifact from describing the scan as AST-based until it is.
- **Regression grep: no live `FR-P1-02-3`+`TA-18` mispairing survives outside preserved text.** Every remaining co-occurrence of `FR-P1-02-3` and `TA-18` in `security-design.md` (lines 91, 334, 337, 442, 569, 578, 584, 617, 622, 640) and `logical-components.md` (lines 233–234) sits inside a dated correction box or a preserved prior `## Review` section quoting the pre-repair defect for the record — none is a live current-fact claim.
- **No overclaim.** Neither table marks a new row satisfied or an acceptance row discharged by either fix; `FR-P1-02-6`'s "NO ACCEPTANCE ROW" status is unaffected; WS-18/TA-18/TA-27/TA-28 remain `Pending` in both files; `NFR-AUD-01` remains "one half unbuilt." Nothing in either fix touches a scientific value or a `TBD — freeze gate` field.

### Coverage limits

- This pass re-derived ownership from `inception/units-generation/unit-of-work.md` and `unit-of-work-story-map.md` (the shared inception contracts passed with this dispatch) and from `inception/requirements-analysis/requirements.md`; no sibling unit's `construction/<other-unit>/` content was opened, globbed, or grepped.
- The line-level code claims re-verified across five prior passes (`open_restricted`'s five properties, DISC-1's seven-member enumeration, DISC-2's textual scan, the two absent symbols, `_read_guarded` at both sites) were not re-run this pass; nothing in the two fixes touches built code, only the coverage tables and § Sources.
- The `unit-of-work-story-map.md` line-285 header inconsistency (`TA-18` vs. the file's own `TA-25`) is reported as an observation for the record, not corrected here and not treated as blocking this artifact's READY — it sits in a contract this unit's stage does not own or edit.

### Summary

Both fixes hold under independent re-derivation against the shared contracts. Fix 1's ownership label (`FR-P1-02-3` owned by `inventory-and-registry`) is confirmed by `unit-of-work.md`'s per-unit carried/acceptance lists and by `unit-of-work-story-map.md`'s own per-ID table row, and `governance-guards`' own carried list confirms it never owned the requirement. Fix 2's `logical-components.md` § Sources addition is present and dated to match its sibling. The prior Critical repair's acceptance-row citations, the 12/7/7+5=12 count, and both self-reported discrepancies (DISC-1, DISC-2) all stand unsoftened, and no live mispairing of `FR-P1-02-3`/`TA-18` survives outside preserved review text. One residual observation — a stale acceptance-row label inside `unit-of-work-story-map.md` itself — is noted for the record but belongs to `units-generation`, not to this artifact. Zero Critical, zero Major, zero Minor against this artifact.

READY

---

## Review — 2026-09-05 re-affirmation (post-gate receipt refresh)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T08:05:18Z
**Iteration:** 1 (re-affirmation)

### What was confirmed

1. **Terminal prior verdict.** The PRIMARY's last review before this pass is `## Review — 2026-09-04 confirming pass (fourth floor)`, dated 2026-09-04T22:03:51Z, iteration 1, verdict **READY**, zero findings (Critical/Major/Minor all zero).
2. **No content edits after that verdict.** `git log` on both `security-design.md` and `logical-components.md` shows exactly one commit after the terminal review: `7ec1feb` ("Re-register nfr-design artifacts on this clone; repair split sentence"). Its diff against `governance-guards`' two files adds only a dated "fifth re-save 2026-09-04 — not a redo" banner paragraph to each file, stating explicitly that the consolidated summary confirmation stands, was not re-asked, and "no status claim is altered by this note" / "no design content changed." The commit touched four other units (`acquisition`, `external-products`, `foundation`, `inventory-and-registry` — visible in the full commit, `governance-guards` was one of the six re-registered but not one of the four the gate rejection revised); this unit's coverage tables, § Sources, and correction boxes are byte-identical to the terminal-review state.
3. **Spot-checks of the terminal review's verified claims, re-derived directly from current file content (not accepted from the review text):**
   - `security-design.md` line 314 and `logical-components.md` line 222 both still read the `FR-P1-02-3` row as **"row owned by `inventory-and-registry`"**, matching the terminal review's Fix 1 confirmation.
   - `logical-components.md` § Sources (line 72) still carries **`FR-P1-05-12`** with its dated addition note, matching the terminal review's Fix 2 confirmation.
   - `DISC-1` and `DISC-2` are both still present, unsoftened, at `security-design.md` lines 113 and 130 (and echoed in the re-save banner at line 10), matching the terminal review's "stand unsoftened" claim.

All three hold. No new edit exists to introduce a defect between the terminal verdict and this receipt refresh.

READY
