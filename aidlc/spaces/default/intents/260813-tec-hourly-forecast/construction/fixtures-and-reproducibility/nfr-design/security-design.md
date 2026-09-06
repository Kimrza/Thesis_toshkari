# Security Design — `fixtures-and-reproducibility`

**Unit** `fixtures-and-reproducibility` (Bolt 12) · **Kind** `library` · **Stage** `nfr-design`

> ## ⚠ NOTHING HERE IS CLAIMED SATISFIED — AND NEITHER FIXTURE HAS EVER RUN
>
> This is a design. **No measured value exists** — every runtime, tolerance, row-count range
> and storage figure stays a placeholder until fixture time (TE §15.1), and **the two
> manifest freeze acts remain the project owner's under Q-31**; nothing here performs them.
> **No Python interpreter exists in this environment; `configs/` does not exist;
> `foundation`'s TensorFlow pin is `TBD — freeze gate`**, so nothing in this unit can
> execute today. **FR-WS-2, FR-WS-3 and FR-P1-03-5 have no acceptance row; REQ-ENG-10 is
> untested by design — 4 requirements carry no evidence.** WS-20, TA-09, TA-17, TA-03 and
> TA-26 are undischarged. **G-09 is signed (D-31) with preconditions UNMET**; BLK-08 ↓ is
> checked here rather than inherited silently. TE §18.2's absolute rule stands: **no
> scientific value is decided here.**

## Sources

- `../nfr-requirements/security-requirements.md` — **SEC-X-01** (hash-protected frozen manifest, one validating loader, the unenforced-chokepoint concession in the rule body), **SEC-X-02** (plumbing fixture never evidence; December excluded on record dates), **SEC-X-03** (the clean run compares; the two-receipt ordering contract), **SEC-X-04** (the in-session gate; lock-bound staleness, Q1 = A there). This design gives each a mechanism; it re-decides none.
- `../nfr-requirements/tech-stack-decisions.md` — **TS-X-01** (the manifest, `pyyaml`, the hash check in the loader, the reference-hash constraint this stage's Q1 resolves), **TS-X-02** (deterministic write order — D-18/`DATA-17`), **TS-X-03** (the clean run drives real scripts, no GPU visible), TS-X-04/05 as carried.
- `../functional-design/business-logic-model.md` — **W-1**…**W-10**, especially W-2 (measure then freeze), W-6 (`test_clean_run.py`), W-7 (the ordering contract as an executable gate), W-8 (the in-session gate), W-9 (the three generated evidence artifacts).
- `../functional-design/business-rules.md` — R-133…R-142.
- `evidence/DECISIONS.md` — D-11, D-14, D-18; the freeze acts owed as future D-numbers (Q1 = C's second write lands there).
- `nfr-design-questions.md` — **Q1 = C** (sibling file + D-number record), **Q2 = A** (lock-bound receipt validity), and the receipted Consolidated Summary Confirmation.
- Absent by scope design (`library` kind): `performance-requirements.md`, `scalability-requirements.md`, `reliability-requirements.md` were not produced at `nfr-requirements`; that stage's Scope note carries the assessments (every performance figure is a placeholder) and this design does not reinvent them.

---

## Scope note

"Security" here is what `nfr-requirements` fixed: **the integrity of the evidence everything
else rests on** — if the fixture manifest can be edited to match a bad run, every
reproducibility claim becomes unfalsifiable. No credential, user, or network surface.
Reliability (this unit IS the project's reliability evidence) is realised by the fail-closed
mechanisms below.

## SD-X-01 — The reference hash lives in two places, checked in one (Q1 = C, owner ruling)

**The ruling.** Upstream fixed the constraint (a hash inside the file it protects protects
nothing) and routed the location choice to the owner; the owner ruled **C** at this stage's
receipted question. Design:

1. **Mechanical home:** `tests/fixtures/<fixture_id>/fixture_manifest.sha256`, a sibling
   file **written only by the freeze act**. R-133's single validating loader reads manifest
   + sibling and **refuses on mismatch** — one `hashlib` comparison at the read path every
   load already passes (TS-X-01). Format-stable: no prose parsing in the loader.
2. **Governance home:** the freeze act's **D-number entry** in `evidence/DECISIONS.md` also
   records the hash. Re-freezing without a new D-number is structurally visible, because the
   freeze is already the owner's deliberate two-step under Q-31 — this adds the record to
   the step that already exists, not a new step.
3. **Agreement is tested, not assumed:** one check, **owned by the evidence-generator
   component (`logical-components.md` F7)**, asserts sibling-file hash == D-number-recorded
   hash for every frozen manifest. A disagreement **raises**, naming both sites — the
   two-representation risk closed by the project's own negative-control idiom. *(Ownership
   corrected 2026-09-05 on adversarial finding 1, Major; superseded: "one check in
   `tests/test_clean_run.py`'s apparatus" — which contradicted `logical-components.md`'s
   three F7 assignments and its dependency diagram (`F7 --> F2`, no `F5 --> F2`). F7 owns
   the check; the clean-run suite is where F7's checks execute, not their owner.)*

**Negative controls:** an edited manifest fails to load (hash mismatch); an edited sibling
without a matching D-number entry fails the agreement check; a `candidate`-state manifest
with a sibling hash **raises** (only `frozen` manifests carry one).

**The standing limit, carried in the body, not softened:** the loader chokepoint is **not
enforced today** — a direct `yaml.safe_load` bypasses schema, hash and all of the above;
R-132's convention that would catch it is unwritten. **No artifact may describe "no silent
update" as enforced.** This design narrows the author-convenience-edit case; it closes
nothing that goes around the loader.

## SD-X-02 — Receipt validity is lock-bound, like the gate (Q2 = A)

**The gap, as raised.** Fixture-pass receipts must outlive their session for the two-receipt
check (R-140: both fixtures pass, in order, before any full-year job), and Kaggle's
durability semantics are unmeasured.

**Design.** Each fixture-pass receipt records the **§13.1 environment-lock items in force
when its fixture passed** — the same item set the in-session gate records (SEC-X-04). The
exported two-receipt check accepts a receipt **iff its recorded lock matches the full-year
job's own §13.1 lock**. Consequences:

- **Staleness is a derived fact, not a time window or a storage property** — the same
  discriminator SEC-X-04's Q1 = A fixed for gate reuse, now one rule for both mechanisms.
  A config edit or re-install invalidates receipts automatically; an unchanged environment
  reuses them regardless of session age.
- **Durability becomes self-answering:** a receipt that did not survive is simply absent,
  the check fails closed, and the fixtures re-run. No trust is placed in Kaggle persistence
  and no measurement of it is required for correctness (only for cost).
- **The ordering stays inside the receipts:** the scientific-fixture receipt records the
  plumbing receipt it found (identity by citation, R-134's idiom), so "in order" is checked
  from the artifacts, not from timestamps — the same containment reasoning the sibling
  units' ordering check uses.

**Inherited limit, stated:** lock-bound validity cannot see a change the §13.1 items do not
cover; the check is as good as the lock's completeness, and `configs/` does not exist yet,
so the four config hashes have nothing to hash today. The mechanism is **specified and
unrunnable**, like the gate it mirrors.

**A second limit, stated rather than left to be discovered** *(added 2026-09-05 at the stage
gate, governance Recommendation 7)*: **receipts carry no tamper-evidence.** The manifest gets
two-representation hash protection (SD-X-01); a receipt gets none, and the same
threat — one convenience edit of a receipt's recorded lock makes both fixtures appear passed
in the current environment — applies to the artifact R-140's ordering check and G-07's
evidence rest on. The design does not claim this closed. **Routed to 3.5:** record receipts
through `foundation`'s append-safe registry rows (the NFR-AUD-01 surface — failed runs stay
visible, rows are never overwritten) rather than as free files, so a receipt inherits the
registry's integrity properties instead of needing its own.

## SD-X-03 — The evidence surfaces stay fail-closed and quarantined

**Smoke quarantine (SEC-X-02).** The `smoke_only` stamp travels with the plumbing fixture's
outputs; consuming surfaces assert its absence where evidence is required. December
exclusion is asserted on **record dates**, never folder names (R-136, the TEC-09 lesson).
D-11's freight (not December-representative; provisional Dst characterises selection only)
is carried on every surface that cites the window.

**Generated evidence artifacts (SEC-X-03, W-9).** The matrix, the 13-row bounded acceptance
table (WS-01 plus WS-09…WS-20; a deferral is a raise) and `environment_and_cpu_preflight_report`
are **generated paths that refuse** — never hand-assembled, so a missing input is a failure
rather than a blank cell. The clean run **compares** against the manifest's frozen
expectations (exact classes by equality, toleranced classes against declared tolerances with
units) and never updates an expectation (SD-X-01's mechanism is what makes that stick at the
manifest).

**In-session gate (SEC-X-04).** Carried as designed upstream: lock-bound reuse, platform
resolved by `foundation`'s detection (which does not exist — unrunnable today), a `local`
stamp on a governed Kaggle run fails before domain work.

---

## Requirement coverage

The upstream table's 14 IDs, mapped to this design's sections. Statuses are the upstream
artifact's verbatim; nothing is upgraded here.

| Requirement | Design section | Status (upstream) |
|---|---|---|
| FR-WS-1 | SD-X-03 | `Pending` |
| FR-WS-2 | SD-X-03 (smoke quarantine) | not evidence — NO ROW, R-136 control (13) meanwhile |
| FR-WS-3 | SD-X-03 (record-date exclusion) | not evidence — NO ROW, R-136 control (14) meanwhile |
| FR-WS-4 | SD-X-03 (13-row bounded table) | `Pending` |
| FR-WS-5 | SD-X-03 (clean run compares) | `Pending` |
| FR-WS-6 | SD-X-02, SD-X-03 (in-session gate) | `Pending` |
| NFR-REP-01 | SD-X-01 (the manifest integrity its exact-equality classes rest on), SD-X-03 | `Pending` |
| REQ-NFR-A3 | SD-X-03 (in-session gate) | `Pending` |
| FR-WS-7 *(context — `foundation`'s)* | SD-X-03 | `Pending` — `aws_ai_dlc_preflight_report` does not exist |
| FR-P1-03-5 | SD-X-01 | not evidence — NO ROW, `UNTESTED` (WS-05 deferred to G-P3A) |
| REQ-ENG-4 | SD-X-03 | `Pending` |
| REQ-ENG-5 | SD-X-03 | `Pending` — TA-27 row owned by `governance-guards` |
| REQ-ENG-10 | SD-X-02 (receipts record the §13.1 items), SD-X-03 | not evidence — UNTESTED by design |
| NFR-PHASE-01 | SD-X-03 (Phase 2 invocations raise) | `Pending` |

**Derived and printed**: 3 design sections (SD-X-01…SD-X-03); **14** coverage rows, matching
the upstream `security-requirements.md`'s 14 exactly (same ID set, set-differenced:
+0 / −0); **4** rows carrying no evidence, restated verbatim from upstream (FR-WS-2, FR-WS-3,
FR-P1-03-5 — NO ROW; REQ-ENG-10 — UNTESTED by design); **0** rows claimed satisfied; **0**
scientific values decided; **2** mechanisms specified and unrunnable today (the lock-bound
checks, blocked on `configs/` and `foundation`'s platform detection).

## Assumptions & Open Questions

- **[Q1]** The agreement test (sibling vs D-number hash) parses `evidence/DECISIONS.md` in
  **test apparatus**, not in the loader — the loader stays format-stable. If DECISIONS.md's
  format defeats reliable extraction at 3.5, the fallback is a machine-readable freeze-record
  sidecar cited by the D-number, and that fallback is said here so 3.5 does not improvise it.
- **[Q1]** The freeze act now writes two representations of one hash. The agreement check is
  what keeps them honest; a freeze that skips the D-number write fails the check — by design,
  since Q-31 makes the freeze a deliberate owner act.
- **[Q2]** Lock-bound receipts inherit the gate's stated limit: invisible to changes outside
  the §13.1 item set. Owed with the gate at G-07's evidence review, not resolvable here.
- **Carried — the loader chokepoint is unenforced** (R-132's convention unwritten); the two
  freeze acts are the owner's under Q-31 and no measured value exists to freeze; BLK-08 ↓
  checked not inherited; WS-02–WS-08 deferred to G-P3A (the 13-row bound).
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or
  claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T07:05:40Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `security-design.md` SD-X-01 step 3 (line 52–55) vs. `logical-components.md` component table row F7 (line 33), Shared resources table (line 103), Cross-cutting notes (line 108–109) | **The two artifacts under review name two different components as the owner of the sibling/D-number agreement check (Q1 = C step 3).** `security-design.md` states, in SD-X-01's own body, not a hedge: *"one check in `tests/test_clean_run.py`'s apparatus asserts sibling-file hash == D-number-recorded hash for every frozen manifest."* `tests/test_clean_run.py` is explicitly F5 in `logical-components.md` ("F5 \| `tests/test_clean_run.py` \| the amended §13.2 sequence verbatim, CPU with no GPU visible; comparison ledger (exact/toleranced per manifest) \| W-6"), and F5's own `Owns` column does **not** list the agreement check. `logical-components.md` instead assigns the identical check to a different, separately-defined component three times over: the component table's F7 row ("evidence generators \| ... the sibling/D-number **agreement check** (Q1 = C step 3)"), the Shared resources table ("`evidence/DECISIONS.md` freeze entries \| owner \| read-only, by **F7's** agreement check"), and Cross-cutting notes for 3.5 ("the sibling-file naming and the D-number extraction mechanism for **F7's** agreement check"). The component-boundary Mermaid diagram reinforces the F7 reading structurally: it draws `F7 --> F1` and `F7 --> F2` edges for exactly this read-path, but draws **no** `F5 --> F2` edge, so F5 (test_clean_run.py) has no modelled access path to F2 (the freeze-record pair) that SD-X-01's own claim requires it to read. A developer building from these two library-kind artifacts — the sole design output for 3.5 — is told two different things about which module hosts a security-critical integrity check, and the dependency graph in the second artifact does not even support the placement the first artifact asserts. This is exactly the kind of cross-artifact contradiction `project.md`'s sweep-every-representation corrections were adopted to catch, now surfacing as a disagreement between the two files of one `library`-kind deliverable rather than within a single file. | Pick one owner for the Q1 = C step-3 agreement check (F5 `test_clean_run.py` or F7 evidence generators) and correct the other artifact and the Mermaid diagram to match; if the intent is that F5 invokes F7 as part of the clean run, state that dependency explicitly and add the missing `F5 --> F7` (or `F5 --> F2`) edge. |
| 2 | Minor | Upstream `../nfr-requirements/security-requirements.md` review trail (its own appended `## Review` sections) | **The consumed upstream contract's own most recently appended review verdict is NOT-READY** (`## Review — 2026-09-01 re-verification after gate rejection`, Critical finding on a stale line-138 representation), yet the artifact's live content at that same line already carries the fix described by the *prior* terminal "READY" pass (the strikethrough-and-correction at the SEC-X-02 Status paragraph is present, matching the state that pass certified). The file was edited to append four separate `## Review` sections rather than replacing one, in tension with this stage's own reviewing convention ("replace, don't append a second one"), leaving the artifact's on-disk review history inconsistent with its on-disk content. This design's Sources section (line 20) cites SEC-X-01…SEC-X-04 as settled inputs without noting that the upstream artifact's own recorded governance state, as last appended, reads NOT-READY. Verified against this design's own claims: every fact this design draws from `security-requirements.md` (the 14-ID coverage set, the 4-no-evidence-row count, the loader-chokepoint concession, the SEC-X-04 unrunnable-today disclosure) matches the upstream artifact's *current* (corrected) content exactly — no defect propagated into this design — so this is a chain-of-custody/audit-hygiene flag on the upstream artifact, not a substantive defect in `security-design.md` or `logical-components.md` themselves. | Have the `nfr-requirements` stage's review trail reconciled — either append a closing pass confirming the line-138 fix and re-affirming READY, or replace the stacked sections per the stage's own review-update convention — before treating `security-requirements.md` as a closed, stable contract for future stages. |

### What was verified

- **Q1 = C honesty (owner ruling).** `tech-stack-decisions.md` TS-X-01 (lines 44–47) states the non-negotiable constraint (hash must sit outside the manifest) and explicitly routes the location choice to the owner under Q-31; `security-design.md` SD-X-01 correctly frames its answer as that ruling, not a fresh technical decision. Confirmed consistent.
- **Loader-chokepoint limit carried in the rule body.** SD-X-01's closing paragraph (lines 61–65) states the unenforced-chokepoint limit in the Requirement body of the PRIMARY artifact, not only under `## Assumptions & Open Questions` (which also restates it, redundantly but not defectively) — satisfies the recurring defect pattern this project's `project.md` corrections warn about.
- **Q2 = A coherence with SEC-X-04.** SD-X-02's "same discriminator SEC-X-04's Q1 = A fixed for gate reuse" claim checked against `security-requirements.md` SEC-X-04 (lines 196–209): both use lock-identity-vs-clock as the staleness discriminator. Consistent.
- **Coverage completeness, set-differenced and printed.** Upstream `security-requirements.md`'s 14-row coverage table (FR-WS-1…7, FR-P1-03-5, REQ-ENG-4, REQ-ENG-5, REQ-ENG-10, NFR-PHASE-01, NFR-REP-01, REQ-NFR-A3) against this design's 14-row table: **same 14 IDs, set-differenced +0/−0.** The "4 rows carrying no evidence" claim (FR-WS-2, FR-WS-3, FR-P1-03-5 — NO ROW; REQ-ENG-10 — UNTESTED by design) reproduces upstream's *current, corrected* figure exactly and is independently confirmed against `requirements.md` (FR-P1-03-5 `UNTESTED` at line 364/912; REQ-ENG-10 `UNTESTED` at line 271; FR-WS-2/FR-WS-3 `UNTESTED` at lines 457–458). No status is upgraded from upstream anywhere in the coverage table (checked cell-by-cell against both `security-requirements.md` and `tech-stack-decisions.md`).
- **Scientific-value discipline.** No measured runtime, tolerance, row-count range or storage figure is stated in either artifact; D-11/D-14/D-18 are cited by reference, never restated with values; both freeze acts are consistently described as the owner's under Q-31; the banner and closing bullets in both files disclose the same standing blockers (no interpreter, `configs/` absent, TensorFlow pin `TBD`, G-09 preconditions UNMET) without claiming any discharged.
- **"2 mechanisms specified and unrunnable today" claim.** Traced to SD-X-02 (receipt/gate lock-bound validity, blocked on `configs/` having nothing to hash) and the in-session gate covered in SD-X-03/SEC-X-04 (blocked on `foundation`'s non-existent `resolve_platform_roots`) — exactly two, matching the printed count.
- **Sensor / structural checks.** `security-design.md` carries 6 H2 sections, `logical-components.md` carries 7 — both ≥ 2. Both files state the absence of `performance-requirements.md`, `scalability-requirements.md` and `reliability-requirements.md` as scope-designed, per the `library`-kind exclusion.
- **D-14 currency.** This design correctly treats D-14 (scientific fixture, March 2022) as frozen, matching `business-logic-model.md`'s explicit note that any record still calling the scientific window "open under Q-31" is "stale on disk" (corrected 2026-08-22 under `UG-08`) — `team.md`'s memory layer is the stale one here, not this design.

### Coverage limits

- Cross-unit spot-checks (this unit names no other unit's entity/service/workflow ID as an integration point beyond citations already resolved via the shared `unit-of-work.md`/`business-rules.md` chain within this unit's own directory) were not needed; no sibling unit's `construction/<other-unit>/` content was read.
- The upstream `security-requirements.md` review-trail inconsistency (Finding 2) was read as context for chain-of-custody, not re-litigated on its substantive merits — that stage's gate is closed to this pass.

### Summary

The two `library`-kind artifacts are disciplined on the axis this project cares most about — no measured value is stated, no upstream status is upgraded, the coverage set matches upstream exactly (14=14, 4-of-14 correctly flagged no-evidence), and the recurring "concession buried in Assumptions only" defect family this project has hit repeatedly elsewhere is avoided here (the loader-chokepoint and unrunnable-gate disclosures are both in the rule bodies). But the two artifacts directly contradict each other on which component (F5 `test_clean_run.py` or F7 evidence generators) implements the Q1 = C step-3 agreement check that is this design's own centerpiece answer to "how do we know the freeze-record pair wasn't silently re-edited" — and the component-boundary diagram in the second artifact does not even model the dependency the first artifact's claim requires. A developer cannot implement from these two documents without asking which file the check belongs in.

NOT-READY

## Review — iteration 2 (terminal)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T07:08:10Z
**Iteration:** 2 (terminal)

### Verification of the iteration-1 repair

**Finding 1 (Major — ownership contradiction) — RESOLVED.** SD-X-01 step 3 (lines 52–59)
now reads: "one check, owned by the evidence-generator component (`logical-components.md`
F7)," with a dated correction box naming the finding, quoting the superseded text verbatim
("one check in `tests/test_clean_run.py`'s apparatus"), and stating the reconciled reading:
"F7 owns the check; the clean-run suite is where F7's checks execute, not their owner."
Cross-checked against `logical-components.md`, unchanged since iteration 1 and requiring no
edit of its own:
- Component table F7 row (line 33) still assigns "the sibling/D-number **agreement check**
  (Q1 = C step 3)" to F7, unchanged.
- Shared resources table (line 103) still reads "read-only, by F7's agreement check," unchanged.
- Cross-cutting notes (lines 108–109) still read "F7's agreement check," unchanged.
- The Mermaid diagram still draws `F7 --> F1` and `F7 --> F2` (lines 58–59) and still draws
  no `F5 --> F2` edge — F5's only edge is `F5 --> F1` (line 54).
Both artifacts now name one owner (F7) for the Q1 = C step-3 check, matching the diagram's
modelled read-access paths. Grepped `security-design.md` for every remaining `F5`/
`test_clean_run`/`F7` occurrence (lines 22, 53, 57–59, 62, 156, 178, 199): the only other
site is the correction box itself, quoting the superseded claim as a quotation, not asserting
it live — no second site needed a sweep.

**Residual note, not a blocking defect.** The correction box's closing clause — "the
clean-run suite is where F7's checks execute, not their owner" — is prose distinguishing
execution locus from design ownership (a check can run when the test suite is invoked while
still being conceptually owned by F7), not a data-flow claim; the Mermaid diagram is scoped
to read-access paths, not test-invocation wiring, so this clause does not require a new edge
to avoid contradiction. It does leave one thing genuinely unresolved — precisely which test
module's code contains the F7 agreement-check assertion is still not named (`security-design.md`'s
own "Owed" list at `logical-components.md` lines 108–109 already flags this as owed to 3.5,
correctly scoped as an implementation-mapping detail rather than an architectural gap).

**Finding 2 (Minor — upstream review-trail hygiene) — CONFIRMED NOT RE-OPENED.** No edit was
made to `../nfr-requirements/security-requirements.md`: its four appended `## Review` sections
(lines 271, 306, 339, 373) are unchanged from iteration 1, and `git status`/`git diff` on that
path show no modification. The finding was correctly left as a record-only chain-of-custody
flag for the `nfr-requirements` stage's own gate, not treated as this stage's repair scope.

### Regression hunt

- **F5's Owns column, Failure-domains table, Shared-resources table** — unchanged; F5's row
  (line 31) still lists only "the amended §13.2 sequence verbatim... comparison ledger," no
  agreement-check ownership. The Failure-domains table's F7 row (line 91, "Freeze act skips
  the D-number write | F7 | agreement check fails") is unchanged and consistent with F7
  ownership.
- **Mermaid edges** — unchanged, `F7 --> F1`, `F7 --> F2` present, `F5 --> F2` absent, as
  required by the resolved reading.
- **14-row coverage set** — re-checked: same 14 IDs as upstream `security-requirements.md`,
  set-differenced +0/−0 (unchanged table, lines 126–141).
- **4-carry-no-evidence figure** — unchanged (FR-WS-2, FR-WS-3, FR-P1-03-5 — NO ROW;
  REQ-ENG-10 — UNTESTED by design), restated verbatim from upstream.
- **No measured value stated** — banner and closing bullets unchanged; still zero measured
  runtimes/tolerances/row-counts/storage figures in either artifact.
- **Freeze acts remain the owner's** — unchanged framing throughout ("the owner's under
  Q-31"), no freeze act attributed to this design.
- **No status upgraded** — the coverage table's Status column is still stated as "the
  upstream artifact's verbatim; nothing is upgraded here" (line 124), and cell-by-cell values
  are unchanged from iteration 1's verified state.

No new contradiction was introduced by the repair.

### Coverage limits

- Cross-unit spot-checks: not needed, same as iteration 1 — this unit names no other unit's
  entity/service/workflow ID as an integration point beyond citations already resolved inside
  this unit's own directory chain; no sibling unit's `construction/<other-unit>/` content was
  read.
- The upstream `security-requirements.md` review-trail stack (finding 2) was read only to
  confirm it was not edited; its substantive resolution remains that stage's own gate, out of
  this pass's scope.

### Summary

The repair resolves the sole Major finding cleanly: both artifacts now name F7 as the owner
of the Q1 = C step-3 agreement check, the correction box quotes and supersedes the prior
claim rather than silently replacing it, and the Mermaid diagram — unchanged and already
correct — now matches the prose in both files. No other site in either artifact still
asserted the superseded F5-ownership claim, so no sweep was skipped. The regression hunt
found no new contradiction in the F5 row, the failure-domain table, the shared-resources
table, the coverage set, the no-evidence count, or the freeze-ownership framing. The Minor
finding on the upstream review trail was correctly left unedited and record-only. A developer
can now implement the Q1 = C step-3 check from these two documents without ambiguity about
which component owns it.

READY

## Review — 2026-09-05 post-gate repair verification

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T07:58:09Z
**Iteration:** 1 (fresh budget after gate rejection)

### Verification of governance Recommendation 7

**Landed, in the rule body, dated, and routed correctly.** SD-X-02 (lines 99–107) carries a
second, separately-labelled limit — *"added 2026-09-05 at the stage gate, governance
Recommendation 7"* — stating in the RULE BODY, not only under `## Assumptions & Open
Questions`: *"receipts carry no tamper-evidence"*; that *"one convenience edit of a receipt's
recorded lock makes both fixtures appear passed in the current environment"*; and that this
threatens exactly the artifact R-140's ordering check and G-07's evidence rest on. The
sentence *"The design does not claim this closed"* is verbatim the same disclosure idiom
SD-X-01 already uses for the loader-bypass hole (*"The design does not claim this closed"*,
line 68–69) — the same idiom, not a weaker or stronger one, confirming point 2 of the
verification brief. The routing to 3.5 is explicit and concrete: *"record receipts through
`foundation`'s append-safe registry rows (the NFR-AUD-01 surface — failed runs stay visible,
rows are never overwritten) rather than as free files, so a receipt inherits the registry's
integrity properties instead of needing its own."*

**Companion artifact carries the matching owed line.** `logical-components.md`'s Cross-cutting
notes for 3.5 (lines 108–112) read: *"the receipt recording surface — prefer `foundation`'s
append-safe registry rows over free files, so receipts inherit tamper-evidence (SD-X-02's
stated limit, governance Recommendation 7)."* Same mechanism (append-safe registry rows),
same rationale (tamper-evidence), same citation back to SD-X-02 and to Recommendation 7 by
name. The two representations agree.

### Regression hunt

- **SD-X-01 (Q1 = C, F7-owned agreement check)** — untouched by this edit. Still reads "one
  check, owned by the evidence-generator component (`logical-components.md` F7)" with the
  iteration-1/2 correction box intact, quoting the superseded F5 claim as a quotation only.
- **SD-X-02's lock-bound validity mechanics** — the pre-existing paragraphs (lines 77–97:
  staleness-as-derived-fact, durability-self-answering, ordering-inside-receipts, the
  §13.1-completeness inherited limit) are unchanged; the Recommendation 7 text is appended
  after them as a clearly delimited "second limit," not interleaved with or rewording the
  original mechanics.
- **14-row coverage table / "4 carry no evidence"** — unchanged (FR-WS-2, FR-WS-3, FR-P1-03-5
  — NO ROW; REQ-ENG-10 — UNTESTED by design); the derived-and-printed summary line (153–158)
  still reads 14/14, +0/−0, 4 no-evidence, 0 satisfied, 0 scientific values, 2 unrunnable
  mechanisms — same figures as iteration 2.
- **F1–F7 consistency** — `logical-components.md`'s component table, Mermaid diagram
  (`F7 --> F1`, `F7 --> F2`, no `F5 --> F2`), and Failure-domains table are otherwise
  unchanged from iteration 2's verified state.
- **Nothing newly claimed satisfied** — the new SD-X-02 text explicitly disclaims closure
  ("The design does not claim this closed") and the banner/closing-bullets discipline (no
  measured value, freeze acts the owner's, G-09 preconditions UNMET) is unchanged in both
  files.
- **Freeze acts still the owner's** — both new passages describe the receipt-recording change
  as a routing to 3.5's implementation, not a freeze act; Q-31 ownership is not touched.

### New finding

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Minor | `logical-components.md` Failure domains and blast radius table (line 88), row "Receipt lost or environment changed \| F4 \| full-year job blocked, fixtures re-run \| fail-closed by lock-binding; cost, never a wrong result" | This row's containment claim — **"never a wrong result"** — is stated as a blanket property of the F4 failure domain, but SD-X-02's newly landed Recommendation-7 text describes a distinct F4 failure mode (a tampered/edited receipt) for which the design explicitly does **not** claim containment: *"one convenience edit of a receipt's recorded lock makes both fixtures appear passed in the current environment... The design does not claim this closed."* That is a wrong result (a false pass), not merely a blocked run or a cost. The Failure-domains table — the artifact's own per-domain risk/containment register, and the natural place a developer checks "what can go wrong with F4 and is it contained" — has no row for the tamper case and, read alongside the one row it does have for F4, could be misread as covering it. This is the same class of gap `project.md`'s "sweep every REPRESENTATION of a corrected fact" correction exists to catch, one representation short of complete: SD-X-02's body and the Cross-cutting-notes owed line both landed; the Failure-domains table — a third representation of the same F4 risk surface — did not. It does not misstate what was built (nothing is newly claimed satisfied) and does not block READY on its own. | Add a second F4 row to the Failure-domains table — e.g. "Receipt edited/tampered in place \| F4 \| both fixtures appear passed on a full-year job \| **not contained today** — no tamper-evidence on the free-file receipt; routed to 3.5 as an append-safe registry row" — so the table's containment language for F4 does not read as broader than SD-X-02 now states it to be. |

### Coverage limits

- Cross-unit spot-checks: not needed — this pass re-verifies a single-unit repair; no new
  integration point was introduced, and no sibling unit's `construction/<other-unit>/` content
  was read.
- The upstream `security-requirements.md` review-trail hygiene item (iteration 1's Finding 2)
  was re-checked only for "not reopened, not touched by this edit" — confirmed unchanged — its
  substantive resolution remains that stage's own gate.

### Summary

Governance Recommendation 7 landed exactly where the gate ruling required: SD-X-02's rule
body states the receipt tamper-evidence limit with a dated note and the idiom this project
already uses for an unclosed gap ("The design does not claim this closed"), and routes the fix
to 3.5 via `foundation`'s append-safe registry rows; `logical-components.md`'s Cross-cutting
notes state the matching owed line, citing SD-X-02 and Recommendation 7 by name. The
regression hunt found no repair-introduced defect: SD-X-01's F7 ownership, SD-X-02's original
lock-bound mechanics, the 14-row coverage table, the 4-no-evidence count, and the
freeze-ownership framing are all unchanged. One new Minor finding — the Failure-domains
table's "never a wrong result" containment claim for F4 was not extended to name the newly
disclosed tamper case as a distinct, uncontained risk — is a completeness gap in a third
representation, not a contradiction of what Recommendation 7 asked for, and does not block
approval.

READY
