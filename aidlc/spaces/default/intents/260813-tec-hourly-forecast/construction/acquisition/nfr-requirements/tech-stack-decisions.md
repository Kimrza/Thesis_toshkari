# Tech Stack Decisions — `acquisition`

**Unit** `acquisition` (Bolt 3) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ THIS UNIT SELECTS NOTHING NEW, AND CLAIMS NOTHING INSTALLED
>
> The governed stack is fixed by **TE §8** and transcribed at
> `../../foundation/nfr-requirements/tech-stack-decisions.md`. This unit **uses** two
> components TE §8.1 already approves and adds none.
>
> **One of them is conditional and remains so.** `madrigalWeb` is **conditional on D-144
> approval**, which has not been given. Nothing here treats it as settled.
>
> No Python interpreter exists in this environment; **TA-15, TA-22, TA-32 and the §18.3
> preflight are undischarged**; **G-09 is signed (D-31) with preconditions UNMET**; stage
> 3.1 remains **FAIL**; **BLK-07 is open**.

## Sources

- `../../foundation/nfr-requirements/tech-stack-decisions.md` — the governed stack, its prohibitions, the platform rules, and the `TBD — freeze gate` TensorFlow pin. Referenced, not restated.
- `../functional-design/business-rules.md` — **R-30**, **R-34**, **R-35**, **R-36**, **R-38**, **R-39**, **R-40**.
- `../functional-design/business-logic-model.md` — **W-1** (retrieving the approved prepared VTEC product), **W-3**, **W-4**, **W-8** (the notebook and the script), **W-9**, **W-11**.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§8.1** (`madrigalWeb` conditional on D-144; `h5py`/`netCDF4` conditional on the approved export format; `requests` *"where provider terms permit"*; stdlib `urllib`, `hashlib`, `csv`, `json`, `zipfile` required for acquisition/audit code with **no scientific TEC transformation**), **§9.1**, **§12**, **§14**.
- `nfr-requirements-questions.md` — Q1 = A, Q2 = A, and the receipted Consolidated Summary Confirmation.

---

## TS-A-01 — The retrieval client, and why it is still conditional

| Component | TE §8.1 status | Used here for |
|---|---|---|
| `madrigalWeb` client/API | **Conditional on D-144 approval** | Exact experiment/file discovery, parameter-filtered prepared `gps` retrieval, permanent citation support |
| `requests` | Preferred, *"where provider terms permit"* | Controlled downloads |
| stdlib `urllib`, `hashlib`, `csv`, `json`, `zipfile` | **Required** for acquisition/audit code | HTTPS retrieval, manifests, SHA-256, packaging — **no scientific TEC transformation** |

**`madrigalWeb` is not adopted here.** TE §8.1 makes it conditional on **D-144**, and no
D-number records that approval. This artifact records the dependency as **conditional and
unapproved**, and states the consequence: **`madrigalWeb_version` is a required manifest
field** (R-35 — an absent key fails exactly as `"unknown"` fails), so the client's version
is recorded whether or not the client is finally approved. If D-144 is refused, the
retrieval path changes and this section returns for re-decision.

**Requirement — the client is pinned, or its exact web-service interface recorded.** TE §8.1
gives both forms; either satisfies the environment lock, and neither is chosen here because
the choice depends on D-144.

**No scientific transformation in the retrieval layer** (R-30, TE §8.1). The stdlib set is
listed by TE explicitly *"for acquisition/audit code"* with that constraint attached.

## TS-A-02 — The prepared-product reader is frozen after the schema audit, not now

| Component | TE §8.1 status |
|---|---|
| `h5py` and/or `netCDF4` | **Conditional on the approved Madrigal export format** — *"exact format and dependency are frozen after the schema audit"* |

**Not chosen here.** The schema audit has not run. Recording `h5py` as the reader would fix a
dependency on an unaudited format, which is the same class of act TE §18.2 forbids for
scientific values — and TE §8.1 states the freeze condition in the same row.

**A related fact worth stating, because it is easy to misread.** `evidence.md` records that
`raw_isprint_cache/` holds **isprint text extractions**, not provider `.hdf5` bytes. So the
existing cache does **not** exercise this reader at all, and no inference about the reader's
adequacy can be drawn from twelve months of cached text.

## TS-A-03 — Retrieval resilience is implemented in the approved stack

**Decision (Q1 = A).** The resumable, hash-verified retrieval SEC-A-01 requires is built
from the **already-approved** components — `requests` or the `madrigalWeb` client for
transport, stdlib `hashlib` for verification, stdlib file IO for the incomplete-marker
discipline. **No retry library is added.**

**Why no retry library.** A backoff package would be a new dependency, a §10.1 reuse-register
entry, and a version to pin on two platforms — for a bounded retry loop that is a dozen
lines. The cost/benefit is the same one TS-G-01 records for `governance-guards`' AST walk.

**What must be recorded, not chosen here.** The retry count, backoff schedule and timeout are
**operational values** and are **owed at stage 3.5**, with the constraint that they appear in
the **run record** so a retrieval's behaviour is reconstructible. They are **not** scientific
constants, so TE §18.2's freeze-gate rule does not attach — but §12/TC-03e still applies to
anything that turns out to be one.

## TS-A-04 — Notebook and script are one behaviour, within a declared scope

**Requirement (R-38, W-8, TE §14).** The acquisition notebook and the stage script are
**behaviourally equivalent within a declared scope**, and the notebook **does not hold the
only copy** of parsing, calibration, feature, split, training, evaluation or bootstrap logic.

**Migration obligation, already recorded upstream and restated because it is this unit's
code.** `scripts/audit_ec1_drivers.py` and `scripts/merge_coverage_year.py` move onto the
§12 structure — `--config configs/`, a numbered `NN_verb_noun.py` position — and the
triplicated SHA-256 helper consolidates into `src/data/release.py`. The notebook's inline
station coordinates and its coordinate-to-cell rule are **§18.2 forbidden-choice items** and
must be **frozen under a D-number before** they move, so the migration cannot silently change
a scientific value.

**The acquisition notebook is deliberately excluded** from REQ-ENG-12's import-from-`src/`
and no-only-copy rules and is governed by **REQ-ENG-13** instead — stated because the two
notebook regimes are easy to conflate.

## TS-A-05 — Platform posture

Unchanged from `foundation`: **exactly two platforms**; **CPU is a complete execution path**;
outputs under `/kaggle/working`; artifacts moving between platforms move **with a SHA-256
manifest** and the transfer is recorded.

**Specific to this unit.** Kaggle is the **Phase 1 acquisition/audit host** and Internet is
enabled there for the approved acquisition notebook. That makes this the unit where
credential egress into **saved notebook output cells** is a live path rather than a
theoretical one — see SEC-A-03 limb 2.

**Kaggle durability is unmeasured** (`foundation` W-6 step 8's carried dependency). It bears
on this unit because an interrupted retrieval's incomplete-marker must survive the session
that wrote it.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| REQ-ENG-13 | TS-A-04 | TA-16 | `Pending` |
| FR-P1-01-1 | TS-A-01, TS-A-03 | TA-32 | `Pending` |
| FR-P1-01-2 | TS-A-01 (`madrigalWeb_version` recording) | TA-15 | `Pending` |
| FR-P1-01-3 | TS-A-01 | TA-03, TA-15 | `Pending` |
| FR-P1-01-4 | TS-A-02, TS-A-03 | TA-04, TA-15 | `Pending` |
| FR-P1-01-6 | TS-A-01 | TA-08 | `Pending` |
| NFR-SEC-01 | TS-A-05 (the notebook-output egress path) | TA-22 | **not claimed** |

**Derived and printed**: 5 decision sections (TS-A-01…TS-A-05); **7** coverage rows — six
fewer than `security-requirements.md`'s thirteen, because FR-P1-00-1, FR-P1-00-2,
FR-P1-01-5, FR-P1-01-7, NFR-AUD-01 and NFR-DQ-01 raise **no technology choice**; **0** rows
claimed satisfied; **0** new dependencies; **2** components recorded as **conditional and
unapproved** (`madrigalWeb` on D-144; the HDF5/netCDF reader on the schema audit).

## Assumptions & Open Questions

- **[Q1]** Retry parameters are **owed at stage 3.5** and recorded in the run record; they are not chosen here.
- **[Q2]** The re-run contract needs both hashes and both provider suffixes retained. **For 2022-04, 2022-07 and 2022-12 the original suffixes were never recorded**, so a divergence on those three months will be **uninterpretable no matter what this requirement does** — stated as a limit, not solved.
- **Open, and not this stage's — `madrigalWeb` awaits D-144.** If refused, TS-A-01 returns for re-decision.
- **Open, and not this stage's — the prepared-product reader awaits the schema audit.** Recording `h5py` now would fix a dependency on an unaudited format.
- **Carried — Kaggle's durability semantics are unmeasured**, and an interrupted retrieval's incomplete marker depends on them.
- **Carried — `foundation`'s TensorFlow pin stays `TBD — freeze gate`.** This unit's stack contains no unfrozen pin of its own.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row, install or test as discharged.
