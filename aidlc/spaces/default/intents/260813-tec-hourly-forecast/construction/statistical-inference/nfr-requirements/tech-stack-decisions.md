# Tech Stack Decisions — `statistical-inference`

**Unit** `statistical-inference` (Bolt 10) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NO NEW DEPENDENCY, AND ONE PIN THAT IS A CORRECTNESS CONTRACT
>
> The governed stack is fixed by **TE §8** and transcribed at
> `../../foundation/nfr-requirements/tech-stack-decisions.md`. This unit adds **none**.
>
> **The RNG pin is not a preference.** `numpy.random.default_rng(seed)` — **PCG64** — is what
> makes *"reproduces exactly from seed 20221201"* mean anything at all. A different generator
> gives different draws from the same seed, and WS-17's replicate hash would be unreproducible
> without changing a single scientific value.
>
> **NO NUMERIC MEMORY CEILING EXISTS IN THE AUTHORITIES.** None is asserted or borrowed here.
> **Neither fixture has run**, so **no bootstrap has ever executed** and every runtime and
> memory figure in this design is a placeholder.
>
> **The interval method is UNCONFIRMED.** **G-09** is signed (D-31) with preconditions UNMET;
> stage 3.1 remains **FAIL**; `configs/` does not exist; no Python interpreter exists here.

## Sources

- `../../foundation/nfr-requirements/tech-stack-decisions.md` — the governed stack and the platform rules. Referenced, not restated.
- `../functional-design/business-rules.md` — **R-114**, **R-115**, **R-117** (the generator pins), **R-118**, **R-119**, **R-120**, **R-122**.
- `../functional-design/business-logic-model.md` — **W-2** (precompute once, resample the precomputed), **W-3** (the block grid and the vector draw), **W-4** (seed and stream discipline), **W-5** (interval construction, method-parametric), **W-6** (the widening guard), **W-8** (the verification plan).
- `../../evaluation-and-comparison/nfr-requirements/tech-stack-decisions.md` — § TS-C-02, which records that unit's obligation **not** to reimplement this bootstrap.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§8.1** (`numpy` required — *"arrays, deterministic numerics, bootstrap implementation"*; `pandas`, `pyarrow`, `pytest` required), **§9.2–9.3**, **§13.5**, **§13.6**, **§13.7** (exact equality), **§15.1** (measured, never invented), **§15.3**, **§18.2**.
- `nfr-requirements-questions.md` — Q1 = B, Q2 = A, and the receipted Consolidated Summary Confirmation.

---

## TS-S-01 — The RNG is pinned by name, and that pin is load-bearing

**Decision (R-117, W-4).** The generator is **`numpy.random.default_rng(seed)` — PCG64**.
Streams are derived by **seed-sequence spawn**: block-index draws consume the **primary**
stream; the **48-hour sensitivity** and the **widening comparator** consume **deterministically
derived child streams**.

**Why this belongs in a tech-stack artifact rather than being an implementation detail.** TE
§8.1 lists `numpy` for *"arrays, deterministic numerics, bootstrap implementation"* and stops
there. **NumPy offers two RNG APIs** — the legacy `RandomState` and the modern `Generator` —
and **they produce different streams from the same seed**. Picking either "naturally" at 3.5
would silently determine whether a recorded replicate hash is reproducible. **The pin removes
that choice from implementation.**

**Child streams are a correctness requirement, not tidiness.** Without them, adding or removing
a sensitivity run **perturbs the primary draws**, and the confirmatory replicate hash changes
for a reason unrelated to the confirmatory computation. Spawn makes each consumer's draws
**independent of whether the others ran**.

**This pin is an engineering contract, not a scientific constant.** The scientific value —
**20221201** — lives in `configs/seeds.yaml`; **the generator name is no more a scientific
constant than the language pin**, and naming it here fills no freeze-gate value.

**A call without `seed` is a `TypeError` by signature** — the never-defaulted rule made
**unrepresentable** rather than checked.

## TS-S-02 — One estimand arithmetic, and the resampling touches indices only

**Decision (R-114, W-2).** The per-pair squared-error differences are **precomputed once** into
a `numpy` array; the bootstrap **resamples indices** into that array. **The replicate loop
contains no estimand arithmetic.**

**Why the shape matters.** A loop that recomputed `benchmark − model` per replicate would be a
**second copy** of the estimand — and the copy inside a 10,000-iteration loop is the one nobody
reads. It could invert the sign, apply **row-weighting** instead of **equal-station
weighting**, or drop a station, and the interval would look normal. **`evaluation-and-comparison`
owns the estimand's orientation and its reversed-sign control; this unit adds no second
definition.**

**Vectorisation is a consequence, not the goal.** Resampling indices into a precomputed array is
also what makes 10,000 replicates tractable on CPU — but the reason it is *required* is
single-definition, not speed.

**No resampling or statistics package is added.** `numpy` supplies the draws; **`scipy.stats` is
not used**, and TS-C-02 records the sibling obligation not to reach for it either. A library
resampler would offer a within-station or naive mode, which `project.md` forbids for producing
**systematically narrower intervals**.

## TS-S-03 — The interval component is parametric, and refuses an unconfirmed method

**Decision (R-119, Q7 = B).** Interval construction is a **named component reading its method
from `experiment.yaml`**. **The percentile method is PROPOSED and routed to the gate** — TE
§13.6 says *"report 95% confidence intervals"* and **names no method**.

**Why the method is a scientific value.** Percentile, basic and BCa **can differ materially** on
10,000 replicates of a skewed statistic, so §18.2 bars an implementer filling it by convenience.
**Nothing here adopts one.**

**What being method-parametric buys.** A BCa ruling at the gate changes **that component, not
the whole unit** — so the architecture does not have to be redesigned around a decision that has
not been taken.

**Negative control (18).** An **unrecognised, absent or unconfirmed** interval-method value →
**refused** (`BootstrapError`, naming the config key). **If implementation is reached with the
method unconfirmed, the posture is TE §18.3's: stop and report.**

**One property the percentile proposal has and the artifact should not lose.** It is **exactly
reproducible from the replicate set alone**, which keeps **WS-17's replicate-hash evidence
sufficient to re-derive the interval**. A method requiring additional state would weaken that
evidence — worth stating because it bears on the gate ruling.

## TS-S-04 — Resource posture: measured, never asserted

**Decision (Q2 = A, TE §9.2, TC-01).** The bootstrap **completes on CPU** within the two
governed platforms. **CPU is a complete execution path, not an emergency mode**; **GPU may be an
optional accelerator only and never a dependency of any result.**

> ### ⛔ NO MEMORY CEILING IS ASSERTED, BORROWED OR INVENTED
>
> **TE §9.3 is a storage budget.** `services.md`'s *"peak memory … against TE §9.3's 10.0 GB
> hard planning envelope"* is a **conflation**, quoted as upstream text and **not adopted**; a
> **change record against `services.md` is owed** and is not this stage's to write.
>
> **The peak-memory figure is to be MEASURED on the fixtures and FROZEN** — TE §15.1: exact
> counts, tolerances and runtimes are **measured from the fixtures and frozen, never invented**.
> **Neither fixture has run.** An implementer therefore has **no memory budget to design
> against today**, and that gap is stated rather than filled with a number the authorities do
> not supply for this purpose.

**The replicate count is a frozen scientific value.** **10,000 cannot be reduced to fit a
resource budget** — a smaller count is a different protocol, and TE §18.2 bars changing a
scientific value for convenience. If measured memory proves intolerable, the response is a
**decision routed to the owner**, not a quiet reduction, and **this artifact pre-authorises
nothing**.

**TE §15.3's reduced-replicate fixture bootstrap is a separate thing**, an **apparatus constant**
in `tests/fixtures/scientific_1month/fixture_manifest.yaml` — **not** a licence to reduce the
confirmatory count. **Its classification is open** (Recommendation 24): apparatus constant, or a
predeclared `experiment.yaml` named run if the owner rules a replicate count is protocol
wherever it appears.

**A design consequence worth naming.** Because memory is unbudgeted and the replicate count is
fixed, the **only** dimension left to an implementer is **how the replicates are held** —
streaming reductions versus materialising a 10,000-row replicate matrix. That is an
implementation choice **constrained by a measurement that does not exist yet**, so 3.5 may find
it must measure before it can choose.

## TS-S-05 — Platform posture

Unchanged from `foundation`: **exactly two platforms**; artifacts move between them **with a
SHA-256 manifest**; the transfer is recorded.

**Specific to this unit.** **The G-06 interval is computed once.** If that run executes inside a
Kaggle session, the **in-Kaggle obligation binds**: the required critical tests and applicable
fixtures must have passed **inside that same session**, because a Kaggle session carries no git
working tree and a local suite run proves nothing about the environment the one-shot computation
actually ran in.

**Determinism across platforms is what the RNG pin buys.** With `default_rng`/PCG64 pinned and
child streams spawned, the replicate hash is **implementation-independent** — *"reproduces
exactly"* stops meaning *"reproduces on the machine that wrote the hash"*, which is precisely
what a two-platform project needs.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| **FR-P1-05-8** | TS-S-01, TS-S-02, TS-S-03, TS-S-04 | **WS-17 (primary)**, TA-13, TA-26 | `Pending` — **no bootstrap has ever been run** |
| **NFR-DET-01** | TS-S-01, TS-S-05 | WS-17 (supporting), TA-13 | `Pending` |
| **NFR-REP-01** | TS-S-01, TS-S-05 | **WS-20, TA-17** | `Pending` — the RNG pin is what makes §13.7 exact equality reachable |

**Derived and printed**: 5 decision sections (TS-S-01…TS-S-05); **3** coverage rows *(corrected 2026-09-01, same finding; superseded: **2**)* — **two
fewer** than `security-requirements.md`'s **five**, because **FR-P1-04-5** (the folds and
embargo, `features-and-splits`') and **NFR-AUD-01** (append-safe records, `foundation`'s rows)
raise **no technology choice in this unit**; **0** rows claimed satisfied; **0** new
dependencies; **0** values left `TBD — freeze gate` by this unit; **1** figure recorded as
**owed as a fixture measurement** (peak memory); **1** scientific value **proposed and
unconfirmed** (the interval method).

## Assumptions & Open Questions

- **[TS-S-01]** The RNG pin is an **engineering contract**, not a scientific constant, and fills no freeze-gate value. **If a future NumPy changes PCG64's stream** the replicate hash changes with it — which is why the **generator identity is recorded in `BootstrapResult`** rather than assumed stable, and why the environment pin and this pin must be read together.
- **[TS-S-03]** **The interval method is unconfirmed.** Percentile is **proposed**; **stage 3.5 must stop and report** if it is reached unconfirmed. The percentile method's exact-reproducibility-from-replicates property is stated because it **bears on the gate ruling**, not to argue for it.
- **[Q2 / TS-S-04]** **No memory ceiling exists in the authorities, and none is adopted.** The figure is **owed as a fixture measurement**, and **neither fixture has run** — so **how the replicates are held is an implementation choice constrained by a measurement that does not exist**.
- **[assumption]** 10,000 replicates over 3 stations × 30 scored days is tractable on CPU within a Kaggle session. **Unmeasured.** If it is not, **the replicate count is not the variable to change** — it is frozen, and the trade is the owner's.
- **Carried — `evaluation-and-comparison` must not reimplement this bootstrap** (its § TS-C-02). That obligation is **stated on both sides**; neither declares it satisfied.
- **Carried — BLK-03, BLK-04, BLK-08 and BLK-09** are inherited exit conditions on this stage; **none is closed here**.
- **Carried — `foundation`'s TensorFlow pin stays `TBD — freeze gate`.** This unit trains nothing and does not wait on it.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row, install or test as discharged.
