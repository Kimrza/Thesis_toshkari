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
