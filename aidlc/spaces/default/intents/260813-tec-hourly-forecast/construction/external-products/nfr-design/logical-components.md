# Logical Components — `external-products`

**Unit** `external-products` (Bolt 5) · **Kind** `library` · **Stage** `nfr-design`

> **Re-saved 2026-09-02 after the owner-directed redo.** This artifact **did change**: E-1's
> DISC-E-1 box now carries the two-limb vacuity predicate over the **allowlist complement**
> and the precedence rule (a detected reachability path fails regardless of either limb), the
> §18.3 dependency is attributed to `foundation`'s FR-WS-7 and routed to the gate, and the
> announce-itself claim is narrowed at § The boundary criterion as well as § Failure domains.
> See `security-design.md` § Remediation of the TERMINAL-pass findings.
>
> **Revised again 2026-09-02 under a SECOND owner-directed redo.** E-1's limb-1 mechanism
> cell and its DISC-E-1 box now state the **candidate-importer set as the allowlist's
> complement**, defined once in `security-design.md` § SD-E-01 and **never enumerated** —
> closing the gap where the limb counted modules the walk never opened.
>
> **Revised a THIRD time 2026-09-02** after the sixth pass found the enumeration gone but the
> **domain** narrowed in its place. The domain now spans **`.py` files and `.ipynb` code
> cells**; the **walk includes `__init__.py`** while only the cardinality count subtracts it;
> **`tests/*` is NOT allowlisted**; and the unresolvable-intermediate rule is **inside** the
> ordered switch, ranked below a found path — this box carries all four, having diverged from
> its sibling twice before.
>
> **Revised a FOURTH time 2026-09-02** under a third owner-directed redo. The seventh pass
> confirmed this box **no longer diverges from its sibling** — the first pass in seven where
> that check held — and found the remaining defect in the **workspace claim**: DISC-E-1 still
> said the candidate set was empty and limb 1 *"cannot fail today"*. **Derived and printed
> instead: 18 files walked, 12 counted; only the target limb is empty**, so limb 1 is **live**
> and reports `skipped` over 18 files. The `__init__.py` sizes are corrected, `src/evaluation/`
> is removed from that list as allowlisted, the matrix discrepancy is routed with an owner,
> and the payload schema matches its sibling field for field.

> ## ⚠ NONE OF THESE COMPONENTS EXISTS, AND ONE OF THEM HAS NO TEST
>
> `src/external/iri.py`, `gim.py` and `spaceweather.py` do not exist — `src/external/` holds
> `__init__.py` only. Neither does `scripts/04_build_external_products.py`, nor `configs/`.
> **R-55's boundary contract for the whole package is an amendment owed.**
>
> **`tests/test_iri_denial.py` does not exist either.** `nfr-requirements` records it as
> *"written but UNEXECUTED"*; it is **unwritten**. E-1's entire reason for being has no
> negative control — see `security-design.md` § SD-E-00.
>
> **This is a logical decomposition, not an infrastructure deployment.** No services, no
> processes, no network boundaries. `external-products` is a **library of three product
> families plus one stage script plus its tests**, and its "failure domains" are the blast
> radii of function calls in one process.
>
> **IRI generation is blocked** on R-59's unrun validation. **FR-P1-04-18's interpolation rule
> is UNSET** (§18.2 Student, Q-15) and comparator generation refuses while it stands. The
> **`gim_network_overlap_flag` audit has not run**. **G-09 is signed (D-31) with preconditions
> UNMET**; the §18.3 preflight has never run; the Python interpreter present is **3.14.7, off
> the governed 3.11 pin**.

## Sources

- `security-design.md` — **SD-E-00** … **SD-E-07**, this stage's sibling artifact. The boundaries below are where those decisions land, and § SD-E-00 carries the workspace evidence and DISC-E-1.
- `../nfr-requirements/security-requirements.md` — **SEC-E-01** … **SEC-E-05** as the requirement set; **three status claims superseded**, per § SD-E-00.
- `../nfr-requirements/tech-stack-decisions.md` — **TS-E-01** … **TS-E-05**.
- `../functional-design/business-logic-model.md` — **W-1** … **W-10**; `../functional-design/business-rules.md` — **R-54** … **R-63**.
- **`performance-requirements.md`, `scalability-requirements.md` and `reliability-requirements.md` are absent by `produces_kinds` design** for a `library` unit; assessed in `security-design.md` § Scope note.
- `../../foundation/nfr-design/logical-components.md`, `../../governance-guards/nfr-design/logical-components.md`, `../../inventory-and-registry/nfr-design/logical-components.md` — the three sibling decompositions and their stated criteria.
- **The workspace, read 2026-09-02** — `src/` (six packages, one populated), `src/data/config.py`, `scripts/audit_ec1_drivers.py`, `tests/` (six modules).
- `../../../inception/application-design/component-dependency.md`, `components.md`, `component-methods.md`, `services.md`.
- `../../../inception/requirements-analysis/requirements.md` — **FR-P1-04-1**, **-3**, **-4**, **-9**, **-15**, **-17**, **-18**; **REQ-ENG-9**; **NFR-IRI-01**, **NFR-LEAK-01**, **NFR-REP-01**.
- `nfr-design-questions.md` — **Q4 = A**, and the receipted Consolidated Summary Confirmation.

---

## The boundary criterion (Q4 = A)

**The boundary is drawn on what each component keeps out.**

> **Everything in this unit is a boundary against something getting in, and the three things
> are unrelated to one another.**

- **E-1** keeps **IRI and GIM** out of training and inference.
- **E-2** keeps **the future** out of a forecast origin.
- **E-3** keeps an **unvalidated benchmark** and an **unaudited-independence comparator** out
  of the comparison.

Each has a different adversary — a **module graph**, a **clock**, and a **gate** — and
therefore a different mechanism, a different failure mode, and a different blast radius. The
useful question about a boundary is what is on the other side of it, and that is the question
this decomposition answers.

**Consistency with the three siblings, without copying any of them.** `foundation` drew on
**failure consequence**; `governance-guards` on **enforcement timing**; `inventory-and-registry`
on **how the failure reaches a human**. Each picked the axis its own material actually varies
on. This unit's material varies weakly on all three and sharply on **what is being
excluded**. Same discipline, different axis.

**Precisely how weakly, since this is the sentence that dismisses the other axes** *(corrected
2026-09-02 on terminal finding 2, Major — the first issue read "every component here fails
silently and none of them raises at a human", which § Failure domains had already narrowed and
which is false as written)*: **every component's BOUNDARY failure is silent**, and **E-2
additionally carries one loud path** — its input-integrity tier, where a hash mismatch
terminates non-zero and names the file and the violated expectation. So
`inventory-and-registry`'s *how-the-failure-reaches-a-human* axis would yield **two** boxes
here, not zero. **The rejection therefore does not rest on "barely varies"**; it rests on the
ground § Failure domains gives — those two boxes would split E-2's hash check from E-2's own
leakage rules, grouping it with nothing it shares a purpose with.

**Why not "by workflow grouping"** (W-3/W-4/W-5 | W-6/W-7 | W-8/W-9). Traceable straight back
to `functional-design` and easy to verify. It groups **W-9** (Dst's three restrictions) with
**W-8** (an exit-code gap) purely by adjacency, and separates W-9 from W-4/W-5 despite Dst's
restrictions being the same class of forecast-safety rule as the lags.

**Why not "by module"** (`iri.py` / `gim.py` / `spaceweather.py`). It matches `src/external/`'s
own structure and would be the easiest to check against the tree — except that **none of the
three exists**. It is a module listing rather than a decomposition, rejected on that ground by
all three siblings, and the import allowlist would have to be split across all three boxes
because it is a property of the **graph**, not of a module.

**Why not "by enforcement mechanism"** (static scan / property test / gate).
`governance-guards` made this work, so the precedent is real. Here it would **split the F10.7
trailing-mean property test from the carry-forward bound and the lag assertions**, which are
one rule about time enforced three ways — the same conflation `governance-guards` itself
rejected when it declined to group a static scan with a run-time assertion.

**Two things cross all three components and are placed explicitly rather than left implicit**
(the cost Q4's own impact line named):

- **W-8's exit-code closure** is a property of **every manifest this unit writes**, not of one
  product family. It is stated once in **E-2**, whose manifest carries the reanalysed-value
  fields, and **named as crossing** in E-1 and E-3 rather than duplicated.
- **W-10's build boundary** — what Bolt 5 may build before G-09 — binds all three identically
  and is stated once in § Failure domains.

---

## Component inventory

| # | Component | Contents | What it keeps out | Adversary | State on disk |
|---|---|---|---|---|---|
| **E-1** | **Containment** | the transitive import-reachability scan and its two disclosed gaps (W-3); the feature-matrix content assertion with its flipped provenance default (SD-E-03) | **IRI and GIM**, out of training and inference | a **module graph** | **Unbuilt**, and its **test is unwritten** |
| **E-2** | **Forecast safety** | the trailing F10.7 mean proven as a property (W-4); driver alignment onto the hourly grid (W-5); lags, carry-forward bound, release grades, never-backfill (W-9, SEC-E-04); the manifest and its reanalysed-value fields (W-8) | **the future**, out of a forecast origin | a **clock** | **Unbuilt**; one predecessor script exists with its gap open |
| **E-3** | **Benchmark and comparator integrity** | the IRI validation gate and its four limbs (W-6); the GIM comparator's four obligations (W-7); the byte-identical-or-divergent contract (SD-E-07) | an **unvalidated benchmark** and an **unaudited-independence comparator**, out of the comparison | a **gate** | **Unbuilt**; both gates **blocked** |

### E-1 — Containment (keeps IRI and GIM out of the model)

**Blast radius: the confirmatory result itself.** A containment failure does not corrupt a
file or stop a run — it makes the model's reported skill partly a restatement of the benchmark
it is being compared against. Vision §7.1 calls the rule **binding architectural**, and TE
§18.3 names IRI-free denial among its **ten critical items**.

**Two limbs, neither substituting for the other.**

| Limb | Question it answers | Mechanism | Built? |
|---|---|---|---|
| **1 — the module graph** | Can anything outside the allowlist **reach** `iri` or `gim`, directly or transitively? | stdlib `ast` reachability over **the candidate-importer set** — the allowlist's complement, defined once in `security-design.md` § SD-E-01, spanning **`.py` files and `.ipynb` code cells** and including `__init__.py`. **Static check authoritative** for this unit | **Unbuilt.** When built it is **live today**, not inert: the target limb is empty and the risk-surface limb is populated, so it reaches **clause 4** and reports **`skipped` over the 18 files it walks**. See DISC-E-1 below |
| **2 — the data** | Does any column reaching training or inference carry an IRI value? | content assertion at the feature-matrix boundary, admitting a column only if its provenance is **present and not IRI** | **No.** Its surface is `features-and-splits`', and **this unit's half of the contract is now larger** |

> **⚠ DISC-E-1 lives in this component, and it is why E-1 exists as its own box.** Every module
> limb 1 protects (`iri.py`, `gim.py`) is **absent**, so a reachability scan under the
> pre-design specification finds nothing to reach and returns **pass** having verified
> nothing — and a vacuous pass satisfies TE §18.3's *"no failing critical test"* in full.
>
> **⚠ But the candidate-importer set is NOT empty, and saying it was was a defect**
> *(corrected 2026-09-02 on the second-redo terminal pass's finding 1, Critical)*. The
> superseded text claimed **two independent causes of vacuity**; **only one is real**. Derived
> under this design's own definition and printed: **the target limb is EMPTY; the
> risk-surface limb is POPULATED at 18 files walked, 12 counted** — the notebook, both
> `scripts/` modules, `src/__init__.py`, four `src/data/` modules, four package `__init__.py`
> files, and the six `tests/` modules, with `src/evaluation/` excluded because it is
> **allowlisted**, not because it is empty. **So the check is live, not inert**: under the
> ordered switch it reaches **clause 4** and reports **`skipped`, naming the target limb**,
> over 18 files it really would inspect.
>
> § SD-E-01's design is that the check reports **`skipped`, never `passed`**, under a
> **two-limb vacuity predicate** with an **ordered outcome switch**. The limbs:
>
> | Limb | Populated when |
> |---|---|
> | **Target side** | at least one of `src/external/iri.py`, `src/external/gim.py` exists |
> | **Risk-surface side** | the **candidate-importer set is non-empty**. That set is **the complement of the allowlist**, defined once in `security-design.md` § SD-E-01 and **never enumerated**: everything in the repository that can execute Python — **`.py` files and the code cells of `.ipynb` notebooks** — except the **two** allowlisted paths, `scripts/04_build_external_products.py` and anything under `src/evaluation/`. **`tests/*` is NOT allowlisted**; `component-dependency.md`:34's blanket row is routed to the gate as a discrepancy, contradicted at `:38` by that artifact's own *"exactly two importers"*. |
>
> **Precedence, because a condition without one is not a control:**
>
> 1. **The scan found a reachability path → `failed`**, regardless of either limb **and
>    regardless of any unresolved edge elsewhere in the graph**.
> 2. No path found, but the walk hit **an unresolved edge** → `skipped`, edge recorded.
> 3. No path, no unresolved edge, both limbs populated → `passed`.
> 4. No path, no unresolved edge, either limb empty → `skipped`, naming which.
>
> **A third-party or stdlib import is not an edge in this graph and is NOT an unresolved
> edge.** The graph is **first-party only**; an import naming a module outside this repository
> — `pytest`, `pandas`, `numpy`, `pyyaml`, the stdlib — is not walked and not recorded.
> **Without this, all six `tests/` modules importing `pytest` would land the scan on clause 2
> rather than clause 4**, making the liveness claim wrong in exactly the clean CPU environment
> TE §13.2 governs. An unresolved edge is only a **first-party** import naming a repository
> module that does not exist. *(Added 2026-09-02, third-redo finding 2, Major.)*
>
> **Clause 1 outranks clause 2 explicitly**: a found path is a fact, an unresolved edge is an
> absence of information, and an absence never outranks a fact. An unresolvable intermediate
> — `a.py` imports `b`, `b` does not exist, so `a → b → gim` cannot be walked — yields
> **`skipped`, not `passed`**, on the same reasoning as an empty limb, because a partly-built
> tree is full of unresolvable intermediates and treating them as clean would restore the
> vacuous pass by a third route. This is the transitive-walk counterpart of R-27's rule that
> an unparseable file is a failure rather than a file importing nothing.
>
> **The walked set and the counted set differ in exactly one stated way.** The walk covers
> the candidate-importer set **entire, `__init__.py` files included**; the risk-surface
> limb's cardinality count subtracts `__init__.py`, so an otherwise-empty package does not
> read as a populated risk surface. **The walk is a strict superset of the count** — which
> matters on today's tree, where **`src/features/`, `src/models/`, `src/gnss/` and
> `src/external/` each hold only their `__init__.py`** (24, 22, 20 and 24 bytes by `wc -c`),
> so the one file an `src/features` → `iri` import could be written in is the file the count
> subtracts. *(Sizes corrected and `src/evaluation/` removed from this list 2026-09-02,
> terminal finding 3: it is **allowlisted**, so it is not a candidate at all.)*
>
> **One payload schema, carried by every outcome** *(field list unified across both artifacts
> 2026-09-02, terminal Minor — the two had listed different subsets and neither was the
> union)*: the **candidate-importer set actually walked, by count and by module path**; **any
> unresolved edges**; and, on a skip, **the identifier of the empty limb**. `failed`,
> `passed` and `skipped` all carry it; the empty-limb field is populated only where it
> applies.
>
> **⚠ Corrected TWICE, and the second correction is why this box is worth reading closely.**
> *(a) 2026-09-02, iteration-1 finding 1, Critical:* the first issue carried the **target limb
> only** and so reproduced the defect it was written to fix — W-10 permits *"module structure,
> interfaces, placeholder CLI definitions"* before G-09, so `iri.py` and `gim.py` may exist as
> **stubs** while other trees hold only `__init__.py`, and a one-limb predicate then lets the
> scan walk `src/data`'s three real modules, find nothing, and report **`passed`**.
> *(b) 2026-09-02, terminal finding 1, Critical, and post-redo finding 1, Critical:* that
> repair scoped the risk surface to **`src/features/` and `src/models/`**, which
> `requirements.md`:370 contradicts in terms — the boundary is *"an **allowlist, not a
> denylist**… an import from `src/data/`, `src/gnss/`, **a training script or a notebook**
> violates it exactly as an import from `src/features/` or `src/models/` does"*. Paired with
> an unconditional *"otherwise it skips"*, a violation **detected** in `src/data/` would have
> reported `skipped`. **The post-redo pass found that repair applied in `security-design.md`
> and NOT here**, in this very box — the site the terminal finding had named. Both halves now
> stand in both artifacts.
>
> **The preflight that consumes the skip is NOT this unit's.** `requirements.md` **FR-WS-7**
> already carries the §18.3 criterion with the **ten critical tests enumerated** and
> **IRI-free denial** among them, and `components.md:63` assigns FR-WS-7 to `config.py` —
> `foundation`'s module. A skip is not a pass, so it fails FR-WS-7 by definition. **What is
> owed is that `foundation`'s assertion reads the structured reason rather than counting
> non-failures**, and that dependency is **routed to the gate**, not assumed. *(Corrected
> 2026-09-02 on adversarial finding 2, Major: the first issue called the coupling "the
> design", cited no owner and routed nothing.)*

**Why limb 1 is static-authoritative here while `governance-guards`' phase boundary is
run-time-authoritative.** A module graph is a property of the **source tree**; a loaded module
is a property of a **running process**. W-3 argues this in its own terms, and the asymmetry is
stated rather than left to read as an oversight.

**What limb 1 cannot see, carried unchanged.** A **dynamic import** —
`importlib.import_module`, `__import__`, or a module path assembled from a string — is
invisible to an `ast` walk. Two partial controls: a **grep-class visibility check** outside the
allowlist, and any hit treated as a **review item** rather than an automatic pass. **Residual,
uncovered:** a dynamic import whose target is computed at run time and whose call site uses
neither name. A run-time caller check inside `iri.py` and `gim.py` was **declined**, because it
would make the two guarded modules aware of three sibling units' paths.

> **⚠ The residual that survives BOTH limbs is narrowed here, not closed.** Flipping the
> provenance default closes the **stripping** act: a laundered value must **forge** a stamp
> rather than delete one. A value **renamed and recomputed from scratch**, carrying a
> fabricated provenance, still survives. **No artifact may describe NFR-IRI-01 as fully
> enforced.**

**`src/evaluation/` is owned by three units** — `evaluation-and-comparison`,
`statistical-inference`, `regimes-diagnostics-reporting`. The allowlist grants an authorized
**path**, never a whole unit's unrelated code.

### E-2 — Forecast safety (keeps the future out of a forecast origin)

**Blast radius: every result, and it is *"invisible in validation, fatal on discovery"*** —
the artifact's own words about backfilled drivers. This is the component whose failures pass
every downstream check. A centered F10.7 mean produces a **smoother, entirely plausible
series**; a driver backfilled from final archived values **satisfies its stated lag**; both
surface as unexplained optimism against a benchmark, or not at all.

**One rule about time, enforced several ways — which is why they share a box.**

| Rule | Control |
|---|---|
| F10.7 81-day mean is **trailing**, ending at the safe-lagged day | **A property test, not a code review**: shift the input, assert the output shifts with it — catching a centered variant *regardless of which API produced it*. A centered mean **is a defect, not a fallback** |
| Missing driver value carries forward **≤ 3 h**, then the row is **excluded** | An **injected four-hour gap** must produce an exclusion |
| Every predictor lagged to its **actual availability timestamp** — Kp/ap3 ≥ 3 h, Hp60/ap60 ≥ 1 h, F10.7 previous-day observed | Assertion against the frozen availability matrix (`features-and-splits`' artifact) |
| Driver series are **time-indexed only** — one value per epoch, identical across all three cells | Schema assertion; **a station performance difference is never attributed to local forcing the dataset does not contain** |
| **Dst's three restrictions kept apart** — diagnostic/hindcast-only; grades never mixed, 2022 grade recorded before use; eligibility a property of **the data** | Three separate results, not one |
| **Never backfill from future final or definitive archived values** | **Record the release status of every driver, not only its lag** |
| **No imputation for the F10.7 outage window** until the measured gap is recorded and governed | — |

**W-8's manifest lives here, and its exit-code closure crosses every component.** The
two-tier posture — a **missing month recorded** as a machine-readable field naming *which*
months; a **hash mismatch terminating** non-zero and naming the file and the violated
expectation — is a property of **every manifest this unit writes**. It is stated once here and
named as crossing in E-1 and E-3.
`scripts/audit_ec1_drivers.py:184`'s unconditional `return 0` is the gap, confirmed open this
session. **Both injections are tested, because they assert opposite outcomes**: a single test
covers half the requirement and lets the other half regress silently.

> **⚠ The reanalysed-value check is BOUNDED, not closed, and this component is where the bound
> lives.** Four fields per series — `release_status`, `retrieval_date`, the full product
> identity **including any version suffix**, `sha256` — asserted for internal consistency **and**
> for the declared status matching the **contemporaneous** grade. Where a file carries no
> provenance column, the sanctioned evidence is **that absence plus an explicit
> unverified-status statement**. **Inferring a grade from silence is not evidence.** F10.7 and
> Dst are **declared-status-only**; substantive detection is specified only for the two
> **unretrieved** GFZ series. **No artifact may report this as closed.**

> **⚠ `carry_forward_composition` is a G-04 freeze item and is `TBD`.** No rule states what a
> **3-hour** bound means on a **24-hour** step, and the two readings differ by **20 of 24
> scored rows per affected day, in all three cells**. Availability resolution **raises
> `FeatureAvailabilityError` and stops** until the Student freezes it. **This stage adopts
> neither reading.**

### E-3 — Benchmark and comparator integrity (keeps an unvalidated benchmark out of the comparison)

**Blast radius: what the thesis reports a comparison against.** E-3 computes nothing the model
consumes; it produces the two things the model is **measured against**. A failure here does not
make the model wrong — it makes the measurement meaningless, and in a direction nobody
downstream can detect.

**Both of this component's gates are currently blocked, for different reasons.**

| Gate | Blocked by | Kind of block |
|---|---|---|
| **IRI benchmark generation** | R-59's **pre-declared validation has not run** | A gate that has not been attempted |
| **GIM comparator generation** | FR-P1-04-18's **interpolation rule is UNSET** — §18.2 Student-owned, Q-15 | A gate that **cannot** be attempted until a human decides |

**Three of the IRI gate's four limbs are ordering or content checks, not presence checks —
which is the whole point.** *"A passing report exists"* is satisfiable by a report whose
tolerance was chosen **after** the comparison ran. The **tolerance's timestamp preceding the
comparison** is the only evidence class that separates *declared before* from *fitted after* —
the same mechanism `inventory-and-registry` adopts for retrospective split redesign. Limb 3
asserts the report **field by field** (the pinned build; all switches and the topside option;
the ceiling **stated explicitly as 2000 km**; units and extraction; driver inputs **with
confirmation that none is future-centered or unavailable at target time**; **5–10 samples**
spanning sites, day and night, quiet and disturbed, against the **official IRI interface**;
the predeclared tolerance).

> **⚠ Limb 4 is the one with scientific consequence.** *A benchmark fed better-timed drivers
> than the model gets is not a benchmark.* The benchmark's own drivers must appear in **the
> same frozen availability matrix** used for ML features. **That matrix is
> `features-and-splits`' artifact; this unit states the obligation and does not own the row.**
> This is the one limb whose violation would **flatter** the model rather than break the run.
>
> **⚠ And the convention it leans on carries its own ungranted amendment** *(added 2026-09-02
> on adversarial finding 4, Major)*. Where a provider supplies no publication timestamp — which
> is the case for **F10.7**, the one series D-25 exists to govern — limb 4 admits the
> conservative convention plus a documented absence. `evidence/DECISIONS.md:1854` records that
> D-25 **"Requests, but does not take, a §15.2 amendment to TE §7.0A stage 4 and EV-12; until
> granted, EV-12's F10.7 limb is unmet at G-04."** `:1648` lists that request among the open
> holes leaving §18.3's first precondition only **partially met**. The relaxation of
> FR-P1-04-15's plain *"publication timestamp"* requirement therefore rests on a route that is
> **not yet closed**, and nothing here treats it as granted.

**On validation failure the implementation is NOT silently switched.** A switch made because
the first implementation failed validation is a scientific change wearing an operational
disguise.

**The GIM comparator's four obligations, with one blocked, one partial and one residual.**
Obligation 2's hand-check **timestamp must precede** generation. Obligation 3's
map-product-to-map-product statement, and the **spatial-representativeness mismatch**, are
**emitted by the reporting path itself** rather than left to a writer. Obligation 4 is a
**grep-class check** over `gim.py` plus a report statement citing the overlap audit, with
**⛔ the residual** — tuning done **outside** `gim.py` and pasted in as a constant — reached by
no check.

> **⚠ Obligation 1's refusal is a mitigation that EXPIRES.** The moment Q-15 is decided, the
> refusal stops covering obligation 4's disclosure. The overlap-disclosure control therefore
> keys to **a GIM comparison artifact existing**, not to the refusal standing.

**The `gim_network_overlap_flag` result is disclosed once the audit runs, and no independence
claim precedes it.** Disclosure is **mandatory**, not conditional on the result being
favourable. **The audit has not run.**

**SD-E-07's byte-identical-or-explicitly-divergent contract is stated in E-3 and crosses into
E-2**, because both product families are fetched. It matters most here: a re-issued CODE final
GIM day that silently replaced the old one would **change a published number with no trace**.

---

## Failure domains and blast radius

| Component | Failure announces itself? | Blast radius | Contained by |
|---|---|---|---|
| **E-1** | **No** — nothing raises; the result is simply optimistic | The **confirmatory result**: reported skill partly restates the benchmark | Two limbs, **both unbuilt**. Limb 1 is **live but incomplete today** — its target limb is empty, so it reports `skipped` over the **18 files it walks** rather than failing. **Its negative control is unwritten**: `tests/test_iri_denial.py` does not exist |
| **E-2** | **Not for its boundary property** — *"invisible in validation, fatal on discovery"*. Its **input-integrity tier is loud**: a hash mismatch terminates non-zero. That is a fact about a file, not about whether the future leaked | **Every result**, and a defect can survive to the thesis | Property tests and injected-gap controls, **all unbuilt**; one predecessor script with its exit-code gap **open** |
| **E-3** | **No** — a meaningless measurement looks like a measurement | **What the thesis reports a comparison against** | Two gates, **both blocked** — one unattempted, one awaiting a human decision |

**No component's CHARACTERISTIC failure announces itself, and that is the finding.**

> **⚠ CORRECTED 2026-09-02 on adversarial finding 3, Major.** The first issue read *"Not one
> of the three announces itself… **This unit has none**"* — contradicted three times by this
> artifact's own text, because **E-2's hash-mismatch tier terminates non-zero, naming the file
> and the violated expectation**, which is exactly the raise-and-stop class the sentence
> invoked as the sibling contrast. The claim is narrowed below rather than dropped, and Q4's
> rejection rationale is corrected with it.

The distinction the corrected claim rests on: **E-2's one loud path is an integrity check on
its INPUTS, not on the boundary the component exists to hold.** A hash mismatch says a file is
not the file it claims to be — a fact about provenance that any consumer of that file would
want. **It says nothing about whether the future leaked into a forecast origin**, which is
what E-2 is for, and a centered mean or a backfilled driver passes every hash check ever
written. So the unit does contain one raise-and-stop path, and **not one of the three boundary
properties has one**.

**What this changes in Q4's reasoning, stated rather than left standing.** The rejection of
the *how-the-failure-surfaces* axis was argued as *"it would have produced one box"*. That
argument is **too strong** and is withdrawn: E-2's integrity tier would have gone in a
second box, so the axis yields two, not one. **The rejection stands on the narrower ground**
that those two boxes would separate E-2's hash check from E-2's own leakage rules while
grouping it with nothing it shares a purpose with — splitting a component by the loudness of
its failures rather than by what it is for.

The three siblings each had a component whose **boundary property** raises: `foundation`'s bad
read, `governance-guards`' run-time guards, `inventory-and-registry`'s build-time integrity.
**On that comparison this unit still has none**, which is why the decomposition is drawn on
*what is kept out*.

**W-10's build boundary binds all three identically.** Permitted before G-09: module structure,
interfaces, placeholder CLI definitions, configuration wiring, safe fail-fast behaviour, and
this unit's `tests/` scaffolding. Barred until G-09 is signed for the affected component:
implementing any component whose P0 decision is unresolved; **filling any `TBD — freeze gate`
field**; executing any governed run; generating code for a unit carrying an open blocker on
that scope.

## Shared resources

| Resource | Owner | Used by | Note |
|---|---|---|---|
| `src/data/config.py` — `IntegrityError` and the hierarchy | `foundation` (R-01); declaration site ruled 2026-08-28 | E-1, E-2, E-3 | **Five exceptions this unit needs are absent**, against `__all__`'s 17 names. Q2 covered **two**; `BenchmarkError` and `ComparatorError` are routed to the gate with a proposed disposition, and **`DriverError` with none** — its raise-conditions are self-contradictory upstream (carried **Finding 9**) |
| `AlignmentError` | `foundation`, already declared | E-2 | **Already exists** and already means *"a driver series did not align onto the hourly grid"* — this unit's own W-5 condition. **Not** in the missing set |
| The **frozen availability matrix** | `features-and-splits` | E-2 (ML feature lags), **E-3 (limb 4, the benchmark's own drivers)** | **Obligation stated, row not owned.** E-3's fairness depends on an artifact this unit does not write |
| The **feature matrix** and its provenance column | `features-and-splits` | E-1 (limb 2) | **A two-half contract whose other half has not been stated**, and SD-E-03 **enlarges this unit's half** to every column rather than `iri_*`-named ones |
| `component-methods.md`'s boundary blocks | `application-design` | E-1, E-2, E-3 | **`src/external` has no block for any of its three modules.** One amendment owed (R-55), part of **five across three units** |
| `configs/features.yaml` — `carry_forward_composition` | this unit writes into it; `foundation` owns the config contract | E-2 | **`configs/` does not exist**, and the field is a **G-04 freeze item**, `TBD`. Availability resolution raises and stops |
| `tests/test_phase_boundary.py`'s `_imported_modules` | `governance-guards` | E-1 | Reused as a **primitive**. **NFR-PHASE-01 is not weakened and no coverage of it is claimed** |

---

## Requirement coverage

| Requirement | Component | Acceptance row | Row primary owner | Status |
|---|---|---|---|---|
| **REQ-ENG-9** | E-2 | ⚠ **NO ACCEPTANCE ROW** | — | untested |
| FR-P1-04-3 | E-2 | **WS-11** *(row restored 2026-09-02 on adversarial finding 5, Minor)*; R-57a's injected-four-hour-gap control is the mechanism, not the row | `features-and-splits` | `Pending` |
| **FR-P1-04-4** | E-2 | ⚠ **NO ACCEPTANCE ROW** | — | untested |
| FR-P1-04-9 | E-3 | WS-09, TA-12 | **`external-products`** (WS-09); `models-and-baselines` (TA-12) | `Pending` |
| **FR-P1-04-15** | E-3 | ⚠ **NO ACCEPTANCE ROW** | — | untested |
| FR-P1-04-17 | E-2 | **TA-36** | `features-and-splits` | ⚠ **`Pending` — approved, never run** |
| **FR-P1-04-18** | E-3 | ⚠ **NO ACCEPTANCE ROW** | — | untested |
| FR-P1-04-1 | E-1 | WS-10, TA-07 | — | `Pending` — ⚠ **control NOT WRITTEN** |
| NFR-IRI-01 | E-1 | WS-10, TA-07 | — | `Pending` — ⚠ **control NOT WRITTEN** |
| NFR-LEAK-01 | E-1, E-2 | TA-11 | `features-and-splits` | `Pending` |

**Derived and printed.** **3** components (E-1, E-2, E-3). **10** coverage rows, identical in
membership to `security-design.md`'s table — set-differenced in both directions, **empty both
ways**. **4** rows with no acceptance row, counted from the blank acceptance cells above.
**0** rows claimed satisfied. **0** of the three components exist on disk, and **E-1's negative
control is unwritten**.

**Decomposition of `security-design.md`'s 7 design sections across the three components**,
derived rather than asserted: **5** land in exactly one component — SD-E-01 → E-1,
SD-E-03 → E-1, SD-E-04 → E-3, SD-E-05 → E-3, SD-E-06 → E-2 — and **2** are shared:
**SD-E-02** (the exceptions split across all three: `ImportBoundaryError` → E-1,
`FeatureAvailabilityError` → E-2, `BenchmarkError` and `ComparatorError` → E-3) and
**SD-E-07** (byte-identical-or-divergent, across E-2 and E-3). 5 + 2 = 7, matching the sibling
artifact's section count.

> **⚠ ONE EXCEPTION IN SD-E-02's SPLIT LANDS IN NO COMPONENT, AND THAT IS DELIBERATE**
> *(registered 2026-09-02 on adversarial finding 6, Minor — the split named four of the five
> and left `DriverError` unplaced without saying so)*. **`DriverError` is not assigned to
> E-1, E-2 or E-3.** It cannot be: its raise-conditions are self-contradictory upstream under
> the carried **Finding 9** (`domain-entities.md` § 9's cell was annotated without being
> changed, so it *"both is and is not"* the exception `AlignmentError` in fact owns), and
> **which component it belongs to depends on which reading survives** — the alignment reading
> puts it in E-2 beside `AlignmentError`, the grade-and-provenance reading puts it in E-2 as
> well but for a different rule, and neither is decided. **Assigning it now would encode a
> reading this stage has explicitly refused to take**, so it is left unplaced and named here.
> `AlignmentError`, which **already exists**, is placed in E-2 and is unaffected.

**2** subjects are here-only with no `security-design.md`
counterpart: the § Failure domains observation that **no component's CHARACTERISTIC failure
announces itself — every boundary failure here is silent, while E-2 alone carries one loud
input-integrity path** *(narrowed form, 2026-09-02, terminal finding 2)*, and the explicit
placement of the two cross-cutting concerns W-8 and W-10.

**A decomposition that verifies is not evidence the decomposed set is complete.** The 5 / 2 / 2
split is arithmetically sound against `security-design.md` as written; it says nothing about
whether that artifact covers everything it should. The completeness check is the FR-P1-04 set
difference recorded in `security-design.md` § Requirement coverage, and the two answer
different questions.

**Why the other eleven `FR-P1-04-*` IDs are absent.** `requirements.md`'s FR-P1-04 space is
`{1…18}`. This unit carries `{1, 3, 4, 9, 15, 17, 18}`; the set difference is
`{2, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16}` — the **feature contract itself**,
`features-and-splits`' space.

## Assumptions & Open Questions

- **[Q4]** The criterion is **what the component keeps out**. It required placing W-8's exit-code closure and W-10's build boundary explicitly, since both cross all three; both are placed rather than left implicit.
- **[E-1 / DISC-E-1 — what limb 1 does TODAY, derived not asserted]** The **target limb is empty**; the **risk-surface limb is POPULATED — 18 walked, 12 counted**. Limb 1 is **live**: it reaches **clause 4** and reports **`skipped`, naming the target limb**. *(Corrected 2026-09-02, second-redo terminal finding 1, Critical: the superseded bullet claimed "neither its targets nor any potential violator exists — two independent causes". Only one cause is real.)*
- **[E-1 — OPEN, routed to the gate]** **The §18.3 preflight is `foundation`'s row, not this unit's.** `requirements.md` **FR-WS-7** already enumerates the ten critical tests with **IRI-free denial** among them, and `components.md:63` assigns it to `config.py`. A skip fails FR-WS-7 by definition; what is owed is that the assertion **reads the structured skip reason** rather than counting non-failures.
- **[E-1 — the domain, the two sets, and the allowlist]** The candidate-importer set is the complement of TE §12's **two** allowlisted paths over a domain of **`.py` files and `.ipynb` code cells**. The **walk includes `__init__.py`; only the cardinality count subtracts it.** **`tests/*` is NOT allowlisted** — `component-dependency.md`:34's blanket row is routed to the gate as a discrepancy, contradicted at `:38`. *(Corrected 2026-09-02, second-redo findings 1, 2 and 5.)*
- **[E-1 — OPEN, routed to the gate: the `component-dependency.md` blanket row]** `:34`'s `tests/*` row reads `yes` in all seven columns, contradicted at `:38` by *"exactly two importers"*. **This design follows TE §12's two paths; `tests/*` is not allowlisted.** **Owner: the project decision owner.** *(Routed with an owner 2026-09-02, terminal finding 4.)*
- **[E-1 — precedence, and where the intermediate rule sits]** The ordered switch is **four** clauses, not three: a **found path fails regardless of either limb AND regardless of any unresolved edge**; an unresolved edge with no path found yields `skipped`; then the two limb clauses. **Clause 1 outranks clause 2 explicitly** — a found path is a fact, an unresolved edge is an absence, and an absence never outranks a fact. *(Corrected 2026-09-02, second-redo finding 4: the intermediate rule sat outside the switch with its rank unstated.)*
- **[E-3 / D-25 — carried]** **D-25's requested §15.2 amendment is UNGRANTED and EV-12's F10.7 limb is unmet at G-04.** Limb 4's relaxation of FR-P1-04-15's plain *"publication timestamp"* requirement rests on that route, and it is not closed.
- **[Shared resources — `DriverError` is unplaced]** It is assigned to **no** component, because which one it belongs to depends on the reading that carried **Finding 9** leaves unresolved. Assigning it would encode a reading this stage refused to take.
- **[E-1 — the residual is narrowed, not closed]** A value renamed and recomputed from scratch, carrying a fabricated provenance, survives both limbs. **No artifact may describe NFR-IRI-01 as fully enforced.**
- **[E-1 — OPEN, routed to the gate]** SD-E-03 **enlarges this unit's half of a two-half contract whose other half has not been stated**: every feature-matrix column now needs a provenance value, not only `iri_*`-named ones. `features-and-splits` owes where the assertion sits, what it raises, and when it runs.
- **[Shared resources — OPEN, routed to the gate]** **The missing-exception set is five and Q2 named two.** `BenchmarkError` and `ComparatorError` carry a proposed disposition identical to Q2 = A; **`DriverError` carries none**, pending the upstream reconciliation of carried **Finding 9**.
- **[E-2]** **`carry_forward_composition` is a G-04 freeze item**, `TBD`, differing by 20 of 24 scored rows per affected day in all three cells. **This stage adopts neither reading.**
- **[E-2]** The **reanalysed-value check is bounded, not closed** for F10.7 and Dst, both declared-status-only. **No artifact may report it as closed.**
- **[E-3]** **IRI generation is blocked** on R-59's unrun validation; **no IRI benchmark exists**. **FR-P1-04-18's interpolation rule is UNSET** and comparator generation refuses — a refusal that **expires the moment Q-15 is decided**.
- **[E-3]** The **`gim_network_overlap_flag` audit has not run**; no independence claim may precede it, and disclosure is mandatory whatever the result. **Obligation 4's residual** — tuning outside `gim.py` pasted in as a constant — is reached by no check.
- **[E-3]** **Limb 4's availability matrix is `features-and-splits`' artifact.** E-3's fairness guarantee depends on a row this unit does not own.
- **Carried — `src/external` has no contract block for any of its three modules** (R-55). One amendment owed, part of five across three units.
- **Carried — TA-36 is `Pending`**: approved, never run, never cited as a result.
- **Carried — the Python interpreter present is 3.14.7, off the governed 3.11 pin.** Nothing it runs is governed evidence.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, authorises writing a module, or claims a gate, acceptance row or test as discharged.

---

## Re-save note — 2026-09-04

A **fourth** owner-directed redo of `nfr-design`, ordered to repair two Majors in
**`target-standardization`**, cleared every unit's receipts again. **This unit was untouched
by it**; the summary was re-confirmed and the artifact re-saved. **No component, boundary or
status claim above is altered by this note.**
