# Security Design — `acquisition`

**Unit** `acquisition` (Bolt 3) · **Kind** `library` · **Stage** `nfr-design`

> ## ⚠ WRITTEN AGAINST THE WORKSPACE ON 2026-09-01 — NOTHING HERE IS BUILT
>
> Per the owner's 2026-09-01 ruling, this design is written against **current workspace
> state** while **`nfr-requirements` stays unchanged** — so the upstream artifact carries
> status claims this document contradicts **by instruction, not by oversight**. The
> divergences are in § SD-A-00.
>
> **Every mechanism designed below is unbuilt.** The **redaction serializer** does not
> exist (no `CredentialEgressError`, no redaction helper of any name, anywhere in `src/`,
> `scripts/` or `tests/`). **`write_restricted` does not exist.** The **pre-commit hook**
> does not exist. **`configs/`, `pyproject.toml` and `requirements.txt` are absent**, so
> **TC-06's scaffold precondition is unmet**.
>
> **The suite runs off-pin.** 277 passed / 2 skipped under **Python 3.14.7 / pytest
> 9.1.1**, against a governed pin of **Python 3.11 exactly** (TE §8.1, TC-03d), with no
> `requirements.txt` to pin pytest. **Not governed evidence.**
>
> **DATA-07 stands unchanged.** The twelve pre-TC-06 months' provenance is **unverifiable
> in principle** — no provider byte stream exists anywhere in the workspace, and
> **2022-04, 2022-07 and 2022-12** hold **no `raw_isprint_cache/` at all**. Nothing below
> discharges that caveat.
>
> **G-09 is signed (D-31) with preconditions UNMET**; **stage 3.1 remains FAIL**.
> **No scientific value is decided here.** TE §18.2's absolute rule stands.

## Sources

- `nfr-requirements/security-requirements.md` — **SEC-A-01** (resumable, hash-verified retrieval), **SEC-A-02** (byte-identical or explicitly divergent re-run), **SEC-A-03** (credential egress: two limbs), **SEC-A-04** (restricted access routed and logged both directions), **SEC-A-05** (provenance and integrity). Consumed as the requirement set; its **status claims** are superseded by § SD-A-00.
- `nfr-requirements/tech-stack-decisions.md` — **TS-A-01** (the conditional retrieval client), **TS-A-02** (reader frozen after the schema audit), **TS-A-03** (resilience in the approved stack), **TS-A-04** (notebook/script equivalence), **TS-A-05** (platform posture).
- `functional-design/business-rules.md` — **R-30** … **R-43**, in particular **R-32** (every restricted read through a named accessor), **R-33** (a restricted write logs before it writes), **R-34** (version-suffix mismatch recorded at retrieval, refused at release), **R-36** (hashing covers provider files), **R-37** (gaps are NaN at acquisition), **R-39** (credentials cannot leave through this unit's outputs).
- `functional-design/business-logic-model.md` — **W-2**/**W-2a** (BLK-07's mechanism; writing under the restricted root), **W-3** (provenance per retrieved file), **W-4** (hashing), **W-9** (keeping credentials out of outputs).
- **The workspace, read 2026-09-01** — `src/data/locked_test.py`, `scripts/merge_coverage_year.py`, `evidence/locked_test_restricted/audit_evidence_2022-FULL/`, and the greps recorded in § SD-A-00. Primary evidence for every status claim here.
- `../../governance-guards/nfr-design/security-design.md` — **§ SD-G-01**, whose chokepoint this unit calls and whose module hosts the write contract at § SD-A-03.
- `../../foundation/nfr-design/security-design.md` — **§ SD-02**, the credential resolution this unit consumes.
- `../../../inception/requirements-analysis/requirements.md` — **REQ-ENG-13**, **FR-P1-00-1**, **FR-P1-00-2**, **FR-P1-01-1** … **FR-P1-01-7**, **FR-P1-01-10**, **NFR-SEC-01**, **NFR-AUD-01**, **NFR-DQ-01**.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§8.1** (`requests` *"where provider terms permit"*), **§9.1**, **§10** (credentials and secrets), **§13.1**, **§13.3**, **§13.4**, **§18.2–18.3**, **§19** (TA-19, TA-22).
- `nfr-design-questions.md` — Q1 = A, Q2 = A, Q3 = A, Q4 = A, and the receipted Consolidated Summary Confirmation.

---

## Scope note

`produces_kinds` excludes `performance-design`, `scalability-design` and
`reliability-design` for a `library` unit. Those categories were assessed at
`nfr-requirements` and are **not re-opened**: no latency target (the one real quantity is
**retrieval throughput against provider terms**, a permission constraint rather than a
speed goal); bounded and known scale (twelve months, three cells, one user, two
platforms); and reliability that **is** integrity here, because a retrieval that
half-succeeds produces a file whose hash verifies against its own truncation.

---

## SD-A-00 — Where this design contradicts its own upstream

| Upstream claim | Actual state on 2026-09-01 |
|---|---|
| SEC-A-04: *"BLK-07 is open… **neither accessor exists**"* | **Half stale.** The **read** side exists — `open_restricted` (`src/data/locked_test.py:147`) and `scripts/merge_coverage_year.py:98`'s `guarded()` helper routing through it. The **write** contract (R-33) does **not** exist. |
| SEC-A-04: the FULL-manifest test blocked on a missing artifact | `evidence/locked_test_restricted/audit_evidence_2022-FULL/request_manifest.json` **exists**, with `sha256_manifest.json`, three CSVs and `PROVENANCE_NOTICE.md`. |
| SEC-A-03 limb 1: *"one declared redaction serializer"* | **Entirely unbuilt** — zero hits for `CredentialEgressError` or any redaction helper across `src/`, `scripts/`, `tests/`. |

**The one that matters is the third.** The read accessor existing is good news; the
serializer's absence is the **live gap**, and § SD-A-02 states why no sibling can cover it.

## SD-A-01 — Retrieval integrity: the failure that survives every later check

**Design (SEC-A-01, Q1 = A at `nfr-requirements`).** **Bounded** retry with backoff on
transient transport failure — bounded, so a failing provider cannot become an unbounded
loop inside a Kaggle session. **Resumption** rather than restart where the provider
supports it. **A partial file is never promoted**: an interrupted retrieval leaves its
target **absent**, or present and **explicitly marked incomplete** in the manifest, never a
short file that looks whole. **The hash is computed over the completed file**, after the
completeness check — never over whatever bytes arrived.

**Why the ordering of those last two is the whole requirement.** A truncated file hashed
at truncation produces a manifest that **verifies against itself forever**. Every later
integrity check passes; the data is simply missing, silently, in a way **no hash check can
ever surface**. This is the one acquisition failure that survives the project's entire
verification chain, which is why the completeness check must precede the hash rather than
accompany it.

**Design (SEC-A-02).** A re-run recomputes the SHA-256 and, on any difference, **records
the divergence — both provider filenames including version suffixes, and both hashes — and
refuses to overwrite.** Provider version drift is **observed in this dataset** (`g.002`
versus `g.003`), so a mismatch is a fact to record, not an error to resolve by replacement.

**Provider terms bound the rate.** TE §8.1's permission for `requests` is conditional on
exactly that.

> **⚠ Owed at 3.5, and not chosen here.** The concrete **retry count, backoff schedule and
> timeout** are operational values, not scientific constants — so §18.2's freeze-gate rule
> does not reach them — but they are not picked in this artifact either. They are named as
> owed, with the constraint that each is **recorded in the run record**, so a retrieval's
> behaviour is reconstructible after the fact.

## SD-A-02 — Credential egress: fail closed on what is known, block on what is guessed

**Design (Q1 = A).** **One declared redaction serializer.** Every value this unit writes to
a manifest, log or notebook output passes through it.

| Class | Rule |
|---|---|
| **Signed request URL** | **Refused unconditionally** |
| **Auth header** | **Refused unconditionally** |
| Everything else | Broader entropy/prefix heuristic — **blocks the write**, and **names what it matched** |

**Why the asymmetry, rather than one uniform rule.** A signed URL and an auth header are
**structurally identifiable**; treating them as heuristic results understates what the
check actually knows, and it exposes the certain cases to the tuning pressure generated by
the uncertain ones. SEC-A-03 names these two as *"the realistic ones… what a manifest or a
log would carry without anyone deciding to put them there."* They get a rule. Everything
else genuinely is a guess — and a guess that **blocks** is still correct when the artifact
is committed and permanent.

**Refusal is integrity tier.** `CredentialEgressError` terminates the run, and an
`aborted` row is written through the `IntegrityError` catch. One checkable chokepoint,
testable directly: feed it a token-shaped value and assert refusal.

> ### ⚠ The cost, stated with the rule rather than discovered later
>
> **False positives on legitimate high-entropy values will occur** — a hash, a UUID, a
> content-addressed identifier. They need an **allowlist**, and that allowlist is a
> **review surface, never grown to silence a failure**. This is the same trap `foundation`
> § SD-01 records for the secret scanner, and it has the same answer, because it is the
> same failure mode: an exception list widened once per incident eventually misses the
> thing it was built to catch.

**Design (Q3 = A) — limb 2, the egress a serializer cannot reach.** A notebook carrying
**saved output cells fails the pre-commit hook**; the author clears and re-commits.

**Why refusing rather than auto-stripping.** A credential in committed history needs a
**history rewrite** to remove, and this repository **tags its freeze gates**, so that
rewrite would rewrite tagged commits. Auto-stripping is also the wrong shape for this
project specifically: `team.md` requires a commit changing a governed artifact to **cite a
D-number**, which presumes the author knows exactly what they are committing — and a tool
that silently rewrites staged content defeats that presumption. Where outputs genuinely
need preserving for review, that is an **exported artifact with its own provenance**, not a
committed cell.

**Why neither limb can be delegated to TA-22's scan.** That scan covers tree, history,
configs, logs and artifacts — but it is **detection after the artifact exists**, and it is
**`foundation`'s**. Relying on it would be this unit depending on a sibling's gate to catch
its own leak.

> **⚠ Nothing here exists.** No `CredentialEgressError`, no redaction helper, no hook.
> `notebooks/madrigal_phase1_coverage_audit.ipynb` is in the workspace **today**, and
> **NFR-SEC-01 is unclaimed**.

> **⚠ Not decided here, and no reading adopted.** The **NFR-SEC-01 / Madrigal-identity
> conflict** — `USER_EMAIL` in the coverage notebook, `user_fullname` / `user_affiliation`
> in **thirteen committed manifests** — is the **supervisor's**, recorded at `foundation`
> § SEC-F-02 and `requirements.md` § Known defects row 13.

## SD-A-03 — The restricted write logs first, and lives behind the one door

**Design (Q2 = A, R-33).** `write_restricted` **logs durably, then writes** — the write-side
counterpart to `governance-guards` R-25's durable-append-before-read. It is a **sibling
function in `src/data/locked_test.py`**, sharing **`_append_and_flush`** and the **same
boundary derivation from the module's own location**.

**Why a write that logged afterwards is not a smaller version of the same thing.** It would
leave a **mutation with no record** if it failed between the two operations. The read-side
ordering exists so an access cannot happen unrecorded; the write-side ordering exists so a
**change** cannot.

**Why it lives in `governance-guards`' module rather than this unit.** The decisive
argument is the **exempt list**. A separate write path here would make a **second module
name the restricted-root literal**, taking the list from **seven to eight**.
`governance-guards` DISC-1 records what each new holder costs: the seventh was admitted
only because a membership assertion **fired on first run**. D-15's boundary *"does not
weaken slightly; it ends."* One module, one door, one durability implementation for both
directions.

> **Ownership is stated rather than blurred.** The module is **`governance-guards`'**.
> **`acquisition` is its caller, not its co-owner** — adding a function there for this
> unit's concern transfers no ownership of the boundary, and any change to it is
> `governance-guards`' to review.

**Design (R-32).** Every read beneath the restricted root goes through the **named
accessor**; this unit constructs **no ad-hoc path** into it. That accessor now exists
(§ SD-A-00), and `scripts/merge_coverage_year.py` already routes through it via `guarded()`.

## SD-A-04 — Provenance is recorded at retrieval, and refused at release

**Design (SEC-A-05, R-34, R-36, W-3).** Every retrieved file records its **full provider
filename including version suffix**, its **retrieval date** and its **SHA-256**. A
**version-suffix mismatch is recorded at retrieval and refused at release** — recorded
early so the fact exists, refused late so it cannot enter a governed artifact silently.

**Design (R-37, NFR-DQ-01, TA-19).** Gaps are **explicit NaN at acquisition** — never
interpolated, smoothed or filled. Missingness and support are **reported by cell and
month**; unexplained negative VTEC is rejected.

**Design (R-31).** Fold and partition membership derives from **record timestamps** —
never from a directory or file name. A year-blind predicate once filed locked-month records
into `audit_evidence_2022-01/`, which is why this is asserted on record dates rather than on
the folder a file was filed under.

**Design — drivers carry a release grade, not only a lag (FR-P1-01-8, R-40, R-41).** No
driver is **backfilled from future final or definitive archived index values**, and the
**release status of every driver is recorded**, not only its lag. Each driver's manifest
carries a **release-status field**, and a reanalysed-value check passes.

**Why the lag alone is insufficient, stated because it is the subtle half.** A series can
**satisfy its stated lag while still being built from reanalysed indices** — invisible in
validation, fatal on discovery, because a final archived value is **not** the
contemporaneous operational value available at a 2022 forecast origin. Kyoto Dst release
grades (real-time, provisional, final) are **never mixed within one series**, and the grade
for calendar 2022 is recorded **before use**.

**Design — gaps are NaN, and that is an acquisition-time property (FR-P1-01-9, R-37,
D-5/D-10.2).** Data gaps are stored as **explicit `NaN` at acquisition time**; **no
interpolation, smoothing or fill occurs at acquisition**. The test is an **injected gap
surviving acquisition as `NaN`** — and `requirements.md` records this row as **`UNTESTED`**,
with no §16 or §19 acceptance row attached.

**Design — a derived multi-month release re-merges or is re-pointed (FR-P1-01-11, R-42).**
A derived release either **re-merges from the current months** or **carries a D-number
re-pointing its provenance**. `PROVENANCE_NOTICE.md` states this as prose today — *"Do not
rely on this artifact at a freeze gate while this notice stands"* — and the requirement
makes it a contract rather than a note. **`audit_evidence_2022-FULL/` is exactly such a
derived release**, and it carries that notice now.

> **⚠ DATA-07 governs everything above for the existing twelve months.** Their provenance
> is **unverifiable in principle**: no provider byte stream exists anywhere in the
> workspace, and **2022-04, 2022-07 and 2022-12** have **no `raw_isprint_cache/` at all**.
> Re-acquisition produces new bytes; **it cannot retroactively prove the original ones**.
> Every re-acquired file therefore records its full suffix, date and hash, and **any
> mismatch against a previously recorded suffix is surfaced rather than silently
> accepted** — an obligation on the deferred work, not an observation about the past.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| REQ-ENG-13 | SD-A-02 | TA-16 | `Pending` |
| FR-P1-00-1 | SD-A-01 | TA-04 | `Pending` |
| FR-P1-00-2 | SD-A-01 | TA-04 | `Pending` |
| FR-P1-01-1 | SD-A-01 | TA-25 | `Pending` |
| FR-P1-01-2 | SD-A-01, SD-A-04 | TA-25 | `Pending` |
| FR-P1-01-3 | SD-A-04 | TA-31 | `Pending` |
| FR-P1-01-4 | SD-A-04 | TA-31 | `Pending` |
| **FR-P1-01-5** | SD-A-04 | ⚠ **NO ACCEPTANCE ROW** | untested |
| FR-P1-01-6 | SD-A-03 | TA-08 | `Pending` |
| **FR-P1-01-7** | SD-A-04 | ⚠ **NO ACCEPTANCE ROW** | untested |
| **FR-P1-01-8** | SD-A-04 | TA-31 | `Pending` |
| **FR-P1-01-9** | SD-A-04 | ⚠ **NO ACCEPTANCE ROW** — `UNTESTED` in `requirements.md` | untested |
| **FR-P1-01-10** | SD-A-02 | TA-22 | `Pending` — **NOT MET** |
| **FR-P1-01-11** | SD-A-04 | TA-31 | `Pending` |
| **NFR-SEC-01** | SD-A-02 | TA-22 | `Pending` — **unclaimed** |
| **NFR-AUD-01** | SD-A-03 | **TA-10, TA-21** — both rows, owned elsewhere | `Pending` |
| **NFR-DQ-01** | SD-A-04 | **TA-19** | `Pending` |

**Derived and printed**: 5 design sections (SD-A-00…SD-A-04); **17** coverage rows *(count
re-derived 2026-09-01 on a pre-dispatch self-sweep; superseded figure preserved: **14**)* —
counted directly from the table above, **not** read off `nfr-requirements`' table or the
unit's `functional-design` map. **3** requirements with **no acceptance row**
(FR-P1-01-5, FR-P1-01-7, **FR-P1-01-9**) — counted by reading this table's cells
*(superseded: **2**)*. **0** rows claimed satisfied; **0** acceptance rows discharged.

**Three IDs were missing, and I found them rather than a reviewer.** A set-difference of
this table's `FR-P1-01-*` citations against `requirements.md`'s range returned
**`FR-P1-01-8`, `FR-P1-01-9` and `FR-P1-01-11`** as uncited. All three are this unit's
work and two were **already reproduced** in prose before the sweep — the NaN-at-acquisition
rule and the derived-release re-point contract, the latter through `R-42` in § Sources.
`FR-P1-01-8`'s driver release-grade obligation was genuinely absent and is now designed at
§ SD-A-04.

**This is the check that produced a Critical on `foundation` at this stage**, where
`NFR-DET-01`, `NFR-REP-01` and `REQ-ENG-10` were reproduced but uncited. The difference
here is only the order: **the set-difference ran before dispatch rather than after**.
Writing the check into a reviewer's brief is not the same act as performing it — that
lesson is recorded in this stage's diary and this is the first unit where it was applied.

## Assumptions & Open Questions

- **[Q1 / SD-A-02]** **The redaction serializer does not exist**, and its "credential-shaped" heuristic is **explicitly heuristic**. The two named carriers are rules; the rest is a guess that blocks.
- **[Q1 / SD-A-02]** **The false-positive allowlist is a review surface.** Nothing here says who reviews it — and an unreviewed allowlist disables the check one pattern at a time.
- **[Q2 / SD-A-03]** **`write_restricted` does not exist.** Placing it in `governance-guards`' module keeps the exempt list at **seven**; that unit **owns** the file and this unit **calls** it.
- **[Q3 / SD-A-02]** **The pre-commit hook does not exist**, and `notebooks/madrigal_phase1_coverage_audit.ipynb` is in the workspace today.
- **[SD-A-01]** **Retry count, backoff schedule and timeout are owed at 3.5** and are not chosen here; each must be **recorded in the run record**.
- **[SD-A-04 / DATA-07]** The twelve pre-TC-06 months are **unverifiable in principle**, three of them lacking `raw_isprint_cache/` entirely. **Re-acquisition cannot prove the original bytes.**
- **[carried]** The **NFR-SEC-01 / Madrigal-identity conflict is the supervisor's**; **no reading is adopted**.
- **[carried]** **`configs/`, `pyproject.toml`, `requirements.txt` absent** — TC-06's scaffold precondition unmet. The suite is **off-pin** and **not governed evidence**.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row, install or test as discharged.
