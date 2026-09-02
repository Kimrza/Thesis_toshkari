# Security Requirements — `acquisition`

**Unit** `acquisition` (Bolt 3) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NOTHING HERE IS CLAIMED SATISFIED
>
> **BLK-07 is open.** W-2's restricted-access contract does not exist, so the FULL-manifest
> test stays **deferred against `RES-04`**. **Every acceptance row this unit touches is
> undischarged** *(enumerated 2026-08-31 on adversarial finding 2, Minor: the box previously
> named only TA-15, TA-22 and TA-32, leaving the rest recoverable only by reading every
> coverage-table row)* — **TA-03, TA-04, TA-08, TA-10, TA-15, TA-16, TA-21, TA-22, TA-25,
> TA-31, TA-32**, and the **TE §18.3 zero-TBD preflight** *(**TA-19** added 2026-09-01 with
> NFR-DQ-01's coverage-row citation; superseded list preserved above)*. **G-09 is signed (D-31) with its
> own preconditions UNMET**; **stage 3.1 remains FAIL**. No Python interpreter exists in
> this environment, so every test is **written-but-unexecuted** or unwritten. The single
> exception, and it is an existence claim only: `tests/test_acquisition_window.py` exists on
> disk and is recorded as green — **not re-executed here**.
>
> **The twelve pre-TC-06 months' provenance is unverifiable in principle** — no provider
> byte stream exists anywhere in the workspace, and **2022-04, 2022-07 and 2022-12** hold no
> `raw_isprint_cache/` at all (governance finding **DATA-07**). Nothing below discharges
> that caveat.
>
> **FR-P1-01-5 and FR-P1-01-7 carry no acceptance row.** No scientific value is decided
> here, and TE §18.2's absolute rule stands.

## Sources

- `../functional-design/business-rules.md` — **R-30** (retrieval applies no scientific transformation), **R-31** (membership derives from record timestamps, never from a name), **R-32** (every restricted-root access routed through a named accessor), **R-33** (a restricted **write** logs before it writes, and has its own contract), **R-34** (a version-suffix mismatch is recorded at retrieval and refused at release), **R-35** (an absent `madrigalWeb_version` fails exactly as `"unknown"` fails), **R-36** (hashing covers provider files; pre-TC-06 months say what they are), **R-37** (gaps are NaN at acquisition, and the count is conserved), **R-38** (notebook/script behavioural equivalence within a declared scope), **R-39** (credentials cannot leave through this unit's outputs), **R-40** (driver acquisition at one recorded grade), **R-41** (the F10.7 window is measured before anything is reconstructed), **R-42** (a derived release's provenance is current, or re-pointed by a D-number), **R-43** (ICTP is rejected, recorded immutably, and unreachable from the target path).
- `../functional-design/business-logic-model.md` — **W-1** … **W-11**, in particular **W-2**/**W-2a** (BLK-07's mechanism; writing under the restricted root), **W-3** (provenance per retrieved file), **W-4** (hashing; what the twelve pre-TC-06 months mean), **W-5** (identity-field agreement at release), **W-9** (keeping credentials out of this unit's outputs), **W-10** (closing the ICTP rejected-source audit), § Requirement-to-workflow map.
- `../../governance-guards/functional-design/business-rules.md` — **R-28** (one path into the restricted root; the enumerated exemption) and **R-25** (durable append before the read), which R-32/R-33 are the acquisition-side counterparts of.
- `../../../inception/requirements-analysis/requirements.md` — **REQ-ENG-13**, **FR-P1-00-1**, **FR-P1-00-2**, **FR-P1-01-1** … **FR-P1-01-7**, **NFR-SEC-01**, **NFR-AUD-01**, **NFR-DQ-01**.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§10** (credentials and secrets), **§8.1** (`requests` permitted *"where provider terms permit"*), **§9.1** (exactly two platforms), **§13.1**, **§13.3**, **§13.4**, **§18.2–18.3**, **§19**.
- `nfr-requirements-questions.md` — Q1 = A, Q2 = A, and the receipted Consolidated Summary Confirmation.

---

## Scope note

`produces_kinds` excludes `performance-requirements`, `scalability-requirements` and
`reliability-requirements` for a `library` unit. Assessed anyway:

| Category | Assessment for `acquisition` | Where it lives |
|---|---|---|
| **Performance** | No latency target. The one real quantity is **retrieval throughput against provider terms**, which is a **politeness and permission** constraint rather than a speed goal — TE §8.1 permits `requests` only *"where provider terms permit"*. | § SEC-A-01 |
| **Scalability** | Bounded and known: twelve months, three cells, one user, two platforms. No growth projection. | — |
| **Reliability** | This unit's reliability **is** its integrity: a retrieval that half-succeeds produces a file whose hash verifies against its own truncation. Stated as a security requirement because the failure is silent. | § SEC-A-01 |
| **Security** | This artifact. | — |
| **Observability** | Per-file provenance (W-3), the run record, and the access log for any restricted read or write (R-32, R-33). | § SEC-A-03, § SEC-A-05 |

---

## SEC-A-01 — Retrieval is resumable and hash-verified, and a partial file is never promoted

**This is a new requirement.** A grep of this unit's `business-rules.md` and
`business-logic-model.md` for rate limiting, backoff, retry, resumption or throttling
returns **no rule and no workflow step** on the subject. *(Precise form, corrected
2026-08-31 on adversarial finding 1, Minor: the raw grep is not empty — it hits
`business-logic-model.md:715`, "rebased 2026-08-28 on the **resume** pass", which is a
governance-remediation resume and not a retrieval-resumption rule. The substantive claim
stands; the "returns nothing" framing overstated its own reproducibility.)* The gap is
stated rather than assumed filled.

**Requirement (Q1 = A).**

1. **Bounded retry with backoff** on transient transport failure. Bounded, so a failing
   provider cannot turn into an unbounded loop inside a Kaggle session.
2. **Resumption** rather than restart where the provider supports it, so a twelve-month
   acquisition is not discarded by one transient error.
3. **A partial file is never promoted.** An interrupted retrieval leaves its target
   **absent**, or present and **explicitly marked incomplete** in the manifest — never a
   short file that looks whole.
4. **The hash is computed over the completed file**, after the completeness check, never
   over whatever bytes arrived.

**The failure this closes, stated plainly.** A truncated file hashed at truncation
produces a manifest that **verifies against itself forever**. Every later integrity check
passes; the data is simply missing, silently, in a way no hash check can ever surface. This
is the one acquisition failure that survives the project's entire verification chain.

**Requirement — provider terms bound the rate.** Retrieval respects the provider's stated
terms and any rate limit they impose. TE §8.1's permission for `requests` is conditional
on exactly that.

**Owed at stage 3.5, not invented here.** The concrete retry count, backoff schedule and
timeout are **operational values, not scientific constants** — choosing them is not a TE
§18.2 freeze-gate act — but they are not chosen in this artifact either. They are named as
owed, with the constraint that they be **recorded in the run record** so a retrieval's
behaviour is reconstructible.

## SEC-A-02 — A re-run is byte-identical, or explicitly divergent

**Requirement (Q2 = A).** A re-run of the same retrieval recomputes the SHA-256. On any
difference it **records the divergence — both provider filenames including version
suffixes, and both hashes — and refuses to overwrite.** It never silently replaces the
earlier bytes.

**Why, and it is not hypothetical.** Provider version drift is **observed in this
dataset**: `g.002` versus `g.003`. `team.md` states that a disagreement between original
and re-acquired bytes is **uninterpretable unless the original suffixes were recorded** —
and for **2022-04, 2022-07 and 2022-12** they were not. Latest-wins would destroy exactly
the comparison that makes drift interpretable, and would be a silent mutation of a governed
input, the class NFR-AUD-01 forbids for registry rows.

**This extends R-34 rather than replacing it.** R-34 already records a version-suffix
mismatch at retrieval and refuses it at release; this requirement states the same contract
for the re-run case, which R-34 does not address.

**Accepted cost.** A legitimate provider re-issue also stops the run. Someone must
adjudicate each divergence rather than the pipeline absorbing it — which is the point.

**Requirement — re-acquisition records the full identity of every file.** Full provider
filename **including version suffix**, retrieval date, and SHA-256. Re-acquisition produces
new bytes; **it cannot retroactively prove the original ones**, and nothing in it discharges
the DATA-07 caveat for the three months that never had a `raw_isprint_cache/`.

## SEC-A-03 — Credentials cannot leave through this unit's outputs

**Requirement (R-39, W-9, Q8 = D).** Credentials reach the provider client **directly from
the environment via `foundation`'s resolution** — never through a config file, log, registry
note or notebook (TE §10, NFR-SEC-01). **The live risk in this unit is egress**, because it
writes manifests, logs a run record, and runs inside a notebook whose outputs are saved.

**Two named carriers, because they are the realistic ones**: a **signed request URL** and an
**auth header**. An acquisition client naturally holds both, and both are what a manifest or
a log would carry without anyone deciding to put them there.

**Two limbs.**

1. **One declared redaction serializer.** Every value this unit writes to a manifest, log or
   notebook output passes through it, and it **refuses unredacted credential-shaped values**,
   raising `CredentialEgressError` — integrity tier, so the run terminates and an `aborted`
   row is written through the `IntegrityError` catch. One checkable chokepoint, testable
   directly: feed it a token-shaped value and assert refusal. **The definition of
   "credential-shaped" is heuristic, and that is accepted rather than hidden.**
2. **Notebook outputs cleared as a precondition of commit.** This is the one egress a
   serializer inside the process cannot reach: saved output cells are committed artifacts,
   and they are exactly where TE §10's "never in a notebook" is breached in practice.
   `notebooks/madrigal_phase1_coverage_audit.ipynb` exists in the workspace today, and
   `team.md` already commits this project to a pre-commit hook once git exists.

**Why not rely on TA-22's scan alone.** It covers tree, history, configs, logs and
artifacts — but it is **detection after the artifact exists**, and it is `foundation`'s. This
unit would be relying on a sibling's gate to catch its own leak.

**Not decided here.** The NFR-SEC-01 / Madrigal-identity conflict — `USER_EMAIL` in the
coverage notebook and `user_fullname` / `user_affiliation` in thirteen committed manifests —
is the **supervisor's**, recorded at `foundation` § SEC-F-02 and `requirements.md` § Known
defects row 13. **No reading is adopted.**

## SEC-A-04 — Every restricted access is routed and logged, in both directions

**Requirement (R-32).** Every read beneath the restricted root goes through a **named
accessor**; this unit constructs no ad-hoc path into it.

**Requirement (R-33).** A restricted **write** has its own contract and **logs before it
writes** — the write-side counterpart of `governance-guards` R-25's durable-append-before-read
ordering. A write that logged afterwards would leave a mutation with no record if it failed
between the two.

**Status: blocked upstream.** **BLK-07 is open** and W-2's contract does not exist, so
neither accessor exists. The consequence is recorded rather than worked around: the
FULL-manifest test — against
`evidence/locked_test_restricted/audit_evidence_2022-FULL/request_manifest.json`, which has
**no `madrigalWeb_version` key** because `merge_coverage_year.py` copies eight identity
fields and drops that one — is **deferred against `RES-04`**. Building it now would need
authorization this stage cannot give, or would read the root unlogged, which is the breach
BLK-07 exists to prevent.

## SEC-A-05 — Provenance and integrity of what is retrieved

**Requirement (R-30).** Retrieval applies **no scientific transformation**. What is stored
is what the provider sent.

**Requirement (R-37, NFR-DQ-01).** Gaps are **explicit NaN at acquisition** — never
interpolated, smoothed or filled — and **the count is conserved**: a record that disappears
between input and output is a defect, not a cleanup.

**Requirement (R-31).** Fold and partition membership derives from **record timestamps**,
never from a directory name or a filename. The year-blind acquisition predicate already
filed locked-test-month records into `audit_evidence_2022-01/` once, which is why this is a
rule rather than a convention. Enforced by `tests/test_acquisition_window.py` — which
**exists and is green**, and is the only test in this unit's scope of which that is true.

**Requirement (R-36).** Hashing covers **provider files**, and pre-TC-06 months **say what
they are**: `provenance_class` distinguishes a month with a provider byte stream from a
`derived_only` month, so a release or freeze gate can **refuse** the latter.

**Requirement (R-40, R-41).** Driver acquisition follows the frozen contract at **one
recorded release grade** — never mixing real-time, provisional and final within a series —
and the **F10.7 outage window is measured before anything is reconstructed**. No value is
imputed for it until the measured gap is recorded and governed.

**Requirement (R-42, R-43).** A derived release's provenance is **current, or re-pointed by
a D-number** — never left pointing at superseded per-month hashes. ICTP is **rejected,
recorded immutably, and unreachable from the target path**; the rejected-source evidence is
retained rather than deleted.

**A dated observation, never a live invariant.** The `provenance_class` field reaches
**43** sites, `derived_only` **38**, `producing_interpreter` **17**; split, `acquisition`
**25 / 21 / 11** and `inventory-and-registry` **18 / 17 / 6**. The two facts that no edit can
change: the three fields reach exactly **2** units, and **`foundation` carries all three
zero times** — which is why `write_release` faces an unstated choice that **§18.3 forbids an
agent from making**, routed to G-P1A / stage 3.2.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Row primary owner | Status |
|---|---|---|---|---|
| REQ-ENG-13 | SEC-A-03 | TA-16 | `regimes-diagnostics-reporting` | `Pending` |
| FR-P1-00-1 | SEC-A-05 | TA-31 — **no Table 2 owner row** | — | `Pending` |
| FR-P1-00-2 | SEC-A-05 | TA-25 | `inventory-and-registry` | `Pending` |
| FR-P1-01-1 | SEC-A-01, SEC-A-05 | TA-32 | **`acquisition`** | `Pending` |
| FR-P1-01-2 | SEC-A-02, SEC-A-05 | TA-15 | `foundation` | `Pending` — **TA-15 NOT covered** |
| FR-P1-01-3 | SEC-A-02 | TA-03, TA-15 | `foundation` | `Pending` |
| FR-P1-01-4 | SEC-A-01, SEC-A-02 | TA-04, TA-15 | `foundation` | `Pending` |
| **FR-P1-01-5** | SEC-A-05 | ⚠ **NO ACCEPTANCE ROW** — but `tests/test_acquisition_window.py` exists and is **green** | — | untested by row |
| FR-P1-01-6 | SEC-A-05 | TA-08 | `features-and-splits` (`external-products` supporting) | `Pending` |
| **FR-P1-01-7** | SEC-A-05 | ⚠ **NO ACCEPTANCE ROW** | — | untested |
| NFR-SEC-01 | SEC-A-03 | TA-22 | `foundation` | **not claimed as satisfied** |
| NFR-AUD-01 | SEC-A-02, SEC-A-04 | TA-10, TA-21 | `foundation` | `Pending` |
| NFR-DQ-01 | SEC-A-05 | **TA-19** *(cited 2026-09-01 on the confirming pass's Major; superseded cell preserved: `—`. `requirements.md` assigns NFR-DQ-01 its own row — units, times, signs and fill values documented; unexplained negative VTEC rejected; missingness and support reported by cell and month; target uncertainty budget produced — and the blank cell asserted it had none.)* | **not this unit** — per `requirements.md` §19 | `Pending` |

**Derived and printed**: 5 requirement sections (SEC-A-01…SEC-A-05); **13** coverage rows;
**2** requirements with no acceptance row (FR-P1-01-5, FR-P1-01-7) — **re-derived 2026-09-01 by
counting blank acceptance-row cells in the table above, not carried from the map**. The figure is
unchanged at 2, but it was previously **right by coincidence**: the table then showed **three**
blank cells (FR-P1-01-5, FR-P1-01-7 and NFR-DQ-01) while this line named two, because the count
came from the `functional-design` map rather than from the table. **Citing TA-19 on the NFR-DQ-01
row is what makes 2 true.** The clause *"matching the `functional-design` map"* is withdrawn:
matching the map is how three of this stage's coverage defects were introduced, and the map does
not carry NFR-DQ-01 at all. **0** rows claimed satisfied.

## Assumptions & Open Questions

- **[Q1]** Retrieval resilience is a **new requirement** this stage adds; the unit's `functional-design` states none. The concrete retry count, backoff schedule and timeout are **owed at stage 3.5** and are not chosen here.
- **[assumption]** The provider supports ranged or resumable requests. If it does not, limb 2 of SEC-A-01 degrades to restart-with-verification and **only limbs 1, 3 and 4 bind** — the partial-file prohibition is the load-bearing one and does not depend on resumability.
- **[Q2]** A re-run is byte-identical or explicitly divergent. **Re-acquisition cannot retroactively prove the original bytes**, and nothing here discharges DATA-07 for the three months that never had a `raw_isprint_cache/`.
- **[assumption]** "Credential-shaped" stays heuristic. A novel token format the serializer does not recognise passes it. Limb 2 (notebook outputs cleared) and TA-22's scan are the compensating controls, and **neither is a guarantee**.
- **Carried, not decided here — BLK-07 is open**, so R-32's and R-33's accessors do not exist and the FULL-manifest test stays deferred against `RES-04`.
- **Carried — `foundation` carries `provenance_class` zero times**, leaving `write_release` an unstated choice routed to G-P1A / stage 3.2. **§18.3 forbids an agent choosing**; `code-generation` must stop and report.
- **Carried, and the supervisor's** — the NFR-SEC-01 / Madrigal-identity conflict. **No reading adopted.**
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-31T00:00:00Z (system-reported current date; UTC clock command unavailable in this session)
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Minor | `security-requirements.md` SEC-A-01, "This is a new requirement" claim | A raw case-insensitive grep of `functional-design/business-logic-model.md` for `retry\|backoff\|resum\|throttl\|rate.?limit` DOES return one hit on line 715: "...rebased 2026-08-28 on the **resume** pass...", referring to a governance-remediation resume pass, not a retrieval-resumption workflow step. The artifact's claim ("returns no rule and no workflow step") survives on substance — that hit is neither a rule nor a workflow step — but the literal "returns no rule" framing overstates what a raw grep shows, and a future reader who reruns the same grep without the artifact's context could be confused into thinking the check failed. No hit for `retry`, `backoff`, `throttl`, or `rate.?limit` anywhere in either file (`business-rules.md` had zero hits of any kind). | Reword to "no *rule or workflow step addressing* retry/backoff/resumption/throttling" or note the one incidental "resume pass" hit and why it doesn't count, so the claim is grep-reproducible without needing tribal context. |
| 2 | Minor | `security-requirements.md` header box and TS-A-03 | The header box names only TA-15, TA-22, TA-32 as undischarged and BLK-07 as open; the fuller set the dispatch brief expects (TA-03, TA-04, TA-08, TA-10, TA-16, TA-21, TA-25, TA-31, §18.3 preflight) is not restated in the warning box, only scattered across the coverage table as `Pending`/"not claimed as satisfied". Every row checked *is* consistent with "undischarged" — no row claims satisfaction — so this is a presentation gap, not a factual error. | Consider listing the full undischarged TA set in the warning box (or a pointer to the coverage table) so a reader does not have to reconstruct completeness from row-by-row status. |

### Verified and NOT broken (adversarial checks that failed to find a defect)

- **Q1/Q2 retry-value discipline**: no concrete retry count, backoff schedule, or timeout literal appears anywhere in either artifact; both consistently defer the values to stage 3.5 and classify them as operational, not scientific, while explicitly hedging that TC-03e still applies if one later proves to be a scientific constant (`tech-stack-decisions.md` TS-A-03). This hedge is a reasonable, non-evasive treatment of the challenge posed in the dispatch brief.
- **No satisfaction/discharge claims**: scanned every coverage-table row and the Assumptions section in both files — every row reads `Pending`, "not claimed", "NOT covered", or carries an explicit "no acceptance row" flag. No row asserts a gate, test, or acceptance item as discharged. BLK-07 is stated open; G-09/D-31 preconditions are stated unmet; stage 3.1 is stated FAIL. `tests/test_acquisition_window.py` was confirmed to exist on disk at `tests/test_acquisition_window.py` (existence only, per instructions — not executed); this is the one exception the brief flagged and the artifact's "exists and is green" framing is consistent with that carve-out.
- **DATA-07 caveat**: both artifacts state the twelve-month provenance is "unverifiable in principle," name 2022-04, 2022-07, and 2022-12 as missing `raw_isprint_cache/`, and state re-acquisition "cannot retroactively prove the original bytes" — matching `team.md`'s caveat with no softening found.
- **Conditional dependencies held conditional**: `madrigalWeb` is stated "not adopted here," "conditional and unapproved" pending D-144; the HDF5/netCDF reader is stated "not chosen here," pending the schema audit. Neither is treated as adopted anywhere in either file.
- **`provenance_class` figures**: 43/38/17 with acquisition 25/21/11 and inventory-and-registry 18/17/6 are presented under an explicit "dated observation, never a live invariant" framing, with the two stable facts (fields reach exactly 2 units; `foundation` carries all three zero times) called out as the load-bearing, edit-proof claims. Matches the brief.
- **Counts, re-derived**: `security-requirements.md` — 5 sections (SEC-A-01…05, counted from headers), 13 coverage-table rows (counted), 2 no-acceptance-row requirements (FR-P1-01-5, FR-P1-01-7, counted). `tech-stack-decisions.md` — 5 sections (TS-A-01…05), 7 coverage-table rows, 2 conditional components (`madrigalWeb`, HDF5/netCDF reader). All four printed derivations match a fresh count of the tables as they stand on disk.
- **Scope**: both artifacts stay within the `library`-unit `produces_kinds` (security-requirements.md, tech-stack-decisions.md); `tech-stack-decisions.md` explicitly declines to select or claim installation of anything, deferring to `foundation`'s transcribed stack.

### Coverage limits (within the 8-tool-call budget)

- Did not independently verify FR-P1-01-5/FR-P1-01-7 "no acceptance row" against the full `functional-design` requirement-to-workflow map beyond the excerpt read (lines 710–719 of `business-logic-model.md`); the excerpt is consistent with the claim but the map itself was not exhaustively cross-checked.
- Did not verify `tests/test_acquisition_window.py` is actually green (explicitly out of scope per the dispatch brief).
- Did not open sibling-unit files beyond what the dispatch brief's carve-out permits; no sibling-unit claim in either artifact required a spot-check beyond what was already checked.

### Summary

Both artifacts are self-consistent, honest about what is undischarged, and hold every conditional dependency and caveat as stated in the human answers and team practice. The one substantive challenge attempted — trying to catch an invented retry/backoff/timeout literal or a softened DATA-07 caveat — found nothing. The two findings are both Minor (a slightly overstated grep claim that survives on substance, and a warning-box completeness gap that the coverage table itself resolves), well under the NOT-READY threshold.

READY

## Review — 2026-09-01 confirming pass

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T05:17:46Z
**Iteration:** 2 (fresh budget after human gate rejection; artifacts unchanged since the 2026-08-31 READY above)

### Prior findings — status

- Finding 1 (Minor, "new requirement" grep overstatement): unchanged, unresolved, still Minor — not re-raised as new.
- Finding 2 (Minor, warning-box completeness): unchanged, unresolved, still Minor — not re-raised as new.

### New finding

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 3 | Major | § Requirement coverage table, `NFR-DQ-01` row, and the "Derived and printed" line immediately below it | `../../../inception/requirements-analysis/requirements.md` line 487 assigns `NFR-DQ-01` its own acceptance row, **TA-19** (*"Units, times, signs and fill values documented; unexplained negative VTEC rejected; missingness and support reported by cell and month; target uncertainty budget produced"*) — substance this unit's own SEC-A-05 rests on directly (R-37: gaps as explicit NaN, count conserved). This table cites no acceptance row for `NFR-DQ-01` (`—` in both the Acceptance Row and Row Primary Owner columns) and `TA-19` appears nowhere in either artifact (confirmed by grep across both files). This is exactly the dispatch brief's named failure mode — "missing an NFR ID whose substance the artifacts rested on while citing its TE section directly" — and the brief flagged `NFR-DQ-01` by name as a likely miss. It also breaks the table's own arithmetic: the "Derived and printed" line states "**2** requirements with no acceptance row (FR-P1-01-5, FR-P1-01-7)," but the table as printed shows **three** rows with a blank acceptance-row cell — FR-P1-01-5, FR-P1-01-7, **and NFR-DQ-01** — so the printed count is derived from an incomplete scan of the artifact's own table, not from the table itself. | Add TA-19 as `NFR-DQ-01`'s acceptance row (owner per `requirements.md` §19, not decided here) and correct the derived-and-printed line to 3 requirements with no acceptance row **before** TA-19 is added, or to 2 with TA-19 cited, whichever the table ends up stating. Re-run the set-difference against `requirements.md`'s full ID space rather than against the artifacts' own prior table. |

### Verified again, no new defect found

- `NFR-AUD-01` and `NFR-SEC-01` (the other two NFR IDs the brief flagged as likely misses along with `NFR-DQ-01`): both carry correct acceptance-row citations (TA-10/TA-21 and TA-22 respectively), matching `requirements.md` lines 488–489 exactly. Only `NFR-DQ-01` is affected.
- Q1 ("Resumable, hash-verified") and Q2 ("Byte-identical or explicit divergence") are carried faithfully into SEC-A-01/SEC-A-02 with the resumption boundary (limb 2, degrading to restart-with-verification if the provider lacks ranged requests) and the divergence mechanism (recompute SHA-256, record both provider filenames with version suffixes and both hashes, refuse to overwrite) both stated where the guarantee is claimed, not only under Assumptions.
- The retrieval-resilience requirement (SEC-A-01) is stated as genuinely new work: the artifact's own grep-based derivation stands (finding 1 above already covers its one imprecision), no retry/backoff/timeout literal is invented, and nothing claims the requirement exists in code — it is explicitly "owed at stage 3.5."
- The DATA-07 caveat (unverifiable-in-principle provenance; 2022-04, 2022-07, 2022-12 with no `raw_isprint_cache/`; version-suffix drift `g.002`/`g.003`) is stated at the point each guarantee is claimed (header box, SEC-A-01, SEC-A-02, § Assumptions), not confined to Assumptions alone.
- No mechanism is overstated elsewhere: every coverage-table row and the Assumptions section still reads `Pending`/"not claimed"/"NOT covered"; BLK-07 open, G-09/D-31 preconditions unmet, stage 3.1 FAIL, and `tests/test_acquisition_window.py`'s green status is stated as an existence claim only — none of this changed since the prior pass.

### Summary

Artifacts are otherwise unchanged and were correctly found READY on 2026-08-31. This confirming pass, re-run against the full NFR ID space named in the dispatch brief rather than against the artifact's own table, finds one Major defect the prior pass missed: `NFR-DQ-01`'s acceptance row (TA-19) is uncited, and the table's own derived count of requirements lacking an acceptance row is wrong by one as a direct consequence. This is exactly the failure pattern the human's gate rejection was called to catch. Combined with the two standing Minor findings, this is 1 Major + 2 Minor — under the >2-Major NOT-READY threshold by count, but I am recording NOT-READY on judgment: this is the specific completeness check the rejection targeted, the unit's own summary line is factually wrong on its face, and the fix (one table cell, one line) is small enough that gating on it costs little against the cost of letting a ninth unit through with this exact defect.

NOT-READY

## Review — 2026-09-01 repair verification

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T05:21:02Z
**Iteration:** 3 (repair verification of the 2026-09-01 confirming-pass Major, finding #3 above)

### Repair verified at all three named sites

1. **Coverage table, `NFR-DQ-01` row (line 224).** Now reads `**TA-19** (cited 2026-09-01 …; superseded cell preserved: —)`, with the row's substance quoted (units/times/signs/fill-value documentation, negative-VTEC rejection, missingness/support reporting, target-uncertainty budget) and owner cell `**not this unit** — per requirements.md §19`. Checked against `requirements.md` line 487: `NFR-DQ-01 | Data quality and target uncertainty | … | TA-19` — the citation is genuine, TA-19 is verbatim `NFR-DQ-01`'s own row (not borrowed from an adjacent ID), and the owner cell makes no owner claim beyond deferring to §19 — not overclaimed.
2. **"Derived and printed" line (lines 226–234).** Recounted the coverage table directly rather than trusting the artifact's prose: 13 rows total (REQ-ENG-13, FR-P1-00-1/00-2, FR-P1-01-1…01-7, NFR-SEC-01, NFR-AUD-01, NFR-DQ-01) — matches the printed "13". Blank acceptance-row cells after the repair: FR-P1-01-5 and FR-P1-01-7 only (`NFR-DQ-01`'s cell is no longer blank) — count is **2**, matching the printed "2" exactly, and the line's own derivation method (count blank cells in the table, not the map) is now what the printed figure actually reflects. The "matching the map" clause is withdrawn as stated, with the correct reason given (the map doesn't carry `NFR-DQ-01` at all).
3. **Header warning box (lines 9–13).** The undischarged TA-row enumeration now reads `TA-03, TA-04, TA-08, TA-10, TA-15, TA-16, TA-21, TA-22, TA-25, TA-31, TA-32`, plus `TA-19` called out separately with its addition date and reason. `TA-19` is present in the enumerated set.

All three sites are mutually consistent: the table cites TA-19, the derived count reflects that citation, and the header box lists TA-19 among the undischarged rows.

### No fourth stale site found

Swept the full artifact (both numerals and spelled-out forms, all surfaces — table cells, header box, correction parentheticals, findings table, Assumptions) for a surviving claim that `NFR-DQ-01` has no acceptance row, that the no-row count is 3, or that the count still matches the map. None found. The one place "three" appears in connection with this fact (line 230, inside the correction parenthetical explaining what the table *previously* showed) is a deliberately preserved superseded-state quotation, not a live claim, and is correctly labeled as such — this is the pattern the dispatch brief told me to ignore. The findings-table row (#3, line 299) is left standing verbatim per this project's preserve-don't-overwrite convention for review records; it is historical, not a live claim, and does not conflict with the repair.

### `tech-stack-decisions.md` arithmetic — untouched, re-verified rather than assumed

`Derived and printed`: "7 coverage rows — six fewer than `security-requirements.md`'s thirteen, because FR-P1-00-1, FR-P1-00-2, FR-P1-01-5, FR-P1-01-7, NFR-AUD-01 and NFR-DQ-01 raise no technology choice." Verified: the six named IDs are exactly the six requirements this pass confirms are technology-choice-silent (nothing about the TA-19 repair changes whether `NFR-DQ-01` raises a technology choice — it still doesn't, it now has an acceptance-row owner elsewhere). 13 − 6 = 7 holds against the tables as printed. The repair changed a coverage-table cell and a derived count in `security-requirements.md`, not either artifact's row count, so this arithmetic was correctly left untouched.

### Full ID-space set-difference, re-run

`requirements.md`'s eleven NFR IDs: `NFR-AUD-01, NFR-DET-01, NFR-DQ-01, NFR-FAIR-01, NFR-IRI-01, NFR-LEAK-01, NFR-LIC-01, NFR-PHASE-01, NFR-REP-01, NFR-SEC-01, NFR-TDEF-01`. Only three appear in this unit's coverage table: `NFR-SEC-01`, `NFR-AUD-01`, `NFR-DQ-01` — the other eight are out of this unit's SEC-A-section scope and are not cited here at all, which is not truncation (nothing here purports to cover them). For the three that are cited, checked each citation against its full `requirements.md` Test-column list for the truncated-citation defect named in the brief (TA-10 cited, TA-21 dropped, found on another unit):
- `NFR-AUD-01`: table cites `TA-10, TA-21` — `requirements.md` lists `TA-10, TA-21`. Complete.
- `NFR-SEC-01`: table cites `TA-22` — `requirements.md` lists `TA-22`. Complete.
- `NFR-DQ-01`: table cites `TA-19` — `requirements.md` lists `TA-19`. Complete.
No truncation found on any of the three cited rows.

### Standing Minors — verified resolved on disk

- **Finding 1** ("returns no rule" grep overstatement): resolved. A 2026-08-31 correction is present in place (lines 58–60 area) naming the `business-logic-model.md:715` "resume pass" hit verbatim and explaining why it is a governance-remediation resume rather than a retrieval-resumption rule, and reframing the claim's precise scope. The finding row stays in the table per this project's preserve-don't-overwrite convention; that is a record of history, not a live defect.
- **Finding 2** (header box naming only TA-15/TA-22/TA-32): resolved. The header box's enumeration is now the full eleven-item TA set plus TA-19, with a note dated 2026-08-31 explaining what was added and why. The finding row likewise stays in the table as history.
Both are correctly stated as resolved rather than standing; neither is re-raised.

### No regression

Re-checked, unchanged and correct: Q1/Q2 fidelity into SEC-A-01/SEC-A-02, the "genuinely new requirement" framing (owed at stage 3.5, no retry/backoff literal invented), the DATA-07 caveat stated at every point a guarantee is claimed (not confined to Assumptions), and no coverage-table row, Assumptions bullet, or header-box line claims a gate, test, or acceptance item as discharged. `G-09` remains stated signed (D-31) with preconditions **UNMET**; stage 3.1 remains stated **FAIL**; `BLK-07` remains stated open; no claim that `configs/` exists or that a Python interpreter is present in this environment. Nothing in this repair pass discharges any TA row — TA-19 included, which is added as *cited*, not as satisfied.

### Summary

All three repair sites are present, correct, and mutually consistent; the printed "2" now matches a direct recount of the table; TA-19 is genuinely `NFR-DQ-01`'s row per `requirements.md` and its owner is not overclaimed; no fourth stale site survives; `tech-stack-decisions.md`'s dependent arithmetic (13 − 6 = 7) still holds and was correctly left untouched; the full NFR ID-space set-difference finds no truncated citation this time; and both standing Minors are genuinely resolved on disk, not merely reasserted. The Major that blocked the prior pass is fully repaired.

READY
