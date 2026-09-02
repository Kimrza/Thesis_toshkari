# Security Design — `foundation`

**Unit** `foundation` (Bolt 1) · **Kind** `library` · **Stage** `nfr-design`

> ## ⚠ THIS IS A DESIGN. NOTHING HERE IS BUILT, RUN, OR DISCHARGED
>
> **Module inventory, re-derived against the workspace on 2026-09-01.**
>
> *(This box previously read: "**No module in this document exists.** `src/data/config.py`,
> `src/data/release.py`, `src/data/registry.py`, `src/data/reuse_registry.py` and
> `tests/test_determinism.py` are **named, not written**… **No Python interpreter exists in
> this environment**." **That was false when written here.** It was carried from
> `nfr-requirements` as established input without checking disk — which `project.md`
> § Way of Working forbids in those words. Superseded text preserved above. Corrected under
> a gate rejection on 2026-09-01, the only route that lifts the §12a write-freeze; the owner
> ruled that `nfr-requirements` itself stays unchanged.)*
>
> | Module | State on disk |
> |---|---|
> | `src/data/config.py` | **EXISTS** |
> | `src/data/release.py` | **EXISTS** |
> | `src/data/locked_test.py` | **EXISTS** — `open_restricted` at line 147 |
> | `src/data/registry.py` | **absent** |
> | `src/data/reuse_registry.py` | **absent** |
> | `tests/test_determinism.py` | **absent** |
>
> **What has not changed.** **`configs/`, `pyproject.toml` and `requirements.txt` are all
> absent** — all three §12-mandated, so **TC-06's scaffold precondition remains unmet**.
> **G-09 is signed (D-31) with its own preconditions UNMET**; **stage 3.1 remains FAIL**.
>
> **On execution — a correction that is not good news.** A Python interpreter **does**
> exist: **3.14.7**, with pytest installed 2026-09-01, and `python -m pytest tests/ -q`
> returns **277 passed, 2 skipped**. But **3.14.7 is not the governed pin** — TE §8.1 and
> TC-03d fix Python **3.11 exactly** — and no `requirements.txt` exists to pin pytest
> against. **That run is not governed evidence.** It establishes that six test modules are
> executable and internally consistent, and **nothing** about TA-03, the §13.1 environment
> lock, or any WS/TA row. Every test named in this document remains
> **written-but-unexecuted under the governed environment**, or unwritten.
>
> **TA-22 is `Pending` and NFR-SEC-01 is unclaimed** — the history, configuration, log and
> artifact limbs have **not been scanned**, and § SEC-F-02's acquisition identity-block
> exception is **unresolved**. **TA-15 is NOT covered.** **TA-10 and TA-21 are `Pending`.**
> **WS-18 and TA-18 are not discharged.** `foundation`'s **TensorFlow pin stays
> `TBD — freeze gate`**.
>
> **The correction discharges nothing, and that is worth stating explicitly.** Three modules
> existing where this document once said none did **does not move a single acceptance row**.
> A written module is not a tested one, a tested one is not one tested under the governed
> environment, and none of the three is any of those. Every row below remains `Pending`,
> `NOT MET`, `unclaimed` or `untested` — verified against the coverage table after the
> correction, not assumed.
>
> **No scientific value is decided here.** TE §18.2's absolute rule stands.

## Sources

- `nfr-requirements/security-requirements.md` — **SEC-F-01** (secret-scan scope at TE §10's full width), **SEC-F-02** (the acquisition identity block as a known unresolved exception), **SEC-F-03** (credentials per platform through one interface), **SEC-F-04** (the restricted root unreachable from this unit), **SEC-F-05** (audit integrity as a security property), **SEC-F-06** (release immutability; D-29), **SEC-F-07** (the §10.1 reuse register).
- `nfr-requirements/tech-stack-decisions.md` — **TS-01** (Python 3.11), **TS-02** (the unfrozen TensorFlow pin), **TS-05** (exactly two platforms), **TS-06** (repository structure and tooling), **TS-07** (determinism and the environment lock).
- `functional-design/business-logic-model.md` — **W-5** (the run record), **W-6** (the twenty-column registry; step 8's durability confirmation), **W-8** (`resolve_platform_roots`), and § Assumptions, which names three release-enumeration surfaces and chooses none.
- `../../../inception/requirements-analysis/requirements.md` — **REQ-ENG-6**, **REQ-ENG-10** *(the eight-item per-run environment lock)*, **FR-P1-01-10**, **FR-P1-05-13**, **NFR-SEC-01**, **NFR-AUD-01**, **NFR-LIC-01**, **NFR-DET-01**, **NFR-REP-01** *(the last three cited 2026-09-01 on adversarial finding 1, **Critical** — this artifact's Sources already cited **TS-07 "determinism and the environment lock"** and § SD-03 rests on the lock throughout, while the governing IDs appeared nowhere in either file)*.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§10** (credentials and secrets), **§10.1** (the code-reuse register), **§13.1** (the environment lock), **§13.3** (immutable dataset releases), **§13.4** (the registry schema), **§18.2–18.3**, **§19** (TA-10, TA-15, TA-21, TA-22), **§16** (WS-18).
- `evidence/DECISIONS.md` — **D-29** (`dataset_version` as the first 12 hex characters of `content_hash`, with verify-on-write), **D-31** (G-09 signed, preconditions unmet).
- `nfr-design-questions.md` — Q1 = B, Q2 = A, Q3 = B, Q4 = A, and the receipted Consolidated Summary Confirmation.

---

## Scope note — why this unit has three fewer design artifacts

`produces_kinds` maps `performance-design` to `[service, ui]` and `scalability-design`
and `reliability-design` to `[service]`. `foundation` is `kind: library`, so those three
are **not produced**. The categories were assessed at `nfr-requirements` and are **not
re-opened here**: no latency or throughput target applies, no load projection applies
(exactly two execution environments, one user), and the two reliability obligations that
do exist — registry **durability** and release **immutability** — are security-adjacent
and are designed below rather than dropped.

**What this unit is.** A library the other eleven units import. It loads configs, hashes
them, resolves the platform, resolves credentials, seeds, records runs, and writes
releases. **It serves no request and computes no scientific quantity.** The stage's Step 5
vocabulary — caching tiers, connection pooling, CDN usage, load balancing, failover —
describes a networked service and has **no referent here**. Manufacturing content for
those headings would be writing fiction into the foundation of a research pipeline.

---

## SD-01 — The secret scan runs in two modes, and only one of them is evidence

**Design (Q1 = B).** Two scans, answering two different questions.

| Mode | Scope | When | What it is |
|---|---|---|---|
| **Incremental** | The **staged diff** | Every `git commit`, via the pre-commit hook | A **preventive net**. Not evidence. |
| **History-inclusive** | **History, configurations, logs, artifacts** — TE §10's full width | Before each governed run and each freeze gate | **TA-22's evidence**, with tool version and commit range |

**Neither replaces the other, and the design must not let them be confused.** The
incremental scan **proves nothing about history** — it sees one diff. The gate scan is
the only one whose result can be attached to TA-22. A pipeline that ran only the
incremental scan and reported TA-22 satisfied would be making a claim its evidence cannot
support.

**Why the incremental scan is worth its cost.** A credential that reaches history
requires a **history rewrite** to remove. This repository **tags its freeze gates**
(`team.md` § Way of Working), so that rewrite would rewrite tagged commits — the tag
either breaks or silently points at different content, and the freeze the tag exists to
record is destroyed either way. Catching the credential at `git commit` costs a second.

**The gate scan's evidence contract.** Its output records the **tool name and pinned
version**, the **commit range scanned**, the **scan scope** (which of history,
configurations, logs and artifacts were covered), and the result. A scan report that does
not name its commit range is not evidence: TA-22 is a claim about a range, and a report
without one cannot be checked against the commit being gated.

**Accepted costs, stated rather than discovered later.** Two configurations to keep in
step — a drift between them is a silent narrowing of the incremental net. Periodic false
positives on test fixtures, which is standard for this tool class and must be handled by
an **allowlist that is itself reviewed**, never by disabling the hook.

> **⚠ The tool is not selected, and selecting it is not this stage's act.** `gitleaks`,
> `trufflehog` or equivalent, **pinned**. SEC-F-01 left this open and this design does not
> close it — pinning a scanner version is a repository-tooling decision that belongs with
> the `pyproject.toml` scaffold TC-06 places before acquisition work.

> **⚠ What this design does NOT do.** It does not scan anything. **TA-22 remains
> `Pending`, NFR-SEC-01 remains unclaimed**, and the zero-hit evidence recorded at
> `nfr-requirements` is `git ls-files` **at one commit** — blind by construction to a
> credential committed and later removed. § SEC-F-02's identity-block exception is
> **unresolved and awaits the supervisor**; nothing here resolves it.

## SD-02 — One credential interface, and it never learns a value

**Design (SEC-F-03, R-14).** Credentials reach the process from a **platform secret store
or environment configuration excluded from version control**. One resolution interface;
**calling code never branches on platform**.

| Platform | Mechanism |
|---|---|
| **Kaggle** | Kaggle Secrets (`UserSecretsClient`) |
| **Local** | Shell environment, or a file matched by the `.gitignore` deny-list |

**The interface's hard property.** `resolve_platform_roots` identifies the platform as
exactly one of `kaggle` or `local` (`PlatformError` otherwise) and returns **a label and
roots**. **No credential value is read, returned, logged, serialized, interpolated or
persisted** — there, or in any foundation-layer diagnostic.

**Why that property is structural and not a coding rule.** A resolver that returned a
value would put credentials inside the object every other unit imports, and the eleven
downstream units would each acquire a way to leak one. Keeping the value out of the
foundation layer means a leak requires a unit to reach for the secret store **itself**,
which is a visible act in a diff rather than an accident of logging an object.

**The presence check, and what it does not prove.** Stages requiring authenticated
provider access check that required environment-variable **names** are present, failing
early and **naming what is missing**. It does **not** prove a value is non-empty, valid or
authorized — the provider client validates the value **without exposing it**. Stated at
the design because a presence check mistaken for a validity check reports a readiness
that does not exist.

**Accepted cost.** Two provisioning paths are two ways to misconfigure. That is why a
missing name must fail **early and by name** rather than surfacing later as a provider
authentication error, which is the failure that costs a session to diagnose.

> **⚠ Open, and not this stage's to close.** The concrete `CredentialNameMap` contents
> await `configs/` existing. This design fixes the **mechanism**; the names are filled
> when the four governed configs exist.

## SD-03 — Audit integrity: append-only, closed vocabulary, and a durability stamp

**Design (SEC-F-05, NFR-AUD-01, FR-P1-05-13, TE §13.4).** The experiment registry is
**append-safe and atomic**. Failed and aborted runs **remain visible with status and
reason**. **No entry is deleted, overwritten or silently re-run.** The schema is TE
§13.4's **twenty** columns, asserted at write time.

**Three properties that make the guarantee mechanical rather than procedural:**

1. **Writes never read the run history** (R-08). This is what makes the append safe under
   concurrency, and it is also the reason **no row can be rewritten to match a later
   belief** — the writer has no way to find the row it would need to change.
2. **The status vocabulary is closed and validated at write time** (R-07). An unknown
   status is a **failure**, not a new category.
3. **`exploratory` is derived in the writer, never passed by a caller** (R-20). A caller
   that could set it could **suppress** it — and suppressing it is exactly the act the
   flag exists to prevent.

**`AccessRecord` / `RegistryEvent` join on `run_id` with orphan detection in both
directions** (R-19). The **five retrospectively logged December accesses**, and the **one
possible unauthorized access `GOV-2026-08-28-FD-01` Recommendation 31 records as
expressly unresolved**, are reported as **known pre-guard orphans**. **No registry row is
ever back-filled to clear them** — the orphan is the record.

**On integrity failure, report honestly even when reporting fails** (R-10): terminate
with a message naming **the file and the violated expectation**. Never continue silently
past a failed hash or integrity check.

### The durability stamp (Q3 = B)

**Kaggle's durability semantics are characterised nowhere in this design.** W-6 step 8's
durability confirmation reuses `governance-guards` R-25's pattern, and platform behaviour
differs between the two governed platforms.

**Design.** The write **proceeds**, and the row records that its durability is
**unverified on this platform**. **The freeze gate refuses to accept a so-stamped row as
evidence.**

**Both halves are this design's, and the second is what makes the first honest.** A stamp
with no refusal behind it is decoration — it records a caveat into a column nobody reads
at the moment it matters. The refusal at the gate is therefore **part of this design**,
not an assumption about a downstream unit's behaviour. This is the same shape the project
already uses for `inventory-and-registry`'s audit blindness and for its two-half
cross-unit contracts: **the limitation travels as a machine-carried field**, and the
consumer refuses.

**The residual, stated with the rule.** A stamped row is **easy to accumulate and easy to
normalise**. Nothing in this design bounds how many may exist, and a project that
routinely produces them has converted a warning into background noise. What prevents that
is the gate refusal actually biting — which is checkable — rather than anyone's intention.

> **⚠ The measurement is owed and is not performed here.** W-6 step 8 needs its own
> **measured** evidence before rows written inside a Kaggle session are relied on at a
> freeze gate. That is a measurement obligation on Bolt 1's in-Kaggle work, **not an
> implementation choice**, and not this stage's to discharge. **TA-10 and TA-21 are
> `Pending`; the registry tests are unwritten.**

## SD-04 — Releases are immutable, and the uniqueness check refuses rather than assumes

**Design (SEC-F-06, TE §13.3, R-11, R-13).** A release directory is **never
overwritten**. Every immutable dataset release records version, source manifest, SHA-256
hashes, schema, row counts, exclusions and fold/mask identifiers, and is write-protected
or stored under a **new version**. **Release identity is the content hash; the label is
not authoritative.**

**`dataset_version` is the first 12 hex characters of `content_hash`** with a
**verify-on-write** uniqueness check (**D-29**, 2026-08-28).

### The enumeration surface (Q2 = A) — an owner decision at a §18.3 stop-and-report point

D-29's check must read back the **existing release population**, and where that population
lives was **not settled**: the release-history ledger that would have answered it was
**declined as drafted at Amendment C**, and `ReleaseLedgerEntry` withdrawn with it.
`functional-design` § Assumptions names three candidate surfaces and chooses none.

**Decision: `write_release` enumerates the release root**, reading each release
directory's recorded `content_hash`.

**Recorded as an explicit owner decision, not an agent default.** TE §18.3 forbids an
implementer from picking an unresolved mechanism by convenience and requires it to stop
and report; the owner directing the choice is the sanctioned path, and that is what
happened.

**Why this surface.** The releases **are** the population, so the check **cannot disagree
with reality**. The registry-columns alternative was rejected on its **failure mode**: a
release written by a path that failed to register would be **invisible**, silently turning
a collision check into a **no-op** — and injectivity is D-29's entire purpose. The narrower
ledger was rejected because it **reopens a refusal already on record**, which `project.md`
permits only on a new argument or an explicit decision, and because it adds a third thing
that can disagree with the other two.

> ### ⚠ The limit this choice carries — read it with the decision, not after it
>
> **The check is only as complete as the release root the writing process can see.**
> Across **two platforms with different filesystem semantics**, that is precisely the
> assumption this project has been bitten by before.
>
> Two consequences, both binding:
>
> 1. **Enumeration is over a single authoritative release root** — never whichever root
>    the current session happened to resolve. A per-session root would make uniqueness a
>    property of where the code ran.
> 2. **A `write_release` that cannot reach that root REFUSES.** It does **not** treat an
>    unreachable population as an empty one — because **an empty population makes every
>    hash unique**, which turns the guard into a rubber stamp at exactly the moment it is
>    most needed.

> **⚠ Owed, and not performed here: this decision should carry a D-number.** It settles a
> mechanism a governing document left open at a stop-and-report point, and `team.md`'s
> linking rule makes `evidence/DECISIONS.md` authoritative for this class of decision.
> **Recording it there is the student's act**; this design records that it is owed.

> **⚠ TA-15 is NOT covered.** `tests/test_release_hashes.py` exists and its name matches
> the mandated module, but it exercises **none** of §13.3's required manifest fields and
> does **not** exercise R-13's overwrite refusal. TA-15 must not be read as covered.

## SD-05 — The restricted root is unreachable, and the reuse register precedes use

**Design (SEC-F-04, R-15, R-16).** **No `foundation` code path constructs a path into
`evidence/locked_test_restricted/`.** Only `src/data/locked_test.py`, owned by
`governance-guards`, may reach it, and **every access records `locked_test_accessed =
true`**. Only `foundation` reads `configs/`; **no machine-specific path enters a governed
config**.

**Bolt 1's boundary, stated precisely.** Bolt 1 performs no governed run, so the
in-Kaggle obligation does not bind it — but that obligation is a **condition on the
execution session, not on a Bolt number**, and binds **any** Bolt performing a governed
run inside a Kaggle session.

**Design (SEC-F-07, TE §10.1, NFR-LIC-01, gate G-P2).** Any reused or materially adapted
third-party source is recorded in the §10.1 register **before the code is used**, with
the full field set: `reuse_id`, repository URL, immutable commit or tag, upstream file and
line or function, retrieval date, licence and SPDX ID, copied-versus-adapted status,
destination file, scientific purpose, modifications, tests, original citation, notice
location, reviewer and approval date.

**Standing default while the AGPLv3 question is open.** Third-party source whose licence
is **absent, ambiguous or incompatible** is **not copied or materially adapted** —
reimplement the published method from the paper with a citation. The AGPLv3
Global-TEC-forecasting repository is the one approved direct-copy source today, and
**whether its repository-distribution obligations permit that copying is a governance
dependency this project does not resolve on its own.**

> **⚠ Status.** `src/data/reuse_registry.py` and `tests/test_reuse_registry.py` **do not
> exist**. **G-P2 is unaffected by G-09's signature.** The executable guard for the
> restricted root is `tests/test_locked_test_guard.py` — `governance-guards`', **written
> but unexecuted** — so **WS-18 and TA-18 are not discharged**.

## SD-06 — The environment lock is an integrity artifact, and determinism is one of its items

*(Section added 2026-09-01 on adversarial finding 1, **Critical**. The substance below was
already load-bearing across § SD-03 and `logical-components.md` C-1 — the environment lock
is what a registry row's `environment_lock_hash` column points at — while **NFR-DET-01**,
**NFR-REP-01** and **REQ-ENG-10** were cited nowhere. The design rested on them and named
only TE §13.1 and TS-07.)*

**Design (REQ-ENG-10, TE §13.1).** Every run captures the **eight items** of the per-run
environment lock: the `requirements.txt` hash **and** a per-run `pip freeze`; Python, OS,
CPU and key library versions; the code commit; configuration snapshot hashes for **all
four** configs; input dataset and manifest versions; the platform; and any known
nondeterministic operations.

> **The 7-versus-8 count is carried, not smoothed.** TE §13.1 renders as **seven**
> bullets while REQ-ENG-10 calls them **eight items**: bullet 1 carries **two separately
> capturable artifacts**. Both are right, and `nfr-requirements` § TS-07 derived this
> programmatically. This design does not silently pick one number.

**Why the lock belongs in a security design at all.** It is the object a registry row's
`environment_lock_hash` **points at**. If the lock is incomplete, the hash is a stable
identifier for an under-specified environment — the row looks reproducible and is not, and
§ SD-03's append-only guarantees would faithfully preserve a false claim. **Audit
integrity is only as good as what the audited field references.**

**Design (NFR-DET-01, TC-21).** Seeds are fixed in `seeds.yaml`; the **three-seed
element-wise mean** is the confirmatory prediction; nondeterministic operations are
**recorded** where determinism cannot be guaranteed. **No seed is selected on validation
or after seeing December.**

**Two properties that keep determinism honest rather than asserted:**

1. **Determinism is applied before any graph construction** — re-exec first (R-05). Set
   after construction, it is set too late and silently so.
2. **An empty `nondeterministic_ops` is never proof of determinism** (R-06). It is equally
   consistent with *"nothing was nondeterministic"* and *"nobody looked"*, and the design
   must not let the second masquerade as the first.

**Design (NFR-REP-01, TE §13.7).** The §13.2 ordered sequence completes on **CPU from a
clean environment**, and **§13.7's exact-equality classes hold exactly** — hashes,
schemas, partition membership, IDs and deterministic CPU transformations compare **for
equality, not tolerance**, and a mismatch **must never silently update the expectation**.

**Where this design touches NFR-REP-01 and where it does not.** `foundation` supplies the
lock and the seeding utility that the clean run depends on; **it does not run the clean
run**, which is `fixtures-and-reproducibility`'s. What this unit owes is that the lock's
eight items are **captured completely** and that the seeding utility is **one tested
path** — the rest of NFR-REP-01 is discharged elsewhere and is **not claimed here**.

> **⚠ Carried, with its status intact.** The frozen seed values — development **42**,
> final **{1337, 2024, 7}**, bootstrap **20221201** — are **D-122**, which Vision §14.2
> marks *"Approved — supervisor sign-off pending"*: **frozen for implementation, still
> owing a signature at G-05**. This design carries that status rather than treating the
> values as settled.

> **⚠ REQ-ENG-10 has NO acceptance row.** `requirements.md` records it `UNTESTED` — no
> WS or TA row covers the §13.1 capture list, and a candidate row via Vision §15.2 was
> **declined at Amendment A on 2026-08-24**. So the most security-relevant artifact in
> this section is the one nothing tests. Stated because a reader would otherwise assume
> the lock is covered by TA-03. **`tests/test_determinism.py` does not exist**; **WS-17,
> TA-13, WS-20 and TA-17 are all undischarged**.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| REQ-ENG-6 | SD-01 | TA-22 | `Pending` — **NOT MET** |
| FR-P1-01-10 | SD-01 | TA-22 | `Pending` — **NOT MET** |
| **NFR-SEC-01** | SD-01, SD-02 | TA-22 | `Pending` — **unclaimed** |
| FR-P1-05-13 | SD-03 | TA-10, TA-21 | `Pending` |
| **NFR-AUD-01** | SD-03 | **TA-10, TA-21** — both rows | `Pending` |
| **NFR-LIC-01** | SD-05 | TA-29 — row owned by `governance-guards` | `Pending` |
| **REQ-ENG-10** | SD-06 | ⚠ **NO ACCEPTANCE ROW** — `UNTESTED`; candidate row declined at Amendment A, 2026-08-24 | untested |
| **NFR-DET-01** | SD-06 | WS-17, TA-13 | `Pending` |
| **NFR-REP-01** | SD-06 | WS-20, TA-17 — rows owned by `fixtures-and-reproducibility` | `Pending` |

**Derived and printed**: 6 design sections (SD-01…SD-06); **9** coverage rows *(count
re-derived 2026-09-01 on adversarial finding 1, **Critical**; superseded figure preserved:
**6**)* — counted directly from the table above, **not** read off the `nfr-requirements`
coverage table. **0** rows claimed satisfied; **0** acceptance rows discharged; **1**
requirement recorded as **actively NOT MET** (NFR-SEC-01 / TA-22, at SD-01); **1** with
**no acceptance row at all** (REQ-ENG-10).

**What the miss was, stated rather than quietly patched.** The three added rows were not
peripheral: **REQ-ENG-10** is the environment lock a registry row's `environment_lock_hash`
points at, and **NFR-DET-01**/**NFR-REP-01** are the seeding and clean-run obligations
`logical-components.md` C-1 lists among its own responsibilities. This artifact's Sources
already cited **TS-07 — "determinism and the environment lock"** — so the substance was
consciously included and only the governing IDs were absent. **The dispatch brief for this
review predicted these two NFR IDs by name as the likeliest misses, and they were missed
anyway** — which says the prediction was right and the check was still not run against
`requirements.md`'s ID space before writing.

---

## Review — 2026-09-01 repair verification

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 2

### Findings

None at Critical or Major severity. The single Critical from iteration 1 is resolved.

| # | Severity | Location | Finding |
|---|---|---|---|
| — | — | — | No new findings raised. |

### Verification of the repair

**All six sites present, and mutually consistent.** Both coverage tables were recounted
directly against their own rows, not against the artifacts' printed totals:
`security-design.md` § Requirement coverage carries exactly **9** rows (REQ-ENG-6,
FR-P1-01-10, NFR-SEC-01, FR-P1-05-13, NFR-AUD-01, NFR-LIC-01, REQ-ENG-10, NFR-DET-01,
NFR-REP-01); `logical-components.md` § Requirement coverage carries exactly **6**
(FR-P1-05-13, NFR-AUD-01, REQ-ENG-6, REQ-ENG-10, NFR-DET-01, NFR-REP-01). Set-differencing
the two ID lists gives shared = {FR-P1-05-13, NFR-AUD-01, REQ-ENG-6, REQ-ENG-10,
NFR-DET-01, NFR-REP-01} = **6**, security-only = {FR-P1-01-10, NFR-SEC-01, NFR-LIC-01} =
**3**, logical-only = **0**, and 6 + 3 = 9 — exactly the decomposition both artifacts
state, and this time derived against the complete row set rather than the incomplete one
iteration 1's arithmetic check (correctly) validated.

**Acceptance rows verified against `requirements.md`, not against the artifacts' own
claims.** Line 486: `NFR-DET-01` → WS-17, TA-13 — matches both artifacts. Line 485:
`NFR-REP-01` → WS-20, TA-17, owned by `fixtures-and-reproducibility` — matches, and both
artifacts correctly state they do not claim the clean run themselves. Line 271:
`REQ-ENG-10` → `UNTESTED`, "no WS/TA row covers the §13.1 capture list; candidate new TA
row via Vision §15.2" — the artifacts' fuller claim ("candidate row declined at Amendment
A on 2026-08-24") is independently confirmed at
`construction/foundation/functional-design/business-rules.md` line 1788 and
`functional-design-questions.md` line 913 ("DECLINED... Owner, on the evidence that no
rule requires universal §19 coverage"). Line 488: `NFR-AUD-01` → TA-10, TA-21 — both rows
present in both artifacts' tables, not truncated.

**ID-space sweep.** Checked the full `REQ-ENG-*` range for undisclosed reproduced
substance: REQ-ENG-7 (freeze-gate tagging and D-number citation in commit messages,
`requirements.md` line 269) is not reproduced anywhere in either artifact — SD-06 and C-1
describe only the environment-lock and determinism substance of REQ-ENG-10, never
REQ-ENG-7's tagging/citation obligation — so no undisclosed reproduction exists there; the
exclusion needs no statement because nothing is reproduced. No other `NFR-*`, `FR-P1-*`,
`FR-WS-*` or `REQ-ENG-*` ID's text was found reproduced in either artifact outside the rows
already in both coverage tables.

**SD-06 accuracy, checked against source.** The eight-item list matches REQ-ENG-10's text
at `requirements.md` line 271 verbatim in substance. The 7-vs-8 explanation, R-05, and R-06
match `tech-stack-decisions.md` TS-07 (lines 199–216) word-for-substance, including the
"eight items in seven bullets... bullet 1 carries two separately capturable artifacts"
derivation and its stated `awk`-derived provenance. The D-122 status ("Approved —
supervisor sign-off pending") matches `requirements.md` line 395's own citation of Vision
§14.2 and `tech-stack-decisions.md` TS-07's identical framing.

**No stale site.** No live assertion of "6 coverage rows" or "3 coverage rows" or "3
shared" was found outside the explicitly labelled superseded-figure notes (both artifacts
preserve the prior figure in a parenthetical announcing it as superseded, per this
project's stated convention).

**No regression.** Q1–Q4 findings from iteration 1 remain intact and unmoved; the
`produces_kinds` scope note, the Mermaid diagram with its `NEVER` edge and text fallback,
and the unbuilt/unmeasured caveat paired with every guarantee at its point of claim are
all still present and unchanged in substance.

**Nothing newly claimed discharged.** The banner and inline status markers (G-09
signed/preconditions unmet, stage 3.1 FAIL, TA-22 `Pending`/NFR-SEC-01 unclaimed, TA-15 not
covered, TA-10/TA-21 `Pending`, WS-17/TA-13/WS-20/TA-17 undischarged, WS-18/TA-18 not
discharged, TensorFlow pin `TBD — freeze gate`, SEC-F-02 unresolved) are all still present
and unchanged; the new SD-06 section adds no claim of anything built, run, or tested.

### Summary

The Critical from iteration 1 is resolved: all three requirement IDs are now cited with
accurate, source-verified acceptance-row status in both artifacts, the coverage-table
counts and their set-difference decomposition are internally consistent and correctly
derived, and no regression or new defect was found across the six repair sites, the
ID-space sweep, or the no-newly-discharged check.

READY

**Why this table is shorter than `security-requirements.md`'s.** That artifact carries
**16** requirements across both its files; this one covers the **6** whose text this
design reproduces. The remainder are stated upstream and **not restated here** — a design
that re-listed every upstream requirement would be a copy, not a design. The test applied
was **reproduction, not ownership**: an ID appears here when this document states an
obligation against it.

## Assumptions & Open Questions

- **[Q1 / SD-01]** **The scanner is not selected.** `gitleaks`, `trufflehog` or equivalent, **pinned** — a repository-tooling decision belonging with the `pyproject.toml` scaffold, not with this design.
- **[Q1 / SD-01]** The false-positive **allowlist is itself a review surface**. Nothing here specifies who reviews it, and an unreviewed allowlist is a silent way to disable the check one pattern at a time.
- **[Q2 / SD-04]** **The single authoritative release root is not named.** This design fixes that there must be exactly one and that an unreachable root **refuses**; **which** root it is awaits `configs/` existing.
- **[Q2 / SD-04]** **A D-number is owed** for the enumeration-surface decision. The student's act; recorded here as owed.
- **[Q3 / SD-03]** **Kaggle durability is unmeasured**, and the stamp does not measure it. The gate-side refusal is specified here and **unbuilt**, like everything else in this document.
- **[Q3 / SD-03]** **Nothing bounds how many durability-stamped rows may accumulate.** A project that routinely produces them has normalised the warning.
- **[SD-02]** **`CredentialNameMap` is empty** until `configs/` exists.
- **[SD-01]** **§ SEC-F-02's acquisition identity-block exception is unresolved** and awaits the supervisor. It is a **known exception**, not a resolved one, and no reading has been adopted.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row, install or test as discharged.

---

## Review — 2026-09-01

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | `security-design.md` § Requirement coverage; `logical-components.md` C-1 and § Requirement coverage | **NFR-DET-01 and NFR-REP-01 are cited nowhere in either artifact, despite both artifacts' substance resting on them.** C-1's own responsibility list is "config loading and hashing; platform and root resolution; credential resolution; **seeding and the environment lock**" — that is the exact substance of NFR-DET-01 ("Seeds fixed in `seeds.yaml`; three-seed element-wise mean is the confirmatory prediction; nondeterministic ops recorded", `requirements.md` line 486, acceptance WS-17/TA-13) and NFR-REP-01 (clean-CPU reproducibility and the §13.7 exact-equality classes, line 485, acceptance WS-20/TA-17). `security-design.md`'s own Sources line cites **TS-07 "determinism and the environment lock"** directly but never turns that into a coverage-table row. REQ-ENG-10 (the eight-item per-run environment lock, which cites both `[NFR-REP-01]` and `[NFR-AUD-01]` at its own definition, line 271) is likewise reproduced by C-1's "environment lock" responsibility and by SD-02/SD-03's design of what a run records, and is cited nowhere. This is precisely the defect class the dispatch brief flags as having been found on all twelve units of the previous stage — text reproduced, ID and acceptance row cited nowhere — and the brief's own prediction ("NFR-DET-01 and NFR-REP-01 are the likeliest misses here") is confirmed on inspection of the requirement text at `requirements.md` lines 271, 395, 460, 485–486. | Add coverage-table rows for NFR-DET-01 (WS-17, TA-13), NFR-REP-01 (WS-20, TA-17), and REQ-ENG-10 (candidate new TA row per Vision §15.2, per the requirement's own `UNTESTED` status note) to both artifacts, and state in C-1's write-up (and SD's seeding/environment-lock passages, which currently exist only as bare mentions) which of these three obligations the "seeding and the environment lock" responsibility discharges and which it only names. |

### Verified faithful to the receipted decisions

- **Q1 = B** — two scan modes present in `security-design.md` SD-01 with the incremental/gate table; "the incremental scan **proves nothing about history**" and "TA-22 remains `Pending`" both stated in the rule body, not only under Assumptions; scanner tool explicitly unselected (⚠ block).
- **Q2 = A** — `write_release` enumerates the release root (SD-04); framed as a TE §18.3 owner decision, not an agent default; both binding consequences present in the rule body ("Enumeration is over a single authoritative release root" and the refuse-rather-than-assume clause with its reason: "an empty population makes every hash unique"); the owed D-number is stated as owed, not recorded as done.
- **Q3 = B** — write proceeds and stamps durability unverified; "the freeze gate refuses to accept a so-stamped row as evidence" stated as **part of this design** in the rule body (SD-03), not assumed of a downstream unit; the accumulation/normalisation residual is in the rule body under "The residual, stated with the rule," not only under `## Assumptions`.
- **Q4 = A** — the C-1/C-2/C-3 split in `logical-components.md` is argued as a failure-kind analysis ("A bad read fails a run. A bad write corrupts the permanent record."), not a module listing; C-2 and C-3 are genuinely distinguished (unit of damage: a row vs. a release directory and every downstream claim citing it; separate, already-divergent acceptance-row status: TA-10/TA-21 `Pending` vs. TA-15 explicitly **not covered**).

### Verified structural claims

- The "three fewer / shorter table" framing in both artifacts is a genuine decomposition, not an unverified subtraction: `security-design.md`'s six coverage rows are {REQ-ENG-6, FR-P1-01-10, NFR-SEC-01, FR-P1-05-13, NFR-AUD-01, NFR-LIC-01}; `logical-components.md`'s three are {FR-P1-05-13, NFR-AUD-01, REQ-ENG-6} — a strict subset. Shared = 3, security-only = 3, logical-only = 0, exactly as both artifacts state.
- `produces_kinds` scope note is correct: `performance-design` maps to `[service, ui]`, `scalability-design`/`reliability-design` to `[service]`; a `library` unit produces neither, and neither artifact manufactures service-shaped content (no caching, autoscaling, or failover language present).
- Mermaid diagram parses; the `NEVER` edge to `RESTRICTED` is present and its text fallback ("No path runs from any `foundation` component into `evidence/locked_test_restricted/`") matches the diagram.
- No mechanism is overstated where its guarantee is unbuilt: every claim of a guarantee ("the freeze gate refuses," "no credential value is read, returned, logged...") is paired at the point of the claim with an unbuilt/unmeasured caveat, not deferred to `## Assumptions` alone.
- No item under "Do not report as newly discharged" is misreported as discharged in either artifact; both open with an unmissable "NOTHING IS BUILT" banner and repeat the `TA-10`/`TA-21`/`TA-15`/`TA-22`/`WS-18`/`TA-18`/G-09/TensorFlow-pin status accurately throughout.

### Summary

The four receipted decisions (Q1–Q4) are carried into the design faithfully, including their stated limits and residuals in the rule body rather than buried in Assumptions, and the coverage-table decomposition and scope-note claims both verify on inspection. The blocking defect is the coverage gap on NFR-DET-01, NFR-REP-01, and REQ-ENG-10: their substance is reproduced by C-1's "seeding and the environment lock" responsibility and by the Sources' own citation of TS-07, but no coverage row, ID, or acceptance row for any of the three appears in either artifact — the same defect class flagged as systemic at the prior stage.

NOT-READY

---

## Review — 2026-09-01 post-correction

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 1 (fresh budget after gate rejection)

### What this pass verified against the workspace, not against either document

1. **`src/data/config.py`, `src/data/release.py`, `src/data/locked_test.py` — confirmed EXISTS** on disk (`locked_test.py` carries `open_restricted` per the artifact's own line reference). Both artifacts' corrected module-inventory tables (`security-design.md` lines 7–22; `logical-components.md` lines 7–16) match this exactly — the correction replaced one false claim ("no module exists") with a true one, not with a different false one.
2. **`src/data/registry.py`, `src/data/reuse_registry.py`, `tests/test_determinism.py` — confirmed absent.** Both artifacts state this correctly and nowhere claim any of the three built.
3. **`configs/`, `pyproject.toml`, `requirements.txt` — confirmed absent.** TC-06's scaffold precondition is genuinely still unmet in both artifacts' telling, matching disk.
4. **Off-pin caveat verified present at the point of the test-result claim in both files**, not deferred to Assumptions: `security-design.md` lines 32–33 ("returns **277 passed, 2 skipped**. But **3.14.7 is not the governed pin**…") and `logical-components.md` lines 18–19 (same figures, same caveat). Neither file lets the run stand as governed evidence or as discharging TA-03, the §13.1 environment lock, or any WS/TA row — both explicitly withhold that.
5. **Both files carry the correction**, not just `security-design.md`. `logical-components.md`'s own banner (lines 7–16) independently states "Corrected 2026-09-01 under a gate rejection" with the same three-file existence table and the same disk-check framing — it is not a copy-through of `security-design.md`'s box, it restates the fact in its own words and cites its own three modules.

No item of 1–5 is wrong, so no Critical is raised on this axis.

### Re-run coverage set-difference (fresh, not accepted from printed arithmetic)

Read both tables directly: `security-design.md` § Requirement coverage lists **9** rows — {REQ-ENG-6, FR-P1-01-10, NFR-SEC-01, FR-P1-05-13, NFR-AUD-01, NFR-LIC-01, REQ-ENG-10, NFR-DET-01, NFR-REP-01}. `logical-components.md` § Requirement coverage lists **6** rows — {FR-P1-05-13, NFR-AUD-01, REQ-ENG-6, REQ-ENG-10, NFR-DET-01, NFR-REP-01}. Set-differencing (not comparing totals): the 6 logical-components rows are a strict subset of the 9 security-design rows; the 3 security-design-only rows (FR-P1-01-10, NFR-SEC-01, NFR-LIC-01) are scan-scope and licence items that raise no component-boundary question, exactly as `logical-components.md` lines 216–221 argue rather than assert. Decomposition is 6 shared / 3 security-only / 0 logical-only, 6+3=9 — internally consistent and independently re-derived, not copied from the artifacts' own printed arithmetic.

Checked `NFR-AUD-01` specifically against `requirements.md`: its acceptance-row list is **TA-10, TA-21**, and both rows appear at every citation in both artifacts (`security-design.md` line 379, `logical-components.md` line 200) — the row list is not truncated.

Checked the remaining six of the eleven named NFR IDs (`NFR-DQ-01`, `NFR-FAIR-01`, `NFR-IRI-01`, `NFR-LEAK-01`, `NFR-PHASE-01`, `NFR-TDEF-01`) against `requirements.md`: each governs IRI-boundary, feature-leakage, phase-boundary, target-definition, fairness or data-quality substance owned by other units (feature engineering, evaluation, phase-transition) — none names a config/release/credential/registry/scan responsibility that `foundation`'s two artifacts claim or reproduce. Their absence from `foundation`'s coverage tables is a scope match, not a gap. No `REQ-ENG-*`, `FR-P1-0*-*`, `FR-WS-*` or `REQ-*` ID was found reproduced in substance in either artifact without a corresponding coverage row.

**Does the correction change any coverage row?** No — `config.py`/`release.py`/`locked_test.py` now existing on disk does not upgrade any row's status: every row remains `Pending`, `NOT MET`, `unclaimed`, or `untested` exactly as before, because module existence is not the acceptance criterion any WS/TA row measures (a written module is not a passing test, a signed gate, or a discharged acceptance row). Both artifacts correctly decline to claim otherwise.

### Verified unchanged from the prior pass (re-checked, not merely carried forward)

- Q1=B, Q2=A, Q3=B, Q4=A all still hold in the current text at the cited locations; the owed D-number for Q2 is still stated as owed; the Q3 refusal and residual are still in the rule body.
- § SD-06 still states REQ-ENG-10's eight items, the 7-vs-8 count carried rather than picked, R-05/R-06, and D-122 "Approved — supervisor sign-off pending."
- Mermaid diagram still parses; the `NEVER`-edge text fallback still matches.
- Every item under "Do not report as newly discharged" — TA-22, NFR-SEC-01 unclaimed, TA-15 not covered, TA-10/TA-21 `Pending`, WS-17/TA-13/WS-20/TA-17/WS-18/TA-18 undischarged, REQ-ENG-10's missing acceptance row, TensorFlow pin `TBD`, SEC-F-02 unresolved, G-09 preconditions unmet, stage 3.1 `FAIL` — remains stated accurately and is not contradicted by the new module-existence facts.

### Findings

None rise to Critical or Major. No broken cross-reference, no false discharge, no stale status claim, and no coverage gap in the applicable ID space was found on this pass.

### Summary

The correction replaced a false "nothing exists" claim with a verified-true module inventory in both artifacts, independently stated in each rather than copy-pasted, and the off-pin test-result caveat sits at the point of the claim rather than in Assumptions. The SD-06 coverage decomposition (9/6, 6 shared/3 security-only/0 logical-only) re-derives cleanly against a freshly re-read table, `NFR-AUD-01`'s two acceptance rows are both present at every citation, and the six NFR IDs outside `foundation`'s scope are correctly absent rather than missing. No item on the "do not report as newly discharged" list is misreported, and module existence is correctly not treated as discharging any acceptance row.

READY

## Review — 2026-09-01 post-jump confirming pass

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Iteration:** 1 (fresh budget after redo jump)

**Reason for this entry:** the prior "2026-09-01 post-correction" pass above returned READY on this exact content; a redo jump then cleared the review-receipt floor for the unrelated procedural reason stated in the dispatch (a sibling artifact needed a post-confirmation write that the write-freeze blocked). The reviewed content itself is unchanged. This entry is a confirming re-verification, not a new review of new content.

**Re-verified independently against disk, this pass:**
- `src/data/config.py`, `src/data/release.py`, `src/data/locked_test.py` — confirmed **EXIST** (`ls`/existence check re-run).
- `src/data/registry.py`, `src/data/reuse_registry.py`, `tests/test_determinism.py`, `configs/`, `pyproject.toml`, `requirements.txt` — confirmed **ABSENT**. TC-06's scaffold precondition remains genuinely unmet; no item of the correction overstates what exists.
- Both `security-design.md` (this file, lines ~1–16 banner) and `logical-components.md` (its own banner, independently worded) still carry the correction with superseded text preserved rather than deleted — consistent with this project's stated convention, and not a case of a struck claim being misread as stale.
- Spot-checked the SD-06 coverage decomposition and the `NFR-AUD-01` TA-10/TA-21 citation pair already re-derived in the "2026-09-01 post-correction" entry above: figures match a fresh read of both tables (9 rows here, 6 in `logical-components.md`, 6 shared / 3 security-only / 0 logical-only) — no drift since that pass.
- Confirmed no row's status has been silently upgraded by the presence of the three now-existing modules: TA-22, TA-15, TA-10/TA-21, WS-17/TA-13/WS-20/TA-17, WS-18/TA-18, REQ-ENG-10's missing acceptance row, the TensorFlow `TBD` pin, SEC-F-02, and the G-09/stage-3.1 preconditions all still read exactly as the "do not report as newly discharged" list states — module existence is not an acceptance criterion any WS/TA row measures, and neither artifact claims otherwise.

**Findings this pass:** none. No Critical, no Major, no newly-stale representation, no coverage-set drift, no broken cross-reference introduced between the prior pass and now.

**Verdict rationale:** the redo jump was procedural (a sibling write-freeze), not a defect in this unit's content; re-verification confirms the corrected facts still hold on disk and no downstream drift occurred in the interim. Nothing here reopens or re-litigates the prior pass's settled findings.

READY

## Review — 2026-09-01 final confirming pass

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z (system clock; no shell timestamp taken this pass)
**Iteration:** 1 of 2 (advisory)

**Scope of this pass:** a further redo jump cleared the receipt floor for the same stated procedural reason (write-freeze on a native-tool write after human confirmation, unrelated to content). One paragraph was added to each file since the prior confirming pass. This entry verifies those two additions plus re-runs the standing checks; it does not re-litigate settled findings.

**Added paragraph 1 — `security-design.md` "discharges nothing" claim.** Re-checked the coverage table (lines 382–390) and every status-bearing banner line directly: every row still reads `Pending`, `NOT MET`, `unclaimed`, or `untested` — no row reads "satisfied" or any synonym of discharged. `TA-22`/`Pending`, `NFR-SEC-01`/`unclaimed`, `TA-15`/not covered, `TA-10`+`TA-21`/`Pending`, `REQ-ENG-10`/no acceptance row (`untested`) all confirmed unchanged. Accurate, not Critical.

**Added paragraph 2 — `logical-components.md` C-1/C-2/C-3 partial-vs-absent claim.** `src/data/registry.py` re-confirmed **ABSENT** by direct existence check this pass (alongside `reuse_registry.py`, `tests/test_determinism.py`, `configs/`, `pyproject.toml`, `requirements.txt`, all also absent). `src/data/config.py`, `release.py`, `locked_test.py` re-confirmed **EXIST**. This matches C-1 (config/release/seeding responsibilities, backed by `config.py`/`release.py`) and C-3 (release writer, backed by `release.py`) having partial coverage while C-2 (registry writer, needs `registry.py`) has no module at all — the claim is accurate.

**Standing checks re-run, all held:** the six existence/absence facts above; the off-pin caveat (277 passed / 2 skipped, Python 3.14.7 / pytest 9.1.1 vs. governed 3.11, no `requirements.txt` to pin) still sits at the point of the test-result claim in both files, not deferred to Assumptions; the SD-06 coverage decomposition (9 rows in `security-design.md`, 6 in `logical-components.md`, 6 shared / 3 security-only / 0 logical-only) still re-derives cleanly, with `NFR-AUD-01` carrying both `TA-10` and `TA-21`; Q1–Q4 positions, the Mermaid diagram (parses, text fallback present, `NEVER`-edge recorded), and the "do not report as newly discharged" list (`TA-22`, `NFR-SEC-01` unclaimed, `TA-15` not covered, `TA-10`/`TA-21` `Pending`, `WS-17`/`TA-13`/`WS-20`/`TA-17`, `WS-18`/`TA-18`, `REQ-ENG-10`'s missing row, TensorFlow `TBD` pin, `SEC-F-02` unresolved, `G-09` preconditions unmet, stage 3.1 `FAIL`) all remain accurately stated and unclaimed-as-discharged.

**Findings this pass:** none — no Critical, no Major, no drifted status, no broken cross-reference.

**Summary:** both newly added paragraphs are accurate against the workspace (module existence/absence verified directly) and against the artifacts' own coverage tables (no row status drifted toward satisfied). This is a confirming pass over a procedural redo, not new content review.

READY
