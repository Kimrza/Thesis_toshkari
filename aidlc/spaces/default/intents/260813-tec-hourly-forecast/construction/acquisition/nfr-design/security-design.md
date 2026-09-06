# Security Design — `acquisition`

**Unit** `acquisition` (Bolt 3) · **Kind** `library` · **Stage** `nfr-design`

> **Re-saved 2026-09-02, content unchanged.** A `STAGE_JUMPED` redo of `nfr-design` — ordered
> by the project decision owner to repair a Critical finding in the sibling unit
> `external-products` — cleared this stage's per-unit checkpoint and review receipts for every
> unit. This unit's answers, artifacts and prior reviewer verdict were **not** revised; the
> summary was re-confirmed and the artifact re-saved so the required receipts exist again.
> **No status claim is altered by this note** — the redaction serializer is still unbuilt and
> BLK-07's authorization limb is still open.
>
> **Repeated once more the same day**, after a second owner-directed redo of the same stage,
> **and a third time** after the seventh reviewer pass on `external-products`. **This unit was
> untouched by all three redos** — the redaction serializer is still unbuilt and BLK-07's
> authorization limb is still open.
>
> **And a fourth redo 2026-09-04**, to repair two Majors in `target-standardization`. **This unit was untouched by all four.**
>
> **And a fifth re-save 2026-09-04 — not a redo.** This stage's final pass ran on another clone
> of this repository, rooted at a different absolute path; the engine's completion check matches
> each artifact against the path recorded in its write receipt, so those confirmed writes are
> unreachable from this clone. The consolidated summary confirmation of `2026-09-04T14:07:48Z`
> **stands and was not re-asked**. This paragraph is the native-tool write that re-registers the
> artifact here. **No status claim is altered by this note** — the redaction serializer is still
> unbuilt and BLK-07's authorization limb is still open.
>
> *(Reader's note. The fourth-redo line above had been inserted mid-sentence by that earlier
> pass, splitting "BLK-07's … authorization limb is still open" across it. Repaired
> 2026-09-04 on the project decision owner's explicit instruction: the third-redo sentence is
> rejoined and the fourth-redo line now follows it whole. Presentation only — no wording was
> changed, and no finding or status claim is altered.)*

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

> ⚠ **The amendment is UNAPPROVED, not merely unbuilt** *(added 2026-09-04 on adversarial
> finding 3, Major)*. `component-methods.md`'s approved `src/data/locked_test.py` block
> defines `open_restricted` and carries **no `write_restricted` and no `_append_and_flush`**
> as approved symbols, and R-33 states plainly that the restricted writer and the
> `AccessRecord.purpose` extension *"need change records"* — BLK-07's routing contract is
> **proposed rather than approved until this clears change control**. So this design's Q2 = A
> decision is a proposal to that change-control gate, distinct from and prior to the "unbuilt"
> status stated above: `governance-guards` must accept the interface amendment before any
> implementation may exist to be built.

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
| FR-P1-00-1 | SD-A-01 | **TA-31** | `Pending` |
| FR-P1-00-2 | SD-A-01 | **TA-25** | `Pending` |
| FR-P1-01-1 | SD-A-01 | **TA-32** | `Pending` |
| FR-P1-01-2 | SD-A-01, SD-A-04 | **TA-15** | `Pending` |
| FR-P1-01-3 | SD-A-04 | **TA-03, TA-15** | `Pending` |
| FR-P1-01-4 | SD-A-04 | **TA-04, TA-15** | `Pending` |
| **FR-P1-01-5** | SD-A-04 | ⚠ **NO ACCEPTANCE ROW** | untested |
| FR-P1-01-6 | SD-A-03 | TA-08 | `Pending` |
| **FR-P1-01-7** | SD-A-04 | ⚠ **NO ACCEPTANCE ROW** | untested |
| **FR-P1-01-8** | SD-A-04 | ⚠ **NO ACCEPTANCE ROW** — `UNTESTED` in `requirements.md` | untested |
| **FR-P1-01-9** | SD-A-04 | ⚠ **NO ACCEPTANCE ROW** — `UNTESTED` in `requirements.md` | untested |
| **FR-P1-01-10** | SD-A-02 | TA-22 — **row owned by `foundation`, this unit supporting** | `Pending` — **NOT MET** |
| **FR-P1-01-11** | SD-A-04 | ⚠ **NO ACCEPTANCE ROW** — `UNTESTED` in `requirements.md` | untested |
| **NFR-SEC-01** | SD-A-02 | TA-22 — **row owned by `foundation`, this unit supporting** | `Pending` — **unclaimed** |
| **NFR-AUD-01** | SD-A-03 | **TA-10** (owned by `foundation`), **TA-21** (owned by **`fixtures-and-reproducibility`**) — this unit supporting both | `Pending` *(owner corrected 2026-09-04 on iteration-2 adversarial finding, Critical; superseded label preserved: "owned by `foundation`/`inventory-and-registry`". `unit-of-work.md` gives TA-21 to `fixtures-and-reproducibility` — the superseded pairing was carried from a sibling's table instead of derived from the ledger, the exact defect class this table's other cells were repaired for)* |
| **NFR-DQ-01** | SD-A-04 | **TA-19** — **row owned by `target-standardization`, this unit supporting** | `Pending` |
| **REQ-NFR-A1** | SD-A-04 | ⚠ **NO ACCEPTANCE ROW** — `UNTESTED` in `requirements.md` | untested — **this unit's own row, previously uncited** |
| **REQ-NFR-A2** | SD-A-04 | ⚠ **NO ACCEPTANCE ROW** — `UNTESTED` in `requirements.md` | untested — **this unit's own row, previously uncited** |

**Derived and printed**: 5 design sections (SD-A-00…SD-A-04); **19** coverage rows *(superseded
figures preserved: **14**, then **17**)* — counted directly from the table above. **7**
requirements with **no acceptance row** (FR-P1-01-5, -7, -8, -9, -11, REQ-NFR-A1, REQ-NFR-A2),
counted by reading this table's cells *(superseded: **2**, then **3** — the jump to 7 is
**5 + 2**: FR-P1-01-8 and FR-P1-01-11 reclassified from a fabricated `Pending`/TA-31 to their
true `UNTESTED`-no-row status, plus the two newly added REQ-NFR rows)*. **0** rows claimed
satisfied; **0** acceptance rows discharged.

> ### ⚠ CORRECTED 2026-09-04 on adversarial findings 1 and 2, both **Critical** — 17 → 19 rows, 8 cells re-derived, 4 rows re-owned
>
> **Finding 1 — eight of thirteen owned rows cited the wrong acceptance row**, verified against
> each ID's own row in `requirements.md` rather than against the ID set. The superseded values,
> preserved: FR-P1-00-1 and FR-P1-00-2 both cited **TA-04** (which belongs to `FR-P1-02-*`
> rows, none of them here); FR-P1-01-1 and FR-P1-01-2 both cited **TA-25** (FR-P1-00-2's real
> row); FR-P1-01-3, -4, -8 and -11 all cited **TA-31** (FR-P1-00-1's real row). The pattern —
> real rows reused against neighbouring IDs — reads as a shift across rows, not independent
> typos. **Worst of the eight: FR-P1-01-8 and FR-P1-01-11 were presented as `Pending` against
> TA-31 when `requirements.md` marks both `UNTESTED` with no acceptance row at all** — a
> fabricated test status, not merely a wrong number.
>
> **Finding 2 — four rows belong to other units, and this unit's own two were absent.**
> `unit-of-work.md`'s "Requirements carried (15)" list for `acquisition` contains
> **REQ-NFR-A1** and **REQ-NFR-A2** — neither appeared in either artifact, though § SD-A-04
> designs both requirements' substance (release-grade integrity; timestamp-derived membership)
> under other IDs' names. Meanwhile FR-P1-01-10, NFR-SEC-01 and NFR-AUD-01 are **`foundation`'s**
> and NFR-DQ-01 is **`target-standardization`'s**. All four are kept as rows — this unit
> genuinely contributes to each — but every one now carries its owning unit, matching how
> `governance-guards` records `FR-P1-05-12` and how this table's own NFR-AUD-01 cell already
> read ("owned elsewhere") one column from a bare `Pending` that implied otherwise.
>
> **Why five prior passes missed both**: every earlier check verified **ID-set completeness**
> (is any relevant ID missing) and never the **per-ID value** (does this ID's cited row match
> its own row in `requirements.md`) or the **per-ID owner** (does `unit-of-work.md` assign this
> ID here). A set-union check is structurally blind to a correctly-listed ID carrying a
> neighbour's acceptance row — the same blindness `governance-guards`' correction box records.
> Nothing here approves an acceptance row or discharges one; the newly-honest `UNTESTED` cells
> **widen** the recorded evidence gap.

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

> ⚠ **And the sweep above was itself too narrow, corrected 2026-09-04.** It ranged over
> `FR-P1-01-*` only, so it caught FR-P1-01-8/-9/-11 and was **structurally blind to
> `REQ-NFR-A1` and `REQ-NFR-A2`** — two requirements `unit-of-work.md` carries for this unit
> under a different prefix, both absent from both artifacts until adversarial finding 2 added
> them. A set-difference is only as complete as the ID range it is run over; the correct range
> is the unit's own "Requirements carried" list, not one prefix family of it.

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

## Review — 2026-09-05 adversarial pass (fresh receipt floor)

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-04T20:51:20Z
**Iteration:** 1
**Prior verdict does NOT hold.** The 2026-09-03 confirming pass verified that this table's **ID set** matches `logical-components.md`'s and that three named rows lack an acceptance row. It never checked each cited ID's acceptance row against that ID's **own row** in `requirements.md` — the per-ID check this sweep's dispatch brief requires, and the exact gap that let a Critical citation defect stand undetected in `governance-guards` for five passes. Run against this table, that check finds a Critical of the same class, plus a second, independent Critical on requirement ownership.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | `security-design.md` § Requirement coverage (lines 268–286); mirrored for two IDs in `logical-components.md` § Requirement coverage (lines 184–192) | **Most of this table's acceptance-row citations are wrong**, verified against each ID's own row in `requirements.md`. `requirements.md`'s actual rows: FR-P1-00-1 → **TA-31** (line 281); FR-P1-00-2 → **TA-25** (line 282); FR-P1-01-1 → **TA-32** (line 293); FR-P1-01-2 → **TA-15** (line 294); FR-P1-01-3 → **TA-03, TA-15** (line 295); FR-P1-01-4 → **TA-04, TA-15** (line 296). This table instead cites FR-P1-00-1 → TA-04, FR-P1-00-2 → TA-04, FR-P1-01-1 → TA-25, FR-P1-01-2 → TA-25, FR-P1-01-3 → TA-31, FR-P1-01-4 → TA-31 — **every one of these six rows is wrong**, and the values look shifted across rows rather than independently mistyped (TA-31 is FR-P1-00-1's real row, reused here for FR-P1-01-3/4/8/11; TA-25 is FR-P1-00-2's real row, reused for FR-P1-01-1/2; TA-04 belongs to none of the rows it is attached to here — it is FR-P1-02-1/2/3-1's row). **Worse, two rows misrepresent test status, not just the row number**: FR-P1-01-8 and FR-P1-01-11 are cited here as `Pending` against acceptance row **TA-31**, but `requirements.md` lines 338 and 297 give both as **`UNTESTED`, with no WS/TA row at all**. `logical-components.md` inherits the FR-P1-01-1/FR-P1-01-2 half of this defect (lines 186–187, same wrong TA-25 citation). This is the identical defect class the `governance-guards` sibling artifact records as Critical on its own centerpiece row (a substituted acceptance row surviving because prior passes checked the ID set, never the per-ID value) — it recurs here across eight of this table's thirteen `acquisition`-owned rows (62%), not one. | Re-derive every acceptance-row cell in this table directly from `requirements.md`'s own row for that ID — REQ-ENG-13 (TA-16, correct as-is), FR-P1-00-1 (TA-31), FR-P1-00-2 (TA-25), FR-P1-01-1 (TA-32), FR-P1-01-2 (TA-15), FR-P1-01-3 (TA-03, TA-15), FR-P1-01-4 (TA-04, TA-15), FR-P1-01-6 (TA-08, correct as-is), FR-P1-01-8 (`UNTESTED`, no row), FR-P1-01-11 (`UNTESTED`, no row). Correct the mirrored FR-P1-01-1/FR-P1-01-2 cells in `logical-components.md` in the same pass. Recompute the "3 requirements with no acceptance row" count afterward — with FR-P1-01-8 and FR-P1-01-11 correctly reclassified `UNTESTED`, the true count is **5** (FR-P1-01-5, -7, -8, -9, -11), not 3. |
| 2 | Critical | `security-design.md` § Requirement coverage (lines 268, 284–286); `logical-components.md` § Requirement coverage (lines 189–192) | **This unit's coverage tables claim requirements owned by other units, and omit the two requirements this unit actually owns.** `unit-of-work.md` line 196 gives `acquisition`'s own "Requirements carried (15)" list — it contains **REQ-NFR-A1** and **REQ-NFR-A2**, not FR-P1-01-10, NFR-SEC-01, NFR-AUD-01, or NFR-DQ-01. Those four instead belong elsewhere per `unit-of-work.md`'s own per-unit `Owns`/`Requirements carried` blocks: FR-P1-01-10, NFR-SEC-01 and NFR-AUD-01 are `foundation`'s (line 129, "**Requirements carried (16)**… FR-P1-01-10 … NFR-AUD-01, NFR-SEC-01"), and NFR-DQ-01 is `target-standardization`'s (line 261, "**Requirements carried (6)**… NFR-DQ-01"). Both `security-design.md` (4 of 17 rows) and `logical-components.md` (4 of 7 rows — the majority of that table) build coverage rows for these four IDs as if this unit's own design sections and components discharge them. Meanwhile **REQ-NFR-A1 and REQ-NFR-A2 do not appear anywhere in either nfr-design artifact** (`grep -rn "REQ-NFR-A1\|REQ-NFR-A2"` on both files: zero hits), even though this unit's own § SD-A-04 substantively designs both: REQ-NFR-A1 is "driver release-grade integrity… no value backfilled from a future final archive" — the same substance § SD-A-04 designs under FR-P1-01-8's citation; REQ-NFR-A2 is "fold/partition membership derives from record timestamps only" — the same substance § SD-A-04's R-31 paragraph designs, uncited to its own requirement ID. This is the "mechanism vs. wrong-unit attribution" defect class named in the dispatch brief, applied to requirement ownership rather than a module path: the unit is credited with covering four requirements it does not own and is silent on the two it does. | Remove FR-P1-01-10, NFR-SEC-01, NFR-AUD-01 and NFR-DQ-01 from this unit's coverage tables (or state explicitly, if intentional, that this unit is a *supporting* contributor to a row owned elsewhere — as `logical-components.md`'s own "TA-10, TA-21 — both rows, owned elsewhere" phrasing already does for NFR-AUD-01, which contradicts treating it as this unit's row one column over). Add REQ-NFR-A1 and REQ-NFR-A2 as their own coverage rows, citing their actual `requirements.md` status (both `UNTESTED`, no acceptance row — lines 527–528) and pointing at the § SD-A-04 paragraphs that already design their substance under the wrong requirement IDs. Recompute the 17/7/7-shared/10-SD-only arithmetic afterward — it will change. |
| 3 | Major | `security-design.md` § SD-A-03 (lines 186–210); `logical-components.md` § A-3 (lines 132–144) | **`write_restricted` is presented as a settled Q2=A design decision, without disclosing that the underlying interface amendment is itself unapproved**, not merely unbuilt. `functional-design/business-rules.md` R-33 (line 798) states plainly: *"R-32's named accessors — `open_d9_input` and the restricted writer — are absent from `component-methods.md`'s approved `src/data/locked_test.py` block, and they are BLK-07's central mechanism, so BLK-07's routing contract is proposed rather than approved until this clears change control… R-33 extends `AccessRecord.purpose` and adds a restricted-write function to the same file… need change records."* `component-methods.md` was checked directly: it defines `open_restricted` (line 276) but contains no `write_restricted` or `_append_and_flush` symbol at all. Both nfr-design artifacts state only that `write_restricted` "does not exist" (implementation-pending framing) — never that the function and its `AccessRecord.purpose` extension are not yet an approved part of the interface contract they are designed against, and require a change-control record before `governance-guards` may even accept the amendment. | Add one sentence at § SD-A-03/§ A-3 stating the amendment's approval status: `write_restricted` and the `AccessRecord.purpose` extension are not yet in `component-methods.md`'s approved contract and require a change-control record (per `business-rules.md` R-33) before `governance-guards` can accept them, distinct from and prior to the "unbuilt" status already stated. |

### Verified — did not break

- **Disk-state claims (re-verified today, not from a prior pass's record):** `grep -rn "CredentialEgressError\|redact" src/ scripts/ tests/` → 0 hits; `grep -rn "write_restricted" src/ scripts/ tests/` → 0 hits; `open_restricted` present at `src/data/locked_test.py:147`, exercised by `tests/test_locked_test_guard.py`, `tests/test_acquisition_window.py`, `tests/test_release_hashes.py`, and routed through by `scripts/merge_coverage_year.py`'s `guarded()`. `configs/`, `pyproject.toml`, `requirements.txt` all absent. `evidence/locked_test_restricted/audit_evidence_2022-FULL/` holds exactly `request_manifest.json`, `sha256_manifest.json`, three CSVs and `PROVENANCE_NOTICE.md`, matching the claimed set.
- **D-numbers.** D-31 (line 1626, "G-09 (Agent preflight) is signed, with its §18.3 preconditions recorded as unmet") and D-15 (line 651) both exist in `evidence/DECISIONS.md`, matching this artifact's citations. No D-number beyond D-32 was cited by this artifact.
- **Sibling spot-check (the one permitted read).** `write_restricted`'s stated home, `governance-guards`' exempt-list count of **seven**, was independently confirmed inside that unit's own `security-design.md` (DISC-1, "seven members on disk, not six") — consistent with this unit's citation. The ownership statement ("`acquisition` is its caller, not its co-owner") is not contradicted by anything in that sibling file.
- **Printed counts.** 5 design sections (SD-A-00…SD-A-04), 3 components (A-1…A-3, in the sibling artifact), 17 coverage rows in this table, 7 shared / 10 SD-only / 0 LC-only — all recount correctly from the current tables' row lists as printed, independent of finding #1's per-cell content defect. The "3 requirements with no acceptance row" *count of rows so labelled* is internally consistent with the table's own `NO ACCEPTANCE ROW` markers; finding #1 shows the true figure should be 5 once FR-P1-01-8/-11 are corrected, which is a consequence of that finding rather than a separate arithmetic error.
- **Cross-artifact consistency.** Both artifacts agree on every figure and status checked, including the two defects found here — `logical-components.md` reproduces the same wrong FR-P1-01-1/FR-P1-01-2 citations and the same four wrong-unit rows, so the recurring "one artifact repaired, its sibling not" pattern does not apply; both need the same fix.
- **Overclaim sweep.** No row is claimed satisfied or discharged; BLK-07's authorization limb, the redaction serializer, and `write_restricted` are all still stated as open/unbuilt; no `TBD — freeze gate` field is filled; no scientific value is decided. DATA-07's three-month caveat and the supervisor-owned NFR-SEC-01/Madrigal-identity conflict are both still stated, unsoftened.
- **Receipt-floor notes.** All five re-save notes on this file and the two on `logical-components.md` state no new design claim and contradict nothing checked above.
- **Q1–Q3 implementation as answered** (independent of the ownership/citation defects above): § SD-A-02's unconditional-refusal-for-two-named-carriers-plus-heuristic design, and § SD-A-03's sibling-function/shared-`_append_and_flush`/exempt-list-stays-at-seven design, both match Q1=A and Q2=A as stated in `nfr-design-questions.md`.

### Coverage limits of this pass

- Read-scope bound honoured: only `unit-of-work.md` (shared inception contract), `requirements.md` (shared inception contract), `component-methods.md` (shared inception contract), and the single named integration-point file `governance-guards/nfr-design/security-design.md` were opened outside this unit's own artifacts. No other sibling `construction/<other-unit>/` content was read.
- The suite was not executed; the "277 passed / 2 skipped, off-pin" figure is quoted from the artifact, not re-measured, and is already labelled *not governed evidence* there.
- Component and boundary soundness (the egress-direction boundary criterion, A-1/A-2/A-3 isolation properties) was re-read and not found unsound in itself; this pass's findings are about the requirement-coverage tables, not the decomposition.
- Findings #1 and #2 were found by the per-ID/per-owner check the dispatch brief specifies; a full independent re-derivation of every remaining `requirements.md` cross-reference in this document (e.g., R-30…R-43, W-2…W-9, TS-A-01…05) was not performed under this pass's budget.

### Summary

Two Criticals, both citation-integrity defects the prior confirming pass's ID-set-only check could not catch: most of the requirement-coverage table's acceptance-row citations are wrong against `requirements.md`'s own per-ID rows (including two rows that hide `UNTESTED` status behind a fabricated `Pending`/TA-31), and four of the table's rows credit this unit with requirements `unit-of-work.md` assigns to `foundation` and `target-standardization` while this unit's own REQ-NFR-A1/REQ-NFR-A2 never appear at all. A third, Major finding notes that `write_restricted`'s design is stated as unbuilt but not as an unapproved interface amendment awaiting change control. All previously-verified disk-state claims, D-number citations, and cross-artifact consistency hold. NOT-READY.

---

## Review — 2026-09-05 adversarial repair-verification pass (iteration 2, final)

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-04T21:06:17Z
**Iteration:** 2 (of 2, final)
**Prior verdict does NOT hold.** Iteration 1's Findings 1 and 2 (both Critical, citation and
ownership) and Finding 3 (Major, unapproved-amendment disclosure) were repaired. Findings 1 and
3 verify clean against `requirements.md` and `component-methods.md`/`business-rules.md`
respectively. Finding 2's repair introduces a new, independently checkable Critical of the exact
same defect class it was fixing: one of the four re-owned rows now names the **wrong** owning
unit.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Critical | `security-design.md` § Requirement coverage, `NFR-AUD-01` row (line 295); `logical-components.md` § Requirement coverage, `NFR-AUD-01` row (line 198) | **The Finding-2 repair's new ownership label misattributes acceptance row TA-21.** Both tables now read *"TA-10, TA-21 — both rows, owned by `foundation`/`inventory-and-registry`, this unit supporting."* Verified against `unit-of-work.md`'s own per-unit `**Acceptance rows (N).**` lines (the shared inception contract this repair itself cites as its source): TA-10 is correctly `foundation`'s (line 133: "TA-01, TA-02, TA-03, TA-10, TA-15, TA-22, TA-23"). **TA-21 is not `inventory-and-registry`'s — it belongs to `fixtures-and-reproducibility`** (line 527: "**Acceptance rows (4).** WS-20, TA-09, TA-17, TA-21"). `inventory-and-registry`'s own list (line 233) is "WS-01, TA-04, TA-25" and contains no TA-21. The requirement `NFR-AUD-01` itself is also solely `foundation`'s per its "Requirements carried (16)" line (129) — `inventory-and-registry`'s "Requirements carried (7)" list (line 229) does not contain it either. So `inventory-and-registry` has no documented claim on this row from either the requirement-ownership or the acceptance-row-ownership angle; the citation appears to have been invented rather than derived. This is the identical defect class Findings 1 and 2 already found Critical on this artifact twice — a paired ID substituted without checking it against the shared contract that is supposed to settle it — now reintroduced by the very repair meant to fix that class of error, and it lands in both sibling artifacts identically. | Correct both cells to *"TA-10, TA-21 — TA-10 owned by `foundation`, TA-21 owned by `fixtures-and-reproducibility`, this unit supporting"* (or the equivalent two-owner phrasing `logical-components.md`'s own § Relation prose uses elsewhere). Re-run the per-ID/per-owner check from this iteration's dispatch brief over the *other* three re-owned rows' labels too (FR-P1-01-10/TA-22→foundation, NFR-SEC-01/TA-22→foundation, NFR-DQ-01/TA-19→target-standardization) — all three were independently reverified in this pass and are correct as stated, but the TA-21 miss shows the check that would have caught it (cross the label against the named unit's own `Acceptance rows` line, not just its `Requirements carried` line) was not run uniformly across all four rows before this repair landed. |

### Verified — did not break

- **Finding 1's repair (all ten cited acceptance-row cells) re-derived independently against `requirements.md`'s own per-ID rows, not from the correction box's account:** REQ-ENG-13→TA-16 (line 275, unchanged from iteration 1, correct), FR-P1-00-1→TA-31 (line 281, correct), FR-P1-00-2→TA-25 (line 282, correct), FR-P1-01-1→TA-32 (line 293, correct), FR-P1-01-2→TA-15 (line 294, correct), FR-P1-01-3→TA-03,TA-15 (line 295, correct), FR-P1-01-4→TA-04,TA-15 (line 296, correct), FR-P1-01-6→TA-08 (line 299, unchanged, correct), FR-P1-01-8→`UNTESTED`/no row (line 338, confirmed — `requirements.md`'s own Test column reads `UNTESTED`, no WS/TA row), FR-P1-01-11→`UNTESTED`/no row (line 297, confirmed). The mirrored FR-P1-01-1/FR-P1-01-2 cells in `logical-components.md` (lines 193–194) carry the same corrected TA-32/TA-15 values. REQ-NFR-A1 and REQ-NFR-A2 both independently confirmed `UNTESTED` with no acceptance row in `requirements.md` (lines 527–528), matching both artifacts' new rows.
- **The "5 + 2 = 7" no-acceptance-row recount reproduces exactly** from the table's own `NO ACCEPTANCE ROW` markers: FR-P1-01-5, -7, -8, -9, -11, REQ-NFR-A1, REQ-NFR-A2 — seven IDs, each independently confirmed `UNTESTED` with no WS/TA row in `requirements.md`.
- **The 19/7 row counts and the 7-shared / 12-SD-only / 0-LC-only decomposition all recompute correctly by ID set-difference, not by total.** `security-design.md`'s 19 rows and `logical-components.md`'s 7 rows were each enumerated from their tables; the intersection is exactly the 7 IDs both artifacts list under § Relation (FR-P1-01-1, -2, -6, -10, NFR-SEC-01, NFR-AUD-01, NFR-DQ-01); the SD-only remainder is exactly the 12 IDs listed there (REQ-ENG-13, FR-P1-00-1, FR-P1-00-2, FR-P1-01-3, -4, -5, -7, -8, -9, -11, REQ-NFR-A1, REQ-NFR-A2); 7 + 12 = 19 with no LC-only remainder. Arithmetic is sound independent of finding #1 above.
- **Three of the four "re-owned" rows verify clean against `unit-of-work.md`.** FR-P1-01-10→TA-22 and NFR-SEC-01→TA-22, both labelled "owned by `foundation`": `foundation`'s "Acceptance rows (7)" line (133) contains TA-22, and its "Requirements carried (16)" line (129) contains both FR-P1-01-10 and NFR-SEC-01. NFR-DQ-01→TA-19, labelled "owned by `target-standardization`": that unit's "Acceptance rows (1)" line (265) is exactly "TA-19", and its "Requirements carried (6)" line (261) contains NFR-DQ-01. Only the fourth (NFR-AUD-01/TA-21) fails, per finding #1.
- **REQ-NFR-A1 and REQ-NFR-A2's presence in `acquisition`'s own requirement set is confirmed**, not assumed: `unit-of-work.md`'s "Requirements carried (15)" line for `acquisition` (line 196) lists both by name, alongside all thirteen `FR-P1-*`/`REQ-ENG-13` IDs the table already carried. The decision to omit both from `logical-components.md`'s 7-row table is internally consistent with that file's own § Relation section, which explicitly lists both as SD-only and states the reason (no component-boundary question); this does not contradict any completeness claim `logical-components.md` makes about itself.
- **Finding 3's repair verified at both sites** (`security-design.md` § SD-A-03, `logical-components.md` § A-3) against `component-methods.md` and `business-rules.md` R-33 directly, not from the correction box's account. `component-methods.md` was grepped for `write_restricted`, `_append_and_flush` and `open_restricted`: only `open_restricted` (line 276) is present; the other two return zero hits — the approved block genuinely carries neither symbol. `business-rules.md` R-33's own Assumptions bullet (line 798) states verbatim: *"R-32's named accessors… are absent from `component-methods.md`'s approved `src/data/locked_test.py` block… BLK-07's routing contract is proposed rather than approved until this clears change control… (2) R-33 extends `AccessRecord.purpose` and adds a restricted-write function to the same file… All three need change records."* Both repaired boxes' quotations match this source accurately.
- **Spot-checks of untouched cells show no drift.** REQ-ENG-13→TA-16 and FR-P1-01-6→TA-08 are byte-identical to their iteration-1 state and independently reconfirmed against `requirements.md` above. Disk-state claims, D-number citations and cross-artifact consistency were not re-litigated this pass (the repair did not touch them); nothing in the repaired text contradicts them.

### Coverage limits of this pass

- Read-scope bound honoured: only `unit-of-work.md`, `requirements.md`, `component-methods.md`, `business-rules.md` (this unit's own functional-design artifact) and the workspace grep of `component-methods.md` were opened outside this unit's own two nfr-design artifacts. No other sibling `construction/<other-unit>/` content was read, and no `construction/*/` glob was used.
- The full `unit-of-work.md` was consulted only for the twelve `Acceptance rows (N)` and `Requirements carried (N)` per-unit lines relevant to the rows this table cites; a complete audit of every acceptance-row citation in `security-design.md` against its owning unit (e.g. TA-31, TA-25, TA-04, TA-03, TA-08, TA-15, TA-16, TA-32 for the other ten rows) was not performed, because those citations carry no ownership claim to verify — they are the same unlabelled pattern already confirmed sound for FR-P1-01-6→TA-08 in iteration 1, where a requirement genuinely carried by `acquisition` cites an acceptance row built and tracked by a different unit's test suite without implying this unit built that module. Only the four rows this repair explicitly labelled "owned by X" were checked against that label.
- D-number citations, disk-state claims (`grep` results for `CredentialEgressError`, `write_restricted`, `configs/`/`pyproject.toml`/`requirements.txt` absence) and the suite's off-pin figure were not re-executed this pass; the repair did not touch this content and iteration 1's verification of it stands.
- This is the final iteration of this repair-verification budget (2). The single Critical finding above must be corrected before this artifact can be re-submitted for a fresh pass or carried to the gate as an open finding.

### Summary

Findings 1 and 3 from iteration 1 repaired cleanly: every re-derived acceptance-row cell, the 5+2=7 no-acceptance-row recount, and the 19/7/7-shared/12-SD-only/0-LC-only decomposition all verify against `requirements.md` and each other. Finding 3's unapproved-amendment disclosure at § SD-A-03/§ A-3 quotes `business-rules.md` R-33 and `component-methods.md` accurately. Finding 2's ownership-labelling repair is three-quarters correct — FR-P1-01-10, NFR-SEC-01 and NFR-DQ-01 all check out against `unit-of-work.md`'s per-unit `Acceptance rows`/`Requirements carried` lines — but the fourth row, NFR-AUD-01, misattributes TA-21 to `inventory-and-registry` when `unit-of-work.md` assigns that acceptance row to `fixtures-and-reproducibility`, in both `security-design.md` and `logical-components.md` identically. This is the same substitution-without-verification defect class the prior two Criticals were raised for, reintroduced by their own repair. NOT-READY.

---

## Superseded review — 2026-09-02 post-redo confirming pass (retained for record; superseded by the pass above)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-03T10:13:45Z
**Iteration:** 1 (of 2) — confirming pass after three `STAGE_JUMPED` redos of `nfr-design` ordered against the sibling unit `external-products`
**Prior verdict still holds:** Yes. No regression found; every present-tense workspace claim re-verified against disk today. Two Minor findings, neither blocking.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Minor | `security-design.md` (whole file) | The dispatch brief states the prior verdict is recorded in this file's own `## Review` section; `grep -n "^## Review"` returned no match (exit 1) before this section was appended. The earlier verdict is therefore not recoverable from the artifact — the re-save preserved the design text but not the review receipt. | No action on the design. This section restores the record; if the earlier verdict text is held elsewhere, quote it here at the next pass. |
| 2 | Minor | `security-design.md` § SD-A-02 ⚠ box; `logical-components.md` § A-2 | Q3's limb-2 rationale is prospective, not remedial, and the artifacts do not say so. `notebooks/madrigal_phase1_coverage_audit.ipynb` carries **14 code cells, all with `"outputs": []` and `"execution_count": null`** — zero saved output cells today. The design never claims otherwise (it says only that the notebook "is in the workspace today", which is true, and the live identity exposure is `USER_EMAIL` in cell **source**, 4 hits, not in outputs), but the juxtaposition invites a reader to treat the pre-commit hook as clearing an existing leak. | Add one measured clause: the hook is preventive — the notebook holds no saved outputs as of this date — and the `USER_EMAIL` exposure sits in cell source, which limb 2 does not reach either. |

### Checks run

| Check | Command / method | Result | Interpretation |
|---|---|---|---|
| Redaction serializer absent | `grep -rn "CredentialEgressError\|redact" src/ scripts/ tests/` | 0 hits | Claim **holds**. `SD-A-00` row 3, both ⚠ boxes and both Assumptions lists are current. |
| `write_restricted` absent | `grep -rn "write_restricted" src/ scripts/ tests/` | 0 hits | Claim **holds**. R-33 contract genuinely unbuilt. |
| `open_restricted` present | same grep | `src/data/locked_test.py:147` (def); `scripts/merge_coverage_year.py:76,107` routes via `guarded()`; exercised by `tests/test_locked_test_guard.py`, `tests/test_acquisition_window.py`, `tests/test_merge_script_restricted_reads.py` | `SD-A-00`'s "half stale" characterisation of SEC-A-04 is **exactly right** — read side exists, write side does not. |
| FULL artifact set | `ls evidence/locked_test_restricted/audit_evidence_2022-FULL/` | `request_manifest.json`, `sha256_manifest.json`, 3 CSVs, `PROVENANCE_NOTICE.md` | `SD-A-00` row 2 **holds**, including the `PROVENANCE_NOTICE.md` claim at § SD-A-04. |
| Notebook saved outputs | `grep -c '"output_type"'` = **0**; `"outputs": []` = 14; `"execution_count": null` = 14 | No saved outputs | See finding 2. No artifact claim is falsified; the framing is what is thin. |
| TC-06 scaffold | `ls configs/ pyproject.toml requirements.txt` | all three absent | "TC-06's scaffold precondition unmet" **holds**; the off-pin/not-governed-evidence caveat stands. |
| Coverage-table count, this file | rows enumerated by hand from the table | **17** (REQ-ENG-13, FR-P1-00-1/2, FR-P1-01-1…11, NFR-SEC-01, NFR-AUD-01, NFR-DQ-01) | Printed **17** is **correct**; the preserved superseded **14** is correctly labelled. |
| Rows with no acceptance row | `grep -c "NO ACCEPTANCE ROW"` = 3 → FR-P1-01-5, -7, -9 | **3** | Printed **3** is **correct** (superseded **2** correctly preserved). |
| Section count | `## SD-A-00` … `## SD-A-04` | **5** | Printed **5** correct. |
| Sibling table + set difference | `logical-components.md`: 7 rows enumerated; shared set = FR-P1-01-1, -2, -6, -10, NFR-SEC-01, NFR-AUD-01, NFR-DQ-01; SD-only list enumerated = REQ-ENG-13, FR-P1-00-1, FR-P1-00-2, FR-P1-01-3, -4, -5, -7, -8, -9, -11 | 7 shared, **10** SD-only, **0** LC-only, 7 + 10 = **17** | Every printed figure re-derived and **correct**; the ID lists were set-differenced, not the totals. |
| Cross-artifact consistency | both artifacts compared on: 17/14 correction, serializer status, `write_restricted` status, exempt list at **seven**, G-09 signed / stage 3.1 FAIL, DATA-07 three-month caveat, redo note | **No divergence** | The repeated defect of this stage — a repair landing in one artifact and not its sibling — **did not recur here**; both carry the corrected 17 in prose, table and heading, and both carry the third-redo note. |
| No satisfaction/discharge claim | read both `## Assumptions & Open Questions` closers and every `Status` cell | 0 rows satisfied, 0 acceptance rows discharged, BLK-07 authorization limb open, no freeze-gate value filled, no module write authorised beyond G-09/D-31 | **Holds** in both artifacts. |
| Q1–Q4 implemented as answered | § SD-A-02 (Q1: unconditional refusal for signed URL / auth header, blocking heuristic elsewhere naming its match, allowlist trap stated as a review surface never grown to silence a failure); § SD-A-03 (Q2: sibling function in `governance-guards`' module, shares `_append_and_flush`, exempt list stays at seven, ownership stated as caller-not-owner); § SD-A-02 limb 2 (Q3: pre-commit refusal, not auto-strip, with the tagged-history argument); `logical-components.md` § boundary criterion (Q4: egress direction, with both rejected alternatives argued) | All four implemented with costs and residuals stated | No answered question is under-designed or silently softened. |

### Coverage limits of this pass

- Read-scope bound honoured: no sibling unit's `construction/<other-unit>/` file was opened, grepped or globbed. The claims about `governance-guards`' module ownership, its DISC-1 exempt list of seven, and `foundation` § SD-01/SEC-F-02 are **this unit's own characterisation** and were not verified against those units' artifacts. The one workspace fact I could check without crossing that bound — that `open_restricted` lives in `src/data/locked_test.py` — is confirmed.
- The suite was **not executed**; the "277 passed / 2 skipped, off-pin under Python 3.14.7 / pytest 9.1.1" figure is quoted from the artifact, not re-measured. It is labelled *not governed evidence* in the artifact itself, so nothing rests on it.
- Component and boundary soundness was re-read but not re-litigated; the prior pass's assessment stands.

### Summary

Nothing in this unit regressed across the three redos, and nothing has gone stale: all four disk-checkable claims — no redaction serializer and no `CredentialEgressError`, `open_restricted` present with R-33's write contract absent, the FULL manifest set complete, and the TC-06 scaffold missing — verify against the workspace today, and every printed count (17 rows, 3 without an acceptance row, 5 sections, 3 components, 7 shared / 10 SD-only / 0 LC-only) re-derives correctly from the current files. The two artifacts agree on every corrected figure and status, so the one-artifact-repaired-and-not-its-sibling defect that recurred four times in this stage did not recur here. The two Minor findings are a missing prior-review receipt in the file and one prospective-versus-remedial framing around the notebook; neither changes a design decision.

---

## Receipt-floor note — 2026-09-04 (re-saved after the second re-affirmation)

*A second redo jump was taken because the first recovery ran confirm/write/review out of
order. This unit's design is untouched by any of it.*

A **redo jump** on `nfr-design` reset this stage's receipt floor, invalidating this unit's
summary-confirmation and review receipts. The jump was taken to lift the review-freeze on two
*other* units whose adversarial findings the project decision owner directed be fixed; the
reset is stage-wide.

**No design content changed and no claim above is altered by this note** — the redaction
serializer and `CredentialEgressError` are still absent, R-33's write contract is still
unbuilt, and every printed count stands as re-derived. The stored confirmation was re-affirmed
by the owner on 2026-09-04 (its value was already `Looks correct`), and this artifact is
re-saved unchanged so the engine's write-after-confirmation precondition is satisfied honestly
rather than bypassed.

---

## Review — 2026-09-04 confirming pass (fourth floor)

**Reviewer:** aidlc-architecture-reviewer-agent

**Verdict:** READY

**Date:** 2026-09-04T22:07:18Z

**Iteration:** 1 (fresh receipt floor)

### Findings

None.

### Verified — did not break

- **The TA-21 fix, re-derived independently against `unit-of-work.md`.** Read `unit-of-work.md`'s own per-unit `**Acceptance rows (N).**` lines directly: line 133, under § 1 `foundation`, reads "TA-01, TA-02, TA-03, TA-10, TA-15, TA-22, TA-23" — **TA-10 is `foundation`'s**. Line 527, under § 12 `fixtures-and-reproducibility`, reads "WS-20, TA-09, TA-17, TA-21" — **TA-21 is `fixtures-and-reproducibility`'s**. Both files' `NFR-AUD-01` rows (`security-design.md` line 295, `logical-components.md` line 198) now read exactly this pairing, with the superseded `foundation`/`inventory-and-registry` label preserved and dated. The one cell that flipped on this floor is correct.
- **Re-derived acceptance cells spot-checked against `requirements.md` per-ID rows.** FR-P1-00-1 (line 281) → `TA-31`, matching the table. FR-P1-01-1 (line 293) → `TA-32`, matching the table. FR-P1-01-8 (line 338) → `UNTESTED`, no acceptance row — matching the table's `NO ACCEPTANCE ROW` marker. REQ-NFR-A1/REQ-NFR-A2 (lines 841, 528, 919) are `UNTESTED` with no row, matching both tables' rows, which are now present and correctly labelled "this unit's own row, previously uncited."
- **19-row count and 7+12 decomposition.** Counted the coverage table in `security-design.md` by hand: 19 data rows (REQ-ENG-13, FR-P1-00-1/2, FR-P1-01-1…11, NFR-SEC-01, NFR-AUD-01, NFR-DQ-01, REQ-NFR-A1, REQ-NFR-A2). 7 carry `NO ACCEPTANCE ROW` (FR-P1-01-5/-7/-8/-9/-11, REQ-NFR-A1, REQ-NFR-A2), matching the printed "5 + 2 = 7" derivation. `logical-components.md`'s 7-row table plus this file's 10 SD-only rows sums to 17 (the pre-REQ-NFR-A1/A2 total), and 17 + 2 = 19 — consistent with the printed decomposition.
- **R-33 change-control disclosure present at both sites.** `security-design.md` lines 213–214 and `logical-components.md` lines 147–149 both state that `write_restricted`/`AccessRecord.purpose` are absent from `component-methods.md`'s approved block and require a change-control record under R-33 before `governance-guards` may accept the amendment — the Major finding's repair is in place at both files, not just one.
- **Regression grep, live text only.** Searched both files for `inventory-and-registry`: the only hits are inside the preserved-superseded quotation on the NFR-AUD-01 row and inside `## Review` sections recounting past findings — no live mispairing. Read the full coverage tables in both files line-by-line: TA-04 appears only on FR-P1-01-4 (its own row per `requirements.md`'s TA-03/TA-04/TA-08/TA-15/TA-22/TA-32 grouping for FR-P1-01-1…11), TA-25 only on FR-P1-00-2, TA-31 only on FR-P1-00-1 — no superseded pairing is live.
- **Overclaim sweep.** Line 306 and line 394 both state 0 rows satisfied, 0 acceptance rows discharged; `write_restricted` grep (line 389, re-confirmed) returns 0 hits in `src/`, `scripts/`, `tests/`; DATA-07's three-month caveat is stated unsoftened at lines 51, 266, 366.

### Coverage limits

Read-scope bound to this unit's `nfr-design/` artifacts, its own `nfr-requirements/`/`functional-design/`, the shared `unit-of-work.md` contract, and the one permitted sibling file `governance-guards/nfr-design/security-design.md` (not re-read this pass — no new claim against it was introduced). Disk-state claims not touched by this floor's fix (redaction serializer, `CredentialEgressError`, FULL manifest set, TC-06 scaffold) were not re-executed; iteration 1's and iteration 2's verification of them stands unchanged.

---

## Review — 2026-09-05 re-affirmation (post-gate receipt refresh)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T08:07:50Z
**Iteration:** 1 (re-affirmation, fresh receipt after a stage-gate rejection that revised four
other units — `acquisition`'s own artifacts were not part of that revision)

**Prior terminal review quoted verbatim** (§ "Review — 2026-09-04 confirming pass (fourth
floor)", immediately above): Verdict READY, Reviewer aidlc-architecture-reviewer-agent, Date
2026-09-04T22:07:18Z, Iteration 1 (fresh receipt floor), Findings: None. That pass verified the
TA-21 ownership fix (`NFR-AUD-01` → `foundation`/`fixtures-and-reproducibility`, correcting the
iteration-2 misattribution to `inventory-and-registry`) and reconfirmed the 19-row coverage
table, the 5+2=7 no-acceptance-row decomposition, and R-33's change-control disclosure at both
`security-design.md` and `logical-components.md`.

**No edits since that pass, confirmed two ways.** (1) The audit shard's last `ARTIFACT_UPDATED`
event for this file is timestamped 2026-09-04T22:07:45Z, immediately followed by the fourth-floor
review's `SUBAGENT_COMPLETED` event at 2026-09-04T22:07:55Z — no later update event for this file
exists in `audit/git-ae-srv-rdt1-8d4da85135a5.md`. (2) The gate rejection this receipt refresh
responds to required fresh reviews for eight units whose completion gate blocked on missing
receipts; `acquisition`'s prior terminal pass already satisfied that gate, and nothing in this
file's content overlaps the four units the gate rejection's revisions actually touched.

**Spot-checks re-verified against current disk state:**
- `unit-of-work.md` line 527, § 12 `fixtures-and-reproducibility`: `**Acceptance rows (4).** WS-20, TA-09, TA-17, TA-21` — TA-21 is still `fixtures-and-reproducibility`'s, matching the corrected `NFR-AUD-01` cell (line 295) exactly.
- `write_restricted` still returns 0 hits across `src/`, `scripts/`, `tests/` — R-33's write contract remains unbuilt, matching the § SD-A-03 disclosure.
- The coverage table's data rows re-count to **19** by direct enumeration, matching the printed derivation.

**Verdict:** READY — the standing terminal verdict is unchanged and correctly carried forward; this unit's artifacts are unaffected by the gate rejection that prompted this receipt refresh.

READY
