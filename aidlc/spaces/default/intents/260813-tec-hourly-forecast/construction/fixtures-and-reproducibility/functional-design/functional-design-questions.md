# Functional Design Questions — `fixtures-and-reproducibility`

**Unit** `fixtures-and-reproducibility` — Fixtures and Reproducibility: the two
walking-skeleton fixtures and the clean run.
**Kind** `library` · **Complexity** M · **Deployment** standalone · **Depends on**
`acquisition`, `inventory-and-registry`, `target-standardization`, `external-products`,
`features-and-splits`, `models-and-baselines`, `evaluation-and-comparison`,
`statistical-inference`, `regimes-diagnostics-reporting`.

Unit **12 of 12** — the last, and the terminal node of the DAG. It owns — **derived by
counting § 12's `Owns` list, five bullets** — `scripts/run_walking_skeleton.py` (the
orchestrator that enforces both-fixtures-in-order before any full-year job);
`tests/fixtures/plumbing_7day/fixture_manifest.yaml` and
`tests/fixtures/scientific_1month/fixture_manifest.yaml`; `tests/test_clean_run.py`; the
traceability matrix and the `environment_and_cpu_preflight_report`; and **execution** of
the M10 contract fixture in the clean-run sequence (owner ruling Q12 = C — authored by
`features-and-splits`, run here, **not** a third mandated fixture and never scientific
evidence). It owns **no `src/` module and no stage script other than the orchestrator**:
its boundary invokes every stage script and implements no domain logic of its own. Seven
of its nine dependency edges rest on a stage script the clean-run sequence invokes
directly; the two on `statistical-inference` and `regimes-diagnostics-reporting` rest on
the artifacts the clean-run tolerance comparison and TA-21's traceability matrix consume.

**8 requirements, 2 untested — derived by reading the story map's rows, and the per-unit
coverage summary agrees (row: 8 / 2 / WS-20, TA-09, TA-17, TA-21 / TA-03, TA-04, TA-23,
TA-26, TA-27)**: FR-WS-1 (WS-20, TA-09), FR-WS-4 (WS-01, WS-09…WS-20), FR-WS-5 (WS-20,
TA-17), FR-WS-6 (TA-03, TA-26), NFR-REP-01 (WS-20, TA-17), REQ-NFR-A3 (TA-03), and two
with **no current acceptance row** — FR-WS-2 (the plumbing fixture never scientific
evidence) and FR-WS-3 (December record-date exclusion). TA-09 is **bounded to 13 rows**
— WS-01 plus WS-09…WS-20 — per FR-WS-4 and `requirements.md` § Known defects row 8;
reading it as "all 20" would demand WS-02–WS-08 evidence §7.0's Phase 1 hard prohibition
bars. Two untested of eight is a figure this file must convert into designed falsifiers
or leave as recorded gaps — never silently narrow.

**One owned blocker and four inherited exit conditions stand on this stage.** **BLK-02**
(owned): the `plumbing_7day` manifest — its reading limb was settled by the D-11
clarification of 2026-08-22 (D-11's `Stations:` line is eligibility evidence; TE §15.1's
one-station execution scope retained) and its station-selection limb froze the same day
as **BSHM 32/35 (D-20)**, but the manifest itself **does not exist, the fixture has never
been run, and no measured value may be invented, inferred or substituted** (§15.1).
**BLK-03 ↓, BLK-04 ↓, BLK-08 ↓, BLK-09 ↓** (inherited from five upstream units): the
clean-run tolerance comparison and TA-21's matrix consume their released artifacts, so
what those contracts permit bounds what WS-20 and TA-17 can be said to have reproduced —
**BLK-08 ↓ in particular bounds the units of every tolerance this unit compares**: a
clean-run tolerance stated in TECU cannot be checked against output no design path
returns to TECU. All are **exit conditions on stage 3.1, not entry conditions**
(`GOV-2026-08-22-REM-01` Rec 2, extended 2026-08-23): this unit may enter, **may not
complete or exit** 3.1 while any stands, and **no implementation may proceed**.

**G-09 is not signed.** Workspace inspection 2026-08-27: `tests/` holds three modules
(`test_acquisition_window.py`, `test_phase_boundary.py`, `test_release_hashes.py`) —
none this unit's; **no `tests/fixtures/` directory exists**; `src/` and `configs/` are
absent; `scripts/` holds only the two pre-scaffold audit scripts. No answer here
authorises creating any module, manifest or fixture run.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 12 — the `Owns` list (five bullets), the responsibility (manifests carrying identity, input hashes, expected schema, row-count ranges, support and missingness limits, timestamp tolerances, required outputs, measured CPU runtime range, permitted floating-point tolerances; the orchestrator enforcing both-in-order; the §13.2 clean-run contract reproduced on CPU), the boundary (invokes every stage script, no domain logic; two artifact-only edges), the 8 requirements (2 bolded untested), acceptance rows WS-20/TA-09/TA-17/TA-21, the M10 execution ruling (Q12 = C: authored in `features-and-splits`' `test_train_only_transforms.py`/`test_split_embargo.py`, run here — what puts it inside TA-17's and WS-20's reach; **not a third mandated fixture**, §9.2 unchanged, no full-year job gates on it), the implementation notes (D-11 window 2022-11-01…07 all three cells with measured completeness ARUC 163/168, BSHM 168/168, NICO 155/168 and 7/7 day presence, the not-representative-of-December limitation; **the scientific window frozen as D-14 — March 2022, all three cells** (`CR-2026-08-21-FREEZES`), carrying its own equinox-month limitation, **no longer open under Q-31** (corrected 2026-08-22, finding `UG-08`); the Kaggle in-session rule; NFR-PHASE-01's hash-diff row carried here with `governance-guards` supporting); § Blocker register — BLK-02's limb table (reading resolved; station **RESOLVED 2026-08-22 — BSHM 32/35, D-20**, selected on the only complete observed coverage, 168/168 bins, from `evidence/audit_evidence_2022-11/madrigal_coverage_raw_records.csv`; ARUC's one-bin shortfall **DORMANT, explicitly NOT resolved**; manifest and execution **PENDING**; measured evidence **PENDING — no value exists and none is claimed**); **BLK-01 CLOSED 2026-08-22** — TE §13.2 now carries the `PYTHONHASHSEED=0` clean-run clause (`CR-2026-08-22-TE-AMEND`), so `test_clean_run.py`, WS-20 and TA-17 test the **amended** sequence.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Table 1 rows for the 8 requirements (FR-WS-2 and FR-WS-3 marked **NO CURRENT ACCEPTANCE ROW**); Table 2's WS-20 row (evidence: `tests/test_clean_run.py`, clean-run log, both fixture manifests), TA-09 row (**bounded** to WS-01 and WS-09…WS-20; evidence: fixture acceptance table with per-row evidence links), TA-17 row (full ordered clean-run contract on CPU within declared runtime, storage and numerical tolerances; evidence: `test_clean_run.py`, clean-run log, matched artifacts), TA-21 row (traceability matrix connecting each implemented requirement to a decision, test/experiment, and evidence artifact); supporting rows TA-03 (install on both platforms + `environment_and_cpu_preflight_report`), TA-04 (hash tooling operates on both fixtures), TA-23 (preflight), TA-26 (deterministic seed utility on both platforms), TA-27 (the hash-diff evidence; second limb accepted at G-P2/G-P3C, not inside Phase 1); § Per-unit coverage summary (8 / 2 / four primary rows / five supporting).
- `../../../inception/requirements-analysis/requirements.md` — FR-WS-1 (both fixtures in order before any full-year job; D-11 and **D-14** named in the requirement text); FR-WS-2 (`UNTESTED` — no result artifact cites the plumbing fixture as evidence); FR-WS-3 (`UNTESTED` — record-date exclusion, asserted on record dates never folder names; `tests/test_acquisition_window.py` named); FR-WS-4 (the 13-row Phase 1 acceptance set, WS-01 exception approved 2026-08-21); FR-WS-5 (clean CPU reproduction within declared tolerances, §13.2 sequence; `test_clean_run.py` + clean-run log + artifact comparison report); FR-WS-6 (critical set **and both fixtures inside the Kaggle session**, result captured in that run's evidence record); NFR-REP-01 (**§13.7's exact-equality classes hold exactly**: hashes, schemas, partition membership, IDs and deterministic CPU transformations compare for equality, not tolerance, and a mismatch **must not silently update the expected value** — the D-18 re-merge's traversal-order lesson, `DATA-17`); REQ-NFR-A3 (platform parity of the gate — NFR-REP-01 governs *a* clean environment, not *the* environment the governed run runs in); REQ-ENG-4 (fixture assertion data lives in `fixture_manifest.yaml` carrying **thirteen per REQ-ENG-4 as posed; the artifacts bind to §15.2's derived twelve — see `business-logic-model.md` § Assumptions** — its enumeration: identity, input hashes, expected schema, row-count ranges, support and missingness limits, timestamp tolerances, required outputs, expected CPU runtime range measured before freeze, permitted floating-point tolerances — **nine enumerated items against a claimed thirteen; the three §15.2 areas its own sentence omits are Processing, Units and Independent reference checks, and 9 + 3 = 12, the figure §15.2's table yields once its `Area` header row is dropped. Board-arbitrated 2026-08-28 on `GOV-2026-08-28-FD-01` Recommendation 30: §15.2 names twelve, this unit is correct, and REQ-ENG-4 is wrong on both limbs. Correcting REQ-ENG-4 is a `requirements.md` change outside this stage's produces list — reported at the gate, not applied** — never hardcoded in test bodies; **TE §15.4's `artifact_manifest.json` hash-listing required as well**; D-11's pre-freeze obligation on ARUC's shortfall); § Known defects rows 8 and 12; REQ-ENG-10 (the §13.1 eight-item environment lock every run captures).
- `../../../inception/application-design/services.md` — `run_walking_skeleton.py`'s row (orchestrator, phases 1 and 2, reads `--fixture`, writes the fixture run log); § Stage entry contract (foundation's six ordered steps, identical in all nine scripts — an approved surface); § Ordering contract (`run_walking_skeleton.py` **enforces** the ordering, it does not merely document it; each stage reads only artifacts a prior stage released, **identified by release ID and verified by hash**, never by path convention); the `02` ordinal collision reading (one `02` per phase, `--phase` selects); § Execution platforms (Kaggle carries **no git working tree**); the § Ordering contract's "precondition currently unmet" paragraph is **superseded on the station limb** by D-20 — cited as history, not as current fact.
- `../../../inception/application-design/component-methods.md` — § Depth (Q1 = B: full signatures at cross-package boundaries only; **this unit has no approved cross-package signature of its own** — the orchestrator is a script and the manifests are data, so every shape here is intra-unit or test apparatus, this stage's to specify, names indicative); `ConfigSnapshot` (`platform: "kaggle" | "local"`, `resolved_roots`, four config hashes); the ADR-11 `FeatureBundle` architecture and the **containment-not-equality correction** (a `score` spec covering seven days inside November — the D-11 window — **passes**, which is what keeps WS-12/WS-13/WS-20 representable); the `lead_in_hours` removal (the locked test scores 30 days, not 31).
- `../foundation/functional-design/business-rules.md` — **READY**: R-01 (all **fourteen** project exceptions derive from `IntegrityError`, base declared in `src/data/config.py`; **no fixture-specific exception is among the fourteen**; R-01 admits "any future integrity-related exception" and its negative control proves an unenumerated subclass is still caught, but the "fourteen" figure is a representation carried in foundation's READY text and in `regimes-diagnostics-reporting`'s assumptions — minting a fifteenth obliges a cross-representation sweep); R-05 (determinism first, the re-exec sentinel read once and unset; module-scope framework imports prohibited transitively); R-09/R-10 (a failed or aborted run stays visible; report honestly even when reporting fails); R-15 (only `foundation` reads `configs/`); the OPEN item that each raising unit's 3.1 declares its own exceptions.
- `../features-and-splits/functional-design/business-rules.md` — **READY**: R-74's controls-that-must-not-fire (the D-11 seven-day `score` containment **passes**; the M10-shaped negative controls: identity by enumeration over the six partition ids, exactly one enumerated `REFIT` → `DEC` exception, `fit_transforms` **equality** with the training range, `transform_id is None` raises at `fit_predict`/`06`/`07`); R-80 (the partition list: five partitions plus the locked month — frozen calendar boundaries); R-82 (the locked partition materialises only against a verified `g05_signature`); **FU-7 = A** (G-06 scores 2–31 December, 30 days); BLK-04/BLK-09's home.
- `../statistical-inference/functional-design/business-rules.md` — **READY**: R-120 clause 4 (**the widening-guard's doubled CPU cost is measured at fixture time and frozen into the fixture manifest per §15.2** — a named slot this unit's manifest schema must carry); R-121 (the planted-correlation recovery **tolerance lives in the fixture manifest, not the rule** — §13.7's fixture-derived-tolerance discipline); R-122 (fixture parameters are **declared constants of the test apparatus, explicitly not scientific values**; fixture assertion data in `tests/fixtures/<fixture_id>/fixture_manifest.yaml`, never hardcoded — the manifest convention consumed beyond the two mandated directories).
- `../evaluation-and-comparison/functional-design/business-rules.md` — **READY**: R-109 (hash-receipt before metrics, one chokepoint, exactly 2–31 December); R-104 (inverse-before-metric at the boundary — BLK-08's joint contract R-103, whose TECU bound reaches this unit's tolerances); R-111 (`test_common_masks.py` and the WS-13 proposal).
- `../governance-guards/functional-design/business-rules.md` — **READY**: R-25/R-26 (the access log appends durably **before** any December read; what counts as a December hit); R-23/R-24 (both phase-boundary limbs run) — the clean-run sequence must be executable **without** a single December hit, both fixtures being December-free by construction.
- `../acquisition/functional-design/business-rules.md` and `../inventory-and-registry/functional-design/business-rules.md` — **READY**: R-31 (membership derives from record timestamps, never from a name — FR-WS-3's mechanism); R-36 (hashing covers provider files, and **pre-TC-06 months say what they are**); R-44…R-53 (the registry and hash tooling TA-04 says must operate on both fixtures).
- `aidlc/spaces/default/memory/team.md` § Walking Skeleton — the eligibility criterion (a month is eligible when its four declared artifacts verify against its `sha256_manifest.json` and per-day coverage is present in all three cells; **derived-artifact verification, not retrieval verification**); the **DATA-07 interim caveat, binding until the `raw_isprint_cache/` re-acquisition completes**: provenance of the pre-TC-06 evidence is unverifiable in principle, and every artifact produced before the re-acquisition **must state the caveat wherever coverage figures are relied on**; completeness figures are **measured, not tested against a threshold**; D-11's mandatory limitation and the provisional-Dst restriction (selection-characterisation only — never a modelling input, a frozen tolerance, or a G-05 regime count); `team.md` § Testing Posture — the §13.2 clean-run contract as the reproducibility test's actual definition, G-07 (Blocked, Supervisor) the accepting gate, evidence `environment_and_cpu_preflight_report` plus the clean-run log and matched artifacts; the Kaggle-session practice (TC-03g, TA-03, TA-26).
- `aidlc/spaces/default/memory/project.md` § Mandated/Forbidden — both fixtures in order before any full-year job, the seven-day fixture never scientific evidence (TC-03f); CPU a complete execution path (TC-01); the in-session Kaggle rule; the two-tier error posture (integrity violations exit naming file and expectation); no scientific constant in source (TC-03e); membership never from a directory name (ML-07); stamps `phase_id`/`source_id`/`target_definition_id` on every dataset, prediction, mask and comparison; NEVER let a coding agent fill a "TBD — freeze gate" value by convenience; TE §18.3's stop-and-report posture.
- Workspace inspection, 2026-08-27: `tests/` holds three modules, none this unit's; **no `tests/fixtures/` directory**; `src/`, `configs/`, `pyproject.toml` absent; `evidence/audit_evidence_2022-11/` present (the D-11 window's lineage; D-20 selected BSHM from its `madrigal_coverage_raw_records.csv`).
- Absent by scope design: `stories` (2.4 `SKIP`), `mockups` (1.6 and 2.5 `SKIP`). `kind: library`.

---

## Question 1

**The fixture manifest as an executable contract — one schema, one loader, and where the
loader lives.** REQ-ENG-4 fixes the content: all thirteen of TE §15.2's content areas,
plus §15.4's `artifact_manifest.json` hash-listing, never hardcoded in test bodies. Two
READY siblings already consume the manifest as a contract surface: `statistical-inference`
R-120 freezes the widening-guard's measured doubled-CPU runtime **into the fixture
manifest**, and R-121 places the planted-correlation recovery tolerance there — R-122
states the `tests/fixtures/<fixture_id>/fixture_manifest.yaml` convention generally, so
the schema this unit designs is consumed beyond its own two directories. But this unit
owns **no `src/` module**: TE §7 makes scripts orchestration-only, `src/data/` is
`foundation`'s, and §12 names no module for a manifest loader — yet
`run_walking_skeleton.py` and `test_clean_run.py` must both read the same manifest.
Unstated: the schema's shape, the loader's home, and what validation rejects.

> **⚠ Marked 2026-08-28 — the question as asked, preserved as the dated interview record.**
> The preamble above and options **A**, **B** and **C** below carry REQ-ENG-4's *"thirteen"*
> §15.2 content areas, which is **what was put to the human on this date and is therefore
> kept verbatim**. It does **not** state what the design binds to. Derived after the
> answer — and board-arbitrated in this unit's favour on 2026-08-28 under
> `GOV-2026-08-28-FD-01` Recommendation 30 — **§15.2 names twelve** content areas (its table
> has 13 `^| ` rows, one of them the `| Area | Required manifest content |` header), and
> **REQ-ENG-4 is wrong on both limbs**: it asserts thirteen while enumerating nine, the three
> omitted being **Processing**, **Units** and **Independent reference checks** (9 + 3 = 12).
> **The three design artifacts bind to the named twelve** — see `business-logic-model.md`
> § Assumptions, `business-rules.md` R-133 limb 1, and `domain-entities.md` § 1. Correcting
> REQ-ENG-4 itself is a `requirements.md` change outside this stage's produces list and is
> **reported at the gate, not applied**. Every forward-looking site in this file — § Sources,
> § What will be generated, and the § Each answer row for Q1 — is marked accordingly; these
> option texts are not, because rewriting a posed question would falsify the record of what
> was asked.

A) No shared loader: the schema is documented prose, and `run_walking_skeleton.py` and `test_clean_run.py` each parse the YAML directly
   > **Impact**: Two parsers of one contract drift independently — the exact list-versus-rule failure R-01's rationale names — and R-120/R-121's cross-unit slots have no validated home, so a manifest missing a §15.2 area is discovered at 3.5 or never.

B) One schema, one validating loader: the manifest schema enumerates the thirteen §15.2 content areas as required blocks plus named cross-unit slots (R-120's measured widening-guard runtime; R-121's per-check tolerances; the §15.4 `artifact_manifest.json` cross-reference), and a single loader validates on read — rejecting a manifest missing any required area, naming the file and the missing expectation per the two-tier posture. The loader's **home is routed to the gate with the candidates named**: a function set in `foundation`'s `src/data/` by cross-unit contract (mirroring how the eight non-foundation exceptions import the base), or a test-apparatus helper under `tests/fixtures/` — because §12 names no module for it and this stage may not amend §12 by assertion
   > **Impact**: Every consumer — orchestrator, clean-run test, and the sibling test modules R-122 points at the same convention — reads one validated object, and the placement decision lands with the only authority that can make it. Costs one schema definition and a gate item.

C) B, plus the negative controls: a manifest missing any one of the thirteen content areas **fails validation** (asserted per area, by enumeration); a manifest whose §15.4 `artifact_manifest.json` is absent or whose hash-listing disagrees with the files on disk **fails**; a required-output entry with no declared comparison class (Question 6's ledger) **fails**; and the loader is asserted to be the **only** read path — a second YAML parse of a fixture manifest anywhere in this unit's scope fails a grep-style only-copy check
   > **Impact**: The manifest becomes falsifiable the way the acceptance vocabulary demands — "visual inspection alone is insufficient" — and the schema's thirteen areas are proven present rather than assumed. Costs the per-area enumeration fixtures, all synthetic.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. The manifest is this unit's central artifact and three READY siblings already treat it as an executable contract; a schema without a validating loader is prose, and a loader without controls is a promise. The home question genuinely has two defensible answers and belongs at the gate, not in an assumption.

[Answer]: C

---

## Question 2

**Measure-then-freeze: candidate versus frozen manifests, identity by citation, and the
no-silent-update rule.** TE §15.1: exact counts, tolerances and runtimes are **measured
from the fixtures and frozen, never invented** — and BLK-02 says it operationally: no
value may be invented, inferred or substituted; the manifest does not exist and the
fixture has never been run. The identities are already decided elsewhere: D-11 (window),
D-20 (station BSHM 32/35), D-14 (March 2022, all three cells). Freeze authority is the
student under Q-31, exercised under the recorded authority equivalence. NFR-REP-01 adds
§13.7: a comparison mismatch **must not silently update the expected value**. Unstated:
how "measured then frozen" becomes a workflow the design enforces rather than a sentence
it repeats.

A) The first successful fixture run writes the manifest directly — measurement and freeze are one act
   > **Impact**: Whatever the first run produces becomes the frozen expectation with no human act between, which inverts §15.1 (the freeze is the student's Q-31 decision, not a side effect) and makes an anomalous first run self-ratifying — the exact failure the no-silent-update rule exists to prevent, moved one step earlier.

B) Two-state manifests: a measuring run emits a **candidate** manifest (`status: candidate`) whose identity fields are **cited from the D-numbers, never re-derived** (D-11's window and limitation, D-20's station, D-14's month and limitation), and whose measured fields (row counts, support/missingness, timestamp tolerances, runtime ranges, FP tolerances) each carry the **measuring run's registry id** as provenance — a measured field without a run id is unrepresentable. Freezing is a separate recorded human act under Q-31 that sets `status: frozen` and records the manifest's own hash in the evidence record; after freeze, every mismatch **raises** naming file and expectation, and re-measurement happens only through a new candidate and a new freeze act, the superseded manifest preserved rather than overwritten
   > **Impact**: §15.1's measure-then-freeze becomes two distinguishable states with the human act between them, and an invented value has nowhere to hide — it would be a measured field with no measuring-run provenance. Costs a status field, a provenance field per measured value, and the freeze act's recording.

C) B, plus the controls and the evidence bound: a run against a `candidate` manifest **cannot produce WS-20/TA-09/TA-17 evidence** — the evidence emitters refuse when the manifest is not frozen; a post-freeze edit without a new freeze act **fails the manifest self-hash check**; a manifest whose identity fields disagree with the cited D-number record **fails**; and D-11's measured completeness figures (ARUC 163/168, BSHM 168/168, NICO 155/168, 7/7 day presence) enter the manifest as **recorded eligibility evidence, not as expected assertion values** — the one-station plumbing fixture's own expected counts are measured from its BSHM-only run, per §15.1
   > **Impact**: The freeze becomes a gate the evidence chain actually passes through, silent drift is caught by the manifest's own hash, and the eligibility-versus-assertion distinction keeps D-11's three-cell record from being misread as a three-cell execution expectation. Costs three refusal paths and their fixtures.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. BLK-02's remaining limbs are exactly "the manifest must exist and be hash-verifiable, and the fixture must actually run" — the two-state workflow is the only shape in which both can happen without an agent inventing a value or a first run ratifying itself, and the evidence bound makes the freeze act load-bearing rather than ceremonial.

[Answer]: C

---

## Question 3

**The plumbing fixture: one-station execution against a three-cell eligibility record, and
the DATA-07 lineage caveat.** The D-11 clarification settled the reading: D-11's
`Stations:` line is **eligibility evidence** for the frozen window; TE §15.1's
**one-station execution scope is retained**; the station is frozen as **BSHM 32/35
(D-20)**, selected on the only complete coverage of the window. ARUC's one-bin shortfall
is **dormant, not discharged** — it attaches to a station that is not selected. The
fixture's inputs are pre-TC-06 derived artifacts under `evidence/audit_evidence_2022-11/`,
whose eligibility rests on derived-artifact verification (the four declared artifacts
against `sha256_manifest.json`) and whose provenance is, until the `raw_isprint_cache/`
re-acquisition, **unverifiable in principle** — the DATA-07 interim caveat binds every
artifact that relies on those coverage figures. Unstated: how the manifest encodes
identity versus eligibility, how one-station execution is enforced, and how the caveat
travels.

A) The manifest states window and station; input hashes cover the November artifacts; the caveat lives in the evidence documentation
   > **Impact**: Nothing distinguishes eligibility evidence from execution scope — the precise confusion Known-defects row 12 took two governance rounds to untangle — and a caveat that lives outside the artifact is exactly the kind that fails to appear "wherever FULL's coverage figures are relied on", which is the binding wording.

B) Identity by citation, scope by enforcement, caveat as freight: the manifest cites D-11 and D-20 by D-number (window 2022-11-01…07 inclusive; station BSHM 32/35; D-11's mandatory not-representative-of-December limitation and the provisional-Dst selection-only restriction carried verbatim in a limitations block, with ARUC's shortfall recorded **dormant, not discharged**); the input-hash area verifies the month's declared artifacts against its `sha256_manifest.json` — the same derived-artifact verification that made the month eligible; fixture assembly **enforces one-station scope** — a record from any station other than the frozen D-20 selection fails assembly; and the **DATA-07 caveat is a machine-readable manifest field** propagated onto the fixture run log and every artifact carrying the fixture's coverage figures, until the re-acquisition discharges it
   > **Impact**: Eligibility and execution stop sharing a sentence, the caveat becomes freight that cannot be forgotten at the artifacts the binding rule names, and the one-station scope is a raise rather than a reading. Costs one enforcement check and a propagated field.

C) B, plus the negative controls: a planted ARUC or NICO record in the assembled plumbing input **fails**; a manifest naming any station other than BSHM 32/35 **fails against the D-20 citation**; a coverage figure emitted from the fixture without the DATA-07 caveat field **fails**; and an input artifact whose hash disagrees with the month's `sha256_manifest.json` **fails before the fixture runs** — the eligibility check re-executed at use, not assumed from the selection record
   > **Impact**: Each limb of BLK-02's history gets its violation-is-caught pair, and the fixture cannot silently run on inputs the eligibility criterion never verified. Costs four fixture cases, all constructible from the existing November evidence plus synthetic plants.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. Row 12's whole history is the cost of leaving identity, eligibility and scope entangled in prose; B separates them structurally and C proves the separations hold. The caveat-as-field is the only design under which DATA-07's "must state it wherever relied on" is checkable rather than remembered.

[Answer]: C

---

## Question 4

**FR-WS-2 and FR-WS-3: the unit's two untested requirements as designed falsifiers.**
FR-WS-2: the seven-day fixture is **never** scientific evidence — no result artifact
cites it, plots it as a result, or interprets it as skill (TC-03f). FR-WS-3: no record
whose **observation date** falls in December 2022 enters either fixture — asserted on
record dates, never on the folder a file was filed under (the ML-07 lesson;
`tests/test_acquisition_window.py` exists and carries the predicate). Both are
`UNTESTED` — the story map marks them **NO CURRENT ACCEPTANCE ROW**. Unstated: the
mechanism for each, and whether the acceptance-row gap is routed or left.

A) Both are documented prohibitions, checked by review
   > **Impact**: The two requirements stay untested by choice, and FR-WS-2's failure mode — a smoke-test number quietly cited as evidence — is precisely the kind that looks harmless in review and fatal at a gate.

B) Label-based quarantine and record-date assertion: every artifact the plumbing fixture produces is stamped `evidence_class: smoke_only` by the producing path (the stamp travels with the artifact, R-110's emit-from-the-producing-path pattern), and every evidence-bearing surface — results artifacts, the TA-09 acceptance table, releases, the traceability matrix — **asserts the absence of `smoke_only` inputs**, so a plumbing-derived figure entering evidence fails structurally; fixture assembly asserts every input record's observation date against the window bounds and the December exclusion **on record timestamps** (consuming R-31's membership rule and `test_acquisition_window.py`'s predicate rather than duplicating either)
   > **Impact**: FR-WS-2 becomes a stamp plus an absence assertion instead of a memory, and FR-WS-3's mechanism reuses the two places the record-date rule already lives — no third copy. Costs one stamp field and two assertions.

C) B, plus the controls and the routing: a `smoke_only`-stamped artifact planted into a results artifact or the TA-09 table **fails**; a December-dated record planted inside a fixture input **is caught at assembly** — by record date, with the folder name deliberately mislabelled in the fixture to prove the predicate ignores it; and the two falsifiers are named at the gate as **candidate acceptance rows, proposed not applied** (a Vision §15.2 amendment is the owner's, and `requirements.md` § Known defects already models the shape), the machine-readable check results named as what each row's evidence column would point at
   > **Impact**: The unit's 2-of-8 untested figure is addressed through both legitimate channels at once — designed falsifiers now, acceptance rows by owner amendment — and the folder-mislabel control encodes the exact TEC-09 history that made record-date the rule. Costs two plant fixtures and a gate item.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. Both requirements exist because a specific failure already happened or nearly did (TEC-09's mislabelled directory; the smoke-test-as-evidence risk TC-03f names); the affirmed methodology requires the violation proven caught, and C is the only option that also moves the acceptance gap toward the authority that can close it.

[Answer]: C

---

## Question 5

**Fixture partition semantics under ADR-11, and the M10 execution slot.** A collision the
READY siblings leave at this unit's door: the plumbing fixture is representable —
`features-and-splits` R-74 lists a `score` spec covering seven days inside November as a
control that must **not** fire (containment in F4's validation month). But the scientific
fixture is **March 2022** (D-14), and March is inside **no** validation month (Apr, Jul,
Oct, Nov, Dec), while a `train`-role fit must equal the partition's training range
**exactly** — so under the frozen partition list (R-80: five partitions plus the locked
month), a March-only frame can lawfully neither fit nor score. R-122 supplies the
precedent for the way out: fixture parameters are **declared constants of the test
apparatus, explicitly not scientific values**, and the M10 contract fixture already uses
**synthetic partition dates** on the same authority. Separately, this unit **runs** the
M10 contract fixture in the clean-run sequence (Q12 = C) — authored in
`features-and-splits`' `test_train_only_transforms.py` and `test_split_embargo.py`, not a
third mandated fixture, gating no full-year job. Unstated: how stages 05–07 execute at
scientific-fixture scale, and where the M10 step sits.

A) The scientific fixture runs stages 00–04 only, stopping before features, so partitions never arise
   > **Impact**: The stages most acceptance rows need fixture evidence from — splits (WS-12), window parity (WS-13), masks (WS-16), bootstrap (WS-17) — would have no scientific-fixture path, and WS-20's "reproduces both fixtures" would silently mean less than §9.2 intends. The ordering gate would pass something weaker than what it guards.

B) Fixture-local partitions as test apparatus: the scientific manifest declares a fixture partition set over the March window — fixture ids **distinct from the six frozen partition ids**, declared apparatus constants under R-122's precedent exactly as M10's synthetic dates are — and stages 05–07 run against them at fixture scale; every fixture-partition artifact is stamped, and the quarantine holds: **no fixture artifact may carry a frozen confirmatory partition id**, so nothing fixture-scale can be mistaken for, or leak into, a confirmatory artifact. Because WS-12/WS-13 fixture evidence semantics turn on this reading, it is **routed to the gate as a proposal, not adopted silently**
   > **Impact**: The full pipeline is exercised at fixture scale without touching a frozen scientific value — the fixture partitions decide nothing D-numbers haven't — and ADR-11's identity enumeration stays intact because fixture ids never enter the six-id space. Costs the fixture-partition declaration and the gate item.

C) B, plus the M10 slot and the controls: the M10 contract fixture executes as its **own named step** of the clean-run sequence — after the plumbing fixture, invoking the two `features-and-splits`-authored modules, its placement recorded in §13.2 terms as a **proposal** (the sequence's text is authority; adding a step is not this stage's to apply) — with §9.2's boundary asserted: the M10 step **gates no full-year job** and the two-fixture ordering contract is unchanged by it; controls: a fixture artifact carrying any of the six frozen partition ids **fails**; a fixture partition id offered to the ADR-11 identity check **raises** like any mismatched pair (no seventh enumerated exception is minted); the M10 step absent from the executed sequence **fails `test_clean_run.py`** — running it here is what puts it inside TA-17's and WS-20's reach, which was the entire point of Q12 = C
   > **Impact**: The owner's Q12 = C split becomes executable — authorship there, execution here, verified — and the two boundaries that could quietly erode (fixture ids into confirmatory space; M10 into a third mandated fixture) each get a raise. Costs two controls and one sequence assertion.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. The March/partition collision is real and unresolved upstream — option A resolves it by evidence starvation, which the acceptance rows cannot afford. B's apparatus-constants reading is the only one with an in-project precedent on exactly this shape (M10, R-122), and routing it to the gate respects that WS-row evidence semantics are not this stage's to fix by assertion. C then closes the Q12 = C loop the ruling deliberately created.

[Answer]: C

---

## Question 6

**`test_clean_run.py`: the literal §13.2 sequence, the CPU assertion, and the comparison
ledger.** The amended §13.2 is the reproducibility test's actual definition:
`PYTHONHASHSEED=0` set **before the first command** (BLK-01's closure, tested as
amended), then `python scripts/run_walking_skeleton.py --config configs/ --fixture
plumbing_7day`, then `--fixture scientific_1month`, then the nine phase-aware stage
scripts — one `02` per phase, `--phase` selecting — all completing on CPU. NFR-REP-01
fixes the comparison discipline: §13.7's exact-equality classes (hashes, schemas,
partition membership, IDs, deterministic CPU transformations) compare **for equality, not
tolerance**, and a mismatch must not silently update the expected value; everything else
compares within the manifest's declared FP tolerances (never a test body's). TA-17 adds
declared **runtime and storage** tolerances. BLK-08 ↓ bounds the units of every
TECU-stated tolerance. Unstated: how the test executes the sequence, what asserts
CPU-only, which comparison each output gets and who declares it, and what data scope the
nine-script segment runs at.

A) `test_clean_run.py` shells the commands in order and asserts exit codes
   > **Impact**: "Succeeds" without "reproduces" — no artifact comparison, no tolerance discipline, no §13.7 classes — which fails WS-20's actual wording ("reproduces both fixtures within declared tolerances") while appearing green.

B) The test executes the amended sequence verbatim in a fresh environment with no GPU visible, and compares through a **manifest-declared comparison ledger**: every required output carries its comparison class in the manifest — `exact` for §13.7's five classes, `toleranced` with the manifest's FP tolerance otherwise — the class declared per output at manifest-freeze time (Question 2's workflow), a mismatch in an `exact`-class artifact raising with file and expectation and **never updating the expectation**; runtime and storage asserted inside the manifest's measured ranges (R-120's widening-guard cost landing in the runtime range it was measured into); the clean-run log and a machine-readable matched-artifact report emitted as WS-20/TA-17 evidence
   > **Impact**: The comparison discipline moves wholly into the manifest — no tolerance, class or expectation lives in a test body (TC-03e's shape applied to test apparatus) — and the D-18 traversal-order lesson (`DATA-17`) is honoured: byte-identity is asserted where §13.7 demands it, not approximated. Costs the per-output class declaration.

C) B, plus the controls and the honest scope routing: a planted single-bit change in an `exact`-class artifact **fails**; a tolerance sourced from a test body rather than the manifest **fails** an only-copy check; the sequence executed out of order **fails**; a run that completes only when a GPU is present **fails** — CPU is asserted as the complete path (TC-01), GPU never a dependency of any result; and the **nine-script segment's data scope is routed to the gate**: §13.2 orders the nine scripts after the fixtures but does not state what data they run over inside the clean-run contract, TA-17's runtime tolerance is only measurable at whatever scope is fixed, and §15.1 bars inventing it — so the candidates (fixture-scale via Question 5's apparatus partitions; a declared reduced window; full-year) are named for the owner rather than assumed
   > **Impact**: WS-20 and TA-17 get falsifiers matching their wording, and the one genuinely open reading in §13.2 is surfaced instead of silently resolved — a wrong assumption there would freeze a runtime tolerance measured at the wrong scale, unfixable after freeze without a new act. Costs four controls and a gate item.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. The clean run is this project's reproducibility definition and G-07's evidence; the ledger is the only design under which §13.7's exact classes and §15.2's tolerances coexist without a test body deciding anything, and the scope question is exactly the class of ordering ambiguity `project.md` requires raised rather than reinterpreted.

[Answer]: C

---

## Question 7

**The ordering contract as an executable gate: pass receipts, the full-year check's home,
and what raises.** TE §9.2's rule — both fixtures pass, in order, before any full-year
job — is hard and pipeline-enforced, and `services.md` states the posture:
`run_walking_skeleton.py` **enforces** the ordering. But enforcement inside the
orchestrator's own process reaches only runs the orchestrator starts: nothing yet stops a
direct full-year stage-script invocation. The stage entry contract (six steps) is
`foundation`'s approved surface — adding a step is a formal amendment this stage may not
make. And no fixture-specific exception exists among R-01's fourteen. Unstated: what
records "passed", where the full-year check lives, and what raises.

A) Ordering enforced only within `run_walking_skeleton.py`'s own process; a violation exits with a message; nothing checks a direct stage-script invocation
   > **Impact**: The hard rule holds exactly as long as everyone uses the orchestrator — a convention, not a gate — and the first direct full-year invocation after an environment rebuild violates §9.2 invisibly.

B) Receipts plus an exported check: on each fixture pass, `run_walking_skeleton.py` writes a machine-readable **fixture-pass receipt** — fixture id, the frozen manifest's hash, the result, the run's registry id — following the release pattern (`identified by release ID and verified by hash`, never by path convention); a single check function consumes both receipts, verifies each against the frozen manifest hashes, and asserts plumbing-before-scientific order; its **call site in full-year jobs is routed to the gate** — the candidates being a seventh stage-entry step (`foundation`'s surface, formal amendment) or an in-script assertion the nine scripts adopt by contract — proposed, not applied; ordering violations raise the base `IntegrityError` with file and violated expectation, **no fifteenth exception minted** (the alternative — a `FixtureError` subclass, which R-01's "any future integrity-related exception" admits and its negative control proves catchable — is named at the gate with its cost stated: the "fourteen" figure lives in `foundation`'s READY text and a sibling's assumptions, so minting obliges a cross-representation sweep)
   > **Impact**: "Passed" becomes an artifact with provenance instead of a process memory, the enforcement seam is put to the only authority that owns the entry contract, and the exception question is decided with its sweep cost visible rather than discovered. Costs the receipt schema and two gate items.

C) B, plus the negative controls: a scientific-fixture run without a plumbing receipt **raises**; a full-year invocation without both receipts **raises** (asserted through the check function on a synthetic tree); a receipt whose manifest hash disagrees with the frozen manifest **raises** — a re-frozen manifest invalidates old receipts by construction; a receipt written from a `candidate` manifest **is refused at write time** (Question 2's evidence bound applied to receipts); and the M10 step's result is recorded **in the clean-run evidence, not as a third receipt** — the two-receipt gate is §9.2's and is not extended
   > **Impact**: The gate's four bypass routes — skip plumbing, skip both, stale receipt, unfrozen manifest — each get a raise, and the receipt set stays exactly two, keeping §9.2 unextended the way the Q12 = C ruling requires. Costs four controls on synthetic receipt trees.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A hard sequencing rule enforced by convention is the register's definition of a blocker waiting to happen; receipts make the rule survivable across sessions and platforms (a Kaggle session has no memory of a local run), and the manifest-hash binding makes a re-freeze do the right thing automatically. Base-`IntegrityError` reuse is the default because it changes no READY text; the gate can still choose the subclass with its sweep cost on the table.

[Answer]: C

---

## Question 8

**The Kaggle in-session gate (FR-WS-6, REQ-NFR-A3): evidence that the gate ran where the
governed run ran.** TC-03g (`binding: hard`): the critical test set **and both fixtures**
run **inside the Kaggle session** before any governed run executed there, the result
captured in that run's evidence record — because a Kaggle session carries no git working
tree, no commit hook fires there, and a local suite run proves nothing about the
environment the governed run actually executes in. REQ-NFR-A3 names the gap NFR-REP-01
leaves: *a* clean environment is not *the* platform. `foundation`'s `ConfigSnapshot`
resolves `platform: "kaggle" | "local"` and the §13.1 environment lock captures eight
items per run. Unstated: how "ran in-session" becomes a checkable fact rather than an
operator's paste.

A) A documented procedure: the operator runs the suite and fixtures in the notebook and records the output
   > **Impact**: The evidence is whatever was pasted — indistinguishable from a local run's output — and TA-03/TA-26's evidence columns ("install logs from both platforms", "restore on both platforms") reduce to trust in transcription.

B) The in-session gate is a producing path: before any governed Kaggle run, the critical set and both fixtures execute in-session and emit a machine-readable **in-session gate result** stamped with the resolved platform (from `ConfigSnapshot.platform` — resolved by `foundation`'s detection, never asserted by the caller), the §13.1 environment-lock items in force (code commit, config snapshot hashes, pins), timestamps, and the per-test and per-fixture results; the governed run's registry evidence record references that artifact, and a governed run on Kaggle whose evidence record lacks an in-session gate result — or carries one stamped `local` — **fails before domain work** rather than proceeding silently
   > **Impact**: Platform parity becomes a stamp comparison the run itself performs, and the evidence TA-03/TA-26 need is emitted by the same act that satisfies the rule. Costs one artifact schema and one precondition check.

C) B, plus the controls and the staleness bound: a `local`-stamped result offered as in-session evidence **fails on the platform stamp**; a gate result whose code commit or config-snapshot hashes disagree with the governed run's own §13.1 lock **fails** — the gate proves the environment of *this* run, not of some earlier session; and a gate result predating the frozen manifests in force **fails** the same way a stale receipt does (Question 7's hash binding applied here)
   > **Impact**: The three ways the in-session rule can be satisfied in letter and violated in substance — wrong platform, wrong code, wrong manifests — each get a raise, which is what BENCH-01 was about. Costs three controls on synthetic evidence records.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. TC-03g exists because the one environment that matters most is the one with no git tree and no hook; only evidence emitted by the session itself, bound to the run's own environment lock, closes that. The staleness bound is cheap and converts "ran the gate once in August" from a loophole into a failure.

[Answer]: C

---

## Question 9

**TA-21's traceability matrix, the TA-09 acceptance table, and the
`environment_and_cpu_preflight_report`: producing paths, not documents.** Three evidence
artifacts land in this unit's `Owns`: the traceability matrix (TA-21: each implemented
requirement connected to a decision, a test/experiment, and an evidence artifact), the
fixture acceptance table (TA-09's evidence: per-row evidence links, **bounded to the
13-row FR-WS-4 set** — WS-01 plus WS-09…WS-20 — with WS-02–WS-08 deferred to G-P3A), and
the `environment_and_cpu_preflight_report` (G-07's named evidence alongside the clean-run
log and matched artifacts; TA-03's evidence). The acceptance vocabulary is explicit:
evidence is machine-readable or reviewable, and visual inspection alone is insufficient.
Unstated: what produces each, from what sources, and what refuses.

A) Three hand-maintained markdown documents, updated as work completes
   > **Impact**: Every count and link in them is carried rather than derived — the exact failure mode `project.md`'s count-derivation and representation-sweep corrections document five times over — and TA-21's "connects each implemented requirement" is unverifiable the day it is written.

B) Three producing paths: the traceability matrix is **generated** from machine-readable sources — requirement ids joined to their D-numbers, test modules and evidence artifact ids — with completeness asserted against the implemented-requirement list, a row missing any of its three links failing rather than rendering blank; the TA-09 acceptance table is emitted from the fixture-pass receipts and the per-row evidence artifacts, **bounded to the 13 rows by construction** with the WS-02–WS-08 deferral stated on the table itself; the `environment_and_cpu_preflight_report` is assembled from `foundation`'s §13.1 environment lock plus the clean-run results, its field set fixed so G-07's evidence column is a parse, not a screenshot
   > **Impact**: All three artifacts become derivations with refusal semantics, and the deferral that took a countersignature and a named exception to settle is enforced by the emitting path instead of remembered by it. Costs three emitters over sources that already exist by contract.

C) B, plus the controls and the honest limits: a matrix row citing a test module absent from the workspace **fails**; a WS row claimed `PASS` without an evidence link **fails**; a TA-09 table containing any WS-02…WS-08 row **fails** — the deferral is a raise, not a footnote; the report and matrix each carry the DATA-07 caveat field wherever a fixture coverage figure appears (Question 3's freight arriving at its last stop); and TA-27's entry in the matrix records **this unit as supporting evidence for the first limb only**, the transition-manifest hash-diff limb recorded as deferred to G-P2/G-P3C rather than claimed inside Phase 1
   > **Impact**: The unit's evidence surfaces cannot overstate — not a passed row without proof, not a deferred row as done, not a Phase 2 limb as Phase 1 — which is the entire value of a traceability artifact at a supervisor gate. Costs four controls, all on synthetic inputs.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. These artifacts are what G-07 and the TA rows actually read; a generated artifact that refuses is the only kind whose claims survive the board's own standard, and this project's correction history is one long argument against hand-carried links and counts.

[Answer]: C

---

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence: the siblings close at **R-132**
  (derived 2026-08-27 by grepping every sibling `business-rules.md` heading set:
  `regimes-diagnostics-reporting` R-123…R-132, ten headings, is the highest; verified
  against a full-corpus extraction whose maximum genuine rule id is R-132), so this unit
  opens at **R-133**. The inherited R-83…R-89 gap remains observed, not explained.
- **[assumption]** Depth Q1 = B: this unit has **no approved cross-package boundary
  signature of its own** in `component-methods.md` — `run_walking_skeleton.py` is a
  script row in `services.md` and the manifests are data — so the manifest schema and
  loader, the comparison ledger, the receipts, the in-session gate result and the three
  evidence emitters are intra-unit and test-apparatus shapes this stage specifies, names
  indicative, finalized in the three design artifacts after the gate.
- **[assumption]** **The scientific window is frozen as D-14 — March 2022, all three
  cells** (`CR-2026-08-21-FREEZES`; `unit-of-work.md` § 12 as corrected under `UG-08`;
  FR-WS-1's own text). Any earlier record stating the window "remains open under Q-31"
  is superseded on disk, and this design is written against the frozen value. The
  design remains window-parametric only in the trivial sense that identity is cited
  from the D-number, never hardcoded (TC-03e).
- **[assumption]** Exception placement: **no fifteenth exception is minted by
  default** — ordering, manifest and receipt violations raise the base `IntegrityError`
  with file and violated expectation, catchable by `foundation`'s stage-entry contract
  exactly as R-01's negative control proves. The `FixtureError` alternative is named at
  the gate (Question 7) with its cost stated: R-01's "fourteen" is a representation
  carried in `foundation`'s READY text and `regimes-diagnostics-reporting`'s
  assumptions, and minting obliges the cross-representation sweep `project.md`'s
  corrections mandate.
- **[assumption]** The fixture-manifest schema carries the cross-unit slots the READY
  siblings already rely on: `statistical-inference` R-120's measured widening-guard
  runtime and R-121's fixture-derived tolerances (§13.7 discipline), and R-122's
  general `tests/fixtures/<fixture_id>/fixture_manifest.yaml` convention — this unit
  owns the schema; whether any sibling's synthetic fixture warrants its own
  `tests/fixtures/` directory is that sibling's §12 question, not this one's.
- **[assumption]** TA-04's fixture obligations run on `inventory-and-registry`'s and
  `foundation`'s tooling (hash manifests, station registry) invoked over this unit's
  fixtures — this unit provides the fixture runs and logs; it re-implements no hashing
  (the single hashing home is `src/data/release.py`).
- **Verification obligations owned here:** the validated manifest schema, its thirteen
  §15.2 areas, the §15.4 cross-check and the single-loader discipline (Q1); the
  candidate/frozen workflow, identity-by-citation, measured-value provenance and the
  no-silent-update raise (Q2); the one-station enforcement, eligibility re-verification
  at use, and the DATA-07 caveat as machine-readable freight (Q3); the `smoke_only`
  quarantine and the record-date assembly assertion (Q4); the fixture-partition
  quarantine, the ADR-11 id-space separation, and the M10 sequence step (Q5); the
  literal amended §13.2 execution, the CPU-complete-path assertion, the comparison
  ledger and the matched-artifact evidence (Q6); the fixture-pass receipts, the
  two-receipt full-year gate and its bypass controls (Q7); the in-session gate result
  and its platform/staleness binding (Q8); the three generated evidence artifacts with
  refusal semantics (Q9).
- **Governance dependencies owned outside this unit:** the two manifest freeze acts —
  the measured values' promotion from candidate to frozen — are the **project owner's
  under Q-31** (TE §18.2 assigns fixture station, dates and tolerances to the Student),
  and nothing here performs them; BLK-03/BLK-04/BLK-08/BLK-09's contract approvals
  (their owning units' 3.1 gates) — until BLK-08's joint contract is adopted by both
  halves, no TECU-stated clean-run tolerance is checkable, and the comparison ledger
  inherits that bound; the loader's home and the full-year check's call site (Q1, Q7 —
  `foundation`'s surfaces, proposed not applied); the nine-script clean-run data scope
  (Q6 — owner ruling; the runtime tolerance freeze depends on it); the fixture-partition
  reading's effect on WS-12/WS-13 evidence semantics (Q5 — gate); the candidate
  acceptance rows for FR-WS-2/FR-WS-3 (Q4 — Vision §15.2, owner/supervisor); the
  `raw_isprint_cache/` re-acquisition that alone discharges the DATA-07 caveat (FU-1 = B,
  sequenced after requirements-analysis, owned outside this unit); **G-07
  Reproducibility** (Blocked, Supervisor) — the gate that actually accepts WS-20/TA-17's
  evidence, due before thesis submission; G-05/G-06 as the freeze events the receipts
  and evidence records reference.
- **Open — BLK-02 is not closed by this design.** The manifests' design is specified
  here; the manifests do not exist, the fixtures have never run, and **no measured value
  exists and none is claimed**. BLK-02 closes only when the authoritative manifests
  exist, are hash-verifiable, and the fixtures have actually run under the frozen
  identities — acts gated by G-09, stage 3.5, and the Q-31 freeze authority.
- **Open — the four inherited blockers are EXIT conditions on this stage.** BLK-03 ↓,
  BLK-04 ↓, BLK-08 ↓, BLK-09 ↓ remain open; nothing in this file closes any of them;
  this unit may not complete or exit 3.1 while any stands, and no implementation may
  proceed while they stand.
- **G-09 is not signed.** No answer here authorises creating
  `scripts/run_walking_skeleton.py`, either `fixture_manifest.yaml`,
  `tests/test_clean_run.py`, any receipt or evidence emitter, or a `tests/fixtures/`
  directory; TE §18.3's stop-and-report rule binds every affected component while any
  P0 decision is unresolved.
- **None** of the above decides a scientific value. The window, station, month, seeds,
  partitions and tolerances are frozen elsewhere (D-11, D-20, D-14, `seeds.yaml`, R-80)
  or measured under §15.1 and frozen by the Q-31 authority; everything underdetermined —
  the loader home (Q1), the clean-run scope (Q6), the check's call site and the
  exception choice (Q7), the fixture-partition reading (Q5), the acceptance-row
  proposals (Q4) — is expressly routed to the gate.

---

## Consolidated Summary Confirmation (superseded by the 2026-08-28 post-execution pass below)

Questions 1–9 are answered above: **Q1 = C, Q2 = C, Q3 = C, Q4 = C, Q5 = C, Q6 = C,
Q7 = C, Q8 = C, Q9 = C**. This is the pre-generation summary stop: before the three
design artifacts are generated, this section states the whole of what those answers
commit to, and nothing else is generated from them.

### What will be generated

Three artifacts, in this directory:

- **`business-logic-model.md`** — the workflows: the **manifest loader and validation
  path** — one schema enumerating the TE §15.2 content areas as required blocks
  (**thirteen per REQ-ENG-4 as posed; the artifacts bind to §15.2's derived twelve — see
  `business-logic-model.md` § Assumptions**)
  plus the §15.4 `artifact_manifest.json` cross-check and the named cross-unit slots
  (`statistical-inference` R-120's measured widening-guard runtime, R-121's per-check
  tolerances), one validating loader rejecting a manifest missing any area naming file
  and missing expectation, asserted the **only** read path, with per-area
  missing-block negative controls (Q1); the **measure-then-freeze workflow** — candidate
  versus frozen manifests, identity fields **cited from D-11/D-20/D-14 and never
  re-derived**, every measured field carrying its measuring run's registry id, the freeze
  a separate recorded human act under Q-31 setting `status: frozen` and recording the
  manifest's own hash, evidence emitters refusing a `candidate` manifest, a post-freeze
  edit failing the self-hash, D-11's completeness figures entering as **eligibility
  evidence, not expected assertion values** (Q2); the **plumbing-fixture lineage** —
  one-station scope (BSHM 32/35, D-20) enforced at assembly, eligibility re-verified at
  use against the month's `sha256_manifest.json`, D-11's limitation and the
  provisional-Dst restriction carried verbatim, ARUC's shortfall recorded dormant, and
  the **DATA-07 caveat as a machine-readable field** propagated onto the run log and
  every artifact relying on the fixture's coverage figures (Q3); the **smoke quarantine
  and December exclusion** — `evidence_class: smoke_only` stamped by the producing path
  with absence assertions on every evidence-bearing surface, and the record-date
  assembly assertion consuming R-31 and `test_acquisition_window.py`'s predicate with
  the folder-mislabel control encoding TEC-09 (Q4); the **fixture partitions and the M10
  step** — fixture-local partition ids as declared apparatus constants on R-122's
  precedent, distinct from the six frozen ids and quarantined from confirmatory
  artifacts, stages 05–07 running at fixture scale, and the M10 contract fixture
  executing as its own named clean-run step (authored by `features-and-splits`, run
  here, gating no full-year job), its absence failing `test_clean_run.py` (Q5); the
  **clean-run test** — the amended §13.2 sequence verbatim (`PYTHONHASHSEED=0` before
  the first command), fresh environment, no GPU visible, CPU asserted the complete path,
  and the **manifest-declared comparison ledger** — `exact` for §13.7's five classes
  (never silently updating an expectation), `toleranced` with manifest FP tolerances
  otherwise, runtime and storage inside measured ranges, single-bit-plant and
  out-of-order controls (Q6); the **ordering receipts** — machine-readable fixture-pass
  receipts bound to the frozen manifest hash on the release pattern, one exported check
  asserting plumbing-before-scientific and both-before-any-full-year-job, the four
  bypass routes each raising, candidate-manifest receipts refused at write time, the M10
  result recorded in clean-run evidence and never a third receipt (Q7); the **Kaggle
  in-session gate** — a producing path emitting a platform-stamped gate result bound to
  the governed run's own §13.1 environment lock, a Kaggle governed run without it (or
  with a `local` stamp, mismatched hashes, or a pre-freeze timestamp) failing before
  domain work (Q8); and the **generated reports** — the traceability matrix, the TA-09
  acceptance table bounded to the 13-row set by construction, and the
  `environment_and_cpu_preflight_report`, all derivations with refusal semantics, the
  DATA-07 caveat arriving at its last stop and TA-27 recorded as first-limb supporting
  evidence only (Q9).
- **`business-rules.md`** — rules opening at **R-133**, continuing the single sequence:
  re-verified 2026-08-27 by grepping every sibling `business-rules.md` heading set — the
  maximum genuine rule id is **R-132** (`regimes-diagnostics-reporting` R-123…R-132);
  the R-83…R-89 gap is inherited as observed, not explained.
- **`domain-entities.md`** — the intra-unit and test-apparatus shapes Depth Q1 = B
  assigns to this stage: the **two-state fixture manifest** (**thirteen §15.2 areas per
  REQ-ENG-4 as posed; the artifacts bind to §15.2's derived twelve — see
  `business-logic-model.md` § Assumptions**, the
  §15.4 cross-reference, the cross-unit tolerance slots, the per-output comparison-class
  ledger, `status: candidate | frozen`, identity by D-number citation, per-measured-field
  run provenance, the eligibility-evidence block, the DATA-07 caveat field, the
  fixture-partition declaration, the `smoke_only` stamp); the **fixture-pass receipt**
  (fixture id, frozen-manifest hash, result, registry id); the **in-session gate result**
  (platform stamp from `ConfigSnapshot.platform`, §13.1 lock items, timestamps, per-test
  and per-fixture results); the **three report artifacts** (matrix rows with three
  mandatory links, the bounded acceptance table with the WS-02–WS-08 deferral stated on
  it, the preflight report's fixed field set); and **exception placement** — no
  fifteenth exception minted by default: ordering, manifest and receipt violations raise
  the base `IntegrityError` naming file and violated expectation, the `FixtureError`
  alternative a named gate item.

The test scope here is **`tests/test_clean_run.py`** plus the two fixture trees
`tests/fixtures/plumbing_7day/` and `tests/fixtures/scientific_1month/` with their
`fixture_manifest.yaml`s per TE §15.2 — **specified, not created**: G-09 is not signed,
no `tests/fixtures/` directory exists, and neither fixture has ever run.

### Each answer, one line

| Q | Answer | Design consequence |
|---|---|---|
| 1 | C | One validated manifest schema (§15.2 areas + §15.4 cross-check + R-120/R-121 slots — **thirteen per REQ-ENG-4 as posed; the artifacts bind to §15.2's derived twelve, see `business-logic-model.md` § Assumptions**; board-arbitrated 2026-08-28 on `GOV-2026-08-28-FD-01` Rec 30 in this unit's favour), one validating loader asserted the only read path, per-area negative controls; the loader's **home** routed to the gate with both candidates named |
| 2 | C | Candidate/frozen two-state manifests with the Q-31 human act between; identity cited from D-numbers, measured fields carrying run provenance; evidence emitters refuse `candidate`; post-freeze edits fail the self-hash; D-11 figures are eligibility evidence, never execution expectations |
| 3 | C | One-station (BSHM 32/35, D-20) enforced at assembly; eligibility re-verified at use; D-11's limitation and provisional-Dst restriction carried verbatim; the DATA-07 caveat a machine-readable field that travels; planted ARUC/NICO records and hash disagreements fail |
| 4 | C | FR-WS-2 becomes the `smoke_only` stamp plus absence assertions on every evidence surface; FR-WS-3 consumes R-31 and `test_acquisition_window.py`'s predicate (no third copy), the folder-mislabel control proving record-date wins; candidate acceptance rows **proposed, not applied** |
| 5 | C | Fixture-local partition ids as R-122 apparatus constants, quarantined from the six frozen ids; stages 05–07 run at fixture scale; the M10 step named in the clean-run sequence (placement proposed in §13.2 terms), gating no full-year job; its absence fails `test_clean_run.py` |
| 6 | C | `test_clean_run.py` executes the amended §13.2 verbatim, no GPU visible, CPU the complete path; the manifest-declared comparison ledger (`exact` for §13.7's classes, `toleranced` otherwise) with no tolerance in a test body; the nine-script data scope routed to the gate |
| 7 | C | Fixture-pass receipts bound to frozen-manifest hashes; one exported check enforces the §9.2 order across sessions and platforms; four bypass controls; base `IntegrityError`, no fifteenth exception by default, `FixtureError` named at the gate with its sweep cost; call site routed |
| 8 | C | The in-session gate is a producing path: platform-stamped result bound to the run's own §13.1 lock; a Kaggle governed run missing it, stamped `local`, hash-mismatched, or pre-freeze **fails before domain work** — BENCH-01's three substance violations each raise |
| 9 | C | Matrix, TA-09 table and preflight report generated with refusal semantics: no `PASS` without evidence, no WS-02…WS-08 row ever, the deferral a raise not a footnote; the DATA-07 caveat reaches both; TA-27 recorded first-limb-supporting only, the hash-diff limb deferred to G-P2/G-P3C |

### Gate items

Routed, not decided:

- **The manifest loader's home (Q1)** — a function set in `foundation`'s `src/data/` by
  cross-unit contract (mirroring how the eight non-foundation exceptions import the
  base), or a test-apparatus helper under `tests/fixtures/`; §12 names no module for it
  and this stage may not amend §12 by assertion. The amendment consequence of each
  candidate is derived in § The figures below.
- **The exception choice (Q7)** — base `IntegrityError` reuse is the default (it changes
  no READY text); `FixtureError` as a fifteenth `IntegrityError` subclass is named with
  its cost stated: R-01's "fourteen" is a representation carried in `foundation`'s READY
  text and `regimes-diagnostics-reporting`'s assumptions, so minting obliges the
  cross-representation sweep `project.md`'s corrections mandate.
- **The full-year check's call site (Q7)** — a seventh stage-entry step (`foundation`'s
  approved six-step surface, a formal amendment this stage may not make) or an in-script
  assertion the nine scripts adopt by contract; proposed, not applied.
- **The nine-script clean-run data scope (Q6)** — §13.2 orders the nine scripts after
  the fixtures but does not state what data they run over inside the clean-run contract;
  the candidates (fixture-scale via Q5's apparatus partitions; a declared reduced
  window; full-year) are named for the owner. TA-17's runtime tolerance is only
  measurable at whatever scope is fixed, and §15.1 bars inventing it.
- **The fixture-partition reading and the M10 placement (Q5)** — fixture-local ids as
  apparatus constants and their effect on WS-12/WS-13 fixture-evidence semantics; the
  M10 step's position recorded in §13.2 terms — both proposals, since the sequence's
  text and the WS rows' semantics are not this stage's to fix by assertion.
- **Candidate acceptance rows for FR-WS-2 and FR-WS-3 (Q4)** — Vision §15.2 amendments
  owned by the owner/supervisor, each naming the machine-readable check result its
  evidence column would point at; **proposed, never applied here**. Both stay covered by
  the designed falsifiers meanwhile.

### The blockers and standing authority

- **BLK-02 (owned) — open on implementation only.** The reading limb was settled by the
  D-11 clarification of 2026-08-22 (the `Stations:` line is eligibility evidence; TE
  §15.1's one-station execution scope retained) and the station limb froze as **BSHM
  32/35 (D-20)**; what remains open is exactly what no design can close: the manifests
  do not exist, neither fixture has ever run, and **no measured value is invented,
  inferred or substituted** (§15.1). Q2's candidate/frozen workflow is the designed path
  to closing it — the closing acts are gated by G-09, stage 3.5, and the Q-31 freeze
  authority.
- **BLK-03 ↓, BLK-04 ↓, BLK-08 ↓, BLK-09 ↓ (all inherited)** — exit conditions on stage
  3.1, **not closed by anything in this file**; this unit may enter, may not complete or
  exit 3.1 while any stands, and no implementation may proceed. **BLK-08 ↓ bounds the
  units of every TECU-stated clean-run tolerance**: until its joint contract (R-103) is
  adopted by both halves, no TECU-stated tolerance is checkable, and Q6's comparison
  ledger inherits that bound as checked, not silent.
- **G-09 is not signed.** Workspace inspection 2026-08-27: `tests/` holds three modules,
  none this unit's; no `tests/fixtures/` directory; `src/`, `configs/` and
  `pyproject.toml` absent. The artifacts specify design only; no answer authorises
  creating `scripts/run_walking_skeleton.py`, either `fixture_manifest.yaml`,
  `tests/test_clean_run.py`, any receipt or evidence emitter, or a `tests/fixtures/`
  directory. TE §18.3's stop-and-report rule binds while any P0 decision is unresolved.
- **The frozen identities are cited, never re-derived**: D-11 (window 2022-11-01…07
  inclusive, with its mandatory not-representative-of-December limitation and the
  provisional-Dst selection-only restriction), D-20 (station BSHM 32/35), D-14 (the
  scientific window — March 2022, all three cells, carrying its own equinox-month
  limitation).
- **No measured value is invented**: every exact count, tolerance and runtime is
  measured from the fixtures at fixture time and frozen under TE §15.1 by the Q-31
  authority; nothing in the three artifacts states a measured number.
- **G-07 Reproducibility (Blocked, Supervisor)** is the gate that actually accepts
  WS-20/TA-17's evidence, due before thesis submission; G-05 and G-06 are the freeze
  events the receipts and evidence records reference.

### The figures, derived not carried

- **8 requirements, 2 untested** — derived by filtering the story map's Table 1 on this
  unit (eight rows: FR-WS-1, FR-WS-2, FR-WS-3, FR-WS-4, FR-WS-5, FR-WS-6, NFR-REP-01,
  REQ-NFR-A3), with the per-unit coverage summary row agreeing (8 / 2 / four primary /
  five supporting) and the untested list agreeing by ID: **FR-WS-2, FR-WS-3**.
- **Acceptance rows — 4 primary + 5 supporting**: **WS-20, TA-09, TA-17, TA-21** primary
  — TA-09 **bounded to 13 rows** (WS-01 plus WS-09…WS-20, per FR-WS-4 and
  `requirements.md` § Known defects row 8); **TA-03, TA-04, TA-23, TA-26, TA-27**
  supporting — TA-27's first limb only inside Phase 1, the hash-diff limb accepted at
  G-P2/G-P3C.
- **Rules open at R-133** — grep-derived 2026-08-27: the maximum sibling
  `business-rules.md` heading id is **R-132**.
- **Amendments owed — derived against the current chain, printed before asserted:
  5 + 0 + 1 + 1 + 0 + 0 = 7 across 5 units.** The basis: `external-products` R-55's
  **5 across 3** + `features-and-splits` **0** + `evaluation-and-comparison` **1** (the
  BLK-08 package, R-103) + `statistical-inference` **1** (the R-118 signature amendment)
  + `regimes-diagnostics-reporting` **0** — re-verified 2026-08-27 by reading its
  `business-rules.md` § Amendments owed, which prints exactly that
  5 + 0 + 1 + 1 + 0 = 7-across-5 derivation — **plus this unit's 0 today**. This unit
  changes no approved boundary signature: `run_walking_skeleton.py` is a script row in
  `services.md`, the manifests are data, and every shape here (loader, ledger, receipts,
  gate result, emitters) is intra-unit or test apparatus under Depth Q1 = B. **One
  honest conditional**: if the gate places the manifest loader in `foundation`'s
  `src/data/` as a cross-unit contract (Q1's first candidate), that placement mints a
  new `component-methods.md` boundary surface and the ledger takes **+1, to 8 across 6,
  at that ruling** — counted then, not now, because the alternative home (a
  test-apparatus helper under `tests/fixtures/`) adds none. Q7's
  seventh-stage-entry-step candidate would amend `services.md`'s approved stage entry
  contract — a formal amendment, but not a `component-methods.md` boundary contract,
  the only class this ledger tracks; noted, not counted. The total therefore **stands
  at 7 across 5 units** today.

### What is NOT decided here

- **No scientific value.** The window, station, month, seeds, partitions and tolerances
  are frozen elsewhere (D-11, D-20, D-14, `seeds.yaml`, R-80) or measured under §15.1
  and frozen by the Q-31 authority; the loader home (Q1), the acceptance-row proposals
  (Q4), the fixture-partition reading and M10 placement (Q5), the nine-script scope
  (Q6), and the call site and exception choice (Q7) are proposed and routed to the gate.
- **No module creation.** G-09 is not signed; the artifacts specify design only.
- **No blocker closes.** BLK-02's remaining limbs and all four inherited exit conditions
  stand exactly as the register rules them; the two manifest freeze acts are not
  performed here.

### Assumptions and open questions, summarized

- **Assumptions carried into the artifacts**: rule numbering opens at R-133 with the
  R-83…R-89 gap inherited as observed; this unit has **no approved cross-package
  boundary signature of its own** (Depth Q1 = B) — every shape is intra-unit or test
  apparatus, names indicative, finalized in the three artifacts after the gate; no
  fifteenth exception is minted by default, violations raising the base `IntegrityError`
  exactly as R-01's negative control proves catchable; the manifest schema carries the
  cross-unit slots the READY siblings already rely on (R-120's measured runtime, R-121's
  tolerances, R-122's general convention); TA-04's fixture obligations run on
  `inventory-and-registry`'s and `foundation`'s tooling — this unit re-implements no
  hashing (the single home is `src/data/release.py`). **One supersession note stands
  recorded**: any record stating the scientific window "remains open under Q-31" — the
  dispatch brief's phrasing included — is stale on disk; **D-14 froze March 2022, all
  three cells** (`CR-2026-08-21-FREEZES`, corrected under `UG-08`) and **D-20 froze BSHM
  32/35**, and this design is written against the frozen values, identity cited by
  D-number and never hardcoded (TC-03e).
- **Verification obligations owned here**: the validated schema, §15.4 cross-check and
  single-loader discipline (Q1); the candidate/frozen workflow, citation-identity,
  measured-value provenance and no-silent-update raise (Q2); one-station enforcement,
  eligibility re-verification at use, the DATA-07 caveat as freight (Q3); the
  `smoke_only` quarantine and record-date assembly assertion (Q4); the fixture-partition
  quarantine, id-space separation and M10 step (Q5); the literal amended §13.2
  execution, CPU-complete-path assertion, comparison ledger and matched-artifact
  evidence (Q6); the receipts, the two-receipt full-year gate and its bypass controls
  (Q7); the in-session gate result with platform and staleness binding (Q8); the three
  generated evidence artifacts with refusal semantics (Q9).
- **Governance dependencies owned outside**: the two manifest freeze acts (the project
  owner's under Q-31; TE §18.2 assigns fixture station, dates and tolerances to the
  Student); BLK-03/BLK-04/BLK-08/BLK-09's contract approvals at their owning units'
  gates; the loader's home and the full-year check's call site (`foundation`'s surfaces,
  proposed not applied); the nine-script clean-run data scope (owner ruling; the runtime
  tolerance freeze depends on it); the fixture-partition reading's effect on
  WS-12/WS-13 evidence semantics (gate); the FR-WS-2/FR-WS-3 candidate rows (Vision
  §15.2, owner/supervisor); the `raw_isprint_cache/` re-acquisition that alone
  discharges the DATA-07 caveat (FU-1 = B, owned outside this unit); **G-07
  Reproducibility** (Blocked, Supervisor); G-05/G-06 as the freeze events referenced.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The receipt is recorded, the three design artifacts are generated on these answers, and the adversarial review follows.

- Request changes
   > **Impact**: Nothing is recorded or generated; state what to change and the summary is re-presented.

> **💡 Recommendation**: **Looks correct** — every figure above is derived from this
file's own sources rather than carried (the R-133 opening, the 8/2 requirement split,
the 4+5 acceptance rows and the 7-across-5 amendment total were all re-derived today,
and this unit adds zero to the amendment ledger now, with the loader-home conditional
stated honestly), every frozen identity is cited from its D-number rather than
re-derived, no measured value is invented, everything underdetermined is routed to the
gate as a proposal, and BLK-02's remaining limbs plus all four inherited exit conditions
stay open exactly as the register rules them.

[Answer]: Looks correct

---

## Consolidated Summary Confirmation

**What changed in this unit since the last receipt.** **D-29** supersession applied at four sites — `write_release` is now implementable and the 3.5 release-path block **lifts**; **G-09 signed (D-31)**. ⚠ **TA-15 is NOT discharged by this** and the artifacts say so.

**Governance recorded this pass.** **D-29** (`dataset_version` = first 12 hex of
`content_hash`, verify-on-write), **D-30** (`.dst_summary.json` relocation, performed and
hash-verified), **D-31** (**G-09 signed**, with its §18.3 preconditions recorded as
**unmet**), **D-32** (**all eight Vision §15.2 acceptance rows approved**, board option 1,
none deferred). Change records: `CHANGE_RECORD_2026-08-28_G09_signed.md`,
`CHANGE_RECORD_2026-08-28_dst_summary_relocation.md`.

**Execution evidence, and its exact limits.** Python **3.11.16** — the governed pin (TE §8.1, TC-03d) — obtained via `uv` and used to run the suites: **277 passed, 0 failed, 0 errors, 2 skipped** (both skips justified and recorded). Evidence packaged at `artifacts/exec_evidence/` with a SHA-256 manifest. **The runner was not pytest**: PyPI is unreachable in this environment, so a harness providing the pytest API surface was used; it has no plugins, no conftest and no assertion rewriting, and it **errors** rather than passes on an unsupported fixture. Two defects were found *by execution*: the access log could not evidence its own ordering (fixed — the guard now stamps `logged_at_utc` itself; 37 rows, 37 distinct monotonic instants), and the one-door assertion **failed against a file this session had just written**, which is the behaviour R-28 specifies.

⚠ **What is still NOT discharged, and this receipt does not claim otherwise:** TA-15, WS-18 and TA-18 have passing tests against **current** code, but their acceptance rows are discharged only at their own gates; `aws_ai_dlc_preflight_report` does not exist; `configs/` and the §18.3 zero-TBD preflight are unbuilt; and **D-31 records G-09's own preconditions as unmet**. Stage 3.1 remains **FAIL** and no board has passed it.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: Receipt recorded, this unit's artifacts re-saved, and a fresh adversarial review dispatched against the post-execution state.

- Request changes
   > **Impact**: Nothing recorded for this unit; name what to change and it is corrected before any receipt is taken.

- Other (please specify)
   > **Impact**: Depends on what you specify.

> **💡 Recommendation**: **Looks correct** — every claim above is either a recorded decision, a hash-verified act, or a test result from a run whose runner limitations are stated; nothing here asserts a gate is discharged.

[Answer]:
