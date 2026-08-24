# Functional Design Questions — `governance-guards`

**Unit** `governance-guards` — the runtime prohibitions that must hold before any
scientific work runs, plus the contract that closes Phase 1.
**Kind** `library` · **Complexity** M · **Deployment** shared · **Depends on** `foundation`.

Unit **2 of 12**, and the most governance-sensitive in the plan: it owns the only
code path into the locked December root, both limbs of the phase-boundary
prohibition, the Phase 1 → Phase 2 transition manifest, and the §10.1 reuse
register.

**Nothing here decides a scientific value.** Every question below is about
*mechanism* — how a hash is computed, what a walk covers, where an assertion runs,
what aborts a read. The canonical protected set is frozen by **D-24** and this
stage does not reopen it.

**G-09 is not signed.** `src/data/phase_contract.py`, `src/data/locked_test.py` and
`src/data/reuse_registry.py` do not exist; neither does `src/` or `configs/`.
BLK-01 closed 2026-08-22 granting **authority only** — authority to name a module
is not authority to write one.

**What does exist, and matters to three of these questions:** `tests/` holds
three modules today — `test_acquisition_window.py`, `test_phase_boundary.py`,
`test_release_hashes.py`. Two of them already implement, statically, work this
unit's contracts specify at run time. Where they diverge, the divergence is named
below rather than assumed away.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 2 — the `Owns` list, the boundary that keeps this unit a root, the 10 carried requirements, and BLK-06 / BLK-07.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2 plus § Per-unit coverage summary. **Derived by reading the rows, not carried from prose:** 10 requirements, **1** with no acceptance row (FR-P1-02-6); **owns** TA-27 and TA-28; **supports** WS-18, TA-07 and TA-18. Table 2 also records `RES-01`: permitted-read access logging is **NOT TESTED**.
- `../../../inception/requirements-analysis/requirements.md` — REQ-ENG-5; FR-P1-02-6; FR-P1-03-2; FR-P1-05-12; FR-P1-06-1 through -4; NFR-PHASE-01; NFR-LIC-01. FR-P1-06-1 was amended 14 → 17 under Vision §15.2 (`CR-2026-08-22-PROTECTED-SET`).
- `../../../inception/application-design/components.md` — `phase_contract.py`, `locked_test.py` (**NEW**) and `reuse_registry.py` as this unit's three owned modules, each with its requirement set.
- `../../../inception/application-design/component-methods.md` — the approved contracts: `RAW_MODULES`, `assert_phase_boundary`, `assert_no_raw_fields`, `TransitionManifest`, `build_transition_manifest`, `diff_protected_hashes`, `RESTRICTED_ROOT`, `AccessRecord`, `open_restricted`, `assert_no_december_outside_restricted`.
- `../../../inception/application-design/services.md` § Stage entry contract — the six ordered steps, with `assert_phase_boundary` as **step 4**, skipped only by `02_build_vtec_target.py`. Its § The nine stage scripts table is the source for the producing-script enumeration in Question 7. § Execution platforms records the fact that a Kaggle session carries **no git working tree**.
- `../../../inception/application-design/component-dependency.md` § Shared resources — the unqualified carve-out: *"nothing else may construct a path into it."*
- `../../../inception/delivery-planning/bolt-plan.md` § Gate 0 and § Bolt 2 — the `DP-CHAIR-02` ruling, the Definition of Done, and the confidence hypothesis *"that the prohibitions are enforced at run time, not only in tests."*
- `evidence/DECISIONS.md` **D-24** — the canonical protected set, 17 items, each with a governing artifact and a hashable representation. **D-15** — the relocation of the December-bearing files into the restricted root.
- `../foundation/functional-design/` — unit 1's `IntegrityError` base (R-01), its two-tier error posture, its `ConfigSnapshot` contract, and **R-15**, which states this unit's chokepoint from `foundation`'s side as the absence of a path.
- Workspace inspection, 2026-08-22: `tests/test_phase_boundary.py` (266 lines) and `tests/test_acquisition_window.py`, read directly rather than described from a citation.
- Absent by scope design: `stories` (2.4 `SKIP`), `mockups` (1.6 and 2.5 `SKIP`). `kind: library`, no user-facing surface, so `frontend-components.md` is not produced.

## What the owner's ruling permits this stage to do with BLK-06

Quoted from `bolt-plan.md` § Gate 0, the `DP-CHAIR-02` ruling:

> Functional design **may begin** while BLK-05 and BLK-06 remain open, **but only
> to analyze those blockers and generate the evidence required for their
> resolution**. Both blockers are presented to the owner with options, supporting
> evidence, risks and a recommendation. **Neither is marked resolved and no
> approval is assumed until the owner explicitly decides.**

**BLK-06's limb status.** The *enumeration* and *cardinality* limbs are **RESOLVED**
by D-24 at 17 items, calculated from the enumeration rather than assumed. What
remains **PENDING** is the **per-item binding to concrete config fields and file
paths** — and D-24's own consequence 2 records that none of the four config files
or six `src/` packages exists yet, so *"no file path or field name in the table
above is claimed to exist today."* Questions 1 through 3 produce exactly that
binding evidence. **They do not close BLK-06.**

## Three corrections to the previous draft of this file, so they are not re-inherited

Each was found by re-deriving from the source rather than re-reading the draft,
per `project.md` § Way of Working ("derive a count programmatically from the
artifact and print it before asserting it").

1. **The config-section count was wrong, and so was its membership.** The draft
   said *"Eight of D-24's 17 items hash a config-section — items 4, 5, 6, 7, 9, 11,
   14, 16."* Counted from D-24's Hashable-representation column: **six** items
   carry a bare `Config-section hash` — **4, 7, 9, 11, 14, 16** — and item **13**
   carries `Source + config-section hash`, for **seven** items with a
   config-section component. Items **5 and 6 are `Field hash`**, not
   config-section, and item **12 is a whole-file `Config hash`**. The draft both
   over-counted and named two wrong members while omitting item 13. Question 1 is
   rewritten on the corrected reading, which turns out to change the question:
   there are **three** granularities in D-24, not one.
2. **FR-P1-02-6 is not unenforced.** The draft implied its guard was still to be
   built. `requirements.md` records it as **satisfied 2026-08-21 under D-15** and
   *"enforced by `tests/test_acquisition_window.py::test_locked_month_values_exist_only_under_the_restricted_path"*,
   which exists and is green. What FR-P1-02-6 lacks is a **§16/§19 acceptance
   row**, which is a different thing from lacking a test. Questions 4 and 5 are
   therefore about the *scope* of an existing green check, not about whether one
   exists.
3. **`test_phase_boundary.py` already exists and enforces statically.** The draft
   treated the import limb as purely prospective. The module is 266 lines and
   walks `src/` and `scripts/` with `ast`; the approved contract
   `assert_phase_boundary(phase, *, loaded_modules)` is a **run-time** check on
   `sys.modules`. Static and run-time enforcement are not the same guarantee, and
   the bolt-plan's confidence hypothesis is explicitly about the run-time half.
   Question 7 makes that relationship the decision rather than leaving it implied.

---

## Question 1

D-24 binds its 17 items to **three different hash granularities**, and nothing
defines any of them:

| Granularity | Items | Count |
|---|---|---|
| Whole-file config hash | 12 (`seeds.yaml`) | 1 |
| Config-**section** hash | 4, 7, 9, 11, 14, 16 — plus 13 as `Source + config-section hash` | 7 |
| Config-**field** hash | 5 (`history window`), 6 (`station encoding`) | 2 |

Five of those sections live in **one file**: items 5, 9, 11, 14 and 16 all name
`configs/experiment.yaml`, and items 4 and 6 both name `configs/features.yaml`. So
"section" has to individuate five regions of one YAML file, and "field" has to
address two values inside sections that are themselves separately hashed.

This is the question that decides whether **G-P3C is usable at all**: a hash that
changes when someone reflows a comment fails the freeze spuriously, and a team
that learns to expect spurious failures stops treating a real failure as real.
Note that `foundation`'s **R-16** already forbids machine paths in any governed
config, so relocating the workspace must not move any of these hashes.

How are the config-section and config-field hashes defined?

A) Hash the raw bytes of the region as it appears in the file
   > **Impact**: Trivial and unarguable. But it changes on a comment edit, a key reorder, a quote-style change or a trailing-whitespace fix, none of which alters a governed value — and it gives no way at all to address items 5 and 6, which are single fields inside a larger hashed section. G-P3C would fail on formatting, indistinguishably from a real change.

B) Hash a canonical serialization of the parsed region — keys sorted, comments dropped, scalars normalised — at whichever granularity the item names
   > **Impact**: Stable against every formatting change and sensitive to every value change, which is the required behaviour, and it addresses all three granularities uniformly. Costs a canonicaliser that must itself be frozen, because changing *how* you canonicalise changes every hash — so the canonicaliser's own version belongs in the manifest.

C) Give every item an explicit key list — each of the 17 names the exact config keys it covers, and the hash is taken over exactly those
   > **Impact**: Most auditable: a reviewer can see precisely which fields item 9 protects, and the field/section distinction disappears because everything is a key list. But it is 17 hand-maintained lists, which is the `DP-DATA-01` failure mode — a key added to a grid and not added to the list is silently unprotected, and item 9's grids are exactly where keys get added.

D) B for the hash, plus C as an asserted completeness check — canonical serialization at the item's granularity, with a per-item key list asserted to cover its region and no other item's
   > **Impact**: Stability from B, auditability from C, and the list's completeness machine-checked rather than trusted. The "and no other item's" clause matters here specifically: without it, items 5 and 9 both sit in `experiment.yaml` and nothing detects an overlap that would let one item's change hide inside another's hash. Costs both mechanisms plus one reconciling test.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D, with the canonicaliser version recorded in the manifest and the section/field boundaries stated per item in `business-rules.md`. Option A cannot express items 5 and 6 at all, which by itself rules it out. Option C alone reintroduces the silent-gap failure this project has now corrected four times. D costs one extra test and buys a freeze that fails only when something real changed — which is precisely what G-P3C's empty-diff pass condition is supposed to mean.

[Answer]: D — accepted with the amendments below, recorded verbatim as the human wrote them. Two of them modify the option as offered (the overlap rule and item 13's composition) and one imposes a raise-don't-assume constraint on item 12; all three are binding on the artifacts.

> Define config-section and config-field hashes as SHA-256 hashes over a versioned canonical serialization of the parsed YAML value at the exact granularity authorized by D-24.
>
> Each protected item must have an explicit canonical YAML path and an asserted key inventory. A mechanical completeness test must reconcile that inventory with the parsed governed region so that adding, deleting, or renaming a governed key cannot leave it silently unprotected.
>
> Record the canonicaliser identifier and version in the transition manifest. The canonicalisation contract must define mapping-key ordering, sequence-order treatment, scalar typing and normalization, Unicode and encoding, duplicate-key rejection, alias or merge-key handling, and rejection of unsupported or ambiguous values. Comments, whitespace, quote style, mapping-key order, and workspace relocation must not change the hash; governed value changes must change it.
>
> Modify the proposed non-overlap rule: reject undeclared overlap, but permit explicit parent-section/child-field overlap where D-24 intentionally protects both a section and a field within it. Every permitted overlap must be declared and tested so that a change cannot be hidden or ambiguously attributed.
>
> For item 13, compute the source hash and config-section hash independently and combine them using a versioned, domain-separated representation.
>
> Preserve item 12's approved whole-file semantics. If applying semantic YAML canonicalisation to the whole-file hash would change D-24's meaning, raise that as a governed amendment rather than assuming it.
>
> State the section and field boundaries per item in business-rules.md and verify the complete mapping mechanically against D-24 before G-P3C.

---

## Question 2

`build_transition_manifest` must hash all 17 items. **Today none of the governing
artifacts exists** — no config file, no `src/` package, no run record. And even
once they do, some items are legitimately absent at a given moment: item 10
(selected hyperparameters, governed by a *run record*) cannot exist before tuning
has run, and item 2 (architecture serialization) cannot exist before a model has
been built.

So the manifest is unbuildable now and *partially* unbuildable for most of Phase 1.
What does it do about an item whose governing artifact is absent?

A) Raise — a manifest that cannot hash all 17 items is not a manifest
   > **Impact**: Strongest guarantee at the freeze, which is the only moment G-P3C cares about. But it makes the manifest unbuildable at every earlier moment, so it cannot be exercised, tested or demonstrated until the last Bolt — and a mechanism first run at a freeze gate is a mechanism first debugged at a freeze gate.

B) Record the item with an explicit `absent` sentinel, and raise only when the manifest is built *for a freeze*
   > **Impact**: Buildable and testable from Bolt 2 onward with the full guarantee retained where it counts. Requires a draft-versus-freeze build mode, and that mode must be recorded **inside** the manifest, so a draft can never be mistaken for a freeze by a later reader or by `diff_protected_hashes`.

C) Record `absent` always, no build modes, and let `diff_protected_hashes` treat `absent → present` as a difference
   > **Impact**: Uniform and simple. But nothing then prevents freezing a manifest with sixteen `absent` entries, and G-P3C's empty-diff pass condition becomes satisfiable by a manifest that protects almost nothing — the precise failure `component-methods.md` means when it says a short list must not pass silently.

D) B, plus the freeze-mode build additionally asserting the key set equals D-24's 17 items exactly — no missing key, no extra key, and no `absent` value
   > **Impact**: Closes C's failure mode, which is a *short or hollow* list, and only an explicit membership-and-cardinality assertion catches it. This is what `component-methods.md` already demands when it says the key list is asserted equal to the canonical set "so a short list cannot pass silently"; B alone leaves the assertion unstated.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. The approved design already requires the key-list assertion, so B alone under-delivers against it and C actively defeats it. The draft/freeze distinction earns its cost by letting the transition manifest be exercised ten Bolts before it is relied on — and this project's affirmed posture is that reproducibility and determinism are *executable*, not asserted. Recommend also that the draft/freeze flag be a field of `TransitionManifest` itself rather than a build-time argument, so it survives serialization.

[Answer]: D

---

## Question 3

`diff_protected_hashes` returns the differing keys, and an empty mapping is the
**G-P3C pass condition**. `component-methods.md` carries a standing caution:
until BLK-06's implementation limb is discharged, *"an empty
`diff_protected_hashes` result must not be read as proof that no protected item
changed."* Question 2's assertion needs an authoritative 17-item list to check
against. Where does that list live?

Note the circularity this creates, which is real and not hypothetical: items 5, 9,
11, 14 and 16 all hash sections of `configs/experiment.yaml`. A list stored in
that file sits inside a file it protects, so adding an item to the list changes
the hash of a section the list itself governs.

A) A literal in `phase_contract.py`
   > **Impact**: Adjacent to the code that uses it and versioned with it. But `project.md` § Forbidden prohibits hiding a scientific constant in source, and the canonical protected set is a governed enumeration frozen by a D-number, not an implementation detail. It would also put a governance list outside the config-hash net entirely.

B) In `configs/experiment.yaml`, read through `foundation`'s `ConfigSnapshot`
   > **Impact**: Governed, versioned, hashable, and reachable through the one sanctioned config path (`foundation` R-15 makes `foundation` the only reader of `configs/`). Consistent with the rule that every governed constant lives in one of the four config files. Leaves the circularity above unaddressed.

C) Derived at run time from D-24 by parsing `evidence/DECISIONS.md`
   > **Impact**: Single source of truth, and D-24 genuinely is the authority. But it makes a governance prose document a runtime dependency and a parse target, and a decision record's table formatting is not a stable interface — it will break the first time someone reflows a row.

D) B with the circularity resolved explicitly — the list in `configs/experiment.yaml` under a section excluded from every item's section hash, with a test asserting both the exclusion and that no *other* section is excluded
   > **Impact**: Keeps the list governed and hashable while making the one genuine circularity a named, tested exclusion rather than a latent bug. The second clause matters: an unbounded exclusion mechanism is a hole, so the test must assert the exclusion list has exactly one member. Costs stating the exclusion in two places — the config and the test — which is where a reviewer would look for it.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A is barred outright by `project.md` § Forbidden. C turns a decision record into a runtime parser target. D is B with the circularity handled openly instead of discovered later, and the circularity is not avoidable by choosing a different file: any of the four configs could hold the list, and items 4, 6, 7 and 12 mean `features.yaml`, `data.yaml` and `seeds.yaml` are all hashed too.

[Answer]: D — the 17-item list lives in `configs/experiment.yaml` under a section excluded from every item’s section hash, with the exclusion stated in both the config and the test, and the test asserting the exclusion list has exactly one member.

---

## Question 4

`assert_no_december_outside_restricted(evidence_root)` walks `evidence/`
recursively and returns any December-bearing artifact found outside the restricted
root; an empty sequence is the pass condition. FR-P1-02-6's criterion is broader
than the current implementation: *"No file under `evidence/` at any depth, outside
`evidence/locked_test_restricted/`, contains a record whose observation date falls
in December 2022."*

**What the existing green check actually covers, read from the code.**
`tests/test_acquisition_window.py` sets `RAW_RECORDS = "madrigal_coverage_raw_records.csv"`
and its `_record_csvs_at_any_depth()` helper returns `EVIDENCE_DIR.rglob(RAW_RECORDS)`
minus anything under the restricted root. So the walk is **one filename**, not a
content class. Inventory of `evidence/` by filename shows 16 instances each of
`madrigal_coverage_raw_records.csv`, `madrigal_coverage_summary.csv`,
`madrigal_coverage_monthly.csv`, `sha256_manifest.json` and
`request_manifest.json`. Only the first is scanned.

`madrigal_coverage_summary.csv` carries columns `december_days_present` and
`december_coverage_pct`. Scanned on 2026-08-22, **every non-zero instance is
already under the restricted root** — so the check is green *and* the gap is
latent rather than currently breached. A December-bearing
`madrigal_coverage_summary.csv` appearing outside the restricted root tomorrow
would pass.

What does this unit's guard walk?

A) Keep the existing scope — the one raw-records filename, at any depth
   > **Impact**: Zero new work, and it preserves a green check. But it makes the guard's coverage a filename convention, and the `DATA-01` finding is that a narrowed glob "silently stopped checking the artifacts that matter most" — the same shape of defect, one level up. The pass would keep meaning less than FR-P1-02-6's criterion says.

B) Every parseable CSV under `evidence/`, discovered by extension
   > **Impact**: Covers all three coverage CSVs including the summary aggregates, at low cost. But it silently skips the JSON manifests, the HTML driver captures and `experiment_registry.md`, and "parseable" quietly becomes "whatever the CSV reader accepted" — a file that fails to parse disappears from the result rather than being reported.

C) Every file under `evidence/`, dispatched to a declared parser per artifact class, with an **unparseable file treated as a failure** rather than a pass
   > **Impact**: Matches FR-P1-02-6's stated criterion. A file the guard cannot read is exactly where a December record would hide, so treating it as clean is the one answer that cannot be defended. Costs a parser table and occasional friction on a genuinely irrelevant unparseable file — resolved by an explicit, recorded exclusion rather than by silence.

D) C, plus a declared artifact-class registry asserted to cover every filename present under `evidence/`
   > **Impact**: Closes the last gap — under C, a new artifact class with no parser is a failure the first time it appears, which is correct but arrives as a surprise mid-run. An asserted registry surfaces the unhandled class at design time instead. Costs a registry that must be updated when a new artifact class is introduced, and that update is the intended friction.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. It satisfies the requirement's own wording, and the unparseable-equals-failure clause closes the only hiding place. D is attractive and I would not argue against adding it later, but it front-loads a registry before any of the artifact classes it would enumerate is produced by this pipeline — the current 16-instance inventory is all pre-TC-06 evidence. C's failure-on-unknown gives the same protection without freezing a registry against artifacts that do not exist yet.

[Answer]: C

---

## Question 5

Question 4 settles *which files* the guard opens. This settles *what counts as a
hit*, and the two answers together are what "December-bearing" means. Three
distinct things were found under `evidence/` outside the restricted root:

1. **A raw December target record** — the case the guard was written for. None
   currently exists outside the restricted root; D-15 relocated them all.
2. **A December-derived aggregate** — `madrigal_coverage_summary.csv`'s
   `december_days_present` / `december_coverage_pct` columns. A count *about*
   December, carrying no target value.
3. **A December-dated driver capture** —
   `evidence/audit_ec1_2026-08-15/kyoto_dst/dst_provisional_202212.html`, present
   outside the restricted root today. Hourly Dst for December 2022: a record whose
   observation date falls in December, and not a target value.

FR-P1-02-6 says *"Any file containing a December 2022 target value is a locked-test
artifact"* but its criterion says *"a record whose observation date falls in
December 2022."* Those two sentences do not pick out the same set, and case 3 is
the difference. `project.md` § Forbidden also bars December from informing model
selection, feature selection, thresholds or hyperparameters — with the trigger
being December being **seen**, not the lock being opened.

What is a hit?

A) Target values only — case 1
   > **Impact**: Narrowest, and it matches the requirement's first sentence and the guard's original purpose. Leaves the December Dst capture and the December coverage aggregates outside the guard entirely, which is defensible for Dst (diagnostic-only, never a confirmatory feature) but leaves the aggregates unaddressed.

B) Target values and target-derived aggregates — cases 1 and 2
   > **Impact**: Covers the channel that actually matters for the § Forbidden rule: a December coverage figure sitting in an unrestricted summary is December being *seen* without an access-log row. Costs deciding, per artifact class, which columns are target-derived — a judgement the guard has to encode.

C) Any record whose observation date falls in December 2022 — cases 1, 2 and 3
   > **Impact**: Matches the criterion's literal wording and needs no target-versus-driver judgement in the guard. But it turns the December Dst capture into a violation, which would force a driver file under the restricted root and route every ordinary Dst read through `open_restricted` — a real cost for a series that is diagnostic-only and must never be a model input.

D) B, with case 3 handled by a separate recorded exclusion naming the driver classes and why they are excluded, tested to be exactly that set
   > **Impact**: Gets B's protection while making the driver carve-out explicit and bounded rather than an unstated omission — and the exclusion is where a reviewer would look to check that a *target* file has not been mislabelled a driver. Costs one exclusion list and the test that pins its membership.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. Option A leaves the aggregate channel open, which is the one that bears on the § Forbidden rule about December being seen. Option C is literal but would sweep a diagnostic-only driver series into locked-test custody and make every Dst read an access-logged event, which buys nothing the lock is for. D states the target/driver line as a tested exclusion rather than leaving it to the reader — and it is the only option under which mislabelling a target file as a driver is detectable.

[Answer]: D

---

## Question 6

`open_restricted` writes the access record **and flushes it** before returning the
path, and **raises when the registry write fails** — *"a failed log write must
abort the read, not proceed unlogged."* The ordering is the requirement (`VAL-2`,
FR-P1-02-3): an access recorded after the fact **fails** the ordering check rather
than satisfying it.

Two facts constrain where the proof can live. `tests/test_locked_test_guard.py` is
owned by **`features-and-splits`**, not this unit — ADR-03 splits the guard
deliberately, and assigning that test here would close a cycle. And story-map
Table 2 records `RES-01`: **permitted-read access logging is NOT TESTED**, with
its candidate §19 criterion owned by stage 3.2.

So this unit must prove its own contract without owning the test that covers both
limbs. How is log-before-read *proven* rather than intended?

A) Code review of the call order
   > **Impact**: No machinery at all. But this is the single most governance-critical sequence in the project, and "we looked at it" is the evidence class this project's affirmed methodology explicitly rejects — §16 and §19 both state that visual inspection alone is insufficient.

B) A test that patches the registry writer to fail and asserts the read never happens
   > **Impact**: Proves the abort limb directly, and that is the limb where the breach lives — an unlogged read. Straightforward against a synthetic restricted root, and it belongs to this unit rather than to `features-and-splits`.

C) B, plus a test asserting the log row is durable on disk before the read is attempted
   > **Impact**: Proves both limbs — abort-on-failure *and* flush-before-read. The second is what distinguishes this contract from one that logs and reads inside a single buffered transaction, where a crash loses the row and keeps the read. Two tests, no new fields.

D) C, plus a positive-path test for the **permitted** pre-G-05 coverage read, so `RES-01` stops being untested
   > **Impact**: The only option that closes a recorded residual obligation rather than leaving it to stage 3.2. `inventory-and-registry` performs that audit through this unit's contract, so a test here proving a permitted read is logged before it proceeds covers the shape of it. Risk: the test would exercise this unit's contract against a synthetic root, not the real audit, so it must not be claimed as evidence that the real audit was logged.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C, with `RES-01` raised at this stage's gate rather than absorbed. C proves both limbs of the stated contract with two tests this unit can own. D is the more ambitious answer and its instinct is right — an untested permitted read is a real gap — but `RES-01` is recorded as owned by stage 3.2 under Vision §15.2, and closing it here with a synthetic-root test would produce evidence that looks like coverage of the real audit and is not. Recommend C plus an explicit gate note that `RES-01` remains open.

[Answer]: C — and `RES-01` is raised at this stage’s gate as still open, not absorbed here.

---

## Question 7

FR-P1-03-2 requires **two independent pass/fail results**, and
`component-methods.md` states that *"neither this nor `assert_phase_boundary`
substitutes for the other."* Two things are unsettled, and they are connected.

**The import limb already has a static implementation that the contract does not
describe.** `tests/test_phase_boundary.py` exists — 266 lines — and enforces by
walking `src/` and `scripts/` with `ast`, skipping explicitly (never passing
vacuously) where the subject does not exist yet. The approved contract is
`assert_phase_boundary(phase, *, loaded_modules=sys.modules)`, a **run-time**
check at step 4 of the stage entry contract. `bolt-plan.md`'s confidence
hypothesis is *"that the prohibitions are enforced at run time, not only in
tests"*, because a Kaggle session carries no git working tree and a static scan of
a local checkout proves nothing about the process that actually ran.

**The produced-field limb has no defined call site at all.** `assert_no_raw_fields`
is specified but `services.md`'s six-step entry contract places only
`assert_phase_boundary` (step 4). Reading `services.md` § The nine stage scripts,
**eight** scripts are Phase-1-reachable and write artifacts: `00_acquire_prepared_vtec`,
`01_inventory_and_registry`, `02_standardize_prepared_target`, `03_verify_processing`,
`04_build_external_products`, `05_build_features_and_splits`, `06_train_and_predict`,
`07_evaluate_and_report`. (`02_build_vtec_target` is Phase 2 by definition and is
the one script that skips step 4; `run_walking_skeleton` is the orchestrator.)

How do the two limbs run, and what is the existing static test's standing?

A) Static only — the existing `ast` scan is the enforcement; add a field scan to it
   > **Impact**: Already written, and it catches a forbidden import before anything executes, which is earlier than run time. But it defeats the bolt-plan's confidence hypothesis outright: no static scan of a checkout constrains a Kaggle session, and a dynamic import assembled from a string is invisible to `ast`.

B) Run-time only — implement both contracts as specified and retire the static scan
   > **Impact**: Matches the approved contracts exactly and holds inside the Kaggle session. But it discards a working guard that fires before execution, and it moves first detection of a forbidden import from "any test run" to "the run that would have violated the boundary".

C) Both, with declared roles: the static scan as the early-warning limb, the run-time assertions as the authoritative limb, and `assert_no_raw_fields` called by each of the eight Phase-1 producing scripts before it writes
   > **Impact**: Keeps the existing green check, satisfies the run-time hypothesis, and gives the field limb a call site that respects the dependency direction — `governance-guards` depends on `foundation`, so putting the field check inside `foundation`'s release path would close a cycle. Per-script obligation means a ninth script that forgets the call is silently unchecked.

D) C, plus a completeness test asserting every Phase-1 producing script calls `assert_no_raw_fields` before its first write
   > **Impact**: Turns C's omission from a silent gap into a test failure, and it is the same shape as the `RequiredFieldsMap` completeness assertion `foundation` already adopted under R-03 — one pattern used twice. The enumerating test must itself stay current, but it fails loudly rather than quietly when it does not.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A cannot deliver the run-time guarantee the Bolt's confidence hypothesis names, and B throws away enforcement that already works for no gain. The alternative call sites for the field limb are both worse: inside `foundation`'s release API it would invert the dependency and close a cycle; at the transition-manifest build it would catch a contaminated frame only after every Phase 1 artifact was written and possibly consumed — a post-mortem, not a guard. Recommend also that `business-rules.md` state the static scan's *subordinate* status where the code lives, so a future maintainer cannot read its presence as sufficient.

[Answer]: D — and `business-rules.md` states the static scan’s subordinate status where the code lives, so its presence cannot be read as sufficient.

---

## Question 8

The §10.1 reuse register carries **all fifteen fields** and must be recorded
**before the code is used** and before gate G-P2. FR-P1-06-3 additionally requires
the adapter pattern — reused code lives behind a project-owned adapter and is
**never pasted into a notebook**. NFR-LIC-01 is accepted by **TA-28**, which this
unit owns outright with no supporting unit.

"Before the code is used" is an ordering claim about a human act. How is it
enforced?

A) Procedural — the register is filled in when a developer copies code
   > **Impact**: How such registers usually work, and it costs nothing. But it is unenforced, and this register's purpose is licence compliance, where an unrecorded copy has legal consequences rather than merely audit ones. TA-28 would reduce to an attestation.

B) A test asserting every third-party-derived module has a complete register row
   > **Impact**: Machine-checkable, and `tests/test_reuse_registry.py` is already mandated. But it needs a way to know a module *is* third-party-derived, and that is the hard part: an unregistered copy is indistinguishable from original work by inspection.

C) B, keyed on a mandatory provenance marker every adapter module must carry
   > **Impact**: Makes the check tractable in both directions — the register is asserted complete against the set of marked modules, and an unmarked module is asserted to contain no reuse. Costs a convention, but a missing marker is itself visible at review, and the marker gives TA-28 something to point at.

D) C, plus the standing default recorded as the primary control: reimplement from the paper with a citation rather than copy
   > **Impact**: Matches the rule actually in force — `project.md` § Forbidden bars copying source whose licence is absent, ambiguous or incompatible, and FR-P1-06-4 makes reimplementation the standing default while the AGPLv3 question is open. Under D the register becomes the **exception** path rather than the expected one, and the design reflects that ordering instead of inverting it.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. The project already has a standing rule making reimplementation the default and copying the exception, so designing the register as the main road would misrepresent the policy in force. The AGPLv3 Global-TEC-forecasting repository remains the only approved direct-copy source, and whether its distribution obligations permit that copying is an **unresolved governance dependency this project does not settle** — which is itself a reason to make copying deliberately harder to reach than reimplementation.

[Answer]: D

---

## Question 9

`component-dependency.md` § Shared resources states without qualification that
`evidence/locked_test_restricted/` is reached by `data.locked_test` alone and
*"nothing else may construct a path into it."* `foundation`'s **R-15** already
states its own side of that as the absence of a path, enforced by a static check.

**BLK-07** records that `acquisition`'s routing through `open_restricted` was
never captured — and `acquisition` is the unit that reads the D-9 input
`audit_evidence_2022-FULL/`, which now lives under the restricted root. Four
downstream consumers reach that root through this unit's contract:
`inventory-and-registry` (the pre-G-05 coverage audit), `acquisition` (the D-9
input and any December re-acquisition), `features-and-splits` (the locked
partition) and `evaluation-and-comparison` (the locked evaluation). BLK-07 is an
**exit condition on this stage**, and no acquisition run may touch calendar
2022-12 while it stands.

How does this unit's design treat the single-chokepoint rule?

A) State the rule and rely on the four consumers to honour it
   > **Impact**: Minimal, and it keeps the rule in the design where it was written. But D-15 records *why* the boundary matters — it is a **governance boundary, not an access control**, so it holds only while exactly one code path reaches it. A rule that depends on four units remembering is not "exactly one path".

B) A static check asserting no module outside `locked_test.py` contains the restricted-root literal
   > **Impact**: Makes the single-path claim machine-checkable across the whole tree, and it is cheap — the same grep-class assertion R-15 already applies to `foundation`, generalised. Catches the accidental second path, which is the realistic failure. Does not catch a path assembled at run time from fragments.

C) B, plus `open_restricted` raising when its caller is not one of the four recorded consumers
   > **Impact**: Closes the run-time-assembly gap too. But it makes this unit's guard depend on knowing its callers, coupling a root unit to four downstream units — the coupling the DAG was arranged to avoid, and the reverse edge would close a cycle.

D) B, plus BLK-07 raised at this stage's gate as an open item with the four consumers enumerated and `acquisition`'s routing named — not closed here
   > **Impact**: Gets B's enforcement while keeping BLK-07 where it belongs: the question of which units are *authorised* to reach the locked month is the owner's, not a design document's. It also honours the exit-condition framing — the blocker is discharged by an owner decision recorded at the gate, not by an artifact asserting it away.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. B is the right mechanism, and C's extra coverage costs the acyclic structure that keeps this unit a root — a high price for a failure mode (run-time path assembly) that the static check plus review makes unlikely. BLK-07 is an authorisation question rather than a design question, so it goes to the gate. Note that B has a live consequence worth stating: `acquisition` cannot hold its own path to `audit_evidence_2022-FULL/` once the check exists, so BLK-07's resolution is a precondition of Bolt 3, not a formality.

[Answer]: D — B’s static check is the mechanism; BLK-07 is raised at the gate as an authorisation question with the four consumers enumerated and `acquisition`’s routing named, and its resolution is a precondition of Bolt 3.

---

## Assumptions & Open Questions

- **[assumption]** `tests/test_locked_test_guard.py` is **not** this unit's. ADR-03 splits the guard deliberately — the access-log limb here, the execution limb in `features-and-splits`'s `splits.py` — and the test covering both limbs is owned by `features-and-splits` to keep this unit a root. Story-map Table 2 confirms `features-and-splits` owns WS-18 and TA-18 with this unit supporting.
- **[assumption]** `RAW_MODULES` names **four** `gnss` modules — `rinex`, `calibration`, `target`, `verification` — not the two that FR-P1-03-2's earlier wording listed. `target.py` and `verification.py` were added per finding `IMPL-2`, and the existing `tests/test_phase_boundary.py` already encodes all four. This stage designs to four.
- **[assumption]** Rule IDs continue `foundation`'s single sequence rather than restarting per unit. `foundation`'s `business-rules.md` runs R-01 through R-17, so this unit opens at **R-18**. If per-unit numbering was intended, say so at the gate and the artifacts will restart.
- **[assumption]** NFR-PHASE-01's transition-manifest hash-diff test has **no module in the TE §12 tree** and needs frozen artifacts from every later unit. Story-map Table 2 carries it on `fixtures-and-reproducibility` with this unit supporting. Not this unit's to build.
- **[assumption]** TA-27's second limb (Phase 2 cannot change protected forecasting hashes) is accepted at G-P2 and G-P3C, **outside Phase 1**, per the bolt-plan's Acceptance-rows line. Only the first limb is acceptable inside this initiative.
- **Open — BLK-06's per-item binding.** D-24 resolved the enumeration and cardinality at **17 items**, calculated rather than assumed. The **binding to concrete config fields and file paths is PENDING**, and D-24's own consequence 2 records that no file path or field name in its table is claimed to exist today. Questions 1–3 produce that binding evidence; **BLK-06 is not closed by this stage**, per the `DP-CHAIR-02` ruling.
- **Open — BLK-07, an exit condition on this stage.** `acquisition`'s routing through `open_restricted` is unrecorded, and Question 9's static check would make `acquisition`'s current direct path to `audit_evidence_2022-FULL/` a violation. The mechanism is a design question; the authorisation is the owner's, and it goes to the gate.
- **Open — `RES-01`, permitted-read access logging is NOT TESTED.** Recorded in story-map Table 2 with its candidate §19 criterion owned by stage 3.2 under Vision §15.2. Question 6 option D would close it here; the recommendation declines to, and raises it at the gate instead.
- **Open — FR-P1-02-6 has no §16/§19 acceptance row.** It *is* enforced, by `tests/test_acquisition_window.py::test_locked_month_values_exist_only_under_the_restricted_path`, and it *is* currently green. Questions 4 and 5 both narrow or widen what that green means. Whichever is chosen, the requirement still lacks an acceptance row and remains this unit's 1-of-10.
- **Open — a stale statement in two approved artifacts, reported not edited.** `component-methods.md`'s `TransitionManifest` comment reads *"Final enumeration and cardinality are DEFERRED TO STAGE 3.1; this design states neither"*, and `unit-of-work.md` § 2 and `components.md` line 61 say the same. **D-24 has since resolved the enumeration at 17 items**, and `bolt-plan.md` § Bolt 2 already reflects that. Per `CHANGE_RECORD_PROCEDURE.md` a sweep reports on approved-stage artifacts and does not edit them absent owner approval for annotate-in-place. Raised at the gate.
- **Open — the AGPLv3 distribution question.** Whether the Global-TEC-forecasting repository's obligations permit direct copying is a governance dependency **this project does not resolve**. The standing default is reimplementation from the paper with a citation (FR-P1-06-4).
- **G-09 is not signed.** No answer here authorises creating `phase_contract.py`, `locked_test.py` or `reuse_registry.py`.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

---

## Consolidated Summary Confirmation

Questions 1 and 2 were already answered (D with amendments; D). Questions 3–9 are
answered above as the recommended option in each case, on the owner's instruction
to apply the recommendations. Consolidated:

| Q | Answer | What it settles |
|---|--------|-----------------|
| 1 | D (with the owner's three amendments) | BLK-06's 17 items expressed with canonicaliser version recorded in the manifest and section/field boundaries stated per item |
| 2 | D | Key-list assertion plus the draft/freeze distinction, the flag a field of `TransitionManifest` |
| 3 | D | The 17-item list lives in `configs/experiment.yaml` under one section excluded from every item's section hash; a test asserts the exclusion and that the exclusion list has exactly one member |
| 4 | C | The guard walks every file under `evidence/`, dispatched to a declared parser per artifact class; an unparseable file is a **failure**, not a pass. No artifact-class registry is frozen yet |
| 5 | D | A hit is a target value or a target-derived aggregate; December-dated **driver** captures are a separate recorded exclusion naming the driver classes, tested to be exactly that set |
| 6 | C | Two tests owned by this unit: registry-write failure aborts the read, and the log row is durable on disk before the read is attempted. `RES-01` stays open and is raised at the gate |
| 7 | D | Both limbs with declared roles — static scan subordinate/early-warning, run-time assertions authoritative; `assert_no_raw_fields` called by each of the eight Phase-1 producing scripts before it writes, plus a completeness test over those call sites. `business-rules.md` records the static scan's subordinate status |
| 8 | D | Provenance-marker-keyed register test, with reimplementation-from-the-paper recorded as the **primary** control and the register as the exception path |
| 9 | D | Static check that no module outside `locked_test.py` contains the restricted-root literal; BLK-07 raised at the gate with the four consumers enumerated and `acquisition`'s routing named — not closed here |

Carried to the gate, unchanged by these answers: `RES-01` still untested; BLK-07
still open and a precondition of Bolt 3; BLK-06 not closed by this stage; FR-P1-02-6
still has no §16/§19 acceptance row; the stale `TransitionManifest` deferral
statement in three approved artifacts reported, not edited; the AGPLv3 distribution
question unresolved; G-09 unsigned.

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

### Re-confirmation, 2026-08-23 — after a stage-wide redo jump

A redo jump on `functional-design` reset the receipt floor for every unit of this stage.
No answer above changed. **What this redo also does for this unit: it resets the exhausted
adversarial reviewer budget.** The three artifacts were regenerated against this
nine-question set after the 2-iteration budget had been spent on the previous issue, so
those changes have never been reviewed. A fresh pass follows this confirmation.

### Re-confirmation, 2026-08-23 (second) — after a second stage-wide redo jump

A redo jump aimed at correcting `external-products` reset the receipt floor for every unit.
**No answer above changed.** Since the first re-confirmation this unit reached **READY** on
its iteration-2 adversarial pass, after a Critical arithmetic slip in the § W-3a taxonomy
sum was corrected — the printed proof summed to 15 where it asserted 17.

### Re-confirmation, 2026-08-23 (third) — after a third stage-wide redo jump

A redo jump aimed at correcting a **misreading of `component-methods.md` § Depth** reset the
receipt floor for every unit of this stage. **No question, option, answer or amendment on
this unit changed.**

### Re-confirmation, 2026-08-23 (fourth) — after a fourth stage-wide redo jump

A redo jump aimed at sweeping two **question files** that had fallen stale against their
own corrected artifacts reset the receipt floor for every unit of this stage. **No
question, option, answer or amendment on this unit changed.**

### Re-confirmation, 2026-08-23 (fifth) — after a fifth stage-wide redo jump

A redo jump aimed at correcting four stale cross-references in `target-standardization`'s
question file reset the receipt floor for every unit of this stage. **No question, option,
answer or amendment on this unit changed.** *(Answered `Looks correct`, 2026-08-23; that
receipt belongs to the previous attempt — the live answer tag for this section is the
blank one at the end of the sixth re-confirmation below.)*

### Re-confirmation, 2026-08-24 (sixth) — new stage attempt after the Inception close

**Why this is being re-asked.** Inception closed and Construction opened on
**2026-08-24T11:46:26Z**, starting a fresh `functional-design` attempt. A fresh attempt
resets the receipt floor for every unit: the fifth re-confirmation above no longer
satisfies it. Unit 1 `foundation` re-confirmed at 12:36:34Z and its artifacts were
amended; `governance-guards` is unit 2.

**What happened upstream since the fifth re-confirmation, and why it leaves this unit's
answers untouched.** `foundation` ran an amendment pass, executed and recorded in
`governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md`:

| | Ruling | What it touched | Why this unit is unaffected |
|---|---|---|---|
| **A** — §19 rows for REQ-ENG-7 / REQ-ENG-10 | **DECLINED** | nothing | **No count moved.** This unit's derived figures stand: 10 requirements, **1** with no acceptance row (FR-P1-02-6); owns TA-27 and TA-28; supports WS-18, TA-07, TA-18 |
| **B** — three `DeterminismRecord` fields | **APPROVED** | `component-methods.md` — `DeterminismRecord` **6 → 9** fields | `DeterminismRecord` is a `foundation` contract. This unit cites `component-methods.md` for `RAW_MODULES`, `assert_phase_boundary`, `assert_no_raw_fields`, `TransitionManifest`, `build_transition_manifest`, `diff_protected_hashes`, `RESTRICTED_ROOT`, `AccessRecord`, `open_restricted`, `assert_no_december_outside_restricted` — none amended |
| **C** — release-history ledger | **APPROVED** | `services.md` § Run record and registry (**two → three** artifacts); `unit-of-work.md` § 1 `Owns` | This unit cites `services.md` § Stage entry contract, § The nine stage scripts and § Execution platforms, and `unit-of-work.md` **§ 2** — none amended |

The change record's own sweep states the same conclusion independently, under
§ Report-only files: *"other units' `functional-design/` artifacts, verified
unaffected."*

**What still stands, unchanged.** All nine answers (1=D with the owner's three
amendments, 2=D, 3=D, 4=C, 5=D, 6=C, 7=D, 8=D, 9=D). Carried to the gate: `RES-01`
permitted-read access logging still **NOT TESTED**; **BLK-07** still open and a
precondition of Bolt 3; **BLK-06** not closed by this stage; **FR-P1-02-6** still with no
§16/§19 acceptance row; the stale `TransitionManifest` deferral statement in three
approved artifacts reported, not edited; the AGPLv3 distribution question unresolved;
**G-09 unsigned**, so nothing here authorises creating `phase_contract.py`,
`locked_test.py` or `reuse_registry.py`.

**One thing this confirmation does change.** The three artifacts on disk, and their
iteration-2 **READY** verdict of 2026-08-22, belong to the previous attempt. On
confirmation they are re-saved and re-reviewed under this attempt, so the verdict that
reaches the gate is one this attempt actually produced.

Does this all look correct before the stage proceeds?

- Looks correct
   > **Impact**: The confirmation receipt is recorded for `governance-guards` under this attempt. The three artifacts are re-saved and put through a fresh reviewer pass, then the stage moves to unit 3. No answer, contract or scientific value changes.

- Request changes
   > **Impact**: No receipt is recorded and nothing is re-saved. Tell me what to change — an answer, a carried-to-gate item, or the reading of the amendment pass above — and I re-present before touching anything.

> **💡 Recommendation**: **Looks correct** — the amendment pass touched three `foundation` contracts this unit does not cite, Amendment A was declined so no count propagated, and the change record's sweep independently verified this unit's artifacts unaffected. Re-confirming records the receipt this attempt needs without reopening a settled answer.

*(Answered `Request changes`, 2026-08-24 — the owner named two execution defects to
resolve. The verification pass below is the response; the live answer tag for this section
is the blank one at its end.)*

### Verification of the two execution defects raised at the sixth confirmation

The owner answered the sixth confirmation by naming the two defects the `foundation`
amendment pass introduced during execution — **a duplicate bullet**, and **corrupted
footers caused by letting bash treat backticks as command substitution** — and asked that
they be resolved. Both were checked against the workspace rather than against the change
record's account of them. **Both are already resolved on disk; neither needs an edit.**

| Defect | Check run | Result |
|---|---|---|
| Duplicate `RequiredFieldsMap` / `CredentialNameMap` bullet | `grep -n "RequiredFieldsMap" foundation/functional-design/business-logic-model.md` | **Two hits, neither a duplicate bullet.** Line 491 is the single § Assumptions bullet; line 598 is a prose mention inside the Review section's iteration summary. The duplicate the change record records as *"Removed"* is gone |
| Backtick / command-substitution corruption | `grep -rn '``\|$(' ` over `foundation/functional-design/` and the change record; `grep -rn "command not found\|: not found\|bash: \|syntax error near"` over the whole intent record, `governance/` and `evidence/` | **No corruption residue anywhere.** Every `` `…` `` hit is legitimate inline code; the two `` `` `UNTESTED` `` `` hits in the change record are correct nested-backtick markdown. No shell-error text, no truncated footer |

**Nothing was edited to reach this result** — the checks found the workspace already clean,
so there was no defect left to fix. The change record's own § Sweep result already recorded
both as corrected during execution; this pass confirms that record against the files.

**One stale representation found while checking, reported and not edited.**
`foundation/functional-design/business-logic-model.md` **line 598**, inside the
**iteration-1 Review section**, still reads that *"`DeterminismRecord`'s three pending
fields and the release ledger await Amendments B and C (correctly marked not-approved,
with the approved six-field contract stated as the current binding shape)"*. B and C were
approved and executed on 2026-08-24, so that sentence describes a superseded state. It sits
inside a **reviewer's verdict text** — a dated record of what that reviewer saw — not in the
design body a builder reads, and `CHANGE_RECORD_PROCEDURE.md` does not authorise editing a
recorded review. It is raised here rather than swept. It belongs to `foundation`, not to
this unit, and does not touch any `governance-guards` contract.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The confirmation receipt is recorded for `governance-guards` under this attempt. The three artifacts are re-saved and put through a fresh reviewer pass, then the stage moves to the next unit. The stale line-598 review sentence stays as raised — reported, not edited.

- Request changes
   > **Impact**: No receipt is recorded and nothing is re-saved. Use this if the two defects meant something other than what was checked above, or if you want the line-598 review sentence annotated in place rather than left as a raised item — that would need your approval as an annotate-in-place exception.

> **💡 Recommendation**: **Looks correct** — both named defects verify as already resolved with no edit required, and the one stale sentence found sits inside a dated review record that the change procedure protects from sweeping. Nothing outstanding blocks this unit.

[Answer]: Looks correct
