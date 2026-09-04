# Stage Diary — `nfr-design`

## Interpretations

- 2026-09-01T00:00:00Z — Read `produces_kinds` as yielding **two** artifacts for a `kind: library` unit — `security-design.md` and `logical-components.md`; context: `performance-design`, `scalability-design` and `reliability-design` map to `[service]`/`[service, ui]`, and all twelve units of this intent are `library`. `logical-components` lists `library` explicitly and `security-design` carries no kind restriction, so it applies to every kind. This matches the engine's own `produces` list in the run-stage directive, so the reading is confirmed rather than inferred.

- 2026-09-01T00:00:00Z — Read the stage's four NFR design categories (Performance, Security, Scalability, Reliability) as **assessed but mostly inapplicable** for this unit rather than as headings to fill; context: `foundation`'s own `nfr-requirements` § Scope note already assessed all five categories and found no latency target, no load projection, and exactly two execution environments with one user. Inventing a caching tier, an auto-scaling rule or a circuit breaker here would be writing service-shaped design into a research library that serves no request.

## Deviations

- 2026-09-01T00:00:00Z — The stage prose's Step 5 vocabulary (CDN usage, connection pooling, load balancing, data partitioning, failover) describes a networked service; context: this unit loads configs, hashes them, seeds, records runs and writes releases. The design addresses the categories the upstream requirements actually raise — secret-scan scope, credential resolution, audit-integrity durability, release immutability — and states plainly where a category has no content rather than manufacturing one.

## Tradeoffs

- 2026-09-01T00:00:00Z — Declined to write the stage file's Step 5 vocabulary — caching tiers, connection pooling, CDN usage, load balancing, failover — into a `library` unit that serves no request; context: the alternative was five headings of plausible service-shaped prose in the foundation of a research pipeline. Stated the absence and the reason instead. Risk accepted: a reader expecting the stage's standard shape finds four of its five categories addressed as "no referent here", which looks like an omission until the scope note is read.

- 2026-09-01T00:00:00Z — Routed the D-29 release-enumeration surface to the owner as a question rather than designing it; context: TE §18.3 makes it a stop-and-report point, and `functional-design` had named three candidates and chosen none. The owner directed the recommended option, so the decision is recorded as owner-made and a D-number is recorded as owed. The alternative — designing it and flagging the assumption — would have been the exact "fill by convenience" §18.2 forbids, dressed as diligence.

- 2026-09-01T00:00:00Z — Wrote `NFR-DET-01` and `NFR-REP-01` into the reviewer's dispatch brief as "the likeliest misses here", then committed exactly that miss; context: the brief's prediction was correct and the check it predicted was never run against `requirements.md`'s ID space before the artifacts were written. Naming a defect class in an instruction to someone else is not the same act as performing the check, and this stage now has direct evidence that the two feel similar from the inside. The mechanical form that would have caught it: derive the cited-ID set and set-difference it against `requirements.md` **as the last step before writing**, not as a thing the reviewer will do afterwards.

- 2026-09-01T00:00:00Z — A decomposition that verifies is not evidence the decomposed set is complete; context: `logical-components.md` printed 3 shared / 3 security-design-only / 0 here-only, the reviewer independently confirmed that decomposition as arithmetically sound, and it *was* sound — against a row set missing three requirements. The decomposition form was adopted precisely because "N fewer than M" kept going stale, and it does fix that; it simply answers a different question from completeness. Both checks are needed, and passing the first reads as reassurance about the second.

## Open questions

- 2026-09-01T00:00:00Z — SEC-F-06 carries an explicit TE §18.3 stop-and-report point: D-29's verify-on-write uniqueness check has **no enumeration surface**, three candidates are named at `functional-design` § Assumptions, and none is chosen. The stage file's Step 5 would have me design the mechanism; §18.2/§18.3 forbid filling that value by convenience. Routing it to the owner as a question is the sanctioned path — an agent may not pick, but the owner may decide.

## Interpretations

- 2026-09-01T20:04:58Z — Applied the prior entry's own prescription — derive the set-difference **before** writing, not as something the reviewer will do afterwards — and it caught a defect the question set had missed; context: set-differencing W-1…W-6's `RAISES` lines against `src/data/config.py`'s 17-name `__all__` yielded THREE missing exceptions (`InventoryError`, `AuditScopeError`, `SchemaError`), while the questions file had put only two to the owner. The check that was recorded as a lesson at `governance-guards` paid out at `inventory-and-registry` on its first use. Its value was not in confirming a number but in finding an item the question set never contained.

- 2026-09-01T20:04:58Z — Read the owner's 2026-09-01 current-state ruling as requiring this artifact to state the corrections and leave `nfr-requirements` untouched; context: three of that artifact's status claims are stale and **two run in this unit's favour** (the restricted-read chokepoint exists; `performance_inspected` and the `purpose` enum are built). A correction that only ever tightens is a correction being used selectively, so the favourable ones are stated with the same prominence as the unfavourable one.

## Deviations

- 2026-09-01T20:04:58Z — Added **NFR-SEC-01** as a coverage row the upstream `security-requirements.md` does not carry; context: it is cited in that artifact's `## Sources` and given no row, and this is the **security design** artifact, where TE §5.1's `licence and access notes` field on a committed inventory is a concrete egress surface. The addition claims an obligation, never a discharge, and is labelled as added at this stage so it does not read as inherited.

## Tradeoffs

- 2026-09-01T20:04:58Z — Chose Q1 = C (both boundary limbs) knowing it owes a change record against an approved application-design matrix, over B alone which owes none; context: the deciding fact was `component-dependency.md`'s `scripts/*` row granting `yes` against both `models` and `evaluation`, which leaves the script that CALLS the audit free to import what the audit may not. A boundary that binds the callee and not the caller is not a boundary, and no amount of transitive closure inside `src/` fixes it.

- 2026-09-01T20:04:58Z — Declined to fold `SchemaError` into Q2's answer even though the reasoning applies to it on its face; context: the owner answered a two-item question, and `project.md` records that a ruling given on a scope which misdescribes the work must have the correction stated before the ruling is acted on. Routing it to the gate costs one extra decision; folding it in would have been the widening this project has already had to correct once. The cheaper move was the wrong one.

- 2026-09-01T20:04:58Z — Kept W-2's approved `RAISES RegistryError` rather than proposing `StationRegistryError`, accepting a real type-level residual; context: two unrelated failure classes sharing one exception is the worse design in isolation, and changing it from a downstream stage would overrule an approved `functional-design` contract. The residual is recorded and the change-record route is named, so the better design stays reachable without this stage taking it.

## Open questions

- 2026-09-01T20:04:58Z — **No approved application-design row owns the December audit's two output artifacts.** `services.md` gives `01_inventory_and_registry.py` the inventory and the registry only; grep across `services.md`, `components.md` and `component-methods.md` for five spellings of the coverage and regime-count reports returns zero matches in all three. Limb A's constrained set assumes the audit lives in that script; if 3.5 places it elsewhere the set must move with it, and that is a boundary defect rather than a relocation.

## Interpretations

- 2026-09-01T20:31:40Z — Treated the terminal READY's two Major findings as **gate input, not edits**; context: `project.md` fixes that a finding riding a READY verdict is quoted at the gate rather than applied, and the receipt is terminal — a later write to a `produces[]` artifact would invalidate it. Both findings are real and both stay unfixed on purpose, which feels wrong from the inside and is the rule working as designed.

## Deviations

- 2026-09-01T20:31:40Z — Declined the reviewer's iteration-1 finding 5 on its `TA-08` limb while adopting its substance; context: the finding attached `TA-08` to `inventory.py`, and `components.md:169` shows TA-08/TA-12 to be the grep for absent SSN, residual and GRU modules. The seam was registered as DISC-I-3 with the attribution corrected. The iteration-2 pass independently confirmed the refusal was right, which is the first time this project's builder has corrected a reviewer rather than the reverse.

## Tradeoffs

- 2026-09-01T20:31:40Z — The Critical defect **quoted its own refutation two sentences later**: the paragraph said every read routes through `open_restricted` and then approvingly quoted that `open_restricted` refuses any path outside the restricted root. Context: the contradiction sat inside one paragraph of the section covering I-2, the unit's only silent-failure component, and still shipped. The mechanical form that would have caught it: when a design routes an operation through a guard that REFUSES some inputs, enumerate the actual inputs against the guard's predicate before writing — here, `ls evidence/` against `is_relative_to(RESTRICTED_ROOT)`, which takes one command and would have shown eleven of twelve months failing. Prose-level review of one's own paragraph does not catch this; running the predicate does.

- 2026-09-01T20:31:40Z — Repairing the Critical **created the two Majors the terminal pass found**; context: splitting Check 3 into two reconciliations scoped limb 2 to "the other eleven months" and left December in neither limb, and naming `assert_no_december_outside_restricted` as the guard that keeps the path test and the record-date test agreeing asserted an assurance without stating that the guard scans `*.json` only. Both are defects of the repair, not of the original. This is the third time in this project a correction has introduced a fresh contradiction, and the pattern is now specific enough to name: a repair that **partitions** something previously stated as whole must have the partition's coverage re-derived against the original whole, not just checked for internal consistency.

## Open questions

- 2026-09-01T20:31:40Z — **`assert_no_december_outside_restricted` scans `*.json` only** (`src/data/locked_test.py:213`, `root.rglob("*.json")`) while its own docstring claims it *"walks `evidence/` recursively and returns every December-bearing artifact"*. Outside the restricted root `evidence/` holds 33 `.csv`, 23 `.json`, 1 `.jsonl` and 4 `.md`. A December-bearing CSV under `audit_evidence_2022-01/` — the exact TEC-09 failure — would be classed ordinary, read unlogged, and reported clean. This is a defect in existing `governance-guards` code found while designing against it; it is not this unit's to fix and it is load-bearing for this unit's routing.

- 2026-09-01T20:31:40Z — **December is in neither limb of the split reconciliation.** Limb 1 reconciles access rows against the declared scope and never against the report; limb 2 is scoped to the other eleven months. A December read that logs correctly but whose count is dropped from the coverage report passes both checks, which is I-2's own stated failure mode on the one month that matters, and defeats FR-P1-02-3's criterion that the coverage report covers all twelve months.

## Interpretations

- 2026-09-02T05:01:26Z — Read the owner's "apply your recommendations" as a **one-time instruction for one unit's question set**, never a standing autonomy grant; context: the stage protocol fixes that autonomy is never inferred and that a "go with recommended" answer covers only the stage it was given for. Recorded in the questions file itself so the next unit's questions are asked normally rather than assumed answered.

## Deviations

- 2026-09-02T05:01:26Z — Corrected two coverage-status cells DOWNWARD from `nfr-requirements` and disclosed the change; context: FR-P1-04-1 and NFR-IRI-01 read "`Pending` — test written, UNEXECUTED" upstream, and `tests/test_iri_denial.py` does not exist. A downward correction removes a claim rather than adding one, so it needs no argument for its direction — but a coverage cell that changes between stages is exactly what this project has had to correct before, so it was stated rather than quietly applied.

## Tradeoffs

- 2026-09-02T05:01:26Z — **The derivation caught the same class of defect on two consecutive units, and the second was worse.** Context: at `inventory-and-registry` the question set put two missing exceptions to the owner and the set-difference found three; here it put two and the set-difference found **five**, one of which (`DriverError`) cannot be dispositioned at all because its raise-conditions are self-contradictory upstream under a carried Major finding. The mechanical form that fixes it is now specific: **derive the exception set-difference BEFORE writing the questions file**, not before writing the artifacts. Deriving it late means the owner is asked about a scope that misdescribes the work, and the correction then has to be routed to the gate instead of being answered in the question that should have carried it.

- 2026-09-02T05:01:26Z — Declined the numeric-fingerprint option for the IRI residual rather than leaving it unmentioned; context: correlating feature columns against the IRI benchmark would reach the rename-and-recompute case the chosen design cannot, and VTEC is supposed to agree with an IRI VTEC estimate of the same cell and hour, so its threshold would be a number invented beside frozen ones. Recording the rejection with its reason costs a paragraph and stops the option being re-proposed as an obvious improvement at a later stage.

- 2026-09-02T05:01:26Z — Accepted a design whose load-bearing half is a **reading of another document's gate criterion**; context: Q1's skip-not-pass only works because TE §18.3's "no failing critical test" is read as "no critical check unmet". Without that reading the skip is strictly worse than the vacuous pass it replaces, because it looks like diligence. Stated as the design's own risk in the artifact rather than as an implementation note, since an implementer who misses it inverts the control.

## Open questions

- 2026-09-02T05:01:26Z — **This unit has no component that announces its own failure.** The three sibling units each had at least one that raises and stops; every failure mode in `external-products` is silent — containment yields optimistic skill, forecast-safety defects are "invisible in validation, fatal on discovery", and a meaningless measurement looks like a measurement. Worth carrying to `build-and-test`: a unit with no loud failure mode gets no early warning from ordinary use, so its negative controls are the only signal, and one of them is unwritten.

## Deviations

- 2026-09-02T05:26:44Z — Left `external-products` at a **terminal NOT-READY** with 1 Critical and 1 Major open, rather than fixing them; context: the adversarial budget of 2 iterations was exhausted, and the stage protocol routes an exhausted-iteration NOT-READY to the human gate with the findings quoted. `project.md` also forbids applying a finding before the gate on the strength of the finding alone. Both rules point the same way, and the defect is real and severe, which makes following them feel wrong from the inside — recorded because that feeling is exactly when the rule matters.

## Tradeoffs

- 2026-09-02T05:26:44Z — **The repair to a Critical finding created a worse Critical finding, and the mechanism was a narrowing that read as a tightening.** Context: the iteration-1 Critical was that the vacuity predicate covered one of two causes. The repair added a second limb scoped to `src/features/` and `src/models/` "the two package trees FR-P1-04-1 and TE §12 name as the forbidden importers" — but `requirements.md:370` states the boundary as an **allowlist, not a denylist**, and names `src/data/`, `src/gnss/`, a training script and a notebook as violating it identically. DISC-E-1's own wording had said "and any other importer"; the repair dropped that clause while appearing to add rigour. Combined with an unconditional "otherwise it skips", the result is strictly worse than what it replaced: iteration 1's predicate could only skip where a violation was **impossible**, and the repair's can skip where one has been **found**.

- 2026-09-02T05:26:44Z — The general lesson, stated so it is checkable next time: **when a repair narrows a set, print the set it narrowed FROM and set-difference it against the rule's own statement of scope before writing.** The two-tree list came from the rule's own example sentence, not from the rule; the artifact being repaired already carried the correct wider phrase three paragraphs earlier. A sweep for the corrected fact would not have caught this, because the defect was in the **new** text rather than in a stale representation of an old one.

- 2026-09-02T05:26:44Z — A control's **outcome switch needs a precedence rule**, not only a condition. The predicate answered "is this check meaningful?" and never said what happens when the scan is meaningless by one limb **and** has found a real violation. Stating "otherwise it skips" unconditionally let a detected violation be reported as unverified. Any future vacuity-gated check in this project should state the precedence explicitly: a detected violation fails regardless of vacuity.

## Open questions

- 2026-09-02T05:26:44Z — **`external-products` carries an open Critical into its stage gate**: the containment check's risk-surface limb is scoped to two package trees where the rule is an allowlist complement, and a detected violation from `src/data/` would report `skipped` rather than fail. Two fixes are named by the reviewer — widen the limb to the allowlist complement the scan already walks, and state that a detected violation fails regardless of either limb — and neither may be applied before the human rules at the gate, because the reviewer's iteration budget is spent and applying a finding on its own strength is forbidden.

- 2026-09-02T05:26:44Z — **A Major sweep miss remains open on the same unit**: `logical-components.md:62` and `:375` still carry the un-narrowed "every component here fails silently and none of them raises at a human", after § Failure domains was narrowed to "no component's CHARACTERISTIC failure announces itself". This is the third time this project has had a correction land in one surface while a justification paragraph elsewhere kept asserting the superseded form.
