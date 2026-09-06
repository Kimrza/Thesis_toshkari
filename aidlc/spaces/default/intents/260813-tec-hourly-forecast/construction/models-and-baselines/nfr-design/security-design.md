# Security Design — `models-and-baselines`

**Unit** `models-and-baselines` (Bolt 8) · **Kind** `library` · **Stage** `nfr-design`

> ## ⚠ NOTHING HERE IS BUILT, NOTHING IS TRAINED, NOTHING IS DISCHARGED
>
> The asset this design protects is **the honesty of the comparison**, not a credential. Every
> mechanism below is a design for a module that **does not exist**: Derivation 1 puts W-11's
> **ten** named files at **0** present — `src/models/` holds `__init__.py` only, `scripts/`
> holds only `audit_ec1_drivers.py` and `merge_coverage_year.py`, and neither
> `tests/test_models_smoke.py` nor `tests/test_checkpoint_restore.py` exists.
>
> **No model has ever been trained.** No runtime, no peak memory, no convergence behaviour has
> been measured, and none is claimed. **The TensorFlow pin is `TBD — freeze gate`** and this is
> the unit it blocks: M-06's serialization contract, checkpoint format and determinism settings
> are all version-dependent. **`configs/` does not exist**; **no Python interpreter is
> reachable**, so every check designed here is **written-but-unexecutable**.
>
> **BLK-03 is an open exit condition** and independently bars implementation. **BLK-07 is
> open**, so `governance-guards` R-25's durable access log does not exist — § SD-M-01 is
> designed around that rather than through it.
>
> **7 of this unit's 9 requirements have no §16 or §19 acceptance row** — the largest untested
> share of any unit in this project — proposed at 3.2 as **one** Vision §15.2 request and
> **not approved**. **WS-14, WS-15, TA-12, TA-13 and TA-26 are owned and undischarged**; TA-20
> is supported, not owned; **TA-10, TA-21 and TA-27 are owned elsewhere**. **0 rows are claimed
> satisfied.**
>
> **No scientific value is decided here.** TE §18.2's absolute rule stands: the seeds are
> D-122's, the grid counts D-121's, the seven LSTM settings Vision §8.6's.

## Sources

- `../nfr-requirements/security-requirements.md` — **SEC-M-01** (December cannot inform selection; the three mechanisms; the Q2 = B block; the residual no mechanism closes; seeds never selected; grid content asserted; RF importance diagnostic), **SEC-M-02** (the three-seed mean and what may not stand in for it; provenance-disagreeing means fail; lowest-validation-RMSE restore; selection on mean per-fold skill; the stamp match before every scoring path), **SEC-M-03** (the closed model set; two absences as evidence; PyTorch prohibited; M-03 fitted on training partitions only; the co-reporting and disclosure obligations), **SEC-M-04** (the one-shot `DEC` write and the receipt that precedes any metric), **SEC-M-05** (determinism, CPU completeness, predeclared ablations, the config-only horizon), **SEC-M-06** (seven missing rows, seven controls), and its **13**-row coverage table.
- `../nfr-requirements/tech-stack-decisions.md` — **TS-M-01** (one forecasting stack; the pin this unit waits on; TA-26), **TS-M-02** (determinism as a utility and a recorded absence; *"where supported"* is version-dependent), **TS-M-03** (`scikit-learn` for M-04/M-05; the two library-shaped prohibitions; grid bounded by content), **TS-M-04** (checkpoints, serialization as a phase-transition asset, the config-only horizon), **TS-M-05** (two absences the stack must prove), **TS-M-06** (platform posture; the in-Kaggle obligation live here).
- `../functional-design/business-logic-model.md` — **W-1** (the stamp match before **every** scoring path), **W-2** (fit and predict over six families), **W-3** (the confirmatory prediction and BLK-03's four limbs), **W-4** (checkpointing and restore), **W-5** (tuning, and the channel that stays open), **W-6** (the grid freeze as content and immutability in one mechanism), **W-7** (five ablations, four reachable in Phase 1), **W-8** (the +24 h horizon, structurally config-only), **W-9** (M-03's fitting partition), **W-10** (two evidence obligations belonging to siblings), **W-11** (the ten files, and what this unit must not do), **W-12** (the one-shot `DEC` write, its five-step order, and the rejected alternative that is the whole design).
- `../functional-design/business-rules.md` — **R-90**…**R-102a**.
- **`performance-requirements`, `scalability-requirements` and `reliability-requirements` are absent by scope design**, not missing: `produces_kinds` maps all three to `[service]` / `[service, ui]` and this unit is `library`. Their subject matter is assessed in § Scope note, continuing `security-requirements.md`'s own § Scope note assessment of the same five categories at 3.2.
- `../../../inception/requirements-analysis/requirements.md` — the **14** IDs the two upstream artifacts carry between them (Derivation 3). No ID is added at this stage.
- `../../../inception/units-generation/unit-of-work.md` § 8 — the **9** requirements carried, and **BLK-03**.
- `../../../inception/application-design/component-methods.md` — `FeatureBundle`, `Prediction` carrying `partition_id`/`transform_id`, and § Depth's intra-package carve-out.
- `../../../inception/application-design/services.md` — `06_train_and_predict.py`'s writes, and the nine stage scripts' read/write split.
- `../../foundation/nfr-requirements/tech-stack-decisions.md` — the governed stack and the `TBD — freeze gate` pin, referenced not restated.
- `../../features-and-splits/nfr-design/security-design.md` — § SD-F-01's fail-closed answer and the discriminator it stated, which § SD-M-01 diverges from with the reason printed.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§7.1**, **§7.2**, **§8.1**, **§8.2**, **§8.3**, **§9.2**, **§9.3**, **§13.4**, **§13.5**, **§18.2–18.3**, **§19**.
- `../../../../../../../../PreFlight/vision_document(3)(2)(2).md` — **§2.4** (the binding honesty rule), **§6.4**, **§8.1**, **§8.3**, **§8.6**, **§15.2**.
- `evidence/DECISIONS.md` — **D-31** (G-09 signed, preconditions UNMET). *(Citation corrected 2026-09-04 on adversarial finding 2, Major: this line previously also attributed **D-121** and **D-122** to `evidence/DECISIONS.md`, which **ends at D-32** and contains neither — the same distinction `GOV-2026-08-21-UG-01` already resolved. The upstream `nfr-requirements` artifacts carry the same wrong attribution; they stay unedited under their frozen receipts, routed to the gate.)*
- **Vision §14.2's own decision register** — **D-121** (grid sizes: ridge 6, RF 18, LSTM 16), **D-122** (seeds; status quoted from the register's current row: *"Approved; supervisor sign-off closed 2026-08-22 by the project owner under the recorded student/supervisor authority equivalence … No supervisor signature artifact exists and none is claimed."*). A register **distinct from `evidence/DECISIONS.md`**. *(Status corrected 2026-09-04 on fourth-floor adversarial finding 1, Major; superseded quote preserved: "Approved — supervisor sign-off pending" — stale since 2026-08-22, carried here from upstream `nfr-requirements`, which still quotes it and stays unedited under its frozen receipt. Whether the authority-equivalence closure satisfies what "supervisor sign-off" gates at G-05 is a governance question routed to the gate, not resolved here.)*
- `nfr-design-questions.md` — **Q1 = C**, **Q2 = A**, **Q3 = A**, **Q4 = A**, **Q5 = A**, three printed derivations, and the receipted Consolidated Summary Confirmation.
- Workspace inspection, 2026-09-04 — recorded in § SD-M-00.

---

## Scope note

`produces_kinds` yields **two** artifacts for a `library` unit. The three absent categories are
assessed anyway:

| Category | Assessment for `models-and-baselines` | Where it lands |
|---|---|---|
| **Performance** | The one genuine constraint is **CPU completeness**, not speed (TE §9.2). M-06 is the largest compute in the project and **no runtime has been measured**. Two costs are added by design here: op determinism is documented to slow training (§ SD-M-05), and Q4's positive probe adds one deliberate nondeterministic operation per determinism check. Neither may be traded for a GPU dependency — TC-01 forbids it. | § SD-M-05 |
| **Scalability** | Bounded: three cells, calendar 2022, hourly, six model families, three seeds, six partitions. No growth projection. | — |
| **Reliability** | **Fail-closed on identity**, and Q3 = A extends it to durability: a frame whose spec is not `(partition k, role "score")` never reaches partition *k*'s scoring; a confirmatory mean whose inputs disagree on provenance fails; `06` **refuses to exit** holding a `DEC` prediction unless **both** the receipt rename and the registry append returned success. | § SD-M-02, § SD-M-04 |
| **Security** | This artifact — **selection integrity**. The threat is not an attacker; it is a plausible number standing in for the specified one. | § SD-M-01…§ SD-M-04 |
| **Observability** | `TuningRecord` (now carrying the attestation, Q2 = A), the grid hash committed before G-05, the prediction-hash receipt, the three-seed provenance record, and `nondeterministic_ops` **with its probe result** (Q4 = A). | § SD-M-01, § SD-M-04, § SD-M-05 |

---

## SD-M-00 — What is on disk

Verified 2026-09-04, before any mechanism below was designed.

| Claim | Verified state |
|---|---|
| W-11's ten files | **0 of 10 present.** `src/models/` holds `__init__.py`; `scripts/` holds two pre-scaffold scripts; `tests/` holds six modules, none of them this unit's two. |
| A Python interpreter | **Not reachable.** `python` resolves to the zero-byte Windows Store stub; the `py` launcher is absent. A **3.14** interpreter ran here at some point (`src/data/__pycache__/config.cpython-314.pyc`) — **not** the governed 3.11 pin, so nothing it produced is governed evidence. |
| `configs/` | **Absent.** `experiment.yaml`'s grid, `seeds.yaml`'s seeds and the horizon list are all reads against a file that is not there. |
| `governance-guards` R-25's durable access log | **Absent** (BLK-07 open). `src/data/locked_test.py` exists; the log § SEC-M-01's mechanism 3 reads does not. |
| The five exceptions this unit raises | **All present.** Derivation 2: `PartitionError`, `LeakageError`, `SeedError`, `AlignmentError`, `LockedTestError` are 5 of the **17** names in `src/data/config.py`'s `__all__`. Set-difference: **0** owed. |

**No claim/disk contradiction was found on this unit.** That is recorded as a result rather
than passed over in silence: the same inspection on the unit run immediately before this one
found a test module claimed absent that was present, and W-11's "these do not exist" is
accurate here file for file.

---

## SD-M-01 — December cannot inform selection, and the attestation is unconditional (Q1 = C)

**The requirement (R-95, W-5, Vision §8.3).** Model selection, feature selection, thresholds
and hyperparameters are **never** informed by December. **The trigger is December being
*seen*, not the locked test being opened** — the required pre-G-05 coverage audit means
December is legitimately seen earlier, and that is precisely the channel this closes.

**Two mechanisms run today.**

1. **`TuningRecord.partitions_read` excludes December.** Catches a December partition read.
2. **`criterion_hash == criterion_used_hash`** — the criterion declared *before* tuning equals
   the one used. Catches a criterion changed after December was seen, which the partition
   record cannot see.

**The third mechanism cannot run, and the design routes around it rather than through it.**
§ SEC-M-01's mechanism 3 joins `AccessRecord.retrieved_at_utc` against
`TuningRecord.criterion_declared_at` and `run_at`, restricted to `purpose` in
`"coverage_audit"` or `"regime_audit"`, with `"locked_evaluation"` **included rather than
filtered** because it is the G-06 event and cannot legitimately precede a tuning run at all.
That join reads `governance-guards` R-25's durable log. **BLK-07 is open and the log does not
exist.**

**The design (Q1 = C).** The human attestation becomes **unconditional**:

```
tune(...):
    require TuningRecord.attestation is present and binds this run's criterion_hash
    # no window computation; no read of R-25's log
```

Every tuning run carries a **dated, named attestation** that no December figure informed the
criterion. The control therefore depends on **no external artifact** and is runnable the moment
the module exists. When R-25's log later lands it does **two** things, not one: it **narrows**
when an attestation is demanded, **and it reinstates mechanism 3's sequencing detection**, which
the attestation cannot perform (see the box below). It does not *enable* the attestation check —
that runs without it — but it is **not** merely a narrowing either.

> ### Why unconditional, and why this diverges from the preceding unit
>
> `features-and-splits` § SD-F-01 answered the same shape of question — *what does a control do
> while its input does not exist* — with **fail closed**, and stated the discriminator: does
> the guarded object **exist and get consumed**. A tuning result plainly does; it feeds the
> G-05 grid freeze. So fail-closed would be the consistent answer **if the check had no
> runnable form**. It has one.
>
> **The attestation was never the log's dependent.** § SEC-M-01 introduced the log to decide
> *when* an attestation is demanded. The attestation itself is a dated record that a named
> person considered the question while they still remembered what they knew. Removing the
> gating condition makes that record **unconditional** — every run attests, rather than only the
> runs a log flags — and one unit's open blocker no longer stops a second unit's entire tuning
> stage.
>
> ### ⚠ "Strictly more coverage" is WITHDRAWN — mechanism 3 did two jobs and this replaces one
>
> *(Corrected 2026-09-04 on adversarial finding 1, Major. The superseded claim, preserved: this
> design was described as **"strictly more coverage than the window ever gave"**, and BLK-07 as
> **"a future narrowing rather than a blocker"**. Both are true of one limb and false of the
> other.)*
>
> Mechanism 3 carried **two** capabilities, and only one of them has a human-memory component:
>
> | Limb | What it did | Under Q1 = C |
> |---|---|---|
> | **(a) Attestation trigger** | Decided **when** a human attestation was demanded, by detecting a `"coverage_audit"` or `"regime_audit"` access inside the window | **Replaced, and widened.** Every run now attests, not only flagged runs. The **residual is unchanged and irreducible**: a December figure carried in a human's head leaves no trace in any mechanism, and **no mechanism can close it.** |
> | **(b) Sequencing detection** | § SEC-M-01 states that `"locked_evaluation"` is **included rather than filtered**, because it is the G-06 event and *"cannot legitimately precede a tuning run at all, so an access carrying it inside the window is itself a finding"* | **NOT replaced.** This is a **purely mechanical** detection with no human-memory component — a G-06 evaluation event straddling a tuning run — and an attestation about what informed a criterion **cannot** catch it. **It is unavailable today, with no substitute.** |
>
> **So the coverage comparison is not one-directional**: Q1 = C is **more** coverage on limb (a)
> and **strictly less** on limb (b). Conflating the two would let a reader take the whole loss
> to be the unclosable residual, when part of it is a concrete check the redesign does not
> perform.
>
> **What is owed, so the capability is not quietly abandoned.** When R-25's durable log lands,
> **limb (b) is reinstated as an additional check** — `"locked_evaluation"` inside the window
> raises — **and limb (a)'s attestation stays unconditional rather than reverting to
> log-gated**, because an unconditional record is the wider of the two. **Until then, no artifact
> may describe the sequencing violation as detected**, and **no artifact may describe
> December-blindness in tuning as fully enforced.**
>
> **What the attestation is worth, stated without inflation.** A self-attestation about one's
> own knowledge **proves nothing on its own**. What it buys is a dated, named record that a
> specific person considered the question **at the time** — worth more than a flag read weeks
> later at G-05.
>
> **The residual, unchanged.** *"A choice informed by a December figure a human carries in
> their head leaves no trace"* in any mechanism. Mechanism 3 would have made an overlap
> **visible**; it never eliminated it, **and no mechanism can**. **No artifact may describe
> December-blindness in tuning as fully enforced.**
>
> **The sequence is not forbidden.** The pre-G-05 December coverage and regime audit is
> **required** and its timing is not this unit's to control. Forbidding a tuning run from
> post-dating an audit access would set one mandatory obligation against another with no rule
> to resolve them.

**Where the attestation lives (Q2 = A).** A field group on **`TuningRecord`**:

| Field | Content | Why |
|---|---|---|
| `attested_by` | The person's name | An attestation with no attester is not one. |
| `attested_at_utc` | ISO timestamp | *"At the time"* is the whole value; a date added later is a different claim. |
| `attests_criterion_hash` | **The `criterion_hash` it attests to** | **Load-bearing.** It makes the attestation about *this* criterion, so a **re-declared criterion invalidates it** and a fresh one is required. |

**The reuse channel this closes, with no new mechanism.** A name-and-date attestation floats
free of what it certifies, so one attestation could cover a criterion changed after it was
signed — exactly the substitution mechanism 2 exists to catch, reintroduced through the human
record. Binding the hash closes it: `attests_criterion_hash != criterion_hash` **raises**.

> ⚠ **The three attestation fields are an OWED entity amendment, not existing fields** *(added
> 2026-09-04 on adversarial finding 1, Major)*. `TuningRecord`'s **owning definition** —
> `functional-design/domain-entities.md` § 5, frozen under its completed-stage receipt —
> carries exactly the seven fields its own review history froze, and **none of the three
> above**. Adding them is an amendment to an approved functional-design entity and is
> **change-control-gated**, the same footing as `acquisition`'s `write_restricted` and this
> unit's serialization-format constraint: Q2 = A is a **proposal to that gate**, and no
> implementation may add the fields before the entity's owning definition is amended under a
> change record. The upstream artifact stays unedited; the amendment is a gate item.

**Negative controls.** A tuning run with **no** attestation **fails**. An attestation whose
`attests_criterion_hash` does not match the run's criterion **fails**. A December partition in
`partitions_read` **fails**. A `criterion_hash` / `criterion_used_hash` mismatch **fails**.

**Rejected, and recorded so it is not re-proposed.** Option B — a separate attestation artifact
under `evidence/` joined by `run_id` — is more supervisor-readable and introduces a **join that
can dangle**: an attestation matching no run, or a run resolving to an attestation for a
different criterion, are two new failure modes needing their own checks. A rendered,
supervisor-readable **projection** of the `TuningRecord` field delivers the same benefit
without the join, and remains available later. Option C — an `evidence/DECISIONS.md`
D-number — was rejected because an attestation is **not a decision**, and one per tuning run
would flood the register.

**Carried unchanged.** Seeds are **never selected** — not on validation, not after seeing
December; `seeds.yaml` fixes development **42**, final **{1337, 2024, 7}**, bootstrap
**20221201**, and **D-122's own status travels with them** — quoted from Vision §14.2's
current row: *"Approved; supervisor sign-off closed 2026-08-22 by the project owner under the
recorded student/supervisor authority equivalence … No supervisor signature artifact exists
and none is claimed."* The set is frozen for implementation. *(Corrected 2026-09-04 on
fourth-floor finding 1, Major; superseded: "Approved — supervisor sign-off pending … still
owes a signature at G-05". Whether the authority-equivalence closure satisfies what
"supervisor sign-off" was to gate at G-05 — given no signature artifact exists — is routed to
the gate, not decided here.)*
Grid **content** is asserted as well as immutability — **ridge 6, RF 18, LSTM 16** (D-121) and
the **seven** fixed LSTM settings, living **once** in `experiment.yaml` with its **hash
committed before G-05**, because *"a grid that is immutable but wrong is immutably wrong."*
**Random Forest importance is diagnostic and never a selection input** (R-100, Vision §6.4) —
saved with `authoritative = false` in its own metadata, and an importance score reaching the
production feature path **fails**, checked on this unit's own module graph. **FR-P1-05-3's
stated evidence is the feature manifest's provenance, and that manifest is
`features-and-splits`'** — a consumed cross-unit dependency over which this unit **claims no
check** (W-10).

---

## SD-M-02 — The confirmatory prediction, and the four substitutions it refuses

**The confirmatory prediction is the three-seed element-wise mean** (R-91, W-3, NFR-DET-01),
and **nothing may be substituted for it** — not a single seed, not a best-of-three, not a
median. Four refusals, each with its own failure:

| Substitution attempted | Refusal | Rule |
|---|---|---|
| A single seed, a best-of-three, or a median presented as the confirmatory prediction | `SeedError` — the expected seed set is an argument (`expected_seeds`), so a mean over the wrong set is unrepresentable rather than merely wrong | R-91 |
| A mean over predictions from different feature sets, partitions or transform IDs | `AlignmentError` / `PartitionError` — *"a number that looks like one"* is refused on provenance | R-92 |
| M-06's **last epoch** in place of its **lowest-validation-RMSE checkpoint** | The restore path is a **tested behaviour** (`test_checkpoint_restore.py`), because last-epoch restore is the library default shape and the correct behaviour is the one that needs proving | R-94, W-4, TS-M-04 |
| A refit that **re-tunes** in place of the frozen refit | Selection is on **mean per-fold skill score**, and **the refit changes no hyperparameter** — *"a refit that re-tunes is a second selection with no record"* | R-101 |

**The stamp match runs before EVERY scoring path, not once at entry** (R-90, W-1). A frame
whose spec is not `(partition k, role "score")` **never reaches** partition *k*'s scoring, and
a bundle whose `transform_id is None` **raises** — the consumer-side half of
`features-and-splits`' fitting-identity contract. `Prediction` carries `partition_id` and
`transform_id` onward to `07`, because the stamp has to travel the whole way rather than to the
first consumer.

---

## SD-M-03 — The model set is closed, and two absences are tested

**The set is closed** (R-102, TE §8.2, §8.3): **M-01** persistence, **M-02** 24-hour seasonal
persistence, **M-03** fitted station×month×hour climatology, **M-04** Ridge, **M-05** Random
Forest, **M-06** compact LSTM. **B-01 (IRI) and C-01 (CODE GIM) are generated, not trained** —
a benchmark table and a comparator table, **never models in the ladder**.

**Two absences are evidence, not omissions.** **GRU** is removed with the gate closed;
**residual modules** (IRI-residual RF, IRI-residual LSTM) are removed; **SSN** is absent as a
feature. **TA-08 and TA-12 require grep evidence that they are absent from the codebase** — an
absence that is **tested rather than assumed**, which is what makes "we did not build it" a
checkable property of the tree. **Consequence for dependency choice, carried from TS-M-05:** no
package is added that bundles a prohibited architecture or makes one a one-line import, because
it would make that grep evidence harder to interpret.

**PyTorch is prohibited** in the governed pipeline, and the reason is scientific rather than
operational: a framework change between Phase 1 and Phase 2 would make the cross-phase
comparison uninterpretable. Transformer, attention, BiLSTM, GNN and broad architecture search
are out of scope.

**M-03 is fitted on training partitions only** (R-98, W-9, NFR-LEAK-01) —
`climatology_fit_partition(prediction)` returns the partitions it was **actually** fitted on and
every one must be a training partition. **Negative control: a climatology fitted across all
partitions fails.** *"A climatology fitted on everything is a leak wearing the clothes of a
baseline."*

**The three difficulty controls are produced here and reported elsewhere.** Persistence,
24-hour seasonal persistence and the training-partition-only climatology are **co-reported in
the same primary results table** as the LSTM-vs-IRI comparison, never in an appendix, and **any
baseline that beats the LSTM on the locked test is disclosed** in that table and in the
abstract-level conclusion (Vision §2.4's binding honesty rule). **`regimes-diagnostics-reporting`
owns that table (TA-20); this unit supports it.** This artifact states the obligation and
**does not claim to discharge it**.

---

## SD-M-04 — The one-shot `DEC` write, and what "durably flushed" means (Q3 = A)

**W-12's five-step order is the control, and its order is the whole design.** `06` writes the
`DEC` prediction **once**; computes `sha256` over the file **as written**, at a moment when **no
metric exists**; **durably flushes** the receipt, whose `sha256` becomes `prediction_hash`,
TE §13.4's **column 18 of twenty** on `06`'s own registry row; **refuses to exit** if step 1
happened and steps 2–3 did not; and only then may `07` or the bootstrap score, each
re-verifying the file against `sha256` and refusing a `recorded_at_utc` that does not precede
its own call.

**What 3.2 left undefined, designed here.** Step 4's refusal can only work if `06` can tell
whether the flush **succeeded**, and NFR-AUD-01 requires registry writes to be **atomic or
append-safe** — a partially written receipt is indistinguishable at the artifact from a missing
one.

```
1. write receipt to <path>.tmp
2. fsync(<path>.tmp)
3. atomic rename <path>.tmp -> <path>          # a reader never sees a partial receipt
4. append the registry row (prediction_hash at column 18, joined by run_id)
5. exit ONLY IF steps 3 AND 4 both returned success; otherwise LockedTestError
```

**Precedence, stated rather than left to be discovered.** The **receipt file is authoritative
for the hash**; the **registry row is authoritative for the run's existence**; and a
**disagreement between them raises**. Two carriers without a stated precedence would convert a
detectable divergence into an invisible one — the same reasoning that rejected the
dual-carrier option on the preceding unit.

> **Why the file is not collapsed into the registry row.** W-12's mechanism **is** the process
> boundary: *"writer and reader in different processes, with a file and a registry row between
> them."* Writing the receipt inside `07_evaluate_and_report.py` or inside
> `vector_block_bootstrap` is the cheapest way to satisfy the two consuming rules and is
> **prohibited**, because both are metric callers — the process computing the metric would also
> timestamp the receipt, so *"the receipt precedes the metric"* would hold **by construction on
> every run**, including a run where the prediction was regenerated after a score was seen.
> **The control would pass its own test and detect nothing.** Making the registry row the only
> durable record removes the file that boundary is built on, which is why Q3's option B was
> rejected.
>
> For the same reason step 4 is a refusal **to exit** and not a refusal to score: a refusal to
> score is the check `07` already owns, and duplicating it would leave the producer side
> unguarded.

**Negative controls.** A `DEC` prediction file with **no receipt** → **raises in `06`**, not in
`07`. A receipt whose `sha256` does not match the file as written → **raises in `06`**. A
receipt renamed but whose registry append failed → **raises in `06`** on the exit path. A
receipt written but **not flushed** before exit → **raises in `06`**.

**Locked-test discipline, carried.** Predictions are generated and written **exactly once**,
after **G-05 is signed**, and **hashed before any metric is computed**. Every `DEC` metric entry
point **refuses without a verified receipt** — fail-closed while the producing half is unbuilt.
Every locked-test access records **`locked_test_accessed = true`**, and any test-driven change
made **after** locked-test access is labelled **exploratory**.

**Two halves, and this one does not declare the contract satisfied.** `foundation` R-18's W-6
step 4 **refuses a `prediction_hash` presented by the metric-computing process** — the
destination-side complement. *"Neither half suffices alone: this workflow stops the receipt
being created in a metric process, R-18 stops it being recorded from one."* **TA-10 and TA-21
are both owned elsewhere and neither is discharged here.**

**`prior_period_exposure` is not written by this unit**, and its Phase 1 value is **`false`**.
`foundation`'s W-6 step 5 is a hard refusal of `true` on a Phase 1 row — *"Phase 1 is the first
December exposure; `true` belongs to the Phase 2 replication"* — and the field's **source is
`governance-guards`' locked-test guard** while its **destination is `foundation`'s registry
row**. This unit is neither, and **claims no check over it**. The deviation from the approved
remediation text is carried to the gate at `business-rules.md` R-102a rather than resolved
here.

---

## SD-M-05 — Determinism, CPU, and the ablations (Q4 = A)

**The rule 3.2 stated and left without a mechanism**: *"an empty `nondeterministic_ops` is
never proof of determinism"* — an empty list is equally consistent with a determinism check
that never ran. And the list itself **cannot be enumerated until the pin is frozen**, because
which operations lack deterministic kernels is version-dependent.

**The design (Q4 = A) — a positive probe.** The seed utility runs a **known-nondeterministic
operation** and asserts it is **caught and recorded**. If the probe records nothing, **the check
itself fails**:

```
determinism_check():
    set seeds via tf.keras.utils.set_random_seed
    enable tf.config.experimental.enable_op_determinism()   # "where supported"
    result = probe(known_nondeterministic_op)
    if result records nothing:  raise DeterminismError(resource, expectation)
    record nondeterministic_ops  +  the probe's own result
```

An empty `nondeterministic_ops` is now reachable **only** through a probe that demonstrably
detects something, so **emptiness becomes evidence instead of ambiguity**. Option B's
`determinism_probe_ran` boolean is kept as a **by-product set by the probe's result**, never as
the mechanism — a `true` written by a probe that silently did nothing is the same shape as the
forged-stamp residual recorded on the preceding unit.

**The dependency, stated rather than absorbed.** The probe's **subject operation is owed at
pin-freeze**: which operations are reliably nondeterministic differs across TensorFlow
releases, and the pin is `TBD — freeze gate`. **If no operation on the frozen pin is reliably
nondeterministic, the probe degrades to option B, and that degradation is recorded** rather
than passed over. Likewise, if a **required** operation has no deterministic kernel,
**NFR-DET-01's guarantee narrows** and the narrowing is recorded.

**Determinism costs speed, and the cost cannot be traded away.** Enabling op determinism is
documented to slow training. **CPU is a complete execution path, not an emergency mode**
(TE §9.2, TC-01), and **GPU may be an optional accelerator only, never a dependency of any
result** — so a determinism setting that costs speed cannot be exchanged for a faster GPU path,
because no result may depend on that path existing. Any GPU parity check is **optional evidence
within a frozen tolerance** (EV-18), never the primary path.

**Nothing is measured.** M-06 is the largest compute in the project and **no training runtime,
peak memory or convergence behaviour exists**. TE §9.3's planning envelope is a **storage**
budget, and **no numeric memory ceiling exists in the authorities** — the conflation is not
repeated here.

**The in-Kaggle obligation is live for this unit** in a way it is not for Bolt 1: any governed
run inside a Kaggle session must first evidence that the required critical tests and applicable
fixtures **passed inside that same session**, because a Kaggle session carries no git working
tree and a local suite run proves nothing about the environment the training actually ran in.
**This unit performs the project's largest governed runs.**

**Ablations are predeclared** (R-97, W-7, TE §7.2) as named runs in `experiment.yaml` with run
IDs, executed on the **frozen January–November folds** with identical folds, masks and tuning
budget. **Five are named; four are reachable in Phase 1** — `ABL-NODOY`, `ABL-DIFF`,
`ABL-NOSW`, `ABL-HIST48`, with **`ABL-ZENITH` deferred to Phase 2**. **`ABL-DIFF`
inverse-transforms to absolute TECU before any metric**; **`ABL-HIST48` runs only after the
primary configuration is frozen**; **no ablation is invented after results are seen**.

**The +24 h horizon is structurally config-only** (R-99, W-8): `experiment.yaml` exposes
`horizons: [1]` with **24 implemented and testable but absent from the default run list**, and
horizon travels as a **parameter**. **A horizon change requiring a code edit fails** — stated
because the natural implementation, a second training script or a branch on horizon, would make
the horizon a code fact and give a later run an occasion to alter the model while "just adding
a horizon".

**Serialization is a phase-transition asset** (NFR-PHASE-01, TE §7.0B). The
`phase_transition_manifest` hashes the **architecture serialization** among its protected
items, and **Phase 2 refuses to train if any protected hash differs**, so the format is **not a
free implementation choice at 3.5** — changing it changes a protected hash. Phase 2 also
**carries no Phase 1 fitted weights forward** and **no Phase 1 result may motivate a Phase 2
model or evaluation change**. **TA-27 is `governance-guards`'** and is not discharged here.

---

## SD-M-06 — Seven requirements have no acceptance row, and all seven keep their controls

The seven controls affirmed at 3.2 are carried unchanged, because a control required
independently of §19 does not become optional at the next stage. **One is updated by Q1 = C**:

| Requirement | Rule | Negative control |
|---|---|---|
| **FR-P1-04-14** | R-101 — selection on mean per-fold skill; refit preserves hyperparameters | A refit that changes a hyperparameter **fails** |
| **FR-P1-05-3** | R-100 — RF importance never a selection input | An importance score used to add or drop a feature **fails** |
| **FR-P1-05-4** | R-95 — tuning reads Jan–Nov only | A December partition in `partitions_read` **fails**; a criterion-hash mismatch **fails**; **and, updated by Q1 = C, a run with no attestation — or an attestation not bound to this run's `criterion_hash` — fails.** The third clause is now **runnable**: it no longer reads R-25's log. ⚠ **But mechanism 3's OTHER limb is not replaced** — a `"locked_evaluation"` access inside the tuning window, which § SEC-M-01 calls *"itself a finding"*, is a mechanical sequencing detection an attestation cannot perform, and it is **unavailable until R-25's log lands** (§ SD-M-01's correction box) |
| **FR-P1-05-5** | R-96 — grid content and immutability | A grid whose content differs from D-121's counts **fails**; a changed grid hash **fails** |
| **FR-P1-05-6** | R-97 — ablations predeclared | An ablation absent from `experiment.yaml` **fails**; `ABL-HIST48` before the primary freeze **fails** |
| **FR-P1-05-21** | R-98 — M-03 fitted on training partitions only | A climatology fitted on the full dataset **fails** |
| **FR-P1-05-22** | R-99 — +24 h horizon config-only | A horizon change requiring a code edit **fails** |

**The seven rows stay proposed and unapproved.** They were put to the gate at 3.2 as **one**
Vision §15.2 request, because they are one gap rather than seven, with D-32 cited as precedent
for the **route** and not as approval. **This stage proposes nothing new and approves nothing.**

---

## SD-M-07 — What this unit does not own

- **The primary results table** (TA-20) — `regimes-diagnostics-reporting`'s. This unit produces
  all three difficulty controls and states the co-reporting and disclosure obligations.
- **The feature manifest's provenance** — `features-and-splits`'. FR-P1-05-3's stated evidence
  rests on it, and this unit **claims no check over it** (W-10).
- **TA-10 and TA-21** — both owned elsewhere; the receipt is a two-half contract with
  `foundation`.
- **TA-27** — `governance-guards`'; cited as an obligation on this unit's serialization choice.
- **`prior_period_exposure`** — source `governance-guards`, destination `foundation`; this unit
  is neither.
- **`PartitionError`'s declaration site** — `src/data/config.py`. This unit is the exception's
  **semantic owner but not its declaration site**.
- **Fold construction** — `features-and-splits`'. This unit **consumes partitions and derives
  none**, and `scikit-learn`'s CV splitters are not used.
- **The TensorFlow pin** — `foundation`'s, and **`TBD — freeze gate`**.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| **FR-P1-04-14** | SD-M-02, SD-M-06 | ⚠ **NO ROW** — proposed at 3.2, **not approved** | control required |
| FR-P1-05-1 | SD-M-03 | WS-14, TA-12, TA-26 | `Pending` — **pin unfrozen** |
| FR-P1-05-2 | SD-M-02, SD-M-05 | WS-15, TA-13 | `Pending` |
| **FR-P1-05-3** | SD-M-01, SD-M-06 | ⚠ **NO ROW** — proposed | control required; evidence rests on a sibling's manifest |
| **FR-P1-05-4** | SD-M-01, SD-M-06 | ⚠ **NO ROW** — proposed | control required; **third clause now runnable** (Q1 = C) |
| **FR-P1-05-5** | SD-M-01, SD-M-06 | ⚠ **NO ROW** — proposed | control required |
| **FR-P1-05-6** | SD-M-05, SD-M-06 | ⚠ **NO ROW** — proposed | control required |
| **FR-P1-05-21** | SD-M-03, SD-M-06 | ⚠ **NO ROW** — proposed | control required |
| **FR-P1-05-22** | SD-M-05, SD-M-06 | ⚠ **NO ROW** — proposed | control required |
| NFR-DET-01 | SD-M-02, SD-M-05 | WS-17 (supporting), TA-13 | `Pending` — probe subject **owed at pin-freeze** |
| NFR-LEAK-01 | SD-M-03 | TA-11 | `Pending` |
| NFR-IRI-01 | SD-M-03 | WS-10, TA-07 | `Pending` — test written, **UNEXECUTED** |
| NFR-AUD-01 | SD-M-04 | **TA-10, TA-21** — both owned elsewhere | `Pending` |
| NFR-PHASE-01 | SD-M-05 | **TA-27** — owned by `governance-guards` | `Pending` |

**Derived and printed.** **8** design sections (SD-M-00…SD-M-07). **14** coverage rows, counted
directly from the table above: FR-P1-04-14, FR-P1-05-1, -2, -3, -4, -5, -6, -21, -22,
NFR-DET-01, NFR-LEAK-01, NFR-IRI-01, NFR-AUD-01, NFR-PHASE-01. **7** with **no acceptance
row** — re-derived by counting `⚠ NO ROW` cells, not read off the map. **0** rows claimed
satisfied. **0** new dependencies. **0** IDs added at this stage. **0** exceptions owed at
their declaration site.

**The arithmetic of 14, printed.** `security-requirements.md` carries **13** rows;
`tech-stack-decisions.md` carries **7**, of which **NFR-PHASE-01** appears in that file alone.
**13 ∪ {NFR-PHASE-01} = 14.** Set-differencing the ID lists rather than the totals:
`unit-of-work.md` § 8's **9** requirements are **all** present in the 13, so **0** are added
here. This is stated as a result: the same derivation found **3** uncited IDs on the unit run
immediately before this one, and the eleven-NFR space was swept at 3.2 — which is where
NFR-AUD-01 was added on an adversarial Major and the six out-of-scope NFRs (`NFR-DQ-01`,
`NFR-FAIR-01`, `NFR-LIC-01`, `NFR-REP-01`, `NFR-SEC-01`, `NFR-TDEF-01`) received a stated
exclusion rationale.

## Assumptions & Open Questions

- **[Q1 / SD-M-01]** The attestation is **unconditional** and depends on no external artifact. **The residual is unchanged: the attestation proves nothing on its own, a December figure carried in someone's head leaves no trace, and no artifact may describe December-blindness in tuning as fully enforced.**
- **⚠ Open, and OWED — mechanism 3's sequencing detection is dropped, not replaced** *(added 2026-09-04 on adversarial finding 1, Major; the withdrawn claim "strictly more coverage than the window ever gave" is preserved in § SD-M-01's correction box)*. Mechanism 3 did **two** jobs: it triggered the attestation, **and** it made a `"locked_evaluation"` access inside the tuning window *"itself a finding"* — a **purely mechanical** sequencing check with no human-memory component. Q1 = C replaces the first and **cannot perform the second**, which is therefore **unavailable today with no substitute**. **BLK-07 is consequently not a mere narrowing**: when R-25's durable log lands, limb (b) is **reinstated as an additional check** while the attestation **stays unconditional**. Until then **no artifact may describe the sequencing violation as detected**.
- **[Q1 / SD-M-01]** This unit **diverges** from `features-and-splits`' fail-closed answer on the same shape of question, and the discriminator is printed: there the missing artifact was the check's **only** possible input; here the check has a runnable form that does not need it. Recorded so the divergence reads as reasoned rather than inconsistent.
- **[Q2 / SD-M-01]** A supervisor-readable **projection** of the `TuningRecord` attestation fields is available later without introducing a join. If a separate `evidence/` artifact is ever adopted instead, the dangling-join and wrong-criterion failure modes need their own checks.
- **[Q3 / SD-M-04]** Precedence is stated: **receipt file authoritative for the hash, registry row authoritative for the run's existence, and a disagreement raises.** Collapsing either carrier removes the process boundary W-12's design rests on.
- **[Q4 / SD-M-05]** **The probe's subject operation is owed at pin-freeze.** If no operation on the frozen pin is reliably nondeterministic, the probe **degrades to a recorded boolean and the degradation is recorded**. If a required operation has no deterministic kernel, **NFR-DET-01's guarantee narrows**, and the narrowing is recorded rather than absorbed.
- **[assumption]** `tf.config.experimental.enable_op_determinism()` is available and effective on the eventual pin. TE §8.1 says *"where supported"*, which concedes it may not be for every operation.
- **[assumption]** CPU training of M-06 completes in a tolerable time. **Unmeasured** — nothing has been trained. If it does not, the response is **not** to make GPU a dependency; TC-01 forbids it and the constraint returns here.
- **[SD-M-01]** **The TensorFlow pin is `TBD — freeze gate` and blocks this unit specifically.** M-06's serialization contract, checkpoint format and determinism settings are all version-dependent, and `nondeterministic_ops` is a **measured output of the frozen environment**, not a list this stage writes.
- **Open — BLK-03 is an exit condition on this unit** and independently bars implementation while its contract limbs stand unapproved. **Approving this design is not the contract's approval.**
- **Open — seven acceptance rows are proposed and unapproved**, as one §15.2 request. Several of the seven are rules `project.md` lists under `## Forbidden` or `## Mandated`.
- **Carried, re-derived 2026-09-04 — D-122's sign-off status.** Vision §14.2's current row: closed 2026-08-22 by the project owner under the recorded authority equivalence, with **no supervisor signature artifact existing and none claimed**. The superseded carried line ("owes a supervisor signature at G-05") is preserved here; whether the equivalence closure satisfies the G-05 gate's intent is a **governance question routed to the gate**. The grid hash must still be **committed before G-05** — unchanged.
- **Carried — the prediction-hash receipt is a two-half contract** with `foundation`; **not satisfied from one side**. **`prior_period_exposure`'s predicate deviation** stays raised for the owner at R-102a: if Recommendation 1 meant a different predicate, it needs a different field name.
- **Carried — D-31's disclosure travels with the G-09 signature**: the §18.3 preflight never ran, the critical tests are unexecuted here, and `aws_ai_dlc_preflight_report` does not exist. **"No failing critical test" is unproven, not proven.**
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, approves an acceptance row, closes a blocker, or claims a gate or test as discharged.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-04T17:18:59Z
**Iteration:** 1 (fresh receipt floor — prior pass's two Majors independently re-verified as fixed; see below)

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `nfr-design/security-design.md` § SD-M-01 "Where the attestation lives (Q2 = A)" (lines 180–191); `logical-components.md` C-3 entry (lines 137–139) | **The Q2=A attestation field group (`attested_by`, `attested_at_utc`, `attests_criterion_hash`) added to `TuningRecord` is not reflected anywhere in the entity's own owning definition, `functional-design/domain-entities.md` § 5, and no artifact flags this as an owed update.** Read `domain-entities.md` § 5 directly: its `TuningRecord` table has exactly seven fields — `run_id`, `partitions_read`, `criterion_declared_at`, `criterion_hash`, `criterion_used_hash`, `run_at`, `audit_access_since_declaration` — none of them the three attestation fields, and that seven-field count is the product of a carefully tracked, multi-iteration field-count history (`business-logic-model.md`'s own review log: "Seven fields, all used" as of the 2026-08-24 fix). `business-rules.md` R-95's three mechanisms likewise name only the pre-existing seven fields. An implementer building `src/models/train.py`'s tuning path from the functional-design layer alone — the layer this project's own `TuningRecord` field-consistency history treats as authoritative for the entity's shape — has no way to know the three attestation fields exist; conversely, an implementer following only this nfr-design artifact has no cross-reference telling them `domain-entities.md` needs a matching update. This is exactly the "mechanism sketched against a shape the approved entity does not carry" failure mode the dispatch calls this project's highest-prior defect, and it recurs here in the same file (`domain-entities.md` § 5) that a prior iteration cycle at `functional-design` already spent four review passes making internally consistent. | Add the three attestation fields to `functional-design/domain-entities.md` § 5's `TuningRecord` table (or, if `functional-design` artifacts are frozen/terminal and cannot be re-opened, add an explicit `## Assumptions & Open Questions` item in both `security-design.md` and `logical-components.md` stating that this nfr-design-introduced field group is not yet reflected in the owning entity definition and is owed at or before `code-generation`). |
| 2 | Major | `nfr-design/security-design.md` § Sources (line 47); the identical pattern in `nfr-requirements/security-requirements.md` § Sources (line 28) and `nfr-requirements/tech-stack-decisions.md` § Sources (line 26) | **D-121 and D-122 are misattributed to `evidence/DECISIONS.md`, which does not contain them.** § Sources reads: `"evidence/DECISIONS.md — D-121 (grid sizes), D-122 (seeds, ...), D-31 (G-09 signed, preconditions UNMET)."` Read `evidence/DECISIONS.md` directly (1861 lines): its decisions run D-1 through D-32, with **no D-121 or D-122 entry anywhere** — `D-31` (line 1626) and `D-32` (line 1699) are the two highest-numbered real entries, and both are correctly cited elsewhere in this unit's coverage. Grepping the entire workspace for a `## D-121` or `## D-122` heading returns **zero matches anywhere**, including inside `evidence/DECISIONS.md` and this project's own AI-DLC `decisions.md` files. This project's own governance record already resolved this exact question: `governance/reviews/GOV-2026-08-21-UG-01.md` line 29 states plainly, *"D-122 confirmed in Vision §14.2, a register distinct from `evidence/DECISIONS.md`"* — D-121/D-122 are entries in the Vision document's own §14.2 decision register, not `evidence/DECISIONS.md`. This artifact's own body text gets it right in one place (§ SD-M-01, "**D-122's own status travels with them**: *'Approved — supervisor sign-off pending'*" tracks Vision §14.2's language) but its Sources line bundles D-121/D-122 with the genuinely-`evidence/DECISIONS.md`-sourced D-31 under one file path, misstating their provenance. Since `team.md` treats `evidence/DECISIONS.md` as the single authoritative decision log ("a decision is not real until it has a D-number" there), a reader taking the Sources line at face value would believe the frozen grid/seed values are recorded in the project's authoritative decision log when they are not — they sit in a document register this project's own prior governance pass explicitly called out as a *different* record. | Correct the Sources line in all three files to cite D-121/D-122 as `Vision §14.2` (not `evidence/DECISIONS.md`), keeping `D-31` under its correct `evidence/DECISIONS.md` citation, matching the precedent already set correctly elsewhere in this project (e.g. `security-requirements.md` line 95's own body prose, and `GOV-2026-08-21-UG-01`'s resolution). |

### Verified — resolved from the prior pass (independently re-derived, not read off the correction boxes)

- **Prior finding 1 ("strictly more coverage" overclaim), now WITHDRAWN.** Re-read § SD-M-01 top to bottom against `security-requirements.md` § SEC-M-01's actual wording (line-for-line: the `"locked_evaluation"` "is itself a finding" clause and the "included rather than filtered" language both match verbatim). Confirmed the two-limb distinction (attestation trigger vs. mechanical sequencing detection) is now stated explicitly, and independently confirmed it is swept to every site the correction claims: § SD-M-01's opening box (no residual "strictly more" language), the correction box itself, § SD-M-06's FR-P1-05-4 row (line 434, "⚠ But mechanism 3's OTHER limb is not replaced..."), § Assumptions (line 504), and in `logical-components.md` the C-3 entry (lines 145–153), the shared-resources row (line 211), the Mermaid edge label (line 79: `"narrows the attestation AND reinstates<br/>the dropped sequencing check"`) and its text fallback (line 87). No surviving un-narrowed "strictly more coverage" or "mere narrowing" claim was found by grep across either file.
- **Prior finding 2 (per-component distribution arithmetic), now corrected.** Recounted `logical-components.md`'s 14-row coverage table by component directly: C-1 → FR-P1-05-1, FR-P1-05-21, NFR-LEAK-01, NFR-IRI-01 (4); C-2 → FR-P1-05-2, NFR-DET-01, NFR-PHASE-01 (3); C-3 → FR-P1-04-14, FR-P1-05-3, -4, -5, -6, -22 (6); C-4 → NFR-AUD-01 (1). 4+3+6+1=14, matching both the file's printed "C-2: 3" (line 244) and the stated total. No stale "C-2: 4" survives outside the correction box that preserves it as a superseded quotation (line 246).

### Verified — did not break

- **Focus 1, Q1=C's core mechanics.** Re-read § SEC-M-01 (`security-requirements.md`) and confirmed § SD-M-01 quotes it accurately: the Q2=B block language ("does not proceed until a human attests"), the "worth without inflation" framing, and the verbatim residual sentence ("a choice informed by a December figure a human carries in their head leaves no trace") all match word-for-word. Q2=B ("the window BLOCKS") is not contradicted by Q1=C — Q1=C removes the *log-gated* form of the block and replaces it with an *unconditional* one, which is a strictly more frequent block, not a relaxation; a downstream reader cannot conclude the log becomes unnecessary, because § SD-M-01 states explicitly that a future log "narrows when an attestation is demanded," i.e. remains relevant. (The one qualification to this is Finding 1 above.)
- **Focus 2, the divergence claim.** Read the one exempted sibling file (`features-and-splits/nfr-design/security-design.md`) in full. § SD-F-01's actual reasoning is framed as "what would the artifact be" (contrasting `external-products`' skip-not-pass against `target-standardization`'s fail-closed, the latter because "its check guards a scientific artifact that would exist and be read"), which is the same substance § SD-M-01 paraphrases as "does the guarded object exist and get consumed." The paraphrase is not a literal quotation and none is claimed — it is presented as this unit's own restatement of the discriminator, and it is a faithful restatement. No inconsistency between the two units' answers: `features-and-splits` blocked because the guarded object (a trainable feature matrix) would be produced and consumed with no substitute check; this unit did not block because two of its three mechanisms are runnable and the third has a substitute (the attestation) that needs no missing artifact. Reasoned, not contradictory.
- **Focus 3, Q2=A's `criterion_hash` binding.** The raise condition is explicitly stated: "`attests_criterion_hash != criterion_hash` **raises**" (line 164), and the negative control ("An attestation whose `attests_criterion_hash` does not match the run's criterion **fails**") confirms it. The case of `attests_criterion_hash` present but `criterion_hash` absent from the run is not addressed, but `TuningRecord`'s own field group makes `criterion_hash` a required field of the run being attested to (it is what the attestation is *about*), so this is a vacuous edge case rather than a real gap — not raised as a finding.
- **Focus 4, W-12's five-step order and the precedence rule.** `business-logic-model.md` W-12's five steps (write DEC once; hash+stamp at a moment no metric exists; durably flush the receipt with `sha256`→`prediction_hash` column 18; refuse to exit if step 1 happened and 2–3 did not; only then may 07/bootstrap score) are restated verbatim in § SD-M-04's prose before the pseudocode. The pseudocode that follows is explicitly introduced as "What 3.2 left undefined, designed here" — an elaboration of *how* step 3's "durably flushed" and step 4's exit-refusal are implemented (temp-file write, fsync, atomic rename, registry append, conditional exit), not a redefinition of W-12's overall order; the two are consistent once read as different levels of granularity. The precedence rule (receipt file authoritative for hash, registry row authoritative for existence, disagreement raises) does not contradict anything W-12 says about `foundation` R-18 — W-12 states only that R-18 "owns that row" and "refuses a hash presented by the metric-computing process," which is compatible with the stated precedence. Option B's "removes the process boundary" characterization is fair: W-12 itself states the mechanism *is* "writer and reader in different processes, with a file and a registry row between them," and collapsing to registry-row-only removes exactly that.
- **Focus 5, Q4's positive probe.** Not circular: the design explicitly defers the probe's *subject operation* to pin-freeze and states the degradation path in the rule body, not just in Assumptions ("If no operation on the frozen pin is reliably nondeterministic, the probe degrades to option B, and that degradation is recorded"). `DeterminismError` **is** a declared exception — confirmed directly against `src/data/config.py`'s `__all__` (17 entries via `grep -n "__all__" -A 25`), which lists `DeterminismError` as entry 5 of 17 with a matching `class DeterminismError(IntegrityError)` definition. It is correctly absent from Derivation 2's "5 raised across W-1…W-12" set because it is not raised by any of the twelve functional-design workflows — it belongs to this stage's own new determinism-check design, not to the functional-design layer Derivation 2 audits, so its absence from that derivation is not a defect.
- **Focus 6, both coverage-table counts.** Recounted `security-design.md`'s 14-row table directly: FR-P1-04-14, FR-P1-05-1,2,3,4,5,6,21,22 (9) + NFR-DET-01, NFR-LEAK-01, NFR-IRI-01, NFR-AUD-01, NFR-PHASE-01 (5) = 14, confirmed. Verified the "13 ∪ {NFR-PHASE-01} = 14" arithmetic against both upstream tables: `security-requirements.md` genuinely carries 13 rows (9 FR + NFR-DET-01/LEAK-01/IRI-01/AUD-01), `tech-stack-decisions.md` genuinely carries 7 (FR-P1-05-1,2,5,6,22 + NFR-DET-01 + NFR-PHASE-01), and NFR-PHASE-01 is the only ID in the 7 absent from the 13 — confirmed by direct read of both files. `logical-components.md`'s total of 14 rows is correct; only its per-component breakdown is wrong (Finding 2).
- **Focus 7, Derivations 1–3.** Derivation 1 (ten files, zero present) verified directly against the live filesystem: `src/models/` holds only `__init__.py`, `scripts/` holds only the two pre-scaffold scripts, `configs/` is absent, no `python`/`py` interpreter is reachable — all confirmed by direct shell inspection, matching the artifact's SD-M-00 table exactly. Derivation 2 (5 exceptions raised, 0 owed against the 17-name `__all__`) verified: `src/data/config.py`'s `__all__` genuinely lists 17 names including all five of `PartitionError`, `LeakageError`, `SeedError`, `AlignmentError`, `LockedTestError`. Derivation 3 (`unit-of-work.md` § 8's nine IDs vs. the 13-row upstream table) verified directly against `unit-of-work.md` line 375: "Requirements carried (9). FR-P1-04-14, FR-P1-05-1, FR-P1-05-2, FR-P1-05-3, FR-P1-05-4, FR-P1-05-5, FR-P1-05-6, FR-P1-05-21, FR-P1-05-22" — exact match, all nine present in the 13, 0 owed. None of the three "0" derivations hides a skipped check.
- **Focus 8, overclaim sweep.** No sentence found in either artifact describing a mechanism as already enforcing (vs. designed to enforce), a row as closed, or a gate as satisfied. The FR-P1-05-4 coverage-table cell's "third clause now runnable" (Q1=C) is stated consistently in both `security-design.md` and `logical-components.md` (its C-3 entry: "Was blocked, now is not") with no stale "unrunnable" claim surviving in either construction-stage artifact (the upstream, terminal-READY `security-requirements.md` still says "UNRUNNABLE today," which is correct — it predates this stage's redesign and is not edited, per `project.md`'s never-edit-a-signed-record rule).
- **Focus 9, stale-figure sweep.** Numerals 14/13/7/9/10/5/17/6/4 and their spelled-out forms were checked at each site named in the dispatch; all are internally consistent across both artifacts and against the upstream tables, with the one exception being Finding 2's per-component distribution.
- **Focus 10, Mermaid validity.** The `graph TD` block's brackets and quotes are balanced; every node referenced in an edge (C1, C2, C3, C4, PIN, CFG, LOG, FND, RPT) is declared; the dashed `LOG -.->|"narrows later, does not enable"| C3` syntax is valid Mermaid; the text fallback names every edge the diagram draws, with no edge or node omitted or invented.
- **§ SD-M-06's FR-P1-05-4 row and the Q1=C interaction.** The updated row states "the third clause is now **runnable**: it no longer reads R-25's log, so BLK-07 narrows it later rather than blocking it" — consistent with § SD-M-01's design and with `logical-components.md`'s C-3 entry; no other passage in either artifact still describes this clause as unrunnable.
- **Sensor checks.** Both files carry well over two H2 headings (`required-sections`). Both files' prose references all six `consumes:` artifacts from the stage frontmatter (`performance-requirements`, `security-requirements`, `scalability-requirements`, `reliability-requirements`, `tech-stack-decisions`, `business-logic-model`) — the three absent-by-scope-design categories are explicitly named and assessed in § Scope note in both files (`upstream-coverage`).
- **Q1–Q5 answers and Consolidated Summary Confirmation.** Verified against `nfr-design-questions.md` directly: C, A, A, A, A and "Looks correct" — matches the dispatch brief exactly, and each answer's stated rationale in the questions file matches its restatement in both produced artifacts.
- **Cross-references into shared inception contracts.** `component-methods.md`'s `FeatureBundle`/`Prediction` (carrying `partition_id`/`transform_id`) and `services.md`'s `06_train_and_predict.py` read/write split and nine-script split are cited consistently with both artifacts' descriptions of the stamp-carrying and script-boundary mechanisms.

### Coverage limits

- Did not read any sibling unit's `construction/<other-unit>/` content beyond the one exempted file (`features-and-splits/nfr-design/security-design.md`); claims about `foundation`, `governance-guards`, `regimes-diagnostics-reporting`, and `evaluation-and-comparison` were checked only against this unit's own internal coherence, the one exempted file, and the shared inception contracts named in the dispatch, per the read-scope bound.
- Did not attempt to execute any script or test — confirmed directly that no Python interpreter is reachable in this environment, consistent with both artifacts' own disclosure.
- Did not verify every one of the roughly thirty cross-references in the Sources sections individually against `business-rules.md` R-90…R-102a; spot-checked R-90 and R-101 (both match their cited section headers exactly) rather than all thirteen rule IDs.
- Did not independently verify the BLK-07/R-25 cross-unit dependency's existence or shape beyond what `governance-guards`' own construction artifacts are stated to contain in the shared contracts and in the prior `security-requirements.md` review pass — `governance-guards`' construction directory is outside this unit's read-scope and was not the exempted sibling file.
- Did not re-derive `logical-components.md`'s "7 across 5 units" / test-module-adjacent open items beyond what the artifact itself already flags and routes to the gate.
- Verified `evidence/DECISIONS.md` (repo root, in-scope, not a sibling unit's construction content) directly and in full for D-121/D-122; did not open the PreFlight Vision document itself to confirm §14.2's register content, relying instead on this project's own governance record (`GOV-2026-08-21-UG-01`) which already resolved D-121/D-122's actual home as "Vision §14.2, a register distinct from `evidence/DECISIONS.md`" — a coverage limit on independent confirmation of Vision §14.2's exact content, not on the misattribution finding itself, which rests on the negative result (no D-121/D-122 heading anywhere in the workspace, confirmed by full-repository grep).
- Did not independently verify whether `functional-design/domain-entities.md` is writable at this point in the workflow (i.e., whether it counts as a "signed record" under `project.md`'s never-edit-a-signed-record rule) — Finding 1's recommendation offers the Assumptions-note alternative for that reason.
- This pass found two new Major findings not raised by the prior pass; combined with the two prior Majors verified fixed, this is four Major findings raised against this unit across its full review history, none open at once. No circular dependency, and no `## NO ROW` / satisfaction overclaim, was found in either artifact.

---

## Receipt-floor note — 2026-09-04 (re-saved after the second re-affirmation)

*A second redo jump was taken because the first recovery ran confirm/write/review out of
order, wedging the engine against its own write-freeze. The steps were re-run as confirm →
write → review. **Both fixes below are unchanged by that**; only the receipts moved.*

**This is one of the two units the redo jump was taken for.** The prior pass's two Majors are
both fixed on the project decision owner's direction. Because a terminal review receipt freezes
a `produces[]` artifact, the fix required a **redo jump** to clear this stage's receipt floor,
which invalidated every unit's receipts rather than only this one's.

**What changed, and where:**

- **§ SD-M-01** — *"strictly more coverage than the window ever gave"* is **WITHDRAWN**, in a
  correction box that preserves the superseded claim. Mechanism 3 is now stated as having
  carried **two** limbs: the attestation trigger (replaced and widened) and a **purely
  mechanical `locked_evaluation` sequencing detection** with no human-memory component, which
  the unconditional attestation **cannot** perform and which is therefore **unavailable today
  with no substitute**. It is **reinstated as an additional check** when R-25's log lands, so
  **BLK-07 is not a mere narrowing**. Swept to every representation: § SD-M-01's opening, the
  correction box, § SD-M-06's FR-P1-05-4 control row, § Assumptions, and in
  `logical-components.md` the C-3 entry, the shared-resources row, the Mermaid edge label and
  its text fallback.
- **`logical-components.md`** — the per-component distribution's `C-2: 4` corrected to
  **`C-2: 3`**, now derived by grepping the table's own rows, with `4 + 3 + 6 + 1 = 14` printed.
  The total had been right, which is exactly what concealed the component error.

**Nothing else changed**, and the summary was re-affirmed by the owner on 2026-09-04 (its
stored value was already `Looks correct`). Every other claim, count and open item above stands
as recorded — the pin still `TBD — freeze gate` and blocking, BLK-03 open, seven acceptance
rows proposed and unapproved, no model ever trained.

## Review — 2026-09-04 confirming pass (fourth floor)

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-04T22:26:10Z
**Iteration:** 1 (fresh receipt floor — third stage-wide reset)

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | § Sources line 48; § Assumptions line 525; `logical-components.md` line 275 | **D-122's sign-off status is quoted as pending, but Vision §14.2's own row states it is closed.** All three sites assert or quote *"Approved — supervisor sign-off pending"* / *"owes a supervisor signature at G-05"*. Read `PreFlight/vision_document(3)(2)(2).md` §14.2 directly (line 1207): D-122's status column reads **"Approved; supervisor sign-off closed 2026-08-22 by the project owner under the recorded student/supervisor authority equivalence (`CR-2026-08-22-TE-AMEND`; `GOV-2026-08-22-REM-01` Rec 4). No supervisor signature artifact exists and none is claimed."** The register this unit cites as the fix's own source for D-122 does not say "pending" anywhere in its current text — that status was closed under a recorded authority-equivalence mechanism over two weeks before this pass, and the artifact's own Sources line (the very line this floor's fix 2 rewrote) introduces a fresh misquotation of the register it now correctly attributes. | Correct all three sites to state D-122's sign-off is closed under the recorded student/supervisor authority equivalence (no supervisor signature artifact exists, none is claimed), citing Vision §14.2 line 1207 directly, or — if the project disputes that this authority-equivalence closure satisfies "supervisor signature" for this unit's purposes — state that distinction explicitly rather than silently reasserting "pending." |

### Verified — fix 1 (attestation field group)

- Read `functional-design/domain-entities.md` § 5 `TuningRecord` directly and counted its attribute table row by row: `run_id`, `partitions_read`, `criterion_declared_at`, `criterion_hash`, `criterion_used_hash`, `run_at`, `audit_access_since_declaration` — **exactly seven fields**, none of them `attested_by`, `attested_at_utc`, or `attests_criterion_hash`. The three attestation fields genuinely do not exist on the owning definition.
- Confirmed the correction box at § SD-M-01 (lines 194–202) states the three fields are an **owed, change-control-gated entity amendment**, that Q2=A is a proposal to that gate, and that no implementation may add the fields before the owning definition is amended — matching the claimed fix exactly.
- Confirmed `logical-components.md`'s C-3 entry (lines 137–140) carries the matching inline note ("the three attestation fields are an **owed, change-control-gated amendment**... which does [not exist on the frozen definition]").
- No other live passage in either artifact implies the three fields already exist on the approved shape; every reference to them is now framed as owed/proposed.

### Verified — fix 2 (D-121/D-122 attribution split)

- Read `evidence/DECISIONS.md` in full: 33 `## D-` headings, running D-1 through D-32 (plus a D-1 addendum) — **no D-121 or D-122 entry anywhere**, confirming the split's premise.
- Confirmed the Sources line (line 47) now cites **D-31 alone** to `evidence/DECISIONS.md`, with a dated correction box noting the prior misattribution and that upstream `nfr-requirements` carries the same error, routed to the gate rather than edited.
- Confirmed a new Sources line (line 48) cites **Vision §14.2's own decision register**, stated as "distinct from `evidence/DECISIONS.md`," for D-121/D-122.
- Read `PreFlight/vision_document(3)(2)(2).md` §14.2 directly: D-121 (line 1206, "Exact frozen grids: ridge 6, RF 18, LSTM 16 combinations... Approved") and D-122 (line 1207) are genuinely present in that register, confirming the register itself is real and correctly located. The split's file-attribution claim is correct — but see Finding 1 above: the same line that now correctly attributes the register misquotes what the register currently says about D-122's status.

### Verified — did not break

- **C-2 per-component distribution.** Recounted `logical-components.md`'s printed distribution directly: C-1: 4, C-2: 3, C-3: 6, C-4: 1 → 4+3+6+1=14, matching the stated total; the superseded `C-2: 4` survives only inside its own correction box (lines 249, 295–296) as a preserved quotation, not as live text.
- **"Strictly more coverage" withdrawal, swept.** Grepped both artifacts for "strictly more" / "WITHDRAWN": found only inside the correction box and its cross-references at all seven claimed sites — § SD-M-01 opening/box, § SD-M-06's FR-P1-05-4 row, § Assumptions, and in `logical-components.md` the C-3 entry, shared-resources row, Mermaid label, and text fallback (per line 305's own cross-reference). No un-narrowed "strictly more coverage" claim survives.
- **Regression sweep.** `TensorFlow pin` still stated as `TBD — freeze gate` and blocking (both artifacts, multiple sites); **BLK-03** still open and independently barring implementation (both artifacts); nine `⚠ NO ROW`/`NO ACCEPTANCE ROW` markers present in `security-design.md`'s coverage table and cross-referenced text, consistent with "7 of 9 requirements have no acceptance row"; "**No model has ever been trained**" / "No model has ever been trained. No runtime, no peak memory..." still stated verbatim in both artifacts. No claim of satisfaction, discharge, or a filled `TBD` field was found anywhere in either artifact.

### Coverage limits

- Did not open any sibling unit's `construction/<other-unit>/` content; the D-121/D-122 misattribution's cross-reference to `foundation`'s artifacts (which share the same pattern per the finding table at line 542) was noted from this unit's own artifact text, not independently re-verified inside `foundation`'s directory.
- Verified `evidence/DECISIONS.md` and `PreFlight/vision_document(3)(2)(2).md` directly and in full for the relevant sections; did not re-read the entire Vision document end to end.
- Did not re-verify every cross-reference in § Sources beyond the two this floor's fixes touched (D-31/D-121/D-122) and the attestation-field group; the remaining ~28 citations were not re-checked on this pass, consistent with the tightened scope of a confirming pass.
- Did not evaluate whether Finding 1's "sign-off closed" reading is itself the correct one for this unit's purposes to adopt (e.g., whether the authority-equivalence mechanism actually substitutes for what `project.md`'s "Approved; supervisor sign-off pending" language originally meant to gate at G-05) — that is a question for the human/governance layer, not resolvable by text comparison alone; the finding is that the artifact's current wording does not match its own newly-correct citation target, not a ruling on which status is scientifically correct.

## Review — 2026-09-04 iteration 2 (D-122 repair verification, final)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-04T23:04:12Z
**Iteration:** 2 (final — budget 2)

### Findings

None.

### Verified — did not break

- **All four repair sites, checked verbatim against `PreFlight/vision_document(3)(2)(2).md` §14.2 line 1207.** Read the source row directly: *"Approved; supervisor sign-off closed 2026-08-22 by the project owner under the recorded student/supervisor authority equivalence (`CR-2026-08-22-TE-AMEND`; `GOV-2026-08-22-REM-01` Rec 4). No supervisor signature artifact exists and none is claimed. Seed values unchanged — verified against this row and TE §12's `configs/seeds.yaml` description before closure."* Confirmed each site's quote/paraphrase against this text: § Sources line 48 (exact quotation, matches word-for-word), § SD-M-01 rule body lines 219–222 (exact quotation), § Assumptions line 531 (accurate paraphrase — "closed 2026-08-22 by the project owner under the recorded authority equivalence, with no supervisor signature artifact existing and none claimed"), `logical-components.md` line 275 (accurate paraphrase, same substance). No site asserts "pending" or "owes a signature" as current status.
- **Superseded text preserved at all four sites**, each in a dated parenthetical distinguishable from live text: Sources line 48 ("superseded quote preserved: 'Approved — supervisor sign-off pending' — stale since 2026-08-22, carried here from upstream `nfr-requirements`, which still quotes it and stays unedited under its frozen receipt"); SD-M-01 body lines 223–224 ("superseded: 'Approved — supervisor sign-off pending … still owes a signature at G-05'"); Assumptions line 531 ("The superseded carried line ... is preserved here"); `logical-components.md` line 275 ("superseded carried line preserved: 'owes a supervisor signature at G-05'"). Each attributes the stale wording to upstream `nfr-requirements`, which stays unedited under its own frozen receipt — consistent with `project.md`'s never-edit-a-signed-record rule and with the routing (not editing) of upstream artifacts stated at Sources line 47's D-31 correction box.
- **No site declares the G-05 obligation discharged.** All four explicitly route the governance question — whether the authority-equivalence closure satisfies what "supervisor sign-off" was to gate at G-05 — to the human/governance layer rather than deciding it: Sources line 48 ("is a governance question routed to the gate, not resolved here"), SD-M-01 body line 225 ("is routed to the gate, not decided here"), Assumptions line 531 ("is a governance question routed to the gate"), `logical-components.md` line 275 ("routed to the gate — see `security-design.md`'s matching correction"). Each also restates, unchanged, that the grid hash must still be committed before G-05.
- **Regression grep clean.** Grepped both artifacts for "sign-off pending" and "owes a supervisor signature"/"owes a signature": every live hit sits inside one of the four repaired parentheticals (correctly attributed as the superseded/upstream quote) or inside the prior Review sections' own Finding-1 text (historical record of what the finding found, not a live claim). No un-parenthesized site asserts "pending" as current status.
- **C-2 per-component distribution unchanged.** `logical-components.md` line 246: `C-1: 4, C-2: 3, C-3: 6, C-4: 1`, total 14 — matches the fix verified at the prior floor; superseded `C-2: 4` survives only inside its own correction box (lines 249, 295–296).
- **Split D-31 / Vision-§14.2 Sources lines unchanged.** Line 47 cites `evidence/DECISIONS.md` for D-31 alone (with the D-121/D-122 misattribution correction box); line 48 cites "Vision §14.2's own decision register" for D-121/D-122 as "distinct from `evidence/DECISIONS.md`" — both lines present and correctly separated, as verified at the prior floor.
- **Attestation owed-amendment note unchanged.** § SD-M-01 (lines 180–191 area) and `logical-components.md`'s C-3 entry still frame the three attestation fields as an owed, change-control-gated entity amendment not yet reflected in `domain-entities.md` § 5 — grepped for `attested_by`/`attests_criterion_hash`; no new claim that the fields already exist on the approved entity shape.
- **"Strictly more coverage" withdrawal box unchanged.** Grepped both artifacts: the WITHDRAWN language and its two-limb (attestation trigger vs. mechanical sequencing detection) explanation remain at all seven previously-swept sites in both files; no un-narrowed "strictly more coverage" claim resurfaced.
- **Overclaim sweep on the four reworded sites.** None of the four asserts a mechanism as enforcing rather than designed, a row as closed, or a test/gate as passed; each explicitly states "unchanged" for the grid-hash-before-G-05 obligation and none upgrades D-122's status beyond what Vision §14.2's row itself states.

### Coverage limits

- Verified `PreFlight/vision_document(3)(2)(2).md` §14.2 directly (lines 1195–1214) for D-121/D-122's row text; did not re-read the entire Vision document end to end.
- Did not open any sibling unit's `construction/<other-unit>/` content; this pass's scope was the four named D-122 repair sites plus the named unchanged-items list, not a full re-review of either artifact.
- Did not re-verify the roughly thirty other Sources cross-references, the Mermaid diagram, or the requirement-coverage table beyond the spot-checks listed above — those were fully verified at the prior floor and are outside this iteration's scope.
- This is the final iteration at this budget (2); no further review pass will run against this artifact at this stage.

## Review — 2026-09-05 re-affirmation (post-gate receipt refresh)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T08:18:45Z
**Iteration:** re-affirmation (fresh receipt after a stage-gate rejection that revised `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`, and `fixtures-and-reproducibility`; this unit's artifacts were not part of that revision)

### Prior terminal review, quoted

`## Review — 2026-09-04 iteration 2 (D-122 repair verification, final)` — **Verdict: READY**,
**Date: 2026-09-04T23:04:12Z**, **Iteration: 2 (final — budget 2)**, **Findings: None**.

### Confirmed no edits since that review

Both artifacts (`security-design.md`, `logical-components.md`) end their live content at the
iteration-2 review block quoted above; no content follows it apart from this new section. The
gate-triggering revision named in this pass's dispatch touched only `evaluation-and-comparison`,
`statistical-inference`, `regimes-diagnostics-reporting`, and `fixtures-and-reproducibility` —
four sibling units, none of them this one. Nothing in this unit's two artifacts was altered
between the prior terminal receipt and this pass.

### Spot-checks of the prior pass's verified claims (re-derived independently, not read off the correction boxes)

- **Attestation fields still absent from the owning entity.** Read `functional-design/domain-entities.md` § 5 `TuningRecord` directly: seven attributes (`run_id`, `partitions_read`, `criterion_declared_at`, `criterion_hash`, `criterion_used_hash`, `run_at`, `audit_access_since_declaration`) — still none of `attested_by`, `attested_at_utc`, `attests_criterion_hash`. The correction box's "owed, change-control-gated amendment" framing in both artifacts still holds.
- **D-122's status still matches its cited source verbatim.** Read `PreFlight/vision_document(3)(2)(2).md` line 1207 directly: *"Approved; supervisor sign-off closed 2026-08-22 by the project owner under the recorded student/supervisor authority equivalence (`CR-2026-08-22-TE-AMEND`; `GOV-2026-08-22-REM-01` Rec 4). No supervisor signature artifact exists and none is claimed."* This still matches § SD-M-01's quotation and the Sources line (line 48) word for word; no site reasserts "pending."
- **`logical-components.md`'s per-component arithmetic still correct.** C-1: 4, C-2: 3, C-3: 6, C-4: 1 → 14, matching the printed total and the identical 14-ID set in `security-design.md`'s own coverage table.

No drift, no new contradiction, and no claim of satisfaction, discharge, or a filled `TBD` field was introduced. The standing verdict is re-affirmed unchanged.

READY
