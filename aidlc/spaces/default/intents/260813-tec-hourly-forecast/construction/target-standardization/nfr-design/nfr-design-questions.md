# NFR Design — Questions — `target-standardization`

**Unit** `target-standardization` (Bolt 6) · **Kind** `library` · **Stage** `nfr-design`

Two artifacts only — `security-design.md` and `logical-components.md`. `produces_kinds`
maps the other three to `[service]` / `[service, ui]`, and this unit is `library`.

**Nothing below decides a scientific value.** TE §18.2's absolute rule stands. The **QC
operation list** stays `TBD — freeze gate` and the **floating-point diff tolerance** stays
unset; no question here fills either.

> ## ⚠ UPSTREAM STATUS CLAIMS CHECKED AGAINST THE WORKSPACE, 2026-09-03
>
> | Upstream claim | Actual state |
> |---|---|
> | Banner: *"**No Python interpreter exists** in this environment, so every test is written-but-unexecuted"* | **Stale.** `python --version` returns **Python 3.14.7**, and the suite runs — but **3.14.7 is not the governed pin** (TE §8.1, TC-03d fix **3.11 exactly**), so nothing it produces is governed evidence. The conclusion survives; the reason does not. |
> | `configs/` does not exist | **Holds.** So does the rest: `scripts/` contains only `audit_ec1_drivers.py` and `merge_coverage_year.py` — **neither `02` script exists**, and `src/gnss/` holds `__init__.py` only. |
> | The `02` ordinal collision | **Holds as a recorded §12 defect.** Both `02_standardize_prepared_target.py` and `02_build_vtec_target.py` are unwritten, so the collision is still only on paper. |
>
> **Nothing this unit designs is built.** Every question below is about what to build, not
> about repairing something running.

**What is already fixed upstream and is not re-asked.** The QC operations are a **named list
in `configs/data.yaml`**, a scientific constant frozen under a D-number before any
implementation reads it (Q1 = A). The label and lineage caveat travel **as data on the
artifact**, not as documentation, and a consumer reporting a comparison without them **fails**
(Q2 = A) — one half of a cross-unit contract this unit does not declare satisfied. The target
row is **exactly D-17's sixteen fields**; **three definition IDs** stamp every artifact; the
**excluded set is asserted, never substituted**; the support thresholds are **D-19's, carrying
their basis**, with December excluded by construction. `code-generation` **must not invent a
`02a`/`02b` convention**, and the reachability question belongs to `governance-guards` R-23.
None of that is reopened here.

---

## Question 1

TS-T-03 leaves one thing explicitly **owed at 3.5**: whether the label and lineage caveat are
a **column** or **Parquet key-value metadata** — *"whichever survives the round-trip that
`pyarrow` performs"* — and it names the constraint honestly: metadata *"is **easy to drop**
through an intermediate `pandas` operation that rebuilds the frame."*

That matters more than a storage detail, because SEC-T-02's requirement is not that the
caveat be *present* — it is that **a consumer reporting a comparison without it FAILS**. A
carrier the pipeline can silently drop cannot support that.

Where does the caveat live?

A. **A column on every row**, alongside `target_definition_id`
   > **Impact**: Survives any `pandas` rebuild that preserves columns, which is the operation TS-T-03 names as the risk. It makes "a consumer without it fails" a **schema-level check** — the same class of check D-17's sixteen-field contract already uses, so no new mechanism. Cost, stated plainly: one repeated identical string per row. Parquet's dictionary encoding makes that near-free on disk, and it is genuinely redundant data in memory.

B. **Parquet key-value metadata**
   > **Impact**: Semantically right — the caveat is a property of the **artifact**, not of each row — and costs nothing per row. It is the carrier TS-T-03 itself flags as droppable: an intermediate frame rebuild loses it silently, and a consumer would then report without a caveat that no longer exists to be missing. The failure mode is invisible.

C. **Both — the column authoritative, the metadata a mirror**
   > **Impact**: The column carries the guarantee, the metadata keeps the artifact self-describing for a reader who inspects the file rather than the frame. Two places to keep in step, and a divergence between them is a new failure mode that needs its own rule about which wins.

D. **Defer to 3.5**, as TS-T-03 already did
   > **Impact**: Nothing is decided against a format that is not yet written. It is the second deferral of the same question, and it leaves the one requirement in this unit that depends on a consumer **failing** resting on a carrier nobody has chosen.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the requirement's strength decides it. SEC-T-02 asks a
> consumer to **fail**, and only a column makes that a check the pipeline's real operations
> cannot quietly defeat. B is the better model of the world and the worse guarantee, which is
> the wrong trade for a disclosure Vision §6.6 makes mandatory. C is defensible and should be
> taken only with an explicit rule that the **column wins**, because otherwise it adds a
> disagreement rather than a safeguard.

[Answer]: A

---

## Question 2

SEC-T-01 records FR-P1-03-1's closed-set criterion as **BLOCKED**: the diff must show *"only
the documented transformations"*, the set has exactly four members, and the fourth —
**"documented QC"** — is defined nowhere. The QC list is a scientific constant, `TBD — freeze
gate`, and TE §18.2 forbids an implementer filling it.

So the design must say **what the check does while the list is unset**. The unit's own stated
reliability posture is *"it would rather produce nothing than produce a target whose
definition is uncertain."*

What happens when `configs/data.yaml`'s QC list is `TBD`?

A. **Fail closed — standardization refuses to run at all**, raising and naming the unset
   field, so **no standardized target is produced**
   > **Impact**: The strongest reading of the unit's own posture, and it matches TE §18.3's stop-and-report rule directly. Nothing downstream can consume a target whose transformation set was never closable, because nothing downstream gets one. It blocks the entire unit until a supervisor freeze lands — which is the point, and is also a real schedule cost that should be visible rather than discovered.

B. **Produce the target, but skip the closed-set check** with a machine-readable reason, and
   let the §18.3 preflight read the skip as unmet
   > **Impact**: Work proceeds and the gate still refuses. It is the pattern `external-products` adopted for its containment check — but that check guards **code that does not exist yet**, whereas this one guards **a scientific artifact that would exist and be consumable**. A target on disk gets used; a skipped check on a gate report does not stop it.

C. **Produce the target and run the diff over the three specified transformations**, reporting
   the fourth as unverifiable
   > **Impact**: Maximum information — you learn whether UTC normalization, cell selection and aggregation behaved. It reports a **partial** closed-set result for a claim that is only meaningful when closed, and W-2 already says why: with one member unspecified, *"an undocumented change is indistinguishable from a QC-attributable one."*

D. **Defer to 3.5**
   > **Impact**: Nothing is designed against an unfrozen value. It leaves 3.5 to decide behaviour at a stop-and-report point, which is exactly the decision §18.3 says an agent may not make.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — and the contrast with `external-products` is the argument,
> not an inconsistency. That unit's skip-not-pass answer was right because its check guards a
> module that does not exist, so nothing can be wrongly consumed in the meantime. Here the
> artifact **would exist**, and a target whose transformation set cannot be closed is precisely
> what R-64 calls a failure. B's weakness is concrete: a file on disk gets read by whoever
> needs it, and a gate report does not travel with it.

[Answer]: A

---

## Question 3

R-73 and TS-T-04 fix that a run contains **exactly one `02` script**, selected by `--phase`,
and that the clean-run contract **asserts** it — which is what makes the adopted reading of
the `02` ordinal collision **falsifiable** rather than merely stated. Neither `02` script
exists yet, so this designs the assertion, not a repair.

How is "exactly one `02` per run" asserted?

A. **From the run manifest**: every run records the stage scripts it executed, and the
   clean-run contract asserts **exactly one** recorded entry whose basename matches `02_*`
   > **Impact**: Asserts what the rule actually says — a property of **the run**, checked against what the run recorded it did. It reuses the environment-lock/run-record machinery `foundation` already owns rather than adding a mechanism, and it fails loudly on the one thing the reading assumes cannot happen. It depends on the run manifest recording executed scripts, which is `foundation`'s contract and must be stated as a dependency rather than assumed.

B. **A static check on the tree**: assert `scripts/` holds exactly two `02_*` files and that
   `--phase` selects between them
   > **Impact**: Cheap, needs no run, and catches a third `02` script being added. It constrains the **repository**, not the **execution** — two `02` scripts running in one process would pass it, which is the exact failure R-73 exists to detect.

C. **A run-time guard inside each `02` script**, asserting via `sys.modules` that the other
   is not loaded
   > **Impact**: Catches the failure at the moment it happens, in the process where it matters. It makes each script aware of its sibling's module path — the coupling `governance-guards` R-28 declined for the same reason elsewhere — and it duplicates a phase-boundary concern that W-6 explicitly assigns to `governance-guards` R-23, against its own warning that *"two rules about one fact is how they drift apart."*

D. **Defer to 3.5**
   > **Impact**: Nothing designed against scripts that do not exist. It also leaves the falsifiability claim unfunded: the reading is called falsifiable because the contract asserts it, and if the assertion is never designed, the claim is doing no work.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it is the only option whose subject is the run, which is
> what R-73 constrains. B checks a fact about the tree that does not bind execution, and C buys
> immediacy at the cost of exactly the drift W-6 warns about. A's dependency on the run manifest
> recording executed scripts is real and should be stated as owed to `foundation` rather than
> assumed satisfied.

[Answer]: A

---

## Question 4

`logical-components.md` needs a boundary criterion. The four sibling units each chose a
different axis and said why: `foundation` **failure consequence**; `governance-guards`
**enforcement timing**; `inventory-and-registry` **how the failure reaches a human**;
`external-products` **what the component keeps out**.

This unit is not a guard and keeps nothing out. Everything it does makes some claim about the
target true — what its **values** are, what **shape** each row has, and what the number
**means** when someone reports it.

What criterion should the decomposition use?

A. **What each component makes true about the target** — three components: **values** (the
   four transformations, D-16's aggregation, D-1's cell rule, the value-level diff);
   **shape** (D-17's sixteen fields, the three definition IDs, the asserted excluded set,
   D-19's thresholds and their basis); **meaning** (the label, the lineage caveat, the
   spatial-representativeness mismatch, the no-equivalence rule)
   > **Impact**: Names the axis this unit actually varies on, and separates three failures with genuinely different consequences: a wrong **value** is wrong science, a wrong **shape** breaks a consumer loudly, and a wrong **meaning** is a correct number that gets reported as something it is not — the only one of the three that is silent all the way to the thesis. It groups the diff with the transformations it verifies rather than with the schema test, which needs saying since both are "checks".

B. **By workflow grouping** (W-1/W-2 | W-3/W-5 | W-6/W-7)
   > **Impact**: Traceable straight back to `functional-design` and easy to verify. It separates W-5's labelling from W-3's field contract despite both being properties of the same row, and pairs W-6 (a script-ordinal defect) with W-7 (the uncertainty budget) on adjacency alone.

C. **By artifact produced** — the standardized target, the data-quality block, the
   uncertainty budget
   > **Impact**: Maps onto what a reader can open. It puts the label and the caveat inside "the standardized target" with nothing marking that they are the one part whose failure is silent, and W-7 already records that the uncertainty budget is **not wholly this unit's**.

D. **By requirement** (FR-P1-03-1 … -5)
   > **Impact**: Direct traceability, and the coverage table writes itself. It splits nothing by behaviour: FR-P1-03-3 and -4 both land on the same row-level contract but sit in separate boxes, while -1's diff and -5's budget share a box only through ID adjacency.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the useful question about a definitional unit is what each
> part *establishes*, and the three answers here fail in three different directions. It also
> isolates the one component whose failure nobody sees: a target labelled as something it is
> not produces a correct number, passes every schema and value check, and is wrong only in the
> sentence someone writes about it — which is precisely why Vision §6.6 makes that disclosure
> mandatory and why SEC-T-02 carries it as data.

[Answer]: A

---

## Consolidated Summary Confirmation

All four answered with the recommended option, on the owner's instruction of 2026-09-03
("Apply your recommendations"). Recorded as a **one-time instruction for this unit's question
set**, not a standing autonomy grant.

**Q1 — where the lineage caveat lives**: **A. A column on every row**, alongside
`target_definition_id`. The requirement's strength decides it: SEC-T-02 asks a consumer
reporting without the caveat to **fail**, and only a column makes that a **schema-level
check** the pipeline's real operations cannot quietly defeat — TS-T-03 itself names
Parquet metadata as *"easy to drop through an intermediate `pandas` operation that rebuilds
the frame."* Cost accepted and stated: one repeated identical string per row, near-free on
disk under dictionary encoding, genuinely redundant in memory. **If the metadata mirror
(option C) is ever added, the column wins by rule.**

**Q2 — standardization while the QC list is `TBD`**: **A. Fail closed — no standardized
target is produced.** It matches TE §18.3's stop-and-report rule and the unit's own stated
posture, *"it would rather produce nothing than produce a target whose definition is
uncertain."* **This deliberately differs from `external-products`' skip-not-pass answer, and
the difference is the argument**: that check guards a module that does not exist, so nothing
can be wrongly consumed meanwhile; this one would guard **a scientific artifact that exists
and gets read**, and a gate report does not travel with a file on disk. **Schedule cost
stated rather than discovered: the unit is blocked until the supervisor freeze lands.**

**Q3 — asserting exactly one `02` script per run**: **A. From the run manifest** — every run
records the stage scripts it executed, and the clean-run contract asserts exactly one entry
whose basename matches `02_*`. It asserts a property of **the run**, which is what R-73
constrains, and reuses `foundation`'s run-record machinery rather than adding one.
**Dependency stated as owed, not assumed: the run manifest must record executed scripts.**
The reachability question stays `governance-guards` R-23's — not guarded twice.

**Q4 — the component boundary criterion**: **A. What each component makes true about the
target** — **values** (the four transformations, D-16, D-1, the value-level diff), **shape**
(D-17's sixteen fields, the three definition IDs, the asserted excluded set, D-19's
thresholds and their basis), **meaning** (the label, the lineage caveat, the
spatial-representativeness mismatch, the no-equivalence rule). The three fail in three
directions, and **only "meaning" fails silently** — a correct number reported as something it
is not.

**Unchanged by these answers.** No scientific value is decided. The **QC operation list**
stays `TBD — freeze gate`, owed a D-number. The **floating-point diff tolerance** stays unset
and belongs with the fixture manifest. FR-P1-03-1 stays **BLOCKED**. The `02` ordinal
collision stays a **recorded §12 defect**; no `02a`/`02b` convention is invented. SEC-T-02
stays **one half of a cross-unit contract** this unit does not declare satisfied. No module is
written by this stage.

- Looks correct
- Request changes

[Answer]: Looks correct
