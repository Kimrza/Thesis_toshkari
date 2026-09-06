# NFR Design — Questions — `features-and-splits`

**Unit** `features-and-splits` (Bolt 7) · **Kind** `library` · **Stage** `nfr-design`

Two artifacts only — `security-design.md` and `logical-components.md`. `produces_kinds` maps
`performance-design`, `scalability-design` and `reliability-design` to `[service]` /
`[service, ui]`, and this unit is `library`.

**Nothing below decides a scientific value.** TE §18.2's absolute rule stands. The lags are
D-10.3's, the window length is a frozen 24, the folds are exact calendar boundaries, and the
`train_start`/`train_end` values are `configs/data.yaml` content. No question here fills a
`TBD — freeze gate` field, approves an acceptance row, or closes a blocker.

**BLK-04, BLK-08 and BLK-09 are open exit conditions on this unit.** Answering these questions
does not close any of them, and **no implementation is authorised** while BLK-04 stands.

---

> ## ⚠ WORKSPACE STATE VERIFIED 2026-09-04 — THREE UPSTREAM CLAIMS CHECKED, ONE IS STALE
>
> | Upstream claim | Verified state, 2026-09-04 |
> |---|---|
> | W-10: *"`src/features/availability.py`, `build.py`, `transforms.py`, `windows.py`, `src/data/splits.py`, `scripts/05_build_features_and_splits.py` and all **six** test modules DO NOT EXIST"* | **Holds for the modules; STALE for one test.** `src/features/` holds `__init__.py` only; `src/data/` holds `config.py`, `locked_test.py`, `release.py` — no `splits.py`. `scripts/` holds only `audit_ec1_drivers.py` and `merge_coverage_year.py`. But **`tests/test_locked_test_guard.py` EXISTS** — see Question 3. |
> | `nfr-requirements` banner: *"no Python interpreter exists in this environment, so every test is written-but-unexecuted"* | **Conclusion holds; one detail is now different.** No interpreter is reachable today (`python` resolves to the zero-byte Windows Store stub; `py` launcher absent), so nothing can be executed. `src/data/__pycache__/config.cpython-314.pyc` shows a **3.14** interpreter ran here at some point — **not** the governed 3.11 pin (TE §8.1, TC-03d), so no execution it performed would be governed evidence either way. |
> | `configs/` does not exist | **Holds.** So every `configs/data.yaml` / `features.yaml` / `experiment.yaml` read this design specifies is a read against a file that is not there. |
>
> **Nothing this unit designs is built.** Every question below is about what to build.

## Derivations printed before they are asserted

`project.md` § Way of Working fixes that a count is derived from the artifact and printed, and
that two artifacts which should agree are reconciled by **set-differencing their ID lists**,
never by comparing totals. Three derivations were run **before** these questions were written,
because this stage's own diary records that deriving them afterwards means the owner is asked
about a scope that misdescribes the work.

**Derivation 1 — the six test modules this unit owns, against `tests/` on disk.** Owned set
(W-10, R-76a): `test_feature_availability.py`, `test_iri_denial.py`, `test_split_embargo.py`,
`test_train_only_transforms.py`, `test_locked_test_guard.py`,
`test_feature_leakage_guards.py` — **6**. On disk: **6** files, none of them the same set.
Intersection: **1** — `test_locked_test_guard.py`. Owned and absent: **5**. This is
Question 3.

**Derivation 2 — the exceptions this unit raises, against their declaration site.** Raised
across W-1…W-6: `LeakageError`, `AlignmentError`, `PartitionError`, `LockedTestError` — **4**.
`src/data/config.py`'s `__all__` declares **17**. Set-difference (raised, not declared):
**0**. Nothing is owed here — recorded because the same derivation found **3** missing at
`inventory-and-registry` and **5** at `external-products`, so a zero is a result, not a
skipped check.

**Derivation 3 — this unit's requirement IDs, against the upstream coverage table.**
`unit-of-work.md` § 7 carries **11**: FR-P1-04-1, -2, -5, -6, -8, -10, -12, -13, -16,
NFR-IRI-01, NFR-LEAK-01. `nfr-requirements`' `security-requirements.md` carries **13** rows.
Set-difference, both directions:

- **In the 11, absent from the 13: FR-P1-04-2, FR-P1-04-5, FR-P1-04-8** — `grep -c` returns
  **0** for each across both `nfr-requirements` artifacts.
- In the 13, not in the 11: FR-P1-04-7, FR-P1-04-17, NFR-FAIR-01, NFR-TDEF-01, FR-P1-03-3 —
  **5**, every one a legitimate later addition (`CR-2026-08-22-LEAKAGE-TA`, R-76a's cross-unit
  assignment, the NFR-TDEF-01 repair of 2026-09-01).

**The three absent IDs are implemented verbatim upstream and cited nowhere.** FR-P1-04-2 is
SEC-F-02's lag rule word for word (its acceptance rows **WS-11, TA-08**); FR-P1-04-5 is
SEC-F-03's fold-and-embargo rule (**WS-12, TA-11**); FR-P1-04-8 is SEC-F-03's
one-window-two-representations rule (**WS-13, TA-11**). This is the **same defect class** as
the two Major findings already recorded against this unit — substance implemented, requirement
ID missing from every coverage table — and it is the third recurrence. **This stage's coverage
table carries 16 rows** (13 + 3), with the three labelled as added here so they do not read as
inherited. **Adding a citation claims an obligation, never a discharge.**

---

## Question 1

§ SEC-F-01's provenance check is this unit's answer to the one leakage channel that survives
both existing controls: a value **computed from IRI**, **renamed** to a legitimate §6.2 field,
and written into the feature path — it passes R-76's name closure, passes
`tests/test_iri_denial.py`, and passes `external-products`' import boundary.

The check **cannot run today**. It needs a **permitted-producer list per §6.2 dictionary row**,
and TS-F-01 states plainly that the list **does not exist**, is **not created at 3.1 or 3.2**,
and — sharpened by the reviewer's third channel — must be keyed per **(row, producer)** pair
rather than per producer.

So the design must say what `build_features` does while that list is unset.

A. **Fail closed — `build_features` raises and names the unset list, so no feature matrix is
   produced at all**
   > **Impact**: The strongest reading of this unit's own stated posture — *"it would rather produce nothing than produce a matrix that might leak"* — and it matches TE §18.3's stop-and-report rule directly. Nothing downstream can train on a matrix whose provenance was never checkable, because nothing downstream gets one. It blocks the entire unit until the list is authored, which is a real schedule cost that should be visible now rather than discovered at 3.5.

B. **Produce the matrix, skip the provenance limb with a machine-readable reason, and let the
   §18.3 preflight read the skip as unmet**
   > **Impact**: Work proceeds and the gate still refuses. It is the pattern `external-products` adopted for its containment check — but that check guards **code that does not exist**, whereas this one would guard **a feature matrix that exists on disk and gets trained on**. A file gets read by whoever needs it; a skip recorded on a gate report does not travel with it. This is precisely the contrast `target-standardization` drew when it chose fail-closed for the same reason.

C. **Run the name-closure limb, skip only the provenance resolution, and stamp the emitted
   bundle `provenance_unverified`**
   > **Impact**: Keeps the checks that can run, and the stamp travels **with the data** in `spec.json` rather than on a report — which is a genuine improvement on B's weakness. It still emits a trainable matrix whose one uncheckable property is the one that closes the rename channel, and it adds a bundle field whose absence in an older bundle would be indistinguishable from a verified one unless the field is required.

D. **Defer to 3.5**, as TS-F-01 already deferred the carrier question
   > **Impact**: Nothing is decided against a list that does not exist. It is the second deferral of the same dependency, and it leaves a stop-and-report point for `code-generation` to resolve — which is the one decision §18.3 says an agent may not make.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the artifact test decides it, and this project has already
> ruled the same way on the same test. `external-products` could skip because a missing module
> consumes nothing; here the emitted object is **the last artifact before training**, and every
> reported number inherits it. B's failure mode is concrete and silent: a full-year matrix on
> disk with an unverifiable column is trained on, and the resulting metric looks like a
> measurement. C is the best of the weaker options and worth taking **only** if the
> `provenance_unverified` field is made **required** on every bundle, so its absence raises
> rather than reads as clean. **A's cost is stated rather than hidden: this unit produces
> nothing until the permitted-producer list is authored and frozen, and that list is not this
> stage's to write.**

[Answer]: A

---

## Question 2

If per-column provenance is stamped, it needs a carrier. TS-F-01 deferred this to 3.5 and named
the constraint honestly: Parquet **field-level** metadata survives a `pyarrow` round-trip but is
*"easy to drop through an intermediate `pandas` operation that rebuilds the frame"*, which would
make the check *"fail for the wrong reason, or worse, pass on stamps silently regenerated as
blank."*

ADR-11 changes what is available. A `FeatureBundle` is already persisted as a directory —
`matrix.parquet`, `tensor.npy`, `spec.json` — where **loading reads all three or raises**, and a
directory name disagreeing with its `spec.json` **raises on load**. `target-standardization`
answered the analogous question with **a column**, because its caveat is per-**row**; provenance
here is per-**column**, so a column cannot carry it.

Where do the per-column provenance stamps live?

A. **In `spec.json`**, as a column-keyed map alongside the bundle's existing identity fields
   > **Impact**: Reuses the one carrier ADR-11 already makes read-or-raise, so a dropped stamp becomes a **load failure** rather than a silent blank — the exact hazard TS-F-01 names, closed by a mechanism that already exists. It puts a per-column fact in the object that carries the bundle's identity, which is where `FeatureBundle`'s own design says the stamp *"cannot drift from the data the way a side-car manifest can."* Cost: `spec.json` grows one entry per column, and a column added without its entry must raise rather than default.

B. **Parquet field-level metadata on `matrix.parquet`**
   > **Impact**: Semantically the closest fit — a property of the column, stored on the column — and costs nothing extra. It is the carrier TS-F-01 itself flags as droppable, and the tensor half of the bundle has no field metadata at all, so the stamps would exist for one representation and not the other. That asymmetry is exactly what WS-13 exists to catch.

C. **A separate companion manifest file in the bundle directory**
   > **Impact**: Keeps provenance out of the identity object, which some readers will find cleaner, and a fourth file is trivially added to the read-all-three-or-raise rule. It is a side-car by construction — the thing `FeatureBundle`'s design chose against by name — and a bundle written by an older path would simply lack it.

D. **Both `spec.json` and field metadata, `spec.json` authoritative**
   > **Impact**: The bundle stays self-describing to someone who opens `matrix.parquet` directly, and the guarantee lives in the read-or-raise carrier. Two places to keep in step, and a divergence needs its own rule about which wins — which is a new failure mode, not a safeguard, unless the precedence is stated as a raise.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the requirement is that a bad stamp **fails**, and only the
> read-or-raise carrier makes that true against the operations the pipeline actually performs.
> B is the better model of the world and the worse guarantee, the same trade
> `target-standardization` rejected. D is defensible and should be taken only with an explicit
> rule that a disagreement **raises** rather than resolving to `spec.json` silently. Whichever
> is chosen, the stamps are **additional to** `phase_id` / `source_id` /
> `target_definition_id`, which the mandated rule requires on the matrix and on every mask
> regardless.

[Answer]: A

---

## Question 3

**Derivation 1's finding, stated as the question it raises.** `tests/test_locked_test_guard.py`
**exists on disk**, and W-6 records it as **this unit's** module, on the stated ground that it
*"exercises both limbs"* — this unit's pre-G-05 **execution** block on
`materialise_locked_partition`, and `governance-guards`' **read** chokepoint through
`open_restricted` — and that assigning it to `governance-guards` *"would close a cycle."*

The module on disk does not do that. Its own docstring scopes it to the read chokepoint —
*"`open_restricted` writes a durable `AccessRecord` before the read"*, bypass refusal, a failed
log write aborting the read, after-the-fact verifiability — and states *"No December target
value is read, parsed, counted or computed anywhere in this module."* **W-6's limb 1 is not in
it.** The file exists, the claim that this unit owns it is on paper, and the half this unit owes
is unwritten.

`materialise_locked_partition` does not exist either, so nothing is broken today. What is at
stake is where its guard test goes — and §12's mandated `tests/` tree names
`test_locked_test_guard.py`, not a second module.

A. **Extend the existing module in place** with this unit's limb-1 cases, keeping one file and
   §12's name
   > **Impact**: Honours §12's mandated tree exactly and keeps W-6's "both limbs, one module" reading true once the cases are added. One file then carries tests owned by two units, so a `governance-guards` change and a `features-and-splits` change touch the same module — and the existing file's Governance block cites only `governance-guards` R-25/R-28, so the ownership split has to be stated inside the file or it will read as one unit's.

B. **Add a second module** — `tests/test_locked_partition_guard.py` — for limb 1, and narrow
   W-6's claim to limb 2
   > **Impact**: Clean ownership: each unit's module is its own, and neither unit's change touches the other's file. It adds a test module **not named in §12's tree**, which is a change to the mandated set — the same class of act as `CR-2026-08-22-LEAKAGE-TA` — so it needs the owner's approval rather than this stage's, and the story map's TA-18 attribution would need to name both files.

C. **Extend in place, and record the two-unit ownership as an explicit block in the module's
   own docstring** plus a row in this unit's coverage table
   > **Impact**: Option A with its one real weakness closed: the file says which cases belong to which unit and which rules govern each, so a later reader does not attribute limb 1 to `governance-guards`. It is the most writing for the least new structure, and it still leaves two units editing one file.

D. **Record the contradiction and route it to the gate without designing the placement**
   > **Impact**: Takes no decision that belongs to the owner, and the finding is disclosed rather than buried. It leaves 3.5 to place a mandated test module, and this unit's own diary records that naming a defect in an instruction to someone else is not the same act as resolving it.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C — it keeps §12's mandated tree untouched, which is the only
> option that needs no change record, and it fixes the one thing that makes A risky. B is the
> better design in isolation and costs an owner-approved addition to the mandated test set for a
> benefit that is organisational rather than evidentiary; if you would rather have clean
> ownership than an untouched §12 tree, B is the right answer and should be routed as a change
> record, not applied here. **Either way the substantive gap is unchanged and is not closed by
> this answer: limb 1 is unwritten, and `materialise_locked_partition` does not exist.**

[Answer]: C

---

## Question 4

**WS-13's evidence question is open, and three artifacts decline to settle it.** R-81 states
*"one window definition, two representations"* and records that what evidence proves the matrix
and the tensor encode the same window is **not settled**; TS-F-03 adds that no tooling choice
settles it; the story map adopts no reading.

ADR-11 changed the ground under the question. Both representations now travel in **one**
`FeatureBundle` built by **one** producer from **one** window definition, which
`component-methods.md` says makes FR-P1-04-8's parity *"structural rather than asserted"*. But
W-4 also records the fact that makes a structural argument insufficient on its own: **the
tensor carries no record timestamps**, so no row-level check can reach it.

What evidence discharges WS-13 / FR-P1-04-8?

A. **A value-level parity test on the fixture** — reconstruct the flattened matrix rows from the
   tensor's slices and assert element-wise equality within the fixture manifest's declared
   floating-point tolerance
   > **Impact**: Tests the property the requirement actually states ("contain the same underlying window values") rather than the construction that is supposed to guarantee it, and it is the only option that would catch a defect in `windows.py` itself. It needs the fixture manifest's tolerance, which `team.md` fixes as fixture-manifest content and which is **unset** — so the test is designed now and unrunnable until that value is frozen, a dependency to state rather than assume.

B. **The structural argument alone** — one producer, one window definition, one bundle;
   no assertion
   > **Impact**: Costs nothing and is what `component-methods.md` already claims. This unit's own W-3 is the standing counter-example: an interface was claimed to make a leak *"unrepresentable"* and did not, and this stage has recorded that lesson three times. A structural guarantee with no check is exactly the shape that failed there.

C. **A shape-and-ordering assertion** — assert the tensor's dimensions, step count and column
   order against the matrix's, without comparing values
   > **Impact**: Cheap, needs no tolerance, and catches the most likely mechanical defect (a transposed or misordered window). It passes a tensor whose shape is right and whose values came from the wrong rows, which is the failure a matched-window assertion is for.

D. **Defer to 3.5**, as R-81 and TS-F-03 both did
   > **Impact**: Nothing is designed against a module that does not exist. It is the third deferral of the same question, and it leaves TA-11's evidence for `test_common_masks.py` resting on a parity claim nobody has designed a check for.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A, with C as its cheap precondition rather than its
> alternative — assert shape and ordering first so a value comparison that fails is
> interpretable, then compare values. The tolerance dependency is real and should be recorded as
> **owed to the fixture manifest**, not filled here: `team.md` fixes that fixture assertion data
> lives in `tests/fixtures/<fixture_id>/fixture_manifest.yaml` and TE §15.1 fixes that
> tolerances are **measured and frozen, never invented**. **This proposes a check; it does not
> adopt a reading of TE §16's WS-13 criterion, which stays open.**

[Answer]: A

---

## Question 5

`logical-components.md` needs a boundary criterion. The six sibling units each chose a different
axis and said why: `foundation` **write-integrity**; `governance-guards` **enforcement timing**;
`acquisition` **egress direction**; `inventory-and-registry` **how a failure reaches a human**;
`external-products` **what the component keeps out**; `target-standardization` **what each
component makes true about the target**.

This unit is the **last boundary before training**, and it both **builds artifacts** (the
availability record, the `FeatureBundle`, the `Partition` set) and **guards** them. Its failures
are not alike: most raise, and one — a full-dataset fit — *"produces better validation numbers
and raises nothing anywhere."*

What criterion should the decomposition use?

A. **By the object whose integrity each component guarantees** — four components: the
   **availability record** (W-1, the three lag limbs and the anchor recomputation); the
   **feature bundle** (W-2, W-4, dictionary closure, provenance, the two representations); the
   **partition set** (W-5, W-8, W-9, folds, embargo, both bounds, the two carry-forward rules);
   the **fitting identity** (W-3, W-6, the transform-to-partition match and the locked
   partition's guard)
   > **Impact**: Names what an implementer builds and what a reviewer opens, and each component maps to a distinct artifact with a distinct schema. It groups W-3's transform identity with W-6's lock because both are identity checks on a persisted stamp, which needs saying since one is a leakage control and the other an access control. Its weakness: the silent failure and the loud ones end up inside the same box (the fitting identity), so the visibility distinction has to be carried in § Failure domains rather than by the boundary itself.

B. **By whether the failure is loud or silent** — the raising boundary versus the
   silently-biased fit
   > **Impact**: Isolates the one failure that reaches the thesis undetected, which is the most consequential fact about this unit. It is `inventory-and-registry`'s axis already, and two components is a distinction rather than a decomposition — W-1, W-2, W-5 and W-8 would share one box despite guarding unrelated properties with unrelated schemas.

C. **By leakage channel closed** — one component per channel: the lag, the dictionary, the
   provenance, the transform identity, the window, the split, the lock
   > **Impact**: Maps one-to-one onto the requirements and the negative controls, so the coverage table writes itself and no channel can be silently merged into another. Seven components for one `library` unit is finer than any sibling's decomposition, and several would share a single module (`src/features/build.py`), so the boundaries would not correspond to anything an implementer can isolate or test independently.
D. **By workflow grouping** (W-1/W-2 | W-3/W-4 | W-5/W-6 | W-7…W-10)
   > **Impact**: Traceable straight back to `functional-design` and trivial to verify. It pairs W-5 (folds) with W-6 (the lock) on adjacency alone, and separates W-2's dictionary closure from W-7's IRI denial, which are two limbs of the same channel.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the useful question about a unit that both builds and guards
> is *which object is at stake*, because that is what a failure damages, what a test loads, and
> what a downstream consumer refuses. It also puts the four persisted artifacts of this unit in
> four boxes, which is what `infrastructure-design` and `code-generation` need next. B's insight
> is the one thing A does not carry, so it is adopted **inside** A as § Failure domains'
> organising distinction rather than discarded — that is a deliberate composition, not a
> compromise.

[Answer]: A

---

## Consolidated Summary Confirmation

All five answered with the recommended option, guided mode, 2026-09-04. Recorded as **five
separate answers to five questions in this unit's set**, not a standing autonomy grant — the
next unit's questions are asked normally.

**Q1 — the provenance check while the permitted-producer list is unset**: **A. Fail closed.**
`build_features` **raises** and names the unset list; **no feature matrix is produced**. The
deciding fact is what the artifact would be: the emitted object is the **last artifact before
training**, so every reported number would inherit an unverifiable column. This deliberately
**differs from `external-products`' skip-not-pass** and **agrees with
`target-standardization`'s fail-closed**, and the difference is the argument — a missing module
consumes nothing, a matrix on disk gets trained on and a gate report does not travel with it.
**Schedule cost stated rather than discovered: this unit produces nothing until the
permitted-producer list is authored and frozen, and that list is not this stage's to write.**
The list must be keyed per **(row, producer)** pair, not per producer.

**Q2 — where the per-column provenance stamps live**: **A. In `spec.json`**, as a
column-keyed map alongside the bundle's existing identity fields. ADR-11 already makes the
bundle directory **read-all-three-or-raise**, so a dropped stamp becomes a **load failure**
rather than a stamp silently regenerated as blank — the exact hazard TS-F-01 named against
Parquet field metadata. A column added without its `spec.json` entry **raises** rather than
defaulting. These stamps are **additional to** `phase_id` / `source_id` /
`target_definition_id`, which the mandated rule requires on the matrix and on every mask
regardless.

**Q3 — where this unit's locked-partition guard test goes**: **C. Extend
`tests/test_locked_test_guard.py` in place, and record the two-unit ownership explicitly** in
the module's own docstring plus a row in this unit's coverage table. This keeps §12's mandated
`tests/` tree **untouched** — the only option needing no change record — and closes A's one real
weakness, that the existing file's Governance block cites only `governance-guards` R-25/R-28 so
limb 1 would read as theirs. **The substantive gap is not closed by this answer**: limb 1 is
unwritten and `materialise_locked_partition` does not exist. Option B remains the cleaner
ownership design and is available as an owner-approved change record to the mandated set.

**Q4 — WS-13 / FR-P1-04-8 parity evidence**: **A. A value-level parity test on the fixture** —
reconstruct the flattened matrix rows from the tensor's slices and assert element-wise equality
within the fixture manifest's declared floating-point tolerance, with **C's shape-and-ordering
assertion as its precondition rather than its alternative**, so a failing value comparison is
interpretable. **The tolerance is unset and is recorded as owed to the fixture manifest, not
filled here**: `team.md` fixes that fixture assertion data lives in
`tests/fixtures/<fixture_id>/fixture_manifest.yaml`, and TE §15.1 fixes that tolerances are
**measured and frozen, never invented**. **This proposes a check; it adopts no reading of
TE §16's WS-13 criterion, which stays open.**

**Q5 — the boundary criterion**: **A. By the object whose integrity each component
guarantees** — four components: the **availability record** (W-1), the **feature bundle**
(W-2, W-4), the **partition set** (W-5, W-8, W-9), and the **fitting identity** (W-3, W-6).
Four persisted artifacts, four distinct schemas, which is what `infrastructure-design` and
`code-generation` need next. **B's insight is adopted inside A** as § Failure domains'
organising distinction — most failures here raise, and the full-dataset fit *"produces better
validation numbers and raises nothing anywhere"* — rather than discarded.

**Unchanged by these answers.** No scientific value is decided; TE §18.2's absolute rule
stands. **BLK-04, BLK-08 and BLK-09 stay open exit conditions** and **no implementation is
authorised**. The **permitted-producer list** stays non-existent and owed. FR-P1-04-10 still has
**no acceptance row**; TA-33, TA-34, TA-35 and TA-36 stay `Pending`; WS-10/11/12/13/16/18,
TA-07/08/11/15 and the §18.3 preflight stay undischarged. The **station-registry provenance
question** stays open and owned by `inventory-and-registry`, so `station_lat` stays blocked and
`lst_sin`/`lst_cos` stay excluded. `configs/` does not exist and no interpreter is reachable, so
every check designed here is **written-but-unexecutable** today. **No module is written by this
stage.**

**Carried to the gate, not applied here.** The three uncited requirement IDs of Derivation 3
(**FR-P1-04-2, FR-P1-04-5, FR-P1-04-8**) are added to **this stage's** coverage tables and
labelled as added here; the upstream `nfr-requirements` artifacts are **not edited** — they are
terminal-READY under a frozen receipt. The signed "nine-site sweep" record in
`functional-design-questions.md` **stays unedited**, its correction still awaiting one owner
ruling.

<!-- Re-collected 2026-09-04: the redo jump on `nfr-design` reset this stage's receipt floor,
     invalidating this unit's summary-confirmation receipt. The stored value was `Looks correct`
     and is being re-affirmed on the fresh floor, not changed. The three adversarial findings
     fixed after that jump are recorded in the artifacts' own correction boxes. -->

- Looks correct
- Request changes

[Answer]: Looks correct
