# NFR Requirements — Questions — `governance-guards`

**Unit** `governance-guards` (Bolt 2) · **Kind** `library` · **Stage** `nfr-requirements`

Two artifacts only — `security-requirements.md` and `tech-stack-decisions.md`. The
stage's `produces_kinds` maps `performance-requirements`, `scalability-requirements` and
`reliability-requirements` to `[service]` / `[service, ui]`, and this unit is
`kind: library`.

**Not re-asked, because `functional-design` already decided them.** The static-scan role
(R-24, Q7 = D — the `ast` scan is the early-warning limb, run-time assertions are
authoritative, both run); the December-hit definition and its bounded driver exclusion
(R-26); the per-artifact-class walk and unparseable-file-is-a-failure rule (R-27); the
durable-append-before-read ordering (R-25, Q6 = C); the one-door reading (Q9 = D). Those
are carried, not reopened.

**Carried as a stated dependency, not decided here.** **BLK-07 is open and stays open**,
and is a precondition of Bolt 3.

---

## Question 1

`business-rules.md` R-28 records a **live breach**, in its own words: two of the exempt
modules read content beneath the restricted root **today** with **no `AccessRecord`** —
`tests/test_release_hashes.py:137` and `tests/test_acquisition_window.py:195`. That is
`evidence/experiment_registry.md:79–83`'s recorded RES-04 hazard *"occurring in fact
rather than in principle"*. R-28 states the ruling **does not cure it**; routing those two
reads through `open_restricted` is **owed at stage 3.5**.

R-25 requires the access-log append to be **durably completed before the December read
begins** — a log-write or durability failure must **prevent the read**.

How should `security-requirements.md` state the requirement these two facts produce?

A. Every read beneath the restricted root routes through `open_restricted`, stated as a requirement that is **currently breached at two named sites**, with remediation owed at stage 3.5 and named a precondition of the G-05 evidence package
   > **Impact**: The requirement is stated at full strength and the breach is visible with file and line, so no reader can mistake the current state for compliance. It makes an unmet requirement part of the G-05 package's preconditions, which raises the cost of reaching G-05 with it still open — deliberately.

B. State the requirement prospectively, and record the two existing reads as grandfathered pre-guard accesses
   > **Impact**: Clean separation between what the guard will enforce and what predates it, matching how the five retrospective December access rows are already handled. It converts a breach the project's own evidence calls "occurring in fact" into an accepted historical artifact, and `open_restricted` does not exist yet, so there is no guard for them to predate.

C. Require the two reads to be fixed before any further work in this unit
   > **Impact**: Closes the hole soonest. G-09's disclosure is that no module may be created and these are edits to existing test modules whose fix depends on `open_restricted`, which is unbuilt — so the requirement would be unsatisfiable in the order it demands.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — R-28 already states the breach in exactly these terms and assigns the remediation to stage 3.5, so A transcribes a decision rather than taking a new one. Option B's "grandfathered" framing does not survive the detail that the guard does not yet exist; there is nothing to predate. Option C inverts a dependency: the fix needs `open_restricted` first.

[Answer]: A

---

## Question 2

The one-door static check asserts that **no module outside the exemption contains the
restricted-root literal**. A literal check has a stated blind spot: a path assembled at
run time — `EVIDENCE_DIR / ("locked_test" + "_restricted")`, an `os.path.join` of parts,
or a name read from config — contains no literal and passes. R-24 already makes run-time
assertions the **authoritative** limb and the static scan **subordinate**, and
`open_restricted` is the content chokepoint, so a computed path still cannot read content
without going through it.

What should `security-requirements.md` require of the static check itself?

A. Keep it literal, and **disclose the computed-path blind spot** as a stated limit, leaning on `open_restricted` and R-24's run-time limb to carry enforcement
   > **Impact**: Matches R-24's declared hierarchy exactly and adds no mechanism the design has not approved. The static check keeps a gap that a determined or careless computed path walks through, and the gap is only closed at run time — which a local checkout scan never reaches.

B. Require the static check to be **AST-based with constant folding**, so a concatenation or `join` of literal parts is also caught
   > **Impact**: Closes the most likely accidental evasion — a path split across two string literals — while keeping the check static and cheap. It cannot catch a genuinely dynamic path (a config value, an environment variable), so the blind spot narrows rather than closes, and the check becomes a piece of code that itself needs testing. `tests/test_phase_boundary.py` already walks the tree with `ast`, so the technique is in use here.

C. Require both the literal check and a run-time path-assembly assertion inside `open_restricted`'s caller allowlist
   > **Impact**: Strongest coverage. It couples this root unit more tightly to the four downstream consumers, which R-28 already names as the cost of the caller allowlist, and adds an obligation on units that have not agreed to it.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B — the project already runs an `ast` walk over `src/` and `scripts/` for the phase-boundary limb, so constant folding is an increment on an existing technique rather than a new mechanism, and it catches the evasion most likely to happen by accident. It must be stated with its residual honestly: a genuinely dynamic path still passes, and R-24's run-time limb remains the authoritative one. Option A is defensible and cheaper; option C reaches into other units' contracts, which this stage should not do.

[Answer]: B

---

## Consolidated Summary Confirmation

Confirm this reading before the two artifacts are written. Nothing below decides a
scientific value, and nothing claims a gate or acceptance row is discharged.

**Scope.** Two artifacts only — `security-requirements.md` and `tech-stack-decisions.md`.
`foundation` is `kind: library` and so is this unit; `produces_kinds` excludes the other
three. Performance, scalability and reliability are still assessed, and the assessment is
recorded in the security artifact's scope note.

**Q1 = A — the one-door requirement is stated at full strength and recorded as currently
breached.** Every read of content beneath `evidence/locked_test_restricted/` routes
through `open_restricted`, which durably appends the `AccessRecord` **before** the read
begins (R-25). The requirement is **breached today at two named sites** —
`tests/test_release_hashes.py:137` and `tests/test_acquisition_window.py:195` — which
`evidence/experiment_registry.md:79-83` records as the RES-04 hazard occurring in fact.
Remediation is **owed at stage 3.5** and is named a precondition of the G-05 evidence
package. Nothing is grandfathered: `open_restricted` does not exist, so there is no guard
for those reads to predate.

**Q2 = B — the static check is AST-based with constant folding.** It catches a
restricted-root path assembled from concatenated or joined string literals, not only an
exact literal. Its **residual is stated rather than hidden**: a genuinely dynamic path — a
config value, an environment variable — still passes the static check, and **R-24's
run-time limb remains the authoritative one** with the static scan subordinate.

**The exempt-module count used throughout is five**, in addition to the chokepoint
`src/data/locked_test.py` — **six** counting it, the convention R-28's box uses. The fifth
member is `scripts/merge_coverage_year.py`, a **production script, not a test**, which is
why membership is an exact enumerated list and never a `tests/` directory predicate.

**Correction applied upstream on your approval, and recorded here.** Four live sites in
this unit's approved `functional-design` still asserted the superseded count of four —
`business-logic-model.md` W-10's mechanism sentence and its "four modules" restatement,
`business-rules.md` R-28's own **Rule** statement, and the 2026-08-28 ruling box's "no
fourth". All four were annotated in place on 2026-08-31 with superseded figures preserved.
A change record under `governance/` may be owed and is yours to file.

**Carried, not re-decided.** R-24's static/run-time hierarchy (Q7 = D); R-25's
durable-append ordering (Q6 = C); R-26's December-hit definition and bounded driver
exclusion; R-27's per-class walk with unparseable-file-is-a-failure; the Q9 = D one-door
reading. **BLK-07 is open and stays open**, and is a precondition of Bolt 3.

**Status claims made.** None. **WS-18 and TA-18 are not discharged** — the guard test is
written but **unexecuted**, and no Python interpreter exists in this environment. TA-27 and
TA-28 are `Pending`. G-09 is signed (D-31) with its own §18.3 preconditions UNMET. Stage
3.1 remains FAIL. `FR-P1-02-6` carries **no acceptance row**.

Reply `Looks correct` to proceed, or state what to change.

[Answer]: Looks correct
