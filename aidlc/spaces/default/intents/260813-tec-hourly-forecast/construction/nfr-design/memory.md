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

## Interpretations

- 2026-09-04T15:34:17Z — Read the diary's own two-stage prescription and moved the derivation one step earlier again — **before the questions file, not before the artifacts** — and it paid a third time; context: at `inventory-and-registry` the set-difference ran before the artifacts and found one item the questions had missed; at `external-products` the same lesson was restated as "derive before writing the questions file"; here it was actually done that way, and Derivation 1 produced a question (Q3) the question set would not otherwise have contained at all. The check has now graduated from a correction to an input.

- 2026-09-04T15:34:17Z — Read Q1's fail-closed answer as **agreeing with `target-standardization` and diverging from `external-products` on one discriminating fact**, and wrote that fact into the artifact rather than the conclusion; context: three sibling units have now answered the same "what does the check do while its input does not exist" question and the answers split. The discriminator is whether the guarded object would EXIST and be consumed — a missing module consumes nothing, a feature matrix on disk is trained on. Stating the discriminator makes the divergence auditable; stating only the answer would make it look like inconsistency between units.

## Deviations

- 2026-09-04T15:34:17Z — Added **three requirement IDs** (FR-P1-04-2, FR-P1-04-5, FR-P1-04-8) that the upstream `nfr-requirements` coverage table does not carry, labelled as added at this stage, and did **not** edit the upstream artifact; context: all three are in `unit-of-work.md` § 7's canonical eleven, all three are implemented verbatim in SEC-F-02/SEC-F-03, and `grep -c` returns 0 for each across both upstream artifacts. This is the **third recurrence** of one defect class on this unit (7 → 11 → 13 → 16). The upstream file is terminal-READY under a frozen receipt, so the reconciliation is a gate item and the addition claims an obligation rather than a discharge.

- 2026-09-04T16:02:37Z — **Bracketing one unit with the lifecycle receipt verbs switched the whole workflow out of artifact-driven coverage, and the engine then re-routed to an already-built unit**; context: the stage protocol says to bracket every inline per-unit directive with `unit start` / `unit complete`, and also says "workflows that never call the verbs keep today's artifact-driven coverage unchanged". Both are true and the second is the trap: the audit trail held **zero** `UNIT_*` events before this session, so the first receipt pair made the six previously-built units unsettled by definition. Surfaced to the owner rather than improvised across eleven units; on the owner's ruling the six were backfilled with `unit start` + `unit complete` and **not** regenerated or re-reviewed, since each already carries a terminal `READY` `REVIEW_COMPLETED` in this attempt's trail and `unit complete` verifies the artifacts on disk. The mechanical lesson: **check whether a workflow is already in receipt mode before emitting the first receipt**, because the first one is a mode switch for every unit, not a record about one.

- 2026-09-04T15:34:17Z — Verified three upstream status claims against the workspace before designing anything, and **one was jointly false with a second claim**; context: W-10 says all six of this unit's test modules do not exist and W-6 says `test_locked_test_guard.py` is this unit's because it exercises both limbs. The file exists and covers `governance-guards`' read limb only. Each claim was true when written; together they are now false in a way neither is false alone, so a reader checking either one concludes the guard test is entirely absent or entirely present.

## Tradeoffs

- 2026-09-04T15:34:17Z — **A defect found by workspace inspection rather than by review, and the shape of it is new to this project's record.** Context: every prior sweep failure here was a stale REPRESENTATION of a corrected fact — the correction landed in one surface and not another. This one is different: two claims in the same artifact were each accurate on their own date and became **jointly** false through a change to the workspace that neither claim's author saw. No sweep of the artifacts could find it, because the contradiction is not between two texts; it is between two texts and a directory listing. The mechanical form that catches it: **before designing against a claim about what does not exist, list the directory.** It costs one command.

- 2026-09-04T15:34:17Z — Chose Q3 = C (extend the existing module plus an ownership block) over Q3 = B (a second module) knowing B is the better design, on the single ground that B **adds to §12's mandated `tests/` tree**; context: §12 names `test_locked_test_guard.py` and no sibling, so a second module is a change to the mandated set — the same class of act as `CR-2026-08-22-LEAKAGE-TA` — and this stage may not take it. The cost accepted is two units editing one module. B was recorded as available by change record rather than dismissed, so the better design stays reachable without this stage reaching for it.

- 2026-09-04T15:34:17Z — Adopted Q5's rejected option B **inside** the chosen decomposition rather than discarding it, and said so in the artifact; context: the loud/silent failure distinction is the single most consequential fact about this unit — F-4's characteristic failure produces *better* validation numbers and raises nothing — but it yields two boxes, which is a distinction and not a decomposition. Carrying it as § Failure domains' organising fact keeps the insight without letting it set a boundary it cannot support. Risk accepted: a reader who wanted the visibility axis will read § Failure domains as a consolation, so the composition is stated as deliberate.

- 2026-09-04T15:34:17Z — Printed **F-2: 8 of 16** coverage rows and stated the imbalance rather than rebalancing it; context: the honest alternative was decomposing F-2 along leakage channels, which is Q5's option C and would place several components inside one module (`build.py`), making boundaries that no test can isolate. An uneven distribution that follows the axis is better than an even one that follows nothing, but it looks like a decomposition that gave up halfway unless the reason is on the page.

## Deviations

- 2026-09-04T17:00:00Z — **Recommended a redo jump to fix two numerals and a paragraph, and it cost two jumps, sixteen artifact re-saves and sixteen human re-affirmations**; context: two units held terminal READY receipts with findings the owner directed be fixed, and the review-freeze hook refuses a write to a frozen `produces[]` artifact. I offered four routes and recommended the jump, estimating its cost as "eight units re-run". The actual cost was four compounding cascades — invalidated review receipts, invalidated **human-backed** summary confirmations, an engine precondition requiring a native-tool artifact write *after* each fresh confirmation, and finally a hard deadlock. The route I listed second and did not recommend — build the remaining units, reach the stage gate, and let the human's Request Changes lift the freeze — costs **nothing extra**, because `GATE_REJECTED` is one of the three events that reset the floor. **The rule for next time: when a terminal receipt blocks a fix, the gate rejection is the cheap release and a jump is the expensive one; prefer the gate unless the gate is unreachable for an independent reason.**

## Tradeoffs

- 2026-09-04T17:00:00Z — **The deadlock was an ORDERING error of mine, not a framework defect, and the order that terminates is confirm → write → review.** Context: the first recovery ran fix → review → confirm. That leaves every artifact write *older* than its confirmation, so the engine demanded a post-confirmation write while the fresh READY receipt from the just-run review forbade exactly that write. Neither guard was wrong; they were satisfiable only in one sequence, and I picked another. The second jump was spent solely on re-running the same steps in the right order. Recorded because the two guards are individually documented and their **interaction** is not: the engine wants a write after the confirmation, the hook forbids a write after a READY verdict, so the confirmation must precede the write and the review must follow it.

- 2026-09-04T17:00:00Z — **Read the enforcing hook instead of continuing to guess at it, and that is what ended the thrashing**; context: after two blocked attempts I read `.claude/hooks/aidlc-review-freeze.ts`, whose header names its exact release conditions — `GATE_REJECTED`, `STAGE_JUMPED`, `WORKFLOW_STARTED`, and a `NOT-READY` verdict never freezing. That turned an apparently arbitrary refusal into a decision table, and it also ruled out the two dishonest escapes (fabricating a NOT-READY verdict; disabling the hook via a settings change the human had not asked for). Three probe attempts had been spent on guesses that the header answered in four lines.

## Interpretations

- 2026-09-04T16:20:00Z — **Answered the "what does a control do while its input does not exist" question the OPPOSITE way one unit later, and the discriminator held**; context: `features-and-splits` chose fail-closed, and the reason recorded there was whether the guarded object exists and gets consumed. A tuning result plainly does, so the same test pointed at fail-closed here too — until a third option appeared that the earlier unit did not have: the check had a **runnable form that never needed the missing artifact**. § SEC-M-01 had introduced R-25's log to decide *when* an attestation is demanded, not to enable one, so making the attestation unconditional turned a blocked control into a stricter runnable one. The general shape: before answering fail-closed-versus-skip, ask whether the control can be **re-expressed without** the missing input; that third option dominates both when it exists.

## Deviations

- 2026-09-04T16:20:00Z — Designed a control that makes **BLK-07 a future narrowing rather than a blocker**, which changes another unit's blocker's reach from this unit's side; context: 3.2 recorded the December-window block as *"specified and unrunnable today"* and its own Assumptions treated BLK-07 as the thing to wait for. Removing the dependency is a design change, not a restatement, so it is recorded as a deviation from the upstream artifact's own posture even though it strengthens the requirement rather than weakening it.

## Tradeoffs

- 2026-09-04T16:20:00Z — **Bound the human attestation to `criterion_hash` rather than to the run**, at the cost of putting a human signature inside a machine-written record; context: a name-and-date attestation floats free of what it certifies, so one attestation could cover a criterion changed after it was signed — reintroducing, through the human record, exactly the substitution mechanism 2 exists to catch. The alternative (a separate `evidence/` artifact joined by `run_id`) is more supervisor-readable and adds a join that can dangle or resolve to the wrong criterion. Recorded with the note that a **rendered projection** of the field delivers the readability without the join.

- 2026-09-04T16:20:00Z — **The cheapest implementation of W-12's receipt is the one that silently disables it, and that is now stated as the mechanism rather than as an implementation note**; context: writing the receipt inside `07` or the bootstrap satisfies both consuming rules and makes *"the receipt precedes the metric"* true **by construction on every run**, including a run where the prediction was regenerated after a score was seen — the control would pass its own test and detect nothing. So Q3's option B (registry row only) was rejected for removing the process boundary the design rests on, and the precedence rule (file authoritative for the hash, row for the run's existence, disagreement raises) was stated rather than left to be discovered.

- 2026-09-04T16:24:35Z — **Printed a per-component count I did not derive, in the same artifact where I printed three derivations I did** — and the reviewer caught it; context: `logical-components.md` asserted "C-1: 4, C-2: 4, C-3: 6, C-4: 1 — sums to 14". The total was right and one component figure was wrong: a grep over the coverage table's own rows gives **C-2: 3**, and 4+3+6+1 = 14. Confirmed independently before relaying the finding, per `project.md`'s verify-before-handing-on rule. The mechanism of the error is worth more than the error: the three **named** derivations were run with commands and printed, and this fourth count — one sentence lower, in the same paragraph — was read off the table by eye because it felt like part of the sentence rather than a claim. `project.md` § Way of Working already fixes that every count is derived programmatically and printed; the gap it does not close is that a count can hide **inside** a sentence whose other numbers were derived, which is where the habit stops looking. The finding rides a READY verdict, so it is gate input rather than an edit: the receipt is terminal and a write would invalidate it.

- 2026-09-04T16:20:00Z — **A zero set-difference recorded as a result rather than passed over**; context: this unit's requirement IDs, its exceptions, and its file list all came back clean — 0 uncited IDs, 0 undeclared exceptions, 0 claim/disk contradictions — immediately after a unit where the same three derivations found 3, 0 and 1. Writing "0" with the derivation printed is what makes the check visible as having run; omitting it because nothing was found is indistinguishable from not running it, which is the same reasoning as Q4's positive probe two sections away in the artifact.

- 2026-09-04T16:20:00Z — **Chose a decomposition axis on the shape of the unit's RULES rather than on its objects, artifacts or modules**; context: seven siblings had taken seven axes, and the obvious eighth (the object at stake, `features-and-splits`') under-discriminates here because most of this unit's objects are the same object — a `Prediction` — at different moments. What genuinely varies is *what plausible thing must not stand in for the specified one*, and every rule R-90…R-102a has that shape. The payoff was not tidiness: each component's negative control **falls out** of the boundary, which is the affirmed every-hard-rule-gets-a-test practice expressed as structure.

## Deviations

- 2026-09-05T00:00:00Z — **`acquisition` goes to the gate at a terminal NOT-READY with one open Critical — introduced by my own repair.** Context: iteration 1 found eight wrong acceptance-row cells and four wrong-owner rows; the repair re-derived every acceptance cell from `requirements.md` per-ID, but the OWNERSHIP labels were written from memory of a sibling's table — and one was wrong: NFR-AUD-01's TA-21 labelled "owned by `inventory-and-registry`" when `unit-of-work.md` assigns TA-21 to `fixtures-and-reproducibility`, identical in both files. The reviewer's iteration-2 pass caught it; the budget is spent; per stage-protocol §12a the finding is quoted at the gate and NOT edited, because a post-terminal-receipt write would invalidate the receipt and re-wedge the workflow — the exact trap this stage already paid for twice. The fix is one word in two files and belongs to the gate's Request-Changes path.

## Tradeoffs

- 2026-09-05T00:00:00Z — **A repair that derives half its cells and carries the other half is worse than it looks, because the derived half buys false confidence in the whole row.** Context: every acceptance-row VALUE in the acquisition repair was re-derived per-ID with the command printed; every OWNERSHIP label in the same cells was written from the pattern established at `governance-guards` and `models-and-baselines` ("TA-10, TA-21 — foundation/inventory-and-registry") without re-deriving WHO owns each TA row from `unit-of-work.md`. The mechanical form that closes it: an ownership label is a citation like any other — derive it from the owning artifact's per-unit `Acceptance rows` lines at the moment of writing, never from another unit's table, however recently that table was itself verified. Also recorded: the per-ID VALUE check and the per-ID OWNER check are two different checks, and this stage has now been burned by skipping each one separately.

## Tradeoffs

- 2026-09-05T01:00:00Z — **The carried-not-derived defect hit me three times in one review sweep, each time in text ABOUT findings rather than in a finding's subject.** Context: (1) `acquisition` — the TA-21 ownership label carried from a sibling's table (`unit-of-work.md` gives TA-21 to `fixtures-and-reproducibility`); (2) `external-products` — my receipt-floor note re-opened a Critical and a Major that the file's own 2026-09-02 terminal pass had CLOSED, carried from session memory of the original run; (3) `external-products` again — my correction's "genuinely still open" list re-typed the recommendation's five-item example instead of deriving from the terminal review's enumeration, omitting `IMPL-13`. The common shape: meta-text (ownership labels, status notes, still-open lists) feels like commentary and so escapes the derive-before-assert discipline the substantive cells get. The rule that closes it: **a status claim about a finding is a citation like any other — derive it from the artifact's own body (its Review sections, its correction boxes) at the moment of writing, never from memory of the run that produced it.** Two of the three now sit as open findings at the gate because the iteration budgets are spent.

## Open questions

- 2026-09-05T01:00:00Z — **The TA-21 misattribution is systemic, not local**: `inventory-and-registry`'s artifacts natively attribute TA-21 to `foundation`, my `acquisition` repair copied the same wrong pairing, and `unit-of-work.md` gives TA-21 to `fixtures-and-reproducibility`. Any artifact citing NFR-AUD-01's rows should be swept for it. Worth one gate ruling covering all representations at once rather than per-unit fixes.

- 2026-09-04T16:20:00Z — **The two components whose failures are silent are the two that could be built today, and the two whose failures are loud are the two the unfrozen pin blocks.** C-1 and C-2 wait on the TensorFlow pin; C-3 (selection) and C-4 (the one-shot write) do not. So the build order the pin imposes is the inverse of the one risk would choose. Worth carrying to `delivery-planning` or the gate: this is a sequencing fact, not a design defect, and no artifact currently states it.

- 2026-09-04T15:34:17Z — **The permitted-producer list is assigned to no unit, and Q1 = A now makes it blocking.** Before this answer it was a named dependency; after it, Bolt 7 produces **nothing** until the list exists. No unit owns it, TC-03e has not decided whether it is governed config or a code constant, and if it is config it needs a D-number before any implementation reads it. Worth carrying to `infrastructure-design` and to the gate: a blocking artifact with no owner is a schedule stop, not a design note.

- 2026-09-04T15:34:17Z — **Three sibling units have now answered the same question and split two-to-one, and no rule records the discriminator.** `external-products` skips, `target-standardization` and this unit fail closed, and the discriminating fact — does the guarded object exist and get consumed — is stated in each artifact's own prose and nowhere general. Four more units run this stage. If the discriminator is not recorded as a practice, the fourth answer will be argued from scratch or copied from whichever sibling was read last.

- 2026-09-04T15:34:17Z — **A 3.14 interpreter ran in this workspace and the governed pin is 3.11.** `src/data/__pycache__/config.cpython-314.pyc` exists; no interpreter is reachable today. The upstream banner's conclusion (nothing is executed evidence) survives, but the reason has changed twice in three days, and a `.pyc` from an ungoverned interpreter is the kind of artifact that later reads as evidence that something ran and passed. Worth a check at `build-and-test`: whether ungoverned-interpreter bytecode should be excluded from the repository at all.

## Interpretations

- 2026-09-04T22:43:34Z — Read `nfr-requirements`' raised-not-resolved clock-domain assumption (the ordering check compares timestamps two hosts may have written) as **this stage's to resolve**, not 3.5's; context: `nfr-requirements` deferred "where the timestamp is read from" to 3.5, but the *mechanism* is a security design choice, and deferring both would leave 3.5 choosing a design with no design stage behind it. Q1 put four mechanisms to the owner; the containment answer (A) removes the clock comparison rather than bounding it — the access record captures the registry's `mask_id`s and content hash at access time, so registration provably preceded access on any clocks.

## Tradeoffs

- 2026-09-04T22:43:34Z — **Chose containment (Q1 = A) over a declared skew bound (C) because C's bound is an invented constant with no measured basis** — Kaggle's clock behaviour being unmeasured is the raised problem, so a bound picked by convenience would sit next to §18.2's posture uncomfortably even though it is not a scientific value, and a too-small bound gives false refusals at G-06, the one event that can never be re-run. The accepted cost: two new fields on `governance-guards`' access record — a half-contract this unit states and cannot satisfy alone, the third such half-contract this unit now carries (hash receipt, BLK-08, containment fields).

- 2026-09-04T22:43:34Z — **Q2 = C composes A's single failure domain with per-entry negative controls because a guard module alone fails open on a forgotten call, and inline copies drift**; context: the drift failure is not hypothetical here — R-105 raised the wrong exception while claiming to mirror R-92 (GOV-2026-08-28-FD-01 Rec 8), and one copy of the logic leaves nothing to drift. The per-entry controls are WS-10's prove-the-denial-fires methodology applied to this unit's own boundary; cost is one control per public entry point in an already-specified, unwritten test plan.

## Open questions

- 2026-09-04T22:43:34Z — **The two containment fields (`mask_bundle_ids`, `mask_registry_hash`) need `governance-guards`' adoption** — its access record is R-25's and its `open_restricted` populates the fields at access time. Stated in both artifacts as a half-contract, not declared satisfied; owed to `governance-guards` at its next touch and to the gate as a cross-unit obligation. Unrunnable while BLK-07 is open.

- 2026-09-04T22:43:34Z — **The registry content hash assumes the mask registry is one hashable artifact** (TS-C-03's single Parquet + manifest). If 3.5 splits the registry, the hash target must become the manifest enumerating the parts — carried to 3.5 as a note, not a new decision.

## Interpretations

- 2026-09-05T06:04:44Z — Read `statistical-inference`'s scientific opens (interval method, block scheme, correlation series, §15.3 count classification) as **off-limits to this stage's questions**, and asked only engineering questions; context: all four are proposed-and-routed upstream under §18.2/§18.3, so a design question that re-asked one would be the fill-by-convenience channel wearing a question's clothes. The two questions asked (hash byte definition, guard sourcing) are contracts in the same class as the PCG64 pin — the sort `nfr-requirements` itself classifies as engineering, not scientific.

## Tradeoffs

- 2026-09-05T06:04:44Z — **Extended the sibling's guard-module design across a unit boundary (Q2 = A) rather than keeping each unit's checks self-contained**; context: the R-105-vs-R-92 drift already proved two copies of one check diverge, and both units co-own `src/evaluation` by the approved path grant, so the import crosses no package boundary. Cost accepted: `statistical-inference`'s design now depends on a sibling module that does not exist, and a reshape at 3.5 moves both units. The dependency is stated as check semantics, not a file name, to keep that reshape cheap.

- 2026-09-05T06:04:44Z — Defined the replicate hash's bytes at design time (Q1 = A) instead of leaving serialisation to 3.5; context: WS-17's evidence is only evidence if two platforms compute the same hash, and the four pinned facts (float64, little-endian, C-order, draw order) travel in `BootstrapResult` so drift is diagnosable. One derived figure printed (replicate vector = 80,000 bytes), which also collapsed most of TS-S-04's held-in-memory question: the vector is materialised; only the workspace peak stays measurement-bound.

## Open questions

- 2026-09-05T06:04:44Z — **The shared guard module is now load-bearing for two units before either exists.** If the stage gate or 3.5 changes `evaluation-and-comparison`'s SD-C-01 shape (the gate holds a Major against its guard table already — the mask-vs-member partition check), `statistical-inference`'s B1 design inherits the change. The gate should rule on the Major with both consumers in view.

## Interpretations

- 2026-09-05T06:37:36Z — Read `regimes-diagnostics-reporting`'s two raised-not-resolved assumptions (the unowned thesis-level location list; the rendering refusals' home) as this stage's design work, and the gate-routed items (exploratory label's writer, coverage notebook's home, §15.2 proposals) as untouchable; context: same boundary as the two prior units — a raised engineering gap is design work, a routed scientific or owner decision is not.

## Deviations

- 2026-09-05T06:37:36Z — Drew an explicit metric-entry/rendering boundary split against the sibling's shared guard module rather than absorbing the sibling's open Major into this unit's render guards; context: the mask-vs-member partition check is a metric-entry concern and a rendering check runs too late to catch it, so papering it over here would hide the gap the gate needs to rule on. The split is stated in both new artifacts so no check is homeless or double-owned by silence.

## Tradeoffs

- 2026-09-05T06:37:36Z — Made the registered conclusion surface the single thesis-level location enumeration (Q1 = A), accepting a stated residual: hand-authored prose outside the pipeline never passes a producing path and cannot be forced to register; context: the alternatives (hand-maintained config list, directory globs) reintroduce exactly the staleness the raised assumption names. The residual is the same class as the already-stated indirect-citation weakness — narrowed, not closed, and said in both artifacts so no reader takes the checklist as fully enforced.

- 2026-09-05T06:37:36Z — Third unit in a row settled on the same guard shape (single module + per-entry negative controls), each time by the human choosing the recommended option; context: the pattern is now project idiom across `evaluation-and-comparison` (metric-entry), `statistical-inference` (consumed), and `regimes-diagnostics-reporting` (rendering). Worth surfacing at the §13 ritual as a candidate practice — one guard home per boundary, per-entry controls proving invocation — so the fourth unit inherits it as a rule rather than a question.

## Open questions

- 2026-09-05T06:37:36Z — **The registration/guard transaction boundary is owed at 3.5**: an artifact must not be emittable registered-but-unguarded or guarded-but-unregistered. Stated in `logical-components.md`'s notes; if 3.5 cannot give the two one boundary, the fallback ordering (register first, guard refuses unregistered) must be stated there.

## Tradeoffs

- 2026-09-05T07:00:00Z — **The Critical repair reproduced its own defect class at narrower scope, and the terminal pass caught it**: four guards were added because five mandated render-time controls were homeless, and one of the four (`require_provenance_block`) was scoped to the table (W-3) while its control (32) says "table or breakdown artifact" — derived per-control against `business-rules.md` for the Refuses text, but the Called-by column was written from the section's own W-3 narrative rather than re-derived from each control's scope. The two derivations are different checks: WHAT a guard refuses, and WHERE it must run. This stage has now been burned by deriving one and carrying the other on the same table row. The finding rides a terminal READY and goes to the gate unedited.

## Open questions

- 2026-09-05T07:00:00Z — **Open at the stage gate, `regimes-diagnostics-reporting`**: widen `require_provenance_block`'s Called-by to W-5 (and sweep FR-P1-05-16's coverage row plus `logical-components.md` R4) — one-word-class fix, blocked by the terminal receipt, belongs to the gate's ruling.

## Interpretations

- 2026-09-05T06:59:48Z — Read the reference-hash location question as **legitimately askable at this stage** even though upstream assigned the choice to the owner; context: the questions file's human IS the owner path, so a structured question with the three upstream-named candidates is the sanctioned route-to-owner, not a convenience fill. The answer (Q1 = C) is recorded as an owner ruling in the artifact, not as a stage decision.

## Tradeoffs

- 2026-09-05T06:59:48Z — **Unified receipt staleness with gate staleness (Q2 = A) instead of solving receipt durability**; context: the raised assumption asked whether receipts survive Kaggle sessions, and binding validity to §13.1 lock identity makes survival irrelevant to correctness — an absent receipt fails closed and re-runs fixtures. One discriminator now serves two mechanisms (gate reuse, receipt validity), which removes a drift surface but also couples both to the lock's completeness; that shared limit is stated in both artifacts and owed to G-07.

- 2026-09-05T06:59:48Z — Accepted a second representation of the freeze hash (sibling file + D-number entry, Q1 = C) in the unit whose own history shows multi-representation counts going stale; context: the mitigation is structural — the agreement is a tested assertion that raises naming both sites, not a convention. The alternative single-home options each lost something real (A: no governance provenance; B: loader coupled to prose). The choice was the owner's.

## Open questions

- 2026-09-05T06:59:48Z — **F7's agreement check parses `evidence/DECISIONS.md` in test apparatus.** If prose extraction proves unreliable at 3.5, the stated fallback is a machine-readable freeze-record sidecar cited by the D-number. Carried so 3.5 does not improvise.
