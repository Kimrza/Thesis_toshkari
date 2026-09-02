# NFR Requirements — Questions — `statistical-inference`

**Unit** `statistical-inference` (Bolt 10) · **Kind** `library` · **Stage** `nfr-requirements`

Two artifacts only — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit.

**This unit's `functional-design` is unusually complete, and most of what an NFR stage would
normally ask is already answered there.** Not re-asked: the bootstrap as a **metric entry point
in full** (R-113, W-1); **one copy of the estimand arithmetic** — precompute once, resample the
precomputed (R-114, W-2); the **fixed non-overlapping block grid** and what a boundary
violation raises (R-115, W-3); the **vector property** and the declared rule for missing pairs
(R-116); **seed sourcing and generator identity** — `default_rng(seed)` **(PCG64)**, block-index
draws the only consumer of the primary stream, child streams by seed-sequence spawn, the
replicate hash emitted by the producing path, and a call without `seed` a **`TypeError` by
signature** (R-117, W-4, Q5 = C); the frozen numbers in config with the signature amendment
**proposed not applied** (R-118); the **method-parametric** interval construction with the
**percentile method PROPOSED and routed to the gate** (R-119, Q7 = B); the **widening guard**
(R-120, W-6); the **cross-station paired-error correlation** defined and emitted by the
producing path (R-121, W-7); `tests/test_bootstrap.py`'s **eight checks** (R-122, W-8).

**Carried, not decided here.** The **interval method is unconfirmed** — percentile is
**proposed**, and if implementation is reached with it unconfirmed the posture is TE §18.3's:
**stop and report rather than choose a default**.

---

## Question 1

R-120's widening guard uses the **rejected** within-station method as a yardstick: the vector
time-block bootstrap should produce **wider** intervals, because that is the whole reason
`project.md` forbids the within-station variant — *"it produces systematically narrower
intervals"*.

The guard's **raise lands at fixture time**. On **real data**, R-120 makes the comparison a
**mandatory disclosure** — it is reported, not enforced.

So if, on the real December data, the vector bootstrap turns out **not** wider than the
rejected method, the result is disclosed and the run proceeds. But that outcome has only two
explanations: **the implementation is wrong**, or **the assumption behind rejecting
within-station does not hold for this dataset**. Either would matter to the reported interval.

What should `security-requirements.md` require?

A. **Disclosure, as designed** — the comparison is reported at G-06 and in the results, and the run proceeds
   > **Impact**: Matches R-120 exactly and adds nothing this stage would be inventing. It lets a confidence interval that may be too narrow reach the thesis with a disclosure attached, and this project has already recorded how far a caveat travels compared with the number it qualifies.

B. **Disclosure plus a required adjudication** — the run proceeds, but a non-widening outcome is a **named G-06 item the supervisor must rule on** before the interval is reported as confirmatory
   > **Impact**: Keeps the design's disclosure and adds a decision point at the gate that already exists, so the outcome cannot pass as routine. It puts one more item in front of the supervisor, and the ruling would rest on a comparison against a method the project rejected.

C. **Block** — a non-widening outcome on real data halts the confirmatory interval until resolved
   > **Impact**: Treats the anomaly as an integrity failure rather than an observation. The comparator is **exact and quarantined** precisely so it is not load-bearing, and making a rejected method's output a blocking condition inverts that — the yardstick would become the authority.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B — the outcome is diagnostic of either a bug or a broken assumption, and both deserve a human ruling before the interval is called confirmatory; but the comparator is deliberately quarantined and must not become the thing that decides. Option A's weakness is the one this project has already lived: a disclosure attached to a number travels less far than the number. Option C would let a rejected method block the accepted one.

[Answer]: B

---

## Question 2

This unit runs the project's heaviest computation: **10,000 replicates** over 24-hour blocks
carrying **all three stations together**, plus the **48-hour sensitivity** and the **widening
comparator** as child streams.

`services.md` states, and this unit's own artifacts quote as **upstream text rather than
adopting it**, that *"peak memory, not cumulative runtime, is the binding quantity against TE
§9.3's 10.0 GB hard planning envelope"*. That framing was ruled a **conflation**: **TE §9.3 is
a storage budget**, and **no numeric memory ceiling exists in the authorities at all**. A change
record against `services.md` is owed and is not this stage's to write.

So this unit must state a resource posture with **no governing number to state it against**.

What should the artifacts require?

A. State the constraint as **CPU-completeness only** — the bootstrap must complete on CPU within the two governed platforms — and record explicitly that **no numeric memory ceiling exists in the authorities**, with the `services.md` conflation named as an owed change record
   > **Impact**: Says exactly what the authorities support and nothing more, and keeps the owed correction visible instead of quietly inheriting a wrong number. It gives an implementer no memory budget to design against, which for a 10,000-replicate vector bootstrap is a real gap rather than a tidy one.

B. Adopt **10.0 GB** as a working memory ceiling, noting it is borrowed from a storage budget
   > **Impact**: Gives implementation a concrete figure to design against, which a resampling routine genuinely needs. It would be this stage **adopting a number the authorities do not state for this purpose** — the conflation named as a defect, now inherited deliberately.

C. Require the peak memory to be **measured on the fixtures and frozen** as a declared value, with no ceiling asserted until then
   > **Impact**: Produces a real number from the project's own measurement discipline — the same route TE §15.1 uses for fixture tolerances — rather than borrowing or inventing one. Nothing is available to design against until the fixtures run, and **neither fixture has run**.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A **with** C's measurement obligation stated as owed — say only what the authorities support, name the conflation, and record that the peak-memory figure is to be **measured on the fixtures and frozen** rather than asserted now. Option B is the one to avoid: it would make this stage the place a storage budget quietly became a memory ceiling, which is exactly the defect the change record exists to correct. If you prefer strictly one option, A is the safe answer and C is the useful one.

[Answer]: A

---

## Consolidated Summary Confirmation

Confirm this reading before the two artifacts are written. Nothing below decides a
scientific value, and nothing claims a gate or acceptance row is discharged.

**Scope.** Two artifacts — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit. Those categories are still
assessed in the security artifact's scope note — and for this unit **Performance is a real
category**, which is why Question 2 was asked at all.

**Requirement set, derived before writing rather than after.** This unit's `functional-design`
states **1 requirement, 0 untested** — **FR-P1-05-8**, which the story map names **the one unit
with full acceptance coverage**. Its design additionally names **FR-P1-04-5** (context;
`features-and-splits`' requirement), **NFR-DET-01** and **NFR-AUD-01**. All four are cited.
*(This check was run up front for this unit. The same check, run only by the reviewer, found a
Major on each of the three preceding units.)*

**Q1 = B — a non-widening outcome on real data is disclosed AND adjudicated.** R-120's raise
stays at **fixture time**; on real data the comparison remains a **mandatory disclosure**, and
a **non-widening outcome becomes a named G-06 item the supervisor must rule on** before the
interval is reported as confirmatory. **This is not a new route:** this unit's own
`functional-design` already records that **the G-06 abort policy for a failed widening
comparison is owed to the Supervisor at G-05** (`GOV-2026-08-28-FD-01` Recommendation 23) and
is **decided by no artifact**. This answer states what that ruling must cover, and **does not
pre-empt it**.

**Why adjudication rather than a block.** A non-widening outcome means either **the
implementation is wrong** or **the assumption behind rejecting within-station does not hold for
this dataset** — both deserve a human ruling. But the comparator is **exact and quarantined**
precisely so it is **not load-bearing**; blocking on it would make a **rejected** method the
authority over the accepted one.

**Q2 = A, with C's measurement obligation stated as owed.** The resource posture is
**CPU-completeness only** — the bootstrap completes on CPU within the two governed platforms —
and the artifacts **record explicitly that no numeric memory ceiling exists in the
authorities**. **TE §9.3 is a storage budget**, and `services.md`'s *"peak memory … against TE
§9.3's 10.0 GB hard planning envelope"* is a **conflation with a change record owed**, quoted as
upstream text and **not adopted**. **The peak-memory figure is to be measured on the fixtures
and frozen** (TE §15.1's discipline), **not asserted now** — and **neither fixture has run**, so
there is no figure and none is invented.

**Carried, not re-decided.** R-113's bootstrap as a metric entry point in full; R-114's single
copy of the estimand arithmetic; R-115's fixed non-overlapping block grid; R-116's vector
property and missing-pair rule; **R-117's seed and generator pins** — `default_rng(seed)`
**(PCG64)**, block-index draws the only primary-stream consumer, child streams by
seed-sequence spawn, the replicate hash emitted by the producing path, and a call without
`seed` a **`TypeError` by signature**; R-118's config-resident frozen numbers with the
signature amendment **proposed not applied**; **R-119's method-parametric interval with the
percentile method PROPOSED and routed to the gate**; R-121's correlation emitted by the
producing path; R-122's eight checks.

**Status claims made.** None. **The interval method is unconfirmed** — if implementation is
reached with it unconfirmed, the posture is **TE §18.3's: stop and report rather than choose a
default**. **BLK-03, BLK-04, BLK-08 and BLK-09 are inherited exit conditions on this stage and
none is closed here.** The block-resampling scheme and the correlation series are likewise
**proposed, not decided**. **WS-17 (primary), TA-13 and TA-26 are undischarged**; TA-13 and
TA-26 belong to `foundation` and `models-and-baselines`. G-09 is signed (D-31) with
preconditions UNMET; stage 3.1 remains FAIL; `configs/` does not exist; no Python interpreter
exists here, so **no bootstrap has ever been run**.

Reply `Looks correct` to proceed, or state what to change.

[Answer]: Looks correct
