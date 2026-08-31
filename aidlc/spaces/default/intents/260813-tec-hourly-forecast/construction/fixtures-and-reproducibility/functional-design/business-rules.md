# Business Rules — `fixtures-and-reproducibility`

> ## ✳ G-09 IS SIGNED — 2026-08-28, **D-31** (read this before any G-09 statement below)
>
> The project decision owner **signed and approved G-09 (Agent preflight)** on 2026-08-28,
> recorded as **D-31** in `evidence/DECISIONS.md` with change record
> `governance/CHANGE_RECORD_2026-08-28_G09_signed.md`. **Every statement below of the form
> "G-09 is not signed" / "G-09 stays unsigned" is superseded as to the gate's status**, and
> is left standing as the accurate record of the constraint that applied when it was
> written.
>
> ⚠ **D-31 records the gate's own TE §18.3 preconditions as UNMET, and that disclosure
> travels with the signature.** `configs/`, and until 2026-08-28 `src/`, did not exist, so
> the mandated automated zero-TBD preflight **could not run**; the ten named critical tests
> **cannot be executed in this environment** (no Python interpreter is installed — a
> zero-byte Windows Store stub, no registry entry, no interpreter on disk); and the evidence
> artifact `aws_ai_dlc_preflight_report` **does not exist**. "No failing critical test" is
> therefore **unproven, not proven** — an absence of executions, not an absence of failures.
> This is the owner **opening the gate by authority**, not a record that its evidentiary
> conditions were satisfied, and no reader may infer the second from the first.
>
> **What the signature changes here:** the **G-09 ground** for the creation bar is lifted — G-09 is no longer among the grounds. **Creation remains barred on the blocker ground**: BLK-03/BLK-04/BLK-08/BLK-09 are exit conditions untouched by D-31, so nothing here authorises creating a module, manifest, receipt, evidence emitter or `tests/fixtures/` directory.
> What the signature **does** make correctable is any defect this unit deferred *solely* because G-09 barred **editing an existing file**. (Swept 2026-08-30 to all three lead boxes, on the terminal-pass Critical finding that the body sweep had not reached this box.)
> **What it does NOT change:** G-05 and G-06 remain `Blocked`; G-P1A, G-P2, G-P3A, G-P3C
> and G-07 are unaffected; **TE §18.2's absolute rule stands** — every scientific value this
> unit routed to G-04/G-05 **stays routed**, and no agent may fill a freeze-gate value by
> convenience; and **§18.3's stop-and-report obligation survives its own gate**, being a
> standing rule on implementation rather than a one-time gate condition.

**Unit** `fixtures-and-reproducibility` · **Kind** `library` · **Complexity** M ·
**Deployment** standalone · **Depends on** `acquisition`, `inventory-and-registry`,
`target-standardization`, `external-products`, `features-and-splits`,
`models-and-baselines`, `evaluation-and-comparison`, `statistical-inference`,
`regimes-diagnostics-reporting`

The prohibitions this unit enforces, each with what it rejects, what it raises or fails,
and the negative control that proves the rejection happens.

**This project's affirmed methodology is a negative control paired with every hard rule** —
a test that proves the violation is *caught*, not only that the happy path works.

**Every rule here guards the step from "the pipeline ran" to "the pipeline reproduces".** A
violation of any of them does not crash anything: it produces a green fixture run whose
expectations were invented rather than measured, a smoke-test number cited as skill, a
full-year job that skipped the gate that was supposed to precede it, a clean run that
compared nothing, or a traceability matrix whose links point at modules that do not exist.
Each of those is invisible in the artifact and fatal at G-07, which is why each is made
structural or loud here.

**Rule IDs continue the single sequence.** `foundation` R-01…R-17, `governance-guards`
R-18…R-29, `acquisition` R-30…R-43, `inventory-and-registry` R-44…R-53, `external-products`
R-54…R-63 (plus R-54a), `target-standardization` R-64…R-73, `features-and-splits`
R-74…R-82 (plus R-76a), `models-and-baselines` R-90…R-102, `evaluation-and-comparison`
R-103…R-112, `statistical-inference` R-113…R-122, `regimes-diagnostics-reporting`
R-123…R-132 — so this unit opens at **R-133**. **Re-derived 2026-08-28** by extracting
every `^## R-` heading from all eleven sibling `business-rules.md` files and taking the
numeric maximum: **128 distinct rule headings, maximum genuine id R-132**. The
**R-83…R-89 gap** between `features-and-splits` and `models-and-baselines` is inherited as
observed, not explained: if it was a reservation, or per-unit numbering was intended, say
so at the gate and these artifacts renumber.

> **Remediation of `GOV-2026-08-28-FD-01` (verdict FAIL), applied 2026-08-28.** Seven items
> from the project decision owner's ruling, each carrying a dated note at its site:
> **Rec 5** (BLOCKER) — R-138 now executes §13.2's **seven Phase 1 stage-script
> invocations** and defers the Phase 2 segment to **G-P2**, with new control **(39)**;
> **Rec 24** — R-133 limb **5** declares §15.3's mandatory reduced-replicate fixture
> bootstrap as a test-apparatus constant with its scored range and block counts, control
> **(37)**; **Rec 36** — **D-14's second clause** is enumerated at every site and given the
> machine-readable `december_representativeness` field on **both** fixtures (R-135 limb 4),
> control **(38)**; **Rec 30** — the four post-answer `thirteen` sites in
> `functional-design-questions.md` are marked; **Rec 9** — the
> `environment_and_cpu_preflight_report` (**G-07**, this unit) is distinguished from
> `aws_ai_dlc_preflight_report` (**G-09**, **`foundation`'s**, discharged by **FR-WS-7**),
> supporting-row figure re-derived as **5**; **Rec 42** — `dataset_version`'s **unruled**
> encoding recorded as blocking the release path, with the `test_release_hashes.py` naming
> hazard stated (**no encoding invented**); **Rec 47** — the in-session gate records **its own
> measured total runtime** (R-141). **Ratified as D-28**: the G-06 locked-test scored set is
> **2–31 December 2022 (30 days)**, approved by the project owner 2026-08-28 under the
> recorded authority equivalence, with the Vision §8.2 / TE §7.1 embargo-column conflict
> **recorded, not resolved**, carried to G-05, and **no supervisor signature claimed**.
> Negative controls move **36 → 39**, must-not-fire **10 → 11**, rules stay **10**, amendments
> owed stay **7 across 5**. **No measured value is stated, inferred or substituted** (§15.1).

**One owned blocker and four inherited exit conditions stand on this stage.** **BLK-02**
(owned) is **open on implementation only**: its reading limb was settled by the D-11
clarification of 2026-08-22 and its station limb froze the same day as **BSHM 32/35
(D-20)**, but the manifests do not exist, neither fixture has ever run, and **no measured
value is invented, inferred or substituted** (TE §15.1). **BLK-03 ↓, BLK-04 ↓, BLK-08 ↓,
BLK-09 ↓** are inherited from five upstream units; the clean-run comparison and TA-21's
matrix consume their released artifacts, so what those contracts permit bounds what WS-20
and TA-17 can be said to have reproduced. **BLK-08 ↓ bounds the units of every tolerance
this unit compares** — a clean-run tolerance stated in TECU cannot be checked against
output no design path returns to TECU — and R-139 makes that dependence a **checked
refusal** rather than a silent inheritance. All five are **exit conditions on stage 3.1,
not entry conditions** (`GOV-2026-08-22-REM-01` Rec 2, extended 2026-08-23): this unit
may enter, **may not complete or exit** 3.1 while any stands, and **no implementation may
proceed**. **G-09 is not signed** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated **G-09 ground** no longer holds. **Creation remains barred — on the blocker ground**, the blockers being exit conditions untouched by D-31; G-09 is simply no longer among the grounds, and nothing here authorises a creation the blockers still bar. (Swept 2026-08-30 to every occurrence in these three artifacts, on the terminal-pass Critical finding that the 2026-08-30 line-97 repair reached one occurrence of four.) **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.
>
> ⚠ **Sentence repaired 2026-08-30 on adversarial finding 1, Major.** The G-09 annotation was
> spliced into the middle of this sentence and its **original tail was left standing**, so the
> sentence asserted "module creation is authorised" in one clause and *"no module, manifest,
> receipt, emitter or fixture directory named here **may be created**"* in the next — opposite
> conclusions in one sentence. The parallel sentence in `domain-entities.md` was reworked
> coherently and the one in `business-logic-model.md` was deliberately left unannotated per this
> file set's stated convention; this file alone did neither. **What now governs, stated once:**
> **G-09 no longer bars creating anything** — that ground is lifted. **What still bars it is the
> blockers**, which are exit rather than entry conditions and are **untouched by D-31**: this
> unit may enter 3.1 and **may not complete or exit it** while any blocker stands, and **no
> implementation may proceed** on that ground. **Superseded tail preserved:** ~~": no module,
> manifest, receipt, emitter or fixture directory named here may be created."~~ — superseded only
> as to its G-09 ground; the blocker ground stated above continues to bar the same creations.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 12 — the `Owns` list (five bullets: `scripts/run_walking_skeleton.py`; the two `fixture_manifest.yaml`s; `tests/test_clean_run.py`; the traceability matrix and the `environment_and_cpu_preflight_report`; **execution** of the M10 contract fixture), the responsibility, the boundary (invokes every stage script, implements no domain logic; seven script-owning edges and two artifact-only edges), the 8 requirements (2 bolded untested), acceptance rows WS-20/TA-09/TA-17/TA-21, the M10 execution ruling (**Q12 = C** — authored by `features-and-splits`, run here, **not a third mandated fixture**, §9.2 unchanged and unextended, no full-year job gating on it), the implementation notes (D-11's window and measured completeness; **D-14 — March 2022, all three cells**, no longer open under Q-31, corrected 2026-08-22 under `UG-08`; the Kaggle in-session rule; NFR-PHASE-01's hash-diff row carried here with `governance-guards` supporting); § Blocker register **BLK-02** with its six-row limb table (reading **Resolved**; station **RESOLVED — BSHM 32/35, D-20**; ARUC's one-bin shortfall **DORMANT, explicitly NOT resolved**; manifest **PENDING**; execution **PENDING**; measured evidence **PENDING — no value exists and none is claimed**) and the ARUC dormancy rule; **BLK-01 CLOSED 2026-08-22** (`CR-2026-08-22-TE-AMEND` put the `PYTHONHASHSEED=0` clause into TE §13.2, so this unit tests the **amended** sequence).
- `../../../inception/units-generation/unit-of-work-story-map.md` — Table 1's eight rows for this unit (FR-WS-2 and FR-WS-3 marked **NO CURRENT ACCEPTANCE ROW**); Table 2's WS-20, TA-09 (**bounded** to WS-01 and WS-09…WS-20), TA-17 and TA-21 rows with their evidence columns; the supporting rows TA-03, TA-04, TA-23, TA-26, TA-27 (**5**, re-derived 2026-08-28 from the per-unit coverage row; TA-27 first limb only inside Phase 1; **TA-23 supporting-only — `foundation` primary, evidence artifact `aws_ai_dlc_preflight_report`, discharging requirement FR-WS-7 at line 127, none of the three this unit's; see R-142's box**); § Per-unit coverage summary (`8 / 2 / WS-20, TA-09, TA-17, TA-21 / TA-03, TA-04, TA-23, TA-26, TA-27`); **line 206**'s TA-23 row (primary `foundation`, supporting `fixtures-and-reproducibility`, evidence `aws_ai_dlc_preflight_report`) and **line 127**'s `| FR-WS-7 | foundation | TA-23 |`; § Cross-unit responsibilities (NFR-PHASE-01/TA-27; REQ-ENG-5's spread across four units); **REQ-ENG-4 is `foundation`'s requirement whose acceptance row is TA-09 — this unit's primary row**, so the manifest schema designed here is the mechanism by which another unit's requirement discharges.
- `../../../inception/requirements-analysis/requirements.md` — FR-WS-1 (both fixtures in order before any full-year job; D-11 and **D-14** named in the requirement text), FR-WS-2 (`UNTESTED`), FR-WS-3 (`UNTESTED`; record dates never folder names; `tests/test_acquisition_window.py` named), FR-WS-4 (the 13-row Phase 1 set, WS-01 approved as a named exception 2026-08-21), FR-WS-5 (clean CPU reproduction within declared tolerances, the §13.2 sequence), FR-WS-6 (critical set **and both fixtures** inside the Kaggle session), NFR-REP-01 (**§13.7's exact-equality classes hold exactly**, and a mismatch **must not silently update the expected value** — the D-18 traversal-order lesson, `DATA-17`), REQ-NFR-A3 (platform parity: NFR-REP-01 governs *a* clean environment, not *the* one the governed run runs in), **REQ-ENG-4** (fixture assertion data in `fixture_manifest.yaml`, never hardcoded in test bodies; §15.4's `artifact_manifest.json` hash-listing required as well; D-11's pre-freeze obligation on ARUC), REQ-ENG-10 (the §13.1 eight-item environment lock, `UNTESTED`), § Known defects rows 8, 9 and 12.
- `../../../inception/application-design/services.md` — `run_walking_skeleton.py`'s row (orchestrator, phases 1 and 2, reads `--fixture`, writes the fixture run log); § Stage entry contract (foundation's **six** ordered steps, identical in all nine scripts, an **approved surface**; failure in steps 1–5 exits non-zero naming file and expectation and writes an `aborted` row); § Ordering contract (`run_walking_skeleton.py` **enforces** the ordering, it does not merely document it; each stage reads only artifacts a prior stage released, **identified by release ID and verified by hash**, never by path convention); the `02` ordinal reading (one `02` per phase, `--phase` selects) — **an ordinal fact about naming, never a licence to execute both `02` scripts in one sequence; R-138 as corrected 2026-08-28 executes §13.2's seven Phase 1 invocations and defers the Phase 2 segment to G-P2**; § Execution platforms (exactly two, TC-03c; **Kaggle carries no git working tree**; `resolve_platform_roots` writes the resolved values into the environment lock; a run whose recorded platform is neither **fails**); the M9 bundle-directory naming rule and the M13 envelope note. § Ordering contract's "precondition currently unmet" paragraph is **superseded on the station limb** by D-20 and is cited as history, not current fact.
- `../../../inception/application-design/component-methods.md` — § Depth (**Q1 = B**: full signatures at cross-package boundaries only; **this unit has no approved cross-package signature of its own** — the orchestrator is a script row in `services.md` and the manifests are data, so every shape here is intra-unit or test apparatus); `ConfigSnapshot` (`platform: "kaggle" | "local"`, `resolved_roots`, `snapshot_dir`, four config hashes) and `load_configs`/`assert_no_tbd`/`assert_declared_sources_exist`/`resolve_platform_roots`; the ADR-11 `FeatureBundle` architecture, the **containment-not-equality** correction (a `score` spec covering seven days inside November **passes**), and the `lead_in_hours` removal.
- `../foundation/functional-design/business-rules.md` — **READY**: R-01 (all **fourteen** project exceptions derive from `IntegrityError`, base declared in `src/data/config.py`, six raised by `foundation` and eight by other units; **no fixture-specific exception is among the fourteen**; the constructor requires the affected file or resource **and** the violated expectation; the negative control proves an unenumerated subclass is still caught), R-05 (determinism first, the re-exec sentinel read once and unset, module-scope framework imports prohibited transitively), R-09/R-10 (a failed or aborted run stays visible; report honestly even when reporting fails), R-15 (only `foundation` reads `configs/`), R-16 (no machine path in a governed config), R-17 (docstrings), § Stage entry contract; the OPEN item that each raising unit's 3.1 declares its own exceptions.
- `../features-and-splits/functional-design/business-rules.md` — **READY**: R-74's four elements and its **controls that must not fire** (the D-11 seven-day `score` containment **passes**; `fit_transforms` **range equality** with the partition's training range; identity by enumeration over the six partition ids; exactly one enumerated `REFIT` → `DEC` `score` exception; `transform_id is None` raises), R-80 (the partition list — F1…F4, `REFIT`, `DEC`; exact calendar boundaries; exactly-one holds over **evaluation role**, the training ranges nesting), R-82 (the locked partition materialises only against a verified `g05_signature`); **FU-7 = A** (G-06 scores 2–31 December, 30 days); BLK-04/BLK-09's home.
- `../statistical-inference/functional-design/business-rules.md` — **READY**: R-120 clause 4 (**the widening guard's doubled CPU cost is measured at fixture time and frozen into the fixture manifest per §15.2** — a named slot this unit's schema carries) and clause 3 (the comparator's numbers **never serialized as a reported interval**), R-121 control (22) (**the planted-correlation recovery tolerance lives in the fixture manifest, not in the rule** — §13.7's fixture-derived-tolerance discipline), R-122 (fixture parameters are **declared constants of the test apparatus, explicitly not scientific values**; the scientific values arrive from config even under test; assertion data in `tests/fixtures/<fixture_id>/fixture_manifest.yaml`, never hardcoded — the manifest convention consumed **beyond** this unit's two directories).
- `../evaluation-and-comparison/functional-design/business-rules.md` — **READY**: R-103 (the **BLK-08 joint** transform-resolution contract, one statement in two halves), R-104 (inverse-before-metric enforced at the boundary every caller crosses — the TECU bound that reaches this unit's tolerances), R-106/R-107 (declared comparison-set membership; mask identity and the G-05 freeze), R-108 (the estimand's machine-readable orientation/weighting/sign fields), R-109 (hash-receipt before metrics, one chokepoint, exactly 2–31 December), R-110 (the **emit-from-the-producing-path** pattern this unit adopts for the `smoke_only` stamp and the DATA-07 caveat), R-111 (`tests/test_common_masks.py` and the WS-13 proposal), R-112.
- `../regimes-diagnostics-reporting/functional-design/business-rules.md` — **READY**: R-123…R-132; R-127/R-129 (stamped artifacts, the required-plot inventory asserted complete — the completeness pattern R-142's bounded table follows), R-125's units assertion (BLK-08 ↓ made checked at the reporting surface, the precedent R-139 applies at the tolerance surface); the "fixture parameters as test apparatus" reading restated there; its § Assumptions carry the **"fourteen"** figure whose cross-representation sweep a fifteenth exception would oblige.
- `../governance-guards/functional-design/business-rules.md` — **READY**: R-23/R-24 (both phase-boundary limbs run; run time authoritative, static scan subordinate, **both** run), R-25/R-26 (the access log appends durably **before** any December read; what counts as a December hit and the bounded driver exclusion), R-27/R-28 (one path into the restricted root) — the clean-run sequence must be executable **without a single December hit**, both fixtures being December-free by construction.
- `../acquisition/functional-design/business-rules.md` and `../inventory-and-registry/functional-design/business-rules.md` — **READY**: R-31 (**membership derives from record timestamps, never from a name** — FR-WS-3's mechanism, whose negative control `tests/test_acquisition_window.py` already exists and is green), R-36 (hashing covers provider files; **pre-TC-06 months say what they are**), R-42 (a derived release's provenance is current or re-pointed by a D-number), R-44…R-53 (the registry, schema-validation and hash tooling TA-04 says must operate on both fixtures), R-50 (the December audit logs per artifact).
- `../target-standardization/functional-design/` and `../external-products/functional-design/` and `../models-and-baselines/functional-design/` — the released artifacts the fixture runs produce and the clean run compares; R-55's amendment basis (**5 across 3**); R-100's `authoritative = false` labelling.
- `evidence/DECISIONS.md` — **D-11** (window 2022-11-01…07 inclusive; three-cell measured completeness ARUC 163/168, BSHM 168/168, NICO 155/168, 7/7 day presence; the **mandatory not-representative-of-December limitation**; the **provisional-Dst restriction** — selection characterisation only, never a modelling input, a frozen tolerance, or a G-05 regime count; "Not decided here"), the **D-11 clarification of 2026-08-22** (the `Stations:` line is **eligibility evidence**; §15.1's one-station execution scope retained), **D-20** (station **BSHM 32/35**, selected on 168/168 hourly bins from `evidence/audit_evidence_2022-11/madrigal_coverage_raw_records.csv`; ARUC's shortfall not discharged and not needing to be), **D-14** (**March 2022, 2022-03-01…31 inclusive, all three cells**; its **Mandatory limitation in both clauses** — (i) March 2022 is an equinox month and *"does not reproduce December's winter-solstice regime or its activity distribution"*, and (ii) *"It is **not** representative of the locked test month, and **no fixture result may be read as evidence about December behaviour**"*; "Measured, not invented"), D-15 (locked-month custody relocation), D-17/D-19 (the target contract and support thresholds the fixture's expected-schema block asserts), D-18 (the traversal-order lesson NFR-REP-01 cites).
- `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — §9.1/§9.2 (two platforms; **both fixtures before any full-year job**; the in-session rule), §9.3 (the 10.0 GB envelope), §13.1 (the **eight**-item environment lock), **§13.2 as amended** (`PYTHONHASHSEED=0` set once **before the first command**; the **Phase 1 segment of 9 `python` invocations = the two `run_walking_skeleton.py` calls + seven Phase 1 stage scripts**, and the separate segment gated `# Phase 2, only after G-P2` carrying **7** invocations of which **`02_build_vtec_target.py`** and **`03_verify_processing.py`** appear nowhere else — derived 2026-08-28 by parsing the fence; TE:795's clarification that §12's *"nine phase-aware stages"* counts the nine **distinct** scripts spanning both segments, **not** a sequence to execute; *"Both fixtures must pass before full execution. The whole sequence must complete on CPU."*; *"Exact counts, tolerances, and runtimes are measured from the fixtures and frozen; they are not invented here."*), §13.3, §13.4, §13.5, §13.7 (**exact equality required for hashes, schemas, partition membership, IDs and deterministic CPU transformations**; fixture-derived tolerances elsewhere; *"it must not silently update the expected value"*), §15.1 (two fixture date windows; **"One station"** for `plumbing_7day`; all three stations for `scientific_1month`; the **binding limitation** that the seven-day LSTM result *"is explicitly not scientific evidence"* and *"may not be cited, plotted as a result, or interpreted as skill"*), **§15.2** (the fixture-manifest table), §15.3 (fixture 1 runs M-01…M-05 and a **minimal M-06 that saves and restores its best checkpoint**, plus B-01 and C-01 sample generation; fixture 2 runs the complete ladder across all three stations with pooled masks and one reduced-replicate bootstrap for timing), **§15.4** (the required-output tree; *"Every output is hash-listed in `artifact_manifest.json`."*), §16 and §16.1 (WS-01…WS-20; the G-P3A deferral), §18.3 (the preflight gate, its ten named critical tests, and the **stop-and-report** rule binding every agent), §19 (TA-03, TA-04, TA-09 with its 2026-08-22 Phase 1 bound, TA-17, TA-21, TA-23, TA-26, TA-27).
- `aidlc/spaces/default/memory/team.md` § Walking Skeleton — the eligibility criterion (**derived-artifact verification, not retrieval verification**: a month is eligible when its four declared artifacts verify against its `sha256_manifest.json` and per-day coverage is present in all three cells); the **DATA-07 interim caveat, binding until the `raw_isprint_cache/` re-acquisition completes** — provenance of the pre-TC-06 evidence is **unverifiable in principle**, and every artifact produced before the re-acquisition **must state the caveat wherever coverage figures are relied on**; completeness figures **measured, not tested against a threshold**; § Testing Posture — §13.2 as the reproducibility test's actual definition, the seventeen-module `tests/` tree, **G-07 (Blocked, Supervisor)** as the accepting gate with evidence `environment_and_cpu_preflight_report` plus the clean-run log and matched artifacts, the negative-control-per-hard-rule methodology, the two-tier error posture; § Deployment (the two platforms; releases as this project's deployments).
- `aidlc/spaces/default/memory/project.md` § Mandated/Forbidden — both fixtures in order before any full-year job and the seven-day fixture never scientific evidence (TC-03f); **CPU a complete execution path** (TC-01); the in-session Kaggle rule (TC-03g, TA-03, TA-26); membership never from a directory name (ML-07); the `phase_id`/`source_id`/`target_definition_id` stamps (TEC-05); no scientific constant in source (TC-03e); **NEVER let a coding agent fill a "TBD — freeze gate" value by convenience**; **NEVER change a scientific value after seeing any result**; the two-tier error posture; § Way of Working's count-derivation and representation-sweep corrections.
- Workspace inspection, **2026-08-28**: `tests/` holds exactly three modules — `test_acquisition_window.py`, `test_phase_boundary.py`, `test_release_hashes.py` — **none this unit's**; **no `tests/fixtures/` directory**; `src/`, `configs/` and `pyproject.toml` absent; `scripts/` holds only the two pre-scaffold audit scripts; `evidence/audit_evidence_2022-11/` and `evidence/audit_evidence_2022-03/` each present with the same five entries plus `raw_isprint_cache/`, and each `sha256_manifest.json` hashes exactly **four** derived files.
- `functional-design-questions.md` (**Q1 through Q9, all answered `C`**; Consolidated Summary Confirmation receipted `Looks correct`), `business-logic-model.md`, `domain-entities.md`.

---

## R-133 — One manifest schema, one validating loader, and the loader is the only read path

**Rule (Q1 = C).** There is **exactly one fixture-manifest schema** and **exactly one
validating loader**, and every consumer — `run_walking_skeleton.py`,
`tests/test_clean_run.py`, and the sibling test modules R-122 points at the same
`tests/fixtures/<fixture_id>/fixture_manifest.yaml` convention — reads a manifest **only**
through it. The loader validates on read and **rejects**, naming the file and the missing
or violated expectation per the two-tier posture (`foundation` R-01's constructor
contract). Four obligations:

1. **Every TE §15.2 content area is a required block, enumerated by name.** The schema
   names the areas rather than counting them, so the block set stays correct whichever
   numeral a downstream register carries: **Identity, Inputs, Processing, Expected schema,
   Units, Row-count ranges, Support/missingness, Timestamp tolerances, Independent
   reference checks, Required outputs, Runtime, Numerical variation.**

   > **⚠ The count "thirteen" does not survive derivation — a conflict raised, not
   > resolved.** Derived 2026-08-28 by extracting `^| ` rows from §15.2's table:
   > **13 rows, of which one is the `| Area | Required manifest content |` header → 12
   > content areas.** `requirements.md` REQ-ENG-4 asserts *"all thirteen of TE §15.2's
   > content areas"* and then **enumerates nine** (identity, input hashes, expected
   > schema, row-count ranges, support and missingness limits, timestamp tolerances,
   > required outputs, expected CPU runtime range, permitted floating-point tolerances);
   > the three §15.2 areas absent from that enumeration are **Processing**, **Units** and
   > **Independent reference checks**, and 9 + 3 = 12 — the same figure the table yields.
   > So three representations disagree: **13** (claimed in REQ-ENG-4, in this stage's own
   > question file and in its receipted summary), **9** (enumerated inside REQ-ENG-4's own
   > sentence), **12** (derived from the source table). The 13 is the row count *including
   > the header*. This design binds to the **named twelve**; correcting REQ-ENG-4's
   > numeral and its short enumeration is a `requirements.md` change outside this stage's
   > produces list, and correcting the receipted summary's numeral is not this stage's
   > either — **both are reported at the gate, not applied here.**

2. **Three of the twelve areas name Phase 2 quantities Phase 1 is barred from producing** —
   Inputs (RINEX/CRX, DCB), Processing (`gnss-tec` version, calibration-layer commit) and
   Independent reference checks (STEC/VTEC intermediates, the hand-worked DCB pass).
   Requiring all twelve blocks **non-empty** on a Phase 1 fixture manifest would demand
   exactly the raw-processing evidence TE §7.0's Phase 1 hard prohibition bars and
   NFR-PHASE-01 forbids — structurally the same contradiction § Known defects row 1
   records for §16's "all 20". **Reading proposed, not applied:** every block is required
   **present**; a Phase 2-only quantity inside a block is recorded **`not_applicable` with
   its reason**, never absent and never emitted empty — the FR-P1-03-5 precedent
   (*"recorded not-applicable rather than emitted empty"*). A missing **block** still
   fails; `not_applicable` on a Phase-1-applicable quantity fails. **Routed to the gate**,
   because narrowing §15.2 by inference is not this stage's to do.
3. **The §15.4 cross-check.** The manifest's Required-outputs block cross-references
   §15.4's `artifact_manifest.json`, and the loader asserts the hash-listing agrees with
   the files on disk. §15.4's tree yields, derived 2026-08-28 by enumerating its entries:
   **22 lines → 20 hash-listable outputs** (excluding the `plots/` directory line and
   `artifact_manifest.json` itself, which cannot list its own hash), of which
   `target_uncertainty_budget.json` is fixture-2-only → **20 for `scientific_1month`, 19
   for `plumbing_7day`**. The Required-outputs block is asserted **complete against that
   enumeration**, the R-129 inventory-completeness pattern applied to outputs.
4. **The named cross-unit slots**, carried because two READY siblings already rely on
   them: `statistical-inference` **R-120 clause 4**'s measured widening-guard runtime (the
   doubled CPU cost, measured at fixture time and frozen — a Runtime-block slot) and
   **R-121**'s per-check tolerances (the planted-correlation recovery tolerance — a
   Numerical-variation slot). R-122's general convention means the schema is consumed
   beyond this unit's two directories; whether a sibling's synthetic fixture warrants its
   own `tests/fixtures/` directory is that sibling's §12 question, not this one's.
5. **The §15.3 reduced-replicate fixture bootstrap is declared here, as a constant of the
   test apparatus** *(added 2026-08-28 per `GOV-2026-08-28-FD-01` Recommendation 24, board
   option 2 — the board's stated preference)*. §15.3 **requires** it, verbatim: *"Fixture 2
   must run the complete ladder across all three stations with pooled comparison-wide
   masks, the full benchmark join at evaluation time, and **one bootstrap execution at
   reduced replicate count for timing**."* Derived 2026-08-28 across all twelve units:
   `reduced-replicate` / `reduced replicate` appears **once** — in this file's own § Sources
   citation of §15.3 — and **zero** times in `statistical-inference`, which owns
   `vector_block_bootstrap`. So the requirement is mandatory and designed nowhere. It is
   designed here, in `tests/fixtures/scientific_1month/fixture_manifest.yaml`, on **R-122's
   already-established authority** that *fixture parameters are declared constants of the
   test apparatus, explicitly **not** scientific values* — the same authority **R-137** uses
   for the fixture partition ids — and because **§15.2's Runtime block already requires the
   fixture's runtime figures to live here**. Three declared fields, none of them a value
   this design states:

   | Manifest field | What it declares | Why it must be here rather than in `experiment.yaml` |
   |---|---|---|
   | `fixture_bootstrap.replicates` | the reduced count, **for timing only**, never reported | `statistical-inference` **R-118** declares `replicates` in `experiment.yaml` *passed explicitly at every call with the signature defaults never exercised*, and its control (17) **fails a confirmatory interval whose recorded `replicates` differs from the config-declared value** — so a second `experiment.yaml` value would either collide with that control or make a timing smoke-test look like a scientific run in the registry. As apparatus, it does neither. |
   | `fixture_bootstrap.scored_range` | the fixture bootstrap's scored range, in hours, from the apparatus-partition declaration (R-137) | makes `statistical-inference` **R-115** limb 1's divisibility raise **checkable rather than latent** — R-115's *"never fires"* is derived over `DEC` only |
   | `fixture_bootstrap.block_counts` | whole blocks at **24 h** and at **48 h** over that range | the same limb: a range not evenly divisible by the block length **raises `BootstrapError`** rather than truncating or padding |

   **Why the scored range must be declared and not assumed.** Derived arithmetic on the
   ranges in play (calendar facts, not measured values): the **raw March fixture window is
   744 h** (31 × 24) → 31 whole 24-h blocks but **15.5** at 48 h; the **April and November
   validation months after the 24-h exclusion are 696 h each** → 29 and **14.5**; the **raw
   seven-day plumbing window is 168 h** → 7 and **3.5**. The 48-hour sensitivity is
   therefore **indivisible on every one of them**, so a fixture bootstrap pointed at a raw
   window would raise. The scored range the apparatus partitions actually declare is
   **measured and frozen under §15.1 by the Q-31 authority and is not stated here**; what is
   fixed here is that it **must be declared with its two block counts**, so the divisibility
   limb is evaluated at freeze rather than discovered at run time.

   **Two things this limb explicitly does not do.** It states **no number** — the reduced
   count is a measured/declared apparatus value frozen by the Q-31 act (R-134), and §15.1
   bars inventing it. And it does **not** reclassify the replicate count wherever it appears:
   if the owner rules that a replicate count is a **protocol** value everywhere, board option
   1 applies instead — register the fixture bootstrap as a predeclared named run in
   `experiment.yaml`, exactly as R-118 handled the 48-hour sensitivity — and this limb moves
   there unchanged. **Routed to the gate as a classification question.**

   **Noted, not assumed:** `statistical-inference` is being amended in parallel so **R-120's
   widening comparator uses the *same* replicate count as its primary call** rather than the
   literal **10,000** its limb 1 currently pins. Without that amendment a reduced-replicate
   primary against a full-replicate comparator is not like-for-like and biases the guard
   toward firing, since a 2.5/97.5 percentile interval is unstable at low replicate counts.
   This unit does not make that amendment and does not depend on having made it — R-138's
   new must-not-fire control is what surfaces it if it does not land.

**The loader's home is routed to the gate with both candidates named**, because TE §12
names no module for it and this stage may not amend §12 by assertion:

| Candidate | Consequence |
|---|---|
| A function set in `foundation`'s `src/data/` as a **cross-unit contract** (mirroring how the eight non-`foundation` exceptions import the base from `src/data/config.py`) | Mints a new `component-methods.md` boundary surface, so the amendment ledger takes **+1, to 8 across 6, at that ruling** (§ Amendments owed). The only-copy check in control (4) then scopes project-wide rather than to this unit. Puts test-apparatus data loading into a production package. |
| A **test-apparatus helper under `tests/fixtures/`** | Adds **no** amendment. But `run_walking_skeleton.py` — a `scripts/` module — would import from the test tree, which §12 does not forbid and no other script does. The only-copy check scopes to this unit. |

Neither is chosen here. R-15 does not reach the question: a fixture manifest is not
`configs/`, so `foundation`'s exclusive read of the four governed configs is untouched
either way.

**Negative controls.** (1) A manifest missing **any one** of the twelve named content
areas → **fails validation**, asserted **per area by enumeration** (one synthetic case per
area, so the check cannot pass by testing only the areas someone remembered). (2) A
manifest whose §15.4 `artifact_manifest.json` is **absent**, or whose hash-listing
**disagrees with the files on disk** → **fails**. (3) A Required-outputs entry with **no
declared comparison class** (R-139's ledger) → **fails**. (4) A **second YAML parse** of a
fixture manifest anywhere in this unit's scope → **fails** a grep-style only-copy check,
so the single-loader discipline is asserted rather than asked for. (37, added 2026-08-28
per Recommendation 24) A `scientific_1month` manifest **missing any of limb 5's three
`fixture_bootstrap` fields** — the reduced replicate count, the scored range, or the block
counts at 24 h and 48 h — → **fails validation**; and a declared `scored_range` **not evenly
divisible by either declared block length** → **fails at freeze**, so `statistical-inference`
R-115 limb 1's raise is evaluated before the run rather than discovered inside it.

**Control that must *not* fire:** a frozen manifest carrying all twelve blocks with the
Phase 2-only quantities recorded `not_applicable` and their reasons → **validates** (limb
2's proposed reading; if the gate rejects it, this control and control (1)'s Phase-2 area
cases are what change).

**Acceptance.** TA-09 (primary, **bounded to 13 rows**), WS-20 (primary — the manifests
are named in its evidence column); TA-04 (supporting).

## R-134 — Measure then freeze: two manifest states, identity by citation, and no silent update

**Rule (Q2 = C).** TE §15.1 and §13.2 both state it — *"exact counts, tolerances, and
runtimes are measured from the fixtures and frozen; they are not invented here"* — and
BLK-02 states it operationally: **no value may be invented, inferred or substituted**, the
manifests do not exist, and neither fixture has ever run. The design makes that a workflow
rather than a sentence:

1. **`status: candidate`** is what a **measuring run** emits. Its **identity fields are
   cited from the D-numbers and never re-derived** — D-11's window and its mandatory
   limitation, D-20's station, and **D-14's month with its Mandatory limitation in both
   clauses**: (i) the equinox-month clause (*"does not reproduce December's winter-solstice
   regime or its activity distribution"*) **and** (ii) the operative prohibition, *"It is
   **not** representative of the locked test month, and **no fixture result may be read as
   evidence about December behaviour**"* — and each of its **measured** fields (row-count
   ranges, support and missingness limits, timestamp tolerances, runtime ranges,
   floating-point tolerances) carries the **measuring run's registry id** as provenance. A
   measured field **without** a run id is unrepresentable, which is precisely what makes an
   invented value have nowhere to hide.

   > **⚠ D-14's second clause is enumerated, not labelled** *(added 2026-08-28 per
   > `GOV-2026-08-28-FD-01` Recommendation 36, board option 2)*. Derived across all 48 stage
   > artifacts: the string `evidence about December behaviour` returned **0 hits** — the
   > operative half of D-14's Mandatory limitation existed nowhere, while D-11's clauses were
   > enumerated in full at four sites and D-14's were carried only as the label *"equinox
   > limitation"*. This is load-bearing rather than tidy: **R-136 correctly scopes the
   > `evidence_class: smoke_only` quarantine to `plumbing_7day` only**, so the scientific
   > fixture's outputs legitimately *can* serve WS-12/WS-13/WS-16/WS-17 evidence — which
   > makes clause (ii) the **only** barrier between a March number and a December reading.
   > It is therefore also given machine-readable freight (R-135's
   > `december_representativeness` field), on the identical argument this unit already made
   > for the `data07_caveat`: *a caveat living in prose outside the artifact is exactly the
   > kind that fails to appear there*.
2. **`status: frozen`** is set only by a **separate recorded human act under Q-31** (TE
   §18.2 assigns fixture station, dates and acceptance tolerances to the Student), which
   also records the **manifest's own hash** in the evidence record. **Nothing in this
   design performs that act.**
3. **After freeze, every mismatch raises**, naming file and violated expectation, and
   **never updates the expected value** (NFR-REP-01; §13.7). Re-measurement happens only
   through a **new candidate and a new freeze act**, and the superseded manifest is
   **preserved, never overwritten** (the `foundation` R-13 release-directory posture and
   §13.3's new-version rule applied to test apparatus).
4. **D-11's measured completeness figures enter as recorded eligibility evidence, not as
   expected assertion values.** D-11 reports three cells (ARUC 163/168, BSHM 168/168,
   NICO 155/168, 7/7 day presence); the plumbing fixture **executes on one** (§15.1, D-20),
   so its expected counts are measured from its **BSHM-only** run. Conflating the two would
   turn a three-cell eligibility record into a three-cell execution expectation — the exact
   confusion § Known defects row 12 took two governance rounds to untangle.

**No scientific value is decided.** Window, station, month, seeds, partitions and grids are
frozen elsewhere; everything else is measured under §15.1 and frozen by the Q-31 authority.
Where a required value is unfrozen, TE §18.3's rule governs: **stop and report, never
choose a default.**

**Negative controls.** (5) A run against a `candidate` manifest **cannot produce
WS-20/TA-09/TA-17 evidence** — the evidence emitters **refuse** when the manifest is not
frozen. (6) A **post-freeze edit without a new freeze act** → **fails** the manifest
self-hash check. (7) A manifest whose **identity fields disagree with the cited D-number
record** → **fails**. (8) A **measured field with no measuring-run registry id** →
**fails**, so an invented number is rejected at the shape rather than argued about.

**Control that must *not* fire:** a candidate manifest emitted by a measuring run, with
every measured field carrying its run id → **validates and is offered for freeze** (it is
simply barred from evidence until frozen).

**Acceptance.** WS-20, TA-09, TA-17 (primary — all three gated on `frozen` by control (5));
TA-23 (supporting — **`foundation` primary; its evidence artifact
`aws_ai_dlc_preflight_report` and its discharging requirement FR-WS-7 are both
`foundation`'s, not this unit's — see R-142**).

## R-135 — The plumbing fixture: identity cited, one-station scope enforced, DATA-07 and the December-representativeness prohibition travelling as freight

**Rule (Q3 = C).** The `plumbing_7day` manifest **cites** D-11 and D-20 by D-number
(window **2022-11-01…07 inclusive**; station **BSHM 32/35**) and carries, **verbatim in a
limitations block**, D-11's **mandatory not-representative-of-December limitation** and the
**provisional-Dst restriction** (provisional values may characterise selection only — never
a modelling input, a frozen tolerance, or a G-05 regime count). **ARUC's one-bin shortfall
is recorded `dormant`, not `discharged`** — the register's own word — with its reactivation
condition attached, so the dormancy cannot be read as closure. Three enforcement limbs:

1. **One-station scope is a raise, not a reading.** Fixture assembly **fails** on a record
   from any station other than the frozen D-20 selection. §15.1's "One station" is retained
   by the D-11 clarification and is enforced here rather than restated.
2. **Eligibility is re-verified at use, not assumed from the selection record.** The
   Inputs block verifies the month's **four declared derived artifacts** against
   `evidence/audit_evidence_2022-11/sha256_manifest.json` — the same **derived-artifact
   verification** that made the month eligible (`team.md` § Walking Skeleton, corrected
   after `CHAIR-02`), and the same four-file shape the workspace inspection confirms.
3. **The DATA-07 caveat is a machine-readable manifest field, propagated onto the fixture
   run log and every artifact carrying the fixture's coverage figures**, until the
   `raw_isprint_cache/` re-acquisition discharges it. This is R-110's
   emit-from-the-producing-path pattern applied to a caveat: `team.md` binds the caveat to
   appear *"wherever FULL's coverage figures are relied on"*, and a caveat living in prose
   outside the artifact is exactly the kind that fails to appear there.
4. **`december_representativeness: not_representative` is a second machine-readable field,
   on `FixtureArtifactStamp`, for *both* fixtures** *(added 2026-08-28 per
   `GOV-2026-08-28-FD-01` Recommendation 36, board option 2)*. It carries the operative
   second clause of the governing limitation — **D-11's** for `plumbing_7day` and **D-14's**
   for `scientific_1month` — and it is **asserted present wherever a fixture-derived figure
   is reported**, exactly as `data07_caveat` is. The field's own justification is the one
   this unit already accepted for that caveat and which applies here verbatim: *a caveat
   living in prose outside the artifact is exactly the kind that fails to appear there.*

   **Why both fixtures and not just the smoke one.** R-136's `smoke_only` quarantine is
   correctly scoped to `plumbing_7day` alone, so `scientific_1month`'s outputs *are* allowed
   to be evidence for WS-12, WS-13, WS-16 and WS-17. That is precisely why the scientific
   fixture needs the field **more**, not less: without it the fixture whose numbers may be
   cited would carry a **weaker** caveat than the fixture whose numbers may not. The field
   **flags rather than adjudicates** — it cannot distinguish a legitimate methodological
   citation from an illegitimate December inference, and it is not claimed to; what it does
   is make the prohibition travel with the number instead of living in a decision record the
   citing surface never reads.

**Provenance is unverifiable in principle, not merely unverified.** The pre-TC-06 evidence
these fixtures read has no provider byte stream anywhere in the workspace. The caveat
records that; it does not repair it, and no fixture result may be read as though it did.

**Negative controls.** (9) A **planted ARUC or NICO record** in the assembled plumbing
input → **fails**. (10) A manifest **naming any station other than BSHM 32/35** → **fails**
against the D-20 citation. (11) A **coverage figure emitted from the fixture without the
DATA-07 caveat field** → **fails**. (12) An **input artifact whose hash disagrees with the
month's `sha256_manifest.json`** → **fails before the fixture runs**, the eligibility check
re-executed at use. (38, added 2026-08-28 per Recommendation 36) A **fixture-derived figure
reported without the `december_representativeness` field** — from *either* fixture — →
**fails**, and a **`scientific_1month` artifact cited as December evidence is caught** by
that field's presence at the citing surface. The limb-4 field is thereby tested, not
documented.

**Controls that must *not* fire:** the four November artifacts verifying against their
`sha256_manifest.json`, with BSHM-only records assembled and **both** the `data07_caveat`
and `december_representativeness` fields present → **assembly proceeds**.

**Acceptance.** WS-20, TA-09 (primary); TA-04 (supporting — the hash tooling operating on
this fixture is `inventory-and-registry`'s, invoked here).

## R-136 — The plumbing fixture is never evidence, and December is excluded on record dates

**Rule (Q4 = C).** This unit's **two untested requirements** become designed falsifiers.

**FR-WS-2 — the smoke quarantine.** Every artifact the plumbing fixture produces is
stamped **`evidence_class: smoke_only` by the producing path** (R-110's pattern: the stamp
travels *with* the artifact, so it cannot be lost in a hand-off), and **every
evidence-bearing surface asserts the absence of `smoke_only` inputs** — results artifacts,
the TA-09 acceptance table, releases, and the traceability matrix. A plumbing-derived
figure entering evidence therefore fails **structurally**, not on review. This matters
because §15.3 **requires** fixture 1 to run M-01…M-05 and a minimal M-06: a seven-day LSTM
number really is produced, and TE §15.1's binding limitation is that it *"may not be cited,
plotted as a result, or interpreted as skill."*

**FR-WS-3 — the record-date assertion.** Fixture assembly asserts every input record's
**observation date** against the window bounds and the December exclusion, **on record
timestamps**, by **consuming `acquisition` R-31's membership rule and
`tests/test_acquisition_window.py`'s existing predicate rather than duplicating either** —
no third copy. `test_acquisition_window.py` is one of the three modules that exist today
and is green, including the case that produced the original defect.

**The acceptance-row gap is routed, never narrowed.** Both requirements are marked **NO
CURRENT ACCEPTANCE ROW** by the story map. Two **candidate Vision §15.2 acceptance rows**
are **proposed at the gate and not applied** — a §15.2 amendment is the owner's, and
`requirements.md` § Known defects already models the shape — each naming the
machine-readable check result its evidence column would point at: the `smoke_only`
absence-assertion result for FR-WS-2, and the record-date assembly-assertion result for
FR-WS-3. Until then the falsifiers below are the coverage, and the 2-of-8 figure stands
as recorded.

**Negative controls.** (13) A **`smoke_only`-stamped artifact planted into a results
artifact or the TA-09 table** → **fails**. (14) A **December-dated record planted inside a
fixture input** → **caught at assembly by record date**, with the **folder name
deliberately mislabelled in the fixture** to prove the predicate ignores it — encoding the
exact TEC-09 history (`audit_evidence_2022-01/` carrying locked-month records) that made
record-date the rule.

**Control that must *not* fire:** a November-dated record in a directory whose name
mentions December → **admitted**, because the predicate reads the record and not the name.
(The converse of control (14), and the reason the rule is stated on record dates.)

**Acceptance.** ⚠ **No row for either requirement** — candidate §15.2 rows proposed at the
gate, never applied here.

## R-137 — Fixture partitions are apparatus constants in a quarantined id space, and the M10 step is named

**Rule (Q5 = C).** A collision the READY siblings leave at this unit's door: the plumbing
window is representable — R-74's controls-that-must-not-fire list a `score` spec covering
seven days inside November as one that **passes** (containment in F4's validation month) —
but the scientific fixture is **March 2022** (D-14), and March is inside **no** validation
month (Apr, Jul, Oct, Nov, Dec) while a `train`-role fit must equal the partition's
training range **exactly** (R-74 element 1, ADR-11's strengthening). Under R-80's frozen
list a March-only frame can lawfully neither fit nor score.

**The way out has an in-project precedent on exactly this shape.** R-122 declares fixture
parameters **constants of the test apparatus, explicitly not scientific values**, and the
M10 contract fixture already uses **synthetic partition dates** on that authority. So:

1. The `scientific_1month` manifest **declares a fixture partition set over the March
   window**, with ids **distinct from the six frozen partition ids** (F1…F4, `REFIT`,
   `DEC`) — declared apparatus constants, stamped on every artifact they produce.
2. **Stages 05–07 run against them at fixture scale**, which is what gives WS-12, WS-13,
   WS-16 and WS-17 a scientific-fixture path at all.
3. **The quarantine holds both ways**: no fixture artifact may carry a frozen confirmatory
   partition id, and no fixture partition id may enter the six-id space, so ADR-11's
   identity enumeration stays intact and **no seventh enumerated exception is minted**.
4. **Because WS-12/WS-13 fixture-evidence semantics turn on this reading, it is routed to
   the gate as a proposal, not adopted silently.** R-81 already records WS-13's evidence
   question as open in its own lane.

**The M10 contract fixture executes as its own named step of the clean-run sequence** —
after the plumbing fixture, invoking the two `features-and-splits`-authored modules
(`test_train_only_transforms.py`, `test_split_embargo.py`). Its **placement is recorded in
§13.2 terms as a proposal**: the sequence's text is the authority and adding a step is not
this stage's to apply. §9.2's boundary is asserted alongside it — the M10 step **gates no
full-year job**, the **two**-fixture ordering contract is unchanged and unextended, and
the M10 result is recorded **in the clean-run evidence, not as a third receipt** (R-140).
**Running it here is what puts it inside TA-17's and WS-20's reach**, which was the whole
point of the owner's Q12 = C split.

**Negative controls.** (15) A **fixture artifact carrying any of the six frozen partition
ids** → **fails**. (16) A **fixture partition id offered to the ADR-11 identity check** →
**raises** like any mismatched pair, no seventh exception minted. (17) **The M10 step
absent from the executed sequence** → **fails `test_clean_run.py`**.

**Controls that must *not* fire:** a `score` spec covering the seven days inside November
→ **passes** (R-74's inherited must-not-fire, containment not equality); the M10 fixture's
own result recorded in the clean-run evidence → **is not** counted as a third mandated
fixture and **does not** gate a full-year job.

**Acceptance.** WS-20, TA-17 (primary — the M10 step's reach is the ruling's stated
purpose); ⚠ WS-12/WS-13 fixture-evidence semantics are the gate item, not this rule's
claim.

## R-138 — The clean run executes the amended §13.2 sequence verbatim — the seven Phase 1 invocations, Phase 2 deferred to G-P2 — on CPU, with no GPU visible

**Rule (Q6 = C; segment membership corrected 2026-08-28 per `GOV-2026-08-28-FD-01`
Recommendation 5, board option 1).** `tests/test_clean_run.py` executes the **amended**
§13.2 sequence **verbatim** in a **fresh environment**, with **`PYTHONHASHSEED=0` set once
before the first command** (BLK-01's closure under `CR-2026-08-22-TE-AMEND`, so WS-20 and
TA-17 test the amended sequence and not an unamended one), then
`run_walking_skeleton.py --config configs/ --fixture plumbing_7day`, then
`--fixture scientific_1month`, then **the seven Phase 1 stage-script invocations of §13.2,
in §13.2's order and exactly as §13.2 writes them** — while **§13.2's Phase 2 segment,
which the fence itself gates `# Phase 2, only after G-P2`, is deferred to G-P2 and is
**not** executed by this test**, the same form this unit already uses for TA-27's second
limb (R-142):

| # | §13.2 Phase 1 invocation |
|---|---|
| 1 | `python scripts/00_acquire_prepared_vtec.py --config configs/` |
| 2 | `python scripts/01_inventory_and_registry.py --config configs/ --phase 1` |
| 3 | `python scripts/02_standardize_prepared_target.py --config configs/` |
| 4 | `python scripts/04_build_external_products.py --config configs/ --phase 1` |
| 5 | `python scripts/05_build_features_and_splits.py --config configs/ --phase 1` |
| 6 | `python scripts/06_train_and_predict.py --config configs/ --phase 1` |
| 7 | `python scripts/07_evaluate_and_report.py --config configs/ --phase 1` |

> **⚠ The superseded reading — "then the nine phase-aware stage scripts, one `02` per
> phase, `--phase` selecting" — was defective in both directions, and is corrected here,
> not narrowed.** Derived 2026-08-28 by parsing §13.2's fenced block (TE:765–789)
> programmatically: the **Phase 1 segment is 9 `python` invocations = 2 ×
> `run_walking_skeleton.py` + 7 stage scripts**; the Phase 2 segment is **7** invocations;
> and exactly **two** distinct scripts appear **only** below `# Phase 2, only after G-P2` —
> **`02_build_vtec_target.py`** and **`03_verify_processing.py`** (TE:795: *"`03_verify_processing.py`
> appears in the Phase 2 sequence only"*). Across both segments the **distinct** stage
> scripts number **nine**, which is precisely what TE:795's clarification says §12's *"nine
> phase-aware stages"* counts — **an inventory of distinct scripts, not a sequence to
> execute**. Reading it as a sequence produced two defects: run "the nine" inside Phase 1
> and the test executes `02_build_vtec_target.py`, which `governance-guards` classifies
> *"Phase 2 by definition"* and which produces the DCB/STEC/mapping/satellite/arc fields
> §7.0's Phase 1 hard prohibition bars — **the already-green `tests/test_phase_boundary.py`
> would fail**; run the whole two-phase fence and the test executes the Phase 2 segment
> **pre-G-P2**, which the fence forbids in its own comment. Neither reading is available,
> so §13.2's own Phase 1 enumeration is what the test executes.

**CPU is asserted as a complete execution path** (TC-01; Vision §9.2 *"CPU is a complete
execution path, not an emergency mode"*): the sequence runs with **no GPU visible**, and a
run that completes only when a GPU is present **fails**. GPU may accelerate; **no result may
depend on it.**

**The sequence must be executable without a single December hit.** Both fixtures are
December-free by construction (November seven days; March), so `governance-guards` R-25/R-26
record no access, and `features-and-splits` R-82 keeps the locked partition unmaterialised
absent a verified `g05_signature`. A clean run that logs a December access is a defect in
this unit's sequencing, not a governance event.

**The Phase 1 segment's data scope is routed to the gate — and only the data scope.**
Segment *membership* is settled by §13.2 and §7.0 and is corrected above; what §13.2 does
**not** state is what data those seven invocations run over inside the clean-run contract.
TA-17's runtime tolerance is only measurable at whatever scope is fixed, and §15.1 bars
inventing it. The candidates are named with their consequences, **not chosen**:

| Candidate | Consequence |
|---|---|
| **Fixture scale**, via R-137's apparatus partitions | The clean run then contains **no full-year job**, so `test_clean_run.py` never exercises R-140's two-receipt check and control (26) must be asserted on a synthetic tree — which this design already does. Shortest measured runtime; the tolerance frozen at fixture scale says nothing about confirmatory runtime. |
| A **declared reduced window** | A third scope to declare, freeze and cite — a new apparatus constant under R-122, with its own §15.2 identity. |
| **Full year** | Lawful before G-05 — R-82 leaves December unmaterialised, so a pre-G-05 full-year Phase 1 run is January–November by construction — but it is the longest-running candidate, and its measured runtime range **changes again after G-06 adds December**, so a tolerance frozen now would need a second freeze act later. |

A wrong assumption here would freeze a runtime tolerance measured at the wrong scale,
unfixable after freeze without a new act — which is why it is surfaced rather than
resolved. **This item is listed at the gate ahead of any tolerance freeze**: because TA-17's
runtime tolerance is only measurable at whatever scope is fixed, **the data scope must be
ruled before a runtime tolerance is frozen into either manifest**, not alongside it
(`GOV-2026-08-28-FD-01` Recommendations 5 and 47).

**Negative controls.** (18) The sequence **executed out of order** → **fails** — this
control tests **order, not membership**, which is why it never caught the superseded
nine-script reading and why control (39) is added rather than (18) being restated. (19) A
run that **completes only when a GPU is present** → **fails**; CPU is the complete path.
(20) **`PYTHONHASHSEED` unset, or set after the first command** → **fails**, the amended
clause tested as amended rather than assumed. (39, added 2026-08-28 per Recommendation 5) A
clean run that **invokes a Phase-2-only script** — `02_build_vtec_target.py` or
`03_verify_processing.py`, the two §13.2 names appearing only below
`# Phase 2, only after G-P2` — **raises `PhaseBoundaryError`**, `governance-guards`'
exception under R-23/R-24 and one of the **fourteen** (**no fifteenth is minted**; this is a
consumed precondition, not a new declaration). Membership is thereby tested, not assumed.

**Controls that must *not* fire:** the amended sequence in order, on CPU,
`PYTHONHASHSEED=0` first, over §13.2's **seven** Phase 1 invocations → **completes**, and
emits the clean-run log and matched-artifact report WS-20 and TA-17 name; and the
**§15.3 fixture-2 bootstrap at the manifest-declared reduced replicate count** (R-133 limb
5) executes inside that run → **without raising**, neither on `statistical-inference`
R-115's divisibility limb nor on R-120's widening guard.

**Acceptance.** WS-20, TA-17 (primary); TA-03, TA-26 (supporting — the same sequence run on
both platforms).

## R-139 — The comparison ledger: classes declared in the manifest, exactness where §13.7 demands it, no expectation ever updated

**Rule (Q6 = C, second limb).** The clean run **compares**; it does not merely succeed. A
run that exits zero without comparing artifacts satisfies A's shape and fails WS-20's
wording (*"reproduces both fixtures within declared tolerances"*) while appearing green.
So **every required output carries its comparison class in the manifest**, declared per
output at **freeze** time (R-134's workflow), never in a test body:

- **`exact`** for §13.7's five classes — **hashes, schemas, partition membership, IDs, and
  deterministic CPU transformations** — compared for **equality, not tolerance**;
- **`toleranced`** otherwise, against the manifest's **floating-point tolerance** for that
  field, with its **units** declared;
- **runtime and storage** asserted inside the manifest's **measured** ranges — the slot
  where R-120 clause 4's measured widening-guard cost lands, in the range it was measured
  into.

**A mismatch in an `exact`-class artifact raises**, naming file and violated expectation,
and **never updates the expectation** (§13.7's closing sentence; NFR-REP-01). This is not
theoretical: the D-18 re-merge hashed differently from an artifact holding the identical
record set because output order followed directory traversal, and only a sort on the dedup
key made two consecutive runs agree byte for byte (`DATA-17`). Byte-identity is asserted
where §13.7 demands it, not approximated.

**No tolerance, class or expectation lives in a test body** — TC-03e's shape applied to
test apparatus, and R-122's convention read as this unit's own obligation.

**BLK-08 ↓ is checked here rather than inherited silently.** A clean-run tolerance stated
in TECU cannot be checked against output no design path returns to TECU. Until
`evaluation-and-comparison`'s **R-103** joint contract is adopted by **both** halves,
a `toleranced` ledger entry declaring TECU units for an output whose producing path
declares no inverse route is **not freezable**, and the ledger **refuses** it — the R-125
precedent (make the dependence a checked assertion at the surface the register names)
applied at the tolerance surface.

**Negative controls.** (21) A **planted single-bit change in an `exact`-class artifact** →
**fails**. (22) A **tolerance sourced from a test body** rather than the manifest →
**fails** an only-copy check. (23) An `exact`-class mismatch that **updates the expected
value** → **fails**; §13.7's no-silent-update made executable. (24) A **runtime or storage
figure outside the manifest's measured range** → **fails** (TA-17's declared runtime and
storage tolerances). (25) A **`toleranced` entry declaring TECU units for an output whose
producing path declares no inverse route** → **fails** — BLK-08 ↓ checked, not assumed.

**Control that must *not* fire:** a `toleranced` floating-point field differing within its
declared manifest tolerance across two platforms → **passes**, which is the platform
variation §13.7's fixture-derived tolerances exist to admit.

**Acceptance.** WS-20, TA-17 (primary); NFR-REP-01's exact-equality classes are what
control (23) enforces.

## R-140 — Fixture-pass receipts, and an exported two-receipt check for any full-year job

**Rule (Q7 = C).** TE §9.2's rule — **both fixtures pass, in order, before any full-year
job** — is hard and pipeline-enforced, and `services.md` states the posture:
`run_walking_skeleton.py` **enforces** the ordering, it does not merely document it. But
enforcement inside the orchestrator's own process reaches only runs the orchestrator
starts: nothing yet stops a **direct** full-year stage-script invocation, and a Kaggle
session has no memory of a local run. So:

1. **On each fixture pass, `run_walking_skeleton.py` writes a machine-readable
   fixture-pass receipt** — **fixture id, the frozen manifest's hash, the result, and the
   run's registry id** — following the release pattern `services.md` § Ordering contract
   already fixes: *identified by release ID and verified by hash*, never by path
   convention.
2. **One check function consumes both receipts**, verifies each against the **frozen**
   manifest hashes, and asserts **plumbing before scientific**. A **re-frozen manifest
   invalidates old receipts by construction**, which is the behaviour a hash binding buys
   for free.
3. **Its call site in full-year jobs is routed to the gate**, proposed and not applied:
   either a **seventh stage-entry step** — `foundation`'s **approved** six-step surface, so
   a formal `services.md` amendment this stage may not make — or an **in-script assertion
   the nine scripts adopt by contract**. Neither is a `component-methods.md` boundary
   contract, so neither enters the amendment ledger; the `services.md` amendment is
   **noted, not counted** (§ Amendments owed).
4. **Ordering, manifest and receipt violations raise the base `IntegrityError`** with the
   affected file and the violated expectation. **No fifteenth exception is minted by
   default.** The alternative — a `FixtureError` subclass, which R-01's *"any future
   integrity-related exception"* admits and whose catchability R-01's own negative control
   proves — is **named at the gate with its cost stated**: R-01's **"fourteen"** is a
   representation carried in `foundation`'s READY text **and** in
   `regimes-diagnostics-reporting`'s § Assumptions, so minting a fifteenth obliges the
   cross-representation sweep `project.md`'s corrections mandate. Base reuse is the
   default because it changes **no** READY text.

**The receipt set stays exactly two.** The M10 step's result is recorded **in the clean-run
evidence**, never as a third receipt — §9.2's "both" is not extended by the Q12 = C ruling,
and the register says so explicitly.

**Negative controls.** (26) A **scientific-fixture run without a plumbing receipt** →
**raises**. (27) A **full-year invocation without both receipts** → **raises**, asserted
through the check function **on a synthetic tree** (so the control does not depend on which
scope R-138's gate item fixes). (28) A **receipt whose manifest hash disagrees with the
frozen manifest** → **raises**. (29) A **receipt written from a `candidate` manifest** →
**refused at write time** (R-134's evidence bound applied to receipts).

**Control that must *not* fire:** a full-year invocation with both receipts, in order, each
bound to the manifest hash in force → **proceeds**.

**Acceptance.** WS-20, TA-09 (primary); FR-WS-1's *"fixture run log shows plumbing before
scientific before any full-year job"* is exactly what the receipts make checkable.

## R-141 — The Kaggle in-session gate is a producing path, stamped by the platform and bound to the run's own lock

**Rule (Q8 = C).** TC-03g (`binding: hard`) and TE §9.1/§9.2: the **critical test set and
both fixtures** run **inside the Kaggle session** before any governed run executed there,
the result captured in that run's evidence record — because a Kaggle session carries **no
git working tree**, no commit hook fires there, and a local suite run proves nothing about
the environment the governed run actually executes in. REQ-NFR-A3 names the gap NFR-REP-01
leaves: NFR-REP-01 governs *a* clean environment, not *the* platform.

Before any governed Kaggle run, the critical set and both fixtures execute **in-session**
and emit a machine-readable **in-session gate result** carrying:

- the **resolved platform**, taken from `ConfigSnapshot.platform` — resolved by
  `foundation`'s `resolve_platform_roots` detection, **never asserted by the caller**;
- the **§13.1 environment-lock items in force** (code commit, the four configuration
  snapshot hashes, the `requirements.txt` hash and per-run `pip freeze`, versions, input
  dataset and manifest versions, platform, known nondeterministic operations);
- timestamps, and the **per-test and per-fixture results**;
- **its own measured total runtime** — the wall-clock sum of the critical set plus both
  fixtures as executed in that session — **recorded into the
  `environment_and_cpu_preflight_report` at G-07** (R-142 limb 3) *(added 2026-08-28 per
  `GOV-2026-08-28-FD-01` Recommendation 47)*.

**Why a total, when there is nothing to compare it to.** Stated plainly rather than dressed
up as a limit: **no session or wall-clock ceiling exists in any authority.** Verified — the
only quota is the ~30 Kaggle **GPU** hours per week at Vision §4.4, which *"are available but
not required"* and does not bind the CPU path this rule governs, and no unit references a
session limit. **No resource infeasibility was found and none is asserted here.** What this
rule does is make the number **visible at the gate that would care**: because R-141 stacks
the critical set **and both fixtures** ahead of the governed work in one session, a full-year
governed run can carry fixture 2's complete ladder in front of the confirmatory work, and
the per-fixture timestamps already make the total *derivable* — it was simply never
recorded anywhere a reviewer reads. One recorded field closes that, and no ceiling is
invented to check it against.

The governed run's registry evidence record **references that artifact**, and a governed
Kaggle run whose evidence record **lacks** one — or carries one stamped `local` — **fails
before domain work** rather than proceeding silently. The evidence TA-03 and TA-26 need
("install logs from both platforms", "restore on both platforms") is emitted by the same
act that satisfies the rule, so it is a parse rather than a transcription.

**Negative controls.** (30) A **`local`-stamped result offered as in-session evidence** →
**fails on the platform stamp**. (31) A gate result whose **code commit or config-snapshot
hashes disagree with the governed run's own §13.1 lock** → **fails**; the gate proves the
environment of *this* run, not of some earlier session — BENCH-01's substance. (32) A gate
result **predating the frozen manifests in force** → **fails**, the same way a stale
receipt does (R-140's hash binding applied here), so "ran the gate once in August" is a
failure rather than a loophole.

**Control that must *not* fire:** a `kaggle`-stamped gate result whose lock items match the
governed run's own, emitted after the manifests in force were frozen → **admitted as the
run's in-session evidence**.

**Acceptance.** TA-03, TA-26 (supporting — `foundation` and `models-and-baselines`
primary); FR-WS-6 and REQ-NFR-A3 are what these controls test.

## R-142 — The matrix, the bounded acceptance table and the preflight report are generated paths that refuse

**Rule (Q9 = C).** Three evidence artifacts land in this unit's `Owns`, and the acceptance
vocabulary is explicit that evidence is machine-readable or reviewable and **visual
inspection alone is insufficient** (§16). All three are **derivations with refusal
semantics**, never hand-maintained documents:

1. **The traceability matrix (TA-21)** is **generated** from machine-readable sources —
   requirement ids joined to their D-numbers, their test modules and their evidence
   artifact ids — with **completeness asserted against the implemented-requirement list**.
   A row missing any of its **three** mandatory links **fails** rather than rendering
   blank.
2. **The TA-09 acceptance table** is emitted from the fixture-pass receipts and the per-row
   evidence artifacts, **bounded to the 13-row FR-WS-4 set by construction** — **WS-01
   plus WS-09…WS-20**, derived 2026-08-28 by enumerating that set (13 rows; WS-02…WS-08
   deferred, 7 rows; 13 + 7 = 20, agreeing with §16's twenty). The **WS-02–WS-08 deferral
   to G-P3A is stated on the table itself** and is enforced by the emitting path.
3. **The `environment_and_cpu_preflight_report`** is assembled from `foundation`'s §13.1
   environment lock plus the clean-run results, its field set fixed so **G-07's evidence
   column is a parse, not a screenshot**. It additionally records **the in-session gate's
   own measured total runtime** (R-141) *(added 2026-08-28 per `GOV-2026-08-28-FD-01`
   Recommendation 47)*.

> **⚠ Two preflight reports, two gates — the distinction stated rather than blurred**
> *(added 2026-08-28 per `GOV-2026-08-28-FD-01` Recommendation 9, board option 1)*.
>
> | Artifact | Gate it evidences | Designed by |
> |---|---|---|
> | **`environment_and_cpu_preflight_report`** | **G-07 Reproducibility** (Vision:1121, gate table; defined at TE:530 — install from pins on both Kaggle and local, a completed skeleton run, measured CPU runtime, RAM and storage, no GPU-only dependency) | **this unit** — limb 3 above |
> | **`aws_ai_dlc_preflight_report`** | **G-09 Agent preflight** (Vision:1123) — and it is **TA-23's** evidence column (TE:1119) and §18.3's named evidence artifact (TE:1083, *"The evidence artifact is `aws_ai_dlc_preflight_report`"*) | **`foundation`** — **not this unit**, and named nowhere in this unit's three design artifacts because this unit does not build it |
>
> **TA-23's discharging requirement is `foundation`'s, not this unit's**: **FR-WS-7**, whose
> criterion is *"`aws_ai_dlc_preflight_report` shows all four preconditions met"*, is owned
> by `foundation` per `unit-of-work-story-map.md:127` (`| FR-WS-7 | foundation | TA-23 |`).
> This is the **identical discharge pattern** this unit already flags for REQ-ENG-4/TA-09 —
> another unit's requirement passing through one of this unit's rows — and the asymmetry of
> flagging one and not the other is what the finding caught. `foundation` is being amended in
> parallel to own FR-WS-7's discharge onto TA-23 with `aws_ai_dlc_preflight_report` in its
> artifact family; this unit makes no claim on either.
>
> **The supporting-row figure, re-derived 2026-08-28 and printed before assertion.** Read
> from `unit-of-work-story-map.md:239`'s per-unit coverage row —
> `| fixtures-and-reproducibility | 8 | 2 | WS-20, TA-09, TA-17, TA-21 | TA-03, TA-04,
> TA-23, TA-26, TA-27 |` — the supporting set is **TA-03, TA-04, TA-23, TA-26, TA-27 = 5**,
> and **the figure stays 5**: story-map line 206 lists this unit as TA-23's *supporting*
> party with **`foundation` primary** and evidence `aws_ai_dlc_preflight_report`, so dropping
> TA-23 to make the figure 4 would contradict the story map. What is corrected is the
> **claim**, not the count: TA-23 is a supporting row **whose evidence artifact and whose
> discharging requirement are both `foundation`'s**, and this unit's contribution to it is
> the clean-run and gate-test results §18.3's decision criterion consumes — never the
> report.

**The DATA-07 caveat arrives at its last stop**: the report and the matrix each carry the
caveat field wherever a fixture coverage figure appears (R-135's freight), and — since
2026-08-28 — the **`december_representativeness`** field alongside it (R-135 limb 4).

**TA-27 is recorded first-limb-only.** This unit is **supporting evidence for the first
limb** — Phase 1 cannot import raw GNSS modules (`governance-guards` primary, R-23/R-24) —
and the **transition-manifest hash-diff limb is recorded as deferred to G-P2/G-P3C**, never
claimed inside Phase 1. Claiming the second limb here would assert a Phase 2 result from a
Phase 1 artifact.

> **⚠ Control (33) checks a module's *presence*, not its *coverage* — and one existing
> module makes that gap concrete** *(recorded 2026-08-28 per `GOV-2026-08-28-FD-01`
> Recommendation 42; stated as a limitation of this unit's control, not as a claim about
> another unit's design)*. `tests/test_release_hashes.py` **exists** (267 lines) and its
> **name matches the mandated §12 module**, so control (33) passes on it — but derived
> 2026-08-28, `grep -c "dataset_version|mask_id|feature_set_id|row_count|exclusion"` over it
> returns **0**, and `grep -c "overwrite|write_release"` returns **0**. **None of §13.3's
> required manifest fields is covered today and the overwrite refusal is not exercised**, so
> **TA-15 must not be read as covered** on the strength of a matching filename. The matrix
> therefore records **module presence** and **the acceptance row's own evidence artifact**
> as two separate links (limb 1's three mandatory links), and a present-but-non-covering
> module is a **gate disclosure**, not something control (33) can catch. Widening (33) into a
> per-module coverage assertion is **not proposed here**: the §13.3 field contract is
> `foundation`'s (its R-11/R-12/R-13), and asserting another unit's coverage from this unit's
> matrix would be the trespass `project.md`'s corrections warn against.

**Negative controls.** (33) A **matrix row citing a test module absent from the
workspace** → **fails** (today that is 18 of REQ-ENG-4's 21 modules, so the control has
live subjects; **presence only — see the box above**). (34) A **WS row claimed `PASS` without
an evidence link** → **fails**. (35) A **TA-09 table containing any WS-02…WS-08 row** →
**fails**; the deferral is a raise, not a footnote. (36) A **report or matrix carrying a
fixture coverage figure without the DATA-07 caveat field — or, since 2026-08-28, without the
`december_representativeness` field** → **fails**.

**Control that must *not* fire:** a TA-09 table with all 13 rows present, each linked to an
existing evidence artifact, and the deferral stated → **renders**.

**Acceptance.** TA-21, TA-09 (primary); TA-03, TA-27 (supporting) and **TA-23 (supporting —
`foundation` primary, evidence artifact `aws_ai_dlc_preflight_report`, discharging
requirement FR-WS-7, all three `foundation`'s; this unit contributes the clean-run and
gate-test results §18.3's criterion consumes, not the report)**.

---

## Negative-control count, derived not carried

Controls are numbered (1)–(39) above, each counted once at its owning rule. **Re-derived
2026-08-28 after the `GOV-2026-08-28-FD-01` remediation added three**, and printed before
assertion: R-133 **5** — (1)–(4) plus **(37)**, R-134 **4**, R-135 **5** — (9)–(12) plus
**(38)**, R-136 **2**, R-137 **3**, R-138 **4** — (18)–(20) plus **(39)**, R-139 **5**,
R-140 **4**, R-141 **3**, R-142 **4** → 5+4+5+2+3+4+5+4+3+4 = **39 distinct negative
controls**.

**The three added, with their recommendation numbers:** **(37)** R-133 — a
`scientific_1month` manifest missing any of limb 5's three `fixture_bootstrap` fields, or
declaring an indivisible scored range (Recommendation 24); **(38)** R-135 — a fixture-derived
figure reported without `december_representativeness`, from either fixture
(Recommendation 36); **(39)** R-138 — a clean run invoking a Phase-2-only script raises
`PhaseBoundaryError` (Recommendation 5). The prior figure was **36**
(4+4+4+2+3+3+5+4+3+4); 36 + 3 = 39.

**Eleven controls that must *not* fire** are listed separately at their rules and are
**not** in that count: R-133's `not_applicable` Phase 2 block; R-134's provenance-carrying
candidate; R-135's verified November assembly (now asserting **both** caveat fields);
R-136's mislabelled-directory admission; R-137's two (the November `score` containment
inherited from R-74, and the M10 result not counting as a third fixture); R-138's **two** —
the in-order CPU completion over §13.2's **seven** Phase 1 invocations, and the
**reduced-replicate fixture bootstrap executing without raising** (added 2026-08-28 per
Recommendation 24); R-139's within-tolerance platform variation; R-140's two-receipt
full-year pass; R-141's matching `kaggle` gate result. Derivation:
1+1+1+1+2+2+1+1+1 = **11** (previously 10; the R-138 slot went 1 → 2).

## Amendments owed

**Derived against the current chain, and printed before asserted:
5 + 0 + 1 + 1 + 0 + 0 = 7 across 5 units.**

| Source | Owed | Basis |
|---|---|---|
| `external-products` **R-55** | **5**, across **3** units | Derived there (`acquisition` 3, `inventory-and-registry` 1, `external-products` 1), boundary contracts only. Not restated here; a restated count drifts. |
| `features-and-splits` | **0** | Re-derived 2026-08-26 in its § Amendments owed: its three dissolved into ADR-11. |
| `evaluation-and-comparison` | **1** | The BLK-08 resolution package (its R-103), one consolidated amendment. |
| `statistical-inference` | **1** | The R-118 signature amendment. |
| `regimes-diagnostics-reporting` | **0** | Re-verified 2026-08-28 by reading its § Amendments owed, which prints exactly the 5 + 0 + 1 + 1 + 0 = 7-across-5 derivation this row carries forward. |
| **This unit** | **0** | **No amendment today.** This unit changes no approved boundary signature: `run_walking_skeleton.py` is a **script row in `services.md`**, the manifests are **data**, and every shape here — loader, ledger, receipts, gate result, emitters, apparatus partitions — is intra-unit or test apparatus under Depth **Q1 = B**. |
| | **7 across 5 units** | 5 + 0 + 1 + 1 + 0 + 0 — the total stands unchanged |

**One honest conditional, stated rather than absorbed.** If the gate places the manifest
loader in `foundation`'s `src/data/` as a **cross-unit contract** (R-133's first candidate),
that placement mints a new `component-methods.md` boundary surface and the ledger takes
**+1, to 8 across 6, at that ruling** — counted **then, not now**, because the alternative
home (a test-apparatus helper under `tests/fixtures/`) adds none.

**What the other gate items do to the ledger — nothing, and why.** R-140's
**seventh-stage-entry-step** candidate would amend `services.md`'s approved **stage entry
contract**: a formal amendment, but **not** a `component-methods.md` boundary contract, the
only class this ledger tracks — **noted, not counted**. R-137's M10 placement and R-138's
data scope are **§13.2 sequence text**, the authority document's. R-136's acceptance rows
are **Vision §15.2 amendments** owned by the owner/supervisor. R-133's `not_applicable`
reading is a **§15.2 reading** proposed to the owner. None is a boundary contract.

## Requirement coverage

| Requirement | Rules | Acceptance |
|---|---|---|
| FR-WS-1 | R-140 (the two receipts and the exported order check), R-134 (identity cited from D-11/D-14) | WS-20, TA-09 (primary) |
| FR-WS-2 | R-136 (the `smoke_only` stamp emitted by the producing path plus absence assertions on every evidence surface), R-142 (control 33–36's surfaces) | ⚠ **no row** — `UNTESTED`; contract-level control lands in R-136 control (13); candidate §15.2 row **proposed at the gate, never applied** |
| FR-WS-3 | R-136 (record-date assembly assertion, consuming `acquisition` R-31 and `test_acquisition_window.py`'s predicate) | ⚠ **no row** — `UNTESTED`; contract-level control lands in R-136 control (14); candidate §15.2 row **proposed at the gate, never applied** |
| FR-WS-4 | R-142 (TA-09 bounded to the 13-row set by construction; the WS-02–WS-08 deferral a raise) | WS-01, WS-09…WS-20 (13 rows) |
| FR-WS-5 | R-138 (the amended §13.2 sequence, CPU the complete path), R-139 (the comparison ledger) | WS-20, TA-17 (primary) |
| FR-WS-6 | R-141 (the in-session gate as a producing path) | TA-03, TA-26 (supporting) |
| NFR-REP-01 | R-139 (§13.7's exact-equality classes; the no-silent-update raise), R-138 | WS-20, TA-17 (primary) |
| REQ-NFR-A3 | R-141 (the platform stamp and the staleness bound) | TA-03 (supporting) |

**8 requirements, 2 untested — derived 2026-08-28 by filtering the story map's Table 1 on
this unit (eight rows) and set-differencing the untested list, the per-unit coverage
summary row agreeing (`8 / 2 / WS-20, TA-09, TA-17, TA-21 / TA-03, TA-04, TA-23, TA-26,
TA-27`).** The two without acceptance rows, by ID: **FR-WS-2, FR-WS-3**. Each one's
contract-level control lands in R-136; **every §15.2 acceptance-row proposal is a gate
item — proposed, never applied here**. The two-untested figure is never silently narrowed:
designed falsifiers now, acceptance rows by owner amendment.

**Two requirements not carried here but discharging onto this unit's rows, named so neither
is mistaken for a ninth.** *(The second was added 2026-08-28 per `GOV-2026-08-28-FD-01`
Recommendation 9: the design flagged one instance of this discharge pattern in every
artifact and left the identical second instance silent, and the asymmetry was the tell.)*

1. **REQ-ENG-4** is `foundation`'s requirement and its acceptance row is **TA-09 — this
   unit's primary row**. The manifest schema R-133 designs is therefore the mechanism by
   which another unit's requirement passes its acceptance check.
2. **FR-WS-7** is `foundation`'s requirement (`unit-of-work-story-map.md:127`,
   `| FR-WS-7 | foundation | TA-23 |`) and its acceptance row is **TA-23 — this unit's
   *supporting* row**. Its criterion is *"`aws_ai_dlc_preflight_report` shows all four
   preconditions met"*, and **that artifact is `foundation`'s, evidencing G-09** — **not**
   this unit's `environment_and_cpu_preflight_report`, which evidences **G-07**. This unit
   contributes the clean-run and gate-test results §18.3's decision criterion consumes; it
   does not build the report, and `aws_ai_dlc_preflight_report` appears nowhere in this
   unit's three design artifacts for exactly that reason. See R-142's two-report box.

Neither requirement is this unit's and neither is counted in the eight. **The supporting-row
figure re-derived 2026-08-28 from `unit-of-work-story-map.md:239` is 5** — TA-03, TA-04,
TA-23, TA-26, TA-27 — and **stays 5**, because line 206 lists this unit as TA-23's
supporting party; what the remediation corrected is the *claim* attached to TA-23, not the
count.

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence: the siblings close at **R-132** (re-derived 2026-08-28 by extracting every `^## R-` heading from all eleven sibling files — 128 distinct headings, numeric maximum R-132), so this unit opens at **R-133** and closes at **R-142** — **10 rules, derived by numbering this file's own headings**. The **R-83…R-89 gap** is inherited as observed, not explained. **The 2026-08-28 remediation of `GOV-2026-08-28-FD-01` added no rule**: all seven applied items land inside R-133, R-134, R-135, R-138, R-141 and R-142, so the rule count stays **10** and the negative-control count moves **36 → 39** (derived in § Negative-control count).
- **[assumption]** Depth **Q1 = B**: this unit has **no approved cross-package boundary signature of its own** in `component-methods.md` — `run_walking_skeleton.py` is a script row in `services.md` and the manifests are data — so the schema, the loader, the comparison ledger, the receipts, the in-session gate result, the apparatus partitions and the three evidence emitters are **intra-unit or test-apparatus shapes this stage specifies**, names indicative, finalized in `domain-entities.md`.
- **[assumption]** **No fifteenth exception is minted by default**: ordering, manifest, receipt, ledger and gate-result violations raise the base **`IntegrityError`** naming file and violated expectation, catchable by `foundation`'s stage-entry contract exactly as R-01's negative control proves. The **`FixtureError`** alternative is a named gate item (R-140) with its cost stated: R-01's **"fourteen"** is a representation carried in `foundation`'s READY text and in `regimes-diagnostics-reporting`'s § Assumptions, and minting obliges the cross-representation sweep `project.md`'s corrections mandate.
- **[assumption]** The frozen identities are **cited, never re-derived**: **D-11** (window 2022-11-01…07 inclusive, with its mandatory not-representative-of-December limitation and the provisional-Dst selection-only restriction), **D-20** (station **BSHM 32/35**), **D-14** (the scientific window — **March 2022, all three cells**, with its **Mandatory limitation in both clauses**: (i) the equinox-month clause, *"does not reproduce December's winter-solstice regime or its activity distribution"*, **and** (ii) the operative prohibition, *"It is **not** representative of the locked test month, and **no fixture result may be read as evidence about December behaviour**"* — clause (ii) enumerated at every site from 2026-08-28 per `GOV-2026-08-28-FD-01` Recommendation 36, having previously appeared **0 times across all 48 stage artifacts** while being the only barrier between a March number and a December reading, since R-136's `smoke_only` quarantine is correctly scoped to `plumbing_7day` alone). Any record stating the scientific window *"remains open under Q-31"* is **stale on disk** — corrected 2026-08-22 under `UG-08`, frozen by `CR-2026-08-21-FREEZES`.
- **[assumption]** TA-04's fixture obligations run on `inventory-and-registry`'s and `foundation`'s tooling (hash manifests, station registry, schema validation) invoked over this unit's fixtures; this unit provides the fixture runs, receipts and logs and **re-implements no hashing** — the single hashing home is `src/data/release.py`.
- **[assumption]** The schema carries the cross-unit slots the READY siblings already rely on (R-120 clause 4's measured widening-guard runtime; R-121's fixture-derived tolerances; R-122's general `tests/fixtures/<fixture_id>/fixture_manifest.yaml` convention). Whether any sibling's synthetic fixture warrants its own `tests/fixtures/` directory is **that sibling's §12 question**, not this one's.
- **Conflict raised, not resolved — the §15.2 content-area count.** Derived: §15.2's table has **13 rows including its `Area` header → 12 content areas**; `requirements.md` REQ-ENG-4 asserts **thirteen** and enumerates **nine**, the three missing being **Processing**, **Units** and **Independent reference checks** (9 + 3 = 12). This stage's own question file and its receipted summary carry the **thirteen**. R-133 binds to the **named twelve** so the block set is correct regardless; correcting REQ-ENG-4 is a `requirements.md` change and correcting the receipted summary is not this stage's either. **Reported at the gate, not applied.**
- **Conflict raised, not resolved — three §15.2 areas name Phase 2 quantities Phase 1 is barred from producing.** Inputs, Processing and Independent reference checks. Requiring them **non-empty** on a Phase 1 manifest would demand exactly the raw-processing evidence §7.0 bars — the §16 "all 20" contradiction in a second place. **Reading proposed** (block present, Phase 2-only quantities recorded `not_applicable` with reason, on the FR-P1-03-5 precedent), **not applied**.
- **Verification obligations owned here:** controls **(1)–(39)**, enumerated per rule and counted in § Negative-control count, plus the **eleven** must-not-fire controls listed there; the twelve-area per-area enumeration; the §15.4 completeness assertion against **20/19** hash-listable outputs; the single-loader only-copy check; the **§15.3 reduced-replicate `fixture_bootstrap` declaration with its scored range and its 24 h / 48 h block counts**; the candidate/frozen states with per-measured-field provenance; the one-station assembly raise and the eligibility re-verification; the `smoke_only` stamp, the **`december_representativeness` field on both fixtures**, and the record-date assertion; the apparatus-partition quarantine and the M10 sequence step; the **verbatim amended §13.2 execution over its seven Phase 1 invocations, with the Phase 2 segment deferred to G-P2 and a Phase-2-only invocation raising `PhaseBoundaryError`**, and the CPU-complete-path assertion; the ledger's `exact`/`toleranced` classes and the no-silent-update raise; the two receipts and the exported order check; the platform-stamped in-session gate result **with its own measured total runtime recorded at G-07**; the three generated evidence artifacts with refusal semantics.
- **Governance dependencies owned outside this unit:** **the two manifest freeze acts** — the promotion of measured values from `candidate` to `frozen` — are the **project owner's under Q-31** (TE §18.2 assigns fixture station, dates and tolerances to the Student), and **nothing here performs them**; **BLK-03/BLK-04/BLK-08/BLK-09**'s contract approvals at their owning units' 3.1 gates — until **BLK-08**'s R-103 joint contract is adopted by both halves, no TECU-stated clean-run tolerance is checkable and R-139 control (25) is what keeps that checked rather than silent; **the loader's home** (R-133) and **the full-year check's call site** (R-140) — `foundation`'s and `services.md`'s surfaces, **proposed not applied**; **the Phase 1 segment's clean-run data scope** (R-138 — owner ruling; **this item must be ruled BEFORE any runtime tolerance is frozen**, since TA-17's tolerance is only measurable at whatever scope is fixed — `GOV-2026-08-28-FD-01` Recommendations 5 and 47; **segment membership is no longer open**, being settled by §13.2 and §7.0 and corrected 2026-08-28); **the classification of the §15.3 reduced replicate count** (R-133 limb 5 — apparatus constant under R-122, or a predeclared `experiment.yaml` named run under R-118's pattern if the owner rules a replicate count is protocol wherever it appears); **the fixture-partition reading and the M10 placement** (R-137 — WS-12/WS-13 evidence semantics and §13.2's sequence text); **the FR-WS-2/FR-WS-3 candidate acceptance rows** (R-136 — Vision §15.2, owner/supervisor); **the §15.2 twelve-versus-thirteen correction and the `not_applicable` reading** (R-133); **`statistical-inference`'s R-120 comparator amendment** (that the widening comparator use the *same* replicate count as its primary call rather than the literal 10,000 — being amended there in parallel; this unit does not make it and does not depend on having made it); **`dataset_version`'s encoding** — **the release path is blocked on it**: `foundation` R-12 records idempotence **PROVIDED** and injectivity **NOT YET ESTABLISHED**, so **`write_release` cannot be implemented until the encoding is a D-number decision** ⚠ **SUPERSEDED 2026-08-28 by D-29** (`GOV-2026-08-28-FD-01` Rec 42, board option 2, owner-approved): the **encoding** is specified — the first **12 hex** of `content_hash` — and **injectivity is established by verify-on-write**, `write_release` refusing a prefix that already names a different `content_hash`. The **`verify_release` amendment** is discharged in substance (the read-back hole closes on the write path) with **no change to that functions signature claimed**. **No release ledger is introduced.** Release immutability never depended on any of this. ⚠ **TA-15 remains NOT covered** — `tests/test_release_hashes.py` still exercises none of §13.3s manifest fields and not R-13s overwrite refusal.. The board recommended a **fixed-length prefix plus a recorded collision bound and a verify-on-write uniqueness check** (which would also discharge the `verify_release` amendment `foundation` R-12 lists as open); the alternative is the **full 64-hex `content_hash`**. ~~**The owner has NOT ruled it and no encoding is invented here**~~ ⚠ **SUPERSEDED 2026-08-28 by D-29** (`GOV-2026-08-28-FD-01` Rec 42, board option 2, owner-approved): the **encoding** is specified — the first **12 hex** of `content_hash` — and **injectivity is established by verify-on-write**, `write_release` refusing a prefix that already names a different `content_hash`. The **`verify_release` amendment** is discharged in substance (the read-back hole closes on the write path) with **no change to that functions signature claimed**. **No release ledger is introduced.** Release immutability never depended on any of this. ⚠ **TA-15 remains NOT covered** — `tests/test_release_hashes.py` still exercises none of §13.3s manifest fields and not R-13s overwrite refusal. (`GOV-2026-08-28-FD-01` Recommendation 42; TE §13.3; TA-15). Related and recorded at R-142: `tests/test_release_hashes.py` exists and its name matches the mandated module, but derived 2026-08-28 it covers **none** of §13.3's required manifest fields and does not exercise the overwrite refusal — **TA-15 must not be read as covered**; **the `raw_isprint_cache/` re-acquisition** that alone discharges the DATA-07 caveat (FU-1 = B, sequenced after requirements-analysis); **`aws_ai_dlc_preflight_report` and FR-WS-7** — **`foundation`'s**, evidencing **G-09**, distinct from this unit's `environment_and_cpu_preflight_report` which evidences **G-07** (R-142's box; Recommendation 9); **G-07 Reproducibility (Blocked, Supervisor)** — the gate that actually accepts WS-20/TA-17's evidence, due before thesis submission; **G-09 Agent preflight (Supervisor)** — ⚠ **SIGNED 2026-08-28 (D-31)** with its own §18.3 preconditions UNMET, and the gate before which no affected component may be coded; **G-05** and **G-06** as the freeze events the receipts and evidence records reference; **G-P3A** as the gate that accepts WS-02–WS-08 and **G-P2/G-P3C** for TA-27's second limb.
- **Open — BLK-02 is not closed by this design.** The manifests' design is specified here; **the manifests do not exist, neither fixture has ever run, and no measured value exists or is claimed.** BLK-02 closes only when the authoritative manifests exist, are hash-verifiable, and the fixtures have actually run under the frozen identities — acts gated by **G-09**, stage 3.5, and the **Q-31** freeze authority. ARUC's one-bin shortfall stays **dormant, not discharged**, with its reactivation condition intact.
- **Open — the four inherited blockers are EXIT conditions on this stage.** **BLK-03 ↓, BLK-04 ↓, BLK-08 ↓, BLK-09 ↓** remain open; nothing in this file closes any of them; this unit **may not complete or exit 3.1** while any stands, and **no implementation may proceed** while they stand.
- **G-09 is not signed.** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated **G-09 ground** no longer holds. **Creation remains barred — on the blocker ground**, the blockers being exit conditions untouched by D-31; G-09 is simply no longer among the grounds, and nothing here authorises a creation the blockers still bar. (Swept 2026-08-30 to every occurrence in these three artifacts, on the terminal-pass Critical finding that the 2026-08-30 line-97 repair reached one occurrence of four.) **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged. No rule here authorises creating `scripts/run_walking_skeleton.py`, either `fixture_manifest.yaml`, `tests/test_clean_run.py`, any receipt or evidence emitter, or a `tests/fixtures/` directory. Workspace inspection 2026-08-28: `tests/` holds three modules, none this unit's; no `tests/fixtures/` directory; `src/`, `configs/` and `pyproject.toml` absent. **TE §18.3's stop-and-report rule binds every affected component while any P0 decision is unresolved** — and where a required value is unfrozen, this design stops and reports rather than choosing a default.
- **None** of the above decides a scientific value. Window, station, month, seeds, partitions, folds and grids are frozen elsewhere (D-11, D-20, D-14, `seeds.yaml`, R-80) or **measured under §15.1 and frozen by the Q-31 authority**; **nothing in these three artifacts states a measured number**, and everything underdetermined is expressly routed to the gate.

---

> **Re-confirmation receipt, 2026-08-29 — `fixtures-and-reproducibility`.** The 2026-08-27T21:49:36Z REDO jump reset every unit's
> receipt floor, and this unit's content had already changed after that floor under the 2026-08-28
> post-execution pass (D-29 through D-32; **G-09 signed under D-31 with its TE §18.3 preconditions
> disclosed unmet**). The owner re-confirmed that post-execution content via the Consolidated
> Summary Confirmation at the foot of `functional-design-questions.md`, receipted `2026-08-29`.
> **No line above this marker was touched by this pass**, no count was re-derived, and nothing here
> discharges TA-15, WS-18 or TA-18, creates `aws_ai_dlc_preflight_report`, or alters the fact that
> stage 3.1 remains **FAIL** with no board having passed it.
