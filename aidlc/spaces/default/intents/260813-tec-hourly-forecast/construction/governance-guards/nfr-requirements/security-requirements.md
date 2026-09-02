# Security Requirements — `governance-guards`

**Unit** `governance-guards` (Bolt 2) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NOTHING HERE IS CLAIMED SATISFIED — AND ONE REQUIREMENT IS CURRENTLY BREACHED
>
> **WS-18 and TA-18 are NOT discharged.** `tests/test_locked_test_guard.py` is written but
> **UNEXECUTED** — no Python interpreter exists in this environment. **TA-27 and TA-28 are
> `Pending`.** `src/data/locked_test.py` and `open_restricted` **do not exist**.
> **G-09 is signed (D-31, 2026-08-28) with its own §18.3 preconditions UNMET**; **stage 3.1
> remains FAIL**; **BLK-07 is open and stays open**, and is a precondition of Bolt 3.
>
> **SEC-G-01 is breached today at two named sites.** That is stated as a live finding
> below, not as a risk.
>
> No scientific value is decided here, and TE §18.2's absolute rule stands.

## Sources

- `../functional-design/business-rules.md` — **R-23** (both phase-boundary limbs run; neither substitutes for the other), **R-24** (run time is authoritative, the static scan subordinate, both run — Q7 = D), **R-25** (the access log is durably appended **before** the December read begins — Q6 = C), **R-26** (what counts as a December hit; the bounded driver exclusion), **R-27** (the guard walks every file, dispatched per artifact class; an unparseable file is a failure), **R-28** (one path into the restricted root; the enumerated exemption; **BLK-07 is not this design's to close**), **R-29** (reuse is registered before use; reimplementation is the default).
- `../functional-design/business-logic-model.md` — **W-1**/**W-2**/**W-2a** (the import limb, the produced-field limb, the existing static scan and its declared subordinate role), **W-5** (the transition manifest), **W-6** (`diff_protected_hashes` and the G-P3C pass condition), **W-7** (a guarded read of the locked December root), **W-8**/**W-8a** (what counts as a December hit; scanning outside the restricted root), **W-9** (registering reused third-party source), **W-10** (one path in, and who may use it), **W-11** (what Bolt 2 builds and what it must not), § Requirement-to-workflow map.
- `../functional-design/domain-entities.md` — **§ 3** `RAW_MODULES`, **§ 7** `RESTRICTED_ROOT`, **§ 10** `RESTRICTED_LITERAL_EXEMPT_MODULES` (**five members**, membership asserted exactly), `AccessRecord`.
- `../../foundation/functional-design/business-rules.md` — **R-15** (the absence of a path; the rule W-10 generalises), **R-19** (the `AccessRecord` / `RegistryEvent` join on `run_id` with orphan detection both ways).
- `../../../inception/requirements-analysis/requirements.md` — **REQ-ENG-5**, **FR-P1-02-6**, **FR-P1-03-2**, **FR-P1-05-12**, **FR-P1-06-1** … **FR-P1-06-4**, **NFR-PHASE-01**, **NFR-LIC-01**, **NFR-AUD-01** *(added
  2026-09-01 on adversarial finding 2, Major — SEC-G-02's second Requirement paragraph
  reproduced NFR-AUD-01's substance while citing only R-19 and Vision §8.3, never the governing
  NFR ID. This is cause 3 of the stage-wide coverage defect: an NFR the artifact rests on, cited
  by its TE section rather than by its ID.)*.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§7.0** (the Phase 1 hard prohibition), **§7.0B** (the phase transition), **§10.1** (the code-reuse register), **§2.2** (the phase boundary), **§19** (TA-07, TA-08, TA-12, **TA-18**, TA-27, TA-28), **§16** (WS-18).
- `evidence/experiment_registry.md:79–83` — the recorded RES-04 hazard, cited by R-28 as *"occurring in fact rather than in principle"*.
- `nfr-requirements-questions.md` — Q1 = A, Q2 = B, and the receipted Consolidated Summary Confirmation.

---

## Scope note — why this unit has three fewer NFR artifacts

`produces_kinds` maps `performance-requirements`, `scalability-requirements` and
`reliability-requirements` to `[service]` / `[service, ui]`; this unit is
`kind: library`. The categories were assessed:

| Category | Assessment for `governance-guards` | Where it lives |
|---|---|---|
| **Performance** | One real constraint, and it is a **correctness** constraint rather than a speed target: R-25 requires the access-log append to be **durably completed before** the read begins, so the guard is deliberately not optimised for latency. R-27's whole-tree walk runs at test time, not in a serving path. | § SEC-G-01, § SEC-G-04 |
| **Scalability** | No load projection. The tree is one repository; the walk is bounded by file count. | — |
| **Reliability** | **Fail-closed** is the reliability posture: a log-write or durability failure must **prevent the read** (R-25); an unparseable file is a **failure**, not a skip (R-27). Stated here because both are security properties before they are availability properties. | § SEC-G-01, § SEC-G-04 |
| **Security** | This artifact. | — |
| **Observability** | `AccessRecord`, and its join to `RegistryEvent` on `run_id` with orphan detection **both ways** (`foundation` R-19). | § SEC-G-02 |

---

## SEC-G-01 — One door into the restricted root, and it is breached today

**Requirement.** Every read of **content** beneath `evidence/locked_test_restricted/`
routes through **`open_restricted`**. `open_restricted` **durably appends the
`AccessRecord` before the read begins**: a log-write failure **or** a durability failure
must **prevent the read** — not be reported alongside it, not be retried after it, not be
logged as a warning while the read proceeds (R-25, Q6 = C).

**Holding the literal is not an access; reading bytes is** (D-15, as scoped by R-28). The
restricted root is a **governance boundary, not an access control** — it holds only while
exactly one code path reaches content beneath it, and D-15's boundary *"does not weaken
slightly; it ends"*.

> ### ⛔ STATUS: BREACHED, at two named sites, today
>
> **Two exempt modules read content beneath the root with no `AccessRecord`** —
> `tests/test_release_hashes.py:137` and `tests/test_acquisition_window.py:195`. R-28
> states this in its own words as `evidence/experiment_registry.md:79–83`'s recorded
> **RES-04 hazard occurring in fact rather than in principle**, and that the 2026-08-28
> ruling **does not cure it** — it fixes which mechanism must.
>
> **Nothing is grandfathered.** `open_restricted` does not exist, so there is no guard for
> these reads to predate. Routing them through it is **owed at stage 3.5**, and this
> artifact names that remediation a **precondition of the G-05 evidence package** (Q1 = A).
>
> Until then, this unit's negative control cannot pass honestly, and **no artifact may
> describe the one-door property as enforced**.

**Acceptance.** `tests/test_locked_test_guard.py` proves the guard **rejects** an
unlogged read — the negative control, not only the happy path — and the two named sites
read through `open_restricted`. Evidence: the guard test plus an access-log sample
(TA-18), and WS-18. **Both are `Pending` and the test is unexecuted.**

## SEC-G-02 — Every access is recorded, and orphans are detected both ways

**Requirement.** Every locked-test access records **`locked_test_accessed = true`** in the
experiment registry. `AccessRecord` and `RegistryEvent` **join on `run_id`**, with
**orphan detection in both directions** (`foundation` R-19).

**Requirement — known pre-guard orphans are reported, never cleared** (**NFR-AUD-01**, R-19,
Vision §8.3). NFR-AUD-01 is the governing requirement for everything in this paragraph:
**registry writes are atomic or append-safe; a failed or aborted run stays visible with its
status and reason; a silent re-run is prohibited; no entry is deleted or overwritten.** *(ID
cited 2026-09-01 on adversarial finding 2, Major — the paragraph below already stated this
behaviour and named only R-19 and Vision §8.3.)* The **five
retrospectively logged December accesses**, and the **one possible unauthorized access
`GOV-2026-08-28-FD-01` Recommendation 31 records as expressly unresolved**, are reported
as known pre-guard orphans. **No registry row is ever back-filled to clear them.**

**Requirement.** December opens **once** for the one-shot post-G-05 evaluation, predictions
hashed **before** any metric — and that is a **separate event** from the **required,
performance-blind pre-G-05 December coverage and regime audit**, which must **not** be
blocked by this guard. A guard that blocked it would breach Vision §8.3 as surely as one
that let a model see December.

**Status.** `Pending`. The registry half is `foundation`'s (W-6 step 8); this unit owns the
`AccessRecord` half. R-19 is the **first** statement of the relationship — zero of the
twelve units' artifacts named both entities before 2026-08-28 — and neither side is built.

## SEC-G-03 — The restricted-root literal is bounded to an exact list of six

**Requirement.** A static check asserts that **no module outside the exemption contains the
restricted-root literal**, and that the exemption list's membership is **exactly** its
declared members.

**The list is five members in addition to the chokepoint — six counting
`src/data/locked_test.py`**, the convention R-28's box uses:

| # | Module | Class | Route for content reads |
|---|---|---|---|
| chokepoint | `src/data/locked_test.py` | production | is the door |
| 1 | `tests/test_locked_test_guard.py` | test | synthetic fixture root |
| 2 | `tests/test_acquisition_window.py` | test | **breached today — see SEC-G-01** |
| 3 | `tests/test_phase_boundary.py` | test | names the root, reads no content |
| 4 | `tests/test_release_hashes.py` | test | **breached today — see SEC-G-01** |
| 5 | `scripts/merge_coverage_year.py` | **production script, not a test** | `open_restricted`, owed at 3.5 |

**Member 5 is why membership is an exact enumerated list and never a `tests/` directory
predicate.** A directory predicate would have missed a production script that holds the
literal, which is precisely how the fifth member went unnoticed until the 2026-08-29
full-repository sweep.

**The membership test fails in both directions**: an unlisted module holding the literal
fails the static check, and a listed module that no longer needs it fails the membership
test until the list is edited. A **seventh** holder cannot appear silently.

> **Upstream correction applied 2026-08-31, on the project decision owner's approval to
> annotate in place.** Four live sites in this unit's approved `functional-design` still
> asserted the superseded count of **four** — `business-logic-model.md` W-10's mechanism
> sentence and its "four modules" restatement, `business-rules.md` **R-28's own Rule
> statement**, and the 2026-08-28 ruling box's "no fourth" — while `domain-entities.md` § 10
> and R-28's own box already carried five/six. All four are annotated with superseded
> figures preserved. Root cause: the 2026-08-29 repair swept only the five sites its finding
> enumerated (`project.md` `fd-2026-08-30-sweep-derive-sites`). **A change record under
> `governance/` may be owed and is the owner's to file.**

## SEC-G-04 — The static check is AST-based, and its residual is stated

**Requirement (Q2 = B).** The restricted-root static check is **AST-based with constant
folding**, so a path assembled from **concatenated or joined string literals** —
`EVIDENCE_DIR / ("locked_test" + "_restricted")`, an `os.path.join` of literal parts — is
caught, not only an exact literal.

**Residual, stated rather than hidden.** A **genuinely dynamic** path — a value read from
config, an environment variable, a name computed at run time — **still passes** the static
check. The blind spot **narrows; it does not close.**

**What carries enforcement instead.** **R-24's hierarchy is unchanged**: the static `ast`
scan is the **early-warning** limb, the **run-time assertions are authoritative**, and both
run. A static scan of a local checkout constrains nothing about a Kaggle session.
`open_restricted` is the content chokepoint, so a computed path still cannot read content
without passing through it — which is why the residual is tolerable and why SEC-G-01's
breach, which bypasses the chokepoint entirely, is not.

**Fail-closed on unparseable input.** R-27: the guard walks **every** file, dispatched per
artifact class, and an unparseable file is a **failure**, never a skip. A guard that skips
what it cannot read reports a cleanliness it never checked.

**Technique already in use.** `tests/test_phase_boundary.py` (266 lines) already walks
`src/` and `scripts/` with `ast`, so constant folding is an increment on an existing
technique rather than a new mechanism. **The check is itself code and needs its own test.**

**The second scan this section carries: December-bearing artifacts outside the restricted
root (W-8a, FR-P1-02-6).** The residency check is distinct from the literal check above and
from SEC-G-01's content chokepoint — it asks not "who may name the root" but **"has December
content escaped it"**. Its hit definition is R-26's, including the **bounded driver
exclusion**, and R-27's per-artifact-class dispatch with **unparseable-file-is-a-failure**
governs the walk. **`FR-P1-02-6` carries no acceptance row at all**, so this scan has no §16
or §19 evidence obligation attached to it — recorded here because a requirement with no row
is the one most likely to be read as covered by a neighbouring row that does not cover it.

## SEC-G-05 — The phase boundary is enforced on two limbs, neither substituting for the other

**Requirement (NFR-PHASE-01, TE §7.0).** Phase 1 code paths must not import or execute
raw-processing modules, nor produce DCB/STEC/mapping/satellite/arc fields. `RAW_MODULES` is
**four** modules — `rinex`, `calibration`, `target`, `verification` — not two; FR-P1-03-2's
earlier two-module wording was corrected under finding `IMPL-2`, and
`tests/test_phase_boundary.py` already encodes all four.

**Requirement.** **Both limbs run** (R-23) — the **import** limb and the **produced-field**
limb — and **neither substitutes for the other**. `assert_no_raw_fields` is called by **each
of the eight Phase 1 producing scripts before it writes**, and a **completeness test asserts
every one of them calls it** before its first write.

**Requirement (TE §7.0B, gate G-P3C).** Phase 2 refuses to train if any **protected hash**
differs. Phase 1 fitted weights are **never** carried into Phase 2, and no Phase 1 result may
motivate a Phase 2 model or evaluation change, absent a separately approved,
exploratory-labelled transfer-learning experiment.

**Status.** TA-27 (`Pending`) requires the phase-boundary test **and** a
transition-manifest hash-diff test; TA-28 (`Pending`) covers `diff_protected_hashes` and the
G-P3C pass condition. `FR-P1-02-6` carries **no acceptance row at all**.

## SEC-G-06 — Reuse is registered before use; reimplementation is the default

**Requirement (R-29, NFR-LIC-01, TE §10.1, gate G-P2).** Any reused or materially adapted
third-party source is recorded in the §10.1 register **before the code is used**, with the
full field set — `reuse_id`, repository URL, immutable commit or tag, upstream file and line
or function, retrieval date, licence and SPDX ID, copied-versus-adapted status, destination
file, scientific purpose, modifications, tests, original citation, notice location, reviewer
and approval date.

**Reimplementation is the default**, not the fallback: source whose licence is absent,
ambiguous or incompatible is **not copied or materially adapted** — the published method is
reimplemented from the paper with a citation. The AGPLv3 Global-TEC-forecasting repository is
the one approved direct-copy source today, and whether its repository-distribution
obligations permit that copying is a **governance dependency this project does not resolve on
its own**.

**Status.** `Pending`. `src/data/reuse_registry.py` and `tests/test_reuse_registry.py` do
not exist. G-P2 is unaffected by G-09's signature.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Row primary owner | Status |
|---|---|---|---|---|
| REQ-ENG-5 | SEC-G-05 | WS-10, TA-07, TA-08, TA-12, TA-27 | mixed; TA-27 **this unit** | `Pending` |
| **FR-P1-02-6** | **SEC-G-03, SEC-G-04** *(corrected 2026-08-31 on adversarial finding 1, Major; superseded cell preserved: `SEC-G-02`. The requirement is W-8/W-8a's December-bearing-artifact residency and the per-class scan, which live in SEC-G-03's literal bounding and SEC-G-04's scan — not in SEC-G-02's `AccessRecord`/`RegistryEvent` orphan detection.)* | ⚠ **NO ACCEPTANCE ROW** | — | untested |
| FR-P1-03-2 | SEC-G-05 | TA-27 | `governance-guards` | `Pending` |
| FR-P1-05-12 | SEC-G-01, SEC-G-02, SEC-G-03 | **WS-18, TA-18** | `features-and-splits` | `Pending` — **and BREACHED** |
| FR-P1-06-1 | SEC-G-05 | TA-27 | `governance-guards` | `Pending` |
| FR-P1-06-2 | SEC-G-05 | TA-27 | `governance-guards` | `Pending` |
| FR-P1-06-3 | SEC-G-05 | TA-28 | `governance-guards` | `Pending` |
| FR-P1-06-4 | SEC-G-05 | TA-28 | `governance-guards` | `Pending` |
| NFR-PHASE-01 | SEC-G-05 | TA-27 | `governance-guards` | `Pending` |
| NFR-LIC-01 | SEC-G-06 | TA-28 | `governance-guards` | `Pending` |
| **NFR-AUD-01** | SEC-G-02 | **TA-10, TA-21** *(TA-21 added 2026-09-01 on the repair-verification Minor; superseded cell preserved: `TA-10` alone. `requirements.md` carries both rows for NFR-AUD-01, and citing one silently narrowed the requirement's acceptance surface.)* | **not this unit** — the registry's owner | `Pending` |

**Derived and printed**: 6 requirement sections (SEC-G-01…SEC-G-06); **11** coverage rows *(count
re-derived 2026-09-01 on adversarial finding 2, Major; superseded figure preserved: **10**)*;
**0** rows claimed satisfied; **1** requirement recorded as **actively breached**.

**The row count no longer matches the map, and that is the point.** It was previously stated as
"**10** coverage rows, matching `functional-design`'s *10 requirements, 1 without an acceptance
row*" — and matching the map was exactly the defect. **NFR-AUD-01 is not in this unit's map**;
SEC-G-02 reproduces its substance anyway, so it is covered here. The test is **whose text these
artifacts reproduce, whoever owns the row** — not which requirements the unit owns. The map now
accounts for **10 of the 11** rows.

## Assumptions & Open Questions

- **[Q1]** SEC-G-01's breach remediation is named a **precondition of the G-05 evidence package**. That naming is this stage's, derived from R-28's assignment of the remediation to stage 3.5 plus the fact that the guard evidences WS-18/TA-18; **it is not a supervisor ruling** and the owner may place it elsewhere.
- **[Q2]** The static check is AST-based with constant folding. **The dynamic-path residual is not closed** and is not claimed to be.
- **[assumption]** The AST check runs on Python source only. Neither the exemption list nor R-27's per-class walk states what happens if the restricted-root literal appears in a **notebook** (`.ipynb`), a YAML config, or a Markdown artifact. `W-8a` scans for December-**bearing artifacts** outside the restricted root, which is a related but distinct obligation. Raised, not resolved.
- **Carried, not decided here — BLK-07 is open and stays open**, and is a **precondition of Bolt 3**. Four units reach the root through `open_restricted`'s caller allowlist, which couples this root unit to four downstream consumers; R-28 names that coupling as the accepted cost.
- **Carried — the `AccessRecord` / `RegistryEvent` reconciliation is a joint obligation.** `foundation` W-6 designs the registry half; this unit owns the `AccessRecord` half. Neither is built.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row or test as discharged. **SEC-G-01 is recorded as breached, which is the opposite of a claim.**

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-31T00:00:00Z (see note below — sandboxed clock check unavailable; taken from system-provided current date)
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `security-requirements.md` § Requirement coverage, `FR-P1-02-6` row | The coverage table maps `FR-P1-02-6` to **`SEC-G-02`** ("Every access is recorded, and orphans are detected both ways" — the `AccessRecord`/`RegistryEvent` join). But every upstream source for this requirement points elsewhere: `functional-design/business-logic-model.md:1007` maps it to **W-8, W-8a**; `functional-design/domain-entities.md:641` maps it to **`RESTRICTED_ROOT` guard, `DriverExclusionList`**; `functional-design/business-rules.md:1143-1144` maps it to **R-26** ("what counts as a December hit") and **R-27** ("the recursive per-class walk"). None of those upstream mappings is about access recording or orphan detection — they are all about restricted-path residency and the per-class scan, which in this artifact's own structure live in **SEC-G-01** (one door, R-25/R-28) and **SEC-G-04** (AST scan, explicitly citing R-27's "unparseable file is a failure"). This is a mapping error introduced at this stage (upstream mapped it correctly to W-8/W-8a/R-26/R-27; this artifact's translation into its own SEC-G-* numbering sent it to the wrong section). An implementer tracing `FR-P1-02-6` from this table to find what work item covers it lands on the wrong requirement text. | Re-point the `FR-P1-02-6` row to `SEC-G-01`/`SEC-G-04` (or add it as a cross-listed row the way `FR-P1-05-12` is cross-listed across three sections), and correct the "Section here" column so it names a section whose Requirement prose is actually about restricted-path residency / the per-class walk, not access-log orphan detection. |
| 2 | Minor | `security-requirements.md` § SEC-G-03 correction box (lines 128–136) | The box asserts four specific upstream sites were annotated 2026-08-31 (`business-logic-model.md` W-10's mechanism sentence and "four modules" restatement, `business-rules.md` R-28's Rule statement, the 2026-08-28 "no fourth" ruling box). Spot-checked against `business-rules.md` R-28 (lines 864–876, 934–940) and `business-logic-model.md` W-10 (lines 863–903): the annotations are present, in the `~~four~~ ⛔ five/six` strikethrough-preserve pattern this project's own learned convention requires, and no live site asserts the superseded "four" in the text I read. This is not a defect — recorded as a positive confirmation, not a finding requiring action. |

### Validation Tool Results

No validation tools are declared in this stage's frontmatter (`.claude/aidlc-common/stages/construction/nfr-requirements.md`) beyond the standard sensor set; none were run as machine checks beyond the grep-based cross-reference derivations shown above and in the findings.

### Coverage limits (8-call budget)

Verified: stage frontmatter `produces`/`produces_kinds` (confirms only `security-requirements.md` and `tech-stack-decisions.md` are unconditional for `kind: library` — the scope note's claim is correct, no missing-artifact defect); the exempt-module count (5 in addition to the chokepoint, 6 counting it) at every site read, and the four claimed 2026-08-31 upstream annotations; the breach claim (SEC-G-01 stated breached at `tests/test_release_hashes.py:137` / `tests/test_acquisition_window.py:195`, never softened anywhere in either artifact); the no-satisfaction claim (both artifacts print "0 rows claimed satisfied" and it holds on inspection); `RAW_MODULES` = four (`rinex`, `calibration`, `target`, `verification`), correctly transcribed and correctly left alone; R-24's hierarchy, R-25's durable-append-before-read, R-27's unparseable-file-is-a-failure, all transcribed correctly in both artifacts; the derived counts (6 sections / 10 rows in security; 4 sections / 8 rows in tech-stack) recomputed by hand from each table and both are correct; requirements.md's "10 requirements, 1 without an acceptance row" claim, cross-checked against `business-logic-model.md`, `domain-entities.md` and `business-rules.md`, all agreeing at 10/1 (`FR-P1-02-6`). Not independently re-verified within budget: the `foundation/nfr-requirements/tech-stack-decisions.md` cross-reference content itself (the reviewer read-scope hook refuses reads into `construction/foundation/` even though the dispatch names it as a granted exception — the hook's own per-path check rejected the combined command; re-attempting as an isolated single-path call was not spent given remaining budget), and the acceptance-row IDs (WS-10, TA-07/08/12/18/27/28) were not traced into their owning §16/§19 checklist text.

### Summary

Both artifacts are disciplined about not claiming anything satisfied, consistently state the SEC-G-01 breach without softening, and correctly carry forward the exemption-count and RAW_MODULES corrections from `functional-design`. The one real defect is a broken internal cross-reference: `FR-P1-02-6`'s coverage row points at the wrong SEC-G section, inconsistent with every upstream mapping for that requirement. One Major finding, zero Critical — does not meet the NOT-READY bar (which needs a Critical or >2 Major), so the artifact is READY subject to fixing finding #1.

## Review — 2026-09-01 confirming pass

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T05:11:26Z
**Iteration:** 2 (fresh budget after gate rejection; artifacts unchanged since prior READY)

### Prior finding status

- **Finding #1 (Major, `FR-P1-02-6` mismapped to `SEC-G-02`)** — **RESOLVED.** Line 221's coverage row now reads `SEC-G-03, SEC-G-04`, annotated `corrected 2026-08-31 on adversarial finding 1, Major`, with the superseded `SEC-G-02` cell preserved as a strikethrough-style note rather than silently dropped. Confirmed against the same three upstream sources the original finding cited (`business-logic-model.md`, `domain-entities.md`, `business-rules.md` R-26/R-27) — the corrected mapping agrees with all three.

### New findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 2 | Major | `security-requirements.md` § SEC-G-02, lines 86-89 | This section's second Requirement paragraph reproduces `NFR-AUD-01`'s substance verbatim in effect — "No registry row is ever back-filled to clear them," pre-guard orphans "reported, never cleared" — which is exactly NFR-AUD-01's mandated behaviour ("registry writes must be atomic or append-safe; failed and aborted runs remain visible with status and reason; silent reruns are prohibited," per `team.md`/`project.md` § Mandated and `requirements.md`'s own NFR-AUD-01 row). `NFR-AUD-01` is never cited by ID anywhere in `security-requirements.md` or `tech-stack-decisions.md` (confirmed by grep — zero hits in either file), and § Sources (line 24) does not list it among the NFR IDs pulled from `requirements.md`. This is the exact defect pattern named in the dispatch (cause 3: "missing an NFR ID whose substance the artifacts rested on while citing its TE section directly") — here the artifact cites Vision §8.3 and R-19 directly but never the governing NFR ID. | Add `NFR-AUD-01` to § Sources' NFR list and cite it explicitly in SEC-G-02's Requirement paragraph, alongside R-19/Vision §8.3. |

### Requirement-coverage set-difference (the check that matters most)

Derived and printed: `requirements.md` carries eleven NFR IDs — `NFR-AUD-01, NFR-DET-01, NFR-DQ-01, NFR-FAIR-01, NFR-IRI-01, NFR-LEAK-01, NFR-LIC-01, NFR-PHASE-01, NFR-REP-01, NFR-SEC-01, NFR-TDEF-01`. Both `security-requirements.md` and `tech-stack-decisions.md` cite only `NFR-LIC-01` and `NFR-PHASE-01` by ID — nine of eleven are uncited by ID in either artifact. Of those nine, this unit's declared scope (restricted-root access, static AST checks, phase boundary, reuse registry — SEC-G-01 through SEC-G-06) is genuinely disjoint from eight of them (IRI denial, F10.7/lag leakage, comparison-wide masking, determinism/seeding, data-quality, reproducibility, target-definition, credentials — none of their substance appears anywhere in either artifact, confirmed by grep for their characteristic terms: zero hits for "append-safe," "leakage," "train-only," "comparison-wide mask," "credential," "secret"). The ninth, `NFR-AUD-01`, is not disjoint — its substance is reproduced in SEC-G-02 without the ID, which is finding #2 above. This is a narrower version of the seven-of-twelve pattern than the dispatch describes at the stage level: one real uncited-substance defect, not a wholesale coverage gap, because the other eight NFRs are legitimately out of this unit's scope by its own § Scope note (produces_kinds is `library`, and the scope note correctly narrows performance/scalability/reliability/observability to what SEC-G-01/02/04 actually need — that reasoning extends to the eight out-of-scope NFRs by the same logic, though the artifact never states it in those terms).

### Exempt-module count and numeral sweep

Confirmed at every site read (lines 22, 107, 119, 264): `RESTRICTED_LITERAL_EXEMPT_MODULES` is stated as **five members in addition to the chokepoint, six counting it**, with member 5 identified as `scripts/merge_coverage_year.py` (a production script). No stale "four" (numeral or spelled out) found anywhere in `security-requirements.md`; `tech-stack-decisions.md` contains no exempt-module-count language at all (zero matches on the sweep pattern), so it carries no stale figure to correct.

### Q1/Q2 answer fidelity

Q1 ("state it, breached at two sites") — confirmed: line 13 and the § SEC-G-01 status box both state the guarantee and name the breach as occurring at two named sites (`tests/test_release_hashes.py:137`, `tests/test_acquisition_window.py:195`), never softened to a mere risk. Q2 ("AST-based with constant folding") — confirmed in the SEC-G-04 **Requirement** body itself (line 140), not relegated to `## Assumptions`; the dynamic-path evasion residual is also stated in the rule body (lines 149-154), with only the narrower notebook/YAML/Markdown sub-question left to `## Assumptions & Open Questions` (line 239), which is a genuinely open scope question rather than a restatement of the AST/constant-folding mechanism itself.

### Not independently re-verified within budget

`tech-stack-decisions.md`'s full content beyond the grep sweeps above; the acceptance-row IDs' text in their owning §16/§19 checklists; whether the eight NFRs judged out-of-scope above are formally documented as out-of-scope anywhere upstream (this pass inferred it from absence of substance plus the unit's stated `kind: library` narrowing, not from an explicit upstream scoping statement).

### Summary

One prior Major (`FR-P1-02-6` mismap) is confirmed resolved. One new Major surfaces on independent verification: `NFR-AUD-01`'s substance is reproduced in SEC-G-02 without ever citing the ID, matching the dispatch's named defect pattern. One Major, zero Critical — under the ≤2-Major rule this remains READY, but the citation gap should be closed before the next gate.

READY

READY

## Review — 2026-09-01 repair verification

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 3 (repair verification of the 2026-09-01 confirming pass's one new Major)

### Prior finding status

- **Finding #2 (Major, `NFR-AUD-01` reproduced in SEC-G-02 without ever citing the ID)** — **RESOLVED.** All four claimed repair sites are present and mutually consistent:
  1. § Sources (line 24) — `NFR-AUD-01` added to the `requirements.md` ID list, with a dated note naming this finding.
  2. § SEC-G-02 (lines 90-95) — the "known pre-guard orphans are reported, never cleared" Requirement paragraph now opens `(**NFR-AUD-01**, R-19, Vision §8.3)` and states the mandated behaviour explicitly (atomic/append-safe writes; failed or aborted runs stay visible with status and reason; silent re-runs prohibited; no entry deleted or overwritten).
  3. § Requirement coverage — new row `NFR-AUD-01 | SEC-G-02 | TA-10 | not this unit — the registry's owner | Pending` (line 239); the printed count moved **10 → 11**, superseded figure preserved verbatim (lines 241-243), with a paragraph (lines 245-250) explaining the count deliberately no longer matches `functional-design`'s map because matching the map was the defect.
  4. `tech-stack-decisions.md` (lines 118-123) — dependent phrase now reads "**three fewer** than `security-requirements.md`'s **eleven**", superseded "two fewer than ten" preserved in a parenthetical, and `NFR-AUD-01` added to the raise-no-technology-choice list with its rationale (append-safe registry write is `foundation`'s stack decision).

### Verification detail

- **Arithmetic.** 8 = 11 − 3 confirmed by direct recount: `tech-stack-decisions.md`'s coverage table (lines 108-116) has exactly 8 rows; `security-requirements.md`'s coverage table (lines 228-239) has exactly 11 rows. The three-item gap (`FR-P1-02-6`, `FR-P1-05-12`, `NFR-AUD-01`) is named explicitly and each is absent from the tech-stack table — checked row-by-row.
- **Superseded figures preserved, not overwritten** — confirmed at both sites (line 242 `superseded figure preserved: **10**`; line 120 `superseded: "two fewer than ten"`), per this project's `never-edit-signed-record`/append-only convention.
- **Full-file numeral/word sweep** (`grep -noE '(10|ten)'` bounded to non-identifier characters, both artifacts). Every hit resolves to one of: a `§10`/`§10.1` TE section citation, an ID substring (`TA-10`, `NFR-LIC-01`... not matched but adjacent), the new row's own `TA-10` citation, the intentionally-quoted superseded notes, or the printed **10**/**11** correction pair itself. No live, uncorrected assertion of a "10 coverage rows" or "ten" row-count claim survives outside a quoted superseded note in either file. Banners, § Scope note, table cells, headings and `## Assumptions` were all in the swept range.
- **`TA-10` is the right acceptance row.** `requirements.md` line 488 states directly: `NFR-AUD-01 | Auditability and versioning | Stable IDs connect inputs to claims; registry is append-safe; failed runs stay visible | TA-10, TA-21`, and line 408 (FR-P1-05-13, the registry schema requirement) also cites `[NFR-AUD-01] [TE §13.4] | TA-10`. `TA-10` is confirmed as NFR-AUD-01's governing acceptance row, not an invented one. The owner attribution ("not this unit — the registry's owner") is not overclaimed: it is unchanged from, and consistent with, SEC-G-02's own pre-existing Status paragraph ("The registry half is `foundation`'s (W-6 step 8); this unit owns the `AccessRecord` half").

### New finding

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 3 | Minor | `security-requirements.md` § Requirement coverage, `NFR-AUD-01` row (line 239) | `requirements.md` line 488 lists **two** acceptance rows for `NFR-AUD-01` — `TA-10, TA-21` — but the new coverage row cites only `TA-10`. `TA-21` is dropped without comment. | Either cite `TA-10, TA-21` to match `requirements.md`, or state explicitly why only `TA-10` is relevant to this unit's SEC-G-02 substance (e.g. if `TA-21` covers a facet — such as `code_commit`/`environment_lock_hash` population — outside `AccessRecord`/orphan-detection scope). Not blocking: the ID itself, the section mapping, and the owner attribution are all correct. |

### No regression

- `FR-P1-02-6` → `SEC-G-03, SEC-G-04` mapping (line 230) unchanged from the resolved prior finding.
- Exempt-module count (line 22, 116-126, 264): **five members in addition to the chokepoint, six counting it**, member 5 = `scripts/merge_coverage_year.py`, unchanged.
- SEC-G-01 breach stated at both named sites (lines 13-14, 64-77), unsoftened.
- SEC-G-04's AST-with-constant-folding mechanism and dynamic-path residual both stated in the Requirement/rule body (lines 149-156), not relegated to `## Assumptions`.
- Nothing newly claimed discharged: the banner (lines 5-16) still states G-09 signed (D-31) with preconditions **UNMET**, stage 3.1 **FAIL**, `src/data/locked_test.py`/`open_restricted` do not exist, WS-18/TA-18 undischarged; every coverage row in both tables remains `Pending`; the new `NFR-AUD-01` row is `Pending`, never presented as run or as evidence.

### Coverage limits (4-call budget)

Verified by direct read and grep: both coverage tables' row counts (11 and 8), the numeral/word sweep across both files, `requirements.md`'s TA-10/TA-21 rows for NFR-AUD-01 (lines 408, 488). Not independently re-verified within budget: `TA-21`'s own §19 checklist text; whether `functional-design`'s upstream artifacts (out of this stage's read scope) have themselves been swept for the same "10 requirements" figure this correction responds to — that sweep, if owed, belongs to `functional-design`, not to this repair.

### Summary

All four repair sites are present, consistent with each other, and consistent with `requirements.md`. The arithmetic checks out, superseded figures are preserved per convention, and the full-file numeral sweep found no fifth stale "10"/"ten" site. One new Minor: the coverage row cites `TA-10` but drops `TA-21`, which `requirements.md` also assigns to `NFR-AUD-01`. Zero Critical, zero Major, one Minor — READY.

READY
