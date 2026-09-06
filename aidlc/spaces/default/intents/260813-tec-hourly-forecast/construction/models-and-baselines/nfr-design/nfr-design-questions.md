# NFR Design — Questions — `models-and-baselines`

**Unit** `models-and-baselines` (Bolt 8) · **Kind** `library` · **Stage** `nfr-design`

Two artifacts only — `security-design.md` and `logical-components.md`. `produces_kinds` maps
the other three to `[service]` / `[service, ui]`, and this unit is `library`.

**Nothing below decides a scientific value.** TE §18.2's absolute rule stands. The seeds are
D-122's, the grid counts D-121's, the seven LSTM settings Vision §8.6's, and the **TensorFlow
pin stays `TBD — freeze gate`**. No question here fills any of them.

**BLK-03 is an open exit condition on this unit** and independently bars implementation.
**7 of this unit's 9 requirements have no acceptance row** — proposed at 3.2 as one Vision
§15.2 request, **not approved**. Nothing below approves one.

---

> ## ⚠ WORKSPACE STATE VERIFIED 2026-09-04 — UPSTREAM CLAIMS HOLD, WITH ONE DETAIL CHANGED
>
> | Upstream claim | Verified state |
> |---|---|
> | W-11: this unit builds **ten** files, none of which exist | **Holds, exactly.** `src/models/` holds `__init__.py` only; `scripts/` holds only `audit_ec1_drivers.py` and `merge_coverage_year.py`; neither `tests/test_models_smoke.py` nor `tests/test_checkpoint_restore.py` is present. Derivation 1: **10 named, 0 on disk.** |
> | *"No Python interpreter exists in this environment"* | **Conclusion holds; the reason has changed.** No interpreter is reachable (`python` resolves to the zero-byte Windows Store stub; `py` launcher absent). A **3.14** interpreter ran here at some point (`src/data/__pycache__/config.cpython-314.pyc`) — **not** the governed 3.11 pin, so no execution it performed is governed evidence. **No model has ever been trained**, and no runtime, memory or convergence figure exists. |
> | `configs/` does not exist | **Holds.** So `experiment.yaml`'s grid, `seeds.yaml`'s seeds and the horizon list are all reads against a file that is not there. |
> | BLK-07 open, so `governance-guards` R-25's durable access log does not exist | **Holds.** `src/data/locked_test.py` exists but the log R-95 mechanism 3 reads is not there. This is Question 1. |

## Derivations printed before they are asserted

**Derivation 1 — the ten files W-11 names, against disk.** 10 named
(`src/models/persistence.py`, `climatology.py`, `ridge.py`, `random_forest.py`, `lstm.py`,
`train.py`, `checkpoint.py`; `scripts/06_train_and_predict.py`;
`tests/test_models_smoke.py`, `tests/test_checkpoint_restore.py`). **0 present.** No
contradiction between the "does not exist" claim and disk — unlike the sibling unit run
immediately before this one, where a test module claimed absent was present.

**Derivation 2 — the exceptions this unit raises, against their declaration site.** Raised
across W-1…W-12 (`grep -n "^RAISES"`, four fenced blocks): `PartitionError`, `LeakageError`,
`SeedError`, `AlignmentError`, `LockedTestError` — **5** distinct. `src/data/config.py`'s
`__all__` declares **17** and contains all five. Set-difference (raised, not declared): **0**.

**Derivation 3 — this unit's requirement IDs, against the upstream coverage tables.**
`unit-of-work.md` § 8 carries **9**: FR-P1-04-14, FR-P1-05-1, -2, -3, -4, -5, -6, -21, -22.
`security-requirements.md` carries **13** rows (those 9 + NFR-DET-01, NFR-LEAK-01, NFR-IRI-01,
NFR-AUD-01); `tech-stack-decisions.md` carries **7**, of which **NFR-PHASE-01** appears in that
file alone. Set-differencing the ID lists rather than the totals:

- **In the 9, absent from the 13: 0.** Every requirement this unit carries is cited.
- **Union across both upstream artifacts: 14** distinct IDs (13 ∪ {NFR-PHASE-01}).

**This unit's coverage set is complete**, and that is a result rather than a skipped check —
the same derivation found **3** uncited IDs on the unit run immediately before this one, and
`requirements.md`'s eleven-NFR space was already swept at 3.2, which is where NFR-AUD-01 was
added and the six genuinely-out-of-scope NFRs got a stated exclusion rationale. **This stage's
tables therefore carry 14 rows and add no ID.**

---

## Question 1

§ SEC-M-01's third mechanism — the one the 3.2 gate made **blocking** rather than advisory
(Q2 = B) — reads `governance-guards` R-25's durable access log to detect a December audit
access falling between `criterion_declared_at` and `run_at`. **BLK-07 is open and that log does
not exist**, so the artifact's own Assumptions record the block as *"specified and unrunnable
today."*

Mechanisms 1 and 2 (`partitions_read` excludes December; `criterion_hash` equals
`criterion_used_hash`) are runnable and depend on nothing external. So the question is what a
tuning run does while mechanism 3 cannot fire.

A. **Fail closed — no tuning run proceeds until R-25's log exists**
   > **Impact**: Consistent with the fail-closed answer the immediately preceding unit gave on the same shape of question, and with TE §18.3's stop-and-report rule. It makes one unit's blocker (BLK-07) block a second unit's entire tuning stage, and the selected hyperparameters are the input to the G-05 grid freeze — so the critical path lengthens by however long BLK-07 takes.

B. **Run mechanisms 1 and 2, record mechanism 3 as unmet** with a machine-readable reason the §18.3 preflight reads as a failing critical check
   > **Impact**: Tuning proceeds and the gate still refuses. But a `TuningRecord` and a selected hyperparameter set **exist on disk and get consumed** — they feed the grid freeze — and a gate report does not travel with them. This is the weakness that decided against skip-not-pass on the preceding unit.

C. **Make the human attestation UNCONDITIONAL** — every tuning run carries a dated, named attestation that no December figure informed the criterion, so the control no longer depends on the log at all; when R-25's log later exists, it **narrows** when an attestation is required rather than enabling the check
   > **Impact**: The control becomes runnable **today**, and the missing log makes the requirement **stricter** rather than unrunnable — every run attests, instead of only the runs the log flags. It costs a human turn on every tuning run, and it weakens nothing that mechanism 3 provided, because mechanism 3 never proved anything on its own: § SEC-M-01 already states the attestation *"proves nothing on its own"* and that the real residual — a December figure carried in someone's head — **cannot be closed by any mechanism**.

D. **Defer to 3.5**
   > **Impact**: Nothing is designed against a log that does not exist. It leaves `code-generation` to decide the behaviour of a control at a §18.3 stop-and-report point, which is the one decision §18.3 says an agent may not make.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C — it is the only option that makes the control **run**, and
> the argument is the artifact's own. The attestation was never the log's dependent: § SEC-M-01
> introduced the log to decide *when* an attestation is demanded, and the attestation itself is
> just a dated record that a named person considered the question while they still remembered
> what they knew. Removing the gating condition makes that record unconditional, which is
> strictly more coverage than the window ever gave, and it turns BLK-07 from a blocker into a
> future *narrowing*. A is defensible and is what the preceding unit chose — but there the
> missing artifact was the check's **only** possible input, whereas here the check has a
> runnable form that does not need it, so fail-closed would block a stage for a dependency the
> design can route around. **The residual is unchanged and stays stated: no artifact may
> describe December-blindness in tuning as fully enforced.**

[Answer]: C

---

## Question 2

3.2 deferred one thing about the attestation explicitly: *"Where it lives and what form it
takes is **owed at 3.5**; nothing here designs the field."* This is the stage that designs it.

The attestation has to be about a **specific** criterion — an attestation that floats free of
the criterion it certifies can be reused across a criterion change, which is exactly the
substitution mechanism 2 exists to catch.

Where does the attestation live?

A. **A field group on `TuningRecord`**, carrying the attester's name, an ISO date, and **the
   `criterion_hash` it attests to** — a re-declared criterion invalidates it and a fresh one is
   required
   > **Impact**: Binds the attestation to the exact criterion, so it cannot survive a criterion change — which closes the reuse channel without a new mechanism. It travels with the record the tuning run already writes, so there is one artifact to verify rather than two to join. It puts a human signature inside a machine-written record, and the record's integrity then carries the signature's.

B. **A separate attestation artifact under `evidence/`**, referenced by `run_id` from `TuningRecord`
   > **Impact**: Keeps the human record where this project's other human records live, auditable by a supervisor without reading a machine artifact. It is a join, and a join can be dangling — an attestation whose `run_id` matches nothing, or a run whose reference resolves to an attestation for a different criterion, are both new failure modes needing their own checks.

C. **An `evidence/DECISIONS.md` D-number**
   > **Impact**: Uses the project's authoritative decision record, and `team.md` fixes that a decision is not real until it has a D-number. An attestation is **not a decision** — it is a statement about what someone knew — so this would put a different kind of object into that register, and one per tuning run would flood it.

D. **Defer to 3.5**, as 3.2 already did
   > **Impact**: Second deferral of the same question. If Q1 lands on an unconditional attestation, deferring where it lives leaves the whole control undesigned at exactly the point it becomes load-bearing.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A, with the `criterion_hash` binding as the non-negotiable
> part. What makes an attestation worth anything here is that it is about **this** criterion at
> **this** time; a name and a date alone would let one attestation cover a criterion that
> changed after it was signed. B's supervisor-readability is a real benefit and is available as
> an addition later — a rendered view of the `TuningRecord` field — without introducing a join
> that can dangle. **Whichever is chosen, the attestation still proves nothing on its own, and
> that limit stays stated in the rule body rather than only in Assumptions.**

[Answer]: A

---

## Question 3

**W-12's receipt is this unit's half of a two-half contract, and its design turns on one word
3.2 left undefined: "durably flushed."** `06` writes the `DEC` prediction once, hashes it *at a
moment when no metric exists*, and **refuses to exit** if the write happened and the receipt
did not. `foundation` R-18's W-6 step 4 is the other half: it **refuses a `prediction_hash`
presented by the metric-computing process**.

Step 4's refusal can only work if `06` can tell whether the flush **succeeded**. NFR-AUD-01
requires registry writes to be **atomic or append-safe**, and a partially written receipt is
indistinguishable at the artifact from a missing one.

What does "durably flushed" mean concretely?

A. **Write the receipt to a temp file, `fsync`, then atomically rename into place; then append
   the registry row; `06` refuses to exit unless BOTH returned success**
   > **Impact**: A reader never sees a half-written receipt — the rename is atomic, so the receipt either is not there or is complete. The two writes are ordered and both checked, so the exit refusal has a real condition to test rather than an assumption. Cost: the receipt exists in two places (file and registry row) and they can disagree, which needs a stated rule about which is authoritative.

B. **The registry row is the only durable record** — no separate receipt file
   > **Impact**: One artifact, no divergence, and NFR-AUD-01's append-safe requirement applies to it directly. `foundation` R-18 owns that row, so this unit's producer-side control would depend on a sibling's write succeeding — and W-12's whole design rests on **writer and reader being in different processes with a file between them**. Collapsing the file removes the thing the control is built on.

C. **Receipt file only**, with the registry column populated later from it
   > **Impact**: Keeps this unit's half self-contained and testable without the registry existing. It defers the moment the hash becomes part of the permanent record, and TE §13.4's column 18 is where a reviewer looks — a receipt on disk that never reached the row is invisible to the audit that matters.

D. **Defer to 3.5**
   > **Impact**: Nothing designed against a registry that does not exist. It leaves the durability semantics of the one artifact that gates every `DEC` metric to an implementer, and G-06 cannot execute if this half is wrong.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A, with the **receipt file authoritative for the hash and the
> registry row authoritative for the run's existence**, and a disagreement between them a
> **raise** rather than a resolution. It is the only option that preserves W-12's stated
> mechanism — two processes, a file and a row between them — while giving step 4's exit refusal
> a condition it can actually evaluate. B is simpler and defeats the design; C leaves the
> audit surface empty. **Nothing here discharges TA-10 or TA-21 — both rows are owned
> elsewhere — and the contract stays unsatisfied from this side alone.**

[Answer]: A

---

## Question 4

§ SEC-M-05 and TS-M-02 state a rule and leave its mechanism open: **"an empty
`nondeterministic_ops` is never proof of determinism"** — an empty list is equally consistent
with a determinism check that never ran. And TS-M-02 records that the list itself **cannot be
enumerated until the TensorFlow pin is frozen**, because which operations lack deterministic
kernels is version-dependent.

So the design must make an empty list distinguishable from an absent check, without knowing
the pin.

A. **A positive probe** — the determinism utility runs a known-nondeterministic operation and
   asserts it is **caught and recorded**; if the probe records nothing, the check itself
   **fails**
   > **Impact**: Makes "empty is never proof" **executable** rather than stated: an empty list can only be reached through a probe that demonstrably detects something, so emptiness becomes evidence instead of ambiguity. It needs one operation known to be nondeterministic on the eventual pin — and TS-M-02 records that the set is version-dependent, so the probe's subject is itself owed at pin-freeze, which must be stated rather than assumed.

B. **Record a `determinism_probe_ran` boolean and the probe method** alongside the list
   > **Impact**: Cheap, needs no known-nondeterministic operation, and distinguishes the two cases in the record. It is a claim about the check rather than a demonstration by it — a `true` written by a probe that silently did nothing passes, which is the same shape as the forged-provenance residual on the preceding unit.

C. **Fail closed until the pin is frozen** — no determinism claim is recorded at all
   > **Impact**: Refuses to produce a record that could be misread, which matches this project's posture on unverifiable artifacts. It also blocks recording determinism evidence during fixture runs, which is where the pin gets frozen — so it risks a circular block.

D. **Defer to 3.5**
   > **Impact**: Nothing designed against an unfrozen pin. NFR-DET-01's evidence is WS-17 and TA-13, and both would rest on a record whose emptiness nobody can interpret.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A, with **B's boolean as a by-product rather than the
> mechanism** — the probe's own result is what sets it. The reason is the one this project keeps
> re-learning: a control that records that it ran is weaker than a control that proves it can
> detect. The dependency is real and belongs in Assumptions rather than in the design's
> confidence: **the probe's subject operation is owed at pin-freeze**, and if no operation on
> the frozen pin is reliably nondeterministic, the probe degrades to B and that degradation
> must be recorded, not absorbed.

[Answer]: A

---

## Question 5

`logical-components.md` needs a boundary criterion. The seven sibling units each chose a
different axis: `foundation` **write-integrity**; `governance-guards` **enforcement timing**;
`acquisition` **egress direction**; `inventory-and-registry` **how a failure reaches a human**;
`external-products` **what the component keeps out**; `target-standardization` **what each
component makes true about the target**; `features-and-splits` **the object whose integrity is
at stake**.

This unit is the only one that **trains**, and almost every rule it carries — R-90 through
R-102a — has the same shape: something plausible must not be allowed to stand in for the thing
that was specified. A single seed for the three-seed mean. A last epoch for the best
checkpoint. A re-tuned refit for the frozen one. A December-informed criterion for a
January–November one. A regenerated prediction for the one-shot write.

What criterion should the decomposition use?

A. **By the substitution each component refuses** — four components: the **model set** (a
   family added, a prohibited architecture present, a baseline fitted on everything); the
   **prediction** (a single seed, a best-of-three, a median, a last-epoch checkpoint, a
   provenance-mismatched mean); the **selection** (December, a changed grid, an invented
   ablation, an RF importance score, a re-tuning refit); the **locked-test write** (a second
   write, a regenerated file, a metric before the receipt)
   > **Impact**: Names the axis this unit actually varies on, and each box collects failures that are alike in kind and unalike across boxes. It also makes the negative controls fall out of the decomposition rather than being bolted on: every component's control is "the substitution is attempted and it fails," which is the affirmed practice's exact shape.

B. **By pipeline stage** — tune | fit | checkpoint | predict
   > **Impact**: Matches how an implementer reads `06_train_and_predict.py` and how the modules divide. It splits the three-seed mean from the checkpoint restore even though both are substitutions of one model for another, and it has no box for the locked-test write, which is not a stage but an event.

C. **By model family** — one component per M-01…M-06 plus the two generated tables
   > **Impact**: Maps one-to-one onto `src/models/*.py`, so the module boundaries and the component boundaries coincide exactly. Eight components for one `library` unit, and the rules that matter most here — determinism, tuning, the receipt — cut **across** every family rather than belonging to any, so they would have to be replicated or homeless.
D. **By workflow grouping** (W-1/W-2 | W-3/W-4 | W-5/W-6/W-7 | W-8…W-12)
   > **Impact**: Traceable straight back to `functional-design` and trivial to verify. W-12's one-shot write would share a box with the horizon and the sibling-owned evidence obligations on adjacency alone.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — a unit whose entire security property is *"the honesty of
> the comparison, not a credential"* is best decomposed by what each part refuses to let
> through, and this unit's rules are unusually uniform in that shape. It also gives the four
> boxes genuinely different blast radii: a wrong **model set** invalidates the ladder, a wrong
> **prediction** invalidates one number, a wrong **selection** invalidates every number
> downstream of it, and a wrong **locked-test write** cannot be undone at all. B is the better
> map of the code and the worse map of the risk.

[Answer]: A

---

## Consolidated Summary Confirmation

All five answered with the recommended option, guided mode, 2026-09-04. Recorded as **five
answers to five questions in this unit's set**, not a standing autonomy grant.

**Q1 — the December-window control while R-25's log is absent**: **C. The human attestation
becomes UNCONDITIONAL.** Every tuning run carries a dated, named attestation that no December
figure informed the criterion, so the control depends on **no external artifact** and is
runnable today. When R-25's durable log later exists it **narrows** when an attestation is
required, rather than enabling the check — **BLK-07 becomes a future narrowing, not a
blocker.** This deliberately differs from the fail-closed answer the preceding unit gave, and
the discriminator is stated: there the missing artifact was the check's **only** possible
input; here the check has a runnable form that does not need it. **The residual is unchanged
and stays in the rule body: the attestation proves nothing on its own, a December figure
carried in someone's head leaves no trace, and no artifact may describe December-blindness in
tuning as fully enforced.**

**Q2 — where the attestation lives**: **A. A field group on `TuningRecord`**, carrying the
attester's name, an ISO date, and **the `criterion_hash` it attests to**. The hash binding is
the non-negotiable part: it makes the attestation about **this** criterion, so a re-declared
criterion **invalidates** it and a fresh one is required — closing the reuse channel with no
new mechanism. A supervisor-readable rendered view (option B's benefit) remains available later
as a projection of the same field, without introducing a join that can dangle.

**Q3 — what "durably flushed" means**: **A. Write the receipt to a temp file, `fsync`,
atomically rename into place; then append the registry row; `06` refuses to exit unless BOTH
returned success.** The atomic rename means a reader never sees a half-written receipt, and the
two ordered checked writes give step 4's exit refusal a condition it can actually evaluate.
Precedence stated rather than left open: **the receipt file is authoritative for the hash, the
registry row is authoritative for the run's existence, and a disagreement between them
raises.** This preserves W-12's stated mechanism — writer and reader in different processes with
a file and a row between them — which option B would have collapsed. **Nothing here discharges
TA-10 or TA-21; both rows are owned elsewhere and the contract is not satisfied from this side
alone.**

**Q4 — making "an empty `nondeterministic_ops` is never proof" executable**: **A. A positive
probe.** The determinism utility runs a known-nondeterministic operation and asserts it is
**caught and recorded**; a probe that records nothing **fails the check**, so an empty list is
reachable only through a probe that demonstrably detects something. Option B's
`determinism_probe_ran` boolean is kept as a **by-product** set by the probe's own result, never
as the mechanism. **The dependency is stated, not absorbed: the probe's subject operation is
owed at pin-freeze**, since which operations lack deterministic kernels is version-dependent —
and if no operation on the frozen pin is reliably nondeterministic, the probe **degrades to B
and that degradation is recorded**.

**Q5 — the boundary criterion**: **A. By the substitution each component refuses** — four
components: the **model set**, the **prediction**, the **selection**, and the **locked-test
write**. Every rule this unit carries (R-90…R-102a) has that shape, the negative controls fall
out of the decomposition rather than being bolted on, and the four have genuinely different
blast radii: a wrong model set invalidates the ladder, a wrong prediction invalidates one
number, a wrong selection invalidates everything downstream of it, and a wrong locked-test write
**cannot be undone at all**.

**Unchanged by these answers.** No scientific value is decided; TE §18.2 stands. The
**TensorFlow pin stays `TBD — freeze gate`** and **blocks this unit specifically**;
`nondeterministic_ops` still cannot be enumerated until it is frozen. **D-122's seed set still
owes a supervisor signature at G-05**, and the grid hash must be committed before G-05.
**BLK-03 remains an open exit condition** and independently bars implementation. **7 of 9
requirements still have no acceptance row** — proposed as one §15.2 request, **not approved**.
WS-14, WS-15, TA-12, TA-13, TA-26 stay undischarged; TA-20 is supported, not owned. **No model
has ever been trained** and no runtime, memory or convergence figure exists. The **prediction-hash
receipt stays a two-half contract** with `foundation`; the **primary results table** stays
`regimes-diagnostics-reporting`'s; the **feature manifest's provenance** stays
`features-and-splits`'. **No module is written by this stage.**

<!-- Re-collected 2026-09-04: the redo jump on `nfr-design` reset this stage's receipt floor,
     invalidating this unit's summary-confirmation receipt. The stored value was `Looks correct`
     and is being re-affirmed on the fresh floor, not changed. The three adversarial findings
     fixed after that jump are recorded in the artifacts' own correction boxes — including the
     withdrawal of "strictly more coverage" in § SD-M-01, which qualifies the Q1 = C
     recommendation this file's own text states unqualified. That recommendation is left
     standing as written; the correction lives in the artifacts. -->

- Looks correct
- Request changes

[Answer]: Looks correct
